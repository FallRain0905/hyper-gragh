# Numerical investigations of scalable loop-type flow fields with enhanced convective mass transfer for vanadium redox flow batteries

Zexin Zhou, Xu Yang, Nianben Zheng ${ \ " } \oplus _ { \cdot }$ , Zhiqiang Sun \*\*

HunaEgedt 410083,China

# HIGHLIGHTS

·Two innovative flow fields are proposed for enhanced mass transfer for VRFBs. ·The LCFF achieves a system efficiency of $8 0 . 4 ~ \%$ at $3 0 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ · The scaled-up LCFF exhibits a $4 . 3 ~ \%$ higher system efficiency than the SFF.

# ARTICLEINFO

Keywords:
Vanadium redox flow batteries
Loop-type flow field
Loop-type corrugated flow field
Mass transfer

# ABSTRACT

The architecture of flow fields plays a critical role in vanadium redox flow bateries (VRFBs） performance. However,traditional serpentine flow fields (SFF)often suffer from uneven distribution of active species,which limits their efectivenessunder high-power-density conditions.To overcome this limitation,this study presents two modified flow field designs based on the serpentine configuration: the loop-type flow field (LFF)and the loop-type corrugated flow field(LCFF).These innovativedesigns optimizerib distribution and feature corrugated channel surfaces to enhance convective mass transfer and improve reactant uniformity.Three-dimensional numerical simulations indicate that the modified structures provoke disturbances during flow,enhance mass transfer,and lower equilibrium potential during electrochemical reactions,allof which significantly boost VRFB performance.Notably,at a current density of $3 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ,the LCFF achievesa system efficiency of $8 0 . 4 ~ \%$ and an electrolyte utilization of $7 0 . 9 \%$ ,outperforming the LFF by $1 . 4 \%$ and $8 . 1 \%$ ,and the SFF by $3 . 2 \%$ and $1 7 . 1 \ \%$ Furthermore,scale-up studies confirm that the LCFF maintains superior performance,exhibiting a $4 . 3 ~ \%$ higher efficiency than the SFF.This study highlights the effectivenes of theoptimized structures in enhancing battery performance and offers valuable insights for the scaling of VRFB systems.

# 1．Introduction

The global energy crisis demands structural changes in energy systems and a swift transition to renewable sources.While wind and solar energy are abundant [1],they inherently face issues of intermittency and volatility [2],which can lead to supply-demand imbalances and disrupt grid stability.To address these challenges, energy storage systems are essential for smoothing out fluctuations in renewable output and enhancing grid integration capacity [3,4].Among the various energy storage technologies,electrochemical storage stands out for its high reliability and is currently a research hotspot [5,6].Vanadium redox flow batteries (VRFBs) emerge as a highly promising electrochemical storage solution,utilizing different valence states of vanadium ions as active species in positive and negative electrolytes to mitigate self-discharge problems caused by ion crossover [7,8].Nevertheless, the high costs associated with the commercialization of VRFBs pose a significant challenge [9,lO],and enhancing power density is crucial for reducing these costs [11].Optimizing the flow field design is vital for improving the transport of active species,thereby boosting the power density of VRFB[12],and establishing it asa key direction for performance enhancement.

The architecture of flow fields plays a critical role in determining the performance of VRFBs by improving the uniformity of electrolyte distribution in porous electrodes and convective mass transfer eficiency [13-16]. Traditional configurations,including parallel,interdigitated [17],and serpentine flow fields (SFF) [18],have been extensively validated in fuel cell applications.Comparative analyses reveal that the SFF exhibits superior system efficiency compared to parallel designs [19],primarily due to enhanced under-rib convection despite the higher flow resistance [2O].Wang et al. highlighted the key factors influencing convection intensity to mitigate local mass transfer bottlenecks [21], while Dennison et al.established systematic design principles that connect geometric parameters to electrochemical kinetics [22].

To further unlock the performance potential of the SFF,researchers have proposed various enhancements.Wei et al.[23] introduced a modified SFF by manipulating the sequence and configuration of channels,which effectively augmented the pressure differentials between adjacent channels,thereby improving electrolyte convection and mass transfer efficiency.Pan etal.[24,25] developed an improved SFF featuring gradient compression ratios along the flow direction to optimize electrode compression in under-rib regions.This design enhanced convection near rib ends and improved the uniformity of active species distribution in low-concentration zones.The optimized flow field achieved an impressive energy efficiency of $7 3 . 1 ~ \%$ at $4 0 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ， $5 \%$ higher than SFF.Lu etal.[26] and Chai etal.[27] explored rotating SFFs to modify flow paths and velocity distributions within the channels.This innovation enhances electrolyte penetration into electrodes and optimizes the distribution of active species on electrode surfaces,thereby reducing local concentration gradients and alleviating concentration polarization. Cheng etal.[28] introduced the concept of a flow guidance field,emphasizing the synergy of concentration, velocity,and pressure fields,and determined the optimal channel dimensions through orthogonal optimization.Zhang etal.[29] developed a tapered hierarchical interdigitated flow field that enhances the flow rate atthe channel ends and improves mass transfer.The numerical results showed that at $2 4 0 \mathrm { m A } / \mathrm { c m } ^ { \bar { 2 } }$ and a flow rate of $6 \mathrm { m L } / s$ ,the pump-based efficiency of the tapered hierarchical interdigitated flow field increased by $6 \% - 1 0 \%$ compared to the traditional interdigitated flow field.

Several researchers have explored the compression characteristics of electrodes.For instance,Saha et al.[3O] examined three scenarios of electrode compression: uncompressed,non-homogeneous,and homogeneous.Their numerical simulations assessed the charge-discharge performance of VRFBs with varying compression characteristics.The results highlighted the importance of non-uniform compression in modeling and analyzing the VRFB performance,offering a more realistic representation than no compression or homogeneous compression of the electrodes.Similarly, Xiong etal.[31] proposed a 3D VRFB model that accounts for uneven electrode deformation to evaluate cel performance under different electrode compression ratios.The numerical study revealed that both pressure drop and concentration overpotential are sensitive to the compression ratio,with a compression ratio of $4 5 \ \%$ yielding the minimum overpotential and optimum system performance. Besides,previous research has indicated that multi-channel parallel SFFs exhibit lower flow resistance,while rotating SFE,a variant of SFE, demonstrates enhanced electrochemical performance [11,32].Collectively,the shape,dimensions,and flow patterns of the channels significantly impact battery performance,and advancements in channel structures have the potential to greatly advance VRFB technology [33, 34].

Moreover,concurrent studies reveal that during the scale-up process from laboratory to commercial applications,the efficiency of VRFBs tends to degrade,regardless of the type of flow fields (serpentine [32], interdigitated [35],or novel designs [36]). This fundamental challenge mainly arises from intensified discrepancy in convective transport across the electrode regions in larger batteries,leading to increased non-uniformity in reactant concentration,increased concentration polarization,and ultimately,a decline in efficiency [37].Systematic analysis indicates the presence of heterogeneous transport mechanisms: horizontal convection is primarily driven by fluid,while vertical convection depends on pressure differentials between channels and ribs.

This bidirectional transport heterogeneity poses constraints on geometric scalability.

To address these limitations,we introduce two novel architectures: the loop-type flow field (LFF),which utilizes periodic orthogonal channels to harmonize the distribution of directional concentration,and the loop-type corrugated flow field (LCFF),which replaces straight channels with corrugated surfaces to induce turbulence that enhances under-rib mass transfer,as shown in Fig.1.For performance comparison among the flow fields,we conduct numerical simulations to evaluate charge-discharge cycles across the structures,assessng flow resistance, reactant uniformity,charge/discharge voltage,system efficiency,and discharge capacity.Additionally,we develop large-scale battery models to analyze performance differences between the SFF and LCFF structures during scale-up.

# 2.Experiment

# 2.1. Battery setup

The typical schematic and electrochemical reaction process of VRFB is depicted in Fig.S1.In this study,a laboratory single-cell VRFB was assembled to assess its charge-discharge performance.Considering both experimental and computational costs,an effective reaction area of 9 $\mathrm { c m } ^ { 2 }$ was applied for a single cell [35,36].The single-cell model primarily consists of two commercial graphite electrodes,one sheet of proton exchange membrane, two copper current collectors,and two stainless steel end plates.The entire single-cell model was tightly assembled using eight sets of bolts and nuts.And the setup of the single-cell assembly is shown in Fig.S2. Commercial graphite electrodes (GFD 4.6 EA, $3 0 \times 3 0$ $\mathrm { m m } ^ { 2 }$ ，SGL,Germany) were used,with each electrode being halved to obtain a $2 . 3 ~ \mathrm { m m }$ thick section for experimentation.After compression, the electrode thickness was approximately $1 \ \mathrm { m m }$ ,and the electrode underwent heat treatment at $5 5 0 ~ ^ { \circ } \mathrm { C }$ in air for $^ { 5 \mathrm { ~ h ~ } }$ before use.A commercial Nafion 212 proton exchange membrane $( 4 0 \times 4 0 \mathrm { m m } ^ { 2 }$ ,DuPont, USA) was applied,and it was pretreated by boiling in a $5 ~ \% \mathrm { H } _ { 2 } \mathrm { O } _ { 2 }$ Solution at $8 0 ~ ^ { \circ } \mathrm { C }$ for $^ \textrm { \scriptsize 1 h }$ ,followed by exposure to1M $\mathrm { H _ { 2 } S O _ { 4 } }$ solution at $8 0 ~ ^ { \circ } \mathrm { C }$ for $^ { 1 \mathrm { ~ h ~ } }$ ,and then stored in deionized water.The entire single-cell assembly was tightly fastened using eight bolts and nuts.For the electrolytes,a laboratory-prepared $1 . 5 \mathrm { ~ M ~ V } ^ { 3 . 5 + }$ with $3 \mathrm { ~ M ~ H _ { 2 } S O _ { 4 } }$ solutions were used [38],delivered to the battery module by a two-head peristaltic pump (BT1oOL,Leadfluid, China).

# 2.2．VRFB test

During operation, the peristaltic pump was activated to circulate the electrolyte,ensuring a constant flow rate of $4 0 \mathrm { m L / m i n }$ throughout the experiment.The positive and negative electrode storage tanks each contain $3 0 ~ \mathrm { m L }$ of $\mathsf { \bar { V } } ^ { 3 . 5 + }$ electrolyte. Nitrogen was continuously purged through the storage tank during the charge-discharge process to eliminate air and prevent oxygen from reacting with the electrolyte.A battery charger/discharger (CT-4008Tn-5V12A,Neware,China）was used to regulate current and voltage.The battery was tested sequentially at100, 200,300,400,and $5 0 0 ~ \mathrm { \ m A / c m ^ { 2 } }$ current densities,completing five charge-discharge cycles at each density: initially charging to $1 . 6 5 \mathrm { V }$ and subsequently discharging to $0 . 9 \mathrm { V } .$ Finally,the battery was disassembled and thoroughly cleaned before repeating the experiment.

# 3．Numerical simulations

# 3.1.Basic assumptions

In this work,to simulate the charge-discharge cycle of VRFBs,a three-dimensional transient multiphysics coupled model was developed to evaluate the transport and reaction processes within the battery.The schematic of the flow channel and the parameters for SFF,LFF,and LCFF are shown in Fig. S3 and detailed in Table S1.Within the threedimensional model, the reactions taking place in the porous electrode during the charging and discharging process are described as follows [26]:

![](images/3a50c6913b589a992adabf61fd249293767c7aa9662c071d62beeaf4723e0c39.jpg)
Fig.1.(a)Schematic structuresofatypical VRFBwiththe SFBipolarplateswiththe(b)SFF,(c)LFF,and(d)LCFFrespectively.

Positive reaction:

$$
\mathsf { V O } ^ { 2 + } - \mathsf e ^ { - } + \mathrm { H } _ { 2 } \mathsf { O } \underbrace { \overbrace { = } ^ { \mathrm { c h a r g e } } \nabla O _ { 2 } ^ { + } + 2 H ^ { + } } _ { \mathrm { d i s c h a r g e } }
$$

Negative reaction:

$$
\mathrm { { \bf V } ^ { 3 + } + e ^ { - } \sum _ { d i s c h a r g e } ^ { \ c h a r g e } \bf V ^ { 2 + } }
$$

To simplify the computation in this work,the following assumptions are established.

1） The electrolyte is treated as an incompressible fluid,and the flow is assumed to be laminar.
2) The electrode is considered homogeneous with isotropic physical properties.
3) Potential side reactions,such as hydrogen evolution,are excluded from consideration.
4) The cross-membrane transport of vanadium ions and water is disregarded.
5) Temperature changes resulting from reaction heat arenot considered.
6) The effects of gravity on the reactions are neglected.
7） The electrode is considered to be uniformly compressed.

