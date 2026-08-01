# An analytical model for shunt currents in electrolyser, fuel cell,and flow battery stacks

J.W.Haverkort(

Delft Universityofechnology,Process &EnergyDepartment,Leghwaterstraat39,Delft2628CB,TheNetherlands

# HIGHLIGHTS

·Exact analytical shunt current model revisited for flow batteries and electrolysers.
·Very simple yet accurate approximations are obtained for engineering estimates.
·Faradaic and energy efficiency expressions can be directly used for optimisation.
·High manifold resistance is the surest way to avoid shunt currents for long stacks.
·Criteria for stack failure and optimum battery current with self-discharge derived.

# GRAPHICAL ABSTRACT

![](images/e08f7ce048b49c5f06d6fe16ca6a2ffb518c5798d3c67ad679a73cfb99bf7491.jpg)

# ARTICLEINFO

# ABSTRACT

Keywords: Shunt currents Bypass currents Leakage currents Parasitic currents Stray currents Bipolar stacks Analytical modelling

Ina bipolar stack,electrochemical cells are electronically connected in series.If the electrolyte resistance between cells through the manifold is insufficient,some curent will leak out of the cells.This reduces overall effciency,an important loss mechanism to consider when designing a stack.Many works exist in the literature that model these shunt currents through an equivalent circuit with resistances $R _ { \mathrm { i o } }$ into or out of the cells, $R _ { \mathrm { m n } }$ in the manifold between cells,and a linearised cell voltage with offset $V _ { \mathrm { l i n } }$ and resistance $R _ { \mathrm { l i n } }$ .However,these typically require a numerical solution.We discuss the exact analytical solution,which gives $- ( V _ { \mathrm { l i n } } - I R _ { \mathrm { l i n } } ) / ( R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } + 1 2 R _ { \mathrm { i o } } / ( N ( N + 1 ) ) )$ as a new intuitive,simple approximation for the average manifold shunt current. In an electrolyser, $V _ { \mathrm { l i n } } < 0$ and shunt currents increase with increasing current $I$ .In a discharging (flow) battery, $V _ { \mathrm { l i n } } > 0$ and shunt currents are negative,as they run in a direction opposite to the stack currnt.We use this model to provide clear engineering guidelines for stack design.The exact and approximate solutions are highly practical and insightful results that can be easily used for optimisation and should find widespread use in various industrially relevant applications.

# 1. Introduction

In a bipolar stack configuration, each anode is connected to a bipolar plate and to the cathode of the next cell, forming an electrical series circuit. Contrary to a monopolar or unipolar configuration,in which cells are electrically connected in parallel, the current is approximately constant throughout the stack,and the voltage increases with every cell [1]. Its main advantage is that the current remains relatively low, minimising ohmic losses in cables,connectors,and power equipment, and the relatively high voltage requires less transformation of typical power sources that operate at high voltage [2].

In many bipolar stacks,electrolyte is fed to the cells and products are removed by a common manifold that connects all cells. Voltage

# Nomenclature

# Greek variables

$\eta$ Activation overpotential [V] $\kappa$ Electrolyte conductivity $[ \Omega \mathrm { m } ^ { - 1 } ]$ $\phi$ Electrostatic potential in electrolyte [V] $\varphi$ Efficiency [-] $V$ Electrostatic potential in electrodes [V]

# Roman

$I$ Stack current $( I = I _ { 0 } = I _ { N } ) [ \mathrm { A } ]$ $i$ Shunt current through manifold [A] $i ^ { \prime }$ Shunt into/out of cells [A] $k$ Cell index (1..N) [-] M Thiele modulus (Eq.(14)) [-] $N$ Number of cells [-] $R$ Resistance [Ω] $\bar { R } _ { \mathrm { i o } }$ Dimensionless $\mathbf { i } / \mathbf { o }$ resistance $\frac { R _ { \mathrm { i o } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } } [ - ]$ $x$ $\frac { 1 + 2 \bar { R } _ { \mathrm { i o } } - \sqrt { 1 + 4 \bar { R } _ { \mathrm { i o } } } } { 2 \bar { R } _ { \mathrm { i o } } }$ viz q (C.8, .)

# Mathematical operators

cosh $x$ Hyperbolic cosine $\begin{array} { l } { \displaystyle { \frac { 1 } { 2 } \left( { \bf e } ^ { x } + { \bf e } ^ { - x } \right) } } \end{array}$ $\sinh x$ Hyperbolic sine ${ \frac { 1 } { 2 } } ( \mathbf { e } ^ { x } - \mathbf { e } ^ { - x } )$ tanh $x$ Hyperbolic tangent $\sinh x / \cosh x$

# Subscripts

<table><tr><td>k</td><td>index</td></tr><tr><td>a</td><td>Anode</td></tr><tr><td>av</td><td>Average</td></tr><tr><td>C</td><td>Cathode</td></tr><tr><td>EE</td><td>Energy Efficiency</td></tr><tr><td>eq</td><td>Equilibrium,no current</td></tr><tr><td>FE</td><td>Faradaic Efficiency</td></tr><tr><td>io</td><td>Input/Output to cells</td></tr><tr><td>lin</td><td>Linear(ised)</td></tr><tr><td>max</td><td>Maximum</td></tr><tr><td>mem</td><td>Membrane or diaphragm</td></tr><tr><td>mn</td><td>Manifold:header and footer</td></tr><tr><td>tn</td><td>Thermoneutral</td></tr></table>

differences between cells can cause currents to run through the manifold between cells, called shunt currents, or sometimes bypass currents, leakage,by-pass currents, inter-cell currents,stray currents,parasitic currents,dispersion currents,or leakage currents.In electrolytic processes,these currents are in the same direction as the stack current, but they can skip many cells,decreasing the amount of product produced.

In galvanic stacks with a shared electrolyte,such as a discharging flow battery,ora liquid-electrolyte fuel cell like an alkaline fuel cell,phosphoric acid fuel cell,or molten carbonate fuel cell,shunt currents oppose the stack current.These currents are also undesirable because they are internal and cannot be used to do useful work,but they do increase voltage losses.Even without a net stack current, shunt currents in a flow battery persist, slowly discharging the battery. Similarly,reaction products in the electrolyte or at the electrodes of an electrolyser can react back [3],causing ‘reverse currents'that are sometimes referred to as the‘battery effect'.For example,whena water electrolyser is switched of,dissolved hydrogen and oxygen can cause the stack to operate as a fuel cell,with the anodes becoming cathodes and vice versa.However,the electrodes themselves can also participate in these reverse reactions,causing corrosion products and accelerated electrode deterioration.

Shunt and reverse currents can be mitigated by using long,smalldiameter inlet and outlet ports [4],sometimes called connecting tubes, or bubble separator channels. Such external manifolds are common, for example,in many redox flow battery designs.Chlor-alkali electrolysers also typically use external inlets and outlets,but are even more effective in avoiding shunt currents by having fluid-wise completely separated cells without a common manifold.A wide variety of patents to reduce or eliminate shunt currents exists,including innovative inlet/outlet channels [5-7],manifolds [8-12],means of stacking [13,14],or using auxiliary electrodes [5].Ways to interrupt current paths include cascaded flows [15] or dispersion [16,17].Shunt current interrupters or suppression devices exist in the form of perforated plates [18], elongated (helical) loops,gas bubbles,or revolving barriers [19].These measures often increase fabrication complexity and reduce the fraction of cross-sectional cell area available for the reaction.Inherently,increasing resistance to shunt currents usually also increases the pressure drop for electrolyte recirculation,which is required to supply reactants and remove heat and reaction products.This requires increased pumping costs but can also lead to significant,unsafe pressure build-up in the event of blockages,for example,due to corrosion products from the reverse reactions [2O].Therefore,it is often helpful to understand the relationship between geometrical design parameters and shunt current losses to achieve optimal designs that mitigate shunt currents while keeping pressure drops acceptable.

A wealth of literature exists on shunt currents,both from the modelling and the experimental side.Unfortunately，the modelling of electrolysers,flow batteries,or electrodialysis stacks is almost always treated separately despite their strong similarity:papers on redox flow batteries hardly citeworks on water electrolysers,and vice versa. Additionally,a large bodyof literature from the former USSR,despite being translated into English,has hardly been taken up in modern publications.As a result,many results are inadvertently reproduced.For example,solutions to the same equivalent circuit are published repeatedly,while insightful analytical formulas exist that render numerical solutions unnecessary.

A few limited review-like works exist [4,21] that provide a general overview or summarise various analytical models [22],solution methods [23],or using finite difference [24,25],

A particularly simple and almost exact analytical solution for the case of constant inlet and outlet port,manifold,and cell resistances can be obtained by treating the cell index as a continuous variable. This converts finite-difference equations into differential equations with solutions expressed in terms of hyperbolic functions.While several papers in the Russian literature point to [26] as the original reference of such continuous solutions, these seemed to have missed the original derivation of [27].Also Ref.[28] in the context of a general high voltage power supply system precedes [26]. The work by Ksenzhek and Koshel is one of the relatively few papers that consider a fuel cell stack,in which the shunt currents flow in the direction opposite to the stack current. Later publications using or expanding upon such solutions include Refs.[23,29-33] or ignoring manifold resistance [34], and extending to include multiple stacks [35].Ref.[36] includes a ground in the analysis and corrects some errors in Ref.[26].

If the resistance in the connecting manifold can be neglected,a parabolic shunt-current profile in the manifold results.Calculations showing such behaviour in Ref.[37] were within $1 4 \%$ of the experimental results [38].An analytical solution in this limit was obtained in Ref.[39] and mentioned in e.g. Refs. [21,40]. According to Ref.[27], a Russian book from1931 [4l] mayalready contain this derivation.A much simpler calculation appears in Ref.[2O].However,unfortunately, a mistake is made,and shunt currents are predicted to increase with the number of cells $N$ as $N ^ { 3 }$ .The review of Kuhn [21] mentions the correct scaling of shunt currents with $N ^ { 2 }$ . However,as argued, for example, in Refs.[42,43],this limit is of little practical use since the manifold resistance cannot usually be neglected.

Including the manifold resistance flattens the parabolic profile of the manifold shunt currents,with the cells at the ends making the dominant contribution.Ref.[23] notices the analogy with the penetration depth of porous electrodes and later extends the analysis to Tafel and also Butler-Volmer equation kinetics using computational methods in Ref.[44].A recent paper [33] uses linearised kinetics to derive continuous analytical solutions.An early purely algebraic approach was applied to electrodialysis stacks [45],where the cell voltage offset, which describes an equilibrium potential for a reaction,can be omitted. Additionally,a slightly different equivalent circuit was used.While insightful, the resulting shunt current expressions contain a factor 2/3 that should not appear,as in the reported limits of the more general analysis of Mandersloot and Hicks [46].

Ref.[35] derives an analytical solution by assuming all cells have the same cell voltage,which will only be accurate in the case of small shunt currents that hardly perturb the stack current.Actually,a year earlier,Thiele et al.[42] already published an exact solution for a linearised cell voltage. Unfortunately,possibly because this work is in German and contains a typographical error requiring re-analysis,it has been largely ignored.An exception is Ref.[47],which,however, does not explicitly credit Ref.[42].Later, this same model was reproduced in Refs.[48-5O].These works considered reserve batteries'that,unlike conventional batteries,have a common manifold.This allows the electrolyte to be added easily upon first use,thereby increasing the shelf life.

The flow-rate pressure drop relation for low-Reynolds-number fully developed laminar pipe flow,as described by the Hagen-Poiseuille equation,or Darcy's law inside a porous medium,is completely analogous to ohmic resistances.Therefore,very similar solutions can be found in the literature on flow in Z-type manifolds of e.g. heat exchangers [51] or fuel cells [52].Also,for heat transport,similar solutions for such ‘ladder networks'can be found,e.g.,in the recent work of Ref.[53].In the latter work,the finite-difference equations are solved exactly rather than resorting to a continuum approximation.

Equivalent circuit models for general bipolar stacks [24,54-56], water electrolysers [57], fuel cells [58-6O], for reserve batteries [47], chlorate cells [37],electrodialysis stacks [61] or e.g.Fe/Cr redox flow batteries [62] have been around fora long time.However,relatively recentlya large number of publications have come out for vanadium redox flow batteries with varying degrees of complexity,accuracy,validation,and additional physics [63-8O].Recent reduced-dimensional multiphysics water electrolyser models also sometimes include shunt currents [81-83].They have been equally applied to model reverse currents [84].

Shunt currents have also been studied experimentally in the literature,initially using magnetic field detectors [85],later using potential probes.Experimental results have been reported for chlorate [38], model systems [34],batteries [31],magnesium cells [86],vanadium redox flow batteries [68,71], zinc-bromine flow batteries [87], ironchromium redox flow batteries [88],lead electrolysis from molten chlorides [22],chlorate electrolysers [38],seawater electrolysers to make hypochlorite [89],and alkaline water electrolysers [4O,87,90- 96] These experiments overall reported to be in reasonable to excellent agreement with simplified models.

While plastic frames are increasingly common,and even standard in flow batteries,manifolds in electrolysers were traditionally made of metal.Burney and White [97] also included shunt currents through metallic manifolds,similar to Ref.[46] for electrodialysis.Ref.[98] improves upon the oversimplified analysis of Ref.[97] by including the reaction equilibrium voltage of the unwanted side-reactions

To study how deep shunt currents penetrate a single cell,some analytical attempts exist [33,47,66,99].Researchers have attempted computational simulations,from a single cell of an alkaline fuel cell in 2D [100],or an electrolyser [101] to multiple cells [66,90,102-

104] up to full 3D computational fluid dynamics simulations in single cell [105] or short-stacks [1O6-108]. Such computationally demanding three-dimensional models are not necessarily more accurate than rapid equivalent-circuit models,since they require information on many more geometric details that may not be fully characterised.

