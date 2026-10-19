"""Offline, case1-identical table schemas and chunk-derived source diagnostics."""
import csv
import json
import shutil
import statistics
import subprocess
import sys
from collections import defaultdict

from scripts.align_pfas_case1 import BASE, QA, WORK, PUBLIC, GROUPS, require
from scripts.pfas_qa_common import read_json, write_json, file_hash, utc
from scripts.run_qa_formal_llm import write_csv


SOURCE_POLICY = "A query is a source hit when a top-5 retrieved chunk from that source has qrel at or above the threshold."
SOURCE_INTERPRETATION = "chunk-derived source diagnostic; because relevance is currently judged at (query_id, chunk_id), this binary value is expected to equal chunk Hit@5 until source-level qrels are audited."


def source_summary(systems, query_ids, ranks, grades):
    rows = []
    for group in systems:
        for threshold in (2, 3):
            hits, unique_sources, duplicates = [], [], []
            for qid in query_ids:
                ids = [cid for rank, cid in sorted(ranks[group, qid]) if rank <= 5]
                hits.append(int(any(grades[qid, cid] >= threshold for cid in ids)))
                docs = {cid.split("_CHK_")[0] for cid in ids}
                unique_sources.append(len(docs))
                duplicates.append(1 - len(docs)/len(ids) if ids else 0.)
            rows.append({"system": group, "threshold": f"grade>={threshold}", "queries": len(query_ids),
                         "Source-level Hit@5": round(statistics.mean(hits), 6),
                         "chunk Hit@5 (same qrel policy)": round(statistics.mean(hits), 6),
                         "mean unique sources@5": round(statistics.mean(unique_sources), 6),
                         "mean source duplicate ratio@5": round(statistics.mean(duplicates), 6),
                         "source_policy": SOURCE_POLICY, "interpretation": SOURCE_INTERPRETATION})
    return rows


