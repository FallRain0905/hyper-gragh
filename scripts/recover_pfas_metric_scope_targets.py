"""Recover failed target subrecords without guessing IDs or changing valid data."""
import asyncio
import collections
import copy
import json
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, read_json, write_json, parse_json_response, file_hash, digest, utc
from scripts.evaluate_pfas_shared_retrieval import prepare, validate_annotation
from scripts.adjudicate_pfas_shared_retrieval import ADJUDICATION_RULES, patched_annotation, validate_review, source_conflicts, materialize
from scripts.audit_pfas_retrieval_metric_scope import SCOPE_POLICY, scope_packet, scope_selection
from scripts.run_pfas_qa40 import request_stats


def retained_targets(packet, value, rows):
    expected = {t["target_id"]: t for t in packet["targets"]}
    decisions = value.get("target_decisions", [])
    counts = collections.Counter(d.get("target_id") for d in decisions if isinstance(d, dict))
    valid, issues, effective = {}, [], dict(rows)
    for d in decisions:
        if not isinstance(d, dict): continue
        tid = d.get("target_id")
        if tid not in expected or counts[tid] != 1:
            issues.append({"received_target_id": tid, "reason": "Unknown or duplicate ID; never mapped by spelling similarity."})
            continue
        t = expected[tid]
        try:
            a = patched_annotation(t, d)
            validate_annotation(a, {**packet, "RAW_SPAN_CATALOG": {sid: packet["RAW_SPAN_CATALOG"][sid] for sid in t["allowed_span_ids"]}})
        except (ValueError, KeyError, TypeError) as exc:
            issues.append({"received_target_id": tid, "reason": str(exc)})
            continue
        valid[tid] = copy.deepcopy(d)
        for key in t["aliases"]: effective[key] = {**rows[key], "annotation": a}
    aliases = {key: t["target_id"] for t in packet["targets"] for key in t["aliases"]}
    implicated = set()
    for c in source_conflicts(effective):
        if c["question_id"] != packet["question_id"]: continue
        keys = ["sets/" + c["set_id"]] + ["pool/" + c["question_id"] + "__" + cid for cid in c["single_chunk_full_support_ids"]]
        implicated.update(aliases[k] for k in keys if k in aliases)
    for tid in implicated:
        if tid in valid:
            del valid[tid]
            issues.append({"received_target_id": tid, "reason": "Requires joint source-consistency review with a failed target."})
    return valid, [t for t in packet["targets"] if t["target_id"] not in valid], issues


def merge_review(packet, original, retained, fresh):
    missing = [t["target_id"] for t in packet["targets"] if t["target_id"] not in retained]
    items = fresh.get("target_decisions")
    if not isinstance(items, list) or any(not isinstance(d, dict) for d in items) or [d.get("target_id") for d in items] != missing:
        raise ValueError("Fresh response must supply exactly the failed target IDs in order")
    for v in (original, fresh):
        if type(v.get("source_ambiguity_requires_manual")) is not bool or not isinstance(v.get("source_ambiguity_reason"), str):
            raise ValueError("Explicit scientific ambiguity status required")
        if bool(v["source_ambiguity_reason"].strip()) != v["source_ambiguity_requires_manual"]:
            raise ValueError("A scientific ambiguity reason must agree with its explicit flag")
    all_decisions = {**retained, **{d["target_id"]: d for d in items}}
    flag = original["source_ambiguity_requires_manual"] or fresh["source_ambiguity_requires_manual"]
    reasons = [v["source_ambiguity_reason"] for v in (original, fresh) if v["source_ambiguity_requires_manual"]]
    return {"target_decisions": [copy.deepcopy(all_decisions[t["target_id"]]) for t in packet["targets"]],
            "source_ambiguity_requires_manual": flag, "source_ambiguity_reason": "\n".join(reasons)}


