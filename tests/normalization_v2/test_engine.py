import asyncio
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from hyperche.normalization_v2.engine import Engine, IncompleteJob, job_lease
from hyperche.normalization_v2.ledger import Ledger
from hyperche.normalization_v2.projections import RetrievalAdapter
from test_resolver import batch


CONFIG = Path(__file__).resolve().parents[2] / "configs/normalization_v2"


def create(tmp_path, raw=None, target=None):
    raw = raw or batch("PFOA")
    raw["mentions"][0]["kind"] = "chemical"
    source = tmp_path / "raw.jsonl"
    source.write_text(json.dumps(raw) + "\n", encoding="utf-8")
    engine = Engine(source=source, target=target or tmp_path / "v2", corpus_id="test", registry_paths=[CONFIG],
                    normalization_profile_hash="offline-profile", embedding_model="test-only", embedding_dimension=4,
                    expected_docs=1, expected_chunks=1)
    return engine, source


def test_end_to_end_import_resolve_embed_validate_publish_and_zero_call_resume(tmp_path):
    engine, source = create(tmp_path)
    original = source.read_bytes()
    calls = []
    async def embedding(texts, **kw):
        calls.append(len(texts))
        return np.ones((len(texts), 4))
    state = asyncio.run(engine.run("all", embedder=embedding, embedding_request_budget=1))
    assert state["status"] == "completed_and_published"
    assert state["identity_candidate_embedding_calls"] == 0
    assert len(RetrievalAdapter(engine.target).records) == 1
    counts = engine.ledger.counts()
    repeated = asyncio.run(engine.run("all", embedder=embedding, embedding_request_budget=0))
    assert repeated["generation"] == state["generation"] and calls == [1]
    assert engine.ledger.counts() == counts
    assert source.read_bytes() == original
    engine.close()


def test_insufficient_budget_and_missing_identity_work_do_not_publish(tmp_path):
    engine, source = create(tmp_path)
    with pytest.raises(IncompleteJob): asyncio.run(engine.run("all"))
    assert json.loads(engine.state_path.read_text())["status"] == "partial"
    assert not (engine.target / "current.json").exists()
    engine.close()


def test_live_job_lock_blocks_second_owner_and_finally_releases(tmp_path):
    with Ledger(tmp_path / "ledger.sqlite", "test") as ledger:
        with job_lease(ledger):
            with pytest.raises(IncompleteJob):
                with job_lease(ledger): pass
        with job_lease(ledger): pass


def test_ordinary_existing_target_and_source_target_overlap_reject(tmp_path):
    existing = tmp_path / "existing"
    existing.mkdir()
    (existing / "run_config.json").write_text('{"already_accepted":true}')
    before = (existing / "run_config.json").read_bytes()
    with pytest.raises(ValueError, match="non-v2"): create(tmp_path, target=existing)
    assert list(existing.iterdir()) == [existing / "run_config.json"]
    assert (existing / "run_config.json").read_bytes() == before


def test_failed_new_source_revision_does_not_displace_active_release(tmp_path):
    engine, source = create(tmp_path)
    async def embed(texts, **kw): return np.ones((len(texts), 4))
    first = asyncio.run(engine.run("all", embedder=embed, embedding_request_budget=1))
    bad = batch("PFOA")
    bad.update(revision_hash="new", extraction_id="failed-extraction", status="technical_failed", finish_reason="length")
    for mention in bad["mentions"]: mention.update(revision_hash="new", mention_id="failed-mention")
    source.write_text(json.dumps(bad) + "\n")
    with pytest.raises(IncompleteJob): asyncio.run(engine.run("all"))
    assert RetrievalAdapter(engine.target).manifest["generation"] == first["generation"]
    assert engine.ledger.db.execute("SELECT revision FROM sources WHERE status='active'").fetchone()[0] == "r1"
    engine.close()


def test_cli_compile_is_offline_and_no_budget_without_opt_in(tmp_path):
    root = Path(__file__).resolve().parents[2]
    cli = root / "scripts/normalize_registry_offline.py"
    result = subprocess.run([sys.executable, str(cli), "--stage", "compile"], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0
    assert json.loads(result.stdout)["status"] == "compiled"
    engine, source = create(tmp_path)
    engine.close()
    result = subprocess.run([sys.executable, str(cli), "--stage", "all", "--source", str(source),
                             "--target", str(tmp_path / "another"), "--corpus-id", "test",
                             "--offline-profile-id", "test", "--embedding-model", "test-only",
                             "--embedding-dimension", "4", "--request-budget", "1"], cwd=root, capture_output=True, text=True)
    assert result.returncode == 1
    assert not (tmp_path / "another").exists()
