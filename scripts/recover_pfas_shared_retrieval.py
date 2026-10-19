"""Recover only missing shared-retrieval labels, preserving all prior evidence."""
import argparse
import asyncio
import json
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, digest, file_hash, read_json, write_json, utc, parse_json_response
from scripts.evaluate_pfas_shared_retrieval import (
    RULES, prepare, annotation_packet, validate_annotation, validate_checkpoint,
    derive_grade, report,
)
from scripts.run_pfas_qa40 import request_stats


def complete_json_without_fence_repair(content, finish):
    """Unwrap only a Markdown opening fence around otherwise complete JSON.

    Never complete a truncated object, discard trailing prose, or change fields.
    The raw failed trial remains immutable and its hash is recorded separately.
    """
    try:
        return parse_json_response(content, finish), "none"
    except ValueError:
        if finish != "stop" or not isinstance(content, str):
            raise
        header, newline, body = content.strip().partition("\n")
        if not newline or header.strip() not in ("```json", "```"):
            raise
        # The standard parser already handles paired fences. Only the single
        # opening fence is removed here; json.loads must consume the whole body.
        value = json.loads(body)
        if not isinstance(value, dict):
            raise ValueError("Expected exactly one complete annotation object")
        return value, "opening_markdown_fence_only"


def retry_prompt(packet, previous_error=""):
    guidance = (
        "\nCLEAN TECHNICAL RETRY: No earlier assistant response is included. "
        "Reassess the actual raw sources; do not change scientific judgments merely "
        "to satisfy a validator. Return only one complete JSON object, without Markdown. "
        "A partial/full rubric match implies useful context with an exact offered span. "
        "If the text is only generic PFAS background, reconsider the point as none; "
        "do not infer useful context from a shared chemical name alone. "
        "Every required boolean, evidence list and point must be supplied.\n"
    )
    if not packet["answerable"]:
        guidance += (
            "NEGATIVE QUERY MODE: The rubric consists of QA response behaviors, "
            "NOT positive facts to be established by this source packet. Neither "
            "absence of a result nor obeying 'do not invent' can be proved by a local "
            "packet. Copy the mandatory point checks below, all support=none and "
            "span_ids=[]. Independently inspect whether the packet actually reports "
            "a direct answer with the requested exact target/condition/value binding. "
            "Only such a direct answer can set negative_query_answer_found=true; "
            "then also set context_relevant=true with exact source IDs. Never use a "
            "missing result as a positive answer.\nMANDATORY_POINT_CHECKS:\n"
        )
        guidance += json.dumps([
            {"point_id": p["point_id"], "support": "none", "span_ids": [],
             "reason": "Corpus-wide absence and QA response behavior are not established by a local evidence packet."}
            for p in packet["rubric"]
        ], ensure_ascii=False)
    if previous_error:
        guidance += "\nPrevious strict validation category, not an answer to copy: " + previous_error[:350]
    return RULES + guidance + "\nINPUT:\n" + json.dumps(packet, ensure_ascii=False)


def checkpoint_row(packet, protocol, value, kind, provenance):
    validate_annotation(value, packet)
    selected = {sid for p in value["point_checks"] for sid in p["span_ids"]}
    selected |= set(value["context_span_ids"]) | set(value["negative_answer_span_ids"])
    row = {"signature": digest({"packet": packet, "protocol": digest(protocol)}),
           "question_id": packet["question_id"],
           "chunk_ids": list(dict.fromkeys(s["chunk_id"] for s in packet["RAW_SPAN_CATALOG"].values())),
           "annotation": value, "span_evidence": {sid: packet["RAW_SPAN_CATALOG"][sid] for sid in selected},
           "completed_at": utc(), "human_confirmed": False, "technical_recovery": provenance}
    if kind == "pool":
        row["relevance_grade"] = derive_grade(value, packet["answerable"])
    validate_checkpoint(row, packet, protocol)
    return row


def offline_trial(root, packet):
    prompt = RULES + "\nINPUT:\n" + json.dumps(packet, ensure_ascii=False)
    signature = digest({"prompt": prompt, "role": "judge", "model": "deepseek-ai/DeepSeek-V4-Flash",
                        "temperature": 0, "reasoning_effort": "low", "protocol": "pfas-qa-strict-v1"})
    paths = sorted((root / "calls").glob(signature + ".attempt*.json"), key=lambda p: p.stat().st_mtime_ns, reverse=True)
    cache = root / "calls" / (signature + ".json")
    if cache.exists(): paths.insert(0, cache)
    for p in paths:
        trial = read_json(p)
        if trial.get("signature") != signature or trial.get("finish_reason") != "stop":
            continue
        try:
            value, repair = complete_json_without_fence_repair(trial.get("content"), trial.get("finish_reason"))
            validate_annotation(value, packet)
        except (ValueError, KeyError, TypeError):
            continue
        return value, {"mode": "offline_complete_response_validation", "format_repair": repair,
                       "raw_trial": str(p), "raw_trial_sha256": file_hash(p), "new_api_requests": 0}
    return None, None


