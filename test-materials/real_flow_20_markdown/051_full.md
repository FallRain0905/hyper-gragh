# Modelling extreme shunt currents and their role in vanadium redox flow battery degradation: A tool for multi-cell stack design optimisation

Vishnu K aO, Nishant Beriwalb, Sumit Kumar Pramanick $\mathrm { c } _ { \oplus }$ ， Anil Verma b,\*①

SchoolofIterdisciplinaryesearch (e),dian Instituteofechnologyelhi,Newelhio6,dia bDepartmentofcalngneofoee ‘Departmentof Electrical Engineering,Indian Institute of Technology Delhi,New Delhi,11ool6,India

# HIGHLIGHTS

·Developed a model framework for predicting shunt currents in multi-cell VRFB.   
·Predicts individual cell voltage imbalance and graphitic degradation across stack.   
·Evaluates the compatibility of developed flow frame with the stack.   
·Model validated using an experimental 10-cell VRFB stack.

# GRAPHICALABSTRACT

![](images/a5bad704e055a223f5b759aea8a4dff023c9d8fa0fac316fecdee10f26e81580.jpg)

# ARTICLEINFO

Keywords:   
Degradation   
MATLAB modelling   
Multi-cell stack   
Shunt current   
Vanadium redox flow battery

# ABSTRACT

Vanadium redox flow batteries (VRFBs) have gained significant atention as a sustainable solution for large-scale energy storage due to their long cycle-life,modular design,and independent scalability of power and energy capacity.However,certain technological challenges need to be addressed forits effctive market penetration.For instance,high shunt current inside te multi-cellstack could lead to poor performance as well as degradation of the active components.This work presents a comprehensive analysis of the degradation effects of shunt current through acombined modeling and experimental approach.For the first time,a detailed MATLAB-based model is developed to predict shunt current behaviour in a multi-cell VRFB stack,enabling quantitative analysis of the shunt current's influence on active material health.To establish the modelling results,a 10-cell lab-scale VRFB stack is fabricated to observe degradation patterns and discover optimal operating parameters.Furthermore,the developed model is used to mitigate these degradation efects by evaluating thecompatibilityof the designed flow frames with the multi-cell VRFB stack.This work notonly suggests shunt current as an important design parameter but also acts as a tool for better architecture design of the stack,including but not limited to flow batteries,electrolysers and fuel cells.

# 1．Introduction

The global energy system is undergoing a rapid transition to mitigate climate change by reducing dependence on fossil fuels [1].The increasing integration of renewable energy sources such as solar and wind into power grids has accelerated this shift toward cleaner and more sustainable technologies [2].However, the intermittent and variable nature of these renewable sources poses significant challenges in maintaining grid stability,ensuring a reliable power supply and complete independence from fossil fuel-based energy sources.To address these challenges, energy storage systems (Ess) have emerged as a key component of modern power networks. ESS technologies store excess energy during periods of low demand when available and release it during periods of intermittency,thereby balancing supply and demand [3,4].Among the various ESS technologies, VRFBs have emerged as a highly promising solution for grid-level energy storage [5].Unlike conventional batteries,VRFBs store energy in external electrolyte tanks (containing vanadium ions in different oxidation states),enabling independent scaling of power and energy capacities [6]. This modularity makes them useful for ESS applications that require long-duration storage,thus providing cost-effective scale-up.Moreover,VRFB offers long cycle life $( > 1 0 , 0 0 0 )$ ,rapid response time,deep discharge capability,high recyclability of vanadium electrolytes and safe operation [7-9]. Additionally, the ability to avoid cross-contamination by using the same redox species (vanadium) in both half-cells ensures electrolyte health. These features make VRFBs an attractive solution for sustainable,large-scale renewable energy storage [6]. The single-cell VRFB consists of two half-cells separated by an ion-selective membrane,with graphite electrodes contained in a gasket-sealed arrangement along with graphitic bipolar plates [1O] as shown in Fig.1. The practical energy storage applications demand higher voltage levels,which are achieved by connecting multiple cells in series,electrically joined using bipolar plates,to form a multi-cell arrangement called a stack [11,12].When cells are stacked together,the electrolyte is distributed via interconnected manifolds that deliver and collect electrolyte from each cell. Although these manifolds are essential for a uniform electrolyte supply, they also create an ion conduction path between all half-cels of the same electrolyte.The resistance of these paths leads to parasitic shunt currents between the cells,even during no-load conditions.The magnitude of these currents is governed by various parameters,most critically by the number of cells,the electrolyte manifold,and the flow channel geometry,making them a critical design consideration for multi-cell stacks.

# 2.Shunt currents in multi-cell stack

Shunt currents arise mainly in multi-cell VRFB stack configurations due to the presence of internal ionic short-circuit paths formed by the electrolyte-flooded manifolds.Fig.2a illustrates the schematic of a multi-cell VRFB stack,in which individual cells are electrically interconnected through bipolar plates.The bipolar plate,placed between two adjacent cells,for example,between cell1 and cell 2,electrically connects the negative electrode of cell 1 to the positive electrode of cell 2. Consequently,vanadium ions $\mathrm { V } ^ { 2 + }$ at the negative side of cell 1 can undergo oxidation by releasing electrons,which could be subsequently accepted by $\mathsf { V } ^ { 5 + }$ ions at the positive side of cell 2.Because of this electron transfer,charge neutrality must be preserved through a corresponding ionic transport mechanism, such as the migration of a proton from the negative side of cell1 to the positive side of cell 2.Identifying this critical path for proton migration will result in shunt current flow between these adjacent cells.For instance, $( \mathrm { H } ^ { + } )$ ions from the negative side of cell1 can migrate towards the positive side of cell1 through the membrane.And since the positive half-cells of all individual cels are hydraulically connected via a common electrolyte manifold,these migrated $( \mathrm { H } ^ { + } )$ ions can then travel from the positive of cell 1 to the positive of cell 2, thereby completing the ionic circuit path.This combined electronic and ionic conduction path forms an unintended but continuous internal current loop within the stack.The magnitude of the shunt current is primarily governed by the ohmic resistance associated with proton conduction along this internal path.Even under no-load conditions,such leakage currents result in parasitic self-discharge of the electrolyte,leading to reduced coulombic efficiency and even degradation of key active materials [13-16].Therefore,shunt current mitigation is a critical design consideration for multi-cell VRFB stacks [17].

