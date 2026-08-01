Research papers

# Adaptive estimation of SOC and capacity of iron-chromium redox flow battery based on improved parameter identification and unscented Kalman filtering

Yang Liua,b, Weibin Jiangc, Qianqian Zengb, Xi Liub.d, Guanchen Liub, Xiaoyin Xie b, Sheng Wu a, Chongyang Xu a,

aYantai Research Institute,Harbin Engineering University,Yantai, Shandong 264oo3,China bSchoolofeistrydemicalThologyHubeiytecnicUiversityHuangshi50 Yantai Taixin Electronics Technology Co.,Ltd, 2640o6,China dSchoolofsicsdElectroicformationntai Universityntai6o,in

# ARTICLEINFO

# ABSTRACT

Keywords:   
Iron-chromium redox flow battery   
Self-discharge loss first-order RC model   
Improved AFFRLS   
Joint estimation of low-order SOC and capacity

Due to the influence of side reactions on the exchange membrane,the iron-chromium redox flow battery (ICRFB) experiences electrolyte imbalance and capacity decay during operation.Therefore,accurately estimating the ICRFB's capacity and state of charge (SOC) is equally important.Although existing collaborative estimation methods efectively address model dynamics by combining parameter identification and state estimation,potential cros-talk within the integrated framework may stilltreaten the stability and accuracy of the computations.In this research,a strategyof decoupling the parameter identification from the state estimation proces is adopted to eliminate the risk of cros-talk.Specifically,we propose an improved adaptive forgetting factor recursive least squares (IAFFRLS)algorithm for online parameter identification,followed by theconstruction of a state estimator based on unscented Kalman filtering (UKF),which accurately estimates both the SOC and batery capacity simultaneously.Furthermore,the two-dimensional state vectors, which include only SOC and capacity, significantly enhance computational speed and numerical robustnessLaboratory-scale experimental validation of the ICRFB demonstrates that the proposed method achieves excellent accuracy and remains robust under variations in real-time operating conditions.A comparison with existing methods further confirms the combined advantages of the proposed method in terms of estimation precision,convergence,and processing cost.

# 1． Introduction

The rational use of energy is becoming more and more important as people's concerns about energy shortages and environmental issues continue to grow.Therefore,advancing the development of renewable energy has become a key strategy for addressing climate change and promoting sustainable development[1,2].Liu etal.demonstrated that if Chinaactively develops renewable energy over the next thirty years, electricity generated from wind and solar power could meet two-thirds of their electricity demand by 2O5o [3].But these energy sources due to their intermittent,peak generation of too much power is difficult to fully utilize.Battery storage systems can store excess electricity chemically for extended periods,mitigate the instability of renewable energy outputs by regulating frequency，filling in peaks and valleys,and dynamically providing on-demand output, thereby enhancing the flexibility of sustainable energy integration into the grid.Among the various types of batteries,flow batteries exhibit the most potential with their independently designed capacity and power advantages. The representative Iron-chromium redox flow battery(ICRFB) is recognized as the first true redox flow battery(RFB),which is a cost-effective and highly efficient energy storage system utilizing the abundant and inexpensive FeCl2 and CrCl3 as active materials for long term use and deep charge/ discharge cycling [4].In comparison to other RFBs,such as the all-vanadium flow battery (VRFB) and the zinc-bromine flow battery (ZBFB), ICRFB exhibita comparable cycle life.However,their electrolyte is less expensive,less environmentally harmful,and safer.Furthermore,the RFBs offers high scalability by decoupling the energy storage unit from the power output, which makes ICRFB particularly suitable for largescale grid energy storage [5,6]. In recent years, some researchers have improved the efciency and performance of ICRFB to a certain extent through the modification studies of electrolyte and electrode materials, as well as the optimizations of battery structure and system design [7-9]．With the efforts of numerous scholars,ICRFB is gradually developing into a cost-effective and high-performance energy storage technology，playing an important role in advancing the large-scale deployment of renewable energy [10].

![](images/a80cd1a0c73c1f818fe258e718b4de2677b5bfd35bc462b39ee8052879c45d61.jpg)  
Fig.1.First-order RC model considering self-discharge losses.

Despite extensive research by many scholars on unit design, testing, and performance enhancement of ICRFB,in-depth exploration of system-level techniques is necessary to realize its commercial application.A reliable battery management system (BMS) is also necessary to enhance the long-term stability and eficiency of the ICRFB system through precise charge/discharge control,flow regulation,and temperature management [11-16]. State of charge(SOC) is a key indicator of the BMS,which indicates the battery's residual charge and also estimates the remaining usage time of the battery [17].In addition, the SOC helps the BMS assess the risk of overcharging or overdischarging the battery,ensuring safe battery operation.However,since ICRFB is a complex nonlinear time-varying electrochemical system,direct measurements of SOC and capacity are relatively challenging,and thus SOC and capacity estimation for ICRFB primarily depends on indirect methods [18].Accurate ICRFB state estimation relies on accurate modeling,and for lithium and vanadium batteries,extensive research has focused on equivalent circuit models (ECM) [19].A substantial body of literature confirms that ECM-based SOC observers are accurate and feasible,and that SOC can be accurately estimated from experimental currents and measured terminal voltages [2O]. For the purpose of increasing the model's accuracy, Xiong et al. proposed a VRFB model and incorporated the particle swarm optimization (PsO) algorithm for offline parameter identification.Model accuracy can be significantly reduced under actual working conditions due to the influence of multiple factors,including temperature, flow rate,current,and aging on model parameters [21]. Xiong et al.also proposed an ECM that includes a capacity decay factor to predict the battery's capacity loss with the increasing number of cycles. Based on this model,an adaptive sliding mode observer is used for SOC estimation.However,the offline identified parameters do not adapt to external influences in real-time [22]. The study by Zhang etal. introduced a comprehensive ECMof the VRFB for conducting system-level analysis,accounting for the intrinsic characteristics of shunt current and pump energy dissipation of the VRFB. Their model achieved high accuracy in predicting terminal voltage and pump power errors [23].

Qiu et al.introduced a modified extended Kalman filter (EKF) to estimate the SOC of a VRFB by applying an adaptive gain factor,and their results confirmed the superior benefit of the IEKF for SOC estimation in industrial applications.Furthermore,they proposed a data fusion method based on the estimation outcomes of EKF and AEKF, resulting in two improved estimation methods: the DF-EKF and the DF-AEKF.The improved method shows higher precision and fidelity in SOC estimation [24]. Zhao etal.proposed a Kalman filtering method based on a forgetting factor,which accurately estimates the SOC by factoring in the effects of the battery's past states on its current status,and calculates the capacity of the battery using the estimated SOC value,but their ECM model does not take into account the influence of factors such as pump loss and hydrogen evolution [25].Currently there are two approaches of estimating the capacity of liquid flow batteries,one so that the capacity is coupled in the state vector,estimated jointly with the SOC.[26] The other approach involves decoupling the SOC from the capacity and using the obtained SOC to achieve an accurate estimation of the capacity by the Ampere-hour (AH) integration method [27].Lee et al.used dual EKF to estimate SOC and capacity of Li-ion batteries, while the parameters of the ofline ECM model could not compensate for the changes in the battery's operating conditions and the alterations in the internal mechanism of the battery [28]．Aiming to lower the computational complexity of estimating the capacity and dynamic SOC, some scholars have used a dual EKF on a multiscale framework to estimate SOC and capacity [29].Not only does it reduces the crossover interference of coupled estimates,but also improves computational efficiency[3O].A fourth-order EKF-based approach for joint estimation of SOC and capacity was introduced by Zou et al. The method can periodically update parameters such as resistance and capacitance to achieve SOC and capacity estimation on a macroscopic time scale. However, high-dimensional matrix operations increase the computational effort and are difficult to execute in real time on low-cost MCUs,so the algorithm needs to offline operation to preserve its stability [31].

