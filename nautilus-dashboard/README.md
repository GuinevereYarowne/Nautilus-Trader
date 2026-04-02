# Nautilus Trader — Dashboard (nautilus-dashboard)

这是一个用于展示 Nautilus Trader 市场数据的演示型 Web 仪表盘（K 线 + 成交量 + 状态监控）。

目录结构（相关）

- `backend/` — FastAPI 后端，提供 `GET /api/klines`、`GET /api/status` 和 `ws /ws/trades`。
- `frontend/` — React (Create React App) 前端，使用 ECharts 渲染图表。
- `docker-compose.yml` — 用于一键构建并启动前后端容器。

前提条件

- 本地运行：
  - Python 3.8+
  - Node 16+/npm
- Docker (用于容器化部署)

本地开发（推荐）

1. 后端

```powershell
cd nautilus-dashboard/backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # PowerShell
pip install -r requirements.txt
# 启动 (开发模式)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

访问测试：

```powershell
curl http://localhost:8000/api/status
curl http://localhost:8000/api/klines?limit=100
```

2. 前端

```powershell
cd nautilus-dashboard/frontend
npm install
npm start
```

打开浏览器： `http://localhost:3000`（若使用 dev server）

使用 Docker Compose（推荐一键启动）

在仓库根目录运行：

```bash
cd nautilus-dashboard
docker-compose up --build
```

服务启动后：

- 后端： `http://localhost:8000`
- 前端： `http://localhost:3000` （由 nginx 提供静态文件）

快速故障排查

- 如果前端页面空白或没有数据：检查浏览器控制台（F12）和 Network，确认 `/api/klines` 与 WebSocket `ws://localhost:8000/ws/trades` 是否可访问。
- 如果端口被占用：使用 `netstat -aon | findstr 8000` 找出 PID 并结束进程或修改端口。
- 如果 Docker 构建失败：确保主机网络通畅且 Docker Desktop 运行，查看 `docker-compose logs` 获取错误信息。

如何对接真实 Nautilus Trader 数据（概述）

1. 推荐做法：在 Nautilus 运行环境中，把行情数据（Bar/Trade/Quote）通过 HTTP 或 Redis 发布到本仪表盘后端（示例接口：`POST /ingest` 或写入 Redis list），后台服务读取并缓存至 `/api/klines` 与 WebSocket 推送。
2. 也可把仪表盘部署为 Nautilus 的一个扩展模块，直接订阅其内部消息总线并转发到前端。

安全与生产部署（建议）

- 在生产环境，替换 `nginx` 配置以加入 TLS（反向代理）和安全头。
- 对 WebSocket 使用反向代理（如 nginx 或 Traefik）并配置心跳与重连策略。

如果你需要，我可以：

- 添加 `start.ps1`/`start.sh` 一键脚本；
- 把后端改为读取真实 Nautilus 数据的示例适配器；
- 或把 Docker Compose 增强为 production-ready（TLS、环境变量、持久卷）。
