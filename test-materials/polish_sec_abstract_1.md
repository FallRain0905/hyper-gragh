**摘要：**化工实验知识通常涉及多个变量在特定条件下的协同作用，传统向量检索和二元知识图谱难以充分表达这类高阶耦合关系。为此，本文提出了一种面向化工文献的领域适配超图增强检索方法（Hyper-RAG），将实验知识建模为"实验事实单元"，利用超边同时关联多个异构变量。以液流电池和PFAS降解两个领域为案例，分别设计了领域本体，并实现了基于大语言模型的结构化抽取与超图自动构建，进而设计了向量数据库与超图数据库协同的双路径检索机制。测试结果表明，Hyper-RAG在复杂条件查询中的召回更丰富，高阶超边有助于维持多个实验变量之间的共同上下文，从而改善了检索完整性和回答可解释性。

**关键词：**超图知识建模；检索增强生成；知识图谱；液流电池；PFAS降解；领域适配

**Hypergraph Knowledge Modeling and Enhanced Retrieval for Higher-Order Relational Expression in Chemical Engineering Knowledge**

**Abstract:** Experimental knowledge in chemical engineering typically involves the coordinated action of multiple variables under specific conditions, which is difficult to fully express through conventional vector retrieval or binary knowledge graphs. To address this limitation, a domain-adaptive hypergraph-enhanced retrieval method (Hyper-RAG) is proposed, modeling experimental knowledge as "experimental fact units" and employing hyperedges to simultaneously associate multiple heterogeneous variables. Taking flow battery and PFAS degradation as two case studies, domain ontologies were designed respectively, and structured extraction combined with automated hypergraph construction based on large language models was implemented. A dual-path retrieval mechanism leveraging vector and hypergraph database collaboration was also developed. Test results indicate that Hyper-RAG achieves richer recall for complex conditional queries, and high-order hyperedges help maintain shared context among multiple experimental variables, thereby improving retrieval completeness and response interpretability.

**Keywords:** hypergraph knowledge modeling; retrieval-augmented generation; knowledge graph; flow battery; PFAS degradation; domain adaptation


## 1 方法

### 1.1 化工文献知识的高阶关系特征

化工领域的实验知识具有显著的条件依赖性与多变量耦合特征。不同于一般文本知识中实体间简单的二元关联，化工实验事实往往涉及活性物质、操作条件、性能指标、系统组件等多个要素在特定情境下的协同作用。以液流电池研究为例，一个完整的实验知识单元通常包含：活性物质类型及其浓度（活性物质，ACTIVE_SPECIES）、操作温度与电流密度等工况条件（操作条件，CONDITION）、能量效率与容量衰减率等性能指标（性能指标，METRIC）、电极材料与膜材料等系统组件（电极材料ELECTRODE/膜材料MEMBRANE），以及这些要素之间的复杂交互关系。这些要素并非独立存在，而是通过实验操作（OPERATION）、组成配置（COMPOSITION）、降解机制（DEGRADATION）等关系类型形成高度交织的知识网络。

传统基于图的知识表示采用二元边 $e=(v_i, v_j)$ 描述实体间关系，难以直接表达"在特定温度和电流密度条件下，活性物质A在电极B上表现出容量衰减C"这类涉及三个及以上节点的复合实验事实。这种局限使得传统Graph-RAG在处理化工文献时需要将高阶关系拆分为多条二元边，分散了知识单元原有的变量关联信息。超图（Hypergraph）通过允许超边（hyperedge）同时连接任意数量的顶点，能够自然地表达化工实验知识中的多变量耦合关系，如图1所示。

图1 普通图与超图对化工实验知识的表达差异：普通图将多变量关系拆分为多条二元边，超图通过单一超边保留实验上下文

基于上述观察，本文将化工文献中的知识单元建模为"实验事实单元"（Experimental Fact Unit, EFU），每个EFU对应超图中的一条超边，其关联的实体要素构成该超边的顶点集合。这种建模方式使得检索过程能够在保持语义完整性的前提下，实现从高阶关系到具体实体的双向信息扩散。

