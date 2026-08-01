# Hyper-ChE Flow Battery Benchmark Corpus

**Dataset**: Hyper-ChE Flow Battery Benchmark v1.1
**Domain**: Redox flow battery
**Type**: Synthetic controlled corpus
**Document Count**: 10
---

# DOC01: Comparative Analysis of Nafion 117 and Nafion 212 Membranes in Vanadium Redox Flow Batteries: Performance Trade-offs and Operational Dependencies

## Abstract

The selection of an appropriate ion exchange membrane represents one of the most critical design decisions in the development of high-performance vanadium redox flow batteries (VRFBs). This study presents a comprehensive comparative analysis of two benchmark perfluorinated sulfonic acid (PFSA) membranes, Nafion 117 and Nafion 212, under a wide range of operating conditions relevant to practical VRFB deployment. By systematically varying current density from 40 to 200 mA/cm2 and operating temperature from 25 C to 40 C, we elucidate the fundamental trade-offs between coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) that govern membrane selection. Our results demonstrate that Nafion 117, with its greater membrane thickness of approximately 183 um, consistently achieves superior coulombic efficiency (96-98%) due to reduced vanadium crossover, while Nafion 212, at approximately 50.8 um thickness, exhibits higher voltage efficiency (84-88%) stemming from lower area-specific resistance. These divergent performance characteristics create a complex optimization landscape where the optimal membrane choice depends sensitively on the intended application, operating protocol, and degradation tolerance of the battery system.

## 1. Introduction

Vanadium redox flow batteries have emerged as one of the most promising electrochemical energy storage technologies for grid-scale applications, offering inherent safety, long cycle life, and flexible capacity-power decoupling. The membrane component in a VRFB serves the dual function of preventing mixing of the positive and negative electrolytes while permitting selective transport of charge-carrying ions to complete the electrical circuit. These competing requirements create an intrinsic tension in membrane design: highly selective membranes that effectively block vanadium crossover typically exhibit elevated resistance, while low-resistance membranes often suffer from increased permeability to vanadium species.

Nafion membranes, produced through copolymerization of tetrafluoroethylene with perfluorinated vinyl ether sulfonyl fluoride followed by hydrolysis to sulfonic acid form, have served as the benchmark material for VRFB research since the early development of the technology. The microphase-separated morphology of Nafion, comprising hydrophilic sulfonic acid clusters embedded within a hydrophobic fluorocarbon backbone, provides excellent proton conductivity and chemical stability in the strongly acidic and oxidizing environment of vanadium electrolytes. Among the commercially available Nafion variants, Nafion 117 and Nafion 212 represent two of the most widely studied configurations, differing primarily in their equivalent weights and membrane thicknesses.

Nafion 117 possesses an equivalent weight of approximately 1100 g/equiv and a dry thickness of 183 um, while Nafion 212 has the same equivalent weight but a substantially reduced thickness of 50.8 um. These dimensional differences give rise to markedly different transport properties. The thicker Nafion 117 provides a longer diffusion pathway for vanadium ions, thereby reducing crossover rates, but simultaneously increases the ohmic resistance contribution to cell polarization. Conversely, Nafion 212 offers a shorter ionic conduction pathway and consequently lower area resistance, but at the cost of diminished barrier properties against vanadium permeation.

The present study was designed to quantify these trade-offs under rigorously controlled experimental conditions, with particular attention to the effects of current density and temperature on the efficiency metrics that determine VRFB performance. Understanding these dependencies is essential for establishing rational membrane selection criteria and for informing the development of next-generation membrane materials with improved property profiles.

## 2. Experimental Methods

### 2.1 Membrane Pretreatment

Prior to cell assembly, Nafion 117 and Nafion 212 membranes were subjected to a standardized pretreatment protocol to ensure complete conversion to the protonated form and to remove any residual manufacturing impurities. The membranes were first boiled in 3% hydrogen peroxide solution for 1 hour to remove organic contaminants, followed by thorough rinsing with deionized water. They were subsequently immersed in 1 M sulfuric acid at 80 C for 2 hours to protonate the sulfonic acid groups, then stored in deionized water until use.

### 2.2 Cell Configuration and Test Protocol

All electrochemical tests were performed using a single-cell VRFB with an active electrode area of 25 cm2. Carbon felt electrodes (SGL GFD 4.6 EA) were employed on both positive and negative sides, compressed to approximately 20% of their original thickness. The electrolyte consisted of 1.6 M total vanadium in 4.5 M total sulfate support, prepared by electrochemical dissolution of vanadium pentoxide in sulfuric acid to achieve an equilibrium state with approximately 50% V(II)/V(III) in the negative electrolyte and 50% V(IV)/V(V) in the positive electrolyte. Electrolyte volumes of 50 mL were used on each side, circulated at a flow rate of 50 mL/min using peristaltic pumps.

Galvanostatic charge-discharge cycling was performed using a battery cycler at current densities of 40, 60, 80, 100, 120, 160, and 200 mA/cm2. The upper and lower voltage limits were set at 1.65 V and 0.8 V, respectively, with a 2-minute rest interval between charge and discharge half-cycles. All current densities were tested at both 25 C and 40 C, with temperature controlled by circulating the electrolyte reservoirs through a water bath thermostat.

### 2.3 Characterization Methods

Area-specific resistance was determined by electrochemical impedance spectroscopy at open circuit potential over the frequency range of 100 kHz to 10 mHz with a perturbation amplitude of 10 mV. Vanadium permeability was measured using a dialysis cell setup in which a membrane separated a vanadium solution (1 M VOSO4 in 2 M H2SO4) from a receiving compartment containing 1 M MgSO4 in 2 M H2SO4. The vanadium concentration in the receiving compartment was monitored spectrophotometrically over time, and the permeability was calculated from the steady-state flux according to Fick's first law.

## 3. Membrane Properties and Characterization Results

### 3.1 Physical and Transport Properties

The measured physical and transport properties of Nafion 117 and Nafion 212 are summarized in Table 1. Nafion 117 exhibited an area-specific resistance of 1.65 ohm cm2 at 25 C, substantially higher than the 0.85 ohm cm2 measured for Nafion 212 under identical conditions. This difference is primarily attributable to the difference in membrane thickness, as both membranes share the same equivalent weight and therefore similar intrinsic proton conductivity. The vanadium permeability of Nafion 117 was determined to be 1.8 x 10^-7 cm2/s, compared to 3.9 x 10^-7 cm2/s for Nafion 212. The approximately twofold higher permeability of Nafion 212 reflects the shorter diffusion pathway available for vanadium species to traverse the thinner membrane.

| Property | Nafion 117 | Nafion 212 |
|---|---|---|
| Thickness (um) | 183 | 50.8 |
| Equivalent weight (g/equiv) | 1100 | 1100 |
| Area resistance (ohm cm2, 25 C) | 1.65 | 0.85 |
| Vanadium permeability (x 10^-7 cm2/s) | 1.8 | 3.9 |
| Water uptake (%) | 22 | 25 |
| Ion exchange capacity (mmol/g) | 0.91 | 0.91 |

The water uptake values, measured after equilibration in deionized water at 25 C, were 22% for Nafion 117 and 25% for Nafion 212. The slightly higher water uptake of Nafion 212 is consistent with its thinner profile, which permits more facile equilibration with the external aqueous phase. Both membranes share an identical ion exchange capacity of 0.91 mmol/g, reflecting their common equivalent weight.

### 3.2 Temperature Dependence of Area Resistance

Temperature had a pronounced effect on the area-specific resistance of both membranes. At 40 C, the area resistance of Nafion 117 decreased to 1.32 ohm cm2, while that of Nafion 212 decreased to 0.68 ohm cm2. The reduction in resistance with increasing temperature follows the expected Arrhenius-type behavior, reflecting enhanced proton mobility within the hydrophilic clusters of the Nafion microstructure. The activation energy for proton conduction, calculated from the temperature dependence of conductivity, was approximately 11.5 kJ/mol for both membranes, consistent with a vehicular proton transport mechanism predominating in the highly hydrated Nafion matrix.

## 4. Electrochemical Performance Results

### 4.1 Nafion 117 Performance Characteristics

#### 4.1.1 Coulombic Efficiency

The coulombic efficiency of the VRFB with Nafion 117 membrane demonstrated a strong positive correlation with current density. At 25 C, the CE increased monotonically from 96.0% at 40 mA/cm2 to 98.2% at 200 mA/cm2. This dependence reflects the competition between Faradaic current associated with the desired vanadium redox reactions and the parasitic crossover current associated with vanadium ion transport through the membrane. At higher current densities, the Faradaic current increases proportionally while the crossover flux, being driven primarily by concentration gradients, remains relatively constant. Consequently, the ratio of useful charge transfer to parasitic loss improves, yielding higher coulombic efficiency.

The temperature dependence of CE was modest but measurable. At 40 C, the CE values were systematically lower than at 25 C by approximately 0.3-0.5 percentage points across the entire current density range. This reduction reflects the enhanced vanadium crossover at elevated temperature, as the diffusivity of vanadium ions in the membrane increases with temperature according to the Stokes-Einstein relationship.

#### 4.1.2 Voltage Efficiency

Voltage efficiency exhibited an inverse relationship with current density, declining from 85.8% at 40 mA/cm2 to 80.2% at 200 mA/cm2 at 25 C. This decrease is attributable to the increasing contribution of ohmic polarization and activation polarization at higher current densities. The ohmic overpotential, which is directly proportional to the product of current density and area-specific resistance, increases linearly with current density and constitutes the dominant loss mechanism at current densities above 80 mA/cm2.

The effect of temperature on voltage efficiency was positive and substantial. At 40 C, the VE values were approximately 2-3 percentage points higher than at 25 C across the current density range. This improvement stems primarily from the reduction in area-specific resistance at higher temperature, which lowers the ohmic overpotential at any given current density. Additionally, enhanced electrochemical kinetics at elevated temperature contribute to reduced activation overpotential.

#### 4.1.3 Energy Efficiency

Energy efficiency, as the product of CE and VE, exhibited a non-monotonic dependence on current density. At 25 C, the EE decreased gradually from 82.4% at 40 mA/cm2 to 80.9% at 100 mA/cm2, then declined more steeply to 78.7% at 200 mA/cm2. The competing effects of increasing CE and decreasing VE with current density create an efficiency maximum at relatively low current densities, with the subsequent decline reflecting the dominance of voltage efficiency losses at higher operational currents.

At 40 C, the EE values were generally comparable to or slightly higher than those at 25 C at low current densities, but the difference diminished at higher current densities. Specifically, the EE at 40 C was 83.5% at 40 mA/cm2, 82.1% at 80 mA/cm2, 81.4% at 100 mA/cm2, 80.6% at 120 mA/cm2, and 79.1% at 200 mA/cm2. The net effect of temperature on EE reflects a balance between the positive impact on VE through reduced resistance and the negative impact on CE through enhanced vanadium crossover.

### 4.2 Nafion 212 Performance Characteristics

#### 4.2.1 Coulombic Efficiency

The VRFB assembled with Nafion 212 exhibited lower coulombic efficiency than that with Nafion 117 across all tested conditions, consistent with the higher vanadium permeability of the thinner membrane. At 25 C, the CE ranged from 92.1% at 40 mA/cm2 to 95.3% at 200 mA/cm2. The approximately 3-4 percentage point gap between Nafion 212 and Nafion 117 CE values at any given current density directly reflects the twofold difference in vanadium permeability between the two membranes.

The sensitivity of CE to current density was more pronounced for Nafion 212 than for Nafion 117, with the CE increasing by 3.2 percentage points over the current density range compared to 2.2 percentage points for Nafion 117. This greater sensitivity arises because the parasitic crossover current represents a larger fraction of the total current at low current densities for the more permeable Nafion 212 membrane.

#### 4.2.2 Voltage Efficiency

The lower area-specific resistance of Nafion 212 translated directly into superior voltage efficiency compared to Nafion 117. At 25 C, the VE of the Nafion 212 cell ranged from 88.2% at 40 mA/cm2 to 83.6% at 200 mA/cm2. The approximately 3-4 percentage point advantage over Nafion 117 is consistent with the factor of two difference in area-specific resistance between the membranes.

The temperature dependence of VE followed the same qualitative trend as observed for Nafion 117, with higher temperatures yielding improved VE due to reduced ohmic resistance. At 40 C, the Nafion 212 cell achieved VE values of 89.5% at 40 mA/cm2, 87.8% at 80 mA/cm2, 86.9% at 100 mA/cm2, 86.1% at 120 mA/cm2, 85.4% at 160 mA/cm2, and 84.8% at 200 mA/cm2.

#### 4.2.3 Energy Efficiency

The energy efficiency of the Nafion 212 cell at 25 C ranged from 81.2% at 40 mA/cm2 to 79.7% at 200 mA/cm2, with a maximum of 82.5% observed at 80 mA/cm2. The flatter dependence of EE on current density for Nafion 212, compared to Nafion 117, reflects the competing sensitivities of CE and VE: the more rapidly increasing CE partially compensates for the declining VE, resulting in a relatively stable EE profile.

At 40 C, the Nafion 212 cell achieved EE values of 82.4% at 40 mA/cm2, 83.8% at 80 mA/cm2, 83.2% at 100 mA/cm2, 82.6% at 120 mA/cm2, 81.9% at 160 mA/cm2, and 80.9% at 200 mA/cm2. Notably, the 40 C EE exceeded the 25 C EE across the entire current density range for Nafion 212, whereas this was not uniformly the case for Nafion 117. This difference arises because the thinner Nafion 212 benefits more substantially from the resistance reduction at elevated temperature, and the associated CE penalty is proportionally smaller due to the shorter diffusion pathway.

## 5. Comparative Analysis and Performance Trade-offs

### 5.1 Efficiency Metrics Comparison

A direct comparison of the two membranes reveals a clear performance trade-off that must be navigated in practical VRFB system design. At 100 mA/cm2 and 25 C, Nafion 117 achieved CE of 97.1%, VE of 82.6%, and EE of 80.2%, while Nafion 212 achieved CE of 93.8%, VE of 86.2%, and EE of 80.9%. Although the EE values were remarkably similar, the underlying composition differed substantially: Nafion 117 prioritized coulombic efficiency at the expense of voltage efficiency, while Nafion 212 achieved the converse balance.

The practical implications of this difference depend on the operational priorities of the specific application. Applications requiring high round-trip efficiency and tolerant of modest capacity fade may favor Nafion 212, while applications demanding maximum capacity retention and coulombic efficiency may prefer Nafion 117. The higher CE of Nafion 117 also implies slower rates of capacity degradation over extended cycling, as vanadium crossover is a primary contributor to the capacity fading mechanism in VRFBs.

### 5.2 Current Density Dependence and Optimization

The opposing dependencies of CE and VE on current density create distinct optimization landscapes for the two membranes. For Nafion 117, the EE decreased monotonically with increasing current density at both temperatures, indicating that maximum energy efficiency is achieved at the lowest practical current density. However, the absolute magnitude of the EE decrease was modest (approximately 3.7 percentage points from 40 to 200 mA/cm2), suggesting that operating at higher current densities to reduce stack size and capital cost incurs only a modest efficiency penalty.

For Nafion 212, the EE exhibited a shallow maximum at intermediate current densities, particularly at 40 C where the EE peaked at approximately 83.8% at 80 mA/cm2. This non-monotonic behavior creates an optimal operating window for Nafion 212-based systems, where the competing effects of CE improvement and VE degradation are most favorably balanced.

### 5.3 Temperature Effects and Crossover Dynamics

The dual effect of temperature on VRFB performance was clearly manifested in the experimental results. Higher temperatures improve voltage efficiency through reduced membrane resistance and enhanced electrochemical kinetics, but simultaneously degrade coulombic efficiency through accelerated vanadium crossover. The magnitude of these competing effects differs between the two membranes, leading to distinct temperature sensitivities.

For Nafion 117, the net effect of increasing temperature from 25 C to 40 C on EE was slightly positive at low current densities but diminished at higher current densities. This crossover in temperature dependence reflects the increasing importance of CE degradation relative to VE improvement as the current density increases and the Faradaic-to-crossover current ratio shifts.

For Nafion 212, the net temperature effect on EE was positive across all tested current densities, with the largest improvements observed at intermediate current densities. The more favorable temperature response of Nafion 212 can be attributed to its lower intrinsic resistance, which means that the fractional reduction in resistance upon heating is more significant in absolute terms, while the fractional increase in crossover is moderated by the shorter diffusion pathway.

### 5.4 Degradation Mechanisms and Long-term Implications

Vanadium crossover through the membrane initiates a cascade of degradation processes that limit the long-term cycling stability of VRFBs. When vanadium ions permeate from one half-cell to the other, they create an imbalance in the state of charge between the positive and negative electrolytes. This imbalance manifests as a progressive reduction in the accessible discharge capacity, as the capacity of the full cell becomes limited by the electrolyte side with the lesser amount of active vanadium species.

The self-discharge reaction that occurs when permeated vanadium ions react with counter ions at the opposing electrode represents an additional energy loss mechanism beyond the CE reduction measured during normal cycling. The exothermic nature of these cross-mixing reactions can also create local hotspots within the cell, potentially accelerating further degradation of the membrane and electrode materials.

Given its approximately 50% lower vanadium permeability, Nafion 117 is expected to exhibit substantially slower capacity fade rates during extended cycling compared to Nafion 212. Based on the measured permeability values and the electrolyte volumes employed, the capacity fade rate attributable to vanadium crossover alone is estimated at approximately 0.08% per cycle for Nafion 117 and 0.18% per cycle for Nafion 212 under standard operating conditions at 100 mA/cm2 and 25 C.

## 6. Design Implications and Membrane Selection Criteria

The comprehensive dataset generated in this study enables the formulation of rational membrane selection guidelines for VRFB system designers. The choice between Nafion 117 and Nafion 212 should be guided by the following considerations.

For stationary energy storage applications prioritizing long cycle life and minimal maintenance, Nafion 117 offers superior performance due to its higher coulombic efficiency and reduced vanadium crossover. The associated penalty in voltage efficiency represents an acceptable trade-off when the total cost of ownership is dominated by capacity degradation rather than energy efficiency.

For applications where power density and capital cost are primary drivers, Nafion 212 provides advantages through its lower area-specific resistance, which enables higher operating current densities without excessive ohmic losses. The reduced membrane thickness also translates to lower material costs per unit area.

For high-temperature operation above 35 C, Nafion 212 may be preferred as its voltage efficiency advantage becomes more pronounced and the crossover penalty is partially offset by the shorter diffusion pathway. However, the designer must account for the more rapid capacity fade and implement appropriate electrolyte rebalancing strategies.

## 7. Conclusion

This study has provided a detailed quantitative comparison of Nafion 117 and Nafion 212 membranes in vanadium redox flow batteries across a comprehensive matrix of current densities and temperatures. The results confirm the expected performance trade-off between the thicker Nafion 117, which delivers superior coulombic efficiency (96-98%) and reduced vanadium crossover (1.8 x 10^-7 cm2/s) but at the cost of higher area resistance (1.65 ohm cm2), and the thinner Nafion 212, which achieves higher voltage efficiency (84-88%) and lower resistance (0.85 ohm cm2) but with increased vanadium permeability (3.9 x 10^-7 cm2/s). The opposing dependencies of CE and VE on current density create complex optimization landscapes that are further modulated by temperature effects on both resistance and crossover. These findings establish a rigorous benchmark dataset against which novel membrane materials can be evaluated and provide actionable guidance for membrane selection in practical VRFB system design.
---

# DOC02: Non-Fluorinated Membrane Materials for Vanadium Redox Flow Batteries: Structure-Property-Performance Relationships in PBI, SNPBI, SPEEK, and SPTPC Systems

## Abstract

The development of cost-effective, high-performance membranes represents a critical challenge for the widespread commercialization of vanadium redox flow batteries (VRFBs). While perfluorinated sulfonic acid membranes such as Nafion have served as benchmark materials, their high cost and significant vanadium crossover have motivated extensive research into non-fluorinated alternatives. This study presents a comprehensive evaluation of four non-fluorinated membrane systems for VRFB applications: polybenzimidazole (PBI), sulfonated non-fluorinated polybenzimidazole with ion exchange capacity of 1.42 mmol/g (SNPBI-1.42), sulfonated poly(ether ether ketone) blended with aryl-substituted polyketone (SPEEK/APK), and sulfonated poly(terphenylene piperidinium) with IEC of 2.59 mmol/g (SPTPC-2.59). By systematically correlating ion exchange capacity, area-specific resistance, and vanadium permeability with the resulting coulombic efficiency, voltage efficiency, and energy efficiency across current densities from 40 to 200 mA/cm2, we establish quantitative structure-property-performance relationships that guide rational membrane design for non-fluorinated VRFB separators.

## 1. Introduction

Vanadium redox flow batteries continue to attract significant research attention as a promising technology for large-scale stationary energy storage. The membrane constitutes one of the most critical and costly components of a VRFB system, with the dual requirements of high proton conductivity for low ohmic losses and high ion selectivity for minimal vanadium crossover. Perfluorinated membranes, despite their excellent chemical stability and conductivity, suffer from inherent limitations including high material cost (approximately 500-1000 USD/m2 for Nafion), substantial vanadium permeability, and environmental concerns associated with fluorinated polymer production and disposal.

Non-fluorinated aromatic polymers have emerged as promising alternatives, offering potential advantages in cost, processability, and tunable transport properties. The key design strategy for these materials involves the incorporation of ion-conducting functional groups, primarily sulfonic acid moieties, into aromatic polymer backbones with high chemical stability. By controlling the density and distribution of these functional groups, as quantified by the ion exchange capacity (IEC), researchers can modulate the balance between proton conductivity and vanadium barrier properties.

This study focuses on four representative non-fluorinated membrane systems that span a range of IEC values and chemical architectures. Polybenzimidazole (PBI) represents a baseline non-sulfonated aromatic polymer that relies on acid-base complexation with phosphoric acid for proton conduction. SNPBI-1.42 extends this platform through controlled sulfonation to introduce additional proton-conducting sites. SPEEK/APK represents a blended system combining the well-characterized sulfonated poly(ether ether ketone) with an aryl-substituted polyketone to improve mechanical properties and chemical stability. SPTPC-2.59 represents a high-IEC system based on a rigid terphenylene backbone with piperidinium functional groups, designed to achieve high conductivity while maintaining good dimensional stability.

The relationship between IEC and VRFB performance is complex and non-monotonic. At low IEC values, insufficient proton conductivity leads to high ohmic resistance and consequently poor voltage efficiency. As IEC increases, proton conductivity improves and resistance decreases, but excessive sulfonation can compromise the mechanical integrity of the polymer matrix and increase vanadium permeability by creating overly large and interconnected hydrophilic domains. Understanding this trade-off is essential for identifying optimal IEC ranges and for developing design rules for next-generation non-fluorinated membranes.

## 2. Experimental Methods

### 2.1 Membrane Preparation and Characterization

PBI membranes were prepared by solution casting from 3% PBI (IV = 0.8-0.9 dL/g) in dimethylacetamide onto glass plates, followed by drying at 80 C under vacuum for 24 hours. The resulting membranes were doped in 85% phosphoric acid at room temperature for 7 days to achieve acid doping levels of approximately 5-6 mole H3PO4 per PBI repeat unit.

SNPBI-1.42 membranes were prepared by post-sulfonation of PBI using a mixture of fuming sulfuric acid (30% SO3) and concentrated sulfuric acid at controlled temperature and reaction time to achieve the target IEC of 1.42 mmol/g. The sulfonation degree was verified by titration of the acid-form membranes against standardized NaOH solution.

SPEEK/APK blend membranes were prepared by co-dissolving SPEEK (IEC = 1.8 mmol/g) and APK in N-methyl-2-pyrrolidone (NMP) at a weight ratio of 7:3, followed by solution casting and drying at 60 C under vacuum. The blend membrane achieved an effective IEC of approximately 1.26 mmol/g based on the composition-weighted average.

SPTPC-2.59 membranes were synthesized through polycondensation of 4,4'-dichloro-3,3'-disulfonylterphenylene with N-methylpiperidine, followed by membrane casting from dimethyl sulfoxide solution and ion exchange to the protonated form.

### 2.2 Physicochemical Characterization

Ion exchange capacity was determined by acid-base titration following standard procedures. Membrane samples in the acid form were immersed in 1 M NaCl solution for 24 hours to exchange protons with sodium ions. The released protons were then titrated with 0.01 M NaOH solution using phenolphthalein indicator.

Area-specific resistance was measured by electrochemical impedance spectroscopy (EIS) using a two-electrode cell configuration. Measurements were performed over a frequency range of 1 MHz to 1 Hz with an AC perturbation amplitude of 10 mV. The membrane resistance was determined from the high-frequency intercept of the Nyquist plot with the real axis.

Vanadium permeability was measured using a diffusion cell consisting of two compartments separated by the test membrane. The feed compartment contained 1.5 M VOSO4 in 3 M H2SO4, while the receiving compartment contained 1.5 M MgSO4 in 3 M H2SO4 as a supporting electrolyte to balance ionic strength. Samples were withdrawn from the receiving compartment at regular intervals and the vanadium concentration was determined by UV-Vis spectrophotometry at 765 nm.

Water uptake was determined by measuring the weight difference between fully hydrated membranes (equilibrated in deionized water at 25 C for 24 hours) and vacuum-dried membranes (dried at 80 C for 24 hours).

### 2.3 VRFB Single Cell Testing

Single cell VRFB tests were conducted using an active electrode area of 10 cm2 with carbon felt electrodes (SGL Carbon, GFD 4.6 EA) compressed to 15% of original thickness. The electrolyte consisted of 1.5 M V(II)/V(III) mixed solution in 3 M H2SO4 on the negative side and 1.5 M V(IV)/V(V) mixed solution on the positive side. Electrolyte flow rate was maintained at 40 mL/min throughout all tests.

Galvanostatic charge-discharge tests were performed at current densities of 40, 80, 100, 160, and 200 mA/cm2 with voltage limits of 0.8 V (discharge cutoff) and 1.65 V (charge cutoff). Three cycles were performed at each current density to ensure steady-state performance, and the reported values represent the average of the last two cycles.

## 3. Membrane Physicochemical Properties

### 3.1 Ion Exchange Capacity and Water Uptake

The ion exchange capacities and water uptake values of the four membrane systems are summarized in Table 1. PBI, being a non-sulfonated polymer that relies on acid doping rather than covalently bound acid groups, exhibited the lowest IEC of 0.0 mmol/g as measured by acid-base titration. However, the phosphoric acid doping introduces mobile proton carriers that effectively enable proton conduction through a different mechanism than the sulfonic acid groups in the other membranes.

SNPBI-1.42 exhibited the target IEC of 1.42 mmol/g, achieved through controlled post-sulfonation of the parent PBI. The sulfonation process also increased water uptake to 18%, compared to 12% for the acid-doped PBI baseline.

SPEEK/APK, with an effective IEC of 1.26 mmol/g derived from the 7:3 blend ratio of SPEEK (1.8 mmol/g) and non-sulfonated APK, showed moderate water uptake of 21%. The APK component reduces the overall IEC compared to pure SPEEK but contributes to improved mechanical properties and chemical stability.

SPTPC-2.59 exhibited the highest IEC of 2.59 mmol/g among all tested membranes, reflecting the high density of sulfonic acid groups on the terphenylene backbone combined with the piperidinium cationic groups that create an ionic cross-linked network. The water uptake of 28% was correspondingly the highest among the four systems.

| Membrane | IEC (mmol/g) | Water Uptake (%) | Area Resistance (ohm cm2) | Vanadium Permeability (x 10^-7 cm2/s) |
|---|---|---|---|---|
| PBI | 0.0 | 12 | 2.45 | 0.50 |
| SNPBI-1.42 | 1.42 | 18 | 1.15 | 0.95 |
| SPEEK/APK | 1.26 | 21 | 1.38 | 2.10 |
| SPTPC-2.59 | 2.59 | 28 | 0.82 | 3.20 |

### 3.2 Area-Specific Resistance

The area-specific resistance values showed a strong inverse correlation with IEC. PBI exhibited the highest resistance at 2.45 ohm cm2, reflecting the relatively low proton mobility in the acid-doped system at room temperature. SNPBI-1.42 showed a substantially reduced resistance of 1.15 ohm cm2, demonstrating the effectiveness of covalently bound sulfonic acid groups in providing continuous proton conduction pathways. SPEEK/APK exhibited an intermediate resistance of 1.38 ohm cm2, while SPTPC-2.59 achieved the lowest resistance of 0.82 ohm cm2, benefiting from its high IEC and the additional proton conduction contribution from the piperidinium groups.

The relationship between IEC and area resistance is not strictly linear, as the connectivity and morphology of the hydrophilic domains also play important roles. The transition from isolated hydrophilic clusters to interconnected proton transport channels typically occurs at a critical IEC threshold that depends on the specific polymer architecture. For the aromatic polymer systems studied here, this percolation threshold appears to lie in the range of 1.0-1.3 mmol/g, as evidenced by the significant resistance reduction observed between PBI (effectively zero IEC) and SNPBI-1.42.

### 3.3 Vanadium Permeability

Vanadium permeability showed a positive correlation with IEC, as expected from the increasing size and connectivity of hydrophilic domains that facilitate vanadium ion transport. PBI exhibited the lowest permeability at 0.5 x 10^-7 cm2/s, attributed to its dense aromatic polymer matrix that provides an effective barrier to vanadium ions. SNPBI-1.42 showed a slightly elevated permeability of 0.95 x 10^-7 cm2/s, still substantially lower than commercial Nafion membranes.

SPEEK/APK exhibited a permeability of 2.1 x 10^-7 cm2/s, approaching the range of Nafion 117 (1.8 x 10^-7 cm2/s). The relatively high permeability of this blend system may reflect phase separation between the SPEEK and APK components, creating heterogenous transport pathways. SPTPC-2.59 showed the highest permeability among the non-fluorinated membranes at 3.2 x 10^-7 cm2/s, approaching that of Nafion 212 (3.9 x 10^-7 cm2/s). The high IEC and substantial water uptake of this system create relatively large hydrophilic domains that are less selective against vanadium ion transport.

### 3.4 Structure-Transport Correlations

The trade-off between proton conductivity (inverse of resistance) and vanadium selectivity (inverse of permeability) defines the fundamental performance envelope for VRFB membranes. A selectivity parameter, defined as the ratio of proton conductivity to vanadium permeability, provides a useful figure of merit for comparing different membrane systems.

SNPBI-1.42 exhibited the highest selectivity among the tested non-fluorinated membranes, combining moderate proton conductivity (low resistance of 1.15 ohm cm2) with low vanadium permeability (0.95 x 10^-7 cm2/s). SPTPC-2.59, despite its superior proton conductivity, showed lower selectivity due to its elevated vanadium permeability. PBI achieved high selectivity through extremely low vanadium permeability but at the cost of prohibitively high resistance. SPEEK/APK occupied an intermediate position in the selectivity landscape.

## 4. VRFB Performance Evaluation

### 4.1 Coulombic Efficiency

The coulombic efficiency of all four membranes showed the expected positive correlation with current density, consistent with the fundamental mechanism wherein the parasitic crossover flux becomes a smaller fraction of the total current at higher operational currents.

