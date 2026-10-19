import hashlib
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from hyperche.normalization_v2.contracts import digest
from hyperche.normalization_v2.ledger import Ledger, LedgerConflict


def batch(doc="doc1", revision="1" * 64, text="BaTiO3 treats PFOA.", local="e1"):
    chunk = doc + "_CHK_001"
    mid = f"{doc}:{revision}:{local}"
    return {"schema_version": "registry-offline-v2.1", "corpus_id": "test", "doc_id": doc,
            "revision_hash": revision, "chunk_id": chunk,
            "chunk_hash": hashlib.sha256(text.encode()).hexdigest(), "raw_text": text,
            "extraction_id": f"extract:{doc}:{revision}", "status": "complete", "finish_reason": "stop",
            "prompt_hash": "p" * 64, "model_profile_hash": "m" * 64, "response_hash": "r" * 64,
            "mentions": [{"mention_id": mid, "doc_id": doc, "revision_hash": revision,
                          "chunk_id": chunk, "local_id": local, "raw_name": "BaTiO3", "kind": "material"}],
            "facts": []}


def entity(eid="material:batio3"):
    return {"canonical_id": eid, "canonical_name": eid, "kind": "material", "granularity": "concept"}


def test_identity_properties_cannot_be_redefined_under_existing_id(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        original = {**entity(), "variant_dimensions": ["phase"], "properties": {"phase": "alpha"}}
        ledger.ensure_entity(original)
        with pytest.raises(LedgerConflict, match="protected identity"):
            ledger.revise_entity(original["canonical_id"], {**original, "properties": {"phase": "beta"}}, reason="attempted redefinition")
        assert ledger.entity(original["canonical_id"])["properties"]["phase"] == "alpha"


def test_duplicate_import_and_immutable_source(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        b = batch()
        assert ledger.import_batch(b)
        counts = ledger.counts()
        assert not ledger.import_batch(b)
        assert ledger.counts() == counts
        changed = batch(text="Another valid source text.")
        with pytest.raises(LedgerConflict):
            ledger.import_batch(changed)
        assert ledger.counts() == counts
        assert ledger.verify_event_chain()


def test_failed_new_revision_preserves_previous_active_source(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        old = batch()
        ledger.import_batch(old)
        ledger.ensure_entity(entity())
        ledger.bind(old["mentions"][0]["mention_id"], "material:batio3", method="resolved_dictionary")
        ledger.activate_revision("doc1", "1" * 64, expected_chunks=1)
        new = batch(revision="2" * 64)
        ledger.import_batch(new)
        with pytest.raises(ValueError, match="every expected chunk"):
            ledger.activate_revision("doc1", "2" * 64, expected_chunks=2)
        assert [m["revision_hash"] for m in ledger.mentions(active_only=True)] == ["1" * 64]
        assert ledger.source_entities("doc1") == {"material:batio3"}
        ledger.activate_revision("doc1", "2" * 64, expected_chunks=1)
        assert [m["revision_hash"] for m in ledger.mentions(active_only=True)] == ["2" * 64]
        assert ledger.counts()["batches"] == 2


def test_rebinding_retires_derived_fact_occurrences_not_original_evidence(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        b = batch()
        ledger.import_batch(b)
        for eid in ("material:batio3", "material:variant"):
            ledger.ensure_entity(entity(eid))
        mid = b["mentions"][0]["mention_id"]
        ledger.bind(mid, "material:batio3", method="resolved_dictionary")
        ledger.activate_revision("doc1", "1" * 64, expected_chunks=1)
        fact = {"fact_id": "fact:old", "roles": {"material": ["material:batio3"]}}
        occurrence = {"occurrence_id": "occ:old", "doc_id": "doc1", "revision_hash": "1" * 64,
                      "chunk_id": b["chunk_id"], "quote": "BaTiO3 treats PFOA."}
        ledger.save_fact(fact, occurrence)
        assert len(ledger.active_facts()) == 1
        ledger.bind(mid, "material:variant", method="reviewed_rebinding", metadata={"reason": "Independent sample identity"})
        assert ledger.active_facts() == []
        assert ledger.counts()["fact_occurrences"] == 1
        assert ledger.counts()["bindings"] == 2
        assert ledger.counts()["mentions"] == 1
        assert ledger.verify_event_chain()
        exported = ledger.export(tmp_path / "export")
        assert "events.jsonl" in exported
        assert "BaTiO3 treats PFOA." in (tmp_path / "export/fact_occurrences.jsonl").read_text()


def test_withdraw_one_source_retains_shared_identity_and_other_evidence(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        ledger.ensure_entity(entity())
        for doc in ("doc1", "doc2"):
            b = batch(doc=doc)
            ledger.import_batch(b)
            ledger.bind(b["mentions"][0]["mention_id"], "material:batio3", method="resolved_dictionary")
            ledger.activate_revision(doc, "1" * 64, expected_chunks=1)
            ledger.save_fact({"fact_id": "fact:shared", "roles": {"material": ["material:batio3"]}},
                             {"occurrence_id": "occ:" + doc, "doc_id": doc, "revision_hash": "1" * 64,
                              "chunk_id": b["chunk_id"]})
        assert ledger.withdraw_source("doc1") == {"material:batio3"}
        assert len(ledger.active_facts()[0]["occurrences"]) == 1
        assert ledger.active_facts()[0]["occurrences"][0]["doc_id"] == "doc2"
        assert ledger.counts()["fact_occurrences"] == 2
        assert ledger.entity("material:batio3")


def test_transaction_rollback_and_foreign_key_guards(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        ledger.ensure_entity(entity())
        before = ledger.counts()
        with pytest.raises(sqlite3.IntegrityError):
            ledger.bind("nonexistent-mention", "material:batio3", method="resolved_dictionary")
        assert ledger.counts() == before
        with pytest.raises(RuntimeError):
            with ledger.transaction():
                ledger.import_batch(batch())
                raise RuntimeError("Injected process failure before commit")
        assert ledger.counts() == before


def test_task_claim_is_exclusive_across_connections(tmp_path):
    path = tmp_path / "ledger.sqlite"
    with Ledger(path, "test") as ledger:
        ledger.put_task("task:a", {"mention": "test"})
    barrier = Barrier(2)
    def worker(owner):
        with Ledger(path, "test") as ledger:
            barrier.wait()
            return ledger.claim_task("task:a", owner)
    with ThreadPoolExecutor(2) as pool:
        results = list(pool.map(worker, ["worker1", "worker2"]))
    assert sum(results) == 1


def test_successful_decision_and_alias_cannot_be_overwritten(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        ledger.ensure_entity(entity())
        ledger.put_task("task:a", {"mention": "BTO"})
        decision = {"decision": "SAME_ID", "canonical_id": "material:batio3"}
        did = ledger.save_decision("task:a", decision)
        assert ledger.save_decision("task:a", decision) == did
        with pytest.raises(LedgerConflict):
            ledger.save_decision("task:a", {"decision": "NEW_ID"})
        ledger.task_status("task:a", "completed")
        with pytest.raises(LedgerConflict):
            ledger.task_status("task:a", "pending")
        alias = {"raw_name": "BTO", "scope": {"doc_id": "doc1"}, "canonical_id": "material:batio3"}
        ledger.add_learned_alias(alias, decision_id=did)
        ledger.add_learned_alias(alias, decision_id=did)
        assert len(ledger.learned_aliases()) == 1


def test_outbox_idempotence_and_publication_gate(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        ledger.begin_generation("generation:one", {"profile": "frozen"})
        tid = ledger.enqueue_projection("entity:a", "vector", "generation:one", "hash1", {"text": "a"})
        assert ledger.enqueue_projection("entity:a", "vector", "generation:one", "hash1", {"text": "a"}) == tid
        with pytest.raises(LedgerConflict):
            ledger.enqueue_projection("entity:a", "vector", "generation:one", "hash2", {"text": "b"})
        with pytest.raises(ValueError, match="unapplied"):
            ledger.publish_generation("generation:one")
        with pytest.raises(LedgerConflict):
            ledger.mark_projection_applied(tid, content_hash="wrong-receipt")
        ledger.mark_projection_applied(tid, content_hash="hash1")
        ledger.put_task("task:unresolved", {})
        with pytest.raises(ValueError, match="technically unfinished"):
            ledger.publish_generation("generation:one")
        ledger.task_status("task:unresolved", "deferred_semantic")
        ledger.publish_generation("generation:one")
        assert ledger.verify_event_chain()


def test_reject_foreign_database_and_identity_mutation(tmp_path):
    path = tmp_path / "auth.sqlite"
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE users (name TEXT)")
    db.commit()
    db.close()
    original = path.read_bytes()
    with pytest.raises(ValueError, match="non-v2"):
        Ledger(path, "test")
    assert path.read_bytes() == original
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        ledger.ensure_entity(entity())
        with pytest.raises(LedgerConflict):
            ledger.ensure_entity({**entity(), "canonical_name": "new display name"})
        ledger.revise_entity("material:batio3", {**entity(), "canonical_name": "new display name"}, reason="Display label correction")
        with pytest.raises(LedgerConflict):
            ledger.revise_entity("material:batio3", {**entity(), "kind": "metric"}, reason="Invalid identity mutation")
        assert ledger.entity("material:batio3")["canonical_name"] == "new display name"


def test_event_chain_detects_tampering(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        ledger.event("test", {"source": "raw"})
        assert ledger.verify_event_chain()
        ledger.db.execute("UPDATE events SET payload=? WHERE seq=1", ('{"source":"changed"}',))
        assert not ledger.verify_event_chain()
