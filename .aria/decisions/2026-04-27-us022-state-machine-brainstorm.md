# US-022 State Machine Brainstorm — Final Decision

```yaml
agent: backend-architect
round: 3
group: discussion_integrator
status: FINAL_DRAFT_FOR_CHALLENGE_VERIFICATION
date: 2026-04-27
spec_ref: US-022 (M2 Layer 1 状态机)

# ============================================================
# SECTION 1: BACKGROUND — Q1 + Q1.5 决议链
# ============================================================

background:
  q1_decision:
    question: "silknode 是否可以作为 GLM provider 的合规代理层"
    decision: "YES — silknode (Luxeno 品牌) 经 r1-legal-memo v1.1 评估, 作为 OAI-compatible baseURL 使用"
    basis: "r1-legal-memo v1.1 IS-3/IS-4 合规评估 + silknode-integration-contract §契约 1"
    consumed_in_states: [S2_DECIDE, S3_BUILD_CMD, S6_REVIEW]

  q1_5_decision:
    question: "M2 使用哪个 GLM endpoint / fallback 策略"
    decision: "OAI-compatible endpoint only; 主: GLM-air, fallback: GLM-flashx (AD-M0-8 非对称设计)"
    anthropic_endpoint: "暂不启用 (M3 US-023 加双 provider fallback 时启用)"
    consumed_in_states: [S3_BUILD_CMD, S6_REVIEW]

# ============================================================
# SECTION 2: 10-STATE MACHINE DESIGN
# ============================================================

state_machine_design:

  states:

    - id: S0_IDLE
      type: normal
      role: "cron 等待 (60min tick), 系统入口"
      entry_from: [system_start, S9_CLOSE, S_FAIL]
      exit_to: [S1_SCAN]
      timeout: null
      key_actions:
        - "acquire advisory file lock (.aria/cache/hermes-tick.lock)"
        - "acquire SQLite BEGIN EXCLUSIVE"
        - "skip tick if lock already held by concurrent cron (OD-5f)"
      fields_written: [last_heartbeat_at]

    - id: S1_SCAN
      type: normal
      role: "heartbeat + triage (确定性规则, 不调 LLM)"
      entry_from: [S0_IDLE]
      exit_to: [S2_DECIDE, S0_IDLE]
      timeout: null
      key_actions:
        - "query Forgejo open issues via forgejo CLI"
        - "filter: labeled aria-auto + not already dispatched (UNIQUE issue_id check)"
        - "heartbeat: write last_heartbeat_at for all active dispatches"
        - "if no eligible issues → return to S0_IDLE"
      fields_written: [issue_id, last_heartbeat_at]

    - id: S2_DECIDE
      type: normal
      role: "分类决策: 是否值得自动化处理 (LLM triage call via silknode→GLM-air)"
      entry_from: [S1_SCAN]
      exit_to: [S3_BUILD_CMD, S9_CLOSE, S_FAIL]
      timeout_s: 120
      key_actions:
        - "call GLM-air via silknode OAI baseURL for issue classification"
        - "record token_usage_input / token_usage_output / model_used / fallback_triggered"
        - "if LLM call > 120s → S_FAIL(reason=timeout)"
        - "if response schema invalid → S_FAIL(reason=schema_invalid)"
        - "if decision=skip → S9_CLOSE (no work needed)"
      fields_written: [dispatch_id, token_usage_input, token_usage_output, token_cost_usd, model_used, fallback_triggered]

    - id: S3_BUILD_CMD
      type: normal
      role: "构建 hermes dispatch 命令 + 绑定 prompt_path (LLM call via silknode→GLM-air)"
      entry_from: [S2_DECIDE]
      exit_to: [S4_LAUNCH, S_FAIL]
      timeout_s: 120
      key_actions:
        - "call GLM-air via silknode OAI baseURL to generate dispatch command"
        - "validate image_sha is pinned (not mutable tag, AD-M1-2 guard)"
        - "bind prompt_path to Nomad meta < 100KB (Layer 1→2 protocol, R7)"
        - "record token usage (OD-5d)"
        - "if LLM call > 120s → S_FAIL(reason=timeout)"
        - "if mutable tag detected → S_FAIL(reason=schema_invalid)"
      fields_written: [prompt_path, image_sha, token_usage_input, token_usage_output, token_cost_usd, model_used, fallback_triggered]

    - id: S4_LAUNCH
      type: normal
      role: "dispatch Nomad alloc (idempotent, Hermes Extension Plugin)"
      entry_from: [S3_BUILD_CMD]
      exit_to: [S5_AWAIT, S_FAIL]
      timeout: null
      key_actions:
        - "pre-dispatch check: UNIQUE(issue_id) WHERE state NOT IN (S_FAIL, S9_CLOSE) (OD-5a)"
        - "Nomad meta key = hash(issue_id + attempt_count) for idempotency"
        - "call hermes-ext dispatch via Hermes Extension Plugin (Option C, AD3)"
        - "record alloc_id on success"
        - "if dispatch returns existing alloc_id → idempotent resume, proceed to S5_AWAIT"
        - "if dispatch fails → S_FAIL(reason=dispatch_lost)"
      fields_written: [alloc_id, state_entered_at]

    - id: S5_AWAIT
      type: normal
      role: "轮询 alloc 状态, 跨 tick polling (LLM-free, heartbeat-driven)"
      entry_from: [S4_LAUNCH]
      exit_to: [S6_REVIEW, S_FAIL]
      timeout_s: 1800  # 30min default (OD-5b)
      key_actions:
        - "poll Nomad alloc status at each 60min tick"
        - "update last_heartbeat_at on each poll"
        - "if alloc heartbeat absent > 30min → S_FAIL(reason=timeout)"
        - "if alloc status=dead AND exit_code!=0 → S_FAIL(reason=container_crash)"
        - "if alloc status=complete → proceed to S6_REVIEW"
      fields_written: [last_heartbeat_at]
      note: "S5 is the only multi-tick wait state; persisted in SQLite WAL for crash recovery (OD-2)"

    - id: S6_REVIEW
      type: normal
      role: "AI 评审 alloc 输出 (LLM call via silknode→GLM-air)"
      entry_from: [S5_AWAIT]
      exit_to: [S7_HUMAN_GATE, S8_MERGE, S_FAIL]
      timeout_s: 120
      key_actions:
        - "read alloc output artifact"
        - "call GLM-air via silknode OAI baseURL for review"
        - "sub-step bitmask tracking for partial-write atomicity (M2-15)"
        - "record token usage (OD-5d)"
        - "if LLM call > 120s → S_FAIL(reason=timeout)"
        - "if review=reject → S_FAIL(reason=review_rejected)"
        - "if review=needs_human → S7_HUMAN_GATE"
        - "if review=approve → S8_MERGE"
      fields_written: [token_usage_input, token_usage_output, token_cost_usd, model_used, fallback_triggered]

    - id: S7_HUMAN_GATE
      type: normal
      role: "人工审核门控 (Feishu webhook 桩, M2 = 发送即终)"
      entry_from: [S6_REVIEW]
      exit_to: [S8_MERGE, S9_CLOSE]
      timeout: null
      key_actions:
        - "send Feishu webhook notification (M2 stub: fire-and-forget)"
        - "record HTTP response code"
        - "M2: state terminal after webhook send; M3: polling for human response"
      fields_written: [state_entered_at]
      m2_scope_note: "M2 实现为发送即终止, 不等待人工回复; 完整门控推 M3"

    - id: S8_MERGE
      type: normal
      role: "合并 PR + 关闭 issue (idempotent)"
      entry_from: [S6_REVIEW, S7_HUMAN_GATE]
      exit_to: [S9_CLOSE, S_FAIL]
      timeout: null
      key_actions:
        - "check Forgejo PR title hash + comment idempotency marker before merge"
        - "sub-step bitmask: [pr_created, pr_approved, pr_merged, issue_closed]"
        - "if any sub-step already done (bitmask set) → skip idempotently"
        - "if merge fails → S_FAIL(reason=infrastructure)"
      fields_written: [state_entered_at]

    - id: S9_CLOSE
      type: terminal
      role: "成功终态, 记录完成"
      entry_from: [S8_MERGE, S2_DECIDE]
      exit_to: [S0_IDLE]
      timeout: null
      key_actions:
        - "write final state record"
        - "release advisory lock"
        - "log summary: issue_id / total_token_cost_usd / model_used / fallback_triggered"
      fields_written: [state_entered_at]

    - id: S_FAIL
      type: terminal
      role: "失败终态, 记录原因 + forensic (OD-5c)"
      entry_from:
        - S2_DECIDE
        - S3_BUILD_CMD
        - S4_LAUNCH
        - S5_AWAIT
        - S6_REVIEW
        - S8_MERGE
      exit_to: [S0_IDLE]
      timeout: null
      s_fail_is_universal_sink: true
      key_actions:
        - "write fail_reason enum value"
        - "write forensic fields (last state, alloc_id, token usage up to failure)"
        - "release advisory lock"
        - "log AD-M0-8 fallback detail if fallback_triggered=true (OD-5e)"
        - "M2: no auto-retry (OD-2, retry policy → M3)"
      fields_written: [fail_reason, state_entered_at, last_heartbeat_at]

  transitions:
    - from: S0_IDLE
      to: S1_SCAN
      trigger: "cron tick (60min)"
      guard: "advisory lock acquired AND BEGIN EXCLUSIVE acquired"

    - from: S1_SCAN
      to: S2_DECIDE
      trigger: "eligible issue found"
      guard: "issue_id not in active dispatch set"

    - from: S1_SCAN
      to: S0_IDLE
      trigger: "no eligible issues"
      guard: null

    - from: S2_DECIDE
      to: S3_BUILD_CMD
      trigger: "LLM decision=proceed"
      guard: "response schema valid AND call < 120s"

    - from: S2_DECIDE
      to: S9_CLOSE
      trigger: "LLM decision=skip"
      guard: null

    - from: S2_DECIDE
      to: S_FAIL
      trigger: "timeout OR schema_invalid OR provider_5xx"
      guard: null

    - from: S3_BUILD_CMD
      to: S4_LAUNCH
      trigger: "command built successfully"
      guard: "image_sha pinned AND prompt_path < 100KB"

    - from: S3_BUILD_CMD
      to: S_FAIL
      trigger: "timeout OR schema_invalid OR mutable_tag_detected OR provider_5xx"
      guard: null

    - from: S4_LAUNCH
      to: S5_AWAIT
      trigger: "alloc dispatched (new or idempotent resume)"
      guard: "UNIQUE(issue_id) check passed OR existing alloc_id matches"

    - from: S4_LAUNCH
      to: S_FAIL
      trigger: "dispatch_lost OR quota_exhausted"
      guard: null

    - from: S5_AWAIT
      to: S6_REVIEW
      trigger: "alloc status=complete AND exit_code=0"
      guard: null

    - from: S5_AWAIT
      to: S_FAIL
      trigger: "heartbeat_absent > 30min OR container_crash"
      guard: null

    - from: S6_REVIEW
      to: S7_HUMAN_GATE
      trigger: "LLM review=needs_human"
      guard: null

    - from: S6_REVIEW
      to: S8_MERGE
      trigger: "LLM review=approve"
      guard: null

    - from: S6_REVIEW
      to: S_FAIL
      trigger: "timeout OR review_rejected OR provider_5xx"
      guard: null

    - from: S7_HUMAN_GATE
      to: S8_MERGE
      trigger: "webhook_sent successfully (M2: auto-proceed)"
      guard: null

    - from: S7_HUMAN_GATE
      to: S9_CLOSE
      trigger: "webhook_send_failed (M2: graceful degradation)"
      guard: null

    - from: S8_MERGE
      to: S9_CLOSE
      trigger: "merge + issue close complete"
      guard: "all bitmask sub-steps confirmed"

    - from: S8_MERGE
      to: S_FAIL
      trigger: "merge failure"
      guard: null

    - from: S9_CLOSE
      to: S0_IDLE
      trigger: "next cron tick"
      guard: null

    - from: S_FAIL
      to: S0_IDLE
      trigger: "next cron tick (M2: no auto-retry)"
      guard: null

  terminal_states: [S9_CLOSE, S_FAIL]
  s_fail_universal_sink: true

# ============================================================
# SECTION 3: STATE FIELDS MINIMAL SET
# ============================================================

state_fields_minimal_set:

  - field: issue_id
    type: TEXT
    constraint: "UNIQUE WHERE state NOT IN (S9_CLOSE, S_FAIL)"
    rationale: "OD-5a idempotency guard; prevents duplicate dispatch"

  - field: dispatch_id
    type: TEXT
    constraint: "per dispatch attempt; idempotency key for Nomad meta"
    rationale: "hash(issue_id + attempt_count)"

  - field: state
    type: ENUM
    values: [S0_IDLE, S1_SCAN, S2_DECIDE, S3_BUILD_CMD, S4_LAUNCH, S5_AWAIT, S6_REVIEW, S7_HUMAN_GATE, S8_MERGE, S9_CLOSE, S_FAIL]
    rationale: "OD-1 PRD §M2 naming"

  - field: state_entered_at
    type: DATETIME
    constraint: NOT NULL
    rationale: "audit trail + timeout computation"

  - field: alloc_id
    type: TEXT
    constraint: nullable
    rationale: "set at S4_LAUNCH; used for S5_AWAIT polling"

  - field: prompt_path
    type: TEXT
    constraint: nullable
    rationale: "R7 bind mount; Layer 1→2 protocol; must be < 100KB content at path"

  - field: image_sha
    type: TEXT
    constraint: "must be digest-pinned (sha256:...), not mutable tag"
    rationale: "AD-M1-2 pin guard enforced at S3_BUILD_CMD"

  - field: fail_reason
    type: ENUM
    values:
      - quota_exhausted
      - provider_5xx
      - timeout
      - schema_invalid
      - container_crash
      - dispatch_lost
      - review_rejected
      - infrastructure
      - other
    constraint: nullable
    rationale: "OD-5c; set only in S_FAIL"

  - field: token_usage_input
    type: INTEGER
    constraint: nullable
    rationale: "OD-5d; cumulative across all LLM calls for this dispatch"

  - field: token_usage_output
    type: INTEGER
    constraint: nullable
    rationale: "OD-5d"

  - field: token_cost_usd
    type: REAL
    constraint: nullable
    rationale: "OD-5d; computed from model pricing"

  - field: model_used
    type: TEXT
    constraint: nullable
    rationale: "OD-5d; e.g. 'glm-4.7-air' or 'glm-4.7-flashx'"

  - field: fallback_triggered
    type: BOOLEAN
    default: false
    rationale: "OD-5d/5e; true if air→flashx fallback occurred per AD-M0-8"

  - field: last_heartbeat_at
    type: DATETIME
    constraint: nullable
    rationale: "S5_AWAIT timeout computation; updated each poll tick"

  - field: retry_count
    type: INTEGER
    default: 0
    rationale: "M2 always 0; M3 incrementable when retry policy added (OD-2)"

# ============================================================
# SECTION 4: TIMEOUT PATHS (OD-5b + OD-5c)
# ============================================================

timeout_paths:
  - path: "S2_DECIDE —[LLM call > 120s]→ S_FAIL"
    fail_reason: timeout
    implementation: "asyncio.wait_for / httpx timeout=120"

  - path: "S3_BUILD_CMD —[LLM call > 120s]→ S_FAIL"
    fail_reason: timeout
    implementation: "asyncio.wait_for / httpx timeout=120"

  - path: "S5_AWAIT —[alloc heartbeat absent > 30min]→ S_FAIL"
    fail_reason: timeout
    implementation: "compare last_heartbeat_at + now() at each tick; 30min = configurable default"
    configurable: true
    default_min: 30
    env_var: "HERMES_ALLOC_TIMEOUT_MIN"

  - path: "S6_REVIEW —[LLM call > 120s]→ S_FAIL"
    fail_reason: timeout
    implementation: "asyncio.wait_for / httpx timeout=120"

# ============================================================
# SECTION 5: IDEMPOTENCY STRATEGY (OD-5a)
# ============================================================

idempotency_strategy:

  s0_s1_filter:
    mechanism: "SQLite UNIQUE(issue_id) WHERE state NOT IN (S_FAIL, S9_CLOSE)"
    on_duplicate: "skip issue, log warning, continue to next eligible issue"
    note: "completed or failed issues are excluded from filter; allows re-dispatch after manual reset"

  s4_dispatch:
    mechanism: "Nomad dispatch meta key = hash(issue_id + attempt_count)"
    pre_dispatch_check: "query existing alloc by meta key before dispatching"
    on_existing_alloc: "resume at S5_AWAIT with existing alloc_id"
    on_new_dispatch: "record new alloc_id, proceed to S5_AWAIT"

  s8_merge:
    mechanism: "Forgejo PR title hash + idempotency comment marker in PR body"
    sub_step_bitmask: "[pr_created=1, pr_approved=2, pr_merged=4, issue_closed=8]"
    on_partial_completion: "read bitmask, skip completed steps, continue from first incomplete step"

# ============================================================
# SECTION 6: CRON CONCURRENCY PROTECTION (OD-5f)
# ============================================================

cron_concurrency_protection:
  layer_1_advisory_lock:
    mechanism: "fcntl LOCK_EX LOCK_NB on .aria/cache/hermes-tick.lock"
    on_conflict: "skip current tick, log 'tick skipped: concurrent execution detected'"
    release: "finally block on S9_CLOSE or S_FAIL"

  layer_2_sqlite_exclusive:
    mechanism: "SQLite BEGIN EXCLUSIVE transaction"
    scope: "state read + UNIQUE check + state write as atomic unit"
    on_conflict: "SQLITE_BUSY with timeout=5s; if still busy → skip tick"

  audit_trail: "both lock events (acquired / skipped) written to .aria/cache/hermes-audit.log"

# ============================================================
# SECTION 7: SILKNODE CONTRACT CONSUMPTION (OD-3)
# ============================================================

silknode_contract_consumption:

  source_spec: "openspec/changes/aria-2.0-silknode-integration-contract/proposal.md"

  verbatim_text_to_embed: |
    **silknode 代理 (Luxeno 品牌) 在 Aria 2.0 架构中必须保持 "API 调用透传, 不落地存储" 的行为**:

    - **禁止**: 在 silknode 侧对 issue body / code diff / Aria prompt / GLM response 进行任何形式的持久化
      (磁盘日志 / 内存缓存 > 单次请求生命周期 / 数据库存储 / 审计日志保留)
    - **允许**: 单次请求生命周期内的内存缓冲区 (用于协议转换 / 格式适配 / 错误重试)
    - **允许**: 指标级 meta 日志 (请求次数 / 延迟 / 错误码), 前提是不含 request/response payload 内容
    - **可追溯**: 若 silknode 新增任何落地行为, **必须**触发 r1-legal-memo v1.1 失效条件,
      重新评估 IS-3/IS-4 并更新 Memo 至 v2.0+

  placement_in_m2_proposal: "§外部依赖契约 (新增章节, Phase A.1 spec-drafter 负责)"
  cross_reference: "anchor link to silknode-integration-contract proposal.md + commit SHA pin"
  acceptance_checkmark: "M2 proposal §验收 add: [ ] silknode contract §99 第一项已满足"

  s5_s6_implementation_note: >
    S5_AWAIT / S6_REVIEW 经 silknode→GLM 调用受契约 1 no-storage 兜底;
    Aria 客户端 SHOULD NOT 在 prompt 内 inline secrets/PII;
    issue body / code diff 按契约 2 业务数据分类为"技术工单", 属于允许类别

  aria_client_obligation: >
    Aria M2 客户端不在 prompt 内嵌入: credentials / personal identity tokens /
    任何《数据安全法》重要数据类别内容

# ============================================================
# SECTION 8: M2 REQUIRED SCOPE (OD-5 全 6 项 + 其他必做项)
# ============================================================

m2_required_scope:

  - id: M2-1
    item: "状态机基本骨架 (10 状态 + S_FAIL transition table, SQLite schema)"
    od_ref: null
    estimate_h: 16

  - id: M2-2
    item: "SQLite WAL 持久化 + 启动恢复读 (验收 B 弱形式)"
    od_ref: OD-2
    rationale: "WAL persist + 进程重启后状态可读 + 不丢已 dispatched 记录; 完整 reconciler → M3"
    estimate_h: 8

  - id: M2-3
    item: "S0/S1 重复 dispatch idempotency: SQLite UNIQUE(issue_id)"
    od_ref: OD-5a
    estimate_h: 4

  - id: M2-4
    item: "S3_BUILD_CMD + S5_AWAIT alloc timeout (LLM 120s + heartbeat 30min default)"
    od_ref: OD-5b
    estimate_h: 8

  - id: M2-5
    item: "S_FAIL reason enum (9 values) + forensic 字段 (no auto-retry)"
    od_ref: OD-5c
    estimate_h: 6

  - id: M2-6
    item: "token usage tracking per dispatch: input/output/cost_usd/model_used/fallback_triggered"
    od_ref: OD-5d
    estimate_h: 5

  - id: M2-7
    item: "AD-M0-8 fallback 显式日志: air→flashx 触发时写 audit log + set fallback_triggered=true"
    od_ref: OD-5e
    estimate_h: 3

  - id: M2-8
    item: "cron tick advisory file lock + SQLite BEGIN EXCLUSIVE (skip-on-conflict)"
    od_ref: OD-5f
    estimate_h: 4

  - id: M2-9
    item: "silknode §99 verbatim 引用入 M2 proposal §外部依赖契约 (新增章节)"
    od_ref: OD-3
    estimate_h: 2

  - id: M2-10
    item: "Hermes Extension Plugin (Option C, AD3): 继承 M0 Spike POC (~286 LoC + 100-200 增量)"
    od_ref: "AD3 Option C"
    estimate_h: 30

  - id: M2-11
    item: "60min cron tick entry + 跨 tick polling loop (S5_AWAIT multi-tick wait)"
    od_ref: null
    estimate_h: 12

  - id: M2-12
    item: "Layer 1→2 ISSUE_ID + prompt_path 协议 (Nomad meta, R7 bind mount < 100KB)"
    od_ref: "R7"
    estimate_h: 10

  - id: M2-13
    item: "Feishu webhook 桩 (S7_HUMAN_GATE): fire-and-forget + HTTP code logging"
    od_ref: null
    estimate_h: 6

  - id: M2-14
    item: "S2/S3 image SHA pin guard: reject mutable tag at build command generation"
    od_ref: "AD-M1-2"
    estimate_h: 2

  - id: M2-15
    item: "S6/S8 partial-write 原子性: sub-step bitmask + idempotency key per sub-step"
    od_ref: null
    estimate_h: 6
    risk_note: "若实战未触发可降级为 reason=partial_write 监控 + M3 修复, 节省 6h"

  - id: M2-16
    item: "状态机 unit test suite: DI clock + alloc_status mock + fast-forward tick simulation"
    od_ref: null
    estimate_h: 10

  - id: M2-17
    item: "M2 E2E demo: DEMO-001 (happy path) + DEMO-002 (S_FAIL recovery); perf non-regression × 1.5"
    od_ref: null
    estimate_h: 12

  - id: M2-18
    item: "M2 Report + handoff: m2-handoff.yaml additive-only schema"
    od_ref: null
    estimate_h: 8

  total_estimate_h: 152
  budget_140h_baseline: 140
  overrun_h: 12
  overrun_pct: "8.6%"
  overrun_disposition: "Acceptable with risk annotation; M2-15 降级可节省 6h → 146h 接近预算"

  budget_mitigation:
    trigger: "M2-15 partial-write 在 E2E demo 中未触发"
    action: "降级为 S_FAIL reason=partial_write 监控日志; 完整 bitmask → M3"
    savings_h: 6
    adjusted_total_h: 146

# ============================================================
# SECTION 9: M3 DEFERRALS
# ============================================================

m3_deferrals:

  - id: M3-1
    item: "S_FAIL → 自动 retry policy (transient/permanent error 分类 + backoff)"
    rationale: "OD-2 显式决策; M2 retry_count=0 always; M3 根据实战 fail_reason 分布设计 policy"
    r_ref: "R1 Discussion D unanimous"

  - id: M3-2
    item: "完整 crash recovery: orphan alloc 清扫 + state replay + reconciler"
    rationale: "OD-2 验收 B 降级; M2 仅做 WAL persist 弱形式"
    r_ref: "R1 OBJ-7 / R2 OBJ-32"

  - id: M3-3
    item: "silknode quota 预检接口集成 (pre-flight quota check before S3_BUILD_CMD)"
    rationale: "需 silknode 团队提供 endpoint; 跨 repo 协调成本 > M2 scope"
    r_ref: "R2 OBJ-37"

  - id: M3-4
    item: "S_TIMEOUT 细分状态 (S_TIMEOUT_RUN vs S_TIMEOUT_REVIEW)"
    rationale: "M2 折叠为 S_FAIL reason=timeout; M3 根据实战 timeout 频率决策是否拆分"
    r_ref: "R1 OBJ-12"

  - id: M3-5
    item: "Anthropic endpoint 启用 + 双 provider (GLM + Claude) fallback chain"
    rationale: "Q1.5 已确认 M2 OAI-only; US-023 M3 承接"
    r_ref: "Q1.5 decision"

  - id: M3-6
    item: "S_FAIL 人工介入 CLI 工具 (hermes-ext reset-issue / requeue-issue)"
    rationale: "运维层工具; M3 配套 observability dashboard"
    r_ref: "R1 OBJ-19"

  - id: M3-7
    item: "AD3 Option C 0 hermes core 修改 vs S6/S7 polling 兼容性 final 验证"
    rationale: "M2 实施期可能触发; 不阻 brainstorm 但需 M2 E2E demo 验证后决策"
    r_ref: "R2 OBJ-36"

  - id: M3-8
    item: "observability hooks: Prometheus metrics export / OpenTelemetry spans"
    rationale: "M3 配套 dashboard; M2 仅做 audit log (structured JSONL)"
    r_ref: "R1 OBJ-22"

# ============================================================
# SECTION 10: PENDING PATCHES (delegated to Phase A.1)
# ============================================================

patches_pending:

  ad5_patch:
    trigger: "OD-1 选择 PRD §M2 命名后 AD5 9-state naming 需对齐 10-state PRD §M2"
    who: "Phase A.1 spec-drafter (delegated, OD-4)"
    patch_scope:
      - "AD5 line 399: rename 9 states → 10 states using PRD §M2 naming"
      - "AD5 line 399: add S9_CLOSE as 10th state"
      - "AD5 line 451-453: mapping table 重做 to reflect 10 states + S_FAIL"
    not_in_brainstorm_output: true

  prd_patch:
    trigger: "PRD §M2 line 159 标题写 '9 states' 但正文列 10 项 — PRD 自身 typo"
    who: "Phase A.1 spec-drafter (OD-4)"
    patch_scope: "PRD §M2 line 159 标题改为 '10 states + S_FAIL'"
    not_in_brainstorm_output: true

  us022_patches:
    - location: "US-022 line 78 §验收 B"
      change: >
        降级为: "SQLite WAL 持久化 + 进程重启后状态可读 + 不丢已 dispatched 记录
        (完整 reconciler + replay → US-023 M3)"
      who: "Phase A.1 spec-drafter"

    - location: "US-022 line 87 §不在范围 第一条"
      change: >
        改为: "Crash recovery 完整 reconciler + Replay → US-023 (M3);
        M2 仅做 WAL persist 弱形式 + 启动恢复读"
      who: "Phase A.1 spec-drafter"

# ============================================================
# SECTION 11: OWNER DECISIONS (OD-1 ~ OD-6)
# ============================================================

owner_decisions:
  date: 2026-04-27
  decided_by: "10CG Lab Owner (uni.concept.wzfq@gmail.com)"
  locked: true

  OD-1:
    summary: "命名采用 PRD §M2 10 状态: S0_IDLE / S1_SCAN / S2_DECIDE / S3_BUILD_CMD / S4_LAUNCH / S5_AWAIT / S6_REVIEW / S7_HUMAN_GATE / S8_MERGE / S9_CLOSE + S_FAIL"
    ad5_impact: "AD5 patch 对齐 delegated to Phase A.1 spec-drafter"

  OD-2:
    summary: "验收 B 降级为 WAL 持久化弱形式; 完整 reconciler → M3 US-023"
    us022_impact: "line 78 + line 87 patches delegated to Phase A.1"

  OD-3:
    summary: "S5_AWAIT / S6_REVIEW 评审走 silknode→GLM (LLM-based); silknode contract §99 verbatim 引用入 M2 proposal"
    compliance: "r1-legal-memo v1.1 IS-3/IS-4 兜底"

  OD-4:
    summary: "PRD §M2 patch + AD5 patch + US-022 patch 全部推到 Phase A.1 spec-drafter; brainstorm 不产 PR 或 diff"

  OD-5:
    summary: "以下 6 项全部 M2 必做"
    items:
      5a: "S0 重复 dispatch idempotency UNIQUE(issue_id) (~4h)"
      5b: "S3/S5 alloc timeout 默认 30min (~8h)"
      5c: "S_FAIL reason enum + forensic 字段, 不实现重试 (~6h)"
      5d: "token usage tracking: input/output/cost/model/fallback_triggered (~5h)"
      5e: "AD-M0-8 fallback 显式日志 air→flashx (~3h)"
      5f: "cron tick 重叠 advisory lock (~4h)"

  OD-6:
    summary: "brainstorm 输出 = 单文件 .aria/decisions/2026-04-27-us022-state-machine-brainstorm.md"

# ============================================================
# SECTION 12: AUDIT TRAIL — R1/R2/R3 OBJECTION DISPOSITION
# ============================================================

audit_trail:
  total_objections: 38
  breakdown:
    r1_objections: 28
    r2_new_objections: 10

  disposition_summary:
    resolved_by_owner_decisions: 24
    addressed_in_m2_required_scope: 10
    deferred_to_m3: 8
    remaining_open_for_phase_a1: 2  # AD5 patch + PRD §M2 patch

  r3_convergence_blockers_resolved:
    - blocker: "状态命名分歧 (AD5 vs PRD §M2)"
      resolution: "OD-1: PRD §M2 wins; AD5 patch delegated"

    - blocker: "验收 B 完整 reconciler feasibility"
      resolution: "OD-2:降级为 WAL 弱形式; reconciler → M3"

    - blocker: "silknode compliance 对 LLM-in-state-machine 的影响"
      resolution: "OD-3: silknode contract §99 verbatim embed; r1-legal-memo v1.1 兜底"

    - blocker: "brainstorm 是否直接产 PR/diff"
      resolution: "OD-4: No; all patches delegated to Phase A.1"

    - blocker: "OD-5 scope creep risk (6 mandatory items)"
      resolution: "OD-5: All 6 confirmed M2 必做; M2-15 有降级路径节省 6h"

    - blocker: "单文件 vs 多文件 brainstorm output"
      resolution: "OD-6: 单文件 .aria/decisions/"

# ============================================================
# SECTION 13: REFERENCES
# ============================================================

references:
  - id: REF-1
    doc: "openspec/changes/aria-2.0-silknode-integration-contract/proposal.md"
    note: "§契约 1 no-storage 约束文本 (verbatim source)"

  - id: REF-2
    doc: "docs/requirements/prd-aria-v2.md §M2"
    note: "10 states canonical naming; §M2 line 159 has pending patch"

  - id: REF-3
    doc: "aria/skills/hermes-extension/ (M0 Spike POC)"
    note: "Option C baseline; ~286 LoC; M2-10 継承"

  - id: REF-4
    doc: ".aria/decisions/2026-04-17-aria-2.0-m1-scope-reorg.md"
    note: "US-021/US-022 scope reorg decision; US-022 = M2 Layer 1 状态机"

  - id: REF-5
    doc: "docs/architecture/system-architecture.md §AD5"
    note: "9-state design (pre-OD-1); pending patch to 10-state alignment"

  - id: REF-6
    doc: "docs/requirements/prd-aria-v2.md §AD-M0-8"
    note: "GLM-air (主) / GLM-flashx (fallback) 非对称设计"

  - id: REF-7
    doc: "docs/requirements/prd-aria-v2.md §AD-M1-2"
    note: "image SHA pin requirement; enforced at S3_BUILD_CMD"

  - id: REF-8
    doc: "docs/requirements/user-stories.md US-022"
    note: "M2 Layer 1 状态机 acceptance criteria; pending 2 patches (OD-2)"

  - id: REF-9
    doc: "docs/decisions/r1-legal-memo-v1.1.md"
    note: "IS-3/IS-4 compliance evaluation; linked to silknode contract lifecycle"

  - id: REF-10
    doc: ".aria/decisions/2026-04-18-m1-phase-b-predraft-session.md"
    note: "M1 build infra context; Aether topology + Nomad Variables pattern"

# ============================================================
# SECTION 14: MERMAID STATE DIAGRAM
# ============================================================

mermaid_diagram: |
  stateDiagram-v2
      [*] --> S0_IDLE : system_start / S9_CLOSE / S_FAIL
      S0_IDLE --> S1_SCAN : cron tick (lock acquired)
      S1_SCAN --> S2_DECIDE : eligible issue found
      S1_SCAN --> S0_IDLE : no eligible issues
      S2_DECIDE --> S3_BUILD_CMD : LLM decision=proceed
      S2_DECIDE --> S9_CLOSE : LLM decision=skip
      S2_DECIDE --> S_FAIL : timeout / schema_invalid / provider_5xx
      S3_BUILD_CMD --> S4_LAUNCH : command built (SHA pinned)
      S3_BUILD_CMD --> S_FAIL : timeout / mutable_tag / provider_5xx
      S4_LAUNCH --> S5_AWAIT : alloc dispatched (idempotent)
      S4_LAUNCH --> S_FAIL : dispatch_lost / quota_exhausted
      S5_AWAIT --> S6_REVIEW : alloc complete (exit_code=0)
      S5_AWAIT --> S_FAIL : heartbeat_absent > 30min / container_crash
      S6_REVIEW --> S7_HUMAN_GATE : needs_human
      S6_REVIEW --> S8_MERGE : approve
      S6_REVIEW --> S_FAIL : timeout / review_rejected
      S7_HUMAN_GATE --> S8_MERGE : webhook sent (M2 auto-proceed)
      S7_HUMAN_GATE --> S9_CLOSE : webhook failed (M2 graceful)
      S8_MERGE --> S9_CLOSE : merge complete
      S8_MERGE --> S_FAIL : merge failure
      S9_CLOSE --> [*]
      S_FAIL --> [*]

# ============================================================
# SECTION 15: NEXT STEPS
# ============================================================

next_steps:
  phase_a1_inputs:
    - "此文件 (OD-1~OD-6 locked decisions)"
    - "M2 required scope 18 items (152h)"
    - "3 pending patches (AD5 / PRD §M2 / US-022)"
    - "silknode §契约 1 verbatim text (REF-1)"

  phase_a1_outputs_expected:
    - "US-022 proposal.md (updated: §验收 B 弱形式 + §外部依赖契约 + §不在范围 patch)"
    - "US-022 tasks.md (18 items decomposed)"
    - "AD5 patch (line 399 + line 451-453)"
    - "PRD §M2 line 159 patch"

  challenge_verification_gate:
    status: "FINAL_DRAFT_FOR_CHALLENGE_VERIFICATION"
    challenge_group: "pending"
    acceptance_criteria:
      - "全 10+S_FAIL 状态覆盖完整 (entry_from / exit_to / timeout 全部定义)"
      - "OD-5 全 6 项映射到具体状态/transition"
      - "silknode §99 verbatim 文本完整嵌入"
      - "M2 scope 152h 含预算风险注记"
      - "M3 deferrals 8 项来源可追溯"
      - "patches_pending 全部 delegated (不在 brainstorm output 内实施)"

# ============================================================
# SECTION 16: ROUND 3 CHALLENGE GROUP DISPOSITION (R3 patch)
# ============================================================

r3_challenge_disposition:
  cr_verdict: CONVERGED_WITH_MINOR_NOTES
  cm_verdict: CONVERGED_WITH_MINOR_NOTES (ready_for_owner_signoff=true)

  owner_action_required:
    - id: R3-OBJ-1
      severity: important
      issue: "M2 scope 152h vs PRD §M2 140h baseline 超 12h (8.6%) 未由 owner 显式签字"
      disposition: "已列入本节 owner_signoff_required, 等 owner sign-off 时一并确认; 备选裁剪项 = M2-15 partial-write 6h (若 E2E 不触发)"
      blocks_signoff: true

    - id: R3-OBJ-2
      severity: important
      issue: "ai-engineer R2 立场 (silknode quota 预检 M2 必做) 与 R3 final draft (推 M3) 冲突"
      disposition: "立场调和: silknode quota 预检需 silknode 团队提供 endpoint, 跨 repo 协调成本 > M2 直接价值; M3-3 deferral 维持; ai-engineer R2 立场标记为 'condition-not-met (silknode endpoint 未就绪)'; 若 M2 实施期 silknode 提供 quota endpoint, M2 可低成本回填"
      blocks_signoff: false

  phase_a1_followup:
    - id: R3-OBJ-3
      severity: minor
      action: "M2 proposal §约定偏离备注 1 行: 'PRD §M2 状态命名采用 SCREAMING_SNAKE_with_underscore (S0_IDLE), 偏离 Aria snake_case 约定, OD-1 锁定保留, AD5 patch 时 spec-drafter 显式记录 rationale'"

    - id: R3-OBJ-4
      severity: minor
      action: "M2 proposal §字段最小集 注 'fallback_triggered bool + 配套 log 字段 (trigger_reason / latency_ms / endpoint_from / endpoint_to) 由 A.1 spec-drafter 起草'"

    - id: R3-OBJ-5
      severity: minor
      action: "M2 proposal §状态语义 注 'S7_HUMAN_GATE 默认 block-until-PR-merge, 无 auto-pass timeout, A.1 spec-drafter 落地'"

    - id: R3-OBJ-cm-1
      severity: minor
      action: "M2 proposal §状态映射表 必含 POC 5 状态 → M2 10 状态对照行 + LoC 增量重算 (从 4 新增改 5 新增, 预算上调 ~25%)"

    - id: R3-OBJ-cm-2
      severity: minor
      action: "M2 proposal §角色定义 补 1 行: 'S7_HUMAN_GATE 中 human = owner (continues AD-M0-9)'"

    - id: R3-OBJ-cm-3
      severity: minor
      action: "M2 proposal §外部依赖契约 补 'prompt_path 指向文件 size ≤ 128 KiB' assertion (R7 hard cap)"

    - id: R3-OBJ-cm-4
      severity: minor
      action: "M2 proposal §运维契约 补 escalation matrix: S_FAIL retry 次数上限 / silknode 不可用降级路径 / S5 review 持续 LOW 触发 owner 介入"

  partially_resolved_carry_forward:
    - id: R1-OBJ-7-cr
      issue: "fallback log schema 待 A.1 落地"
      mapped_to: R3-OBJ-4
    - id: R2-OBJ-3-cr
      issue: "S7_HUMAN_GATE 阻塞行为待 A.1 落地"
      mapped_to: R3-OBJ-5
    - id: R2-OBJ-4-cr
      issue: "reconciler 骨架 vs deferral 边界 A.1 明确"
      mapped_to: phase_a1_outputs_expected (US-022 proposal §不在范围 patch)
    - id: R2-OBJ-5-cr
      issue: "10×10 transition 矩阵 A.1 落地"
      mapped_to: phase_a1_outputs_expected (US-022 tasks.md 18 items)
    - id: R2-OBJ-8-cr
      issue: "M3 deferrals 8 项 owner sign-off"
      disposition: "本节 owner_signoff_required 列, 与 OD-1~OD-6 合并签"
    - id: R2-OBJ-10-cr
      issue: "fail_reason enum 取值定义"
      mapped_to: phase_a1_outputs_expected (US-022 proposal §字段定义)
    - id: R1-OBJ-4-cm
      issue: "POC 5→10 mapping LoC 重算"
      mapped_to: R3-OBJ-cm-1
    - id: R1-OBJ-5-cm
      issue: "AD3 Option C M3 spike 验证"
      mapped_to: M3-7 deferral

  convergence_status:
    discussion_group_internal_consistency: TRUE (R3 single integrator)
    challenge_group_remaining_critical: 0
    challenge_group_remaining_important: 1 (R3-OBJ-1, blocks signoff, owner-action)
    challenge_group_remaining_minor: 7 (全部 phase_a1_followup, 不阻 signoff)
    overall_verdict: CONVERGED_PENDING_OWNER_SIGNOFF

# ============================================================
# SECTION 17: OWNER SIGN-OFF REQUIRED
# ============================================================

owner_signoff_required:
  - item: "OD-1~OD-6 决策内容"
    confirmed_in_brainstorm: true

  - item: "M2 scope 152h vs PRD 140h 超 12h (8.6%)"
    owner_decision: "OD-7 = b (2026-04-27) — **SUPERSEDED by OD-8 (2026-04-28)**"
    decision_detail: "裁剪 M2-15 partial-write (6h), 落 146h, partial-write 推 M3 配套 reconciler"
    blocking_phase_a1: false
    resolved: true
    superseded_note: |
      Phase A.1 post_spec audit (2026-04-28, cm F3) 暴露 tasks 工时实测累加 = 156h ≠ claim 146h,
      根因是 task 重组 (silknode/LLM review/S8 merge 抽出独立 task) 时 brainstorm M2 scope 18 项 (146h post-cut)
      与 tasks 17 项 (156h) 工时未真正 reconcile。Owner OD-8 = a (2026-04-28) 接受 156h 新基线,
      M2-15 partial-write 仍裁 (推 M3-2 reconciler), 净结果是 OD-7 文字 "146h" → "156h", 其他维度不变。

  - item: "M3 deferrals 8 项确认"
    owner_decision: "全部接受 (2026-04-27)"
    list:
      - id: M3-1
        item: "自动 retry policy (transient/permanent 分类)"
        estimate_h: 12
        m2_groundwork: "OD-5c reason enum + forensic 字段已落"
      - id: M3-2
        item: "完整 crash recovery + reconciler + replay (orphan alloc 清扫)"
        estimate_h: 30
        m2_groundwork: "OD-2 WAL persist 弱形式已落"
      - id: M3-3
        item: "silknode quota 预检接口集成 (ai-engineer R2 立场调和: condition-not-met silknode endpoint 未就绪)"
        estimate_h: 6
        m2_groundwork: "等 silknode 团队提供 GET /v1/quota; M2 实施期若上线可低成本回填"
      - id: M3-4
        item: "S_TIMEOUT 拆分细分 (S_TIMEOUT_RUN / S_TIMEOUT_REVIEW)"
        estimate_h: 4
        m2_groundwork: "OD-5c enum 含 timeout, 仅 enum→state 提升"
      - id: M3-5
        item: "Anthropic endpoint 启用 + 双 provider fallback (silknode Anthropic baseURL → Claude)"
        estimate_h: 10
        m2_groundwork: "OD-5e fallback_triggered 字段 + air→flashx 日志已就绪"
      - id: M3-6
        item: "S_FAIL 人工介入 CLI 工具 (hermes-ext reset-issue)"
        estimate_h: 4
        m2_groundwork: "OD-5c forensic 字段已落"
      - id: M3-7
        item: "AD3 Option C 0 hermes core 修改 final 验证 (M2 实施期天然触发, M3 ratify)"
        estimate_h: 3
        m2_groundwork: "M2 实施期 S6/S7 实装时验证, 违约即升级 ADR"
      - id: M3-8
        item: "observability hooks (Prometheus / OTel + Grafana dashboard)"
        estimate_h: 12
        m2_groundwork: "OD-5c/5d 字段已是 metrics 数据源"
    total_m3_estimate_h: 81
    m3_budget_share: "约 US-023 ~140h 预算的 58%"
    blocking_phase_a1: false
    resolved: true

  - item: "Brainstorm 输出 status: Draft → Approved (准入 Phase A.1)"
    owner_decision: "Approved (2026-04-27)"
    blocking_phase_a1: false
    resolved: true

  - item: "OD-8 (post_spec audit gap reconciliation): tasks 实测 156h vs OD-7=b 锁定 146h"
    owner_decision: "OD-8 = a (2026-04-28)"
    decision_detail: |
      接受 156h 新基线 (替代 OD-7=b 146h)。M2-15 partial-write 仍裁 (推 M3-2)。
      理由: task 重组真实成本 + M1 实战 +7% over 估算先例。PRD 140h baseline 偏离 +16h (11.4%) owner 接受。
    blocking_phase_b: false
    resolved: true
    audit_trail: ".aria/audit-reports/post_spec-2026-04-28T1700Z-us022-m2-layer1.md"

# ============================================================
# SECTION 18: FINAL M2 SCOPE (POST OD-7, 146h)
# ============================================================

final_m2_scope_146h:
  decision_ref: "OD-7 = b (M2-15 partial-write 推 M3-2 配套 reconciler)"
  removed_from_m2:
    - id: M2-15
      item: "S6/S8 partial-write 原子性 (sub-step bitmask + 幂等 key)"
      original_h: 6
      new_location: "M3-2 (完整 crash recovery + reconciler + replay) 一并实现"
      m2_mitigation: "S6/S8 失败仍走 S_FAIL with reason=partial_write, 监控触发后人工介入"
  retained_m2_scope_h: 146
  retained_m2_items: 17
  status: APPROVED

# ============================================================
# SECTION 19: BRAINSTORM CONCLUSION STATUS
# ============================================================

conclusion_status:
  document_status: APPROVED
  approved_date: "2026-04-27"
  approved_by: "owner (10CG Lab solo, AD-M0-9)"
  next_phase: Phase A.1 (spec-drafter)
  next_phase_inputs:
    - "本文件 (OD-1 ~ OD-7 全部 owner 决议锁定)"
    - "M2 final scope 146h (17 items, M2-15 removed)"
    - "M3 deferrals 8 items (81h, all accepted)"
    - "Phase A.1 followup checklist (R3-OBJ-3/4/5 + R3-OBJ-cm-1/2/3/4, 7 minor items 文档化)"
    - "3 pending patches (AD5 / PRD §M2 line 159 / US-022 line 78+87)"
  convergence_audit_trail:
    rounds_executed: 4
    total_objections_raised: 43  # R1: 28, R2: 10, R3: 9 (cr 5 + cm 4)
    total_resolved: 35  # OD 决议 + R3 patch 落地
    total_deferred_phase_a1: 7
    total_owner_action_required: 0  # all resolved by 2026-04-27
    total_carried_to_m3: 8  # M3 deferrals
    final_challenge_verdict_r4_cr: CONVERGED_PENDING_OWNER_ACTION (now resolved)
    final_challenge_verdict_r4_cm: CONVERGED_PENDING_OWNER_ACTION (now resolved)
    convergence_rule_satisfied: "讨论组内容稳定 (R3→R4 仅吸收 minor) AND 挑战组 0 new objection (R4)"
```
