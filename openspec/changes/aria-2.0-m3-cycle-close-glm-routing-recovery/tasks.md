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
- [ ] **T1.9** AD-M3-1 回填 (HCL meta keys + image pin 决策 + registry domain owner-decision)
- [ ] **T1.OWNER** Owner action: (a) 确认 image registry domain (registry.10cg.pub 新建 vs 沿用 forgejo.10cg.pub); (b) `nomad var put nomad/jobs/aria-layer2-runner ...` 8 secrets (T13 rotation 后); (c) `nomad job run aria-layer2-runner.hcl` on Aether (~30min, verify alloc launch)

**T1.done = HCL validate PASS + Aether 部署成功 + sample dispatch 实测 alloc state 推进 + AD-M3-1 回填**

#### T2 — `NomadAllocHTTPProvider` 生产化 (~4h, AD-M3-2 触发, R2 C3)

- [ ] **T2.1** 实施 `aria_layer1/clients/alloc_status_provider.py` `NomadAllocHTTPProvider` class
- [ ] **T2.2** `AllocStatusProvider` Protocol 实施 (M2 同 contract per AD-M2-9)
- [ ] **T2.3** HTTP GET `/v1/allocation/{alloc_id}` (Nomad API, base_url 走 `NOMAD_ADDR` Nomad Variable)
- [ ] **T2.4** 30s ack-poll budget (M2 fake-only → M3 真实化, 30s 超时则留状态 reconciler 处理)
- [ ] **T2.5** alloc states 映射 Layer 1 transition (per OD-12 §Q3): `pending|queued` → 不动 / `running` → S6 prep / `complete` → S6_REVIEW / `failed` → S_FAIL(layer2_runner_failed) / `lost` → S_FAIL(alloc_lost)
- [ ] **T2.6** **Lazy-wire 注入** (per R2 C3 + OD-3c): `tick_runner.py` 内 `if os.environ.get("ARIA_LAZY_WIRE") == "1": self._alloc_provider = NomadAllocHTTPProvider()` (ForgejoCliClient + NomadDispatchClientHTTP pattern 一致)
- [ ] **T2.7** Unit tests: 5 alloc state mapping + lazy-wire 注入 + Protocol contract assert (≥8 tests)
- [ ] **T2.8** Integration test: testing-mock Nomad HTTP (httpx mock or local nomad agent dev mode), 3 状态 round-trip
- [ ] **T2.9** AD-M3-2 回填 (lazy-wire + Protocol contract 决策)

**T2.done = NomadAllocHTTPProvider class 实施 + Protocol assert + ARIA_LAZY_WIRE=1 注入测试 + Nomad mock integration test PASS + AD-M3-2 回填**

#### T3 — Schema migration v2 (~3h, AD-M3-3 触发, R2 I4 + R2 M3 + R2 M5 + R1-C1/M2/M3)

- [ ] **T3.1** Migration script `aria-orchestrator/migrations/002_schema_v2_additive.sql`:
  - **Pre-condition (R1-C1)**: 验 v1 fixture 已含 `fallback_triggered INTEGER NOT NULL DEFAULT 0` (M2 schema.sql:85 实证); fail-fast if missing
  - `ALTER TABLE dispatches ADD COLUMN cycle_start_ts TEXT`
  - `ALTER TABLE dispatches ADD COLUMN cycle_end_ts TEXT`
  - `ALTER TABLE dispatches ADD COLUMN dispatched_job_id TEXT`
  - `ALTER TABLE dispatches ADD COLUMN eval_id TEXT`
  - `ALTER TABLE dispatches ADD COLUMN provider_cost_model TEXT`
  - `ALTER TABLE dispatches ADD COLUMN attempt_history_json TEXT` (per R1-M2, T6.6 reconciler stuck event log)
  - `CREATE TABLE IF NOT EXISTS migration_notes (key TEXT PRIMARY KEY, note TEXT, applied_at TEXT)` (per R1-M3, backfill placeholder audit trail)
  - `INSERT INTO schema_meta VALUES ('fallback_chain_outcome_enum', '["ok","http_5xx","http_429","http_4xx","timeout","network_error","quality_degrade"]')` (per R1-C2 self-doc, future audit drift detect)
- [ ] **T3.2** `fallback_chain_json` write-time exhaustive transform (per R2 I4): UPDATE all v1 字符串数组 → v2 dict array, 同 ALTER 同 transaction
- [ ] **T3.3** `INSERT INTO schema_meta VALUES ('schema_version', '2.0')`
- [ ] **T3.4** Backfill rules:
  - 历史 row `provider_cost_model = 'subscription_flat'` (per AD-M1-12 Luxeno-only, R2 M3)
  - 历史 S9_CLOSE / S_FAIL row `cycle_start_ts = state_entered_at` (per R2 M5, 显式 placeholder 注 in `migration_notes` table)
