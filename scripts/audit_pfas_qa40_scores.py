"""Audit all frozen QA scores uniformly, with exact answer-span attribution.

The first review is blind to the system and original score. Changed labels,
coverage or grounding get a further source-based adjudication. Original records
are never overwritten. All reviewers remain LLM-based, not human confirmation.
"""
from __future__ import annotations

import argparse
import asyncio
import copy
import difflib
import hashlib
import json
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, digest, file_hash, read_json, utc, write_json
from scripts.run_pfas_qa40 import GROUPS, request_stats
from scripts import run_qa_formal_llm as formal


RULES = """Audit this chemical-literature QA answer point by point.
You are blind to the retrieval system. Do not infer which system is better.
Do not treat a missing detail as a false statement or hallucination.
Paraphrase, equivalent units, recognized chemical notation and properly qualified
mechanistic proposals are allowed. Read the ACTUAL answer before asserting a phrase
is missing. In particular distinguish incomplete coverage from incorrect claims.
Evaluate rubric coverage against answer text. A covered point must identify an exact
contiguous answer_quote copied from the answer (not the source or rubric).
Check grounding separately against RAW RETRIEVED CHUNKS. The gold source quotes only
clarify the rubric: they are not evidence that the answer generator retrieved.
Do not call a source-supported summary false just because it omits intermediate steps.
Do flag wrong PFAS/material/condition/value/unit/denominator and claims absent from raw
retrieved evidence. Removal, parent degradation, fluoride release, defluorination and
carbon mineralization are distinct; adsorption/coagulation is not destruction.
When the answer explicitly abstains without factual claims, it is not hallucinated.
For supported questions, abstention is POOR. For unanswerable questions, an accurate
abstention with no invented result covers the negative rubric and can be GOOD.
GOOD requires all points covered and no hallucination. SATISFACTORY means a correct,
grounded core answer that misses some details. POOR means wrong core, false abstention,
or hallucination. Missing several details alone does not prove hallucination.
Every material factual claim must appear in claim_checks, including incidental numbers.
For each supported factual claim, supply an exact RAW source_quote and its evidence_rank.
Only quote evidence actually in the raw retrieved chunks. Reference quotes are separate.
Use empty source_quote/evidence_ranks for unsupported claims. Copy claims from answer.
Citation support measures claims actually supported by their cited retrieved blocks,
not just valid citation labels. Do not penalize uncited abstention as a hallucination.
Return exactly one JSON object with this schema:
{
 "point_checks":[{"point_id":0,"covered":true,"answer_quote":"exact answer span",
                   "reason":"specific rationale"}],
 "claim_checks":[{"answer_quote":"exact answer span","supported":true,
                   "evidence_rank":1,"source_quote":"exact raw source span",
                   "reason":"why the source supports this claim"}],
 "hallucinated":false,"unsupported_claims_found":[],
 "quality_label":"GOOD or SATISFACTORY or POOR",
 "citation_support_score":0.0,"rationale":"specific overall reason"
}
point_checks must have every point_id in the supplied order. For uncovered points
answer_quote may be empty. If the answer has no material factual claims use [] for
claim_checks. Do not silently ignore an uncertain factual claim; explain the issue.
"""


def packet(qa, record, retrieval, chunks):
    raw = []
    for rank, row in enumerate(retrieval["evidence"], 1):
        cid = row.get("source_chunk_id") or row["id"]
        if cid not in chunks:
            raise ValueError("Retrieved source ID missing")
        raw.append({"rank": rank, "chunk_id": cid, "content": chunks[cid]["content"]})
    return {"question": qa["question"], "answerable": qa["answerable"],
            "rubric": [{"point_id": i, "point": p} for i, p in enumerate(qa["required_key_points"])],
            "reference_answer": qa["reference_answer"],
            "reference_source_quotes_NOT_retrieved_evidence": [
                {"chunk_id": e["chunk_id"], "quote": e["quote"]} for e in qa.get("evidence", [])],
            "actual_answer": record["generated_answer"], "answer_citations": record["citations"],
            "answer_abstained": record["abstained"], "raw_retrieved_chunks": raw}


