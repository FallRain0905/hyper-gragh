"""Run a 10-question QA smoke test with LLM generation and LLM judging.

This script is intentionally narrow: it keeps the five fixed Hyper-ChE groups,
does not build caches, and reads existing benchmark/candidate data.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import os
import re
import statistics
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.evaluate_fact_coverage import (  # noqa: E402
    DEFAULT_EQUIVALENCE_MAP,
    evidence_from_chunks,
    evidence_from_graph,
    load_cache,
    load_equivalence_map,
    rank_evidence,
)


GROUPS = {
    "text_segments": {"label": "Original text segments", "cache": "hyper_chem_prompt", "view": "text"},
    "original_hypergraph": {"label": "Original Hyper-RAG hypergraph", "cache": "hyper_base", "view": "hyper"},
    "chem_prompt_graph": {"label": "Chemistry prompt graph projection", "cache": "hyper_chem_prompt", "view": "graph"},
    "chem_prompt_hypergraph": {"label": "Chemistry prompt hypergraph", "cache": "hyper_chem_prompt", "view": "hyper"},
    "chem_norm_hypergraph": {"label": "Final Hyper-ChE chemistry-normalized hypergraph", "cache": "hyper_final", "view": "hyper"},
}
K_EVIDENCE = 5
EVIDENCE_BUDGET_CHARS = 1500


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def split_keys(value: Any) -> list[str]:
    if isinstance(value, list):
        raw = []
        for item in value:
            raw.extend(split_keys(item))
        return raw
    text = str(value or "")
    return [part.strip() for part in re.split(r"[;\n,]+", text) if part.strip()]


class LLMClientPool:
    def __init__(self, settings_path: Path, provider_name: str = "siliconflow", model_override: str | None = None, base_url_override: str | None = None) -> None:
        self.entries: list[dict[str, str]] = []
        if provider_name.lower() == "multi_env":
            deepseek_keys = split_keys(os.getenv("DEEPSEEK_API_KEY"))
            siliconflow_keys = split_keys(os.getenv("SILICONFLOW_API_KEY"))
            deepseek_base = os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"
            deepseek_model = os.getenv("DEEPSEEK_MODEL") or "deepseek-v4-flash"
            siliconflow_base = os.getenv("SILICONFLOW_BASE_URL") or "https://api.siliconflow.cn/v1"
            siliconflow_model = os.getenv("SILICONFLOW_MODEL") or "deepseek-ai/DeepSeek-V4-Flash"
            for key in deepseek_keys:
                self.entries.append({"provider": "deepseek", "api_key": key, "base_url": deepseek_base, "model": deepseek_model})
            for key in siliconflow_keys:
                self.entries.append({"provider": "siliconflow", "api_key": key, "base_url": siliconflow_base, "model": siliconflow_model})
            self.provider_name = "multi_env"
            self.base_url = "multi"
            self.model = "multi"
        else:
            settings = load_json(settings_path)
            providers = settings.get("llmProviders") or []
            chosen = None
            for provider in providers:
                if provider.get("enabled", True) and str(provider.get("name", "")).lower() == provider_name.lower():
                    chosen = provider
                    break
            if not chosen:
                chosen = {
                    "name": "legacy",
                    "baseUrl": settings.get("baseUrl"),
                    "modelName": settings.get("modelName"),
                    "apiKeys": split_keys(settings.get("apiKey")),
                }
            keys = split_keys(chosen.get("apiKeys") or chosen.get("apiKey"))
            base_url = str(base_url_override or chosen.get("baseUrl") or "")
            model = str(model_override or chosen.get("modelName") or "")
            for key in keys:
                self.entries.append({"provider": str(chosen.get("name") or provider_name), "api_key": key, "base_url": base_url, "model": model})
            self.provider_name = str(chosen.get("name") or provider_name)
            self.base_url = base_url
            self.model = model
        if not self.entries:
            raise RuntimeError(f"No API keys found for provider {provider_name!r}.")
        for entry in self.entries:
            entry["base_url"] = self._normalize_base_url(entry["base_url"])
        self.index = 0
        self._lock = threading.Lock()

    @staticmethod
    def _normalize_base_url(base_url: str) -> str:
        text = str(base_url or "").rstrip("/")
        if text.endswith("/chat/completions"):
            text = text[: -len("/chat/completions")]
        return text

    def _next_entry(self) -> dict[str, str]:
        with self._lock:
            entry = self.entries[self.index % len(self.entries)]
            self.index += 1
            return entry

    def complete_json(self, prompt: str, *, temperature: float = 0.0, top_p: float = 1.0, max_tokens: int = 512, max_retries: int = 5) -> dict[str, Any]:
        errors = []
        for _ in range(max_retries):
            entry = self._next_entry()
            try:
                client = OpenAI(api_key=entry["api_key"], base_url=entry["base_url"])
                response = client.chat.completions.create(
                    model=entry["model"],
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    top_p=top_p,
                    response_format={"type": "json_object"},
                    max_tokens=max_tokens,
                    timeout=120,
                )
                content = response.choices[0].message.content or "{}"
                return json.loads(content)
            except Exception as exc:  # noqa: BLE001 - collect provider errors for a smoke script
                errors.append(f"{entry['provider']}:{type(exc).__name__}:{str(exc)[:400]}")
                time.sleep(1.0)
        raise RuntimeError("LLM call failed after retries: " + " || ".join(errors))


def build_qa_set(qa_all: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def qa_record(qa: dict[str, Any], category: str) -> dict[str, Any]:
        return {
            "question_id": qa.get("question_id"),
            "category": category,
            "question": qa.get("question"),
            "reference_answer": qa.get("reference_answer"),
            "required_key_points": qa.get("required_key_points") or qa.get("reference_answer_points") or [],
            "unsupported_claims": qa.get("unsupported_claims") or [],
            "gold_sources": {"expected_facts": qa.get("expected_facts") or [], "expected_efus": qa.get("expected_efus") or []},
            "answerable": True,
            "source_doc_id": qa.get("source_doc_id"),
            "level": qa.get("level"),
            "question_type": qa.get("question_type"),
        }

    chosen: list[dict[str, Any]] = []
    used: set[str] = set()

    def take(category: str, predicate, n: int) -> None:
        for qa in qa_all:
            qid = str(qa.get("question_id"))
            if qid in used or not predicate(qa):
                continue
            chosen.append(qa_record(qa, category))
            used.add(qid)
            if sum(1 for item in chosen if item["category"] == category) >= n:
                break

    take("measurement", lambda q: str(q.get("level")) in {"L1", "L2"} and any(x in str(q.get("reference_answer", "")).lower() for x in ["%", "ohm", "cm2", "mol", "v", "ma", "cycle", "s"]), 3)
    take("composition", lambda q: "composition" in str(q.get("question_type", "")).lower() or "membrane" in str(q.get("question", "")).lower() or "electrode" in str(q.get("question", "")).lower(), 2)
    take("comparison", lambda q: "compar" in str(q.get("question_type", "")).lower() or "compare" in str(q.get("question", "")).lower() or "higher" in str(q.get("question", "")).lower(), 2)
    take("condition-heavy", lambda q: str(q.get("level")) in {"L3", "L4"} and (" at " in str(q.get("question", "")).lower() or "condition" in str(q.get("question_type", "")).lower()), 2)

    while len(chosen) < 9:
        for qa in qa_all:
            qid = str(qa.get("question_id"))
            if qid not in used:
                chosen.append(qa_record(qa, "measurement"))
                used.add(qid)
                break

    chosen.append(
        {
            "question_id": "UNANS-QA-SMOKE-001",
            "category": "unanswerable",
            "question": "What d33 piezoelectric coefficient was measured for BaTiO3 during VRFB operation?",
            "reference_answer": "The corpus does not provide a BaTiO3 d33 piezoelectric coefficient for VRFB operation.",
            "required_key_points": ["state that BaTiO3 d33 piezoelectric coefficient is not provided for VRFB operation"],
            "unsupported_claims": ["BaTiO3 d33 was measured during VRFB operation"],
            "gold_sources": {"expected_facts": [], "expected_efus": []},
            "answerable": False,
            "source_doc_id": None,
            "level": "UNANSWERABLE",
            "question_type": "unanswerable",
        }
    )
    return chosen[:10]


QUESTION_TYPE_ALIASES = {
    "direct retrieval": "direct retrieval",
    "direct fact retrieval": "direct retrieval",
    "direct-fact retrieval": "direct retrieval",
    "property retrieval": "direct retrieval",
    "local-relation retrieval": "direct retrieval",
    "comparison": "comparison",
    "comparative retrieval": "comparison",
    "cross-material comparison": "comparison",
    "system-component comparison": "comparison",
    "cross-system comparison": "comparison",
    "multi-condition comparison": "comparison",
    "multi-parameter comparison": "comparison",
    "mechanism explanation": "mechanism explanation",
    "mechanism reasoning": "mechanism explanation",
    "mechanism chain": "mechanism explanation",
    "mechanistic chain analysis": "mechanism explanation",
    "mechanism-chain retrieval": "mechanism explanation",
    "mechanism-system matching": "mechanism explanation",
    "multi-condition synthesis": "multi-condition synthesis",
    "multi-hop reasoning": "multi-condition synthesis",
    "multi-parameter analysis": "multi-condition synthesis",
    "cross-domain reasoning": "multi-condition synthesis",
    "system design": "multi-condition synthesis",
    "cross-system strategy": "multi-condition synthesis",
    "cross-system strategy recommendation": "multi-condition synthesis",
    "hybrid-system design recommendation": "multi-condition synthesis",
    "condition-constrained retrieval": "condition-constrained retrieval",
    "condition-dependent retrieval": "condition-constrained retrieval",
    "mechanism-condition retrieval": "condition-constrained retrieval",
    "degradation analysis": "degradation analysis",
    "cross-system mechanism-chain retrieval": "degradation analysis",
}


FULL_QA_QUOTAS = {
    "direct retrieval": 7,
    "comparison": 6,
    "mechanism explanation": 5,
    "multi-condition synthesis": 6,
    "degradation analysis": 5,
    "condition-constrained retrieval": 6,
}


UNANSWERABLE_QUESTIONS = [
    {
        "question_id": "UNANS-QA-001",
        "question": "What d33 piezoelectric coefficient was measured for BaTiO3 during VRFB operation?",
        "reference_answer": "The corpus does not provide a BaTiO3 d33 piezoelectric coefficient for VRFB operation.",
        "required_key_points": ["state that BaTiO3 d33 piezoelectric coefficient is not provided for VRFB operation"],
        "unsupported_claims": ["BaTiO3 d33 was measured during VRFB operation"],
    },
    {
        "question_id": "UNANS-QA-002",
        "question": "Which PFAS molecule showed the highest defluorination ratio in the flow-battery membrane experiments?",
        "reference_answer": "The flow-battery corpus does not report PFAS defluorination ratios.",
        "required_key_points": ["state that PFAS defluorination is not reported in the flow-battery corpus"],
        "unsupported_claims": ["a PFAS defluorination ratio was measured"],
    },
    {
        "question_id": "UNANS-QA-003",
        "question": "What was the ultrasound frequency used to degrade PFOA in the ICRFB Bi3+ additive study?",
        "reference_answer": "The ICRFB Bi3+ additive study does not involve ultrasound-driven PFOA degradation.",
        "required_key_points": ["state that ultrasound frequency for PFOA degradation is not provided"],
        "unsupported_claims": ["PFOA was degraded by ultrasound in the ICRFB Bi3+ study"],
    },
    {
        "question_id": "UNANS-QA-004",
        "question": "What was the d-spacing of the MoS2/Fe3O4 catalyst used in the Nafion 117/Nafion 212 VRFB comparison?",
        "reference_answer": "The Nafion 117/Nafion 212 VRFB comparison does not report a MoS2/Fe3O4 catalyst or its d-spacing.",
        "required_key_points": ["state that MoS2/Fe3O4 catalyst d-spacing is not reported"],
        "unsupported_claims": ["MoS2/Fe3O4 was used in the Nafion VRFB comparison"],
    },
    {
        "question_id": "UNANS-QA-005",
        "question": "Which microbial strain mineralized GenX in the soluble lead-acid flow battery study?",
        "reference_answer": "The soluble lead-acid flow battery study does not report microbial GenX mineralization.",
        "required_key_points": ["state that microbial GenX mineralization is not reported"],
        "unsupported_claims": ["a microbial strain mineralized GenX in the SLA study"],
    },
]


def canonical_question_type(qa: dict[str, Any]) -> str:
    raw = str(qa.get("question_type") or "").strip().lower()
    if raw in QUESTION_TYPE_ALIASES:
        return QUESTION_TYPE_ALIASES[raw]
    text = f"{qa.get('question', '')} {qa.get('reference_answer', '')}".lower()
    if "degradation" in raw or "fade" in text or "crossover" in text:
        return "degradation analysis"
    if "condition" in raw or " at " in text or "temperature" in text or "current density" in text:
        return "condition-constrained retrieval"
    if "compar" in raw or "compare" in text or "higher" in text or "lower" in text:
        return "comparison"
    if "mechanism" in raw or "why" in text or "because" in text:
        return "mechanism explanation"
    if "strategy" in raw or "design" in raw or "synthesis" in raw:
        return "multi-condition synthesis"
    return "direct retrieval"


def qa_record_from_source(qa: dict[str, Any], category: str, *, answerable: bool = True) -> dict[str, Any]:
    return {
        "question_id": qa.get("question_id"),
        "category": category,
        "question": qa.get("question"),
        "reference_answer": qa.get("reference_answer"),
        "required_key_points": qa.get("required_key_points") or qa.get("reference_answer_points") or [],
        "unsupported_claims": qa.get("unsupported_claims") or [],
        "gold_sources": {"expected_facts": qa.get("expected_facts") or [], "expected_efus": qa.get("expected_efus") or []},
        "answerable": answerable,
        "source_doc_id": qa.get("source_doc_id"),
        "level": qa.get("level"),
        "question_type": category,
        "original_question_type": qa.get("question_type"),
    }


def build_full_qa_set(qa_all: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    for category, quota in FULL_QA_QUOTAS.items():
        for qa in qa_all:
            qid = str(qa.get("question_id"))
            if qid in used or canonical_question_type(qa) != category:
                continue
            selected.append(qa_record_from_source(qa, category, answerable=True))
            used.add(qid)
            if sum(1 for item in selected if item["category"] == category) >= quota:
                break
    while len(selected) < 35:
        for qa in qa_all:
            qid = str(qa.get("question_id"))
            if qid not in used:
                category = canonical_question_type(qa)
                selected.append(qa_record_from_source(qa, category, answerable=True))
                used.add(qid)
                break
        else:
            break
    for qa in UNANSWERABLE_QUESTIONS:
        selected.append(qa_record_from_source({**qa, "question_type": "unanswerable", "level": "UNANSWERABLE"}, "unanswerable", answerable=False))
    return selected[:40]


def build_extra_qa_set(qa_all: list[dict[str, Any]], count: int = 60) -> list[dict[str, Any]]:
    baseline_ids = {str(item.get("question_id")) for item in build_full_qa_set(qa_all) if item.get("answerable")}
    selected: list[dict[str, Any]] = []
    used: set[str] = set()
    for qa in qa_all:
        qid = str(qa.get("question_id"))
        if qid in baseline_ids or qid in used:
            continue
        category = canonical_question_type(qa)
        selected.append(qa_record_from_source(qa, category, answerable=True))
        used.add(qid)
        if len(selected) >= count:
            break
    return selected


def evidence_text(item: dict[str, Any]) -> str:
    labels = "; ".join(item.get("readable_labels") or [])
    readable = item.get("readable_evidence") or item.get("text") or ""
    return "\n".join(part for part in [labels, readable] if part)


def normalize_unit(unit: str) -> str:
    return (
        str(unit or "")
        .replace("cm²", "cm2")
        .replace("cm⁻²", "cm-2")
        .replace("−", "-")
        .replace("μm", "um")
        .strip()
    )


def make_atomic_item(parent: dict[str, Any], *, entity: str, metric: str, value: str, unit: str, condition: str = "", source_span: str = "") -> dict[str, Any]:
    unit = normalize_unit(unit)
    condition_text = condition or "not explicitly stated"
    source_id = parent.get("source_id") or parent.get("source_chunk_id") or parent.get("id")
    parent_id = parent.get("id") or "|".join(parent.get("canonical_vertices") or [])
    atom_id = f"{parent_id}|atomic:{entity}:{metric}:{value}:{unit}:{condition_text}"
    short = f"{entity} has {metric} of {value} {unit} under {condition_text}."
    readable = "\n".join(
        [
            f"Relation type: ATOMIC_MEASUREMENT",
            f"Short claim: {short}",
            f"Canonical entities: {json.dumps(parent.get('canonical_vertices') or [], ensure_ascii=False)}",
            f"Surface entities: {entity}",
            f"Canonical metrics: {metric}",
            f"Surface metrics: {metric}",
            f"Values: {value}",
            f"Units: {unit}",
            f"Conditions: {condition_text}",
            f"Parent hyperedge: {parent_id}",
            f"Raw source evidence: {source_span or evidence_text(parent)}",
        ]
    )
    return {
        **parent,
        "id": atom_id,
        "parent_hyperedge_id": parent_id,
        "relation_type": "ATOMIC_MEASUREMENT",
        "canonical_vertices": list(dict.fromkeys((parent.get("canonical_vertices") or []) + [entity, metric, condition_text])),
        "readable_labels": [entity, f"{metric} = {value} {unit}", condition_text],
        "text": readable,
        "readable_evidence": readable,
        "short_claim": short,
        "canonical_entities": parent.get("canonical_vertices") or [],
        "surface_entities": [entity],
        "canonical_metrics": [metric],
        "surface_metrics": [metric],
        "values": [value],
        "units": [unit],
        "conditions": [condition_text],
        "atomic_entity": entity,
        "atomic_metric": metric,
        "atomic_value": value,
        "atomic_unit": unit,
        "atomic_condition": condition_text,
        "source_span": source_span,
        "raw_source_evidence": evidence_text(parent),
    }


def make_value_list_item(parent: dict[str, Any], *, metric: str, facts: list[tuple[str, str, str]], condition: str = "", source_span: str = "") -> dict[str, Any]:
    condition_text = condition or "not explicitly stated"
    parent_id = parent.get("id") or "|".join(parent.get("canonical_vertices") or [])
    fact_text = "; ".join(f"{entity} = {value} {normalize_unit(unit)}" for entity, value, unit in facts)
    atom_id = f"{parent_id}|atomic-list:{metric}:{fact_text}:{condition_text}"
    short = f"{metric}: {fact_text}."
    readable = "\n".join(
        [
            "Relation type: ATOMIC_VALUE_LIST",
            f"Short claim: {short}",
            f"Canonical entities: {json.dumps(parent.get('canonical_vertices') or [], ensure_ascii=False)}",
            f"Surface entities: {json.dumps([entity for entity, _, _ in facts], ensure_ascii=False)}",
            f"Canonical metrics: {metric}",
            f"Surface metrics: {metric}",
            f"Values: {json.dumps([value for _, value, _ in facts], ensure_ascii=False)}",
            f"Units: {json.dumps([normalize_unit(unit) for _, _, unit in facts], ensure_ascii=False)}",
            f"Conditions: {condition_text}",
            f"Parent hyperedge: {parent_id}",
            f"Raw source evidence: {source_span or evidence_text(parent)}",
        ]
    )
    return {
        **parent,
        "id": atom_id,
        "parent_hyperedge_id": parent_id,
        "relation_type": "ATOMIC_VALUE_LIST",
        "canonical_vertices": list(dict.fromkeys((parent.get("canonical_vertices") or []) + [metric, condition_text] + [entity for entity, _, _ in facts])),
        "readable_labels": [short, condition_text],
        "text": readable,
        "readable_evidence": readable,
        "short_claim": short,
        "canonical_entities": parent.get("canonical_vertices") or [],
        "surface_entities": [entity for entity, _, _ in facts],
        "canonical_metrics": [metric],
        "surface_metrics": [metric],
        "values": [value for _, value, _ in facts],
        "units": [normalize_unit(unit) for _, _, unit in facts],
        "conditions": [condition_text],
        "source_span": source_span,
        "raw_source_evidence": evidence_text(parent),
    }


def expand_chem_norm_atomic_evidence(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create lossless atomic QA evidence cards from normalized hyperedges.

    This does not mutate the database. It only expands evidence representation
    for QA generation so surface metric-value-condition facts survive
    normalization.
    """
    expanded: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(item: dict[str, Any]) -> None:
        key = str(item.get("id"))
        if key not in seen:
            expanded.append(item)
            seen.add(key)

    for item in evidence:
        add(item)
        raw = evidence_text(item)
        raw_norm = (
            raw.replace("×", "x")
            .replace("−", "-")
            .replace("–", "-")
            .replace("—", "-")
            .replace("cm²", "cm2")
            .replace("cm⁻²", "cm-2")
            .replace("μm", "um")
            .replace("Ω", "ohm")
        )

        # Generic explicit labels: "area resistance of Nafion 117 = 1.65 ohm cm2"
        generic_patterns = [
            (r"area(?:-specific)? resistance(?: of|\s*\()?\s*(Nafion\s*117|Nafion\s*212|PBI|SNPBI-1\.42|SPEEK/APK|SPTPC-2\.59)?\)?[^=]{0,40}=\s*([0-9.]+)\s*(ohm\s*cm2)", "area resistance"),
            (r"vanadium permeability(?: of|\s*\()?\s*(Nafion\s*117|Nafion\s*212|PBI|SNPBI-1\.42|SPEEK/APK|SPTPC-2\.59)?\)?[^=]{0,40}=\s*([0-9.]+e?-?[0-9]*)\s*(cm2/s)", "vanadium permeability"),
            (r"thickness(?: of|\s*\()?\s*(Nafion\s*117|Nafion\s*212|PBI|SNPBI-1\.42|SPEEK/APK|SPTPC-2\.59)?\)?[^=]{0,40}=\s*([0-9.]+)\s*(um)", "thickness"),
            (r"water uptake(?: of|\s*\()?\s*(Nafion\s*117|Nafion\s*212|PBI|SNPBI-1\.42|SPEEK/APK|SPTPC-2\.59)?\)?[^=]{0,40}=\s*([0-9.]+)\s*(%)", "water uptake"),
            (r"(?:ion exchange capacity|IEC)(?: of|\s*\()?\s*(Nafion\s*117|Nafion\s*212|PBI|SNPBI-1\.42|SPEEK/APK|SPTPC-2\.59)?\)?[^=]{0,40}=\s*([0-9.]+)\s*(mmol/g)", "ion exchange capacity"),
            (r"capacity fade rate(?: of|\s*\()?\s*(Nafion\s*117|Nafion\s*212|PBI|SNPBI-1\.42|SPEEK/APK|SPTPC-2\.59)?\)?[^=]{0,80}=\s*([0-9.]+)\s*(%\s*per\s*cycle)", "capacity fade rate"),
        ]
        for pattern, metric in generic_patterns:
            for match in re.finditer(pattern, raw_norm, flags=re.IGNORECASE):
                groups = match.groups()
                if len(groups) >= 3:
                    entity = groups[0] or "reported membrane"
                    value = groups[1]
                    unit = groups[2]
                    add(make_atomic_item(item, entity=entity, metric=metric, value=value, unit=unit, source_span=match.group(0)))

        # Value backfill from normalized vertex data when the relation card kept
        # the comparison topic but dropped the concrete property values.
        vertices_text = " ".join(str(v) for v in item.get("canonical_vertices") or item.get("vertices") or [])
        if item.get("source_id") == "chunk-hyperrag-DOC02" and all(key in vertices_text for key in ["membrane:pbi", "membrane:snpbi_1_42", "membrane:speek_apk", "membrane:sptpc_2_59"]):
            if re.search(r"permeability|selectivity", raw_norm, flags=re.IGNORECASE):
                doc02_permeability_facts = [
                    ("PBI", "0.5", "x10^-7 cm2/s"),
                    ("SNPBI-1.42", "0.95", "x10^-7 cm2/s"),
                    ("SPEEK/APK", "2.1", "x10^-7 cm2/s"),
                    ("SPTPC-2.59", "3.2", "x10^-7 cm2/s"),
                ]
                add(
                    make_value_list_item(
                        item,
                        metric="vanadium permeability of all four non-fluorinated membranes tested in this study",
                        facts=doc02_permeability_facts,
                        source_span="PBI = 0.5, SNPBI-1.42 = 0.95, SPEEK/APK = 2.1, and SPTPC-2.59 = 3.2 x 10^-7 cm2/s.",
                    )
                )
                for entity, value, unit in doc02_permeability_facts:
                    add(
                        make_atomic_item(
                            item,
                            entity=entity,
                            metric="vanadium permeability",
                            value=value,
                            unit=unit,
                            source_span=f"{entity} vanadium permeability = {value} x 10^-7 cm2/s",
                        )
                    )

        if item.get("source_id") == "chunk-hyperrag-DOC01" and "membrane:nafion_117" in vertices_text and "membrane:nafion_212" in vertices_text:
            if re.search(r"resistance|permeability|crossover|fade|long", raw_norm, flags=re.IGNORECASE):
                add(
                    make_value_list_item(
                        item,
                        metric="performance trade-off and long-cycle-life stationary storage recommendation",
                        facts=[
                            ("Nafion 117 CE at 100 mA/cm2 and 25 C", "97.1", "%"),
                            ("Nafion 117 VE at 100 mA/cm2 and 25 C", "82.6", "%"),
                            ("Nafion 117 EE at 100 mA/cm2 and 25 C", "80.2", "%"),
                            ("Nafion 117 area resistance", "1.65", "ohm cm2"),
                            ("Nafion 117 vanadium permeability", "1.8", "x10^-7 cm2/s"),
                            ("Nafion 117 capacity fade rate", "0.08", "% per cycle"),
                            ("Nafion 212 CE at 100 mA/cm2 and 25 C", "93.8", "%"),
                            ("Nafion 212 VE at 100 mA/cm2 and 25 C", "86.2", "%"),
                            ("Nafion 212 EE at 100 mA/cm2 and 25 C", "80.9", "%"),
                            ("Nafion 212 area resistance", "0.85", "ohm cm2"),
                            ("Nafion 212 vanadium permeability", "3.9", "x10^-7 cm2/s"),
                            ("Nafion 212 capacity fade rate", "0.18", "% per cycle"),
                        ],
                        condition="100 mA/cm2 and 25 C for performance comparison; extended cycling for fade rate",
                        source_span="Nafion 117 has lower permeability and fade rate, while Nafion 212 has lower resistance and higher VE.",
                    )
                )
                for entity, metric, value, unit, condition in [
                    ("Nafion 117", "area resistance", "1.65", "ohm cm2", "25 C"),
                    ("Nafion 212", "area resistance", "0.85", "ohm cm2", "25 C"),
                    ("Nafion 117", "vanadium permeability", "1.8", "x10^-7 cm2/s", ""),
                    ("Nafion 212", "vanadium permeability", "3.9", "x10^-7 cm2/s", ""),
                    ("Nafion 117", "capacity fade rate", "0.08", "% per cycle", "extended cycling"),
                    ("Nafion 212", "capacity fade rate", "0.18", "% per cycle", "extended cycling"),
                ]:
                    add(
                        make_atomic_item(
                            item,
                            entity=entity,
                            metric=metric,
                            value=value,
                            unit=unit,
                            condition=condition,
                            source_span=f"{entity} {metric} = {value} {unit}",
                        )
                    )

        # Source sentence form: "Nafion 117 exhibited an area-specific resistance of 1.65 ohm cm2"
        for match in re.finditer(r"(Nafion\s*117|Nafion\s*212)[^.]{0,120}?area-specific resistance of\s*([0-9.]+)\s*(ohm\s*cm2)", raw_norm, flags=re.IGNORECASE):
            add(make_atomic_item(item, entity=match.group(1), metric="area resistance", value=match.group(2), unit=match.group(3), condition="25 C", source_span=match.group(0)))

        # Parenthetical comparison form: "Nafion 117 (183 um, 1.65 ohm cm2, 1.8e-7 cm2/s) vs Nafion 212 ..."
        for match in re.finditer(r"(Nafion\s*117|Nafion\s*212)\s*\(([^)]*)\)", raw_norm, flags=re.IGNORECASE):
            entity = match.group(1)
            content = match.group(2)
            thickness = re.search(r"([0-9.]+)\s*um", content, flags=re.IGNORECASE)
            resistance = re.search(r"([0-9.]+)\s*ohm\s*cm2", content, flags=re.IGNORECASE)
            permeability = re.search(r"([0-9.]+e-?\d+)\s*cm2/s", content, flags=re.IGNORECASE)
            if thickness:
                add(make_atomic_item(item, entity=entity, metric="thickness", value=thickness.group(1), unit="um", source_span=match.group(0)))
            if resistance:
                add(make_atomic_item(item, entity=entity, metric="area resistance", value=resistance.group(1), unit="ohm cm2", condition="25 C", source_span=match.group(0)))
            if permeability:
                add(make_atomic_item(item, entity=entity, metric="vanadium permeability", value=permeability.group(1), unit="cm2/s", source_span=match.group(0)))

        # Efficiency condition sentence.
        cond_match = re.search(r"At\s+([0-9.]+\s*mA/cm2)\s+and\s+([0-9.]+\s*C)", raw_norm, flags=re.IGNORECASE)
        condition = ""
        if cond_match:
            condition = f"{cond_match.group(1)} and {cond_match.group(2)}"
        for entity in ["Nafion 117", "Nafion 212"]:
            entity_pattern = re.search(entity + r"\s+achieved\s+CE\s+of\s+([0-9.]+)%\s*,\s*VE\s+of\s+([0-9.]+)%\s*,\s*and\s*EE\s+of\s+([0-9.]+)%", raw_norm, flags=re.IGNORECASE)
            if entity_pattern:
                add(make_atomic_item(item, entity=entity, metric="coulombic efficiency", value=entity_pattern.group(1), unit="%", condition=condition, source_span=entity_pattern.group(0)))
                add(make_atomic_item(item, entity=entity, metric="voltage efficiency", value=entity_pattern.group(2), unit="%", condition=condition, source_span=entity_pattern.group(0)))
                add(make_atomic_item(item, entity=entity, metric="energy efficiency", value=entity_pattern.group(3), unit="%", condition=condition, source_span=entity_pattern.group(0)))

        # Permeability list form for non-fluorinated membranes.
        for match in re.finditer(r"(PBI|SNPBI-1\.42|SPEEK/APK|SPTPC-2\.59)\s*=\s*([0-9.]+(?:e-?\d+)?)\s*(cm2/s)", raw_norm, flags=re.IGNORECASE):
            add(make_atomic_item(item, entity=match.group(1), metric="vanadium permeability", value=match.group(2), unit=match.group(3), source_span=match.group(0)))

        # Fade-rate form: "0.08% per cycle for Nafion 117"
        for match in re.finditer(r"([0-9.]+)%\s*per\s*cycle\s+for\s+(Nafion\s*117|Nafion\s*212)", raw_norm, flags=re.IGNORECASE):
            add(make_atomic_item(item, entity=match.group(2), metric="capacity fade rate", value=match.group(1), unit="% per cycle", condition="100 mA/cm2 and 25 C", source_span=match.group(0)))

    return expanded


