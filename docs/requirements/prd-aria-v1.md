# Aria - 产品需求文档 (PRD)

> **Version**: 1.0.0
> **Status**: Active
> **Created**: 2026-01-18
> **Owner**: 10CG Lab

---

## 文档目的

Aria 是一个 AI-DDD (AI-Assisted Domain-Driven Design) 方法论研究项目，探索如何让 AI Agent 深度参与软件工程全流程。本 PRD 定义 Aria v1.x 系列的产品范围和成功标准。

---

## 产品定位

### 核心定位

让 AI 成为理解项目意图的协作者，而非被动工具。通过标准化流程实现可重现的 AI 协作模式。

### 目标用户

| 用户角色 | 描述 | 核心需求 |
|---------|------|---------|
| AI 协作研究者 | 探索 AI 辅助开发方法论的研究人员 | 可重现的协作流程、效果量化 |
| 开发者 | 使用 Claude Code 的软件工程师 | 高效工作流、减少上下文传递成本 |
| AI Agent | Claude Code 中的 AI 助手 | 清晰指令、完整上下文、结构化交互 |

### 核心价值主张

- **可重现性**: 不同项目、不同 AI 都能获得一致的协作结果
- **效率提升**: 最小化上下文传递成本，AI 快速理解项目状态
- **决策可追溯**: 每个"为什么"都有据可查 (OpenSpec + 归档体系)

### 成功标准

- [x] 十步循环工作流完整定义并通过实际项目验证
- [x] OpenSpec 需求规范格式化并支持 3 级别 (Skip/Minimal/Full)
- [x] 27 个 Skills + 11 个 Agents 覆盖完整开发流程
- [x] 基准测试体系量化评估 Skill 效果 (100% pass rate)
- [ ] 跨项目验证方法论适用性 (v1.1.0 目标)
- [ ] 多 AI 平台兼容性 (v1.2.0 目标)

---

## 功能范围

### Must-have (v1.0 已交付)

#### 1. 十步循环工作流

```yaml
十步循环:
  A. 规划:
    ✅ A.0 状态扫描 (state-scanner)
    ✅ A.1 规范创建 (spec-drafter)
    ✅ A.2 任务规划 (task-planner)
    ✅ A.3 Agent 分配 (agent-router)
  B. 开发:
    ✅ B.1 分支创建 (branch-manager)
    ✅ B.2 执行验证 (subagent-driver + tdd-enforcer)
  C. 集成:
    ✅ C.1 提交 (commit-msg-generator + strategic-commit-orchestrator)
    ✅ C.2 合并 (branch-finisher)
  D. 收尾:
    ✅ D.1 进度更新 (progress-updater)
    ✅ D.2 归档 (openspec-archive)
```

#### 2. OpenSpec 需求规范

```yaml
OpenSpec:
  ✅ Level 1 (Skip): 简单修复，无需规范
  ✅ Level 2 (Minimal): proposal.md
  ✅ Level 3 (Full): proposal.md + tasks.md + detailed-tasks.yaml
  ✅ 归档体系: changes/ → archive/
```

#### 3. 质量保障机制

```yaml
质量保障:
  ✅ TDD 强制执行 (tdd-enforcer v2.0)
  ✅ 两阶段代码审查 (requesting-code-review)
  ✅ 强制执行机制 (branch-manager + subagent-driver + branch-finisher)
```

#### 4. 基准测试体系

```yaml
基准测试:
  ✅ 27 Skill 评估套件
  ✅ 自动化执行器 (runner)
  ✅ 效果量化 (with vs without Skill)
```

### Nice-to-have (v1.1.0+ 规划)

```yaml
可选功能:
  ⚠️ 增强工作流自动化: 减少手动步骤，提升端到端自动化程度
  ⚠️ 多 AI 平台支持: 扩展到 Claude 以外的 AI Agent
  ⚠️ 需求追踪可视化: 提供 PRD → Story → OpenSpec 的可视化链路
```

### Out of Scope

| 功能 | 排除原因 | 未来计划 |
|------|---------|---------|
| 代码生成模板 | Aria 是方法论，非框架 | 不计划 |
| 特定编程语言绑定 | 技术栈无关 | 不计划 |
| CI/CD 配置 | 超出方法论边界 | 不计划 |
| 企业级多团队支持 | 当前聚焦个人/小团队 | v2.0.0 |

---

## 非功能需求

| 类型 | 要求 | 优先级 |
|------|------|--------|
| 可理解性 | 新人 30 分钟内理解核心概念 | HIGH |
| 可操作性 | 每个步骤都有明确输入输出 | HIGH |
| 可扩展性 | 支持新增 Skill 和 Agent | HIGH |
| 兼容性 | 与 Claude Code 无缝集成 | HIGH |
| 向后兼容 | 新版本不破坏现有工作流 | HIGH |

---

## 关联文档

### System Architecture

- `docs/architecture/system-architecture.md` - v1.5.0

### User Stories

| Story ID | 标题 | 优先级 | 状态 |
|----------|------|--------|------|
| US-001 | 增强工作流自动化 | HIGH | pending |
| US-002 | 跨项目方法论验证 | MEDIUM | pending |
| US-003 | 多 AI 平台兼容性 | LOW | pending |

### OpenSpec Changes

- `openspec/archive/` - 29 个已完成变更

---

## 版本历史

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-03-16 | 初始版本，基于已交付功能整理 | 10CG Lab |
