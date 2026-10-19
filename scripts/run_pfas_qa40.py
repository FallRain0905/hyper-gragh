"""Evaluate frozen machine-reviewed PFAS40 using shared read-only retrieval.

Results are an automated benchmark, not human-confirmed publication gold.
"""
from __future__ import annotations

import argparse
import asyncio
import gc
import json
import re
import sys
from pathlib import Path

import numpy as np

from scripts.pfas_qa_common import QAClient, digest, file_hash, read_json, utc, write_json
from scripts import run_qa_formal_llm as formal
from scripts import run_qa_smoke_llm as core
from scripts import structured_graph_retrieval as structured
from scripts.final_graph_retrieval import FinalGraphIndex, FinalRetrievalConfig
from scripts.verify_pfas_qa40 import validate_supported, validate_audit

GROUPS = {
    "original_hypergraph": {"cache": "hyper_base", "view": "hyper", "label": "Original Hyper-RAG"},
    "chem_prompt_graph": {"cache": "hyper_chem_prompt", "view": "graph", "label": "Chemistry Binary Graph"},
    "chem_prompt_hypergraph": {"cache": "hyper_chem_prompt", "view": "hyper", "label": "Chemistry Hypergraph"},
    "hybrid_text": {"cache": "hyper_chem_prompt", "view": "text", "label": "BM25 + Dense + RRF Text"},
    "normalized_hypergraph": {"cache": "hyper_norm", "view": "hyper", "label": "Normalized Hypergraph"},
    "final_hypergraph": {"cache": "hyper_final", "view": "hyper", "label": "Final Hypergraph with Measurements"},
}
TRACKED = ["run_config.json", "kv_store_full_docs.json", "kv_store_text_chunks.json",
           "kv_store_llm_response_cache.json", "vdb_chunks.json", "vdb_entities.json",
           "vdb_relationships.json", "hypergraph_chunk_entity_relation.hgdb"]


def evidence_context(evidence, chunks):
    blocks = []
    for rank, row in enumerate(evidence, 1):
        cid = row.get("source_chunk_id") or row.get("id")
        if cid not in chunks:
            raise ValueError("Retrieval evidence does not resolve to raw chunk")
        raw = chunks[cid]["content"]
        rel = row.get("supporting_relations") or []
        # Uniform source text and relationship cap; graph statements are secondary
        # hints and must be checked against the actual raw source.
        hints = json.dumps(rel[:3], ensure_ascii=False, default=str)[:1200]
        blocks.append(f"Evidence {rank}\nSource: {cid} / {chunks[cid]['source_doc_id']}\n"
                      + ("Structured hints (verify against raw text): " + hints + "\n" if rel else "")
                      + "Complete raw source chunk:\n" + raw)
    return "\n\n".join(blocks)


def judge_prompt(qa, answer, context):
    quotes = [{"chunk_id": e["chunk_id"], "quote": e["quote"]} for e in qa.get("evidence", [])]
    return formal.formal_judge_prompt(qa, answer, context) + "\nAdditional PFAS rules: distinguish removal, parent degradation, defluorination and carbon mineralization; respect exact target/material/condition/denominator binding. Cite support in RAW retrieved chunks; structured hints alone are insufficient. A correct abstention on an unanswerable question can be GOOD. Do not penalize a source-qualified statement merely for using cautious language. The gold is automated and may be imperfect: flag any reference conflict in rationale. Exact gold raw spans for checking reference correctness (NOT added to retrieved answer evidence):\n" + json.dumps(quotes, ensure_ascii=False)


def snapshot(cache_root, groups):
    return {name: {fn: file_hash(cache_root / name / fn) for fn in TRACKED}
            for name in sorted({s["cache"] for s in groups.values()})}


def validate_answer(value):
    require_validation(core.validate_generation(value))
    if not value["answer"].strip():
        raise ValueError("Empty answer cannot complete a QA item")
    if any(not isinstance(c, str) for c in value["citations"]):
        raise ValueError("Citations must be text labels")
    explicit_refusal = value["answer"].strip().lower().startswith("i don't know based on the retrieved evidence")
    if explicit_refusal and not value["abstained"]:
        raise ValueError("Explicit refusal must be marked abstained")


def validate_judge(value, qa, abstained):
    require_validation(formal.validate_formal_judgment(value, qa["required_key_points"], abstained))
    label = value["quality_label"]
    if value["good"] != (label == "GOOD") or value["satisfactory_or_better"] != (label in ("GOOD", "SATISFACTORY")):
        raise ValueError("Quality booleans must agree with quality_label")
    if label in ("GOOD", "SATISFACTORY") and value["hallucinated"]:
        raise ValueError("A hallucinated answer must be POOR")
    if label == "GOOD" and value["missing_key_points"]:
        raise ValueError("GOOD requires every scoring point")


