# 解决计算机IP变动导致硬件连接不稳定的问题

## 问题描述

当您的计算机IP地址发生变化时（例如：切换WiFi网络、重启路由器、网络环境变更），ESP32设备可能无法正常连接到小智服务器，表现为：

- 设备无法通过OTA接口获取正确的WebSocket地址
- 设备连接WebSocket失败
- 语音交互功能失效

## 问题原因分析

### 1. 硬编码IP地址

当配置文件中使用了固定的IP地址时：

```yaml
server:
  websocket: ws://192.168.1.100:8000/xiaozhi/v1/
  vision_explain: http://192.168.1.100:8003/mcp/vision/explain
```

一旦IP地址发生变化（如从 `192.168.1.100` 变为 `192.168.1.200`），设备仍然会尝试连接旧的IP地址，导致连接失败。

### 2. WebSocket地址生成机制

系统有两种WebSocket地址生成方式：

| 配置方式 | 示例 | IP变化时行为 |
|---------|------|-------------|
| 占位符模式 | `ws://你的ip或者域名:端口号/xiaozhi/v1/` | 自动检测当前IP，动态生成地址 |
| 固定IP模式 | `ws://192.168.1.100:8000/xiaozhi/v1/` | 使用固定地址，IP变化后失效 |

## 解决方案

### 方案一：使用占位符（推荐，最简单）

**适用场景**：局域网环境，IP地址经常变化

**配置方法**：

1. 编辑配置文件 `data/.config.yaml`：

```yaml
server:
  # 使用占位符，系统会自动检测当前IP
  websocket: ws://你的ip或者域名:8100/xiaozhi/v1/
  vision_explain: http://你的ip或者域名:8102/mcp/vision/explain
  port: 8100  # WebSocket服务端口
  http_port: 8102  # HTTP服务端口
```

2. 重启服务使配置生效

**工作原理**：

- 系统在每次OTA请求时调用 `get_local_ip()` 函数
- 通过连接到Google DNS (8.8.8.8) 检测当前本机IP
- 自动生成包含当前IP的WebSocket地址

**优点**：
- 配置简单，无需额外软件
- 自动适应IP变化
- 无需重启服务即可生效

**缺点**：
- 需要能访问外网（用于IP检测）
- 生成的地址只适用于局域网访问

---

### 方案二：使用动态域名（DDNS）

**适用场景**：需要从外网访问，或希望使用固定的域名地址

**实施步骤**：

