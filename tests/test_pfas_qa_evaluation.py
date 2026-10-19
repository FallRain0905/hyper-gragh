import pytest

from scripts.run_pfas_qa40 import evidence_context, validate_answer, validate_judge
from scripts import structured_graph_retrieval as s
import re


def test_empty_answer_and_mislabeled_refusal_never_complete():
    with pytest.raises(ValueError, match="Empty answer"):
        validate_answer({"answer": "", "citations": [], "abstained": False})
    with pytest.raises(ValueError, match="Explicit refusal"):
        validate_answer({"answer": "I don't know based on the retrieved evidence.", "citations": [], "abstained": False})


def test_good_cannot_hide_missing_or_hallucinated_claims():
    qa = {"required_key_points": ["One supported statement", "Second supported statement"]}
    value = {"quality_label": "GOOD", "good": True, "satisfactory_or_better": True,
             "key_point_coverage": .5, "covered_key_points": [qa["required_key_points"][0]],
             "missing_key_points": [qa["required_key_points"][1]], "hallucinated": False,
             "abstained": False, "citation_support_score": 1., "unsupported_claims_found": [],
             "rationale": "one point is missing"}
    with pytest.raises(ValueError, match="every scoring point"):
        validate_judge(value, qa, False)
    value.update(quality_label="SATISFACTORY", good=False, hallucinated=True)
    with pytest.raises(ValueError, match="hallucinated answer"):
        validate_judge(value, qa, False)


def test_pfAS_source_context_is_complete_and_not_gold_filtered(monkeypatch):
    chunks = {"PFAS_003_CHK_001": {"content": "Verbatim raw source that differs from a graph summary.", "source_doc_id": "PFAS_003"}}
    edge = {"source_id": "PFAS_003_CHK_001<SEP>PFAS_004_CHK_001"}
    monkeypatch.setattr(s, "CHUNK_ID_RE", re.compile(r"(?:PFAS|RFB)_\d+_CHK_\d+", re.I))
    assert s.source_chunk_ids(edge, chunks) == ["PFAS_003_CHK_001"]
    context = evidence_context([{"id": "PFAS_003_CHK_001", "supporting_relations": [{"description": "fallible hint"}]}], chunks)
    assert chunks["PFAS_003_CHK_001"]["content"] in context
    assert "verify against raw text" in context