The purpose of the present contribution is to revisit and rigorously analyse a somewhat overlooked exact analytical model from the literature.From its limiting cases,we derive a surprisingly simple and intuitive new accurate approximation that is easy to use for optimisation.In Section 2 we first introduce a simplified equivalent circuit model, its exact solution,and approximations,in a form applicable to both electrolysers and (flow) batteries.In Section 3,we consider various performance criteria and discuss some aspects of optimisation.

# 2.Model

We aim to model the bipolar stack shown in Fig.1,where the stack current enters and leaves as a flow of electrons. These electrons are converted to or from ions in redox reactions that continue the current through the electrolyte and membranes between opposing electrodes. Electrolytes have to enter and leave cells to supply reactants and remove products and heat.To simplify the design,each cell usually does not have its own inlets and outlets;they are shared with the other cells in a stack by connecting to a manifold. To avoid product mixing,usually the anolyte and catholyte have their own inlet-,or feed manifold,and outlet-,or return manifold.However,by traversing a membrane,a continuous ionic pathway still exists between each anode and cathode in such a stack.The trajectory from the first to the last cell will be most used,as it bypasses all other cells,maximising the potential drop.However,each possible trajectory can contribute to the total shunt current that we now set out to analyse.

# 2.1.Resistances

Fig.1 shows a few possible shunt current trajectories.There are four different paths an ion can take to bypass the reaction: the feed channel or return channel for the anolyte and for the catholyte.For simplicity we will consider first a single manifold channel with an effective resistance $R _ { \mathrm { m n } }$ between adjacent cells.We will assume all resistances,including those introduced below,are constant and equal across each cell.

Fig. 2 shows an example shunt current trajectory. The contributing ionic current can originate and terminate at any point along the electrode's height.We assign a single ‘internal’ resistance $R _ { \mathrm { i n t } }$ to account for these trajectories to the cell outlet. The internal resistances and membrane resistance act in series with the outlet resistances to give a single equivalent outlet resistance

$$
R _ { \mathrm { o } } = R _ { \mathrm { o u t } } + R _ { \mathrm { i n t } } + R _ { \mathrm { m e m } } / 2
$$

Since the membrane has to be crossed only once per two outlet ports, this contribution is halved.Similarly for the inlets,we have $R _ { \mathrm { i } } { \mathrm { ~ \Omega ~ } } =$ $R _ { \mathrm { i n } } + R _ { \mathrm { i n t } } + R _ { \mathrm { m e m } } / 2$ .We will be able to generalise this later,but for now, considering a single manifold channel,we consider a single effective inlet/outlet resistance $R _ { \mathrm { i o } }$

The ohmic resistance over a pipe segment of length $l$ ,cross-sectional area $A$ ,equal to $\scriptstyle { \frac { \pi } { 4 } } \pi d ^ { 2 }$ for a circular cross-section with diameter $d$ ,and effective ionic conductivity $\kappa$ is given by Pouillet's law as

$$
R = { \frac { l } { \kappa A } }
$$

Therefore,to maximise the resistance to shunt currents,inlet and outlet ports in bipolar stacks are usually relatively slender.

In the above,we have simplified the shunt current resistance to a single resistance $R _ { \mathrm { i o } }$ into and out of the cell,in series with an integer number of manifold resistances $R _ { \mathrm { m n } }$ ,depending on the distance between cells.

![](images/568b2fe41d41ae9a1ca4bcc20a4470e2bcdeb36f6ca350709a8e24a9c88083cc.jpg)
FigAec fuelcell theeeesc oftheinletfoda ofcatholytedloeeee referred to the web version of this article.)

![](images/e2feed6c9285d8042d41d87c3b901dad648a3caa1a011e246e225d36dab9db78.jpg)
Fig.2.The idealised resistances encountered by an example shunt current trajectory through the return negolyte $( - )$ manifold.We group the resistances internal to a cell as $2 R _ { \mathrm { o } } = 2 R _ { \mathrm { o u t } } + 2 R _ { \mathrm { i n t } } + R _ { \mathrm { m e m } }$ and similarly for $2 R _ { \mathrm { i } }$

![](images/367cee98a6ea94f2cb7a40dcc8f8c75099e925d680d3b248d234e5341d512120.jpg)
Fig.3.A schematic of the header with the notation used in the analysis, showing the negolyte outlet shunt currents as an example,but the contributions from posolyte and feed manifolds are understood to be combined.The currents in the bipolar plates $I _ { k }$ and the manifolds $i _ { k }$ add up to the net stack current $I = I _ { k } + i _ { k }$ . The inlet and outlet port currents (only outlet shown here, mind the slightly different typography) $i _ { \boldsymbol { k } } ^ { \prime }$ contribute to the manifold current: $i _ { k } ^ { \prime } = i _ { k } - i _ { k - 1 }$ ,where negative values imply current from the manifold into the cells.

Fig.3 shows the index $k = 1$ to $N$ we use to label the different cells in the direction of the main current $I _ { k } > 0$ .We will linearise the electrolyte voltage drop,between cells $k$ and $k + 1$ as

$$
\Delta \phi _ { k } \equiv \phi _ { k + 1 } - \phi _ { k } = V _ { \mathrm { l i n } } - I _ { k } R _ { \mathrm { l i n } }
$$

where the resistance $R _ { \mathrm { l i n } }$ can be chosen based on an empirical linearisation in the relevant current range; see Eq. (B.7).As schematically depicted in Fig. B.7, $V _ { \mathrm { l i n } } < 0$ for an electrolytic cell,like an electrolyser ora charging flow battery.In this case,a larger current makes the potential drop $\Delta \phi _ { k }$ more negative,increasing shunt currents.For a Galvanic cell,with a spontaneous electrochemical reaction as in a discharging flow battery, $V _ { \mathrm { l i n } } > 0$ .An increase in current thus decreases a positive potential drop $\Delta \phi _ { k }$ ,reducing shunt currents.In an electrochemical cell, the potential decreases continuously in the direction of the stack current.Between cells,however, the potential in a Galvanic stack increases due to the reaction's equilibrium potential; see Fig. B.7. In this case,shunt currents $i _ { k } < 0$ will be in the direction opposite the main current.

![](images/8f6a24bcd354e9e09d780f2fa13c7f7376122cea1bb1f0ae1a7e6a769481f49d.jpg)
Fig.4.A schematic depiction of shunt currents $i _ { k }$ in the manifold (horizontal, the black line is a continuous representation) and $i _ { k } ^ { \prime }$ into/out of the cells (vertical,the grey line is a continuous approximation) in case the port resistance $R _ { \mathrm { i o } }$ can be neglected (top),the manifold resistance $R _ { \mathrm { m n } }$ can be neglected (middle) and when neither of these resistances is negligible (bottom).

Appendix B elaborates on how the voltage drop in Eq.(3) relates to the cell potential, measured between electrodes. The linearised voltage $V _ { \mathrm { l i n } }$ may be chosen significantly different from the equilibrium voltage, to account for reaction overpotentials.

# 2.2. Negligibleinlet/outlet portresistance $R _ { \mathrm { i o } } \ll R _ { \mathrm { m n } }$

First,we consider what shunt currents to expect if we can neglect the inlet/outlet port resistance $R _ { \mathrm { i o } } ~ \approx ~ 0$ and the main resistance to shunt currents is $R _ { \mathrm { m n } }$ in the manifold.This may be a relevant limit for some particular cell designs,such as the Sapporo cell or a similar design by Alcoa for industrial applications in the Hall-Héroult process of aluminium smelting.In this case,schematically depicted in Fig. 4(top),all shunt currents will flow between the first and last cells,since there is no potential drop associated with leaving or entering the cells. Because of this,the voltage drops in the manifold will be equal to those $\Delta \phi _ { k }$ between cell.Therefore,Ohm's law gives $\begin{array} { r } { i _ { k } = - \frac { \varDelta \phi _ { k } } { R _ { \mathrm { m n } } } } \end{array}$ and the shunt current in the manifold is everywhere equal to its average value:

$$
i _ { \mathrm { a v } } \equiv \frac { 1 } { N - 1 } \sum _ { k = 1 } ^ { N - 1 } i _ { k } = \frac { - \varDelta \phi _ { \mathrm { a v } } } { R _ { \mathrm { m n } } }
$$

Because there are $N { - } 1$ manifold segments between $N$ cells, the average potential drop over the electrolyte between two adjacent cells is $\Delta \phi _ { \mathrm { a v } } \equiv$ $\frac { \mathbf { \dot { \phi } } _ { N } - \phi _ { 1 } } { N - 1 }$

The cell current through the end-plates is the net stack current $I$ ,but the current through the bipolar plates and the rest of the cells is $I - i _ { \mathrm { a v } }$ Therefore, from Eq. (3) we have $\Delta \phi _ { \mathrm { a v } } = V _ { \mathrm { l i n } } - R _ { \mathrm { l i n } } \left( I - i _ { \mathrm { a v } } \right)$ .Inserting into Eq. (4) and solving for $i _ { \mathrm { a v } }$ gives $i _ { \mathrm { a v } } = i _ { \mathrm { m a x } } .$ ，the maximum average shunt current which occurs for negligible inlet/outlet resistance,where

$$
i _ { \mathrm { m a x } } \equiv \frac { - { \cal A } \phi _ { 0 } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } } \mathrm { a n d } { \cal A } \phi _ { 0 } \equiv V _ { \mathrm { l i n } } - I R _ { \mathrm { l i n } }
$$

Here $\varDelta \phi _ { 0 }$ is the maximum electrolyte voltage drop,obtained in the absence of shunt currents.In Eq.(5), it seems as if the two resistances $R _ { \mathrm { m n } }$ and $R _ { \mathrm { l i n } }$ act in series. However, $R _ { \mathrm { l i n } }$ appears here only due to the decrease in voltage that arises as current bypasses cells.Not because shunt current passes through the membrane,which it does as illustrated in Fig.2.But this resistance we included in $R _ { \mathrm { i o } }$ as shown in Eq. (1).

The simple and insightful result of Eq.(5) is not too often found in papers on shunt currents. However, see for example equation eight of Ref.[43] where it is attributed to Ishikawa and Kondo [1O9]. Or see Ref.[46],where it is obtained in the limit $N \to \infty$ and $V _ { \mathrm { l i n } } = 0$ ,in the context of electrodialysis.

# 2.3.Negligible manifold resistance $R _ { \mathrm { m n } } \ll R _ { \mathrm { i o } }$

In case of negligible resistance in the manifold $( R _ { \mathrm { m n } } \approx 0 )$ ,the entire manifold has the same voltage.Since we assume equal properties for each cell, there exists a symmetry with respect to the mid-plane of the stack.In case of an odd number of cells $N$ ,the N+1-th cell is exactly in the middle and has no shunt current flowing into or out of its cell into the manifold. This means that the potential in this cell will be the same as in the manifold: $\phi _ { \mathrm { m n } } = \phi _ { \frac { N + 1 } { \gamma } }$ .Therefore,the shunt current leaving, or entering in case $i _ { k } ^ { \prime } < 0$ ,the $k$ -the cell into the manifold is

$$
i _ { k } ^ { \prime } \approx \frac { \phi _ { k } - \phi _ { \mathrm { m n } } } { R _ { \mathrm { i o } } } = \frac { \Delta \phi _ { \mathrm { a v } } } { R _ { \mathrm { i o } } } \left( \frac { N + 1 } { 2 } - k \right)
$$

where we approximated $\phi _ { k } \approx \phi _ { 1 } + ( k - 1 ) \Delta \phi _ { \mathrm { a v } }$ assuming small enough shunt currents to have equal voltage differences between all cells.Now the shunt current $i _ { k }$ in the manifold between cell $k$ and $k + 1$ is obtained by summing all the contributions from the inlet/outlet ports,to give

$$
i _ { k } = \sum _ { k ^ { \prime } = 1 } ^ { k } i _ { k ^ { \prime } } ^ { \prime } = \frac { - \varDelta \phi _ { \mathrm { a v } } } { R _ { \mathrm { i o } } } \frac { k ( N - k ) } { 2 }
$$

obae $\begin{array} { r } { \sum _ { k ^ { \prime } = 1 } ^ { k } k ^ { \prime } = k \frac { k + 1 } { \gamma } } \end{array}$ Using this ga $\begin{array} { r } { \sum _ { k = 1 } ^ { N } k ^ { 2 } = \frac { { \bf \bar { \Phi } } _ { N ( N + 1 ) ( 2 N + 1 ) } } { 6 } } \end{array}$ the average shunt current $\begin{array} { r } { i _ { \mathrm { a v } } = \frac { 1 } { N - 1 } \sum _ { k = 1 } ^ { N - 1 } i _ { k } } \end{array}$ is obtained as

$$
i _ { \mathrm { a v } } = \frac { - \Delta \phi _ { \mathrm { a v } } } { 1 2 R _ { \mathrm { i o } } } N \left( N + 1 \right)
$$

This resultl first appears in the western literature in Ref.[39],followed by the mistaken derivation of Ref.[2O],while according to Ref.[27] a book [41] from 1933 already contains this result.While its validity is limited by the assumptions used,which are usually not warranted, Refs.[21,4O] nonetheless made use of this result in describing shunt currents.With $\Delta \phi _ { \mathrm { a v } } = V _ { \mathrm { l i n } } - R _ { \mathrm { l i n } } \left( I - i _ { \mathrm { a v } } \right)$ Eq. (8) gives

