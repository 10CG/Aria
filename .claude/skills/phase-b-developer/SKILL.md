---
name: phase-b-developer
description: |
  十步循环 Phase B - 开发阶段执行器。
  编排 B.1-B.3 步骤：分支管理、测试验证、架构同步。

  使用场景：
  - "执行开发阶段"
  - "Phase B"
  - "创建分支并运行测试"
  - 被 workflow-runner 调用

  特性: 步骤编排、智能跳过、测试验证、架构同步
allowed-tools: Bash, Read, Write, Glob, Grep, Task
---

# Phase B - 开发阶段 (Developer)

> **版本**: 1.1.0 | **十步循环**: B.1-B.3
> **更新**: 2026-01-18 - 添加 Worktree 支持和两阶段评审机制

## 快速开始

### 我应该使用这个 Skill 吗？

**使用场景**:
- 需要创建功能分支
- 需要运行测试验证
- 需要同步架构文档
- 代码开发完成后的验证阶段

**不使用场景**:
- 已在功能分支 → 跳过 B.1
- 无测试文件 → B.2 降级模式
- 无架构变更 → 跳过 B.3

---

## 核心功能

| 步骤 | Skill | 职责 | 输出 |
|------|-------|------|------|
| B.1 | branch-manager | 分支创建 | branch_name |
| B.2 | test-verifier | 测试验证 | test_passed, coverage |
| B.3 | arch-update | 架构同步 | arch_updated |

---

## 执行流程

### 输入

```yaml
context:
  phase_cycle: "Phase4-Cycle9"
  module: "mobile"
  changed_files: ["lib/auth.dart", "test/auth_test.dart"]
  spec_id: "add-auth-feature"      # 来自 Phase A
  task_list: [TASK-001, ...]       # 来自 Phase A

config:
  skip_steps: []
  params:
    coverage_threshold: 80
    branch_prefix: "feature"
```

### 步骤执行

```yaml
B.1 - 分支管理:
  skill: branch-manager
  action: create
  skip_if:
    - already_on_feature_branch: true
  action:
    - 检查当前分支
    - 创建功能分支
  output:
    branch_name: "feature/mobile/TASK-001-add-auth"

B.2 - 测试验证:
  skill: test-verifier
  params:
    coverage_threshold: 80
  degrade_if:
    - no_test_files: true           # 降级模式，不阻塞
  action:
    - 检测变更文件类型
    - 运行对应测试
    - 检查覆盖率
  output:
    test_passed: true
    coverage: 87.5
    tests_run: 15

B.3 - 架构同步:
  skill: arch-update
  skip_if:
    - no_architecture_changes: true
  action:
    - 检测架构相关变更
    - 更新 ARCHITECTURE.md
  output:
    arch_updated: true
    files_modified: ["docs/ARCHITECTURE.md"]
```

### 输出

```yaml
success: true
steps_executed: [B.1, B.2, B.3]
steps_skipped: []
results:
  B.1:
    branch_name: "feature/mobile/TASK-001-add-auth"
  B.2:
    test_passed: true
    coverage: 87.5
  B.3:
    arch_updated: true

context_for_next:
  branch_name: "feature/mobile/TASK-001-add-auth"
  test_results:
    passed: true
    coverage: 87.5
  arch_sync_status: "updated"
```

---

## 跳过规则

| 条件 | 跳过步骤 | 检测方法 |
|------|---------|----------|
| 已在功能分支 | B.1 | 当前分支不是 main/develop |
| 无测试文件 | B.2 (降级) | 变更文件无对应 *_test.* |
| 无架构变更 | B.3 | 无 ARCHITECTURE.md 变更 |

### 跳过逻辑

```yaml
skip_evaluation:
  B.1:
    - check: git branch --show-current
      skip_if: not in [main, master, develop]
      reason: "已在功能分支"

  B.2:
    - check: test file mapping
      degrade_if: no corresponding test files
      action: 运行但不阻塞，输出警告

  B.3:
    - check: changed_files
      skip_if: no files match *ARCHITECTURE*.md
      reason: "无架构文档变更"
```

