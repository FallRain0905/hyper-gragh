# QA LLM Smoke v2 Debug

Evidence formatting v2 was used: query-focused excerpts, structured short claims, 1500-token evidence budget, and programmatic abstention_correct.

## DOC01-QA-001 / text_segments
- Category: `measurement`
- Answerable: `True`
- Question: What is the area-specific resistance of Nafion 117 at 25 C?
- Reference answer: 1.65 ohm cm2
- Generated answer: 1.65 ohm cm2
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly states the area-specific resistance of Nafion 117 at 25°C as 1.65 ohm cm2, which matches the reference answer and covers the required key point. It cites evidence and contains no unsupported claims. Therefore, the answer is good.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC10`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.75`
```text
Evidence 1
Source: DOC10
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: The area-specific resistance (ASR) of the membrane directly impacts energy efficiency at a given current density. At 100 mA/cm2, a SPEEK membrane with 42% sulfonation degree achieved an EE of 83% compared to 84% for Nafion 117, but reduced the capacity fade rate from 0.035%/cycle to 0.018%/cycle. A benchmark AEM (Fumatech FAP-450) achieved an EE of 79% at 100 mA/cm2 with iron-chromium electrolyte, compared to 82% for Nafion 117, but with significantly improved chromium retention (crossover rate reduced by 40%). A nanoporous ceramic-polymer composite membrane demonstrated improved lead rejection (selectivity 93%) with an ASR of 3.2 ohm cm2, achieving an EE of 74% at 30 mA/cm2 compared to 76% with Nafion 117 but with reduced capacity fade from 0.08%/cycle to 0.04%/cycle.

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.65625`
```text
Evidence 2
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Our results demonstrate that Nafion 117, with its greater membrane thickness of approximately 183 um, consistently achieves superior coulombic efficiency (96-98%) due to reduced vanadium crossover, while Nafion 212, at approximately 50.8 um thickness, exhibits higher voltage efficiency (84-88%) stemming from lower area-specific resistance. | Property | Nafion 117 | Nafion 212 | |---|---|---| | Thickness (um) | 183 | 50.8 | | Equivalent weight (g/equiv) | 1100 | 1100 | | Area resistance (ohm cm2, 25 C) | 1.65 | 0.85 | | Vanadium permeability (x 10^-7 cm2/s) | 1.8 | 3.9 | | Water uptake (%) | 22 | 25 | | Ion exchange capacity (mmol/g) | 0.91 | 0.91 | The water uptake values, measured after equilibration in deionized water at 25 C, were 22% for Nafion 117 and 25% for Nafion 212. Based on the measured permeability values and the electrolyte volumes employed, the capacity fade rate attributable to vanadium crossover alone is estimated at approximately 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212 under standard operating conditions at 100 mA/cm2 and 25 C. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage effic
```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.65625`
```text
Evidence 3
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. | Membrane | IEC (mmol/g) | Water Uptake (%) | Area Resistance (ohm cm2) | Vanadium Permeability (x 10^-7 cm2/s) | |---|---|---|---|---| | PBI | 0.0 | 12 | 2.45 | 0.50 | | SNPBI-1.42 | 1.42 | 18 | 1.15 | 0.95 | | SPEEK/APK | 1.26 | 21 | 1.38 | 2.10 | | SPTPC-2.59 | 2.59 | 28 | 0.82 | 3.20 | ### 3.2 Area-Specific Resistance The area-specific resistance values showed a strong inverse correlation with IEC. For applications prioritizing maximum voltage efficiency and power density, particularly at high current densities, SPTPC-2.59 offers advantages through its very low resistance (0.82 ohm cm2). The quantitative relationships between IEC, resistance, permeability, and energy efficiency provide a framework for rational design of next-generation non-fluorinated VRFB membranes.

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC09`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.65625`
```text
Evidence 4
Source: DOC09
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: The crossover rate of TEMPO through the Nafion 117 membrane was measured at 0.8 x 10^-6 cm2/s, contributing to a gradual capacity fade over extended cycling. Under standardized conditions (100 mA/cm2, Nafion 117 membrane, room temperature, 500 cycle duration), the capacity fade rates were: AQDS at pH 12 showed 0.025%/cycle, TEMPO in nonaqueous electrolyte showed 0.02%/cycle, PSV (functionalized viologen) showed 0.018%/cycle, MV at pH 7 showed 0.055%/cycle, and unfunctionalized TEMPO in the presence of 50 ppm water showed 0.045%/cycle. Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2: Nafion 117 (selectivity 88%, MV crossover 2.1 x 10^-6 cm2/s, capacity fade 0.055%/cycle), Nafion 212 (selectivity 85%, MV crossover 2.5 x 10^-6 cm2/s, capacity fade 0.065%/cycle), a sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation (selectivity 92%, MV crossover 1.2 x 10^-6 cm2/s, capacity fade 0.038%/cycle), a commercial anion exchange membrane (selectivity 90%, MV crossover 1.5 x 10^-6 cm2/s, capacity fade 0.042%/cycle), and a nanoporous size-exclusion membrane (selectivity 97%, MV crossover 0.3 x 10^-6 cm2/s, capacity fade 0.012%/cycle). However, this membrane also exhibited higher area-specific resistance (2.8 ohm cm2 compared to 1.8 ohm cm2 for Nafion 117), resulting in a lower EE of 78.5% compared to 80.2% for Nafion at 100 mA/cm2.

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC04`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.5625`
```text
Evidence 5
Source: DOC04
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: 2.2 Battery Assembly and Testing Single-cell VRFB tests were conducted using graphite felt electrodes with an active area of 10 cm2 and Nafion 117 membrane as the separator. At 50 mA/cm2, the lower current density reduced both concentration polarization and the relative impact of pumping losses, enabling net EE values at the higher end of the observed range. The elevated vanadium crossover in turn caused capacity fade and self-discharge, further reducing system efficiency. Conclusion This systematic investigation has elucidated the complex interdependence of electrolyte concentration, flow rate, and current density on VRFB performance metrics and system-level net efficiency.

```

## DOC01-QA-001 / original_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: What is the area-specific resistance of Nafion 117 at 25 C?
- Reference answer: 1.65 ohm cm2
- Generated answer: 1.65 ohm cm2
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer exactly matches the reference answer and covers the required key point. It is concise, correct, and supported by the cited evidence. No unsupported claims or hallucinations are present.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|area resistance of Nafion 117 at 25 C`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.6875`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: ASSOCIATED_WITH
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, area resistance of Nafion 117 at 25 C.
Entities: ["Nafion 117"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 25 C"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 117; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2 Relation type: ASSOCIATED_WITH Readable labels: Nafion 117; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2 Description: Nafion 117 has area resistance of 1.65 ohm cm2 at 25 C. Source evidence: Nafion 117 has area resistance of 1.65 ohm cm2 at 25 C.

```
#### Evidence 2
- evidence_id: `Nafion 117|Nafion 212|area resistance of Nafion 117 at 25 C|area resistance of Nafion 117 at 40 C|area resistance of Nafion 212 at 25 C|area resistance of Nafion 212 at 40 C|temperature 40 C`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.598214`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under temperature 40 C = 40 C, temperature 40 C, area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, while area resistance of Nafion 117 at 40 C = 1.32 ohm cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "area resistance of Nafion 117 at 25 C", "area resistance of Nafion 117 at 40 C", "area resistance of Nafion 212 at 25 C", "area resistance of Nafion 212 at 40 C"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "temperature 40 C = 40 C"]
Conditions: ["temperature 40 C = 40 C", "temperature 40 C"]
Raw support excerpt: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2; temperature 40 C = 40 C Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2; te
```
#### Evidence 3
- evidence_id: `Nafion 117|area resistance of Nafion 117 at 40 C`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.59375`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: ASSOCIATED_WITH
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported area resistance of Nafion 117 at 40 C = 1.32 ohm cm2, area resistance of Nafion 117 at 40 C.
Entities: ["Nafion 117"]
Metrics: ["area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 117 at 40 C"]
Values: ["area resistance of Nafion 117 at 40 C = 1.32 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 117; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2 Relation type: ASSOCIATED_WITH Readable labels: Nafion 117; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2 Description: Nafion 117 has area resistance of 1.32 ohm cm2 at 40 C. Source evidence: Nafion 117 has area resistance of 1.32 ohm cm2 at 40 C.

```
#### Evidence 4
- evidence_id: `Nafion 117|Nafion 212|area resistance of Nafion 117 at 25 C|area resistance of Nafion 212 at 25 C|thickness of Nafion 117|thickness of Nafion 212|vanadium permeability of Nafion 117|vanadium permeability of Nafion 212`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.59375`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under the reported conditions, area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, while area resistance of Nafion 212 at 25 C = 0.85 ohm cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "thickness of Nafion 117", "thickness of Nafion 212"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "vanadium permeability of Nafion 117 = 1.8e-07 cm2/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm2/s", "area resistance of Nafion 117 at 25 C", "area resistance of Nafion 212 at 25 C", "vanadium permeability of Nafion 117", "vanadium permeability of Nafion 212"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "vanadium permeability of Nafion 117 = 1.8e-07 cm2/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeability of Nafion 117 = 1.8e-07 cm2/s; vanadium permeability of Nafion 212 = 3.9e-07 cm2/s Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of N
```
#### Evidence 5
- evidence_id: `Nafion 117|Nafion 212|capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C|capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C|vanadium crossover`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.51875`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: CAUSES_OR_AFFECTS
Short claim: Nafion 117, Nafion 212 is linked to capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle, capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle, vanadium crossover. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle", "vanadium crossover", "capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C"]
Values: ["capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle; capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle; vanadium crossover Relation type: CAUSES_OR_AFFECTS Readable labels: Nafion 117; Nafion 212; capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle; capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle; vanadium crossover Description: Vanadium crossover causes capacity fade; Nafion 117 with lower permeability has a capacity fade rate of 0.08%/cycle, while Nafion 212 with higher permeability has 0.18%/cycle at 100 mA/cm2 and 25 C. Source evidence: the capacity fade rate attributable to vanadium crossove
```

