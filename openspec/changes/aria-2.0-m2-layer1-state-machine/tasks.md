# aria-2.0-m2-layer1-state-machine — Tasks

> **Parent**: [proposal.md](./proposal.md)
> **US**: [US-022](../../../docs/requirements/user-stories/US-022.md)
> **Total**: 146h (Core 17 items, OD-7=b 已裁 M2-15 partial-write 6h, partial-write 推 M3-2)
> **PRD baseline**: 140h (±4.3%, 可接受)
> **Status**: Draft (Phase A.1.2 起草, post_spec 审计待 owner 决策)
> **Owner Decisions**: OD-1~OD-7 (per brainstorm conclusion 2026-04-27)

## Task 工时基线

| ID | Task | 估算 | 依赖 | 验收锚点 | Agent 主责 |
|----|------|------|------|----------|-----------|
| **T0** | M2 kickoff + Forgejo Issue + AD-M2-* 决议位预留 | 3h | M1 done | T0.done + Issue URL + AD-M2 frontmatter | knowledge-manager |
| **T1** | Hermes Extension plugin 骨架 (Option C, 继承 M0 Spike POC) | 30h | T0 | T1.done + extension load PASS + 基础 dispatch hook | backend-architect + ai-engineer |
| **T2** | SQLite WAL schema + 持久化层 (含字段最小集 + UNIQUE idempotency) | 8h | T1 | T2.done + schema validator PASS + WAL+重启可读 (验收 B) | backend-architect |
| **T3** | 10+S_FAIL 状态机核心 (transition table + guards + advisory lock) | 16h | T2 | T3.done + 全 10 状态 transition 单元测试 | backend-architect |
| **T4** | S3/S5/S6 timeout + heartbeat + S_FAIL reason enum forensic 字段 | 8h | T3 | T4.done + timeout 触发 unit test + 9 值 reason enum 覆盖 | backend-architect + qa-engineer |
| **T5** | S0/S4 idempotency (UNIQUE + Nomad meta dispatch_id) | 4h | T2 | T5.done + 重复 dispatch unit test PASS (no double Nomad alloc) | backend-architect |
| **T6** | cron tick 60min + 跨 tick polling (S5_AWAIT) + advisory lock | 12h | T3 | T6.done + cron 重叠 skip 行为验证 + flock 拒绝并发 | backend-architect |
| **T7** | Layer 1 → Layer 2 ISSUE_ID + prompt_path 协议 (R7 meta < 100KB 守卫) | 10h | T2, M1 archive | T7.done + meta size assertion + bind mount 写入 round-trip | backend-architect |
| **T8** | silknode 集成 (OAI baseURL + GLM-air 主 / flashx fallback + AD-M0-8 fallback log) | 8h | T1 | T8.done + 真实 silknode 调用 smoke + fallback_chain_json 落 SQLite | ai-engineer |
| **T9** | token usage tracking (input/output/cost/model 字段写入) | 5h | T8 | T9.done + 跨 dispatch token 累计正确 + US-027 cost routing 数据基础 | ai-engineer |
| **T10** | S6_REVIEW LLM 评审 (silknode→GLM, 单次 review 1 call + 1 retry, 同 dispatch hash 复用) | 10h | T8 | T10.done + review verdict (PASS/REVIEW_REJECTED) 准确率 ≥ 80% on synthetic | ai-engineer + qa-engineer |
| **T11** | S2 image SHA pin guard (拒 mutable_tag, AD-M1-2) | 2h | T2 | T11.done + non-sha256 image 拒绝 + S_FAIL(reason=infrastructure) | backend-architect |
| **T12** | S7_HUMAN_GATE Feishu webhook 桩 (M2: send-and-forget, 记 HTTP code) | 6h | T3 | T12.done + webhook send 成功 + notification_status 字段落 SQLite | backend-architect |
| **T13** | S8_MERGE Forgejo PR API (确定性 merge + 幂等 marker) | 6h | T7 | T13.done + 重复 S8 不重复评论 + Forgejo merge API 成功 | backend-architect |
| **T14** | 状态机 unit test (DI clock + alloc_status mock, fast-forward) | 10h | T3, T4, T6 | T14.done + 100+ unit tests + 60min cron 在测试内 < 1s | qa-engineer |
| **T15** | M2 E2E demo (DEMO-001 + DEMO-002 ≥ 10 dispatches via cron) | 12h | T1-T14 | T15.done + 验收 A (≥10 issues) + 验收 D (perf ≤ M1 × 1.5) | qa-engineer + ai-engineer |
| **T16** | M2 Report + m2-handoff.yaml v1.0 + 3 patches (AD5 / PRD §M2 / US-022) + tech-lead co-sign | 6h | T15 | T16.done + handoff validator PASS + 3 patches merged + owner sign-off | knowledge-manager + tech-lead |

