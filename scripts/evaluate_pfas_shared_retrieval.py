"""Shared PFAS40 pooled qrels and answer-independent top-5 evidence evaluation.

Uses frozen retrieval results; never generates answers or rebuilds embeddings.
New relevance judgments remain machine annotations, separate from the user's
confirmation of the previously delivered QA results.
"""
import argparse
import asyncio
import json
import math
import statistics
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, MODEL, ENDPOINT, read_json, write_json, file_hash, digest, utc
from scripts.audit_pfas_qa40_scores import source_span_catalog
from scripts.run_pfas_qa40 import GROUPS
from scripts.run_qa_formal_llm import write_csv

RULES = """Judge the supplied raw PFAS evidence against the question and frozen rubric.
The retrieval system and its QA answer/score are hidden. Use only the supplied
raw text as evidence; reference answers define the information need, not support.
For each rubric point use support=full only when ALL requested facts and their
target/material/condition/value/unit binding are established. Use partial when
a useful part is established, and none otherwise. Do not join incompatible
experiments or PFAS identities. Cross-study comparison is allowed only when
the question explicitly requests it, without claiming a controlled ranking.
Removal, parent degradation, defluorination and mineralization are distinct.
Adsorption/coagulation is not destruction. Chemical notation and equivalent units
may be interpreted in the reason; never alter raw quoted text or numerical scope.
Every partial/full point MUST choose one or more exact offered span IDs. A span
ID is a mechanical pointer, not a guarantee of support. For none use no span IDs.
Context relevance requires genuinely useful question-specific context and an
exact offered span; sharing the broad PFAS domain or bibliography is not enough.
For a negative question the rubric describes absence, which a single retrieved
packet cannot prove: all rubric points must be none. Separately flag an actual
direct answer that conflicts with its negative status, with exact supporting IDs.
List binding issues by point_id; a point with an unresolved binding issue cannot
be full. Do not infer missing facts from memory, graph hints or other papers.
Return one COMPLETE JSON object, all fields required:
{
 "point_checks":[{"point_id":0,"support":"full or partial or none","span_ids":[],"reason":"specific source-based explanation"}],
 "context_relevant":false,"context_span_ids":[],
 "negative_query_answer_found":false,"negative_answer_span_ids":[],
 "binding_issues":[{"point_id":0,"reason":"specific unresolved binding"}],
 "rationale":"specific overall explanation"
}
point_checks must contain EVERY supplied point_id exactly once in order.
Use [] for binding_issues if none. All span IDs must be copied exactly from the
catalog in THIS packet. Do not return literal quotations, IDs from elsewhere,
retrieval ranks as support or a quality score for a generated answer.
"""


def annotation_packet(question, ids, chunks):
    # Evidence composition is independent of retrieval order. Present identical
    # sets identically, so their machine call is shared rather than rejudged.
    ids = sorted(ids)
    raw = [{"rank": i, "chunk_id": cid, "content": chunks[cid]["content"]} for i, cid in enumerate(ids, 1)]
    return {"question_id": question["question_id"], "question": question["question"],
            "answerable": question["answerable"], "reference_answer_NOT_evidence": question["reference_answer"],
            "rubric": [{"point_id": i, "point": p} for i, p in enumerate(question["required_key_points"])],
            "RAW_SPAN_CATALOG": source_span_catalog({"raw_retrieved_chunks": raw})}