# 3.2. Governing equations

The multiphysics coupled model was established by mass conservation,momentum conservation,charge conservation,and reaction kinetics [23,28].

# 1）Flow equation

The continuity equation can be expressed as [23]:

$$
\rho \nabla \cdot \boldsymbol { u } = 0
$$

The conservation of momentum for electrolytes in channels and porous electrodes can be expressed by the transient Navier-Stokes equation and the Brinkman equation [39], respectively:

$$
\begin{array} { l } { \displaystyle \rho \frac { \partial \boldsymbol { u } } { \partial t } + \rho \boldsymbol { u } \cdot \nabla \boldsymbol { u } = - \nabla p + \mu \nabla \cdot \big ( \nabla \boldsymbol { u } + \left( \nabla \boldsymbol { u } \right) ^ { T } \big ) } \\ { \displaystyle \rho \frac { } { \varepsilon } \frac { \partial \boldsymbol { u } } { \partial t } + \frac { \rho } { \varepsilon } \boldsymbol { u } \cdot \nabla \frac { \boldsymbol { u } } { \varepsilon } = - \nabla p + \nabla \cdot \frac { \mu } { \varepsilon } \big ( \nabla \boldsymbol { u } + \left( \nabla \boldsymbol { u } \right) ^ { T } \big ) - \frac { \mu } { k } \boldsymbol { u } } \end{array}
$$

where $u , \rho , p$ ,and $\mu$ represent fluid velocity,density,pressure,and dynamic viscosity,respectively. $\varepsilon$ and $k$ denote the porosity and permeability of the porous electrode.The superscript $T$ denotes the transpose matrix.The permeability of the porous medium is described by the Carman-Kozeny equation [40]:

$$
k = \frac { d ^ { 2 } \varepsilon ^ { 3 } } { 1 6 k _ { c k } { ( 1 - \varepsilon ) } ^ { 2 } }
$$

where $d$ is the fiber diameter of electrodes,and $k _ { c k }$ is the Carman-Kozen constant.During the assembly process,the electrodes are compressed. Taking into account the compression ratio $\theta$ [41],the compressed porosity $\varepsilon ,$ and the specific surface area $a$ ,can be described as:

$$
\theta { = } \frac { V _ { 0 } - V } { V _ { 0 } } , \varepsilon { = } \frac { \varepsilon _ { 0 } - \theta } { 1 - \theta } , a { = } \frac { a _ { 0 } } { 1 - \theta }
$$

where $V _ { 0 } , \varepsilon _ { 0 } ,$ and $a _ { 0 }$ represent the volume, porosity,and specific surface area of the electrode before compression, respectively.

The pump power during the flow process is [24]:

$$
W _ { \mathrm { p } } = \frac { 2 Q _ { 0 } \Delta P } { \eta _ { 0 } }
$$

where $\Delta P$ represents the pressure difference between the inlet and outlet, $Q _ { 0 }$ represents the total flow rate of electrolyte, and $\eta _ { 0 }$ represents the pump efficiency,which is assumed to be 0.9.

# 2) Mass transfer equation

The diffusion,migration,and convection of species in dilute solutions are described by the Nernst-Planck equation [23]:

$$
N _ { i } = \mathrm { ~ - ~ } D _ { i } ^ { \mathrm { e f f } } \nabla c _ { i } - \frac { z _ { i } c _ { i } D _ { i } ^ { \mathrm { e f f } } } { R T } \nabla \varphi _ { i } + u c _ { i }
$$

The conservation of matter for diferent species can be expressed as:

$$
\frac { \partial } { \partial t } \left( \varepsilon c _ { i } \right) + \nabla \cdot \left( - N _ { i } \right) = - S _ { i }
$$

