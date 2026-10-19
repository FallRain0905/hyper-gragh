import asyncio
import copy
import json

import numpy as np
import pytest

from hyperche.normalization_v2.facts import persist_batch_facts
from hyperche.normalization_v2.ledger import Ledger
from hyperche.normalization_v2.projections import Projector, RetrievalAdapter, VectorCache, generation_directory
from test_facts import source, bindings


def ledger_with_source(tmp_path):
    ledger = Ledger(tmp_path / "ledger.sqlite", "test")
    b = source()
    ledger.import_batch(b)
    for mid, binding in bindings().items():
        eid = binding["entity_id"]
        ledger.ensure_entity({"canonical_id": eid, "canonical_name": eid,
                              "kind": b["mentions"][list(bindings()).index(mid)]["kind"],
                              "granularity": "concept", "properties": {}})
        ledger.bind(mid, eid, method="resolved_dictionary")
    ledger.activate_revision(b["doc_id"], b["revision_hash"], expected_chunks=1)
    persist_batch_facts(ledger, b)
    return ledger, b


class OfflineEmbedding:
    """Deterministic vectors only for fault tests; not a production default."""
    def __init__(self): self.calls = 0
    async def __call__(self, texts, *, model, dimensions):
        self.calls += 1
        return np.tile(np.arange(1, dimensions + 1, dtype=np.float32), (len(texts), 1))


def publish(projector, embedder):
    generation = projector.prepare(registry_hash="test-registry", task_ids=[])
    asyncio.run(projector.embed(generation, embedder))
    return generation, projector.publish(generation)


def test_published_release_contains_roles_exact_source_and_idempotent_vectors(tmp_path):
    ledger, b = ledger_with_source(tmp_path)
    root = tmp_path / "new-target"
    projector = Projector(ledger, root, model="test-only", dimension=4)
    embedder = OfflineEmbedding()
    generation, manifest = publish(projector, embedder)
    assert manifest["counts"] == {"records": 4, "chunks": 1, "buckets": 1}
    adapter = RetrievalAdapter(root)
    results = adapter.search("PFOA", top_k=5)
    assert any(r["view"] == "fact" and r["data"]["roles"]["target"] == ["pfas:pfoa"] for r in results)
    assert all(r["sources"][0]["content"] == b["raw_text"] for r in results)
    assert "[" not in str(generation_directory(root, generation).name[:11])
    count = ledger.counts()
    repeat, _ = publish(projector, embedder)
    assert repeat == generation and embedder.calls == 1
    assert ledger.counts() == count
    ledger.close()


def test_partial_vectors_and_corrupt_checkpoints_cannot_publish(tmp_path):
    ledger, b = ledger_with_source(tmp_path)
    projector = Projector(ledger, tmp_path / "new-target", model="test-only", dimension=4)
    generation = projector.prepare(registry_hash="r", task_ids=[])
    with pytest.raises(ValueError, match="incomplete"): projector.publish(generation)
    async def bad(texts, **kw): return np.zeros((len(texts), 4))
    with pytest.raises(ValueError, match="nonzero"):
        asyncio.run(projector.embed(generation, bad))
    assert not list(projector.cache.root.glob("*.npz"))
    assert len(ledger.projection_tasks(generation)) == 4
    ledger.close()


def test_new_provenance_without_new_index_content_reuses_vectors(tmp_path):
    ledger, b = ledger_with_source(tmp_path)
    # Only the identity projections are relevant in this test.
    ledger.db.execute("UPDATE fact_occurrences SET active=0")
    projector = Projector(ledger, tmp_path / "new-target", model="test-only", dimension=4)
    embedder = OfflineEmbedding()
    first, _ = publish(projector, embedder)
    new = copy.deepcopy(b)
    new.update(doc_id="doc2", chunk_id="doc2_chunk1", extraction_id="extract:doc2", facts=[])
    for mention in new["mentions"]:
        mention.update(doc_id="doc2", chunk_id="doc2_chunk1", mention_id=mention["mention_id"] + ":doc2")
    ledger.import_batch(new)
    for old_mid, row in bindings().items(): ledger.bind(old_mid + ":doc2", row["entity_id"], method="resolved_dictionary")
    ledger.activate_revision("doc2", new["revision_hash"], expected_chunks=1)
    second, manifest = publish(projector, embedder)
    assert first != second and embedder.calls == 1
    assert manifest["counts"]["chunks"] == 2
    assert len(RetrievalAdapter(projector.root).search("PFOA")[0]["sources"]) == 2
    ledger.close()


def test_failed_pointer_switch_keeps_old_release_readable(tmp_path, monkeypatch):
    from hyperche.normalization_v2 import projections
    ledger, b = ledger_with_source(tmp_path)
    root = tmp_path / "new-target"
    projector = Projector(ledger, root, model="test-only", dimension=4)
    embedder = OfflineEmbedding()
    first, _ = publish(projector, embedder)
    ledger.withdraw_source(b["doc_id"])
    second = projector.prepare(registry_hash="test-registry", task_ids=[])
    real = projections.atomic_json
    def fail(path, value):
        if path.name == "current.json": raise OSError("injected file switch failure")
        return real(path, value)
    monkeypatch.setattr(projections, "atomic_json", fail)
    with pytest.raises(OSError): projector.publish(second)
    assert RetrievalAdapter(root).manifest["generation"] == first
    monkeypatch.setattr(projections, "atomic_json", real)
    projector.publish(second)
    assert RetrievalAdapter(root).manifest["generation"] == second
    assert RetrievalAdapter(root).search("PFOA") == []
    ledger.close()


def test_released_file_tampering_and_query_dimension_rejected(tmp_path):
    ledger, _ = ledger_with_source(tmp_path)
    root = tmp_path / "new-target"
    projector = Projector(ledger, root, model="test-only", dimension=4)
    generation, _ = publish(projector, OfflineEmbedding())
    adapter = RetrievalAdapter(root)
    with pytest.raises(ValueError): adapter.search("PFOA", query_vector=[1, 2])
    (generation_directory(root, generation) / "records.json").write_text("[]")
    with pytest.raises(ValueError, match="hash mismatch"): RetrievalAdapter(root)
    ledger.close()
