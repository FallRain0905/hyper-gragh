import asyncio
import json

import pytest

from hyperche.normalization_v2.contracts import CanonicalEntity
from hyperche.normalization_v2.decisions import DecisionWorker, PROMPT_HASH, validate_judgment
from hyperche.normalization_v2.ledger import Ledger
from hyperche.normalization_v2.registry import Registry
from hyperche.normalization_v2.resolver import Resolver
from test_resolver import batch


def setup(tmp_path):
    ledger = Ledger(tmp_path / "ledger.sqlite", "test")
    registry = Registry([CanonicalEntity(canonical_id="known", canonical_name="PFOA-7", kind="chemical")])
    b = batch("PFOA7")
    ledger.import_batch(b)
    resolver = Resolver(ledger, registry, profile_hash="profile", prompt_hash=PROMPT_HASH)
    resolver.run()
    return ledger, registry, b, ledger.tasks()[0]


def good(b, outcome="SAME_ID"):
    return {"outcome": outcome, "candidate_id": "known" if outcome in {"SAME_ID", "RELATED_VARIANT"} else None,
            "reason": "Explicit identity evidence in this synthetic test only",
            "evidence": [{"quote": "PFOA7", "start": 0, "end": 5, "chunk_id": b["chunk_id"]}]}


class Fake:
    profile_hash = "profile"
    def __init__(self, responses):
        self.responses, self.calls = list(responses), []
    async def complete(self, messages, *, max_tokens):
        self.calls.append(max_tokens)
        result = self.responses.pop(0)
        if isinstance(result, BaseException): raise result
        return result


def response(value, finish="stop"):
    return {"content": json.dumps(value), "finish_reason": finish, "stream_complete": True, "usage": None}


def test_success_is_immutable_and_resume_does_not_reissue(tmp_path):
    ledger, registry, b, task = setup(tmp_path)
    transport = Fake([response(good(b))])
    worker = DecisionWorker(ledger, registry, transport, max_requests=3)
    assert asyncio.run(worker.run())[0]["status"] == "resolved_llm"
    before = ledger.counts()
    assert asyncio.run(worker.run()) == []
    assert transport.calls == [4096]
    assert ledger.counts() == before
    assert ledger.bindings()[b["mentions"][0]["mention_id"]]["entity_id"] == "known"
    assert ledger.learned_aliases()[0]["scope"]["doc_id"] == "doc1"
    ledger.close()


def test_truncation_and_fake_spans_are_not_valid_judgments(tmp_path):
    ledger, registry, b, task = setup(tmp_path)
    forged = good(b)
    forged["evidence"][0]["quote"] = "not in source"
    transport = Fake([response(good(b), "length"), response(forged), response(good(b))])
    result = asyncio.run(DecisionWorker(ledger, registry, transport, max_requests=3).run())
    assert result[0]["status"] == "resolved_llm"
    assert transport.calls == [4096, 8192, 16384]
    assert ledger.db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0] == 3
    ledger.close()


def test_three_failed_calls_remain_failed_and_do_not_reset_on_resume(tmp_path):
    ledger, registry, b, task = setup(tmp_path)
    transport = Fake([response({}, "length")] * 3)
    worker = DecisionWorker(ledger, registry, transport, max_requests=9)
    assert asyncio.run(worker.run())[0]["status"] == "technical_failed"
    assert asyncio.run(worker.run())[0]["status"] == "technical_failed"
    assert len(transport.calls) == 3
    assert ledger.decision(task["id"]) is None
    ledger.begin_generation("g1", {"resolution_task_ids": [task["id"]]})
    with pytest.raises(ValueError, match="technically unfinished"): ledger.publish_generation("g1")
    # Retiring a source/task does not turn its historical failure into success.
    ledger.begin_generation("g2", {"resolution_task_ids": []})
    ledger.publish_generation("g2")
    assert ledger.tasks()[0]["status"] == "technical_failed"
    ledger.close()


def test_budget_zero_does_not_call_and_scientific_uncertainty_is_separate(tmp_path):
    ledger, registry, b, task = setup(tmp_path)
    transport = Fake([response(good(b, "UNCERTAIN"))])
    assert asyncio.run(DecisionWorker(ledger, registry, transport, max_requests=0).run())[0]["status"] == "budget_deferred"
    assert transport.calls == []
    assert asyncio.run(DecisionWorker(ledger, registry, transport, max_requests=1).run())[0]["status"] == "deferred_semantic"
    assert ledger.tasks()[0]["status"] == "deferred_semantic"
    ledger.close()


def test_invalid_candidate_and_guard_conflict_rejected(tmp_path):
    ledger, registry, b, task = setup(tmp_path)
    altered = good(b)
    altered["candidate_id"] = "invented"
    with pytest.raises(ValueError, match="unknown candidate"):
        validate_judgment(altered, task["payload"], b["raw_text"])
    task["payload"]["candidates"][0].update(identity_guards=["phase"], properties={"phase": "alpha"})
    with pytest.raises(ValueError, match="identity guards"):
        validate_judgment(good(b), task["payload"], b["raw_text"])
    ledger.close()


def test_cancelled_worker_preserves_pending_task(tmp_path):
    ledger, registry, b, task = setup(tmp_path)
    transport = Fake([asyncio.CancelledError()])
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(DecisionWorker(ledger, registry, transport, max_requests=1).run())
    assert ledger.tasks()[0]["status"] == "pending"
    assert ledger.decision(task["id"]) is None
    ledger.close()


def test_validated_receipt_recovers_after_identity_transaction_failure_without_new_call(tmp_path, monkeypatch):
    ledger, registry, b, task = setup(tmp_path)
    transport = Fake([response(good(b))])
    worker = DecisionWorker(ledger, registry, transport, max_requests=1)
    original = ledger.save_decision
    def fail(*args, **kw): raise OSError("injected transaction failure")
    monkeypatch.setattr(ledger, "save_decision", fail)
    with pytest.raises(OSError): asyncio.run(worker.run())
    assert ledger.tasks()[0]["status"] == "pending"
    assert ledger.decision(task["id"]) is None
    monkeypatch.setattr(ledger, "save_decision", original)
    assert asyncio.run(worker.run())[0]["status"] == "resolved_llm"
    assert transport.calls == [4096]
    ledger.close()
