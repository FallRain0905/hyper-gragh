# 完整计划实施状态

日期：2026-10-19。分支：`codex/normalization-registry-implementation-20261019`。

**当前是可审查的实现进度提交，完整 v2 尚未验收或替换默认方案。** DESIGN/DECISIONS/ACCEPTANCE 中的完整目标继续有效；没有取消 Web、旧数据导入、独立质量和总成本门槛，也没有将本进度提交作为 MVP 发布。

## 已实现并测试的代码

| 范围 | 当前证据 | 尚缺内容 |
|---|---|---|
| 策略和契约 | 旧缺省配置保持原义；独立 v2 schema、来源/目标检查；严格 JSON/finish/span/局部引用 | 现有 builder 的完整显式策略适配 |
| 声明式词典 | 两领域及通用/单位配置；编译、导出重载；作用域/guards/显式歧义；相关依赖哈希 | 独立科学参考集核验；维护 UI |
| 来源账本 | 独立 SQLite、原始批次、追加决策/绑定、来源版本、撤回、事件链、outbox/generation | 完整运维/迁移故障演练 |
| 轻量抽取旁路 | 无网络的响应适配器；程序赋来源；未定位 span 明示；不调用判同 | builder 单步/两步实接；旧成功缓存的可验证导入收据 |
| 词典优先解析 | 词典/有作用域学习映射、临时身份、纯词法候选；上限 5；不做身份候选嵌入 | 来源显式定义的完整核验/绑定路径；规则修订的操作界面 |
| 判断 | 显式 profile，4096/8192/16384，最多 3 次且跨 resume 保留；严格候选/引文；成功复用；预算与科学未决分离 | 全项目旧请求入口/SDK 重试全面接入与实测 |
| 请求租用 | 全局物理 key SQLite broker；跨进程/角色与取消/死进程恢复测试；现有 QA limiter 接入 | 旧抽取/构建/独立评测脚本全部接入前，不能声称生产全覆盖 |
| 数值和事实 | 十进制与明确单位；原始值/未解项保留；实验 occurrence；角色、顺序、重数、条件、极性、陈述性质参与事实 ID | 新旧实际语料上的独立科学核验 |
| 图与检索投影 | 独立 fact_store/结构桶；双文本、BM25/稠密 RRF；内容签名向量断点；原子指针；原文回查 | Web 查询适配和现有完整检索参数集接入 |
| CLI | 显式 import/resolve/judge/project/embed/validate/publish/all；目标独占租用；离线默认零 API；未完成返回非零 | update/withdraw/rebind/impact/取消的完整命令族及 Web 生命周期 |
| Web/profile/提示包 | 仅现有 QA limiter 增加共享 broker；新 CLI profile 严格独立 | normalization 角色 UI、作业 API、所有权和提示包版本发布 |
| 科学质量/成本/最终发布 | 保留全部门槛；未执行新语料建库/真实成本对照 | W11 与 W12 全部证据；没有默认切换 |

## 本次回归

```text
python -m pytest tests/normalization_v2 \
  tests/test_posthoc_normalization.py tests/test_final_cache.py \
  tests/test_pfas_final_cache.py tests/test_pfas_cluster_recovery.py \
  tests/test_pfas_posthoc_transport.py tests/test_published_cache_runtime.py \
  tests/test_qa_runtime_requests.py -q
```

结果：**164 passed**，含 98 项新增测试与原有 66 项选定回归；保留一条已有 Pydantic 弃用警告。测试使用的确定性嵌入仅存在于测试夹具，生产 CLI 没有伪向量回退。完整响应已校验但身份事务失败时，从已保存的成功响应恢复，不重新调用模型。

这证明列出的离线保护与模拟恢复场景，不代表真实身份准确性、全量 Web 流程、所有原项目测试或总成本已经通过。具体范围见 `implementation_checks.json`。

## 科学种子与迁移

- 种子是机器整理/代码审查状态，不冒充独立人工金标准。
- 对原两个 YAML 的 312 条名称记录逐项登记于 `migration_dispositions.json`：224 条存在种子对应，26 条身份拆分，24 条仅作候选，38 条不进入可信词典。
- 这些数量是映射库存，不是准确率或节约成本。移除危险别名不改变旧 YAML 或旧实验结果。
- 裸 PFOA/PFOS/PFBA/PFBS 保留形式未指定的概念；明确酸与阴离子身份分开。去除、降解、脱氟、矿化和速率/效率不互作无条件别名。
- 不明研究范围的 Sample A、C-C 等标签不进行跨来源的全球身份绑定。

## 新 CLI 的安全使用范围

`scripts/normalize_registry_offline.py --stage compile` 只做本地编译。输入导入必须为已通过契约校验的 RawBatch JSONL；它目前**不能**直接把旧聚合图或缺少完整来源证据的旧 LLM 缓存当作成功 RawBatch。

所有 API 默认为关闭；需要显式 normalization/embedding profile、`--allow-api` 和独立请求预算。API key 只通过 profile 指定的环境变量读取，不能写在 JSON 中。缺少判断或向量时 `all` 返回 partial，不发布伪完成结果。

本提交不重建或改写 case1/case2 的成功缓存、图、向量、run_config、题集和论文结果。旧方案恢复仍使用 `normalization-legacy-20261019`。
