# 修改后的摘要与引言

---

## 摘要

化工实验知识通常涉及反应物、催化剂、操作条件与评价指标等多个变量的协同约束，传统向量检索和二元知识图谱在表达此类多变量耦合关系时存在局限。

本文对液流电池和PFAS降解两个领域的文献进行梳理，发现实验知识中的条件、材料、指标和机理等要素常以多实体组合的形式出现。例如，液流电池中电解质组成与电极材料的匹配关系、PFAS降解中催化剂结构与反应条件的调控关系，均需要同时记录多个关联变量才能完整表达。针对这一特点，本文提出将实验知识组织为"实验事实单元"（Experimental Fact Unit, EFU），并在此基础上构建领域适配的超图增强检索框架 Hyper-ChE。

Hyper-ChE 的核心设计包括三个部分：一是 EFU 建模，将文献中的实验发现抽象为包含多实体关联的结构化单元；二是面向液流电池和PFAS降解两个领域分别构建本体，并基于大语言模型实现从非结构化文本到超图结构的自动抽取；三是设计向量数据库与超图数据库协同的双路径检索机制，以兼顾语义匹配与高阶关联查询。

实验结果表明，在涉及多变量约束的复杂查询中，Hyper-ChE 的召回内容比基线方法更为完整。超边结构能够保持多个实验变量之间的共同上下文，改善了检索结果的可解释性。当前工作初步验证了超图建模在化工实验知识检索中的可行性，为后续面向更多反应体系的知识库构建提供了参考。

**关键词**：化工知识工程；超图检索；实验事实单元；液流电池；PFAS降解

---

## Abstract

Chemical experimental knowledge typically involves the joint constraints of multiple variables—reaction substrates, catalysts, operating conditions, and performance metrics. Conventional vector retrieval and binary knowledge graphs face limitations when representing such multi-variable coupling relationships.

Through a systematic review of literature in two representative domains—flow batteries and PFAS degradation—we observe that experimental knowledge tends to appear in the form of multi-entity combinations. For instance, the pairing between electrolyte composition and electrode materials in flow batteries, or the matching between catalyst structure and reaction conditions in PFAS degradation, both require simultaneous tracking of multiple related variables for complete expression. To address this structural feature, we propose organizing experimental knowledge into "Experimental Fact Units" (EFUs) and building Hyper-ChE, a domain-adapted hypergraph-enhanced retrieval framework.

Hyper-ChE comprises three core components: (1) EFU modeling, which abstracts experimental findings from literature into structured units containing multi-entity associations; (2) domain-specific ontology construction for flow batteries and PFAS degradation respectively, coupled with LLM-based extraction pipelines that transform unstructured text into hypergraph structures; and (3) a dual-path retrieval mechanism that coordinates vector and hypergraph databases to support both semantic matching and higher-order relation queries.

Experimental results show that Hyper-ChE yields more complete recall than baseline methods on complex queries involving multi-variable constraints. The hyperedge structure preserves shared context among experimental variables and improves the interpretability of retrieval outputs. This work provides preliminary evidence for the feasibility of hypergraph-based modeling in chemical knowledge retrieval and offers a reference prototype for future knowledge base construction across additional reaction systems.

**Keywords**: chemical knowledge engineering; hypergraph retrieval; experimental fact unit; flow battery; PFAS degradation

---

## 1 引言

### 1.1 研究背景与问题

液流电池、PFAS降解、电催化等化工子领域的学术文献产出持续增加，实验数据与工艺经验分散于大量非结构化文本中。以液流电池为例，全钒体系的研究文献已超过万篇，涉及电解液配方、电极改性、膜材料筛选等多类实验信息；PFAS降解领域同样积累了大量关于催化剂设计、反应条件优化的实验记录。不同反应体系之间的知识壁垒仍然明显，研究人员在解决具体问题时难以高效调用已有结论。

将分散的实验发现转化为可计算、可检索的结构化知识，是化工知识工程面临的基础问题。与一般文本知识不同，化工实验结论通常由多个要素共同决定：反应物种类、催化剂结构、操作参数和评价指标之间存在相互约束关系。例如，在液流电池研究中，电解液中钒离子浓度与电极表面功能化修饰往往需要协同优化；在PFAS降解中，催化剂的晶相结构与溶液pH值、温度的匹配直接影响降解效率。这类知识更接近"多变量共同成立的实验事实"，而非可以任意拆分的独立陈述。

