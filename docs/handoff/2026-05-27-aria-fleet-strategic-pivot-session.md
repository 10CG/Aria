---
track-id: aria-fleet-strategic-pivot
owner-container: dev-claude
phase: D.3-strategic-design
status: done
updated-at: 2026-05-27T07:50:00Z
---

# Aria — Strategic Pivot Session (2026-05-25 → 2026-05-27, ~跨 3 天)

> **Status**: ✅ Session FULLY CLOSED — 5 个产出 (v1.29.0 Phase A + dashboard dogfood + aria-fleet 战略 + boundary audit + sign-off) 全部 commit + dual push
> **Type**: Multi-arc session (短期任务 + 长期战略并行交织)
> **Duration**: ~5.5h+ 本 session 实际工作 (但跨 ~3 day-boundary,2026-05-25 ~14:30Z 起源, 2026-05-26 持续, 2026-05-27 主要执行)
> **Cycle period**: 实际有 4 个独立 cycle 并行 (见 §1)
> **Rule #9 trigger**: ✅ session > 4h + ≥ 2 cycles + 跨 2+ phases

---

## §0 入口 (新 session 优先读)

按时间倒序:

1. **本 doc** — strategic pivot session 综合 handoff
2. **战略 memo**: [`.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md`](../../.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md) — aria-fleet + 三层架构 + 10CG.local 边界 (✅ D1-D6 Approved 2026-05-27)
3. **Boundary audit**: [`.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`](../../.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md) — 18 hardcode 信号 / 9 真技术债 / P0-P2 修复优先级
4. **v1.29.0 carry-forward**: [`docs/handoff/2026-05-25-v1.29.0-flip-phase-a-approved.md`](./2026-05-25-v1.29.0-flip-phase-a-approved.md) — Phase B+C+D ship checklist (2026-06-07 D+14 hard date,还 11 天)
5. **本 session shipped Spec**: `openspec/changes/aria-submodule-gate-block-flip/` (Approved)

→ **next session priorities** (按建议顺序):
- ⭐⭐ **P0 boundary audit fixes** (Sprint 1, M6 之外的 hygiene cycle): 修 3 处 hardcoded `forgejo.10cg.pub` + CI 后端抽象
- ⭐ **v1.29.0 D+14 ship** (2026-06-07 即将到来): 见 carry-forward handoff §3
- M6 sister 推进: Spec #1 Phase B.1 启动 (cron 累积 3-day data for Spec #2)
- aria-fleet 实施 (deferred M6 ship 后, M7+)

---

## §1 本 session 完成了什么 (4 个独立 arc)

### Arc 1: v1.29.0 submodule-gate-block-flip Phase A (3.5h, 2026-05-25 起源)

