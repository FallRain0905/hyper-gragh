# Hyper-ChE 40QA Final Result Summary

This file summarizes the corrected 40QA v3 benchmark results for the five experimental groups. It uses the corrected final Hyper-ChE mapping and the stricter evidence-grounded hallucination rejudge.

## 1. Benchmark Setup

- Benchmark: 40QA v3.
- Total questions: 40.
- Answerable questions: 35.
- Unanswerable questions: 5.
- Groups: 5.
- Generator and judge: same LLM setting for all groups.
- Evidence formatting: QA pipeline v3.
- Final Hyper-ChE group: `chem_norm_hypergraph`.
- Correct final Hyper-ChE cache: `hyper_final`.
- Important correction: `chem_norm_hypergraph` no longer uses the incomplete `hyper_norm` cache.

## 2. Group Definitions

| group | meaning | cache | view |
| --- | --- | --- | --- |
| text_segments | original text segment baseline | hyper_chem_prompt | text |
| original_hypergraph | original Hyper-RAG style hypergraph with generic JSON prompt | hyper_base | hyper |
| chem_prompt_graph | chemistry prompt extraction, projected to pairwise graph | hyper_chem_prompt | graph |
| chem_prompt_hypergraph | chemistry prompt extraction, hypergraph view | hyper_chem_prompt | hyper |
| chem_norm_hypergraph | final Hyper-ChE, chemistry prompt + normalization + measurement instances + EFU repair | hyper_final | hyper |

## 3. Main QA Results

These are the original QA benchmark scores. The original hallucination column is retained for traceability, but the stricter hallucination rejudge in Section 4 should be used for paper discussion.

| group | questions | Good Rate | Satisfactory-or-Better Rate | Key-Point Coverage | Original Hallucination Rate | Abstention Accuracy | Citation Stability Experimental |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| text_segments | 40 | 0.175 | 0.175 | 0.175 | 0.000 | 0.725 | 0.150 |
| original_hypergraph | 40 | 0.075 | 0.075 | 0.075 | 0.000 | 0.550 | 0.075 |
| chem_prompt_graph | 40 | 0.100 | 0.100 | 0.100 | 0.000 | 0.550 | 0.075 |
| chem_prompt_hypergraph | 40 | 0.150 | 0.150 | 0.150 | 0.025 | 0.675 | 0.125 |
| chem_norm_hypergraph | 40 | 0.075 | 0.075 | 0.075 | 0.000 | 0.550 | 0.075 |

## 4. Evidence-Grounded Hallucination Rejudge

The original hallucination metric was too weak because it mostly checked explicit conflict with the reference answer. The stricter rejudge reads retrieved evidence blocks and checks unsupported claims, wrong entity binding, wrong condition or metric binding, wrong numeric values or units, and overgeneralization. The reference answer is treated as the gold standard.

| group | questions | Strict Hallucination Rate | Major Hallucination Rate | Minor Hallucination Rate | Avg Evidence Groundedness | Empty or Abstention Rate | Old Hallucination Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| text_segments | 40 | 0.000 | 0.000 | 0.000 | 0.3475 | 0.700 | 0.000 |
| original_hypergraph | 40 | 0.000 | 0.000 | 0.000 | 0.1500 | 0.875 | 0.000 |
| chem_prompt_graph | 40 | 0.025 | 0.025 | 0.000 | 0.2875 | 0.800 | 0.000 |
| chem_prompt_hypergraph | 40 | 0.075 | 0.075 | 0.000 | 0.3325 | 0.675 | 0.025 |
| chem_norm_hypergraph | 40 | 0.000 | 0.000 | 0.000 | 0.3250 | 0.750 | 0.000 |

## 5. Results by Answerability

| group | answerable | questions | Good Rate | Satisfactory-or-Better Rate | Key-Point Coverage | Original Hallucination Rate | Abstention Accuracy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| text_segments | False | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.000 |
| text_segments | True | 35 | 0.1714 | 0.1714 | 0.1714 | 0.000 | 0.6857 |
| original_hypergraph | False | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| original_hypergraph | True | 35 | 0.0857 | 0.0857 | 0.0857 | 0.000 | 0.4857 |
| chem_prompt_graph | False | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.000 |
| chem_prompt_graph | True | 35 | 0.0857 | 0.0857 | 0.0857 | 0.000 | 0.4857 |
| chem_prompt_hypergraph | False | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.000 |
| chem_prompt_hypergraph | True | 35 | 0.1429 | 0.1429 | 0.1429 | 0.0286 | 0.6286 |
| chem_norm_hypergraph | False | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| chem_norm_hypergraph | True | 35 | 0.0857 | 0.0857 | 0.0857 | 0.000 | 0.4857 |

