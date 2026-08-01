## 4 讨论

### 4.1 超图建模的优势与适用边界

基于液流电池案例的实验结果，超图建模的价值集中在三类高复杂度查询：**多条件约束问题**（Level 3）、**跨材料对比问题**（Level 4）与**策略推荐问题**（Level 6）。对于多条件约束问题，高阶超边将操作条件与性能指标保留在同一关系结构内，减少二元图中条件-指标对分散在不同边中的问题。对于跨材料对比问题，超图通过共享实体连接不同材料体系的关系簇，降低了横向比较对人工对齐的依赖。对于策略推荐问题，高阶关系能够维持"目标-约束-方案-预期"之间的语义完整性，使推荐结果中的变量组合更为连贯。

超图建模的优势边界可描述为：当查询需要判断"多个条件是否属于同一实验事实"时，高阶超边提供的结构信息才能体现。对于单一概念解释类问题、简单事实查询或仅需枚举型知识的语料总览型问题，向量检索或二元图检索已能提供足够准确的答案，超图建模的收益有限。

在PFAS去除与降解案例中，两个案例中Hyper-RAG的表现规律相似，但具体的高阶关系类型有所不同。液流电池案例中的高阶关系主要体现为"体系-活性物种-膜/电极-操作条件-性能指标"的实验操作组合，而PFAS降解案例中的高阶关系则集中表现为"目标污染物-催化材料-反应条件-性能指标-机理证据"的多实体耦合。这反映了不同子领域知识组织的差异：液流电池研究以电化学性能测试为主线，条件组合主要服务于效率优化；PFAS降解研究以污染物去除机理为核心，条件组合需要同时支撑性能评价与机制解释。两个案例表明，当查询涉及多个条件共同约束、跨实体横向对比或多证据协同支撑时，超图建模能够提供优于二元图的知识表达与检索能力。

值得补充的是，超图建模的优势并非在所有查询类型上均匀分布。在PFAS降解案例中，Level 1语料总览型问题（如Q1、Q2）中两套系统的回答质量差距较小，因为这类问题主要依赖枚举型知识，对条件组合的完整性要求较低。而在Level 3条件组合型问题（Q5）和Level 5机理证据链型问题（Q10）中，Hyper-RAG的优势最为明显，因为此类问题本质上要求判断"多个变量是否属于同一实验事实"或"多类证据是否共同支撑同一机理判断"。这一规律与液流电池案例中的观察一致，进一步表明超图建模的优势边界在于：当查询需要保持多变量在同一关系结构中的协同出现时，高阶超边才能发挥优势。

### 4.2 领域适配的必要性

通用LLM在化工文献实体抽取中面临三方面挑战。其一，专业术语与同义词的辨识：同一材料或概念在不同文献中可能以多种表述形式出现（如"Nafion膜"与"全氟磺酸膜"、"PFOA"与"C8"），缺乏领域约束的抽取容易将同一实体的不同表述割裂为独立节点。其二，实验条件数值与单位的非标准化形式：温度、浓度、电流密度等条件常以不同单位或数值范围呈现，需要结构化解析才能归一。其三，离子形态变体：如V(II)/V(III)/V(IV)/V(V)在液流电池中代表不同价态，PFAS类物质存在链长变异与官能团替换，通用模型难以区分化学意义上的等价与不等价表述。

本文采用三方面措施应对上述挑战。第一层，通过预定义实体类型与超边类型约束抽取空间，使LLM在有限类型的引导下进行结构化输出，减少术语歧义。第二层，采用JSON结构化输出格式，明确指定字段名称与层级关系，减少格式漂移。第三层，将UNKNOWN率作为辅助质量指标，当抽取过程中出现无法归类为预定义类型的实体或关系时，以UNKNOWN标签标记并统计其占比，据此判断当前领域提示词的适配程度。在液流电池案例中，UNKNOWN率约为10%~15%，提示仍有部分术语或关系超出预定义类型的覆盖范围；而在PFAS降解案例中，UNKNOWN节点数为0，表明当前领域提示词的实体一致性较好。这种差异可能与两个领域术语标准化程度不同有关——PFAS领域存在相对统一的物质命名体系（如PFOA、PFOS等缩写已被广泛接受），而液流电池领域的材料命名和体系描述更为多样。

需要指出的是，本文未对LLM进行微调训练，所有领域适配均通过提示词工程实现。这一设计选择确保了方法的可迁移性：当应用场景从液流电池切换至PFAS降解时，仅需替换实体类型与关系类型的定义即可复用整套抽取与检索流程。基于当前语料的观察，这种轻量级适配策略在两个化工子领域中均展现了基本的可用性，但精度仍低于微调模型。

### 4.3 局限性与未来工作

本文方法存在以下局限。

