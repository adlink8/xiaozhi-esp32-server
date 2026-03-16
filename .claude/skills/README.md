# .claude/skills 技能索引

本目录是“技能/手册”的入口索引。

> 约定：**README 只做索引**（只放链接与简述），详细步骤只维护在对应文档中，避免重复与漂移。

## 快速入口

- 故障诊断（统一入口）：[`troubleshooting.md`](./troubleshooting.md)
- 本地源码运行（无需 Docker）：[`../references/config-local-run-guide.md`](../references/config-local-run-guide.md)
- 硬件连接与基础配置：[`hardware-setup.md`](./hardware-setup.md)
- 项目管理工作流：[`project-management.md`](./project-management.md)
- 项目文档与代码导航：[`docs-nav.md`](./docs-nav.md)

## 故障诊断索引（Troubleshooting）

> 详细步骤统一维护在 [`troubleshooting.md`](./troubleshooting.md)。

### 🔐 认证与配置
- [`server-secret-mismatch`](./troubleshooting.md#server-secret-mismatch)
- [`server-ota-config`](./troubleshooting.md#server-ota-config)

### OTA
- [`ota-connection-error`](./troubleshooting.md#ota-connection-error)
- [`ota-404-fix`](./troubleshooting.md#ota-404-fix)
- [`ota-upgrade-fail`](./troubleshooting.md#ota-upgrade-fail)

### 🌐 网络与容器
- [`container-port-mapping`](./troubleshooting.md#container-port-mapping)
- [`ip-change-solution`](./troubleshooting.md#ip-change-solution)

## 文档维护注意事项

- **不要在任何文档中写入真实 API Key/Token/密码**；请使用占位符（如 `<YOUR_API_KEY>`）或环境变量说明。
- 新增/合并技能：
  1) 排障类优先更新 `troubleshooting.md`
  2) 其他主题新增独立文档
  3) 最后仅在本 README 增加索引链接
