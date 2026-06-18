# Design Memo: aria-fleet MVP — 跨项目状态只读聚合 tool pack (M7)

> **Type**: Strategic design memo (非 OpenSpec / 非 DEC — 封存 fleet 整体 MVP scoping brainstorm 收敛, 供 M6 ship 后起 M7 OpenSpec 作 starting point)
> **日期**: 2026-06-18
> **来源**: owner "M7 aria-fleet brainstorm" → "先 1 再 2" 第二轮 (fleet 整体 MVP scoping)
> **Status**: MVP 第一刀 + 取数模型已确认; 实施时机 M7 (M6 ship 后); planning sediment, 未立项
> **Predecessors**:
>   - `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` (D1-D6 Approved — 命名/三层/时机/D5 tool pack 形态)
>   - `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md` (9 处 hardcode; **P0 已 ship**, 见 §1 recon)
>   - `.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md` (fleet 另一子能力: agent 生命周期管理, 本 session 第一轮)
>   - Forgejo Aria #128 (M7 aria-fleet tracker, US-027)
> **Owner sign-off**: ✅ 本轮逐项确认 (fleet 第一刀=选项 1 / 取数=①读+②刷新③推迟) (2026-06-18 session)
> **Audit discipline**: 设计备忘录, 未走 post_brainstorm audit; 正式审计留 M7 OpenSpec 立项时

---

## §0 一句话

aria-fleet 整体 MVP = 把各 10CG 项目已有的 `state-snapshot.json` **跨项目聚合**成只读"指挥塔", 让 Hermes 能回答"哪个项目卡了"。这是 fleet 的**核心 essence 第一刀**, 区别于本 session 第一轮设计的 agent-生命周期管理 (fleet 的另一子能力)。

---

## §1 Recon (动手前核实, 改变了候选)

- **boundary audit (2026-05-27) 的两个 P0 已 ship** (核实代码确认):
  - C1-C3 Forgejo hosts → `ARIA_FORGEJO_HOSTS env > config > legacy` (v1.30.0 forgejo-hosts-parameterization)
  - C5-C6 CI 后端 → `ci_backends/` 包 (`CIBackend` ABC + aether + github_actions stub) (v1.31.0 ci-backend-abstraction)
  - → **候选「boundary-audit hardcode 修复排序」基本作废**; 只剩 orchestrator 侧零碎 (C7 standards repo / C8-C9 inject-demo 路径 / Feishu 通知抽象), L2 内部、低优。
- **单项目 dashboard 已 dogfood** (2026-05-27, `aria-dashboard` skill v1.1.0)。
- **state-scanner 每项目机械产出** `.aria/state-snapshot.json` = 聚合的天然原料 (零新采集基建)。
- 缺的只是: **跨项目聚合** + 一份"看哪些项目"的清单。

---

## §2 fleet MVP 第一刀 = 跨项目状态只读聚合 (依赖最小的 essence)

owner 在三候选 (聚合 tool pack / workspace repo 地基先行 / 多 channel 渲染先) 中选**聚合 tool pack**:
- workspace repo 整建 = 给还没设计的 fleet 功能预搭结构 = 偏早; 聚合只需其**一小片** (projects.yaml)。
- 多 channel 渲染先 = 无聚合层则无内容可渲染 = 偏早。
- 聚合 tool pack = 上来就有用, 复用现成快照, 依赖最小。

---

## §3 MVP 具体构成

| 件 | 内容 | 复用/新建 |
|----|------|------|
| **projects.yaml** | 极简项目清单 `{name, path/repo, branch}` (= workspace repo 那一小片) | 新 (5-20 行) |
| **快照获取** | 见 §4 取数模型 | 复用 state-scanner 产物 |
| **健康/卡点推导** | 每项目把丰富快照**降维**成 `{phase, health: ok/warn/blocked, blockers[], snapshot_age}` | 复用快照字段 |
| **tool pack 接口** (Hermes 可调) | `fleet_status()` 全项目一行健康 / `fleet_project(name)` 钻取 / `fleet_blocked()` 只看 warn+blocked | 新 (D5: `aria-orchestrator/extensions/aria-fleet/`) |
| **输出** | 结构化数据 + 默认文本渲染; channel (飞书卡片/CLI/dashboard) 由 Hermes 决定渲染 | 复用 (memory `feedback_channels_as_agent_render_outputs`) |

**读取范围**: 只读聚合, **不做跨项目动作** (推迟)。

### 健康/卡点推导信号 (从快照现成字段)

`blocked` / `warn` 候选信号 (M7 细化阈值):
- `custom_checks` 有 `fail` (severity)
- `interrupt.status != none` (在飞中断)
- `openspec.design_deferred[]` 非空 (设计未实施)
- `sync_status` behind-remote / parity 不齐
- `handoff` 陈旧 (age 高) 且带 carry-forward
- `openspec.pending_archive` 非空 (待归档堆积)
- `audit.last_audit.verdict == FAIL`