| Step | 产出 | Commit |
|------|------|--------|
| A.0 | Version stake-out (v1.29.0 / v1.7.1 slot 空闲;Aria #124 verified closed) | (no file) |
| A.1 | proposal.md skeleton (Level 2, 380+ 行) | `5d00826` |
| A.2 R1 | tl PWW + qa **REVISE 2C** + cr PWW (3 agent) | (audit reports) |
| A.2 Rev1 | 2 Critical + 13 Important + 8 Minor fixed | (in commit) |
| A.2 R2 | **3/3 unanimous PASS_WITH_WARNINGS CONVERGED** (2 Critical CLOSED, 0 new) | (audit reports) |
| Spec Status | ✅ Approved | (in commit) |
| Handoff doc | `2026-05-25-v1.29.0-flip-phase-a-approved.md` 含 D+14 ship checklist | (in commit) |

Carry-forward: Phase B+C+D ship 2026-06-07 (D+14 hard date,~11 天后)。

### Arc 2: aria-dashboard 首次 Aria self-dogfood (1h, 2026-05-27 ~02:00Z)

| Step | 产出 | Commit |
|------|------|--------|
| Scout 5 数据源 | 19 Stories / 5 active + 87 archived Specs / 63-105 audits / AB fallback | (no file) |
| Python generator | `/tmp/dashboard_gen.py` (~210 LoC, 解析 + 占位符替换) | (临时, 未 commit) |
| HTML 产物 | `.aria/dashboard/index.html` (37KB / 1450 lines) | `1730884` |
| Playwright screenshot | `/tmp/dashboard.png` (1400×~2900 全页) | (临时, 未 commit) |
| 3 Forgejo issues | [#125](https://forgejo.10cg.pub/10CG/Aria/issues/125) AB parser / [#126](https://forgejo.10cg.pub/10CG/Aria/issues/126) audit frontmatter / [#127](https://forgejo.10cg.pub/10CG/Aria/issues/127) UPM-less rendering | (Forgejo only) |

Dogfood 价值: 验证 skill 可工作 + 暴露 3 个 cross-project usability issue。

### Arc 3: Strategic pivot — Routine + aria-fleet 设计 (2h+)

**起源**: 之前 session 末为 v1.29.0 ship 设了个云端 routine `trig_01TwejQFQRdXsvzLVrUc1JXJ`。Owner 问 "CF Access 保护我的 forgejo, routine 真能拉到吗?" → 实测 Anthropic 云端 git clone 拿到空骨架 (CF 在 edge 挡掉) → **安全确认 + routine 失效, disable**。

**沿展**: 由 "aria 看板视觉/排版改进" 起步, Owner 关键洞察推动 re-frame:
1. "命名: aria-fleet 比 aria-dashboard-hub 准 (dashboard 只是渲染之一)"
2. "现有飞书 bot 接的是 Hermes (not Claude), aria-hub 该是 Hermes tool pack 不是 standalone service"
3. "Aria 需要通用性 — 整个架构包括 Hermes 一起, 可适配不同工作室"
4. "aria-orchestrator 跑起来后, 10CG.local 的特有价值是什么?"

→ 产出 **三层架构** (通用 / workspace / instance) + **10CG.local 累积价值** 定义。

| 产出 | 路径 | Commit |
|------|------|--------|
| Strategic design memo | `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` (~330 行, 10 sections) | `2e90312` |
| Boundary audit | `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md` (~355 行, 18 hardcode 信号) | `2e90312` |
| §8 D1-D6 sign-off update | memo §8 (Approved 标记 + 硬约束段) | (pending commit, 见 §3) |
| Forgejo #127 close | [#127](https://forgejo.10cg.pub/10CG/Aria/issues/127) deferred-to-aria-fleet | (Forgejo only) |

### Arc 4: Audit P0 fix vs handoff 选择 + 本 doc

无 Aria context-usage tool → 退回 session signals → Rule #9 trigger 满足 → execute D (本 doc)。

---

## §2 关键决策 (Approved by owner this session)

### D1-D6 Aria-Fleet 战略决策 (memo §8)

| # | 决策 | 选定 |
|---|------|------|
| **D1 命名** | `aria-fleet` (drop "dashboard-hub" 等 6 备选) |
| **D2 架构** | 三层 (通用 / workspace / instance), 通用层 forbid 10CG hardcode |
| **D3 实施时机** | M6 ship 后 (M7+), 不阻塞 M6 主线 |
| **D4 workspace** | `10CG/aria-workspace` 私有 repo (workspace bundle pattern) |
| **D5 fleet 形态** | `aria-orchestrator/extensions/aria-fleet/` Python entry-point plugin (tool pack) |
| **D6 短期** | aria-dashboard skill 沿用 (本 session 已 dogfood) + boundary audit + memo 沉淀 |

### Sign-off 后的硬约束 (per memo §8)

- 通用层禁止新增 10CG-specific hardcode (P0 修 9 处技术债 → Sprint 1-2 backlog)
- aria-orchestrator core 升级时, hub-related capability 必须 entry-point plugin 形式, 不允许 inline
- M7 brainstorm 直接引用本 memo 作 starting point
- Forgejo #127 close 为 deferred-to-aria-fleet (已 close 2026-05-27T07:46:30Z)

### 其他小决策

- v1.29.0 Spec Level 2, 6 deliverables (A 3-place flip / B cron / C SOT bump / D main repo 1.7.1 / E decision doc / F wording sync)
- v1.29.0 §决策框架 6 trigger (A-F), default fallback 改为 (a) extend (从 (b) flip-with-risk-accept)
- 云端 routine 在 CF Access 后失效, 退化到本地日历提醒 (D+14 reminder)
- Audit prompt 应强制要求 YAML frontmatter (Forgejo #126 surface 的供给侧约束)

---

## §3 提交清单

### Final master state (after 本 doc commit)

```
[Aria 主仓]          master = (TBD) | origin TBD | github TBD
[aria-plugin]        master = 82c8abd | v1.28.0 | unchanged
[standards]          master = 4b834d0 | unchanged
[aria-orchestrator]  master = 0ce52b9 | unchanged
[refs/aria/coordination] = ?? (本 session 未 acquire Layer L claim — Spec 起草级别工作)
```

### 本 session 主仓 commits (chronological)

| Time (UTC) | SHA | Subject |
|------------|-----|---------|
| 2026-05-25 ~14:30 | `5d00826` | docs(openspec): aria-submodule-gate-block-flip Phase A Approved — Level 2 Spec + R1+R2 CONVERGED + handoff |
| 2026-05-27 ~02:10 | `1730884` | docs(dashboard): first Aria self-dogfood — aria-dashboard v1.1.0 generated |
| 2026-05-27 ~07:36 | `2e90312` | docs(aria-fleet): strategic design memo + boundary audit (M7+ scope) |
| 2026-05-27 ~07:50 | (TBD) | docs(handoff): aria-fleet strategic pivot session — 4 arcs closeout + D1-D6 sign-off memo update (本 commit) |

### Forgejo issues activity 本 session

- Created: [#125 dashboard AB parser](https://forgejo.10cg.pub/10CG/Aria/issues/125) / [#126 audit frontmatter](https://forgejo.10cg.pub/10CG/Aria/issues/126) / [#127 UPM-less rendering](https://forgejo.10cg.pub/10CG/Aria/issues/127)
- Closed: [#127](https://forgejo.10cg.pub/10CG/Aria/issues/127) (deferred-to-aria-fleet, comment `#9203`)

### Anthropic remote routine activity

- Created: `trig_01TwejQFQRdXsvzLVrUc1JXJ` (D+14 reminder for 2026-06-07)
- Manually triggered: 1 次 (CF Access 验证)
- Disabled: 2026-05-27 (CF 挡掉, routine 链路失效)
- Status: enabled=false, 不会再 fire

---

## §4 Memory candidates (本 session 反思)

| # | Candidate | Cross-cycle valuable? | Recommended action |
|---|-----------|---------------------|-------------------|
| 1 | "**Cross-cutting capability 在有 agent OS 时, 该是 tool pack 不是 standalone service**" | ✅ HIGH — universal architectural pattern | **Memorialize** as `feedback_cross_cutting_capability_as_agent_tool_pack` |
| 2 | "**通用 / workspace / instance 三层架构**" | ✅ HIGH — SaaS-style for AI-driven systems | **Memorialize** as `feedback_three_layer_universal_workspace_instance` |
| 3 | "**Channels (IM/web/CLI) 是 AI agent 的 render output, 不该单独建 bot**" | ✅ HIGH — 设计原则 | **Memorialize** as `feedback_channels_as_agent_render_outputs` |
| 4 | "**Anthropic 云端 routine + CF Access 保护的 forgejo = empty clone**" | ✅ MEDIUM — security 实证 + 跨 session 复用 | **Memorialize** as `feedback_cloud_routine_blocked_by_cf_access` |
| 5 | "Workspace 累积资产 = team's unique contextualized intelligence" | ⚠ MAYBE — universal but偏 abstract | Defer; 若 P0 fix 时再 surface, 再 memorialize |
| 6 | "Audit prompt 应强制 YAML frontmatter (per Forgejo #126)" | ✅ MEDIUM — supply-side cross-cutting | **Memorialize** as `feedback_audit_prompt_must_require_frontmatter` (with Forgejo #126 ref) |
| 7 | "Skill 跨项目 dogfood 是验证通用性的最 cheap 方式" | ⚠ universal 但有点显而易见 | Defer |

**推荐固化**: 1, 2, 3, 4, 6 共 5 个 (1-3 是战略架构, 4 是 security 实证, 6 是 cross-cutting)。

**MEMORY.md warning** (per T-Spec4 handoff 2026-05-25): **99.4% utilization, 写 memory 前需 prune**。建议:
- 先 prune (合并 / 删过期 / 压缩) — 由 next session 起步时做
- 再批量 add 这 5 个 candidates

---

## §5 Next session 入口确认

```bash
# 标准入口
/aria:state-scanner

# state-scanner Phase 1.15 handoff collector 应解析本 doc (2026-05-27 mtime 最新)
# 推荐 Path:
#   A. P0 boundary audit fixes (Sprint 1 hygiene cycle, 不撞 M6) 
#   B. v1.29.0 D+14 ship (2026-06-07, ~11 天倒计时)
#   C. M6 Spec #1 Phase B.1 启动 (其他终端可能并行)
#   D. MEMORY.md prune (前置任务 — 5 candidates 待 add 但需 prune 先)
```

### 跨 Spec coordination 预警

| 风险 | 描述 | Mitigation |
|------|------|-----------|
| **撞 M6 sister terminal** | dev-claude2 同期 ship M6 Specs (Spec #1 Phase B.1 可能启动) | next session 起 Layer L claim 前先看 `tracks_multibranch` |
| **撞 v1.29.0 ship 倒计时** | 2026-06-07 11 天后 | D+14 ship 当天的 ship checklist 在 carry-forward handoff §3 |
| **MEMORY.md 容量** | 99.4% / next-session 写 memory 前必 prune | prune 是前置任务 |

---

## §6 Carry-forward 优先级 (next session 推荐顺序)

按 ROI 排:

1. **MEMORY.md prune** (~30min) — 前置任务, blocks memory candidate 固化
2. **P0 boundary audit fixes Sprint 1** (~2-3h) — 9 处 hardcoded forgejo.10cg.pub, 不撞 M6, 通用化收益最高
3. **v1.29.0 D+14 ship 当天** (2026-06-07, ~5-6h) — hard date 不能错过
4. **M7 brainstorm 起草** (deferred, 等 M6 ship 后) — aria-fleet 实施起点
5. **aria-orchestrator README 更新** (M7 kickoff 时, batch with aria-fleet brainstorm)

---

## §7 Session 元数据

- **Session 起源**: 2026-05-25 ~14:30 UTC (前 session 由 `/state-scanner` 启动, 跨 3 个 day-boundary 持续)
- **Session 终**: 2026-05-27 ~07:50 UTC (本 doc 写完时)
- **Duration**: ~5.5h 实际工作 (跨 2026-05-25 → 26 → 27 三天 boundary, total wall-clock ~65h)
- **Mode**: 单终端 dev-claude
- **Sister terminal activity**: dev-claude2 同期 ship M6 Spec #4 release-closeout (2026-05-25 ~22:00Z, commits 00ee85b / 94d0bd1 / f8da03e / 650b70a / 3c7ad0f / 2f9c268 / 94f5d0f) — 1 race 经 git pull --rebase 解决, 无文件冲突
- **Layer L claim**: 未 acquire (本 session 仅 Spec 起草 + memo + audit, 无 source code 改动)
- **3-way SHA parity**: 每个 commit 后 verified (origin = github = local)

---

## §8 Memory entries (本 session, 待 prune 后 add)

§4 列出 5 个推荐固化候选。**Action**: next session 第一步 MEMORY.md prune (per T-Spec4 99.4% warning), 然后 batch add 5 个。

---

## Cross-references

### Session artifacts (cumulative across 2026-05-25 + 27)

- v1.29.0 Phase A Spec: `openspec/changes/aria-submodule-gate-block-flip/proposal.md` (Approved)
- v1.29.0 audit reports: `.aria/audit-reports/post_spec-R{1,2}-{tl,qa,cr}-2026-05-25-aria-submodule-gate-block-flip.md` (6 个)
- v1.29.0 carry-forward handoff: `docs/handoff/2026-05-25-v1.29.0-flip-phase-a-approved.md`
- Dashboard 产物: `.aria/dashboard/index.html`
- Strategic memo: `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md`
- Boundary audit: `.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`
- 本 doc: `docs/handoff/2026-05-27-aria-fleet-strategic-pivot-session.md`
- Forgejo issues: #125 / #126 / #127 (closed)
- Anthropic routine: `trig_01TwejQFQRdXsvzLVrUc1JXJ` (disabled)

### Parallel work (other terminals, sister session)

- T-Spec4 (dev-claude same-day 2026-05-25): `docs/handoff/2026-05-25-m6-spec4-release-closeout-approved.md` — M6 Phase A 4/4 sub-Specs COMPLETE
- M6 推进 follow-up commits (dev-claude2): `94f5d0f` Spec #1 A.3 / `2f9c268` Status frontmatter fix

### Forward (next session priorities — by ROI)

1. MEMORY.md prune (前置) → batch add §4 5 candidates
2. P0 boundary audit fixes Sprint 1 (hygiene cycle)
3. v1.29.0 D+14 ship (2026-06-07, ~11 天)
4. M7 brainstorm (deferred, M6 ship 后)

---

**Created**: 2026-05-27T07:50:00Z
**Session cumulative duration**: ~5.5h working time across 3 calendar days
**Status**: ✅ Session FULLY CLOSED — 4 arcs ship + D1-D6 Approved + audit P0 backlog + #127 closed + routine disabled + 0 actionable in-session carry-forward (all deferred to next session per §6)
**Next entry**: `/aria:state-scanner` → 本 doc surface (mtime 最新) → next session 选 §6 carry-forward Path
