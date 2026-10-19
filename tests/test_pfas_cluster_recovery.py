import asyncio
import itertools
import json
from unittest.mock import patch

import pytest

from hyperche.normalization import posthoc_cache as core
from scripts import normalize_cache_posthoc as cli


def test_case_only_ids_remain_unique_after_both_hash_fallbacks_collide():
    names = ("A", "Total Fluorine", "total fluorine")
    features = {name: core.extract_features(name, {"entity_name": "total fluorine", "entity_type": "METRIC"})
                for name in names}
    with patch.object(core, "stable_hash", return_value="fb31dd72"):
        result = core._build_map_payload(features, [[n] for n in names], [], core.AliasRegistry(),
                                         merge_confidence=0.9)
        repeated = core._build_map_payload(features, [[n] for n in names], [], core.AliasRegistry(),
                                           merge_confidence=0.9, previous=result)
    ids = [r["canonical_id"] for r in result["clusters"]]
    assert len(set(ids)) == 3
    assert ids == [r["canonical_id"] for r in repeated["clusters"]]
    assert [r["members"] for r in result["clusters"]] == [[n] for n in names]


def test_cluster_truncation_retries_with_bounded_budget_and_releases_keys():
    async def run():
        pool = core.AsyncLLMEndpointPool([core.LLMEndpoint("https://example.test", f"fake-{i}")
                                          for i in range(3)], name="cluster-test")
        calls = []

        async def complete(**kwargs):
            calls.append(kwargs)
            assert len(pool.active_leases) == 1
            if kwargs["max_tokens"] < 16384:
                raise RuntimeError("Incomplete extraction stream: finish_reason='length'")
            return {"content": json.dumps({"valid": True, "reason": "Same entity in supplied evidence",
                                            "weakest_pair_id": None}), "finish_reason": "stop"}

        with patch("hyperrag.llm.openai_complete_if_cache", complete), \
             patch.object(core, "_cluster_audit_prompt", return_value=("unchanged evidence", "cluster:test")):
            result = await core._call_cluster_audit([], {}, [], {}, model="deepseek-v4.1-flash",
                                                     base_url="https://example.test", key_pool=pool, timeout=1)
        assert result["status"] == "ok" and result["api_attempts"] == 3
        assert [r["max_tokens"] for r in calls] == [4096, 8192, 16384]
        assert all(r["reasoning_effort"] == "low" for r in calls)
        assert not pool.active_leases
    asyncio.run(run())


def _cluster_fixture(tmp_path):
    source, work = tmp_path / "source", tmp_path / "work"
    source.mkdir()
    work.mkdir()
    cid = "PFAS_001_CHK_001"
    nodes = {name: {"entity_name": name, "entity_type": "OTHER", "source_id": cid} for name in ("alpha", "beta", "gamma")}
    graph = {"v_data": nodes, "e_data": {}}
    chunks = {cid: {"content": "alpha, beta and gamma refer to the same object", "full_doc_id": "PFAS_001"}}
    features, _, _ = core.build_context_index(graph, chunks)
    decisions = [{"pair_id": core._pair_id(a, b), "left_id": a, "right_id": b, "status": "ok",
                  "decision": "ALIAS", "confidence": 0.99, "reason": "aliases"}
                 for a, b in itertools.combinations(nodes, 2)]
    core.write_jsonl(work / "normalization_candidates.jsonl", decisions)
    core.write_jsonl(work / "normalization_decisions.jsonl", decisions)
    return source, work, graph, chunks, features, decisions


