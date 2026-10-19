"""Preserve v1 and repair references identified by source-level scientific review."""
import argparse
import asyncio
import copy
import hashlib
import json
import sys
from pathlib import Path

from scripts.pfas_qa_common import QAClient, digest, file_hash, read_json, utc, write_json
from scripts.verify_pfas_qa40 import independent_prompt, validate_audit, validate_supported


def span(chunks, cid, start, end=None):
    text = chunks[cid]["content"]
    pos = text.index(start)
    stop = pos + len(start) if end is None else text.index(end, pos + len(start)) + len(end)
    return {"chunk_id": cid, "quote": text[pos:stop]}


def proposals(gold, chunks):
    rows = {q["question_id"]: copy.deepcopy(q) for q in gold["qa_questions"]}

    def set_question(n, question, answer, point_specs, reason, typ=None):
        row = rows[f"PFAS40-Q{n:02d}"]
        row.update(question=question, reference_answer=answer,
                   point_support=[{"point": point, "evidence": evidence} for point, evidence in point_specs],
                   required_key_points=[point for point, _ in point_specs], refinement_reason=reason,
                   rationale=reason, decision="REVISE", answerable=True,
                   unsupported_claims=["Generalizing the study result to other PFAS, matrices, or conditions.",
                                       "Equating removal or fluoride release alone with complete carbon mineralization."],
                   support_mode="multi_study" if n == 22 else "single_study")
        if typ:
            row["question_type"] = typ
        return row

    q4 = rows["PFAS40-Q04"]
    e4a = q4["point_support"][0]["evidence"]
    e4b = [span(chunks, "PFAS_005_CHK_001", "of which e– dominated the PFOA degradation process.")]
    set_question(4, q4["question"],
                 "Under optimum conditions, the hybrid system reportedly achieved complete PFOA removal and more than 99% defluorination and TOC removal. Electrons were reported to dominate the piezocatalytic PFOA degradation process.",
                 [("Under optimum conditions the study reported complete PFOA removal, >99% defluorination and >99% TOC removal.", e4a),
                  ("Electrons were reported to dominate piezocatalytic PFOA degradation in this system.", e4b)],
                 "Omit the OCR-corrupted list of other active species; the requested dominant species is explicit.")
    q12 = rows["PFAS40-Q12"]
    q12["reference_answer"] = q12["reference_answer"].replace("This indicated that", "The authors interpreted this as indicating that")
    q12["required_key_points"][2] = "The authors described PEC alone as partial degradation into shorter-chain intermediates and PEC/PMS as promoting mineralization; the reported percentages do not demonstrate complete carbon mineralization."
    q12["point_support"][2]["point"] = q12["required_key_points"][2]
    q12.update(refinement_reason="Qualify mineralization as the authors' interpretation; avoid treating partial defluorination as proof of complete carbon mineralization.",
               rationale="Qualify the original author's interpretation and preserve the reported quantitative results.")
    q14 = rows["PFAS40-Q14"]
    q14["reference_answer"] = q14["reference_answer"].replace("complete destruction of the parent PFAS", "complete defluorination of all fluorinated species")
    q14.update(refinement_reason="Parent disappearance and destruction of all fluorinated products must remain distinct.",
               rationale="Correct the reference conclusion to incomplete overall defluorination.")
    e19 = [span(chunks, "PFAS_058_CHK_001", "For all experiments, the main mechanism of PFAS oxidation", "decomposition of 6:2 FTCA.")]
    set_question(19,
                 "In the BDD study of PFOA alternatives (PFBA, GenX and 6:2 FTCA), what initiating mechanism and radical contributions were reported?",
                 "The study attributed initiation primarily to direct electron transfer at the anode. Sulfate radicals contributed to oxidation of all tested PFAS, while hydroxyl radicals contributed only to 6:2 FTCA decomposition.",
                 [("Direct electron transfer at the anode was reported as the main initiating mechanism.", e19),
                  ("Sulfate radicals contributed to oxidation of all PFAS tested in that study.", e19),
                  ("Hydroxyl-radical participation was reported only for 6:2 FTCA decomposition in those experiments.", e19)],
                 "Replace a ROS experiment on fluorescent whitening agents that was incorrectly used as a PFAS mechanism question.", "mechanism_chain")
    e21 = [span(chunks, "PFAS_058_CHK_001", "The results indicated the significance of chain length and structure", "within 120 min of electrolysis).")]
    set_question(21,
                 "After 120 min of electrolysis in the BDD/Na2SO4 study, how did the reported degradability of PFBA, GenX, PFOA and 6:2 FTCA compare?",
                 "Reported degradation was PFBA 65.6 ± 5.0%, GenX 84.9 ± 3.3%, PFOA 97.9 ± 0.1%, and 6:2 FTCA 99.4 ± 0.0%, in ascending order, after 120 min. This comparison was study-specific and reflected both chain length and molecular structure.",
                 [("After 120 min, PFBA degradation was 65.6 ± 5.0% and GenX degradation was 84.9 ± 3.3%.", e21),
                  ("At that time, PFOA degradation was 97.9 ± 0.1% and 6:2 FTCA degradation was 99.4 ± 0.0%.", e21),
                  ("The observed order was PFBA < GenX < PFOA < 6:2 FTCA in that BDD study, attributed to chain length and structure.", e21)],
                 "Replace the review's internally contradictory PFHxS short-chain classification with a primary-study structural comparison.", "target_numeric_comparison")
    e22a = [span(chunks, "PFAS_004_CHK_001", "PTFE achieved 93.4 % PFOA removal and 91.5 % defluorination efficiency in 1 h.")]
    e22b = [span(chunks, "PFAS_012_CHK_001", "The research demonstrates a substantial 90.5% degradation and 29% defluorination of PFOS after 6 h of treatment", ".")]
    set_question(22,
                 "Compare the reported parent-removal/degradation and defluorination outcomes for PTFE treating PFOA (1 h) and BaTiO3 treating PFOS (6 h). What differences prevent a controlled comparison of catalyst superiority?",
                 "PTFE/PFOA was reported at 93.4% parent removal and 91.5% defluorination after 1 h; BaTiO3/PFOS at 90.5% degradation and 29% defluorination after 6 h. The targets and treatment durations differ, so these results are separate experimental outcomes and do not establish an intrinsic catalyst ranking under matched conditions.",
                 [("PTFE treating PFOA showed 93.4% removal and 91.5% defluorination after 1 h.", e22a),
                  ("BaTiO3 treating PFOS showed 90.5% degradation and 29% defluorination after 6 h.", e22b),
                  ("Different PFAS targets and durations prevent interpreting these two outcomes as a matched-condition comparison of catalyst superiority.", e22a + e22b)],
                 "Add a true cross-study comparison with explicit target and time bindings; its limitation is a stated inference from the documented mismatched conditions.", "cross_study_comparison")
    changed = [rows[f"PFAS40-Q{i:02d}"] for i in (4, 12, 14, 19, 21, 22)]
    for row in changed:
        row["unsupported_claims"] = ["A universal PFAS treatment or catalyst ranking independent of experimental conditions.",
                                    "Complete carbon mineralization established by fluoride release or parent disappearance alone."]
        row["required_key_points"] = [p["point"] for p in row["point_support"]]
    return changed