**Total Core**: 146h (per OD-7=b, M2-15 partial-write 6h 已裁 → 推 M3-2 reconciler)
**PRD baseline**: 140h (overrun 4.3%, owner 接受)

> **M2-15 (M3 deferred) 占位说明**: S6/S8 partial-write 原子性 (sub-step bitmask + 幂等 key) 在 M2 不实现; M2 实施期若发生 partial-write, 走 S_FAIL with `reason=infrastructure`, 监控触发后人工介入 reset。完整原子性 + 自动 reconciler 推 M3-2 (US-023 ~30h)。

---

## T0 — M2 Kickoff + Forgejo Issue + AD-M2-* 决议位预留 (3h)

**先决**: M1 已 done (`e2e_demo_passed=true`, 2026-04-23) + brainstorm conclusion 2026-04-27 Approved + Phase A.1 三件套 (proposal.md + tasks.md + 3 patches) 起草完成。

- [ ] **T0.1** 创建 Forgejo Issue 10CG/Aria (0.5h)
  - Title: `[US-022] Aria 2.0 M2 — Layer 1 状态机 + Hermes Extension`
  - 引用 brainstorm conclusion (`.aria/decisions/2026-04-27-us022-state-machine-brainstorm.md`)
  - URL 回填 US-022.md §Forgejo Issue 字段 (line 8)
- [ ] **T0.2** AD-M2-* 决议位 frontmatter 预留 (0.5h)
  - 在 `aria-orchestrator/docs/architecture-decisions.md` 新增 `## AD-M2-*` 占位段
  - 预留 6 个常见决议位 (provider 切换 / heartbeat 阈值 / cron 间隔 / fail_reason 演进 / S7 ack 触发 / handoff schema 演化)
- [ ] **T0.3** brainstorm conclusion phase_a1_followup 7 项 cross-ref 验证 (0.5h)
  - grep 本 Spec proposal.md, 确认 R3-OBJ-3/4/5 + R3-OBJ-cm-1/2/3/4 全部可定位
- [ ] **T0.4** synthetic fixture 复用确认 (1h)
  - 复用 M1 `aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/`, 扩展 8 个 issue variants (DEMO-003~010) 用于 T15 ≥10 dispatches 验收
- [ ] **T0.5** silknode endpoint 确认 (0.5h)
  - 与 silknode owner (= 本 owner per AD-M0-9) 确认 OAI baseURL: `https://silknode.10cg.pub/v1` 还是其他
  - 确认 GLM-air / flashx 配置在该 endpoint 已就绪 (M1 实战已用过, 大概率 yes)

**T0.done = AD-M2 frontmatter 已 commit + Forgejo Issue URL 回填 US-022.md + silknode endpoint URL 锁定**

---

## T1 — Hermes Extension Plugin 骨架 (30h)

**目标**: 按 AD3 Option C "Extension-only, 0 hermes core 修改", 实现 Hermes Extension plugin 骨架, 复用 M0 Spike POC (286 LoC, 13/13 tests pass) 作为起点。

- [ ] **T1.1** Hermes Extension 工程 scaffold (4h)
  - 按 hermes plugin 标准目录布局 (`hermes-extensions/aria-layer1/`)
  - `plugin.json` + `__init__.py` + `extension.py` + `requirements.txt` (stdlib + hermes SDK only)
  - manifest 声明 lifecycle hooks: `on_session_start` (per R-AD3-2 缓解 MCP 动态刷新 race)
- [ ] **T1.2** 复用 M0 Spike POC 5 状态代码 (3h)
  - 从 `openspec/archive/2026-04-16-aria-2.0-m0-spike-hermes/poc-code/` 拉 286 LoC 起点
  - 重命名状态: PENDING → S0_IDLE, RUNNING → S4_LAUNCH+S5_AWAIT (拆分占位), SUCCESS → S9_CLOSE, FAILED → S_FAIL, TIMEOUT → S_FAIL with reason
- [ ] **T1.3** 60min cron tick 注册 (3h)
  - Hermes scheduler API 注册 `aria_layer1_tick`, 间隔 60min
  - 启动时刻可配 (默认对齐 UTC 整点)
- [ ] **T1.4** Forgejo API client (issue list + label filter) (4h)
  - 复用 `forgejo` CLI wrapper (路径已知 `/home/dev/.npm-global/bin/forgejo`, per CLAUDE.md)
  - 支持 label-based filter (默认 `aria-auto`)
- [ ] **T1.5** Issue YAML schema validator (复用 M1 v0.1) (3h)
  - 直接复用 `openspec/archive/2026-04-23-aria-2.0-m1-mvp/artifacts/validate-issue-schema.py`
  - 验证 `id` / `title` / `description` / `expected_changes` / `ip_classification=synthetic`
