"""PFAS evidence release using the five retained adapters in the Oct-08 paper.

All accepted caches and previous experiments are read-only. New calls/checkpoints
live on D:. Case1 algorithms are imported, rather than reimplemented under aliases.
"""
from __future__ import annotations

import argparse
import asyncio
import gc
import json
import math
import os
import re
import shutil
import statistics
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np

from scripts.pfas_qa_common import QAClient, MODEL, ENDPOINT, EMBEDDING_MODEL, digest, file_hash, read_json, write_json, utc
from scripts import structured_graph_retrieval as sg
from scripts.final_graph_retrieval import FinalGraphIndex, FinalRetrievalConfig
from scripts.upstream_hyper_query_retrieval import UpstreamHyperQueryRetriever
from scripts.audit_pfas_qa40_scores import source_span_catalog
from scripts.evaluate_shared_retrieval_qrels import metrics as case1_metrics
from scripts import run_qa_smoke_llm as core
from scripts import run_qa_formal_llm as formal
from scripts.run_pfas_qa40 import validate_answer, validate_judge, snapshot, request_stats

BASE = Path(__file__).resolve().parents[2]
QA = Path(r"D:\Hyper-rag-case2-backups\qa40_workspace")
WORK = Path(r"D:\Hyper-rag-case2-backups\case2_case1_aligned_v1")
PUBLIC = BASE / "Hyper-ChE/experiments/case2_pfas_v1"
CACHE = BASE / "case2_pfas_build"
GOLD_HASH = "aebf4e38e16fdf0e811f230d1f699c901e2b657cbbfc161b36b16e43c3f061c1"
GROUPS = {
    "original_hypergraph": {"code": "B0", "cache": "hyper_base", "adapter": "upstream_hyper_query", "domain": "default"},
    "chem_prompt_graph": {"code": "B1", "cache": "hyper_chem_prompt", "adapter": "structured_graph_hybrid_v1", "view": "graph"},
    "chem_prompt_hypergraph": {"code": "B2", "cache": "hyper_chem_prompt", "adapter": "upstream_hyper_query", "domain": "pfas_piezocatalysis"},
    "normalized_final_no_rerank": {"code": "F0", "cache": "hyper_final", "adapter": "normalized_final_hybrid_rrf_v1", "rerank": False},
    "normalized_final": {"code": "F1", "cache": "hyper_final", "adapter": "normalized_final_hybrid_rerank_v1", "rerank": True},
}

GRADE_RULES = """Judge chemical-literature retrieval relevance, blind to system and rank.
Use only the supplied raw chunk, not memory, graph descriptions or the reference
as evidence. The reference and required elements define the information need.
Case1 grade schema:
3 DIRECT: the chunk alone directly answers the question or states the decisive
requested facts. For multi-condition/multi-metric questions, grade 3 requires
the requested entities, conditions, measurements and their binding actually present.
2 STRONG_SUPPORT: a substantial necessary part, but another chunk is needed.
1 BACKGROUND: a concrete useful requested subfact/property/condition/mechanism
or comparison context, insufficient for grade 2.
0 IRRELEVANT: unrelated, generic PFAS discussion, bibliographic, or contradictory
without useful support. Topic overlap alone is not relevance.
Removal, parent degradation, defluorination, and carbon mineralization differ.
Do not mix targets, materials, experiments, conditions, values or units. A negative
question's instruction to abstain is NOT a fact a chunk can support. Grade it by
actual question-specific evidence; if a direct answer contradicts the negative
status, flag negative_answer_found and cite the exact raw span IDs. A packet
cannot establish a corpus-wide absence.
Return JSON {"judgments":[{"chunk_id":"exact supplied ID","relevance_grade":0,
"span_ids":[],"negative_answer_found":false,"rationale":"specific explanation"}]}.
Include every supplied chunk exactly once, in its supplied order. Grade > 0 needs
one or more span IDs from THAT chunk. Grade 0 must use []. Never invent IDs or
quote normalized text. A span ID only points to source text, it does not prove
semantic support. Do not return retrieval-system names or answer quality scores.
"""

