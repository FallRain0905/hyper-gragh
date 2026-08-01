# Evidence-Grounded Hallucination Rejudge

This audit rejudges existing QA answers without regenerating them.
The judge reads the retrieved evidence blocks and flags unsupported claims, wrong bindings, wrong values/units, and overgeneralizations.

## Summary

| group | questions | strict hallucination | major | minor | avg groundedness | empty/abstention | old hallucination |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| chem_norm_hypergraph | 40 | 0.0 | 0.0 | 0.0 | 0.325 | 0.75 | 0.0 |
| chem_prompt_graph | 40 | 0.025 | 0.025 | 0.0 | 0.2875 | 0.8 | 0.0 |
| chem_prompt_hypergraph | 40 | 0.075 | 0.075 | 0.0 | 0.3325 | 0.675 | 0.025 |
| original_hypergraph | 40 | 0.0 | 0.0 | 0.0 | 0.15 | 0.875 | 0.0 |
| text_segments | 40 | 0.0 | 0.0 | 0.0 | 0.3475 | 0.7 | 0.0 |

## Hallucinated Cases

### DOC01-QA-004 | chem_prompt_graph

- Severity: major
- Groundedness: 0.0
- Question: Why does coulombic efficiency increase with increasing current density in VRFBs with Nafion membranes->
- Answer: Higher current density reduces vanadium ion crossover through the Nafion membrane, thereby decreasing self-discharge and increasing coulombic efficiency.
- Unsupported claims: ["Higher current density reduces vanadium ion crossover through the Nafion membrane"]
- Wrong bindings: []
- Wrong values/units: []
- Overgeneralizations: []
- Rationale: The generated answer claims that higher current density reduces vanadium ion crossover, which contradicts the reference answer stating that crossover flux remains relatively constant. Although evidence block 1 appears to support the claim, the reference answer is the gold standard and indicates the claim is incorrect. Therefore, the answer is hallucinated.

### DOC01-QA-004 | chem_prompt_hypergraph

- Severity: major
- Groundedness: 0.2
- Question: Why does coulombic efficiency increase with increasing current density in VRFBs with Nafion membranes->
- Answer: Coulombic efficiency increases with increasing current density because higher current density reduces vanadium ion crossover across the Nafion membrane, thereby minimizing self-discharge and improving coulombic efficiency.
- Unsupported claims: ["Higher current density reduces vanadium ion crossover across the Nafion membrane"]
- Wrong bindings: []
- Wrong values/units: []
- Overgeneralizations: ["The claim that higher current density reduces crossover is not supported by the reference answer and contradicts the established mechanism for VRFBs with Nafion membranes"]
- Rationale: The generated answer claims that coulombic efficiency increases because higher current density reduces vanadium ion crossover. However, the reference answer states that crossover flux driven by concentration gradients remains constant, and the increase in CE is due to the proportional increase in Faradaic current. The retrieved evidence (Evidence 1 and 2) supports the reduction in crossover, but this conflicts with the reference answer. According to instructions, when evidence and reference conflict, trust the reference. Therefore, the generated answer is hallucinated, as it presents a mechanism that is not consistent with the gold standard.

### DOC01-QA-006 | chem_prompt_hypergraph

- Severity: major
- Groundedness: 0.2
- Question: At 100 mA/cm2 and 25 C, both membranes achieve similar EE despite different CE/VE compositions. Explain the performance trade-off and recommend which membrane to use for long-cycle-life stationary storage.
- Answer: The performance trade-off is that Nafion 117 achieves a slightly higher EE (84% vs 83%) but has a higher capacity fade rate (0.035%/cycle) compared to SPEEK (0.018%/cycle). For long-cycle-life stationary storage, the lower capacity fade of SPEEK is more beneficial, so SPEEK is recommended.
- Unsupported claims: ["Claims about Nafion 117 vs SPEEK instead of Nafion 117 vs Nafion 212", "EE values 84% and 83% not matching reference 80.2% and 80.9%", "Capacity fade rates 0.035%/cycle and 0.018%/cycle not matching reference 0.08%/cycle and 0.18%/cycle"]
- Wrong bindings: ["SPEEK membrane bound instead of Nafion 212 in the comparison"]
- Wrong values/units: ["EE values (84%, 83%) are incorrect; reference gives 80.2% and 80.9%", "Capacity fade rates (0.035%/cycle, 0.018%/cycle) are incorrect; reference gives 0.08%/cycle and 0.18%/cycle"]
- Overgeneralizations: []
- Rationale: The generated answer compares Nafion 117 with SPEEK, while the question asks about Nafion 117 and Nafion 212. The specific EE values and capacity fade rates provided are from evidence about SPEEK and do not match the reference answer's values for Nafion 117 and Nafion 212. Thus, the answer is hallucinated with major severity due to wrong entities and values.

### DOC02-QA-006 | chem_prompt_hypergraph

- Severity: major
- Groundedness: 0.2
- Question: A VRFB system designer needs to select a non-fluorinated membrane for an application requiring maximum energy efficiency at 100 mA/cm2 with minimal capacity fade over long-term cycling. Which membrane should be selected and what is the rationale->
- Answer: Select SPEEK membrane with 42% sulfonation degree due to its significantly lower capacity fade rate (0.018%/cycle vs 0.035%/cycle for Nafion 117) and comparable energy efficiency (83% vs 84% at 100 mA/cm2).
- Unsupported claims: ["Recommends SPEEK membrane instead of SNPBI-1.42 as required by reference"]
- Wrong bindings: ["Selected membrane SPEEK vs reference SNPBI-1.42"]
- Wrong values/units: []
- Overgeneralizations: []
- Rationale: Generated answer selects SPEEK membrane, conflicting with reference answer which selects SNPBI-1.42. Retrieved evidence supports SPEEK metrics but does not support the choice over SNPBI-1.42 for the specified application. Hence hallucination is major.
