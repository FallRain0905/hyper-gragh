"""Build an auditable PFAS40 draft from frozen raw chunks.

The file is generated without querying an LLM. Every supported item is bound to
an exact source span and every negative item gets an initial corpus-wide
search audit. These searches are not proof of absence. This keeps construction independent of graph-derived
aggregates and never writes to a build cache.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT.parent / "case2_pfas_build"
CORPUS = ROOT.parent / "case2_pfas_corpus_60"
OUT = BUILD / "diagnostics" / "qa40_pfas_v1"
CHUNKS = BUILD / "hyper_final" / "kv_store_text_chunks.json"
MANIFEST = CORPUS / "corpus_manifest.jsonl"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def q(qid, question, answer, points, anchor, *, typ, level, docs=None,
      unsupported=None, scope="primary_treatment", answerable=True):
    return {
        "question_id": qid,
        "question": question,
        "question_type": typ,
        "difficulty": level,
        "scope": scope,
        "answerable": answerable,
        "gold_label": "supported" if answerable else "unanswerable",
        "reference_answer": answer,
        "required_key_points": points,
        "unsupported_claims": unsupported or [],
        "quote_anchor": anchor,
        "expected_doc_ids": docs or [],
    }


QUESTIONS = [
q("PFAS40-Q01", "Under the FMC piezoremediation experiment, what PFAS removal was achieved and after how long?", "FMC removed 91.6% of PFAS from the soil after 50 min.", ["FMC", "91.6% PFAS removal", "50 min"], "FMC exhibited significantly higher piezoremediation performance", typ="direct_numeric", level="L1", docs=["PFAS_003"]),
q("PFAS40-Q02", "In the FMC soil experiment, how did defluorination compare with PFAS removal at 50 min?", "At 50 min, defluorination reached 64.3%, lower than the corresponding 91.6% PFAS removal.", ["64.3% defluorination", "91.6% removal", "defluorination is lower"], "defluorination efficiency gradually increases with time and reaches 64.3%", typ="metric_comparison", level="L2", docs=["PFAS_003"]),
q("PFAS40-Q03", "What PFOA removal and defluorination efficiencies did PTFE achieve in one hour?", "PTFE achieved 93.4% PFOA removal and 91.5% defluorination in 1 h.", ["93.4% PFOA removal", "91.5% defluorination", "1 h"], "PTFE achieved 93.4 % PFOA removal", typ="direct_numeric", level="L1", docs=["PFAS_004"]),
q("PFAS40-Q04", "What did the FMC-pipe/CIS hybrid system achieve for PFOA and TOC, and which active species dominated?", "Under optimum conditions it achieved complete PFOA removal, over 99% defluorination and TOC removal; electrons dominated the PFOA degradation process.", ["complete PFOA removal", ">99% defluorination", ">99% TOC removal", "electrons were dominant"], "Under the optimum conditions, the hybrid system achieved complete PFOA removal", typ="multi_metric_mechanism", level="L4", docs=["PFAS_005"]),
q("PFAS40-Q05", "What degradation and defluorination did BaTiO3 piezocatalysis achieve for PFOS after 6 h?", "It achieved 90.5% PFOS degradation and 29% defluorination after 6 h, with stepwise chain shortening indicated by products.", ["90.5% degradation", "29% defluorination", "6 h", "stepwise chain shortening"], "substantial 90.5% degradation and 29% defluorination", typ="direct_numeric", level="L2", docs=["PFAS_012"]),
q("PFAS40-Q06", "Which PFAS targets were tested in the US/PTFE contact-electro-catalytic system, and how did the non-PFOA targets perform qualitatively?", "The system tested PFOA, PFOS, 6:3-FTCA, HFPO-DA and PFBS; PFOS, PFBS, 6:3-FTCA and HFPO-DA were also degraded but at lower efficiency, with equivalent defluorination ratios.", ["five targets identified", "non-PFOA targets had lower degradation efficiency", "equivalent defluorination ratios"], "The US/PTFE system was also applicable for degrading PFOS", typ="target_comparison", level="L3", docs=["PFAS_008"]),
q("PFAS40-Q07", "For the US/PTFE system, what fluoride release and defluorination-ratio range were reported across five PFAS?", "Average fluoride release was 14.6, 14.9, 11.8, 10.6 and 7.9 mol F− per mol degraded for PFOA, PFOS, 6:3-FTCA, HFPO-DA and PFBS, respectively, corresponding to 87.6–97.3% defluorination.", ["five fluoride-release values in target order", "87.6–97.3% range", "values are per mole degraded"], "14.6, 14.9, 11.8, 10.6 and 7.9", typ="multi_numeric", level="L4", docs=["PFAS_008"]),
q("PFAS40-Q08", "What treatment challenge and outcome are reported for UV/S–EO treatment of AFFF?", "The process addressed complex AFFF matrices and achieved near-complete defluorination and mineralization of most PFAS and organics at ambient temperature and pressure.", ["AFFF is a complex organic matrix", "near-complete defluorination", "near-complete mineralization", "ambient temperature and pressure"], "At ambient temperature and pressure, The UV/S−EO realized near-complete defluorination", typ="application_synthesis", level="L4", docs=["PFAS_020"]),
q("PFAS40-Q09", "What dual-electron mechanism was proposed for the Pd-decorated TiO2 cathode treating PFOS?", "Cathodic potentials promote PFAS adsorption on TiO2, while UV254-excited Pd sites generate hot electrons that directly cleave C–F bonds or form hydrated electrons for indirect reduction.", ["cathodic adsorption on TiO2", "UV254-excited Pd hot electrons", "direct C–F cleavage or hydrated-electron reduction"], "cathodic potentials promote PFAS adsorption on TiO2", typ="mechanism_chain", level="L5", docs=["PFAS_013"]),
q("PFAS40-Q10", "Under what conditions was PFOS completely defluorinated in the visible-LED photocatalysis study?", "PFOS was completely defluorinated within 8 h under 405-nm LED irradiation.", ["PFOS", "complete defluorination", "8 h", "405 nm LED"], "PFOS was completely defluorinated within 8-h irradiation of 405-nm LED light", typ="condition_constrained", level="L2", docs=["PFAS_032"]),
q("PFAS40-Q11", "What PFOS degradation and defluorination were obtained with 2% Fe-ZnO piezo-photocatalytic PMS activation?", "The process achieved 96% PFOS degradation in 90 min and about 26.1% defluorination; both radical and non-radical pathways were discussed.", ["96% PFOS degradation", "90 min", "about 26.1% defluorination", "radical and non-radical pathways"], "2 % Fe-ZnO achieved degradation efficiencies of 92 % for methylene blue", typ="multi_metric_mechanism", level="L3", docs=["PFAS_021"]),
q("PFAS40-Q12", "How did adding PMS change the interpretation of the PEC treatment of PFOA?", "PEC alone produced only partial degradation into shorter-chain intermediates, whereas PEC plus PMS promoted complete mineralization.", ["PEC alone partial degradation", "shorter-chain intermediates", "PEC/PMS promoted complete mineralization"], "These results confirmed that the PEC process alone achieved only partial degradation", typ="mechanism_comparison", level="L3", docs=["PFAS_002"]),
q("PFAS40-Q13", "Which shorter-chain products were reported during PFOA degradation before complete defluorination?", "The pathway produced PFHxA, PFPeA, PFBA and PFPrA as shorter-chain intermediates before complete defluorination.", ["PFHxA", "PFPeA", "PFBA", "PFPrA", "complete defluorination follows"], "PFHxA", typ="pathway_retrieval", level="L3", docs=["PFAS_002"]),
q("PFAS40-Q14", "Why should removal/degradation and defluorination be reported separately in PFAS treatment?", "Removal or degradation tracks disappearance of the parent PFAS, whereas defluorination tracks C–F cleavage and fluoride release; the two can differ substantially, as shown by 91.6% removal versus 64.3% defluorination in the FMC study.", ["removal/degradation and defluorination are distinct metrics", "defluorination reflects C–F cleavage/fluoride release", "the metrics can diverge", "FMC example 91.6% versus 64.3%"], "Considering the high fluorination of PFAS", typ="mechanism_explanation", level="L5", docs=["PFAS_003"]),
q("PFAS40-Q15", "How did MC and FMC compare for PFAS removal from the co-contaminated soil?", "MC removed 74.8% and FMC removed 91.6% of PFAS.", ["MC 74.8%", "FMC 91.6%", "same PFAS soil-remediation comparison"], "74.8% and 91.6% of PFAS are removed", typ="comparison", level="L2", docs=["PFAS_003"]),
q("PFAS40-Q16", "How did dissolved oxygen affect PFAS removal in the FMC experiment?", "Removal was 79.7% under N2 compared with 91.6% in air within 50 min, indicating a dissolved-oxygen effect.", ["79.7% under N2", "91.6% in air", "within 50 min"], "79.7% removal under", typ="condition_comparison", level="L3", docs=["PFAS_003"]),
q("PFAS40-Q17", "What pretreatment was used to reach adsorption–desorption equilibrium before FMC/MC piezoremediation?", "The granules were stirred at 100 rpm for 120 min to reach adsorption–desorption equilibrium.", ["100 rpm", "120 min", "adsorption–desorption equilibrium"], "stirred (100 rpm, 120 min)", typ="condition_retrieval", level="L2", docs=["PFAS_003"]),
q("PFAS40-Q18", "What operating point was reported for efficient contact-electro-catalytic PFAS treatment, and what did ultrasound alone do?", "The reaction proceeded efficiently at 40 kHz and 0.3 W cm−2, whereas ultrasound alone caused negligible degradation.", ["40 kHz", "0.3 W cm−2", "ultrasound alone negligible degradation"], "reaction proceeds efficiently at 40 kHz and 0.3 W", typ="condition_comparison", level="L3", docs=["PFAS_006"]),
q("PFAS40-Q19", "Which reactive oxygen species were identified as central to contact-electro-catalytic pollutant degradation?", "Hydroxyl radicals, singlet oxygen and superoxide radicals were identified as reactive oxygen species generated at solid–liquid interfaces.", ["hydroxyl radicals", "singlet oxygen", "superoxide radicals", "solid–liquid charge transfer context"], "generating reactive oxygen species (ROS) such as", typ="mechanism_retrieval", level="L3", docs=["PFAS_001"]),
q("PFAS40-Q20", "What interfacial charge-transfer change was associated with the MoSe2/TiO2 heterostructure?", "A positive Efb shift indicated electron transfer from TiO2 to MoSe2, producing electron accumulation in MoSe2 and hole accumulation at the TiO2 interface.", ["electron transfer TiO2 to MoSe2", "electron accumulation in MoSe2", "hole accumulation at TiO2"], "positive", typ="mechanism_chain", level="L5", docs=["PFAS_002"]),
q("PFAS40-Q21", "Which PFAS are classified as long-chain versus short-chain in the review evidence?", "PFOA and PFOS are long-chain; PFBS and PFHxS are short-chain PFAS.", ["PFOA/PFOS long-chain", "PFBS/PFHxS short-chain"], "PFOA) and perfluorooctane sulfonate", typ="taxonomy", level="L2", docs=["PFAS_014"]),
q("PFAS40-Q22", "What chain-length trend in degradation is stated in the review evidence?", "The evidence states that degradation is chain-length dependent: long-chain PFAS perform better, while short-chain PFAS are more resistant.", ["chain-length dependence", "long-chain better", "short-chain more resistant"], "Degradation rate is chain-length dependent", typ="trend_analysis", level="L3", docs=["PFAS_014"]),
q("PFAS40-Q23", "What design features and application result are reported for ionic fluorogels?", "Ionic fluorogels combine ionic and fluorous components, remove 21 legacy and emerging PFAS from natural water, can be regenerated, and one material outperformed a commercial ion-exchange resin for short-chain PFAS in column tests.", ["ionic plus fluorous components", "21 PFAS", "natural water", "regeneration", "short-chain column advantage"], "a class of polymer networks with a synergistic combination", typ="adsorbent_synthesis", level="L4", docs=["PFAS_029"]),
q("PFAS40-Q24", "What GenX performance and regeneration results were reported for the magnetic fluorinated polymer sorbent?", "GenX removal exceeded 99% within 30 s, the estimated Langmuir capacity was 219 mg g−1, and regeneration was demonstrated over four cycles.", [">99% GenX removal", "30 s", "219 mg g−1", "four cycles"], "The removal of the ammonium salt of hexafluoropropylene oxide dimer acid", typ="multi_numeric", level="L3", docs=["PFAS_030"]),
q("PFAS40-Q25", "How did reducing TFN-CDP nitriles change PFAS adsorption performance?", "Reduction reversed the charge affinity toward anionic MPs/PFAS; the reduced polymer removed 80–98% of ten anionic PFAS after 30 min and outperformed commercial granular activated carbon.", ["charge-affinity reversal", "10 anionic PFAS", "80–98% after 30 min", "better than GAC"], "Kinetic studies of the removal of 10 anionic PFAS", typ="adsorbent_comparison", level="L4", docs=["PFAS_026"]),
q("PFAS40-Q26", "What material and mechanism were reported for selective PFAS adsorption on hydrophobic zeolite Beta?", "A hydrophobic all-silica zeolite Beta was proposed as a selective, high-capacity PFAS adsorbent; adsorption was driven by a very negative adsorption enthalpy and favorable steric factors.", ["hydrophobic all-silica zeolite Beta", "selective high-capacity PFAS adsorption", "negative adsorption enthalpy", "steric factors"], "hydrophobic, all-silica zeolite Beta material", typ="adsorbent_mechanism", level="L3", docs=["PFAS_027"]),
q("PFAS40-Q27", "At acidic pH in the coagulation study, what approximate removal ratios were reported for PFOA and PFOS?", "At pH 4, the reported removal ratios were approximately 47.6% for PFOA and 94.7% for PFOS.", ["pH 4", "about 47.6% PFOA", "about 94.7% PFOS"], "Coagulation achieved high removal ratios", typ="condition_numeric", level="L3", docs=["PFAS_015"]),
q("PFAS40-Q28", "What did the electrochemical landfill-leachate study investigate and which PFAS were its focus?", "It investigated electrochemical oxidation of PFOA and PFOS in landfill leachates using low- and highly boron-doped diamond electrodes.", ["landfill leachate matrix", "PFOA and PFOS", "electrochemical oxidation", "two BDD doping levels"], "Electrochemical oxidation of PFOA and PFOS in landfill leachates", typ="application_retrieval", level="L2", docs=["PFAS_018"]),
q("PFAS40-Q29", "Why are AFFF-impacted groundwater concentrations important when interpreting electrochemical PFAS treatment kinetics?", "The study notes that degradation kinetics can differ substantially at the lower concentrations typical of AFFF-impacted sites, so high-concentration laboratory results may not transfer directly.", ["AFFF-impacted groundwater", "lower environmentally typical concentrations", "kinetics can differ substantially", "transfer requires caution"], "Degradation kinetics may be substantially different", typ="transferability", level="L4", docs=["PFAS_025"]),
 q("PFAS40-Q30", "What transformation pathway was proposed for PFOS in the mediated electrochemical study?", "PFOS was converted primarily to PFOA and other shorter-chain carboxylates through radical desulfonation and hydroxide coupling, followed by mineralization under low-temperature DMSO/NaOH conditions.", ["PFOS to PFOA", "shorter-chain carboxylates", "radical desulfonation/hydroxide coupling", "subsequent mineralization"], "formation of perfluorooctanoic acid", typ="pathway_mechanism", level="L5", docs=["PFAS_043"]),
q("PFAS40-Q31", "How were removal and defluorination partitioned in the graphene-sponge electrochemical study?", "For C4–C8 PFAS, removal was 16.7–67% and defluorination was 8–24%; removal was attributed to electrosorption plus electrooxidation, while fluoride recovery relative to the electrooxidized fraction was 74–87%.", ["16.7–67% removal", "8–24% defluorination", "electrosorption/electrooxidation contributions", "74–87% fluoride recovery relative to electrooxidized fraction"], "Removal efficiencies, obtained in low conductivity electrolyte", typ="metric_decomposition", level="L5", docs=["PFAS_049"]),
q("PFAS40-Q32", "What PFOA performance and proposed electrode property were reported for the F-doped Ti/SnO2 electrode?", "The F-doped electrode decomposed over 99% of PFOA in 30 min; F incorporation was proposed to raise oxygen-evolution potential and generate weakly adsorbed hydroxyl radicals.", [">99% PFOA decomposition", "30 min", "higher oxygen-evolution potential", "weakly adsorbed OH radicals"], "could decomposed over 99% of PFOA", typ="material_mechanism", level="L4", docs=["PFAS_050"]),
q("PFAS40-Q33", "Which factors were most important for PFOA degradation in the BDD factorial-design study?", "Current density and treatment time were the most important factors for PFOA degradation; the design also examined initial PFAS concentration, electrolyte concentration and interactions.", ["current density", "treatment time", "factorial design", "other factors examined"], "current density and time were the most important factors", typ="design_of_experiments", level="L4", docs=["PFAS_048"]),
q("PFAS40-Q34", "What practical limitations of TiO2 photocatalysis for PFAS remediation are highlighted in the review?", "Rapid electron–hole recombination, limited visible-light absorption and pH-dependent surface charge constrain TiO2; acidic conditions may be needed, complicating scale-up.", ["electron–hole recombination", "limited visible-light absorption", "pH-dependent surface charge", "acidic-condition/scale-up limitation"], "limited by rapid electron-hole recombination", typ="limitations", level="L4", docs=["PFAS_060"]),
q("PFAS40-Q35", "Which solution-chemistry and operating variables are identified as influencing hydrated-electron PFAS reduction?", "The review identifies pH, sulfite/iodide dose, dissolved oxygen, humic acid, nitrate and temperature as influential variables.", ["pH", "sulfite/iodide dose", "dissolved oxygen", "humic acid", "nitrate", "temperature"], "considerably influenced by solution chemistry parameters", typ="factor_synthesis", level="L4", docs=["PFAS_045"]),
q("PFAS40-Q36", "What is the exact PFOA removal percentage at 25 °C, pH 7.0, 40 kHz and 0.3 W cm−2 using FMC?", "I don't know based on the retrieved evidence: the frozen corpus does not provide this exact combined condition/value record.", [], "__ABSENCE__25C_pH7_FMC", typ="unanswerable_exact_combination", level="L5", answerable=False, scope="negative_audit"),
q("PFAS40-Q37", "What is the experimentally measured PFOS half-life for the US/PTFE system at 25 °C and pH 7.00?", "I don't know based on the retrieved evidence: this exact half-life under the stated combined conditions is not reported in the frozen corpus.", [], "__ABSENCE__PFOS_half_life_25C_pH7", typ="unanswerable_exact_value", level="L5", answerable=False, scope="negative_audit"),
q("PFAS40-Q38", "What is the optimum catalyst mass in grams that maximizes GenX removal in the four-cycle fluorogel experiment?", "I don't know based on the retrieved evidence: the frozen corpus does not establish that exact optimum mass for the four-cycle GenX experiment.", [], "__ABSENCE__GenX_optimum_mass", typ="unanswerable_exact_value", level="L4", answerable=False, scope="negative_audit"),
q("PFAS40-Q39", "What is the exact energy consumption in kWh m−3 for the FMC/AFFF UV/S–EO hybrid at complete defluorination?", "I don't know based on the retrieved evidence: the frozen corpus does not report that exact energy value for this combined system and endpoint.", [], "__ABSENCE__FMC_AFFF_energy", typ="unanswerable_exact_value", level="L5", answerable=False, scope="negative_audit"),
q("PFAS40-Q40", "What p-value proves that PFBA is statistically easier to defluorinate than PFBS in the 60-paper corpus?", "I don't know based on the retrieved evidence: no such corpus-wide p-value is reported in the frozen literature.", [], "__ABSENCE__PFBA_PFBS_pvalue", typ="unanswerable_statistical_claim", level="L6", answerable=False, scope="negative_audit"),
]


def sentence_context(text: str, anchor: str) -> str:
    if anchor not in text:
        raise ValueError("anchor not found: " + anchor)
    if anchor.startswith("__ABSENCE__"):
        return ""
    pos = text.index(anchor)
    left = max(text.rfind("\n\n", 0, pos), text.rfind(". ", 0, pos), text.rfind("。", 0, pos))
    left = 0 if left < 0 else left + (2 if text[left:left+2] == ". " else 2 if text[left:left+2] == "\n\n" else 1)
    rights = [x for x in (text.find("\n\n", pos), text.find(". ", pos + len(anchor)), text.find("。", pos + len(anchor))) if x >= 0]
    right = min(rights) if rights else min(len(text), pos + 900)
    quote = text[left:right].strip()
    if len(quote) < 40:
        quote = text[pos:min(len(text), pos + 700)].strip()
    return quote[:1600]


def main():
    chunks = json.loads(CHUNKS.read_text(encoding="utf-8-sig"))
    manifest_rows = [json.loads(x) for x in MANIFEST.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
    manifest = {r["doc_id"]: r for r in manifest_rows}
    out_questions = []
    for item in QUESTIONS:
        if item["answerable"]:
            matches = [(cid, row) for cid, row in chunks.items()
                       if item["quote_anchor"].lower() in str(row.get("content", "")).lower()
                       and (not item["expected_doc_ids"] or row.get("source_doc_id") in item["expected_doc_ids"])]
            if not matches:
                raise ValueError(f"no chunk for {item['question_id']}: {item['quote_anchor']}")
            cid, row = matches[0]
            text = row["content"]
            # Preserve the exact source spelling by locating case-insensitively.
            pos = text.lower().index(item["quote_anchor"].lower())
            anchor = text[pos:pos + len(item["quote_anchor"])]
            quote = sentence_context(text, anchor)
            evidence = [{"chunk_id": cid, "doc_id": row.get("source_doc_id"), "source_file": row.get("source_file"), "quote": quote, "quote_sha256": hashlib.sha256(quote.encode()).hexdigest()}]
            docs = sorted({row.get("source_doc_id")})
            if item["expected_doc_ids"] and not set(item["expected_doc_ids"]).issubset(set(docs)):
                raise ValueError(f"doc mismatch {item['question_id']}: {docs}")
            item = {**item, "gold_chunk_ids": [cid], "evidence": evidence, "expected_doc_ids": docs, "source_scope": row.get("source_doc_id")}
        else:
            corpus_text = "\n".join(str(v.get("content") or "") for v in chunks.values())
            # Negative audit searches the exact combined-condition/value phrase;
            # it is deliberately recorded so a reviewer can challenge it.
            patterns = {
                "__ABSENCE__25C_pH7_FMC": r"25\s*(?:°|\\circ)?\s*C.{0,100}pH\s*[=:]?\s*7.{0,100}40\s*kHz.{0,100}0\.3\s*W",
                "__ABSENCE__PFOS_half_life_25C_pH7": r"PFOS.{0,80}(?:half[- ]life|half life).{0,80}25.{0,30}pH\s*7",
                "__ABSENCE__GenX_optimum_mass": r"GenX.{0,100}(?:optimum|optimal).{0,80}(?:mass|g)",
                "__ABSENCE__FMC_AFFF_energy": r"FMC.{0,100}AFFF.{0,100}(?:energy|kWh)",
                "__ABSENCE__PFBA_PFBS_pvalue": r"PFBA.{0,100}PFBS.{0,100}p[- ]?value",
            }
            pattern = patterns[item["quote_anchor"]]
            hits = list(re.finditer(pattern, corpus_text, re.I | re.S))
            item = {**item, "gold_chunk_ids": [], "evidence": [], "absence_audit": {"pattern": pattern, "matches": len(hits), "corpus_chunks": len(chunks), "audited_cache_sha256": sha(CHUNKS)}}
            if hits:
                raise ValueError(f"negative audit matched {item['question_id']}")
        item.pop("quote_anchor", None)
        out_questions.append(item)
    payload = {
        "benchmark_id": "case2-pfas-qa40-v1",
        "title": "HyperChE Case 2 PFAS 40-question grounded benchmark",
        "status": "draft_requires_claim_and_absence_review",
        "human_confirmed": False,
        "protocol_version": "independent-pfas-qa40-v1",
        "gold_construction": "raw_chunk_exact_span; no graph-derived gold; no liquid-flow-battery questions",
        "answerable_count": sum(bool(x["answerable"]) for x in out_questions),
        "unanswerable_count": sum(not bool(x["answerable"]) for x in out_questions),
        "source": {"chunks": str(CHUNKS), "chunks_sha256": sha(CHUNKS), "manifest": str(MANIFEST), "manifest_sha256": sha(MANIFEST), "documents": 60, "chunks_count": len(chunks)},
        "qa_questions": out_questions,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "qa_questions.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {"status": "DRAFT", "anchor_location_passed": True, "claim_support_verified": False, "absence_verified": False, "question_count": len(out_questions), "answerable": payload["answerable_count"], "unanswerable": payload["unanswerable_count"], "source": payload["source"], "sha256": sha(path), "exact_quote_count": sum(bool(x.get("evidence")) for x in out_questions), "negative_initial_search_count": sum(bool(x.get("absence_audit")) for x in out_questions)}
    (OUT / "qa40_build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
