import json

import pytest

from hyperche.normalization_v2.extraction import adapt_live_response


def adapt(value, text="PFOA is treated.", **kw):
    options = dict(finish_reason="stop", stream_complete=True, corpus_id="test", doc_id="d1",
                   revision_hash="r1", chunk_id="c1", raw_text=text, prompt_hash="p", model_profile_hash="m")
    options.update(kw)
    return adapt_live_response(json.dumps(value), **options)


def payload():
    return {"entities": [{"local_id": "e1", "name": "PFOA", "kind": "contaminant", "evidence": [{"quote": "PFOA"}]}], "facts": []}


def test_adapter_preserves_source_and_missing_clues_without_identity_call():
    b = adapt(payload())
    assert b.mentions[0].attributes == {}
    assert b.mentions[0].evidence[0].start == 0
    assert b.mentions[0].doc_id == "d1"
    assert b.metadata["extra_identity_calls"] == 0
    assert b == adapt(payload())


def test_ambiguous_span_is_not_assigned_first_occurrence():
    b = adapt(payload(), text="PFOA is treated; PFOA remains.")
    assert b.mentions[0].evidence == []
    assert b.metadata["unlocated_evidence"][0]["reason"] == "ambiguous_span"
    p = payload()
    p["entities"][0]["evidence"] = [{"quote": "PFOA", "start": 17, "end": 21}]
    assert adapt(p, text="PFOA is treated; PFOA remains.").mentions[0].evidence[0].start == 17


@pytest.mark.parametrize("kwargs", [{"finish_reason": "length"}, {"stream_complete": False}])
def test_failed_transport_never_becomes_confirmed_empty(kwargs):
    with pytest.raises(ValueError): adapt({"entities": [], "facts": []}, **kwargs)


def test_empty_full_response_is_explicit_and_foreign_references_reject():
    assert adapt({"entities": [], "facts": []}).status == "confirmed_empty"
    p = payload()
    p["facts"] = [{"local_id": "f1", "relation_type": "REMOVES", "roles": {"target": ["missing"]}}]
    with pytest.raises(ValueError): adapt(p)
    p = payload()
    p["entities"][0]["doc_id"] = "model-invented-doc"
    with pytest.raises(ValueError): adapt(p)


def test_fact_evidence_is_assigned_program_source_and_fake_quotes_rejected():
    p = payload()
    p["facts"] = [{"local_id": "f1", "relation_type": "TREATS", "roles": {"target": ["e1"]},
                   "evidence": [{"quote": "PFOA is treated."}]}]
    assert adapt(p).facts[0].evidence[0].chunk_id == "c1"
    p["entities"][0]["evidence"] = [{"quote": "PFOS"}]
    with pytest.raises(ValueError): adapt(p)