- [ ] **T1.6** Extension 集成测试 (8h)
  - 启动 hermes + load extension, 触发 1 次手动 tick
  - 验证: tick handler 被调用, Forgejo API 可读 issue 列表, schema validator 拒绝 malformed issue
- [ ] **T1.7** Extension 部署到 dev (Aether `aria-build` heavy-1 节点, 复用 M1 base infra) (5h)
  - Nomad job 定义 (long-running service) + host volume 挂载 SQLite db
  - 启动验证: hermes process up, extension loaded, 第一次 cron tick 在 60min 内触发

**T1.done = Extension 在 dev 环境 long-running, 60min cron 自动触发, Forgejo issue 可读, schema validator 工作**

---

## T2 — SQLite WAL Schema + 持久化层 (8h)

**目标**: 实现 dispatches.db schema (per proposal.md §What 二), 含全部字段最小集 + UNIQUE idempotency 约束。

- [ ] **T2.1** schema DDL + migration 脚本 (3h)
  - 完整 CREATE TABLE (per proposal.md §What 二 SQL)
  - WAL mode + foreign keys + indexes
  - schema_version 字段 = "1.0" (per AD-M1-7 additive-only 治理)
- [ ] **T2.2** ORM-lite wrapper (Python sqlite3 + dataclass) (2h)
  - 不引入 SQLAlchemy (stdlib only, 继承 M1 stdlib unittest 风格)
  - `Dispatch` dataclass + `insert / get_by_issue / update_state / list_by_state` 方法
- [ ] **T2.3** WAL+重启可读测试 (2h, 验收 B)
  - 进程启动 → insert 5 rows → kill -9 → 重启 → 验证 5 rows 完整 + state 字段保留
- [ ] **T2.4** dispatches.db 禁存 payload guard (1h)
  - 静态 lint rule (T14 unit test): schema 不含 `issue_body` / `prompt` / `response` 列, 仅 metadata
  - 触发: 任何 PR 试图新增 payload 列 → CI fail

**T2.done = schema 落库 + WAL 重启测试 PASS + payload guard rule 生效**

---

## T3 — 10+S_FAIL 状态机核心 (16h)

**目标**: 实现完整 transition table (per proposal.md §What 一) + guards + advisory lock。

- [ ] **T3.1** transition table 定义 (3h)
  - 显式声明全部合法 (from, to) pair 与触发条件
  - 非法 transition → assertion error (M2 fail-fast, M3 reconciler 软处理)
- [ ] **T3.2** guard 函数实现 (4h)
  - S0 → S1 guard: 查 active dispatches (per OD-5a)
  - S1 → S2 guard: filter pass (label 匹配 + schema valid)
  - S4 → S5 guard: alloc started (poll Nomad)
  - S5 → S6 guard: alloc ended + result file exists
  - 全部 guard 单元可测
- [ ] **T3.3** advisory file lock (per OD-5f) (2h)
  - tick 启动前 `flock -n .aria/cache/hermes-tick.lock`
  - 锁失败 → log skip + 跳过本次 tick + 落 audit trail
- [ ] **T3.4** SQLite BEGIN EXCLUSIVE 事务包装 (2h)
  - 每次 transition 函数包在 `BEGIN EXCLUSIVE` ... `COMMIT` 事务内
  - 失败 → ROLLBACK + 不修改 state 字段
- [ ] **T3.5** 状态机主循环 (5h)
  - 单 tick 内: scan all non-terminal dispatches → 按 state 路由到 handler → handler 返回 next state → 持久化
  - 终态 (S9_CLOSE / S_FAIL) 跳过

**T3.done = 单 tick 可推进多个 dispatch + transition 全部合法 (单元测试) + advisory lock + 事务保护**

---

## T4 — Timeout + Heartbeat + S_FAIL Reason Enum (8h)

**目标**: 实现 timeout 触发 (per proposal.md §What 三) + S_FAIL forensic 字段填充 (per OD-5c)。

- [ ] **T4.1** S3/S5/S6 LLM timeout (2h)
  - OpenAI SDK timeout=120s (单次 call, 含 SDK 内 3 次 expo backoff)
  - 触发 → S_FAIL with `reason=timeout`, `failed_from_state` 记录
- [ ] **T4.2** S5_AWAIT alloc heartbeat 30min (3h)
  - cron tick 期间检查 `last_heartbeat_at` (Layer 2 容器周期写持久卷文件)
  - 缺失 > 30min → S_FAIL with `reason=timeout`
- [ ] **T4.3** 9 值 fail_reason enum 覆盖 (2h)
  - 全部 9 值 (`quota_exhausted` / `provider_5xx` / `timeout` / `schema_invalid` / `container_crash` / `dispatch_lost` / `review_rejected` / `infrastructure` / `other`) 在代码中作为 enum class
  - 每个失败路径显式赋值, 不允许 fallthrough 到 `other`