$$
i _ { \mathrm { a v } } = \frac { - \Delta \phi _ { 0 } } { R _ { \mathrm { l i n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } }
$$

# 2.4. Combined approximation

The limits of Eqs.(4)and (8) individually have limited applicability as they both neglect one of the main resistances to shunt currents. There is,however,an obvious way to generalise both limits,by simply adding the resistances in series to give

$$
i _ { \mathrm { a v } } \approx \frac { - \Delta \phi _ { \mathrm { a v } } } { R _ { \mathrm { m n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } }
$$

This simple approximation expresses that shunt currents are determined by the manifold and port resistances in series,but not before multiplying the latter by $1 2 / ( N ( N + 1 ) )$ .This naturally leads to a hypothesis on how to approximately consider several manifolds in parallel, by replacing

$$
\frac { 1 } { R _ { \mathrm { m n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } } \approx \sum \frac { 1 } { R _ { \mathrm { f e e d / r e t u r n } } + \frac { 1 2 R _ { \mathrm { i n / o u t } } } { N ( N + 1 ) } }
$$

where the sum runs over all feed and return manifolds with their respective inlet and outlet ports.

In (10), $\begin{array} { r } { \Delta \phi _ { \mathrm { a v } } = V _ { \mathrm { l i n } } - ( I - i _ { \mathrm { a v } } ) R _ { \mathrm { l i n } } } \end{array}$ depends on $i _ { \mathrm { a v } }$ , so this is an implicit equation. It can be written in terms of the known stack current $I$ ,with $\Delta \phi _ { 0 } = V _ { \mathrm { l i n } } - I R _ { \mathrm { l i n } }$ to

$$
i _ { \mathrm { a v } } \approx \frac { - \varDelta \phi _ { 0 } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } }
$$

This reduces to the limit of Eq.(5) in case of negligible input/outlet resistance $R _ { \mathrm { i o } }$ and to Eq.(9),when the sum of manifold and cell resistances $R _ { \mathrm { m n } }$ is negligible.At this point,Eqs.(lO) and(l2） are unsubstantiated.In the following subsection,we will compare these heuristic approximations to the exact analytical solution,to test their accuracy.

# 2.5.Exact analytical solution

In the appendix,we derived the exact result for the shunt current distribution

$$
\frac { i _ { k } } { i _ { \operatorname* { m a x } } } = 1 - \frac { \cosh \left( \mathbf { M } \left( 1 - \frac { 2 k } { N } \right) \right) } { \cosh \left( \mathbf { M } \right) }
$$

where $i _ { \mathrm { m a x } }$ was defined in Eq. (5), and

$$
\mathbf { M } = \frac { N \ln \left( \frac { 2 \bar { R } _ { \mathrm { i o } } } { 1 + 2 \bar { R } _ { \mathrm { i o } } - \sqrt { 1 + 4 \bar { R } _ { \mathrm { i o } } } } \right) } { 2 } \approx \left\{ \begin{array} { l l } { \frac { N } { 2 \sqrt { \bar { R } _ { \mathrm { i o } } } } } & { \bar { R } _ { \mathrm { i o } } \gg 1 } \\ { \frac { N } { 2 } \ln \left( \frac { 1 } { \bar { R } _ { \mathrm { i o } } } \right) } & { \bar { R } _ { \mathrm { i o } } \ll 1 } \end{array} \right.
$$

in terms of the dimensionless inlet/outlet resistance

$$
\bar { R } _ { \mathrm { i o } } \equiv \frac { R _ { \mathrm { i o } } } { R _ { \mathrm { l i n } } + R _ { \mathrm { m n } } }
$$

This is an exact solution that can serve as a benchmark for checking numerical codes.It was first obtained in Ref.[42],with a likely typographical error that Eq.(14) corrects. See also Ref.[47,48] for an application to batteries.In the limit $\bar { R } _ { \mathrm { i o } } \gg 1$ this solution tends to the approximate result of Refs.[23,26,27,30-33],obtained by treating the cell index $k$ as a continuous variable.In Fig.5 we compare this limit with the exact result, showing only an appreciable difference for small $N$ and $\bar { R } _ { \mathrm { i o } }$

We introduce the relative difference between the average and maximum shunt current per cell,or the stack's ‘effectiveness factor',as

$$
\mathcal { E } \equiv \frac { i _ { \mathrm { m a x } } - \frac { N - 1 } { N } i _ { \mathrm { a v } } } { i _ { \mathrm { m a x } } } \ s _ { 0 } \ \frac { i _ { \mathrm { a v } } } { i _ { \mathrm { m a x } } } = \frac { N \left( 1 - \mathcal { E } \right) } { N - 1 }
$$

Here $\begin{array} { r } { \frac { N - 1 } { N } i _ { \mathrm { a v } } \ = \ \frac { 1 } { N } \sum _ { k = 1 } ^ { N - 1 } i _ { k } } \end{array}$ ishe per segment between the cells.This makes for a non-zero

![](images/1883f12de6b035cb2ca25a58996792c254093df93bef8a846ea500bcc45bbf9f.jpg)
Fig.5.The dimensionless average shunt current $\begin{array} { r } { \frac { i _ { \mathrm { a v } } } { i _ { \mathrm { m a x } } } = \frac { N } { N - 1 } \left( 1 - \mathcal { E } \right) } \end{array}$ for $N = 1 0$ and $N = 1 0 0$ comparing the exact result of Eq.(l7) (black),the top limit Eq. (14) for $\bar { R } _ { \mathrm { i o } } \gg 1$ (grey)and the approximation of Eq.(l8)(blue).This approximation gives Eq.(l2) and overestimates the shunt currents by at most $^ { 1 3 \% }$ when ${ \bar { R } } _ { \mathrm { i o } }$ is of the order of $N ( N + 1 ) / 1 2$ .(For interpretation of the references to colour in this figure legend,the reader is referred to the web version of this article.)

in case $i _ { \mathrm { a v } } = i _ { \mathrm { m a x } }$ ，since shunt currents do originate and terminate in one of the stack's cells.A higher effectiveness factor closer to one is desirable,as in this case,less current bypasses.Additionally,ideally, also $i _ { \mathrm { m a x } }$ should be small compared to $I$ ,but that is considered in the Faradaic efficiency that we will introduce shortly in Section 3.1.From the analytical solution of Eq.(l3),we derive in the appendix :

$$
\mathcal { E } = \frac { \operatorname { t a n h } { ( \mathbf { M } ) } } { N \operatorname { t a n h } { ( \mathbf { M } / N ) } } \approx \left\{ \begin{array} { l l } { \frac { 1 } { N } } & { \mathbf { M } \gg N } \\ { \frac { \operatorname { t a n h } { ( \mathbf { M } ) } } { \mathbf { M } } } & { \mathbf { M } \ll N } \end{array} \right.
$$

The bottom approximation of Eq.(l7） is equal to the effectiveness factor expression for a catalyst layer or porous electrode [1lo,111], where $\mathbf { M }$ is referred to as the Thiele modulus.2

From Eq.(l3)we can see that for large values of $N / 2 \bf { M } \approx 1 / \ln { ( \bar { R } _ { \mathrm { i o } } ) }$ acts as a penetration depth indicating the number of cells near the edges over which the shunt current builds up to $1 - \mathsf { e } ^ { - 1 } \approx 6 3 \%$ of its maximum $i _ { \mathrm { m a x } }$ .Such a profile is schematically illustrated in Fig.4 (bottom).

For $\mathbf M \ll 1$ ,a leading order expansion of Eqs.(16) and (17) gives $i _ { \mathrm { a v } } / i _ { \mathrm { m a x } } ~ \approx ~ ( N + 1 ) { \bf M } ^ { 2 } / 3 N ~ \approx ~ N ( N + 1 ) / 1 2 \bar { R } _ { \mathrm { i o } }$ .On the other hand,if $\mathbf M \gg N$ it tends to unity.A simple expression that respects both these limits is

$$
\frac { i _ { \mathrm { a v } } } { i _ { \mathrm { m a x } } } \approx \frac { 1 } { 1 + \frac { 1 2 \bar { R } _ { \mathrm { i o } } } { N ( N + 1 ) } }
$$

which is exactly our earlier hypothesised Eq. (l2).As illustrated in Fig. 5,it approximates the exact result very well,and the relative error with the exact solution never exceeds $^ { 1 3 \% }$ .So,for the simplified case of a linear voltage current relationship and constant resistances,we now have the insightful exact analytical solution of Eqs.(l6) and (17),but also the arguably even more insightful as well as simple and accurate approximation in Eq.(l2).Note from Eq.(l8) that it is the magnitude of $1 2 \bar { R } _ { \mathrm { i o } } / N ( N + 1 )$ rather than $\bar { R } _ { \mathrm { i o } }$ that determines whether the port resistance is significant. So, even when $R _ { \mathrm { i o } } \gg R _ { \mathrm { m n } }$ ,the port resistance can still be negligible when $N$ is sufficiently large.

In the next section,we will define several performance criteria for an electrolyser stack and use the exact and approximate expressions to analyse the influence of shunt currents.

# 3.Performance criteria

# 3.1. Faradaic efficiency

The Faradaic efficiency $\varphi _ { \mathrm { F E } }$ is the fraction of the total current that is usefully deployed. It is also sometimes referred to as Faraday efficiency or yield,current efficiency,or coulombic efficiency,each of which may have slightly different meanings depending on the context.Here,we assume there are no unwanted side reactions and consider only the influence of shunt currents.

In an electrolyser,or other stack of electrolytic cells,we define the Faradaic efficiency as the average main current divided by the stack current $I$ .This gives the ratio of the realised amount of product to the ideally produced amount of product in the absence of shunt currents:

$$
\varphi _ { \mathrm { F E } } \equiv \frac { \sum _ { k = 1 } ^ { N } I _ { k } } { N I } = 1 - \frac { N - 1 } { N } \frac { i _ { \mathrm { a v } } } { I } = 1 - \frac { i _ { \mathrm { m a x } } } { I } \left( 1 - \mathcal { E } \right)
$$

where we used that the main current $I _ { k }$ and the shunt current $i _ { k }$ alwaysadd uptothestackcurrnt $I$ (Eq.(A.1)) to write $\begin{array} { r } { \sum _ { k = 1 } ^ { N } I _ { k } \ = } \end{array}$ $N I - ( N - 1 ) i _ { \mathrm { a v } }$ .The appearance of the factor $( N - 1 ) / N$ may also be appreciated by the observation that each ion is produced and consumed in a useful redox reaction in a cell,but in the rest of the $N - 1$ cells, the average useful stack current is reduced to $I - i _ { \mathrm { a v } }$

The definition in Eq. (19) is used in e.g. Refs.[42,43,109]. Several other references, for example Refs. [39,56,91] introduce the quantity $1 - \frac { i _ { \mathrm { a v } } } { I }$ ,only equal to our definition of Faradaic efficiency in case $N \gg 1$ Note from Eq.(19) that to obtain a high Faradaic efficiency requires the product of $i _ { \mathrm { m a x } } / I$ and $1 - \mathcal { E }$ to be small.Either of the two can,when small enough,ensure a high efficiency. These two options correspond roughly to having either a high enough manifold resistance or a high enough port resistance.

Inserting the approximation of Eq.(12) into Eq. (19) gives

$$
\varphi _ { \mathrm { F E } } \approx 1 - \frac { N - 1 } { N } \frac { R _ { \mathrm { l i n } } - V _ { \mathrm { l i n } } / I } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } }
$$

This shows how at large current densities, $\varphi _ { \mathrm { F E } }$ primarily depends on the various resistances.At low current densities $R _ { \mathrm { l i n } }$ will be small compared to $V _ { \mathrm { l i n } } / I$ .To ensure a high Faradaic efficiency,assuming $N \gg 1$ ，the current has to satisfy at least

$$
I \gg \frac { - V _ { \mathrm { l i n } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ^ { 2 } } }
$$

This provides a practical operational limit imposed by shunt currents, to avoid operating electrolysers very ineficiently.

A more dramatic electrolyser malfunction,particularly relevant when operating under variable loads,occurs if all the current $I$ leaves the first cell, bypasses the $N - 1$ cells in between,and enters the final cell.Conservatively,to avoid this the potential drop for all the current bypassing $I \left( ( N - 1 ) R _ { \mathrm { m n } } + 2 R _ { \mathrm { i o } } \right)$ has to be smaller than roughly $N - 1$ times $- \varDelta \phi _ { 0 }$ .With Eq. (5),this gives for the minimum current

$$
I \gtrsim \frac { - V _ { \mathrm { l i n } } } { R _ { \mathrm { m n } } - R _ { \mathrm { l i n } } + \frac { 2 R _ { \mathrm { i o } } } { N - 1 } }
$$

Mind,upon comparing with Eq.(21） in the denominator,the minus sign of the second term and the different third term. Therefore,Eq. (22) may be harder to satisfy than Eq.(21),which therefore provides a more stringent current minimum for electrolysers.

At high currents,the best protection against a low Faradaic electrolyser efficiency, from Eq. (2O),is to have

$$
R _ { \mathrm { m n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } \gg R _ { \mathrm { l i n } }
$$

It will be interesting to know how to design an electrolyser such that this is the case.Therefore,we provide rough order-of-magnitude estimates.Typically, $R _ { \mathrm { l i n } } \sim 1 \ \Omega \ \mathrm { c m } ^ { 2 }$ and the conductivity of most used liquid electrolytes $\kappa \sim \Omega ^ { - 1 } / \mathrm { c m }$ .Pouillet's law Eq.(2) then requires $A _ { \mathrm { m n } } / l _ { \mathrm { m n } } \ll \mathrm { c m } ^ { - 1 }$ ,to have $R _ { \mathrm { m n } } \gg R _ { \mathrm { l i n } }$ .With a stack pitch $l _ { \mathrm { m n } }$ of the orderof $^ { 1 \mathrm { \ c m } }$ ,the cross-sectional area of the manifold has to be much less than $1 \ \mathrm { c m } ^ { 2 }$ ，or even smaller when taking into account several parallel pathways. Such small manifolds may be challenging in gasproducing electrolysers or in flow batteries,which require high flow rates.Therefore,in this case,the second term in Eq.(23) may be needed,which limits the number of cells to

$$
N \lesssim \sqrt { R _ { \mathrm { i o } } / R _ { \mathrm { l i n } } }
$$

Assuming the largest contribution to $R _ { \mathrm { i o } }$ in Eq.(1) comes from the cell inlet/outlet ports,this implies,with the above assumptions,that $N ~ \lesssim ~ \sqrt { 1 ~ \mathrm { c m } \times l _ { \mathrm { i o } } / A _ { \mathrm { i o } } }$ With $l _ { \mathrm { i o } } ~ = ~ 1 ~ \mathrm { c m }$ and a small outlet area of $A _ { \mathrm { i o } } = 1 ~ \mathrm { m m } ^ { 2 }$ limits $N \lesssim 1 0$ To allow $N \sim 1 0 0$ then requires very long inlets/outlets of $l _ { \mathrm { i o } } \sim 1 \ \mathrm { m }$ or,sub-millimetre outlet diameters which incur large pressure drops.With these rough estimates,it is clear that shunt currents provide a significant design challenge and that a large number of cells require either very long and narrow inlet and outlet ports or manifolds or require other smarter solutions.

In a stack of Galvanic cells, ${ i _ { \mathrm { a v } } < 0 }$ ， so Eq. (19) gives values of $\varphi _ { \mathrm { F E } }$ above1.Therefore,ina galvanic stack $\varphi _ { \mathrm { F E } }$ is perhaps not so useful as an efficiency.However,we maintain the same definition as a useful placeholder.

# 3.2. Stack voltage

The full stack current $I$ undergoes redox reactions at terminating half cells,and only in between these cells do shunt currents arise. Therefore,as is also illustrated in Fig.B.7, the stack voltage is approximately once the voltage $\varDelta \phi _ { 0 }$ associated with the net stack current $I$ and $N - 1$ times $\Delta \phi _ { \mathrm { a v } } \equiv V _ { \mathrm { l i n } } - ( I - i _ { \mathrm { a v } } ) R _ { \mathrm { l i n } } = \Delta \phi _ { 0 } + i _ { \mathrm { a v } } R _ { \mathrm { l i n } } .$ s0

$$
\frac { V _ { \mathrm { s t a c k } } } { N } = A \phi _ { 0 } + \frac { N - 1 } { N } i _ { \mathrm { a v } } R _ { \mathrm { l i n } } = V _ { \mathrm { l i n } } - \varphi _ { \mathrm { F E } } I R _ { \mathrm { l i n } }
$$

The final expression follows from inserting Eq.(19).It shows that shunt currents do not contribute to the cell voltage losses.They reduce the absolute value of the stack voltage by making the electrolyser stack voltage less negative or the Galvanic stack voltage less positive.

What is usually known is the stack voltage.From Eq.(25) we have $\begin{array} { r } { \Delta \phi _ { \mathrm { a v } } = \frac { V _ { \mathrm { s t a c k } } + i _ { \mathrm { a v } } R _ { \mathrm { l i n } } } { N } } \end{array}$ ,so we can writeEq.(10)also as

$$
i _ { \mathrm { a v } } \approx \frac { - V _ { \mathrm { s t a c k } } / N } { R _ { \mathrm { m n } } + \frac { R _ { \mathrm { l i n } } } { N } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } }
$$

Here $R _ { \mathrm { l i n } }$ re-appears,as in Eq. (l2),however this time divided by $N$ .As discussed before,it does not act as a resistance to shunt currents; rather, it describes the voltage change as shunt currents arise.In Eq.(26),most of this effect is taken into account by the numerator.

Eq.(25） shows how shunt currents change the current-voltage relationship at the stack level.However, because $\varphi _ { \mathrm { F E } }$ depends on $I$ this is still an implicit relation. Inserting into $\begin{array} { r } { \varphi _ { \mathrm { F E } } = 1 - \frac { i _ { \mathrm { m a x } } } { I } ( 1 - \mathcal { E } ) } \end{array}$ from Eq (16) gives with $\begin{array} { r } { i _ { \operatorname* { m a x } } = - \frac { V _ { \mathrm { l i n } } - I R _ { \mathrm { l i n } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } } } \end{array}$ that

$$
\frac { V _ { \mathrm { s t a c k } } } { N } = \left( V _ { \mathrm { l i n } } - I R _ { \mathrm { l i n } } \right) ( 1 - \zeta )
$$

where $\begin{array} { r } { \zeta \equiv \frac { R _ { \mathrm { l i n } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } } \left( 1 - \mathcal { E } \right) = \frac { R _ { \mathrm { l i n } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } } \frac { N - 1 } { N } \frac { i _ { \mathrm { a v } } } { i _ { \mathrm { m a x } } } } \end{array}$ . Using the approximation of Eq. (26) gives,after some algebra

$$
\zeta \approx \frac { \frac { N - 1 } { N } R _ { \mathrm { l i n } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } }
$$

which only depends on stack design parameters.This parameter was introduced in Ref.[47] as $\xi$ and written as $\zeta$ in a subsequent paper [48]. So,independent of current density,the entire stack voltage will be lower bya factor $1 - \zeta$ to the value $N \varDelta \phi _ { 0 }$ that is expected in the absence of shunt currents.If the cell resistance is not much smaller than the shunt-current resistance, the stack voltage magnitude may drop below $N | V _ { \mathrm { l i n } } |$ .While foran electrolyser this may seem beneficial,the Faradaic efficiency will suffer as is clear from Eq.(20).

# 3.3. Energy efficiency

In anelectrolyser,the stack energy efficiency is defined by the ratio of the usefully deployed power,given by the useful current $\varphi _ { \mathrm { F E } } N I > 0$ times the equilibrium voltage,or the thermoneutral voltage $V _ { \mathrm { t n } } ~ < ~ 0$ ， divided by the total electrochemically consumed power $I V _ { \mathrm { s t a c k } } ~ < ~ 0$ ， giving

$$
\varphi _ { \mathrm { E E , e l } } \equiv \frac { \varphi _ { \mathrm { F E } } V _ { \mathrm { t n } } } { V _ { \mathrm { s t a c k } } / N } = \frac { \varphi _ { \mathrm { F E } } V _ { \mathrm { t n } } } { V _ { \mathrm { l i n } } - \varphi _ { \mathrm { F E } } I R _ { \mathrm { l i n } } }
$$

where both numerator and denominator are negative,to give a positive value.An increase in Faradaic efficiency $\varphi _ { \mathrm { F E } }$ thus changes the energy efficiency of an electrolyser in two ways: it increases the useful current but also the voltage losses. However,the overall effect on the energy efficiency is always positive. In case of negligible $| V _ { \mathrm { l i n } } | \ll I R _ { \mathrm { l i n } }$ ,as may be the case for example in some electrodialysis or capacitive deionisation stacks,the energy efficiency $\varphi _ { \mathrm { E E , e l } } \approx - V _ { \mathrm { t n } } / I R _ { \mathrm { l i n } }$ becomes inversely proportional to the current density,independent of the Faradaic efficiency: the positive effect of an increase in $\varphi _ { \mathrm { F E } }$ of on the useful current is offset by the negative efect of an increase in the stack voltage.

When a high energy efficiency is desired,ideally $V _ { \mathrm { l i n } } ~ \gg ~ I R _ { \mathrm { l i n } }$ so, from Eq. (29), $\varphi _ { \mathrm { E E , e l } } ~ \approx ~ \varphi _ { \mathrm { F E } } ( V _ { \mathrm { t n } } / V _ { \mathrm { l i n } } )$ and optimising for energy efficiency is the same as optimising the Faradaic eficiency.To ensure a high efficiency,then also requires at least Eq.(21) to be satisfied.

In a discharging flow battery or liquid-electrolyte fuel cell,the energy efficiency is given by the stack power $I V _ { \mathrm { s t a c k } } > 0$ divided by the power produced electrochemically,which is the total current $N I \varphi _ { \mathrm { F E } }$ times the equilibrium voltage $V _ { \mathrm { e q } } > 0$ s0

$$
\varphi _ { \mathrm { E E , b a t } } \equiv \frac { V _ { \mathrm { s t a c k } } / N } { V _ { \mathrm { e q } } \varphi _ { \mathrm { F E } } } = \frac { V _ { \mathrm { l i n } } - \varphi _ { \mathrm { F E } } I R _ { \mathrm { l i n } } } { V _ { \mathrm { e q } } \varphi _ { \mathrm { F E } } }
$$

Note that this the inverse of Eq. (29): $\varphi _ { \mathrm { E E , b a t } } = 1 / \varphi _ { \mathrm { E E , e l } }$ but the definition of $\varphi _ { \mathrm { F E } }$ is different.In the case of a Galvanic stack, $V _ { \mathrm { l i n } } > 0$ and shunt currents make $\varphi _ { \mathrm { F E } } > 1$ ,so they decrease the stack voltage in the numerator and also increase the electrochemically consumed power in the denominator,both decreasing the energy efficiency.

# 3.4.Self-discharge of a redox flow battery

Attaching a fuel cell or battery load with resistance $R _ { \mathrm { l o a d } }$ we have $V _ { \mathrm { s t a c k } } = I R _ { \mathrm { l o a d } }$ ,and solving Eq.(27) for the current gives

$$
I = \frac { V _ { \mathrm { l i n } } } { R _ { \mathrm { l i n } } + \frac { R _ { \mathrm { l o a d } } } { N ( 1 - \zeta ) } }
$$

The useful battery power $P \ = \ I V _ { \mathrm { s t a c k } } \ = \ I ^ { 2 } R _ { \mathrm { l o a d } }$ is maximised with respect to the load when ${ \partial P } / { \partial R _ { \mathrm { l o a d } } } = 0$ ,which gives $R _ { \mathrm { l o a d } } = N R _ { \mathrm { l i n } } ( 1 { - } \zeta )$ Without shunt currents, $\zeta = 0$ and we obtain the well-known result that the power is maximised when the external load $R _ { \mathrm { l o a d } }$ equals the internal resistance $N R _ { \mathrm { l i n } }$ .However,in the presence of shunt currents, the highest power is obtained fora load that is $1 - \zeta$ times smaller,as was already shown in Ref.[48].

It may be useful to know how the energy efficiency of Eq (30) depends on the battery load.From Eqs.(5)，(19) and the definition of $\zeta$ below Eq. (27), gives $\begin{array} { r } { \varphi _ { \mathrm { F E } } = 1 + \zeta \frac { \bar { V } _ { \mathrm { l i n } } - I R _ { \mathrm { l i n } } } { I R _ { \mathrm { l i n } } } } \end{array}$ . Inserting Eq. (31) gives $\begin{array} { r } { \varphi _ { \mathrm { F E } } = 1 + \frac { \zeta } { 1 - \zeta } \frac { R _ { \mathrm { l o a d } } } { N R _ { \mathrm { l i n } } } } \end{array}$

$$
\varphi _ { \mathrm { E E , b a t } } = \frac { V _ { \mathrm { l i n } } } { V _ { \mathrm { e q } } } \frac { 1 - \zeta } { \left( 1 + \frac { \zeta } { 1 - \zeta } \frac { R _ { \mathrm { l o a d } } } { N R _ { \mathrm { l i n } } } \right) \left( 1 + \frac { N ( 1 - \zeta ) R _ { \mathrm { l i n } } } { R _ { \mathrm { l o a d } } } \right) }
$$

This can be optimised analytically by solving $\partial \varphi _ { \mathrm { E E , b a t } } / \partial R _ { \mathrm { l o a d } } = 0$ to give $\begin{array} { r } { R _ { \mathrm { l o a d } } \ = \ \frac { 1 - \zeta } { \sqrt { \zeta } } N R _ { \mathrm { l i n } } . } \end{array}$ aresultalsopreviouslyobaiedinRe.48]. Without shunt currents $( \zeta = 0 )$ the load should beas high as possible, so the battery current is as small as possible,to obtain the highest energy efficiency.However, shunt currents will drain the battery slowly so that an optimal energy efficiency is obtained at a finite current,obtained by inserting the optimal load in Eq.(31) to give

$$
{ I _ { \mathrm { o p t } } = \frac { V _ { \mathrm { l i n } } } { R _ { \mathrm { l i n } } \left( 1 / \sqrt { \zeta } + 1 \right) } }
$$

# 3.5.Side-reactions in manifolds

When the voltage differences inside the manifold increase beyond a certain voltage threshold,certain side-reactions may occur. These can lead to unwanted corrosion,but the reaction products can also contaminate the desired products or pose safety risks.For example,for voltage differences exceeding $1 . 2 3 \mathrm { V }$ ,aqueous electrolytes can undergo water splitting，potentially leading to explosive mixtures.Ref.[97] shows an experimental result from Ref.[113] in which a metallic foil in a brine performs hydrogen evolution on one side and chloride evolution on the other,without being connected to an outside circuit, demonstrating that this is not necessary.Electrons only have to be able to travel through the metal,and there has to be a sufficient potential over the electrolyte along the metal.

Self-consistently describing this requires including at leasta decomposition potential and resistances in parallel to the manifold,as was done in Ref.[98] in the limit of a continuous cell index,or considered in Ref.[1l4].Here,we will only evaluate the conditions under which this could arise.

Multiplying $i _ { k }$ from Eq.(13) with $R _ { \mathrm { m n } }$ and summing gives the potentialdropoverthemanifoldas $\begin{array} { r } { \Delta \phi _ { \mathrm { m n } } ^ { - - 1 } = R _ { \mathrm { m n } } \sum _ { k } ^ { N - 1 } i _ { k } = ( N - 1 ) \sum _ { k } ^ { N - 1 } i _ { k } . } \end{array}$ $1 ) i _ { \mathrm { a v } } R _ { \mathrm { m n } }$ . Inserting our approximate Eq. (l2), this gives

$$
\Delta \phi _ { \mathrm { m n } } \approx \frac { - ( N - 1 ) R _ { \mathrm { m n } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } } { \Delta \phi _ { 0 } }
$$

If this potential difference exceeds the onset potential of corrosion reactions,or e.g.water splitting,ionic shunt currents may switch to electronic shunt currents through the conducting manifold. Assuming this onset potential is similar in magnitude to $\varDelta \phi _ { 0 }$ ，avoiding this requires $\begin{array} { r l r } {  { \Delta \phi _ { \mathrm { m n } } \lesssim - \Delta \phi _ { 0 } } } \end{array}$ ,which gives

$$
( N - 2 ) R _ { \mathrm { m n } } \lesssim R _ { \mathrm { l i n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) }
$$

So,avoiding currents through metallic manifolds imposes a limit on the number of cells, $N$ .Note that Eq. (35),which is more easily satisfied for low manifold resistance $R _ { \mathrm { m n } }$ ,contrasts with Eq. (23),which shows that a high value helps to achieve a high efficiency.

There are at least two ways out of these conflicting design criteria. One is to rely on a high inlet/outlet resistance so $R _ { \mathrm { i o } } \gtrsim ( N - 2 ) ( N ^ { 2 } -$ $1 ) R _ { \mathrm { m n } } / 1 2$ and $R _ { \mathrm { i o } } \gg N ( N + 1 ) R _ { \mathrm { l i n } } / 1 2$ ,to satisfy both (35) and Eq. (23). This will become increasingly difficult as the number of cells per stack, $N$ ,increases.Alternatively,non-conducting manifolds,such as polymers,may be used to prevent side reactions.This is indeed increasingly more common.

# 3.6. Summary

The above design considerations for a stack with a large number of cells $N \gg 1$ can be summarised as:

·Adesirable high energy eficiency requires a Faradaic efficiency close to 1, which from Eq. (20) requires $\begin{array} { r } { R _ { \mathrm { m n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ( N + 1 ) } } \end{array}$ to be much larger than both $R _ { \mathrm { l i n } }$ and $| V _ { \mathrm { l i n } } | / I$ .The latter condition provides a minimum current for efficient operation.

·The inlet/outlet ports thus only significantly contribute to mitigating shunt currents for stacks with a limited number of cells $N \lesssim \sqrt { R _ { \mathrm { i o } } / R _ { \mathrm { l i n } } }$ ·
·When the first condition in this list is satisfied, the current that optimises the energy efficiency of a fuel cell or a discharging flow battery is $\begin{array} { r } { I \approx \frac { V _ { \mathrm { l i n } } } { \sqrt { R _ { \mathrm { l i n } } \Big ( R _ { \mathrm { m n } } + \frac { 1 2 R _ { \mathrm { i 0 } } } { N ( N + 1 ) } \Big ) } } } \end{array}$ ,obtained from combining Eqs. (28) and (33).

Additionally,unless the port resistances can be made very large, nonconducting manifolds seem a required and appropriate design solution to avoid undesirable manifold-side reactions.

# 4. Conclusions

Assuming the linearised cell voltage of Eq. (3),we heuristically derived the average shunt current in the limits of negligible inlet/outlet resistance,Eq.(5),and negligible manifold resistance,Eq.(9). These limits can be conveniently combined in the form of Eq.(l2).Fig.5 shows this simple expression to be a reasonable approximation to the exact solution of Eq.(14),with a maximum relative error less than $^ { 1 3 \% }$ While the exact solution can be useful in verifying numerical solvers,or when more accuracy is required, this approximation suffices for many purposes.

In an electrolyser or charging flow battery,to avoid current bypassing cells and maintain a high Faradaic efficiency,Eqs.(21) and (22) show that the current should be sufficiently high,which is an important restriction for operation with variable loads as occur in combination with renewable energy sources.Additionally,to avoid significant shunt currents also at higher current densities,the summed manifold and inlet/outlet port resistances should far exceed the cell resistance,viz. Eq. (23).If the manifold resistance cannot be made much larger than the cell resistance,for example,to avoid side-reactions (viz. (35)), this gives a stringent condition,Eq.(24),on the maximum number of cells.

Inaliquid-electrolyte fuel cell or flow battery,the equations derived equally hold and show that the reverse currents are negative,which means they are in the direction opposite to the main current.Eq. (33) shows the current that optimises the energy efficiency,taking into account the effect of shunt currents.

By providing a simple yet accurate analytical model that easily allows calculation of stack voltage, efficiencies,and design limitations, valid for both galvanic and electrolytic stacks,we hope to bring some order to the vast body of knowledge on shunt currents.We resolved several subtleties and errors in this literature and brought together results from various subfields.By Pouillet's law,Eq.(2),the resistances used in the present equivalent circuit model can be related to geometrical design parameters,which therefore may be optimised for various applications.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Acknowledgements

I thank Bart de Rooij and Sohan Phadke for stimulating initial discussions on simplifying numerical equivalent circuit models.

$$
\begin{array} { r l } { k = 1 } & { 2 } \\ { \underset { \mathrm { | \overline { { \it { R _ { \mathrm { i } } \mathrm { o } } } } \mathrm { | \overline { { \it { 1 } } } _ { 1 } } \mathrm { | \overline { { \it { 1 } } } _ { 1 } } } } { \mathrm { | \overline { { \it { R _ { \mathrm { m n } } } } } \mathrm { ] } } } \frac { \mathrm { | \overline { { \it { R _ { \mathrm { m n } } } } } \mathrm { | \mathrm { \it { ~ 1 } } } \mathrm { | \it { R _ { \mathrm { m n } } } } \mathrm { \it { ~ 1 } } - } } { \mathrm { | \overline { { \it { R _ { \mathrm { m } } } } } \mathrm { \it { ~ 1 } } \mathrm { | \it { 1 } } _ { 2 } } \mathrm { | \it { 1 } } _ { 2 } } } &  \underset { \mathrm { | \overline { { \it { R _ { \mathrm { i } } \mathrm { o } } } } \mathrm { | \mathrm { | \it { 1 } } } \mathrm { | \it { 1 } } _ { \mathrm { i } } \mathrm { | \it { 1 } } _ { \mathrm { N } - 1 } } }  \mathrm { | \it { 1 } } _ { \mathrm { i } \mathrm { i } } \mathrm { | \it { 1 } } _ { \mathrm { i } } \mathrm { | \it { 1 } } _ { \mathrm { i } } \mathrm { | \it { 1 } } _ { \mathrm { i } } \mathrm { \it { 1 } } _ { \mathrm { i } } \mathrm { \it { 1 } } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } _ { \mathrm { i } } \mathrm { 1 } \end{array}
$$

Fig.A.6. The equivalent circuit model that Eq. (A.9) or,equivalently,Eq. (13) solves exactly.Note that we arbitrarily put the ground and a voltage $V _ { \mathrm { l i n } }$ (indicated by the two unequal-length parallel lines) on the left and an additional resistance on the right.This may differ for diferent shunt current paths,and we merely assume that they sum up to an additional $\Delta \phi _ { 0 } = V _ { \mathrm { l i n } } - I R _ { \mathrm { l i n } }$ in defining the stack voltage as in Eq. (25).

# Appendix A. Exact analytical solution

# A.1.Equivalent circuit model

We consider here the equivalent circuit of Eq.A.6,formalising the schematics of Figs.1,2,and 3.The currents $i _ { k } ^ { \prime }$ are positive in the direction out the cells into the manifold.An additional resistance $R _ { \mathrm { l i n } }$ and offset voltage $V _ { \mathrm { l i n } }$ are arbitrarily added the right and left, respectively,but could equally have been both on the left or the right.

Kirchhoff's first law, junction law,or current law,expresses conservation of charge,by demanding that in any closed loop along the circuit, the currents sum up to zero.Equivalently,the average current in any direction is constant.This means that the current through the bipolar plates, $I _ { k }$ ,and that through the manifold $i _ { k }$ adds up to the total current

$$
I = I _ { k } + i _ { k }
$$

Additionally,current conservation demands that the difference in current between two manifold segments comes from the cells:

$$
i _ { k } - i _ { k - 1 } = i _ { k } ^ { \prime }
$$

Kirchhoff's second law,loop rule,or voltage law expresses conservation of electrostatic energy by demanding that by traversing a closed loop,the potential change is zero.The potential difference between any two points should not depend on the path taken.The potential drop between two consecutive half-cells equals the potential drop following the shunt current out of the half cell and through a manifold section, back into the next half cell:

$$
\Delta \phi _ { k } \equiv \phi _ { k + 1 } - \phi _ { k } = - \left( R _ { \mathrm { i o } } i _ { k } ^ { \prime } + R _ { \mathrm { m n } } i _ { k } - R _ { \mathrm { i o } } i _ { k + 1 } ^ { \prime } \right)
$$

The minus sign on the final term results from following the path from manifold into cell $k + 1$ ，while we define currents $i ^ { \prime }$ as positive when going from the cell into the manifold.

Eqs. (3), (5) and (A.1) combine to $\Delta \phi _ { k } = \Delta \phi _ { 0 } + R _ { \mathrm { l i n } } i _ { k }$ . Using this in Eq. (A.3),along with Eq. (A.2), gives

$$
\begin{array} { r } { \Delta \phi _ { 0 } = R _ { \mathrm { i o } } \left( i _ { k - 1 } + i _ { k + 1 } - 2 i _ { k } \right) - \left( R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } \right) i _ { k } } \end{array}
$$

This linear recurrence relation describes the equivalent circuit of Eq.A.6,along with boundary conditions $i _ { 0 } = i _ { N } = 0$

# A.2. Continuous approximation

In several works in the literature,Eq. (A.4) is solved approximately by treating $k$ asa continuous rather than a discrete Variable.A Taylor expand up to second order then gives ik±1 \~ik±+.1 Inserting in Eq. (A.4) gives

$$
\varDelta \phi _ { 0 } = R _ { \mathrm { i o } } \frac { \mathrm { d } ^ { 2 } i _ { k } } { \mathrm { d } k ^ { 2 } } - \left( R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } \right) i _ { k }
$$

With the corresponding boundary conditions $i ( k = 0 ) = i ( k = N ) = 0$ ， this equation is solved by

$$
\frac { i _ { k } } { i _ { \mathrm { m a x } } } = 1 - \frac { \cosh \left( \frac { N / 2 - k } { \sqrt { \bar { R } _ { \mathrm { i o } } } } \right) } { \cosh \left( \frac { N / 2 } { \sqrt { \bar { R } _ { \mathrm { i o } } } } \right) }
$$

where Rio = $\begin{array} { r l } { \bar { R } _ { \mathrm { i o } } ~ \equiv ~ \frac { R _ { \mathrm { i o } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } } } & { { } } \end{array}$ . This solution seems to have been derived first in Ref.[27].As can be seen from Fig.5, the difference with the exact solution is very small.

# A.3.Exact solution

Eq. (A.4) can also be solved exactly. Similar to the way a constantcoefficient linear inhomogeneous second-order differential equation is solved,we first find the particular solution,which can easily be seen to be $i _ { \mathrm { m a x } } = - \Delta \phi _ { 0 } / \left( R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } \right) ,$ Inserting the trial solutions $x ^ { k }$ into the homogeneous version of Eq. (A.5),so without the left-hand side $\varDelta \phi _ { 0 }$ already taken care of by the particular solution,gives

