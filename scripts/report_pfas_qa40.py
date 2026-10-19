"""Validate immutable inputs and independently recompute the PFAS QA40 report."""
import collections
import hashlib
import json
import statistics
from pathlib import Path

import numpy as np

from scripts.pfas_qa_common import read_json, write_json, file_hash, digest, utc
from scripts.audit_pfas_qa40_scores import packet, validate, review_fields, source_span_catalog
from scripts.run_pfas_qa40 import GROUPS

ROOT = Path(r"C:\Users\19855\Desktop\Hyper-rag")
BUILD = ROOT / "case2_pfas_build"
QA = Path(r"D:\Hyper-rag-case2-backups\qa40_workspace")
AUDIT = QA / "score_audit_v1"
OUT = QA / "final_report"


def measure(records):
    n = len(records)
    supported = [r for r in records if r["answerable"]]
    negative = [r for r in records if not r["answerable"]]
    required = sum(len(r["required_key_points"]) for r in records)
    covered = sum(len(r["covered_key_points"]) for r in records)
    return {
        "questions": n,
        "Good Rate": round(sum(r["quality_label"] == "GOOD" for r in records) / n, 4),
        "Satisfactory-or-Better Rate": round(sum(r["quality_label"] != "POOR" for r in records) / n, 4),
        "Macro KPC": round(sum(len(r["covered_key_points"]) / len(r["required_key_points"]) for r in records) / n, 4),
        "Micro KPC": round(covered / required, 4),
        "Hallucination Rate": round(sum(r["hallucinated"] for r in records) / n, 4),
        "False Abstention Rate": round(sum(r["abstained"] for r in supported) / len(supported), 4) if supported else 0.0,
        "False Answer Rate": round(sum(not r["abstained"] for r in negative) / len(negative), 4) if negative else 0.0,
        "Unanswerable Abstention Accuracy": round(sum(r["abstained"] for r in negative) / len(negative), 4) if negative else 0.0,
        "Citation Presence Rate": round(sum(r["citation_present"] for r in records) / n, 4),
        "Citation Support Score (LLM)": round(sum(r["citation_support_score"] for r in records) / n, 4),
    }


def table(rows, columns):
    def fmt(v):
        if isinstance(v, float):
            return f"{v * 100:.2f}%"
        return str(v)
    return "| " + " | ".join(title for key, title in columns) + " |\n| " + " | ".join("---" for _ in columns) + " |\n" + "\n".join(
        "| " + " | ".join(fmt(row[key]) for key, title in columns) + " |" for row in rows)


