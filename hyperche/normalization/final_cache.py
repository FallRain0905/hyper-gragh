"""Build the agreed final cache from existing extraction and normalization.

No extraction or pair judgement calls are made here. Numerical occurrences are
resolved within their source chunk, and only existing edge endpoints are replaced.
"""
from __future__ import annotations

import asyncio
import copy
import hashlib
import json
import logging
import math
import re
import shutil
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from openai import AsyncOpenAI, APIConnectionError, APITimeoutError, APIStatusError

from . import posthoc_cache as core
from .alias_registry import AliasRegistry
from .entity_normalizer import EntityNormalizer, NormalizationResult
from .text_normalizer import normalize_text

VERSION = "final-posthoc-v2"
MODEL = "Qwen/Qwen3-Embedding-4B"
DIMENSION = 2560
LOGGER = logging.getLogger("hyper_rag.final_cache")


def _sources(data: dict) -> list[str]:
    return sorted(set(core.extract_ids(
        [data.get(k) for k in ("source_id", "source_chunk_id", "source_chunk_ids", "source_document_ids")],
        core.CHUNK_ID_PATTERN,
    )))


def _set_sources(data: dict, chunks: list[str]) -> None:
    chunks = sorted(set(chunks))
    docs = sorted({c.split("_CHK_", 1)[0] for c in chunks})
    data.update(source_id="<SEP>".join(chunks), source_chunk_id="<SEP>".join(chunks),
                source_chunk_ids=chunks, source_doc_id="<SEP>".join(docs), source_doc_ids=docs,
                source_document_ids=docs)


