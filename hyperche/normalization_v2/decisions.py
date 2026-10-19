"""Bounded identity judgments with explicit profiles and immutable successes."""
from __future__ import annotations

import asyncio
import json
import os
from typing import Literal
import uuid

import httpx
from pydantic import BaseModel, ConfigDict, Field

from hyperche.request_leases import RequestBroker
from .candidate_index import compatible
from .contracts import CanonicalEntity, EvidenceSpan, Mention, canonical_json, digest, validate_evidence
from .text_policy import default_normalizer_for_kind, normalize


RULES = """Decide chemical identity only from the supplied source and declared candidates.
Return exactly one JSON object: outcome SAME_ID|NEW_ID|RELATED_VARIANT|UNCERTAIN,
candidate_id (a supplied ID for SAME_ID/RELATED_VARIANT, otherwise null),
reason (nonempty string), evidence (array of exact source EvidenceSpan objects
with quote/start/end/chunk_id). Preserve charge, phase, acid/anion/salt, model,
composition, sample and unknown guards. Shared components and similar roles do
not prove identity. Do not generate IDs or promote global aliases. If uncertain
use UNCERTAIN. Scientific names/units/numbers may not be silently corrected.
"""
PROMPT_HASH = digest(RULES)


class Judgment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    outcome: Literal["SAME_ID", "NEW_ID", "RELATED_VARIANT", "UNCERTAIN"]
    candidate_id: str | None
    reason: str = Field(min_length=1)
    evidence: list[EvidenceSpan]


def validate_judgment(value, task, source_text):
    result = Judgment.model_validate(value)
    mention = Mention.model_validate(task["mention"])
    candidates = {e["canonical_id"]: CanonicalEntity.model_validate(e) for e in task["candidates"]}
    if len(candidates) > 5 or not candidates:
        raise ValueError("Identity tasks require one to five frozen candidates")
    if result.outcome in {"SAME_ID", "RELATED_VARIANT"}:
        if result.candidate_id not in candidates:
            raise ValueError("Judgment refers to an unknown candidate")
        if not result.evidence:
            raise ValueError("Identity claims require exact source evidence")
        if not compatible(mention, candidates[result.candidate_id], exact=result.outcome == "SAME_ID"):
            raise ValueError("Judgment contradicts declared identity guards")
    elif result.candidate_id is not None:
        raise ValueError("New or unresolved identities cannot select a candidate")
    for span in result.evidence:
        validate_evidence(span, source_text, mention.chunk_id)
    return result


class TransportFailure(RuntimeError):
    """Safe diagnostics; upstream exception text and headers are never included."""


class ChatTransport:
    def __init__(self, *, endpoint: str, model: str, key: str, profile_hash: str,
                 broker=None, timeout=180):
        if not endpoint.startswith(("https://", "http://127.0.0.1:")) or not model or not profile_hash:
            raise ValueError("Explicit endpoint, model and frozen profile are required")
        self.endpoint, self.model, self.key = endpoint.rstrip("/"), model, key
        self.profile_hash, self.timeout = profile_hash, timeout
        self.broker = broker or RequestBroker()
        self.actual_requests = 0

    async def complete(self, messages, *, max_tokens):
        lease = await self.broker.acquire(self.key, role="normalization")
        try:
            # No SDK and no hidden transport retries. Every actual send is
            # exactly one lease. Explicit worker retries account separately.
            async with httpx.AsyncClient(timeout=self.timeout,
                                         transport=httpx.AsyncHTTPTransport(retries=0)) as client:
                self.actual_requests += 1
                async with client.stream("POST", self.endpoint + "/chat/completions",
                        headers={"Authorization": "Bearer " + self.key},
                        json={"model": self.model, "messages": messages, "stream": True,
                              "stream_options": {"include_usage": True}, "temperature": 0,
                              "reasoning_effort": "low", "max_tokens": max_tokens}) as response:
                    if response.status_code != 200:
                        raise TransportFailure(f"HTTP_{response.status_code}")
                    content, finish, done, usage = [], None, False, None
                    async for line in response.aiter_lines():
                        if not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            done = True
                            continue
                        event = json.loads(data)
                        usage = event.get("usage") or usage
                        for choice in event.get("choices", []):
                            content.append(choice.get("delta", {}).get("content") or "")
                            finish = choice.get("finish_reason") or finish
                    if not done:
                        raise TransportFailure("INCOMPLETE_STREAM")
                    return {"content": "".join(content), "finish_reason": finish,
                            "usage": usage, "model": self.model, "stream_complete": done}
        except asyncio.CancelledError:
            raise
        except TransportFailure:
            raise
        except Exception as exc:
            raise TransportFailure(type(exc).__name__) from None
        finally:
            lease.release()