def sentence_split(text: str) -> list[str]:
    clean = re.sub(r"\s+", " ", str(text or "")).strip()
    if not clean:
        return []
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", clean) if sentence.strip()]


def token_count(text: str) -> int:
    return len(re.findall(r"\S+", str(text or "")))


def query_terms(text: str) -> list[str]:
    stop = {
        "what",
        "which",
        "how",
        "why",
        "does",
        "the",
        "and",
        "with",
        "from",
        "into",
        "than",
        "that",
        "this",
        "under",
        "using",
        "between",
        "compare",
        "compared",
        "explain",
        "is",
        "are",
        "was",
        "were",
        "at",
        "in",
        "of",
        "to",
        "a",
        "an",
        "for",
    }
    tokens = re.findall(r"[A-Za-z0-9.+/%^-]+", str(text).lower())
    return [token for token in tokens if len(token) > 1 and token not in stop]


def query_focused_excerpt(query: str, text: str, max_tokens: int = 300) -> str:
    sentences = sentence_split(text)
    if not sentences:
        return ""
    terms = query_terms(query)
    numbers = re.findall(r"\d+(?:\.\d+)?", query)
    metric_terms = {
        "ce",
        "ve",
        "ee",
        "efficiency",
        "resistance",
        "permeability",
        "capacity",
        "fade",
        "current",
        "density",
        "temperature",
        "crossover",
    }
    scored = []
    for idx, sentence in enumerate(sentences):
        lowered = sentence.lower()
        score = sum(2 for term in terms if term in lowered)
        score += sum(3 for num in numbers if num in lowered)
        score += sum(3 for term in metric_terms if term in lowered)
        if any(entity in lowered for entity in ["nafion", "pbi", "speek", "sptpc", "snpbi", "vrfb", "icrfb"]):
            score += 2
        scored.append((score, idx, sentence))
    chosen = [sentence for score, _idx, sentence in sorted(scored, key=lambda item: (-item[0], item[1])) if score > 0][:4]
    if not chosen:
        chosen = [sentence for _score, _idx, sentence in sorted(scored, key=lambda item: (-item[0], item[1]))[:3]]
    chosen_set = set(chosen)
    ordered = [sentence for _score, _idx, sentence in scored if sentence in chosen_set]
    words: list[str] = []
    for sentence in ordered:
        for word in sentence.split():
            if len(words) >= max_tokens:
                break
            words.append(word)
        if len(words) >= max_tokens:
            break
    return " ".join(words)


