# Aria 2.0 M5 — Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable

> **Level**: 3 (Full — 跨多 module + 架构变更 + schema migration + abi_compat 约束)
> **Status**: Draft (Phase A.1, ready for Phase A.2 post_spec audit)
> **Change ID**: `aria-2.0-m5-replay-reconciler-drift-review-loop-audit`
> **Parent US**: [US-025](../../../docs/requirements/user-stories/US-025.md)
> **Parent PRD**: [prd-aria-v2.md §M5](../../../docs/requirements/prd-aria-v2.md) (Week 20-25, 120h baseline)
> **Predecessor Spec**: [aria-2.0-m4-human-gate-feishu-approval](../../archive/2026-05-09-aria-2.0-m4-human-gate-feishu-approval/proposal.md) (M4 archived 2026-05-09)
> **Brainstorm Source**: [.aria/decisions/2026-05-10-us025-m5-brainstorm.md](../../../.aria/decisions/2026-05-10-us025-m5-brainstorm.md) (10 个 Q 全部锁定)
> **Effort baseline**: 113-118h (vs 120h PRD lock); OD-M5-1 trigger at 144h
> **abi_compat hard constraints**: 4 forward-binding promises from m4-handoff.yaml (validate-m5-handoff.py enforced)

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

### 总体策略 (Phase Decomposition)

```
Phase 1 — Schema + Foundation (~30h)
  ├── Schema migration v3 → v4 (含 F + E)
  ├── db.py helpers (append_audit_event, query_audit_log, get_risk_tier)
  └── Audit log instrumentation (state_transition + llm_call + human_decision)

Phase 2 — G + B (~21h)
  ├── comment-poll direct transition (G, 6h)
  └── Failure analysis + smart retry (B, 15h)

Phase 3 — D Review loop (~50-55h, 最大 workpackage)
  ├── Schema 加 rework_round / rework_of / rework_mode columns
  ├── Comment-poll 协议扩展 (4 commands)
  ├── /aria changes 改稿模式 Layer 2 二次进入 + force-push
  ├── /aria redo 重做模式 新 dispatch + 旧 PR close
  └── rework cap=3 enforcement + Feishu round 显示

Phase 4 — A Replay (~10h)
  ├── aria_layer1/replay.py
  ├── query audit log + dispatches 主表 join
  └── markdown report 生成

Phase 5 — C Drift defense (~12h)
  ├── Commit lint validator + Layer 2 hook (5h)
  └── Spec diff LLM call + Feishu drift 卡片 (7h)

Phase 6 — T-acceptance + T-docs + T-prd-reframe + T-deploy
  ├── Tier-1 synthetic 验收 (各项单元 + 集成测试)
  ├── m5-handoff.yaml schema (additive on m4-handoff)
  ├── AD-M5-1..M5-N 全部 backfill
  ├── PRD 同步 (US-025 done + AD-M5 references)
  └── T-deploy (owner-runnable, post-merge)
```

### 关键技术决策 (AD-M5 slots, Phase B 实施期回填)

