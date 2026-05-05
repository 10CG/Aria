# aria-2.0-m3-cycle-close-glm-routing-recovery — Aria 2.0 M3 Layer 2 Cycle Close + GLM Multi-Model Routing + Crash Recovery

> **Level**: Full (Level 3 Spec)
> **Status**: **Approved** (Phase A.3 lock 2026-05-04; AI-drafted per AD-M0-9 with provenance; owner final sign-off pending implicit per `feedback_ai_代填_sign_off_pattern`, audit trail in `.aria/decisions/2026-05-04-us-023-phase-a2-r1-owner-advisory.md` + `.aria/decisions/2026-05-04-od-13-prd-m3-effort-90-to-185h.md`)
> **Created**: 2026-05-04
> **Approved**: 2026-05-04 (Phase A.3 OD-12 baseline final lock + OD-13 PRD patch applied + R2 SCOPE_OK_R2 4/4 + R3+R4 collapsed per OD-15)
> **Parent Story**: [US-023](../../../docs/requirements/user-stories/US-023.md)
> **Target Version**: v2.0.0-m3
> **Source**:
>   - [US-023.md](../../../docs/requirements/user-stories/US-023.md) (scope per Q1=D' reframe, commit 127605c)
>   - [OD-12 RESOLVED](../../../.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md) — 7 主决策 + 25 细节
>   - [R2 closeout memo](../../../.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md) — 3 critical / 10 important / 6 minor / 3 owner-decide findings
>   - [PRD v2.1 §M3 line 404 + line 510 US-023](../../../docs/requirements/prd-aria-v2.md) (待 Phase A.3 OD-13 patch)
>   - [M2 closeout memory](../../../.claude/projects/-home-dev-Aria/memory/project_aria_m2_closeout_2026-05-03.md) (M3 carryover ~21h scope)
>   - [m2-handoff.yaml](../../../aria-orchestrator/docs/m2-handoff.yaml) (M2→M3 input 契约)
>   - [m2-report.md §4.2](../../../aria-orchestrator/docs/m2-report.md) (carryover scope)
>   - [AD-M2-9](../../../aria-orchestrator/docs/architecture-decisions.md) §风险 #1 (Layer 2 job 缺失即 M3 scope)
>   - [OD-11](../../../.aria/decisions/2026-05-03-od-11-t15-4-5-perf-reframe.md) (T15.4/T15.5 perf carryover)
>   - [secret_rotation_deferred SOP](../../../.aria/decisions/2026-05-02-secret-rotation-deferred.md) (T13 mid Phase B.2 trigger)
> **Forgejo Issue**: _Pending creation T0_
> **Related**:
>   - **前置 (硬门控)**: [US-022 / aria-2.0-m2-layer1-state-machine](../../archive/2026-05-03-aria-2.0-m2-layer1-state-machine/) — `m2_e2e_passed=true` + Go-with-revision 2026-05-03 已满足
>   - **后继**: US-024 (M4 Human gate + Feishu approve + 7d ack timeout)
>   - **跨 milestone**: US-027 (Cost routing + 预算控制 跨 M3-M6, M3 起 per-provider token breakdown 铺路)
> **Owner Decisions**: OD-12 RESOLVED 2026-05-03 (7 主决策 + 25 细节) / **OD-13 RESOLVED 2026-05-04** (PRD §M3 工时 90→185h, Phase A.3 lock; PRD patches applied) / OD-3a/b/c RESOLVED Phase A.2 R1 (HCL sha digest pin / crash recovery scope=仅 S5_AWAIT / lazy-wire ARIA_LAZY_WIRE=1) / **OD-14 RESOLVED 2026-05-04** (T13 secret rotation 拉到 B.2.0 startup per advisory Q1=YES) / **OD-15 RESOLVED 2026-05-04** (Phase A.2 R3+R4 collapse per R2 SCOPE_OK_R2 4/4) / OD-3d/3e/3f/3g RESOLVED 2026-05-04 (silknode contract generalize / multi-model benchmark exploratory / Zhipu pricing snapshot / ZhipuClient timeout default)

> **Q1=D' divergence 声明 (per OD-12)**: 本 Spec 的 "双 provider" 解读 supersedes PRD §M3 字面 — 实际为 **Luxeno (primary, flat sub) + Zhipu 官方 (HA fallback, per-token billing) + GLM 多模型 routing** (S2=4.5-air / S3=5-turbo / S6=5.1, fallback ladder 5.1→5-turbo→4.5-air)。Anthropic provider 保留 deprecated (per AD-M1-12 supersedes AD-M1-6, owner subscription-only no API key)。Patch 02 在 Phase A.1.4 落地。

> **OD-12 baseline 声明**: 实际 scope discovery 后 baseline = **185h hard** (PRD §M3 90h × 2.06 inflation, 与 M2 100h→148h × 1.48 同模式), 5-6 周 50% 投入容量。OD-13 立 if 超 6 周。Phase A.3 OD-13 PRD patch 落地。

## Why

US-022 M2 (2026-05-03 done) 完成 Layer 1 状态机自动化 dispatch (cron 60min tick, S0→S4_LAUNCH HTTP dispatch 真发, 11 issue 自动派发实证)。但 M2 验收 D (perf vs M1 ×1.5) 因 **Layer 2 job HCL 缺失** WAIVED carryover (per OD-11 选项 C, AD-M2-9 §风险 #1) — S4_LAUNCH HTTP 500 进 S_FAIL(infrastructure) 立终止, cycle 在 S5_AWAIT 之前止步。

M3 的核心价值: 把 "M2 cycle 终止于 dispatch fail" 升级为 "完整 S0→S9_CLOSE 闭环 + Hermes 重启可恢复 + 双 provider HA + 多模型 quality routing", 是 Aria 2.0 从 "可派发" 到 "可运营 cycle" 的关键跃迁, 同时为 M4 human gate 接入提供稳定基座。

具体变化:

| 维度 | M2 (Layer 1 only) | M3 (Layer 1 + Layer 2 闭环) |
|------|-------------------|------------------------------|
| Cycle 终点 | S4_LAUNCH HTTP 500 → S_FAIL(infrastructure) | S9_CLOSE (PR merged) 或 triage S_FAIL 显式分流 |
| Layer 2 job | 不存在 (HCL 未部署) | `aria-layer2-runner` parameterized job (US-021 M1 fork, sha digest pin) |
| alloc 状态 | 未消费 | `NomadAllocHTTPProvider` 真实 HTTP `/v1/allocation/{id}` 轮询 + 30s ack budget |
| LLM provider | Luxeno-only (M2 单链路) | Luxeno primary + Zhipu 官方 fallback (per Q1=D') |
| LLM model | flashx single (subscription) | S2=glm-4.5-air / S3=glm-5-turbo / S6=glm-5.1 (state-aware quality routing) |
| Fallback | 字符串数组 fallback_chain_json (M2) | dict-array `[{provider, model, outcome, reason, latency_ms, ts}]` (schema v2 transform) |
| 重启行为 | Hermes restart → in-memory state lost; S5_AWAIT dispatch 视为 stuck | Hermes restart → S5_AWAIT 自动 resume (alloc_id 持久, alloc_provider re-query) |
| Stuck detection | 无 (cron 单挂会永远 stuck) | 独立 `aria-layer1-reconcile.nomad.hcl` periodic (30min) + CAS 锁 + 三阈值 + Feishu 告警 |
| Schema | v1.0 (字符串数组 fallback, 无 cycle 时间戳) | v2.0 (5 新 col additive: cycle_start/end_ts, dispatched_job_id, eval_id, provider_cost_model) |
| Secret keys | 4 (LUXENO_API_KEY + 3 FEISHU_*) | 5 (+ZHIPU_API_KEY); rotation T13 一次性 5 keys |
| Token cost | M2 仅 S6 wired | S2/S3/S6 全 wired + provider-aware compute_cost (Luxeno=0 flat / Zhipu metered) |
| Acceptance D | WAIVED carryover | 真实 cycle wall p50 ≤ M1 demo_002 × 1.5 = 47.25s |

**为什么 M3 不引入 Anthropic** (per OD-12 §Q1=D'): owner 仅 claude.ai 订阅, 无 API key 账号。"双 provider" 字面在 M3 解读为 **跨 provider HA fallback** (Luxeno → Zhipu) + **同 provider 内 quality routing** (GLM 三档模型), 远比 PRD 字面 "Anthropic ⇄ GLM" 切换更贴合 owner 实际可用资源, 且 legal OD-9 续延 (Zhipu 也境内 vendor, IS-4 不重审)。Anthropic provider 保留 deprecated 状态, M5+ 视需复活。

**M3 出 scope 时的 deliverable**:
- ≥10 个 synthetic issue 走完整 Layer 1+Layer 2 cycle (S0→S9_CLOSE, 含 ≥1 真实 PR merged 实例)
- Tier-1 自动化集成 fake-cycle test 全 PASS (per Q6=A)
- Cycle p50 ≤ 47.25s (S1_SCAN→S9_CLOSE wall, fallback_triggered=false 过滤, per Q7=C)
- Hermes kill -9 重启实测: pre-restart 的 S5_AWAIT dispatch post-restart auto-resume polling 后 S6/S7 推进
- Luxeno 5xx 模拟实测 fallback 到 Zhipu, fallback_chain_json 含 luxeno + zhipu 两类 entry
- Reconciler 检测 stuck S5_AWAIT > 60min → S_FAIL(stuck) routing + Feishu 通知, 单元 + integration test 全 PASS
- 全 5 secret keys post-rotation 后 perf benchmark PASS (Q8d 复用 验收 B)

## What

### 一、Layer 2 真实容器路径 (carryover #1, ~6h)

**HCL job spec** (`aria-orchestrator/jobs/aria-layer2-runner.nomad.hcl`, fork from US-021 M1):
- `type = "batch"` + `parameterized` stanza
- `meta_required = ["ISSUE_ID", "ISSUE_URL", "DISPATCH_ID", "IMAGE_SHA", "IDEMPOTENCY_KEY"]` (per OD-3a HCL meta key inventory + R2 I1)
- `meta_optional = ["BUDGET_CAP_USD", "TRIAGE_BODY_JSON"]`
- Image pin: **sha digest** (per Phase A.2 OD-3a default, AD-M1-7 reproducibility); HCL 用 `image = "registry.10cg.pub/aria-runner@sha256:${IMAGE_SHA}"` form (immutable)
- Driver: `docker` (与 M1 一致, 不切 raw_exec)
- Networking + volumes: 与 M1 一致 (含 host_volume `aria-runner-cache` if applicable)
- Resources: M1 baseline (CPU 1000 / Mem 2048MB)
- Constraints: heavy nodes only (`attribute = "${node.class}" value = "heavy"`)
- Lifecycle: 默认 (无 prestart hook)
- Idempotency: per OD-5a + AD-M1-7 (DISPATCH_ID + IDEMPOTENCY_KEY 双重 dedupe; HCL 内 alloc 重启不重跑 setup)

### 二、alloc_provider 生产化 (carryover #2, ~4h)

**`NomadAllocHTTPProvider` class** (`aria_layer1/clients/alloc_status_provider.py`, supersedes Fake):
- HTTP GET `/v1/allocation/{alloc_id}` (Nomad API, base_url 走 `NOMAD_ADDR` Nomad Variable)
- 30s ack-poll budget (M2 fake-only; M3 真实化, 30s 超时则 S5_AWAIT 留状态供 reconciler 处理 per Q3=A 三阈值)
- alloc states 映射 Layer 1 transition: `pending|queued` → 不动 (reconciler stuck>60min 处理) / `running` → S6_REVIEW 准备 / `complete` → S6_REVIEW / `failed` → S_FAIL(layer2_runner_failed) / `lost` → S_FAIL(alloc_lost)
- 实施 `AllocStatusProvider` Protocol (M2 同 contract per AD-M2-9 §contract)
- **Lazy-wire 注入** (per R2 C3 + OD-3c default): `tick_runner.py` 内 `if os.environ.get("ARIA_LAZY_WIRE") == "1": self._alloc_provider = NomadAllocHTTPProvider()` (与 ForgejoCliClient + NomadDispatchClientHTTP pattern 一致)
- 真实化测试: integration test 用 testing-mock Nomad HTTP (httpx mock or local nomad agent dev mode)

### 三、Schema migration v2 (carryover #3, ~3h)

**Schema v1.0 → v2.0 (additive-first per OD-12 §Q5=A + R2 I4 + R2 M3 + R2 M5)**:

ALTER TABLE `dispatches` 加 6 column (R1-M2 加入 attempt_history_json):
| col | type | 用途 | 来源 |
|---|---|---|---|
| cycle_start_ts | TEXT | S1_SCAN entry 时设 (acceptance B p50 起点) | OD-12 §Q5 |
| cycle_end_ts | TEXT | S9_CLOSE / S_FAIL entry 时设 (终点) | OD-12 §Q5 |
| dispatched_job_id | TEXT | Nomad parameterized dispatch ID (forensic per AD-M2-9 §风险 #5) | OD-12 §Q5 |
| eval_id | TEXT | Nomad evaluation ID | OD-12 §Q5 |
| provider_cost_model | TEXT | `metered` (Zhipu) / `subscription_flat` (Luxeno) | OD-12 §Q5 + R2 C1 |
| attempt_history_json | TEXT | Reconciler stuck detection event log (per AD-M2-9 §forensic, T6.6 wired) | R1-M2 |

CREATE TABLE 新增 (R1-M3):
- `migration_notes (key TEXT PRIMARY KEY, note TEXT, applied_at TEXT)` — placeholder + backfill rule audit trail

**Schema v1 pre-condition** (per R1-C1): T3.1 migration script 必须验 v1 fixture 已含 `fallback_triggered INTEGER NOT NULL DEFAULT 0` (M2 schema.sql:85 实证存在); fail-fast if missing。

ALTER TABLE 转换:
- `fallback_chain_json` write-time exhaustive transform (per R2 I4): 一次性 UPDATE all v1 字符串数组 row → v2 dict array, 同 ALTER 同 transaction
- inline UNIQUE constraint (`schema.sql:98`) 保留 — 应用层 dedupe (e36beb2 commit) 续用; drop 推 v3 (M4 / US-024)

ALTER TABLE `schema_meta`:
- INSERT `('schema_version', '2.0')`

Migration runner 时机: 启动时自动检查 schema_version 升级 (简单, ALTER 失败 SQLite 自动回滚, 不需手动 rollback)。

Backfill rules (per R2 M3 + R2 M5):
- 历史 row `provider_cost_model = 'subscription_flat'` (per AD-M1-12 Luxeno-only)
- 历史 S9_CLOSE / S_FAIL row `cycle_start_ts = state_entered_at` (近似估计, 显式 placeholder 注 in `migration_notes` table)

Test fixture: T15.3 真实 11-row dispatches.db 快照 (per qa R1 OBJ-5 CanonicalDispatchesDB pattern), migration test PASS, 0 数据丢失。

### 四、GLM 多模型 routing (per Q1=D', ~32h)

**`ZhipuClient`** (`aria_layer1/clients/zhipu_client.py`, mirror SilknodeClient stdlib urllib pattern, ~4h):
- Base URL: `open.bigmodel.cn/api/paas/v4/chat/completions`
- Auth: `ZHIPU_API_KEY` (per Q8d post-rotation)
- **Timeout policy (per R1-I1, AI 推荐 default 等 OD-3g 确认)**: `connect_timeout=5s` + `read_timeout=60s` per call (硬 ceiling, 防止单 hanging 阻塞 ProviderRouter retry budget); ProviderRouter total fallback wall ≤ `3 × 65s = 195s` (cron tick 60min headroom 充裕)
- Per-token billing model (vs Luxeno flat sub)
- silknode-integration-contract 契约 1 no-storage 透传 (**OD-3d generalize**: 契约 1 §禁止条款 适用所有上游 LLM provider, 含 ZhipuClient 直连; in-memory buffer only, 无 disk log payload, 等 owner Phase A.2 确认)

**`ProviderRouter` 抽象** (`aria_layer1/llm/provider_router.py`, ~14h):
- 主链: Luxeno → Zhipu (3 次 expo backoff 1s/2s/4s 后 fallback)
- Model chain (per OD-12 §Q1):
  - S2_DECIDE → `glm-4.5-air` (cheap)
  - S3_BUILD_CMD → `glm-5-turbo` (mid-tier, 对标 Sonnet)
  - S6_REVIEW → `glm-5.1` (top-tier, 对标 Opus)
- Per-state fallback ladder (model degrade): `5.1 → 5-turbo → 4.5-air` if quality model 5xx
- Test matrix (per R2 I8): parameterized (3 state × 5 fallback path × 6 dict field assertion) ≥ 12 cases
- fallback_chain_json dict 写入 (write-time, schema v2; **dict 字段类型/枚举锁定 per R1-C2**):
  - `provider`: enum `{luxeno, zhipu}` — 后续扩 Anthropic 时新加
  - `model`: str (free-form, 例 `glm-4.5-air`/`glm-5-turbo`/`glm-5.1`)
  - `outcome`: enum `{ok, http_5xx, http_429, http_4xx, timeout, network_error, quality_degrade}`
  - `reason`: str | null (free-form, 例 "HTTP 503 from upstream")
  - `latency_ms`: int (per-call wall, 0 if connection failed)
  - `ts`: str ISO-8601 UTC (例 `2026-05-04T10:30:00Z`)
  - schema_meta entry `('fallback_chain_outcome_enum', '<json-list>')` self-documents 当前枚举 (T3 schema migration 同期写入, future audit 容易 drift detect)
  - **intra-provider retry 写入语义 (per R1-M6)**: ProviderRouter 每次 attempt (含 within-Luxeno retry, model-degrade) 都写 1 entry, `outcome` 反映该次结果; e.g. Luxeno 4.5-air 5xx → 4.5-air `outcome=http_5xx`, then 5-turbo `outcome=ok` → chain 含 2 entries

**S2/S3 token tracking wiring** (per R2 I3, 复用 M2 T9 pattern, ~2h):
- `_handle_s2_decide` + `_handle_s3_build_cmd` 末尾加 `repo.update_token_usage(...)` 调用
- 1 unit test 验 cumulative = S2 + S3 + S6 tokens

**Multi-model benchmark** (~8h):
- 测试 3 模型 × 同 prompt 重复 3 次 = 9 次/state, 验证 quality (S2 决策正确率 / S3 命令合法率 / S6 review 一致性)
- benchmark 结果写入 m3-handoff.yaml `multi_model_routing_benchmark` field

**ProviderRouter abstraction (其余, ~10h)**: provider switching glue + retry policy + audit trail

### 五、Mechanical Reconciler (per Q3=A + Q4=A, ~14h)

**`aria-layer1-reconcile.nomad.hcl`** (~6h):
- Nomad periodic job, cadence 30min (在 cron 60min 中点跑, 减撞概率)
- 与 cron 同 docker image, 不同 entry-point (`aria-layer1-reconcile` CLI)

**Reconciler logic** (~8h):
- 三阈值 (per OD-12 §Q3 default):
  - `max_age_at_S5_AWAIT_minutes = 60`
  - `max_total_attempts = 3`
  - `stuck_alloc_states = ('pending', 'queued')`
- 路由策略: 混合
  - Attempt 1-2: `attempt_count++` (let next cron tick retry)
  - Attempt 3: S_FAIL(stuck) terminal
- CAS 锁 (per OD-12 §Q4 + R2 I5):
  - `UPDATE ... WHERE rowid=X AND state='S5_AWAIT' AND last_heartbeat_at=? AND attempt_count=?` (compound 版本字段)
  - SQLite WAL 天然支持 + `PRAGMA busy_timeout=5000` (per R2 M4); CAS 失败 retry 1 次 (lost = let cron win)
- Feishu 告警 (per R2 M2): `FEISHU_OPS_ALERT_WEBHOOK` env 可选, fallback `FEISHU_NOTIFY_WEBHOOK` + warning
- M5 LLM-decided 升级预留: Strategy interface (mechanical vs LLM, env var `ARIA_RECONCILER_STRATEGY=mechanical|llm` 切换 1 行)

### 六、Crash Recovery (per OD-3b default 仅 S5_AWAIT, ~10h)

**Scope** (per R2 I2): M3 仅 S5_AWAIT (Nomad-controlled 状态, alloc_id 持久 in dispatches table)。其他 5 普通状态 (S1_SCAN/S2/S3/S4/S6/S7/S8) 中断由 reconciler stuck >60min → S_FAIL 处理。M4/M5 视需扩展。

**实施**:
- Hermes restart 后, cron tick 进入 `_handle_s5_await`:
  - 不依赖 in-memory state (M2 已设计无 in-memory)
  - 从 dispatches table 读 `alloc_id` + `dispatched_at`
  - alloc_provider re-query (HTTP) 获取 alloc 状态
  - 状态分支: pending/queued → leave (next tick) / running/complete → S6_REVIEW / failed/lost → S_FAIL / **404 Not Found → S_FAIL(alloc_lost)** (R1-M9, alloc 已被 Nomad GC, e.g. >72h node_gc_threshold)
- Test harness (per R2 C2): named test `test_t12_crash_recovery_s5_await_auto_resume`
  - 5 步: pre-seed (S5_AWAIT row + alloc_id) → fresh hermes-extension instance → tick → assert `_handle_s5_await` fired → assert state advances (running → S6 prep)

### 七、Nomad integration 加固 (~8h)

- Parameterized job idempotency (per OD-5a + AD-M1-7): DISPATCH_ID + IDEMPOTENCY_KEY 双重 dedupe re-verify, 跨 alloc 失败 retry semantics
- alloc_provider 真实化 (HTTP GET `/v1/allocation/{id}`)
- Nomad Variable 绑定 (per R2 M6): `M1_VALIDATOR_PATH` 加入 aria-orchestrator HCL Nomad Variable, 容器内 bind mount

**Stuck reason routing matrix (per R1-M10, T6.3 实施)**: 不同状态被 reconciler 检测 stuck 时 fail_reason 不同 — `S2/S3 → 'timeout'` (LLM call >60min 极罕见仅 network) / `S4/S5 → 'stuck'` (Nomad-controlled, 真 stuck) / `S1/S6/S7/S8 → 'infrastructure'` (上游 dependency)。

### 八、Secret rotation T13 (per Q8d, ~3h)

- 一次性 rotate 全 5 keys (LUXENO_API_KEY / 3 FEISHU_* / ZHIPU_API_KEY)
- 时机: **T13 拉到 Phase B.2.0 startup (week 1)** per OD-14 (R1 tech-lead 推荐, owner Phase A.2 advisory 待确认; 原 OD-12 §Q8d mid-B.2 因 90-day cap 2026-08-02 与 13-week wall 距离过近, 不安全)
- post-rotation 用 验收 B perf benchmark 顺便验证新 keys
- m3-handoff.yaml `secret_rotation_completed=true` + date

### 九、Per-provider token breakdown (US-027 prep, ~4h)

- `repo.update_token_usage` signature 改 `(provider, model, in_tok, out_tok, cost_usd)`
- m3-handoff.yaml 加 `luxeno_subscription_baseline_usd_monthly` + `zhipu_metered_usd_total` 两 field (per R2 C1)
- compute_cost provider-aware branch: Luxeno=0 (flat sub), Zhipu metered (constants module 含 `_PRICING_VERSION` + `_PRICING_FETCHED_AT` snapshot date + source URL comment + 6-month review trigger per R1-I7; AI 推荐 default snapshot 取数 vs runtime API, 等 OD-3f owner 确认)

## Acceptance (per OD-12 §验收标准)

| ID | 验收 | 量化 metric | Tier |
|---|---|---|---|
| A | ≥10 issue 走完整 Layer 1+Layer 2 cycle (S0→S9_CLOSE) | `count(state=S9_CLOSE) ≥ 10` 在 Tier-1 fake-cycle test 内 | Tier-1 自动化集成 only (Q6=A) |
| B | M3 cycle p50 ≤ M1 baseline × 1.5 = **47.25s** | `median(cycle_end_ts - cycle_start_ts) WHERE state='S9_CLOSE' AND fallback_triggered=false ≤ 47.25s` | Tier-1 fake-cycle test |
| C | Crash recovery: Hermes 重启 → S5_AWAIT auto-resume polling | named test PASS: `test_t12_crash_recovery_s5_await_auto_resume` (5-step) | Tier-1 + Tier-2 |
| D | GLM 多 provider HA fallback (Q1=D'): Luxeno 5xx → Zhipu 接管 | `fallback_chain_json` 含 `provider=luxeno` + `provider=zhipu` 两类 entry; integration test parameterized 3×5×6 ≥12 cases PASS | Tier-1 |
| E | Schema migration v2 backward-compat (Q5=A additive) | T15.3 实际 11-row dispatches.db 快照 fixture migration test PASS, 0 数据丢失 | Tier-1 |
| F | Secret rotation 完成 (5 keys) + post-rotation perf PASS | rotation_completed=true + date 在 m3-handoff.yaml + post-rotation 验收 B PASS | Tier-2 |

**M3.done** = (A ∧ B ∧ C ∧ D ∧ E ∧ F) ∧ (m3-handoff.yaml validator PASS) ∧ (owner sign-off + tech-lead co-sign + 268 → 320+ tests baseline) — R1-M7 校准: T2≥8 + T3≥10 + T6.5≥10 + T8.6≥7 + T9.7≥12 + T10.5≥4 + T11.5≥8 + T12 (5-step + ≥6 boundary + concurrent + kill -9) + T7.5=1 → ≥56 new + sister-bug fixes ≈ 60+ → 268+60 = **328+** baseline

## Out of Scope

- M4 完整 human gate (Feishu approve UI / 7d ack timeout) — 留 US-024
- M5 防漂移 + 审计日志 + Review loop — 留 US-025
- M6 v2.0.0 release docs — 留 US-026
- Cost routing 完整化 (跨 milestone US-027 不在 M3 内闭合; M3 仅做 per-provider breakdown 铺路)
- v1.x 心跳扫描器替换 (M3 仍 side-by-side 共存)
- 用户项目 (非 10CG/Aria) onboarding — Lab-internal 优先 per project_aria2_scope memory
- inline UNIQUE constraint drop — 推 schema v3 (M4 / US-024 自然落)
- LLM-decided reconciler — 推 US-025 M5 (M3 仅 Strategy interface 预留)
- 其他 5 状态 crash recovery (M3 仅 S5_AWAIT, 其余 reconciler stuck>60min 处理) — M4/M5 视需扩展

## Risks (Initial, 待 Phase A.2 audit 扩展)

| # | 风险 | 影响 | 缓解 |
|---|---|---|---|
| 1 | Layer 2 HCL fork from M1 偏离 image_sha pin pattern | 中 | OD-3a 锁 sha digest pin (default); T1 verify image_sha round-trip; T15 cluster smoke 实证 |
| 2 | Anthropic deprecated 但 PRD 字面仍要求双 provider | 低 | OD-12 §Q1=D' + Patch 02 (PRD §M3 字面 reframe), AD-M1-12 supersedes |
| 3 | Schema migration v2 在 production dispatches.db zero-downtime | 中 | additive-first (新 schema_version=2 + 双 read 策略, drop UNIQUE 推 v3); ALTER 失败 SQLite 自动回滚; T15 11-row fixture migration test PASS gate |
| 4 | Reconciler 与 cron tick 锁竞争 | 中 | CAS (compound 版本字段 last_heartbeat_at + attempt_count) + busy_timeout=5000ms + retry 1; 故障隔离 (cron 挂 reconciler 仍工作) |
| 5 | Secret rotation 2026-08-02 hard cap 与 M3 schedule 接近 | 中 | T13 mid Phase B.2 trigger (~Week 14-15), 不晚于 cap; M3 不超 6 周硬约束 |
| 6 | Crash recovery test 需重现 stuck dispatch | 中 | T12 named test (5-step) + integration test kill -9 lock; MockClock fast-forward 不需真等 60min |
| 7 | 双 provider 切换 token cost 不确定性 | 中 | T9 token_tracking 已就位; T10 加 per-provider breakdown |
| 8 | OD-12 baseline 185h × 6 周硬约束被超 | 高 | OD-13 立 Phase A.3; B.2 mid-sprint scope-cut review 触发; 候选裁切: T9 multi-model benchmark / T11 加固 / T15 Tier-2 stretch |
| 9 | CAS double-recovery race (cron + reconciler 同 row 同 ts) | 中 | R2 I5: WHERE 加 attempt_count compound 字段; T12 concurrent test 验 BEGIN IMMEDIATE 序列化 |
| 10 | NomadAllocHTTPProvider 注入路径偏 (lazy attribute vs ARIA_LAZY_WIRE) | 低 | OD-3c 锁 ARIA_LAZY_WIRE=1 显式注入 (与 ForgejoCliClient + NomadDispatchClientHTTP pattern 一致); T2 spec 明示 |
| 11 | Tier-1 only 验收 A 弱于 Tier-2 | 中 | OD-12 §Q6=A owner 接受; T15 stretch 提供 Tier-1 + Tier-2 同时 (≥12-14h, 不强制) |

## Architecture Decisions (AD-M3-* placeholders, 7 主 + 3 spillover)

| ID | 主题 | 状态 | 触发 | 主责 agent (Phase A.3.4) |
|---|---|---|---|---|
| AD-M3-1 | Layer 2 parameterized job HCL (image sha pin + meta keys + idempotency) | **Decided 2026-05-05 (T1)** — see [architecture-decisions.md §AD-M3-1](../../../aria-orchestrator/docs/architecture-decisions.md) | OD-3a sha digest 锁 | backend-architect (HCL design) + qa-engineer (validate) |
| AD-M3-2 | NomadAllocHTTPProvider 注入路径 (ARIA_LAZY_WIRE) + Protocol contract | **Decided 2026-05-05 (T2)** — see [architecture-decisions.md §AD-M3-2](../../../aria-orchestrator/docs/architecture-decisions.md) | OD-3c lazy-wire 锁 | backend-architect (Protocol) + ai-engineer (lazy-wire pattern) |
| AD-M3-3 | Schema v2 migration (additive-first + write-time fallback transform + backfill rules) | _待回填_ Phase B.2.0 T3 | OD-12 §Q5 实施期 | backend-architect (SQL) + qa-engineer (fixture) |
| AD-M3-4 | ProviderRouter abstraction + Luxeno→Zhipu HA + GLM multi-model state-aware | _待回填_ Phase B.2.1 T9 | OD-12 §Q1=D' + OD-3d/3e/3f/3g | ai-engineer (router design) + backend-architect (concurrency) |
| AD-M3-5 | Reconciler periodic job + CAS lock + 三阈值 + Strategy interface | _待回填_ Phase B.2.1 T5-T6 | OD-12 §Q3+Q4 + R1-M8 | backend-architect (CAS + HCL) + ai-engineer (Strategy interface) |
| AD-M3-6 | Crash recovery scope (仅 S5_AWAIT + alloc_provider re-query + 404 case) | _待回填_ Phase B.2.1 T7 | OD-3b 锁 + R1-M9 | qa-engineer (test harness) + ai-engineer (semantic) |
| AD-M3-7 | Provider-aware token cost model (Luxeno=0 flat / Zhipu metered + Zhipu pricing snapshot) | _待回填_ Phase B.2.1 T10 | R2 C1 + OD-3f snapshot | ai-engineer (pricing + cost) + qa-engineer (cumulative test) |
| AD-M3-8 | _spillover_ | _spillover_ | _on demand_ |
| AD-M3-9 | _spillover_ | _spillover_ | _on demand_ |
| AD-M3-10 | _spillover_ | _spillover_ | _on demand_ |

> **AD slot backfill 强制 closeout** (per `feedback_ad_slot_backfill_checkpoint` + R1-M5 spillover sentinel exception): T16 closeout 必须 fail-fast if AD-M3-1..7 任何 status 仍 `_待回填_`; AD-M3-8/9/10 的 status `_spillover_` 字面值是预期占位, validator skip; 实际未用则归档时清空 status 改 `_unused_`。

## M2 Input 契约 (per US-023.md §M2 input 契约)

从 [m2-handoff.yaml schema v1.0](../../../aria-orchestrator/docs/m2-handoff.yaml) 消费:

| Field | 用途 |
|---|---|
| `state_machine.fail_reason_enum` (9 values) | M3 reconciler 必须复用同枚举 (additive-only per AD-M1-7 + AD-M2-9 错误路由 matrix) |
| `m2_dispatches` 总计 (11 rows) | 11-row 真实 fixture for T15.3 schema migration test |
| `fail_reason_breakdown` (10 infrastructure) | M3 success metric: infrastructure → success cycle 转化率 |
| `hermes_extension.{package_name, package_version, cron_registration_method}` | M3 复用 plugin loading 不重写 |
| `persistence.{db_path, lock_path, payload_guard_enforced}` | M3 schema migration v2 必须保持 db_path + WAL mode + payload guard |
| `llm_provider.{base_url, primary_model, fallback_model, fallback_log_field}` | M3 双 provider routing 在此基础上加 Zhipu HA |
| `ad_m2_decisions.ad_m2_9` | M3 alloc_provider production class 必须实现 NomadDispatchClient Protocol 同 contract |
| `legal_assumptions.m2_secret_rotation_status` | "deferred to production launch (4 keys, hard cap 2026-08-02)" 是 M3 sign-off 前必触发 trigger |

## Patches (Phase A.1.4 起草, Phase B.2 配套 commit)

5 PRD/AD/US patches (per R2 closeout §"PRD patches needed"):

1. `patches/01-prd-m3-effort-90-to-185h.md` — PRD §M3 工时 90→185h (justification = OD-12 §Q2 scope discovery × 2.06 inflation, M2 mode 校准); via OD-13 in Phase A.3
2. `patches/02-prd-m3-dual-provider-reframe.md` — PRD §M3 'dual provider' 字面 → 'multi-model GLM routing + cross-provider HA fallback' (Luxeno primary + Zhipu fallback per AD-M1-12 supersedes; OD-12 §Q1=D' reference)
3. `patches/03-prd-m3-acceptance-a-tier1.md` — PRD §M3 验收 A 'cluster smoke gate' 字面 (若有) → 'Tier-1 自动化集成 + carryover #1 cluster verification embedded' (Q6=A reference)
4. `patches/04-prd-m3-acceptance-b-p50.md` — PRD §M3 验收 B p50 baseline 'M1 ×1.5' → 'M1 demo_002 p50_s × 1.5 = 47.25s, S1_SCAN→S9_CLOSE wall + fallback_triggered=false filter' (Q7=C reference)
5. `patches/05-prd-m3-acceptance-d-e-f-explicit.md` — PRD §M3 验收 D/E/F 显式化 (D: cycle-close p50 / E: schema migration zero loss / F: secret rotation 后 benchmark validation)

> **Patch 应用模式** (per OD-4 + M2 mode): patch 内容 Phase A.1.4 起草完成, 实际 commit 在 Phase B.2 startup (T1 / T16); tech-lead 复核与 T16 M3 Report 同期 co-sign。

## Phase 路线图 (per OD-12 §Spec 内 phase 排序)

```
Phase A.0 (DONE)  状态扫描 + brainstorm R1 + R2 (4-agent parallel)
Phase A.1 (DONE)  proposal.md + tasks.md + 5 patches (~12h, 2026-05-04)
Phase A.2 (DONE)  post_spec audit R1+R2 (R3+R4 collapsed per OD-15) — 4-agent fix-verify SCOPE_OK_R2 4/4 (~4h, 2026-05-04)
Phase A.3 (DONE)  OD-13 立 + PRD Patch 01-05 commit + Status: Draft → Approved + Agent assign (~1h, 2026-05-04)
Phase B.1         feature 分支 (`feature/aria-2.0-m3-cycle-close-glm-routing-recovery`) (<0.5h)
Phase B.2.0       M2 carryover (T1-T4, ~21h):
                    T1: aria-layer2-runner HCL fork (~6h)
                    T2: alloc_provider 生产化 (~4h)
                    T3: schema migration v2 (~3h)
                    T4: single-issue Layer 2 cycle smoke (~3h)
Phase B.2.1       M3 新 scope (T5-T12, ~90h):
                    T5: reconciler design + HCL (~6h)
                    T6: reconciler stuck-detection + S_FAIL + Feishu (~8h)
                    T7: crash recovery: hermes restart → S5_AWAIT auto-resume (~10h)
                    T8: ZhipuClient (~4h)
                    T9: ProviderRouter + multi-model + dict fallback_chain (~14h)
                    T10: per-provider token breakdown (~4h)
                    T11: Nomad integration 加固 (~8h)
                    T12: reconciler + crash recovery integration tests (~8h)
Phase B.2.Z       E2E + handoff (T13-T16, ~30h):
                    T13: secret rotation execution 5 keys (~3h)
                    T14: perf benchmark vs M1 (post-rotation, ~6h)
                    T15: ≥10 cycle Tier-1 集成 (验收 A+B+D+E) (~10h)
                    T16: m3-handoff.yaml + AD-M3 backfill + Report + Spec archive (~6h)
Phase C.1+C.2     dual push (Forgejo + GitHub) + PR
Phase D.1+D.2     Spec archive (`openspec/archive/<date>-aria-2.0-m3-cycle-close-glm-routing-recovery/`) + UPM N/A for Aria
```

**估算总额** (per OD-12 §Q2 baseline 185h):
- A.1: 12h
- A.2: 4h
- A.3: 1h
- B.1: 0.5h
- B.2.0: 21h
- B.2.1: 90h
- B.2.Z: 30h (含 T13 + T14 + T15 + T16)
- 隐性 audit 25h (Phase A.2 4-round + Phase B.2 scope-bounded per task group + Phase D 4-round) — 按 OD-12 §Q8c 已纳入 baseline
- 10% buffer: 17h
- **Total**: ~185h hard / 5-6 weeks 50% 投入

## Owner Action Items (3 个 active, 1 跳过, per OD-12 §Owner action items + R1-M7)

1. ~~Phase A.0a Anthropic legal reverify~~ — *Q1=D' 后跳过* (provider 不变 OD-9 续延)
2. **Phase B.2.0 T1**: 部署 aria-layer2-runner HCL on Aether (~30min) — owner 执行 `nomad job run` + verify alloc launch
3. **Phase B.2.0 T13** (per OD-14 pull forward): 执行 secret rotation (5 keys, ~45min per SOP `.aria/decisions/2026-05-02-secret-rotation-deferred.md`) — 拉到 week 1 startup, 不晚于 cap 2026-08-02
4. **Phase D T16**: M3 sign-off (~5min, m3-handoff.yaml `signoffs.owner` 字段填决定)

## 引用

- US-023.md: `docs/requirements/user-stories/US-023.md` (scope per Q1=D' reframe)
- OD-12 RESOLVED: `.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- R2 closeout: `.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md`
- M2 closeout memory: `.claude/projects/-home-dev-Aria/memory/project_aria_m2_closeout_2026-05-03.md`
- m2-handoff.yaml: `aria-orchestrator/docs/m2-handoff.yaml` (M2→M3 契约)
- m2-report.md §4.2: `aria-orchestrator/docs/m2-report.md` (carryover scope)
- AD-M2-9: `aria-orchestrator/docs/architecture-decisions.md#ad-m2-9` (Layer 1→2 dispatch 契约)
- AD-M1-12: `aria-orchestrator/docs/architecture-decisions.md#ad-m1-12` (Luxeno-only supersedes AD-M1-6)
- OD-9: `.aria/decisions/2026-05-02-od-9-silknode-luxeno-reframe.md`
- OD-11: `.aria/decisions/2026-05-03-od-11-t15-4-5-perf-reframe.md`
- secret_rotation_deferred SOP: `.aria/decisions/2026-05-02-secret-rotation-deferred.md`
- silknode-integration-contract (deprecated): `openspec/changes/aria-2.0-silknode-integration-contract/proposal.md`
- AB benchmark transparency: `openspec/archive/2026-04-10-benchmark-transparency-enhancement/`
- Aria 规范: `feedback_pre_merge_4round_convergence_template`, `feedback_ad_slot_backfill_checkpoint`, `feedback_validator_repo_drift_guard_test`, `feedback_unit_tests_dont_validate_plugin_loading`
