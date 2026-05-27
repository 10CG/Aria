# DEC: aria-fleet 三层架构 brainstorm (2026-05-27)

> **Type**: Brainstorm DEC (location-normalized stub, content 主体在 referenced memo)
> **Status**: ✅ **Owner-Approved 2026-05-27** (D1-D6 batch sign-off via "执行 A" 直接指令)
> **Track-ID**: `aria-fleet-strategic-pivot`
> **Implementation timing**: deferred M7+ (per D3, M6 v2.0.0 release 后)
> **Aria 规范 location**: 本文件位于 `.aria/decisions/` 满足 brainstorm DEC convention (per `/aria:brainstorm` skill 产出 location)。content 实质在 referenced memo, 本文件作 stub + index。

---

## Content (主体引用)

完整 brainstorm 内容 (含 Why / What / How / 决策框架 / 实施时机 / 跨 Spec 关系 / Memory candidates 等) 见:

→ **[`.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md`](../notes/2026-05-27-aria-fleet-three-layer-architecture.md)** (10 sections, ~330 行)

---

## Decisions snapshot (D1-D6)

| # | 决策 | 选定 |
|---|------|------|
| **D1** 命名 | `aria-fleet` (drop `aria-dashboard-hub` / `aria-hub` / `aria-atlas` 等 6 备选) |
| **D2** 架构 | 三层 (通用 / workspace / instance), 通用层禁止 10CG hardcode |
| **D3** 实施时机 | M6 ship 后 (M7+), 不阻塞 M6 主线 |
| **D4** Workspace repo | `10CG/aria-workspace` 私有 repo (workspace bundle pattern) |
| **D5** Fleet 形态 | `aria-orchestrator/extensions/aria-fleet/` Python entry-point plugin (Hermes tool pack) |
| **D6** 短期 | aria-dashboard skill 沿用 + boundary audit + memo 沉淀 |

---

## 触发对话 + Owner key insights (本 brainstorm 由 owner 主导推进)

1. **"现有飞书 bot 接的是 Hermes (not Claude), aria-hub 该是 Hermes tool pack 不是 standalone service"** — 推动 re-frame 整个 cross-project capability 设计
2. **"Aria 需要通用性, 整个架构包括底层 Hermes 一起可适配不同工作室"** — 推动三层架构 (通用 / workspace / instance) 设计
3. **"aria-orchestrator 跑起来后, 10CG.local 怎么定义独特价值?"** — 推动 workspace 累积资产 = contextualized intelligence 定义
4. **"aria-dashboard-hub 命名不准 — dashboard 只是渲染之一"** — 推动 `aria-fleet` 命名选定

---

## Alternatives considered + drop 理由

| 命名候选 | Drop 理由 |
|---------|---------|
| `aria-hub` | 太泛 |
| `aria-dashboard-hub` | 暴露实现而非本质 |
| `aria-atlas` | 全景图比喻偏抽象 |
| `aria-vantage` | 制高点比喻偏抽象 |
| `aria-cockpit` | control 含义偏强 (本设计还不是 control plane) |
| `aria-overview` | 朴素无品牌感 |

| 架构候选 | Drop 理由 |
|---------|---------|
| Standalone repo + cron + static HTML (P0~P3 原方案) | 跟 Aria 2.0 agent OS vision 不一致;未复用 Hermes 现有飞书 / 状态机 |
| aria-plugin 内新 skill `aria-multi-dashboard` | aria-plugin 是 skill 集, 不该持有项目注册表 |
| Aria 主仓 cross-project-hub/ 子目录 | Aria 主仓是方法论项目, 不应混入跨项目工具 |

| 实施时机候选 | Drop 理由 |
|------------|---------|
| 立即起 (M6 之前) | 会撞 M6 主线 in-flight (M5/M6 orchestrator core 还在改);加 tool pack 风险高 |
| M7+ (M6 ship 后) | ✅ 选定 — orchestrator core 已稳, 加 fleet tool pack 安全 |

---

## Convergence path

