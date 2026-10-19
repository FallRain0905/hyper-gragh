import asyncio
import json
from types import SimpleNamespace

import numpy as np
import pytest

from hyperche.normalization import final_cache as final
from hyperche.normalization import posthoc_cache as core
from hyperche.normalization.alias_registry import AliasRegistry
from hyperche.normalization.entity_normalizer import EntityNormalizer
from hyperrag.prompt import get_entity_extraction_prompt
from hyperrag.utils import compute_args_hash


def numeric(name, value=None, unit=None, typ="METRIC", **extra):
    entity = {"name": name, "type": typ, "value": value, "unit": unit, **extra}
    return final.local_instance(entity, EntityNormalizer(AliasRegistry()), domain="pfas_piezocatalysis",
                                canonical={"canonical_id": "accepted:" + name, "canonical_name": name})[0]


def test_pfas_values_preserve_quantity_and_target_identity():
    rows = [numeric(name, 90, "%") for name in ("PFOA removal", "PFOS removal", "PFOA defluorination")]
    assert len({r["node_id"] for r in rows}) == 3
    assert [r["canonical_id"] for r in rows] == ["accepted:" + n for n in ("PFOA removal", "PFOS removal", "PFOA defluorination")]
    assert numeric("PFOA removal", None, "%", description="90% at 60 min") is None
    assert numeric("PFOA removal", 90, "%", description="70% at 30 min")["value"] == 90


def test_pfas_units_scientific_values_and_formula_digits():
    assert numeric("Na2SO4 concentration", 5, "mM", "CONDITION")["value"] == 5
    assert numeric("rate constant", 1.2e-4, "min^-1")["value"] == 1.2e-4
    assert numeric("degradation rate", 140, "L/mol·s")["value"] == 140
    assert numeric("initial PFOA concentration", 10, "μg/L", "CONDITION")["unit"] == "μg/L"
    assert numeric("initial PFOA concentration", 10, "mg/L", "CONDITION")["node_id"] != numeric("initial PFOA concentration", 10, "μg/L", "CONDITION")["node_id"]
    assert numeric("PFAS_TARGET", 90, "%", "PFAS_TARGET") is None


@pytest.mark.parametrize("name,value,unit", [("PFOA removal", 120, "%"), ("pH", 15, None),
    ("photon flux", 5, None), ("pH", 7, "mV/pH"), ("pH 7", 8, None),
    ("PFOA removal at 60 min, 90%", 90, "%"), ("rate constant", float("nan"), "min^-1"),
    ("rate constant", True, "min^-1")])
def test_ambiguous_or_invalid_pfas_values_are_preserved(name, value, unit):
    assert numeric(name, value, unit) is None


def test_pfas_ranges_remain_ranges_and_partial_or_mixed_ranges_preserved():
    row = numeric("reaction time", None, "min", "CONDITION", value_min=10, value_max=30)
    assert row["value"] is None and row["min_value"] == 10 and row["max_value"] == 30
    assert numeric("reaction time", None, "min", "CONDITION", value_min=10) is None
    assert numeric("reaction time", 20, "min", "CONDITION", value_min=10, value_max=30) is None


def test_two_step_arrays_require_complete_unambiguous_json():
    row = {"name": "PFOA", "type": "PFAS_TARGET"}
    assert final.cached_payload("[]\n```json\n" + json.dumps([row]) + "\n```", two_step=True) == {"entities": [row]}
    assert final.cached_payload("```json\n[]\n```", two_step=True) == {"entities": []}
    for text in ('[{"name":"PFOA","type":"PFAS_TARGET"}', '[{},', '[{}]',
                 json.dumps([row]) + json.dumps([row]), '{"entities": []}'):
        with pytest.raises(ValueError):
            final.cached_payload(text, two_step=True)


def test_exact_entity_prompt_maps_each_pfas_chunk_and_missing_cache_fails(tmp_path):
    model, domain = "deepseek-v4.1-flash", "pfas_piezocatalysis"
    config = {"llm": {"model": model}, "domain": domain}
    chunks = {"PFAS_001_CHK_001": {"content": "PFOA removal"}, "PFAS_002_CHK_001": {"content": "PFOS removal"}}
    responses = {}
    for chunk in chunks.values():
        prompt = get_entity_extraction_prompt(domain=domain, CHUNK_TEXT=chunk["content"])
        key = compute_args_hash(model, [{"role": "user", "content": prompt}])
        responses[key] = {"return": '[{"name":"PFAS","type":"PFAS_TARGET"}]', "model": model}
    for filename, value in (("run_config.json", config), ("kv_store_text_chunks.json", chunks), ("kv_store_llm_response_cache.json", responses)):
        core.write_json(tmp_path / filename, value)
    result = final.build_chunk_map(tmp_path)
    assert set(result["mapped"]) == set(chunks)
    assert {r[0]["cache_key"] for r in result["mapped"].values()} == set(responses)
    responses.pop(next(iter(responses)))
    core.write_json(tmp_path / "kv_store_llm_response_cache.json", responses)
    with pytest.raises(ValueError, match="no matching cached entity response"):
        final.build_chunk_map(tmp_path)