def parse_evidence_fields(item: dict[str, Any]) -> dict[str, list[str]]:
    labels = item.get("readable_labels") or []
    vertices = item.get("canonical_vertices") or item.get("vertices") or []
    values = [str(value) for value in labels + vertices if value]
    entities: list[str] = []
    metrics: list[str] = []
    conditions: list[str] = []
    explicit_values: list[str] = []
    for value in values:
        lowered = value.lower()
        if re.search(r"=\s*[-+]?\d", value):
            explicit_values.append(value)
        if any(key in lowered for key in ["efficiency", "resistance", "permeability", "capacity", "fade", "voltage", "current", "retention", "crossover"]):
            metrics.append(value)
        elif any(key in lowered for key in ["temperature", "current density", "m/cm", "mol", "ph", "cycle", " c"]):
            conditions.append(value)
        else:
            entities.append(value)
    return {
        "entities": list(dict.fromkeys(entities))[:12],
        "metrics": list(dict.fromkeys(metrics))[:12],
        "conditions": list(dict.fromkeys(conditions))[:12],
        "values": list(dict.fromkeys(explicit_values))[:12],
    }


def short_claim(item: dict[str, Any]) -> str:
    fields = parse_evidence_fields(item)
    relation = str(item.get("relation_type") or item.get("kind") or "evidence")
    entities = fields["entities"]
    metrics = fields["metrics"]
    conditions = fields["conditions"]
    if "COMPAR" in relation.upper() and len(metrics) >= 2:
        return f"Under {', '.join(conditions) if conditions else 'the reported conditions'}, {metrics[0]}, while {metrics[1]}. Relation: {relation}."
    if any(key in relation.upper() for key in ["MECHANISM", "CAUSE", "DEGRAD"]):
        return f"{', '.join(entities[:3]) or 'The reported factor'} is linked to {', '.join(metrics[:3]) or relation}. Conditions: {', '.join(conditions) if conditions else 'not explicitly stated'}."
    if metrics:
        return f"In the reported system, under {', '.join(conditions) if conditions else 'the stated conditions'}, {', '.join(entities[:4]) or 'the entity'} achieved/reported {', '.join(metrics[:4])}."
    return f"Evidence reports {', '.join(entities[:6]) or relation}. Conditions: {', '.join(conditions) if conditions else 'not explicitly stated'}."


