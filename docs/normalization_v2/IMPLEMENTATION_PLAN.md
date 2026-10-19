# 词典优先离线归一化：完整实施计划

计划版本：implementation-1，2026-10-19。状态：**待实现**。本文所有新增文件、接口、CLI 和 schema 均为规划目标，不表示当前仓库已经支持。

上位设计：[DESIGN.md](DESIGN.md)。固定决策：[DECISIONS.yaml](DECISIONS.yaml)。验收契约：[ACCEPTANCE.yaml](ACCEPTANCE.yaml)。基线：[baseline.json](baseline.json)。

## 1. 终态范围与交付规则

完整终态包含：

- 两个现有子领域的声明式身份规则和统一编译器；
- 轻量抽取输出及兼容旧数据的导入器；
- 确定性身份绑定、临时身份登记、少量歧义任务及持久复用；
- 原始来源、身份决策、事实和测量的事务账本；
- 正确保留角色与实验范围的图、检索和向量投影；
- 文献更新、撤回、规则变更、绑定拆分及中断恢复；
- CLI、Web、模型 profile、提示包版本和运行配置的完整集成；
- 新旧方案并存、独立目标缓存、离线验收、真实成本及科学质量对照；
- 使用说明、决策追踪、恢复说明和完整发布清单。

W01—W12 是同一个完整设计的依赖顺序。单个工作包完成不能标记整个 v2 已完成；不能用删掉来源事务、Web 接入、恢复、成本核验等方式提前发布“MVP”。所有新增运行逻辑都限定在显式选择的 v2 策略下。

## 2. 路由与兼容真值表

| 入口／来源 | 执行策略 | 抽取阶段判同 | 输出规则 |
|---|---|---:|---|
| 现有在线构建入口和旧配置 | legacy_online，或保留原关闭状态 | 按原开关 | 维持旧行为与旧格式 |
| 现有 normalize_cache_posthoc.py | legacy_posthoc | 不改变源抽取 | 维持旧脚本、参数、输出格式 |
| 缺少 strategy 的已发布缓存 | 使用已有冻结 manifest/run_config | 不启动构建 | 只读查询，禁止猜测为 v2 |
| 新建 v2 作业 | registry_offline_v2 | false | 独立 schema、作业库、图和索引 |
| 从旧抽取导入 v2 | registry_offline_v2 | 不重抽取 | 显式字段可用性和导入证据 |

新增配置采用 `normalization_strategy`、`normalization_phase`、`normalize_during_extraction` 和 `normalization_profile_hash`。原 `enable_entity_normalization` 继续保持旧语义；v2 由单一配置适配器映射，禁止被旧 JSON 抽取 hook 再次归一化。冲突配置启动前失败。

保留 `hyperche/normalization/` 下旧实现。新代码放在 `hyperche/normalization_v2/`。现有 modes 中 hyper_base、hyper_chem_prompt、hyper_norm、hyper_final、F0/F1 比较及论文结果不重定义。新评估另设 profile 和输出目录，不覆盖历史分组。

## 3. 目标模块与现有接入点

| 新模块或改动位置 | 责任 | 现有代码依据 |
|---|---|---|
| normalization_v2/contracts.py | 版本化记录、状态、校验和指纹 | 不复用旧自由格式作为新契约 |
| normalization_v2/registry.py、text_policy.py | YAML 编译、作用域索引、保护属性 | 旧 alias_registry/text_normalizer 作为迁移参照 |
| normalization_v2/ledger.py | SQLite 约束、事件、事务、outbox | 独立于 auth 数据库，禁止混入密钥 |
| normalization_v2/importers.py、extraction.py | 原始记录及旧响应导入、抽取旁路落盘 | hyperrag/operate.py、build_experiment_cache.py |
| normalization_v2/resolver.py、candidate_index.py | 已知命中、新身份、有限候选与歧义 | 不调用旧 generate_candidates |
| normalization_v2/decisions.py | 冻结判断任务、校验、重试及复用 | providers.py、runtime_requests.py 的共享接口 |
| normalization_v2/quantities.py、facts.py | 数值单位、实验范围、角色和事实 ID | final_cache.py 的经验与回归样例 |
| normalization_v2/projections.py、vectors.py | fact_store、结构桶、BM25/向量投影 | hyperrag/storage.py 和检索适配器 |
| normalization_v2/engine.py、reporting.py | 编排、状态、验收、成本和发布 | 新增入口，不修改旧 CLI 的算法 |
| configs/normalization_v2/ | schema、通用政策、两领域词典及单位表 | 显式迁移旧 YAML 并记录差异 |
| scripts/normalize_registry_offline.py | 新离线 CLI | 明确源、目标、预算、stage 与 resume |
| web-ui/backend/normalization_service.py | 作业、状态、取消、租约和 profile | main.py/auth.py/providers.py/migrations.py |
| 前端数据库、提示包与作业界面 | 策略选择、词典校验、未决项和成本展示 | 复用现有 Providers/Prompts 架构 |
| tests/normalization_v2/ | 契约、科学反例、事务、增量与端到端 | 保留旧测试，不用新断言替换旧协议 |