where the subscriptidenotes the species; $N _ { i }$ and $s _ { i }$ representthe flux and the molar source term of species i; $c _ { i }$ and $\mathfrak { z } _ { i }$ indicate the species concentration and charge number,respectively. $R$ is the ideal gas constant, Trefers to temperature,and $F$ represents the Faraday constant. $\varphi _ { i }$ is the potential of the electrolyte phase,and the effective diffusion coefficient in the electrode, $D _ { i } ^ { \mathrm { e f f } }$ ,is corrected according to the Bruggeman equation [30]:

$$
D _ { i } ^ { \mathrm { e f f } } = \varepsilon ^ { 3 / 2 } D _ { i }
$$

The conservation of charge in the electrolyte phase and electrode phase is described as:

$$
\nabla \cdot i _ { 1 } = - \nabla { \cdot } i _ { s } = j
$$

where $i _ { s }$ and $\dot { \boldsymbol { \mathbf { \eta } } } _ { \dot { \boldsymbol { \mathbf { l } } } }$ represent the current densities in the electrode phase and electrolyte phase,respectively,which can be calculated using Ohm's law [41]:

$$
\begin{array} { l } { i _ { s } = - \sigma _ { s } ^ { \mathrm { e f f } } \nabla \varphi _ { s } } \\ {  _ { i _ { 1 } = F \sum _ { i } z _ { i } N _ { i } } } \end{array}
$$

where $\sigma _ { s } ^ { \mathrm { e f f } }$ representsteetiecoductivitsofteeectrec can be corrected according to the Bruggeman equation [30]:

$$
\sigma _ { s } ^ { \mathrm { e f f } } = ( 1 - \varepsilon ) ^ { 1 . 5 } \sigma _ { s }
$$

# 3) Electrode potential and reaction kinetic equation

The cell voltage of VRFB during charging and discharging is determined by the overpotential and the equilibrium potential of the electrodes,which can be expressed by the Nernst equation [23]:

$$
\begin{array} { l } { { \displaystyle E _ { \mathrm { p o s } } = E _ { 0 , \mathrm { p o s } } + \frac { R T } { F } \mathrm { l n } \left( \frac { c _ { \mathrm { V } 0 _ { 2 } ^ { + } } c _ { \mathrm { H } ^ { + } } ^ { 2 } } { c _ { \mathrm { V } 0 ^ { + + } } } \right) } } \\ { { \displaystyle E _ { \mathrm { n e g } } = E _ { 0 , \mathrm { n e g } } + \frac { R T } { F } \mathrm { l n } \left( \frac { c _ { \mathrm { V } ^ { 3 + } } } { c _ { \mathrm { V } ^ { 2 + } } } \right) } } \end{array}
$$

where $E _ { 0 , \mathrm { p o s } }$ and $E _ { 0 , \mathrm { n e g } }$ represent the standard equilibrium potentials of the positive and negative electrode, respectively.

The overpotential $\eta$ of the positive and negative electrodes can be expressed as [23]:

$$
\begin{array} { r l } & { \eta _ { \mathrm { p o s } } = \varphi _ { \mathrm { s , p o s } } - \varphi _ { \mathrm { l , p o s } } - E _ { \mathrm { p o s } } } \\ & { } \\ & { \eta _ { \mathrm { n e g } } = \varphi _ { \mathrm { s , n e g } } - \varphi _ { \mathrm { l , n e g } } - E _ { \mathrm { n e g } } } \end{array}
$$

Therefore,the cell voltage during the charging and discharging process can be expressed as [23]:

$$
\begin{array} { r l } & { E _ { \mathrm { c h } } = \left( E _ { \mathrm { p o s } } + \eta _ { \mathrm { p o s } } \right) - \left( E _ { \mathrm { n e g } } + \eta _ { \mathrm { n e g } } \right) + \Delta E _ { \mathrm { m e m } } } \\ & { } \\ & { E _ { \mathrm { d i s c h } } = \left( E _ { \mathrm { p o s } } - \eta _ { \mathrm { p o s } } \right) - \left( E _ { \mathrm { n e g } } - \eta _ { \mathrm { n e g } } \right) - \Delta E _ { \mathrm { m e m } } } \end{array}
$$

where $\Delta E _ { \mathrm { m e m } }$ represents the potential difference between both sides of the ion exchange membrane.

The rates of electrochemical reactions at the positive and negative electrodes are described by the current densities $j _ { \mathrm { p o s } } \operatorname { a n d } j _ { \mathrm { n e g } }$ ,which can be calculated by the Butler-Volmer equation [42].

$$
\begin{array} { r l } & { { \bf j } _ { \mathrm { p o s } } = F k _ { 0 , \mathrm { p o s } } c _ { \mathrm { V } 0 ^ { 2 + } } ^ { \alpha _ { \mathrm { p o s , c } } } c _ { \mathrm { V } 0 _ { 2 } ^ { + } } ^ { \alpha _ { \mathrm { p o s , a } } } \left[ \frac { c _ { \mathrm { V } 0 _ { 2 } ^ { + } } ^ { s } } { c _ { \mathrm { V } 0 _ { 2 } ^ { + } } } \exp \left( - \frac { \alpha _ { \mathrm { p o s , c } } F \eta _ { \mathrm { p o s } } } { R T } \right) - \frac { c _ { \mathrm { V } 0 ^ { 2 + } } ^ { s } } { c _ { \mathrm { V } 0 ^ { 2 + } } } \exp \left( \frac { \alpha _ { \mathrm { p o s , c } } } { c _ { \mathrm { V } 0 ^ { + } } } \right) \right] } \\ & { \quad - \frac { \alpha _ { \mathrm { p o s } , a } F \eta _ { \mathrm { p o s } } } { R T } \bigg ) \Bigg ] } \end{array}
$$

$$
\begin{array} { l } { { \displaystyle j _ { \mathrm { n e g } } = F k _ { \mathrm { 0 , n e g } } c _ { \mathrm { V } ^ { 2 + } } ^ { \alpha _ { \mathrm { n e g , c } } } c _ { \mathrm { V } ^ { 3 + } } ^ { \alpha _ { \mathrm { n e g , a } } } \left[ \frac { c _ { \mathrm { V } ^ { 3 + } } ^ { s } } { c _ { \mathrm { V } ^ { 3 + } } } \exp \bigg ( - \frac { \alpha _ { \mathrm { n e g , c } } F \eta _ { \mathrm { n e g } } } { R T } \bigg ) - \frac { c _ { \mathrm { V } ^ { 2 + } } ^ { s } } { c _ { \mathrm { V } ^ { 2 + } } } \exp \bigg ( - \frac { \alpha _ { \mathrm { n e g , c } } } { R T } \bigg ) \right] } }  \\ { { \displaystyle \quad - \frac { \alpha _ { \mathrm { n e g , a } } F \eta _ { \mathrm { n e g } } } { R T } \bigg ) \bigg ] } } \end{array}
$$

where $\alpha _ { \mathrm { a } }$ and $\alpha _ { \mathrm { c } }$ represent the anode and cathode reaction transport coefficients,respectively, $k _ { 0 }$ denotes the reaction rate constant,and superscript $s$ indicates the concentration of species at the electrode surface.Fick's First Law establishes the relationship between the concentration of active species at the electrode surface and the bulk concentration [41]:

$$
k _ { m } \left( c _ { i } - c _ { i } ^ { s } \right) = - \frac { j } { F }
$$

where $k _ { m }$ represents the mass transfer coeficient,which can be approximated by the empirical formula [37]:

$$
k _ { m } = 1 . 6 \times 1 0 ^ { - 4 } \lvert u ^ { 0 . 4 } \rvert
$$

The voltage efficiency $V E$ during charging and discharging is expressed as [28]:

$$
V E = \frac { V _ { \mathrm { d i s c h , a v g } } } { V _ { \mathrm { c h , a v g } } }
$$

where $V _ { \mathrm { d i s c h , a v g , } }$ and $V _ { \mathrm { c h , a v g } }$ represent the average voltages during discharging and charging,respectively.

# 3.3.Boundary conditions

Boundary conditions for the flow field and concentration field are set to initialize the numerical analysis.

1） Flow field boundary conditions

The inlet velocity of the electrolyte is defined as follows:

$$
- \int { u _ { \mathrm { i n } } { \cdot } n d S _ { \mathrm { i n } } } = Q _ { \mathrm { i n } }
$$

