# HyperChE 服务器部署

本仓库的生产部署只带 `web-ui/backend/hyperrag_cache/case1` 这一套较小的公开示例缓存。
`hyper_base`、`hyper_chem` 以及实验缓存不会被 Docker 镜像打包，也不会作为部署缓存使用。

## 一、服务器准备

推荐使用 Linux + Docker Compose。服务器需要安装：

- Git
- Git LFS
- Docker Engine
- Docker Compose v2（命令是 `docker compose`）

## 二、拉取指定分支

```bash
git lfs install
git clone -b codex/full-project-transfer-20260801 https://github.com/FallRain0905/hyper-gragh.git
cd hyper-gragh
git lfs pull
```

如果服务器已经有旧仓库：

```bash
cd /opt/hyper-gragh
git fetch origin codex/full-project-transfer-20260801
git switch -C codex/full-project-transfer-20260801 FETCH_HEAD
git lfs pull
```

确认缓存文件不是 LFS 指针：

```bash
git lfs ls-files | grep 'web-ui/backend/hyperrag_cache/case1'
ls -lh web-ui/backend/hyperrag_cache/case1
```

`case1` 的 7 个文件总大小约 331 MB，首次拉取和构建需要一些时间。

## 三、创建服务器配置

进入 Web UI 目录：

```bash
cd /opt/hyper-gragh/web-ui
cp backend/settings.example.json backend/settings.json
cp .env.example .env
```

编辑 `backend/settings.json`，至少填写：

- `apiKey`：LLM API Key
- `baseUrl`：LLM 的 OpenAI 兼容 API 根地址，例如 `https://api.siliconflow.cn/v1`
- `modelName`：LLM 模型名
- `embeddingApiKey`：Embedding API Key
- `embeddingBaseUrl`：Embedding API 根地址
- `embeddingModel`：Embedding 模型名

注意：`baseUrl` 和 `embeddingBaseUrl` 填 API 根地址，不要填 `/chat/completions`、`/completions`、`/embedding` 或 `/embeddings`。

生成并填写两个随机密钥：

```bash
JWT_SECRET=$(openssl rand -hex 32)
APP_SECRET_KEY=$(openssl rand -hex 32)
printf 'WEB_PORT=5000\nJWT_SECRET=%s\nAPP_SECRET_KEY=%s\n' "$JWT_SECRET" "$APP_SECRET_KEY" > .env
chmod 600 .env backend/settings.json
```

如果要覆盖默认管理员，可以继续在 `.env` 中设置：

```dotenv
HYPERCHE_ADMIN_EMAIL=your-admin@example.com
HYPERCHE_ADMIN_PASSWORD=change-this-password
```

默认管理员账号仍由后端初始化逻辑创建；首次上线后建议立即修改密码或通过环境变量覆盖。

## 四、构建并启动

在 `web-ui` 目录执行：

```bash
docker compose up -d --build
```

查看状态和日志：

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f nginx
```

健康检查：

```bash
curl http://127.0.0.1:5000/health
```

浏览器访问：

```text
http://服务器IP:5000/
```

如果服务器前面已有 Nginx、Caddy 或 Traefik，可以将 `WEB_PORT` 改成仅监听本机的端口，并由外层反向代理到该端口。

## 五、更新版本

```bash
cd /opt/hyper-gragh
git fetch origin codex/full-project-transfer-20260801
git switch codex/full-project-transfer-20260801
git pull --ff-only origin codex/full-project-transfer-20260801
git lfs pull
cd web-ui
docker compose up -d --build
```

`settings.json` 不在 Git 中，更新代码不会覆盖服务器上的 API 配置。数据库、上传文件和知识库使用 Docker named volumes 持久化。

## 六、停止和备份

```bash
cd /opt/hyper-gragh/web-ui
docker compose down
```

停止容器不会删除 named volumes。删除容器前建议备份运行数据：

```bash
docker run --rm \
  -v hyperche_runtime:/source:ro \
  -v "$PWD":/backup \
  alpine tar czf /backup/hyperche-runtime-backup.tgz -C /source .
```

不要执行 `docker compose down -v`，除非确认要删除用户、额度、个人 API 配置和上传数据。