PBI achieved the highest CE values among all tested membranes, ranging from 98.2% at 40 mA/cm2 to 98.5% at 200 mA/cm2. The exceptionally low vanadium permeability of PBI (0.5 x 10^-7 cm2/s) translates directly into minimal crossover losses and correspondingly high coulombic efficiency. The relatively flat CE profile (increasing by only 0.3 percentage points over the current density range) reflects the already minimal crossover at even the lowest current density.

SNPBI-1.42 achieved CE values of 97.5% at 40 mA/cm2, increasing to 98.4% at 200 mA/cm2. The CE remained consistently high across all current densities, reflecting the favorable balance of moderate IEC and low vanadium permeability. At 100 mA/cm2, the CE was 98.1%, which is competitive with Nafion 117 and superior to Nafion 212.

SPEEK/APK exhibited CE values ranging from 95.8% at 40 mA/cm2 to 97.9% at 200 mA/cm2. The more pronounced CE dependence on current density (2.1 percentage points over the range) reflects the higher vanadium permeability of this membrane system. At 100 mA/cm2, the CE was 96.8%.

SPTPC-2.59 showed the lowest CE among the non-fluorinated membranes, ranging from 95.0% at 40 mA/cm2 to 97.2% at 200 mA/cm2. The higher vanadium permeability (3.2 x 10^-7 cm2/s) associated with its elevated IEC and water uptake directly translates into greater crossover losses, particularly at low current densities where the crossover flux represents a larger fraction of the total current.

### 4.2 Voltage Efficiency

Voltage efficiency exhibited the expected inverse correlation with current density for all membranes, driven by the increasing contribution of ohmic polarization at higher operational currents.

PBI showed the lowest VE values due to its high area-specific resistance of 2.45 ohm cm2. At 40 mA/cm2, the VE was 78.4%, declining to 68.2% at 200 mA/cm2. The steep decline reflects the dominant contribution of ohmic losses in this high-resistance membrane system.

SNPBI-1.42 achieved substantially improved VE compared to PBI, with values of 84.2% at 40 mA/cm2 and 78.5% at 200 mA/cm2. The 5.7 percentage point decline over the current density range is consistent with the moderate resistance of 1.15 ohm cm2. At 100 mA/cm2, the VE was 82.1%.

SPEEK/APK exhibited VE values of 83.1% at 40 mA/cm2, declining to 76.8% at 200 mA/cm2. The resistance of 1.38 ohm cm2 positions this membrane between SNPBI-1.42 and PBI in terms of voltage efficiency. At 100 mA/cm2, the VE was 80.4%.

SPTPC-2.59 achieved the highest VE among all non-fluorinated membranes, with values of 85.6% at 40 mA/cm2 and 80.2% at 200 mA/cm2. The low resistance of 0.82 ohm cm2 enabled this superior voltage efficiency performance. At 100 mA/cm2, the VE was 83.8%, which is competitive with Nafion 212 and superior to Nafion 117.

### 4.3 Energy Efficiency

Energy efficiency, as the product of CE and VE, reflects the combined impact of membrane transport properties on overall VRFB performance.

PBI achieved EE values ranging from 76.8% at 40 mA/cm2 to 66.9% at 200 mA/cm2. Despite the excellent coulombic efficiency, the poor voltage efficiency resulting from high resistance limits the overall energy efficiency, particularly at higher current densities.

SNPBI-1.42 demonstrated the highest EE among all tested non-fluorinated membranes, with values of 82.1% at 40 mA/cm2 and 77.1% at 200 mA/cm2. The optimal balance of high CE and moderate VE creates a favorable efficiency profile across the entire current density range. At 100 mA/cm2, the EE was 80.5%, which exceeds the performance of both Nafion 117 and Nafion 212 under comparable conditions.

SPEEK/APK achieved EE values of 79.6% at 40 mA/cm2 and 74.1% at 200 mA/cm2. At 100 mA/cm2, the EE was 77.9%. The moderate CE and VE values combine to yield acceptable but not outstanding energy efficiency.

SPTPC-2.59 exhibited EE values of 81.3% at 40 mA/cm2 and 78.0% at 200 mA/cm2. At 100 mA/cm2, the EE was 81.4%. The combination of excellent VE and moderate CE yields competitive energy efficiency, though not quite matching SNPBI-1.42 due to the lower coulombic efficiency offsetting the voltage efficiency advantage.

### 4.4 Performance Comparison at 100 mA/cm2

At 100 mA/cm2, which represents a commonly used reference condition for VRFB membrane evaluation, the performance hierarchy among the non-fluorinated membranes is clearly established. SNPBI-1.42 achieved the highest EE at 80.5% (CE 98.1%, VE 82.1%), followed by SPTPC-2.59 at 81.4% (CE 96.3%, VE 83.8%), then SPEEK/APK at 77.9% (CE 96.8%, VE 80.4%), and finally PBI at 71.8% (CE 98.4%, VE 73.0%).

It is noteworthy that both SNPBI-1.42 and SPTPC-2.59 achieve energy efficiency values that meet or exceed the performance of benchmark Nafion membranes under comparable conditions. SNPBI-1.42 achieves this through a balanced CE/VE profile enabled by its optimal selectivity, while SPTPC-2.59 leverages its superior voltage efficiency despite a lower coulombic efficiency.

## 5. Quantitative Structure-Property-Performance Relationships

### 5.1 IEC-Resistance Relationship

The relationship between IEC and area-specific resistance follows a power-law dependence that reflects the percolation behavior of proton transport channels in the polymer matrix. For the systems studied, the resistance decreases approximately as IEC^-1.8 for IEC values above the percolation threshold of approximately 1.0 mmol/g. Below this threshold, resistance increases sharply as the hydrophilic domains become disconnected.

This relationship has important implications for membrane design. Targeting an IEC in the range of 1.2-1.6 mmol/g appears to provide the optimal balance, achieving reasonably low resistance without the excessive vanadium permeability that accompanies higher IEC values. SNPBI-1.42, with its IEC of 1.42 mmol/g, sits near the center of this optimal range.

### 5.2 IEC-Permeability Relationship

Vanadium permeability increases with IEC in a approximately linear fashion for the range studied (0-2.59 mmol/g). The permeability coefficient increases by approximately 1.0-1.3 x 10^-7 cm2/s per mmol/g of IEC above the baseline set by the non-sulfonated polymer matrix. This linear relationship suggests that each additional sulfonic acid group contributes proportionally to the size and connectivity of hydrophilic domains that facilitate vanadium transport.

The ratio of proton conductivity to vanadium permeability, representing membrane selectivity, reaches a maximum in the IEC range of 1.2-1.5 mmol/g. At lower IEC values, the poor proton conductivity dominates the selectivity. At higher IEC values, the rapidly increasing vanadium permeability degrades selectivity despite the improved conductivity.

### 5.3 Resistance-EE and Permeability-EE Correlations

Multiple linear regression analysis of the performance data reveals that energy efficiency at 100 mA/cm2 can be predicted from area resistance and vanadium permeability with good accuracy. The regression coefficients indicate that a 0.1 ohm cm2 increase in area resistance decreases EE by approximately 0.4-0.5 percentage points, while a 1.0 x 10^-7 cm2/s increase in vanadium permeability decreases EE by approximately 0.8-1.0 percentage points. These coefficients quantify the relative importance of resistance versus crossover in determining overall membrane performance.

The resistance contribution to EE loss operates primarily through its effect on voltage efficiency, while the permeability contribution operates primarily through its effect on coulombic efficiency. This mechanistic separation enables rational optimization strategies: for applications where VE is the limiting factor, membrane design should prioritize low resistance even at some cost in permeability, while for applications where CE is critical, permeability minimization should take precedence.

### 5.4 Membrane Selection Guidelines for Non-Fluorinated VRFB Systems

Based on the comprehensive performance evaluation and structure-property analysis, the following selection guidelines are proposed for non-fluorinated VRFB membranes.

For applications requiring maximum energy efficiency across a range of current densities, SNPBI-1.42 represents the optimal choice among the tested membranes. Its balanced transport properties, combining moderate resistance (1.15 ohm cm2) with low vanadium permeability (0.95 x 10^-7 cm2/s), yield the highest energy efficiency (80.5% at 100 mA/cm2) and excellent coulombic efficiency that should translate to favorable long-term cycling stability.

For applications prioritizing maximum voltage efficiency and power density, particularly at high current densities, SPTPC-2.59 offers advantages through its very low resistance (0.82 ohm cm2). However, the higher vanadium permeability (3.2 x 10^-7 cm2/s) may lead to more rapid capacity fade over extended cycling, requiring appropriate electrolyte rebalancing strategies.

PBI, despite its excellent vanadium barrier properties, is not recommended for practical VRFB operation at current densities above 60 mA/cm2 due to its prohibitively high resistance and consequent poor voltage efficiency. Potential applications may be limited to very low current density operation where extremely long cycle life is the overriding priority.

SPEEK/APK occupies a middle position in the performance landscape, offering acceptable but not outstanding efficiency metrics. The primary advantage of this system may lie in its relatively mature processing technology and favorable mechanical properties rather than in peak electrochemical performance.

## 6. Degradation Mechanisms and Long-Term Stability Considerations

### 6.1 Chemical Degradation Pathways

Non-fluorinated aromatic polymers face distinct chemical degradation challenges compared to their perfluorinated counterparts. The primary degradation mechanism involves attack by the strongly oxidizing V(V) species (VO2+) on the aromatic polymer backbone, particularly at electron-rich positions. Sulfonated polymers are additionally susceptible to desulfonation under strongly acidic and oxidative conditions, which progressively reduces IEC and consequently degrades proton conductivity.

The PBI backbone exhibits excellent chemical stability due to the electron-deficient nature of the benzimidazole ring, which is less susceptible to electrophilic attack by V(V) species. However, the phosphoric acid dopant can leach from the membrane during long-term operation, leading to gradual loss of proton conductivity.

The SNPBI-1.42 membrane benefits from the inherent stability of the PBI backbone while introducing sulfonic acid groups for improved conductivity. The sulfonation occurs at the less reactive positions of the phenylene ring, providing reasonable stability against desulfonation. Accelerated degradation testing at elevated temperature (60 C) showed less than 5% IEC loss after 500 hours of immersion in 1.5 M V(V) solution.

### 6.2 Mechanical Degradation

The mechanical stability of non-fluorinated membranes under VRFB operating conditions depends sensitively on their water uptake and swelling behavior. Excessive swelling can lead to dimensional instability, loss of contact with the electrode, and eventual mechanical failure. PBI exhibited the lowest water uptake (12%) and consequently the best dimensional stability. SNPBI-1.42 maintained moderate swelling (18% water uptake) that is compatible with stable long-term operation. SPTPC-2.59, with its 28% water uptake, showed the highest swelling ratio and may require careful control of compression forces in the cell assembly to prevent excessive deformation.

### 6.3 Degradation Chain Analysis

The degradation of non-fluorinated VRFB membranes follows a chain process that initiates with chemical attack on the polymer backbone or pendant acid groups, progresses through loss of ion exchange capacity and/or mechanical integrity, and manifests as declining voltage efficiency and/or increasing vanadium crossover. For SNPBI-1.42, the primary degradation pathway involves gradual desulfonation, which increases resistance and reduces VE over extended cycling. For SPTPC-2.59, backbone degradation may create additional free volume that increases vanadium permeability, leading to declining CE. The SPEEK/APK blend may suffer from phase separation under cycling conditions, compromising both mechanical properties and transport characteristics.

## 7. Conclusion

This study has established comprehensive structure-property-performance relationships for four representative non-fluorinated membrane systems in VRFB applications. The results demonstrate that non-fluorinated membranes can achieve energy efficiency values competitive with or exceeding benchmark Nafion membranes when appropriately designed. SNPBI-1.42 emerges as the most promising candidate, achieving an energy efficiency of 80.5% at 100 mA/cm2 through its optimal balance of low area resistance (1.15 ohm cm2) and low vanadium permeability (0.95 x 10^-7 cm2/s). The quantitative relationships between IEC, resistance, permeability, and energy efficiency provide a framework for rational design of next-generation non-fluorinated VRFB membranes. Future work should focus on long-term cycling stability evaluation under realistic operating conditions and on scaling membrane synthesis and processing to industrially relevant dimensions and throughputs.
---

# DOC03: Enhanced Electrochemical Performance of Vanadium Redox Flow Batteries Through Controlled Surface Modification of Carbon Felt Electrodes

1. Introduction

Vanadium redox flow batteries (VRFBs) have attracted substantial research interest as scalable energy storage systems for grid-level applications. The electrochemical performance of VRFBs is critically dependent on the electrode material, which must simultaneously provide high electrochemical activity for vanadium redox reactions, adequate surface area for reaction sites, and sufficient wettability for electrolyte accessibility. Commercial carbon felt electrodes, while widely adopted due to their favorable cost profile and mechanical stability, suffer from inherent hydrophobicity and limited active surface area, which collectively contribute to elevated charge-transfer resistances and reduced voltage efficiencies.

To address these limitations, surface modification strategies have been extensively investigated. Among these approaches, controlled oxidation and heteroatom doping have demonstrated particular promise in enhancing the hydrophilicity and electrocatalytic activity of carbon-based electrodes. This study systematically evaluates three electrode configurations: untreated commercial carbon felt (C-C), mild acid-etched carbon felt (MC-C), and boron-doped mildly etched carbon felt with subsequent thermal treatment (BMC-C). The progressive modification strategy was designed to isolate the individual contributions of surface roughening, defect generation, and heteroatom doping toward the overall electrochemical performance in a vanadium redox flow battery environment.

2. Experimental Methods

2.1 Electrode Preparation

The C-C electrode was obtained as-received from a commercial carbon felt supplier without any post-treatment. The MC-C electrode was prepared by immersing the commercial carbon felt in a 5.0 mol/L HNO3 solution at 80 C for 6 hours, followed by thorough washing with deionized water and drying at 120 C overnight. The BMC-C electrode was fabricated through a two-step process: first, the commercial carbon felt was subjected to the same HNO3 etching procedure used for MC-C; second, the etched felt was soaked in a boric acid solution (0.3 mol/L) for 2 hours, dried at 80 C, and then heat-treated at 750 C under argon atmosphere for 2 hours to incorporate boron heteroatoms into the carbon lattice.

2.2 Physical Characterization

Surface wettability was assessed through contact angle measurements using a sessile drop method with 2.0 mol/L VOSO4 in 3.0 mol/L H2SO4 electrolyte as the probe liquid. Surface morphology and roughness were examined by scanning electron microscopy and profilometry, with the arithmetic mean roughness (Ra) quantified from three independent measurements on each electrode type. Electrochemical impedance spectroscopy was conducted in a three-electrode configuration with Ag/AgCl reference electrode and platinum counter electrode, using the vanadium electrolyte at open circuit potential over a frequency range of 100 kHz to 10 mHz with 5 mV perturbation amplitude.

2.3 Battery Testing

Single-cell VRFB tests were performed with an active area of 10 cm2. The electrolyte consisted of 1.6 mol/L vanadium in 3.0 mol/L H2SO4 supporting electrolyte, with 40 mL of analyte and catholyte circulated at 40 mL/min using peristaltic pumps. Nafion 117 membrane was employed as the separator. Charge-discharge cycling was conducted at current densities of 50, 100, 200, and 500 mA/cm2 using a battery cycler with voltage cutoffs of 1.65 V (charge) and 0.8 V (discharge). Coulombic efficiency (CE), voltage efficiency (VE), and energy efficiency (EE) were calculated from the measured capacity and voltage profiles.

3. Results and Discussion

3.1 Surface Wettability and Morphology

The contact angle measurements revealed a progressive improvement in hydrophilicity across the three electrode types. The C-C electrode exhibited a contact angle of 130.4 deg, indicating strong hydrophobic character typical of untreated carbon felts. The MC-C electrode showed a substantially reduced contact angle of 102 deg, demonstrating that mild acid etching effectively introduced oxygen-containing functional groups and increased surface polarity. The BMC-C electrode achieved the lowest contact angle of 92.8 deg, suggesting that boron doping further enhanced the surface hydrophilicity through additional polar sites and modified electronic structure. The transition from a hydrophobic to near-hydrophilic surface is expected to facilitate electrolyte penetration into the porous electrode structure and improve ion accessibility to active sites.

Surface roughness analysis provided complementary insights into the morphological changes induced by each treatment step. The C-C electrode displayed a mean roughness Ra of 8.4 um, characteristic of the relatively smooth fiber surfaces of commercial carbon felt. The MC-C electrode exhibited increased roughness with Ra of 11.2 um, confirming that acid etching created surface defects and microporosity on the carbon fibers. The BMC-C electrode showed the highest roughness with Ra of 14.7 um, attributable to the combined effects of acid etching and the structural rearrangement associated with boron incorporation and high-temperature thermal treatment. The progressive increase in surface roughness correlates directly with the expanded electrochemically active surface area available for vanadium redox reactions.

3.2 Charge-Transfer Resistance

Electrochemical impedance spectroscopy measurements quantified the charge-transfer resistance (Rct) associated with the V2+/V3+ and VO2+/VO2+ redox couples. The C-C electrode presented the highest Rct value of 3.82 ohm cm2, reflecting the inherently poor electrocatalytic activity of untreated carbon surfaces toward vanadium redox reactions. The MC-C electrode demonstrated a substantially reduced Rct of 2.17 ohm cm2, representing a 43.2% decrease relative to C-C. This improvement is attributed to the increased surface area and the catalytic effect of oxygen functional groups introduced during acid etching. The BMC-C electrode achieved the lowest Rct of 1.34 ohm cm2, corresponding to a 64.9% reduction compared to C-C and a 38.2% reduction compared to MC-C. The additional decrease in charge-transfer resistance for BMC-C is attributed to the electronic structure modification induced by boron doping, which creates favorable active sites with enhanced adsorption properties for vanadium ions and accelerates the electron transfer kinetics at the electrode-electrolyte interface.

3.3 Coulombic Efficiency

Coulombic efficiency measurements across the tested current densities revealed consistent trends among the three electrode types. At 100 mA/cm2, the C-C electrode achieved a CE of 94%, while the MC-C electrode attained 96%, and the BMC-C electrode reached 97%. The progressive improvement in CE correlates with the enhanced surface properties of the modified electrodes. The higher surface area and improved wettability of MC-C and BMC-C electrodes facilitate more uniform current distribution across the electrode volume, reducing localized overcharge conditions that promote side reactions. Additionally, the increased density of active sites on modified electrodes promotes more complete conversion of vanadium species during charge and discharge, minimizing the residual concentration differences that contribute to capacity loss. The reduced charge-transfer resistance in MC-C and BMC-C also enables the redox reactions to proceed closer to equilibrium potentials, suppressing the parasitic hydrogen and oxygen evolution reactions that degrade coulombic efficiency.

3.4 Voltage Efficiency and Energy Efficiency

Voltage efficiency measurements at 100 mA/cm2 showed marked differences among the three electrode configurations. The C-C electrode exhibited a VE of 70%, consistent with the significant overpotential associated with its high charge-transfer resistance. The MC-C electrode demonstrated improved VE of 77%, reflecting the reduced kinetic limitations achieved through surface roughening and oxygen functionalization. The BMC-C electrode achieved the highest VE of 85%, attributable to the synergistic combination of enhanced surface area, improved wettability, and boron-catalyzed charge-transfer kinetics. The 15 percentage point improvement in VE from C-C to BMC-C represents a substantial enhancement in the voltage utilization efficiency of the cell.

Energy efficiency, as the product of CE and VE, showed corresponding improvements. At 100 mA/cm2, the C-C electrode delivered an EE of 65.8%, calculated from 94% CE and 70% VE. The MC-C electrode achieved an EE of 73.9%, derived from 96% CE and 77% VE. The BMC-C electrode reached an EE of 82.5%, computed from 97% CE and 85% VE. The 16.7 percentage point improvement in EE from C-C to BMC-C underscores the practical significance of the progressive modification strategy for enhancing the round-trip energy storage efficiency of VRFB systems.

3.5 Performance at Varied Current Densities

The electrochemical performance of each electrode type was further characterized across current densities ranging from 50 to 500 mA/cm2. At 50 mA/cm2, all three electrodes showed elevated efficiencies due to reduced kinetic and mass transfer limitations. As current density increased to 200 mA/cm2, the performance gap between the modified and unmodified electrodes widened, with BMC-C maintaining substantially higher VE and EE values compared to C-C. At 500 mA/cm2, the high overpotential on C-C resulted in severe kinetic limitations, while BMC-C continued to exhibit usable efficiency levels. This behavior confirms that the surface modifications provide particular benefit under high-rate operating conditions where charge-transfer kinetics dominate the cell overpotential. The improved performance at elevated current densities is especially relevant for practical applications where high power density operation is desired to reduce system footprint and capital cost.

3.6 Degradation Mechanisms and Stability

Long-term cycling stability was evaluated to assess the durability of the surface modifications. The C-C electrode exhibited gradual performance degradation characterized by increasing overpotential and declining VE over 200 cycles. This degradation pattern is consistent with the progressive oxidation and loss of limited active surface area on untreated carbon felt. The MC-C electrode showed improved stability compared to C-C, though some performance decline was observed after extended cycling, potentially associated with the gradual leaching or reduction of oxygen functional groups under the strongly acidic and oxidizing environment of the positive half-cell. The BMC-C electrode demonstrated the most stable performance, with minimal degradation over 200 cycles. The enhanced stability of BMC-C is attributed to the covalent incorporation of boron into the carbon lattice, which provides more durable catalytic sites compared to surface-bound oxygen functional groups. Furthermore, the improved wettability of BMC-C mitigates the preferential flooding and dry-out phenomena that can cause uneven current distribution and accelerated localized degradation in hydrophobic electrodes.

Vanadium crossover represents another degradation pathway that is influenced by electrode properties. While the membrane primarily controls crossover, the electrode surface chemistry can affect the local concentration polarization and thus the concentration gradient driving crossover. The reduced overpotential on BMC-C decreases the extent of concentration polarization during charge, which modestly reduces the driving force for vanadium ion crossover from the positive to negative half-cell.

3.7 Mechanistic Insights

The systematic comparison of C-C, MC-C, and BMC-C electrodes provides mechanistic insights into the role of surface properties in VRFB electrode performance. The contact angle reduction from 130.4 deg to 92.8 deg demonstrates that both oxygen functionalization and boron doping contribute to hydrophilicity enhancement, with the combined treatment achieving near-complete wetting. The charge-transfer resistance reduction from 3.82 ohm cm2 to 1.34 ohm cm2 reveals that surface area expansion and heteroatom doping have complementary but distinct contributions to electrocatalytic activity. The acid etching primarily increases active surface area and introduces oxygen groups that facilitate vanadium ion adsorption, while boron doping modifies the electronic structure to lower the activation energy for electron transfer between the electrode and vanadium species.

The correlation between surface roughness and electrochemical performance suggests that the increased Ra from 8.4 um to 14.7 um creates additional triple-phase boundaries where the electrode, electrolyte, and reactant species meet. These expanded interfacial zones provide more sites for redox reactions to occur simultaneously, effectively increasing the geometric current density capability of the electrode. The rougher surface also promotes turbulent flow patterns within the porous electrode, enhancing mass transfer of vanadium species to and from active sites.

3.8 Design Implications

The comparative results from this study establish a clear design pathway for optimizing VRFB electrodes. The progression from C-C to MC-C to BMC-C demonstrates incremental and cumulative benefits of successive surface treatments. For cost-sensitive applications, the MC-C treatment offers a favorable balance between performance improvement and processing cost, achieving a 73.9% EE at 100 mA/cm2 with a relatively simple acid etching procedure. For high-efficiency applications, the BMC-C electrode provides state-of-the-art performance with 82.5% EE at 100 mA/cm2, though the additional boron doping and thermal treatment steps increase manufacturing complexity. The design trade-off between performance and cost should be evaluated in the context of specific application requirements, including operating current density, cycle life targets, and system-scale economic models. The results also suggest that further optimization of boron doping concentration and thermal treatment conditions could yield additional performance gains beyond those demonstrated in this study.

4. Conclusion

This study has systematically investigated the effects of progressive surface modification on carbon felt electrode performance in vanadium redox flow batteries. The untreated C-C electrode exhibited hydrophobic characteristics with a contact angle of 130.4 deg, high charge-transfer resistance of 3.82 ohm cm2, and moderate energy efficiency of 65.8% at 100 mA/cm2. Mild acid etching to produce MC-C substantially improved hydrophilicity (contact angle 102 deg), reduced charge-transfer resistance to 2.17 ohm cm2, and increased energy efficiency to 73.9%. The combined boron doping and thermal treatment to produce BMC-C achieved the optimal properties with contact angle of 92.8 deg, charge-transfer resistance of 1.34 ohm cm2, and energy efficiency of 82.5%. The 16.7 percentage point improvement in energy efficiency from C-C to BMC-C demonstrates that coordinated surface engineering strategies can substantially enhance VRFB performance for grid-scale energy storage applications.
---

# DOC04: Comprehensive Investigation of Electrolyte Concentration and Flow-Rate Effects on Vanadium Redox Flow Battery Performance Metrics and System Efficiency

1. Introduction

Vanadium redox flow batteries (VRFBs) represent one of the most promising electrochemical energy storage technologies for large-scale grid applications due to their decoupled energy and power capacity, long cycle life, and inherent safety characteristics. While significant research attention has been directed toward electrode and membrane materials, the electrolyte composition and flow conditions represent equally critical operational parameters that directly influence battery performance, efficiency, and overall system economics. The electrolyte concentration determines the energy density and ionic conductivity of the system, while the flow rate governs mass transfer characteristics, concentration polarization behavior, and pumping energy consumption. Understanding the coupled effects of these parameters is essential for optimizing VRFB operation and designing efficient balance-of-plant systems.

This study presents a systematic investigation of how vanadium concentration, sulfuric acid supporting electrolyte concentration, electrolyte flow rate, and operating current density collectively influence the electrochemical performance of VRFBs. Special emphasis is placed on quantifying the relationship between gross electrochemical efficiency and net system efficiency after accounting for parasitic pumping losses. The experimental design encompasses a broad parameter space that spans practical operating ranges for commercial VRFB systems, enabling the development of comprehensive operational guidelines.

2. Experimental Methods

2.1 Electrolyte Preparation

Vanadium electrolytes were prepared by dissolving VOSO4 in sulfuric acid solutions at specified concentrations. Vanadium concentrations of 1.2, 1.5, 1.6, 1.8, 2.0, and 3.0 mol/L were investigated, with H2SO4 concentrations ranging from 2.0 to 5.0 mol/L. All electrolytes were prepared using deionized water and analytical grade reagents. The electrolytes were fully charged and discharged for three preconditioning cycles prior to data collection to ensure stable electrochemical behavior. For each test condition, 40 mL of analyte and 40 mL of catholyte were employed.

2.2 Battery Assembly and Testing

Single-cell VRFB tests were conducted using graphite felt electrodes with an active area of 10 cm2 and Nafion 117 membrane as the separator. The cell was assembled with PTFE gaskets to ensure proper sealing and compression. Charge-discharge cycling was performed at current densities of 50, 100, and 200 mA/cm2 using an electrochemical workstation with programmable voltage cutoffs of 1.65 V (upper) and 0.8 V (lower). Electrolyte flow rates were controlled using calibrated peristaltic pumps at 10, 20, 40, 60, and 100 mL/min. All tests were conducted at ambient temperature (approximately 25 C).

2.3 Pumping Power and Net Efficiency Calculation

Pumping power consumption was measured using calibrated pressure sensors and flow meters installed at the inlet and outlet of each half-cell. The measured pumping power ranged from 5 mW at the lowest flow rate to 50 mW at the highest flow rate, depending on the flow rate and electrolyte viscosity. Gross energy efficiency was calculated from the ratio of discharge energy to charge energy obtained from the electrochemical cycling data. Net energy efficiency was computed by subtracting the total pumping energy consumption from the discharge energy output prior to calculating the efficiency ratio. This approach provides a realistic assessment of the usable energy efficiency that accounts for parasitic losses in the balance-of-plant system.

3. Results and Discussion

3.1 Effect of Vanadium Concentration on Electrochemical Performance

The vanadium concentration in the electrolyte directly determines the theoretical energy density and influences the ionic conductivity, viscosity, and electrochemical reaction kinetics. Testing across the concentration range from 1.2 to 3.0 mol/L revealed complex trade-offs in performance metrics. At lower concentrations (1.2 mol/L), the reduced viscosity facilitated efficient mass transfer and minimized concentration polarization, contributing to favorable voltage efficiency. However, the lower energy density resulted in reduced capacity utilization and higher relative pumping losses. At 1.5 mol/L, a balance between conductivity and viscosity was observed, with moderate efficiency performance.

The electrolyte with 1.6 mol/L vanadium concentration demonstrated near-optimal overall performance, providing sufficient ionic conductivity for good reaction kinetics while maintaining viscosity at levels that did not excessively impede mass transfer. As concentration increased to 1.8 mol/L, increased viscosity began to noticeably affect flow distribution within the porous electrode and elevate pumping power requirements. At 2.0 mol/L, the viscosity effects became more pronounced, requiring higher flow rates to maintain adequate mass transfer. The highest tested concentration of 3.0 mol/L exhibited significant viscosity-related challenges, including uneven flow distribution and elevated concentration polarization at moderate to high current densities.

3.2 Effect of Sulfuric Acid Concentration

The sulfuric acid concentration serves a dual role as supporting electrolyte and pH regulator, influencing both proton conductivity and vanadium ion stability. Testing at H2SO4 concentrations of 2.0, 3.0, 4.0, and 5.0 mol/L revealed distinct effects on performance. At 2.0 mol/L H2SO4, the limited proton availability restricted the proton-coupled electron transfer reactions that govern vanadium redox processes, resulting in elevated overpotentials and reduced voltage efficiency. The lower acidity also raised concerns regarding the long-term chemical stability of vanadium species, particularly the precipitation of V(V) compounds at elevated temperatures.

At 3.0 mol/L H2SO4, proton conductivity was substantially improved, enabling faster reaction kinetics and lower charge-transfer overpotential. This concentration provided adequate buffering capacity to maintain vanadium ion solubility across the full state-of-charge range. Increasing H2SO4 to 4.0 mol/L further enhanced conductivity but introduced additional viscosity and corrosion considerations. At 5.0 mol/L H2SO4, the highest proton concentration provided excellent conductivity; however, the increased viscosity and aggressive chemical environment presented challenges for membrane durability and long-term component stability. The optimal balance for the tested conditions was observed at 3.0 mol/L H2SO4, which provided favorable conductivity without excessive viscosity or corrosion effects.

3.3 Effect of Flow Rate on Mass Transfer and Efficiency

Electrolyte flow rate represents a critical operating parameter that directly influences mass transfer coefficients, concentration polarization, and pumping energy consumption. Testing across flow rates from 10 to 100 mL/min revealed significant effects on all performance metrics. At the lowest flow rate of 10 mL/min, mass transfer limitations were pronounced, particularly at higher current densities where vanadium species depletion at the electrode surface led to elevated concentration overpotential. This condition resulted in reduced voltage efficiency and premature voltage cutoff during discharge, limiting usable capacity.

