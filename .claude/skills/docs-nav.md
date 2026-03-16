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
- `.claude/skills/troubleshooting.md`：统一故障诊断手册（排障优先看这里）

## 建议用法

- 想找“怎么部署/怎么跑”：先看 `README.md` + `docs/`，再看 `.claude/references/`
- 想排障：直接从 `.claude/skills/troubleshooting.md` 的目录进入
- 想定位代码位置：优先从 `main/` 下按模块（xiaozhi-server / manager-api / manager-web）查入口文件
