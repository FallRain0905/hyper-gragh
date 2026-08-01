### 3.1 数据来源与知识库构建

以全氟/多氟烷基化合物（Per- and Polyfluoroalkyl Substances, PFAS）去除与降解为应用背景，构建涵盖多目标污染物、多处理策略的专业知识库。实验语料库来源于49篇领域学术文献，涵盖PFOA（全氟辛酸）、PFOS（全氟辛烷磺酸）、PFBA（全氟丁酸）、PFBS（全氟丁烷磺酸）、GenX（HFPO-DA）等主要目标污染物，处理策略涉及吸附、压电催化、压电-光催化、压电-Fenton、电化学氧化等技术路线。经文本解析与分块预处理后，共提取599个文本块作为知识抽取的基本单元。

基于上述语料构建的PFAS降解案例知识库统计如表5所示。

**表5 PFAS去除与降解知识库构建统计**

| 项目 | 数量 | 说明 |
|------|------|------|
| 文档数 | 49 | 当前缓存实际写入49篇PFAS去除与降解领域文献 |
| 文本块 | 599 | 文献解析与分块后的基本抽取单元 |
| 实体节点 | 7253 | 超图数据库中的全部实体节点 |
| 全部关系/超边 | 10363 | 低阶关系与高阶超边总数 |
| 低阶关系 | 8051 | 二元关系，cardinality = 2 |
| 高阶关系/高阶超边 | 2278 | 三元及以上关系，cardinality ≥ 3 |
| 单节点/自关系 | 34 | cardinality = 1 |
| UNKNOWN节点 | 0 | 表明当前领域提示词的实体一致性较好 |

对表5的分析表明，在PFAS去除与降解案例中，高阶关系/超边占全部关系的21.98%。该比例与液流电池案例（20.9%）处于相近水平，说明PFAS降解文献中同样存在大量不能由普通二元边完整表达的多变量实验事实。

知识库中的实体类型分布如表6所示。

**表6 PFAS去除与降解案例实体类型分布**

| 实体类型 | 数量 |
|----------|------:|
| METRIC（性能指标） | 1397 |
| CONDITION（反应条件） | 1181 |
| CATALYST_MATERIAL（催化材料） | 1181 |
| MATERIAL_FEATURE（材料特征） | 1048 |
| MECHANISM_EVIDENCE（机理证据） | 856 |
| PROCESS_STRATEGY（过程策略） | 503 |
| PFAS_TARGET（目标PFAS） | 323 |
| ACTIVE_SPECIES（活性物种） | 312 |
| PIEZO_PROPERTY（压电性质） | 249 |
| WATER_MATRIX（水体基质） | 203 |

关系/超边类型分布如表7所示。

**表7 PFAS去除与降解案例关系/超边类型分布**

| 关系/超边类型 | 数量 |
|--------------|------:|
| OPERATION_PERFORMANCE（操作-性能关系） | 3147 |
| MECHANISM_PATHWAY（机理路径关系） | 2511 |
| MATERIAL_DESIGN（材料设计关系） | 2303 |
| COMPARISON（比较关系） | 943 |
| MATRIX_APPLICATION（基质应用关系） | 563 |
| COUPLING_STRATEGY（耦合策略关系） | 337 |
| CHARGE_TRANSFER（电荷转移关系） | 220 |
| ADSORPTION_ORIENTATION（吸附取向关系） | 189 |

基于当前语料的归纳表明，PFAS降解文献中的知识并非仅由污染物和材料之间的二元关系构成，而是大量体现为目标污染物、材料结构、反应条件、性能指标与机理证据之间的高阶耦合。OPERATION_PERFORMANCE、MECHANISM_PATHWAY和MATERIAL_DESIGN三类关系占比较高，说明PFAS降解文献的知识组织并不只是"材料A降解污染物B"这类简单事实，而是集中体现为实验操作、性能结果和机理证据之间的多实体耦合。

从领域适配角度来看，上述方法框架本身无需改变，仅需根据PFAS降解领域的知识结构特征替换实体类型与关系类型。具体而言，将液流电池案例中的SYSTEM、ACTIVE_SPECIES、ELECTRODE、MEMBRANE等实体类型替换为PFAS_TARGET、CATALYST_MATERIAL、ACTIVE_SPECIES、MECHANISM_EVIDENCE、PIEZO_PROPERTY、WATER_MATRIX等类型，将OPERATION、COMPOSITION、DEGRADATION等关系类型替换为OPERATION_PERFORMANCE、MECHANISM_PATHWAY、MATERIAL_DESIGN、ADSORPTION_ORIENTATION等类型，即可实现从液流电池领域向PFAS降解领域的知识建模迁移。这一可迁移性表明，本文所提出的超图知识建模框架具有一定的领域通用性，能够适配不同化工子领域中"多变量共同约束实验事实"的表达需求。

需要指出的是，当前PFAS案例仅基于已完成嵌入的49篇文献，尚未覆盖全部候选文献集。因此，本节不将后续问答结果解释为对PFAS降解领域的全面综述结论，而将其作为知识结构对检索增强效果影响的子集验证。
