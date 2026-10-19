"""Source-based consistency review, with immutable initial shared PFAS labels."""
import argparse
import asyncio
import copy
import json
import shutil
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, digest, read_json, write_json, file_hash, utc
from scripts.evaluate_pfas_shared_retrieval import (
    RULES, prepare, annotation_packet, validate_annotation, validate_checkpoint, derive_grade, report,
)
from scripts.run_pfas_qa40 import request_stats

ADJUDICATION_RULES = RULES.split("Return one COMPLETE JSON object", 1)[0] + """
This is source-based adjudication of conflicting single-chunk/joint support labels.
All system names, QA answers and system scores are hidden. Earlier annotations
are hypotheses, not votes. Re-read the exact raw sources. A compound rubric
point is full only when every part is established with the correct scientific
scope; a useful subset is partial. A complete individual chunk cannot lose that
support merely by appearing in a larger packet. Correct either or both earlier
labels according to the text, without preferring a system or forcing full support.
Only listed disputed points may be changed; other point fields remain frozen.
Select IDs only from the target's allowed source spans, even though other raw
sources are visible for adjudication. Never use an outside source to improve a
target packet. Binding issues must be explained, not invented for absent details.
Return exactly one JSON object using this sole response schema:
{
 "target_decisions":[{
   "target_id":"copy an offered target ID",
   "point_decisions":[{"point_id":0,"support":"partial","span_ids":[],"reason":"source-based explanation","binding_issue_reason":""}],
   "context_relevant":true,"context_span_ids":[],"rationale":"source-based overall explanation"
 }],
 "source_ambiguity_requires_manual":false,"source_ambiguity_reason":""
}
Return EVERY target and EVERY listed disputed point in the supplied order.
Choose support from exactly full, partial, none. Partial/full need exact source
IDs; none needs an empty list. A full point cannot have a binding issue. Specific
useful context requires an exact span; broad PFAS background is not sufficient.
Explain why the disputed complete point is or is not established, including its
numeric/condition/target binding. The original reference answer is not evidence.
If the raw science genuinely admits unresolved interpretations, set the manual
flag and give the precise scientific ambiguity; technical JSON/ID problems are
not manual cases. Otherwise resolve all stated single/joint contradictions.
"""


def remap_spans(annotation, source_catalog, destination_catalog):
    """Map explicit selections only by identical chunk, offset and raw bytes."""
    index = {(s["chunk_id"], s["start"], s["end"], s["exact_raw_text"]): sid for sid, s in destination_catalog.items()}
    out = copy.deepcopy(annotation)
    proof = {}
    def remap(ids):
        result = []
        for sid in ids:
            s = source_catalog[sid]
            key = (s["chunk_id"], s["start"], s["end"], s["exact_raw_text"])
            if key not in index:
                raise ValueError("Selected source is outside this exact target packet")
            result.append(index[key])
            proof[sid] = index[key]
        return result
    for p in out["point_checks"]:
        p["span_ids"] = remap(p["span_ids"])
    for field in ("context_span_ids", "negative_answer_span_ids"):
        out[field] = remap(out[field])
    return out, proof


def source_conflicts(rows):
    conflicts = []
    for key, joint in rows.items():
        if not key.startswith("sets/"): continue
        for pid, point in enumerate(joint["annotation"]["point_checks"]):
            singles = [cid for cid in joint["chunk_ids"] if rows["pool/" + joint["question_id"] + "__" + cid]["annotation"]["point_checks"][pid]["support"] == "full"]
            if singles and point["support"] != "full":
                conflicts.append({"question_id": joint["question_id"], "set_id": key.split("/", 1)[1],
                                  "point_id": pid, "single_chunk_full_support_ids": singles})
    return conflicts


