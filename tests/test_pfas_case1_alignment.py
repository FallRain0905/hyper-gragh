import copy

import pytest

from scripts.align_pfas_case1 import GROUPS, validate_keywords, label_packet, validate_labels, validate_facts, vector, case1_metrics


def packet():
    return label_packet({"question_id": "Q", "question": "PFOA removal?", "answerable": True,
                         "reference_answer": "50% removal", "required_key_points": ["50% removal"]},
                        ["PFAS_001_CHK_001", "PFAS_001_CHK_002"],
                        {"PFAS_001_CHK_001": {"content": "PFOA removal was 50% after 60 minutes."},
                         "PFAS_001_CHK_002": {"content": "Defluorination was measured independently."}})


def test_main_five_and_true_f0():
    assert [v["code"] for v in GROUPS.values()] == ["B0", "B1", "B2", "F0", "F1"]
    assert GROUPS["normalized_final_no_rerank"]["cache"] == GROUPS["normalized_final"]["cache"] == "hyper_final"
    assert GROUPS["chem_prompt_hypergraph"]["adapter"] == "upstream_hyper_query"


@pytest.mark.parametrize("v", [{}, {"high_level_keywords": "PFOA", "low_level_keywords": []},
                              {"high_level_keywords": [], "low_level_keywords": []}])
def test_invalid_keywords(v):
    with pytest.raises(ValueError): validate_keywords(v)


def test_qrel_ids_and_source_partition():
    p = packet()
    sid = next(iter(p["RAW_SPAN_CATALOG"]))
    v = {"judgments": [{"chunk_id": p["chunk_ids"][0], "relevance_grade": 3, "span_ids": [sid], "negative_answer_found": False, "rationale": "direct result"},
                       {"chunk_id": p["chunk_ids"][1], "relevance_grade": 0, "span_ids": [], "negative_answer_found": False, "rationale": "different metric"}]}
    validate_labels(v, p)
    wrong = copy.deepcopy(v)
    wrong["judgments"][1].update(relevance_grade=2, span_ids=[sid])
    with pytest.raises(ValueError): validate_labels(wrong, p)
    wrong = copy.deepcopy(v)
    wrong["judgments"].pop()
    with pytest.raises(ValueError): validate_labels(wrong, p)


def test_atomic_fact_cannot_join_different_chunks():
    p = packet()
    ids = list(p["RAW_SPAN_CATALOG"])
    v = {"facts": [{"claim": "PFOA removal was 50%", "entity": "PFOA", "metric": "removal", "condition": "60 min",
                    "relation": "was", "value": "50", "unit": "%", "rubric_point_ids": [0], "span_ids": [ids[0]]}]}
    validate_facts(v, p)
    v["facts"][0]["span_ids"] = ids
    with pytest.raises(ValueError): validate_facts(v, p)


def test_case1_mrr_and_zero_idcg():
    r = case1_metrics([0] * 5 + [2], [2], 2, 5)
    assert r["MRR"] == pytest.approx(1 / 6) and r["Hit@5"] == 0
    assert case1_metrics([0], [0], 2, 5)["gNDCG@5"] == 0


@pytest.mark.parametrize("v", [[0] * 2560, [1] * 2559, [float("nan")] * 2560])
def test_bad_query_vectors(v):
    with pytest.raises(ValueError): vector(v)
