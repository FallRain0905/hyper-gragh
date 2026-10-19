import json

import pytest

from scripts.recover_pfas_shared_retrieval import complete_json_without_fence_repair, checkpoint_row, retry_prompt
from scripts.evaluate_pfas_shared_retrieval import annotation_packet, validate_annotation


def test_unclosed_markdown_fence_can_only_unwrap_complete_data():
    raw = '```json\n{"point_checks":[],"number":"25 °C","target":"PFOA"}'
    parsed, method = complete_json_without_fence_repair(raw, "stop")
    assert parsed == {"point_checks": [], "number": "25 °C", "target": "PFOA"}
    assert method == "opening_markdown_fence_only"
    assert json.loads(raw.split("\n", 1)[1]) == parsed


@pytest.mark.parametrize("raw,finish", [
    ('```json\n{"target":"PFOA"}', "length"),
    ('```json\n{"target":"PFOA"', "stop"),
    ('```json\n{"target":"PFOA"}\nExplanation after JSON', "stop"),
    ('```json\n{"target":"PFOA"}{"other":1}', "stop"),
    ('Here is JSON:\n{"target":"PFOA"}', "stop"),
    ('```json\n[]', "stop"),
    ('', "stop"),
])
def test_incomplete_or_extra_data_never_recovered(raw, finish):
    with pytest.raises(ValueError):
        complete_json_without_fence_repair(raw, finish)


def test_negative_root_explains_scope_without_changing_source_or_question():
    q = {"question_id": "q", "question": "Exact PFOA result at 25 °C?", "answerable": False,
         "reference_answer": "Exact result absent.", "required_key_points": ["Do not invent a value."]}
    packet = annotation_packet(q, ["chunk"], {"chunk": {"content": "PFOA was tested at a different temperature."}})
    prompt = retry_prompt(packet, "A local packet cannot establish corpus-wide absence")
    assert "No earlier assistant response is included" in prompt
    assert "NOT positive facts" in prompt
    assert json.loads(prompt.split("\nINPUT:\n", 1)[1]) == packet
    sid = next(iter(packet["RAW_SPAN_CATALOG"]))
    invalid = {"point_checks": [{"point_id": 0, "support": "full", "span_ids": [sid], "reason": "No exact value."}],
               "context_relevant": True, "context_span_ids": [sid], "negative_query_answer_found": False,
               "negative_answer_span_ids": [], "binding_issues": [], "rationale": "No exact result."}
    with pytest.raises(ValueError, match="corpus-wide"):
        checkpoint_row(packet, {}, invalid, "pool", {})
    # Recovery must ask the model again rather than silently replacing full by none.
    assert invalid["point_checks"][0]["support"] == "full"