- [ ] **T3.5** Migration runner: 启动时自动检查 schema_version 升级 (与 M2 SchemaInitializer 集成); ALTER 失败 SQLite 自动回滚
- [ ] **T3.6** Test fixture: T15.3 真实 11-row dispatches.db 快照 (per qa R1 OBJ-5 CanonicalDispatchesDB pattern)
- [ ] **T3.7** Unit + integration tests: migration apply on fixture → 0 数据丢失 + 6 新 col present + migration_notes table created + schema_meta outcome_enum entry + dict fallback round-trip + backfill rules applied + R1-C1 fallback_triggered pre-condition assertion (≥12 tests)
- [ ] **T3.8** **inline UNIQUE constraint (`schema.sql:98`) 保留** (drop 推 schema v3 / M4) — 应用层 dedupe 续用
- [ ] **T3.9** Drift guard test (per `feedback_validator_repo_drift_guard_test`): committed schema.sql 通过 migration 等价 production
- [ ] **T3.10** AD-M3-3 回填 (schema v2 additive 决策 + fallback_chain transform 时机)

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

- [ ] **T5.1** HCL `aria-orchestrator/jobs/aria-layer1-reconcile.nomad.hcl`: Nomad periodic job, cadence 30min (cron 60min 中点跑)
- [ ] **T5.2** 同 docker image 不同 entry-point: `aria-layer1-reconcile` CLI
- [ ] **T5.3** 三阈值 default (per OD-12 §Q3): `max_age_at_S5_AWAIT_minutes=60` / `max_total_attempts=3` / `stuck_alloc_states=('pending', 'queued')`
- [ ] **T5.4** 路由策略: 混合 — Attempt 1-2: `attempt_count++` (let next cron tick retry) / Attempt 3: S_FAIL(stuck) terminal
- [ ] **T5.5** CAS 锁 (per OD-12 §Q4 + R2 I5): `UPDATE ... WHERE rowid=X AND state='S5_AWAIT' AND last_heartbeat_at=? AND attempt_count=?` (compound 版本字段)
- [ ] **T5.6** SQLite WAL + `PRAGMA busy_timeout=5000` (per R2 M4); CAS 失败 retry 1 次 (lost = let cron win)
- [ ] **T5.7** Strategy interface (M5 LLM-decided 升级预留): env `ARIA_RECONCILER_STRATEGY=mechanical|llm` 切换 1 行 + **`ReconcilerStrategy` Protocol stub** (per R1-M8): `decide(stuck_row: DispatchRow) -> Decision` 返回 enum `{RETRY, FAIL, LEAVE}`
- [ ] **T5.8** `nomad job validate` HCL pre-deploy
- [ ] **T5.9** AD-M3-5 回填 (reconciler design 决策)

**T5.done = HCL validate PASS + 三阈值/CAS/Strategy interface 实施 + AD-M3-5 回填**

#### T6 — Reconciler stuck-detection + S_FAIL routing + Feishu (~8h)

- [ ] **T6.1** `aria_layer1/reconciler.py` MechanicalReconciler class
- [ ] **T6.2** Detect stuck S5_AWAIT row (per 三阈值)
- [ ] **T6.3** Route: attempt_count<3 → CAS UPDATE attempt_count++ / attempt_count=3 → CAS UPDATE state='S_FAIL'; **stuck reason routing matrix (per R1-M10)**: S2/S3 → fail_reason='timeout' / S4/S5 → fail_reason='stuck' / S1/S6/S7/S8 → fail_reason='infrastructure'
- [ ] **T6.4** Feishu 告警 (per R2 M2): `FEISHU_OPS_ALERT_WEBHOOK` env 可选, fallback `FEISHU_NOTIFY_WEBHOOK` + warning log
- [ ] **T6.5** Unit tests: 三阈值 boundary + CAS lost-update + Feishu webhook send mock (≥10 tests)
- [ ] **T6.6** Audit log: stuck detection event 写 `dispatches.attempt_history_json` (per AD-M2-9 §forensic)

**T6.done = reconciler 三阈值实施 + stuck → S_FAIL 路由 + Feishu 通知 + ≥10 tests**

#### T7 — Crash recovery (~10h, AD-M3-6 触发, OD-3b scope=仅 S5_AWAIT)

