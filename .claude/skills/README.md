# xiaozhi-esp32-server 故障诊断技能索引

> 📚 **统一诊断手册**：[Problems.md](./Problems.md) - 包含所有故障诊断技能的完整文档

---

## 技能分类

### 🔐 认证与配置问题

| 技能 | 适用场景 | 详细文档 |
|------|----------|----------|
| [server-secret-mismatch](#server-secret-mismatch) | 无效的服务器密钥、API 认证失败、容器启动失败 | [Problems.md](./Problems.md#server-secret-mismatch) |
| [ota-404-fix](#ota-404-fix) | OTA 接口返回 404 错误、context-path 配置问题 | [Problems.md](./Problems.md#ota-404-fix) |
| [ota-connection-error](#ota-connection-error) | OTA 接口无法连接、ESP32 设备激活失败 | [Problems.md](./Problems.md#ota-connection-error) |
| [server-ota-config](#server-ota-config) | server.ota 参数配置、IP 变更更新、Redis 缓存清理 | [Problems.md](./Problems.md#server-ota-config) |

### 🔌 容器与网络问题

| 技能 | 适用场景 | 详细文档 |
|------|----------|----------|
| [container-port-mapping](#container-port-mapping) | 端口映射错误、容器间网络通信、服务无法访问 | [Problems.md](./Problems.md#container-port-mapping) |

### 📥 OTA 升级问题

| 技能 | 适用场景 | 详细文档 |
|------|----------|----------|
| [ota-upgrade-fail](#ota-upgrade-fail) | ESP32 可检测新版本但下载失败、auto_update 配置 | [Problems.md](./Problems.md#ota-upgrade-fail) |

---

## 快速诊断流程

```bash
# 1. 检查容器状态
docker ps -a | grep xiaozhi

# 2. 查看最近的错误日志
docker logs xiaozhi-esp32-server --tail 50

# 3. 测试 OTA 接口
curl -X POST http://localhost:8102/ota/ \
  -H "Device-Id: 11:22:33:44:55:66" \
  -H "Content-Type: application/json" \
  -d '{"application":{"version":"0.0.1"}}'

# 4. 检查端口映射
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

---

## 技能详情

### server-secret-mismatch（服务器密钥不匹配）

**适用场景：**
- xiaozhi-server 容器启动失败，日志显示 `无效的服务器密钥`
- 容器反复重启（Restarting 状态）
- 智控台 API 返回 401 认证错误

**快速诊断：**
```bash
# 检查容器状态
docker ps -a | grep xiaozhi-esp32-server

# 查看错误日志
docker logs xiaozhi-esp32-server --tail 50

# 检查数据库密钥
docker exec xiaozhi-esp32-server-db mysql -uroot -p123456 -e \
  "SELECT param_value FROM xiaozhi_esp32_server.sys_params WHERE param_code = 'server.secret';"

# 清除 Redis 缓存
docker exec xiaozhi-esp32-server-redis redis-cli del 'sys:params'
```

**详细文档：** [Problems.md#server-secret-mismatch](./Problems.md#server-secret-mismatch)

---

### ota-404-fix（OTA 接口 404 错误）

**适用场景：**
- ESP32 设备请求 OTA 接口返回 404
- 日志显示 `Failed to check version, status code: 404`

**快速诊断：**
```bash
# 检查 context path
docker logs xiaozhi-esp32-server-web | grep "context path"

# 测试 OTA 接口
docker exec xiaozhi-esp32-server-web wget -qO- http://localhost:8003/ota/
```

**详细文档：** [Problems.md#ota-404-fix](./Problems.md#ota-404-fix)

---

### ota-connection-error（OTA 连接错误）

**适用场景：**
- 智控台参数管理界面无法连接
- ESP32 设备配置 OTA 后无法连接
- 日志显示 `httpx.ConnectError`

**快速诊断：**
```bash
# 检查端口映射
docker ps --filter "name=xiaozhi" --format "table {{.Names}}\t{{.Ports}}"

# 测试 OTA 接口
curl -X POST http://localhost:8102/ota/ \
  -H "Device-Id: 11:22:33:44:55:66" \
  -H "Content-Type: application/json" \
  -d '{"application":{"version":"0.0.1"}}'
```

**详细文档：** [Problems.md#ota-connection-error](./Problems.md#ota-connection-error)

---

### server-ota-config（server.ota 参数配置）

**适用场景：**
- 智控台参数设置中 `server.ota` 显示连接错误
- IP 地址变更后未更新配置
- Redis 缓存参数过期

**快速诊断：**
```bash
# 检查数据库参数
docker exec xiaozhi-esp32-server-db mysql -uroot -p123456 -e \
  "SELECT param_code, param_value FROM sys_params WHERE param_code IN ('server.ota', 'server.mqtt_gateway');"

# 检查 Redis 缓存
docker exec xiaozhi-esp32-server-redis redis-cli hgetall 'sys:params'

# 清除 Redis 缓存
docker exec xiaozhi-esp32-server-redis redis-cli DEL sys:params
```

**详细文档：** [Problems.md#server-ota-config](./Problems.md#server-ota-config)

---

### ota-upgrade-fail（OTA 升级失败）

**适用场景：**
- ESP32 设备可以检测到新版本，但下载固件时失败
- 关闭自动升级后设备反复连接

**快速诊断：**
```bash
# 检查设备 auto_update 状态
docker exec xiaozhi-esp32-server-db mysql -uroot -p123456 -e \
  "SELECT id, mac_address, auto_update FROM ai_device WHERE mac_address='98:88:e0:16:3e:e8';"

# 启用自动升级
docker exec xiaozhi-esp32-server-db mysql -uroot -p123456 -e \
  "UPDATE ai_device SET auto_update=1 WHERE mac_address='98:88:e0:16:3e:e8';"

# 测试 OTA 接口
curl -s -X POST "http://localhost:8102/ota/" \
  -H "Device-Id: 98:88:e0:16:3e:e8" \
  -H "Content-Type: application/json" \
  -d '{"application":{"version":"1.9.4"},"board":{"type":"xingzhi-cube-1.54tft-wifi"}}' | grep firmware
```

**详细文档：** [Problems.md#ota-upgrade-fail](./Problems.md#ota-upgrade-fail)

---

### container-port-mapping（容器端口映射）

**适用场景：**
- 服务无法访问
- 容器间网络通信失败
- 前端无法调用后端 API

**标准端口映射：**

| 容器 | 内部端口 | 宿主机端口 | 用途 |
|------|---------|-----------|------|
| xiaozhi-esp32-server-web | 8002 | **8101** | 智控台 Web UI（浏览器访问） |
| xiaozhi-esp32-server-web | 8003 | **8102** | manager-api 后端（设备/API 调用） |
| xiaozhi-esp32-server | 8000 | **8100** | WebSocket 服务（音频流通信） |
| xiaozhi-esp32-server-db | 3306 | **3307** | MySQL 数据库 |
| xiaozhi-esp32-server-redis | 6379 | **6380** | Redis 缓存 |

**记忆口诀：**
- **8101** = 智控台（人用的，浏览器）
- **8102** = manager-api（设备用的，接口调用）
- **8100** = WebSocket（音频流）

**详细文档：** [Problems.md#container-port-mapping](./Problems.md#container-port-mapping)

---

## 完整诊断手册

所有技能的详细诊断步骤、解决方案、配置文件说明请查看：

👉 **[Problems.md](./Problems.md)** - 完整故障诊断手册

---

## 技能更新记录

| 日期 | 技能 | 说明 |
|------|------|------|
| 2026-03-13 | Problems.md | 整合所有技能到统一文档 |
| 2026-03-12 | server-secret-mismatch | 新增：服务器密钥不匹配问题诊断 |
| 2026-03-12 | ota-404-fix | 新增：OTA 接口 404 错误修复 |
| 2026-03-12 | ota-connection-error | 整合：OTA 连接错误诊断 |
| 2026-03-12 | server-ota-config | 整合：server.ota 参数配置 |
| 2026-03-12 | container-port-mapping | 新增：容器端口映射说明 |
| 2026-03-13 | ota-upgrade-fail | 整合：OTA 升级失败诊断 |