Several studies have examined behaviour and implications of shunt currents in VRFB stacks,using both experimental and modelling approaches.The first equivalent circuit representations to simulate shunt current behaviour were done by NASA[18].Additionally, Kazacos et al. [16] provided a detailed explanation of the mechanism and modelling approaches for shunt current formation,which has since served as a foundation for subsequent studies.Fink etal.[19] developed a five-cell mini-stack with switchable hydraulic paths,enabling direct measurement of shunt currents under controlled conditions. Similarly, Xing et al. [15] performed a sensitivity analysis on critical design parameters, including cell count,manifold resistance,and channel resistance,offering insight into the influence on shunt current magnitude.Yin et al. [20] later applied three-dimensional finite element modelling (FEM) to simulate shunt current distribution and validated their findings experimentally.Beyond electrical characterisation,extensive research has addressed the thermal and system-level impacts of shunt currents throughenhancedmodellingapproaches，includingcoupled thermal-electrical stack models,state-of-charge (SoC) dependent electrolyte conductivity,standby and high-current thermal behaviour,and loss mitigation strategies in large-scale and multi-stack VRFB systems [21-32].Here, SoC denotes the ratio of remaining charge to the nominal capacity，typically expressed as a percentage ( $0 \%$ fully discharged, $1 0 0 \%$ fully charged).Another key factor is the flow-frame geometry, which plays a key role in controlling shunt current magnitude.By increasing the electrolyte channel length and reducingthe cross-sectional area of the electrolyte flow passages,the ionic resistance of the shunt path can be increased, thereby suppressing shunt currents. Several studies have examined flow-frame optimisation strategies aimed at minimising shunt current losses,reporting values ranging from approximately $9 \%$ [33] to below $1 \%$ [34],depending on the channel geometry and stack configuration [13,33-36]. These studies consistently demonstrate that narrower and longer electrolyte paths are effective in suppressing shunt currents.Table 1 summarises the shunt current magnitudes reported in the literature for various flow-frame geometries.However，excessively narrow channels significantly increase the pressure drop within the stack,resulting in higher pumping power requirements and reduced overall system efficiency.

![](images/c819e04c74f1eab85a424756e49e534341f197cde77a45ff65ade4c36ddc922f.jpg)  
Fig.1.Exploded view showing the main components of a VRFB stack.

To address this trade-off,Ye et al.[3O] analysed the relationship between shunt current re duction and hydraulic losses.Their results indicate that an optimal flow-frame design should employ suficiently long channels to increase ionic resistance while maintaining adequate channel width to limit pressure drop.Furthermore,they demonstrated that large stacks comprising many cells can be divided into multiple smaller stacks that are electrically connected in series and hydraulically connected in parallel.Using this approach,the shunt current in a 120-cell stack was reduced from $1 1 . 7 \%$ to approximately $1 . 6 4 \%$ Previous studies have only addressed the performance losses and mitigation strategies to minimise shunt current.However,no study has focused on the possible negative effects of these shunt currents inside the stack.This is important because,in related electrochemical systems such as fuel cells,bipolar plate deterioration within the stack has been reported, primarily due to excessively wetted manifolds that form low-resistance paths leading to the generation of shunt currents [37,38]. Such findings,although scarce, suggest that similar effects could occur in VRFBs, particularly where incompatible flow frames with high shunt current are employed.For instance,the fundamental design of flow frames from the point of view of either minimising shunt currents or pressure drops is different.The development of flow frames for minimisation of pressure drops will demand the use of wider and short channel flow frames, however, these flow frames will have increased shunt currents.If the shunt currents cross some voltage threshold value,they may result in the degradation of graphitic components inside the stack.In our earlier work [17],the evidence of shunt current-induced bipolar plate degradation in multi-cell VRFB stacks was experimentally identified and highlighted as an important design consideration.However， no modelling-based validation or prediction model for this degradation mechanism is available.The need for this modelling approach is important because it would lead to the estimation of shunt currents while designing optimum flow frames for multi-cell VRFB stack.Further, it will also help to uncover the voltage variation among individual cells inside the stack and help understand the possible degradation at intended stack operation.This will help various stakeholders involved in flow system research to optimise the stack performance and its durability.

Table 1 Shunt current in different flow frame geometries reported in the literature.   

<table><tr><td>No. of cells</td><td>Operating parameters</td><td>Shunt current</td><td>Ref.</td></tr><tr><td>20</td><td>Load =39 A SoC=80%</td><td>&lt;1%</td><td>[34]</td></tr><tr><td>64</td><td>Active area = 780 cm2 Load = 84 A SoC=50%</td><td>~8%</td><td>[35]</td></tr><tr><td>40</td><td>Active area = 416 cm² Load = 27.44 A SoC=50%</td><td>6.55%</td><td>[13]</td></tr><tr><td rowspan="3">10</td><td>Active area = 343 cm² Load = 27.44 A SoC = 50%</td><td>1.57%</td><td></td></tr><tr><td>Active area = 343 cm² Load = 0.4 A</td><td>9%</td><td>[33]</td></tr><tr><td>SoC=50% Active area = 4 cm² SoC=80% Active area = 600 cm²</td><td>~7%</td><td>[23]</td></tr></table>

The main contributions of this paper are summarised as follows:

i.This work presents a novel modelling framework that explicitly couples shunt current behaviour,flow-frame geometry,and celllevel voltage imbalance with bipolar plate degradation in multicell VRFB stacks,thereby enabling early-stage evaluation of performance and component health during stack design.

![](images/2e314a0d830c949fcea066ac613eef71d8f312803c37b245a213068b25c44802.jpg)  
Fig2.ad all system.

ii.A MATLAB-based iterative battery model is developed that captures the dependence of open-circuit voltage (OCV),internal resistance,and electrolyte conductivity on the SoC,enabling a realistic representation of electrochemical behaviour and dynamic shunt current distribution under varying operating conditions.

iii.Experimental validation is conducted to demonstrate the advantages of the proposed modelling approach across different flowframe configurations and to support the findings reported in our earlier work [17].

The remainder of the paper is organised as follows.Section III presents the modelling framework and methodology,detailing the proposed approach.Section IV discusses the simulation and experimental results,including a comprehensive analysis and validation of the shunt current modelling.Finally, Section V concludes the paper.

# 3. Modelling framework and methodology

# 3.1. Flow frame configuration

The flow field of a VRFB can be configured in multiple ways, including externally fed channels and internally fed manifolds,and its design is a critical factor governing overall system performance.An effective flow frame ensures uniform electrolyte distribution while maintaining a low pressure drop to enabling smooth circulation.In contrast,poor flow-frame design can lead to increased pressure losses, non-uniform electrolyte distribution,and localised concentration imbalances,ultimately degrading system performance [39].As the stack size is strongly influenced by the arrangement of internal components, the flow-channel geometry becomes particularly important. Complex flow paths can restrict electrolyte transport,resulting in uneven distribution,local heating,and hotspot formation [4O].While externally fed configurations require additional channels that increase stack size and introduce higher risks of leakage and mechanical failure,internally fed manifold designs rely on proper manifold geometry and operating pressure to achieve uniform electrolyte delivery.Accordingly,this work adopts an internally fed flow-frame configuration,which offers a more compact stack design and reduces the risk of leakage, thereby improving overall reliability and durability.

