---
id: R2-CLOSEOUT
title: US-023 brainstorm R2 verify 综合 — Phase A.1 Spec drafting input
date: 2026-05-03
status: closed
relates_to: OD-12 RESOLVED, US-023 Approved Pending baseline lock, Phase A.1 next
---

# R2 Closeout — Phase A.1 Drafting Readiness

## 触发

OD-12 RESOLVED 2026-05-03 evening (commit 127605c). R2 4-agent parallel verify (backend-architect / qa-engineer / tech-lead / ai-engineer) 验证 OD-12 输入是否充分支持 Phase A.1 Spec drafting。

## R2 综合 verdict

**4/4 READY_FOR_R3** — 不直接 PHASE_A1 (因为 R2 出新 findings 需 Spec tasks 内 explicit), 不 BLOCK_NEED_OWNER (因为 0 critical 需要 owner reopen OD-12)。

按 Aria 规范 (`feedback_pre_merge_4round_convergence_template` proportionality), R2 全 READY 时 R3 是 stability 冗余轮, 直接进 Phase A.1 把 R2 findings explicit map 到 Spec tasks 即可。

## R2 综合 findings

### 3 Critical (Phase A.1 必须 explicit)

| ID | 来源 | finding | Spec 落地 |
|---|---|---|---|
| C1 | ai R2 OBJ-R2-AI-1 | `token_tracking.compute_cost` 必须 provider-aware branch (Luxeno=0 / Zhipu metered) | T10 task spec 改 signature `compute_cost(provider, model, in, out)`; m3-handoff.yaml 加 `luxeno_subscription_baseline_usd_monthly` + `zhipu_metered_usd_total` 两 field |
| C2 | qa R2 NEW-OBJ-1 | Crash recovery test harness 缺 — acceptance C 没 Tier-1 test design | T12 task spec 加 named test `test_t12_crash_recovery_s5_await_auto_resume` (5 步: pre-seed → fresh extension → tick → assert _handle_s5_await fired → assert state advances) |
| C3 | qa R2 NEW-OBJ-2 | `NomadAllocHTTPProvider` (production AllocStatusProvider) 缺失, S5_AWAIT 在 production 无 alloc_provider | T2 task spec 改: 不只 alloc_provider HTTP class, 也含 tick_runner.py lazy-wire 注入路径 (ARIA_LAZY_WIRE=1 时 self._alloc_provider = NomadAllocHTTPProvider()) |

### 8 Important (Phase A.1 task line items)

| ID | 来源 | finding | 处理 |
|---|---|---|---|
| I1 | backend BA-3 | HCL meta key inventory + IMAGE_SHA pin 未定义 | T1 + T5 sub-task: 显式 enumerate Nomad meta keys + 选择 sha digest vs mutable tag (需 owner decide via Phase A.2) |
| I2 | backend BA-6 / R2-TL-Q3 | S5_AWAIT crash recovery scope (仅 S5 还是含其他 states) | T7 spec text: M3 仅 S5_AWAIT (Nomad-controlled); 其他 5 states 中断由 reconciler 处理 stuck >60min → S_FAIL; 推 M4/M5 (owner advisory in Phase A.2) |
| I3 | backend BA-8 / ai OBJ-8 | S2/S3 token tracking wiring 缺 (M2 仅 S6 wired) | T10 task spec 加 sub-task: extend `repo.update_token_usage` 到 _handle_s2_decide + _handle_s3_build_cmd (per usage_from_silknode_response pattern) + 1 unit test 验 cumulative=S2+S3+S6 |
| I4 | backend R2-2 | fallback_chain_json schema migration transform 时机 (read-time vs write-time) | T3 task spec: write-time exhaustive transform (一次性 UPDATE all v1 string-array → v2 dict-array, 同 ALTER 一 transaction), read-time 不 backward compat (新 schema_version=2.0 lock) |
| I5 | backend R2-3 / ai OBJ-4 | CAS double-recovery race (cron + reconciler 同 row 同 ts) | T5 task spec: WHERE clause 加 `attempt_count` (compound 版本字段, 比 last_heartbeat_at 单独更鲁棒) |
| I6 | tech R2-1 | PRD §M3 'dual provider' 字面 → Q1=D' divergence | Phase A.1 第一动作 PRD §M3 patch (5 patches 详见下) |
| I7 | tech R2-3 | OD-13 应 Phase A.3 立, 不等 mid-sprint | Phase A.3 加 task: OD-13 PRD §M3 工时 90→185 patch (justification = OD-12 §Q2) |
| I8 | qa NEW-OBJ-3 | ProviderRouter test matrix undefined | T9 task spec: parameterized test matrix (3 state × 5 fallback path × 6 dict field assertion) ≥ 12 cases |
| I9 | qa NEW-OBJ-5 | Reconciler CAS contention test gap | T12 task spec: concurrent tick + reconciler 测试 (BEGIN IMMEDIATE 序列化 + lost-update 检测) |
| I10 | tech R2-2 | Q6=A weakness vs C — Phase D sign-off gate weak | T15 spec stretch: ≥10 cycle 同时 Tier-1 fake + Tier-2 deployed 实链 (扩 T15 至 ~12-14h) |

