import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import numpy as np
import pytest

from hyperrag import HyperRAG
from hyperrag import llm, operate
from hyperrag.storage import JsonKVStorage
from hyperrag.utils import EmbeddingFunc, compute_args_hash


def test_entity_parser_recovers_leading_empty_array_and_latex():
    response = '[]\n```json\n[{"name":"PFOS","type":"PFAS_TARGET","description":"\\mathrm{PFOS}"}]\n```'
    assert operate.parse_json_entities(response)[0]["name"] == "PFOS"
    assert not operate._is_valid_empty_entity_extraction(response)


def test_truncated_array_is_not_silently_recovered_as_one_entity():
    assert operate.parse_json_entities('[{"name":"PFOS","type":"PFAS_TARGET"},') == []
    assert not operate._is_valid_empty_entity_extraction("thinking... []")
    assert operate._is_valid_empty_entity_extraction("```json\n[]\n```")


def test_malformed_relationship_output_is_not_a_valid_empty_relation_set():
    with pytest.raises(ValueError):
        operate.parse_json_combined_relationships('model returned an error')
    assert operate.parse_json_combined_relationships(
        '{"low_order_relations": [], "high_order_hyperedges": []}'
    ) == ([], [])


def test_force_refresh_replaces_existing_cache_and_persists(tmp_path, monkeypatch):
    async def run():
        cache = JsonKVStorage(namespace="llm_response_cache", global_config={"working_dir": str(tmp_path)})
        key = compute_args_hash("model", [{"role": "user", "content": "prompt"}])
        await cache.upsert({key: {"return": "old malformed response", "model": "model"}})
        create = AsyncMock(return_value=SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="new response"))]))
        monkeypatch.setattr(llm, "AsyncOpenAI", lambda **kwargs: SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create))))
        assert await llm.openai_complete_if_cache("model", "prompt", hashing_kv=cache, force_cache_refresh=True) == "new response"
        await cache.index_done_callback()
        reloaded = JsonKVStorage(namespace="llm_response_cache", global_config={"working_dir": str(tmp_path)})
        assert (await reloaded.get_by_id(key))["return"] == "new response"
    asyncio.run(run())


def test_confirmed_empty_keeps_document_text_and_vector(tmp_path):
    calls = []

    async def complete(prompt, **kwargs):
        calls.append(kwargs.get("force_cache_refresh", False))
        return "[]"

    async def embed(texts):
        return np.ones((len(texts), 8), dtype=np.float32)

    async def run():
        rag = HyperRAG(working_dir=str(tmp_path), domain="pfas_piezocatalysis",
                       enable_one_pass_extraction=False, enable_entity_normalization=False,
                       enable_efu_repair=False, llm_model_func=complete,
                       embedding_func=EmbeddingFunc(embedding_dim=8, max_token_size=8192, func=embed))
        await rag.ainsert({"doc_id": "PFAS_001", "content": "Publisher copyright notice."})
        assert await rag.full_docs.get_by_id("PFAS_001")
        assert len(await rag.text_chunks.all_keys()) == 1
        assert len(rag.chunks_vdb._client.get(["PFAS_001_CHK_001"])) == 1
    asyncio.run(run())
    assert calls == [False, True]
    audit = json.loads((tmp_path / "empty_extraction_audit.jsonl").read_text(encoding="utf-8"))
    assert audit["status"] == "valid_empty_confirmed"


def test_failed_extraction_never_creates_chunk_only_vectors(tmp_path, monkeypatch):
    async def fail(*args, **kwargs):
        raise RuntimeError("network failure")

    async def embed(texts):
        raise AssertionError("embedding must not run before extraction succeeds")

    monkeypatch.setattr("hyperrag.hyperrag.extract_entities", fail)

    async def run():
        rag = HyperRAG(working_dir=str(tmp_path), enable_efu_repair=False,
                       embedding_func=EmbeddingFunc(embedding_dim=8, max_token_size=8192, func=embed))
        with pytest.raises(RuntimeError, match="network failure"):
            await rag.ainsert({"doc_id": "PFAS_001", "content": "PFOS degradation."})
        assert await rag.full_docs.all_keys() == []
        assert await rag.text_chunks.all_keys() == []
        assert rag.chunks_vdb._client.get(["PFAS_001_CHK_001"]) == []
    asyncio.run(run())


def test_malformed_empty_confirmation_remains_a_retryable_failure(tmp_path):
    async def complete(*args, **kwargs):
        return "not JSON"

    async def run():
        with pytest.raises(RuntimeError, match="entity extraction failed"):
            await operate._process_json_format_extraction(
                "PFOS degradation", "PFAS_001_CHK_001", complete,
                {"working_dir": str(tmp_path), "enable_one_pass_extraction": False},
                "pfas_piezocatalysis",
            )
    asyncio.run(run())
    assert not (tmp_path / "empty_extraction_audit.jsonl").exists()