async def run():
    root = Path(r"D:\Hyper-rag-case2-backups\qa40_workspace\shared_retrieval_v1")
    qa, output = root.parent, root / "metric_scope_v1"
    retry = output / "target_recovery_v1"; retry.mkdir(exist_ok=True)
    base = root / "source_consistency_v1/effective_labels"
    protocol, gold, chunks, pool, sets, _ = prepare(base, qa)
    backup_pointer = read_json(output / "latest_target_recovery_backup.json")
    assert file_hash(backup_pointer["manifest"]) == backup_pointer["sha256"]
    backup = read_json(backup_pointer["manifest"]); assert backup["complete"] and backup["readback_verified"]
    rows = {"pool/" + r["question_id"] + "__" + r["chunk_id"]: read_json(base / "pool" / (r["question_id"] + "__" + r["chunk_id"] + ".json")) for r in pool}
    rows.update({"sets/" + sid: read_json(base / "sets" / (sid + ".json")) for sid in sets})
    qid, pids = next(iter(scope_selection(gold).items()))
    q = next(q for q in gold["qa_questions"] if q["question_id"] == qid)
    packet = scope_packet(q, pids, rows, chunks)
    scope_protocol = read_json(output / "protocol.json")
    assert digest(packet) == scope_protocol["input_hashes"][qid]
    candidates = [p for p in (output / "calls").glob("*.attempt*.json") if read_json(p).get("finish_reason") == "stop"]
    raw_path = max(candidates, key=lambda p: p.stat().st_mtime_ns)
    trial = read_json(raw_path); original = parse_json_response(trial["content"], trial["finish_reason"])
    retained, targets, issues = retained_targets(packet, original, rows)
    needed = {sid for t in targets for sid in t["allowed_span_ids"]}
    subset = {**packet, "targets": targets, "RAW_SPAN_CATALOG": {sid: s for sid, s in packet["RAW_SPAN_CATALOG"].items() if sid in needed}}
    proof = {"raw_trial": str(raw_path), "raw_trial_sha256": file_hash(raw_path), "finish_reason": trial["finish_reason"],
             "retained_ids": sorted(retained), "retained_subrecord_hashes": {k: digest(v) for k, v in retained.items()},
             "fresh_required_ids": [t["target_id"] for t in targets], "issues": issues,
             "no_approximate_identity_mapping": True, "strict_original_validation_unchanged": True}
    write_json(retry / "selection.json", proof)
    state = {"stage": "failed_target_recovery", "started_at": utc(), "retained_targets": len(retained),
             "fresh_targets": len(targets), "complete": False}
    write_json(retry / "progress.json", state)
    client = QAClient(retry)
    try:
        error = ""
        for budget in (4096, 8192, 16384):
            prompt = ADJUDICATION_RULES + "\n" + SCOPE_POLICY
            prompt += "\nReturn only the offered failed/associated target subrecords. Other valid subrecords remain unchanged. Copy the offered target IDs exactly; do not guess or shorten them. Keep reasons concise but specific."
            if error: prompt += "\nPrevious validation category (no rejected assistant output): " + error
            prompt += "\nINPUT:\n" + json.dumps(subset, ensure_ascii=False)
            def validate(value):
                merged = merge_review(packet, original, retained, value)
                validate_review(merged, packet, rows)
            try:
                fresh = await client.json(prompt, role="judge", validator=validate, label="failed-targets:" + qid, budgets=(budget,))
                break
            except RuntimeError:
                audit = [json.loads(x) for x in (retry / "request_audit.jsonl").read_text(encoding="utf-8").splitlines()]
                error = audit[-1].get("validation_error") or "Transient request failure"
        else: raise RuntimeError("Failed target recovery exhausted bounded strict attempts")
        merged = merge_review(packet, original, retained, fresh)
        validate_review(merged, packet, rows)
        for d in merged["target_decisions"]:
            if d["target_id"] in retained: assert digest(d) == proof["retained_subrecord_hashes"][d["target_id"]]
        signature = digest({"input": packet, "protocol": scope_protocol})
        path = output / "reviews" / (qid + ".json")
        assert not path.exists(), "Completed scope review must not be overwritten"
        write_json(path, {"signature": signature, "input": packet, "result": merged, "at": utc(), "human_confirmed": False,
                          "target_recovery": proof, "fresh_response_sha256": digest(fresh)})
    finally:
        await client.close()
    for path, expected in backup["file_hashes"].items(): assert file_hash(path) == expected
    derived, manual = materialize(base, qa, output, protocol, gold, chunks, rows, {qid: {"input": packet, "result": merged}})
    state.update(stage="metric_scope_completed_via_target_recovery", finished_at=utc(), complete=True, prior_failed_evidence_unchanged=True,
                 effective_labels=str(derived), manual_skips=len(manual), actual_requests=request_stats(),
                 remaining_conflicts=len(read_json(derived / "cross_packet_consistency.json")["conflicts"]))
    write_json(retry / "progress.json", state)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    asyncio.run(run())
