# agent-team-quality — Agent Team Description 精确化 + 协作契约

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-04-11
> **Parent Story**: [US-010](../../../docs/requirements/user-stories/US-010.md)
> **Target Version**: v1.12.0

## Why

Aria Agent Team 的 11 个 Agent 是十步循环中集体讨论、审计、开发的核心执行单元。当前存在三个结构性问题影响整体效能:

1. **路由模糊**: 6/11 Agent description 缺乏精确触发条件,导致 agent-router 路由准确率不足
2. **职责重叠**: code-reviewer 与 qa-engineer, tech-lead 与 backend-architect 边界不清
3. **协作断裂**: Agent 间无结构化 handoff,开发阶段各 Agent 独立工作,无上下文传递

实证: M3-slim B.2 阶段 3 个 Critical bug 未被开发 Agent 发现,全部推迟到 pre-merge 才暴露。

## What

### 1. Description 精确化 (11 个 Agent)

每个 Agent description 遵循统一模式:

```
{职责一句话}

专长: {具体擅长的任务类型, 3-5 项}
产出物: {Agent 典型输出, 如 "架构决策文档", "测试策略报告"}
触发条件: "Use when {具体场景}. Use PROACTIVELY for {自动触发场景}."
消歧: "Use {this} for {X}; use {neighbor} for {Y}."
不做: {明确排除的职责}
```

### 2. 关键消歧对

| Agent A | Agent B | 消歧规则 |
|---------|---------|---------|
| code-reviewer | qa-engineer | reviewer: per-commit/per-PR 代码质量. QA: 跨版本测试策略 + 缺陷分析 |
| tech-lead | backend-architect | lead: 跨团队协调 + 任务分解. architect: 单系统内 API/DB/性能设计 |
| context-manager | knowledge-manager | context: 多 Agent 工作流上下文保持. knowledge: 文档结构 + 知识体系维护 |

### 3. Handoff Contract

Agent 间传递的结构化上下文块:

```yaml
handoff:
  task_id: "triage-engine-implementation"
  agent_from: "backend-architect"
  decisions_made:
    - "triage.sh 使用 bash + python3 heredoc 模式"
    - "配置走 orchestrator.dispatch_policy 独立节点"
  artifacts_created:
    - "triage.sh"
    - "test-fixtures/"
  open_questions:
    - "飞书消息截断策略: 10 条 or 按字数?"
  constraints:
    - "不新增 heartbeat.sh 必需 env 变量"
```

### 4. agent-router 增强

- 路由规则中注入消歧条件
- 前端场景 fallback 置信度从 0.70 提升至 0.85+
- 增加项目技术栈元数据 (从 .aria/config.json 读取) 影响路由权重

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 每次 Agent 调用路由准确率提升, 直接影响十步循环所有 Agent 参与环节 |
| **Positive** | 为 v2.0 Layer 1 调度提供更精确的 Agent 能力边界 |
| **Risk** | description 修改可能影响现有 AB benchmark baseline (需重跑) |

## Estimation

| Task | 工作量 |
|------|--------|
| 11 个 Agent description 修订 | 2-3h |
| agent-router 路由规则增强 | 1-2h |
| Handoff contract 定义 + 文档 | 1h |
| AB benchmark 验证 (如有 Skill 触发变更) | 按需 |
