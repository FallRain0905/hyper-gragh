import copy
import pytest

from scripts.recover_pfas_case1_facts import resolve_generation, resolve_review, generation_prompt
from scripts.recover_pfas_case1_qrels import aliased_packet
from tests.test_pfas_case1_alignment import packet


def fixture():
    p = packet()
    ap, aliases = aliased_packet(p)
    first = next(iter(aliases))
    gen = {"facts": [{"claim": "PFOA removal was 50%", "entity": "PFOA", "metric": "removal", "value": "50", "unit": "%",
                      "condition": "60 min", "relation": "was", "rubric_point_ids": [0], "span_ids": [first]}]}
    return p, ap, aliases, gen


def test_numeric_values_not_coerced():
    p, ap, aliases, gen = fixture()
    gen["facts"][0]["value"] = 50
    with pytest.raises(ValueError): resolve_generation(gen, p, ap, aliases)
    gen["facts"][0]["value"] = "50"
    del gen["facts"][0]["unit"]
    with pytest.raises(ValueError): resolve_generation(gen, p, ap, aliases)


def test_fact_review_cannot_switch_span_or_rewrite_value():
    p, ap, aliases, gen = fixture()
    before = copy.deepcopy(gen)
    resolved = resolve_generation(gen, p, ap, aliases)
    assert gen == before and resolved["facts"][0]["value"] == "50"
    rv = {"fact_checks": [{"fact_id": 0, "atomic": True, "supported": True, "numeric_unit_binding_valid": True,
                           "question_relevant": True, "support_span_ids": [next(iter(aliases))], "reason": "Exact bound result"}]}
    result = resolve_review(rv, resolved["facts"], gen["facts"], p, aliases)
    assert result["fact_checks"][0]["support_span_ids"] == resolved["facts"][0]["span_ids"]
    rv["fact_checks"][0]["support_span_ids"] = [list(aliases)[-1]]
    with pytest.raises(ValueError): resolve_review(rv, resolved["facts"], gen["facts"], p, aliases)


def test_fact_schema_is_at_end_and_requires_string_values():
    _, ap, _, _ = fixture()
    prompt = generation_prompt(ap)
    assert prompt.rfind("OUTPUT JSON SCHEMA") > prompt.rfind("END INPUT DATA")
    assert '"value": {"type": ["string", "null"]}' in prompt