第三方引用采用固定源码版本与许可证记录。设计可以独立实现；若复制 Apache-2.0 代码，保留必要版权与许可证说明。不得未经依赖审查把整个对照框架加入运行环境。

## 4. 数据契约

所有记录均有 schema_version，跨记录使用稳定 ID；标识、身份判定依据和展示文本分别保存。

| 记录／表 | 核心字段与约束 |
|---|---|
| source_documents | corpus_id、doc_id、revision_hash、active/superseded/withdrawn；一个文档一个活动版本 |
| extraction_batches | chunk_id/hash、model/profile、prompt/schema 哈希、finish 状态、response_hash、成功／失败；任务唯一 |
| mentions | mention_id、文档版本、chunk、局部编号、raw_name、kind、roles、粒度、明确属性、引文与偏移／定位状态 |
| alias_assertions | 两个原文名称、明确释义的来源 span、作用域、验证结果；不是无条件的全局 alias |
| canonical_entities | 不变 canonical_id、kind、granularity、可变展示名、provisional/confirmed/retired、父概念关系 |
| alias_bindings | 表面键及 normalizer、scope、guards、目标 ID、决策依据、有效版本；允许合法多义映射 |
| resolution_tasks | task_key、证据与候选快照、完整 registry/rules 快照引用、相关依赖子集哈希、profile/prompt 哈希、状态、attempts 和请求租约 |
| identity_decisions | 任务、输出、证据、适用范围、校验和 supersedes；追加保存，不覆盖历史 |
| mention_bindings | mention_id、canonical_id、binding_version、active、decision_id；可按来源撤回或拆分 |
| observations | observation_id、实验／局部范围、对象角色、指标、原值/规范值、范围、原单位/规范单位、来源 |
| facts | fact_id、关系类型、角色到 ID、条件、observations、否定/假设/实测性质、来源出现集合 |
| projection_outbox | 对象 ID、视图类型、期望内容哈希、目标 generation、pending/applied；幂等更新 |
| run_manifests | source/registry/rules/profile 版本、统计、预算、技术失败、未决项、索引一致性及保护哈希 |

### 4.1 身份与任务指纹

- canonical ID 不包含可变规范显示名；YAML ID 固定，新 ID 生成后持久保存并检查碰撞。
- mention ID 对文档版本、chunk 与局部实体槽唯一；重复导入同一成功批次不会重复出现。
- 临时身份创建键包含 kind、granularity、guards 和必要 scope。未知值单独表示，不能当作相等条件。
- task_key 包含相关身份证据和候选版本。仅相同文字但含义或作用域不同的任务不能复用。
- 完整快照用于运行复现；任务失效由相关词条／规则的依赖哈希决定。无关词条变更不能清空全部成功判断缓存；影响身份语义的政策升级必须使相关绑定重新验证。
- 非身份性上下文变化不应强迫已确认的通用 alias 重判；身份相关证据变化必须形成新版本。两者由模板显式声明。
- fact_id 保留关系角色、上下文和陈述性质。图结构桶 key 与完整事实 ID 是不同字段。

### 4.2 状态模型

