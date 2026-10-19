"""Offline export of completed case1-aligned PFAS experiments, with readback."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import statistics
import zipfile
from collections import defaultdict
from pathlib import Path

from scripts.align_pfas_case1 import BASE, QA, WORK, PUBLIC, GROUPS, GOLD_HASH, protocol, require
from scripts.pfas_qa_common import file_hash, read_json, write_json, utc
from scripts.evaluate_shared_retrieval_qrels import metrics
from scripts import run_qa_formal_llm as formal


def export(work=WORK, public=PUBLIC):
    status = read_json(work / "progress.json")
    require(status["complete"] and status["stage"] == "ready_for_package", "Aligned experiment is not ready for export")
    require(read_json(work / "preservation_after.json")["unchanged"], "Protected evidence preservation failed")
    require(read_json(work / "paired_pool_acceptance.json")["passed"], "F0/F1 pool audit failed")
    gold = read_json(QA / "gold_v2/qa_gold.json")
    require(file_hash(QA / "gold_v2/qa_gold.json") == GOLD_HASH, "Gold hash changed")
    queries = gold["qa_questions"]
    byq = {q["question_id"]: q for q in queries}
    candidates = read_json(work / "candidate_rankings.json")
    qrels = read_json(work / "shared_qrels.json")
    pool = candidates["candidate_union"]
    grades = {(r["query_id"], r["chunk_id"]): r["relevance_grade"] for r in qrels["qrels"]}
    require(set(grades) == {(r["query_id"], r["chunk_id"]) for r in pool}, "Qrels must cover the identical shared pool")
    ranks = defaultdict(list)
    for row in pool:
        for o in row["system_occurrences"]:
            ranks[o["system"], row["query_id"]].append((o["retrieval_rank"], row["chunk_id"]))
    skips = read_json(work / "manual_skips.json")
    skipped = {r["query_id"] for r in skips}
    retained = [q for q in queries if q["question_id"] not in skipped]
    ideals = {q["question_id"]: sorted([g for (qid, _), g in grades.items() if qid == q["question_id"]], reverse=True) for q in queries}
    per, ranked_rows, source_rows = [], [], []
    for group in GROUPS:
        for q in retained:
            qid = q["question_id"]
            ordered = sorted(ranks[group, qid])
            require([r for r, _ in ordered] == list(range(1, len(ordered)+1)), "Duplicate or gapped ranks")
            ids = [cid for _, cid in ordered]
            require(len(ids) == len(set(ids)) and len(ids) <= 20, "Invalid frozen candidate list")
            gs = [grades[qid, cid] for cid in ids]
            for threshold in (1, 2, 3):
                row = {"system": group, "query_id": qid, "threshold": threshold,
                       **metrics(gs, ideals[qid], threshold, 5)}
                for field in ("answerable", "difficulty", "question_type", "support_mode", "fact_arity"):
                    row[field] = q.get(field)
                per.append(row)
            for rank, cid in ordered:
                ranked_rows.append({"system": group, "query_id": qid, "retrieval_rank": rank, "chunk_id": cid,
                                    "relevance_grade": grades[qid, cid], "source_doc_id": cid.split("_CHK_")[0]})
            relevant_docs = {cid.split("_CHK_")[0] for (qq, cid), g in grades.items() if qq == qid and g >= 2}
            source_rows.append({"system": group, "query_id": qid,
                                "derived_source_hit_at5": int(bool({cid.split("_CHK_")[0] for cid in ids[:5]} & relevant_docs)),
                                "independent_source_gold": False})
    summary = []
    for group in GROUPS:
        for threshold in (1, 2, 3):
            rs = [r for r in per if r["system"] == group and r["threshold"] == threshold]
            summary.append({"system": group, "threshold": threshold, "queries": len(rs),
                            "zero_idcg_queries": sum(r["IDCG@5"] == 0 for r in rs),
                            **{k: statistics.mean(r[k] for r in rs) for k in ("P@1", "Hit@5", "MRR", "gNDCG@5")}})
    slices = []
    for field in ("answerable", "difficulty", "question_type", "support_mode", "fact_arity"):
        for value in sorted({str(q.get(field)) for q in retained}):
            for group in GROUPS:
                rs = [r for r in per if r["system"] == group and r["threshold"] == 2 and str(r[field]) == value]
                if rs:
                    slices.append({"field": field, "value": value, "system": group, "queries": len(rs),
                                   **{k: statistics.mean(r[k] for r in rs) for k in ("P@1", "Hit@5", "MRR", "gNDCG@5")}})
    facts = read_json(work / "composite_fact_gold_machine_verified.json")
    fact_rows, cfr = [], []
    for group in GROUPS:
        for q in facts["queries"]:
            if q["query_id"] in skipped: continue
            top = {cid for rank, cid in ranks[group, q["query_id"]] if rank <= 5}
            for f in q["atomic_facts"]:
                fact_rows.append({"system": group, "query_id": q["query_id"], "fact_id": f["fact_id"],
                                  "recalled": int(bool(top & set(f["supporting_chunk_ids"])))})
        rs = [r for r in fact_rows if r["system"] == group]
        by_query = defaultdict(list)
        for r in rs: by_query[r["query_id"]].append(r["recalled"])
        cfr.append({"system": group, "facts": len(rs), "recalled_facts": sum(r["recalled"] for r in rs),
                    "CFR@5": statistics.mean(r["recalled"] for r in rs),
                    "macro_query_CFR@5": statistics.mean(statistics.mean(v) for v in by_query.values()),
                    "fact_queries": len(by_query)})
    qa_records = [read_json(work / "qa/records" / (q["question_id"] + ".json")) for q in queries]
    require(len(qa_records) == 40, "Need forty valid supplementary F1 records")
    for folder in ("benchmark", "retrieval", "cfr", "qa", "protocol", "reports", "supplementary"):
        (public / folder).mkdir(parents=True, exist_ok=True)
    write_json(public / "benchmark/retrieval_queries.json", {"version": "pfas40-reused-information-needs", "queries": [
        {**{k: q.get(k) for k in ("question", "reference_answer", "answerable", "required_key_points", "question_type", "difficulty", "support_mode", "fact_arity", "gold_chunk_ids")},
         "query_id": q["question_id"]} for q in queries]})
    write_json(public / "benchmark/candidate_rankings.json", candidates)
    write_json(public / "retrieval/shared_retrieval_summary_retained.json", {"systems": list(GROUPS), "rows": summary,
               "protocol": {"thresholds": [1,2,3], "headline_threshold": 2, "k": 5, "mrr_depth": 20, "zero_idcg": 0},
               "included_queries": len(retained), "manual_skips": skips})
    formal.write_csv(public / "retrieval/shared_retrieval_summary_retained.csv", summary)
    formal.write_csv(public / "retrieval/shared_retrieval_per_query_retained.csv", per)
    formal.write_csv(public / "retrieval/shared_retrieval_slice_summary_retained.csv", slices)
    formal.write_csv(public / "retrieval/shared_retrieval_ranked_topk_retained.csv", ranked_rows)
    formal.write_csv(public / "retrieval/source_level_hit_summary_retained.csv", source_rows)
    write_json(public / "cfr/shared_qrels.json", qrels)
    write_json(public / "cfr/shared_qrels_final_audit.json", {"complete": True, "qrel_pairs": len(grades), "human_confirmed": False,
               "method": "source-span validated LLM annotations under frozen case1 grade rubric; no system/rank input",
               "new_annotations_covered_by_prior_user_review": False, "manual_skips": skips})
    write_json(public / "cfr/composite_fact_gold_machine_verified.json", facts)
    write_json(public / "cfr/rejected_facts.json", read_json(work / "rejected_facts.json"))
    write_json(public / "cfr/composite_fact_recall_retained.json", {"rows": cfr, "definition": "exact supporting_chunk_ids intersection with top5"})
    formal.write_csv(public / "cfr/composite_fact_recall_retained.csv", cfr)
    formal.write_csv(public / "cfr/fact_recall_per_query_retained.csv", fact_rows)
    shutil.copyfile(QA / "gold_v2/qa_gold.json", public / "qa/qa_questions.json")
    shutil.copyfile(QA / "human_reviewed_release_20261015/human_review.json", public / "qa/original_gold_user_review_receipt.json")
    with (public / "qa/qa_final_records.jsonl").open("w", encoding="utf-8") as f:
        for r in qa_records: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    qaproto = {"group": "normalized_final", "top_k": 5, "evidence_format": "legacy", "evidence_budget_chars_option": 1500,
               "actual_budget_unit": "legacy token_count function", "model": protocol()["llm"], "endpoint": protocol()["endpoint"],
               "temperature": 0, "reasoning_effort": "low", "prior_case1_model": "kimi-k2.6 / DashScope / temperature1 / top_p.95",
               "cross_case_qa_is_controlled": False, "new_result_human_confirmed": False}
    write_json(public / "qa/qa_final_protocol.json", qaproto)
    write_json(public / "protocol/qa_final_protocol.json", qaproto)
    write_json(public / "qa/qa_final_summary_normalized_final.json", {"groups": formal.aggregate_summary(qa_records, {"normalized_final": GROUPS["normalized_final"]}), "protocol": qaproto})
    for field in ("answerable", "difficulty", "fact_arity", "question_type", "support_mode"):
        formal.write_csv(public / ("qa/qa_final_by_" + field + ".csv"), formal.aggregate_by_field(qa_records, {"normalized_final": GROUPS["normalized_final"]}, field))
    write_json(public / "protocol/case2_alignment_protocol.json", protocol())
    shutil.copyfile(work / "paired_pool_acceptance.json", public / "protocol/paired_pool_acceptance.json")
    shutil.copyfile(work / "preservation_after.json", public / "protocol/preservation_acceptance.json")
    write_json(public / "protocol/case2_experiment_state.json", {"complete": True, "stages": status["counts"], "runtime_status": status,
               "supplementary_original_results": str(QA), "new_annotations_human_confirmed": False})
    write_json(public / "reports/manual_skips.json", skips)
    paired = []
    pp = {(r["system"], r["query_id"]): r for r in per if r["threshold"] == 2}
    for group in GROUPS:
        if group == "normalized_final": continue
        for metric in ("P@1", "Hit@5", "MRR", "gNDCG@5"):
            differences = [pp["normalized_final", q["question_id"]][metric] - pp[group, q["question_id"]][metric] for q in retained]
            paired.append({"reference": "normalized_final", "comparator": group, "metric": metric, "paired_queries": len(differences),
                           "mean_delta": statistics.mean(differences), "wins": sum(d > 1e-12 for d in differences),
                           "ties": sum(abs(d) <= 1e-12 for d in differences), "losses": sum(d < -1e-12 for d in differences)})
    formal.write_csv(public / "retrieval/paired_comparisons.csv", paired)
    headline = [r for r in summary if r["threshold"] == 2]
    table = "\n".join("| {system} | {P@1:.4f} | {Hit@5:.4f} | {MRR:.4f} | {gNDCG@5:.4f} |".format(**r) for r in headline)
    facttable = "\n".join(f"| {r['system']} | {r['CFR@5']:.4f} | {r['macro_query_CFR@5']:.4f} |" for r in cfr)
    report = f"""# Case2 PFAS: results aligned with the retained Case1 protocol

