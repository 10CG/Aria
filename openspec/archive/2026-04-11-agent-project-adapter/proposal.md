# agent-project-adapter — 项目适配能力: 分析 + 覆盖度评估 + Agent 生成

> **Level**: Full (Level 3 Spec)
> **Status**: Implemented
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
  ├── 读取清单文件内容 (package.json deps, go.mod requires, pyproject.toml 等)
  ├── 识别工作模式 (monorepo 子包 / 微服务 / 前后端分离)
  ├── 识别工具链 (CI/CD / 测试框架 / ORM / 部署方式)
  └── 输出: project-profile.yaml
  │
  ▼
agent-gap-analyzer Skill
  ├── 读取 project-profile.yaml
  ├── 读取所有插件级 Agent 的 capabilities 字段 (机读, 非 LLM 解析)
  ├── 规则匹配: 项目需求场景 vs Agent capabilities
  ├── 识别缺口 (哪些场景无 Agent 覆盖)
  └── 输出: coverage-report.yaml (覆盖度 + 缺口 + 推荐)
  │
  ▼
[人工确认] ← 交互式确认, 展示缺口 + 推荐, 用户选择/修改/跳过
  │
  ▼
agent-creator Skill
  ├── 读取确认后的缺口选择
  ├── 匹配技术栈模板 (Node.js/Python/Go/Flutter/generic)
  ├── 用 few-shot exemplar (2-3 个现有 Agent 作为示例) 生成完整 Agent 定义
  ├── 输出预览 → 用户确认 --confirm / --dry-run
  └── 写入 .aria/agents/<name>.md
  │
  ▼
agent-router 运行时注入
  └── Skill 执行时读取 .aria/agents/ 目录, 将项目级 Agent
      注入当前路由决策上下文 (非 Plugin 级静态注册)
```

### 1. project-analyzer Skill

**扫描方式**: Glob 定位文件 + Read 读取内容 (非仅检测存在)

```yaml
输入: 项目根目录路径
输出: .aria/project-profile.yaml (schema_version: "1")

project_profile:
  name: "kairos"
  tech_stack:
    primary_language: "TypeScript"
    runtime: "Node.js 20"
    framework: "Express + Prisma"       # 从 package.json dependencies 读取
    frontend: null
    mobile: null
  packages:                              # monorepo 子包 (如有)
    - name: "api"
      path: "packages/api"
      tech_stack: { language: "TypeScript", framework: "Express" }
    - name: "worker"
      path: "packages/worker"
      tech_stack: { language: "TypeScript", framework: "BullMQ" }
  patterns:
    architecture: "monorepo"
    testing: "Jest + Supertest"
    ci_cd: "GitHub Actions"
    orm: "Prisma"
    deployment: "Docker + Nomad"
  detected_from:
    - { file: "package.json", fields: ["dependencies", "devDependencies"] }
    - { file: "tsconfig.json", fields: ["compilerOptions"] }
    - { file: "prisma/schema.prisma", fields: ["datasource", "model"] }
```

**降级处理**: 无法识别技术栈时 (纯 shell/Makefile 项目), 输出 `tech_stack.primary_language: "unknown"` 并提示用户手工补充, 不静默失败。

### 2. Agent capabilities 机读字段

**前置变更**: 在 11 个 Agent frontmatter 中增加 `capabilities` 字段:

```yaml
# agents/backend-architect.md
---
name: backend-architect
description: |
  RESTful API design, microservice boundaries, database schemas...
capabilities:                    # 新增: 机读能力标签
  - api-design
  - database-schema
  - microservice-architecture
  - performance-optimization
model: sonnet
color: green
---
```

agent-gap-analyzer 通过规则匹配 capabilities 标签 vs 项目需求场景, **不依赖 LLM 解析自然语言 description**。coverage_report 中的匹配度基于标签重合率 (确定性计算, 非 LLM 评分)。

**标签词汇表**: `aria/references/capabilities-taxonomy.yaml` 定义规范标签集 + 同义词映射 (如 `orm-migration` ↔ `database-migration`)。agent-gap-analyzer 在匹配前先做标签规范化,避免同义词导致假缺口。

### 3. agent-gap-analyzer Skill

```yaml
输入: project-profile.yaml + 所有 Agent capabilities + capabilities-taxonomy.yaml
输出: .aria/coverage-report.yaml (schema_version: "1")

coverage_report:
  covered:
    - scenario: "API design"
      matched_agent: "backend-architect"
      matched_capabilities: ["api-design"]
      match_rate: 1.0                    # 标签重合率, 非 LLM 评分
  gaps:
    - scenario: "Prisma schema migration"
      reason: "No agent has capability: orm-migration"
      suggested_agent:
        name: "database-specialist"
        capabilities: ["orm-migration", "prisma-schema", "query-optimization"]
        scope: "Prisma schema design, migration planning, query optimization"
  summary:
    total_scenarios: 8
    covered: 5
    gaps: 3
    coverage_rate: 62.5%