---

## 输出格式

```
╔══════════════════════════════════════════════════════════════╗
║              PHASE B - DEVELOPMENT                           ║
╚══════════════════════════════════════════════════════════════╝

📋 执行计划
───────────────────────────────────────────────────────────────
  B.1 branch-manager    → 创建分支
  B.2 test-verifier     → 测试验证
  B.3 arch-update       → 架构同步 (跳过 - 无架构变更)

🚀 执行中...
───────────────────────────────────────────────────────────────
  ✅ B.1 完成 → 分支: feature/mobile/TASK-001-add-auth
  ✅ B.2 完成 → 测试: 15/15 通过, 覆盖率: 87.5%
  ○  B.3 跳过 → 理由: 无架构文档变更

📤 上下文输出
───────────────────────────────────────────────────────────────
  branch: feature/mobile/TASK-001-add-auth
  tests: passed (87.5% coverage)
  ready_for: Phase C
```

---

## 使用示例

### 示例 1: 完整开发阶段

```yaml
输入:
  context:
    module: "mobile"
    changed_files: ["lib/auth.dart", "test/auth_test.dart"]

执行:
  B.1: 创建分支 → feature/mobile/TASK-001-add-auth
  B.2: 运行测试 → 15/15 通过
  B.3: 更新架构 → ARCHITECTURE.md 已更新

输出:
  context_for_next:
    branch_name: "feature/mobile/TASK-001-add-auth"
    test_passed: true
```

### 示例 2: 跳过分支创建

```yaml
输入:
  current_branch: "feature/add-auth"  # 已在功能分支

执行:
  B.1: 跳过 (已在功能分支)
  B.2: 运行测试
  B.3: 检查架构

输出:
  steps_skipped: [B.1]
  branch_name: "feature/add-auth"  # 使用现有分支
```

### 示例 3: 测试降级

```yaml
输入:
  changed_files: ["lib/new_feature.dart"]  # 无对应测试

执行:
  B.1: 创建分支
  B.2: 降级模式 (警告无测试)
  B.3: 检查架构

输出:
  B.2:
    mode: "degraded"
    warning: "lib/new_feature.dart 没有对应测试"
    suggestion: "使用 flutter-test-generator 生成测试"
```

---

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| 分支创建失败 | 分支已存在 | 切换到现有分支 |
| 测试失败 | 代码问题 | 停止执行，报告失败 |
| 架构更新失败 | 文档格式错误 | 输出警告，继续执行 |

### 测试失败处理

```yaml
on_test_failure:
  action: stop
  report:
    - 失败的测试列表
    - 错误信息
    - 修复建议
  next_step: "修复测试后重新运行 Phase B"
```

---

## 与其他 Phase 的关系

```
phase-a-planner
    │
    │ context:
    │   - spec_id
    │   - task_list
    ▼
phase-b-developer (本 Skill)
    │
    │ context_for_next:
    │   - branch_name
    │   - test_results
    │   - arch_sync_status
    ▼
phase-c-integrator
```

---

## 相关文档

- [branch-manager](../branch-manager/SKILL.md) - B.1 分支管理
- [test-verifier](../test-verifier/SKILL.md) - B.2 测试验证
- [arch-update](../arch-update/SKILL.md) - B.3 架构同步
- [phase-a-planner](../phase-a-planner/SKILL.md) - 上一阶段
- [phase-c-integrator](../phase-c-integrator/SKILL.md) - 下一阶段

---

**最后更新**: 2026-01-18
**Skill版本**: 1.1.0

---

## Git Worktree 集成

> **新增于 v1.1.0**

Phase B 支持使用 Git Worktrees 创建隔离的开发环境。

### Worktree 模式

```yaml
use_worktree: true  # 启用 worktree 模式

B.1 - 分支创建 (Worktree 模式):
  action:
    - 使用 branch-manager 的 worktree 创建
    - 工作目录: .git/worktrees/{task-name}/
  output:
    worktree_path: ".git/worktrees/TASK-001-user-auth"
    branch_name: "feature/backend/TASK-001-user-auth"
```

### Worktree 路径切换