- [ ] **T7.1** `_handle_s5_await` 重写 — 不依赖 in-memory state (M2 已设计无 in-memory)
- [ ] **T7.2** 从 dispatches table 读 `alloc_id` + `dispatched_at`
- [ ] **T7.3** alloc_provider re-query (HTTP) 获取 alloc 状态
- [ ] **T7.4** 状态分支: pending/queued → leave (next tick) / running/complete → S6_REVIEW / failed/lost → S_FAIL / **404 Not Found → S_FAIL(alloc_lost)** (per R1-M9, alloc 已 GC)
- [ ] **T7.5** 1 unit test: `test_handle_s5_await_resumes_from_db_only` (verify 不读 self._memory)
- [ ] **T7.6** AD-M3-6 回填 (crash recovery scope 决策, OD-3b 锁后)

**T7.done = _handle_s5_await DB-only 实施 + unit test + AD-M3-6 回填 (T12 集成 test 收尾)**

#### T8 — `ZhipuClient` (~4h)

- [ ] **T8.1** `aria_layer1/clients/zhipu_client.py` mirror SilknodeClient (stdlib urllib, per `feedback_secrets_never_in_conversation` os.environ)
- [ ] **T8.2** Base URL: `open.bigmodel.cn/api/paas/v4/chat/completions`
- [ ] **T8.3** Auth: `ZHIPU_API_KEY` (post-rotation 才 wired, T13)
- [ ] **T8.4** Per-token billing model field (vs Luxeno flat)
- [ ] **T8.5** silknode-integration-contract 契约 1 no-storage 透传 — **OD-3d generalize**: 契约 1 §禁止条款 适用所有上游 LLM provider, 含 ZhipuClient 直连 (in-memory buffer only, 无 disk log payload); 等 owner Phase A.2 advisory 确认 yes/no
- [ ] **T8.6** **Timeout policy (per R1-I1, OD-3g default 等 owner)**: `connect_timeout=5s` + `read_timeout=60s` per call (硬 ceiling)
- [ ] **T8.7** Unit tests: success / 5xx / 429 / timeout / token usage parse / connect_timeout / read_timeout (≥7 tests)

**T8.done = ZhipuClient 实施 + 契约 1 no-storage + ≥7 tests**

#### T9 — `ProviderRouter` + multi-model + dict fallback_chain_json (~14h, AD-M3-4 触发, OD-12 §Q1=D')

- [ ] **T9.1** `aria_layer1/llm/provider_router.py` ProviderRouter class
- [ ] **T9.2** 主链: Luxeno (primary, flat sub) → Zhipu (fallback, per-token) — 3 次 expo backoff (1s/2s/4s) 后被动 fallback
- [ ] **T9.3** Model chain (per OD-12 §Q1):
  - S2_DECIDE → `glm-4.5-air`
  - S3_BUILD_CMD → `glm-5-turbo`
  - S6_REVIEW → `glm-5.1`
- [ ] **T9.4** Per-state fallback ladder (model degrade): `5.1 → 5-turbo → 4.5-air` if quality model 5xx
- [ ] **T9.5** fallback_chain_json dict-array 写入 (write-time, schema v2): `[{provider, model, outcome, reason, latency_ms, ts}]` — **dict 字段类型/枚举锁定 (per R1-C2)**: `provider ∈ {luxeno, zhipu}`; `outcome ∈ {ok, http_5xx, http_429, http_4xx, timeout, network_error, quality_degrade}`; `ts` ISO-8601 UTC; `latency_ms` int; `reason` str|null; intra-provider retry (per R1-M6) 也写 entry, outcome 反映该次结果
- [ ] **T9.5b** **fallback_triggered 写入点 (per R1-M4)**: ProviderRouter 落 fallback 时同步 UPDATE `dispatches.fallback_triggered=1` (任何 fallback_chain_json 含 outcome != 'ok' 即 trigger); 1 unit test asserting field after fallback path
- [ ] **T9.6** Wire to `_handle_s2_decide` / `_handle_s3_build_cmd` / `_handle_s6_review` (M2 单一 SilknodeClient 替换为 ProviderRouter)
- [ ] **T9.7** Test matrix (per R2 I8): parameterized (3 state × 5 fallback path × 6 dict field assertion) ≥ 12 cases
  - States: S2_DECIDE, S3_BUILD_CMD, S6_REVIEW
  - Paths: Luxeno-only-success (1 entry chain) / Luxeno-success-after-1-retry (2 entries: fail + ok) / Luxeno→Zhipu-fallback (2 entries: luxeno fail + zhipu ok) / Luxeno→Zhipu-both-5xx → S_FAIL (≥2 entries all non-ok) / Luxeno→Zhipu-quality-degrade-5.1→5-turbo (≥2 entries quality_degrade outcome)
  - Assertions: provider/model/outcome/reason/latency_ms/ts in fallback_chain_json (R1-C2 enum 严格)