def validate(value, data):
    points = value.get("point_checks")
    if not isinstance(points, list) or any(type(p.get("point_id")) is not int for p in points) or [p.get("point_id") for p in points] != list(range(len(data["rubric"]))):
        raise ValueError("Review must check every point_id in order")
    answer = data["actual_answer"]
    for p in points:
        if type(p.get("covered")) is not bool or not isinstance(p.get("answer_quote"), str) or not p.get("reason"):
            raise ValueError("Incomplete scoring-point review")
        if p["covered"] and (not p["answer_quote"].strip() or p["answer_quote"] not in answer):
            raise ValueError("Covered point must cite an exact answer span")
    claims = value.get("claim_checks")
    if not isinstance(claims, list):
        raise ValueError("Missing claim grounding review")
    if not data["answer_abstained"] and not claims:
        raise ValueError("A substantive answer needs material claim checks")
    sources = {r["rank"]: r["content"] for r in data["raw_retrieved_chunks"]}
    for c in claims:
        quote = c.get("answer_quote")
        if not isinstance(quote, str) or not quote.strip() or quote not in answer or type(c.get("supported")) is not bool or not c.get("reason"):
            raise ValueError("Claim must quote the actual answer and give a grounding judgment")
        if c["supported"]:
            rank = c.get("evidence_rank")
            source = c.get("source_quote")
            if type(rank) is not int or rank not in sources or not isinstance(source, str) or len(source.strip()) < 15 or source not in sources[rank]:
                raise ValueError("Supported claim must cite an exact raw retrieved span and rank")
    if type(value.get("hallucinated")) is not bool or not isinstance(value.get("unsupported_claims_found"), list):
        raise ValueError("Grounding summary missing")
    if any(not c["supported"] for c in claims) and not value["hallucinated"]:
        raise ValueError("Unsupported material claim must be reflected in hallucination flag")
    if value["hallucinated"] and all(c["supported"] for c in claims):
        raise ValueError("Hallucination flag needs an identified unsupported answer claim")
    if value["hallucinated"] and not value["unsupported_claims_found"]:
        raise ValueError("Hallucination flag needs concrete unsupported claims")
    if not value["hallucinated"] and value["unsupported_claims_found"]:
        raise ValueError("Conflicting grounding summary")
    label = value.get("quality_label")
    if label not in ("GOOD", "SATISFACTORY", "POOR") or not value.get("rationale"):
        raise ValueError("Invalid quality label or missing rationale")
    if label == "GOOD" and not all(p["covered"] for p in points):
        raise ValueError("GOOD requires every rubric point")
    if value["hallucinated"] and label != "POOR":
        raise ValueError("Hallucinated answers must be POOR")
    if data["answerable"] and data["answer_abstained"] and label != "POOR":
        raise ValueError("Supported-item abstention must be POOR")
    score = value.get("citation_support_score")
    if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 1:
        raise ValueError("Citation support score must be in [0,1]")


def exact_whitespace_span(quote, text):
    """Recover only a unique contiguous span with identical non-space characters.

    Do not change punctuation, case, numbers, units, source rank or semantics.
    The returned quote is copied from the raw input, with offsets as proof.
    """
    if not isinstance(quote, str) or not isinstance(text, str) or not quote.strip():
        return None
    if quote in text:
        start = text.find(quote)
        return quote, start, start + len(quote)
    positions = [i for i, c in enumerate(text) if not c.isspace()]
    compact_text = "".join(text[i] for i in positions)
    compact_quote = "".join(c for c in quote if not c.isspace())
    if not compact_quote:
        return None
    start = compact_text.find(compact_quote)
    if start < 0 or compact_text.find(compact_quote, start + 1) >= 0:
        return None
    raw_start, raw_end = positions[start], positions[start + len(compact_quote) - 1] + 1
    return text[raw_start:raw_end], raw_start, raw_end


