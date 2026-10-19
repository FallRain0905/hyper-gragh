"""Ground every PFAS40 scoring point, then audit it independently of generation."""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, digest, file_hash, read_json, utc, write_json


def validate_supported(value, chunks, allowed):
    if value.get("decision") not in ("ACCEPT", "REVISE"):
        raise ValueError("Question needs a supported revision")
    for field in ("question", "reference_answer", "rationale"):
        if not isinstance(value.get(field), str) or len(value[field].strip()) < 20:
            raise ValueError("Missing substantive " + field)
    points = value.get("point_support")
    if not isinstance(points, list) or not 2 <= len(points) <= 7:
        raise ValueError("Need 2–7 scoring points with support")
    if len({p.get("point") for p in points}) != len(points):
        raise ValueError("Duplicate rubric point")
    for p in points:
        if not isinstance(p.get("point"), str) or len(p["point"].strip()) < 12:
            raise ValueError("Scoring point too vague")
        ev = p.get("evidence")
        if not isinstance(ev, list) or not ev:
            raise ValueError("Every point needs source evidence")
        for e in ev:
            cid, quote = e.get("chunk_id"), e.get("quote")
            if cid not in allowed or cid not in chunks:
                raise ValueError("Evidence outside supplied raw chunks")
            if not isinstance(quote, str) or len(quote.strip()) < 35 or quote not in chunks[cid]["content"]:
                raise ValueError("Evidence quote is not a substantive exact raw-source span")
    if value.get("answerable") is not True:
        raise ValueError("Supported item must be answerable")
    if not isinstance(value.get("unsupported_claims"), list):
        raise ValueError("Missing unsupported-claim guardrails")


def source_packet(item, chunks):
    doc_ids = set(item["expected_doc_ids"])
    candidates = {k: v for k, v in chunks.items() if v.get("source_doc_id") in doc_ids}
    terms = {t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9-]+", item["question"] + " " + item["reference_answer"])
             if len(t) > 3}
    scored = []
    for cid, row in candidates.items():
        text = row["content"]
        # The generation packet is not used by evaluated retrieval systems.
        score = sum(min(text.lower().count(t), 4) for t in terms)
        if cid in item["gold_chunk_ids"]:
            score += 25
        # Bibliographies should not win by merely repeating a paper title.
        if re.search(r"(?:^|\n)\s*#?\s*(?:References|REFERENCES)\s*(?:\n|$)", text):
            score -= 20
        scored.append((score, cid))
    ids = [cid for _, cid in sorted(scored, key=lambda x: (-x[0], x[1]))[:5]]
    # Preserve immediate adjacent context for chunk-boundary sentences.
    for cid in item["gold_chunk_ids"]:
        number = int(cid.rsplit("_", 1)[1])
        for n in (number - 1, number + 1):
            adjacent = cid.rsplit("_", 1)[0] + f"_{n:03d}"
            if adjacent in candidates and adjacent not in ids:
                ids.append(adjacent)
    return {cid: chunks[cid] for cid in sorted(ids)}


def make_prompt(item, packet):
    return """Create an auditable literature QA reference and rubric from the raw source chunks below.
The draft is fallible. Check every material, target PFAS, numeric value/unit, time,
condition and mechanism. Do not repeat source OCR/name errors as established facts.
Revise the question if its original reference is not fully supported. Preserve its
scientific focus. Do not merge unrelated studies or invent combined conditions.
Removal, parent degradation, fluoride release/defluorination, and carbon mineralization
are distinct. Fluoride release alone does not establish complete carbon mineralization.
Adsorption or coagulation is not evidence of chemical destruction. Mechanistic proposals
and review statements must remain qualified as reported/proposed, not proven universally.
No external knowledge; no graph fields. The question must stand alone without chunk IDs.
Use English. Keep it one coherent question with at most two connected requests.
Create 2–7 substantive required scoring points. Each point needs one or more EXACT
contiguous quotes copied from a supplied chunk, preserving all newlines/LaTeX/OCR.
Do not cite bibliography entries as primary experimental results.
When OCR is ambiguous, omit the affected quantitative claim and ask a supported question.

Return strict JSON:
{"decision":"ACCEPT or REVISE", "answerable":true, "question":"...",
 "reference_answer":"...", "point_support":[{"point":"...",
 "evidence":[{"chunk_id":"PFAS_...", "quote":"exact span"}]}],
 "unsupported_claims":["specific prohibited extrapolation"],
 "fact_arity":4, "support_mode":"single_study or multi_study", "rationale":"..."}

DRAFT:\n""" + json.dumps(item, ensure_ascii=False) + "\nRAW SOURCE CHUNKS:\n" + json.dumps(
        [{"chunk_id": cid, "doc_id": r["source_doc_id"], "content": r["content"]} for cid, r in packet.items()], ensure_ascii=False)


def independent_prompt(question, chunks):
    ids = sorted({e["chunk_id"] for p in question["point_support"] for e in p["evidence"]})
    return """Independently audit the QA reference below against complete raw source chunks.
Do not assume previous reviewer correctness. Check question answerability, all reference
claims, every rubric point and exact claim-to-quote binding. Reject wrong material/PFAS,
condition stitching, denominator swaps, metric conflation, numerical/OCR ambiguity,
or mechanistic certainty beyond the original study. Do not require external facts.
Important: fluoride release does not by itself prove complete carbon mineralization;
removal by adsorption/coagulation is not chemical destruction. Citation support must
come from raw body text, not bibliography. Report all unsupported or ambiguous claims.
Return strict JSON {"accepted":true, "point_checks":[{"point":"copy rubric exactly",
"supported":true,"reason":"specific explanation"}], "reference_supported":true,
"question_answerable":true,"numeric_unit_binding_valid":true,"issues":[],"rationale":"..."}.

QUESTION AND REFERENCE:\n""" + json.dumps(question, ensure_ascii=False) + "\nRAW CHUNKS:\n" + json.dumps(
        [{"chunk_id": cid, "content": chunks[cid]["content"]} for cid in ids], ensure_ascii=False)


