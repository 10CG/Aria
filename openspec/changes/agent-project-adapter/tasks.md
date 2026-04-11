# agent-project-adapter — Task Plan

> **Scope**: US-011 (v1.13.0)
> **Parent Spec**: [proposal.md](./proposal.md)
> **Audit**: 3 轮 Agent Team 收敛 (2026-04-11)
> **Estimate**: ~15-21h

## Tasks

### Task 0: 前置 — 11 Agent 增加 capabilities 字段 [1-2h]

为现有 11 个 Agent frontmatter 添加 `capabilities` 机读标签列表。

**实现**:
- 每个 Agent 根据其 STCO Scope + Trigger 提取 3-8 个能力标签
- 标签用 kebab-case (如 `api-design`, `database-schema`)
- 同时创建 `aria/references/capabilities-taxonomy.yaml` 种子词汇表

**capabilities-taxonomy.yaml 结构**:
```yaml
version: "1"
tags:
  api-design:
    synonyms: ["rest-api", "endpoint-design"]
  database-schema:
    synonyms: ["db-design", "data-modeling", "erd"]
  orm-migration:
    synonyms: ["database-migration", "schema-migration"]
  # ... 完整列表随 Agent 定义生成
```

**验收**: 11 个 Agent 均有 capabilities 字段 + taxonomy.yaml 存在

---

### Task 1: project-analyzer Skill [3-4h]

**新建**: `aria/skills/project-analyzer/SKILL.md`

**核心逻辑**:
- Glob 定位清单文件 (package.json, go.mod, pyproject.toml, pubspec.yaml, Makefile 等)
- Read 读取内容 (dependencies, devDependencies, requires 等)
- 识别工作模式 (monorepo 子包检测: lerna.json, pnpm-workspace.yaml, packages/)
- 识别工具链 (CI: .github/workflows/, .gitlab-ci.yml; 测试: jest.config, pytest.ini; ORM: prisma/, alembic/)
- 输出: `.aria/project-profile.yaml` (schema_version: "1")

**降级**: 无法识别技术栈时输出 `primary_language: "unknown"` + 提示手工补充

**验收**: 
- 对 Aria 项目自身运行 → 输出合理画像
- 对无清单文件的目录运行 → 输出 unknown + 提示

---

### Task 2: agent-gap-analyzer Skill [4-6h]

**新建**: `aria/skills/agent-gap-analyzer/SKILL.md`

**核心逻辑**:
- 读取 `.aria/project-profile.yaml`
- 读取所有 Agent capabilities (插件级 + 项目级)
- 加载 `capabilities-taxonomy.yaml` 做标签规范化 (同义词合并)
- 从 project-profile 的 tech_stack + patterns 推导需求场景列表
- 场景推导规则: 技术栈 → 预定义场景映射 (如 `orm: "Prisma"` → 需求 `orm-migration` + `query-optimization`)
- 规则匹配: 需求标签 vs Agent capabilities → 标签重合率
- 输出: `.aria/coverage-report.yaml` (schema_version: "1")

**实现注意**:
- 场景列表来自规则映射 (确定性), 非 LLM 每次推断
- match_rate = 命中标签数 / 需求标签数 (如 3 个需求标签命中 2 个 = 0.67)
- covered 阈值: match_rate >= 0.5
- gap 阈值: match_rate < 0.5 或 0 命中

**验收**: 对 Aria 项目运行 → 输出覆盖度 + 合理缺口

---

### Task 3: agent-creator Skill [3-4h]

**新建**: `aria/skills/agent-creator/SKILL.md`

**核心逻辑**:
- 读取确认后的缺口选择 (coverage-report.yaml 的 gaps[])
- 匹配技术栈模板 (Node.js/Python/Go/Flutter/generic)
- 用 few-shot exemplar (code-reviewer + backend-architect) 生成完整 Agent
- 生成内容: STCO frontmatter + capabilities 字段 + body (Focus Areas 3+ / Approach 3+ / Output 2+)
- 输出预览 → 用户确认

**确认机制**:
- 默认: 交互式预览, 用户确认后写入 `.aria/agents/<name>.md`
- `--dry-run`: 仅预览不写入
- 同名保护: 与现有 Agent 同名时警告 + 要求确认

**技术栈模板**: 
- 4 个专属模板 + 1 个 generic 骨架
- 模板存放: `aria/skills/agent-creator/templates/`

**验收**: 
- 根据 coverage-report 的缺口生成 Agent → STCO 格式正确
- --dry-run 模式不写入文件
- 同名时弹出警告

---

### Task 4: agent-router 运行时注入 [4-5h]

**修改**: `aria/skills/agent-router/SKILL.md`

**核心逻辑**:
- 路由决策时, 扫描 `.aria/agents/` 目录
- 读取每个项目级 Agent 的 STCO description + capabilities
- 注入当前路由上下文 (与插件级 Agent 合并)
- 首次扫描缓存到 `.aria/cache/project-agents.json`
- 缓存失效: `.aria/agents/` 目录 mtime 变化 或 文件数量变化时重新扫描

**同名保护**:
- 项目级与插件级 Agent 同名 → 路由器输出警告
- 提供 `--plugin-only` fallback 描述

**验收**:
- `.aria/agents/` 下放一个 test Agent → router 能路由到它
- 同名时显示警告
- 删除 test Agent 后 → router 不再路由到它 (缓存失效)

---

## Execution Order

```
Task 0 (前置, capabilities)
  ↓
Task 1 (project-analyzer) ←→ Task 2 (gap-analyzer) 可并行开发
  ↓                              ↓
  └──────── 合并后 ────────────────┘
                ↓
Task 3 (agent-creator, 依赖 Task 2 的 coverage-report schema)
  ↓
Task 4 (agent-router, 依赖 Task 3 的 .aria/agents/ 输出)
```

## Acceptance Criteria (总验收)

1. 11 Agent 有 capabilities 字段 + taxonomy.yaml 存在
2. project-analyzer 输出合理画像 (Aria 自身 + unknown 降级)
3. agent-gap-analyzer 输出覆盖度报告 (确定性匹配, 非 LLM)
4. agent-creator 生成 STCO + capabilities + body Agent (含确认机制)
5. agent-router 发现并路由到项目级 Agent (含缓存 + 同名保护)
6. 端到端: 分析 → 缺口 → 确认 → 生成 → 路由 全流程可用

## Deferred (不在 v1.13.0 范围)

- agent-router ROUTING_RULES.md 静态规则更新 (依赖实际路由数据)
- AB benchmark for agent-creator Skill (需先建立 Agent benchmark 机制)
- v2.0 Layer 1 接口契约 (v2.0 M0 定义)