$$
0 = R _ { \mathrm { i _ { 0 } } } \left( x ^ { k - 1 } + x ^ { k + 1 } - 2 x ^ { k } \right) - \left( R _ { \mathrm { l i n } } + R _ { \mathrm { m n } } \right) x ^ { k }
$$

Dividing by $x ^ { k - 1 }$ gives a quadratic equation for $x$ that is solved by

$$
x = \frac { 1 + 2 \bar { R } _ { \mathrm { i o } } - \sqrt { 1 + 4 \bar { R } _ { \mathrm { i o } } } } { 2 \bar { R } _ { \mathrm { i o } } }
$$

where Rio = $\begin{array} { r } { \bar { R } _ { \mathrm { i o } } \equiv \frac { R _ { \mathrm { i o } } } { R _ { \mathrm { m n } } + R _ { \mathrm { l i n } } } } \end{array}$ . A second solution is the same expression, but with a $^ +$ instead of a+-in the numerator,where we note that this solution is equal to $1 / x$ .Therefore,the full solution is the sum of the particular solution $i _ { \mathrm { m a x } }$ and a linear combination of $x ^ { k }$ and $x ^ { - k }$ ：

$$
{ \frac { i _ { k } } { i _ { \operatorname* { m a x } } } } = 1 - { \frac { x ^ { N - k } + x ^ { k } } { 1 + x ^ { N } } }
$$

