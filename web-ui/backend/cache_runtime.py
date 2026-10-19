"""Preserve the accepted index profile when querying a published cache."""
import json
from pathlib import Path


def apply_completed_cache_settings(settings: dict, cache_dir: str | Path) -> dict:
    root = Path(cache_dir)
    manifest = root / "publication_manifest.json"
    if not manifest.exists():
        return settings
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    if not payload.get("validation_passed") or not payload.get("runtime_profile_locked"):
        return settings
    config = json.loads((root / "run_config.json").read_text(encoding="utf-8"))
    result = dict(settings)
    for runtime_key, build_key in {
        "hyperrag_domain": "effective_domain", "experimentMode": "experiment_mode",
        "promptProfile": "prompt_profile", "indexProfile": "index_profile",
        "enableEntityNormalization": "enable_entity_normalization",
        "enableMeasurementInstances": "enable_measurement_instances",
        "enableEfuRepair": "enable_efu_repair", "enableHybridRerank": "enable_hybrid_rerank",
    }.items():
        if build_key in config:
            result[runtime_key] = config[build_key]
    result.update(prompt_pack_id=None, prompt_version_id=None, _preserve_build_config=True)
    return result
