# 两阶段代码审查实现 (Superpowers Two-Phase Review)

> **Level**: Full (Level 3 Spec)
> **Status**: Approved
> **Created**: 2026-02-06
> **Approved**: 2026-02-06
> **Story ID**: US-Superpowers-001
> **Milestone**: v1.4.0

---

## Why

### 背景分析

根据 [Aria vs Superpowers 对比分析](docs/analysis/aria-vs-superpowers-comparison.md)，Superpowers 在代码审查方面有以下优势：

1. **两阶段分离** - Phase 1 验证规范合规性，Phase 2 检查代码质量
2. **阻塞优先** - Phase 1 的 FAIL 必须阻塞，Phase 2 的 FAIL 可配置
3. **计划对照** - 明确对照 `{PLAN_OR_REQUIREMENTS}` 检查实现

Aria 现有的代码审查机制 (`subagent-driver/internal/INTER_TASK_REVIEW.md`) 是**综合审查**，一次性检查所有维度，缺少两阶段分离。

### 问题陈述

```
当前问题:
  1. subagent-driver 的代码审查是综合性的，无两阶段分离
  2. feature-dev:code-reviewer 缺少计划对照功能
  3. 无法强制要求"规范合规后才能进行质量检查"

期望状态:
  1. Phase 1 (规范检查) 必须通过后才进行 Phase 2 (质量检查)
  2. 支持与 detailed-tasks.yaml 或 OpenSpec proposal.md 对照
  3. 复用 Superpowers 的成功模式，适配 Aria 架构
```

---

## What

### 核心变更

新增 `aria:code-reviewer` Agent 和 `requesting-code-review` Skill，实现 Superpowers 风格的两阶段代码审查。

### 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                    两阶段代码审查架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  requesting-code-review Skill (用户入口)                         │
│       │                                                         │
│       │ 1. 获取 git SHA                                          │
│       │ 2. 填充 code-reviewer.md 模板                            │
│       │ 3. 使用 Task 工具派发 aria:code-reviewer Agent            │
│       │                                                         │
│       ▼                                                         │
│  aria:code-reviewer Agent (审查执行)                             │
│       │                                                         │
│       │ Phase 1: 规范合规性检查                                   │
│       │  ├─ 对照 detailed-tasks.yaml 检查                        │
│       │  ├─ 验证文件路径是否正确                                  │
│       │  ├─ 验证实现是否完整                                      │
│       │  └─ 判定: PASS → 继续, FAIL → 阻塞                        │
│       │       │                                                 │
│       │       ▼ (仅 Phase 1 PASS 后)                             │
│       │  Phase 2: 代码质量检查                                    │
│       │  ├─ 代码风格检查                                         │
│       │  ├─ 测试覆盖率检查                                       │
│       │  ├─ 安全漏洞检查                                         │
│       │  └─ 判定: PASS/WARN/FAIL                                 │
│       │                                                         │
│       ▼                                                         │
│  格式化审查报告                                                  │
│       │                                                         │
│       ▼                                                         │
│  用户处理反馈 → 继续下一任务 或 返回修复                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 与 Superpowers 的对比

| 维度 | Superpowers | Aria 实现 |
|------|-------------|-----------|
| Agent 名称 | `superpowers:code-reviewer` | `aria:code-reviewer` |
| Skill 名称 | `requesting-code-review` | `requesting-code-review` |
| Phase 1 检查 | 计划对照 | 计划对照 + OpenSpec 支持 |
| Phase 2 检查 | 代码质量 | 代码质量 + Aria 最佳实践 |
| 输出格式 | Critical/Important/Minor | Critical/Important/Minor |
| 语言 | 英语 | 中英双语 |

### Key Deliverables

| ID | 交付物 | 路径 |
|----|--------|------|
| D1 | `aria:code-reviewer` Agent | `aria/agents/code-reviewer.md` |
| D2 | `requesting-code-review` Skill | `aria/skills/requesting-code-review/SKILL.md` |
| D3 | Agent 模板文件 | `aria/skills/requesting-code-review/code-reviewer.md` |
| D4 | `subagent-driver` 集成更新 | `aria/skills/subagent-driver/SKILL.md` |
| D5 | 使用文档和示例 | `aria/skills/requesting-code-review/examples/` |

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 提升代码质量保证，规范与质量分离检查，借鉴 Superpowers 成熟模式 |
| **Risk** | 可能增加审查时间 | 缓解: Phase 1 快速失败，避免不必要的 Phase 2 |
| **Compatibility** | 向后兼容 | 现有审查机制保留，新功能为可选 |

---

## 详细设计

### D1: aria:code-reviewer Agent

**文件**: `aria/agents/code-reviewer.md`