def validate_annotation(value, packet):
    if not isinstance(value, dict) or not packet["rubric"]:
        raise ValueError("An annotation object and a nonempty rubric are required")
    points = value.get("point_checks")
    if not isinstance(points, list) or any(not isinstance(p, dict) or type(p.get("point_id")) is not int for p in points):
        raise ValueError("Point checks must be an ordered complete list")
    if [p["point_id"] for p in points] != list(range(len(packet["rubric"]))):
        raise ValueError("Every rubric point must be checked in order")
    catalog = packet["RAW_SPAN_CATALOG"]
    def spans(ids, required):
        if not isinstance(ids, list) or any(not isinstance(x, str) or x not in catalog for x in ids) or len(set(ids)) != len(ids):
            raise ValueError("Unknown, duplicate or wrong-packet raw span ID")
        if required != bool(ids):
            raise ValueError("Positive support requires spans; absent support requires an empty list")
    for point in points:
        support = point.get("support")
        if support not in ("full", "partial", "none") or not isinstance(point.get("reason"), str) or not point["reason"].strip():
            raise ValueError("Each point needs support status and a specific reason")
        spans(point.get("span_ids"), support != "none")
        if not packet["answerable"] and support != "none":
            raise ValueError("A retrieved packet cannot prove a negative corpus-wide rubric")
    for flag, ids in (("context_relevant", "context_span_ids"), ("negative_query_answer_found", "negative_answer_span_ids")):
        if type(value.get(flag)) is not bool:
            raise ValueError("Annotation flags must be booleans")
        spans(value.get(ids), value[flag])
    if packet["answerable"] and value["negative_query_answer_found"]:
        raise ValueError("Negative-query conflict flag is only for negative questions")
    if value["negative_query_answer_found"] and not value["context_relevant"]:
        raise ValueError("A direct negative-query answer must also be context-relevant")
    if any(p["support"] != "none" for p in points) and not value["context_relevant"]:
        raise ValueError("Supported rubric content must also be context-relevant")
    issues = value.get("binding_issues")
    if not isinstance(issues, list):
        raise ValueError("binding_issues must be a list")
    for issue in issues:
        if not isinstance(issue, dict):
            raise ValueError("Each binding issue must be an object")
        pid = issue.get("point_id")
        if type(pid) is not int or not 0 <= pid < len(points) or not isinstance(issue.get("reason"), str) or not issue["reason"].strip() or points[pid]["support"] == "full":
            raise ValueError("An unresolved binding issue cannot coexist with full support for that point")
    if not isinstance(value.get("rationale"), str) or not value["rationale"].strip():
        raise ValueError("Overall rationale required")


def derive_grade(value, answerable):
    if not answerable:
        return int(value["context_relevant"])
    supports = [p["support"] for p in value["point_checks"]]
    if not supports:
        raise ValueError("An empty rubric cannot establish full support")
    if all(s == "full" for s in supports): return 3
    if "full" in supports: return 2
    return int("partial" in supports or value["context_relevant"])


def ranking_metrics(ids, grades, k=5):
    if type(k) is not int or k <= 0 or any(type(g) is not int or not 0 <= g <= 3 for g in grades.values()):
        raise ValueError("Positive integer k and integer relevance grades 0..3 required")
    if any(cid not in grades for cid in ids):
        raise ValueError("Unjudged candidates cannot be treated as irrelevant")
    ranked_ids = list(dict.fromkeys(ids))[:k]
    ranked = [grades[cid] for cid in ranked_ids]
    ideal = sorted(grades.values(), reverse=True)[:k]
    def dcg(values): return sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(values))
    denominator = dcg(ideal)
    relevant = {cid for cid, g in grades.items() if g >= 2}
    first = next((i + 1 for i, g in enumerate(ranked) if g >= 2), None)
    return {"P@1_grade2": float(bool(ranked) and ranked[0] >= 2), "P@5_grade2": sum(g >= 2 for g in ranked) / k,
            "Hit@5_grade2": float(any(g >= 2 for g in ranked)), "MRR@5_grade2": 1 / first if first else 0.,
            "pooled_recall@5_grade2": len(set(ranked_ids) & relevant) / len(relevant) if relevant else None,
            "gNDCG@5_shared_pool": dcg(ranked) / denominator if denominator else None,
            "shared_IDCG@5": denominator, "pooled_relevant_chunks_grade2": len(relevant)}