```

### 4. agent-creator Skill

**生成策略**:
- 使用 2-3 个现有 Agent 定义作为 few-shot exemplar (code-reviewer + backend-architect)
- 生成完整 Agent: STCO frontmatter + capabilities + body (含 Focus Areas / Approach / Output 章节)
- body 最低质量标准: 必须含 Focus Areas (3+ 项) + Approach (3+ 步) + Output (2+ 类产出)

**确认机制**:
- 默认: 交互式展示生成预览, 用户确认后写入
- `--dry-run`: 仅预览不写入
- `--confirm`: 跳过预览直接写入 (仅脚本/自动化场景)
- **同名覆盖保护**: 如果 `.aria/agents/` 下已存在同名文件, 或与插件级 Agent 同名, 发出显式警告并要求确认

### 5. 技术栈模板集

| 模板 | 检测条件 | 预设缺口 Agent |
|------|---------|---------------|
| Node.js/TypeScript | package.json + tsconfig.json | testing-specialist, database-specialist |
| Python/ML | requirements.txt / pyproject.toml + *.ipynb | data-engineer, ml-ops |
| Go | go.mod | infra-engineer, performance-specialist |
| Flutter | pubspec.yaml | platform-specialist (iOS/Android) |
| **generic** | 无法匹配上述模板 | STCO 骨架, 无预设 Agent |

### 6. agent-router 运行时注入 (非 Plugin 静态注册)

**关键设计变更** (R1 C1 修复):

Claude Code Plugin 的 Agent 是安装时静态注册的, `.aria/agents/` 不会被 Plugin 机制自动加载。因此:

- agent-router Skill 在执行路由决策时, **主动扫描 `.aria/agents/` 目录**
- 将发现的项目级 Agent 名称 + STCO description 注入当前路由上下文
- 这是 **Skill 层的运行时行为**, 不是 Plugin 层的静态注册
- 首次扫描结果缓存到 `.aria/cache/project-agents.json`, 后续路由使用缓存
- 缓存失效: `.aria/agents/` 目录 mtime 变化时重新扫描

**同名保护**: 项目级 Agent 与插件级同名时, 路由器发出警告 `⚠️ 项目级 Agent '<name>' 覆盖了插件级, 使用 --plugin-only 可回退`。

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | 项目级 `.aria/agents/`, 非全局 | 生命周期跟随项目,不污染 aria-plugin |
| D2 | 缺口报告→人工确认→生成 | 规范先行: 无确认的 Agent 不应自动生效 |
| D3 | 最小技术栈模板集 + generic fallback | 模板是起点不是终点 |
| D4 | agent-router 运行时注入 (非 Plugin 静态注册) | Claude Code Plugin 不支持动态 Agent 加载, 改由 Skill 层实现 |
| D5 | 生成的 Agent 遵循 STCO + capabilities 机读字段 | 确保路由质量 + 能力矩阵可确定性计算 |
| D6 | PromptX Nuwa 启发, 增加确认步骤 | Nuwa 直接生成; Aria 需确认 (规范先行) |
| D7 | capabilities 标签匹配 (非 LLM 解析 description) | 确定性 > 非确定性, 可审计 |
| D8 | agent-creator 用 few-shot exemplar 生成 body | 保证 body 含 Focus Areas / Approach / Output 章节 |
| D9 | 同名覆盖保护: 警告 + 显式确认 | 防止项目级 bug Agent 静默替换插件级 |
| D10 | capabilities-taxonomy.yaml 规范标签 + 同义词映射 | 确保标签匹配确定性, 避免同义词假缺口 |
| D11 | YAML 输出含 schema_version | v2.0 依赖这些产物时可检测格式变化 |

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 新项目接入从"手动探索"降为"分析+确认+生成" |
| **Positive** | 为 v2.0 Layer 1 提供项目感知能力 |
| **Risk** | 生成 Agent body 质量依赖 LLM, 需 few-shot + 人工审阅 |
| **Risk** | agent-router 目录扫描增加延迟 (首次扫描后缓存缓解) |

## Estimation

| Task | 工作量 |
|------|--------|
| 11 Agent 增加 capabilities 字段 (前置) | 1-2h |
| project-analyzer Skill | 3-4h |
| agent-gap-analyzer Skill | 4-6h |
| agent-creator Skill + 技术栈模板 | 3-4h |
| agent-router 运行时注入 + 缓存 + 同名保护 | 4-5h |
| **合计** | **15-21h** |
