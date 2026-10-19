"""Audit the five PFAS40 negative items against all 60 complete documents."""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, digest, file_hash, read_json, utc, write_json
from scripts.verify_pfas_qa40 import validate_supported, validate_audit


def validate(value, questions, packet):
    rows = value.get("judgments")
    if not isinstance(rows, list) or [r.get("question_id") for r in rows] != [q["question_id"] for q in questions]:
        raise ValueError("Check all five questions in order")
    for r in rows:
        if r.get("status") not in ("not_reported", "supported", "ambiguous") or not r.get("reason"):
            raise ValueError("Missing substantive absence judgment")
        if r["status"] in ("supported", "ambiguous"):
            if not r.get("evidence"):
                raise ValueError("Potential support needs exact evidence")
            for e in r["evidence"]:
                if e.get("chunk_id") not in packet or not isinstance(e.get("quote"), str) or e["quote"] not in packet[e["chunk_id"]]["content"]:
                    raise ValueError("Candidate support is not exact source evidence")


async def run(output):
    draft = read_json(output / "qa_questions.json")
    chunks = read_json(draft["source"]["chunks"])
    if file_hash(draft["source"]["chunks"]) != draft["source"]["chunks_sha256"]:
        raise ValueError("Frozen sources changed")
    questions = [q for q in draft["qa_questions"] if not q["answerable"]]
    docs = sorted({r["source_doc_id"] for r in chunks.values()})
    if len(docs) != 60:
        raise ValueError("Absence audit requires all 60 corpus documents")
    client = QAClient(output)
    semaphore = asyncio.Semaphore(10)
    status = {"stage": "negative_full_corpus_audit", "started_at": utc(), "documents_done": 0,
              "documents_total": 60, "question_count": 5, "errors": [], "complete": False}
    lock = asyncio.Lock()

    async def one(doc):
        async with semaphore:
            packet = {k: v for k, v in sorted(chunks.items()) if v["source_doc_id"] == doc}
            signature = digest({"questions": questions, "document": packet, "protocol": "full-document-absence-v1"})
            path = output / "absence_audits" / (doc + ".json")
            if path.exists():
                value = read_json(path)
                if value.get("input_signature") != signature:
                    raise ValueError("Absence checkpoint source mismatch")
                validate(value, questions, packet)
                return value
            prompt = """Audit whether each question is answerable from the COMPLETE raw document below.
The proposed unanswerable labels may be wrong. Search carefully for the exact requested
material, PFAS, metric, value, unit and combined experimental conditions, including tables,
conclusions and citations. A nearby value under different conditions is insufficient.
Do not invent a corpus-level statistical test or an optimum never demonstrated.
Do not infer absence from a missing keyword: examine all supplied chunks.
Use status supported if the precise requested relation/value is actually reported;
ambiguous if OCR or indirect statements might support it; not_reported only if absent.
For supported/ambiguous, provide exact contiguous source quotes and a chunk ID. Preserve
newlines/LaTeX. For not_reported explain the specific missing relation, not merely 'no'.
Return JSON {"judgments":[{"question_id":"copy", "status":"not_reported or supported or ambiguous",
"reason":"...", "evidence":[{"chunk_id":"...","quote":"..."}]}]}.
Check all five questions in the supplied order.
QUESTIONS:\n""" + json.dumps([{"question_id": q["question_id"], "question": q["question"]} for q in questions], ensure_ascii=False) + "\nCOMPLETE RAW DOCUMENT:\n" + json.dumps(
                [{"chunk_id": k, "content": v["content"]} for k, v in packet.items()], ensure_ascii=False)
            value = await client.json(prompt, role="judge", validator=lambda v: validate(v, questions, packet), label=doc + ":absence")
            value.update(input_signature=signature, document_id=doc, chunk_ids=list(packet), checked_at=utc())
            write_json(path, value)
            return value

    async def tracked(doc):
        try:
            value = await one(doc)
            async with lock:
                status["documents_done"] += 1
                status["updated_at"] = utc()
                write_json(output / "negative_progress.json", status)
                print(json.dumps({"audited_document": doc, "documents_done": status["documents_done"]}), flush=True)
            return value
        except Exception as e:
            async with lock:
                status["errors"].append({"doc_id": doc, "error_type": type(e).__name__})
                write_json(output / "negative_progress.json", status)
                print(json.dumps({"failed_document": doc, "error_type": type(e).__name__}), flush=True)
            return None

    try:
        results = await asyncio.gather(*(tracked(d) for d in docs))
        status["complete"] = all(results)
        potential = [{"doc_id": r["document_id"], **j} for r in results if r
                     for j in r["judgments"] if j["status"] != "not_reported"]
        status.update(finished_at=utc(), potential_support=potential)
        write_json(output / "negative_progress.json", status)
        if not all(results) or potential:
            return 2
        supported = []
        for item in draft["qa_questions"]:
            if not item["answerable"]:
                continue
            path = output / "verified" / (item["question_id"] + ".json")
            row = read_json(path)
            validate_supported(row, chunks, chunks)
            validate_audit(row["audit"], row["required_key_points"])
            if not row["audit"]["accepted"]:
                raise ValueError("Supported review not accepted")
            supported.append(row)
        negatives = []
        for q in questions:
            q = {**q, "required_key_points": ["State that the requested exact result is not available in the supplied corpus.",
                                               "Do not invent a numeric value, optimum, condition combination or statistical conclusion."],
                 "unsupported_claims": ["An exact experimental or statistical result for this question."],
                 "review_status": "machine_full_corpus_absence_verified", "human_confirmed": False,
                 "support_mode": "unanswerable", "fact_arity": None,
                 "full_corpus_absence_audit": {"documents": docs, "chunks": 1330, "audits_sha256": digest(results)}}
            negatives.append(q)
        payload = {**draft, "status": "machine_verified_gold", "human_confirmed": False,
                   "review_provenance": {"reference_model": "deepseek-ai/DeepSeek-V4-Flash",
                                         "independent_review": "separate prompts using same model; not independent human review",
                                         "negative_scope": "60 complete raw documents; all 1330 chunks", "finished_at": utc()},
                   "qa_questions": sorted(supported + negatives, key=lambda q: q["question_id"])}
        write_json(output / "qa_gold.json", payload)
        docs_covered = sorted({d for q in supported for d in q["source_doc_ids"]})
        freeze = {"question_count": 40, "answerable": 35, "unanswerable": 5,
                  "gold_sha256": file_hash(output / "qa_gold.json"),
                  "raw_source_sha256": file_hash(draft["source"]["chunks"]),
                  "supported_source_documents": docs_covered, "supported_document_count": len(docs_covered),
                  "absence_audited_documents": 60, "human_confirmed": False, "frozen_at": utc()}
        write_json(output / "freeze_manifest.json", freeze)
        lines = ["# PFAS40 reference and evidence review", "", "Status: machine verified; no human confirmation is claimed.",
                 "35 supported items and 5 negatives audited against all 60 documents. Supported-document coverage: " + str(len(docs_covered)) + ".", ""]
        for q in payload["qa_questions"]:
            lines += ["## " + q["question_id"], "", q["question"], "", "Reference: " + q["reference_answer"], "", "Scoring points:", ""]
            lines += ["- " + p for p in q["required_key_points"]]
            for e in q.get("evidence", []):
                lines += ["", e["chunk_id"] + " — " + e["doc_id"], "", "> " + e["quote"].replace("\n", "\n> ")]
            lines += [""]
        (output / "qa_gold_review.md").write_text("\n".join(lines), encoding="utf-8")
        status.update(stage="gold_frozen", gold_sha256=freeze["gold_sha256"])
        write_json(output / "negative_progress.json", status)
        print(json.dumps(freeze), flush=True)
        return 0
    finally:
        await client.close()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args.output)))


if __name__ == "__main__":
    main()