Five retained systems: B0/B1/B2/F0/F1. B0/B2 call actual upstream hyper_query;
B1 uses structured graph retrieval. F0/F1 use the identical final cache and
RRF top50 candidate pool, differing only in deterministic rerank. EFU is false.
See `protocol/alignment_matrix.md` for the audited cross-case differences.

## Hyper_ChE contribution and evaluation purpose

Chemical facts jointly bind materials, targets, conditions, values, units and
outcomes. Hyperedges directly represent these multiway roles. Hyper_ChE adapts
that representation through chemical semantic constraints, normalization,
source-local measurement/condition instances, canonical/surface representations
and hybrid evidence retrieval and candidate organization.

F1 evaluates this complete domain-adapted configuration. F0 already contains its
core domain adaptation and differs only in reranking; similar F0/F1 scores do
not test or refute domain adaptation. B2 is not the complete Hyper_ChE system.
These system comparisons do not isolate each adaptation module or pure structure.
See `实验结果汇报_两案例与方法定位.md` for two-case results and limitations.

## Shared retrieval, grade >=2

| System | P@1 | Hit@5 | MRR (top20) | shared gNDCG@5 |
|---|---:|---:|---:|---:|
{table}

All {len(retained)} common eligible queries are included; zero IDCG contributes 0.
The shared pool has {len(grades)} pairs and retains historical seed pairs even
when no retained system ranks them. Labels follow the case1 grade rubric and
were obtained without system/rank input. Sensitivity at thresholds1/3, slices,
per-query values and paired F1 differences are exported beside the main table.