def test_failed_audit_stops_rewrite_then_resume_reuses_success_and_ignores_failed_revoke(tmp_path):
    source, work, graph, chunks, features, decisions = _cluster_fixture(tmp_path)
    calls = []
    succeed = False

    async def audit(cluster, features, edges, chunks, **kwargs):
        _, key = core._cluster_audit_prompt(cluster, features, edges, chunks, kwargs["model"])
        calls.append(key)
        return {"audit_type": "cluster", "audit_key": key, "status": "ok" if succeed else "api_error",
                "members": sorted(cluster), "valid": succeed, "reason": "valid evidence" if succeed else "truncated",
                "api_attempts": 1}

    kwargs = dict(llm_model="deepseek-v4.1-flash", llm_base_url="https://example.test", llm_keys=["fake"],
                  max_async=1, resume=True)
    with patch.object(core, "load_graph", return_value=graph), patch.object(core, "load_chunks", return_value=chunks), \
         patch.object(core, "_call_cluster_audit", audit):
        with pytest.raises(RuntimeError, match="incomplete"):
            asyncio.run(core.build_canonical_map(source, work, **kwargs))
        assert not (work / "canonical_entity_map.json").exists()
        assert not any(r.get("audit_type") == "cluster_revoke" for r in core.read_jsonl(work / "normalization_audit.jsonl"))
        old = core.read_jsonl(work / "normalization_audit.jsonl")[0]
        revoked_id = decisions[0]["pair_id"]
        core.append_jsonl(work / "normalization_audit.jsonl", {"audit_type": "cluster_revoke",
                          "audit_key": "revoke:" + revoked_id, "revoked_pair_id": revoked_id,
                          "members": old["members"], "reason": old["reason"]})
        prefix = (work / "normalization_audit.jsonl").read_bytes()
        decision_bytes = (work / "normalization_decisions.jsonl").read_bytes()
        succeed = True
        result = asyncio.run(core.build_canonical_map(source, work, **kwargs))
        assert len(result["clusters"]) == 1
        assert result["metadata"]["ignored_failed_audit_revocations"] == [revoked_id]
        assert result["metadata"]["revoked_pair_ids"] == []
        assert not core._unresolved_cluster_audits(work)
        assert (work / "normalization_audit.jsonl").read_bytes().startswith(prefix)
        assert (work / "normalization_decisions.jsonl").read_bytes() == decision_bytes
        count = len(calls)
        asyncio.run(core.build_canonical_map(source, work, **kwargs))
        assert len(calls) == count


def test_rewrite_and_validation_reject_unresolved_cluster_audits(tmp_path):
    source, work, graph, chunks, features, decisions = _cluster_fixture(tmp_path)
    core.append_jsonl(work / "normalization_audit.jsonl", {"audit_type": "cluster", "audit_key": "cluster:failed",
                                                        "status": "api_error", "valid": False})
    with pytest.raises(RuntimeError, match="Unresolved cluster"):
        core.rewrite_graph(source, work, {"clusters": [{"canonical_id": "id"}]})

    class StopAfterGate(Exception):
        pass

    with patch.object(core, "_load_json_dict", side_effect=StopAfterGate), \
         patch.object(core, "_unresolved_cluster_audits", wraps=core._unresolved_cluster_audits) as gate:
        with pytest.raises(StopAfterGate):
            core.validate_cache(source, work, expected_docs=1, expected_chunks=1)
        gate.assert_called_once_with(work)


def test_legacy_revocation_requires_successful_negative_evidence():
    good = {"audit_type": "cluster", "audit_key": "cluster:good", "status": "ok", "valid": False,
            "members": ["a", "b"], "reason": "distinct objects"}
    bad = {**good, "audit_key": "cluster:bad", "status": "api_error", "reason": "transport failure"}
    revokes = [{"audit_type": "cluster_revoke", "revoked_pair_id": pair, "members": ["a", "b"],
                "reason": reason} for pair, reason in (("pair:good", "distinct objects"), ("pair:bad", "transport failure"))]
    assert core._effective_cluster_revocations([good, bad, *revokes]) == ({"pair:good"}, {"pair:bad"})


def test_rewrite_retry_invalidates_old_vectors_and_validation_before_resuming(tmp_path):
    core.write_json(tmp_path / "normalization_state.json", {"stages": {
        "judge": {"status": "completed"}, "rewrite": {"status": "incomplete"},
        "embed": {"status": "completed"}, "validate": {"status": "completed"}}})
    args = cli._parser().parse_args(["--source-cache", "source", "--target-cache", "target", "--resume"])

    async def failed_recovery(*args, **kwargs):
        raise RuntimeError("cluster audit remains incomplete")

    with patch.object(cli, "_keys", return_value=["fake"]), \
         patch.object(core, "build_canonical_map", failed_recovery):
        with pytest.raises(RuntimeError, match="incomplete"):
            asyncio.run(cli._rewrite_stage(tmp_path / "source", tmp_path, args, [], []))
    state = core._load_json_dict(tmp_path / "normalization_state.json")["stages"]
    assert state["judge"]["status"] == "completed"
    assert state["rewrite"]["status"] == "incomplete"
    assert "embed" not in state and "validate" not in state