# 3.2.COMSOL & MATLAB model

In order to evaluate the shunt resistance of the flow frame,simulations were carried out using COMsOL?.A three-dimensional model was developed by exporting the geometry from a 3D design software (Autodesk Fusion) and subsequently defining the flow frame structure within COMsOL.The material properties of both the electrolyte and the structural components were incorporated into the model. This approach enabled an accurate evaluation of manifold resistance associated with the flow channels.The equivalent electrical circuit of the VRFB shunt current network was developed based on methodologies reported in Refs.[l4,29].The governing equations for shunt current evaluation were formulated using Kirchhoff's Law.These equations were subsequently implemented in MATLAB to enable numerical analysis of the current distribution across the manifold and flow channels.A key feature of the developed model is the incorporation of SoC-dependent cell internal resistance.As the internal resistance varies dynamically with SoC,a lookup table is employed to update the resistance values during simulation,and data is shown in Fig.S1.The internal resistance at each SoC was obtained experimentally using electrochemical impedance spectroscopy (EIS) measurements performed on a single-cell VRFB.The SoC of the battery was evaluated following the approach presented in Fig.3,ensuring accurate coupling between SoC variation and resistance update. This approach enables the model to closely represent the practical behaviour of the battery under different operating conditions.

![](images/b386fe3170f2e83c0f6751b890886108bc344d21f747146196c8ae8793f7971e.jpg)  
Fig. 3.Flowchart of the proposed computation algorithm during charging.

# 3.2.1.Simulation details

In this study, the numerical workflow combines a 3D COMsOL model with a MATLAB-based shunt-current network solver.The COMSOL model(COMSOL Multiphysics 6.2, Build 290) uses the Electric Currents interface (AC/DC Module) on the imported 3D flow-frame geometry.

