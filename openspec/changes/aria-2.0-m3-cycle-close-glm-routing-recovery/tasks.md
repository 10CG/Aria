# aria-2.0-m3-cycle-close-glm-routing-recovery — Tasks

> **Spec**: [proposal.md](./proposal.md)
> **Status**: **Approved** (Phase A.3 lock 2026-05-04, AI-drafted per AD-M0-9)
> **Baseline (OD-12 §Q2)**: 185h hard / 5-6 weeks 50% 投入
> **Audit pattern (OD-12 §Q8c)**: 混合 (Phase A.2 4-round + Phase B.2 scope-bounded 1-round per task group + Phase D 4-round, ~25h overhead in baseline)

---

## Phase A: 规划

### Phase A.1 — Spec drafting (NOW, ~12h)

- [x] **A.1.1** Spec 目录创建 `openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/` (含 patches/)
- [x] **A.1.2** proposal.md 起草 (~6h) — 含 Why/What 9 节/Acceptance/Out of Scope/Risks/AD-M3 placeholder/Phase 路线图/Owner action
- [x] **A.1.3** tasks.md 起草 (本文件, ~5h)
- [x] **A.1.4** 5 PRD patches 起草 (`patches/01-05`, ~2h, 按 R2 closeout §"PRD patches needed")
- [ ] **A.1.5** Forgejo Issue T0 创建 (M3 kickoff issue, owner 触发 / Phase A.3 锁后)

### Phase A.2 — post_spec audit (DONE 2026-05-04, ~4h actual)

- [x] **A.2.1** R1 4-agent multi-agent audit (backend-architect / qa-engineer / tech-lead / ai-engineer parallel)
  - 验证 R2 (2026-05-03) findings 全 closure: 3 critical (C1/C2/C3) + 10 important (I1-I10) + 6 minor (M1-M6) 全 COVERED
  - R1 NEW: 18 findings (2 Critical + 9 Important + 9 Minor) + 7 owner-decide (OD-14 / OD-15 / OD-3d/3e/3f/3g / Q-NEW-1)
  - Verdict aggregate: BLOCK_NEED_OWNER (qa + ai NEEDS_OWNER_INPUT)
- [x] **A.2.2** R1 audit report `.aria/audit-reports/post_spec-2026-05-04T103702Z-us023-m3.md` + advisory `.aria/decisions/2026-05-04-us-023-phase-a2-r1-owner-advisory.md`
- [x] **A.2.3** Owner advisory 7/7 RESOLVED 2026-05-04 (sustain all AI defaults)
- [x] **A.2.4** R1 fix batch auto-resolved (proposal.md + tasks.md ~17 fix points; commit `9479257`)
- [x] **A.2.5** R2 4-agent fix-verify SCOPE_OK_R2 4/4 (R1 closure 24/24 + 0 NEW critical/important + 14/14 coherence PASS)
- [x] **A.2.6** R2 closeout report `.aria/audit-reports/post_spec-r2-2026-05-04T1130Z-us023-m3.md`
- [x] **A.2.7** R3+R4 collapse per OD-15 (R2 SCOPE_OK_R2 4/4 + tech-lead 显式 COLLAPSE_R3_R4_PROCEED_A3)

### Phase A.3 — Approved 准入 (DONE 2026-05-04, ~1h actual)

- [x] **A.3.1** OD-12 baseline final lock (185h 显式记录 in proposal.md + tasks.md status table; m3-handoff.yaml `effort.baseline_h` 写入 Phase B.2.Z T16.1)
- [x] **A.3.2** **OD-13** 立 + applied: `.aria/decisions/2026-05-04-od-13-prd-m3-effort-90-to-185h.md` + PRD line 404 (90→185h + reframe) + line 409 (750→845h) + line 412 (注释段追加) + 新增 §M3 detail 章节 (Patches 01/02/03/04/05 内容合并 commit)
- [x] **A.3.3** Spec proposal.md Status: Draft → **Approved** (AI-drafted per AD-M0-9 with provenance; owner final sign-off pending implicit per `feedback_ai_代填_sign_off_pattern`, audit trail 双 advisory)
- [x] **A.3.4** Agent 分配回填 (proposal.md AD-M3-1..7 表格 主责 agent column 已加; 与 M2 模式一致)
- [ ] **A.3.5** Forgejo Issue T0 创建 (M3 kickoff issue, owner action, 推 Phase B.1)

---

## Phase B: 开发

### Phase B.1 — feature 分支 (~0.5h)

- [x] **B.1.1** 主仓 + aria-orchestrator submodule 同名 feature 分支创建: `feature/aria-2.0-m3-cycle-close-glm-routing-recovery` (实质完成 Phase A 期间; 主仓 HEAD=`dc87bac`, aria-orchestrator submodule HEAD=`f2c2ae3`)
- [x] **B.1.2** 双远程 push branch (origin + github) — 验证 2026-05-05 state-snapshot: 主仓 + standards + aria + aria-orchestrator 所有 4 repos 双 remote `parity=equal`, `overall_parity=true`

### Phase B.2.0 — M2 carryover (T1-T4, ~21h, OD-11 解锁)

#### T1 — `aria-layer2-runner` HCL parameterized job (~6h, AD-M3-1 触发)

- [x] **T1.1** Fork from US-021 M1 HCL → `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl`; diff 标注 M1→M3 变化点 (header 表格 7 维度)
  - **Path reframe** (per `feedback_spec_reframe_in_session`): tasks.md 字面 `aria-orchestrator/jobs/aria-layer2-runner.nomad.hcl` 与 sister files 路径不一致; 实际 path 取 `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` (与 `aria-runner-template.hcl` / `aria-build.hcl` / `aria-layer1.hcl` 对齐, 无 `.nomad.` infix)。Reframe 三处: HCL header note + commit message + 本 tasks.md 此处。
- [x] **T1.2** `meta_required` 字段 enumerate (per R2 I1 + OD-3a): `ISSUE_ID, ISSUE_URL, DISPATCH_ID, IMAGE_SHA, IDEMPOTENCY_KEY` ✓ HCL `parameterized.meta_required` 5 keys
- [x] **T1.3** `meta_optional` 字段: `BUDGET_CAP_USD, TRIAGE_BODY_JSON` ✓ HCL `parameterized.meta_optional` 2 keys
- [x] **T1.4** Image pin sha digest (per OD-3a default, AD-M1-7 reproducibility): HCL `image = "registry.10cg.pub/aria-runner@sha256:${NOMAD_META_IMAGE_SHA}"` ✓ — 注: registry domain `registry.10cg.pub` (proposal 字面) 与 M1 实际 `forgejo.10cg.pub/10cg/aria-runner` 不一致, T1.OWNER 部署前 owner 确认 (HCL header note + AD-M3-1 待回填)
- [x] **T1.5** Driver = docker (M1 一致, 不切 raw_exec); host_volume `aria-runner-outputs` + `aria-runner-inputs` (M1 一致, 无 `aria-runner-cache` per M1 baseline 实证)
- [x] **T1.6** Resources / Constraints: M1 baseline (cpu=2000 MHz, mem=2048 MiB), heavy nodes only (`node.class = heavy_workload`, M1 实证 ground truth) — 注: proposal §一 字面 "CPU 1000" 是 paraphrase, 此处遵从 M1 BA-I1 实证值 (HCL header note 标 deviation)
- [x] **T1.7** Idempotency: DISPATCH_ID + IDEMPOTENCY_KEY 双重 dedupe — HCL 层完成 meta key enumeration (T1.2) + restart `attempts=0 mode=fail` (跨 alloc retry 由 Layer 1 reconciler + entrypoint dedupe 处理); entrypoint 层 dedupe 在 image 内, 非 HCL scope
- [x] **T1.8** `nomad job validate aria-layer2-runner.hcl` pre-deploy (per `feedback_nomad_hcl_validate_early`) — PASS (Nomad v1.7.7, "Job validation successful"; driver-level checks 待 Aether agent 连接验证, per `feedback_hcl_driver_feature_matrix`)
- [x] **T1.9** AD-M3-1 回填 (HCL meta keys + image pin 决策 + registry domain owner-decision) — 2026-05-05 done: aria-orchestrator/docs/architecture-decisions.md §AD-M3-* 占位段 (10 槽) + AD-M3-1 完整 6 段 (决策/背景/Alternatives/选型理由/风险/回滚路径) + version history 0.7 + proposal.md AD-M3-1 行 cross-reference
- [ ] **T1.OWNER** Owner action: (a) 确认 image registry domain (registry.10cg.pub 新建 vs 沿用 forgejo.10cg.pub); (b) `nomad var put nomad/jobs/aria-layer2-runner ...` 8 secrets (T13 rotation 后); (c) `nomad job run aria-layer2-runner.hcl` on Aether (~30min, verify alloc launch)