- [ ] **T4.4** S_FAIL forensic 字段填充 (1h)
  - 进入 S_FAIL 时必填 `fail_reason` + `fail_detail` + `failed_from_state`

**T4.done = 9 reason enum 全覆盖 + S3/S5/S6 timeout unit test + S_FAIL row 必含 forensic 字段**

---

## T5 — S0/S4 Idempotency (4h)

**目标**: 实现重复 dispatch 防护 (per OD-5a + qa R1 OBJ-2)。

- [ ] **T5.1** S0 → S1 active dispatch guard (1h)
  - SQL: `SELECT issue_id FROM dispatches WHERE state NOT IN ('S_FAIL', 'S9_CLOSE')`
  - 已存在则跳过, 不进 S1
- [ ] **T5.2** SQLite UNIQUE 约束实测 (1h)
  - 模拟两个 cron tick 同时 INSERT → 第二个抛 UNIQUE constraint violation → 跳过
- [ ] **T5.3** S4 Nomad meta idempotency_token (2h)
  - `dispatch_id = SHA256(issue_id || attempt_count)`
  - `nomad job dispatch -meta IDEMPOTENCY_KEY={dispatch_id}`
  - 重复 dispatch (Hermes crash recovery 简化场景) → Nomad 自动去重

**T5.done = 重复 dispatch unit test PASS (no double Nomad alloc) + UNIQUE 约束实测 PASS**

---

## T6 — Cron Tick 60min + 跨 Tick Polling (12h)

**目标**: 实现完整 cron tick 主循环 + S5_AWAIT 跨 tick 持续 (per US-022 §核心交付 line 32)。

- [ ] **T6.1** Hermes scheduler 注册 (3h)
  - 60min interval, UTC 整点对齐
  - 启动延迟 (避免与 owner 手动测试冲突)
- [ ] **T6.2** S5_AWAIT poll 逻辑 (4h)
  - 每次 tick 期间扫描所有 S5_AWAIT 行
  - 调 Nomad alloc API 检查状态: running → 留 S5; terminated → S6 (with result file 路径)
  - alloc lost → S_FAIL with `reason=dispatch_lost`
- [ ] **T6.3** 跨 tick state 一致性 (3h)
  - tick N 写 SQLite → tick N+1 读 SQLite, 中间不丢
  - kill Hermes 然后重启, S5 状态保留 (验收 B 弱形式)
- [ ] **T6.4** cron 重叠 skip 行为 (per T3.3) (2h)
  - 模拟 tick 跑超过 60min, 下个 tick 启动时 lock 已占
  - 验证: 第二个 tick log skip + 落 audit trail, 不并发写 SQLite

**T6.done = 60min cron 实测触发 + S5_AWAIT 可跨 ≥3 个 tick + 重叠 skip 验证 PASS**

---

## T7 — Layer 1 → Layer 2 ISSUE_ID + Prompt_Path 协议 (10h)

**目标**: 实现 Layer 1 → Layer 2 数据传递 (R7 / T2.4 hard cap), 复用 M1 bind mount 模式。

- [ ] **T7.1** prompt 渲染 + bind mount 写入 (3h)
  - 复用 M1 prompt template (`docker/aria-runner/prompts/issue-dispatch.md`)
  - 渲染后写 `/opt/aria-inputs/{dispatch_id}/prompt.txt`
  - 验证 size ≤ 100 KB (per T2.4 §6.2 客户端断言)
- [ ] **T7.2** Nomad meta 构造 (2h)
  - meta = `{ISSUE_ID, DISPATCH_ID, PROMPT_PATH}`, 总 size < 100 KB (Hermes 客户端断言)
  - 失败 → S_FAIL with `reason=infrastructure`, log "meta size exceeded"
- [ ] **T7.3** Nomad 错误分诊 rule (per T2.4 §6.3) (2h)
  - 监听 Nomad dispatch API 错误 string `"meta key value exceeds maximum"`
  - 命中 → log + S_FAIL (避免 silent failure)
- [ ] **T7.4** bind mount round-trip 测试 (3h)
  - 写 prompt.txt → dispatch alloc → alloc 内读 prompt.txt 验证内容一致
  - 复用 M1 inputs volume (`aria-runner-inputs`, 三节点已就绪)

**T7.done = prompt 写盘 + meta 100KB 断言 + 错误分诊 rule + round-trip 测试 PASS**

---

## T8 — silknode 集成 (8h)

**目标**: silknode OAI baseURL 调用 + AD-M0-8 主/fallback (air → flashx) + fallback log 字段。

- [ ] **T8.1** OpenAI SDK 客户端配置 (2h)
  - `base_url = "https://silknode.10cg.pub/v1"` (T0.5 确认 URL)
  - `api_key` 来自 Hermes secret store (复用 M1 Nomad Variables 模式)