def prepare(root, qa):
    gold_file = qa / "gold_v2/qa_gold.json"
    gold = read_json(gold_file)
    reviewed = read_json(qa / "latest_reviewed_release.json")
    assert reviewed["human_review_confirmed"] and reviewed["gold_sha256"] == file_hash(gold_file)
    assert read_json(qa / "final_report/acceptance.json")["complete"]
    chunks = read_json(gold["source"]["chunks"])
    assert file_hash(gold["source"]["chunks"]) == gold["source"]["chunks_sha256"]
    pool = {}
    sets = {}
    rankings = {}
    source_hashes = {}
    for q in gold["qa_questions"]:
        assert q["required_key_points"] and type(q["answerable"]) is bool
        qid = q["question_id"]
        for cid in q["gold_chunk_ids"]:
            pool[(qid, cid)] = {"question_id": qid, "chunk_id": cid, "occurrences": [], "gold_source_member": True}
        for group in GROUPS:
            p = qa / "evaluation_v2/retrieval" / group / (qid + ".json")
            source_hashes[p.relative_to(qa).as_posix()] = file_hash(p)
            r = read_json(p)
            ids = [x.get("source_chunk_id") or x["id"] for x in r["evidence"]]
            assert len(ids) <= 5 and len(set(ids)) == len(ids) and all(cid in chunks for cid in ids)
            rankings[(group, qid)] = ids
            for rank, cid in enumerate(ids, 1):
                row = pool.setdefault((qid, cid), {"question_id": qid, "chunk_id": cid, "occurrences": [], "gold_source_member": False})
                row["occurrences"].append({"group": group, "rank": rank})
            sid = digest({"question_id": qid, "ordered_chunk_ids": ids})[:24]
            row = sets.setdefault(sid, {"question_id": qid, "chunk_ids": ids, "occurrences": []})
            row["occurrences"].append(group)
    pool_rows = sorted(pool.values(), key=lambda r: (r["question_id"], r["chunk_id"]))
    for r in pool_rows:
        r["chunk_sha256"] = digest(chunks[r["chunk_id"]]["content"])
    protocol = {"version": "pfas40-shared-pool-and-evidence-support-v1", "gold_sha256": file_hash(gold_file),
                "review_receipt_sha256": file_hash(reviewed["receipt"]), "source_chunks_sha256": gold["source"]["chunks_sha256"],
                "retrieval_hashes": source_hashes, "rules_sha256": digest(RULES), "groups": GROUPS,
                "k": 5, "pool": "union of all six frozen top5 lists and gold reference chunks; not exhaustive corpus qrels",
                "grades": {"3": "all rubric points fully supported by this single chunk", "2": "at least one rubric point fully supported", "1": "partial point or specific useful context", "0": "irrelevant/generic/bibliographic"},
                "positive_binary_threshold": 2, "set_proxy": "all frozen rubric points fully supported jointly at top5 with valid target/material/condition binding",
                "annotation_source_order": "lexical chunk ID, independent of retrieval ranking; identical source sets share the annotation call",
                "new_annotations_human_confirmed": False, "prior_qa_release_user_confirmed": True,
                "model": MODEL, "endpoint": ENDPOINT, "temperature": 0, "reasoning_effort": "low", "max_actual_requests": 10, "max_per_key": 1,
                "pool_pairs": len(pool_rows), "unique_ordered_evidence_sets": len(sets), "no_new_qa_or_embedding_calls": True}
    root.mkdir(parents=True, exist_ok=True)
    if (root / "protocol.json").exists():
        assert read_json(root / "protocol.json") == protocol, "Frozen retrieval protocol changed"
        assert read_json(root / "candidate_union.json") == {"candidate_union": pool_rows}, "Candidate pool changed"
        assert read_json(root / "evidence_sets.json") == sets, "Ordered evidence sets changed"
    else:
        write_json(root / "protocol.json", protocol)
        write_json(root / "candidate_union.json", {"candidate_union": pool_rows})
        write_json(root / "evidence_sets.json", sets)
    return protocol, gold, chunks, pool_rows, sets, rankings


