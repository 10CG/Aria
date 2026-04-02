# 十步循环自动审计系统

> **Level**: Full (Level 3 Spec)
> **Status**: Draft (Reviewed — 3-round convergence audit applied)
> **Created**: 2026-04-01
> **Reviewed**: 2026-04-02
> **Parent Story**: [US-004](../../docs/requirements/user-stories/US-004.md)
> **Target Version**: v1.9.0 (当前 plugin v1.8.0, 新增 Skill = MINOR)
> **Audit Report**: [.aria/audit-reports/post_spec-2026-04-01T23.md](../../.aria/audit-reports/post_spec-2026-04-01T23.md)

## Why

当前 Aria 的 agent-team-audit 是单轮审计 — spawn agents, 收集意见, 输出 verdict。这种模式存在局限：

1. **一轮不够深入** — Agent 之间无法对彼此意见进行质疑和修正，遗漏难以被发现
2. **无对抗机制** — 所有 Agent 角色平等，没有"挑战者"视角，容易形成 AI 的自信偏差
3. **触发点有限** — 仅 3 个检查点（post_spec, post_implementation, pre_merge），规划和收尾阶段无审计
4. **无收敛保证** — 单轮即结束，无法判断意见是否充分

需要一个多轮收敛的审计系统，在十步循环的关键环节自动触发，确保质量、决策和共识经过充分验证。

## What

### 核心设计

两种审计模式，7 个检查点，按复杂度自适应或手动配置：

**循环审计 (convergence)**: 全员讨论 → 结论提取 → 审查上轮结论 → 循环直到收敛

**挑战审计 (challenge)**: 讨论组提案 → 挑战组质疑 → 全员合并讨论 → 循环直到收敛且反对意见全部 resolved

**收敛判定**: 结论集合无变化（结构化比较）+ 全票 PASS 双重验证

### 架构关系: audit-engine 与 agent-team-audit

```
audit-engine (新建, 多轮编排层)
    │
    │ 调用 (每轮)
    ▼
agent-team-audit (现有, 退化为单轮执行引擎)
    │
    │ spawn
    ▼
各 Agent (按检查点配置的 team)
```

**关系**: 组合而非替代。audit-engine 负责多轮编排和收敛判定，agent-team-audit 保持为单轮执行引擎被 audit-engine 调用，最大化复用现有并发控制、超时策略、去重算法。

### 检查点

| 检查点 | 阶段 | 状态 | 侧重 | 触发位置 |
|--------|------|------|------|----------|
| post_brainstorm | A (brainstorm 结束后) | 新增 | 决策验证 | brainstorm Skill 内部 |
| post_spec | A.1 | 已有→升级 | 决策验证 | phase-a-planner |
| post_planning | A.2 | 新增 | 质量保障 | task-planner |
| post_implementation | B.2 | 已有→升级 | 质量保障 | phase-b-developer |
| mid_implementation | B.2 | 新增 | 质量保障 | phase-b-developer (条件触发) |
| pre_merge | C.2 | 已有→升级 | 共识构建 | phase-c-integrator |
| post_closure | D.1 | 新增 | 经验积累 | phase-d-closer |

**"已有→升级"**: 现有 3 个检查点从单轮 agent-team-audit 升级为多轮 audit-engine 编排。

**post_closure 限制**: 代码已合并后无法回退，此检查点限制为 convergence 模式 + max_rounds=1，侧重经验提取而非质量阻塞。

**mid_implementation 触发条件**: 可配置，非运行时 AI 判断：

```json
"mid_implementation": {
  "trigger": "task_progress",
  "threshold": 50,
  "unit": "percent_tasks_completed"
}
```

当已完成任务数 ≥ 总任务数 × threshold% 时触发。由 phase-b-developer 在每个任务完成后检查。

### 收敛判定算法

#### 结论比较 (结构化字段匹配)

每条结论提取为结构化记录：

```json
{
  "id": "auto-generated-hash",
  "type": "decision | issue | risk",
  "severity": "critical | major | minor",
  "category": "architecture | implementation | testing | documentation",
  "scope": "affected module or file",
  "summary": "truncated to 50 words"
}
```