- [ ] **T8.2** 主/fallback 切换逻辑 (3h)
  - 主调用 `glm-4.7-air`; 5xx 持续 (SDK 内 3 次 expo backoff 后仍 fail) → 切 `glm-4.7-flashx`
  - fallback 切换记录 `fallback_chain_json` 字段 (per OD-5e schema 完整)
- [ ] **T8.3** silknode 真实调用 smoke (2h)
  - dev 环境跑 1 次完整 dispatch, 验证 silknode 收到调用 (silknode 日志可见 metric-level meta, 不见 payload — 验证契约 1 no-storage)
- [ ] **T8.4** Aria 客户端 secrets/PII lint rule (1h)
  - 静态 lint: prompt 模板不含 `<secret>` / `<api_key>` / 已知 PII pattern
  - 命中 → CI fail

**T8.done = silknode 真实调用 PASS + fallback 切换 unit test + lint rule 生效 + 契约 1 metric-level 日志验证**

---

## T9 — Token Usage Tracking (5h)

**目标**: 持久化 token cost 数据 (per OD-5d, US-027 cost routing 依赖)。

- [ ] **T9.1** OpenAI SDK response 字段提取 (1h)
  - `usage.prompt_tokens` / `usage.completion_tokens`
  - silknode 是否透传 usage? T8 smoke 时验证, 不透传则 fallback 估算 (token count + 单价)
- [ ] **T9.2** 单价表 (1h)
  - `glm-4.7-air`: 输入 / 输出 USD per 1K tokens (实际 silknode 账单价, T0.5 owner 提供)
  - `glm-4.7-flashx`: 同上
- [ ] **T9.3** dispatches 表字段写入 (2h)
  - 每次 LLM call 后 update `token_usage_input/output/cost_usd/model_used`
  - 跨多次 call 累计 (S2/S3/S6 同 dispatch 内多次调用)
- [ ] **T9.4** 跨 dispatch 累计正确性测试 (1h)
  - 5 个 dispatch 跑完, SQL aggregate 应等于 silknode 账单 (允许 ±5% 误差)

**T9.done = token 字段填充 + 累计正确性测试 PASS**

---

## T10 — S6_REVIEW LLM 评审 (10h)

**目标**: 实现 S6_REVIEW LLM 评审逻辑 (per OD-3 silknode→GLM)。

- [ ] **T10.1** review prompt 模板 (2h)
  - 输入: Layer 2 输出的 PR diff + commit message + acceptance criteria
  - 输出 JSON: `{verdict: PASS|REVIEW_REJECTED, reason: str, code_quality_score: 0-10, scope_violations: []}`
- [ ] **T10.2** 单次 review 1 call + 1 retry on 5xx 限制 (per ai-engineer R1 silknode no-storage 强制) (2h)
  - 不允许 multi-turn dialogue (防 silknode 侧 cache 污染)
  - hash 同 dispatch_id 内 review prompt 命中复用 Aria 侧 cache
- [ ] **T10.3** verdict 路由 (2h)
  - PASS → S7_HUMAN_GATE
  - REVIEW_REJECTED → S_FAIL with `reason=review_rejected`
- [ ] **T10.4** review 准确率 evaluation (4h, synthetic ground truth)
  - 在 M1 fixtures 上手动标注 ground truth (PASS/REJECT)
  - 跑 review 测准确率, 目标 ≥ 80%
  - 不达标 → 调 prompt 模板, 不达标即 T10 fail (但不阻 M2 demo, M3 优化)

**T10.done = review verdict 准确率 ≥ 80% + 单次 1 call + cache 复用 unit test**

---

## T11 — S2 Image SHA Pin Guard (2h)

**目标**: 强制 immutable_sha (per AD-M1-2 / TL-R3-4)。

- [ ] **T11.1** dispatches.image_sha 字段填充 (1h)
  - dispatch 前从 `m1-handoff.yaml.image_refs.immutable_sha` 读取
  - 写入 `dispatches.image_sha` 字段
- [ ] **T11.2** S4 launch guard (1h)
  - `assert image_sha matches /^sha256:[a-f0-9]{64}$/`
  - 失败 → S_FAIL with `reason=infrastructure`, log "image_pin_violation"
  - 拒绝 mutable_tag (claude-latest)

**T11.done = non-sha256 image 拒绝测试 PASS**

---

## T12 — S7_HUMAN_GATE Feishu Webhook 桩 (6h)

**目标**: M2 仅 send-and-forget Feishu webhook (per OD-3 + 验收 = 桩, 完整 ack M4)。

- [ ] **T12.1** Feishu webhook URL + 签名 (1h)
  - URL 配置 (Hermes secret store)
  - 签名按 Feishu 文档 (复用现有 hermes feishu 集成 if any)
- [ ] **T12.2** 卡片模板 (2h)
  - 内容: dispatch_id / issue_title / PR URL / review verdict / "请 owner 在 Forgejo 上 merge PR 完成 dispatch"
