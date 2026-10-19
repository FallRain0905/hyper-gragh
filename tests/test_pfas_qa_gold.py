import copy

import pytest

from scripts.pfas_qa_common import parse_json_response
from scripts.verify_pfas_qa40 import validate_audit, validate_supported


def reference():
    quote = "The catalyst removed 90% of PFOA after two hours under irradiation."
    chunks = {"PFAS_001_CHK_001": {"content": quote}}
    value = {"decision": "ACCEPT", "answerable": True,
             "question": "What PFOA removal was reported after two hours?",
             "reference_answer": "PFOA removal was 90% after two hours of irradiation.",
             "rationale": "Each value and condition belongs to the same source experiment.",
             "unsupported_claims": ["Complete carbon mineralization was not measured."],
             "point_support": [
                 {"point": "PFOA removal reached 90%.", "evidence": [{"chunk_id": "PFAS_001_CHK_001", "quote": quote}]},
                 {"point": "Treatment duration was two hours.", "evidence": [{"chunk_id": "PFAS_001_CHK_001", "quote": quote}]},
             ]}
    return value, chunks


def test_valid_json_in_truncated_response_is_rejected():
    with pytest.raises(ValueError, match="Incomplete"):
        parse_json_response('{"answer":"plausible but truncated"}', "length")


def test_wrong_source_or_changed_numeric_quote_cannot_pass():
    value, chunks = reference()
    validate_supported(value, chunks, chunks)
    changed = copy.deepcopy(value)
    changed["point_support"][0]["evidence"][0]["quote"] = chunks["PFAS_001_CHK_001"]["content"].replace("90%", "99%")
    with pytest.raises(ValueError, match="exact raw-source"):
        validate_supported(changed, chunks, chunks)
    with pytest.raises(ValueError, match="outside supplied"):
        validate_supported(value, chunks, {"PFAS_002_CHK_001"})


def test_independent_reviewer_cannot_accept_with_unsupported_point():
    value, _ = reference()
    points = [p["point"] for p in value["point_support"]]
    audit = {"accepted": True, "reference_supported": True, "question_answerable": True,
             "numeric_unit_binding_valid": True, "issues": [],
             "point_checks": [{"point": p, "supported": True, "reason": "Source explicitly states it."} for p in points]}
    validate_audit(audit, points)
    audit["point_checks"][0]["supported"] = False
    with pytest.raises(ValueError, match="Inconsistent acceptance"):
        validate_audit(audit, points)


def test_independent_review_must_cover_all_rubric_points():
    audit = {"point_checks": [{"point": "one point", "supported": True, "reason": "yes"}]}
    with pytest.raises(ValueError, match="every scoring point"):
        validate_audit(audit, ["one point", "another point"])