async def run(args):
    gold = read_json(args.gold)
    freeze = read_json(args.gold.parent / "freeze_manifest.json")
    if file_hash(args.gold) != freeze["gold_sha256"] or gold.get("status") != "machine_verified_gold":
        raise ValueError("Gold freeze gate failed")
    questions = gold["qa_questions"]
    if len(questions) != 40 or len({q["question_id"] for q in questions}) != 40:
        raise ValueError("Need exactly 40 unique questions")
    if not all(q.get("required_key_points") for q in questions):
        raise ValueError("Every item requires a scoring rubric")
    if sum(q["answerable"] is True for q in questions) != 35:
        raise ValueError("Frozen PFAS protocol requires 35 supported and 5 negative items")
    raw_chunks = read_json(gold["source"]["chunks"])
    if file_hash(gold["source"]["chunks"]) != gold["source"]["chunks_sha256"]:
        raise ValueError("Gold raw sources changed")
    for q in questions:
        if q["answerable"]:
            validate_supported(q, raw_chunks, raw_chunks)
            validate_audit(q["audit"], q["required_key_points"])
            if not q["audit"]["accepted"]:
                raise ValueError("Reference audit did not accept question")
        elif len(q.get("full_corpus_absence_audit", {}).get("documents", [])) != 60:
            raise ValueError("Negative gold lacks all 60 document audits")
    del raw_chunks
    selected = list(GROUPS) if args.groups == "all" else args.groups.split(",")
    groups = {name: GROUPS[name] for name in selected}
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    protocol = {"version": "pfas-qa40-six-group-v1", "gold_sha256": freeze["gold_sha256"], "groups": groups,
                "qa_model": "deepseek-ai/DeepSeek-V4-Flash", "endpoint": "https://api.siliconflow.cn/v1",
                "query_embedding_model": "Qwen/Qwen3-Embedding-4B", "dimension": 2560,
                "top_k": 5, "source_budget": "5 complete raw chunks plus at most 1200 chars of structured hints per chunk",
                "concurrency": 10, "per_key": 1, "temperature": 0, "reasoning_effort": "low",
                "gold_source_filtering": False, "human_confirmed_gold": False,
                "index_config": structured.StructuredRetrievalConfig().as_dict()}
    protocol_path = output / "protocol.json"
    if protocol_path.exists() and read_json(protocol_path) != protocol:
        raise ValueError("Output protocol changed; resume requires identical settings")
    write_json(protocol_path, protocol)
    original_hashes = snapshot(args.cache_root, groups)
    before_path = output / "cache_hashes_before.json"
    if before_path.exists() and read_json(before_path) != original_hashes:
        raise ValueError("Read-only cache changed since original evaluation")
    write_json(before_path, original_hashes)
    client = QAClient(output)
    status = {"stage": "query_embeddings", "started_at": utc(), "records_done": 0,
              "records_total": 40 * len(groups), "errors": [], "complete": False}
    write_json(output / "progress.json", status)
    vectors = {}
    try:
        vector_slots = asyncio.Semaphore(10)
        async def embed_question(q):
          async with vector_slots:
            path = output / "query_vectors" / (q["question_id"] + ".json")
            sig = digest({"query": q["question"], "model": "Qwen/Qwen3-Embedding-4B", "dim": 2560})
            if path.exists():
                row = read_json(path)
                if row["signature"] != sig:
                    raise ValueError("Query-vector checkpoint differs from question")
                v = np.asarray(row["vector"], dtype=np.float32)
            else:
                v = (await client.embed([q["question"]]))[0]
                write_json(path, {"signature": sig, "model": "Qwen/Qwen3-Embedding-4B", "dimension": 2560, "vector": v.tolist()})
            if v.shape != (2560,) or not np.isfinite(v).all() or not np.any(v):
                raise ValueError("Invalid query vector")
            vectors[q["question_id"]] = v
            status.update(query_vectors_done=len(vectors), actual_requests=request_stats(), updated_at=utc())
            write_json(output / "progress.json", status)
        await asyncio.gather(*(embed_question(q) for q in questions))
        # Adapt identifiers only in this QA process; preserve existing RFB protocol.
        structured.CHUNK_ID_RE = re.compile(r"(?:PFAS|RFB)_\d+_CHK_\d+", re.IGNORECASE)
        records = []
        for group, spec in groups.items():
            status.update(stage="answer_and_judge", group=group)
            write_json(output / "progress.json", status)
            cache = args.cache_root / spec["cache"]
            chunks = read_json(cache / "kv_store_text_chunks.json")
            if len(chunks) != 1330 or {v["source_doc_id"] for v in chunks.values()} != {f"PFAS_{i:03d}" for i in range(1, 61)}:
                raise ValueError("PFAS cache corpus gate failed")
            config = read_json(cache / "run_config.json")
            if config.get("enable_efu_repair") is not False:
                raise ValueError("EFU repair must be false")
            if spec["view"] == "text":
                class Pool:
                    dimension = 2560
                    vector = None
                    def embed(self, _text):
                        return self.vector
                pool = Pool()
                index = formal.HybridTextRetriever(cache, pool)
                retrieval_config = None
            else:
                index = FinalGraphIndex(cache) if group == "final_hypergraph" else structured.StructuredGraphIndex(cache)
                retrieval_config = FinalRetrievalConfig() if group == "final_hypergraph" else structured.StructuredRetrievalConfig()
                write_json(output / f"{group}_mapping_audit.json", index.mapping_audit)
            pending = []
            for q in questions:
                path = output / "records" / group / (q["question_id"] + ".json")
                if path.exists():
                    record = read_json(path)
                    if record["protocol_sha256"] != digest(protocol):
                        raise ValueError("Completed record protocol mismatch")
                    validate_answer({"answer": record["generated_answer"], "citations": record["citations"], "abstained": record["abstained"]})
                    validate_judge(record, q, record["abstained"])
                    records.append(record)
                    status["records_done"] += 1
                    continue
                if spec["view"] == "text":
                    pool.vector = vectors[q["question_id"]]
                    evidence = index.search(q["question"], 5)
                else:
                    evidence = index.search(q["question"], vectors[q["question_id"]], view=spec["view"], top_k=5, config=retrieval_config)
                context = evidence_context(evidence, chunks)
                write_json(output / "retrieval" / group / (q["question_id"] + ".json"),
                           {"evidence": evidence, "context": context, "retrieved_chunk_ids": [e.get("source_chunk_id") or e["id"] for e in evidence]})
                pending.append((q, evidence, context, path))
            semaphore = asyncio.Semaphore(10)
            lock = asyncio.Lock()

            async def one(q, evidence, context, path):
                async with semaphore:
                    try:
                        generated = await client.json(core.generation_prompt(q, context)
                            + "\nUse the raw source text to verify structured hints. Keep mineralization and defluorination distinct.",
                            validator=validate_answer, label=group + ":" + q["question_id"] + ":answer")
                        judged = await client.json(judge_prompt(q, generated, context), role="judge",
                            validator=lambda v: validate_judge(v, q, generated["abstained"]),
                            label=group + ":" + q["question_id"] + ":judge")
                        label = judged["quality_label"]
                        ids = [e.get("source_chunk_id") or e["id"] for e in evidence]
                        citation = formal.citation_metrics(generated["citations"], len(evidence), generated["abstained"])
                        record = {**q, "group": group, "group_label": spec["label"], "generated_answer": generated["answer"],
                                  "citations": generated["citations"], "abstained": generated["abstained"],
                                  **judged, **citation, "good": label == "GOOD", "satisfactory_or_better": label in ("GOOD", "SATISFACTORY"),
                                  "key_point_coverage": len(judged["covered_key_points"]) / len(q["required_key_points"]),
                                  "retrieved_chunk_ids": ids,
                                  "gold_chunk_recall_at5": len(set(ids) & set(q["gold_chunk_ids"])) / len(q["gold_chunk_ids"]) if q["gold_chunk_ids"] else None,
                                  "protocol_sha256": digest(protocol), "completed_at": utc()}
                        write_json(path, record)
                        async with lock:
                            records.append(record)
                            status["records_done"] += 1
                            status["updated_at"] = utc()
                            status["actual_requests"] = request_stats()
                            write_json(output / "progress.json", status)
                            print(json.dumps({"done": q["question_id"], "group": group, "records": status["records_done"]}), flush=True)
                    except Exception as e:
                        async with lock:
                            status["errors"].append({"group": group, "question_id": q["question_id"], "error_type": type(e).__name__})
                            write_json(output / "progress.json", status)
                            print(json.dumps({"failed": q["question_id"], "group": group, "error_type": type(e).__name__}), flush=True)

            await asyncio.gather(*(one(*p) for p in pending))
            del index, chunks, pending
            gc.collect()
        after = snapshot(args.cache_root, groups)
        unchanged = original_hashes == after
        write_json(output / "cache_hashes_after.json", after)
        status.update(complete=len(records) == status["records_total"] and not status["errors"] and unchanged,
                      cache_files_unchanged=unchanged, finished_at=utc())
        status.update(stage="completed" if status["complete"] else "incomplete", actual_requests=request_stats())
        summary = formal.aggregate_summary(records, groups)
        for row in summary:
            vals = [r["gold_chunk_recall_at5"] for r in records if r["group"] == row["group"] and r["gold_chunk_recall_at5"] is not None]
            row["Gold Chunk Recall@5"] = round(float(np.mean(vals)), 4) if vals else None
            if not any(not r["answerable"] for r in records if r["group"] == row["group"]):
                row["False Answer Rate"] = None
                row["Unanswerable Abstention Accuracy"] = None
        write_json(output / "summary.json", {"protocol": protocol, "status": status, "groups": summary,
                    "limitations": ["Gold and judge use the same LLM in separate calls; no independent human confirmation.",
                                    "Supported references cover a subset of corpus documents; absence checks cover all 60.",
                                    "Benchmark source annotations are not exhaustive relevance judgments."]})
        formal.write_csv(output / "summary.csv", summary)
        write_json(output / "progress.json", status)
        return 0 if status["complete"] else 2
    finally:
        await client.close()


def require_validation(pair):
    if not pair[0]:
        raise ValueError(pair[1])


def request_stats():
    from runtime_requests import QA_REQUEST_LIMITER
    return QA_REQUEST_LIMITER.snapshot()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--groups", default="all")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args)))


if __name__ == "__main__":
    main()