解析输出：`resolved_dictionary`、`resolved_learned`、`resolved_document`、`resolved_llm`、`provisional_new`、`deferred_semantic`、`technical_failed`、`budget_deferred`。

作业阶段：`pending → running → completed`，或 `failed/cancelled/partial`。科学未决与技术状态分别统计；存在技术未完成或预算挂起时，不能标记全作业 completed。允许完成的科学未决必须携带来源、独立身份和原因，不得静默丢弃。

发布状态：`draft → validated → published`。读者只读取一个完整 generation；取消或崩溃后继续使用上一已发布 generation。

## 5. 工作包、依赖与交付物

### W01 基线、策略隔离与配置合同

依赖：已推送基线标签。决策：D01、D12、D13、D14。

- 建立新策略路由和 run_config 字段合同；覆盖旧参数无新字段时的全部兼容分支。
- 增加源／目标规范路径检查、目标锁、已发布缓存只读检查和新命名空间。
- 选定作业级冻结 profile 接口；新角色 normalization 的解析必须显式指定或显式选择已有 profile 的映射，不能借 QA 默认值悄悄切换建库渠道。
- 保存 schema/registry/rules/prompt/profile 哈希，并将其加入实例与作业缓存键，防止新旧实例串用。
- 输出兼容真值表测试和只读保护测试；保留原 66 项基线回归。

完成条件：缺省旧配置行为不变；显式 v2 不会调用旧在线或候选对引擎；冲突配置和目标覆盖在网络请求前拒绝。

### W02 声明式模板编译和两领域词典

依赖：W01。决策：D02、D03、D04、D08。

- 建立严格 schema：实体 kind、实验 role、粒度、identity_guards、普通名称／化学式正规化、alias 作用域、单位政策、关系角色、merge/index 投影。
- 为 flow_battery 与 pfas 提供完整的已知身份、缩写、负约束、复合材料及型号政策；从旧 YAML 迁移时生成逐项差异报告。
- 酸／离子／盐、通用概念／样品、价态、电荷、相态及型号有明确政策；没有领域依据的合并不自动继承旧 alias。
- 为歧义 alias 建立一对多索引及 scope/guard 过滤；拒绝冲突、悬空 ID、循环重定向、非法字段和单位定义。
- 编译得到抽取 schema、离线规则快照和索引字段合同；提示包发布时做同一套校验。

完成条件：两个领域编译、导出、重载指纹一致；Co/CO、VO²⁺/VO₂⁺、PFOA/PFOS、Nafion 型号及复合物反例通过；模板字段写错在建库前报错。

### W03 事务账本与来源版本

依赖：W01、W02。决策：D07、D09、D11。

- 实现第 4 节记录的 SQLite schema、索引、外键、事务、追加事件和幂等唯一约束。
- 独立 corpus 命名空间；运行数据库不加入 Git，不复用存密钥的 auth 数据库保存语料。
- 实现文档版本暂存、激活、撤回和恢复事件；新版本有效前不撤掉旧版本。
- 实现 outbox、generation 状态、进程退出与租约恢复、只读审计导出及 manifest。
- 导出原文／模型输出时脱敏；身份账本仅保存 profile 引用，不保存凭据。

完成条件：重复导入不增量；文档更新任一故障点崩溃后旧版本仍可读；重新运行收敛到单一活动版本；不能出现无来源的已确认绑定。

### W04 轻量抽取旁路与旧缓存导入

依赖：W01—W03。决策：D01、D02、D07、D13。

- 在现有实体/关系抽取成功后、聚合入图前落盘完整原始记录；v2 不进入在线判同 hook。
- 在同次抽取中保留原始名称、局部 ID、kind、roles、明确 alias 与必要 identity_guards；其余缺失允许为空。
- 不给抽取模型全库词表；不增加额外判同调用；保存原始单位及局部实验引用。
- 程序附加来源及版本，验证模型短引文和局部关系引用；多义 span 明确未定位，不猜偏移。
- 为现有单步、两步和合法空抽取提供适配；失败不生成伪成功空记录。
- 导入旧原文和完整成功的缓存响应，验证原 prompt/model/messages 映射与 chunk 一致；无法恢复的字段报告 unavailable。