**T1.done = HCL validate PASS + Aether 部署成功 + sample dispatch 实测 alloc state 推进 + AD-M3-1 回填**

#### T2 — `NomadAllocHTTPProvider` 生产化 (~4h, AD-M3-2 触发, R2 C3)

- [x] **T2.1** 实施 `aria_layer1/alloc_status_provider.py` `NomadAllocHTTPProvider` class (276 行)
  - **Path reframe** (per `feedback_spec_reframe_in_session`): proposal §二 字面 `aria_layer1/clients/alloc_status_provider.py` 与 sister files 路径不一致 (实际无 `clients/` 子目录, nomad_client.py / forgejo_client.py / silknode_client.py 均 flat); 实际 path 取 `aria_layer1/alloc_status_provider.py`。Reframe 三处: 文件 header note + 本 tasks.md 此处 + commit message。
- [x] **T2.2** `AllocStatusProvider` Protocol 实施 — M2 frozen Protocol (interfaces.py L128) 直接复用, additive 即可 (per AD-M2-9 §contract); M3 实施类 duck-type satisfies, 无需修改 Protocol 自身
- [x] **T2.3** HTTP GET `/v1/allocation/{alloc_id}` — `_fetch_allocation` 实施 (urllib stdlib, percent-quote alloc_id, NOMAD_TOKEN forward-compat); 默认 base_url=`$NOMAD_ADDR` env 或 Aether `http://192.168.69.70:4646`
- [x] **T2.4** 30s ack-poll budget — provider 自身 per-call timeout 5s (≥6 retries fit 在 30s budget); 30s budget 由 caller (M2 `_handle_s4_launch` ack-poll loop + `_handle_s5_await` 跨 tick re-entry) 强制, provider 保持简单 (单 GET, 无内部 retry)
- [x] **T2.5** alloc states 映射 (5 → M2 frozen 3-state vocabulary, additive-only per AD-M2-9):
  - Nomad `pending|queued` → Protocol `running` + exit_code=None (M2 _handle_s5 heartbeat & 不动)
  - Nomad `running` → `running` + None
  - Nomad `complete` → `terminated` + exit_code=0 (从 TaskStates Terminated event 取, defensive 验非零)
  - Nomad `failed` → `terminated` + exit_code (从 Terminated event ExitCode 取, default 1)
  - Nomad `lost` → `lost` + None
  - Unknown → `running` + None (defensive, 防 Nomad 新版本 ClientStatus enum 演进)
- [x] **T2.6** Lazy-wire 注入 — `extension.py` 两处加 (per OD-3c default + R2 C3): `_handle_s4_launch` ack-poll path (ARIA_LAZY_WIRE=1 → NomadAllocHTTPProvider) + `_handle_s5_await` 进入时 (alloc_id 已设, lazy-wire opt-in); 与 ForgejoCliClient + NomadDispatchClientHTTP pattern 一致
- [x] **T2.7** Unit tests — `tests/test_t2_alloc_status_provider.py` 12 unit tests: 5 ClientStatus mapping + 4 defensive fallback (unknown/empty alloc_id/fetch error/complete with task non-zero) + Protocol conformance + 2 exit_code extraction (with/without Terminated event); 全 PASS
- [x] **T2.8** Integration tests — 3 integration via `unittest.mock.patch` urlopen (URL %2F-encoding / 404 GC fallback / real Nomad-shaped JSON 解析); 全 PASS。无 httpx 第三方依赖 (stdlib mock 与 test_phase1/test_t8 precedent 一致)
- [x] **T2.9** AD-M3-2 回填 (lazy-wire + Protocol contract 决策) — 2026-05-05 done: aria-orchestrator/docs/architecture-decisions.md §AD-M3-2 完整 6 段 (决策/背景/6 alternatives/选型理由/7 风险/3-level 回滚) + version history 0.8 + proposal.md AD-M3-2 行 cross-reference

**T2.done = NomadAllocHTTPProvider class 实施 + Protocol assert + ARIA_LAZY_WIRE=1 注入测试 + Nomad mock integration test PASS + AD-M3-2 回填**

#### T3 — Schema migration v2 (~3h, AD-M3-3 触发, R2 I4 + R2 M3 + R2 M5 + R1-C1/M2/M3)

- [x] **T3.1** Migration script `aria_layer1/migrations/002_schema_v2_additive.sql` (44 行):
  - **Path reframe** (per `feedback_spec_reframe_in_session`): 字面 `aria-orchestrator/migrations/...` 改为 in-package `aria_layer1/migrations/...` (importlib.resources 可加载, raw_exec/docker/pip install 通用); reframe 三处: SQL header note + schema_migrate.py header + 本 tasks.md 此处
  - **Pre-condition (R1-C1)**: 由 schema_migrate.py `_assert_fallback_triggered_column_exists` 实施 (PRAGMA table_info), fail-fast if missing
  - 6 ALTER TABLE ADD COLUMN: cycle_start_ts / cycle_end_ts / dispatched_job_id / eval_id / provider_cost_model / attempt_history_json (全 TEXT nullable additive per AD-M1-7)
  - CREATE TABLE IF NOT EXISTS migration_notes (key/note/applied_at, per R1-M3)
  - INSERT OR IGNORE schema_meta fallback_chain_outcome_enum (per R1-C2)
  - UPDATE schema_meta SET value='2.0' WHERE key='schema_version'
- [x] **T3.2** `fallback_chain_json` 写时 transform (per R2 I4): `_transform_fallback_chain_v1_to_v2` Python 实施 (Python SQL 联动, 同 BEGIN IMMEDIATE 事务内); v1 string-array → v2 dict-array (7 keys: model/trigger_reason='legacy_v1_migrated'/latency_ms/endpoint_from/endpoint_to/model_switched_to/outcome='ok'); 已是 v2 dict-array round-trip safe; null/malformed 跳过
- [x] **T3.3** schema_version 写入 — 通过 SQL `UPDATE schema_meta SET value='2.0'` (existing key) + schema.sql `INSERT OR IGNORE schema_version='2.0'` (fresh DB)
- [x] **T3.4** Backfill rules — `_apply_backfill_rules` 实施 (Python, 同 BEGIN IMMEDIATE 事务):
  - Rule 1: provider_cost_model NULL → 'subscription_flat' (M1+M2 Luxeno-only per AD-M1-12 + R2 M3)
  - Rule 2: cycle_start_ts NULL on (S9_CLOSE / S_FAIL) → state_entered_at (per R2 M5, 显式 placeholder)
  - 每 rule 写 migration_notes audit row (per R1-M3)