- 本 brainstorm 不是经 `/aria:brainstorm` formal skill 触发, 而是 **owner-driven 自由对话** 中自然涌现的设计共识
- 单轮 (无 R1-R2-R3 multi-round audit), owner 直接 batch sign-off D1-D6
- **未来 M7 启动 formal Phase A.0 brainstorm** 时, 应 trigger `/aria:brainstorm` 跑 multi-round audit (per Aria 规范),本 DEC 作 input + starting point, 不重新讨论 D1-D6 (已 Approved)

**convergence 实质**: 1 round owner direct sign-off, 类似 [[feedback_post_spec_audit_pragmatic_convergence]] 中 "unanimous + verdict 改善 + 无振荡" 的简化版 (单 round 无振荡可能)。

---

## Hard constraints (Sign-off 后约束)

- 通用层禁止新增 10CG-specific hardcode (P0 修 9 处技术债 → Sprint 1-2 backlog,见 [boundary-audit](../notes/2026-05-27-boundary-audit-10cg-hardcode.md))
- aria-orchestrator core 升级时, hub-related capability 必须 entry-point plugin 形式接入, 不允许 inline
- M7 启动 formal brainstorm 时直接引用本 DEC 作 starting point, 不重新讨论 D1-D6
- Forgejo #127 close 为 deferred-to-aria-fleet (已 close 2026-05-27T07:46:30Z, comment `#9203`)

---

## Cross-references

### 本 DEC stub 主体内容
- `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` (memo, 10 sections / ~330 行 / 完整设计)

### 平行 audit (pre-implementation 技术债清单)
- `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md` (boundary audit, 18 hardcode 信号 / 9 真技术债 / P0-P2 优先级)

### Session record
- `docs/handoff/2026-05-27-aria-fleet-strategic-pivot-session.md` (本 DEC 产生的 session)

### 决议下游影响 (referenced 关闭/降级)
- [Forgejo #127](https://forgejo.10cg.pub/10CG/Aria/issues/127) (UPM-less rendering) — closed deferred-to-aria-fleet
- [Forgejo #125](https://forgejo.10cg.pub/10CG/Aria/issues/125) (AB parser) — 仍 valid, transitions to aria-fleet 设计
- [Forgejo #126](https://forgejo.10cg.pub/10CG/Aria/issues/126) (audit frontmatter) — 仍 valid, cross-cutting

### M7 tracker
- (待 create) Forgejo issue: M7 aria-fleet implementation tracker

### 引用 PRD / US
- `docs/requirements/prd-aria-v2.md` — 当前 PRD 不含 aria-fleet (intentional defer M7 brainstorm 时 update PRD v2.1+ or v3.0)
- US-027/028 — currently free slots, 待 M7 brainstorm 时 create

### Methodology
- Aria CLAUDE.md §不可协商规则 #1 (OpenSpec) — M7 启动时需 create
- Aria CLAUDE.md §不可协商规则 #2 (十步循环不跳 Phase A) — 本 DEC 是 pre-A.0, M7 启动后从 A.0 formal brainstorm 开始
- Aria CLAUDE.md §项目状态 — 已 update 包含 aria-fleet M7+ cross-ref (commit `b7f562d`)

---

## Memory entries (本 DEC + memo 产生, 待 prune 后 add)

5 cross-cycle valuable candidates (详见 memo §9 + handoff §4):
1. `feedback_cross_cutting_capability_as_agent_tool_pack` (HIGH)
2. `feedback_three_layer_universal_workspace_instance` (HIGH)
3. `feedback_channels_as_agent_render_outputs` (HIGH)
4. `feedback_cloud_routine_blocked_by_cf_access` (MEDIUM)
5. `feedback_audit_prompt_must_require_frontmatter` (MEDIUM)

---

**Created**: 2026-05-27T~08:25Z (DEC location-normalization stub)
**Owner sign-off**: ✅ Approved 2026-05-27 (simonfishgit, "执行 A" batch directive)
**Implementation start**: TBD (M7+, post M6 v2.0.0 release)