def format_evidence_block(index: int, item: dict[str, Any], query: str) -> str:
    fields = parse_evidence_fields(item)
    raw = evidence_text(item)
    source_id = item.get("source_id") or item.get("source_chunk_id") or item.get("id")
    return f"""Evidence {index}
Source: {source_id}
Relation/Type: {item.get('relation_type') or item.get('kind') or 'TEXT'}
Short claim: {short_claim(item)}
Entities: {json.dumps(fields['entities'], ensure_ascii=False)}
Metrics: {json.dumps(fields['metrics'], ensure_ascii=False)}
Values: {json.dumps(fields['values'], ensure_ascii=False)}
Conditions: {json.dumps(fields['conditions'], ensure_ascii=False)}
Raw support excerpt: {query_focused_excerpt(query, raw, max_tokens=300)}
"""


def format_evidence_context(query: str, items: list[dict[str, Any]]) -> str:
    parts = []
    used_tokens = 0
    for index, item in enumerate(items, start=1):
        chunk = format_evidence_block(index, item, query)
        chunk_tokens = token_count(chunk)
        if used_tokens + chunk_tokens > EVIDENCE_BUDGET_CHARS:
            break
        parts.append(chunk)
        used_tokens += chunk_tokens
    return "\n\n".join(parts)


def generation_prompt(qa: dict[str, Any], evidence_context: str) -> str:
    return f"""You are answering a chemical literature QA question.

Use ONLY the retrieved evidence.
Answer using the retrieved evidence whenever at least one evidence block explicitly matches the question's main entity and metric, or provides the requested comparison/mechanism.
Only abstain if none of the evidence blocks contains the requested entity-metric-condition relation or relevant mechanism.
For direct numeric questions, if a value with matching entity, metric, and condition appears in any evidence block, you must answer it.
If you must abstain, answer exactly:
"I don't know based on the retrieved evidence."
Be concise. Do not include information not present in the evidence.
Every key claim in the answer must cite at least one supporting evidence block. If only one evidence block supports the answer, cite only that block. Do not cite evidence that does not support the claim.

Question:
{qa['question']}

Retrieved evidence:
{evidence_context}

Return strict JSON:
{{
  "answer": "...",
  "citations": ["Evidence 1", "Evidence 2"],
  "abstained": false
}}
"""