which satisfies $i _ { 0 } = i _ { N } = 0$ .This exact analytical solution to Eq. (A.4) and the equivalent circuit of Fig.A.6 was first derived in Ref.[42]. However,Eq. (A.8)for $x$ seed to rad $\begin{array} { r } { b \left( \frac { 1 } { 2 } + \frac { 1 } { 4 } + b \right) ^ { - 2 } } \end{array}$ ，where $b$ is what we here denote as $\bar { R } _ { \mathrm { i o } }$ .This, likely typographical, error along with the article being written in German, likely did not help its widespread use and appreciation.

Multiplying both numerator and denominator of Eq.(A.9) by $x ^ { - N / 2 }$ and inserting $x = \mathrm { e } ^ { - 2 \mathbf { M } / N }$ gives Eq. (13). Using the first order expansion $- \ln ( 1 - \epsilon ) \approx \epsilon$ and the second order expansion $\sqrt { 1 + \epsilon } = 1 + \epsilon / \bar { 2 } - \epsilon ^ { 2 } / 8$ in $\epsilon \ll 1$ give the approximations of Eq. (14).

Upon comparing this with the continuous approximation of Eq. (A.6) we see that they are equal in case $\bar { R } _ { \mathrm { i o } } \gg 1$ ,in agreement with Fig.5.

