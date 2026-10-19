"""Explicit, credential-free profile contracts used by v2 CLI and Web jobs."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field

from hyperche.request_leases import RequestBroker
from .contracts import digest
from .decisions import ChatTransport, TransportFailure


class ModelProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    profile_id: str = Field(min_length=1)
    role: Literal["normalization", "embedding"]
    endpoint: str = Field(min_length=1)
    model: str = Field(min_length=1)
    api_key_env: str = Field(min_length=1)
    dimension: int | None = None
    timeout: int = Field(default=180, ge=1, le=1800)
    temperature: Literal[0] = 0
    reasoning_effort: Literal["low"] = "low"

    @property
    def fingerprint(self):
        return digest(self.model_dump(exclude={"api_key_env"}))

    def key(self):
        value = os.environ.get(self.api_key_env)
        if not value:
            raise ValueError("Explicit profile credential environment variable is unavailable")
        return value

    def chat(self, *, broker=None):
        if self.role != "normalization": raise ValueError("An explicit normalization profile is required")
        return ChatTransport(endpoint=self.endpoint, model=self.model, key=self.key(),
                             profile_hash=self.fingerprint, timeout=self.timeout, broker=broker)

    @classmethod
    def read(cls, path):
        return cls.model_validate(json.loads(Path(path).read_text(encoding="utf-8-sig")))


class EmbeddingTransport:
    def __init__(self, profile: ModelProfile, *, broker=None, key=None):
        if profile.role != "embedding" or not profile.dimension or profile.dimension < 1:
            raise ValueError("Explicit embedding model and dimension are required")
        if not profile.endpoint.startswith(("https://", "http://127.0.0.1:")):
            raise ValueError("Invalid embedding endpoint")
        self.profile, self.key = profile, key or profile.key()
        self.broker, self.actual_requests = broker or RequestBroker(), 0

    async def __call__(self, texts, *, model, dimensions):
        if model != self.profile.model or dimensions != self.profile.dimension:
            raise ValueError("Embedding request conflicts with its frozen profile")
        lease = await self.broker.acquire(self.key, role="embedding")
        try:
            async with httpx.AsyncClient(timeout=self.profile.timeout, transport=httpx.AsyncHTTPTransport(retries=0)) as client:
                self.actual_requests += 1
                response = await client.post(self.profile.endpoint.rstrip("/") + "/embeddings",
                    headers={"Authorization": "Bearer " + self.key},
                    json={"model": model, "input": texts, "dimensions": dimensions})
                if response.status_code != 200:
                    raise TransportFailure(f"HTTP_{response.status_code}")
                data = sorted(response.json()["data"], key=lambda row: row["index"])
                if [row["index"] for row in data] != list(range(len(texts))):
                    raise ValueError("Embedding response indices do not match input rows")
                return [row["embedding"] for row in data]
        except TransportFailure:
            raise
        except Exception as exc:
            raise TransportFailure(type(exc).__name__) from None
        finally:
            lease.release()