class DecisionWorker:
    def __init__(self, ledger, registry, transport, *, max_requests: int):
        if isinstance(max_requests, bool) or max_requests < 0:
            raise ValueError("A nonnegative explicit request budget is required")
        self.ledger, self.registry, self.transport = ledger, registry, transport
        self.max_requests = max_requests
        self.requests = 0
        self.owner = f"{os.getpid()}:{uuid.uuid4().hex}"

    def _source(self, mention):
        sources = [b for b in self.ledger.batches() if b["doc_id"] == mention["doc_id"]
                   and b["revision_hash"] == mention["revision_hash"] and b["chunk_id"] == mention["chunk_id"]]
        if len({b["chunk_hash"] for b in sources}) != 1:
            raise ValueError("Judgment source is absent or ambiguous")
        return sources[0]["raw_text"]

    async def process(self, row):
        task_id, task = row["id"], row["payload"]
        prior = self.ledger.decision(task_id)
        if prior:
            return {"task_id": task_id, "status": "resume", "decision": prior}
        if task["profile_hash"] != self.transport.profile_hash or task["prompt_hash"] != PROMPT_HASH:
            raise ValueError("Frozen profile/prompt mismatch; create a new task explicitly")
        if not self.ledger.claim_task(task_id, self.owner):
            return {"task_id": task_id, "status": "leased_elsewhere"}
        try:
            source = self._source(task["mention"])
        except Exception:
            self.ledger.task_status(task_id, "technical_failed", owner=self.owner)
            raise
        messages = [{"role": "system", "content": RULES}, {"role": "user", "content": canonical_json({"task": task, "source": source})}]
        receipts = [json.loads(row[0]) for row in self.ledger.db.execute("SELECT payload FROM attempts WHERE task_id=? ORDER BY id", (task_id,))]
        for receipt in receipts:
            if receipt.get("status") == "validated":
                response = receipt["response"]
                if response.get("finish_reason") == "stop" and response.get("stream_complete") is True:
                    result = validate_judgment(json.loads(response["content"]), task, source)
                    return self._apply(task_id, task, result)
        previous_attempts = self.ledger.db.execute("SELECT COUNT(*) FROM attempts WHERE task_id=?", (task_id,)).fetchone()[0]
        for attempt, budget in list(enumerate((4096, 8192, 16384), 1))[previous_attempts:]:
            if self.requests >= self.max_requests:
                self.ledger.task_status(task_id, "budget_deferred", owner=self.owner)
                return {"task_id": task_id, "status": "budget_deferred"}
            self.requests += 1
            response = None
            try:
                response = await self.transport.complete(messages, max_tokens=budget)
                if response.get("finish_reason") != "stop" or response.get("stream_complete") is not True:
                    raise ValueError("Incomplete model response")
                result = validate_judgment(json.loads(response["content"]), task, source)
            except asyncio.CancelledError:
                self.ledger.task_status(task_id, "pending", owner=self.owner)
                raise
            except Exception as exc:
                self.ledger.attempt(task_id, {"attempt": attempt, "max_tokens": budget,
                    "status": "technical_failed", "error_type": type(exc).__name__, "response": response})
                # Clean-root retries, never repeat an invalid assistant object.
                continue
            self.ledger.attempt(task_id, {"attempt": attempt, "max_tokens": budget,
                "status": "validated", "response": response})
            return self._apply(task_id, task, result)
        self.ledger.task_status(task_id, "technical_failed", owner=self.owner)
        return {"task_id": task_id, "status": "technical_failed"}

    def _apply(self, task_id, task, result):
        try:
            with self.ledger.transaction():
                return self._commit_result(task_id, task, result)
        except BaseException:
            # The validated call receipt is already durable. A failure in the
            # identity transaction must be resumable without another API call.
            row = self.ledger.db.execute("SELECT status,owner FROM tasks WHERE id=?", (task_id,)).fetchone()
            if row and row["status"] == "running" and row["owner"] == self.owner:
                self.ledger.task_status(task_id, "pending", owner=self.owner)
            raise

    def _commit_result(self, task_id, task, result):
            identifier = task["provisional_id"]
            method = "resolved_llm"
            if result.outcome == "SAME_ID":
                identifier = result.candidate_id
                candidate = next(e for e in task["candidates"] if e["canonical_id"] == identifier)
                if not self.ledger.entity(identifier):
                    self.ledger.ensure_entity(candidate, status=candidate.get("status", "confirmed"))
            elif result.outcome == "RELATED_VARIANT":
                current = self.ledger.entity(identifier)
                current["parent_id"] = result.candidate_id
                self.ledger.revise_entity(identifier, current, reason="source-confirmed related variant")
                method = "provisional_related"
            elif result.outcome == "NEW_ID":
                method = "provisional_new"
            else:
                method = "deferred_semantic"
            payload = {**result.model_dump(mode="json"), "canonical_id": identifier, "binding_method": method}
            with self.ledger.transaction():
                decision_id = self.ledger.save_decision(task_id, payload)
                mention = Mention.model_validate(task["mention"])
                self.ledger.bind(mention.mention_id, identifier, method=method, decision_id=decision_id,
                                 metadata={"task_id": task_id})
                self.ledger.task_status(task_id, "deferred_semantic" if result.outcome == "UNCERTAIN" else "completed", owner=self.owner)
                if result.outcome == "SAME_ID":
                    policy = default_normalizer_for_kind(mention.kind)
                    dependency_ids = [e["canonical_id"] for e in task["candidates"] if e["canonical_id"] in self.registry.entities]
                    dependency = self.registry.dependency_hash(dependency_ids) if dependency_ids else digest([])
                    self.ledger.add_learned_alias({"canonical_id": identifier, "kind": mention.kind,
                        "granularity": mention.granularity, "normalizer": policy,
                        "normalized": normalize(mention.raw_name, policy), "attributes": mention.attributes,
                        "scope": {**mention.scope, "doc_id": mention.doc_id, "revision_hash": mention.revision_hash},
                        "dependency_ids": dependency_ids, "dependency_hash": dependency}, decision_id=decision_id)
            return {"task_id": task_id, "status": method, "decision": payload}

    async def run(self):
        # Sequential per-worker issuance makes its explicit budget exact. The
        # broker coordinates multiple workers and existing QA roles globally.
        return [await self.process(task) for task in self.ledger.tasks(
            ["pending", "technical_failed", "budget_deferred", "running"])]
