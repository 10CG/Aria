# 十步循环自动审计系统

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-04-01
> **Parent Story**: US-004
> **Target Version**: v1.2.0

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

**挑战审计 (challenge)**: 讨论组提案 → 挑战组质疑 → 全员合并讨论 → 循环直到收敛且无反对

**收敛判定**: 结论集合无变化 + 全票 PASS 双重验证

### 检查点

| 检查点 | 阶段 | 状态 | 侧重 |
|--------|------|------|------|
| post_brainstorm | A.0 | 新增 | 决策验证 — 头脑风暴结论是否经过充分挑战 |
| post_spec | A.1 | 已有 | 决策验证 — Spec 的完整性和可行性 |
| post_planning | A.2 | 新增 | 质量保障 — 任务分解是否有遗漏 |
| post_implementation | B.2 | 已有 | 质量保障 — 实现是否符合 Spec |
| mid_implementation | B.2 | 新增 | 质量保障 — 大功能中途方向检查 |
| pre_merge | C.2 | 已有 | 共识构建 — 多视角合并前审查 |
| post_closure | D.1 | 新增 | 共识构建 — 收尾复盘，积累经验 |

### Agent 分组策略

**按检查点动态分组**（配置化，非运行时判断）：

- 每个检查点预定义 convergence_agents, discussion, challenge 列表
- 根据议题性质分配"方案提出方"和"质疑方"
- 例: post_spec → 讨论组 [tech-lead, backend-architect], 挑战组 [qa-engineer, knowledge-manager]

**config-loader 自动裁剪**：

- 首次运行时分析项目特征（技术栈、目录结构、测试框架）
- 推断相关 Agent 子集，排除不适用的 Agent（如无 mobile/ 则排除 mobile-developer）
- 生成裁剪后的审计配置，用户可覆盖

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
        "convergence": ["tech-lead", "backend-architect"],
        "discussion": ["tech-lead"],
        "challenge": ["backend-architect", "qa-engineer"]
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

### 执行流程

**convergence 模式**:

```
Round N:
  spawn agent team → 各 Agent 独立分析
  → 汇总引擎合并输出
  → 结论提取: { decisions: [], issues: [], risks: [] }
  → 与 Round N-1 比较
  → 收敛? (结论无变化 + 全票 PASS)
    → 是 → 输出审计报告 ✅
    → 否 → Round N+1 (输入: 上轮结论, 任务: 审查修正)
  → max_rounds 达到 → 未收敛警告 + 人工介入
```

**challenge 模式**:

```
Round N:
  讨论组 spawn → 统一提案
  → 挑战组 spawn → 反对意见列表
  → Round N+1: 全员讨论 (提案 + 反对意见) → 修正提案
  → 挑战组再审 → 新反对意见?
  → 收敛? (提案结论无变化 + 反对意见为空)
    → 是 → 输出审计报告 ✅
    → 否 → 继续
```

### 审计报告格式

存储位置: `.aria/audit-reports/{checkpoint}-{timestamp}.md`

```markdown
---
checkpoint: {checkpoint_name}
mode: convergence | challenge
rounds: {N}
converged: true | false
timestamp: {ISO 8601}
context: {被审计内容的路径}
---

## 审计结论
### Decisions (收敛)
### Issues (已解决)
### Risks (已识别)

## 轮次记录
### Round 1 ... Round N
```

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 多轮收敛确保决策经过充分验证，减少 AI 自信偏差 |
| **Positive** | 挑战模式引入对抗视角，发现单一视角遗漏的风险 |
| **Positive** | 7 个检查点覆盖全流程，不留质量盲区 |
| **Risk** | Token 消耗显著增加（多轮 x 多 Agent），通过 adaptive 模式和 max_rounds 控制 |
| **Risk** | 收敛可能需要多轮，影响开发速度，通过默认关闭 + 按需启用缓解 |

## Constraints

| 约束 | 影响 |
|------|------|
| 默认关闭 | 不影响现有用户体验，opt-in 启用 |
| max_rounds = 5 | 防止无限循环，可配置 |
| 配置化分组 | 不依赖运行时 AI 判断，确定性行为 |
| 向后兼容 | 现有 agent-team-audit 配置继续工作 |

## Dependencies

- config-loader 扩展（项目特征分析 + 配置自动生成）
- 现有 agent-team-audit（升级为多轮收敛）
- 7 个 Phase Skills 需集成检查点触发逻辑

## Success Criteria

- [ ] convergence 模式在 3 轮内收敛率 > 80%
- [ ] challenge 模式发现至少 1 个 convergence 模式遗漏的问题（对比测试）
- [ ] config-loader 自动生成配置准确率 > 90%（Agent 选择与项目实际匹配）
- [ ] 未收敛警告触发时，人工介入后可恢复流程
- [ ] 审计报告可被后续 Phase Skill 引用（决策可追溯）
