# OD-M4-2: M4 underbaseline retrospective (60h → ~22-26h actual ×0.42)

> **Date**: 2026-05-09
> **Spec**: openspec/archive/2026-05-09-aria-2.0-m4-human-gate-feishu-approval
> **Trigger**: R3 TL-R3-5 (Phase B.3 audit important finding)
> **Decided by**: AI draft pending owner Phase D.2 sign-off
> **Provenance**: AI-drafted from pre_merge R5 audit data + memory `feedback_phase_a_depth_drives_b_velocity` + `feedback_paper_fix_antipattern`

---

## 现象

M4 spec 锁 60h Phase B.2 baseline (per Q8' β'); 实测 ~22-26h (×0.42, ~63% saved)。

trajectory 与 M3 反向:
- M3 OD-13 over baseline +20% (60h → 72h)
- M4 OD-M4-2 under baseline -58% (60h → 22-26h)

---

## Why baseline 高估了 (4 因素)

### 1. Trust-but-verify discovery 红利 (~25-30h saved)

M2/M3 已实现以下骨架,M4 实施时复用而非重写:
- `S7_HUMAN_GATE` state enum + transitions (M2/M3 stub,M4 actualized)
- `FeishuWebhookClient` 完整 outbound webhook + signing (M2/M3 used for ops alerts,M4 reused for human gate cards)
- `aria-layer1-reconcile.nomad.hcl` cron pattern (M3 driver,M4 加 S7 timeout 检测分支)
- `forgejo_client.py` PR/issue/comment API (M2/M3 PR creation,M4 加 list_comments + find_pr_by_head_branch)

Phase A.1 brainstorm 时未充分 audit 已有代码路径,导致 baseline 按 "ground-up" 估算。

### 2. Phase A 决策深度高 (per `feedback_phase_a_depth_drives_b_velocity`)

Q1-Q14 brainstorm 14 个问题全部锁定 + R2 SCOPE_OK_R2 4/4 + 6 段 OD lock,让 Phase B 几乎 mechanical translation:
- 无 mid-implementation 重构 (e.g. Q10 锁 Forgejo PR comment 而非 Cloudflare Tunnel,避免 alternate 路径切换成本)
- Schema migration 选 v3 additive (vs M3 OD-12 数据迁移),节省 ~4h testing 反复
- AD-M4-1~AD-M4-11 11 决策预先 lock,Phase B 无重新讨论

### 3. Audit 5-round 真跑反而省了 rework (~5h saved)

R1 36 findings → R2 SCOPE_OK_R2 70-76% reduction (8 NEW + 2 PARTIAL),无 paper-only fix → 后续 R3-R5 无大规模回滚。

OD-15 collapse 假捷径在 R2 后被 owner 显式否决 (per `feedback_owner_invoked_convergence_loop`),反而避免了"R2 后假声称 collapsed → merge → 后续 prod bug → rollback" 路径 (~5-10h potential rework saved)。

### 4. Schema migration v3 选 additive-only (~2-4h saved)

vs M3 OD-12 数据迁移:
- 7 cols ADD + 2 fail_reason values + UNIQUE INDEX,全 additive
- 无 ALTER COLUMN / DROP COLUMN (SQLite 限制)
- 无回填脚本 (新 cols 用 DEFAULT)
- atomic migration 单 transaction

per BA-2 R2 fix `_strip_sql_line_comments` 后 per-statement execute 模式稳定。

---

## How to apply (M5 spec drafter)

### 1. **M5 baseline 不可直接套用 M4 ×0.42 ratio**

M5 范围 (Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable, ~120h baseline per PRD §409) 与 M4 不同维度:
- Replay framework 是 ground-up (无 M2/M3 骨架),trust-but-verify 红利不存在
- Review loop trinary 涉及 state machine 重构 (M5 引入 `changes_requested` enum,per `human_decision_first_decision_wins` abi_compat promise)
- 审计日志 immutable 涉及新表 + retention policy

