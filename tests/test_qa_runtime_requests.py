import asyncio
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "web-ui" / "backend"))
from runtime_requests import RuntimeRequestLimiter, request_query_embeddings


def candidates(keys):
    return [{"provider": {"modelName": "embedding", "baseUrl": "https://test/v1",
                          "maxAsync": 10, "perKeyMaxAsync": 1},
             "key": key, "key_index": i + 1, "key_total": len(keys)}
            for i, key in enumerate(keys)]


def test_chat_and_embedding_share_total_and_physical_key_limits():
    async def run():
        limiter = RuntimeRequestLimiter()
        active = Counter()
        peaks = Counter()

        async def chat(key):
            release = await limiter.acquire("https://test/v1", key, total_limit=3)
            active[key] += 1
            peaks[key] = max(peaks[key], active[key])
            try:
                await asyncio.sleep(0.005)
            finally:
                active[key] -= 1
                release()

        async def embed(texts, api_key, **kwargs):
            active[api_key] += 1
            peaks[api_key] = max(peaks[api_key], active[api_key])
            try:
                await asyncio.sleep(0.005)
                return np.ones((len(texts), 4))
            finally:
                active[api_key] -= 1

        work = []
        for i in range(24):
            key = str(i % 5)
            work.extend([chat(key), request_query_embeddings(
                ["query"], candidates([key]), embed, dimension=4,
                total_limit=3, limiter=limiter)])
        await asyncio.gather(*work)
        stats = limiter.snapshot()
        assert stats["active"] == 0 and stats["network_peak"] == 3
        assert stats["key_peak"] == 1 and max(peaks.values()) == 1

    asyncio.run(run())


def test_failed_key_is_retried_with_one_distinct_key_and_explicit_dimensions():
    async def run():
        seen = []

        async def request(texts, api_key, dimensions, timeout, **kwargs):
            seen.append((api_key, dimensions, timeout))
            if api_key == "first":
                raise TimeoutError("request timed out")
            return np.ones((len(texts), dimensions))

        vectors = await request_query_embeddings(
            ["query"], candidates(["first", "second"]), request, dimension=4,
            timeout=3, limiter=RuntimeRequestLimiter())
        assert seen == [("first", 4, 3), ("second", 4, 3)]
        assert vectors.shape == (1, 4)

    asyncio.run(run())


@pytest.mark.parametrize("invalid", [np.ones((1, 3)), np.full((1, 4), np.nan), np.zeros((1, 4))])
def test_invalid_query_vectors_never_count_as_success(invalid):
    async def request(*args, **kwargs):
        return invalid

    with pytest.raises(RuntimeError, match="bounded key retries"):
        asyncio.run(request_query_embeddings(
            ["query"], candidates(["key"]), request, dimension=4, limiter=RuntimeRequestLimiter()))


def test_cancellation_releases_key_without_starting_a_retry():
    async def run():
        limiter = RuntimeRequestLimiter()
        entered = asyncio.Event()
        called = []

        async def request(*args, api_key, **kwargs):
            called.append(api_key)
            entered.set()
            await asyncio.Event().wait()

        task = asyncio.create_task(request_query_embeddings(
            ["query"], candidates(["first", "second"]), request,
            dimension=4, limiter=limiter))
        await entered.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert called == ["first"] and limiter.snapshot()["active"] == 0
        release = await asyncio.wait_for(limiter.acquire("https://test/v1", "first"), 1)
        release()

    asyncio.run(run())


def test_joined_keys_are_rejected_before_any_request():
    async def request(*args, **kwargs):
        raise AssertionError("must not send joined keys")

    with pytest.raises(ValueError, match="one API key"):
        asyncio.run(request_query_embeddings(
            ["query"], candidates(["first\nsecond"]), request,
            dimension=4, limiter=RuntimeRequestLimiter()))