FACT_RULES = """Construct source-bounded atomic facts for composite fact recall.
Use the question/rubric only to define what is asked. Use ONLY the offered raw
source spans as factual support. Split distinct requested measurements or claims
into separate atomic facts. Preserve the target/material/condition/metric/value/
unit/relation binding; do not invent operating conditions or split a numeric value
from its denominator. Qualify proposed mechanisms. Removal, parent degradation,
defluorination and carbon mineralization are distinct. Do not force a fact count.
Each fact must be independently fully supported by one source chunk. You may list
multiple spans from that same chunk, but cannot join separate papers into one fact.
Use null for value/unit when genuinely qualitative. Return
{"facts":[{"claim":"one atomic claim","entity":"subject","metric":"property or mechanism",
"value":null,"unit":null,"condition":"source condition or not specified",
"relation":"predicate","rubric_point_ids":[0],"span_ids":["exact offered ID"]}]}.
Every requested rubric point must map to at least one fact; do not add unrelated
facts. Choose exact offered span IDs, not literal rewritten quotations.
"""


def require(flag, message):
    if not flag:
        raise ValueError(message)


def vector(value):
    v = np.asarray(value, dtype=np.float32)
    require(v.shape == (2560,) and np.isfinite(v).all() and np.linalg.norm(v) > 0,
            "Invalid query embedding")
    return v


def validate_keywords(v):
    require(isinstance(v, dict), "Keyword object required")
    for field in ("high_level_keywords", "low_level_keywords"):
        require(isinstance(v.get(field), list) and all(isinstance(x, str) and x.strip() for x in v[field]),
                "Keyword fields must be arrays of nonempty strings")
    require(bool(v["high_level_keywords"] or v["low_level_keywords"]), "Both keyword branches empty")


def label_packet(q, ids, chunks):
    raw = [{"rank": n, "chunk_id": cid, "content": chunks[cid]["content"]} for n, cid in enumerate(ids, 1)]
    return {"query_id": q["question_id"], "question": q["question"], "answerable": q["answerable"],
            "reference_NOT_evidence": q["reference_answer"], "required_elements": q["required_key_points"],
            "chunk_ids": ids, "RAW_SPAN_CATALOG": source_span_catalog({"raw_retrieved_chunks": raw})}


def validate_labels(v, p):
    rows = v.get("judgments")
    require(isinstance(rows, list) and all(isinstance(r, dict) for r in rows), "Judgment list required")
    require([r.get("chunk_id") for r in rows] == p["chunk_ids"], "Incomplete, reordered or wrong chunk IDs")
    for r in rows:
        g = r.get("relevance_grade")
        require(type(g) is int and 0 <= g <= 3, "Grade must be integer 0..3")
        ids = r.get("span_ids")
        require(isinstance(ids, list) and len(set(ids)) == len(ids), "Span list required")
        require(bool(ids) == (g > 0), "Only positive grades require exact source spans")
        require(all(isinstance(i, str) and i in p["RAW_SPAN_CATALOG"] and
                    p["RAW_SPAN_CATALOG"][i]["chunk_id"] == r["chunk_id"] for i in ids),
                "Span must belong to this exact chunk")
        require(type(r.get("negative_answer_found")) is bool and
                (not r["negative_answer_found"] or (not p["answerable"] and g >= 2)), "Invalid negative-answer flag")
        require(isinstance(r.get("rationale"), str) and bool(r["rationale"].strip()), "Source-based rationale required")


