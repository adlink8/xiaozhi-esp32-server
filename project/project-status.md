# 项目状态（project/project-status.md）

> 本文件分为两部分：
> - **AUTOGEN 快照**：脚本自动更新（只读）。
> - **手写状态**：你维护的项目事实与阶段目标。

<!-- AUTOGEN:PROJECT_SNAPSHOT:START -->
_Generated at: 2026-03-20 22:39:23 +0800_

- Git branch: `feat/websocket`
- Git HEAD: `a5d00b8d`
- TODO/FIXME in repo: TODO=0, FIXME=0

### Recent commits (5)
```
a5d00b8d Update CLAUDE.md navigation
d642cb25 Reorganize docs and skills navigation
d869f573 feat: add manage-project skill and project docs
f70717a3 feat: Add initial documentation files for project requirements, status, and todo list
40518f63 feat: Add project management workflow and troubleshooting manual
```

### Working tree (porcelain)
```
M project/project-status.md
```
<!-- AUTOGEN:PROJECT_SNAPSHOT:END -->

---

## 1. 基本信息（手写）

- **项目名称**：xiaozhi-esp32-server
- **主要模块**：
  - `main/xiaozhi-server`：Python AI 引擎（WebSocket + ASR/TTS/LLM）
  - `main/manager-api`：Java Spring Boot 管理后端
  - `main/manager-web`：Vue.js Web 管理前端
  - `main/manager-mobile`：uni-app 移动端
- **部署方式**（按你的实际情况补充）：
  - Docker 最简化安装 / 全模块安装（参考 `docs/deployment/` + `docs/index.md`）
  - 源码模式运行（参考 `.claude/references/config-local-run-guide.md`）

---

## 2. 模块状态概览（手写）

> 建议状态：`✅ 已可用` / `🟡 可用但待优化` / `🚧 开发中` / `❌ 未启用`

| 模块 | 位置 | 状态 | 说明 |
|------|------|------|------|
| Python AI 引擎 | `main/xiaozhi-server` | 🟡 | 基本语音链路已具备，部分 ASR/LLM/TTS 组合需按环境调试 |
| Java 管理后端 | `main/manager-api` | 🟡 | 接口已经成型，具体配置和权限策略视实际部署而定 |
| Web 管理前端 | `main/manager-web` | 🟡 | 智控台页面可用，样式与功能后续可继续优化 |
| 移动端（H5/uni-app） | `main/manager-mobile` | 🚧 | 基本结构就绪，按移动端场景继续完善 |

---

## 3. 进行中的工作（手写）

- （例）优化本地开发体验（config、日志、调试脚本）
- （例）完善管理端功能（用户/设备/更多可视化）
- （例）整理文档体系与项目管理三件套

---

## 4. 待办总览（手写）

> 详细拆解在 `project/todo.md`。

- P0：
  - 稳定一条语音交互链路（设备 → ASR → LLM → TTS → 设备）
  - 基础安全与配置检查（密钥管理、端口暴露、Docker/源码一致性）
- P1：
  - 完善管理端多设备视图与操作
  - 优化集成文档入口与可复现性
- P2：
  - 清理 TODO/FIXME
  - 统一部分代码/配置规范

---

## 5. 风险与问题记录（手写）

- （例）公网暴露后的安全性与限流策略尚未系统评估
- （例）部分云服务在网络不佳时延迟明显

---

## 6. 更新记录（手写）

> 这里记录“对开发协作有影响”的变更（文档结构、skills 工作流、分支约定等）。

| 日期 | 修改人 | 变更内容 |
|------|--------|----------|
| 2026-03-20 | Copilot + 用户 | 重构 CLAUDE.md 为首屏导航与规则；对齐 skills/references/project/docs 的权威入口；补充分支约定（feat/websocket + test）。 |
| 2026-03-20 | Copilot + 用户 | docs 按主题分类（deployment/hardware/integrations/operations/tools/community），并更新 docs 索引与相关链接。 |
| 2026-03-20 | Copilot + 用户 | skills 索引与导航对齐：新增 `.claude/skills/index.md`；排障统一入口迁移到 `diagnose-xiaozhi-issue`；`project-management.md/ip-change.md` 等旧入口删除/弃用。 |
| 2026-03-20 | Copilot + 用户 | `.claude/references/README.md` 增强为导航入口；`docs-nav/hardware-setup` 归档到 `.claude/references/`。 |
| 2026-03-16 | （历史） | 创建初稿：模块概览 + 状态表 + 待办视图 |
