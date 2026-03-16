 # xiaozhi-esp32-server 故障诊断手册

> 统一的故障诊断技能索引，涵盖认证、配置、容器网络、OTA 升级等常见问题

---

## 目录

| 问题分类 | 章节 |
|----------|------|
| [🔐 服务器密钥不匹配](#server-secret-mismatch) | 容器启动失败、API 认证错误 |
| [📡 OTA 连接错误](#ota-connection-error) | ESP32 设备无法连接、端口配置错误 |
| [🔧 OTA 接口 404 错误](#ota-404-fix) | context-path 配置问题 |
| [⚙️ server.ota 参数配置](#server-ota-config) | IP 变更更新、Redis 缓存清理 |
| [🌐 IP变动导致设备连接不稳定](#ip-change-solution) | 计算机IP变化、设备无法连接、配置硬编码IP |
| [📥 OTA 升级失败](#ota-upgrade-fail) | 设备 auto_update、Redis UUID、nginx 配置 |
| [🐳 容器端口映射](#container-port-mapping) | 端口混淆、容器间网络通信 |

---

\## 🔐 server-secret-mismatch（服务器密钥不匹配）

### 适用场景
- xiaozhi-server 容器启动失败，日志显示 `无效的服务器密钥`
- 容器反复重启（Restarting 状态）
- 智控台 API 返回 401 认证错误

### 诊断步骤

**1. 检查容器状态**
```bash
docker ps -a | grep xiaozhi-esp32-server
# 如果状态是 Restarting，说明启动失败
```

**2. 查看错误日志**
```bash
docker logs xiaozhi-esp32-server --tail 50
# 查找：Exception: API 返回错误：无效的服务器密钥
```

**3. 检查配置文件中的密钥**
```bash
cat /home/li/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/data/.config.yaml
# 查看 manager-api.secret 值
```

**4. 检查数据库中的密钥**
```bash
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> -e \
  "SELECT param_value FROM xiaozhi_esp32_server.sys_params WHERE param_code = 'server.secret';"
```

**5. 检查 Redis 缓存中的密钥**
```bash
docker exec xiaozhi-esp32-server-redis redis-cli hget 'sys:params' 'server.secret'
```

### 常见原因

| 原因 | 说明 |
|------|------|
| Redis 缓存过期 | 数据库中已更新密钥，但 Redis 缓存仍是旧值 |
| 配置文件不同步 | 智控台修改了密钥，但 xiaozhi-server 配置文件未更新 |
| 多环境混用 | 开发/测试/生产环境使用了相同的配置文件 |

### 解决方案

```bash
# 方案 1：清除 Redis 缓存（让服务从数据库重新加载）
docker exec xiaozhi-esp32-server-redis redis-cli del 'sys:params'

# 方案 2：更新 xiaozhi-server 配置文件中的密钥
# 编辑 /home/li/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server/data/.config.yaml
# 将 secret 更新为数据库中的值

# 方案 3：重启 xiaozhi-server 容器
docker restart xiaozhi-esp32-server
```

### 验证修复
```bash
# 1. 检查容器是否正常运行
docker ps | grep xiaozhi-esp32-server
# 状态应为 Up，不是 Restarting

# 2. 测试 API 接口
docker run --rm --network xiaozhi-server_default alpine sh -c \
  'wget -qO- --header="Authorization: Bearer <你的密钥>" \
   http://xiaozhi-esp32-server-web:8002/xiaozhi/config/server-base'
```

### 关键文件
| 文件 | 作用 |
|------|------|
| `data/.config.yaml` | xiaozhi-server 配置文件 |
| `ServerSecretFilter.java` | 密钥验证过滤器 |
| `sys_params` 表 | 系统参数存储 |

---

## 📡 ota-connection-error（OTA 连接错误）

### 适用场景
- 智控台参数管理界面无法连接服务器
- ESP32 设备配置 OTA 后无法连接
- OTA 接口返回 404 或连接失败
- 容器日志显示 `httpx.ConnectError` 或 `Resource not found`

### 快速诊断

```bash
# 1. 检查容器状态和端口映射
docker ps --filter "name=xiaozhi" --format "table {{.Names}}\t{{.Ports}}"

# 2. 测试 OTA 接口（ESP32 设备访问）
curl -X POST http://localhost:8102/ota/ \
  -H "Device-Id: 11:22:33:44:55:66" \
  -H "Content-Type: application/json" \
  -d '{"application":{"version":"0.0.1"}}'

# 3. 测试智控台后端（前端访问）
curl http://localhost:8102/xiaozhi/config/server-base
```

### 常见错误及解决方案

#### 错误 1：ESP32 设备 OTA 配置错误

**症状：**
- ESP32 配置 OTA 地址后无法连接
- 日志显示 `httpx.ConnectError: All connection attempts failed`
- 或返回 `Resource not found: No static resource ota`

**正确配置：**

| 配置项 | 错误值 | 正确值 |
|--------|-------|-------|
| OTA 地址 | `http://192.168.1.102:8101/xiaozhi/ota` | `http://192.168.1.102:8102/ota/` |
| 说明 | 8101 是 Web UI 端口 | 8102 是 manager-api 后端端口 |

**原因分析：**
1. **端口混淆**：
   - 8101 → 智控台 Web 界面（给浏览器用）
   - 8102 → manager-api 后端（给 ESP32 设备用）

2. **路径问题**：
   - manager-api 的 OTAController 映射路径是 `/ota/`
   - 前端 API 调用使用 `/xiaozhi/ota/`（经过 Vue 代理）
   - ESP32 设备直接访问，应使用 `/ota/`

**正确配置示例：**
```cpp
// ESP32 设备固件中配置
#define OTA_URL "http://192.168.1.102:8102/ota/"
```

#### 错误 2：Shiro 安全过滤导致 404

**症状：**
- 访问 OTA 接口返回 404
- 日志显示 `Resource not found: No static resource`

**检查 ShiroConfig：**
确认 `/ota/**` 在匿名访问列表中：
```java
filterMap.put("/ota/**", "anon");  // 必须配置
filterMap.put("/otaMag/download/**", "anon");
```
位置：`main/manager-api/src/main/java/xiaozhi/modules/security/config/ShiroConfig.java`

### 配置文件检查

**xiaozhi-server/.config.yaml**
```yaml
read_config_from_api: true  # 启用智控台
manager-api:
  url: http://xiaozhi-esp32-server-web:8002/xiaozhi  # Docker 内部网络
  secret: <你的密钥>
```

### 关键文件
| 文件 | 作用 |
|------|------|
| `OTAController.java` | manager-api OTA 接口 |
| `ShiroConfig.java` | 安全过滤配置 |
| `DeviceServiceImpl.java` | 设备激活和固件检查逻辑 |
| `http_server.py` | xiaozhi-server HTTP 服务 |

---

## 🔧 ota-404-fix（OTA 接口 404 错误修复）

### 问题现象
ESP32 设备请求 OTA 接口返回 404 错误：
```
E (153684) Ota: Failed to check version, status code: 404
W (153684) Application: Alert [cloud_slash] 错误：检查新版本失败，将在 320 秒后重试
```

### 根本原因
Java 后端 `application.yml` 配置了 `context-path: /xiaozhi`，导致：
- ESP32 设备请求 `http://IP:8102/ota/`
- 但实际路径是 `/xiaozhi/ota/`
- 因此返回 404 错误

### 诊断步骤
```bash
# 1. 检查 context path 配置
docker logs xiaozhi-esp32-server-web | grep "context path"
# 如果输出 '/xiaozhi' 则说明配置有问题

# 2. 测试 OTA 接口
docker exec xiaozhi-esp32-server-web wget -qO- http://localhost:8003/ota/
# 如果返回 404，说明 context path 有问题
```

### 解决方案

**修改 Docker Compose 配置**

编辑 `/opt/xiaozhi-server/docker-compose_all.yml`，在 `xiaozhi-esp32-server-web` 服务中添加环境变量：
```yaml
xiaozhi-esp32-server-web:
  environment:
    - SERVER_SERVLET_CONTEXT_PATH=/
```

**重启容器**
```bash
cd /opt/xiaozhi-server
docker compose -f docker-compose_all.yml up -d xiaozhi-esp32-server-web
```

### 验证修复
```bash
# 1. 验证 context path 是否为空
docker logs xiaozhi-esp32-server-web | grep "context path"
# 预期输出：context path '/'

# 2. 测试 OTA 接口
docker exec xiaozhi-esp32-server-web wget -qO- http://localhost:8003/ota/
# 预期输出：OTA 接口运行正常，websocket 集群数量：1
```

### 注意事项
1. 修改 `application.yml` 后需要重新构建 Docker 镜像才能生效
2. 使用环境变量 `SERVER_SERVLET_CONTEXT_PATH=/` 可以在不重新构建镜像的情况下覆盖配置

---

## ⚙️ server-ota-config（server.ota 参数配置）

### 问题背景
当智控台参数设置中 `server.ota` 显示无法连接或配置错误时，通常是因为：
1. 数据库中 `server.ota` 参数值为 `null` 或错误值
2. Redis 缓存中参数未更新
3. IP 地址变更后未同步更新配置

### 快速诊断
```bash
# 1. 检查数据库中的参数值
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "SELECT param_code, param_value FROM sys_params WHERE param_code IN ('server.ota', 'server.mqtt_gateway', 'server.websocket');"

# 2. 检查 Redis 缓存
docker exec xiaozhi-esp32-server-redis redis-cli hgetall 'sys:params' | grep -A1 "server.ota"

# 3. 测试 OTA 接口
curl -s http://localhost:8102/xiaozhi/ota/
```

### 修复步骤

**步骤 1：更新数据库中的参数值**
```bash
# 替换为你的实际 IP 或域名
YOUR_IP_OR_DOMAIN="10.205.150.28"

docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "UPDATE sys_params SET param_value = 'http://${YOUR_IP_OR_DOMAIN}:8102/ota/' WHERE param_code = 'server.ota'; \
      UPDATE sys_params SET param_value = 'mqtt://${YOUR_IP_OR_DOMAIN}:8100' WHERE param_code = 'server.mqtt_gateway';"
```

**步骤 2：清除并刷新 Redis 缓存**
```bash
# 删除缓存键（让服务从数据库重新加载）
docker exec xiaozhi-esp32-server-redis redis-cli DEL sys:params

# 等待几秒让服务重新加载
sleep 5
```

**步骤 3：验证修复**
```bash
# 验证 OTA 接口是否正常
curl -s http://localhost:8102/xiaozhi/ota/
# 预期输出：OTA 接口运行正常，websocket 集群数量：1
```

### 配置说明

| 参数名 | 格式 | 示例 |
|--------|------|------|
| `server.ota` | `http://{IP 或域名}:8102/ota/` | `http://10.205.150.28:8102/ota/` |
| `server.mqtt_gateway` | `mqtt://{IP 或域名}:8100` | `mqtt://10.205.150.28:8100` |
| `server.websocket` | `ws://{Docker 内部网络}:8000/xiaozhi/v1/` | `ws://xiaozhi-esp32-server:8000/xiaozhi/v1/` |

### IP 变更问题

**问题：** 每次宿主机 IP 变更后，都需要手动更新 `server.ota` 和 `server.mqtt_gateway` 参数

**解决方案：**

1. **使用域名 + DDNS（推荐）**
   - 配置 DDNS（动态 DNS）到你的域名（如 `xiaozhi.shuoyan.me`）
   - 将参数值配置为域名格式：
     ```
     server.ota: http://xiaozhi.shuoyan.me:8102/ota/
     server.mqtt_gateway: mqtt://xiaozhi.shuoyan.me:8100
     ```

2. **脚本自动更新**
   ```bash
   #!/bin/bash
   NEW_IP=$(curl -s ifconfig.me)  # 获取当前公网 IP
   docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
     -e "UPDATE sys_params SET param_value = 'http://${NEW_IP}:8102/ota/' WHERE param_code = 'server.ota';"
   docker exec xiaozhi-esp32-server-redis redis-cli DEL sys:params
   ```

### 常见问题

**OTA 接口返回 "缺少 ota 地址"**
- 原因：数据库中 `server.ota` 值为 `null` 或 Redis 缓存未更新
- 解决：按上述步骤更新数据库并清除 Redis 缓存

---

## 🌐 ip-change-solution（IP变动导致设备连接不稳定）

### 适用场景
- 计算机IP地址发生变化后，ESP32设备无法连接到服务器
- 智控台参数设置中 `server.ota` 显示连接错误
- 设备通过OTA接口获取的WebSocket地址与当前IP不符
- 切换WiFi网络、重启路由器后设备无法正常使用

### 快速诊断

```bash
# 1. 查看当前IP地址
ip addr show | grep "inet " | grep -v 127.0.0.1

# 2. 访问OTA接口查看返回的WebSocket地址
curl http://localhost:8102/xiaozhi/ota/
# 或（不使用智控台时）
curl http://localhost:8102/ota/

# 3. 检查配置文件中的WebSocket地址
grep -A 5 "websocket:" main/xiaozhi-server/data/.config.yaml

# 4. 检查数据库中的参数值（使用智控台时）
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "SELECT param_code, param_value FROM sys_params WHERE param_code IN ('server.ota', 'server.websocket');"

# 5. 检查Redis缓存
docker exec xiaozhi-esp32-server-redis redis-cli hgetall 'sys:params' | grep server.ota
```

### 问题原因分析

#### 原因 1：配置文件中硬编码了IP地址

当配置文件中使用了固定的IP地址时：

```yaml
server:
  websocket: ws://192.168.1.100:8100/xiaozhi/v1/
  vision_explain: http://192.168.1.100:8102/mcp/vision/explain
```

一旦IP地址发生变化，设备仍然会尝试连接旧的IP地址。

#### 原因 2：数据库参数未更新（智控台模式）

使用智控台时，`server.ota` 和 `server.websocket` 参数存储在数据库中，IP变化后需要更新。

#### 原因 3：Redis缓存未刷新

即使更新了数据库，Redis缓存可能仍保留旧值。

### 解决方案

#### 方案 1：使用占位符（推荐，本地模式）

**适用场景**：局域网环境，IP地址经常变化，不使用智控台

**配置方法**：

编辑配置文件 `main/xiaozhi-server/data/.config.yaml`：

```yaml
server:
  # 使用占位符，系统会自动检测当前IP
  websocket: ws://你的ip或者域名:8100/xiaozhi/v1/
  vision_explain: http://你的ip或者域名:8102/mcp/vision/explain
  port: 8100      # WebSocket服务端口
  http_port: 8102 # HTTP服务端口
```

**工作原理**：
- 系统检测配置中包含"你的"占位符
- 每次OTA请求时调用 `get_local_ip()` 获取当前IP
- 自动生成包含当前IP的WebSocket地址

**优点**：
- 配置简单，无需额外软件
- 自动适应IP变化
- 无需重启服务即可生效

#### 方案 2：更新数据库参数（智控台模式）

**步骤 1：更新数据库中的参数值**

```bash
# 替换为你的实际IP
YOUR_IP="<SERVER_IP>"

# 更新OTA地址
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "UPDATE sys_params SET param_value = 'http://${YOUR_IP}:8102/ota/' WHERE param_code = 'server.ota';"

# 更新WebSocket地址（如果使用）
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "UPDATE sys_params SET param_value = 'ws://${YOUR_IP}:8100/xiaozhi/v1/' WHERE param_code = 'server.websocket';"
```

**步骤 2：清除Redis缓存**

```bash
docker exec xiaozhi-esp32-server-redis redis-cli DEL sys:params
```

#### 方案 3：使用DDNS动态域名

**适用场景**：需要从外网访问，或希望使用固定的域名地址

**配置方法**：

1. 注册DDNS服务（DuckDNS、No-IP、花生壳等）
2. 配置DDNS客户端定期更新IP
3. 在配置文件或数据库中使用域名：

```yaml
server:
  websocket: ws://your-domain.duckdns.org:8100/xiaozhi/v1/
  vision_explain: http://your-domain.duckdns.org:8102/mcp/vision/explain
```

### 验证配置是否正确

```bash
# 方法 1：检查OTA接口返回的地址
curl http://localhost:8102/ota/
# 预期输出：OTA接口运行正常，向设备发送的websocket地址是：ws://当前IP:8100/xiaozhi/v1/

# 方法 2：检查服务启动日志
# 启动服务时，日志会显示当前地址
```

### 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 配置了占位符，但地址仍不正确 | 系统无法访问外网检测IP | 检查网络连接，确保能访问8.8.8.8 |
| 设备连接成功但无法语音交互 | 防火墙阻止WebSocket | 开放8100和8102端口 |
| Docker部署设备无法连接 | 配置使用了容器内端口 | 使用宿主机端口8100/8102 |
| 更新数据库后仍使用旧地址 | Redis缓存未刷新 | 清除Redis缓存 |

### 端口说明

| 容器 | 内部端口 | 宿主机端口 | 用途 |
|------|---------|-----------|------|
| xiaozhi-esp32-server-web | 8002 | **8101** | 智控台 Web UI |
| xiaozhi-esp32-server-web | 8003 | **8102** | manager-api 后端 |
| xiaozhi-esp32-server | 8000 | **8100** | WebSocket 服务 |

**记忆口诀**：
- **8101** = 智控台（人用的，浏览器）
- **8102** = manager-api（设备用的，接口调用）
- **8100** = WebSocket（音频流）

### 相关文件

| 文件 | 作用 |
|------|------|
| `data/.config.yaml` | xiaozhi-server 本地配置文件 |
| `ota_handler.py` | OTA接口处理器，生成WebSocket地址 |
| `util.py` | 工具函数，包含 `get_local_ip()` |
| `sys_params` 表 | 系统参数存储（智控台模式） |


---

## 📥 ota-upgrade-fail（OTA 升级失败）

### 问题现象
ESP32 设备可以检测到新版本，但下载固件时失败或返回错误：
```
E (153684) Ota: Failed to download firmware
```

### 常见原因与解决方案

#### 原因 1：设备 auto_update 未启用（最常见）

**检查方法：**
```bash
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "SELECT id, mac_address, auto_update FROM ai_device WHERE mac_address='<DEVICE_MAC>';"
```

**解决方案：**
```bash
# 启用自动升级
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "UPDATE ai_device SET auto_update=1 WHERE mac_address='<DEVICE_MAC>';"
```

#### 原因 2：Redis UUID 缓存过期或格式错误

OTA 下载链接使用一次性 UUID，存储在 Redis 中。如果 UUID 过期或格式错误，会导致 500 错误。

**检查方法：**
```bash
# 检查 Redis 中的 UUID 缓存
docker exec xiaozhi-esp32-server-redis redis-cli keys "ota:id:*"
```

**解决方案：**
```bash
# 清除过期的 UUID 缓存
docker exec xiaozhi-esp32-server-redis redis-cli keys "ota:id:*" | xargs docker exec xiaozhi-esp32-server-redis redis-cli del
```

#### 原因 3：nginx 配置问题

如果通过 8102 端口下载失败，但直接访问 8003 端口可以下载，说明 nginx 配置有问题。

**测试方法：**
```bash
# 测试直接访问后端（容器内）
docker exec xiaozhi-esp32-server-web wget -qO- http://127.0.0.1:8003/otaMag/download/{uuid}

# 测试通过 nginx 访问
curl -I http://localhost:8102/otaMag/download/{uuid}
```

**解决方案：**
修改 nginx 配置，确保 `/xiaozhi/otaMag/` 路径正确转发：
```nginx
location /xiaozhi/otaMag/ {
    proxy_pass http://127.0.0.1:8003/otaMag/;
    proxy_set_header   Host   $host;
    proxy_connect_timeout 60;
    proxy_read_timeout 60;
}
```

#### 原因 4：固件文件不存在

**检查方法：**
```bash
# 查看数据库中的固件路径
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "SELECT id, firmware_name, firmware_path FROM ai_ota;"

# 检查容器内文件是否存在
docker exec xiaozhi-esp32-server-web ls -la /uploadfile/
```

**解决方案：**
重新上传固件文件，确保 `uploadfile` 目录在容器内可访问。

### 完整诊断流程

**步骤 1：检查设备状态**
```bash
# 检查设备是否激活，auto_update 是否为 1
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "SELECT id, mac_address, app_version, auto_update FROM ai_device;"
```

**步骤 2：检查固件列表**
```bash
# 查看可用的固件版本
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> xiaozhi_esp32_server \
  -e "SELECT id, type, version, firmware_path FROM ai_ota;"
```

**步骤 3：测试 OTA 接口**
```bash
# 模拟 ESP32 请求
curl -s -X POST "http://localhost:8102/ota/" \
  -H "Device-Id: <DEVICE_MAC>" \
  -H "Content-Type: application/json" \
  -d '{"application":{"version":"1.9.4"},"board":{"type":"xingzhi-cube-1.54tft-wifi"}}' | grep firmware
```
预期输出应包含 `firmware` 字段和 `url` 下载地址。

**步骤 4：测试下载链接**
```bash
# 获取 UUID 并测试下载
UUID=$(curl -s http://localhost:8102/otaMag/getDownloadUrl/7258ddea9ff7e3ac9a49d6edd2280c45 2>/dev/null | grep -o '"data":"[^"]*"')
curl -I "http://localhost:8102/otaMag/download/${UUID//\"/}"
```

### 关键端口说明

| 端口 | 用途 |
|------|------|
| 8100 | WebSocket（音频流） |
| 8101 | 智控台 Web UI（浏览器） |
| 8102 | manager-api 后端（**ESP32 设备使用此端口**） |

**ESP32 设备应配置的 OTA 地址：**
```
http://{服务器 IP}:8102/ota/
```

**不要使用 `/xiaozhi` 前缀！**

### 相关文件
| 文件 | 作用 |
|------|------|
| `OTAMagController.java` | 固件管理控制器 |
| `OTAController.java` | OTA 检查接口控制器 |
| `DeviceServiceImpl.java` | 设备服务实现 |
| `/uploadfile/` | 固件文件存储目录（容器内） |

---

## 🐳 container-port-mapping（容器端口映射）

### 适用场景
- 服务无法访问
- 容器间网络通信失败
- 前端无法调用后端 API

### 标准端口映射

| 容器 | 内部端口 | 宿主机端口 | 用途 |
|------|---------|-----------|------|
| xiaozhi-esp32-server-web | 8002 | **8101** | 智控台 Web UI（浏览器访问） |
| xiaozhi-esp32-server-web | 8003 | **8102** | manager-api 后端（设备/API 调用） |
| xiaozhi-esp32-server | 8000 | **8100** | WebSocket 服务（音频流通信） |
| xiaozhi-esp32-server-db | 3306 | **3307** | MySQL 数据库 |
| xiaozhi-esp32-server-redis | 6379 | **6380** | Redis 缓存 |

### 诊断命令

```bash
# 检查端口映射
docker ps --format "table {{.Names}}\t{{.Ports}}" | grep xiaozhi

# 测试端口连通性
docker run --rm --network xiaozhi-server_default alpine nc -zv xiaozhi-esp32-server-web:8002
```

### 记忆口诀
- **8101** = 智控台（人用的，浏览器）
- **8102** = manager-api（设备用的，接口调用）
- **8100** = WebSocket（音频流）

---

## 快速诊断命令合集

```bash
# ===== 容器状态检查 =====
docker ps -a | grep xiaozhi                    # 查看所有容器状态
docker stats --no-stream                       # 查看资源使用

# ===== 日志检查 =====
docker logs xiaozhi-esp32-server --tail 50     # xiaozhi-server 日志
docker logs xiaozhi-esp32-server-web --tail 50 # manager-api 日志
docker logs xiaozhi-esp32-server-db --tail 50  # MySQL 日志

# ===== 数据库检查 =====
docker exec xiaozhi-esp32-server-db mysql -uroot -p<MYSQL_ROOT_PASSWORD> -e \
  "SELECT param_code, param_value FROM xiaozhi_esp32_server.sys_params \
   WHERE param_code IN ('server.secret', 'server.ota', 'server.websocket');"

# ===== Redis 检查 =====
docker exec xiaozhi-esp32-server-redis redis-cli keys '*'           # 所有键
docker exec xiaozhi-esp32-server-redis redis-cli hgetall 'sys:params' # 系统参数

# ===== 接口测试 =====
curl -H "Authorization: Bearer <密钥>" \
  http://localhost:8102/xiaozhi/config/server-base                  # 配置接口
curl http://localhost:8102/ota/                                     # OTA 接口
```

---

## 技能更新记录

| 日期 | 技能 | 说明 |
|------|------|------|
| 2026-03-16 | ip-change-solution | 新增：IP变动导致设备连接不稳定问题解决方案 |
| 2026-03-12 | server-secret-mismatch | 新增：服务器密钥不匹配问题诊断 |
| 2026-03-12 | ota-404-fix | 新增：OTA 接口 404 错误修复（context-path） |
| 2026-03-12 | ota-connection-error | 整合：OTA 连接错误诊断 |
| 2026-03-12 | server-ota-config | 整合：server.ota 参数配置 |
| 2026-03-12 | container-port-mapping | 新增：容器端口映射说明 |
| 2026-03-13 | ota-upgrade-fail | 整合：OTA 升级失败诊断（auto_update、Redis UUID、nginx） |

---

## 🐍 local-run-errors（本地源码运行错误）

### 适用场景
- 本地源码运行 xiaozhi-server 时遇到的错误
- 不依赖 Docker 容器的开发调试模式

### 错误 1：auth_key 缺失

**症状：**
```
启动失败：'auth_key'
```

**原因：** `config_loader.py` 从 API 获取配置时，期望 `server.auth_key` 存在，但本地配置文件中未设置

**解决方案：**
```yaml
# 编辑 main/xiaozhi-server/data/.config.yaml
server:
  auth_key: local-dev-auth-key  # 添加此行
```

**代码修复：** 修改 `config/config_loader.py` 添加回退逻辑：
```python
# 如果服务器没有 auth_key，则从本地配置读取
if not config_data.get("server", {}).get("auth_key"):
    config_data["server"]["auth_key"] = config.get("server", {}).get("auth_key", "default-auth-key")
```

### 错误 2：loguru 模块未找到

**症状：**
```
ModuleNotFoundError: No module named 'loguru'
```

**原因：** 未使用虚拟环境，系统 Python 缺少项目依赖

**解决方案：**
```bash
# 使用项目虚拟环境
source /home/li/xiaozhi/xiaozhi-esp32-server/venv/bin/activate
python3 app.py
```

### 错误 3：端口被占用

**症状：**
```
OSError: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

**原因：** Docker 容器或其他进程占用了 8000 端口

**解决方案：**
```bash
# 方案 1：停止占用端口的 Docker 容器
docker stop xiaozhi-esp32-server-web

# 方案 2：修改配置使用其他端口
# 编辑 .config.yaml
server:
  port: 8001  # 改为其他可用端口
```

### 错误 4：API key 未设置

**症状：**
```
配置错误：LLM 的 API key 未设置，当前值为：你的 chat-glm web key
```

**原因：** `config.yaml` 中 LLM 配置使用了占位符值，未设置真实的 API key

**解决方案：**
```yaml
# 编辑 config.yaml 或 selected_module 对应的 LLM 配置
LLM:
  your-provider:
    api_key: <YOUR_API_KEY>
```

**注意：** 此错误不影响服务启动，但会导致 AI 对话功能无法使用

### 错误 5：WebSocket 地址重复前缀

**症状：**
日志显示：
```
WebSocket 地址是 ws://ws://<SERVER_IP>:8100/xiaozhi/v1/
```

**原因：** `app.py` 中输出时重复添加了 `ws://` 前缀

**解决方案：**
```python
# 修复前
logger.info(f"WebSocket 地址是 ws://{config['server'].get('websocket')}")
# 修复后
logger.info(f"WebSocket 地址是 {config['server'].get('websocket')}")
```

### 完整启动命令

```bash
cd /home/li/xiaozhi/xiaozhi-esp32-server/main/xiaozhi-server
source ../../venv/bin/activate
python3 app.py
```

### 验证运行
```bash
# 查看日志
tail -f main/xiaozhi-server/tmp/server.log

# 检查进程
ps aux | grep "python3 app.py"

# 测试 WebSocket
curl -i http://localhost:8000  # 应返回 "Server is running"
```

### 相关技能文件
- `/skills/config-local-run-guide.md`: 本地运行配置详细指南