def validate_checkpoint(row, packet, protocol):
    if row.get("signature") != digest({"packet": packet, "protocol": digest(protocol)}):
        raise ValueError("Annotation input or protocol signature changed")
    if row.get("question_id") != packet["question_id"]:
        raise ValueError("Annotation query identity changed")
    ids = list(dict.fromkeys(s["chunk_id"] for s in packet["RAW_SPAN_CATALOG"].values()))
    if row.get("chunk_ids") != ids:
        raise ValueError("Annotation source ordering changed")
    validate_annotation(row["annotation"], packet)
    selected = {sid for p in row["annotation"]["point_checks"] for sid in p["span_ids"]}
    selected |= set(row["annotation"]["context_span_ids"]) | set(row["annotation"]["negative_answer_span_ids"])
    if row.get("span_evidence") != {sid: packet["RAW_SPAN_CATALOG"][sid] for sid in selected}:
        raise ValueError("Saved source evidence differs from exact raw spans")


async def run(root, qa):
    protocol, gold, chunks, pool_rows, sets, rankings = prepare(root, qa)
    questions = {q["question_id"]: q for q in gold["qa_questions"]}
    client = QAClient(root)
    semaphore = asyncio.Semaphore(10)
    call_locks = {}
    lock = asyncio.Lock()
    state = {"stage": "shared_qrels_and_evidence_sets", "started_at": utc(), "pool_total": len(pool_rows), "pool_done": 0,
             "sets_total": len(sets), "sets_done": 0, "errors": [], "complete": False}
    write_json(root / "progress.json", state)
    async def one(kind, key, qid, ids):
        async with semaphore:
            ids = sorted(ids)
            data = annotation_packet(questions[qid], ids, chunks)
            signature = digest({"packet": data, "protocol": digest(protocol)})
            checkpoint = root / kind / (key + ".json")
            if checkpoint.exists():
                row = read_json(checkpoint)
                validate_checkpoint(row, data, protocol)
                return row
            prompt = RULES + "\nINPUT:\n" + json.dumps(data, ensure_ascii=False)
            async with call_locks.setdefault(signature, asyncio.Lock()):
                value = await client.json(prompt, role="judge", validator=lambda v: validate_annotation(v, data), label=kind + ":" + qid + ":" + key)
            row = {"signature": signature, "question_id": qid, "chunk_ids": ids, "annotation": value,
                   "span_evidence": {sid: data["RAW_SPAN_CATALOG"][sid] for sid in {sid for p in value["point_checks"] for sid in p["span_ids"]} | set(value["context_span_ids"]) | set(value["negative_answer_span_ids"])},
                   "completed_at": utc(), "human_confirmed": False}
            if kind == "pool": row["relevance_grade"] = derive_grade(value, questions[qid]["answerable"])
            write_json(checkpoint, row)
            return row
    async def tracked(kind, key, qid, ids):
        try:
            await one(kind, key, qid, ids)
            async with lock:
                state["pool_done" if kind == "pool" else "sets_done"] += 1
                from scripts.run_pfas_qa40 import request_stats
                state.update(updated_at=utc(), actual_requests=request_stats())
                write_json(root / "progress.json", state)
                print(json.dumps({"kind": kind, "done": state["pool_done"] if kind == "pool" else state["sets_done"], "question_id": qid}), flush=True)
        except Exception as exc:
            async with lock:
                state["errors"].append({"kind": kind, "key": key, "question_id": qid, "error_type": type(exc).__name__,
                                         "validation_error": str(exc)[:250] if isinstance(exc, ValueError) else None})
                write_json(root / "progress.json", state)
    try:
        tasks = [tracked("pool", r["question_id"] + "__" + r["chunk_id"], r["question_id"], [r["chunk_id"]]) for r in pool_rows]
        tasks += [tracked("sets", key, r["question_id"], r["chunk_ids"]) for key, r in sets.items()]
        await asyncio.gather(*tasks)
        state.update(finished_at=utc(), complete=not state["errors"] and state["pool_done"] == len(pool_rows) and state["sets_done"] == len(sets))
        state["stage"] = "annotation_completed" if state["complete"] else "annotation_incomplete"
        write_json(root / "progress.json", state)
    finally:
        await client.close()
    if state["complete"]:
        report(root, qa)
    return 0 if state["complete"] else 2