- [ ] **T12.3** notification_status 字段落 SQLite (2h)
  - 字段记 webhook HTTP code (200 / 5xx / network_error)
  - 失败 (非 2xx) → log warning, **不**进 S_FAIL (per qa R1 OBJ-6: M2 桩静默失败可观测但不阻塞)
- [ ] **T12.4** 阻塞行为验证 (1h, per R3-OBJ-5)
  - S7 进入后, 状态机不再推进 (block-until-PR-merge)
  - cron tick 期间 S7 dispatch 仅检查 PR 是否 merged (S7 → S8 触发条件)

**T12.done = webhook send 成功 (即使 stub) + notification_status 字段落库 + S7 阻塞行为验证**

---

## T13 — S8_MERGE Forgejo PR API (6h)

**目标**: 确定性 merge + 幂等 marker 防重复评论。

- [ ] **T13.1** Forgejo PR API client (复用 forgejo CLI wrapper) (2h)
  - 列 PR / 检查 PR ready / merge PR
- [ ] **T13.2** 幂等 marker (2h)
  - PR 评论包含 `[aria-dispatch:{dispatch_id}]` 字符串
  - 重复 S8 进入时, 先扫 PR comments 查 marker, 命中则跳过评论 (但仍尝试 merge — Forgejo 侧自然幂等)
- [ ] **T13.3** S8 → S9_CLOSE 转换 (1h)
  - merge 成功 → S9_CLOSE
  - merge 失败 (PR 已 closed / conflict) → S_FAIL with `reason=infrastructure`
- [ ] **T13.4** 重复 S8 不重复评论测试 (1h)
  - 模拟 S8 retry (M2 不实现自动 retry, 但 owner 手动重置场景仍可能触发)

**T13.done = Forgejo merge API 成功 + marker 防重复评论测试 PASS**

---

## T14 — 状态机 Unit Test (10h)

**目标**: DI clock + alloc_status mock, fast-forward 60min cron 至毫秒级 (per qa R1 OBJ-7)。

- [ ] **T14.1** DI 接口设计 (3h)
  - `Clock` 接口: `now() -> datetime` (生产 = `datetime.utcnow()`, test = mock)
  - `AllocStatusProvider` 接口: `get_status(alloc_id) -> str` (生产 = Nomad API, test = dict lookup)
- [ ] **T14.2** 100+ unit tests (5h)
  - 覆盖全部 transition (S0→S1, S1→S2, ..., S8→S9_CLOSE) 合法 + 非法
  - 覆盖全部 timeout (S2/S3/S5/S6/S4/S8)
  - 覆盖全部 9 fail_reason
  - 覆盖 idempotency (S0/S4)
  - 覆盖 advisory lock skip
  - stdlib unittest (per M1 风格, 192 tests baseline)
- [ ] **T14.3** fast-forward cron 测试 (2h)
  - 测试内 60min cron 在 < 1s 内 simulate 多个 tick
  - 验证 S5_AWAIT 跨 ≥3 tick 行为

**T14.done = ≥ 100 unit tests + DI 接口完整 + fast-forward < 1s/cycle**

---

## T15 — M2 E2E Demo (12h)

**目标**: 验收 A (≥10 自动 dispatch) + 验收 D (perf ≤ M1 × 1.5)。

- [ ] **T15.1** dev 环境完整部署 (2h)
  - hermes + extension up, SQLite db 初始化, silknode 配置就位
- [ ] **T15.2** 10 个 synthetic issue 注入 Forgejo (2h)
  - DEMO-001/002 (M1 复用) + DEMO-003~010 (T0.4 新增 8 个 variants)
  - label `aria-auto` 触发 cron tick filter
- [ ] **T15.3** 实测 ≥3 个 cron tick 全程 (3h)
  - 第一 tick scan + dispatch 部分 issue
  - 第二 tick poll S5_AWAIT, 处理 S6/S7/S8
  - 第三 tick close 剩余
  - 全程不需 owner 介入 (除 S7 PR merge)
- [ ] **T15.4** Performance metrics 收集 (3h)
  - 单 issue dispatch 总时长 (S0 → S9_CLOSE 或 S_FAIL)
  - LLM call cumulative latency
  - 与 M1 baseline 对比 (`m1_handoff.performance_baseline.demo_002_p50_duration_s`)
- [ ] **T15.5** non-regression 验证 (验收 D) (2h)
  - `m2_demo_002_p50 ≤ m1_demo_002_p50 × 1.5`
  - 不达标 → triage (silknode latency? cron overhead? 状态机 transition 频次?)

**T15.done = 验收 A (≥10 issue auto dispatched) + 验收 D (perf ≤ 1.5x) + 全程无 owner 手工介入**

---

## T16 — M2 Report + Handoff + Patches (6h)