At 20 mL/min, mass transfer conditions improved modestly, though concentration polarization remained significant at current densities above 100 mA/cm2. The 40 mL/min flow rate provided a transition point where mass transfer became sufficiently effective to support stable operation at moderate current densities. At 60 mL/min, concentration polarization was substantially mitigated, enabling efficient operation at 200 mA/cm2 with minimal mass transfer losses. The highest tested flow rate of 100 mL/min provided excellent mass transfer conditions with near-negligible concentration polarization, but at the cost of substantially elevated pumping power consumption.

The measured pumping power increased from approximately 5 mW at 10 mL/min to 50 mW at 100 mL/min, following a non-linear relationship with flow rate that reflected both viscous losses and pump efficiency characteristics. This pumping power represents a parasitic energy loss that directly reduces the net energy efficiency of the system, creating a fundamental trade-off between mass transfer enhancement and pumping energy consumption.

3.4 Gross and Net Energy Efficiency Analysis

The gross energy efficiency, representing the pure electrochemical conversion efficiency without pumping losses, was measured across all experimental conditions. Gross EE values ranged from 78% to 87%, with the highest values achieved at moderate vanadium concentrations (1.6 mol/L), optimal H2SO4 concentration (3.0 mol/L), moderate to high flow rates (40-100 mL/min), and lower current densities (50 mA/cm2). At 100 mA/cm2 with the standard electrolyte composition of 1.6 mol/L vanadium in 3.0 mol/L H2SO4 at 40 mL/min, a gross EE of approximately 83% was achieved.

After accounting for pumping power consumption, the net energy efficiency showed a different dependence on operating conditions. Net EE values ranged from 72% to 83%, with the highest net efficiency achieved at conditions that balanced electrochemical performance with moderate pumping losses. Notably, while the highest flow rate of 100 mL/min produced the highest gross EE due to excellent mass transfer, the elevated pumping power reduced the net EE below that achieved at 60 mL/min for most conditions. This demonstrates that maximizing gross electrochemical efficiency does not necessarily maximize net system efficiency.

At 50 mA/cm2, the lower current density reduced both concentration polarization and the relative impact of pumping losses, enabling net EE values at the higher end of the observed range. At 100 mA/cm2, the combination of moderate polarization and manageable pumping losses at 40-60 mL/min produced optimal net efficiency. At 200 mA/cm2, the increased concentration polarization necessitated higher flow rates to maintain efficiency, but the associated pumping costs partially offset the mass transfer benefits.

3.5 Coupled Effects and Optimal Operating Windows

The interaction between vanadium concentration and flow rate revealed important coupled effects. At lower vanadium concentrations (1.2-1.5 mol/L), the reduced viscosity enabled efficient mass transfer even at moderate flow rates, and the relative pumping penalty was higher due to lower energy throughput. At 1.6 mol/L vanadium, the viscosity-flow coupling produced favorable efficiency across a broad flow rate range. At higher concentrations (2.0-3.0 mol/L), the increased viscosity necessitated higher flow rates to prevent performance degradation, but the pumping cost increase partially negated the benefits of higher energy density.

The optimal operating window for achieving net EE above 80% was identified at vanadium concentrations of 1.5-1.8 mol/L, H2SO4 concentration of 3.0 mol/L, flow rates of 40-60 mL/min, and current densities of 50-100 mA/cm2. These conditions provide a practical balance between energy density, electrochemical efficiency, and parasitic losses. For applications prioritizing maximum power density, operation at 200 mA/cm2 with 60-100 mL/min flow rate and 1.6 mol/L vanadium concentration provides acceptable net EE values in the 74-78% range.

3.6 Mass Transfer Coefficient Analysis

Mass transfer coefficients were estimated from the experimental data using concentration polarization analysis. At 10 mL/min, the mass transfer coefficient was insufficient to support the vanadium flux required at 200 mA/cm2, resulting in substantial electrode surface depletion. The mass transfer limitation manifested as a steep decline in cell voltage during constant-current discharge. At 40 mL/min, the mass transfer coefficient increased sufficiently to support stable 100 mA/cm2 operation, though some polarization remained at 200 mA/cm2. At 100 mL/min, the mass transfer coefficient reached levels that effectively eliminated concentration polarization as a significant source of overpotential across all tested current densities.

The relationship between flow rate and mass transfer coefficient followed expected behavior for flow-through porous electrodes, with the mass transfer coefficient approximately proportional to the square root of flow velocity in the laminar regime. This relationship has important implications for system design, as it indicates diminishing returns in mass transfer improvement per unit increase in pumping power at high flow rates.

3.7 Degradation and Stability Considerations

Extended operation under suboptimal flow conditions can induce accelerated degradation mechanisms. At very low flow rates (10 mL/min), the combination of mass transfer limitations and localized overpotential can promote non-uniform current distribution, leading to preferential electrode degradation in regions with highest current density. This non-uniform degradation manifests as gradual capacity loss and increasing ohmic resistance over extended cycling.

At high vanadium concentrations (3.0 mol/L) combined with low H2SO4 concentrations (2.0 mol/L), vanadium precipitation becomes a significant risk during prolonged charge cycles, particularly when the state of charge approaches upper limits. Precipitation not only reduces active material availability but can also physically block flow channels within the porous electrode, further exacerbating mass transfer limitations. The 3.0 mol/L vanadium electrolyte also showed increased susceptibility to thermal precipitation when operating temperatures exceeded 30 C.

High acid concentrations (5.0 mol/L H2SO4) contributed to accelerated membrane degradation through chemical attack of the polymer backbone, resulting in increased vanadium crossover after extended cycling. The elevated vanadium crossover in turn caused capacity fade and self-discharge, further reducing system efficiency. These degradation mechanisms underscore the importance of selecting electrolyte compositions that balance performance with long-term stability.

3.8 System Design Implications

The comprehensive dataset from this study provides quantitative guidance for VRFB system design and operation. For stationary energy storage applications where high round-trip efficiency is prioritized, operation at 1.6 mol/L vanadium in 3.0 mol/L H2SO4 with 40 mL/min flow rate and 100 mA/cm2 current density provides net EE of approximately 80%, representing a favorable compromise between efficiency and power density. For applications where minimizing capital cost is paramount, the higher energy density achievable at 2.0 mol/L vanadium may justify the modest efficiency penalty and increased pumping requirement.

The flow rate optimization represents a critical system design decision, as it directly affects both the electrochemical performance and the balance-of-plant energy consumption. The results demonstrate that net EE peaks at intermediate flow rates and that excessive flow rates designed to maximize gross EE can actually degrade net system performance. Flow distribution engineering within the cell stack also plays a critical role, as maldistribution can create localized regions of insufficient flow that limit overall performance even when average flow rates appear adequate.

4. Conclusion

This systematic investigation has elucidated the complex interdependence of electrolyte concentration, flow rate, and current density on VRFB performance metrics and system-level net efficiency. Gross energy efficiencies ranging from 78% to 87% were measured across the experimental parameter space, with net energy efficiencies of 72% to 83% after accounting for parasitic pumping losses ranging from 5 mW to 50 mW. The optimal operating window for achieving net EE above 80% was identified at vanadium concentrations of 1.5-1.8 mol/L, H2SO4 concentration of 3.0 mol/L, flow rates of 40-60 mL/min, and current densities of 50-100 mA/cm2. These findings provide quantitative design guidelines for maximizing the practical energy efficiency of VRFB systems while accounting for the essential trade-off between mass transfer enhancement and pumping energy consumption.
---

# DOC05: Influence of Operating Temperature on Long-Term Cycling Stability and Capacity Retention in Vanadium Redox Flow Batteries

## Abstract

The vanadium redox flow battery (VRFB) represents one of the most promising electrochemical energy storage technologies for grid-scale applications, owing to its decoupled power and energy capacity, extended cycle life, and inherent safety characteristics. However, the operating temperature exerts profound influence on multiple degradation pathways that collectively determine the long-term performance trajectory of these systems. This study presents a comprehensive experimental investigation into the temperature-dependent behavior of VRFB cells operated at 25 C, 40 C, and 60 C over 500 charge-discharge cycles at a constant current density of 80 mA/cm2. The results demonstrate that elevated temperatures accelerate vanadium ion crossover through the ion-exchange membrane, exacerbate state-of-charge (SOC) imbalance between the positive and negative half-cells, and precipitate more rapid capacity fading. At 25 C, the cell retained 85% of its initial capacity after 500 cycles, whereas capacity retention declined to 74% at 40 C and further to 60% at 60 C. Coulombic efficiency exhibited temperature-dependent degradation from initial values of approximately 97.2% to 94.8% at 25 C, from 97.0% to 92.1% at 40 C, and from 96.8% to 88.5% at 60 C. Vanadium crossover coefficients, determined through spectrophotometric analysis of electrolyte samples, increased from 2.1 x 10^-7 cm2/s at 25 C to 3.8 x 10^-7 cm2/s at 40 C and 6.5 x 10^-7 cm2/s at 60 C. The progressive accumulation of SOC imbalance, quantified as 8% at 25 C, 15% at 40 C, and 24% at 60 C after 500 cycles, was identified as a primary driver of premature capacity loss at elevated temperatures. These findings underscore the necessity of active thermal management strategies for VRFB installations subject to variable ambient conditions and provide quantitative benchmarks for degradation rate modeling in predictive maintenance frameworks.

## 1. Introduction

Vanadium redox flow batteries have garnered substantial research attention over the past two decades as a scalable and durable solution for stationary energy storage. The fundamental architecture of the VRFB employs vanadium ions in four distinct oxidation states-V(II), V(III), V(IV), and V(V)-dissolved in aqueous sulfuric acid electrolyte, with the V2+/V3+ redox couple serving as the negative half-cell reaction and the VO2+/VO2+ couple as the positive half-cell reaction. This unique design, wherein both half-cells utilize the same elemental species, eliminates irreversible cross-contamination that plagues other flow battery chemistries and enables electrolyte rebalancing through remixing procedures.

Despite these architectural advantages, VRFB systems remain susceptible to several degradation mechanisms that manifest over extended cycling intervals. Among these, vanadium ion crossover through the ion-exchange membrane constitutes one of the most consequential long-term degradation pathways. The transport of vanadium species from one half-cell to the other occurs via diffusion, migration, and electro-osmotic convection, with the relative contribution of each mechanism depending on the membrane properties, electrolyte composition, and operational parameters. Temperature, in particular, exerts a multiplicative effect on crossover rates by increasing both the diffusion coefficients of vanadium ions and the ionic conductivity of the membrane.

The consequences of enhanced vanadium crossover extend beyond simple electrolyte loss. The differential rates at which various vanadium oxidation states permeate through the membrane create an imbalance in the state-of-charge between the positive and negative half-cells. This SOC imbalance progressively restricts the accessible capacity window, as one half-cell reaches its limiting state earlier during charge or discharge, effectively reducing the overall system capacity. Over hundreds of cycles, the cumulative effect of this imbalance drives significant capacity fading that can substantially diminish the economic viability of the installation.

Furthermore, elevated temperatures promote side reactions that compromise the Coulombic efficiency of the battery. The hydrogen evolution reaction (HER) at the negative electrode and the oxygen evolution reaction (OER) at the positive electrode become increasingly favorable at higher temperatures, diverting charge current away from the intended redox reactions. The precipitation of V(V) species as V2O5 at the positive electrode, particularly when local temperatures exceed solubility limits, introduces additional capacity loss mechanisms that may be partially irreversible.

This study was designed to isolate and quantify the individual and synergistic effects of operating temperature on VRFB degradation over an extended cycling protocol spanning 500 charge-discharge cycles. By maintaining all other operational parameters constant-including current density at 80 mA/cm2, electrolyte composition at 1.5 M VOSO4 in 3.0 M H2SO4, and electrolyte flow rate at 40 mL/min-we establish a controlled experimental framework wherein observed differences in performance can be confidently attributed to temperature effects. The three temperatures selected-25 C, 40 C, and 60 C-encompass the practical operating range encountered in fielded VRFB systems, from well-conditioned indoor installations to poorly ventilated enclosures or hot-climate deployments.

## 2. Experimental Methods

### 2.1 Cell Assembly and Materials

The VRFB single cells were assembled using commercially available graphite felt electrodes (SGL Carbon GFD 4.6 EA) with a projected geometric area of 10 cm2 and a compressed thickness of 3.5 mm. The felt was thermally treated at 400 C for 6 hours in air to enhance surface wettability and increase the density of oxygen-containing functional groups that serve as active sites for the vanadium redox reactions. Prior to cell assembly, the treated electrodes were characterized by scanning electron microscopy to confirm the preservation of fiber morphology and by contact angle measurements to verify hydrophilic surface characteristics.

Nafion 117 membranes, serving as the separator and proton-conducting medium, were pretreated according to a standard protocol involving sequential immersion in 3% hydrogen peroxide at 80 C for 1 hour, deionized water at 80 C for 1 hour, 0.5 M sulfuric acid at 80 C for 1 hour, and finally deionized water at 80 C for 1 hour. This pretreatment regimen removes organic impurities, converts the membrane to the fully protonated form, and ensures uniform hydration prior to cell assembly. The membrane thickness after pretreatment was measured at 183 um using a micrometer caliper.

The positive and negative electrolytes were prepared by dissolving VOSO4·xH2O (Alfa Aesar, 97% purity) in deionized water and adding concentrated sulfuric acid to achieve a final composition of 1.5 M vanadium species and 3.0 M total sulfate. The electrolyte was fully electrolyzed in a separate conditioning cell to generate equal volumes of V(II) and V(III) solutions for the negative electrolyte and V(IV) and V(V) solutions for the positive electrolyte, ensuring a balanced starting state. Each half-cell electrolyte reservoir contained 50 mL of solution.

Graphite composite bipolar plates with machined serpentine flow fields were employed as current collectors and cell structural elements. The flow field design featured three parallel serpentine channels with a width of 2 mm, depth of 2 mm, and rib width of 1.5 mm, providing a compromise between pressure drop and reactant distribution uniformity.

### 2.2 Electrochemical Testing Protocol

All electrochemical tests were performed using a Bio-Logic VMP-300 potentiostat/galvanostat equipped with a 20 A booster module. The cycling protocol consisted of galvanostatic charge and discharge at a constant current density of 80 mA/cm2, with voltage cutoffs set at 1.65 V for charge termination and 0.8 V for discharge termination. These cutoffs were selected to avoid excessive overcharge that would precipitate V(V) species and over-discharge that would promote hydrogen evolution, while maintaining sufficient capacity utilization for meaningful comparison across temperature conditions.

The electrolyte flow rate was maintained at 40 mL/min per half-cell using peristaltic pumps calibrated by gravimetric flow measurement. Flow was initiated 30 seconds prior to the start of each charge or discharge step to ensure complete wetting of the electrode and flow field, and was terminated 30 seconds after the step completion to prevent unnecessary pumping during rest intervals.

Temperature control was achieved by immersing both electrolyte reservoirs in a programmable circulating water bath with a temperature stability of +/- 0.5 C. The cell assembly itself was housed within an environmental chamber maintained at the target temperature to minimize thermal gradients across the membrane-electrode assembly. Temperature monitoring was performed using Type K thermocouples positioned in each electrolyte reservoir and at the cell inlet and outlet ports.

### 2.3 Analytical Methods

Vanadium crossover coefficients were determined through an ex-situ spectrophotometric method adapted from established literature procedures. At predetermined cycle intervals (cycles 1, 50, 100, 200, and 500), 1 mL samples were withdrawn from both electrolyte reservoirs and analyzed using a UV-visible spectrophotometer (Shimadzu UV-2600). The concentrations of V(II), V(III), V(IV), and V(V) species were quantified by deconvolution of the absorbance spectra at characteristic wavelengths-400 nm, 600 nm, 760 nm, and 850 nm-using a calibration matrix established from standard solutions of known composition. The crossover flux was calculated from the rate of change of vanadium concentration in the receiving half-cell, and the effective diffusion coefficient was computed by normalizing the flux by the membrane area and concentration gradient.

State-of-charge imbalance was quantified by measuring the open-circuit potential of each half-cell against a Ag/AgCl reference electrode inserted into the respective electrolyte reservoir at the end of the 50th, 100th, 200th, and 500th cycles. The SOC of each half-cell was calculated from the measured potential using the Nernst equation with activity coefficients determined from prior calibration. The SOC imbalance was defined as the absolute difference between the positive and negative half-cell SOC values, expressed as a percentage of the full SOC range.

Capacity retention was calculated by normalizing the discharge capacity at each cycle by the initial discharge capacity measured during the first three formation cycles, and expressing the result as a percentage. The Coulombic efficiency (CE) was computed as the ratio of discharge capacity to charge capacity for each cycle, while the voltage efficiency (VE) was calculated as the ratio of the average discharge voltage to the average charge voltage. The energy efficiency (EE) was derived as the product of CE and VE.

Electrochemical impedance spectroscopy (EIS) was conducted at the fully discharged state after cycles 1, 100, and 500 to monitor the evolution of ohmic and charge-transfer resistances. The impedance spectra were recorded over a frequency range of 100 kHz to 10 mHz with an AC perturbation amplitude of 5 mV RMS, and fitted to an equivalent circuit model comprising an ohmic resistance in series with a parallel combination of charge-transfer resistance and constant phase element, followed by a Warburg diffusion element.

## 3. Results and Discussion

### 3.1 Capacity Retention Behavior Across Temperatures

The long-term cycling behavior of VRFB cells operated at 25 C, 40 C, and 60 C revealed pronounced temperature-dependent differences in capacity retention trajectories. At 25 C, the cell demonstrated stable cycling with gradual capacity decline, retaining 85% of the initial discharge capacity after 500 cycles. The fading rate was approximately linear after an initial conditioning period of approximately 50 cycles, during which the capacity increased slightly due to electrode wetting improvement and electrochemical activation of the graphite felt surface.

At 40 C, the capacity retention curve exhibited a more pronounced negative slope, with the cell achieving only 74% capacity retention at cycle 500. The accelerated fading at this temperature became particularly evident after approximately 200 cycles, suggesting the onset of a degradation mechanism that exhibits threshold-like behavior. Post-test analysis of the electrolyte revealed significant redistribution of vanadium species between the half-cells, consistent with enhanced crossover as a primary contributor to the observed capacity loss.

The most severe capacity degradation occurred at 60 C, where capacity retention reached merely 60% after 500 cycles. The fading trajectory at this temperature displayed a distinctly nonlinear character, with the rate of capacity loss increasing progressively throughout the cycling protocol. This acceleration pattern indicates the potential involvement of autocatalytic degradation processes or the accumulation of degradation products that increasingly interfere with the intended electrochemical reactions.

The differential impact of temperature on capacity fading can be partially understood through Arrhenius-type behavior of the underlying degradation reactions. Assuming an Arrhenius relationship between temperature and capacity fading rate, the effective activation energy for the dominant degradation process can be estimated from the relative fading rates at the three temperatures. The data suggest an activation energy in the range of 35-45 kJ/mol, which is consistent with diffusion-controlled vanadium crossover through hydrated ion-exchange membranes and is lower than typical activation energies for electrochemical side reactions such as hydrogen evolution.

### 3.2 Coulombic Efficiency Degradation Patterns

Coulombic efficiency, representing the charge utilization efficiency of the battery, exhibited systematic degradation over the cycling protocol with both temperature-dependent and time-dependent components. At 25 C, the initial CE of 97.2% gradually declined to 94.8% by cycle 500, corresponding to an average loss rate of approximately 0.0048% per cycle. This modest degradation is characteristic of well-operated VRFB systems and reflects the gradual accumulation of minor side reactions and crossover-related charge inefficiencies.

At 40 C, the CE degradation was substantially more pronounced, decreasing from an initial value of 97.0% to 92.1% at cycle 500. The average degradation rate of 0.0098% per cycle represents more than a doubling compared to the 25 C condition. Notably, the degradation curve at 40 C exhibited an inflection point around cycle 200, after which the rate of CE decline accelerated. This behavior correlates with the enhanced crossover rates and the progressive development of SOC imbalance observed at this temperature.

The 60 C condition produced the most severe CE degradation, with values falling from 96.8% to 88.5% over 500 cycles. The average degradation rate of 0.0166% per cycle at this temperature is more than three times that observed at 25 C. The particularly rapid CE decline during the final 200 cycles suggests the emergence of additional side reaction pathways that become significant only at elevated temperatures and extended cycle numbers. The hydrogen evolution reaction, which exhibits strong temperature dependence with typical activation energies of 40-60 kJ/mol, likely contributes to this accelerated CE degradation.

The temperature dependence of CE degradation provides important diagnostic information regarding the dominant loss mechanisms. The relatively modest CE degradation at 25 C, even after 500 cycles, indicates that vanadium crossover at this temperature remains within tolerable limits for many applications. In contrast, the substantially accelerated CE decline at 60 C signals that thermal management is critical for maintaining acceptable round-trip efficiency in practical deployments subject to elevated temperatures.

### 3.3 Vanadium Crossover Coefficients and Transport Mechanisms

The effective vanadium crossover coefficients, determined from spectrophotometric concentration measurements, exhibited strong temperature dependence consistent with activated diffusion behavior. At 25 C, the measured crossover coefficient was 2.1 x 10^-7 cm2/s, which is in good agreement with literature values for Nafion 117 in contact with vanadium electrolyte solutions. This value reflects the combined contributions of diffusive transport driven by concentration gradients, migratory transport driven by the electric field during charge and discharge, and electro-osmotic drag associated with proton transport.

At 40 C, the crossover coefficient increased to 3.8 x 10^-7 cm2/s, representing an 81% increase relative to the 25 C value. This enhancement factor is consistent with the expected temperature dependence of diffusion coefficients in hydrated polymer membranes, which typically increase by a factor of 1.6-2.0 for a 15 C temperature increase. The close correspondence with the expected Arrhenius behavior supports the interpretation that diffusive transport constitutes the dominant crossover mechanism under these operating conditions.

At 60 C, the crossover coefficient reached 6.5 x 10^-7 cm2/s, representing a 210% increase relative to the 25 C baseline and a 71% increase relative to the 40 C value. The particularly steep increase between 40 C and 60 C may reflect not only enhanced diffusivity but also structural changes in the Nafion membrane at elevated temperatures. Nafion undergoes a glass-to-rubber transition in the vicinity of 60-80 C, depending on hydration state, which leads to increased segmental mobility of the polymer backbone and correspondingly larger free volume available for ion transport.

The differential crossover rates among vanadium oxidation states contribute to the development of SOC imbalance. V(V) species, present as the dioxovanadium cation VO2+, exhibit the highest permeability through cation-exchange membranes due to their smaller hydrated radius and lower charge density compared to the more highly charged V(II) and V(III) species. The preferential crossover of V(V) from the positive to the negative half-cell leads to chemical reduction at the negative electrode, effectively constituting an internal short-circuit that discharges the battery without producing external current. Similarly, V(II) species crossing to the positive half-cell undergo oxidation, contributing to the same parasitic discharge process.

### 3.4 State-of-Charge Imbalance and Its Consequences

The progressive development of SOC imbalance between the positive and negative half-cells was quantified through open-circuit potential measurements and represents one of the most consequential manifestations of vanadium crossover for practical battery operation. At 25 C, the SOC imbalance reached 8% after 500 cycles, which, while measurable, has relatively modest impact on the accessible capacity of the battery. This level of imbalance corresponds to approximately 4% of the total vanadium inventory having redistributed between the half-cells.

At 40 C, the SOC imbalance increased to 15% after 500 cycles, nearly double the value observed at 25 C. This level of imbalance begins to significantly constrain the usable capacity window, as the half-cell with excess vanadium in its discharged state reaches its charge limit before the other half-cell can be fully charged. The practical consequence is a reduction in the depth of discharge that can be achieved without encountering voltage cutoff limitations, directly translating to lower energy throughput per cycle.

The most severe SOC imbalance developed at 60 C, reaching 24% after 500 cycles. At this level, nearly one-quarter of the full SOC range is rendered inaccessible due to the mismatch between half-cell states. The cumulative effect of this imbalance, combined with the direct capacity loss due to vanadium inventory redistribution, accounts for the majority of the 40% capacity loss observed at this temperature. The particularly rapid development of SOC imbalance between cycles 200 and 500 at 60 C suggests an accelerating feedback mechanism, wherein increased crossover leads to greater imbalance, which in turn creates larger concentration gradients that drive even faster crossover.

The relationship between SOC imbalance and capacity fading can be understood through a simple volumetric balance analysis. In a perfectly balanced VRFB, both half-cells reach their respective charge and discharge limits simultaneously, maximizing the utilization of the vanadium inventory. As SOC imbalance develops, the limiting half-cell determines the practical capacity of the system. When the imbalance reaches 24%, as observed at 60 C, the theoretical maximum capacity utilization is reduced by approximately 24% even before accounting for other loss mechanisms. The observed 40% capacity loss at 60 C therefore implies that approximately 16% of the initial capacity is lost through mechanisms other than SOC imbalance, including direct vanadium inventory depletion through precipitation or side reactions.

### 3.5 Voltage Efficiency and Polarization Behavior

Voltage efficiency, defined as the ratio of average discharge voltage to average charge voltage, exhibited relatively modest temperature dependence compared to the Coulombic efficiency and capacity metrics. The initial VE values were approximately 83.5% at 25 C, 82.0% at 40 C, and 80.2% at 60 C. The slight decrease in VE with increasing temperature reflects the temperature dependence of the equilibrium cell potential, which decreases by approximately 0.6 mV per degree Celsius due to the negative entropy change of the overall cell reaction.

Over the course of 500 cycles, the voltage efficiency at 25 C decreased by approximately 2.5 percentage points, reaching 81.0% at cycle 500. This decline is primarily attributable to the gradual increase in ohmic resistance as the membrane undergoes chemical degradation and the electrodes experience surface modification. At 40 C, the VE decline was more pronounced at approximately 4.0 percentage points, while at 60 C the decrease reached 6.0 percentage points. The accelerated VE degradation at elevated temperatures likely reflects enhanced membrane degradation, increased electrode polarization due to surface fouling, and the development of concentration polarization due to uneven electrolyte utilization associated with SOC imbalance.

Electrochemical impedance spectroscopy measurements conducted at cycles 1, 100, and 500 provided additional insight into the evolution of cell resistances. At all three temperatures, the ohmic resistance component remained relatively stable, increasing by less than 10% over the cycling protocol. In contrast, the charge-transfer resistance exhibited more substantial growth, particularly at 60 C where it increased by approximately 35% over 500 cycles. This behavior suggests that electrode surface degradation, rather than membrane ohmic losses, constitutes the dominant contributor to VE degradation at elevated temperatures.

### 3.6 Degradation Mechanism Analysis and Interactions

The comprehensive dataset generated in this study enables a mechanistic analysis of the interactions among the various degradation pathways active in VRFB systems. At the foundational level, vanadium crossover through the ion-exchange membrane serves as the primary driver of multiple secondary degradation processes. The direct consequence of crossover is the chemical reaction of permeating vanadium species with the electrolyte in the receiving half-cell, leading to partial self-discharge that reduces the Coulombic efficiency. The differential crossover rates among vanadium oxidation states produce the SOC imbalance that progressively restricts the accessible capacity.

At 25 C, the relatively low crossover coefficient of 2.1 x 10^-7 cm2/s limits the rate at which these degradation processes develop. Over 500 cycles, the cumulative vanadium crossover amounts to approximately 4-5% of the total vanadium inventory, consistent with the observed 8% SOC imbalance and 15% capacity fading. The side reactions contributing to CE degradation at this temperature are relatively minor, with the majority of the CE decline attributable to crossover-induced self-discharge rather than independent electrochemical side reactions.

At 40 C, the increased crossover coefficient of 3.8 x 10^-7 cm2/s approximately doubles the rate of vanadium inventory redistribution. The SOC imbalance of 15% after 500 cycles at this temperature represents a significant operational constraint, reducing the accessible capacity window and accelerating the apparent capacity fading. Additionally, the elevated temperature promotes hydrogen evolution at the negative electrode, which becomes progressively more severe as the SOC imbalance drives the negative half-cell to increasingly negative potentials during charge in an attempt to compensate for the mismatch.

At 60 C, the crossover coefficient of 6.5 x 10^-7 cm2/s produces vanadium transport rates that approach the practical limit for acceptable long-term operation. The resulting SOC imbalance of 24% severely constrains the usable capacity, while the cumulative effect of crossover-induced self-discharge and direct electrochemical side reactions drives the CE below 90%. The particularly nonlinear character of the degradation curves at this temperature suggests the emergence of synergistic interactions among degradation mechanisms, wherein the products of one degradation process catalyze or accelerate other degradation pathways.

One such synergistic interaction involves the coupling between vanadium crossover and hydrogen evolution. As V(V) species cross to the negative half-cell, they are reduced to V(IV) and subsequently to lower oxidation states, consuming protons in the process. The resulting local pH increase at the negative electrode shifts the equilibrium potential for hydrogen evolution to more negative values, effectively increasing the overpotential required to drive the parasitic reaction. However, the increased temperature simultaneously reduces the activation overpotential for hydrogen evolution, partially offsetting this mitigating effect. The net result is a complex temperature-dependent balance between crossover-driven and thermally-driven side reactions.

Another important interaction involves the coupling between SOC imbalance and precipitation of vanadium species. The SOC imbalance creates situations where one half-cell is driven to extreme SOC values during charge or discharge, producing local vanadium concentrations that may exceed solubility limits. At the positive electrode, high SOC during charge elevates the V(V) concentration, which exhibits lower solubility than other vanadium oxidation states and can precipitate as V2O5 solid phase. This precipitation not only removes active material from the electrolyte but can also physically block electrode pores and membrane surfaces, further accelerating degradation.

### 3.7 Cycle-Resolved Degradation Metrics

The cycle-resolved analysis of degradation metrics provides temporal detail that complements the summary statistics presented above. At 25 C, the capacity fading exhibited three distinct phases: an initial activation phase during cycles 1-20 where capacity increased by approximately 2-3%, a linear fading phase during cycles 20-400 with a nearly constant fading rate of 0.03% per cycle, and a slightly accelerated phase during cycles 400-500 where the fading rate increased marginally to 0.05% per cycle. The CE degradation at this temperature followed a similarly structured pattern, with gradual decline throughout the protocol and modest acceleration in the final 100 cycles.

At 40 C, the capacity fading curve displayed a more pronounced acceleration pattern. After an initial activation period similar to that observed at 25 C, the fading rate increased progressively from approximately 0.04% per cycle during cycles 20-100 to 0.06% per cycle during cycles 100-300 and further to 0.08% per cycle during cycles 300-500. This acceleration pattern is consistent with the progressive development of SOC imbalance, wherein the capacity constraint imposed by the mismatch becomes increasingly severe as the imbalance grows. The CE degradation at 40 C exhibited a corresponding acceleration, with the rate of CE decline approximately doubling after cycle 200.

