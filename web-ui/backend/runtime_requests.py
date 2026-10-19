"""Bound actual QA requests across chat and query embedding calls."""

from __future__ import annotations

import asyncio
import hashlib
import weakref

import numpy as np


class RuntimeRequestLimiter:
    def __init__(self):
        self._loops = weakref.WeakKeyDictionary()

    def _state(self):
        loop = asyncio.get_running_loop()
        return self._loops.setdefault(loop, {
            "groups": {}, "keys": {}, "active": 0, "peak": 0,
            "key_active": {}, "key_peak": 0, "requests": 0,
        })

    async def acquire(self, endpoint, key, *, total_limit=10, per_key_limit=1):
        state = self._state()
        endpoint = str(endpoint or "").rstrip("/")
        fingerprint = hashlib.sha256(str(key or "").encode()).hexdigest()
        identity = (endpoint, fingerprint)
        group = state["groups"].setdefault((endpoint, total_limit), asyncio.Semaphore(max(1, total_limit)))
        key_slot = state["keys"].setdefault((identity, per_key_limit), asyncio.Semaphore(max(1, per_key_limit)))
        await key_slot.acquire()
        try:
            await group.acquire()
        except BaseException:
            key_slot.release()
            raise
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        state["key_active"][identity] = state["key_active"].get(identity, 0) + 1
        state["key_peak"] = max(state["key_peak"], state["key_active"][identity])
        state["requests"] += 1
        released = False

        def release():
            nonlocal released
            if released:
                return
            released = True
            state["active"] -= 1
            state["key_active"][identity] -= 1
            group.release()
            key_slot.release()

        return release

    def snapshot(self):
        state = self._state()
        return {"active": state["active"], "network_peak": state["peak"],
                "key_peak": state["key_peak"], "requests": state["requests"]}


QA_REQUEST_LIMITER = RuntimeRequestLimiter()


async def request_query_embeddings(
    texts, candidates, request, *, dimension, timeout=120.0,
    max_attempts=3, total_limit=10, per_key_limit=1,
    limiter=QA_REQUEST_LIMITER, on_result=None,
):
    """Try distinct single keys and validate each returned query vector."""
    if not texts:
        return np.empty((0, dimension), dtype=np.float32)
    if not candidates:
        raise RuntimeError("No query embedding key candidates are available")
    errors = []
    for attempt, candidate in enumerate(candidates[:max(1, max_attempts)], 1):
        provider = candidate["provider"]
        key = candidate.get("key")
        if key and any(char in key for char in "\r\n,;"):
            raise ValueError("Query embedding requires one API key per request")
        release = await limiter.acquire(
            provider.get("baseUrl"), key,
            total_limit=min(total_limit, int(provider.get("maxAsync") or total_limit)),
            per_key_limit=min(per_key_limit, int(provider.get("perKeyMaxAsync") or per_key_limit)),
        )
        error = None
        try:
            response = await asyncio.wait_for(request(
                texts, model=provider["modelName"], api_key=key,
                base_url=provider.get("baseUrl"), timeout=timeout,
                dimensions=dimension,
            ), timeout=timeout + 5.0)
            vectors = np.asarray(response, dtype=np.float32)
            if vectors.shape != (len(texts), dimension):
                raise ValueError(f"Query embedding shape {vectors.shape} != {(len(texts), dimension)}")
            if not np.isfinite(vectors).all() or not np.all(np.any(vectors != 0, axis=1)):
                raise ValueError("Query embedding must contain finite nonzero vectors")
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            error = exc
        finally:
            release()
        if on_result:
            on_result(candidate, error, attempt)
        if error is None:
            return vectors
        # Error summaries deliberately omit upstream text that may contain a key.
        errors.append(f"key {candidate.get('key_index')}: {type(error).__name__}")
    raise RuntimeError("Query embedding failed after bounded key retries: " + "; ".join(errors))