**比较算法**: 基于 `{type, severity, category, scope}` 四元组的集合相等。`summary` 不参与比较（消除 AI 措辞差异的噪声）。

**收敛条件**:
- `Round N` 结论集的四元组集合 = `Round N-1` 结论集的四元组集合
- AND 全员投票 PASS（convergence 模式: convergence_agents 全员; challenge 模式: 挑战组无 unresolved 反对意见）

**振荡检测**: 若 Round N 结论 = Round N-2 结论（隔轮重复），标记为"噪声振荡"，自动取最后轮结论，不要求人工介入。

### 汇总引擎

audit-engine 的内部组件，非独立 Skill。职责：

1. **合并**: 收集同一轮所有 Agent 的输出
2. **去重**: 基于 `{category, scope}` 去重（复用 agent-team-audit 已有算法）
3. **冲突解决**: 同一 scope 上的矛盾意见保留双方，标记为 `conflicted`，不自动裁决
4. **结构化提取**: 将自由文本输出转换为上述结构化记录

### Challenge 模式数据 Schema

```
Round N 数据流:

讨论组输出 (discussion_output):
  {
    proposal: string,          // 统一提案文本
    decisions: [{severity, category, scope, summary}],
    rationale: [string]
  }
         ↓
挑战组输入: discussion_output
挑战组输出 (challenge_output):
  {
    objections: [{
      agent: string,
      target_decision: string,   // 指向 proposal 中的哪个决策
      severity: "critical | major | minor",
      point: string,
      status: "new"              // new → resolved | overruled
    }]
  }
         ↓
全员合并输入: discussion_output + challenge_output
全员输出: 修正后的 discussion_output
         ↓
挑战组再审: 修正后的 discussion_output
挑战组输出: 更新 objections (status: resolved | new)
         ↓
收敛判定:
  - 提案结论四元组集合无变化
  - AND objections 全部 status=resolved (无 unresolved)
```

**Round 计数**: 一个 Round = 讨论组提案 + 挑战组质疑的完整周期。全员合并讨论属于下一 Round 的开头。max_rounds=5 意味着最多 5 个完整周期。

### Severity/Verdict 兼容

新系统继承现有 Severity 体系：

| 字段 | 来源 | 说明 |
|------|------|------|
| severity | agent-team-audit (Critical/Major/Minor) | 每条 issue/risk 必须标注 |
| verdict | 从 severity 计算 | ≥1 Critical → FAIL, ≥1 Major → PASS_WITH_WARNINGS, 仅 Minor → PASS |

审计报告输出同时包含 `converged` (收敛状态) 和 `verdict` (质量判定)：

- `converged: true, verdict: PASS` → 正常通过
- `converged: true, verdict: FAIL` → 收敛但有 Critical 问题，阻塞流程
- `converged: false` → 未收敛，触发降级策略

### 配置 Schema

```json
{
  "audit": {
    "enabled": false,
    "mode": "adaptive",
    "max_rounds": 5,
    "convergence_criteria": {
      "conclusion_match": true,
      "unanimous_pass": true
    },
    "adaptive_rules": {
      "level_1": "off",
      "level_2": "convergence",
      "level_3": "challenge"
    },
    "priority_rule": "checkpoints 显式配置 > adaptive_rules 推导 > 默认 off",
    "mid_implementation": {
      "trigger": "task_progress",
      "threshold": 50,
      "unit": "percent_tasks_completed"
    },
    "checkpoints": {
      "post_brainstorm": "off",
      "post_spec": "off",
      "post_planning": "off",
      "post_implementation": "off",
      "mid_implementation": "off",
      "pre_merge": "off",
      "post_closure": "off"
    },
    "teams": {
      "post_brainstorm": {
        "convergence": ["tech-lead", "backend-architect", "knowledge-manager"],
        "discussion": ["tech-lead"],
        "challenge": ["backend-architect", "qa-engineer", "knowledge-manager"]
      },
      "post_spec": {
        "convergence": ["tech-lead", "backend-architect", "qa-engineer", "knowledge-manager"],
        "discussion": ["tech-lead", "backend-architect"],
        "challenge": ["qa-engineer", "knowledge-manager"]
      },
      "post_planning": {
        "convergence": ["tech-lead", "qa-engineer"],
        "discussion": ["tech-lead"],
        "challenge": ["qa-engineer", "backend-architect"]
      },
      "post_implementation": {
        "convergence": ["code-reviewer", "backend-architect", "qa-engineer"],
        "discussion": ["code-reviewer", "backend-architect"],
        "challenge": ["qa-engineer", "tech-lead"]
      },
      "mid_implementation": {
        "convergence": ["tech-lead", "code-reviewer"],
        "discussion": ["code-reviewer"],
        "challenge": ["tech-lead"]
      },
      "pre_merge": {
        "convergence": ["code-reviewer", "qa-engineer", "tech-lead"],
        "discussion": ["code-reviewer", "qa-engineer"],
        "challenge": ["tech-lead", "knowledge-manager"]
      },
      "post_closure": {
        "convergence": ["tech-lead", "knowledge-manager"],
        "discussion": ["tech-lead"],
        "challenge": ["knowledge-manager", "qa-engineer"]
      }
    }
  }
}
```

