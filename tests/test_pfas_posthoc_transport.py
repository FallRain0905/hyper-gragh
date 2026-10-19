import asyncio
from pathlib import Path
from unittest.mock import patch

from hyperche.normalization import posthoc_cache as core
from scripts import normalize_cache_posthoc as cli


def test_available_credentials_cannot_overlap_when_fast_worker_reuses_pool():
    async def run():
        pool = core.AsyncLLMEndpointPool(
            [core.LLMEndpoint("https://example.test", str(i)) for i in range(3)], name="test"
        )
        slow = await pool.acquire()
        for _ in range(12):
            fast = await pool.acquire()
            assert fast != slow
            pool.release(fast)
        assert len(pool.active_leases) == 1
        pool.release(slow)
        assert pool.available.qsize() == 3
        leased = [await pool.acquire() for _ in range(3)]
        waiter = asyncio.create_task(pool.acquire())
        await asyncio.sleep(0)
        assert not waiter.done()
        pool.release(leased[0])
        assert await waiter == leased[0]
        for credential in leased:
            pool.release(credential)
    asyncio.run(run())


def test_provider_caps_hold_under_uneven_completion_times():
    async def run():
        endpoints = [
            core.LLMEndpoint("https://ali", f"a{i}") for i in range(15)
        ] + [
            core.LLMEndpoint("https://tree", f"t{i}") for i in range(20)
        ]
        pool = core.AsyncLLMEndpointPool(
            endpoints,
            name="capped",
            provider_max_async={"https://ali": 10, "https://tree": 10},
        )
        active = {"https://ali": 0, "https://tree": 0}
        peak = {"https://ali": 0, "https://tree": 0}

        async def worker(i):
            endpoint = await pool.acquire()
            url = endpoint.base_url
            active[url] += 1
            peak[url] = max(peak[url], active[url])
            await asyncio.sleep(0.003 if i % 3 else 0.012)
            active[url] -= 1
            pool.release(endpoint)

        await asyncio.gather(*(worker(i) for i in range(80)))
        assert peak == {"https://ali": 10, "https://tree": 10}
        assert not pool.active_leases and pool.available.qsize() == 35

    asyncio.run(run())


def test_pfas_pair_prompt_contains_source_chunks_and_original_evidence():
    cid = "PFAS_002_CHK_003"
    graph = {"v_data": {name: {"source_id": cid, "description": name, "entity_type": "PFAS_TARGET"}
                         for name in ("PFOA", "perfluorooctanoic acid")},
             "e_data": {("PFOA", "perfluorooctanoic acid"): {"source_id": cid}}}
    chunks = {cid: {"content": "PFOA (perfluorooctanoic acid) removal", "full_doc_id": "PFAS_002"}}
    features, _, _ = core.build_context_index(graph, chunks)
    pair = {"left_id": "PFOA", "right_id": "perfluorooctanoic acid",
            "left_features": core.asdict(features["PFOA"]),
            "right_features": core.asdict(features["perfluorooctanoic acid"])}
    prompt, supplied = core._context_for_pair(pair, graph, chunks)
    assert supplied == [cid]
    assert "PFAS_002" in prompt and chunks[cid]["content"] in prompt
    assert core.extract_ids({"source_id": "RFB_001_CHK_001"}, core.CHUNK_ID_PATTERN) == ["RFB_001_CHK_001"]


def test_gateway_and_broken_stream_errors_are_retryable():
    assert core._is_retryable_judge_exception(RuntimeError("Incomplete extraction stream: finish_reason=None"))
    from tenacity import RetryError
    from concurrent.futures import Future
    from openai import InternalServerError
    import httpx
    fut = Future()
    response = httpx.Response(504, request=httpx.Request("POST", "https://example.test"))
    fut.set_exception(InternalServerError("gateway", response=response, body=None))
    assert core._is_retryable_judge_exception(RetryError(fut))
    assert not core._is_retryable_judge_exception(ValueError("invalid evidence id"))


def test_direct_and_wrapped_stream_transport_errors_are_retryable():
    from concurrent.futures import Future
    from tenacity import RetryError
    import httpx

    request = httpx.Request("POST", "https://example.test")
    for error in (httpx.ReadError("", request=request),
                  httpx.RemoteProtocolError("stream closed", request=request)):
        assert core._is_retryable_judge_exception(error)
        future = Future()
        future.set_exception(error)
        assert core._is_retryable_judge_exception(RetryError(future))
    assert not core._is_retryable_judge_exception(httpx.UnsupportedProtocol("invalid URL"))


