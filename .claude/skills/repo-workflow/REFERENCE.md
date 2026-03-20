# Repo Workflow Reference

> 本文是把 `me/WORKFLOW.md` 抽象成可复用 skill 的参考流程（适用于 fork 二次开发：上游同步 + 三层分支）。

## 0. 目标

- `main`（正式版）始终可部署/可回滚
- `test`（测试版）用于集成与解决冲突
- `feat/*` `fix/*` `debug/*` 分支用于开发与排错
- `upstream-main` 分支保持与上游官方仓库完全一致，用于同步上游

关键原则：
- 上游更新永远先进入 `test`，再进入 `main`
- 开发也永远先进入 `test`，再进入 `main`

---

## 1. 分支角色（Branch Roles）

### 1) upstream-main（上游官方镜像分支）

- 作用：只做一件事 —— 镜像 upstream 的默认分支（`upstream/main` 或 `upstream/master`）
- 规则：
  - 不允许在 `upstream-main` 上做任何本地开发改动
  - 每次同步上游时，使用 `git reset --hard upstream/<default>` 强制对齐
  - 允许 `git push -f origin upstream-main`（只对这个分支允许强推）

### 2) test（测试/集成分支）

- 作用：集成功能、解决冲突、跑验证（check/smoke）
- 合入来源：
  - `feat/*` `fix/*` `debug/*` 分支
  - `upstream-main`（上游同步）
- 规则：
  - 所有 PR 默认先合并到 `test`
  - 上游同步产生冲突只允许在 `test` 解决
  - `test` 必须至少通过 smoke test 才能合入 `main`

### 3) main（正式/发布分支）

- 作用：正式可发布版本（必须可运行/可部署/可回滚）
- 合入来源：只允许从 `test` 合并
- 规则：
  - 禁止直接在 `main` 开发
  - 禁止 `main` 直接 merge `upstream-main`
  - 发布可打 tag（例如 `v0.1.0`）用于快速回滚

### 4) feat/* fix/* debug/*（开发分支）

- 命名建议：
  - `feat/<topic>`：新功能
  - `fix/<topic>`：修复
  - `debug/<topic>`：排错（允许临时日志/临时验证代码）
- 规则：
  - 从 `test` 拉出：
    ```bash
    git switch test
    git pull
    git switch -c feat/<topic>
    ```
  - 完成后开 PR 合入 `test`
  - `debug` 分支合入 `test` 前需要清理临时代码，或用开关禁用（默认关闭）

---

## 2. Remote 配置（一次性）

本仓库是 fork，需要配置 upstream：

```bash
git remote -v
# 如果还没有 upstream：
git remote add upstream <UPSTREAM_GIT_URL>
git fetch upstream
```

---

## 3. 同步上游（Upstream Sync）

### Step A：更新 upstream-main（镜像上游）
```bash
git fetch upstream
git switch upstream-main || git switch -c upstream-main
git reset --hard upstream/main   # 或 upstream/master
git push -f origin upstream-main
```

### Step B：合入 test（只在 test 解决冲突）
```bash
git switch test
git pull
git merge upstream-main
```

### Step C：test 稳定后合入 main
```bash
git switch main
git pull
git merge test
git push
```

（可选）打 tag：
```bash
git tag v0.1.0
git push origin v0.1.0
```

---

## 4. 开发新功能（Feature Development）

```bash
git switch test
git pull
git switch -c feat/<topic>
# 开发...
git add -A
git commit -m "feat: <message>"
git push -u origin feat/<topic>
```

---

## 5. Debug 分支（排错）建议

- 用 `debug/<topic>`，允许临时日志但要可控（开关/环境变量）
- 排错结论要沉淀到排障手册或项目文档
