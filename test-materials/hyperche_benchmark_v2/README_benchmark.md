# Hyper-ChE Flow Battery Benchmark v1.1

## Overview

This benchmark is a **synthetic controlled corpus** designed for evaluating knowledge extraction and retrieval systems in the redox flow battery domain. It is specifically built to test **Hyper-RAG**, **Graph-RAG**, **Vector RAG**, and **Hyper-ChE** frameworks on their ability to retrieve **Experimental Fact Units (EFUs)**---high-order relational facts that capture "system-material-condition-metric-mechanism" combinations.

## Dataset Statistics

| Metric | Count | Target |
|--------|-------|--------|
| Documents | 10 | 10 |
| Total Words | ~40,000 | 30,000-40,000 |
| Gold EFUs | 234 | 220-300 |
| Gold Facts | 180 | 180-250 |
| QA Questions | 104 | 80-120 |

### EFU Type Distribution

| Type | Count | Min Required |
|------|-------|-------------|
| OPERATION_PERFORMANCE | 98 | 80 |
| COMPARISON | 39 | 30 |
| COMPOSITION | 26 | 20 |
| DEGRADATION_CHAIN | 28 | 20 |
| MECHANISM_EVIDENCE | 30 | 20 |
| DESIGN_SUMMARY | 13 | 10 |

### QA Level Distribution

| Level | Count | Min Required |
|-------|-------|-------------|
| L1 (direct fact retrieval) | 22 | 10 |
| L2 (local comparison) | 24 | 10 |
| L3 (condition combination) | 26 | 10 |
| L4 (cross-material comparison) | 12 | 10 |
| L5 (mechanism chain) | 10 | 10 |
| L6 (cross-system strategy) | 10 | 10 |

## Document List

| Doc ID | Title | Theme | Words |
|--------|-------|-------|-------|
| DOC01 | VRFB Baseline with Nafion 117 and Nafion 212 | Nafion membrane grades, CE/VE/EE tradeoff | ~3,250 |
| DOC02 | Non-Fluorinated Membranes for VRFB | PBI, SNPBI-1.42, SPEEK/APK, SPTPC-2.59 | ~3,680 |
| DOC03 | Carbon Felt and Modified Carbon Electrodes | C-C, MC-C, BMC-C, contact angle, Rct | ~2,100 |
| DOC04 | Electrolyte Concentration and Flow-Rate Effects | Vanadium conc., H2SO4, flow rate, pumping loss | ~2,230 |
| DOC05 | Temperature, Cycling, and Capacity Fading | 25C/40C/60C, crossover, SOC imbalance | ~4,900 |
| DOC06 | Iron-Chromium RFB with Bi3+ Additive | ICRFB, Bi3+, HER, Cr kinetics | ~5,400 |
| DOC07 | Zinc-Bromine Flow Battery Degradation | Bromine crossover, complexing agent, dendrites | ~4,120 |
| DOC08 | Soluble Lead-Acid Flow Battery Degradation | PbO2 passivation, oxygen evolution, cycle life | ~4,640 |
| DOC09 | Organic Redox Flow Batteries | TEMPO, viologen, quinone, pH, AEM | ~4,710 |
| DOC10 | Cross-System Design Rules | 5-system comparison, transferable strategies | ~5,170 |

## Files

| File | Description |
|------|-------------|
| `corpus_documents.md` | 10 long documents in markdown format, separated by `---` |
| `gold_annotations.json` | Complete annotations: metadata, documents, gold_efu, gold_facts, qa_questions, evaluation_rubric |
| `qa_questions.json` | Standalone QA questions with metadata and level distribution |
| `README_benchmark.md` | This file |

## Schema

### Gold EFU

Each EFU (Experimental Fact Unit) represents a high-order relational fact:

```json
{
  "gold_id": "DOC01-EFU-001",
  "source_doc_id": "DOC01",
  "source_section": "Section 1: Membrane Performance",
  "relation_type": "OPERATION_PERFORMANCE",
  "claim": "At 100 mA/cm2 and 25 C, Nafion 117 in VRFB delivers CE 96.2%, VE 84.1%, EE 80.9%.",
  "entities": [{"canonical_id": "system:vrfb", "name": "VRFB", "type": "SYSTEM"}],
  "conditions": [{"quantity_type": "current_density", "value": 100, "unit": "mA/cm2", "canonical_id": "condition:current_density_100_ma_cm2"}],
  "measurements": [{"metric_type": "EE", "value": 80.9, "unit": "%", "canonical_id": "measurement:ee_80_9_percent"}],
  "mechanisms": ["degradation:vanadium_crossover"],
  "evidence_text": "exact sentence from document"
}
```

### Gold Fact

Each fact is used for Fact Coverage@k evaluation:

```json
{
  "fact_id": "DOC01-FACT-001",
  "source_doc_id": "DOC01",
  "claim": "At 100 mA/cm2 and 25 C, Nafion 117 in VRFB delivers CE 96.2%, VE 84.1%, EE 80.9%.",
  "required_entities": ["system:vrfb", "membrane:nafion_117"],
  "required_conditions": [{"quantity_type": "current_density", "value": 100, "unit": "mA/cm2", "canonical_id": "condition:current_density_100_ma_cm2"}],
  "required_metrics": [{"metric_type": "CE", "value": 96.2, "unit": "%", "canonical_id": "measurement:ce_96_2_percent"}],
  "required_mechanisms": ["degradation:vanadium_crossover"],
  "supporting_efus": ["DOC01-EFU-001"],
  "difficulty": "L3",
  "fact_type": "OPERATION_PERFORMANCE"
}
```

### QA Question

Each question targets specific facts and EFUs:

```json
{
  "question_id": "DOC01-QA-001",
  "source_doc_id": "DOC01",
  "level": "L3",
  "question_type": "condition-constrained retrieval",
  "question": "What is the EE of Nafion 117 VRFB at 100 mA/cm2 and 25 C?",
  "reference_answer": "EE is 80.9% with CE 96.2% and VE 84.1%.",
  "reference_answer_points": ["EE is 80.9%", "Condition: 100 mA/cm2, 25 C", "System: VRFB with Nafion 117"],
  "expected_facts": ["DOC01-FACT-001"],
  "expected_efus": ["DOC01-EFU-001"]
}
```

## Covered Test Points

1. Nafion 117 vs Nafion 212 CE/VE/EE tradeoff
2. Current density effects on CE/VE/EE (opposite trends)
3. Temperature effects on VE and crossover
4. Non-fluorinated membranes (SNPBI-1.42, SPEEK/APK, SPTPC-2.59)
5. IEC, area resistance, vanadium permeability vs EE
6. C-C, MC-C, BMC-C electrode comparison (contact angle, Rct, CE/VE/EE)
7. Flow rate, pumping loss, mass transfer vs net EE
8. ICRFB Bi3+ additive effects on Cr kinetics and HER
9. Zinc-bromine: bromine crossover, complexing agent, dendrite growth
10. Soluble lead-acid: PbO2 passivation, oxygen evolution, cycle life
11. Organic RFB: TEMPO, viologen, quinone stability and degradation
12. Cross-system design rules: membrane, electrode, additive, flow field

## Normalization Stress Points

The corpus includes intentional semantic normalization challenges:

- **Entity variants**: Nafion vs Nafion 117 vs Nafion 212; PBI vs SNPBI-1.42
- **Abbreviation expansion**: TEMPO, VRFB, ICRFB, AEM
- **Unit normalization**: All units in ASCII (cm2, mA/cm2, ohm cm2, C)
- **Hierarchical resolution**: membrane -> Nafion -> Nafion 117
- **Cross-reference disambiguation**: CE in different contexts

## Evaluation

### Fact Coverage@k

A retrieved fact is:
- **SUPPORTED**: All required entities, conditions, metrics, and mechanisms present
- **PARTIALLY_SUPPORTED**: Some required elements present
- **UNSUPPORTED**: No supporting evidence found

### QA Scoring (1-5 scale)

Dimensions:
- factual_correctness
- condition_completeness
- numerical_accuracy
- mechanistic_support
- comparative_clarity
- source_grounding
- readability

## Usage Notes

- This is a **synthetic corpus** for controlled evaluation. Do not cite as real experimental data.
- All ASCII units: use `cm2` not `cm^2`, `25 C` not `25 degC`, `x 10^-7` not `x 10^-7`.
- JSON must be parsed with `json.load()` using `encoding='utf-8'`.
- Canonical IDs use snake_case consistently throughout.

## License

Generated for Hyper-ChE project internal evaluation. Not for commercial redistribution.

## Validation and Benchmark Workflow

Before running experiments, validate the benchmark package from the repository root:

```powershell
python scripts\validate_benchmark.py test-materials\hyperche_benchmark_v2
```

If Kimi or another generator rewrites the benchmark files, apply deterministic packaging fixes and validate again:

```powershell
python scripts\validate_benchmark.py test-materials\hyperche_benchmark_v2 --fix
python scripts\validate_benchmark.py test-materials\hyperche_benchmark_v2
```

The validator checks:

- Required benchmark files are present.
- `gold_annotations.json` follows the evaluator-compatible schema.
- `gold_facts` use `required_metrics`, not `required_measurements`.
- EFU, fact, and QA IDs are internally consistent.
- QA `expected_facts` and `expected_efus` resolve to existing gold records.
- `corpus_documents.md` contains exactly 10 `# DOCxx:` document headings.
- Canonical IDs use snake_case namespace format.

Recommended build order:

1. Build `hyper_base` to validate the generic JSON prompt baseline.
2. Build `hyper_chem_prompt` to isolate chemistry prompt adaptation.
3. Build `hyper_norm` to measure normalization gains without measurement instances or repair.
4. Build `hyper_final` as the main Hyper-ChE system.
5. Build ablation caches: `final_no_measurement`, `final_no_repair`, and `final_no_rerank`.
6. Reuse the `hyper_final` cache for `graph_final`, because Graph-RAG is evaluated as a graph projection/query view.

Fact Coverage smoke test:

```powershell
python scripts\evaluate_fact_coverage.py `
  --gold test-materials\hyperche_benchmark_v2\gold_annotations.json `
  --modes graph_final hyper_base hyper_chem_prompt hyper_norm hyper_final `
  --cache-map configs\experiments\cache_map.yaml `
  --k-values 1 3 5 10 `
  --judge-mode heuristic `
  --output-dir outputs\fact_coverage\flow_benchmark_v2_smoke
```

Main Fact Coverage evaluation:

```powershell
python scripts\evaluate_fact_coverage.py `
  --gold test-materials\hyperche_benchmark_v2\gold_annotations.json `
  --modes graph_final hyper_base hyper_chem_prompt hyper_norm hyper_final final_no_measurement final_no_repair final_no_rerank `
  --cache-map configs\experiments\cache_map.yaml `
  --k-values 1 3 5 10 `
  --judge-mode llm `
  --judge-models kimi deepseek qwen `
  --output-dir outputs\fact_coverage\flow_benchmark_v2_main
```

QA evaluation requires generated answer files for each mode. After answer generation, run:

```powershell
python scripts\evaluate_qa_answers.py `
  --answer-map configs\experiments\qa_answer_map.yaml `
  --modes graph_final hyper_base hyper_chem_prompt hyper_norm hyper_final `
  --judge-models kimi deepseek qwen `
  --output-dir outputs\qa_eval\flow_benchmark_v2_main
```

