---
name: phase-c-integrator
description: |
  十步循环 Phase C - 集成阶段执行器。
  编排 C.1-C.2 步骤：Git 提交、PR 创建/合并。

  使用场景：
  - "执行集成阶段"
  - "Phase C"
  - "提交代码并创建 PR"
  - 被 workflow-runner 调用

  特性: 步骤编排、智能跳过、增强提交消息
allowed-tools: Bash, Read, Write, Glob, Grep, Task
---

# Phase C - 集成阶段 (Integrator)

> **版本**: 1.0.0 | **十步循环**: C.1-C.2

## 快速开始

### 我应该使用这个 Skill 吗？

**使用场景**:
- 需要提交代码变更
- 需要创建 Pull Request
- 需要合并分支
- 开发完成后的集成阶段

**不使用场景**:
- 无变更需要提交 → 跳过 C.1
- 不需要 PR → 跳过 C.2

---

## 核心功能

| 步骤 | Skill | 职责 | 输出 |
|------|-------|------|------|
| C.1 | commit-msg-generator | Git 提交 | commit_sha, message |
| C.2 | branch-manager | PR/合并 | pr_url, pr_number |

---

## 执行流程

### 输入

```yaml
context:
  phase_cycle: "Phase4-Cycle9"
  module: "mobile"
  changed_files: ["lib/auth.dart", "test/auth_test.dart"]
  branch_name: "feature/mobile/TASK-001-add-auth"  # 来自 Phase B
  test_results:                                     # 来自 Phase B
    passed: true
    coverage: 87.5

config:
  skip_steps: []
  params:
    enhanced_markers: true        # 使用增强提交标记
    create_pr: true               # 是否创建 PR
```

### 步骤执行

```yaml
C.1 - Git 提交:
  skill: commit-msg-generator
  params:
    enhanced_markers: true
    subagent_type: "from_context"
    phase_cycle: "from_context"
    module: "from_context"
  skip_if:
    - no_changes_to_commit: true
  action:
    - 分析暂存区变更
    - 生成规范提交消息
    - 执行 git commit
  output:
    commit_sha: "abc1234"
    commit_message: "feat(auth): 添加用户认证..."

C.2 - PR/合并:
  skill: branch-manager
  action: pr
  skip_if:
    - no_pr_needed: true
    - direct_push_allowed: true
  action:
    - 推送分支到远程
    - 创建 Pull Request
    - (可选) 自动合并
  output:
    pr_url: "https://..."
    pr_number: 123
```

### 输出

```yaml
success: true
steps_executed: [C.1, C.2]
steps_skipped: []
results:
  C.1:
    commit_sha: "abc1234"
    commit_message: "feat(auth): 添加用户认证..."
  C.2:
    pr_url: "https://..."
    pr_number: 123

context_for_next:
  commit_sha: "abc1234"
  pr_url: "https://..."
```

---

## 跳过规则

| 条件 | 跳过步骤 | 检测方法 |
|------|---------|----------|
| 无变更 | C.1 | git status --porcelain 为空 |
| 不需要 PR | C.2 | 配置或分支策略 |
| 直接推送 | C.2 | 在 develop 分支 |

### 跳过逻辑

```yaml
skip_evaluation:
  C.1:
    - check: git status --porcelain
      skip_if: empty
      reason: "没有需要提交的变更"

  C.2:
    - check: branch_name
      skip_if: in [develop, main]
      reason: "主分支不需要 PR"

    - check: config.create_pr
      skip_if: false
      reason: "配置为不创建 PR"
```

---

## 输出格式

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE C - INTEGRATION                           ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  C.1 commit-msg-generator  → Git 提交
  C.2 branch-manager        → 创建 PR

🚀 执行中...
───────────────────────────────────────────────────────────────
  ✅ C.1 完成 → Commit: abc1234
     Message: feat(auth): 添加用户认证 / Add user authentication

  ✅ C.2 完成 → PR #123 已创建
     URL: https://github.com/...

📤 上下文输出
───────────────────────────────────────────────────────────────
  commit: abc1234
  pr: #123
  ready_for: Phase D (可选)
```

---

## 使用示例

### 示例 1: 完整集成

```yaml
输入:
  context:
    branch_name: "feature/add-auth"
    test_results: { passed: true }

执行:
  C.1: 提交代码 → abc1234
  C.2: 创建 PR → #123

输出:
  commit_sha: "abc1234"
  pr_url: "https://..."
```

### 示例 2: 仅提交

```yaml
输入:
  config:
    create_pr: false

执行:
  C.1: 提交代码
  C.2: 跳过 (不需要 PR)

输出:
  steps_skipped: [C.2]
  commit_sha: "abc1234"
```

### 示例 3: 直接推送

```yaml
输入:
  context:
    branch_name: "develop"  # 在主分支

执行:
  C.1: 提交代码
  C.2: 跳过 (主分支不需要 PR)
  额外: git push

输出:
  commit_sha: "abc1234"
  pushed: true
```

---

## 提交消息增强

### 增强标记格式

```
feat(auth): 添加用户认证 / Add user authentication

- 实现 JWT token 验证
- 添加登录 API 端点

🤖 Executed-By: mobile-developer subagent
📋 Context: Phase4-Cycle9 功能开发
🔗 Module: mobile
```

### 标记来源

| 标记 | 来源 |
|------|------|
| 🤖 Executed-By | 执行的 Agent 类型 |
| 📋 Context | Phase/Cycle + 任务描述 |
| 🔗 Module | 活跃模块名 |

---

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| 提交失败 | hook 拒绝 | 显示 hook 错误，提示修复 |
| PR 创建失败 | 权限问题 | 提示检查权限 |
| 推送失败 | 远程冲突 | 提示拉取最新代码 |

### Hook 失败处理

```yaml
on_commit_hook_failure:
  action: stop
  report:
    - Hook 错误信息
    - 缺少的标记或格式问题
  next_step: "使用 commit-msg-generator 重新生成消息"
```

---

## 与其他 Phase 的关系

```
phase-b-developer
    │
    │ context:
    │   - branch_name
    │   - test_results
    ▼
phase-c-integrator (本 Skill)
    │
    │ context_for_next:
    │   - commit_sha
    │   - pr_url
    ▼
phase-d-closer
```

---

## 相关文档

- [commit-msg-generator](../commit-msg-generator/SKILL.md) - C.1 提交生成
- [branch-manager](../branch-manager/SKILL.md) - C.2 PR/合并
- [phase-b-developer](../phase-b-developer/SKILL.md) - 上一阶段
- [phase-d-closer](../phase-d-closer/SKILL.md) - 下一阶段

---

**最后更新**: 2025-12-25
**Skill版本**: 1.0.0
