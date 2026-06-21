# 决策: DEC-20260621-001 - agent-team-audit 项目级 audit agent 增补 (#145)

> **日期**: 2026-06-21 | **模式**: technical brainstorm | **触发**: Forgejo Aria #145 (re-triage verdict `partial-repro`/`major`/`next-cycle`, 见 `.aria/triage-report.json` + `#issuecomment-13407`)

## 背景

`agent-team-audit` 执行流程 step 3 = "按触发点选择 Agent 组合 (见 `agent-selection-matrix.md`)"。该 matrix 是一张**静态表**: 3 个触发点 (pre_merge / post_implementation / post_spec) → 写死的 4 内置 agent (Tech Lead / Code Reviewer / QA Engineer / Knowledge Manager) 子集组合。step 3 **从不查 `.aria/agents/`、从不看 capabilities**。

后果: `agent-gap-analyzer → agent-creator → .aria/agents/<name>.md` 的项目专属 agent 生成链已建成 (含 capabilities tags), 但下游 audit 消费方 (`agent-team-audit`) 永远不会把这些项目 agent 选进审计批次。reporter 实证 (10cg.local): 项目专属 `security-auditor` (shell-safety / ssh-egress) 能抓到 tech-lead/code-reviewer 视角抓不到的 Critical (pct exec 命令注入 / 路径注入), 但当前 audit 架构用不上它们。

**与 M7 边界**: M7 agent-lifecycle Spec 物化 agent 到 `.claude/agents/` (原生) + `.aria/agents/` (source 层)。#145 纯粹是 audit **消费侧** 改造, 与 M7 **正交** (M7 ship 不自动解决 #145)。reporter Option 1 (agent-creator 也写 `.claude/agents/`) 与 M7 重叠, 让给 M7。

