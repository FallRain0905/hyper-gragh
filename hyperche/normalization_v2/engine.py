"""Explicit v2 job orchestration. Legacy builders and defaults are untouched."""
from __future__ import annotations

from collections import defaultdict
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import uuid

from hyperche.request_leases import process_alive
from .contracts import RawBatch, STRATEGY, digest, utc_now, validate_source_target
from .decisions import DecisionWorker, PROMPT_HASH
from .facts import persist_batch_facts
from .ledger import Ledger
from .projections import Projector, RetrievalAdapter, atomic_json
from .quantities import UnitRegistry
from .registry import Registry
from .resolver import Resolver


class IncompleteJob(RuntimeError):
    pass


@contextmanager
def job_lease(ledger):
    token = uuid.uuid4().hex
    with ledger.transaction():
        row = ledger.db.execute("SELECT value FROM registry_meta WHERE key='job_owner'").fetchone()
        if row:
            prior = json.loads(row[0])
            if process_alive(prior["pid"]):
                raise IncompleteJob("Another live job owns this target")
        ledger.db.execute("INSERT OR REPLACE INTO registry_meta VALUES ('job_owner',?)",
                          (json.dumps({"pid": os.getpid(), "token": token}),))
    try:
        yield
    finally:
        with ledger.transaction():
            row = ledger.db.execute("SELECT value FROM registry_meta WHERE key='job_owner'").fetchone()
            if row and json.loads(row[0]).get("token") == token:
                ledger.db.execute("DELETE FROM registry_meta WHERE key='job_owner'")


