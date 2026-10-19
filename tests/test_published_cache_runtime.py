import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "web-ui" / "backend"))
from cache_runtime import apply_completed_cache_settings
from hyperrag.hyperrag import HyperRAG


def test_accepted_pfas_cache_keeps_build_profile_and_efu_off(tmp_path):
    settings = {"hyperrag_domain": "flow_battery", "enableEfuRepair": True, "modelName": "query-model"}
    (tmp_path / "publication_manifest.json").write_text(json.dumps({"validation_passed": True, "runtime_profile_locked": True}))
    (tmp_path / "run_config.json").write_text(json.dumps({"effective_domain": "pfas_piezocatalysis", "experiment_mode": "hyper_final",
        "prompt_profile": "chemistry", "index_profile": "dual_concat", "enable_efu_repair": False,
        "enable_entity_normalization": True, "enable_measurement_instances": True, "enable_hybrid_rerank": True}))
    result = apply_completed_cache_settings(settings, tmp_path)
    assert result["hyperrag_domain"] == "pfas_piezocatalysis"
    assert result["enableEfuRepair"] is False and result["_preserve_build_config"] is True
    assert result["indexProfile"] == "dual_concat" and result["modelName"] == "query-model"
    assert settings["enableEfuRepair"] is True


def test_unpublished_cache_retains_existing_runtime_choice(tmp_path):
    settings = {"hyperrag_domain": "flow_battery", "enableEfuRepair": True}
    assert apply_completed_cache_settings(settings, tmp_path) is settings
    (tmp_path / "publication_manifest.json").write_text(json.dumps({"validation_passed": False, "runtime_profile_locked": True}))
    assert apply_completed_cache_settings(settings, tmp_path) is settings


def test_loading_preserved_build_config_does_not_write_it(tmp_path, monkeypatch):
    import hyperrag.hyperrag as module
    from hyperrag.utils import EmbeddingFunc

    class Storage:
        def __init__(self, **kwargs):
            pass

    async def embed(texts):
        raise AssertionError("loading must not request embeddings")

    async def llm(*args, **kwargs):
        raise AssertionError("loading must not request the LLM")

    monkeypatch.setattr(module, "set_logger", lambda *args: None)
    config = tmp_path / "run_config.json"
    original = b'{"build_provenance":"accepted","enable_efu_repair":false}'
    config.write_bytes(original)
    rag = HyperRAG(working_dir=str(tmp_path), persist_run_config=False,
                   embedding_func=EmbeddingFunc(embedding_dim=2560, max_token_size=8192, func=embed),
                   llm_model_func=llm, key_string_value_json_storage_cls=Storage,
                   vector_db_storage_cls=Storage, hypergraph_storage_cls=Storage,
                   domain="pfas_piezocatalysis", enable_efu_repair=False)
    assert config.read_bytes() == original and not rag.enable_efu_repair