## 6. Key Question-Type Findings

Only the most important question-type patterns are listed here.

| question type | key observation |
| --- | --- |
| direct retrieval | `text_segments` and `chem_prompt_hypergraph` perform best, both with KPC = 0.7143. |
| comparison | `chem_norm_hypergraph` is the only group with non-zero KPC, reaching 0.1667. |
| mechanism explanation | all systems are weak; `chem_prompt_hypergraph` has hallucination in this category. |
| degradation analysis | all systems are weak; scores are close to zero. |
| multi-condition synthesis | all systems are weak; scores are close to zero. |
| unanswerable | abstention is generally strong, but this should be discussed separately from answer quality. |

## 7. Important Hallucinated Cases

The stricter hallucination rejudge identified the following representative errors:

1. `DOC01-QA-004 / chem_prompt_graph`
   - Wrong claim: higher current density reduces vanadium ion crossover.
   - Reason: the reference answer states that crossover flux remains relatively constant; CE increases because Faradaic current increases.

2. `DOC01-QA-004 / chem_prompt_hypergraph`
   - Wrong claim: CE increases because higher current density reduces crossover.
   - Error type: wrong mechanism / unsupported causal explanation.

3. `DOC01-QA-006 / chem_prompt_hypergraph`
   - Wrong binding: compares Nafion 117 with SPEEK instead of Nafion 117 with Nafion 212.
   - Error type: wrong material binding and wrong numeric values.

4. `DOC02-QA-006 / chem_prompt_hypergraph`
   - Wrong recommendation: selects SPEEK instead of SNPBI-1.42.
   - Error type: wrong membrane selection and wrong evidence binding.

## 8. Interpretation for Paper Writing

The 40QA benchmark should not be used as the only evidence for Hyper-ChE's advantage. The results show that the current end-to-end QA generation pipeline remains weak, especially on complex mechanism, degradation, and multi-condition synthesis questions.

The key responsible interpretation is:

- `chem_prompt_hypergraph` gives the best structured QA coverage among graph/hypergraph variants, but it has the highest strict hallucination rate.
- `chem_norm_hypergraph`, the final Hyper-ChE setting, has zero strict hallucination in this run, but this is partly because its empty/abstention rate is high.
- Therefore, final Hyper-ChE is more conservative and safer, but not yet stronger in end-to-end answer coverage.
- QA results should be reported together with abstention rate and groundedness score.
- Retrieval benchmark and Fact Coverage are better suited to demonstrate the modeling advantage of hypergraph structure.
- QA benchmark should be discussed as an end-to-end stress test and as evidence of remaining system-level limitations.

## 9. Recommended Paper Table

For the paper, use the following columns instead of the old hallucination-only table:

| group | Good Rate | Sat+ Rate | KPC | Strict Hallucination | Empty/Abstention | Avg Groundedness |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| text_segments | 0.175 | 0.175 | 0.175 | 0.000 | 0.700 | 0.3475 |
| original_hypergraph | 0.075 | 0.075 | 0.075 | 0.000 | 0.875 | 0.1500 |
| chem_prompt_graph | 0.100 | 0.100 | 0.100 | 0.025 | 0.800 | 0.2875 |
| chem_prompt_hypergraph | 0.150 | 0.150 | 0.150 | 0.075 | 0.675 | 0.3325 |
| chem_norm_hypergraph | 0.075 | 0.075 | 0.075 | 0.000 | 0.750 | 0.3250 |

## 10. Source Files

- Main QA records: `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_records.jsonl`
- Main QA summary: `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_summary.csv`
- Question-type summary: `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_by_question_type.csv`
- Answerability summary: `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_by_answerability.csv`
- Strict hallucination summary: `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/hallucination_rejudge_v2/hallucination_rejudge_summary.csv`
- Strict hallucination report: `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/hallucination_rejudge_v2/hallucination_rejudge_report.md`