### 6 Minor (Spec optional 提升点, 可 deferred 实施期 sister-bug)

| ID | 来源 | finding | 处理 |
|---|---|---|---|
| M1 | ai OBJ-R2-AI-5 | fallback_chain_json M2/M1 旧数据 backward read | I4 已含 (write-time exhaustive transform, 不需 backward read) |
| M2 | tech R2-TL-5 | Reconciler Feishu 与 S7 webhook 复用 | T6 sub-task: `FEISHU_OPS_ALERT_WEBHOOK` env 可选; fallback to `FEISHU_NOTIFY_WEBHOOK` + warning |
| M3 | tech R2-TL-6 | provider_cost_model NULL backfill | T3 migration script 加 backfill rule: 历史 row `provider_cost_model = 'subscription_flat'` (Luxeno-only AD-M1-12) |
| M4 | tech R2-TL-7 | SQLite busy_timeout for CAS | T5 sub-task: `PRAGMA busy_timeout=5000`; CAS 失败 retry 1 次 (race lost = let cron win) |
| M5 | qa NEW-OBJ-6 | `cycle_start_ts` 历史 row 默认 NULL → acceptance B p50 query 在 ≥10 post-migration 后才有意义 | T3 migration script 加 backfill rule: 历史 S9_CLOSE/S_FAIL row `cycle_start_ts = state_entered_at` (近似估计, 显式注 placeholder) |
| M6 | qa OBJ-11 | M1 validator path Nomad Variable 绑定 | T11 sub-task: `M1_VALIDATOR_PATH` 加入 aria-orchestrator HCL Nomad Variable, 容器内 bind mount |

### 3 Owner-decide (Phase A.2 advisory)

| ID | 来源 | question | 推荐 default |
|---|---|---|---|
| OD-3a | backend BA-OQ-3 | HCL image pinning: sha digest (immutable) vs mutable tag (rolling)? | sha digest pin (per AD-M1-7 reproducibility) |
| OD-3b | backend R2-TL-Q3 / qa OQ-M3-2 | Crash recovery scope: 仅 S5_AWAIT 还是含其他 5 states? | 仅 S5_AWAIT (Nomad-controlled), 其他状态 reconciler stuck>60min 处理, M4/M5 拓展 |
| OD-3c | qa OQ-M3-1 | NomadAllocHTTPProvider 注入路径: __init__ default lazy attribute vs ARIA_LAZY_WIRE 显式注入? | ARIA_LAZY_WIRE=1 显式注入 (per ForgejoCliClient + NomadDispatchClientHTTP pattern) |

### PRD patches needed (Phase A.1 起首动作, per tech-lead R2 5 patches)

