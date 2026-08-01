# State of charge estimation of vanadium redox flow battery based on time-frequency feature and layered physical constraints

Xuan Liu aD,Lifeng Caoa, KaiLia, Jinquan Wang ab, Gang Danga, Mifeng Rena, Gaowei Yan $\mathbf { a } \oplus \mathbf { , * }$ , Suxia Ma a

College of Electrical and Power Engineering,Taiyuan Universityof Technology,Taiyuan,O3oo24,China 'Shanxi Saiying Energy Storage Technology Co.,Ltd.,Taiyuan O3o031,China

# HIGHLIGHTS

# GRAPHICAL ABSTRACT

Dataacquisition Data export Frequency domain Time domain feature extraction feature extraction Split Endogenous variable DCT embedding.. A Cross feature Exogenous Input data variable Stack embedding VRFB platform State of Charge Estimation Framework Physical c Feature fusion BMS Physical feature ★ output lconstraint enhancement Physical memory unit Endogenousconvolutonmodule ↑ Enhanced ↓ SoCpred features Cross-Attention module Nernst layer ? Enhanced features

# ARTICLE INFO

# ABSTRACT

Keywords:
Vanadium redox flow battery
State of charge
Time-frequency features
Physical constraints
Dynamic operating conditions
Endogenous-exogenous variables

Accurate estimation of the state of charge (SoC)of vanadium redox flow battery (VRFB)is a key prerequisite for ensuring safe battery operation and facilitating eficient energy management and optimized dispatch strategies in energy storage systems. However,under high frequency dynamic operating conditions such as grid frequency regulation and abrupt load variations, VRFB operating parameters exhibit pronounced time varying behavior and complex multiphysics coupling efects,posing severe challenges to SoC estimation.To address these challenges,this paper proposes a SoC estimation framework based on time-frequency feature fusion and physical constraints.Time-frequency feature extraction module is developed to transform raw operational signals into time-frequency feature,and achieve their complementary fusion, thereby enhancing the feature representation capabilityof the model.Internal batery state variables are treated as endogenous variables, whereas operating conditions and external disturbances are treated as exogenous variables.Differentiated embedding mechanism is introduced to model the dynamic contributions of these two types of variables separately,aleviating the isse of variable heterogeneity.In addition,hierarchical physical constraints are designed.Electrochemical laws are incorporated .Experimental results show high accuracy with MAE below $1 \%$ RMSE below $1 . 1 \%$

# 1. Introduction

With the advancement of carbon peaking and carbon neutrality targets,the penetration of renewable energy continues to increase.The deployment of renewables such as wind and photovoltaic power has grown rapidly; however,their inherent intermittency and variability exacerbate supply-demand imbalances and increase the pressure on peak regulation and frequency control, thereby constraining high-level renewable energy utilization to some extent [1].To enhance the grid's capability to accommodate renewables,grid-side energy storage technologies with both peak-shaving,valley-filling and power-smoothing capabilities are urgently needed [2]. Redox flow battery (RFB) systems have emerged as a premier solution for large-scale energy storage owing to their unique ability to decouple power and capacity.While various RFB chemistries have been explored,the selection of electrolytes remains a critical determinant of system cost and reliability. For instance,although iron-based RFB or zinc-based RFB present significant cost advantages,their widespread deployment is still hindered by unsatisfactory operational stability and complex cross-contamination issues [3]. Among RFB technologies, the Vanadium redox flow battery (VRFB) offers distinct advantages,including decoupled power and capacity,prolonged cycle life, exceptional scalability,and superior safety. These characteristics render it highly competitive in long-duration energy storage and high-frequency charge-discharge applications [4],and it currently represents the most widely implemented and commercially mature system [5].Furthermore,within the VRFB system,the state of charge (SoC) serves as a crucial metric governing charge-discharge control,available capacity evaluation,and overall operational safety. However,under dynamic operating conditions,complex electrochemical reactions within the stack render the mapping between measurable signals and SoC strongly nonlinear and time-varying. Consequently, neither simplified physics-based models nor purely data-driven models can achieve high-accuracy SoC estimation across a wide range of operating conditions.Therefore,it is necessary to develop a highprecision and highly adaptive model for SoC estimation under dynamic conditions to ensure the safe,economical,and efficient operation of VRFB [6].

Existing SoC estimation approaches mainly include coulomb counting,the open-circuit voltage method abbreviated as OCV,model-based filtering,and data-driven methods [7].Coulomb counting obtains charge variation by integrating the current [8].It is simple and suitable for real-time implementation,yet it is highly sensitive to the initial SoC and current-measurement errors.In addition, the integration operation inevitably accumulates errors,making unbiased estimation difficult to guarantee during long-term dynamic operation.The OCV method infers SoC by inverting the OCV-SoC mapping [9],but it is limited in practice because sufficiently long rest periods are difficult to satisfy frequently. In addition,the voltage sensitivity is low in certain SoC intervals,and the measured OCV is susceptible to measurement noise,temperature disturbances,and the slow evolution of electrolyte composition and concentration induced by transmembrane ion transport [1O,11],which can lead to OCVdrift and introduce systematic bias.Model-based filtering methods describe internal battery processes using equivalent-circuit models or simplified electrochemical models [12,13],and estimate SoC with filters such as the extended Kalman filter abbreviated as EKF [14], the unscented Kalman filter abbreviated as UKF [15],and the cubature Kalman filter abbreviated as CKF [16].Their advantage is that,when the model structure is appropriate and the noise approximately follows Gaussian assumptions, they can recursively fuse current and terminalvoltage information with relatively low computational complexity, producing accurate SoC estimates that are suitable for integration into battery management systems abbreviated as BMs [17].In addition to the above methods,Ref.[18] proposed a digital twin-based VRFB SoC estimation method.By constructing a virtual replica that integrates a zero-dimensional dynamic model and real-time sensing data,real-time and accurate SoC prediction was achieved.However, these methods strongly rely on model fidelity and parameter accuracy.Under abrupt load changes and flow-rate regulation, the transient terminal-voltage response is dominated by ohmic drop and polarization dynamics,which reduces the identifiability of the voltage-SoC relationship.Meanwhile, changes in temperature and mass-transport conditions can lead to fast time variation of polarization parameters,causing structural mismatch under fixed-parameter or steady-state assumptions.When the mismatch is significant or the noise-statistics assumptions are violated,filter consistency deteriorates,estimation bias may accumulate,and divergence can occur in extreme cases [19],thereby undermining reliability under dynamic conditions.

In contrast,data-driven methods do not require an explicit physical model and do not depend on internal parameters that are dificult to measure,while still achieving strong nonlinear fiting capability [20, 21].Data-driven approaches have been widely used for battery SoC estimation.Ref.[22] developed a multi-head-attention-driven long shortterm memory network that accounts for flow rate and complex charge and discharge conditions.By removing dependence on physics-based models,it provides a framework that can be applied by BMS engineers without requiring prior electrochemical knowledge.Ref.[23] also proposed using a back-propagation neural network abbreviated as BPNN to predict SoC for VRFB,and improved the network via Bayesian regularization to achieve real-time,high-accuracy prediction.Li et al. Ref.[24] developed an online SoC prediction model based on viscosity and temperature using a feed-forward neural network,which can be programmed and integrated into VRFB control systems.

Nevertheless,SoC estimation for VRFB is essentially a complex multivariate time-series modeling problem. Under dynamic conditions, different inputs such as voltage,current,temperature,and flow rate influence SoC through different mechanisms.Many existing data-driven models embed and process all input signals in a homogeneous manner,which can cause feature coupling and contribution mixing.As a result,the model may fail to distinguish the roles of different variables during dynamic evolution, limiting estimation accuracy and generalization under complex scenarios.To alleviate feature coupling caused by homogeneous treatment, Transformer-based models that introduce hierarchical embeddings for endogenous and exogenous variables have shown unique advantages in recent years.By representing different variable types in a differentiated way and modeling them with attention,they are expected to improve representation capability for complex dynamics. The TimeXer model in Ref.[25] separates endogenous and exogenous variables,and adopts hierarchical embeddings and differentiated attention to bridge causal information from external conditions into feature extraction for internal time series.Applying this endogenous-exogenous hierarchical embedding idea to VRFB SoC estimation can enable more accurate separation and modeling of the dynamic contributions of different variables.By effectively leveraging exogenous operating-condition information,it mitigates feature coupling caused by homogeneous processing and improves feature expressiveness and estimation accuracy for VRFB in dynamic operation.

On the other hand,grid-connected VRFB operation also faces challenges from high-frequency dynamic disturbances.Load fluctuations can induce high-frequency oscillations in voltage and current,and pump-speed regulation combined with fluid-electrochemical coupling further aggravates nonlinearity and time variation of the signals [26]. Feature extraction methods that rely only on time-domain amplitude variations often fail to distinguish informative high-frequency dynamics from high-frequency random noise.This can drive the model to overfit transient fluctuations and weaken robustness across operating conditions.Therefore,some studies have introduced frequency-domain or time-frequency-domain feature extraction to enhance the completeness of dynamic characterization.Ref. [27] proposed a CNN with timefrequency learning capability，where two-dimensional spectrogram analysis improves lithium-ion SoC estimation accuracy across temperatures.Ref.[28] combined a simplified electrochemical model with electrochemical impedance spectroscopy and addressed poor temperature adaptability and limited accuracy in lithium-ion SoC estimation by selecting key frequency features. Ref.[29] proposed a frequencydomain feature extractor based on a channel-attention mechanism and established frequency dependence among channels via the discrete cosine transform abbreviated as DCT,providing more comprehensive time-frequency features for SoC predictors. These studies demonstrate that incorporating frequency-domain analysis can enhance the completeness of input representations and provides an effective route to overcome limitations of purely time-domain methods under dynamic conditions.Although such approaches can utilize frequency-domain information for SoC estimation,they still fall withina purely data-driven paradigm and lack physical-consistency constraints.As a result,under extreme dynamics or distribution shift, the model may output estimates that violate electrochemical principles.Related studies have introduced physics-informed neural networks abbreviated as PINN [30], integrating key physical laws of electrochemical processes into the loss function [31,32] to improve physical consistency and interpretability of data-driven methods.Nevertheless,practical challenges remain in high-dimensional partial differential equation constraints,loss-weight tuning,noise sensitivity,and training stability.This motivates the need for a more refined way to embed electrochemical physical constraints into data-driven frameworks.

Based on the above analysis, this study targets VRFB dynamic operating conditions with time-varying current and time-varying flow rate, and proposes a SoC estimation method that combines time-frequency features with hierarchical physical constraints.The core idea is to treat the historical SoC sequence as endogenous state information,and to treat current,terminal voltage,OCV,temperature,and electrolyte flow rate as exogenous operating-condition information.Differentiated embeddings are used to handle variable heterogeneity.Meanwhile, time-frequency representations are introduced to achieve comprehensive feature characterization under dynamic conditions,and electrochemical priors are incorporated during learning to construct physical constraints,thereby enhancing physical plausibility and robustness of the estimates.Experimental results demonstrate that,across different operating conditions,the proposed method achieves an average mean absolute error (MAE) below $0 . 6 \%$ and an average root mean squared error (RMSE) below $0 . 7 \%$ ，with the coefficient of determination $( \mathbb { R } ^ { 2 } )$ exceeding 0.99.

The main innovations of this paper can be summarized in the following aspects:

(1) Time-frequency feature extraction module: Extracts time-domain and frequency-domain features from the raw signals and fuses them. The module captures high-frequency oscillations and slow-changing trends of parameters under dynamic conditions.Alleviates the limitations of pure time-domain feature extraction and achieves comprehensive feature representation under dynamic conditions.

(2)Electrochemical layered physical constraints:Embeds electrochemical prior knowledge from Faraday law and the Nernst equation into the network structure.Integrates physical constraints into different modules to ensure that the estimation results satisfy electrochemical and thermodynamic laws.The output of model conforms to physical laws.

(3) Introduction of a layered embedding strategy for endogenous and exogenous variables: Endogenous variables are embedded using patch tokens and global tokens,while exogenous variables are embedded at the variable level using variate tokens.This enables the separation and effective utilization of the dynamic contributions of both types of variables,alleviating the feature coupling problem caused by the homogeneous treatment of variable information.

# 2.Problem motivation and mechanism analysis

# 2.1.Electrochemical mechanism of VRFB

VRFB uses vanadium ions in different valence states as active materials,dissolved in the positive and negative electrolyte solutions,with a circulation pump driving the electrolyte to circulate within the stack. The electrode reactions during operation are as follows:

Negative Electrode: $\mathbf { V } ^ { 3 + } + e ^ { - }  \mathbf { V } ^ { 2 + }$

During the charging process,the applied current drives the reduction of the negative electrode $\mathsf { V } ^ { 3 + }$ to $\mathrm { V } ^ { 2 + }$ . The positive electrode $\scriptstyle \mathrm { V O } ^ { 2 + }$ is oxidized to ${ \mathrm { V O } _ { 2 } } ^ { + }$ .The battery system converts electrical energy into chemical energy.The discharge process is the reverse.The SoC of each side is usually defined by the concentration of reactive ions in the storage tank of that side.The definition of the negative electrode SoC is as follows:

Prior to the commencement of the experiments in this study,the positive and negative electrolytes were strictly balanced, possessing identical initial volumes,equivalent total vanadium concentrations, and an identical initial SoC. Since the experiments in this work involved only a limited number of charge-discharge cycles,and the coulombic efficiency consistently remained between $9 4 . 2 5 \%$ and $9 5 . 5 3 \%$ during the testing.Ref.[33] explicitly demonstrates that the VRFB achieves an average cycle life of 13,ooo cycles at an $8 0 \%$ depth of discharge (DOD).Similarly,Ref.[34] indicates that the energy efficiency of the VRFB remains stable at $7 3 . 6 \%$ after 450 charge-discharge cycles.For industrial-scale VRFB systems operating under stringent conditions of a $1 0 0 \%$ DOD and a 3C charge-discharge rate, the capacity loss is a mere $1 \%$ after 20,0o0 cycles [22].Given that the experiments in this study encompass onlya limited number of charge-discharge cycles,it is assumed that the accumulation of capacity imbalance induced by transmembrane crossover and side reactions during the experimental period is negligible and can thus be safely ignored.

Under these conditions,the numbers of electrons transferred on both sides are identical and the reaction progress evolves synchronously during charge and discharge,such that the tank SoC on the positive and negative sides are approximately equal in value.Therefore,in the subsequent derivations,we use the negative-tank SoC as an equivalent expression of the system-level SoC.The definition of the negative-side SoC is given as follows:

