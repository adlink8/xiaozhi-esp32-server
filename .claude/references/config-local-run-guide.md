# 本地运行配置指南

> 本文档说明如何在本地源码运行 xiaozhi-server，无需 Docker 容器

## 快速开始

### 1. 停止占用端口的 Docker 容器

本地运行前，需要先停止占用端口的 Docker 容器：

```bash
# 停止占用 8102 端口的容器（manager-api）
docker stop xiaozhi-esp32-server-web

# 可选：停止所有相关容器
docker-compose -f main/xiaozhi-server/docker-compose_all.yml down

# 验证端口已释放
lsof -i :8102  # 无输出表示端口已释放
```

### 2. 修改配置文件

编辑 `main/xiaozhi-server/data/.config.yaml`：

```yaml
# 关闭从 API 读取配置
read_config_from_api: false

# 注释掉 manager-api 的 url（关键步骤）
manager-api:
  # url: http://xiaozhi-esp32-server-web:8002/xiaozhi  # 注释此行
  secret: local-dev-secret-key
```

### 2. 启动服务

```bash
cd /home/li/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server
../venv/bin/python app.py
```

### 3. 验证运行

查看日志输出：
```
Websocket 地址是 ws://<SERVER_IP>:8100/xiaozhi/v1/
视觉分析接口是 http://<SERVER_IP>:8102/mcp/vision/explain
```

## 配置说明

### 运行模式对比

| 配置项 | 容器模式 | 本地开发模式 |
|--------|----------|--------------|
| read_config_from_api | true | false |
| manager-api.url | 容器地址 | 注释掉 |
| 配置来源 | Java 后端 API | 本地 YAML 文件 |
| 智控台支持 | ✅ 支持 | ❌ 不支持 |
| 适用场景 | 生产部署 | 开发调试 |

### 关键配置项

```yaml
# 1. read_config_from_api: false
#    作用：关闭从 manager-api 动态读取配置
#    原因：本地运行时 manager-api 容器可能未启动

# 2. manager-api.url: 注释掉
#    作用：阻止配置加载器尝试连接 API
#    原因：config_loader.py 第 34 行检查 url 是否存在

# 3. server.port: 8000
#    作用：WebSocket 服务监听端口（容器内）
#    注意：本地运行时可能需要修改为其他端口避免冲突
```

## 常见问题

### 问题 1：启动时报 API 请求失败

```
POST /config/server-base 异步请求失败
httpx.HTTPStatusError: 502 Bad Gateway
```

**原因**：`manager-api.url` 未注释，程序尝试连接不存在的容器服务

**解决**：
```yaml
# 注释掉 url 行
# url: http://xiaozhi-esp32-server-web:8002/xiaozhi
```

### 问题 2：设备连接报认证失败

```
E (129265) WS: Missing message type, data: 认证失败
```

**原因**：`server.auth.enabled` 为 true，但设备未携带 token

**解决**：在 `config.yaml` 中关闭认证
```yaml
server:
  auth:
    enabled: false
```

### 问题 3：端口被占用

```
OSError: [Errno 98] Address already in use
```

**原因**：Docker 容器或其他进程占用了 8000 端口

**解决**：修改端口配置
```yaml
server:
  port: 8001  # 改为其他可用端口
```

## 硬件连接地址

本地运行时，设备端 WebSocket 地址：

```
ws://<SERVER_IP>:8100/xiaozhi/v1/
```

- IP：宿主机 IP（<SERVER_IP>）
- 端口：Docker 映射端口（8100 → 容器内 8000）
- 路径：`/xiaozhi/v1/`

## 相关技能文件

- `/skills/simplify`: 代码审查和优化技能
- `/skills/claud-api`: API 构建相关

## 参考文件

- 主配置文件：`main/xiaozhi-server/config.yaml`
- 本地覆盖配置：`main/xiaozhi-server/data/.config.yaml`
- 配置加载器：`main/xiaozhi-server/config/config_loader.py`
- API 客户端：`main/xiaozhi-server/config/manage_api_client.py`