where $n$ represents the outward unit normal vector, $S _ { \mathrm { i n } }$ is the inlet area $( 2 \ : \mathrm { m m } ^ { 2 } )$ ,and $Q _ { \mathrm { i n } }$ is the volumetric flow rate $( 4 0 ~ \mathrm { m L / m i n } )$ . The calculated inlet velocity $u _ { \mathrm { i n } }$ is found to be $0 . 3 3 \mathrm { ~ m } / s$ ，while the Reynolds number $( R e )$ at the inlet is determined to be 120.

At the outlet, the pressure is defined to be zero,as expressed by:

$$
P _ { \mathrm { o u t } } = 0
$$

For the other walls,a no-slip boundary condition is applied, which is given by:

$$
u = 0
$$

# 2） Concentration field boundary conditions

During the charging and discharging,the movement of the electrolyte solution through the pump results ina time-varying inlet electrolyte concentration.The inlet concentrations are derived from the following mass balance equation,which assumes instantaneous mixing and negligible reactions within the tanks:

$$
\frac { d c _ { i , \mathrm { i n } } } { d t } = \frac { Q _ { \mathrm { i n } } \left( c _ { i , \mathrm { o u t } } - c _ { i , \mathrm { i n } } \right) } { V - V _ { \mathrm { e } } } , c _ { i , \mathrm { i n } } ( 0 ) = c _ { i } ^ { 0 }
$$

where $c _ { i , \mathrm { i n } }$ denotes the average concentration at the inlet, $c _ { \mathrm { i , o u t } }$ is the average concentration at the outlet, $V$ is the total electrolyte volume (30 mL),and $V _ { \mathrm { e } }$ is the electrolyte volume contained within the porous electrode $\left( 0 . 9 ~ \mathrm { m L } \right)$ .The volume in the connecting pipes is considered negligible.

At the outlet,a non-diffusive flux boundary condition is applied, described by:

$$
\boldsymbol { n } \cdot \boldsymbol { D } _ { i } \Delta c _ { i } = 0
$$

A fixed current density is set at the outer boundary of the positive current collector,while grounding is applied at the outer boundary of the negative current collector:

$$
- n { \cdot } i _ { \mathrm { c , p o s } } = i _ { \mathrm { a v g } } , \varphi _ { \mathrm { c , n e g } } = 0
$$

For the other walls,a no-flux boundary condition is maintained:

$$
n \cdot N _ { i } = 0
$$

# 3.4.Numerical methods and model validation

This study employed COMSOL Multiphysics 6.2 to perform the simulation,with computational parameters listed in Table S2.The flow dynamics during the charging and discharging of VRFB were analyzed using the free and porous media flow module.At the same time,the tertiary current distribution solved the electrochemical reactions and mass transport.Utilizing this model,a VRFB with SFFs was simulated, and the geometry was discretized using hexahedral meshes.The cell voltage and pressure drop of the VRFB across different mesh sizes are presented in Fig.2a.When the grid count exceeded 2oo,ooo,the relative computational difference was less than $0 . 1 ~ \%$ .To strike a balance between computational accuracy and cost-effectiveness,subsequent calculations employed the 2oo,ooo-grid system.And the relative tolerance was set to $1 \times 1 0 ^ { - 4 }$ [24].Fig. S4 shows the voltage and current results from the experiment.Additionally,model validation was performed across various current densities.Fig.2b presents a comparison of the terminal voltages during both the charging and discharging processes at a current density of $3 0 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ .Moreover, the validation results for other current densities are depicted in Fig.S5.The relative error observed between the simulated and experimental results is within 1.9 $\%$ ,thereby affirming the model’s high level of accuracy.

# 3.5.Data analysis

To quantitatively evaluate the differences in battery performance among SFF,LFF,and LCFF,the flow characteristics,reaction performance,and system performance were assessed.

# 1）Flow characteristics

The flow characteristics of the channel are evaluated based on the average velocity of the electrolyte within the electrode and the electrolyte inflow volume ratio $\gamma$ [43]. Here, $\gamma$ is defined as:

$$
\gamma = \frac { Q _ { \mathrm { e } } } { Q _ { \mathrm { i n } } }
$$

where $Q _ { \mathrm { e } }$ represents the flow rate of electrolyte entering the electrode, and $Q _ { \mathrm { i n } }$ denotes the total flow rate of electrolyte.

# 2） Reaction performance

The performance of the VRFB reaction is assessed based on the average concentration of reactants in the electrode and the uniformity factor $U$ [44]. Here, $U$ is defined as:

$$
U = 1 - { \frac { 1 } { c _ { \mathrm { a v g } } } } { \sqrt { \frac { 1 } { V _ { \mathrm { e } } } \iiint ( c - c _ { \mathrm { a v g } } ) ^ { 2 } d V _ { \mathrm { e } } } }
$$

![](images/a8d16763a3a2abf05e5598d98e717d1a9e11bcfb9ea7d719bd9e30dc680fddb0.jpg)
Fig.2.(a) Grid-independence tests.(b) Model validation.

where $c _ { \mathrm { a v g } }$ represents the average concentration of reactants in the electrode,and $V _ { \mathrm { e } }$ refers to the electrolyte volume.

# 3） System performance

The system performance of VRFB is evaluated based on system efficiency $( S E )$ and electrolyte utilization (EU) [45].Here, $S E$ is defined as:

$$
S E { = } \frac { I E _ { \mathrm { d i s c h , a v g } } - W _ { \mathrm { p } } } { I E _ { \mathrm { c h , a v g } } - W _ { \mathrm { p } } }
$$

# 4．Results and discussion

# 4.1.Effects of the flow fields

The transport efficiency of active species within the electrodes plays acritical role in determining battery performance.To reveal the distinct characteristics among three different flow field configurations,this section presents a comparative analysis of the flow velocity vectors and reactant concentration distributions across the midplanes of the electrode ata flowrate of $4 0 ~ \mathrm { { m L / m i n } }$ .Fig.3a shows that conventional SFF exhibits significantly higher electrolyte velocity in under-rib regions than sub-channel areas,with maximum velocity reaching $1 . 5 \ \mathrm { m m } / s$ This is primarily due to enhanced convective transport resulting from the pressure drops between the ribs.Meanwhile,the velocity gradient diminishes along rib pathways owing to cumulative pressure drops. Therefore,the distribution of reactant concentration displays a similar non-uniform pattern,as depicted in Fig.3d.

The LFF augments under-rib convection by extending the inlet channels,achieving peak velocities of $2 . 3 \mathrm { m m } / \mathrm { s }$ and enhancing reactant uniformity compared to SFF,as illustrated in Fig.3b and e.Despite the LFF increasing the overall concentration of reactants in the electrode,a pronounced non-uniform distribution continues in the under-rib regions and sub-channel zones.In contrast, the LCFF induces surface turbulence that boosts the maximum flow velocity to $3 . 4 \ \mathrm { m m } / s$ while improving inter-zonal mass transfer efficiency,significantly enhancing the uniformity of reactant concentration, as shown in Fig. 3c and f. In summary, these structural innovations demonstrate a progressive enhancement in performance:the loop-type architecture increases electrolyte velocity in under-rib regions.In contrast,the corrugated architecture intensifies mixing between under-rib regions and sub-channel zones,improving reactant uniformity.

To assess the impact of three different structures on the flow process, we evaluated flow characteristics using the electrolyte penetration ratio $( \gamma )$ and average velocity $\left( u _ { \mathrm { a v e } } \right)$ ，as illustrated in Fig.4a. The ratio $\gamma$ represents the proportion of active species contributing to electrode reactions; thus,a higher $\gamma$ indicates a greater involvement of these active species,which is essential for improving the performance of the VRFB. The SFF exhibited a minimal $\gamma$ of $9 . 4 ~ \%$ ,indicating substantial underutilization of the electrolyte.In contrast, the LFF and LCFF achieved $\gamma$ values of $1 3 . 5 ~ \%$ and $2 1 . 7 ~ \%$ respectively. This suggests that the looptype and corrugated architecture enhance electrolyte transport to the electrode by optimizing the flow field topology and surface morphology. These improvements fascinate more reactants to the electrodes, ensuring the availability of sufficient species for the reactions.At the same time, the $u _ { \mathrm { a v e } }$ increased from $0 . 5 1 \mathrm { m m } / s$ in the SFF to $0 . 7 4 \mathrm { m m } / s$ in the LFF and $0 . 9 8 ~ \mathrm { m m } / s$ in the LCFF,demonstrating that the optimized flow fields enhance convective effects within the electrode,accelerate the transport rates of active species,and maximize mass transfer processes at the kinetic level.In summary,the combination of loop-type and corrugated architectures improves the penetration ratio and average velocity，thereby augmenting reactant transport kinetics through intensified convective effects and providing strong fluid dynamic support for optimizing VRFB performance.