def align_public_schema(public=PUBLIC, work=WORK):
    require(not read_json(work / "manual_skips.json"), "Export with scientific skips requires the same explicit query filter in the offline evaluator")
    gold = read_json(QA / "gold_v2/qa_gold.json")
    queries = []
    for q in gold["qa_questions"]:
        queries.append({"query_id": q["question_id"], "question": q["question"], "reference_answer": q["reference_answer"],
                        "retrievable": q["answerable"], "answerable": q["answerable"], "required_key_points": q["required_key_points"],
                        "difficulty": q["difficulty"], "support_mode": q["support_mode"], "fact_type": q["question_type"],
                        "question_type": q["question_type"], "fact_arity": q["fact_arity"], "gold_chunk_ids": q["gold_chunk_ids"]})
    payload = {"metadata": {"benchmark": "PFAS40 reused QA information needs", "corpus_docs": 60, "corpus_chunks": 1330,
                  "field_mapping": "retrievable derives from frozen answerable; fact_type copies original PFAS question_type without changing category labels",
                  "not_independent_retrieval_questions": True},
               "query_counts": {"total": 40, "retrievable": 35, "unanswerable": 5}, "queries": queries}
    write_json(public / "benchmark/retrieval_queries.json", payload)
    stage = work / "case1_schema_export"
    stage.mkdir(exist_ok=True)
    command = [sys.executable, str(BASE / "hyper-gragh/scripts/evaluate_shared_retrieval_qrels.py"),
               "--candidate-union", str(public / "benchmark/candidate_rankings.json"),
               "--qrels", str(public / "cfr/shared_qrels.json"), "--queries", str(public / "benchmark/retrieval_queries.json"),
               "--output-dir", str(stage), "--k", "5", "--thresholds", "1", "2", "3",
               "--scope-label", "case2_pfas_retained_five_case1_protocol"]
    for group in GROUPS: command += ["--system", group]
    completed = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
    (stage / "evaluator_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    canonical = read_json(public / "retrieval/shared_retrieval_summary_retained.json")
    case1 = read_json(stage / "shared_retrieval_summary.json")
    old = {(r["system"], r["threshold"]): r for r in canonical["rows"]}
    for row in case1["summary"]:
        reference = old[row["system"], int(row["relevance_threshold"].split(">=")[1])]
        for name in ("P@1", "Hit@5", "MRR", "gNDCG@5"):
            require(abs(row[name]-reference[name]) <= 0.00000051, "Case1 evaluator differs from original full-precision metric")
    for stem in ("summary", "per_query", "slice_summary", "ranked_topk"):
        shutil.copyfile(stage / ("shared_retrieval_"+stem+".csv"), public / ("retrieval/shared_retrieval_"+stem+"_retained.csv"))
    canonical.update(case1)
    canonical["metadata"].update(new_annotations_human_confirmed=False, annotation_model="deepseek-ai/DeepSeek-V4-Flash")
    write_json(public / "retrieval/shared_retrieval_summary_retained.json", canonical)
    candidates = read_json(public / "benchmark/candidate_rankings.json")["candidate_union"]
    ranks = defaultdict(list)
    top20 = []
    for row in candidates:
        for o in row["system_occurrences"]:
            ranks[o["system"], row["query_id"]].append((o["retrieval_rank"], row["chunk_id"]))
            top20.append({"system": o["system"], "query_id": row["query_id"], "rank": o["retrieval_rank"],
                          "chunk_id": row["chunk_id"], "qrel_grade": 0, "original_retrieval_rank": o["retrieval_rank"], "candidate_id": o["candidate_id"]})
    grades = {(r["query_id"], r["chunk_id"]): r["relevance_grade"] for r in read_json(public / "cfr/shared_qrels.json")["qrels"]}
    for row in top20: row["qrel_grade"] = grades[row["query_id"], row["chunk_id"]]
    write_csv(public / "retrieval/shared_retrieval_ranked_top20_retained.csv", sorted(top20, key=lambda r:(r["system"],r["query_id"],r["rank"])))
    write_csv(public / "retrieval/source_level_hit_summary_retained.csv", source_summary(list(GROUPS), [q["query_id"] for q in queries], ranks, grades))
    cfr = read_json(public / "cfr/composite_fact_recall_retained.json")
    summary = [{"system": r["system"], "facts": r["facts"], "supported_facts": r["recalled_facts"],
                "Composite Fact Recall@5": round(r["CFR@5"],6), "macro_query_CFR@5": round(r["macro_query_CFR@5"],6),
                "method": "machine_verified_atomic_gold_exact_chunk_binding"} for r in cfr["rows"]]
    write_csv(public / "cfr/composite_fact_recall_retained.csv", summary)
    cfr.update(version="pfas-composite-fact-recall-machine-verified-v1", created_at=utc(), status="completed_machine_verified_audit",
               summary=summary, accepted_gold="composite_fact_gold_machine_verified.json", new_annotations_human_confirmed=False,
               paper_database_scope="same retained five groups as latest case1; atomic facts are newly machine-reviewed")
    write_json(public / "cfr/composite_fact_recall_retained.json", cfr)
    qp = read_json(public / "qa/qa_final_protocol.json")
    qp.update(protocol_version="pfas-case1-legacy-supplementary-v1", evidence_budget_chars=1500,
              groups={"normalized_final": {"label":"Normalized Final (EFU repair disabled)", "cache":"hyper_final", "view":"hyper", "rerank":True,
                                           "retriever":"normalized_final_hybrid_rerank_v1"}},
              generator={"provider":"research_group_siliconflow", "base_url":"https://api.siliconflow.cn/v1", "model":qp["model"], "key_count":10},
              judge={"provider":"research_group_siliconflow", "base_url":"https://api.siliconflow.cn/v1", "model":qp["model"], "key_count":10},
              parallel_workers=10, per_key_max_actual_requests=1, gold_source_doc_filtering=False)
    write_json(public / "qa/qa_final_protocol.json", qp)
    write_json(public / "protocol/qa_final_protocol.json", qp)
    qa_summary = read_json(public / "qa/qa_final_summary_normalized_final.json")
    qa_summary["protocol"] = qp
    write_json(public / "qa/qa_final_summary_normalized_final.json", qa_summary)
    configs = {}
    for name in ("hyper_base", "hyper_chem_prompt", "hyper_norm", "hyper_final"):
        path = BASE / "case2_pfas_build" / name / "run_config.json"
        config = read_json(path)
        whitelist = ("domain", "prompt_profile", "index_profile", "enable_measurement_instances", "enable_efu_repair", "embedding_model", "embedding_dim", "llm_model", "reasoning_effort", "chunk_token_size", "chunk_overlap_token_size")
        configs[name] = {"source_sha256":file_hash(path), "settings":{k:config[k] for k in whitelist if k in config}}
    write_json(public / "protocol/accepted_cache_profiles.json", {"immutable":True, "configs":configs,
               "baseline_exception":"45 original relation-placeholder vertices were separately audited and retained; no EFU repair"})
    check = []
    reference = BASE / "Hyper-ChE/experiments/final_v1"
    for p in sorted(reference.rglob("*.csv")):
        rel = p.relative_to(reference)
        target = public / rel
        require(target.exists(), "Missing case1-shaped table: " + str(rel))
        with p.open(encoding="utf-8-sig",newline="") as f: expected = next(csv.reader(f))
        with target.open(encoding="utf-8-sig",newline="") as f: actual = next(csv.reader(f))
        require(actual == expected, "Case1 CSV header mismatch: " + str(rel))
        check.append({"path":rel.as_posix(), "identical_header":True})
    result = {"complete":True, "case1_csv_schemas_identical":True, "tables":check,
              "metrics_recomputed_by_actual_case1_evaluator":True, "source_policy":SOURCE_POLICY,
              "main_retrieval_and_cfr_values_unchanged":True,
              "earlier_broader_source_document_hit_export_superseded":True, "at":utc()}
    write_json(public / "protocol/table_schema_acceptance.json", result)
    dictionary = public / "data_dictionary.md"
    text = dictionary.read_text(encoding="utf-8")
    note = f"\n## Case1 table compatibility\n\nAll {len(check)} shared CSV filenames use exactly the case1 column schemas. Values are rounded to six decimals in the case1 CSVs; full-precision canonical rows remain in the JSONs. ranked_topk is Top5; an additional ranked_top20 export and candidate_rankings retain complete MRR ranks. Source-level Hit uses the actual retrieved chunk's grade and therefore equals chunk Hit at the same threshold; it is not inferred from another relevant chunk in the same paper. PFAS category labels are preserved: fact_type copies original question_type, retrievable copies corpus answerable, and the same case1 arity-bucket code is used.\n"
    if "## Case1 table compatibility" not in text: dictionary.write_text(text+note,encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(align_public_schema(),ensure_ascii=False))
