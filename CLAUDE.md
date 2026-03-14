# 🤖 Claude Code 项目导航

> **给 Claude 的快速索引**：这个文档优先级最高，初始化时先读这个！

## 📁 核心目录结构

```
xiaozhi-esp32-server/
├── main/
│   ├── xiaozhi-server/          # Python AI 引擎
│   │   ├── app/
│   │   │   ├── websocket/       # WebSocket 连接管理
│   │   │   ├── services/        # AI 服务（ASR/TTS/LLM）
│   │   │   └── config/          # 配置管理
│   │   ├── requirements.txt     # Python 依赖
│   │   └── main.py              # 入口文件
│   │
│   ├── manager-api/             # Java Spring Boot 后端
│   │   ├── src/main/java/
│   │   │   └── com/**/
│   │   │       ├── controller/  # REST API
│   │   │       ├── service/     # 业务逻辑
│   │   │       ├── entity/      # 数据模型
│   │   │       └── mapper/      # MyBatis Mapper
│   │   └── pom.xml              # Maven 依赖
│   │
│   ├── manager-web/             # Vue.js 前端
│   │   ├── src/
│   │   │   ├── views/           # 页面组件
│   │   │   ├��─ components/      # 通用组件
│   │   │   ├── api/             # API 调用
│   │   │   └── router/          # 路由配置
│   │   └── package.json         # npm 依赖
│   │
│   └── manager-mobile/          # uni-app 移动端
│       └── (类似 manager-web 结构)
│
├── docker-setup.sh              # 一键部署脚本
├── Dockerfile-*                 # Docker 镜像定义
└── README.md                    # 主文档
```

## 🔑 关键入口文件

| 模块 | 入口文件 | 作用 |
|------|---------|------|
| Python AI | `main/xiaozhi-server/main.py` | 启动 WebSocket 服务器 |
| Java 后端 | `main/manager-api/src/main/java/**/Application.java` | Spring Boot 启动类 |
| Vue 前端 | `main/manager-web/src/main.js` | Vue 应用入口 |
| 部署 | `docker-setup.sh` | Docker Compose 自动化脚本 |

## 🚀 快速开始命令

### 查看项目概览
```bash
@workspace 这个项目的核心功能是什么？各模块如何协作？
```

### 查看某个模块
```bash
# Python AI 引擎
@workspace main/xiaozhi-server 的 WebSocket 如何处理音频流？

# Java 后端
@workspace manager-api 有哪些 REST API？

# Vue 前端
@workspace manager-web 的主要页面有哪些？
```

### 调试问题
```bash
# 附上日志
@workspace 我的 xiaozhi-server 报错 [错误信息]，如何修复？
```

## 📚 重要概念

### 数据流
```
ESP32 设备 → WebSocket → xiaozhi-server (Python) → AI 服务 (ASR/LLM/TTS)
                                    ↓
                            manager-api (Java)
                                    ↓
                            manager-web (Vue)
```

### AI 服务集成
- **ASR**（语音识别）: 支持阿里云/讯飞/本地 Whisper
- **LLM**（大模型）: 支持 OpenAI/Claude/Qwen
- **TTS**（语音合成）: 支持多种云服务

### 配置文件
- Python: `main/xiaozhi-server/config.yaml`
- Java: `main/manager-api/src/main/resources/application.yml`
- Vue: `main/manager-web/.env.production`

## ❓ 常见问题速查

| 问题 | 查看文件 |
|------|---------|
| 如何添加新的 AI 模型 | `main/xiaozhi-server/app/services/llm/` |
| 如何修改 API 接口 | `main/manager-api/src/main/java/**/controller/` |
| 如何调整前端 UI | `main/manager-web/src/views/` |
| 如何部署 | `docker-setup.sh` + `README.md` |

## 🎯 优化建议

1. **精确提问**: 说明模块名（xiaozhi-server/manager-api/manager-web）
2. **提供上下文**: 附上错误日志或相关配置
3. **分步骤**: 复杂任务拆成多个小问题

Xiaozhi ESP32 Server - Claude Code 规则

## 项目架构
- **xiaozhi-server**: Python AI 引擎（WebSocket + ASR/TTS/LLM）
- **manager-api**: Java Spring Boot 管理后端
- **manager-web**: Vue.js Web 前端
- **manager-mobile**: uni-app 移动端

## 技术栈约定
- Python: 使用 asyncio、websockets、pydantic
- Java: Spring Boot 3.x, MyBatis, MySQL
- Vue: Vue 3 + Vite + Element Plus
- 部署: Docker Compose