![](images/9cb4827d1524fde5900d8997817d3d99f23f97b41923bfaab89446fccd7973e0.jpg)
Fig.3.Velocity distributions in the electrodes for (a) SFF,(b) LFF,and (c) LCFF. $\mathsf { V } ^ { 3 + }$ concentration distributions during charging at $3 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ and ${ \tt S O C } = 0 . 5$ f01 (d) SFF,(e) LFF,and (f) LCFF.

![](images/886cb5b55d494edf80762b626a11da8ae3b2ca84726e3c96b94fefce91cd08b7.jpg)
Fig.4.The battery performances of the SFF,LFF,and LCFF at $3 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ：(a) the penetration ratio and average velocity; (b) the concentration of reactants and the uniformity coefficient.

To clarify the influence of optimized structures on electrode reaction processes,we further quantitatively evaluated reaction performance by examining the average concentration of reactants and uniformity coefficient $( U )$ within the electrode,as shown in Fig. $^ { 4 \mathrm { b } }$ .ALower $U$ value is associated with increased risks of local overcharging and concentration polarization due to reactant depletion.These findings indicate that the reactant uniformity of the SFF is only $5 4 . 8 \%$ ,highlighting variations in concentration distribution within the electrode.In contrast, the LFF and

![](images/cea12ebda9908d11d7284589e591b9e8abbb45cb83066ce2f0f4157f40892ee3.jpg)
Fig.5.Thebaerypformanceofte,ndF.(a)arge-dshargeprofiles,(b)sstemefciecydcapacitytatiat $3 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ; (c) system fficiencyand(d)capacityuilzationatdferentcurrntdnsities; (e)overpotenialandlibrumpotentialwihdifentCsat $1 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ；(f) overpotential and equilibrium potential at $3 0 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$

LCFF achieve uniformity levels of $6 7 . 2 ~ \%$ and $7 5 . 5 ~ \%$ ，respectively. These results demonstrate that the optimized flow fields effectively reduce concentration gradients in the electrode,thereby reducing the risks of overcharging and side reactions,diminishing concentration overpotentials,and enhancing the performance of the VRFB.Moreover, the average reactant concentrations in LFF and LCFF are higher than those in SFF.Elevated reactant concentrations can reduce electrochemical polarization during the reaction process.Additionally,according to the Nernst equation,the concentration of reactants in the electrode is a key factor determining the reaction equilibrium potential; higher reactant concentrations can lead to an increase in discharge voltage and a reduction in charge voltage,thereby optimizing the charge-discharge platform and expanding the effective operating voltage range of the VRFB.In conclusion，the optimized structure significantly improves cell reaction performance through two primary mechanisms: suppressing concentration polarization by enhancing the uniformity of reactant distribution and optimizing the charge-discharge platform by increasing the average reactant concentration.

# 4.2. Charge-discharge performance analysis

To systematically evaluate the performance of SFF,LFF,and LCFF, charge-discharge cycling tests were performed at a current density of $3 0 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ ，The variation in cell voltage during charging and discharging is illustrated in Fig.5a. The LCFF configuration exhibits the smallest charge-discharge electrode potential difference and achieves the highest voltage efficiency.In contrast, the SFF exhibits the largest potential difference and the lowest efficiency.Moreover, the LCFF results in the longest discharge duration,indicating enhanced mass transport that ensures a sustained supply of reactants,facilitating more complete reactions and enhancing electrolyte utilization.As shown in Fig.5b,the system eficiency (SE) and electrolyte utilization (EU) were assessed for each structure.Despite the loop-corrugated design of LCFF leading to increased flow resistance and requiring higher pump power, it also enhances convection, thereby improving the transport of active species.After accounting for pump losses,the LCFF achieves an impressive system efficiency of $8 0 . 4 \%$ ,surpassing the LFF by $1 . 4 \%$ and the SFF by $3 . 2 ~ \%$ .Similarly,at $3 0 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ ，the LCFF reaches the highest capacity utilization at $7 0 . 9 \%$ ,compared to $6 2 . 8 ~ \%$ for the LFF and $5 3 . 8 ~ \%$ for the SFF.These findings illustrate that the LFF and LCFF significantly enhance VRFB performance compared to the SFF.

It is worth noting that the present study adopted a model of uniform electrode compression to facilitate the computational process.Previous research [3O,31] has demonstrated that electrodes subjected to non-uniform compression exhibit greater pressure drops and overpotentials when compared to their uniform counterparts.Therefore,it is imperative that future investigations focus on the development of models incorporating non-uniformly compressed electrodes to more accurately reflect the characteristics of VRFBs.

To evaluate the adaptability of each structure under a broader range of operating conditions for VRFBs,we compared the performance of three different structures across various current densities,as shown in Fig.5c and d.As current density rises, both SEand EU decrease across all configurations,with the SFF showing the most decline,while the LCFF exhibits the least reduction.Elevated current densities accelerate electrochemical reaction rates, but when transport of species cannot keep up,polarization losses increase,leading to decreased performance.The loop structure and corrugated surface enhance convection, thereby improving the transport capacity of active species within the electrodes. Therefore,the performance advantages of the LCFF become more prominent at higher current densities.At a current density of $5 0 0 ~ \mathrm { m A } / $ $\mathrm { c m } ^ { 2 }$ ,the electrolyte utilization rates are $1 6 . 8 \%$ for SFF, $3 3 . 1 \ \%$ for LFF, and $4 7 . 0 ~ \%$ for LCFF.Additionally,the system efficiency for LCFF reaches $7 2 . 3 ~ \%$ ,exceeding that of LFF by $2 . 7 ~ \%$ and SFF by $7 . 3 ~ \%$ These improvements supporta more efficient operation of VRFBs at elevated current densities and enhance the ultimate current density achievable by

the system.

