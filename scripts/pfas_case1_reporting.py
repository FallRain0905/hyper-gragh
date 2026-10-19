"""Export report references without changing evaluation records or metrics."""
from __future__ import annotations

import csv
import hashlib
import shutil
from pathlib import Path


def export_method_reporting(public: Path) -> None:
    paper_root = Path(__file__).resolve().parents[2] / "Hyper-ChE"
    case1 = paper_root / "experiments/final_v1"
    report = paper_root / "docs/HyperChE_两案例实验结果汇报_20261015.md"
    shutil.copyfile(report, public / "reports/实验结果汇报_两案例与方法定位.md")
    references = public / "supplementary/case1_reference"
    references.mkdir(parents=True, exist_ok=True)
    names = ("shared_retrieval_summary_retained.csv", "composite_fact_recall_retained.csv")
    for source, name in zip((case1 / "retrieval" / names[0], case1 / "cfr" / names[1]), names):
        shutil.copyfile(source, references / name)

    fields = ["evidence_id", "claim_type", "claim_summary", "source_path", "source_sha256",
              "source_key", "protocol", "system", "metric", "slice", "value", "unit",
              "status", "limitations"]
    entries = []
    for case, root, query_slice in (("case1", references, "all 58 retrieval queries"),
                                     ("case2", public, "all 40 reused QA information needs")):
        retrieval = root / names[0] if case == "case1" else root / "retrieval" / names[0]
        fact = root / names[1] if case == "case1" else root / "cfr" / names[1]
        for source, kind in ((retrieval, "retrieval"), (fact, "fact")):
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            with source.open(encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
            if kind == "retrieval":
                rows = [r for r in rows if r["relevance_threshold"] == "grade>=2"]
            assert len(rows) == 5
            for row in rows:
                metric_keys = ("P@1", "Hit@5", "MRR", "gNDCG@5") if kind == "retrieval" else (
                    "facts", "supported_facts", "Composite Fact Recall@5", "macro_query_CFR@5")
                for metric in metric_keys:
                    entries.append(dict(zip(fields, [
                        f"{case}:{row['system']}:{metric}", "measured",
                        "Frozen within-case system result; percentage-point differences are arithmetic from these rows",
                        source.relative_to(public).as_posix(), digest,
                        row["system"] + (";grade>=2" if kind == "retrieval" else ""),
                        "top20 MRR; top5 Hit/gNDCG; shared pooled IDCG" if kind == "retrieval" else
                        "exact atomic-fact supporting chunk hit in top5; micro and macro-query",
                        row["system"], metric, query_slice if kind == "retrieval" else
                        ("150 accepted facts" if case == "case1" else "141 accepted facts in 35 positive queries"),
                        row[metric], "count" if metric in ("facts", "supported_facts") else "ratio",
                        "verified", "Within-case comparison; different adapters except F0/F1; no significance claim. "
                        + ("PFAS new labels/facts machine-reviewed; pooled, not exhaustive." if case == "case2" else
                           "Case1 frozen user-accepted release; not a controlled cross-domain effect.")
                    ])))
    source = public / "protocol/alignment_matrix.md"
    entries.append(dict(zip(fields, [
        "method:scope", "design_and_protocol", "Multiway representation motivates domain adaptation; F1 complete, F0 core adaptation with rerank off",
        source.relative_to(public).as_posix(), hashlib.sha256(source.read_bytes()).hexdigest(),
        "Method-level interpretation; five-group mapping", "same final cache and RRF top50 for F0/F1", "F0/F1", "not a measured structural causal effect",
        "retained five-group experiments", "", "", "verified",
        "Design rationale and verified protocol; does not establish physical coupling, universal structural superiority or isolated module gains."
    ])))
    with (public / "reports/method_claim_evidence.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(entries)


if __name__ == "__main__":
    export_method_reporting(Path(__file__).resolve().parents[2] / "Hyper-ChE/experiments/case2_pfas_v1")