大概率 over baseline (类似 M3 OD-13 模式)。

### 2. **M5 brainstorm Q0** 必须先 audit 现有代码

per Trust-but-verify lesson:
- Q0a: M5 哪些功能已有 M2-M4 骨架?
- Q0b: 哪些是 ground-up?
- Q0c: 锁 baseline 时分别估算两类 effort,避免 M4-style underestimate of existing skeleton work。

### 3. **abi_compat_promises 4 forward-binding** 已锁

`m4-handoff.yaml::abi_compat_promises` 4 promises 已锁,M5 不得违反 (validate-m5-handoff.py 强制 cross-reference per AD-M4-10):
1. `risk_tier_stub_to_risk_tier` — M5 ADD COLUMN 不 RENAME 不 DROP
2. `forgejo_approval_comment_id_unique_index` — preserve UNIQUE INDEX partial WHERE NOT NULL
3. `comment_poll_cadence_independent` — 30s + 30min 不合并
4. `human_decision_first_decision_wins` — review-loop 用新 enum 不允许 multi-write

### 4. **5-round audit 收敛是 M3+ 默认范式**

per `feedback_audit_convergence_pattern`:
- R1 discovery (大量 findings)
- R2 fix-verify (70%+ reduction)
- R3+ stability/strict (owner-invoked,not collapsed)
- R_N == R_{N-1} (严格收敛)

M5 spec drafter 在 effort estimate 时应分配 ~5h B.3 audit (M4 实测一致),不缩水。

---

## Ratio 历史 trajectory (3 milestones)

| Milestone | Spec baseline (h) | Actual (h) | Δ Ratio | 方向 | OD reference |
|-----------|-------------------|-----------|---------|------|--------------|
| M2 | 156 | ~150 | 0.96 | ≈ baseline | OD-8=a (156h 新基线) |
| M3 | 60 | 72 | 1.20 | over | OD-13 (M3 carryover scope expansion) |
| **M4** | **60** | **22-26** | **0.42** | **under** | **OD-M4-2 (本 retrospective)** |
| M5 | 120 (PRD §409) | TBD | TBD | TBD | (M5 brainstorm Q0 lock) |

avg ratio (M2-M4) = (0.96 + 1.20 + 0.42) / 3 = **~0.86** — 但分散度高 (σ ≈ 0.32),baseline 单点估算可信度低,建议 M5 用 PERT 三点估算 (optimistic / likely / pessimistic)。

---

## Owner sign-off

- [ ] Owner 已审阅本 retrospective (date: ____________)
- [ ] OD-M4-2 锁定 (M4 spec archived 2026-05-09, this decision is post-hoc retrospective)
- [ ] m4-handoff.yaml::effort.actual_phase_b_2_hours 实际值确认 (期望区间: 22-26h)
- [ ] m4-handoff.yaml::effort.od_m4_1_triggered = false (under baseline,未触发)
- [ ] M5 brainstorm Q0 已 plan to acknowledge 本 retrospective + abi_compat_promises 4 forward-binding

---

## Co-references

- `feedback_phase_a_depth_drives_b_velocity` (Phase A 深度 → B velocity 实证)
- `feedback_paper_fix_antipattern` (R 轮 fix 三位一体)
- `feedback_spec_frontmatter_reflects_reality` (frontmatter reality drift TL-R3-1)
- `feedback_owner_invoked_convergence_loop` (R5 真跑 vs OD-15 collapse)
- `feedback_audit_convergence_pattern` (R_N == R_{N-1} 收敛)
- `project_us024_m4_closeout_2026-05-09` (M4 closeout context)
- `aria-orchestrator/docs/m4-handoff.yaml::effort` (实测数据 anchor)
- `aria-orchestrator/docs/architecture-decisions.md` AD-M4-1~AD-M4-11

---

**Status**: AI-drafted, pending owner Phase D.2 sign-off
**Maintainer**: AI (draft) + Owner (sign-off)