**现成范式**: `agent-router` v1.1.0 **已实现**所需机制 —— 扫描 `.aria/agents/*.md` → 合并候选 → 按 capabilities + FP/TT/关键词路由 (含缓存 `.aria/cache/project-agents.json` + 同名保护)。本修复复用这套**发现 + capabilities 匹配**范式, 不另造。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 优先级 | `agent-team-audit` = `experimental: true`, 默认关闭, `agent_team_audit_points` 默认仅 `["pre_merge"]` | 真实影响面有限 → 最小 scope, Level 2 |
| 向后兼容 (Rule #4) | 现有 4-agent 流程零回归 | 增补必须 additive, 降级到纯基线 |
| 复用 (反重复造轮子) | agent-router 已有发现+capabilities 范式; capabilities-taxonomy.yaml 已有词表 | 不新造扫描/词表/schema |
| taxonomy 粒度 | `security-audit` 是单一粗标签, 基线 code-reviewer 已带它 | 排除"baseline 减法"判据 (见方案修正) |

## 考虑的方案

### 选择模型 (项目 agent 与固定基线如何组合)

| 方案 | 描述 | 评分 | 状态 |
|------|------|------|------|
| **Augment 增补** | 基线 4-agent 永远跑; 项目 agent capabilities 命中即 ADD 进本批 (additive) | ⭐ 最小风险, 零回归 | ✅ **选定** |
| Override 覆盖 | 项目 agent 按 capability 替换/顶替同职能内置 agent | 语义强但需覆盖/同名/去重规则, 回归面大 | ❌ OOS (本 cycle) |
| 显式 opt-in 标签 | 项目 agent frontmatter 声明加入哪些检查点 (无 capability 推断) | 零歧义但需 owner 手写 + agent-creator 补字段 | ❌ 未选 |

### 匹配判据 (多匹配才算命中加入)

| 方案 | 描述 | 评分 | 状态 |
|------|------|------|------|
| any-overlap (∩≠∅) | 任一标签重叠即加入 | 最包容但过度触发 (通用标签注水) | ❌ 未选 |
| **专有标签阈值** | 只看 specialist 标签 (security-audit/performance/领域), 排除通用 code-review/documentation | ⭐ 精准命中 reporter 场景, 杜绝噪声 | ✅ **选定** |
| match_rate ≥ 0.5 | 镜像 agent-gap-analyzer 阈值 | 较严, 可能漏单能力专家 agent | ❌ 未选 |

## 最终选择

**模型 = Augment 增补 + 专有标签阈值 (显式策展白名单)**。

`agent-team-audit` step 3 拆两段:
- **step 3a (不变)**: 按 selection-matrix 取该检查点固定基线 (TL/CR/QA/KM 子集)。
- **step 3b (新增)**: 项目 agent 增补 —
  1. **直接读 `.aria/agents/*.md` frontmatter 的 `capabilities`** (agent-router 扫的同一源; `.aria/cache/project-agents.json` 仅可选加速, **不依赖** agent-router 是否先跑过)。
  2. 取该检查点的**"增补 capabilities 白名单"** (matrix 新增列, 显式策展)。
  3. 项目 agent `capabilities ∩ 白名单 ≠ ∅` → 加入本批。
  4. 受现有 `max_parallel_agents` 约束 (不新增 cap)。
- **降级**: `.aria/agents/` 空 / 无白名单命中 → step 3b 空集 → 退化为纯基线 (零回归)。

### ⚠️ 方案修正 (brainstorm 段 2, 由代码核实触发)

段 1 初版判据为 `gap = required − ∪(基线 agent.capabilities)` (派生减法)。**核实暴露缺陷**: 基线 `code-reviewer` 已带 `security-audit` 标签 → 减法会把 reporter 的 security-auditor "盖住"排除, 恰好打不中其核心用例。根因: taxonomy 的 `security-audit` 太粗, 无法区分"通用安全过一眼"vs"领域专职深审"。

**修正**: 放弃 baseline 减法, 改为**每检查点显式策展 specialist 白名单**, 项目 agent ∩ 白名单 ≠ ∅ 即加入, **不管基线是否名义上也带该标签** (基线通用维度 + 项目专家纵深 = 互补非冗余)。白名单**只放** specialist 标签 (security-audit / performance-optimization / 领域标签), **不放** code-review / documentation-audit 等基线本职通用维度。白名单值锚定 `capabilities-taxonomy.yaml` 既有标签。

初版策展 (proposal 待细化):

| 触发点 | 基线 (固定) | 增补 capabilities 白名单 (新列) |
|--------|------------|----------------------------------|
| pre_merge | TL+CR+KM | security-audit, performance-optimization |
| post_implementation | CR+QA | security-audit, performance-optimization |
| post_spec | TL+KM | (默认空 → 纯基线) |

## Spec & 文件清单

**Level 2** (proposal.md only)。单一 experimental skill 行为改造, additive, 复用现成 taxonomy + 发现范式, 无新 artifact schema。

| 文件 | 变更 |
|------|------|
| `aria/skills/agent-team-audit/SKILL.md` | step 3 → 3a (基线不变) + 3b (项目 agent 增补算法) |
| `aria/skills/agent-team-audit/references/agent-selection-matrix.md` | 新增"增补 capabilities 白名单"列 + 三检查点策展值 + 算法说明 |
| (可能) `agent-team-audit/references/` 新 ref | 增补算法详述 (若 SKILL.md 篇幅压力) |

## 测试 / 回归 (Rule #6)

`agent-team-audit` = **prose/process skill** (非确定性 code) → Rule #6 substitute = **structural fixture + dogfood-by-construction** (per memory `feedback_deterministic_structural_skill_rule6_substitute` / `feedback_rule6_framing_differs_by_skill_type`):
- structural fixture: 造 `.aria/agents/` 含带 `security-audit` 标签 fake 项目 agent → 验 pre_merge 批次含它; 仅带通用 `code-review` → 验**不**纳入; 空目录 → 验纯基线。
- dogfood: 本 Aria 项目实跑一次 pre_merge (临时开 `experiments.agent_team_audit`) 验不破现有 4-agent 流程。

## OOS (明确不做)

- ❌ Option 1 (agent-creator 写 `.claude/agents/`) → 让给 M7 agent-lifecycle (正交, 避免重叠)
- ❌ Override / 替换语义 → 本 cycle 仅 augment
- ❌ 扩 taxonomy 加细粒度 specialist 标签 (shell-safety / ssh-egress 等) → 用既有标签, 细化留后续 cycle
- ❌ 改 `agent-router` / 任务路由路径 → triage 已确认那条路正常 (项目 agent 在任务路由已被感知, 断裂特定于 audit 编排路径)

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 增补 agent 失控放大并发/成本 | 受现有 `max_parallel_agents` 约束; 白名单只放 specialist 标签 (非通用维度) 限制命中面 |
| 白名单策展过宽 → 噪声 | 默认 post_spec 白名单空; pre_merge/post_implementation 仅 security-audit/performance 两项起步 |
| 项目 agent capabilities 字段缺失/畸形 | step 3b 读 frontmatter 失败 → skip 该 agent (不阻断基线); 降级到纯基线 |
| taxonomy 粗粒度仍无法区分领域深审 | 本 cycle 用既有标签 (security-audit 命中即纳入领域 security agent); 细粒度标签留后续, 在 OOS 透明披露 |
| 与 M7 边界混淆 | OOS 明确 Option 1 让给 M7; 本 cycle 纯消费侧, 不碰物化 |

## 后续 (Phase A)

- post_brainstorm audit checkpoint **配置为 `off`** (项目刻意, 集中 audit 预算在 post_spec) → 本决策记录不经 post_brainstorm 审计。
- 真实 audit gate = **Phase A spec-drafter 写 proposal.md 后的 post_spec** (audit-engine convergence 多轮收敛)。
- Phase B 不受 M6/M7 时机门约束 (本 cycle 与主线解耦, 属等待期填空)。
