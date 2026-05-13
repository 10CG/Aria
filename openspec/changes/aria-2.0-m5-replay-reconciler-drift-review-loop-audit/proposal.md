# Aria 2.0 M5 — Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable

> **Level**: 3 (Full — 跨多 module + 架构变更 + schema migration + abi_compat 约束)
> **Status**: **Approved** (Phase A.2 post_spec audit R1+R2 SCOPE_OK_R2 4/4, R2 92.3% reduction; R3+ collapsed per Aria-default convergence — non-owner-invoked, R2 critical 11/11 closed + 0 new critical)
> **Change ID**: `aria-2.0-m5-replay-reconciler-drift-review-loop-audit`
> **Parent US**: [US-025](../../../docs/requirements/user-stories/US-025.md)
> **Parent PRD**: [prd-aria-v2.md §M5](../../../docs/requirements/prd-aria-v2.md) (Week 20-25, 120h baseline)
> **Predecessor Spec**: [aria-2.0-m4-human-gate-feishu-approval](../../archive/2026-05-09-aria-2.0-m4-human-gate-feishu-approval/proposal.md) (M4 archived 2026-05-09)
> **Brainstorm Source**: [.aria/decisions/2026-05-10-us025-m5-brainstorm.md](../../../.aria/decisions/2026-05-10-us025-m5-brainstorm.md) (10 个 Q 全部锁定)
> **Effort baseline**: 138h (R2-cleanup reconcile per TL-R2-1/4: feature 113-118h + Phase 6 实际 18h subtask sum); OD-M5-1 trigger raised to 165h (= 138 × 1.20, R2-cleanup TL-R2-2 raise from 156h for 6.5% pessimistic cushion)
> **abi_compat hard constraints**: 4 forward-binding promises from m4-handoff.yaml (validate-m5-handoff.py enforced)
> **Audit trajectory**:
>   - Phase A.2 R1 (2026-05-10): NEEDS_FIX (65 findings: 11C + 34I + 14m + 6o); R1 report `.aria/audit-reports/post_spec-R1-2026-05-10T1506Z-aria-2.0-m5.md`
>   - Phase A.2 R2 (2026-05-12): SCOPE_OK_R2 4/4 (92.3% reduction; 0 new critical, 1 new important closed inline as polish); R2 report `.aria/audit-reports/post_spec-R2-2026-05-12T2351Z-aria-2.0-m5.md`
>   - R2-cleanup (2026-05-13): 14 minor/observation polish 应用 (TL-R2-1/2/3/4 + BA-R2-1/2/3/4 + QA-R2-1/2/3 + AI-R2-1/2/3 + QA-R2-2 important security)
>   - R3+ collapsed: per Aria-default convergence (owner 未显式 invoke deep R3 stability per `feedback_owner_invoked_convergence_loop`); R1 critical 100% closed + R2 vote unanimity sufficient for Phase A.3 entry

---

## Why

M4 (US-024) 完成后, Aria 2.0 在 production 已能跑通 "AI dispatch → Layer 2 容器 → PR → owner approve → S8_MERGE" 完整流程
(Track A T-deploy 2026-05-09 实证, smoke S7→S8 verified)。M5 是从 "能跑通" 升级到 "能信任 + 能自我管理":

1. **看历史 (Replay)** — owner 任意时点能回看某 dispatch 的完整决策链 (state 转换 + LLM 调用 + human decision + rework cycle), 解决 "AI 当时为什么这样判" 的疑问
2. **救故障 (Failure analysis)** — dispatch 失败时, LLM 自动分析失败原因 + 给 owner 智能建议 (retry / abort / 重写 issue), 解决 M4 historical 13 条 S_FAIL 都没后续的痛点
3. **保规范 (Drift defense)** — AI 写代码不能跑偏: commit message 必须符合 Conventional Commits + Aria 规范, 实施必须符合 OpenSpec proposal (drift score 阈值警告)
4. **改稿 + 重做 (Review loop)** — 看 PR 后 owner 不只能 approve/reject, 还能 `/aria changes:` 改稿 (同 PR force-push) 或 `/aria redo:` 重做 (新 PR), per-rework 自由选模式
5. **可审计 (Audit log immutable)** — 所有事件 immutable 写入 SQLite 新表, replay + drift detection + failure analysis 都基于这份事实
6. **Schema 占位 (Risk-tier dual-write)** — 满足 abi_compat #1 强制, 为 M6 真实 risk classification 铺路 (M5 只 schema, 算法推 M6)
7. **SLO 优化 (cron cadence)** — Track A T-deploy 发现: cron 1h cadence 让 owner approve 后等最长 1h 才合 PR, PRD §618 SLO < 10min 不达标。改 comment-poll direct transition, S7→S8 < 60s