**目标**: 收尾产物, 准入 US-023 (M3) 起草。

- [ ] **T16.1** m2-handoff.yaml v1.0 起草 (2h)
  - additive-only on m1-handoff.yaml v1.0
  - 新增段 `m2_dispatches/*` (state machine metrics 聚合, 含 ≥10 dispatch 全部数据)
  - 字段: `total_dispatches / success_count / fail_count / fail_reason_breakdown / avg_p50_duration / token_cost_total / fallback_trigger_count`
- [ ] **T16.2** validate-m2-handoff.py 脚本 (1h)
  - 复用 M1 validator 模式 (`validate-m1-handoff.py`)
- [ ] **T16.3** 3 patches commit + merge + tech-lead 复核 (2h)
  - **Patch 1**: AD5 (`aria-orchestrator/docs/architecture-decisions.md` line 399 + 451-453)
  - **Patch 2**: PRD (`docs/requirements/prd-aria-v2.md` §M2 line 159 标题)
  - **Patch 3**: US-022 (`docs/requirements/user-stories/US-022.md` line 78 验收 B + line 87 §不在范围)
  - **注**: patch 内容已在 Phase A.1.3 起草完成 (per OD-4), T16.3 仅做最终 commit + merge + tech-lead 复核
- [ ] **T16.4** M2 Report (`docs/m2-report.md`) (1h)
  - 简洁报告 (M1 风格): go_decision / e2e_passed / metrics / lessons learned / handoff link
  - tech-lead co-sign 字段
  - owner sign-off 字段

**T16.done = m2-handoff.yaml validator PASS + 3 patches merged + M2 Report owner 签字 + brainstorm phase_a1_followup 7 项全部体现**

---

## 工时校验

| 阶段 | T# | 工时 |
|------|-----|------|
| Kickoff | T0 | 3h |
| Hermes Extension | T1 | 30h |
| 持久化 | T2 | 8h |
| 状态机核心 | T3 | 16h |
| Timeout + reason enum | T4 | 8h |
| Idempotency | T5 | 4h |
| Cron tick | T6 | 12h |
| Layer1→2 协议 | T7 | 10h |
| silknode 集成 | T8 | 8h |
| Token tracking | T9 | 5h |
| LLM review | T10 | 10h |
| Image pin | T11 | 2h |
| S7 webhook | T12 | 6h |
| S8 merge | T13 | 6h |
| Unit test | T14 | 10h |
| E2E demo | T15 | 12h |
| Report + handoff + patches | T16 | 6h |
| **Total** | **17 items** | **146h** |

**PRD baseline**: 140h
**Overrun**: 6h (4.3%, owner 已接受 OD-7=b 时确认)

---

## 依赖图 (简化)

```
T0 (kickoff)
 └─ T1 (Hermes Extension scaffold)
     ├─ T2 (SQLite schema)
     │   ├─ T3 (状态机核心) ─┬─ T4 (timeout+reason)
     │   │                    ├─ T5 (idempotency)
     │   │                    ├─ T6 (cron tick)
     │   │                    ├─ T11 (image pin)
     │   │                    ├─ T12 (S7 webhook)
     │   │                    └─ T13 (S8 merge)
     │   └─ T7 (Layer1→2 协议)
     │       └─ T13 (S8 依赖 T7)
     └─ T8 (silknode) ─┬─ T9 (token tracking)
                       └─ T10 (LLM review)
T3+T4+T6 ─→ T14 (unit test)
T1-T14   ─→ T15 (E2E)
T15      ─→ T16 (Report + handoff + patches)
```

**关键路径**: T0 → T1 → T2 → T3 → T4 → T6 → T15 → T16 (~88h)
**可并行**: T1 / T8 (Hermes 与 silknode 集成可并行); T11/T12/T13 在 T3 后可并行

---

## Status

- [ ] **Phase A.1.1**: proposal.md 起草完成 (2026-04-28, 348 行)
- [ ] **Phase A.1.2**: tasks.md 起草完成 (2026-04-28, 17 items 146h, 本文件)
- [ ] **Phase A.1.3**: 3 patches 起草完成 (待用户 review 后启动)
- [ ] **Phase A.2**: post_spec 审计 (待 owner 决策启动 / 跳过)
- [ ] **Phase A.3**: Agent 分配 (本文件已含 Agent 主责字段, 后续可由 task-planner 微调)
- [ ] **Phase B 准入**: owner Status: Draft → Approved

---

## Brainstorm M2 Scope → Tasks Mapping (per OD-1~OD-7 追溯)

