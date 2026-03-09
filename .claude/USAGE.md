# 小智ESP32后端服务 - 使用说明

## 快速启动

### 一键启动服务

```bash
cd /home/li/xiaozhi-esp32-server
bash start.sh
```

### 服务地址

启动成功后，服务会自动检测IP地址并显示：

- **WebSocket地址**: `ws://你的IP地址:8000/xiaozhi/v1/`
- **HTTP接口**: `http://你的IP地址:8003`
- **OTA接口**: `http://你的IP地址:8003/xiaozhi/ota/`
- **视觉分析接口**: `http://你的IP地址:8003/mcp/vision/explain`

## 配置说明

### 基本配置

所有配置都在 `main/xiaozhi-server/config.yaml` 文件中。

### 自定义配置

创建 `main/xiaozhi-server/data/.config.yaml` 文件来覆盖默认配置，这样更新代码时不会丢失你的配置。

### 重要配置项

#### 1. 服务器配置
```yaml
server:
  ip: 0.0.0.0        # 监听地址
  port: 8000           # WebSocket端口
  http_port: 8003      # HTTP接口端口
```

#### 2. 模块选择
```yaml
selected_module:
  VAD: SileroVAD           # 语音活动检测
  ASR: FunASR             # 语音识别
  LLM: ChatGLMLLM          # 大语言模型
  VLLM: ChatGLMVLLM        # 视觉模型
  TTS: EdgeTTS             # 语音合成
  Memory: nomem            # 记忆功能
  Intent: function_call     # 意图识别
```

#### 3. API密钥配置

你需要配置以下服务的API密钥（在 `data/.config.yaml` 中设置）：

##### ChatGLM（智谱AI）- 推荐，免费
```yaml
LLM:
  ChatGLMLLM:
    api_key: "你的智谱AI密钥"
```
申请地址：https://bigmodel.cn/usercenter/proj-mgmt/apikeys

##### TTS语音合成
推荐使用免费服务：
- **EdgeTTS**（微软，免费）
- **LinkeraiTTS**（灵犀流式，免费，默认已配置）

##### 其他配置
详见 `config.yaml` 文件中的注释说明。

## 测试工具

### 音频交互测试

```bash
# 在浏览器中打开
cd /home/li/xiaozhi-esp32-server/main/xiaozhi-server/test
# 使用谷歌浏览器打开 test_page.html
```

### 性能测试

```bash
cd /home/li/xiaozhi-esp32-server/main/xiaozhi-server
source ../../venv/bin/activate
python performance_tester.py
```

## 常见问题

### 1. 提示API key未设置

编辑 `data/.config.yaml` 文件，添加你的API密钥：

```yaml
LLM:
  ChatGLMLLM:
    api_key: "你的智谱AI密钥"
```

### 2. 服务无法启动

确保已安装以下依赖：
```bash
sudo apt install -y python3.12-venv python3-pip libopus-dev ffmpeg
```

### 3. 查看日志

日志文件位置：`main/xiaozhi-server/tmp/server.log`

## 目录结构

```
xiaozhi-esp32-server/
├── main/
│   └── xiaozhi-server/      # 主服务目录
│       ├── config.yaml         # 默认配置
│       ├── app.py             # 主程序
│       ├── data/              # 数据目录
│       │   └── .config.yaml  # 自定义配置
│       ├── tmp/               # 临时文件
│       ├── models/            # 模型目录
│       └── test/             # 测试工具
├── venv/                    # 虚拟环境
└── start.sh                 # 一键启动脚本
```

## 需要配置API密钥的模块

| 模块 | 推荐免费服务 | 申请地址 |
|-----|------------|---------|
| LLM | ChatGLM | https://bigmodel.cn/usercenter/proj-mgmt/apikeys |
| ASR | FunASR（本地）| 无需申请 |
| TTS | EdgeTTS/LinkeraiTTS | 无需申请/https://linkerai.cn |
| VLLM | ChatGLM视觉 | https://bigmodel.cn/usercenter/proj-mgmt/apikeys |

## 更多信息

- 项目文档：https://github.com/adlink8/xiaozhi-esp32-server
- 部署文档：见项目README.md
- 常见问题：docs/FAQ.md