| AD-M5-N | 主题 | Phase | Status |
|---------|------|-------|--------|
| AD-M5-1 | comment-poll direct transition reframe (supersedes AD-M4-9 § 决策 #4) | Phase 2 | _slot_ |
| AD-M5-2 | rework_round 存储设计 (新 dispatch row vs 同 row counter) | Phase 3 | _slot_ |
| AD-M5-3 | Layer 2 二次进入 mechanism (改稿 vs 重做的容器路径区分) | Phase 3 | _slot_ |
| AD-M5-4 | force-push vs append-commit (改稿模式的 PR history shape) | Phase 3 | _slot_ |
| AD-M5-5 | spec_drift_detected 阈值 (默认 70, 阈值可调机制) | Phase 5 | _slot_ |
| AD-M5-6 | Failure analysis LLM prompt template 设计 + 版本管理 | Phase 2 | _slot_ |
| AD-M5-7 | Audit log retention 策略 (M5 不做 archival, 推 M6) | Phase 1 | _slot_ |
| AD-M5-8 | risk_tier dual-write 接口边界 (read-side hot-swap mechanism) | Phase 1 | _slot_ |
| AD-M5-9 | comment-poll 进程崩溃后的 reconciler 兜底契约 | Phase 2 | _slot_ |
| AD-M5-10 | abi_compat_promises forward-binding M5→M6 (新增 promises) | Phase 6 | _slot_ |
| AD-M5-11 | T-deploy schema migration v3→v4 3-safeguard 实施 | Phase 6 | _slot_ |

### Schema migration v3 → v4 (additive only)

```sql
-- F Risk-tier dual-write column
ALTER TABLE dispatches ADD COLUMN risk_tier TEXT;
-- (不 DROP risk_tier_stub, 不 RENAME)

-- D Review loop columns
ALTER TABLE dispatches ADD COLUMN rework_of INTEGER REFERENCES dispatches(rowid);
ALTER TABLE dispatches ADD COLUMN rework_round INTEGER NOT NULL DEFAULT 0;
ALTER TABLE dispatches ADD COLUMN rework_mode TEXT CHECK(rework_mode IN ('changes', 'redo'));

-- E Audit log immutable table
CREATE TABLE dispatch_audit_log (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  dispatch_id  TEXT    NOT NULL,
  ts           TEXT    NOT NULL,
  event_type   TEXT    NOT NULL,
  payload_json TEXT    NOT NULL,
  CHECK (json_valid(payload_json))
);
CREATE INDEX idx_audit_dispatch_ts ON dispatch_audit_log(dispatch_id, ts);

CREATE TRIGGER audit_no_update BEFORE UPDATE ON dispatch_audit_log
  BEGIN SELECT RAISE(ABORT, 'audit log immutable'); END;
CREATE TRIGGER audit_no_delete BEFORE DELETE ON dispatch_audit_log
  BEGIN SELECT RAISE(ABORT, 'audit log immutable'); END;

-- 2 new fail_reason values
-- (CHECK constraint update via migration script per `feedback_schema_migration_3_safeguard_pattern`)
-- 'rework_exceeded'  (rework_round >= ARIA_REWORK_MAX_ROUND)
-- 'changes_requested' (existing M4 reject_reason now used as fail_reason for /aria changes /redo)
```

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

## Constraints (abi_compat hard 约束, M5 不可违反)

| Promise | M5 必须遵守 | Enforcement |
|---------|------------|-------------|
| #1 risk_tier_stub_to_risk_tier | ADD COLUMN risk_tier 不 RENAME 不 DROP stub; dual-write; read hot-swap | validate-m5-handoff.py::check_risk_tier_migration_acknowledged |
| #2 forgejo_approval_comment_id_unique_index | 不 DROP uq_approval_comment; rebuild 时保持 partial WHERE NOT NULL 语义 | validate-m5-handoff.py::check_unique_index_preserved |
| #3 comment_poll_cadence_independent | comment-poll 仍独立 Nomad job (不合并到其他 job, 即使 G 项扩展责任) | M5 deploy review (T-deploy.6 carryforward) |
| #4 human_decision_first_decision_wins | rework 用 NEW dispatch row, 同 row human_decision 一次性写入 | validate-m5-handoff.py::check_first_decision_wins_preserved |

---

## Acceptance criteria

### Tier-1 (synthetic, AI-implementable, 必过)

- [ ] **A.1** Replay output 含完整 state 时间线 + LLM metadata + rework chain (单元测试 + 集成测试)
- [ ] **B.1** Failure analysis LLM 调用 + retry/abort/notify_owner 路径 + audit log 写入 (单元测试 + mock LLM 集成测试)
- [ ] **C.1** Commit lint 拒绝不规范 commit (regex 单元测试 12+ fixtures)
- [ ] **C.2** Spec diff LLM 调用 + score 计算 + Feishu 警告卡片 (单元测试 + mock LLM)
- [ ] **D.1** /aria changes + /aria redo 创建新 dispatch row (集成测试: 4 commands × 3 rounds)
- [ ] **D.2** rework_round cap=3 enforcement (单元测试: round 3 后 fail_reason='rework_exceeded')
- [ ] **D.3** abi_compat #4 first-decision-wins 保持 (集成测试: 同一 row 多次写 human_decision 应被 CAS 拒绝)
- [ ] **E.1** Schema migration v3→v4 backward-compat (per `feedback_schema_migration_3_safeguard_pattern`)
- [ ] **E.2** Audit log immutable (UPDATE/DELETE 都 RAISE)
- [ ] **F.1** risk_tier 列加但 M5 行为不变 (validate-m5-handoff.py::check_risk_tier_migration_acknowledged)
- [ ] **G.1** comment-poll direct transition 集成测试 (mock approve → 60s 内 state=S8_MERGE)
- [ ] **All** 单元测试 + 集成测试合计 ≥ 600 PASS (vs M4 final 537)

### Tier-2 (real-dispatch, post-deploy 累积, 不阻塞 Phase D.2)

- [ ] **D.2.real** ≥3 real dispatches 含 ≥1 changes + ≥1 redo + ≥1 reject + ≥1 successful approve
- [ ] **D.2.cap** 至少 1 个 dispatch 测到 rework_round=2 (非边界测试)
- [ ] **B.2.real** ≥1 real failure 触发 Failure analysis LLM 给出建议 (owner 验证建议合理)
- [ ] **C.2.real** ≥1 real spec drift detected (score < 70 触发卡片) — owner 验证 drift 真实
- [ ] **G.2.real** real comment → S8_MERGE p99 latency < 60s (M4 实测 17min 含中断, M5 必须 < 60s)

### Phase D.2 final go_decision

- [ ] m5-handoff.yaml validator OK ✅
- [ ] m5-handoff.yaml::abi_compat_promises 全 4 条遵守 + 新增 M5→M6 forward-binding 文档化
- [ ] AD-M5-1..M5-N 全部 Decided
- [ ] Tier-2 N≥3 累积或 owner 显式 sign-off accept partial Tier-2

---

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-M5-1 | D Review loop 是 M5 最大 workpackage (~50-55h, 41% M5), 估计偏差风险大 | High | Phase A.1 早期 break down 到 ≤8h sub-tasks; 每周 progress review; AD-M5-2/3/4 早期 lock |
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
M5: 120h baseline → ~? (本 Spec)
   ─ σ 大 (M2-M4 0.42-1.20), 单点估算 unreliable
   ─ 建议 PERT 三点估算 (per OD-M4-2 §M5 application guidance):
     • optimistic   ~95h  (Trust-but-verify 红利同 M4 模式)
     • likely      ~115h  (本 Spec 估算)
     • pessimistic ~140h  (D Review loop 偏差 + LLM 调试反复)
   ─ OD-M5-1 trigger: 144h (= 120 × 1.2)
```

**M5 中期监控 (Phase B 实施)**:
- Phase 1+2 完成后 (~51h预算): 实测 actual_h_phase_1_plus_2 vs 51 estimate, 偏差 > 30% → 触发 mid-impl reforecast (per `feedback_audit_convergence_pattern` mid-implementation 模式)
- Phase 3 (D Review loop) 是高风险段, 加 R3 audit checkpoint

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