# A.4. Limits of the exact solution

When $\mathbf M \ll 1$ ,the leading order expansion cosh $\epsilon \approx 1 + \epsilon ^ { 2 } / 2$ gives reduces Eq. (13) to $i _ { k } \approx 2 i _ { \operatorname* { m a x } } { \bf M } ^ { 2 } k ( N - k ) / N ^ { 2 }$ When additionally $\bar { R } _ { \mathrm { i o } } \gg$ $N ^ { 2 }$ ,the top limit of Eq. (14) gives $\mathbf { M } \approx N / 2 \sqrt { R _ { \mathrm { i o } } }$ s0

$$
i _ { k } \approx \frac { - \varDelta \phi _ { 0 } } { 2 R _ { \mathrm { i o } } } k ( N - k )
$$

This is a parabolic profile in $k$ and represents the limiting solution obtained first in Ref.[39],but possibly already in Ref.[41].

In the opposite limit $\mathbf M \gg 1$ ,Eq.(13) becomes approximately a constant $i _ { k } = i _ { \operatorname* { m a x } }$ ,except for the first and last cells.We can approximate Eq. (13) near $k = 0$ in this limit by

$$
\frac { i _ { k } } { i _ { \operatorname* { m a x } } } = 1 - \mathrm { e } ^ { - 2 \mathrm { M } k / N }
$$

Here $N / 2 \mathbf { M }$ is an e-folding dimensionless“penetration-depth’into the manifold [23,26]. It gives the cell number up to which $1 - \mathsf { e } ^ { - 1 } \approx 6 3 \%$ of the maximum shunt current in the manifold has been established.

![](images/b810d19a149d4b8e84955c74c5e7b89c9341aa3235ad6ccf95d03c8c0b95ba21.jpg)
Fig.B.7．An idealised rough schematic of the first and last cell showing that the stack voltage $V _ { N } ^ { \mathrm { c } } - V _ { 1 } ^ { \mathrm { a } }$ and the voltage drop $\phi _ { 1 } - \phi _ { N }$ over the electrolyte differ by $V ^ { + , \mathrm { e q } } - V ^ { - , \mathrm { e q } } + \eta _ { 1 } ^ { + } - \eta _ { N } ^ { - }$ ，with $^ +$ and minus denoting posolyte and negolyte,respectively.This is approximately equal to $\varDelta \phi _ { 0 }$ .Possible potential differences between $\phi _ { k } ^ { 0 }$ and $\phi _ { k }$ are not shown.

When $\mathbf { M } \gtrsim N$ ,the majority of the shunt current comes from the first cell and enters the last.When $\mathbf { M } \lesssim N$ several cells contribute,while for $\mathbf M \lesssim 1$ the concept starts to lose its significance as all cells contribute significantly.

# A.5. Average shunt current $i _ { \mathrm { a v } }$

The average shunt current $\begin{array} { r c l } { i _ { \mathrm { a v } } } & { \equiv } & { \frac { 1 } { N - 1 } \sum _ { k = 1 } ^ { N - 1 } i _ { k } } \end{array}$ is obtained from Eq. (A.9) as

$$
\begin{array} { c } { { \displaystyle \frac { i _ { \mathrm { a v } } } { i _ { \mathrm { m a x } } } = 1 - \frac { 1 } { N - 1 } \sum _ { k = 1 } ^ { N - 1 } \frac { x ^ { N - k } + x ^ { k } } { 1 + x ^ { N } } } } \\ { { 1 - \displaystyle \frac { 1 } { N - 1 } \frac { 2 x - 2 x ^ { N } } { ( 1 - x ) ( 1 + x ^ { N } ) } } } \\ { { 1 - \displaystyle \frac { 1 } { N - 1 } \left( \frac { \operatorname { t a n h } { ( \mathbf { M } ) } } { \operatorname { t a n h } { ( \mathbf { M } / N ) } } - 1 \right) } } \end{array}
$$

Using the geometrical series result $\begin{array} { r } { \sum _ { k = 1 } ^ { N - 1 } x ^ { k } \ = \ \frac { x - x ^ { N } } { 1 - x } } \end{array}$ for $x$ and $x ^ { - 1 }$ gives,after some algebra Eq. (A.13).Multiplying the numerator and denominator by $x ^ { - ( 1 + N ) / 2 }$ and replacing $x = \mathrm { e } ^ { - 2 \mathbf { M } / N }$ gives Eq. (A.14), equal to Eq.(2O) of Ref.[42].With the definition of the effectiveness factor in Eq. (16),Eq. (A.14) gives Eq. (17).

# Appendix B. A note on potentials

In this work,we make a clear distinction between the electrostatic potentials $\phi$ in the electrolyte and $V$ in metals like the electrode and bipolar and end plates. This is not always made explicit; see, however, for example,Ref.[47].Applying a potential $V$ to a metal in an electrolyte,a potential difference $V - \phi$ arises over the electric double layer that,relative to its value in thermodynamic equilibrium, we call an activation overpotential $\eta$

$$
\eta \equiv V - \phi _ { 0 } - \left( V - \phi _ { 0 } \right) _ { \mathrm { { e q } } }
$$

Here,a subscript O refers to the position near the ‘front’of the electrode,facing the membrane.The cell voltage is defined as the voltage difference between the anode (a) and the cathode (c):

$$
V _ { \mathrm { c e l l } } \equiv V _ { \mathrm { c } } - V _ { \mathrm { a } } = V _ { \mathrm { e q } } - \left( \eta _ { \mathrm { a } } - \eta _ { \mathrm { c } } + \Delta \phi _ { \mathrm { m e m } } \right)
$$

where we used $\phi _ { \mathrm { { e q } , \mathrm { { a } } } } ~ = ~ \phi _ { \mathrm { { e q } , \mathrm { { c } } } }$ and defined the equilibrium voltage as $V _ { \mathrm { e q } } \equiv V _ { \mathrm { e q , c } } - V _ { \mathrm { e q , a : } }$ ，and the membrane or diaphragm potential drop as $\Delta \phi _ { \mathrm { m e m } } \equiv \phi _ { \mathrm { 0 , a } } - \phi _ { \mathrm { 0 , c } } > 0 .$ Here $\eta _ { \mathrm { c } } < 0 ,$ ，so between brackets is a sum of positive quantities. For galvanic cells, $V _ { \mathrm { c e l l } }$ and $V _ { \mathrm { e q } }$ are positive, whereas for electrolytic cells, they are negative.

In a zero-gap configuration,there will be a potential difference between the front and back of the electrode

$$
\phi _ { k } - \phi _ { 0 , k } = \varDelta \phi _ { \mathrm { h } , k }
$$

where we use the indicator $\mathbf { h }$ of Ref.[115],which dealt with holes ina perforated plate electrode.Assuming all cells are equal,we have $( V - \phi ) _ { \mathrm { e q } , k } = ( V - \phi ) _ { \mathrm { e q } , k + 1 }$ so Eq. (B.1) gives for $\varDelta \phi _ { k } = \phi _ { k + 1 } - \phi _ { k }$ ：

$$
\begin{array} { r } { \varDelta \phi _ { k } = V _ { \mathrm { c e l l } , k } + \varDelta V _ { k } } \end{array}
$$

where $V _ { \mathrm { c e l l } , k } \equiv V _ { k + 1 } - V _ { k }$ is the cell voltage, including a potential voltage difference over the current collector,and

$$
\varDelta V _ { k } \equiv \varDelta \phi _ { \mathrm { h } , k + 1 } - \eta _ { k + 1 } - \varDelta \phi _ { \mathrm { h } , k } + \eta _ { k }
$$

In case the current through all cells is similar,this term may be neglected. This is implicitly assumed in using Eq.(3),which only depends on $I _ { k }$ and not on $I _ { k + 1 }$ . With this assumption, linearising Eq. (B.4) gives $\varDelta \phi _ { k } \approx V _ { \mathrm { l i n } } - I R _ { \mathrm { l i n } }$ where

$$
\begin{array} { l } { V _ { \mathrm { l i n } } = V _ { \mathrm { e q } } - \left. \left( \eta _ { \mathrm { a } } - \eta _ { \mathrm { c } } + \Delta \phi _ { \mathrm { m e m } } \right) \right| _ { I } } \\ { R _ { \mathrm { l i n } } = \left. \frac { \partial \left( \eta _ { \mathrm { a } } - \eta _ { \mathrm { c } } \right) } { \partial I } \right| _ { I } + R _ { \mathrm { m e m } } } \end{array}
$$

with $R _ { \mathrm { m e m } } = \left. \partial A \phi _ { \mathrm { m e m } } / \partial I \right| _ { I }$ is the membrane resistance evaluated for a current $I$ . For Tafel kinetics $\begin{array} { r } { \frac { \partial \left( \eta _ { \mathrm { a } } - \eta _ { \mathrm { c } } \right) } { \partial I } \bigg | _ { I } = \frac { b } { I } } \end{array}$ with $b$ the summed anodic and cathodic Tafel slope. Assuming ${ \bf \dot { \theta } } _ { \mathrm { l i n } }$ to be constant,as assumed in this work,thus strictly speaking requires $R _ { \mathrm { m e m } } \gg I b$ or otherwise $I _ { k } \approx I$

# Appendix C. Optimal port length

In the definition of electrolyser energy efficiency,Eq.(29),only the stack power consumption $- I V _ { \mathrm { s t a c k } }$ was included as an energy loss. Adding also other power losses $P _ { \mathrm { l o s s } }$ a generalised energy efficiency may be defined as

$$
\varphi _ { \mathrm { E E , e l } } \equiv \frac { - \varphi _ { \mathrm { F E } } N I V _ { \mathrm { t n } } } { - I V _ { \mathrm { s t a c k } } + P _ { \mathrm { l o s s } } } \approx \frac { V _ { \mathrm { t n } } } { V _ { \mathrm { l i n } } } \frac { 1 + \frac { V _ { \mathrm { l i n } } / I } { R _ { \mathrm { m n } } + \frac { 1 2 R _ { \mathrm { i o } } } { N ^ { 2 } } } } { 1 - \frac { P _ { \mathrm { l o s s } } } { N I V _ { \mathrm { l i n } } } }
$$

In the final approximation, we inserted Eq. (2O),assuming an optimised stack with a large number of cellsand negligible resistance $R _ { \mathrm { l i n } }$

In case the cell inlets and outlets are made sufficiently small, the flow may be laminar,and the pressure drop $\varDelta p$ may be approximated by the fully-developed single-phase Hagen-Poiseuille equation, so

$$
{ \frac { P _ { \mathrm { l o s s } } } { N } } \approx { \frac { Q A p } { \varphi _ { \mathrm { p u m p } } } } = { \frac { 1 6 \pi \mu l Q ^ { 2 } } { A ^ { 2 } \varphi _ { \mathrm { p u m p } } } } = c R _ { \mathrm { i o } } I ^ { 2 }
$$

where $ { Q \ [ \mathbf { m } ^ { 3 } / \mathbf { s } ] }$ is the flow rate per port,of length $l$ and area $A$ ,which we assume to be traversed once into and once out of the cell. Assuming the ohmic resistance of the ports dominates Eq.(l),Pouillet's law Eq. (2) gives,in case of four equal parallel feed and return manifolds, $R _ { \mathrm { { i o } } } ~ = ~ { \frac { l } { 4 \kappa A } } ~$ SO $\begin{array} { r c l } { c } & { = } & { \frac { 6 4 \pi \kappa \mu } { A \varphi _ { \mathrm { p u m p } } } \left( \frac { Q } { I } \right) ^ { 2 } } \end{array}$ ，This allows the energy efciency approximation of Eq.(C.1) to be analytically optimised for $R _ { \mathrm { i o } }$ for constant $c$ by solving $\partial \varphi _ { \mathrm { E E , e l } } / \partial R _ { \mathrm { i o } } = 0$ for $R _ { \mathrm { i o } }$ ,to give

$$
{ \frac { 1 2 R _ { \mathrm { { i o , o p t } } } } { N ^ { 2 } } } = { \sqrt { \frac { R _ { \mathrm { { m n } } } V _ { \mathrm { { l i n } } } } { I } + { \frac { V _ { \mathrm { { l i n } } } ^ { 2 } \left( 1 + { \frac { 1 2 } { c N ^ { 2 } } } \right) } { I ^ { 2 } } } } } - R _ { \mathrm { { m n } } } - { \frac { V _ { \mathrm { { l i n } } } } { I } }
$$

A real solution only exists for sufficiently small $R _ { \mathrm { m n } }$ ；otherwise,the manifold resistance will take over as the dominant resistance to shunt currents,and there is no need for small inlets and outlets.

Inserting typical numbers,we find that often the term involving $1 / c$ will dominate and

$$
R _ { \mathrm { i o , o p t } } \approx \frac { N } { I } \sqrt { \frac { V _ { \mathrm { l i n } } ^ { 2 } } { 1 2 c } } \ \mathrm { o r } \ l _ { \mathrm { o p t } } \approx \frac { N } { Q } \sqrt { \frac { \kappa V _ { \mathrm { l i n } } ^ { 2 } A ^ { 3 } } { 4 8 \pi \mu / \varphi _ { \mathrm { p u m p } } } }
$$

