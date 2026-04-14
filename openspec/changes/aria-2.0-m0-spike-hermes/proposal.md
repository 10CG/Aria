# aria-2.0-m0-spike-hermes — Hermes fork vs 自研路线 Spike

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-04-14
> **Parent Story**: [US-020](../../../docs/requirements/user-stories/US-020.md)
> **Parent Spec**: [aria-2.0-m0-prerequisite](../aria-2.0-m0-prerequisite/proposal.md) (本 Spec 是 T4 的独立化)
> **Target Version**: v2.0.0-m0
> **Timebox**: 1 sprint (~52h, 硬边界 > 60h 评估, > 72h 强制终止)
> **Source**: PRD v2.0 §AD3 + Agent Team R3 投票 2:2 分歧

## Why

> **ST1 更新 (2026-04-14)**: 纸面结构分析 (见 `aria-orchestrator/spikes/hermes-route/upstream-structure.md`) 后, 原本的 "fork vs 自研" 二元选择扩展为 **三选项: Option A (fork) / Option B (自研) / Option C (Extension-only tool pack)**。Option C 是 ST1 新发现, 可能完全消除 fork 月度 rebase 成本。本 Spec 已更新裁决规则, Option C 成为首选。

PRD v2.0 AD3 (Hermes Layer 1 实现路径) 在 Agent Team R3 讨论中 **2:2 分歧**:
- **fork 路径**: 基于 `hermes-agent` v0.7+ upstream fork, 在 `internal/aria/` 扩展 Layer 1 状态机。优势: 继承 upstream 基础设施 (FTS5 memory / parameterized job 支持)。风险: 月度 rebase 工时, upstream license 变更风险。
- **自研路径**: 基于 Python 重新实现 gateway + SQLite state machine (~800-1200 LoC 估算)。优势: 完全可控, 无 upstream 依赖。风险: 工程成本 + 功能 parity。

PRD 原案给出的是 "fork 为默认" 的保守方案, 但未经量化验证。因此 Agent Team 要求 **timeboxed 1 sprint 的 Spike**, 产出 **量化数据** 而非主观评估, 由产品负责人裁决。

**为什么独立成 Spec (而非 T4 内部任务)**: Agent Team R2-R3 讨论结论 — Spike 的风险 (反转架构 AD3) 需要独立 Round-by-Round 决策记录, 独立 Spec 支持 Spike 失败时的独立归档路径。

## What

### Spike 交付物

1. **可运行原型** (`aria-orchestrator/spikes/hermes-route/`)
   - gateway stub (飞书 API 最小调用 + SQLite state 最小原型)
   - 必含 5 状态 4 转换演示: `idle → dispatched → running → awaiting_human → resumed`
   - 覆盖正常路径 + 1 个 human-in-loop

2. **Hermes 元知识 prompt v0.1** (~1K token)
   - 起草并在 Spike gateway 中实跑
   - 验证 token 预算与 prompt 格式可行性
   - 产出 `spikes/hermes-route/meta-knowledge-v0.1.md`

3. **量化指标数据**
   - **自研路径**:
     - `cloc --include-lang=Python --exclude-dir=.venv,__pycache__,migrations` 业务 Python LoC
     - 测试 LoC 单列不计入主体
     - 实测开发工时 (记录每个状态转换的实现时间)
   - **fork 路径**:
     - 单次 rebase 实测工时 (拉最新 upstream / 解冲突 / 跑测试)
     - 月度估算 = 单次 × 1.5 (固定系数, 产品负责人可上调, >×2.0 需 tech-lead co-sign)
     - `upstream_velocity` = `git log --since="6 months ago" --oneline upstream/main | wc -l ÷ 6`
   - **双路径**:
     - direct + transitive license 全表 (`license-checker --production --json` + `pip-licenses --format=json --with-system`)
     - GPL/AGPL/LGPL/Unknown 单列高亮
     - `unknown_count` 汇总行

4. **Spike Report** (`openspec/changes/aria-2.0-m0-spike-hermes/spike-report.md`)
   - 主位置: 本 Spec 目录 (交付物归属)
   - 代码路径: `aria-orchestrator/spikes/hermes-route/` (执行就近)
   - AD3 回填时以 OpenSpec 路径作为**主引用**

### 裁决规则 (硬编码, v2 含 Option C)