传统检索方法主要依赖关键词匹配或向量相似度计算，能够定位语义相近的文本片段，但难以保证同一实验事实涉及的多变量组合被完整召回。当查询需要保持条件组合的一致性时，返回结果往往呈现碎片化特征，无法还原完整的实验上下文。例如，查询"全钒液流电池中电解液浓度对库仑效率的影响"时，向量检索可能返回讨论电解液黏度或电极孔隙率的片段，却遗漏了同时涉及浓度与效率测量条件的原文段落。

### 1.2 从知识图谱到超图的建模思路

知识图谱增强检索（Graph-RAG）通过二元关系三元组（头实体-关系-尾实体）对文献内容进行结构化建模，在一定程度上改善了检索的逻辑性和可解释性。然而，二元图谱将多变量关联强行拆解为多条 pairwise 边，丢失了多实体共同成立的上下文信息。

例如，液流电池中的一组完整实验结论可能涉及"电解液组成A-在电极B上-于温度C下-实现了效率D"，这是一个四变量共同成立的实验事实。若拆分为三条二元边（A-B、B-C、C-D），每次检索只能召回两两之间的关系，无法判断A、B、C、D是否来自同一实验记录。PFAS降解中存在类似的结构："催化剂X-在pH Y下-对底物Z-达到降解率W"，同样需要多变量联合表达。

超图（hypergraph）理论为解决上述问题提供了形式化工具。超图 H=(V,E) 中的超边可以连接任意数量的顶点，从而直接刻画 beyond-pairwise 的关联模式。一条超边可以同时包含电解液组成、电极材料、温度条件和效率指标等多个实体，保持它们之间的共同上下文。Feng等提出的 Hyper-RAG 框架以超图替代二元图进行知识建模，展示了处理复杂关联结构的潜力。

### 1.3 相关工作

**传统RAG与Graph-RAG。** 检索增强生成（RAG）技术通过从外部知识库中检索相关文本片段来辅助大语言模型回答领域问题。传统RAG主要基于文本块的向量相似度进行检索，在需要整合多个关联信息片段的复杂查询中表现有限。Graph-RAG 方法通过从文本中提取实体关系三元组构建知识图谱，利用图的连通性进行多跳推理检索。研究表明，Graph-RAG 在需要逻辑推理的查询中优于纯向量检索，但在处理多变量联合约束时，二元关系的表达能力仍然不足。

**超图增强检索。** 近年来，超图结构被引入检索系统以处理高阶关联。Feng等提出的 Hyper-RAG 利用超边连接多个关联实体，实现了超越二元关系的知识建模。后续研究如 HyperGraphRAG 进一步探索了超图在开放域问答中的应用，通过超边保持多实体之间的共现信息。目前超图检索方法主要面向通用领域，在化工等实验科学领域的适配研究尚不多见。

**知识超图生成。** 从非结构化文本自动生成超图结构是超图检索的基础环节。Hyper-KGGen 等工作探索了基于大语言模型的超图抽取方法，通过设计结构化提示模板引导模型识别多实体关联。这类方法为领域超图的自动构建提供了技术参考，但在面向化工文献时，需要针对实验知识的特点进行领域适配，包括设计专用的信息抽取模板和质量验证机制。

### 1.4 本文工作

基于上述分析，本文提出面向化工文献的领域适配超图增强检索框架 Hyper-ChE（Hypergraph-enhanced Chemical Engineering Retrieval），并以液流电池和PFAS降解两个领域为例进行原型验证。本文的主要贡献包括：

（1）提出"实验事实单元"（EFU）建模方式，将化工文献中的实验发现抽象为包含多实体关联的结构化单元，为超图构建提供统一的知识组织形式；

（2）构建 Hyper-ChE 检索框架，实现面向化工领域的超图自动构建与双路径协同检索，支持语义匹配与高阶关联查询的结合；

（3）在液流电池和PFAS降解两个领域上完成原型实现与初步测试，结果表明超图结构在多变量约束查询中能够提供更完整的召回和更好的可解释性。

后续章节安排如下：第2节介绍实验事实单元建模方法与 Hyper-ChE 框架的总体架构；第3节描述液流电池和PFAS降解两个领域的本体设计与超图构建流程；第4节给出检索机制的设计与实验测试结果；第5节进行讨论；第6节总结全文。

---