def review_packet(question, conflicts, rows, chunks):
    targets = {}
    for c in conflicts:
        source_keys = ["sets/" + c["set_id"]] + ["pool/" + question["question_id"] + "__" + cid for cid in c["single_chunk_full_support_ids"]]
        for key in source_keys:
            row = rows[key]
            canonical = key if key.startswith("pool/") else "sets/" + digest(sorted(row["chunk_ids"]))[:24]
            target = targets.setdefault(canonical, {"target_id": canonical, "base_key": key, "aliases": [], "disputed_point_ids": set()})
            target["disputed_point_ids"].add(c["point_id"])
    for target in targets.values():
        base = rows[target["base_key"]]
        target["chunk_ids"] = base["chunk_ids"]
        target["aliases"] = [key for key, row in rows.items() if key.split("/", 1)[0] == target["base_key"].split("/", 1)[0]
                             and row["question_id"] == question["question_id"] and row["chunk_ids"] == base["chunk_ids"]]
        assert all(rows[k]["annotation"] == base["annotation"] for k in target["aliases"]), "Identical source sets already have conflicting initial annotations"
        target["disputed_point_ids"] = sorted(target["disputed_point_ids"])
    targets = sorted(targets.values(), key=lambda t: t["target_id"])
    all_ids = sorted({cid for t in targets for cid in t["chunk_ids"]})
    packet = annotation_packet(question, all_ids, chunks)
    for target in targets:
        prior = rows[target["base_key"]]
        local = annotation_packet(question, prior["chunk_ids"], chunks)
        target["prior_annotation"], _ = remap_spans(prior["annotation"], local["RAW_SPAN_CATALOG"], packet["RAW_SPAN_CATALOG"])
        target["allowed_span_ids"] = [sid for sid, s in packet["RAW_SPAN_CATALOG"].items() if s["chunk_id"] in target["chunk_ids"]]
    packet["targets"] = targets
    packet["initial_contradictions"] = conflicts
    return packet


def patched_annotation(target, decision):
    if decision.get("target_id") != target["target_id"]:
        raise ValueError("Wrong adjudication target")
    points = decision.get("point_decisions")
    if not isinstance(points, list) or any(not isinstance(p, dict) or type(p.get("point_id")) is not int for p in points):
        raise ValueError("Ordered complete disputed-point decisions required")
    if [p["point_id"] for p in points] != target["disputed_point_ids"]:
        raise ValueError("All and only the listed disputed points may change")
    out = copy.deepcopy(target["prior_annotation"])
    out["binding_issues"] = [x for x in out["binding_issues"] if x["point_id"] not in target["disputed_point_ids"]]
    for p in points:
        if not isinstance(p.get("binding_issue_reason"), str):
            raise ValueError("Binding issue reason must be a string, empty when absent")
        out["point_checks"][p["point_id"]] = {k: p.get(k) for k in ("point_id", "support", "span_ids", "reason")}
        if p["binding_issue_reason"].strip():
            out["binding_issues"].append({"point_id": p["point_id"], "reason": p["binding_issue_reason"]})
    for field in ("context_relevant", "context_span_ids", "rationale"):
        out[field] = decision.get(field)
    return out


def validate_review(value, packet, rows):
    if not isinstance(value, dict) or type(value.get("source_ambiguity_requires_manual")) is not bool:
        raise ValueError("Explicit scientific ambiguity flag required")
    reason = value.get("source_ambiguity_reason")
    if not isinstance(reason, str) or bool(reason.strip()) != value["source_ambiguity_requires_manual"]:
        raise ValueError("Manual cases require a specific scientific explanation; resolved cases use an empty explanation")
    decisions = value.get("target_decisions")
    if not isinstance(decisions, list) or any(not isinstance(x, dict) for x in decisions):
        raise ValueError("Complete target decisions required")
    if [x.get("target_id") for x in decisions] != [t["target_id"] for t in packet["targets"]]:
        raise ValueError("Every target must appear exactly once in order")
    effective = dict(rows)
    for target, decision in zip(packet["targets"], decisions):
        annotation = patched_annotation(target, decision)
        scoped = {**packet, "RAW_SPAN_CATALOG": {sid: packet["RAW_SPAN_CATALOG"][sid] for sid in target["allowed_span_ids"]}}
        validate_annotation(annotation, scoped)
        for key in target["aliases"]:
            effective[key] = {**rows[key], "annotation": annotation}
    remaining = [c for c in source_conflicts(effective) if c["question_id"] == packet["question_id"]]
    if remaining and not value["source_ambiguity_requires_manual"]:
        raise ValueError("Source review still contains single/joint support contradictions at point IDs " + str(sorted({x["point_id"] for x in remaining})))


