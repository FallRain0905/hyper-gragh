"""Build role-aware facts independently of unordered hypergraph buckets."""
from __future__ import annotations

from collections import Counter
import json
from typing import Mapping

from .contracts import RawBatch, digest, stable_id, validate_evidence
from .quantities import UnitRegistry, observation


class FactError(ValueError):
    pass


def build_facts(batch: RawBatch | dict, bindings: Mapping[str, dict], *,
                units: UnitRegistry | None = None, relation_aliases: Mapping[str, str] | None = None) -> dict:
    parsed = batch if isinstance(batch, RawBatch) else RawBatch.model_validate(batch)
    source = parsed.model_dump(mode="json")
    local = {m["local_id"]: m for m in source["mentions"]}
    by_local = {}
    for local_id, mention in local.items():
        bound = bindings.get(mention["mention_id"])
        if bound:
            by_local[local_id] = bound.get("entity_id") or bound.get("canonical_id")
    facts, quantities, issues = [], [], []
    for raw in source["facts"]:
        mapped_roles = {}
        for role, members in raw["roles"].items():
            if not members or any(m not in local or not by_local.get(m) for m in members):
                raise FactError("Every fact role must reference a bound mention from its exact source batch")
            # Preserve multiplicity and role-local order. Templates may later
            # explicitly declare a role unordered; no implicit global sorting.
            mapped_roles[role] = [by_local[m] for m in members]
        if not mapped_roles:
            raise FactError("A fact requires at least one explicit role")
        for span in raw.get("evidence", []):
            validate_evidence(span, source["raw_text"], source["chunk_id"])
        context = {"doc_id": source["doc_id"], "revision_hash": source["revision_hash"],
                   "scope": raw.get("context_id") or (source["chunk_id"] + ":" + raw["local_id"]),
                   "explicit": bool(raw.get("context_id"))}
        context_id = stable_id("context", context)
        observation_rows = []
        for index, measure in enumerate(raw.get("observations", [])):
            metric = measure.get("metric") or measure.get("metric_local_id")
            if metric not in by_local:
                issues.append({"fact_local_id": raw["local_id"], "observation_index": index,
                               "reason": "metric_must_reference_a_local_bound_mention", "original": measure})
                continue
            entry = observation(measure, metric_id=by_local[metric], roles=mapped_roles,
                                doc_id=source["doc_id"], revision_hash=source["revision_hash"],
                                chunk_id=source["chunk_id"], local_id=raw["local_id"] + f":q{index}",
                                context_id=context_id, units=units, dimension=measure.get("dimension"),
                                bounds=tuple(measure["bounds"]) if measure.get("bounds") else None)
            observation_rows.append(entry)
            quantities.append(entry)
            if entry["status"] != "normalized_explicit":
                issues.append({"fact_local_id": raw["local_id"], "observation_index": index,
                               "reason": entry["reason"], "observation_id": entry["observation_id"]})
        relation_type = (relation_aliases or {}).get(raw["relation_type"], raw["relation_type"])
        identity = {"relation_type": relation_type, "roles": mapped_roles, "context": context,
                    "conditions": raw.get("conditions", {}), "polarity": raw.get("polarity", "positive"),
                    "assertion": raw.get("assertion", "reported"),
                    "observations": [{"metric_id": q["metric_id"], "raw": q["raw"],
                                      "canonical": q["canonical"], "status": q["status"]} for q in observation_rows],
                    "unresolved_observations": [i for i in issues if i["fact_local_id"] == raw["local_id"] and "original" in i]}
        fact_id = stable_id("fact", identity)
        vertices = sorted({v for members in mapped_roles.values() for v in members} |
                          {q["observation_id"] for q in observation_rows})
        fact = {"fact_id": fact_id, **identity, "vertices": vertices,
                "structural_bucket": stable_id("bucket", vertices),
                "observation_ids": [q["observation_id"] for q in observation_rows]}
        occurrence = {"occurrence_id": stable_id("occurrence", [source["extraction_id"], raw["local_id"], fact_id]),
                      "doc_id": source["doc_id"], "revision_hash": source["revision_hash"],
                      "chunk_id": source["chunk_id"], "extraction_id": source["extraction_id"],
                      "fact_local_id": raw["local_id"], "raw_fact": raw,
                      "mention_ids": [local[m]["mention_id"] for ids in raw["roles"].values() for m in ids],
                      "evidence": raw.get("evidence", [])}
        facts.append({"fact": fact, "occurrence": occurrence})
    return {"facts": facts, "observations": quantities, "issues": issues,
            "counts": {"facts": len(facts), "observations": len(quantities),
                       "quantity_statuses": dict(Counter(q["status"] for q in quantities))}}


def persist_batch_facts(ledger, batch: RawBatch | dict, *, units=None, relation_aliases=None) -> dict:
    source = batch.model_dump(mode="json") if isinstance(batch, RawBatch) else batch
    built = build_facts(batch, ledger.bindings(), units=units, relation_aliases=relation_aliases)
    with ledger.transaction():
        old = {r[0] for r in ledger.db.execute("SELECT id FROM fact_occurrences WHERE doc_id=? AND revision=? AND chunk_id=? AND active=1",
                                               (source["doc_id"], source["revision_hash"], source["chunk_id"]))}
        expected = {r["occurrence"]["occurrence_id"] for r in built["facts"]}
        if old != expected:
            ledger.db.execute("UPDATE fact_occurrences SET active=0 WHERE doc_id=? AND revision=? AND chunk_id=?",
                              (source["doc_id"], source["revision_hash"], source["chunk_id"]))
        for row in built["observations"]:
            ledger.save_observation(row)
        for row in built["facts"]:
            ledger.save_fact(row["fact"], row["occurrence"])
        if old != expected:
            ledger.event("source_facts_projected", {"extraction_id": source["extraction_id"],
                                                    "old_occurrences": sorted(old), "new_occurrences": sorted(expected)})
    return built