In previous studies,it is often challenging to balance computational complexity and accuracy,especially when capacity estimation is incorporated,and high-order matrix operations significantly increase the MCU computational burden.Moreover,unlike the VRFB and lithium battery,the voltage of the ICRFB changes more gently at the same current density of charge and discharge current, and the slowly changing voltage further increases the difficulty of estimation [6].To achieve greater accuracy and stability in calculations,this research establishes a first-order resistance-capacitance(RC) ECM of ICRFB,including selfdischarge loss,and identifies the parameters online based on the proposed improved adaptive forgetting factor recursive least squares (IAFFRLS) under the DST operating condition, followed by joint estimation of the SOC and capacity.The model identification based on IAFFRLS is constructed to be completely disconnected from the state estimation based on adaptive unscented Kalman filter (AUKF),by this means,the crossover interference between estimation accuracy and numerical stability can be effectively reduced. Unlike typical state estimators, that only incorporate SOC and capacity, the proposed method results in considerable improvements in stability and computational efficiency.The analysis results indicate that the method presented in this paper achieves both good accuracy and robustness. The methodology implemented in this study shows superiority with respect to convergence,and computational speed,which is further demonstrated by comparison with other commonly used methods.This study is organized into the following sections:The second section presents the developed ICRFB model and the improved parameter identification method.Part 3 then focuses on the construction of the SOC and capacity estimators and the estimation algorithms employed.The fourth part describes the design and operation flow of the experimental platform.Finally,in Part 5,we verify the feasibility of the algorithm and analyse the result.

# 2.ICRFB modeling and parameter identification process

# 2.1.Modeling of equivalent circuit considering self-discharge

Toaccurately reflect the dynamic performance and characteristics of the battery,an accurate battery model is essential,and this step directly impacts the subsequent precise estimation of the model parameters. Typically,the higher order of the battery model the more accurate the prediction of the terminal voltage,but it will increase the complexity and computational difficulty of the model.To balance the complexity of the model and the prediction accuracy,the first-order model is the most eclectic choice.As illustrated in Fig.1.

Table 1 The process of transforming the regression form of the ECM.   

