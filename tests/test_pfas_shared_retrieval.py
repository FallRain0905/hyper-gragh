import copy
import math

import pytest

from scripts.evaluate_pfas_shared_retrieval import (
    annotation_packet, derive_grade, ranking_metrics, validate_annotation,
    validate_checkpoint,
)
from scripts.pfas_qa_common import digest


def example(answerable=True):
    question = {"question_id": "PFAS_Q01", "question": "Which target and outcome?",
                "answerable": answerable, "reference_answer": "PFOA; 95% removal.",
                "required_key_points": ["PFOA target", "95% removal, not defluorination"]}
    chunks = {"PFAS_001_CHK_001": {"content": "PFOA removal was 95%. This is not a defluorination measurement."}}
    packet = annotation_packet(question, list(chunks), chunks)
    sid = next(iter(packet["RAW_SPAN_CATALOG"]))
    value = {"point_checks": [
        {"point_id": 0, "support": "full", "span_ids": [sid], "reason": "Target explicitly named."},
        {"point_id": 1, "support": "full", "span_ids": [sid], "reason": "Removal explicitly measured."}],
        "context_relevant": True, "context_span_ids": [sid],
        "negative_query_answer_found": False, "negative_answer_span_ids": [],
        "binding_issues": [], "rationale": "Both facts are bound to the same raw measurement."}
    return packet, value


def test_source_ids_roundtrip_exact_offsets_and_checkpoint_binding():
    packet, value = example()
    validate_annotation(value, packet)
    for span in packet["RAW_SPAN_CATALOG"].values():
        raw = "PFOA removal was 95%. This is not a defluorination measurement."
        assert raw[span["start"]:span["end"]] == span["exact_raw_text"]
    protocol = {"rules": "frozen"}
    row = {"question_id": packet["question_id"], "chunk_ids": ["PFAS_001_CHK_001"],
           "signature": digest({"packet": packet, "protocol": digest(protocol)}),
           "annotation": value, "span_evidence": packet["RAW_SPAN_CATALOG"]}
    validate_checkpoint(row, packet, protocol)
    row["span_evidence"] = copy.deepcopy(row["span_evidence"])
    next(iter(row["span_evidence"].values()))["exact_raw_text"] = "PFOA defluorination was 95%."
    with pytest.raises(ValueError, match="exact raw spans"):
        validate_checkpoint(row, packet, protocol)


def test_identical_evidence_sets_are_presented_without_retrieval_order():
    question = {"question_id": "q", "question": "PFOA?", "answerable": True,
                "reference_answer": "PFOA", "required_key_points": ["PFOA"]}
    chunks = {"b": {"content": "Second raw source."}, "a": {"content": "First raw source."}}
    assert annotation_packet(question, ["a", "b"], chunks) == annotation_packet(question, ["b", "a"], chunks)


@pytest.mark.parametrize("mutation", [
    lambda v: v["point_checks"][0].update(span_ids=["R1:invented"]),
    lambda v: v["point_checks"][0].update(span_ids=[]),
    lambda v: v["point_checks"][0].update(point_id=False),
    lambda v: v["point_checks"].reverse(),
    lambda v: v.update(context_relevant=False, context_span_ids=[]),
    lambda v: v.update(binding_issues=[{"point_id": 0, "reason": "Wrong target."}]),
    lambda v: v.update(binding_issues=["not an object"]),
    lambda v: v.update(negative_query_answer_found=True, negative_answer_span_ids=v["context_span_ids"]),
])
def test_incomplete_wrong_source_or_inconsistent_binding_rejected(mutation):
    packet, value = example()
    mutation(value)
    with pytest.raises(ValueError):
        validate_annotation(value, packet)


def test_negative_packet_cannot_establish_corpus_absence():
    packet, value = example(False)
    with pytest.raises(ValueError, match="corpus-wide"):
        validate_annotation(value, packet)
    for p in value["point_checks"]:
        p.update(support="none", span_ids=[], reason="A local packet cannot establish corpus absence.")
    validate_annotation(value, packet)
    value.update(negative_query_answer_found=True, negative_answer_span_ids=value["context_span_ids"],
                 context_relevant=False, context_span_ids=[])
    with pytest.raises(ValueError, match="context-relevant"):
        validate_annotation(value, packet)


def test_grades_distinguish_partial_point_from_complete_point():
    _, value = example()
    assert derive_grade(value, True) == 3
    value["point_checks"][1]["support"] = "partial"
    assert derive_grade(value, True) == 2
    value["point_checks"][0]["support"] = "partial"
    assert derive_grade(value, True) == 1
    for p in value["point_checks"]:
        p["support"] = "none"
    value["context_relevant"] = False
    assert derive_grade(value, True) == 0
    value["point_checks"] = []
    with pytest.raises(ValueError, match="empty rubric"):
        derive_grade(value, True)


def test_shared_ideal_and_pooled_recall_have_common_denominators():
    grades = {"a": 3, "b": 2, "c": 1, "d": 0}
    a = ranking_metrics(["a", "c"], grades)
    b = ranking_metrics(["b", "a"], grades)
    ideal = 7 + 3 / math.log2(3) + 1 / math.log2(4)
    assert a["shared_IDCG@5"] == pytest.approx(ideal)
    assert b["shared_IDCG@5"] == pytest.approx(ideal)
    assert a["P@5_grade2"] == .2
    assert a["pooled_recall@5_grade2"] == .5
    assert b["pooled_recall@5_grade2"] == 1
    assert a["gNDCG@5_shared_pool"] == pytest.approx((7 + 1 / math.log2(3)) / ideal)
    assert ranking_metrics(["d", "b"], grades)["MRR@5_grade2"] == .5


def test_unjudged_is_not_silently_irrelevant_and_zero_ideal_is_na():
    with pytest.raises(ValueError, match="Unjudged"):
        ranking_metrics(["unjudged"], {"a": 0})
    empty = ranking_metrics([], {"a": 0})
    assert empty["pooled_recall@5_grade2"] is None
    assert empty["gNDCG@5_shared_pool"] is None
    assert empty["P@5_grade2"] == 0
    assert ranking_metrics(["a", "a", "b"], {"a": 2, "b": 3})["P@5_grade2"] == .4


@pytest.mark.parametrize("grades", [{"a": True}, {"a": 4}, {"a": -1}])
def test_metric_grade_domain_is_strict(grades):
    with pytest.raises(ValueError, match="integer relevance grades"):
        ranking_metrics(["a"], grades)