完成条件：相同输入的抽取阶段数保持原合同；假响应／截断／不明引用不能完成；旧缓存导入不发网络请求，不修改原文件，不从聚合描述补造属性。

### W05 确定性解析与有限候选

依赖：W02—W04。决策：D03—D06、D09。

- 按 DESIGN 第 6 节执行词典、来源局部定义及已确认绑定优先流程。
- 相同作用域和完整相容依据可直接复用；未知保护属性不能把特定样品与家族概念视为完全相同。
- 无可信候选直接登记 provisional；分离 kind 与 role，避免 PTFE 仅因实验角色变化就拆成无关物质。
- 候选硬上限 5，无精确／化学式豁免；超过上限的歧义报告过宽原因并继续其他任务。
- 实现纯离线候选索引；共享组分产生关联，不生成材料桶内全组合；不新增身份候选专用 embedding。W08 的最终检索向量单独统计，不属于此零调用约束。
- 保存所有绑定路径、拦截理由、候选来源与未决项，不用隐藏的相似度阈值自动升级为同一。

完成条件：重复 mention 不重复决策；新无候选名称零 LLM；多义缩写不跨文档污染；修改身份保护字段会正确阻断旧绑定复用。

### W06 有界歧义判断与共享请求调度

依赖：W03、W05。决策：D05、D06、D09、D10。

- 一个唯一歧义任务携带至多 5 个候选和必要原文，返回 SAME_ID/NEW_ID/RELATED_VARIANT/UNCERTAIN。
- 严格检查候选 ID、scope、身份保护、原文 span、字段完整与完整 finish 状态；禁止模型自由造 ID。
- 输出预算依次 4096/8192/16384，有界重试；关闭 SDK 内部隐式重试，所有实际发送归调度器计数；技术失败保留原响应证据，成功任务不重复请求。
- 在 providers/model_profiles 增加 normalization 使用场景和显式 profile 绑定；保留既有 extraction/QA/judge 角色。
- 通过单一 worker/共享租约实现总请求及物理 key 上限；现有抽取、查询、embedding 与归一化入口共同接入，不能只限制新增角色。同 key 不因不同 profile、端点别名、限额配置、线程或 CLI/Web 作业获得额外并发。
- 记录真实请求、重试、usage 缺失、预算挂起；不同模型和规则下的任务不无条件命中。
- 模型确认的新 alias 先形成有作用域和证据的运行绑定，提供词典建议导出；不自动改写全局 YAML。

完成条件：完整 HTTP200 但截断、伪引文、错误身份、非法 ID 或模型自报高分都不能绕过校验；缓存与规则命中零租用；取消和崩溃释放租约；混合进程总峰值≤10、每物理 key≤1。

### W07 数值、角色事实与规范投影输入

依赖：W03、W05；存在歧义时接收 W06 结果。决策：D04、D07、D08、D09。

- 用确定性十进制和单位注册表处理标量／范围、量纲、百分比及前缀；原始表示始终保存。
- 指标概念、值和实验 occurrence 分层；不同来源同值不合成同一次实验。
- 保留目标、材料、条件、指标、机制等角色；方向、否定、假设/实测、实验范围影响事实签名。
- 建立独立 fact_store；旧 HypergraphDB 的成员集合边仅为结构聚合，保存 fact_ids，不充当完整事实主键。
- 无明确上下文的记录限制在来源局部范围，不跨 chunk 自动拼接不同实验。
- 对未解决身份保留原事实及 provisional 引用；不发明缺失端点，EFU repair=false。

完成条件：PFOA 去除/脱氟/矿化、CE/EE、不同温度/浓度/单位及角色交换全部保持区别；同义句的严格相同事实可聚合来源；模糊数值和缺失单位可追溯保留。

### W08 图、索引及增量发布

依赖：W03、W07。决策：D07、D08、D11、D12。

