# Effect of membrane diffusion potential on losses in vanadium redox flow batteries

V. Kumar@ \*, M. Pugach@, A. Kasimov

Skolkovo Institute of Science and Technology,Bolshoy Blvd.30,bldg.1,Moscow,121205,Russia

# GRAPHICAL ABSTRACT

![](images/49889e840292a12ed9882bf6f1e91b54d2f00312a7dcd5652bd8b970b5d7a222.jpg)

# HIGHLIGHTS

·Importance of mitigating diffusion potential across membrane is shown.   
·Impact of membrane diffusion potential on voltage efficiency is estimated.   
·Kilowatt class stacks are considered to estimate power loss during charging.

# ARTICLEINFO

# ABSTRACT

Keywords:   
Vanadium redox flow battery   
Membrane potential   
Voltage efficiency

In this work,we numerically investigate losses due to membrane difusion potential as well as ohmic and activation losses in a vanadium redox flow batery(VRFB).A two-dimensional steady-state mathematical model accounting for fluid flow in porous electrodes,electrochemical reactions,species and charge transport is employed and solved using fine adaptive meshes and second-order accurate numerical algorithms.Contributions of

Power loss

the losses to the total cellvoltage are evaluated over arange of operating temperatures and load currents,and the impactof difusion potentialon VRFB voltage eficiency is estimated.Itis found that at high temperatures and low currents,losses due to membrane diffusion potential become comparable to activation loses.The loss in state of charge due to membrane diffusion potential during charging is estimated to range from $2 \%$ to $2 4 \%$ ,depending on target state of charge,operating temperature,and load current.It is also shown that for stacks ranging from 5kW to 2OkW,an excess charging power of $_ { 1 4 \mathrm { ~ W ~ } }$ to $5 8 0 ~ \mathrm { W }$ is required due to membrane diffusion potential,indicating an increasing importance of this phenomenon for large scale stacks.

# 1. Introduction

Energy storage systems are gaining traction in the electricity industryas they aim to increase the dependability and stability of the power grid,reduce variability caused by energy sources that are renewable (such as wind and solar),and provide backup power in areas with poor connectivity or in applications like island grids and remote networks which are off grid [1].Recent years have seen an increased interest in the research and developmentof different types of redox flow batteries. Out of all the types studied,the most successful and widely used is the all vanadium redox flow battery (VRFB).The ability to separate the energy storage component from the energy conversion component allows VRFBs to decouple their energy capacity from power capacity. In comparison to solid electrode batteries,this flexibility in design makes VRFBs more adaptable to different requirements.For large scale energy storage applications,this design flexibility makes VRFBs easier to scale up,safer,and cost-effective.They are also more environmentally friendly in comparison to solid electrode batteries [2].

Previously important aspects have been considered to improve the performance of VRFBs,such as: methods to improve the electrocatalytic activity of the electrodes [3],role of electrode compression [4], design of flow field configuration [5],and modification of the electrode structure [6].To further this goal,multiple eforts in modeling and simulating VRFB over different levels of complexity have been undertaken [7,8]. Studies using zero dimensional models where an indepth analysis of the capacity loss mechanism,including the electrolyte volume transfer,electrolyte imbalance,and electrolyte flow rate,were conducted under different current and flow-rate regimes [9-11]. Since such zero dimensional models are limited by the many simplifications used in the modeling process,a need for simulations with increased sophistication emerges [2].