In this limit,the optimal port length scales linearly in the number of cells,more than linearly in the port cross-sectional area $A$ ，and inversely proportional to the flow rate. Often,the flow rate in an electrolyser is chosen high enough to maintain a maximum temperature difference $\varDelta T$ over the cell height.The heat generated in each cell is $I \varDelta V$ ，with $\Delta V = V _ { \mathrm { s t a c k } } / N - V _ { \mathrm { t n } }$ the amount by which the cell voltage exceeds the thermoneutral voltage.Equating this to the heat removal rate $\rho c _ { p } Q \Delta T$ gives $\begin{array} { r } { c = \frac { 6 4 \pi \kappa \mu } { A \varphi _ { \mathrm { p u m p } } } \left( \frac { A V } { \rho c _ { p } A T } \right) ^ { - } } \end{array}$ , independent of the current. With e.g. $\Delta V \sim 0 . 3 \mathrm { ~ V ~ } _ { : }$ $\varDelta T = 1 0 \mathrm { ~ K ~ }$ $\varphi _ { \mathrm { p u m p } } ^ { \ } = 0 . 8$ ， $\kappa = 1 . 5 \ { \mathrm { S / c m } }$ ， $\mu = 1 { \mathrm { ~ m P a } }$ s and a volumetric heat capacity $\dot { \rho } c _ { p } = 4 \cdot 1 0 ^ { 6 } \mathrm { ~ J } / \mathrm { m } ^ { 3 } / \mathrm { K } ,$ typical values for an alkaline electrolyser,with say $A _ { \mathrm { i o } } = 1 ~ \mathrm { m m } ^ { 2 }$ ，gives $c \approx 2 \cdot 1 0 ^ { - 9 }$ ,s0 we can indeed use Eq. (C.4).

Fora typical large,megawatt-scale,alkaline electrolyser, $I = 1 0 ^ { 4 }$ A so the above approximations give $Q \approx 8 \cdot 1 0 ^ { - 5 } \mathrm { ~ m } ^ { 3 } / s .$ With $V _ { \mathrm { l i n } } = 1 . 5$ V and $N = 1 0 ^ { 2 }$ Eq. (C.3) gives $l _ { \mathrm { o p t } } = 1 . 8 ~ \mathrm { k m }$ ，so that it is clearly not feasible to make use of this optimum.Note that this does not necessarily mean that the energy efficiency cannot be high, just not a maximum.

In line with this,Ref.[8l] argues that the inlet and outlet ports should be made as long as possible,and that the channel diameter should then be used to optimise for the desired pressure drop and shunt losses.This can be immediately appreciated since a change in length impacts shunt current and pressure drop in a similar way.However, a change in diameter affects pressure drop much more than shunt currents.In the laminar analysis provided here,the pressure drop at constant flow rate scales inversely with the channel diameter to the power 4,whereas in fully turbulent flow it scales roughly to the power 5.While this section presents an illustrative example that enables analytical optimisation,in general,the energy efficiency in Eq.(C.1) can only be optimised numerically.

# Data availability

No data was used for the research described in the article.

# References