- [x] **T3.5** Migration runner — `aria_layer1/schema_migrate.py:apply_migrations(conn)` (305 行); BEGIN IMMEDIATE 事务包裹, ALTER 失败 ROLLBACK; idempotent re-runs via schema_version 检测; wired in `extension.py:_get_repo` (schema.sql executescript → apply_migrations)
- [x] **T3.6** Test fixture — `_create_v1_baseline_db()` + `_insert_v1_dispatch()` 在 test_t3 内合成 11-row M2 T15.3 trajectory (DEMO-001/002 S9_CLOSE + ISS-705..713 S_FAIL); 不依赖外部 .db 文件 (per testability + reproducibility, 无 binary fixture)
- [x] **T3.7** Tests — `tests/test_t3_schema_migration.py` 16 tests: 5 apply_migrations behavior + 1 R1-C1 pre-condition + 4 fallback_chain transform + 3 backfill rules/audit + 3 integration (11-row fixture / drift guard / extension._get_repo 触发); 全 PASS, 0 regression on 283 baseline (now 299 total)
- [x] **T3.8** inline UNIQUE 保留 — `schema.sql:98` `CONSTRAINT uq_issue_active UNIQUE (issue_id)` 不动 (drop 推 schema v3 / M4); 应用层 dedupe (M2 T15.2 e36beb2 dedupe sister-bug fix) 续用
- [x] **T3.9** Drift guard test — `test_drift_guard_committed_schema_matches_migrated_v1` (per `feedback_validator_repo_drift_guard_test`): 两 path (fresh schema.sql 直建 v2 vs v1+migration) 必须 column set + table set + schema_version 完全相等; 实测 PASS
- [x] **T3.10** AD-M3-3 回填 — 2026-05-05 done: aria-orchestrator/docs/architecture-decisions.md §AD-M3-3 完整 6 段 (决策 7 维度 / 背景 / 7 alternatives / 7 选型理由 / 8 风险 / 4-level 回滚 / 治理影响) + version history 0.9 + proposal.md AD-M3-3 行 cross-reference

**T3.done = migration apply 11-row fixture 0 loss + 5 col additive + dict fallback transform + backfill rules + AD-M3-3 回填**

#### T4 — Single-issue Layer 2 cycle smoke (~3h)

- [ ] **T4.1** Trigger 1 issue 走 S0→S9_CLOSE (Tier-2 Aether 实链, T1+T2+T3 wired)
- [ ] **T4.2** Verify alloc launch + alloc state polling + S6_REVIEW LLM (Luxeno) + S7-S8 Forgejo + S9_CLOSE
- [ ] **T4.3** Capture cycle_start_ts + cycle_end_ts (schema v2)
- [ ] **T4.4** Smoke 通过 → 解锁 T15 ≥10 issue 集成

**T4.done = 1 issue 真实 Aether cycle PASS + cycle 时间戳 captured**

---

### Phase B.2.1 — M3 新 scope (T5-T12, ~90h)

#### T5 — Reconciler design + `aria-layer1-reconcile.nomad.hcl` (~6h, AD-M3-5 触发, OD-12 §Q3+Q4)

