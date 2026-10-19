"""Strict, resumable PFAS QA calls; never write to a knowledge-base cache."""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
from openai import AsyncOpenAI

REPO = Path(__file__).resolve().parents[1]
BACKEND = REPO / "web-ui" / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))
from runtime_requests import QA_REQUEST_LIMITER, request_query_embeddings

MODEL = "deepseek-ai/DeepSeek-V4-Flash"
ENDPOINT = "https://api.siliconflow.cn/v1"
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-4B"


def utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def append_json(path, value):
    with Path(path).open("a", encoding="utf-8") as f:
        f.write(json.dumps(value, ensure_ascii=False) + "\n")


def parse_json_response(content, finish_reason):
    if finish_reason != "stop":
        raise ValueError("Incomplete LLM response: finish_reason=" + str(finish_reason))
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Empty LLM response")
    text = content.strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    elif text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("Expected one JSON object")
    return value


class QAClient:
    """All roles share one actual-request limiter and physical-key identity."""

    def __init__(self, output):
        import providers
        for name in ("httpx", "httpcore", "openai"):
            logging.getLogger(name).setLevel(logging.WARNING)
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.candidates = {}
        self.cursor = 0
        self.clients = {}
        self.prompt_cache = self.output / "calls"
        self.prompt_cache.mkdir(exist_ok=True)
        for role in ("answer", "judge", "embedding"):
            ps = [p for p in providers.resolve_role_providers(role)
                  if p["baseUrl"].rstrip("/") == ENDPOINT
                  and p["modelName"] == (EMBEDDING_MODEL if role == "embedding" else MODEL)]
            candidates = providers.build_candidates(ps)
            if len(candidates) != 10 or len({c["key"] for c in candidates}) != 10:
                raise ValueError(f"QA {role} must resolve exactly 10 distinct authorized SiliconFlow keys")
            if any(c["provider"]["maxAsync"] != 10 or c["provider"].get("perKeyMaxAsync") != 1 for c in candidates):
                raise ValueError("QA role concurrency differs from authorized 10/1 configuration")
            self.candidates[role] = candidates

    def rotated(self, role):
        values = self.candidates[role]
        pos = self.cursor % len(values)
        self.cursor += 1
        return values[pos:] + values[:pos]

    def client(self, key):
        if key not in self.clients:
            self.clients[key] = AsyncOpenAI(api_key=key, base_url=ENDPOINT, timeout=180, max_retries=0)
        return self.clients[key]

    async def json(self, prompt, *, role="answer", validator=None, label="call", budgets=(4096, 8192, 16384), response_transform=None, recover_attempts=False, validation_feedback=None, fresh_validator=None):
        signature = digest({"prompt": prompt, "role": role, "model": MODEL, "temperature": 0,
                            "reasoning_effort": "low", "protocol": "pfas-qa-strict-v1"})
        cache_path = self.prompt_cache / (signature + ".json")
        if cache_path.exists():
            row = read_json(cache_path)
            if row.get("signature") == signature and row.get("status") == "ok":
                value = parse_json_response(row["content"], row["finish_reason"])
                if response_transform:
                    value = response_transform(value)
                if validator:
                    validator(value)
                return value
        # A complete failed response may become valid after a deterministic,
        # evidence-preserving format repair. Retain its raw content and trial.
        previous_rejection = None
        if recover_attempts:
            for attempt_path in sorted(self.prompt_cache.glob(signature + ".attempt*.json"), key=lambda p: p.stat().st_mtime_ns):
                row = {}
                try:
                    row = read_json(attempt_path)
                    if row.get("signature") != signature or row.get("status") != "failed":
                        continue
                    value = parse_json_response(row["content"], row["finish_reason"])
                    if response_transform:
                        value = response_transform(value)
                    if validator:
                        validator(value)
                except (ValueError, KeyError, TypeError) as exc:
                    if validation_feedback and row.get("content") and row.get("finish_reason") == "stop":
                        try:
                            rejected = parse_json_response(row["content"], row["finish_reason"])
                            previous_rejection = (row["content"], str(exc), validation_feedback(rejected, exc))
                        except (ValueError, KeyError, TypeError):
                            pass
                    continue
                proof = {"at": utc(), "label": label, "signature": signature,
                         "source_attempt": attempt_path.name, "source_sha256": file_hash(attempt_path),
                         "mode": "offline_full_response_revalidation", "new_api_requests": 0}
                write_json(cache_path, {**row, "status": "ok", "recovery": proof})
                append_json(self.output / "validation_recovery.jsonl", proof)
                return value
        failures = []
        candidates = self.rotated(role)
        messages = [{"role": "user", "content": prompt}]
        if previous_rejection:
            messages += [{"role": "assistant", "content": previous_rejection[0]},
                         {"role": "user", "content": "Correct the complete rejected JSON: " + previous_rejection[1]
                          + "\n" + previous_rejection[2]}]
        for i, budget in enumerate(budgets):
            candidate = candidates[i % len(candidates)]
            release = await QA_REQUEST_LIMITER.acquire(ENDPOINT, candidate["key"], total_limit=10, per_key_limit=1)
            started = time.monotonic()
            audit = {"at": utc(), "label": label, "signature": signature, "role": role,
                     "model": MODEL, "key_index": candidate["key_index"], "attempt": i + 1,
                     "max_tokens": budget}
            if validation_feedback:
                audit["response_format_assistance"] = "raw_context_candidates_full_validation_unchanged"
                audit["seeded_from_complete_failed_response"] = previous_rejection is not None
            content = ""
            finish = None
            try:
                response = await asyncio.wait_for(self.client(candidate["key"]).chat.completions.create(
                    model=MODEL, messages=messages,
                    temperature=0, max_tokens=budget, reasoning_effort="low", timeout=180,
                ), timeout=185)
                audit["http_status"] = 200
                if not response.choices:
                    raise ValueError("No response choice")
                content = response.choices[0].message.content
                finish = response.choices[0].finish_reason
                value = parse_json_response(content, finish)
                if response_transform:
                    value = response_transform(value)
                if validator:
                    validator(value)
                if fresh_validator:
                    fresh_validator(value)
                audit["status"] = "ok"
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                # Upstream error strings can contain Authorization credentials.
                audit.update(status="failed", error_type=type(exc).__name__)
                if isinstance(exc, (ValueError, json.JSONDecodeError)):
                    audit["validation_error"] = str(exc)[:350]
                failures.append(audit["error_type"])
            finally:
                release()
                audit.update(seconds=round(time.monotonic() - started, 3), finish_reason=finish,
                             content_chars=len(content or ""), requests=QA_REQUEST_LIMITER.snapshot())
                append_json(self.output / "request_audit.jsonl", audit)
                write_json(self.prompt_cache / (signature + f".attempt{i + 1}.{time.time_ns()}.json"),
                           {**audit, "content": content})
            if audit["status"] == "ok":
                write_json(cache_path, {**audit, "content": content})
                return value
            if content and audit.get("validation_error"):
                feedback = ""
                if validation_feedback:
                    try:
                        feedback = "\n" + validation_feedback(parse_json_response(content, finish), ValueError(audit["validation_error"]))
                    except (ValueError, KeyError, TypeError):
                        pass
                messages = [{"role": "user", "content": prompt},
                            {"role": "assistant", "content": content},
                            {"role": "user", "content": "Correct the rejected response: " + audit["validation_error"]
                             + ". Return the complete corrected JSON. Preserve exact raw source text. "
                             + "Use a longer exact span for short table cells. Check every scoring point exactly." + feedback}]
            await asyncio.sleep(min(2 ** i, 4))
        raise RuntimeError("QA call failed after bounded retries: " + ",".join(failures))

    async def embed(self, texts):
        async def request(texts, **kwargs):
            response = await self.client(kwargs["api_key"]).embeddings.create(
                model=EMBEDDING_MODEL, input=texts, dimensions=2560, timeout=120,
            )
            if len(response.data) != len(texts) or {d.index for d in response.data} != set(range(len(texts))):
                raise ValueError("Query embedding indexes are incomplete or duplicated")
            return [d.embedding for d in sorted(response.data, key=lambda d: d.index)]

        def done(candidate, error, attempt):
            append_json(self.output / "request_audit.jsonl", {
                "at": utc(), "role": "embedding", "key_index": candidate["key_index"],
                "attempt": attempt, "status": "ok" if error is None else "failed",
                "error_type": type(error).__name__ if error else None,
                "model": EMBEDDING_MODEL, "dimension": 2560,
                "requests": QA_REQUEST_LIMITER.snapshot(),
            })

        return await request_query_embeddings(texts, self.rotated("embedding"), request,
                                             dimension=2560, timeout=120, max_attempts=3,
                                             total_limit=10, per_key_limit=1, on_result=done)

    async def close(self):
        for client in self.clients.values():
            await client.close()
