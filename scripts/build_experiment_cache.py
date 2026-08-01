"""Build a Hyper-ChE experiment cache for one configured mode."""

from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path
import re
import sys
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hyperrag import HyperRAG
from hyperrag.experiment import resolve_experiment_mode, write_run_config
from hyperrag.llm import openai_complete_if_cache, openai_embedding
from hyperrag.utils import EmbeddingFunc


def read_input(path: Path) -> str:
    if path.is_file():
        return path.read_text(encoding="utf-8-sig")
    if not path.is_dir():
        raise FileNotFoundError(f"Input path not found: {path}")
    parts = []
    for file_path in sorted(iter_text_files(path)):
        parts.append(f"\n\n# Source File: {file_path.name}\n\n")
        parts.append(file_path.read_text(encoding="utf-8-sig"))
    if not parts:
        raise FileNotFoundError(f"No .md/.txt files found under: {path}")
    return "".join(parts)


def iter_text_files(path: Path) -> Iterable[Path]:
    for suffix in ("*.md", "*.markdown", "*.txt"):
        yield from path.rglob(suffix)


def env_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def split_key_pool(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[;,\r\n]+", value or "") if part.strip()]


class AsyncKeyPool:
    def __init__(self, keys: list[str], *, name: str):
        if not keys:
            raise RuntimeError(f"{name} key pool is empty")
        self.keys = keys
        self.name = name
        self._index = 0
        self._lock = asyncio.Lock()

    async def next(self) -> tuple[int, str]:
        async with self._lock:
            idx = self._index % len(self.keys)
            self._index += 1
            return idx, self.keys[idx]


def positive_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got {value!r}") from exc


def build_llm_func(*, model: str, base_url: str | None, api_keys: list[str], timeout: float):
    pool = AsyncKeyPool(api_keys, name="LLM_API_KEY")

    async def llm_func(prompt: str, system_prompt=None, history_messages=None, **kwargs):
        attempts = max(1, min(len(api_keys), positive_int_env("LLM_KEY_ATTEMPTS", len(api_keys))))
        last_exc = None
        for attempt in range(attempts):
            key_index, api_key = await pool.next()
            try:
                return await openai_complete_if_cache(
                    model,
                    prompt,
                    system_prompt=system_prompt,
                    history_messages=history_messages or [],
                    base_url=base_url,
                    api_key=api_key,
                    timeout=timeout,
                    **kwargs,
                )
            except Exception as exc:
                last_exc = exc
                print(
                    f"[BuildExperiment] LLM call failed with key={key_index + 1}/{len(api_keys)} "
                    f"attempt={attempt + 1}/{attempts}: {type(exc).__name__}: {exc}",
                    flush=True,
                )
        raise last_exc

    return llm_func


def build_embedding_func(*, model: str, base_url: str | None, api_keys: list[str], dim: int, timeout: float) -> EmbeddingFunc:
    pool = AsyncKeyPool(api_keys, name="EMB_API_KEY")

    async def embedding_func(texts: list[str]):
        attempts = max(1, min(len(api_keys), positive_int_env("EMB_KEY_ATTEMPTS", len(api_keys))))
        last_exc = None
        for attempt in range(attempts):
            key_index, api_key = await pool.next()
            try:
                return await openai_embedding(
                    texts,
                    model=model,
                    base_url=base_url,
                    api_key=api_key,
                    timeout=timeout,
                )
            except Exception as exc:
                last_exc = exc
                print(
                    f"[BuildExperiment] embedding call failed with key={key_index + 1}/{len(api_keys)} "
                    f"attempt={attempt + 1}/{attempts}: {type(exc).__name__}: {exc}",
                    flush=True,
                )
        raise last_exc

    return EmbeddingFunc(embedding_dim=dim, max_token_size=8192, func=embedding_func)


async def amain() -> None:
    parser = argparse.ArgumentParser(description="Build a Hyper-ChE experiment cache.")
    parser.add_argument("--input", required=True, type=Path, help="Input markdown/text file or directory.")
    parser.add_argument("--cache-dir", required=True, type=Path, help="Output HyperRAG cache directory.")
    parser.add_argument("--mode", default="hyper_final", help="Experiment mode from configs/experiments/modes.yaml.")
    parser.add_argument("--domain", default="flow_battery", help="Chemistry domain for chemistry prompt_profile.")
    parser.add_argument("--chunk-size", type=int, default=None)
    parser.add_argument("--chunk-overlap", type=int, default=None)
    parser.add_argument("--llm-timeout", type=float, default=float(os.getenv("LLM_TIMEOUT", "600")))
    parser.add_argument("--embedding-timeout", type=float, default=float(os.getenv("EMB_TIMEOUT", "120")))
    parser.add_argument("--llm-max-async", type=int, default=positive_int_env("LLM_MAX_ASYNC", 4))
    parser.add_argument("--embedding-max-async", type=int, default=positive_int_env("EMB_MAX_ASYNC", 8))
    parser.add_argument("--embedding-batch-num", type=int, default=positive_int_env("EMB_BATCH_NUM", 8))
    args = parser.parse_args()

    llm_api_keys = split_key_pool(env_required("LLM_API_KEY"))
    llm_base_url = os.getenv("LLM_BASE_URL")
    llm_model = env_required("LLM_MODEL")
    emb_api_keys = split_key_pool(env_required("EMB_API_KEY"))
    emb_base_url = os.getenv("EMB_BASE_URL")
    emb_model = env_required("EMB_MODEL")
    emb_dim = positive_int_env("EMB_DIM", 2560)

    resolved = resolve_experiment_mode(args.mode, domain=args.domain)
    cache_dir = args.cache_dir
    extra = {
        "input": str(args.input.resolve()),
        "llm": {"model": llm_model, "base_url": llm_base_url, "api_key_count": len(llm_api_keys)},
        "embedding": {
            "model": emb_model,
            "base_url": emb_base_url,
            "api_key_count": len(emb_api_keys),
            "embedding_dim": emb_dim,
        },
        "chunk_size": args.chunk_size,
        "chunk_overlap": args.chunk_overlap,
    }
    run_config_path = write_run_config(cache_dir, resolved, extra=extra)
    print(f"[BuildExperiment] run_config written: {run_config_path}", flush=True)
    print(f"[BuildExperiment] resolved mode: {resolved}", flush=True)
    print(f"[BuildExperiment] key pools: llm={len(llm_api_keys)}, embedding={len(emb_api_keys)}", flush=True)

    content = read_input(args.input)
    print(f"[BuildExperiment] loaded input chars={len(content)}", flush=True)

    rag_kwargs = {
        "working_dir": str(cache_dir),
        "domain": resolved["effective_domain"],
        "experiment_mode": resolved["experiment_mode"],
        "query_mode": resolved["query_mode"],
        "prompt_profile": resolved["prompt_profile"],
        "enable_entity_normalization": resolved["enable_entity_normalization"],
        "enable_measurement_instances": resolved["enable_measurement_instances"],
        "enable_efu_repair": resolved["enable_efu_repair"],
        "enable_hybrid_rerank": resolved["enable_hybrid_rerank"],
        "llm_model_func": build_llm_func(
            model=llm_model,
            base_url=llm_base_url,
            api_keys=llm_api_keys,
            timeout=args.llm_timeout,
        ),
        "llm_model_max_async": args.llm_max_async,
        "embedding_func": build_embedding_func(
            model=emb_model,
            base_url=emb_base_url,
            api_keys=emb_api_keys,
            dim=emb_dim,
            timeout=args.embedding_timeout,
        ),
        "embedding_func_max_async": args.embedding_max_async,
        "embedding_batch_num": args.embedding_batch_num,
    }
    if args.chunk_size is not None:
        rag_kwargs["chunk_token_size"] = args.chunk_size
    if args.chunk_overlap is not None:
        rag_kwargs["chunk_overlap_token_size"] = args.chunk_overlap

    rag = HyperRAG(**rag_kwargs)
    await rag.ainsert(content)
    print(f"[BuildExperiment] cache build complete: {cache_dir.resolve()}", flush=True)


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()

