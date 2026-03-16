# 文档索引（docs/index.md）

> 本文件用于快速总览 `docs/` 目录中的文档，并按用途分类。建议从这里入口查找需要的文档。

---

## 1. 项目管理（三件套）

- [requirements.md](./requirements.md)  
  项目整体目标、范围、功能 / 非功能需求、阶段规划与验收标准。
- [project-status.md](./project-status.md)  
  模块状态总览、已完成/进行中/待办事项、环境与版本信息。
- [todo.md](./todo.md)  
  按高/中/低优先级拆解的任务清单，配合项目状态使用。

---

## 2. 部署与运行

- [Deployment.md](./Deployment.md)  
  最简化安装方式（Docker / 源码只运行 server）。
- [Deployment_all.md](./Deployment_all.md)  
  全模块安装方式（server + manager-api + manager-web 等）。
- [docker-build.md](./docker-build.md)  
  Docker 镜像构建与相关说明。
- [firmware-build.md](./firmware-build.md)  
  ESP32 固件构建指南。
- [firmware-setting.md](./firmware-setting.md)  
  固件参数与设备侧配置说明。
- [dev-ops-integration.md](./dev-ops-integration.md)  
  源码部署自动更新、DevOps 集成方案。
- [ota-upgrade-guide.md](./ota-upgrade-guide.md)  
  OTA 升级流程与注意事项。
- [paddlespeech-deploy.md](./paddlespeech-deploy.md)  
  PaddleSpeech 本地部署说明（兼具部署与语音能力集成）。

---

## 3. 组件与服务集成

### 3.1 ASR / TTS / 语音相关

- [fish-speech-integration.md](./fish-speech-integration.md)  
  FishSpeech 集成配置。
- [huoshan-streamTTS-voice-cloning.md](./huoshan-streamTTS-voice-cloning.md)  
  火山流式 TTS / 声音克隆配置。
- [voiceprint-integration.md](./voiceprint-integration.md)  
  声纹识别（3D-Speaker 等）集成。

### 3.2 记忆 / 知识库

- [powermem-integration.md](./powermem-integration.md)  
  PowerMem 智能记忆与本地总结集成。
- [ragflow-integration.md](./ragflow-integration.md)  
  RAGFlow 检索增强生成集成。

### 3.3 MCP / 工具 / 网关

- [mqtt-gateway-integration.md](./mqtt-gateway-integration.md)  
  MQTT+UDP 网关接入与配置。
- [mcp-get-device-info.md](./mcp-get-device-info.md)  
  通过 MCP 获取设备信息的用法说明。
- [mcp-endpoint-integration.md](./mcp-endpoint-integration.md)  
  MCP 服务端接入点集成方案。
- [mcp-endpoint-enable.md](./mcp-endpoint-enable.md)  
  MCP 接入点启用/禁用与配置说明。
- [mcp-vision-integration.md](./mcp-vision-integration.md)  
  视觉类 MCP 能力集成。

### 3.4 其他插件与外部系统

- [homeassistant-integration.md](./homeassistant-integration.md)  
  HomeAssistant 集成与设备联动。
- [weather-integration.md](./weather-integration.md)  
  天气插件配置与使用。
- [index-stream-integration.md](./index-stream-integration.md)  
  Index-TTS / 流式能力集成说明。
- [ali-sms-integration.md](./ali-sms-integration.md)  
  阿里云短信服务集成配置。
- [context-provider-integration.md](./context-provider-integration.md)  
  上下文提供者（Context Provider）集成方式。
- [newsnow_plugin_config.md](./newsnow_plugin_config.md)  
  新闻播报 / NewsNow 插件配置。

---

## 4. 运维 / 故障排查 / 工具

- [FAQ.md](./FAQ.md)  
  常见问题与答案集合。
- [performance_tester.md](./performance_tester.md)  
  性能测试工具说明（ASR/LLM/TTS 等核心模块压测）。
- [ip-change-solution.md](./ip-change-solution.md)  
  服务器 IP 变更后的处理与排查步骤。

---

## 5. 社区与贡献

- [contributor_open_letter.md](./contributor_open_letter.md)  
  致开发者的公开信：贡献方式、项目愿景与合作方式。

---

## 6. 使用建议

- 需要做 **需求/规划** 时：
  - 从「项目管理（三件套）」三篇文档开始（requirements / project-status / todo）。
- 需要做 **部署 / 升级 / 迁移** 时：
  - 优先阅读「部署与运行」相关文档（Deployment 系列、firmware-*、ota-upgrade-guide 等）。
- 需要开启 **某个具体能力或外部服务** 时：
  - 在「组件与服务集成」中按类别找到对应的 *integration* 文档。
- 遇到问题需要 **排查 / 调优** 时：
  - 先看 FAQ 与运维类文档，再结合项目状态与 TODO 做记录和跟踪。