def validate_facts(v, p):
    facts = v.get("facts")
    require(isinstance(facts, list) and 0 < len(facts) <= 25, "Nonempty bounded atomic fact list required")
    covered = set()
    for f in facts:
        require(isinstance(f, dict), "Fact object required")
        for field in ("claim", "entity", "metric", "condition", "relation"):
            require(isinstance(f.get(field), str) and f[field].strip(), "Fact binding field missing: " + field)
        require(all(x in f and (f[x] is None or isinstance(f[x], str)) for x in ("value", "unit")), "Value/unit must be present, text or null")
        ids = f.get("span_ids")
        require(isinstance(ids, list) and ids and len(ids) == len(set(ids)) and
                all(isinstance(i, str) and i in p["RAW_SPAN_CATALOG"] for i in ids), "Fact must select offered raw spans")
        require(len({p["RAW_SPAN_CATALOG"][i]["chunk_id"] for i in ids}) == 1,
                "Atomic fact must have complete single-chunk support")
        pts = f.get("rubric_point_ids")
        require(isinstance(pts, list) and pts and len(pts) == len(set(pts)) and
                all(type(i) is int and 0 <= i < len(p["required_elements"]) for i in pts), "Fact/rubric map invalid")
        covered.update(pts)
    require(covered == set(range(len(p["required_elements"]))), "Atomic facts must cover each requested rubric point")
    require(len({f["claim"] for f in facts}) == len(facts), "Duplicate atomic fact claims")


def validate_fact_review(v, facts, packet):
    checks = v.get("fact_checks")
    require(isinstance(checks, list) and [r.get("fact_id") for r in checks] == list(range(len(facts))),
            "Every fact needs a review in order")
    for r, f in zip(checks, facts):
        require(all(type(r.get(k)) is bool for k in ("atomic", "supported", "numeric_unit_binding_valid", "question_relevant")),
                "Review boolean fields required")
        require(isinstance(r.get("reason"), str) and r["reason"].strip(), "Specific fact-review reason required")
        ids = r.get("support_span_ids")
        require(isinstance(ids, list) and all(i in f["span_ids"] for i in ids), "Review support must select this fact's spans")
        if all(r[k] for k in ("atomic", "supported", "numeric_unit_binding_valid", "question_relevant")):
            require(bool(ids), "Accepted fact requires selected source span")


def protected_hashes():
    # Reuse the previous *path/expected-hash manifest*, not cached observations.
    # Its 329 published files live directly below case2, not variant subfolders.
    # Re-read every byte and require continuity with the accepted release.
    result = read_json(QA / "shared_retrieval_v1/preservation_before.json")["hashes"].copy()
    for i, (name, expected) in enumerate(result.items(), 1):
        require(Path(name).is_file() and file_hash(name) == expected, "Prior accepted evidence changed: " + name)
        if i % 250 == 0: print(json.dumps({"stage": "preservation", "checked": i}), flush=True)
    for folder in ("gold_v2", "evaluation_v2", "score_audit_v1", "final_report", "human_reviewed_release_20261015", "shared_retrieval_v1"):
        for p in sorted((QA / folder).rglob("*")):
            if p.is_file() and str(p) not in result:
                result[str(p)] = file_hash(p)
    core_files = ("run_config.json", "kv_store_full_docs.json", "kv_store_text_chunks.json", "kv_store_llm_response_cache.json",
                  "vdb_chunks.json", "vdb_entities.json", "vdb_relationships.json", "hypergraph_chunk_entity_relation.hgdb",
                  "canonical_entity_map.json", "normalization_candidates.jsonl", "normalization_decisions.jsonl",
                  "normalization_audit.jsonl", "final_validation.json", "measurement_occurrences.jsonl")
    for name in ("hyper_base", "hyper_chem_prompt", "hyper_norm", "hyper_final"):
        for fn in core_files:
            p = CACHE / name / fn
            if p.is_file() and str(p) not in result: result[str(p)] = file_hash(p)
    return result


