"""Separate opt-in offline registry entry point. Existing CLIs are unchanged."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hyperche.normalization_v2.contracts import digest
from hyperche.normalization_v2.engine import Engine, IncompleteJob
from hyperche.normalization_v2.profiles import EmbeddingTransport, ModelProfile
from hyperche.normalization_v2.registry import Registry


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--stage", choices=["compile", "status", "import", "resolve", "judge", "project", "embed", "validate", "publish", "all"], default="status")
    cli.add_argument("--source", type=Path)
    cli.add_argument("--target", type=Path)
    cli.add_argument("--corpus-id")
    cli.add_argument("--registry", type=Path, action="append")
    cli.add_argument("--normalization-profile", type=Path)
    cli.add_argument("--embedding-profile", type=Path)
    cli.add_argument("--offline-profile-id", help="Explicit offline-only profile fingerprint seed")
    cli.add_argument("--embedding-model", help="Frozen retrieval embedding model, not an identity-candidate model")
    cli.add_argument("--embedding-dimension", type=int)
    cli.add_argument("--allow-api", action="store_true", help="Explicitly enable the selected profiles; default is zero API")
    cli.add_argument("--request-budget", type=int, default=0)
    cli.add_argument("--embedding-request-budget", type=int, default=0)
    cli.add_argument("--expected-docs", type=int)
    cli.add_argument("--expected-chunks", type=int)
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    registry_paths = args.registry or [ROOT / "configs/normalization_v2"]
    if args.stage == "compile":
        registry = Registry.from_paths(registry_paths)
        print(json.dumps({"status": "compiled", "registry_hash": registry.snapshot_hash,
                          "entities": len(registry.entities), "units": len(registry.units)}))
        return 0
    if args.stage == "status":
        if not args.target: raise ValueError("--target is required")
        path = args.target / "progress.json"
        print(path.read_text(encoding="utf-8") if path.exists() else '{"status":"not_started"}')
        return 0
    if not all((args.source, args.target, args.corpus_id)):
        raise ValueError("--source, --target and --corpus-id are required")
    normalization = ModelProfile.read(args.normalization_profile) if args.normalization_profile else None
    embedding = ModelProfile.read(args.embedding_profile) if args.embedding_profile else None
    if normalization and normalization.role != "normalization": raise ValueError("Wrong normalization profile role")
    if embedding and embedding.role != "embedding": raise ValueError("Wrong embedding profile role")
    if not normalization and not args.offline_profile_id:
        raise ValueError("Provide a frozen normalization profile or --offline-profile-id")
    if min(args.request_budget, args.embedding_request_budget) < 0:
        raise ValueError("Request budgets cannot be negative")
    if not args.allow_api and (args.request_budget or args.embedding_request_budget):
        raise ValueError("Nonzero API budgets require --allow-api")
    model = embedding.model if embedding else args.embedding_model
    dimension = embedding.dimension if embedding else args.embedding_dimension
    if not model or not dimension: raise ValueError("Explicit retrieval embedding model/dimension required")
    profile_hash = normalization.fingerprint if normalization else digest({"offline_profile_id": args.offline_profile_id})
    engine = Engine(source=args.source, target=args.target, corpus_id=args.corpus_id,
        registry_paths=registry_paths, normalization_profile_hash=profile_hash,
        embedding_model=model, embedding_dimension=dimension,
        expected_docs=args.expected_docs, expected_chunks=args.expected_chunks,
        accepted_targets=[ROOT / "web-ui/backend/hyperrag_cache"])
    try:
        transport = normalization.chat() if args.allow_api and normalization and args.request_budget else None
        embedder = EmbeddingTransport(embedding) if args.allow_api and embedding and args.embedding_request_budget else None
        result = asyncio.run(engine.run(args.stage, transport=transport, embedder=embedder,
            request_budget=args.request_budget, embedding_request_budget=args.embedding_request_budget))
        print(json.dumps({k: result.get(k) for k in ("status", "stage", "generation", "source_unchanged")}))
        return 0
    except IncompleteJob:
        print(json.dumps({"status": "partial", "detail": "Inspect target/progress.json for unfinished tasks or vectors"}))
        return 2
    finally:
        engine.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        # Never dump provider exceptions, keys, input text or Authorization.
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}), file=sys.stderr)
        raise SystemExit(1)
