"""Portable, API-free metrics and checksum verification for the PFAS release."""
import hashlib
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


def load(p): return json.loads(p.read_text(encoding="utf-8-sig"))


def reproduce(root):
    manifest = load(root / "publication_manifest.json")
    assert manifest["complete"]
    for a in manifest["artifacts"]:
        assert hashlib.sha256((root / a["path"]).read_bytes()).hexdigest() == a["sha256"], a["path"]
    systems = manifest["retained_systems"]
    candidates = load(root / "benchmark/candidate_rankings.json")["candidate_union"]
    qs = load(root / "benchmark/retrieval_queries.json")["queries"]
    skips = {r["query_id"] for r in load(root / "reports/manual_skips.json")}
    qs = [q for q in qs if q["query_id"] not in skips]
    grades = {(r["query_id"], r["chunk_id"]): r["relevance_grade"] for r in load(root / "cfr/shared_qrels.json")["qrels"]}
    assert len(grades) == manifest["dimensions"]["qrels"] and set(grades) == {(r["query_id"], r["chunk_id"]) for r in candidates}
    ranks = defaultdict(list)
    for r in candidates:
        for o in r["system_occurrences"]: ranks[o["system"], r["query_id"]].append((o["retrieval_rank"], r["chunk_id"]))
    def dcg(v): return sum((2**g - 1) / math.log2(i+2) for i, g in enumerate(v[:5]))
    reference = load(root / "retrieval/shared_retrieval_summary_retained.json")["rows"]
    expected_per = {}
    for group in systems:
        for threshold in (1,2,3):
            rows = []
            for q in qs:
                qid = q["query_id"]
                ordered = sorted(ranks[group, qid])
                assert [rank for rank, _ in ordered] == list(range(1, len(ordered)+1))
                gs = [grades[qid, cid] for _, cid in ordered]
                ideal = sorted([g for (qq, _), g in grades.items() if qq == qid], reverse=True)
                first = next((i+1 for i,g in enumerate(gs) if g >= threshold), None)
                idcg = dcg(ideal)
                item = {"P@1": float(bool(gs) and gs[0]>=threshold), "Hit@5": float(any(g>=threshold for g in gs[:5])),
                        "MRR": 1/first if first else 0., "gNDCG@5": dcg(gs)/idcg if idcg else 0., "IDCG@5":idcg}
                rows.append(item)
                expected_per[group,qid,threshold] = item
            ref = next(r for r in reference if r["system"] == group and r["threshold"] == threshold)
            assert ref["queries"] == len(rows)
            for key in ("P@1", "Hit@5", "MRR", "gNDCG@5"):
                assert abs(statistics.mean(r[key] for r in rows)-ref[key]) < 1e-12, (group, threshold, key)
    facts = load(root / "cfr/composite_fact_gold_machine_verified.json")["queries"]
    refs = load(root / "cfr/composite_fact_recall_retained.json")["rows"]
    for group in systems:
        values, macro = [], []
        for q in facts:
            if q["query_id"] in skips: continue
            top = {cid for rank,cid in ranks[group,q["query_id"]] if rank <= 5}
            hits = [int(bool(top & set(f["supporting_chunk_ids"]))) for f in q["atomic_facts"]]
            values.extend(hits)
            if hits: macro.append(statistics.mean(hits))
        ref = next(r for r in refs if r["system"] == group)
        assert len(values) == ref["facts"]
        assert abs(statistics.mean(values)-ref["CFR@5"]) < 1e-12
        assert abs(statistics.mean(macro)-ref["macro_query_CFR@5"]) < 1e-12
    def csv_rows(path):
        with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
    for r in csv_rows(root/"retrieval/shared_retrieval_summary_retained.csv"):
        threshold = int(r["relevance_threshold"].split(">=")[1])
        ref = next(x for x in reference if x["system"]==r["system"] and x["threshold"]==threshold)
        for k in ("P@1","Hit@5","MRR","gNDCG@5"): assert abs(float(r[k])-ref[k]) <= 0.00000051
    per_rows=csv_rows(root/"retrieval/shared_retrieval_per_query_retained.csv")
    assert len(per_rows)==len(systems)*len(qs)*3
    for r in per_rows:
        key=(r["system"],r["query_id"],int(r["threshold"].split(">=")[1]))
        for k,v in expected_per[key].items(): assert abs(float(r[k])-v)<=0.00000051
    for r in csv_rows(root/"retrieval/shared_retrieval_ranked_topk_retained.csv"):
        ordered=sorted(ranks[r["system"],r["query_id"]])
        rank=int(r["rank"])
        assert 1<=rank<=5 and ordered[rank-1][1]==r["chunk_id"]
        assert grades[r["query_id"],r["chunk_id"]]==int(r["qrel_grade"])
    for r in csv_rows(root/"retrieval/source_level_hit_summary_retained.csv"):
        threshold=int(r["threshold"].split(">=")[1]);hits=[];unique=[];duplicates=[]
        for q in qs:
            ordered=[cid for rank,cid in sorted(ranks[r["system"],q["query_id"]]) if rank<=5]
            hit=any(grades[q["query_id"],cid]>=threshold for cid in ordered)
            hits.append(int(hit));docs={cid.split("_CHK_")[0] for cid in ordered}
            unique.append(len(docs));duplicates.append(1-len(docs)/len(ordered) if ordered else 0.)
        assert abs(float(r["Source-level Hit@5"])-statistics.mean(hits))<=0.00000051
        assert float(r["Source-level Hit@5"])==float(r["chunk Hit@5 (same qrel policy)"])
        assert abs(float(r["mean unique sources@5"])-statistics.mean(unique))<=0.00000051
        assert abs(float(r["mean source duplicate ratio@5"])-statistics.mean(duplicates))<=0.00000051
    for r in csv_rows(root/"cfr/composite_fact_recall_retained.csv"):
        ref=next(x for x in refs if x["system"]==r["system"])
        assert int(r["facts"])==ref["facts"] and int(r["supported_facts"])==ref["recalled_facts"]
        assert abs(float(r["Composite Fact Recall@5"])-ref["CFR@5"])<=0.00000051
        assert abs(float(r["macro_query_CFR@5"])-ref["macro_query_CFR@5"])<=0.00000051
    records=[json.loads(s) for s in (root/"qa/qa_final_records.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(records)==40 and len({r["question_id"] for r in records})==40
    for r in records:
        covered,missing=r["covered_key_points"],r["missing_key_points"]
        assert not set(covered)&set(missing) and set(covered)|set(missing)==set(r["required_key_points"])
        assert r["good"]==(r["quality_label"]=="GOOD")
        assert not (r["hallucinated"] and r["quality_label"] in ("GOOD","SATISFACTORY"))
        assert abs(r["key_point_coverage"]-len(covered)/len(r["required_key_points"]))<1e-12
    qa=load(root/"qa/qa_final_summary_normalized_final.json")["groups"][0]
    expected={"Good Rate":sum(r["good"] for r in records)/40,
              "Satisfactory-or-Better Rate":sum(r["satisfactory_or_better"] for r in records)/40,
              "Macro KPC":statistics.mean(r["key_point_coverage"] for r in records),
              "Micro KPC":sum(len(r["covered_key_points"]) for r in records)/sum(len(r["required_key_points"]) for r in records),
              "Hallucination Rate":sum(r["hallucinated"] for r in records)/40}
    for k,v in expected.items(): assert abs(qa[k]-round(v,4))<1e-12
    return {"passed": True, "verified_artifacts": len(manifest["artifacts"]), "systems": len(systems),
            "queries": len(qs), "qrels": len(grades), "retrieval_and_cfr_reproduced": True,
            "case1_csv_values_and_source_policy_verified":True,"qa_summary_reproduced":True}


if __name__ == "__main__":
    print(json.dumps(reproduce(Path(__file__).resolve().parent), ensure_ascii=False, indent=2))