At 60 C, the acceleration pattern was most pronounced, with the capacity fading rate increasing from 0.06% per cycle during cycles 20-100 to 0.10% per cycle during cycles 100-300 and reaching 0.15% per cycle during the final 200 cycles. This progressively steepening degradation curve suggests the operation of multiple feedback mechanisms that amplify the primary degradation processes. The CE degradation at this temperature exhibited a similarly nonlinear character, with particularly rapid decline during cycles 300-500 that coincided with the emergence of visible precipitation in the positive electrolyte reservoir.

The crossover coefficients, measured at discrete cycle intervals, also exhibited temporal evolution that provides insight into membrane degradation processes. At 25 C, the crossover coefficient increased by approximately 15% between cycle 1 and cycle 500, suggesting modest membrane degradation. At 40 C, the increase was approximately 30%, while at 60 C the crossover coefficient nearly doubled over the cycling protocol. This progressive increase in crossover coefficient, beyond the initial temperature effect, indicates that the membrane undergoes chemical and/or physical degradation during extended operation at elevated temperatures, with the degradation rate itself being temperature-dependent.

### 3.8 Implications for System Design and Thermal Management

The experimental results presented in this study carry significant implications for the design and operation of VRFB systems in practical applications. The quantitative relationship between operating temperature and degradation rates provides a foundation for optimizing thermal management strategies that balance the capital cost of cooling systems against the operational benefit of extended battery lifetime.

For indoor installations with controlled ambient temperatures, the data suggest that maintaining the electrolyte temperature at or below 25 C can achieve capacity retention of 85% over 500 cycles, corresponding to an effective calendar life of approximately 2-3 years for a daily cycling application. Under these conditions, the rate of capacity fading is sufficiently gradual that electrolyte rebalancing interventions at intervals of 200-300 cycles may be adequate to maintain acceptable performance.

For outdoor installations subject to seasonal temperature variations or for systems without active cooling, the accelerated degradation at 40 C implies that capacity retention may fall below 75% within the same cycling period. Such systems would benefit from more frequent electrolyte rebalancing, perhaps every 100-150 cycles, and may require electrolyte replacement or major refurbishment after 500-800 cycles depending on the acceptable capacity threshold.

Operation at 60 C, which may occur in poorly ventilated enclosures or hot-climate deployments without air conditioning, produces degradation rates that seriously compromise the economic viability of the VRFB installation. With capacity retention reaching only 60% after 500 cycles and CE declining below 90%, such systems would require frequent maintenance intervention and may experience total cost of ownership that exceeds competing storage technologies. These findings strongly support the inclusion of active thermal management as a standard component of VRFB system design, rather than treating it as an optional accessory.

The trade-off between thermal management energy consumption and battery lifetime optimization represents an important system-level optimization problem. Based on the measured degradation rates, a simple lifetime cost analysis suggests that the energy penalty associated with maintaining electrolyte temperature at 25 C rather than 40 C is economically justified for cycling applications with more than one daily cycle, while the benefit of cooling from 40 C to 25 C may be marginal for infrequently cycled backup power applications.

## 4. Conclusions

This study has presented a comprehensive experimental investigation of temperature effects on VRFB degradation over 500 charge-discharge cycles at operating temperatures of 25 C, 40 C, and 60 C. The key findings can be summarized as follows:

The capacity retention after 500 cycles decreased monotonically with increasing temperature, achieving 85% at 25 C, 74% at 40 C, and 60% at 60 C. This temperature-dependent capacity fading is primarily driven by vanadium crossover through the ion-exchange membrane, with crossover coefficients increasing from 2.1 x 10^-7 cm2/s at 25 C to 3.8 x 10^-7 cm2/s at 40 C and 6.5 x 10^-7 cm2/s at 60 C.

Coulombic efficiency degradation followed a similar temperature dependence, declining from initial values of 97.2%, 97.0%, and 96.8% to final values of 94.8%, 92.1%, and 88.5% at 25 C, 40 C, and 60 C respectively. The progressive accumulation of SOC imbalance, reaching 8%, 15%, and 24% at the three temperatures after 500 cycles, served as a primary driver of premature capacity loss by constraining the accessible capacity window.

The degradation mechanisms active at elevated temperatures include enhanced vanadium crossover driven by increased ion diffusivity, accelerated hydrogen evolution at the negative electrode, and potential precipitation of V(V) species at the positive electrode. These mechanisms exhibit synergistic interactions that produce nonlinear degradation acceleration, particularly at 60 C where the fading rate increased progressively throughout the cycling protocol.

These quantitative results provide essential input data for predictive degradation models and inform the design of thermal management strategies for fielded VRFB installations. The strong temperature dependence of degradation rates underscores the importance of active thermal control for achieving the extended operational lifetimes required for grid-scale energy storage applications.
---

# DOC06: Kinetic Enhancement of Chromium Redox Reactions and Hydrogen Evolution Suppression in Iron-Chromium Redox Flow Batteries via Bi3+ Electrolyte Additive

## Abstract

The iron-chromium redox flow battery (ICRFB) represents a potentially cost-effective alternative to vanadium-based systems for large-scale energy storage, utilizing abundant and inexpensive active materials. However, the sluggish kinetics of the Cr(III)/Cr(II) redox couple at the negative electrode and competing hydrogen evolution reaction (HER) have historically limited the achievable energy efficiency and operational current density of ICRFB systems. This study investigates the application of Bi3+ ions as an electrolyte additive to simultaneously accelerate the Cr(III)/Cr(II) electron transfer kinetics and suppress parasitic hydrogen evolution in ICRFB cells. Through systematic variation of Bi3+ concentration from 0.5 to 5.0 mmol/L and operational evaluation at current densities ranging from 40 to 160 mA/cm2, we demonstrate that Bi3+ additive at optimized concentrations enables substantial performance improvements. Without Bi3+, the baseline cell exhibited a Coulombic efficiency of 72% and energy efficiency of 51% at 80 mA/cm2. With Bi3+ addition, Coulombic efficiency improved to the range of 87-96% and energy efficiency reached 62-85% depending on the specific concentration and current density. The Cr(III)/Cr(II) reaction rate constant increased from 2.1 x 10^-3 cm/s to 4.8 x 10^-3 cm/s in the presence of the optimized Bi3+ concentration, while the parasitic hydrogen evolution loss decreased from 13% to 3.5% of the total charge passed, corresponding to an HER overpotential shift of +85 mV. The mechanisms underlying these improvements involve the underpotential deposition of metallic bismuth on the graphite felt electrode surface, which provides catalytically active sites for the chromium redox reaction while increasing the kinetic barrier for proton reduction. These findings establish Bi3+ electrolyte addition as a facile and effective strategy for addressing the fundamental kinetic limitations of ICRFB systems and advancing their competitiveness for grid-scale energy storage.

## 1. Introduction

Redox flow batteries have emerged as leading candidates for stationary energy storage applications requiring discharge durations of 4-12 hours and operational lifetimes exceeding 15 years. Among the various flow battery chemistries under development, the iron-chromium system offers distinctive advantages related to material abundance and cost. Iron and chromium are among the most plentiful transition metals in the Earth's crust, with raw material costs approximately two orders of magnitude lower than vanadium on a per-mole basis. The ICRFB employs the Fe(III)/Fe(II) redox couple in the positive half-cell with a standard potential of +0.77 V versus SHE, and the Cr(III)/Cr(II) couple in the negative half-cell with a standard potential of -0.41 V versus SHE, yielding a theoretical cell voltage of 1.18 V.

Despite these compelling economic and thermodynamic attributes, the practical deployment of ICRFB systems has been hindered by two interrelated technical challenges. The first challenge concerns the intrinsically sluggish electron transfer kinetics of the Cr(III)/Cr(II) couple on conventional carbon-based electrodes. The Cr(III) aqua complex, [Cr(H2O)6]3+, exhibits particularly slow outer-sphere electron transfer due to the substantial reorganization energy associated with the change in metal-ligand bond distance upon reduction to the [Cr(H2O)6]2+ state. This kinetic limitation manifests as high activation overpotential at practical current densities, resulting in low voltage efficiency and constraining the maximum operational current density to values well below those achievable in VRFB systems.

The second challenge involves the hydrogen evolution reaction (HER), which competes directly with the Cr(III)/Cr(II) reduction for electrons at the negative electrode. The standard potential for hydrogen evolution in acidic media (0 V versus SHE) is substantially more positive than the Cr(III)/Cr(II) potential (-0.41 V versus SHE), rendering the HER thermodynamically favored. On untreated carbon electrodes, which exhibit relatively low HER overpotential, a significant fraction of the charge current is diverted to hydrogen gas generation rather than chromium reduction. This parasitic process reduces the Coulombic efficiency, introduces safety concerns related to hydrogen accumulation, and creates pH gradients in the negative electrolyte that can destabilize the chromium species.

Previous approaches to addressing these challenges have included thermal activation of graphite felt electrodes to increase surface oxygen functional groups, catalytic surface modification using noble metals such as palladium and gold, and the development of advanced electrode structures with enhanced surface area. While these strategies have demonstrated varying degrees of success, many involve complex processing steps, expensive materials, or limited durability that constrain their practical applicability.

The use of metal ion additives dissolved directly in the electrolyte represents an alternative approach with potential advantages in terms of processing simplicity and scalability. Additive species that deposit on the electrode surface during operation can create in-situ catalytic layers without requiring separate electrode modification steps. Bismuth species have been identified as particularly promising candidates due to the high hydrogen evolution overpotential on metallic bismuth surfaces and the established electrochemistry of bismuth underpotential deposition on carbon substrates.

This study presents a comprehensive investigation of Bi3+ addition to ICRFB electrolyte, spanning a concentration range from 0.5 to 5.0 mmol/L and operational current densities from 40 to 160 mA/cm2. The work addresses three primary objectives: (1) quantifying the kinetic enhancement of the Cr(III)/Cr(II) redox reaction in the presence of Bi3+, (2) characterizing the suppression of parasitic hydrogen evolution achieved through Bi3+ addition, and (3) establishing the relationship between Bi3+ concentration, operational current density, and full-cell performance metrics including Coulombic efficiency, voltage efficiency, and energy efficiency.

## 2. Experimental Methods

### 2.1 Electrolyte Preparation and Characterization

The ICRFB electrolyte was prepared by dissolving CrCl3·6H2O (Sigma-Aldrich, 99% purity) and FeCl3 (Sigma-Aldrich, 97% purity) in deionized water with addition of concentrated hydrochloric acid to achieve a supporting electrolyte concentration of 1.0 M HCl. The positive electrolyte contained 1.0 M FeCl3 and 0.5 M FeCl2 (pre-reduced by reaction with metallic iron powder), while the negative electrolyte contained 1.0 M CrCl3 and 0.1 M CrCl2 (pre-reduced electrochemically in a conditioning cell). The supporting electrolyte composition was selected to provide adequate ionic conductivity while maintaining chromium and iron species in their soluble chloride complexes.

Bi3+ additive was introduced into the negative electrolyte as BiCl3 (Alfa Aesar, 99.9% purity) at concentrations of 0.5, 1.0, 1.5, 2.0, 3.0, and 5.0 mmol/L. BiCl3 exhibits moderate solubility in aqueous chloride media through formation of chloro-bismuth complexes such as [BiCl4]- and [BiCl5]2-, with solubility increasing at the HCl concentrations employed in this study. The negative electrolyte was prepared fresh for each Bi3+ concentration to avoid aging effects, and was purged with nitrogen for 30 minutes prior to cell assembly to minimize dissolved oxygen.

The electrolyte pH was measured before and after each experimental run using a calibrated glass electrode pH meter. The conductivity of each electrolyte formulation was determined at 25 C using a four-electrode conductivity cell. Viscosity measurements were performed using a rotational viscometer at controlled temperature to assess the potential impact of Bi3+ addition on mass transport characteristics.

### 2.2 Cell Assembly and Electrode Materials

The ICRFB single cells were assembled with a geometric electrode area of 10 cm2, using graphite felt electrodes (SGL Carbon GFD 4.6 EA) with a nominal thickness of 4.0 mm and compressed to 75% of the nominal thickness during cell assembly. The graphite felt was thermally activated at 450 C for 5 hours in air prior to use, a treatment known to increase surface oxygen functional groups and enhance wettability. The mass of graphite felt in each electrode compartment was approximately 0.8 g, providing a specific surface area of approximately 0.5 m2/g as determined by nitrogen adsorption measurements.

A microporous polyethylene separator (Celgard 2500) with a thickness of 25 um and porosity of 55% was employed as the membrane between the positive and negative half-cells. This separator was selected based on its low cost, chemical stability in chloride electrolyte, and low hydraulic permeability that minimizes bulk electrolyte crossover while permitting ionic transport. The separator was soaked in the respective electrolyte for 24 hours prior to cell assembly to ensure complete wetting and equilibration.

Graphite composite bipolar plates with single-pass serpentine flow fields were used as current collectors. The flow field featured two parallel serpentine channels with 1.5 mm width and 1.5 mm depth, providing balanced pressure drop and uniform flow distribution. Silicone gaskets with a thickness of 1.5 mm defined the cell geometry and prevented external leakage.

The cell was assembled using stainless steel endplates with uniform bolt tightening to a compressive pressure of approximately 0.5 MPa on the active area. The cell compression was verified through thickness measurements of the assembled cell stack.

### 2.3 Electrochemical Characterization Protocol

Cyclic voltammetry (CV) was performed on the negative half-cell using a three-electrode configuration with the graphite felt working electrode, a Ag/AgCl (3 M KCl) reference electrode, and a platinum wire counter electrode. CV measurements were conducted over a potential range from -0.9 V to -0.3 V versus Ag/AgCl at scan rates of 5, 10, 20, 50, and 100 mV/s. The peak current densities and peak separations were extracted from the voltammograms to assess the reversibility and kinetics of the Cr(III)/Cr(II) couple in the presence and absence of Bi3+.

The Cr(III)/Cr(II) apparent reaction rate constant was determined using the Nicholson method, which relates the peak separation in cyclic voltammetry to the dimensionless kinetic parameter psi. The diffusion coefficient of Cr(III) in the electrolyte was independently determined from the Randles-Sevcik analysis of the peak current versus square root of scan rate relationship, and was used as an input parameter for the kinetic analysis.

Hydrogen evolution characteristics were evaluated through linear sweep voltammetry on the graphite felt electrode in the negative electrolyte with and without Bi3+ additive. The potential was scanned from the open-circuit potential in the negative direction to -1.2 V versus Ag/AgCl at a scan rate of 1 mV/s. The Tafel slope and exchange current density for hydrogen evolution were extracted from the linear region of the Tafel plot constructed from the voltammetric data. The overpotential required to achieve a specific hydrogen evolution current density was used as a quantitative metric for comparing HER activity.

Galvanostatic charge-discharge cycling was performed at current densities of 40, 80, 120, and 160 mA/cm2 using voltage cutoffs of 1.3 V for charge and 0.3 V for discharge. These cutoffs were selected to avoid overcharge that would promote oxygen evolution at the positive electrode and over-discharge that would exacerbate hydrogen evolution at the negative electrode. The cycling protocol consisted of at least 50 charge-discharge cycles at each current density and Bi3+ concentration combination to ensure stable performance before recording the reported efficiency values.

The Coulombic efficiency was calculated as the ratio of discharge capacity to charge capacity. The voltage efficiency was computed as the ratio of average discharge voltage to average charge voltage. The energy efficiency was determined as the product of Coulombic efficiency and voltage efficiency. The parasitic hydrogen evolution loss was estimated from the difference between 100% and the Coulombic efficiency, corrected for minor contributions from other side reactions, and was validated by gas chromatographic analysis of the headspace gas from the negative electrolyte reservoir.

### 2.4 Post-Operative Analysis

After completion of the electrochemical testing, the graphite felt electrodes were carefully removed from the cell, rinsed with deionized water, and dried under vacuum for subsequent surface analysis. Scanning electron microscopy (SEM) with energy-dispersive X-ray spectroscopy (EDS) was employed to characterize the surface morphology and elemental composition, with particular attention to the presence and distribution of bismuth on the electrode surface.

X-ray photoelectron spectroscopy (XPS) was performed on selected electrode samples to determine the chemical state of bismuth deposited on the surface and to quantify the relative surface concentrations of bismuth, carbon, oxygen, and other relevant elements. The XPS spectra were deconvoluted using reference binding energy values for metallic bismuth (Bi 4f7/2 at 157.0 eV) and bismuth oxide species (Bi 4f7/2 at 159.5 eV).

The electrolyte samples collected before and after cycling were analyzed by inductively coupled plasma optical emission spectroscopy (ICP-OES) to determine the concentrations of chromium, iron, and bismuth species. These measurements provided information on the stability of Bi3+ in the electrolyte and the extent of crossover of active species between half-cells during operation.

## 3. Results and Discussion

### 3.1 Baseline Performance without Bi3+ Additive

The baseline ICRFB cell, operated without Bi3+ additive in the negative electrolyte, exhibited performance characteristics consistent with literature reports for iron-chromium systems using untreated graphite felt electrodes. At a current density of 40 mA/cm2, the cell achieved a Coulombic efficiency of 85%, a voltage efficiency of 68%, and an energy efficiency of 58%. The Coulombic efficiency below 100% reflects primarily the parasitic hydrogen evolution reaction at the negative electrode, where proton reduction competes with the thermodynamically less favorable Cr(III) reduction.

At 80 mA/cm2, the baseline cell performance declined significantly, with Coulombic efficiency dropping to 72% and energy efficiency to 51%. The reduction in Coulombic efficiency with increasing current density is characteristic of systems where the parasitic HER exhibits lower activation overpotential than the desired chromium reduction reaction. As the current density increases, the electrode potential shifts to more negative values to drive the chromium reduction, but this more negative potential simultaneously accelerates the HER, resulting in a disproportionate increase in parasitic current.

At 120 mA/cm2, the Coulombic efficiency further decreased to 63% and the energy efficiency to 43%, while at 160 mA/cm2 the cell became difficult to operate in a stable manner with Coulombic efficiency below 55% and energy efficiency around 35%. These baseline results confirm the fundamental limitation imposed by the kinetic mismatch between the Cr(III)/Cr(II) couple and the HER on conventional carbon electrodes, and establish the performance benchmarks against which the Bi3+ additive effects are evaluated.

The parasitic hydrogen evolution loss estimated from the Coulombic efficiency deficit corresponded to approximately 8% of the total charge passed at 40 mA/cm2, increasing to 13% at 80 mA/cm2, 19% at 120 mA/cm2, and over 25% at 160 mA/cm2. Gas chromatographic analysis of the headspace above the negative electrolyte reservoir confirmed hydrogen as the primary gaseous product, validating the assignment of the Coulombic efficiency loss to the HER.

### 3.2 Effect of Bi3+ Concentration on Coulombic Efficiency

The addition of Bi3+ to the negative electrolyte produced systematic improvements in Coulombic efficiency across all tested current densities. At 80 mA/cm2, the baseline Coulombic efficiency of 72% increased progressively with Bi3+ concentration, reaching 87% at 0.5 mmol/L, 91% at 1.0 mmol/L, 93% at 1.5 mmol/L, 94% at 2.0 mmol/L, 95% at 3.0 mmol/L, and 96% at 5.0 mmol/L. This monotonic increase in CE with Bi3+ concentration demonstrates the effectiveness of bismuth species in suppressing parasitic hydrogen evolution.

The relationship between Bi3+ concentration and Coulombic efficiency exhibited a diminishing returns pattern, with the incremental improvement decreasing at higher concentrations. The largest single increment occurred between the baseline (0 mmol/L) and 0.5 mmol/L Bi3+, where the CE increased by 15 percentage points. Between 0.5 and 1.0 mmol/L, the improvement was 4 percentage points, and between 1.0 and 1.5 mmol/L, the improvement was 2 percentage points. At concentrations above 2.0 mmol/L, the incremental CE gains were modest, with only 1-2 percentage points improvement between each concentration step.

This diminishing returns pattern is consistent with a surface coverage model wherein Bi3+ deposits on the graphite felt electrode to form a catalytic layer, and the coverage approaches saturation as the concentration increases. At low concentrations, the deposition is incomplete and increasing concentration leads to substantial additional surface coverage. At higher concentrations, the surface becomes nearly saturated with deposited bismuth and further increases in bulk concentration produce only marginal increases in surface coverage and catalytic effect.

The current density dependence of the Bi3+ effect was also investigated. At 40 mA/cm2, the baseline CE of 85% increased to 96% with 1.5 mmol/L Bi3+ and reached 98% at 5.0 mmol/L. At 120 mA/cm2, the baseline CE of 63% increased to 87% with 1.5 mmol/L Bi3+ and reached 92% at 5.0 mmol/L. At 160 mA/cm2, the baseline CE below 55% increased to 80% with 1.5 mmol/L Bi3+ and reached 87% at 5.0 mmol/L. The consistent pattern across current densities indicates that Bi3+ addition provides benefits over a broad operational range, with particularly significant relative improvements at higher current densities where the baseline performance is most severely limited by hydrogen evolution.

### 3.3 Effect of Bi3+ Concentration on Energy Efficiency

The energy efficiency improvements achieved through Bi3+ addition exceeded those predicted from Coulombic efficiency gains alone, indicating that Bi3+ also enhances the voltage efficiency by reducing the activation overpotential of the chromium redox reaction. At 80 mA/cm2, the baseline energy efficiency of 51% increased to 62% at 0.5 mmol/L Bi3+, 70% at 1.0 mmol/L, 76% at 1.5 mmol/L, 80% at 2.0 mmol/L, 83% at 3.0 mmol/L, and 85% at 5.0 mmol/L.

The energy efficiency improvement of 34 percentage points between baseline and 5.0 mmol/L Bi3+ at 80 mA/cm2 comprises contributions from both enhanced Coulombic efficiency (+24 percentage points) and enhanced voltage efficiency (+10 percentage points). The voltage efficiency component reflects the catalytic effect of deposited bismuth on the kinetics of the Cr(III)/Cr(II) couple, which reduces the activation overpotential required to achieve the target current density and thereby increases the average discharge voltage relative to the average charge voltage.

At 40 mA/cm2, the energy efficiency improved from the baseline of 58% to 78% with 1.5 mmol/L Bi3+ and reached 82% at 5.0 mmol/L. At 120 mA/cm2, the energy efficiency improved from the baseline of 43% to 68% with 1.5 mmol/L Bi3+ and reached 75% at 5.0 mmol/L. At 160 mA/cm2, the energy efficiency improved from below 35% to 58% with 1.5 mmol/L Bi3+ and reached 68% at 5.0 mmol/L. These results demonstrate that Bi3+ addition enables operation at current densities previously considered impractical for ICRFB systems while maintaining acceptable energy efficiency.

The optimal Bi3+ concentration for energy efficiency depends on the target current density and the relative importance of maximizing efficiency versus minimizing additive cost. At current densities up to 80 mA/cm2, 1.5-2.0 mmol/L Bi3+ provides a favorable balance, achieving 76-80% energy efficiency with a modest additive concentration. At higher current densities, 3.0-5.0 mmol/L may be justified to maintain energy efficiency above 70%. Concentrations above 5.0 mmol/L were not investigated due to solubility limitations and the diminishing returns observed in the concentration range studied.

### 3.4 Kinetic Enhancement of Cr(III)/Cr(II) Redox Reaction

Cyclic voltammetry measurements on the negative half-cell revealed substantial changes in the Cr(III)/Cr(II) redox behavior upon Bi3+ addition. In the absence of Bi3+, the cyclic voltammogram exhibited a cathodic peak corresponding to Cr(III) reduction and an anodic peak corresponding to Cr(II) oxidation, with a peak separation of 380 mV at a scan rate of 10 mV/s. This large peak separation indicates quasi-reversible to irreversible electron transfer kinetics, consistent with the known sluggishness of the hexa-aqua chromium redox couple.

Upon addition of 1.5 mmol/L Bi3+, the peak separation decreased to 220 mV at the same scan rate, indicating substantially enhanced electron transfer kinetics. The peak current density also increased by approximately 35%, suggesting that the deposited bismuth catalytically facilitates the chromium redox reaction. Further increases in Bi3+ concentration to 3.0 and 5.0 mmol/L produced additional modest reductions in peak separation to 190 mV and 170 mV respectively.

The apparent reaction rate constant for the Cr(III)/Cr(II) couple was determined from the scan-rate-dependent peak separation using the Nicholson method. In the absence of Bi3+, the rate constant was determined to be 2.1 x 10^-3 cm/s, which is consistent with literature values for the Cr(III)/Cr(II) couple on glassy carbon and graphite electrodes in acidic chloride media. With 1.5 mmol/L Bi3+, the rate constant increased to 4.8 x 10^-3 cm/s, representing a 2.3-fold enhancement. This kinetic enhancement translates directly into reduced activation overpotential during galvanostatic operation, contributing significantly to the observed improvement in voltage efficiency.

The relationship between Bi3+ concentration and the rate constant exhibited a saturation profile similar to that observed for the Coulombic efficiency. At 0.5 mmol/L, the rate constant was 3.2 x 10^-3 cm/s. At 1.0 mmol/L, it increased to 4.2 x 10^-3 cm/s. At 2.0 mmol/L, the value was 5.1 x 10^-3 cm/s, and at 5.0 mmol/L, it reached 5.8 x 10^-3 cm/s. The diminishing incremental kinetic enhancement at higher concentrations is again consistent with progressive surface coverage saturation.

### 3.5 Hydrogen Evolution Suppression Mechanism

The suppression of parasitic hydrogen evolution by Bi3+ addition was quantified through multiple complementary techniques. Linear sweep voltammetry on the graphite felt electrode in the negative electrolyte revealed a pronounced shift in the hydrogen evolution characteristics upon Bi3+ addition. In the absence of Bi3+, the HER onset potential was approximately -0.55 V versus Ag/AgCl, and the current density attributable to hydrogen evolution reached 10 mA/cm2 at an overpotential of -0.35 V relative to the reversible hydrogen potential in the electrolyte.

With 1.5 mmol/L Bi3+ in the electrolyte, the HER onset potential shifted to approximately -0.72 V versus Ag/AgCl, corresponding to an overpotential shift of +85 mV at a given current density. This shift reflects the increased kinetic barrier for proton reduction on the bismuth-modified electrode surface compared to the bare graphite surface. Metallic bismuth is well-known for its high hydrogen evolution overpotential, a property that has been exploited in various electrochemical applications including sensors and electroanalytical devices.

The Tafel analysis of the HER data yielded Tafel slopes of 118 mV/decade in the absence of Bi3+ and 142 mV/decade with 1.5 mmol/L Bi3+. The increase in Tafel slope suggests a change in the HER mechanism, possibly reflecting the transition from a Volmer-Heyrovsky mechanism on the graphite surface to a more kinetically hindered Volmer-Tafel mechanism or a purely Volmer-controlled process on the bismuth surface. The exchange current density for hydrogen evolution decreased from 2.8 x 10^-6 A/cm2 on bare graphite to 1.1 x 10^-6 A/cm2 on the bismuth-modified surface, confirming the reduced intrinsic HER activity.

The parasitic hydrogen evolution loss during galvanostatic cycling, estimated from the Coulombic efficiency deficit, decreased from 13% at 80 mA/cm2 without Bi3+ to 3.5% with 1.5 mmol/L Bi3+. This 9.5 percentage point reduction in parasitic loss represents a 73% relative decrease in hydrogen evolution. The remaining 3.5% parasitic loss likely reflects hydrogen evolution occurring at uncovered regions of the graphite felt surface where bismuth deposition is incomplete, as well as minor contributions from other side reactions such as oxygen reduction at the negative electrode.

Gas chromatographic analysis of the headspace gas from the negative electrolyte reservoir during cycling confirmed the substantial reduction in hydrogen evolution rate. Without Bi3+, hydrogen was detected at concentrations corresponding to an evolution rate of 0.35 mL/min during charge at 80 mA/cm2. With 1.5 mmol/L Bi3+, the hydrogen evolution rate decreased to 0.09 mL/min, in good agreement with the reduction predicted from the Coulombic efficiency improvement.

### 3.6 Surface Characterization of Bi-Modified Electrodes

Post-operative analysis of the graphite felt electrodes provided direct evidence for bismuth deposition and insights into the surface morphology and chemical state of the deposited layer. Scanning electron micrographs of the electrode cycled with Bi3+-containing electrolyte revealed the presence of small metallic particles dispersed across the carbon fiber surfaces. The particle size distribution was bimodal, with a population of fine particles in the 20-50 nm range and a smaller population of larger aggregates in the 100-300 nm range. In contrast, the electrode cycled without Bi3+ additive showed clean carbon fiber surfaces without particulate deposits.

Energy-dispersive X-ray spectroscopy confirmed the presence of bismuth on the electrode surface, with a surface atomic concentration of approximately 3.5% on the electrode cycled with 1.5 mmol/L Bi3+. The bismuth signal was uniformly distributed across the analyzed area, suggesting that the electrolyte flow during cell operation facilitates uniform deposition throughout the electrode volume. Trace amounts of chromium were also detected on the electrode surface, consistent with adsorption or precipitation of chromium species during operation.

X-ray photoelectron spectroscopy provided detailed information on the chemical state of the deposited bismuth. The Bi 4f spectrum exhibited a doublet with the Bi 4f7/2 component at 157.2 eV and the Bi 4f5/2 component at 162.5 eV. These binding energies are characteristic of metallic bismuth (Bi 0), confirming that the deposited species is in the elemental form rather than as Bi3+ oxide or chloride. The absence of significant intensity at higher binding energies (159-160 eV for Bi 4f7/2) indicates that oxidation of the deposited bismuth during cell operation or post-operative handling is minimal.

The mechanism of bismuth deposition is attributed to underpotential deposition (UPD) followed by possible bulk deposition at more negative potentials encountered during cell operation. Bismuth UPD on carbon substrates occurs at potentials positive of the Nernst potential for Bi3+/Bi, and involves the reduction of Bi3+ to metallic bismuth that adsorbs on favorable surface sites. During the charge half-cycle of ICRFB operation, the negative electrode potential reaches values sufficiently negative to drive both the UPD process and bulk bismuth deposition, resulting in gradual accumulation of a catalytic bismuth layer over multiple cycles.

### 3.7 Durability and Stability Considerations

The durability of the Bi3+ additive effect was evaluated through extended cycling tests at 80 mA/cm2. With 1.5 mmol/L Bi3+, the cell maintained stable energy efficiency of 75-76% over 200 cycles with less than 2 percentage points variation. The Coulombic efficiency remained in the range of 92-93% throughout the extended cycling protocol. These results indicate that the deposited bismuth layer remains stable and catalytically active over extended operation, without significant dissolution or deactivation.

Analysis of the electrolyte by ICP-OES after 200 cycles revealed that approximately 60% of the initial Bi3+ remained in the negative electrolyte, with the remaining 40% having deposited on the electrode surface or been lost through minor crossover to the positive half-cell. The bismuth concentration in the positive electrolyte was below the detection limit of 0.01 mmol/L, indicating minimal crossover of bismuth species through the separator. This stability is important for practical applications, as it suggests that periodic replenishment of Bi3+ at extended intervals may be sufficient to maintain the catalytic effect.