def restore_exact_quotes(value, data):
    restored = copy.deepcopy(value)
    proofs = []
    sources = {r["rank"]: r["content"] for r in data["raw_retrieved_chunks"]}
    for collection in ("point_checks", "claim_checks"):
        for i, row in enumerate(restored.get(collection, [])):
            if not isinstance(row, dict):
                continue
            fields = [("answer_quote", data["actual_answer"], "actual_answer")]
            if collection == "claim_checks" and row.get("supported") is True:
                rank = row.get("evidence_rank")
                if type(rank) is int and rank in sources:
                    fields.append(("source_quote", sources[rank], f"retrieved_rank_{rank}"))
            for field, raw, source in fields:
                quote = row.get(field)
                if isinstance(quote, str) and quote not in raw:
                    match = exact_whitespace_span(quote, raw)
                    if match:
                        row[field] = match[0]
                        proofs.append({"collection": collection, "index": i, "field": field,
                                       "original_model_quote": quote, "exact_quote": match[0],
                                       "source": source, "start": match[1], "end": match[2],
                                       "method": "unique_identical_non_whitespace_characters"})
    if proofs:
        restored["quote_format_recovery"] = proofs
    return restored


def source_span_catalog(data):
    """Offer exact raw ranges; IDs encode the content, rank and offsets."""
    catalog = {}
    for row in data["raw_retrieved_chunks"]:
        raw, rank = row["content"], row["rank"]
        ranges = [(0, len(raw))]
        start = 0
        for paragraph in raw.split("\n\n"):
            end = start + len(paragraph)
            if len(paragraph.strip()) >= 15:
                ranges.append((start, end))
            start = end + 2
        for start, end in dict.fromkeys(ranges):
            text = raw[start:end]
            span_id = f"R{rank}:{start}:{end}:" + digest(text)[:12]
            catalog[span_id] = {"rank": rank, "chunk_id": row.get("chunk_id"),
                                "start": start, "end": end, "exact_raw_text": text}
    return catalog


def resolve_explicit_source_spans(value, data):
    """Resolve only a new, explicit model selection; never infer another rank.

    Existing non-exact quotes are not fixed by this function. A model must select
    an offered ID and leave source_quote empty, or copy that exact selected span.
    """
    restored = copy.deepcopy(value)
    catalog = source_span_catalog(data)
    proofs = []
    for i, claim in enumerate(restored.get("claim_checks", [])):
        if not isinstance(claim, dict) or not claim.get("source_span_id"):
            continue
        span_id = claim["source_span_id"]
        if not isinstance(span_id, str) or span_id not in catalog:
            raise ValueError("source_span_id must be explicitly selected from this packet's raw catalog")
        span = catalog[span_id]
        if claim.get("supported") is not True or type(claim.get("evidence_rank")) is not int or claim["evidence_rank"] != span["rank"]:
            raise ValueError("Selected raw span rank must match the explicit supported-claim rank")
        supplied = claim.get("source_quote")
        if not isinstance(supplied, str) or supplied not in ("", span["exact_raw_text"]):
            raise ValueError("With source_span_id, source_quote must be empty or exactly that raw span; no altered units or punctuation")
        claim["source_quote"] = span["exact_raw_text"]
        proofs.append({"claim_index": i, "source_span_id": span_id, **span,
                       "method": "explicit_model_selected_raw_span_id", "model_source_quote": supplied})
    if proofs:
        restored["explicit_source_selection"] = proofs
    return restored


def prepare_review(value, data):
    return restore_exact_quotes(resolve_explicit_source_spans(value, data), data)