> **ST1 更新 (2026-04-14)**: 纸面结构分析发现 hermes-agent v0.9.0 (非 PRD 假设的 v0.7) 已有公开的 `ToolRegistry` 扩展 API, 支持外部 tool pack 无需 fork。新增 **Option C (Extension-only)** 路径。详见 [`aria-orchestrator/spikes/hermes-route/upstream-structure.md`](../../../aria-orchestrator/spikes/hermes-route/upstream-structure.md) §5。

**裁决矩阵** (按优先级从上到下):

| 优先级 | 条件 | 结论 |
|---|---|---|
| **🥇 首选** | **Option C POC 成功** (aria-tool-pack 能注册自定义 tool 到 hermes-agent 并触发 state transition, 见 ST3.5) + license 扫描无阻断 | **Option C acceptable (首选)** |
| 🥈 次选 | Option C POC 失败 或 不可行 (扩展 API 无法表达状态机需求) + fork 路径: 月度 rebase ≤ 20h × 1.5 且 license 扫描无阻断 | **Option A (fork) acceptable** |
| 🥉 兜底 | Option C + Option A 均不 acceptable + 自研路径: cloc 业务 Python LoC ≤ 1000 且开发工时 ≤ 60h | **Option B (自研) acceptable** |
| ☠️ 降级 | 三路都 fail | **R8 退出策略** (CLI-only 降级模式) |

**License 扫描触发条件** (所有路径共享):

| 触发 | 动作 |
|---|---|
| LGPL transitive > 0 | 路由人类 legal-advisor 人工研判, 不自动降级 |
| GPL/AGPL transitive > 0 或 Unknown count ≥ 1 | fork 路径自动降级; 若 Option C/B 的依赖链无此问题 → 优先 C 或 B |

**路径选型示例**:
- Option C POC 通过 + fork 也通过 → 选 Option C (首选), fork 不选 (避免 rebase 成本)
- Option C POC 通过 + fork 因 GPL 传染失败 → 选 Option C
- Option C POC 失败 + fork 月度 rebase 超 20h × 1.5 = 30h → Option A 不 acceptable → 选 Option B (自研)
- 三路都 fail → R8 退出

**产品负责人选择空间**: Go-with-Revision PR 中产品负责人可以在 acceptable 路径之间选择 (例如强制选 fork 而非 C), 但必须在 PR 中说明理由。

### 非目标

- **不是**生产级实现 — Spike 代码不会进入 M1 MVP 主干 (若选自研则提升到 `src/`, 由 US-021 承接迁移)
- **不是** Hermes 完整功能清单实现 — 仅覆盖 5 状态 4 转换的最小闭环
- **不是** 替代 AD3 正式裁决 — Spike 产出是量化输入, 裁决权归产品负责人
- **不含** 真实 GLM API 流量测试 — Spike 阶段禁止上传真实代码/issue (R2-D2.4 / R4-D10), 仅用合成 fixture

## Impact

**反转 AD3 的可能性**:
- 若 fork 路径 license 扫描发现 GPL/AGPL 传染 → fork 自动降级, 需要裁决是否选自研
- 若自研路径 LoC > 1000 或工时 > 60h → 自研降级, 必须选 fork (承担 rebase 成本)
- 若双 fail → v2.0 架构需要重大修订或 R8 退出

**与父 Spec 的耦合**:
- 本 Spec 必须先产出 Spike Report → 父 Spec T5 (AD3 回填) → 父 Spec T6 (M0 Report 引用)
- 本 Spec 归档早于父 Spec

**PRD 修订触发**:
- 如 Spike 结论与 PRD AD3 矛盾 → 提交产品负责人**二次裁决**, 若选自研则触发 PRD AD3 patch PR (走 `prd_patch_pr` 机制)

## 约束

- **工时硬边界**: ~52h 基线, > 60h 评估, > 72h 强制终止
- **时间硬边界**: 1 sprint (1 周)
- **合成 fixture**: 禁止真实采样, 模板需 ai-engineer + legal-advisor (人类) 最终签字
- **license 扫描深度**: transitive (不得仅扫 direct)
- **rebase 实测**: 必须实际执行一次 (pull / 解冲突 / 跑测试), 禁止纯 changelog 估算

## References

- PRD AD3: [prd-aria-v2.md §AD3](../../../docs/requirements/prd-aria-v2.md)
- 父 Spec: [../aria-2.0-m0-prerequisite/proposal.md](../aria-2.0-m0-prerequisite/proposal.md)
- US-020: [US-020.md](../../../docs/requirements/user-stories/US-020.md)
- Agent Team 收敛: [Round 1-4 review log](../../../.aria/decisions/2026-04-14-us020-agent-team-review.md)
