"""Recover only missing score reviews using an unambiguous raw-span JSON schema.

The same semantic rules and exact validators apply. Accepted prior calls and
reviews remain unchanged. No answers, retrievals or embeddings are generated.
"""
import argparse
import asyncio
import json
import subprocess
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, MODEL, digest, file_hash, read_json, write_json, parse_json_response, utc
from scripts.audit_pfas_qa40_scores import (
    RULES, packet, source_span_catalog, prepare_review, validate,
    require_explicit_source_selections, differs,
)


def indexed_prompt(data, original=None, review=None):
    # Keep the semantic scoring rules verbatim; replace the contradictory old
    # response schema instead of placing another schema after failed JSON.
    rules = RULES.split("Return exactly one JSON object with this schema:")[0]
    payload = {k: v for k, v in data.items() if k != "raw_retrieved_chunks"}
    payload["RAW_RETRIEVED_SPAN_CATALOG"] = source_span_catalog(data)
    schema = {
        "point_checks": [{"point_id": 0, "covered": True, "answer_quote": "copy actual answer", "reason": "specific reason"}],
        "claim_checks": [{"answer_quote": "copy actual answer", "supported": True,
                          "evidence_rank": 1, "source_span_id": "exact catalog ID", "source_quote": "",
                          "reason": "independently explain whether this actual raw span supports the actual claim"}],
        "hallucinated": False, "unsupported_claims_found": [], "quality_label": "GOOD or SATISFACTORY or POOR",
        "citation_support_score": 0.0, "rationale": "specific overall reason",
    }
    text = rules + "\nRESPONSE FORMAT: Return exactly one complete JSON object in the following format. "
    text += "Every supported claim MUST select source_span_id from RAW_RETRIEVED_SPAN_CATALOG and set evidence_rank to that span's rank. "
    text += "Set source_quote to the empty string; the exact catalog text will be copied mechanically, without scientific edits. "
    text += "The selected raw text must actually support the claim. Selection alone is not evidence of support. "
    text += "For unsupported claims set supported=false, source_span_id='', source_quote='', evidence_rank=null. "
    text += "Check every rubric point in order; actual-answer quotes must be contiguous verbatim spans. "
    text += "Do not use reference quotes as retrieved sources. All summary fields are mandatory.\nSCHEMA:\n"
    text += json.dumps(schema, ensure_ascii=False) + "\nINPUT:\n" + json.dumps(payload, ensure_ascii=False)
    if original is not None:
        text += "\nSOURCE-BASED ADJUDICATION: Derive the decision from the actual answer, rubric and retrieved raw text; do not vote or average. Explain a previous scoring error if any.\n"
        text += "ORIGINAL SCORE:\n" + json.dumps(original, ensure_ascii=False)
        text += "\nBLIND REVIEW:\n" + json.dumps(review, ensure_ascii=False)
    return text


def accepted_call(client, prompt, data):
    signature = digest({"prompt": prompt, "role": "judge", "model": MODEL, "temperature": 0,
                        "reasoning_effort": "low", "protocol": "pfas-qa-strict-v1"})
    path = client.prompt_cache / (signature + ".json")
    if not path.exists():
        return None
    row = read_json(path)
    if row.get("status") != "ok" or row.get("signature") != signature:
        return None
    value = prepare_review(parse_json_response(row["content"], row["finish_reason"]), data)
    validate(value, data)
    return value


async def recover(args):
    gold = read_json(args.gold)
    questions = {q["question_id"]: q for q in gold["qa_questions"]}
    chunks = read_json(gold["source"]["chunks"])
    protocol = read_json(args.output / "protocol.json")
    assert file_hash(args.gold) == protocol["gold_sha256"]
    assert file_hash(gold["source"]["chunks"]) == gold["source"]["chunks_sha256"]
    assert protocol["rules_sha256"] == digest(RULES)
    client = QAClient(args.output)
    failures = []

    async def one(path):
        record = read_json(path)
        group, qid = record["group"], record["question_id"]
        checkpoint = args.output / "reviews" / group / (qid + ".json")
        if checkpoint.exists():
            return
        assert protocol["original_record_hashes"][path.relative_to(args.evaluation).as_posix()] == file_hash(path)
        qa = questions[qid]
        retrieval = read_json(args.evaluation / "retrieval" / group / (qid + ".json"))
        data = packet(qa, record, retrieval, chunks)
        signature = digest({"data": data, "original_record": file_hash(path), "protocol": protocol["version"]})
        original_prompt = RULES + "\nINPUT:\n" + json.dumps(data, ensure_ascii=False)
        review = accepted_call(client, original_prompt, data)
        reused = review is not None
        if review is None:
            review = await client.json(indexed_prompt(data), role="judge", label=group + ":" + qid + ":indexed_blind",
                                       response_transform=lambda v: prepare_review(v, data),
                                       validator=lambda v: validate(v, data), fresh_validator=require_explicit_source_selections)
        changed = differs(record, review, qa)
        adjudication = None
        if changed:
            original = {f: record[f] for f in ("quality_label", "hallucinated", "covered_key_points", "missing_key_points", "rationale")}
            adjudication = await client.json(indexed_prompt(data, original, review), role="judge", label=group + ":" + qid + ":indexed_adjudication",
                                            response_transform=lambda v: prepare_review(v, data),
                                            validator=lambda v: validate(v, data), fresh_validator=require_explicit_source_selections)
        row = {"question_id": qid, "group": group, "input_signature": signature,
               "original_record_sha256": file_hash(path), "review": review,
               "disagreed_with_original": changed, "adjudication": adjudication, "completed_at": utc(),
               "response_format_protocol": "explicit-raw-span-schema-v2", "prior_blind_call_reused": reused}
        assert not checkpoint.exists(), "A completed review must never be overwritten"
        write_json(checkpoint, row)
        print(json.dumps({"recovered": group + ":" + qid, "reused_blind": reused}), flush=True)

    async def tracked(path):
        try:
            await one(path)
        except Exception as exc:
            failures.append({"record": path.relative_to(args.evaluation).as_posix(), "error_type": type(exc).__name__})

    try:
        await asyncio.gather(*(tracked(p) for p in sorted((args.evaluation / "records").rglob("*.json"))))
        write_json(args.output / "indexed_recovery_status.json", {"at": utc(), "errors": failures,
                     "reviews": len(list((args.output / "reviews").rglob("*.json"))),
                     "semantic_rules_sha256": digest(RULES), "response_format_protocol": "explicit-raw-span-schema-v2"})
    finally:
        await client.close()
    return not failures


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gold", type=Path, required=True)
    p.add_argument("--evaluation", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    ok = asyncio.run(recover(args))
    if ok:
        # All calls/reviews now resume; this step only rebuilds audit aggregates.
        raise SystemExit(subprocess.run([sys.executable, "-u", "-m", "scripts.audit_pfas_qa40_scores", "--gold", str(args.gold),
                                         "--evaluation", str(args.evaluation), "--output", str(args.output)]).returncode)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