def require_explicit_source_selections(value):
    for claim in value["claim_checks"]:
        if claim["supported"] and (not isinstance(claim.get("source_span_id"), str) or not claim["source_span_id"]):
            raise ValueError("Every supported claim in a NEW response must explicitly select an offered source_span_id; source_quote must be empty with that selection")


def quote_validation_feedback(value, data):
    """Supply raw context for a new LLM decision; never repair scientific text.

    These are candidate excerpts for inspection, not assertions of support.
    The unchanged validator still requires exact quotes and a complete judgment.
    """
    sources = {r["rank"]: r["content"] for r in data["raw_retrieved_chunks"]}
    problems = []
    for i, claim in enumerate(value.get("claim_checks", [])):
        if not isinstance(claim, dict) or claim.get("supported") is not True:
            continue
        rank, quote = claim.get("evidence_rank"), claim.get("source_quote")
        if type(rank) is int and isinstance(quote, str) and quote in sources.get(rank, "") and len(quote.strip()) >= 15:
            continue
        problem = {"claim_index": i, "selected_rank": rank, "rejected_model_quote": quote,
                   "raw_context_candidates_NOT_support_decisions": []}
        if isinstance(quote, str) and quote:
            for raw_rank, raw in sources.items():
                if quote in raw:
                    problem["raw_context_candidates_NOT_support_decisions"].append({"rank": raw_rank, "exact_raw_quote": quote})
            if type(rank) is int and rank in sources:
                raw = sources[rank]
                match = difflib.SequenceMatcher(None, quote, raw).find_longest_match(0, len(quote), 0, len(raw))
                if match.size >= 15:
                    start, end = max(0, match.b - 350), min(len(raw), match.b + match.size + 350)
                    problem["raw_context_candidates_NOT_support_decisions"].append(
                        {"rank": rank, "start": start, "end": end, "exact_raw_context": raw[start:end]})
        problems.append(problem)
    return ("Return the complete JSON with every required field. Copy exact text including OCR, LaTeX, parentheses and units. "
            "Do not silently correct raw source text. Choose a contiguous raw span yourself, explain any interpretation in reason, "
            "and independently decide whether it supports the actual answer. Candidate context is not proof. "
            "If support is absent, mark the material claim unsupported. Never import reference quotes as retrieved evidence. "
            "An abstention with no material factual claims may use empty claim_checks; missing detail is not hallucination.\n"
            + "For this NEW response, every supported claim MUST explicitly select an offered source_span_id. "
            "Set source_quote to an empty string and evidence_rank to the selected span's rank; the exact raw range will be copied mechanically. "
            "An ID does not establish support: independently compare the actual claim and chosen raw text, and explain the judgment. "
            "Do not use an ID for an unsupported claim. Every other required JSON field and all scoring rules remain mandatory.\n"
            + json.dumps({"answer_abstained": data["answer_abstained"], "actual_answer": data["actual_answer"],
                          "quote_problems": problems, "offered_raw_source_spans": source_span_catalog(data)}, ensure_ascii=False))


def review_fields(review, qa):
    covered = [qa["required_key_points"][p["point_id"]] for p in review["point_checks"] if p["covered"]]
    missing = [p for p in qa["required_key_points"] if p not in covered]
    label = review["quality_label"]
    return {"quality_label": label, "good": label == "GOOD", "satisfactory_or_better": label in ("GOOD", "SATISFACTORY"),
            "covered_key_points": covered, "missing_key_points": missing,
            "key_point_coverage": len(covered) / len(qa["required_key_points"]),
            "hallucinated": review["hallucinated"], "unsupported_claims_found": review["unsupported_claims_found"],
            "citation_support_score": review["citation_support_score"], "rationale": review["rationale"]}


def differs(record, review, qa):
    fields = review_fields(review, qa)
    return (record["quality_label"] != fields["quality_label"] or record["hallucinated"] != fields["hallucinated"]
            or set(record["covered_key_points"]) != set(fields["covered_key_points"]))