- [x] **T5.1** HCL `aria-orchestrator/deploy/aria-layer1-reconcile.nomad.hcl` (path reframe: `deploy/` not `jobs/` 与 sister `aria-layer1-cron.nomad.hcl` 对齐, per `feedback_spec_reframe_in_session`): Nomad periodic job, 30min cadence, half-offset cron expression `15,45 * * * *` (avoids :00 collision with cron tick at `0 * * * *`)
- [x] **T5.2** Entry-point reframe (per `feedback_spec_reframe_in_session`): tasks.md 字面 "同 docker image 不同 entry-point" 描述 Layer 2 image; 实际 Layer 1 reconciler 运行 Layer 1 代码路径 (查 dispatches.db + Forgejo + Feishu, 不跑 user prompt) → raw_exec on light-1 venv mirroring `aria-layer1-cron.nomad.hcl`. CLI module `aria_layer1.reconcile_runner` (sister to `tick_runner.py`).
- [x] **T5.3** 三阈值 mixed env+const (per OD-12 §Q3): `ARIA_RECONCILER_S5_MAX_AGE_MIN=60` env (HCL) / `ARIA_RECONCILER_MAX_ATTEMPTS=3` env (HCL) / `STUCK_ALLOC_STATES=('pending','queued')` 代码常量 (`reconciler.py:ReconcilerThresholds`, 不开放 env 防 misclassify 'running' 为 stuck → 风险 #2)
- [x] **T5.4** 混合路由 `MechanicalReconciler.decide()`: `attempt_count < MAX_ATTEMPTS` → `Decision.RETRY` (T6 CAS UPDATE attempt_count++) / `attempt_count >= MAX_ATTEMPTS` → `Decision.FAIL` (T6 CAS UPDATE state='S_FAIL' + fail_reason 路由矩阵 per T6.3)
- [x] **T5.5** CAS 复合版本字段契约 documented in `reconciler.py` module docstring (per OD-12 §Q4 + R2 I5): `UPDATE dispatches SET ... WHERE rowid=? AND state='S5_AWAIT' AND last_heartbeat_at=? AND attempt_count=?`; rowcount==0 一次重试 (re-SELECT + re-decide + re-UPDATE) 失败推下一 reconciler tick. T6 实施 SQL.
- [x] **T5.6** SQLite WAL + `PRAGMA busy_timeout=5000` 复用 `db.open_repo` 中央 PRAGMA (per R2 M4); 半偏移 cron `15,45 * * * *` 是 primary guard, busy_timeout 是 secondary (manual force trigger 兜底)
- [x] **T5.7** Strategy interface 完整: `Decision` enum {RETRY, FAIL, LEAVE} + `ReconcilerStrategy` Protocol (`reconciler.py`, runtime_checkable, decide(stuck_row) -> Decision) + `select_strategy()` env-driven (`ARIA_RECONCILER_STRATEGY=mechanical(default)|llm`); 'llm' 选项 fail-fast NotImplementedError (M5 forward); unknown 值降级 mechanical + warning. MechanicalReconciler self-bound default (`__init__` 检测 None / sentinel 自绑 self.decide)
- [x] **T5.8** `nomad job validate aria-orchestrator/deploy/aria-layer1-reconcile.nomad.hcl` PASS (Nomad v1.7.7, "Job validation successful"; 唯一 warning `cron is deprecated and may be removed` 与 sister `aria-layer1-cron.nomad.hcl` 同 pattern, hygiene cron→crons sweep 推单独 Spec per AD-M3-5 §风险 #6)
- [x] **T5.9** AD-M3-5 回填 — 2026-05-05 done: `aria-orchestrator/docs/architecture-decisions.md` §AD-M3-5 完整 6 段决议 (决策 7 维度 / 背景 / 11 alternatives / 10 选型理由 / 10 风险 / 4-level 回滚 / 治理影响) + version history 0.9 → 1.0 + proposal.md AD-M3-5 行 cross-reference + 299 tests 0 regression 实测

**T5.done = HCL validate PASS + 三阈值/CAS/Strategy interface 实施 + AD-M3-5 回填**

#### T6 — Reconciler stuck-detection + S_FAIL routing + Feishu (~8h)

- [x] **T6.1** `aria_layer1/reconciler.py` MechanicalReconciler.run() — pipeline (1) `repo.list_stuck_s5_await(cutoff_iso)` (2) `strategy.decide(row)` (3) CAS UPDATE per Decision (`_handle_retry` / `_handle_fail`) (4) Feishu alert on FAIL (5) result aggregation. Result dict: `{stuck_rows_found, retried, failed, left, cas_lost, alerts_sent, alerts_skipped}`.
- [x] **T6.2** `db.list_stuck_s5_await(cutoff_iso)`: SELECT WHERE state='S5_AWAIT' AND (last_heartbeat_at IS NULL OR last_heartbeat_at < cutoff). NULL heartbeat 视作 stuck (alloc never ack'd).
- [x] **T6.3** CAS via `db.cas_increment_attempt` + `db.cas_mark_failed_stuck` (复合版本字段: state + last_heartbeat_at + attempt_count, NULL-safe). Routing matrix `_FAIL_REASON_BY_STATE` in reconciler.py — S2/S3 → TIMEOUT / S4_LAUNCH → DISPATCH_LOST / S5_AWAIT → TIMEOUT / S1/S6/S7/S8 → INFRASTRUCTURE. M2 frozen FailReason enum 无 'stuck' value (per AD-M2-9 frozen enum), 文档化语义对齐: S5_AWAIT → TIMEOUT (elapsed-budget 语义) / S4_LAUNCH → DISPATCH_LOST. Inline comment 三处锚定 reframe (reconciler.py + tasks.md 此条 + AD-M3-5 §决策 #3 footnote).
- [x] **T6.4** `reconcile_runner._build_feishu_client()` — URL resolution per T6.4: (1) `ARIA_FEISHU_OPS_ALERT_WEBHOOK` 优先 → FeishuWebhookClient(ops_url) (2) fallback `ARIA_FEISHU_WEBHOOK_URL` + warning log → FeishuWebhookClient(general_url) (3) 都 unset → None (skip alerts, info log, reconciler 不 block). MechanicalReconciler.feishu Protocol DI; tests inject FakeFeishuWebhook.
- [x] **T6.5** `tests/test_t6_reconciler.py` 18 tests (≥10 target 满足): 4 decide boundary (1/2/3/4 attempt_count) + 4 thresholds/strategy plumbing + 2 stuck scan (S5_AWAIT only, NULL=stuck) + 4 run() body (RETRY CAS / FAIL CAS / fail_reason matrix contract / CAS lost-update rebound) + 2 Feishu (alert sent / skipped when unconfigured) + 2 attempt_history (append / malformed replace). 全 PASS, 0 regression on T5 baseline (299 → 317 total).
- [x] **T6.6** `attempt_history_json` audit log via `MechanicalReconciler._build_history()` — JSON array append, schema `{detected_at, stuck_state, elapsed_min, attempt_count, action_taken}` per AD-M2-9 §forensic + R1-M2. Malformed existing JSON → replaced with single-event array + warning log. CAS UPDATE 同 statement 写入 (atomic, 无 TOCTOU)。
- [x] **T6.7** Dispatch dataclass v2 column coverage — 新增 6 字段 (cycle_start_ts / cycle_end_ts / dispatched_job_id / eval_id / provider_cost_model / attempt_history_json) + `from_row()` 解析. T3 ALTER 已加列, dataclass 同步对齐 (per `feedback_validator_repo_drift_guard_test` schema-code consistency)。

**T6.done = reconciler 三阈值 + 混合路由 CAS + Feishu DI + 18 tests + attempt_history audit + Dispatch dataclass v2 sync**

#### T7 — Crash recovery (~10h, AD-M3-6 触发, OD-3b scope=仅 S5_AWAIT)

- [x] **T7.1** `_handle_s5_await` audit confirm DB-only (M2 已设计无 in-memory): handler 完全读 `ctx.dispatch_row` (DB SELECT 结果) + `repo` (DispatchRepository) + DI clients (alloc_provider / clock); `AriaLayer1Extension` 实例零 in-flight 缓存/dict/set tracking。T7 不改 handler 逻辑, 仅 audit confirm + AD-M3-6 §决策 #2 显式 contract 锚定。
- [x] **T7.2** `alloc_id` + `last_heartbeat_at` 从 `dispatches` 表读 — 通过 `ctx.dispatch_row.get("alloc_id")` + `dispatch_row.get("last_heartbeat_at")`, M2 已实施。T7 audit confirm: alloc_id 在 S4_LAUNCH 期间持久化, S5_AWAIT 进入时已 readable; T7.5 fixture `_insert_s5_await_row` 实证 DB-only 输入路径足够。
- [x] **T7.3** `alloc_provider.get_status(alloc_id)` HTTP re-query — M2 lazy-wire 模式 (per AD-M3-2 §决策 #2): cron runner 设 `ARIA_LAZY_WIRE=1` → `_handle_s5_await` 进入时构造 `NomadAllocHTTPProvider`; 失败异常 catch + log + fall-through 到 stub path。T7 不改 wire 路径。
- [x] **T7.4** 状态分支 — running → leave + heartbeat update / terminated+exit_code==0 → S6_REVIEW / terminated+exit_code!=0 → S_FAIL(CONTAINER_CRASH) / lost → S_FAIL(DISPATCH_LOST) / 未知 ClientStatus → 保守 fallback running + warning. **404 → state='lost' (R1-M9)**: `NomadAllocHTTPProvider._fetch_allocation` raise `_AllocFetchError(http_code=exc.code)`; `get_status` catch 时 `if exc.http_code == 404` → return `{"state":"lost"}` (alloc 已 GC, permanent), 其他 HTTP 错误 → conservative running fallback (transient, per AD-M2-9)。下游 `_handle_s5_await` "lost" 分支已存在 → S_FAIL(DISPATCH_LOST), 0 路由改动。
- [x] **T7.5** Unit tests — `tests/test_t7_crash_recovery.py` 6 tests: 3 NomadAllocHTTPProvider (404 → lost / 500 → running / 无 http_code → running) + 3 _handle_s5_await (DB-only resume → S6_REVIEW / 404-derived lost → S_FAIL(DISPATCH_LOST) / 无 alloc_id → 留态 + heartbeat update)。M2 test `test_integration_http_404_falls_back_to_running` 翻转为 `test_integration_http_404_maps_to_lost` + docstring 显式说明 M2→M3 contract change。0 regression on T6 baseline (317 → 323 total)。
- [x] **T7.6** AD-M3-6 回填 — 2026-05-06 done: `aria-orchestrator/docs/architecture-decisions.md` §AD-M3-6 完整 6 段决议 (决策 7 维度 / 背景 / 8 alternatives / 7 选型理由 / 8 风险 / 4-level 回滚 / 治理影响) + version history 1.1 → 1.2 + proposal.md AD-M3-6 行 cross-reference。

**T7.done = _handle_s5_await DB-only 实施 + unit test + AD-M3-6 回填 (T12 集成 test 收尾)**

#### T8 — `ZhipuClient` (~4h)

- [x] **T8.1** Path reframe (per `feedback_spec_reframe_in_session` + AD-M3-2 §选型 #6): tasks.md 字面 `aria_layer1/clients/zhipu_client.py` → 实际 `aria_layer1/zhipu_client.py` (flat 与 sister forgejo_client / silknode_client / nomad_client 对齐, 无 clients/ 子目录, 与 alloc_status_provider.py / schema_migrate.py 同模式)。stdlib http.client (用于 connect/read timeout 切分; urllib 单一 timeout 不支持) + json + urllib.parse + ssl. ZHIPU_API_KEY / ZHIPU_BASE_URL via os.environ (per `feedback_secrets_never_in_conversation`).
- [x] **T8.2** Base URL: `https://open.bigmodel.cn/api/paas/v4` (POST `/chat/completions`); ZHIPU_BASE_URL env override 支持。
- [x] **T8.3** Auth: `ZHIPU_API_KEY` env (T13 rotation 后 wired); 缺失时 RuntimeError + 错误信息显式指向 .env / Nomad Variables; 测试 `test_missing_api_key_raises_runtime_error` 实证。
- [x] **T8.4** Per-token billing field: result dict 加 `provider="zhipu"` + `provider_cost_model="metered"` (vs Luxeno `subscription_flat`); ProviderRouter T9 + token tracking T10 读这 2 字段做 attribution。
- [x] **T8.5** No-storage contract (OD-3d generalize 适用所有上游 LLM provider, 等 owner Phase A.2 advisory): 模块 docstring 锚定 + logger.warning 仅记 metadata (model + status + body_len + retryable), 不入 prompt content; 测试 `test_logger_does_not_record_prompt_content` 实证 capture 整个 zhipu logger output 不含 prompt 字面。
- [x] **T8.6** Timeout policy (per R1-I1 hard ceiling, OD-3g default): `CONNECT_TIMEOUT_SECONDS=5` + `READ_TIMEOUT_SECONDS=60` 模块常量; `http.client.HTTPSConnection(timeout=connect_timeout)` 后 `conn.sock.settimeout(read_timeout)` 切分 connect 与 read budget; `ZhipuTimeout(phase, seconds)` 区分 connect vs read 触发点 (caller can route差异化 retry 策略); 单层 — ProviderRouter T9 自有 retry/fallback。两测试 `test_call_llm_connect_timeout_raises_zhipu_timeout` + `..._read_timeout_...` 实证。
- [x] **T8.7** Unit tests `tests/test_t8_zhipu_client.py` 11 tests (T8.7 ≥7 target 满足): 3 success/parsing (zhipu metadata / token usage / provider_cost_model='metered') + 3 HTTP errors (500 retryable / 429 retryable / 400 non-retryable) + 2 timeout (connect / read) + 3 config/Protocol/no-storage (missing key / Protocol conformance / logger no-prompt). 0 regression on T7 baseline (323 → 334 total)。

**T8.done = ZhipuClient 实施 + 契约 1 no-storage + ≥7 tests**

#### T9 — `ProviderRouter` + multi-model + dict fallback_chain_json (~14h, AD-M3-4 触发, OD-12 §Q1=D')

- [x] **T9.1** Path reframe (per `feedback_spec_reframe_in_session` + AD-M3-2 §选型 #6 + T8 reframe): `aria_layer1/provider_router.py` (flat 与 sister silknode_client / zhipu_client / forgejo_client / nomad_client 对齐, 无 llm/ subdir). ProviderRouter class — DI: luxeno (SilknodeClient Protocol) + zhipu (optional) + sleep (test injection) + retry_backoffs + retries_per_provider; satisfies SilknodeClient Protocol via `call_llm(prompt, model)` (Protocol-compatible drop-in for self._silknode slot); also exposes `route_for_state(prompt, state)` 便捷 API。
- [x] **T9.2** Provider chain: Luxeno (primary, flat sub) → Zhipu (fallback, per-token); 3 次 expo backoff (1s/2s/4s) `RETRY_BACKOFF_SECONDS` 模块常量, 测试零 wait via `sleep=lambda _:None`; intra-provider 4 attempts (initial + 3 retries) 后 retries 耗尽 → 切下一 provider; 任一 provider 出 non-retryable 错误 (4xx-other) 直接跳下个 provider 不重试 (per `feedback_pre_merge_4round_convergence_template` 类似耗尽语义).
- [x] **T9.3** State-aware primary model `STATE_PRIMARY_MODEL` 模块常量 (per OD-12 §Q1=D'): S2_DECIDE → glm-4.5-air, S3_BUILD_CMD → glm-5-turbo, S6_REVIEW → glm-5.1. Handler call site: S2 unchanged glm-4.5-air, S3 改 "glm-4.5-air" → "glm-5-turbo", S6 `call_review` 加 `primary_model="glm-5.1"`.
- [x] **T9.4** Per-state degrade ladder `MODEL_DEGRADE_LADDER` 常量: glm-5.1 → glm-5-turbo → glm-4.5-air (3-tier S6); glm-5-turbo → glm-4.5-air (2-tier S3); glm-4.5-air → 单层 (terminal, S2 cheapest tier). 降级触发: 当前 tier 在所有 provider 均耗尽 → quality_degrade marker entry → 下一 tier。
- [x] **T9.5** fallback_chain_json dict-array (R1-C2 enum strict 实施): 字段 {provider, model, outcome, reason, latency_ms, ts}; outcome enum {ok, http_5xx, http_429, http_4xx, timeout, network_error, quality_degrade}; provider enum {luxeno, zhipu, **router**} (router 是 synthetic kind, 仅 quality_degrade 跨 tier 转移 marker 用; R1-C2 文档化扩展, AD-M3-4 §决策 #5 锚定 + tests/test_t9_provider_router.py `test_provider_enum_includes_router_for_synthetic_entries` 实证); intra-provider retry 每次都写 entry (per R1-M6).
- [x] **T9.5b** fallback_triggered 写入点 (per R1-M4): ProviderRouter `_finalize_success` 在 chain 闭环时计算 (any non-ok entry → True); result dict 透出 `fallback_triggered` boolean; M2 `repo.update_token_usage(fallback_triggered=...)` API 直接消费, 0 改 token tracking 层 (router I/O-narrow). Tests `test_fallback_triggered_false_on_clean_success` + `..._true_after_any_non_ok` 实证.
- [x] **T9.6** Handler wiring via `extension._ensure_silknode_wired()` lazy-wire 助手 — production `ARIA_LAZY_WIRE=1 + LUXENO_API_KEY` set → 构造 LuxenoSilknodeClient + (optional ZHIPU_API_KEY) ZhipuClient → wrap ProviderRouter → 装 `self._silknode` slot (Protocol-compatible drop-in); 测试不设 env, 直接 `silknode=` DI 注入 ScriptedClient/FakeSilknodeClient 走相同 Protocol 路径 (M2 测试 0 改); S2/S3/S6 handler entry 调 `_ensure_silknode_wired()`. Reframe per `feedback_spec_reframe_in_session`: tasks.md 字面 "替换为 ProviderRouter" 实施实质等价 (silknode slot 现指向 router 实例), AD-M3-4 §决策 #7 + 风险 #10 锚定。
- [x] **T9.7** Test matrix `tests/test_t9_provider_router.py` (T9.7 ≥12 target — 19 tests landed): Path 1 Luxeno-only-success ×3 states (S2/S3/S6) + Path 2 retry-then-ok / Path 3 Luxeno→Zhipu fallback (5xx exhaust + 429 retry) ×2 + Path 4 quality_degrade 5.1→5-turbo + full-ladder-exhausted raises ×2 + Path 5 4xx no-retry skip-to-zhipu + 4xx both raises ×2 + Schema strict (dict keys / outcome enum / router synthetic provider) ×3 + fallback_triggered (clean false / non-ok true) ×2 + Misc (Protocol conformance / route_for_state / no-zhipu / unknown-model) ×4. ScriptedClient deque 配置错误时 `AssertionError("ScriptedClient ran out")` 显式抛 (per R1-C2 严格性); 0 regression on T8 baseline (334 → 353 total).
- [ ] **T9.8** Multi-model benchmark (~8h subset of T9) — **OWNER-BLOCKED** per OD-3e default (exploratory 不阻塞合并) + R1-I9 ($5 budget cap 显式 approval 必需) + T13 (ZHIPU_API_KEY rotation 必需). 当 owner 启用时: 3 模型 × 同 prompt 重复 3 次 = 9 次/state, S2 ≥80% / S3 ≥90% / S6 ≥66% 三轮 review 多数票. 决策本体 (T9.1-T9.7+T9.10) 不依赖 benchmark 结果, 即使延期至 M4 也仅影响 acceptance D 子条目, 不破坏 ProviderRouter 实施.
- [ ] **T9.9** Benchmark 结果写入 m3-handoff.yaml — owner-blocked 与 T9.8 联动. m3-handoff 已留 `multi_model_benchmark_gate` field hook (default false = exploratory). 未跑则字段保 default, M3 acceptance D 仍可标 PASS-with-deferred.
- [x] **T9.10** AD-M3-4 回填 — 2026-05-06 done: `aria-orchestrator/docs/architecture-decisions.md` §AD-M3-4 完整 6 段决议 (决策 8 维度 / 背景 / 13 alternatives / 9 选型理由 / 10 风险 / 4-level 回滚 / 治理影响) + version history 1.2 → 1.3 + proposal.md AD-M3-4 行 cross-reference. T9.8/T9.9 owner-blocked 状态显式记录在 §状态 + §决策 #8 + §风险 #1 三处。

**T9.done = ProviderRouter 实施 + multi-model state-aware + dict fallback + ≥12 test matrix + benchmark + AD-M3-4 回填**

#### T10 — Per-provider token breakdown (~4h, AD-M3-7 触发, R2 C1)

- [x] **T10.1** `repo.update_token_usage` 加 additive `provider: str | None = None` param (M2 backward compat, default None preserves migration 002 backfill column value); provider="luxeno" → write provider_cost_model='subscription_flat' / provider="zhipu" → 'metered' / None → leave column unchanged. Cumulative semantics 不变 (token_usage_input/output/cost_usd accumulate per R2 I3).
- [x] **T10.2** S2/S3 token wiring via `extension._persist_llm_usage()` 助手 (best-effort, swallows persistence errors per observability-not-correctness 原则); _handle_s2_decide + _handle_s3_build_cmd capture LLM `result =` (was `_result =` discarded) + 调 `_persist_llm_usage`. `usage_from_silknode_response` helper 已透明支持 Zhipu (response.usage shape `{input_tokens, output_tokens}` 已 in T8 ZhipuClient `_parse_response` 标准化, 与 silknode 透传一致 — 无需 ZhipuTokenAdapter); helper 自动读 `response.get("provider")` default "luxeno" (M2 silknode legacy 兼容). S6_REVIEW already-wired path 加 `provider=verdict.provider` arg (T10.2 collateral via ReviewVerdict.provider field).
- [x] **T10.3** Path reframe (per `feedback_spec_reframe_in_session` + AD-M3-2 §选型 #6 + T8/T9 reframe): `aria_layer1/zhipu_pricing.py` (flat 与 sister silknode_client / zhipu_client / provider_router / token_tracking 对齐, 无 llm/ subdir). 模块 _PRICING dict 4 行 (glm-4.5-air / glm-4.7 M2 baseline + glm-5-turbo / glm-5.1 M3 GLM-5 tier AI snapshot estimates). 元数据常量: `_PRICING_VERSION='1.0'` + `_PRICING_FETCHED_AT='2026-05-06'` + `_PRICING_SOURCE='open.bigmodel.cn public price page'` + `_PRICING_REVIEW_DUE='2026-11-06'` (6-month review trigger per R1-I7) + `_PRICING_OWNER_VERIFIED=False` (待 owner OD-3f 拍板). `compute_cost(provider=...)` 三 branch: luxeno → 0.0 / zhipu → 委托 `compute_zhipu_cost` / None → legacy M2 `_PRICING` 表 (KeyError on unknown). Zhipu `_parse_response` 已透传 `usage.input_tokens/output_tokens` 字段 (T8 实施), 无 ZhipuTokenAdapter 需要.
- [x] **T10.4** `aria-orchestrator/docs/m3-handoff.yaml` T10 stub 落地 (T16.1 expand 完整 schema 时 only-add 不改字段名, per AD-M2-7 placeholder discipline). 4 个 T10 锚定字段: `cost_attribution.luxeno_subscription_baseline_usd_monthly` (owner monthly bill) + `cost_attribution.zhipu_metered_usd_total` (T16.4 DB sum) + `cost_attribution.zhipu_pricing_version` + `cost_attribution.zhipu_pricing_review_due` (1.0 / 2026-11-06). 加 stub 还含 multi_model_routing_benchmark 块 (T9.8/T9.9 owner-blocked) + secret_rotation 块 (T13) + performance_vs_m1 块 (T14) + acceptance 块 (T15) + go_decision (T16.4) + sign-offs (T16.4) + carryover_to_m4 (T16.4)。
- [x] **T10.5** `tests/test_t10_provider_token_breakdown.py` 13 tests (T10.5 ≥4 target 大幅满足): 3 update_token_usage provider column writes (luxeno → subscription_flat / zhipu → metered / None preserves backfill) + 5 compute_cost branch (luxeno=0 / zhipu metered / zhipu unknown returns 0+log / legacy uses _PRICING / legacy unknown raises KeyError) + 1 cumulative S2+S3+S6 within dispatch (R2 I3 实证 token cumulate + last-write-wins on provider_cost_model) + 2 helper Zhipu compat (provider field read / default luxeno when absent) + 1 m3-handoff stub presence + 1 pricing snapshot metadata. 0 regression on T9 baseline (353 → 366 total)。
- [x] **T10.6** AD-M3-7 回填 — 2026-05-06 done: `aria-orchestrator/docs/architecture-decisions.md` §AD-M3-7 完整 6 段决议 (决策 9 维度 / 背景 / 14 alternatives / 9 选型理由 / 8 风险 / 4-level 回滚 / 治理影响) + version history 1.3 → 1.4 + proposal.md AD-M3-7 行 cross-reference. **AD-M3-1..7 全部 Decided** (七连即时回填闭环, 不积压到 T16, per `feedback_ad_slot_backfill_checkpoint`)。

**T10.done = signature 改 + S2/S3/S6 全 wired + Luxeno=0 / Zhipu metered branch + handoff fields + AD-M3-7 回填**

#### T11 — Nomad integration 加固 (~8h)

- [x] **T11.1** Idempotency contract verified by 3 tests on `derive_dispatch_id` (M2 deterministic SHA derivation): same (issue_id, attempt_count) → identical dispatch_id (Nomad-level dedupe contract); same value used for both DISPATCH_ID and IDEMPOTENCY_KEY meta keys per AD-M3-1 §决策 #4 双层 idempotency; different attempt_count → distinct dispatch_id (reconciler T6 attempt_count++ produces fresh dispatch).
- [x] **T11.2** Cross-alloc retry semantics verified by 2 tests: alloc state="lost" → S_FAIL(DISPATCH_LOST), attempt_count unchanged; alloc state="terminated" exit_code=137 → S_FAIL(CONTAINER_CRASH), attempt_count unchanged. Reconciler 单源 contract (per AD-M3-5) — handler MUST NOT auto-increment attempt_count even on terminal alloc failure.
- [x] **T11.3** M1_VALIDATOR_PATH Nomad Variable wiring (per R2 M6) in `aria-orchestrator/deploy/aria-layer1-cron.nomad.hcl`: env block default `/opt/aether-volumes/aria-layer1/data/validate-issue-schema.py` (host volume on light-1 raw_exec) + new template stanza `secrets/aria-validator.env` rendering `M1_VALIDATOR_PATH={{ .M1_VALIDATOR_PATH }}` from Nomad Variable `nomad/jobs/aria-orchestrator` key when set (template-injected env wins over env-block default per Nomad precedence). Owner overrides via `nomad var put nomad/jobs/aria-orchestrator M1_VALIDATOR_PATH=...`. `nomad job validate` PASS (only pre-existing cron deprecation warning, shared with sister cron). Path "container 内 bind mount" reframe per `feedback_spec_reframe_in_session`: cron HCL uses raw_exec on light-1, no docker container — file is on host filesystem at the configured path, accessed via `importlib.util.spec_from_file_location` per `extension._load_m1_issue_validator`.
- [x] **T11.4** alloc_provider HTTP error log severity refinement: 404 → warning + state="lost" (T7 done); 4xx-other (400/401/403) → **error** + state="running" (auth/permission likely permanent config issue, ops attention); 5xx / timeout / URL / JSON / no http_code → warning + state="running" (transient blip). Behavioral semantics unchanged from M3 T7 (still single-shot conservative fallback for non-404); only log level changes for 4xx-other. Internal retry remains at ProviderRouter (T9) and reconciler (T6) layers per AD-M3-2 §决策 #4 alloc_provider I/O-narrow design — T11.4 spec "5xx exponential backoff (3 次)" already lives at those higher layers, NOT at provider HTTP boundary.
- [x] **T11.5** Unit tests `tests/test_t11_nomad_integration_hardening.py` 11 tests (T11.5 ≥8 target 满足): 3 idempotency (deterministic / IDEMPOTENCY_KEY=DISPATCH_ID / attempt_count distinct) + 2 cross-alloc (lost / container_crash, attempt_count unchanged) + 2 HCL Nomad Var (default in env / template stanza renders nomadVar) + 4 HTTP error policy (404 → lost+warning / 4xx-other → running+error ×3 codes 400/401/403 / 5xx → running+warning / no-http-code → running+warning). 0 regression on T10 baseline (366 → 377 total).

**T11.done = idempotency 双重 verify + retry semantics 锁定 + M1_VALIDATOR_PATH Nomad Var + ≥8 tests**

#### T12 — Reconciler + crash recovery integration tests (~8h, R2 C2 + R2 I9)

- [ ] **T12.1** Named test `test_t12_crash_recovery_s5_await_auto_resume` (per R2 C2):
  - Step 1: pre-seed dispatches.db 1 row `state=S5_AWAIT, alloc_id='alloc-test-001', dispatched_at=now-30s`
  - Step 2: fresh hermes-extension instance (kill + restart simulation)
  - Step 3: tick (cron simulate)
  - Step 4: assert `_handle_s5_await` fired (DB-only, no in-memory)
  - Step 5: assert state advances (running mock alloc → S6_REVIEW prep)
- [ ] **T12.2** Reconciler concurrent test (per R2 I9): cron tick + reconciler 同 row 同 ts; verify CAS lost-update detected (BEGIN IMMEDIATE 序列化, 一方 win + 另一方 retry once → lost)
- [ ] **T12.3** Reconciler 三阈值 boundary tests (各阈值 ±1 内/外, ≥6 tests)
- [ ] **T12.4** Hermes kill -9 lock test (per R1-I3 harness 设计明示 + Q-NEW-1 owner 确认 unit vs integration):
  - **AI 推荐 default = unit (subprocess+SIGKILL)** (Tier-1 sufficient per Q6=A; Tier-2 live Hermes 推 T15 stretch)
  - 实施 (default unit path): `subprocess.Popen(['python', '-m', 'aria_layer1.tick_runner'])` 启动 fresh hermes-extension 子进程 → mid-S5_AWAIT 时 `os.kill(pid, signal.SIGKILL)` → 重启相同 cmd → 5-step pattern (per T12.1) verify _handle_s5_await DB-only resume
  - Fixture: FakeAllocStatusProvider injection via env var (subprocess 继承)
  - 若 owner 选 integration: 推 T15 stretch, 加 ~6h Tier-2 cluster smoke
- [ ] **T12.5** MockClock fast-forward 验 60min boundary 不需真等

**T12.done = crash recovery named test (5 步) PASS + reconciler concurrent CAS test PASS + 三阈值 boundary tests + kill -9 lock test PASS**

---

### Phase B.2.Z — E2E + handoff (T13-T16, ~30h)

#### T13 — Secret rotation execution (~3h, OD-12 §Q8d)

- [ ] **T13.1** 一次性 rotate 全 5 keys: LUXENO_API_KEY + 3 FEISHU_* + ZHIPU_API_KEY (per SOP `.aria/decisions/2026-05-02-secret-rotation-deferred.md`)
- [ ] **T13.2** Nomad Variables 更新 (per `feedback_secrets_never_in_conversation` 不出现在对话)
- [ ] **T13.3** Hermes 重启 + 验证 token usage 正常
- [ ] **T13.4** post-rotation perf benchmark trigger (T14 顺便 run, 验证新 keys 有效)
- [ ] **T13.5** m3-handoff.yaml `secret_rotation_completed=true` + date

**T13.done = 5 keys rotated + Nomad Var 更新 + post-rotation T14 benchmark trigger + handoff field 填**

#### T14 — Perf benchmark vs M1 baseline (~6h, 验收 B post-rotation)

- [ ] **T14.1** 触发 ≥10 cycle 走完整 S0→S9_CLOSE (Tier-1 fake-cycle test, 复用 T15 fixtures)
- [ ] **T14.2** 计算 p50: `median(cycle_end_ts - cycle_start_ts) WHERE state='S9_CLOSE' AND fallback_triggered=false`
- [ ] **T14.3** 阈值: `m1_demo_002_p50_s × 1.5 = 31.5 × 1.5 = 47.25s`
- [ ] **T14.4** PASS (p50 ≤ 47.25s) → 写 m3-handoff `performance_vs_m1.passed=true` + p50 实测值
- [ ] **T14.5** Methodology field: `performance_vs_m1.m3_p50_methodology = "S1_SCAN→S9_CLOSE wall + fallback_triggered=false filter"` (per Q7=C)
- [ ] **T14.6** post-rotation flag: `performance_vs_m1.measured_post_rotation=true` (Q8d 复用)

**T14.done = ≥10 cycle p50 ≤ 47.25s + handoff fields filled + methodology recorded**

#### T15 — ≥10 issue full cycle Tier-1 集成 (~10h, 验收 A+B+D+E)

- [ ] **T15.1** Tier-1 fake-cycle test harness (Fixture 复用 M2: FakeAllocStatusProvider + FakeNomadClient + FakeSilknodeClient + 新增 FakeZhipuClient per Q1=D')
- [ ] **T15.2** ≥10 issue trigger end-to-end S0→S9_CLOSE (验收 A)
- [ ] **T15.3** Validation: `count(state=S9_CLOSE) ≥ 10` query PASS
- [ ] **T15.4** 验收 D: fallback_chain_json 含 luxeno + zhipu 两类 entry (≥1 cycle 模拟 Luxeno 5xx → Zhipu 接管)
- [ ] **T15.5** 验收 E: 11-row dispatches.db 真实 fixture (T15.3 M2 实际数据) migration test → 0 数据丢失
- [ ] **T15.6** m3-handoff.yaml `acceptance_a_actual_dispatches=10` + `acceptance_d_fallback_observed=true` + `acceptance_e_migration_zero_loss=true`
- [ ] **T15.7** Tier-2 cluster verification (embedded in T1 implementation per Q6=A, 不强制单独 gate)
  - **Falsifiable evidence (per R1-I4)**: `acceptance_a_tier2_carryover_verified=true` 必须有可验证 metric — **≥1 dispatches.db row WHERE `dispatched_job_id IS NOT NULL AND eval_id IS NOT NULL`** (T1.OWNER sample dispatch 后)
  - 不强制 multi-row, 但 0-row 则 validator FAIL_FAST (防 boolean true 无下层证据)

**T15.done = ≥10 issue full cycle PASS + 验收 A+D+E 全 documented + handoff fields filled**

#### T16 — Closeout: m3-handoff.yaml + AD backfill + Report + Spec archive (~6h)

- [ ] **T16.1** `aria-orchestrator/docs/m3-handoff.yaml` schema v1.0 (additive-only on m2-handoff schema, per AD-M2-7 plugin.yaml + OD-9 + OD-5c fail_reason 不重写)
  - **Acceptance fields enumerate (per R1-I2)**: 6 验收必备 fields:
    - `acceptance_a_actual_dispatches: int` (≥10)
    - `acceptance_a_tier2_carryover_verified: bool` (per R1-I4 falsifiable evidence)
    - `acceptance_b_p50_passed: bool` + `acceptance_b_p50_actual_s: float` + `acceptance_b_methodology: str` + `acceptance_b_measured_post_rotation: bool`
    - `acceptance_c_crash_recovery_test_passed: bool` (per R1-I2 missing field)
    - `acceptance_d_fallback_observed: bool` + `acceptance_d_test_matrix_count: int`
    - `acceptance_e_migration_zero_loss: bool` + `acceptance_e_fixture_rows: int`
    - `acceptance_f_rotation_completed: bool` + `acceptance_f_rotation_date: str`
- [ ] **T16.2** `validate-m3-handoff.py` (stdlib, ≥15 checks per R1-I2, fail-fast on AD-M3-1..7 `_待回填_` per R1-M5 spillover sentinel exception):
  - **6 acceptance truthy assertions** (per `feedback_smoke_benchmark_truthiness`): `acceptance_*.passed is True` (boolean, 不仅 key-present)
  - **AD slot fail-fast** (per R1-M5): grep `_待回填_` only in AD-M3-1..7 范围, AD-M3-8/9/10 `_spillover_` 字面值跳过 (实际未用则 status 改 `_unused_`)
  - validator 自身 drift guard test (per `feedback_validator_repo_drift_guard_test`): committed canonical instance 通过 validator
- [ ] **T16.3** AD-M3-1..7 回填 (per `feedback_ad_slot_backfill_checkpoint`); validator fails if any `_待回填_`
- [ ] **T16.4** 4 PRD patches commit at T16.4 (Patch 01 已在 A.3.2 OD-13 立 commit per R1-I5 reword; T16.4 仅 commit Patches 02-05):
  - ~~Patch 01: PRD §M3 工时 90→185h (OD-13)~~ — **已在 A.3.2 commit, T16.4 不重复**
  - Patch 02: 'dual provider' → 'multi-model GLM routing + cross-provider HA fallback' (Q1=D')
  - Patch 03: 验收 A → Tier-1 + carryover #1 cluster verification embedded (Q6=A)
  - Patch 04: 验收 B → 47.25s + S1_SCAN→S9_CLOSE wall + fallback filter (Q7=C)
  - Patch 05: 验收 D/E/F 显式化
- [ ] **T16.5** `aria-orchestrator/docs/m3-report.md` (M2 风格, ≤2 页): go_decision / e2e_passed / metrics / lessons learned / handoff link
- [ ] **T16.6** tech-lead co-sign (AI-drafted per AD-M0-9 with provenance) + owner sign-off
- [ ] **T16.7** Spec archive: `mv openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery openspec/archive/<closeout-date>-aria-2.0-m3-cycle-close-glm-routing-recovery`
- [ ] **T16.8** Submodule branch verify (per `feedback_submodule_branch_before_archive`): aria-orchestrator submodule pointer 在 master, 不在 feature 分支
- [ ] **T16.9** Status: Approved → Done — Archived (proposal.md 改 status 字段)

**T16.done = m3-handoff validator PASS + AD-M3-1..7 全回填 + 5 patches committed + m3-report.md + signoffs filled + Spec archived**

---

## Phase C: 集成

- [ ] **C.1.1** strategic-commit-orchestrator: per-task commit (M2 mode)
- [ ] **C.2.1** Phase C.2 dual-push (origin + github) per CLAUDE.md, post-push SHA verify
- [ ] **C.2.2** PR 创建 (Forgejo + GitHub): feature/aria-2.0-m3-cycle-close-glm-routing-recovery → master
- [ ] **C.2.3** PR review + merge (owner action; submodule pointer first per multi-remote SOP)

---

## Phase D: 收尾

- [ ] **D.1.1** UPM 进度更新: N/A for Aria (按 standards/core/progress-management/ Aria 自身不 active UPM)
- [ ] **D.2.1** Spec archive 完成 (T16.7 已动)
- [ ] **D.2.2** US-023 Status: Approved Pending → done (M3 closeout)
- [ ] **D.2.3** PRD §M3 状态 → done
- [ ] **D.2.4** Memory 更新: `project_aria_m3_closeout_<date>.md` (M2 mode)

---

## Phase 依赖图 (per OD-12 §Spec 内 phase 排序)

```
A.1 ─→ A.2 ─→ A.3 ─→ B.1 ─→ B.2.0 (T1-T4 carryover) ─┐
                                                       ├─→ B.2.Z (T13-T16) ─→ C ─→ D
                              B.2.1 (T5-T12 new) ─────┘

T1 (HCL) ─→ T2 (alloc_provider) ─→ T3 (schema v2) ─→ T4 (smoke)
T5 (reconciler HCL) ─→ T6 (reconciler logic)
T7 (crash recovery) ──→ T12 (integration tests, 含 crash recovery test harness)
T8 (ZhipuClient) ─→ T9 (ProviderRouter)
T10 (token breakdown) 独立, 复用 T9 ProviderRouter wire
T11 (Nomad 加固) 独立, T1+T2 后

T13 (secret rotation) ─→ T14 (perf bench) ─→ T15 (≥10 cycle) ─→ T16 (handoff + report + archive)
```

## 状态汇总

| Phase | 任务 | 估时 | 状态 |
|---|---|---|---|
| A.0 | 状态扫描 + brainstorm R1+R2 | (DONE 2026-05-03) | ✅ |
| A.1 | proposal.md + tasks.md + 5 patches | 12h | ✅ A.1.1-4 done (2026-05-04); A.1.5 Forgejo Issue 推 A.3 |
| A.2 | post_spec audit R1+R2 (R3+R4 collapsed per OD-15) | 4h | ✅ R1+R2 both done 2026-05-04 (R1: 18 findings 全 closeable + 7 OD; R2: SCOPE_OK_R2 4/4 + 0 critical) |
| A.3 | OD-12 lock + OD-13 + Approved + Agent assign | 1h | ✅ done 2026-05-04 (PRD patches applied + Status Approved + AD agent column 回填) |
| B.1 | feature 分支 + dual push | 0.5h | ✅ done 2026-05-05 (state-snapshot `overall_parity=true`) |
| B.2.0 | M2 carryover (T1-T4 + T13 pull-forward per OD-14) | 24h | ⏳ T1+T2+T3 done 2026-05-05 (实际 ~5.5h vs ~13h baseline = 7.5h 节省); T4 blocked by T1.OWNER + T13 (异步 owner action) |
| B.2.1 | M3 new scope (T5-T12) | 90h | ⏳ |
| B.2.Z | E2E + handoff (T14-T16, T13 已拉前) | 27h | ⏳ |
| C+D | 集成 + 归档 | (含 buffer 17h) | ⏳ |
| **Total** | | **185h** | |

> **Status table 数学 reconcile (per R1-I6)**: A.1+A.2+A.3+B.1+B.2.0+B.2.1+B.2.Z = 12+4+1+0.5+24+90+27 = **158.5h** 显式; OD-12 §Q2 baseline 168h subtotal **含 25h audit overhead** (Phase A.2 4h 显式 + Phase B.2 scope-bounded ~16h 隐含在 B.2.0/B.2.1/B.2.Z hours + Phase D 4-round ~5h 在 C+D 17h buffer 内); 17h buffer 在 C+D 行隐含 → 158.5+17+9.5 audit absorbed = 185h. R2 audit reconcile gap 0.

## 引用

- proposal.md (本 Spec): `./proposal.md`
- US-023.md: `../../../docs/requirements/user-stories/US-023.md`
- OD-12 RESOLVED: `../../../.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- R2 closeout: `../../../.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md`
- M2 archived: `../../archive/2026-05-03-aria-2.0-m2-layer1-state-machine/`
- m2-handoff.yaml: `../../../aria-orchestrator/docs/m2-handoff.yaml`
- secret_rotation_deferred SOP: `../../../.aria/decisions/2026-05-02-secret-rotation-deferred.md`