$$
\begin{array} { r l r } {  { S o C ^ { - } = \frac { c _ { \nabla ^ { 2 + } } } { c _ { \nabla ^ { 2 + } } + c _ { \nabla ^ { 3 + } } } } } \\ & { } & \\ & { c _ { \nabla ^ { 2 + } } = S o C ^ { - } \cdot C _ { \mathrm { t o t } } ^ { - } , \quad c _ { \nabla ^ { 3 + } } = ( 1 - S o C ^ { - } ) \cdot C _ { \mathrm { t o t } } ^ { - } } \end{array}
$$

where $c _ { i }$ represents the concentration, $\begin{array} { r l r } { i } & { { } = } & { \nabla ^ { 3 + } } \end{array}$ ， $\mathrm { V } ^ { 2 + }$ $C _ { \mathrm { t o t } } ^ { - }$ denotes the concentration of the negative electrode electrolyte.If the electrolyte concentration remains approximately constant over a certain time scale,the relationship between concentration and SoC can be obtained.SoC essentially reflects the degree of shift in the oxidationreduction equilibrium of the electrode's active material,and is a key internal state for characterizing the available capacity.

Essentially, the time evolution of SoC follows Faraday law, meaning the change in active material is proportional to the charge amount.

$$
\frac { d S o C ( t ) } { d t } = \frac { \eta _ { I } I ( t ) } { n F C _ { \mathrm { t o t } } V _ { \mathrm { e l e c } } }
$$

where $I ( t )$ is the current,with the charging direction considered positive. $\eta _ { I }$ is the current efficiency. $n$ is the number of electrons. $F$ is the Faraday constant. $V _ { \mathrm { e l e c } }$ is the effective electrolyte volume.After discretization, the commonly used ampere-hour integration formula is:

$$
S o C ( k ) = S o C ( k - 1 ) + \frac { \eta _ { I } I ( k ) \varDelta t } { C _ { \mathrm { n o m } } }
$$

where $C _ { \mathrm { n o m } }$ is the nominal capacity. This relationship reflects the charge conservation and accumulation characteristics of SoC. Thus,it can be seen that in the time domain, SoC is the integral state of current. The current integration,accumulated charge variation,and other timedomain features overa period essentiallyuse Faraday's law to describe the time-domain evolution of SoC.

It should be noted that Eqs.(5) and (6) are derived under the assumptions of well-mixed tanks and approximately constant total activespecies concentration and effective electrolyte volume over a short time scale.These equations thus describe the dominant charge-conservation process driven by the applied current,without explicitly accounting for the direct effects of membrane crossover and self-discharge on electrolyte concentration and SoC. Given that the experiments in this study are conducted over an hour-level duration, the impacts of crossover and self-discharge remain limited; therefore,this simplification constitutesa reasonable approximation for online SoC estimation under the investigated operating conditions.Nevertheless,we acknowledge that such effects may accumulate during long-term cycling,and future work will incorporate online concentration measurements to further refine the physical constraints and enable a dual-side SoC characterization.

On the other hand, the terminal voltage and SoC are related through thermodynamic constraints.Under thermodynamic equilibrium conditions,the electrode potential and the concentration of active material satisfy the Nernst equation.Taking the negative electrode as an example, by combining the concentration and SoC relationship,the following equation can be obtained,and the same applies to the positive electrode.The $E _ { \mathrm { O C V } }$ of the battery under equilibrium conditions can also be obtained.

$$
\begin{array} { l } { E _ { - } = E _ { - } ^ { 0 } + \displaystyle \frac { R T } { a F } \ln \left( \frac { 1 - S o C ^ { - } } { S o C ^ { - } } \right) } \\ { E _ { 0 \mathrm { C V } } ( S o C , T ) = E ^ { 0 ^ { \prime } } + \frac { 2 R T } { F } \ln \left( \frac { S o C } { 1 - S o C } \right) } \end{array}
$$

where $E ^ { 0 ^ { \prime } }$ denotes the formal potential. $R$ is the gas constant. $T$ is the absolute temperature.

For the experimental system in this study, $E ^ { 0 ^ { \prime } }$ is obtained from an offline equilibrium OCV calibration. Specifically,in the OCV-SoC calibration experiment,after each step,the current is set to zero and the cell is rested until the voltage stabilizes; the open-circuit voltage at the end of the rest period is recorded,and the corresponding SoC at that time is obtained simultaneously. The $E ^ { 0 ^ { \prime } }$ is then treated as an unknown to be identified and is solved by least-squares fitting over all data points.

$$
{ E ^ { 0 } } ^ { \prime } = \arg \operatorname* { m i n } _ { E ^ { 0 } } \sum _ { k = 1 } ^ { K } \left[ E _ { 0 \mathrm { C V } , k } - { E ^ { 0 } } ^ { \prime } - { \frac { 2 R T _ { k } } { F } } \ln \left( { \frac { S o C _ { k } } { 1 - S o C _ { k } } } \right) \right] ^ { 2 }
$$

The fitted $E ^ { 0 ^ { \prime } }$ is further used in the OCV expression of Eq. (8) and is also consistently applied in the subsequent physics-constrained branch for the Nernst-constraint calculation, ensuring that the thermodynamic parameters are consistent with the experimental system.Moreover, since the temperature range covered by our calibration and tests is relatively narrow,the formal potential is approximated as a constant. If a wider temperature span is involved,the formal potential can be formulated as a temperature-dependent function and the temperature term can be fitted simultaneously during the calibration stage.

The Nernst equation provides the thermodynamic relationship between SoC and the OCV.In the subsequent analysis,the positive and negative electrolytes are assumed to have identical volume and concentration. The reaction kinetics in the two half-cels are assumed to be in dynamic equilibrium,and the SoC of the positive and negative halfcells is considered identical. In practice,issues such as ion migration across membranes and mass transfer limitations occur,and the terminal voltage is affected by dynamic and impedance effects on top of the OCV.Therefore,in the time domain, the trend of terminal voltage is mainly determined by the slow changes in SoC and temperature,while the rapid fluctuations mainly arise from polarization reactions.

In this work, for mechanistic illustration,Eq.(8) is written at the single-cell level. For a series-connected stack consisting of $N$ identical cells,the stack open-circuit voltage equals the sum of the open-circuit voltages of all cells. Under the common assumption that all cells share the same SoC and temperature,the following proportional relationship holds.In our experiments,a reference single cell was connected in series with the stack's electrolyte loop,and both the reference cell and the stack were fed by the same positive and negative tanks.Meanwhile, the reference cell was kept fully open-circuited and was neither charged nor discharged.Therefore,a stack-level Nernst-type relationship can be written as:

$$
E _ { \mathrm { 0 C V , s t a c k } } ( \mathrm { S o C } , T ) = N _ { s } E _ { \mathrm { 0 C V , c e l l } } ( \mathrm { S o C } , T )
$$

In our experiments, the measured voltage signal corresponds to the stack voltage,and $N _ { s } = 1 9$

# 2.2.Mapping relationship between time-frequency feature and electrochemical mechanisms

During practical operation of a VRFB,the terminal voltage is typically determined jointly by the OCV and various polarization voltages. Indeed,in practical VRFB systems,the substantial discrepancy between the measured terminal voltage and the ideal Nernst potential is predominantly ascribed to electrochemical polarization.Recent research has further highlighted that the sluggish kinetics and inferior reversibility of the $\mathsf { V } ^ { 3 + } / \mathsf { V } ^ { 2 + }$ redox couple at the negative electrode constitute the primary physical origin of activation polarization [35]. The thermodynamic constraint described by the Nernst equation is only applicable under equilibrium conditions,whereas under current-carrying conditions,the terminal voltage can be expressed as:

$$
U ( t ) = E _ { \mathrm { { O C V } } } ( S o C ( t ) , T ( t ) ) - \eta _ { \mathrm { { a c t } } } ( t ) - \eta _ { \mathrm { { c o n c } } } ( t ) - I ( t ) R _ { \mathrm { { o h m } } } ( t )
$$

where $I R _ { \mathrm { o h m } }$ represents the ohmic loss contributed by the electrolyte, ion-exchange membrane,and related components. $\eta _ { \mathrm { a c t } }$ denotes the activation polarization caused by charge transfer. $\eta _ { \mathrm { c o n c } }$ denotes the concentration polarization induced by reactant concentration imbalance. Let $\Delta U _ { \mathrm { p o l } } ~ = ~ \eta _ { \mathrm { a c t } } + \eta _ { \mathrm { c o n c } } + I R _ { \mathrm { o h m } }$ ,then the terminal voltage can be decomposed as:

$$
U ( t ) = E _ { \mathrm { { O C V } } } ( S o C ( t ) , T ( t ) ) - A U _ { \mathrm { p o l } } ( t )
$$

where $E _ { 0 \mathrm { C V } } ( S o C , T )$ manifests as a slow drift trend in the voltage over time,especially when the polarization effect is small.By introducing the concept of electrochemical impedance,the small-signal batery voltage near a certain operating point can be written as:

$$
\varDelta U ( \omega ) \approx \varDelta E _ { \mathrm { O C V } } ( \omega ) + Z ( \omega ) \varDelta I ( \omega ) + n ( \omega )
$$

where $Z ( \omega )$ is the electrochemical impedance,which includes ohmic, activation,and concentration polarization. $n ( \omega )$ represents measurement noise and other high-frequency disturbances.Eq.(l3) is a typical small-signal frequency-domain formulation.It is obtained by linearizing the relationship between terminal voltage and current with respect to small perturbations around a given operating point,and by approximating the system as linear time-invariant within a finite observation window,thereby yielding a frequency-domain transfer relation.It should be emphasized that Eq.(l3) does not neglect activation or concentration polarization; on the contrary,these polarization processes arising from charge-transfer kinetics and mass-transport limitations,together with ohmic losses,constitute the major components of the electrochemical impedance.Related studies on flow batteries have quantitatively decomposed the impedance contributions from ohmic resistance, charge transfer,and diffusion using EIS measurements and physicsbased impedance models,and have employed them to characterize polarization variations under different operating conditions.

From the SoC evolution governed by Faraday's law,the local bridge between SoC and the frequency domain around this operating point can be expressed as:

$$
\Delta S o C ( \omega ) = \frac { \eta _ { I } } { C _ { \mathrm { n o m } } } \frac { 1 } { j \omega } \Delta I ( \omega )
$$

From the above equation,it can be seen that the SoC signal is dominated by low-frequency components.However, the polarization reactions embedded in the mid-to-high frequency components can affect SoC. Concentration polarization causes ion concentration nonuniformity within the battery,directly affecting the concentration ratio of active vanadium ions in the electrolyte.Ohmic polarization leads to energy loss in the form of heat during charging and discharging, resulting in a lower ion conversion ratio under the same energy input, and the actual SoC change is smaller than the theoretical value.Activation polarization reduces the reaction rate,causing ion conversion during charging and discharging to require a higher overpotential, which exacerbates the concentration gradient and further increases the estimation error of SoC.

# 3. Methodology

This section introduces the SoC estimation framework based on time-frequency feature extraction and layered physical constraints. Accurate SoC estimation under dynamic conditions is achieved through the feature extraction module, feature enhancement module,and physical constraint output module.The overall framework of the model is shown in Fig.1.First, time-series samples are constructed from the raw charge and discharge data.Next, time-domain and frequencydomain features are extracted to provide a more comprehensive feature representation for the model.Then, feature enhancement is performed through the physical memory unit, convolution module,and cross-attention mechanism.Finally, the estimation results are corrected through the Nernst equation constraint,outputting precise SoC estimation values.

# 3.1.Time-frequency feature extraction module

# 3.1.1. Frequency-domain feature extraction

To effectively capture the frequency-domain feature of charge and discharge signals,existing studies perform independent frequencydomain transformations on each channel and then fuse them trough simple concatenation and fully connected layers [29].However,this approach neglects the intrinsic coupling relationship between different physical quantities in the frequency-domain.To address this,this section introduces a cross-feature module to represent the frequencydomain interactions between channels.At the same time,by combining the single-channel frequency-domain features obtained from DCT,a more comprehensive feature representation is achieved.The overall workflow of this module is shown in Fig. 2.

To effectively obtain the frequency-domain characteristics of a single variable,the single-channel time-series signal is decomposed. The input features are divided along the channel dimension into d separate channel variables.The split channel variables are transformed into frequency-domain signals using DCT to extract their frequency-domain information.The cosine core term of the DCT basis function is defined as follows:

$$
\phi _ { j } ( m ) = \left\{ \begin{array} { l l } { \sqrt { \frac { 1 } { L } } } & { j = 0 } \\ { \sqrt { \frac { 2 } { L } } \cos \left( \frac { \pi j ( 2 m + 1 ) } { 2 L } \right) } & { 1 \leq j \leq L - 1 } \end{array} \right.
$$

where $L$ is the sampling length of the single-channel time-domain signal. $m$ represents the time-domain index,corresponding to the mth sampling point of the original signal. $j$ represents the frequency-domain index,corresponding to the frequency level. $m , j ~ \in ~ [ 0 , L - 1 ]$ $\phi _ { j } ( m )$ denotes the value of the $j$ th basis function at the mth sampling point.

Next,we need to obtain the representation of different components in the frequency-domain.Let the time-domain signal of the ith channel be $x _ { i }$ ,and its $j$ th DCT coefficient is defined as:

$$
F r e q _ { i } ( j ) = \sum _ { m = 0 } ^ { L } x _ { i } ( m ) \cdot \phi _ { j } ( m )
$$

where $F r e q _ { i } ( j )$ represents the frequency-domain information of the channel variable $x _ { i }$ at the $j$ th frequency component. $x _ { i } ( m )$ is the specific value of the mth sampling point in the sequence.

Through the aforementioned DCT single-feature extraction module, the frequency-domain characteristics of each channel are analyzed independently. Then,cross-feature extraction is performed,considering the intrinsic coupling between physical quantities.For example, fluctuations in current inevitably lead to voltage responses,and their frequency-domain relationship directly reflects the dynamic impedance characteristics of the battery.To model the frequency-domain coupling relationship between different channels,the cross-frequency-domain feature $C S M _ { p } ( q )$ is defined and can be computed using the following equation:

$$
C S M _ { p } ( q ) = F r e q _ { p } ( q ) F r e q _ { q } ( q ) , ( p < q )
$$

By calculating the cross-frequency-domain feature $\begin{array} { r } { C _ { d } ^ { 2 } = \frac { d ( d - 1 ) } { 2 } } \end{array}$ ,new features representing the second-order interaction information between channels are obtained.This feature characterizes the coupling strength of different channels in frequency response and supplements the interaction information not represented in the single-channel spectral features.Finally, the original single-channel frequency-domain feature and the newly generated cross-frequency-domain feature are concatenated to form a more comprehensive enhanced feature.This enhanced feature vector not only contains the frequency-domain information of each signal but also includes the rich interaction information between signals.By adaptively selecting frequency-domain components strongly correlated with SoC,high-frequency measurement noise and irrelevant frequency-domain information can be suppressed,preventing invalid information from interfering with SoC estimation.

$$
F _ { f r e q } = \sigma \left( W _ { f } ^ { ( 2 ) } \cdot \mathrm { R e L U } \left( W _ { f } ^ { ( 1 ) } \cdot F _ { c o m b i n e d } + b _ { f } ^ { ( 1 ) } \right) + b _ { f } ^ { ( 2 ) } \right)
$$

where $W _ { f } ^ { ( i ) }$ is the adaptive weight. $b _ { f } ^ { ( i ) }$ is the bias term. $\sigma$ is the Sigmoid function, which constrains the weight range to [0,1]. $F _ { f r e q }$ is the final obtained frequency-domain feature.

# 3.1.2. Time-domain feature extraction

In this paper,endogenous variables refer to the latent states to be estimated and their historical information,i.e.,the historical sequence of SoC;exogenous variables refer to the observation and excitation sequences that can be acquired in real time during estimation and are fed into the model as known covariates,including current I, flow rate Q,terminal voltage U,open-circuit voltage OCV,and temperature T.The embedding schemes for the endogenous and exogenous variables are illustrated in Fig.2: the endogenous variables use patchlevel embeddings,whereas the exogenous variables use variable-level embeddings.

As a core state variable of the system,the SoC trajectory evolves through a sequence of physical phases,such as charging,discharging, and idle periods.To precisely capture the dynamic characteristics within each stage,the SoC sequence is segmented.The core objective of endogenous embedding is to accurately capture the time-dependent dynamic characteristics of the SoC in the VRFB.During actual operation, the SoC exhibits both rapid short-term fluctuations during charging and discharging and a slow decay trend under long-term cycling, requiring the use of different tokens for multi-scale information capture.

![](images/414a31c10c1de09ac50d0b273bec5eec284d50002e624177cdbcb12c0d66be0c.jpg)
Fig.1.Overall framework diagram.

![](images/0dc66ebfc373a7abeb76848ff7992fe6d3dea855b4fb37298702944cbecf0390.jpg)
Fig.2.Time-domain and frequency-domain feature extractor architecture.

Given that endogenous and exogenous variables play different roles in prediction tasks,they are embedded at different granularities [22].To capture the time-series variation features of endogenous variables， the model adopts a block-based representation strategy. Specifically,the endogenous sequence is divided into several nonoverlapping blocks,and each block is projected into a time series token.The SoC endogenous sequence undergoes patch segmentation, where the SoC sequence is divided into $M$ non-overlapping patches, each corresponding to the SoC variation trend during a local period of the VRFB.These patches represent three stages: charging increase, discharging decrease,and idle steady periods,with patch tokens formed through the patch embedding layer. This process can be represented as follows:

$$
\{ s _ { 1 } , s _ { 2 } , \ldots s _ { i } \ldots s _ { M } \} = \mathrm { P a t c h i f y } ( \mathrm { S o C } )
$$

$$
\begin{array} { l } { M = T / P } \\ { \ } \\ { P _ { \mathrm { e n } } = \mathrm { P a t c h E m b e d } ( s _ { 1 } , s _ { 2 } , \dots s _ { i } \dots , s _ { M } ) } \end{array}
$$

where $s _ { i }$ represents the ith non-overlapping patch after segmentation.
$P _ { \mathrm { e n } }$ represents the patch token. $P$ represents the patch length. $M$
represents the number of patches. $T$ represents the sequence length.

Since the global state of SoC imposes certain constraints on the local dynamics,when the SoC is close to Oor 1,the charging and discharging rates need to be reduced to avoid overcharging or overdischarging. In this case,the rate of change of the patches will be limited by the global state.Therefore,a global token is introduced,which encodes the macro characteristics of SoC through linear projection and adaptive learning of the full-duration SoC sequence.At the same time, the global token is used as a bridge for subsequent interactions with exogenous variables,avoiding estimation bias caused by local patches ignoring global constraints.The representation of the global token is as follows:

$$
G _ { \mathrm { e n } } = \mathrm { L e a r n a b l e } ( \mathrm { S o C } )
$$

where $G _ { \mathrm { e n } }$ represents the global token.Learnable(-) is used to extract the overall features of the SoC sequence.

To ensure a well-justified selection of input features,we determined the model exogenous variables as current I, terminal voltage $U$ ,open-circuit voltage $O C V$ ,temperature $T$ ,and electrolyte flow rate $Q$ from three perspectives:mechanistic relevance,statistical evidence, and engineering measurability.Mechanistically,I directly drives SoC evolution via Faraday's law;under thermodynamic equilibrium,OCV hasa well-defined mapping to SoC and thus provides a static indicator of SoC; under dynamic conditions, $U$ jointly reflects ohmic drop and polarization effects,complementing the information that OCV may miss under non-equilibrium operation; $T$ affects the Nernst term and reaction kinetics,thereby altering both OCV and polarization magnitudes; and $Q$ influences electrolyte circulation and mass transport,which in turn modulate the dynamic voltage response and the effective reaction rate.Statistically,we further computed a Pearson-correlation matrix and visualized the correlation strengths between each input variable and SoC using a heat map,while also examining inter-feature correlations to identify potential redundancy,thereby providing testable quantitative evidence for feature selection.From an engineering standpoint,all these variables are standard monitoring signals that can be acquired online via conventional sensors in VRFB systems,meeting the real-time availability requirements in BMS applications.

Unlike SoC,which is an endogenous variable,current $( I )$ ,terminal voltage $( U )$ ，open circuit voltage (OCV),temperature $( T )$ ，and flow rate $( Q )$ are exogenous operating conditions that directly affect SoC changes.For example,current is the direct determinant of the SoC change rate. Temperature indirectly affects efficiency by influencing reaction kinetics and electrolyte viscosity.And flow rate determines mass transfer efficiency.To enable the model to utilize these different exogenous variables,each exogenous variable is embedded as an independent variate token.The embedding process of the aforementioned exogenous variables can be represented as follows [36]:

$$
V _ { \mathrm { e x } , k } = \mathrm { V a r i a t e E m b e d } ( x _ { k } )
$$

where $x _ { k }$ represents the time series of the kth exogenous variable,and $x _ { k } ~ \in ~ \{ I , U , \mathrm { O C V } , T , Q \}$ . Through a trainable linear projection layer,

VariateEmbed, the entire time-series sequence is compressed into a variate token $V _ { \mathrm { e x } }$

Finally,the resulting time-domain and frequency-domain features are concatenated as the input to the subsequent modules,and a linear projection is applied to keep the representation in a D-dimensional space.This process can be expressed as:

$$
\begin{array} { r } { Z = \operatorname { C o n c a t } ( G _ { \mathrm { e n } } , F _ { \mathrm { f r e q } } ) } \\ { ~ } \\ { G _ { \mathrm { t m p } } = W _ { f } ^ { \mathrm { f u s e } } Z + b _ { f } ^ { \mathrm { f u s e } } } \end{array}
$$

where, $W _ { f } ^ { \mathrm { f u s e } }$ and $b _ { f } ^ { \mathrm { f u s e } }$ denote the weight matrices and bias vectors of the two fully connected layers,respectively.Applying LayerNorm to $G _ { \mathrm { t m p } }$ yields the time-frequency fused feature $G _ { \mathrm { f u s e } }$ . The pseudocode for the complete time-frequency feature extraction and fusion process is provided in Table 1.

# 3.2.Physical feature enhancement module

# 3.2.1. Physical memory unit

The underlying physical principle of SoC is the charge conservation principle,which is most directly described mathematically as the time integration of current,known as the coulomb counting method.To simulate this core physical process in the model,a gated recurrent unit (GRU) is used as the physical memory unit.Its internal update and reset gates allow it to function as a learnable integrator,which not only accumulates current information but also learns and compensates for integration biases caused by side reactions,measurement noise, and other factors through a data-driven approach.Thus enabling the memory of the historical evolution of SoC.

The physical memory unit selects the physical quantity directly related to SoC,which is the current.Physical normalization is performed usin $g$ Faraday's law to directly relate it to the physical meaning of SoC variations:

$$
I _ { \mathrm { n o r m } , t } = \frac { I _ { t } } { n \cdot F \cdot C _ { \mathrm { n o m } } }
$$

where the current is normalized using Faraday's law,reflecting the contribution of charge transfer to SoC. $I _ { t }$ is the current at time t.n represents the number of electrons transferred, where $n = 1$ $F = 9 6 4 8 5$ $\mathsf { C } / \mathrm { m o l }$ is the Faraday constant.

Then,through the gating mechanism of the GRU,the sequential accumulation of physical information is achieved under the guidance of the global trend.The fused feature of the global token $G _ { \mathrm { e n } }$ and frequency-domain feature $F _ { f r e q }$ is used as the initial $h _ { 0 }$ state for the input physical memory.At each time step,the current normalized current is concatenated with the physical memory from the previous time step and input into the GRU to dynamically update the memory state:

$$
\begin{array} { r l } & { h _ { t } = \mathrm { G R U } ( \left[ h _ { t - 1 } , I _ { n o r m , t } \right] , h _ { t - 1 } ) } \\ & { } \\ & { { r _ { t } } = \sigma ( W _ { r } \cdot \operatorname* { i n p } _ { t } + U _ { r } \cdot h _ { t - 1 } + b _ { r } ) } \\ & { } \\ & { z _ { t } = \sigma ( W _ { z } \cdot \operatorname* { i n p } _ { t } + U _ { z } \cdot h _ { t - 1 } + b _ { z } ) } \\ & { } \\ & { \tilde { h } _ { t } = \operatorname { t a n h } ( W _ { h } \cdot \operatorname* { i n p } _ { t } + U _ { h } \cdot ( r _ { t } \odot h _ { t - 1 } ) + b _ { h } ) } \\ & { } \\ & { h _ { t } = ( 1 - z _ { t } ) \odot h _ { t - 1 } + z _ { t } \odot \tilde { h } _ { t } } \end{array}
$$

where $W _ { i }$ and $U _ { i }$ are the weight matrices. $b$ is the bias term.is the hyperbolic tangent activation function. $\mathrm { i n p } _ { t }$ is the input to the GRU at time step $t$ ,formed by concatenating the normalized current and the hidden state from the previous time step.The GRU uses the reset gate $r _ { t }$ ， update gate $z _ { t } ,$ and hidden state $h _ { t }$ to allow the model to remember the macro trends of VRFB long-term operation.It also responding in realtime to the dynamic changes in current physical quantities, providing a hidden state with physical meaning for subsequent steps.After iterative updates at all time steps,the final physical memory state is returned, which encodes the cumulative effect of the entire current sequence on SoC changes,and $h _ { t }$ serves as the final enhanced feature.

Table 1 Pseudocode for time-frequency feature extraction and fusion.

<table><tr><td>Algorithm</td><td>Steps</td></tr><tr><td>Inputs and outputs</td><td>1 Input multivariate time-series signals: X∈ R B×Txn. 2 Output patch-level time-domain tokens: Pen ∈RBxM×D. 3 Output fused global token: Gfuse ∈RB×D. 4 Output exogenous-condition tokens: Vex ∈ R B×CxD.</td></tr><tr><td>Frequency-domain feature extraction</td><td>1 Channel splitting: extract the ith variable as xi = X(:,:,i) ∈ RB×T. 2 DCT transform: for each frequency index j =0,.,L-1,compute L-1 m=0 3 Cros-spectrum construction: for any pair (p &lt;q),construct CSMpq(j)=Freqp(j) Freqq(j). 4Frequency-omain enhanced concatenation:concatenateallsngle-channelspectraandcrosspectraalong the featuredimension. Fcombined=Concat(Freq,..,Freq,CM12,.). 5 Adaptive weighting: generate element-wise weights via a neural network. Fatt=σ(WReLU(WFcombined)). 6 Frequency-domain embedding: linearly project to a unified dimensionality.</td></tr><tr><td>Time-domain feature extraction</td><td>Freq =W(FcobnedFat）+∈RB×D 1 SoC patching: partition the historical SoC sequence into M patches of length P, where m =1.,M and M=T/P. 2 Patch tokens: apply a linear mapping to each patch and stack them to obtain Pm=Wp(sm+em)+bp，Pen=[P1,..,PM]. 3 Global token: obtain Gen via linear projection. Gen =Wgg+b&amp;∈RBXD. 4 Exogenous embedding: represent each exogenous variable at the variable level. Uex,i =Wexzi + bex 5 Set of exogenous tokens:Vex= {Uex,1..,Uex.c}.</td></tr><tr><td>Time-frequency feature fusion</td><td>1 Feature concatenation: concatenate the global time-domain token with the frequency-domain embedding. 2 Linear projection: project back to D dimensions. Gtmp =WfuseZ +bfuse ∈RBXD. 3 Normalization: apply LayerNorm to Gtmp Gfuse =LN(Gtmp)，LN(u) = u-μ V²+ε 4 Output for subsequent modules:Pen,Gfuse,Vex,Ffreq&#x27;</td></tr></table>

# 3.2.2. Physical memory unit

A one-dimensional temporal convolutional layer is designed for patch tokens and global tokens to capture local dependencies between adjacent patches.At the same time,the convolutional layer integrates the global SoC features into the local patches.The above process can be represented as follows:

$$
\begin{array} { r l } & { P _ { \mathrm { c o n v } } = \mathrm { G E L U } ( \mathrm { B a t c h N o r m } ( \mathrm { C o n v 1 D } ( h _ { t } , W , k , s ) ) ) } \\ & { } \\ & { \hat { P } _ { \mathrm { e n } } = P _ { \mathrm { e n } } + P _ { \mathrm { c o n v } } } \\ & { } \\ & { \hat { G } _ { \mathrm { e n } } = \mathrm { C o n v 1 D } \left( \mathrm { G l o b a l A v g P o o l } ( \hat { P } _ { \mathrm { e n } } ) , W _ { g } \right) } \end{array}
$$

where $k$ represents the size of the convolutional kernel.s refers to the stride. $W$ and $W _ { g }$ is the weight matrix. ConvlD represents the convolution operation applied to the features, simultaneously extracting the local dependencies between patches and the influence of global constraints on the local patches.The final result is the updated global token $\hat { G } _ { \mathrm { e n } }$ and patch token $\hat { P } _ { \mathrm { e n } }$

# 3.2.3.Endogenous-exogenous cross-attention module

The design goal of cross-attention is to establish an accurate relationship between exogenous and endogenous variables,which must align with the characteristic that exogenous variables affect SoC through different mechanisms in VRFB.In this module, $\hat { G } _ { \mathrm { e n } }$ is used as the query, $V _ { \mathrm { e x } }$ as the key(K),and the value(V). This avoids the information interference caused by traditional feature concatenation.

The core logic lies in the global token encoding the global state of SoC,which can adaptively select key information from the exogenous variables based on the current state.The expression is as follows:

$$
\hat { G } _ { \mathrm { \tiny ~ e n } } ^ { \prime } = \mathrm { L a y e r N o r m } ( \hat { G } _ { \mathrm { e n } } + \mathrm { C r o s s - A t t e n t i o n } ( \hat { G } _ { \mathrm { e n } } , V _ { \mathrm { e x } } ) )
$$

$$
\mathrm { A t t e n t i o n } ( Q , K , V ) = \mathrm { S o f t m a x } \left( \frac { Q K ^ { T } } { \sqrt { D } } \right) V
$$

where $\sqrt { D }$ is the scaling factor,which helps alleviate gradient explosion.Ultimatelytheudated globaltoke $\hat { G } _ { \mathrm { ~ \tiny ~ e ~ n ~ } } ^ { \prime }$ and patch token $\hat { P } _ { \mathrm { e n } }$ serve as the output of the physical feature enhancement module.

# 3.3.Physical constraint output module

This module aims to synergistically integrate the data-driven results with physical constraints,producing prediction results that better align with physical laws.The module adopts a dual-branch parallel architecture,as shown in Fig.3.The data-driven branch is responsible for capturing complex nonlinear mapping relationships,while the physical constraint branch ensures that the estimation results follow the physical laws described by the Nernst equation. The outputs of the two branches are integrated through a learnable adaptive fusion mechanism,ultimately generating SoC estimation results with physical consistency.

# 3.3.1.Physical constraint output module

The feature processing network is responsible for integrating the features output by the upstream modules.Its core is to provide input features for SoC estimation by multi-scale feature fusion and physical information encoding,which can accurately characterize the electrochemical process of the battery.

$$
\begin{array} { r l r } {  { P _ { \mathrm { a v g } } = \frac { 1 } { M } \sum \hat { P } _ { \mathrm { e n } } } } & { ( 3 7 ) } \\ & { } & { \hat { P } _ { \mathrm { e n } } ^ { \prime } = W _ { p } ^ { ( 3 ) } ( \mathrm { \ D r o p o u t ~ } \big ( \mathrm { \ R e L U ~ } \big ( W _ { p } ^ { ( 2 ) } ~ \big ( \mathrm { \ D r o p o u t } \big ( \mathrm { R e L U } \big ( W _ { p } ^ { ( 1 ) } P _ { \mathrm { a v g } } + b _ { p } ^ { ( 1 ) } \big ) \big )   } \\ & { } & {   + b _ { p } ^ { ( 2 ) } ~ \big ) \big ) ) ) + b _ { p } ^ { ( 3 ) } } \end{array}
$$

where $M$ is the number of patches. $\boldsymbol { W } _ { p } ^ { ( i ) }$ is the weight matrix $b _ { p } ^ { ( i ) }$ is the bias vector. $i = { 1 , 2 , 3 }$ 、Finally,the processed patch token features and

![](images/68287f420a3bcf75703dc4adc766a1a92dc6d795ccebe36f30f8f02044059651.jpg)
Fig.3.Physical constraint output module.

the global token are fused by element-wise addition to obtain a unified feature representation.This fused feature serves as the common input for the subsequent dual-branch network.

$$
F _ { t o t a l } = \hat { P } _ { \mathrm { ~ e n } } ^ { \prime } + \hat { G } _ { \mathrm { ~ e n } } ^ { \prime }
$$

# 3.3.2.Dual-branch parallel estimation architecture

The data-driven branch directly learns the complex nonlinear mapping of SoC from the high-dimensional feature representation,without relying on any explicit physical model assumptions.This branch uses a fully connected network structure:

$$
\begin{array} { l } { { S o C _ { d a t a } = \sigma \left( W _ { S o C } ^ { ( 3 ) } \cdot \mathrm { R e } L U \left( W _ { S o C } ^ { ( 2 ) } \cdot \mathrm { R e } L U \left( W _ { S o C } ^ { ( 1 ) } \cdot F _ { t o t a l } + b _ { S o C } ^ { ( 1 ) } \right) \right. \right. } } \\ { { \qquad + \left. \left. b _ { S o C } ^ { ( 2 ) } \right) + b _ { S o C } ^ { ( 3 ) } \right) } } \end{array}
$$

where $W _ { S o C } ^ { ( i ) }$ is the weight matrix and $b _ { S o C } ^ { ( i ) }$ is the bias vector, $i = 1 , 2 , 3$ The design philosophy of this branch is to fully utilize the powerful representation ability of neural networks,to capture the complex nonlinear dependencies that may exist between SoC and factors such as current, voltage,temperature,and flow rate. These relationships may be difficult to fully capture using traditional physical models.

The Physical Constraint Branch is based on the principles of electrochemical thermodynamics,and the theoretical relationship between the OCV and the SoC is established via the Nernst equation.Firstly, the $E _ { p r e d } ^ { O C V }$ is estimated from the fused feature $F _ { \mathrm { t o t a l } }$ through a fully connected network.

$$
E _ { p r e d } ^ { O C V } = W _ { o c v } ^ { ( 3 ) } \cdot \mathrm { { R e L U } } \left( W _ { o c v } ^ { ( 2 ) } \cdot \mathrm { { R e L U } } \left( W _ { o c v } ^ { ( 1 ) } \cdot F _ { \mathrm { { t o t a l } } } + b _ { o c v } ^ { ( 1 ) } \right) + b _ { o c v } ^ { ( 2 ) } \right) + b _ { o c v } ^ { ( 3 ) }
$$

Next, the estimated $E _ { p r e d } ^ { O C V }$ and temperature $T$ are substituted into the inverse operation of the Nernst equation to calculate $S o C _ { p h y }$ under physical constraints.The Nernst equation can be expressed as:

$$
E _ { p r e d } ^ { O C V } = E ^ { 0 ^ { \prime } } + \frac { 2 R T } { F } \ln \left( \frac { S o C _ { p h y } } { 1 - S o C _ { p h y } } \right)
$$

where $E ^ { 0 ^ { \prime } }$ is the formal potential,and $a$ is the number of electrons
transferred. $R \ = \ 8 . 3 1 4 \mathrm { J / ( m o l } \mathrm { K } )$ is the gas constant. $T$ is the abso
lute temperature of the stack. $\mathsf { S o C } _ { p h y }$ is the estimate under physical $E _ { p r e d } ^ { O C V }$ $E _ { p r e d } ^ { O C V }$
under the physical constraint,ensuring that the results comply with
electrochemical thermodynamics.

Table 2 Model hyperparameters.

<table><tr><td>Category</td><td>Parameter</td><td>Value</td></tr><tr><td>Data splitting and windowing</td><td>input_window stride</td><td>12 1</td></tr><tr><td>Time-domain module</td><td>patch_len embed_dim</td><td>12 64</td></tr><tr><td>Attention mechanism</td><td>num_heads num_layers</td><td>4 2</td></tr><tr><td>Frequency-domain module</td><td>keep_freq_coeffs embed_dim</td><td>8 64</td></tr><tr><td>Output module</td><td>hidden_dims dropout</td><td>[256,128,64] 0.1</td></tr><tr><td>Adaptive fusion mechanism</td><td></td><td>Initialization 0.3; α = Sigmoid(𝛼raw)</td></tr><tr><td>Optimizer</td><td>lr</td><td>5×10-4</td></tr><tr><td>Training setup</td><td>batch_size epochs</td><td>32 10</td></tr></table>

# 3.3.3.Adaptive fusion mechanism

To effectively integrate the advantages of the data-driven branch and the physical constraint branch,this paper designs a learnable adaptive fusion mechanism.This mechanism dynamically adjusts the contribution of the outputs from the two branches through a learnable parameter:

$$
S o C _ { c o r r e c t e d } = \alpha \cdot S o C _ { p h y } + ( 1 - \alpha ) \cdot S o C _ { d a t a }
$$

where $\alpha$ is the fusion weight,and $\alpha \in [ 0 , 1 ]$ .During training,it is automatically optimized through backpropagation,allowing the model to automatically adjust the trust level between the data-driven estimate and the physical constraint estimate.When the data-driven branch's estimate deviates from the physical laws,the model can decrease the value of $\alpha$ ,relying more on the physical constraint branch's estimate, ensuring the physical consistency of the output results.Under different operating conditions,such as varying currents and electrolyte flow rates,the model can automatically adjust the fusion weight to achieve optimal performance.

# 3.3.4. Loss function

The model training uses Mean Squared Error (MSE)as the loss function,aiming to minimize the difference between the final fused SoC

![](images/f757e42f7125d1ae217746fef56b4dc567d4c14b7144925a7c5ec5cf87a82675.jpg)
Fig.4VRFBtaladea:xpeall;atfe

:stimate and the true SoC value.The loss function is defined as follows

$$
\mathcal { L } _ { D a t a } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \left\| S o C _ { r e a l } ^ { ( i ) } - S o C _ { c o r r e c t e d } ^ { ( i ) } \right\| ^ { 2 }
$$

where $N$ is the batch size. $S o C _ { r e a l } ^ { ( i ) }$ is the true SoC value of the $i$ -th sample.By optimizing with this loss function, the final SoC estimate is obtained.

To improve the reproducibility of the proposed method,we provide a table of model hyperparameters.In addition, we adopt a two-stage hyperparameter selection procedure.First,undera fixed data split and a fixed random seed,we performed a coarse scan over key parameters such as the learning rate,embedding dimension,dropout rate,and the initialization of the fusion coeficients,discarding combinations that failed to converge or exhibited obvious overfitting,thereby determining a candidate range that supports stable training.Next,we conducted a grid search within this candidate range and selected the optimal configuration primarily according to the validation-set RMSE.After fixing the optimal hyperparameters,we repeated the training to verify the stability of the results.The hyperparameters listed in Table 2 are ultimately used as the default setting in this work.

# 4.Experimental design and evaluation metrics

# 4.1.Experimental platform

The analysis and experiments in this study are conducted on a 2.5 kW/3 kWh VRFB system,as illustrated in Fig.4(a). The system comprises a stack,an electrolyte circulation and delivery unit, monitoring sensors,and a battery management system,which jointly enable electrolyte circulation,charge-discharge regulation,and operating-state monitoring.The detailed specifications of the experimental platform are summarized in Table 3.

# 4.2.Experimental design

All variables in the experiments were synchronously sampled at $\Delta t \ = \ 1$ s.The operating conditions were uniformly categorized according to the time variability of the current $I$ and the electrolyte flow rate $Q$ .When both $I$ and $Q$ remained constant over a time interval, i.e., two consecutive samples satisfied $| I ( k ) - I ( k - 1 ) | ~ \approx ~ 0$ and $| Q ( k ) - Q ( k - 1 ) | \approx 0$ ,the interval was defined as a static operating condition.When $I$ or $Q$ varied with time,the interval was defined as a dynamic operating condition.To ensure reproducibility,the degree of dynamicity was characterized by the discrete rate of change:

$$
{ \frac { d I } { d t } } \approx { \frac { I ( k ) - I ( k - 1 ) } { \Delta t } }
$$

Table 3 Specifications of the experimental VRFB system.

<table><tr><td>Parameter</td><td>Value</td><td>Unit</td></tr><tr><td>Electrolyte volume per side</td><td>150</td><td>L</td></tr><tr><td>Total vanadium concentration</td><td>1.5</td><td>mol/L</td></tr><tr><td>Electrode surface area</td><td>0.1</td><td>m²</td></tr><tr><td>Membrane thickness</td><td>5×10-5</td><td>m</td></tr><tr><td>Membrane area</td><td>625× 160</td><td>mm</td></tr><tr><td>Membrane model</td><td>Nafion 112</td><td>/</td></tr><tr><td>Charge cutoff voltage</td><td>30</td><td>V</td></tr><tr><td>Discharge cutoff voltage</td><td>19</td><td>V</td></tr><tr><td>Pump power</td><td>25</td><td>W</td></tr><tr><td>Number of cells in the stack</td><td>19</td><td>/</td></tr><tr><td>Rated power</td><td>2.5</td><td>kW</td></tr><tr><td>Rated energy capacity</td><td>126</td><td>Ah</td></tr></table>

$$
{ \frac { d Q } { d t } } \approx { \frac { Q ( k ) - Q ( k - 1 ) } { \Delta t } }
$$

The high-frequency dynamic operating condition described in this paper refers to second-level perturbations occurring during operation. Such perturbations were realized by short-duration current steps (Condition 3) and by injecting point-wise disturbances into the measured signals on a per-sample basis in the noise experiments (see Section 5.3 for the noise-experiment settings).

To verify the effectiveness of the proposed method, several experiments under different operating conditions were conducted on the developed platform. The design of each experiment group is as follows:

(1) Operating condition 1: constant current-constant voltage (CC-CV) experiment.

The CC-CV mode is the most commonly used standard charging strategy for batteries. It combines two stages: constant current charging and constant voltage charging,enabling fast charging while preventing overcharging,ensuring charging safety,and extending the battery's cycle life.In CC mode,the VRFB is charged with a constant current of $8 0 ~ \mathrm { A }$ ,and the voltage gradually increases.When the voltage reaches the cutoff voltage of $3 0 ~ \mathrm { V }$ ,it switches to CV mode,where the voltage remains constant and the current gradually decreases.When the current drops to $3 0 \mathrm { A }$ ,the battery switches to discharge mode.Discharge occurs in CC mode with a current of $- 8 0 \ \mathsf { A } ,$ and when the voltage reaches $1 9 \mathrm { V }$ ,it switches back to CV mode,where the voltage remains constant and the current starts to rise again.When the current reaches $- 3 0 \mathrm { ~ A ~ }$ ， the battery switches back to the charging state,completing one charge and discharge cycle.

(2) Operating condition 2: variable flow rate experiment.

The core objective of this experiment is to simulate the field operation scenario of VRFB.To optimize system performance,the pump speed needs to be adjusted to balance mass transfer efficiency with energy consumption. This adjustment process directly affects the electrolyte flow rate.When the energy storage system needs to increase its output power,the pump speed increases.The flow rate increases, accelerating the transport of vanadium ions to the electrode surface. This alleviates the concentration polarization phenomenon.When the power demand decreases,the flow rate decreases accordingly.This reduces the energy consumption of the circulation pump.The experiment uses a stepped flow rate adjustment strategy of O.4,0.5,and $0 . 6 ~ \mathrm { m } ^ { 3 } / \mathrm { h }$ This strategy is used to simulate flow rate fluctuations caused by sudden power demand.

[3) Operating condition 3: variable current experiment.

This experiment simulates the sudden current fluctuations caused by load changes during the VRFB's field operation. When the energy storage system responds to grid commands,the charge and discharge current rapidly increases or decreases from the rated value.When the load is suddenly disconnected,the current rapidly drops from a high value to a low value.The experiment uses a high-frequency fluctuation scenario with sudden current changes,where the current varies in a stepped pattern of 60 A, 70 A,and $^ { 8 0 \mathrm { ~ A ~ } }$ ，Charge and discharge are carried out under this cycle,covering the common current disturbance range in field operations.

[4) Operating condition 4: constant current experiment.

The purpose of this experiment is to evaluate the SoC estimation accuracy of the battery under a stable load.The experiment simulates a steady charge and discharge process of the VRFB under constant current.The charge and discharge experiments are conducted at constant currents of 6O A,70 A,and 80 A during different cycles.

(5) Operating condition 5: random current experiment.

This experiment simulates the response of the VRFB under load frequency regulation conditions.The charge and discharge process is controlled by randomly varying current commands,with the SoC adjusted to approximately O.5 at the start of the experiment.This operating condition is primarily used to test the model's SoC estimation performance under rapid current fluctuations and to validate the model's ability to handle complex dynamic conditions.

# 4.3.Experimental evaluation metrics

Data collection is performed on the constructed VRFB platform,to verify the effectiveness and advantages of the proposed method over traditional methods.To quantify the model's performance,the following metrics are introduced. The RMSE,MAE, $\mathtt { R } ^ { 2 }$ ，and Maximum Absolute Error (MAX) are calculated as evaluation metrics. $\mathtt { R } ^ { 2 }$ measures the model's fitting accuracy to the real SoC,and for good model performance,the closer the $\mathbb { R } ^ { 2 }$ value is to 1, the better the performance. MAX is used to measure the worst-case estimation of the model.It reflects the lower bound of the stability and reliability of the estimation algorithm.The smaller the MAE and RMSE values,the better the model's performance.P95 is the 95th percentile of the absolute errors between the SoC ground truth and estimated values for all samples.It indicates that $9 5 \%$ of the absolute estimation errors do not exceed this value,and can be used to evaluate the upper bound of the estimation error distribution.Error Std, namely the standard deviation of the error, is the standard deviation of the SoC prediction errors relative to the mean of the prediction errors.A smaller value indicates lower volatility of the prediction errors and better stability of the estimation algorithm.

$$
\begin{array} { l } { \displaystyle \mathrm { R M S E } = \sqrt { \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \left( y _ { i } - \hat { y } _ { i } \right) ^ { 2 } } } \\ { \displaystyle \mathrm { M A E } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \left| y _ { i } - \hat { y } _ { i } \right| } \\ { \displaystyle \mathrm { R } ^ { 2 } = 1 - \frac { \sum _ { i = 1 } ^ { n } \left( y _ { i } - \hat { y } _ { i } \right) ^ { 2 } } { \sum _ { i = 1 } ^ { n } \left( y _ { i } - \bar { y } \right) ^ { 2 } } } \end{array}
$$

$$
\begin{array} { r l } & { \mathrm { M A X } = \operatorname* { m a x } \left( \left| y _ { i } - \hat { y } _ { i } \right| \right) } \\ & { \mathrm { P 9 5 } = \mathrm { P e r c e n t i l e } _ { 9 5 } \left( \{ | y _ { 1 } - \hat { y } _ { 1 } | , | y _ { 2 } - \hat { y } _ { 2 } | , \dotsc , | y _ { n } - \hat { y } _ { n } | \} \right) } \\ & { \mathrm { E r r o r ~ } \mathrm { S t d } = \displaystyle \sqrt { \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \left( ( y _ { i } - \hat { y } _ { i } ) - \bar { e } \right) ^ { 2 } } } \\ & { \bar { e } = \displaystyle \frac { 1 } { n } \sum _ { i = 1 } ^ { n } ( y _ { i } - \hat { y } _ { i } ) } \end{array}
$$

where $n$ is the total number of samples. $y _ { i }$ and $\hat { y } _ { i }$ represent the true value and estimated value of SoC,respectively. $\bar { y }$ denotes the mean value. $\bar { e }$ denotes the mean value of prediction errors over all samples.

To assess the reliability of SoC estimation under dynamic operating conditions from a mechanistic-consistency perspective,we introduce two physics-consistency metrics in addition to the conventional accuracy metrics.The two metrics are the directional consistency rate (DCR) and the Faraday consistency correlation (FCC).

(1) Directional consistency rate (DCR)

Under ideal conditions where side reactions and capacity drift are neglected, the direction of SoC variation should be consistent with the current direction: a positive charging current corresponds to an increase in SoC,whereas a negative discharging current corresponds to a decrease in SoC.Based on this physical constraint,we define DCR as the proportion of time steps at which the sign of the predicted SoC increment matches the sign of the current:

$$
\mathrm { D C R } = \frac { 1 } { \left| \varOmega \right| } \sum _ { t \in \varOmega } \mathbb { I } \left( \mathrm { s i g n } \left( \widehat { A S o C } _ { t } \right) = \mathrm { s i g n } \left( I _ { t } \right) \right)
$$

$$
\widehat { A S o C _ { t } } = \widehat { S o C _ { t } } - \widehat { S o C _ { t - 1 } }
$$

where Ⅱ(·) denotes the indicator function. To avoid sign instability in zero-current or low-current intervals,where directional judgments are physically less meaningful, the set $\Omega = \left\{ t : | I _ { t } | > \varepsilon \right\}$ only includes time instants at which the current magnitude exceeds a prescribed threshold $\varepsilon$ ，A DCR closer to 1 indicates that the model better captures the charge/discharge direction,i.e.,the monotonicity of SoC,in a manner consistent with the underlying physics during dynamic operation.

(2) Faraday consistency correlation (FCC)

According to Faraday's law,under a discrete time step,the SoC increment is linearly related to the integrated current,which can be approximated as

$$
\varDelta S o C _ { t } \propto \frac { I _ { t } \varDelta t } { n F C _ { \mathrm { n o m } } }
$$

where $n$ is the number of electrons transferred, $F$ is Faraday's constant, and $C _ { \mathrm { n o m } }$ is the nominal capacity.Accordingly, the SoC increment $\widehat { \Delta S o C } _ { t }$ can be obtained from the estimated SoC.We also compute the normalized current term as follows:

$$
\mathrm { F C C } = \mathrm { c o r r } \left( \varDelta \widehat { S o C } _ { t } , \ I _ { t } ^ { \mathrm { n o r m } } \right) , \quad t \in \varOmega
$$

$$
\mathrm { c o r r } x _ { t } , y _ { t } = { \frac { \sum _ { t \in { \mathcal { Q } } } \left( x _ { t } - { \bar { x } } \right) \left( y _ { t } - { \bar { y } } \right) } { { \sqrt { \sum _ { t \in { \mathcal { Q } } } \left( x _ { t } - { \bar { x } } \right) ^ { 2 } \sum _ { t \in { \mathcal { Q } } } \left( y _ { t } - { \bar { y } } \right) ^ { 2 } } } } }
$$

where $\mathrm { c o r r } x _ { t } , y _ { t }$ denotes the Pearson correlation coefficient. $\bar { x } \quad =$ $\begin{array} { r } { \frac { 1 } { | \varOmega | } \sum _ { t \in \varOmega } x _ { t } } \end{array}$ and $\begin{array} { r } { \bar { y } = \frac { 1 } { | \varOmega | } \sum _ { t \in \varOmega } y _ { t } } \end{array}$ . An FCC closer to1indicatestatthe model-predicted SoC variations are more consistent with the coulomb counting principle.Conversely,a lower FCC often implies physically unreasonable drift in the estimates under dynamic conditions or a weakened relationship with the current-driven dynamics.

In summary,DCR characterizes the physical interpretability of the direction of SoC variation,whereas FCC quantifies the correlation consistency between the magnitude of SoC variation and Faraday's law.These two metrics complement conventional accuracy indicators, enabling a more comprehensive evaluation of both performance and physical plausibility under dynamic operating conditions.

We define FCC as the Pearson correlation coeficient between the SoC increment and the normalized current term:

$$
I _ { t } ^ { \mathrm { n o r m } } = \frac { I _ { t } \Delta t } { n F C _ { \mathrm { n o m } } }
$$

# 4.4.Reference SoC calculation

To obtain a SoC reference ground truth for model training and evaluation,we adopt a hybrid strategy that combines recursive coulomb counting with OCV calibration at cycle boundaries.The core idea is to update SoC within each charge-discharge cycle using high-precision current sampling,and to calibrate the initial SoC at the cycle boundary using the rested open-circuit voltage,thereby suppressing integration drift and improving the consistency of the reference values.

The current $I$ is recorded via a high-precision acquisition chain, with a sensor accuracy of $1 0 ^ { - 4 }$ of full scale and a sampling period of one second.We adopt the sign convention that charging current is positive and discharging current is negative. Over an entire charge-discharge cycle, SoC can be computed as follows:

$$
S o C = S o C _ { 0 } + \frac { \int { I d t } } { C _ { n } }
$$

where $S o C _ { 0 }$ denotes the initial SoC at the beginning of the chargedischarge cycle.With sufficiently accurate current sampling,the dominant error source in the above equation becomes long-term integration drift.Therefore,we further introduce OCV calibration at the cycle boundaries.

At the end of each charge-discharge cycle,the current is set to zero and the system enters a rest period to allow suficient electrolyte mixing and gradual relaxation of polarization. Once the terminal voltage satisfies a predefined stability criterion,the open-circuit voltage is recorded. Then,based on the offline-calibrated monotonic OCV-SoC mapping, the calibrated $S o C _ { 0 }$ is obtained via interpolation look-up.

$$
S o C _ { 0 } = f ^ { - 1 } \left( E _ { \mathrm { o c v , c e l l } } \right)
$$

If alignment with the voltage scale of a 19-cell series stack is required, the stack-level equivalent open-circuit voltage can be converted by the number of series-connected cells, i.e., $E _ { 0 \mathrm { C V , s t a c k } } = 1 9 E _ { 0 \mathrm { C V , c e l l } }$ It should be noted that SoC is a state variable and is independent of the number of series cells. Therefore, the inversion of the reference $\mathrm { S o C } _ { 0 }$ in this study is performed using the reference single-cell open-circuit voltage and the single-cell OCV-SoC mapping.

Through the above procedure,we obtain the reference ground-truth SoC values,which serve as the benchmark for model training and performance evaluation.

# 4.5.Input feature relevance analysis

To improve the testability of feature selection and the reproducibility of the proposed method,we validate the statistical associations between the input variables and SoC.Specifically,we select the current $I$ ,terminal voltage $U$ ,open-circuit voltage $O C V$ ,temperature $T$ ，and electrolyte flow rate $Q$ ,all of which are available online from the experimental platform,and compute their Pearson correlation coefficients with SoC.The resulting correlation matrix is visualized as a heat map to quantify the association strength between each variable and SoC and to examine potential redundancy among inputs.As shown in Fig. 4(b),OCV exhibits a strong correlation with SoC,which is consistent with the mapping characterized by the Nernst relationship under thermodynamic equilibrium.Temperature also shows a certain correlation with SoC,reflecting the influence of temperature on electrode reaction kinetics and electrolyte properties.Meanwhile,a relatively strong correlation is observed between $I$ and $U$ ,indicating that they share part of the external operating-condition information.However, their physical meanings are not equivalent. Specifically, $I$ represents the external energy-exchange driving signal, whereas $U$ further integrates dynamic effects such as ohmic polarization and mass-transport polarization. Therefore, jointly using $I$ and $U$ is beneficial for improving identifiability under dynamic operating conditions.

It should be noted that,mechanistically, SoC is an integral state of the current,and the primary effect of current on SoC is more directly reflected in the SoC change rate rather than in the instantaneous SoC value.Consequently, the zero-lag correlation coefficient mayunderestimate the importance of dynamic variables such as current.To further verify feature effectiveness,we additionally construct the SoC changerate feature dSoC_dt and perform a correlation test.The results show that the correlation coefficient between Iand dSoC_dt is approximately 0.53,confirming the effective driving role of current in the dynamic evolution of SoC.

# 5.Experimental results and analysis

# 5.1.Comparative experiment of different models

To confirm the superior performance of the proposed model, comparative experiments were conducted with different models.These included the results of the traditional ampere-hour integration method,as well as various data-driven methods,such as CNN,TCN-BiLSTM [37], and BPNN[22].During the experiment, the dataset was split into 0.8 training and O.2 testing.The performance metrics of the SoC estimation results for all models are shown in Table 4.

Compared with the other models,the proposed method exhibits superior SoC estimation performance under all operating conditions, as shown in Fig.5.Experiments were conducted under four different operating conditions to validate the SoC estimation capability for VRFB. The results indicate that the proposed model achieves the best overall performance,with an average RMSE of only $0 . 3 4 \%$ ,MAEof $0 . 2 4 \%$ ,Max of $1 . 5 0 \%$ ,and $\mathbb { R } ^ { 2 }$ of $9 9 . 9 6 \%$ ,outperforming the other methods across all four metrics.This demonstrates consistently high accuracy and good generalization across different operating modes.

Among the compared methods,coulomb counting yields the largest errors.The error curves clearly show that its estimation error accumulates continuously over time,making it difficult to adapt to dynamic operating conditions.In contrast, the proposed method effectively prevents drift caused by time-accumulated errors and is particularly advantageous under dynamic conditions,achieving maximum reductions of $9 6 . 6 7 \%$ in RMSE and $9 3 . 9 9 \%$ in MAE relative to coulomb counting.

Compared with the data-driven baselines,the proposed method maintains lower error levels under strongly disturbed conditions such as dynamic current profiles.Taking the dynamic-current condition as an example,the proposed method achieves an RMSE of only $0 . 3 5 \%$ ， substantially lower than that of TCN-BiLSTM,corresponding to an errorreduction of approximately $7 6 . 6 7 \%$ .Meanwhile,MAE decreases from $1 . 2 2 \%$ to $0 . 2 7 \%$ ,and the maximum error decreases from $3 . 1 3 \%$ to $1 . 2 8 \%$ ，indicating a stronger capability to suppress transient deviations induced by rapid current variations.Moreover,under the dynamic-flow-rate condition, some models exhibit pronounced performance fluctuations,e.g.,the RMSE of CNN is $3 . 4 3 \%$ ，whereas the proposed method remains at $0 . 4 3 \%$ .In addition,the maximum error is reduced by $8 0 . 1 6 \%$ from $8 . 6 2 \%$ to $1 . 7 1 \%$ ,demonstrating improved adaptability to non-stationary effects caused by flow-rate disturbances. Overall, the proposed method delivers clear accuracy advantages in the designed experimental scenarios and exhibits more pronounced cross-condition stability.

To evaluate the computational load and real-time feasibility of the proposed method,we supplemented computational-complexity reporting and conducted inference performance tests,with the results summarized in Table 5.The trained model has a file size of approximately1.38 MB.Inference benchmarking was performed on an NVIDIA GeForce RTX 4060 Laptop GPU. The mean per-sample inference latency is $4 . 2 7 3 ~ \mathrm { m s }$ on Testl with 8772 samples and $4 . 6 4 9 ~ \mathrm { m s }$ on Test2 with 15,726 samples.We also report the fastest and slowest inference times, the total inference time,and the standard deviation to characterize the stability of inference latency.The corresponding throughputs are 210.1 FPS and 197.0 FPS,respectively,indicating millisecond-level latency and high throughput that can support the real-time computational requirements of online SoC estimation.It should be noted that the present results are GPU-based benchmarks,and on-device deployment and measurements on embedded hardware will be investigated as future work.

Table 4 Results of comparative experiments on different models.

<table><tr><td>Models</td><td>Metrics (%)</td><td>CC-CV</td><td>Variable flow rate</td><td>Variable current</td><td>Constant current</td><td>Mean value</td></tr><tr><td rowspan="4">Ampere-hour integration</td><td>RMSE</td><td>10.21</td><td>7.38</td><td>12.21</td><td>11.04</td><td>10.21</td></tr><tr><td>MAE</td><td>8.47</td><td>6.09</td><td>10.05</td><td>9.34</td><td>8.49</td></tr><tr><td>Max</td><td>23.71</td><td>16.07</td><td>27.65</td><td>20.89</td><td>22.08</td></tr><tr><td>R²</td><td>85.58</td><td>69.69</td><td>54.37</td><td>73.09</td><td>70.68</td></tr><tr><td rowspan="4">CNN</td><td>RMSE</td><td>0.70</td><td>3.43</td><td>2.01</td><td>2.51</td><td>2.16</td></tr><tr><td>MAE</td><td>0.57</td><td>2.56</td><td>1.83</td><td>1.97</td><td>1.73</td></tr><tr><td>Max</td><td>2.56</td><td>8.62</td><td>6.25</td><td>6.73</td><td>6.04</td></tr><tr><td>R²</td><td>99.90</td><td>97.54</td><td>99.29</td><td>98.67</td><td>98.85</td></tr><tr><td rowspan="4">TCN-BiLSTM</td><td>RMSE</td><td>2.00</td><td>1.38</td><td>1.50</td><td>1.13</td><td>1.50</td></tr><tr><td>MAE</td><td>1.37</td><td>1.16</td><td>1.22</td><td>1.01</td><td>1.19</td></tr><tr><td>Max</td><td>5.14</td><td>3.02</td><td>3.13</td><td>2.36</td><td>3.41</td></tr><tr><td>R²</td><td>99.16</td><td>99.57</td><td>99.60</td><td>99.73</td><td>99.52</td></tr><tr><td rowspan="4">Proposed</td><td>RMSE</td><td>0.36</td><td>0.43</td><td>0.35</td><td>0.21</td><td>0.34</td></tr><tr><td>MAE</td><td>0.19</td><td>0.35</td><td>0.27</td><td>0.15</td><td>0.24</td></tr><tr><td>Max</td><td>1.86</td><td>1.71</td><td>1.28</td><td>1.14</td><td>1.50</td></tr><tr><td>R²</td><td>99.98</td><td>99.96</td><td>99.94</td><td>99.96</td><td>99.96</td></tr></table>

![](images/4c7d9aed121df10b9c5ae8a6d0c0bba0f6856d03ccf3a248cafed62d241902f3.jpg)
Fig.5.Comparative experiment results diagram.

Table 5 Inference performance on different test sets.

<table><tr><td>Test set size</td><td>Testl (8772)</td><td>Test2 (15726)</td></tr><tr><td>Avg.inference time</td><td>4.273 ms</td><td>4.649 ms</td></tr><tr><td>Fastest inference time</td><td>3.169 ms</td><td>3.146 ms</td></tr><tr><td>Slowest inference time</td><td>14.178 ms</td><td>28.523 ms</td></tr><tr><td>Time Std. Dev.</td><td>1.029 ms</td><td>1.444 ms</td></tr><tr><td>Throughput</td><td>210.1 FPS</td><td>197.0 FPS</td></tr></table>

Table 6 Evaluation metrics of ablation experiments.

<table><tr><td>Models</td><td>Metrics (%)</td><td>CC-CV</td><td>Variable flow rate</td><td>Variable current</td><td>Constant current</td><td>Mean value</td></tr><tr><td rowspan="4">Trail 1</td><td>RMSE</td><td>1.78</td><td>1.80</td><td>1.98</td><td>1.47</td><td>1.76</td></tr><tr><td>MAE</td><td>0.72</td><td>0.75</td><td>1.04</td><td>1.04</td><td>0.89</td></tr><tr><td>Max</td><td>3.02</td><td>5.74</td><td>4.68</td><td>3.79</td><td>4.31</td></tr><tr><td>R²</td><td>99.56</td><td>98.19</td><td>98.74</td><td>99.48</td><td>98.99</td></tr><tr><td rowspan="4">Trail 2</td><td>RMSE</td><td>1.89</td><td>1.76</td><td>1.91</td><td>1.26</td><td>1.71</td></tr><tr><td>MAE</td><td>0.83</td><td>0.80</td><td>0.93</td><td>0.56</td><td>0.78</td></tr><tr><td>Max</td><td>4.46</td><td>5.99</td><td>3.93</td><td>3.61</td><td>4.50</td></tr><tr><td>R²</td><td>99.48</td><td>98.26</td><td>98.83</td><td>99.62</td><td>99.05</td></tr><tr><td rowspan="4">Trail 3</td><td>RMSE</td><td>2.65</td><td>2.28</td><td>2.27</td><td>2.08</td><td>2.32</td></tr><tr><td>MAE</td><td>2.12</td><td>1.28</td><td>1.64</td><td>1.69</td><td>1.68</td></tr><tr><td>Max</td><td>7.19</td><td>6.93</td><td>6.75</td><td>5.42</td><td>6.57</td></tr><tr><td>R²</td><td>99.01</td><td>97.09</td><td>98.43</td><td>99.01</td><td>98.39</td></tr><tr><td rowspan="4">Trail 4</td><td>RMSE</td><td>0.36</td><td>0.43</td><td>0.35</td><td>0.21</td><td>0.34</td></tr><tr><td>MAE</td><td>0.19</td><td>0.35</td><td>0.27</td><td>0.15</td><td>0.24</td></tr><tr><td>Max</td><td>1.86</td><td>1.71</td><td>1.28</td><td>1.14</td><td>1.50</td></tr><tr><td>R²</td><td>99.98</td><td>99.96</td><td>99.94</td><td>99.96</td><td>99.96</td></tr></table>

# 5.2. Ablation experiment

In the ablation study of this section, the impact of different model components on performance is investigated.Four different experimental setups were used in the study: Trail1,Trail 2,Trail 3,and Trail 4.In each experimental setup,the involved model components include the frequency-domain feature extraction module,physical feature enhancement module,and physical constraint output module.Specifically, Trail 1 does not include the time-frequency feature extraction module. Trail 2 includes the frequency-domain feature extraction and physical constraint output modules,but lacks physical feature enhancement. Trail 3 only includes time-frequency feature extraction and physical feature enhancement. Trail 4 includes all three components.Through these different combinations,the contribution of each component to model performance is analyzed under four different operating conditions.

The evaluation metrics of the ablation study results are shown in Table 6.The complete model of the proposed method can estimate SoC more accurately and stably compared to the other ablation models, further validating the effectiveness of the proposed model components and their accuracy in SoC estimation.

The ablation study compares the model performance with different component combinations,validating the effectiveness of each core component in the proposed framework.Trail 4,which includes the full set of components- frequency-domain feature extraction,physical feature enhancement,and physical constraint output-performs the best. Trail 1,which lacks frequency-domain feature,shows worse performance metrics,indicating that the fusion of time-frequency feature effectively captures key information under dynamic operating conditions.Trails 2 and 3,which lack physical information,show increased error metrics. This suggests that different physical features not only enhance the model's interpretability but also ensure the physical plausibility of the output.The experiment demonstrates that the synergy of the three components is key to achieving high-accuracy and high-stability SoC estimation in the model.

To verify the necessity and effectiveness of the proposed physical memory unit (PMU),we design three comparative variants: removing the PMU,replacing the PMU with a standard GRU,and using the proposed PMU.All three variants share the same input features and training strategy to ensure a fair comparison. In addition to conventional accuracy metrics,we further introduce two physics-consistency measures.The DCR characterizes the agreement between the predicted direction of SoC change and the current direction,while the FCC quantifies the correlation between the predicted SoC variation and the normalized current term.

The results in Table 7 indicate that the proposed PMU achieves better performance on both DCR and FCC,and still shows a clear advantage over the standard GRU.The standard GRU brings only marginal improvements,whereas the PMU yields a pronounced gain in FCC,suggesting that the performance improvement stems from injecting the normalized current into the memory-update process,thereby making the hidden-state evolution more consistent with Faraday-based integration.This demonstrates that the proposed PMU enhances the physical plausibility of the model via mechanism-guided memory updates,rather than merely increasing the representational capacity of a recurrent structure.

Table 7 Ablation study of the PMU.

<table><tr><td>Model</td><td>DCR</td><td>FCC</td><td>MAE (%)</td><td>RMSE (%)</td></tr><tr><td>Remove PMU</td><td>0.8397</td><td>0.6146</td><td>0.2698</td><td>0.3529</td></tr><tr><td>Ordinary GRU</td><td>0.8419</td><td>0.6218</td><td>0.2724</td><td>0.3480</td></tr><tr><td>PMU</td><td>0.8527</td><td>0.6729</td><td>0.2505</td><td>0.3493</td></tr></table>

# 5.3.Noise robustness experiment

The experimental data in this paper are sourced from laboratory equipment,and the laboratory environment is considered ideal. Therefore,two types of noise are added in this experiment to ensure the robustness of the proposed method in practical applications.The noise robustness test in battery SoC estimation is crucial.Noise is denoted as Noise A and Noise B,where Noise A is used to simulate random measurement errors and Noise $\mathbf { B }$ is used to simulate complex nonlinear noise in real-field conditions [38].

Noise A uses Gaussian noise to simulate random sensor measurement errors,representing realistic disturbances during the data acquisition stage.Noise A is directly injected into the raw signals (e.g.,sensormeasured voltage,current,and temperature).The distributional characteristics of Noise A are defined as follows:

$$
N _ { \mathrm { n o i s e A } } \sim \mathcal { N } ( 0 , 0 . 0 1 )
$$

Noise B is a complex composite noise designed to emulate the more complicated, highly nonlinear disturbances introduced by adjacent devices in practical environments, e.g., power supplies and pumps. The distributional characteristics of Noise B are defined as follows:

$$
\begin{array} { r l } & { u _ { 0 } , u _ { 1 } \sim \mathcal { V } ( 0 . 1 , 0 . 5 ) } \\ & { } \\ & { G \sim \mathcal { N } ( 0 . u _ { 1 } ) } \\ & { } \\ & { \phi \sim \mathcal { V } ( 0 . 2 \pi ) } \\ & { } \\ & { N _ { \mathrm { s i n } } = u _ { 0 } \left[ \mathrm { i n } ( 2 \pi f _ { 1 } t ) + 0 . 5 \mathrm { s i n } ( 2 \pi f _ { 2 } t + \phi ) \right] } \\ & { } \\ & { N _ { \mathrm { n o n l i n e a r } } = \mathrm { t a n h } ( u _ { 0 } \cdot G ) + 0 . 2 \cdot | G | \cdot \mathrm { s i g n } ( \mathrm { s i n } ( 2 \pi f _ { 3 } t ) ) } \\ & { } \\ & { N _ { \mathrm { c r e a p } } = \theta \cdot ( w _ { \cdot } \ G + w _ { \cdot } \ N _ { \cdot \mathrm { e x i n } } + w _ { \cdot } \ N _ { \mathrm { e x i n } } ) . } \end{array}
$$

where $\mathcal { N }$ denotes a Gaussian distribution. $\boldsymbol { \nu }$ denotes a uniform distribution. $f _ { 1 }$ and $f _ { 2 }$ represent the low and high-frequency sinusoidal components,respectively. $f _ { 3 }$ denotes the high-frequency modulation applied to the noise $\phi$ denotes a random phase shift. $w _ { 1 }$ ， $w _ { 2 }$ and $w _ { 3 }$ are the weighting coefficients for Gaussian noise,sinusoid-based periodic noise,and nonlinear noise,respectively. $\beta$ is the noise-intensity factor that determines the magnitude of the injected noise.The coefficient values are given as follows:

$$
f _ { 1 } = 0 . 1 \ \mathrm { H z }
$$

$$
f _ { 2 } = 5 ~ \mathrm { H z }
$$

![](images/a09fce6075d604f1134da5160eb95f73801be51feaee1f272324aa08cc3a26a4.jpg)
Fig.6.Estimation results and error plots of noise experiments.

$$
f _ { 3 } = 2 ~ \mathrm { H z }
$$

$$
w _ { 1 } = w _ { 2 } = w _ { 3 } = 1
$$

As shown in Fig. 6,after injecting two types of noise, the prediction trajectories of all models deviate from the true SoC to varying extents. In contrast, the proposed method remains closely aligned with the ground-truth SoC trajectory,with the least pronounced error growth especially around charge-discharge peaks and turning points.The error curves further indicate that the proposed method achieves the smallest absolute-error magnitude over the entire time domain,and no sustained errorelevation is observed after the high-frequency perturbations are introduced,demonstrating a stronger capability to suppress transient noise.As shown in Table 8,under Noise A,the proposed method attains an RMSE of $0 . 3 5 \%$ and an MAE of $0 . 2 8 \%$ .Compared with the best-performing baseline,TCN-BiLSTM,which yields $1 . 0 4 \%$ and $0 . 8 9 \%$ ，these values are reduced by approximately $6 6 \%$ and $6 8 \%$ ， respectively,while the maximum error decreases from $2 . 3 4 \%$ to $1 . 0 7 \%$ Under Noise B, the advantage becomes more pronounced.The proposed method achieves an RMSE and MAE of $0 . 2 4 \%$ and $0 . 1 8 \%$ ,respectively, representing reductions of about $7 6 \%$ and $7 7 \%$ relative to TCN-BiLSTM. These results indicate that the proposed approach maintains higher fidelity and stability even under more complex composite noise.

Table 8 Performance comparison under different noise types.

<table><tr><td rowspan="2">Noise type</td><td rowspan="2">Model</td><td colspan="6">Metrics (%)</td></tr><tr><td>RMSE</td><td>MAE</td><td>P95</td><td>Error Std</td><td>Max</td><td>R²</td></tr><tr><td>Noise A</td><td>CNN</td><td>1.13</td><td>0.96</td><td>2.10</td><td>0.68</td><td>3.58</td><td>99.28</td></tr><tr><td>Noise A</td><td>BPNN</td><td>1.51</td><td>1.22</td><td>2.85</td><td>1.51</td><td>4.46</td><td>98.73</td></tr><tr><td>Noise A</td><td>TCN-BiLSTM</td><td>1.04</td><td>0.89</td><td>1.81</td><td>0.88</td><td>2.34</td><td>99.40</td></tr><tr><td>Noise A</td><td>Proposed</td><td>0.35</td><td>0.28</td><td>0.68</td><td>0.32</td><td>1.07</td><td>99.93</td></tr><tr><td>Noise B</td><td>CNN</td><td>1.04</td><td>0.85</td><td>2.04</td><td>0.76</td><td>3.14</td><td>99.39</td></tr><tr><td>Noise B</td><td>BPNN</td><td>1.52</td><td>1.23</td><td>2.86</td><td>1.51</td><td>4.29</td><td>98.72</td></tr><tr><td>Noise B</td><td>TCN-BiLSTM</td><td>0.98</td><td>0.78</td><td>1.91</td><td>0.78</td><td>2.75</td><td>99.46</td></tr><tr><td>Noise B</td><td>Proposed</td><td>0.24</td><td>0.18</td><td>0.46</td><td>0.24</td><td>1.36</td><td>99.97</td></tr></table>

Combined with the box plots,it is evident that the proposed method exhibits the lowest median error, the narrowest interquartile range, and the fewest outliers.This indicates that it not only achieves a smaller average error but also presents a more concentrated error distribution with reduced fluctuations,thereby verifying the robustness of the proposed model under conditions of random measurement errors and complex in-situ noise.As shown in Table 8,under Noise A,the P95 of the proposed model decreases by approximately $7 3 \%$ compared to that of the BPNN model,and its Error Std decreases by approximately $7 7 \%$ .Under Noise B,when compared with the superiorperforming TCN-BiLSTM model, the P95 and Error Std of the proposed method are reduced by approximately $7 5 \%$ and $6 8 \%$ ,respectively. The aforementioned analysis validates that the proposed model possesses an enhanced capacity for controlling the $9 5 \%$ sample error and exhibits diminished residual fluctuations.

In summary,the proposed method maintains stable estimation amidst random measurement noise and composite nonlinear interference.This demonstrates that the introduced time-frequency feature representation can effectively suppress the impact of high-frequency disturbances on the estimation,while the physical constraint mechanism aids in mitigating the cumulative deviations that may emerge during dynamic processes.Consequently,this significantly enhances the reliability and generalizability of the model in complex noise scenarios.

# 5.4.Initial value experiment

Accurately knowing the initial SoC is crucial before performing algorithmic estimation.However,in practical applications,the initial value assumed by the algorithm may deviate from the true battery state.Therefore,to validate the robustness of the proposed method under different initial SoC values,we set the initial SoC to O.7O,0.50, and O.30,respectively,and conducted verification under two different operating conditions.The results are shown in Fig.7(a) and (b).

The proposed algorithm maintains accurate SoC estimation even under large initial-SoC deviations,with fast convergence and strong adaptability to different initial SoC values.This indicates that the method is insensitive to initial-condition errors,mainly for two reasons. First,the model does not rely solely on propagation from the initial SoC;instead,it constructs a multi-source feature representation using exogenous variables such as current,voltage,OCV,temperature,and flow rate.At each time instant, sufficient measurable information is available to correct the state,preventing the initial bias from continuously accumulating over time.Second, the hierarchical physical constraints guide the SoC update to follow physically plausible evolution trends,thereby enhancing convergence and stability against initial-state perturbations.

# 5.5.Comparative experiment of diffrent loss functions

The effectiveness of incorporating physical information into the model has been validated through this studies.This experiment focuses on comparing conventional regularization loss terms with the proposed layered physical constraints.During the experiment, the electrochemical constraints used in this work are incorporated into the network in the form of a loss function.This approach replaces the physics-embedding scheme adopted in the paper while keeping all other settngs identical,and the estimation results are shown in Fig. 7(c).

From the experimental results,conventional regularization-based models are prone to overshoot during operating-condition transitions, primarily due to the limitations of backpropagation-based gradient penalties.This strategy penalizes physically inconsistent outputs only during backpropagation via the loss function; however,its effectiveness depends on hyperparameters and can be dominated by data-driven loss terms,causing the constraint to become ineffective under distribution shifts such as operating-condition switching.The proposed model yields smoother estimation results,mainly benefiting from the layered physics-embedding design.By embedding Faraday's law into the physical memory unit and the Nernst equation into the output layer, a full-process physical constraint is established across feature extraction, feature enhancement,and output correction, rather than relying solely on gradient adjustment through backpropagation. For example, during charge and discharge switching, the physical memory unit preserves historical charge accumulation via the GRU gating mechanism, preventing abrupt SoC changes induced by current steps.Meanwhile, the physics-constrained output layer directly rectifies estimation values that deviate from the Nernst equation,ensuring consistency with the electrochemical mechanism.

Table 9 Evaluation metrics for the random current experiment.

<table><tr><td rowspan="2">Model</td><td colspan="6">Metrics (%)</td></tr><tr><td>RMSE</td><td>MAE</td><td>P95</td><td>Error Std</td><td>Max</td><td>R</td></tr><tr><td>CNN</td><td>0.76</td><td>0.69</td><td>1.27</td><td>0.36</td><td>2.04</td><td>97.58</td></tr><tr><td>BPNN</td><td>0.47</td><td>0.32</td><td>0.33</td><td>0.41</td><td>1.88</td><td>99.10</td></tr><tr><td>TCN-BiLSTM</td><td>0.26</td><td>0.17</td><td>0.43</td><td>0.26</td><td>1.17</td><td>99.71</td></tr><tr><td>Proposed</td><td>0.11</td><td>0.08</td><td>0.15</td><td>0.11</td><td>0.66</td><td>99.95</td></tr></table>

# 5.6. Random current experiment

This experiment simulates the random current commands for grid frequency regulation,where the current signal has no fixed pattern, encompassing trends of sudden increases and decreases.The model's performance in real-world application scenarios is verified.The comparison of estimation results is shown in Fig.8,and the estimation performance metrics are shown in Table 9.

In the baseline CNN,local convolutions fail to capture the global fluctuations of stochastic current profiles,leading to repeated estimation overshoots, which are particularly pronounced at current switching instants.The BPNN updates its weights via gradient descent and is prone to local optima;moreover,without a physics-based constraint mechanism,its generalization deteriorates sharply under rapid current variations,accompanied by evident oscillations.The TCN-BiLSTM performs better than the first two models;however,in the absence of physical-law constraints,abrupt changes occur near extrema,resulting in relatively large errors.

The proposed model demonstrates strong adaptability to complex, highly dynamic operating conditions.Its key advantage lies in the synergistic integration of time-frequency features and physics-based constraints.Frequency-domain feature extraction captures both highfrequency transients and low-frequency trends in stochastic current profiles,preventing high-frequency information loss inherent to purely time-domain methods.The physics-constrained output module corrects integration drift under stochastic currents by enforcing charge conservation.This ensures that,even in previously unseen stochastic scenarios,the estimation results remain consistent with the electrochemical principles of VRFB.These results indicate that the proposed architecture is better suited to practical frequency-regulation conditions, supporting its feasibility for engineering applications.

The quantitative metrics in Table 9 demonstrate that the proposed model achieves optimal performance under random current conditions. Compared to the CNN model, the P95 of the proposed model exhibits the most substantial reduction, decreasing by $8 8 \%$ .The superiority of this metric underscores the model's formidable capacity for sample error control.Additionally,the Error Std demonstrates the maximum reduction of $7 3 \%$ when compared to the BPNN model. The minimized Error Std signifies the lowest degree of dispersion in the prediction residuals,thereby indicating enhanced stability.Concurrently, the $\mathtt { R } ^ { 2 }$ of the proposed model reaches $9 9 . 9 5 \%$ ,indicating the highest fitting precision to the true SoC,which enables the accurate capture of dynamic variation patterns under random currents.

In summary, the proposed framework achieves SoC estimation with superior accuracy,enhanced stability,and robust performance under complex and highly dynamic operating conditions.This effectively validates the synergy between time-domain feature representations and physical constraints.

It should be noted that the experimental validation in this study is conducted on VRFB.Cost-driven flow-battery variants,such as ironbased systems,have attracted attention due to their advantages in material cost and resource availability [39].Nevertheless,they also exhibit chemistry-specific differences in reaction kinetics,suppression of side reactions,solubility and deposition behavior,and key component matching.Accordingly,while the proposed framework has the potential for cross-chemistry transfer,it must satisfy explicit conditions.

![](images/989fbf33377eb39a03467c72ae917b5045992bf03043917775afcb4d7f1b3d17.jpg)
Fig.7.Results of the initial-condition experiments: (a)-(b)and the los-function comparison experiment (c).

On the one hand, the hierarchical embedding and time-frequency representation modules are data-driven modeling components that mainly relyon measurable input signals; thus,if other flow-battery chemistries provide commonly measurable inputs such as current, terminal voltage, temperature,and flow rate,these components are largely reusable.On the other hand, the reference ground-truth calibration and the physicalconstraint branch are chemistry-dependent.When transferring to ironbased or other chemistries,it is necessary to re-establish the OCV-SoC calibration for the target chemistry and to re-parameterize key parameters and/or mechanistic terms in the physical constraints,while updating the error-source analysis by incorporating chemistry-specific side reactions and operational constraints.

# 5.7. Sensitivity analysis experiment

During the long-term operation of VRFB,ion crossover through the membrane and side reactions induce variations in the active vanadium ion concentration within the electrolyte,which macroscopically manifests as continuous capacity fading.To verify the generalization capability of the proposed model during the later stages of the battery life cycle,a sensitivity analysis focusing on the degradation of capacity parameters $C _ { \mathrm { n o m } }$ is designed in this section.

In the physical feature enhancement module proposed in this work, the current is physically normalized according to Faraday's law to establish a direct correlation with the physical significance of SoC variations,as expressed in Eq.(26).However,this normalization process is inherently susceptible to the selected value of the rated capacity.

To simulate the phenomenon of capacity fading,decay deviations were introduced into the baseline parameter of the rated capacity during the model inference phase,reducing it by $5 \%$ ， $1 5 \%$ ,and $2 0 \%$ ,respectively.This capacity degradation is utilized to equivalently emulate various aging stages of the battery.Subsequently, the SOC estimation performance of the model was re-evaluated,and the corresponding experimental results are presented in Table 10.

As observed from the data in Table 1O,as the capacity fading ratio increases,Faraday's law of charge conservation within the physical constraint layer deviates from the actual state,resulting in an anticipated upward trend across the error metrics of the model. When the battery exhibits no capacity degradation,the RMSE and Max of the model are maintained at relatively low levels of $0 . 3 2 4 \%$ and $1 . 2 7 2 \%$ ， respectively.When the battery experiences capacity fading of $5 \%$ and $1 5 \%$ ,although the RMSE of the model increases,it remains strictly controlled at $0 . 6 1 9 \%$ and $0 . 8 4 9 \%$ . Even under conditions simulating severe battery agingwitha sharp capacity drop of $2 0 \%$ ,the RMSE of the model only exhibits a marginal increase to $1 . 0 8 1 \%$ ，and the Max, which represents the worst-case scenario,remains at $2 . 3 1 0 \%$ These experimental results demonstrate that the proposed framework retains robust estimation capability even when confronted with aging scenarios characterized by severe concentration deviations.

![](images/7647f5695c1fb5c6be716e5aa7896f2744289562965703e30ce37360538e0041.jpg)
Fig.8.Estimation results and error plots of the random current experiment

Table 10 Sensitivity analysis of capacity degradation.

<table><tr><td rowspan="2">Battery capacity degradation ratio</td><td colspan="4">Metrics (%)</td></tr><tr><td>RMSE</td><td>MAE</td><td>Max</td><td>R</td></tr><tr><td>0%</td><td>0.324</td><td>0.238</td><td>1.272</td><td>99.95</td></tr><tr><td>5%</td><td>0.619</td><td>0.504</td><td>1.334</td><td>99.93</td></tr><tr><td>15%</td><td>0.849</td><td>0.696</td><td>2.102</td><td>99.85</td></tr><tr><td>20%</td><td>1.081</td><td>0.995</td><td>2.310</td><td>99.76</td></tr></table>

# 6. Conclusion

To address the challenges of SoC estimation for VRFB under dynamic operating conditions,including incomplete feature representation,insufficient treatment of variable heterogeneity,and limited physical interpretability,this study proposes a SoC estimation framework that integrates time-frequency features with hierarchical physical constraints.A time-frequency feature extraction module is designed to provide a more comprehensive representation,while a physical feature enhancement module and a physically constrained output module are further introduced to strengthen and regularize the fused features.As aresult,high-accuracy and high-robustness SoC estimation is achieved undercomplex operating scenarios.

The effectiveness of the proposed method is validated through a series of experiments. Compared with the conventional coulomb counting method, the proposed approach reduces the maximum error by $2 0 \%$ .Across different operating conditions,the maximum error of the proposed model remains below $3 \%$ ,and $\mathtt { R } ^ { 2 }$ stays above 0.99.Notably, in two high-frequency dynamic experiments, namely the noise-injection test and the random-current test, the model maintains favorable estimation accuracy and robustness in the presence of measurement noise and rapidly varying current profiles.Moreover,no physically implausible estimates are observed during mode transitions.

Future work can be further expanded and deepened along the following two directions:

First,constructing a multi-time-scale joint estimation framework for SoC and state of health (SOH) [4O].Considering the significant difference in time scales between the slowly varying characteristics of battery capacity degradation and the high-frequency abrupt mutation characteristics of dynamic currents,subsequent research plans to couple a multi-time-scale joint estimation mechanism into the existingarchitecture [41].Specifically,the high-frequency dynamic feature extraction model proposed in this paper will be maintained at the microscopic time scale,while a capacity degradation prediction submodule will be introduced at the macroscopic cycle scale [42]. This submodule will utilize long-term charge-discharge historical features to evaluate the actual capacity loss inside the battery in real time, and adaptively feed the updated rated capacity back to the physicsconstrained layer.Through such synergistic state monitoring and online dynamic calibration of model parameters,it is expected to alleviate the model generalization issues caused by long-term aging,thereby ensuring the robustness of the model during the middle and later stages of the battery lifecycle.

Second,introducing online concentration monitoring to achieve high-precision refined dual-SoC modeling [43]. The asymmetric imbalance of the positive and negative electrolytes induced by transmembrane ion crossover constitutes another underlying physical root cause of error accumulation during the long-term operation of the VRFB. To this end,subsequent research plans to configure non-invasive optical sensing equipment,such as dual-channel ultraviolet-visible (UV-Vis) spectroscopy [44]，within the fluid pipelines to conduct real-time, independent,and refined measurements of the ion concentrations in the positive and negative half-cells during operation. Integrated with the transient transmembrane physical model [45],the current single SoC prediction will be extended into a dual-state synergistic perception framework encompassing the positive electrode and the negative electrode.This deep integration of physical hardware perception and algorithmic mechanisms can provide an absolute concentration groundtruth reference for the underlying Nernst constraint module,thereby fundamentally mitigating the cumulative errors induced by electrolyte imbalance.

# CRediT authorship contribution statement

Xuan Liu:Writing-original draft,Validation,Methodology,Conceptualization.Lifeng Cao: Supervision.Kai Li: Visualization.Jinquan Wang: Funding acquisition. Gang Dang: Data curation. Mifeng

Ren: Software. Gaowei Yan: Writing-review & editing, Supervision, Funding acquisition. Suxia Ma:Resources.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Acknowledgments

This work was supported by the Shanxi Province General Program of Natural Science Research (202403021221055),Shanxi Province Major Special Program of Science and Technology (202501060301003), and Saiying Technology Innovation Fund Project (2025-01).

# Data availability

Data will be made available on request.

# References

[1]Y.Wang,H. Zuo,L.Cao,H. Ren,J.Wang,G.Yan， S.Ma,An uncertainty information-guided optimization method for economic scheduling of PV-BESS systems, Energy (2025) 139794.
[2] C. Sun, E. Negro, K. Vezzu, G.Pagot, G. Cavinato,A. Nale, Y.H. Bang, V. Di Noto, Hybrid inorganic-organic proton-conducting membranes based on SPEEK doped with WO3 nanoparticles for application in vanadium redox flow batteries, Electrochim. Acta 309 (2019) 311-325.
[3] H. Zhang,C. Sun, Cost-effective iron-based aqueous redox flow batteries for large-scale energy storage application: A review, J. Power Sources 493 (2021) 229445.
[4] B.Dunn, H. Kamath, J.-M. Tarascon, Electrical energy storage for the grid: a battery of choices, Science 334 (6058) (2011) 928-935.
[5] C.Ding,H. Zhang, X. Li, T. Liu,F. Xing,Vanadium flow battery for energy storage: prospects and challenges, J. Phys. Chem. Lett. 4 (8) (2013) 1281-1294.
[6] W.-Y. Chang, The state of charge estimating methods for battery: A review, Int. Sch. Res.Not. 2013 (1) (2013) 953792.
[7] R. Feng, Z. Guo, X. Meng, C. Sun,Modeling and state of charge estimation of vanadium redox flow batteries: A review, Energies 18 (17) (2025) 4666.
[8]C. Stolze, J.P.Meurer, M.D. Hager, U.S. Schubert, An amperometric, temperatureindependent, and calibration-free method for the real-time state-of-charge monitoring of redox flow battery electrolytes,Chem.Mater.31 (15) (2019) 5363-5369.
[9]M.R. Mohamed, H. Ahmad,M.A. Seman, Estimating the state-of-charge of allvanadium redox flow battery using a divided, open-circuit potentiometric cell, Elektron. Elektrotechnika 19 (3) (2013) 37-42.
[10] C. Sun,E. Negro,A. Nale,G.Pagot,K. Vezzu,T.A. Zawodzinski, L. Meda, C. Gambaro，V. Di Noto，An eficient barrier toward vanadium crossover in redox flow batteries: The bilayer [Nafion/(WO3) x] hybrid inorganic-organic membrane, Electrochim. Acta 378 (2021) 138133.
[11]C. Sun, A. Zlotorowicz, G. Nawn, E. Negro,F. Bertasi, G. Pagot, K. Vezzu, G. Pace, M. Guarnieri, V. Di Noto,[Nafion/(WO3) x] hybrid membranes for vanadium redox flow batteries, Solid State Ion. 319 (2018) 110-116.
[12] D.Han,K. Yoo,P. Lee,S. Kim,S.Kim,J.Kim, Equivalent circuit model considering self-discharge for SOC estimation of vanadium redox flow battery, in: 2018 2lst International Conference on Electrical Machines and Systems, ICEMS, IEEE, 2018,pp.2171-2176.
[13]Y. Zhang, J. Zhao,P. Wang, M. Skyllas-Kazacos, B. Xiong, R. Badrinarayanan, A comprehensive equivalent circuit model of all-vanadium redox flow battery for power system analysis, J. Power Sources 290 (2015) 14-24.
[14]B．Xiong，J. Zhao，Z. Wei，M. Skyllas-Kazacos，Extended Kalman filter method for state of charge estimation of vanadium redox flow battry using thermal-dependent electrical model, J. Power Sources 262 (2014) 50-61.
[15] S.Dong,J.Feng, Y. Zhang,S.Tong, J. Tang, B. Xiong, State of charge estimation of vanadium redox flow battery based on online equivalent circuit model, in: 2021 3lst Australasian Universities Power Engineering Conference,AUPEC, IEEE, 2021, pp. 1-6.
[16] C. Yang,J. Liu, Z. Gao,D. Song,W. Yang,H. Wang,A strategy for state of charge estimation of lithium-ion battery via an adaptive cubature Kalman filter based on fractional-order model, IEEE Trans. Instrum. Meas. (2025).
[17] G.L. Plett, Extended Kalman filtering for battery management systems of LiPBbased HEV battry packs: Part 3. State and parameter estimation, J. Power Sources 134 (2) (2004) 277-292.
[18] I.N. Idrisov,Y. Khan, S.D. Bogdanov, M.A. Pugach, F.M. Ibanez, Digital twin for state of charge estimation of a vanadium redox flow battry,in: 2024 IEEE 25th International Conference of Young Professionals in Electron Devices and Materials, EDM, IEEE, 2024, pp.1880-1884.
[19] Z.Liu,Z.ZhaoY.Qiu,B.Jing,C.Yang,Stateofchargeestimation forLiion bateries based on iterative Kalman filter with adaptive maximum correntropy criterion, J. Power Sources 580 (2023) 233282.
[20] S. Tong,J.H. Lacap, J.W. Park， Batery state of_charge estimation using a load-classfying neural network, J.Energy Storage7 (2016)236-243.
[21]M.Kharseh，M.BalahK.AlamaraEstimatingstateofchargeoftter inrenewable energy systems:a data-driven approach with artificial neural networks, Clean Energy 8 (6) (2024) 134-147.
[22] T. Zhang, Y.Wang, R. Li, State-of-charge estimation for vanadium redox flow batery using a multi-head attention-based LSTM network, J. Energy Storage 143 (2026) 119667.
[23] H. Niu,J. Huang, C. Wang, X. Zhao,Z. Zhang,W. Wang, State of charge prediction study of vanadium redox-flow battery with BP neural network, in: 2020 IEEE International Conference on Artificial Intelligence and Computer Applications,ICAICA, IEEE, 2020,pp. 1289-1293.
[24] X.Li, J. Xiong,A. Tang,Y. Qin,J. Liu,C. Yan, Investigation of the use of electrolyte viscosity for online state-of-charge monitoring design in vanadium redox flow battery,Appl. Energy 211 (2018) 1050-1059.
[25] Y. Wang,H. Wu,J. Dong, G. Qin,H. Zhang, Y. Liu, Y. Qiu, J. Wang, M. Long, Timexer: Empowering transformers for time series forecasting with exogenous variables, Adv. Neural Inf. Process. Syst. 37 (2024) 469-498.
[26] A. Tang, J. Bao,M. Skyllas-Kazacos, Studies on pressure losses and flow rate optimization in vanadium redox flow battery，J. Power Sources 248 (2014) 154-162.
[27]K.-H.Kim,K.-H.Oh，H-S.Ahn,H.-D.Choi，Time-frequencydomain_deep convolutional neural network for Li-ion battery SoC estimation， IEEE Trans. Power Electron.39 (1) (2023) 125-134.
[28] L. Kong, S.Fang,T.Niu, G. Chen,L. Yang,R. Liao, Fast state of charge estimation for lithium-ion battery based on electrochemical impedance spectroscopy frequency feature extraction, IEEE Trans.Ind. Appl. 60 (1) (2023) 1369-1379.
[29] K.Li,Y. Zhang,H. Liu,Y.You,L. Zeng,Y.Hong,Z. Zhang,Z. He,A novel temporal-frequency dual attention mechanism network for state of charge estimation of lithium-ion battery, J.Power Sources 622 (2024) 235374.
[30] M. Raiss, P. Perdikaris, G.E. Karniadakis,Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations, J. Comput. Phys. 378 (2019) 686-707.
[31]J.Li, W. Ziehm,J.Kimball,R. Landers,J.Park,Physical-based trainingdata coletion approach for data-driven lithium-ion battery state-of-charge prediction, Energy AI 5 (2021) 100094.
[32] S. Singh, Y.E. Ebongue,S. Rezaei, K.P. Birke, Hybrid modeling of lithium-ion batery: Physics-informed neural network for battery state estimation, Bateries 9 (6) (2023) 301.
[33]M. Hiremath, K. Derendorf, T.Vogt, Comparative life cycle assessment of battery storage systems for stationary applications, Environ. Sci. Technol. 49 (8) (2015) 4825-4833.
[34] Q.-a. Zhang, H. Yan, Y.Song, J. Yang, Y. Song,A. Tang,Boosting anode kinetics in vanadium flow batteries with catalytic bismuth nanoparticle decorated carbon felt via electro-deoxidization processing,J. Mater. Chem.A 11 (16) (2023) 8700-8709.
[35] S. Chen, C.Sun, H. Zhang,H. Yu,W.Wang,Electrochemical deposition of bismuth on graphite felt electrodes: Influence on negative half-cell reactions in vanadium redox flow batteries, Appl. Sci. 14 (8) (2024) 3316.
[36]Y.Liu, T.Hu,H. Zhang,H.Wu, S.Wang,L. Ma,M.Long,Itransformer: Inverted transformers are effective for time series forecasting,2O23,arXiv preprint arXiv: 2310.06625.
[37] Y. Zhao, C. Zhang,M. Wang, C.Song, J.Li,M. Zheng, State of charge estimation for flow bateries based on electrochemical impedance spectroscopy and temporal convolutional network-bidirectional long short-term memory network hybrid model, J. Power Sources 657 (2025) 238161.
[38] C. Zheng,W.Feng, Z. Wei, Y.Li, H.H.C. Iu,T.Fernando, X. Zhang,A robust machine learning-based SOC estimation_approach for vanadium redox flow battery, J. Power Sources 645 (2025) 237087.
[39] Z. Huan,C.Sun, M.Ge,Progress in profitable fe-based flow bateries for broadscale energy storage，Wiley Interdiscip.Rev.: Energy Environ.13 (6) (2024) e541.
[40] X.Li，D.Mu,Y.Ning,Y.Song,Joint SOC/SOH estimationof al-vanadium flow bateries based on DAUKF algorithm, in: 2O23 5th International Academic Exchange Conference on Science and Technology Innovation， IAECST, IEEE, 2023, pp.1413-1418.
[41] Z. Wei, J. Zhao,D.Ji, K.J. Tseng, A multi-timescale estimatorforbaterystate of charge and capacity dual estimation based on an online identified model, Appl. Energy 204 (2017) 1264-1274.
[42] B. Khaki, P.Das,Fast and simplified algorithms for SoC and SoH estimation of vanadium redox flow batteries,in: 2021 IEEE Green Technologies Conference, GreenTech, IEEE,2021, pp.494-501.

[43] A.A. Maurice, A. Bernaldo de Quirós, S. Sevilla, V. Mufioz Perales, P.A. Prieto-Diaz,A.E.E. Quintero Gamez, M. Vera, Monitoring the state of charge imbalance of vanadium redox flow batteries via dual online UV/Visible spectroscopy,in: Electrochemical Society Meeting Abstracts 243, The Electrochemical Society, Inc., 2023,46,2493-2493.

[44]S.-C. Chuang, C.-H. Kuo, Y.-M. Wang, N.-Y. Hsu, H.-J. Lin, J.-Y. Kuo, C.-C. Chou, A non-invasive optical sensor for real-time state of charge and capacity fading tracking in vanadium redox flow batteries, Energies 18 (23) (2025) 6366.
[45] S.P.Vudata,D. Bhattacharyya, Transient modeling of a vanadium redox flow battery and real-time monitoring of its capacity and state of charge,Ind. Eng. Chem. Res.61 (48) (2022) 17557-17571.