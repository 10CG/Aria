# agent-team-quality — Agent Team Description 精确化 + 协作契约

> **Level**: Minimal (Level 2 Spec)
> **Status**: Implemented
> **Created**: 2026-04-11
> **Parent Story**: [US-010](../../../docs/requirements/user-stories/US-010.md)
> **Target Version**: v1.12.0

## Why

Aria Agent Team 的 11 个 Agent 是十步循环中集体讨论、审计、开发的核心执行单元。当前存在三个结构性问题影响整体效能:

1. **路由模糊**: 6/11 Agent description 缺乏精确触发条件,导致 agent-router 路由准确率不足
2. **职责重叠**: code-reviewer 与 qa-engineer, tech-lead 与 backend-architect 边界不清
3. **协作断裂**: Agent 间无结构化 handoff,开发阶段各 Agent 独立工作,无上下文传递

实证: M3-slim B.2 阶段 3 个 Critical bug 未被开发 Agent 发现,全部推迟到 pre-merge 才暴露。

### PromptX 研究启发 (2026-04-11)

研究 [PromptX](https://github.com/Deepractice/PromptX) (3.6k Stars) 的角色管理机制后,Agent Team 讨论确定:

| PromptX 概念 | 借鉴决策 | 理由 |
|-------------|---------|------|
| Gherkin `.feature` 语法 | **不采用语法** | LLM 路由基于语义匹配,结构化语法增加 token 但不增路由信号 |
| 三段式结构化思维 | **采纳** → STCO 模式 | 借鉴 Given/When/Then 的结构化表达意图,但用自然语言 |
| Nuwa 角色创造者 | **Layer 2 采纳** | 项目级 Agent 生成,需人工确认,不在 US-010 范围 |
| RoleX 生命周期/记忆 | **不采纳** | 与 Fresh Subagent 无状态设计哲学冲突 (D3) |
| MCP 标准化接口 | **handoff contract 替代** | Aria 版轻量协议,不引入外部依赖 |

## What

### 1. STCO Description 模式 (11 个 Agent)

基于 code-reviewer (当前路由效果最佳) 的成功模式提炼,结合 PromptX 三段式思维:

```
Scope:    {领域名词, 描述能力空间}
Trigger:  "Use when:" + {3-5 用户视角场景}. "Use PROACTIVELY for:" + {自动触发场景}.
Contract: "Expects:" + {调用方需提供的输入}
Output:   "Produces:" + {具体产出物类型}
```

**示例 — tech-lead 重写:**

```yaml
description: |
  System architecture decisions, multi-service task decomposition, and engineering process design.
  Use when: planning complex features across services, resolving architecture trade-offs,
  decomposing epics into implementable tasks, optimizing CI/CD or review workflows.
  Expects: problem statement or feature scope; optionally current architecture context.
  Produces: architecture decision record, prioritized task breakdown, or process recommendation.
```

**示例 — context-manager 重写:**

```yaml
description: |
  Preserves and synthesizes context across multi-agent workflows and long-running sessions.
  Use when: coordinating 3+ agents on a shared goal, resuming work after session breaks,
  context window approaching limits and key decisions must be distilled.
  Expects: agent outputs to summarize, or session history to compress.
  Produces: structured context summary with decisions, open questions, and next actions.
```

### 2. 关键消歧对

| Agent A | Agent B | 消歧规则 |
|---------|---------|---------|
| code-reviewer | qa-engineer | reviewer: per-commit/per-PR 代码质量 + 规范合规. QA: 跨版本测试策略 + 缺陷分析 + 质量评估 |
| tech-lead | backend-architect | lead: 跨系统协调 + 任务分解 + 流程设计. architect: 单系统内 API/DB/性能设计 |
| context-manager | knowledge-manager | context: 多 Agent 工作流上下文保持. knowledge: 文档结构 + 知识体系维护 |

消歧通过 STCO 中的 Trigger + Output 自然实现 (不同场景 + 不同产出 = 路由区分)。

### 3. Handoff Contract

Agent 间传递的结构化上下文块,由 **caller (subagent-driver) 注入**,不在 description 中:

```yaml
handoff:
  task_id: "triage-engine-implementation"
  agent_from: "backend-architect"
  agent_source: "plugin"          # "plugin" | "project" — 预留 Layer 2 项目级 Agent
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

- STCO 的 Trigger 行成为路由的主要匹配信号
- 前端场景 fallback 置信度显著提升 (当前 0.70, 目标消除 general-purpose fallback)
- 增加项目技术栈元数据 (从 .aria/config.json 读取) 影响路由权重

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | 质量优先于数量 — 不新增 Agent | 4/4 共识: 路由噪声风险 > 覆盖度收益 |
| D2 | Layer 1/2 拆分 | 产品负责人 "立即有用" + "避免短板" 双重目标分层实现 |
| D3 | Agent 保持无状态 (Fresh Subagent) | 状态管理由 Skills 层承担; RoleX 进化模式与 subagent-driver 不兼容 |
| D4 | STCO 模式 (非 Gherkin 语法) | LLM 路由基于语义匹配, 自然语言+结构化意图 > 形式化语法 |
| D5 | Handoff contract 由 caller 注入 | description 用于路由, handoff 用于执行, 职责分离 |

## Implementation Strategy

**渐进式 (降低回归风险):**

1. **Pilot**: 选 `api-documenter` (低路由冲突) 重写为 STCO → AB benchmark 验证
2. **扩展**: pilot 通过后批量重写剩余 10 个 Agent
3. **Handoff**: 定义 contract schema + subagent-driver 集成文档

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 每次 Agent 调用路由准确率提升, 直接影响十步循环所有 Agent 参与环节 |
| **Positive** | 为 v2.0 Layer 1 调度提供更精确的 Agent 能力边界 |
| **Positive** | handoff contract 预留 agent_source 字段, Layer 2 项目级 Agent 无缝接入 |
| **Risk** | description 修改可能影响现有 AB benchmark baseline (pilot 先行缓解) |

## Estimation

| Task | 工作量 |
|------|--------|
| Pilot: api-documenter STCO 重写 + AB benchmark | 1-2h |
| 扩展: 剩余 10 Agent STCO 重写 | 2-3h |
| Handoff contract schema 定义 + 文档 | 1h |
| agent-router 路由增强 | 1-2h |
| **合计** | **5-8h** |

## Layer 2 预告 (不在本 Spec 范围)

Layer 2 (v1.13.0) 将基于 PromptX Nuwa 启发实现:
- 项目分析 → Agent 覆盖度评估 → 缺口报告
- 人工确认 → Agent 配置生成 (项目级 `.aria/agents/`)
- agent-router 动态感知项目级 Agent (需 `routing-hints` frontmatter 字段)
- 按技术栈 (Node.js/Python/Go/Flutter) 提供最小 Agent 模板集作为生成起点
- 流程: 缺口报告 → 人工确认 → 模板选择 → 生成 (禁止跳过确认, 规范先行)