def materialize(root, qa, output, protocol, gold, chunks, rows, reviews):
    derived = output / "effective_labels"
    prepare(derived, qa)
    corrections = {}
    manual = []
    for qid, proof in reviews.items():
        packet, result = proof["input"], proof["result"]
        if result["source_ambiguity_requires_manual"]:
            manual.append({"query_id": qid, "reason": result["source_ambiguity_reason"], "status": "scientific_ambiguity_skipped_all_groups"})
        for target, decision in zip(packet["targets"], result["target_decisions"]):
            annotation = patched_annotation(target, decision)
            for key in target["aliases"]:
                prior = rows[key]
                q = next(q for q in gold["qa_questions"] if q["question_id"] == qid)
                local = annotation_packet(q, prior["chunk_ids"], chunks)
                remapped, mapping = remap_spans(annotation, packet["RAW_SPAN_CATALOG"], local["RAW_SPAN_CATALOG"])
                row = copy.deepcopy(prior)
                row["annotation"] = remapped
                selected = {sid for p in remapped["point_checks"] for sid in p["span_ids"]}
                selected |= set(remapped["context_span_ids"]) | set(remapped["negative_answer_span_ids"])
                row["span_evidence"] = {sid: local["RAW_SPAN_CATALOG"][sid] for sid in selected}
                if key.startswith("pool/"): row["relevance_grade"] = derive_grade(remapped, q["answerable"])
                row["source_consistency_adjudication"] = {"at": utc(), "review": str(output / "reviews" / (qid + ".json")),
                    "original_checkpoint_sha256": file_hash(root / (key + ".json")), "explicit_global_to_local_span_map": mapping,
                    "disputed_point_ids": target["disputed_point_ids"], "human_confirmed": False}
                validate_checkpoint(row, local, protocol)
                corrections[key] = row
    for key in rows:
        path = derived / (key + ".json")
        if key in corrections: write_json(path, corrections[key])
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / (key + ".json"), path)
    write_json(output / "manual_skip_queries.json", manual)
    write_json(output / "corrections.json", {"changed_targets": len(corrections), "keys": sorted(corrections),
               "initial_labels_untouched": True, "new_annotations_human_confirmed": False})
    report(derived, qa)
    return derived, manual