def report(root, qa):
    protocol, gold, chunks, pool_rows, sets, rankings = prepare(root, qa)
    questions = {q["question_id"]: q for q in gold["qa_questions"]}
    judgments = {}
    set_judgments = {}
    conflicts = set()
    for r in pool_rows:
        qid, cid = r["question_id"], r["chunk_id"]
        row = read_json(root / "pool" / (qid + "__" + cid + ".json"))
        validate_checkpoint(row, annotation_packet(questions[qid], [cid], chunks), protocol)
        assert row["relevance_grade"] == derive_grade(row["annotation"], questions[qid]["answerable"])
        judgments[(qid, cid)] = row
        if row["annotation"]["negative_query_answer_found"]: conflicts.add(qid)
    for sid, r in sets.items():
        row = read_json(root / "sets" / (sid + ".json"))
        validate_checkpoint(row, annotation_packet(questions[r["question_id"]], r["chunk_ids"], chunks), protocol)
        set_judgments[sid] = row
        if row["annotation"]["negative_query_answer_found"]: conflicts.add(r["question_id"])
    consistency = []
    for sid, r in sets.items():
        joint = set_judgments[sid]["annotation"]
        for pid, point in enumerate(joint["point_checks"]):
            supporting = [cid for cid in r["chunk_ids"] if judgments[(r["question_id"], cid)]["annotation"]["point_checks"][pid]["support"] == "full"]
            if supporting and point["support"] != "full":
                consistency.append({"question_id": r["question_id"], "set_id": sid, "point_id": pid,
                                    "single_chunk_full_support_ids": supporting, "joint_support": point["support"],
                                    "reason": "Single-chunk full support and joint incomplete support require source-based consistency review."})
    write_json(root / "cross_packet_consistency.json", {"complete": not consistency, "conflicts": consistency,
               "rule": "Any member that fully establishes a point must also establish that point in the joint evidence set; conflicting annotations require source-based review, not vote counting."})
    qrels = [{"query_id": qid, "chunk_id": cid, "relevance_grade": r["relevance_grade"], "human_confirmed": False} for (qid, cid), r in judgments.items()]
    write_json(root / "qrels.json", {"qrels": qrels, "status": "machine_annotated_shared_pool", "human_confirmed": False})
    write_json(root / "manual_skip_queries.json", [{"query_id": qid, "reason": "New exact-source annotation flags a possible answer contradicting a negative question; skip all groups pending human adjudication."} for qid in sorted(conflicts)])
    per_query = []
    for group in GROUPS:
        for qid, q in questions.items():
            if qid in conflicts: continue
            ids = rankings[(group, qid)]
            grades = {cid: row["relevance_grade"] for (query, cid), row in judgments.items() if query == qid}
            sid = digest({"question_id": qid, "ordered_chunk_ids": ids})[:24]
            v = set_judgments[sid]["annotation"]
            full = sum(p["support"] == "full" for p in v["point_checks"])
            partial = sum(p["support"] in ("partial", "full") for p in v["point_checks"])
            per_query.append({"group": group, "question_id": qid, "answerable": q["answerable"], "difficulty": q["difficulty"],
                              **ranking_metrics(ids, grades), "full_point_coverage@5": full / len(v["point_checks"]),
                              "partial_or_full_point_coverage@5": partial / len(v["point_checks"]),
                              "all_rubric_points_full@5": float(full == len(v["point_checks"]) and not v["binding_issues"]),
                              "binding_issue_points": len({x["point_id"] for x in v["binding_issues"]})})
    metric_names = ["P@1_grade2", "P@5_grade2", "Hit@5_grade2", "MRR@5_grade2", "pooled_recall@5_grade2", "gNDCG@5_shared_pool", "full_point_coverage@5", "partial_or_full_point_coverage@5", "all_rubric_points_full@5"]
    aggregates = []
    for group in GROUPS:
        rows = [r for r in per_query if r["group"] == group and r["answerable"]]
        out = {"group": group, "supported_queries": len(rows), "manual_skips_all_groups": len(conflicts)}
        for name in metric_names:
            vals = [r[name] for r in rows if r[name] is not None]
            out[name] = statistics.mean(vals) if vals else None
            out[name + "_denominator"] = len(vals)
        aggregates.append(out)
    assert all(file_hash(qa / rel) == h for rel, h in protocol["retrieval_hashes"].items())
    assert file_hash(qa / "gold_v2/qa_gold.json") == protocol["gold_sha256"]
    write_csv(root / "per_query.csv", per_query)
    write_csv(root / "summary.csv", aggregates)
    write_json(root / "summary.json", {"complete": not consistency, "annotation_complete": True, "pending_source_consistency_checks": len(consistency), "protocol": protocol, "groups": aggregates, "manual_skip_queries": sorted(conflicts),
               "pool_judgments": len(judgments), "ordered_set_judgments": len(set_judgments), "new_annotations_human_confirmed": False,
               "limitations": ["The pool includes six frozen top5 lists plus gold chunks; recall and IDCG are pooled, not exhaustive corpus relevance.",
                               "These queries are the human-confirmed QA40 questions, not an independent newly sampled retrieval benchmark.",
                               "New qrels/evidence labels are machine annotations and were not covered by the prior human QA review.",
                               "All-rubric-points-full is an evidence-composition proxy, not a claim of exhaustive chemical fact recovery."]})
    lines = ["# PFAS40 共享相关性与组合证据检索评测", "", "使用六组已冻结的top5结果与金标准来源块构建共享判定池；复用原40题。新增标注为机器判定，先前QA人工复审不覆盖这些新标注。", "",
             f"候选query/chunk对：{len(judgments)}；独立有序top5证据包：{len(set_judgments)}。待人工查询按用户指示跨全部组跳过：{len(conflicts)}。", "",
             f"跨单块/组合证据一致性待核查：{len(consistency)}；存在待核查时，下列指标仅为初轮标注结果，不能作为最终指标。", "",
             "仅对支持题汇总检索指标；负题单列检查潜在金标准冲突。池化Recall与IDCG不等于全库真召回/完整qrels；无正例/零IDCG记为NA并列出分母。组合证据指标为原冻结评分要点在top5原文中的完整支撑代理。", "",
             "|组别|支持题数|P@5 强支持|池化nDCG@5|完整要点覆盖|全部要点完整|", "|---|---:|---:|---:|---:|---:|"]
    for r in aggregates:
        def fmt(x): return "NA" if x is None else f"{x:.4f}"
        lines.append(f"|{r['group']}|{r['supported_queries']}|{fmt(r['P@5_grade2'])}|{fmt(r['gNDCG@5_shared_pool'])}|{fmt(r['full_point_coverage@5'])}|{fmt(r['all_rubric_points_full@5'])}|")
    lines += ["", "逐题与分母见 per_query.csv / summary.csv；每条原文片段和绑定判定见 pool/ 与 sets/。不因结果顺序修改题集、标签或排序。", ""]
    (root / "report.md").write_text("\n".join(lines), encoding="utf-8")
    write_json(root / "report_acceptance.json", {"complete": not consistency, "annotation_complete": True, "pending_source_consistency_checks": len(consistency), "gold_and_retrieval_hashes_unchanged": True,
               "all_annotation_span_ids_validated": True, "human_confirmed_new_annotations": False,
               "summary_sha256": file_hash(root / "summary.json"), "report_sha256": file_hash(root / "report.md"), "at": utc()})


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--qa-root", type=Path, default=Path(r"D:\Hyper-rag-case2-backups\qa40_workspace"))
    p.add_argument("--output", type=Path, default=Path(r"D:\Hyper-rag-case2-backups\qa40_workspace\shared_retrieval_v1"))
    p.add_argument("--stage", choices=["prepare", "run", "report"], default="run")
    a = p.parse_args()
    if a.stage == "prepare":
        protocol, *_ = prepare(a.output, a.qa_root)
        print(json.dumps({"prepared": True, "pairs": protocol["pool_pairs"], "sets": protocol["unique_ordered_evidence_sets"]}))
    elif a.stage == "report": report(a.output, a.qa_root)
    else: raise SystemExit(asyncio.run(run(a.output, a.qa_root)))


if __name__ == "__main__": main()
