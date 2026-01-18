# 用户验收测试

> **版本**: 1.0.0
> **来源**: TASK-031
> **提案**: aria-workflow-enhancement

---

## 概述

本文档定义 `aria-workflow-enhancement` 的验收标准和测试用例。

---

## 验收标准

### 功能验收

| 标准 | 描述 | 验证方法 |
|------|------|----------|
| **FC-001** | tdd-enforcer skill 创建并测试通过 | 检查 SKILL.md 存在且格式正确 |
| **FC-002** | branch-manager 支持 worktree 模式 | 执行 worktree-create.sh 验证 |
| **FC-003** | phase-b-developer 集成两阶段评审 | 检查 validators/ 目录存在 |
| **FC-004** | CLAUDE.md 自动触发规则生效 | 测试关键词触发对应 Skill |
| **FC-005** | hooks/ 目录和 session-start.sh 实现 | 检查文件存在且可执行 |

### 质量验收

| 标准 | 描述 | 目标值 | 实际值 |
|------|------|--------|--------|
| **QC-001** | 新增代码测试覆盖率 | >= 85% | __ |
| **QC-002** | Skill 文档通过 OpenSpec Lint | 通过 | __ |
| **QC-003** | 回滚方案测试验证通过 | 4/4 场景 | __ |

### 兼容性验收

| 标准 | 描述 | 验证方法 |
|------|------|----------|
| **CC-001** | 现有 skills 目录结构保持不变 | 对比 Agent Skills 规范 |
| **CC-002** | 所有新功能可选启用 | 逐个测试禁用功能 |
| **CC-003** | 向后兼容性测试通过 | mobile + backend + standards |

---

## 验收测试用例

### 用例 1: TDD Enforcer 功能验证

```yaml
用例 ID: UC-001
名称: TDD Enforcer Skill 验证
前置条件: tdd-enforcer/SKILL.md 存在
步骤:
  1. 读取 SKILL.md 文件
  2. 验证包含必需章节
  3. 验证工作流程定义完整

预期结果:
  - ✅ SKILL.md 文件存在
  - ✅ 包含 RED-GREEN-REFACTOR 流程描述
  - ✅ 包含使用示例

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

### 用例 2: Git Worktrees 集成验证

```yaml
用例 ID: UC-002
名称: Git Worktrees 脚本验证
前置条件: Git >= 2.30
步骤:
  1. 执行 worktree-create.sh
  2. 验证 worktree 目录创建
  3. 执行 worktree-switch.sh
  4. 验证切换成功
  5. 执行 worktree-cleanup.sh
  6. 验证清理完成

预期结果:
  - ✅ 脚本可执行
  - ✅ worktree 正确创建
  - ✅ 切换正确
  - ✅ 清理无残留

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

### 用例 3: 自动触发规则验证

```yaml
用例 ID: UC-003
名称: 自动触发规则验证
前置条件: CLAUDE.md 和 trigger-rules.json 存在
步骤:
  1. 测试 "test" 关键词
  2. 验证触发 tdd-enforcer
  3. 测试 "branch" 关键词
  4. 验证触发 branch-manager
  5. 测试 "state" 关键词
  6. 验证触发 state-scanner

预期结果:
  - ✅ "test" 触发 tdd-enforcer (置信度 >= 0.8)
  - ✅ "branch" 触发 branch-manager (置信度 >= 0.8)
  - ✅ "state" 触发 state-scanner (置信度 >= 0.8)

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

### 用例 4: 两阶段评审机制验证

```yaml
用例 ID: UC-004
名称: 两阶段评审验证
前置条件: phase-b-developer/validators/ 存在
步骤:
  1. 检查 spec-compliance.md 存在
  2. 验证包含 Phase 1 检查规则
  3. 检查 code-quality.md 存在
  4. 验证包含 Phase 2 检查规则
  5. 验证阻塞机制配置存在

预期结果:
  - ✅ spec-compliance.md 存在
  - ✅ 包含 critical/high/medium 分级
  - ✅ code-quality.md 存在
  - ✅ 包含阈值配置
  - ✅ blocking-rules.json.md 存在

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

### 用例 5: Hooks 系统验证

