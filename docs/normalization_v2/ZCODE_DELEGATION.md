# ZCODE CLI 编码委派

## 本机入口与指定供应商

- CLI：`D:\zcode\resources\glm\zcode.cjs`，已实测版本 `0.16.9`。
- Node：`C:\Program Files\nodejs\node.exe`。不依赖 ZCODE 已加入 PATH。
- 本轮唯一授权上游：`https://api.treeapi.online/v1`。
- 模型：`deepseek-v4.1-flash`，`reasoning_effort=low`。
- 凭据从用户已有的私有 ZCODE provider 配置读取，不写入仓库、提示文件或命令行。

可复用启动器为 `scripts/run_zcode_delegate.py`。它验证 provider 的实际 endpoint/model，给子进程使用独立临时配置和本机中继令牌。真实上游 key 由父进程中继使用；本机中继同时接入跨进程物理 key 请求租用。这个隔离方式不等于操作系统文件沙箱，委派产出仍须审查。

## 调用方式

先准备只包含任务、允许修改文件、验收条件的提示文件。会话输出目录放在源码目录之外，例如 D 盘工作区。

```powershell
& 'C:\Users\19855\AppData\Local\Programs\Python\Python312\python.exe' `
  scripts/run_zcode_delegate.py `
  --cwd 'C:\Users\19855\Desktop\Hyper-rag\hyper-gragh' `
  --provider-id '<已有私有配置中的 provider ID>' `
  --prompt-file 'D:\work\task.txt' `
  --run-dir 'D:\work\zcode-run-001' `
  --max-requests 30 --timeout 1800
```

不要把 API key 当作参数，也不要把完整私有 provider 配置复制到仓库。启动器不改用户默认供应商配置。

## 本轮实测与产出

1. 单次探针返回指定模型的完整 `stop` 响应，实际请求 1 次。
2. 第一轮委派产出契约、文本政策、编译器及词典初稿，触及预先设置的 60 请求上限，退出非零。
3. 定向补完产出额外契约测试并修正词典冲突；20 次实际请求后发生本机中继连接超时，退出非零。

两轮编码委派不能记作成功完成的独立验收。父代理接手后修复了 guards 类型比较、未复核别名误入可信索引、角色成员去重、明确歧义声明及科学词典混同，并运行本仓库测试。科学 API 建库、身份评测及旧语料重抽取未因这些编码调用而启动。

最初的 81 次请求由旧委派启动器的单 key 串行中继记录，峰值为 1；不能把这份历史记录说成已通过全项目混合角色的生产调度验收。当前提交中的可复用启动器已接入共享 broker，相关 broker 测试为离线跨进程测试。

原始会话和安全请求日志保存在本机 D 盘 `normalization_v2_zcode` 工作区，未提交到 Git。仓库只保存可复用代码、聚合实测说明和检查结果。
