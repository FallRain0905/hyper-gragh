"""Contract tests for the offline-normalization boundary records."""

from __future__ import annotations

import hashlib

import pytest
from pydantic import ValidationError

from hyperche.normalization_v2.contracts import (
    SCHEMA_VERSION,
    RawBatch,
    RawFact,
    locate_evidence,
    validate_evidence,
    validate_source_target,
    validate_strategy_config,
)


def _batch(**overrides):
    text = "BaTiO3 removes PFOA with 90% defluorination."
    payload = {
        "corpus_id": "corpus",
        "doc_id": "doc1",
        "revision_hash": "a" * 64,
        "chunk_id": "doc1:chunk1",
        "chunk_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "raw_text": text,
        "extraction_id": "extraction:1",
        "status": "complete",
        "finish_reason": "stop",
        "prompt_hash": "prompt",
        "model_profile_hash": "profile",
        "response_hash": "response",
        "mentions": [
            {
                "mention_id": "mention:m1",
                "doc_id": "doc1",
                "revision_hash": "a" * 64,
                "chunk_id": "doc1:chunk1",
                "local_id": "m1",
                "raw_name": "BaTiO3",
                "kind": "material",
            },
            {
                "mention_id": "mention:m2",
                "doc_id": "doc1",
                "revision_hash": "a" * 64,
                "chunk_id": "doc1:chunk1",
                "local_id": "m2",
                "raw_name": "PFOA",
                "kind": "contaminant",
            },
        ],
        "facts": [
            {
                "local_id": "f1",
                "relation_type": "REMOVES",
                "roles": {"material": ["m1"], "target": ["m2"]},
            }
        ],
    }
    payload.update(overrides)
    return payload


# ---------------------------------------------------------------------------
# RawFact role structure
# ---------------------------------------------------------------------------


def test_raw_fact_roles_preserve_order_and_multiplicity():
    fact = RawFact(
        local_id="f1",
        relation_type="COMPARES",
        roles={"material": ["m2", "m1", "m2"], "target": ["m1"]},
    )
    assert fact.roles["material"] == ["m2", "m1", "m2"]
    assert fact.model_dump()["roles"]["material"] == ["m2", "m1", "m2"]


@pytest.mark.parametrize("roles", [{}, {"material": []}, {"": ["m1"]}, {"material": [""]}])
def test_raw_fact_roles_reject_empty_roles_or_members(roles):
    with pytest.raises(ValidationError):
        RawFact(local_id="f1", relation_type="REMOVES", roles=roles)


# ---------------------------------------------------------------------------
# Batch status, finish reasons, spans and local references
# ---------------------------------------------------------------------------


def test_successful_status_requires_explicit_finish_reason():
    for status in ("complete", "confirmed_empty"):
        with pytest.raises(ValidationError, match="finish_reason"):
            RawBatch(**_batch(status=status, finish_reason="length"))


def test_complete_and_confirmed_empty_payload_shapes():
    with pytest.raises(ValidationError, match="at least one"):
        RawBatch(**_batch(mentions=[], facts=[]))
    with pytest.raises(ValidationError, match="must not contain"):
        RawBatch(**_batch(status="confirmed_empty", finish_reason="stop"))
    empty = RawBatch(**_batch(status="confirmed_empty", finish_reason="stop", mentions=[], facts=[]))
    assert empty.mentions == []
    technical = RawBatch(**_batch(status="technical_failed", finish_reason="length"))
    assert technical.status == "technical_failed"


def test_evidence_spans_must_match_exact_source_text():
    text = "BaTiO3 removes PFOA."
    span = locate_evidence("PFOA", text, "chunk")
    assert (span.start, span.end, span.status) == (15, 19, "verified")
    with pytest.raises(ValueError, match="exactly match"):
        validate_evidence({"quote": "PFOa", "start": 15, "end": 19, "chunk_id": "chunk"}, text, "chunk")
    with pytest.raises(ValueError, match="beyond"):
        validate_evidence({"quote": "PFOA", "start": 90, "end": 94, "chunk_id": "chunk"}, text, "chunk")
    with pytest.raises(ValueError, match="different chunk"):
        validate_evidence(span, text, "other-chunk")


def test_ambiguous_evidence_requires_explicit_offsets():
    text = "PFOA and PFOA"
    with pytest.raises(ValueError, match="Ambiguous"):
        locate_evidence("PFOA", text, "chunk")
    second = locate_evidence("PFOA", text, "chunk", start=9, end=13)
    assert second.start == 9


def test_fact_local_references_must_exist():
    fact = _batch()["facts"][0]
    bad = dict(fact, roles={"material": ["missing"]})
    with pytest.raises(ValidationError, match="unknown"):
        RawBatch(**_batch(facts=[bad]))


def test_batch_rejects_mismatched_mention_origin_and_duplicate_ids():
    mention = _batch()["mentions"][0]
    with pytest.raises(ValidationError, match="origin"):
        RawBatch(**_batch(mentions=[dict(mention, chunk_id="other")]))
    with pytest.raises(ValidationError, match="Duplicate mention"):
        RawBatch(**_batch(mentions=[mention, dict(mention)]))


# ---------------------------------------------------------------------------
# Strategy routing: legacy absence and v2 online conflicts
# ---------------------------------------------------------------------------


def test_absent_strategy_preserves_legacy_semantics():
    summary = validate_strategy_config(None)
    assert summary["legacy"] is True
    assert summary["strategy"] is None

    old = validate_strategy_config({"enable_entity_normalization": True})
    assert old["legacy"] is True
    assert old["normalize_during_extraction"] is True
    assert old["strategy"] is None


@pytest.mark.parametrize(
    "config",
    [
        {"normalization_strategy": "registry_offline_v2", "normalize_during_extraction": True},
        {"normalization_strategy": "registry_offline_v2", "normalization_phase": "online"},
        {"normalization_strategy": "registry_offline_v2", "candidate_cap": 6},
        {"normalization_strategy": "registry_offline_v2", "efu_repair": True},
        {"normalization_strategy": "registry_offline_v2", "identity_candidate_embedding_calls": 1},
        {"normalization_strategy": "legacy_posthoc", "normalize_during_extraction": True},
        {"normalization_strategy": "not_a_strategy"},
    ],
)
def test_v2_rejects_online_or_contradictory_configuration(config):
    with pytest.raises(ValueError):
        validate_strategy_config(config)


def test_v2_offline_configuration_is_frozen():
    summary = validate_strategy_config(
        {"normalization_strategy": "registry_offline_v2", "normalization_phase": "posthoc"}
    )
    assert summary["legacy"] is False
    assert summary["strategy"] == "registry_offline_v2"
    assert summary["candidate_cap"] == 5
    assert summary["normalize_during_extraction"] is False
    assert summary["identity_candidate_embedding_calls"] == 0


def test_schema_version_is_pinned():
    assert SCHEMA_VERSION == "registry-offline-v2.1"
    with pytest.raises(ValidationError, match="schema_version"):
        RawBatch(**_batch(schema_version="registry-offline-v2.0"))


# ---------------------------------------------------------------------------
# Source / target guard
# ---------------------------------------------------------------------------


def test_source_and_target_must_not_overlap(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    with pytest.raises(ValueError, match="different"):
        validate_source_target(source, source)
    with pytest.raises(ValueError, match="inside the source"):
        validate_source_target(source, source / "out")
    target = tmp_path / "target"
    target.mkdir()
    (target / ".published").write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="accepted"):
        validate_source_target(source, target)
