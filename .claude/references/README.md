# .claude/references（参考资料库）

这里存放“可复用的工程参考资料”，用于辅助排障/开发时快速查阅（尤其给 Copilot/Claude 提供上下文）。

## 放什么

- **高价值、可复用** 的操作指南/模板/索引
- 依赖关系图、架构/接口梳理等“辅助理解材料”

## 不放什么

- 与 `docs/` 完全重复的副本文档（`docs/` 才是对外/权威文档）
- 含真实密钥/Token/密码的内容

## 推荐入口

- 本地源码运行：[`config-local-run-guide.md`](./config-local-run-guide.md)
- 依赖图：`dependencies/`（dot/mmd/json）
- 项目正式文档：仓库根目录的 `docs/`