def test_pfas_graph_values_bind_to_existing_endpoints_in_the_same_chunk():
    chunks = ["PFAS_001_CHK_001", "PFAS_002_CHK_001"]
    vertices = {n: {"source_chunk_ids": chunks} for n in ("catalyst", "PFOA removal")}
    source = {"v_data": vertices, "e_data": {("catalyst", "PFOA removal"): {"evidence_instances": [
        {"vertices": ["catalyst", "PFOA removal"], "source_chunk_id": c, "source_span": f"removal {v}%", "repair_applied": False}
        for c, v in zip(chunks, (80, 90))]}}}
    mapping = {n: {"canonical_id": "canonical:" + n, "canonical_name": n} for n in vertices}
    normalized = {"v_data": {d["canonical_id"]: {"canonical_name": n, "aliases": [n], "source_chunk_ids": chunks} for n, d in mapping.items()}}
    cmap = {"entities": mapping, "clusters": [{"canonical_id": d["canonical_id"], "members": [n]} for n, d in mapping.items()]}
    extracted = {c: [{"name": "PFOA removal", "type": "METRIC", "value": v, "unit": "%"},
                     {"name": "PFOS removal", "type": "METRIC", "value": 50, "unit": "%"}] for c, v in zip(chunks, (80, 90))}
    nodes, edges, occurrences, details = final.rewrite_final_graph(source, normalized, cmap, extracted, domain="pfas_piezocatalysis")
    assert len(edges) == len(occurrences) == 2
    for key, edge in edges.items():
        numeric_node = next(nodes[n] for n in key if nodes[n].get("instance_id"))
        assert len(key) == 2 and numeric_node["canonical_id"] == mapping["PFOA removal"]["canonical_id"]
        assert numeric_node["value"] == (80 if edge["source_chunk_ids"] == [chunks[0]] else 90)
        assert not edge["repair_applied"]
    assert details["summary"]["removed_replaced_numeric_clusters"] == 1


def test_embedding_key_lanes_checkpoint_resume_and_bad_index_rejection(tmp_path, monkeypatch):
    records = {"entities": {f"e-{i}": {"content": f"entity-{i}"} for i in range(22)}, "relationships": {}}
    core.write_json(tmp_path / "embedding_records.json", records)
    activity = {"global": 0, "peak": 0, "calls": 0, "per_key": {}, "bad": False}

    class FakeClient:
        def __init__(self, api_key, **kwargs):
            self.key = api_key
            self.embeddings = self

        async def create(self, input, **kwargs):
            activity["calls"] += 1
            activity["global"] += 1
            activity["peak"] = max(activity["peak"], activity["global"])
            activity["per_key"][self.key] = activity["per_key"].get(self.key, 0) + 1
            assert activity["per_key"][self.key] == 1
            await asyncio.sleep(.001)
            activity["global"] -= 1
            activity["per_key"][self.key] -= 1
            return SimpleNamespace(data=[SimpleNamespace(index=(1 if activity["bad"] else i), embedding=np.ones(final.DIMENSION).tolist()) for i in range(len(input))])

        async def close(self):
            pass

    monkeypatch.setattr(final, "AsyncOpenAI", FakeClient)
    endpoints = [("test", f"fake-{i}") for i in range(10)]
    result = asyncio.run(final.embed_final(tmp_path, endpoints, concurrency=10, batch_size=1))
    assert result["entities"] == 22 and activity["peak"] == 10
    assert result["api_statistics"]["network_peak"] == 10
    assert all(k["peak"] == 1 and k["active"] == 0 for k in result["api_statistics"]["key_usage"].values())
    before = activity["calls"]
    asyncio.run(final.embed_final(tmp_path, endpoints, concurrency=10, batch_size=1))
    assert activity["calls"] == before
    bad = tmp_path / "bad"
    bad.mkdir()
    core.write_json(bad / "embedding_records.json", {"entities": {"e": {"content": "bad"}}, "relationships": {}})
    activity["bad"] = True
    with pytest.raises(RuntimeError, match="successes checkpointed"):
        asyncio.run(final.embed_final(bad, endpoints, concurrency=10, batch_size=1))
    assert not (bad / "vdb_entities.json").exists()