The long-term stability of the bismuth catalyst layer itself was assessed by interrupting the cycling after 200 cycles, replacing the Bi3+-containing electrolyte with fresh electrolyte without Bi3+, and continuing cycling for an additional 50 cycles. The energy efficiency remained at approximately 74% during this post-replacement period, only 2 percentage points below the value with Bi3+-containing electrolyte. This result indicates that the deposited bismuth layer provides a persistent catalytic effect even after removal of the Bi3+ source from the electrolyte, and that the primary function of maintaining Bi3+ in the electrolyte is to replenish any minor catalyst loss that may occur over extended operation.

Potential concerns regarding the toxicity and environmental impact of bismuth species are mitigated by the relatively low concentrations employed and the low toxicity of bismuth compounds compared to heavy metals such as lead or cadmium. Bismuth and its compounds are classified as low-toxicity materials, and bismuth subsalicylate is widely used in pharmaceutical applications. Nevertheless, appropriate containment and recycling procedures should be implemented in practical ICRFB systems utilizing Bi3+ additive.

### 3.8 Comparative Analysis and Performance Benchmarking

The performance improvements achieved through Bi3+ addition place the ICRFB system within competitive reach of other flow battery technologies. At 80 mA/cm2 with 1.5 mmol/L Bi3+, the energy efficiency of 76% approaches the values typically reported for VRFB systems operating under similar conditions, although the voltage efficiency component remains lower due to the intrinsically lower cell voltage of the ICRFB (1.18 V theoretical versus 1.26 V for VRFB). The Coulombic efficiency of 93% with Bi3+ compares favorably with VRFB values of 95-97%, indicating that the parasitic reaction suppression is highly effective.

The comparison with other ICRFB electrode modification strategies provides context for evaluating the Bi3+ approach. Thermal activation of graphite felt at 400-500 C typically improves energy efficiency by 5-8 percentage points, primarily through increased surface area and wettability, but does not address the fundamental kinetic limitation or HER competition. Catalytic modification using palladium nanoparticles has achieved energy efficiency improvements of 15-20 percentage points, but involves expensive noble metal loadings that compromise the cost advantage of the ICRFB chemistry. The Bi3+ additive approach achieves comparable or superior efficiency improvements (25-34 percentage points at optimized concentrations) while utilizing an inexpensive and abundant additive that is introduced through simple electrolyte formulation.

The cost analysis of Bi3+ addition reveals that the incremental material cost is modest relative to the overall system cost. At a concentration of 1.5 mmol/L in a 1000 L negative electrolyte reservoir, the required BiCl3 quantity is approximately 470 g, costing approximately $50-100 at current commercial prices. This represents less than 1% of the total electrolyte cost and less than 0.1% of the total system cost for a utility-scale installation. The performance improvement of 25 percentage points in energy efficiency translates to substantially increased energy throughput over the system lifetime, providing a highly favorable return on the additive investment.

### 3.9 Mechanistic Insights and Theoretical Framework

The dual catalytic effect of Bi3+ addition-on Cr(III)/Cr(II) kinetics and HER suppression-can be understood within a unified mechanistic framework. The deposition of metallic bismuth on the graphite felt electrode creates a modified surface with distinct catalytic properties compared to the bare carbon substrate. The bismuth surface presents different adsorption energetics for the reactants involved in both the desired chromium redox reaction and the parasitic hydrogen evolution reaction.

For the Cr(III)/Cr(II) couple, the bismuth surface may facilitate the electron transfer through several mechanisms. The adsorption of Cr(III) species on the bismuth surface could proceed through an inner-sphere pathway that bypasses the slow outer-sphere reorganization associated with the hexa-aqua complex. Alternatively, the bismuth surface may provide electronic states that enable more facile electron tunneling between the electrode and the chromium redox center. The observed increase in the apparent rate constant from 2.1 x 10^-3 cm/s to 4.8 x 10^-3 cm/s is consistent with either mechanism and represents a substantial kinetic enhancement.

For the HER, the bismuth surface is intrinsically less catalytic than the graphite surface due to the weaker binding energy of hydrogen atoms on bismuth. The hydrogen evolution reaction on metallic surfaces typically follows a Volmer step (proton discharge to adsorbed hydrogen atoms) followed by either a Tafel recombination step or a Heyrovsky electrochemical desorption step. The relatively weak Bi-H bond impedes the Volmer step, requiring more negative potentials to achieve comparable hydrogen evolution rates. The measured +85 mV shift in HER overpotential and the reduction in exchange current density by a factor of 2.5 are consistent with this mechanism.

The coexistence of catalytic effects for chromium reduction and anti-catalytic effects for hydrogen evolution on the same bismuth surface represents a fortunate convergence that is not generally observed for other metal additives. Many catalytic metals that accelerate the Cr(III)/Cr(II) reaction, such as palladium and platinum, simultaneously accelerate the HER due to their strong hydrogen binding energies, resulting in minimal net improvement in Coulombic efficiency. Bismuth occupies a unique position in the catalytic landscape, providing the desired kinetic selectivity that simultaneously enhances the target reaction and suppresses the parasitic competitor.

## 4. Conclusions

This study has demonstrated that Bi3+ electrolyte additive provides a facile, cost-effective, and highly effective approach to addressing the fundamental kinetic limitations of iron-chromium redox flow batteries. The principal findings are as follows:

The addition of Bi3+ at concentrations of 0.5-5.0 mmol/L to the negative electrolyte substantially improves both Coulombic efficiency and energy efficiency across the operational current density range of 40-160 mA/cm2. At 80 mA/cm2, the energy efficiency improved from a baseline of 51% without Bi3+ to 62-85% depending on the Bi3+ concentration, with the optimal concentration of 1.5-2.0 mmol/L achieving 76-80% energy efficiency.

The Cr(III)/Cr(II) apparent reaction rate constant increased from 2.1 x 10^-3 cm/s to 4.8 x 10^-3 cm/s upon addition of 1.5 mmol/L Bi3+, representing a 2.3-fold kinetic enhancement that reduces activation overpotential and improves voltage efficiency. Parasitic hydrogen evolution was suppressed from 13% to 3.5% of the total charge passed at 80 mA/cm2, corresponding to an HER overpotential shift of +85 mV that reflects the intrinsically low catalytic activity of metallic bismuth toward proton reduction.

The mechanism involves underpotential deposition of metallic bismuth on the graphite felt electrode during cell operation, forming a stable catalytic layer that provides the desired kinetic selectivity. Post-operative characterization confirmed the presence of metallic bismuth in the zero oxidation state, uniformly distributed across the carbon fiber surfaces.

Extended cycling tests demonstrated stable performance over 200 cycles with less than 2 percentage points variation in energy efficiency, indicating that the bismuth catalyst layer is durable under ICRFB operating conditions. The Bi3+ additive approach compares favorably with alternative electrode modification strategies, achieving comparable or superior performance improvements without the use of expensive noble metals or complex processing steps.

These results position the ICRFB with Bi3+ additive as a technologically viable and economically attractive option for grid-scale energy storage, narrowing the performance gap with vanadium-based systems while preserving the substantial raw material cost advantage that motivates the development of iron-chromium chemistry.
---

# DOC07: Degradation Mechanisms in Zinc-Bromine Flow Batteries: Crossover, Complexation, and Dendrite Formation

## Abstract

Zinc-bromine flow batteries (ZBFBs) represent one of the most technologically mature hybrid redox flow battery systems, offering high theoretical energy density and relatively low material costs. However, prolonged cycling operation reveals multiple interconnected degradation pathways that collectively limit system lifetime and commercial viability. This study systematically investigates the principal degradation mechanisms in ZBFBs, including bromine crossover through microporous separators, the role of N-methylethylpyrrolidinium bromide (MEP) complexing agent in mitigating self-discharge, and zinc dendrite growth at the negative electrode. Through controlled experiments spanning current densities from 20 to 80 mA/cm2 and MEP concentrations from 0 to 0.5 M, we establish quantitative relationships between operating conditions and performance decay. Results demonstrate that bromine crossover rates range from 0.03 to 0.16 mL/h depending on current density and separator properties, while zinc dendrite growth rates between 0.6 and 3.0 um/cycle directly correlate with zinc utilization efficiency, which degrades from 72% to 55% over extended cycling. These findings provide a mechanistic framework for designing improved electrolyte formulations and cell architectures that address the coupled degradation phenomena in ZBFB systems.

## 1. Introduction

The zinc-bromine flow battery has attracted significant research attention as a grid-scale energy storage technology due to its high theoretical specific energy of 430 Wh/kg, the abundance of both zinc and bromine precursors, and the well-established electrochemical chemistry derived from the zinc-bromine galvanic couple. The fundamental cell reaction involves the deposition and dissolution of metallic zinc at the negative electrode and the reversible conversion between bromide ions and elemental bromine at the positive electrode. During charge, zinc metal plates onto the conductive substrate while bromide ions are oxidized to bromine, which is subsequently complexed with a quaternary ammonium salt to form an immiscible polybromide oil phase. During discharge, these reactions proceed in the reverse direction, releasing stored electrochemical energy.

Despite these attractive features, the zinc-bromine chemistry suffers from several intrinsic degradation pathways that compromise long-term operational stability. The high solubility of bromine in aqueous electrolytes facilitates transport across the separator membrane, leading to bromine crossover and direct chemical reaction with deposited zinc. This crossover-induced self-discharge represents a primary capacity loss mechanism that manifests as reduced coulombic efficiency, particularly at low current densities where the electrochemical reaction rate cannot outcompete diffusive transport. Meanwhile, the non-uniform electrodeposition of zinc from aqueous bromide electrolytes promotes dendritic morphologies that can penetrate the separator and induce internal short circuits. The growth rate and morphology of these zinc dendrites are strongly dependent on current density, electrolyte composition, and the presence of additives that modulate nucleation and surface diffusion kinetics.

The introduction of complexing agents, most notably N-methylethylpyrrolidinium bromide (MEP), has proven effective in sequestering elemental bromine as a dense polybromide complex phase, thereby reducing the concentration of free bromine available for crossover. However, the concentration of MEP must be carefully optimized, as insufficient complexing capacity fails to fully suppress bromine activity while excessive concentrations increase electrolyte viscosity and ohmic resistance, degrading voltage efficiency and overall energy efficiency. Understanding the interplay between these competing factors is essential for developing next-generation ZBFB systems with extended cycle life.

This work presents a comprehensive experimental study of ZBFB degradation mechanisms across a range of operating conditions. We examine the individual and synergistic effects of current density (20-80 mA/cm2), MEP complexing agent concentration (0-0.5 M), and cycle number (up to 200 cycles) on key performance metrics including coulombic efficiency, energy efficiency, zinc utilization, bromine crossover rate, and dendrite growth kinetics. The resulting dataset enables quantitative correlation of operating parameters with degradation rates and provides mechanistic insights for rational electrolyte and cell design.

## 2. Experimental Methods

### 2.1 Cell Configuration and Assembly

All experiments were conducted in a laboratory-scale zinc-bromine flow cell with an active electrode area of 10 cm2. The positive electrode consisted of a carbon felt substrate (SGL GFD 4.6 EA, 4.6 mm thickness) compressed to 3.0 mm between titanium current collectors and a polyethylene frame. The negative electrode employed a copper-clad graphite plate with a surface-treated carbon layer to promote uniform zinc nucleation. A microporous polyethylene separator (Daramic, 200 um thickness, 55% porosity) was used as the cell separator, providing ionic conductivity while limiting bulk mixing of positive and negative electrolytes. The electrolyte reservoir on each side contained 50 mL of aqueous solution circulated at 100 mL/min using peristaltic pumps.

### 2.2 Electrolyte Preparation

The baseline electrolyte consisted of 2.0 M ZnBr2 dissolved in deionized water with varying concentrations of MEP complexing agent. Four electrolyte formulations were prepared with MEP concentrations of 0 M, 0.1 M, 0.3 M, and 0.5 M. The electrolyte pH was adjusted to 2.0 using HBr to minimize zinc hydroxide precipitation and hydrogen evolution side reactions. All electrolyte solutions were degassed with argon for 30 minutes prior to cell assembly to eliminate dissolved oxygen.

### 2.3 Electrochemical Testing Protocol

Galvanostatic charge-discharge cycling was performed using a Bio-Logic VMP3 potentiostat/galvanostat operating in battery cycling mode. Cells were charged to a capacity limit corresponding to 25% of theoretical zinc deposition capacity (defined as 50% state of charge) and discharged to a lower voltage cutoff of 1.0 V. Current densities of 20, 40, 60, and 80 mA/cm2 were applied symmetrically during charge and discharge. Cycling experiments were conducted for 50, 100, or 200 cycles depending on the experimental condition. Between cycles, a 10-second rest period was imposed to allow electrolyte equilibration.

Coulombic efficiency (CE) was calculated as the ratio of discharge capacity to charge capacity. Voltage efficiency (VE) was determined from the ratio of average discharge voltage to average charge voltage. Energy efficiency (EE) was computed as the product of CE and VE. Zinc utilization was defined as the ratio of the practical discharge capacity to the theoretical capacity based on total zinc content in the electrolyte. Ohmic resistance was measured through electrochemical impedance spectroscopy at open circuit potential with a 10 mV amplitude sinusoidal perturbation over frequencies from 100 kHz to 10 mHz.

### 2.4 Degradation Quantification Methods

Bromine crossover rate was quantified by collecting aliquots from the negative electrolyte reservoir at regular intervals during extended cycling and titrating with sodium thiosulfate to determine accumulated bromine concentration. The crossover rate was expressed as the volume-normalized rate of bromine accumulation in mL/h, calibrated against standard bromine solutions.

Zinc dendrite growth rate was measured through post-mortem analysis of the negative electrode after defined cycle numbers. Cells were carefully disassembled, and the deposited zinc morphology was examined using scanning electron microscopy (SEM) at multiple locations across the electrode surface. The maximum dendrite protrusion length was measured from the planar electrode substrate to the dendrite tip, and the growth rate was expressed as um per cycle by normalizing to the number of completed cycles.

## 3. Results and Discussion

### 3.1 Effect of Current Density on Base Performance Metrics

The influence of current density on ZBFB performance was first established using the baseline electrolyte containing 0.3 M MEP. At a current density of 20 mA/cm2, the system achieved a coulombic efficiency of 85.3%, a voltage efficiency of 75.2%, and an energy efficiency of 64.1%. The relatively low CE at this current density reflects the significant bromine crossover that occurs when the electrochemical reaction rate is slow relative to diffusive transport across the separator. Increasing the current density to 40 mA/cm2 improved CE to 88.7% while VE decreased to 71.4%, yielding an EE of 63.3%. The CE improvement arises from enhanced bromine consumption at the positive electrode, reducing the concentration gradient driving crossover. At 60 mA/cm2, CE reached 90.5% with VE at 68.9% and EE at 62.4%. The highest current density of 80 mA/cm2 produced the maximum CE of 92.1% but the lowest VE of 65.8%, resulting in an EE of 60.6%. These results demonstrate the fundamental CE-VE tradeoff in ZBFB operation, where higher current densities suppress crossover-mediated self-discharge but incur greater ohmic and activation overpotentials.

The ohmic resistance measured under these conditions ranged from 1.55 ohm cm2 at 20 mA/cm2 to 1.28 ohm cm2 at 80 mA/cm2. The decrease in apparent ohmic resistance at higher current densities is attributed to improved wetting of the carbon felt electrode surface and enhanced ionic transport in the convective flow regime, though concentration polarization effects become increasingly significant at elevated currents.

### 3.2 Effect of MEP Complexing Agent Concentration

The concentration of MEP complexing agent was systematically varied to assess its impact on bromine management and overall cell performance at a fixed current density of 40 mA/cm2. In the absence of MEP (0 M), the cell exhibited a CE of only 82.4%, a VE of 76.8%, and an EE of 63.3%. The low CE in this formulation directly reflects substantial bromine crossover and self-discharge, as elemental bromine remains highly mobile in the free state. Addition of 0.1 M MEP improved CE to 86.1% while slightly reducing VE to 74.5%, yielding an EE of 64.1%. The CE improvement confirms the effectiveness of MEP in sequestering bromine as the less mobile polybromide complex. At the optimal 0.3 M MEP concentration, CE reached 88.7%, VE was 71.4%, and EE was 63.3%. Further increasing MEP to 0.5 M produced marginal CE gains to 89.4% but caused a more pronounced VE reduction to 69.2%, with EE declining to 61.9%. The deterioration in VE at high MEP concentration is attributed to increased electrolyte viscosity, which reduces ionic conductivity and enhances concentration polarization during both charge and discharge.

The bromine crossover rate exhibited a strong inverse correlation with MEP concentration. Without MEP, the crossover rate was 0.14 mL/h, reflecting rapid bromine transport through the separator. At 0.1 M MEP, the rate decreased to 0.10 mL/h. The 0.3 M formulation reduced crossover to 0.07 mL/h, and the 0.5 M formulation achieved the lowest rate of 0.05 mL/h. These results confirm that MEP complexation effectively reduces the chemical potential of free bromine, thereby diminishing the driving force for diffusive crossover.

### 3.3 Zinc Utilization and Its Degradation During Extended Cycling

Zinc utilization represents the fraction of total available zinc that participates in the reversible electrochemical reaction and serves as a sensitive indicator of cumulative degradation. At 40 mA/cm2 with 0.3 M MEP, the initial zinc utilization after 10 cycles was 72.1%, indicating relatively efficient zinc deposition and dissolution morphology. However, extended cycling revealed progressive degradation of zinc utilization, which declined to 68.4% at 50 cycles, 63.7% at 100 cycles, and 58.2% at 200 cycles. This gradual deterioration is attributed to the accumulation of electrically isolated zinc deposits, often termed "dead zinc," that become mechanically detached from the conductive substrate and are no longer accessible for oxidation during discharge.

The current density significantly influenced the rate of zinc utilization degradation. At 20 mA/cm2, zinc utilization decreased from 70.5% at 10 cycles to 65.3% at 50 cycles, 60.8% at 100 cycles, and 55.1% at 200 cycles. The lower current density promotes larger, more compact zinc crystallites that are susceptible to complete detachment during dissolution. At 60 mA/cm2, the initial utilization of 71.3% degraded more slowly, reaching 64.5% at 100 cycles and 59.8% at 200 cycles. The 80 mA/cm2 condition showed the highest initial utilization of 73.6% but the most rapid degradation, falling to 62.1% at 100 cycles and 55.4% at 200 cycles. The accelerated degradation at high current density reflects the formation of highly porous, dendritic zinc deposits with poor mechanical adhesion to the substrate.

### 3.4 Bromine Crossover Rate Under Varied Operating Conditions

Bromine crossover represents one of the most critical degradation mechanisms in ZBFBs, as it directly consumes active material and generates heat through the exothermic reaction between bromine and zinc. The crossover rate was measured as a function of current density, MEP concentration, and cycle number.

At 0.3 M MEP and after 50 cycles, the bromine crossover rate increased systematically with decreasing current density: 0.03 mL/h at 80 mA/cm2, 0.05 mL/h at 60 mA/cm2, 0.07 mL/h at 40 mA/cm2, and 0.12 mL/h at 20 mA/cm2. This inverse relationship confirms that bromine crossover is diffusion-limited, with slower electrochemical reaction rates allowing more time for bromine to diffuse across the separator before being consumed at the positive electrode.

Extended cycling affected crossover rates through separator degradation and electrolyte compositional changes. At 40 mA/cm2 with 0.3 M MEP, the crossover rate increased from 0.07 mL/h at 50 cycles to 0.09 mL/h at 100 cycles and 0.11 mL/h at 200 cycles. This progressive increase is attributed to separator pore enlargement due to chemical attack by bromine and mechanical stress from electrolyte flow, as well as gradual MEP consumption and degradation over extended operation.

The crossover rate also depended on the direction of concentration gradient during different phases of cycling. During charge, bromine generation at the positive electrode creates a transient concentration spike that drives crossover, while during discharge, bromine consumption reduces this gradient. Time-resolved measurements revealed peak crossover rates during the final stages of charging when bromine concentration is highest, with values approximately 2.5 times the average rate over a complete cycle.

### 3.5 Zinc Dendrite Growth Kinetics and Morphological Evolution

Zinc dendrite formation at the negative electrode constitutes the primary mechanical failure mode in ZBFBs, with dendrite penetration of the separator leading to internal short circuits and cell death. The dendrite growth rate was quantified across the full parameter space of current density, MEP concentration, and cycle number.

At 0.3 M MEP, the dendrite growth rate increased substantially with current density: 0.6 um/cycle at 20 mA/cm2, 1.2 um/cycle at 40 mA/cm2, 1.9 um/cycle at 60 mA/cm2, and 3.2 um/cycle at 80 mA/cm2. The approximately quadratic dependence of growth rate on current density is consistent with the Sand time theory for dendrite initiation, which predicts that the induction time for dendrite formation scales inversely with the square of applied current density. At high current densities, the depletion of Zn2+ ions near the electrode surface creates a concentration gradient that promotes unstable, tip-enhanced growth of zinc deposits.

MEP concentration exhibited a moderate but measurable effect on dendrite growth kinetics. At 40 mA/cm2, increasing MEP from 0 M to 0.5 M progressively reduced the dendrite growth rate from 1.5 um/cycle to 1.0 um/cycle. This beneficial effect is attributed to the increased viscosity and modified ionic environment of the electrolyte, which alters the Zn2+ coordination shell and deposition overpotential. However, the magnitude of this effect is smaller than that of current density variation.

Post-mortem SEM analysis revealed distinct dendrite morphologies corresponding to different growth regimes. At 20 mA/cm2, zinc deposits exhibited predominantly hexagonal platelet morphologies with thicknesses of 5-10 um and lateral dimensions of 20-50 um, with occasional filamentary protrusions extending 10-20 um from the surface. At 40 mA/cm2, a mixed morphology of compact layers and porous mossy deposits was observed, with dendrite filaments reaching lengths of 60-120 um after 100 cycles. At 60 mA/cm2, highly branched dendritic structures with primary stems and secondary branches were prevalent, with maximum protrusion lengths of 190-380 um after 100 cycles. The highest current density of 80 mA/cm2 produced dense, needle-like dendrites with lengths exceeding 320 um after only 100 cycles, representing a significant short-circuit risk given the 200 um separator thickness.

### 3.6 Degradation Chain Analysis: Coupling Between Crossover and Dendrite Formation

The degradation mechanisms in ZBFBs are not independent but rather form a coupled degradation chain where bromine crossover and zinc dendrite growth synergistically accelerate capacity fade. Bromine that crosses to the negative side reacts with freshly deposited zinc according to Zn + Br2 -> ZnBr2, consuming active zinc and roughening the electrode surface. This chemically induced surface roughness creates preferential nucleation sites for subsequent zinc deposition, promoting non-uniform current distribution and enhanced dendrite growth. Conversely, dendrite formation increases the effective surface area of the negative electrode and creates local regions of high curvature that disrupt the separator integrity, providing additional pathways for bromine crossover.

To quantify this coupling, cells were cycled at 40 mA/cm2 with 0.3 M MEP, and the temporal evolution of both crossover rate and dendrite growth rate was monitored. During the initial 50 cycles, the crossover rate increased from 0.06 mL/h to 0.07 mL/h while the dendrite growth rate remained relatively constant at 1.2 um/cycle. Between 50 and 100 cycles, the crossover rate accelerated to 0.09 mL/h, and the dendrite growth rate increased to 1.4 um/cycle. From 100 to 200 cycles, both rates increased more rapidly, with crossover reaching 0.11 mL/h and dendrite growth reaching 1.7 um/cycle. This acceleration in degradation rates during later cycling stages confirms the positive feedback between the two mechanisms.

The capacity fade rate showed a corresponding acceleration, with average fade rates of 0.08% per cycle during cycles 1-50, 0.12% per cycle during cycles 51-100, and 0.18% per cycle during cycles 101-200. This non-linear capacity degradation is characteristic of systems with coupled degradation pathways and has important implications for predictive lifetime modeling.

### 3.7 Ohmic Resistance Evolution and Separator Degradation

The ohmic resistance of the ZBFB cell evolved during extended cycling due to separator property changes, electrolyte composition shifts, and electrode surface modifications. At 40 mA/cm2 with 0.3 M MEP, the initial ohmic resistance of 0.78 ohm cm2 increased to 0.89 ohm cm2 at 50 cycles, 1.05 ohm cm2 at 100 cycles, and 1.28 ohm cm2 at 200 cycles. This progressive increase is attributed primarily to separator pore constriction from zinc oxide and bromine byproduct accumulation, as well as partial MEP decomposition products that deposit on the separator surface.

The ohmic resistance also varied significantly with MEP concentration. At 40 mA/cm2 and 50 cycles, the resistance was 0.75 ohm cm2 with 0 M MEP, 0.82 ohm cm2 with 0.1 M MEP, 0.89 ohm cm2 with 0.3 M MEP, and 1.15 ohm cm2 with 0.5 M MEP. The substantial resistance increase at 0.5 M MEP reflects the high viscosity of concentrated MEP solutions, which reduces ionic mobility and increases the diffusive boundary layer thickness at the electrode surfaces.

Current density had a secondary effect on resistance evolution. Cells cycled at 80 mA/cm2 showed more rapid resistance growth than those at 20 mA/cm2, with 200-cycle values of 1.58 ohm cm2 versus 1.12 ohm cm2, respectively. The accelerated degradation at high current density is attributed to more vigorous electrode reactions that produce soluble byproducts and mechanical stress on the separator matrix.

### 3.8 Comparison of Degradation Behavior Across MEP Concentrations

A direct comparison of degradation metrics across the four MEP concentrations reveals distinct optimization tradeoffs. At 40 mA/cm2 and 100 cycles, the 0 M MEP electrolyte showed the highest CE of 89.2% among the initial measurements but suffered from bromine crossover at 0.16 mL/h and severe capacity fade due to chemical self-discharge. The 0.1 M MEP formulation achieved a CE of 87.4% with a reduced crossover rate of 0.11 mL/h. The 0.3 M MEP formulation provided the best balance with a CE of 88.7% and the lowest crossover rate of 0.07 mL/h among the tested concentrations. The 0.5 M MEP formulation showed a CE of 89.4% with the lowest crossover rate of 0.05 mL/h but the highest ohmic resistance of 1.38 ohm cm2 and consequently the lowest EE of 58.2%.

When comparing energy efficiency across the full parameter space, the 0.1 M MEP formulation at 60 mA/cm2 achieved the highest EE of 68.5% at 50 cycles, benefiting from moderate crossover suppression without excessive viscosity penalty. In contrast, the 0.5 M MEP formulation at 20 mA/cm2 produced the lowest EE of 54.1% at 100 cycles due to the combined effects of high viscosity and prolonged exposure to crossover-induced self-discharge at low current density.

### 3.9 Cycle Life Assessment and Failure Mode Analysis

Extended cycling experiments up to 200 cycles were conducted to identify characteristic failure modes and their dependence on operating conditions. At 40 mA/cm2 with 0.3 M MEP, the cell maintained stable operation for approximately 150 cycles before exhibiting accelerated capacity fade. The failure was attributed to cumulative dendrite growth reaching critical dimensions that compromised separator integrity, combined with ohmic resistance increase that raised thermal generation and accelerated side reactions.

At 60 mA/cm2, the cycle life was reduced to approximately 120 cycles due to more rapid dendrite growth, though the higher CE during the stable period partially compensated for the shorter lifetime in terms of total throughput. At 80 mA/cm2, cells frequently experienced catastrophic short-circuit failure within 80-100 cycles as dendrites penetrated the 200 um separator. In contrast, cells operated at 20 mA/cm2 achieved the longest calendar life but suffered from the lowest average CE, resulting in comparable cumulative energy throughput despite the extended cycle number.

Post-mortem analysis of failed cells consistently revealed zinc dendrite filaments embedded in or penetrating the separator, with bromine staining of the negative electrode surface confirming extensive crossover. In cells with 0 M and 0.1 M MEP, separator embrittlement and pore coalescence were additionally observed, indicating chemical degradation of the polyethylene matrix by free bromine. Cells with 0.5 M MEP showed separator surface fouling by MEP decomposition products, which contributed to the elevated ohmic resistance.

### 3.10 Mechanistic Evidence for Degradation Pathways

Multiple lines of evidence support the identified degradation mechanisms. Electrochemical impedance spectroscopy revealed a systematic increase in charge transfer resistance at the zinc electrode during extended cycling, rising from 0.42 ohm cm2 at 10 cycles to 1.25 ohm cm2 at 200 cycles at 40 mA/cm2 with 0.3 M MEP. This increase correlates with the accumulation of surface films and the roughening of zinc deposits that reduce the effective electrochemically active surface area.

X-ray diffraction analysis of cycled zinc electrodes showed progressive broadening of the Zn(002) reflection and the emergence of ZnO and Zn(OH)2 phases, particularly in cells with high bromine crossover rates. The ZnO formation is attributed to the reaction of crossed-over bromine with zinc in the presence of trace water hydrolysis, while Zn(OH)2 formation indicates localized pH excursions at the zinc surface during deposition and stripping.

Cyclic voltammetry of the positive electrode after 100 cycles revealed a 35 mV increase in the peak separation between bromide oxidation and polybromide reduction, indicating diminished electrode kinetics due to carbon surface oxidation and partial wetting loss. The bromine evolution overpotential also increased by approximately 50 mV, consistent with the accumulation of non-conductive surface species on the carbon felt.

Analysis of the electrolyte composition after 200 cycles showed a gradual decrease in MEP concentration from 0.3 M to approximately 0.22 M, indicating slow chemical degradation of the complexing agent through Hofmann elimination and other thermal decomposition pathways. The resulting loss of complexing capacity contributes to the observed acceleration of bromine crossover during extended cycling.

### 3.11 Design Implications and Mitigation Strategies

The comprehensive degradation dataset enables identification of design principles for improved ZBFB systems. The optimal MEP concentration of 0.3 M represents a compromise between bromine sequestration efficiency and viscosity constraints. Operation at moderate current densities of 40-60 mA/cm2 provides the best balance between CE and cycle life, while current densities above 80 mA/cm2 should be avoided unless dendrite suppression additives or modified separators are employed.

The coupled nature of bromine crossover and dendrite growth suggests that mitigation strategies targeting both mechanisms simultaneously will be more effective than single-mechanism approaches. Potential strategies include the use of asymmetric separators with pore size gradients that resist dendrite penetration while maintaining ionic conductivity, the incorporation of organic additives that promote compact zinc deposition through surface adsorption, and the development of more chemically stable complexing agents with lower viscosity contributions.

## 4. Conclusions

This study has provided a quantitative characterization of the principal degradation mechanisms in zinc-bromine flow batteries, establishing the relationships between operating conditions and performance decay. Key findings include:

Bromine crossover rates range from 0.03 mL/h at 80 mA/cm2 to 0.16 mL/h at 20 mA/cm2 with 0 M MEP, and can be reduced by 50-60% through optimization of MEP complexing agent concentration to 0.3 M. Zinc dendrite growth rates scale approximately quadratically with current density, from 0.6 um/cycle at 20 mA/cm2 to 3.2 um/cycle at 80 mA/cm2, representing the primary life-limiting failure mode at elevated current densities. Coulombic efficiency improves from 82-85% at low current density to 90-92% at high current density, but energy efficiency remains relatively constant at 60-65% across the middle range due to the opposing trends in CE and VE. Zinc utilization degrades progressively from initial values of 70-73% to 55-60% over 200 cycles due to the accumulation of electrically isolated zinc deposits. Ohmic resistance increases by 40-60% over 200 cycles due to separator fouling and electrolyte compositional changes, contributing to the gradual decline in voltage efficiency.

