---
name: branch-manager
description: |
  管理 Git 分支的创建、推送和 PR 流程。
  支持十步循环中的 B.1 (分支创建) 和 C.2 (分支合并/PR)。

  使用场景：开始新任务时创建分支、完成开发后创建 PR。

  特性: 支持主仓库和子模块内操作、集成 Forgejo API
---

# 分支管理器 (Branch Manager)

> **版本**: 1.2.0 | **十步循环**: B.1, C.2
> **更新**: 2026-01-18 - 添加 Git Worktrees 支持

## 快速开始

### 我应该使用这个 skill 吗？

**使用场景**:
- B.1: 开始新任务，需要创建功能分支
- C.2: 完成开发，需要推送并创建 PR

**不使用场景**:
- 简单的 commit 操作 → 使用 `commit-msg-generator`
- 跨模块批量提交 → 使用 `strategic-commit-orchestrator`

---

## 核心功能

| 功能 | 十步循环 | 描述 |
|------|---------|------|
| 创建分支 | B.1 | 验证环境 + 创建规范分支 + 推送远程 |
| 创建 PR | C.2 | 推送分支 + 创建 Forgejo PR + 等待审批 |

---

## B.1: 分支创建

### 触发条件

- A.3 Agent 分配完成
- 用户确认开始开发任务

### 输入参数

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `module` | ✅ | 目标模块 | `backend`, `mobile`, `shared`, `cross`, `docs`, `standards` |
| `task_id` | ✅ | 任务标识 | `TASK-001`, `ISSUE-42` |
| `description` | ✅ | 简短描述 | `user-auth`, `login-ui` |
| `branch_type` | ❌ | 分支类型 (默认 `feature`) | `feature`, `bugfix`, `hotfix`, `release`, `experiment` |
| `in_submodule` | ❌ | 是否在子模块内操作 | `true`, `false` (默认) |

### 执行流程

```yaml
B.1.1 - 环境验证:
  - 确认当前在正确的工作目录
  - 确认在 develop 分支
  - 确认工作目录干净 (无未提交变更)
  - 拉取最新的 develop

B.1.2 - 分支创建:
  - 生成分支名: {branch_type}/{module}/{task_id}-{description}
  - 创建本地分支: git checkout -b {branch_name}

B.1.3 - 推送远程:
  - 推送并设置上游: git push -u origin {branch_name}
```

### 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| feature | `feature/{module}/{task-id}-{desc}` | `feature/backend/TASK-001-user-auth` |
| bugfix | `bugfix/{module}/{issue}-{desc}` | `bugfix/mobile/ISSUE-42-login-crash` |
| hotfix | `hotfix/{version}-{desc}` | `hotfix/v1.2.1-security-patch` |
| release | `release/{version}` | `release/v1.3.0` |
| experiment | `experiment/{name}` | `experiment/openspec-pilot` |

### 模块标识符

| 模块 | 标识符 | 说明 |
|------|--------|------|
| Backend | `backend` | Python/FastAPI 服务 |
| Mobile | `mobile` | Flutter 应用 |
| Shared | `shared` | API 契约、schemas |
| Cross-module | `cross` | 多模块变更 |
| Documentation | `docs` | 仅文档变更 |
| Standards | `standards` | AI-DDD 规范 |

### 子模块操作

当 `in_submodule=true` 时：

```bash
# 1. 进入子模块目录
cd {submodule_path}  # 如 backend/, mobile/

# 2. 确保子模块 develop 最新
git checkout develop
git pull origin develop

# 3. 创建分支 (在子模块内)
git checkout -b feature/{module}/{task-id}-{desc}
git push -u origin feature/{module}/{task-id}-{desc}

# 4. 返回主仓库 (提醒用户)
cd ..
# 提醒: 完成后需要在主仓库更新子模块指针
```

---

## Git Worktrees 集成

> **新增于 v1.2.0**

Git Worktrees 允许在同一个仓库中同时检出多个分支到不同的工作目录，实现干净并行的开发。

### 何时使用 Worktrees

| 场景 | 传统方式 | Worktrees 方式 |
|------|----------|----------------|
| 同时开发多个功能 | 频繁切换分支，构建缓存失效 | 每个功能独立目录，构建隔离 |
| 紧急 hotfix | stash 当前工作，切换分支 | 直接在 worktree 中修复 |
| 代码审查 | 切换到 PR 分支查看 | 在 worktree 中并行查看 |

### Worktree 参数

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `use_worktree` | ❌ | 是否使用 worktree (默认 `false`) | `true`, `false` |
| `worktree_path` | ❌ | worktree 路径 (默认 `.git/worktrees/`) | custom path |

### 创建 Worktree 分支

```bash
# B.1 with --worktree flag
git worktree add .git/worktrees/{feature-name} feature/{module}/{task-id}-{desc}

# 完整示例
git worktree add .git/worktrees/TASK-001-user-auth feature/backend/TASK-001-user-auth
cd .git/worktrees/TASK-001-user-auth
```

