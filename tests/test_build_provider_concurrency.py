import asyncio
from collections import Counter
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from scripts import build_experiment_cache as build
from hyperrag import llm
from hyperrag.storage import JsonKVStorage
from hyperrag.utils import compute_args_hash


def test_actual_calls_respect_total_limit_and_key_reservations(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER_CONFIG", raising=False)
    monkeypatch.setenv("LLM_KEY_ATTEMPTS", "2")
    active = Counter()
    peaks = Counter()
    total_peak = 0
    attempts = Counter()

    async def fake(model, prompt, api_key=None, **kwargs):
        nonlocal total_peak
        attempts[prompt] += 1
        active[api_key] += 1
        peaks[api_key] = max(peaks[api_key], active[api_key])
        total_peak = max(total_peak, sum(active.values()))
        try:
            await asyncio.sleep(0.002)
            if attempts[prompt] == 1:
                raise RuntimeError("gateway error")
            return "[]"
        finally:
            active[api_key] -= 1

    monkeypatch.setattr(build, "openai_complete_if_cache", fake)

    async def run():
        fn = build.build_llm_func(model="test", base_url=None, api_keys=["a", "b", "c"], timeout=1, max_async=2)
        assert await asyncio.gather(*(fn(str(i)) for i in range(30))) == ["[]"] * 30

    asyncio.run(run())
    assert total_peak == 2
    assert all(peak == 1 for peak in peaks.values())
    assert sum(active.values()) == 0


def test_reasoning_only_short_summary_reuses_original_text_without_caching(tmp_path, monkeypatch):
    class ReasoningOnlyStream(FakeStream):
        async def events(self):
            yield SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=None, reasoning_content="budget used for reasoning"), finish_reason="length")])

    create = AsyncMock(return_value=ReasoningOnlyStream())
    close = AsyncMock()
    monkeypatch.setattr(llm, "AsyncOpenAI", lambda **kwargs: SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)), close=close))

    async def run():
        cache = JsonKVStorage(namespace="llm_response_cache", global_config={"working_dir": str(tmp_path)})
        result = await llm.openai_complete_if_cache("test", "summary", hashing_kv=cache, aggregate_stream=True, allow_length_finish=True, max_tokens=100)
        assert result is None
        assert await cache.all_keys() == []
        close.assert_awaited_once()

    asyncio.run(run())


def test_cache_hits_do_not_consume_rotation_or_make_requests(tmp_path, monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER_CONFIG", raising=False)
    used = []

    async def fake(model, prompt, api_key=None, **kwargs):
        used.append(api_key)
        return "network"

    monkeypatch.setattr(build, "openai_complete_if_cache", fake)

    async def run():
        cache = JsonKVStorage(namespace="llm_response_cache", global_config={"working_dir": str(tmp_path)})
        await cache.upsert({compute_args_hash("test", [{"role": "user", "content": "cached"}]): {"return": "saved"}})
        fn = build.build_llm_func(model="test", base_url=None, api_keys=["a", "b"], timeout=1)
        for _ in range(40):
            assert await fn("cached", hashing_kv=cache) == "saved"
        assert await fn("new", hashing_kv=cache) == "network"

    asyncio.run(run())
    assert used == ["a"]


def test_cancelled_request_releases_http_slot_and_key(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER_CONFIG", raising=False)
    entered = asyncio.Event()

    async def fake(model, prompt, **kwargs):
        if prompt == "cancel":
            entered.set()
            await asyncio.Event().wait()
        return "ok"

    monkeypatch.setattr(build, "openai_complete_if_cache", fake)

    async def run():
        fn = build.build_llm_func(model="test", base_url=None, api_keys=["a"], timeout=1, max_async=1)
        task = asyncio.create_task(fn("cancel"))
        await entered.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert await asyncio.wait_for(fn("after"), 1) == "ok"

    asyncio.run(run())


class FakeStream:
    def __init__(self, finish="stop", broken=False):
        self.finish = finish
        self.broken = broken

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    def __aiter__(self):
        return self.events()

    async def events(self):
        yield SimpleNamespace(choices=[])
        yield SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="[", reasoning_content="thinking"), finish_reason=None)])
        if self.broken:
            raise RuntimeError("disconnected")
        yield SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="]"), finish_reason=self.finish)])


@pytest.mark.parametrize("finish,broken,succeeds", [("stop", False, True), (None, False, False), ("length", False, False), ("stop", True, False)])
def test_stream_caches_only_complete_answers(tmp_path, monkeypatch, finish, broken, succeeds):
    create = AsyncMock(return_value=FakeStream(finish, broken))
    close = AsyncMock()
    monkeypatch.setattr(llm, "AsyncOpenAI", lambda **kwargs: SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)), close=close))

    async def run():
        cache = JsonKVStorage(namespace="llm_response_cache", global_config={"working_dir": str(tmp_path)})
        key = compute_args_hash("test", [{"role": "user", "content": "prompt"}])
        if succeeds:
            result = await llm.openai_complete_if_cache("test", "prompt", hashing_kv=cache, aggregate_stream=True, return_metadata=True)
            assert result["content"] == "[]"
            assert result["reasoning_content"] == "thinking"
            assert (await cache.get_by_id(key))["return"] == "[]"
            assert await llm.openai_complete_if_cache("test", "prompt", hashing_kv=cache) == "[]"
            assert create.await_count == 1
        else:
            with pytest.raises(RuntimeError):
                await llm.openai_complete_if_cache("test", "prompt", hashing_kv=cache, aggregate_stream=True)
            assert await cache.get_by_id(key) is None
        close.assert_awaited_once()

    asyncio.run(run())