The coupled degradation chain between bromine crossover and dendrite growth produces non-linear capacity fade that accelerates in later cycling stages, with fade rates increasing from approximately 0.08% per cycle in early cycling to 0.18% per cycle after 100 cycles. These findings provide a mechanistic foundation for the rational design of improved electrolyte formulations, separator materials, and operating protocols that can extend ZBFB cycle life and enhance commercial competitiveness for grid-scale energy storage applications.
---

# DOC08: Degradation Phenomena in Soluble Lead-Acid Flow Batteries: PbO2 Passivation, Oxygen Evolution, and Cycle Life Limitations

## Abstract

Soluble lead-acid flow batteries (SLFBs) present an attractive energy storage paradigm by eliminating the solid-state electrodeposition challenges of conventional lead-acid systems through the use of fully soluble lead species in methanesulfonic acid electrolyte. However, the unique electrochemistry of the SLFB introduces distinct degradation pathways that compromise long-term operational stability. This study provides a systematic investigation of the dominant degradation mechanisms in SLFBs, focusing on lead dioxide passivation at the positive electrode, parasitic oxygen evolution during charging, and their combined effects on cycle life. Through controlled experiments spanning current densities from 10 to 40 mA/cm2, Pb2+ concentrations from 0.5 to 1.5 mol/L, and H2SO4 concentrations from 1.0 to 2.0 mol/L, we establish quantitative relationships between operating conditions and performance degradation. Results demonstrate that PbO2 passivation layer thickness ranges from 2.5 to 8.3 um depending on cycling conditions, while oxygen evolution rates between 0.8 and 4.2 mL/h directly correlate with capacity fade rates. Coulombic efficiency varies from 78% to 92%, voltage efficiency from 70% to 85%, and energy efficiency from 58% to 78%, with capacity retention after 200 cycles ranging from 63% to 88%. These findings elucidate the coupled degradation mechanisms that limit SLFB cycle life and provide guidance for improved electrolyte formulation and operating protocols.

## 1. Introduction

The soluble lead-acid flow battery represents an innovative evolution of traditional lead-acid chemistry, addressing the principal limitation of conventional systems by maintaining all active materials in solution throughout the charge-discharge cycle. The SLFB employs methanesulfonic acid (MSA) or sulfuric acid electrolyte containing dissolved lead(II) ions, with lead dioxide deposited and dissolved at the positive electrode and metallic lead deposited and dissolved at the negative electrode during normal operation. This approach eliminates the dimensional changes and paste shedding that plague stationary lead-acid batteries, while retaining the advantages of low material cost, established recycling infrastructure, and high theoretical energy density.

The fundamental electrochemical reactions governing SLFB operation involve the oxidation of Pb2+ to PbO2 at the positive electrode during charging (Pb2+ + 2H2O -> PbO2 + 4H+ + 2e-) and the reduction of Pb2+ to metallic lead at the negative electrode (Pb2+ + 2e- -> Pb). During discharge, both reactions reverse, returning lead species to solution as Pb2+ ions. The use of fully soluble chemistry enables flow-through cell designs with continuous electrolyte circulation, facilitating thermal management and uniform reactant distribution.

Despite these conceptual advantages, the SLFB system exhibits several intrinsic degradation mechanisms that limit practical cycle life. The most significant of these is the passivation of the positive electrode through the formation of electrochemically inactive lead dioxide layers. During repeated cycling, PbO2 deposits accumulate in locations that are not fully re-dissolved during discharge, gradually building up a resistive surface layer that reduces the available electrochemically active surface area and increases charge transfer resistance. This passivation phenomenon is exacerbated by the simultaneous occurrence of parasitic oxygen evolution at the positive electrode during charging, which competes with Pb2+ oxidation for available current and causes local pH excursions that alter PbO2 dissolution kinetics.

The oxygen evolution reaction (2H2O -> O2 + 4H+ + 4e-) occurs at potentials exceeding 1.23 V vs SHE and represents a significant parasitic process during SLFB charging, where the positive electrode potential typically ranges from 1.5 to 1.8 V vs SHE. The rate of oxygen evolution depends on the positive electrode overpotential, electrolyte composition, and the catalytic activity of the PbO2 surface, which itself evolves during extended cycling as passivation layers develop. The evolved oxygen not only reduces coulombic efficiency but also modifies the local electrolyte chemistry through proton generation and potential dehydration of the passivation layer.

This work presents a comprehensive experimental study of SLFB degradation mechanisms across a systematic parameter space. We investigate the individual and coupled effects of current density (10-40 mA/cm2), Pb2+ concentration (0.5-1.5 mol/L), and H2SO4 concentration (1.0-2.0 mol/L) on key performance metrics including CE, VE, EE, capacity retention, PbO2 passivation layer thickness, and oxygen evolution rate. The resulting dataset provides quantitative understanding of the degradation landscape and identifies operating windows that maximize cycle life.

## 2. Experimental Methods

### 2.1 Cell Configuration and Assembly

All experiments were conducted in a laboratory-scale soluble lead-acid flow cell with an active electrode area of 5 cm2. Both positive and negative electrodes consisted of carbon polymer composite plates (SGL Carbon, Sigrafine) with machined flow channels for electrolyte distribution. A microporous polyethylene separator (Celgard 2500, 25 um thickness) was employed to prevent direct electrical contact between electrodes while allowing ionic transport. The electrolyte reservoir contained 100 mL of lead-containing solution circulated at 50 mL/min using peristaltic pumps. Copper current collectors were used with graphite gaskets to ensure uniform electrical contact and prevent electrolyte leakage.

### 2.2 Electrolyte Preparation

Electrolyte solutions were prepared by dissolving lead(II) methanesulfonate in aqueous sulfuric acid. Three Pb2+ concentrations were investigated: 0.5 mol/L, 1.0 mol/L, and 1.5 mol/L. For each Pb2+ concentration, three H2SO4 concentrations were evaluated: 1.0 mol/L, 1.5 mol/L, and 2.0 mol/L, yielding nine distinct electrolyte formulations. All electrolyte solutions were filtered through 0.45 um membrane filters to remove particulate matter and degassed with argon for 20 minutes prior to cell assembly. The electrolyte temperature was maintained at 25 C using a circulating water bath.

### 2.3 Electrochemical Testing Protocol

Galvanostatic charge-discharge cycling was performed using an Arbin BT2000 battery testing system. Cells were charged at constant current to an upper voltage limit of 2.1 V and discharged to a lower voltage cutoff of 0.8 V. Current densities of 10, 20, 30, and 40 mA/cm2 were applied symmetrically during charge and discharge. Cycling experiments were conducted for 200 cycles unless terminated earlier due to cell failure. Between cycles, a 30-second rest period was imposed to allow potential relaxation and electrolyte equilibration.

Coulombic efficiency was calculated as the ratio of discharge capacity to charge capacity. Voltage efficiency was determined from the ratio of average discharge voltage to average charge voltage. Energy efficiency was computed as the product of CE and VE. Capacity retention was defined as the ratio of discharge capacity at a given cycle to the maximum discharge capacity observed during the first 10 cycles, expressed as a percentage. Electrochemical impedance spectroscopy was performed at the end of discharge using a 10 mV amplitude perturbation over frequencies from 100 kHz to 10 mHz.

### 2.4 Passivation Layer Characterization

The thickness and morphology of PbO2 passivation layers were characterized through post-mortem analysis of cycled positive electrodes. Cells were disassembled after defined cycle numbers (50, 100, and 200 cycles), and the positive electrode was rinsed with deionized water and dried under vacuum. Cross-sectional samples were prepared by embedding electrodes in epoxy resin and polishing to expose the layer structure. PbO2 passivation layer thickness was measured using scanning electron microscopy (SEM) at five locations across the electrode surface, with average values reported.

The electrochemical activity of passivated electrodes was assessed through cyclic voltammetry in fresh electrolyte, comparing the peak currents for Pb2+/PbO2 redox reactions with those of freshly prepared electrodes. The degree of passivation was quantified as the ratio of aged electrode peak current to fresh electrode peak current, expressed as a percentage.

### 2.5 Oxygen Evolution Rate Measurement

The rate of oxygen evolution during charging was quantified using an inverted burette gas collection system attached to the positive electrolyte reservoir. Evolved gas was collected over a defined charge period, and the gas volume was corrected to standard temperature and pressure. The oxygen fraction was determined by gas chromatography, and the oxygen evolution rate was expressed in mL/h. Measurements were performed at regular intervals during extended cycling to track the evolution of oxygen evolution activity with electrode aging.

## 3. Results and Discussion

### 3.1 Effect of Current Density on Base Performance Metrics

The influence of current density on SLFB performance was established using the baseline electrolyte containing 1.0 mol/L Pb2+ and 1.5 mol/L H2SO4. At a current density of 10 mA/cm2, the system achieved a coulombic efficiency of 85.2%, a voltage efficiency of 82.4%, and an energy efficiency of 70.2%. The relatively high VE at this current density reflects the modest overpotentials associated with low-current operation, while the CE indicates moderate levels of parasitic reactions. At 20 mA/cm2, CE decreased to 82.8% while VE remained relatively high at 80.1%, yielding an EE of 66.3%. The CE decrease at higher current density is attributed to enhanced oxygen evolution at the more polarized positive electrode during charging.

At 30 mA/cm2, CE further decreased to 80.5%, VE declined to 76.9%, and EE dropped to 61.9%. The more pronounced CE reduction reflects the increased overpotential driving oxygen evolution at the positive electrode, while VE degradation results from higher ohmic and concentration polarization at both electrodes. The highest current density of 40 mA/cm2 produced the lowest CE of 78.3% and the lowest VE of 72.5%, resulting in an EE of 56.8%. However, it should be noted that the operational EE in the 40 mA/cm2 condition stabilized near 58% after the initial cycles as the passivation layer partially suppressed oxygen evolution by increasing the effective overpotential for the Pb2+ oxidation reaction relative to water oxidation.

The voltage efficiency trend demonstrates the increasing significance of ohmic losses at higher current densities, with the cell resistance contribution to overpotential rising from approximately 0.05 V at 10 mA/cm2 to 0.18 V at 40 mA/cm2. Concentration polarization also increases substantially at elevated current densities due to the finite rate of Pb2+ transport to the electrode surfaces, particularly at the positive electrode where Pb2+ depletion during charging promotes side reactions.

### 3.2 Effect of Pb2+ Concentration on Performance and Degradation

The concentration of Pb2+ in the electrolyte significantly influences both the initial performance and the rate of degradation during extended cycling. Experiments were conducted at a fixed current density of 20 mA/cm2 and H2SO4 concentration of 1.5 mol/L across three Pb2+ concentrations.

At 0.5 mol/L Pb2+, the initial CE was 80.1%, VE was 78.5%, and EE was 62.9%. The relatively low CE reflects the higher ratio of parasitic current to total current at low active material concentrations, where oxygen evolution competes more effectively with the Pb2+/PbO2 redox couple. Over 200 cycles, capacity retention was 68.4%, indicating significant cumulative degradation. The PbO2 passivation layer reached a thickness of 7.2 um after 200 cycles, substantially exceeding the values observed at higher Pb2+ concentrations.

At 1.0 mol/L Pb2+, initial CE improved to 82.8%, VE to 80.1%, and EE to 66.3%. Capacity retention after 200 cycles was 76.8%, representing a significant improvement over the 0.5 mol/L condition. The passivation layer thickness after 200 cycles was 5.8 um, reflecting more favorable dissolution kinetics due to the higher driving force for PbO2 reduction during discharge. The oxygen evolution rate was also reduced compared to the dilute electrolyte, consistent with the improved CE.

At 1.5 mol/L Pb2+, initial CE reached 86.5%, VE was 81.3%, and EE was 70.3%. This formulation achieved the highest capacity retention of 82.1% after 200 cycles and the thinnest passivation layer of 4.9 um. The improved performance at higher Pb2+ concentration is attributed to several factors: enhanced mass transport reducing concentration polarization, higher exchange current density for the Pb2+/PbO2 couple, and more favorable dissolution thermodynamics that limit passivation layer accumulation. However, the higher Pb2+ concentration increases electrolyte density and viscosity, raising pumping power requirements and potentially complicating system design.

### 3.3 Effect of H2SO4 Concentration on Performance and Degradation

The H2SO4 concentration in the electrolyte governs the conductivity, pH, and speciation of lead complexes, all of which influence SLFB performance and degradation behavior. Experiments at 20 mA/cm2 with 1.0 mol/L Pb2+ investigated three H2SO4 concentrations.

At 1.0 mol/L H2SO4, initial CE was 79.4%, VE was 75.2%, and EE was 59.7%. The relatively low VE reflects the moderate ionic conductivity of this electrolyte, which results in higher ohmic overpotentials. Over 200 cycles, capacity retention was 65.7%, the lowest among the tested H2SO4 concentrations. The PbO2 passivation layer thickness reached 7.8 um, and the oxygen evolution rate was 2.8 mL/h during early cycling, increasing to 3.5 mL/h after 200 cycles. The thin passivation layer and high oxygen evolution rate suggest that the low acid concentration provides insufficient proton activity to support complete PbO2 dissolution during discharge.

At 1.5 mol/L H2SO4, initial CE improved to 82.8%, VE increased to 80.1%, and EE reached 66.3%. The improved VE is directly attributable to the higher ionic conductivity of the more concentrated acid electrolyte. Capacity retention after 200 cycles was 76.8%, with a passivation layer thickness of 5.8 um. The oxygen evolution rate was 2.1 mL/h initially, increasing to 2.7 mL/h after 200 cycles. This formulation represents a significant improvement over the 1.0 mol/L condition.

At 2.0 mol/L H2SO4, initial CE was 83.5%, VE was 82.7%, and EE was 69.1%. The highest VE among the tested conditions reflects the maximum ionic conductivity. Capacity retention after 200 cycles was 79.3%, with a passivation layer thickness of 5.2 um and oxygen evolution rate of 1.9 mL/h initially, increasing to 2.4 mL/h after 200 cycles. However, the 2.0 mol/L H2SO4 condition showed a more rapid initial fade rate during the first 50 cycles, which is attributed to the enhanced chemical dissolution of freshly deposited PbO2 in highly acidic media, leading to structural reorganization of the deposit morphology.

### 3.4 PbO2 Passivation Layer Formation and Growth Kinetics

The formation and growth of PbO2 passivation layers represents the primary degradation mechanism at the positive electrode in SLFBs. The passivation process begins during the initial cycles as PbO2 deposits nucleate and grow on the carbon substrate. During discharge, a fraction of these deposits fails to fully dissolve, particularly in regions with poor electrolyte access or where the local pH has shifted due to oxygen evolution. The residual PbO2 serves as nucleation sites for subsequent deposition, gradually building up a multilayer structure with decreasing electrochemical accessibility.

At the baseline condition of 20 mA/cm2, 1.0 mol/L Pb2+, and 1.5 mol/L H2SO4, the passivation layer thickness increased progressively with cycle number: 2.5 um at 50 cycles, 4.1 um at 100 cycles, and 5.8 um at 200 cycles. The growth rate exhibited a decelerating trend, with an average of 0.05 um/cycle during cycles 1-50, 0.032 um/cycle during cycles 51-100, and 0.017 um/cycle during cycles 101-200. This deceleration is attributed to the self-limiting nature of passivation growth, where the increasing layer resistance reduces the local current density at the electrode-electrolyte interface, thereby slowing further accumulation.

Current density had a strong effect on passivation layer development. At 10 mA/cm2 with 1.0 mol/L Pb2+ and 1.5 mol/L H2SO4, the layer thickness was 3.1 um at 100 cycles and 4.5 um at 200 cycles. At 30 mA/cm2, the thickness increased to 5.2 um at 100 cycles and 7.1 um at 200 cycles. At 40 mA/cm2, the layer reached 6.3 um at 100 cycles and 8.3 um at 200 cycles. The accelerated passivation at high current density reflects the higher rate of PbO2 deposition during charging, which exceeds the dissolution rate during discharge, leading to net accumulation.

Post-mortem SEM analysis revealed distinct microstructural features of the passivation layers. At low current density (10 mA/cm2), the layer exhibited a relatively compact, columnar morphology with fine crystallites and limited porosity. At moderate current density (20 mA/cm2), a mixed morphology of compact and porous regions was observed, with the porous regions corresponding to locations of preferential oxygen evolution. At high current density (40 mA/cm2), a highly porous, dendritic morphology prevailed, with extensive cracking and delamination indicating poor mechanical adhesion to the substrate. The porous morphology at high current density provides high surface area for oxygen evolution while limiting the electrochemically accessible area for Pb2+ oxidation.

### 3.5 Oxygen Evolution Kinetics and Its Relationship to Passivation

Oxygen evolution represents the dominant parasitic reaction in SLFBs, consuming charge capacity during charging and contributing to the positive electrode degradation through local pH changes and PbO2 dehydration. The oxygen evolution rate was measured as a function of current density, electrolyte composition, and cycle number.

At the baseline condition of 20 mA/cm2, 1.0 mol/L Pb2+, and 1.5 mol/L H2SO4, the oxygen evolution rate increased with cycling: 2.1 mL/h during cycles 1-10, 2.3 mL/h during cycles 41-50, 2.7 mL/h during cycles 91-100, and 3.0 mL/h during cycles 191-200. This progressive increase is attributed to the growth of the PbO2 passivation layer, which alters the effective catalytic surface for water oxidation. The PbO2 surface that develops during cycling exhibits higher catalytic activity for oxygen evolution compared to the fresh carbon substrate, a phenomenon analogous to the behavior of dimensionally stable anodes used in chlor-alkali electrolysis.

Current density strongly influenced the oxygen evolution rate. At 10 mA/cm2 with 1.0 mol/L Pb2+ and 1.5 mol/L H2SO4, the rate was 0.8 mL/h during early cycling and 1.4 mL/h after 200 cycles. At 30 mA/cm2, the rate increased to 3.2 mL/h initially and 4.0 mL/h after 200 cycles. At 40 mA/cm2, the highest rates were observed: 4.2 mL/h during early cycling and 4.2 mL/h after 200 cycles, though the rate stabilized as the thick passivation layer increased the ohmic drop and reduced the effective overpotential for water oxidation.

The relationship between Pb2+ concentration and oxygen evolution rate revealed a significant inverse correlation. At 20 mA/cm2 and 1.5 mol/L H2SO4, the oxygen evolution rate after 100 cycles was 3.4 mL/h with 0.5 mol/L Pb2+, 2.7 mL/h with 1.0 mol/L Pb2+, and 2.2 mL/h with 1.5 mol/L Pb2+. The lower oxygen evolution rate at higher Pb2+ concentration is attributed to the reduced overpotential required for Pb2+ oxidation when mass transport limitations are minimized, which narrows the potential window available for water oxidation.

The H2SO4 concentration also affected oxygen evolution, though the relationship was more complex. At 20 mA/cm2 and 1.0 mol/L Pb2+, the rate after 100 cycles was 2.9 mL/h with 1.0 mol/L H2SO4, 2.7 mL/h with 1.5 mol/L H2SO4, and 2.4 mL/h with 2.0 mol/L H2SO4. The decrease in oxygen evolution rate at higher acid concentration is attributed to the Nernstian shift in oxygen evolution equilibrium potential and the reduced activity of water at high proton concentrations.

### 3.6 Degradation Chain: Coupling Between Passivation and Oxygen Evolution

The degradation mechanisms in SLFBs exhibit strong coupling, with PbO2 passivation and oxygen evolution forming a self-reinforcing cycle that accelerates capacity fade. During charging, the positive electrode potential must be sufficiently high to oxidize Pb2+ to PbO2. As passivation develops, the effective surface area for this reaction decreases, forcing the electrode potential to more positive values to maintain the applied current. These elevated potentials simultaneously accelerate oxygen evolution, which generates local acidity that alters PbO2 dissolution kinetics and promotes the formation of more stable, less soluble PbO2 polymorphs that resist subsequent dissolution.

This degradation chain was quantified by tracking the simultaneous evolution of passivation layer thickness and oxygen evolution rate at the baseline condition. During cycles 1-50, the passivation layer grew from 0 to 2.5 um while the oxygen evolution rate increased from 2.1 to 2.3 mL/h. During cycles 51-100, the layer grew from 2.5 to 4.1 um while the oxygen rate increased from 2.3 to 2.7 mL/h. During cycles 101-200, the layer grew from 4.1 to 5.8 um while the oxygen rate increased from 2.7 to 3.0 mL/h. The progressive acceleration in both metrics confirms their mutual reinforcement.

The capacity fade rate showed a corresponding pattern, with average fade rates of 0.10% per cycle during cycles 1-50, 0.14% per cycle during cycles 51-100, and 0.20% per cycle during cycles 101-200. This acceleration is consistent with the increasing fraction of charge current consumed by oxygen evolution rather than productive PbO2 formation.

EIS analysis provided additional evidence for the degradation chain. The charge transfer resistance at the positive electrode increased from 0.35 ohm cm2 at 10 cycles to 0.82 ohm cm2 at 100 cycles and 1.28 ohm cm2 at 200 cycles. This increase correlates with the growing passivation layer and is accompanied by a decrease in the double-layer capacitance, indicating loss of electrochemically active surface area. The ohmic resistance component also increased from 0.45 ohm cm2 to 0.68 ohm cm2 over 200 cycles, attributed to the development of a resistive PbO2 interlayer and electrolyte compositional changes.

### 3.7 Comparison of Degradation Behavior Across Electrolyte Compositions

A comprehensive comparison of the nine electrolyte formulations at 20 mA/cm2 reveals the electrolyte design space and its impact on degradation. The lowest degradation rates were observed with 1.5 mol/L Pb2+ and 2.0 mol/L H2SO4, which achieved CE of 86.2%, EE of 70.8%, capacity retention of 85.3% at 200 cycles, passivation layer thickness of 4.7 um, and oxygen evolution rate of 2.0 mL/h. This formulation benefits from the high Pb2+ concentration that suppresses parasitic reactions and the high acid concentration that provides favorable conductivity and PbO2 dissolution kinetics.

The highest degradation rates occurred with 0.5 mol/L Pb2+ and 1.0 mol/L H2SO4, which showed CE of 76.8%, EE of 58.2%, capacity retention of 63.4% at 200 cycles, passivation layer thickness of 8.1 um, and oxygen evolution rate of 3.6 mL/h. This dilute electrolyte suffers from the combined effects of poor mass transport, low conductivity, and unfavorable PbO2 dissolution thermodynamics.

Comparing across H2SO4 concentrations at fixed 1.0 mol/L Pb2+, the capacity retention at 200 cycles improved from 65.7% at 1.0 mol/L H2SO4 to 76.8% at 1.5 mol/L H2SO4 and 79.3% at 2.0 mol/L H2SO4. The corresponding passivation layer thickness decreased from 7.8 um to 5.8 um to 5.2 um, while oxygen evolution rates decreased from 3.5 mL/h to 2.7 mL/h to 2.4 mL/h. These trends confirm the beneficial effect of increased acid concentration on both conductivity and PbO2 management.

Comparing across Pb2+ concentrations at fixed 1.5 mol/L H2SO4, capacity retention improved from 68.4% at 0.5 mol/L Pb2+ to 76.8% at 1.0 mol/L Pb2+ and 82.1% at 1.5 mol/L Pb2+. The passivation layer thickness decreased from 7.2 um to 5.8 um to 4.9 um, while oxygen evolution rates decreased from 3.4 mL/h to 2.7 mL/h to 2.2 mL/h. These results demonstrate that increasing Pb2+ concentration provides substantial benefits for cycle life, though practical constraints may limit the maximum achievable concentration.

### 3.8 Capacity Retention and Cycle Life Analysis

Capacity retention over 200 cycles was evaluated across the full parameter space. At the optimal electrolyte composition (1.5 mol/L Pb2+, 2.0 mol/L H2SO4), capacity retention was 91.2% at 50 cycles, 88.5% at 100 cycles, and 85.3% at 200 cycles at 10 mA/cm2. At 20 mA/cm2, the retention was 87.4% at 50 cycles, 82.6% at 100 cycles, and 76.8% at 200 cycles. At 30 mA/cm2, the values were 82.1% at 50 cycles, 75.3% at 100 cycles, and 68.5% at 200 cycles. At 40 mA/cm2, the capacity retention was 76.8% at 50 cycles, 69.2% at 100 cycles, and 62.8% at 200 cycles.

The capacity fade mechanism was analyzed through differential capacity analysis, which revealed two distinct contributions. The first, dominant during the initial 50 cycles, is attributed to the formation and stabilization of the PbO2 passivation layer and the concurrent increase in oxygen evolution activity. The second, more prominent after 50 cycles, reflects the progressive thickening of the passivation layer and the associated increase in charge transfer resistance and ohmic losses.

At high current densities (30-40 mA/cm2), cells occasionally exhibited sudden capacity drops associated with partial delamination of the passivation layer, which exposed fresh carbon surface temporarily but also created electrically isolated PbO2 particles that contributed to irreversible capacity loss. This mechanical failure mode was not observed at lower current densities where the passivation layer developed more uniformly.

### 3.9 Mechanistic Evidence for Degradation Pathways

Multiple analytical techniques provided mechanistic evidence for the identified degradation pathways. X-ray diffraction analysis of cycled positive electrodes confirmed the presence of both alpha-PbO2 (orthorhombic) and beta-PbO2 (tetragonal) phases, with the beta-phase content increasing from 45% in fresh deposits to 78% after 200 cycles. The beta-PbO2 phase is known to be more electrochemically stable and less soluble than alpha-PbO2, explaining the progressive difficulty in fully dissolving the passivation layer during discharge.

X-ray photoelectron spectroscopy (XPS) analysis of the passivation layer surface after 200 cycles revealed the presence of PbSO4 in addition to PbO2, indicating that sulfate incorporation into the passivation layer contributes to its electrochemical inactivity. The PbSO4 fraction increased with decreasing H2SO4 concentration, suggesting that the local pH excursions associated with oxygen evolution promote sulfate precipitation within the passivation layer when the bulk acid concentration is insufficient to prevent it.

Cyclic voltammetry of aged positive electrodes in fresh electrolyte showed a 45% reduction in the Pb2+/PbO2 redox peak current after 200 cycles compared to fresh electrodes, consistent with the loss of electrochemically active surface area. The peak potential separation increased from 85 mV on fresh electrodes to 152 mV on aged electrodes, indicating slower electrode kinetics due to the passivation layer.

Analysis of the electrolyte composition after 200 cycles showed a gradual decrease in Pb2+ concentration of approximately 8-12%, attributed to the accumulation of lead species in the passivation layer that are not fully recovered during discharge. This active material inventory loss contributes to the observed capacity fade in addition to the resistance-driven fade mechanisms.

### 3.10 Design Implications for Improved SLFB Systems

The comprehensive degradation analysis enables identification of design strategies for improved SLFB performance. The optimal electrolyte composition of 1.5 mol/L Pb2+ and 2.0 mol/L H2SO4 provides the best balance between initial efficiency and cycle life, achieving CE of 86.2%, VE of 82.1%, EE of 70.8%, and capacity retention of 85.3% at 200 cycles when operated at 10 mA/cm2.

Operating current density should be maintained at or below 20 mA/cm2 for applications requiring extended cycle life, as higher current densities produce thicker passivation layers and higher oxygen evolution rates that accelerate degradation. For applications where power density is prioritized over cycle life, operation at 30-40 mA/cm2 may be acceptable with appropriate electrolyte formulation, though the capacity retention falls below 70% after 200 cycles.

The coupled nature of passivation and oxygen evolution suggests that effective mitigation strategies must address both mechanisms simultaneously. Potential approaches include the use of pulse charging protocols that periodically apply anodic pulses to dissolve passivation layers, the incorporation of additives that stabilize alpha-PbO2 relative to the less soluble beta-phase, and the development of positive electrode substrates with optimized surface chemistry that promotes uniform PbO2 nucleation and complete dissolution.

## 4. Conclusions

This study has provided a comprehensive characterization of the principal degradation mechanisms in soluble lead-acid flow batteries, establishing quantitative relationships between operating conditions and performance decay. Key findings include:

PbO2 passivation layer thickness ranges from 2.5 um at 50 cycles to 8.3 um at 200 cycles depending on current density and electrolyte composition, with higher current densities and lower Pb2+ concentrations promoting thicker, more resistive layers. Oxygen evolution rates range from 0.8 mL/h at 10 mA/cm2 to 4.2 mL/h at 40 mA/cm2 during early cycling, with rates increasing by 40-75% over 200 cycles as the passivation layer develops enhanced catalytic activity for water oxidation. Coulombic efficiency varies from 78.3% at 40 mA/cm2 to 86.5% at 20 mA/cm2 with 1.5 mol/L Pb2+, with higher Pb2+ and H2SO4 concentrations generally improving CE by reducing oxygen evolution and promoting complete PbO2 dissolution. Capacity retention at 200 cycles ranges from 63% with 0.5 mol/L Pb2+ and 1.0 mol/L H2SO4 to 88% with 1.5 mol/L Pb2+ and 2.0 mol/L H2SO4 at 10 mA/cm2, demonstrating the strong dependence of cycle life on electrolyte formulation.

The coupled degradation chain between PbO2 passivation and oxygen evolution produces accelerating capacity fade, with fade rates increasing from approximately 0.10% per cycle in early cycling to 0.20% per cycle after 100 cycles. This non-linear degradation is characteristic of systems with self-reinforcing failure mechanisms and must be accounted for in predictive lifetime models. The optimal SLFB design identified in this work employs 1.5 mol/L Pb2+ and 2.0 mol/L H2SO4 electrolyte operated at 10-20 mA/cm2, achieving energy efficiency of 70% and capacity retention above 75% over 200 cycles. These findings provide a mechanistic foundation for the continued development of soluble lead-acid flow batteries for stationary energy storage applications.
---

# DOC09: Stability and Degradation Mechanisms of Organic Active Species in Nonaqueous and Aqueous Redox Flow Batteries

## Abstract

Organic redox flow batteries (ORFBs) have emerged as promising candidates for large-scale energy storage due to the structural tunability, elemental abundance, and potentially low cost of organic active materials. Among the numerous organic redox-active compounds investigated, three classes have demonstrated particular promise: nitroxyl radicals based on 2,2,6,6-tetramethylpiperidine-1-oxyl (TEMPO) and its derivatives, viologen-based bipyridinium salts, and quinone derivatives including anthraquinone and benzoquinone analogs. This review examines the stability profiles, degradation pathways, and performance characteristics of these three organic active species families under practical battery operating conditions. We analyze the influence of pH, current density, state of charge, and membrane properties on capacity retention, coulombic efficiency, and energy efficiency. Particular attention is given to the molecular degradation mechanisms including radical disproportionation, nucleophilic attack, dimerization, and crossover-induced capacity fade. Through systematic comparison across different chemistries, we identify design principles for mitigating degradation and extending cycle life in ORFB systems.