```yaml
---
name: code-reviewer
description: |
  两阶段代码审查 Agent: Phase 1 验证规范合规性, Phase 2 检查代码质量。
  参考 obra/superpowers requesting-code-review 实现。

model: inherit
color: blue
tools: ["Read", "Grep", "Glob", "Bash"]
---

# Code Review Agent (Two-Phase)

## Phase 1: 规范合规性检查 (Specification Compliance)

### 输入参数
- `{WHAT_WAS_IMPLEMENTED}` - 刚刚实现的内容
- `{PLAN_OR_REQUIREMENTS}` - 应该做什么 (detailed-tasks.yaml 或 OpenSpec)
- `{BASE_SHA}` - 起始提交
- `{HEAD_SHA}` - 结束提交

### 检查项
1. 文件路径是否与计划一致
2. 实现是否覆盖所有计划功能
3. 是否有超出计划的范围变更
4. OpenSpec 字段是否同步更新

### 判定标准
- **PASS**: 所有关键检查点通过 → 继续 Phase 2
- **FAIL**: 有关键缺失 → 阻塞，返回修复

## Phase 2: 代码质量检查 (Code Quality)

### 检查项
1. 代码风格 (CLAUDE.md 合规)
2. 测试覆盖率
3. 安全漏洞
4. 架构设计

### 判定标准
- **PASS**: 无问题或仅有 Minor 问题
- **PASS_WITH_WARNINGS**: 有 Important 问题
- **FAIL**: 有 Critical 问题

## 输出格式

### Strengths
[哪些做得好？具体说明。]

### Issues
#### Critical (Must Fix)
[Bug、安全问题、数据丢失风险、功能损坏]

#### Important (Should Fix)
[架构问题、缺失功能、错误处理不当、测试缺口]

#### Minor (Nice to Have)
[代码风格、优化机会、文档改进]

### Assessment
**Ready to proceed?** [Yes/No/With fixes]
**Reasoning:** [技术评估 1-2 句]
```

### D2: requesting-code-review Skill

**文件**: `aria/skills/requesting-code-review/SKILL.md`

```markdown
---
name: requesting-code-review
description: |
  使用代码审查验证工作是否符合要求 - 派发 aria:code-reviewer Agent
  对照计划或需求审查实现，在继续之前捕获问题。

  核心原则: 早审查，常审查。
user-invocable: true
---

# Requesting Code Review

## 何时请求审查

**强制**:
- subagent-driven development 中每个任务完成后
- 完成主要功能后
- 合并到主分支前

**可选但有价值**:
- 遇到困难时 (新视角)
- 重构前 (基线检查)
- 修复复杂 bug 后

## 如何请求

### 1. 获取 git SHA
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

### 2. 派发 code-reviewer Agent
使用 Task 工具和 aria:code-reviewer 类型，填充 `code-reviewer.md` 模板

### 3. 处理反馈
- 立即修复 Critical 问题
- 继续前修复 Important 问题
- 记录 Minor 问题稍后处理
- 如果审查者错误，用技术理由反驳

## 集成

### subagent-driven-development
- **每个任务后**审查
- 在问题复合前捕获
- 移动到下一任务前修复

### 执行计划
- 每批 (3 个任务) 后审查
- 获得反馈、应用、继续
```

### D3: Agent 模板文件

**文件**: `aria/skills/requesting-code-review/code-reviewer.md`

```markdown
# Code Review Agent

You are reviewing code changes for production readiness.

**Your task:**
1. Review {WHAT_WAS_IMPLEMENTED}
2. Compare against {PLAN_OR_REQUIREMENTS}
3. Execute two-phase review: Specification Compliance → Code Quality
4. Categorize issues by severity
5. Assess production readiness

## What Was Implemented
{DESCRIPTION}

## Requirements/Plan
{PLAN_REFERENCE}

## Git Range to Review
**Base:** {BASE_SHA}
**Head:** {HEAD_SHA}

```bash
git diff --stat {BASE_SHA}..{HEAD_SHA}
git diff {BASE_SHA}..{HEAD_SHA}
```

## Phase 1: Specification Compliance

**Critical Check:**
- [ ] File paths match plan
- [ ] All planned features implemented
- [ ] No scope creep
- [ ] OpenSpec fields updated if applicable

**Phase 1 Verdict:** PASS / FAIL
- If FAIL, list blocking issues and stop.
- If PASS, proceed to Phase 2.

## Phase 2: Code Quality

**Code Quality:**
- Clean separation of concerns?
- Proper error handling?
- Type safety (if applicable)?
- DRY principle followed?
- Edge cases handled?

**Architecture:**
- Sound design decisions?
- Scalability considerations?
- Performance implications?
- Security concerns?

**Testing:**
- Tests actually test logic (not mocks)?
- Edge cases covered?
- Integration tests where needed?
- All tests passing?

**Aria Best Practices:**
- CLAUDE.md compliance?
- Documentation complete?
- No obvious bugs?

## Output Format

### Phase 1 Result
**Verdict:** [PASS/FAIL]

If FAIL:
#### Blocking Issues
1. **[Issue description]**
   - File:line reference
   - What's missing
   - Why it matters
   - How to fix

### Phase 2 Result (only if Phase 1 PASS)

#### Strengths
[What's well done? Be specific.]

#### Issues
##### Critical (Must Fix)
[Bugs, security issues, data loss risks, broken functionality]

##### Important (Should Fix)
[Architecture problems, missing features, poor error handling, test gaps]

##### Minor (Nice to Have)
[Code style, optimization opportunities, documentation improvements]

**For each issue:**
- File:line reference
- What's wrong
- Why it matters
- How to fix (if not obvious)

#### Recommendations
[Improvements for code quality, architecture, or process]

#### Assessment
**Ready to proceed?** [Yes/No/With fixes]
**Reasoning:** [Technical assessment in 1-2 sentences]
```

