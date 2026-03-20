# 项目待办（project/todo.md）

> 这是项目的**权威任务清单**。本文件分为两部分：
> - **AUTOGEN 区**：由脚本自动更新（只读），用于发现代码中的 TODO/FIXME。
> - **手写区**：你维护的真实任务（建议结构化），用于 `-next/-progress` 等工作流。

<!-- AUTOGEN:DISCOVERED_TASKS:START -->
_Generated at: 2026-03-20 21:21:27 +0800_

- Totals: TODO=0, FIXME=0

### Top TODO/FIXME occurrences (first 80)
<!-- AUTOGEN:DISCOVERED_TASKS:END -->

---

## 结构化任务格式（推荐）

把任务写成结构化条目，能显著降低 `-next` 的主观性：

```md
- [ ] (mp-001) 任务标题
  - module: xiaozhi-server | manager-api | manager-web | manager-mobile | ops | docs
  - status: planned | in_progress | blocked | done
  - deps: [mp-000]            # 可空
  - acceptance: 具体验收标准（可验证/可复现）
  - scores:                   # 可选：你填了就优先采用
      impact: 0-10
      effort: 0-10
      risk: 0-10
      dependencies: 0-10
      urgency: 0-10
```

约定：
- `(mp-xxx)` 必须唯一；任务完成后把 `status` 标为 `done`。
- `deps` 用来表达依赖关系，避免并行推进时互相阻塞。

---

## 高优先级（P0）

- [ ] (mp-001) 打通目标环境下的语音交互主链路
  - module: xiaozhi-server
  - status: planned
  - deps: []
  - acceptance: 从唤醒词开始，到设备播报回答，连续 10 轮对话无异常中断

- [ ] (mp-002) 明确当前使用的 ASR/LLM/TTS 组合，并写入配置与文档
  - module: docs
  - status: planned
  - deps: []
  - acceptance: 在 `project/requirements.md` 或配置文件中能明确看到当前组合、关键参数与替换方式

- [ ] (mp-003) 整理敏感配置（API key、数据库密码等）的管理方式
  - module: ops
  - status: planned
  - deps: []
  - acceptance: 仓库中无明文密钥；有一份简短的“配置说明”并可在新机器上复现

---

## 中优先级（P1）

- [ ] (mp-010) 更新 `project/project-status.md` 中的模块状态与说明
  - module: docs
  - status: planned
  - deps: []
  - acceptance: 状态表与“进行中的工作”反映你当前真实进度

- [ ] (mp-011) 将常用部署方式与注意事项整理为“我的环境笔记”
  - module: ops
  - status: planned
  - deps: []
  - acceptance: 换机器/重装环境时可以按笔记在 30 分钟内恢复可运行状态

- [ ] (mp-012) 梳理 manager-api / manager-web / manager-mobile 的关键页面与接口
  - module: manager-web
  - status: planned
  - deps: []
  - acceptance: 能说清楚“核心管理动作”对应哪些前后端文件与接口

---

## 低优先级（P2）

- [ ] (mp-020) 清理项目代码中的 TODO/FIXME（优先 main/）
  - module: ops
  - status: planned
  - deps: []
  - acceptance: 主业务路径上不再有明显 TODO/FIXME（或已变为结构化任务并在此追踪）

- [ ] (mp-021) 固化并执行一套最小项目规范（代码/配置/目录约定）
  - module: docs
  - status: planned
  - deps: []
  - acceptance: 新增代码基本遵循约定；关键脚本/命令入口能在文档中找到

- [ ] (mp-022) 为集成文档增加更多“能复制粘贴”的例子（可选）
  - module: docs
  - status: planned
  - deps: []
  - acceptance: 你自己未来再看文档也能快速上手

---

## 文档维护（长期）

- [ ] (mp-030) 定期审阅 `project/requirements.md` 与 `project/project-status.md`
  - module: docs
  - status: planned
  - deps: []
  - acceptance: 主要目标与当前状态不会相差太远

- [ ] (mp-031) 完成阶段性目标后，更新 `project/todo.md` 与 `project/project-status.md`
  - module: docs
  - status: planned
  - deps: []
  - acceptance: 能通过两份文档快速回忆“最近一段时间做了什么”

---

## 你的自定义任务区

> 可以按模块或场景分类，例如：
> - Python AI 引擎
> - Java 管理后端
> - Web 管理端
> - 移动端
> - 部署与运维

- [ ] (mp-100) （示例）为某个特定场景设计并验证一套完整的 Demo 流程
  - module: docs
  - status: planned
  - deps: []
  - acceptance: 有一份可复现的演示步骤（从部署到展示）
