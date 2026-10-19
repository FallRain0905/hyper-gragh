"""Independently verify shared PFAS retrieval labels, metrics and final archive."""
import collections
import hashlib
import itertools
import json
import math
import statistics
import zipfile
from pathlib import Path

import numpy as np

from scripts.pfas_qa_common import read_json, write_json, file_hash, digest, utc
from scripts.evaluate_pfas_shared_retrieval import prepare, annotation_packet, validate_checkpoint, derive_grade
from scripts.adjudicate_pfas_shared_retrieval import validate_review, patched_annotation, remap_spans, source_conflicts
from scripts.run_pfas_qa40 import GROUPS
from scripts.run_qa_formal_llm import write_csv

QA = Path(r"D:\Hyper-rag-case2-backups\qa40_workspace")
ROOT = QA / "shared_retrieval_v1"
FINAL = ROOT / "metric_scope_v1/effective_labels"
OUT = ROOT / "final_report"


def independent_rank_metrics(ids, grades, chunks):
    ranked = list(dict.fromkeys(ids))[:5]
    relevant = {cid for cid in grades if grades[cid] >= 2}
    discounted = lambda gs: math.fsum((2. ** g - 1.) / math.log2(i + 2.) for i, g in enumerate(gs))
    ideal = discounted(sorted(grades.values(), reverse=True)[:5])
    hits = [i + 1 for i, cid in enumerate(ranked) if cid in relevant]
    docs = {chunks[cid]["source_doc_id"] for cid in relevant}
    retrieved_docs = {chunks[cid]["source_doc_id"] for cid in ranked}
    return {"P@1_grade2": float(bool(ranked) and ranked[0] in relevant), "P@5_grade2": len(hits) / 5.,
            "Hit@5_grade2": float(bool(hits)), "MRR@5_grade2": 1. / hits[0] if hits else 0.,
            "pooled_recall@5_grade2": len(relevant.intersection(ranked)) / len(relevant) if relevant else None,
            "gNDCG@5_shared_pool": discounted([grades[cid] for cid in ranked]) / ideal if ideal else None,
            "shared_IDCG@5": ideal, "pooled_relevant_chunks_grade2": len(relevant),
            "source_doc_Hit@5": float(bool(docs & retrieved_docs)),
            "pooled_source_doc_recall@5": len(docs & retrieved_docs) / len(docs) if docs else None}


def load_rows(folder, protocol, gold, chunks, pool, sets):
    qs = {q["question_id"]: q for q in gold["qa_questions"]}
    rows = {}
    for r in pool:
        key = "pool/" + r["question_id"] + "__" + r["chunk_id"]
        rows[key] = read_json(folder / (key + ".json"))
    for sid in sets: rows["sets/" + sid] = read_json(folder / "sets" / (sid + ".json"))
    for key, row in rows.items():
        q = qs[row["question_id"]]
        validate_checkpoint(row, annotation_packet(q, row["chunk_ids"], chunks), protocol)
        assert row["human_confirmed"] is False
        if key.startswith("pool/"): assert row["relevance_grade"] == derive_grade(row["annotation"], q["answerable"])
    return rows


def verify_layer(base_folder, output, derived_folder, base_rows, derived_rows, questions, chunks):
    changes = {}
    p = read_json(output / "protocol.json")
    hashes = p.get("initial_label_hashes") or p["base_label_hashes"]
    assert all(file_hash(base_folder / (key + ".json")) == h for key, h in hashes.items())
    for path in (output / "reviews").glob("*.json"):
        r = read_json(path); packet = r["input"]
        assert digest(packet) == (p.get("inputs_sha256") or p["input_hashes"])[path.stem]
        assert r["signature"] == digest({"input": packet, "protocol": p})
        assert packet["question"] == questions[path.stem]["question"]
        assert [x["point"] for x in packet["rubric"]] == questions[path.stem]["required_key_points"]
        for span in packet["RAW_SPAN_CATALOG"].values():
            raw = chunks[span["chunk_id"]]["content"]
            assert raw[span["start"]:span["end"]] == span["exact_raw_text"]
        validate_review(r["result"], packet, base_rows)
        if "target_recovery" in r:
            retained = r["target_recovery"]["retained_subrecord_hashes"]
            assert all(digest(d) == retained[d["target_id"]] for d in r["result"]["target_decisions"] if d["target_id"] in retained)
        for target, decision in zip(packet["targets"], r["result"]["target_decisions"]):
            a = patched_annotation(target, decision)
            for key in target["aliases"]:
                local = annotation_packet(questions[path.stem], base_rows[key]["chunk_ids"], chunks)
                expected, _ = remap_spans(a, packet["RAW_SPAN_CATALOG"], local["RAW_SPAN_CATALOG"])
                assert derived_rows[key]["annotation"] == expected
                changes[key] = True
    for key in base_rows:
        if key not in changes:
            assert file_hash(base_folder / (key + ".json")) == file_hash(derived_folder / (key + ".json"))
    return len(changes)