def validate_audit(value, points):
    checks = value.get("point_checks")
    if not isinstance(checks, list) or [p.get("point") for p in checks] != points:
        raise ValueError("Independent audit must check every scoring point in order")
    for p in checks:
        if type(p.get("supported")) is not bool or not p.get("reason"):
            raise ValueError("Incomplete point judgment")
    for field in ("accepted", "reference_supported", "question_answerable", "numeric_unit_binding_valid"):
        if type(value.get(field)) is not bool:
            raise ValueError("Missing audit Boolean " + field)
    if not isinstance(value.get("issues"), list):
        raise ValueError("Missing audit issues")
    if value["accepted"] and (not all(p["supported"] for p in checks)
                              or not all(value[f] for f in ("reference_supported", "question_answerable", "numeric_unit_binding_valid"))
                              or value["issues"]):
        raise ValueError("Inconsistent acceptance")


async def run(args):
    draft = read_json(args.output / "qa_questions.json")
    chunks = read_json(draft["source"]["chunks"])
    if file_hash(draft["source"]["chunks"]) != draft["source"]["chunks_sha256"]:
        raise ValueError("Frozen raw source changed")
    client = QAClient(args.output)
    lock = asyncio.Lock()
    semaphore = asyncio.Semaphore(10)
    status = {"stage": "supported_reference_verification", "started_at": utc(), "supported_done": 0,
              "supported_total": 35, "errors": [], "negative_done": 0, "complete": False}
    write_json(args.output / "progress.json", status)

    async def one(item):
        async with semaphore:
            qid = item["question_id"]
            packet = source_packet(item, chunks)
            signature = digest({"draft": item, "packet": packet, "version": 1})
            path = args.output / "verified" / (qid + ".json")
            if path.exists():
                row = read_json(path)
                if row.get("input_signature") != signature:
                    raise ValueError("Verified checkpoint has a different source/draft")
                if row.get("audit", {}).get("accepted"):
                    return row
            prompt = make_prompt(item, packet)
            for revision in range(3):
                value = await client.json(prompt, validator=lambda v: validate_supported(v, chunks, packet), label=qid + ":reference")
                points = [p["point"] for p in value["point_support"]]
                audit = await client.json(independent_prompt(value, chunks), role="judge",
                                          validator=lambda v: validate_audit(v, points), label=qid + ":independent_audit")
                write_json(args.output / "reviews" / f"{qid}.revision{revision}.json", {"reference": value, "audit": audit})
                if audit["accepted"]:
                    evidence = []
                    for p in value["point_support"]:
                        for e in p["evidence"]:
                            ev = {**e, "doc_id": chunks[e["chunk_id"]]["source_doc_id"],
                                  "source_file": chunks[e["chunk_id"]]["source_file"],
                                  "start_char": chunks[e["chunk_id"]]["content"].index(e["quote"]),
                                  "quote_sha256": digest(e["quote"]),
                                  "chunk_content_sha256": digest(chunks[e["chunk_id"]]["content"])}
                            ev["end_char"] = ev["start_char"] + len(ev["quote"])
                            if ev not in evidence:
                                evidence.append(ev)
                    row = {**item, **value, "input_signature": signature, "audit": audit,
                           "required_key_points": points, "evidence": evidence,
                           "gold_chunk_ids": sorted({e["chunk_id"] for e in evidence}),
                           "source_doc_ids": sorted({e["doc_id"] for e in evidence}),
                           "review_status": "machine_verified", "human_confirmed": False}
                    write_json(path, row)
                    return row
                prompt = make_prompt(item, packet) + "\nPREVIOUS FAILED REFERENCE AND AUDIT (revise every issue):\n" + json.dumps({"reference": value, "audit": audit}, ensure_ascii=False)
            raise ValueError("Independent reference audit rejected after bounded revision")

    async def tracked(item):
        try:
            row = await one(item)
            async with lock:
                status["supported_done"] += 1
                status["actual_requests"] = client_snapshot()
                write_json(args.output / "progress.json", status)
                print(json.dumps({"verified": row["question_id"], "supported_done": status["supported_done"], "points": len(row["required_key_points"])}), flush=True)
            return row
        except Exception as e:
            async with lock:
                status["errors"].append({"question_id": item["question_id"], "error_type": type(e).__name__,
                                         "validation_error": str(e)[:350] if isinstance(e, ValueError) else None})
                write_json(args.output / "progress.json", status)
                print(json.dumps({"failed": item["question_id"], "error_type": type(e).__name__}), flush=True)
            return None

    def client_snapshot():
        from runtime_requests import QA_REQUEST_LIMITER
        return QA_REQUEST_LIMITER.snapshot()

    try:
        results = await asyncio.gather(*(tracked(q) for q in draft["qa_questions"] if q["answerable"]))
        status["stage"] = "supported_verified_negative_review_pending" if all(results) else "supported_review_failed"
        status["finished_at"] = utc()
        status["actual_requests"] = client_snapshot()
        write_json(args.output / "progress.json", status)
    finally:
        await client.close()
    print(json.dumps(status), flush=True)
    return 0 if all(results) else 2


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args)))


if __name__ == "__main__":
    main()