## Exact fact recall

| System | micro CFR@5 | macro query CFR@5 |
|---|---:|---:|
{facttable}

The denominator is the newly source-verified atomic fact inventory, not a forced
copy of case1's 150 facts. Facts rejected by the independent source-audit prompt
are retained in rejected_facts.json and excluded identically for every system.
This exact-chunk proxy can undercount alternate valid evidence and does not
establish that a generator read or combined the facts.

## Supplementary QA and limitations

Only F1 is shown in the main supplementary QA package, as in the latest case1
release. It uses the same top5/legacy formatter and option value1500; the actual
case1 code counts tokens despite the argument's `chars` name. The authorized
DeepSeek/SiliconFlow configuration remains in use; case1 used Kimi/DashScope with
different sampling. Cross-case QA differences therefore are not controlled.

The original PFAS40 and earlier six-system QA were accepted by the user. New
retrieval labels, atomic facts and supplementary QA results are machine work;
the earlier human confirmation does not cover them. LLM generation and review
use the same model in separate prompts, not independent human annotation.
The 40 information needs reuse QA questions rather than an independent58-query
retrieval set. Source-supported references cover25 documents; negative-question
absence checks cover all60. Shared pooled qrels are not exhaustive corpus gold.
Source-level hits are derived diagnostics, not independent document qrels.
No ranking has been optimized to favor the final system. Earlier six-group
results remain separate and were not overwritten or renamed as this experiment.