- 构建实体／fact_id 向量、结构桶、词法索引和来源回查；新增检索适配器恢复事实角色及原文。
- 投影签名包含文本、模型、维度、索引字段和格式版本；按哈希判断必要重嵌入。
- 增量处理新增／更新／撤回来源、alias 修订、身份合并与拆分、模板变化；计算受影响对象集合。
- outbox 任务幂等；临时索引／文件验收后原子切换 generation。文件、SQLite 和向量状态不一致时不得发布。
- 旧查询返回契约继续可读；v2 profile 必须通过适配器，旧缓存使用旧读取路径。

完成条件：重复运行零新增 API；仅来源增加但投影不变时零重嵌入；一次文献撤回只影响相关对象；任一发布故障后上一 generation 可用；所有矩阵维度正确、有限且非零。

### W09 CLI 与作业生命周期

依赖：W01—W08。决策：D09—D14。

规划 CLI 阶段：`import → resolve → judge → project → embed → validate → publish`；`all` 编排完整已有抽取数据的后处理，不能暗中重新抽取原文。

- 参数包括源、独立目标、registry/profile、model_profile_id、预算、resume、预期文档/块数和 offline-only。
- 新抽取由现有 builder 的显式 v2 配置运行；与后处理 CLI 分开统计与审计。
- 提供 dry-run 影响集合、stage 状态、错误恢复、取消、绑定修订及词典建议导出。
- 缺预算或 profile 时不自动调用模型；技术失败时保留成功 checkpoint，stage all 不能跳过失败后发布。
- 提供来源 update/withdraw 和规则 rebind 命令，先校验新 generation，再进行激活。

完成条件：任一阶段中断重启只完成缺项；不能同时启动同一目标作业；CLI 返回码、状态和 manifest 一致。

### W10 Web、提示包与模型配置集成

依赖：W01、W02、W06、W09。决策：D01、D03、D10、D12、D13。

- 在 API/前端增加显式策略选择，保留旧在线、旧离线及关闭选项；v2 展示为独立离线处理。
- 提示包版本关联抽取 schema、registry/policy 快照与内容哈希；创建和发布均运行 W02 编译校验。
- 作业 API 支持创建、预检、启动、进度、取消、resume、验证与发布；鉴权和所有权校验沿用现有 auth 框架。
- 页面显示词典命中、provisional、科学未决、技术失败、请求预算、实际使用、受影响对象和发布 generation。
- profile 选择显式记录模型、渠道、参数及限额；不在响应、日志、YAML 或 manifest 回显凭据。
- 同一进程中的多数据库实例缓存必须包含策略及版本；已发布 case1/case2 仍由 cache_runtime 的锁定配置读取。

完成条件：UI/CLI 生成等价的冻结作业配置；不同用户不能改彼此词典／作业；切换 UI 策略不会重写已有缓存或静默启动旧在线归一化。

### W11 兼容导入、科学准确性与成本对照

依赖：W04—W10。决策：D13、D15—D18。

两条证据轨道分开：

1. **既有数据离线轨道**：复用完整原始成功抽取，导入并比较身份、候选与影响集合；不重发成功抽取/判断，不将模拟请求数称真实成本。
2. **冻结新增样本轨道**：选用未发生重复成功调用的独立样本，在显式预算与同模型、同采样、同语料范围下比较抽取字段开销和归一化真实使用。样本、规则与判定协议在请求前冻结，不能用结果倒调规则。

评估集覆盖两个子领域、别名、未知新词、文档多义缩写、价态、电荷、相态、型号、复合物、样品、数值单位和来源更新。与词典制定样本隔离，来源及专家／可验证身份依据可追溯。旧 LLM 判断只能作为有来源的参照，不能充当独立真值。

指标与分母：

- 错合并率＝独立复核判错的合并数／被复核的合并数；高风险反例单列。
- 漏合并率＝应合并却未归并的对数／独立真值中的应合并对数。
- 未决率＝provisional/deferred_semantic 记录数／全部合格解析记录数，按类别、领域和来源分层。
- 字典／已确认绑定命中率、唯一歧义任务数、每任务候选数及过宽桶数。
- 真实请求、重试、输入／输出 token、推理 usage、总时长及 embedding 调用；缺失 usage 单列。
- 总成本包含新抽取字段和后处理，不仅比较归一化请求数；同价目快照下计算金额，缺价目时不报金额结论。
- 文档更新、撤回及重绑定的受影响对象数、重嵌入数、恢复时间与无关对象哈希不变。