<table><tr><td>Laplace transform Eq. 3:</td><td>U(S)/It(S)=Ri/(1+RCiS)</td></tr><tr><td>Let EL =Eo-Eocv:</td><td>EL(S)/It(S)=-(R1+RoRiCiS+Ro)/(1+RCiS)</td></tr><tr><td>Bilinear transformation:</td><td>E[(z-1)/It(z-1)=</td></tr><tr><td></td><td>-((TsR1+2RiCiRo+TsRo)+(TsRi-2RiCiRo+TsRo)z-1)/(Ts+2RiC1+(Ts-2RiC1)z-1)</td></tr><tr><td>Simplified: Reverse:</td><td>E[(z-1)/1t(z-1)=(02+0z-1)/(1+0z-1)</td></tr><tr><td>Simplified:</td><td>ELk=-01,kEqk-1+02KItk+03,ILk-1 ELk=kOk</td></tr></table>

Table 2 FFRLS algorithm process.   

<table><tr><td>Initialize:</td><td>P,O0,,I0,EL,</td></tr><tr><td>Update gain matrix:</td><td>Kk=Pk-1(a+ΦxPk-1)-1</td></tr><tr><td>Update innovation:</td><td>ε=ELk-Φkk-1</td></tr><tr><td>Update parameter:</td><td>0=0k-1+Kkεk</td></tr><tr><td>Update covariance:</td><td>Pk=(I-KkΦk)Pk-1-1</td></tr></table>

$\mathtt { E } _ { \mathrm { { O C V } } }$ indicates the true open circuit voltage (OCV) of ICRFB,influenced by SOC and temperature. $\mathrm { R } _ { 0 }$ characterizes the ohmic losses inside the ICRFB,which are caused by multiple factors both inside the battery (such as electrolytes,electrodes,etc.）and outside.The parallel resistance $\mathrm { R } _ { \mathrm { s h u n t } }$ is utilized to characterize the losses caused by the selfdischarge phenomenon of the cell due to the flow of $\mathrm { F e / C r }$ ions through the tubes and carbon plate channels [32].A parallel RC network is used to simulate the transient dynamics process during the operation of the ICRFB. ${ \mathrm { R } } _ { 1 }$ signifies the polarization resistance,while $\mathrm { C _ { 1 } }$ denotes the polarization capacitance.Both the load current (I) and the terminal voltage $\left( \operatorname { E } _ { 0 } \right)$ are measurable quantities.SOC is a function of $\mathtt { E o c v }$ ,which is calculated using the Nernst equation in Eq. (1).

$$
E _ { O C V } = E _ { \theta } + 2 l n ( S O C / ( 1 - S O C ) ) { \cdot } R _ { g \mathrm { a s } } T _ { T \mathrm { e m p } } / F
$$

where $\mathtt { E } _ { \theta }$ is the equilibrium potential (1.18 V), $\mathrm { R } _ { \mathrm { g a s } }$ is the gas constant (8.3145 $J / { \mathrm { K } } { \cdot } { \mathrm { m o l } } $ ， $\mathrm { T } _ { \mathrm { T e m p } }$ is the operating temperature (in K),and F is the Faraday constant (96,485C/mol).However, since the activity coefficient and standard potential of ICRFB vary with temperature [33],an error occurs when using the Nernst equation at $6 5 ~ ^ { \circ } \mathrm { C } .$ ·In this study,the OCV-SOC relationship is determined by fitting a polynomial function,as shown in Eq. (2),where $\mathbf { a _ { i } }$ denotes the coeficients of the polynomial.

$$
O C V = \sum _ { i = 0 } ^ { m } a _ { i } S O C ^ { i }
$$

In accordance with Kirchhoffs voltage and current laws, Eqs. $( 3 )$ and (4) describe the electrical characteristics of the first-order RC model:

$$
\begin{array} { r } { \begin{array} { r } { E _ { 0 } = E _ { O C V } - I ( \mathrm { t } ) R _ { 0 } - U _ { 1 } } \\ { } \\ { C _ { 1 } d u _ { 1 } / d t + U _ { 1 } / R _ { 1 } = I ( t ) } \end{array} } \end{array}
$$

$\mathrm { U } _ { 1 }$ represents the open-circuit voltage throughout the RC network, and SOC can be calculated by the AH integration.

$$
S O C ( t ) = S O C ( 0 ) - \int _ { 0 } ^ { t } \eta I ( \tau ) \biggl / Q _ { N } d \tau
$$

SOC(O) indicates the starting SOC, $Q _ { \mathrm { N } }$ represents the nominal capacity of the ICRFB,and $\boldsymbol { \mathsf { \Pi } } \boldsymbol { \mathsf { \Pi } }$ represents the coulomb efficiency,as detailed in Eq. (5).

$$
\eta = \left\{ \begin{array} { l l } { 1 - E _ { O C V } / R _ { s h u n t } I ( t ) } & { I ( t ) \ne 0 } \\ { 1 } & { I ( t ) = 0 } \end{array} \right.
$$

The self-discharge loss $\mathrm { R } _ { \mathrm { s h u n t } }$ due to tube and electrolyte flow can be expressed by Eq. $( 7 )$

$$
R _ { s h u n t } = \sum l \Big / \sigma S = E _ { \theta } \Delta t \Big / Q _ { N }
$$

where $\sigma$ denotes the conductivity of the electrolyte consisting of a mixture of Fe/Cr ions,S represents the effective area of the carbon felt in contact with the membrane,and l denotes the effective length of the tube,△t is the self-discharge time and $Q _ { \mathrm { N } }$ is the discharge capacity [21,23,34].

# 2.2.Parameter identification

The modeled parameters $\mathrm { R } _ { 0 } , \mathrm { R } _ { 1 }$ ,and $\mathrm { C _ { 1 } }$ require identification and are influenced by various factors such as temperature,current,and electrolyte flowrate.In this paper,the IAFFRLS algorithmis employed for online parameter identification. This approach incorporates a forgeting factor to reduce the weight of historical data,ensuring the accuracy of the model.For parameter identification using the RLS algorithm, the first-order RC ECM must be transformed into a least-squares structural form.

During the transformation of the regression form in Table 1, $\mathbf { E } _ { \mathrm { { L } } } = \mathbf { E } _ { 0 } ,$ $\operatorname { E o c V } , \mathbf { z }$ is the discretisation operator and $\mathrm { T } _ { s }$ denotes the sampling interval. $\phi _ { k } = \Big [ - E _ { L , k - 1 } I _ { k } I _ { k - 1 } \Big ]$ ， $\theta _ { k } = \left[ \begin{array} { l l l } { \theta _ { 1 , k } } & { \theta _ { 2 , k } } & { \theta _ { 3 , k } } \end{array} \right] ^ { T }$ ，representing the matrices of coefficients and parameters that are to be identified, separately.When solving the regression using RLS to obtain $\Theta _ { \mathrm { i } s }$ use Eq. 8 to calculate the parameters to be identified [35].

$$
\left\{ \begin{array} { l } { R _ { 0 } = ( \theta _ { 3 } - \theta _ { 2 } ) / ( 1 - \theta _ { 1 } ) } \\ { R _ { 1 } = 2 ( \theta _ { 1 } \theta _ { 2 } - \theta _ { 3 } ) / \big ( 1 - \theta _ { 1 } ^ { 2 } \big ) } \\ { C _ { 1 } = T _ { s } ( 1 - \theta _ { 1 } ) ^ { 2 } \Big / 4 ( \theta _ { 1 } \theta _ { 2 } - \theta _ { 3 } ) } \end{array} \right.
$$

where:

$$
\left[ \begin{array} { c } { \theta _ { 1 } } \\ { \theta _ { 2 } } \\ { \theta _ { 3 } } \end{array} \right] = \left[ \begin{array} { c } { ( T _ { s } - 2 R _ { 1 } C _ { 1 } ) / ( T _ { s } + 2 R _ { 1 } C _ { 1 } ) } \\ { - ( T _ { s } R _ { 1 } + 2 R _ { 1 } C _ { 1 } R _ { 0 } + T _ { s } R _ { 0 } ) / ( T _ { s } + 2 R _ { 1 } C _ { 1 } ) } \\ { - ( T _ { s } R _ { 1 } - 2 R _ { 1 } C _ { 1 } R _ { 0 } + T _ { s } R _ { 0 } ) / ( T _ { s } + 2 R _ { 1 } C _ { 1 } ) } \end{array} \right]
$$

The basic idea of RLS is to transform the system model, converting the parameters of the system matrix, input matrix into state variables, finding the optimum parameters through the minimization of the aggregate of squared errors.The general FFRLS steps are shown in Table 2.

Where $\theta _ { \mathbf { k } - 1 }$ is the estimated value of the parameter at the previous moment, $\operatorname { E } _ { \mathrm { L } , \mathrm { k } }$ is the measured value at the current moment. $\phi _ { k } \theta _ { k - 1 }$ is the prediction of moment $\mathbf { k }$ based on measurement, $\varepsilon _ { k } \mathrm { i } s$ the prediction error, also known as innovation,and the corrected gain matrix is $\mathrm { K } _ { \mathrm { k \cdot } }$ The optimal estimate of the parameter at this point is obtained by multiplying the previous estimate plus the corrected gain matrix by innovation.The initial values $\mathrm { { P _ { 0 } } }$ and $\theta _ { 0 }$ need to be determined during the recursive calculations in order to derive the $\mathrm { K } _ { \mathrm { k + 1 } }$ gain matrix. $\theta _ { 0 }$ is theoretically preferred to be as small a parameter as possible and is usually chosen to be 0. $\mathrm { P } _ { 0 } = \alpha \mathrm { E }$ ，where $\alpha$ denotes a positive rational number,E denotes the identity matrix.

Based on the variable forgetting factor strategy,Lao et al. proposed an AFFRLS algorithm that adjusts the value of $\lambda$ according to the change in error magnitude.The $\lambda$ update expression is given in Eq.(10):

Table 3 UKF algorithm process.   

<table><tr><td>Initialize:</td><td>X0=E[xo]P=E[(x-x)(x-x0）]</td></tr><tr><td>Update of priori state:</td><td>x/-=f</td></tr><tr><td>Update of priori error covariance:</td><td>Pxk/k-1=∑²[x/k-1-</td></tr><tr><td></td><td>Xx/k-1][x/k-1-k/k-1]+Qk</td></tr><tr><td>Calculation of observations:</td><td>yk-1=h(x/1u）/-1=∑/</td></tr><tr><td>Update of covariance:</td><td>Pyx=∑[/k-1-yk/k-1][y/k-1-yk/k-1]+ Rk</td></tr><tr><td>Update of Kalman gain:</td><td>Pxyk=∑/-][/</td></tr><tr><td>Update of posteriori state:</td><td>Kk=Pxy,k/Pyk</td></tr><tr><td>Update of posteriori error</td><td>Xk/k=Xk/k-1+K(yx-yk/k-1)</td></tr><tr><td>covariance:</td><td>Px,k/k=Pxk/k-1-KkPy,kK</td></tr></table>

$$
\left\{ \begin{array} { l l } { \lambda ( k ) = \lambda _ { \operatorname* { m i n } } + ( 1 - \lambda _ { \operatorname* { m i n } } ) { \mathrm { \Omega } } ^ { \alpha ( k ) } } \\ { \alpha ( k ) = 2 ^ { \rho e ^ { 2 } ( k ) } } \end{array} \right.
$$

where $\rho$ is the coeficient to be determined, $\rho { \in } [ 1 0 ^ { 4 } , 5 \times 1 0 ^ { 4 } ] ; \lambda _ { \mathrm { m i n } }$ is the minimum allowed $\lambda$ value.The rate at which $\lambda$ tends to minimize is affected by the magnitude of $\rho _ { : }$ ，which is more demanding in terms of coefficient values.All subsequent references to AFFRLS in this paper are to the method used by Lao et al. [36]

In the IAFFRLS algorithm proposed in this paper,influenced by errors,the forgetting factor gradually adjusts to an appropriate value, thus enabling online parameter identification to quickly track the true value. The experimental results show that the process by which the forgeting factor converges to its optimal value demonstrates a nonlinear relationship with the prediction error of the terminal voltage [37].To describe this nonlinear relationship,this paper considers the equation of the exponential function curve with the natural constant e as the base, and the $\lambda$ update expression is given in Eq.(11):

$$
\begin{array} { r } { \lambda ( k ) = \left\{ \begin{array} { l l } { \lambda _ { \operatorname* { m a x } } } & { | e ( k ) | \leq 1 0 ^ { - 5 } } \\ { \lambda _ { \operatorname* { m i n } } + ( \lambda _ { \operatorname* { m a x } } - \lambda _ { \operatorname* { m i n } } ) \cdot e x p \Big ( - ( e ( k ) / e _ { \operatorname* { m a x } } ) ^ { 2 } \Big ) } & { 1 0 ^ { - 5 } < | e ( k ) | \leq 1 0 ^ { - 2 } } \\ { \lambda _ { \operatorname* { m i n } } } & { 1 0 ^ { - 2 } \leq | e ( k ) | } \end{array} \right. } \end{array}
$$

In Eq. (11),the forgetting factor is restricted to an upper limit of $\lambda _ { \operatorname* { m a x } }$ $= 0 . 9 9 5$ and a lower limit of $\lambda _ { \operatorname* { m i n } } = 0 . 9$ $\mathbf { e _ { \mathrm { m a x } } }$ is the maximum error allowed.By adjusting the coefficients in the exponential term,the trend and magnitude of the change of the forgetting factor can be flexibly controlled.The update of $\lambda$ in Eq.(lO) is primarily governed by the square of the error. This method may cause the forgetting factor to change too quickly or too slowly in some cases,particularly when the error is small，potentially leading to overshooting or inadequate parameter updates.The approach proposed in this paper defines a specific error range and imposes constraints on $\lambda$ ,allowing for more precise control over the adjustment of the forgetting factor,thereby effectively preventing overshooting. The optimal value of $\lambda ( \mathbf { k } )$ is found using the exponential function curve equation when the error value $\vert \mathbf { e } ( \mathbf { k } ) \vert \in ( 1 0 ^ { - 5 }$ ， $1 0 ^ { - 2 } ]$ . For error values of $| \mathrm { e } ( \mathbf { k } ) | \mathrm { e } ( 0 , 1 0 ^ { - 5 } ]$ ， $\lambda ( \mathbf { k } ) = \lambda _ { \operatorname* { m a x } } ,$ and for values of $\vert \mathrm { e } ( \mathrm { k } ) \vert { > } 0 . 0 1$ ， $\lambda ( \mathbf { k } ) = \lambda _ { \operatorname* { m i n } }$ The maximum allowable error is set according to the estimation requirements.According to Eq. (10), $\lambda ( \mathbf { k } )$ is calculated using the error value $\boldsymbol { \mathrm { e } } ( \mathbf { k } )$ .For large e(k),λis likely to decrease rapidly toward $\lambda _ { \mathrm { m i n } } ,$ whereas for small $\boldsymbol { \mathrm { e } } ( \mathbf { k } )$ ,it is expected to increase swiftly toward $\lambda _ { \operatorname* { m a x } }$

# 3. Joint SOC and capacity estimation

SOC represents the battery's remaining charge,determined by the different valence states of iron and chromium ions in the liquid storage tank, defined as Eq. $( 5 )$ ,and it cannot be measured directly during operation. Therefore,for effective battery SOC estimation,the design of a state estimator is required.To apply the AUKF algorithm for SOC estimation, the state space equations for the lumped parameter battery model need to be established.The nonlinear state-space model of the ICRFB is represented by Eq. (12).

$$
\left\{ \begin{array} { c c } { y _ { k } = E _ { O C V , k } - I _ { k } R _ { 0 } - U _ { 1 , k } + \nu _ { k } } & { w _ { k } \sim ( 0 , Q _ { k } ) } \\ { x _ { k + 1 } = A x _ { k } + B u _ { k } + \omega _ { k } } & { \nu _ { k } \sim ( 0 , R _ { k } ) } \end{array} \right.
$$

where A, C is the system matrix:

$$
A = \left[ \begin{array} { c c } { 1 } & { - \eta I _ { k } T _ { s } } \\ { 0 } & { 1 } \end{array} \right] \mathbf { C } = [ d E _ { O C V } / d s o c d E _ { O C V } / d ( 1 / Q ) ]
$$

where $\pmb { x } = \left[ S O C \quad 1 / Q \right] ^ { T }$ signifies the status vector,while I and $\mathtt { E } _ { 0 }$ are the system inputs and measured voltages,respectively. Compared to SOC and polarization voltage,the process of capacity loss is much slower and the capacity can be considered constant over shorter sampling intervals.

This paper employs AUKF to estimate the battery's SOC and capacity. This method linearizes the nonlinear system based on the classic statistical technique of unscented transformation (UT),thereby avoiding the calculation of Jacobian matrix during the model linearization process.Furthermore,an adaptive covariance matching method is introduced in the AUKF,which enables real-time updates of process and measurement covariances,thus improving estimation accuracy.The process of the UT is described as follows:

1)Obtain $( 2 \mathsf { n } + 1 )$ sigma points through the UT transformation.

$$
\left\{ \begin{array} { l l } { x _ { 0 } = \widehat { x } } \\ { x _ { k - 1 } = \widehat { x } + \left( \sqrt { ( n + \lambda ) P _ { k - 1 } } \right) _ { i } , i = 1 , 2 , 3 . . . , n } \\ { x _ { k - 1 } = \widehat { x } - \left( \sqrt { ( n + \lambda ) P _ { k - 1 } } \right) _ { i - n } , i = n + 1 , n + 2 , . . . , 2 n } \end{array} \right.
$$

where n denotes the number of state dimensions, $\lambda = \alpha ^ { 2 } ( n + k ) - n$ denotes the scale scaling parameter.For the covariance matrix to be positive semidefinite,k,which denotes another scale factor, should satisfy $\mathbf { k }$ $\geq 0$ ,usually taken to be O or $_ { 3 - \mathrm { n } }$ ，The parameter $\alpha \in \left[ 0 , 1 \right]$ defines the sigma point distribution,ideally a smaller value.

2)The weights of the sampling points:

$$
\left\{ \begin{array} { l l } { \omega _ { m } ^ { 0 } = \lambda / ( n + \lambda ) } \\ { \omega _ { c } ^ { 0 } = \lambda / ( n + \lambda ) + \left( 1 - \alpha ^ { 2 } + \beta \right) } \\ { \omega _ { m } ^ { i } = \omega _ { c } ^ { i } = \lambda / 2 ( n + \lambda ) , i = 1 , 2 , 3 , . . . 2 n } \end{array} \right.
$$

where $\omega _ { m } ^ { 0 }$ ， $\omega _ { m } ^ { i }$ represents the mean weight of the sampling point and $\omega _ { c } ^ { 0 }$ ， $\omega _ { c } ^ { i }$ represents the covariance weight. $\beta$ represents a non-negative weight coefficient,usually taking a value of 2.completing the estimation of the system after the UT transformation, The specific steps of UKF are shown in Table 3, $\overline { { x } } _ { 0 }$ denotes the initial mean,and $\mathrm { { P _ { 0 } } }$ denotes the initial covariance [38].

During SOC estimation,nonlinear noise is invariably present,and its statistical characteristics are usually unknown,which causes the possibility of divergence in the KF and UKF during filtering process.The UKF is less adaptive in responding to divergent scenarios,leading to deviations between estimated and actual values.To address this problem, this paper employs the AUKF algorithm to estimate both the SOC and capacity of the ICRFB.The algorithm incorporates an adaptive mechanism based on the UKF,enabling continuous estimation of the process and measurement noise covariance matrices, thereby further improving estimation accuracy.

The key to the AUKF is the introduction of a time-varying noise estimator by which the process noise covariance $\mathrm { Q _ { k } }$ and the measurement noise covariance $\mathrm { R } _ { \mathrm { k } }$ are calculated. The update of $\mathbf { Q } _ { \mathrm { k } }$ and $\mathrm { R _ { k } }$ is described by Eq. (16):

![](images/12a4f1c75b64d4c4d4720a90af664956e385d20805b31ce73841ef2f3af6d9b8.jpg)  
Fig.2.Schematic diagram of the battery test platform.

![](images/60140a6ecc77577aff64208b0ae29d2e37106853fe72631e7a98d5f1cb019aa9.jpg)  
Fig.3.(a) Self-discharge curve. (b) OCV-SOC fiting curve.

$$
\left\{ \begin{array} { l } { \displaystyle Q _ { k } = K _ { k } H _ { e _ { k } } \left( K _ { k } \right) ^ { T } } \\ { \displaystyle R _ { k } = H _ { e _ { k } } + \sum _ { i = 0 } ^ { 2 n } \omega _ { c } ^ { i } \left[ y _ { k / k - 1 } ^ { i } - \widehat { y } _ { k / k - 1 } \right] \left[ y _ { k / k - 1 } ^ { i } - \widehat { y } _ { k / k - 1 } \right] ^ { T } } \end{array} \right.
$$

$H _ { e _ { k } }$ defined as:

$$
H _ { e _ { k } } = \left\{ \begin{array} { c } { ( ( k - 1 ) / k ) H _ { e _ { k } } + k ^ { - 1 } e _ { k } e _ { k } ^ { T } } \\ { W ^ { - 1 } \sum _ { i = k - w + 1 } ^ { k } e _ { i } e _ { i } ^ { T } } \end{array} \right. k \leq W
$$

the voltage innovation of the system at time $\mathbf { k }$ ， $H _ { e _ { k } }$ indicates the innovation covariance at step $\mathbf { k } ,$ and $\mathsf { W }$ indicates the length of the moving window for covariance matching.

# 4. Detailed experimental procedure

For the purpose of analyzing and validating the precision and effectiveness of the proposed SOC and capacity estimation methods, different filtering algorithms are employed for numerical validation using constant current charge and discharge conditions,as well as mixed power pulse conditions,serving as loading conditions,respectively,and the experimental results are subsequently analyzed and compared.

# 4.1．Experimental platform

The battery test platform mainly comprises a battery tester,a thermostat box and a computer for saving experimental data.The Wuhan Lanhe CTK3oo2K test system can realize a variety of charging and discharging modes such as constant current,constant voltage,multiplication,pulse,custom working conditions,etc.In addition,it can also carry out real-time monitoring of battery voltage,current and temperature. Shaoxing Shangcheng Instruments 1O1-OoBS electric constant temperature drying oven is responsible for ICRFB single cell to provide a constant temperature and stable working environment, in order to make the ICRFB performance reach the optimum,as well as to alleviate the aging of chromium ions, the working temperature is set at $6 5 ~ ^ { \circ } \mathrm { C }$ ,but higher temperatures can exacerbate ionic crossover and hydrogen evolution problems [39].The Shanghai Kamoer DIPump55O adjustable speed stepper motor peristaltic pump circulates the electrolyte ata flow rate of $1 0 0 ~ \mathrm { { m L / m i n } }$ .In this study, $5 c m \times 5 c m$ ICRFB single cells separated by DuPont Nafion 212 membrane from USA are used.The ICRFB single cell is connected to the reservoirs via two peristaltic pumps and BPT tube, and each reservoir contained ${ \bf 8 0 m l }$ of mixed electrolyte prepared from

![](images/dbc34a9d57b28484b94e34d6c82c485aea983ef7acf6aaca8a2ddb5ad905cbb7.jpg)  
Fig.4.(a) Load current from DST1; (b) terminal voltage curves.

![](images/e1f1a86469c99b4c5aaefa3a4bb9c58e763919b924507746c0cac4d4948cb901.jpg)  
Fig.5.Comparison results of modeled and actual voltages and zoom-in comparison at 5430 s.

![](images/bec9683df07b9a0488cec7584d459f7873a29b2ac91ec7bfa1b97a773ecb2134.jpg)  
Fig.6.Comparison of voltage errors at the outputs of FFRLS,AFFRLS and IAFFRLS.

Table 4 Parameter identification performance evaluation table.   

<table><tr><td></td><td>RMSE(%)</td><td>MAE</td><td>Maximum error</td></tr><tr><td>FFRLS</td><td>0.0421</td><td>2.6016*10-4</td><td>5.2 mV</td></tr><tr><td>AFFRLS</td><td>0.0487</td><td>2.5478*10-4</td><td>4.8 mV</td></tr><tr><td>IAFFRLS</td><td>0.0352</td><td>2.2519*10-4</td><td>3.4 mV</td></tr></table>

![](images/d2b78debe98bff220860e05991e1144d51311dd01482f199c060b1285f31470c.jpg)  
Fig.7.Online identification of first-order ECM parameter results: (a) $\operatorname { R } _ { 0 } ;$ (b) $\operatorname { R } _ { 1 } ;$ (c) $\mathrm { C _ { 1 } }$ (d) Variation curve of forgetting factor during IAFFRLS identification o. parameters (updated forgetting factor at 6888 s is 0.953179).

3 M/L HCL and $1 \ M / \mathrm { L }$ of $\mathrm { F e C L } ^ { 2 }$ and $\mathrm { C r C L } ^ { 3 }$ ,respectively. Constant flow circulation of the electrolytes is achieved by rotating the squeeze tube with a stepper motor.The connections of the battery test platform are shown in Fig. 2.

# 4.2. Battery testing process

Constant current charge/discharge test and mixed pulse discharge test were performed with a sampling interval of 1 s. The experiment was conducted within a voltage range of $0 . 8 – 1 . 2 \mathrm { V }$ [6,40],and the ambient temperature of the experiment was $6 5 ~ ^ { \circ } \mathrm { C }$ created by the thermostat. During testing，the battery test system collects and records data, including voltage,current, actual SOC and capacity at each sampling point,while accurately controlling the charging and discharging process.The data collected from these experiments served as a reference for comparing the outcomes resulting from the presented method.It is assumed that the battery capacity remains constant for each cycle,and take the final capacity displayed on the battery tester at the conclusion of each cycle considered as the effective battery capacity for that cycle.

To calculate $\mathrm { R } _ { \mathrm { s h u n t } } ,$ the ICRFB was fully charged in constant current constant voltage (CC-CV) mode and subsequently rested until the SOC was $0 ~ \%$ ,and record the discharge time and capacity,therefore,it is possible to calculate $\mathrm { R } _ { \mathrm { s h u n t } }$ through Eq.7 [21].Subsequently,charge and discharge cycling tests were conducted to fit the non-linear functions of SOC and OCV.Firstly,ICRFB is charged in CC-CV mode.Specifically, the battery is charged to an upper limit voltage of $_ { 1 . 2 \mathrm { V } }$ at a current density of $8 0 \mathrm { \ m A } / \mathrm { c m } ^ { 2 }$ and then charged at $_ { 1 . 2 \mathrm { V } }$ until the cut-off current drops to $2 0 0 ~ \mathrm { { m A } }$ Discharge to $_ { 0 . 8 \mathrm { ~ V ~ } }$ at a discharge current density of $8 0 \mathrm { m A } /$ $\mathrm { c m } ^ { 2 }$ [25].Fig. 3(a) illustrates the self-discharge curve of the ICRFB, using the self-discharge time $\Delta \mathbf { t }$ ,the values of $\mathrm { R } _ { \mathrm { s h u n t } }$ and coulombic efficiency can be calculated from Eqs.6 and 7, the reference SOC is obtained through AH integration of compensating for the coulombic efficiency.The OCV-SOC function curve is plotted using the averaged charge and discharge data, shown in Fig.3(b). The function is represented by a 6th-order polynomial,as given in Eq.18.

$$
\begin{array} { c } { { O C V = 1 . 2 7 4 4 \cdot S O C ^ { 6 } - 2 . 9 7 3 3 \cdot S O C ^ { 5 } + 2 . 3 8 3 4 \cdot S O C ^ { 4 } } } \\ { { - 0 . 4 6 2 2 \cdot S O C ^ { 3 } - 0 . 3 3 2 \cdot S O C ^ { 2 } + 0 . 3 7 \cdot S O C + 0 . 8 5 6 7 } } \end{array}
$$

In an effort to test the performance of the model and IAFFRLS-AUKF algorithm under complex operating conditions,online estimation of SOC and capacity is performed in conjunction with DST operating conditions. According to the Technical Conditions of Battery Management System for Electric Vehicles,the battery is tested and the sampling frequency of the test system is $_ { 1 \textrm { H z } }$ .The specific experimental steps for the DST process are as follows: 1)Use CC-CV mode to fully charge the battery,then leave it for1 h; 2)Load DST pulse current; 3)Cycle the DST operating current until the terminal voltage is ${ < } 0 . 8 \mathrm { ~ V } .$ ，Fig.4 illustrates the load current and terminal voltage obtained from the DST,i.e.DST1. Upon completion of the testing,data such as experimental currents and voltages are used in the introduced method to assess the fidelity of the modeling.

# 5．Verification and discussion

This paper compares different parameter identification methods and

![](images/88d70b143de579546840e25697c25fafe1905c819396058fbbf3bf35108cdea8.jpg)  
Fig8sedeUU AUKF:(c)OCs; tion parameters.

Table 5 SOC estimation performance evaluation.   

<table><tr><td></td><td>RMSE(%)</td><td>MAE</td><td>Error_max(%)</td></tr><tr><td>IAFFRLS-EKF</td><td>2.4181</td><td>0.0105</td><td>1.47</td></tr><tr><td>IAFFRLS-UKF</td><td>2.3988</td><td>0.0102</td><td>1.89</td></tr><tr><td>IAFFRLS-AUKF</td><td>0.9133</td><td>0.0041</td><td>0.6</td></tr><tr><td>FFRLS-AUKF</td><td>2.7235</td><td>0.0179</td><td>2.04</td></tr><tr><td>AFFRLS-AUKF</td><td>2.4470</td><td>0.0092</td><td>2.56</td></tr></table>

SOC estimators.Based on this analysis,an IAFFRLS-AUKF identification and estimation method is proposed.

# 5.1. Model identification accuracy

The prerequisite for accurately estimating the SOC and capacity of an ICRFB is to obtain precise ECM parameters.The identification error of the parameters is represented by the difference between the experimental terminal voltage and the output voltage.To compare the convergence of the IAFFRLS algorithm, $\lambda = 0 . 9 7 5$ FFRLS and AFFRLS algorithms are included for comparison.The results of the terminal voltage identification for all three algorithms are shown in Fig.5.

All three RLS identification results exhibit good convergence when comparing the model's terminal voltage output from different algorithms with the experimental terminal voltage curves.However,at the sharp peak of current switching,all three algorithms show a significant deviation from the actual voltage. But the IAFFRLS algorithm is closer to the actual voltage,indicating that the IAFFRLS algorithm provides better convergence than both the FFRLS and AFFRLS algorithms.

As shown in Fig.6, the terminal voltage output by the IAFFRLS algorithm exhibits less oscillation around O compared to both the FFRLS and AFFRLS algorithms.This result arises from IAFFRLS algorithm realizing optimal outcomes based on the reduction of the prediction error in conjunction with the forgetting factor by using the prediction error of the voltage as a variable.The maximum voltage prediction error for the IAFFRLS algorithm is $3 . 4 \mathrm { m V }$ ,which is smaller than the $4 . 8 \mathrm { m V }$ and $5 . 2 ~ \mathrm { m V }$ errors of the AFFRLS and FFRLS algorithms.The results indicate that the IAFFRLS algorithm effectively reduces the prediction voltage error.In order to illustrate more clearly,the superiority of the IAFFRLS algorithm over the AFFRLS and the FFRLS algorithm,the convergence performance of the three algorithms was evaluated in terms of the mean absolute error(MAE)and the root-mean-square error (RMSE) in the DST1 operating condition.

Table 4 calculates the performance metrics for each algorithm separately:MAE and RMSE.MAE calculates the average of absolute errors but is less effective at emphasizing larger errors.In contrast, RMSE highlights the impact of larger errors by squaring the prediction errors before calculating their square root.A smaller RMSE value indicates better estimation performance of the algorithm under the same conditions [41].By comparing the different performance indexes of IAFFRLS algorithm with FFRLS and AFFRLS algorithms,it can be seen that IAFFRLS is superior to FFRLS and AFFRLS algorithms in terms of

![](images/0c4d9520fb696181138b2ed61af766794aeaf32dd7666e8e9fb627f604200871.jpg)  
Fig.9sedo; BasednAFais;aao IAFFRLS identification parameters.

Table 6 capacity estimation performance evaluation.   

<table><tr><td></td><td>RMSE(%)</td><td>MAE</td></tr><tr><td>IAFFRLS-EKF</td><td>11.27</td><td>59.7915</td></tr><tr><td>IAFFRLS-UKF</td><td>12.51</td><td>68.5798</td></tr><tr><td>IAFFRLS-AUKF</td><td>6.65</td><td>24.9306</td></tr><tr><td>FFRLS-AUKF</td><td>10.65</td><td>54.0522</td></tr><tr><td>AFFRLS-AUKF</td><td>10.48</td><td>47.4124</td></tr></table>

identifying convergence.

The parameter identification results are shown in Fig.7.Where the reference values of the model parameters are determined offline through the following process:

$\mathrm { U } _ { \mathrm { O C V } }$ is computed using Eq. (18),and $\mathtt { R } _ { 0 }$ is determined from the instantaneous voltage change resulting from the step change in current.

$$
R _ { 0 } = \Delta E / \Delta I
$$

Once $\mathrm { U } _ { \mathrm { O C V } }$ and $\mathrm { R } _ { 0 }$ are obtained, $\mathrm { U } _ { 1 }$ is determined using Eq. (3), and ${ \mathrm { R } } _ { 1 }$ and $\mathrm { C _ { 1 } }$ are subsequently extracted by solving Eq. (20).

$$
U _ { 1 } ( k ) = \lceil U _ { 1 } ( k - 1 ) \quad I ( K - 1 ) \ \rfloor { \cdot } \varphi ( k )
$$

where $\varphi ( k ) = \left[ e ^ { - T _ { s } / ( R _ { 1 } C _ { 1 } ) } \quad \left( 1 - e ^ { - T _ { s } / ( R _ { 1 } C _ { 1 } ) } \right) R _ { 1 } \right] ^ { T } [ 2 6 ] .$

Under DST1 operating conditions, the reference value of ${ \mathrm { R } } _ { 0 }$ is $2 0 \mathrm { m } \Omega$ the polarization resistance ${ \bf R } _ { 1 }$ ranges from 5 to $1 0 ~ \mathrm { m } \Omega$ ,and the polarization capacitance $\mathrm { C _ { 1 } }$ ranges from 500 to 1500 F.Fig.7(a-c)

demonstrates that the parameters identified by the IAFFRLS algorithm can track the reference ECM parameters in real-time.In Fig.7(d),λ varies with load current but remains within the range of 0.9 to 0.995, which indicates that under dynamic operation conditions,λ can be adaptively updated based on the voltage error value,achieving fast convergence to suitable values and reducing the terminal voltage prediction error.

# 5.2. SOC, capacity estimation accuracy

To verify the efficacy of the IAFFRLS-AUKF method under experimental conditions,the parameters identified by different RLS methods under DST operating conditions were tested for joint SOC and capacity estimation.

The results of SOC estimation are shown in Fig.8,which presents a comparison of the reference value and the estimated value.The reference SOC is taken from the AH integration method with coulombic efficiency. Initially,the estimation error is significant due to the inaccuracy in the state vector and initial values as well as the absence of historical accumulated data.After the first cycle of DST1,the error is mitigated by the Kalman gain,enabling the estimated curve quickly tracks the reference SOC value.

Fig.8(b) compares the SOC estimation errors of three algorithms using the same model parameters.Although all algorithms start with the same initial value,only AUKF is able to track the true value with minimal error.To clearly demonstrate the impact of model errors on SOC estimation, SOC estimation was performed using AUKF with different model parameters,as shown in Fig.8(d).Although the algorithm eventually converges,model errors result ina larger error in the final SOC estimation.Where the performance evaluation of SOC estimates, derived from data subsequent to the first cycle of DST1,is demonstrated in Table 5.The SOC error of the IAFFRLS-AUKF remains stable within 1 $\%$ ,and in comparison,AUKF effectively controls the maximum deviation.The maximum error of the SOC estimate based on IAFFRLS is below $2 \%$ ,demonstrating that the accuracy of the model is the basis for to ensuring the high accuracy of the estimator.

![](images/f420f244c593df2e75c3779b318140ba98a915f74df288e30ab19681398c1a5a.jpg)  
Fig.10.(a) Discharge capacity and coulombic eficiency. (b) Electrolyte after 80 cycles.

![](images/2521e153ae27496b9d7514237c02941908e8a30a8663e54a56329c917c073edf.jpg)  
Fig.11.Modeling results applied to DST2: (a) terminal voltage. (b) terminal voltage error.

Table 7 Parameter identification performance evaluation after multiple cycles.   

<table><tr><td></td><td>RMSE(%)</td><td>MAE</td><td>Maximum error</td></tr><tr><td>FFRLS</td><td>0.2636</td><td>1.2*10-3</td><td>19.96mv</td></tr><tr><td>AFFRLS</td><td>0.2455</td><td>1.1*10-3</td><td>17.55mv</td></tr><tr><td>IAFFRLS</td><td>0.0483</td><td>3.041*10-4</td><td>4.92mv</td></tr></table>

During the charge/discharge process,capacity degradation occurs at a very slow rate.Therefore,the capacity can be considered constant over a brief sampling interval. The single reservoir $8 0 ~ \mathrm { m l }$ ICRFB discharged $1 1 9 2 . 4 \mathrm { \ m A h }$ in this DST1,consequently,the reference capacity was $1 1 9 2 . 4 ~ \mathrm { m A h }$ ，Fig.9 illustrates the estimation results of the algorithms with the initial values set at $1 0 0 0 \ \mathrm { m A h }$ .From Figs.9(a) and (b),it is evident that the EKFalgorithmis characterizedbyits stability.Although it can gradually approach the true value,its convergence speed is slow, which may lead to insufficient real-time performance in rapidly changing battery states.While this slow convergence prevents overshooting,it may also result in the omission of important dynamic information in practice,leading to untimely responses.In contrast, while the UKF algorithm provides a faster approximation speed,its overshoot phenomenon is more pronounced while it responds quickly.This overshoot may not only temporarily overestimate the capacity estimation, thereby afecting the accuracy of the assessment, but also result in system instability.Moreover,the AUKF algorithm represents significant improvements on the basis of these two.It not only rapidly converges to the true value,demonstrating excellent fast response,but also effectively stabilizes after a short overshoot and continues to slowly approach the true value. This dual characteristic of rapid convergence and stability renders the AUKF more flexible and reliable in dynamic environments. The AUKF possesses a superior capability to handle nonlinear dynamics, maintaining high accuracy under complex charge and discharge conditions while reducing the risk of instability caused by overshoot.From Figs.9(c) and (d),model parameter errors also affect the convergence accuracy of capacity estimation.Although the estimator converges quickly,the final estimation error remains substantial.

Although the EKF algorithm can provide relatively stable capacity estimation in certain scenarios,its convergence speed is comparatively slow.The UKF,despite its superior responsiveness compared to the EKF and its capacity to promptly react to state changes,its over-sensitive nature allows for significant overshooting during the estimation process,which further increases the error performance,resulting in larger RMSEs and MAEs compared to those estimated by the EKF.The fast convergence and low error of the AUKF indicate that it can more efficiently track the dynamics of the SOC more efficiently and mitigate estimation errors stemming from system overreaction,and its RMSE and MAE are significantly lower than those of the EKF and the UKF.The RMSE of the capacity estimate based on the FFRLS and AFFRLS model parameters is also small,attributable to the fast convergence of the AUKF. (See Table 6.)

![](images/35c804099ee8b1d930084e91487f2881b3a9068f7164773586afea04f8e9ed35.jpg)  
FigOa:( SOCstmatiaciadaiaee estimation; (f) SOC estimation error; (g) capacity estimation; (h) capacity estimation error.

# 5.3.5.3 Performance after multiple cycles

To verify the estimated performance after long-term operation,the ICRFB underwent 80 charge-discharge cycles.As shown in Fig.10(a), the coulombic effciency of the ICRFB remained above $9 8 \%$ .However, after 80 cycles,the capacity decreased from $1 5 3 8 \mathrm { m A h }$ to 662 mAh.This degradation is attributed to electrolyte crossover,hydrogen evolution during operation,and electrolyte imbalance [6].As shown in Fig.10(b), the electrolyte in the negative electrode storage bottle is slightly more than that in the positive electrode storage bottle [42].

A second DST experiment (DST2) was conducted to assess further the robustness of the proposed method and its ability to track the capacity degradation of the ICRFB.As depicted in Fig.11(b),IAFFRLS can still accurately identify the model parameters,with an identification accuracy comparable to that observed before multiple cycles, demonstrating its ability to adapt to the aging of the ICRFB.The identification results for FFRLS and AFFRLS exhibit significantly larger errors,increasing by two to three times compared to those observed before multiple cycles.

Table 7 presents the evaluation metrics for the parameter identification performance.The maximum terminal voltage error predicted by IAFFRLS does not exceed $5 ~ \mathrm { m V }$ ，compared to $3 . 4 ~ \mathrm { m V }$ before multiple cycles,indicating minimal degradation in its identification accuracy. The maximum terminal voltage errors for the FFRLS and AFFRLS models are $1 9 . 9 6 ~ \mathrm { m V }$ and $1 7 . 5 5 ~ \mathrm { m V }$ ,respectively,with similar RMSE values, indicating comparable accuracy in identifying the ICRFB model parameters.Therefore,the λupdating method of AFFRLS may be unsuitable for identifying the ECM parameters of the ICRFB.

The AUKF-based estimation results of the three-parameter identification methods are presented in Figs.l2(a-d). The discharge capacity of the DST2 test is $5 3 9 ~ \mathrm { m A h }$ .As shown in Figs.12(b) and (d),the SOC estimation error of IAFFRLS-AUKF remains consistently within $1 \ \%$ In contrast,due to the inability of FFRLS and AFFRLS to adapt to the aging of the ICRFB,the identified model exhibits larger errors,leading to a greater deviation between the estimated and actual values.Fig.12(e-h) presents the estimation results of the three KF algorithms under the model parameters identified by IAFFRLS.The UKF and EKF algorithms exhibit slow SOC estimation convergence rates and significant convergence errors,they also exhibit substantial convergence errors in capacity estimation after loss,and the EKF shows a relatively large overshoot during the early stages.Since AUKF can adaptively adjust the noise covariance,it effectively suppresses the accumulation of noise and errors,resulting in higher accuracy and better convergence.

![](images/d8fa7da7116cd3300a08d7a7bc5b8f5367b0eb68c005069980c2292ff5de3384.jpg)  
Fig. 12. (continued).

Table 8 SOC and capacity estimation performance evaluation for DST2.   

<table><tr><td></td><td colspan="3">SOC estimation</td><td colspan="2">capacity estimation</td></tr><tr><td></td><td>RMSE(%)</td><td>MAE</td><td>Error_max(%)</td><td>RMSE(%)</td><td>MAE</td></tr><tr><td>IAFFRLS-EKF</td><td>3.3737</td><td>0.0121</td><td>2.99</td><td>9.86</td><td>20.3801</td></tr><tr><td>IAFFRLS-UKF</td><td>3.8773</td><td>0.0141</td><td>3.38</td><td>14.41</td><td>77.7078</td></tr><tr><td>IAFFRLS-AUKF</td><td>1.0864</td><td>0.0024</td><td>0.92</td><td>8</td><td>9.6947</td></tr><tr><td>FFRLS-AUKF</td><td>3.9145</td><td>0.0149</td><td>3.81</td><td>17.61</td><td>48.0348</td></tr><tr><td>AFFRLS-AUKF</td><td>3.4662</td><td>0.0145</td><td>3.57</td><td>20.47</td><td>45.7179</td></tr></table>

Table 8 provides an evaluation of the performance of SOC and capacity estimation after capacity loss. The proposed method can adapt to the aging of the ICRFB,with the SOC estimation error maintained within $1 \ \%$ .However,although its capacity estimation converges to the true value with a small error,it requires suficient data support. Specifically, errors will occur in the real-time capacity update during the discharge process,but the updated value will eventually converge to the true value.

# 6.Conclusion

In this paper,a battery model incorporating self-discharge losses is developed to simulate the dynamics of ICRFB.A computational method for RLS parameter identification with higher identification accuracy is proposed,and a method that completely decouples parameter identification using this algorithm from state estimation with the UKF is adopted, thus effectively mitigating cross-talk.By employing a loworder joint SOC and battery capacity estimation strategy,the stability and efficiency of computations have been significantly enhanced.The experimental results indicate that IAFFRLS algorithm can identify timevarying model parameters online while maintaining high modeling accuracy.The AUKF algorithm enables real-time and accurate estimation of SOC and capacity. Even after multiple cycles,the proposed method remains capable of accurately estimating the SOC and capturing changes in capacity.By comparing and analysis with other methods,the method proposed in this paper demonstrates significant advantages in terms of estimation precision, convergence and robustness.

# CRediT authorship contribution statement

Yang Liu: Writing - original draft, Methodology.Weibin Jiang: Conceptualization. Qianqian Zeng: Writing-review & editing. Xi Liu: Investigation.Guanchen Liu: Resources. Xiaoyin Xie: Supervision, Funding acquisition. Sheng Wu: Project administration. Chongyang Xu: Conceptualization.

# Declaration of competing interest

There are no conflicts to declare.

# Acknowledgments

This work was supported by the National Key Research and Development Program of China No.2022YFB4200704 and Hubei Provincial

Key R&D Program Projects,NO.: 2023DJC187; Hubei Provincial Natural Science Foundation Project, NO.:2024AFDoo3;Fundamental Research Projects of Science & Technology Innovation and Development Plan in Yantai City (No.2022JCYJo43),and the Natural Science Foundation of Shandong Province (Grant No. ZR2022QB068).

# Data availability

No data was used for the research described in the article.

# References

[1] A. Cherp, V. Vinichenko,J. Tosun, J.A. Gordon, J. Jewell, National growth dynamics of wind and solar power compared to the growth required for global climate targets, Nat. Energy 6 (7) (2021) 742-754.   
[2] M.K.G. Deshmukh, M.Sameeroddin,D.Abdul,Sattar M. Abdul, Renewable energy in the 2lst century: a review, Materials Today: Proceedings.80 (2023) 1756-1759.   
[3] L. Liu, Y. Wang, Z. Wang, S. Li, J. Li, G.He, et al.,Potential contributions of wind and solar power to China's carbon neutrality, Resour. Conserv. Recycl. (2022) 180.   
[4] C. Sun, H. Zhang, Review of the development of first-generation redox flow batteres: Iron-chromium system, ChemSusChem 15 (1) (2022) e202101798.   
[5] E.Sänchez-Diez, E. Ventosa, M. Guarnieri, A. Trovo, C.Flox, R. Marcilla, et al., Redox flow batteries: status and perspective towards sustainable stationary energy storage,J. Power Sources 481 (2021) 228804.   
[6] Y.K. Zeng, T.S. Zhao,L. An, X.L. Zhou, L. Wei, A comparative study of all-vanadium and iron-chromium redox flow batteries for large-scale energy storage, J. Power Sources 300 (2015) 438-443.   
[7] E. Bai, C. Sun, H. Zhu, Z. Liu, C. Xu, X. Xie, et al., Amino-functionalized multi-walled carbon nanotube/SPEEK hybrid proton exchange membrane for iron-chromium redox flow battery, Batteries Supercaps 7 (6) (2024) e202400007.   
[8] N. Mans, D.van der Westhuizen, H.M. Krieg, The effect of bismuth on the performance of a single-celliron-chromium redox flow battery, Advanced Energy and Sustainability Research. n/a(n/a):2400113 (2024).   
[9] M. Wu, M. Nan, Y.Ye, M. Yang,L. Qiao,H. Zhang, et al.,A highly active electrolyte for high-capacity iron-chromium flow batteries, Appl. Energy.358 (2024) 122534.   
[10] A. Ashok, A. Kumar, A comprehensive review of metal-based redox flow batteries: progress and perspectives, Green Chem. Lett. Rev.17 (1) (2024) 2302834.   
[11] A. Bhattacharjee, H. Saha, Development of an efficient thermal management system for vanadium redox flow battery under different charge-discharge conditions, Appl. Energy 230 (2018) 1182-1192.   
[12] A. Bhattacharjee, H. Samanta, N. Banerjee, H. Saha, Development and validation of a real time flow control integrated MPPT charger for solar PV applications of vanadium redox flow battery, Energy Convers. Manag. 171 (2018) 1449-1462.   
[13] B. Khaki, P.Das, Multi-objective optimal charging current and flow management of vanadium redox flow batteries for fast charging and energy-efficient operation, J. Power Sources 506 (2021) 230199.   
[14] Y.Li, X. Zhang, J. Bao,M. Skyllas-Kazacos, Control of electrolyte flow rate for the vanadium redox flow battery by gain scheduling, Journal of Energy Storage. 14 (2017) 125-133.   
[15] M. Pugach, S. Parsegov, E. Gryazina,A. Bischi, Output feedback control of electrolyte flow rate for vanadium redox flow batteries, J. Power Sources 455 (2020) 227916.   
[16] H. Wang, S.A.Pourmousavi, W.L.Soong, X. Zhang,N. Ertugrul,Battery and energy management system for vanadium redox flow battery: a critical review and recommendations, Journal of Energy Storage. 58 (2023) 106384.   
[17] H. Pang, K. Chen, Y. Geng,L. Wu,F. Wang, J. Liu, Accurate capacity and remaining useful life prediction of lithium-ion batteries based on improved particle swarm optimization and particle filter, Energy 293 (2024) 130555.   
[18] H. Zhang, C. Sun, Iron-Chromium Flow Battery, Flow Batteries, 2023, pp. 741-763.   
[19] H. Zhang, C. Deng, Y. Zong, Q. Zuo, H. Guo, S. Song, et al., Effect of sample interval on the parameter identification results of RC equivalent circuit models of Li-ion battery: an investigation based on HPPC test data, Batteries 9 (2023) 1.   
[20] Q. Zheng, X.Li, Y. Cheng, G. Ning,F. Xing, H. Zhang, Development and perspective in vanadium flow battery modeling, Appl. Energy 132 (2014) 254-266.   
[21] B. Xiong, Y. Yang, J. Tang, Y. Li, Z. Wei, Y. Su, et al.,An enhanced equivalent circuit model of vanadium redox flow battery energy storage systems considering thermal effects, IEEE Access.7 (2019) 162297-162308.   
[22] Xiong B, Zhang H,Deng X,Tang J.State of Charge Estimation Based on Sliding Mode Observer for Vanadium Redox Flow Battery. Conference State of Charge Estimation Basedon Sliding Mode Observer for Vanadium Redox Flow Battery.p. 1-5.   
[23] Y. Zhang, J. Zhao, P. Wang, M. Skyllas-Kazacos, B. Xiong, R. Badrinarayanan, A comprehensive equivalent circuit model of all-vanadium redox flow battery for power system analysis, J. Power Sources 290 (2015) 14-24.   
[24] Y. Qiu, X. Li, W. Chen, Z.-m. Duan,L. Yu, State of charge estimation of vanadium redox battery based on improved extended Kalman filter, ISA Trans. 94 (2019) 326-337.   
[25] X. Zhao, J. Nam, H.-Y. Jung, S. Jung, Real-time state of charge and capacity estimations of vanadium redox flow battery based on unscented Kalman filter with a forgetting factor, Journal of Energy Storage. 74 (2023) 109146.   
[26] Z. Wei, K.J. Tseng, N. Wai, T.M. Lim, M. Skyllas-Kazacos, Adaptive estimation of state of charge and capacity with online identified battery model for vanadium redox flow battery, J. Power Sources 332 (2016) 389-398.   
[27] Z. Cen, P. Kubiak, Lithium-ion battery SOC/SOH adaptive estimation via simplified single particle model, Int. J. Energy Res.44 (15) (2020) 12444-12459.   
[28] S. Lee,J. Kim, J.Lee, B.H. Cho, State-of-charge and capacity estimation of lithium-ion battery using a new open-circuit voltage versus state-of-charge, J. Power Sources 185 (2) (2008) 1367-1373.   
[29] R. Xiong, F. Sun, Z. Chen, H. He,A data-driven multi-scale extended Kalman filtering based parameter and state estimation approach of lithium-ion polymer battery in electric vehicles, Appl. Energy 113 (2014) 463-476.   
[30] C. Hu, B.D. Youn, J. Chung, A multiscale framework with extended Kalman filter for lithium-ion battery SOC and capacity estimation, Appl. Energy 92 (2012) 694-704.   
[31] Y. Zou, X. Hu, H. Ma, S.E.Li, Combined state of charge and state of health estimation over lithium-ion battery cell cycle lifespan for electric vehicles,J.Power Sources 273 (2015) 793-803.   
[32] Chahwan J,Abbey C, Joos G. VRB Modelling for the Study of Output Terminal Voltages,Internal Losses and Performance.Conference VRB Modelling for the Study of Output Terminal Voltages, Internal Losses and Performance.p.387-92.   
[33] D.M. Hall, J. Grenier, T.S. Duffy, S.N. Lvov, The energy storage density of redox flow battery chemistries: a thermodynamic analysis, J. Electrochem. Soc.167 (11) (2020) 110536.   
[34] Dong S,Feng J, Zhang Y,Tong S,Tang J, Xiong B. State of Charge Estimation of Vanadium Redox Flow Battery Based on Online Equivalent Circuit Model. Conference State of Charge Estimation of Vanadium Redox Flow Battery Based on Online Equivalent Circuit Model. p. 1-6.   
[35] Z. Wei, A. Bhattarai, C. Zou, S. Meng, T.M. Lim, M. Skyllas-Kazacos, Real-time monitoring of capacity loss for vanadium redox flow battery, J. Power Sources 390 (2018) 261-269.   
[36] Z. Lao, B. Xia, W.Wang,W. Sun, Y. Lai, M. Wang,A novel method for Lithium-ion battery online parameter identification based on variable forgetting factor recursive least squares, Energies 11 (6) (2018).   
[37] X. Hao, S.Wang, Y. Fan, Y. Xie, C. Fernandez, An improved forgeting factor recursive least square and unscented particle filtering algorithm for accurate lithium-ion battery state of charge estimation, Journal of Energy Storage. (2023) 59.   
[38] M. Partovibakhsh, G. Liu, An adaptive unscented Kalman filtering approach for online estimation of model parameters and state-of-charge of lithium-ion batteries for autonomous mobile robots, IEEE Trans. Control Syst. Technol. 23 (1) (2015) 357-363.   
[39] Gahn RF,Hagedorn NH, Ling JS.Single cell performance studies on the Fe/Cr redox energy storage system using mixed reactant solutions at elevated temperature.Conference Single Cell Performance Studies on the Fe/Cr Redox Energy Storage System Using Mixed Reactant Solutions at Elevated Temperature.   
[40] H. Zhu,E.Bai, C.Sun, G.Liu, Z. Zhang, X. Xie, etal.,Biomass pomelo peel modified graphite feltelectrode for iron-chromium redox flow battery,J. Mater.Sci.58 (45) (2023) 17313-17325.   
[41] J.Chen,Y. Zhang, J.Wu, W. Cheng, Q. Zhu, SOC estimationfor lithium-ion battery using the LSTM-RNN with extended input and constrained output, Energy 262 (2023) 125375.   
[42] C.T.-C. Wan, K.E.Rodby, M.L. Perry, Y.-M. Chiang,F.R. Brushett Hydrogen evolution mitigation in iron-chromium redox flow batteries via electrochemical purification of the electrolyte, J. Power Sources 554 (2023) 232248.