async def run(output):
    old = read_json(output / "qa_gold.json")
    chunks = read_json(old["source"]["chunks"])
    target = output / "gold_v2"
    target.mkdir(exist_ok=True)
    proposed = proposals(old, chunks)
    client = QAClient(target)

    async def audit(row):
        validate_supported(row, chunks, chunks)
        points = row["required_key_points"]
        result = await client.json(independent_prompt(row, chunks), role="judge",
                                   validator=lambda v: validate_audit(v, points), label=row["question_id"] + ":refined_audit")
        write_json(target / "reviews" / (row["question_id"] + ".json"), {"proposed": row, "audit": result})
        if not result["accepted"]:
            raise ValueError("Refined gold review rejected: " + row["question_id"])
        evidence = []
        for point in row["point_support"]:
            for e in point["evidence"]:
                cid, quote = e["chunk_id"], e["quote"]
                ev = {**e, "doc_id": chunks[cid]["source_doc_id"], "source_file": chunks[cid]["source_file"],
                      "start_char": chunks[cid]["content"].index(quote),
                      "quote_sha256": hashlib.sha256(quote.encode()).hexdigest(),
                      "chunk_content_sha256": hashlib.sha256(chunks[cid]["content"].encode()).hexdigest()}
                ev["end_char"] = ev["start_char"] + len(quote)
                if ev not in evidence:
                    evidence.append(ev)
        return {**row, "evidence": evidence, "gold_chunk_ids": sorted({e["chunk_id"] for e in evidence}),
                "source_doc_ids": sorted({e["doc_id"] for e in evidence}), "audit": result,
                "review_status": "machine_verified_after_scientific_source_correction", "human_confirmed": False}

    try:
        revised = await asyncio.gather(*(audit(r) for r in proposed))
    finally:
        await client.close()
    replacements = {r["question_id"]: r for r in revised}
    questions = [replacements.get(q["question_id"], q) for q in old["qa_questions"]]
    payload = {**old, "revision": 2, "parent_gold_sha256": file_hash(output / "qa_gold.json"),
               "qa_questions": questions,
               "refinement": {"changed_questions": list(replacements), "checked_at": utc(),
                              "historical_v1_preserved": True,
                              "provenance": "agent source-level correction and separate LLM audit; no human confirmation"}}
    write_json(target / "qa_gold.json", payload)
    old_freeze = read_json(output / "freeze_manifest.json")
    docs = sorted({d for q in questions if q["answerable"] for d in q["source_doc_ids"]})
    freeze = {**old_freeze, "revision": 2, "gold_sha256": file_hash(target / "qa_gold.json"),
              "supported_source_documents": docs, "supported_document_count": len(docs), "frozen_at": utc(),
              "parent_gold_sha256": payload["parent_gold_sha256"],
              "negative_audits_directory": str(output / "absence_audits")}
    write_json(target / "freeze_manifest.json", freeze)
    lines = ["# PFAS40 v2 reference review", "", "Machine reviewed; no human confirmation is claimed.", ""]
    for q in questions:
        lines += ["## " + q["question_id"], "", q["question"], "", "Reference: " + q["reference_answer"], "", "Scoring points:", ""]
        lines += ["- " + p for p in q["required_key_points"]]
        for e in q.get("evidence", []):
            lines += ["", e["chunk_id"], "", "> " + e["quote"].replace("\n", "\n> ")]
        lines += [""]
    (target / "qa_gold_review.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(freeze), flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    asyncio.run(run(parser.parse_args().output))
