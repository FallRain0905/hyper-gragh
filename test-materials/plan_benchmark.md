# Hyper-ChE Flow Battery Benchmark 生成计划

## 任务概述
生成10篇英文长文档（每篇2500-3500词）+ 200-300条gold EFU + 200+条gold facts + 40-60条QA questions

## 执行批次

### Batch 1: 并行生成 Doc 01-05
- 每个agent负责一篇完整文档+annotations
- 5个agent并行

### Batch 2: 并行生成 Doc 06-10  
- 每个agent负责一篇完整文档+annotations
- 5个agent并行

### Batch 3: 组装
- 合并所有文档到最终JSON格式
- 验证canonical_id一致性
- 输出corpus_documents.md + gold_annotations.json
