import copy
import pytest

from scripts.recover_pfas_case1_qrels import aliased_packet, resolve_aliases, retry_prompt
from tests.test_pfas_case1_alignment import packet


def example():
    original = packet()
    revised, aliases = aliased_packet(original)
    sid = next(iter(aliases))
    v = {"judgments": [{"chunk_id": original["chunk_ids"][0], "relevance_grade": 2, "span_ids": [sid],
                        "negative_answer_found": False, "rationale": "Substantial requested result"},
                       {"chunk_id": original["chunk_ids"][1], "relevance_grade": 0, "span_ids": [],
                        "negative_answer_found": False, "rationale": "Different metric"}]}
    return original, revised, aliases, v


def test_explicit_alias_preserves_fields_and_source():
    original, revised, aliases, v = example()
    before = copy.deepcopy(v)
    result = resolve_aliases(v, original, revised, aliases)
    assert v == before
    assert result["judgments"][0]["relevance_grade"] == 2
    assert result["judgments"][0]["span_ids"] == [next(iter(original["RAW_SPAN_CATALOG"]))]
    assert [r["rationale"] for r in result["judgments"]] == [r["rationale"] for r in v["judgments"]]


def test_unknown_alias_and_cross_chunk_rejected():
    original, revised, aliases, v = example()
    v["judgments"][0]["span_ids"] = ["S9999"]
    with pytest.raises(ValueError): resolve_aliases(v, original, revised, aliases)
    v["judgments"][0]["span_ids"] = [list(aliases)[-1]]
    with pytest.raises(ValueError): resolve_aliases(v, original, revised, aliases)


def test_missing_fields_not_synthesized():
    original, revised, aliases, v = example()
    del v["judgments"][1]["negative_answer_found"]
    with pytest.raises(ValueError): resolve_aliases(v, original, revised, aliases)
    text = retry_prompt(revised)
    assert text.rfind("OUTPUT JSON SCHEMA") > text.rfind("END INPUT DATA")