- [ ] **T9.8** Multi-model benchmark (~8h subset of T9): 3 模型 × 同 prompt 重复 3 次 = 9 次/state, 验证 quality
  - **Quality threshold (per R1-I8, OD-3e default 等 owner)**: S2 ≥80% 状态决策正确率 / S3 ≥90% bash command shellcheck-equivalent 通过 / S6 ≥66% 三轮 review 多数票一致
  - **Gate vs exploratory (per OD-3e)**: AI 推荐 default = **exploratory only** (Luxeno 已实战稳定; 硬 gate budget cap 不够), owner 确认后改 m3-handoff `multi_model_benchmark_gate=true|false`
  - **Budget cap (per R1-I9)**: `BUDGET_CAP_USD=5.00` hard ceiling, abort if exceeded; m3-handoff `t9_8_benchmark_actual_cost_usd` field
- [ ] **T9.9** Benchmark 结果写入 m3-handoff.yaml `multi_model_routing_benchmark` field (含 quality metrics + actual_cost_usd + threshold pass/fail)
- [ ] **T9.10** AD-M3-4 回填 (ProviderRouter 决策)

**T9.done = ProviderRouter 实施 + multi-model state-aware + dict fallback + ≥12 test matrix + benchmark + AD-M3-4 回填**

#### T10 — Per-provider token breakdown (~4h, AD-M3-7 触发, R2 C1)

- [ ] **T10.1** `repo.update_token_usage` signature 改: `(provider: str, model: str, in_tok: int, out_tok: int, cost_usd: float | None)`
- [ ] **T10.2** S2/S3 token tracking wiring (per R2 I3, 复用 M2 T9 pattern): `_handle_s2_decide` + `_handle_s3_build_cmd` 末尾加 `repo.update_token_usage(...)` 调用 + `usage_from_silknode_response` helper extend (Zhipu compat)
- [ ] **T10.3** compute_cost provider-aware branch:
  - Luxeno: cost_usd = 0 (flat sub baseline 单独跟踪 m3-handoff)
  - Zhipu: cost_usd = metered per pricing table (T10 含 `aria_layer1/llm/zhipu_pricing.py` constants module **per R1-I7 + OD-3f default**: `_PRICING_VERSION='1.0'` + `_PRICING_FETCHED_AT='<T10 实施日>'` + source URL comment + 6-month review trigger; AI 推荐 default = snapshot at T10 day, 等 owner OD-3f 确认 vs runtime API)
  - **Zhipu response.usage compat (per ai R1)**: 验 Zhipu /v4/chat/completions response.usage `{prompt_tokens, completion_tokens, total_tokens}` shape 与 silknode 透传一致 → 同 helper + provider param; 不一致 → 加 `ZhipuTokenAdapter`
- [ ] **T10.4** m3-handoff.yaml 加 fields: `luxeno_subscription_baseline_usd_monthly` + `zhipu_metered_usd_total` (per R2 C1)
- [ ] **T10.5** Unit test: cumulative S2 + S3 + S6 tokens (per R2 I3) + provider-aware cost (≥4 tests)
- [ ] **T10.6** AD-M3-7 回填 (provider-aware cost model 决策)

**T10.done = signature 改 + S2/S3/S6 全 wired + Luxeno=0 / Zhipu metered branch + handoff fields + AD-M3-7 回填**

#### T11 — Nomad integration 加固 (~8h)

- [ ] **T11.1** Parameterized job idempotency re-verify (per OD-5a + AD-M1-7): DISPATCH_ID + IDEMPOTENCY_KEY 双重 dedupe; integration test fire-twice-same-key 仅 1 alloc
- [ ] **T11.2** 跨 alloc 失败 retry semantics: alloc lost/failed → S_FAIL terminal (不自动 re-dispatch); attempt_count 不增 (reconciler 单源处理)
- [ ] **T11.3** Nomad Variable 绑定 (per R2 M6): `M1_VALIDATOR_PATH` 加入 aria-orchestrator HCL Nomad Variable, 容器内 bind mount
- [ ] **T11.4** alloc_provider HTTP error handling: 4xx terminal log + 5xx exponential backoff (3 次)
- [ ] **T11.5** Unit tests: idempotency / cross-alloc semantics / Nomad Var binding / HTTP error policy (≥8 tests)

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
| B.2.0 | M2 carryover (T1-T4 + T13 pull-forward per OD-14) | 24h | ⏳ |
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
