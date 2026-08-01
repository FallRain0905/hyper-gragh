# The impact of flow channel shape on the creep rate and degradation of vanadium-redox flow battery components

Daniel Slawinski D

Itutesbo st. Gdansk 80-231,Poland

# HIGHLIGHTS

# GRAPHICAL ABSTRACT

·BPs with sinusoidal constrictions had a lower creep deformation. ·Additional constrictions in the channels increased the stiffness of the BP. ·Greater plate stiffness means less stress and longer component life. ·Introduction of sinusoidal constrictions increased the depth of stress relaxation. ·The modified LMP more precisely indicated the most exploited area.

![](images/28fdf939e1c54437e6035dfba90104d45ecc501aaeb029b4f3066998a1c09d0d.jpg)

# ARTICLEINFO

# ABSTRACT

Keywords: Vanadiumredox flow batteries Stress redistribution Creep phenomenon Larson-miller parameter Fluid-solid interaction

The pursuit of higher energy density can put more stress on flow battery components and lead to faster degradation.In this work,several variants of bipolar plates were examined to evaluate how the introduced changes affect their degradation rate.To do this,the creep process of the bipolar plates and membrane was monitored throughout the battery's life cycle.The Larson-Miller parameter was used to estimate the degradation rate.A novel scientific contribution of this work is theaddition ofamodification to the Larson-Miller formula, which allows for a more precise assessment of the most stressed areas. Choosing the correct number of flow channel constrictions and their shape not only significantly increased the curent produced but also enhanced the stiffness of the bipolar plates,resulting in slower degradation processes.An essential aspect of the work is to demonstrate how the stress field redistributes over the ten years of flow battery operation.

# 1. Introduction

Although redox flow batteries have undergone extensive development, they continue to encounter significant technical challenges.A primary issue is the low current flux produced by the stack,which restricts the potential applications of vanadium redox flow batteries (VRFBs)and renders them less competitive compared to lithium-ion batteries.In response,researchers at various institutions have implemented design modifications that enhance flow battery performance [1-3].

The first method to enhance efficiency is to adjust the geometry of the flow channels.For bipolar plates equipped with classic parallel flow channels (CPFF),the most common way to boost the battery's electrochemical efficiency is to add constrictions or obstructions in the channel cross-section.These obstructions create additional convective flux, thereby increasing the generated current.This method is thoroughly described in [4-6]. Xiao and Yang [7] demonstrated that introducing spheroidal shapes with suitable channel length-to-width

# Nomenclature

# Abbreviations

CFD Computational Fluid Dynamics CSD Computational Solid Dynamics FSI Fluid-Solid Interaction CPFF Classical Parallel Fluid Flow BP Bipolar Plates FF Flow Frame LMP Larson-Miller Parameter IEM Ion-Exchange Membrane RES Renewable Energy Sources SFF Serpentine Fluid Flow SoC State of Charge VRFB Vanadium Redox Flow Battery DC Direct Current AC Alternating Current

# Parameters

$h$ Medium enthalpy, $\mathbf { J } ~ \mathrm { k g ^ { - 1 } }$
$J _ { i }$ Diffusion flux, $\mathbf { k g \ m } ^ { - 2 }$
$\boldsymbol { J } _ { i } ^ { q }$ The Fourier heat conduction, $\mathrm { W m } ^ { - 2 }$
$J _ { i } ^ { u }$ The total inertial energy flux, $\textrm { W m } ^ { - 2 }$
$n _ { \perp }$ Vector normal to surface
$D = 1 / \alpha$ Diagonal matrices, $\mathrm { m } ^ { - 2 }$
$v _ { i }$ Flow velocity, $\mathrm { ~ m ~ s ~ } ^ { - 1 }$
$F$ Faraday's constant, $F = 9 . 6 4 8 5 \times 1 0 ^ { 4 } \mathrm { C ~ m o l } ^ { - 1 }$
$e$ The electric charge, $e = 1 . 6 0 2 \times 1 0 ^ { - 1 9 } \mathrm { C }$
$I _ { i }$ Electric current,A
$T$ Temperature,K
$u$ Internal energy, J
Eij Strain tensor, $\mathrm { { m } } / \mathrm { { m } }$

# Subscripts

$f$ Fluid
$s$ Solid
$\alpha , \beta$ ith and $j \mathrm { t h }$ component of species, permeability of layer
$V$ Volume, $\mathbf { m } ^ { 3 }$
$A$ Area, $\mathbf { m } ^ { 2 }$
q Heat
an, cat Anode and cathode
ref Reference
eff Effective
$u$ Internal energy

# Greek symbols

dA Partial area, $\mathtt { m } ^ { 2 }$
$\rho$ Density, ${ \bf k } { \bf g } { \bf m } ^ { - 3 }$
$\delta _ { i j }$ Kronecker delta $\delta _ { i j } ~ = ~ \delta _ { i i } { \vec { e } } _ { i } \otimes { \vec { e } } _ { j }$ where if $i = j$ it $\delta _ { i i } = 1$ and if $i \neq j$ it $\delta _ { i i } = 0$
$p$ The static pressure, Pa
$\tau _ { i j }$ The shear stress,Pa
$\mu$ Molecular Viscosity, Pa s
$\eta$ Efficiency
$S$ The source of momentum in porous model
$Y$ The mass fraction of species

<table><tr><td></td><td></td></tr><tr><td>?</td><td>Porosity</td></tr><tr><td>p</td><td>Electric potential, V</td></tr></table>

ratios optimally affects the uniform distribution of reaction components across the electrode surface,thereby increasing the generated current density.The results indicated that a properly designed constriction not only enhances electrochemical efficiency but also boosts the stiffness of the entire stack.

Xiong and Jing [8] demonstrated that a properly designed stack has a uniform stress distribution and that the assembly stresses needed for tightness prevent uncontrolled electrolyte leakage.The computational model was limited to calculating elastic strains,ignoring the significant effect of permanent strains caused by thermal creep of the components. At low temperatures,below $0 . 4 ~ \mathrm { T m }$ (where Tm is the melting point), creep strains develop similarly to plastic flow,based on slip mechanisms [9].The estimated reduced von Mises stress in the membrane during normal operation was about $3 \ \mathrm { M P a }$ ,aligning with the results in this paper.An essential aspect of estimating residual and thermal stresses at the interface between bipolar plates (BP) and the flow frame (FF) was discussed by Nam and Lee [1O].The high stress peak generated at the interface was reduced by applying suitable surface hardening technology during component manufacturing. Cai and Zhou et al.[11] noted that one of the primary challenges in designing and configuring a stack is maintaining consistent compression and compensating for stress fluctuations during operation.A key condition for achieving this is understanding the relationship between stack stresses and their performance.As noted in [l2],the creep phenomenon and the likelihood of failure are heavily affected by stress changes during operating cycles.

