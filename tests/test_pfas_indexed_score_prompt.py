import json
from scripts.recover_pfas_qa40_indexed_scores import indexed_prompt
from scripts.audit_pfas_qa40_scores import RULES, source_span_catalog


def test_indexed_prompt_keeps_semantic_rules_and_has_one_unambiguous_format():
    data = {"actual_answer": "A supported answer.", "rubric": [{"point_id": 0, "point": "A fact."}],
            "raw_retrieved_chunks": [{"rank": 1, "content": "Actual retrieved source, dose 10 mg L@1."}]}
    prompt = indexed_prompt(data)
    assert prompt.startswith(RULES.split("Return exactly one JSON object with this schema:")[0])
    assert '"source_span_id": "exact catalog ID"' in prompt
    assert '"source_quote": ""' in prompt
    assert '"source_quote":"exactrawsourcespan"' not in prompt.replace(" ", "")
    assert "10 mg L@1" in prompt
    assert list(source_span_catalog(data))[0] in prompt
    assert "original_hypergraph" not in prompt
