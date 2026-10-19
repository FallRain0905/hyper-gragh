import copy

import pytest

from scripts.recover_pfas_metric_scope_targets import retained_targets, merge_review
from scripts.adjudicate_pfas_shared_retrieval import validate_review


def example():
    sid = "R1:0:16:source"
    a = {"point_checks": [{"point_id": 0, "support": "full", "span_ids": [sid], "reason": "Exact parent measurement."}],
         "context_relevant": True, "context_span_ids": [sid], "negative_query_answer_found": False,
         "negative_answer_span_ids": [], "binding_issues": [], "rationale": "Supported measurement."}
    rows = {"pool/q__a": {"question_id": "q", "chunk_ids": ["a"], "annotation": copy.deepcopy(a)},
            "sets/s": {"question_id": "q", "chunk_ids": ["a"], "annotation": copy.deepcopy(a)}}
    targets = [{"target_id": key, "aliases": [key], "disputed_point_ids": [0],
                "allowed_span_ids": [sid], "prior_annotation": copy.deepcopy(a)} for key in rows]
    packet = {"question_id": "q", "answerable": True, "rubric": [{"point_id": 0, "point": "Parent measurement."}],
              "targets": targets, "RAW_SPAN_CATALOG": {sid: {"chunk_id": "a", "rank": 1, "start": 0, "end": 16, "exact_raw_text": "PFOA degradation"}}}
    decisions = [{"target_id": t["target_id"], "point_decisions": [{"point_id": 0, "support": "full", "span_ids": [sid],
                  "reason": "Raw parent measurement is explicit.", "binding_issue_reason": ""}], "context_relevant": True,
                  "context_span_ids": [sid], "rationale": "Source supports the parent-outcome component."} for t in targets]
    value = {"target_decisions": decisions, "source_ambiguity_requires_manual": False, "source_ambiguity_reason": ""}
    return packet, rows, value


def test_misspelled_target_is_not_guessed_and_valid_subrecord_is_retained():
    packet, rows, original = example()
    original["target_decisions"][1]["target_id"] = "sets/s_typo"
    retained, missing, issues = retained_targets(packet, original, rows)
    assert list(retained) == ["pool/q__a"]
    assert [t["target_id"] for t in missing] == ["sets/s"]
    fresh = copy.deepcopy(original)
    fresh["target_decisions"] = [copy.deepcopy(original["target_decisions"][1])]
    fresh["target_decisions"][0]["target_id"] = "sets/s"
    merged = merge_review(packet, original, retained, fresh)
    validate_review(merged, packet, rows)
    assert merged["target_decisions"][0] == original["target_decisions"][0]
    assert original["target_decisions"][1]["target_id"] == "sets/s_typo"


def test_internally_conflicting_subrecord_is_requested_again_without_auto_fix():
    packet, rows, original = example()
    original["target_decisions"][0]["context_relevant"] = False
    original["target_decisions"][0]["context_span_ids"] = []
    retained, missing, _ = retained_targets(packet, original, rows)
    assert "pool/q__a" not in retained
    assert "pool/q__a" in [t["target_id"] for t in missing]
    assert original["target_decisions"][0]["context_relevant"] is False


def test_ambiguous_duplicate_target_is_never_silently_selected():
    packet, rows, original = example()
    original["target_decisions"].append(copy.deepcopy(original["target_decisions"][0]))
    retained, missing, _ = retained_targets(packet, original, rows)
    assert "pool/q__a" not in retained
    assert "pool/q__a" in [t["target_id"] for t in missing]


def test_missing_correct_identity_cannot_be_filled_by_typo_or_reason_drop():
    packet, _, original = example()
    retained = {"pool/q__a": original["target_decisions"][0]}
    fresh = copy.deepcopy(original)
    fresh["target_decisions"] = [fresh["target_decisions"][1]]
    fresh["target_decisions"][0]["target_id"] = "sets/s_typo"
    with pytest.raises(ValueError, match="exactly the failed target"):
        merge_review(packet, original, retained, fresh)
