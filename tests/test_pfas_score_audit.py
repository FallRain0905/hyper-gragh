import copy
import asyncio
import json

import pytest
from scripts.audit_pfas_qa40_scores import validate, review_fields, differs, exact_whitespace_span, restore_exact_quotes, quote_validation_feedback
from scripts.pfas_qa_common import QAClient, digest, write_json
from scripts.audit_pfas_qa40_scores import source_span_catalog, resolve_explicit_source_spans, prepare_review
from scripts.audit_pfas_qa40_scores import require_explicit_source_selections


def example():
    answer = "The carboxylates were mineralized using low-temperature DMSO/NaOH."
    data = {"actual_answer": answer, "rubric": [{"point_id": 0, "point": "Subsequent low-temperature mineralization."}],
            "raw_retrieved_chunks": [{"rank": 1, "content": answer}], "answerable": True, "answer_abstained": False}
    review = {"point_checks": [{"point_id": 0, "covered": True, "answer_quote": "low-temperature DMSO/NaOH", "reason": "explicit in answer"}],
              "claim_checks": [{"answer_quote": answer, "supported": True, "source_quote": answer, "evidence_rank": 1, "reason": "raw evidence explicitly supports it"}],
              "hallucinated": False, "unsupported_claims_found": [], "quality_label": "GOOD", "citation_support_score": 1., "rationale": "The full result is supported."}
    return data, review


def test_coverage_requires_a_real_answer_span():
    data, review = example()
    validate(review, data)
    review["point_checks"][0]["answer_quote"] = "invented answer wording"
    with pytest.raises(ValueError, match="exact answer span"):
        validate(review, data)


def test_gold_cannot_be_used_as_retrieved_support():
    data, review = example()
    review["claim_checks"][0]["source_quote"] = "A fact in gold but not retrieved."
    with pytest.raises(ValueError, match="raw retrieved span"):
        validate(review, data)


def test_missing_detail_is_distinct_from_hallucination():
    data, review = example()
    review["point_checks"][0].update(covered=False, answer_quote="", reason="not covered")
    review["quality_label"] = "SATISFACTORY"
    validate(review, data)
    qa = {"required_key_points": [data["rubric"][0]["point"]]}
    fields = review_fields(review, qa)
    assert fields["key_point_coverage"] == 0
    assert fields["hallucinated"] is False


def test_quality_and_point_disagreement_triggers_adjudication():
    data, review = example()
    qa = {"required_key_points": [data["rubric"][0]["point"]]}
    original = {"quality_label": "POOR", "hallucinated": True, "covered_key_points": []}
    assert differs(original, review, qa)


def test_unsupported_material_claim_cannot_be_marked_grounded():
    data, review = example()
    review["claim_checks"][0]["supported"] = False
    with pytest.raises(ValueError, match="hallucination flag"):
        validate(review, data)


def test_hallucination_cannot_be_based_only_on_missing_points():
    data, review = example()
    review.update(hallucinated=True, quality_label="POOR", unsupported_claims_found=["a missing step"])
    with pytest.raises(ValueError, match="identified unsupported answer claim"):
        validate(review, data)


def test_format_recovery_copies_only_unique_raw_span():
    raw = "The carboxylates were\nmineralized using low-temperature DMSO/NaOH."
    quote = "carboxylates were mineralized using low-temperature DMSO/NaOH"
    recovered, start, end = exact_whitespace_span(quote, raw)
    assert recovered == raw[start:end]
    assert "\n" in recovered
    assert exact_whitespace_span("95 %", "95 % and 95%") is not None  # exact quote already exists
    assert exact_whitespace_span("95  %", "95 % and 95%") is None


@pytest.mark.parametrize("quote,raw", [("95%", "96%"), ("PFOA", "PFOS"), ("5 mg/L", "5 mg L-1"), ("DMSO-NaOH", "DMSO/NaOH")])
def test_format_recovery_cannot_change_scientific_identity(quote, raw):
    assert exact_whitespace_span(quote, raw) is None


def test_recovered_quote_keeps_original_and_strict_grounding():
    data, review = example()
    data["raw_retrieved_chunks"][0]["content"] = data["actual_answer"].replace("were mineralized", "were\nmineralized")
    restored = restore_exact_quotes(review, data)
    validate(restored, data)
    assert restored["quote_format_recovery"][0]["original_model_quote"] == review["claim_checks"][0]["source_quote"]
    assert review["claim_checks"][0]["source_quote"] not in data["raw_retrieved_chunks"][0]["content"]
    review["claim_checks"][0]["evidence_rank"] = 2
    with pytest.raises(ValueError, match="raw retrieved span"):
        validate(restore_exact_quotes(review, data), data)


def test_format_recovery_cannot_supply_missing_scoring_summary():
    data, review = example()
    del review["hallucinated"]
    with pytest.raises(ValueError, match="Grounding summary missing"):
        validate(restore_exact_quotes(review, data), data)