Toanswer this need,many efforts have been taken to study the VRFB in one,two,and three dimensions [7]. For example,the analysis in [12] utilizing a one-dimensional (1D) model provides a full description of charge and ion transport through the membrane by solving the Poisson equation to describe the Donnan effect between the two layers of interface.Multiple studies have also been done using two-dimensional (2D） models,showcasing the spatial distribution of important parameters such as temperature and species distribution over a range of operating conditions [13,14]. The work [15] also provides insights into mitigating ohmic and concentration overpotentials. In [16],the authors utilized a 2D model to assess the concentration overpotential during charge-discharge cycling at different operating conditions and presented a method to determine the mass transfer coefficient, finally concluding with a strategy proposal to reduce the concentration overpotential.

A number of studies using three-dimensional (3D) simulations have also been performed [17-19].In a recent paper [2O],the authors analyzed the dependence of electrolyte imbalance on different proton and vanadium concentrations in the battery half-cells,revealing a potential way to mitigate this imbalance.At times it is beneficial to model only certain aspects of VRFB using 2D or 3D models, and the rest using lower dimensions so as to reduce computational cost.Such a hybrid model was developed in [2l],in which the authors combined a two-dimensional analytical solution for the active species,a one-dimensional analytical model for cross-over mechanisms, and a zero-dimensional numerical model for outlet concentrations of reactants.

Some of the many reasons that affect efficiency of VRFB operation are:the cell over-potentials,shunt currents,vanadium species crossover,precipitation of vanadium,and hydraulic pressure drops in the stack [22].To the best of our knowledge,there is currently no systematic parametric evaluation of the contribution by the components of membrane potential (e.g.,the Donnan potential and membrane diffusion potential),on VRFB efficiency.

One of the costliest components of the VRFB is the membrane. An ideal membrane for the VRFB is expected to have high ionic conductivity,to be chemically and thermally stable,highly selective to particular ions,to be able to minimize water uptake,and at the same time have a low cost [23].Currently,the most popular choice for ion exchange membranes is the perfluorinated polymeric ion exchange (Nafion) membrane.Although they provide high stability in acidic electrolytes and have a high ionic conductivity [24,25],their high cost and the presence of crossover of active species across these membranes [26,27] are reasons for searching for alternatives.

Within the ion exchange membrane (and the regions it separates) we have movement of ions.We understand that the combination of convective,diffusive,and migratory fluxes would result in changes in distribution of species concentrations,including in the membraneelectrode interface region.The non-uniform species distribution that develops near the membrane results in concentration gradients across it,promoting diffusion of species (as the diffusive flux dominates over migration in the membrane [28]).As different ionic species have different mobilities,the faster ions diffuse ahead of the slower ones. This causes a separation of charges,resulting in a potential difference called the diffusion potential of the membrane,or liquid junction potential [29].Along with this,due to the selective permeability of the membrane,at equilibrium,a non uniform fixed distribution of certain ions occurs on either side of the membrane-electrode interface, which once again results in a potential difference (at each interface), called the Donnan potential [3O].It is worth noting that multiple works based on numerical simulations were found capturing the Donnan potential[12,20,28,31,32],but none extract and analyze the membrane diffusion potential. In this work,we focus on the impact of membrane diffusion potential on loss in total cell voltage and voltage efficiency of the VRFB.

We employ a two-dimensional (2D) model which describes fluid flow,species transport,and charge transport in a VRFB.The model is utilized to study the effects of load current, operating temperature, and initial vanadium-ion concentration (state of charge, SOC) on: (1) the changes in membrane diffusion potential; (2) the losses associated with chemical kinetics (activation overpotential)；and (3) the ohmic overpotential. These losses are compared to one another based on their contribution to cell voltage losses with a focus on the role of diffusion potential in loss in state of charge and voltage efficiency of the cell.We additionally consider examples of stack ranging from $5 ~ \mathrm { k W }$ to $2 0 ~ \mathrm { k W }$ and estimate the impact of diffusion potential on the power loss.

The obtained results are important for determination of optimal operating conditions and development of reliable and eficient VRFB systems.The study also showcases the importance of membrane diffusion potential in comparison to the activation and ohmic losses.In this regard, the present study brings to light an unaccounted cause for loss in VRFB efficiency.

![](images/1a3af2c7942c1128aa6c460a13ab75126f75684595eba99d1bc767586a1c2919.jpg)  
Figcheofls coletorsll methods.

The remainder of the paper is organized as follows. In Section 2, we describe the governing equations (which includes description of the reactions,model for fluid flow,species transport,reaction kinetics,and charge transport),boundary conditions,and simulation procedure.In Section 3,we perform a parametric study using operating temperature, current load,and initial vanadium ion concentration (state of charge) as parameters and analyze the activation loss,ohmic loss,and loss due to diffusion potential.In Section 4,we go over our main findings and give some final remarks.

# 2.VRFB working principle and model description

In this section,we described briefly the main working principle of VRFB and introduce the mathematical model that is subsequently used to analyze the battery properties.

A VRFB primarily consists of two main components: the cell stacks which are responsible for converting chemical energy into electricity through a reversible process,and the electrolyte tanks where energy is stored.Each cell is comprised of two porous electrodes separated by an ion-exchange membrane, current collectors,and electrolyte storage tanks as illustrated in Fig. 1. In our work, we model the VRFB operating in“flow-through”configuration.As opposed to the“flow-by”design, where the electrolyte flows over the porous electrode and seeps in perpendicular to the direction of flow,in the“flow-through”design, the liquid electrolyte is pumped along the intended direction of seepage.These electrodes act as reaction cites for the electrolytes flowing through it and play the role of capturing electrons and conducting current during charging and discharging. Separating the two electrodes is an ion selective membrane which allows the passage of particular type of ion; in our study,we model a cation-exchange membrane. The bipolar plates adjacent to the two ends of the electrode (near the current collector) physically separate adjacent cells in series and provide conduction between them.In case of “flow-by”cells,the bipolar plates additionally contain flow fields meant for distributing electrolyte across the electrode surface.Finally,we have the current collectors which facilitate the flow of electrons between the porous electrode and the external circuit.In a VRFB,the positive electrolyte tank stores $\mathrm { V O } ^ { 2 + } / \mathrm { V O } _ { 2 } ^ { + }$ ,while the negative electrolyte tank stores $\mathrm { V } ^ { 2 + } / \mathrm { V } ^ { 3 + }$

# 2.1. Governing equations

The full system of governing equations that we use in this study consists of the equations of electrochemical kinetics,of fluid flow in a porous medium, of species transport,and of electric potential. The equations are supplied with appropriate boundary conditions.We investigate only steady state solutions and therefore no initial conditions are required.While it is true that dynamic models can additionally describe transient behavior and hence cover a wider range of phenomena,our focus in this study is on steady state regimes with the goal of estimating relative contributions to net voltage loss.The results obtained represent practical long duration charge-discharge regimes, where variations over time are negligible.

# 2.1.1.Electrochemical reactions

During battery operation,redox reactions take place in each half cell resulting in changes in the oxidation states of the vanadium ions accompanied with transfer of electrons mediated by an external circuit. The resulting reactions are as follows:

$$
\begin{array} { r l } & { \mathrm { V O } _ { 2 } ^ { + } + 2 \mathrm { H } ^ { + } + \mathrm { e } ^ { - } \frac { \mathrm { d i s c h a r g e } } { \mathrm { c h a r g e } } \mathrm { V O } ^ { 2 + } + \mathrm { H } _ { 2 } \mathrm { O } , E _ { 0 + } = 1 . 0 0 4 \mathrm { \ V } , } \\ & { \mathrm { V } ^ { 2 + } \frac { \mathrm { d i s c h a r g e } } { \mathrm { c h a r g e } } \mathrm { V } ^ { 3 + } + \mathrm { e } ^ { - } , E _ { 0 - } = - 0 . 2 5 5 \mathrm { \ V } , } \\ & { \mathrm { V } ^ { 2 + } + \mathrm { V O } _ { 2 } ^ { + } + 2 \mathrm { H } ^ { + } \frac { \mathrm { d i s c h a r g e } } { \mathrm { c h a r g e } } \mathrm { V O } ^ { 2 + } + \mathrm { V } ^ { 3 + } + \mathrm { H } _ { 2 } \mathrm { O } , E _ { 0 } = 1 . 2 5 9 \mathrm { \ V } . } \end{array}
$$

Here,we have the reactions at positive electrode (la),negative electrode (1b),and overall reaction (lc).

In addition, the two steps of dissociation of sulfuric acid are given by

$$
\begin{array} { r l } { { \mathrm { H } _ { 2 } S \mathrm { O } _ { 4 } \longrightarrow \mathrm { H S O } _ { 4 } ^ { - } + \mathrm { H } ^ { + } , } } & { { } } \\ { { \mathrm { H S O } _ { 4 } ^ { - } \longrightarrow \mathrm { S O } _ { 4 } ^ { 2 - } + \mathrm { H } ^ { + } . } } & { { } } \end{array}
$$

# 2.1.2.Electrolyte fluid flow

The flow of electrolyte in the porous electrode is described here by the steady state equations of fluid mechanics assuming incompressible viscous flow.The flow rates involved in the study are relatively low, hence pressure and viscous forces dominate.The effect of the presence of the porous media is modeled by adding a sink term in the momentum equation that is proportional to the bulk fluid velocity.

The equation of continuity for an incompressible fluid and of momentum are,respectively:

$$
\begin{array} { r l } & { \nabla \cdot \mathbf { u } = 0 , } \\ & { \rho ( \mathbf { u } \cdot \nabla ) \mathbf { u } = - \nabla p + \mu \nabla ^ { 2 } \mathbf { u } - \frac { \mu } { K } \mathbf { u } . } \end{array}
$$

Here, $\mathbf { u }$ is the velocity vector, $\rho$ is the electrolyte density, $\mu$ isits dynamic viscosity, and $\nabla p$ is the pressure gradient. The last term in Eq.

Table 1 Model parameters used in the present simulations.   

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Length of electrode,Le,cm</td><td>4</td></tr><tr><td>Thickness of electrode,L,,mm</td><td>4</td></tr><tr><td>Membrane thickness,Lf,m,mm</td><td>0.15</td></tr><tr><td>Specific surface area, a,m-1</td><td>1.62·104[31]</td></tr><tr><td>Reference temperature, Tref,K</td><td>298.15 [13]</td></tr><tr><td>Electrolyte density,p,kg/m</td><td>1300 [28]</td></tr><tr><td>Dynamic viscosity of electrolyte,μ, Pa s Cathodic charge transfer coeficient (positive electrode),α+,c</td><td>0.004[13]</td></tr><tr><td>Anodic charge transfer coeficient (positive electrode),𝛼+,a</td><td>0.5[13] 0.5[13]</td></tr><tr><td>Cathodic charge transfer coefficient (negative electrode), α_,c</td><td>0.5[13]</td></tr><tr><td>Anodic charge transfer coefficient (positive electrode),α-,a</td><td>0.5[13]</td></tr><tr><td>Electrode conductivity,os,S/m</td><td>200[13]</td></tr><tr><td>Current collector conductivity,σc,S/m</td><td>1000 [28]</td></tr><tr><td>Current collector thickness,Lc,m</td><td>0.01[28]</td></tr><tr><td>Reference concentration,Cref,mol/m</td><td>1000 [28]</td></tr><tr><td>Standard rate constant,positive electrode,k,,m/s</td><td>6.8·10-7[13]</td></tr><tr><td>Standard rate constant, negative electrode,k_,m/s</td><td>1.7 ·10-7 [13]</td></tr><tr><td>Diffusion coefficient (vO+),m²/s</td><td>3.9·10-9 [28]</td></tr><tr><td>Difusioncoefficient (vO²+),m²/s</td><td>3.9·10-9 [28]</td></tr><tr><td>Diffusion coefficient (V²+),m²/s</td><td>2.4·10-9[28]</td></tr><tr><td>Diffusion coefficient (V3+),m²/s</td><td>2.4·10-[28]</td></tr><tr><td>Diffusion coefficient (H+),m²/s</td><td>9.312·10-10 [28]</td></tr><tr><td>Diffusion coefficient (HsO4),m²/s</td><td>1.33·10-10 [28]</td></tr><tr><td>Diffusion coefficient (SO²-),m²/s</td><td>1.065·10-10 [28]</td></tr><tr><td>Difusion coeficient in membrane (VO²),m²/s</td><td>2.403·10-12 [28]</td></tr><tr><td>Diffusion coefficient in membrane (VO²+),m²/s</td><td>4.445·10-12 [28]</td></tr><tr><td>Difusion coeficient in membrane (V²+),m²/s</td><td>9.435·10-12[28]</td></tr><tr><td>Diffusion coefficient in membrane (v3+),m²/s</td><td>1.445·10-11 [28]</td></tr><tr><td>Diffusion coefficient in membrane (H+),m²/s</td><td>3.5·10-10 [28]</td></tr><tr><td>Dissociation coefficient,kd,mol/(ms)</td><td>104[28]</td></tr><tr><td>Degree of dissociation,β</td><td>0.25[28]</td></tr><tr><td>porosity of electrode,e</td><td>0.9</td></tr></table>

(4) comes from the Darcy law and has been added as a sink to the momentum equation to model the flow resistance produced by the porous medium.The factor $K$ is the permeability of the electrode material,which depends in particular on the porosity $\epsilon$ of the electrode.

# 2.1.3.Species transport

Spatial distributions of all the individual species involved in the chemical reactions are calculated by solving the following transport equations,

$$
\nabla \cdot \mathbf { f } _ { i } = s _ { i } ,
$$

in which the flux $\mathbf { f } _ { i }$ of species $i$ is defined as the sum of fluxes due to convection,migration in the electric field,and diffusion [28]:

$$
\mathbf { f } _ { i } = c _ { i } \mathbf { u } - F \frac { D _ { i } ^ { e f f } } { R T } z _ { i } c _ { i } \nabla \phi _ { e } - D _ { i } ^ { e f f } \nabla c _ { i } .
$$

In these equations, $c _ { i }$ is the bulk concentration of species $i$ ,where $i = 5$ corresponds to $\nabla { \mathsf { O } } _ { 2 } ^ { + }$ ， $i = 4$ to $\scriptstyle \mathrm { V O } ^ { 2 + }$ ， $i = 3$ to $\mathsf { V } ^ { 3 + }$ ， $i = 2$ to $\mathrm { V } ^ { 2 + }$ . Note that the index $i$ is chosen to correspond to the oxidation number of the vanadium ion. Concentrations of $\mathrm { H } ^ { + }$ and $\mathrm { H S O } _ { 4 } ^ { - }$ are denoted as $c _ { \mathrm { H } ^ { + } }$ and $c _ { \mathrm { H S O _ { 4 } ^ { - } } }$ . The symbols $F$ and $R$ are the Faraday constant and universal gas constant, respectively. The effective mass diffusivity $D _ { i } ^ { e f f }$ of species $i$ is defined as

$$
\begin{array} { r } { D _ { i } ^ { e f f } = \epsilon ^ { 3 / 2 } D _ { i } , } \end{array}
$$

where $D _ { i }$ is the binary diffusion coefficient of species $i$ in the bulk fluid, which is a mixture of sulfuric acid and water. Further, $T$ is temperature, $z _ { i }$ is the charge number of species i, $\phi _ { e }$ is the electrolyte potential,and $s _ { i }$ is the source term for species $i$ due to chemical reactions.The term $s _ { i }$ depends on the kinetic mechanism and the reactions that create or consume species $i$ Expressions for $s _ { i }$ are shown in Table 2.

Following [28,31],we model the source term associated only with the second step (2b) of dissociation of sulfuric acid,

$$
s _ { d } = k _ { d } \left( \frac { c _ { H ^ { + } } - c _ { H S O _ { 4 } ^ { - } } } { c _ { H ^ { + } } + c _ { H S O _ { 4 } ^ { - } } } - \beta \right) ,
$$

Table 2 Source terms $s _ { i }$ at positive and negative electrodes. Quantities $s _ { d }$ and $j _ { \pm }$ are given in (7) and (13)-(14),respectively.   

<table><tr><td>i</td><td>Species</td><td>s𝑖,positive electrode</td><td>s, negative electrode</td></tr><tr><td>2</td><td>V²+</td><td>0</td><td>小</td></tr><tr><td>3</td><td>V3+</td><td>0</td><td></td></tr><tr><td>4</td><td>VO2+</td><td>1</td><td>0</td></tr><tr><td>5</td><td>vo</td><td>一</td><td>0</td></tr><tr><td>H+</td><td>H+</td><td>-2 1Sd</td><td>-sd</td></tr><tr><td>HSO4</td><td>HSO4</td><td>Sd</td><td>Sd</td></tr></table>

where $k _ { d }$ is the dissociation constant,and $\beta$ is the degree of dissociation.Note that it is widely considered that the first step (2a) is complete [2O],in the sense that all of $\mathrm { H } _ { 2 } S 0 _ { 4 }$ exists as $\mathrm { H S O } _ { 4 } ^ { - }$ and $\mathrm { H } ^ { + }$ ions, so we do not have to solve for the $\mathrm { H } _ { 2 } S 0 _ { 4 }$ species.

# 2.1.4. Electric potential

The charge conservation equation ensures that the current generated by redox reactions in the electrolyte is balanced by the current coming in or leaving the electrode.It balances the liquid phase and solid phase current densities (per unit area; $\mathbf { i } _ { e }$ and $\mathbf { i } _ { s }$ ，respectively) through the following expression [31]:

$$
\nabla \cdot \mathbf { i } _ { e } = - \nabla \cdot \mathbf { i } _ { s } = - j ,
$$

where $j$ is the volumetric current density (per unit volume) due to the electrochemical reactions.

The solid phase current density is found from Ohm's law,

$$
\mathbf { i } _ { s } = - \sigma _ { s } \nabla \phi _ { s } ,
$$

where $\sigma _ { s }$ is the conductivity of the solid material, and $\phi _ { s }$ is the potential in the solid phase.

The electrolyte current density depends on the flux of the ions as follows:

$$
\mathbf { i } _ { e } = F \sum z _ { i } \mathbf { f } _ { i } .
$$

Substituting (5b) into this equation and applying the electro-neutrality condition $( \sum z _ { i } c _ { i } = 0 )$ ,we obtain

$$
\mathbf { i } _ { e } = - \sigma _ { e } \nabla \phi _ { e } - F \sum _ { i } z _ { i } D _ { i } ^ { e f f } \nabla c _ { i } ,
$$

in which we introduce $\sigma _ { e }$ as the electrolyte conductivity,

$$
\sigma _ { e } = \frac { F ^ { 2 } } { R T } \sum _ { i } z _ { i } ^ { 2 } D _ { i } ^ { e f f } c _ { i } .
$$

The volumetric current density $( j _ { + }$ in positive and $j _ { - }$ in negative electrodes） is computed using the Butler-Volmer equation [13,28] as follows:

$$
j _ { + } = j _ { + , 0 } \left[ \frac { c _ { 5 } ^ { s } } { c _ { 5 } } \cdot \exp \left( \frac { - \alpha _ { + , c } F \eta _ { + } } { R T } \right) - \frac { c _ { 4 } ^ { s } } { c _ { 4 } } \cdot \exp \left( \frac { \alpha _ { + , a } F \eta _ { + } } { R T } \right) \right]
$$

and

$$
j _ { - } = j _ { - , 0 } \left[ \frac { c _ { 3 } ^ { s } } { c _ { 3 } } \cdot \exp \left( \frac { - \alpha _ { - , c } F \eta _ { - } } { R T } \right) - \frac { c _ { 2 } ^ { s } } { c _ { 2 } } \cdot \exp \left( \frac { \alpha _ { - , a } F \eta _ { - } } { R T } \right) \right] .
$$

Here, $c _ { 5 } ^ { s } / c _ { 5 }$ is the surface/bulk concentration of $\nabla { \mathsf { O } } _ { 2 } ^ { + }$ ， $c _ { 4 } ^ { s } / c _ { 4 }$ is surface/bulk concentration of $\scriptstyle \mathrm { V O } ^ { 2 + }$ ,and $j _ { + , 0 }$ is the volumetric exchange current density in positive electrode,defined as

$$
j _ { + , 0 } = a F k _ { + } ^ { T } \left( c _ { 4 } \right) ^ { \alpha _ { + , c } } \left( c _ { 5 } \right) ^ { \alpha _ { + , a } } .
$$

Similarly,for the negative electrode, $c _ { 2 } ^ { s } / c _ { 2 }$ is the surface/bulk concentration of $\mathrm { V } ^ { 2 + }$ ， $c _ { 3 } ^ { s } / c _ { 3 }$ is surface/bulk concentration of $\mathsf { V } ^ { 3 + }$ ，and $j _ { - , 0 }$ is the volumetric exchange current density in negative electrode,defined as

$$
j _ { - , 0 } = a F k _ { - } ^ { T } \left( c _ { 2 } \right) ^ { \alpha _ { - , c } } \left( c _ { 3 } \right) ^ { \alpha _ { - , a } } .
$$

All parameters appearing here in Eqs. (l3)-(l6) and others further below are defined in Table 1.

The rate constants in Eqs.(l5)and (l6) are temperature dependent and are given by [13]

$$
k _ { \pm } ^ { T } = k _ { \pm } \exp \left[ \frac { n F E _ { \pm } } { R } \left( \frac { 1 } { T _ { r e f } } - \frac { 1 } { T } \right) \right] ,
$$

where $n$ is the number of electrons participating in the reaction (one in our case).The overpotentials in the Butler-Volmer equation are defined as

$$
\eta _ { \pm } = \phi _ { s } - \phi _ { e } - E _ { \pm } .
$$

The equilibrium potentials $E _ { \pm }$ in (18) are defined using the Nernst equation as

$$
\begin{array} { r l } & { E _ { + } = E _ { 0 + } ^ { T } + \frac { R T } { F } \ln \left( \frac { c _ { 5 } } { c _ { 4 } } \cdot \left( \frac { c _ { H ^ { + } } } { c _ { r e f } } \right) ^ { 2 } \right) , } \\ & { E _ { - } = E _ { 0 - } ^ { T } + \frac { R T } { F } \ln \left( \frac { c _ { 3 } } { c _ { 2 } } \right) . } \end{array}
$$

The temperature dependent formal potential can be estimated using the following expressions [13]:

$$
\begin{array} { l } { { E _ { 0 + } ^ { T } = E _ { 0 + } - ( 9 \cdot 1 0 ^ { - 3 } \cdot ( T - T _ { r e f } ) ) , } } \\ { { \ } } \\ { { E _ { 0 - } ^ { T } = E _ { 0 - } + ( 1 . 5 \cdot 1 0 ^ { - 3 } \cdot ( T - T _ { r e f } ) ) , } } \end{array}
$$

where the terms $E _ { 0 + }$ and $E _ { 0 - }$ are the formal potentials given in Eqs. (la) and (1b).

The flux of species between the bulk electrolyte and surface of electrode is balanced by the flux generated due to the chemical reactions consuming or creating species.Using the following expressions we can determine the surface concentration $c _ { i } ^ { s }$ of species $i$ [31]:

$$
a k _ { m } \left( c _ { 5 } ^ { s } - c _ { 5 } \right) = - \frac { j _ { + } } { F } ,
$$

$$
\begin{array} { l } { \displaystyle { a k _ { m } \left( c _ { 4 } ^ { s } - c _ { 4 } \right) = \frac { j _ { + } } { F } } , } \\ { \displaystyle { a k _ { m } \left( c _ { 2 } ^ { s } - c _ { 2 } \right) = \frac { j _ { - } } { F } } , } \\ { \displaystyle { a k _ { m } \left( c _ { 3 } ^ { s } - c _ { 3 } \right) = - \frac { j _ { - } } { F } } . } \end{array}
$$

Here $a$ is the specific (per unit volume) surface area of the electrode, and $k _ { m }$ is the mass transfer coeficient of the electrode.

# 2.1.5.Transport across membrane

The fluid within the membrane is assumed to be stationary,hence the flux of ions within the membrane arises only due to the force of electric field and diffusion.Effects of osmotic pressure and electroosmotic forces can be neglected (as shown in [28,33]).

The electroneutrality condition in the membrane is given by

$$
\sum _ { i } z _ { i } c _ { i } + z _ { f } c _ { f } = 0 ,
$$

where $z _ { f }$ is the fixed charge number,and $c _ { f }$ is the concentration of fixed charge in the membrane.

We consider that only $H ^ { + }$ ions can pass through the membrane,and their flux is given by [34]:

$$
{ \bf f } _ { H ^ { + } , m } = - F \frac { D _ { H ^ { + } } } { R T } z _ { H ^ { + } } c _ { H ^ { + } } \nabla \phi _ { e , m } - D _ { H ^ { + } } \nabla c _ { H ^ { + } } .
$$

As there are no reactions taking place within the membrane,the equation for electrolyte potential in the membrane becomes

$$
\nabla \cdot \mathbf { i } _ { e , m } = 0 ,
$$

where $\mathbf { i } _ { e , m }$ is the electrolyte current in the membrane. Substituting (11) into (26),we obtain

$$
\nabla \cdot \left( - \sigma _ { e , m } \nabla \phi _ { e , m } - z _ { H ^ { + } } D _ { H ^ { + } } F \nabla c _ { H ^ { + } } \right) = 0 ,
$$

where

$$
\sigma _ { e , m } = \frac { F ^ { 2 } } { R T } z _ { H ^ { + } } ^ { 2 } D _ { H ^ { + } } c _ { H ^ { + } }
$$

is the conductivity of electrolyte,and $\phi _ { e , m }$ is the electrolyte potential in the membrane.

# 2.1.6.Diffusion potential in membrane

Owing to the non-uniform species distribution on either side of the membrane (caused by the interplay of components of the flux given in Eq.(5b)),a concentration gradient is formed promoting diffusion of species.As the participating ions have diferent ionic mobilities, a charge separation and electric potential difference - known as the diffusion potential or liquid junction potential-is created.

Additionally,at the membrane-electrode interface,there is an electrochemical equilibrium enforced for each ion capable of passing through.Due to the membrane's charge,the co-ions are excluded, leading to a discontinuous jump in potential at the interface know as the Donnan potential, whereas the diffusion potential has a continuous change.The difference between the two is shown in Fig.2.

In our VRFB system,we can see that the two electrodes which are separated by an ion-selective membrane consist of electrolytes with ions of different mobilities,hence such an additional potential difference (diffusion potential） is expected to occur in our system as well.The ideal cation-exchange membrane utilized in VRFBs is expected to exclusivelyallow the passage of $\mathrm { H } ^ { + }$ ions between electrodes through the membrane.But the reality is that any positive ion can pass through.Hence our model does not capture the diffusion potential due to each ion (our model only calculates $\mathrm { H } ^ { + }$ ion flux in all domains). This difusion potential across membrane can be accounted for by solving the Poisson-Nernst-Planck equations ((27) and (5b)),after which one needs to separate out the part of the electrolyte potential caused by unequal ion mobilities. This method is not only computationally expensive,but also cumbersome to extract the diffusion potential across the membrane.Alternative to this,we utilize the species concentrations obtained through our simulation at the membrane-electrode interface, and use them as an input for calculating the membrane diffusion potential post-hoc using the Henderson equation [29].This allows us to easily isolate the component of the membrane potential due to unequal mobilities and is computationally cheaper as compared to solving the whole set of equations within the membrane domain for all species.The validity of the Henderson equation for ion-selective membrane has also been shown previously by comparing its prediction with that obtained by solving the Poisson-Nernst-Planck equation [35].

![](images/9a80d16f70b2d23893cd57cf49dadb2fe025892252834f72a8694bf498a6d5ee.jpg)  
Fig.2.Graphical description contrasting electrolyte potential predicted by our model,electrolyte potential when accounting for flux of all cations moving in the membrane,and when accounting for Donnan potential as well.Here, the positive electrode is fixed as a reference electrode (constant potential), $\phi _ { e , m }$ is the membrane potential when only the flux of $\mathrm { H } ^ { + }$ ions is considered (shown in Eq.(27)), $\phi _ { d i f f }$ is the potential due to unequal mobility of all cations passing through,and $E _ { D }$ is the Donnan potential.We can observe a jump in the potential at the interface due to the Donnan effect,whereas transition across interface for diffusion potential is continuous.

Based on the Henderson equation [29],the equation for the membrane diffusion potential is given by

$$
E _ { j } = \frac { \boldsymbol { \Sigma } _ { i } \frac { | z _ { i } | \boldsymbol { v } _ { i } } { z _ { i } } \left[ c _ { i } | _ { \lambda _ { 1 } } - c _ { i } | _ { \lambda _ { 2 } } \right] } { \boldsymbol { \Sigma } _ { i } | z _ { i } | \boldsymbol { v } _ { i } \left[ c _ { i } | _ { \lambda _ { 1 } } - c _ { i } | _ { \lambda _ { 2 } } \right] } \cdot \frac { R T } { F } \ln \left( \frac { \boldsymbol { \Sigma } _ { i } | z _ { i } | \boldsymbol { v } _ { i } \left[ c _ { i } | _ { \lambda _ { 2 } } \right] } { \boldsymbol { \Sigma } _ { i } | z _ { i } | \boldsymbol { v } _ { i } \left[ c _ { i } | _ { \lambda _ { 1 } } \right] } \right) ,
$$

where $c _ { i } | _ { \lambda _ { 1 } }$ and $c _ { i } | _ { \lambda _ { 2 } }$ mean the concentration of species $i$ in region $\lambda _ { 1 }$ and $\lambda _ { 2 }$ ,respectively.The regions $\lambda _ { 1 }$ and $\lambda _ { 2 }$ correspond to the positive and negative electrode-membrane interface,respectively (during discharge),and vice versa during charge.In the equation above, $v _ { i }$ is the mobility of species $i$ ，

$$
v _ { i } = \frac { D _ { i } ^ { m , e f f } } { R T } .
$$

Here, $D _ { i } ^ { m , e f f }$ is the effective diffusivity of ions in the membrane (described in Eq.(6)). The values for diffusivity of ions in membrane are taken from [28]. Now,the new cell voltage $E _ { c e l l } ^ { \prime }$ can be obtained from

$$
E _ { c e l l } ^ { \prime } = E _ { c e l l } + E _ { j } ,
$$

where $E _ { c e l l }$ is the total cell voltage consisting of the overpotentials.

As the membrane is cation-selective,it permits only positively charged ions to cross.For this reason, we exclude $\mathrm { H S O _ { 4 } ^ { - } }$ and $\bar { \mathsf { S O } } _ { 4 } ^ { 2 - }$ from the calculation as they are effectively immobile across the junction, so they do not contribute to the diffusion potential.

# 2.2.Boundary conditions

From our set of governing Eqs. (3)-(5) and (8),we need to solve foru $, p , c _ { i } , \phi _ { s }$ ,and $\phi _ { e }$ ,and hence require boundary conditions for each of these variables at the faces labeled in Fig.1.Regarding velocity of fluid, we have no-slip condition $\mathbf { u } _ { w a l l } = 0$ at the current collectors (1) and (4)and the membrane electrode interfaces (7) and (8).As we solve using“velocity inlet- pressure outlet"setup,at the inlets (5) and (6) we have velocity corresponding to the input flow rate $Q _ { i n }$ ,and at outlets (2) and (3) we set the pressure equal to zero (relative to atmospheric pressure):

$$
\begin{array} { c } { { - \mathbf { u } _ { i n } \cdot \mathbf { n } A = Q _ { i n } , } } \\ { { { } } } \\ { { p _ { o u t } = 0 , } } \end{array}
$$

where $\mathbf { n }$ is the unit outward normal to the inlet boundary,and $A$ is the area of the inlet.

For the species, we have inlet species corresponding to the state of charge soc:

$$
\begin{array} { l } { { c _ { 5 } ^ { i n } = c _ { + } ^ { 0 } \cdot s o c , } } \\ { { c _ { 4 } ^ { i n } = c _ { + } ^ { 0 } \cdot ( 1 - s o c ) , } } \\ { { c _ { 2 } ^ { i n } = c _ { - } ^ { 0 } \cdot s o c , } } \\ { { c _ { 3 } ^ { i n } = c _ { - } ^ { 0 } \cdot ( 1 - s o c ) , } } \end{array}
$$

while at the outlet, we have zero diffusive flux,

$$
D _ { i } ^ { e f f } \nabla c _ { i } \cdot \mathbf { n } = 0 .
$$

This latter condition implies that the outflow of species occurs only with the bulk flow of the fluid,and that the species concentrations are nearly uniform at the outlet boundary.

We assume that there is no crossover of species through the membrane other than that of hydrogen ion.Hence,we state that the flux of species is zero for all species,except for hydrogen ion,for which we have a continuous flux condition.

Regarding the potential in the solid phase during discharge,at positive current collector (1) we have

$$
- \sigma _ { s } \nabla \phi _ { s } \cdot \mathbf { n } = - I ,
$$

and at the negative current collector (4) we have

$$
- \sigma _ { s } \nabla \phi _ { s } \cdot \mathbf { n } = I .
$$

During charge,the signs are reversed for the operating current density $I$ .At the membrane-electrode interfaces (7) and (8),we state that the current is continuous,while implementing an extremely low conductivity for solid phase in membrane, $1 0 ^ { - 1 8 } \ S / m$

As all other faces are assumed to be insulated,we state that the flux of potential is zero (i.e.,the solid phase current is zero),

$$
- \sigma _ { s } \nabla \phi _ { s } \cdot \mathbf { n } = 0 .
$$

Similarly,we have continuous flux condition for the electrolyte potential across the electrode-membrane interfaces (7) and (8).At all other faces we have the insulation boundary condition,

$$
- \sigma _ { e } \nabla \phi _ { e } \cdot \mathbf { n } = 0 .
$$

# 2.3. Simulation procedure

The governing Eqs. (3)-(5),(8),and the electrochemical reaction kinetics model, Eqs.(l3) and (14),are solved numerically using the commercial computational fluid dynamics (CFD) software Ansys Fluent 19.2 [36]. The solution methodology utilizes the Semi-Implicit Method for Pressure Linked Equations (SIMPLE) algorithm along with the algebraic multigrid (AMG) method [37,38]. Since the software does not have built-in capabilities for solving our system,custom User-Defined Functions (UDFs) and User-Defined Scalars (UDSs) are incorporated to specify source terms,material transport properties,reaction kinetics as well as equations governing species transport and the equations for potential.Numerical convergence analysis as well as model validation have been performed to make sure the simulations accurately represent the phenomena under study.

In Fig. 3(a),we show a zoom into the computational domain.At the center of the zoomed region we have the mesh for the membrane,and on its either side we have the mesh for the electrode which gradually reduces in size as it approaches the mesh used for the membrane.We use 768,ooo quadrilateral cells in the positive and negative electrode domains each,and 168,ooO quadrilateral cells in the membrane region. The time required for a single simulation is approximately $2 0 \ \mathrm { m i n }$ on a workstation with a dual processor Intel Xeon E5-236O v4 CPU consisting of 20 cores and 128 GB RAM.

# 3.Results and discussion

# 3.1.Model validation

The model was validated, in part,using experimental data reported in [34].The simulation's voltage response over a range of states of charge is evaluated against the experimental measurements obtained from the mentioned reference,as shown in Fig.3(b).We replicate the same conditions as in [34],with active species composition of 1500 $\mathrm { m o l } / \mathrm { m } ^ { 3 }$ in both positive and negative electrodes.The other parameters used during validation,such as porosity,permeability,initial proton concentration, fixed charge concentration,membrane thickness etc., are also the same in our work and the reference work.The data correspond to an applied current density of $8 0 ~ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ with an inlet flow rate of $6 0 ~ \mathrm { m l / m i n }$ .Additional validation is performed based on polarization curve from [39].Compared to the previous validation on data from [34],in this case the flow rate is at a lower value of $1 5 \ \mathrm { m l / m i n }$ 、The data used from [39] corresponds to the Nafion 115 membrane. The cell voltage is now evaluated over a large range of applied currents up to $1 2 0 0 ~ \mathrm { m A } / \mathrm { c m } ^ { 2 }$

From the two validation tests,a strong agreement between experiments and present simulations is found for the cel's output response overa range of states of charge,applied currents,and flow rates.In Figs.3(b) and 3(c) we can see that the numerical and experimental results demonstrate a high degree of correlation,exhibiting both a similar trend and close numerical agreement.The largest discrepancy is observed towards the end of charge and discharge cycles.Despite this difference,the average error between the numerical predictions and experimental measurements is below $2 \%$ .In addition to the validation, a numerical mesh independence study was carried out to establish the accuracy of the numerical scheme and determine an optimal mesh element size.We observed a second order convergence with mesh refinement for fluid velocity,electrolyte potential,and solid potential.

# 3.2.Distribution of species concentration

In this section,we present the spatial distribution of vanadium species concentration for the case of $^ { 1 5 \% }$ SOC discharge (corresponding to electrolyte composition of $1 0 4 0 \mathrm { \ m o l } / \mathrm { m } ^ { 3 }$ vanadium [28]),at an applied current density of $4 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ,and inlet flow rate of $1 0 \mathrm { m l / m i n }$

The 2D contour plots of species concentration are presented in Fig. 4.We see a non-uniform distribution,underscoring the importance of simulations in two dimensions.Furthermore,the interplay of the fluxes described in Eq.(5b) results in spikes in the species concentration at the interface.To observe this better,in Figs.4(c) and 4(d) we plot the species distribution on a line perpendicular to the flow direction at $^ { 1 \mathrm { c m } }$ from the inlet.

# 3.3.Analysis of diffusion potential in membrane

In this section,we analyze the membrane diffusion potential. For this purpose,we take the area weighted average across the electrodemembrane interface for the species concentration and use it as an input for Eq.(29).The flow rate is fixed at $6 0 \mathrm { m l / m i n }$ for all results presented henceforth.

First,we study the effect of initial vanadium concentration (state of charge) on the diffusion potential $E _ { j }$ at different operating temperatures keeping the applied current fixed at $4 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ .The SOC used ranges from $1 0 \%$ to $9 0 \%$ with a step size of $1 0 \%$ ，and the operating temperatures range from $1 0 ~ ^ { \circ } \mathrm { C }$ to $4 0 ~ ^ { \circ } \mathrm { C }$ with a step of $1 0 ~ ^ { \circ } \mathrm { C }$ In Fig. 5(a) and 5(b),we observe that the magnitudes of the difusion potential for the charge and discharge cases are close to each other.Also,in Fig. 5(c) we observe that the membrane diffusion potential increases with increasing SOC and operating temperature,both for the charge and discharge cases.This can be attributed to the fact that the potential generated at the interface is highly dependent on the concentration of species in that region.As the change in SOC implies a change in concentration ratio of all the vanadium ions,we see variation in the potential.

Next,we study the variation of the diffusion potential at different applied currents while fixing the state of charge.We utilize currents ranging from $2 0 ~ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ to $1 2 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ while the range of operating temperatures is the same as before.The results are presented in Fig. 5(c).For reasons stated in the previous paragraph,we see that an increase in state of charge leads to an increase in diffusion potential in this figure as well.We also see that the magnitude of the diffusion potential increases with an increase in applied current. This is because an increase in applied current increases the electric field which in turn contributes to the migration flux.This migration flux in turn plays a direct role in the species concentration at the junction.As the contribution of flux due to migration is much lower than that of diffusion [28],we see that changing the applied current from 20 $\mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ to $1 2 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ (which in turn changes the migration flux) does not bring about a drastic difference in diffusion potential $\left( \leq 1 \mathrm { m V } \right)$

# 3.4. Analysis of activation overpotential $\eta _ { \pm }$

In this section,we analyze the variation of activation overpotential with temperature and applied current density at three different states of charge.As before,the operating temperature is varied from $1 0 ~ ^ { \circ } \mathrm { C }$ to $4 0 ~ ^ { \circ } \mathrm { C }$ and the applied current from $2 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ to $1 2 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ ； the states of charge selected are $2 0 \%$ ， $5 0 \%$ ,and $8 0 \%$ . In Fig.6(a), we see a linear variation of $\eta _ { + }$ with applied current density $I$ ，whereas in Fig.6(b) the variation of $\eta _ { - }$ with respect to applied current $I$ shows some nonlinear behavior.The linear like behavior of $\eta _ { + }$ can be attributed to the fact that we are still in the low overpotential regime where linear behavior is observed with respect to the applied current.Additionally,we have estimated the area-weighted average value of the activation overpotential across each electrode,so some minor deviations are expected.To verify the linearity,we simplified the Butler-Volmer Eq.(l3) by substituting our values for charge transfer coefficients $( \alpha _ { + , a } , ~ \alpha _ { + , c } )$ and assuming that the surface concentrations are equal to bulk concentrations.This results in the expression $\eta _ { + } =$ $\begin{array} { r } { { \frac { R T } { F } } \sinh ^ { - 1 } \left( { \frac { i } { 2 i _ { 0 } A ^ { * } } } \right) } \end{array}$ ,where $\begin{array} { r } { A ^ { * } = \frac { a V _ { e } } { \varDelta _ { s } } } \end{array}$ such that $V _ { e }$ is the volume of the cuboid defined by dimensions of our electrode,and $A _ { s }$ is the surface area of the electrode (product of length and width of electrode). (Note, here we assume the Butler-Volmer current density $i$ is equal to the load current density $I$ ,and in this way we analyze variation of overpotential for each applied current density.Here,unlike Eq. (l3),we are not using volumetric currents,the units of $i$ and $i _ { 0 }$ are in $A / m ^ { 2 } )$ .Upon comparing the results from this simplified expression to our simulation, a reasonable similarity of values was observed.Also,a linear variation for $\eta _ { + }$ and some non-linear variation for $\eta _ { - }$ versus applied current densityi was observed.

Regarding the behavior of activation overpotential with current, the explanation can be obtained directly by analyzing the Butler-Volmer relation.Fora fixed exchange current density, sustaining higher applied currents requires a larger activation overpotential as more electrons must be transferred.Conversely,an increase in temperature increases the rate constant and thus the exchange current density,so for the same applied current the activation overpotential decreases.With respect to state of charge,we can see from (l9) that the equilibrium potential increases with SOC due to the rise in $\nabla { \mathsf { O } } _ { 2 } ^ { + }$ concentration. The solid potential $\phi _ { s }$ remains constant at fixed load current,while the electrolyte potential $\phi _ { e }$ also shifts with SOC. As a result, the term $\phi _ { s } - \phi _ { e } - E _ { \pm }$ in (18) increases in magnitude with SOC leading to a larger activation overpotential.

![](images/4e523fda07918387bed17971682846118b78026579b2db9554533980d1e00924.jpg)  
Fig3.(a)oc bold black line shows a reference scale of length $1 0 ~ \mathrm { m m }$ .The black square approximately at the center of the geometry shows the region which is magnified for observing the mesh.In the electrode regions we use a maximum element size of $5 0 ~ { \mu \mathrm { m } }$ while in the membrane it is $8 \ \mu \mathrm { m }$ .(b) Comparison of charge-discharge curves at flow rate of $6 0 ~ \mathrm { m l / m i n }$ betweenpresent simulationsand experimentaldata from34]forcellvoltageatdiferentstatesof charge. (c)Validationbased on polarization curve at flow rate of $1 5 ~ \mathrm { m l / m i n }$ with data taken from [39].

# 3.5.Impact of diffusion potential on voltage efficiency and comparison of voltage losses

In this section,we compare the contributions of the membrane diffusion potential,activation overpotential,and ohmic overpotential to the loss in the cell voltage and study the impact of diffusion potential on voltage efficiency.To define the ohmic losses we use an expression from [12],

$$
\eta _ { o h m i c } = \left( \frac { I L _ { t } } { \epsilon ^ { \frac { 3 } { 2 } } \frac { F ^ { 2 } } { R T } \sum _ { i } z _ { i } ^ { 2 } D _ { i } ^ { e f f } c _ { i } } \right) _ { + } + \left( \frac { I L _ { t } } { \epsilon ^ { \frac { 3 } { 2 } } \frac { F ^ { 2 } } { R T } \sum _ { i } z _ { i } ^ { 2 } D _ { i } ^ { e f f } c _ { i } } \right) _ { - } + \frac { 2 I } { \sigma _ { c } } L _ { c } ,
$$

where the subscript $+ / -$ denotes the positive or negative side of the cell, and $\epsilon$ is the porosity of the electrode. The remaining parameters: $L _ { t } , \ \sigma _ { c }$ ，and $L _ { c }$ are the thickness of electrode,conductivity of current collectors,and thickness of current collectors,respectively (see Table 1).

The results are presented in Fig.9 in the Appendix.We see that the ohmic overpotential dominates the losses over the other two in all cases,even at low current of $2 0 \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ,owing to the fact that we have a highly diluted solution resulting in low ionic conductivity.At high temperature,high current,and low state of charge,loss due to ohmic overpotential is the highest as seen in Fig.9(c).The contribution from diffusion potential is small at high currents.Additionally,in the same Fig. 9(c) we observe that at low state of charge,low currents,and high temperature the loss due to diffusion potential becomes comparable to the loss due to activation overpotential.It is also observed that,at low temperatures,low state of charge and high currents,the diffusion potential gives a negligible contribution to the cell voltage losses (Fig. 9(a)).Regarding contribution of activation losses,we see that it is highest at low temperatures and high states of charge. In general, we can conclude that for higher power usage the focus should be shifted to reducing the ohmic losses,as its contribution to the losses is dominant in that regime,whereas for low load situations and low temperatures, we cannot ignore the activation and diffusion potential.

![](images/853f8cf42a8d51ac3f9bf3d2d0302a019465e2848be3ef9e003b84981af3906c.jpg)  
Fig.4.Distribution of species concentration (a) positive electrode $\nabla { \mathsf { O } } _ { 2 } ^ { + }$ and negative electrode $\mathrm { V } ^ { 2 + }$ ,(b） positive electrode $\scriptstyle \mathsf { V O } ^ { 2 + }$ and negative electrode $\mathsf { V } ^ { 3 + }$ Distribution of species concentration along horizontal line at $_ { 1 \mathrm { \ c m } }$ from inlet: (c) $\mathrm { V O } _ { 2 / } ^ { + } \mathrm { V O } ^ { 2 + }$ ， $\mathsf { V } ^ { 2 + } / \mathsf { V } ^ { 3 + }$ ；(d) $\mathrm { H } ^ { + }$ ， $\mathrm { H S O } _ { 4 } ^ { - }$ ·

![](images/7a7d43db1a35075200a835aad5aa293df9b102d5543ed5f4e4a65f7ec11fb00e.jpg)  
Fig.5.(a) and (b)- Variation of difusion potential across membrane $E _ { j }$ with state of charge and applied temperature at fixed current load for (a) charging and (b) discharging.(c)- Variation of difusion potential $E _ { j }$ $\mathrm { ( m V ) }$ during discharge,with applied current and operating temperature at varying initial vanadium concentrations (states of charge) of $2 0 \%$ ， $5 0 \%$ ,and $8 0 \%$ SOC.

Next,we analyze the effect of diffusion potential on loss in state of charge and voltage efficiency.The loss in state of charge can be estimated as the diference between the state of charge corresponding to the ideal situation (meaning-no diffusion potential) and the state of charge with presence of diffusion potential. The ratio of this diference to the ideal case will give us the relative loss,defined as

![](images/c63c7c980988ea050a71a2b07670c6d1ae9e2f35a58b453653da0647e95bd263.jpg)  
Fig6ctidi of charge (SOC).

![](images/5e46838ec434cee8f3e397e76eb187e243f35b90c62e61f8f6daf31716bc8887.jpg)  
Fig.7.(a)Graphicalrepresentationoflossin stateofchargedueto membrane difusion potentialduring charging.The term $E _ { l o s s }$ consists of the sum of overpotentials considered in this work. $S O C _ { c h }$ means charging mode with diffusion potential included, and $S O C _ { c h } ^ { * }$ implies charging in absence of difusion potential. (b)-(d): effect of diffusion potential on loss in state of charge for charging to SOC of (b) $3 0 \%$ （c) $6 0 \% ,$ and (d) $9 0 \%$ at applied currents $4 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ， $8 0 ~ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ， $1 2 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ,and operating temperatures ranging from ${ 1 0 ~ ^ { \circ } \mathrm { C } }$ to $4 0 ~ ^ { \circ } \mathrm { C }$

$$
 { \displaystyle { \cal A } _ { S O C } = \frac { S O C _ { c h } ^ { * } - S O C _ { c h } } { S O C _ { c h } ^ { * } } . }
$$

Here, the term $S O C _ { c h }$ means charging mode with diffusion potential included, and $S O C _ { c h } ^ { * }$ implies charging in absence of difusion potential.

A graphical description of the loss in state of charge is presented in Fig.7(a). In the figure,the bold black curve is the case when there are no overpotentials,the dashed black curve corresponds to what we called the “ideal situation”in the preceding paragraph (ohmic and activation losses added to cell voltage,but no diffusion potential across membrane),and the red curve shows the cell voltage accounting for all three loss contributors considered in this article.

![](images/471e3dd338502077074fb6636823dada3a88c913b326e19f0065a39225b29285.jpg)  
Fig.8.(a)Lossinnergyadcapacitycausedbyifusionpotentialduringcharge.(b)-(d)ierenceinpowerrequiredforharging $( P _ { i n } ^ { \prime } )$ and power in absence of membrane diffusion potential $\left( P _ { i n } \right)$ for charging to SOC of (b) $3 0 \%$ ，(c) $6 0 \%$ ,and (d) $9 0 \%$ ,at applied currents $4 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ， $8 0 ~ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ,and $1 2 0 ~ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ,and operating temperatures ranging from ${ 1 0 ~ ^ { \circ } \mathrm { C } }$ to $4 0 ~ ^ { \circ } \mathrm { C }$

We analyze the loss in state of charge due to diffusion potential when charging up to $3 0 \%$ ， $6 0 \%$ ，and $9 0 \%$ SOC at different temperatures.To do this,we determine the cell voltage corresponding to the target SOC (out of $3 0 \%$ ， $6 0 \%$ and $9 0 \%$ at $2 0 \ ^ { \circ } \mathrm { C } ,$ and use this cell voltage as the cutoff potential for the remaining operating temperatures $( 1 0 \ ^ { \circ } \mathrm { C } , 3 0 \ ^ { \circ } \mathrm { C } , 4 0 \ ^ { \circ } \mathrm { C } )$ . In this way we perform the analysis for charging at applied current of $4 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ， $8 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ ，and $1 2 0 \ \mathrm { m A } / \mathrm { c m } ^ { 2 }$ .The result is presented in Fig.7.While diffusion potential is seen to increase with SOC,current,and temperature,the corresponding SOC loss does not follow a simple increasing or decreasing trend. In Fig.7(b) we observe a simple trend - the SOC loss increases with applied current and temperature.In the cases presented in Figs. 7(c) and 7(d),we see that the loss in state of charge now does not follow any particular trend with respect to load current and operating temperature.This can be attributed to the fact that the SOC loss is governed by a combination of diffusion potential and other overpotentials (e.g.，activation and ohmic),whose relative magnitudes vary with operating conditions.At high currents,for instance,the impact of diffusion potential may be masked by dominant ohmic losses,while at low currents it becomes proportionally more significant (see Appendix 5).These interactions lead to non-monotonic behavior in the SOC loss profile. Overall,we can see that these losses range from $2 \%$ to $2 4 \%$ depending on the cut-off potential,which can be highly significant when operating with large stacks.

Next,we estimate the impact of diffusion potential on charging voltage efficiency.In Fig.8(a),we show how the diffusion potential contributes to energy and capacity loss,both of which are associated to the voltage efficiency.

Let $\hat { \eta } _ { c h }$ be the voltage efficiency of the cell in the absence of membrane diffusion potential (but including the overpotentials),and $\hat { \eta } _ { c h } ^ { \prime }$ bethe voltage efficiency of thecell when we acount for the membrane diffusion potential in addition to the overpotentials.Then using our definition for cell voltage in Eq.(31),we can define the

voltage efficiencies as [10]:

$$
\hat { \eta } _ { c h } = \frac { \int _ { t _ { 0 } } ^ { t _ { c h } } E _ { e q } d t } { \int _ { t _ { 0 } } ^ { t _ { c h } } E _ { c e l l } d t } ,
$$

and

$$
\hat { \eta } _ { c h } ^ { \prime } = \frac { \int _ { t _ { 0 } } ^ { t _ { c h } } E _ { e q } d t } { \int _ { t _ { 0 } } ^ { t _ { c h } } E _ { \underline { { { c } } } e l l } ^ { \prime } d t } .
$$

As described previously, $E _ { c e l l }$ is the total cell voltage in the absence of diffusion potential, and $E _ { c e l l } ^ { \prime }$ includes the diffusion potential. The starting time for charge and end time for charge are denoted by $t _ { 0 }$ and $t _ { c h }$ ，respectively. $E _ { e q }$ is the net equilibrium potential defined in Eqs.(19) and (2O).The factor by which the voltage efficiency changes due to the presence of diffusion potential $E _ { j }$ can be evaluated as follows:

$$
\xi _ { c h } = \frac { \hat { \eta } _ { c h } ^ { \prime } } { \hat { \eta } _ { c h } } = \frac { \int _ { t _ { 0 } } ^ { t _ { c h } } E _ { c e l l } d t } { \int _ { t _ { 0 } } ^ { t _ { c h } } E _ { c e l l } ^ { \prime } d t } = \frac { I ^ { * } \langle E _ { c e l l } \rangle } { I ^ { * } \langle E _ { { c e l l } } ^ { \prime } \rangle } = \frac { \langle P _ { i d } \rangle } { \langle P _ { i n } ^ { \prime } \rangle } .
$$

Here $I ^ { * }$ is fixed load current, $P _ { i d }$ is the power required for charging in the ideal case (absence of membrane diffusion potential),and $P _ { i n } ^ { \prime }$ is the power required for charging when membrane diffusion potential is present. The average $\langle f \rangle$ is defined as:

$$
\langle f \rangle = \frac { 1 } { t _ { c h } - t _ { 0 } } \int _ { t _ { 0 } } ^ { t _ { c h } } f ( t ) d t = \frac { 1 } { s _ { e } - s _ { 0 } } \int _ { s _ { 0 } } ^ { s _ { e } } f ( s o c ) d ( s o c ) ,
$$

where $s _ { e }$ is the state of charge at time $t _ { c h }$ (which is the end time of charge),and $s _ { 0 }$ is the state of charge at time $t _ { 0 }$ (the starting time of charge).This is derived from the relation between state of charge and capacity.

We observed that the diffusion potential does not cause any dramatic effects on the voltage efficiency of the cell.A maximum loss of $2 \%$ was observed depending on our operating parameters, while charging to $9 0 \%$ state of charge.We could see that the loss in efficiency increases with the decrease in applied current and increase in temperature,as the effect of the diffusion potential becomes more dominant under these circumstances.When operating with large stacks,the accumulation of these losses becomes significant.To observe this,we take the examples of a5 kW,10 kW,and $2 0 ~ \mathrm { k W }$ stacks and study the difference between the input power required for charging and the power required when we exclude diffusion potential across the membrane.Based on the relationship between power and change in voltage eficiency $\xi _ { c h }$ ，we can calculate the input power required:

![](images/a8c4f56b1fb7cd68b404fbd78b334b70f708ec5f15b4693d153f942b4a6ed83a.jpg)  
Fig.9.Comparison of contribution to voltage losses by membrane difusion potential $( E _ { j } )$ ，activation overpotential $( \eta _ { a c t } )$ ,and ohmic overpotential $( \eta _ { o h m i c } )$ a varying states of charge and at varying temperatures: (a) $1 0 \ ^ { \circ } \mathrm { C } ,$ (b) $2 0 ~ ^ { \circ } \mathrm { C }$ and (c) $4 0 ~ ^ { \circ } \mathrm { C }$

$$
\langle P _ { i n } ^ { \prime } \rangle = \frac { \langle P _ { i d } \rangle } { \xi _ { c h } } .
$$

In Fig. 8, we display the dependence of $P _ { i n } ^ { \prime } - P _ { i d }$ on the operating temperature and applied current.We observe that the power loss ranges from 14 watts to 58O watts depending on the final state of charge,load current,operating temperature,and the number of cells used in stack. In Figs.8(b)-8(d) we also observe that the loss in power increases as we charge up to a higher state of charge.As previously stated,this minor loss due to diffusion potential is expected to accumulate as we use more cells and become a significant number,which can be seen from the increasing loss in power with increasing size of stack.We also observe in the same figure that the power discrepancy is highest for large temperature and low current,as the contribution of diffusion potential is dominant in this situation.

# 4. Conclusions

In this work,a 2D steady state model for VRFB cell incorporating all fluxes in species transport is numerically investigated. The study is devoted to the detailed investigation of the effect of diffusion potential across membrane on the loss in cell voltage,power,and state of charge in VRFB systems.The obtained results are important for determination of proper operating conditions and development of reliable and efficient VRFB systems.

First, we analyzed the efects of load current, operating temperature, and initial vanadium ion concentration (state of charge) on: (1） the changes in membrane diffusion potential;(2) losses associated with chemical kinetics;and (3) ohmic losses.It was determined that the main contributors to diffusion potential are the operating temperature and initial vanadium concentration (state of charge).The applied current was also a contributor due to its effect on the migration flux which causes changes in concentration gradients across the membrane. Next,we found that an increase in temperature decreases the activation overpotential, both in the negative and positive electrode.We also found that activation overpotential increases with applied current, but its rate of increase is higher in the negative electrode owing to the change in chemical kinetics described by the model. The ohmic losses were found to be increasing with increase in operating temperature, load current,and state of charge.

The evaluation of contribution to loss in voltage due membrane diffusion potential,activation loss,and ohmic loss showed that the loss due to diffusion potential becomes comparable to the activation losses at high temperatures.The loss in state of charge due to diffusion potential was observed to range from $2 \%$ to $2 4 \%$ depending on the applied current,operating temperature,and cut-off potential.While diffusion potential was seen to increase with initial vanadium concentration, current,and temperature, the corresponding SOC loss does not show a simple monotonic increasing/decreasing behavior.Further analysis on voltage efficiency for stacks ranging from $5 \mathrm { k W }$ to $2 0 ~ \mathrm { k W }$ showed that the diffusion potential causes power loss ranging from 14 to 58o wats, depending on the load current, operating temperature and final state of charge.This implies that for $1 0 0 ~ \mathrm { k W }$ to 1 MW scale stacks, these losses become increasingly important to counteract.

As the main cause of diffusion potential across membrane is the diference in mobilities of ions and concentration gradients across the membrane,it is recommended to balance electrolyte compositions actively and maintain temperatures below $3 0 ~ ^ { \circ } \mathrm { C }$ for mitigating the diffusion potential.It should be noted that properties of the membrane material can also affect the membrane potential due to different mechanisms of ion conductivity.Analysis of these effects are outside the scope of the present paper,but would in our opinion be interesting to investigate in the future.

# CRediT authorship contribution statement

V.Kumar:Writing- review & editing,Writing- original draft, Visualization,Validation,Software,Methodology,Investigation, Formal analysis,Data curation.M.Pugach:Writing - review & editing, Supervision,Methodology, Investigation,Conceptualization.A.Kasimov: Writing -review & editing,Writing- original draft, Supervision, Methodology, Investigation, Conceptualization.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Appendix 5

See Fig. 9.

# Data availability

Data will be made available on request.

# References

[1]B.Dunn,H. Kamath,J.M. Tarascon,Electrical energy storage for the grid:a battery of choices,Science 334 (6058) (2011) 928-935,http://dx.doi.org/10. 1126/science.1212741.   
[2] L.F.Arenas,C.P.de León,F.C.Walsh,Redox flow batteries for energy storage: their promise,achievements and challenges,Curr.Opin.Electrochem.16 (2019) 117-126, http://dx.doi.org/10.1016/j.coelec.2019.05.007.   
[3]Y.Jiang,Z. Liu,Y.Ren,A.Tang,L.Dai,L.Wang,S.Liu,Y. Liu,Z. He, Maneuverable B-site cation in perovskite tuning anode reaction kinetics in vanadium redox flow batteries,J.Mater.Sci.Technol.186 (2024) 199-206, http://dx.doi.org/10.1016/j.jmst.2023.12.005.   
[4]Q.Wang,R. Yan, J. Chen, Z. Jiang,Z. Qu, Numerical study of vanadium redox flow battery with gradient porosity induced by electrode compression,J.Energy Storage 72 (2023) 108465,http://dx.doi.org/10.1016/j.est.2023.108465. (24) (2022) 7786-7810, http://dx.doi.0rg/10.1021/acssuschemeng.2c01372. [6]X.Chen,L.Li,Y. Jiang,Z.Feng,Q.Li,L.Jiang,L.Dai,L.Wang,Z. He, Manipulating the local electronic structure microenvironment at the MXene interface to achieve efficient anode for vanadium redox flow battery,J.Energy Chem.104 (2025) 118-126,http://dx.doi.0rg/10.1016/j.jechem.2024.11.062. [7]T.Puleston,A. Clemente,R.C.Castell6,M. Serra,Modelling and estimation of vanadium redox flow batteries:A review,Batteries 8 (9)(2022) http://dx.doi. org/10.3390/batteries8090121. [8]A.A. Kurilovich,A.Trovo,M.Pugach,K.J. Stevenson,M. Guarnieri, Prospect of modeling industrial scale flow bateries-From experimental data to accurate overpotential identification,Renew. Sustain. Energy Rev.167 (2022) 112559, http://dx.doi.org/10.1016/j.rser.2022.112559.   
[9] W.J. Zou,H.Y. Jung,S.Jung，Modeling and performance optimization of vanadium redox flow batteries,J.Energy Storage 121 (2025) 116601，http: //dx.doi.org/10.1016/j.est.2025.116601.   
[10]M. Pugach,V.Vyshinsky,A.Bischi,Energy efficiency analysis fora kilo-watt class vanadium redox flow battery system,Appl.Energy 253 (2019)113533, http://dx.doi.org/10.1016/j.apenergy.2019.113533.   
[11]H. Wang,S.A. Pourmousavi, Y.Li, W.L.Soong,X. Zhang,B. Xiong,A new zerodimensional dynamic model to study the capacity loss mechanism of vanadium redox flow batteries,J.Power Sources 603(2024) 234428,http://dx.doi.org/ 10.1016/j.jpowsour.2024.234428.   
[12]Y.Lei, B.Zhang,B.Bai,T. Zhao,A transient electrochemical model incorporating the Donnan effect for all-vanadium redox flow batteries,J.Power Sources 299 (2015) 202-211, http://dx.doi.0rg/10.1016/j.jpowsour.2015.08.100.   
[13]P.J.Alphonse,G.Elden,The investigation of thermal behavior in a vanadium redox flow battery during charge and discharge processes,J.Energy Storage 40 (2021) 102770, http://dx.doi.0rg/10.1016/j.est.2021.102770.   
[14] Y.S.Chou,S.C. Yen,A.Arpornwichanop,B.Singh,Y.S.Chen,Mathematical model to study vanadiumion crossover in an all-vanadium redox flow battery, ACS Sustain.Chem. Eng.9 (15) (2021) 5377-5387,http://dx.doi.org/10.1021/ acssuschemeng.lc00233.   
[15]F.Staciaki,L.F.Pilonetto,E. Nobrega,E.B.Carneiro-Neto,J.da Silva,M.A.B. Ferreira,E.Pereira,CFD simulation for optimizing vanadium redox flow batteries:Addressing geometric design and cross-contamination challenges,ECS Meet.Abstr.MA2025-01 (27) (2025)1510,http://dx.doi.0rg/10.1149/MA2025- 01271510mtgabs.   
[16] N.M. Delgado,R. Monteiro,M.Abdollahzadeh,P.Ribeirinha,A. Bentien,A. Mendes,2D-dynamic phenomenological modelling of vanadium redox flow batteries-Analysis of the mass transport related overpotentials,J.Power Sources 480 (2020) 229142, http://dx.doi.org/10.1016/j.jpowsour.2020.229142.   
[17]Q.He,Z.Li,D.Zhao,J.Yu,P.Tan,M.Guo,T.Liao,T.Zhao,M.Ni,A 3D modeling study on all vanadium redox flow battery at various operating temperatures, Energy 282 (2023)128934，htp://dx.doi.0rg/10.1016/j.energy. 2023.128934.   
[18]S.Bogdanov,M.Pugach,S.Parsegov,V.Vlasov,F.M.Ibanez,K.J.Stevenson, P.Vorobev,Dynamic modeling of vanadium redox flow batteries: Practical approaches,their applications and limitations, J. Energy Storage 57 (2023) 106191, http://dx.doi.org/10.1016/j.est.2022.106191， URL: https://www.sciencedirect. com/science/article/pii/S2352152X22021806.   
[19]M. Messggi, C.Gambaro,A. Casalegno,M. Zago, Development of innovative flow fields in a vanadium redox flow battery:Design of channel obstructions with the aid of 3D computational fluid dynamic model and experimental validation through locally-resolved polarization curves,J.Power Sources 526 (2022) 231155, http://dx.doi.org/10.1016/j.jpowsour.2022.231155.   
[20] F. Zorrilla,M.Montiel,R. Mustata,R.Losantos,L.Valino,Impact of electrolyte composition on the mitigation of electrolyte imbalance in a vanadium redox flow battery:A3D multiphysics model,J.Energy Storage 107 (2025) 14899, http://dx.doi.0rg/10.1016/j.est.2024.114899.   
[21]Y.Chen, J. Bao,Z.Xu,P.Gao,L.Yan,S.Kim,W.Wang,A hybrid analytical and numerical model for cross-over and performance decay in a unit cell vanadium redox flow batery,J.Power Sources 578 (2023) 233210,htp://dx.doi.org/10. 1016/j.jpowsour.2023.233210.   
[22] Andrea Trovo,Francesco Picano,Massimo Guarnieri, Comparison of energy losses in a 9 kW vanadium redox flow battery,J.Power Sources 440 (2019) 227144, http://dx.doi.0rg/10.1016/j.jpowsour.2019.227144.   
[23] C.Tempelman,J.Jacobs,R.Balzer,V.Degirmenci, Membranes for all vanadium redox flow batteries, J. Energy Storage 32 (2020) htp://dx.doi.org/10.1016/j. est.2020.101754.   
[24]K. Hongsirikarn,X.Mo,Z. Liu, J.G.Goodwin, Prediction of the effective conductivity of Nafion in the catalyst layer of a proton exchange membrane fuel cell, J. Power Sources 195 (17) (2010) 5493-5500,htp://dx.doi.0rg/10. 1016/j.jpowsour.2010.03.074.   
[25] C.Sun,J.Chen,H. Zhang,X.Han,Q.Luo,Investigations on transfer of water and vanadium ions across Nafion membrane in an operating vanadium redox flow battery,J. Power Sources 195 (3) (2010) 890-897, htp://dx.doi.0rg/10.   
[26]Y.Chen,J. Bao,Z.Xu,P.Gao,L.Yan,S.Kim,W.Wang,A hybrid analytical and numerical model for cross-over and performance decay in a unit cell vanadium redox flow battery,J.Power Sources 578 (2023) 233210,http://dx.doi.org/10. 1016/j.jpowsour.2023.233210.   
[27]M. Pugach,S.Bogdanov,V.Vlasov,V.Erofeeva,S.Parsegov,Identification of crossover flux in VRFB cells during battery cycling,J.Power Sources 61o (2024) 234745, http://dx.doi.org/10.1016/j.jpowsour.2024.234745.   
[28] X.G.Yang,Q.Ye,P.Cheng,T.S.Zhao,Effects of the electric field on ion crossover in vanadium redox flow batteries,Appl. Energy 145 (2015) 306-319, http://dx.doi.org/10.1016/j.apenergy.2015.02.038.   
[29] A.J.Bard， L.R. Faulkner， Electrochemical Methods: Fundamentalsand Applications, second ed.Wiley, 2001.   
[30] P.A.Gokturk,R.Sujanani,J.Qian,Y.Wang,L.E.Katz,B.D.Freeman,E.J. Crumlin,The Donnan potential revealed,Nat. Commun.13(1) (2022) 5880, http://dx.doi.org/10.1038/s41467-022-33592-3.   
[31]Y.W.Liang Hao,Y.He,Modeling of ion crossover in an all-vanadium redox flow battery with the interfacial efect at membrane/electrode interfaces,J. Electrochem.Soc.166 (2019) http://dx.doi.org/10.1149/2.1061906jes.   
[32]K.W.Knehr,E.Agar,C.R. Dennison,A.R. Kalidindi, E.C. Kumbur,A transient vanadium flow battery model incorporating vanadium crossover and water transport through the membrane,J.Electrochem. Soc.159 (2012) http://dx. doi.org/10.1149/2.017209jes.   
[33] Y.Ashraf Gandomi,D.Aaron,M. Mench,Coupled membrane transport parameters for ionic species in all-vanadium redox flow batteries,Electrochim.Acta 218 (2016) 174-190, http://dx.doi.org/10.1016/j.electacta.2016.09.087.   
[34]D.You,H. Zhang,J.Chen,A simple model for the vanadium redox battery,Electrochim.Acta 54 (27) (2009) 6827-6836,http://dx.doi.org/10.1016/j. electacta.20o9.06.086, URL: https://www.sciencedirect.com/science/article/pii/ S0013468609009128.   
[35]J.W.Perram，P.J. Stiles,On the nature of liquid junction and membrane potentials,Phys.Chem. Chem.Phys.(20o6) http://dx.doi.org/10.1039/ B601668E.   
[36] Ansys Inc.，Ansys@fluent,release 19.2，ANSYS Inc.，2018,Canonsburg, Pennsylvania, USA, URL: https://www.ansys.com/products/fluids/ansys-fluent, Computer Software.   
[37] H.K.Versteeg，W. Malalasekera，An Introduction to Computational Fluid Dynamics: The Finite Volume Method, second ed. Pearson, 2007.   
[38]K. Stuiben,Algebraic Multigrid (AMG).An Introduction with Applications,1999, http://dx.doi.org/10.24406/publica-fhg-290270.   
[39]Q. Zheng,F. Xing,X.Li, T.Liu, Q.Lai,G. Ning,H. Zhang,Investigation on the performance evaluation method of flow batteries,J.Power Sources 266 (2014) 145-149, http://dx.doi.org/10.1016/j.jpowsour.2014.04.148.