## 1. Introduction to Organic Active Species in Flow Batteries

The transition to renewable energy sources necessitates the development of cost-effective, scalable energy storage technologies. Redox flow batteries (RFBs) offer distinct advantages for grid-scale applications, including decoupled energy and power ratings, long cycle life, and inherent safety features. While traditional all-vanadium and zinc-bromine systems have dominated the flow battery landscape, organic redox flow batteries have attracted substantial research interest due to their potential for dramatic cost reduction and structural versatility.

Organic active species derive their redox activity from functional groups that undergo reversible electron transfer reactions. The three most extensively studied classes are nitroxyl radicals (exemplified by TEMPO), bipyridinium salts (viologens), and quinones. Each class offers distinct redox potentials, solubility characteristics, and stability profiles that determine their suitability for different battery configurations.

TEMPO and its derivatives operate via a single-electron oxidation process, transitioning between the neutral radical state and the oxoammonium cation. This redox couple typically exhibits excellent electrochemical reversibility with fast electron transfer kinetics. Viologens, based on 4,4'-bipyridine structures, undergo two consecutive one-electron reductions, forming first a radical cation and then a neutral species. Quinones operate through a two-electron, two-proton redox mechanism that is highly dependent on pH and electrolyte composition.

The practical deployment of ORFBs depends critically on understanding and controlling the degradation mechanisms that limit cycle life. Unlike inorganic redox couples, organic species are susceptible to a broader range of decomposition pathways including chemical degradation, electrochemical side reactions, and membrane crossover. This review provides a comprehensive analysis of these degradation mechanisms and the strategies employed to mitigate them.

## 2. TEMPO-Based Catholyte Materials: Performance and Stability

### 2.1 Electrochemical Characteristics and Operating Performance

TEMPO (2,2,6,6-tetramethylpiperidine-1-oxyl) and its functionalized derivatives have emerged as leading catholyte materials for nonaqueous and hybrid organic flow batteries. The TEMPO radical undergoes reversible one-electron oxidation to form the TEMPO+ oxoammonium cation at a potential of approximately +0.3 V to +0.6 V versus Ag/AgCl depending on the solvent and substituent groups. This moderate oxidation potential provides good compatibility with a range of anolyte chemistries while avoiding the oxidative decomposition of common electrolyte solvents.

In a nonaqueous TEMPO-based flow battery employing 0.1 M TEMPO in acetonitrile with tetraethylammonium tetrafluoroborate supporting electrolyte, operation at a current density of 100 mA/cm2 yielded a coulombic efficiency (CE) of 98.2% and an energy efficiency (EE) of 84.3% when paired with a viologen-based anolyte. When the current density was reduced to 60 mA/cm2, the energy efficiency increased to 87.1% while maintaining a CE of 98.5%, reflecting the reduced overpotential losses at lower current densities. Further reduction to 40 mA/cm2 yielded an EE of 88.0% with CE of 98.8%. At 20 mA/cm2, the system demonstrated an EE of 88.5% with CE approaching 99.0%.

The membrane employed in these studies was a Nafion 117 cation exchange membrane, which provided a membrane selectivity of 94% for the supporting electrolyte over the active species. The crossover rate of TEMPO through the Nafion 117 membrane was measured at 0.8 x 10^-6 cm2/s, contributing to a gradual capacity fade over extended cycling. The capacity fade rate under these conditions was approximately 0.02%/cycle over 500 continuous charge-discharge cycles.

Functionalization of the TEMPO core structure has been explored as a strategy for improving stability and reducing crossover. A TEMPO derivative incorporating a poly(ethylene glycol) (PEG) chain, referred to as TEMPO-PEG, demonstrated a significantly reduced crossover rate of 0.3 x 10^-6 cm2/s through Nafion 117 due to the increased molecular size and hydrophilic character of the PEG tail. When tested at 100 mA/cm2, the TEMPO-PEG system achieved a CE of 98.9% and EE of 83.7%, with a capacity fade rate of 0.015%/cycle over 300 cycles.

### 2.2 Degradation Mechanisms of TEMPO Species

The degradation of TEMPO-based catholytes proceeds through several distinct pathways that operate in parallel under battery cycling conditions. Understanding these mechanisms is essential for developing mitigation strategies.

The primary degradation pathway for TEMPO involves the disproportionation of the oxoammonium cation (TEMPO+) in the presence of water or nucleophilic species. The oxoammonium form is thermodynamically susceptible to reaction with water molecules, producing the hydroxylamine derivative and oxygen-containing byproducts. This disproportionation reaction is accelerated at elevated temperatures and in the presence of acidic impurities. In nonaqueous electrolytes with rigorous water exclusion (water content below 10 ppm), the disproportionation rate is substantially reduced, contributing to extended cycle life.

A second significant degradation pathway involves the radical-radical coupling or disproportionation of two TEMPO radicals to form non-redox-active adducts. The extent of dimerization was quantified at approximately 5% after 200 cycles in a standard acetonitrile-based electrolyte. This dimerization extent increased to 12% when the electrolyte was cycled at elevated temperature (45 C), indicating the thermal sensitivity of the radical stability. The dimerization products are electrochemically inactive and thus represent a permanent loss of active material capacity.

Electrochemical instability of the oxoammonium form at high states of charge (SOC) represents a third degradation mechanism. When the catholyte is charged to SOC levels exceeding 90%, the high concentration of TEMPO+ promotes side reactions with solvent molecules and supporting electrolyte anions. This phenomenon manifests as a gradual decline in CE during extended cycling at high SOC limits. Cycling with an SOC upper limit of 85% rather than 95% reduced the capacity fade rate from 0.035%/cycle to 0.018%/cycle, demonstrating the importance of SOC window management.

The fourth degradation pathway involves membrane crossover and the subsequent reaction of crossed-over TEMPO species with the anolyte material. The crossover of TEMPO through the membrane creates a chemical short-circuit, resulting in SOC imbalance between the catholyte and anolyte sides. In long-term cycling experiments, SOC imbalance was observed to reach approximately 12% after 400 cycles with Nafion 117 membrane. The use of a size-selective membrane with higher selectivity (98%) reduced this SOC imbalance to 5% over the same cycle number.

## 3. Viologen-Based Anolyte Materials: Performance and Stability

### 3.1 Electrochemical Characteristics and Operating Performance

Viologens, derived from 4,4'-bipyridine, have established themselves as premier anolyte materials for organic and hybrid redox flow batteries. The viologen structure undergoes two sequential one-electron reductions: first from the dication (V2+) to the radical cation (V+), and subsequently to the neutral species (V0). The first reduction step occurs at a potential of approximately -0.4 V to -0.6 V versus Ag/AgCl, providing a favorable cell voltage when paired with TEMPO-based catholytes. The second reduction to the neutral form occurs at more negative potentials (-0.9 V to -1.1 V) and is generally avoided in practical battery operation due to stability concerns.

A benchmark study of methyl viologen (MV, 1,1'-dimethyl-4,4'-bipyridinium dichloride) in aqueous electrolyte at pH 7 demonstrated excellent performance when paired with a TEMPO catholyte. At a current density of 100 mA/cm2, the cell achieved a CE of 96.8% and an EE of 80.2%. Reducing the current density to 60 mA/cm2 improved the EE to 83.5% with a CE of 97.5%. At 40 mA/cm2, the system delivered an EE of 85.2% and CE of 98.0%. Operation at 20 mA/cm2 yielded the highest EE at 86.8% with CE of 98.5%.

The membrane selectivity plays a critical role in viologen-based systems due to the relatively small molecular size of the methyl viologen dication. With Nafion 117 membrane, the selectivity was measured at 88%, with a viologen crossover rate of 2.1 x 10^-6 cm2/s. This substantial crossover rate contributed to a capacity fade rate of 0.055%/cycle. To address this limitation, researchers have developed viologen derivatives with bulky substituents. A propylsulfonate-functionalized viologen (PSV) demonstrated a dramatically reduced crossover rate of 0.4 x 10^-6 cm2/s through Nafion 117, with membrane selectivity improving to 96%. The PSV system at 100 mA/cm2 achieved a CE of 98.5% and EE of 82.1%, with the capacity fade rate reduced to 0.018%/cycle.

The pH dependence of viologen performance has been systematically investigated. While the viologen redox chemistry itself is pH-independent for the first reduction step, the overall cell performance is influenced by pH-dependent side reactions and membrane transport properties. At pH 9, the CE of a MV/TEMPO cell increased to 97.5% compared to 96.8% at pH 7, attributed to suppression of proton crossover effects. At pH 11, the CE was 97.8%, while at pH 12 the CE decreased slightly to 97.2% due to onset of alkaline degradation of the TEMPO catholyte. At pH 14, the CE dropped to 95.5% as both active species showed accelerated degradation under strongly alkaline conditions.

### 3.2 Degradation Mechanisms of Viologen Species

Viologen degradation in flow battery electrolytes proceeds through mechanisms distinct from those affecting TEMPO species, reflecting the different electronic structures and redox states involved.

The primary degradation pathway for viologens involves the dimerization of viologen radical cations (V+) to form dimers that are electrochemically inactive. The viologen radical cation, formed during the first reduction step, has an unpaired electron that is delocalized over the bipyridine framework. Under conditions of high radical concentration, two radical cations can couple to form a diamagnetic dimer. The dimerization extent was measured at approximately 8% after 200 cycles in a standard aqueous MV electrolyte at pH 7 and current density of 100 mA/cm2. This dimerization extent increased to 14% at higher viologen concentrations (0.2 M), reflecting the second-order dependence of the dimerization kinetics on radical cation concentration.

Functionalization of the viologen core with bulky substituents has proven effective in mitigating dimerization. A benzyl-substituted viologen derivative showed a reduced dimerization extent of 4% under identical cycling conditions, attributed to steric hindrance preventing close approach of the radical cation species. The trade-off for this improved stability was a slight reduction in solubility, from 1.2 M for MV to 0.8 M for the benzyl derivative.

A second degradation pathway involves nucleophilic attack on the viologen dication by hydroxide ions or other nucleophiles present in the electrolyte. This pathway becomes significant under alkaline conditions, particularly at pH values above 12. The nucleophilic attack occurs at the 2- and 6-positions of the pyridine rings, forming dihydropyridine adducts that alter the redox properties of the molecule. At pH 14, this degradation pathway resulted in a capacity fade rate of 0.072%/cycle, substantially higher than the 0.035%/cycle observed at pH 7.

The third degradation mechanism involves the over-reduction of viologen to the neutral form (V0), which is highly reactive and susceptible to chemical decomposition. The neutral viologen species is poorly soluble in aqueous media and can undergo disproportionation or reaction with solvent molecules. In battery operation, over-reduction is avoided by implementing appropriate charge cutoff voltages, but voltage excursions during high-rate operation or impedance growth can lead to localized over-reduction. When cells were operated without appropriate voltage limits, the capacity fade rate increased to 0.065%/cycle due to neutral viologen formation and subsequent decomposition.

## 4. Quinone-Based Active Materials: Performance and Stability

### 4.1 Electrochemical Characteristics and Operating Performance

Quinone derivatives represent the third major class of organic active species for redox flow batteries, distinguished by their two-electron, two-proton redox mechanism. Anthraquinone derivatives have been particularly extensively studied due to their favorable redox potentials, high solubility in alkaline media, and low cost. The redox potential of anthraquinone is highly pH-dependent, shifting by approximately 59 mV per pH unit according to the Nernst equation, providing flexibility in cell voltage design.

9,10-anthraquinone-2,7-disulfonic acid (AQDS) has emerged as a leading quinone anolyte material. In alkaline electrolyte at pH 12, AQDS undergoes reversible two-electron reduction at a potential of -0.45 V versus Ag/AgCl. When paired with a ferrocyanide catholyte in an all-aqueous configuration, the cell voltage is approximately 0.8 V. At a current density of 100 mA/cm2, this system achieved a CE of 95.5% and an EE of 78.5%. At 60 mA/cm2, the EE improved to 82.1% with CE of 96.5%. Operation at 40 mA/cm2 yielded an EE of 84.3% and CE of 97.2%, while at 20 mA/cm2 the system reached an EE of 85.5% with CE of 98.0%.

The pH dependence of AQDS performance has been comprehensively characterized. At pH 9, the CE was 94.2% at 100 mA/cm2 with EE of 76.5%, reflecting slower redox kinetics under less alkaline conditions. At pH 11, the CE improved to 95.8% and EE to 79.2%. At pH 12, the system demonstrated optimal performance with CE of 95.5% and EE of 78.5% at 100 mA/cm2. At pH 14, the CE decreased to 93.8% due to accelerated chemical degradation under strongly alkaline conditions, with the EE dropping to 76.2%.

Benzoquinone and its derivatives have also been investigated as catholyte materials, although their use is limited to nonaqueous or mildly acidic systems due to instability in alkaline media. In nonaqueous electrolyte (acetonitrile with tetrabutylammonium hexafluorophosphate), p-benzoquinone demonstrated a CE of 97.2% and EE of 83.5% at 60 mA/cm2 when paired with an AQDS anolyte. The lower performance compared to all-aqueous systems reflects the higher ohmic resistance of nonaqueous electrolytes.

The crossover characteristics of AQDS are favorable due to the sulfonate functional groups that provide electrostatic repulsion from cation exchange membranes. The crossover rate of AQDS through Nafion 117 was measured at 0.2 x 10^-6 cm2/s, substantially lower than that of TEMPO or MV. This low crossover rate contributed to excellent capacity retention, with fade rates as low as 0.01%/cycle observed over 1000 cycles at 60 mA/cm2 with an appropriate membrane.

### 4.2 Degradation Mechanisms of Quinone Species

Quinone degradation in redox flow batteries proceeds through mechanisms that are strongly dependent on pH, oxygen exposure, and cycling conditions.

The primary degradation pathway for anthraquinone derivatives in alkaline media involves the nucleophilic addition of hydroxide ions to the oxidized quinone form, followed by rearrangement to form non-redox-active hydroxylated products. This pathway, often referred to as the Dakin-type degradation, is accelerated at high pH and elevated temperature. At pH 14, the degradation rate was sufficiently rapid to produce a capacity fade rate of 0.068%/cycle, compared to 0.012%/cycle at pH 12 and 0.028%/cycle at pH 9. The optimal pH of 12 represents a compromise between maintaining favorable redox kinetics (which improve at higher pH) and suppressing nucleophilic degradation (which accelerates at higher pH).

A second significant degradation pathway for quinones involves oxidation by molecular oxygen. The reduced form of anthraquinone (anthrahydroquinone) is highly susceptible to autoxidation by dissolved oxygen, regenerating the oxidized quinone but consuming electrons in the process. This autoxidation represents a parasitic reaction that reduces coulombic efficiency. In a cell operated with oxygen-saturated electrolyte, the CE dropped to 90.2% at 100 mA/cm2, compared to 95.5% under oxygen-free conditions. Rigorous deoxygenation of the electrolyte is therefore essential for maintaining high efficiency in quinone-based systems.

The third degradation mechanism involves the Michael addition of nucleophiles to the quinone ring. Under alkaline conditions, species such as sulfite, bisulfite, or organic thiols can add to the quinone framework, permanently modifying the electronic structure and redox properties. In electrolytes containing trace sulfite impurities (introduced through degradation of sulfonate-functionalized membranes or supporting electrolytes), this pathway contributed to an additional 0.015%/cycle capacity fade beyond the base degradation rate.

For benzoquinone in nonaqueous electrolytes, a distinct degradation pathway involves the polymerization of reduced semiquinone radicals to form oligomeric products. This radical coupling pathway is analogous to viologen dimerization but produces higher molecular weight species that can precipitate or deposit on electrode surfaces. The extent of polymerization was estimated at approximately 3% after 150 cycles in a benzoquinone-based nonaqueous cell, based on mass balance analysis and electrochemical impedance spectroscopy indicating increased electrode resistance.

## 5. Comparative Analysis of Degradation Pathways Across Organic Chemistries

### 5.1 Degradation Rate Comparison

A systematic comparison of degradation rates across the three organic active species classes reveals important patterns that inform battery design. Under standardized conditions (100 mA/cm2, Nafion 117 membrane, room temperature, 500 cycle duration), the capacity fade rates were: AQDS at pH 12 showed 0.025%/cycle, TEMPO in nonaqueous electrolyte showed 0.02%/cycle, PSV (functionalized viologen) showed 0.018%/cycle, MV at pH 7 showed 0.055%/cycle, and unfunctionalized TEMPO in the presence of 50 ppm water showed 0.045%/cycle.

These results demonstrate that functionalized derivatives consistently outperform their unfunctionalized counterparts due to reduced crossover and improved chemical stability. The AQDS system showed the lowest crossover rate but was more sensitive to pH optimization, with performance degrading substantially outside the narrow pH window of 11-12. The TEMPO system demonstrated good performance in rigorously dried nonaqueous electrolytes but showed accelerated degradation in the presence of water or nucleophilic impurities.

### 5.2 Mechanism Cross-Comparison

The dominant degradation mechanisms differ substantially between the three organic chemistries. TEMPO degradation is primarily driven by disproportionation of the oxoammonium form and radical dimerization, both of which are concentration- and temperature-dependent. Viologen degradation is dominated by radical cation dimerization and, under alkaline conditions, nucleophilic attack on the bipyridinium framework. Quinone degradation is primarily driven by nucleophilic addition to the oxidized ring and autoxidation of the reduced form.

An important cross-cutting mechanism is membrane crossover, which affects all three species but to different extents. The crossover rates through Nafion 117 follow the order: MV (2.1 x 10^-6 cm2/s) > TEMPO (0.8 x 10^-6 cm2/s) > AQDS (0.2 x 10^-6 cm2/s). This ordering reflects the combined effects of molecular size, charge, and hydrophobicity on membrane transport. The high crossover rate of MV is particularly problematic due to its small dicationic structure, while the sulfonate groups of AQDS provide effective electrostatic exclusion from the cation exchange membrane.

The SOC imbalance induced by differential crossover rates represents a system-level degradation mechanism that couples the two half-cells. When one species crosses over more rapidly than its counterpart, an asymmetric capacity fade develops between the catholyte and anolyte. In a MV/TEMPO cell, the higher MV crossover rate led to an SOC imbalance of 15% after 300 cycles. In contrast, an AQDS/TEMPO cell with better matched crossover rates showed only 7% SOC imbalance over the same duration.

### 5.3 Dimerization and Coupling Pathways

The tendency of organic radicals to undergo coupling or dimerization represents a shared degradation mechanism across all three chemistries, though with different kinetic parameters. TEMPO radical dimerization proceeds with an estimated rate constant of approximately 0.5 M^-1 s^-1 in acetonitrile, producing a dimerization extent of 5% after 200 cycles at standard concentration. Viologen radical cation dimerization is more rapid, with an estimated rate constant of 2.5 M^-1 s^-1, producing 8% dimerization under equivalent conditions. The benzoquinone semiquinone radical shows the highest dimerization tendency with a rate constant of approximately 4 M^-1 s^-1, though the overall impact is moderated by the lower radical concentration in the two-electron redox mechanism.

Steric protection through molecular design has proven effective across all three platforms. Bulky substituents adjacent to the redox center reduce the dimerization rate by increasing the activation barrier for radical approach. For TEMPO, substitution at the 4-position with a tert-butyl group reduced the dimerization extent from 5% to 2% over 200 cycles. For viologens, benzyl substituents at the nitrogen positions reduced dimerization from 8% to 4%. These modifications demonstrate the generalizability of steric protection as a stabilization strategy.

## 6. Membrane and System Design Considerations

### 6.1 Membrane Selectivity and Performance Impact

The selection of membrane material profoundly impacts the degradation rate and overall performance of organic redox flow batteries. Five membrane configurations were evaluated with a MV/TEMPO cell at 100 mA/cm2: Nafion 117 (selectivity 88%, MV crossover 2.1 x 10^-6 cm2/s, capacity fade 0.055%/cycle), Nafion 212 (selectivity 85%, MV crossover 2.5 x 10^-6 cm2/s, capacity fade 0.065%/cycle), a sulfonated polyether ether ketone (SPEEK) membrane with 40% sulfonation (selectivity 92%, MV crossover 1.2 x 10^-6 cm2/s, capacity fade 0.038%/cycle), a commercial anion exchange membrane (selectivity 90%, MV crossover 1.5 x 10^-6 cm2/s, capacity fade 0.042%/cycle), and a nanoporous size-exclusion membrane (selectivity 97%, MV crossover 0.3 x 10^-6 cm2/s, capacity fade 0.012%/cycle).

The results demonstrate a strong correlation between membrane selectivity and capacity fade rate. The nanoporous size-exclusion membrane, with its 97% selectivity, reduced the capacity fade by a factor of 4.6 compared to Nafion 117. However, this membrane also exhibited higher area-specific resistance (2.8 ohm cm2 compared to 1.8 ohm cm2 for Nafion 117), resulting in a lower EE of 78.5% compared to 80.2% for Nafion at 100 mA/cm2.

For AQDS-based systems, the benefit of high-selectivity membranes is less pronounced due to the inherently low crossover rate of the sulfonated quinone. With Nafion 117 (selectivity 94% for AQDS), the capacity fade rate was already low at 0.025%/cycle. Switching to the size-exclusion membrane (selectivity 98%) reduced this only marginally to 0.018%/cycle, while decreasing the EE from 78.5% to 76.2% at 100 mA/cm2 due to higher membrane resistance.

### 6.2 SOC Imbalance Management

SOC imbalance develops when the crossover rates of the two active species differ, leading to asymmetric capacity utilization. In a MV/TEMPO system with Nafion 117, the SOC imbalance reached 15% after 300 cycles, as the higher MV crossover rate depleted the anolyte side more rapidly. This imbalance manifests as a decrease in accessible capacity and can eventually lead to electrolyte remixing if the imbalance exceeds safe operating thresholds.

Several strategies have been demonstrated for managing SOC imbalance. Periodic remixing of the electrolytes (every 200 cycles) restored the SOC balance but incurred a temporary capacity penalty and operational downtime. The use of symmetry-breaking additives, such as a small concentration of redox-inert salt on the high-crossover side, can partially compensate for differential crossover. In the MV/TEMPO system, addition of 0.05 M tetraethylammonium chloride to the catholyte reduced the SOC imbalance from 15% to 9% over 300 cycles by slowing TEMPO crossover through a common-ion effect.

The most effective approach to managing SOC imbalance is the use of matched crossover pairs, where both active species have similarly low crossover rates. The AQDS/PSV pairing exemplifies this strategy, with crossover rates of 0.2 x 10^-6 cm2/s and 0.4 x 10^-6 cm2/s respectively, resulting in an SOC imbalance of only 5% after 300 cycles with Nafion 117.

## 7. Mitigation Strategies and Molecular Design Principles

### 7.1 Functionalization Strategies

Molecular functionalization has emerged as the most effective approach for stabilizing organic active species against the degradation mechanisms described above. For TEMPO derivatives, substitution at the 4-position with electron-donating groups increases the stability of the oxoammonium form against nucleophilic attack. A 4-acetamido-TEMPO derivative demonstrated a capacity fade rate of 0.012%/cycle compared to 0.02%/cycle for unmodified TEMPO, attributed to the electron-donating acetamido group stabilizing the charged oxidation product.

For viologens, the primary functionalization strategy involves adding bulky or charged substituents to the nitrogen positions. Sulfonate-functionalized viologens combine steric protection against dimerization with reduced crossover due to electrostatic repulsion from cation exchange membranes. A viologen derivative with two propylsulfonate groups demonstrated a dimerization extent of only 3% after 200 cycles (compared to 8% for MV) and a crossover rate of 0.4 x 10^-6 cm2/s (compared to 2.1 x 10^-6 cm2/s for MV).

For quinones, sulfonation at positions remote from the redox center provides the dual benefits of increased water solubility and reduced membrane crossover. Additional functionalization with electron-withdrawing groups can tune the redox potential while modifying the susceptibility to nucleophilic attack. A tetrafluoro-substituted anthraquinone derivative demonstrated improved stability at pH 14, with the capacity fade rate reduced from 0.068%/cycle for AQDS to 0.035%/cycle, attributed to the electron-withdrawing fluorine groups reducing the electrophilicity of the quinone ring toward nucleophilic attack.

### 7.2 Electrolyte Engineering

The composition of the supporting electrolyte significantly influences the degradation rate of organic active species. For TEMPO-based nonaqueous systems, rigorous water exclusion is paramount. The capacity fade rate increased from 0.02%/cycle at 10 ppm water content to 0.035%/cycle at 50 ppm, 0.055%/cycle at 200 ppm, and 0.08%/cycle at 500 ppm. These data establish a critical threshold of approximately 100 ppm water content for maintaining acceptable stability.

For aqueous viologen systems, pH optimization represents the primary electrolyte engineering lever. Operation at pH 8-9 provides the best balance of viologen stability and cell performance, avoiding both acid-catalyzed decomposition and alkaline nucleophilic attack. Buffer selection is also important, as certain buffer species can participate in unwanted side reactions. Phosphate buffers at pH 7-8 provided stable performance over 500 cycles, while borate buffers at pH 9 showed slight buffer decomposition contributing an additional 0.008%/cycle capacity fade.

For quinone systems, oxygen exclusion is the most critical electrolyte engineering requirement. Dissolved oxygen levels must be maintained below 0.1 ppm to prevent autoxidation of the reduced anthrahydroquinone form. Nitrogen sparging of electrolyte reservoirs, combined with oxygen-impermeable tubing and seals, achieved the necessary oxygen exclusion. Addition of catalase enzyme (0.01 mg/mL) to the electrolyte provided additional protection by decomposing trace hydrogen peroxide that can form through oxygen reduction, further reducing the capacity fade rate by approximately 0.005%/cycle.

### 7.3 System-Level Design Approaches

Beyond molecular and electrolyte engineering, system-level design choices significantly impact the long-term stability of ORFBs. The implementation of SOC limits to avoid overcharging or over-discharging has proven highly effective. For TEMPO-based systems, limiting the SOC window to 10-85% reduced the capacity fade rate by 48% compared to 5-95% operation, by avoiding the high-concentration regimes where disproportionation and dimerization are accelerated.

Flow rate optimization also plays a role in stability. Higher flow rates improve mass transport and reduce concentration polarization, but also increase membrane crossover by enhancing convective transport. An optimal linear flow velocity of 10-15 cm/s was identified for TEMPO/viologen cells with Nafion 117, balancing mass transport requirements against crossover-induced fade.

Temperature control represents a final system-level lever. All degradation mechanisms exhibit Arrhenius-type temperature dependence, with degradation rates increasing by a factor of 1.5-2.5 for every 10 C increase in temperature. Operating at reduced temperature (15 C rather than 25 C) reduced the capacity fade rate of a MV/TEMPO cell from 0.055%/cycle to 0.032%/cycle, albeit with some performance penalty due to increased electrolyte viscosity (EE decreased from 80.2% to 77.5% at 100 mA/cm2).

## 8. Conclusions and Outlook

This review has provided a comprehensive analysis of the stability and degradation mechanisms of three leading organic active species classes for redox flow batteries: TEMPO-based nitroxyl radicals, viologen-based bipyridinium salts, and quinone derivatives. Each chemistry presents a distinct set of degradation challenges that must be addressed through tailored molecular design, electrolyte engineering, and system optimization.

TEMPO degradation is dominated by oxoammonium disproportionation and radical dimerization, with water content and SOC management being the critical control parameters. With appropriate functionalization and water exclusion, TEMPO-based catholytes can achieve capacity fade rates below 0.015%/cycle with CE exceeding 98% and EE above 83% at 100 mA/cm2. Viologen degradation is primarily driven by radical cation dimerization and nucleophilic attack, with steric protection through bulky substituents and pH optimization providing effective mitigation. Functionalized viologens can achieve capacity fade rates below 0.02%/cycle with CE exceeding 98%. Quinone degradation proceeds through nucleophilic addition and autoxidation pathways, with pH optimization and oxygen exclusion being the most critical mitigation strategies. AQDS at optimal pH 12 demonstrates capacity fade rates as low as 0.012%/cycle with CE exceeding 95%.

The comparison across chemistries reveals several universal design principles. Membrane selectivity above 95% is essential for minimizing crossover-induced fade, regardless of the active species employed. SOC imbalance management through matched crossover pairs or periodic remixing is necessary for long-term capacity retention. Steric protection of radical intermediates through bulky substituents is broadly applicable across nitroxyl, viologen, and semiquinone platforms. Electrolyte purity, particularly water and oxygen exclusion, is a cross-cutting requirement.

Future research directions should focus on the development of next-generation organic active species that combine the best features of each class: the fast kinetics and high stability of functionalized TEMPO, the tunable potential and steric protection of modified viologens, and the low crossover and aqueous compatibility of sulfonated quinones. The continued advancement of organic redox flow batteries depends on the systematic application of the molecular design principles and degradation mitigation strategies outlined in this review.
---

# DOC10: Cross-System Design Rules and Strategy Comparison for Redox Flow Batteries: A Multi-Platform Analysis

## Abstract

The diversity of redox flow battery (RFB) chemistries presents both opportunities and challenges for technology development. While each system - all-vanadium (VRFB), iron-chromium (ICRFB), zinc-bromine (Zn-Br), soluble lead-acid (SLA), and organic (ORFB) - possesses unique operational characteristics and degradation mechanisms, certain design principles exhibit remarkable transferability across platforms. This review systematically compares membrane selection rules, electrode modification strategies, electrolyte additive approaches, and flow field design principles across five major RFB chemistries. Through quantitative analysis of energy efficiency, capacity fade mechanisms, and cost-performance trade-offs at matched power densities, we identify universally applicable design heuristics and chemistry-specific adaptations required for optimal performance. Our analysis reveals that membrane selectivity requirements above 95% are universal, electrode surface area enhancement benefits all systems but through different mechanisms, additive strategies are highly chemistry-dependent, and flow field optimization follows common fluid dynamic principles with chemistry-specific constraints. These cross-system insights enable accelerated development of new RFB chemistries by leveraging proven design strategies from mature systems.

## 1. Introduction: The Case for Cross-System Design Analysis

Redox flow batteries encompass a broad spectrum of electrochemical couples, each developed through largely independent research trajectories. The all-vanadium system has achieved the highest technology readiness level, with multiple megawatt-scale installations worldwide. Iron-chromium systems have been pursued for their potential cost advantages using earth-abundant elements. Zinc-bromine technology has found niche applications in stationary storage. Soluble lead-acid chemistry offers a potentially low-capital-cost alternative leveraging existing lead-acid infrastructure. Organic systems represent the frontier of molecularly engineered energy storage.

The conventional approach of developing each system independently has led to significant duplication of effort and missed opportunities for knowledge transfer. Electrode modifications developed for VRFBs may benefit zinc-bromine systems facing similar kinetic limitations. Membrane selection criteria established for all-vanadium systems provide a foundation for organic RFB development. Flow field optimization insights from the fuel cell community, adapted for zinc-bromine systems, may transfer to soluble lead-acid configurations.

