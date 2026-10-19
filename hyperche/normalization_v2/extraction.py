"""Source-assigned sidecar for a single existing extraction call.

This adapter does not call a model, compare identities, embed names, or append
the registry vocabulary to an extraction prompt. Models supply only local
records; corpus/document/version identifiers and hashes belong to the caller.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .contracts import EvidenceSpan, Mention, RawBatch, RawFact, digest, locate_evidence, stable_id


class LocalEntity(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    local_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    kind: str = Field(min_length=1)
    roles: list[str] = Field(default_factory=list)
    granularity: str = "concept"
    attributes: dict[str, Any] = Field(default_factory=dict)
    aliases: list[str] = Field(default_factory=list)
    evidence: list[dict] = Field(default_factory=list)


class LocalFact(RawFact):
    evidence: list[dict] = Field(default_factory=list)


class ExtractionPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    entities: list[LocalEntity]
    facts: list[LocalFact]
    alias_assertions: list[dict] = Field(default_factory=list)


def _spans(values, text, chunk_id):
    spans, unavailable = [], []
    for item in values:
        if isinstance(item, EvidenceSpan):
            item = item.model_dump()
        if set(item) - {"quote", "start", "end", "chunk_id"}:
            raise ValueError("Unknown evidence fields")
        if item.get("chunk_id", chunk_id) != chunk_id:
            raise ValueError("Cross-chunk evidence is not allowed")
        quote = item.get("quote")
        if not isinstance(quote, str) or not quote or quote not in text:
            raise ValueError("Extraction evidence is absent from source")
        # Ambiguous repeated quotes are reported as unlocated, never assigned
        # the first occurrence. Explicit offsets must validate exactly.
        if item.get("start") is None and text.count(quote) > 1:
            unavailable.append({"quote": quote, "chunk_id": chunk_id, "reason": "ambiguous_span"})
            continue
        span = locate_evidence(quote, text, chunk_id=chunk_id,
                               start=item.get("start"), end=item.get("end"))
        spans.append(span)
    return spans, unavailable


def adapt_live_response(response_text: str, *, finish_reason: str, stream_complete: bool,
                        corpus_id: str, doc_id: str, revision_hash: str, chunk_id: str,
                        raw_text: str, prompt_hash: str, model_profile_hash: str,
                        scope=None) -> RawBatch:
    if finish_reason != "stop" or stream_complete is not True:
        raise ValueError("Truncated or incomplete extraction cannot become an empty success")
    payload = ExtractionPayload.model_validate(json.loads(response_text))
    source = {"doc_id": doc_id, "revision_hash": revision_hash, "chunk_id": chunk_id}
    mentions, unresolved_spans = [], []
    for entity in payload.entities:
        spans, missing = _spans(entity.evidence, raw_text, chunk_id)
        unresolved_spans += [{"local_id": entity.local_id, **item} for item in missing]
        mentions.append(Mention(**source, mention_id=stable_id("mention", {**source, "local_id": entity.local_id}),
            local_id=entity.local_id, raw_name=entity.name, kind=entity.kind, roles=entity.roles,
            granularity=entity.granularity, attributes=entity.attributes, aliases=entity.aliases,
            scope=scope or {}, evidence=spans))
    facts = []
    for raw in payload.facts:
        data = raw.model_dump()
        spans, missing = _spans(raw.evidence, raw_text, chunk_id)
        unresolved_spans += [{"local_id": raw.local_id, **item} for item in missing]
        data["evidence"] = spans
        facts.append(RawFact.model_validate(data))
    # Alias claims are retained verbatim as source-local claims. They are not
    # dictionary entries and require their own exact defining span validation.
    aliases = []
    local_ids = {e.local_id for e in payload.entities}
    for assertion in payload.alias_assertions:
        if set(assertion) != {"left", "right", "evidence"} or assertion["left"] not in local_ids or assertion["right"] not in local_ids:
            raise ValueError("Alias assertion must refer to two existing local records")
        spans, missing = _spans(assertion["evidence"], raw_text, chunk_id)
        if not spans or missing:
            raise ValueError("Alias definition needs an unambiguous exact source span")
        aliases.append({**assertion, "evidence": [s.model_dump(mode="json") for s in spans],
                        "status": "unverified_source_claim"})
    response_hash = hashlib.sha256(response_text.encode()).hexdigest()
    signature = {**source, "prompt_hash": prompt_hash, "model_profile_hash": model_profile_hash,
                 "response_hash": response_hash}
    return RawBatch(corpus_id=corpus_id, **source,
        chunk_hash=hashlib.sha256(raw_text.encode()).hexdigest(), raw_text=raw_text,
        extraction_id=stable_id("extraction", signature), status="complete" if mentions or facts else "confirmed_empty",
        finish_reason=finish_reason, prompt_hash=prompt_hash, model_profile_hash=model_profile_hash,
        response_hash=response_hash, mentions=mentions, facts=facts,
        metadata={"adapter": "live-sidecar-1", "unlocated_evidence": unresolved_spans,
                  "alias_assertions": aliases, "extra_identity_calls": 0})


def schema_hint(registry):
    """Small schema/role hint. It contains no list of canonical names or IDs."""
    return {"output_schema": ExtractionPayload.model_json_schema(),
            "roles": [r.model_dump(mode="json") for r in registry.roles],
            "instructions": ["Retain exact surface names and original values/units.",
                "Use only local entity IDs in fact roles and observation.metric.",
                "Unknown attributes remain absent; no identity judgment is requested."]}