---

## Tasks

### Phase 1: 核心 Agent 和 Skill 创建 (Week 1)

- [ ] **TASK-001**: 创建 `aria/agents/code-reviewer.md` Agent
  - 定义两阶段审查流程
  - 实现 Phase 1 规范合规性检查逻辑
  - 实现 Phase 2 代码质量检查逻辑
  - 定义输出格式

- [ ] **TASK-002**: 创建 `requesting-code-review` Skill
  - 编写 SKILL.md
  - 定义使用场景和触发条件
  - 编写使用示例

- [ ] **TASK-003**: 创建 Agent 模板文件
  - 编写 `code-reviewer.md` 模板
  - 定义占位符变量
  - 编写输出格式示例

### Phase 2: 集成与文档 (Week 2)

- [ ] **TASK-004**: 更新 `subagent-driver` Skill
  - 添加两阶段审查调用选项
  - 更新工作流文档
  - 保持向后兼容

- [ ] **TASK-005**: 编写使用文档和示例
  - 创建 examples/ 目录
  - 编写完整示例对话
  - 编写最佳实践指南

- [ ] **TASK-006**: 集成测试
  - 端到端测试两阶段审查
  - 验证与 subagent-driver 集成
  - 验证独立调用模式

### Phase 3: 验证与发布 (Week 2)

- [ ] **TASK-007**: 文档完善
  - 更新 CHANGELOG.md
  - 更新 README.md
  - 更新系统架构文档

- [ ] **TASK-008**: 发布准备
  - 版本号更新 (v1.4.0)
  - 插件清单更新
  - 发布说明编写

---

## Success Criteria

- [ ] **SC-001**: `aria:code-reviewer` Agent 可以独立执行两阶段审查
- [ ] **SC-002**: Phase 1 FAIL 时正确阻塞，不进入 Phase 2
- [ ] **SC-003**: 输出格式与 Superpowers 兼容，支持 Critical/Important/Minor 分类
- [ ] **SC-004**: 可以通过 `requesting-code-review` Skill 或直接调用 Agent
- [ ] **SC-005**: 与 `subagent-driver` 集成后保持向后兼容
- [ ] **SC-006**: 中英双语支持

---

## References

| 类型 | 链接 |
|------|------|
| 对比分析 | `docs/analysis/aria-vs-superpowers-comparison.md` |
| Superpowers Skill | https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md |
| Superpowers Agent | https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/code-reviewer.md |
| 现有审查机制 | `aria/skills/subagent-driver/internal/INTER_TASK_REVIEW.md` |
| feature-dev 示例 | https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/agent-development/examples/complete-agent-examples.md |

---

## Open Questions

1. **Q1**: 是否需要置信度评分 (类似 feature-dev code-review plugin)?
   - **倾向**: 否，Superpowers 不使用置信度评分

2. **Q2**: Phase 1 FAIL 后是否自动中断?
   - **倾向**: 是，阻塞继续，但允许用户 override

3. **Q3**: 是否支持 CLAUDE.md 合规性检查?
   - **倾向**: 是，在 Phase 2 中检查

---

## Appendix: 实施依赖

### 已完成组件

| 组件 | 状态 | 版本 |
|------|------|------|
| TDD Enforcer | ✅ 已完成 | v2.0.0 |
| Brainstorm Skill | ✅ 已完成 | v2.0.0 |
| subagent-driver | ✅ 已完成 | v1.0.0 |

### 需要创建

| 组件 | 状态 | 路径 |
|------|------|------|
| aria:code-reviewer Agent | 🔄 本提案 | `aria/agents/code-reviewer.md` |
| requesting-code-review Skill | 🔄 本提案 | `aria/skills/requesting-code-review/` |

---

**文档维护**: Aria 项目组
**更新日期**: 2026-02-06
**状态**: Approved - 已通过评审，准备实施