Original caches and prior evidence files were SHA256 checked before/after.
Manual scientific skips: {len(skips)} queries, excluded across all groups.
"""
    (public / "reports/paper_analysis_report.md").write_text(report, encoding="utf-8")
    (public / "reports/B1_B2_retrieval_protocol_diagnosis.md").write_text("# B1/B2 attribution\n\nB1 uses structured_graph_hybrid_v1 in graph view. B2 uses actual upstream hyper_query with PFAS keyword prompt and 10+10 branch quotas. These are system comparisons with different adapters, not a single-variable arity or prompt ablation. B2 is not the complete domain-adapted Hyper_ChE method. F0/F1 both contain the core domain adaptation, share the same final cache and RRF top50 pool, and isolate the rerank switch. Similar F0/F1 scores concern rerank increment, not the value of domain adaptation.\n", encoding="utf-8")
    (public / "data_dictionary.md").write_text("""# Data dictionary

candidate_rankings.candidate_union: every query/chunk pair in the shared pool;
system_occurrences gives retained system and one-based frozen retrieval_rank.
Empty occurrences are valid historical seed pairs and stay in the shared IDCG.
shared_qrels.qrels: exact matching pair set, integer relevance_grade0..3; exact
support spans carry source chunk ID, offsets and verbatim raw text. Model labels
are not human_confirmed. manual_skips are excluded across all retained systems.
summary_retained: all common eligible queries, grade thresholds1/2/3; headline2.
MRR uses the returned top20, while Hit/gNDCG use5. Zero IDCG ->0 included.
atomic_facts: newly generated facts, selected exact raw support and separate
source review. supporting_chunk_ids use OR semantics for exact CFR@5 hits.
fact recall is not a full semantic combination score or exhaustive relevance.
QA records: F1 answers and model judgments under the new legacy-budget protocol.
Original gold contains historical human_confirmed=false; the separate original
user-review receipt is the later acceptance, without modifying historical bytes.
Local paths are provenance, not portable setup instructions. Full corpus/vectors
are intentionally excluded from this compact package.
""", encoding="utf-8")
    (public / "README.md").write_text(f"""# Case2 PFAS experiment evidence