1. PRD §M3 工时 90h → 185h (justification = OD-12 §Q2 scope discovery, M2 mode 校准 ×2.06 inflation; via OD-13 in Phase A.3)
2. PRD §M3 'dual provider' 字面 → 'multi-model GLM routing + cross-provider HA fallback' (Luxeno primary + Zhipu fallback per AD-M1-12 supersedes; OD-12 §Q1=D' reference)
3. PRD §M3 验收 A 'cluster smoke gate' 字面 (若有) → 'Tier-1 自动化集成 + carryover #1 cluster verification embedded' (Q6=A reference)
4. PRD §M3 验收 B p50 baseline 'M1 ×1.5' → 'M1 demo_002 p50_s × 1.5 = 47.25s, S1_SCAN→S9_CLOSE wall + fallback_triggered=false filter' (Q7=C reference)
5. PRD §M3 验收 D/E/F 显式化 (D: cycle-close p50 / E: schema migration zero loss / F: secret rotation 后 benchmark validation)

## R2 各 agent verdict 详细

| Agent | Verdict | R1 closure rate | New R2 findings | Owner-decide raised |
|---|---|---|---|---|
| backend-architect | READY_FOR_R3 | 5/8 closed (3 still_blocking: BA-3 / BA-6 / BA-8) | 5 (2 blocking_phase_a1) | 1 (BA-OQ-3 HCL pinning) |
| qa-engineer | READY_FOR_R3 | 7/11 closed (4 still_open critical/important: OBJ-3 / OBJ-8 / OBJ-9 / OBJ-10) | 6 (3 critical) | 6 questions Phase A.1 advisory |
| tech-lead | READY_FOR_R3 | 8/8 RESOLVED/DISSOLVED/ACCEPTED (residual risks 全 documented) | 7 (3 important PRD patches) | 1 (R2-TL-Q3 crash recovery scope) |
| ai-engineer | READY_FOR_R3 | 4 RESOLVED + 2 DISSOLVED + 2 PARTIAL + 2 STILL_OPEN | 5 (1 critical _PRICING) | 1 (Q-A1 timeout policy) |

## Phase A.1 Spec drafting 准备清单

下 session 入口 (Phase A.1 Spec drafting):

1. ✅ OD-12 RESOLVED (`.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`)
2. ✅ R2 closeout memo (本文件)
3. ✅ US-023.md scope 已 reframe (commit 127605c)
4. ⏳ **PRD §M3 patch** (5 patches) — Phase A.1.0 第一动作
5. ⏳ Spec dir 创建: `openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/`
6. ⏳ Spec proposal.md drafting (~6h, 含 What/Why/Acceptance/Out of Scope/Risk/AD-M3 placeholder)
7. ⏳ Spec tasks.md drafting (~5h, 17 task groups T0-T16, 每 group 含 R2 findings 具体子任务)
8. ⏳ Spec patches/01-PRD-M3.md / 02-AD-M1-12-续延.md / 03-...-M3.md (~2h)
9. ⏳ Phase A.2 post_spec audit (4-round) — 验证 R2 critical/important 全在 Spec 内
10. ⏳ Phase A.3 OD-12 baseline lock + OD-13 PRD patch + Status: Draft → Approved
11. ⏳ Phase B.1 feature branch `feature/aria-2.0-m3-cycle-close-glm-routing-recovery`
12. ⏳ Phase B.2 实施 (~5-6 weeks)

## 不影响

- M2 closeout 已完成 (Spec archived, signoffs filled)
- T7.5/T7.6 cluster smoke 已 PASS
- 268 unit tests baseline
- US-023.md scope (commit 127605c) 已与 OD-12 一致

## 引用

- OD-12: `.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- US-023: `docs/requirements/user-stories/US-023.md`
- M2 closeout memory: `project_aria_m2_closeout_2026-05-03.md`
- R1 transcripts (本 session 上半段): backend-architect / qa-engineer / tech-lead / ai-engineer
- R2 transcripts (本 session 下半段, 4 task IDs in `/tmp/claude-1000/-home-dev-Aria/.../tasks/`)
- Aria 规范 `feedback_pre_merge_4round_convergence_template`: R3 stability 在 R2 全 READY 时可 skip
