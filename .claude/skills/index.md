# .claude/skills 技能索引

本目录用于存放可复用的“工作流 skill”，并提供统一入口。

> 约定：索引文件只放**链接与简述**；详细步骤只维护在对应 skill 的 `SKILL.md/REFERENCE.md` 中，避免重复与漂移。

## 快速入口

- 故障诊断（权威入口）：[`diagnose-xiaozhi-issue/SKILL.md`](./diagnose-xiaozhi-issue/SKILL.md)
- 项目管理（权威入口）：[`manage-project/SKILL.md`](./manage-project/SKILL.md)
- Git 工作流（fork/upstream/分支策略）：[`repo-workflow/SKILL.md`](./repo-workflow/SKILL.md)
- 写一个新 skill 的流程：[`write-a-skill/SKILL.md`](./write-a-skill/SKILL.md)

参考资料（项目私有/事实类文档，不属于工作流 skill）：
- 文档与代码导航：[`../references/docs-nav.md`](../references/docs-nav.md)
- 硬件连接与环境配置：[`../references/hardware-setup.md`](../references/hardware-setup.md)

项目“事实文档”入口（权威来源）：
- 项目三件套：[`project/requirements.md`](../../project/requirements.md)、[`project/project-status.md`](../../project/project-status.md)、[`project/todo.md`](../../project/todo.md)
- docs 总索引：[`docs/index.md`](../../docs/index.md)

## 故障诊断索引（Troubleshooting）

> 排障全文只维护一份：[`diagnose-xiaozhi-issue/REFERENCE.md`](./diagnose-xiaozhi-issue/REFERENCE.md)

- 🔐 认证与配置：
  - [`server-secret-mismatch`](./diagnose-xiaozhi-issue/REFERENCE.md#server-secret-mismatch)
  - [`server-ota-config`](./diagnose-xiaozhi-issue/REFERENCE.md#server-ota-config)
- OTA：
  - [`ota-connection-error`](./diagnose-xiaozhi-issue/REFERENCE.md#ota-connection-error)
  - [`ota-404-fix`](./diagnose-xiaozhi-issue/REFERENCE.md#ota-404-fix)
  - [`ota-upgrade-fail`](./diagnose-xiaozhi-issue/REFERENCE.md#ota-upgrade-fail)
- 🌐 网络与容器：
  - [`container-port-mapping`](./diagnose-xiaozhi-issue/REFERENCE.md#container-port-mapping)
  - [`ip-change-solution`](./diagnose-xiaozhi-issue/REFERENCE.md#ip-change-solution)

## Legacy（兼容入口）

- `troubleshooting.md`：已降级为 stub，仅用于兼容旧入口（权威内容在 diagnose-xiaozhi-issue）。

## 维护注意事项

- 不要在任何文档中写入真实 API Key/Token/密码；使用占位符或环境变量说明。
- 排障类内容只更新 `diagnose-xiaozhi-issue/REFERENCE.md`，避免多处重复维护。
- `manage-project` 自动化只允许写 AUTOGEN 区块，禁止覆盖手写内容。
