---
name: manage-project
description: Automate xiaozhi-esp32-server project lifecycle with intelligent task prioritization, progress tracking, and safe documentation sync. Use when user runs -start/-progress/-next/-update-status, or asks about project status/next steps.
---

# Project Management — xiaozhi-esp32-server

这个 skill 的目标：**少猜测、可执行、可安全自动更新**。

## 何时使用（触发）

- `-start`：初始化上下文快照（模块、git、TODO/FIXME、阶段）
- `-progress`：计算整体进度与关键缺口
- `-next`：根据任务结构化信息 + 评分体系，给出下一步任务序列（含依赖）
- `-update-status`：**只更新 AUTOGEN 区块**，不会覆盖你手写内容

自然语言触发：
- “项目现在什么状态/进度如何” → `-start` + `-progress`
- “接下来做什么/优先级怎么排” → `-next`
- “同步一下文档/更新状态” → `-update-status`

---

## Skill 文件约定（非常重要）

这个工作流只读写仓库中的以下文件（不在 skill 目录内复制项目文档，以免和大量 docs 混在一起、也避免重复维护）：

- `project/requirements.md`：需求与范围（主要是手写）
- `project/project-status.md`：项目状态总览（手写 + AUTOGEN）
- `project/todo.md`：任务清单（手写 + AUTOGEN，建议结构化）
- `.claude/skills/manage-project/REFERENCE.md`：优先级评分体系与推断规则
- `.claude/skills/manage-project/SKILL.md`：使用说明（本文件）

### AUTOGEN 安全区（可自动更新）

`-update-status` **只能**修改以下标记之间的内容，其他内容必须保留：

- `project/todo.md`：
  - `<!-- AUTOGEN:DISCOVERED_TASKS:START -->` … `<!-- AUTOGEN:DISCOVERED_TASKS:END -->`
- `project/project-status.md`：
  - `<!-- AUTOGEN:PROJECT_SNAPSHOT:START -->` … `<!-- AUTOGEN:PROJECT_SNAPSHOT:END -->`

---

## todo.md 的结构化任务格式（推荐）

为了让 `-next` 的排序更“确定”、更少主观，请尽量把任务写成下面格式（字段可逐步补全）：

```md
- [ ] (mp-001) 任务标题
  - module: xiaozhi-server | manager-api | manager-web | manager-mobile | ops | docs
  - status: planned | in_progress | blocked | done
  - deps: [mp-000]              # 可空
  - acceptance: 具体验收标准
  - scores:                    # 可选：你写了就优先采用
      impact: 0-10
      effort: 0-10
      risk: 0-10
      dependencies: 0-10
      urgency: 0-10
```

如果缺少 `scores`，则按 `REFERENCE.md` 的规则做推断，但会更不稳定。

---

## 可执行脚本（提升自动化）

脚本都在 `scripts/` 里：

- `scripts/scan_todos.py`：扫描仓库 TODO/FIXME
- `scripts/git_snapshot.sh`：输出 git 快照
- `scripts/update_autogen.py`：更新 AUTOGEN 区块（推荐用于 `-update-status`）

运行示例（在仓库根目录执行）：

```bash
python3 .claude/skills/manage-project/scripts/update_autogen.py
```
