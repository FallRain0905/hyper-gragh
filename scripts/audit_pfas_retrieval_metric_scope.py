"""Apply one question-defined parent-outcome scope consistently across its pool."""
import asyncio
import json
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, read_json, write_json, file_hash, digest, utc
from scripts.evaluate_pfas_shared_retrieval import prepare, annotation_packet
from scripts.adjudicate_pfas_shared_retrieval import (
    ADJUDICATION_RULES, remap_spans, validate_review, materialize,
)
from scripts.run_pfas_qa40 import request_stats

SCOPE_POLICY = """
QUESTION-DEFINED METRIC SCOPE: This question explicitly permits the alternative
labels 'parent-removal/degradation' for the reported parent-compound outcome.
For that parent-outcome component, an accurately reported parent degradation
result is within the permitted scope; do not reject it merely because the raw
source calls it 'degradation' whereas the rubric uses 'removal'. Retain the exact
reported metric wording in the source-based explanation. All target, material,
time, numerical value and other components of the point still must be supported.
This permission is asymmetric: generic removal/adsorption does not establish
chemical degradation. Parent disappearance does not establish defluorination or
carbon mineralization. Their separate values and meanings remain mandatory.
Scientific paraphrase and valid entailment are allowed; literal phrase presence
is not a requirement. Do not change the frozen question, rubric or reference.
Review every pooled chunk and every distinct top5 source set for this question,
irrespective of its system or prior grade. Only the selected parent-outcome
rubric point is in scope; other point fields remain frozen.
"""


def scope_selection(gold):
    selected = {}
    for q in gold["qa_questions"]:
        if "parent-removal/degradation" not in q["question"].casefold(): continue
        ids = [i for i, p in enumerate(q["required_key_points"]) if "removal" in p.casefold()]
        if ids: selected[q["question_id"]] = ids
    return selected


def scope_packet(q, point_ids, rows, chunks):
    groups = {}
    for key, row in rows.items():
        if row["question_id"] != q["question_id"]: continue
        canonical = key if key.startswith("pool/") else "sets/" + digest(sorted(row["chunk_ids"]))[:24]
        target = groups.setdefault(canonical, {"target_id": canonical, "base_key": key, "aliases": [],
                                              "chunk_ids": row["chunk_ids"], "disputed_point_ids": point_ids})
        target["aliases"].append(key)
    packet = annotation_packet(q, sorted({cid for t in groups.values() for cid in t["chunk_ids"]}), chunks)
    packet["targets"] = sorted(groups.values(), key=lambda t: t["target_id"])
    for t in packet["targets"]:
        base = rows[t["base_key"]]
        assert all(rows[k]["annotation"] == base["annotation"] for k in t["aliases"])
        local = annotation_packet(q, base["chunk_ids"], chunks)
        t["prior_annotation"], _ = remap_spans(base["annotation"], local["RAW_SPAN_CATALOG"], packet["RAW_SPAN_CATALOG"])
        t["allowed_span_ids"] = [sid for sid, s in packet["RAW_SPAN_CATALOG"].items() if s["chunk_id"] in t["chunk_ids"]]
    packet["selection_reason"] = "The frozen question explicitly groups parent-removal/degradation; audit every source packet under that scope, not only any particular system's evidence."
    return packet


async def run():
    root = Path(r"D:\Hyper-rag-case2-backups\qa40_workspace\shared_retrieval_v1")
    qa = root.parent
    base = root / "source_consistency_v1/effective_labels"
    output = root / "metric_scope_v1"
    output.mkdir(exist_ok=True)
    pointer = read_json(root / "latest_scope_backup.json")
    assert file_hash(pointer["manifest"]) == pointer["sha256"]
    backup = read_json(pointer["manifest"])
    assert backup["complete"] and backup["readback_verified"]
    protocol, gold, chunks, pool, sets, _ = prepare(base, qa)
    rows = {"pool/" + r["question_id"] + "__" + r["chunk_id"]: read_json(base / "pool" / (r["question_id"] + "__" + r["chunk_id"] + ".json")) for r in pool}
    rows.update({"sets/" + sid: read_json(base / "sets" / (sid + ".json")) for sid in sets})
    questions = {q["question_id"]: q for q in gold["qa_questions"]}
    selection = scope_selection(gold)
    packets = {qid: scope_packet(questions[qid], ids, rows, chunks) for qid, ids in selection.items()}
    rules = ADJUDICATION_RULES + "\n" + SCOPE_POLICY
    p = {"version": "pfas-question-defined-parent-outcome-scope-v1", "base": str(base), "selection": selection,
         "selection_by_frozen_question_only": True, "rules_sha256": digest(rules),
         "base_label_hashes": {key: file_hash(base / (key + ".json")) for key in rows},
         "input_hashes": {qid: digest(packet) for qid, packet in packets.items()}, "human_confirmed": False}
    if (output / "protocol.json").exists(): assert read_json(output / "protocol.json") == p
    else: write_json(output / "protocol.json", p)
    state = {"stage": "parent_outcome_scope_review", "started_at": utc(), "queries_total": len(packets),
             "queries_done": 0, "targets": sum(len(p["targets"]) for p in packets.values()), "errors": [], "complete": False}
    write_json(output / "progress.json", state)
    client, reviews = QAClient(output), {}
    try:
        for qid, packet in packets.items():
            path = output / "reviews" / (qid + ".json")
            signature = digest({"input": packet, "protocol": p})
            if path.exists():
                saved = read_json(path); assert saved["signature"] == signature
                value = saved["result"]; validate_review(value, packet, rows)
            else:
                error = ""
                for budget in (4096, 8192, 16384):
                    prompt = rules + ("\nPrevious technical validation category (no rejected answer shown): " + error if error else "")
                    prompt += "\nINPUT:\n" + json.dumps(packet, ensure_ascii=False)
                    try:
                        value = await client.json(prompt, role="judge", validator=lambda v: validate_review(v, packet, rows),
                                                  label="metric-scope:" + qid, budgets=(budget,))
                        break
                    except RuntimeError:
                        audit = [json.loads(x) for x in (output / "request_audit.jsonl").read_text(encoding="utf-8").splitlines()]
                        error = audit[-1].get("validation_error") or "Transient request failure"
                else: raise RuntimeError("Metric scope review exhausted bounded strict attempts")
                write_json(path, {"signature": signature, "input": packet, "result": value, "at": utc(), "human_confirmed": False})
            reviews[qid] = {"input": packet, "result": value}
            state["queries_done"] += 1
            state.update(updated_at=utc(), actual_requests=request_stats())
            write_json(output / "progress.json", state)
    finally:
        await client.close()
    for path, expected in backup["file_hashes"].items(): assert file_hash(path) == expected
    derived, manual = materialize(base, qa, output, protocol, gold, chunks, rows, reviews)
    state.update(stage="metric_scope_completed", finished_at=utc(), complete=True, prior_files_unchanged=True,
                 effective_labels=str(derived), manual_skips=len(manual), actual_requests=request_stats(),
                 remaining_conflicts=len(read_json(derived / "cross_packet_consistency.json")["conflicts"]))
    write_json(output / "progress.json", state)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    asyncio.run(run())