## 代码规范
- Python: 遵循 PEP 8，使用类型注解
- JavaScript/Vue: ESLint + Prettier
- Java: 遵循 Google Java Style

## 开发流程
1. 所有功能先在本地测试，再部署 Docker
2. API 修改需同步更新 manager-api 和 xiaozhi-server
3. 前端组件优先使用 Element Plus

## 常见任务
- 添加新 AI 模型: 修改 `main/xiaozhi-server/app/services/llm/`
- 添加设备控制: 修改 `main/manager-api/src/main/java/com/**.controller/`
- 修改 UI: `main/manager-web/src/views/`

## 提问建议
- 问"如何添加 X 功能"时，说明要改哪个模块（Python/Java/Vue）
- 问代码位置时，先说明是"前端"/"后端"/"AI 引擎"
- 提供错误信息时，附上完整的日志栈

## 快捷命令
- `@arch`: 解释整体架构 → 读取 CLAUDE_GUIDE.md
- `@deploy`: 部署步骤 → 读取 docker-setup.sh + README.md
- `@api`: 查看 API 列表 → 扫描 manager-api/controller

## 项目术语
- **小智**: 指 ESP32 智能音箱硬件
- **AI 引擎**: 指 xiaozhi-server (Python 后端)
- **管理端**: 指 manager-api + manager-web
- **VAD**: Voice Activity Detection (语音活动检测)

## 开发环境
- **操作系统**: Windows + WSL2 (Ubuntu) + Docker Desktop
- **代码位置**: WSL Ubuntu  (`/home/li/xiaozhi/xiaozhi-esp32-server`)
- **IDE**: VS Code (Windows) 连接 WSL 进行开发
- **ESP32 设备**: 无名科技 1.54 寸 ESP32-S3 (WiFi 版)
- **串口设备**: `/dev/ttyUSB*` (USB 转 TTL，C 口连接)

## 硬件配置
- **设备型号**: xingzhi-cube-1.54tft-wifi
- **MAC 地址**: 98:88:e0:16:3e:e8
- **固件版本**: 1.9.4
- **OTA 地址**: `http://192.168.1.105:8102/ota/`
- **部署 IP**: 192.168.1.105

## 端口映射
| 宿主机端口 | 容器端口 | 用途 |
|-----------|---------|------|
| 8100 | 8000 | WebSocket (音频流) |
| 8101 | 8002 | 智控台 Web UI |
| 8102 | 8003 | manager-api 后端 |
| 3307 | 3306 | MySQL |
| 6380 | 6379 | Redis |
## 🚀 本地运行指南（源码模式）

### 适用场景
- 开发调试 Python AI 引擎
- 不依赖 Docker 容器快速测试
- 需要查看 AI 服务详细日志

### 运行步骤

**1. 停止占用端口的 Docker 容器**
```bash
docker stop xiaozhi-esp32-server-web
lsof -i :8000  # 验证端口已释放
```

**2. 修改配置文件**
编辑 `main/xiaozhi-server/data/.config.yaml`：
```yaml
read_config_from_api: false  # 关闭从 API 读取配置
manager-api:
  # url: http://xiaozhi-esp32-server-web:8002/xiaozhi  # 注释此行
  secret: local-dev-secret-key
server:
  auth_key: local-dev-auth-key  # 添加认证密钥
```

**3. 启动服务**
```bash
cd /home/li/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server
source ../../venv/bin/activate
python3 app.py
```

**4. 后台运行**
```bash
nohup python3 app.py > /dev/null 2>&1 &
# 查看进程
ps aux | grep "python3 app.py"
# 停止服务
pkill -f "python3 app.py"
```

### 运行模式对比
| 配置项 | 容器模式 | 本地开发模式 |
|--------|----------|--------------|
| read_config_from_api | true | false |
| manager-api.url | 容器地址 | 注释掉 |
| 配置来源 | Java 后端 API | 本地 YAML 文件 |
| 智控台支持 | ✅ 支持 | ❌ 不支持 |

### 常见问题
| 问题 | 解决方案 |
|------|---------|
| `auth_key` 错误 | 在 `.config.yaml` 中添加 `server.auth_key` |
| 端口被占用 | `docker stop` 停止容器或修改 `server.port` |
| `loguru` 模块未找到 | 使用虚拟环境：`source ../../venv/bin/activate` |
| LLM API key 未设置 | 在 `config.yaml` 中配置正确的 API key |