**配置优先级**: `checkpoints` 显式值 > `adaptive_rules` 推导值 > 默认 `"off"`。当 `mode=adaptive` 且用户手动设置 `post_spec: "convergence"` 时，手动配置优先。

**旧配置兼容**: config-loader 读取时，若检测到 `experiments.agent_team_audit: true` 且无 `audit` 块，自动映射为 `audit.enabled: true` + `audit.mode: "manual"` + 旧 `agent_team_audit_points` 映射到对应 checkpoints，并输出迁移提示。

### 执行流程

**convergence 模式**:

```
Round N:
  spawn agent team (通过 agent-team-audit 单轮引擎)
  → 各 Agent 独立分析
  → 汇总引擎: 合并 + 去重 + 结构化提取
  → 结论记录: [{ type, severity, category, scope, summary }]
  → 与 Round N-1 比较 (四元组集合)
  → 振荡检测 (Round N = Round N-2?)
  → 收敛判定:
    收敛 → 计算 verdict → 输出审计报告 ✅
    振荡 → 取最后轮结论 → 输出报告 + 振荡标记
    未收敛 + max_rounds → 降级策略
    未收敛 + 有余量 → Round N+1
```

**challenge 模式**:

```
Round N (一个完整周期):
  Step 1: 讨论组 spawn → discussion_output
  Step 2: 挑战组 spawn (输入: discussion_output) → challenge_output
  Step 3: 全员讨论 (输入: discussion_output + challenge_output) → 修正 proposal
  Step 4: 挑战组再审 (输入: 修正 proposal) → 更新 objections status
  → 收敛判定:
    提案四元组无变化 + objections 全部 resolved → 输出报告 ✅
    否则 → Round N+1
  → max_rounds 达到 → 降级策略
```

### 错误处理

| 场景 | 行为 |
|------|------|
| Agent spawn 失败 | 跳过该 Agent，当轮结论标记 `incomplete: true`，不阻塞收敛 |
| Agent 超时 (继承 agent-team-audit 的 120s) | 同 spawn 失败处理 |
| API 限流 (529) | 等待 30s 重试一次，仍失败则跳过 |
| 部分收敛 (结论无变化但有 REVISE 投票) | 继续下一轮 |
| 全部 Agent 失败 | 当轮作废，输出错误报告，不计入 max_rounds |

### 降级策略 (未收敛时)

当 max_rounds 耗尽且未收敛：

1. **展示摘要**: 输出最后轮结论 + 各轮差异对比 + 未收敛原因分析
2. **三路径选择** (通过 AskUserQuestion):
   - `[1] 接受当前结论` — 标记 `converged: false, overridden_by_user: true`，继续流程
   - `[2] 增加轮次` — 临时将 max_rounds +2，继续审计
   - `[3] 降级为单轮` — 取最后轮结论作为最终结果，标记 `degraded: true`

### 并发控制 (多轮场景)

