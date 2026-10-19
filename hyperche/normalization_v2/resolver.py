"""Dictionary-first offline resolution; only unresolved candidates create tasks."""
from __future__ import annotations

from collections import Counter
from typing import Mapping

from .candidate_index import CandidateIndex, compatible
from .contracts import CanonicalEntity, Mention, digest, stable_id
from .text_policy import default_normalizer_for_kind, normalize


RESOLVER_POLICY = "dictionary-local-provisional-candidates-1"


class Resolver:
    def __init__(self, ledger, registry, *, profile_hash: str, prompt_hash: str,
                 candidate_limit=5):
        if not profile_hash or not prompt_hash:
            raise ValueError("Explicit profile and prompt fingerprints are required")
        self.ledger, self.registry = ledger, registry
        self.profile_hash, self.prompt_hash = profile_hash, prompt_hash
        self._dependency_hashes = {}
        self._learned_index = {}
        for alias in ledger.learned_aliases():
            key = (alias.get("kind"), alias.get("granularity"), digest(alias.get("scope")),
                   alias.get("normalizer", "exact"), alias.get("normalized"))
            self._learned_index.setdefault(key, []).append(alias)
        self.index = CandidateIndex(registry.entities.values(), limit=candidate_limit)
        for row in ledger.db.execute("SELECT payload FROM entities ORDER BY id"):
            import json
            self.index.add(json.loads(row[0]))

    def scope(self, mention):
        return {**mention.scope, "doc_id": mention.doc_id, "revision_hash": mention.revision_hash}

    def dependency_hash(self, ids):
        key = tuple(sorted(set(ids)))
        if key not in self._dependency_hashes:
            self._dependency_hashes[key] = self.registry.dependency_hash(key)
        return self._dependency_hashes[key]

    def _provisional(self, mention, *, reason, parent_id=None):
        # Unknown names are not promoted to corpus-wide aliases. Identical
        # source-local names can share a provisional concept while samples and
        # variants preserve all explicitly extracted identity attributes.
        policy = default_normalizer_for_kind(mention.kind)
        key = {"kind": mention.kind, "granularity": mention.granularity,
               "name": normalize(mention.raw_name, policy), "scope": self.scope(mention),
               "attributes": mention.attributes, "parent_id": parent_id}
        identifier = stable_id("provisional", key)
        entity = CanonicalEntity(canonical_id=identifier, canonical_name=mention.raw_name,
                                 kind=mention.kind, granularity=mention.granularity,
                                 properties=mention.attributes, parent_id=parent_id,
                                 name_normalizer=policy, status="provisional")
        if self.ledger.entity(identifier) is None:
            self.ledger.ensure_entity(entity, status="provisional", creation_key=digest(key))
        else:
            entity = CanonicalEntity.model_validate(self.ledger.entity(identifier))
        self.index.add(entity)
        return identifier, key

    def _bind(self, mention, identifier, method, **metadata):
        if identifier in self.registry.entities:
            entity = self.registry.entities[identifier]
            old = self.ledger.entity(identifier)
            if old is None:
                self.ledger.ensure_entity(entity)
            elif old != entity.model_dump(mode="json"):
                self.ledger.revise_entity(identifier, entity.model_dump(mode="json"),
                                          reason="explicit registry revision")
        self.ledger.bind(mention.mention_id, identifier, method=method, metadata=metadata)
        return {"mention_id": mention.mention_id, "canonical_id": identifier,
                "status": method, **metadata}

    def _learned(self, mention):
        result = set()
        candidates = []
        for policy in ("common_name", "chemical_formula", "exact"):
            key = (mention.kind, mention.granularity, digest(self.scope(mention)), policy, normalize(mention.raw_name, policy))
            candidates.extend(self._learned_index.get(key, ()))
        for alias in candidates:
            policy = alias.get("normalizer", "exact")
            if normalize(mention.raw_name, policy) != alias.get("normalized"):
                continue
            if alias.get("attributes") != mention.attributes:
                continue
            identifier = alias["canonical_id"]
            dependencies = alias.get("dependency_ids", [identifier] if identifier in self.registry.entities else [])
            if dependencies:
                if any(i not in self.registry.entities for i in dependencies):
                    continue
                if alias.get("dependency_hash") != self.dependency_hash(dependencies):
                    continue
            entity = self.ledger.entity(identifier)
            if entity and compatible(mention, CanonicalEntity.model_validate(entity), exact=True):
                result.add(identifier)
        return sorted(result)

    def resolve(self, mention: Mention | Mapping):
        mention = Mention.model_validate(mention)
        matches = self.registry.lookup(mention.raw_name, mention.kind, self.scope(mention),
                                       mention.attributes, mention.granularity)
        dependency_ids = [e.canonical_id for e in matches]
        if len(matches) == 1:
            return self._bind(mention, matches[0].canonical_id, "resolved_dictionary",
                              dependency_hash=self.dependency_hash(dependency_ids))
        learned = self._learned(mention)
        if len(learned) == 1 and not matches:
            return self._bind(mention, learned[0], "resolved_learned")
        provisional, creation_key = self._provisional(mention, reason="unresolved")
        # A repeated exact local provisional is deterministic and does not
        # create a candidate task against itself.
        candidate = self.index.find(mention, exclude=[provisional])
        if not candidate.candidates and not candidate.too_broad:
            return self._bind(mention, provisional, "provisional_new", reason="no_candidate",
                              creation_key=creation_key)
        if candidate.too_broad:
            return self._bind(mention, provisional, "deferred_semantic", reason="candidate_cap_exceeded",
                              matched_count=candidate.matched_count)
        ids = [e.canonical_id for e in candidate.candidates]
        registered = [i for i in ids if i in self.registry.entities]
        deps = self.dependency_hash(registered) if registered else digest([])
        # Full snapshot hash is stored as provenance, but excluded from the
        # task ID. Unrelated alias additions cannot invalidate this decision.
        payload = {"mention": mention.model_dump(mode="json"), "provisional_id": provisional,
                   "candidates": [e.model_dump(mode="json") for e in candidate.candidates],
                   "candidate_reasons": candidate.reasons, "dependency_hash": deps,
                   "policy": RESOLVER_POLICY, "profile_hash": self.profile_hash,
                   "prompt_hash": self.prompt_hash}
        task_id = stable_id("identity-task", payload)
        # Snapshot references live in the event stream, outside the immutable
        # identity task payload used for idempotent resume.
        inserted = self.ledger.put_task(task_id, payload)
        if inserted:
            self.ledger.event("registry_task_snapshot", {"task_id": task_id,
                             "snapshot_hash": self.registry.snapshot_hash})
        decision = self.ledger.decision(task_id)
        if decision:
            identifier = decision["canonical_id"]
            return self._bind(mention, identifier, decision["binding_method"], task_id=task_id)
        return self._bind(mention, provisional, "pending_judgment", task_id=task_id)

    def run(self):
        records = [self.resolve(mention) for mention in self.ledger.mentions()]
        return {"records": records, "counts": dict(Counter(r["status"] for r in records)),
                "identity_embedding_requests": 0, "identity_llm_requests": 0}
