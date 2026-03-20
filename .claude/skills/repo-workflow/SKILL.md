---
name: repo-workflow
description: Standard Git workflow for forked development (upstream sync + test/main + feat|fix|debug branches). Use when user asks how to sync upstream, manage branches, open PRs, release, or says "workflow".
---

# Repo Workflow（Fork 二次开发：上游同步 + 三层分支）

目标：把“固定顺序的 git 操作”固化成可复用工作流，减少口头约定与临时发挥。

## 适用场景（何时用）

- 你是 fork 仓库，需要定期同步上游（upstream）更新
- 你希望用 `main/test/feat|fix|debug` 分层，保证 **main 永远可回滚/可部署**
- 你想把“上游同步、冲突处理、发布打 tag”变成固定流程

## 约定（关键原则）

- 上游更新永远：`upstream-main → test → main`
- 本地开发永远：`feat|fix|debug → test → main`
- 冲突只在 `test` 解决
- `upstream-main` 只做镜像：禁止本地开发改动

## 执行入口（你可以这样用我）

当你说：
- “怎么同步上游？” → 我按 REFERENCE 的 **Upstream Sync** 流程输出可直接运行的命令
- “分支怎么分层？” → 我解释分支职责 + 给出新功能/修复/排错的标准落地步骤
- “准备发布/回滚怎么做？” → 我按 **Release/Tag** 流程给步骤

> 参考全文在：`.claude/skills/repo-workflow/REFERENCE.md`
