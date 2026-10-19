import copy

import pytest

from scripts.adjudicate_pfas_shared_retrieval import (
    review_packet, validate_review, patched_annotation, remap_spans, source_conflicts,
)
from scripts.evaluate_pfas_shared_retrieval import annotation_packet


def example():
    q = {"question_id": "q", "question": "PFOA measurement and conditions?", "answerable": True,
         "reference_answer": "95% PFOA removal at a specified condition.",
         "required_key_points": ["Measurement with its complete condition binding.", "Another required detail."]}
    chunks = {"a": {"content": "PFOA removal was 95%. Conditions were not specified here."},
              "b": {"content": "Other PFAS background, without a specific measurement."}}
    def annotation(ids, support):
        packet = annotation_packet(q, ids, chunks)
        sid = next(iter(packet["RAW_SPAN_CATALOG"]))
        return {"point_checks": [{"point_id": 0, "support": support, "span_ids": [sid] if support != "none" else [], "reason": "Source interpretation."},
                                 {"point_id": 1, "support": "none", "span_ids": [], "reason": "Not established."}],
                "context_relevant": support != "none", "context_span_ids": [sid] if support != "none" else [],
                "negative_query_answer_found": False, "negative_answer_span_ids": [], "binding_issues": [], "rationale": "Source interpretation."}
    rows = {"pool/q__a": {"question_id": "q", "chunk_ids": ["a"], "annotation": annotation(["a"], "full")},
            "pool/q__b": {"question_id": "q", "chunk_ids": ["b"], "annotation": annotation(["b"], "none")},
            "sets/s": {"question_id": "q", "chunk_ids": ["a", "b"], "annotation": annotation(["a", "b"], "partial")}}
    packet = review_packet(q, source_conflicts(rows), rows, chunks)
    value = {"target_decisions": [], "source_ambiguity_requires_manual": False, "source_ambiguity_reason": ""}
    for t in packet["targets"]:
        a_span = next(sid for sid in t["allowed_span_ids"] if packet["RAW_SPAN_CATALOG"][sid]["chunk_id"] == "a")
        value["target_decisions"].append({"target_id": t["target_id"],
            "point_decisions": [{"point_id": 0, "support": "partial", "span_ids": [a_span],
                                 "reason": "The 95% measurement is given but its complete condition is absent.", "binding_issue_reason": ""}],
            "context_relevant": True, "context_span_ids": [a_span], "rationale": "Useful partial evidence, not the complete composite point."})
    return q, chunks, rows, packet, value


def test_source_review_can_correct_single_label_without_forcing_joint_full():
    _, _, rows, packet, value = example()
    validate_review(value, packet, rows)
    assert rows["pool/q__a"]["annotation"]["point_checks"][0]["support"] == "full"
    for t, d in zip(packet["targets"], value["target_decisions"]):
        patched = patched_annotation(t, d)
        assert patched["point_checks"][1] == t["prior_annotation"]["point_checks"][1]
        assert patched["point_checks"][0]["support"] == "partial"


def test_joint_cannot_stay_partial_while_member_stays_full_without_explicit_ambiguity():
    _, _, rows, packet, value = example()
    next(d for d in value["target_decisions"] if d["target_id"].startswith("pool/"))["point_decisions"][0]["support"] = "full"
    with pytest.raises(ValueError, match="single/joint"):
        validate_review(value, packet, rows)


def test_visible_but_outside_target_source_cannot_upgrade_a_single_chunk():
    _, _, rows, packet, value = example()
    d = next(d for d in value["target_decisions"] if d["target_id"].startswith("pool/"))
    b_span = next(sid for sid, s in packet["RAW_SPAN_CATALOG"].items() if s["chunk_id"] == "b")
    d["point_decisions"][0]["span_ids"] = [b_span]
    with pytest.raises(ValueError, match="wrong-packet"):
        validate_review(value, packet, rows)


def test_only_requested_disputed_point_partition_can_change():
    _, _, rows, packet, value = example()
    value["target_decisions"][0]["point_decisions"][0]["point_id"] = True
    with pytest.raises(ValueError, match="disputed-point"):
        validate_review(value, packet, rows)
    value["target_decisions"] = []
    with pytest.raises(ValueError, match="Every target"):
        validate_review(value, packet, rows)


def test_exact_span_remapping_cannot_change_condition_or_numerical_bytes():
    q, chunks, rows, packet, _ = example()
    original = annotation_packet(q, ["a"], chunks)
    selected = rows["pool/q__a"]["annotation"]
    mapped, _ = remap_spans(selected, original["RAW_SPAN_CATALOG"], packet["RAW_SPAN_CATALOG"])
    roundtrip, _ = remap_spans(mapped, packet["RAW_SPAN_CATALOG"], original["RAW_SPAN_CATALOG"])
    assert roundtrip == selected
    changed = copy.deepcopy(original["RAW_SPAN_CATALOG"])
    next(iter(changed.values()))["exact_raw_text"] = "PFOA defluorination was 96%."
    with pytest.raises(ValueError, match="exact target packet"):
        remap_spans(mapped, packet["RAW_SPAN_CATALOG"], changed)