def cached_payload(text: str, *, two_step: bool = False) -> dict:
    """Repair JSON escaping only; never invent truncated extraction content."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    if two_step or text.startswith("["):
        # Two-step PFAS extraction returns a bare array. Some accepted responses
        # contain a leading [] followed by a complete populated array. Decode
        # all top-level values, never salvage nested objects from a truncated array.
        values, offset = [], 0
        while offset < len(text):
            value, end = json.JSONDecoder().raw_decode(text, offset)
            if not isinstance(value, list):
                raise ValueError("two-step entity response must contain arrays")
            values.append(value)
            offset = end
            while offset < len(text) and text[offset].isspace():
                offset += 1
        populated = [v for v in values if v]
        if len(populated) > 1 or not values:
            raise ValueError("ambiguous cached entity arrays")
        value = populated[0] if populated else []
        if any(not isinstance(e, dict) or not (e.get("name") or e.get("entity_name")) or not (e.get("type") or e.get("entity_type")) for e in value):
            raise ValueError("invalid cached entity schema")
        return {"entities": value}
    # Decode the entities array independently: old relation sections sometimes
    # contain invalid quotation marks although every entity is intact.
    match = re.search(r'"entities"\s*:\s*\[', text)
    if not match:
        raise ValueError("cached extraction has no entities array")
    array = text[match.end() - 1:]
    try:
        value, _ = json.JSONDecoder().raw_decode(array)
    except json.JSONDecodeError:
        repaired, index = [], 0
        while index < len(array):
            char = array[index]
            if char == "\\" and index + 1 < len(array):
                following = array[index + 1]
                valid = following in '"\\/bfnrt' or (following == "u" and
                         re.fullmatch(r"[0-9a-fA-F]{4}", array[index + 2:index + 6]))
                repaired.append(("\\" if valid else "\\\\") + following)
                index += 2
            else:
                repaired.append(char)
                index += 1
        array = re.sub(r",\s*([}\]])", r"\1", "".join(repaired))
        value, _ = json.JSONDecoder().raw_decode(array)
    if not isinstance(value, list):
        raise ValueError("cached extraction entities is not an array")
    return {"entities": value}


def build_chunk_map(source: Path) -> dict:
    """Reproduce exact extraction cache keys without making provider requests."""
    from hyperrag.prompt import get_entity_extraction_prompt
    from hyperrag.utils import compute_args_hash
    config = core._load_json_dict(source / "run_config.json")
    chunks = core._load_json_dict(source / "kv_store_text_chunks.json")
    responses = core._load_json_dict(source / "kv_store_llm_response_cache.json")
    model = config["llm"]["model"]
    domain = config.get("effective_domain") or config["domain"]
    mapped = {}
    for cid, chunk in sorted(chunks.items()):
        prompt = get_entity_extraction_prompt(domain=domain, CHUNK_TEXT=chunk["content"])
        key = compute_args_hash(model, [{"role": "user", "content": prompt}])
        response = responses.get(key)
        if not response or response.get("model") != model or not isinstance(response.get("return"), str):
            raise ValueError(f"no matching cached entity response: {cid}")
        mapped[cid] = [{"cache_key": key, "stage": "entity", "model": model,
                        "content_sha256": hashlib.sha256(chunk["content"].encode()).hexdigest(),
                        "response_sha256": hashlib.sha256(response["return"].encode()).hexdigest()}]
    return {"mapped": mapped, "domain": domain, "model": model,
            "method": "exact get_entity_extraction_prompt/model/messages hash"}


def _pfas_local_instance(entity: dict, canonical: dict | None) -> tuple[dict | None, str]:
    """Bind a scalar/range to its accepted PFAS cluster and explicit local fields.

    Keep pollutant identities and quantities from different canonical clusters
    separate. Units are retained without converting magnitudes. Descriptions,
    chemical-formula digits and unit powers never supply measurement values.
    """
    name = str(entity.get("name") or entity.get("entity_name") or "").strip()
    typ = str(entity.get("type") or entity.get("entity_type") or "").upper()
    if typ not in {"METRIC", "CONDITION", "PIEZO_PROPERTY", "PERFORMANCE_METRIC", "OPERATING_CONDITION"}:
        return None, "non_numeric_type"
    numeric = {}
    for field in ("value", "value_min", "value_max"):
        value = entity.get(field)
        if value is None:
            numeric[field] = None
            continue
        if isinstance(value, bool):
            return None, "invalid_numeric_field"
        try:
            numeric[field] = float(value)
        except (TypeError, ValueError, OverflowError):
            return None, "invalid_numeric_field"
        if not math.isfinite(numeric[field]):
            return None, "invalid_numeric_field"
    scalar, lower, upper = (numeric[k] for k in ("value", "value_min", "value_max"))
    if scalar is None and lower is None and upper is None:
        return None, "no_explicit_local_value"
    if (lower is None) != (upper is None):
        return None, "partial_range_preserved"
    if lower is not None:
        if lower > upper:
            return None, "invalid_range"
        if scalar is not None:
            return None, "scalar_and_range_preserved"
    surface = re.findall(r"(?<![\w.^])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?(?![\w.])", name)
    if scalar is not None and surface:
        if len(surface) != 1 or not math.isclose(float(surface[0]), scalar, rel_tol=1e-12, abs_tol=1e-12):
            return None, "surface_structured_value_conflict"
    unit = str(entity.get("unit") or "").strip().replace("µ", "μ").replace("−", "-")
    values = [v for v in (scalar, lower, upper) if v is not None]
    is_ph = re.search(r"\bpH\b", name, flags=re.I) is not None
    if is_ph:
        if unit.lower() not in ("", "ph") or any(v < 0 or v > 14 for v in values):
            return None, "ph_unit_or_value_conflict"
        unit = ""
    elif not unit:
        return None, "numeric_unit_missing"
    if unit == "%" and re.search(r"removal|degrad|defluorin|mineraliz|efficiency|yield|conversion", name, re.I) and any(v < 0 or v > 100 for v in values):
        return None, "percentage_value_conflict"
    # The accepted cluster ID includes all existing PFAS identity safeguards,
    # including suffixes that distinguish independent case-only clusters.
    cid = (canonical or {}).get("canonical_id") or (typ.lower() + ":" + core.stable_hash(name, 20))
    label = (canonical or {}).get("canonical_name") or name
    identity = {"canonical_id": cid, "value": scalar, "min_value": lower, "max_value": upper, "unit": unit}
    method = "condition_instance" if typ in {"CONDITION", "OPERATING_CONDITION"} or is_ph else "measurement_instance"
    prefix = "condition" if method == "condition_instance" else "measurement"
    node = f"{prefix}:pfas:{core.stable_hash(core.json_hash(identity), 24)}"
    result = NormalizationResult(original_entity_id=name, original_name=name, entity_type=typ,
                                 decision="MERGE", canonical_id=cid, canonical_name=label,
                                 confidence=1.0, method=method, node_id=node, instance_id=node,
                                 raw_mention=name, semantic_group="pfas_local_quantity",
                                 value=scalar, min_value=lower, max_value=upper, unit=unit or None,
                                 reason="Explicit chunk-local quantity; accepted cluster identity and units preserved.")
    return result.to_dict(), method


def local_instance(entity: dict, normalizer: EntityNormalizer, *, domain: str = "flow_battery",
                   canonical: dict | None = None) -> tuple[dict | None, str]:
    """Use local numeric fields, excluding description numbers and other facts."""
    if domain == "pfas_piezocatalysis":
        return _pfas_local_instance(entity, canonical)
    name = str(entity.get("name") or entity.get("entity_name") or "").strip()
    typ = str(entity.get("type") or entity.get("entity_type") or "").upper()
    if typ not in {"METRIC", "CONDITION", "PERFORMANCE_METRIC", "OPERATING_CONDITION", "PIEZO_PROPERTY"}:
        return None, "non_numeric_type"
    numeric = {k: entity.get(k) for k in ("value", "value_min", "value_max")}
    for k, value in numeric.items():
        if value is not None:
            try:
                numeric[k] = float(value)
                if not math.isfinite(numeric[k]):
                    return None, "invalid_numeric_field"
            except (ValueError, TypeError):
                return None, "invalid_numeric_field"
    readable = normalize_text(name)
    # Exclude digits embedded in formulas and unit powers (H2SO4, cm2).
    numbers = re.findall(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?![\d.])", readable)
    if all(v is None for v in numeric.values()) and len(numbers) != 1:
        return None, "no_unambiguous_local_value"
    if len(numbers) > 1 and numeric["value"] is not None:
        return None, "multiple_surface_values"
    if (numeric["value_min"] is None) != (numeric["value_max"] is None):
        return None, "partial_range_preserved"
    if numeric["value"] is None and any(numeric[k] is not None for k in ("value_min", "value_max")):
        # Existing range IDs are implemented for conditions; do not flatten a
        # metric range to one endpoint or expand paired measurements.
        if typ in {"METRIC", "PERFORMANCE_METRIC", "PIEZO_PROPERTY"}:
            return None, "metric_range_preserved"
    local = {"name": name, "entity_name": name, "type": typ, "unit": entity.get("unit") or "", **numeric}
    result = normalizer._try_measurement_or_condition_instance(local, name, typ, name)
    if result is None:
        return None, "unsupported_quantity"
    if result.min_value is not None and result.max_value is not None:
        # A range has two endpoints; a number in a formula/name is not a third
        # scalar observation (e.g. H2SO4 in a concentration range).
        result.value = None
    values = [v for v in (result.value, result.min_value, result.max_value) if v is not None]
    if result.canonical_id == "condition:ph":
        if local["unit"] not in ("", "pH", "ph") or any(v < 0 or v > 14 for v in values):
            return None, "ph_unit_or_value_conflict"
    if result.canonical_id in {"metric:ce", "metric:ve", "metric:ee", "metric:capacity_retention"}:
        if any(v < 0 or v > 100 for v in values):
            return None, "efficiency_value_conflict"
    if result.canonical_id == "metric:energy_density" and not local["unit"]:
        return None, "energy_density_unit_missing"
    if result.min_value is None and numeric["value"] is not None and result.value != numeric["value"]:
        return None, "surface_structured_value_conflict"
    if result.min_value is not None and result.max_value is not None and result.min_value > result.max_value:
        return None, "invalid_range"
    return result.to_dict(), result.method


def _resolve(name: str, names: set[str]) -> str | None:
    if name in names:
        return name
    exact = [n for n in names if n.strip() == name.strip()]
    return exact[0] if len(exact) == 1 else None


def rewrite_final_graph(source_graph: dict, normalized_graph: dict, canonical_map: dict,
                        extracted: dict[str, list[dict]], *, domain: str = "flow_battery") -> tuple[dict, dict, list, dict]:
    from hyperrag.utils import compute_mdhash_id
    source_vertices = source_graph["v_data"]
    mapping = canonical_map["entities"]
    vertices = copy.deepcopy(normalized_graph["v_data"])
    for node, data in vertices.items():
        data["node_id"] = node
        data["raw_name"] = "<SEP>".join(data.get("aliases") or [data.get("canonical_name") or node])
        data["source_mentions"] = data.get("aliases") or [data.get("canonical_name") or node]
        _set_sources(data, _sources(data))
    by_chunk: dict[str, set[str]] = defaultdict(set)
    for raw, data in source_vertices.items():
        for chunk in _sources(data):
            by_chunk[chunk].add(raw)
    normalizer = EntityNormalizer(AliasRegistry())
    local: dict[tuple[str, str], str] = {}
    occurrences: list[dict] = []
    reasons = Counter()
    for chunk, entities in sorted(extracted.items()):
        candidates: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
        for entity in entities:
            raw = _resolve(str(entity.get("name") or entity.get("entity_name") or ""), by_chunk[chunk])
            if raw is None:
                reasons["raw_entity_not_in_source_chunk"] += 1
                continue
            result, reason = local_instance(entity, normalizer, domain=domain, canonical=mapping[raw])
            reasons[reason] += 1
            if result:
                candidates[raw].append((entity, result))
        for raw, entries in candidates.items():
            if len({core.json_hash({k: r[k] for k in ("node_id", "value", "min_value", "max_value", "unit")}) for _, r in entries}) != 1:
                reasons["ambiguous_same_chunk_same_name"] += 1
                continue
            entity, result = entries[0]
            node = result["node_id"]
            if node in normalized_graph["v_data"]:
                # Historical cluster slugs can spell the same string as a new
                # numerical instance. Keep the two identities separate unless
                # the old cluster is later proven fully replaced.
                result = dict(result)
                result["base_instance_id"] = node
                node += ":instance"
                result["node_id"] = result["instance_id"] = node
                reasons["instance_id_disambiguated"] += 1
            identity = {"canonical_id": result["canonical_id"], "value": result["value"],
                        "value_min": result["min_value"], "value_max": result["max_value"], "unit": result["unit"]}
            if node in vertices and any(vertices[node].get(k) != v for k, v in identity.items()):
                result = dict(result)
                node += ":" + core.stable_hash(core.json_hash(identity))
                result["node_id"] = result["instance_id"] = node
                reasons["numeric_signature_disambiguated"] += 1
            occurrence = {"source_chunk_id": chunk, "raw_vertex": raw,
                          "raw_entity": entity, "normalization": result}
            occurrences.append(occurrence)
            local[chunk, raw] = node
            incoming = {
                "node_id": node, "entity_name": node, "instance_id": node,
                "canonical_id": result["canonical_id"], "canonical_name": result["canonical_name"],
                "entity_type": str(entity.get("type") or "UNKNOWN"),
                "semantic_group": result["semantic_group"], "normalization_method": result["method"],
                "normalization_confidence": 1.0, "value": result["value"], "unit": result["unit"],
                "value_min": result["min_value"], "value_max": result["max_value"],
                "raw_name": raw, "source_mentions": [raw], "legacy_vertex_ids": [raw],
                "description": str(entity.get("description") or ""),
                "source_chunk_ids": [chunk], "measurement_occurrences": [occurrence],
            }
            if node in vertices and vertices[node].get("instance_id") != node:
                raise ValueError(f"instance ID collides with a canonical cluster: {node}")
            vertices[node] = core._merge_metadata(vertices.get(node), incoming)
    edges = {}
    edge_audit = []
    collapsed = 0
    for source_key, edge in sorted(source_graph["e_data"].items()):
        originals = set(source_key)
        instances = edge.get("evidence_instances") or []
        if not instances:
            raise ValueError(f"Source edge has no evidence instances: {source_key}")
        for index, instance in enumerate(instances):
            chunks = _sources(instance)
            if len(chunks) != 1:
                raise ValueError("each source evidence instance must have exactly one chunk")
            chunk = chunks[0]
            raw_vertices = instance.get("vertices") or []
            resolved = [_resolve(str(raw), originals) for raw in raw_vertices]
            if not resolved or any(raw is None for raw in resolved):
                raise ValueError(f"evidence endpoint not in source edge: {chunk} {raw_vertices}")
            mapped = sorted({local.get((chunk, raw), mapping[raw]["canonical_id"]) for raw in resolved})
            audit = {"source_edge_vertices": list(source_key), "source_instance_index": index,
                     "source_chunk_id": chunk, "raw_vertices": list(raw_vertices), "resolved_vertices": resolved,
                     "final_vertices": mapped, "collapsed": len(mapped) < 2}
            edge_audit.append(audit)
            if len(mapped) < 2:
                collapsed += 1
                continue
            key = tuple(mapped)
            stored_instance = copy.deepcopy(instance)
            stored_instance["canonical_vertices"] = mapped
            incoming = {
                "vertices": mapped, "node_ids": mapped, "canonical_vertices": mapped,
                "evidence_instances": [stored_instance], "legacy_vertex_sets": [list(source_key)],
                "description": str(instance.get("description") or ""),
                "keywords": str(instance.get("keywords") or ""),
                "relation_type": str(instance.get("relation_type") or edge.get("relation_type") or "RELATION"),
                "source_chunk_ids": [chunk], "source_spans": [instance.get("source_span") or instance.get("evidence_span") or ""],
                "weight": float(instance.get("weight") or 0), "repair_applied": False, "repair_rules": [],
            }
            if key in edges:
                weight = float(edges[key]["weight"]) + incoming["weight"]
                edges[key] = core._merge_metadata(edges[key], incoming)
                edges[key]["weight"] = weight
            else:
                edges[key] = incoming
    used = {n for key in edges for n in key}
    # Remove an old numerical cluster only if all its source occurrences were
    # replaced. Non-numerical and unresolved source entities remain available.
    removed = []
    for cluster in canonical_map["clusters"]:
        cid = cluster["canonical_id"]
        pairs = [(chunk, raw) for raw in cluster["members"] for chunk in _sources(source_vertices[raw])]
        if cid not in used and pairs and all(pair in local for pair in pairs):
            vertices.pop(cid, None)
            removed.append(cid)
    for node, data in vertices.items():
        _set_sources(data, _sources(data))
        for field in ("description", "additional_properties", "raw_name", "entity_type", "semantic_group"):
            if isinstance(data.get(field), list):
                data[field] = "<SEP>".join(map(str, core._unique_values(data[field])))
    for key, data in edges.items():
        _set_sources(data, _sources(data))
        for field in ("description", "keywords", "relation_type"):
            data[field] = "<SEP>".join(map(str, core._unique_values(core._value_list(data.get(field)))))
        data["source_span"] = data["evidence_span"] = next(iter(data["source_spans"]), "")
        data["efu_id"] = compute_mdhash_id("|".join(key) + "|" + data["relation_type"], prefix="efu-")
    summary = {"entities": len(vertices), "relationships": len(edges),
               "measurement_nodes": sum(d.get("normalization_method") == "measurement_instance" for d in vertices.values()),
               "condition_nodes": sum(d.get("normalization_method") == "condition_instance" for d in vertices.values()),
               "instance_occurrences": len(occurrences), "collapsed_evidence_instances": collapsed,
               "removed_replaced_numeric_clusters": len(removed), "instance_decision_counts": dict(reasons)}
    return vertices, edges, occurrences, {"summary": summary, "edge_audit": edge_audit}


def build_dual_records(work: Path) -> tuple[dict, dict]:
    from hyperrag.operate import _build_entity_embedding_text, _build_relationship_embedding_text, _build_dual_embedding_text
    from hyperrag.utils import compute_mdhash_id, relationship_vector_id
    graph = core.load_graph(work)
    entities, relationships = {}, {}
    for node, data in sorted(graph["v_data"].items()):
        canonical = _build_entity_embedding_text(data, view="canonical")
        surface = _build_entity_embedding_text(data, view="surface")
        content = _build_dual_embedding_text(canonical, surface)
        entities[compute_mdhash_id(node, prefix="ent-")] = {
            "entity_name": node, "canonical_id": data.get("canonical_id") or node,
            "canonical_name": data.get("canonical_name") or node, "entity_type": data.get("entity_type"),
            "content": content, "canonical_text": canonical, "surface_text": surface,
            "content_hash": core.json_hash(content), "index_view": "dual_concat",
            "embedding_model": MODEL, "embedding_dim": DIMENSION,
        }
    for key, data in sorted(graph["e_data"].items()):
        labels = [str(graph["v_data"][n].get("canonical_name") or n) +
                  (f" [{n}]" if graph["v_data"][n].get("instance_id") else "") for n in key]
        dp = {**data, "id_set": list(key), "node_ids": labels}
        canonical = _build_relationship_embedding_text(dp, view="canonical")
        surface = _build_relationship_embedding_text(dp, view="surface")
        content = _build_dual_embedding_text(canonical, surface)
        relationships[relationship_vector_id(key)] = {
            "id_set": list(key), "canonical_names": labels, "relation_type": data["relation_type"],
            "source_doc_id": data["source_doc_id"], "source_chunk_id": data["source_chunk_id"],
            "content": content, "canonical_text": canonical, "surface_text": surface,
            "content_hash": core.json_hash(content), "index_view": "dual_concat",
            "embedding_model": MODEL, "embedding_dim": DIMENSION,
        }
    return entities, relationships


def prepare_final(source: Path, normalized: Path, work: Path, chunk_map: Path) -> dict:
    source_config = core._load_json_dict(source / "run_config.json")
    source_embedding = source_config.get("embedding") or {}
    if (source_config.get("embedding_model") or source_embedding.get("model")) != MODEL:
        raise ValueError("source chunks were built with a different embedding model")
    norm_state = core._load_json_dict(normalized / "normalization_state.json")
    if (norm_state.get("stages", {}).get("validate", {}).get("status") != "completed"
            or not norm_state["stages"]["validate"].get("details", {}).get("validation_passed")
            or core._unresolved_cluster_audits(normalized)):
        raise ValueError("normalization cache has not passed validation")
    source_graph, normalized_graph = core.load_graph(source), core.load_graph(normalized)
    canonical_map = core._load_json_dict(normalized / "canonical_entity_map.json")
    responses = core._load_json_dict(source / "kv_store_llm_response_cache.json")
    cm = core._load_json_dict(chunk_map)
    chunks = core._load_json_dict(source / "kv_store_text_chunks.json")
    domain = source_config.get("effective_domain") or source_config.get("domain", "flow_battery")
    is_pfas = domain == "pfas_piezocatalysis"
    expected_map = build_chunk_map(source) if is_pfas else None
    if expected_map and cm != expected_map:
        raise ValueError("cached entity chunk map differs from exact extraction prompt hashes")
    extracted, unavailable = {}, []
    confirmed_empty = []
    for chunk in chunks:
        refs = cm.get("mapped", {}).get(chunk) or []
        if len(refs) != 1:
            unavailable.append({"chunk_id": chunk, "reason": "no_unique_cached_response"})
            continue
        try:
            text = responses[refs[0]["cache_key"]]["return"]
            payload = cached_payload(text, two_step=is_pfas)
            if is_pfas and not payload["entities"]:
                from hyperrag.operate import _has_confirmed_empty_extraction, _is_valid_empty_entity_extraction
                if not (_is_valid_empty_entity_extraction(text) and _has_confirmed_empty_extraction(
                        {"working_dir": str(source)}, chunk, chunks[chunk]["content"], text)):
                    raise ValueError("empty entity response has no unchanged provider-confirmation evidence")
                confirmed_empty.append(chunk)
            limit = source_config.get("max_entities_per_chunk", 0)
            extracted[chunk] = payload["entities"][:limit] if limit > 0 else payload["entities"]
        except (ValueError, KeyError) as exc:
            unavailable.append({"chunk_id": chunk, "reason": str(exc)})
    if unavailable:
        core.write_json(work / "unavailable_cached_extractions.json", {"chunks": unavailable})
        raise ValueError(f"{len(unavailable)} source chunks lack a complete audited entity response")
    immutable = core.copy_immutable_files(source, work)
    for name in ("canonical_entity_map.json", "normalization_decisions.jsonl", "normalization_candidates.jsonl",
                 "normalization_cluster_audit.jsonl", "normalization_audit.jsonl", "canonical_id_repair.json"):
        if (normalized / name).exists():
            shutil.copy2(normalized / name, work / name)
    if (source / "empty_extraction_audit.jsonl").exists():
        shutil.copy2(source / "empty_extraction_audit.jsonl", work / "empty_extraction_audit.jsonl")
    vertices, edges, occurrences, details = rewrite_final_graph(source_graph, normalized_graph, canonical_map, extracted, domain=domain)
    core._write_graph_file(work / core.GRAPH_FILE, vertices, edges)
    core.write_jsonl(work / "measurement_occurrences.jsonl", occurrences)
    core.write_jsonl(work / "final_edge_rewrite_audit.jsonl", details["edge_audit"])
    summary = {**details["summary"], "cached_extraction_chunks": len(extracted),
               "unavailable_cached_extractions": unavailable, "immutable_file_hashes": immutable,
               "provider_confirmed_empty_chunks": confirmed_empty,
               "extraction_api_requests": 0, "pair_judgement_api_requests": 0,
               "normalization_cache": str(normalized),
               "normalization_map_sha256": core.file_sha256(normalized / "canonical_entity_map.json"),
               "normalization_judge_api_errors_preserved": norm_state.get("stages", {}).get("judge", {}).get("details", {}).get("api_errors", 0)}
    target = work.with_name(work.name.removesuffix(".work"))
    config = {**source_config, "parent_cache": str(source), "normalization_cache": str(normalized),
              "experiment_mode": "hyper_final", "corpus_id": target.name, "cache_dir": str(target),
              "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "corpus_manifest_path": str(target / "corpus_manifest.jsonl"),
              "build_progress_path": str(target / "build_progress.jsonl"),
              "normalization_version": VERSION, "enable_entity_normalization": True,
              "enable_measurement_instances": True, "enable_efu_repair": False,
              "enable_hybrid_rerank": True, "index_profile": "dual_concat",
              "embedding_model": MODEL, "embedding_dim": DIMENSION,
              "embedding": {"model": MODEL, "base_url": "https://api.siliconflow.cn/v1", "embedding_dim": DIMENSION, "api_key_count": 10, "max_async": 10, "batch_num": 16},
              "embedding_provenance": {"chunks": "copied unchanged from chemistry cache",
                                       "entities": MODEL, "relationships": MODEL},
              "measurement_value_source": "chunk-local cached extraction; ambiguous values preserved unsplit"}
    core.write_json(work / "run_config.json", config)
    core.write_json(work / "final_prepare_summary.json", summary)
    entities, relationships = build_dual_records(work)
    core.write_json(work / "embedding_records.json", {"entities": entities, "relationships": relationships})
    return summary


async def embed_final(work: Path, endpoints: list[tuple[str, str]], *, concurrency: int = 10,
                      batch_size: int = 16, timeout: float = 120) -> dict:
    """Persistent clients and per-key lanes; successful batches checkpointed.

    Checkpoint records contain the model signature. A wave writes a compact
    binary shard, avoiding an increasingly large JSON rewrite every 80 vectors.
    """
    import pickle
    if not endpoints or len(set(endpoints)) != len(endpoints) or not 1 <= concurrency <= min(10, len(endpoints)):
        raise ValueError("embedding requires unique credentials and at most ten concurrent requests")
    records = core._load_json_dict(work / "embedding_records.json")
    signature = {"version": VERSION, "model": MODEL, "dimension": DIMENSION,
                 "records_hash": core.json_hash(records)}
    signature_path = work / "embedding_signature.json"
    if signature_path.exists() and core._load_json_dict(signature_path) != signature:
        raise ValueError("embedding checkpoint model/content signature differs; choose a new work directory")
    core.write_json(signature_path, signature)
    shard_dir = work / "embedding_checkpoints"
    shard_dir.mkdir(exist_ok=True)
    stored = {"entities": {}, "relationships": {}}
    for path in sorted(shard_dir.glob("*.pkl")):
        with path.open("rb") as handle:
            shard = pickle.load(handle)
        if shard["signature"] != signature:
            raise ValueError("incompatible embedding checkpoint")
        for kind in stored:
            stored[kind].update(shard.get(kind, {}))
    stats = {"requests": 0, "errors": 0, "network_active": 0, "network_peak": 0,
             "key_usage": {str(i + 1): {"requests": 0, "successes": 0, "errors": 0, "active": 0, "peak": 0} for i in range(len(endpoints))}}
    clients = [AsyncOpenAI(api_key=key, base_url=url, timeout=timeout, max_retries=0) for url, key in endpoints]
    key_locks = [asyncio.Semaphore(1) for _ in clients]
    started = time.monotonic()
    serial = 0
    semaphore = asyncio.Semaphore(concurrency)
    async def batch_call(kind, batch, index):
        async with semaphore:
            for attempt in range(len(clients)):
                slot = (index + attempt) % len(clients)
                usage = stats["key_usage"][str(slot + 1)]
                async with key_locks[slot]:
                    stats["requests"] += 1
                    usage["requests"] += 1
                    stats["network_active"] += 1
                    stats["network_peak"] = max(stats["network_peak"], stats["network_active"])
                    usage["active"] += 1
                    usage["peak"] = max(usage["peak"], usage["active"])
                    try:
                        response = await asyncio.wait_for(clients[slot].embeddings.create(
                            model=MODEL, input=[d["content"] for _, d in batch],
                            dimensions=DIMENSION, encoding_format="float"), timeout=timeout)
                        data = sorted(response.data, key=lambda r: r.index)
                        if [r.index for r in data] != list(range(len(batch))):
                            raise ValueError("embedding response indexes are missing or duplicated")
                        vectors = np.asarray([r.embedding for r in data], dtype=np.float32)
                        if vectors.shape != (len(batch), DIMENSION) or not np.isfinite(vectors).all():
                            raise ValueError(f"invalid embedding response: {vectors.shape}")
                        usage["successes"] += 1
                        return kind, {vid: (meta, vectors[j]) for j, (vid, meta) in enumerate(batch)}
                    except (APIConnectionError, APITimeoutError, asyncio.TimeoutError, APIStatusError, ValueError) as exc:
                        stats["errors"] += 1
                        usage["errors"] += 1
                        # Keys with quota/auth errors can fall through to another
                        # key; malformed input should fail directly.
                        code = getattr(exc, "status_code", None)
                        LOGGER.warning("embedding key=%s batch=%s status=%s error=%s", slot + 1, index, code, type(exc).__name__)
                        if isinstance(exc, ValueError) or code == 400 or attempt + 1 == len(clients):
                            raise
                    finally:
                        stats["network_active"] -= 1
                        usage["active"] -= 1
            raise RuntimeError("embedding pool exhausted")
    try:
        jobs = []
        for kind in stored:
            pending = [(vid, meta) for vid, meta in sorted(records[kind].items()) if vid not in stored[kind]]
            jobs.extend((kind, pending[i:i + batch_size]) for i in range(0, len(pending), batch_size))
        for offset in range(0, len(jobs), concurrency):
            wave = jobs[offset:offset + concurrency]
            results = await asyncio.gather(*(batch_call(kind, batch, offset + i) for i, (kind, batch) in enumerate(wave)), return_exceptions=True)
            shard = {"signature": signature, "entities": {}, "relationships": {}}
            errors = []
            for result in results:
                if isinstance(result, BaseException):
                    errors.append(result)
                else:
                    kind, rows = result
                    stored[kind].update(rows)
                    shard[kind].update(rows)
            while (shard_dir / f"batch_{serial:06d}.pkl").exists():
                serial += 1
            path = shard_dir / f"batch_{serial:06d}.pkl"
            tmp = path.with_suffix(".tmp")
            with tmp.open("wb") as handle:
                pickle.dump(shard, handle, protocol=pickle.HIGHEST_PROTOCOL)
            tmp.replace(path)
            progress = {"completed": {k: len(v) for k, v in stored.items()},
                        "total": {k: len(v) for k, v in records.items()},
                        "elapsed_seconds": round(time.monotonic() - started, 1), "concurrency": concurrency,
                        "active_keys": len(clients), "api_statistics": stats}
            core.write_json(work / "embedding_progress.json", progress)
            LOGGER.info("embedded entities=%s/%s relationships=%s/%s requests=%s errors=%s", len(stored["entities"]),
                        len(records["entities"]), len(stored["relationships"]), len(records["relationships"]), stats["requests"], stats["errors"])
            if errors:
                raise RuntimeError(f"{len(errors)} embedding batches failed; successes checkpointed; {type(errors[0]).__name__}")
        for kind in stored:
            if set(stored[kind]) != set(records[kind]):
                raise ValueError(f"incomplete embedding records: {kind}")
            core._write_vector_file(work / f"vdb_{kind}.json", stored[kind], DIMENSION)
        return {"entities": len(stored["entities"]), "relationships": len(stored["relationships"]), "api_statistics": stats}
    finally:
        await asyncio.gather(*(client.close() for client in clients))


def validate_final(source: Path, normalized: Path, work: Path, *, expected_docs: int = 60, expected_chunks: int = 1328) -> dict:
    failures = []
    graph = core.load_graph(work)
    vertices, edges = graph["v_data"], graph["e_data"]
    config = core._load_json_dict(work / "run_config.json")
    if core._unresolved_cluster_audits(normalized) or core._unresolved_cluster_audits(work):
        failures.append("unresolved normalization cluster audits")
    for key, expected in {"enable_entity_normalization": True, "enable_measurement_instances": True,
                          "enable_efu_repair": False, "index_profile": "dual_concat", "embedding_model": MODEL,
                          "embedding_dim": DIMENSION}.items():
        if config.get(key) != expected:
            failures.append(f"wrong run_config {key}")
    state = core._load_json_dict(work / "normalization_state.json")
    if state["source_checksums"] != core.source_checksums(source):
        failures.append("original source cache changed")
    for name in core.IMMUTABLE_FILES:
        if core.file_sha256(source / name) != core.file_sha256(work / name):
            failures.append(f"immutable file changed: {name}")
    if core.file_sha256(normalized / "canonical_entity_map.json") != core.file_sha256(work / "canonical_entity_map.json"):
        failures.append("canonical judgement map changed")
    docs = core._load_json_dict(work / "kv_store_full_docs.json")
    chunks = core._load_json_dict(work / "kv_store_text_chunks.json")
    if len(docs) != expected_docs or len(chunks) != expected_chunks:
        failures.append("document/chunk count mismatch")
    chunk_dimension, chunk_vectors = core._load_vector_file(work / "vdb_chunks.json")
    if chunk_dimension != DIMENSION or set(chunk_vectors) != set(chunks) or any(v.shape != (DIMENSION,) or not np.isfinite(v).all() for _, v in chunk_vectors.values()):
        failures.append("invalid chunk vector IDs, dimensions or values")
    del chunk_vectors
    for filename in ("normalization_decisions.jsonl", "normalization_candidates.jsonl", "normalization_audit.jsonl"):
        if (normalized / filename).exists() and (not (work / filename).exists() or core.file_sha256(normalized / filename) != core.file_sha256(work / filename)):
            failures.append(f"normalization history changed: {filename}")
    entity_records, relation_records = build_dual_records(work)
    for kind, records in (("entities", entity_records), ("relationships", relation_records)):
        dimension, stored = core._load_vector_file(work / f"vdb_{kind}.json")
        if dimension != DIMENSION or set(stored) != set(records):
            failures.append(f"{kind} vectors do not match graph")
        for vid, (meta, vector) in stored.items():
            if meta.get("embedding_model") != MODEL or meta.get("content_hash") != records.get(vid, {}).get("content_hash"):
                failures.append(f"{kind} stale model/content: {vid}")
                break
            if "[Canonical]" not in meta.get("content", "") or "[Surface]" not in meta.get("content", ""):
                failures.append(f"missing dual text: {vid}")
                break
            if vector.shape != (DIMENSION,) or not np.isfinite(vector).all() or float(np.linalg.norm(vector)) <= 0:
                failures.append(f"invalid vector: {vid}")
                break
    local = {(r["source_chunk_id"], r["raw_vertex"]): r["normalization"]["node_id"]
             for r in core.read_jsonl(work / "measurement_occurrences.jsonl")}
    mapping = core._load_json_dict(work / "canonical_entity_map.json")["entities"]
    audit = core.read_jsonl(work / "final_edge_rewrite_audit.jsonl")
    source_graph = core.load_graph(source)
    source_instances = sum(len(e.get("evidence_instances") or []) for e in source_graph["e_data"].values())
    if len(audit) != source_instances:
        failures.append("source evidence instances were lost")
    for row in audit:
        if not set(row["resolved_vertices"]).issubset(row["source_edge_vertices"]):
            failures.append("new endpoint added to existing relation")
            break
        expected = sorted({local.get((row["source_chunk_id"], raw), mapping[raw]["canonical_id"]) for raw in row["resolved_vertices"]})
        if row["final_vertices"] != expected or len(expected) > len(row["raw_vertices"]):
            failures.append("numeric relation endpoints not locally bound")
            break
    for key, edge in edges.items():
        if any(node not in vertices for node in key) or not isinstance(edge.get("source_id"), str):
            failures.append("invalid graph endpoint or source field")
            break
        if not _sources(edge) or not set(_sources(edge)).issubset(chunks) or edge.get("repair_applied"):
            failures.append("invalid edge source or EFU repair")
            break
        for instance in edge.get("evidence_instances") or []:
            if instance.get("repair_applied") or set(instance.get("canonical_vertices") or []) != set(key):
                failures.append("repair applied or evidence bound to wrong edge")
                break
    for node, data in vertices.items():
        if not _sources(data) or not set(_sources(data)).issubset(chunks):
            failures.append(f"invalid vertex source: {node}")
            break
        if data.get("instance_id") and any(isinstance(data.get(k), list) for k in ("canonical_id", "value", "value_min", "value_max", "unit")):
            failures.append(f"multiple values merged into a single instance: {node}")
            break
        if config.get("effective_domain") == "pfas_piezocatalysis" and data.get("instance_id"):
            for occurrence in data.get("measurement_occurrences") or []:
                raw = occurrence["raw_vertex"]
                if data.get("canonical_id") != mapping[raw]["canonical_id"]:
                    failures.append(f"PFAS instance lost accepted cluster identity: {node}")
                    break
    prepared = core._load_json_dict(work / "final_prepare_summary.json")
    if prepared.get("unavailable_cached_extractions") or prepared.get("cached_extraction_chunks") != len(chunks):
        failures.append("missing cached extraction coverage")
    summary = {"validation_passed": not failures, "validation_failures": failures, "documents": len(docs),
               "chunks": len(chunks), "entities": len(vertices), "relationships": len(edges),
               "audited_evidence_instances": len(audit), "embedding_model": MODEL, "embedding_dim": DIMENSION}
    core.write_json(work / "final_validation.json", summary)
    if failures:
        raise ValueError(f"Final cache validation failed: {failures}")
    return summary
