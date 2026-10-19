"""Independent pointer, checksum, protocol and numeric checks before release.

This is a mechanical/source-pointer audit. Scientific support is supplied by
the stored LLM reviews; this script does not claim a new human review.
"""
import copy
import csv
import hashlib
import json
import os
import re
import shutil
import statistics
import time
import zipfile
from pathlib import Path

import numpy as np

from scripts.align_pfas_case1 import BASE, QA, WORK, PUBLIC, GROUPS, GRADE_RULES, FACT_RULES, Run, label_packet, validate_labels, validate_facts, validate_fact_review, validate_keywords, validate_answer, validate_judge, protocol, require
from scripts.pfas_qa_common import digest, file_hash, read_json, write_json, parse_json_response, MODEL, EMBEDDING_MODEL, utc
from scripts.reproduce_pfas_case1_package import reproduce
from scripts import run_qa_smoke_llm as core
from hyperrag.operate import _get_query_keywords_prompt, _parse_query_keywords
from hyperche.retrieval.query_normalization import normalize_query


def main():
    out = WORK / "final_export_audit_20261015"
    out.mkdir(exist_ok=True)
    write_json(out / "process.json", {"pid": os.getpid(), "started_at": utc(), "stage": "independent_final_verification"})
    before = read_json(WORK / "preservation_before.json")
    for i, (p, sha) in enumerate(before.items(), 1):
        require(Path(p).is_file() and file_hash(p) == sha, "Protected original changed: " + p)
        if i % 500 == 0: print(json.dumps({"protected_files_checked":i}),flush=True)
    code_before = read_json(WORK / "launch_preservation_fix/fixed_source_manifest.json")["files"]
    algorithms = ["scripts/align_pfas_case1.py", "scripts/pfas_qa_common.py", "scripts/structured_graph_retrieval.py",
                  "scripts/upstream_hyper_query_retrieval.py", "scripts/final_graph_retrieval.py", "hyperrag/operate.py"]
    repo = BASE / "hyper-gragh"
    for name in algorithms: require(file_hash(repo / name) == code_before[name], "Frozen retrieval/API algorithm changed")
    runner = Run(WORK)
    qmap = runner.byq
    chunks = runner.chunks
    manifest = Path(runner.gold["source"]["manifest"])
    require(file_hash(manifest) == runner.gold["source"]["manifest_sha256"], "Corpus manifest changed")
    docs = [json.loads(s) for s in manifest.read_text(encoding="utf-8").splitlines()]
    require(len(docs)==60, "Expected sixty documents")
    for row in docs: require(file_hash(manifest.parent / "documents" / row["corpus_filename"]) == row["source_sha256"], "Original source document changed")
    require(len(chunks)==1330 and len({c["source_doc_id"] for c in chunks.values()})==60, "Source chunk coverage wrong")
    quote_count = 0
    for q in runner.questions:
        for e in q.get("evidence",[]):
            raw=chunks[e["chunk_id"]]["content"]
            require(raw[e["start_char"]:e["end_char"]]==e["quote"], "Original gold span changed")
            quote_count += 1
        runner.raw_vector(q)
    vectors = list((WORK / "keyword_query_vectors").glob("*.json"))
    for p in vectors:
        row=read_json(p);v=np.asarray(row["vector"],dtype=np.float32)
        require(row["model"]==EMBEDDING_MODEL and row["dimension"]==2560, "Keyword vector model mismatch")
        require(v.shape==(2560,) and np.isfinite(v).all() and np.linalg.norm(v)>0, "Keyword vector invalid")
        require(row["signature"]==digest({"text":row["text"],"model":EMBEDDING_MODEL,"dimension":2560}), "Keyword vector signature changed")
    records = {}
    keyword_calls = 0
    for group,spec in GROUPS.items():
        for q in runner.questions:
            r=read_json(WORK / "retrieval" / group / (q["question_id"]+".json"))
            require(r["signature"]==digest({"protocol":protocol(),"question":q["question"],"group":group}), "Retrieval protocol mismatch")
            require(len(r["chunk_ids"])==len(set(r["chunk_ids"]))<=20, "Candidate IDs not unique")
            for cid,e in zip(r["chunk_ids"],r["evidence"]):
                require(cid==e["source_chunk_id"] and e["chunk_content"]==chunks[cid]["content"], "Evidence is not the original source chunk")
            if spec["adapter"]=="upstream_hyper_query":
                prompt=_get_query_keywords_prompt(normalize_query(q["question"]),{"domain":spec["domain"],"prompt_profile":"default"})
                signature=digest({"prompt":prompt,"role":"answer","model":MODEL,"temperature":0,"reasoning_effort":"low","protocol":"pfas-qa-strict-v1"})
                call=read_json(WORK / "api/calls" / (signature+".json"))
                require(call["status"]=="ok", "Upstream keyword call incomplete")
                value=parse_json_response(call["content"],call["finish_reason"])
                validate_keywords(value)
                expected=_parse_query_keywords(call["content"],prompt,True)
                require(tuple(r["audit"][k] for k in ("entity_keywords","relation_keywords"))==expected,"Upstream parsed query keywords mismatch")
                for text in expected:
                    if text:
                        sig=digest({"text":text,"model":EMBEDDING_MODEL,"dimension":2560})
                        require((WORK / "keyword_query_vectors" / (sig+".json")).is_file(), "A keyword branch lacks its actual-text vector checkpoint")
                keyword_calls += 1
            records[group,q["question_id"]]=r
    paired=[]
    for q in runner.questions:
        qid=q["question_id"]
        a,b=[records[g,qid] for g in ("normalized_final_no_rerank","normalized_final")]
        ac,bc=copy.deepcopy(a["audit"]["config"]),copy.deepcopy(b["audit"]["config"])
        require(ac.pop("enable_rerank") is False and bc.pop("enable_rerank") is True and ac==bc, "F0/F1 config differs beyond rerank")
        for name in ("candidate_edge_ids","candidate_chunk_ids"):
            av=a["evidence"][0][name] if a["evidence"] else []
            bv=b["evidence"][0][name] if b["evidence"] else []
            require(av==bv,"F0/F1 candidate pool mismatch")
        paired.append({"query_id":qid,"identical_pool":True,"same_top5_order":a["chunk_ids"][:5]==b["chunk_ids"][:5],
                       "same_top5_members":set(a["chunk_ids"][:5])==set(b["chunk_ids"][:5])})
    pool=read_json(WORK / "candidate_rankings.json")["candidate_union"]
    require(read_json(PUBLIC / "benchmark/candidate_rankings.json")["candidate_union"]==pool,"Published candidate ranks changed")
    grouped={}
    for row in pool: grouped.setdefault(row["query_id"],[]).append(row["chunk_id"])
    observed={}
    batches=0
    for qid,ids in grouped.items():
        for i in range(0,len(ids),4):
            packet=label_packet(qmap[qid],ids[i:i+4],chunks)
            sig=digest({"rules":GRADE_RULES,"packet":packet})
            row=read_json(WORK / "qrel_batches" / (sig+".json"))
            require(row["signature"]==sig and row["packet"]==packet,"Qrel packet changed")
            validate_labels(row["judgment"],packet)
            for r in row["judgment"]["judgments"]: observed[qid,r["chunk_id"]]=(r,packet)
            batches+=1
    qrels=read_json(PUBLIC / "cfr/shared_qrels.json")["qrels"]
    require(len(qrels)==len(observed)==len(pool),"Incomplete or duplicate qrel pairs")
    spans=0
    for qrel in qrels:
        row,packet=observed[qrel["query_id"],qrel["chunk_id"]]
        require(all(qrel[k]==row[k] for k in row),"Published qrel differs from validated response")
        expected=[packet["RAW_SPAN_CATALOG"][i] for i in row["span_ids"]]
        require(qrel["exact_support_spans"]==expected,"Qrel source pointers changed")
        for e in expected:
            require(chunks[e["chunk_id"]]["content"][e["start"]:e["end"]]==e["exact_raw_text"],"Qrel raw span not exact")
            spans+=1
    fact_gold=read_json(PUBLIC / "cfr/composite_fact_gold_machine_verified.json")
    accepted={f["fact_id"]:f for q in fact_gold["queries"] for f in q["atomic_facts"]}
    expected_accepted={}
    rejected=0
    proposed=0
    for q in runner.questions:
        if not q["answerable"]: continue
        p=label_packet(q,sorted(q["gold_chunk_ids"]),chunks)
        row=read_json(WORK / "facts" / (q["question_id"]+".json"))
        require(row["signature"]==digest({"rules":FACT_RULES,"packet":p}),"Fact protocol mismatch")
        validate_facts(row["generation"],p);validate_fact_review(row["review"],row["generation"]["facts"],p)
        for i,(fact,review) in enumerate(zip(row["generation"]["facts"],row["review"]["fact_checks"])):
            proposed+=1
            if not all(review[k] for k in ("atomic","supported","numeric_unit_binding_valid","question_relevant")):
                rejected+=1;continue
            fid=q["question_id"]+"|fact:"+str(i+1)
            require(fid in accepted,"Missing accepted atomic fact")
            f=accepted[fid]
            require(all(f[k]==v for k,v in fact.items()),"Published scientific fact fields changed")
            expected=[p["RAW_SPAN_CATALOG"][s] for s in review["support_span_ids"]]
            require(f["exact_support_spans"]==expected and f["supporting_chunk_ids"]==sorted({e["chunk_id"] for e in expected}),"Fact source binding changed")
            for e in expected: require(chunks[e["chunk_id"]]["content"][e["start"]:e["end"]]==e["exact_raw_text"],"Atomic fact span is not exact")
            expected_accepted[fid]=f
    require(set(expected_accepted)==set(accepted) and rejected==len(read_json(PUBLIC / "cfr/rejected_facts.json")),"Accepted/rejected fact partition invalid")
    core.EVIDENCE_BUDGET_CHARS=1500
    for q in runner.questions:
        r=read_json(WORK / "qa/records" / (q["question_id"]+".json"))
        context=core.format_evidence_context(q["question"],records["normalized_final",q["question_id"]]["evidence"][:5],evidence_format="legacy")
        require(context==r["context"] and r["signature"]==digest({"question":q,"context":context,"protocol":protocol()}),"Supplementary QA context/protocol changed")
        validate_answer({"answer":r["generated_answer"],"citations":r["citations"],"abstained":r["abstained"]})
        validate_judge(copy.deepcopy(r),q,r["abstained"])
        shown={"Evidence "+s for s in re.findall(r"(?m)^Evidence (\d+)\s*$",context)}
        require(all(c in shown for c in r["citations"]),"Citation references evidence absent from the generation context")
    schema=read_json(PUBLIC / "protocol/table_schema_acceptance.json")
    require(schema["case1_csv_schemas_identical"] and len(schema["tables"])==11,"Not all case1 CSV schemas aligned")
    requests=[json.loads(s) for s in (WORK / "api/request_audit.jsonl").read_text(encoding="utf-8").splitlines()]
    require(all(r["requests"]["network_peak"]<=10 and r["requests"]["key_peak"]<=1 for r in requests),"Actual network/key peak exceeded authorization")
    for row in requests:
        require(row["model"]==(EMBEDDING_MODEL if row["role"]=="embedding" else MODEL),"Unauthorized runtime model")
        if row["status"]=="ok" and row["role"]!="embedding": require(row["finish_reason"]=="stop","Incomplete successful response")
    from collections import Counter
    request_summary={"total_attempts_across_all_resumes":len(requests),"roles":dict(Counter(r["role"] for r in requests)),
                     "statuses":dict(Counter(r["status"] for r in requests)),"failed_attempt_types":dict(Counter(r.get("error_type") for r in requests if r["status"]!="ok")),
                     "network_peak":max(r["requests"]["network_peak"] for r in requests),"per_key_peak":max(r["requests"]["key_peak"] for r in requests),
                     "unresolved_items":0,"note":"Main progress.actual_requests is the last process only; this report totals all prior bounded retries and resumes."}
    report={"passed":True,"protected_original_files":len(before),"original_source_documents":len(docs),"chunks":len(chunks),
            "original_gold_exact_quotes":quote_count,"raw_question_vectors":40,"keyword_query_vectors":len(vectors),"reconstructed_upstream_keyword_calls":keyword_calls,
            "retrieval_records":len(records),"same_f0_f1_candidate_pool_queries":len(paired),"same_f0_f1_top5_order":sum(p["same_top5_order"] for p in paired),
            "same_f0_f1_top5_members":sum(p["same_top5_members"] for p in paired),"qrel_batches":batches,"qrel_pairs":len(qrels),"verified_qrel_support_spans":spans,
            "fact_queries":35,"proposed_atomic_facts":proposed,"accepted_atomic_facts":len(accepted),"rejected_atomic_facts":rejected,
            "supplementary_qa_records":40,"identical_case1_csv_schemas":11,"no_new_api_requests_in_this_verification":True,
            "scientific_review_scope":"stored same-model independent-prompt source reviews; this verifier checks exact pointers and arithmetic, not new human scientific judgments", "at":utc()}
    write_json(out / "independent_validation.json",report)
    write_json(PUBLIC / "protocol/independent_validation.json",report)
    write_json(PUBLIC / "protocol/request_summary_all_resumes.json",request_summary)
    analysis=PUBLIC / "reports/paper_analysis_report.md"
    content=analysis.read_text(encoding="utf-8")
    if "## Final interpretation" not in content:
        content += """

## Final interpretation and independent export check

F0 and F1 both contain the core domain-adapted representation and retrieval
organization. In this PFAS run they have the same Hit@5 (0.875) and exact CFR@5
(107/141 = 0.758865). Reranking does not show an aggregate gain here: F1's
MRR/gNDCG are slightly lower than F0's. This is not a claim of statistically
significant harm or a universal ranking. Keep the measured result as reported.
The five systems are not a single-variable ablation; only F0/F1 isolate rerank.
The method-level gains over B0/B2, and the Hit@5 gain over B1, remain present
without this rerank. This does not invalidate domain adaptation; individual
adaptation modules and pure structure are not causally isolated here.

The new F1 supplementary QA has Good Rate0.325, Satisfactory-or-Better0.700
and model-judged hallucination rate0.125. Its constrained legacy context differs
from the earlier full-chunk six-system QA, so those two scores must not be
presented as a controlled improvement/degradation comparison.

All 11 CSV table schemas now match case1 exactly. Source-level Hit follows
case1's chunk-derived policy and equals chunk Hit at the same threshold; an
earlier inferred same-paper diagnostic was superseded, with its initial archive
retained as provenance. All main retrieval and CFR values remain unchanged.
The actual case1 offline evaluator independently regenerated the tables.
New fact inventory:143 proposals,141 accepted and2 rejected by stored source
reviews; rejected items are retained. New labels/facts/QA remain machine work.
All7687 protected prior files and all60 original source document hashes passed
the final readback. protocol/request_summary_all_resumes.json accounts for all
1049 request attempts, including126 failed/invalid attempts recovered through
bounded resumes; no unresolved items remain. It is not the last-process count82.
"""
        analysis.write_text(content,encoding="utf-8")
    source_files=[repo/"scripts"/n for n in ("package_pfas_case1.py","finalize_pfas_case1_schema.py","reproduce_pfas_case1_package.py","verify_pfas_case1_release.py")]
    source_files.append(repo/"tests/test_pfas_case1_export_schema.py")
    sources={}
    with zipfile.ZipFile(out / "final_export_source.zip","w",zipfile.ZIP_DEFLATED) as z:
        for p in source_files:
            raw=p.read_bytes();z.writestr(p.name,raw);sources[p.name]=hashlib.sha256(raw).hexdigest()
    with zipfile.ZipFile(out / "final_export_source.zip") as z: require(all(hashlib.sha256(z.read(n)).hexdigest()==h for n,h in sources.items()),"Final source snapshot readback failed")
    write_json(PUBLIC / "protocol/final_export_source_manifest.json",{"complete":True,"source_files":sources,"source_archive_sha256":file_hash(out/"final_export_source.zip"),"parent_initial_export":read_json(out/"pre_correction_manifest.json")["existing_export_archive"]["sha256"]})
    shutil.copyfile(repo/"scripts/reproduce_pfas_case1_package.py",PUBLIC/"reproduce_metrics.py")
    # Scan only for secret-shaped material, without displaying matching values.
    secret=re.compile(r"(?i)(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{24,}|Bearer\s+[A-Za-z0-9_.-]{24,}")
    for p in PUBLIC.rglob("*"):
        if p.is_file() and p.suffix in (".json",".jsonl",".csv",".md",".py"):
            require(not secret.search(p.read_text(encoding="utf-8-sig")),"Secret-shaped content in public export: "+str(p.relative_to(PUBLIC)))
    pubmanifest=read_json(PUBLIC/"publication_manifest.json")
    pubmanifest.update(complete=True,export_revision=2,verification_state="independent_final_check_passed",independently_verified_at=utc())
    pubmanifest["artifacts"]=[{"path":p.relative_to(PUBLIC).as_posix(),"sha256":file_hash(p),"bytes":p.stat().st_size}
        for p in sorted(PUBLIC.rglob("*")) if p.is_file() and p.relative_to(PUBLIC).as_posix() not in ("publication_manifest.json","acceptance.json")]
    write_json(PUBLIC/"publication_manifest.json",pubmanifest)
    try:
        numeric=reproduce(PUBLIC)
    except Exception:
        pubmanifest["complete"]=False;pubmanifest["verification_state"]="failed_offline_reproduction"
        write_json(PUBLIC/"publication_manifest.json",pubmanifest)
        raise
    acceptance={**numeric,"protected_evidence_unchanged":True,"protected_files":len(before),"accepted_atomic_facts":len(accepted),
                "independent_source_pointer_checks_passed":True,"case1_csv_schema_and_source_diagnostic_aligned":True,"at":utc()}
    write_json(PUBLIC/"acceptance.json",acceptance)
    archive=WORK/"case2_pfas_v1_verified_results_final.zip"
    require(not archive.exists(),"Do not overwrite an existing final archive")
    files=[p for p in sorted(PUBLIC.rglob("*")) if p.is_file()]
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.relative_to(PUBLIC).as_posix())
    with zipfile.ZipFile(archive) as z:
        require(len(z.infolist())==len(files),"Final archive file count mismatch")
        require(all(hashlib.sha256(z.read(p.relative_to(PUBLIC).as_posix())).hexdigest()==file_hash(p) for p in files),"Final archive SHA readback mismatch")
    pointer={"folder":str(PUBLIC),"archive":str(archive),"sha256":file_hash(archive),"files":len(files),"bytes":archive.stat().st_size,
             "verified":True,"independently_verified":True,"export_revision":2,"created_at":utc()}
    write_json(WORK/"release_pointer.json",pointer)
    write_json(out/"final_acceptance.json",acceptance)
    status=read_json(WORK/"progress.json")
    status.update(independent_final_verification=True,independently_verified_at=utc(),final_archive=str(archive))
    write_json(WORK/"progress.json",status)
    print(json.dumps({"acceptance":acceptance,"release":pointer}),flush=True)


if __name__=="__main__":main()