async def run(root):
    qa = root.parent
    output = root / "source_consistency_v1"
    output.mkdir(exist_ok=True)
    protocol, gold, chunks, pool, sets, _ = prepare(root, qa)
    pointer = read_json(root / "latest_consistency_backup.json")
    assert file_hash(pointer["manifest"]) == pointer["sha256"]
    backup = read_json(pointer["manifest"])
    assert backup["complete"] and backup["readback_verified"]
    rows = {"pool/" + r["question_id"] + "__" + r["chunk_id"]: read_json(root / "pool" / (r["question_id"] + "__" + r["chunk_id"] + ".json")) for r in pool}
    rows.update({"sets/" + sid: read_json(root / "sets" / (sid + ".json")) for sid in sets})
    conflicts = source_conflicts(rows)
    question_map = {q["question_id"]: q for q in gold["qa_questions"]}
    packets = {qid: review_packet(question_map[qid], [c for c in conflicts if c["question_id"] == qid], rows, chunks)
               for qid in sorted({c["question_id"] for c in conflicts})}
    review_protocol = {"version": "pfas-source-consistency-patch-v1", "original_protocol_sha256": file_hash(root / "protocol.json"),
                       "rules_sha256": digest(ADJUDICATION_RULES), "inputs_sha256": {qid: digest(p) for qid, p in packets.items()},
                       "initial_label_hashes": {key: file_hash(root / (key + ".json")) for key in rows},
                       "model": protocol["model"], "temperature": 0, "reasoning_effort": "low", "human_confirmed": False}
    if (output / "protocol.json").exists(): assert read_json(output / "protocol.json") == review_protocol
    else: write_json(output / "protocol.json", review_protocol)
    state = {"stage": "source_consistency_adjudication", "started_at": utc(), "initial_conflicts": len(conflicts),
             "queries_total": len(packets), "queries_done": 0, "errors": [], "complete": False}
    write_json(output / "progress.json", state)
    client, semaphore, lock, reviews = QAClient(output), asyncio.Semaphore(10), asyncio.Lock(), {}
    async def one(qid, packet):
        async with semaphore:
            path = output / "reviews" / (qid + ".json")
            signature = digest({"input": packet, "protocol": review_protocol})
            if path.exists():
                saved = read_json(path)
                assert saved["signature"] == signature
                value = saved["result"]
                validate_review(value, packet, rows)
            else:
                error = ""
                for budget in (4096, 8192, 16384):
                    prompt = ADJUDICATION_RULES + ("\nTechnical validation category to correct (no rejected answer is shown): " + error if error else "")
                    prompt += "\nINPUT:\n" + json.dumps(packet, ensure_ascii=False)
                    try:
                        value = await client.json(prompt, role="judge", validator=lambda v: validate_review(v, packet, rows), label="source-consistency:" + qid, budgets=(budget,))
                        break
                    except RuntimeError:
                        # Error category only; raw upstream exceptions never enter prompts/logs.
                        records = [json.loads(x) for x in (output / "request_audit.jsonl").read_text(encoding="utf-8").splitlines()]
                        own = [x for x in records if x["label"] == "source-consistency:" + qid]
                        error = own[-1].get("validation_error") or "Transient request failure"
                else: raise RuntimeError("Source consistency review exhausted bounded clean-root attempts")
                write_json(path, {"signature": signature, "input": packet, "result": value, "at": utc(), "human_confirmed": False})
            reviews[qid] = {"input": packet, "result": value}
    async def tracked(qid, packet):
        try:
            await one(qid, packet)
            async with lock: state["queries_done"] += 1
        except Exception as exc:
            async with lock: state["errors"].append({"question_id": qid, "error_type": type(exc).__name__})
        async with lock:
            state.update(updated_at=utc(), actual_requests=request_stats())
            write_json(output / "progress.json", state)
            print(json.dumps({"done": state["queries_done"], "total": len(packets), "errors": len(state["errors"])}), flush=True)
    try:
        await asyncio.gather(*(tracked(qid, packet) for qid, packet in packets.items()))
    finally:
        await client.close()
    for path, expected in backup["file_hashes"].items(): assert file_hash(path) == expected, "An initial label or successful call changed"
    state.update(finished_at=utc(), complete=not state["errors"], prior_files_unchanged=True, actual_requests=request_stats())
    if state["complete"]:
        derived, manual = materialize(root, qa, output, protocol, gold, chunks, rows, reviews)
        state.update(stage="source_consistency_completed", effective_labels=str(derived), manual_skips=len(manual),
                     remaining_conflicts=len(read_json(derived / "cross_packet_consistency.json")["conflicts"]))
    else: state["stage"] = "source_consistency_incomplete"
    write_json(output / "progress.json", state)
    return 0 if state["complete"] else 2


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(r"D:\Hyper-rag-case2-backups\qa40_workspace\shared_retrieval_v1"))
    a = p.parse_args()
    raise SystemExit(asyncio.run(run(a.root)))


if __name__ == "__main__": main()
