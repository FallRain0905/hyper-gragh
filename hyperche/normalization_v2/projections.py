"""Deterministic fact-store and search projections with atomic release pointers."""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import re
import uuid

import numpy as np

from .contracts import canonical_json, digest, stable_id


FORMAT_VERSION = "role-fact-dual-1"


def generation_directory(root, generation):
    if not re.fullmatch(r"generation:[a-f0-9]{32}", generation):
        raise ValueError("Invalid generation identifier")
    return Path(root) / "generations" / generation.replace(":", "_")


def atomic_bytes(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_json(path: Path, value):
    atomic_bytes(path, (canonical_json(value) + "\n").encode())


def tokens(text):
    return re.findall(r"[\w]+|[\u4e00-\u9fff]", text.casefold())


def projection_records(ledger):
    facts = ledger.active_facts()
    bindings = ledger.bindings(active_sources=True)
    mentions = {m["mention_id"]: m for m in ledger.mentions(active_only=True)}
    surfaces, source_refs = defaultdict(set), defaultdict(set)
    for mid, binding in bindings.items():
        mention = mentions[mid]
        identifier = binding["entity_id"]
        surfaces[identifier].add(mention["raw_name"])
        source_refs[identifier].add(mention["chunk_id"])
    records, entities = [], {}
    for identifier in sorted(surfaces):
        entity = ledger.entity(identifier)
        if not entity or entity["status"] == "retired":
            raise ValueError("An active mention has an unavailable identity")
        entities[identifier] = entity
        canonical = canonical_json({"name": entity["canonical_name"], "kind": entity["kind"],
            "granularity": entity.get("granularity"), "properties": entity.get("properties", {}),
            "parent_id": entity.get("parent_id")})
        surface = "\n".join(sorted(surfaces[identifier]))
        records.append({"object_id": identifier, "view": "entity", "canonical": canonical,
                        "surface": surface, "text": canonical + "\n" + surface,
                        "source_chunk_ids": sorted(source_refs[identifier]), "data": entity})
    buckets = defaultdict(list)
    bucket_vertices = {}
    for fact in facts:
        # Evidence additions are provenance changes; they do not change index
        # text unless the actual fact/role/quantity or surface changes.
        data = {k: v for k, v in fact.items() if k != "occurrences"}
        canonical = canonical_json({k: data[k] for k in ("relation_type", "roles", "conditions", "polarity", "assertion", "observations")})
        names = {role: [entities[eid]["canonical_name"] for eid in members] for role, members in fact["roles"].items()}
        surface = canonical_json({"roles": names, "relation_type": fact["relation_type"]})
        refs = sorted({o["chunk_id"] for o in fact["occurrences"]})
        records.append({"object_id": fact["fact_id"], "view": "fact", "canonical": canonical,
                        "surface": surface, "text": canonical + "\n" + surface,
                        "source_chunk_ids": refs, "data": fact})
        buckets[fact["structural_bucket"]].append(fact["fact_id"])
        bucket_vertices[fact["structural_bucket"]] = fact["vertices"]
    return records, {identifier: {"fact_ids": sorted(ids),
            "vertices": bucket_vertices[identifier]}
            for identifier, ids in sorted(buckets.items())}


class VectorCache:
    def __init__(self, root, *, model: str, dimension: int):
        if not model or isinstance(dimension, bool) or dimension < 1:
            raise ValueError("Explicit model and dimension required")
        self.root, self.model, self.dimension = Path(root), model, dimension
        self.root.mkdir(parents=True, exist_ok=True)

    def signature(self, record):
        return digest({"text": record["text"], "view": record["view"], "format": FORMAT_VERSION,
                       "model": self.model, "dimension": self.dimension})

    def load(self, signature):
        path = self.root / (signature + ".npz")
        if not path.exists(): return None
        with np.load(path, allow_pickle=False) as data:
            if str(data["model"]) != self.model or int(data["dimension"]) != self.dimension or str(data["signature"]) != signature:
                raise ValueError("Vector checkpoint metadata mismatch")
            value = data["vector"]
        return self.validate(value)

    def validate(self, value):
        value = np.asarray(value, dtype=np.float32)
        if value.shape != (self.dimension,) or not np.isfinite(value).all() or not np.any(value != 0):
            raise ValueError("Vector checkpoint must be finite, nonzero and exact dimension")
        return value

    def save(self, signature, vector):
        import io
        vector = self.validate(vector)
        existing = self.load(signature)
        if existing is not None:
            if not np.array_equal(existing, vector):
                raise ValueError("A successful vector signature is immutable")
            return
        stream = io.BytesIO()
        np.savez_compressed(stream, vector=vector, signature=signature, model=self.model, dimension=self.dimension)
        atomic_bytes(self.root / (signature + ".npz"), stream.getvalue())


class Projector:
    def __init__(self, ledger, root, *, model, dimension):
        self.ledger, self.root = ledger, Path(root)
        self.cache = VectorCache(self.root / "vector_checkpoints", model=model, dimension=dimension)

    def prepare(self, *, registry_hash, task_ids):
        records, graph = projection_records(self.ledger)
        batches = self.ledger.batches(active_only=True)
        # Chunk payloads retain source-exact text independently of identity
        # display names. Full source contents never enter identity embeddings.
        chunks = {b["chunk_id"]: {"doc_id": b["doc_id"], "revision_hash": b["revision_hash"],
                   "chunk_hash": b["chunk_hash"], "content": b["raw_text"]} for b in batches}
        if len(chunks) != len(batches):
            raise ValueError("Chunk IDs must be unique in a corpus")
        payload = {"format": FORMAT_VERSION, "registry_hash": registry_hash,
            "model": self.cache.model, "dimension": self.cache.dimension,
            "records": records, "graph": graph, "chunks": chunks,
            "resolution_task_ids": sorted(set(task_ids))}
        generation = stable_id("generation", payload)
        self.ledger.begin_generation(generation, payload)
        directory = generation_directory(self.root, generation)
        directory.mkdir(parents=True, exist_ok=True)
        atomic_json(directory / "draft.json", payload)
        for record in records:
            signature = self.cache.signature(record)
            task_id = self.ledger.enqueue_projection(record["object_id"], record["view"], generation, signature, record)
            if self.cache.load(signature) is not None:
                self.ledger.mark_projection_applied(task_id, content_hash=signature)
        return generation

    async def embed(self, generation, embedder, *, batch_size=16):
        if not 1 <= batch_size <= 256:
            raise ValueError("Invalid embedding batch size")
        pending = self.ledger.projection_tasks(generation)
        calls, vectors = 0, 0
        for start in range(0, len(pending), batch_size):
            group = pending[start:start + batch_size]
            texts = [task["payload"]["text"] for task in group]
            output = np.asarray(await embedder(texts, model=self.cache.model, dimensions=self.cache.dimension), dtype=np.float32)
            calls += 1
            if output.shape != (len(group), self.cache.dimension):
                raise ValueError("Embedding batch shape mismatch")
            # Validate entire batch before writing any partial success.
            for vector in output: self.cache.validate(vector)
            for task, vector in zip(group, output):
                self.cache.save(task["content_hash"], vector)
                self.ledger.mark_projection_applied(task["id"], content_hash=task["content_hash"])
                vectors += 1
        return {"embedding_calls": calls, "new_vectors": vectors,
                "identity_candidate_embedding_calls": 0}

    def publish(self, generation):
        directory = generation_directory(self.root, generation)
        draft = json.loads((directory / "draft.json").read_text(encoding="utf-8"))
        if stable_id("generation", draft) != generation:
            raise ValueError("Generation draft does not match its immutable ID")
        if self.ledger.projection_tasks(generation):
            raise ValueError("Embedding projections are incomplete")
        vectors = [self.cache.load(self.cache.signature(record)) for record in draft["records"]]
        if any(vector is None for vector in vectors):
            raise ValueError("A generation vector is unavailable")
        # Each release contains a self-sufficient, hash-verified fact store and
        # sparse index. Pointer replacement is the only publication operation.
        outputs = {"records.json": draft["records"], "graph.json": draft["graph"],
                   "chunks.json": draft["chunks"], "lexical.json": [dict(Counter(tokens(r["text"]))) for r in draft["records"]]}
        for name, value in outputs.items(): atomic_json(directory / name, value)
        import io
        stream = io.BytesIO()
        np.save(stream, np.stack(vectors) if vectors else np.empty((0, self.cache.dimension), dtype=np.float32), allow_pickle=False)
        atomic_bytes(directory / "vectors.npy", stream.getvalue())
        files = {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in [*outputs, "vectors.npy"]}
        manifest = {"generation": generation, "format": FORMAT_VERSION, "model": self.cache.model,
                    "dimension": self.cache.dimension, "files": files, "complete": True,
                    "counts": {"records": len(draft["records"]), "chunks": len(draft["chunks"]), "buckets": len(draft["graph"])}}
        atomic_json(directory / "manifest.json", manifest)
        # A DB commit preceding a failed file switch leaves the previous file
        # release readable; rerunning finishes the same deterministic release.
        self.ledger.publish_generation(generation)
        atomic_json(self.root / "current.json", {"generation": generation,
                    "manifest_hash": digest(manifest), "complete": True})
        return manifest


class RetrievalAdapter:
    def __init__(self, root):
        root = Path(root)
        pointer = json.loads((root / "current.json").read_text(encoding="utf-8"))
        identifier = pointer["generation"]
        if not re.fullmatch(r"generation:[a-f0-9]{32}", identifier):
            raise ValueError("Invalid release identifier")
        directory = generation_directory(root, identifier)
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        if not pointer.get("complete") or not manifest.get("complete") or digest(manifest) != pointer["manifest_hash"]:
            raise ValueError("Incomplete or altered release")
        if manifest.get("generation") != identifier or set(manifest["files"]) != {"records.json", "graph.json", "chunks.json", "lexical.json", "vectors.npy"}:
            raise ValueError("Release manifest has an invalid file set or generation")
        for name, signature in manifest["files"].items():
            if Path(name).name != name or hashlib.sha256((directory / name).read_bytes()).hexdigest() != signature:
                raise ValueError("Release file hash mismatch")
        self.manifest = manifest
        self.records = json.loads((directory / "records.json").read_text(encoding="utf-8"))
        self.chunks = json.loads((directory / "chunks.json").read_text(encoding="utf-8"))
        self.lexical = json.loads((directory / "lexical.json").read_text(encoding="utf-8"))
        self.vectors = np.load(directory / "vectors.npy", allow_pickle=False)
        if self.vectors.shape != (len(self.records), manifest["dimension"]) or not np.isfinite(self.vectors).all() or (len(self.records) and not np.all(np.any(self.vectors != 0, axis=1))):
            raise ValueError("Invalid released vectors")
        if len(self.lexical) != len(self.records) or len({(r["object_id"], r["view"]) for r in self.records}) != len(self.records):
            raise ValueError("Released record/index IDs are inconsistent")
        for chunk in self.chunks.values():
            if hashlib.sha256(chunk["content"].encode()).hexdigest() != chunk["chunk_hash"]:
                raise ValueError("Released source chunk hash mismatch")
        if any(identifier not in self.chunks for record in self.records for identifier in record["source_chunk_ids"]):
            raise ValueError("A released record has an unresolved source")

    def search(self, query, *, query_vector=None, top_k=5, lexical_weight=1.0, dense_weight=1.0, rrf_k=60):
        if top_k < 1 or rrf_k < 1 or min(lexical_weight, dense_weight) < 0:
            raise ValueError("Invalid retrieval parameters")
        count = len(self.records)
        lexical, dense = np.zeros(count), np.zeros(count)
        avg = sum(sum(row.values()) for row in self.lexical) / max(1, count)
        for token in set(tokens(query)):
            df = sum(token in row for row in self.lexical)
            idf = math.log(1 + (count - df + 0.5) / (df + 0.5))
            for i, row in enumerate(self.lexical):
                tf = row.get(token, 0)
                if tf: lexical[i] += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * sum(row.values()) / max(avg, 1)))
        scores = defaultdict(float)
        lists = [(lexical, lexical_weight)]
        if query_vector is not None:
            query_vector = np.asarray(query_vector, dtype=np.float32)
            if query_vector.shape != (self.manifest["dimension"],) or not np.isfinite(query_vector).all() or not np.any(query_vector):
                raise ValueError("Query vector is not compatible with this release")
            matrix = self.vectors.astype(np.float64)
            query64 = query_vector.astype(np.float64)
            norms = np.linalg.norm(matrix, axis=1) * np.linalg.norm(query64)
            dense = matrix @ query64 / norms
            lists.append((dense, dense_weight))
        for values, weight in lists:
            order = sorted(range(count), key=lambda i: (-values[i], self.records[i]["object_id"]))
            for rank, i in enumerate(order, 1):
                if weight and (values[i] > 0 or values is dense): scores[i] += weight / (rrf_k + rank)
        results = []
        for i in sorted(scores, key=lambda i: (-scores[i], self.records[i]["object_id"]))[:top_k]:
            record = self.records[i]
            results.append({**record, "score": scores[i], "sources": [
                {"chunk_id": chunk, **self.chunks[chunk]} for chunk in record["source_chunk_ids"]]})
        return results