The surface of the ion-selective membrane is the last priority area for improving efficiency and current density.Badenhorst and Sanz et al.[13],using carbon ink coatings on the negative electrode and modern ion-exchange membranes (IEMs),achieved a current eficiency of up to $8 5 \%$ at a current density of $2 0 ~ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ . Such a large current flow can be obtained with high concentrations of components,which consequently leads to high osmotic pressures.Cai and Li [14] observed that an increased propagation velocity characterizes cracks under cyclic loading with a higher mean stress.Additionally,the same cyclic plastic zone size occurs at different stress ratios,suggesting that fatigue damage depends primarily on the stress amplitude.Wang and Guo [15] identified fatigue cracking as the main cause of membrane degradation. Theyalso found that the rate of fatigue crack growth mainly depends on the load profile.Lin and Yao [16],studying biaxial fatigue of an ion-exchange membrane,showed that increasing pressure raises stress and accelerates plastic strain buildup in the membrane.Higher temperatures and lower humidity reduce the yield stress,which shortens the membrane's fatigue life.Additionally,lowering the temperature can cause large secondary leaks,greatly reducing the device's efficiency. According to [17],mechanical degradation of the membrane is the primary cause of failure during the early stages of operation.

Amjadi and Fatemi [18] demonstrated that the Larson-Miller parameter can be used to estimate time to failure due to creep in polyethylene components.They also observed that creep strength decreases while creep strain and creep rate increase with rising temperature.Gibhardt D,Krauklis A,etal.[19] confirmed the usefulness of the Larson-Miller Parameter (LMP) in estimating the failure time of polymer and epoxy samples.

The advantage of flow batteries is their long,trouble-free operation. The disadvantage,however,is the low current output. This work focuses on demonstrating the impact of modifying the geometry of flow channels in bipolar plates on maintaining the long life of flow battery components.As mentioned earlier,the introduction of sinusoidal constrictions led to the induction of additional convective flux, thereby improving the current-voltage characteristics of the VRFB.Inappropriate implementation of design changes focused solely on electrochemical aspects can expose the device to premature failure.To estimate component degradation, CSD simulations were used, revealing the permanent strain field caused by the creep of the bipolar plates and the ionexchange membrane.A new scientific finding is the demonstration of stress redistribution in the components over 1O years of flow battery operation. Studies found in the literature typically show the stress field resulting from assembly errors,incorrect technological processes, or loads in the nominal state of the stack.To estimate the impact of the shape modifications on failure-free operation time,the Larson-Miller parameter was used,integrating additional procedures into a commercial calculation code.It is important to note that the Larson-Miller parameter is widely employed in engineering to assess the creep resistance of materials at high temperatures.Its main limitation is its ability to pinpoint the most stressed regions for a given temperature distribution. To enhance the procedure's detail,a proprietary correction was added to the Larson-Miller formula.An additional formula accounts for the effects of the direction of maximum shear stress, hydrostatic pressure,and the specific failure mechanism present in the material.The first term is represented by the third fundamental invariant of the stress deviator, $J _ { 3 S }$ .The second term corresponds to the stress trace,expressed by the first principal invariant of the stress tensor, $I _ { \sigma }$ . The third term is defined according to the Stobyriev hypothesis.A comprehensive explanation of the model is presented in the theoretical section, Section 2.2.4. Comparing the scalar fields from the classical and modified formula showed that the formula with the author's correction was more accurate.

Table 1Geometric parameters of the VRFB model [20].

<table><tr><td>Parameters</td><td>Symbol</td><td>Unit</td><td>Value</td></tr><tr><td>Cell number of stack</td><td>nc</td><td>1</td><td>15</td></tr><tr><td>Canal width,height, length</td><td>Wc,Hc,Lc</td><td>mm</td><td>4.8,1,100</td></tr><tr><td>Active area</td><td>Am</td><td>cm²</td><td>86.4</td></tr><tr><td>Thickness of Membrane</td><td>δMEM</td><td>mm</td><td>0.2</td></tr><tr><td>Electrode thickness (carbon felt)</td><td>δELE</td><td>mm</td><td>4</td></tr><tr><td>Electrode porosity</td><td>Φ</td><td>1</td><td>0.68</td></tr><tr><td>Membrane porosity</td><td>?</td><td>1</td><td>0.28</td></tr></table>

# 2.Numerical model

# 2.1.Problem formulation

Classic paralel-flow channels,as shown in Variant 1,provide many benefits,including low flow resistance through the collector.This design allows multiple cells to be connected into large stacks (Fig.1). Detailed dimensions and material and physical properties are given in Tables 1 and 2.However, it has drawbacks such as low current density and the necessity for a high mass flow rate.The authors'introduction of sinusoidal constrictions in the channel cross-section created additional vertical convective flux in these areas.With better reagent distribution, the efficiency of electrochemical reactions improved,leading to higher current density.Additionally,the authors aimed to show how the design modifications to boost electrochemical eficiency helped ensure long-term,failure-free operation of the VRFB.Computational Solid Dynamic (CsD） simulations were conducted to analyze ten years of continuous operation of a single cell with four different types of bipolar plates.Individual BP loading forces for each channel variant were determined through Computational Fluid Dynamic (CFD) simulations. These simulations also generated current-voltage characteristics,confirming improvements in the electrochemical parameters of the VRFB. Monitoring the evolution of permanent strains showed how stress distributions changed across the BP variants and how they redistributed over the 1O-year operational period.

Additionally,the Larson-Miller parameter,which assesses the degradation rate of the Bipolar Plates and membrane based on temperature and operating time,was estimated.To accurately identify the areas of greatest effort,the author's closure formula was applied to the classical Larson-Miller equation.This boundary employs Stobyriev's hypothesis to describe the mixed-mode failure mechanism.This hypothesis combines ductile failure,represented by the second fundamental invariant of the stress tensor,with brittle failure.The britte failure is caused by stresses acting perpendicular to the developing crack.

Comparing the stress field and permanent deformation over the entire operating time of a VRFB equipped with the considered BP variants enabled us to select the most effective shape for the new flow channels while maintaining the battery's durability and failurefree operation. In other words,we could overcome the disadvantage of low current flux without losing the most significant advantage of VRFBs: their durability.

# 2.2.Mathematical formulation

# 2.2.1.Conservation equations

The mathematical model is based on the following assumptions [22]

·Time-varying phenomena were used to calculate the evolution of strain and stress fields during creep of VRFB components.
·All domains are assumed to be isothermal,with no temperature changes.
·The fluid flow is considered incompressible.
·Gravitational effects are ignored.

# 2.2.2.Maxwell's material model

The Maxwell material connects the virtual spring and damper models in series.The differential equation takes the form.

$$
\eta \dot { \varepsilon } = \sigma + \frac { \eta } { E } \dot { \sigma }
$$

where: $\eta , E$ ,is dynamic viscosity,Pa s,and Young modulus in $\bf { M P a }$ ， respectively.

With a constant loading and unloading impulse,the creep and relaxation phenomenon takes place according to the formula:

$$
\varepsilon ( t ) = \left\{ \begin{array} { c c } { \frac { \sigma } { E } + \frac { \sigma } { \eta } t } & { t < t _ { 1 } } \\ { \frac { \sigma t } { \eta } } & { t > t _ { 1 } } \end{array} \right.
$$

During constant deformation, the stress relaxes to zero

$$
\sigma ( t ) = \sigma \exp \left( - \frac { E t } { \eta } \right)
$$

After a time called relaxation time $t = t _ { r }$ ,the stress decreases to the value

$$
\sigma ( t _ { r } ) = 0 . 3 7 6 \sigma
$$

2.2.3.Creep rate in the second and third stages described by the Norton-Bailey and Kachanov model

The development of permanent strain observed in the second and third stages occurs when creep strain and microcracks resulting from brittle fractures develop simultaneously. Permanent deformations due to creep lead to thermal failure,and loosening caused by structural defects in the mesh leads to the development of micro and minicracks [23].

The development of micro-cracks [24] and gaps reduces the sample cros-sectional area during creep.Therefore,the surface change parameter was defined as:

$$
\omega = ( A - a ) / a
$$

where: $A$ : is the original sample area,and $a$ is the total defect area.

Table 2Mechanical parameters of the VRFB model [21].

<table><tr><td rowspan="2">Parameters</td><td rowspan="2">Symbol</td><td rowspan="2">Unit</td><td colspan="4">TemperatureC</td></tr><tr><td>20</td><td>30</td><td>40</td><td>50</td></tr><tr><td rowspan="3">Young modulus of BP</td><td>E11</td><td>GPa</td><td>142</td><td>128</td><td>114</td><td>100</td></tr><tr><td>E22</td><td>GPa</td><td>13.7</td><td>12</td><td>11</td><td>9.7</td></tr><tr><td>E33</td><td>GPa</td><td>13.7</td><td>12</td><td>11</td><td>9.7</td></tr><tr><td>Poisson&#x27;s ratio</td><td>Y11, Y22, Y33</td><td>二</td><td>0.26</td><td>0.26</td><td>026</td><td>0.26</td></tr><tr><td rowspan="3">Shear modulus of BP</td><td>G12</td><td>MPa</td><td>5.6</td><td>6</td><td>6.6</td><td>7</td></tr><tr><td>G23</td><td>MPa</td><td>0.4</td><td>6.7</td><td>13</td><td>25</td></tr><tr><td>G31</td><td>MPa</td><td>0.4</td><td>6.7</td><td>13</td><td>25</td></tr><tr><td>Thermal conductivity of BP</td><td>λ</td><td>Wm-1 K</td><td>1.2</td><td>1.2</td><td>1.25</td><td>1.28</td></tr><tr><td>Thermal expansion of BP</td><td>α</td><td>Cx10-6</td><td>1.5</td><td>1.5</td><td>1.53</td><td>1.54</td></tr><tr><td>Density of BP</td><td>P</td><td>kg m-3</td><td>1850</td><td>1850</td><td>1850</td><td>1850</td></tr><tr><td rowspan="3">Young modulus of Membrane</td><td>E11</td><td>MPa</td><td>14</td><td>15</td><td>17</td><td>18</td></tr><tr><td>E22</td><td>MPa</td><td>1</td><td>24</td><td>42</td><td>64</td></tr><tr><td>E33</td><td>MPa</td><td>1</td><td>24</td><td>42</td><td>64</td></tr><tr><td>Poisson&#x27;s ratio</td><td>Y11, Y22, Y33</td><td>二</td><td>0.26</td><td>0.26</td><td>026</td><td>0.26</td></tr><tr><td rowspan="3">Shear modulus of Membrane</td><td>G12</td><td>MPa</td><td>54</td><td>49</td><td>44</td><td>38</td></tr><tr><td>G23</td><td>MPa</td><td>5.3</td><td>4.7</td><td>4.2</td><td>3.7</td></tr><tr><td>G31</td><td>MPa</td><td>5.3</td><td>4.7</td><td>4.2</td><td>3.7</td></tr><tr><td>Thermal conductivity of Membrane</td><td>入</td><td>Wm-1 K</td><td>1.2</td><td>1.2</td><td>1.25</td><td>1.28</td></tr><tr><td>Thermal expansion of Membrane</td><td>α</td><td>Cx10-6</td><td>1.5</td><td>1.5</td><td>1.53</td><td>1.54</td></tr><tr><td>Density of Membrane</td><td>P</td><td>kg m-3</td><td>1650</td><td>1650</td><td>1650</td><td>1650</td></tr></table>

![](images/983e58e9e5613e5cf8f40543ba2f72120b9b0302e38fa2cacd67cd0d5f415437.jpg)
'ig.1.Modified shapes of the fluid flow in the Bipolar Plate from a Vanadium-Redox flow battel

Initially,the function is zero,and it is unity at the moment of destruction

$$
t _ { 0 } = 0 \quad \omega ( t _ { 0 } ) = 0 \quad t = t _ { r } \quad \omega ( t _ { r } ) = 1
$$

The rate of evolution of the parameter $\omega$ is most often adopted in the form of a power function similar to that proposed by Norton-Bailey [25] for both the plastic and britle types:

$$
\dot { \omega } = f ( \sigma ) = f \left[ \frac { \sigma } { ( 1 - \omega ) } \right] f ( \sigma ) = C \sigma ^ { S } f ( \sigma ) = B \sigma _ { 0 } ^ { n }
$$

where: $C , s , B , n \colon$ are material parameters strongly dependent on temperature.

The increment of strain resulting from creep for the second and third states was described by the formula [26]:

$$
\frac { d \varepsilon _ { i j } } { d t } = \frac { 3 } { 2 } A \left( \frac { \sigma _ { e q } } { 1 - \omega } \right) ^ { n } \frac { s _ { i j } } { \sigma _ { e q } } t ^ { m }
$$

$$
\frac { d \omega } { d t } = B \frac { \sigma _ { S t } ^ { \chi } } { \left( 1 - \omega \right) \phi } t ^ { m }
$$

$$
\sigma _ { S t } = p _ { S } \sigma _ { R } + \left( 1 - p _ { S } \right) \sigma _ { H M H }
$$

$$
\sigma _ { R } = \operatorname* { m a x } \left( \sigma _ { 1 } , \sigma _ { 2 } , \sigma _ { 3 } \right)
$$

where: $A , n , m$ are the material constants describing the creep process, taken in sequence: for the BP material, $3 . 2 7 \times 1 0 ^ { - 1 2 }$ ，4.8,1； for the Membrane material, $1 . 4 3 \times 1 0 ^ { - 1 0 }$ ,5,1.The second formula defines the failure parameter associated with the third stage of creep.Model parameters were identified through validation against experimental data and are as follows: for Membrane material, $B = 3 . 2 5 \times 1 0 ^ { - 2 5 } , \varphi = 1$ ， and $\chi = 2 3 . 4 6 ;$ forBP, $B = 5 . 3 2 \times 1 0 ^ { - 2 8 } , \varphi = 1$ ,and $\chi = 2 5 . 4 6$

$\sigma _ { R }$ are the maximum Rankine stress normal to the crack direction. The $p _ { S }$ coefficient is a parameter describing the influence of maximum principal stresses on the value of stresses reduced,according to Stobyriev's.Therefore,this parameter will determine the nature of the material deformation, from purely ductile taking O and brittle having a value of 1.As mentioned in the previous subpoints, the specific energy of shear strains, described by Huber-Mises-Hencky's hypothesis $\sigma _ { H M H }$ ， determines the failure of ductile materials [27].In turn, the destruction of brittle materials depends mainly on the principal stresses occurring in the direction perpendicular to the development of microcracks.

# 2.2.4.Classic and modified Larson-Miler parameter formula

Assuming,by Cauchy's postulate,the division into symmetric and asymmetric parts,we obtain the stress tensor in the form [28]:

$$
\sigma _ { i j } = - p \delta _ { i j } + \tau _ { i j }
$$

vhen: $\delta _ { i j }$ is the Gibbs unit tensor, $\delta _ { i j } = \delta _ { i i } \mathbf { e } _ { i } \otimes \mathbf { e } _ { j }$

The tensor $p$ responsible for the hydrostatic pressure,having no direct influence on the creep processes in the material, is written in the form:

$$
p = - \frac { 1 } { 3 } \sigma _ { k k } \delta _ { i i } = - \frac { 1 } { 3 } \left( \sigma _ { x x } + \sigma _ { y y } + \sigma _ { z z } \right)
$$

On the other hand,the viscous stress tensor,which is directly dependent on the deformation rate tensor,was written in the form:

$$
\begin{array} { r l } & { \tau _ { i j } = 2 \mu \varepsilon _ { i j } + \lambda \varepsilon _ { k k } \delta _ { i j } } \\ & { } \\ & { \varepsilon _ { i j } = \frac { 1 } { 2 } \left( \mathrm { g r a d } _ { i } v _ { j } + \mathrm { g r a d } _ { j } ^ { T } v _ { i } \right) } \end{array}
$$

when: $\varepsilon _ { i j }$ is the rate of deformation, while $\mu , \lambda$ is Lame's coefficients.

The stress tensor deviator is written us as [29]:

$$
s _ { i j } = \sigma _ { i j } - \frac 1 3 \sigma _ { k k } \delta _ { i j }
$$

The reduced stresses we were presented as a combination of the first and second main invariants $I _ { \sigma } , I I _ { \sigma }$ written in the form [30]

$$
\begin{array} { l } { I _ { \sigma } = \sigma _ { 1 } + \sigma _ { 2 } + \sigma _ { 3 } } \\ { \ } \\ { I I _ { \sigma } = \sigma _ { 1 } \cdot \sigma _ { 2 } + \sigma _ { 2 } \cdot \sigma _ { 3 } + \sigma _ { 3 } \cdot \sigma _ { 1 } } \\ { \ } \\ { \sigma _ { H M H } = \sqrt { I _ { \sigma } ^ { 2 } - 3 I I _ { \sigma } } = \sqrt { \frac { 3 } { 2 } } \sqrt { \sigma _ { i j } \cdot \sigma _ { i j } - \frac { 1 } { 3 } \sigma _ { i i } \cdot \sigma _ { j j } } } \end{array}
$$

After introducing the definition of the second basic stress invariant $J _ { 2 s }$ from the stress deviator, the stress scalar takes the following form [31]:

$$
\begin{array} { l } { { J _ { 2 S } = I I _ { \sigma } + \displaystyle \frac { 1 } { 3 } I _ { \sigma } ^ { 2 } = \displaystyle \frac { 1 } { 2 } s _ { i j } \cdot s _ { i j } } } \\ { { { } } } \\ { { \sigma _ { H M H } = \sqrt { - J _ { 2 S } } = \sqrt { \displaystyle \frac { 3 } { 2 } s _ { i j } \cdot s _ { i j } } } } \end{array}
$$

The classical definition of the Larson-Miller parameter is expressed by the formula:

$$
L M P = ( 1 . 8 \cdot T + 4 9 1 ) ( C + \log { ( t ) } )
$$

where: $T , C , t$ is the temperature given in degrees Kelvin and converted to degrees Rankine in the left part of the formula, the material constant assumed for polymers at the value of 48,consequently,and the rupture time in h[32]

For the modified formula,an additional term was included to account for the type of failure mechanism (brittle,ductile,or mixed) as described by Stobyriev's stress hypothesis $\sigma _ { S t }$ ,the effect of hydrostatic pressure $I _ { \sigma }$ on volume changes especially noticeable in brittle materials and the direction of shear stresses represented by the third fundamental invariant of stress $J _ { 3 S }$ ：

$$
L M P _ { m o d } = \left( 1 . 8 \cdot { T } + 4 9 1 \right) \left( C + \log \left( t \right) \right) + A \left( \frac { \sigma _ { S t } } { I _ { \sigma } } J _ { 3 S } \right)
$$

$$
J _ { 3 S } = \operatorname* { d e t } \left( s _ { i j } \right) = s _ { 1 } \cdot s _ { 2 } \cdot s _ { 3 }
$$

where: $A$ is the coefficient assumed as $0 . 0 0 1 \mathrm { M P a } ^ { - 3 }$ .

The selection of the $A$ coefficient was based on the assumption that adding the next part to the LMP formula should not drastically increase the value of the calculated parameter,but merely impose and emphasize the stress field mode.The parameter already includes a component for mechanical loading,and a radical increase in its value would prevent the use of existing LMP diagrams prepared for specific materials.The benefits of the applied corrections are well illustrated in the figures in Appendix.

# 2.3. Boundary conditions

Fig.2 shows the flow battery operation scheme and the boundary conditions used during the CFD/CSD simulation. The computational model consisted of a flow collector on the anode and cathode sides. Both collectors are separated by an ion-selective membrane [33].The electrolyte on the anode and cathode sides was supplied separately, and ion exchange only occurred through the ion-selective membrane, modeled as a porous medium.The ion-selective membrane allowed the flow of hydrogen ions and blocked the flow of electrons [34]. Blocking the flow of electrons through the membrane was achieved due to the low coefficient of electrical conductivity. Chemical reactions were possible on the electrodes’external surfaces and volume.The electrodes were modeled as a porous medium [35].Detailed physical data and the values of the coefficients are shown in Table 3.The data regarding the structure of the computational grid are described in the following subsection.

At the inlet to the flow channels,the initial pressure was assumed to reflect the operation of a variable displacement pump.The medium's flow resistance determined the pressure within each channel.The steady-state temperature fields resulted from the exothermic nature of the chemical reactions.Both pressure and temperature fields were obtained through CFD simulations.The mechanical loads considered in the CSD simulation were due to the medium's flow through the channels and the assembly stresses that ensure the tightness of a single cell.Additionally,the osmotic pressure fields caused by the uneven distribution of component and reaction product concentrations were included in the membrane load calculations [36].A symmetry condition was applied to the BP side walls.During the CFD simulation,the electrode geometry remained fixed and did not fill the flow channels despite compresson [37].Additionally,the absence of leakage and shunt currents was assumed by applying zero electric potential at the sides.The initial component concentrations and initial conditions for the simulation are shown in Table 3.

# 2.4.Validation of the numerical model

Fig.3 illustrates a two-stage verification process for the numerical model. The first stage focused on accurately determining the electrochemical parameters of the model.This validated model enabled CFD simulations to produce spatial distributions of pressure and temperature.In the second stage of verification,we mapped the static tensile test curves for both the BP material and the membrane,along with the non-stationary creep tests conducted on the aforementioned materials [4O].The rheological coefficients obtained from these tests facilitated accurate CSD simulations,the results of which are presented in the manuscript. The CFD numerical model did not take into account self-discharge,which resulted in slightly higher efficiency compared to the experimental data.In the manuscript, the current-voltage characteristics during charging and discharging were tested more extensively for the numerical model than they were in the experiment.The colored square indicates the range of experimental data.The numerical model was validated for four selected charge states of the VRFB,defined by state-of-charge (SoC) coefficients of $2 0 \%$ ， $5 0 \%$ ， $8 0 \%$ ，and $9 0 \%$ In all cases,the numerical results were consistent with the measured data [41].The curves describing the static tensile test were modeled at room temperature.Rheological parameters for the membrane material (Fig.3i) were also obtained for a single temperature and load. In the case of the BP material, the curves were modeled for four different loads and four times to failure.Fig.3k-l presents the estimation of permanent strains based on short-term experiments conducted for both the BP and the membrane.Using predictions of long-term strains during the second stage of creep,the Norton-Bailey equation coefficients were determined.The values of these coefficients are displayed in each graph.To evaluate the uncertainty in the strain curve predictions,a $5 \%$ error margin was applied to the data points.

![](images/97eaf828ca340fe08c08d34cd6108913fb429b49640c9df2d64540061012050c.jpg)
Fig.2.Boundary conditions used in numerical simulation.

Table 3 Initial conditions and flow parameters used in numerical simulation [38,39].

<table><tr><td>Name</td><td>Unit</td><td>Symbol</td><td>Value</td></tr><tr><td>Operating temperature</td><td>K</td><td>T</td><td>298</td></tr><tr><td>Anode reference pressure</td><td>Pa</td><td>Pref</td><td>0.105 ×106</td></tr><tr><td>Cathode reference pressure</td><td>Pa</td><td>Pref</td><td>0.105 ×106</td></tr><tr><td>Anode pressure inlet,outlet</td><td>Pa</td><td>P</td><td>35/3</td></tr><tr><td>Cathode pressure inlet, outlet</td><td>Pa</td><td>P</td><td>35/3</td></tr><tr><td>Reference electric potential</td><td>V</td><td>p</td><td>1.25</td></tr><tr><td>Initial V concentration</td><td>mol m-3</td><td>Cv3</td><td>1053</td></tr><tr><td>Initial V² concentration</td><td>mol m-3</td><td>CV2</td><td>27</td></tr><tr><td>Initial VO² concentration</td><td>mol m-3</td><td>Cvo²</td><td>1053</td></tr><tr><td>Initial vO concentration</td><td>mol m-3</td><td>CVO2</td><td>27</td></tr><tr><td>Initial HO concentration</td><td>mol m-3</td><td>CHO</td><td>1200</td></tr><tr><td>Initial H+ concentration</td><td>mol m-3</td><td>CH+</td><td>1200</td></tr><tr><td>Nusselt number</td><td>1</td><td>Nu</td><td>100</td></tr><tr><td>Pressing force</td><td>Pa</td><td>Ppressforce</td><td>1 ×106</td></tr></table>

Table 4 compares the computational grid's size and the convergence of the numerical results with experimental data.The first two types of meshes gave results that differed significantly from the measurement data.The third mesh allowed for accurate results while maintaining a short simulation time.In the fourth case,despite increasing the accuracy of calculations,the simulation time was extended several times.For further numerical simulations,the computational grid size was assumed for the third case.

# 3.Results and discussion

# 3.1. Creep rate of Bipolar Plates during Vanadium-Redox flow battery operation

Fig.4a illustrates the progression of creep in the four different BP geometries considered in the study.Plastic strain fields were recorded at three characteristic time points.The first observation was made after two days of operation,revealing initial regions of creep development for each geometry.These regions are located near the inlets and outlets of the flow channels and exhibit significant geometric nonlinearity, resulting in stress concentration.

Due to creep,plastic deformation occurs in the central part of the channels after the first year of operation. This phenomenon develops uniformly across all BP variants.After 1O years of operation, the highest deformations are observed in variant zero,particularly in the areas around the inlets and outlets of the flow channels.In contrast, the lowest deformations are found in variant 3.The maximum plastic deformation after 1O years of BP operation does not exceed O.00021 $\mathrm { { m m / m m } }$ ，with small variations among the different variants.These values are too small to cause microcracks and thus initiate the third state of creep.

# 3.1.1.Relaxation and stress redistribution due to creep in Bipolar Plates

Fig.4b illustrates the evolving stress field over a span of 10 years during BP operations.The maximum stress fields are aligned with the locations of the highest creep strains.In the nominal state, the maximum stress recorded is $0 . 3 2 \mathrm { M P a }$ ,with the smallest area exhibiting these values identified in the third variant.The introduction of ten necks in this variant not only enhances the electrochemical properties but also increases the stiffness of the plate,which helps reduce the stresses within the structure.Over the course of ten years,there is a noticeable reduction in the maximum stress fields; however, this is accompanied by higher stress concentrations near the central part of the plate.This phenomenon is clearly illustrated in Fig.5.

![](images/16824bb2713c652627f70ed8a540ae8b10e78f42b1c0d3807b7ecefd9ba4c473.jpg)
FigV of charge/discharge curves for different battery charge levels - SoC coefficient; $( { \tt g \mathrm { - } h } )$ static stressstrain diagram for the membrane material and BP respectively; (ipi short-term creep for the bipolar plates and membrane.

Table 4 Effect of mesh number on simulation results.

<table><tr><td>Case</td><td>Grid number of Membrane</td><td>Creep strain of Membrane / (mm/mm)</td><td>Relative error/%</td><td>Grid number ofBP</td><td>Creep strain of BP/ (mm/mm)</td><td>Relative error/%</td></tr><tr><td>1</td><td>1500</td><td>2</td><td>12.64</td><td>1000</td><td>0.09</td><td>13</td></tr><tr><td>2</td><td>2500</td><td>2.2</td><td>4.70</td><td>1500</td><td>0.08</td><td>6</td></tr><tr><td>3</td><td>2800</td><td>2.5</td><td>1.22</td><td>4000</td><td>0.06</td><td>1.1</td></tr><tr><td>4</td><td>3500</td><td>2.49</td><td>1.10</td><td>6000</td><td>0.059</td><td>0.97</td></tr></table>

The stress curves for points P1 and P2 were analyzed based on the characteristic locations identified and described in the previous subsection.In the zero variant,which serves as the reference with PFF channels,a noticeable stress drop occurs at point P1, lasting until approximately the 2Oth month of operation.For variants three and four,the stress drop is greater and lasts until the ${ 8 0 } \mathrm { t h }$ month. Following this period, the zero variant shows an increase in stress.This can be attributed to the development of permanent deformations and the resulting stress redistribution.In simpler terms,areas that were not heavily loaded initially begin to bear structural loads as plastic deformations develop.For variants three and four,complete stress relaxation is observed,in line with the Maxwell model's predictions. This complete relaxation phenomenon is particularly evident at point P2,where stresses in all variants ultimately drop to zero.For the zero variant utilizing PFF channels,the time required for complete relaxation was approximately 30 months.In the subsequent variants, where the number of constrictions along the channel increased to 3,5,and 10, this relaxation time expanded to 80 and 120 months, respectively.

Fig. 5 illustrates the changes in stress distribution measured along the length of the flow channel at selected time points.The stress curve representing the nominal state after just 1O days of operation is shown in red.For each BP variant, this curve exhibits the highest stress values,with distinctive peaks at both the beginning and end of the flow channel.In the middle section,the curve flattens out,with stress values reaching approximately one-third of the maximum readings.As the exploitation continues,the stress curve generally decreases near the previous peaks,while readings in the middle of the BP increase.The most significant reductions in stress were observed in the third variant. This improvement can be attributed to the presence of 1O sinusoidal constrictions along the length of the channel,which enhanced the stiffness of the plate.

# 3.2. Creep rate of membrane during Vanadium-Redox flow battery operation

Fig.6a shows the scalar permanent strain fields obtained as a result of creep.The strain fields were read,as in the previous section, after two days,one year,and 1O years. The largest increase in plastic strain was observed for variant O.Due to its lower electrochemical efficiency,this variant required a higher substrate mass flow to achieve the desired power ina single cell.Consequently,it experienced higher hydrodynamic,osmotic,and assembly pressures, ensuring the tightness of the structure.The highest plastic strain value after ten years was

![](images/5737b36a9430b9fdc7f538c8e7b6de2ea70c4ea5c1694f7cc9e134426b49e399.jpg)
Fig4esaci relaxation at selected points of Bipolar Plates.

![](images/f85986b2af8992c22c5873678f39dab0bfa48faaca886ca57eb1286050b6e301.jpg)
Fig.5.The redistribution of stress caused by the creep phenomenon in different variants of the Bipolar plate after ten days,first year,and ten years of operation in a flow battery.

0.0065 at the membrane periphery,and O.oo4 in the central part of the membrane.Due to their higher electrochemical eficiency, variants two and three required lower mass flows and thus generated lower membrane-loading pressures.As a consequence,the plastic strain decreased to approximately 0.oo5 at the membrane periphery and 0.0003 in the central region. The development of permanent strains led to changes in the stress fields over time,as shown in Fig. 6b.

# 3.2.1.Relaxation and stress redistribution due to creep in Membranes

In each variant, the stress field evolved over 1O years of operation. In the initial state,after 2 days of operation,the maximum stresses were approximately 5 MPa at the membrane's edges and approximately $0 . 2 ~ \mathrm { M P a }$ in the central part.The most intense areas were observed for variants O and 1.In each variant,the stress fields evolved significantly over time.The stress relaxation and redistribution process is shown in Fig.6(c-d).The first point,P1,is slightly offset from the edge,resulting in the truncation of the maximum stresses visible in the previous figure. The second point,P2,is located in the center of the membrane area.

In the zero variant,a stress drop from $0 . 3 \mathrm { M P a }$ at the initial moment to $0 . 1 6 ~ \mathrm { M P a }$ after 12O months is observed at point P1.This decrease corresponds to a 1O-year operational period.A similar relaxation time was noted in the third variant.Meanwhile,the first and second variants maintained a comparable stress range.At point P2,there is a noticeable increase in stress over time.This phenomenon is attributed to stress redistribution and the development of plastic deformation in areas that previously bore the load in the membrane.A slight increase in stress was also observed in the second and third variants,which can be explained by lower membrane loading due to the greater efficiency of the flow channels and,consequently,reduced mass flow requirements.

![](images/e1978dff7ed8a566f2b9f9ceff9f3fd07eb82ffc6169cc706aa29b2bd7694313.jpg)
Fig.6.The scalar fields of (a) equivalent creep strain and; (b) equivalent stress in the Membrane for several characteristic points during operation of VRFB; (c-d) stress relaxation and redistribution at selected points of Membrane.

In summary,introducing 1O sinusoidal constrictions in the flow channels of variant three not only enhances electrochemical eficiency but also strengthens the structure,which reduces overall stresses.As aresult, there is a decrease in the area of plastic deformation and an increasedlevel of stress relaxation observed.

3.3.Estimation of the Larson-Miller parameter according to the classical formula

Fig.7 displays maps of the Larson-Miller parameter calculated for the BP and Membrane variants,using the classic formula.The zero variantdemonstrates a uniform wear process during the VRFB's operational life.The lighter color near the inlet manifold,where the pressure is higher,indicates a more intense material degradation process.The second variant presents clearlydefined maps with different wear rates.A similar degradation process can be observed for the Membrane model. Here,the degradation process is more diverse and uneven across time points.Higher operational intensity occurs in areas of higher pressure and higher temperature.

An undoubted disadvantage of the presented maps is the lack of detail in indicating the locations most exposed to stress and therefore subject to faster degradation.

3.4.Estimation of the Larson-Miller parameter according to the modifiedformula

Fig.8 illustrates the Larson-Miller parameter calculated using a modified formula.This modification includes a term that accounts for the effects of hydrostatic pressure,the failure mechanism,and the direction of maximum shear stress.In the zero variant,after 1O days,an area near the inlet manifold shows a more pronounced developed of the degradation parameter.For the first variant,which initially exhibited a uniform degradation parameter according to the classic formula, the introduction of the modification allowed the Larson-Miller parameter to identify areas with the highest stresses.These critical areas include the inlet and outlet manifolds,as well as the center of the BP plate.As shown in Fig.4, these locations experience the greatest stresses and the most intense permanent creep deformation.

For the second and third variants,the areas around the inlet manifolds are identified as critical.In the case of the membrane,when analyzing the results with the classc formula,areas with varying degrees of degradation are organized into parallel strips.However, the addition of the modified formula revealed that areas with the same degradation parameter became more nonlinear,indicating the directions in which degradation progresses more rapidly.In other words, the areas under the highest stress are more clearly defined

# 4. Conclusions

This paper examines how modifications to the flow channel affect the durability of the bipolar plate and membrane.The introduced modifications included sinusoidal constrictions,which enhanced the electrochemical efficiency of the VRFB [42]. To estimate the degradation rate,we analyzed creep development, stress redistribution,and changes in the Larson-Miller parameter. The following conclusions were drawn from the results of this analysis:

1.Introducing constraints in the flow channels altered stress and permanent strain values,but the locations of maximum stress and creep strain did not change.
2.Introducing ten cyclic constrictions in the flow channel increased the stiffness of the BP structure.The area of creep strain decreased,and stressrelaxationimproved.
3.The flow channel constrictions reduced membrane plastic deformation,which extended membrane life,as confirmed by the LMP index.
4.Fewer constrictions,and thus lower BP stiffness,led to faster stressrelaxation.Furthermore,a larger area of plastic deformation caused greater stress redistribution.
5.The classic LMP index relied on a less precise method to identify rapidly degrading areas. Our correction to the formula enabled more accurate identification of sensitive regions.

Based on the research findings and the conclusions derived from them,we can conclude that altering the shape of the flow channels in the PFF bipolar plate has not only enhanced electrochemical efficiency and performance but has also had a minimal impact on the lifespan of the VRFB components.Additionally,the structural stiffening introduced has reduced stress, thereby prolonging the safe operating duration.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Acknowledgments

This work was financed from the statutory funds of the Institute of the Polish Academy of Sciences.

# Appendix

The appendix presents independent verification of a modified version of the Larson-Miller parameter.Verification procedures utilized the geometry of a flat specimen designed for standard tensile testing. Simulations employed both the classical Larson-Miller parameter formula and the modified version.The following discusses the observed differences in the results.A detailed theoretical discussion of the definitions of both parameter versions is presented in Section 2.2.4.

![](images/15cbfa54f0f4aecfb469c785e80675e28a7abf5481cf96a39395f770e1a376d4.jpg)
Fig.7.The scalarfieldsof the Larson-Miler Parameterin (a) Bipolar Plateand (b) Membrane fromtheclassical formula.

![](images/a93a587b00c8d298873b49e6b5174e7ca5faddab0a436c1ae98adecb174a0820.jpg)
Fig.8.The scalar fields of the Larson-Miller Parameter in (a) Bipolar Plate and (b) Membrane from the modified formula.

The Larson-Miller parameter is defined to correlate two forms of material degradation: one due to elevated temperature and the other due to mechanical cyclic loading. Fig.A.1 presents a comparison of two formulas used to estimate the Larson-Miller Parameter (LMP) during a static tensile test.This test was conducted under a non-uniform temperature field,with temperatures ranging from $1 0 0 ~ ^ { \circ } \mathrm { C }$ at the point of highest load to $2 0 ~ ^ { \circ } \mathrm { C }$ at the sample attachment points.The applied mechanical load was $1 2 0 \ \mathrm { M P a }$ ，which produced a maximum stress of $5 6 4 . 2 \ \mathrm { M P a }$ at the sample notch.At elevated stress levels, the sample exhibited plastic deformation.The convergence of the temperature field with maximum mechanical loads resulted in both the classic and modified formulations identifying identical locations and estimating maximum values at LMP $\begin{array} { r l } { = } & { { } 3 3 6 0 } \end{array}$ and $\mathrm { { L M P } _ { m o d } } \ = \ 3 5 3 4 \mathrm { { . } }$ ，The lower ranges were also nearly identical,at 264O and 2651 for the classic and modified formulations,respectively.

![](images/c2d1c7e73a0917ad5b336ecbd91d37ed29ee9e622298e00462c2cbd1e2dcb856.jpg)
Fig.A.1.Comparison of the classic and modified LMP formulas for static tensile testing under non-uniform temperature conditions.

When the temperature field is uniform, the classic formula does not identify the most stressed regions.This scenario is illustrated in Fig. A.2.The plate was uniformly heated to $2 0 ~ ^ { \circ } \mathrm { C }$ and subjected to the same loading conditions as in the previous case.The maximum stress at the notch location reached $5 6 4 . 3 \mathrm { M P a }$ ,which exceeded the yield strengthat this point.The classic formula for defining the LMP did not identify the most stressed area,whereas the modified formula accurately identified both the notch location and the stress intensity distribution along the plate.The parameter values estimated by the classic and modified formulas were similar,at 2640 and 2683,respectively.

![](images/f06eb751b3329b6abdd653d6190867fef062a0fb60468cc398be0ffbaaf1a9ea.jpg)
Fig.A.2.Comparison of the classic and modified LMP formulas for static tensile testing under uniform temperature condition.

# Data availability

Data will be made available on request.

# References

[1]P.Lu,P.Leung,H. Su,W.Yang,Q.Xu,Materials,performance,and system design for integrated solar and flow batteries-A mini review,Appl.Energy 282 (2021) 116210, http://dx.doi.org/10.1016/j.apenergy.2020.116210.
[2]T.Jirabovornwisut,A.Arpornwichanop,A review on the electrolyte imbalance in vanadium redox flow batteries,Int.J.Hydrog.Energy 44(2019) 24485-24509, http://dx.doi.org/10.1016/j.ijhydene.2019.07.106.
[3]Y. Shi,C.Eze,B.Xiong,W.He,H. Zhang,T.M Lim,A.Ukil,J. Zhao,Recent development of membrane for vanadium redox flow battery applications:A review,Appl. Energy 238 (2019) 202-224,http://dx.doi.org/10.1016/j.apenergy. 2018.12.087.
[4] Z.Guo,J. Sun, Z.Wang,X.Fan,T. Zhao,Numerical modeling of interdigitated flow fields for scaled-up redox flow batteries,Int. Commun.Heat Mass Transfer201 (2023) 123548,http://dx.doi.org/10.1016/j.ijheatmasstransfer.2022. 123548.
[5]J.Sun,H.R.Jiang，B.W.Zhang,C.Y.H.Chao,T.S.Zhao,Towards uniform distributions of reactants via the aligned electrode design for vanadium redox flow batteries,App Energy 259 (2020)114198,http://dx.doi.org/10.1016/j. apenergy.2019.114198.
[6]J.Ren,Y.Li,Z.Wang,J.Sun,Q.Yue,X.Fan,T.Zhao,Thermal issues of vanadium redox flow batteries,Int. Commun.Heat Mass Transfer 2O3 (2023) 123818, http://dx.doi.org/10.1016/j.ijheatmasstransfer.2022.123818.
[7]G.Xiao,G. Yang,S. Zhao,L.Xia,F.Chu,Z. Tan,Battery performance optimization and multi-component transport enhancement of organic flow battery based on channel section reconstruction,Energy 258 (2022）124757,http: //dx.doi.org/10.1016/j.energy.2022.124757.
[8]J. Xionga,M.Jinga,A.Tanga,X.Fana,J. Liua,Ch.Yan,Mechanical modelling and simulation analyses of stress distribution and material failure for vanadium redox flow battery,J.Energy Storage 15 (2018) 133-144,http://dx.doi.org/10. 1016/j.est.2017.11.011.
[9] J. Skrzypek, Plasticity and Creep [In Polish],PWN,Warsaw,1986.
10] N. Soohyun,L.Dongyoung,Ch. Ilbeom,L.D.Gil, Smart cure cycle for reducing the thermal residual stress of a co-cured E-glass/carbon/epoxy composite structure for a vanadium redox flow battery,Compos.Struct. l20 (2015) 107-116, http://dx.doi.org/10.1016/j.compstruct.2014.09.037.
11]W.Cai,R. Zhou, Ch.Wang,Ch. Xie,L. Xiao,On characteristics and research development of coupled fuel cell stack performance and stress,App Energy 388 (2025) 125719, http://dx.doi.org/10.1016/j.apenergy.2025.125719. Stress evolution and creep deformation in solid-oxide electrolysis cell systems - dynamic modeling and multi-objective optimization to maximize stack life and eficiency,J.Power Sources 653 (2025)237687,http://dx.doi.0rg/10.1016/j. jpowsour.2025.237687.
[13] W.D. Badenhorst, L. Sanz,C.Arbizzani,L. Murtomaki, Performance improvements for the all-copper redox flow battery:Membranes，electrodes,and electrolytes,Energy Rep.8 (2022) 8690-8700, http://dx.doi.org/10.1016/j.egyr. 2022.06.075.
[14]L.Cai，W.Li,P.Song,I.Elbugdady,G.Liu,Z.Sun,Creep-fatigue crack growth behavior under mean stress efect in polymer electrolyte membrane: Experimental analysis and numerical crack growth modeling, Eng.Fract. Mech. 314 (2025) 110789, http://dx.doi.org/10.1016/j.engfracmech.2024.110789.
[15]Y.X.Wang,X.Guo,S.W. Shi,G.J.Weng,G.Chen,J.Lu, Biaxial fatigue crack growth in proton exchange membrane of fuel cells based on cyclic cohesive finite element method,Int. J. Mech. Sci.189 (2021) 105946,http://dx.doi.org/ 10.1016/j.ijmecsci.2020.105946.
[16]Q.Lin,Y. Yao,G.Chen,X. Chen,S.Shi, Characterization of biaxial fatigue durability for fuel cell membranes using pressure-loaded blisters,Polym.Test. 125 (2023) 108127, http://dx.doi.org/10.1016/j.polymertesting.2023.108127.
[17]D. Qiua,L.Penga, X.Laia, M. Nic,W.Lehnert, Mechanical failure and mitigation strategies for the membrane in a proton exchange membrane fuel cell Renew. Sustain. Energy Rev.113 (2019) 109289,htp://dx.doi.org/10.1016/j.rser.2019. 109289.
[18] M.Amjadi,A.Fatemi, Creep behavior and modeling of high-density polyethylene (HDPE),Polym.Test.94 (2021）107031，http://dx.doi.org/10.1016/j. polymertesting.2020.107031.
[19]D.Gibhardt, A.E. Krauklis,A. Doblies,A. Gagani, A. Sabalina, Time,temperature and water aging failure envelope of thermoset polymers,Polym.Test.118 (2023) 107901, http://dx.doi.org/10.1016/j.polymertesting.2022.107901.
[20] A.Gonzalez-Espinosa,A.Lozano,M. Montiel,A. Ibanez,Flow visualization in a vanadium redox flow batery electrode using planar laser induced fluorescence, Electrochim.Acta 463 (2023) 142782,http://dx.doi.org/10.1016/j.electacta. 2023.142782.
[21] B.W.Zhang,Y.Lei,B.F.Bai,A. Xu,T.S.Zhao,A two-dimensional mathematical model for vanadium redox flow battery stacks incorporating nonuniform electrolyte distribution in the flow frame,Appl. Therm.Eng.151 (2019) 495-505, http://dx.doi.org/10.1016/j.applthermaleng.2019.02.037.
[22] H.R.Jiang,B.W.Zhang,J.Sun,Z.X.Fan,W.Shyy，T.S.Zhao,A gradient porous electrode with balanced transport properties and active surface areas for vanadium redox flow batteries,J.Power Sources 440 (2019) 227159,http: //dx.doi.0rg/10.1016/j.jpowsour.2019.227159.
[23] J.G.Gong,S.S.Guo,F.H. Gao,T.Y. Niu,F.Z. Xuan, Creep damage and interaction behavior of neighboring notches in components at elevated temperature, Eng. Fract. Mech. 256 (2021) 107996,http://dx.doi.org/10.1016/j.engfracmech.2021. 107996.
[24]K.S.Li,J.Wang,Z.Ch.Fan,S.T.Tu,A life prediction method and damage assessment for creep-fatigue combined with high-low cyclic loading,Int.J. Fatigue 2161 (2022) 106923,http://dx.doi.org/10.1016/j.ijfatigue.2022.106923.
[25] LM. Kachanov， Introduction to Continuum Damage Mechanics， Springer-Science+Business Media B. V, New York,1986.
[26]L.Sun,X. Ch. Zhang,K.S.Li, J.Wang, S.Tokita,Creep-fatigue damage level evaluation based on the relationship between microstructural evolution and mechanical property degradation, Int. J. Plast.181 (2024) 104086,http://dx. doi.org/10.1016/j.ijplas.2024.104086.
[27]H.Li,H.Chen,L. Xu, Q.Wang,Y.Liu,A creep damage model for low cycle fatigue based on the equivalent creep stress:Establishment,verification and application, Eng.Fract. Mech.256 (2021) 107899,http://dx.doi.org/10.1016/j. engfracmech.2021.107899.
[28] A.Loghman,M. Moradi, Creep damage and life assessment of thick-walled spherical reactor using LarsoneMiler parameter, Int. J. Press. Vesels Pip.151 (2017) 11-19, http://dx.doi.org/10.1016/j.ijpvp.2017.02.003.
[29]R.W.Schirmer,S.Roth,M. Abendroth,B. Kiefer,An advanced creep law for large stress and temperature ranges,derived from the Larson-Miller master curve concept,Int.J. Press.Vessels Pip.218 (2025) 105585,http://dx.doi.org/10. 1016/j-jpvp.2025.105585.
[30]K.Maruyamaa,F.Abeb,H. Satoc,J. Shimojod,N. Sekidoa,K. Yoshimia,On the physical basis of a Larson-Miller constant of 2O,Int.J.Press.Vessels Pip.159 (2018) 93-100, http://dx.doi.org/10.1016/j.ijpvp.2017.11.013.
[31]L.Liu,X. Fan,Zh.Chu,J.Yang,Thermo-mechanical loads and creep life assessment for coated turbine blades considering the influence of cooling hole blockage,Eng.Fail.Anal.170 (2025)109321，htp://dx.doi.0rg/10.1016/j. engfailanal.2025.109321.
[32] X.Wang,L.Xu,B.Wu,L. Zhao,Y.Han,Q.Sun,Small punch creep performance of additive manufactured nickel-based GH3536,Int. J.Mech. Sci. 306 (2025) 110850,http://d.doi.org/10.1016/jijmecsci.2025.110850.
[33] A. Bhattarai, N.Wai,R. Schweis,A.Whitehead, G.G.Scherer,P.C.Ghimire,T.M. Lim,H.H. Hng,Vanadium redox flow battery with slotted porous electrodes and automatic rebalancing demonstrated on a 1kW system level,App Energy 236 (2019) 437-443,http://dx.doi.org/10.1016/j.apenergy.2018.12.001.
[34]H. Chen,H.Li,H.Gao,J.Liu, C.Yan,A. Tang,Numerical modelling and in-depth analysis of multi-stack vanadium flow battery module incorporating transport delay,Appl. Energy 247 (2019)13-23,http://dx.doi.org/10.1016/j.apenergy. 2019.04.034.
[35]H.Wang,S.A.Pourmousavi,W.L.Soong,W. Zhang,N. Ertugrul,Battery and energy management system for vanadium redox flow battery:A critical review and recommendations,J.Energy Storage 58 (2023) 106384, http://dx.doi.org/ 10.1016/j.est.2022.106384.
[36]D. Slawifski, S.Bykuc,M. Glifski,P. Chaja,Application of Maxwell-FSI numerical simulation to select the most efficient collector shape in a vanadium redox flow battery,Int.J. Hydrog.Energy 118 (2025) 146-158,http://dx.doi.org/10. 1016/j.ijhydene.2025.02.409.
[37] Z.He,G.Cheng,Y.Jiang,Y.Li, J. Zhu,W.Meng,H. Zhou,L.Dai, L.Wang, Novel 2D porous carbon nanosheet derived from biomass: Ultrahigh porosity and excellent performances toward $\mathrm { V } 2 + / \mathrm { V } 3 +$ redox reaction for vanadium redox flow battery,Int.J.Hydrog.Energy 45 (2020) 3959-3970,http://dx.doi.org/10.1016/ j.ijhydene.2019.12.045.
[38]M.Dieterle,P.Fischer,M.N.Pons,N.Blume,C.Minke,A.Bischi, Life cycle assessment (LCA） for flow batteries:A review of methodological decisions, Sustain.Energy Technol.Assess.53 (2022) 102457,http://dx.doi.org/10.1016/ j.seta.2022.102457.
[39]M.Al-Yasiri, J.Park,A novel cell design of vanadium redox flow batteries for enhancing energy and power performance,App Energy 222 (2018) 530-539, http://dx.doi.org/10.1016/j.apenergy.2018.04.025.
[40] M. Shao,L.Tam,Ch.Wu,A universal creep model for polymers considering void evolution,Compos.Part B 297 (2025) 112280,http://dx.doi.org/10.1016/ j.compositesb.2025.112280.
[41]G.Wypych,Handbook of Polymers,third ed.,Elsevier Inc, London,2O22,http: //dx.doi.0rg/10.1016/C2021-0-00291-1.
[42] D.Slawinski, S.Bykuc,M.Glinski,P.Chaja, Improving the current-voltage characteristics in a vanadium redox flow battery by using bipolar plates with wider channels,J.Energy Storage.129 (2025) 117154,http://dx.doi.org/10. 1016/j.est.2025.117154.