| Brainstorm scope item | 工时 | Tasks T# 承载 | 备注 |
|----------------------|------|--------------|------|
| M2-1 状态机骨架 (transition table) | 16h | T3 | 全 transition + guards + advisory lock + 事务包装 |
| M2-2 SQLite WAL + 重启可读 | 8h | T2 | 验收 B 弱形式实现 |
| M2-3 S0 重复 dispatch idempotency | 4h | T5.1+T5.2 | UNIQUE issue_id WHERE state NOT terminal |
| M2-4 S3/S5 alloc timeout + heartbeat | 8h | T4.1+T4.2 | 含合并 (见下) |
| M2-5 S_FAIL reason enum + forensic 字段 | 6h | T4.3+T4.4 | **合并入 T4 (8h+6h=14h, 但 T4 总 8h)**: T4 整体重组合并 timeout+enum+forensic, 实际工时 ~14h 散落到 T4 (8h) + T13.3+T8.2 (S_FAIL 路径触发 ~6h 散落) |
| M2-6 token usage tracking | 5h | T9 | input/output/cost/model 字段 |
| M2-7 AD-M0-8 fallback log | 3h | T8.2 | 散落入 silknode 集成 |
| M2-8 cron tick advisory lock | 4h | T3.3 (2h) + T6.4 (2h) | 实现 + 验证拆分 |
| M2-9 silknode §99 verbatim 入 proposal | 2h | **A.1.1 已落 (proposal.md §What 六)** | T16 仅复核 |
| M2-10 Hermes Extension plugin | 30h | T1 | 全 7 子任务覆盖 |
| M2-11 60min cron tick + 跨 tick polling | 12h | T6 | 含 S5_AWAIT + 跨 tick 一致性 |
| M2-12 Layer 1 → Layer 2 ISSUE_ID + prompt_path 协议 | 10h | T7 | 含 R7 meta 100KB 客户端断言 |
| M2-13 Feishu webhook 桩 | 6h | T12 | M2 send-and-forget |
| M2-14 S2 image SHA pin guard | 2h | T11 | AD-M1-2 immutable_sha |
| ~~M2-15 S6/S8 partial-write 原子性~~ | ~~6h~~ | **已裁 (OD-7=b)** | 推 M3-2 reconciler |
| M2-16 状态机 unit test (DI clock) | 10h | T14 | fast-forward + 100+ tests |
| M2-17 M2 E2E demo (验收 A+D) | 12h | T15 | ≥10 dispatches + perf ≤ 1.5x |
| M2-18 M2 Report + handoff + tech-lead co-sign | 8h | T0 (3h) + T16 (6h) - 1h | T0 kickoff (3h) 拆出 + T16 (6h, M2-18 原 8h 已含 T16 全部职责); 总 9h vs M2-18 8h, +1h 余量 (per Phase A.1 内化的 T0 kickoff overhead) |
| **新增**: silknode 集成 (主/fallback 切换实现) | 8h | T8 | brainstorm 散落入 M2-1/M2-10 字段, 抽出独立 T 便于追责 |
| **新增**: S6 LLM review 实现 | 10h | T10 | brainstorm 散落入 M2-1, 因 LLM 准确率验收单独抽出 |
| **新增**: S8 Forgejo merge | 6h | T13 | brainstorm 散落入 M2-1, 抽出便于幂等 marker 单独管理 |
| **Total** | **152→146h** | **17 tasks** | OD-7=b 裁 M2-15 6h, 净 146h |

**重组说明**:
- brainstorm 18 scope items (152h) → tasks 17 items (146h) 通过 (a) M2-15 裁切 (-6h) + (b) silknode/LLM review/S8 merge 三项从 M2-1 状态机骨架 split out 单独 tracked (净 0h, 内部 reshuffle) + (c) T0 kickoff (3h) 从 M2-18 拆出便于跟踪
- 每个 brainstorm scope item 在 tasks 中可追溯 (此 mapping table 是 audit trail)
- 16+8+4+8+6+5+3+4+2+30+12+10+6+2+10+12+8 = 146h (M2-15 已裁) ✓

---

## Phase A.1.3 产出 (per OD-4, 不留到 T16 实施期)

按 OD-4 + brainstorm `phase_a1_outputs_expected`, 以下 patches 内容**在 Phase A.1.3 (现阶段) 起草完成**, T16.3 仅负责最终 commit + merge:

| Patch | 目标文件 | 内容 |
|-------|----------|------|
| **Patch 1** | `aria-orchestrator/docs/architecture-decisions.md` AD5 line 399 + 451-453 | 9 状态命名 → 10 状态命名 (per OD-1 PRD §M2) + LoC mapping 重算 (4 新增 → 5 新增, 100-200 LoC → 150-275 LoC, +25%) |
| **Patch 2** | `docs/requirements/prd-aria-v2.md` §M2 line 159 | 标题 "9 states" → "10 states" |
| **Patch 3** | `docs/requirements/user-stories/US-022.md` line 78 + 87 | 验收 B 降级 + §不在范围 reframe |

详细 patch 内容见同目录下 `patches/` 子目录 (Phase A.1.3 产出)。