```yaml
用例 ID: UC-005
名称: Hooks 系统验证
前置条件: aria/hooks/ 目录存在
步骤:
  1. 检查 hooks.json 配置
  2. 验证 session-start.sh 可执行
  3. 验证 run-hook.cmd 可执行 (Windows)
  4. 检查 README.md 存在

预期结果:
  - ✅ hooks.json 格式正确
  - ✅ session-start.sh 可执行
  - ✅ run-hook.cmd 可执行
  - ✅ README.md 包含使用说明

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

---

## 回滚方案验证

### 场景 1: TDD Enforcer 阻塞开发

```yaml
测试步骤:
  1. 模拟 TDD Enforcer 阻塞场景
  2. 执行回滚步骤: 重命名 SKILL.md
  3. 验证原有流程恢复

预期结果:
  - ✅ 重命名后不再触发 TDD 检查
  - ✅ 原有开发流程可继续

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

### 场景 2: Worktree 路径问题

```yaml
测试步骤:
  1. 创建一个 worktree
  2. 模拟路径问题
  3. 执行回滚: git worktree prune
  4. 验证列表正确

预期结果:
  - ✅ git worktree prune 清理成功
  - ✅ git worktree list 显示正确

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

### 场景 3: Hooks 执行失败

```yaml
测试步骤:
  1. 模拟 hook 执行失败
  2. 设置 enabled: false
  3. 验证会话可正常启动

预期结果:
  - ✅ 禁用后不影响会话启动
  - ✅ 其他功能正常工作

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

### 场景 4: 自动触发误判

```yaml
测试步骤:
  1. 触发错误 Skill
  2. 移除对应规则
  3. 验证不再触发

预期结果:
  - ✅ 编辑 CLAUDE.md 后规则更新
  - ✅ 不再触发错误的 Skill

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

---

## 文档验证

### 用例 6: 文档完整性

```yaml
用例 ID: UC-006
名称: 文档完整性验证
步骤:
  1. 检查所有 SKILL.md 存在
  2. 检查用户指南存在
  3. 检查迁移指南存在
  4. 检查兼容性说明存在

预期结果:
  - ✅ tdd-enforcer/SKILL.md
  - ✅ tdd-enforcer/workflow.md
  - ✅ tdd-enforcer/EXAMPLES.md
  - ✅ auto-trigger-guide.md
  - ✅ migration-guide.md
  - ✅ backward-compatibility.md

实际结果: ________________

状态: [ ] 通过 [ ] 失败
```

---

## 验收报告模板

```markdown
# 验收报告

**日期**: 2026-01-18
**版本**: v1.1
**验收人**: __________

## 功能验收

| 用例 | 状态 | 备注 |
|------|------|------|
| UC-001 | [ ] [ ] | TDD Enforcer 验证 |
| UC-002 | [ ] [ ] | Git Worktrees 验证 |
| UC-003 | [ ] [ ] | 自动触发验证 |
| UC-004 | [ ] [ ] | 两阶段评审验证 |
| UC-005 | [ ] [ ] | Hooks 系统验证 |
| UC-006 | [ ] [ ] | 文档完整性验证 |

## 质量验收

| 标准 | 目标 | 实际 | 状态 |
|------|------|------|------|
| QC-001 | >= 85% | __ % | [ ] [ ] |
| QC-002 | 通过 | __ | [ ] [ ] |
| QC-003 | 4/4 | __ | [ ] [ ] |

## 兼容性验收

| 标准 | 状态 | 备注 |
|------|------|------|
| CC-001 | [ ] [ ] | 目录结构兼容 |
| CC-002 | [ ] [ ] | 功能可选启用 |
| CC-003 | [ ] [ ] | 向后兼容测试 |

## 回滚验证

| 场景 | 状态 | 备注 |
|------|------|------|
| 场景 1 | [ ] [ ] | TDD Enforcer 回滚 |
| 场景 2 | [ ] [ ] | Worktree 回滚 |
| 场景 3 | [ ] [ ] | Hooks 回滚 |
| 场景 4 | [ ] [ ] | 自动触发回滚 |

## 总体结论

[ ] **通过** - 所有验收标准满足，可以发布
[ ] **有条件通过** - 部分标准未满足，需修复后发布
[ ] **不通过** - 关键标准未满足，需修复后重新验收

## 签名

验收人: __________
日期: __________
```

---

## 验收流程

```yaml
流程:
  1. 自查
     - 开发团队内部验收
     - 修复发现的问题

  2. 提交验收
     - 提交验收申请
     - 提供验收材料

  3. 验收测试
     - 执行验收测试用例
     - 记录测试结果

  4. 问题修复
     - 如有问题，修复后重新验收

  5. 验收通过
     - 签署验收报告
     - 发布到生产
```

---

**版本**: 1.0.0
**创建**: 2026-01-18
**相关**: [集成测试](../integration/test-plan.md)