### Worktree 目录结构

```
repository/
├── .git/
│   ├── worktrees/
│   │   ├── TASK-001-user-auth/
│   │   │   ├── .git                # worktree 的 git 文件
│   │   │   ├── lib/
│   │   │   ├── src/
│   │   │   └── tests/
│   │   ├── TASK-002-login-ui/
│   │   │   └── ...
│   │   └── ...
│   └── ...
├── lib/                             # 主分支工作区
├── src/
└── tests/
```

### Worktree 常用命令

```bash
# 列出所有 worktrees
git worktree list

# 创建 worktree
git worktree add <path> <branch>

# 删除 worktree
git worktree remove <path>

# 清理过期的 worktree
git worktree prune

# 移动 worktree
git worktree move <old-path> <new-path>
```

### Worktree 清理

任务完成后，清理 worktree 目录：

```bash
# 切换回主分支
cd ../..

# 删除 worktree
git worktree remove .git/worktrees/TASK-001-user-auth

# 或手动删除
rm -rf .git/worktrees/TASK-001-user-auth
git worktree prune
```

### Worktree 状态检查

```bash
# 检查所有 worktree 状态
git worktree list --porcelain

# 检查当前 worktree 分支
git branch --show-current
```

---

## 输出

```yaml
成功输出:
  branch_name: "feature/backend/TASK-001-user-auth"
  location: "main_repo" | "submodule:{name}"
  remote_push: "success"
  next_step: "开始 B.2 执行验证"

失败输出:
  error: "描述错误原因"
  suggestion: "建议的解决方案"
```

---

## C.2: 分支合并 / PR 创建

### 触发条件

- C.1 Git 提交完成
- 用户确认可以创建 PR

### 输入参数

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `branch_name` | ❌ | 分支名 (默认当前分支) | `feature/backend/TASK-001-user-auth` |
| `base_branch` | ❌ | 目标分支 (默认 `develop`) | `develop`, `main` |
| `spec_path` | ❌ | Spec 文件路径 | `standards/openspec/changes/auth/spec.md` |
| `issue_number` | ❌ | 关联的 Issue | `123` |
| `merge_strategy` | ❌ | 合并策略 (默认 `squash`) | `squash`, `merge`, `rebase` |
| `auto_merge` | ❌ | 自动合并 (默认 `false`) | `true`, `false` |

### 执行流程

```yaml
C.2.1 - 同步检查:
  - 获取最新的 develop: git fetch origin develop
  - Rebase 到最新: git rebase origin/develop
  - 解决冲突 (如有)

C.2.2 - 推送分支:
  - 推送到远程: git push origin {branch_name}
  - 如果 rebase 后需要: git push --force-with-lease origin {branch_name}

C.2.3 - 创建 PR (Forgejo):
  - 加载环境变量: source ~/.bash_profile
  - 调用 Forgejo API 创建 PR
  - 返回 PR URL

C.2.4 - 等待审批:
  - 输出 PR URL 供用户查看
  - 等待用户确认合并

C.2.5 - 合并 (可选，auto_merge=true 时):
  - 调用 Forgejo API 合并 PR
  - 删除远程分支
  - 删除本地分支
  - 切换回 develop 并更新
```

### PR 标题和正文格式

**标题格式**:
```
{type}({scope}): {中文描述} / {English description}
```

**正文模板**:
```markdown
## Summary

{从 commit 消息或 Spec 提取的摘要}

Implements: `{spec_path}` (如有)
Related Issue: #{issue_number} (如有)

## Changes

- {变更列表，从 git log 提取}

## Test Plan

- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing completed

## Checklist

- [ ] Spec acceptance criteria satisfied
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No security vulnerabilities
```

### Forgejo API 调用

**创建 PR**:
```bash
source ~/.bash_profile

forgejo-api -X POST "$FORGEJO_API/repos/10CG/todo-app/pulls" \
  -d '{
    "title": "{pr_title}",
    "body": "{pr_body}",
    "head": "{branch_name}",
    "base": "{base_branch}"
  }'
```

**合并 PR**:
```bash
# squash (推荐)
forgejo-api -X POST "$FORGEJO_API/repos/10CG/todo-app/pulls/{pr_number}/merge" \
  -d '{"Do": "squash"}'

# merge
forgejo-api -X POST "$FORGEJO_API/repos/10CG/todo-app/pulls/{pr_number}/merge" \
  -d '{"Do": "merge"}'
```

**删除远程分支**:
```bash
forgejo-api -X DELETE "$FORGEJO_API/repos/10CG/todo-app/branches/{branch_name}"
```

### 子模块 PR 注意事项

在子模块内创建的分支：

