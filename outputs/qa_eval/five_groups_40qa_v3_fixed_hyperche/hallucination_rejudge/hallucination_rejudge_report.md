# Evidence-Grounded Hallucination Rejudge

This audit rejudges existing QA answers without regenerating them.
The judge reads the retrieved evidence blocks and flags unsupported claims, wrong bindings, wrong values/units, and overgeneralizations.

## Summary

| group | questions | strict hallucination | major | minor | avg groundedness | empty/abstention | old hallucination |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chem_norm_hypergraph | 40 | 0.0 | 0.0 | 0.0 | 0.45 | 0.75 | 0.0 |
| chem_prompt_graph | 40 | 0.0 | 0.0 | 0.0 | 0.32 | 0.8 | 0.0 |
| chem_prompt_hypergraph | 40 | 0.0 | 0.0 | 0.0 | 0.4475 | 0.675 | 0.025 |
| original_hypergraph | 40 | 0.0 | 0.0 | 0.0 | 0.25 | 0.85 | 0.0 |
| text_segments | 40 | 0.0 | 0.0 | 0.0 | 0.4487 | 0.675 | 0.0 |

## Hallucinated Cases

No hallucinated cases were detected by the evidence-grounded judge.