def aggregate(rows, names):
    out = {"questions": len(rows)}
    for name in names:
        xs = [r[name] for r in rows if r[name] is not None]
        out[name] = statistics.mean(xs) if xs else None
        out[name + "_denominator"] = len(xs)
    return out


def main():
    OUT.mkdir(exist_ok=True)
    assert read_json(ROOT / "technical_retry_v1/progress.json")["complete"]
    assert read_json(ROOT / "source_consistency_v1/progress.json")["complete"]
    assert read_json(ROOT / "metric_scope_v1/target_recovery_v1/progress.json")["complete"]
    protocol, gold, chunks, pool, sets, rankings = prepare(FINAL, QA)
    questions = {q["question_id"]: q for q in gold["qa_questions"]}
    assert len(questions) == 40 and sum(q["answerable"] for q in questions.values()) == 35
    assert len(pool) == 521 and len(sets) == 227
    initial = load_rows(ROOT, protocol, gold, chunks, pool, sets)
    middle_folder = ROOT / "source_consistency_v1/effective_labels"
    middle = load_rows(middle_folder, protocol, gold, chunks, pool, sets)
    final = load_rows(FINAL, protocol, gold, chunks, pool, sets)
    source_targets = verify_layer(ROOT, ROOT / "source_consistency_v1", middle_folder, initial, middle, questions, chunks)
    scope_targets = verify_layer(middle_folder, ROOT / "metric_scope_v1", FINAL, middle, final, questions, chunks)
    manual = {}
    for path in (FINAL / "manual_skip_queries.json", ROOT / "source_consistency_v1/manual_skip_queries.json", ROOT / "metric_scope_v1/manual_skip_queries.json"):
        for r in read_json(path): manual[r["query_id"]] = r["reason"]
    assert not [x for x in source_conflicts(final) if x["question_id"] not in manual]
    grades = {qid: {} for qid in questions}
    for key, row in final.items():
        if key.startswith("pool/"): grades[row["question_id"]][row["chunk_ids"][0]] = row["relevance_grade"]
    rows = []
    for group in GROUPS:
        for qid, q in questions.items():
            if qid in manual: continue
            ids = rankings[(group, qid)]
            sid = digest({"question_id": qid, "ordered_chunk_ids": ids})[:24]
            v = final["sets/" + sid]["annotation"]
            n = len(v["point_checks"])
            full = sum(p["support"] == "full" for p in v["point_checks"])
            partial = sum(p["support"] != "none" for p in v["point_checks"])
            rows.append({"group": group, "question_id": qid, "answerable": q["answerable"], "difficulty": q["difficulty"],
                         "support_mode": q.get("support_mode", "unspecified"),
                         **independent_rank_metrics(ids, grades[qid], chunks), "full_point_coverage@5": full / n,
                         "partial_or_full_point_coverage@5": partial / n,
                         "all_rubric_points_full@5": float(full == n and not v["binding_issues"])})
    names = ["P@1_grade2", "P@5_grade2", "Hit@5_grade2", "MRR@5_grade2", "pooled_recall@5_grade2", "gNDCG@5_shared_pool",
             "full_point_coverage@5", "partial_or_full_point_coverage@5", "all_rubric_points_full@5", "source_doc_Hit@5", "pooled_source_doc_recall@5"]
    supported = [r for r in rows if r["answerable"]]
    saved = {r["group"]: r for r in read_json(FINAL / "summary.json")["groups"]}
    summaries = []
    for group in GROUPS:
        rs = [r for r in supported if r["group"] == group]
        out = {"group": group, "label": GROUPS[group]["label"], **aggregate(rs, names)}
        if not manual:
            for name in names[:9]:
                assert out[name + "_denominator"] == saved[group][name + "_denominator"]
                assert (out[name] is saved[group][name] is None) or abs(out[name] - saved[group][name]) < 1e-10
        summaries.append(out)
    for qid in questions:
        ideals = {r["shared_IDCG@5"] for r in rows if r["question_id"] == qid}
        assert len(ideals) <= 1, "All groups must share each query's IDCG"
    strata = []
    for group in GROUPS:
        for field in ("difficulty", "support_mode"):
            for value in sorted({r[field] for r in supported}):
                rs = [r for r in supported if r["group"] == group and r[field] == value]
                strata.append({"group": group, "stratum": field, "value": value, **aggregate(rs, names)})
    pairwise = []
    for a, b in itertools.combinations(GROUPS, 2):
        ar = {r["question_id"]: r for r in supported if r["group"] == a}
        br = {r["question_id"]: r for r in supported if r["group"] == b}
        assert set(ar) == set(br)
        for metric in names:
            diffs = [ar[q][metric] - br[q][metric] for q in ar if ar[q][metric] is not None and br[q][metric] is not None]
            pairwise.append({"group_a": a, "group_b": b, "metric": metric, "paired_questions": len(diffs),
                "a_wins": sum(d > 1e-12 for d in diffs), "ties": sum(abs(d) <= 1e-12 for d in diffs), "b_wins": sum(d < -1e-12 for d in diffs),
                "mean_a_minus_b": statistics.mean(diffs) if diffs else None})
    manifest = Path(gold["source"]["manifest"])
    assert file_hash(manifest) == gold["source"]["manifest_sha256"]
    docs = [json.loads(x) for x in manifest.read_text(encoding="utf-8-sig").splitlines() if x]
    assert len(docs) == 60
    for d in docs: assert file_hash(manifest.parent / "documents" / d["corpus_filename"]) == d["source_sha256"]
    quotes = 0
    for q in questions.values():
        vector = read_json(QA / "evaluation_v2/query_vectors" / (q["question_id"] + ".json"))
        assert vector["signature"] == digest({"query": q["question"], "model": "Qwen/Qwen3-Embedding-4B", "dim": 2560})
        arr = np.asarray(vector["vector"]); assert arr.shape == (2560,) and np.isfinite(arr).all() and np.any(arr)
        for e in q.get("evidence", []):
            raw = chunks[e["chunk_id"]]["content"]; assert raw[e["start_char"]:e["end_char"]] == e["quote"]
            assert hashlib.sha256(e["quote"].encode()).hexdigest() == e["quote_sha256"]
            quotes += 1
    assert quotes == 100
    protected = read_json(ROOT / "preservation_before.json")["hashes"]
    for p, h in protected.items(): assert file_hash(p) == h, "A protected QA/build/published file changed: " + p
    audits = []
    for p in ROOT.rglob("request_audit.jsonl"):
        audits += [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x]
    assert all(a["role"] == "judge" and a["model"] == "deepseek-ai/DeepSeek-V4-Flash" for a in audits)
    network = max(a["requests"]["network_peak"] for a in audits); per_key = max(a["requests"]["key_peak"] for a in audits)
    assert network <= 10 and per_key <= 1
    changes = [{"target": key, "question_id": old["question_id"], "point_id": i, "initial": p["support"], "final": final[key]["annotation"]["point_checks"][i]["support"]}
               for key, old in initial.items() for i, p in enumerate(old["annotation"]["point_checks"])
               if p["support"] != final[key]["annotation"]["point_checks"][i]["support"]]
    metrics = {"complete": True, "at": utc(), "groups": summaries, "strata": strata, "pairwise": pairwise,
               "pool_pairs": 521, "ordered_top5_lists": 227, "unique_source_sets": 205, "supported_queries": len(supported) // 6,
               "negative_queries": 5, "manual_skips": manual, "new_annotations_human_confirmed": False,
               "source_consistency_targets": source_targets, "scope_review_targets": scope_targets, "point_status_changes": changes,
               "requests_audited": len(audits), "valid_calls": sum(a["status"] == "ok" for a in audits),
               "failed_attempts_retained": sum(a["status"] != "ok" for a in audits), "network_peak": network, "per_key_peak": per_key}
    write_json(OUT / "metrics.json", metrics)
    write_csv(OUT / "summary.csv", summaries); write_csv(OUT / "per_query.csv", rows)
    write_csv(OUT / "strata.csv", strata); write_csv(OUT / "paired_comparisons.csv", pairwise)
    write_json(OUT / "manual_skips.json", manual); write_json(OUT / "label_revisions.json", changes)
    lines = ["# PFAS40 共享检索与组合证据评测", "", f"完成时间：{metrics['at']}。六组复用原PFAS40问题及冻结top5检索，不重新生成答案、检索或向量。", "",
        "## 范围与判定", "", f"共享池含521个问题—原文块对、227个有序top5列表（205个不同来源集合）。35道支持题用于主要汇总，5道否定题单列核查。当前人工跳过{len(manual)}题，技术未完成0项。", "",
        "原PFAS40题集、240条QA及原报告已由用户整体人工复审确认；本次新增相关性标签由同一DeepSeek模型按独立提示词审查，未冒称人工复核。", "",
        "相关性0=无关/泛背景，1=部分要点或有用上下文，2=至少一个完整评分要点，3=全部要点完整；强支持阈值为2。所有系统共享池化qrels与每题IDCG。缺少检索位置仍计入P@5的5个位置；无相关项的Recall和零IDCG的nDCG记NA，逐项列出有效分母。", "",
        "组合指标检查top5原文对全部冻结评分要点的联合支撑及科学绑定，属于组合证据代理，不是穷尽化学事实召回。文献级Hit仅表示定位到相关论文，不保证定位到事实段。", "",
        "## 六组结果（支持题宏平均）", "", "|组别|nDCG@5|强支持Hit@5|池化Recall@5|完整要点覆盖|全部要点完整|文献Hit@5|", "|---|---:|---:|---:|---:|---:|---:|"]
    for r in summaries:
        fmt = lambda x: "NA" if x is None else f"{x:.4f}"
        lines.append("|" + "|".join([r["group"]] + [fmt(r[n]) for n in ["gNDCG@5_shared_pool", "Hit@5_grade2", "pooled_recall@5_grade2", "full_point_coverage@5", "all_rubric_points_full@5", "source_doc_Hit@5"]]) + "|")
    lines += ["", "## 修订与证据保护", "", f"初轮23项技术失败已恢复；12处单块/组合矛盾经原文裁决，最终未解决矛盾0。另按原题明确许可的parent-removal/degradation范围统一复核Q22全部34个来源目标，保留原文指标称谓；父体消失不作为脱氟或矿化证据。三处抄写错的目标ID未近似猜测；保留29个验证合格子记录，仅重新请求5个失败/关联目标，最后完整34项严检通过。初始与最终共{len(changes)}个要点状态变化，原标注均保留。", "",
        f"60篇源文件、100条精确引文、40个有限非零2560维查询向量及{len(protected)}个原QA/建库/发布文件SHA全部核对。仅judge请求，实际总并发峰值{network}，每key峰值{per_key}；HTTP200/截断/错误JSON不作为有效标注。", "",
        "## 局限与使用", "", "qrels来自六组top5与参考块并集，是池化判定而非全库穷尽相关性。问题复用已人工确认的QA40，不是独立抽样的检索题集；支持题参考证据来自25篇，否定题此前审计60篇全库，不能据此声称每篇均有支持题覆盖。", "",
        "标签具有同模型审查的相关误差风险，结构/引文校验不能代替科学判断。15对系统比较及难度/支持模式分层见CSV，均用同一有效题集；不将QA质量变化当作检索提升证明，不因系统排名修改金标准。与第一领域的题集和模型协议不同，不能合并为一个统一跨领域排名。", "",
        "文件：metrics.json、summary.csv、per_query.csv、strata.csv、paired_comparisons.csv、label_revisions.json、manual_skips.json。逐项原文、原始API尝试与派生链保存在本评测根目录；原QA报告保持不变。", ""]
    (OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    acceptance = {"complete": True, "at": utc(), "pool_labels": 521, "set_labels": 227, "remaining_consistency_conflicts": 0,
        "source_documents_sha_verified": 60, "exact_quotes_verified": 100, "query_vectors_2560_verified": 40,
        "protected_files_sha_unchanged": len(protected), "independent_metrics_recomputed": True, "source_derivation_chains_validated": True,
        "shared_IDCG_verified": True, "no_new_embeddings_or_qa_answers": True, "manual_skips": len(manual),
        "new_annotations_human_confirmed": False, "prior_qa_user_review_receipt": read_json(QA / "latest_reviewed_release.json")["receipt"],
        "metrics_sha256": file_hash(OUT / "metrics.json"), "report_sha256": file_hash(OUT / "report.md")}
    write_json(OUT / "acceptance.json", acceptance)
    archive_dir = Path(r"D:\Hyper-rag-case2-backups\pfas_shared_retrieval_final_20261015"); archive_dir.mkdir(exist_ok=True)
    archive = archive_dir / "verified_shared_retrieval.zip"
    assert not archive.exists(), "Final archive must not be overwritten"
    repo = Path(__file__).resolve().parents[1]
    files = [(p, "evaluation/" + p.relative_to(ROOT).as_posix()) for p in ROOT.rglob("*") if p.is_file() and p.suffix != ".zip" and p.name != "archive_pointer.json"]
    files += [(p, "source/" + p.relative_to(repo).as_posix()) for folder in (repo / "scripts", repo / "tests") for p in folder.glob("*pfas*retriev*.py")]
    for name in ["scripts/pfas_qa_common.py", "scripts/recover_pfas_shared_retrieval.py", "scripts/adjudicate_pfas_shared_retrieval.py", "scripts/audit_pfas_retrieval_metric_scope.py", "scripts/recover_pfas_metric_scope_targets.py", "scripts/audit_pfas_qa40_scores.py", "scripts/run_pfas_qa40.py", "web-ui/backend/runtime_requests.py", "tests/test_pfas_metric_scope.py", "tests/test_pfas_scope_target_recovery.py", "tests/test_pfas_shared_recovery.py", "tests/test_pfas_shared_adjudication.py"]:
        files.append((repo / name, "source/" + name))
    files = list({name: (p, name) for p, name in files}.values())
    entries = {name: file_hash(p) for p, name in files}
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for p, name in files: z.write(p, name)
        z.writestr("archive_manifest.json", json.dumps({"entries_sha256": entries, "prior_qa_archive": read_json(QA / "final_report/archive_pointer.json"), "human_review": read_json(QA / "latest_reviewed_release.json")}, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(archive) as z:
        assert all(hashlib.sha256(z.read(n)).hexdigest() == h for n, h in entries.items())
    pointer = {"complete": True, "at": utc(), "archive": str(archive), "archive_sha256": file_hash(archive), "entries_verified": len(entries), "readback_verified": True,
               "report": str(OUT / "report.md"), "acceptance": str(OUT / "acceptance.json"), "prior_qa_unchanged": True, "new_annotations_human_confirmed": False}
    write_json(OUT / "archive_pointer.json", pointer)
    write_json(QA / "latest_shared_retrieval_release.json", pointer)
    print(json.dumps({"complete": True, "groups": summaries, "archive_bytes": archive.stat().st_size, "entries_verified": len(entries), "protected_files_unchanged": len(protected)}), flush=True)


if __name__ == "__main__": main()