This review addresses the following central question: Which design strategies are genuinely transferable across RFB chemistries, and which require fundamental adaptation? We analyze four critical design domains - membrane selection, electrode modification, electrolyte additives, and flow field design - across five representative RFB systems. For each domain, we establish quantitative performance benchmarks and identify the underlying physics and chemistry that determine transferability.

## 2. System Definitions and Baseline Performance Characteristics

### 2.1 All-Vanadium Redox Flow Battery (VRFB)

The VRFB employs V2+/V3+ and VO2+/VO2+ redox couples in sulfuric acid electrolyte, typically at concentrations of 1.5-2.0 M vanadium. The standard cell voltage is 1.26 V. With Nafion 117 membrane, VRFBs achieve energy efficiency of 78-84% at current densities of 100-200 mA/cm2. At 100 mA/cm2, a typical system achieves EE of 84% and CE of 96%. At 150 mA/cm2, the EE decreases to 81% with CE of 95%. At 200 mA/cm2, the EE further decreases to 78% with CE of 94%. The primary degradation mechanism is vanadium crossover through the membrane, leading to capacity fade rates of 0.02-0.05%/cycle depending on membrane selection and operating conditions.

The VRFB benefits from the use of a single element in both half-cells, eliminating cross-contamination concerns, but suffers from high vanadium cost and relatively low energy density. The sulfuric acid supporting electrolyte at 2-3 M concentration provides adequate ionic conductivity while maintaining vanadium solubility.

### 2.2 Iron-Chromium Redox Flow Battery (ICRFB)

The ICRFB utilizes Fe2+/Fe3+ and Cr2+/Cr3+ redox couples in hydrochloric acid electrolyte. The standard cell voltage is 1.03 V. A critical advancement in ICRFB technology has been the introduction of Bi3+ additives to address the slow kinetics of the Cr3+/Cr2+ reaction. With Bi3+ additive (typically 0.01-0.05 M), ICRFBs achieve energy efficiency of 62-85% at current densities of 80-160 mA/cm2. At 80 mA/cm2, the EE reaches 85% with CE of 97%. At 120 mA/cm2, the EE is 75% with CE of 95%. At 160 mA/cm2, the EE decreases to 62% with CE of 92%.

Without Bi3+ additive, the chromium kinetics are sufficiently sluggish that the EE at 80 mA/cm2 drops to approximately 55%, rendering the system impractical for commercial deployment. The Bi3+ additive is believed to catalyze the chromium reduction reaction through underpotential deposition or surface modification of the electrode. The hydrogen evolution reaction represents a significant parasitic process on the chromium side, particularly at high current densities, contributing to CE loss.

### 2.3 Zinc-Bromine Flow Battery (Zn-Br)

The zinc-bromine system operates through zinc plating/stripping at the negative electrode and bromine/bromide redox at the positive electrode. The standard cell voltage is 1.85 V. Zinc-bromine systems achieve energy efficiency of 64-78% at current densities of 40-80 mA/cm2. At 40 mA/cm2, the EE reaches 78% with CE of 93%. At 60 mA/cm2, the EE is 71% with CE of 90%. At 80 mA/cm2, the EE decreases to 64% with CE of 87%.

The primary degradation mechanisms include zinc dendrite formation during plating, bromine crossover through the microporous separator, and self-discharge through bromine diffusion. The system employs a microporous separator rather than an ion exchange membrane, with bromine complexing agents (typically quaternary ammonium bromides) to sequester elemental bromine as a dense oil phase. Zinc dendrite management requires precise current density control and periodic stripping cycles.

### 2.4 Soluble Lead-Acid Flow Battery (SLA)

The soluble lead-acid system operates through Pb2+/Pb plating at the negative electrode and Pb2+/PbO2 deposition at the positive electrode in methanesulfonic acid (MSA) electrolyte. The standard cell voltage is 1.45 V. SLA systems achieve energy efficiency of 58-78% at current densities of 20-40 mA/cm2. At 20 mA/cm2, the EE reaches 78% with CE of 89%. At 30 mA/cm2, the EE is 68% with CE of 85%. At 40 mA/cm2, the EE decreases to 58% with CE of 82%.

The SLA system faces unique challenges related to electrodeposit morphology control. Lead dioxide deposition at the positive electrode must achieve adequate adhesion and surface area while avoiding excessive roughening that promotes dendrite formation. Methanesulfonic acid at 1-2 M concentration serves as both supporting electrolyte and lead solvent, with lead methanesulfonate typically at 0.5-1.0 M concentration. The system operates at modest current densities due to the kinetic limitations of the PbO2 deposition reaction and ohmic losses in the MSA electrolyte.

### 2.5 Organic Redox Flow Battery (ORFB)

Organic redox flow batteries employ molecularly engineered organic active species, with the most promising systems utilizing TEMPO-based catholytes and viologen or quinone-based anolytes. Representative systems achieve energy efficiency of 76-88% at current densities of 20-100 mA/cm2. At 20 mA/cm2, the EE reaches 88% with CE of 99%. At 60 mA/cm2, the EE is 83% with CE of 97%. At 100 mA/cm2, the EE decreases to 76% with CE of 95%.

The ORFB platform exhibits the greatest diversity in electrolyte composition, operating pH, and membrane selection. Nonaqueous systems using acetonitrile or propylene carbonate solvents require rigorous water exclusion, while aqueous systems operate from neutral to strongly alkaline pH depending on the active species. Degradation mechanisms include radical dimerization, nucleophilic attack, and membrane crossover, with mitigation strategies highly specific to the molecular structures employed.

## 3. Membrane Selection Rules Across RFB Platforms

### 3.1 Membrane Performance Requirements and Metrics

Membrane selection represents one of the most critical and transferable design decisions across RFB platforms. The essential function of the membrane is to transport charge-carrying ions while preventing active species crossover. Two key metrics quantify membrane performance: ionic conductivity (or area-specific resistance, ASR) and selectivity (the ratio of ionic transport to active species crossover).

For all five RFB systems, membrane selectivity above 95% is required to achieve capacity fade rates below 0.02%/cycle. This threshold emerges from the universal relationship between crossover rate and capacity fade: even modest crossover of electroactive species leads to irreversible capacity loss through chemical reaction with the opposing electrolyte. With Nafion 117 (selectivity approximately 88-94% depending on the active species), all systems exhibit capacity fade rates above 0.02%/cycle. Switching to higher-selectivity membranes (selectivity 96-98%) reduces fade rates below this threshold for all chemistries except systems with intrinsically high crossover species.

The area-specific resistance (ASR) of the membrane directly impacts energy efficiency at a given current density. For a target EE penalty from membrane resistance of less than 3%, the ASR must satisfy R_ASR < 0.03 * V_cell / j, where V_cell is the cell voltage and j is the current density. At 100 mA/cm2 with a 1.5 V cell, this requires R_ASR < 4.5 ohm cm2. All commercially available ion exchange membranes satisfy this criterion, but the margin becomes tighter at higher current densities.

### 3.2 Chemistry-Specific Membrane Selection

For VRFB systems, Nafion membranes (Nafion 117, 115, 212) have been the benchmark due to their excellent proton conductivity, chemical stability in sulfuric acid, and mechanical durability. The proton transport mechanism in Nafion is well-matched to the VRFB electrolyte. However, vanadium crossover through Nafion remains a significant issue due to the multiple vanadium oxidation states and their varying charge densities. Alternative membranes including sulfonated polyether ether ketone (SPEEK) and sulfonated polystyrene have shown improved vanadium selectivity (up to 96-97%) with comparable conductivity. At 100 mA/cm2, a SPEEK membrane with 42% sulfonation degree achieved an EE of 83% compared to 84% for Nafion 117, but reduced the capacity fade rate from 0.035%/cycle to 0.018%/cycle.

For ICRFB systems, the membrane must be stable in hydrochloric acid and resist iron and chromium crossover. Nafion membranes perform adequately but show somewhat higher chromium crossover than vanadium crossover due to the smaller ionic radius of Cr3+ compared to VO2+. An anion exchange membrane (AEM) approach has been explored for ICRFBs, using chloride transport rather than proton transport. A benchmark AEM (Fumatech FAP-450) achieved an EE of 79% at 100 mA/cm2 with iron-chromium electrolyte, compared to 82% for Nafion 117, but with significantly improved chromium retention (crossover rate reduced by 40%).

For zinc-bromine systems, the conventional approach uses a microporous separator rather than an ion exchange membrane. The microporous polyolefin separator provides ion transport through the entrained electrolyte while blocking bulk bromine flow. The separator ASR is typically 1.5-2.5 ohm cm2, higher than Nafion but acceptable given the lower operating current densities (40-80 mA/cm2). The selectivity mechanism is primarily physical size exclusion rather than Donnan exclusion. The bromine crossover rate through the microporous separator is approximately 1.8 x 10^-6 cm2/s, significantly higher than vanadium crossover through Nafion, but the self-discharge rate is partially mitigated by bromine complexation agents.

For SLA systems, membrane selection must balance acid stability, lead ion rejection, and low resistance. Nafion membranes show good stability in MSA electrolyte but allow significant Pb2+ crossover due to the divalent cation character. A nanoporous ceramic-polymer composite membrane demonstrated improved lead rejection (selectivity 93%) with an ASR of 3.2 ohm cm2, achieving an EE of 74% at 30 mA/cm2 compared to 76% with Nafion 117 but with reduced capacity fade from 0.08%/cycle to 0.04%/cycle.

For ORFB systems, membrane selection is highly dependent on the solvent and active species. In aqueous systems with sulfonated active species (AQDS, PSV), Nafion provides good selectivity (94-96%) due to Donnan exclusion of anionic species. In nonaqueous systems with neutral species (TEMPO), selectivity is lower (85-88% with Nafion) due to the lack of charge-based exclusion. Size-exclusion membranes with controlled pore distributions have shown improved selectivity (96-98%) for nonaqueous ORFBs but at the cost of higher ASR (2.5-3.5 ohm cm2).

### 3.3 Transferable Membrane Design Rules

Several membrane design principles emerge as transferable across all five systems. First, the selectivity threshold of 95% is universal - no system tolerates high crossover without significant capacity fade. Second, thinner membranes improve EE but generally reduce selectivity, requiring system-level optimization. Third, membrane preconditioning (soaking in supporting electrolyte before assembly) improves initial performance consistency across all chemistries. Fourth, operating temperature affects both conductivity and selectivity through solution viscosity and diffusion coefficient changes, with Arrhenius-type behavior observed universally.

The key non-transferable aspect is the specific transport mechanism required. VRFB, ICRFB, and aqueous ORFB rely on proton or cation transport. Zn-Br uses anion transport through a microporous medium. Nonaqueous ORFB requires specific cation transport in organic solvents. SLA systems must manage divalent cation transport. These differences preclude direct membrane substitution but do not invalidate the general selection framework.

## 4. Electrode Modification Strategies Across Platforms

### 4.1 Electrode Materials and Baseline Performance

Carbon-based electrodes dominate RFB applications due to their chemical stability, high surface area, and acceptable cost. Carbon felt electrodes (typically 3-5 mm thickness, 0.5-4 um fiber diameter, 90-95% porosity) are standard across all five systems. Graphite plate current collectors provide electrical contact and flow distribution.

The baseline performance of untreated carbon felt varies significantly across systems due to differing kinetic requirements. For the VRFB, the V2+/V3+ and VO2+/VO2+ reactions show moderate overpotentials on carbon felt, with charge transfer resistances of 0.8-1.2 ohm cm2. For the ICRFB without additives, the Cr3+/Cr2+ reaction exhibits very high overpotential (charge transfer resistance 3-5 ohm cm2), while the Fe2+/Fe3+ reaction is facile (0.3-0.5 ohm cm2). For Zn-Br, the bromine reaction is facile on carbon (0.2-0.4 ohm cm2) but zinc plating requires nucleation sites. For SLA, the PbO2 deposition reaction shows high overpotential (2-4 ohm cm2) while lead plating is more facile (0.5-1.0 ohm cm2). For ORFB, TEMPO oxidation shows moderate overpotential (0.6-1.0 ohm cm2) while viologen reduction is relatively facile (0.3-0.5 ohm cm2).

### 4.2 Surface Treatment and Catalytic Modification

Thermal treatment of carbon felt in air at 400-500 C for 4-6 hours introduces oxygen-containing functional groups (carboxyl, hydroxyl, carbonyl) that improve wettability and provide catalytic sites. This treatment benefits all five systems but to different degrees. For VRFB, thermal treatment reduces the charge transfer resistance by 20-30% for the vanadium reactions, improving EE by 2-3 percentage points at 100 mA/cm2. For ICRFB, the effect is more dramatic: thermal treatment reduces the chromium reaction resistance by 40-50%, improving EE by 5-7 percentage points at 100 mA/cm2. For Zn-Br, thermal treatment improves zinc nucleation uniformity, reducing dendrite formation tendency. For SLA, thermal treatment reduces PbO2 deposition overpotential by 25-35%, improving EE by 3-4 percentage points at 30 mA/cm2. For ORFB, thermal treatment improves TEMPO oxidation kinetics by 15-20%, contributing 1-2 percentage points EE improvement at 100 mA/cm2.

Metal and metal oxide catalyst coatings provide more aggressive kinetic enhancement. For VRFB, Bi2O3 coating on carbon felt (loading 0.1-0.3 mg/cm2) improves the negative electrode kinetics, increasing EE from 84% to 86% at 100 mA/cm2. For ICRFB, Bi3+ additive in the electrolyte (0.01-0.05 M) combined with Bi-modified electrodes provides synergistic catalysis, increasing EE from 82% to 85% at 80 mA/cm2. For Zn-Br, TiN coating on the negative electrode improves zinc plating uniformity and suppresses dendrite formation, extending cycle life by 30-40%. For SLA, PbO2-coated titanium mesh positive electrodes eliminate the need for in-situ deposition, simplifying operation but adding cost. For ORFB, Pt nanoparticle decoration (0.05-0.1 mg/cm2) improves TEMPO oxidation kinetics but introduces cost and durability concerns.

### 4.3 Transferable Electrode Modification Rules

The transferable principles from electrode modification studies include: (1) Surface area enhancement benefits all systems, with a roughly linear relationship between accessible surface area and kinetic performance up to a saturation point; (2) Wettability improvement through oxidation treatment universally improves electrolyte distribution and reduces mass transport losses; (3) Catalytic coatings are most beneficial for systems with intrinsically slow kinetics (ICRFB chromium, SLA PbO2) and less critical for systems with facile redox reactions (VRFB, ORFB); (4) electrode compression in the range of 10-20% of original thickness optimizes the trade-off between electrical contact and flow permeability across all systems.

Non-transferable aspects include: (1) The specific catalytic materials required differ substantially - Bi for chromium, TiN for zinc, PbO2 for lead, Pt for some organics; (2) Depositing systems (Zn-Br, SLA) require electrode designs that accommodate solid phase changes; (3) The optimal pore size distribution varies with active species size and electrolyte viscosity.

## 5. Electrolyte Additive Strategies Across Platforms

### 5.1 Additive Classification and Mechanisms

Electrolyte additives serve diverse functions across RFB platforms: kinetic catalysis, stability enhancement, precipitation suppression, and conductivity modification. Unlike membrane and electrode strategies, additive approaches show the lowest transferability across systems due to the highly specific chemical interactions involved.

### 5.2 Chemistry-Specific Additive Strategies

For VRFB systems, additives have focused on improving thermal stability and expanding the operating temperature window. Phosphate buffer additives (0.1-0.5 M) stabilize vanadium species against thermal precipitation, enabling operation up to 50 C compared to 35 C for unbuffered electrolyte. Amino acid additives (glycine, 0.1 M) have shown modest CE improvement (1-2 percentage points) through complexation with vanadium ions that reduces crossover. However, additive benefits in VRFB are relatively modest because the all-vanadium chemistry inherently avoids cross-contamination.

For ICRFB systems, the Bi3+ additive represents the most impactful additive strategy in RFB development. At 0.01-0.05 M Bi3+ concentration in the electrolyte, the chromium reduction overpotential is reduced by 200-300 mV, transforming the system from impractical (EE ~55% at 80 mA/cm2) to commercially viable (EE ~85% at 80 mA/cm2). The Bi3+ is believed to deposit as metallic Bi or BiOCl on the electrode surface during charging, providing catalytic sites for the chromium reduction. The additive is consumed gradually (approximately 0.001 M per 100 cycles), requiring periodic replenishment. Other ICRFB additives include HCl concentration optimization (2-3 M) to balance conductivity with corrosion, and thiourea additions (0.001-0.01 M) to suppress hydrogen evolution.

For Zn-Br systems, additives are essential for both electrodeposit control and bromine management. Quaternary ammonium bromides (tetramethylammonium bromide, N-methyl-N-ethylpyrrolidinium bromide) at 0.5-1.0 M concentration form polybromide complex phases that sequester elemental bromine, reducing self-discharge and bromine vapor pressure. Zinc coordination additives (ethylene diamine tetraacetic acid derivatives at 0.01-0.05 M) modify the zinc plating morphology, promoting smooth deposits and suppressing dendrite formation. Surfactant additives (polyethylene glycol, 0.001-0.01 M) further improve zinc deposit uniformity by adsorbing at the electrode interface.

For SLA systems, additives focus on deposit morphology control and electrolyte stability. Gelatin (0.01-0.1 g/L) and lignosulfonate (0.05-0.5 g/L) are added as leveling agents that promote smooth PbO2 deposition by adsorbing at high-surface-energy sites. Copper additives (0.001-0.01 M Cu2+) improve the conductivity and adhesion of lead dioxide deposits. Fluoride additives (0.01-0.05 M NaF) stabilize the MSA electrolyte against decomposition during extended cycling.

For ORFB systems, additives address the diverse degradation mechanisms of organic active species. For TEMPO systems, molecular sieves (3A or 4A) in the electrolyte reservoir maintain water content below 50 ppm, critical for preventing oxoammonium disproportionation. For viologen systems, buffer selection (phosphate at pH 7-8, borate at pH 9) maintains optimal pH while avoiding buffer decomposition. For quinone systems, catalase enzyme (0.01 mg/mL) decomposes trace hydrogen peroxide that forms through oxygen reduction. Redox-active stabilizers (hydroquinone derivatives at 0.001-0.01 M) can scavenge radical intermediates that participate in degradation pathways.

### 5.3 Transferable Additive Principles

Despite the chemistry-specific nature of additive selection, several transferable principles emerge: (1) Interface-active additives (surfactants, leveling agents) that adsorb at electrode surfaces generally improve deposit morphology across all depositing systems (Zn-Br, SLA); (2) Antioxidant-type additives that scavenge reactive intermediates benefit systems with redox-active degradation pathways (TEMPO disproportionation, quinone autoxidation); (3) Buffer systems for pH control improve CE universally in aqueous systems by suppressing parasitic proton/hydroxide transport; (4) Additive stability over long cycling must be verified, as consumed additives create operational complexity.

The most significant transferable insight is that additive strategies are most impactful when addressing the rate-limiting step of a given system. For ICRFB, the rate-limiting step is chromium kinetics, and the Bi3+ additive directly addresses this. For Zn-Br, the rate-limiting concerns are dendrite formation and bromine management, and additives directly target these. This principle - identify the rate-limiting challenge and design additives that specifically address it - applies universally but yields entirely different additive choices for each system.

## 6. Flow Field Design and System Engineering

### 6.1 Flow Field Configurations and Performance Impact

Flow field design determines the distribution of electrolyte across the electrode surface and significantly impacts mass transport, pressure drop, and shunt current. Three primary flow field configurations are employed across RFB systems: serpentine, interdigitated, and parallel channel designs.

For VRFB systems operating at 100-200 mA/cm2, the interdigitated flow field provides the best balance of mass transport enhancement and pressure drop. At 150 mA/cm2, an interdigitated design with 1 mm channel width and 1 mm rib width achieved an EE of 82% compared to 79% for a serpentine design with equivalent channel dimensions. The improvement arises from forced convective flow through the porous electrode in the interdigitated configuration, reducing concentration boundary layer thickness. However, the pressure drop increased from 0.3 bar to 0.8 bar, requiring higher pumping power.

For ICRFB systems, the serpentine flow field is preferred due to the lower operating current densities (80-160 mA/cm2) and the need for uniform distribution to avoid localized hydrogen evolution. At 120 mA/cm2 with Bi3+ additive, a serpentine design achieved an EE of 75% with pressure drop of 0.4 bar, while an interdigitated design achieved only 76% EE at the cost of 1.0 bar pressure drop, rendering the modest performance gain unjustified.

For Zn-Br systems, the flow field must accommodate two-phase flow (zinc solid and liquid electrolyte at the negative electrode) and manage bromine complex phase distribution. A modified serpentine design with wider channels (2 mm) and periodic expansion regions provides space for zinc deposit growth without flow blockage. At 60 mA/cm2, this design achieved an EE of 71% with stable operation over 200 cycles, while a standard interdigitated design showed flow maldistribution and 8% performance degradation after 100 cycles due to zinc accumulation in channel corners.

For SLA systems, the low operating current density (20-40 mA/cm2) and the presence of solid deposit phases require careful flow field design. A parallel channel design with 1.5 mm channels and distributed inlet manifolding provides uniform flow distribution with low pressure drop (0.15 bar at 30 mA/cm2). At 30 mA/cm2, this design achieved an EE of 68%, comparable to serpentine designs but with 40% lower pumping power. The avoidance of sharp channel bends is particularly important for SLA systems to prevent deposit accumulation and flow blockage.

For ORFB systems, flow field requirements vary with solvent viscosity and active species concentration. Aqueous systems using AQDS or viologen electrolytes (viscosity similar to water) perform well with interdigitated designs at 60-100 mA/cm2. At 100 mA/cm2, an interdigitated design achieved an EE of 80% for an AQDS/TEMPO cell compared to 77% for a serpentine design. Nonaqueous systems using acetonitrile (lower viscosity) show less sensitivity to flow field configuration due to intrinsically better mass transport characteristics.

### 6.2 Transferable Flow Field Design Rules

Flow field design exhibits the highest transferability across RFB platforms, as the underlying physics of fluid flow in porous media and electrochemical mass transport are largely chemistry-independent. The transferable principles include: (1) The dimensionless Damkohler number (ratio of reaction rate to transport rate) determines whether flow field optimization significantly impacts performance - systems with high Damkohler numbers (ICRFB chromium, SLA PbO2) benefit most; (2) The Péclet number (ratio of convective to diffusive transport) should be maintained in the range of 1-10 for optimal mass transport without excessive pressure drop; (3) Channel aspect ratio (width/depth) of 0.5-2.0 provides a good balance between electrode utilization and manufacturing simplicity across all systems; (4) Manifold design must achieve uniform flow distribution with less than 5% variation in flow rate across all channels to avoid localized performance degradation.

System-specific adaptations include: (1) Depositing systems (Zn-Br, SLA) require flow fields that accommodate solid phase growth without blockage; (2) Systems with gas evolution (ICRFB hydrogen, VRFB oxygen at overcharge) require flow field features that facilitate gas removal; (3) The optimal linear flow velocity varies with electrolyte viscosity, ranging from 5-10 cm/s for aqueous systems to 10-20 cm/s for nonaqueous ORFBs due to lower viscosity and different diffusion coefficients.

## 7. Cross-System Performance Comparison at Matched Conditions

### 7.1 Energy Efficiency Comparison

A direct comparison of energy efficiency across the five systems at their respective typical current densities reveals the performance landscape. At 100 mA/cm2 (where comparable data exist), the EE ranking is: ORFB 80-83% > VRFB 81-84% > ICRFB with Bi3+ 75-82% > Zn-Br not typically operated at 100 mA/cm2 > SLA not typically operated at 100 mA/cm2. At 60 mA/cm2, the ranking is: ORFB 83-86% > VRFB 83-86% > ICRFB with Bi3+ 82-85% > Zn-Br 71% > SLA not typically operated at 60 mA/cm2.

The higher EE of ORFB systems reflects the fast kinetics of organic redox couples and the lower ASR of thin membranes used in laboratory-scale cells. The VRFB achieves comparable EE due to the well-optimized membrane-electrode interface and extensive system development. The ICRFB with Bi3+ additive approaches VRFB performance but only at lower current densities where kinetic limitations are less severe. The Zn-Br and SLA systems operate at lower current densities due to deposit morphology constraints, achieving moderate EE at their design points.

### 7.2 Capacity Fade Comparison

Capacity fade rates at matched cycle numbers (500 cycles) and with optimized membranes show the following ranking from lowest to highest fade: AQDS-based ORFB 0.01-0.015%/cycle < TEMPO-PEG ORFB 0.015%/cycle < VRFB with SPEEK 0.018%/cycle < PSV ORFB 0.018%/cycle < ICRFB with AEM 0.025%/cycle < standard VRFB with Nafion 0.035%/cycle < Zn-Br with standard separator 0.04-0.06%/cycle < SLA with ceramic membrane 0.04%/cycle < MV-based ORFB with Nafion 0.055%/cycle.

The organic systems with functionalized species and optimized membranes show the best capacity retention due to low crossover rates and molecular engineering of stability. The VRFB with advanced membranes approaches this performance. The depositing systems (Zn-Br, SLA) show higher fade rates due to the mechanical complexity of solid phase cycling, including active material loss through particle shedding and morphology degradation.

### 7.3 Cost-Performance Trade-offs

The system cost per kWh of energy storage capacity varies significantly across the five platforms. VRFB systems cost approximately 350-500 $/kWh, dominated by vanadium electrolyte (60% of total cost) and membrane (15%). ICRFB systems target 200-350 $/kWh, with lower material costs but higher system complexity due to the additive requirement. Zn-Br systems achieve 150-300 $/kWh, benefiting from low-cost materials but requiring complex bromine management systems. SLA systems target the lowest cost at 100-250 $/kWh due to inexpensive lead and simple cell construction, but face cycle life limitations. ORFB systems currently cost 400-800 $/kWh in laboratory quantities, with potential for reduction to 150-300 $/kWh at scale due to synthetic accessibility of organic molecules.

## 8. Universal Design Heuristics and Chemistry-Specific Adaptations

### 8.1 Tier 1: Universally Transferable Rules

The following design rules apply with minimal modification across all five RFB systems:

Membrane selectivity above 95% is required for capacity fade below 0.02%/cycle. This threshold is independent of the specific active species and reflects the universal relationship between crossover and capacity loss. All systems benefit from transition from standard Nafion (88-94% selectivity) to advanced membranes (96-98% selectivity).

Electrode surface area enhancement improves performance up to a saturation point. Thermal treatment of carbon felt at 400-500 C provides 2-7 percentage points EE improvement across all systems, with the greatest benefit for systems with slow kinetics.

Flow field optimization based on Damkohler and Péclet number analysis provides transferable guidance. Interdigitated designs benefit high-rate systems, serpentine designs suit moderate-rate systems with uniform distribution requirements, and parallel designs work for low-rate systems where pressure drop minimization is critical.

SOC management within appropriate windows extends cycle life universally. Avoiding 0% and 100% SOC extremes prevents accelerated degradation in all systems, though the specific safe window varies.

### 8.2 Tier 2: Partially Transferable Rules Requiring Adaptation

Membrane transport mechanism selection requires chemistry-specific adaptation. While the selectivity target is universal, the specific ion transport mechanism (proton, cation, anion, or physical pore transport) must match the electrolyte chemistry.

Catalytic electrode modifications address the specific rate-limiting reactions of each system. The principle of catalyzing the rate-limiting step is universal, but the specific catalyst (Bi for ICRFB, TiN for Zn-Br, thermal treatment for VRFB, Pt for some ORFB) is chemistry-dependent.

Additive strategies target system-specific degradation modes. The principle of identifying the rate-limiting challenge and designing specific additives applies universally, but the specific additive choices are not transferable.

### 8.3 Tier 3: Chemistry-Specific Rules

Deposit morphology management applies only to systems with solid phase changes (Zn-Br, SLA). These systems require specialized flow fields, current density protocols, and electrolyte additives that have no analog in all-liquid systems.

Water and oxygen exclusion for nonaqueous ORFBs represents a unique requirement arising from the specific degradation chemistry of TEMPO and related species. The 100 ppm water threshold has no equivalent in aqueous systems.

Bromine complexation in Zn-Br systems addresses a unique challenge of elemental bromine management that has no parallel in other chemistries. The quaternary ammonium bromide additives and two-phase flow management are entirely Zn-Br specific.

## 9. Accelerated Development Through Cross-System Learning

### 9.1 Technology Transfer Framework

The cross-system analysis presented in this review enables an accelerated development framework for emerging RFB chemistries. Rather than developing each new system independently, researchers can identify the most analogous mature system and adapt its proven design strategies.

For new aqueous inorganic systems (e.g., Mn-based, Ti-Mn), the VRFB provides the most relevant precedent for membrane selection, electrode modification, and flow field design. The key adaptation required is addressing the specific redox couple kinetics and any cross-contamination issues.

For new organic systems, the existing ORFB literature provides direct precedent for molecular design, solvent selection, and membrane compatibility. The key adaptation is addressing the specific degradation mechanisms of the new molecular structures.

For hybrid systems combining inorganic and organic couples, design strategies from both VRFB and ORFB platforms may be relevant, with particular attention to membrane compatibility with both species types.

### 9.2 Future Research Directions

Several cross-system research directions emerge from this analysis. First, the development of universal high-selectivity membranes (selectivity >98%) with low ASR (<2 ohm cm2) would benefit all RFB platforms. Second, standardized testing protocols for capacity fade, crossover measurement, and EE determination would enable more rigorous cross-system comparisons. Third, computational screening approaches for additive and catalyst selection, validated across multiple systems, could accelerate optimization of new chemistries. Fourth, life cycle assessment frameworks that account for system-specific degradation modes would enable meaningful comparison of long-term cost-performance across platforms.

## 10. Conclusions

This cross-system analysis of five major redox flow battery platforms reveals a hierarchy of design rule transferability. Membrane selectivity requirements and electrode surface area enhancement emerge as truly universal principles. Flow field optimization provides transferable frameworks with chemistry-specific adaptations for depositing systems and gas evolution. Additive strategies, while following the universal principle of targeting rate-limiting steps, require entirely chemistry-specific implementations.

The quantitative performance comparison at matched conditions shows that ORFB systems with optimized molecular design achieve the highest energy efficiency (76-88%) and lowest capacity fade rates (0.01-0.018%/cycle), followed closely by advanced VRFB configurations (EE 78-84%, fade 0.018-0.035%/cycle). The ICRFB with Bi3+ additive achieves competitive performance at lower current densities (EE 62-85% at 80-160 mA/cm2). The Zn-Br and SLA systems operate at lower current densities and achieve moderate EE (Zn-Br 64-78% at 40-80 mA/cm2, SLA 58-78% at 20-40 mA/cm2) but offer potential cost advantages.

The most impactful transferable insight is that the systematic identification and targeted mitigation of rate-limiting steps - whether kinetic, transport, or stability-related - provides a universal framework for RFB optimization. The specific interventions required differ substantially across chemistries, but the analytical approach applies universally. This framework enables emerging RFB technologies to leverage decades of development experience from mature systems, accelerating the path to cost-effective, long-lifetime energy storage.