**第一，实体名称归一化尚不充分。** 不同文献对同一材料或概念可能使用不同表述（如"Nafion"与"全氟磺酸树脂"、"PFOA"与"C8"、"PFOS"与"C8S"），当前抽取流程将这些变体视为独立节点，未进行语义层面的合并。这一问题在PFAS降解领域尤为突出：PFAS类物质存在大量同义词变体（如商用名与化学名的混用）、催化材料的缩写与全称并存、以及活性物种的多种表示方式（如"•OH"、"羟基自由基"、"OH radical"）。实体节点的大量分裂不仅增加了知识库冗余，也可能导致检索时因表述差异而遗漏相关文献。未来工作可引入ChEBI、PubChem等化学本体库作为外部知识源，通过实体链接或嵌入相似度计算实现PFAS类物质与催化材料的语义对齐。

**第二，高阶超边的抽取质量存在稳定性问题。** 尽管PFAS案例中UNKNOWN率为0，但高阶超边的结构正确性仍依赖LLM对复杂语义的理解能力。当文献描述存在长距离依赖、隐含条件或复杂逻辑关系时，抽取的高阶超边可能出现实体遗漏或关系类型误判。在液流电池案例中，UNKNOWN率约为10%~15%，表明仍有部分术语或关系超出预定义类型的覆盖范围。未来可通过微调策略或多轮一致性校验提升高阶关系抽取的稳定性，例如利用验证LLM对已抽取的超边进行结构合理性检查。

**第三，结构化条件查询的联合优化尚未解决。** 当查询涉及数值范围（如"电流密度大于100 mA/cm²"）或多个条件的逻辑组合（如"温度低于30℃且电压高于1.5 V"）时，当前检索机制主要基于语义相似度匹配，缺乏对数值约束和逻辑运算符的精确处理。这在两个案例中均可能限制查询的精确性，特别是在需要筛选特定条件区间的实验数据时。未来工作可探索将数值解析与逻辑约束集成到超图检索过程中，实现语义匹配与结构化查询的联合优化。

此外，在PFAS降解案例中，当前知识库仅包含49篇已完成嵌入的文献，尚未覆盖全部候选文献集。随着语料规模从49篇扩展至126篇，以下方面的证据覆盖有望进一步增强：（1）短链PFAS（如PFBA、PFBS、GenX）的降解机理与材料设计知识；（2）压电-光催化和压电-Fenton等耦合策略的实验条件组合；（3）材料掺杂机制（如氧空位调控、异质结构建）与脱氟性能之间的定量关系。基于当前子集规模的验证结果虽已初步表明超图建模在多变量组合查询中的优势，但更全面的结论有待更大规模语料的支持。

## 5 结论

本文提出超图增强RAG（Hyper-RAG）方法，通过高阶超边建模化工实验中多变量耦合关系，解决传统Graph-RAG二元边表示导致的多条件组合信息损失问题。方法核心是将化工实验知识抽象为包含"体系—材料—条件—指标—机理"的高阶组合，以超图结构替代传统图结构进行知识存储与检索，从而在需要保持条件组合完整性的复杂检索场景中提升检索增强效果。

在液流电池领域，基于49篇文献构建的知识库包含9970个实体和12987条超边，其中高阶超边占20.9%。对比评估表明，Hyper-RAG平均召回103条高阶超边/63个实体，Graph-RAG平均召回46条二元边，在条件完整性、上下文可解释性和跨域关联能力三方面具有优势。该案例验证了超图结构对"体系—材料—条件—性能"高阶关系的表达能力，表明化工知识包含多实体共同约束的特征。

为进一步验证超图知识建模在多变量耦合实验科学中的适用性，本文以PFAS去除与降解领域为第二案例进行了验证。基于49篇文献构建的知识库包含7253个实体和10363条关系/超边，其中高阶超边占比21.98%。在覆盖语料总览、条件组合、跨策略比较、长短链对比、机理证据链和实验方案推荐的12个测试问题中，Hyper-RAG平均召回81.5条高阶超边，约为Graph-RAG（37.9条二元边）的2.15倍。典型问题分析表明，Hyper-RAG在多条件组合保留（Q5）、跨策略横向比较（Q7）、目标污染物差异化分析（Q8）、多证据机理链组织（Q10）和实验方案结构化推荐（Q12）等任务中表现更好。该结果与液流电池案例的发现一致，表明化工领域的实验知识涉及多个变量同时约束，超图结构对"目标污染物—材料—条件—指标—机理"高阶关系的表达能力使其在需要保持条件组合完整性的复杂检索场景中具有优势。