### 1.2 领域适配超图增强检索框架

本文构建的领域适配超图增强检索框架，并非简单复用通用Hyper-RAG流程，而是围绕化工文献中"多变量共同约束实验事实"的表达需求，对知识组织方式进行了领域化改造。框架整体包括文献解析、文本分块、结构化抽取、超图构建、向量索引和问答检索六个环节，如图2所示。其中，前四个环节侧重于将非结构化文献转化为领域超图，后两个环节则利用超图结构为复杂问题回答提供增强上下文。

化工文献中的知识单元往往不是孤立实体或简单二元关系，而是由多个要素共同构成的实验事实。例如，在液流电池研究中，一个性能结论通常同时涉及电池体系、活性物质、电极材料、膜材料、电解液组成、电流密度、温度和效率指标等变量。若将其拆分为若干二元边，容易丢失"这些条件在同一实验中共同成立"的核心语义。因此，本文将化工文献中的完整实验事实定义为实验事实单元（experimental fact unit, EFU），并用超图中的一条超边表示该单元。

设输入化工文献集合为：

$$D = \{D_1, D_2, \ldots, D_n\}$$

其中，每篇文献 $D_i$ 经解析和分块后得到若干文本片段。全部文本片段集合记为：

$$T = \{t_1, t_2, \ldots, t_m\}$$

对于任一文本片段 $t_i$，结构化抽取函数 $\phi_d$ 在领域提示词 $P_d$ 的约束下，将其映射为实体集合和关系集合：

$$\phi_d(t_i, P_d) \rightarrow (V_i, E_i)$$

其中，$V_i$ 为从文本片段中抽取的领域实体，$E_i$ 为实体之间的关系或超边。所有文本片段的抽取结果合并后，构成领域超图：

$$G_d = (V, E)$$

其中，$V$ 表示全局实体节点集合，$E$ 表示关系/超边集合。对于任意一条关系 $e \in E$，可表示为：

$$e = (V_e, \tau_e, s_e)$$

其中，$V_e \subseteq V$ 表示该关系连接的实体集合，$\tau_e$ 表示关系类型，$s_e$ 表示来源文本或文献片段。当 $|V_e|=2$ 时，$e$ 对应普通二元关系；当 $|V_e| \geq 3$ 时，$e$ 对应高阶超边，可表示多个实体在同一实验事实中的共同参与关系。

这种建模方式使得一条超边不仅表示实体共现，还保留了具体的领域语义。例如，一条操作超边可以同时连接"VRFB""Nafion膜""BMC-C电极""200 mA/cm²""EE 80%"等实体，从而表示一个完整的"体系—材料—条件—指标"组合事实。相比普通图中多条二元边的分散表达，超图能够直接保留化工实验知识中的条件完整性和语义闭合性。

在问答检索阶段，系统将用户问题转化为实体关键词和关系关键词，并分别在实体向量索引和关系向量索引中进行检索。随后，系统沿超图结构进行一阶扩散，将命中的实体扩展到其所在超边，并将命中的超边扩展到其包含的实体。该过程的作用不是简单增加召回数量，而是尽可能恢复与问题相关的完整实验事实单元，使大语言模型在生成回答时能够同时获得材料、条件、指标和机理之间的结构化上下文。为开展对比实验，本文同时构建普通图基线，即仅保留 $|V_e|=2$ 的二元边，将高阶超边过滤后形成Graph-RAG检索结构。

图2 领域适配超图增强检索框架总体流程图

### 1.3 化工领域结构化抽取设计

结构化抽取是领域适配超图构建的关键步骤，其目标是将自然语言文献中的化工知识转化为可计算的实体节点和关系/超边。与通用信息抽取不同，化工文献抽取需要同时关注实验对象、材料组成、操作条件、性能指标和机理证据等多类信息，并保持它们在同一实验情境中的组合关系。因此，本文围绕液流电池领域设计了实体类型体系、关系/超边类型体系和结构化输出格式。