According to Eqs.(2O） and (21)，determining charge/discharge voltages in VRFBs is fundamentally governed by the equilibrium potential and the accompanying overpotential.A reduced equilibrium potential and diminished overpotential during the charging process correlate with lower charging voltage,improving efficiency. Conversely, an elevated equilibrium potential with a lower overpotential during discharging contributes to superior discharge voltage and efficiency. Yet,the previous research has predominantly focused on overpotential disparities across various flow fields [46,47],inadvertently neglecting the significant influence of equilibrium potential on cell voltage.

To advance the understanding of the performance enhancement mechanisms of LFE and LCFE,we compared the equilibrium potentials and overpotentials at $1 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ and $\mathsf { \bar { 3 0 0 } m A } / \mathsf { c m \bar { ^ { 2 } } }$ ,as shown in Fig.5e and f.At a current density of $1 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ,the equilibrium potential and overpotential differences among the three flow fields are negligible due to relatively slow reaction kinetics and the similarity in average concentrations.However，these differences became pronounced as the current density increased to $3 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ For this analysis,the SOC was fixed at O.5 to ensure a stable reaction environment.The findings reveal that the LCFF exhibits a decrease in equilibrium potential by $2 4 ~ \mathrm { m V }$ compared to the SFF.In contrast,the reduction in overpotential is limited to $6 \mathrm { m V }$ ,indicating that the primary factor in the voltage optimization during the charging and discharging processes in the LCFF is the reduction in equilibrium potential.As Eqs.(16) and (17) indicates, the equilibrium potential primarily depends on the ratio of reactant concentration to product concentration.Specifically,higher reactant and lower product concentrations yield a lower equilibrium potential. The LCFF's enhanced mass transport capacity ensures the supply of sufficient reactants throughout the reaction process while accelerating the desorption and migration of products from the electrode surface, thereby achieving the lowest equilibrium potential observed in the study.

In summary, the loop-type structure and corrugated surface significantly improve the transport capacity of active species by enhancing convective effects within the electrode.This enhancement leads to an increase in reactant concentrations while simultaneously decreasing product concentrations within the electrode. Such modifications optimizethe charge-discharge voltage characteristics by effectively lowering the reaction equilibrium potential, thereby contributing to an overall enhancement in the performance of VRFBs.

# 4.3. LCFF structural scale-up analysis

Compared to conventional SFFs,the LCFF exhibits enhanced performance due to the synergistic design of periodic horizontal and vertical flow channels,which effectively minimizes disparity in reactant concentration between the horizontal and vertical dimensions.To directly compare the differences in their concentration spatial distributions,this study systematically analyzes the distribution of reactant concentration within vertical and horizontal cross-sections located 3 mm from the edges of the electrode.

For the SFF structure,the vertical concentration profile reveals significant periodic fluctuations along the flow direction due to the alternating zones of the sub-channels and the convection-enhanced regions under the rib,as illustrated in Fig.6a.This phenomenon arises from the dominance of pressure-driven convection in under-rib areas,which produces a higher mass transport capacity than that in the sub-channel zones where diffusion-driven mass transfer is dominant.This spatial difference in mass transfer ability directly causes periodic concentration fluctuations across the vertical cross-section.

Conversely,while convective effects predominantly govern the mass transport in the horizontal cross-section,leading to a gradual decrease in concentration along the flow paths,as shown in Fig.6b.In the horizontal direction,convective effects permeate the entire flow channel crosssection，with no masstransfer“weak zones” caused byrib obstructions. Continuous convective transport guarantees uniform consumption of reactants along the flow direction, leading to a monotonically decreasing concentration profile.

![](images/808bc1ad7842a3a781ad26912a920dddead98b9e4004b0a3f62272cc2c3f9768.jpg)
Fig.6.Concentration distributions of $\mathsf { V } ^ { 3 + }$ at $3 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ and ${ \tt S O C } = 0 . 5$ during discharge in (a) vertical and (b) horizontal cross-sections of the SFF,and (c) vertica and(d)horzotalo-sectiosofteLF.Concetratiodistrbutiosoftheverticaladorzotalut-lesof()nd(LFF.

The concentration distributions within the LCFF in both vertical and horizontal sections exhibit distinct periodic fluctuation characteristics. This is attributed to the periodical arrangement of the ribs in both orientations,as demonstrated in Fig.6c and d.This characteristic arises from the LCFF structure,which uses periodic rib arrangements in both horizontal and vertical directions.The spatial periodicity of the ribs directly influences the periodicity of flow field disturbances,leading to synchronized oscillations in mass transfer efficiency.This ultimately results in periodic fluctuations in concentration distribution.

A comparative analysis of the concentration distributions of the vertical and horizontal cut-lines reveals that the LCFF structure significantly reduces concentration differences in both orientations compared to the SFF.This reduction is attributable to its periodic rib distribution, as shown in Fig.6e and f.Although there are discrepancies in concentration values between the two orientations,the fluctuation patterns remain highly consistent: peaks and valleys change synchronously along the flow direction.As the VRFB scale-up,the concentration disparity between horizontal and vertical directions in the SFF structures becomes more pronounced [32]. In contrast, the periodic concentration fluctuations inherent in the LCFF structures effectively mitigate the disparity amplification in both directions,highlighting their superior suitability for large-scale battery applications.

Based on the analysis above,this study undertakes scale-up research on SFF and LCFF structures.As shown in Fig.7a,adhering to geometric similarity principles while maintaining constant specific flow rates,a scaled-up electrode model of $1 5 0 \ \mathrm { m m } \times 1 5 0 \ \mathrm { m m }$ has been constructed witha flowrate of $1 0 0 0 ~ \mathrm { { m L / m i n } }$ .Fig.7b and c illustrate the distributions of reactant concentration in the scale-up electrode: the concentration in the larger cell closely aligns with that of the original cell (refer to Fig.3d and f).However,due to the cumulative effects of convective difference,the reactant concentration distribution in the scale-up cell exhibits greater non-uniformity.As shown in Fig.7d,performance metrics indicate a decrease in both $\gamma$ and $U$ upon scaling; nonetheless, the LCFF maintains significantly higher $U$ values compared to SFF,thus confirming its preserved mass transport enhancement. Significantly, the $_ { S E }$ enhancement of the LCFF shifts from $3 . 2 ~ \%$ to $4 . 3 ~ \%$ ,affirming its scalability.While there is an $8 . 1 ~ \%$ reduction in $S E$ for the scaled-up LCFF,its structural adaptability remains apparent,as illustrated in Fig. 7e.

To further enhance the performance of the LCFF structure in amplified cells,we investigated the effects of rotating SFFs and rotating LCFFs,as illustrated in Fig.S6a.The concentration distributions within the rotating flow field are shown in Fig.S6b and S6c.A comparative analysis reveals that the rotational motion of the channels leads to an increased pressure drop between adjacent channels, thereby enhancing convective mass transfer under the rib structure and elevating the concentration of reactants within the electrode.This improvement is indicative of superior electrochemical performance.Fig.S6d and S6e quantitatively assess the performance enhancement associated with the rotating structures.The performance metrics indicate an increase in both $\gamma$ and $U$ Notably,the rotating LCFF achieves an impressive $\gamma$ value of up to $2 0 \%$ .Correspondingly,the rotating structure enhances both the average concentration of reactants and their uniformity. These findings suggest that there is still space for improvement in the performance of LCFF in large cells.Therefore,future optimization efforts should focus on addressing concentration disparities caused by scaling.Potential strategies may include adjustments in rib spacing,channel width gradients,or the integration of multiscale transport mechanisms to further enhance performance at larger scales [48].

# 5．Conclusion

This study introduces two innovative flow field architectures-LFF and LCFF- which are derived from traditional serpentine configurations to improve the performance of VRFBs.These advanced designs enhance convective mass transfer by optimizing the distribution patterns of the rib and incorporating corrugations on the channel surface, thereby achieving superior uniformity in the distribution of active species.Computational analyses reveal that these enhanced configurations significantly improve the electrolyte penetration ratio into the electrode, therebyensuringadequateparticipation of activespeciesin electrochemical reactions.Moreover,these structure modifications contribute to enhanced uniformity of reactant concentration and optimize equilibrium potential behavior during cell cycling.Notably,at 300 $\mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ ,the LCFF exhibits the highest performance metrics,exhibiting values for $\gamma$ and $U _ { i }$ at $2 1 . 7 \%$ and $7 5 . 5 \%$ ,respectively. Consequently, the LCFF design achieves an impressive system efficiency of $8 0 . 4 ~ \%$ ,representing a $3 . 2 ~ \%$ enhancement compared to conventional serpentine designs.Implementing a corrugated architecture further enhances bidirectional mass transport, thus maintaining superior performance during scaling;notably,it exhibits $4 . 3 ~ \%$ higher system efficiency than the scaled serpentine counterparts.Therefore,the modified flow fields proposed in this study offer a promising strategy for enhancing the power density of VRFBs, reducing overall battery costs,and providing an innovative approach to scaling up the cell configurations.

![](images/dae313f8127bec257bcfbf2ee5d5f6604f6752c7bfd45cf0b1e5c14a9527f0bf.jpg)
Fig.7.(a) Schematic diagram of the scaling of the SFF. $\mathsf { V } ^ { 3 + }$ concentration distribution during discharge at $3 0 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ and ${ \tt S O C } = 0 . 5$ for (b) SFF-L and (c) LCFF-L. (d)Penetrationtidunfoityoefientforrouscell.(eSsteficecyndeletrolyteutilzaonforroul,here $" . . s ^ { \prime \prime }$ denotes the original cell and $" \mathrm { \mathbf { L } } ^ { \prime \prime }$ denotes the scaled-up cell.

Nomenclature

<table><tr><td>a</td><td>specific surface area (1/m)</td></tr><tr><td>ao</td><td>initial specific surface area (1/m)</td></tr><tr><td>C</td><td>concentration (mol/m)</td></tr><tr><td>d</td><td>fiber diameter of electrode (m)</td></tr><tr><td>D</td><td>diffusion coefficient (m²/s)</td></tr><tr><td>E</td><td>cell voltage (V)</td></tr><tr><td>Eo</td><td>the standard equilibrium potential (V)</td></tr><tr><td>F</td><td>Faraday constant (C/mol)</td></tr><tr><td>i</td><td>current density (A/m)</td></tr><tr><td>j</td><td>transfer current density (A/m)</td></tr><tr><td>k</td><td>permeability of the electrode (m²)</td></tr><tr><td>ko</td><td>reaction rate constant (m/s)</td></tr><tr><td>Kck</td><td>Carman-Kozen constant</td></tr><tr><td>km</td><td>mass transfer coefficient</td></tr><tr><td></td><td>(continued on next page)</td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td>N</td><td>flux source term (mol/m²-s)</td></tr><tr><td>p</td><td>pressure (Pa)</td></tr><tr><td>Q</td><td>flow rate (mL/min)</td></tr><tr><td>R</td><td>the ideal gas constant (J/mol·K)</td></tr><tr><td>S</td><td>molar source term</td></tr><tr><td>T</td><td>temperature (K)</td></tr><tr><td>u</td><td>velocity (m/s)</td></tr><tr><td>U</td><td>uniformity factor</td></tr><tr><td>V</td><td>volume of the electrode (m)</td></tr><tr><td>Vo</td><td>initial volume of the electrode (m)</td></tr><tr><td>Ve</td><td>the volume of electrolyte (m)</td></tr><tr><td>z</td><td>the charge number</td></tr><tr><td>Greek symbol</td><td></td></tr><tr><td>α</td><td>reaction transport coeficient (m/s)</td></tr><tr><td>Y</td><td>electrolyte inflow volume ratio</td></tr><tr><td>ε</td><td>porosity of the electrode,dimensionles</td></tr><tr><td>£0</td><td>initial porosity of the electrode</td></tr><tr><td>n</td><td>overpotential (V)</td></tr><tr><td>no</td><td>pump efficiency</td></tr><tr><td>0</td><td>compression ratio</td></tr><tr><td>μ</td><td>dynamic viscosity (Pa·s)</td></tr><tr><td>p</td><td>density (kg/m³)</td></tr><tr><td>0</td><td>conductivity (S/m)</td></tr><tr><td>p</td><td>potential (V)</td></tr><tr><td>Subscript</td><td></td></tr><tr><td>avg</td><td>average</td></tr><tr><td>b</td><td>bipolar plate</td></tr><tr><td>ch</td><td>charge</td></tr><tr><td>disch</td><td>discharge</td></tr><tr><td>i</td><td>species i: v2+,v3+,vO²+,VO,H+</td></tr><tr><td>in</td><td>inlet</td></tr><tr><td>1</td><td>electrolyte phase</td></tr><tr><td>mem</td><td>membrane</td></tr><tr><td>neg</td><td>negative</td></tr><tr><td>P</td><td>pump</td></tr><tr><td>pos</td><td>positive</td></tr><tr><td>S</td><td>electrode phase</td></tr><tr><td>Superscript</td><td></td></tr><tr><td>eff</td><td>effective</td></tr><tr><td>S</td><td>surface</td></tr><tr><td>T</td><td>transposed matrix</td></tr><tr><td>Abbreviated noun</td><td></td></tr><tr><td>LCFF</td><td>loop-type corrugated flow field</td></tr><tr><td>LFF</td><td>loop-type flow field</td></tr><tr><td>SE</td><td>system efficiency</td></tr><tr><td>SFF</td><td>serpentine flow field</td></tr><tr><td>UE</td><td>electrolyte utilization</td></tr><tr><td>VE</td><td>voltage efficiency</td></tr><tr><td>VRFB</td><td>vanadium redox flow battery</td></tr></table>

# CRediT authorship contribution statement

Zexin Zhou: Writing - original draft， Software，Methodology, Investigation.Xu Yang:Writing-review & editing,Validation,Data curation. Nianben Zheng:Writing - review & editing, Supervision, Funding acquisition, Conceptualization. Zhiqiang Sun: Writing - review&editing， Supervision，Project administration，Funding acquisition.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Acknowledgments

The work was supported by the Changsha Outstanding Innovative Youth Training Program (No.kq25o6013),Natural Science Foundation of Sichuan Province (No．2024NSFSC1361)，the High-Performance Computing Center of Central South University,and the Graduate Innovation Project of Central South University (No.1053320241629).

# Appendix A. Supplementary data

Supplementary data to this article can be found online at https://doi. org/10.1016/j.jp0ws0ur.2025.239182.

# Data availability

Data will be made available on request.

# References

[1] Y.-L. He, S.Du, S. Shen, Advances in porous volumetric solar receivers and enhancement of volumetric absorption, Energy Rev. 2 (2023) 100035.
[2] E. Sánchez-Diez, E. Ventosa, M. Guarnieri, A. Trovo, C. Flox,R. Marcilla, F. Soavi, P. Mazur, E. Aranzabe, R. Ferret, Redox flow batteries: status and perspective towards sustainable stationary energy storage, J. Power Sources 481 (2021) 228804.
[3] Z. Wang, J. Ren,J. Sun, Z. Guo,L. Wei, X. Fan,T. Zhao, Characterizations and selections of electrodes with optimal performance for large-scale vanadium redox flow batteries through lab-scale experiments, J. Power Sources 549 (2022) 232094.
[4] B.-L.Bai, S. Du, M.-J.Li, Photovoltaic efficiency improved by self-adaptive water uptake hydrogel evaporative cooling, Appl. Energy 383 (2025) 125367.
[5] J. Kim, H. Park, Recent advances in porous electrodes for vanadium redox flow batteries in grid-scale energy storage systems: a masstransfer perspective, J. Power Sources 545 (2022) 231904.
[6] M.U.Naseer,B.Pan,S.A. Wang,Y.Lyu,B.Liu,L.J.Li,J. Qi, H. Du, A comprehensive review of advancements in vanadium electrolyte preparation for Vanadium Redox Flow Bateries, J. Environ. Chem. Eng.13 (2025) 118402.
[7]J.-W. Ni,M.-J.Li,T.Ma, The study ofenergy filtering managementproce for microgrid based on the dynamic response model of vanadium redox flow battery, Appl. Energy 336 (2023) 120867.
[8] X. Qiu, X. Yang, Q. Zhou, N. Zheng, Z. Sun, A promising catalyst for catalytic reduction of V2O5 to synthesize the V3.5+ electrolytes for vanadium flow batteries, J. Electroanal. Chem. 996 (2025) 119406.
[9] H.Y. Hu, M.S. Han, J. Liu, K.X. Zheng, Z.Y. Zou, Y.B. Mu, F.H. Yu, W.J. Li, L. Wei, L. Zeng, T.S. Zhao, Strategies for improving the design of porous fiber felt electrodes for all-vanadium redox flow batteries from macro and micro perspectives, Energy Environ. Sci. 18 (2025) 3085-3119.
[10] N. Zheng, X. Qiu, S.Jin, Z. Xu, M. Zhou, Z. Zhou, T. Zhou, Z.Sun, Preparation of V4 +electrolyte by nanofluid-based electrocatalytic reduction of V2O5 for vanadium redox flow batteries, Electrochim.Acta 513 (2025)145532.
[11] M.Y. Lu, C. Yin, Q. Ma, H.N. Su, P. Lu, Z.Q. Dai, W.W. Yang, Q. Xu, Flow field structuredesignforredoxflowbatery:developmentsand prospects,J.ergy Storage 95 (2024) 112303.
[12] Z.B. Huang, Y.L. Liu, X. Xie, J.J. Wu, Y.S. Deng, Z.G. Xiong, L.X. Wu, Z. Li, Q. Huang, Y.S. Liu, Y.Luo, C. Zhang, Design and optimization of a novel flow field structure to improve the comprehensive performance of vanadium redox flow batteries, J. Power Sources 640 (2025) 236736.
[13] R. Gundlapalli, A. Bhattarai, R. Ranjan, P.C. Ghimire, X.M. Yeo, N.A. Bin Zainudin, N. Wai, F. Mahlendorf, A. Jasincuk, H. Thorsten, Characterization and scale-up of serpentine and interdigitated flow fields for application in commercial vanadium redox flow batteries, J. Power Sources 542 (2022) 231812.
[14] M. Messaggi, C. Gambaro, A. Casalegno, M. Zago,Development of innovative flow fields in a vanadium redox flow battery: design of channel obstructions with the aid of 3D computational fluid dynamic model and experimental validation through locally-resolved polarization curves, J. Power Sources 526 (2022) 231155.
[15] O.C. Esan, X. Shi, Z.Pan, X. Huo,L. An,T.S. Zhao, Modeling and simulation of flow batteries, Adv. Energy Mater.10 (2020) 2070133.
[16] X.Ke,J.M. Prahl, J.LD. Alexander,J.S. Wainright, T.A. Zawodzinski,R.F.Savinell, Rechargeable redox flow batteries: flow fields, stacks and design considerations, Chem. Soc. Rev. 47 (2018) 8721-8743.
[17] J. Ha, Y.Y. Choi, Y. Kim, J.-N. Lee, J.-I. Choi, Two-layer hydrodynamic network model for redox flow batery stack with flow field design,Int. J. Heat Mass Tran. 201 (2023) 123626.
[18] E.Ali, J. Kim, H. Park, Numerical analysis of modified channel widths of serpentine and interdigitated channels for the discharge performance of vanadium redox flow batteries, J. Energy Storage 53 (2022) 105099.
[19] Q. Xu, T.S. Zhao,P.K. Leung, Numerical investigations of flow field designs for vanadium redox flow batteries, Appl. Energy 105 (2013) 47-56.
[20]F. Li, Y. Wei, P. Tan, Y. Zeng, Y. Yuan, Numerical investigations of effects of the interdigitated channel spacing on overall performance of vanadium redox flow batteries, J. Energy Storage 32 (2020) 101781.
[21] Z. Wang,R. Su, H. Jiang, T. Zhao, Understanding and enhancing the under-rib convection for flow-field structured vanadium redox flow batteries, Int. J. Heat Mass Tran. 230 (2024) 125789.
[22] C.R. Dennison, E. Agar, B. Akuzum, E.C. Kumbur, Enhancing mass transport in redox flow batteries by tailoring flow field and electrode design, J. Electrochem. Soc. 163 (2016) A5163-A5169.
[23] L.Wei, Z.X. Guo, J. Sun, X.Z. Fan, M.C. Wu, J.B. Xu, T.S. Zhao,A convectionenhanced flow field for aqueous redox flow batteries, Int. J. Heat Mass Tran.179 (2021) 121747.
[24] L.M. Pan, J. Sun, H.H. Qi, M.S.Han,L.P. Chen, J.H. Xu,L.Wei, T.S. Zhao, Alongflow-path gradient flow field enabling uniform distributions of reactants for redox flow batteries, J. Power Sources 570 (2023) 233012.
[25] L. Pan, J. Xie, J. Guo, D.Wei,H. Qi, H. Rao,P.Leung,L. Zeng, T. Zhao,L. Wei, In-plane gradient design of flow fields enables enhanced convections for redox flow batteries, Energy Advances 2 (2023) 2006-2017.
[26] M.Y.Lu, Y.M. Deng, W.W. Yang, M. Ye, Y.H. Jiao, Q. Xu, A novel rotary serpentine flow field with improved electrolyte penetration and species distribution for vanadium redox flow battery, Electrochim. Acta 361 (2020) 137089.
[27] Y.W. Chai, D.W. Qu, L.Y. Fan, Y.T. Zheng,F. Yang, A double-spiral flow channel of vanadium redox flow batteries for enhancing mass transfer and reducing pressure drop,J. Energy Storage 78 (2024) 110278.
[28] Q. Cheng,M.-J. Li, R.-L. Wang, S. Du, T.-C. Hung, Design and optimization of guide flow channel for vanadium redox flow battery based on the multi-field synergy, J. Power Sources 650 (2025) 237526.
[29] Q.D. Zhang, H.B. Liu, Q.Q. Shi, S. Tang, Numerical simulation of flow field structure of vanadium Redox flow battery and its optimization on mass transfer performance, J.Electrochem. Soc.171 (2024) 063501.
[30] S. Saha, K.K. Maniam, S.Paul, V.S.Patnaikuni, Hydrodynamic and electrochemical analysis of compression and flow field designs in vanadium Redox flow batteries, Energies 16 (2023) 6311.
[31] B.Y. Xiong, Y. Li, Y.M. Ding, J.S.Wang, Z.B. Wei, J.Y. Zhao, X.M. Ai, J.K. Fang, Numerical analysis of vanadium redox flow batteries considering electrode deformation under various flow fields, J. Power Sources 564 (2023) 232814.
[32] R. Gundlapalli, S. Jayanti, Effective splitting of serpentine flow field for applications in large-scale flow batteries, J. Power Sources 487 (2021) 229409.
[33] X. Xie, Y. Liu, Z. Huang, Z. He, Y. Liu, Q. Huang, Z. Guo, B. Zhang, Numerical analysis of the design optimization obstruction to guide electrolyte flow in vanadium flow batteries, J. Energy Storage 101 (2024) 113802.
[34] Z.B.Huang, A.L. Mu, L.X. Wu, H. Wang, Y.J. Zhang, Electrolyte flow optimization and performance metrics analysis of vanadium redox flow battery for large-scale stationary energy storage, Int. J. Hydrogen Energy 46 (2021) 31952-31962.
[35]J.Sun,M. Zheng, Z. Yang,Z. Yu, Flow field design pathways from lab-scale toward large-scale flow batteries, Energy 173 (2019) 637-646.
[36]R. Su, Z.Wang, Y. Cai, J. Ying, H.Li, T. Zhao,H. Jiang, Scaling up flow fields from lab-scale to stack-scale for redox flow batteries, Chem. Eng.J. 486 (2024) 149946.
[37] F. Wang, G. Xiao, F. Chu, Mass transfer enhancement in electrode and battery performance optimization of all-vanadium flow based on channel section reconstruction, Chem. Eng. J. 451 (2023) 138619.
[38] T. Zhou, Z.N. Xu, N.B. Zheng, Z.Q. Sun, An image analysis-based method to determine the vanadium electrolyte contents during the capacity recovery process with a facile chemical oxidation strategy, J. Electroanal. Chem. 977 (2025) 118834.
[39] J. Sun, H.R. Jiang, B.W. Zhang, C.Y.H. Chao, T.S. Zhao, Towards uniform distributions of reactants via the aligned electrode design for vanadium redox flow batteries, Appl. Energy 259 (2020) 114198.
[40] D. Slawinski, S. Bykuc, M. Glinski, P. Chaja, Improving the current-voltage characteristics in a vanadium redox flow battery by using bipolar plates with wider channels, J. Energy Storage 129 (2025) 117154.
[41] M. Yue, Z.Q. Lv, Q. Zheng, X.F. Li, H.M. Zhang, Battery assembly optimization: tailoring the electrode compression ratio based on the polarization analysis in vanadium flow batteries, Appl. Energy 235 (2019) 495-508.
[42] T.H. Wang, Z. Yuan, Enhanced performance and reduced pumping loss in vanadium flow battery enabled by a leaf-vein-inspired flow field design, J. Energy Storage 114 (2025) 115720.
[43] J. Ren, Z. Guo, Y. Wang, J. Sun, Z.Wang, B.Liu, X. Fan, T. Zhao, A convection-enhanced flow field with height-changing ribs for redox flow batteries, Chem. Eng. J. 500 (2024) 157008.
[44] Z. Guo, J. Sun, Z. Wang,X. Fan, T. Zhao,Numerical modeling of interdigitated flow fields for scaled-up redox flow batteries, Int. J. Heat Mass Tran. 2O1 (2023) 123548.
[45] J.H. Wang, A.L. Mu, B. Yang, Y.P. Wang, W.Y. Wang, Numerical simulation of allvanadium redox flow battery performance optimization based on flow channel cross-sectional shape design, J. Energy Storage 93 (2024) 112409.
[46] Z. Huang,A. Mu, Numerical research on a novel flow field design for vanadium redox flow batteries in microgrid, Int. J. Energy Res. 45 (2021) 14579-14591.
[47] Z. Huang, C. Yang, X. Xie, B. Yang, Y. Liu, Z. Guo, Attributes and performance analysis of all-vanadium redox flow battery based on a novel flow field design, Ionics 29 (2023) 2793-2803.
[48] M. Pang, J. Liu, W. Liu, C. Han, E.D. Ozdemir, M.H. Aksel, Thermal-and-energyconservation optimization of the cooling plate for IGBT by field synergy and entropy generation, Int. J. Heat Fluid Flow 108 (2024) 109453.