[1] H. Fumio, Electrode processes and electrochemical engineering, Plenum Press, 1985.
[2] T.F.Fuller, J.N. Harb,Electrochemical Engineering, John Wiley & Sons, 2018.
[3] V.O.Godoy，P. Davari， H.L. Frandsen，F. Blaabjerg， Physics-based modeling of degradation in alkaline water electrolysis cells due to reverse currents, in: IECON 2025-51st Annual Conference of the IEEE Industrial Electronics Society, IEEE Xplore,2025, pp. 1-6.
[4] E.Rasten, Shunt-currents in alkaline water-electrolyzers and renewable energy, ECS Trans.113 (9) (2024) 25.
[5]R.Bauer,J. Claus, Bipolar electrolysis cell assembly -with electrolyte pasing in parallel through cells electrically in series,1972,Patent Number: FR2114043, holder: Rhone Progil SA, URL http://www.google.it/patents/US4741207.
[6]K. Kampanatsanyakorn，S.Holasut, Compact frameless bipolar stack for a multicell electrochemical reactor with planar bipolar electrical interconnects and internal ducting of circulation of electrolyte solutions through all respective cell compartments,2013, Patent Number: US2013157097A1, priority: IB2010001651W (2010-06-29).
[7] J.Hinatsu， M. Stemp， Electrolyser module， 2O10， Patent Number: US2010012503A1, pri0rity: CA2637865A (2008-07-15).
[8] M. Zahn, P.G. Grimes,R.J. Bellows, Shunt current elimination and device, us patent 4,197, 169,1980.
[9] P.G.Grimes, M. Zahn, Shunt current elimination and device employing tunneled protective current, us patent 4,277, 317, 1981.
[10] P.G. Grimes, M. Zahn, R.J. Bellows, Shunt current elimination, us patent 4,312, 735, 1982.
[11]C.E.Evans,S.Casey，T.Groberg,Y. Song,Redox flow battery and battery system,2021,Patent Number: US2021359327A1,priority:US202063025316P (2020-05-15), URL https://patents.google.com/patent/US2021359327A1.
[12] F. Beille, Stack of redox-flow electrochemical cels with decreased shunt, 2022, Patent Number: US11239483B2, priority: FR1857898A (2018-09-03).
[13] M.C.Chi,P.Carr,Method of minimizing the effects of parasitic currents, 1983,Patent Number: US4371825A,priority: US27048181A (1981-06-04), URL https://patents.google.com/patent/Us4371825A.
[14]J.Ahola,P.Kauranen,M. Niemela,V.Ruuskanen,A.Kosonen,An electrolyzer system and a method for water electrolysis,2O24,Patent Number: US2024410063A1,priority:FI20216157A (2021-11-10),URL https://patents. google.com/patent/US2024410063A1.
[15] E.N. Balko, L.C. Moulthrop, Apparatus for reduction of shunt current in bipolar electrochemical cell assemblies,us patent 4,371,433,1983.
[16] C.A.FRIESEN,R. Krishnan，M.J. Mihalka,J.R. Hayes，G.FRIESEN,Elec-trochemical cell system with shunt current interrupt,us patent 9,1O5, 910, 2015.
[17] E.J. Peters,W.P. Zeman, Electrical current breaker for fluid stream, us patent 4,032, 424, 1977.
[18]M.Stroder，M.Schuster，T.Kania,Bipolar electrochemical system，2016, Patent Number:WO2016128038A1,priority:EP2015052860W,URL https:// patentscope.wipo.int/search/en/detail.jsf?docId=WO2016128038.
[19] R.O.M.Idan, M. Moshkovich, H. Dotan, Device and method for ionic shunt current elimination, us patent app, 590, 2024, 18/572.
[20]RLLeRoyAKtuart,dvncduoareeoisIt.J.d 6 (6) (1981) 589-599.
[21]A.T.Kuhn,J.S.Booth,Electrical leakage currents inbipolarcellstacks,J.Appl. Electrochem.10 (2) (1980) 233-237.
[22]G. Zhao,S.Duan,Q.Tian,T.Wu, Mathematical models of currentlosses in bipolar cells,Met. Trans. B 21 (1990) 783-790.
[23] S.K.Rangarajan, V. Yegnanarayanan, Current losses ina bipolar_cell—an analysis of the tafel regime, Electrochim. Acta 42 (1) (1997) 153-165.
[24] E.A. Kaminski, R.F. Savinell Technique for calculating shunt leakage and cell currents in bipolar stacks having divided or undivided cells, J. Electrochem. Soc. ;(United States) 130 (1983).
[25]M.-Z.Yang, H. Wu, JR.Selman, A model forbipolar curent leakageincell stacks with separate electrolyte loops, J. Appl. Electrochem.19 (2) (1989) 247-254.
[26] O. Ksenzhek,N.D.Koshel, Current leakage in high-voltage battries with a common manifold, Ii, Elektrokhimiya 7 (3) (1971) 353-357.
[27] V.B. Kogan, R.R. Ovsepyan, BHyTpeHHNX yTeYHaX TOHa B JeKTpoJTuecKHx ycTaHoBkax (on internal current leakages in electrolytic installations)，Khimicheskaya Promyshlennost 463 (8） (1954) 15-21.
[28]G.A.BaryshnikoV，A.I. LoshkareV，KOMMyTMPOBAHME HM3KOBOJIbTHbIX ③JIEKTPOPEHEPMPVIOIINX 9JIEMEHTOB B CNCTEME HCTOYHNKA TOKA IOBbIH,adk 5 (123) (1968) 123.
[29] E.F.M. van der Held, Unpublished Results, sponsored research report No. 229, Central Technical Institute,T.N.O.,The Hague,1957.
[30] V.A. Onishchuk，Optimization of the electrical parameters of an electrochemical multivoltage bateryas_a function of the electrolyte feed circuit, Elektrokhimiya 8 (5)(1972) 698-702, translated from Elektrokhimiya. Original article submited February,16,1971, Moscow.
[31] V.F. Grigor'ev, B.P. Nesterov, S.I. Sirotin, Influence of leakage currents on the output characteristics of a battery of electrolyzers with a common collector continuous model, Sov.Electrochem. (Engl.Transl.);(United States) 21 (6) (1985).
[32] A.F. Mazanko， G.M. Kamarian,O.P.Romashin， Promyshlennyi membrannyi elektroliz,1989,p.121,Promyshlennyi membrannyi elektroliz.
[33] E.L.Molel, J.N.Harb,T.F.Fuler,Use of an analytical model to enhance understanding of shunt currents in a bipolar stack, ECS Adv.4 (3) (2025) 030502.
[34] E.R. Henquin,J.M. Bisang, Simplified model to predict the effct of the leakage current on primary and secondary current distributions in electrochemical reactors with a bipolar electrode, J.Appl. Electrochem.35 (12) (2005) 1183-1190.
[35] V.P.Izosenkov，V.L.Kubasov，A.F. Mazanko，A method to calculate leakage currents in bipolar electrolyzers，Elektrokhimiya 18 (9）(1982) 1255-1260,translated from Elektrokhimiya. Original article submited February 23,1981.Published by Plenum Publishing Corporation in 1983.UDC 621,357.1,035.1:66.012.5.
[36] B.P. Nesterov，G.A. Kamzelev,V.P.Gerasimenko， N.V. Korovin， Dispersion currents in filter-press type batteries with a common collector,Elektrokhimiya 9(8)(1973）1154-1158，translated from Elektrokhimiya.Original article submitted June 26, 1972. UDC 541.13. Moscow Power Institute.
[37] I. Rousar, Calculation of currnt density distribution and terminal voltage for bipolar electrolyzers; application to chloratecels,J. Electrochem.Soc.116 (5) (1969) 676.
[38] 1. Rousar, V. Cezner,Experimental determination andcalculation of parasitic currents in bipolar electrolyzers with application to chlorate electrolyzer,J. Electrochem.Soc. 121 (5) (1974) 648.
[39] J.C.Burnett, D.E. Danly,Current bypass in electrochemical cell assemblies, in: AIChE Symp Ser, vol. 8,1979, p.13.
[40] G. Bonvin, C. Comninellis, Scale-up of bipolar electrode stack dimensionless numbers for current bypass estimation, J. Appl. Electrochem. 24 (6) (1994) 469-474.
[41]A. A.yax (Buakh)Electrolysis ofoper,933,e3a(etdat).
[42]W.Thiele,M.Schleif,，HMatsciner,Beitragzurberechnungundmiierung von verluststromen an bipolaren elektrolysezellen, Electrochim.Acta 26 (8) (1981) 1005-1010.
[43] I. Rousar,J. Thonstad, Calculation of bypasscurrents in molten salt bipolar cells,J. Appl. Electrochem. 24 (1994) 1124-1132.
[44] S.K. Rangarajan, V. Yegnanarayanan, M. Muthukumar， Current losses in a bipolarcell-Ii: An analysisof the Butler-Volmer regime, Electrochim.Acta 44 (2-3) (1998) 491-502.
[45]J.R.Wilson，Depolarisation in electrodialytic demineralisation, Trans. Inst. Chem. Eng. 41 (1963) 3.
[46] W.G.B.Mandersloot,R.E. Hicks,Leakage currents_in electrodialytic desalting and brine production, Desalination 1 (2) (1966) 178-193.
[47]S.Szpak，C.J.Gabriel，J.R.Driscoll， Li/socl2 batery intercellcurrents，J. Electrochem. Soc.131 (9) (1984).
[48] C.J.Gabriel， S. Szpak, Power losses in batteries with a common electrolytic path, J. Power Sources 25 (3) (1989) 215-227.
[49]C.J.Gabriel,P.A.Mosier-Boss,S.Szpak,J.Smith, Intercellcurrents inassembly of modules: quality control considerations, J. Power Sources 32 (4) (1990) 353-372.
[50]P.A. Mosier-Boss，S.J. Szpak, Li/Soci2 Battery Technology: Problems and Solutions, Tech.rep., Naval Command Control and Ocean Surveillance Center, 1992.
[51] M.K.Bassiouny，H.J.C.E.S.Martin，Flow distribution_and_pressure dropin plate heat exchangers—ii z-type arrangement, Chem. Eng. Sci. 39 (4) (1984) 701-704.
[52] J. Wang, Pressure drop and flow distribution in parallel-channel configurations OffuelcelsZarrangemntIntJHdrgEergy() 5498-5509.
[53]K.MB.Jansenlosed-foolutiosforurentdistributininder-tye textile heaters, Thermo 4 (4) (2024) 433-444.
[54] R.S.Jupudi, G. Zappi, R. Bourgeois, Prediction of shunt currents in a bipolar electrolyzer stack by difference calculus, J. Appl. Electrochem.37 (8) (2007) 921-931.
[5]PR.Prokopius,ModelforCalculatingElectrolytic SuntPathLoesinLre Electrochemical Energy Conversion Systems, Tech.rep., NASA, 1976.
[56] R.E. White, C.W. Walton, H.S. Burney, R.N. Beaver, Predicting shunt currents in stacks of bipolar plate cells, J. Electrochem. Soc.133 (3) (1986) 485.
[57]F.P. Dousek, K. Micka,Advanced laboratory electrolyser for production of pure hydrogen, J. Appl. Electrochem. 23 (3) (1993) 241-246.
[58] M. Katz,Analysis of electrolyte shunt curents in fuel cell power plants, J. Electrochem. Soc.125 (4) (1978) 515.
[59]J.A.Schaeffer,L-D.Chen,J.P.Seaba, Shuntcurrntcalculationoffuelcell stack using simulink?,J. Power Sources 182 (2) (2008) 599-602.
[60] W.R. Bennett， M.A. Hoberecht, V.F. Lvovich, Analysis of shunt currents and associated corrosion of bipolar plates in pem fuel cells,J. Electroanal. Chem. 737 (2015) 162-173.
[61] A. Culcasi, L. Gurreri, A. Zaffora,A. Cosenza, A. Tamburini, A. Cipollina, G. Micale, Ionic shortcut currents via manifolds in reverse electrodialysis stacks, Desalination 485 (2020) 114450.
[62] G. Codina, A. Aldaz, Scale-up studies of an fe/cr redox flow battry based on shunt current analysis, J. Appl. Electrochem. 22 (7) (1992) 668-674.
[63]F.Wandscheider.Roh,Pcher，Kikwart,J.bke,Nihl, multi-stack simulation of shunt currents in vanadium redox flow batteries, J. Power Sources 261 (2014) 64-74.
[64] Y. Zhang, J. Zhao, P. Wang, M. Skyllas-Kazacos, B. Xiong, R. Badrinarayanan, A comprehensive equivalent circuit model of all-vanadium redox flow battery for power system analysis, J. Power Sources 290 (2015) 14-24.
[65]Q. Ye,J. Hu,P.Cheng, Z.Ma, Design trade-ofs amongshuntcurrent,pumping loss and compactness in the piping system of a multi-stack vanadium flow battery,J. Power Sources 296 (2015) 352-364.
[66] R.M. Darling, H.-S. Shiau, A.Z. Weber, M.L. Perry, The relationship between shunt currents and edge corrosion in flow batteries,J. Electrochem. Soc.164 (11) (2017) E3081.
[67]JL.Barton,FR.Bushet,Aone-imensinalsack modelforedoxfowbey analysis and operation,Batteries 5 (1)(2019) 25.
[68] H. Fink, M. Remy, Shunt currents in vanadium flow batteries: Measurement, modelling and implications for efficiency， J.Power Sources 284 (2015) 547-553.
[69]F.Xing,，H.Zhang,X.MaSuntcurrentosof thevaadiumedoflowttey, J. Power Sources 196 (24) (2011) 10753-10757.
[70] S. Konig,M. Suriyah, T.Leibfried, Model based examination on influence of stack series connection and pipe diameters on eficiency of vanadium redox flow bateries under consideration of shunt currents, J. Power Sources 281 (2015) 272-284.
[71] Y.-S.Chen,S.-Y.Ho,H.-W.Chou, H.-J. Wei, Modeling the efect of shunt current on the charge transfer eficiency of an allvanadium redox flow battery， J. Power Sources 390 (2018) 168-175.
[72] J.Chen,T.Yan,E.Kizhnerman, H. Yin,M.-X. Zhang,D.Hui, Numerical analysis and optimization on shunt loses in a multi-stack vrfb system,in: 2018 2nd IEEE Conference onEnergy Internetand Energy System Integration (EI2),IE,018, pp. 1-6.
[73]A. Trovo,G. Marini, A. Sutto,P.Aloto, M.Giomo,F. Moro,M. Guarnieri, Standby thermal model of a vanadium redox flow battery stack with crossover and shunt-current effects. Appl. Energv 240 (2019) 893-906.
[74] X. Zhao, Y.-B. Kim,S. Jung, Shunt current analysis of vanadium redox flow battery system with multi-stack connections,J. Energy Storage 73 (2023) 109233.
[75] H.-W.Chou,F.-Z. Chang, H.-J. Wei, B. Singh, A. Arpornwichanop,P. Jienkulsawad, Y.-S. Chou, Y.-S. Chen, Locating shunt currents in a multistack system of all-vanadium redox flow batteries,ACS Sustain. Chem. Eng. 9 (12) (2021) 4648-4659.
[76] M.S. Yesilyurt， H.A. Yavasoglu， An all-vanadium redox flow battery:a comprehensive equivalent circuit model, Energies 16 (4) (2023).
[77] A. Tang, J. McCann, J.Bao, M. Skylas-Kazacos, Investigation of the efect of shunt current on battery efficiency and stack temperature in vanadium redox flow battery,J. Power Sources 242 (2013) 349-356.
[78] D.A. Ispas-Gil, E. Zulueta, J. Olarte, A. Zulueta, U. Fernandez-Gamiz, Optimization of the shunt currents and pressure losses of a vrfb by applying a discrete pso algorithm, Batteries 10 (7) (2024).
[79] N.M. Delgado，R. Monteiro，J. Cruz,A. Bentien，A. Mendes，Shunt cur-rents in vanadium redox flow batteries-a parametric and optimization study, Electrochim. Acta 403 (2022) 139667.
[80] B.J. Neyhouse,N.A.Price,F.R.Brushett， A computationally eficient， zerodimensional stack model for simulating redox flow battry performance, J. Electrochem. Soc.172 (1) (2025) 010522.
[81]R.Qi，M.Becker,J.Brauns，T.Turek，J.Lin,Y. Song，Channel design optimization of alkaline electrolysis stacks considering the trade-off between current efficiency and pressure drop, J. Power Sources 579 (2023) 233222.
[82] G. Sakas,A. Ibanez-Rioja, S. Pöyhonen,L. Jarvinen, A. Kosonen, V. Ruuskanen, P.Kauranenoaeiasesd the shunt currents and the sec in an industrial-scale alkaline water electrolyzer plant,Appl. Energy 359 (2024) 122732.
[83] G. Sakas, A. Ibanez-Rioja, S.Pöyhonen, A. Kosonen, V. Ruuskanen, P. Kauranen,J. Ahola, Influenceof shunt currents inindustrialscalealkaline water electrolyzer plants, Renew. Energy 225 (2024)120266.
[84] Y. Uchino, T. Kobayashi, S. Hasegawa, I. Nagashima, Y. Sunada, A. Manabe, Y. Nishiki, S. Mitsushima, Relationship between the redox reactions on a bipolar plate and reverse current after alkaline water electrolysis, Electrocatalysis 9 (1) (2018) 67-74.
[85] P.P.Pirotski,，N.N. Shvetsov， Instrument for measuring direct current in electrolyte jets, Meas. Tech. 4 (12) (1961) 993-995.
[86] H.P. Sarma, A. Antonyraj, G.N. Kannan, A. Selvakesavan, Estimation of bypass current in a bipolar electrode stack-magnesium bipolar cell,Port. Electrochimica Acta 14 (1996) 7-14.
[87] P.G.Grimes,R.J. Bellows， Shunt current control methods in electrochemical_systems—appications，ElectrocemicalCellDesign，Springer，1984pp. 277-292.
[88]N. Hagedorn，M.A.Hoberecht,L.H. Thaller，Nasa-Redox Cell-Stack Shunt Current, Pumping Power,and Cell-Performance Tradeoffs, Tech.rep.,1982.
[89] A.F. Adamson, B.G. Lever, W.F. Stones,The production of hypochlorite by direct electrolysis of sea water: Electrode materials and design of cels for the process, J. Appl. Chem.13 (11) (1963) 483-495.
[90] E.R. Henquin, Estudio teórico y experimental de reactores electroquimicos bipolares,determinacion de lascorrientes parasitas y analisis de su efecto sobre la distribucion de corriente (Ph.D.thesis),2008,availableat:https: //bibliotecavirtual.unl.edu.ar:8443/bitstream/handle/11185/84/Tesis.pdf.
[91] C.Comninells,，E. Platner， P.Bolomey，Estimation of current bypass in a bipolar electrode stack from current-potential curves,J. Appl. Electrochem. 21 (5) (1991) 415-418.
[92] D.Dogan, B.Hecker,B. Schmid,H. Kungl, H. Tempel,R.-A.Eichel,Experi-mental determination of stray currents in parallel operated cells exemplified on alkaline water electrolysis, Electrochim. Acta 50o (2024) 144767.
[93] G. Hysa, T. Anttilainen, V. Ruuskanen, S. Pöyhönen,A. Kosonen, M. Niemelä, P.Kauranen, J. Ahola,Modelling and study of shunt currents in an industrial alkaline water electrolyser with various number of cells in series, IET Renew. Power Gener.19 (1) (2025) e70112.
[94] Q.Li,L.Sha,R. Qi,J. Lin,H.Li, D.Gao,W.Li,R. Lin,A real-time method forestimatingcurrnteficiencyinalalnewaterelectrolysisstacksusing low-power and operational data, 2025,Available at SSRN 5090768.
[95] L. Sha, J. Lin, Y. Chi, Q. Li, R. Qi, A cascaded gas-liquid separator for multi-stack series configuration to improve the current efficiency of alkaline water electrolysis system, 292, 2025, Available at SSRN 5657.
[96] T.Viinanen,V. Ruuskanen, J. Ahola, M. Niemela, R. Kingas, P. Sonnabend, S. Vuorsalo,M. Kauhanen, P.Kauranen, Serial connection of 48-cell alkaline electrolysis stacks, J. Power Sources 659 (2025) 238382.
[97] H.S.Burney,R.E.White, Predicting shunt currents in stacks of bipolar plate cells with conducting manifolds, J. Electrochem. Soc.135 (7) (1988)1609.
[98]RIIzoseovVuseaukasAFMazakoullaculatonoage currents in electrolysis plants with bipolar electrolyzers, Sov. Electrochem. 27 (12) (1991) 1411-1423.
[99] O.S. Ksenzhek, N.D. Koshel', Current leakages in high-voltage batteries with a total collector.i，Elektrokhimiya 6(10) (1970）1587-1591，translated from Elektrokhimiya. Original article submited 1970,.F.E. Dzerzhinskii Dnenronetrovsk Chemical Engineering Institute.
[100] G. Zhou, L.-D. Chen, J.P. Seaba, Cfd prediction of shunt currents present in alkaline fuel cells, J. Power Sources 196 (20) (2011) 8180-8187.
[101] R.Kodym，K. Bouzek,D. Snita,J. Thonstad, Potential and current density distributions along a bipolar electrode, J. Appl. Electrochem. 37 (11) (2007) 1303-1312.
[102] E.R. Henquin, J.M. Bisang, Effect of leakage currents on the secondary current distribution in bipolar electrochemical reactors,J. Appl. Electrochem.38(9) (2008) 1259-1267.
[103] E.R. Henquin, Generalized algebraic phenomenological model for parallel-plate bipolar electrochemical reactors, J. Electrochem. Soc.170 (10) (2023) 103507.
[104] A.N. Colli, H.H. Girault, Compact and general strategy for solving current and potential distribution in electrochemical cells composed of massive monopolar and bipolar electrodes, J.Electrochem.Soc.164(11) (2017) E3465.
[105]D.Huang,B. Xiong,J.Fang,K. Hu,Z. Zhong,Y. Ying,X.Ai, Z. Chen, A multiphysics model of the compactly-assembled industrial alkaline water electrolysis cell, Appl. Energy 314 (2022) 118987.
[106] D.Bordignon, M. Guarnieri, Progress in flow-battery shunt current investigations: a species-resolved foundational approach, J. Energy Storage 124 (2025) 116783.
[107] T.P.Golmarz, S.K. Yekani, et al.,Parasitic shunt currents in alkaline water electrolysis (awe) for generating clean hydrogen, Energy Eng.: J. Assoc.Energy Eng.122 (10) (2025) 4121.
[108]M.A.Sarwar,P.Kauranen,T.Koiranen,J.Ahola,A. Kosonen,K.Hynynen, V.Ruuskanen, Investigating the effect of operating conditions on void fraction,stray currents,and current distribution in an alkaline water electrolysis stack using computational fluid dynamics,2025,http://dx.doi.org/l0.2139/ ssrn.5056519,Submitted to J.Applied En.Preprint Available at SSRN:https: //ssrn-com.tudelft.idm.oclc.org/abstract=5056519.
[109] T.Ishikawa, S. Konda, Evaluation of bipolar electrode cells for electrowinning of liquid aluminum from chloride melts, in: Proceedings of the First International Symposium on Molten Salt Chemical Technology, Kyoto, 1983,pp.20-22.
[110]J.W. Haverkort,Electrolysers,fuel cels and batteries:Analytical modelling, 2024,http://dx.doi.org/10.59490/tb.93,TU Delft OPEN.
[111] J.W.Haverkort,A theoretical analysis of the optimal electrode thickness and porosity, Electrochim. Acta 295 (2019) 846-860.
[112] E.W. Thiele,Relation between catalytic activity and size of particle, Ind. Eng. Chem. 31 (7) (1939) 916-920.
[113] A.Tantram, Shunt Currents in Electrolytic Plant,Wolfson Unit, City Univ., 1975.
[114]J. Divisek,R. Jung,D. Britz, Potential distribution and electrode stability in a bipolar electrolysis cell, J. Appl. Electrochem.20 (2) (1990) 186-195.
[115] J.W.Haverkort, A.S. Aghdam，E. Craye, The optimal electrode hole size in zero gap alkaline water electrolysis:A combined electrochemical, theoretical, and bubble imaging approach, Int. J. Hydrog. Energy 171 (2025) 150919.