async def run(args):
    original = args.evaluation
    summary = read_json(original / "summary.json")
    if not summary["status"]["complete"] or not summary["status"]["cache_files_unchanged"]:
        raise ValueError("Score audit requires completed read-only QA evaluation")
    gold = read_json(args.gold)
    if file_hash(args.gold) != summary["protocol"]["gold_sha256"]:
        raise ValueError("Gold freeze changed")
    questions = {q["question_id"]: q for q in gold["qa_questions"]}
    chunks = read_json(gold["source"]["chunks"])
    if file_hash(gold["source"]["chunks"]) != gold["source"]["chunks_sha256"]:
        raise ValueError("Frozen sources changed")
    paths = sorted((original / "records").rglob("*.json"))
    if len(paths) != 240:
        raise ValueError("Need all 240 records")
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    before = {p.relative_to(original).as_posix(): file_hash(p) for p in paths}
    protocol = {"version": "pfas-score-source-and-answer-span-audit-v1",
                "gold_sha256": file_hash(args.gold), "original_record_hashes": before,
                "blind_review": True, "disagreement_adjudication": True,
                "all_groups_same_rules": True, "rules_sha256": digest(RULES),
                "model": "deepseek-ai/DeepSeek-V4-Flash", "human_confirmed": False}
    protocol_file = output / "protocol.json"
    if protocol_file.exists() and read_json(protocol_file) != protocol:
        raise ValueError("Score audit protocol changed")
    write_json(protocol_file, protocol)
    client = QAClient(output)
    semaphore = asyncio.Semaphore(10)
    lock = asyncio.Lock()
    records = []
    status = {"stage": "blind_score_review_and_adjudication", "started_at": utc(), "completed": 0,
              "total": 240, "disagreements": 0, "errors": [], "complete": False}
    write_json(output / "progress.json", status)

    async def one(path):
        async with semaphore:
            record = read_json(path)
            group, qid = record["group"], record["question_id"]
            qa = questions[qid]
            retrieval = read_json(original / "retrieval" / group / (qid + ".json"))
            data = packet(qa, record, retrieval, chunks)
            signature = digest({"data": data, "original_record": file_hash(path), "protocol": protocol["version"]})
            checkpoint = output / "reviews" / group / (qid + ".json")
            if checkpoint.exists():
                row = read_json(checkpoint)
                if row["input_signature"] != signature:
                    raise ValueError("Review checkpoint source mismatch")
                validate(row["review"], data)
                if row.get("adjudication"):
                    validate(row["adjudication"], data)
                return row
            prompt = RULES + "\nINPUT:\n" + json.dumps(data, ensure_ascii=False)
            review = await client.json(prompt, role="judge", validator=lambda v: validate(v, data), label=group + ":" + qid + ":blind_review",
                                       response_transform=lambda v: prepare_review(v, data), recover_attempts=True,
                                       fresh_validator=require_explicit_source_selections,
                                       validation_feedback=lambda v, e: quote_validation_feedback(v, data))
            changed = differs(record, review, qa)
            adjudication = None
            if changed:
                original_fields = {f: record[f] for f in ("quality_label", "hallucinated", "covered_key_points", "missing_key_points", "rationale")}
                adjudication_prompt = RULES + "\nAdjudicate a scoring disagreement from raw evidence. Neither review is authoritative. Do not vote or average: derive the decision from the ACTUAL answer, point by point, and the supplied raw chunks. Explain why any original missing-point or hallucination claim was correct or wrong. Follow the identical JSON schema with exact answer/source spans.\nINPUT:\n" + json.dumps(data, ensure_ascii=False) + "\nFIRST SCORE:\n" + json.dumps(original_fields, ensure_ascii=False) + "\nBLIND REVIEW:\n" + json.dumps(review, ensure_ascii=False)
                adjudication = await client.json(adjudication_prompt, role="judge", validator=lambda v: validate(v, data), label=group + ":" + qid + ":adjudication",
                                                response_transform=lambda v: prepare_review(v, data), recover_attempts=True,
                                                fresh_validator=require_explicit_source_selections,
                                                validation_feedback=lambda v, e: quote_validation_feedback(v, data))
            row = {"question_id": qid, "group": group, "input_signature": signature,
                   "original_record_sha256": file_hash(path), "review": review,
                   "disagreed_with_original": changed, "adjudication": adjudication, "completed_at": utc()}
            write_json(checkpoint, row)
            return row

    async def tracked(path):
        try:
            row = await one(path)
            record = read_json(path)
            qa = questions[row["question_id"]]
            decision = row["adjudication"] or row["review"]
            revised = {**record, **review_fields(decision, qa), "score_audit_version": protocol["version"],
                       "original_score": {f: record[f] for f in ("quality_label", "hallucinated", "key_point_coverage", "rationale")}}
            write_json(output / "audited_records" / row["group"] / (row["question_id"] + ".json"), revised)
            async with lock:
                records.append(revised)
                status["completed"] += 1
                status["disagreements"] += row["disagreed_with_original"]
                status.update(updated_at=utc(), actual_requests=request_stats())
                write_json(output / "progress.json", status)
                print(json.dumps({"audited": row["question_id"], "group": row["group"], "done": status["completed"], "disagreement": row["disagreed_with_original"]}), flush=True)
        except Exception as e:
            async with lock:
                status["errors"].append({"record": path.relative_to(original).as_posix(), "error_type": type(e).__name__,
                                         "validation_error": str(e)[:250] if isinstance(e, ValueError) else None})
                write_json(output / "progress.json", status)
                print(json.dumps({"failed_audit": path.relative_to(original).as_posix(), "error_type": type(e).__name__}), flush=True)

    try:
        await asyncio.gather(*(tracked(p) for p in paths))
        after = {p.relative_to(original).as_posix(): file_hash(p) for p in paths}
        status.update(original_records_unchanged=before == after, finished_at=utc(), actual_requests=request_stats())
        status["complete"] = len(records) == 240 and not status["errors"] and before == after
        status["stage"] = "completed" if status["complete"] else "incomplete"
        groups = summary["protocol"]["groups"]
        aggregates = formal.aggregate_summary(records, groups)
        strata = {f: formal.aggregate_by_field(records, groups, f) for f in ("answerable", "question_type", "difficulty", "support_mode", "fact_arity")}
        comparisons = formal.pairwise(records, groups)
        changes = []
        for r in records:
            old = r["original_score"]
            if old["quality_label"] != r["quality_label"] or old["hallucinated"] != r["hallucinated"] or old["key_point_coverage"] != r["key_point_coverage"]:
                changes.append({"group": r["group"], "question_id": r["question_id"], "original": old,
                                "audited": {f: r[f] for f in ("quality_label", "hallucinated", "key_point_coverage", "rationale")}})
        write_json(output / "summary.json", {"status": status, "groups": aggregates, "strata": strata,
                    "pairwise": comparisons, "changed_scores": changes,
                    "original_summary": summary["groups"], "protocol": protocol,
                    "limitations": ["Reviews and adjudication use the same LLM in separate prompts; they are not independent human judgments.",
                                    "Gold references cover 25 documents; negative evidence audit covers all 60.",
                                    "Gold chunk matches are incomplete relevance annotations and are not exhaustive recall."]})
        formal.write_csv(output / "summary.csv", aggregates)
        for field, rows in strata.items():
            formal.write_csv(output / ("by_" + field + ".csv"), rows)
        formal.write_csv(output / "pairwise.csv", comparisons)
        write_json(output / "progress.json", status)
        return 0 if status["complete"] else 2
    finally:
        await client.close()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gold", type=Path, required=True)
    p.add_argument("--evaluation", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    raise SystemExit(asyncio.run(run(p.parse_args())))


if __name__ == "__main__":
    main()