def test_offline_revalidation_preserves_failed_response_and_uses_no_request(tmp_path):
    data, review = example()
    data["raw_retrieved_chunks"][0]["content"] = data["actual_answer"].replace("were mineralized", "were\nmineralized")
    client = object.__new__(QAClient)
    client.output = tmp_path
    client.prompt_cache = tmp_path / "calls"
    client.prompt_cache.mkdir()
    prompt = "frozen scoring request"
    signature = digest({"prompt": prompt, "role": "judge", "model": "deepseek-ai/DeepSeek-V4-Flash", "temperature": 0,
                        "reasoning_effort": "low", "protocol": "pfas-qa-strict-v1"})
    attempt = client.prompt_cache / (signature + ".attempt1.123.json")
    write_json(attempt, {"signature": signature, "status": "failed", "content": json.dumps(review), "finish_reason": "stop"})
    before = attempt.read_bytes()
    result = asyncio.run(client.json(prompt, role="judge", validator=lambda v: validate(v, data),
                               response_transform=lambda v: restore_exact_quotes(v, data), recover_attempts=True))
    assert result["quote_format_recovery"]
    assert attempt.read_bytes() == before
    assert json.loads((tmp_path / "validation_recovery.jsonl").read_text())["new_api_requests"] == 0
    assert not (tmp_path / "request_audit.jsonl").exists()


def test_retry_feedback_preserves_corrupt_raw_units_and_cannot_validate_model_quote():
    data, review = example()
    data["raw_retrieved_chunks"][0]["content"] = "A relatively low adsorbent loading (10 mg L@1) removed all anionic PFASs."
    review["claim_checks"][0]["source_quote"] = "A relatively low adsorbent loading (10 mg L-1) removed all anionic PFASs."
    before = copy.deepcopy(review)
    feedback = quote_validation_feedback(review, data)
    assert "10 mg L@1" in feedback
    assert "Candidate context is not proof" in feedback
    assert review == before
    with pytest.raises(ValueError, match="raw retrieved span"):
        validate(review, data)


def test_retry_feedback_uses_only_retrieved_context():
    data, review = example()
    data["reference_source_quotes_NOT_retrieved_evidence"] = [{"quote": "GOLD ONLY SECRET FACT"}]
    review["claim_checks"][0]["source_quote"] = "invented different source"
    assert "GOLD ONLY SECRET FACT" not in quote_validation_feedback(review, data)


def test_explicit_source_id_copies_raw_text_and_preserves_model_selection():
    data, review = example()
    raw = data["actual_answer"] + "\nReported catalyst loading (10 mg L@1)."
    data["raw_retrieved_chunks"][0]["content"] = raw
    span_id = next(iter(source_span_catalog(data)))
    review["claim_checks"][0].update(source_quote="", source_span_id=span_id)
    prepared = prepare_review(review, data)
    validate(prepared, data)
    assert prepared["claim_checks"][0]["source_quote"] == raw
    assert prepared["explicit_source_selection"][0]["model_source_quote"] == ""
    assert review["claim_checks"][0]["source_quote"] == ""


@pytest.mark.parametrize("bad", ["unknown_id", "wrong_rank", "changed_quote", "other_packet"])
def test_source_selection_cannot_infer_or_repair_a_scientific_quote(bad):
    data, review = example()
    span_id = next(iter(source_span_catalog(data)))
    claim = review["claim_checks"][0]
    claim.update(source_quote="", source_span_id=span_id)
    if bad == "unknown_id": claim["source_span_id"] = "invented"
    if bad == "wrong_rank": claim["evidence_rank"] = 2
    if bad == "changed_quote": claim["source_quote"] = "scientifically changed source text"
    if bad == "other_packet": data["raw_retrieved_chunks"][0]["content"] += " A different raw source."
    with pytest.raises(ValueError):
        resolve_explicit_source_spans(review, data)


def test_new_response_must_explicitly_select_a_raw_span():
    data, review = example()
    with pytest.raises(ValueError, match="NEW response"):
        require_explicit_source_selections(review)
    review["claim_checks"][0].update(source_span_id=next(iter(source_span_catalog(data))), source_quote="")
    resolved = prepare_review(review, data)
    validate(resolved, data)
    require_explicit_source_selections(resolved)


def test_fresh_format_guard_does_not_reject_or_repeat_a_valid_cached_call(tmp_path):
    data, review = example()
    client = object.__new__(QAClient)
    client.output = tmp_path
    client.prompt_cache = tmp_path / "calls"
    client.prompt_cache.mkdir()
    prompt = "accepted review before source ID extension"
    signature = digest({"prompt": prompt, "role": "judge", "model": "deepseek-ai/DeepSeek-V4-Flash", "temperature": 0,
                        "reasoning_effort": "low", "protocol": "pfas-qa-strict-v1"})
    path = client.prompt_cache / (signature + ".json")
    write_json(path, {"signature": signature, "status": "ok", "content": json.dumps(review), "finish_reason": "stop"})
    before = path.read_bytes()
    result = asyncio.run(client.json(prompt, role="judge", validator=lambda v: validate(v, data), fresh_validator=require_explicit_source_selections))
    assert result == review
    assert path.read_bytes() == before