```yaml
切换到 worktree:
  command: cd .git/worktrees/{task-name}/

返回主分支:
  command: cd ../..

清理 worktree:
  command: git worktree remove .git/worktrees/{task-name}/
```

### Worktree 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `use_worktree` | `false` | 是否启用 worktree 模式 |
| `worktree_base` | `.git/worktrees` | worktree 基础路径 |

---

## 两阶段评审机制

> **新增于 v1.1.0**

Phase B 扩展支持两阶段评审：**规范合规性** → **代码质量**。

### 评审流程

```yaml
B.Review - 两阶段评审:

  Phase 1 - 规范合规性检查:
    enabled: true
    blocking: true
    checks:
      - OpenSpec 格式验证
      - UPM 状态同步检查
      - 架构文档同步检查
    output:
      spec_compliance: pass/fail
      issues: [...]

  Phase 2 - 代码质量检查:
    enabled: true
    blocking: false  # 警告但不阻塞
    checks:
      - 测试覆盖率检查 (>= 85%)
      - 代码复杂度分析
      - 安全漏洞扫描
    output:
      code_quality_score: 0-100
      recommendations: [...]
```

### Phase 1: 规范合规性

| 检查项 | 说明 | 阻塞 |
|--------|------|------|
| OpenSpec 格式 | proposal.md/tasks.md 格式正确 | ✅ |
| UPM 状态 | 进度状态与实际一致 | ✅ |
| 架构文档 | 代码变更与文档同步 | ✅ |

**失败处理**: 关键问题必须修复后方可继续

### Phase 2: 代码质量

| 检查项 | 阈值 | 阻塞 |
|--------|------|------|
| 测试覆盖率 | >= 85% | ❌ (警告) |
| 代码复杂度 | <= 10 | ❌ (警告) |
| 安全扫描 | 无高危漏洞 | ❌ (警告) |

**失败处理**: 记录警告，生成改进建议

### 评审报告

```yaml
评审报告格式:
  summary:
    phase1_status: "pass"
    phase2_status: "warning"
    overall_score: 85

  phase1_issues:
    - severity: "critical"
      description: "UPM 状态未更新"
      fix_required: true

  phase2_recommendations:
    - type: "coverage"
      current: 82
      target: 85
      suggestion: "为 AuthManager 添加测试用例"
```

### 阻塞机制

```yaml
阻塞条件:
  - Phase 1 有 critical 级别问题
  - OpenSpec 格式验证失败

绕过选项:
  - 用户显式确认 "force_continue"
  - 标记为 "technical_debt" (技术债务)
```

### 评审配置

```yaml
review_config:
  enabled: true
  phase1:
    enabled: true
    blocking: true
    checks:
      openspec_format: true
      upm_sync: true
      arch_doc_sync: true
  phase2:
    enabled: true
    blocking: false
    checks:
      test_coverage:
        threshold: 85
      code_complexity:
        threshold: 10
      security_scan:
        level: "high"
```

---

## 两阶段评审与 Worktree 配合使用

```yaml
完整流程 (Worktree + 两阶段评审):

  B.1 - 创建 Worktree 分支
  ↓
  B.2 - 开发 + 测试验证
  ↓
  B.Review - Phase 1: 规范合规性
  ↓ (通过)
  B.Review - Phase 2: 代码质量
  ↓ (警告/通过)
  B.3 - 架构同步
```

---

## 相关文档 (更新)

- [branch-manager](../branch-manager/SKILL.md) - B.1 分支管理 + Worktree 支持
- [test-verifier](../test-verifier/SKILL.md) - B.2 测试验证
- [arch-update](../arch-update/SKILL.md) - B.3 架构同步
- [tdd-enforcer](../tdd-enforcer/SKILL.md) - TDD 强制执行
- [phase-a-planner](../phase-a-planner/SKILL.md) - 上一阶段
- [phase-c-integrator](../phase-c-integrator/SKILL.md) - 下一阶段
- [Aria Workflow Enhancement](../../../standards/openspec/changes/aria-workflow-enhancement/proposal.md) - 增强提案