综合液流电池与PFAS降解两个案例的验证结果，超图增强检索方法的价值体现在以下三个方面：第一，条件完整性——高阶超边保留了同一实验中多个条件的关联信息，减少了二元关系拆分导致的信息损失；第二，上下文可解释性——通过机理路径和比较关系的结构化组织，检索结果包含事实数据与机理解释；第三，跨域关联能力——统一的知识建模框架支持不同化工子领域间的知识迁移。两个案例的领域差异——液流电池以电化学性能优化为主线、PFAS降解以污染物去除机理为核心——表明该方法不限于特定化工方向，可扩展至其他多变量耦合的实验科学领域。

需要指出的是，当前两个案例分别基于49篇文献的子集语料，尚未覆盖全部候选文献集，因此上述结论属于知识结构对检索增强效果的子集验证，而非全面综述。此外，知识抽取的准确性受限于大语言模型的实体识别与关系抽取能力，复杂机理关系仍可能出现边界模糊的情况。未来工作将从以下方向展开：一是扩大语料覆盖范围，纳入更多文献以检验方法的可扩展性；二是探索超边权重学习机制，优化检索排序；三是将方法推广至电催化、电池材料、反应工程等其他化工子领域，进一步验证其领域通用性。

## 参考文献

[1] 陈海生, 蒋凯, 等. 液流电池关键材料发展研究[J]. 中国工程科学, 2025, 27(10): 1-12.

[2] Ding C S, Zhang H N, et al. Sulfonated polybenzimidazole zwitterionic exchange membrane for vanadium flow batteries[J]. Journal of Membrane Science, 2023, 669: 121-135.

[3] Chen Y K, et al. High-activity and high-stability bismuth single-atom electrocatalyst for vanadium redox flow batteries[J]. Advanced Materials, 2024, 36: 2308124.

[4] 中国储能技术研究进展2024[J]. 储能科学与技术, 2025, 14(1): 1-30.

[5] Ye Y P, Ren J, Wang S Z, et al. Construction and application of materials knowledge graph in multidisciplinary materials science via large language model[J]. arXiv preprint arXiv:2404.03080, 2024.

[6] Lewis P, Perez E, Piktus A, et al. Retrieval-augmented generation for knowledge-intensive NLP tasks[J]. Advances in Neural Information Processing Systems, 2020, 33: 9459-9474.

[7] Gao Y L, Xiong Y T, Gao X R, et al. Retrieval-augmented generation for large language models: A survey[J]. arXiv preprint arXiv:2312.10997, 2024.

[8] Wu S C, Xiong Y T, Cui Y X, et al. Retrieval-augmented generation for natural language processing: A survey[J]. arXiv preprint arXiv:2407.13167, 2024.

[9] Mallen A, Asai A, Zhong V, et al. When not to trust language models: Investigating effectiveness of parametric and non-parametric memories[J]. Proceedings of ACL, 2023, 1: 9802-9822.

[10] Pan S R, Luo L, Wang Y F, et al. Unifying large language models and knowledge graphs: A roadmap[J]. IEEE Transactions on Knowledge and Data Engineering, 2024, 36(7): 3580-3599.

[11] Feng Y, Hu H, Hou X, et al. Hyper-RAG: Combating LLM hallucinations using hypergraph-driven retrieval-augmented generation[J]. arXiv preprint arXiv:2504.08758, 2025.

[12] Zhou D Y, Zheng L, Han J W, et al. A survey of graph neural networks for recommender systems: Challenges, methods, and directions[J]. ACM Transactions on Recommender Systems, 2025, 3(4): 1-53.

[13] Luo H R, Chen G T, Zheng Y D, et al. HyperGraphRAG: Retrieval-augmented generation via hypergraph-structured knowledge representation[J]. arXiv preprint arXiv:2503.21322, 2025.

[14] Edge D, Trinh H, Cheng N, et al. From local to global: A graph RAG approach to query-focused summarization[J]. arXiv preprint arXiv:2404.16130, 2024.

[15] Guo Z, Xia L, Yu Y, et al. LightRAG: Simple and fast retrieval-augmented generation[J]. arXiv preprint arXiv:2410.05779, 2024.

[16] Zhao X, Huang W, Wang Z, et al. Hypergraph structure learning for multimodal retrieval-augmented generation[J]. arXiv preprint arXiv:2506.03778, 2025.

[17] Gao Y, Feng Y, Ji S, et al. HGNN+: General hypergraph neural networks[J]. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2023, 45: 3181-3199.

[18] Dagdelen J, et al. Structured information extraction from scientific text with large language models[J]. Nature Communications, 2024, 15: 1418.

[19] Prince M H, et al. Opportunities for retrieval and tool augmented large language models in scientific facilities[J]. npj Computational Materials, 2024, 10: 251.

[20] Huang L, et al. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions[J]. ACM Transactions on Information Systems, 2025, 43: 1-55.