async def run(root, qa, offline_only=False):
    protocol, gold, chunks, pool, sets, _ = prepare(root, qa)
    backup_pointer = read_json(root / "latest_retry_backup.json")
    assert file_hash(backup_pointer["manifest"]) == backup_pointer["sha256"]
    backup = read_json(backup_pointer["manifest"])
    assert backup["complete"] and backup["readback_verified"]
    retry_root = root / "technical_retry_v1"
    retry_root.mkdir(exist_ok=True)
    questions = {q["question_id"]: q for q in gold["qa_questions"]}
    tasks = [("pool", r["question_id"] + "__" + r["chunk_id"], r["question_id"], [r["chunk_id"]]) for r in pool]
    tasks += [("sets", sid, r["question_id"], r["chunk_ids"]) for sid, r in sets.items()]
    missing, offline_recovered = [], []
    for kind, key, qid, ids in tasks:
        path = root / kind / (key + ".json")
        packet = annotation_packet(questions[qid], ids, chunks)
        if path.exists():
            validate_checkpoint(read_json(path), packet, protocol)
            continue
        value, proof = offline_trial(root, packet)
        if value is not None:
            write_json(path, checkpoint_row(packet, protocol, value, kind, proof))
            offline_recovered.append({"kind": kind, "key": key, **proof})
        else:
            missing.append((kind, key, qid, ids))
    write_json(retry_root / "offline_recovery.json", {"at": utc(), "items": offline_recovered})
    state = {"started_at": utc(), "stage": "technical_retry", "prior_pool_success": backup["pool_success"],
             "prior_set_success": backup["set_success"], "offline_recovered": len(offline_recovered),
             "missing_total": len(missing), "newly_completed": 0, "errors": [], "complete": False}
    write_json(retry_root / "progress.json", state)
    if offline_only:
        return 0
    client = QAClient(retry_root)
    semaphore, locks, state_lock = asyncio.Semaphore(10), {}, asyncio.Lock()
    async def one(kind, key, qid, ids):
        async with semaphore:
            packet = annotation_packet(questions[qid], ids, chunks)
            signature = digest(packet)
            async with locks.setdefault(signature, asyncio.Lock()):
                previous_error = ""
                for budget in (4096, 8192, 16384):
                    prompt = retry_prompt(packet, previous_error)
                    try:
                        value = await client.json(prompt, role="judge", validator=lambda v: validate_annotation(v, packet),
                                                  label=kind + ":" + qid + ":" + key, budgets=(budget,))
                        proof = {"mode": "clean_root_same_rules_and_validator", "call_prompt_sha256": digest(prompt),
                                 "output_budget": budget, "client_output": str(retry_root)}
                        path = root / kind / (key + ".json")
                        assert not path.exists(), "Successful annotation must never be replaced"
                        write_json(path, checkpoint_row(packet, protocol, value, kind, proof))
                        return
                    except RuntimeError:
                        signature_call = digest({"prompt": prompt, "role": "judge", "model": "deepseek-ai/DeepSeek-V4-Flash",
                                                 "temperature": 0, "reasoning_effort": "low", "protocol": "pfas-qa-strict-v1"})
                        trials = sorted((retry_root / "calls").glob(signature_call + ".attempt*.json"), key=lambda p: p.stat().st_mtime_ns)
                        previous_error = read_json(trials[-1]).get("validation_error") or "Transient request failure" if trials else "Transient request failure"
                raise RuntimeError("Technical recovery exhausted bounded clean-root attempts")
    async def tracked(task):
        kind, key, qid, ids = task
        try:
            await one(*task)
            async with state_lock:
                state["newly_completed"] += 1
        except Exception as exc:
            async with state_lock:
                state["errors"].append({"kind": kind, "key": key, "question_id": qid, "error_type": type(exc).__name__})
        async with state_lock:
            state.update(updated_at=utc(), actual_requests=request_stats())
            write_json(retry_root / "progress.json", state)
            print(json.dumps({"newly_completed": state["newly_completed"], "errors": len(state["errors"])}), flush=True)
    try:
        await asyncio.gather(*(tracked(t) for t in missing))
    finally:
        await client.close()
    # All prior successful calls, checkpoints, raw trials, original protocol and
    # original source snapshots remain byte-identical. Newly added records alone
    # are outside this stopped-run preservation manifest.
    for path, expected in backup["original_file_hashes"].items():
        assert file_hash(path) == expected, "A pre-recovery file changed: " + path
    state.update(finished_at=utc(), complete=not state["errors"], prior_files_unchanged=True, actual_requests=request_stats())
    if state["complete"]:
        report(root, qa)
        consistency = read_json(root / "cross_packet_consistency.json")
        state.update(stage="annotation_completed_consistency_pending" if consistency["conflicts"] else "completed",
                     pending_source_consistency_checks=len(consistency["conflicts"]))
    else:
        state["stage"] = "technical_retry_incomplete"
    write_json(retry_root / "progress.json", state)
    return 0 if state["complete"] else 2


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(r"D:\Hyper-rag-case2-backups\qa40_workspace\shared_retrieval_v1"))
    p.add_argument("--offline-only", action="store_true")
    a = p.parse_args()
    raise SystemExit(asyncio.run(run(a.root, a.root.parent, a.offline_only)))


if __name__ == "__main__": main()