def protocol():
    return {"version": "case2-paper-aligned-five-v1", "groups": GROUPS, "gold_sha256": GOLD_HASH,
            "case1_reference": "Hyper-ChE/experiments/final_v1; paper/latex/hyperche_arxiv_body.tex (Oct 08)",
            "documents": 60, "chunks": 1330, "queries": 40, "answerable": 35,
            "top_k_candidates": 20, "metric_k": 5, "thresholds": [1, 2, 3], "headline_threshold": 2,
            "mrr_scope": "all returned top20", "zero_idcg": "0 included in macro average",
            "structured_config": sg.StructuredRetrievalConfig().as_dict(),
            "upstream_config": {"graph_top_k": 60, "entity_quota": 10, "relation_quota": 10, "query_expansion": False},
            "final_pool": "same final cache; hybrid RRF top50 before rerank; paired pool equality required",
            "label_rules_sha256": digest(GRADE_RULES), "fact_rules_sha256": digest(FACT_RULES),
            "qrels_pool": "five systems top20 plus all 521 historical pool pairs (unranked seed pairs retain shared IDCG)",
            "qrels_method": "case1 DIRECT/STRONG_SUPPORT/BACKGROUND/IRRELEVANT; new independent protocol; machine annotated",
            "old_qrels_reuse": False, "old_qrels_difference": "old grade3 required all rubric points, not the case1 grade rubric",
            "cfr": "exact supporting-chunk hit in top5, micro facts and macro positive-query facts; no joint-point proxy",
            "qa_groups": ["normalized_final"], "qa_evidence_format": "legacy", "qa_budget_option": 1500,
            "qa_budget_actual_unit": "token_count in existing case1 code, despite option evidence_budget_chars",
            "llm": MODEL, "endpoint": ENDPOINT, "temperature": 0, "reasoning_effort": "low",
            "max_actual_requests": 10, "max_per_physical_key": 1, "embedding": EMBEDDING_MODEL, "dimension": 2560,
            "efu_repair": False, "new_corpus_embedding": False, "query_embedding": "actual keyword texts only; reuse raw-question vectors",
            "new_annotations_human_confirmed": False, "original_qa40_human_review_confirmed": True}