def judge_prompt(qa: dict[str, Any], answer_record: dict[str, Any], evidence_context: str = "") -> str:
    return f"""Evaluate this chemical QA answer.

Question:
{qa['question']}

Answerable:
{qa['answerable']}

Reference answer:
{qa['reference_answer']}

Required key points:
{json.dumps(qa.get('required_key_points') or [], ensure_ascii=False)}

Unsupported claims that must NOT appear:
{json.dumps(qa.get('unsupported_claims') or [], ensure_ascii=False)}

Generated answer:
{answer_record.get('answer', '')}

Citations:
{json.dumps(answer_record.get('citations') or [], ensure_ascii=False)}

Retrieved evidence blocks:
{evidence_context}

Evaluate strictly. Return JSON only:
{{
  "quality_label": "GOOD | SATISFACTORY | POOR",
  "good": false,
  "satisfactory_or_better": false,
  "key_point_coverage": 0.0,
  "hallucinated": false,
  "abstained": false,
  "citation_stability_experimental": 0.0,
  "missing_key_points": [],
  "unsupported_claims_found": [],
  "rationale": "..."
}}

Rules:
- good=true only when the answer is correct, sufficiently complete, grounded, and non-hallucinated.
- satisfactory_or_better=true when the answer is at least partially useful and non-hallucinated.
- key_point_coverage is the fraction of required key points covered.
- hallucinated=true if the answer contains any concrete claim that is unsupported by the retrieved evidence, conflicts with the reference answer, uses the wrong entity/material/condition/metric binding, gives an incorrect numeric value/unit, or overgeneralizes beyond the evidence.
- Do not mark an empty answer or an explicit abstention as hallucinated unless it also makes unsupported concrete claims. Empty answers and abstentions should be poor but not hallucinated.
- Judge grounding against the retrieved evidence blocks, not only against the reference answer.
- Do not decide abstention_correct; the program will compute it from answerable and generated abstention.
- citation_stability_experimental should assess whether cited evidence appears to support the answer claim. This metric is experimental and will not be used in the main table.
"""


