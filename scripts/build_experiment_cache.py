"""Build a Hyper-ChE experiment cache for one configured mode."""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
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


def text_hash(text: str) -> str:
    return hashlib.md5((text or "").encode("utf-8")).hexdigest()


def safe_id(value: str) -> str:
    text = re.sub(r"\s+", "_", str(value or "").strip())
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("._-")
    return text or "doc"


def extract_numeric_index(path: Path, fallback: int) -> int:
    match = re.search(r"(\d+)", path.stem)
    return int(match.group(1)) if match else fallback


def infer_title(text: str, file_path: Path) -> str:
    for line in (text or "").splitlines()[:40]:
        stripped = line.strip()
        if stripped.startswith("#"):
            stripped = stripped.lstrip("#").strip()
        if stripped and not stripped.lower().startswith("source file:"):
            return stripped[:240]
    return file_path.stem


def iter_text_files(path: Path) -> Iterable[Path]:
    for suffix in ("*.md", "*.markdown", "*.txt"):
        yield from path.rglob(suffix)


def read_input_documents(
    path: Path,
    *,
    doc_id_prefix: str,
    doc_start: int | None = None,
    doc_end: int | None = None,
) -> list[dict]:
    if path.is_file():
        text = path.read_text(encoding="utf-8-sig")
        doc_number = doc_start or extract_numeric_index(path, 1)
        doc_id = f"{safe_id(doc_id_prefix)}_{doc_number:03d}"
        return [
            {
                "doc_id": doc_id,
                "source_doc_id": doc_id,
                "source_file": path.name,
                "source_path": str(path.resolve()),
                "title": infer_title(text, path),
                "text_hash": text_hash(text),
                "content": text,
            }
        ]
    if not path.is_dir():
        raise FileNotFoundError(f"Input path not found: {path}")
    documents = []
    files = sorted(iter_text_files(path))
    for ordinal, file_path in enumerate(files, start=1):
        doc_number = extract_numeric_index(file_path, ordinal)
        if doc_start is not None and doc_number < doc_start:
            continue
        if doc_end is not None and doc_number > doc_end:
            continue
        text = file_path.read_text(encoding="utf-8-sig")
        content = f"# Source File: {file_path.name}\n\n{text}"
        doc_id = f"{safe_id(doc_id_prefix)}_{doc_number:03d}"
        documents.append(
            {
                "doc_id": doc_id,
                "source_doc_id": doc_id,
                "source_file": file_path.name,
                "source_path": str(file_path.resolve()),
                "title": infer_title(text, file_path),
                "text_hash": text_hash(text),
                "content": content,
            }
        )
    if not documents:
        raise FileNotFoundError(f"No .md/.txt files found under: {path}")
    return documents


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def write_manifest(path: Path, documents: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for doc in documents:
            payload = {
                "doc_id": doc["doc_id"],
                "source_doc_id": doc["source_doc_id"],
                "source_file": doc.get("source_file", ""),
                "source_path": doc.get("source_path", ""),
                "title": doc.get("title", ""),
                "text_hash": doc.get("text_hash", ""),
                "chars": len(doc.get("content", "")),
            }
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def load_completed_doc_ids(cache_dir: Path, progress_path: Path) -> set[str]:
    completed = set()
    full_docs_path = cache_dir / "kv_store_full_docs.json"
    if full_docs_path.exists():
        try:
            data = json.loads(full_docs_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                completed.update(str(key) for key in data.keys())
                for value in data.values():
                    if isinstance(value, dict) and value.get("doc_id"):
                        completed.add(str(value["doc_id"]))
        except Exception as exc:
            print(f"[BuildExperiment] warning: failed to read existing full docs: {exc}", flush=True)
    if progress_path.exists():
        for line in progress_path.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if item.get("status") == "success" and item.get("doc_id"):
                completed.add(str(item["doc_id"]))
    return completed


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
    parser.add_argument("--doc-id-prefix", default="DOC", help="Stable document ID prefix, e.g. RFB.")
    parser.add_argument("--doc-start", type=int, default=None, help="Only include files whose numeric index is >= this value.")
    parser.add_argument("--doc-end", type=int, default=None, help="Only include files whose numeric index is <= this value.")
    parser.add_argument("--resume", action="store_true", help="Skip documents already completed in this cache.")
    parser.add_argument("--manifest", type=Path, default=None, help="Optional corpus_manifest.jsonl output path.")
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
    cache_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.manifest or (cache_dir / "corpus_manifest.jsonl")
    progress_path = cache_dir / "build_progress.jsonl"
    extra = {
        "input": str(args.input.resolve()),
        "doc_id_prefix": args.doc_id_prefix,
        "doc_start": args.doc_start,
        "doc_end": args.doc_end,
        "resume": args.resume,
        "corpus_manifest_path": str(manifest_path.resolve()),
        "build_progress_path": str(progress_path.resolve()),
        "index_profile": resolved.get("index_profile"),
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

    documents = read_input_documents(
        args.input,
        doc_id_prefix=args.doc_id_prefix,
        doc_start=args.doc_start,
        doc_end=args.doc_end,
    )
    write_manifest(manifest_path, documents)
    print(
        f"[BuildExperiment] loaded input docs={len(documents)} "
        f"chars={sum(len(doc.get('content', '')) for doc in documents)}",
        flush=True,
    )
    print(f"[BuildExperiment] corpus_manifest written: {manifest_path}", flush=True)

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
        "index_profile": resolved.get("index_profile", "dual_concat"),
        "corpus_manifest_path": str(manifest_path.resolve()),
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
    run_config_path = write_run_config(cache_dir, resolved, extra=extra)
    print(f"[BuildExperiment] run_config refreshed after HyperRAG init: {run_config_path}", flush=True)
    completed_doc_ids = load_completed_doc_ids(cache_dir, progress_path) if args.resume else set()
    if completed_doc_ids:
        print(f"[BuildExperiment] resume enabled; completed docs detected={len(completed_doc_ids)}", flush=True)

    total = len(documents)
    for index, doc in enumerate(documents, start=1):
        doc_id = str(doc["doc_id"])
        if args.resume and doc_id in completed_doc_ids:
            print(f"[BuildExperiment] skip completed {index}/{total}: {doc_id} {doc.get('source_file', '')}", flush=True)
            append_jsonl(
                progress_path,
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "skipped",
                    "doc_id": doc_id,
                    "source_file": doc.get("source_file", ""),
                    "reason": "resume_completed",
                },
            )
            continue
        print(f"[BuildExperiment] start {index}/{total}: {doc_id} {doc.get('source_file', '')}", flush=True)
        append_jsonl(
            progress_path,
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "start",
                "doc_id": doc_id,
                "source_file": doc.get("source_file", ""),
                "text_hash": doc.get("text_hash", ""),
            },
        )
        try:
            await rag.ainsert(doc)
            append_jsonl(
                progress_path,
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "success",
                    "doc_id": doc_id,
                    "source_file": doc.get("source_file", ""),
                    "text_hash": doc.get("text_hash", ""),
                },
            )
            print(f"[BuildExperiment] success {index}/{total}: {doc_id}", flush=True)
        except Exception as exc:
            append_jsonl(
                progress_path,
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "error",
                    "doc_id": doc_id,
                    "source_file": doc.get("source_file", ""),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
            print(f"[BuildExperiment] error {index}/{total}: {doc_id}: {type(exc).__name__}: {exc}", flush=True)
            raise
    print(f"[BuildExperiment] cache build complete: {cache_dir.resolve()}", flush=True)


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()

