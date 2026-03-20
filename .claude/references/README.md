# .claude/references（参考资料库）

这里存放“可复用的工程参考资料”，用于辅助排障/开发时快速查阅（尤其给 Copilot/Claude 提供上下文）。

> 目标：**不搬动文件，只提供一个权威导航入口**，让 Claude/Copilot 能快速“查抄”到正确资料。

## 放什么

- **高价值、可复用** 的操作指南/模板/索引
- 依赖关系图、架构/接口梳理等“辅助理解材料”

## 不放什么

- 与 `docs/` 完全重复的副本文档（`docs/` 才是对外/权威文档）
- 含真实密钥/Token/密码的内容

## 快速导航（给 Claude/Copilot）

### 1) 想按工作流执行（skills）

- skills 总入口：[`../skills/index.md`](../skills/index.md)
  - 排障：`../skills/diagnose-xiaozhi-issue/`
  - 项目管理：`../skills/manage-project/`

### 2) 想看项目权威事实（project 三件套）

- `project/requirements.md`
- `project/project-status.md`
- `project/todo.md`

（以上文件在仓库根目录的 `project/` 下，适合放“当前项目专有事实/状态/计划”。）

### 3) 想找对外/系统化文档（docs）

- docs 总索引：`docs/index.md`

## 本目录内容索引

- 本地源码运行：[`config-local-run-guide.md`](./config-local-run-guide.md)
- 文档与代码导航（项目内快速定位）：[`docs-nav.md`](./docs-nav.md)
- 硬件连接与环境配置（项目私有记录）：[`hardware-setup.md`](./hardware-setup.md)
- 依赖图：`dependencies/`（dot/mmd/json）
- 其他资料汇总：[`documentation/README.md`](./documentation/README.md)

## 维护规则

- references 里的文档如果变成“项目权威事实”，请迁移到根目录 `project/`（避免漂移）。
- 所有路径尽量使用相对链接，避免环境差异。
- 禁止提交任何真实密钥/Token/密码。
