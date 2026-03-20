---
name: docs
description: 项目文档与代码库导航索引（快速定位 README/docs/关键入口）
doc_version:
---

# 文档导航（Docs）

用于快速定位本仓库的文档入口与“去哪里找什么”。

## 主要入口

- 仓库总览：`/README.md`
- 详细文档：`/docs/`
- 模块说明：`/main/README.md`

## Claude/Copilot 辅助资料

- `.claude/references/`：参考资料（部署、配置、FAQ 等）
- 排障 Skill（权威入口）：`.claude/skills/diagnose-xiaozhi-issue/`
- 项目管理 Skill（权威入口）：`.claude/skills/manage-project/`

## 建议用法

- 想找“怎么部署/怎么跑”：先看 `README.md` → `docs/index.md`，再看 `.claude/references/`
- 想做项目规划/状态同步：看 `project/` 三件套（requirements / project-status / todo），再用 `manage-project` 工作流
- 想排障：从 `.claude/skills/diagnose-xiaozhi-issue/SKILL.md` 进入
- 想定位代码位置：优先从 `main/` 下按模块（xiaozhi-server / manager-api / manager-web）查入口文件
