# agent-project-adapter — 项目适配能力: 分析 + 覆盖度评估 + Agent 生成

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-04-11
> **Parent Story**: [US-011](../../../docs/requirements/user-stories/US-011.md)
> **Target Version**: v1.13.0

## Why

Aria 的 11 个 Agent 是通用角色定义,不携带项目特定的技术栈约束。当接入新项目 (如 Kairos TypeScript/Node.js) 时:

1. **Agent 不了解项目** — backend-architect 给的建议可能偏 Python/Go 范式
2. **缺口不可见** — 没有机制检测"哪些场景无 Agent 覆盖"
3. **适配靠人工** — 用户需自行判断需要什么 Agent,手写配置

PromptX 的 Nuwa (角色创造者) 验证了 "AI 分析需求 → 生成角色配置" 的可行性。Aria 需要同等能力,但须遵循规范先行原则 (人工确认,非直接生成)。

## What

### 核心流程

```
用户: "分析这个项目, 看看需要什么 Agent"
  │
  ▼
project-analyzer Skill
  ├── 扫描目录结构 (Glob)
  ├── 识别技术栈 (package.json / requirements.txt / go.mod / pubspec.yaml)
  ├── 检测工作模式 (monorepo / 微服务 / 前后端分离)
  ├── 识别工具链 (CI/CD / 测试框架 / ORM / 部署方式)
  └── 输出: 项目画像 (project-profile.yaml)
  │
  ▼
agent-gap-analyzer Skill
  ├── 读取项目画像
  ├── 加载 11 Agent 能力矩阵 (从 STCO description 提取)
  ├── 对比: 项目需求场景 vs Agent 覆盖范围
  ├── 识别缺口 (哪些场景无专业 Agent)
  └── 输出: 覆盖度报告 + 缺口清单 + 推荐 Agent 定义
  │
  ▼
[人工确认] ← 必须步骤, 不可跳过
  │
  ▼
agent-creator Skill
  ├── 读取确认后的缺口清单
  ├── 匹配技术栈模板 (Node.js / Python / Go / Flutter)
  ├── 生成 STCO 格式的 Agent 定义
  └── 写入 .aria/agents/<name>.md
  │
  ▼
agent-router 自动发现
  └── 路由时优先检索 .aria/agents/ (项目级 > 插件级)
```

### 1. project-analyzer Skill

```yaml
输入: 项目根目录路径
输出: .aria/project-profile.yaml

project_profile:
  name: "kairos"
  tech_stack:
    primary_language: "TypeScript"
    runtime: "Node.js 20"
    framework: "Express + Prisma"
    frontend: null
    mobile: null
  patterns:
    architecture: "monolith"
    testing: "Jest + Supertest"
    ci_cd: "GitHub Actions"
    orm: "Prisma"
    deployment: "Docker + Nomad"
  work_modes:
    - "API development"
    - "LLM pipeline integration"
    - "Database schema evolution"
  detected_from:
    - "package.json"
    - "tsconfig.json"
    - "prisma/schema.prisma"
    - ".github/workflows/"
```

### 2. agent-gap-analyzer Skill

```yaml
输入: project-profile.yaml + 11 Agent STCO descriptions
输出: 覆盖度报告

coverage_report:
  covered:
    - scenario: "API design"
      agent: "backend-architect"
      confidence: 0.95
    - scenario: "Code review"
      agent: "code-reviewer"
      confidence: 0.90
  gaps:
    - scenario: "Prisma schema migration"
      reason: "No agent has ORM/migration expertise"
      suggested_agent:
        name: "database-specialist"
        scope: "Prisma schema design, migration planning, query optimization"
    - scenario: "Jest test strategy"
      reason: "qa-engineer is generic, lacks Jest-specific patterns"
      suggested_agent:
        name: "testing-specialist"
        scope: "Jest configuration, mock strategies, E2E with Supertest"
  summary:
    total_scenarios: 8
    covered: 5
    gaps: 3
    coverage_rate: 62.5%
```

### 3. agent-creator Skill

基于确认后的缺口清单 + 技术栈模板生成 Agent 定义:

```yaml
# 生成的 .aria/agents/database-specialist.md

---
name: database-specialist
description: |
  Prisma schema design, migration planning, query optimization, and data modeling for Node.js/TypeScript projects.
  Use when: designing database schemas, planning migrations, optimizing Prisma queries, reviewing data models. NOT for API endpoint design (use backend-architect).
  Expects: schema requirements or migration context; optionally existing Prisma schema.
  Produces: Prisma schema definition, migration plan, query optimization recommendations.
model: sonnet
color: green
---

You are a database specialist for Prisma-based Node.js/TypeScript projects...
```

### 4. 技术栈模板集

最小模板,每个仅预设 description pattern + 常见 Agent 缺口:

| 技术栈 | 检测条件 | 常见缺口 Agent |
|--------|---------|---------------|
| Node.js/TypeScript | package.json + tsconfig.json | testing-specialist, database-specialist |
| Python/ML | requirements.txt + *.ipynb | data-engineer, ml-ops |
| Go | go.mod | infra-engineer, performance-specialist |
| Flutter | pubspec.yaml | platform-specialist (iOS/Android) |

模板不是预设答案,是 agent-creator 的起点参考。

### 5. agent-router 动态发现

agent-router 增强: 路由时除扫描 `aria/agents/` (插件级) 外,优先扫描 `.aria/agents/` (项目级)。

优先级: 项目级 Agent > 插件级 Agent (同名时项目级覆盖)。

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | 项目级 `.aria/agents/`, 非全局 | 生命周期跟随项目,不污染 aria-plugin |
| D2 | 缺口报告→人工确认→生成 | 规范先行: 无确认的 Agent 不应自动生效 |
| D3 | 最小技术栈模板集 | 模板是起点不是终点 |
| D4 | agent-router 动态感知项目级 Agent | 生成的 Agent 需被路由发现 |
| D5 | 生成的 Agent 遵循 STCO 模式 | 与 US-010 一致,确保路由质量 |
| D6 | PromptX Nuwa 启发,非照搬 | Nuwa 直接生成; Aria 需确认步骤 (规范先行) |

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 新项目接入时间从"手动探索"降为"分析+确认+生成" |
| **Positive** | 为 v2.0 Layer 1 提供项目感知能力 (调度时知道项目有哪些专属 Agent) |
| **Risk** | 生成的 Agent 质量取决于 LLM 能力,需人工审阅把关 |
| **Risk** | agent-router 动态扫描增加路由延迟 (需控制目录扫描开销) |

## Estimation

| Task | 工作量 |
|------|--------|
| project-analyzer Skill | 3-4h |
| agent-gap-analyzer Skill | 3-4h |
| agent-creator Skill + 技术栈模板 | 2-3h |
| agent-router 动态发现增强 | 2-3h |
| **合计** | **10-14h** |

## Dependencies

- US-010 (done): STCO description + handoff contract 是生成质量的基础
- agent-router: 需支持项目级 Agent 目录扫描
- .aria/ 命名空间: 项目级配置已建立 (config.json, issues/, etc.)