独立冻结的统计协议需在运行前确定采样、分层、置信区间与非劣界；不能在看到系统排名后改变界限。高风险确定性反例要求零错合并；真实准确性和总成本结论必须由独立样本支持。证据不足时标记未通过，不以“模型自审通过”宣称科学验收完成。

按用户授权，需要人工科学裁决的项保留、列明原因并继续其他项；跨方案比较使用共同有效子集，同时报告完整分母与排除项，不能通过增加未决项虚构成本优势。

### W12 完整验收、发布与旧方案恢复演练

依赖：W01—W11。决策：D12、D14—D18。

- 执行 ACCEPTANCE.yaml 的全部门槛及决策追踪，交付机器报告和可读对照。
- 从干净 Git 基线检查旧离线核心、脚本及测试可导入；旧语料/密钥/缓存另按数据恢复说明准备，不能声称 Git 包含私有数据。
- 记录已验收旧文件保护清单，验证旧配置、缓存、图、向量和论文结果哈希不变。
- 打包必要源码／配置／小型报告及 SHA256，禁止整项目或嵌套旧备份复制。
- 文档包括新旧入口、词典维护、作用域、撤回、故障恢复、预算及发布说明。
- 新方案默认启用必须同时满足完整功能、兼容、独立科学质量和成本证据。未通过时保留双方案，明确状态，不自动改默认。

完成条件：所有 gate 有可定位证据；报告可离线重算；Git 分支、标签和运行 manifest 一致；没有将未完成项隐藏为完成。

## 6. 必测场景矩阵

| 类别 | 关键反例／故障 | 预期 |
|---|---|---|
| 字符与类型 | 大小写、上下标、Co/CO、VO²⁺/VO₂⁺ | 按种类安全匹配，身份区别保留 |
| 别名与作用域 | BTO 在不同文档不同释义、Sample A 跨文档 | 正确局部绑定；不采用 first-wins |
| 化学身份 | PFOA/PFOS、酸/盐/离子、型号、复合物及相态 | 显式政策，关联不等于同一 |
| 已知与未知 | 多次已知 alias、新名称无候选、疑似 alias | 已知零判断请求；无候选登记；疑点有界 |
| 抽取失败 | 空正文、合法空实体、截断、JSON错误、局部 ID 缺失 | 合法空可核验，其余不伪装完成 |
| 数值事实 | 去除/脱氟/矿化、95%/0.95、mg/L/μg/L、不同条件 | 指标、量纲、范围和来源完整保留 |
| 图关系 | 相同成员不同角色、方向、否定、假设/实测 | 不同 fact_id；结构桶不吞事实 |
| 来源更新 | 新版本抽取失败、撤回共享来源、恢复旧版本 | 旧 generation 可读，只重算依赖对象 |
| 身份修订 | 合并后拆分、alias 撤销、显示名变化 | mention 可回溯；ID不因展示名变化 |
| 请求恢复 | HTTP200截断、超时、取消、预算耗尽 | 有界重试；成功保留；技术未完成单列 |
| 并发 | CLI/Web/不同角色复用同 key、多进程 | 总≤10、key≤1，无重复任务租用 |
| 索引恢复 | 图已写向量失败、outbox重放、模型维度变化 | 不发布混合版本；签名失配明确拒绝 |
| 旧方案 | 旧 CLI、旧缺省配置、已发布缓存只读 | 行为与保护哈希保持 |

## 7. 变更控制与状态汇报

每个实现提交标注 Wxx 和 Dxx；测试或报告标注 Gxx。任何架构调整必须新增 ADR，说明原因、证据、影响的数据与协议、回退方式，并同步设计、决策和验收文件。

工程参数在首次运行前冻结。跨身份粒度、自动别名晋升、在线归一化、无界候选、模型渠道、旧缓存覆盖和默认策略改变属于实质变更，不能当作常规实现细节静默处理。

进度报告区分：源码完成、离线保护通过、真实端到端通过、科学质量通过、成本通过、发布完成。文档写好、单元测试通过或 HTTP200 都不足以单独宣布新方案完成。