**核心驱动力**: M4 已验证 "可跑", M5 验证 "可控 + 可观察 + 可演进"。M6 "v2.0 文档 + release" 之前必须把这层做扎实。

---

## What

### In scope (M5 must deliver, ~113-118h)

#### A. Replay framework — Deterministic state replay (10h)
- `aria_layer1/replay.py` 提供 `replay(dispatch_id) -> markdown` 接口
- Output 含: state 转换时间线 + LLM 调用 metadata + human decisions + rework chain + failure_analysis 输出 + drift detection 结果
- **不重跑 LLM** (deterministic state replay only); LLM stub replay + diff testing 推 M6

#### B. Reconciler 深度增强 — Failure analysis + smart retry (15h)
- dispatch 进入 S_FAIL 时, reconciler 跑 LLM 分析 (input: fail_reason + last 5 audit events; output: action + reason + suggested_owner_action)
- **retry**: 自动 re-dispatch (仅当 fail_reason in {'infrastructure', 'timeout'} + retry_count < 1 + LLM confidence > 0.7)
- **abort**: 写明确 final reason
- **notify_owner**: Feishu reject 卡片含 LLM 诊断 + 建议
- LLM model: glm-4.5-air, fallback glm-5-turbo (per M3 ProviderRouter 链)

#### C. Drift defense — Commit lint + Spec diff (12h)
- **Commit lint** (~5h): regex/parser 验证 Conventional Commits + Aria 规范 (type prefix / scope / title ≤ 70 / Closes #N)
  - 不通过 → Layer 2 dispatcher 拒绝该 commit, force AI 重写
- **Spec diff** (~7h): dispatch 完成后, LLM 比较 proposal.md vs PR diff
  - 输出: `{compliance_score: 0-100, deviations: [...], extra_changes: [...]}`
  - score < 70 → Feishu 警告卡片 "Spec drift detected, owner 检视"
- LLM model: glm-4.5-air, ~¥1-3/月

#### D. Review loop — 双模式 hybrid (50-55h)
- Comment 协议扩展: `/aria approve` / `/aria reject:` / `/aria changes:` / `/aria redo:` 4 commands
- **改稿模式 (`/aria changes:`)** — 新 dispatch row, Layer 2 prompt = 原代码 diff + feedback, force-push 同 branch, ~50% LLM cost
- **重做模式 (`/aria redo:`)** — 新 dispatch row, Layer 2 prompt = 原 issue + feedback, 新 PR + 旧 PR auto-close + comment "Superseded by #<new>", ~100% LLM cost
- **rework_round cap = 3** (合并 cap, 不区分模式), nomadVar `ARIA_REWORK_MAX_ROUND=3` 可调
- Feishu 卡片显示当前 round + mode (e.g. "rework round 2/3 — changes mode")
- abi_compat #4 first-decision-wins 保持: 每 round 创建 NEW dispatch row, 同 row human_decision 一次性写入

#### E. 审计日志 — SQLite immutable 新表 (15h)
- Schema migration v3 → v4: 新表 `dispatch_audit_log` (id / dispatch_id / ts / event_type / payload_json) + INSERT-only triggers
- 8 event types: `state_transition` / `llm_call` / `human_decision` / `rework_cycle` / `failure_analysis` / `risk_tier_classified` / `spec_drift_detected` / `commit_lint_result`
- db.py helpers: `append_audit_event` / `query_audit_log`
- DB triggers: BEFORE UPDATE/DELETE → RAISE(ABORT, 'audit log immutable')

#### F. Risk-tier — schema dual-write only (5h, algo 推 M6)
- Schema migration: ALTER TABLE dispatches ADD COLUMN risk_tier TEXT (不 RENAME / 不 DROP risk_tier_stub)
- db.py helper: `get_risk_tier(dispatch_id)` (prefer risk_tier WHERE NOT NULL else fallback risk_tier_stub)
- M5 写入路径: risk_tier=NULL, risk_tier_stub='always' (M4 行为不变)
- validate-m5-handoff.py::check_risk_tier_migration_acknowledged 通过

#### G. cron cadence — comment-poll direct transition (6h)
- comment_poll.py 在 update_human_decision (CAS) 成功后, **直接调** `extension._handle_s7_human_gate(dispatch_id)`
- 不再依赖 aria-layer1-cron 推进 S7→S8
- 兜底: reconciler 30min cron 仍保留 (扫 stuck S7 — comment-poll 进程崩溃时)
- AD-M5-1 文档化此 reframe (M4 AD-M4-9 § 决策 #4 → M5 superseded)

### Out of scope (推 M6+)

| ID | Description | 原因 |
|----|-------------|------|
| H | aria-layer2-runner deploy | M2/M3 era infra gap, 与 M5 features 异质,与 features 同 milestone 增加 context switching |
| F.algo | Risk-tier 真实 classification 算法 | Owner question 了分级价值; M6 真有清晰 use case 时再做 |
| A.advanced | LLM stub replay + Differential testing | M5 state-only 够用; 改 prompt 后跑老 dispatch 比较输出推 M6 |
| C.advanced | Daily LLM 自审 / prompt drift / behavior drift | 长期累积型 detection, M5 ship 后才有数据 |
| B.advanced | Multi-state stuck detection 扩展 | M5 仅 Failure analysis; S2/S3/S6 stuck timeout 推 M6 |

---

## How

### 总体策略 (Phase Decomposition, R2 reconcile)

```
Phase 1 — Schema + Foundation (~25h)
  ├── Schema migration v3 → v4 (含 F dual-write + E + D 新列 + retry_count)
  │     • 1.1-1.9 schema/db (12h)
  │     • 1.10-1.13 instrumentation via AuditLogger middleware (10h)
  │     • 1.14-1.15 risk-stub validate + AD-M5-8 (3h)
  ├── db.py helpers (append_audit_event, query_audit_log, get_risk_tier)
  └── Audit log instrumentation (state_transition + llm_call via ProviderRouter middleware + human_decision)

Phase 2 — G + B (~21h)
  ├── comment-poll direct transition (G, 6h) + partial failure recovery (AD-M5-9)
  └── Failure analysis + smart retry (B, 15h) + JSON parse fallback + calibration spike

Phase 3 — D Review loop (~50-55h, 最大 workpackage)
  ├── Schema 加 rework_round / rework_of / rework_mode / rework_feedback / retry_count (Phase 1 已含)
  ├── Comment-poll 协议扩展 (4 commands) + AD-M5-2 rework_round semantics
  ├── /aria changes 改稿模式 Layer 2 二次进入 + force-push (AD-M5-3/AD-M5-4)
  ├── /aria redo 重做模式 新 dispatch + 旧 PR close (timing per AD-M5-3 §redo)
  └── rework cap=3 enforcement + Feishu round 显示 + boundary tests

Phase 4 — A Replay (~10h)
  ├── aria_layer1/replay.py (含 NULL-rework_mode handling + pre-M5 graceful degrade)
  ├── query audit log + dispatches 主表 join
  └── markdown report 生成

Phase 5 — C Drift defense (~12h)
  ├── Commit lint validator + Layer 2 hook (5h) + 12 enumerated fixtures + retry cap
  └── Spec diff LLM call (S8_MERGE only) + Feishu drift 卡片 (7h) + input slicing + cost spike

Phase 6 — T-acceptance + T-docs + T-prd-reframe + T-deploy (~12-15h, R2 扩展)
  ├── Tier-1 synthetic 验收 (12 explicit subtasks per 12 criteria, ~10h, QA-1 fix)
  ├── m5-handoff.yaml schema (additive on m4-handoff) + validate-m5-handoff.py 4 checks (~3h)
  ├── AD-M5-1..AD-M5-11 全部 backfill (TL-9 mechanical assert)
  ├── PRD 同步 (US-025 done + AD-M5 references) (~2h)
  └── T-deploy (owner-runnable, post-merge)
```

**Effort sum reconcile (R2 fix TL-1 + R2-cleanup TL-R2-1/4)**:
| Phase | Estimate | Range | Notes |
|-------|----------|-------|-------|
| Phase 1 | 25h | 22-28 | Schema + audit log instrumentation + risk-stub |
| Phase 2 | 21h | 19-24 | G cron direct + B failure analysis |
| Phase 3 | 52h | 50-55 | D Review loop hybrid (largest workpackage) |
| Phase 4 | 10h | 9-12 | A Replay deterministic state |
| Phase 5 | 12h | 11-14 | C Drift defense (commit lint + spec diff) |
| Phase 6 | 18h | 16-20 | T-acceptance ~12 + T-docs ~3 + T-prd ~2 + verify ~1 (T-deploy owner-only excluded; R2-cleanup TL-R2-1 reconcile from 13h after subtask sum 检测) |
| **Total (AI portion)** | **138h** | **127-153h** | T-deploy owner-runnable not counted in B.2 |

**Baseline lock**: 138h central (R2-cleanup TL-R2-4 reconcile from 130h; Phase 6 真实 subtask sum 18h 推高 total)
**OD-M5-1 trigger**: 165h (= 138 × 1.20, R2-cleanup TL-R2-2 raise from 156h to give pessimistic 155h + 10h safety cushion ≈ 6.5%)

### 关键技术决策 (AD-M5-1..AD-M5-11, Phase B 实施期回填; TL-9 mechanical assert)

| ID | 主题 | Phase | Framing (R2 fix TL-10) | Status |
|---|------|-------|------------------------|--------|
| AD-M5-1 | comment-poll direct transition reframe (supersedes AD-M4-9 § 决策 #4) | Phase 2 | open decision | _slot_ |
| AD-M5-2 | rework chain 机制文档 (per-row counter + rework_of FK, 锁定 R2 BA-1/BA-2 后) | Phase 3 | documentation (已 lock in §SQL) | _slot_ |
| AD-M5-3 | Layer 2 二次进入 mechanism (改稿 vs 重做的容器路径 + redo PR close timing) | Phase 3 | open decision | _slot_ |
| AD-M5-4 | force-push rationale lock (备选 append-commit 已考虑 rejected) | Phase 3 | documentation | _slot_ |
| AD-M5-5 | spec_drift_detected 阈值 + nomadVar ARIA_SPEC_DRIFT_THRESHOLD 调机制 + input slicing | Phase 5 | open decision | _slot_ |
| AD-M5-6 | Failure analysis LLM prompt + nomadVar ARIA_FAIL_RETRY_CONFIDENCE_MIN + calibration data | Phase 2 | open decision | _slot_ |
| AD-M5-7 | Audit log retention 策略 (M5 不 archival, M6 trigger condition 显式) | Phase 1 | open decision | _slot_ |
| AD-M5-8 | risk_tier dual-write 接口边界 + M5 stub write ('always' literal, not NULL, per R2 fix TL-2) | Phase 1 | open decision | _slot_ |
| AD-M5-9 | comment-poll partial failure recovery + reconciler 兜底契约 (per R2 fix BA-3) | Phase 2 | open decision | _slot_ |
| AD-M5-10 | abi_compat_promises M5→M6 forward-binding (新增 5 candidate promises 预 enumerate, R2 fix TL-14) | Phase 6 | open decision | _slot_ |
| AD-M5-11 | T-deploy schema migration v3→v4 3-safeguard inline (per R2 fix QA-4) | Phase 6 | open decision | _slot_ |

**AD-M5-10 forward-binding candidates** (预 enumerate per TL-14, finalized in Phase 6):
1. dispatch_audit_log_immutable_promise (M5 INSERT-only enforced via DB triggers; M6 不得 DROP triggers)
2. rework_round_cap_default_3_promise (M5 ARIA_REWORK_MAX_ROUND default=3; M6 不得改默认行为, 仅 nomadVar override)
3. spec_drift_threshold_default_70_promise (同上)
4. comment_poll_direct_transition_promise (M5 锁定 comment-poll 写 human_decision 后直接调 _handle_s7_human_gate; M6 不得回退到 cron-only transition)
5. risk_tier_dual_write_literal_always_promise (M5 写 'always' literal not NULL; M6 算法上线时 dual-write real value 同时仍写 risk_tier_stub)

### Schema migration v3 → v4 (additive only, R2 fixes BA-1/BA-2/BA-4/BA-5/BA-6/BA-13/QA-2)

```sql
-- F Risk-tier dual-write column
ALTER TABLE dispatches ADD COLUMN risk_tier TEXT;
-- M5 写 'always' literal (per R2 fix TL-2 + AD-M5-8, satisfy abi_compat #1 真正 dual-write)
-- 不 DROP risk_tier_stub, 不 RENAME

-- D Review loop columns (R2 fix BA-1: FK 用 dispatch_id TEXT 而非 rowid; BA-5: rework_mode NULL OK for parent rows)
ALTER TABLE dispatches ADD COLUMN rework_of TEXT REFERENCES dispatches(dispatch_id);
ALTER TABLE dispatches ADD COLUMN rework_round INTEGER NOT NULL DEFAULT 0;
ALTER TABLE dispatches ADD COLUMN rework_mode TEXT CHECK(rework_mode IS NULL OR rework_mode IN ('changes', 'redo', 'retry'));
-- BA-6 fix: 分离 fail_reason (enum) 与 rework_feedback (user prose)
ALTER TABLE dispatches ADD COLUMN rework_feedback TEXT;
-- QA-2 fix: retry_count 列 for B 项 Failure analysis system retry guard
ALTER TABLE dispatches ADD COLUMN retry_count INTEGER NOT NULL DEFAULT 0;

-- E Audit log immutable table (R2 fix BA-4: event_type CHECK; BA-13: FOREIGN KEY)
CREATE TABLE dispatch_audit_log (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  dispatch_id  TEXT    NOT NULL,
  ts           TEXT    NOT NULL,
  event_type   TEXT    NOT NULL,
  payload_json TEXT    NOT NULL,
  CHECK (json_valid(payload_json)),
  CHECK (event_type IN (
    'state_transition', 'llm_call', 'human_decision',
    'rework_cycle', 'failure_analysis', 'risk_tier_classified',
    'spec_drift_detected', 'commit_lint_result'
  )),
  FOREIGN KEY (dispatch_id) REFERENCES dispatches(dispatch_id)
);
CREATE INDEX idx_audit_dispatch_ts ON dispatch_audit_log(dispatch_id, ts);

CREATE TRIGGER audit_no_update BEFORE UPDATE ON dispatch_audit_log
  BEGIN SELECT RAISE(ABORT, 'audit log immutable'); END;
CREATE TRIGGER audit_no_delete BEFORE DELETE ON dispatch_audit_log
  BEGIN SELECT RAISE(ABORT, 'audit log immutable'); END;

-- 2 new fail_reason values (via migration script per 3-safeguard pattern inline in T-deploy 6.18)
-- 'rework_exceeded'  (rework_round > ARIA_REWORK_MAX_ROUND, see semantics below)
-- 'changes_requested' (current dispatch row 进入此终态 when /aria changes 或 /aria redo 触发, 新 dispatch row 接力)
```

**Comment-poll protocol field mapping (R2-cleanup BA-R2-4)**:
- `/aria approve` → `human_decision='approve'`; no rework_feedback
- `/aria reject: <reason>` → `human_decision='reject'`; `reject_reason=<reason>` (M4 字段保留, enum-like categorical)
- `/aria changes: <feedback>` → `human_decision='changes_requested'`; **`rework_feedback=<feedback>`** (M5 新增专用列, free-form text); 新 dispatch row `rework_mode='changes'`
- `/aria redo: <feedback>` → 同 changes, `rework_mode='redo'`

**rework_round semantics lock (R2 fix BA-2 + AD-M5-2 documentation)**:
- 原始 dispatch (无 rework): `rework_round=0, rework_of=NULL, rework_mode=NULL`
- /aria changes round 1: 新 row `rework_round=1, rework_of=<original_id>, rework_mode='changes'`
- /aria redo round 2: 新 row `rework_round=2, rework_of=<round1_id>, rework_mode='redo'`
- cap=3 含义: ARIA_REWORK_MAX_ROUND=3 → **允许最多 3 个 rework rows (round=1,2,3)**; round=4 创建拒绝, 当前 row → S_FAIL(rework_exceeded)
- System retry (B Failure analysis, R2 fix BA-7): 新 row `rework_round=0, rework_of=<parent>, rework_mode='retry'`, 不消耗 owner-facing rework cap; retry_count 单独追踪 (max 1 per dispatch)

### 4 commands comment-poll protocol

```
现有 (M4):
  /aria approve              → human_decision='approve', → S8_MERGE
  /aria reject: <reason>     → human_decision='reject', reject_reason=reason → S_FAIL(human_reject)

M5 新增:
  /aria changes: <feedback>  → human_decision='changes_requested', reject_reason=feedback,
                                + new dispatch row (rework_of=current, rework_mode='changes')
                                → 当前 row S_FAIL(changes_requested), 新 row S0_IDLE
  /aria redo: <feedback>     → 同上, 但 rework_mode='redo', 新 row 走完整 S0→S2→S3,
                                Layer 2 prompt 不含原代码

cap 触发:
  current.rework_round >= 3 → 拒绝创建新 row, 当前 row → S_FAIL(rework_exceeded)
```

---

## Constraints (abi_compat hard 约束, M5 不可违反; R2 fix TL-3 完整 4 enforcement)

| Promise | M5 必须遵守 | Enforcement | Tasks Ref |
|---------|------------|-------------|-----------|
| #1 risk_tier_stub_to_risk_tier | ADD COLUMN risk_tier 不 RENAME 不 DROP stub; dual-write 写 'always' literal (per AD-M5-8); read hot-swap | validate-m5-handoff.py::check_risk_tier_migration_acknowledged | T6.6.1 |
| #2 forgejo_approval_comment_id_unique_index | 不 DROP uq_approval_comment; rebuild 时保持 partial WHERE NOT NULL 语义 | validate-m5-handoff.py::check_unique_index_preserved | T6.6.2 |
| #3 comment_poll_cadence_independent | comment-poll 仍独立 Nomad job (G 项扩展责任 OK, 但不合并到 reconciler/cron job) | validate-m5-handoff.py::check_comment_poll_job_independent (扫 deploy/*.nomad.hcl 验证 aria-layer1-comment-poll job 存在且 type=batch) | T6.6.3 |
| #4 human_decision_first_decision_wins | rework 用 NEW dispatch row, 同 row human_decision 一次性写入 (per AD-M5-2 lock); CAS 守卫 | validate-m5-handoff.py::check_first_decision_wins_preserved | T6.6.4 |

---

## Acceptance criteria

### Tier-1 (synthetic, AI-implementable, 必过, R2 fix AI-1 + QA-1 增 live LLM + 完整 mapping)

- [ ] **A.1** Replay output 含完整 state 时间线 + LLM input_prompt+output_text + rework chain (单元 + 集成测试 + pre-M5 dispatch graceful degrade test)
- [ ] **B.1** Failure analysis mock LLM: retry/abort/notify_owner 路径 + confidence 0.7 boundary + JSON parse fallback + audit log 写入
- [ ] **B.1.live** Failure analysis live LLM gate (per R2 fix AI-1): 至少 1 次真 ProviderRouter call to glm-4.5-air,验证 (a) JSON schema 合规率 (b) confidence 字段 ∈ [0,1] (c) action 字段 ∈ enum (d) fallback chain 行为正确
- [ ] **C.1** Commit lint regex 12 enumerated fixtures (per R2 fix QA-5,见 tasks 5.5)
- [ ] **C.2** Spec diff mock LLM + score 计算 + Feishu 警告卡片 + S_FAIL skip + input slicing (proposal What/Acceptance only)
- [ ] **C.2.live** Spec diff live LLM gate (per R2 fix AI-1): 至少 1 次真 LLM call 在 1 个 mock PR diff,验证 JSON 合规 + score 字段 ∈ [0,100]
- [ ] **D.1** /aria changes + /aria redo 创建新 dispatch row (集成测试: 4 commands × 3 rounds × mixed mode)
- [ ] **D.2** rework_round cap=3 enforcement (单元测试: round=3 创建 OK, round=4 创建 reject + 当前 row → S_FAIL(rework_exceeded))
- [ ] **D.3** abi_compat #4 first-decision-wins 保持 (集成测试: 同一 row 多次写 human_decision 被 CAS 拒绝;新 row 接力一次性写入)
- [ ] **D.4** redo 模式 PR close 时序: 新 PR 创建后 (S5_PR_CREATED handler) 才写 "Superseded by #<new>" comment + close 旧 PR (per R2 fix BA-9)
- [ ] **D.5** Forgejo PR close failure handling (mock Forgejo 5xx, 系统状态不 orphaned, 失败写 audit log) (per R2 fix QA-9)
- [ ] **E.1** Schema migration v3→v4 3-safeguard inline (atomic backup + dry-run on copy + integrity_check + row_count assert per R2 fix QA-4)
- [ ] **E.2** Audit log immutable (UPDATE/DELETE 都 RAISE; event_type CHECK 拒绝非法 enum; FK 拒绝 orphan)
- [ ] **F.1** risk_tier 列加 + M5 dispatcher 写 'always' literal (not NULL, per R2 fix TL-2); validate-m5-handoff.py 4 checks PASS
- [ ] **G.1** comment-poll direct transition 集成测试 (mock approve → 60s 内 state=S8_MERGE) + partial failure recovery via reconciler 兜底 (per R2 fix BA-3)
- [ ] **HMAC.1** Feishu HMAC computation oracle test (independent fixture, per R2 fix TL-8: 防止 M4 paper-fix 复发)
- [ ] **All** 单元测试 + 集成测试合计 ≥ 600 PASS from ≥30 new test functions (≥15 为 behavioral integration tests, per R2 fix QA-14)

### Tier-2 (real-dispatch, post-deploy 累积, 不阻塞 Phase D.2; R2 fix QA-10 加 minimum partial acceptance)

**Minimum partial Tier-2 acceptance** (Phase D.2 owner sign-off 前必过, per R2 fix QA-10):
- [ ] **G.2.real** real comment → S8_MERGE max latency < 60s (R2 fix QA-20: max over ≥3 dispatches, p99 留到 ≥20 累积)
- [ ] **TIER-2-min-fallback** 若 2 周内无真 dispatch, owner 可强制 test dispatch (SQL inject S_FAIL + 验证 failure analysis 触发) 替代 B.2.real, 文档化 owner override

**Full Tier-2 (累积型, 不阻塞 production launch)**:
- [ ] **D.2.real** ≥3 real dispatches 含 ≥1 changes + ≥1 redo + ≥1 reject + ≥1 successful approve
- [ ] **D.2.cap** 至少 1 个 dispatch 测到 rework_round=2 (非边界测试)
- [ ] **B.2.real** ≥1 real failure 触发 Failure analysis LLM 给出建议 (owner 验证建议合理)
- [ ] **C.2.real** ≥1 real spec drift detected (score < 70 触发卡片) — owner 验证 drift 真实
- [ ] **H.dep.note** aria-layer2-runner deploy (M6 推迟,Track A-4) 阻塞 D.2.real 真 dispatch; Phase D.2 owner 显式 sign-off accept partial Tier-2 (per R2 fix TL-7)

### Phase D.2 final go_decision

- [ ] m5-handoff.yaml validator OK ✅
- [ ] m5-handoff.yaml::abi_compat_promises 全 4 条遵守 + 新增 5 M5→M6 forward-binding 文档化 (per AD-M5-10)
- [ ] **AD-M5-1..AD-M5-11 全部 Decided** (R2 fix TL-9: mechanical assert, 不用 'N')
- [ ] Tier-2 minimum partial 达成 (G.2.real + TIER-2-min-fallback per QA-10) OR Tier-2 N≥3 累积 OR owner 显式 sign-off accept partial

---

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-M5-1 | D Review loop 是 M5 最大 workpackage (~50-55h, 41% M5), 估计偏差风险大 | High | Phase A.1 早期 break down 到 ≤8h sub-tasks; 每周 progress review; AD-M5-2/3/4 早期 lock; **R2 fix TL-11: Phase 3 mid-checkpoint 加 (after schema+protocol ~15h)** |
| R-M5-2 | Failure analysis LLM 不稳定 (B 项) → 误 retry / 误 abort | Medium | confidence 阈值 0.7 + retry_count < 1 + 仅可恢复 fail_reason; LLM 错也最多多 1 次 dispatch (cost 可控) |
| R-M5-3 | Spec diff LLM 可能误判 drift (C 项) | Medium | score < 70 仅 Feishu 警告 (不阻塞); owner judge 是否真 drift; 阈值 nomadVar 可调 |
| R-M5-4 | Schema migration v3 → v4 风险 (含新表 + 多列 + INSERT-only triggers) | High | per `feedback_schema_migration_3_safeguard_pattern` 三重保险 (atomic backup + dry-run on copy + apply on prod with integrity check + row count assert) |
| R-M5-5 | Layer 2 二次进入 (D 改稿模式) 与现有 entrypoint 冲突 | Medium | Phase A.1 spec-drafter R1 audit ai-engineer 关注; Layer 2 entrypoint 加 mode='rework-changes' 分支 |
| R-M5-6 | comment-poll direct transition (G) 引入 race condition | Low | 复用 abi_compat #4 first-decision-wins 守卫; CAS UPDATE 防止重复 transition |
| R-M5-7 | M5 实测时长偏差 (M3 ratio 1.20, M4 0.47, σ 大) | Medium | OD-M5-1 trigger 144h 给 cushion; underbaseline retrospective 模板已 ready (per OD-M4-2) |
| R-M5-8 | abi_compat_promises 不慎违反 | High | validate-m5-handoff.py 自动 enforce; AD-M5-10 在 Phase 6 显式回头 audit 4 promises |

---

## Effort baseline + ratio reference

```
M2: 156h baseline → ~150h actual, ratio 0.96 (≈ baseline)
M3: 60h baseline → 72h actual, ratio 1.20 (over, OD-13)
M4: 60h baseline → 22-26h actual, ratio 0.47 (under, OD-M4-2 retrospective)
M5: 138h baseline (R2-cleanup reconcile per TL-R2-1/4) → ~? (本 Spec)
   ─ σ 大 (M2-M4 0.42-1.20), 单点估算 unreliable
   ─ PERT 三点估算 (per OD-M4-2 §M5 application guidance + R2-cleanup):
     • optimistic   ~117h  (Trust-but-verify 红利同 M4 模式 ratio 0.85)
     • likely      ~138h  (本 Spec R2-cleanup 估算)
     • pessimistic ~165h  (D Review loop 偏差 + LLM 调试反复 ratio 1.20)
   ─ OD-M5-1 trigger: 165h (= 138 × 1.20, R2-cleanup TL-R2-2 raise to match pessimistic + 0h margin: exact pessimistic 触发即合理 retrospective signal)
```

**M5 中期监控 (Phase B 实施, R2 fix TL-11 加 Phase 3 mid-checkpoint + QA-19 加 reforecast 响应协议)**:
- **Checkpoint 1 — Phase 1+2 完成后 (~46h 预算 R2 reconcile)**: 实测 vs 46h, 偏差 > 30% (> 60h) → 触发 mid-impl reforecast (响应协议见下)
- **Checkpoint 2 — Phase 3 中期 (schema+protocol ~15h 完成后)**: 跑 R3 audit on rework-loop 设计, 验证 AD-M5-2/3/4 实施前真锁
- **Reforecast 响应协议 (per QA-19, 类比 OD-M4-1 三层)**:
  1. 实测 actual_h_phase_1_plus_2 > 60h → 重算 M5 total projection
  2. 识别 Phase 3 sub-tasks eligible for M6 deferral (优先级: redo mode full cycle > changes mode > 共用 schema)
  3. Owner decision required within 1 session before Phase 3 start
  4. M5 total > 156h → 触发 OD-M5-1 underbaseline-or-overbaseline retrospective decision

---

## Cross-references

**Predecessors (M0-M4)**:
- [openspec/archive/2026-04-23-aria-2.0-m1-mvp/](../../archive/2026-04-23-aria-2.0-m1-mvp/) — M1 MVP 容器
- [openspec/archive/2026-05-03-aria-2.0-m2-layer1-state-machine/](../../archive/2026-05-03-aria-2.0-m2-layer1-state-machine/) — M2 Layer 1 状态机
- [openspec/archive/2026-05-07-aria-2.0-m3-cycle-close-glm-routing-recovery/](../../archive/2026-05-07-aria-2.0-m3-cycle-close-glm-routing-recovery/) — M3 GLM routing
- [openspec/archive/2026-05-09-aria-2.0-m4-human-gate-feishu-approval/](../../archive/2026-05-09-aria-2.0-m4-human-gate-feishu-approval/) — M4 Human gate

**Decisions**:
- [.aria/decisions/2026-05-10-us025-m5-brainstorm.md](../../../.aria/decisions/2026-05-10-us025-m5-brainstorm.md) — Brainstorm Q0-Q9 全部锁定 (本 Spec source-of-truth)
- [.aria/decisions/2026-05-09-od-m4-2-underbaseline-retrospective.md](../../../.aria/decisions/2026-05-09-od-m4-2-underbaseline-retrospective.md) — M4 ratio 0.47 retrospective + M5 application guidance

**Handoff docs**:
- [aria-orchestrator/docs/m4-handoff.yaml](../../../aria-orchestrator/docs/m4-handoff.yaml) — abi_compat_promises 4 forward-binding (本 Spec hard constraints source)
- [docs/handoff/2026-05-09-track-a-deploy-done.md](../../../docs/handoff/2026-05-09-track-a-deploy-done.md) — Track A T-deploy 引出 G + H inputs

**Memory entries (M5 design relevant)**:
- `feedback_phase_a_depth_drives_b_velocity` — Phase A 深度 → B mechanical translation
- `feedback_paper_fix_antipattern` — code+test+doc 三位一体
- `feedback_owner_invoked_convergence_loop` — audit 收敛模式
- `feedback_spec_reframe_in_session` — AD-M4-9 → AD-M5-1 reframe 三处文档化
- `feedback_feishu_hmac_key_msg_swap` — LLM call 测试 oracle 设计 (避免 paper-fix 单元 test 与代码同时错)
- `feedback_schema_migration_3_safeguard_pattern` — schema v3→v4 migration 模板
- `feedback_smoke_dispatch_sql_inject_pattern` — Tier-1 smoke 不依赖 M2/M3 真实路径
- `feedback_handoff_doc_assumes_venv_ready_smell` — T-deploy 必显式列 venv refresh + schema migration step
