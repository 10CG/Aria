# agent-team-audit-project-agent-augmentation

> **Status**: ✅ **SHIPPED 2026-06-21** (aria-plugin **v1.48.0**, PR [#89](https://forgejo.10cg.pub/10CG/aria-plugin/pulls/89) merge `a922e5c` 双远程; agent-team-audit 1.0.0→1.1.0)。Phase A.2 post_spec R1 REVISE → Rev1 7 项全落地 → **R2 CONVERGED** [unanimous PASS 2/2]; Phase B 实施 3 文件改 + 5 structural fixture; code-review Phase 1 PASS + Phase 2 I-1/I-2/M-1/M-2 全收; AC-5 dogfood 纯基线零回归确认。审计报告 `.aria/audit-reports/post_spec-R2-2026-06-21-*`。Closes #145。
> **Level**: 2 (Minimal — proposal only, 单 experimental skill 行为改造, additive)
> **Target skill**: `aria/skills/agent-team-audit` (aria-plugin)
> **Target version**: v1.47.0 → **v1.48.0** (MINOR — 新增 audit agent 选择能力: 项目级 audit agent 按 capabilities 增补; additive, 默认行为不变)
> **Forgejo issue**: [Aria #145](https://forgejo.10cg.pub/10CG/Aria/issues/145) (re-triage verdict `partial-repro`/`major`/`next-cycle`, `#issuecomment-13407`)
> **决策记录**: [DEC-20260621-001](../../../.aria/decisions/DEC-20260621-001-agent-team-audit-project-agent-augmentation.md)

## Why

`agent-team-audit` 执行流程 step 3 = "按触发点选择 Agent 组合 (见 `agent-selection-matrix.md`)"。该 matrix 是**静态表**: 3 触发点 (pre_merge / post_implementation / post_spec) → 写死的 4 内置 agent (Tech Lead / Code Reviewer / QA Engineer / Knowledge Manager) 子集。step 3 **从不查 `.aria/agents/`、从不看 capabilities**。

后果: `agent-gap-analyzer → agent-creator → .aria/agents/<name>.md` 项目专属 agent 生成链 (含 capabilities tags) 已建成, 但下游 audit 消费方永远不把项目 agent 选进审计批次。reporter 实证 (10cg.local): 项目专属 `security-auditor` (shell-safety / ssh-egress) 能抓 tech-lead/code-reviewer 视角抓不到的 Critical (pct exec 命令注入 / 路径注入), 当前 audit 架构用不上。

**断裂特定于 audit 编排路径**: triage 已确认 `agent-router` 任务路由路径**会**扫 `.aria/agents/` 感知项目 agent (`agent-router` SKILL.md:397); subagent-driver 契约含 `agent_source: "project"`。唯独 `agent-team-audit` 选择逻辑写死, 不消费项目 agent。

**与 M7 正交**: M7 agent-lifecycle 物化 agent 到 `.claude/agents/` (原生) + `.aria/agents/` (source 层) —— 解决"项目 agent 如何被原生加载"。本 change 是 audit **消费侧** 改造 (selection-matrix 按 capabilities 选项目 agent), M7 ship 不自动解决。reporter Option 1 (agent-creator 也写 `.claude/agents/`) 与 M7 重叠 → OOS, 让给 M7。

**复用现成范式**: `agent-router` v1.1.0 已实现"扫描 `.aria/agents/*.md` → 按 capabilities 路由"(含缓存 + 同名保护)。本 change 复用此**发现 + capabilities 匹配**范式, 不另造。

## What Changes

### 1. `agent-team-audit/SKILL.md` step 3 拆两段 (additive)

```
step 3a (不变): 按 selection-matrix 取该检查点固定基线 (TL/CR/QA/KM 子集)
step 3b (新增): 项目 agent 增补
  1. 读 .aria/agents/*.md frontmatter 的 capabilities (agent-router 扫的同一源;
     .aria/cache/project-agents.json 仅可选加速, 不依赖 agent-router 是否先跑过)
  2. 取该检查点的 "增补 capabilities 白名单" (matrix 新增列)
  3. 项目 agent capabilities ∩ 白名单 ≠ ∅ → 加入本批
  4. 增补 agent 同基线一样进入 batch 调度队列, 受 max_parallel_agents 节流
     但 **不被丢弃** —— 超出并发预算的多出 agent 串行分批跑 (与 matrix §并发调度
     既有"基线 >max 时分 Batch"语义一致, 不新增 cap)
```

> **并发语义澄清 (R1 tech-lead I-1)**: pre_merge 基线已是 3 agent, 默认 `max_parallel_agents=2` 时本就分 Batch (matrix §并发调度已有此设计)。增补 agent 加入同一调度队列, **节流但不丢弃** (排队后续批跑完)。故 AC-1 "批次包含增补 agent" 在默认配置下仍稳定可证 (增补 agent 必被启动, 只是可能在后续 batch)。

### 2. `agent-selection-matrix.md` 新增 "增补 capabilities 白名单" 列 (显式策展)

| 触发点 | 基线 (固定) | 增补 capabilities 白名单 (新列) |
|--------|------------|----------------------------------|
| pre_merge | TL+CR+KM | `security-audit`, `performance-optimization` |
| post_implementation | CR+QA | `security-audit`, `performance-optimization` |
| post_spec | TL+KM | (默认空 → 纯基线) |

**判据 = 专有标签阈值 (非 baseline 减法)**: 白名单**只放** specialist 标签, **不放** `code-review`/`documentation-audit` 等基线本职通用维度; 项目 agent 命中白名单即加入, **不管基线是否名义上也带该标签** (基线通用维度 + 项目专家纵深 = 互补非冗余)。白名单值锚定 `capabilities-taxonomy.yaml` 既有标签。

> **为何非 baseline 减法** (DEC 段 2 修正): 基线 `code-reviewer` 已带 `security-audit` 标签。若按 `gap = required − ∪(基线.capabilities)` 派生, `security-audit` 在 pre_merge 被 code-reviewer 盖住 → 项目 security-auditor 反被排除, 恰好打不中 reporter 用例。根因 taxonomy 粗粒度 → 改显式白名单解耦。

### 3. 降级 (零回归保证)

`.aria/agents/` 空 / frontmatter 读取失败 (skip 该 agent, 不阻断基线) / 无白名单命中 → step 3b 空集 → 退化为**今天的纯基线行为**。

### 4. 文档同步连带更新 (R1 knowledge-manager Important-1, Rule #3)

step 3b 上线后, 以下硬编码固定基线的文档会产生"漏增补 agent"的误导性过时内容, 一并更新:

| 文档 | 现状 (硬编码基线) | 改动 |
|------|------------------|------|
| `agent-team-audit/references/audit-points.md` | 每检查点 `agents:` 字段 (L7-8/36-38/64-65/103-104) 列死基线 | 各 `agents:` 字段下加注 "动态增补: 见 SKILL.md step 3b + agent-selection-matrix.md 白名单" |
| `agent-team-audit/SKILL.md` 触发点表 (L48-52) | `Agents` 列写死 `Tech Lead + Code Reviewer + Knowledge Manager` 等 | `Agents` 列基线后加 "(+ 项目级增补, 见 step 3b)" |
| `agent-team-audit/SKILL.md` 输出格式 (L136/156/174) | "Agents 参与: 3/3" 分母为固定基线数 | 分母改为当次实际批次总数 (基线 + 增补之和); 增补 agent 在列表中标注来源 (项目级) |

## Impact

- **Affected skill**: `agent-team-audit` (experimental, `experimental: true`, 默认关闭, `agent_team_audit_points` 默认 `["pre_merge"]`)。
- **向后兼容 (Rule #4)**: additive。未启用 experiment / `.aria/agents/` 空 / 无白名单命中 → 行为与今天**逐字节相同**。
- **无新 artifact schema**: 复用 `.aria/agents/*.md` (agent-creator 既有输出) + `capabilities-taxonomy.yaml` (既有词表) + `.aria/cache/project-agents.json` (agent-router 既有缓存, 可选)。
- **测试 / 回归 (Rule #6)**: `agent-team-audit` = prose/process skill (非确定性 code) → Rule #6 substitute = **structural fixture + dogfood-by-construction** (per memory `feedback_deterministic_structural_skill_rule6_substitute`):
  - structural fixture: 造 `.aria/agents/` 含带 `security-audit` 标签 fake 项目 agent → 验 pre_merge 批次纳入; 仅带通用 `code-review` → 验**不**纳入; 空目录 → 验纯基线。
  - dogfood: 本 Aria 项目实跑一次 pre_merge (临时开 `experiments.agent_team_audit`) 验不破现有 4-agent 流程。
- **文档同步 (Rule #3)**: `agent-team-audit/SKILL.md` (step 3 算法 + 触发点表 Agents 列 + 输出格式分母) + `agent-selection-matrix.md` (新列 + 说明) + `audit-points.md` (各 `agents:` 字段加动态增补注记) 同步更新 (见 What Changes §4)。
- **能力可用性受 experiment 状态门控 (R1 tech-lead M-1, 透明披露)**: 本 change 把"按 capabilities 选项目 audit agent"绑在 `agent-team-audit` (`experimental: true`, 默认关) 上。reporter 痛点 (security-auditor 抓 Critical) 在 experiment 转正 (default-on) 前**仍享受不到** —— experiment 转正是**独立后续决策, 不在本 change**。ship 本 change ≠ 痛点即解。

## Out of scope

- ❌ **Option 1 (agent-creator 写 `.claude/agents/`)** → 让给 M7 agent-lifecycle (正交, 避免重叠)。
- ❌ **Override / 替换语义** (项目 agent 顶替内置 agent) → 本 change 仅 augment; 替换需覆盖/同名/去重规则, 回归面大。
- ❌ **扩 taxonomy 加细粒度 specialist 标签** (shell-safety / ssh-egress 等) → 用既有 `security-audit` 等粗标签命中领域 security agent; 细粒度留后续 cycle。
- ❌ **改 `agent-router` / 任务路由路径** → triage 确认该路径正常 (项目 agent 已被任务路由感知), 断裂特定于 audit 编排路径。
- ❌ **各检查点白名单内容策展** 超出当前 MVP 初始值 (pre_merge/post_implementation: `security-audit`, `performance-optimization`; post_spec: 空) → 扩充留后续 cycle。
- ❌ **agent-team-audit experiment 转正 (default-on)** → 独立后续决策; 本 change 只补能力, 不改 experiment 默认状态。

## 验收标准 (AC)

- **AC-1**: `.aria/agents/` 含带白名单 capability (如 `security-audit`) 的项目 agent 时, 对应检查点 (pre_merge) 审计批次**包含**该 agent (基线 + 增补)。*(验证手段: structural fixture, 见 AC-6; 增补 agent 受 max_parallel_agents 节流但不丢弃, 见 What Changes §1 并发语义)*
- **AC-2**: `.aria/agents/` 仅含通用标签 (`code-review`/`documentation-audit`) 项目 agent 时, **不**纳入 (白名单不含通用维度)。*(验证手段: structural fixture)*
- **AC-3**: `.aria/agents/` 空 / experiment 未启用 → 审计批次 = 纯基线 (与改造前逐字节相同, 零回归)。
- **AC-4**: 项目 agent frontmatter 边界 (R1 tech-lead M-2 收敛为可证形式): `capabilities` 字段缺失 / 非 list 类型 / 文件 YAML parse 失败 → **skip 该 agent**, 不阻断基线; `capabilities` 空 list → **合法** (= 无白名单命中, 等价不纳入, 非 skip-as-error)。structural fixture 须覆盖空 list 边界。
- **AC-5**: dogfood (R1 km Important-2 澄清范围) — 本 Aria 项目**无 `.aria/agents/` 目录** → dogfood 实跑 pre_merge (临时开 experiment) 仅验证 **AC-3 纯基线零回归** (不破现有 4-agent 流程) + SKILL.md/matrix/audit-points 文档同步。AC-1/AC-2/AC-4 核心场景由 AC-6 structural fixture 验证, **不**由 dogfood 验证。
- **AC-6** (R1 km Important-2 新增, 绑定验证手段): structural fixture 三组场景全部验证通过 —— (a) 造带 `security-audit` 标签 fake 项目 agent → pre_merge 批次纳入; (b) 仅带通用 `code-review` → 不纳入; (c) 空目录 / 空 list → 纯基线退化。这是 AC-1/AC-2/AC-4 的执行载体 (Rule #6 structural substitute)。
- **AC-7**: 文档同步完整 (What Changes §4) — `audit-points.md` 各 `agents:` 字段、SKILL.md 触发点表 Agents 列、输出格式分母 全部加注/更新动态增补, 无遗漏过时硬编码基线。

## Resolved (Rev1 — post_spec R1)

R1 (tech-lead PASS_WITH_WARNINGS + knowledge-manager REVISE) → **REVISE**, 关键技术断言全部由真代码核实成立, 无虚构。Rev1 全落地 (7 项):

| # | lens / sev | 项 | 落地 |
|---|-----------|----|------|
| I-1 | tech-lead / Important | 增补 agent 与 `max_parallel_agents` 交互未定义 → AC-1 默认配置可证性 | What Changes §1 step 3b 第 4 点 + 并发语义澄清块: 节流但不丢弃, 分批串行; AC-1 标注验证前提 |
| K-1 | km / Important | 文档同步漏 `audit-points.md` `agents:` 字段 + SKILL.md 触发点表/输出格式 | 新增 What Changes §4 文档同步连带更新表 + Impact 文档同步扩列 + AC-7 |
| K-2 | km / Important | AC-5 dogfood 在 Aria (无 `.aria/agents/`) 只能验 AC-3; AC-1 未绑定验证手段 | AC-5 澄清范围 (仅 AC-3) + 新增 AC-6 绑定 structural fixture 为 AC-1/2/4 载体 |
| M-1 | tech-lead / Minor | 能力受 experiment default-off 门控, 痛点未即解 | Impact + OOS 透明披露 experiment 转正是独立后续决策 |
| M-2 | tech-lead / Minor | frontmatter "畸形"边界模糊 | AC-4 收敛为可证形式 (缺/非list/parse-fail→skip; 空list→合法) |
| M-3 | km / Minor | OOS 末条只提 post_spec 白名单 | 改为"各检查点白名单内容策展" |
| M-4 | km / Minor | 输出格式 "N/N" 分母语义 | What Changes §4 输出格式行: 分母=基线+增补之和 |
