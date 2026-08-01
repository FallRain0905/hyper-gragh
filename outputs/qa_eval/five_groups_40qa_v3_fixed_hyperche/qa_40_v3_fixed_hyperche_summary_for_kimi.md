# Hyper-ChE 40QA v3 Fixed HyperChE Benchmark Summary

This document summarizes the corrected `five_groups_40qa_v3_fixed_hyperche` QA benchmark run. It is written in English to avoid encoding problems when read by external agents such as Kimi.

## 1. Experiment Background

- Task: 40-question QA generation benchmark.
- Question set: 40 questions in total.
- Answerability split: 35 answerable questions and 5 unanswerable questions.
- System groups: 5 groups.
- Generator and judge: the same LLM-based generation and LLM-as-a-judge pipeline is used for all groups.
- Evidence formatting: v3 QA pipeline.
- For `chem_norm_hypergraph`, lossless / atomic evidence cards are enabled.
- Output directory: `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/`
- Completion: 200 / 200 records completed.
- Error status: `errors.json = []`.

## 2. Important Correction

In the previous run, `chem_norm_hypergraph` incorrectly used the `hyper_norm` cache. That cache had:

- entity normalization enabled;
- measurement instances disabled;
- EFU repair disabled.

Therefore, it did not represent the final Hyper-ChE system.

In this corrected run, `chem_norm_hypergraph` is mapped to `hyper_final`, which represents the final Hyper-ChE configuration:

- chemistry prompt profile enabled;
- entity normalization enabled;
- measurement instances enabled;
- EFU repair enabled;
- hypergraph view used for QA evidence.

## 3. Group Configuration

| group | label | cache | view |
| --- | --- | --- | --- |
| text_segments | Original text segments | hyper_chem_prompt | text |
| original_hypergraph | Original Hyper-RAG hypergraph | hyper_base | hyper |
| chem_prompt_graph | Chemistry prompt graph projection | hyper_chem_prompt | graph |
| chem_prompt_hypergraph | Chemistry prompt hypergraph | hyper_chem_prompt | hyper |
| chem_norm_hypergraph | Final Hyper-ChE chemistry-normalized hypergraph | hyper_final | hyper |

## 4. Main Results

| group | questions | Good Rate | Satisfactory-or-Better Rate | Key-Point Coverage | Hallucination Rate | Abstention Accuracy | Citation Stability Experimental |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| text_segments | 40 | 0.175 | 0.175 | 0.175 | 0.000 | 0.725 | 0.150 |
| original_hypergraph | 40 | 0.075 | 0.075 | 0.075 | 0.000 | 0.550 | 0.075 |
| chem_prompt_graph | 40 | 0.100 | 0.100 | 0.100 | 0.000 | 0.550 | 0.075 |
| chem_prompt_hypergraph | 40 | 0.150 | 0.150 | 0.150 | 0.025 | 0.675 | 0.125 |
| chem_norm_hypergraph | 40 | 0.075 | 0.075 | 0.075 | 0.000 | 0.550 | 0.075 |

## 5. Results by Answerability

| group | answerable | questions | Good Rate | Satisfactory-or-Better Rate | Key-Point Coverage | Hallucination Rate | Abstention Accuracy | Citation Stability Experimental |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| text_segments | False | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.000 | 0.000 |
| text_segments | True | 35 | 0.1714 | 0.1714 | 0.1714 | 0.000 | 0.6857 | 0.1714 |
| original_hypergraph | False | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| original_hypergraph | True | 35 | 0.0857 | 0.0857 | 0.0857 | 0.000 | 0.4857 | 0.0857 |
| chem_prompt_graph | False | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.000 | 0.000 |
| chem_prompt_graph | True | 35 | 0.0857 | 0.0857 | 0.0857 | 0.000 | 0.4857 | 0.0857 |
| chem_prompt_hypergraph | False | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.000 | 0.000 |
| chem_prompt_hypergraph | True | 35 | 0.1429 | 0.1429 | 0.1429 | 0.0286 | 0.6286 | 0.1429 |
| chem_norm_hypergraph | False | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| chem_norm_hypergraph | True | 35 | 0.0857 | 0.0857 | 0.0857 | 0.000 | 0.4857 | 0.0857 |

## 6. Results by Question Type