def test_read_error_retries_and_releases_credentials_before_success():
    import httpx

    async def run():
        cid = "PFAS_002_CHK_003"
        graph = {"v_data": {
            name: {"source_id": cid, "description": name, "entity_type": "PFAS_TARGET"}
            for name in ("PFOA", "perfluorooctanoic acid")
        }, "e_data": {}}
        chunks = {cid: {"content": "PFOA (perfluorooctanoic acid)", "full_doc_id": "PFAS_002"}}
        features, _, _ = core.build_context_index(graph, chunks)
        pair = {"pair_id": core._pair_id("PFOA", "perfluorooctanoic acid"),
                "left_id": "PFOA", "right_id": "perfluorooctanoic acid",
                "left_features": core.asdict(features["PFOA"]),
                "right_features": core.asdict(features["perfluorooctanoic acid"])}
        pool = core.AsyncLLMEndpointPool([
            core.LLMEndpoint("https://example.test", "fake-a"),
            core.LLMEndpoint("https://example.test", "fake-b"),
        ], name="read-error-test")
        calls = []

        async def complete(*args, **kwargs):
            assert len(pool.active_leases) == 1
            calls.append(kwargs["api_key"])
            if len(calls) == 1:
                raise httpx.ReadError("", request=httpx.Request("POST", "https://example.test"))
            return {"finish_reason": "stop", "content":
                    '{"decision":"ALIAS","confidence":0.99,"canonical_name":"PFOA",'
                    '"preferred_name_source":"A","reason":"Explicit expansion in evidence",'
                    '"evidence_chunk_ids":["PFAS_002_CHK_003"]}'}

        with patch("hyperrag.llm.openai_complete_if_cache", complete):
            result = await core._call_llm_judgement(
                pair, graph, chunks, {}, model="test-model", base_url="https://example.test",
                key_pool=pool, timeout=1, semaphore=asyncio.Semaphore(1), attempts_per_pair=2,
            )
        assert result["status"] == "ok" and result["api_attempts"] == 2
        assert result["evidence_chunk_ids"] == [cid]
        assert len(calls) == 2 and calls[0] != calls[1]
        assert not pool.active_leases and pool.available.qsize() == 2

    asyncio.run(run())


def test_repeated_truncation_gets_enough_budget_for_valid_final_answer():
    async def run():
        pool = core.AsyncLLMEndpointPool([
            core.LLMEndpoint("https://example.test", f"fake-{i}") for i in range(3)
        ], name="truncation-test")
        calls = []

        async def complete(*args, **kwargs):
            calls.append(kwargs)
            if kwargs["max_tokens"] < 10000:
                raise RuntimeError("Incomplete extraction stream: finish_reason='length'")
            return {"finish_reason": "stop", "content":
                    '{"decision":"DIFFERENT","confidence":0.99,"canonical_name":null,'
                    '"preferred_name_source":"NONE","reason":"Distinct forms in evidence",'
                    '"evidence_chunk_ids":["PFAS_002_CHK_003"]}'}

        with patch("hyperrag.llm.openai_complete_if_cache", complete), \
             patch.object(core, "_context_for_pair", return_value=("evidence", ["PFAS_002_CHK_003"])), \
             patch.object(core, "_pair_context_hash", return_value="test-context"):
            result = await core._call_llm_judgement(
                {"pair_id": "test-pair"}, {}, {}, {}, model="test-model",
                base_url="https://example.test", key_pool=pool, timeout=1,
                semaphore=asyncio.Semaphore(1), attempts_per_pair=3,
            )
        assert result["status"] == "ok" and result["api_attempts"] == 3
        assert result["finish_reason"] == "stop"
        assert result["evidence_chunk_ids"] == ["PFAS_002_CHK_003"]
        assert len(calls) == 3 and max(x["max_tokens"] for x in calls) <= 16384
        assert all(x["reasoning_effort"] == "low" for x in calls)
        assert not pool.active_leases and pool.available.qsize() == 3

    asyncio.run(run())


def test_failed_judgements_prevent_rewrite_and_preserve_resume_state():
    async def judge(*args, **kwargs):
        return {"api_errors": 1, "completed_calls": 2}
    args = cli._parser().parse_args(["--source-cache", "source", "--target-cache", "target"])
    with patch.object(cli.core, "judge_candidates", judge), patch.object(cli, "_keys", return_value=["fake"]), \
         patch.object(cli, "_mark") as mark, patch.object(cli, "_merge_api_stats"):
        try:
            asyncio.run(cli._judge_stage(Path("unused"), args))
        except RuntimeError:
            pass
        else:
            raise AssertionError("failed judgements passed the gate")
        assert mark.call_args.args[2] == "incomplete"