| 参数 | 值 | 说明 |
|------|-----|------|
| 单轮并发 | 继承 agent-team-audit (max_parallel: 2, hard_cap: 3) | 每轮内的 Agent 并发 |
| 轮次间 | 串行 | 下一轮依赖上一轮结论 |
| overall 超时 | 每轮独立计时 (继承 300s/轮) | 不跨轮累计 |
| challenge 组间 | 串行 (讨论组→挑战组→全员) | 数据依赖 |

### 审计报告格式

存储位置: `.aria/audit-reports/{checkpoint}-{timestamp}.md`

```markdown
---
checkpoint: {checkpoint_name}
mode: convergence | challenge
rounds: {N}
converged: true | false
overridden_by_user: false
degraded: false
verdict: PASS | PASS_WITH_WARNINGS | FAIL
timestamp: {ISO 8601}
context: {被审计内容的路径 — proposal.md / diff / UPM}
agents: [{agent_list}]
---

## 审计结论

### Decisions (收敛)
- [{severity}] {category}/{scope}: {summary}

### Issues (已解决)
- [{severity}] {category}/{scope}: {summary}

### Risks (已识别)
- [{severity}] {category}/{scope}: {summary}

## Verdict
{verdict} — {rationale}

## 轮次记录
### Round 1 ... Round N
```

### Token 消耗估算

| 场景 | 估算 |
|------|------|
| 单检查点 convergence (3 agents, 2 轮收敛) | ~12K tokens |
| 单检查点 challenge (4 agents, 3 轮收敛) | ~30K tokens |
| Level 2 full cycle (adaptive, ~3 检查点) | ~36K tokens |
| Level 3 full cycle (adaptive, ~5 检查点) | ~120K tokens |
| 最坏 (7 检查点 x 5 轮 x 4 agents) | ~280K tokens |

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 多轮收敛确保决策经过充分验证，减少 AI 自信偏差 |
| **Positive** | 挑战模式引入对抗视角，发现单一视角遗漏的风险 |
| **Positive** | 7 个检查点覆盖全流程，不留质量盲区 |
| **Risk** | Token 消耗增加 (Level 2 ~36K, Level 3 ~120K)，通过 adaptive + max_rounds 控制 |
| **Risk** | 收敛振荡（同模型非确定性输出），通过隔轮振荡检测 + 自动取最后轮缓解 |
| **Limitation** | 挑战组与讨论组共享底层模型，对抗质量依赖 prompt 角色差异化 |

## Constraints

| 约束 | 影响 |
|------|------|
| 默认关闭 | 不影响现有用户体验，opt-in 启用 |
| max_rounds = 5 | 防止无限循环，可配置 |
| 配置化分组 | 不依赖运行时 AI 判断，确定性行为 |
| 向后兼容 | 旧 experiments.agent_team_audit 配置自动映射到新 audit.* 块 |
| 组合关系 | audit-engine 编排 + agent-team-audit 执行，旧 Skill 保留不废弃 |
| post_closure 限制 | 仅 convergence + max_rounds=1，侧重经验提取 |

## Dependencies

- config-loader 扩展（旧配置兼容映射 + 项目特征分析生成建议配置）
- agent-team-audit（保留为单轮执行引擎，被 audit-engine 调用）
- brainstorm（post_brainstorm 触发点集成）
- task-planner（post_planning 触发点集成）
- phase-a-planner, phase-b-developer, phase-c-integrator, phase-d-closer（检查点升级/新增）
- state-scanner（adaptive 模式复杂度评估传递）

## Success Criteria

- [ ] audit-engine AB 测试: with_skill delta > 0 (使用 /skill-creator, 结果存 aria-plugin-benchmarks/)
- [ ] convergence 模式: 在 ≥5 个测试场景中，3 轮内收敛率 > 80%
- [ ] challenge vs convergence 对比: 在 ≥5 个 post_spec 场景中，challenge 额外发现 issue 率 > 0%
- [ ] config-loader 裁剪: 在 3 个已知项目 (Aria, Kairos, +1) 上，Agent 选择 F1 ≥ 0.9
- [ ] 未收敛降级: max_rounds 耗尽时，三路径选择可用且流程可恢复
- [ ] 被修改 Phase Skills 回归: 所有被修改 Skill 的 AB delta ≥ 0 (无回归)
- [ ] 审计报告可被后续 Phase Skill 通过路径约定引用