def main():
    OUT.mkdir(exist_ok=True)
    summary = read_json(AUDIT / "summary.json")
    assert summary["status"]["complete"] and summary["status"]["completed"] == 240 and not summary["status"]["errors"]
    assert summary["status"]["original_records_unchanged"]
    gold_path = QA / "gold_v2/qa_gold.json"
    gold = read_json(gold_path)
    assert file_hash(gold_path) == "aebf4e38e16fdf0e811f230d1f699c901e2b657cbbfc161b36b16e43c3f061c1"
    assert gold["human_confirmed"] is False and gold["status"] == "machine_verified_gold"
    questions = {q["question_id"]: q for q in gold["qa_questions"]}
    chunks = read_json(gold["source"]["chunks"])
    assert file_hash(gold["source"]["chunks"]) == gold["source"]["chunks_sha256"]
    assert len(chunks) == 1330 and len(questions) == 40 and sum(q["answerable"] for q in questions.values()) == 35
    corpus_manifest = Path(gold["source"]["manifest"])
    assert file_hash(corpus_manifest) == gold["source"]["manifest_sha256"]
    docs = [json.loads(line) for line in corpus_manifest.read_text(encoding="utf-8-sig").splitlines() if line]
    assert len(docs) == 60
    for row in docs:
        assert file_hash(corpus_manifest.parent / "documents" / row["corpus_filename"]) == row["source_sha256"]
    quote_count = 0
    support_docs = set()
    for q in questions.values():
        assert not q.get("human_confirmed")
        for e in q.get("evidence", []):
            raw = chunks[e["chunk_id"]]["content"]
            assert raw[e["start_char"]:e["end_char"]] == e["quote"]
            assert hashlib.sha256(e["quote"].encode()).hexdigest() == e["quote_sha256"]
            assert hashlib.sha256(raw.encode()).hexdigest() == e["chunk_content_sha256"]
            quote_count += 1
            support_docs.add(e["doc_id"])
    assert quote_count == 100 and len(support_docs) == 25
    for qid, q in questions.items():
        v = read_json(QA / "evaluation_v2/query_vectors" / (qid + ".json"))
        assert v["signature"] == digest({"query": q["question"], "model": "Qwen/Qwen3-Embedding-4B", "dim": 2560})
        a = np.asarray(v["vector"])
        assert a.shape == (2560,) and np.isfinite(a).all() and np.any(a)

    records = []
    review_style = collections.Counter()
    for group in GROUPS:
        for qid, q in questions.items():
            original_path = QA / "evaluation_v2/records" / group / (qid + ".json")
            original = read_json(original_path)
            original_rel = original_path.relative_to(QA / "evaluation_v2").as_posix()
            assert file_hash(original_path) == summary["protocol"]["original_record_hashes"][original_rel]
            retrieval = read_json(QA / "evaluation_v2/retrieval" / group / (qid + ".json"))
            data = packet(q, original, retrieval, chunks)
            row = read_json(AUDIT / "reviews" / group / (qid + ".json"))
            assert row["original_record_sha256"] == file_hash(original_path)
            assert row["input_signature"] == digest({"data": data, "original_record": file_hash(original_path), "protocol": summary["protocol"]["version"]})
            for decision in (row["review"], row["adjudication"]):
                if decision is None:
                    continue
                validate(decision, data)
                catalog = source_span_catalog(data)
                for c in decision["claim_checks"]:
                    if c.get("source_span_id"):
                        span = catalog[c["source_span_id"]]
                        assert c["evidence_rank"] == span["rank"] and c["source_quote"] == span["exact_raw_text"]
            decision = row["adjudication"] or row["review"]
            revised = read_json(AUDIT / "audited_records" / group / (qid + ".json"))
            for field, value in review_fields(decision, q).items():
                assert revised[field] == value, (group, qid, field)
            assert revised["generated_answer"] == original["generated_answer"]
            assert revised["good"] == (revised["quality_label"] == "GOOD")
            assert revised["satisfactory_or_better"] == (revised["quality_label"] in ("GOOD", "SATISFACTORY"))
            assert revised["key_point_coverage"] == len(revised["covered_key_points"]) / len(q["required_key_points"])
            assert len(revised["covered_key_points"]) + len(revised["missing_key_points"]) == len(q["required_key_points"])
            records.append(revised)
            review_style[row.get("response_format_protocol", "original-schema-with-bounded-format-feedback")] += 1

    before = read_json(QA / "evaluation_v2/cache_hashes_before.json")
    for cache, hashes in before.items():
        for name, h in hashes.items():
            assert file_hash(BUILD / cache / name) == h, (cache, name)
    preserved = read_json(QA / "audit238_preservation.json")
    assert all(file_hash(QA / rel) == h for rel, h in preserved["hashes"].items())
    cleanup_pointer = read_json(BUILD / "diagnostics/latest_cleanup_report.json")
    cleanup = read_json(cleanup_pointer["report"])
    cleanup_plan = read_json(cleanup["plan"])
    assert all(file_hash(p) == h for p, h in cleanup_plan["published_before_hashes"].items())

    aggregates = []
    supported_rows, negative_rows = [], []
    for group, spec in GROUPS.items():
        rs = [r for r in records if r["group"] == group]
        assert len(rs) == 40
        metrics = measure(rs)
        saved = next(row for row in summary["groups"] if row["group"] == group)
        for k, v in metrics.items():
            assert abs(saved[k] - v) < 0.00001, (group, k, saved[k], v)
        aggregates.append({"group": group, "label": spec["label"], **metrics})
        supported_rows.append({"group": group, **measure([r for r in rs if r["answerable"]])})
        negative_rows.append({"group": group, **measure([r for r in rs if not r["answerable"]])})
    for comparison in summary["pairwise"]:
        a = {r["question_id"]: r for r in records if r["group"] == comparison["group_a"]}
        b = {r["question_id"]: r for r in records if r["group"] == comparison["group_b"]}
        assert set(a) == set(b) == set(questions) and comparison["paired_questions"] == 40
        assert sum(a[k]["good"] and not b[k]["good"] for k in a) == comparison["a_good_b_not"]
        assert sum(b[k]["good"] and not a[k]["good"] for k in a) == comparison["b_good_a_not"]
        assert abs(round(statistics.mean(a[k]["key_point_coverage"] - b[k]["key_point_coverage"] for k in a), 4) - comparison["macro_kpc_delta_a_minus_b"]) < 0.00001
    for field, saved_rows in summary["strata"].items():
        for saved in saved_rows:
            subset = [r for r in records if r["group"] == saved["group"] and str(r[field]) == saved[field]]
            metrics = measure(subset)
            for key, value in metrics.items():
                assert abs(saved[key] - value) < 0.00001, (field, key)
    requests = []
    for phase in ("evaluation_v2", "score_audit_v1"):
        rows = [json.loads(x) for x in (QA / phase / "request_audit.jsonl").read_text(encoding="utf-8").splitlines() if x]
        assert all(r["requests"]["network_peak"] <= 10 and r["requests"]["key_peak"] <= 1 for r in rows)
        if phase == "score_audit_v1":
            assert all(r["role"] == "judge" for r in rows)
        requests.append({"phase": phase, "attempts": len(rows), "valid_requests": sum(r["status"] == "ok" for r in rows),
                         "network_peak": max(r["requests"]["network_peak"] for r in rows),
                         "key_peak": max(r["requests"]["key_peak"] for r in rows)})
    raw_summary = read_json(QA / "evaluation_v2/summary.json")
    changes = summary["changed_scores"]
    q30 = read_json(AUDIT / "audited_records/original_hypergraph/PFAS40-Q30.json")
    assert q30["quality_label"] == "SATISFACTORY" and not q30["hallucinated"]
    assert q30["key_point_coverage"] == 1 / 3
    delta_rows = []
    for r in aggregates:
        old = next(x for x in raw_summary["groups"] if x["group"] == r["group"])
        delta_rows.append({"group": r["group"], "raw_good": old["Good Rate"], "audited_good": r["Good Rate"],
                           "raw_kpc": old["Macro KPC"], "audited_kpc": r["Macro KPC"],
                           "raw_hallucination": old["Hallucination Rate"], "audited_hallucination": r["Hallucination Rate"]})
    metrics = {"at": utc(), "complete": True, "audited_records": 240, "manual_skips": [], "technical_failures_remaining": [],
               "gold_sha256": file_hash(gold_path), "groups": aggregates, "supported": supported_rows, "negative": negative_rows,
               "raw_vs_audited": delta_rows, "pairwise": summary["pairwise"], "strata": summary["strata"],
               "grading_disagreements": summary["status"]["disagreements"], "changed_final_scores": len(changes),
               "request_history": requests, "review_format_provenance": dict(review_style),
               "acceptance": {"documents": 60, "chunks": 1330, "quotes": 100, "supported_reference_documents": 25,
                              "query_vectors_finite_2560": 40, "immutable_cache_hashes": 32,
                              "published_file_hashes": len(cleanup_plan["published_before_hashes"]),
                              "original_records_unchanged": 240, "prior_success_files_unchanged": len(preserved["hashes"]),
                              "independent_metrics_recomputed": True, "all_reviews_exact_span_validated": True,
                              "human_confirmed": False}}
    write_json(OUT / "metrics.json", metrics)
    lines = ["# PFAS QA40 六组最终评分复核报告", "", "## 完成状态", "",
             "60篇、1330块语料上的40题 × 6组，共240条答题及评分复核已完成。人工跳过0项，未解决技术失败0项。原答案、首轮判分和金标准原样保留；最终分数另存。",
             "", "**题集为 machine_verified_gold，human_confirmed=false。所有题集验证、判分和裁决均为LLM辅助，未经过独立人工确认。**",
             "", "## 协议与范围", "",
             "- 35道支持题、5道否定题。支持题100条精确引文来自25篇；5道否定题逐篇审计全部60篇1330块。不能称支持题直接覆盖全部60篇。",
             "- 题集SHA256：`" + file_hash(gold_path) + "`。题型与难度按冻结题集分层，详细表见 score_audit_v1 的 by_*.csv。",
             "- 答题与judge：科研组 SiliconFlow `deepseek-ai/DeepSeek-V4-Flash`，temperature=0，reasoning_effort=low；总实际请求上限10、每key上限1。",
             "- Query embedding：Qwen/Qwen3-Embedding-4B，2560维；40个有效向量全部复用。审计未调用embedding，未重新生成答案或检索。",
             "- 各组取前5个完整原文块；结构化关系仅作提示，须用原文支撑。最终组采用FinalGraphIndex，其余图组采用StructuredGraphIndex，文本组采用BM25+Dense+RRF。",
             "- 盲审隐藏组别与首轮等级；覆盖、幻觉或等级分歧再按实际答案及检索原文裁决。裁决阶段会看到原评分，仍可能存在锚定效应。",
             "- 缺少细节与虚构事实分别检查。GOOD要求全要点覆盖且无幻觉；SATISFACTORY为正确但不完整；错误核心、支持题拒答或幻觉为POOR。",
             "- 坏JSON、截断、空答案、错误引用和不完整评分partition不计完成；4096/8192/16384有界重试。仅允许唯一空白格式恢复，或模型显式选择原文片段ID；不自动改单位、数值、标点或rank。",
             "", "## 最终审计指标（每组40题）", "",
             table(aggregates, [("group", "组别"), ("questions", "题数"), ("Good Rate", "GOOD"), ("Satisfactory-or-Better Rate", "至少SATISFACTORY"),
                                ("Macro KPC", "宏平均要点覆盖"), ("Micro KPC", "微平均要点覆盖"), ("Hallucination Rate", "幻觉率")]),
             "", "GOOD数：原始超图24/40、化学二元图21/40、化学超图20/40、混合文本24/40、归一化超图20/40、final超图23/40。",
             "", "宏KPC先按每题覆盖要点比例计算再取均值；微KPC为全部已覆盖要点数除以全部必要要点数。1题对应总体2.5个百分点。",
             "", "## 支持题与否定题", "",
             "### 35道支持题", "",
             table(supported_rows, [("group", "组别"), ("Good Rate", "GOOD"), ("Satisfactory-or-Better Rate", "至少SATISFACTORY"),
                                    ("Macro KPC", "宏KPC"), ("False Abstention Rate", "错误拒答"), ("Hallucination Rate", "幻觉率")]),
             "", "### 5道否定题", "",
             table(negative_rows, [("group", "组别"), ("Unanswerable Abstention Accuracy", "正确拒答率"), ("False Answer Rate", "错误作答率")]),
             "", "混合文本与归一化超图各有1/5道否定题错误作答；其他四组均5/5正确拒答。负题每1题对应20个百分点，样本量很小。",
             "", "## 首轮与审计后比较", "",
             table(delta_rows, [("group", "组别"), ("raw_good", "首轮GOOD"), ("audited_good", "审计GOOD"), ("raw_kpc", "首轮宏KPC"),
                               ("audited_kpc", "审计宏KPC"), ("raw_hallucination", "首轮幻觉"), ("audited_hallucination", "审计幻觉")]),
             "", f"盲审与首轮在等级、幻觉或覆盖要点上产生{summary['status']['disagreements']}条分歧，最终有{len(changes)}条记录的等级、幻觉或KPC改变。原始分数未覆盖，所有依据在 reviews/ 与 changed_scores 中。",
             "", "### Q30纠正示例", "",
             "原始超图Q30首轮为POOR、幻觉=true、KPC=0，并错称答案遗漏low-temperature。实际答案明确包含低温DMSO/NaOH矿化及产物去向；检索原文支持其机理概括。裁决改为SATISFACTORY、幻觉=false、KPC=1/3。仍缺氯介导单电子氧化与酸氟化物/水解中间步骤，未因此给满分。",
             "", "## 配对与结果解释", "",
             "所有组均使用同一40题配对，无缺失或跳过造成的分母差异。完整15组两两比较见 score_audit_v1/pairwise.csv。",
             "", "- 混合文本宏KPC为83.13%，高于final的78.33%；GOOD率为60.0%，final为57.5%。",
             "- 原始超图至少SATISFACTORY为97.5%，本次最高；final为95.0%。",
             "- final相对归一化超图的宏KPC提升约7.08个百分点，GOOD提升7.5个百分点；该比较不能单独归因于数值实例，因为表示、嵌入文本和排序也有变化。",
             "- final在本题集上没有全面领先原始超图或混合文本。首轮final较高的GOOD率在复核后下降，报告采用审计后结果。",
             "- 未做显著性推断，不能用40题的小样本差异宣称普遍优越。",
             "", "## 引文、检索与局限", "",
             "所有标签的Citation Reference Validity均为100%，只说明引用编号存在，不能证明事实由该块支持。Citation Support Score仍是LLM判断。原有Gold Chunk Recall@5属于对已标注金标准块的命中比例，标注并非完整qrels，不能解释为全库真实召回率，也不能从QA质量推出检索全面更好。",
             "", "同一V4模型参与金标准复核、答题和judge；不同提示词不构成独立人工或独立模型评审。OCR/LaTeX原文被原样引用，精确字符校验也不能保证原论文的抽取无误或科学解释正确。支持证据仅来自25篇，可能有选题偏差。不同检索与建图方式有多项同时变化，当前实验是固定协议内的系统比较。",
             "", "## 可恢复与验收证据", "",
             "- 全部240审计逐点、实际答案片段及检索原文片段通过校验；指标、分层和配对统计独立重算一致。",
             "- 60篇文档哈希、100引文、40个有限非零2560维query vector已核验。",
             "- 32个验收缓存文件、329个发布文件、240原始QA及1070个此前成功文件哈希不变；EFU关闭，未重建向量。",
             "- 最后两项采用 explicit-raw-span-schema-v2 的明确响应格式恢复；科学评分规则和原文输入一致，格式差异另存provenance。",
             "- 请求统计包含所有历史成功和失败尝试，审计最后的全resume阶段请求为0，不能将该0误作整个审计无API调用。详见 metrics.json/request_history。",
             "- 清理过期备份的报告及替代恢复指针保留；不再要求已授权删除的旧快照存在。",
             "", "## 文件入口", "",
             "- `metrics.json`：验收、重算指标、请求峰值与格式provenance。",
             "- `../gold_v2/qa_gold.json`：冻结题集及逐题证据。",
             "- `../evaluation_v2/records/`：240条原始答案和首轮判分。",
             "- `../score_audit_v1/reviews/`、`audited_records/`：复核、裁决及最终记录。",
             "- `../score_audit_v1/summary.csv`、`by_*.csv`、`pairwise.csv`：汇总、分层和配对指标。",
             "", "本报告完成时间（UTC）：" + utc(), ""]
    (OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    assert "57.50%" in (OUT / "report.md").read_text(encoding="utf-8")
    write_json(OUT / "acceptance.json", {"complete": True, "checks": metrics["acceptance"], "report_sha256": file_hash(OUT / "report.md"), "metrics_sha256": file_hash(OUT / "metrics.json"), "at": utc()})
    print(json.dumps({"complete": True, "report": str(OUT / "report.md"), "groups": aggregates, "changed_scores": len(changes), "requests": requests}, ensure_ascii=False))


if __name__ == "__main__":
    main()