在实体类型设计上，本文选取能够覆盖液流电池实验知识主要要素的7类实体，如表1所示。这些实体类型并非按照通用命名实体识别中的"人名、机构、地点"等类别划分，而是根据化工实验事实的组成方式进行定义。例如，ACTIVE_SPECIES（活性物质）用于表示电解液中的氧化还原活性物质，CONDITION（操作条件）用于表示电流密度、温度、流速等实验工况，METRIC（性能指标）用于表示能量效率、容量保持率、功率密度等评价指标。通过这种领域化实体类型设计，可以使抽取结果更贴近化工研究者实际关注的知识单元。

**表1 液流电池领域实体类型体系**

| 实体类型 | 说明 | 描述 |
| --- | --- | --- |
| ACTIVE_SPECIES | 活性物质 | 电解液中的氧化还原活性物质，如全钒液流电池中的V²⁺/V³⁺电对 |
| METRIC | 性能指标 | 量化评价指标，如能量效率、电压效率、容量衰减率、循环寿命等 |
| CONDITION | 操作条件 | 实验工况参数，如温度、电流密度、流速、充放电制度等 |
| SYSTEM | 系统类型 | 液流电池系统构型，如全钒液流电池、锌溴液流电池等 |
| ELECTRODE | 电极材料 | 电极基体材料及改性，如石墨毡、碳毡、氮掺杂电极等 |
| DEGRADATION | 降解机制 | 性能衰减机理类型，如活性物质交叉污染、电极氧化降解等 |
| MEMBRANE | 膜材料 | 离子交换膜及多孔膜，如Nafion膜、多孔离子传导膜等 |

在关系/超边类型设计上，本文根据液流电池文献中常见的知识组织方式，定义了4类核心关系类型。它们既可以表示二元关系，也可以表示连接多个实体的高阶超边，具体取决于同一实验事实中涉及的实体数量。

（1）OPERATION（操作关系）：用于描述电池体系、活性物质、操作条件和性能指标之间的实验运行关系。例如，一条OPERATION超边可以同时连接"VRFB""VOSO₄""H₂SO₄""100 mA/cm²""EE 80%"等实体，用于表示特定电解液和工况下获得的性能结果。

（2）COMPOSITION（组成关系）：用于描述材料、组件或体系的组成结构。例如，膜材料的基体、改性基团、掺杂组分和离子交换容量可以共同构成一条COMPOSITION超边，用于表示材料设计方案。

（3）DEGRADATION（衰减关系）：用于描述性能衰减或失效过程中的条件、机制和结果。例如，高温、活性物质交叉迁移、副反应和容量衰减可以被组织为一条DEGRADATION超边，用于表示从条件到机制再到性能变化的链式关系。

（4）COMPARISON（对比关系）：用于描述不同材料、不同条件或不同体系之间的性能比较。例如，C-C、MC-C和BMC-C等电极材料在不同电流密度下的效率差异，可以通过COMPARISON超边表示，从而保留比较对象、比较条件和比较指标之间的共同约束。

每个文本块的抽取结果包含三部分：实体列表、低阶关系列表和高阶超边列表。其中，实体列表记录实体名称、类型、数值、单位和描述信息；低阶关系列表记录二元关系；高阶超边列表记录三个及以上实体共同构成的实验事实单元。通过强制结构化输出，可以减少自由文本生成带来的格式不稳定问题，并便于后续进行节点合并、超边构建和来源追踪。

需要指出的是，该结构化抽取设计具有领域可迁移性。对于不同化工子领域，框架本身无需改变，只需替换实体类型、关系类型和领域提示词。例如，在含氟污染物降解案例中，可将实体类型调整为PFAS_TARGET、CATALYST_MATERIAL、ACTIVE_SPECIES、MECHANISM_EVIDENCE等，并将关系类型调整为OPERATION_PERFORMANCE、MECHANISM_PATHWAY、ADSORPTION_ORIENTATION等。由此，本文方法能够在保持统一超图建模框架的同时，适配不同化工领域的知识结构特征。
