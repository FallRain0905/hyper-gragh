import copy
import hashlib

from hyperche.normalization_v2.candidate_index import CandidateIndex
from hyperche.normalization_v2.contracts import CanonicalEntity, Mention
from hyperche.normalization_v2.ledger import Ledger
from hyperche.normalization_v2.registry import Registry
from hyperche.normalization_v2.resolver import Resolver


def entity(eid="known", name="PFOA", **kw):
    return CanonicalEntity(canonical_id=eid, canonical_name=name, kind="chemical", **kw)


def batch(name="PFOA", *, doc="doc1", attributes=None):
    text = name + " is discussed here."
    return {"corpus_id": "test", "doc_id": doc, "revision_hash": "r1", "chunk_id": doc + "c1",
            "chunk_hash": hashlib.sha256(text.encode()).hexdigest(), "raw_text": text,
            "extraction_id": "extract:" + doc, "status": "complete", "finish_reason": "stop",
            "prompt_hash": "p", "model_profile_hash": "m", "response_hash": "r",
            "mentions": [{"mention_id": "mention:" + doc, "local_id": "e1", "raw_name": name,
                          "kind": "chemical", "doc_id": doc, "revision_hash": "r1", "chunk_id": doc + "c1",
                          "attributes": attributes or {}}]}


def run(tmp_path, b, registry):
    ledger = Ledger(tmp_path / "ledger.sqlite", "test")
    ledger.import_batch(b)
    resolver = Resolver(ledger, registry, profile_hash="explicit-profile", prompt_hash="prompt-v1")
    return ledger, resolver, resolver.run()["records"][0]


def test_known_and_unknown_names_do_not_create_requests(tmp_path):
    registry = Registry([entity()])
    ledger, resolver, result = run(tmp_path, batch(), registry)
    assert result["status"] == "resolved_dictionary"
    assert result["canonical_id"] == "known"
    before = ledger.counts()
    resolver.run()
    assert ledger.counts() == before
    ledger.close()
    ledger, resolver, result = run(tmp_path / "other", batch("novel-chemical"), registry)
    assert result["status"] == "provisional_new"
    assert not ledger.tasks()
    before = ledger.counts()
    resolver.run()
    assert ledger.counts() == before
    ledger.close()


def test_fuzzy_key_only_creates_task_and_cap_has_no_formula_exception(tmp_path):
    registry = Registry([entity("x", "PFOA-7")])
    ledger, resolver, result = run(tmp_path, batch("PFOA7"), registry)
    assert result["status"] == "pending_judgment"
    assert result["canonical_id"] != "x"
    assert len(ledger.tasks()[0]["payload"]["candidates"]) == 1
    ledger.close()
    variants = [entity(str(i), "PFOA" + "-" * i + "7") for i in range(6)]
    # Formula/exact aliases receive the same hard cap as every other candidate.
    candidate = CandidateIndex(variants).find(Mention.model_validate(batch("PFOA---7")["mentions"][0]))
    assert candidate.too_broad and candidate.matched_count == 6
    assert candidate.candidates == ()


def test_unrelated_alias_change_does_not_invalidate_task(tmp_path):
    registry = Registry([entity("x", "PFOA-7")])
    b = batch("PFOA7")
    ledger, resolver, first = run(tmp_path, b, registry)
    newer = Registry([entity("x", "PFOA-7"), entity("unrelated", "PFBS")])
    assert newer.snapshot_hash != registry.snapshot_hash
    second = Resolver(ledger, newer, profile_hash="explicit-profile", prompt_hash="prompt-v1").run()["records"][0]
    assert first["task_id"] == second["task_id"]
    assert len(ledger.tasks()) == 1
    ledger.close()


def test_guard_conflicts_block_both_dictionary_and_candidates(tmp_path):
    registered = entity("membrane:117", "Nafion117", identity_guards=["model"], properties={"model": "117"})
    ledger, resolver, result = run(tmp_path, batch("Nafion117", attributes={"model": "115"}), Registry([registered]))
    assert result["status"] == "provisional_new"
    assert result["canonical_id"] != "membrane:117"
    assert not ledger.tasks()
    ledger.close()


def test_unknown_sample_or_source_identity_never_crosses_document(tmp_path):
    ledger, resolver, first = run(tmp_path, batch("novel"), Registry([entity()]))
    ledger.import_batch(batch("novel", doc="doc2"))
    second = resolver.resolve(ledger.mentions()[-1])
    assert first["canonical_id"] != second["canonical_id"]
    ledger.close()


def test_material_roles_do_not_split_registered_identity(tmp_path):
    b = batch()
    b["mentions"][0]["roles"] = ["target", "additive"]
    ledger, resolver, first = run(tmp_path, b, Registry([entity()]))
    assert first["canonical_id"] == "known"
    ledger.close()