| group | question_type | questions | Good Rate | Satisfactory-or-Better Rate | Key-Point Coverage | Hallucination Rate | Abstention Accuracy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| text_segments | comparison | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.6667 |
| text_segments | condition-constrained retrieval | 6 | 0.1667 | 0.1667 | 0.1667 | 0.000 | 0.3333 |
| text_segments | degradation analysis | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.8000 |
| text_segments | direct retrieval | 7 | 0.7143 | 0.7143 | 0.7143 | 0.000 | 0.7143 |
| text_segments | mechanism explanation | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.8000 |
| text_segments | multi-condition synthesis | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.8333 |
| text_segments | unanswerable | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.0000 |
| original_hypergraph | comparison | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.5000 |
| original_hypergraph | condition-constrained retrieval | 6 | 0.1667 | 0.1667 | 0.1667 | 0.000 | 0.3333 |
| original_hypergraph | degradation analysis | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.6000 |
| original_hypergraph | direct retrieval | 7 | 0.2857 | 0.2857 | 0.2857 | 0.000 | 0.4286 |
| original_hypergraph | mechanism explanation | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.8000 |
| original_hypergraph | multi-condition synthesis | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.3333 |
| original_hypergraph | unanswerable | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 1.0000 |
| chem_prompt_graph | comparison | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.1667 |
| chem_prompt_graph | condition-constrained retrieval | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.3333 |
| chem_prompt_graph | degradation analysis | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.8000 |
| chem_prompt_graph | direct retrieval | 7 | 0.4286 | 0.4286 | 0.4286 | 0.000 | 0.4286 |
| chem_prompt_graph | mechanism explanation | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.8000 |
| chem_prompt_graph | multi-condition synthesis | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.5000 |
| chem_prompt_graph | unanswerable | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.0000 |
| chem_prompt_hypergraph | comparison | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.6667 |
| chem_prompt_hypergraph | condition-constrained retrieval | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.3333 |
| chem_prompt_hypergraph | degradation analysis | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.6000 |
| chem_prompt_hypergraph | direct retrieval | 7 | 0.7143 | 0.7143 | 0.7143 | 0.000 | 0.7143 |
| chem_prompt_hypergraph | mechanism explanation | 5 | 0.000 | 0.000 | 0.000 | 0.200 | 0.8000 |
| chem_prompt_hypergraph | multi-condition synthesis | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.6667 |
| chem_prompt_hypergraph | unanswerable | 5 | 0.200 | 0.200 | 0.200 | 0.000 | 1.0000 |
| chem_norm_hypergraph | comparison | 6 | 0.1667 | 0.1667 | 0.1667 | 0.000 | 0.5000 |
| chem_norm_hypergraph | condition-constrained retrieval | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.5000 |
| chem_norm_hypergraph | degradation analysis | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.2000 |
| chem_norm_hypergraph | direct retrieval | 7 | 0.2857 | 0.2857 | 0.2857 | 0.000 | 0.7143 |
| chem_norm_hypergraph | mechanism explanation | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.6000 |
| chem_norm_hypergraph | multi-condition synthesis | 6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.3333 |
| chem_norm_hypergraph | unanswerable | 5 | 0.000 | 0.000 | 0.000 | 0.000 | 1.0000 |

## 7. Focused Pairwise Comparisons

| left_group | right_group | questions | KPC_delta_left_minus_right | good_wins | good_losses | sat_wins | sat_losses | hallucination_better | hallucination_worse |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| text_segments | chem_norm_hypergraph | 40 | 0.100 | 5 | 1 | 5 | 1 | 0 | 0 |
| chem_prompt_hypergraph | chem_prompt_graph | 40 | 0.050 | 2 | 0 | 2 | 0 | 0 | 1 |
| chem_norm_hypergraph | text_segments | 40 | -0.100 | 1 | 5 | 1 | 5 | 0 | 0 |
| chem_norm_hypergraph | original_hypergraph | 40 | 0.000 | 3 | 3 | 3 | 3 | 0 | 0 |
| chem_norm_hypergraph | chem_prompt_graph | 40 | -0.025 | 3 | 4 | 3 | 4 | 0 | 0 |
| chem_norm_hypergraph | chem_prompt_hypergraph | 40 | -0.075 | 2 | 5 | 2 | 5 | 1 | 0 |

## 8. Initial Observations

1. `text_segments` has the highest overall score in this 40QA run, with Good Rate, Satisfactory-or-Better Rate, and Key-Point Coverage all equal to 0.175.
2. Among structured groups, `chem_prompt_hypergraph` performs best overall, with Good Rate / Sat+ / KPC equal to 0.150, but it also has a small hallucination rate of 0.025.
3. After correction, `chem_norm_hypergraph` now truly uses `hyper_final`. Its KPC is 0.075, which is higher than the previous wrong-cache run but still lower than `chem_prompt_hypergraph` and `text_segments`.
4. `chem_norm_hypergraph` has zero hallucination in this run. This suggests conservative normalization may reduce unsupported claims, but it may also reduce answer coverage.
5. On direct retrieval questions, `text_segments` and `chem_prompt_hypergraph` both reach 0.7143 KPC, while `chem_norm_hypergraph` reaches 0.2857.
6. On comparison questions, `chem_norm_hypergraph` is the only group with non-zero KPC among the structured final group comparison, reaching 0.1667. This suggests that normalized hypergraph structure may help some comparison questions.
7. Complex categories such as mechanism explanation, degradation analysis, and multi-condition synthesis remain weak across all systems. This indicates a mismatch among retrieval, evidence verbalization, generation prompt, and judge criteria.

## 9. Questions for Further Analysis

Please focus on the following issues:

1. Why does `chem_norm_hypergraph`, even after using `hyper_final`, still underperform `chem_prompt_hypergraph` in the QA benchmark?
2. Is the final Hyper-ChE evidence representation too conservative, causing low recall in generation?
3. Does the generator fail to use structured evidence even when the evidence contains the correct information?
4. Why does `chem_norm_hypergraph` show some advantage on comparison questions but not on mechanism or multi-condition questions?
5. Is the LLM judge too strict for partially correct answers?
6. Should QA benchmark results be separated from Retrieval Benchmark and Fact Coverage results in the paper narrative?
7. Can Retrieval / Fact Coverage be used as the main evidence for hypergraph modeling advantages, while QA is discussed as an end-to-end system limitation?

## 10. Related Files

- `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_summary.csv`
- `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_summary.json`
- `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_records.jsonl`
- `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_by_question_type.csv`
- `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_by_answerability.csv`
- `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_pairwise_comparison.csv`
- `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/qa_40_debug_failures.md`
- `outputs/qa_eval/five_groups_40qa_v3_fixed_hyperche/errors.json`

## 11. Bottom-Line Note

This corrected 40QA run should be treated as the current fixed 40QA v3 baseline. The final Hyper-ChE group is now correctly mapped to `hyper_final`. However, the end-to-end QA score still does not fully reflect the potential advantages observed in Retrieval Benchmark or Fact Coverage. Therefore, the next step should be a failure analysis of evidence retrieval, evidence verbalization, generation behavior, and judge strictness.