The governing equations correspond to electric-current conservation and the electric field-potential relation: $\begin{array} { r } { \nabla \cdot \mathbf { J } = \mathbf { Q } _ { \mathrm { j , v } } , \mathbf { J } = \sigma \mathbf { E } + \mathbf { J } _ { \mathrm { e } } , } \end{array}$ and $\mathrm { E = }$ $- \nabla \ V .$ Material properties for the electrolyte domain were specified as an electrical conductivity $\left( \sigma \right)$ and a relative permittivity of $\left( \varepsilon _ { \mathrm { r } } \right)$ taken from Table S2. Electric insulation was applied on all boundaries except for a ground boundary and a current terminal where a current was imposed. All simulations were performed as a stationary study; the resulting linear system $_ { ( > 3 0 0 \mathrm { K } }$ degrees of freedom） was solved using an iterative conjugate-gradient method with algebraic multigrid (AMG） preconditioning. The baseline mesh used for the reported results corresponds to the COMsOL“Extra fine”setting,comprising vertices and tetrahedral elements (minimum element quality 0.1599；average element quality 0.6o43).A mesh-refinement (grid-independence) analysis is included by evaluating the sensitivity of the extracted effective resistance to further mesh refinement.For coupling to the network model,COMsOL was used to compute effective electrical resistances (from the global evaluation output) for each geometry,and these values were imported into MATLAB to parameterize the shunt-current network. The MATLAB model employs a matrix-based nodal formulation; for an N-cell stack,a coupled set of 2N-1 equations is assembled from Kirchhoffs current law and Kirchhoffs voltage law and the resulting system is solved iteratively to update branch/loop currents until convergence based on SoC,defined by changes in all currents falling below a prescribed tolerance.

# 3.3.Model validation and assumptions

In the developed model, several assumptions were made to simplify the analysis while retaining the essential physical behaviour of the system [41-44]. The primary assumptions are as follows:

· The electrolyte flow rate through each cellis assumed to be constant, thereby neglecting local variations in flow distribution [41,43].   
· The internal resistance of each cell in a stack is considered constant at a given SoC [44].   
·The temperature is maintained at a constant value of ${ } ^ { 2 5 } \ ^ { \circ } \mathrm { C }$ [41,42, 44].

These assumptions simplify the mathematical modelling and numerical implementation while maintaining accuracy for analysing shunt current behaviour in the VRFB system.

# 3.4. MATLAB-based shunt current modelling framework

In the MATLAB-based modelling framework,the resistance data extracted from COMSOL were utilised as input parameters for the equivalent circuit model.Within the MATLAB environment, Kirchhoff's Voltage Law (KVL) and Kirchhoffs Current Law (KCL) were systematicallyapplied at each node of the circuit network to determine the corresponding node voltages.Based on these calculated voltages,the shunt currents were evaluated under three distinct operating conditions: charging,discharging,and the no-load (idle) condition.The governing KVL and KCL equations for the system are expressed as follows.The cell OCV is defined from the SoC of the cell [45] and calculated by Eqn. (1), where $\alpha$ and $\beta$ are 1.375 and 19.34,respectively.The internal resistance of each cell is a function of the SoC,given by Eqn. (2).

$$
V _ { c e l l , i } = \alpha + \frac { 1 } { \beta } l n \bigg ( \frac { S o C } { 1 - S o C } \bigg ) , \mathrm { w h e r e } i = 1 , 2 , . . . , n
$$

$$
r { = } f ( S o C )
$$

The nodal equation for the equivalent resistive network is expressed as Eqn.(3),where A is the conductance matrix,and $V = \{ V _ { t } , \bar { V _ { m } , } \bar { V _ { b } } \} ^ { T }$ is the unknown node voltage vector, where $V _ { t } , \ V _ { m } ,$ and $V _ { b }$ represent the top,middle,and bottom node voltages,respectively.B is the source vector including OCV contributions and terminal current $I _ { T }$

$$
A . V { = } B
$$

The branch currents are evaluated using Eqns. (4)-(8).

$$
I _ { R _ { a , i } } ^ { u p p e r } = \frac { V _ { m , i } - V _ { t , i } } { R _ { a } ^ { + } } , \mathrm { w h e r e } i = 1 , 2 , . . . , n
$$

$$
I _ { R _ { a , i } } ^ { l o w e r } = \frac { V _ { m , i } - V _ { b , i } } { R _ { a } ^ { - } } , \mathrm { w h e r e } i = 1 , 2 , . . . , n
$$

$$
I _ { R _ { b , i } } ^ { t o p } = \frac { V _ { t , i } - V _ { t , i + 1 } } { R _ { b } ^ { + } } , \mathrm { w h e r e } i = 1 , 2 , . . . , n
$$

$$
I _ { R _ { b , i } } ^ { b o t t o m } = \frac { V _ { b , i } - V _ { b , i + 1 } } { R _ { b } ^ { - } } , \mathrm { w h e r e } i = 1 , 2 , . . . , n
$$

$$
I _ { c e l l , i } = \frac { V _ { m , i + 1 } - V _ { m , i } + V _ { c e l l , i } } { r } , \mathrm { w h e r e } i = 1 , 2 , . . . , n
$$

The terminal cell voltage is obtained by Eqn. (9) and the current balance across the stack is ensured using Eqn. (1O), where $I _ { \mathrm { b y p a s s } , i }$ denotes the circulating current bypassing the ith cell due to shunt effects.

$$
\begin{array} { r l } & { V _ { t e r m , i } = I _ { c e l l , i } . r + V _ { c e l l , i } \mathrm { ~ w h e r e , } i = 1 , 2 , . . . , n } \\ & { } \\ & { I _ { T } = I _ { c e l l , i } + I _ { b y p a s s , i } \mathrm { ~ w h e r e , } i = 1 , 2 , . . . , n } \end{array}
$$

# 3.5. VRFB stack design

Atthe Sustainable Environergy Research Laboratory (SERL),two 10- cell VRFB stack configurations were designed,developed,and assembled to systematically examine shunt current behaviour.The two configurations,designated as short-flow frame and long-flow frame as shown in Fig.4,differ primarily in their flow-frame geometry,thereby enabling a controlled evaluation of the influence of electrolyte flow channel resistance on internal shunt current formation.

The short-flow frame adopts a conventional plate-and-frame architecture using thin graphite bipolar plates (SIGRACELL PV15,SGL Carbon, USA) with a thickness of $0 . 6 \mathrm { m m }$ ,as shown in Fig.4b.Itis designed to minimise electrolyte flow-path resistance through a simplified flow geometry.The flow channels have a uniform depth of $3 \mathrm { m m }$ ,awidth of $1 6 \mathrm { m m }$ ,and an effective length of $1 1 2 \mathrm { m m }$ ,arranged ina Z-type pattern to ensure uniform electrolyte distribution across the electrode surface. Each electrochemical cell employs graphite felt (SIGRACELL GFD4.65 EA,SGL Carbon,Germany) electrodes,thermally treated,with anactive area of $2 2 8 ~ \mathrm { c m } ^ { 2 }$ ,separated bya NafionTM117 membrane.

The long-flow frame is introduced as a modified version of the shortflow configuration, specifically redesigned to increase electrolyte flowpath resistance.While maintaining the same channel depth of $3 \ \mathrm { m m }$ and preserving the Z-type flow pattern, the channel width is reduced to $8 \mathrm { \ m m }$ and the effective channel length is increased to $5 3 6 \ \mathrm { m m }$ as illustrated in Fig.4c.The electrochemical cells in this configuration utilise thermally treated electrodes with an active area of $2 2 7 \mathrm { c m } ^ { 2 }$ All other stack components,materials,and assembly procedures are kept identical to the short-flow design,ensuring that any observed differences in stack behaviour can be attributed solely to changes in shunt resistance.

The assembled stack was fed with vanadium electrolyte $( 1 . 5 \mathrm { M }$ total vanadium in $4 \mathrm { ~ M ~ }$ total sulfate) using magnetic drive centrifugal pumps (Promivac Pumps,India) controlled bya variable frequency drive (VFD-MS300, Delta Electronics, Taiwan). The stack was subjected to chargingdischarging using a battery cycler (Arbin Instruments,LBT22013 25V-100A).

# 4．Results and discussion

Based on the derived circuit equations,a MATLAB code is developed and validated under three operating cases: charging and discharging

![](images/8a4eb4f4982c34f344a182f3892beb09ebe630ba45c265be4ad6dc75942c57bd.jpg)  
Fig.4.Flow configurations: (a) 10-cell VRFB stack,(b) short flow frame,and (c) long flow frame.

under load conditions and an idle (no-load) condition.This evaluation ensures that the model accurately captures system behaviour across all practical operating states.

# 4.1．Shunt current during load condition

Under load conditions,shunt current behaviour is influenced by the applied charging or discharging current and the internal resistance distribution within the stack.The interaction between electrolyte flow, manifold resistance,and cell voltage distribution determines the magnitude and distribution of shunt currents during operation. The following subsections analyse shunt current behaviour during charging and discharging conditions in detail.

# 4.1.1. Shunt current during charging

Considering a stack with lower shunt resistance,a higher fraction of current bypasses through the middle cells,resulting in lower cell voltages compared to those towards either end of the stack.This imbalance becomes more critical as the battery approaches a fully charged state (increasing SoC).At this stage,although the overall stack voltage,which is cumulative of each cell voltage,remains below the maximum rated value,the terminal cells experience voltages that exceed their permissible limits due to the redistribution of current.These over-voltages can be detrimental to the graphitic components of a stack because these high voltages (especially nearest to the positive terminal) would lead to an extreme oxidative environment.As a result, the graphite components, such as the bipolar plate and graphite felt,suffer exfoliation and subsequent $C O _ { 2 }$ gas evolution [46,47].This could lead to a significant rise in cell contact resistance,reduced voltage efficiencies,and irreversible damage to the stack.

![](images/9dda74110349436089553884f4d075baf32d134b6b15d5d368af9a9270f661ff.jpg)  
Fig.5.Celludaaiantsatevelsgaate

Fig.5a shows the effect of shunt current for a stack employing a flow frame with low shunt resistance (manifold resistance of $1 2 2 \Omega$ and a flow channel resistance of ${ 1 8 \ \Omega }$ ). It isclearly evident thatas the battery is charged,the imbalance in the cell voltages increases.In contrast, Fig.5b illustrates that increasing the manifold resistance to $7 0 2 \Omega$ and the flow channel resistance to $^ \textrm { \scriptsize 1 8 9 }$ effectively reduces the magnitude of shunt currents,thereby mitigating voltage imbalance across the stack. Furthermore,Fig. S3(a) and Fig.S3(b) illustrate the shunt current distribution in the positive flow channel and manifold of a 1O-cell VRFB stack during charging at different SoC.The positive channel shunt current shows a symmetric distribution along the stack,with current flowing from lower-index to higher-index cells and returning through the remaining cells.The magnitude of the channel shunt current gradually decreases with increasing cell index.In contrast, the positive manifold shunt current increases monotonically along the stack length due to the cumulative contribution of channel shunt currents,consistent with the equivalent circuit model and KCL.The maximum manifold shunt currentis therefore observed near the terminal cells.

Interestingly,for SoC nearing $9 0 \%$ ,the end cell voltages are above 1.7 V.For certain grades of graphitic bipolar plates,this deviation above $1 . 7 \mathrm { V }$ could lead to irreversible degradation of the graphite plate surface and hence failure of the stack.This can be mitigated by first studying the corrosion resistance of the graphite plate to be used for stack construction and then designing a suitable flow frame in order to limit these cell voltages to avoid degradation.

# 4.1.2. Shunt current during discharging

During discharging,the influence of shunt current is again pronounced in the middle cells,particularly when the manifold resistance is low.In such cases,the middle cells experience a higher bypass current, leading toa reduction in their effective cell voltage.As the SoC reduces (discharging),this reduction in cell voltages becomes more severe,and could drop below the minimum threshold value.Operating under these conditions for an extended period would force additional charge transfer from the affected cells,which leads to the generation of hydrogen gas at the anode side of the cell[46,47]. Fora high shunt manifold resistance, the resulting shunt current is negligible,exhibiting behaviour similar to that observed in the charging case.

In contrast to charging mode,the terminal cells are comparatively less affected during dis charge,as they are subjected to lower shunt current.Nevertheless,this imbalance between middle and end cells contributes to uneven depth of discharge and incomplete use of stored energy (orlower coulombic efficiency).Fig.6 illustrates the cell currents and corresponding voltages across the battery stack during discharging under varying SoC ranges for the lower shunt resistance condition.For the high shunt resistance case,the magnitude of shunt currents is effectively reduced (shown in Fig.S2),thereby mitigating voltage imbalance across the stack,similar to the behaviour observed in the charging model.Fig.S3(c) and Fig. S3(d) depict the current distribution through the manifold and flow channels during discharging.The overall trend of shunt current distribution in the positive channel and manifold remains the same;however, the direction and magnitude of the shunt currents are altered.The positive channel shunt current retains its symmetric profile,while the manifold shunt current increases progressively along the stack due to current accumulation.Variations in SoC significantly influence the shunt current levels in both the channel and manifold,reflecting changes in electrode potentials under discharge operation.

# 4.2.Shunt current under idle conditions (no-load)

When the battery is in the idle state,the total external current becomes zero $\left( I _ { T } = 0 \right)$ ). Under these conditions,with lower shunt resistance, only the shunt currents continue to circulate through the manifold and flow channels. This parasitic current gradually discharges the stack, even though no external load or charging source is connected.If the idle condition persists for an extended period, the accumulated effect of selfdischarge can significantly reduce the available SoC and,in extreme cases,bring the battery close to a fully discharged state.Such uncontrolled discharge significantly reduces the coulombic efficiency of the system,ultimately resulting in poor energy efficiency.Fig.7,highlights the influence of lower shunt resistance on cell current distribution and voltage behaviour across the battery stack during the idle condition at various SoC levels.For the high shunt resistance case under no-load conditions,shunt currents are effectively suppressed,thereby preventing stack self-discharge and maintaining the SoC across the stack (Fig.S4),consistent with the behaviour observed in the charging model. To summarise.the analvsis of shunt current behaviour under

![](images/f6232a9e0b3104314c52778aa21cbc75d508ad4953b46796fd86df6a189f6523.jpg)  
Fig.6.Cell currents and voltages during discharging under low shunt resistance at different SoC levels.

![](images/36af4eec53a2b7208969db6ac0757e0532f716f90385997d4485740d71dfab08.jpg)  
Fig.7.Cellcurrents and voltages during idle operation under low shunt resistance at diferent SoC levels.

charging,discharging,and idle conditions highlights several systemlevel consequences for an improperly designed flow field,having low manifold and flow channel resistance.The effect is most prominent during charging mode,where shunt current within the stack introduces significant cell-to-cell voltage imbalances,which directly affect the overall charging and discharging characteristics of the battery. Furthermore,as the battery approaches a fully charged state,this imbalance could lead to irreversible damage to the graphitic components and hence failure of the battery.For the discharging mode,the persistent voltage imbalance results in poor utilisation of the electrolyte and hence low voltage efficiencies.Lastly,at idle conditions,the prevailing shunt currents lead to rapid self-discharge of the electrolyte and affects the coulombic efficiency when the battery is again operated. Therefore,the developed model can be used to keep these degradation parameters in check during the development and design phase of flow frames fora flow battery.

![](images/7382b9aff8d5013f19f104e98adcb62e5c38fcddc7468b7fc47b8fb830f74fde.jpg)  
Fig.8.(a) Cell currents and voltages during charging at SoC levels above $9 0 \%$ under low shunt resistance,(b) progression of graphite plate degradation (low shunt resistance),(c) Cell currents and voltages during charging at SoC levels above $9 0 \%$ under high shunt resistance,(d) graphite bipolar plate exhibiting no observable egadati

# 4.3.Model-experiment linkage

To ensure that the simulations and experiments represent the same physical scenario,we aligned geometry,material properties,and operating conditions across both approaches.The simulated manifold/flowframe geometry matches the manufactured stack,and electrolyte/material properties were taken from measured values or manufacturer/ datasheet specifications. Simulations are reported only for the same operating conditions used experimentally (applied current, electrolyte flow rate,temperature of ${ } ^ { 2 5 } \ ^ { \circ } \mathrm { C }$ ,and the same state-of-charge window and test protocol).Initial and boundary conditions (e.g.,preconditioning/initial SoC and the imposed current/flow inputs) follow the experimental procedure.

# 4.4.Experimental validation of the developed model

A 10-cell VRFB stack was used as per the construction laid in section 3.5,as shown in Fig.8e. Two flow frames were considered: the shortflow frame and the long-flow frame.The short-flow frame is a simple flow design with channel resistance of $1 2 2 \Omega$ and manifold resistance of $^ \textrm { \scriptsize 1 8 } \Omega$ ，with overall shunt resistance of $^ { 1 4 0 ~ \Omega }$ .On the other hand, the long-flow frame has extended flow channels resulting in increased channel resistance of $7 2 0 \Omega$ and manifold resistance of $^ { 1 8 \Omega }$ as shown in Table 2.The two stacks utilising these flow frames were subjected to charge-discharge analysis in order to observe the performance in correlation to the model results.

# 4.4.1.Stack with short-flow frame

Based on this stack configuration,MATLAB-based simulations clearly indicate that under reduced shunt resistance conditions,attempts to charge the stack to a higher state-of-charge $( S 0 C \ge 9 0 \%$ would result in a severe voltage imbalance among the individual cells. Although the overall stack charging voltage is constrained below $1 7 \mathrm { ~ V ~ }$ (equivalent to $_ { 1 . 7 \mathrm { ~ V ~ } }$ per cell),the model predicts that the end cells experience significantly higher cell voltages.Specifically,at SoC levels above $9 0 \%$ ,cell1O and cell1 reach1.78 V,cell9 and cell 2 reach $1 . 7 4 \mathrm { V } _ { : }$ and cell 8 and cell 3 reach $1 . 7 2 \mathrm { V }$ ,whereas the remaining cells remain below $_ { 1 . 7 \mathrm { ~ V ~ } }$ ,as shown in Fig.8a.These end cells exceed the recommended upper voltage limit,which could lead to corrosion of the employed graphite plate.As discussed previously,such over-voltage conditions accelerate the graphitic oxidation and should result in irreversible degradationof the bipolar plates.

To validate the modelling predictions, the stack was charged to $9 0 \%$ SoC using the OCV method [45] and subsequently subjected to charge-discharge cycling within the considered SoC limit,as shown in

Table 2 Flow-frame characteristics and shunt current effects.   

<table><tr><td colspan="5">Flow-frame geometrical parameters</td></tr><tr><td>Flow Frame</td><td>Depth (mm)</td><td>Width (mm)</td><td>Length (mm)</td><td>Area (cm2）</td></tr><tr><td>Short-flow</td><td>3</td><td>16</td><td>112</td><td>228</td></tr><tr><td>Long-flow</td><td>3</td><td>8</td><td>536</td><td>227</td></tr><tr><td colspan="5">Stack performance and shunt current effects</td></tr><tr><td>Stack Design</td><td>Shunt Resistance ()</td><td>Corrosion</td><td>CE (%)</td><td>EE (%)</td></tr><tr><td>Short-flow</td><td>140</td><td>Severe</td><td>~59</td><td>~37</td></tr><tr><td>Long-flow</td><td>720</td><td>None</td><td>~70</td><td>~61</td></tr></table>

Fig.8f. The cycling response reveals pronounced overpotential losses during both charging and discharging,which intensify progressively with continued operation.During the first cycle,the discharge and charge capacities are limited to approximately $4 . 9 5 \mathrm { A h . L } ^ { - 1 }$ and $8 . 4 ~ \mathrm { A h }$ $\mathrm { L } ^ { - 1 }$ ,respectively,indicating significant irreversibility and poor electrochemical utilisation of the electrolyte.This disparity results in a low coulombic efficiency (CE) of only ${ \sim } 5 8 . 9 \%$ ，Furthermore,the voltage efficiency (VE) and overall energy efficiency (EE) are constrained to approximately $6 3 . 1 \%$ and $3 7 . 2 \%$ ,respectively.With continued cycling, the electrochemical performance degrades rapidly.After approximately 20 charge-discharge cycles,the useable capacity declines to nearly zero, signifying severe and irreversible degradation of the stack.These results clearly demonstrate substantial deterioration of the active materials under the applied operating conditions,further highlighting the critical impact of internal loss mechanisms on long-term stack stability.

Lastly,the stack was disassembled,and the condition of the bipolar plates was examined,as shown in Fig.8b.Visual inspection reveals pronounced graphitic degradation on the positive plates of the end cells subjected to higher voltages,while the positive plates of the remaining cells exhibited noticeable degradation.This experimental observation corroborates the model-predicted voltage imbalance and confirms the critical role of shunt current in driving localised bipolar plate degradation.

# 4.4.2. Stack with long-flow frame

Having established that the short-flow frame configuration results in low shunt resistance and severe cell-to-cell voltage imbalance, the study is extended to a long-flow frame configuration to evaluate its effectiveness in mitigating shunt current effects.The stack with the long-flow frame retains the same plate-and-frame architecture,materials,and assembly procedure as the short-flow stack,ensuring that any observed differences in electrochemical behaviour can be attributed exclusively to changes in the flow-frame geometry.

The long-flow configuration was subsequently evaluated using the developed MATLAB-based shunt current model.The simulated shunt current and individual cell voltage profiles at $\approx 9 0 \%$ SoC during charging are presented in Fig.8c.In contrast to the short-flow case,the results demonstrate a near-uniform voltage distribution across all cells, accompanied by negligible shunt current flow within the stack.The absence of significant over-voltage at the end cells indicates effective suppression of shunt current and the associated graphitic degradation.

Therefore, the stack was subjected to repeated charge-discharge cycling within the discussed SoC limits. The charge-discharge voltage profiles, presented in Fig.8g,remain stable and highly repeatable over successive cycles,indicating consistent electrochemical performance and effective suppression of internal parasitic currents.In contrast to the short-flow configuration,no progressive increase in overpotential or capacity fade is observed during cycling.Following completion of the cycling tests,the stack was disassembled for analysis of graphitic health. Visual inspection of the thin graphite bipolar plates,including those located near the positive terminal,reveals no evidence of graphitic corrosion or surface degradation as shown in Fig.8d.Consistent with these findings,no evidence of bipolar plate degradation was observed for the long-flow configuration,which is in agreement with the experimental observations reported in our earlier studies [17].

Additionally, these results clearly demonstrate that increasing the effective shunt resistance through long-flow frame design is an effective strategy formitigating shunt-current-induced bipolar plate degradation and enhancing long-term stack durability.The developed model could act as an effective and powerful screening tool during the design of flow frames in order to maintain the health of key active components (primarily the graphitic plates).The literature around the development of multi-cell stacks is limited,where the focus is bifurcated towards either minimising internal shunt current, pressure drop or thermal eficiency, primarily through the design of flow frames.The developed model would also act as a link between these three branches of flow frame development and serve stakeholders involved in the development of multi-cell electrochemical flow systems,such as flow batteries,electrolysers,fuel cells,etc.

# 5.Conclusions

# Data availability

This work shows that flow-frame geometry critically influences shunt current behaviour and long-term durability in VRFB stacks.The proposed shunt current model establishes a clear link between parasitic current path and electrode degradation,accurately capturing shunt current behaviour under charging,discharging，and idle operating conditions and revealing significant cell-to-cell voltage imbalance.The modelling predictions are experimentally validated using a1O-cell VRFB stack incorporating two flow-frame designs: a short-flow frame with low shunt resistance and a long-flow frame with high shunt resistance. Longterm charge-discharge cycling shows that the short-flow configuration experiences accelerated degradation and reduced electrochemical performance,whereas the long-flow configuration exhibits improved voltage uniformity and enhanced durability,consistent with the model predictions.The analysis further shows that while charging,low shuntresistance flow frames are most severely affected,with end cells experiencing voltages beyond their rated limits and accelerated bipolar plate and active material degradation，while middle cells operate at comparatively lower voltages,consistent with earlier experimental observations. Overall, the proposed modelling framework confirms previous experimental observations and provides a practical design tool for optimising flow-frame geometry,voltage monitoring,and control strategies to reduce self-discharge and improve the long-term efficiency and reliability of VRFB systems.This modelling approach provides stack designers with valuable insight prior to stack development,enabling optimisa421 tion of both stack performance and durability.

# CRediT authorship contribution statement

Vishnu K:Writing -review & editing,Writing- original draft, Visualization, Validation, Software,Methodology,Investigation,Formal analysis, Data curation, Conceptualization. Nishant Beriwal: Writing - review & editing, Visualization, Validation,Methodology,Investigation, Formal analysis, Data curation, Conceptualization. Sumit Kumar Pramanick:Writing-review& editing,Writing-original draft,Visualization,Validation，Supervision,Resources,Project administration, Methodology,Investigation, Funding acquisition,Formal analysis,Data curation, Conceptualization. Anil Verma: Writing - review & editing, Writing - original draft,Visualization,Validation,Supervision,Re-Sources,Project administration,Methodology, Investigation, Funding acquisition, Formal analysis,Data curation, Conceptualization.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Acknowledgments

The authors gratefully acknowledge the financial support provided by the Department of Science and Technology (DST),Government of India,under the projects DST/TMD/EWO/NICA/2020/34,DST/TMD/ MES/2K18/54,and DST/TMD/MECSP/2K17/07.The authors also acknowledge the facilities and support from the SIEVE laboratory, IIT Delhi.

# Appendix A. Supplementary data

Supplementary data to this article can be found online at https://doi. org/10.1016/j.jp0ws0ur.2026.240002.

Data will be made available on request.

# References

[1] Q. Hassan,P. Viktor, T.J. Al-Musawi, B.M. Ali, S.Algburi, H.M. Alzoubi, A.K. Al-Jiboory, A.Z. Sameen, H.M. Salman, M. Jaszczur, The renewable energy role in the global energy transformations, Renew. Energy Focus 48 (2024) 100545.   
[2] A. Zahedi, A review of drivers, benefits,and challenges in integrating renewable energy sources into electricity grid, Renew. Sustain. Energy Rev.15 (9) (2011) 4775-4779.   
[3] M. Farrokhabadi, B.V. Solanki, C.A. Canizares, K. Bhattacharya, S. Koenig, P. S. Sauter, T.Leibfried, S. Hohmann, Energy storage in microgrids: compensating for generation and demand fluctuations while providing ancillary services, IEEE Power Energy Mag.15 (5) (2017) 81-91. [4] T.-T. Ku, C.-H. Lin, C.-T.Hsu, C.-S. Chen, Z.-Y. Liao,S.-D. Wang,F.-F. Chen, Enhancement of power system operation by renewable ancillary service, IEEE Trans. Ind. Appl. 56 (6) (2020) 6150-6157.   
[5] A.Lucas, S. Chondrogiannis, Smart grid energy storage controler for frequency regulation and peak shaving, using a vanadium redox flow batery, Int. J. Electr. Power Energy Syst. 80 (2016) 26-36.   
[6] A. Aluko, A. Knight, A review on vanadium redox flow battery storage systems for large-scale power systemsapplication, IEE Access 11 (2023) 13773-13793. [7] N. Beriwal,A. Verma, Development of economical and highly eficient electrolyte using vanadium pentoxide for vanadium redox flow battery,Environ. Sci. Pollut. Control Ser.29 (48) (2022) 72187-72195.   
[8] Y. Liang, Y. Yao, Designing modern aqueous batteries, Nat. Rev. Mater. 8 (2) (2023) 109-122.   
[9] J. Ye,L. Xia, H.Li,F.P.G.de Arquer, H. Wang, The critical analysis of membranes toward sustainable and efficient vanadium redox flow batteries, Adv. Mater. 36 (28) (2024) 2402090.   
[10] K. Vishnu, P.T. Bankupalli, S. Pramanick, A. Verma, Advanced battery management system for standalone vrfb applications, in: 2023 11th International Conference on Power Electronics and ECCE Asia (ICPE 2023-ECCE Asia), IEEE, 2023, pp.1805-1810.   
[11] D. Riccardo, L. Baumann, A. Damiano, E. Boggasch, A vanadium-redox-flowbattery model for evaluation of distributed storage implementation in residential energy systems, IEEE Trans. Energy Convers.30 (2) (2014) 421-430.   
[12] K.J. Kim, M.-S. Park, Y.-J. Kim, J.H. Kim, S.X. Dou, M. Skyllas-Kazacos, A technology review of electrodes and reaction mechanisms in vanadium redox flow batteries, J. Mater. Chem.A 3 (33) (2015) 16913-16933.   
[13] N.M. Delgado, R. Monteiro, J. Cruz, A. Bentien, A. Mendes, Shunt currents in vanadium redox flow batteries-a parametric and optimization study, Electrochim. Acta 403 (2022) 139667.   
[14] Y.-S. Chen, S.-Y.Ho, H.-W. Chou,H.-J. Wei, Modeling the effect of shunt current on the charge transfer eficiency of anall-vanadium redox flow battery, J. Power Sources 390 (2018) 168-175.   
[15] F. Xing, H. Zhang, X. Ma, Shunt current loss of the vanadium redox flow battery, J. Power Sources 196 (24) (2011) 10753-10757.   
[16] M. Skylas-Kazacos, J. McCann, Y. Li, J. Bao, A. Tang, The mechanism and modelling of shunt current in the vanadium redox flow battry, ChemistrySelect 1 (10) (2016) 2249-2256.   
[17] N. Beriwal, K. Vishnu, A. Verma, Shunt current associated bipolar plate degradation in a multi-cellvanadium redox flow battry, J. Energy Storage 131 (2025) 117607.   
[18] P.R. Prokopius, Model for calculating electrolytic shunt path losses in large electrochemical energy conversion systems, No. NASA-TM-X-3359 (1976).   
[19] H. Fink, M. Remy, Shunt currents in vanadium flow batteries: measurement, modelling and implications for eficiency, J. Power Sources 284 (2015) 547-553.   
[20] A. Yin, S. Guo, H.Fang, J. Liu, Y.Li, H. Tang, Numerical and experimental studies of stack shunt current for vanadium redox flow battery, Appl. Energy 151 (2015) 237-248.   
[21] W. Tang, Q. Wu, Z. Richardson, Equivalent heat circuit based power transformer thermal model, IEE Proc.Elec. Power Appl.149 (2) (2002) 87-92.   
[22] Q. Xu, T. Zhao, C. Zhang, Effects of soc-dependent electrolyte viscosity on performance of vanadium redox flow batteries, Appl. Energy 130 (2014) 139-147.   
[23] A. Trovo, G. Marini, A. Sutto,P. Alotto, M. Giomo,F. Moro, M. Guarnieri, Standby thermal model of a vanadium redox flow battery stack with crossover and shuntcurrent effects, Appl. Energy 240 (2019) 893-906.   
[24] Trovo, M. Guarnieri, Standby thermal management system for a kw-class vanadium redox flow batery, Energy Convers. Manag. 226 (2020) 113510.   
[25] P. Aloto Trovo, M. Giomo,F. Moro,M. Guarnieri, A validated dynamical model of a kw-class vanadium redox flow battery, Math. Comput. Simulat. 183 (2021) 66-77.   
[26] H. Chen, M. Cheng, X.Feng,Y. Chen,F. Chen, J. Xu, Analysis and optimization for multi-stack vanadium flow battery module incorporating electrode permeability, J. Power Sources 515 (2021) 230606.   
[27] Xiong, Y. Yang, J. Tang, Y. Li, Z. Wei, Y. Su, Q. Zhang, An enhanced equivalent circuit model of vanadium redox flow battery energy storage systems considering thermal effects,IEEE Access 7 (2019) 162297-162308.   
[28] Y. Zhang, J. Zhao, P. Wang, M. Skylas-Kazacos, B. Xiong, R. Badrinarayanan, A comprehensive equivalent circuit model of all-vanadium redox flow battery for power system analysis, J. Power Sources 290 (2015) 14-24.   
[29] H.-W. Chou,F.-Z. Chang, H.-J. Wei, B. Singh, A. Arpornwichanop,P.Jienkulsawad, Y.-S. Chou, Y.-S. Chen, Locating shunt currents in a multistack system of allvanadium redox flow batteries, ACS Sustain. Chem. Eng. 9 (12) (2021) 4648-4659.   
[30] Q. Ye,J. Hu, P. Cheng, Z. Ma, Design trade-offs among shunt current, pumping loss and compactness in the piping system of a multi-stack vanadium flow battery, J. Power Sources 296 (2015) 352-364.   
[31] S. Konig, M. Suriyah, T.Leibfried, Model based examination on influence of stack series connection and pipe diameters on efficiency of vanadium redox flow batteries under consideration of shunt currents, J. Power Sources 281 (2015) 272-284.   
[32] F.Han, W.Wang,P.Li,L. Xian,F.Yang, X. Ran, Investigations on thermal interface and its impact on heat transfer performance in a large-scale water tank, Appl. Therm. Eng.262 (2025) 125214.   
[33] A. Glazkov, R. Pichugov, P.Loktionov,D. Konev, D. Tolstel, M. Petrov, A. Antipov, M.A. Vorotyntsev, Current distribution in the discharge unit of a 1O-cell vanadium redox flow battery: comparison of the computational model with experiment, Membranes 12 (11) (2022) 1167.   
[34] S. Kim, E. Thomsen, G. Xia, Z. Nie, J. Bao, K. Recknagle, W. Wang, V. Viswanathan, Q. Luo, X. Wei, et al., 1 kw/1 kwh advanced vanadium redox flow battery utilizing mixed acid electrolytes, J. Power Sources 237 (2013) 300-309.   
[35] F. Moro,A. Trovo, S. Bortolin, D. Del Col, M. Guarnieri, An alternative low-loss stack topology for vanadium redox flow battery: comparative assessment, J.Power Sources 340 (2017) 229-241.   
[36] M. Guarnieri, A. Trovo,A. D'Anzi, P. Alotto, Developing vanadium redox flow technology on a 9-kw 26-kwh industrial scale test facility: design review and early experiments, Appl. Energy 230 (2018) 1425-1434.   
[37] R. Ye, D. Henkensmeier, S.J. Yoon, Z. Huang, D.K. Kim, Z. Chang, S. Kim, R.Chen, Redox flow batteries for energy storage: a technology review, J. Electrochem. Energy Convers. Storage 15 (1) (2018) 010801.   
[38] M.M. Rahman, M.M. Islam, M. Shafiullah, M.A. Islam, M.A.R. Chowdhury, M. H. Zahir, Advancing grid integration with redox flow batteries: an engineering and economic review, Green Chem. Lett. Rev.18 (1) (2025) 2507333.   
[39] N. Gurieff, C. Cheung, V. Timchenko, C. Menictas, Performance enhancing stack geometry concepts for redox flow battery systems with flow through electrodes, J. Energy Storage 22 (2019) 219-227.   
[40] W. Sharmoukh, Redox flow batteries as energy storage systems: materials, viability,and industrial applications,RSC Adv.15 (13) (2025) 10106-10143.   
[41] Y.S. Chen, S.Y. Ho, H.W. Chou, H.J. Wei, Modeling the effect of shunt current on the charge transfer efficiency of an all-vanadium redox flow battery, J. Power Sources 390 (2018) 168-175.   
[42] C. Yin, S. Guo, H. Fang, J. Liu, Y.Li, H. Tang, Numerical and experimental studies of stack shunt current for vanadium redox flow battery, Appl. Energy 151 (2015) 237-248.   
[43] C. Zhang, T.S. Zhao, Q. Xu,L. An, G. Zhao, Efects of operating temperature on the performance of vanadium redox flow batteries, Appl. Energy 155 (2015) 349-353.   
[44] P.K. Vudisi, S. Jayanti, R. Chetty, Model for rating a vanadium redox flow battery stack through constant power charge-discharge characterization, Batteries 8 (8) (2022) 85.   
[45] M. Kapoor, N. Beriwal, A. Verma, Maximizing durability of vanadium redox flow battery by evaluating electrolyte-repair-point, J. Energy Storage 32 (2020) 101759.   
[46] M. Matsumoto, T. Manako, H. Imai, Electrochemical STM investigation of oxidative corrosion of the surface of highly oriented pyrolytic graphite, J. Electrochem. Soc.156 (10) (2009) B1208.   
[47] S. Rudolph, U. Schroder, I. Bayanov, G. Pfeiffer, Corrosion prevention of graphite collector in vanadium redox flow battery, J. Electroanal. Chem. 709 (2013) 93-98.