---

## §4 取数模型 (唯一架构决策) — ①读 + ②刷新, ③推迟

不冲突、正好组合 = "读缓存 + 必要时刷新":

| # | 模型 | 角色 | 状态 |
|---|------|------|------|
| ① | **读现有快照 + 显示 age** | 默认快路径 | ✅ MVP |
| ② | **陈旧超阈值 (如 >24h 可配) 或 owner 要求 → 跑 scan.py 刷新该项目** | 刷新动作 | ✅ MVP |
| ③ | **项目 scan 时推送到 durable volume / workspace repo, fleet 读汇总** | 跨主机/项目增多时的解耦 | ⏸️ 推迟 |

**caveat (仍算只读聚合)**: ② 的 re-scan 技术上重写快照文件, 但 `scan.py` **幂等安全** — 只从当前状态重生成**派生**快照, **不碰项目代码、不动 git** → 不破坏"只读聚合"本质 (fleet 从不改项目本体)。
**caveat (范围)**: ①② 都要求项目 checkout 在 Hermes host 上; 没 checkout 的项目两者都拿不到 → 正是未来 ③ 解决的。MVP 假设项目都在 host 上有 checkout。

---

## §5 三层映射 (套进 2026-05-27 L1/L2/L3)

| 层 | fleet MVP 放什么 |
|----|------|
| **L1 通用** | fleet tool pack 框架 (聚合引擎 + 健康推导 + 接口 schema + 取数模型); 复用 state-scanner。零 10CG hardcode |
| **L2 workspace (10CG)** | `projects.yaml` (10CG 监管的项目清单) + 刷新阈值/集成配置 (Forgejo/host 路径) |
| **L3 instance (项目)** | 各项目 `.aria/state-snapshot.json` (已有) + checkout |

---

## §6 复用 vs 新建

- **复用**: state-scanner `scan.py` + snapshot schema (取数核心原料); aria-dashboard 渲染思路 (单→多项目); channels-as-render-outputs 哲学。
- **新建**: `projects.yaml` schema + 聚合引擎 + 健康/卡点降维 + tool pack 接口 (`fleet_status/project/blocked`) + 刷新-on-stale 逻辑。

---

## §7 M7+ 推迟项

- 跨项目**动作** (不只读: 触发某项目 scan/ship/审批) — MVP 只读
- **完整 workspace repo** (integrations/playbooks/branding/artifacts) — MVP 只要 projects.yaml 一小片
- **③ 推送到中央库** — 跨主机/项目增多时
- **多 channel 富渲染** (飞书富卡片/实时 dashboard) — MVP 结构化数据 + 默认文本即可
- **历史趋势/risk register** (跨时间聚合) — 后话

---

## §8 开放问题 (M7 立项时回答)

1. **健康/卡点阈值标定**: 哪些信号算 `blocked` vs `warn`, 各阈值 (handoff age / snapshot age / behind count)。
2. **刷新触发策略**: 自动刷 vs 仅提示; 24h 阈值是否合适; 是否默认不自动重跑 (避免 N×scan 延迟)。
3. **projects.yaml 来源**: 手维护 vs 从 host 上 checkout 自动发现 vs 从 Forgejo org 拉取项目列表。
4. **Hermes tool pack 接入**: 复用 AD3 entry-point plugin POC; 接口契约与 Layer 1 元知识 (AD7) 的边界。
5. **跨 plugin 版本**: 各项目 snapshot_schema_version 可能不一致, 聚合需容版本漂移 (additive schema 已部分缓解)。

---

## §9 Cross-references

- 三层架构 (D1-D6): `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md`
- boundary audit (P0 已 ship): `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`
- agent 生命周期 (fleet 另一子能力): `.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md`
- M7 tracker: Forgejo Aria #128 (US-027)
- 现成 Skill/产物: `aria/skills/state-scanner/scripts/scan.py` (snapshot) + `aria/skills/aria-dashboard/` (渲染)
- 相关 memory: `feedback_channels_as_agent_render_outputs` / `feedback_cross_cutting_capability_as_agent_tool_pack` / `feedback_three_layer_universal_workspace_instance` / `feedback_cloud_routine_blocked_by_cf_access` / `feedback_periodic_job_acceptance_data_on_durable_volume`

---

**Created**: 2026-06-18
**Author**: AI (Claude Opus 4.8 1M context) via owner-driven brainstorm
**Status**: fleet MVP scoping 已封存; 实施待 M6 ship 后 M7 OpenSpec 立项
**Next**: M6 ship 后据本 memo + agent-lifecycle memo 起 M7 OpenSpec (fleet 多子能力分阶段)