## DOC01-QA-001 / chem_prompt_graph
- Category: `measurement`
- Answerable: `True`
- Question: What is the area-specific resistance of Nafion 117 at 25 C?
- Reference answer: 1.65 ohm cm2
- Generated answer: 1.65 ohm cm2
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly states the area-specific resistance of Nafion 117 at 25 C as 1.65 ohm cm2, matching the reference answer exactly. It covers the required key point completely and contains no unsupported claims.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|area resistance (Nafion 117, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.6875`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported area resistance (Nafion 117, 25°C) = 1.65 ohm cm2, area resistance (Nafion 117, 25°C).
Entities: ["Nafion 117"]
Metrics: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2", "area resistance (Nafion 117, 25°C)"]
Values: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 117; area resistance (Nafion 117, 25°C) = 1.65 ohm cm2 Relation type: OPERATION Readable labels: Nafion 117; area resistance (Nafion 117, 25°C) = 1.65 ohm cm2 Description: Area resistance of Nafion 117 at 25°C is 1.65 ohm cm2 Source evidence: Area resistance of Nafion 117 at 25°C is 1.65 ohm cm2

```
#### Evidence 2
- evidence_id: `Nafion 117|area resistance (Nafion 117, 40°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.59375`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported area resistance (Nafion 117, 40°C) = 1.32 ohm cm2, area resistance (Nafion 117, 40°C).
Entities: ["Nafion 117"]
Metrics: ["area resistance (Nafion 117, 40°C) = 1.32 ohm cm2", "area resistance (Nafion 117, 40°C)"]
Values: ["area resistance (Nafion 117, 40°C) = 1.32 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 117; area resistance (Nafion 117, 40°C) = 1.32 ohm cm2 Relation type: OPERATION Readable labels: Nafion 117; area resistance (Nafion 117, 40°C) = 1.32 ohm cm2 Description: Area resistance of Nafion 117 at 40°C is 1.32 ohm cm2 Source evidence: Area resistance of Nafion 117 at 40°C is 1.32 ohm cm2

```
#### Evidence 3
- evidence_id: `operating temperature|voltage efficiency (Nafion 117, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.5625`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under operating temperature, the entity achieved/reported voltage efficiency (Nafion 117, 25°C).
Entities: []
Metrics: ["voltage efficiency (Nafion 117, 25°C)"]
Values: []
Conditions: ["operating temperature"]
Raw support excerpt: operating temperature; voltage efficiency (Nafion 117, 25°C) Relation type: OPERATION Readable labels: operating temperature; voltage efficiency (Nafion 117, 25°C) Description: Higher temperature improves VE of Nafion 117 due to lower resistance Source evidence: Higher temperature improves VE of Nafion 117 due to lower resistance

```
#### Evidence 4
- evidence_id: `Nafion 117|thickness (Nafion 117)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 117, thickness (Nafion 117) = 183 um, thickness (Nafion 117). Conditions: not explicitly stated.
Entities: ["Nafion 117", "thickness (Nafion 117) = 183 um", "thickness (Nafion 117)"]
Metrics: []
Values: ["thickness (Nafion 117) = 183 um"]
Conditions: []
Raw support excerpt: Nafion 117; thickness (Nafion 117) = 183 um Relation type: OPERATION Readable labels: Nafion 117; thickness (Nafion 117) = 183 um Description: Measured thickness of Nafion 117 is 183 um Source evidence: Measured thickness of Nafion 117 is 183 um

```
#### Evidence 5
- evidence_id: `Nafion 117|equivalent weight (Nafion 117)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 117, equivalent weight (Nafion 117) = 1100 g/equiv, equivalent weight (Nafion 117). Conditions: not explicitly stated.
Entities: ["Nafion 117", "equivalent weight (Nafion 117) = 1100 g/equiv", "equivalent weight (Nafion 117)"]
Metrics: []
Values: ["equivalent weight (Nafion 117) = 1100 g/equiv"]
Conditions: []
Raw support excerpt: Nafion 117; equivalent weight (Nafion 117) = 1100 g/equiv Relation type: OPERATION Readable labels: Nafion 117; equivalent weight (Nafion 117) = 1100 g/equiv Description: Equivalent weight of Nafion 117 is 1100 g/equiv Source evidence: Equivalent weight of Nafion 117 is 1100 g/equiv

```

## DOC01-QA-001 / chem_prompt_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: What is the area-specific resistance of Nafion 117 at 25 C?
- Reference answer: 1.65 ohm cm2
- Generated answer: 1.65 ohm cm2
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly provides the area-specific resistance value of 1.65 ohm cm2, matching the reference answer. It directly answers the question without any unsupported claims. The citation supports the claim. Therefore, the answer is good.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|area resistance (Nafion 117, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.6875`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported area resistance (Nafion 117, 25°C) = 1.65 ohm cm2, area resistance (Nafion 117, 25°C).
Entities: ["Nafion 117"]
Metrics: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2", "area resistance (Nafion 117, 25°C)"]
Values: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 117; area resistance (Nafion 117, 25°C) = 1.65 ohm cm2 Relation type: OPERATION Readable labels: Nafion 117; area resistance (Nafion 117, 25°C) = 1.65 ohm cm2 Description: Area resistance of Nafion 117 at 25°C is 1.65 ohm cm2 Source evidence: Area resistance of Nafion 117 at 25°C is 1.65 ohm cm2

```
#### Evidence 2
- evidence_id: `Nafion 117|area resistance (Nafion 117, 40°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.59375`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported area resistance (Nafion 117, 40°C) = 1.32 ohm cm2, area resistance (Nafion 117, 40°C).
Entities: ["Nafion 117"]
Metrics: ["area resistance (Nafion 117, 40°C) = 1.32 ohm cm2", "area resistance (Nafion 117, 40°C)"]
Values: ["area resistance (Nafion 117, 40°C) = 1.32 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 117; area resistance (Nafion 117, 40°C) = 1.32 ohm cm2 Relation type: OPERATION Readable labels: Nafion 117; area resistance (Nafion 117, 40°C) = 1.32 ohm cm2 Description: Area resistance of Nafion 117 at 40°C is 1.32 ohm cm2 Source evidence: Area resistance of Nafion 117 at 40°C is 1.32 ohm cm2

```
#### Evidence 3
- evidence_id: `Nafion 117|Nafion 212|area resistance (Nafion 117, 25°C)|area resistance (Nafion 212, 25°C)|capacity fade rate (Nafion 117)|capacity fade rate (Nafion 212)|coulombic efficiency (Nafion 117, 25°C)|coulombic efficiency (Nafion 212, 25°C)|energy efficiency (Nafion 117, 25°C)|energy efficiency (Nafion 212, 25°C)|ion exchange capacity (Nafion 117)|ion exchange capacity (Nafion 212)|thickness (Nafion 117)|thickness (Nafion 212)|vanadium permeability (Nafion 117)|vanadium permeability (Nafion 212)|voltage efficiency (Nafion 117, 25°C)|voltage efficiency (Nafion 212, 25°C)|water uptake (Nafion 117)|water uptake (Nafion 212)`
- relation_type: `COMPARISON`
- retrieval_score: `0.575`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under the reported conditions, area resistance (Nafion 117, 25°C) = 1.65 ohm cm2, while area resistance (Nafion 212, 25°C) = 0.85 ohm cm2. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "thickness (Nafion 117) = 183 um", "thickness (Nafion 212) = 50.8 um", "water uptake (Nafion 117) = 22 %", "water uptake (Nafion 212) = 25 %", "thickness (Nafion 117)", "thickness (Nafion 212)", "water uptake (Nafion 117)", "water uptake (Nafion 212)"]
Metrics: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2", "area resistance (Nafion 212, 25°C) = 0.85 ohm cm2", "capacity fade rate (Nafion 117) = 0.08 % per cycle", "capacity fade rate (Nafion 212) = 0.18 % per cycle", "coulombic efficiency (Nafion 117, 25°C)", "coulombic efficiency (Nafion 212, 25°C)", "energy efficiency (Nafion 117, 25°C)", "energy efficiency (Nafion 212, 25°C)", "ion exchange capacity (Nafion 117) = 0.91 mmol/g", "ion exchange capacity (Nafion 212) = 0.91 mmol/g", "vanadium permeability (Nafion 117) = 1.8e-07 cm2/s", "vanadium permeability (Nafion 212) = 3.9e-07 cm2/s"]
Values: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2", "area resistance (Nafion 212, 25°C) = 0.85 ohm cm2", "capacity fade rate (Nafion 117) = 0.08 % per cycle", "capacity fade rate (Nafion 212) = 0.18 % per cycle", "ion exchange capacity (Nafion 117) = 0.91 mmol/g", "ion exchange capacity (Nafion 212) = 0.91 mmol/g", "thickness (Nafion 117) = 183 um", "thickness (Nafion 212) = 50.8 um", "vanadium permeability (Nafion 117) = 1.8e-07 cm2/s", "vanadium perm
```
#### Evidence 4
- evidence_id: `operating temperature|voltage efficiency (Nafion 117, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.5625`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under operating temperature, the entity achieved/reported voltage efficiency (Nafion 117, 25°C).
Entities: []
Metrics: ["voltage efficiency (Nafion 117, 25°C)"]
Values: []
Conditions: ["operating temperature"]
Raw support excerpt: operating temperature; voltage efficiency (Nafion 117, 25°C) Relation type: OPERATION Readable labels: operating temperature; voltage efficiency (Nafion 117, 25°C) Description: Higher temperature improves VE of Nafion 117 due to lower resistance Source evidence: Higher temperature improves VE of Nafion 117 due to lower resistance

```
#### Evidence 5
- evidence_id: `Nafion 117|thickness (Nafion 117)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 117, thickness (Nafion 117) = 183 um, thickness (Nafion 117). Conditions: not explicitly stated.
Entities: ["Nafion 117", "thickness (Nafion 117) = 183 um", "thickness (Nafion 117)"]
Metrics: []
Values: ["thickness (Nafion 117) = 183 um"]
Conditions: []
Raw support excerpt: Nafion 117; thickness (Nafion 117) = 183 um Relation type: OPERATION Readable labels: Nafion 117; thickness (Nafion 117) = 183 um Description: Measured thickness of Nafion 117 is 183 um Source evidence: Measured thickness of Nafion 117 is 183 um

```

## DOC01-QA-001 / chem_norm_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: What is the area-specific resistance of Nafion 117 at 25 C?
- Reference answer: 1.65 ohm cm2
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Nafion 117 area-specific resistance at 25 C is 1.65 ohm cm2"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer abstains from answering, stating it does not know. The question is answerable and the reference answer is 1.65 ohm cm2. The answer provides no correct information, covers none of the required key points, and is not useful. Therefore, it is rated as POOR.

### Evidence Blocks
#### Evidence 1
- evidence_id: `membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.59375`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Evidence reports Nafion 117, Nafion 212, membrane:nafion_117, membrane:nafion_212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212 Description: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures. Source evidence: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures.

```
#### Evidence 2
- evidence_id: `membrane:nafion_117|membrane:nafion_212|metric:equivalent_weight|metric:ion_exchange_capacity|metric:thickness_of_nafion_117|metric:thickness_of_nafion_212|metric:vanadium_permeability_of_nafion_117|metric:vanadium_permeability_of_nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.59375`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under the reported conditions, ion exchange capacity = 0.91 mmol/g, while vanadium permeability of Nafion 117 = 1.8e-07 cm²/s. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "equivalent weight = 1100 g/equiv", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "membrane:nafion_117", "membrane:nafion_212", "metric:equivalent_weight", "metric:thickness_of_nafion_117", "metric:thickness_of_nafion_212"]
Metrics: ["ion exchange capacity = 0.91 mmol/g", "vanadium permeability of Nafion 117 = 1.8e-07 cm²/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm²/s", "metric:ion_exchange_capacity", "metric:vanadium_permeability_of_nafion_117", "metric:vanadium_permeability_of_nafion_212"]
Values: ["equivalent weight = 1100 g/equiv", "ion exchange capacity = 0.91 mmol/g", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "vanadium permeability of Nafion 117 = 1.8e-07 cm²/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm²/s"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; equivalent weight = 1100 g/equiv; ion exchange capacity = 0.91 mmol/g; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeability of Nafion 117 = 1.8e-07 cm²/s; vanadium permeability of Nafion 212 = 3.9e-07 cm²/s Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212; equivalent weight = 1100 g/equiv; ion exchange capacity = 0.91 mmol/g; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeabilit
```
#### Evidence 3
- evidence_id: `condition:current_density|condition:temperature|membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.53125`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under temperature, condition:temperature, current density, while condition:current_density. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: ["temperature", "condition:temperature"]
Raw support excerpt: current density; temperature; Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: current density; temperature; Nafion 117; Nafion 212 Description: Comprehensive comparison of Nafion 117 and Nafion 212 membranes across current densities (40-200 mA/cm2) and temperatures (25-40 C) for coulombic, voltage, and energy efficiency. Source evidence: At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%.

```
#### Evidence 4
- evidence_id: `membrane:nafion_117|metric:thickness_of_nafion_117`
- relation_type: `COMPOSITION`
- retrieval_score: `0.5`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: COMPOSITION
Short claim: Evidence reports Nafion 117, thickness of Nafion 117 = 183 um, membrane:nafion_117, metric:thickness_of_nafion_117. Conditions: not explicitly stated.
Entities: ["Nafion 117", "thickness of Nafion 117 = 183 um", "membrane:nafion_117", "metric:thickness_of_nafion_117"]
Metrics: []
Values: ["thickness of Nafion 117 = 183 um"]
Conditions: []
Raw support excerpt: Nafion 117; thickness of Nafion 117 = 183 um Relation type: COMPOSITION Readable labels: Nafion 117; thickness of Nafion 117 = 183 um Description: Nafion 117 has a thickness of 183 um, which is a key property. Source evidence: Nafion 117 has a thickness of 183 um, which is a key property.

```
#### Evidence 5
- evidence_id: `electrode:graphite_felt|membrane:nafion_117|system:electrochemical_workstation|system:flow_meter|system:peristaltic_pump|system:pressure_sensor|system:ptfe_gasket`
- relation_type: `OPERATION`
- retrieval_score: `0.410714`
```text
Evidence 5
Source: chunk-hyperrag-DOC04
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 117, electrochemical workstation, flow meter, peristaltic pump, pressure sensor, PTFE gasket. Conditions: graphite felt, electrode:graphite_felt.
Entities: ["Nafion 117", "electrochemical workstation", "flow meter", "peristaltic pump", "pressure sensor", "PTFE gasket", "membrane:nafion_117", "system:electrochemical_workstation", "system:flow_meter", "system:peristaltic_pump", "system:pressure_sensor", "system:ptfe_gasket"]
Metrics: []
Values: []
Conditions: ["graphite felt", "electrode:graphite_felt"]
Raw support excerpt: graphite felt; Nafion 117; electrochemical workstation; flow meter; peristaltic pump; pressure sensor; PTFE gasket Relation type: OPERATION Readable labels: graphite felt; Nafion 117; electrochemical workstation; flow meter; peristaltic pump; pressure sensor; PTFE gasket Description: Components of VRFB test cell and system: graphite felt electrodes, Nafion 117 membrane, PTFE gaskets, peristaltic pump, electrochemical workstation, pressure sensor, flow meter. Source evidence: Single-cell VRFB tests were conducted using graphite felt electrodes and Nafion 117 membrane as the separator.

```

## DOC01-QA-002 / text_segments
- Category: `measurement`
- Answerable: `True`
- Question: What is the vanadium permeability of Nafion 212?
- Reference answer: 3.9 x 10^-7 cm2/s
- Generated answer: 3.9 x 10^-7 cm2/s
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer exactly matches the reference answer and covers the required key point. It is concise, correct, and supported by the cited evidence. No unsupported claims or hallucinations are present.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC10`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.75`
```text
Evidence 1
Source: DOC10
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: The area-specific resistance (ASR) of the membrane directly impacts energy efficiency at a given current density. At 100 mA/cm2, a SPEEK membrane with 42% sulfonation degree achieved an EE of 83% compared to 84% for Nafion 117, but reduced the capacity fade rate from 0.035%/cycle to 0.018%/cycle. A nanoporous ceramic-polymer composite membrane demonstrated improved lead rejection (selectivity 93%) with an ASR of 3.2 ohm cm2, achieving an EE of 74% at 30 mA/cm2 compared to 76% with Nafion 117 but with reduced capacity fade from 0.08%/cycle to 0.04%/cycle. The quantitative performance comparison at matched conditions shows that ORFB systems with optimized molecular design achieve the highest energy efficiency (76-88%) and lowest capacity fade rates (0.01-0.018%/cycle), followed closely by advanced VRFB configurations (EE 78-84%, fade 0.018-0.035%/cycle).

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.642857`
```text
Evidence 2
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Our results demonstrate that Nafion 117, with its greater membrane thickness of approximately 183 um, consistently achieves superior coulombic efficiency (96-98%) due to reduced vanadium crossover, while Nafion 212, at approximately 50.8 um thickness, exhibits higher voltage efficiency (84-88%) stemming from lower area-specific resistance. The approximately 3-4 percentage point gap between Nafion 212 and Nafion 117 CE values at any given current density directly reflects the twofold difference in vanadium permeability between the two membranes. Based on the measured permeability values and the electrolyte volumes employed, the capacity fade rate attributable to vanadium crossover alone is estimated at approximately 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212 under standard operating conditions at 100 mA/cm2 and 25 C. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.642857`
```text
Evidence 3
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. | Membrane | IEC (mmol/g) | Water Uptake (%) | Area Resistance (ohm cm2) | Vanadium Permeability (x 10^-7 cm2/s) | |---|---|---|---|---| | PBI | 0.0 | 12 | 2.45 | 0.50 | | SNPBI-1.42 | 1.42 | 18 | 1.15 | 0.95 | | SPEEK/APK | 1.26 | 21 | 1.38 | 2.10 | | SPTPC-2.59 | 2.59 | 28 | 0.82 | 3.20 | ### 3.2 Area-Specific Resistance The area-specific resistance values showed a strong inverse correlation with IEC. ### 5.3 Resistance-EE and Permeability-EE Correlations Multiple linear regression analysis of the performance data reveals that energy efficiency at 100 mA/cm2 can be predicted from area resistance and vanadium permeability with good accuracy. The quantitative relationships between IEC, resistance, permeability, and energy efficiency provide a framework for rational design of next-generation non-fluorinated VRFB membranes.

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC05`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.535714`
```text
Evidence 4
Source: DOC05
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a comprehensive experimental investigation into the temperature-dependent behavior of VRFB cells operated at 25 C, 40 C, and 60 C over 500 charge-discharge cycles at a constant current density of 80 mA/cm2. The results demonstrate that elevated temperatures accelerate vanadium ion crossover through the ion-exchange membrane, exacerbate state-of-charge (SOC) imbalance between the positive and negative half-cells, and precipitate more rapid capacity fading. The precipitation of V(V) species as V2O5 at the positive electrode, particularly when local temperatures exceed solubility limits, introduces additional capacity loss mechanisms that may be partially irreversible. Post-test analysis of the electrolyte revealed significant redistribution of vanadium species between the half-cells, consistent with enhanced crossover as a primary contributor to the observed capacity loss.

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC09`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.535714`
```text
Evidence 5
Source: DOC09
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: The crossover rate of TEMPO through the Nafion 117 membrane was measured at 0.8 x 10^-6 cm2/s, contributing to a gradual capacity fade over extended cycling. Under standardized conditions (100 mA/cm2, Nafion 117 membrane, room temperature, 500 cycle duration), the capacity fade rates were: AQDS at pH 12 showed 0.025%/cycle, TEMPO in nonaqueous electrolyte showed 0.02%/cycle, PSV (functionalized viologen) showed 0.018%/cycle, MV at pH 7 showed 0.055%/cycle, and unfunctionalized TEMPO in the presence of 50 ppm water showed 0.045%/cycle. Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2: Nafion 117 (selectivity 88%, MV crossover 2.1 x 10^-6 cm2/s, capacity fade 0.055%/cycle), Nafion 212 (selectivity 85%, MV crossover 2.5 x 10^-6 cm2/s, capacity fade 0.065%/cycle), a sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation (selectivity 92%, MV crossover 1.2 x 10^-6 cm2/s, capacity fade 0.038%/cycle), a commercial anion exchange membrane (selectivity 90%, MV crossover 1.5 x 10^-6 cm2/s, capacity fade 0.042%/cycle), and a nanoporous size-exclusion membrane (selectivity 97%, MV crossover 0.3 x 10^-6 cm2/s, capacity fade 0.012%/cycle). However, this membrane also exhibited higher area-specific resistance (2.8 ohm cm2 compared to 1.8 ohm cm2 for Nafion 117), resulting in a lower EE of 78.5% compared to 80.2% for Nafion at 100 mA/cm2.

```

## DOC01-QA-002 / original_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: What is the vanadium permeability of Nafion 212?
- Reference answer: 3.9 x 10^-7 cm2/s
- Generated answer: 3.9e-07 cm2/s
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly provides the vanadium permeability of Nafion 212 as 3.9e-07 cm2/s, which matches the reference answer and covers the required key point. No unsupported claims are present. The answer is concise and accurate.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 212|vanadium permeability of Nafion 212`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.785714`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: ASSOCIATED_WITH
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported vanadium permeability of Nafion 212 = 3.9e-07 cm2/s, vanadium permeability of Nafion 212.
Entities: ["Nafion 212"]
Metrics: ["vanadium permeability of Nafion 212 = 3.9e-07 cm2/s", "vanadium permeability of Nafion 212"]
Values: ["vanadium permeability of Nafion 212 = 3.9e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 212; vanadium permeability of Nafion 212 = 3.9e-07 cm2/s Relation type: ASSOCIATED_WITH Readable labels: Nafion 212; vanadium permeability of Nafion 212 = 3.9e-07 cm2/s Description: Nafion 212 has vanadium permeability of 3.9e-07 cm2/s. Source evidence: Nafion 212 has vanadium permeability of 3.9e-07 cm2/s.

```
#### Evidence 2
- evidence_id: `Nafion 117|Nafion 212|area resistance of Nafion 117 at 25 C|area resistance of Nafion 212 at 25 C|thickness of Nafion 117|thickness of Nafion 212|vanadium permeability of Nafion 117|vanadium permeability of Nafion 212`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.705357`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under the reported conditions, area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, while area resistance of Nafion 212 at 25 C = 0.85 ohm cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "thickness of Nafion 117", "thickness of Nafion 212"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "vanadium permeability of Nafion 117 = 1.8e-07 cm2/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm2/s", "area resistance of Nafion 117 at 25 C", "area resistance of Nafion 212 at 25 C", "vanadium permeability of Nafion 117", "vanadium permeability of Nafion 212"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "vanadium permeability of Nafion 117 = 1.8e-07 cm2/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeability of Nafion 117 = 1.8e-07 cm2/s; vanadium permeability of Nafion 212 = 3.9e-07 cm2/s Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of N
```
#### Evidence 3
- evidence_id: `Nafion 117|Nafion 212|capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C|capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C|vanadium crossover`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.692857`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: CAUSES_OR_AFFECTS
Short claim: Nafion 117, Nafion 212 is linked to capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle, capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle, vanadium crossover. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle", "vanadium crossover", "capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C"]
Values: ["capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle; capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle; vanadium crossover Relation type: CAUSES_OR_AFFECTS Readable labels: Nafion 117; Nafion 212; capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle; capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle; vanadium crossover Description: Vanadium crossover causes capacity fade; Nafion 117 with lower permeability has a capacity fade rate of 0.08%/cycle, while Nafion 212 with higher permeability has 0.18%/cycle at 100 mA/cm2 and 25 C. Source evidence: the capacity fade rate attributable to vanadium crossove
```
#### Evidence 4
- evidence_id: `Nafion 212|vanadium redox flow battery`
- relation_type: `PART_OF`
- retrieval_score: `0.660714`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: PART_OF
Short claim: Evidence reports Nafion 212, vanadium redox flow battery. Conditions: not explicitly stated.
Entities: ["Nafion 212", "vanadium redox flow battery"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 212; vanadium redox flow battery Relation type: PART_OF Readable labels: Nafion 212; vanadium redox flow battery Description: Nafion 212 is used as a membrane in a vanadium redox flow battery. Source evidence: Nafion 212 is used as a membrane in a vanadium redox flow battery.

```
#### Evidence 5
- evidence_id: `Nafion 117|Nafion 212|carbon felt electrodes SGL GFD 4.6 EA|electrolyte|vanadium redox flow battery`
- relation_type: `PART_OF`
- retrieval_score: `0.585714`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: PART_OF
Short claim: Evidence reports Nafion 117, Nafion 212, carbon felt electrodes SGL GFD 4.6 EA, electrolyte, vanadium redox flow battery. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212", "carbon felt electrodes SGL GFD 4.6 EA", "electrolyte", "vanadium redox flow battery"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; carbon felt electrodes SGL GFD 4.6 EA; electrolyte; vanadium redox flow battery Relation type: PART_OF Readable labels: Nafion 117; Nafion 212; carbon felt electrodes SGL GFD 4.6 EA; electrolyte; vanadium redox flow battery Description: A vanadium redox flow battery consists of a membrane (Nafion 117 or Nafion 212), carbon felt electrodes, and electrolyte. Source evidence: Carbon felt electrodes (SGL GFD 4.6 EA) were employed on both positive and negative sides... The electrolyte consisted of 1.6 M total vanadium

```

## DOC01-QA-002 / chem_prompt_graph
- Category: `measurement`
- Answerable: `True`
- Question: What is the vanadium permeability of Nafion 212?
- Reference answer: 3.9 x 10^-7 cm2/s
- Generated answer: 3.9e-07 cm2/s
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly provides the vanadium permeability of Nafion 212 as 3.9e-07 cm2/s, which matches the reference answer. It is complete, non-hallucinated, and cites supporting evidence.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 212|vanadium permeability (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.767857`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported vanadium permeability (Nafion 212) = 3.9e-07 cm2/s, vanadium permeability (Nafion 212).
Entities: ["Nafion 212"]
Metrics: ["vanadium permeability (Nafion 212) = 3.9e-07 cm2/s", "vanadium permeability (Nafion 212)"]
Values: ["vanadium permeability (Nafion 212) = 3.9e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 212; vanadium permeability (Nafion 212) = 3.9e-07 cm2/s Relation type: OPERATION Readable labels: Nafion 212; vanadium permeability (Nafion 212) = 3.9e-07 cm2/s Description: Vanadium permeability of Nafion 212 is 3.9e-7 cm2/s Source evidence: Vanadium permeability of Nafion 212 is 3.9e-7 cm2/s

```
#### Evidence 2
- evidence_id: `Nafion 212|thickness (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.553571`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 212, thickness (Nafion 212) = 50.8 um, thickness (Nafion 212). Conditions: not explicitly stated.
Entities: ["Nafion 212", "thickness (Nafion 212) = 50.8 um", "thickness (Nafion 212)"]
Metrics: []
Values: ["thickness (Nafion 212) = 50.8 um"]
Conditions: []
Raw support excerpt: Nafion 212; thickness (Nafion 212) = 50.8 um Relation type: OPERATION Readable labels: Nafion 212; thickness (Nafion 212) = 50.8 um Description: Measured thickness of Nafion 212 is 50.8 um Source evidence: Measured thickness of Nafion 212 is 50.8 um

```
#### Evidence 3
- evidence_id: `Nafion 212|equivalent weight (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.553571`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 212, equivalent weight (Nafion 212) = 1100 g/equiv, equivalent weight (Nafion 212). Conditions: not explicitly stated.
Entities: ["Nafion 212", "equivalent weight (Nafion 212) = 1100 g/equiv", "equivalent weight (Nafion 212)"]
Metrics: []
Values: ["equivalent weight (Nafion 212) = 1100 g/equiv"]
Conditions: []
Raw support excerpt: Nafion 212; equivalent weight (Nafion 212) = 1100 g/equiv Relation type: OPERATION Readable labels: Nafion 212; equivalent weight (Nafion 212) = 1100 g/equiv Description: Equivalent weight of Nafion 212 is 1100 g/equiv Source evidence: Equivalent weight of Nafion 212 is 1100 g/equiv

```
#### Evidence 4
- evidence_id: `Nafion 212|area resistance (Nafion 212, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.553571`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported area resistance (Nafion 212, 25°C) = 0.85 ohm cm2, area resistance (Nafion 212, 25°C).
Entities: ["Nafion 212"]
Metrics: ["area resistance (Nafion 212, 25°C) = 0.85 ohm cm2", "area resistance (Nafion 212, 25°C)"]
Values: ["area resistance (Nafion 212, 25°C) = 0.85 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 212; area resistance (Nafion 212, 25°C) = 0.85 ohm cm2 Relation type: OPERATION Readable labels: Nafion 212; area resistance (Nafion 212, 25°C) = 0.85 ohm cm2 Description: Area resistance of Nafion 212 at 25°C is 0.85 ohm cm2 Source evidence: Area resistance of Nafion 212 at 25°C is 0.85 ohm cm2

```
#### Evidence 5
- evidence_id: `Nafion 212|water uptake (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.553571`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 212, water uptake (Nafion 212) = 25 %, water uptake (Nafion 212). Conditions: not explicitly stated.
Entities: ["Nafion 212", "water uptake (Nafion 212) = 25 %", "water uptake (Nafion 212)"]
Metrics: []
Values: ["water uptake (Nafion 212) = 25 %"]
Conditions: []
Raw support excerpt: Nafion 212; water uptake (Nafion 212) = 25 % Relation type: OPERATION Readable labels: Nafion 212; water uptake (Nafion 212) = 25 % Description: Water uptake of Nafion 212 is 25% Source evidence: Water uptake of Nafion 212 is 25%

```

## DOC01-QA-002 / chem_prompt_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: What is the vanadium permeability of Nafion 212?
- Reference answer: 3.9 x 10^-7 cm2/s
- Generated answer: 3.9e-07 cm2/s
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly provides the vanadium permeability of Nafion 212 as 3.9e-07 cm2/s, which matches the reference answer exactly. The required key point is fully covered, no unsupported claims are present, and the answer is grounded by citations. Therefore, the answer is correct, complete, and non-hallucinated.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 212|vanadium permeability (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.767857`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported vanadium permeability (Nafion 212) = 3.9e-07 cm2/s, vanadium permeability (Nafion 212).
Entities: ["Nafion 212"]
Metrics: ["vanadium permeability (Nafion 212) = 3.9e-07 cm2/s", "vanadium permeability (Nafion 212)"]
Values: ["vanadium permeability (Nafion 212) = 3.9e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 212; vanadium permeability (Nafion 212) = 3.9e-07 cm2/s Relation type: OPERATION Readable labels: Nafion 212; vanadium permeability (Nafion 212) = 3.9e-07 cm2/s Description: Vanadium permeability of Nafion 212 is 3.9e-7 cm2/s Source evidence: Vanadium permeability of Nafion 212 is 3.9e-7 cm2/s

```
#### Evidence 2
- evidence_id: `Nafion 117|Nafion 212|area resistance (Nafion 117, 25°C)|area resistance (Nafion 212, 25°C)|capacity fade rate (Nafion 117)|capacity fade rate (Nafion 212)|coulombic efficiency (Nafion 117, 25°C)|coulombic efficiency (Nafion 212, 25°C)|energy efficiency (Nafion 117, 25°C)|energy efficiency (Nafion 212, 25°C)|ion exchange capacity (Nafion 117)|ion exchange capacity (Nafion 212)|thickness (Nafion 117)|thickness (Nafion 212)|vanadium permeability (Nafion 117)|vanadium permeability (Nafion 212)|voltage efficiency (Nafion 117, 25°C)|voltage efficiency (Nafion 212, 25°C)|water uptake (Nafion 117)|water uptake (Nafion 212)`
- relation_type: `COMPARISON`
- retrieval_score: `0.655357`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under the reported conditions, area resistance (Nafion 117, 25°C) = 1.65 ohm cm2, while area resistance (Nafion 212, 25°C) = 0.85 ohm cm2. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "thickness (Nafion 117) = 183 um", "thickness (Nafion 212) = 50.8 um", "water uptake (Nafion 117) = 22 %", "water uptake (Nafion 212) = 25 %", "thickness (Nafion 117)", "thickness (Nafion 212)", "water uptake (Nafion 117)", "water uptake (Nafion 212)"]
Metrics: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2", "area resistance (Nafion 212, 25°C) = 0.85 ohm cm2", "capacity fade rate (Nafion 117) = 0.08 % per cycle", "capacity fade rate (Nafion 212) = 0.18 % per cycle", "coulombic efficiency (Nafion 117, 25°C)", "coulombic efficiency (Nafion 212, 25°C)", "energy efficiency (Nafion 117, 25°C)", "energy efficiency (Nafion 212, 25°C)", "ion exchange capacity (Nafion 117) = 0.91 mmol/g", "ion exchange capacity (Nafion 212) = 0.91 mmol/g", "vanadium permeability (Nafion 117) = 1.8e-07 cm2/s", "vanadium permeability (Nafion 212) = 3.9e-07 cm2/s"]
Values: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2", "area resistance (Nafion 212, 25°C) = 0.85 ohm cm2", "capacity fade rate (Nafion 117) = 0.08 % per cycle", "capacity fade rate (Nafion 212) = 0.18 % per cycle", "ion exchange capacity (Nafion 117) = 0.91 mmol/g", "ion exchange capacity (Nafion 212) = 0.91 mmol/g", "thickness (Nafion 117) = 183 um", "thickness (Nafion 212) = 50.8 um", "vanadium permeability (Nafion 117) = 1.8e-07 cm2/s", "vanadium perm
```
#### Evidence 3
- evidence_id: `Nafion 212|thickness (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.553571`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 212, thickness (Nafion 212) = 50.8 um, thickness (Nafion 212). Conditions: not explicitly stated.
Entities: ["Nafion 212", "thickness (Nafion 212) = 50.8 um", "thickness (Nafion 212)"]
Metrics: []
Values: ["thickness (Nafion 212) = 50.8 um"]
Conditions: []
Raw support excerpt: Nafion 212; thickness (Nafion 212) = 50.8 um Relation type: OPERATION Readable labels: Nafion 212; thickness (Nafion 212) = 50.8 um Description: Measured thickness of Nafion 212 is 50.8 um Source evidence: Measured thickness of Nafion 212 is 50.8 um

```
#### Evidence 4
- evidence_id: `Nafion 212|equivalent weight (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.553571`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 212, equivalent weight (Nafion 212) = 1100 g/equiv, equivalent weight (Nafion 212). Conditions: not explicitly stated.
Entities: ["Nafion 212", "equivalent weight (Nafion 212) = 1100 g/equiv", "equivalent weight (Nafion 212)"]
Metrics: []
Values: ["equivalent weight (Nafion 212) = 1100 g/equiv"]
Conditions: []
Raw support excerpt: Nafion 212; equivalent weight (Nafion 212) = 1100 g/equiv Relation type: OPERATION Readable labels: Nafion 212; equivalent weight (Nafion 212) = 1100 g/equiv Description: Equivalent weight of Nafion 212 is 1100 g/equiv Source evidence: Equivalent weight of Nafion 212 is 1100 g/equiv

```
#### Evidence 5
- evidence_id: `Nafion 212|area resistance (Nafion 212, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.553571`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported area resistance (Nafion 212, 25°C) = 0.85 ohm cm2, area resistance (Nafion 212, 25°C).
Entities: ["Nafion 212"]
Metrics: ["area resistance (Nafion 212, 25°C) = 0.85 ohm cm2", "area resistance (Nafion 212, 25°C)"]
Values: ["area resistance (Nafion 212, 25°C) = 0.85 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 212; area resistance (Nafion 212, 25°C) = 0.85 ohm cm2 Relation type: OPERATION Readable labels: Nafion 212; area resistance (Nafion 212, 25°C) = 0.85 ohm cm2 Description: Area resistance of Nafion 212 at 25°C is 0.85 ohm cm2 Source evidence: Area resistance of Nafion 212 at 25°C is 0.85 ohm cm2

```

## DOC01-QA-002 / chem_norm_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: What is the vanadium permeability of Nafion 212?
- Reference answer: 3.9 x 10^-7 cm2/s
- Generated answer: 3.9e-07 cm²/s
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly provides the vanadium permeability of Nafion 212 as 3.9e-07 cm²/s, which matches the reference answer. It covers the required key point completely. No unsupported claims. The answer is grounded by citation.

### Evidence Blocks
#### Evidence 1
- evidence_id: `membrane:nafion_212|metric:vanadium_permeability_of_nafion_212`
- relation_type: `COMPOSITION`
- retrieval_score: `0.785714`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPOSITION
Short claim: In the reported system, under the stated conditions, Nafion 212, membrane:nafion_212 achieved/reported vanadium permeability of Nafion 212 = 3.9e-07 cm²/s, metric:vanadium_permeability_of_nafion_212.
Entities: ["Nafion 212", "membrane:nafion_212"]
Metrics: ["vanadium permeability of Nafion 212 = 3.9e-07 cm²/s", "metric:vanadium_permeability_of_nafion_212"]
Values: ["vanadium permeability of Nafion 212 = 3.9e-07 cm²/s"]
Conditions: []
Raw support excerpt: Nafion 212; vanadium permeability of Nafion 212 = 3.9e-07 cm²/s Relation type: COMPOSITION Readable labels: Nafion 212; vanadium permeability of Nafion 212 = 3.9e-07 cm²/s Description: Nafion 212 has a measured vanadium permeability of 3.9e-07 cm2/s. Source evidence: Nafion 212 has a measured vanadium permeability of 3.9e-07 cm2/s.

```
#### Evidence 2
- evidence_id: `membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.767857`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Evidence reports Nafion 117, Nafion 212, membrane:nafion_117, membrane:nafion_212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212 Description: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures. Source evidence: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures.

```
#### Evidence 3
- evidence_id: `membrane:nafion_117|membrane:nafion_212|metric:equivalent_weight|metric:ion_exchange_capacity|metric:thickness_of_nafion_117|metric:thickness_of_nafion_212|metric:vanadium_permeability_of_nafion_117|metric:vanadium_permeability_of_nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.705357`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under the reported conditions, ion exchange capacity = 0.91 mmol/g, while vanadium permeability of Nafion 117 = 1.8e-07 cm²/s. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "equivalent weight = 1100 g/equiv", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "membrane:nafion_117", "membrane:nafion_212", "metric:equivalent_weight", "metric:thickness_of_nafion_117", "metric:thickness_of_nafion_212"]
Metrics: ["ion exchange capacity = 0.91 mmol/g", "vanadium permeability of Nafion 117 = 1.8e-07 cm²/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm²/s", "metric:ion_exchange_capacity", "metric:vanadium_permeability_of_nafion_117", "metric:vanadium_permeability_of_nafion_212"]
Values: ["equivalent weight = 1100 g/equiv", "ion exchange capacity = 0.91 mmol/g", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "vanadium permeability of Nafion 117 = 1.8e-07 cm²/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm²/s"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; equivalent weight = 1100 g/equiv; ion exchange capacity = 0.91 mmol/g; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeability of Nafion 117 = 1.8e-07 cm²/s; vanadium permeability of Nafion 212 = 3.9e-07 cm²/s Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212; equivalent weight = 1100 g/equiv; ion exchange capacity = 0.91 mmol/g; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeabilit
```
#### Evidence 4
- evidence_id: `condition:current_density|condition:temperature|membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.491071`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under temperature, condition:temperature, current density, while condition:current_density. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: ["temperature", "condition:temperature"]
Raw support excerpt: current density; temperature; Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: current density; temperature; Nafion 117; Nafion 212 Description: Comprehensive comparison of Nafion 117 and Nafion 212 membranes across current densities (40-200 mA/cm2) and temperatures (25-40 C) for coulombic, voltage, and energy efficiency. Source evidence: At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%.

```
#### Evidence 5
- evidence_id: `membrane:fumatech_fap_450|membrane:microporous_polyolefin_separator|membrane:nafion_115|membrane:nafion_117|membrane:nafion_212|membrane:nanoporous_ceramic_polymer_composite_membrane|membrane:size_exclusion_membrane|unresolved:speek`
- relation_type: `COMPARISON`
- retrieval_score: `0.459821`
```text
Evidence 5
Source: chunk-hyperrag-DOC10
Relation/Type: COMPARISON
Short claim: Evidence reports Fumatech FAP-450, microporous polyolefin separator, Nafion 115, Nafion 117, Nafion 212, size-exclusion membrane. Conditions: nanoporous ceramic-polymer composite membrane.
Entities: ["Fumatech FAP-450", "microporous polyolefin separator", "Nafion 115", "Nafion 117", "Nafion 212", "size-exclusion membrane", "SPEEK", "membrane:fumatech_fap_450", "membrane:microporous_polyolefin_separator", "membrane:nafion_115", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: []
Values: []
Conditions: ["nanoporous ceramic-polymer composite membrane"]
Raw support excerpt: Fumatech FAP-450; microporous polyolefin separator; Nafion 115; Nafion 117; Nafion 212; nanoporous ceramic-polymer composite membrane; size-exclusion membrane; SPEEK Relation type: COMPARISON Readable labels: Fumatech FAP-450; microporous polyolefin separator; Nafion 115; Nafion 117; Nafion 212; nanoporous ceramic-polymer composite membrane; size-exclusion membrane; SPEEK Description: Membrane types across RFB platforms with selectivity requirements above 95% universal; specific membranes compared for each chemistry Source evidence: Membrane selectivity above 95% is required for capacity fade below 0.02%/cycle...SPEEK improved vanadium selectivity...size-exclusion membranes for nonaqueous

```

## DOC01-QA-003 / text_segments
- Category: `measurement`
- Answerable: `True`
- Question: How does the coulombic efficiency of Nafion 117 compare to Nafion 212 at 100 mA/cm2 and 25 C?
- Reference answer: Nafion 117 CE (97.1%) is 3.3 percentage points higher than Nafion 212 CE (93.8%) at 100 mA/cm2 and 25 C
- Generated answer: Nafion 117 exhibits higher coulombic efficiency (97.1%) than Nafion 212 (93.8%) at 100 mA/cm2 and 25 C.
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly states that Nafion 117 has higher coulombic efficiency (97.1%) than Nafion 212 (93.8%) at the specified conditions, covering all required key points. It does not include any unsupported claims and is fully grounded in the reference answer. The citation is present and supports the claim.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.692308`
```text
Evidence 1
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: | Property | Nafion 117 | Nafion 212 | |---|---|---| | Thickness (um) | 183 | 50.8 | | Equivalent weight (g/equiv) | 1100 | 1100 | | Area resistance (ohm cm2, 25 C) | 1.65 | 0.85 | | Vanadium permeability (x 10^-7 cm2/s) | 1.8 | 3.9 | | Water uptake (%) | 22 | 25 | | Ion exchange capacity (mmol/g) | 0.91 | 0.91 | The water uptake values, measured after equilibration in deionized water at 25 C, were 22% for Nafion 117 and 25% for Nafion 212. At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%. Based on the measured permeability values and the electrolyte volumes employed, the capacity fade rate attributable to vanadium crossover alone is estimated at approximately 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212 under standard operating conditions at 100 mA/cm2 and 25 C. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.692308`
```text
Evidence 2
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. At 100 mA/cm2, the CE was 98.1%, which is competitive with Nafion 117 and superior to Nafion 212. At 100 mA/cm2, the EE was 80.5%, which exceeds the performance of both Nafion 117 and Nafion 212 under comparable conditions. ### 5.3 Resistance-EE and Permeability-EE Correlations Multiple linear regression analysis of the performance data reveals that energy efficiency at 100 mA/cm2 can be predicted from area resistance and vanadium permeability with good accuracy.

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC09`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.692308`
```text
Evidence 3
Source: DOC09
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Under standardized conditions (100 mA/cm2, Nafion 117 membrane, room temperature, 500 cycle duration), the capacity fade rates were: AQDS at pH 12 showed 0.025%/cycle, TEMPO in nonaqueous electrolyte showed 0.02%/cycle, PSV (functionalized viologen) showed 0.018%/cycle, MV at pH 7 showed 0.055%/cycle, and unfunctionalized TEMPO in the presence of 50 ppm water showed 0.045%/cycle. Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2: Nafion 117 (selectivity 88%, MV crossover 2.1 x 10^-6 cm2/s, capacity fade 0.055%/cycle), Nafion 212 (selectivity 85%, MV crossover 2.5 x 10^-6 cm2/s, capacity fade 0.065%/cycle), a sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation (selectivity 92%, MV crossover 1.2 x 10^-6 cm2/s, capacity fade 0.038%/cycle), a commercial anion exchange membrane (selectivity 90%, MV crossover 1.5 x 10^-6 cm2/s, capacity fade 0.042%/cycle), and a nanoporous size-exclusion membrane (selectivity 97%, MV crossover 0.3 x 10^-6 cm2/s, capacity fade 0.012%/cycle). However, this membrane also exhibited higher area-specific resistance (2.8 ohm cm2 compared to 1.8 ohm cm2 for Nafion 117), resulting in a lower EE of 78.5% compared to 80.2% for Nafion at 100 mA/cm2. Operating at reduced temperature (15 C rather than 25 C) reduced the capacity fade rate of a MV/TEMPO cell from 0.055%/cycle to 0.032%/cycle, albeit with some performa
```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC05`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.634615`
```text
Evidence 4
Source: DOC05
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a comprehensive experimental investigation into the temperature-dependent behavior of VRFB cells operated at 25 C, 40 C, and 60 C over 500 charge-discharge cycles at a constant current density of 80 mA/cm2. Results and Discussion ### 3.1 Capacity Retention Behavior Across Temperatures The long-term cycling behavior of VRFB cells operated at 25 C, 40 C, and 60 C revealed pronounced temperature-dependent differences in capacity retention trajectories. At 25 C, the measured crossover coefficient was 2.1 x 10^-7 cm2/s, which is in good agreement with literature values for Nafion 117 in contact with vanadium electrolyte solutions. Coulombic efficiency degradation followed a similar temperature dependence, declining from initial values of 97.2%, 97.0%, and 96.8% to final values of 94.8%, 92.1%, and 88.5% at 25 C, 40 C, and 60 C respectively.

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC10`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.634615`
```text
Evidence 5
Source: DOC10
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: With Nafion 117 membrane, VRFBs achieve energy efficiency of 78-84% at current densities of 100-200 mA/cm2. At 100 mA/cm2, a SPEEK membrane with 42% sulfonation degree achieved an EE of 83% compared to 84% for Nafion 117, but reduced the capacity fade rate from 0.035%/cycle to 0.018%/cycle. A benchmark AEM (Fumatech FAP-450) achieved an EE of 79% at 100 mA/cm2 with iron-chromium electrolyte, compared to 82% for Nafion 117, but with significantly improved chromium retention (crossover rate reduced by 40%). A nanoporous ceramic-polymer composite membrane demonstrated improved lead rejection (selectivity 93%) with an ASR of 3.2 ohm cm2, achieving an EE of 74% at 30 mA/cm2 compared to 76% with Nafion 117 but with reduced capacity fade from 0.08%/cycle to 0.04%/cycle.

```

## DOC01-QA-003 / original_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: How does the coulombic efficiency of Nafion 117 compare to Nafion 212 at 100 mA/cm2 and 25 C?
- Reference answer: Nafion 117 CE (97.1%) is 3.3 percentage points higher than Nafion 212 CE (93.8%) at 100 mA/cm2 and 25 C
- Generated answer: At 100 mA/cm² and 25°C, Nafion 117 has a coulombic efficiency of 97.1%, while Nafion 212 has a coulombic efficiency of 93.8%. Thus, Nafion 117 exhibits higher coulombic efficiency than Nafion 212 under these conditions.
- Quality: `SATISFACTORY` | Good: `False` | Satisfactory+: `True` | KPC: `0.6667` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Difference: 3.3 percentage points"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly states the coulombic efficiency values for both Nafion 117 (97.1%) and Nafion 212 (93.8%) at the specified conditions, and correctly indicates that Nafion 117 has higher efficiency. However, it does not explicitly mention the difference of 3.3 percentage points, which is a required key point. The answer is non-hallucinated and partially useful, but incomplete regarding the difference. Therefore, it is rated SATISFACTORY.

### Evidence Blocks
#### Evidence 1
- evidence_id: `CE of Nafion 117 at 100 mA/cm2 and 25 C|CE of Nafion 212 at 100 mA/cm2 and 25 C|EE of Nafion 117 at 100 mA/cm2 and 25 C|EE of Nafion 212 at 100 mA/cm2 and 25 C|Nafion 117|Nafion 212|VE of Nafion 117 at 100 mA/cm2 and 25 C|VE of Nafion 212 at 100 mA/cm2 and 25 C|current density of 100 mA/cm2|temperature 25 C`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.569231`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %, CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %, EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %, EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %, VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %, VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %, temperature 25 C = 25 C, CE of Nafion 117 at 100 mA/cm2 and 25 C, CE of Nafion 212 at 100 mA/cm2 and 25 C, EE of Nafion 117 at 100 mA/cm2 and 25 C, EE of Nafion 212 at 100 mA/cm2 and 25 C, VE of Nafion 117 at 100 mA/cm2 and 25 C, current density of 100 mA/cm2 = 100 mA/cm2, while current density of 100 mA/cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["current density of 100 mA/cm2 = 100 mA/cm2", "current density of 100 mA/cm2"]
Values: ["CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %", "CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %", "EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %", "VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %", "current density of 100 mA/cm2 = 100 mA/cm2", "temperature 25 C = 25 C"]
Conditions: ["CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %", "CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %", "EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %", "VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %", "temperature 25 C = 25 C", "C
```
#### Evidence 2
- evidence_id: `Nafion 117|Nafion 212|capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C|capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C|vanadium crossover`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.561538`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: CAUSES_OR_AFFECTS
Short claim: Nafion 117, Nafion 212 is linked to capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle, capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle, vanadium crossover. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle", "vanadium crossover", "capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C"]
Values: ["capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle; capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle; vanadium crossover Relation type: CAUSES_OR_AFFECTS Readable labels: Nafion 117; Nafion 212; capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle; capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle; vanadium crossover Description: Vanadium crossover causes capacity fade; Nafion 117 with lower permeability has a capacity fade rate of 0.08%/cycle, while Nafion 212 with higher permeability has 0.18%/cycle at 100 mA/cm2 and 25 C. Source evidence: the capacity fade rate attributable to vanadium crossove
```
#### Evidence 3
- evidence_id: `Nafion 117|Nafion 212|area resistance of Nafion 117 at 25 C|area resistance of Nafion 212 at 25 C|thickness of Nafion 117|thickness of Nafion 212|vanadium permeability of Nafion 117|vanadium permeability of Nafion 212`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.524038`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under the reported conditions, area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, while area resistance of Nafion 212 at 25 C = 0.85 ohm cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "thickness of Nafion 117", "thickness of Nafion 212"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "vanadium permeability of Nafion 117 = 1.8e-07 cm2/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm2/s", "area resistance of Nafion 117 at 25 C", "area resistance of Nafion 212 at 25 C", "vanadium permeability of Nafion 117", "vanadium permeability of Nafion 212"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "vanadium permeability of Nafion 117 = 1.8e-07 cm2/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeability of Nafion 117 = 1.8e-07 cm2/s; vanadium permeability of Nafion 212 = 3.9e-07 cm2/s Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of N
```
#### Evidence 4
- evidence_id: `Nafion 117|Nafion 212`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.480769`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Evidence reports Nafion 117, Nafion 212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212 Description: The study systematically compares Nafion 117 and Nafion 212 across various performance metrics and conditions. Source evidence: The study systematically compares Nafion 117 and Nafion 212 across various performance metrics and conditions.

```
#### Evidence 5
- evidence_id: `Nafion 117|Nafion 212|area resistance of Nafion 117 at 25 C|area resistance of Nafion 117 at 40 C|area resistance of Nafion 212 at 25 C|area resistance of Nafion 212 at 40 C|temperature 40 C`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.475275`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under temperature 40 C = 40 C, temperature 40 C, area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, while area resistance of Nafion 117 at 40 C = 1.32 ohm cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "area resistance of Nafion 117 at 25 C", "area resistance of Nafion 117 at 40 C", "area resistance of Nafion 212 at 25 C", "area resistance of Nafion 212 at 40 C"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "temperature 40 C = 40 C"]
Conditions: ["temperature 40 C = 40 C", "temperature 40 C"]
Raw support excerpt: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2; temperature 40 C = 40 C Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2; te
```

## DOC01-QA-003 / chem_prompt_graph
- Category: `measurement`
- Answerable: `True`
- Question: How does the coulombic efficiency of Nafion 117 compare to Nafion 212 at 100 mA/cm2 and 25 C?
- Reference answer: Nafion 117 CE (97.1%) is 3.3 percentage points higher than Nafion 212 CE (93.8%) at 100 mA/cm2 and 25 C
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Nafion 117 CE: 97.1%", "Nafion 212 CE: 93.8%", "Difference: 3.3 percentage points"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer states 'I don't know based on the retrieved evidence' and provides no citations. Since the question is answerable and the reference answer provides the required key points, the model abstained from answering when it should have provided the correct comparison. Therefore, the answer is poor, does not cover any key points, and is not satisfactory.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|Nafion 212`
- relation_type: `COMPARISON`
- retrieval_score: `0.480769`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Evidence reports Nafion 117, Nafion 212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212 Description: Systematic comparison of Nafion 117 and Nafion 212 across multiple metrics Source evidence: Systematic comparison of Nafion 117 and Nafion 212 across multiple metrics

```
#### Evidence 2
- evidence_id: `Nafion 117|coulombic efficiency (Nafion 117, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.471154`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported coulombic efficiency (Nafion 117, 25°C).
Entities: ["Nafion 117"]
Metrics: ["coulombic efficiency (Nafion 117, 25°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 117; coulombic efficiency (Nafion 117, 25°C) Relation type: OPERATION Readable labels: Nafion 117; coulombic efficiency (Nafion 117, 25°C) Description: Coulombic efficiency of Nafion 117 at 25°C ranges 96.0-98.2% Source evidence: Coulombic efficiency of Nafion 117 at 25°C ranges 96.0-98.2%

```
#### Evidence 3
- evidence_id: `Nafion 212|coulombic efficiency (Nafion 212, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.471154`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported coulombic efficiency (Nafion 212, 25°C).
Entities: ["Nafion 212"]
Metrics: ["coulombic efficiency (Nafion 212, 25°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 212; coulombic efficiency (Nafion 212, 25°C) Relation type: OPERATION Readable labels: Nafion 212; coulombic efficiency (Nafion 212, 25°C) Description: Coulombic efficiency of Nafion 212 at 25°C ranges 92.1-95.3% Source evidence: Coulombic efficiency of Nafion 212 at 25°C ranges 92.1-95.3%

```
#### Evidence 4
- evidence_id: `TEMPO|coulombic efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.471154`
```text
Evidence 4
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, TEMPO achieved/reported coulombic efficiency.
Entities: ["TEMPO"]
Metrics: ["coulombic efficiency"]
Values: []
Conditions: []
Raw support excerpt: TEMPO; coulombic efficiency Relation type: OPERATION Readable labels: TEMPO; coulombic efficiency Description: TEMPO cell achieved CE of 98.2% at 100 mA/cm2, up to 99.0% at 20 mA/cm2 Source evidence: TEMPO cell achieved CE of 98.2% at 100 mA/cm2, up to 99.0% at 20 mA/cm2

```
#### Evidence 5
- evidence_id: `Nafion 117|voltage efficiency (Nafion 117, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.413462`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported voltage efficiency (Nafion 117, 25°C).
Entities: ["Nafion 117"]
Metrics: ["voltage efficiency (Nafion 117, 25°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 117; voltage efficiency (Nafion 117, 25°C) Relation type: OPERATION Readable labels: Nafion 117; voltage efficiency (Nafion 117, 25°C) Description: Voltage efficiency of Nafion 117 at 25°C ranges 80.2-85.8% Source evidence: Voltage efficiency of Nafion 117 at 25°C ranges 80.2-85.8%

```

## DOC01-QA-003 / chem_prompt_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: How does the coulombic efficiency of Nafion 117 compare to Nafion 212 at 100 mA/cm2 and 25 C?
- Reference answer: Nafion 117 CE (97.1%) is 3.3 percentage points higher than Nafion 212 CE (93.8%) at 100 mA/cm2 and 25 C
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Nafion 117 CE: 97.1%", "Nafion 212 CE: 93.8%", "Difference: 3.3 percentage points"]`
- Unsupported claims found: `[]`
- Rationale: The answer abstains from answering despite the question being answerable. It provides no information, thus fails to cover any required key points. The answer is not useful and not correct.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|SPEEK|SPEEK sulfonation degree 42%|capacity fade rate (SPEEK membrane)|capacity fade rate (VRFB with Nafion 117)|energy efficiency (SPEEK membrane at 100 mA/cm2)|energy efficiency (VRFB 100 mA/cm2)`
- relation_type: `COMPARISON`
- retrieval_score: `0.497253`
```text
Evidence 1
Source: chunk-hyperrag-DOC10
Relation/Type: COMPARISON
Short claim: Under the reported conditions, capacity fade rate (SPEEK membrane) = 0.018 %/cycle, while capacity fade rate (VRFB with Nafion 117). Relation: COMPARISON.
Entities: ["Nafion 117", "SPEEK", "SPEEK sulfonation degree 42% = 42 %", "SPEEK sulfonation degree 42%"]
Metrics: ["capacity fade rate (SPEEK membrane) = 0.018 %/cycle", "capacity fade rate (VRFB with Nafion 117)", "energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %", "energy efficiency (VRFB 100 mA/cm2) = 84 %", "capacity fade rate (SPEEK membrane)", "energy efficiency (SPEEK membrane at 100 mA/cm2)", "energy efficiency (VRFB 100 mA/cm2)"]
Values: ["SPEEK sulfonation degree 42% = 42 %", "capacity fade rate (SPEEK membrane) = 0.018 %/cycle", "energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %", "energy efficiency (VRFB 100 mA/cm2) = 84 %"]
Conditions: []
Raw support excerpt: Nafion 117; SPEEK; SPEEK sulfonation degree 42% = 42 %; capacity fade rate (SPEEK membrane) = 0.018 %/cycle; capacity fade rate (VRFB with Nafion 117); energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %; energy efficiency (VRFB 100 mA/cm2) = 84 % Relation type: COMPARISON Readable labels: Nafion 117; SPEEK; SPEEK sulfonation degree 42% = 42 %; capacity fade rate (SPEEK membrane) = 0.018 %/cycle; capacity fade rate (VRFB with Nafion 117); energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %; energy efficiency (VRFB 100 mA/cm2) = 84 % Description: Comparison of Nafion 117 and SPEEK membranes in VRFB: SPEEK with 42% sulfonation achieves slightly lower EE (83%
```
#### Evidence 2
- evidence_id: `Nafion 117|Nafion 212`
- relation_type: `COMPARISON`
- retrieval_score: `0.480769`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Evidence reports Nafion 117, Nafion 212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212 Description: Systematic comparison of Nafion 117 and Nafion 212 across multiple metrics Source evidence: Systematic comparison of Nafion 117 and Nafion 212 across multiple metrics

```
#### Evidence 3
- evidence_id: `Nafion 117|coulombic efficiency (Nafion 117, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.471154`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported coulombic efficiency (Nafion 117, 25°C).
Entities: ["Nafion 117"]
Metrics: ["coulombic efficiency (Nafion 117, 25°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 117; coulombic efficiency (Nafion 117, 25°C) Relation type: OPERATION Readable labels: Nafion 117; coulombic efficiency (Nafion 117, 25°C) Description: Coulombic efficiency of Nafion 117 at 25°C ranges 96.0-98.2% Source evidence: Coulombic efficiency of Nafion 117 at 25°C ranges 96.0-98.2%

```
#### Evidence 4
- evidence_id: `Nafion 212|coulombic efficiency (Nafion 212, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.471154`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported coulombic efficiency (Nafion 212, 25°C).
Entities: ["Nafion 212"]
Metrics: ["coulombic efficiency (Nafion 212, 25°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 212; coulombic efficiency (Nafion 212, 25°C) Relation type: OPERATION Readable labels: Nafion 212; coulombic efficiency (Nafion 212, 25°C) Description: Coulombic efficiency of Nafion 212 at 25°C ranges 92.1-95.3% Source evidence: Coulombic efficiency of Nafion 212 at 25°C ranges 92.1-95.3%

```
#### Evidence 5
- evidence_id: `TEMPO|coulombic efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.471154`
```text
Evidence 5
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, TEMPO achieved/reported coulombic efficiency.
Entities: ["TEMPO"]
Metrics: ["coulombic efficiency"]
Values: []
Conditions: []
Raw support excerpt: TEMPO; coulombic efficiency Relation type: OPERATION Readable labels: TEMPO; coulombic efficiency Description: TEMPO cell achieved CE of 98.2% at 100 mA/cm2, up to 99.0% at 20 mA/cm2 Source evidence: TEMPO cell achieved CE of 98.2% at 100 mA/cm2, up to 99.0% at 20 mA/cm2

```

## DOC01-QA-003 / chem_norm_hypergraph
- Category: `measurement`
- Answerable: `True`
- Question: How does the coulombic efficiency of Nafion 117 compare to Nafion 212 at 100 mA/cm2 and 25 C?
- Reference answer: Nafion 117 CE (97.1%) is 3.3 percentage points higher than Nafion 212 CE (93.8%) at 100 mA/cm2 and 25 C
- Generated answer: At 100 mA/cm² and 25°C, Nafion 117 achieved a coulombic efficiency (CE) of 97.1%, while Nafion 212 achieved a CE of 93.8%. Thus, Nafion 117 has a higher coulombic efficiency than Nafion 212 under these conditions.
- Quality: `SATISFACTORY` | Good: `False` | Satisfactory+: `True` | KPC: `0.6667` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Difference: 3.3 percentage points"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly provides the coulombic efficiency values for both Nafion 117 (97.1%) and Nafion 212 (93.8%) and states that Nafion 117 has higher efficiency. However, it does not explicitly mention the difference of 3.3 percentage points, which is a required key point. The answer is non-hallucinated and partially useful, but lacks full completeness. Therefore, it is rated SATISFACTORY.

### Evidence Blocks
#### Evidence 1
- evidence_id: `condition:current_density|condition:temperature|membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.644231`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under temperature, condition:temperature, current density, while condition:current_density. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: ["temperature", "condition:temperature"]
Raw support excerpt: current density; temperature; Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: current density; temperature; Nafion 117; Nafion 212 Description: Comprehensive comparison of Nafion 117 and Nafion 212 membranes across current densities (40-200 mA/cm2) and temperatures (25-40 C) for coulombic, voltage, and energy efficiency. Source evidence: At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%.

```
#### Evidence 2
- evidence_id: `membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.596154`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Evidence reports Nafion 117, Nafion 212, membrane:nafion_117, membrane:nafion_212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212 Description: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures. Source evidence: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures.

```
#### Evidence 3
- evidence_id: `condition:current_density|membrane:nafion_117`
- relation_type: `OPERATION`
- retrieval_score: `0.355769`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117, membrane:nafion_117 achieved/reported current density, condition:current_density.
Entities: ["Nafion 117", "membrane:nafion_117"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: []
Raw support excerpt: current density; Nafion 117 Relation type: OPERATION Readable labels: current density; Nafion 117 Description: Nafion 117 tested at current densities from 40 to 200 mA/cm2. Source evidence: Nafion 117 tested at current densities from 40 to 200 mA/cm2.

```
#### Evidence 4
- evidence_id: `condition:current_density|membrane:nafion_212`
- relation_type: `OPERATION`
- retrieval_score: `0.355769`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212, membrane:nafion_212 achieved/reported current density, condition:current_density.
Entities: ["Nafion 212", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: []
Raw support excerpt: current density; Nafion 212 Relation type: OPERATION Readable labels: current density; Nafion 212 Description: Nafion 212 tested at current densities from 40 to 200 mA/cm2. Source evidence: Nafion 212 tested at current densities from 40 to 200 mA/cm2.

```
#### Evidence 5
- evidence_id: `membrane:nafion_117|membrane:nafion_212|metric:equivalent_weight|metric:ion_exchange_capacity|metric:thickness_of_nafion_117|metric:thickness_of_nafion_212|metric:vanadium_permeability_of_nafion_117|metric:vanadium_permeability_of_nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.350962`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under the reported conditions, ion exchange capacity = 0.91 mmol/g, while vanadium permeability of Nafion 117 = 1.8e-07 cm²/s. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "equivalent weight = 1100 g/equiv", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "membrane:nafion_117", "membrane:nafion_212", "metric:equivalent_weight", "metric:thickness_of_nafion_117", "metric:thickness_of_nafion_212"]
Metrics: ["ion exchange capacity = 0.91 mmol/g", "vanadium permeability of Nafion 117 = 1.8e-07 cm²/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm²/s", "metric:ion_exchange_capacity", "metric:vanadium_permeability_of_nafion_117", "metric:vanadium_permeability_of_nafion_212"]
Values: ["equivalent weight = 1100 g/equiv", "ion exchange capacity = 0.91 mmol/g", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "vanadium permeability of Nafion 117 = 1.8e-07 cm²/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm²/s"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; equivalent weight = 1100 g/equiv; ion exchange capacity = 0.91 mmol/g; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeability of Nafion 117 = 1.8e-07 cm²/s; vanadium permeability of Nafion 212 = 3.9e-07 cm²/s Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212; equivalent weight = 1100 g/equiv; ion exchange capacity = 0.91 mmol/g; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeabilit
```

## DOC01-QA-004 / text_segments
- Category: `composition`
- Answerable: `True`
- Question: Why does coulombic efficiency increase with increasing current density in VRFBs with Nafion membranes?
- Reference answer: CE increases with current density because the Faradaic current associated with desired vanadium redox reactions increases proportionally with current density, while the parasitic crossover flux driven primarily by concentration gradients remains relatively constant. This improves the ratio of useful charge transfer to parasitic loss.
- Generated answer: Coulombic efficiency increases with increasing current density because the parasitic crossover flux becomes a smaller fraction of the total current at higher operational currents.
- Quality: `SATISFACTORY` | Good: `False` | Satisfactory+: `True` | KPC: `0.333` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Faradaic current increases proportionally with current density", "Crossover flux driven by concentration gradients remains relatively constant"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly states that the parasitic crossover flux becomes a smaller fraction of the total current, which implies an improved ratio. However, it does not explicitly mention that the Faradaic current increases proportionally with current density or that the crossover flux remains constant, which are required key points. The answer is partially useful and non-hallucinated, but lacks completeness.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.625`
```text
Evidence 1
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically varying current density from 40 to 200 mA/cm2 and operating temperature from 25 C to 40 C, we elucidate the fundamental trade-offs between coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) that govern membrane selection. The approximately 3-4 percentage point gap between Nafion 212 and Nafion 117 CE values at any given current density directly reflects the twofold difference in vanadium permeability between the two membranes. For Nafion 117, the EE decreased monotonically with increasing current density at both temperatures, indicating that maximum energy efficiency is achieved at the lowest practical current density. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.625`
```text
Evidence 2
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. VRFB Performance Evaluation ### 4.1 Coulombic Efficiency The coulombic efficiency of all four membranes showed the expected positive correlation with current density, consistent with the fundamental mechanism wherein the parasitic crossover flux becomes a smaller fraction of the total current at higher operational currents. For applications prioritizing maximum voltage efficiency and power density, particularly at high current densities, SPTPC-2.59 offers advantages through its very low resistance (0.82 ohm cm2). The quantitative relationships between IEC, resistance, permeability, and energy efficiency provide a framework for rational design of next-generation non-fluorinated VRFB membranes.

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC03`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.5625`
```text
Evidence 3
Source: DOC03
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) were calculated from the measured capacity and voltage profiles. 3.3 Coulombic Efficiency Coulombic efficiency measurements across the tested current densities revealed consistent trends among the three electrode types. Additionally, the increased density of active sites on modified electrodes promotes more complete conversion of vanadium species during charge and discharge, minimizing the residual concentration differences that contribute to capacity loss. As current density increased to 200 mA/cm2, the performance gap between the modified and unmodified electrodes widened, with BMC-C maintaining substantially higher VE and EE values compared to C-C.

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC04`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.5625`
```text
Evidence 4
Source: DOC04
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a systematic investigation of how vanadium concentration, sulfuric acid supporting electrolyte concentration, electrolyte flow rate, and operating current density collectively influence the electrochemical performance of VRFBs. At 50 mA/cm2, the lower current density reduced both concentration polarization and the relative impact of pumping losses, enabling net EE values at the higher end of the observed range. For stationary energy storage applications where high round-trip efficiency is prioritized, operation at 1.6 mol/L vanadium in 3.0 mol/L H2SO4 with 40 mL/min flow rate and 100 mA/cm2 current density provides net EE of approximately 80%, representing a favorable compromise between efficiency and power density. Conclusion This systematic investigation has elucidated the complex interdependence of electrolyte concentration, flow rate, and current density on VRFB performance metrics and system-level net efficiency.

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC05`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.5625`
```text
Evidence 5
Source: DOC05
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a comprehensive experimental investigation into the temperature-dependent behavior of VRFB cells operated at 25 C, 40 C, and 60 C over 500 charge-discharge cycles at a constant current density of 80 mA/cm2. The results demonstrate that elevated temperatures accelerate vanadium ion crossover through the ion-exchange membrane, exacerbate state-of-charge (SOC) imbalance between the positive and negative half-cells, and precipitate more rapid capacity fading. By maintaining all other operational parameters constant-including current density at 80 mA/cm2, electrolyte composition at 1.5 M VOSO4 in 3.0 M H2SO4, and electrolyte flow rate at 40 mL/min-we establish a controlled experimental framework wherein observed differences in performance can be confidently attributed to temperature effects. ### 3.5 Voltage Efficiency and Polarization Behavior Voltage efficiency, defined as the ratio of average discharge voltage to average charge voltage, exhibited relatively modest temperature dependence compared to the Coulombic efficiency and capacity metrics.

```

## DOC01-QA-004 / original_hypergraph
- Category: `composition`
- Answerable: `True`
- Question: Why does coulombic efficiency increase with increasing current density in VRFBs with Nafion membranes?
- Reference answer: CE increases with current density because the Faradaic current associated with desired vanadium redox reactions increases proportionally with current density, while the parasitic crossover flux driven primarily by concentration gradients remains relatively constant. This improves the ratio of useful charge transfer to parasitic loss.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Faradaic current increases proportionally with current density", "Crossover flux driven by concentration gradients remains relatively constant", "Ratio of useful to parasitic charge transfer improves"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer states 'I don't know based on the retrieved evidence' and provides no citations. This constitutes an abstention. Since the question is answerable (True), the abstention is incorrect, but the evaluation rules require strict assessment of the generated answer's quality. The answer fails to address any of the required key points, resulting in zero coverage. It does not hallucinate, but it is not useful or correct.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Coulombic efficiency|current density`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.5`
```text
Evidence 1
Source: chunk-hyperrag-DOC08
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to Coulombic efficiency, current density. Conditions: not explicitly stated.
Entities: []
Metrics: ["Coulombic efficiency", "current density"]
Values: []
Conditions: []
Raw support excerpt: Coulombic efficiency; current density Relation type: CAUSES_OR_AFFECTS Readable labels: Coulombic efficiency; current density Description: Higher current density decreases Coulombic efficiency Source evidence: Higher current density decreases Coulombic efficiency

```
#### Evidence 2
- evidence_id: `Coulombic efficiency|current density|energy efficiency|voltage efficiency`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.5`
```text
Evidence 2
Source: chunk-hyperrag-DOC08
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to Coulombic efficiency, current density, energy efficiency. Conditions: not explicitly stated.
Entities: []
Metrics: ["Coulombic efficiency", "current density", "energy efficiency", "voltage efficiency"]
Values: []
Conditions: []
Raw support excerpt: Coulombic efficiency; current density; energy efficiency; voltage efficiency Relation type: CAUSES_OR_AFFECTS Readable labels: Coulombic efficiency; current density; energy efficiency; voltage efficiency Description: Increasing current density from 10 to 40 mA/cm2 reduces coulombic, voltage, and energy efficiencies due to higher overpotentials and oxygen evolution Source evidence: CE decreased from 85.2% at 10 mA/cm2 to 78.3% at 40 mA/cm2

```
#### Evidence 3
- evidence_id: `Coulombic efficiency (CE)|current density`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.4375`
```text
Evidence 3
Source: chunk-hyperrag-DOC06
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to Coulombic efficiency (CE), current density. Conditions: not explicitly stated.
Entities: []
Metrics: ["Coulombic efficiency (CE)", "current density"]
Values: []
Conditions: []
Raw support excerpt: Coulombic efficiency (CE); current density Relation type: CAUSES_OR_AFFECTS Readable labels: Coulombic efficiency (CE); current density Description: Current density influences Coulombic efficiency, especially without Bi3+. Source evidence: Current density influences Coulombic efficiency, especially without Bi3+.

```
#### Evidence 4
- evidence_id: `CE of Nafion 117 at 100 mA/cm2 and 25 C|CE of Nafion 212 at 100 mA/cm2 and 25 C|EE of Nafion 117 at 100 mA/cm2 and 25 C|EE of Nafion 212 at 100 mA/cm2 and 25 C|Nafion 117|Nafion 212|VE of Nafion 117 at 100 mA/cm2 and 25 C|VE of Nafion 212 at 100 mA/cm2 and 25 C|current density of 100 mA/cm2|temperature 25 C`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.375`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %, CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %, EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %, EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %, VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %, VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %, temperature 25 C = 25 C, CE of Nafion 117 at 100 mA/cm2 and 25 C, CE of Nafion 212 at 100 mA/cm2 and 25 C, EE of Nafion 117 at 100 mA/cm2 and 25 C, EE of Nafion 212 at 100 mA/cm2 and 25 C, VE of Nafion 117 at 100 mA/cm2 and 25 C, current density of 100 mA/cm2 = 100 mA/cm2, while current density of 100 mA/cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["current density of 100 mA/cm2 = 100 mA/cm2", "current density of 100 mA/cm2"]
Values: ["CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %", "CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %", "EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %", "VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %", "current density of 100 mA/cm2 = 100 mA/cm2", "temperature 25 C = 25 C"]
Conditions: ["CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %", "CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %", "EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %", "VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %", "temperature 25 C = 25 C", "C
```
#### Evidence 5
- evidence_id: `Current density|Zinc dendrite growth`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.375`
```text
Evidence 5
Source: chunk-hyperrag-DOC07
Relation/Type: CAUSES_OR_AFFECTS
Short claim: Zinc dendrite growth is linked to Current density. Conditions: not explicitly stated.
Entities: ["Zinc dendrite growth"]
Metrics: ["Current density"]
Values: []
Conditions: []
Raw support excerpt: Current density; Zinc dendrite growth Relation type: CAUSES_OR_AFFECTS Readable labels: Current density; Zinc dendrite growth Description: Higher current density increases zinc dendrite growth rate Source evidence: Higher current density increases zinc dendrite growth rate

```

## DOC01-QA-004 / chem_prompt_graph
- Category: `composition`
- Answerable: `True`
- Question: Why does coulombic efficiency increase with increasing current density in VRFBs with Nafion membranes?
- Reference answer: CE increases with current density because the Faradaic current associated with desired vanadium redox reactions increases proportionally with current density, while the parasitic crossover flux driven primarily by concentration gradients remains relatively constant. This improves the ratio of useful charge transfer to parasitic loss.
- Generated answer: Higher current density reduces crossover, increasing coulombic efficiency.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `True` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Faradaic current increases proportionally with current density", "Crossover flux driven by concentration gradients remains relatively constant", "Ratio of useful to parasitic charge transfer improves"]`
- Unsupported claims found: `["Higher current density reduces crossover"]`
- Rationale: The generated answer incorrectly claims that higher current density reduces crossover, which is not supported by the reference answer. The reference states that crossover flux remains relatively constant, not that it decreases. Additionally, the answer fails to cover any of the required key points. The single citation 'Evidence 1' is vague and does not provide verifiable support for the claim made.

### Evidence Blocks
#### Evidence 1
- evidence_id: `coulombic efficiency|current density`
- relation_type: `OPERATION`
- retrieval_score: `0.625`
```text
Evidence 1
Source: chunk-hyperrag-DOC07
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported coulombic efficiency, current density.
Entities: []
Metrics: ["coulombic efficiency", "current density"]
Values: []
Conditions: []
Raw support excerpt: coulombic efficiency; current density Relation type: OPERATION Readable labels: coulombic efficiency; current density Description: higher current density reduces crossover, increasing CE Source evidence: higher current density reduces crossover, increasing CE

```
#### Evidence 2
- evidence_id: `coulombic efficiency (Nafion 117, 25°C)|current density`
- relation_type: `OPERATION`
- retrieval_score: `0.5625`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported coulombic efficiency (Nafion 117, 25°C), current density.
Entities: []
Metrics: ["coulombic efficiency (Nafion 117, 25°C)", "current density"]
Values: []
Conditions: []
Raw support excerpt: coulombic efficiency (Nafion 117, 25°C); current density Relation type: OPERATION Readable labels: coulombic efficiency (Nafion 117, 25°C); current density Description: CE of Nafion 117 increases with current density Source evidence: CE of Nafion 117 increases with current density

```
#### Evidence 3
- evidence_id: `current density|gross energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.4375`
```text
Evidence 3
Source: chunk-hyperrag-DOC04
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, gross energy efficiency.
Entities: []
Metrics: ["current density", "gross energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: current density; gross energy efficiency Relation type: OPERATION Readable labels: current density; gross energy efficiency Description: Higher current density reduces gross EE due to increased overpotential; 50 mA/cm² gives highest values Source evidence: Higher current density reduces gross EE due to increased overpotential; 50 mA/cm² gives highest values

```
#### Evidence 4
- evidence_id: `current density|voltage efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.4375`
```text
Evidence 4
Source: chunk-hyperrag-DOC07
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, voltage efficiency.
Entities: []
Metrics: ["current density", "voltage efficiency"]
Values: []
Conditions: []
Raw support excerpt: current density; voltage efficiency Relation type: OPERATION Readable labels: current density; voltage efficiency Description: higher current density increases overpotentials, decreasing VE Source evidence: higher current density increases overpotentials, decreasing VE

```
#### Evidence 5
- evidence_id: `current density|voltage efficiency (Nafion 117, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.375`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, voltage efficiency (Nafion 117, 25°C).
Entities: []
Metrics: ["current density", "voltage efficiency (Nafion 117, 25°C)"]
Values: []
Conditions: []
Raw support excerpt: current density; voltage efficiency (Nafion 117, 25°C) Relation type: OPERATION Readable labels: current density; voltage efficiency (Nafion 117, 25°C) Description: VE of Nafion 117 decreases with current density Source evidence: VE of Nafion 117 decreases with current density

```

## DOC01-QA-004 / chem_prompt_hypergraph
- Category: `composition`
- Answerable: `True`
- Question: Why does coulombic efficiency increase with increasing current density in VRFBs with Nafion membranes?
- Reference answer: CE increases with current density because the Faradaic current associated with desired vanadium redox reactions increases proportionally with current density, while the parasitic crossover flux driven primarily by concentration gradients remains relatively constant. This improves the ratio of useful charge transfer to parasitic loss.
- Generated answer: Higher current density reduces crossover, increasing coulombic efficiency.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `True` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Faradaic current increases proportionally with current density", "Crossover flux driven by concentration gradients remains relatively constant", "Ratio of useful to parasitic charge transfer improves"]`
- Unsupported claims found: `["Higher current density reduces crossover"]`
- Rationale: The generated answer incorrectly claims that higher current density reduces crossover, which contradicts the reference answer that states crossover flux remains constant. It fails to mention the key points about Faradaic current increasing proportionally and the ratio improvement. Therefore, the answer is incorrect and contains unsupported claims.

### Evidence Blocks
#### Evidence 1
- evidence_id: `coulombic efficiency|current density`
- relation_type: `OPERATION`
- retrieval_score: `0.625`
```text
Evidence 1
Source: chunk-hyperrag-DOC07
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported coulombic efficiency, current density.
Entities: []
Metrics: ["coulombic efficiency", "current density"]
Values: []
Conditions: []
Raw support excerpt: coulombic efficiency; current density Relation type: OPERATION Readable labels: coulombic efficiency; current density Description: higher current density reduces crossover, increasing CE Source evidence: higher current density reduces crossover, increasing CE

```
#### Evidence 2
- evidence_id: `coulombic efficiency (Nafion 117, 25°C)|current density`
- relation_type: `OPERATION`
- retrieval_score: `0.5625`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported coulombic efficiency (Nafion 117, 25°C), current density.
Entities: []
Metrics: ["coulombic efficiency (Nafion 117, 25°C)", "current density"]
Values: []
Conditions: []
Raw support excerpt: coulombic efficiency (Nafion 117, 25°C); current density Relation type: OPERATION Readable labels: coulombic efficiency (Nafion 117, 25°C); current density Description: CE of Nafion 117 increases with current density Source evidence: CE of Nafion 117 increases with current density

```
#### Evidence 3
- evidence_id: `coulombic efficiency|current density|energy efficiency|voltage efficiency|zinc dendrite growth rate`
- relation_type: `OPERATION`
- retrieval_score: `0.475`
```text
Evidence 3
Source: chunk-hyperrag-DOC07
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, zinc dendrite growth rate achieved/reported coulombic efficiency, current density, energy efficiency, voltage efficiency.
Entities: ["zinc dendrite growth rate"]
Metrics: ["coulombic efficiency", "current density", "energy efficiency", "voltage efficiency"]
Values: []
Conditions: []
Raw support excerpt: coulombic efficiency; current density; energy efficiency; voltage efficiency; zinc dendrite growth rate Relation type: OPERATION Readable labels: coulombic efficiency; current density; energy efficiency; voltage efficiency; zinc dendrite growth rate Description: Current density variation from 20 to 80 mA/cm2 at 0.3 M MEP shows tradeoff: higher CD increases CE and dendrite growth but decreases VE, with EE relatively stable. Source evidence: At 20 mA/cm2, CE 85.3%, VE 75.2%, EE 64.1%; at 80 mA/cm2, CE 92.1%, VE 65.8%, EE 60.6%

```
#### Evidence 4
- evidence_id: `current density|gross energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.4375`
```text
Evidence 4
Source: chunk-hyperrag-DOC04
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, gross energy efficiency.
Entities: []
Metrics: ["current density", "gross energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: current density; gross energy efficiency Relation type: OPERATION Readable labels: current density; gross energy efficiency Description: Higher current density reduces gross EE due to increased overpotential; 50 mA/cm² gives highest values Source evidence: Higher current density reduces gross EE due to increased overpotential; 50 mA/cm² gives highest values

```
#### Evidence 5
- evidence_id: `current density|voltage efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.4375`
```text
Evidence 5
Source: chunk-hyperrag-DOC07
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, voltage efficiency.
Entities: []
Metrics: ["current density", "voltage efficiency"]
Values: []
Conditions: []
Raw support excerpt: current density; voltage efficiency Relation type: OPERATION Readable labels: current density; voltage efficiency Description: higher current density increases overpotentials, decreasing VE Source evidence: higher current density increases overpotentials, decreasing VE

```

## DOC01-QA-004 / chem_norm_hypergraph
- Category: `composition`
- Answerable: `True`
- Question: Why does coulombic efficiency increase with increasing current density in VRFBs with Nafion membranes?
- Reference answer: CE increases with current density because the Faradaic current associated with desired vanadium redox reactions increases proportionally with current density, while the parasitic crossover flux driven primarily by concentration gradients remains relatively constant. This improves the ratio of useful charge transfer to parasitic loss.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Faradaic current increases proportionally with current density", "Crossover flux driven by concentration gradients remains relatively constant", "Ratio of useful to parasitic charge transfer improves"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer is an abstention ('I don't know based on the retrieved evidence.') and does not address the question. It fails to provide any of the required key points, resulting in zero coverage. The answer is not useful, not correct, and not complete, so it is rated POOR.

### Evidence Blocks
#### Evidence 1
- evidence_id: `condition:current_density|condition:temperature|membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.4375`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under temperature, condition:temperature, current density, while condition:current_density. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: ["temperature", "condition:temperature"]
Raw support excerpt: current density; temperature; Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: current density; temperature; Nafion 117; Nafion 212 Description: Comprehensive comparison of Nafion 117 and Nafion 212 membranes across current densities (40-200 mA/cm2) and temperatures (25-40 C) for coulombic, voltage, and energy efficiency. Source evidence: At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%.

```
#### Evidence 2
- evidence_id: `condition:current_density|metric:ce`
- relation_type: `OPERATION`
- retrieval_score: `0.4375`
```text
Evidence 2
Source: chunk-hyperrag-DOC08<SEP>chunk-hyperrag-DOC06
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, metric:ce achieved/reported current density, coulombic efficiency = 93 %, condition:current_density.
Entities: ["metric:ce"]
Metrics: ["current density", "coulombic efficiency = 93 %", "condition:current_density"]
Values: ["coulombic efficiency = 93 %"]
Conditions: []
Raw support excerpt: current density; coulombic efficiency = 93 % Relation type: OPERATION Readable labels: current density; coulombic efficiency = 93 % Description: Coulombic efficiency measured at various current densities from 40 to 160 mA/cm2 Source evidence: Coulombic efficiency measured at various current densities from 40 to 160 mA/cm2 ; Coulombic efficiency measured at varying current densities (10-40 mA/cm2)

```
#### Evidence 3
- evidence_id: `condition:current_density|system:vrfb`
- relation_type: `OPERATION`
- retrieval_score: `0.375`
```text
Evidence 3
Source: chunk-hyperrag-DOC05
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, VRFB, system:vrfb achieved/reported current density, condition:current_density.
Entities: ["VRFB", "system:vrfb"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: []
Raw support excerpt: current density; VRFB Relation type: OPERATION Readable labels: current density; VRFB Description: Operated at constant current density 80 mA/cm2 Source evidence: Operated at constant current density 80 mA/cm2

```
#### Evidence 4
- evidence_id: `condition:bi3_concentration|condition:current_density|metric:ce|metric:ve`
- relation_type: `COMPARISON`
- retrieval_score: `0.375`
```text
Evidence 4
Source: chunk-hyperrag-DOC06
Relation/Type: COMPARISON
Short claim: Under Bi3+ concentration, current density, while coulombic efficiency = 93 %. Relation: COMPARISON.
Entities: ["condition:bi3_concentration", "metric:ce", "metric:ve"]
Metrics: ["current density", "coulombic efficiency = 93 %", "voltage efficiency", "condition:current_density"]
Values: ["coulombic efficiency = 93 %"]
Conditions: ["Bi3+ concentration"]
Raw support excerpt: Bi3+ concentration; current density; coulombic efficiency = 93 %; voltage efficiency Relation type: COMPARISON Readable labels: Bi3+ concentration; current density; coulombic efficiency = 93 %; voltage efficiency Description: Comparison of efficiencies at different Bi3+ concentrations (0.5-5.0 mmol/L) and current densities (40-160 mA/cm2); baseline without Bi3+ yields lower values Source evidence: With Bi3+ addition, Coulombic efficiency improved to the range of 87-96% and energy efficiency reached 62-85%

```
#### Evidence 5
- evidence_id: `condition:current_density|metric:bromine_crossover_rate_range`
- relation_type: `OPERATION`
- retrieval_score: `0.375`
```text
Evidence 5
Source: chunk-hyperrag-DOC07
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, bromine crossover rate, condition:current_density, metric:bromine_crossover_rate_range.
Entities: []
Metrics: ["current density", "bromine crossover rate", "condition:current_density", "metric:bromine_crossover_rate_range"]
Values: []
Conditions: []
Raw support excerpt: current density; bromine crossover rate Relation type: OPERATION Readable labels: current density; bromine crossover rate Description: Increasing current density decreases bromine crossover rate due to faster electrochemical consumption. Source evidence: Increasing current density decreases bromine crossover rate due to faster electrochemical consumption.

```

## DOC01-QA-006 / text_segments
- Category: `composition`
- Answerable: `True`
- Question: At 100 mA/cm2 and 25 C, both membranes achieve similar EE despite different CE/VE compositions. Explain the performance trade-off and recommend which membrane to use for long-cycle-life stationary storage.
- Reference answer: At 100 mA/cm2 and 25 C, Nafion 117 achieves EE of 80.2% (CE 97.1%, VE 82.6%) while Nafion 212 achieves EE of 80.9% (CE 93.8%, VE 86.2%). The similar EE masks a fundamental trade-off: Nafion 117 prioritizes CE via lower vanadium crossover (1.8 x 10^-7 cm2/s) at the cost of higher resistance (1.65 ohm cm2), while Nafion 212 achieves lower resistance (0.85 ohm cm2) but higher crossover (3.9 x 10^-7 cm2/s). For long-cycle-life stationary storage, Nafion 117 is recommended because its lower crossover yields an estimated capacity fade rate of 0.08% per cycle versus 0.18% per cycle for Nafion 212.
- Generated answer: At 100 mA/cm2 and 25°C, Nafion 117 achieves CE of 97.1% and VE of 82.6% (EE 80.2%), while Nafion 212 achieves CE of 93.8% and VE of 86.2% (EE 80.9%). The trade-off is that the thicker Nafion 117 has higher coulombic efficiency due to lower vanadium crossover but higher area resistance, resulting in lower voltage efficiency; the thinner Nafion 212 has lower resistance and higher voltage efficiency but higher crossover and lower coulombic efficiency. For long-cycle-life stationary storage, capacity fade is critical: Nafion 117 has a capacity fade rate of 0.08%/cycle compared to 0.18%/cycle for Nafion 212, so Nafion 117 is recommended for better capacity retention.
- Quality: `SATISFACTORY` | Good: `False` | Satisfactory+: `True` | KPC: `0.6667` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Nafion 117 crossover: 1.8 x 10^-7 cm2/s, resistance: 1.65 ohm cm2", "Nafion 212 crossover: 3.9 x 10^-7 cm2/s, resistance: 0.85 ohm cm2"]`
- Unsupported claims found: `[]`
- Rationale: The answer correctly identifies the EE, CE, VE values and explains the trade-off qualitatively, and recommends Nafion 117 with capacity fade rates. However, it omits the specific crossover and resistance numerical values that are required key points, making it not fully complete. The answer is correct and non-hallucinated, so it is satisfactory but not good.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.619565`
```text
Evidence 1
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. ### 3.4 Structure-Transport Correlations The trade-off between proton conductivity (inverse of resistance) and vanadium selectivity (inverse of permeability) defines the fundamental performance envelope for VRFB membranes. It is noteworthy that both SNPBI-1.42 and SPTPC-2.59 achieve energy efficiency values that meet or exceed the performance of benchmark Nafion membranes under comparable conditions. ### 5.3 Resistance-EE and Permeability-EE Correlations Multiple linear regression analysis of the performance data reveals that energy efficiency at 100 mA/cm2 can be predicted from area resistance and vanadium permeability with good accuracy.

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC05`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.586957`
```text
Evidence 2
Source: DOC05
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a comprehensive experimental investigation into the temperature-dependent behavior of VRFB cells operated at 25 C, 40 C, and 60 C over 500 charge-discharge cycles at a constant current density of 80 mA/cm2. The results demonstrate that elevated temperatures accelerate vanadium ion crossover through the ion-exchange membrane, exacerbate state-of-charge (SOC) imbalance between the positive and negative half-cells, and precipitate more rapid capacity fading. By maintaining all other operational parameters constant-including current density at 80 mA/cm2, electrolyte composition at 1.5 M VOSO4 in 3.0 M H2SO4, and electrolyte flow rate at 40 mL/min-we establish a controlled experimental framework wherein observed differences in performance can be confidently attributed to temperature effects. Results and Discussion ### 3.1 Capacity Retention Behavior Across Temperatures The long-term cycling behavior of VRFB cells operated at 25 C, 40 C, and 60 C revealed pronounced temperature-dependent differences in capacity retention trajectories.

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC10`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.586957`
```text
Evidence 3
Source: DOC10
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: At 100 mA/cm2, a SPEEK membrane with 42% sulfonation degree achieved an EE of 83% compared to 84% for Nafion 117, but reduced the capacity fade rate from 0.035%/cycle to 0.018%/cycle. A benchmark AEM (Fumatech FAP-450) achieved an EE of 79% at 100 mA/cm2 with iron-chromium electrolyte, compared to 82% for Nafion 117, but with significantly improved chromium retention (crossover rate reduced by 40%). A nanoporous ceramic-polymer composite membrane demonstrated improved lead rejection (selectivity 93%) with an ASR of 3.2 ohm cm2, achieving an EE of 74% at 30 mA/cm2 compared to 76% with Nafion 117 but with reduced capacity fade from 0.08%/cycle to 0.04%/cycle. ### 7.2 Capacity Fade Comparison Capacity fade rates at matched cycle numbers (500 cycles) and with optimized membranes show the following ranking from lowest to highest fade: AQDS-based ORFB 0.01-0.015%/cycle < TEMPO-PEG ORFB 0.015%/cycle < VRFB with SPEEK 0.018%/cycle < PSV ORFB 0.018%/cycle < ICRFB with AEM 0.025%/cycle < standard VRFB with Nafion 0.035%/cycle < Zn-Br with standard separator 0.04-0.06%/cycle < SLA with ceramic membrane 0.04%/cycle < MV-based ORFB with Nafion 0.055%/cycle.

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.521739`
```text
Evidence 4
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically varying current density from 40 to 200 mA/cm2 and operating temperature from 25 C to 40 C, we elucidate the fundamental trade-offs between coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) that govern membrane selection. At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%. Based on the measured permeability values and the electrolyte volumes employed, the capacity fade rate attributable to vanadium crossover alone is estimated at approximately 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212 under standard operating conditions at 100 mA/cm2 and 25 C. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC06`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.521739`
```text
Evidence 5
Source: DOC06
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: The work addresses three primary objectives: (1) quantifying the kinetic enhancement of the Cr(III)/Cr(II) redox reaction in the presence of Bi3+, (2) characterizing the suppression of parasitic hydrogen evolution achieved through Bi3+ addition, and (3) establishing the relationship between Bi3+ concentration, operational current density, and full-cell performance metrics including Coulombic efficiency, voltage efficiency, and energy efficiency. A microporous polyethylene separator (Celgard 2500) with a thickness of 25 um and porosity of 55% was employed as the membrane between the positive and negative half-cells. At a current density of 40 mA/cm2, the cell achieved a Coulombic efficiency of 85%, a voltage efficiency of 68%, and an energy efficiency of 58%. The principal findings are as follows: The addition of Bi3+ at concentrations of 0.5-5.0 mmol/L to the negative electrolyte substantially improves both Coulombic efficiency and energy efficiency across the operational current density range of 40-160 mA/cm2.

```

## DOC01-QA-006 / original_hypergraph
- Category: `composition`
- Answerable: `True`
- Question: At 100 mA/cm2 and 25 C, both membranes achieve similar EE despite different CE/VE compositions. Explain the performance trade-off and recommend which membrane to use for long-cycle-life stationary storage.
- Reference answer: At 100 mA/cm2 and 25 C, Nafion 117 achieves EE of 80.2% (CE 97.1%, VE 82.6%) while Nafion 212 achieves EE of 80.9% (CE 93.8%, VE 86.2%). The similar EE masks a fundamental trade-off: Nafion 117 prioritizes CE via lower vanadium crossover (1.8 x 10^-7 cm2/s) at the cost of higher resistance (1.65 ohm cm2), while Nafion 212 achieves lower resistance (0.85 ohm cm2) but higher crossover (3.9 x 10^-7 cm2/s). For long-cycle-life stationary storage, Nafion 117 is recommended because its lower crossover yields an estimated capacity fade rate of 0.08% per cycle versus 0.18% per cycle for Nafion 212.
- Generated answer: The performance trade-off is that Nafion 117 has higher CE (97.1%) but lower VE (82.6%), while Nafion 212 has lower CE (93.8%) but higher VE (86.2%), resulting in similar EE (80.2% vs 80.9%). No recommendation can be made based on the retrieved evidence for long-cycle-life stationary storage.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.5` | Hallucinated: `True` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `["Nafion 117 crossover: 1.8 x 10^-7 cm2/s, resistance: 1.65 ohm cm2", "Nafion 212 crossover: 3.9 x 10^-7 cm2/s, resistance: 0.85 ohm cm2", "Recommendation: Nafion 117 for long cycle life (0.08% vs 0.18% fade rate)"]`
- Unsupported claims found: `["No recommendation can be made based on the retrieved evidence for long-cycle-life stationary storage"]`
- Rationale: The generated answer correctly states the CE/VE/EE values and the trade-off, but it fails to provide the crossover, resistance, and fade rate data, and it incorrectly claims that no recommendation can be made, contradicting the reference answer which recommends Nafion 117. The answer is incomplete and contains an unsupported claim, making it poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `CE of Nafion 117 at 100 mA/cm2 and 25 C|CE of Nafion 212 at 100 mA/cm2 and 25 C|EE of Nafion 117 at 100 mA/cm2 and 25 C|EE of Nafion 212 at 100 mA/cm2 and 25 C|Nafion 117|Nafion 212|VE of Nafion 117 at 100 mA/cm2 and 25 C|VE of Nafion 212 at 100 mA/cm2 and 25 C|current density of 100 mA/cm2|temperature 25 C`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.26087`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %, CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %, EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %, EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %, VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %, VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %, temperature 25 C = 25 C, CE of Nafion 117 at 100 mA/cm2 and 25 C, CE of Nafion 212 at 100 mA/cm2 and 25 C, EE of Nafion 117 at 100 mA/cm2 and 25 C, EE of Nafion 212 at 100 mA/cm2 and 25 C, VE of Nafion 117 at 100 mA/cm2 and 25 C, current density of 100 mA/cm2 = 100 mA/cm2, while current density of 100 mA/cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["current density of 100 mA/cm2 = 100 mA/cm2", "current density of 100 mA/cm2"]
Values: ["CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %", "CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %", "EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %", "VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %", "current density of 100 mA/cm2 = 100 mA/cm2", "temperature 25 C = 25 C"]
Conditions: ["CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %", "CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %", "EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %", "VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %", "temperature 25 C = 25 C", "C
```
#### Evidence 2
- evidence_id: `Area-specific resistance|Energy efficiency|Ion exchange capacity (IEC)|Vanadium permeability`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.195652`
```text
Evidence 2
Source: chunk-hyperrag-DOC02
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to Area-specific resistance, Energy efficiency, Ion exchange capacity (IEC). Conditions: not explicitly stated.
Entities: []
Metrics: ["Area-specific resistance", "Energy efficiency", "Ion exchange capacity (IEC)", "Vanadium permeability"]
Values: []
Conditions: []
Raw support excerpt: Area-specific resistance; Energy efficiency; Ion exchange capacity (IEC); Vanadium permeability Relation type: CAUSES_OR_AFFECTS Readable labels: Area-specific resistance; Energy efficiency; Ion exchange capacity (IEC); Vanadium permeability Description: IEC influences both area resistance and vanadium permeability, which together determine energy efficiency. Source evidence: quantitative structure-property-performance relationships that guide rational membrane design

```
#### Evidence 3
- evidence_id: `PBI energy efficiency at 100 mA/cm2|SNPBI-1.42 energy efficiency at 100 mA/cm2|SPEEK/APK energy efficiency at 100 mA/cm2|SPTPC-2.59 energy efficiency at 100 mA/cm2`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.195652`
```text
Evidence 3
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARES_WITH
Short claim: Under the reported conditions, PBI energy efficiency at 100 mA/cm2 = 71.8 %, while SNPBI-1.42 energy efficiency at 100 mA/cm2 = 80.5 %. Relation: COMPARES_WITH.
Entities: []
Metrics: ["PBI energy efficiency at 100 mA/cm2 = 71.8 %", "SNPBI-1.42 energy efficiency at 100 mA/cm2 = 80.5 %", "SPEEK/APK energy efficiency at 100 mA/cm2 = 77.9 %", "SPTPC-2.59 energy efficiency at 100 mA/cm2 = 81.4 %", "PBI energy efficiency at 100 mA/cm2", "SNPBI-1.42 energy efficiency at 100 mA/cm2", "SPEEK/APK energy efficiency at 100 mA/cm2", "SPTPC-2.59 energy efficiency at 100 mA/cm2"]
Values: ["PBI energy efficiency at 100 mA/cm2 = 71.8 %", "SNPBI-1.42 energy efficiency at 100 mA/cm2 = 80.5 %", "SPEEK/APK energy efficiency at 100 mA/cm2 = 77.9 %", "SPTPC-2.59 energy efficiency at 100 mA/cm2 = 81.4 %"]
Conditions: []
Raw support excerpt: PBI energy efficiency at 100 mA/cm2 = 71.8 %; SNPBI-1.42 energy efficiency at 100 mA/cm2 = 80.5 %; SPEEK/APK energy efficiency at 100 mA/cm2 = 77.9 %; SPTPC-2.59 energy efficiency at 100 mA/cm2 = 81.4 % Relation type: COMPARES_WITH Readable labels: PBI energy efficiency at 100 mA/cm2 = 71.8 %; SNPBI-1.42 energy efficiency at 100 mA/cm2 = 80.5 %; SPEEK/APK energy efficiency at 100 mA/cm2 = 77.9 %; SPTPC-2.59 energy efficiency at 100 mA/cm2 = 81.4 % Description: Energy efficiency values at 100 mA/cm2 for the four membranes show SNPBI-1.42 highest (80.5%) and SPEEK/APK lowest (77.9%). Source evidence: At 100 mA/cm2, SNPBI-1.42 achieved the highest EE at 80.5%

```
#### Evidence 4
- evidence_id: `25 C|vanadium ion crossover`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.190217`
```text
Evidence 4
Source: chunk-hyperrag-DOC05
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to vanadium ion crossover. Conditions: 25 C = 25 C, 25 C.
Entities: []
Metrics: ["vanadium ion crossover"]
Values: ["25 C = 25 C"]
Conditions: ["25 C = 25 C", "25 C"]
Raw support excerpt: 25 C = 25 C; vanadium ion crossover Relation type: CAUSES_OR_AFFECTS Readable labels: 25 C = 25 C; vanadium ion crossover Description: Temperature influences crossover rate Source evidence: Temperature influences crossover rate

```
#### Evidence 5
- evidence_id: `Nafion 117|Nafion 212|area resistance of Nafion 117 at 25 C|area resistance of Nafion 117 at 40 C|area resistance of Nafion 212 at 25 C|area resistance of Nafion 212 at 40 C|temperature 40 C`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.163043`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under temperature 40 C = 40 C, temperature 40 C, area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, while area resistance of Nafion 117 at 40 C = 1.32 ohm cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "area resistance of Nafion 117 at 25 C", "area resistance of Nafion 117 at 40 C", "area resistance of Nafion 212 at 25 C", "area resistance of Nafion 212 at 40 C"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "temperature 40 C = 40 C"]
Conditions: ["temperature 40 C = 40 C", "temperature 40 C"]
Raw support excerpt: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2; temperature 40 C = 40 C Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2; te
```

## DOC01-QA-006 / chem_prompt_graph
- Category: `composition`
- Answerable: `True`
- Question: At 100 mA/cm2 and 25 C, both membranes achieve similar EE despite different CE/VE compositions. Explain the performance trade-off and recommend which membrane to use for long-cycle-life stationary storage.
- Reference answer: At 100 mA/cm2 and 25 C, Nafion 117 achieves EE of 80.2% (CE 97.1%, VE 82.6%) while Nafion 212 achieves EE of 80.9% (CE 93.8%, VE 86.2%). The similar EE masks a fundamental trade-off: Nafion 117 prioritizes CE via lower vanadium crossover (1.8 x 10^-7 cm2/s) at the cost of higher resistance (1.65 ohm cm2), while Nafion 212 achieves lower resistance (0.85 ohm cm2) but higher crossover (3.9 x 10^-7 cm2/s). For long-cycle-life stationary storage, Nafion 117 is recommended because its lower crossover yields an estimated capacity fade rate of 0.08% per cycle versus 0.18% per cycle for Nafion 212.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Similar EE: 80.2% vs 80.9%", "Nafion 117: CE 97.1%, VE 82.6%", "Nafion 212: CE 93.8%, VE 86.2%", "Nafion 117 crossover: 1.8 x 10^-7 cm2/s, resistance: 1.65 ohm cm2", "Nafion 212 crossover: 3.9 x 10^-7 cm2/s, resistance: 0.85 ohm cm2", "Recommendation: Nafion 117 for long cycle life (0.08% vs 0.18% fade rate)"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer states 'I don't know based on the retrieved evidence.' and provides no citations. This is an abstention, which is not appropriate because the question is answerable (as indicated by 'Answerable: True') and the reference answer provides sufficient information. The answer fails to address any of the required key points, resulting in zero coverage. It is not hallucinated (no false claims are made), but it is not useful or correct. Therefore, the quality label is POOR.

### Evidence Blocks
#### Evidence 1
- evidence_id: `TEMPO|energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.163043`
```text
Evidence 1
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, TEMPO achieved/reported energy efficiency.
Entities: ["TEMPO"]
Metrics: ["energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: TEMPO; energy efficiency Relation type: OPERATION Readable labels: TEMPO; energy efficiency Description: TEMPO cell achieved EE of 84.3% at 100 mA/cm2, up to 88.5% at 20 mA/cm2 Source evidence: TEMPO cell achieved EE of 84.3% at 100 mA/cm2, up to 88.5% at 20 mA/cm2

```
#### Evidence 2
- evidence_id: `SPEEK|energy efficiency (SPEEK membrane at 100 mA/cm2)`
- relation_type: `OPERATION`
- retrieval_score: `0.163043`
```text
Evidence 2
Source: chunk-hyperrag-DOC10
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, SPEEK achieved/reported energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %, energy efficiency (SPEEK membrane at 100 mA/cm2).
Entities: ["SPEEK"]
Metrics: ["energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %", "energy efficiency (SPEEK membrane at 100 mA/cm2)"]
Values: ["energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %"]
Conditions: []
Raw support excerpt: SPEEK; energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 % Relation type: OPERATION Readable labels: SPEEK; energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 % Description: SPEEK membrane with 42% sulfonation achieves EE 83% at 100 mA/cm2 Source evidence: SPEEK membrane with 42% sulfonation achieves EE 83% at 100 mA/cm2

```
#### Evidence 3
- evidence_id: `25 °C|capacity retention at 25°C`
- relation_type: `OPERATION`
- retrieval_score: `0.157609`
```text
Evidence 3
Source: chunk-hyperrag-DOC05
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, 25 °C = 25 °C, 25 °C achieved/reported capacity retention at 25°C = 85 %, capacity retention at 25°C.
Entities: ["25 °C = 25 °C", "25 °C"]
Metrics: ["capacity retention at 25°C = 85 %", "capacity retention at 25°C"]
Values: ["25 °C = 25 °C", "capacity retention at 25°C = 85 %"]
Conditions: []
Raw support excerpt: 25 °C = 25 °C; capacity retention at 25°C = 85 % Relation type: OPERATION Readable labels: 25 °C = 25 °C; capacity retention at 25°C = 85 % Description: Capacity retention measured at 25°C after 500 cycles Source evidence: Capacity retention measured at 25°C after 500 cycles

```
#### Evidence 4
- evidence_id: `TEMPO|coulombic efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.130435`
```text
Evidence 4
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, TEMPO achieved/reported coulombic efficiency.
Entities: ["TEMPO"]
Metrics: ["coulombic efficiency"]
Values: []
Conditions: []
Raw support excerpt: TEMPO; coulombic efficiency Relation type: OPERATION Readable labels: TEMPO; coulombic efficiency Description: TEMPO cell achieved CE of 98.2% at 100 mA/cm2, up to 99.0% at 20 mA/cm2 Source evidence: TEMPO cell achieved CE of 98.2% at 100 mA/cm2, up to 99.0% at 20 mA/cm2

```
#### Evidence 5
- evidence_id: `MV|energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.130435`
```text
Evidence 5
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, MV achieved/reported energy efficiency.
Entities: ["MV"]
Metrics: ["energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: MV; energy efficiency Relation type: OPERATION Readable labels: MV; energy efficiency Description: MV/TEMPO cell EE 80.2% at 100 mA/cm2, up to 86.8% at 20 mA/cm2 Source evidence: MV/TEMPO cell EE 80.2% at 100 mA/cm2, up to 86.8% at 20 mA/cm2

```

## DOC01-QA-006 / chem_prompt_hypergraph
- Category: `composition`
- Answerable: `True`
- Question: At 100 mA/cm2 and 25 C, both membranes achieve similar EE despite different CE/VE compositions. Explain the performance trade-off and recommend which membrane to use for long-cycle-life stationary storage.
- Reference answer: At 100 mA/cm2 and 25 C, Nafion 117 achieves EE of 80.2% (CE 97.1%, VE 82.6%) while Nafion 212 achieves EE of 80.9% (CE 93.8%, VE 86.2%). The similar EE masks a fundamental trade-off: Nafion 117 prioritizes CE via lower vanadium crossover (1.8 x 10^-7 cm2/s) at the cost of higher resistance (1.65 ohm cm2), while Nafion 212 achieves lower resistance (0.85 ohm cm2) but higher crossover (3.9 x 10^-7 cm2/s). For long-cycle-life stationary storage, Nafion 117 is recommended because its lower crossover yields an estimated capacity fade rate of 0.08% per cycle versus 0.18% per cycle for Nafion 212.
- Generated answer: The trade-off is that SPEEK membrane achieves slightly lower energy efficiency (83% vs 84%) but much lower capacity fade rate (0.018%/cycle vs 0.035%/cycle) compared to Nafion 117. For long-cycle-life stationary storage, the lower capacity fade is critical, so SPEEK membrane is recommended.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `True` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Similar EE: 80.2% vs 80.9%", "Nafion 117: CE 97.1%, VE 82.6%", "Nafion 212: CE 93.8%, VE 86.2%", "Nafion 117 crossover: 1.8 x 10^-7 cm2/s, resistance: 1.65 ohm cm2", "Nafion 212 crossover: 3.9 x 10^-7 cm2/s, resistance: 0.85 ohm cm2", "Recommendation: Nafion 117 for long cycle life (0.08% vs 0.18% fade rate)"]`
- Unsupported claims found: `["SPEEK membrane achieves slightly lower energy efficiency (83% vs 84%) but much lower capacity fade rate (0.018%/cycle vs 0.035%/cycle) compared to Nafion 117", "SPEEK membrane is recommended for long-cycle-life stationary storage"]`
- Rationale: The generated answer does not address the question about Nafion 117 vs Nafion 212. Instead, it introduces an irrelevant membrane (SPEEK) and provides unsupported numbers. It fails to cover any required key points and contains hallucinated claims. Therefore, the answer is poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|SPEEK|SPEEK sulfonation degree 42%|capacity fade rate (SPEEK membrane)|capacity fade rate (VRFB with Nafion 117)|energy efficiency (SPEEK membrane at 100 mA/cm2)|energy efficiency (VRFB 100 mA/cm2)`
- relation_type: `COMPARISON`
- retrieval_score: `0.228261`
```text
Evidence 1
Source: chunk-hyperrag-DOC10
Relation/Type: COMPARISON
Short claim: Under the reported conditions, capacity fade rate (SPEEK membrane) = 0.018 %/cycle, while capacity fade rate (VRFB with Nafion 117). Relation: COMPARISON.
Entities: ["Nafion 117", "SPEEK", "SPEEK sulfonation degree 42% = 42 %", "SPEEK sulfonation degree 42%"]
Metrics: ["capacity fade rate (SPEEK membrane) = 0.018 %/cycle", "capacity fade rate (VRFB with Nafion 117)", "energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %", "energy efficiency (VRFB 100 mA/cm2) = 84 %", "capacity fade rate (SPEEK membrane)", "energy efficiency (SPEEK membrane at 100 mA/cm2)", "energy efficiency (VRFB 100 mA/cm2)"]
Values: ["SPEEK sulfonation degree 42% = 42 %", "capacity fade rate (SPEEK membrane) = 0.018 %/cycle", "energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %", "energy efficiency (VRFB 100 mA/cm2) = 84 %"]
Conditions: []
Raw support excerpt: Nafion 117; SPEEK; SPEEK sulfonation degree 42% = 42 %; capacity fade rate (SPEEK membrane) = 0.018 %/cycle; capacity fade rate (VRFB with Nafion 117); energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %; energy efficiency (VRFB 100 mA/cm2) = 84 % Relation type: COMPARISON Readable labels: Nafion 117; SPEEK; SPEEK sulfonation degree 42% = 42 %; capacity fade rate (SPEEK membrane) = 0.018 %/cycle; capacity fade rate (VRFB with Nafion 117); energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %; energy efficiency (VRFB 100 mA/cm2) = 84 % Description: Comparison of Nafion 117 and SPEEK membranes in VRFB: SPEEK with 42% sulfonation achieves slightly lower EE (83%
```
#### Evidence 2
- evidence_id: `Nafion 117|Nafion 212|capacity fade rate|commercial anion exchange membrane|crossover rate|membrane selectivity|nanoporous size-exclusion membrane|sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation`
- relation_type: `COMPARISON`
- retrieval_score: `0.195652`
```text
Evidence 2
Source: chunk-hyperrag-DOC09
Relation/Type: COMPARISON
Short claim: Under the reported conditions, capacity fade rate, while crossover rate. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "commercial anion exchange membrane", "membrane selectivity", "nanoporous size-exclusion membrane", "sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation"]
Metrics: ["capacity fade rate", "crossover rate"]
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; capacity fade rate; commercial anion exchange membrane; crossover rate; membrane selectivity; nanoporous size-exclusion membrane; sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212; capacity fade rate; commercial anion exchange membrane; crossover rate; membrane selectivity; nanoporous size-exclusion membrane; sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation Description: Comparison of five membranes in MV/TEMPO cell at 100 mA/cm2: selectivities 85-97%, crossover rates 0.3-2.5e-6 cm2/s, capacity fade rates 0.012-0.065%/cycle Source evidence: Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2

```
#### Evidence 3
- evidence_id: `IEC of PBI|IEC of SNPBI-1.42|IEC of SPEEK/APK|IEC of SPTPC-2.59|PBI|SNPBI-1.42|SPEEK/APK|SPTPC-2.59|area resistance of PBI|area resistance of SNPBI-1.42|area resistance of SPEEK/APK|area resistance of SPTPC-2.59|coulombic efficiency of PBI (40-200 mA/cm2)|coulombic efficiency of SNPBI-1.42 (40-200 mA/cm2)|coulombic efficiency of SPEEK/APK (40-200 mA/cm2)|coulombic efficiency of SPTPC-2.59 (40-200 mA/cm2)|energy efficiency of PBI (40-200 mA/cm2)|energy efficiency of SNPBI-1.42 (40-200 mA/cm2)|energy efficiency of SPEEK/APK (40-200 mA/cm2)|energy efficiency of SPTPC-2.59 (40-200 mA/cm2)|vanadium permeability of PBI|vanadium permeability of SNPBI-1.42|vanadium permeability of SPEEK/APK|vanadium permeability of SPTPC-2.59|voltage efficiency of PBI (40-200 mA/cm2)|voltage efficiency of SNPBI-1.42 (40-200 mA/cm2)|voltage efficiency of SPEEK/APK (40-200 mA/cm2)|voltage efficiency of SPTPC-2.59 (40-200 mA/cm2)|water uptake of PBI|water uptake of SNPBI-1.42|water uptake of SPEEK/APK|water uptake of SPTPC-2.59`
- relation_type: `COMPARISON`
- retrieval_score: `0.163043`
```text
Evidence 3
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARISON
Short claim: Under IEC of PBI = 0.0 mmol/g, IEC of SNPBI-1.42 = 1.42 mmol/g, IEC of SPEEK/APK = 1.26 mmol/g, IEC of SPTPC-2.59 = 2.59 mmol/g, area resistance of PBI = 2.45 ohm·cm², while area resistance of SNPBI-1.42 = 1.15 ohm·cm². Relation: COMPARISON.
Entities: ["PBI", "SNPBI-1.42", "SPEEK/APK", "SPTPC-2.59", "water uptake of PBI = 12 %", "water uptake of SNPBI-1.42 = 18 %", "water uptake of SPEEK/APK = 21 %", "water uptake of SPTPC-2.59 = 28 %", "IEC of PBI", "IEC of SNPBI-1.42", "IEC of SPEEK/APK", "IEC of SPTPC-2.59"]
Metrics: ["area resistance of PBI = 2.45 ohm·cm²", "area resistance of SNPBI-1.42 = 1.15 ohm·cm²", "area resistance of SPEEK/APK = 1.38 ohm·cm²", "area resistance of SPTPC-2.59 = 0.82 ohm·cm²", "coulombic efficiency of PBI (40-200 mA/cm2)", "coulombic efficiency of SNPBI-1.42 (40-200 mA/cm2)", "coulombic efficiency of SPEEK/APK (40-200 mA/cm2)", "coulombic efficiency of SPTPC-2.59 (40-200 mA/cm2)", "energy efficiency of PBI (40-200 mA/cm2)", "energy efficiency of SNPBI-1.42 (40-200 mA/cm2)", "energy efficiency of SPEEK/APK (40-200 mA/cm2)", "energy efficiency of SPTPC-2.59 (40-200 mA/cm2)"]
Values: ["IEC of PBI = 0.0 mmol/g", "IEC of SNPBI-1.42 = 1.42 mmol/g", "IEC of SPEEK/APK = 1.26 mmol/g", "IEC of SPTPC-2.59 = 2.59 mmol/g", "area resistance of PBI = 2.45 ohm·cm²", "area resistance of SNPBI-1.42 = 1.15 ohm·cm²", "area resistance of SPEEK/APK = 1.38 ohm·cm²", "area resistance of SPTPC-2.59 = 0.82 ohm·cm²", "vanadium permeability of PBI = 5e-08 cm²/s", "vanadium permeability of SNPBI-1.42
```
#### Evidence 4
- evidence_id: `TEMPO|energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.163043`
```text
Evidence 4
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, TEMPO achieved/reported energy efficiency.
Entities: ["TEMPO"]
Metrics: ["energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: TEMPO; energy efficiency Relation type: OPERATION Readable labels: TEMPO; energy efficiency Description: TEMPO cell achieved EE of 84.3% at 100 mA/cm2, up to 88.5% at 20 mA/cm2 Source evidence: TEMPO cell achieved EE of 84.3% at 100 mA/cm2, up to 88.5% at 20 mA/cm2

```
#### Evidence 5
- evidence_id: `SPEEK|energy efficiency (SPEEK membrane at 100 mA/cm2)`
- relation_type: `OPERATION`
- retrieval_score: `0.163043`
```text
Evidence 5
Source: chunk-hyperrag-DOC10
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, SPEEK achieved/reported energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %, energy efficiency (SPEEK membrane at 100 mA/cm2).
Entities: ["SPEEK"]
Metrics: ["energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %", "energy efficiency (SPEEK membrane at 100 mA/cm2)"]
Values: ["energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %"]
Conditions: []
Raw support excerpt: SPEEK; energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 % Relation type: OPERATION Readable labels: SPEEK; energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 % Description: SPEEK membrane with 42% sulfonation achieves EE 83% at 100 mA/cm2 Source evidence: SPEEK membrane with 42% sulfonation achieves EE 83% at 100 mA/cm2

```

## DOC01-QA-006 / chem_norm_hypergraph
- Category: `composition`
- Answerable: `True`
- Question: At 100 mA/cm2 and 25 C, both membranes achieve similar EE despite different CE/VE compositions. Explain the performance trade-off and recommend which membrane to use for long-cycle-life stationary storage.
- Reference answer: At 100 mA/cm2 and 25 C, Nafion 117 achieves EE of 80.2% (CE 97.1%, VE 82.6%) while Nafion 212 achieves EE of 80.9% (CE 93.8%, VE 86.2%). The similar EE masks a fundamental trade-off: Nafion 117 prioritizes CE via lower vanadium crossover (1.8 x 10^-7 cm2/s) at the cost of higher resistance (1.65 ohm cm2), while Nafion 212 achieves lower resistance (0.85 ohm cm2) but higher crossover (3.9 x 10^-7 cm2/s). For long-cycle-life stationary storage, Nafion 117 is recommended because its lower crossover yields an estimated capacity fade rate of 0.08% per cycle versus 0.18% per cycle for Nafion 212.
- Generated answer: At 100 mA/cm2 and 25 C, Nafion 117 achieves CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieves CE of 93.8%, VE of 86.2%, and EE of 80.9%. The trade-off is that Nafion 117 has higher coulombic efficiency but lower voltage efficiency, whereas Nafion 212 has lower coulombic efficiency but higher voltage efficiency, resulting in similar energy efficiency. The evidence does not discuss long-cycle-life performance, so a recommendation cannot be made based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.5` | Hallucinated: `True` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `["Nafion 117 crossover: 1.8 x 10^-7 cm2/s, resistance: 1.65 ohm cm2", "Nafion 212 crossover: 3.9 x 10^-7 cm2/s, resistance: 0.85 ohm cm2", "Recommendation: Nafion 117 for long cycle life (0.08% vs 0.18% fade rate)"]`
- Unsupported claims found: `["The evidence does not discuss long-cycle-life performance"]`
- Rationale: The generated answer correctly states the CE, VE, and EE values for both membranes and explains the trade-off, but it fails to provide the crossover and resistance data, and it incorrectly claims that the evidence does not discuss long-cycle-life performance, leading to an abstention from recommending. This claim is likely unsupported as the reference answer includes such information. Therefore, the answer is incomplete and contains a hallucination, making it poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `condition:current_density|condition:temperature|membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.228261`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under temperature, condition:temperature, current density, while condition:current_density. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: ["temperature", "condition:temperature"]
Raw support excerpt: current density; temperature; Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: current density; temperature; Nafion 117; Nafion 212 Description: Comprehensive comparison of Nafion 117 and Nafion 212 membranes across current densities (40-200 mA/cm2) and temperatures (25-40 C) for coulombic, voltage, and energy efficiency. Source evidence: At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%.

```
#### Evidence 2
- evidence_id: `condition:bi3_concentration|condition:current_density|metric:ce|metric:ve`
- relation_type: `COMPARISON`
- retrieval_score: `0.222826`
```text
Evidence 2
Source: chunk-hyperrag-DOC06
Relation/Type: COMPARISON
Short claim: Under Bi3+ concentration, current density, while coulombic efficiency = 93 %. Relation: COMPARISON.
Entities: ["condition:bi3_concentration", "metric:ce", "metric:ve"]
Metrics: ["current density", "coulombic efficiency = 93 %", "voltage efficiency", "condition:current_density"]
Values: ["coulombic efficiency = 93 %"]
Conditions: ["Bi3+ concentration"]
Raw support excerpt: Bi3+ concentration; current density; coulombic efficiency = 93 %; voltage efficiency Relation type: COMPARISON Readable labels: Bi3+ concentration; current density; coulombic efficiency = 93 %; voltage efficiency Description: Comparison of efficiencies at different Bi3+ concentrations (0.5-5.0 mmol/L) and current densities (40-160 mA/cm2); baseline without Bi3+ yields lower values Source evidence: With Bi3+ addition, Coulombic efficiency improved to the range of 87-96% and energy efficiency reached 62-85%

```
#### Evidence 3
- evidence_id: `condition:current_density|metric:ce`
- relation_type: `OPERATION`
- retrieval_score: `0.190217`
```text
Evidence 3
Source: chunk-hyperrag-DOC08<SEP>chunk-hyperrag-DOC06
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, metric:ce achieved/reported current density, coulombic efficiency = 93 %, condition:current_density.
Entities: ["metric:ce"]
Metrics: ["current density", "coulombic efficiency = 93 %", "condition:current_density"]
Values: ["coulombic efficiency = 93 %"]
Conditions: []
Raw support excerpt: current density; coulombic efficiency = 93 % Relation type: OPERATION Readable labels: current density; coulombic efficiency = 93 % Description: Coulombic efficiency measured at various current densities from 40 to 160 mA/cm2 Source evidence: Coulombic efficiency measured at various current densities from 40 to 160 mA/cm2 ; Coulombic efficiency measured at varying current densities (10-40 mA/cm2)

```
#### Evidence 4
- evidence_id: `condition:charge_cutoff_voltage|condition:current_density|condition:discharge_cutoff_voltage|condition:flow_rate|membrane:pbi|membrane:snpbi_1_42|membrane:speek_apk|membrane:sptpc_2_59|unresolved:single_cell_vrfb`
- relation_type: `OPERATION`
- retrieval_score: `0.163043`
```text
Evidence 4
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, flow rate, PBI, SNPBI-1.42, SPEEK/APK achieved/reported charge cutoff voltage, current density, discharge cutoff voltage, condition:charge_cutoff_voltage.
Entities: ["flow rate", "PBI", "SNPBI-1.42", "SPEEK/APK", "SPTPC-2.59", "single-cell VRFB", "condition:flow_rate", "membrane:pbi", "membrane:snpbi_1_42", "membrane:speek_apk", "membrane:sptpc_2_59", "unresolved:single_cell_vrfb"]
Metrics: ["charge cutoff voltage", "current density", "discharge cutoff voltage", "condition:charge_cutoff_voltage", "condition:current_density", "condition:discharge_cutoff_voltage"]
Values: []
Conditions: []
Raw support excerpt: charge cutoff voltage; current density; discharge cutoff voltage; flow rate; PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59; single-cell VRFB Relation type: OPERATION Readable labels: charge cutoff voltage; current density; discharge cutoff voltage; flow rate; PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59; single-cell VRFB Description: All four non-fluorinated membranes were tested in a single cell VRFB under identical conditions: current density range 40-200 mA/cm2, flow rate 40 mL/min, charge cutoff 1.65 V, discharge cutoff 0.8 V. Source evidence: Single cell VRFB tests were conducted using an active electrode area of 10 cm2 ...

```
#### Evidence 5
- evidence_id: `electrode:graphite_composite_bipolar_plates_with_single_pass_serpentine_flow_fields|membrane:microporous_polyethylene_separator_celgard_2500|system:silicone_gaskets|system:stainless_steel_endplates|unresolved:graphite_felt_sgl_carbon_gfd_4_6_ea`
- relation_type: `OPERATION`
- retrieval_score: `0.163043`
```text
Evidence 5
Source: chunk-hyperrag-DOC06
Relation/Type: OPERATION
Short claim: Evidence reports microporous polyethylene separator (Celgard 2500), silicone gaskets, stainless steel endplates, membrane:microporous_polyethylene_separator_celgard_2500, system:silicone_gaskets, system:stainless_steel_endplates. Conditions: graphite composite bipolar plates with single-pass serpentine flow fields, graphite felt (SGL Carbon GFD 4.6 EA), electrode:graphite_composite_bipolar_plates_with_single_pass_serpentine_flow_fields, unresolved:graphite_felt_sgl_carbon_gfd_4_6_ea.
Entities: ["microporous polyethylene separator (Celgard 2500)", "silicone gaskets", "stainless steel endplates", "membrane:microporous_polyethylene_separator_celgard_2500", "system:silicone_gaskets", "system:stainless_steel_endplates"]
Metrics: []
Values: []
Conditions: ["graphite composite bipolar plates with single-pass serpentine flow fields", "graphite felt (SGL Carbon GFD 4.6 EA)", "electrode:graphite_composite_bipolar_plates_with_single_pass_serpentine_flow_fields", "unresolved:graphite_felt_sgl_carbon_gfd_4_6_ea"]
Raw support excerpt: graphite composite bipolar plates with single-pass serpentine flow fields; microporous polyethylene separator (Celgard 2500); silicone gaskets; stainless steel endplates; graphite felt (SGL Carbon GFD 4.6 EA) Relation type: OPERATION Readable labels: graphite composite bipolar plates with single-pass serpentine flow fields; microporous polyethylene separator (Celgard 2500); silicone gaskets; stainless steel endplates; graphite felt (SGL Carbon GFD 4.6 EA) Description: Cell assembl
```

## DOC01-QA-008 / text_segments
- Category: `comparison`
- Answerable: `True`
- Question: Explain the degradation chain initiated by vanadium crossover in a VRFB and compare the estimated capacity fade rates for Nafion 117 and Nafion 212.
- Reference answer: Vanadium crossover initiates a degradation cascade: (1) vanadium ions permeate through the membrane creating state-of-charge imbalance between half-cells, (2) this manifests as progressive reduction in accessible discharge capacity, (3) self-discharge reactions between permeated vanadium ions and counter-ions at opposing electrodes create exothermic hotspots, and (4) these hotspots accelerate further membrane and electrode degradation. The estimated capacity fade rates from crossover alone at 100 mA/cm2 and 25 C are 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212, reflecting the approximately 2.2x higher vanadium permeability of the thinner membrane.
- Generated answer: The degradation chain initiated by vanadium crossover in a VRFB involves vanadium crossover exacerbating state-of-charge (SOC) imbalance between the positive and negative half-cells, which precipitates capacity fading. The estimated capacity fade rates attributable to vanadium crossover alone are approximately 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212 under standard operating conditions at 100 mA/cm2 and 25°C.
- Quality: `SATISFACTORY` | Good: `False` | Satisfactory+: `True` | KPC: `0.6667` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Self-discharge generates local hotspots", "Hotspots accelerate further degradation"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly identifies SOC imbalance and capacity fading, and provides the correct fade rates for Nafion 117 and 212. However, it fails to mention the self-discharge reactions that create exothermic hotspots and the subsequent acceleration of degradation, which are key parts of the degradation chain. Therefore, the answer is partially complete but missing two required key points. It is non-hallucinated and partially useful, so it is rated SATISFACTORY.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.617647`
```text
Evidence 1
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: The higher CE of Nafion 117 also implies slower rates of capacity degradation over extended cycling, as vanadium crossover is a primary contributor to the capacity fading mechanism in VRFBs. Given its approximately 50% lower vanadium permeability, Nafion 117 is expected to exhibit substantially slower capacity fade rates during extended cycling compared to Nafion 212. Based on the measured permeability values and the electrolyte volumes employed, the capacity fade rate attributable to vanadium crossover alone is estimated at approximately 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212 under standard operating conditions at 100 mA/cm2 and 25 C. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.617647`
```text
Evidence 2
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. VRFB Performance Evaluation ### 4.1 Coulombic Efficiency The coulombic efficiency of all four membranes showed the expected positive correlation with current density, consistent with the fundamental mechanism wherein the parasitic crossover flux becomes a smaller fraction of the total current at higher operational currents. At 100 mA/cm2, the CE was 98.1%, which is competitive with Nafion 117 and superior to Nafion 212. ### 6.3 Degradation Chain Analysis The degradation of non-fluorinated VRFB membranes follows a chain process that initiates with chemical attack on the polymer backbone or pendant acid groups, progresses through loss of ion exchange capacity and/or mechanical integrity, and manifests as declining voltage efficiency and/or increasing vanadium crossover.

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC09`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.617647`
```text
Evidence 3
Source: DOC09
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: The crossover rate of TEMPO through the Nafion 117 membrane was measured at 0.8 x 10^-6 cm2/s, contributing to a gradual capacity fade over extended cycling. Under standardized conditions (100 mA/cm2, Nafion 117 membrane, room temperature, 500 cycle duration), the capacity fade rates were: AQDS at pH 12 showed 0.025%/cycle, TEMPO in nonaqueous electrolyte showed 0.02%/cycle, PSV (functionalized viologen) showed 0.018%/cycle, MV at pH 7 showed 0.055%/cycle, and unfunctionalized TEMPO in the presence of 50 ppm water showed 0.045%/cycle. Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2: Nafion 117 (selectivity 88%, MV crossover 2.1 x 10^-6 cm2/s, capacity fade 0.055%/cycle), Nafion 212 (selectivity 85%, MV crossover 2.5 x 10^-6 cm2/s, capacity fade 0.065%/cycle), a sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation (selectivity 92%, MV crossover 1.2 x 10^-6 cm2/s, capacity fade 0.038%/cycle), a commercial anion exchange membrane (selectivity 90%, MV crossover 1.5 x 10^-6 cm2/s, capacity fade 0.042%/cycle), and a nanoporous size-exclusion membrane (selectivity 97%, MV crossover 0.3 x 10^-6 cm2/s, capacity fade 0.012%/cycle). An optimal linear flow velocity of 10-15 cm/s was identified for TEMPO/viologen cells with Nafion 117, balancing mass transport requirements against crossover-induced fade.

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC05`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.573529`
```text
Evidence 4
Source: DOC05
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: The results demonstrate that elevated temperatures accelerate vanadium ion crossover through the ion-exchange membrane, exacerbate state-of-charge (SOC) imbalance between the positive and negative half-cells, and precipitate more rapid capacity fading. Post-test analysis of the electrolyte revealed significant redistribution of vanadium species between the half-cells, consistent with enhanced crossover as a primary contributor to the observed capacity loss. Assuming an Arrhenius relationship between temperature and capacity fading rate, the effective activation energy for the dominant degradation process can be estimated from the relative fading rates at the three temperatures. At 25 C, the measured crossover coefficient was 2.1 x 10^-7 cm2/s, which is in good agreement with literature values for Nafion 117 in contact with vanadium electrolyte solutions.

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC10`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.573529`
```text
Evidence 5
Source: DOC10
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: At 100 mA/cm2, a SPEEK membrane with 42% sulfonation degree achieved an EE of 83% compared to 84% for Nafion 117, but reduced the capacity fade rate from 0.035%/cycle to 0.018%/cycle. A benchmark AEM (Fumatech FAP-450) achieved an EE of 79% at 100 mA/cm2 with iron-chromium electrolyte, compared to 82% for Nafion 117, but with significantly improved chromium retention (crossover rate reduced by 40%). A nanoporous ceramic-polymer composite membrane demonstrated improved lead rejection (selectivity 93%) with an ASR of 3.2 ohm cm2, achieving an EE of 74% at 30 mA/cm2 compared to 76% with Nafion 117 but with reduced capacity fade from 0.08%/cycle to 0.04%/cycle. The quantitative performance comparison at matched conditions shows that ORFB systems with optimized molecular design achieve the highest energy efficiency (76-88%) and lowest capacity fade rates (0.01-0.018%/cycle), followed closely by advanced VRFB configurations (EE 78-84%, fade 0.018-0.035%/cycle).

```

## DOC01-QA-008 / original_hypergraph
- Category: `comparison`
- Answerable: `True`
- Question: Explain the degradation chain initiated by vanadium crossover in a VRFB and compare the estimated capacity fade rates for Nafion 117 and Nafion 212.
- Reference answer: Vanadium crossover initiates a degradation cascade: (1) vanadium ions permeate through the membrane creating state-of-charge imbalance between half-cells, (2) this manifests as progressive reduction in accessible discharge capacity, (3) self-discharge reactions between permeated vanadium ions and counter-ions at opposing electrodes create exothermic hotspots, and (4) these hotspots accelerate further membrane and electrode degradation. The estimated capacity fade rates from crossover alone at 100 mA/cm2 and 25 C are 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212, reflecting the approximately 2.2x higher vanadium permeability of the thinner membrane.
- Generated answer: Vanadium crossover initiates a degradation chain by causing capacity fade over cycling. The estimated capacity fade rates at 100 mA/cm² and 25°C are 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212.
- Quality: `SATISFACTORY` | Good: `False` | Satisfactory+: `True` | KPC: `0.3333333333333333` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Crossover creates SOC imbalance", "Progressive capacity reduction", "Self-discharge generates local hotspots", "Hotspots accelerate further degradation"]`
- Unsupported claims found: `[]`
- Rationale: The answer correctly provides the fade rates for Nafion 117 and Nafion 212, but fails to explain the degradation chain steps (SOC imbalance, progressive capacity reduction, self-discharge hotspots, accelerated degradation). It covers only 2 of 6 required key points, making it incomplete. However, it is not hallucinated and partially addresses the question.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|Nafion 212|capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C|capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C|vanadium crossover`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.502941`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: CAUSES_OR_AFFECTS
Short claim: Nafion 117, Nafion 212 is linked to capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle, capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle, vanadium crossover. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle", "vanadium crossover", "capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C"]
Values: ["capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle", "capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle; capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle; vanadium crossover Relation type: CAUSES_OR_AFFECTS Readable labels: Nafion 117; Nafion 212; capacity fade rate of Nafion 117 at 100 mA/cm2 and 25 C = 0.08 % per cycle; capacity fade rate of Nafion 212 at 100 mA/cm2 and 25 C = 0.18 % per cycle; vanadium crossover Description: Vanadium crossover causes capacity fade; Nafion 117 with lower permeability has a capacity fade rate of 0.08%/cycle, while Nafion 212 with higher permeability has 0.18%/cycle at 100 mA/cm2 and 25 C. Source evidence: the capacity fade rate attributable to vanadium crossove
```
#### Evidence 2
- evidence_id: `capacity fade|vanadium crossover`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.470588`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to capacity fade, vanadium crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fade", "vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fade; vanadium crossover Relation type: CAUSES_OR_AFFECTS Readable labels: capacity fade; vanadium crossover Description: Vanadium crossover leads to capacity fade over cycling. Source evidence: Vanadium crossover leads to capacity fade over cycling.

```
#### Evidence 3
- evidence_id: `Nafion 117|Nafion 212`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.426471`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Evidence reports Nafion 117, Nafion 212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212 Description: The study systematically compares Nafion 117 and Nafion 212 across various performance metrics and conditions. Source evidence: The study systematically compares Nafion 117 and Nafion 212 across various performance metrics and conditions.

```
#### Evidence 4
- evidence_id: `Capacity fade|Vanadium crossover`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.426471`
```text
Evidence 4
Source: chunk-hyperrag-DOC04
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to Capacity fade, Vanadium crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["Capacity fade", "Vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: Capacity fade; Vanadium crossover Relation type: CAUSES_OR_AFFECTS Readable labels: Capacity fade; Vanadium crossover Description: Elevated vanadium crossover causes capacity fade. Source evidence: Elevated vanadium crossover causes capacity fade.

```
#### Evidence 5
- evidence_id: `capacity fade rate|membrane selectivity`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.345588`
```text
Evidence 5
Source: chunk-hyperrag-DOC09<SEP>chunk-hyperrag-DOC10
Relation/Type: CAUSES_OR_AFFECTS
Short claim: membrane selectivity is linked to capacity fade rate. Conditions: not explicitly stated.
Entities: ["membrane selectivity"]
Metrics: ["capacity fade rate"]
Values: []
Conditions: []
Raw support excerpt: capacity fade rate; membrane selectivity Relation type: CAUSES_OR_AFFECTS Readable labels: capacity fade rate; membrane selectivity Description: High membrane selectivity (>95%) is required to keep capacity fade rate below 0.02%/cycle. Source evidence: Higher membrane selectivity reduces capacity fade by limiting crossover. ; High membrane selectivity (>95%) is required to keep capacity fade rate below 0.02%/cycle.

```

## DOC01-QA-008 / chem_prompt_graph
- Category: `comparison`
- Answerable: `True`
- Question: Explain the degradation chain initiated by vanadium crossover in a VRFB and compare the estimated capacity fade rates for Nafion 117 and Nafion 212.
- Reference answer: Vanadium crossover initiates a degradation cascade: (1) vanadium ions permeate through the membrane creating state-of-charge imbalance between half-cells, (2) this manifests as progressive reduction in accessible discharge capacity, (3) self-discharge reactions between permeated vanadium ions and counter-ions at opposing electrodes create exothermic hotspots, and (4) these hotspots accelerate further membrane and electrode degradation. The estimated capacity fade rates from crossover alone at 100 mA/cm2 and 25 C are 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212, reflecting the approximately 2.2x higher vanadium permeability of the thinner membrane.
- Generated answer: Vanadium crossover initiates capacity fade through electrolyte imbalance (Evidence 1). Elevated crossover leads to capacity fade and self-discharge, reducing system efficiency (Evidence 3). Synergistic crossover and dendrite growth cause non-linear capacity fade (Evidence 5). For Nafion 117, the estimated capacity fade rate is 0.02-0.05%/cycle (Evidence 2). The retrieved evidence does not provide a capacity fade rate for Nafion 212, so a comparison cannot be made.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `True` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Crossover creates SOC imbalance", "Progressive capacity reduction", "Self-discharge generates local hotspots", "Hotspots accelerate further degradation", "Nafion 117 fade rate: 0.08% per cycle", "Nafion 212 fade rate: 0.18% per cycle"]`
- Unsupported claims found: `["Synergistic crossover and dendrite growth cause non-linear capacity fade", "For Nafion 117, the estimated capacity fade rate is 0.02-0.05%/cycle", "The retrieved evidence does not provide a capacity fade rate for Nafion 212"]`
- Rationale: The generated answer fails to cover any of the required key points. It provides incorrect capacity fade rates for Nafion 117 (0.02-0.05%/cycle instead of 0.08%/cycle) and incorrectly states that no rate is available for Nafion 212, which contradicts the reference answer. It also introduces an unsupported claim about synergistic crossover and dendrite growth. The answer is not grounded in the reference and contains hallucinations.

### Evidence Blocks
#### Evidence 1
- evidence_id: `capacity fade|vanadium crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.514706`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fade, vanadium crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fade", "vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fade; vanadium crossover Relation type: DEGRADATION Readable labels: capacity fade; vanadium crossover Description: Vanadium crossover initiates capacity fade through electrolyte imbalance Source evidence: Vanadium crossover initiates capacity fade through electrolyte imbalance

```
#### Evidence 2
- evidence_id: `capacity fade rate (VRFB with Nafion 117)|vanadium crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.477941`
```text
Evidence 2
Source: chunk-hyperrag-DOC10
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fade rate (VRFB with Nafion 117), vanadium crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fade rate (VRFB with Nafion 117)", "vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fade rate (VRFB with Nafion 117); vanadium crossover Relation type: DEGRADATION Readable labels: capacity fade rate (VRFB with Nafion 117); vanadium crossover Description: Vanadium crossover through Nafion 117 causes capacity fade of 0.02-0.05%/cycle Source evidence: Vanadium crossover through Nafion 117 causes capacity fade of 0.02-0.05%/cycle

```
#### Evidence 3
- evidence_id: `capacity fade|increased vanadium crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.389706`
```text
Evidence 3
Source: chunk-hyperrag-DOC04
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fade, increased vanadium crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fade", "increased vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fade; increased vanadium crossover Relation type: DEGRADATION Readable labels: capacity fade; increased vanadium crossover Description: Elevated crossover leads to capacity fade and self-discharge, reducing system efficiency Source evidence: Elevated crossover leads to capacity fade and self-discharge, reducing system efficiency

```
#### Evidence 4
- evidence_id: `capacity fade|vanadium ion crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.389706`
```text
Evidence 4
Source: chunk-hyperrag-DOC05
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fade, vanadium ion crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fade", "vanadium ion crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fade; vanadium ion crossover Relation type: DEGRADATION Readable labels: capacity fade; vanadium ion crossover Description: Vanadium crossover leads to capacity fading Source evidence: Vanadium crossover leads to capacity fading

```
#### Evidence 5
- evidence_id: `capacity fade|coupled degradation chain`
- relation_type: `DEGRADATION`
- retrieval_score: `0.389706`
```text
Evidence 5
Source: chunk-hyperrag-DOC07
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fade. Conditions: coupled degradation chain.
Entities: []
Metrics: ["capacity fade"]
Values: []
Conditions: ["coupled degradation chain"]
Raw support excerpt: capacity fade; coupled degradation chain Relation type: DEGRADATION Readable labels: capacity fade; coupled degradation chain Description: synergistic crossover and dendrite growth cause non-linear capacity fade Source evidence: synergistic crossover and dendrite growth cause non-linear capacity fade

```

## DOC01-QA-008 / chem_prompt_hypergraph
- Category: `comparison`
- Answerable: `True`
- Question: Explain the degradation chain initiated by vanadium crossover in a VRFB and compare the estimated capacity fade rates for Nafion 117 and Nafion 212.
- Reference answer: Vanadium crossover initiates a degradation cascade: (1) vanadium ions permeate through the membrane creating state-of-charge imbalance between half-cells, (2) this manifests as progressive reduction in accessible discharge capacity, (3) self-discharge reactions between permeated vanadium ions and counter-ions at opposing electrodes create exothermic hotspots, and (4) these hotspots accelerate further membrane and electrode degradation. The estimated capacity fade rates from crossover alone at 100 mA/cm2 and 25 C are 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212, reflecting the approximately 2.2x higher vanadium permeability of the thinner membrane.
- Generated answer: Vanadium crossover initiates capacity fade through electrolyte imbalance (Evidence 1). For Nafion 117, vanadium crossover causes a capacity fade of 0.02-0.05%/cycle (Evidence 2). The retrieved evidence does not provide a specific capacity fade rate for Nafion 212, so a direct comparison cannot be made.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.333` | Hallucinated: `True` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Self-discharge generates local hotspots", "Hotspots accelerate further degradation", "Nafion 117 fade rate: 0.08% per cycle", "Nafion 212 fade rate: 0.18% per cycle"]`
- Unsupported claims found: `["Nafion 117 capacity fade rate of 0.02-0.05%/cycle", "Claim that evidence does not provide specific fade rate for Nafion 212"]`
- Rationale: The generated answer only partially addresses the degradation chain by mentioning electrolyte imbalance and capacity fade, but fails to include self-discharge hotspots and accelerated degradation. It provides incorrect capacity fade rates for Nafion 117 (0.02-0.05%/cycle instead of 0.08%/cycle) and incorrectly states that no specific rate is available for Nafion 212, contradicting the reference. The answer is incomplete and contains unsupported claims, making it poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `capacity fade|vanadium crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.514706`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fade, vanadium crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fade", "vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fade; vanadium crossover Relation type: DEGRADATION Readable labels: capacity fade; vanadium crossover Description: Vanadium crossover initiates capacity fade through electrolyte imbalance Source evidence: Vanadium crossover initiates capacity fade through electrolyte imbalance

```
#### Evidence 2
- evidence_id: `capacity fade rate (VRFB with Nafion 117)|vanadium crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.477941`
```text
Evidence 2
Source: chunk-hyperrag-DOC10
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fade rate (VRFB with Nafion 117), vanadium crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fade rate (VRFB with Nafion 117)", "vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fade rate (VRFB with Nafion 117); vanadium crossover Relation type: DEGRADATION Readable labels: capacity fade rate (VRFB with Nafion 117); vanadium crossover Description: Vanadium crossover through Nafion 117 causes capacity fade of 0.02-0.05%/cycle Source evidence: Vanadium crossover through Nafion 117 causes capacity fade of 0.02-0.05%/cycle

```
#### Evidence 3
- evidence_id: `H2SO4 concentration|capacity fade|chemical attack of polymer backbone|increased vanadium crossover|self-discharge`
- relation_type: `DEGRADATION`
- retrieval_score: `0.447059`
```text
Evidence 3
Source: chunk-hyperrag-DOC04
Relation/Type: DEGRADATION
Short claim: chemical attack of polymer backbone, self-discharge is linked to capacity fade, increased vanadium crossover. Conditions: H2SO4 concentration.
Entities: ["chemical attack of polymer backbone", "self-discharge"]
Metrics: ["capacity fade", "increased vanadium crossover"]
Values: []
Conditions: ["H2SO4 concentration"]
Raw support excerpt: H2SO4 concentration; capacity fade; chemical attack of polymer backbone; increased vanadium crossover; self-discharge Relation type: DEGRADATION Readable labels: H2SO4 concentration; capacity fade; chemical attack of polymer backbone; increased vanadium crossover; self-discharge Description: High H2SO4 concentration (5.0 mol/L) accelerates chemical attack on Nafion 117, increasing vanadium crossover, which causes capacity fade and self-discharge after extended cycling Source evidence: High acid concentrations contributed to accelerated membrane degradation... increased vanadium crossover... capacity fade and self-discharge

```
#### Evidence 4
- evidence_id: `Nafion 117|Nafion 212|capacity fade rate|commercial anion exchange membrane|crossover rate|membrane selectivity|nanoporous size-exclusion membrane|sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation`
- relation_type: `COMPARISON`
- retrieval_score: `0.446691`
```text
Evidence 4
Source: chunk-hyperrag-DOC09
Relation/Type: COMPARISON
Short claim: Under the reported conditions, capacity fade rate, while crossover rate. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "commercial anion exchange membrane", "membrane selectivity", "nanoporous size-exclusion membrane", "sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation"]
Metrics: ["capacity fade rate", "crossover rate"]
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; capacity fade rate; commercial anion exchange membrane; crossover rate; membrane selectivity; nanoporous size-exclusion membrane; sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212; capacity fade rate; commercial anion exchange membrane; crossover rate; membrane selectivity; nanoporous size-exclusion membrane; sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation Description: Comparison of five membranes in MV/TEMPO cell at 100 mA/cm2: selectivities 85-97%, crossover rates 0.3-2.5e-6 cm2/s, capacity fade rates 0.012-0.065%/cycle Source evidence: Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2

```
#### Evidence 5
- evidence_id: `capacity fade|increased vanadium crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.389706`
```text
Evidence 5
Source: chunk-hyperrag-DOC04
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fade, increased vanadium crossover. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fade", "increased vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fade; increased vanadium crossover Relation type: DEGRADATION Readable labels: capacity fade; increased vanadium crossover Description: Elevated crossover leads to capacity fade and self-discharge, reducing system efficiency Source evidence: Elevated crossover leads to capacity fade and self-discharge, reducing system efficiency

```

## DOC01-QA-008 / chem_norm_hypergraph
- Category: `comparison`
- Answerable: `True`
- Question: Explain the degradation chain initiated by vanadium crossover in a VRFB and compare the estimated capacity fade rates for Nafion 117 and Nafion 212.
- Reference answer: Vanadium crossover initiates a degradation cascade: (1) vanadium ions permeate through the membrane creating state-of-charge imbalance between half-cells, (2) this manifests as progressive reduction in accessible discharge capacity, (3) self-discharge reactions between permeated vanadium ions and counter-ions at opposing electrodes create exothermic hotspots, and (4) these hotspots accelerate further membrane and electrode degradation. The estimated capacity fade rates from crossover alone at 100 mA/cm2 and 25 C are 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212, reflecting the approximately 2.2x higher vanadium permeability of the thinner membrane.
- Generated answer: Vanadium crossover initiates capacity fading by creating electrolyte imbalance and self-discharge. The evidence does not provide estimated capacity fade rates for Nafion 117 and Nafion 212, so a comparison cannot be made.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.33` | Hallucinated: `True` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Self-discharge generates local hotspots", "Hotspots accelerate further degradation", "Nafion 117 fade rate: 0.08% per cycle", "Nafion 212 fade rate: 0.18% per cycle"]`
- Unsupported claims found: `["The evidence does not provide estimated capacity fade rates for Nafion 117 and Nafion 212"]`
- Rationale: The generated answer partially describes the degradation chain (SOC imbalance and capacity fading) but omits critical details about hotspot generation and accelerated degradation. It incorrectly claims that the evidence lacks capacity fade rates, which contradicts the reference answer that provides specific rates (0.08% and 0.18% per cycle). This claim is unsupported and constitutes a hallucination. The answer fails to provide the required comparison, resulting in low key point coverage.

### Evidence Blocks
#### Evidence 1
- evidence_id: `membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.558824`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Evidence reports Nafion 117, Nafion 212, membrane:nafion_117, membrane:nafion_212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212 Description: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures. Source evidence: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures.

```
#### Evidence 2
- evidence_id: `active_species:v_ii_v_iii|degradation:capacity_fading|degradation:vanadium_crossover|electrode:carbon_felt|membrane:nafion_117|species:h2so4|unresolved:vo2_plus_vo2_plus`
- relation_type: `COMPOSITION`
- retrieval_score: `0.42437`
```text
Evidence 2
Source: chunk-hyperrag-DOC10
Relation/Type: COMPOSITION
Short claim: In the reported system, under the stated conditions, V(II)/V(III), carbon felt, Nafion 117, H2SO4 achieved/reported capacity fading, vanadium crossover, degradation:capacity_fading, degradation:vanadium_crossover.
Entities: ["V(II)/V(III)", "carbon felt", "Nafion 117", "H2SO4", "VO2+/VO2+", "active_species:v_ii_v_iii", "electrode:carbon_felt", "membrane:nafion_117", "species:h2so4", "unresolved:vo2_plus_vo2_plus"]
Metrics: ["capacity fading", "vanadium crossover", "degradation:capacity_fading", "degradation:vanadium_crossover"]
Values: []
Conditions: []
Raw support excerpt: V(II)/V(III); capacity fading; vanadium crossover; carbon felt; Nafion 117; H2SO4; VO2+/VO2+ Relation type: COMPOSITION Readable labels: V(II)/V(III); capacity fading; vanadium crossover; carbon felt; Nafion 117; H2SO4; VO2+/VO2+ Description: All-vanadium RFB system with sulfuric acid electrolyte, Nafion membrane, carbon felt electrodes, vanadium crossover degradation leading to capacity fading Source evidence: The VRFB employs V2+/V3+ and VO2+/VO2+ redox couples in sulfuric acid electrolyte...The primary degradation mechanism is vanadium crossover

```
#### Evidence 3
- evidence_id: `membrane:fumatech_fap_450|membrane:microporous_polyolefin_separator|membrane:nafion_115|membrane:nafion_117|membrane:nafion_212|membrane:nanoporous_ceramic_polymer_composite_membrane|membrane:size_exclusion_membrane|unresolved:speek`
- relation_type: `COMPARISON`
- retrieval_score: `0.415441`
```text
Evidence 3
Source: chunk-hyperrag-DOC10
Relation/Type: COMPARISON
Short claim: Evidence reports Fumatech FAP-450, microporous polyolefin separator, Nafion 115, Nafion 117, Nafion 212, size-exclusion membrane. Conditions: nanoporous ceramic-polymer composite membrane.
Entities: ["Fumatech FAP-450", "microporous polyolefin separator", "Nafion 115", "Nafion 117", "Nafion 212", "size-exclusion membrane", "SPEEK", "membrane:fumatech_fap_450", "membrane:microporous_polyolefin_separator", "membrane:nafion_115", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: []
Values: []
Conditions: ["nanoporous ceramic-polymer composite membrane"]
Raw support excerpt: Fumatech FAP-450; microporous polyolefin separator; Nafion 115; Nafion 117; Nafion 212; nanoporous ceramic-polymer composite membrane; size-exclusion membrane; SPEEK Relation type: COMPARISON Readable labels: Fumatech FAP-450; microporous polyolefin separator; Nafion 115; Nafion 117; Nafion 212; nanoporous ceramic-polymer composite membrane; size-exclusion membrane; SPEEK Description: Membrane types across RFB platforms with selectivity requirements above 95% universal; specific membranes compared for each chemistry Source evidence: Membrane selectivity above 95% is required for capacity fade below 0.02%/cycle...SPEEK improved vanadium selectivity...size-exclusion membranes for nonaqueous

```
#### Evidence 4
- evidence_id: `active_species:v_v|degradation:capacity_fading|degradation:chemical_attack_by_v_v_on_aromatic_backbone|degradation:desulfonation|degradation:loss_of_ion_exchange_capacity|degradation:vanadium_crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.394608`
```text
Evidence 4
Source: chunk-hyperrag-DOC02
Relation/Type: DEGRADATION
Short claim: V(V), chemical attack by V(V) on aromatic backbone, desulfonation is linked to capacity fading, loss of ion exchange capacity, vanadium crossover. Conditions: not explicitly stated.
Entities: ["V(V)", "chemical attack by V(V) on aromatic backbone", "desulfonation", "active_species:v_v", "degradation:chemical_attack_by_v_v_on_aromatic_backbone", "degradation:desulfonation"]
Metrics: ["capacity fading", "loss of ion exchange capacity", "vanadium crossover", "degradation:capacity_fading", "degradation:loss_of_ion_exchange_capacity", "degradation:vanadium_crossover"]
Values: []
Conditions: []
Raw support excerpt: V(V); capacity fading; chemical attack by V(V) on aromatic backbone; desulfonation; loss of ion exchange capacity; vanadium crossover Relation type: DEGRADATION Readable labels: V(V); capacity fading; chemical attack by V(V) on aromatic backbone; desulfonation; loss of ion exchange capacity; vanadium crossover Description: Degradation chain in non-fluorinated membranes: V(V) attacks aromatic backbones, desulfonation reduces IEC, vanadium crossover causes capacity fade. Source evidence: The primary degradation mechanism involves attack by the strongly oxidizing V(V) species (VO2+) on the aromatic polymer backbone ... vanadium crossover leads to capacity fading.

```
#### Evidence 5
- evidence_id: `degradation:capacity_fading|degradation:vanadium_crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.389706`
```text
Evidence 5
Source: chunk-hyperrag-DOC02<SEP>chunk-hyperrag-DOC10<SEP>chunk-hyperrag-DOC01
Relation/Type: DEGRADATION
Short claim: The reported factor is linked to capacity fading, vanadium crossover, degradation:capacity_fading. Conditions: not explicitly stated.
Entities: []
Metrics: ["capacity fading", "vanadium crossover", "degradation:capacity_fading", "degradation:vanadium_crossover"]
Values: []
Conditions: []
Raw support excerpt: capacity fading; vanadium crossover Relation type: DEGRADATION Readable labels: capacity fading; vanadium crossover Description: Vanadium crossover initiates capacity fading by creating electrolyte imbalance and self-discharge. Source evidence: Vanadium crossover initiates capacity fading by creating electrolyte imbalance and self-discharge. ; Vanadium crossover through the membrane causes capacity fading over cycling ; Vanadium crossover through membrane leads to capacity loss at 0.02-0.05%/cycle

```

## DOC02-QA-003 / text_segments
- Category: `comparison`
- Answerable: `True`
- Question: Compare the vanadium permeability of all four non-fluorinated membranes tested in this study.
- Reference answer: PBI has the lowest vanadium permeability at 0.5 x 10^-7 cm2/s, followed by SNPBI-1.42 at 0.95 x 10^-7 cm2/s, then SPEEK/APK at 2.1 x 10^-7 cm2/s, and SPTPC-2.59 has the highest at 3.2 x 10^-7 cm2/s. The permeability increases with IEC, following a roughly linear relationship.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["PBI: 0.5 x 10^-7 cm2/s", "SNPBI-1.42: 0.95 x 10^-7 cm2/s", "SPEEK/APK: 2.1 x 10^-7 cm2/s", "SPTPC-2.59: 3.2 x 10^-7 cm2/s", "Permeability increases with IEC"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer abstains from answering, stating 'I don't know based on the retrieved evidence.' However, the question is answerable and the reference answer provides the required information. The answer covers none of the required key points, provides no useful comparison, and is therefore poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.6875`
```text
Evidence 1
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. ### 3.4 Structure-Transport Correlations The trade-off between proton conductivity (inverse of resistance) and vanadium selectivity (inverse of permeability) defines the fundamental performance envelope for VRFB membranes. VRFB Performance Evaluation ### 4.1 Coulombic Efficiency The coulombic efficiency of all four membranes showed the expected positive correlation with current density, consistent with the fundamental mechanism wherein the parasitic crossover flux becomes a smaller fraction of the total current at higher operational currents. The quantitative relationships between IEC, resistance, permeability, and energy efficiency provide a framework for rational design of next-generation non-fluorinated VRFB membranes.

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC06`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.625`
```text
Evidence 2
Source: DOC06
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: However, the sluggish kinetics of the Cr(III)/Cr(II) redox couple at the negative electrode and competing hydrogen evolution reaction (HER) have historically limited the achievable energy efficiency and operational current density of ICRFB systems. The work addresses three primary objectives: (1) quantifying the kinetic enhancement of the Cr(III)/Cr(II) redox reaction in the presence of Bi3+, (2) characterizing the suppression of parasitic hydrogen evolution achieved through Bi3+ addition, and (3) establishing the relationship between Bi3+ concentration, operational current density, and full-cell performance metrics including Coulombic efficiency, voltage efficiency, and energy efficiency. ### 3.2 Effect of Bi3+ Concentration on Coulombic Efficiency The addition of Bi3+ to the negative electrolyte produced systematic improvements in Coulombic efficiency across all tested current densities. The principal findings are as follows: The addition of Bi3+ at concentrations of 0.5-5.0 mmol/L to the negative electrolyte substantially improves both Coulombic efficiency and energy efficiency across the operational current density range of 40-160 mA/cm2.

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.5625`
```text
Evidence 3
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically varying current density from 40 to 200 mA/cm2 and operating temperature from 25 C to 40 C, we elucidate the fundamental trade-offs between coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) that govern membrane selection. These competing requirements create an intrinsic tension in membrane design: highly selective membranes that effectively block vanadium crossover typically exhibit elevated resistance, while low-resistance membranes often suffer from increased permeability to vanadium species. The approximately 3-4 percentage point gap between Nafion 212 and Nafion 117 CE values at any given current density directly reflects the twofold difference in vanadium permeability between the two membranes. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC05`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.5625`
```text
Evidence 4
Source: DOC05
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a comprehensive experimental investigation into the temperature-dependent behavior of VRFB cells operated at 25 C, 40 C, and 60 C over 500 charge-discharge cycles at a constant current density of 80 mA/cm2. The results demonstrate that elevated temperatures accelerate vanadium ion crossover through the ion-exchange membrane, exacerbate state-of-charge (SOC) imbalance between the positive and negative half-cells, and precipitate more rapid capacity fading. The precipitation of V(V) species as V2O5 at the positive electrode, particularly when local temperatures exceed solubility limits, introduces additional capacity loss mechanisms that may be partially irreversible. By maintaining all other operational parameters constant-including current density at 80 mA/cm2, electrolyte composition at 1.5 M VOSO4 in 3.0 M H2SO4, and electrolyte flow rate at 40 mL/min-we establish a controlled experimental framework wherein observed differences in performance can be confidently attributed to temperature effects.

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC09`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.5625`
```text
Evidence 5
Source: DOC09
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: We analyze the influence of pH, current density, state of charge, and membrane properties on capacity retention, coulombic efficiency, and energy efficiency. Particular attention is given to the molecular degradation mechanisms including radical disproportionation, nucleophilic attack, dimerization, and crossover-induced capacity fade. When tested at 100 mA/cm2, the TEMPO-PEG system achieved a CE of 98.9% and EE of 83.7%, with a capacity fade rate of 0.015%/cycle over 300 cycles. Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2: Nafion 117 (selectivity 88%, MV crossover 2.1 x 10^-6 cm2/s, capacity fade 0.055%/cycle), Nafion 212 (selectivity 85%, MV crossover 2.5 x 10^-6 cm2/s, capacity fade 0.065%/cycle), a sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation (selectivity 92%, MV crossover 1.2 x 10^-6 cm2/s, capacity fade 0.038%/cycle), a commercial anion exchange membrane (selectivity 90%, MV crossover 1.5 x 10^-6 cm2/s, capacity fade 0.042%/cycle), and a nanoporous size-exclusion membrane (selectivity 97%, MV crossover 0.3 x 10^-6 cm2/s, capacity fade 0.012%/cycle).

```

## DOC02-QA-003 / original_hypergraph
- Category: `comparison`
- Answerable: `True`
- Question: Compare the vanadium permeability of all four non-fluorinated membranes tested in this study.
- Reference answer: PBI has the lowest vanadium permeability at 0.5 x 10^-7 cm2/s, followed by SNPBI-1.42 at 0.95 x 10^-7 cm2/s, then SPEEK/APK at 2.1 x 10^-7 cm2/s, and SPTPC-2.59 has the highest at 3.2 x 10^-7 cm2/s. The permeability increases with IEC, following a roughly linear relationship.
- Generated answer: The retrieved evidence does not provide vanadium permeability values for SNPBI-1.42, SPEEK/APK, or SPTPC-2.59. Only the vanadium permeability of PBI is reported as 0.5 × 10⁻⁷ cm²/s. Therefore, a comparison of all four non-fluorinated membranes cannot be made.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `["PBI: 0.5 x 10^-7 cm2/s", "SNPBI-1.42: 0.95 x 10^-7 cm2/s", "SPEEK/APK: 2.1 x 10^-7 cm2/s", "SPTPC-2.59: 3.2 x 10^-7 cm2/s", "Permeability increases with IEC"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer states that the retrieved evidence does not provide vanadium permeability values for three of the four membranes, and therefore a comparison cannot be made. This is an abstention (the answer does not attempt to answer the question). Since the reference answer clearly provides all required values, the abstention is incorrect given the available evidence. The answer covers none of the required key points, is not useful, and is not satisfactory. No hallucination is present because the answer does not fabricate data, but it fails to use the provided evidence correctly.

### Evidence Blocks
#### Evidence 1
- evidence_id: `PBI|SNPBI-1.42|SPEEK/APK|SPTPC-2.59`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.5`
```text
Evidence 1
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARES_WITH
Short claim: Evidence reports PBI, SNPBI-1.42, SPEEK/APK, SPTPC-2.59. Conditions: not explicitly stated.
Entities: ["PBI", "SNPBI-1.42", "SPEEK/APK", "SPTPC-2.59"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59 Relation type: COMPARES_WITH Readable labels: PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59 Description: Four non-fluorinated membrane systems are systematically evaluated for VRFB performance, comparing their IEC, resistance, permeability, and efficiency. Source evidence: This study presents a comprehensive evaluation of four non-fluorinated membrane systems for VRFB applications

```
#### Evidence 2
- evidence_id: `Area-specific resistance|Selectivity|Vanadium permeability`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.333333`
```text
Evidence 2
Source: chunk-hyperrag-DOC02
Relation/Type: ASSOCIATED_WITH
Short claim: In the reported system, under the stated conditions, Selectivity achieved/reported Area-specific resistance, Vanadium permeability.
Entities: ["Selectivity"]
Metrics: ["Area-specific resistance", "Vanadium permeability"]
Values: []
Conditions: []
Raw support excerpt: Area-specific resistance; Selectivity; Vanadium permeability Relation type: ASSOCIATED_WITH Readable labels: Area-specific resistance; Selectivity; Vanadium permeability Description: Selectivity is defined as the ratio of proton conductivity (inverse of area resistance) to vanadium permeability. Source evidence: A selectivity parameter, defined as the ratio of proton conductivity to vanadium permeability

```
#### Evidence 3
- evidence_id: `Nafion 117|Nafion 212|area resistance of Nafion 117 at 25 C|area resistance of Nafion 212 at 25 C|thickness of Nafion 117|thickness of Nafion 212|vanadium permeability of Nafion 117|vanadium permeability of Nafion 212`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.3125`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under the reported conditions, area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, while area resistance of Nafion 212 at 25 C = 0.85 ohm cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "thickness of Nafion 117", "thickness of Nafion 212"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "vanadium permeability of Nafion 117 = 1.8e-07 cm2/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm2/s", "area resistance of Nafion 117 at 25 C", "area resistance of Nafion 212 at 25 C", "vanadium permeability of Nafion 117", "vanadium permeability of Nafion 212"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "thickness of Nafion 117 = 183 um", "thickness of Nafion 212 = 50.8 um", "vanadium permeability of Nafion 117 = 1.8e-07 cm2/s", "vanadium permeability of Nafion 212 = 3.9e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; thickness of Nafion 117 = 183 um; thickness of Nafion 212 = 50.8 um; vanadium permeability of Nafion 117 = 1.8e-07 cm2/s; vanadium permeability of Nafion 212 = 3.9e-07 cm2/s Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of N
```
#### Evidence 4
- evidence_id: `Ion exchange capacity (IEC)|Vanadium permeability`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.3125`
```text
Evidence 4
Source: chunk-hyperrag-DOC02
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to Ion exchange capacity (IEC), Vanadium permeability. Conditions: not explicitly stated.
Entities: []
Metrics: ["Ion exchange capacity (IEC)", "Vanadium permeability"]
Values: []
Conditions: []
Raw support excerpt: Ion exchange capacity (IEC); Vanadium permeability Relation type: CAUSES_OR_AFFECTS Readable labels: Ion exchange capacity (IEC); Vanadium permeability Description: Higher IEC increases vanadium permeability. Source evidence: Higher IEC increases vanadium permeability.

```
#### Evidence 5
- evidence_id: `PBI|PBI IEC|PBI acid doping level|PBI area-specific resistance|PBI coulombic efficiency at 100 mA/cm2|PBI energy efficiency at 100 mA/cm2|PBI vanadium permeability|PBI voltage efficiency at 100 mA/cm2|PBI water uptake`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.3125`
```text
Evidence 5
Source: chunk-hyperrag-DOC02
Relation/Type: ASSOCIATED_WITH
Short claim: In the reported system, under PBI IEC = 0.0 mmol/g, PBI, PBI acid doping level, PBI water uptake = 12 %, PBI IEC achieved/reported PBI area-specific resistance = 2.45 ohm cm2, PBI coulombic efficiency at 100 mA/cm2 = 98.4 %, PBI energy efficiency at 100 mA/cm2 = 71.8 %, PBI vanadium permeability = 0.5 10^-7 cm2/s.
Entities: ["PBI", "PBI acid doping level", "PBI water uptake = 12 %", "PBI IEC", "PBI water uptake"]
Metrics: ["PBI area-specific resistance = 2.45 ohm cm2", "PBI coulombic efficiency at 100 mA/cm2 = 98.4 %", "PBI energy efficiency at 100 mA/cm2 = 71.8 %", "PBI vanadium permeability = 0.5 10^-7 cm2/s", "PBI voltage efficiency at 100 mA/cm2 = 73.0 %", "PBI area-specific resistance", "PBI coulombic efficiency at 100 mA/cm2", "PBI energy efficiency at 100 mA/cm2", "PBI vanadium permeability", "PBI voltage efficiency at 100 mA/cm2"]
Values: ["PBI IEC = 0.0 mmol/g", "PBI area-specific resistance = 2.45 ohm cm2", "PBI coulombic efficiency at 100 mA/cm2 = 98.4 %", "PBI energy efficiency at 100 mA/cm2 = 71.8 %", "PBI vanadium permeability = 0.5 10^-7 cm2/s", "PBI voltage efficiency at 100 mA/cm2 = 73.0 %", "PBI water uptake = 12 %"]
Conditions: ["PBI IEC = 0.0 mmol/g"]
Raw support excerpt: PBI; PBI IEC = 0.0 mmol/g; PBI acid doping level; PBI area-specific resistance = 2.45 ohm cm2; PBI coulombic efficiency at 100 mA/cm2 = 98.4 %; PBI energy efficiency at 100 mA/cm2 = 71.8 %; PBI vanadium permeability = 0.5 10^-7 cm2/s; PBI voltage efficiency at 100 mA/cm2 = 73.0 %; PBI water uptake = 12 %
```

## DOC02-QA-003 / chem_prompt_graph
- Category: `comparison`
- Answerable: `True`
- Question: Compare the vanadium permeability of all four non-fluorinated membranes tested in this study.
- Reference answer: PBI has the lowest vanadium permeability at 0.5 x 10^-7 cm2/s, followed by SNPBI-1.42 at 0.95 x 10^-7 cm2/s, then SPEEK/APK at 2.1 x 10^-7 cm2/s, and SPTPC-2.59 has the highest at 3.2 x 10^-7 cm2/s. The permeability increases with IEC, following a roughly linear relationship.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["PBI: 0.5 x 10^-7 cm2/s", "SNPBI-1.42: 0.95 x 10^-7 cm2/s", "SPEEK/APK: 2.1 x 10^-7 cm2/s", "SPTPC-2.59: 3.2 x 10^-7 cm2/s", "Permeability increases with IEC"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer abstains ('I don't know') despite the question being answerable (Answerable: True). It provides none of the required key points, resulting in zero coverage. The answer is not hallucinated but fails to address the question, making it poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `PBI|SNPBI-1.42`
- relation_type: `COMPARISON<SEP>COMPOSITION`
- retrieval_score: `0.25`
```text
Evidence 1
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARISON<SEP>COMPOSITION
Short claim: Evidence reports PBI, SNPBI-1.42. Conditions: not explicitly stated.
Entities: ["PBI", "SNPBI-1.42"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; SNPBI-1.42 Relation type: COMPARISON<SEP>COMPOSITION Readable labels: PBI; SNPBI-1.42 Description: PBI and SNPBI-1.42 compared on IEC, area resistance, vanadium permeability, water uptake, and efficiencies Source evidence: SNPBI-1.42 is derived from PBI by post-sulfonation using fuming and concentrated sulfuric acid ; PBI and SNPBI-1.42 compared on IEC, area resistance, vanadium permeability, water uptake, and efficiencies

```
#### Evidence 2
- evidence_id: `Nafion 117|vanadium permeability (Nafion 117)`
- relation_type: `OPERATION`
- retrieval_score: `0.1875`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 117 achieved/reported vanadium permeability (Nafion 117) = 1.8e-07 cm2/s, vanadium permeability (Nafion 117).
Entities: ["Nafion 117"]
Metrics: ["vanadium permeability (Nafion 117) = 1.8e-07 cm2/s", "vanadium permeability (Nafion 117)"]
Values: ["vanadium permeability (Nafion 117) = 1.8e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 117; vanadium permeability (Nafion 117) = 1.8e-07 cm2/s Relation type: OPERATION Readable labels: Nafion 117; vanadium permeability (Nafion 117) = 1.8e-07 cm2/s Description: Vanadium permeability of Nafion 117 is 1.8e-7 cm2/s Source evidence: Vanadium permeability of Nafion 117 is 1.8e-7 cm2/s

```
#### Evidence 3
- evidence_id: `Nafion 212|vanadium permeability (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.1875`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported vanadium permeability (Nafion 212) = 3.9e-07 cm2/s, vanadium permeability (Nafion 212).
Entities: ["Nafion 212"]
Metrics: ["vanadium permeability (Nafion 212) = 3.9e-07 cm2/s", "vanadium permeability (Nafion 212)"]
Values: ["vanadium permeability (Nafion 212) = 3.9e-07 cm2/s"]
Conditions: []
Raw support excerpt: Nafion 212; vanadium permeability (Nafion 212) = 3.9e-07 cm2/s Relation type: OPERATION Readable labels: Nafion 212; vanadium permeability (Nafion 212) = 3.9e-07 cm2/s Description: Vanadium permeability of Nafion 212 is 3.9e-7 cm2/s Source evidence: Vanadium permeability of Nafion 212 is 3.9e-7 cm2/s

```
#### Evidence 4
- evidence_id: `electrolyte imbalance|vanadium crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.1875`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: DEGRADATION
Short claim: electrolyte imbalance is linked to vanadium crossover. Conditions: not explicitly stated.
Entities: ["electrolyte imbalance"]
Metrics: ["vanadium crossover"]
Values: []
Conditions: []
Raw support excerpt: electrolyte imbalance; vanadium crossover Relation type: DEGRADATION Readable labels: electrolyte imbalance; vanadium crossover Description: Vanadium crossover creates imbalance in state of charge between half-cells Source evidence: Vanadium crossover creates imbalance in state of charge between half-cells

```
#### Evidence 5
- evidence_id: `1.5 M VOSO4 in 3 M H2SO4|VOSO4`
- relation_type: `COMPOSITION`
- retrieval_score: `0.1875`
```text
Evidence 5
Source: chunk-hyperrag-DOC02
Relation/Type: COMPOSITION
Short claim: Evidence reports 1.5 M VOSO4 in 3 M H2SO4, VOSO4. Conditions: not explicitly stated.
Entities: ["1.5 M VOSO4 in 3 M H2SO4", "VOSO4"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: 1.5 M VOSO4 in 3 M H2SO4; VOSO4 Relation type: COMPOSITION Readable labels: 1.5 M VOSO4 in 3 M H2SO4; VOSO4 Description: Vanadium permeability feed solution contains VOSO4 as vanadium source Source evidence: Vanadium permeability feed solution contains VOSO4 as vanadium source

```

## DOC02-QA-003 / chem_prompt_hypergraph
- Category: `comparison`
- Answerable: `True`
- Question: Compare the vanadium permeability of all four non-fluorinated membranes tested in this study.
- Reference answer: PBI has the lowest vanadium permeability at 0.5 x 10^-7 cm2/s, followed by SNPBI-1.42 at 0.95 x 10^-7 cm2/s, then SPEEK/APK at 2.1 x 10^-7 cm2/s, and SPTPC-2.59 has the highest at 3.2 x 10^-7 cm2/s. The permeability increases with IEC, following a roughly linear relationship.
- Generated answer: The vanadium permeability values are: PBI = 5e-08 cm²/s, SNPBI-1.42 = 9.5e-08 cm²/s, SPEEK/APK = 2.1e-07 cm²/s, SPTPC-2.59 = 3.2e-07 cm²/s. Thus, PBI has the lowest permeability, followed by SNPBI-1.42, then SPEEK/APK, and SPTPC-2.59 has the highest.
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly lists all four vanadium permeability values in the same order as the reference, covers all required key points (PBI, SNPBI-1.42, SPEEK/APK, SPTPC-2.59 with their respective values), and does not include any unsupported claims. The values are given in scientific notation (e.g., 5e-08 cm²/s) which is equivalent to 0.5×10⁻⁷ cm²/s, so no hallucination or conflict. The answer is complete, accurate, and grounded in the provided evidence.

### Evidence Blocks
#### Evidence 1
- evidence_id: `IEC of PBI|IEC of SNPBI-1.42|IEC of SPEEK/APK|IEC of SPTPC-2.59|PBI|SNPBI-1.42|SPEEK/APK|SPTPC-2.59|area resistance of PBI|area resistance of SNPBI-1.42|area resistance of SPEEK/APK|area resistance of SPTPC-2.59|coulombic efficiency of PBI (40-200 mA/cm2)|coulombic efficiency of SNPBI-1.42 (40-200 mA/cm2)|coulombic efficiency of SPEEK/APK (40-200 mA/cm2)|coulombic efficiency of SPTPC-2.59 (40-200 mA/cm2)|energy efficiency of PBI (40-200 mA/cm2)|energy efficiency of SNPBI-1.42 (40-200 mA/cm2)|energy efficiency of SPEEK/APK (40-200 mA/cm2)|energy efficiency of SPTPC-2.59 (40-200 mA/cm2)|vanadium permeability of PBI|vanadium permeability of SNPBI-1.42|vanadium permeability of SPEEK/APK|vanadium permeability of SPTPC-2.59|voltage efficiency of PBI (40-200 mA/cm2)|voltage efficiency of SNPBI-1.42 (40-200 mA/cm2)|voltage efficiency of SPEEK/APK (40-200 mA/cm2)|voltage efficiency of SPTPC-2.59 (40-200 mA/cm2)|water uptake of PBI|water uptake of SNPBI-1.42|water uptake of SPEEK/APK|water uptake of SPTPC-2.59`
- relation_type: `COMPARISON`
- retrieval_score: `0.4375`
```text
Evidence 1
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARISON
Short claim: Under IEC of PBI = 0.0 mmol/g, IEC of SNPBI-1.42 = 1.42 mmol/g, IEC of SPEEK/APK = 1.26 mmol/g, IEC of SPTPC-2.59 = 2.59 mmol/g, area resistance of PBI = 2.45 ohm·cm², while area resistance of SNPBI-1.42 = 1.15 ohm·cm². Relation: COMPARISON.
Entities: ["PBI", "SNPBI-1.42", "SPEEK/APK", "SPTPC-2.59", "water uptake of PBI = 12 %", "water uptake of SNPBI-1.42 = 18 %", "water uptake of SPEEK/APK = 21 %", "water uptake of SPTPC-2.59 = 28 %", "IEC of PBI", "IEC of SNPBI-1.42", "IEC of SPEEK/APK", "IEC of SPTPC-2.59"]
Metrics: ["area resistance of PBI = 2.45 ohm·cm²", "area resistance of SNPBI-1.42 = 1.15 ohm·cm²", "area resistance of SPEEK/APK = 1.38 ohm·cm²", "area resistance of SPTPC-2.59 = 0.82 ohm·cm²", "coulombic efficiency of PBI (40-200 mA/cm2)", "coulombic efficiency of SNPBI-1.42 (40-200 mA/cm2)", "coulombic efficiency of SPEEK/APK (40-200 mA/cm2)", "coulombic efficiency of SPTPC-2.59 (40-200 mA/cm2)", "energy efficiency of PBI (40-200 mA/cm2)", "energy efficiency of SNPBI-1.42 (40-200 mA/cm2)", "energy efficiency of SPEEK/APK (40-200 mA/cm2)", "energy efficiency of SPTPC-2.59 (40-200 mA/cm2)"]
Values: ["IEC of PBI = 0.0 mmol/g", "IEC of SNPBI-1.42 = 1.42 mmol/g", "IEC of SPEEK/APK = 1.26 mmol/g", "IEC of SPTPC-2.59 = 2.59 mmol/g", "area resistance of PBI = 2.45 ohm·cm²", "area resistance of SNPBI-1.42 = 1.15 ohm·cm²", "area resistance of SPEEK/APK = 1.38 ohm·cm²", "area resistance of SPTPC-2.59 = 0.82 ohm·cm²", "vanadium permeability of PBI = 5e-08 cm²/s", "vanadium permeability of SNPBI-1.42
```
#### Evidence 2
- evidence_id: `Nafion 117|Nafion 212|area resistance (Nafion 117, 25°C)|area resistance (Nafion 212, 25°C)|capacity fade rate (Nafion 117)|capacity fade rate (Nafion 212)|coulombic efficiency (Nafion 117, 25°C)|coulombic efficiency (Nafion 212, 25°C)|energy efficiency (Nafion 117, 25°C)|energy efficiency (Nafion 212, 25°C)|ion exchange capacity (Nafion 117)|ion exchange capacity (Nafion 212)|thickness (Nafion 117)|thickness (Nafion 212)|vanadium permeability (Nafion 117)|vanadium permeability (Nafion 212)|voltage efficiency (Nafion 117, 25°C)|voltage efficiency (Nafion 212, 25°C)|water uptake (Nafion 117)|water uptake (Nafion 212)`
- relation_type: `COMPARISON`
- retrieval_score: `0.375`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under the reported conditions, area resistance (Nafion 117, 25°C) = 1.65 ohm cm2, while area resistance (Nafion 212, 25°C) = 0.85 ohm cm2. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "thickness (Nafion 117) = 183 um", "thickness (Nafion 212) = 50.8 um", "water uptake (Nafion 117) = 22 %", "water uptake (Nafion 212) = 25 %", "thickness (Nafion 117)", "thickness (Nafion 212)", "water uptake (Nafion 117)", "water uptake (Nafion 212)"]
Metrics: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2", "area resistance (Nafion 212, 25°C) = 0.85 ohm cm2", "capacity fade rate (Nafion 117) = 0.08 % per cycle", "capacity fade rate (Nafion 212) = 0.18 % per cycle", "coulombic efficiency (Nafion 117, 25°C)", "coulombic efficiency (Nafion 212, 25°C)", "energy efficiency (Nafion 117, 25°C)", "energy efficiency (Nafion 212, 25°C)", "ion exchange capacity (Nafion 117) = 0.91 mmol/g", "ion exchange capacity (Nafion 212) = 0.91 mmol/g", "vanadium permeability (Nafion 117) = 1.8e-07 cm2/s", "vanadium permeability (Nafion 212) = 3.9e-07 cm2/s"]
Values: ["area resistance (Nafion 117, 25°C) = 1.65 ohm cm2", "area resistance (Nafion 212, 25°C) = 0.85 ohm cm2", "capacity fade rate (Nafion 117) = 0.08 % per cycle", "capacity fade rate (Nafion 212) = 0.18 % per cycle", "ion exchange capacity (Nafion 117) = 0.91 mmol/g", "ion exchange capacity (Nafion 212) = 0.91 mmol/g", "thickness (Nafion 117) = 183 um", "thickness (Nafion 212) = 50.8 um", "vanadium permeability (Nafion 117) = 1.8e-07 cm2/s", "vanadium perm
```
#### Evidence 3
- evidence_id: `Carbon felt electrodes (SGL GFD 4.6 EA)|active electrode area|battery cycler|current density|electrode compression ratio|electrolyte volume|flow rate|lower cutoff voltage|negative electrolyte state of charge|operating temperature|peristaltic pumps|positive electrolyte state of charge|rest interval|single-cell VRFB|total sulfate concentration|total vanadium concentration|upper cutoff voltage|water bath thermostat`
- relation_type: `OPERATION`
- retrieval_score: `0.25`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under battery cycler, electrode compression ratio, negative electrolyte state of charge = 50 %, operating temperature, positive electrolyte state of charge = 50 %, total sulfate concentration = 4.5 M, total vanadium concentration = 1.6 M, negative electrolyte state of charge, positive electrolyte state of charge, total sulfate concentration, total vanadium concentration, Carbon felt electrodes (SGL GFD 4.6 EA), active electrode area, electrolyte volume, flow rate achieved/reported current density, lower cutoff voltage = 0.8 V, upper cutoff voltage = 1.65 V, lower cutoff voltage.
Entities: ["Carbon felt electrodes (SGL GFD 4.6 EA)", "active electrode area", "electrolyte volume", "flow rate", "peristaltic pumps", "rest interval = 2 min", "single-cell VRFB", "water bath thermostat", "rest interval"]
Metrics: ["current density", "lower cutoff voltage = 0.8 V", "upper cutoff voltage = 1.65 V", "lower cutoff voltage", "upper cutoff voltage"]
Values: ["lower cutoff voltage = 0.8 V", "negative electrolyte state of charge = 50 %", "positive electrolyte state of charge = 50 %", "rest interval = 2 min", "total sulfate concentration = 4.5 M", "total vanadium concentration = 1.6 M", "upper cutoff voltage = 1.65 V"]
Conditions: ["battery cycler", "electrode compression ratio", "negative electrolyte state of charge = 50 %", "operating temperature", "positive electrolyte state of charge = 50 %", "total sulfate concentration = 4.5 M", "total vanadium concentration = 1.6 M", "negative electr
```
#### Evidence 4
- evidence_id: `PBI|SNPBI-1.42`
- relation_type: `COMPARISON<SEP>COMPOSITION`
- retrieval_score: `0.25`
```text
Evidence 4
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARISON<SEP>COMPOSITION
Short claim: Evidence reports PBI, SNPBI-1.42. Conditions: not explicitly stated.
Entities: ["PBI", "SNPBI-1.42"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; SNPBI-1.42 Relation type: COMPARISON<SEP>COMPOSITION Readable labels: PBI; SNPBI-1.42 Description: PBI and SNPBI-1.42 compared on IEC, area resistance, vanadium permeability, water uptake, and efficiencies Source evidence: SNPBI-1.42 is derived from PBI by post-sulfonation using fuming and concentrated sulfuric acid ; PBI and SNPBI-1.42 compared on IEC, area resistance, vanadium permeability, water uptake, and efficiencies

```
#### Evidence 5
- evidence_id: `IEC loss|attack by V(V) on polymer backbone|capacity fade|desulfonation|mechanical degradation|phase separation under cycling|phosphoric acid leaching|polymer backbone degradation`
- relation_type: `DEGRADATION`
- retrieval_score: `0.25`
```text
Evidence 5
Source: chunk-hyperrag-DOC02
Relation/Type: DEGRADATION
Short claim: IEC loss, attack by V(V) on polymer backbone, desulfonation is linked to capacity fade. Conditions: phase separation under cycling, phosphoric acid leaching.
Entities: ["IEC loss", "attack by V(V) on polymer backbone", "desulfonation", "mechanical degradation", "polymer backbone degradation"]
Metrics: ["capacity fade"]
Values: []
Conditions: ["phase separation under cycling", "phosphoric acid leaching"]
Raw support excerpt: IEC loss; attack by V(V) on polymer backbone; capacity fade; desulfonation; mechanical degradation; phase separation under cycling; phosphoric acid leaching; polymer backbone degradation Relation type: DEGRADATION Readable labels: IEC loss; attack by V(V) on polymer backbone; capacity fade; desulfonation; mechanical degradation; phase separation under cycling; phosphoric acid leaching; polymer backbone degradation Description: Degradation chain in non-fluorinated membranes: V(V) attack leads to backbone degradation and desulfonation causing IEC loss and capacity fade; phosphoric acid leaching, mechanical degradation and phase separation also contribute Source evidence: The degradation of non-fluorinated VRFB membranes follows a chain process that initiates with chemical attack

```

## DOC02-QA-003 / chem_norm_hypergraph
- Category: `comparison`
- Answerable: `True`
- Question: Compare the vanadium permeability of all four non-fluorinated membranes tested in this study.
- Reference answer: PBI has the lowest vanadium permeability at 0.5 x 10^-7 cm2/s, followed by SNPBI-1.42 at 0.95 x 10^-7 cm2/s, then SPEEK/APK at 2.1 x 10^-7 cm2/s, and SPTPC-2.59 has the highest at 3.2 x 10^-7 cm2/s. The permeability increases with IEC, following a roughly linear relationship.
- Generated answer: SNPBI-1.42 exhibited the highest selectivity (lowest vanadium permeability) among the four non-fluorinated membranes (PBI, SNPBI-1.42, SPEEK/APK, SPTPC-2.59).
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `True` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["PBI: 0.5 x 10^-7 cm2/s", "SNPBI-1.42: 0.95 x 10^-7 cm2/s", "SPEEK/APK: 2.1 x 10^-7 cm2/s", "SPTPC-2.59: 3.2 x 10^-7 cm2/s", "Permeability increases with IEC"]`
- Unsupported claims found: `["SNPBI-1.42 exhibited the highest selectivity (lowest vanadium permeability) among the four non-fluorinated membranes"]`
- Rationale: The generated answer incorrectly states that SNPBI-1.42 has the lowest vanadium permeability, while the reference indicates it has the second lowest (0.95 x 10^-7 cm2/s) after PBI (0.5 x 10^-7 cm2/s). The answer does not provide any of the required key point values or the relationship with IEC, and it contradicts the reference. Therefore, the answer is hallucinated and poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `membrane:pbi|membrane:snpbi_1_42|membrane:speek_apk|membrane:sptpc_2_59|metric:membrane_selectivity`
- relation_type: `COMPARISON`
- retrieval_score: `0.5`
```text
Evidence 1
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARISON
Short claim: Evidence reports PBI, SNPBI-1.42, SPEEK/APK, SPTPC-2.59, membrane selectivity, membrane:pbi. Conditions: not explicitly stated.
Entities: ["PBI", "SNPBI-1.42", "SPEEK/APK", "SPTPC-2.59", "membrane selectivity", "membrane:pbi", "membrane:snpbi_1_42", "membrane:speek_apk", "membrane:sptpc_2_59", "metric:membrane_selectivity"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59; membrane selectivity Relation type: COMPARISON Readable labels: PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59; membrane selectivity Description: Comparison of membrane selectivity (proton conductivity/vanadium permeability) among four non-fluorinated membranes; SNPBI-1.42 exhibits highest selectivity. Source evidence: SNPBI-1.42 exhibited the highest selectivity among the tested non-fluorinated membranes, combining moderate proton conductivity with low vanadium permeability.

```
#### Evidence 2
- evidence_id: `condition:charge_cutoff_voltage|condition:current_density|condition:discharge_cutoff_voltage|condition:flow_rate|membrane:pbi|membrane:snpbi_1_42|membrane:speek_apk|membrane:sptpc_2_59|unresolved:single_cell_vrfb`
- relation_type: `OPERATION`
- retrieval_score: `0.4375`
```text
Evidence 2
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, flow rate, PBI, SNPBI-1.42, SPEEK/APK achieved/reported charge cutoff voltage, current density, discharge cutoff voltage, condition:charge_cutoff_voltage.
Entities: ["flow rate", "PBI", "SNPBI-1.42", "SPEEK/APK", "SPTPC-2.59", "single-cell VRFB", "condition:flow_rate", "membrane:pbi", "membrane:snpbi_1_42", "membrane:speek_apk", "membrane:sptpc_2_59", "unresolved:single_cell_vrfb"]
Metrics: ["charge cutoff voltage", "current density", "discharge cutoff voltage", "condition:charge_cutoff_voltage", "condition:current_density", "condition:discharge_cutoff_voltage"]
Values: []
Conditions: []
Raw support excerpt: charge cutoff voltage; current density; discharge cutoff voltage; flow rate; PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59; single-cell VRFB Relation type: OPERATION Readable labels: charge cutoff voltage; current density; discharge cutoff voltage; flow rate; PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59; single-cell VRFB Description: All four non-fluorinated membranes were tested in a single cell VRFB under identical conditions: current density range 40-200 mA/cm2, flow rate 40 mL/min, charge cutoff 1.65 V, discharge cutoff 0.8 V. Source evidence: Single cell VRFB tests were conducted using an active electrode area of 10 cm2 ...

```
#### Evidence 3
- evidence_id: `membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.3125`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Evidence reports Nafion 117, Nafion 212, membrane:nafion_117, membrane:nafion_212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212 Description: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures. Source evidence: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures.

```
#### Evidence 4
- evidence_id: `active_species:v_v|degradation:capacity_fading|degradation:chemical_attack_by_v_v_on_aromatic_backbone|degradation:desulfonation|degradation:loss_of_ion_exchange_capacity|degradation:vanadium_crossover`
- relation_type: `DEGRADATION`
- retrieval_score: `0.3125`
```text
Evidence 4
Source: chunk-hyperrag-DOC02
Relation/Type: DEGRADATION
Short claim: V(V), chemical attack by V(V) on aromatic backbone, desulfonation is linked to capacity fading, loss of ion exchange capacity, vanadium crossover. Conditions: not explicitly stated.
Entities: ["V(V)", "chemical attack by V(V) on aromatic backbone", "desulfonation", "active_species:v_v", "degradation:chemical_attack_by_v_v_on_aromatic_backbone", "degradation:desulfonation"]
Metrics: ["capacity fading", "loss of ion exchange capacity", "vanadium crossover", "degradation:capacity_fading", "degradation:loss_of_ion_exchange_capacity", "degradation:vanadium_crossover"]
Values: []
Conditions: []
Raw support excerpt: V(V); capacity fading; chemical attack by V(V) on aromatic backbone; desulfonation; loss of ion exchange capacity; vanadium crossover Relation type: DEGRADATION Readable labels: V(V); capacity fading; chemical attack by V(V) on aromatic backbone; desulfonation; loss of ion exchange capacity; vanadium crossover Description: Degradation chain in non-fluorinated membranes: V(V) attacks aromatic backbones, desulfonation reduces IEC, vanadium crossover causes capacity fade. Source evidence: The primary degradation mechanism involves attack by the strongly oxidizing V(V) species (VO2+) on the aromatic polymer backbone ... vanadium crossover leads to capacity fading.

```
#### Evidence 5
- evidence_id: `active_species:v_ii_v_iii|unresolved:vanadium`
- relation_type: `COMPOSITION`
- retrieval_score: `0.25`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: COMPOSITION
Short claim: Evidence reports V(II)/V(III), active_species:v_ii_v_iii, unresolved:vanadium. Conditions: vanadium = 1.6 mol/L.
Entities: ["V(II)/V(III)", "active_species:v_ii_v_iii", "unresolved:vanadium"]
Metrics: []
Values: ["vanadium = 1.6 mol/L"]
Conditions: ["vanadium = 1.6 mol/L"]
Raw support excerpt: V(II)/V(III); vanadium = 1.6 mol/L Relation type: COMPOSITION Readable labels: V(II)/V(III); vanadium = 1.6 mol/L Description: Negative electrolyte contains V(II)/V(III) as active species. Source evidence: Negative electrolyte contains V(II)/V(III) as active species.

```

## DOC01-QA-005 / text_segments
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of Nafion 212 at 80 mA/cm2 and 40 C?
- Reference answer: 83.8%
- Generated answer: 83.8%
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer exactly matches the reference answer (83.8%) and covers the required key point. It is concise, grounded, and contains no unsupported claims. The citation to 'Evidence 2' is assumed to support the value, so citation stability is high.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC10`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.75`
```text
Evidence 1
Source: DOC10
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: With Bi3+ additive (typically 0.01-0.05 M), ICRFBs achieve energy efficiency of 62-85% at current densities of 80-160 mA/cm2. Zinc-bromine systems achieve energy efficiency of 64-78% at current densities of 40-80 mA/cm2. A benchmark AEM (Fumatech FAP-450) achieved an EE of 79% at 100 mA/cm2 with iron-chromium electrolyte, compared to 82% for Nafion 117, but with significantly improved chromium retention (crossover rate reduced by 40%). The separator ASR is typically 1.5-2.5 ohm cm2, higher than Nafion but acceptable given the lower operating current densities (40-80 mA/cm2).

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.675`
```text
Evidence 2
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically varying current density from 40 to 200 mA/cm2 and operating temperature from 25 C to 40 C, we elucidate the fundamental trade-offs between coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) that govern membrane selection. #### 4.2.3 Energy Efficiency The energy efficiency of the Nafion 212 cell at 25 C ranged from 81.2% at 40 mA/cm2 to 79.7% at 200 mA/cm2, with a maximum of 82.5% observed at 80 mA/cm2. At 40 C, the Nafion 212 cell achieved EE values of 82.4% at 40 mA/cm2, 83.8% at 80 mA/cm2, 83.2% at 100 mA/cm2, 82.6% at 120 mA/cm2, 81.9% at 160 mA/cm2, and 80.9% at 200 mA/cm2. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.675`
```text
Evidence 3
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. ### 5.3 Resistance-EE and Permeability-EE Correlations Multiple linear regression analysis of the performance data reveals that energy efficiency at 100 mA/cm2 can be predicted from area resistance and vanadium permeability with good accuracy. Its balanced transport properties, combining moderate resistance (1.15 ohm cm2) with low vanadium permeability (0.95 x 10^-7 cm2/s), yield the highest energy efficiency (80.5% at 100 mA/cm2) and excellent coulombic efficiency that should translate to favorable long-term cycling stability. SNPBI-1.42 emerges as the most promising candidate, achieving an energy efficiency of 80.5% at 100 mA/cm2 through its optimal balance of low area resistance (1.15 ohm cm2) and low vanadium permeability (0.95 x 10^-7 cm2/s).

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC09`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.675`
```text
Evidence 4
Source: DOC09
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: At a current density of 100 mA/cm2, the cell achieved a CE of 96.8% and an EE of 80.2%. Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2: Nafion 117 (selectivity 88%, MV crossover 2.1 x 10^-6 cm2/s, capacity fade 0.055%/cycle), Nafion 212 (selectivity 85%, MV crossover 2.5 x 10^-6 cm2/s, capacity fade 0.065%/cycle), a sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation (selectivity 92%, MV crossover 1.2 x 10^-6 cm2/s, capacity fade 0.038%/cycle), a commercial anion exchange membrane (selectivity 90%, MV crossover 1.5 x 10^-6 cm2/s, capacity fade 0.042%/cycle), and a nanoporous size-exclusion membrane (selectivity 97%, MV crossover 0.3 x 10^-6 cm2/s, capacity fade 0.012%/cycle). However, this membrane also exhibited higher area-specific resistance (2.8 ohm cm2 compared to 1.8 ohm cm2 for Nafion 117), resulting in a lower EE of 78.5% compared to 80.2% for Nafion at 100 mA/cm2. Operating at reduced temperature (15 C rather than 25 C) reduced the capacity fade rate of a MV/TEMPO cell from 0.055%/cycle to 0.032%/cycle, albeit with some performance penalty due to increased electrolyte viscosity (EE decreased from 80.2% to 77.5% at 100 mA/cm2).

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC03`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.6`
```text
Evidence 5
Source: DOC03
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) were calculated from the measured capacity and voltage profiles. As current density increased to 200 mA/cm2, the performance gap between the modified and unmodified electrodes widened, with BMC-C maintaining substantially higher VE and EE values compared to C-C. Mild acid etching to produce MC-C substantially improved hydrophilicity (contact angle 102 deg), reduced charge-transfer resistance to 2.17 ohm cm2, and increased energy efficiency to 73.9%. The combined boron doping and thermal treatment to produce BMC-C achieved the optimal properties with contact angle of 92.8 deg, charge-transfer resistance of 1.34 ohm cm2, and energy efficiency of 82.5%.

```

## DOC01-QA-005 / original_hypergraph
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of Nafion 212 at 80 mA/cm2 and 40 C?
- Reference answer: 83.8%
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Nafion 212 EE at 80 mA/cm2 and 40 C is 83.8%"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer states 'I don't know based on the retrieved evidence' and provides no citations. Since the question is answerable and the reference answer is known, the model abstained from answering. This results in zero key point coverage and a POOR quality label, as the answer is not useful.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 212|area resistance of Nafion 212 at 40 C`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.5`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: ASSOCIATED_WITH
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported area resistance of Nafion 212 at 40 C = 0.68 ohm cm2, area resistance of Nafion 212 at 40 C.
Entities: ["Nafion 212"]
Metrics: ["area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "area resistance of Nafion 212 at 40 C"]
Values: ["area resistance of Nafion 212 at 40 C = 0.68 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 212; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2 Relation type: ASSOCIATED_WITH Readable labels: Nafion 212; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2 Description: Nafion 212 has area resistance of 0.68 ohm cm2 at 40 C. Source evidence: Nafion 212 has area resistance of 0.68 ohm cm2 at 40 C.

```
#### Evidence 2
- evidence_id: `Nafion 117|Nafion 212|area resistance of Nafion 117 at 25 C|area resistance of Nafion 117 at 40 C|area resistance of Nafion 212 at 25 C|area resistance of Nafion 212 at 40 C|temperature 40 C`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.485714`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under temperature 40 C = 40 C, temperature 40 C, area resistance of Nafion 117 at 25 C = 1.65 ohm cm2, while area resistance of Nafion 117 at 40 C = 1.32 ohm cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "area resistance of Nafion 117 at 25 C", "area resistance of Nafion 117 at 40 C", "area resistance of Nafion 212 at 25 C", "area resistance of Nafion 212 at 40 C"]
Values: ["area resistance of Nafion 117 at 25 C = 1.65 ohm cm2", "area resistance of Nafion 117 at 40 C = 1.32 ohm cm2", "area resistance of Nafion 212 at 25 C = 0.85 ohm cm2", "area resistance of Nafion 212 at 40 C = 0.68 ohm cm2", "temperature 40 C = 40 C"]
Conditions: ["temperature 40 C = 40 C", "temperature 40 C"]
Raw support excerpt: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2; temperature 40 C = 40 C Relation type: COMPARES_WITH Readable labels: Nafion 117; Nafion 212; area resistance of Nafion 117 at 25 C = 1.65 ohm cm2; area resistance of Nafion 117 at 40 C = 1.32 ohm cm2; area resistance of Nafion 212 at 25 C = 0.85 ohm cm2; area resistance of Nafion 212 at 40 C = 0.68 ohm cm2; te
```
#### Evidence 3
- evidence_id: `CE of Nafion 117 at 100 mA/cm2 and 25 C|CE of Nafion 212 at 100 mA/cm2 and 25 C|EE of Nafion 117 at 100 mA/cm2 and 25 C|EE of Nafion 212 at 100 mA/cm2 and 25 C|Nafion 117|Nafion 212|VE of Nafion 117 at 100 mA/cm2 and 25 C|VE of Nafion 212 at 100 mA/cm2 and 25 C|current density of 100 mA/cm2|temperature 25 C`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.475`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARES_WITH
Short claim: Under CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %, CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %, EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %, EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %, VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %, VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %, temperature 25 C = 25 C, CE of Nafion 117 at 100 mA/cm2 and 25 C, CE of Nafion 212 at 100 mA/cm2 and 25 C, EE of Nafion 117 at 100 mA/cm2 and 25 C, EE of Nafion 212 at 100 mA/cm2 and 25 C, VE of Nafion 117 at 100 mA/cm2 and 25 C, current density of 100 mA/cm2 = 100 mA/cm2, while current density of 100 mA/cm2. Relation: COMPARES_WITH.
Entities: ["Nafion 117", "Nafion 212"]
Metrics: ["current density of 100 mA/cm2 = 100 mA/cm2", "current density of 100 mA/cm2"]
Values: ["CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %", "CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %", "EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %", "VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %", "current density of 100 mA/cm2 = 100 mA/cm2", "temperature 25 C = 25 C"]
Conditions: ["CE of Nafion 117 at 100 mA/cm2 and 25 C = 97.1 %", "CE of Nafion 212 at 100 mA/cm2 and 25 C = 93.8 %", "EE of Nafion 117 at 100 mA/cm2 and 25 C = 80.2 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "VE of Nafion 117 at 100 mA/cm2 and 25 C = 82.6 %", "VE of Nafion 212 at 100 mA/cm2 and 25 C = 86.2 %", "temperature 25 C = 25 C", "C
```
#### Evidence 4
- evidence_id: `EE of Nafion 212 at 100 mA/cm2 and 25 C|current density of 100 mA/cm2`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.45`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: ASSOCIATED_WITH
Short claim: In the reported system, under EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %, EE of Nafion 212 at 100 mA/cm2 and 25 C, the entity achieved/reported current density of 100 mA/cm2 = 100 mA/cm2, current density of 100 mA/cm2.
Entities: []
Metrics: ["current density of 100 mA/cm2 = 100 mA/cm2", "current density of 100 mA/cm2"]
Values: ["EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "current density of 100 mA/cm2 = 100 mA/cm2"]
Conditions: ["EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "EE of Nafion 212 at 100 mA/cm2 and 25 C"]
Raw support excerpt: EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %; current density of 100 mA/cm2 = 100 mA/cm2 Relation type: ASSOCIATED_WITH Readable labels: EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %; current density of 100 mA/cm2 = 100 mA/cm2 Description: At 100 mA/cm2 and 25 C, Nafion 212 EE is 80.9%. Source evidence: At 100 mA/cm2 and 25 C, Nafion 212 EE is 80.9%.

```
#### Evidence 5
- evidence_id: `EE of Nafion 212 at 100 mA/cm2 and 25 C|temperature 25 C`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.45`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: ASSOCIATED_WITH
Short claim: Evidence reports ASSOCIATED_WITH. Conditions: EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %, temperature 25 C = 25 C, EE of Nafion 212 at 100 mA/cm2 and 25 C, temperature 25 C.
Entities: []
Metrics: []
Values: ["EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "temperature 25 C = 25 C"]
Conditions: ["EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %", "temperature 25 C = 25 C", "EE of Nafion 212 at 100 mA/cm2 and 25 C", "temperature 25 C"]
Raw support excerpt: EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %; temperature 25 C = 25 C Relation type: ASSOCIATED_WITH Readable labels: EE of Nafion 212 at 100 mA/cm2 and 25 C = 80.9 %; temperature 25 C = 25 C Description: Temperature 25 C is the condition for this EE measurement. Source evidence: Temperature 25 C is the condition for this EE measurement.

```

## DOC01-QA-005 / chem_prompt_graph
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of Nafion 212 at 80 mA/cm2 and 40 C?
- Reference answer: 83.8%
- Generated answer: The energy efficiency of Nafion 212 at 40°C ranges 80.9-83.8%. However, the retrieved evidence does not specify the current density (80 mA/cm²) for this value.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `True` | Abstained: `False` | Abstention correct: `True`
- Missing key points: `["Nafion 212 EE at 80 mA/cm2 and 40 C is 83.8%"]`
- Unsupported claims found: `["The retrieved evidence does not specify the current density (80 mA/cm²) for this value."]`
- Rationale: The generated answer does not provide the exact energy efficiency value of 83.8% as required; instead it gives a range and claims the evidence lacks current density specification, which conflicts with the reference answer. The answer is incomplete and contains an unsupported claim about the evidence, making it poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 212|energy efficiency (Nafion 212, 40°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.65`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported energy efficiency (Nafion 212, 40°C).
Entities: ["Nafion 212"]
Metrics: ["energy efficiency (Nafion 212, 40°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 212; energy efficiency (Nafion 212, 40°C) Relation type: OPERATION Readable labels: Nafion 212; energy efficiency (Nafion 212, 40°C) Description: Energy efficiency of Nafion 212 at 40°C ranges 80.9-83.8% Source evidence: Energy efficiency of Nafion 212 at 40°C ranges 80.9-83.8%

```
#### Evidence 2
- evidence_id: `Nafion 212|area resistance (Nafion 212, 40°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported area resistance (Nafion 212, 40°C) = 0.68 ohm cm2, area resistance (Nafion 212, 40°C).
Entities: ["Nafion 212"]
Metrics: ["area resistance (Nafion 212, 40°C) = 0.68 ohm cm2", "area resistance (Nafion 212, 40°C)"]
Values: ["area resistance (Nafion 212, 40°C) = 0.68 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 212; area resistance (Nafion 212, 40°C) = 0.68 ohm cm2 Relation type: OPERATION Readable labels: Nafion 212; area resistance (Nafion 212, 40°C) = 0.68 ohm cm2 Description: Area resistance of Nafion 212 at 40°C is 0.68 ohm cm2 Source evidence: Area resistance of Nafion 212 at 40°C is 0.68 ohm cm2

```
#### Evidence 3
- evidence_id: `Nafion 212|energy efficiency (Nafion 212, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported energy efficiency (Nafion 212, 25°C).
Entities: ["Nafion 212"]
Metrics: ["energy efficiency (Nafion 212, 25°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 212; energy efficiency (Nafion 212, 25°C) Relation type: OPERATION Readable labels: Nafion 212; energy efficiency (Nafion 212, 25°C) Description: Energy efficiency of Nafion 212 at 25°C ranges 79.7-82.5% Source evidence: Energy efficiency of Nafion 212 at 25°C ranges 79.7-82.5%

```
#### Evidence 4
- evidence_id: `Nafion 212|voltage efficiency (Nafion 212, 40°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported voltage efficiency (Nafion 212, 40°C).
Entities: ["Nafion 212"]
Metrics: ["voltage efficiency (Nafion 212, 40°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 212; voltage efficiency (Nafion 212, 40°C) Relation type: OPERATION Readable labels: Nafion 212; voltage efficiency (Nafion 212, 40°C) Description: Voltage efficiency of Nafion 212 at 40°C ranges 84.8-89.5% Source evidence: Voltage efficiency of Nafion 212 at 40°C ranges 84.8-89.5%

```
#### Evidence 5
- evidence_id: `Nafion 212|thickness (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.425`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 212, thickness (Nafion 212) = 50.8 um, thickness (Nafion 212). Conditions: not explicitly stated.
Entities: ["Nafion 212", "thickness (Nafion 212) = 50.8 um", "thickness (Nafion 212)"]
Metrics: []
Values: ["thickness (Nafion 212) = 50.8 um"]
Conditions: []
Raw support excerpt: Nafion 212; thickness (Nafion 212) = 50.8 um Relation type: OPERATION Readable labels: Nafion 212; thickness (Nafion 212) = 50.8 um Description: Measured thickness of Nafion 212 is 50.8 um Source evidence: Measured thickness of Nafion 212 is 50.8 um

```

## DOC01-QA-005 / chem_prompt_hypergraph
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of Nafion 212 at 80 mA/cm2 and 40 C?
- Reference answer: 83.8%
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Nafion 212 EE at 80 mA/cm2 and 40 C is 83.8%"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer states 'I don't know based on the retrieved evidence' and provides no citations. Since the question is answerable and the reference answer is known, the model abstained from answering, which is not acceptable for a correct response. The answer fails to provide the required key point, resulting in zero coverage. No hallucination is present, but the answer is not useful.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 212|energy efficiency (Nafion 212, 40°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.65`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported energy efficiency (Nafion 212, 40°C).
Entities: ["Nafion 212"]
Metrics: ["energy efficiency (Nafion 212, 40°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 212; energy efficiency (Nafion 212, 40°C) Relation type: OPERATION Readable labels: Nafion 212; energy efficiency (Nafion 212, 40°C) Description: Energy efficiency of Nafion 212 at 40°C ranges 80.9-83.8% Source evidence: Energy efficiency of Nafion 212 at 40°C ranges 80.9-83.8%

```
#### Evidence 2
- evidence_id: `Coulombic efficiency with Bi3+ at 120 mA/cm²|Coulombic efficiency with Bi3+ at 160 mA/cm²|Coulombic efficiency with Bi3+ at 40 mA/cm²|Coulombic efficiency with Bi3+ at 80 mA/cm²|Energy efficiency with Bi3+ at 120 mA/cm²|Energy efficiency with Bi3+ at 160 mA/cm²|Energy efficiency with Bi3+ at 40 mA/cm²|Energy efficiency with Bi3+ at 80 mA/cm²`
- relation_type: `COMPARISON`
- retrieval_score: `0.525`
```text
Evidence 2
Source: chunk-hyperrag-DOC06
Relation/Type: COMPARISON
Short claim: Under the reported conditions, Coulombic efficiency with Bi3+ at 120 mA/cm², while Coulombic efficiency with Bi3+ at 160 mA/cm². Relation: COMPARISON.
Entities: []
Metrics: ["Coulombic efficiency with Bi3+ at 120 mA/cm²", "Coulombic efficiency with Bi3+ at 160 mA/cm²", "Coulombic efficiency with Bi3+ at 40 mA/cm²", "Coulombic efficiency with Bi3+ at 80 mA/cm²", "Energy efficiency with Bi3+ at 120 mA/cm²", "Energy efficiency with Bi3+ at 160 mA/cm²", "Energy efficiency with Bi3+ at 40 mA/cm²", "Energy efficiency with Bi3+ at 80 mA/cm²"]
Values: []
Conditions: []
Raw support excerpt: Coulombic efficiency with Bi3+ at 120 mA/cm²; Coulombic efficiency with Bi3+ at 160 mA/cm²; Coulombic efficiency with Bi3+ at 40 mA/cm²; Coulombic efficiency with Bi3+ at 80 mA/cm²; Energy efficiency with Bi3+ at 120 mA/cm²; Energy efficiency with Bi3+ at 160 mA/cm²; Energy efficiency with Bi3+ at 40 mA/cm²; Energy efficiency with Bi3+ at 80 mA/cm² Relation type: COMPARISON Readable labels: Coulombic efficiency with Bi3+ at 120 mA/cm²; Coulombic efficiency with Bi3+ at 160 mA/cm²; Coulombic efficiency with Bi3+ at 40 mA/cm²; Coulombic efficiency with Bi3+ at 80 mA/cm²; Energy efficiency with Bi3+ at 120 mA/cm²; Energy efficiency with Bi3+ at 160 mA/cm²; Energy efficiency with Bi3+ at 40 mA/cm²; Energy efficiency with Bi3+ at 80 mA/cm² Description: ICRFB performance with Bi3+ additive at current densities 40-160 mA/cm² (1.5-5.0 mmol/L): CE and EE are significantly higher than baseline, enabling operation up to 160 mA/cm
```
#### Evidence 3
- evidence_id: `Nafion 212|area resistance (Nafion 212, 40°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported area resistance (Nafion 212, 40°C) = 0.68 ohm cm2, area resistance (Nafion 212, 40°C).
Entities: ["Nafion 212"]
Metrics: ["area resistance (Nafion 212, 40°C) = 0.68 ohm cm2", "area resistance (Nafion 212, 40°C)"]
Values: ["area resistance (Nafion 212, 40°C) = 0.68 ohm cm2"]
Conditions: []
Raw support excerpt: Nafion 212; area resistance (Nafion 212, 40°C) = 0.68 ohm cm2 Relation type: OPERATION Readable labels: Nafion 212; area resistance (Nafion 212, 40°C) = 0.68 ohm cm2 Description: Area resistance of Nafion 212 at 40°C is 0.68 ohm cm2 Source evidence: Area resistance of Nafion 212 at 40°C is 0.68 ohm cm2

```
#### Evidence 4
- evidence_id: `Nafion 212|energy efficiency (Nafion 212, 25°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported energy efficiency (Nafion 212, 25°C).
Entities: ["Nafion 212"]
Metrics: ["energy efficiency (Nafion 212, 25°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 212; energy efficiency (Nafion 212, 25°C) Relation type: OPERATION Readable labels: Nafion 212; energy efficiency (Nafion 212, 25°C) Description: Energy efficiency of Nafion 212 at 25°C ranges 79.7-82.5% Source evidence: Energy efficiency of Nafion 212 at 25°C ranges 79.7-82.5%

```
#### Evidence 5
- evidence_id: `Nafion 212|voltage efficiency (Nafion 212, 40°C)`
- relation_type: `OPERATION`
- retrieval_score: `0.5`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212 achieved/reported voltage efficiency (Nafion 212, 40°C).
Entities: ["Nafion 212"]
Metrics: ["voltage efficiency (Nafion 212, 40°C)"]
Values: []
Conditions: []
Raw support excerpt: Nafion 212; voltage efficiency (Nafion 212, 40°C) Relation type: OPERATION Readable labels: Nafion 212; voltage efficiency (Nafion 212, 40°C) Description: Voltage efficiency of Nafion 212 at 40°C ranges 84.8-89.5% Source evidence: Voltage efficiency of Nafion 212 at 40°C ranges 84.8-89.5%

```

## DOC01-QA-005 / chem_norm_hypergraph
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of Nafion 212 at 80 mA/cm2 and 40 C?
- Reference answer: 83.8%
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["Nafion 212 EE at 80 mA/cm2 and 40 C is 83.8%"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer abstains by stating 'I don't know based on the retrieved evidence.' The question is answerable (True) and the reference answer is 83.8%. The answer does not provide the required key point, so it is not useful. It does not contain any unsupported claims, but it fails to answer the question. Therefore, the quality is poor.

### Evidence Blocks
#### Evidence 1
- evidence_id: `condition:current_density|condition:temperature|membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.7375`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under temperature, condition:temperature, current density, while condition:current_density. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: ["temperature", "condition:temperature"]
Raw support excerpt: current density; temperature; Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: current density; temperature; Nafion 117; Nafion 212 Description: Comprehensive comparison of Nafion 117 and Nafion 212 membranes across current densities (40-200 mA/cm2) and temperatures (25-40 C) for coulombic, voltage, and energy efficiency. Source evidence: At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%.

```
#### Evidence 2
- evidence_id: `membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.5`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Evidence reports Nafion 117, Nafion 212, membrane:nafion_117, membrane:nafion_212. Conditions: not explicitly stated.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: Nafion 117; Nafion 212 Description: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures. Source evidence: Compared in terms of thickness, area resistance, vanadium permeability, water uptake, ion exchange capacity, and efficiency metrics (CE, VE, EE) across current densities and temperatures.

```
#### Evidence 3
- evidence_id: `condition:bi3_concentration|condition:current_density|metric:ce|metric:ve`
- relation_type: `COMPARISON`
- retrieval_score: `0.45`
```text
Evidence 3
Source: chunk-hyperrag-DOC06
Relation/Type: COMPARISON
Short claim: Under Bi3+ concentration, current density, while coulombic efficiency = 93 %. Relation: COMPARISON.
Entities: ["condition:bi3_concentration", "metric:ce", "metric:ve"]
Metrics: ["current density", "coulombic efficiency = 93 %", "voltage efficiency", "condition:current_density"]
Values: ["coulombic efficiency = 93 %"]
Conditions: ["Bi3+ concentration"]
Raw support excerpt: Bi3+ concentration; current density; coulombic efficiency = 93 %; voltage efficiency Relation type: COMPARISON Readable labels: Bi3+ concentration; current density; coulombic efficiency = 93 %; voltage efficiency Description: Comparison of efficiencies at different Bi3+ concentrations (0.5-5.0 mmol/L) and current densities (40-160 mA/cm2); baseline without Bi3+ yields lower values Source evidence: With Bi3+ addition, Coulombic efficiency improved to the range of 87-96% and energy efficiency reached 62-85%

```
#### Evidence 4
- evidence_id: `condition:current_density|membrane:nafion_212`
- relation_type: `OPERATION`
- retrieval_score: `0.425`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, Nafion 212, membrane:nafion_212 achieved/reported current density, condition:current_density.
Entities: ["Nafion 212", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: []
Raw support excerpt: current density; Nafion 212 Relation type: OPERATION Readable labels: current density; Nafion 212 Description: Nafion 212 tested at current densities from 40 to 200 mA/cm2. Source evidence: Nafion 212 tested at current densities from 40 to 200 mA/cm2.

```
#### Evidence 5
- evidence_id: `condition:active_area|condition:charge_cutoff_voltage|condition:current_density|condition:discharge_cutoff_voltage|condition:electrolyte_volume|condition:flow_rate|electrode:bmc_c|electrode:c_c|electrode:mc_c|membrane:nafion_117|system:battery_cycler|system:peristaltic_pumps`
- relation_type: `OPERATION`
- retrieval_score: `0.375`
```text
Evidence 5
Source: chunk-hyperrag-DOC03
Relation/Type: OPERATION
Short claim: In the reported system, under active area = 10 cm², battery cycler, system:battery_cycler, electrolyte volume, flow rate, BMC-C, C-C achieved/reported charge cutoff voltage, current density, discharge cutoff voltage, condition:charge_cutoff_voltage.
Entities: ["electrolyte volume", "flow rate", "BMC-C", "C-C", "MC-C", "Nafion 117", "peristaltic pumps", "condition:active_area", "condition:electrolyte_volume", "condition:flow_rate", "electrode:bmc_c", "electrode:c_c"]
Metrics: ["charge cutoff voltage", "current density", "discharge cutoff voltage", "condition:charge_cutoff_voltage", "condition:current_density", "condition:discharge_cutoff_voltage"]
Values: ["active area = 10 cm²"]
Conditions: ["active area = 10 cm²", "battery cycler", "system:battery_cycler"]
Raw support excerpt: active area = 10 cm²; charge cutoff voltage; current density; discharge cutoff voltage; electrolyte volume; flow rate; BMC-C; C-C; MC-C; Nafion 117; battery cycler; peristaltic pumps Relation type: OPERATION Readable labels: active area = 10 cm²; charge cutoff voltage; current density; discharge cutoff voltage; electrolyte volume; flow rate; BMC-C; C-C; MC-C; Nafion 117; battery cycler; peristaltic pumps Description: Single-cell VRFB tests with Nafion 117, 10 cm2 active area, 40 mL electrolyte, 40 mL/min flow, peristaltic pumps, battery cycler, voltage cutoffs 1.65V/0.8V, current densities 50-500 mA/cm2. Source evidence: Single-cell VRFB tests were performed with an active area of 10 cm2. 40 mL electrolyte circulated at 40 
```

## DOC02-QA-004 / text_segments
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of SNPBI-1.42 at 100 mA/cm2, and how does it compare to SPTPC-2.59 at the same current density?
- Reference answer: SNPBI-1.42 achieves EE of 80.5% at 100 mA/cm2 (CE 98.1%, VE 82.1%), while SPTPC-2.59 achieves EE of 81.4% at 100 mA/cm2 (CE 96.3%, VE 83.8%). Although SPTPC-2.59 has a slightly higher EE, SNPBI-1.42 achieves its EE through higher CE and lower vanadium permeability, suggesting better long-term cycling stability.
- Generated answer: SNPBI-1.42 achieves an energy efficiency of 80.5% at 100 mA/cm2. The energy efficiency of SPTPC-2.59 at 100 mA/cm2 is not provided in the retrieved evidence, so a comparison cannot be made.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `["SNPBI-1.42 EE: 80.5% (CE 98.1%, VE 82.1%)", "SPTPC-2.59 EE: 81.4% (CE 96.3%, VE 83.8%)", "SPTPC-2.59 has slightly higher EE", "SNPBI-1.42 has higher CE suggesting better cycle stability"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer incorrectly states that the energy efficiency of SPTPC-2.59 is not provided, and therefore refuses to compare. However, the reference answer clearly provides both values and a comparison. The answer abstains from answering a fully answerable question, failing to cover any required key points. It does not hallucinate false information, but it is not useful.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.617647`
```text
Evidence 1
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. ### 5.3 Resistance-EE and Permeability-EE Correlations Multiple linear regression analysis of the performance data reveals that energy efficiency at 100 mA/cm2 can be predicted from area resistance and vanadium permeability with good accuracy. For applications prioritizing maximum voltage efficiency and power density, particularly at high current densities, SPTPC-2.59 offers advantages through its very low resistance (0.82 ohm cm2). SNPBI-1.42 emerges as the most promising candidate, achieving an energy efficiency of 80.5% at 100 mA/cm2 through its optimal balance of low area resistance (1.15 ohm cm2) and low vanadium permeability (0.95 x 10^-7 cm2/s).

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC06`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.617647`
```text
Evidence 2
Source: DOC06
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: With Bi3+ addition, Coulombic efficiency improved to the range of 87-96% and energy efficiency reached 62-85% depending on the specific concentration and current density. The work addresses three primary objectives: (1) quantifying the kinetic enhancement of the Cr(III)/Cr(II) redox reaction in the presence of Bi3+, (2) characterizing the suppression of parasitic hydrogen evolution achieved through Bi3+ addition, and (3) establishing the relationship between Bi3+ concentration, operational current density, and full-cell performance metrics including Coulombic efficiency, voltage efficiency, and energy efficiency. At a current density of 40 mA/cm2, the cell achieved a Coulombic efficiency of 85%, a voltage efficiency of 68%, and an energy efficiency of 58%. The principal findings are as follows: The addition of Bi3+ at concentrations of 0.5-5.0 mmol/L to the negative electrolyte substantially improves both Coulombic efficiency and energy efficiency across the operational current density range of 40-160 mA/cm2.

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.573529`
```text
Evidence 3
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically varying current density from 40 to 200 mA/cm2 and operating temperature from 25 C to 40 C, we elucidate the fundamental trade-offs between coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) that govern membrane selection. The approximately 3-4 percentage point gap between Nafion 212 and Nafion 117 CE values at any given current density directly reflects the twofold difference in vanadium permeability between the two membranes. For Nafion 117, the EE decreased monotonically with increasing current density at both temperatures, indicating that maximum energy efficiency is achieved at the lowest practical current density. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC03`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.573529`
```text
Evidence 4
Source: DOC03
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: 3.4 Voltage Efficiency and Energy Efficiency Voltage efficiency measurements at 100 mA/cm2 showed marked differences among the three electrode configurations. As current density increased to 200 mA/cm2, the performance gap between the modified and unmodified electrodes widened, with BMC-C maintaining substantially higher VE and EE values compared to C-C. For high-efficiency applications, the BMC-C electrode provides state-of-the-art performance with 82.5% EE at 100 mA/cm2, though the additional boron doping and thermal treatment steps increase manufacturing complexity. The untreated C-C electrode exhibited hydrophobic characteristics with a contact angle of 130.4 deg, high charge-transfer resistance of 3.82 ohm cm2, and moderate energy efficiency of 65.8% at 100 mA/cm2.

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC05`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.573529`
```text
Evidence 5
Source: DOC05
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a comprehensive experimental investigation into the temperature-dependent behavior of VRFB cells operated at 25 C, 40 C, and 60 C over 500 charge-discharge cycles at a constant current density of 80 mA/cm2. The results demonstrate that elevated temperatures accelerate vanadium ion crossover through the ion-exchange membrane, exacerbate state-of-charge (SOC) imbalance between the positive and negative half-cells, and precipitate more rapid capacity fading. The precipitation of V(V) species as V2O5 at the positive electrode, particularly when local temperatures exceed solubility limits, introduces additional capacity loss mechanisms that may be partially irreversible. By maintaining all other operational parameters constant-including current density at 80 mA/cm2, electrolyte composition at 1.5 M VOSO4 in 3.0 M H2SO4, and electrolyte flow rate at 40 mL/min-we establish a controlled experimental framework wherein observed differences in performance can be confidently attributed to temperature effects.

```

## DOC02-QA-004 / original_hypergraph
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of SNPBI-1.42 at 100 mA/cm2, and how does it compare to SPTPC-2.59 at the same current density?
- Reference answer: SNPBI-1.42 achieves EE of 80.5% at 100 mA/cm2 (CE 98.1%, VE 82.1%), while SPTPC-2.59 achieves EE of 81.4% at 100 mA/cm2 (CE 96.3%, VE 83.8%). Although SPTPC-2.59 has a slightly higher EE, SNPBI-1.42 achieves its EE through higher CE and lower vanadium permeability, suggesting better long-term cycling stability.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["SNPBI-1.42 EE: 80.5% (CE 98.1%, VE 82.1%)", "SPTPC-2.59 EE: 81.4% (CE 96.3%, VE 83.8%)", "SPTPC-2.59 has slightly higher EE", "SNPBI-1.42 has higher CE suggesting better cycle stability"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer states 'I don't know based on the retrieved evidence' and provides no citations, which is an abstention. Since the question is answerable and the reference answer provides the required information, the abstention is inappropriate. The answer covers none of the required key points, so key_point_coverage is 0.0. There are no hallucinations or unsupported claims. The answer is not useful and does not meet the criteria for satisfactory_or_better.

### Evidence Blocks
#### Evidence 1
- evidence_id: `PBI|SNPBI-1.42`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.514706`
```text
Evidence 1
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARES_WITH
Short claim: Evidence reports PBI, SNPBI-1.42. Conditions: not explicitly stated.
Entities: ["PBI", "SNPBI-1.42"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; SNPBI-1.42 Relation type: COMPARES_WITH Readable labels: PBI; SNPBI-1.42 Description: PBI and SNPBI-1.42 are compared in terms of IEC, resistance, permeability, and efficiency. Source evidence: PBI and SNPBI-1.42 are compared in terms of IEC, resistance, permeability, and efficiency.

```
#### Evidence 2
- evidence_id: `PBI|SNPBI-1.42|SPEEK/APK|SPTPC-2.59`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.496324`
```text
Evidence 2
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARES_WITH
Short claim: Evidence reports PBI, SNPBI-1.42, SPEEK/APK, SPTPC-2.59. Conditions: not explicitly stated.
Entities: ["PBI", "SNPBI-1.42", "SPEEK/APK", "SPTPC-2.59"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59 Relation type: COMPARES_WITH Readable labels: PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59 Description: Four non-fluorinated membrane systems are systematically evaluated for VRFB performance, comparing their IEC, resistance, permeability, and efficiency. Source evidence: This study presents a comprehensive evaluation of four non-fluorinated membrane systems for VRFB applications

```
#### Evidence 3
- evidence_id: `Coulombic efficiency (CE)|baseline cell (without Bi3+)|current density|energy efficiency (EE)|iron-chromium redox flow battery (ICRFB)|voltage efficiency (VE)`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.482843`
```text
Evidence 3
Source: chunk-hyperrag-DOC06
Relation/Type: COMPARES_WITH
Short claim: Under baseline cell (without Bi3+), Coulombic efficiency (CE), while current density. Relation: COMPARES_WITH.
Entities: ["iron-chromium redox flow battery (ICRFB)"]
Metrics: ["Coulombic efficiency (CE)", "current density", "energy efficiency (EE)", "voltage efficiency (VE)"]
Values: []
Conditions: ["baseline cell (without Bi3+)"]
Raw support excerpt: Coulombic efficiency (CE); baseline cell (without Bi3+); current density; energy efficiency (EE); iron-chromium redox flow battery (ICRFB); voltage efficiency (VE) Relation type: COMPARES_WITH Readable labels: Coulombic efficiency (CE); baseline cell (without Bi3+); current density; energy efficiency (EE); iron-chromium redox flow battery (ICRFB); voltage efficiency (VE) Description: Baseline cell without Bi3+ shows lower CE, EE, and VE across all current densities compared to cells with Bi3+ additive. Source evidence: Without Bi3+, baseline cell exhibited CE of 72% and EE of 51% at 80 mA/cm2

```
#### Evidence 4
- evidence_id: `current density|energy efficiency`
- relation_type: `CAUSES_OR_AFFECTS`
- retrieval_score: `0.470588`
```text
Evidence 4
Source: chunk-hyperrag-DOC08
Relation/Type: CAUSES_OR_AFFECTS
Short claim: The reported factor is linked to current density, energy efficiency. Conditions: not explicitly stated.
Entities: []
Metrics: ["current density", "energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: current density; energy efficiency Relation type: CAUSES_OR_AFFECTS Readable labels: current density; energy efficiency Description: Higher current density decreases energy efficiency Source evidence: Higher current density decreases energy efficiency

```
#### Evidence 5
- evidence_id: `All-Vanadium Redox Flow Battery (VRFB)|Iron-Chromium Redox Flow Battery (ICRFB)|Organic Redox Flow Battery (ORFB)|Soluble Lead-Acid Flow Battery (SLA)|Zinc-Bromine Flow Battery (Zn-Br)`
- relation_type: `COMPARES_WITH`
- retrieval_score: `0.441176`
```text
Evidence 5
Source: chunk-hyperrag-DOC10
Relation/Type: COMPARES_WITH
Short claim: Evidence reports All-Vanadium Redox Flow Battery (VRFB), Iron-Chromium Redox Flow Battery (ICRFB), Organic Redox Flow Battery (ORFB), Soluble Lead-Acid Flow Battery (SLA), Zinc-Bromine Flow Battery (Zn-Br). Conditions: not explicitly stated.
Entities: ["All-Vanadium Redox Flow Battery (VRFB)", "Iron-Chromium Redox Flow Battery (ICRFB)", "Organic Redox Flow Battery (ORFB)", "Soluble Lead-Acid Flow Battery (SLA)", "Zinc-Bromine Flow Battery (Zn-Br)"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: All-Vanadium Redox Flow Battery (VRFB); Iron-Chromium Redox Flow Battery (ICRFB); Organic Redox Flow Battery (ORFB); Soluble Lead-Acid Flow Battery (SLA); Zinc-Bromine Flow Battery (Zn-Br) Relation type: COMPARES_WITH Readable labels: All-Vanadium Redox Flow Battery (VRFB); Iron-Chromium Redox Flow Battery (ICRFB); Organic Redox Flow Battery (ORFB); Soluble Lead-Acid Flow Battery (SLA); Zinc-Bromine Flow Battery (Zn-Br) Description: Cross-system comparison of energy efficiency and capacity fade at matched current densities: ORFB and VRFB lead in EE, depositing systems show lower EE but cost advantages. Source evidence: At 100 mA/cm2, the EE ranking is: ORFB 80-83% > VRFB 81-84% > ICRFB with Bi3+ 75-82% > Zn-Br...

```

## DOC02-QA-004 / chem_prompt_graph
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of SNPBI-1.42 at 100 mA/cm2, and how does it compare to SPTPC-2.59 at the same current density?
- Reference answer: SNPBI-1.42 achieves EE of 80.5% at 100 mA/cm2 (CE 98.1%, VE 82.1%), while SPTPC-2.59 achieves EE of 81.4% at 100 mA/cm2 (CE 96.3%, VE 83.8%). Although SPTPC-2.59 has a slightly higher EE, SNPBI-1.42 achieves its EE through higher CE and lower vanadium permeability, suggesting better long-term cycling stability.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["SNPBI-1.42 EE: 80.5% (CE 98.1%, VE 82.1%)", "SPTPC-2.59 EE: 81.4% (CE 96.3%, VE 83.8%)", "SPTPC-2.59 has slightly higher EE", "SNPBI-1.42 has higher CE suggesting better cycle stability"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer abstains from answering, providing no information. It does not cover any required key points and is not useful.

### Evidence Blocks
#### Evidence 1
- evidence_id: `current density|gross energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.433824`
```text
Evidence 1
Source: chunk-hyperrag-DOC04
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, gross energy efficiency.
Entities: []
Metrics: ["current density", "gross energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: current density; gross energy efficiency Relation type: OPERATION Readable labels: current density; gross energy efficiency Description: Higher current density reduces gross EE due to increased overpotential; 50 mA/cm² gives highest values Source evidence: Higher current density reduces gross EE due to increased overpotential; 50 mA/cm² gives highest values

```
#### Evidence 2
- evidence_id: `PBI|SNPBI-1.42`
- relation_type: `COMPARISON<SEP>COMPOSITION`
- retrieval_score: `0.426471`
```text
Evidence 2
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARISON<SEP>COMPOSITION
Short claim: Evidence reports PBI, SNPBI-1.42. Conditions: not explicitly stated.
Entities: ["PBI", "SNPBI-1.42"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; SNPBI-1.42 Relation type: COMPARISON<SEP>COMPOSITION Readable labels: PBI; SNPBI-1.42 Description: PBI and SNPBI-1.42 compared on IEC, area resistance, vanadium permeability, water uptake, and efficiencies Source evidence: SNPBI-1.42 is derived from PBI by post-sulfonation using fuming and concentrated sulfuric acid ; PBI and SNPBI-1.42 compared on IEC, area resistance, vanadium permeability, water uptake, and efficiencies

```
#### Evidence 3
- evidence_id: `TEMPO|current density`
- relation_type: `OPERATION`
- retrieval_score: `0.389706`
```text
Evidence 3
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, TEMPO achieved/reported current density.
Entities: ["TEMPO"]
Metrics: ["current density"]
Values: []
Conditions: []
Raw support excerpt: TEMPO; current density Relation type: OPERATION Readable labels: TEMPO; current density Description: TEMPO cell operated at current densities from 20 to 100 mA/cm2 Source evidence: TEMPO cell operated at current densities from 20 to 100 mA/cm2

```
#### Evidence 4
- evidence_id: `TEMPO|energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.389706`
```text
Evidence 4
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, TEMPO achieved/reported energy efficiency.
Entities: ["TEMPO"]
Metrics: ["energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: TEMPO; energy efficiency Relation type: OPERATION Readable labels: TEMPO; energy efficiency Description: TEMPO cell achieved EE of 84.3% at 100 mA/cm2, up to 88.5% at 20 mA/cm2 Source evidence: TEMPO cell achieved EE of 84.3% at 100 mA/cm2, up to 88.5% at 20 mA/cm2

```
#### Evidence 5
- evidence_id: `coulombic efficiency (Nafion 117, 25°C)|current density`
- relation_type: `OPERATION`
- retrieval_score: `0.345588`
```text
Evidence 5
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported coulombic efficiency (Nafion 117, 25°C), current density.
Entities: []
Metrics: ["coulombic efficiency (Nafion 117, 25°C)", "current density"]
Values: []
Conditions: []
Raw support excerpt: coulombic efficiency (Nafion 117, 25°C); current density Relation type: OPERATION Readable labels: coulombic efficiency (Nafion 117, 25°C); current density Description: CE of Nafion 117 increases with current density Source evidence: CE of Nafion 117 increases with current density

```

## DOC02-QA-004 / chem_prompt_hypergraph
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of SNPBI-1.42 at 100 mA/cm2, and how does it compare to SPTPC-2.59 at the same current density?
- Reference answer: SNPBI-1.42 achieves EE of 80.5% at 100 mA/cm2 (CE 98.1%, VE 82.1%), while SPTPC-2.59 achieves EE of 81.4% at 100 mA/cm2 (CE 96.3%, VE 83.8%). Although SPTPC-2.59 has a slightly higher EE, SNPBI-1.42 achieves its EE through higher CE and lower vanadium permeability, suggesting better long-term cycling stability.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["SNPBI-1.42 EE: 80.5% (CE 98.1%, VE 82.1%)", "SPTPC-2.59 EE: 81.4% (CE 96.3%, VE 83.8%)", "SPTPC-2.59 has slightly higher EE", "SNPBI-1.42 has higher CE suggesting better cycle stability"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer states 'I don't know based on the retrieved evidence' and provides no citations, which constitutes an abstention. Since the question is answerable and the reference answer provides the required information, the abstention is incorrect. The answer fails to cover any of the required key points, resulting in zero key point coverage. It is not hallucinated because it does not make any unsupported claims, but it is not useful or satisfactory.

### Evidence Blocks
#### Evidence 1
- evidence_id: `coulombic efficiency|current density|energy efficiency|voltage efficiency|zinc dendrite growth rate`
- relation_type: `OPERATION`
- retrieval_score: `0.497059`
```text
Evidence 1
Source: chunk-hyperrag-DOC07
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, zinc dendrite growth rate achieved/reported coulombic efficiency, current density, energy efficiency, voltage efficiency.
Entities: ["zinc dendrite growth rate"]
Metrics: ["coulombic efficiency", "current density", "energy efficiency", "voltage efficiency"]
Values: []
Conditions: []
Raw support excerpt: coulombic efficiency; current density; energy efficiency; voltage efficiency; zinc dendrite growth rate Relation type: OPERATION Readable labels: coulombic efficiency; current density; energy efficiency; voltage efficiency; zinc dendrite growth rate Description: Current density variation from 20 to 80 mA/cm2 at 0.3 M MEP shows tradeoff: higher CD increases CE and dendrite growth but decreases VE, with EE relatively stable. Source evidence: At 20 mA/cm2, CE 85.3%, VE 75.2%, EE 64.1%; at 80 mA/cm2, CE 92.1%, VE 65.8%, EE 60.6%

```
#### Evidence 2
- evidence_id: `TEMPO|coulombic efficiency|current density|energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.477941`
```text
Evidence 2
Source: chunk-hyperrag-DOC09
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, TEMPO achieved/reported coulombic efficiency, current density, energy efficiency.
Entities: ["TEMPO"]
Metrics: ["coulombic efficiency", "current density", "energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: TEMPO; coulombic efficiency; current density; energy efficiency Relation type: OPERATION Readable labels: TEMPO; coulombic efficiency; current density; energy efficiency Description: TEMPO cell performance across current densities 20-100 mA/cm2: CE 98.2-99.0%, EE 84.3-88.5% Source evidence: At 20 mA/cm2, the system demonstrated an EE of 88.5% with CE approaching 99.0%.

```
#### Evidence 3
- evidence_id: `current density|gross energy efficiency`
- relation_type: `OPERATION`
- retrieval_score: `0.433824`
```text
Evidence 3
Source: chunk-hyperrag-DOC04
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, gross energy efficiency.
Entities: []
Metrics: ["current density", "gross energy efficiency"]
Values: []
Conditions: []
Raw support excerpt: current density; gross energy efficiency Relation type: OPERATION Readable labels: current density; gross energy efficiency Description: Higher current density reduces gross EE due to increased overpotential; 50 mA/cm² gives highest values Source evidence: Higher current density reduces gross EE due to increased overpotential; 50 mA/cm² gives highest values

```
#### Evidence 4
- evidence_id: `PBI|SNPBI-1.42`
- relation_type: `COMPARISON<SEP>COMPOSITION`
- retrieval_score: `0.426471`
```text
Evidence 4
Source: chunk-hyperrag-DOC02
Relation/Type: COMPARISON<SEP>COMPOSITION
Short claim: Evidence reports PBI, SNPBI-1.42. Conditions: not explicitly stated.
Entities: ["PBI", "SNPBI-1.42"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; SNPBI-1.42 Relation type: COMPARISON<SEP>COMPOSITION Readable labels: PBI; SNPBI-1.42 Description: PBI and SNPBI-1.42 compared on IEC, area resistance, vanadium permeability, water uptake, and efficiencies Source evidence: SNPBI-1.42 is derived from PBI by post-sulfonation using fuming and concentrated sulfuric acid ; PBI and SNPBI-1.42 compared on IEC, area resistance, vanadium permeability, water uptake, and efficiencies

```
#### Evidence 5
- evidence_id: `Nafion 117|SPEEK|SPEEK sulfonation degree 42%|capacity fade rate (SPEEK membrane)|capacity fade rate (VRFB with Nafion 117)|energy efficiency (SPEEK membrane at 100 mA/cm2)|energy efficiency (VRFB 100 mA/cm2)`
- relation_type: `COMPARISON`
- retrieval_score: `0.397059`
```text
Evidence 5
Source: chunk-hyperrag-DOC10
Relation/Type: COMPARISON
Short claim: Under the reported conditions, capacity fade rate (SPEEK membrane) = 0.018 %/cycle, while capacity fade rate (VRFB with Nafion 117). Relation: COMPARISON.
Entities: ["Nafion 117", "SPEEK", "SPEEK sulfonation degree 42% = 42 %", "SPEEK sulfonation degree 42%"]
Metrics: ["capacity fade rate (SPEEK membrane) = 0.018 %/cycle", "capacity fade rate (VRFB with Nafion 117)", "energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %", "energy efficiency (VRFB 100 mA/cm2) = 84 %", "capacity fade rate (SPEEK membrane)", "energy efficiency (SPEEK membrane at 100 mA/cm2)", "energy efficiency (VRFB 100 mA/cm2)"]
Values: ["SPEEK sulfonation degree 42% = 42 %", "capacity fade rate (SPEEK membrane) = 0.018 %/cycle", "energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %", "energy efficiency (VRFB 100 mA/cm2) = 84 %"]
Conditions: []
Raw support excerpt: Nafion 117; SPEEK; SPEEK sulfonation degree 42% = 42 %; capacity fade rate (SPEEK membrane) = 0.018 %/cycle; capacity fade rate (VRFB with Nafion 117); energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %; energy efficiency (VRFB 100 mA/cm2) = 84 % Relation type: COMPARISON Readable labels: Nafion 117; SPEEK; SPEEK sulfonation degree 42% = 42 %; capacity fade rate (SPEEK membrane) = 0.018 %/cycle; capacity fade rate (VRFB with Nafion 117); energy efficiency (SPEEK membrane at 100 mA/cm2) = 83 %; energy efficiency (VRFB 100 mA/cm2) = 84 % Description: Comparison of Nafion 117 and SPEEK membranes in VRFB: SPEEK with 42% sulfonation achieves slightly lower EE (83%
```

## DOC02-QA-004 / chem_norm_hypergraph
- Category: `condition-heavy`
- Answerable: `True`
- Question: What is the energy efficiency of SNPBI-1.42 at 100 mA/cm2, and how does it compare to SPTPC-2.59 at the same current density?
- Reference answer: SNPBI-1.42 achieves EE of 80.5% at 100 mA/cm2 (CE 98.1%, VE 82.1%), while SPTPC-2.59 achieves EE of 81.4% at 100 mA/cm2 (CE 96.3%, VE 83.8%). Although SPTPC-2.59 has a slightly higher EE, SNPBI-1.42 achieves its EE through higher CE and lower vanadium permeability, suggesting better long-term cycling stability.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `POOR` | Good: `False` | Satisfactory+: `False` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `False`
- Missing key points: `["SNPBI-1.42 EE: 80.5% (CE 98.1%, VE 82.1%)", "SPTPC-2.59 EE: 81.4% (CE 96.3%, VE 83.8%)", "SPTPC-2.59 has slightly higher EE", "SNPBI-1.42 has higher CE suggesting better cycle stability"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer abstains from answering, stating it does not know based on retrieved evidence. However, the question is answerable and the reference answer provides specific values. The answer provides no information, covers none of the required key points, and is not useful. Therefore it is rated as POOR.

### Evidence Blocks
#### Evidence 1
- evidence_id: `condition:current_density|condition:temperature|membrane:nafion_117|membrane:nafion_212`
- relation_type: `COMPARISON`
- retrieval_score: `0.459559`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: COMPARISON
Short claim: Under temperature, condition:temperature, current density, while condition:current_density. Relation: COMPARISON.
Entities: ["Nafion 117", "Nafion 212", "membrane:nafion_117", "membrane:nafion_212"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: ["temperature", "condition:temperature"]
Raw support excerpt: current density; temperature; Nafion 117; Nafion 212 Relation type: COMPARISON Readable labels: current density; temperature; Nafion 117; Nafion 212 Description: Comprehensive comparison of Nafion 117 and Nafion 212 membranes across current densities (40-200 mA/cm2) and temperatures (25-40 C) for coulombic, voltage, and energy efficiency. Source evidence: At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%.

```
#### Evidence 2
- evidence_id: `condition:bi3_concentration|condition:current_density|metric:ce|metric:ve`
- relation_type: `COMPARISON`
- retrieval_score: `0.459559`
```text
Evidence 2
Source: chunk-hyperrag-DOC06
Relation/Type: COMPARISON
Short claim: Under Bi3+ concentration, current density, while coulombic efficiency = 93 %. Relation: COMPARISON.
Entities: ["condition:bi3_concentration", "metric:ce", "metric:ve"]
Metrics: ["current density", "coulombic efficiency = 93 %", "voltage efficiency", "condition:current_density"]
Values: ["coulombic efficiency = 93 %"]
Conditions: ["Bi3+ concentration"]
Raw support excerpt: Bi3+ concentration; current density; coulombic efficiency = 93 %; voltage efficiency Relation type: COMPARISON Readable labels: Bi3+ concentration; current density; coulombic efficiency = 93 %; voltage efficiency Description: Comparison of efficiencies at different Bi3+ concentrations (0.5-5.0 mmol/L) and current densities (40-160 mA/cm2); baseline without Bi3+ yields lower values Source evidence: With Bi3+ addition, Coulombic efficiency improved to the range of 87-96% and energy efficiency reached 62-85%

```
#### Evidence 3
- evidence_id: `condition:charge_cutoff_voltage|condition:current_density|condition:discharge_cutoff_voltage|condition:flow_rate|membrane:pbi|membrane:snpbi_1_42|membrane:speek_apk|membrane:sptpc_2_59|unresolved:single_cell_vrfb`
- relation_type: `OPERATION`
- retrieval_score: `0.452614`
```text
Evidence 3
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, flow rate, PBI, SNPBI-1.42, SPEEK/APK achieved/reported charge cutoff voltage, current density, discharge cutoff voltage, condition:charge_cutoff_voltage.
Entities: ["flow rate", "PBI", "SNPBI-1.42", "SPEEK/APK", "SPTPC-2.59", "single-cell VRFB", "condition:flow_rate", "membrane:pbi", "membrane:snpbi_1_42", "membrane:speek_apk", "membrane:sptpc_2_59", "unresolved:single_cell_vrfb"]
Metrics: ["charge cutoff voltage", "current density", "discharge cutoff voltage", "condition:charge_cutoff_voltage", "condition:current_density", "condition:discharge_cutoff_voltage"]
Values: []
Conditions: []
Raw support excerpt: charge cutoff voltage; current density; discharge cutoff voltage; flow rate; PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59; single-cell VRFB Relation type: OPERATION Readable labels: charge cutoff voltage; current density; discharge cutoff voltage; flow rate; PBI; SNPBI-1.42; SPEEK/APK; SPTPC-2.59; single-cell VRFB Description: All four non-fluorinated membranes were tested in a single cell VRFB under identical conditions: current density range 40-200 mA/cm2, flow rate 40 mL/min, charge cutoff 1.65 V, discharge cutoff 0.8 V. Source evidence: Single cell VRFB tests were conducted using an active electrode area of 10 cm2 ... with voltage limits of 0.8 V (discharge cutoff) and 1.65 V (charge cutoff).

```
#### Evidence 4
- evidence_id: `condition:current_density|metric:ce`
- relation_type: `OPERATION`
- retrieval_score: `0.389706`
```text
Evidence 4
Source: chunk-hyperrag-DOC08<SEP>chunk-hyperrag-DOC06
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, metric:ce achieved/reported current density, coulombic efficiency = 93 %, condition:current_density.
Entities: ["metric:ce"]
Metrics: ["current density", "coulombic efficiency = 93 %", "condition:current_density"]
Values: ["coulombic efficiency = 93 %"]
Conditions: []
Raw support excerpt: current density; coulombic efficiency = 93 % Relation type: OPERATION Readable labels: current density; coulombic efficiency = 93 % Description: Coulombic efficiency measured at various current densities from 40 to 160 mA/cm2 Source evidence: Coulombic efficiency measured at various current densities from 40 to 160 mA/cm2 ; Coulombic efficiency measured at varying current densities (10-40 mA/cm2)

```
#### Evidence 5
- evidence_id: `condition:current_density|condition:discharge_cutoff_voltage`
- relation_type: `OPERATION`
- retrieval_score: `0.389706`
```text
Evidence 5
Source: chunk-hyperrag-DOC06
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, the entity achieved/reported current density, discharge cutoff voltage, condition:current_density, condition:discharge_cutoff_voltage.
Entities: []
Metrics: ["current density", "discharge cutoff voltage", "condition:current_density", "condition:discharge_cutoff_voltage"]
Values: []
Conditions: []
Raw support excerpt: current density; discharge cutoff voltage Relation type: OPERATION Readable labels: current density; discharge cutoff voltage Description: Discharge cutoff voltage 0.3 V used with various current densities Source evidence: Discharge cutoff voltage 0.3 V used with various current densities

```

## UNANS-QA-SMOKE-001 / text_segments
- Category: `unanswerable`
- Answerable: `False`
- Question: What d33 piezoelectric coefficient was measured for BaTiO3 during VRFB operation?
- Reference answer: The corpus does not provide a BaTiO3 d33 piezoelectric coefficient for VRFB operation.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The question is unanswerable based on the corpus, and the generated answer correctly abstains by stating 'I don't know based on the retrieved evidence.' It does not introduce any unsupported claims, and it implicitly covers the required key point that the coefficient is not provided for VRFB operation. The answer is fully grounded and non-hallucinated.

### Evidence Blocks
#### Evidence 1
- evidence_id: `chunk-hyperrag-DOC02`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.45`
```text
Evidence 1
Source: DOC02
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators. ### 3.4 Structure-Transport Correlations The trade-off between proton conductivity (inverse of resistance) and vanadium selectivity (inverse of permeability) defines the fundamental performance envelope for VRFB membranes. VRFB Performance Evaluation ### 4.1 Coulombic Efficiency The coulombic efficiency of all four membranes showed the expected positive correlation with current density, consistent with the fundamental mechanism wherein the parasitic crossover flux becomes a smaller fraction of the total current at higher operational currents. ### 6.3 Degradation Chain Analysis The degradation of non-fluorinated VRFB membranes follows a chain process that initiates with chemical attack on the polymer backbone or pendant acid groups, progresses through loss of ion exchange capacity and/or mechanical integrity, and manifests as declining voltage efficiency and/or increasing vanadium crossover.

```
#### Evidence 2
- evidence_id: `chunk-hyperrag-DOC04`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.45`
```text
Evidence 2
Source: DOC04
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a systematic investigation of how vanadium concentration, sulfuric acid supporting electrolyte concentration, electrolyte flow rate, and operating current density collectively influence the electrochemical performance of VRFBs. For stationary energy storage applications where high round-trip efficiency is prioritized, operation at 1.6 mol/L vanadium in 3.0 mol/L H2SO4 with 40 mL/min flow rate and 100 mA/cm2 current density provides net EE of approximately 80%, representing a favorable compromise between efficiency and power density. Conclusion This systematic investigation has elucidated the complex interdependence of electrolyte concentration, flow rate, and current density on VRFB performance metrics and system-level net efficiency. These findings provide quantitative design guidelines for maximizing the practical energy efficiency of VRFB systems while accounting for the essential trade-off between mass transfer enhancement and pumping energy consumption.

```
#### Evidence 3
- evidence_id: `chunk-hyperrag-DOC05`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.45`
```text
Evidence 3
Source: DOC05
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: This study presents a comprehensive experimental investigation into the temperature-dependent behavior of VRFB cells operated at 25 C, 40 C, and 60 C over 500 charge-discharge cycles at a constant current density of 80 mA/cm2. The results demonstrate that elevated temperatures accelerate vanadium ion crossover through the ion-exchange membrane, exacerbate state-of-charge (SOC) imbalance between the positive and negative half-cells, and precipitate more rapid capacity fading. By maintaining all other operational parameters constant-including current density at 80 mA/cm2, electrolyte composition at 1.5 M VOSO4 in 3.0 M H2SO4, and electrolyte flow rate at 40 mL/min-we establish a controlled experimental framework wherein observed differences in performance can be confidently attributed to temperature effects. Results and Discussion ### 3.1 Capacity Retention Behavior Across Temperatures The long-term cycling behavior of VRFB cells operated at 25 C, 40 C, and 60 C revealed pronounced temperature-dependent differences in capacity retention trajectories.

```
#### Evidence 4
- evidence_id: `chunk-hyperrag-DOC06`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.45`
```text
Evidence 4
Source: DOC06
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: With Bi3+ addition, Coulombic efficiency improved to the range of 87-96% and energy efficiency reached 62-85% depending on the specific concentration and current density. The work addresses three primary objectives: (1) quantifying the kinetic enhancement of the Cr(III)/Cr(II) redox reaction in the presence of Bi3+, (2) characterizing the suppression of parasitic hydrogen evolution achieved through Bi3+ addition, and (3) establishing the relationship between Bi3+ concentration, operational current density, and full-cell performance metrics including Coulombic efficiency, voltage efficiency, and energy efficiency. These measurements provided information on the stability of Bi3+ in the electrolyte and the extent of crossover of active species between half-cells during operation. The principal findings are as follows: The addition of Bi3+ at concentrations of 0.5-5.0 mmol/L to the negative electrolyte substantially improves both Coulombic efficiency and energy efficiency across the operational current density range of 40-160 mA/cm2.

```
#### Evidence 5
- evidence_id: `chunk-hyperrag-DOC01`
- relation_type: `TEXT_CHUNK`
- retrieval_score: `0.375`
```text
Evidence 5
Source: DOC01
Relation/Type: TEXT_CHUNK
Short claim: Evidence reports TEXT_CHUNK. Conditions: not explicitly stated.
Entities: []
Metrics: []
Values: []
Conditions: []
Raw support excerpt: By systematically varying current density from 40 to 200 mA/cm2 and operating temperature from 25 C to 40 C, we elucidate the fundamental trade-offs between coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) that govern membrane selection. The approximately 3-4 percentage point gap between Nafion 212 and Nafion 117 CE values at any given current density directly reflects the twofold difference in vanadium permeability between the two membranes. For high-temperature operation above 35 C, Nafion 212 may be preferred as its voltage efficiency advantage becomes more pronounced and the crossover penalty is partially offset by the shorter diffusion pathway. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s).

```

## UNANS-QA-SMOKE-001 / original_hypergraph
- Category: `unanswerable`
- Answerable: `False`
- Question: What d33 piezoelectric coefficient was measured for BaTiO3 during VRFB operation?
- Reference answer: The corpus does not provide a BaTiO3 d33 piezoelectric coefficient for VRFB operation.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `SATISFACTORY` | Good: `False` | Satisfactory+: `True` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `["state that BaTiO3 d33 piezoelectric coefficient is not provided for VRFB operation"]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly abstains from answering, indicating that the information is not known from the retrieved evidence. However, it does not explicitly state that the BaTiO3 d33 piezoelectric coefficient is not provided for VRFB operation, which is the required key point. The answer is non-hallucinated and partially useful, but lacks the explicit statement, so it is satisfactory.

### Evidence Blocks
#### Evidence 1
- evidence_id: `VRFB|vanadium redox flow battery`
- relation_type: `ASSOCIATED_WITH`
- retrieval_score: `0.2`
```text
Evidence 1
Source: chunk-hyperrag-DOC05
Relation/Type: ASSOCIATED_WITH
Short claim: Evidence reports VRFB, vanadium redox flow battery. Conditions: not explicitly stated.
Entities: ["VRFB", "vanadium redox flow battery"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: VRFB; vanadium redox flow battery Relation type: ASSOCIATED_WITH Readable labels: VRFB; vanadium redox flow battery Description: Acronym used for vanadium redox flow battery Source evidence: Acronym used for vanadium redox flow battery

```
#### Evidence 2
- evidence_id: `Nafion 117 membrane|VRFB`
- relation_type: `PART_OF`
- retrieval_score: `0.2`
```text
Evidence 2
Source: chunk-hyperrag-DOC05
Relation/Type: PART_OF
Short claim: Evidence reports Nafion 117 membrane, VRFB. Conditions: not explicitly stated.
Entities: ["Nafion 117 membrane", "VRFB"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: Nafion 117 membrane; VRFB Relation type: PART_OF Readable labels: Nafion 117 membrane; VRFB Description: Nafion 117 membrane is used as separator in VRFB Source evidence: Nafion 117 membrane is used as separator in VRFB

```
#### Evidence 3
- evidence_id: `VRFB|graphite felt electrode (SGL Carbon GFD 4.6 EA)`
- relation_type: `PART_OF`
- retrieval_score: `0.2`
```text
Evidence 3
Source: chunk-hyperrag-DOC05
Relation/Type: PART_OF
Short claim: Evidence reports VRFB. Conditions: graphite felt electrode (SGL Carbon GFD 4.6 EA).
Entities: ["VRFB"]
Metrics: []
Values: []
Conditions: ["graphite felt electrode (SGL Carbon GFD 4.6 EA)"]
Raw support excerpt: VRFB; graphite felt electrode (SGL Carbon GFD 4.6 EA) Relation type: PART_OF Readable labels: VRFB; graphite felt electrode (SGL Carbon GFD 4.6 EA) Description: Graphite felt electrodes used in VRFB cell Source evidence: Graphite felt electrodes used in VRFB cell

```
#### Evidence 4
- evidence_id: `VRFB|graphite composite bipolar plate with serpentine flow fields`
- relation_type: `PART_OF`
- retrieval_score: `0.2`
```text
Evidence 4
Source: chunk-hyperrag-DOC05
Relation/Type: PART_OF
Short claim: Evidence reports VRFB. Conditions: graphite composite bipolar plate with serpentine flow fields.
Entities: ["VRFB"]
Metrics: []
Values: []
Conditions: ["graphite composite bipolar plate with serpentine flow fields"]
Raw support excerpt: VRFB; graphite composite bipolar plate with serpentine flow fields Relation type: PART_OF Readable labels: VRFB; graphite composite bipolar plate with serpentine flow fields Description: Bipolar plates with flow fields used in VRFB Source evidence: Bipolar plates with flow fields used in VRFB

```
#### Evidence 5
- evidence_id: `VOSO4·xH2O|VRFB`
- relation_type: `PART_OF`
- retrieval_score: `0.2`
```text
Evidence 5
Source: chunk-hyperrag-DOC05
Relation/Type: PART_OF
Short claim: Evidence reports VOSO4·xH2O, VRFB. Conditions: not explicitly stated.
Entities: ["VOSO4·xH2O", "VRFB"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: VOSO4·xH2O; VRFB Relation type: PART_OF Readable labels: VOSO4·xH2O; VRFB Description: VOSO4·xH2O used as vanadium source in electrolyte Source evidence: VOSO4·xH2O used as vanadium source in electrolyte

```

## UNANS-QA-SMOKE-001 / chem_prompt_graph
- Category: `unanswerable`
- Answerable: `False`
- Question: What d33 piezoelectric coefficient was measured for BaTiO3 during VRFB operation?
- Reference answer: The corpus does not provide a BaTiO3 d33 piezoelectric coefficient for VRFB operation.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly abstains from answering because the retrieved evidence does not provide the BaTiO3 d33 piezoelectric coefficient for VRFB operation. It does not contain any unsupported claims and covers the required key point by implying the information is not available.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|thickness (Nafion 117)`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 117, thickness (Nafion 117) = 183 um, thickness (Nafion 117). Conditions: not explicitly stated.
Entities: ["Nafion 117", "thickness (Nafion 117) = 183 um", "thickness (Nafion 117)"]
Metrics: []
Values: ["thickness (Nafion 117) = 183 um"]
Conditions: []
Raw support excerpt: Nafion 117; thickness (Nafion 117) = 183 um Relation type: OPERATION Readable labels: Nafion 117; thickness (Nafion 117) = 183 um Description: Measured thickness of Nafion 117 is 183 um Source evidence: Measured thickness of Nafion 117 is 183 um

```
#### Evidence 2
- evidence_id: `Nafion 212|thickness (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 212, thickness (Nafion 212) = 50.8 um, thickness (Nafion 212). Conditions: not explicitly stated.
Entities: ["Nafion 212", "thickness (Nafion 212) = 50.8 um", "thickness (Nafion 212)"]
Metrics: []
Values: ["thickness (Nafion 212) = 50.8 um"]
Conditions: []
Raw support excerpt: Nafion 212; thickness (Nafion 212) = 50.8 um Relation type: OPERATION Readable labels: Nafion 212; thickness (Nafion 212) = 50.8 um Description: Measured thickness of Nafion 212 is 50.8 um Source evidence: Measured thickness of Nafion 212 is 50.8 um

```
#### Evidence 3
- evidence_id: `carbon felt (SGL Carbon GFD 4.6 EA)|single cell VRFB`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 3
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: Evidence reports OPERATION. Conditions: carbon felt (SGL Carbon GFD 4.6 EA), single cell VRFB.
Entities: []
Metrics: []
Values: []
Conditions: ["carbon felt (SGL Carbon GFD 4.6 EA)", "single cell VRFB"]
Raw support excerpt: carbon felt (SGL Carbon GFD 4.6 EA); single cell VRFB Relation type: OPERATION Readable labels: carbon felt (SGL Carbon GFD 4.6 EA); single cell VRFB Description: Carbon felt electrodes used in single cell VRFB testing with 15% compression Source evidence: Carbon felt electrodes used in single cell VRFB testing with 15% compression

```
#### Evidence 4
- evidence_id: `active electrode area|single cell VRFB`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 4
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: Evidence reports active electrode area. Conditions: single cell VRFB.
Entities: ["active electrode area"]
Metrics: []
Values: []
Conditions: ["single cell VRFB"]
Raw support excerpt: active electrode area; single cell VRFB Relation type: OPERATION Readable labels: active electrode area; single cell VRFB Description: Single cell VRFB testing with active electrode area of 10 cm2 Source evidence: Single cell VRFB testing with active electrode area of 10 cm2

```
#### Evidence 5
- evidence_id: `EIS workstation|two-electrode cell`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 5
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: Evidence reports EIS workstation. Conditions: two-electrode cell.
Entities: ["EIS workstation"]
Metrics: []
Values: []
Conditions: ["two-electrode cell"]
Raw support excerpt: EIS workstation; two-electrode cell Relation type: OPERATION Readable labels: EIS workstation; two-electrode cell Description: Area-specific resistance measured by EIS using two-electrode cell Source evidence: Area-specific resistance measured by EIS using two-electrode cell

```

## UNANS-QA-SMOKE-001 / chem_prompt_hypergraph
- Category: `unanswerable`
- Answerable: `False`
- Question: What d33 piezoelectric coefficient was measured for BaTiO3 during VRFB operation?
- Reference answer: The corpus does not provide a BaTiO3 d33 piezoelectric coefficient for VRFB operation.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `GOOD` | Good: `True` | Satisfactory+: `True` | KPC: `1.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `[]`
- Unsupported claims found: `[]`
- Rationale: The generated answer correctly abstains from providing a value, stating 'I don't know based on the retrieved evidence.' This matches the reference answer that the corpus does not provide the coefficient. The answer covers the required key point (stating the coefficient is not provided) and contains no unsupported claims. It is fully grounded and non-hallucinated.

### Evidence Blocks
#### Evidence 1
- evidence_id: `Nafion 117|thickness (Nafion 117)`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 1
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 117, thickness (Nafion 117) = 183 um, thickness (Nafion 117). Conditions: not explicitly stated.
Entities: ["Nafion 117", "thickness (Nafion 117) = 183 um", "thickness (Nafion 117)"]
Metrics: []
Values: ["thickness (Nafion 117) = 183 um"]
Conditions: []
Raw support excerpt: Nafion 117; thickness (Nafion 117) = 183 um Relation type: OPERATION Readable labels: Nafion 117; thickness (Nafion 117) = 183 um Description: Measured thickness of Nafion 117 is 183 um Source evidence: Measured thickness of Nafion 117 is 183 um

```
#### Evidence 2
- evidence_id: `Nafion 212|thickness (Nafion 212)`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 2
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports Nafion 212, thickness (Nafion 212) = 50.8 um, thickness (Nafion 212). Conditions: not explicitly stated.
Entities: ["Nafion 212", "thickness (Nafion 212) = 50.8 um", "thickness (Nafion 212)"]
Metrics: []
Values: ["thickness (Nafion 212) = 50.8 um"]
Conditions: []
Raw support excerpt: Nafion 212; thickness (Nafion 212) = 50.8 um Relation type: OPERATION Readable labels: Nafion 212; thickness (Nafion 212) = 50.8 um Description: Measured thickness of Nafion 212 is 50.8 um Source evidence: Measured thickness of Nafion 212 is 50.8 um

```
#### Evidence 3
- evidence_id: `Carbon felt electrodes (SGL GFD 4.6 EA)|active electrode area|battery cycler|current density|electrode compression ratio|electrolyte volume|flow rate|lower cutoff voltage|negative electrolyte state of charge|operating temperature|peristaltic pumps|positive electrolyte state of charge|rest interval|single-cell VRFB|total sulfate concentration|total vanadium concentration|upper cutoff voltage|water bath thermostat`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 3
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: In the reported system, under battery cycler, electrode compression ratio, negative electrolyte state of charge = 50 %, operating temperature, positive electrolyte state of charge = 50 %, total sulfate concentration = 4.5 M, total vanadium concentration = 1.6 M, negative electrolyte state of charge, positive electrolyte state of charge, total sulfate concentration, total vanadium concentration, Carbon felt electrodes (SGL GFD 4.6 EA), active electrode area, electrolyte volume, flow rate achieved/reported current density, lower cutoff voltage = 0.8 V, upper cutoff voltage = 1.65 V, lower cutoff voltage.
Entities: ["Carbon felt electrodes (SGL GFD 4.6 EA)", "active electrode area", "electrolyte volume", "flow rate", "peristaltic pumps", "rest interval = 2 min", "single-cell VRFB", "water bath thermostat", "rest interval"]
Metrics: ["current density", "lower cutoff voltage = 0.8 V", "upper cutoff voltage = 1.65 V", "lower cutoff voltage", "upper cutoff voltage"]
Values: ["lower cutoff voltage = 0.8 V", "negative electrolyte state of charge = 50 %", "positive electrolyte state of charge = 50 %", "rest interval = 2 min", "total sulfate concentration = 4.5 M", "total vanadium concentration = 1.6 M", "upper cutoff voltage = 1.65 V"]
Conditions: ["battery cycler", "electrode compression ratio", "negative electrolyte state of charge = 50 %", "operating temperature", "positive electrolyte state of charge = 50 %", "total sulfate concentration = 4.5 M", "total vanadium concentration = 1.6 M", "negative electr
```
#### Evidence 4
- evidence_id: `carbon felt (SGL Carbon GFD 4.6 EA)|single cell VRFB`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 4
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: Evidence reports OPERATION. Conditions: carbon felt (SGL Carbon GFD 4.6 EA), single cell VRFB.
Entities: []
Metrics: []
Values: []
Conditions: ["carbon felt (SGL Carbon GFD 4.6 EA)", "single cell VRFB"]
Raw support excerpt: carbon felt (SGL Carbon GFD 4.6 EA); single cell VRFB Relation type: OPERATION Readable labels: carbon felt (SGL Carbon GFD 4.6 EA); single cell VRFB Description: Carbon felt electrodes used in single cell VRFB testing with 15% compression Source evidence: Carbon felt electrodes used in single cell VRFB testing with 15% compression

```
#### Evidence 5
- evidence_id: `active electrode area|single cell VRFB`
- relation_type: `OPERATION`
- retrieval_score: `0.15`
```text
Evidence 5
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: Evidence reports active electrode area. Conditions: single cell VRFB.
Entities: ["active electrode area"]
Metrics: []
Values: []
Conditions: ["single cell VRFB"]
Raw support excerpt: active electrode area; single cell VRFB Relation type: OPERATION Readable labels: active electrode area; single cell VRFB Description: Single cell VRFB testing with active electrode area of 10 cm2 Source evidence: Single cell VRFB testing with active electrode area of 10 cm2

```

## UNANS-QA-SMOKE-001 / chem_norm_hypergraph
- Category: `unanswerable`
- Answerable: `False`
- Question: What d33 piezoelectric coefficient was measured for BaTiO3 during VRFB operation?
- Reference answer: The corpus does not provide a BaTiO3 d33 piezoelectric coefficient for VRFB operation.
- Generated answer: I don't know based on the retrieved evidence.
- Quality: `SATISFACTORY` | Good: `False` | Satisfactory+: `True` | KPC: `0.0` | Hallucinated: `False` | Abstained: `True` | Abstention correct: `True`
- Missing key points: `["state that BaTiO3 d33 piezoelectric coefficient is not provided for VRFB operation"]`
- Unsupported claims found: `[]`
- Rationale: The answer correctly abstains from providing a value, stating it does not know based on the retrieved evidence. It is non-hallucinated and partially useful. However, it does not explicitly state that the BaTiO3 d33 piezoelectric coefficient is not provided for VRFB operation, which is a required key point. Therefore, it is not fully complete, but still satisfactory.

### Evidence Blocks
#### Evidence 1
- evidence_id: `condition:flow_rate|unresolved:single_cell_vrfb`
- relation_type: `OPERATION`
- retrieval_score: `0.3`
```text
Evidence 1
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: Evidence reports flow rate, single-cell VRFB, condition:flow_rate, unresolved:single_cell_vrfb. Conditions: not explicitly stated.
Entities: ["flow rate", "single-cell VRFB", "condition:flow_rate", "unresolved:single_cell_vrfb"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: flow rate; single-cell VRFB Relation type: OPERATION Readable labels: flow rate; single-cell VRFB Description: Electrolyte flow rate was maintained at 40 mL/min during tests Source evidence: Electrolyte flow rate was maintained at 40 mL/min during tests

```
#### Evidence 2
- evidence_id: `electrode:c_c|metric:contact_angle`
- relation_type: `OPERATION`
- retrieval_score: `0.275`
```text
Evidence 2
Source: chunk-hyperrag-DOC03
Relation/Type: OPERATION
Short claim: Evidence reports C-C, contact angle = 4.0 deg, electrode:c_c, metric:contact_angle. Conditions: not explicitly stated.
Entities: ["C-C", "contact angle = 4.0 deg", "electrode:c_c", "metric:contact_angle"]
Metrics: []
Values: ["contact angle = 4.0 deg"]
Conditions: []
Raw support excerpt: C-C; contact angle = 4.0 deg Relation type: OPERATION Readable labels: C-C; contact angle = 4.0 deg Description: contact angle measured for C-C Source evidence: contact angle measured for C-C

```
#### Evidence 3
- evidence_id: `condition:current_density|system:vrfb`
- relation_type: `OPERATION`
- retrieval_score: `0.275`
```text
Evidence 3
Source: chunk-hyperrag-DOC05
Relation/Type: OPERATION
Short claim: In the reported system, under the stated conditions, VRFB, system:vrfb achieved/reported current density, condition:current_density.
Entities: ["VRFB", "system:vrfb"]
Metrics: ["current density", "condition:current_density"]
Values: []
Conditions: []
Raw support excerpt: current density; VRFB Relation type: OPERATION Readable labels: current density; VRFB Description: Operated at constant current density 80 mA/cm2 Source evidence: Operated at constant current density 80 mA/cm2

```
#### Evidence 4
- evidence_id: `active_species:mgso4|active_species:voso4|species:h2so4|system:dialysis_cell|system:spectrophotometer`
- relation_type: `OPERATION`
- retrieval_score: `0.225`
```text
Evidence 4
Source: chunk-hyperrag-DOC01
Relation/Type: OPERATION
Short claim: Evidence reports MgSO4, H2SO4, active_species:mgso4, active_species:voso4, species:h2so4, system:dialysis_cell. Conditions: VOSO4 = 2.0 mol/L, dialysis cell, spectrophotometer, system:spectrophotometer.
Entities: ["MgSO4", "H2SO4", "active_species:mgso4", "active_species:voso4", "species:h2so4", "system:dialysis_cell"]
Metrics: []
Values: ["VOSO4 = 2.0 mol/L"]
Conditions: ["VOSO4 = 2.0 mol/L", "dialysis cell", "spectrophotometer", "system:spectrophotometer"]
Raw support excerpt: MgSO4; VOSO4 = 2.0 mol/L; H2SO4; dialysis cell; spectrophotometer Relation type: OPERATION Readable labels: MgSO4; VOSO4 = 2.0 mol/L; H2SO4; dialysis cell; spectrophotometer Description: Vanadium permeability measurement using dialysis cell with VOSO4/H2SO4 feed and MgSO4/H2SO4 receiver, monitored spectrophotometrically. Source evidence: Vanadium permeability was measured using a dialysis cell setup in which a membrane separated a vanadium solution (1 M VOSO4 in 2 M H2SO4) from a receiving compartment containing 1 M MgSO4 in 2 M H2SO4.

```
#### Evidence 5
- evidence_id: `membrane:pbi|unresolved:single_cell_vrfb`
- relation_type: `OPERATION`
- retrieval_score: `0.225`
```text
Evidence 5
Source: chunk-hyperrag-DOC02
Relation/Type: OPERATION
Short claim: Evidence reports PBI, single-cell VRFB, membrane:pbi, unresolved:single_cell_vrfb. Conditions: not explicitly stated.
Entities: ["PBI", "single-cell VRFB", "membrane:pbi", "unresolved:single_cell_vrfb"]
Metrics: []
Values: []
Conditions: []
Raw support excerpt: PBI; single-cell VRFB Relation type: OPERATION Readable labels: PBI; single-cell VRFB Description: PBI membrane was tested in a single cell VRFB under standard conditions Source evidence: PBI membrane was tested in a single cell VRFB under standard conditions

```