class Run:
    def __init__(self, work):
        self.work = work
        self.gold = read_json(QA / "gold_v2/qa_gold.json")
        require(file_hash(QA / "gold_v2/qa_gold.json") == GOLD_HASH, "Frozen gold changed")
        self.questions = self.gold["qa_questions"]
        self.byq = {q["question_id"]: q for q in self.questions}
        self.chunks = read_json(self.gold["source"]["chunks"])
        require(len(self.chunks) == 1330 and file_hash(self.gold["source"]["chunks"]) == self.gold["source"]["chunks_sha256"], "Source chunks changed")
        self.status = {"started_at": utc(), "stage": "prepare", "complete": False, "counts": {}, "errors": []}
        self.client = None
        self.embedding_locks = defaultdict(asyncio.Lock)
        self.stage_lock = asyncio.Lock()

    def progress(self, **updates):
        self.status.update(updates, updated_at=utc(), actual_requests=request_stats())
        write_json(self.work / "progress.json", self.status)

    async def tracked(self, stage, key, fn):
        try:
            await fn()
            self.status["counts"][stage] = self.status["counts"].get(stage, 0) + 1
            self.progress()
            print(json.dumps({"stage": stage, "item": key, "done": self.status["counts"][stage]}), flush=True)
        except Exception as exc:
            row = {"stage": stage, "item": key, "error_type": type(exc).__name__}
            if isinstance(exc, ValueError): row["validation_error"] = str(exc)[:220]
            self.status["errors"].append(row)
            self.progress()
            print(json.dumps({"failed": row}), flush=True)

    async def call(self, prompt, validator, label, role="judge"):
        # Bounded retries always start from the clean prompt, not a rejected
        # assistant response. Every raw attempt remains in QAClient's call log.
        errors = []
        for budget in (4096, 8192, 16384):
            try:
                return await self.client.json(prompt, validator=validator, label=label, role=role, budgets=(budget,), recover_attempts=True)
            except (RuntimeError, ValueError) as exc:
                errors.append(type(exc).__name__)
        raise RuntimeError("Bounded call exhausted: " + ",".join(errors))

    async def embed(self, text):
        signature = digest({"text": text, "model": EMBEDDING_MODEL, "dimension": 2560})
        async with self.embedding_locks[signature]:
            p = self.work / "keyword_query_vectors" / (signature + ".json")
            if p.exists():
                row = read_json(p)
                require(row["signature"] == signature and row["text"] == text, "Keyword vector signature mismatch")
                return vector(row["vector"])
            result = vector((await self.client.embed([text]))[0])
            write_json(p, {"signature": signature, "text": text, "model": EMBEDDING_MODEL, "dimension": 2560, "vector": result.tolist()})
            return result

    def raw_vector(self, q):
        row = read_json(QA / "evaluation_v2/query_vectors" / (q["question_id"] + ".json"))
        require(row["signature"] == digest({"query": q["question"], "model": EMBEDDING_MODEL, "dim": 2560}), "Frozen query vector mismatch")
        return vector(row["vector"])

    async def retrieval(self):
        self.progress(stage="retrieval")
        sg.CHUNK_ID_RE = re.compile(r"(?:PFAS|RFB)_\d+_CHK_\d+", re.I)
        loop = asyncio.get_running_loop()
        async def keywords(prompt):
            return await self.call(prompt, validate_keywords, "upstream_keywords", role="answer")
        def llm_sync(prompt): return asyncio.run_coroutine_threadsafe(keywords(prompt), loop).result(timeout=900)
        def embed_sync(text): return asyncio.run_coroutine_threadsafe(self.embed(text), loop).result(timeout=500)
        for group, spec in GROUPS.items():
            if spec["adapter"] == "upstream_hyper_query":
                index = UpstreamHyperQueryRetriever(CACHE / spec["cache"], llm_json_func=llm_sync, embedding_func=embed_sync,
                    embedding_dim=2560, graph_top_k=60, query_domain=spec["domain"], entity_quota=10, relation_quota=10, enable_query_expansion=False)
            elif group == "chem_prompt_graph": index = sg.StructuredGraphIndex(CACHE / spec["cache"])
            else: index = FinalGraphIndex(CACHE / spec["cache"])
            slots = asyncio.Semaphore(3 if spec["adapter"] == "upstream_hyper_query" else 1)
            async def one(q):
                async with slots:
                    p = self.work / "retrieval" / group / (q["question_id"] + ".json")
                    sig = digest({"protocol": protocol(), "question": q["question"], "group": group})
                    if p.exists():
                        r = read_json(p)
                        require(r["signature"] == sig, "Retrieval checkpoint protocol mismatch")
                    else:
                        if spec["adapter"] == "upstream_hyper_query":
                            mapped, audit = await asyncio.to_thread(index.search, q["question"], top_k=20)
                            require(not audit.get("unmatched_text_units") and not audit.get("ambiguous_text_units"), "Unresolved upstream source mapping")
                            evidence = [{"id": m["chunk_id"], "source_chunk_id": m["chunk_id"],
                                "source_doc_id": self.chunks[m["chunk_id"]]["source_doc_id"],
                                "chunk_content": self.chunks[m["chunk_id"]]["content"],
                                "mapping_method": m.get("mapping_method"), "retrieval_branch": m.get("retrieval_branch")} for m in mapped]
                        else:
                            cfg = sg.StructuredRetrievalConfig() if group == "chem_prompt_graph" else FinalRetrievalConfig(enable_rerank=spec["rerank"])
                            evidence = await asyncio.to_thread(index.search, q["question"], self.raw_vector(q),
                                view=spec.get("view", "hyper"), top_k=20, config=cfg)
                            audit = {"config": cfg.as_dict()}
                        ids = [e["source_chunk_id"] for e in evidence]
                        require(len(ids) <= 20 and len(ids) == len(set(ids)) and all(cid in self.chunks for cid in ids), "Invalid frozen top20")
                        r = {"signature": sig, "query_id": q["question_id"], "system": group, "chunk_ids": ids,
                             "evidence": evidence, "audit": audit, "completed_at": utc()}
                        write_json(p, r)
            await asyncio.gather(*(self.tracked("retrieval", group + ":" + q["question_id"], lambda q=q: one(q)) for q in self.questions))
            del index
            gc.collect()
        require(self.status["counts"].get("retrieval") == 200, "Five-group retrieval incomplete")
        pairs = []
        for q in self.questions:
            a, b = [read_json(self.work / "retrieval" / group / (q["question_id"] + ".json")) for group in ("normalized_final_no_rerank", "normalized_final")]
            require(bool(a["evidence"]) == bool(b["evidence"]), "F0/F1 empty-pool mismatch")
            for field in ("candidate_edge_ids", "candidate_chunk_ids"):
                av = a["evidence"][0][field] if a["evidence"] else []
                bv = b["evidence"][0][field] if b["evidence"] else []
                require(av == bv, "F0/F1 candidate pool mismatch")
            pairs.append({"query_id": q["question_id"], "identical_pool": True,
                          "same_top5": a["chunk_ids"][:5] == b["chunk_ids"][:5]})
        write_json(self.work / "paired_pool_acceptance.json", {"passed": True, "queries": pairs})
        seed = read_json(QA / "shared_retrieval_v1/metric_scope_v1/effective_labels/qrels.json")["qrels"]
        pool = {(r["query_id"], r["chunk_id"]): {"query_id": r["query_id"], "chunk_id": r["chunk_id"], "system_occurrences": [], "historical_seed": True} for r in seed}
        for group in GROUPS:
            for q in self.questions:
                r = read_json(self.work / "retrieval" / group / (q["question_id"] + ".json"))
                for rank, cid in enumerate(r["chunk_ids"], 1):
                    row = pool.setdefault((q["question_id"], cid), {"query_id": q["question_id"], "chunk_id": cid, "system_occurrences": [], "historical_seed": False})
                    row["system_occurrences"].append({"system": group, "retrieval_rank": rank, "candidate_id": group + ":" + cid})
        write_json(self.work / "candidate_rankings.json", {"version": "public-id-rank-export-v1", "retained_systems": list(GROUPS), "candidate_union": [pool[k] for k in sorted(pool)]})

    async def labels(self):
        self.progress(stage="shared_qrels")
        pool = read_json(self.work / "candidate_rankings.json")["candidate_union"]
        byq = defaultdict(list)
        for row in pool: byq[row["query_id"]].append(row["chunk_id"])
        jobs = [(qid, ids[i:i+4]) for qid, ids in byq.items() for i in range(0, len(ids), 4)]
        slots = asyncio.Semaphore(10)
        async def one(qid, ids):
            async with slots:
                p = label_packet(self.byq[qid], ids, self.chunks)
                sig = digest({"rules": GRADE_RULES, "packet": p})
                path = self.work / "qrel_batches" / (sig + ".json")
                if path.exists():
                    row = read_json(path)
                    require(row["signature"] == sig, "Qrel signature mismatch")
                    validate_labels(row["judgment"], p)
                else:
                    val = await self.call(GRADE_RULES + "\n" + json.dumps(p, ensure_ascii=False), lambda v: validate_labels(v, p), "qrels:" + qid)
                    write_json(path, {"signature": sig, "packet": p, "judgment": val, "human_confirmed": False})
        await asyncio.gather(*(self.tracked("qrel_batches", qid + ":" + ids[0], lambda qid=qid, ids=ids: one(qid, ids)) for qid, ids in jobs))
        require(self.status["counts"].get("qrel_batches") == len(jobs), "Unfinished pooled qrels")
        qrels = []
        conflicts = set()
        for qid, ids in jobs:
            p = label_packet(self.byq[qid], ids, self.chunks)
            sig = digest({"rules": GRADE_RULES, "packet": p})
            row = read_json(self.work / "qrel_batches" / (sig + ".json"))
            for r in row["judgment"]["judgments"]:
                if r["negative_answer_found"]: conflicts.add(qid)
                qrels.append({"query_id": qid, **r, "human_confirmed": False,
                              "exact_support_spans": [p["RAW_SPAN_CATALOG"][i] for i in r["span_ids"]]})
        write_json(self.work / "shared_qrels.json", {"version": "case1-rubric-pfas-pool-v1", "qrels": qrels})
        write_json(self.work / "manual_skips.json", [{"query_id": qid, "reason": "New raw source appears to contradict the negative-question status; excluded for ALL groups pending human scientific review"} for qid in sorted(conflicts)])

    async def facts(self):
        self.progress(stage="atomic_facts")
        slots = asyncio.Semaphore(10)
        async def one(q):
            async with slots:
                p = label_packet(q, sorted(q["gold_chunk_ids"]), self.chunks)
                sig = digest({"rules": FACT_RULES, "packet": p})
                path = self.work / "facts" / (q["question_id"] + ".json")
                if path.exists():
                    row = read_json(path)
                    require(row["signature"] == sig, "Atomic fact signature mismatch")
                    validate_facts(row["generation"], p)
                    validate_fact_review(row["review"], row["generation"]["facts"], p)
                    return
                val = await self.call(FACT_RULES + "\n" + json.dumps(p, ensure_ascii=False), lambda v: validate_facts(v, p), "facts:" + q["question_id"])
                prompt = "Independently audit EVERY proposed atomic fact against its selected raw spans and the question. Do not accept because a previous model proposed it. Check atomicity, complete target/material/condition/value/unit binding and scientific scope. Missing or contradicted facts are false, not auto-corrected. Return JSON {\"fact_checks\":[{\"fact_id\":0,\"atomic\":true,\"supported\":true,\"numeric_unit_binding_valid\":true,\"question_relevant\":true,\"support_span_ids\":[],\"reason\":\"source-specific explanation\"}]} in exact order.\n" + json.dumps({"packet": p, "facts": val["facts"]}, ensure_ascii=False)
                review = await self.call(prompt, lambda v: validate_fact_review(v, val["facts"], p), "fact_review:" + q["question_id"])
                write_json(path, {"signature": sig, "packet": p, "generation": val, "review": review})
        positive = [q for q in self.questions if q["answerable"]]
        await asyncio.gather(*(self.tracked("fact_queries", q["question_id"], lambda q=q: one(q)) for q in positive))
        require(self.status["counts"].get("fact_queries") == 35, "Atomic fact verification incomplete")
        queries, rejected = [], []
        for q in positive:
            row = read_json(self.work / "facts" / (q["question_id"] + ".json"))
            facts = []
            for i, (f, review) in enumerate(zip(row["generation"]["facts"], row["review"]["fact_checks"])):
                if not all(review[k] for k in ("atomic", "supported", "numeric_unit_binding_valid", "question_relevant")):
                    rejected.append({"query_id": q["question_id"], "fact_index": i, "fact": f, "review": review})
                    continue
                spans = [row["packet"]["RAW_SPAN_CATALOG"][x] for x in review["support_span_ids"]]
                facts.append({**f, "fact_id": q["question_id"] + "|fact:" + str(i + 1), "query_id": q["question_id"],
                              "supporting_chunk_ids": sorted({x["chunk_id"] for x in spans}),
                              "support_span": "\n\n".join(x["exact_raw_text"] for x in spans), "exact_support_spans": spans,
                              "accepted_by_user": False, "acceptance_method": "same_llm_separate_prompt_source_audit", "review": review})
            queries.append({"query_id": q["question_id"], "atomic_facts": facts})
        write_json(self.work / "composite_fact_gold_machine_verified.json", {"version": "pfas-source-atomic-facts-v1", "status": "machine_verified", "human_confirmed": False, "queries": queries})
        write_json(self.work / "rejected_facts.json", rejected)
        require(all(q["atomic_facts"] for q in queries), "A supported query has no verified atomic facts")

    async def qa(self):
        self.progress(stage="f1_supplementary_qa")
        core.EVIDENCE_BUDGET_CHARS = 1500
        slots = asyncio.Semaphore(10)
        async def one(q):
            async with slots:
                r = read_json(self.work / "retrieval/normalized_final" / (q["question_id"] + ".json"))
                evidence = r["evidence"][:5]
                context = core.format_evidence_context(q["question"], evidence, evidence_format="legacy")
                sig = digest({"question": q, "context": context, "protocol": protocol()})
                p = self.work / "qa/records" / (q["question_id"] + ".json")
                if p.exists():
                    require(read_json(p)["signature"] == sig, "F1 QA protocol mismatch")
                    return
                def valid_citations(v):
                    validate_answer(v)
                    shown = {"Evidence " + x for x in re.findall(r"(?m)^Evidence (\d+)\s*$", context)}
                    require(all(c in shown for c in v["citations"]), "Answer cites unshown evidence")
                answer = await self.call(core.generation_prompt(q, context), valid_citations, "f1_qa:" + q["question_id"], role="answer")
                judged = await self.call(formal.formal_judge_prompt(q, answer, context) +
                    "\nPFAS metric rule: removal, parent degradation, defluorination, carbon mineralization are distinct. Missing detail alone is not a hallucination.",
                    lambda v: validate_judge(v, q, answer["abstained"]), "f1_judge:" + q["question_id"])
                record = {**q, "signature": sig, "group": "normalized_final", "generated_answer": answer["answer"],
                          "citations": answer["citations"], **judged, "abstained": answer["abstained"],
                          "key_point_coverage": len(judged["covered_key_points"]) / len(q["required_key_points"]),
                          **formal.citation_metrics(answer["citations"], len(evidence), answer["abstained"]),
                          "context": context, "context_token_count": core.token_count(context),
                          "retrieved_chunk_ids": r["chunk_ids"][:5], "completed_at": utc(), "human_confirmed_result": False}
                write_json(p, record)
        await asyncio.gather(*(self.tracked("qa", q["question_id"], lambda q=q: one(q)) for q in self.questions))
        require(self.status["counts"].get("qa") == 40, "F1 supplementary QA incomplete")

    async def execute(self, stage):
        self.work.mkdir(parents=True, exist_ok=True)
        write_json(self.work / "process.json", {"pid": os.getpid(), "started_at": utc(), "stage": stage})
        proto = protocol()
        if (self.work / "protocol.json").exists(): require(read_json(self.work / "protocol.json") == proto, "Frozen alignment protocol changed")
        else: write_json(self.work / "protocol.json", proto)
        preserved = self.work / "preservation_before.json"
        if preserved.exists():
            before = read_json(preserved)
            require(all(Path(p).exists() and file_hash(p) == h for p, h in before.items()), "Protected original evidence changed")
        else:
            before = protected_hashes()
            write_json(preserved, before)
        self.client = QAClient(self.work / "api")
        try:
            stages = ("retrieval", "labels", "facts", "qa") if stage == "all" else (stage,)
            for name in stages:
                await getattr(self, name)()
            unchanged = all(Path(p).exists() and file_hash(p) == h for p, h in before.items())
            write_json(self.work / "preservation_after.json", {"unchanged": unchanged, "protected_files": len(before), "at": utc()})
            require(unchanged, "Accepted original artifacts changed")
            self.progress(stage="ready_for_package" if stage == "all" else stage + "_completed", complete=True, finished_at=utc())
            if stage == "all":
                from scripts.package_pfas_case1 import export
                export(self.work)
                self.progress(stage="completed_and_packaged", complete=True, finished_at=utc())
        except Exception as exc:
            self.progress(stage="incomplete", terminal_error_type=type(exc).__name__)
            if isinstance(exc, ValueError): self.status["terminal_validation_error"] = str(exc)[:250]
            self.progress()
            return 2
        finally:
            await self.client.close()
        return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path, default=WORK)
    p.add_argument("--stage", choices=("all", "retrieval", "labels", "facts", "qa"), default="all")
    args = p.parse_args()
    return asyncio.run(Run(args.work).execute(args.stage))


if __name__ == "__main__":
    raise SystemExit(main())