```yaml
子模块 PR 流程:
  1. 在子模块仓库创建 PR (如 10CG/todo-app-backend)
  2. 合并后，回到主仓库
  3. 更新子模块指针:
     - git add {submodule_path}
     - git commit -m "chore(submodule): update {module} pointer"
  4. 主仓库可能也需要创建 PR
```

### 输出

```yaml
成功输出:
  pr_url: "https://forgejo.10cg.pub/10CG/todo-app/pulls/42"
  pr_number: 42
  status: "open" | "merged"
  branch_cleanup: "done" | "pending"
  next_step: "等待审批" | "开始 D.1 进度更新"

失败输出:
  error: "描述错误原因"
  suggestion: "建议的解决方案"
```

---

## 完整工作流示例

### 示例 1: 在主仓库创建功能分支

```yaml
用户请求: "开始 TASK-001 用户认证功能开发"

B.1 执行:
  输入:
    module: backend
    task_id: TASK-001
    description: user-auth
    branch_type: feature
    in_submodule: false

  执行:
    1. git checkout develop && git pull origin develop
    2. git checkout -b feature/backend/TASK-001-user-auth
    3. git push -u origin feature/backend/TASK-001-user-auth

  输出:
    ✅ 分支创建成功: feature/backend/TASK-001-user-auth
    📍 位置: 主仓库
    ➡️ 下一步: 开始 B.2 执行验证
```

### 示例 2: 在子模块内创建分支

```yaml
用户请求: "在 mobile 子模块创建登录 UI 分支"

B.1 执行:
  输入:
    module: mobile
    task_id: TASK-002
    description: login-ui
    in_submodule: true

  执行:
    1. cd mobile/
    2. git checkout develop && git pull origin develop
    3. git checkout -b feature/mobile/TASK-002-login-ui
    4. git push -u origin feature/mobile/TASK-002-login-ui
    5. cd ..

  输出:
    ✅ 分支创建成功: feature/mobile/TASK-002-login-ui
    📍 位置: 子模块 mobile
    ⚠️ 提醒: 完成后需在主仓库更新子模块指针
```

### 示例 3: 创建 PR

```yaml
用户请求: "C.1 完成，创建 PR"

C.2 执行:
  输入:
    branch_name: feature/backend/TASK-001-user-auth
    base_branch: develop
    spec_path: standards/openspec/changes/user-auth/spec.md
    merge_strategy: squash

  执行:
    1. git fetch origin develop
    2. git rebase origin/develop
    3. git push --force-with-lease origin feature/backend/TASK-001-user-auth
    4. source ~/.bash_profile
    5. forgejo-api -X POST ... (创建 PR)

  输出:
    ✅ PR 创建成功
    🔗 URL: https://forgejo.10cg.pub/10CG/todo-app/pulls/42
    📋 状态: 等待审批
    ➡️ 用户确认合并后，执行 D.1
```

---

## 检查清单

### B.1 创建分支前

- [ ] 确认在正确的工作目录（主仓库或子模块）
- [ ] 确认在 develop 分支
- [ ] 确认工作目录干净
- [ ] 确认任务 ID 和描述准确

### C.2 创建 PR 前

- [ ] 确认所有 commit 已完成
- [ ] 确认测试通过
- [ ] 确认文档已更新
- [ ] 确认分支已推送到远程

### C.2 合并后

- [ ] 确认 PR 已合并
- [ ] 确认本地 develop 已更新
- [ ] 确认分支已删除（本地和远程）
- [ ] 如果是子模块，确认主仓库指针已更新

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 工作目录不干净 | 有未提交的变更 | `git stash` 或 commit 变更 |
| 分支已存在 | 分支名冲突 | 选择不同的 task_id 或 description |
| Rebase 冲突 | develop 有新变更 | 手动解决冲突后 `git rebase --continue` |
| PR 创建失败 | Forgejo API 错误 | 检查环境变量和网络连接 |
| 权限不足 | 仓库权限问题 | 联系仓库管理员 |

### 恢复操作

```bash
# 如果分支创建出错，删除分支
git branch -d {branch_name}
git push origin --delete {branch_name}

# 如果 rebase 出错，中止
git rebase --abort

# 如果需要重置到远程状态
git fetch origin
git reset --hard origin/{branch_name}
```

---

## 相关文档

- [十步循环概览](../../../standards/core/ten-step-cycle/README.md)
- [Phase B: 开发执行](../../../standards/core/ten-step-cycle/phase-b-development.md)
- [Phase C: 提交集成](../../../standards/core/ten-step-cycle/phase-c-integration.md)
- [分支管理指南](../../../standards/workflow/branch-management-guide.md)
- [Forgejo API 使用指南](../../docs/FORGEJO_API_GUIDE.md)
- [Git Commit 规范](../../../standards/conventions/git-commit.md)

---

**最后更新**: 2025-12-18
**Skill版本**: 1.1.0