1. **注册DDNS服务**（选择其一）：
   - [No-IP](https://www.noip.com/)（免费）
   - [DuckDNS](https://www.duckdns.org/)（免费）
   - [花生壳](https://hsk.oray.com/)（国内服务）
   - [阿里云DDNS](https://alidns.aliyun.com/)

2. **配置DDNS客户端**：

以DuckDNS为例，创建定时任务：

```bash
# 编辑crontab
crontab -e

# 添加以下行（每5分钟更新一次）
*/5 * * * * curl -s "https://www.duckdns.org/update?domains=your-domain&token=your-token&ip="
```

3. **修改配置文件**：

```yaml
server:
  websocket: ws://your-domain.duckdns.org:8100/xiaozhi/v1/
  vision_explain: http://your-domain.duckdns.org:8102/mcp/vision/explain
```

4. **配置路由器端口转发**（如需外网访问）：

将外网端口映射到内网服务：
- 外网 8100 → 内网 192.168.x.x:8100（WebSocket）
- 外网 8102 → 内网 192.168.x.x:8102（HTTP）

**优点**：
- 可以使用固定的域名地址
- 支持外网访问
- IP变化后自动更新

**缺点**：
- 需要额外配置DDNS服务
- 可能需要配置路由器端口转发

---

### 方案三：使用内网穿透

**适用场景**：没有公网IP，需要从外网访问

**推荐服务**：

| 服务 | 特点 | 费用 |
|-----|------|------|
| [ngrok](https://ngrok.com/) | 简单易用，支持WebSocket | 免费版有限制 |
| [frp](https://github.com/fatedier/frp) | 开源自建，功能强大 | 需要自有服务器 |
| [花生壳](https://hsk.oray.com/) | 国内服务稳定 | 免费版有限制 |
| [cpolar](https://www.cpolar.com/) | 支持WebSocket | 免费版有限制 |

**配置示例（以ngrok为例）**：

```bash
# 安装ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz

# 启动隧道（WebSocket端口）
./ngrok http 8100
```

然后在配置文件中使用ngrok提供的地址：

```yaml
server:
  websocket: ws://abc123.ngrok.io/xiaozhi/v1/
```

**优点**：
- 无需公网IP
- 配置相对简单

**缺点**：
- 免费版通常有流量/带宽限制
- 延迟可能较高

---

### 方案四：手动更新固定IP

**适用场景**：IP不常变化，或不希望依赖外部服务

**操作步骤**：

1. 查看当前IP地址：

```bash
# 方法1：查看系统IP
ip addr show | grep "inet " | grep -v 127.0.0.1

# 方法2：访问OTA接口确认
curl http://localhost:8102/xiaozhi/ota/
```

2. 更新配置文件：

```yaml
server:
  websocket: ws://新的IP地址:8100/xiaozhi/v1/
  vision_explain: http://新的IP地址:8102/mcp/vision/explain
```

3. 重启服务：

```bash
# 如果是Docker部署
docker restart xiaozhi-esp32-server-web

# 如果是源码运行
pkill -f "python3 app.py"
python3 app.py
```

**优点**：
- 不依赖外部服务
- 配置直接明了

**缺点**：
- IP变化后需要手动操作
- 需要重启服务

---

## 验证配置是否正确

### 1. 检查OTA接口返回的地址

```bash
# 访问OTA接口
curl http://localhost:8102/xiaozhi/ota/

# 预期输出示例：
# OTA接口运行正常，向设备发送的websocket地址是：ws://<SERVER_IP>:8100/xiaozhi/v1/
```

确认返回的WebSocket地址中的IP地址是当前有效的IP。

### 2. 检查服务启动日志

启动服务时，日志会显示当前的WebSocket地址：

```
OTA接口是        http://<SERVER_IP>:8102/xiaozhi/ota/
视觉分析接口是    http://<SERVER_IP>:8102/mcp/vision/explain
Websocket地址是  ws://<SERVER_IP>:8100/xiaozhi/v1/
```

### 3. 设备连接测试

使用ESP32设备尝试连接，观察是否能正常建立连接。

---

## 常见问题排查

### Q1: 配置了占位符，但OTA接口返回的地址仍然不正确？

**检查项**：
1. 确认配置文件中确实包含"你的"占位符
2. 检查系统是否能访问外网（用于IP检测）
3. 查看日志中的错误信息

**解决方法**：
```bash
# 测试网络连接
ping -c 3 8.8.8.8

# 如果无法访问外网，可以修改get_local_ip()函数
# 使用其他方式获取IP地址
```

### Q2: 设备显示连接成功，但无法进行语音交互？

**可能原因**：
- 防火墙阻止了WebSocket连接
- 端口映射配置错误

**排查步骤**：
```bash
# 检查端口是否在监听
netstat -tuln | grep 8100

# 检查防火墙状态
sudo ufw status

# 如需开放端口
sudo ufw allow 8100/tcp
sudo ufw allow 8102/tcp
```

### Q3: Docker部署时，设备无法连接？

**检查项**：
1. 确认容器端口正确映射到宿主机
2. 确认配置中使用的是宿主机端口，而不是容器内端口

**端口对照表**：

| 宿主机端口 | 容器端口 | 用途 |
|-----------|---------|------|
| 8100 | 8000 | WebSocket |
| 8102 | 8003 | HTTP/OTA |

配置文件中应使用宿主机端口：

```yaml
server:
  websocket: ws://你的IP:8100/xiaozhi/v1/  # 使用宿主机端口8100
  vision_explain: http://你的IP:8102/mcp/vision/explain  # 使用宿主机端口8102
```

---

## 配置示例参考

### 示例1：局域网开发环境（推荐）

```yaml
# data/.config.yaml
server:
  port: 8100
  http_port: 8102
  # 使用占位符，自动检测IP
  websocket: ws://你的ip或者域名:8100/xiaozhi/v1/
  vision_explain: http://你的ip或者域名:8102/mcp/vision/explain
```

### 示例2：Docker部署 + DDNS

```yaml
# data/.config.yaml
server:
  port: 8100
  http_port: 8102
  # 使用DDNS域名
  websocket: ws://xiaozhi.ddns.net:8100/xiaozhi/v1/
  vision_explain: http://xiaozhi.ddns.net:8102/mcp/vision/explain
```

### 示例3：内网穿透

```yaml
# data/.config.yaml
server:
  port: 8100
  http_port: 8102
  # 使用内网穿透地址
  websocket: ws://xiaozhi.cpolar.cn/xiaozhi/v1/
  vision_explain: http://xiaozhi.cpolar.cn/mcp/vision/explain
```

---

## 总结

| 方案 | 难度 | 适用场景 | 是否需要外网 | IP变化响应 |
|------|------|---------|------------|-----------|
| 占位符 | ⭐ | 局域网，IP常变化 | 需要访问外网检测IP | 自动 |
| DDNS | ⭐⭐ | 需要外网访问 | 需要访问外网更新DNS | 自动（定期更新） |
| 内网穿透 | ⭐⭐ | 无公网IP | 需要 | 自动 |
| 固定IP | ⭐ | IP不常变化 | 不需要 | 手动更新 |

**推荐选择**：

- **开发调试环境**：使用占位符，最简单方便
- **家庭局域网**：使用占位符或DDNS
- **需要外网访问**：使用DDNS或内网穿透
- **生产环境**：使用固定公网IP或DDNS + 端口转发

---

## 相关文档

- [部署指南](Deployment.md)
- [Docker部署](docker/README.md)
- [常见问题](FAQ.md)