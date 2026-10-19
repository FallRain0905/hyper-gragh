"""Create a compact evidence ledger and case1-shaped PFAS release workspace."""
from pathlib import Path
import json
import re
import zipfile

from scripts.align_pfas_case1 import BASE, QA, WORK, PUBLIC, GROUPS, protocol
from scripts.pfas_qa_common import file_hash, write_json, utc


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    for folder in ("benchmark", "retrieval", "cfr", "qa", "protocol", "reports", "supplementary"):
        (PUBLIC / folder).mkdir(parents=True, exist_ok=True)
    paths = [BASE / "Hyper-ChE/paper/README.md", BASE / "Hyper-ChE/paper/latex/hyperche_arxiv_body.tex",
             BASE / "Hyper-ChE/paper/drafts/en/04_experimental_setup.md",
             BASE / "Hyper-ChE/experiments/final_v1/README.md", BASE / "Hyper-ChE/experiments/final_v1/publication_manifest.json",
             BASE / "Hyper-ChE/experiments/final_v1/protocol/qa_final_protocol.json",
             BASE / "Hyper-ChE/scripts/reproduce_paper_metrics.py",
             BASE / "hyper-gragh/outputs/retrieval_benchmark/retrieval_formal_v5_chunk_rerank_full58_20260910/run_protocol.json",
             QA / "gold_v2/qa_gold.json", QA / "latest_reviewed_release.json", QA / "latest_shared_retrieval_release.json"]
    evidence = [{"path": str(p), "exists": p.exists(), "sha256": file_hash(p) if p.is_file() else None} for p in paths]
    skill_map = Path(r"C:\Users\19855\.codex\plugins\cache\personal\hyperche-arxiv-paper\0.1.0\skills\hyperche-paper-writer\references\hyperche-evidence-map.md")
    text = skill_map.read_text(encoding="utf-8")
    references = []
    for block in re.findall(r"```text\n(.*?)```", text, re.S):
        for value in block.splitlines():
            if value.startswith("C:\\") or value.startswith("hyper-gragh\\"):
                p = Path(value) if value.startswith("C:\\") else BASE / value
                references.append({"path": str(p), "exists": p.exists(), "authority": "historical locator; latest Oct08 final_v1 supersedes metric examples"})
    write_json(WORK / "evidence_ledger.json", {"created_at": utc(), "sources": evidence, "skill_locator_checks": references,
                                             "authority": "Oct08 arXiv draft and public final_v1 retained five-system package"})
    write_json(PUBLIC / "protocol/evidence_ledger.json", {"created_at": utc(), "sources": evidence, "skill_locator_checks": references})
    write_json(PUBLIC / "protocol/case2_alignment_protocol.json", protocol())
    (PUBLIC / "README.md").write_text("""# Case 2 PFAS experiment evidence (alignment in progress)

This new folder follows `experiments/final_v1`, the Case 1 evidence package
retained by the 2026-10-08 arXiv draft. Its five systems are B0, B1, B2, F0, F1.
New aligned runs are still in progress; a manifest with `complete: true` is
required before treating this directory as a completed results release.

- `benchmark/`: PFAS40 questions and compact top20 candidate IDs/ranks.
- `retrieval/`: shared-qrels metrics, slices, per-query ranks and source diagnostics.
- `cfr/`: exact-source atomic facts, machine audit, shared qrels and CFR@5.
- `qa/`: F1 supplementary 40-question QA, protocol and diagnostic slices.
- `protocol/`: authoritative source hashes, alignment matrix and run settings.
- `reports/`: evidence interpretation and limitations.
- `supplementary/`: references to immutable earlier six-group PFAS results.

The full resumable workspace is on D:, not inside this compact public folder.
Accepted corpus caches, graph stores and vectors are never rebuilt for this run.
""", encoding="utf-8")
    (PUBLIC / "protocol/alignment_matrix.md").write_text("""# Case1 / PFAS protocol alignment

Authority: latest Oct08 paper draft and `Hyper-ChE/experiments/final_v1`.
The historical seven-system plan and August PFAS qualitative draft are not the
current headline experiment. The five retained systems below are the main table.

| Code | Retained system | Case1 adapter | PFAS aligned adapter / cache |
|---|---|---|---|
| B0 | original_hypergraph | actual upstream hyper_query | same, hyper_base, generic query prompt |
| B1 | chem_prompt_graph | structured graph hybrid | same, hyper_chem_prompt, binary view |
| B2 | chem_prompt_hypergraph | actual upstream hyper_query | same, hyper_chem_prompt, PFAS query prompt |
| F0 | normalized_final_no_rerank | hybrid RRF top50, rerank off | same, hyper_final |
| F1 | normalized_final | same RRF top50, rerank on | same, hyper_final |

F0/F1 must share exact candidate edge/chunk pools for every query. The previous
`normalized_hypergraph` run used hyper_norm and is not F0. Previous B0/B2 used a
different structured adapter; those frozen outputs remain supplementary only.
B1/B2 are system comparisons, not single-variable arity/prompt ablations.

| Dimension | Case1 retained release | Case2 PFAS alignment |
|---|---|---|
| Corpus | 60 docs / 1328 chunks | 60 docs / 1330 chunks |
| Retrieval queries | 58, independent retrieval benchmark | frozen PFAS40, reused QA information needs |
| Ranked depth / metric k | 20 / 5 | same |
| Primary / sensitivity grade | >=2 / >=3 (also >=1) | same DIRECT/STRONG_SUPPORT/BACKGROUND rubric |
| MRR | entire returned top20 | same; not truncated MRR@5 |
| gNDCG denominator | shared complete pooled IDCG; zero -> 0 included | same, retain all historical seed pairs |
| CFR | exact atomic fact supporting-chunk hit in top5 | same; newly source-verified PFAS atomic facts |
| Qrels / new fact acceptance | user-accepted case1 audit | new machine labels, not covered by old QA human confirmation |
| QA main display | supplementary F1 only, 40 questions | same; old six-group QA kept supplementary |
| QA evidence | top5, legacy, option evidence_budget_chars=1500 | same actual function; code counts tokens, despite option name |
| QA model / sampling | Kimi-k2.6, DashScope, temp1/top_p.95 | authorized DeepSeek-V4-Flash, SiliconFlow, temp0/low |
| Embedding | Qwen3-Embedding-4B, 2560 | same; reuse corpus and question vectors |
| EFU repair | false | false |

Cross-case numerical differences are not a controlled domain-only comparison:
the corpora, questions, annotation models/status and QA model/sampling differ.
New qrels need their own protocol because historical PFAS grade3 required every
rubric point, whereas case1 uses DIRECT/decisive requested facts. The old 521
successful labels are preserved; their candidate pairs seed the larger pool but
their grades are not silently relabelled or overwritten.
""", encoding="utf-8")
    supplementary = {"original_qa": str(QA / "human_reviewed_release_20261015"),
                     "six_group_qa": str(QA / "final_report"),
                     "six_group_top5_qrels": str(QA / "shared_retrieval_v1/final_report"),
                     "note": "Historical accepted artifacts preserved; different adapters, grade rubric and metric denominator. Do not merge into aligned five-system main table."}
    write_json(PUBLIC / "supplementary/previous_results.json", supplementary)
    write_json(PUBLIC / "publication_manifest.json", {"snapshot": "case2-pfas-case1-aligned-v1", "complete": False,
                                                     "retained_systems": list(GROUPS), "workspace": str(WORK)})
    source_files = [BASE / "hyper-gragh/scripts" / name for name in
                    ("align_pfas_case1.py", "prepare_pfas_case1_alignment.py", "package_pfas_case1.py", "reproduce_pfas_case1_package.py", "pfas_qa_common.py",
                     "structured_graph_retrieval.py", "upstream_hyper_query_retrieval.py", "final_graph_retrieval.py",
                     "evaluate_shared_retrieval_qrels.py", "run_qa_smoke_llm.py", "run_qa_formal_llm.py")]
    source_files += [BASE / "hyper-gragh/web-ui/backend/runtime_requests.py",
                     BASE / "hyper-gragh/hyperrag/operate.py", WORK / "evidence_ledger.json",
                     PUBLIC / "protocol/case2_alignment_protocol.json", PUBLIC / "protocol/alignment_matrix.md"]
    z = WORK / "source_and_protocol_before.zip"
    if z.exists(): raise ValueError("Source snapshot already exists; do not overwrite provenance")
    manifest = {}
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as archive:
        for i, p in enumerate(source_files):
            name = str(i).zfill(2) + "_" + p.name
            archive.write(p, name)
            manifest[name] = file_hash(p)
    import hashlib
    with zipfile.ZipFile(z) as archive:
        assert all(hashlib.sha256(archive.read(name)).hexdigest() == sha for name, sha in manifest.items())
    write_json(WORK / "snapshot_manifest.json", {"complete": True, "sha256": file_hash(z), "files": manifest,
                                               "bytes": z.stat().st_size, "created_at": utc()})
    print(json.dumps({"target": str(PUBLIC), "workspace": str(WORK), "snapshot_bytes": z.stat().st_size, "files": len(manifest), "verified": True}))


if __name__ == "__main__": main()
