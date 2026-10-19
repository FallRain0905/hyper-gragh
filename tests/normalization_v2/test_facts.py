import copy
import hashlib

import pytest

from hyperche.normalization_v2.facts import FactError, build_facts, persist_batch_facts
from hyperche.normalization_v2.ledger import Ledger


def source():
    text = "BaTiO3 treats PFOA with 90% defluorination."
    doc, rev, chunk = "doc1", "1" * 64, "doc1_chunk1"
    mentions = []
    for lid, name, kind in (("e1", "BaTiO3", "material"), ("e2", "PFOA", "chemical"),
                            ("e3", "defluorination", "metric")):
        mentions.append({"mention_id": "mention:" + lid, "local_id": lid, "raw_name": name,
                         "kind": kind, "doc_id": doc, "revision_hash": rev, "chunk_id": chunk})
    return {"schema_version": "registry-offline-v2.1", "corpus_id": "test", "doc_id": doc,
            "revision_hash": rev, "chunk_id": chunk, "chunk_hash": hashlib.sha256(text.encode()).hexdigest(),
            "raw_text": text, "extraction_id": "extraction:1", "status": "complete", "finish_reason": "stop",
            "prompt_hash": "p", "model_profile_hash": "m", "response_hash": "r", "mentions": mentions,
            "facts": [{"local_id": "f1", "relation_type": "OPERATION_PERFORMANCE",
                       "roles": {"material": ["e1"], "target": ["e2"], "metric": ["e3"]},
                       "observations": [{"metric": "e3", "value": "90", "unit": "%"}],
                       "context_id": "experiment1", "assertion": "measured"}]}


def bindings():
    return {"mention:e1": {"entity_id": "material:batio3"}, "mention:e2": {"entity_id": "pfas:pfoa"},
            "mention:e3": {"entity_id": "metric:defluorination"}}


def fid(batch):
    return build_facts(batch, bindings())["facts"][0]["fact"]["fact_id"]


def test_fact_identity_changes_for_roles_polarity_scope_and_observations():
    b = source()
    original = fid(b)
    for mutation in ("roles", "polarity", "context_id", "assertion", "conditions", "value"):
        edited = copy.deepcopy(b)
        raw = edited["facts"][0]
        if mutation == "roles":
            raw["roles"]["material"], raw["roles"]["target"] = raw["roles"]["target"], raw["roles"]["material"]
        elif mutation == "polarity": raw["polarity"] = "negative"
        elif mutation == "context_id": raw["context_id"] = "experiment2"
        elif mutation == "assertion": raw["assertion"] = "hypothesized"
        elif mutation == "conditions": raw["conditions"] = {"temperature": "80 C"}
        elif mutation == "value": raw["observations"][0]["value"] = "80"
        assert fid(edited) != original
    assert fid(b) == original


def test_structural_buckets_do_not_collapse_fact_roles():
    b = source()
    b["facts"][0]["observations"] = []
    swapped = copy.deepcopy(b)
    swapped["facts"][0]["roles"]["material"], swapped["facts"][0]["roles"]["target"] = ["e2"], ["e1"]
    a, c = (build_facts(x, bindings())["facts"][0]["fact"] for x in (b, swapped))
    assert a["structural_bucket"] == c["structural_bucket"]
    assert a["fact_id"] != c["fact_id"]


def test_unknown_metric_binding_retains_original_problem():
    b = source()
    b["facts"][0]["observations"][0]["metric"] = "not_a_local_mention"
    result = build_facts(b, bindings())
    assert len(result["facts"]) == 1
    assert result["issues"][0]["original"]["metric"] == "not_a_local_mention"
    assert result["facts"][0]["fact"]["unresolved_observations"]
    broken = bindings()
    broken.pop("mention:e1")
    with pytest.raises(FactError, match="exact source batch"):
        build_facts(source(), broken)


def test_failed_partial_extraction_cannot_become_a_resolvable_mention(tmp_path):
    b = source()
    b["status"], b["finish_reason"] = "technical_failed", "length"
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        ledger.import_batch(b)
        assert ledger.mentions() == []
        assert ledger.counts()["batches"] == 1
        with pytest.raises(ValueError):
            ledger.activate_revision("doc1", "1" * 64, expected_chunks=1)


def test_fact_projection_replay_is_idempotent_and_preserves_history(tmp_path):
    b = source()
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        ledger.import_batch(b)
        for mid, bound in bindings().items():
            mention = next(m for m in b["mentions"] if m["mention_id"] == mid)
            eid = bound["entity_id"]
            ledger.ensure_entity({"canonical_id": eid, "canonical_name": eid, "kind": mention["kind"], "granularity": "concept"})
            ledger.bind(mid, eid, method="resolved_dictionary")
        ledger.activate_revision("doc1", "1" * 64, expected_chunks=1)
        persist_batch_facts(ledger, b)
        before = ledger.counts()
        persist_batch_facts(ledger, b)
        assert ledger.counts() == before
        assert len(ledger.active_facts()) == 1
        assert ledger.active_facts()[0]["roles"]["target"] == ["pfas:pfoa"]
        assert ledger.counts()["observations"] == 1
        assert ledger.verify_event_chain()
