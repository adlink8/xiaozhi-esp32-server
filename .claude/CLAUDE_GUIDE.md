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