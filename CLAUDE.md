# CLAUDE.md — 项目导航与协作规则（优先级最高）

> 新会话/初始化时：**先读这个文件**。目标是让 Claude/Copilot 快速找到权威资料，并按项目约束执行。

## 1) 从哪里开始（建议顺序）

1. **工作流 Skills（怎么做事）**：`.claude/skills/index.md`
2. **参考资料 References（可查抄资料）**：`.claude/references/README.md`
3. **项目权威事实（需求/状态/任务）**：`project/`
   - `project/requirements.md`
   - `project/project-status.md`
   - `project/todo.md`
4. **系统化文档（分类索引）**：`docs/index.md`

约定：
- **Skills 只写工作流**（触发条件、步骤、约束、脚本入口）
- **项目事实**写在 `project/`
- **长文/参考/操作记录**优先放 `docs/` 或 `.claude/references/`
- 避免同一内容多处维护导致漂移

---

## 2) 当前推荐使用的 Skills

- 排障（权威入口）：`.claude/skills/diagnose-xiaozhi-issue/`
- 项目管理（权威入口）：`.claude/skills/manage-project/`
- 版本/分支工作流：`.claude/skills/repo-workflow/`

---

## 3) 项目管理约定（project 三件套 + AUTOGEN）

### 3.1 权威文件

- `project/requirements.md`：范围/目标/非目标（主要手写）
- `project/project-status.md`：现状、里程碑、风险（手写 + AUTOGEN）
- `project/todo.md`：任务清单、依赖、验收标准（手写 + AUTOGEN）

### 3.2 AUTOGEN 安全区（自动化只能写这些区块）

自动化（例如 `manage-project` 的 `-update-status` 或脚本）**只允许**修改以下区块内内容，禁止覆盖手写部分：

- `project/todo.md`：
  - `<!-- AUTOGEN:DISCOVERED_TASKS:START -->` … `<!-- AUTOGEN:DISCOVERED_TASKS:END -->`
- `project/project-status.md`：
  - `<!-- AUTOGEN:PROJECT_SNAPSHOT:START -->` … `<!-- AUTOGEN:PROJECT_SNAPSHOT:END -->`

### 3.3 触发映射（给 AI 的默认动作）

- 用户说“同步状态/更新文档” → 走 `manage-project`，只更新 AUTOGEN
- 用户说“接下来做什么/优先级” → 先读 `project/todo.md`（结构化任务优先），再给 next steps
- 用户说“现在进度怎样” → 读 `project/project-status.md` + git 状态，再总结

---

## 4) 分支与版本控制（开发/验证）

当前常用分支：
- `feat/websocket`：主要开发分支（功能迭代与文档/skills 同步）
- `test`：验证/集成分支（用于把某个稳定点对齐到可测试状态）

建议规则：
- `test` 尽量保持 **fast-forward**，避免长期分叉
- 如需从 `feat/*` 同步到 `test`：优先快进；若产生分叉，先明确采用 merge / rebase / force 的策略

---

## 5) 代码库结构速览（定位入口）

模块：
- Python（AI 引擎）：`main/xiaozhi-server/`
- Java（管理后端）：`main/manager-api/`
- Web（管理前端）：`main/manager-web/`
- Mobile（移动端）：`main/manager-mobile/`

推荐导航：
- 代码/文档定位优先看：`.claude/references/docs-nav.md`

---

## 6) 安全与操作约束

- 禁止在仓库中写入真实 API Key/Token/密码（使用占位符或环境变量说明）。
- 避免给出“按名称批量杀进程”的命令示例（如 `pkill`/`killall`）。
  - 需要停止进程：先定位 PID（`ps`/`lsof`），再精确 `kill <PID>`。

---

## 7) 提问/协作建议（让 AI 更可执行）

- 明确范围：`xiaozhi-server` / `manager-api` / `manager-web`
- 提供复现：日志、配置片段（脱敏）、复现步骤
- 复杂任务拆小：先做一个可验证的最小切片，再扩展
