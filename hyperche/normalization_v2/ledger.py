"""Transactional, append-only provenance for the offline registry strategy.

Original source payloads and decisions are immutable. Mutable rows select the
current binding/revision; their prior values remain in the event chain. Files
and indexes are derived through the durable outbox, never inside a fictitious
cross-system transaction.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3
import threading
import time
from typing import Any, Iterable, Iterator, Mapping

from .contracts import SCHEMA_VERSION, canonical_json, digest, stable_id, utc_now


class LedgerConflict(ValueError):
    """An immutable identity was presented with different source data."""


class Ledger:
    def __init__(self, path: str | Path, corpus_id: str):
        if not corpus_id or not str(corpus_id).strip():
            raise ValueError("corpus_id is required")
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.corpus_id = corpus_id
        self._lock = threading.RLock()
        self.db = sqlite3.connect(self.path, timeout=30, isolation_level=None, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        tables = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if tables and "registry_meta" not in tables:
            self.db.close()
            raise ValueError("Refusing to initialize a non-v2 database")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self._initialize()

    def _initialize(self):
        with self.transaction():
            statements = [
                "CREATE TABLE IF NOT EXISTS registry_meta (key TEXT PRIMARY KEY,value TEXT NOT NULL)",
                "CREATE TABLE IF NOT EXISTS sources (doc_id TEXT,revision TEXT,status TEXT NOT NULL CHECK(status IN ('staged','active','superseded','withdrawn')),payload TEXT NOT NULL,created TEXT NOT NULL,PRIMARY KEY(doc_id,revision))",
                "CREATE UNIQUE INDEX IF NOT EXISTS one_active_revision ON sources(doc_id) WHERE status='active'",
                "CREATE TABLE IF NOT EXISTS batches (id TEXT PRIMARY KEY,doc_id TEXT NOT NULL,revision TEXT NOT NULL,chunk_id TEXT NOT NULL,status TEXT NOT NULL,payload TEXT NOT NULL,hash TEXT NOT NULL,FOREIGN KEY(doc_id,revision) REFERENCES sources(doc_id,revision))",
                "CREATE INDEX IF NOT EXISTS source_batches ON batches(doc_id,revision,chunk_id)",
                "CREATE TABLE IF NOT EXISTS mentions (id TEXT PRIMARY KEY,batch_id TEXT NOT NULL,doc_id TEXT NOT NULL,revision TEXT NOT NULL,local_id TEXT NOT NULL,payload TEXT NOT NULL,hash TEXT NOT NULL,UNIQUE(batch_id,local_id),FOREIGN KEY(batch_id) REFERENCES batches(id),FOREIGN KEY(doc_id,revision) REFERENCES sources(doc_id,revision))",
                "CREATE TABLE IF NOT EXISTS entities (id TEXT PRIMARY KEY,creation_key TEXT UNIQUE,status TEXT NOT NULL,payload TEXT NOT NULL,hash TEXT NOT NULL)",
                "CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY,status TEXT NOT NULL,payload TEXT NOT NULL,hash TEXT NOT NULL,owner TEXT,lease_until REAL,updated TEXT NOT NULL)",
                "CREATE TABLE IF NOT EXISTS attempts (id INTEGER PRIMARY KEY,task_id TEXT NOT NULL,payload TEXT NOT NULL,created TEXT NOT NULL,FOREIGN KEY(task_id) REFERENCES tasks(id))",
                "CREATE TABLE IF NOT EXISTS decisions (id TEXT PRIMARY KEY,task_id TEXT UNIQUE,payload TEXT NOT NULL,hash TEXT NOT NULL,created TEXT NOT NULL,FOREIGN KEY(task_id) REFERENCES tasks(id))",
                "CREATE TABLE IF NOT EXISTS bindings (mention_id TEXT NOT NULL,version INTEGER NOT NULL,entity_id TEXT NOT NULL,method TEXT NOT NULL,decision_id TEXT,active INTEGER NOT NULL CHECK(active IN (0,1)),payload TEXT NOT NULL,created TEXT NOT NULL,PRIMARY KEY(mention_id,version),FOREIGN KEY(mention_id) REFERENCES mentions(id),FOREIGN KEY(entity_id) REFERENCES entities(id),FOREIGN KEY(decision_id) REFERENCES decisions(id))",
                "CREATE UNIQUE INDEX IF NOT EXISTS one_binding ON bindings(mention_id) WHERE active=1",
                "CREATE TABLE IF NOT EXISTS learned_aliases (id TEXT PRIMARY KEY,entity_id TEXT NOT NULL,payload TEXT NOT NULL,hash TEXT NOT NULL,decision_id TEXT NOT NULL,FOREIGN KEY(entity_id) REFERENCES entities(id),FOREIGN KEY(decision_id) REFERENCES decisions(id))",
                "CREATE TABLE IF NOT EXISTS observations (id TEXT PRIMARY KEY,doc_id TEXT NOT NULL,revision TEXT NOT NULL,payload TEXT NOT NULL,hash TEXT NOT NULL,FOREIGN KEY(doc_id,revision) REFERENCES sources(doc_id,revision))",
                "CREATE TABLE IF NOT EXISTS facts (id TEXT PRIMARY KEY,payload TEXT NOT NULL,hash TEXT NOT NULL)",
                "CREATE TABLE IF NOT EXISTS fact_occurrences (id TEXT PRIMARY KEY,fact_id TEXT NOT NULL,doc_id TEXT NOT NULL,revision TEXT NOT NULL,chunk_id TEXT NOT NULL,active INTEGER NOT NULL CHECK(active IN (0,1)),payload TEXT NOT NULL,hash TEXT NOT NULL,FOREIGN KEY(fact_id) REFERENCES facts(id),FOREIGN KEY(doc_id,revision) REFERENCES sources(doc_id,revision))",
                "CREATE INDEX IF NOT EXISTS occurrences_by_fact ON fact_occurrences(fact_id,active)",
                "CREATE INDEX IF NOT EXISTS occurrences_by_source ON fact_occurrences(doc_id,revision,chunk_id,active)",
                "CREATE TABLE IF NOT EXISTS generations (id TEXT PRIMARY KEY,status TEXT NOT NULL,payload TEXT NOT NULL,created TEXT NOT NULL)",
                "CREATE UNIQUE INDEX IF NOT EXISTS one_published_generation ON generations(status) WHERE status='published'",
                "CREATE TABLE IF NOT EXISTS outbox (id TEXT PRIMARY KEY,object_id TEXT NOT NULL,view TEXT NOT NULL,generation TEXT NOT NULL,content_hash TEXT NOT NULL,status TEXT NOT NULL,payload TEXT NOT NULL,UNIQUE(object_id,view,generation),FOREIGN KEY(generation) REFERENCES generations(id))",
                "CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT,type TEXT NOT NULL,payload TEXT NOT NULL,created TEXT NOT NULL,previous_hash TEXT NOT NULL,hash TEXT NOT NULL UNIQUE)",
            ]
            for statement in statements:
                self.db.execute(statement)
            for key, value in {"schema_version": SCHEMA_VERSION, "corpus_id": self.corpus_id}.items():
                old = self.db.execute("SELECT value FROM registry_meta WHERE key=?", (key,)).fetchone()
                if old and old[0] != value:
                    raise ValueError(f"Ledger {key} does not match this job")
                self.db.execute("INSERT OR IGNORE INTO registry_meta VALUES (?,?)", (key, value))

    @contextmanager
    def transaction(self) -> Iterator[None]:
        with self._lock:
            nested = self.db.in_transaction
            name = "s" + str(time.monotonic_ns())
            self.db.execute(f"SAVEPOINT {name}" if nested else "BEGIN IMMEDIATE")
            try:
                yield
            except BaseException:
                if nested:
                    self.db.execute(f"ROLLBACK TO {name}")
                    self.db.execute(f"RELEASE {name}")
                else:
                    self.db.rollback()
                raise
            else:
                self.db.execute(f"RELEASE {name}" if nested else "COMMIT")

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.close()

    def event(self, kind: str, payload: Mapping[str, Any]) -> str:
        with self.transaction():
            previous = self.db.execute("SELECT hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
            old_hash = previous[0] if previous else ""
            created = utc_now()
            value = {"type": kind, "payload": dict(payload), "created": created, "previous_hash": old_hash}
            signature = digest(value)
            self.db.execute("INSERT INTO events(type,payload,created,previous_hash,hash) VALUES (?,?,?,?,?)",
                            (kind, canonical_json(dict(payload)), created, old_hash, signature))
            return signature

    @staticmethod
    def _payload(value):
        return value.model_dump(mode="json") if hasattr(value, "model_dump") else dict(value)

    def import_batch(self, batch, *, source_metadata: Mapping[str, Any] | None = None) -> bool:
        from .contracts import RawBatch
        parsed = batch if isinstance(batch, RawBatch) else RawBatch.model_validate(batch)
        value = parsed.model_dump(mode="json")
        if value["corpus_id"] != self.corpus_id:
            raise ValueError("Raw extraction corpus does not match the ledger")
        signature = digest(value)
        with self.transaction():
            old = self.db.execute("SELECT hash FROM batches WHERE id=?", (value["extraction_id"],)).fetchone()
            if old:
                if old[0] != signature:
                    raise LedgerConflict("An extraction ID cannot overwrite its original payload")
                return False
            self.db.execute("INSERT OR IGNORE INTO sources VALUES (?,?,?,?,?)",
                            (value["doc_id"], value["revision_hash"], "staged",
                             canonical_json(dict(source_metadata or {})), utc_now()))
            self.db.execute("INSERT INTO batches VALUES (?,?,?,?,?,?,?)",
                            (value["extraction_id"], value["doc_id"], value["revision_hash"], value["chunk_id"],
                             value["status"], canonical_json(value), signature))
            # Partial failed output is retained only in the immutable batch
            # payload. It must never enter the resolvable mention population.
            for mention in value["mentions"] if value["status"] == "complete" else []:
                old_mention = self.db.execute("SELECT hash FROM mentions WHERE id=?", (mention["mention_id"],)).fetchone()
                if old_mention and old_mention[0] != digest(mention):
                    raise LedgerConflict("A mention ID cannot overwrite source evidence")
                self.db.execute("INSERT OR IGNORE INTO mentions VALUES (?,?,?,?,?,?,?)",
                                (mention["mention_id"], value["extraction_id"], value["doc_id"], value["revision_hash"],
                                 mention["local_id"], canonical_json(mention), digest(mention)))
            self.event("source_batch_imported", {"extraction_id": value["extraction_id"], "hash": signature})
        return True

    def activate_revision(self, doc_id: str, revision: str, *, expected_chunks: int):
        if expected_chunks < 1:
            raise ValueError("A source revision requires its positive expected chunk count")
        with self.transaction():
            source = self.db.execute("SELECT status FROM sources WHERE doc_id=? AND revision=?", (doc_id, revision)).fetchone()
            if not source:
                raise ValueError("Unknown source revision")
            batches = self.db.execute("SELECT chunk_id,status FROM batches WHERE doc_id=? AND revision=?", (doc_id, revision)).fetchall()
            chunks = {r["chunk_id"] for r in batches}
            successes = {r["chunk_id"] for r in batches if r["status"] in {"complete", "confirmed_empty"}}
            if len(chunks) != expected_chunks or successes != chunks:
                raise ValueError("Source activation requires complete valid extraction of every expected chunk")
            if source["status"] == "active":
                return
            affected = self.source_entities(doc_id)
            self.db.execute("UPDATE sources SET status='superseded' WHERE doc_id=? AND status='active'", (doc_id,))
            self.db.execute("UPDATE sources SET status='active' WHERE doc_id=? AND revision=?", (doc_id, revision))
            self.event("source_revision_activated", {"doc_id": doc_id, "revision": revision,
                                                      "affected_entities": sorted(affected | self.source_entities(doc_id))})

    def withdraw_source(self, doc_id: str) -> set[str]:
        with self.transaction():
            affected = self.source_entities(doc_id)
            rows = self.db.execute("SELECT revision FROM sources WHERE doc_id=? AND status='active'", (doc_id,)).fetchall()
            self.db.execute("UPDATE sources SET status='withdrawn' WHERE doc_id=? AND status='active'", (doc_id,))
            if rows:
                self.event("source_withdrawn", {"doc_id": doc_id, "revisions": [r[0] for r in rows],
                                                "affected_entities": sorted(affected)})
            return affected

    def source_entities(self, doc_id: str) -> set[str]:
        return {r[0] for r in self.db.execute("SELECT DISTINCT b.entity_id FROM bindings b JOIN mentions m ON m.id=b.mention_id JOIN sources s ON s.doc_id=m.doc_id AND s.revision=m.revision WHERE b.active=1 AND s.status='active' AND m.doc_id=?", (doc_id,))}

    def mentions(self, *, active_only=False, unbound_only=False) -> list[dict]:
        statuses = "('active')" if active_only else "('active','staged')"
        query = f"SELECT m.payload FROM mentions m JOIN sources s ON s.doc_id=m.doc_id AND s.revision=m.revision WHERE s.status IN {statuses}"
        if unbound_only:
            query += " AND NOT EXISTS (SELECT 1 FROM bindings b WHERE b.mention_id=m.id AND b.active=1)"
        query += " ORDER BY m.id"
        return [json.loads(r[0]) for r in self.db.execute(query)]

    def batches(self, *, active_only=False) -> list[dict]:
        statuses = "('active')" if active_only else "('active','staged')"
        return [json.loads(r[0]) for r in self.db.execute(f"SELECT b.payload FROM batches b JOIN sources s ON s.doc_id=b.doc_id AND s.revision=b.revision WHERE s.status IN {statuses} AND b.status IN ('complete','confirmed_empty') ORDER BY b.doc_id,b.chunk_id,b.id")]

    def ensure_entity(self, entity, *, status="confirmed", creation_key=None) -> str:
        if status not in {"confirmed", "provisional", "retired"}:
            raise ValueError("Unknown entity status")
        payload = self._payload(entity)
        entity_id = payload["canonical_id"]
        with self.transaction():
            if creation_key:
                existing = self.db.execute("SELECT id FROM entities WHERE creation_key=?", (creation_key,)).fetchone()
                if existing:
                    return existing[0]
            old = self.db.execute("SELECT hash FROM entities WHERE id=?", (entity_id,)).fetchone()
            if old:
                if old[0] != digest(payload):
                    raise LedgerConflict("Entity changes require an explicit revision event")
                return entity_id
            self.db.execute("INSERT INTO entities VALUES (?,?,?,?,?)", (entity_id, creation_key, status, canonical_json(payload), digest(payload)))
            self.event("entity_created", {"entity_id": entity_id, "status": status, "payload": payload})
        return entity_id

    def revise_entity(self, entity_id: str, payload: Mapping[str, Any], *, reason: str):
        if not reason or payload.get("canonical_id") != entity_id:
            raise ValueError("Entity revision requires its immutable ID and a reason")
        with self.transaction():
            old = self.db.execute("SELECT payload FROM entities WHERE id=?", (entity_id,)).fetchone()
            if not old:
                raise ValueError("Unknown entity")
            prior = json.loads(old[0])
            if prior == dict(payload):
                return
            if any(payload.get(k) != prior.get(k) for k in ("kind", "granularity")):
                raise LedgerConflict("Changing identity kind or granularity requires explicit mention rebinding")
            fields = set(prior.get("identity_guards", [])) | set(payload.get("identity_guards", [])) | set(prior.get("variant_dimensions", [])) | set(payload.get("variant_dimensions", []))
            if any(prior.get("properties", {}).get(field) != payload.get("properties", {}).get(field) for field in fields):
                raise LedgerConflict("Changing protected identity properties requires a new identity and explicit rebinding")
            status = payload.get("status", "confirmed")
            if status not in {"confirmed", "provisional", "retired"}:
                raise ValueError("Invalid entity status")
            self.db.execute("UPDATE entities SET payload=?,hash=?,status=? WHERE id=?", (canonical_json(payload), digest(payload), status, entity_id))
            self.event("entity_revised", {"entity_id": entity_id, "old": json.loads(old[0]), "new": dict(payload), "reason": reason})

    def entity(self, entity_id: str) -> dict | None:
        row = self.db.execute("SELECT payload,status FROM entities WHERE id=?", (entity_id,)).fetchone()
        return {**json.loads(row[0]), "status": row[1]} if row else None

    def bind(self, mention_id: str, entity_id: str, *, method: str, decision_id: str | None = None, metadata=None) -> int:
        payload = dict(metadata or {})
        with self.transaction():
            old = self.db.execute("SELECT * FROM bindings WHERE mention_id=? AND active=1", (mention_id,)).fetchone()
            if old and old["entity_id"] == entity_id and old["method"] == method and old["decision_id"] == decision_id and old["payload"] == canonical_json(payload):
                return old["version"]
            version = self.db.execute("SELECT COALESCE(MAX(version),0)+1 FROM bindings WHERE mention_id=?", (mention_id,)).fetchone()[0]
            self.db.execute("UPDATE bindings SET active=0 WHERE mention_id=? AND active=1", (mention_id,))
            self.db.execute("INSERT INTO bindings VALUES (?,?,?,?,?,?,?,?)", (mention_id, version, entity_id, method, decision_id, 1, canonical_json(payload), utc_now()))
            if old and old["entity_id"] != entity_id:
                source = self.db.execute("SELECT doc_id,revision,payload FROM mentions WHERE id=?", (mention_id,)).fetchone()
                chunk_id = json.loads(source["payload"])["chunk_id"]
                self.db.execute("UPDATE fact_occurrences SET active=0 WHERE doc_id=? AND revision=? AND chunk_id=?",
                                (source["doc_id"], source["revision"], chunk_id))
            self.event("mention_bound", {"mention_id": mention_id, "entity_id": entity_id, "version": version,
                                         "method": method, "previous_entity_id": old["entity_id"] if old else None})
            return version

    def bindings(self, *, active_sources=False) -> dict[str, dict]:
        query = "SELECT b.* FROM bindings b"
        if active_sources:
            query += " JOIN mentions m ON m.id=b.mention_id JOIN sources s ON s.doc_id=m.doc_id AND s.revision=m.revision"
        query += " WHERE b.active=1" + (" AND s.status='active'" if active_sources else "")
        return {r["mention_id"]: {**dict(r), "metadata": json.loads(r["payload"])} for r in self.db.execute(query)}

    def put_task(self, task_id: str, payload: Mapping[str, Any]) -> bool:
        with self.transaction():
            old = self.db.execute("SELECT hash FROM tasks WHERE id=?", (task_id,)).fetchone()
            if old:
                if old[0] != digest(payload):
                    raise LedgerConflict("Task ID has a different frozen payload")
                return False
            self.db.execute("INSERT INTO tasks VALUES (?,?,?,?,?,?,?)", (task_id, "pending", canonical_json(payload), digest(payload), None, None, utc_now()))
            self.event("resolution_task_created", {"task_id": task_id, "hash": digest(payload)})
        return True

    def tasks(self, statuses: Iterable[str] | None = None) -> list[dict]:
        args = tuple(statuses or ())
        query = "SELECT * FROM tasks" + (" WHERE status IN (" + ",".join("?" for _ in args) + ")" if args else "") + " ORDER BY id"
        return [{**dict(r), "payload": json.loads(r["payload"])} for r in self.db.execute(query, args)]

    def claim_task(self, task_id: str, owner: str, *, lease_seconds=660) -> bool:
        with self.transaction():
            old = self.db.execute("SELECT status,owner,lease_until FROM tasks WHERE id=?", (task_id,)).fetchone()
            if old and old["status"] == "running" and old["owner"]:
                from hyperche.request_leases import process_alive
                process_part = old["owner"].partition(":")[0]
                if process_part.isdigit() and process_alive(int(process_part)):
                    return False
            cursor = self.db.execute("UPDATE tasks SET status='running',owner=?,lease_until=?,updated=? WHERE id=? AND (status IN ('pending','technical_failed','budget_deferred') OR (status='running' AND lease_until<?))",
                                     (owner, time.time() + lease_seconds, utc_now(), task_id, time.time()))
            return cursor.rowcount == 1

    def task_status(self, task_id: str, status: str, *, owner: str | None = None):
        if status not in {"pending", "running", "completed", "technical_failed", "budget_deferred", "deferred_semantic"}:
            raise ValueError("Unknown task status")
        with self.transaction():
            row = self.db.execute("SELECT status,owner FROM tasks WHERE id=?", (task_id,)).fetchone()
            if not row or (owner is not None and row["owner"] != owner):
                raise LedgerConflict("Task is absent or owned by another worker")
            if row["status"] in {"completed", "deferred_semantic"} and status != row["status"]:
                raise LedgerConflict("A successful task cannot be reset")
            self.db.execute("UPDATE tasks SET status=?,owner=NULL,lease_until=NULL,updated=? WHERE id=?", (status, utc_now(), task_id))

    def attempt(self, task_id: str, payload: Mapping[str, Any]):
        with self.transaction():
            self.db.execute("INSERT INTO attempts(task_id,payload,created) VALUES (?,?,?)", (task_id, canonical_json(payload), utc_now()))

    def save_decision(self, task_id: str, payload: Mapping[str, Any]) -> str:
        decision_id = stable_id("decision", {"task_id": task_id, "payload": dict(payload)})
        with self.transaction():
            old = self.db.execute("SELECT id,hash FROM decisions WHERE task_id=?", (task_id,)).fetchone()
            if old:
                if old["hash"] != digest(payload):
                    raise LedgerConflict("A successful frozen task cannot be overwritten")
                return old["id"]
            self.db.execute("INSERT INTO decisions VALUES (?,?,?,?,?)", (decision_id, task_id, canonical_json(payload), digest(payload), utc_now()))
            self.event("identity_decided", {"decision_id": decision_id, "task_id": task_id, "hash": digest(payload)})
        return decision_id

    def decision(self, task_id: str) -> dict | None:
        row = self.db.execute("SELECT id,payload FROM decisions WHERE task_id=?", (task_id,)).fetchone()
        return {"decision_id": row["id"], **json.loads(row["payload"])} if row else None

    def add_learned_alias(self, alias: Mapping[str, Any], *, decision_id: str):
        signature = digest(alias)
        alias_id = stable_id("alias", {"binding": dict(alias), "decision_id": decision_id})
        with self.transaction():
            self.db.execute("INSERT OR IGNORE INTO learned_aliases VALUES (?,?,?,?,?)",
                            (alias_id, alias["canonical_id"], canonical_json(alias), signature, decision_id))

    def learned_aliases(self) -> list[dict]:
        return [{**json.loads(r["payload"]), "decision_id": r["decision_id"]} for r in self.db.execute("SELECT payload,decision_id FROM learned_aliases ORDER BY id")]

    def save_observation(self, observation: Mapping[str, Any]):
        self._insert_immutable("observations", observation["observation_id"], observation,
                               extra=(observation["doc_id"], observation["revision_hash"]))

    def save_fact(self, fact: Mapping[str, Any], occurrence: Mapping[str, Any]):
        with self.transaction():
            self._insert_immutable("facts", fact["fact_id"], fact)
            self._insert_immutable("fact_occurrences", occurrence["occurrence_id"], occurrence,
                                   extra=(fact["fact_id"], occurrence["doc_id"], occurrence["revision_hash"], occurrence["chunk_id"], 1))

    def _insert_immutable(self, table: str, record_id: str, payload: Mapping[str, Any], extra=()):
        if table not in {"observations", "facts", "fact_occurrences"}:
            raise ValueError("Unsupported immutable record table")
        with self.transaction():
            old = self.db.execute(f"SELECT hash FROM {table} WHERE id=?", (record_id,)).fetchone()
            if old and old[0] != digest(payload):
                raise LedgerConflict(f"Immutable {table} ID collision")
            values = (record_id, *extra, canonical_json(payload), digest(payload))
            self.db.execute(f"INSERT OR IGNORE INTO {table} VALUES ({','.join('?' for _ in values)})", values)
            if table == "fact_occurrences":
                self.db.execute("UPDATE fact_occurrences SET active=1 WHERE id=?", (record_id,))

    def active_facts(self) -> list[dict]:
        return [{**json.loads(r["payload"]), "occurrences": self.fact_occurrences(r["id"])} for r in self.db.execute("SELECT DISTINCT f.id,f.payload FROM facts f JOIN fact_occurrences o ON o.fact_id=f.id JOIN sources s ON s.doc_id=o.doc_id AND s.revision=o.revision WHERE s.status='active' AND o.active=1 ORDER BY f.id")]

    def fact_occurrences(self, fact_id: str) -> list[dict]:
        return [json.loads(r[0]) for r in self.db.execute("SELECT o.payload FROM fact_occurrences o JOIN sources s ON s.doc_id=o.doc_id AND s.revision=o.revision WHERE o.fact_id=? AND s.status='active' AND o.active=1 ORDER BY o.id", (fact_id,))]

    def begin_generation(self, generation_id: str, payload: Mapping[str, Any]):
        with self.transaction():
            old = self.db.execute("SELECT payload FROM generations WHERE id=?", (generation_id,)).fetchone()
            if old and old[0] != canonical_json(payload):
                raise LedgerConflict("Generation ID has a different frozen manifest")
            self.db.execute("INSERT OR IGNORE INTO generations VALUES (?,?,?,?)", (generation_id, "draft", canonical_json(payload), utc_now()))

    def enqueue_projection(self, object_id: str, view: str, generation: str, content_hash: str, payload: Mapping[str, Any]) -> str:
        task_id = stable_id("projection", [object_id, view, generation])
        with self.transaction():
            old = self.db.execute("SELECT content_hash FROM outbox WHERE id=?", (task_id,)).fetchone()
            if old and old[0] != content_hash:
                raise LedgerConflict("Projection content changed inside a frozen generation")
            self.db.execute("INSERT OR IGNORE INTO outbox VALUES (?,?,?,?,?,?,?)", (task_id, object_id, view, generation, content_hash, "pending", canonical_json(payload)))
        return task_id

    def projection_tasks(self, generation: str, *, pending_only=True) -> list[dict]:
        return [{**dict(r), "payload": json.loads(r["payload"])} for r in self.db.execute("SELECT * FROM outbox WHERE generation=?" + (" AND status='pending'" if pending_only else "") + " ORDER BY id", (generation,))]

    def mark_projection_applied(self, task_id: str, *, content_hash: str):
        with self.transaction():
            cursor = self.db.execute("UPDATE outbox SET status='applied' WHERE id=? AND content_hash=?", (task_id, content_hash))
            if not cursor.rowcount:
                raise LedgerConflict("Projection receipt does not match its expected signature")

    def publish_generation(self, generation: str):
        with self.transaction():
            row = self.db.execute("SELECT payload,status FROM generations WHERE id=?", (generation,)).fetchone()
            if not row:
                raise ValueError("Unknown generation")
            if self.projection_tasks(generation):
                raise ValueError("Cannot publish a generation with unapplied projections")
            scope = json.loads(row["payload"]).get("resolution_task_ids")
            tasks = {t["id"]: t for t in self.tasks()}
            if scope is not None and (not isinstance(scope, list) or set(scope) - set(tasks)):
                raise ValueError("Generation has an invalid frozen resolution scope")
            relevant = tasks.values() if scope is None else [tasks[key] for key in scope]
            if any(t["status"] not in {"completed", "deferred_semantic"} for t in relevant):
                raise ValueError("Cannot publish while resolution tasks are technically unfinished")
            if row["status"] == "published":
                return
            self.db.execute("UPDATE generations SET status='superseded' WHERE status='published' AND id<>?", (generation,))
            self.db.execute("UPDATE generations SET status='published' WHERE id=?", (generation,))
            self.event("generation_published", {"generation": generation})

    def verify_event_chain(self) -> bool:
        previous = ""
        for row in self.db.execute("SELECT * FROM events ORDER BY seq"):
            value = {"type": row["type"], "payload": json.loads(row["payload"]), "created": row["created"], "previous_hash": previous}
            if row["previous_hash"] != previous or row["hash"] != digest(value):
                return False
            previous = row["hash"]
        return True

    def counts(self) -> dict[str, int]:
        return {t: self.db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                for t in ("sources", "batches", "mentions", "entities", "tasks", "decisions", "bindings", "facts", "fact_occurrences", "observations", "events", "outbox")}

    def export(self, target: str | Path) -> dict[str, str]:
        root = Path(target)
        root.mkdir(parents=True, exist_ok=True)
        checksums = {}
        with self.transaction():
            for table in ("sources", "batches", "mentions", "entities", "tasks", "attempts", "decisions", "bindings", "learned_aliases", "observations", "facts", "fact_occurrences", "generations", "outbox", "events"):
                path = root / (table + ".jsonl")
                with path.open("w", encoding="utf-8") as stream:
                    for row in self.db.execute(f"SELECT * FROM {table} ORDER BY rowid"):
                        item = dict(row)
                        for name in ("payload",):
                            if name in item:
                                item[name] = json.loads(item[name])
                        stream.write(canonical_json(item) + "\n")
                checksums[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        return checksums