This folder mirrors `experiments/final_v1` for the five systems retained in the
2026-10-08 arXiv draft: B0, B1, B2, F0, F1. The alignment matrix and source SHA256
ledger are in `protocol/`. New runs, not renamed historical outputs, supply the
aligned adapters and controlled F0/F1 rerank comparison.

## Method and result interpretation

Hyper_ChE uses hyperedges for multiway chemical facts, with domain semantic
constraints, normalization, source-bound measurements/conditions, dual
representations and hybrid retrieval. F1 evaluates the complete method; F0
already contains the core domain adaptation and disables only reranking.
See [the two-case report](reports/实验结果汇报_两案例与方法定位.md) for the
method contribution, measured results and limits of attribution.

## Package contents

- `benchmark/`:40 frozen PFAS information needs and compact top20 IDs/ranks.
- `retrieval/`: shared qrels metrics, per-query/slice/paired/source diagnostics.
- `cfr/`: {len(grades)} shared judgments, exact-source atomic facts and CFR@5.
- `qa/`: F1 supplementary40 QA records, protocol and slices.
- `protocol/`: audited alignment, original source hashes and run acceptance.
- `reports/`: results and limitations, including manual skips.
- `supplementary/`: pointers to unchanged earlier six-group results.

Run `python reproduce_metrics.py` inside this folder to recompute retrieval and
CFR offline and check all exported hashes. No API or vector cache is required.
The corpus has60 documents and1330 chunks. The query count and annotation/model
differences from case1 are explicitly disclosed, not made equal by relabelling.
New annotations remain machine-verified; prior human acceptance covers the
original PFAS40/240QA release only. See reports/paper_analysis_report.md.
""", encoding="utf-8")
    # Keep the current approved method interpretation in future compact exports.
    # This is reporting only; frozen evaluation data and labels are not changed.
    from scripts.pfas_case1_reporting import export_method_reporting
    export_method_reporting(public)
    repro_source = Path(__file__).with_name("reproduce_pfas_case1_package.py")
    shutil.copyfile(repro_source, public / "reproduce_metrics.py")
    from scripts.finalize_pfas_case1_schema import align_public_schema
    align_public_schema(public, work)
    artifacts = [{"path": p.relative_to(public).as_posix(), "sha256": file_hash(p), "bytes": p.stat().st_size}
                 for p in sorted(public.rglob("*")) if p.is_file() and p.relative_to(public).as_posix() not in ("publication_manifest.json", "acceptance.json")]
    manifest = {"snapshot": "case2-pfas-case1-aligned-v1", "complete": True, "created_at": utc(), "retained_systems": list(GROUPS),
                "dimensions": {"documents": 60, "chunks": 1330, "queries": 40, "eligible_queries": len(retained), "qrels": len(grades),
                               "facts": sum(len(q["atomic_facts"]) for q in facts["queries"]), "qa_records": 40},
                "artifacts": artifacts, "work": str(work), "new_annotations_human_confirmed": False}
    write_json(public / "publication_manifest.json", manifest)
    from scripts.reproduce_pfas_case1_package import reproduce
    result = reproduce(public)
    write_json(public / "acceptance.json", {**result, "protected_evidence_unchanged": True, "at": utc()})
    archive = work / "case2_pfas_v1_verified_results.zip"
    paths = [p for p in sorted(public.rglob("*")) if p.is_file()]
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for p in paths: z.write(p, p.relative_to(public).as_posix())
    with zipfile.ZipFile(archive) as z:
        require(len(z.infolist()) == len(paths), "Archive entry count mismatch")
        require(all(hashlib.sha256(z.read(p.relative_to(public).as_posix())).hexdigest() == file_hash(p) for p in paths), "Archive SHA readback mismatch")
    pointer = {"folder": str(public), "archive": str(archive), "sha256": file_hash(archive), "files": len(paths),
               "bytes": archive.stat().st_size, "verified": True, "created_at": utc()}
    write_json(work / "release_pointer.json", pointer)
    print(json.dumps(pointer), flush=True)
    return pointer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, default=WORK)
    args = parser.parse_args()
    export(args.work)