class Engine:
    def __init__(self, *, source, target, corpus_id, registry_paths,
                 normalization_profile_hash, embedding_model, embedding_dimension,
                 expected_docs=None, expected_chunks=None, accepted_targets=()):
        source, target = validate_source_target(source, target, accepted_targets=accepted_targets)
        self.source, self.target, self.corpus_id = Path(source), Path(target), corpus_id
        if not self.source.is_file():
            raise ValueError("Source must be an explicit RawBatch JSONL file")
        self.registry = Registry.from_paths(registry_paths)
        self.units = UnitRegistry.from_compiled(self.registry)
        self.profile_hash = normalization_profile_hash
        if not self.profile_hash:
            raise ValueError("Normalization profile fingerprint must be explicit, even offline")
        self.expected_docs, self.expected_chunks = expected_docs, expected_chunks
        self.target.mkdir(parents=True, exist_ok=True)
        marker = self.target / ".registry_offline_v2.json"
        if marker.exists():
            ownership = json.loads(marker.read_text(encoding="utf-8"))
            if ownership.get("strategy") != STRATEGY or ownership.get("corpus_id") != corpus_id:
                raise ValueError("Target belongs to another strategy or corpus")
        elif any(self.target.iterdir()):
            raise ValueError("Refusing to write into an existing non-v2 target")
        else:
            atomic_json(marker, {"strategy": STRATEGY, "corpus_id": corpus_id})
        self.ledger = Ledger(self.target / "ledger.sqlite", corpus_id)
        self.projector = Projector(self.ledger, self.target, model=embedding_model, dimension=embedding_dimension)
        self.state_path = self.target / "progress.json"

    def close(self):
        self.ledger.close()

    def _read_source(self):
        before = hashlib.sha256(self.source.read_bytes()).hexdigest()
        batches = [RawBatch.model_validate(json.loads(line)) for line in self.source.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        if not batches:
            raise ValueError("Empty source file")
        if any(batch.corpus_id != self.corpus_id for batch in batches):
            raise ValueError("Source corpus does not match this target")
        if len({(b.doc_id, b.revision_hash, b.chunk_id) for b in batches}) != len(batches):
            raise ValueError("Source must contain one combined extraction batch per chunk")
        if len({b.chunk_id for b in batches}) != len(batches):
            raise ValueError("Chunk IDs must be corpus-unique")
        revisions = defaultdict(set)
        for batch in batches: revisions[batch.doc_id].add(batch.revision_hash)
        if any(len(values) != 1 for values in revisions.values()):
            raise ValueError("A run must select exactly one revision per document")
        if self.expected_docs is not None and len(revisions) != self.expected_docs:
            raise ValueError("Document count differs from frozen expectation")
        if self.expected_chunks is not None and len(batches) != self.expected_chunks:
            raise ValueError("Chunk count differs from frozen expectation")
        if hashlib.sha256(self.source.read_bytes()).hexdigest() != before:
            raise ValueError("Source changed during import")
        return batches, before

    def _current_task_ids(self):
        mentions = {m["mention_id"] for m in self.ledger.mentions()}
        return sorted({row["metadata"]["task_id"] for mid, row in self.ledger.bindings().items()
                       if mid in mentions and row["metadata"].get("task_id")})

    def _require_resolved(self, task_ids):
        tasks = {task["id"]: task for task in self.ledger.tasks()}
        failed = [identifier for identifier in task_ids if tasks[identifier]["status"] not in {"completed", "deferred_semantic"}]
        if failed:
            raise IncompleteJob(f"{len(failed)} identity tasks are technically unfinished")
        if self.ledger.mentions(unbound_only=True):
            raise IncompleteJob("Source mentions have not been resolved")

    def _activate_and_facts(self, batches):
        groups = defaultdict(list)
        for batch in batches: groups[(batch.doc_id, batch.revision_hash)].append(batch)
        with self.ledger.transaction():
            for (doc, revision), rows in groups.items():
                self.ledger.activate_revision(doc, revision, expected_chunks=len(rows))
            for batch in batches:
                persist_batch_facts(self.ledger, batch, units=self.units)

    async def run(self, stage="all", *, transport=None, embedder=None,
                  request_budget=0, embedding_request_budget=0):
        allowed = {"all", "import", "resolve", "judge", "project", "embed", "validate", "publish"}
        if stage not in allowed: raise ValueError("Unsupported job stage")
        with job_lease(self.ledger):
            batches, source_hash = self._read_source()
            state = {"strategy": STRATEGY, "corpus_id": self.corpus_id, "stage": stage,
                     "status": "running", "started_at": utc_now(), "source_hash": source_hash,
                     "registry_hash": self.registry.snapshot_hash, "profile_hash": self.profile_hash,
                     "normalization_prompt_hash": PROMPT_HASH, "efu_repair": False,
                     "identity_candidate_embedding_calls": 0}
            atomic_json(self.state_path, state)
            try:
                if stage in {"all", "import"}:
                    state["imported_batches"] = sum(self.ledger.import_batch(batch) for batch in batches)
                    if any(b.status == "technical_failed" for b in batches):
                        raise IncompleteJob("Source contains technical extraction failures")
                resolver = Resolver(self.ledger, self.registry, profile_hash=self.profile_hash, prompt_hash=PROMPT_HASH)
                if stage in {"all", "resolve"}:
                    state["resolution"] = resolver.run()
                if stage in {"all", "judge"}:
                    if transport:
                        worker = DecisionWorker(self.ledger, self.registry, transport, max_requests=request_budget)
                        selected = set(self._current_task_ids())
                        state["judgments"] = [await worker.process(row) for row in self.ledger.tasks()
                                              if row["id"] in selected and row["status"] not in {"completed", "deferred_semantic"}]
                        state["judgment_budget_issuances"] = worker.requests
                        state["actual_judgment_requests"] = getattr(transport, "actual_requests", None)
                    self._require_resolved(self._current_task_ids())
                if stage in {"all", "project", "embed", "validate", "publish"}:
                    task_ids = self._current_task_ids()
                    self._require_resolved(task_ids)
                    if any(b.status == "technical_failed" for b in batches):
                        raise IncompleteJob("Failed source batches cannot be activated")
                    self._activate_and_facts(batches)
                    generation = self.projector.prepare(registry_hash=self.registry.snapshot_hash, task_ids=task_ids)
                    state["generation"] = generation
                    if stage in {"all", "embed"}:
                        pending = self.ledger.projection_tasks(generation)
                        needed_calls = (len(pending) + 15) // 16
                        if needed_calls and (not embedder or embedding_request_budget < needed_calls):
                            raise IncompleteJob(f"{len(pending)} vectors need an explicit embedding profile and sufficient request budget")
                        if pending:
                            state["embeddings"] = await self.projector.embed(generation, embedder)
                    if stage in {"all", "validate", "publish"}:
                        if self.ledger.projection_tasks(generation):
                            raise IncompleteJob("Vector projections are incomplete")
                        if not self.ledger.verify_event_chain():
                            raise ValueError("Provenance event chain is invalid")
                        state["validation"] = {"passed": True, "batches": len(batches), "task_ids": task_ids}
                    if stage in {"all", "publish"}:
                        state["release"] = self.projector.publish(generation)
                        RetrievalAdapter(self.target)
                state["status"] = "completed" if stage != "all" else "completed_and_published"
            except BaseException as exc:
                state["status"] = "partial" if isinstance(exc, IncompleteJob) else "cancelled" if isinstance(exc, __import__("asyncio").CancelledError) else "failed"
                state["error_type"] = type(exc).__name__
                state["finished_at"] = utc_now()
                atomic_json(self.state_path, state)
                raise
            state["finished_at"] = utc_now()
            state["source_unchanged"] = hashlib.sha256(self.source.read_bytes()).hexdigest() == source_hash
            if not state["source_unchanged"]: raise ValueError("Source changed during job")
            atomic_json(self.state_path, state)
            return state