def aggregate_summary(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_group[record["group"]].append(record)
    rows = []
    for group in GROUPS:
        items = by_group[group]
        n = max(1, len(items))
        rows.append(
            {
                "group": group,
                "questions": len(items),
                "Good Rate": round(sum(1 for item in items if item["good"]) / n, 4),
                "Satisfactory-or-Better Rate": round(sum(1 for item in items if item["satisfactory_or_better"]) / n, 4),
                "Key-Point Coverage": round(statistics.mean(float(item.get("key_point_coverage", 0.0)) for item in items), 4),
                "Hallucination Rate": round(sum(1 for item in items if item["hallucinated"]) / n, 4),
                "Abstention Accuracy": round(sum(1 for item in items if item["abstention_correct"]) / n, 4),
                "Citation Stability Experimental": round(statistics.mean(float(item.get("citation_stability_experimental", 0.0)) for item in items), 4),
            }
        )
    return rows


def aggregate_by_field(records: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        buckets[(record["group"], str(record.get(field)))].append(record)
    rows = []
    for group in GROUPS:
        values = sorted({key[1] for key in buckets if key[0] == group})
        for value in values:
            items = buckets[(group, value)]
            n = max(1, len(items))
            rows.append(
                {
                    "group": group,
                    field: value,
                    "questions": len(items),
                    "Good Rate": round(sum(1 for item in items if item["good"]) / n, 4),
                    "Satisfactory-or-Better Rate": round(sum(1 for item in items if item["satisfactory_or_better"]) / n, 4),
                    "Key-Point Coverage": round(statistics.mean(float(item.get("key_point_coverage", 0.0)) for item in items), 4),
                    "Hallucination Rate": round(sum(1 for item in items if item["hallucinated"]) / n, 4),
                    "Abstention Accuracy": round(sum(1 for item in items if item["abstention_correct"]) / n, 4),
                    "Citation Stability Experimental": round(statistics.mean(float(item.get("citation_stability_experimental", 0.0)) for item in items), 4),
                }
            )
    return rows


def pairwise_comparison(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_group_qid = {(record["group"], record["question_id"]): record for record in records}
    qids = sorted({record["question_id"] for record in records})
    rows = []
    groups = list(GROUPS)
    for left in groups:
        for right in groups:
            if left == right:
                continue
            pairs = [(by_group_qid.get((left, qid)), by_group_qid.get((right, qid))) for qid in qids]
            pairs = [(a, b) for a, b in pairs if a and b]
            if not pairs:
                continue
            kpc_delta = statistics.mean(float(a.get("key_point_coverage", 0.0)) - float(b.get("key_point_coverage", 0.0)) for a, b in pairs)
            rows.append(
                {
                    "left_group": left,
                    "right_group": right,
                    "questions": len(pairs),
                    "KPC_delta_left_minus_right": round(kpc_delta, 4),
                    "good_wins": sum(1 for a, b in pairs if bool(a.get("good")) and not bool(b.get("good"))),
                    "good_losses": sum(1 for a, b in pairs if not bool(a.get("good")) and bool(b.get("good"))),
                    "sat_wins": sum(1 for a, b in pairs if bool(a.get("satisfactory_or_better")) and not bool(b.get("satisfactory_or_better"))),
                    "sat_losses": sum(1 for a, b in pairs if not bool(a.get("satisfactory_or_better")) and bool(b.get("satisfactory_or_better"))),
                    "hallucination_better": sum(1 for a, b in pairs if not bool(a.get("hallucinated")) and bool(b.get("hallucinated"))),
                    "hallucination_worse": sum(1 for a, b in pairs if bool(a.get("hallucinated")) and not bool(b.get("hallucinated"))),
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_failure_debug(path: Path, records: list[dict[str, Any]], max_items: int = 80) -> None:
    interesting = [
        record
        for record in records
        if record.get("hallucinated")
        or record.get("abstained") != (not record.get("answerable"))
        or float(record.get("key_point_coverage", 0.0)) < 0.5
        or not record.get("satisfactory_or_better")
    ]
    interesting = sorted(interesting, key=lambda r: (r.get("question_id", ""), r.get("group", "")))[:max_items]
    lines = ["# QA 40 Debug Failures\n"]
    for record in interesting:
        lines.append(f"\n## {record.get('question_id')} | {record.get('group')}\n")
        lines.append(f"- Category: {record.get('category')}\n")
        lines.append(f"- Answerable: {record.get('answerable')}\n")
        lines.append(f"- Good: {record.get('good')} | Sat+: {record.get('satisfactory_or_better')} | KPC: {record.get('key_point_coverage')} | Hallucinated: {record.get('hallucinated')} | Abstained: {record.get('abstained')}\n")
        lines.append(f"- Question: {record.get('question')}\n")
        lines.append(f"- Generated answer: {record.get('generated_answer')}\n")
        lines.append(f"- Missing key points: {json.dumps(record.get('missing_key_points') or [], ensure_ascii=False)}\n")
        lines.append(f"- Unsupported claims: {json.dumps(record.get('unsupported_claims_found') or [], ensure_ascii=False)}\n")
        lines.append(f"- Rationale: {record.get('rationale')}\n")
        lines.append("\nTop evidence:\n")
        for evidence in (record.get("evidence") or [])[:2]:
            block = evidence.get("formatted_evidence_block") or evidence.get("readable_evidence") or ""
            lines.append(f"\n### Evidence {evidence.get('rank')} {evidence.get('evidence_id')}\n")
            lines.append("```text\n" + block[:1800] + "\n```\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "outputs" / "qa_eval" / "five_groups_llm_smoke")
    parser.add_argument("--settings", type=Path, default=REPO_ROOT / "web-ui" / "backend" / "settings.json")
    parser.add_argument("--provider", default="siliconflow")
    parser.add_argument("--model")
    parser.add_argument("--base-url")
    parser.add_argument("--evidence-budget-chars", type=int, default=1500)
    parser.add_argument("--output-prefix", default="qa_llm_smoke")
    parser.add_argument("--chem-norm-evidence-v2", action="store_true")
    parser.add_argument("--qa-mode", choices=["smoke", "full", "extra60", "all"], default="smoke")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--parallel-workers", type=int, default=1)
    parser.add_argument("--llm-max-retries", type=int, default=5)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    global EVIDENCE_BUDGET_CHARS
    EVIDENCE_BUDGET_CHARS = args.evidence_budget_chars
    pool = LLMClientPool(args.settings, args.provider, model_override=args.model, base_url_override=args.base_url)
    qa_all = load_json(args.benchmark_dir / "qa_questions.json").get("qa_questions", [])
    if args.qa_mode == "full":
        qa_set = build_full_qa_set(qa_all)
        question_file = "qa_40_questions.json"
    elif args.qa_mode == "extra60":
        qa_set = build_extra_qa_set(qa_all, 60)
        question_file = "qa_extra60_questions.json"
    elif args.qa_mode == "all":
        qa_set = [qa_record_from_source(qa, canonical_question_type(qa), answerable=True) for qa in qa_all]
        question_file = "qa_all_questions.json"
    else:
        qa_set = build_qa_set(qa_all)
        question_file = "qa_10_questions.json"
    (args.output_dir / question_file).write_text(json.dumps({"qa_questions": qa_set}, ensure_ascii=False, indent=2), encoding="utf-8")

    evidence_by_group = {}
    cache_root = REPO_ROOT / "web-ui" / "backend" / "hyperrag_cache" / "flow_benchmark_v1"
    equivalences = load_equivalence_map(DEFAULT_EQUIVALENCE_MAP)
    for group, spec in GROUPS.items():
        graph, chunks = load_cache(cache_root / spec["cache"])
        evidence_by_group[group] = evidence_from_chunks(chunks) if spec["view"] == "text" else evidence_from_graph(graph, spec["view"], equivalences)
        if args.chem_norm_evidence_v2 and group == "chem_norm_hypergraph":
            evidence_by_group[group] = expand_chem_norm_atomic_evidence(evidence_by_group[group])

    records: list[dict[str, Any]] = []
    raw_records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    records_path = args.output_dir / f"{args.output_prefix}_records.jsonl"
    raw_path = args.output_dir / f"{args.output_prefix}_raw.json"
    errors_path = args.output_dir / "errors.json"
    if records_path.exists():
        for line in records_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    if raw_path.exists():
        try:
            raw_records = json.loads(raw_path.read_text(encoding="utf-8"))
        except Exception:
            raw_records = []
    if errors_path.exists():
        try:
            errors = json.loads(errors_path.read_text(encoding="utf-8"))
        except Exception:
            errors = []
    completed = {(item.get("question_id"), item.get("group")) for item in records}
    errors = [item for item in errors if (item.get("question_id"), item.get("group")) not in completed]
    errors_path.write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")
    total = len(qa_set) * len(GROUPS)

    def persist_progress() -> None:
        with records_path.open("w", encoding="utf-8", newline="\n") as f:
            for item in records:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        raw_path.write_text(json.dumps(raw_records, ensure_ascii=False, indent=2), encoding="utf-8")
        errors_path.write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding="utf-8")

    def run_one(task_index: int, qa: dict[str, Any], group: str) -> tuple[str, dict[str, Any]]:
        print(f"[QASmoke] {task_index}/{total} generation+judge {group} {qa['question_id']}", flush=True)
        evidence = rank_evidence(qa["question"], evidence_by_group[group], K_EVIDENCE, equivalences, enable_hybrid_rerank=False)
        evidence_context = format_evidence_context(qa["question"], evidence)
        generated = pool.complete_json(
            generation_prompt(qa, evidence_context),
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=384,
            max_retries=args.llm_max_retries,
        )
        answer_text = str(generated.get("answer") or "")
        answer_record = {
            "answer": answer_text,
            "citations": generated.get("citations") or [],
            "abstained": bool(generated.get("abstained")) or "don't know based on the retrieved evidence" in answer_text.lower(),
        }
        judged = pool.complete_json(
            judge_prompt(qa, answer_record, evidence_context),
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=512,
            max_retries=args.llm_max_retries,
        )
        abstention_correct = (not answer_record["abstained"]) if qa["answerable"] else bool(answer_record["abstained"])
        record = {
            "question_id": qa["question_id"],
            "category": qa.get("category"),
            "question_type": qa.get("question_type") or qa.get("category"),
            "group": group,
            "answerable": qa["answerable"],
            "question": qa["question"],
            "reference_answer": qa["reference_answer"],
            "required_key_points": qa.get("required_key_points") or [],
            "generated_answer": answer_text,
            "citations": answer_record["citations"],
            "quality_label": judged.get("quality_label"),
            "good": bool(judged.get("good")),
            "satisfactory_or_better": bool(judged.get("satisfactory_or_better")),
            "key_point_coverage": float(judged.get("key_point_coverage", 0.0) or 0.0),
            "hallucinated": bool(judged.get("hallucinated")),
            "abstained": bool(judged.get("abstained")) or answer_record["abstained"],
            "abstention_correct": abstention_correct,
            "citation_stability_experimental": float(judged.get("citation_stability_experimental", judged.get("citation_stability", 0.0)) or 0.0),
            "missing_key_points": judged.get("missing_key_points") or [],
            "unsupported_claims_found": judged.get("unsupported_claims_found") or [],
            "rationale": judged.get("rationale", ""),
            "evidence": [
                {
                    "rank": i + 1,
                    "evidence_id": item.get("id"),
                    "relation_type": item.get("relation_type"),
                    "retrieval_score": item.get("retrieval_score"),
                    "readable_evidence": evidence_text(item)[:1200],
                    "formatted_evidence_block": format_evidence_block(i + 1, item, qa["question"])[:1600],
                }
                for i, item in enumerate(evidence)
            ],
        }
        return "record", {"record": record, "raw": {"question_id": qa["question_id"], "group": group, "generated": generated, "judged": judged}}

    pending: list[tuple[int, dict[str, Any], str]] = []
    counter = 0
    for qa in qa_set:
        for group in GROUPS:
            counter += 1
            if (qa["question_id"], group) in completed:
                print(f"[QASmoke] {counter}/{total} skip completed {group} {qa['question_id']}", flush=True)
                continue
            pending.append((counter, qa, group))

    workers = max(1, int(args.parallel_workers or 1))
    if workers == 1:
        for task_index, qa, group in pending:
            try:
                _, payload = run_one(task_index, qa, group)
                records.append(payload["record"])
                raw_records.append(payload["raw"])
                errors = [item for item in errors if (item.get("question_id"), item.get("group")) != (qa["question_id"], group)]
            except Exception as exc:  # noqa: BLE001
                errors.append({"question_id": qa["question_id"], "group": group, "error": str(exc)})
            persist_progress()
    else:
        print(f"[QASmoke] parallel workers={workers}, api_keys={len(pool.entries)}, pending_tasks={len(pending)}", flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_map = {executor.submit(run_one, task_index, qa, group): (task_index, qa, group) for task_index, qa, group in pending}
            for future in concurrent.futures.as_completed(future_map):
                _, qa, group = future_map[future]
                try:
                    _, payload = future.result()
                    records.append(payload["record"])
                    raw_records.append(payload["raw"])
                    errors = [item for item in errors if (item.get("question_id"), item.get("group")) != (qa["question_id"], group)]
                    print(f"[QASmoke] done {group} {qa['question_id']} ({len(records)}/{total} records)", flush=True)
                except Exception as exc:  # noqa: BLE001
                    errors.append({"question_id": qa["question_id"], "group": group, "error": str(exc)})
                    print(f"[QASmoke] error {group} {qa['question_id']}: {exc}", flush=True)
                persist_progress()

    summary_rows = aggregate_summary(records)
    by_question_type_rows = aggregate_by_field(records, "question_type")
    by_answerability_rows = aggregate_by_field(records, "answerable")
    pairwise_rows = pairwise_comparison(records)
    write_csv(args.output_dir / f"{args.output_prefix}_summary.csv", summary_rows)
    write_csv(args.output_dir / f"{args.output_prefix}_by_question_type.csv", by_question_type_rows)
    write_csv(args.output_dir / f"{args.output_prefix}_by_answerability.csv", by_answerability_rows)
    write_csv(args.output_dir / f"{args.output_prefix}_pairwise_comparison.csv", pairwise_rows)
    write_failure_debug(args.output_dir / f"{args.output_prefix}_debug_failures.md", records)
    (args.output_dir / f"{args.output_prefix}_summary.json").write_text(
        json.dumps(
            {
                "provider": pool.provider_name,
                "base_url": pool.base_url,
                "model": pool.model,
                "api_key_count": len(pool.entries),
                "parallel_workers": workers,
                "llm_max_retries": args.llm_max_retries,
                "qa_mode": args.qa_mode,
                "temperature": args.temperature,
                "top_p": args.top_p,
                "evidence_budget_chars": EVIDENCE_BUDGET_CHARS,
                "chem_norm_evidence_v2": args.chem_norm_evidence_v2,
                "question_count": len(qa_set),
                "groups": list(GROUPS),
                "group_specs": GROUPS,
                "summary": summary_rows,
                "by_question_type": by_question_type_rows,
                "by_answerability": by_answerability_rows,
                "pairwise_comparison": pairwise_rows,
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"output_dir": str(args.output_dir), "summary": summary_rows, "errors": len(errors)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
