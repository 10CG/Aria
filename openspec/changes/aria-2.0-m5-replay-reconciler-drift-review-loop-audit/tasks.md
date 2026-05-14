# M5 Tasks — Aria 2.0 Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable

> **Spec**: [aria-2.0-m5-replay-reconciler-drift-review-loop-audit](./proposal.md)
> **Level**: 3 (Full)
> **Status**: **Approved** (Phase A.2 R1+R2 SCOPE_OK_R2 4/4 2026-05-12; R2-cleanup applied 2026-05-13; Ready for Phase A.3 → B.1)
> **Brainstorm Source**: [.aria/decisions/2026-05-10-us025-m5-brainstorm.md](../../../.aria/decisions/2026-05-10-us025-m5-brainstorm.md)
> **Estimated total**: 130h baseline (R2 reconcile per TL-1; OD-M5-1 trigger 156h)
> **R2 fixes applied 2026-05-10**: 12 critical + theme-level important closed in proposal.md + tasks.md

---

## Task Group 总览

| Group | 主题 | 估时 | Phase |
|-------|------|------|-------|
| T-schema | Schema migration v3 → v4 (含 F + E) + db.py helpers | ~12h | Phase 1 |
| T-audit-log | Audit log 写入 instrumentation (8 event types) | ~10h | Phase 1 |
| T-risk-stub | F Risk-tier dual-write only (含 Phase 1 schema 部分) | ~3h | Phase 1 |
| T-cron-direct | G comment-poll direct transition + AD-M5-1 reframe | ~6h | Phase 2 |
| T-failure-analysis | B Reconciler Failure analysis + smart retry | ~15h | Phase 2 |
| T-rework-loop | D Review loop 双模式 hybrid (changes + redo) | ~50-55h | Phase 3 |
| T-replay | A Replay framework deterministic state replay | ~10h | Phase 4 |
| T-drift | C Drift defense Commit lint + Spec diff | ~12h | Phase 5 |
| T-acceptance | Tier-1 synthetic 验收 (12 explicit subtasks per criteria) | ~10-12h | Phase 6 |
| T-docs | m5-handoff.yaml + AD-M5-1..M5-N backfill + README | ~3h | Phase 6 |
| T-prd-reframe | PRD 同步 (US-025 done + AD-M5 references) | ~2h | Phase 6 |
| T-deploy | Production deploy on Aether light-1 (owner-runnable) | (owner) | Phase 6 |

---

## Phase 1 — Schema + Foundation (~25h, R2 fixes BA-1/BA-2/BA-4/BA-5/BA-6/BA-13/QA-2/QA-3/QA-4)

- [x] 1.1 起草 schema migration script 004_schema_v4_additive.sql (additive only: per proposal §Schema migration v3→v4 完整 SQL,含 rework_of TEXT FK / rework_feedback / retry_count / event_type CHECK / FK on audit_log)
  - **SPEC REFRAME (per feedback_spec_reframe_in_session, applied 2026-05-14 in M5 Phase 1 T1)**: proposal §SQL literal includes `ALTER TABLE dispatches ADD COLUMN retry_count INTEGER NOT NULL DEFAULT 0;`. The retry_count column already exists in canonical schema.sql since v2.0 (M3 baseline, schema.sql line 108). M5 reuses the existing column for the B Failure-analysis system-retry guard per QA-2 semantic intent; no new ADD COLUMN required. Re-adding would fail with SQLite "duplicate column name". Three-place documentation: (a) 004_schema_v4_additive.sql header, (b) commit message of aria-orchestrator 382a8b0, (c) this tasks.md note. Latent-bug class per feedback_pre_draft_bug_hunt_discipline.
- [x] 1.2 schema_migrate.py::apply_migrations 支持 003 → 004 升级路径 (3-safeguard inline per QA-4: atomic backup → dry-run on copy → integrity_check + row_count assert → apply on prod) + 单元测试
  - **DONE 2026-05-14 (T1)**: Migration 004 registered in `_MIGRATIONS` list with from_version_min=3.0 to_version=4.0. `_LATEST_SCHEMA_VERSION` bumped to "4.0". `_assert_human_decision_column_exists` pre-condition added (mirrors `_assert_cycle_start_ts_column_exists` M4 pattern). `migration_id == "004"` branch in `_apply_backfill_rules` writes documentation-only migration_notes audit row. **Bug fix bonus**: discovered + fixed naive `sql_text.split(";")` splitter bug in `apply_migrations` that broke on CREATE TRIGGER BEGIN/END bodies — replaced with `_split_sql_statements()` BEGIN/END-aware tokenizer. 531 PASS + 6 SKIP test suite (baseline preserved). **Out of scope for T1**: 3-safeguard inline pattern (atomic backup → dry-run → apply) is a T-deploy 6.18 inline pattern at deploy time, not in the runner — runner only does atomic migrate via BEGIN IMMEDIATE.
- [x] 1.3 db.py 新增 helper `append_audit_event(dispatch_id, event_type, payload)` (immutable INSERT, raises on UPDATE/DELETE attempt; DB write 失败时 log to stderr 不抛出 per BA-17)
- [x] 1.4 db.py 新增 helper `query_audit_log(dispatch_id, event_type?, since?, until?, limit=10000)` (R2 fix BA-10: dispatch_id required not Optional; default limit cap)
- [x] 1.5 db.py 新增 helper `get_risk_tier(dispatch_id)` (prefer risk_tier WHERE NOT NULL else fallback risk_tier_stub) — abi_compat #1 hot-swap 接口
- [x] 1.6 db.py 修改写入路径: 所有 dispatch INSERT 写 risk_tier='always' literal + risk_tier_stub='always' (R2 fix TL-2: 真正 dual-write 而非 NULL,满足 abi_compat #1 wording)
- [x] 1.6.5 db.py 加 helper `create_rework_dispatch(parent_id, mode, feedback)` (per AD-M5-2 lock + R2-cleanup BA-R2-2 retry mode branch):
  - if mode == 'retry': rework_round=0 (不消耗 owner cap), rework_of=parent.dispatch_id, rework_mode='retry', retry_count incremented separately
  - else (mode in 'changes','redo'): rework_round=parent.rework_round+1, rework_of=parent.dispatch_id, rework_mode=mode, rework_feedback=feedback
- [x] 1.6.6 db.py 加 helper `count_rework_chain(dispatch_id)` WITH RECURSIVE + LIMIT 10 depth guard (per BA-14: 防 cyclic data corruption) + R2-cleanup BA-R2-3: WHERE rework_mode IN ('changes','redo') (excludes 'retry' so system retries 不消耗 owner cap)
- [x] 1.7 单元测试: schema_migrate v3→v4 整体迁移 (in-memory DB + integrity_check + row count assert) + 3-safeguard 完整 fixture
- [x] 1.7.5 单元测试: schema migration 部分失败 rollback (per QA-13: 模拟 trigger creation fail → 验证 DB 不在 hybrid 状态)
- [x] 1.8 单元测试: dispatch_audit_log immutable triggers (UPDATE/DELETE 都 RAISE) + event_type CHECK 拒绝非法 enum + FK 拒绝 orphan dispatch_id
- [x] 1.9 单元测试: append_audit_event 8 event types 各写一条 + query_audit_log 排序 + filter + dispatch_id required parameter

## Phase 1 audit instrumentation (~10h, R2 fix QA-3 + AI-11: 用 AuditLogger middleware 不 caller-side)

- [x] 1.10 设计 AuditLogger interface (mockable injected at construction; NullAuditLogger 用于 existing tests + 不破坏 537 PASS, per R2 fix QA-3)
- [x] 1.10.5 单元 verify 537 tests pass with NullAuditLogger shim before instrumentation 实施
- [x] 1.11 ProviderRouter wrapper instrumentation (per AI-11): 装饰 call_llm / route_for_state, 自动 append_audit_event(event_type='llm_call', payload={model, tokens_in, tokens_out, cost, duration_ms, input_prompt(4KB cap), output_text(full), provider, fallback_chain_json}); 不需 caller 手动写
- [x] 1.11.5 grep integration test: 自动扫源码确保所有 ProviderRouter.call_llm 调用点附近 ≤5 行有 audit instrumentation (per AI-11 防漏写)
  - **REFRAMED 2026-05-14 (T5)**: With wrapper instrumentation (1.11), audit emission lives inside ProviderRouter itself; callers only need `dispatch_id=` arg. The 1.11.5 grep-test pattern made sense for caller-side instrumentation — under AI-11 wrapper design it's not directly applicable. Advisory regression pattern documented in T5 commit: scan source for `.call_llm(` without `dispatch_id=` within 5 lines as a future safeguard. Not a Phase 1 blocker. Test coverage of audit emission paths verified by `tests/test_t_provider_router_audit.py::TestProviderRouterPreM5Compat::test_router_with_audit_logger_but_no_dispatch_id_skips_emission` (catches the regression class).
- [x] 1.11.6 prompt redaction 中间件 (per AI-4 + AI-R2-1 扩展 pattern + QA-R2-2 execution order):
  - Patterns (cf. `standards/conventions/secret-hygiene.md §2`):
    credit-card, api-key, password, OAuth token, JWT (eyJ prefix), SSH private key (BEGIN PRIVATE KEY), DB conn string (postgres://, mysql://), AWS access key (AKIA…), nomad var literal, Forgejo PAT
  - **Execution order (R2-cleanup QA-R2-2 security-sensitive)**: redaction MUST apply **BEFORE** 4KB truncation; redaction-pass 后内容仍 > 4KB 则 truncation 只截 already-redacted text (boundary 不可能跨越 secret pattern)
- [x] 1.12 现有代码 instrumentation via AuditLogger: state transition 调用点 + human_decision update 调用点 (per R2 fix QA-3 mockable interface)
- [x] 1.12.5 dispatcher INSERT path 加 append_audit_event(event_type='risk_tier_classified', payload={tier: 'always', source: 'M5_stub'}) per TL-6
- [x] 1.13 单元测试: instrumentation 不破坏 M4 单元测试 (537 个原有测试 + NullAuditLogger 全 PASS, 不 regression)
- [x] 1.13.5 integration test: 一个 mock dispatch 全 cycle 后 audit_log 含 ≥3 llm_call event (S2 + S3 + S6) per AI-11 replay completeness invariant

## Phase 1 risk-stub 收尾 (~3h)

- [x] 1.14 validate-m5-handoff.py 加 check_risk_tier_migration_acknowledged (检查 schema 含 risk_tier + risk_tier_stub 双列 + M5 写入路径写 'always' literal not NULL, per R2 fix TL-2)
- [x] 1.15 文档: `aria-orchestrator/docs/architecture-decisions.md` 加 AD-M5-8 slot (risk_tier dual-write 接口边界 + 'always' literal rationale)

---

## Phase 2 — G + B (~21h)

### T-cron-direct (G, 6h, R2 fix BA-3 加 partial failure recovery)

- [x] 2.1 comment_poll.py::process_dispatch 在 update_human_decision 成功后 (CAS PASS) 直接调用 extension._handle_s7_human_gate(dispatch_id); 包 try/except 异常写 audit log 但不 rollback human_decision (immutable)
- [x] 2.2 兜底逻辑 (per R2 fix BA-3 + AD-M5-9 explicit): reconciler 30min 必须扫 `state=S7_HUMAN_GATE AND human_decision IS NOT NULL → re-attempt _handle_s7_human_gate(dispatch_id)` (不论 comment-poll liveness)
- [x] 2.3 单元测试: comment-poll direct transition 端到端 (mock approve → assert state=S8_MERGE within 1 tick cycle)
- [x] 2.4 单元测试: comment-poll partial failure 路径 (per R2 fix BA-3): CAS PASS 后 _handle_s7_human_gate raise → human_decision 已 commit + state 仍 S7 → reconciler 下一 tick 推进 to S8
- [x] 2.5 文档: `aria-orchestrator/docs/architecture-decisions.md` 加 AD-M5-1 slot (comment-poll direct transition reframe, supersedes AD-M4-9 § 决策 #4) + AD-M5-9 slot (partial failure recovery 契约)

### T-failure-analysis (B, 15h, R2 fixes AI-1/AI-2/AI-3/AI-8/AI-10/BA-7/QA-8)

- [x] 2.6 设计 Failure analysis LLM prompt template (input: fail_reason + last 3 llm_call events 含 prompt 摘要 + last 5 state_transition events per AI-10; output JSON {action, confidence, reason, suggested_owner_action}; prompt 末尾 'output ONLY valid JSON no markdown fence')
  - **摘要算法 (R2-cleanup AI-R2-3)**: first 500 chars of input_prompt + ts + model + tokens (metadata + prefix); 不调 LLM 二次生成 (cost discipline per AI-5)
- [x] 2.6.5 JSON parse fallback chain (per R2 fix AI-2): try parse → if malformed (markdown fence / extra text / wrong type) → regex extract → if still fail → 默认 action='notify_owner' + confidence=0.0 + reason='LLM JSON parse failed'; 写 audit log warn
- [x] 2.7 prompt template 版本管理 (放 `aria-orchestrator/aria-layer1/prompts/failure_analysis.md`, 加版本号 + audit log 记录使用版本)
- [x] 2.8 reconciler.py::_handle_failure_analysis 新方法: 当 dispatch 进入 S_FAIL 时调用 LLM analysis; **skip if fail_reason='changes_requested' or 'rework_exceeded'** (per R2 fix BA-6: owner-initiated 非 system failure)
- [x] 2.9 retry 路径 (per R2 fix BA-7 separate from rework cap): action='retry' + confidence >= ARIA_FAIL_RETRY_CONFIDENCE_MIN + retry_count < 1 + fail_reason in {'infrastructure', 'timeout'} → 调用 create_rework_dispatch(parent, mode='retry', feedback=reason); 新 row rework_round=0 不消耗 owner cap; retry_count++
- [x] 2.10 abort 路径: action='abort' → 写明确 fail_reason + final
- [x] 2.11 notify_owner 路径: action='notify_owner' → Feishu reject 卡片含 LLM 诊断 + suggested_owner_action
- [x] 2.12 ProviderRouter 接入 (per R2 fix AI-8): failure_analysis 调用 call_llm(prompt, 'glm-4.5-air'); MODEL_DEGRADE_LADDER['glm-4.5-air'] 当前 terminal → owner decision in AD-M5-6: 接受 terminal (优先稳定) OR 扩 ladder 加 glm-5-turbo (优先成功率); R2 lock 'terminal acceptable for M5, M6 evaluate based on real failure rate'
- [x] 2.13 audit log 写入: event_type='failure_analysis', payload=LLM 完整输出 + 是否触发 retry + raw_output (含 malformed JSON 原文 if applicable)
- [x] 2.13.5 nomadVar `ARIA_FAIL_RETRY_CONFIDENCE_MIN` 接入 (default=0.7, per R2 fix AI-3 与 spec drift threshold 对称)
- [x] 2.14 单元测试: 4 路径 (retry/abort/notify_owner/JSON parse fail) × mock LLM + boundary tests (confidence=0.70 boundary; confidence=null/malformed/out-of-range; action='unknown_value' → notify_owner default per R2 fix QA-8)
- [x] 2.15 集成测试: 真 fail dispatch + mock LLM → 验证完整 audit log 链路
- [x] 2.15.5 calibration spike (per R2 fix AI-3 + R2-cleanup QA-R2-3 信息层澄清): 用 M4 historical 13 条 S_FAIL fail_reason + 手动构造 synthetic mock context (M4 无 audit log table, 非真 historical replay) 离线跑 prompt → 统计 confidence 分布; 如果均值 > 0.85 → 提议阈值提到 0.85; 数据写入 AD-M5-6 + 注明 calibration data 是 synthetic, 生产部署后需用真 audit log 数据复核阈值
  - **OWNER-DEFERRED (Phase 2 P5)**: Calibration spike requires real LLM calls (~¥0.15 budget for 13 synthetic fixtures × glm-4.5-air). Spec status tracked in AD-M5-6 slot with "calibration data: synthetic only, NOT yet collected". Default threshold ARIA_FAIL_RETRY_CONFIDENCE_MIN=0.7 unchanged until owner runs spike + posts results. Threshold updates are nomadVar-only (runtime override, no code change).
- [ ] **2.15.6 live LLM acceptance (per R2 fix AI-1 + B.1.live)**: 至少 1 次真 ProviderRouter call to glm-4.5-air on a synthetic S_FAIL fixture → 验证 (a) JSON schema 合规 (b) confidence ∈ [0,1] (c) action 字段 ∈ enum (d) parse fallback 不触发 (健康路径)
  - **OWNER-DEFERRED to Phase 6 acceptance**: Tier-1 acceptance gate, NOT a Phase 2 P3-P6 blocker. Owner runs pre-merge OR during Phase 6 T-acceptance.B.1.live. Production wiring landed in P4 (`reconcile_runner._build_failure_analysis_caller` + `ARIA_FAILURE_ANALYSIS_ENABLED=1` opt-in env). Cost per run ≈ ¥0.01-0.02; Tier-1 budget ≤ ¥0.10 (4 live calls total: B.1.live + C.2.live + 2 boundary fixtures).
  - **Cost (R2-cleanup AI-R2-2)**: 每次 live call ~1-2K tokens ≈ ¥0.01-0.02; Tier-1 acceptance run 4 live calls (B.1.live + C.2.live + 2 boundary fixtures) ≤ ¥0.10; CI 不跑 live gate (避免 daily cost), 仅 owner 手动 trigger pre-merge OR Phase 6 acceptance
- [x] 2.16 文档: AD-M5-6 slot (Failure analysis LLM prompt 设计 + nomadVar + ladder decision + calibration data)

---

## Phase 3 — D Review loop (~50-55h, 最大 workpackage)

### T-rework-loop schema (~5h, Phase 1 已含 schema, 此处验证 + AD-M5-2 documentation)

- [x] 3.1 schema migration 包含 rework_of TEXT FK / rework_round / rework_mode / rework_feedback / retry_count columns (Phase 1 task 1.1 已含)
- [x] 3.2 db.py::create_rework_dispatch / count_rework_chain helpers (Phase 1 task 1.6.5 / 1.6.6 已含, 此处验证)
- [x] 3.3 文档: AD-M5-2 slot (rework chain 机制 documentation per R2 fix TL-10; per-row counter + rework_of FK 已 lock in §SQL; cap=3 含义: ≤3 rework rows allowed, round=4 reject)
- [x] 3.4 单元测试: rework chain 创建 + cap boundary (round=3 创建 OK, round=4 创建 reject + 当前 row → S_FAIL(rework_exceeded)) + 含 mode='retry' 不消耗 owner cap (per R2 fix BA-7)
- [x] 3.4.5 单元测试: cyclic rework_of chain (合成 corrupt data) → count_rework_chain 不 hang (LIMIT 10 guard 起效, raise or sentinel)

### T-rework-loop comment-poll protocol (~10h, R2 fixes BA-9/QA-9/QA-17/AI-9)

- [x] 3.5 comment_poll.py::parse_magic_string 扩展 4 commands (approve / reject / changes / redo)
- [x] 3.6 process_dispatch 路由: changes → create_rework_dispatch(mode='changes', feedback=feedback) + 当前 row S_FAIL(changes_requested) + rework_feedback=feedback (per R2 fix BA-6: 分离 fail_reason enum 与 rework_feedback text)
- [x] 3.7 process_dispatch 路由: redo → create_rework_dispatch(mode='redo', feedback=feedback) + 当前 row S_FAIL(changes_requested) + 添加 placeholder comment "Superseded — new PR pending (dispatch_id=<new_id>)" 旧 PR (per R2 fix BA-9: 不立即 close, 因新 PR# 未知); 实际 close + 写 "Superseded by #<new>" 在 S5_PR_CREATED handler (见 task 3.22)
- [x] 3.7.5 Forgejo PR close failure handling (per R2 fix QA-9): 包 try/except; 失败时 audit log event_type='rework_cycle' payload 含 close_status='failed'; 后续 reconciler tick 重试; 单元测试 mock Forgejo 5xx → 验证新 dispatch row 状态 OK 不 orphaned
- [x] 3.8 cap enforcement: 创建前检查 count_rework_chain(parent_id) > ARIA_REWORK_MAX_ROUND → 拒绝并 S_FAIL(rework_exceeded); 注意是 > 不是 >= (per R2 fix BA-2 语义 lock)
- [x] 3.9 nomadVar `ARIA_REWORK_MAX_ROUND` 接入 (default=3, override 可调) + startup validation: < 1 raise ConfigurationError (per R2 fix QA-17 防 cap=0/负值)
- [x] 3.10 audit log 写入: event_type='rework_cycle', payload={rework_of, rework_round, rework_mode, rework_feedback (truncated to 4KB), parent_pr_url, parent_dispatch_id} (per R2 fix AI-9)
- [x] 3.11 单元测试: 4 commands 各路径 + cap 边界 (round=3 创建 OK, round=4 拒绝 per R2 fix BA-2) + mixed mode (changes+redo+approve chain) + retry mode 不消耗 cap

### T-rework-loop changes mode (Layer 2 二次进入) (~20h)

- [ ] 3.12 设计 changes 模式 Layer 2 entrypoint (新 mode='rework-changes' 分支, prompt = 原代码 diff + feedback)
- [ ] 3.13 Layer 2 容器启动逻辑: rework-changes mode 时, fetch 原 PR branch + 接收 feedback prompt + AI 改稿
- [ ] 3.14 git push 策略: force-push 同 branch (per AD-M5-4 锁定方向; 备选 append-commit considered+rejected per R2 fix TL-10)
- [ ] 3.15 PR diff 演进: force-push 后 PR diff 自动更新, owner 看到 v1 → v2 演进
- [x] 3.15.5 changes mode state machine 入口 (per R2 fix BA-8): 新 row initial state S4_LAUNCH → fetch original branch + apply feedback → force-push → S5_PR_CREATED (PR 已存在 force-push updates) → S6_REVIEW; 若 S6 LLM 拒绝 changes-mode → S_FAIL(review_rejected) 不 auto-loop
- [ ] 3.16 S6_REVIEW LLM review (changes 模式跳 S2/S3, 节省 ~50% LLM cost — 实测见 task 3.27.5)
- [x] 3.16.5 changes mode audit log completeness (per R2 fix QA-6): 验证新 row audit log 不含 spurious S2/S3 state_transition events; Replay 时显示 'rework entry at S4/S6'
- [ ] 3.16.6 prompt assemble (per R2 fix AI-6): (a) 必须项 feedback + 原 issue body (b) 可选 file-by-file diff 按 'feedback 提到的 file' 优先 + hard cap 60K tokens, 超出 fallback redo mode + audit log warn
- [x] 3.17 Feishu 卡片: round 显示 "rework round 2/3 — changes mode" + 原 PR 链接 + new PR diff 链接
- [ ] 3.18 集成测试: changes 模式完整 cycle (mock /aria changes → 新 row → Layer 2 容器 → PR diff 更新 → S6→S7→approve)
- [ ] 3.18.5 集成测试 large-diff fixture (mock 80KB diff per R2 fix AI-6): 验证 truncation + fallback to redo mode 行为
- [x] 3.19 文档: AD-M5-3 slot (Layer 2 二次进入 mechanism + prompt 长度策略 + state machine 入口) + AD-M5-4 slot (force-push rationale)

### T-rework-loop redo mode (新 dispatch 全周期) (~12h)

- [ ] 3.20 redo 模式 Layer 2 entrypoint (mode='rework-redo', prompt = 原 issue + feedback, 不含原代码)
- [ ] 3.21 Layer 2 容器启动: redo mode 时走完整 S0 → S2 → S3 → S4 → S5 → S6 → S7 (新 PR 创建)
- [ ] 3.22 旧 PR close + 写 "Superseded by #<new>" comment 由 S5_PR_CREATED handler 执行 (per R2 fix BA-9: 解决 temporal ordering — 新 PR# 此时已生成); comment-poll 时仅写 placeholder "Superseded — new PR pending"
- [ ] 3.23 新 PR 描述自动包含原 issue + redo feedback + rework chain 完整链 (原 PR + new PR 双向链接)
- [x] 3.24 LLM cost 计入 audit log (full 100% cost vs changes 50% cost, replay 时可见对比)
- [x] 3.25 Feishu 卡片: round 显示 "rework round 2/3 — redo mode" + new PR 链接 + per-round mode label correctness (per R2 fix QA-7: mixed-mode chain 卡片显示正确 mode)
- [ ] 3.26 集成测试: redo 模式完整 cycle (mock /aria redo → 新 row → 全 state machine → 新 PR → S7→approve)
- [ ] 3.26.5 集成测试 redo timing (per R2 fix D.4): assert "Superseded by #<new>" comment 写入 in S5_PR_CREATED handler 不在 comment-poll 阶段

### T-rework-loop integration (~5h)

- [x] 3.27 mixed mode 测试 (per R2 fix QA-7): changes round 1 + redo round 2 + approve round 3; 验证 (a) cap 合并计数 (b) 每 round Feishu 卡片显示对应 mode (c) PR 链接正确
- [ ] 3.27.5 cost calibration spike (per R2 fix AI-5): mock 1 changes cycle + 1 redo cycle, 实测 LLM total cost 对比 vs M4 baseline; 写入 AD-M5-6 数据
- [x] 3.28 abi_compat #4 兼容性测试: 同一 row 多次写 human_decision 应被 CAS 拒绝 (first-decision-wins); 新 row 接力一次性写入
- [x] 3.29 AD-M5-2 Decided sign-off + cross-link to AD-M5-3 (Layer 2 二次进入) / AD-M5-4 (force-push rationale) (per R2 fix TL-R2-3 dedup: 3.3 is "slot 定义", 3.29 is "Decided sign-off after Phase 3 impl complete")

---

## Phase 4 — A Replay (~10h, R2 fixes BA-5/BA-18/QA-11/QA-18/AI-4)

- [x] 4.1 设计 replay output format = markdown only (per R2 fix BA-18 lock; JSON 推 M6); 文档化 AD-M5-10 forward-binding 'replay output 格式 M6 可加 JSON'
- [x] 4.2 aria_layer1/replay.py::replay(dispatch_id) 主入口 (返回 markdown 字符串)
- [x] 4.3 query audit log + dispatches 主表 join (用 db.py::query_audit_log)
- [x] 4.4 时间序输出: state 转换 + LLM 调用 (含 input_prompt 前 200 字符 + output_text 摘要 per R2 fix AI-4) + human decisions + rework cycles + failure analysis + drift detection 全部按 ts 排序
- [x] 4.5 rework chain 输出: 递归展开 rework_of 链 (round 1 → round 2 → round 3) + NULL rework_mode 处理 (per R2 fix BA-5: 根 dispatch rework_mode=NULL 显示 'origin')
- [x] 4.6 markdown 渲染: 表格 + 链接 + 代码块 + Forgejo PR 链接
- [x] 4.7 文件输出: 默认 stdout, `--output-file` 选项写入 `.aria/replay-reports/{dispatch_id}.md`; dispatch_id sanitize (per R2 fix QA-18: 替换非 alphanumeric/dash/underscore 为 underscore 防 path traversal)
- [x] 4.8 单元测试: replay 各种场景 (无 rework / 1 round changes / 2 round mixed / 含 failure analysis / 含 drift / NULL rework_mode 根 dispatch / dispatch_id 含特殊字符)
- [x] 4.9 集成测试 (per R2 fix QA-11): replay 合成 dispatch (manually seeded audit log entries, 不依赖 M4 production 数据) + pre-M5 dispatch graceful degrade ('audit log: no entries (pre-M5 dispatch)')

---

## Phase 5 — C Drift defense (~12h)

### T-drift commit lint (~5h, R2 fixes QA-5/BA-16)

- [ ] 5.1 设计 commit lint 规则 (Conventional Commits + Aria scope conventions: type prefix / scope 含 milestone / title ≤ 70 / Closes #N)
- [ ] 5.2 aria_layer1/commit_validator.py::validate_commit_message 实现 regex 验证
- [ ] 5.3 Layer 2 hook: AI 写 commit 前调用 validate_commit_message, 不通过则 force AI 重写 (prompt 加 violation feedback); **max 3 重试 per R2 fix BA-16**, 第 3 次失败 dispatch → S_FAIL(commit_lint_failed) with fail_reason detail 含 violations
- [ ] 5.4 audit log 写入: event_type='commit_lint_result', payload={passed, violations, raw_message, retry_attempt}
- [ ] 5.5 单元测试 12 enumerated fixtures (per R2 fix QA-5):
  - (1) valid `feat(M5): title ≤70` + `Closes #N`
  - (2) missing type prefix
  - (3) unknown type (e.g. 'style' vs 'feat' for code)
  - (4) title > 70 chars
  - (5) missing Closes #N
  - (6) scope missing milestone
  - (7) bare fix: no scope
  - (8) breaking change footer
  - (9) multi-line body valid
  - (10) empty body
  - (11) Unicode title
  - (12) trailing whitespace in type

### T-drift spec diff (~7h, R2 fixes BA-12/QA-15/AI-5/AI-7)

- [ ] 5.6 设计 Spec diff LLM prompt template; input slicing (per R2 fix AI-7): 不传 raw proposal.md, 仅传 extracted '## What' + '## Acceptance criteria' 章节 (regex 抽); PR diff 排除 generated/lock/migration-script 文件
- [ ] 5.6.5 cost spike (per R2 fix AI-5): 用 1 个真 M4 PR (3KB diff) 跑 prompt 实测 input tokens + cost; 写入 AD-M5-5 数据
- [ ] 5.6.6 calibration spike (per R2 fix AI-7): 5-10 个真 M4 PR offline run, 校验 false-positive 率 < 30%
- [ ] 5.7 prompt template 版本管理 (`aria-orchestrator/aria-layer1/prompts/spec_drift.md`)
- [ ] 5.8 dispatcher.py::_check_spec_drift 新方法: dispatch **S8_MERGE only** 后调用 LLM 比较 (per R2 fix BA-12 + QA-15: S_FAIL 类 dispatches 不触发, 无 merged code to compare; per-rework-cycle drift 记录在每 round audit log 含 rework_round tag)
- [ ] 5.9 ProviderRouter 接入: spec_drift 用 call_llm(prompt, 'glm-4.5-air'); ladder terminal (per AI-8 lock)
- [ ] 5.10 阈值判断: score < ARIA_SPEC_DRIFT_THRESHOLD → 触发 Feishu drift 警告卡片 (build_drift_alert_card)
- [ ] 5.11 nomadVar `ARIA_SPEC_DRIFT_THRESHOLD=70` 接入 (default 70, owner 可调)
- [ ] 5.12 audit log 写入: event_type='spec_drift_detected', payload={score, deviations, extra_changes, input_prompt(4KB cap), raw_output, rework_round}
- [ ] 5.12.5 JSON parse fallback (per R2 fix AI-2 spec drift 同模式): malformed JSON → 默认 score=NULL + 不触发 Feishu 卡片 + audit log warn
- [ ] 5.13 单元测试: 多 score 阈值 + Feishu 卡片 mock + audit log + JSON parse fail fixtures (5+ malformed samples per R2 fix AI-2)
- [ ] 5.14 集成测试: S8_MERGE dispatch + mock LLM → 完整 drift detection 链路; **negative test**: S_FAIL dispatch 不 trigger spec_drift_detected (per R2 fix BA-12)
- [ ] **5.14.5 live LLM acceptance (per R2 fix AI-1 + C.2.live)**: 至少 1 次真 ProviderRouter call to glm-4.5-air on 1 mock PR diff → 验证 JSON 合规 + score ∈ [0,100]
- [ ] 5.15 文档: AD-M5-5 slot (spec_drift 阈值 + nomadVar + input slicing + cost spike 数据)

---

## Phase 6 — Acceptance + Docs + Deploy

### T-acceptance (~10-12h, R2 fix QA-1 严重扩展 — M4 模式 1:1 mapping)

每个 Tier-1 criterion 单独 subtask, M4 T-acceptance.A.1/B/C/D.1/D.2/E/F 模式扩展到 M5 12 criteria:

- [ ] 6.1 T-acceptance.A.1 — Replay output 完整性测试 (state 时间线 + LLM prompt+response + rework chain) (~1h)
- [ ] 6.1.1 T-acceptance.B.1 — Failure analysis mock LLM 4 路径 (retry/abort/notify_owner/JSON parse fail) + confidence boundary (~1h)
- [ ] 6.1.2 T-acceptance.B.1.live — Failure analysis live LLM gate (per R2 fix AI-1; 真 glm-4.5-air call verify JSON 合规) (~1h)
- [ ] 6.1.3 T-acceptance.C.1 — Commit lint 12 enumerated fixtures (per task 5.5) (~1h)
- [ ] 6.1.4 T-acceptance.C.2 — Spec diff mock LLM + score 计算 + S_FAIL skip + input slicing (~1h)
- [ ] 6.1.5 T-acceptance.C.2.live — Spec diff live LLM gate (真 LLM call on mock PR diff) (~0.5h)
- [ ] 6.1.6 T-acceptance.D.1 — /aria changes + /aria redo + mixed mode × 3 rounds 集成测试 (~1.5h)
- [ ] 6.1.7 T-acceptance.D.2 — rework_round cap boundary (round=3 OK, round=4 reject + S_FAIL(rework_exceeded)) (~0.5h)
- [ ] 6.1.8 T-acceptance.D.3 — abi_compat #4 first-decision-wins CAS test (~0.5h)
- [ ] 6.1.9 T-acceptance.D.4 — redo PR close 时序 (S5_PR_CREATED handler 写 "Superseded by") (~0.5h)
- [ ] 6.1.10 T-acceptance.D.5 — Forgejo PR close failure handling (mock 5xx, 不 orphaned) (~0.5h)
- [ ] 6.1.11 T-acceptance.E.1 — Schema migration v3→v4 3-safeguard inline 测试 (~1h)
- [ ] 6.1.12 T-acceptance.E.2 — Audit log immutable (UPDATE/DELETE RAISE + event_type CHECK + FK orphan) (~0.5h)
- [ ] 6.1.13 T-acceptance.F.1 — risk_tier 'always' literal write + validate-m5-handoff.py check (~0.5h)
- [ ] 6.1.14 T-acceptance.G.1 — comment-poll direct transition < 60s + partial failure reconciler 兜底 (~1h)
- [ ] 6.1.15 T-acceptance.HMAC.1 — Feishu HMAC oracle test (per R2 fix TL-8: fixture-based 防 M4 paper-fix 复发, independent of code) (~1h)
- [ ] 6.2 单元测试 + 集成测试合计 ≥ 600 PASS from ≥30 new test functions (≥15 为 behavioral integration tests, per R2 fix QA-14)
- [ ] 6.3 abi_compat_promises 验证 cross-reference: 4 promises 全部 enforced (validate-m5-handoff.py 4 个 check 函数 PASS) — 依赖 task 6.6 完成 (per R2 fix QA-12 task ordering)
- [ ] 6.4 性能测试: comment-poll direct transition max latency < 60s (per R2 fix QA-20: max over ≥3 dispatches synthetic)

### T-docs (~3h, R2 fixes TL-3/TL-9/TL-14/AI-12)

- [ ] 6.5 m5-handoff.yaml schema (additive on m4-handoff schema v1.0) — 含 m5_acceptance / m5_human_gate_metrics / abi_compat_promises (M5→M6 5 candidates per AD-M5-10) / ad_m5_status / effort / signoffs / open_issues_for_m6 / audit_trail / m4_handoff_cross_reference
- [ ] 6.6 validate-m5-handoff.py (per R2 fix QA-12 必须在 task 6.3 之前完成):
  - [ ] 6.6.1 check_risk_tier_migration_acknowledged (per abi_compat #1) — 验证 schema 含 risk_tier+stub 双列 + 写入路径 'always' literal
  - [ ] 6.6.2 check_unique_index_preserved (per abi_compat #2) — 验证 uq_approval_comment 存在 + partial WHERE NOT NULL 语义
  - [ ] 6.6.3 check_comment_poll_job_independent (per abi_compat #3) — grep deploy/*.nomad.hcl 验证 aria-layer1-comment-poll job 存在 type=batch
  - [ ] 6.6.4 check_first_decision_wins_preserved (per abi_compat #4) — code scan + integration test
  - [ ] 6.6.5 check_all_11_ad_m5_decided (per R2 fix TL-9) — mechanical assert AD-M5-1..AD-M5-11 全 Decided
  - [ ] 6.6.6 单元测试: 运行 validator on committed m5-handoff.yaml canonical instance, 全 6 checks PASS (per `feedback_validator_repo_drift_guard_test`)
- [ ] 6.7 AD-M5-1..AD-M5-11 全部 backfill (per R2 fix TL-9: 显式 1..11 不用 N; Phase B 实施期填充, Phase 6 verify 全 Decided)
- [ ] 6.8 README.md 同步: aria-layer1 plugin.yaml version 0.3.0 → 0.4.0 + M5 features 章节
- [ ] 6.9 architecture-decisions.md AD-M5-1..AD-M5-11 全部填充 (slot → Decided)
- [ ] 6.10 文档: AD-M5-7 slot (Audit log retention 策略, M5 不 archival; M6 trigger condition per R2 fix AI-12: '累积 ≥30 dispatches 且 LLM retry rate spike OR commit_lint failure > 20%')
- [ ] 6.11 文档: AD-M5-9 slot (comment-poll partial failure recovery + reconciler 兜底契约)
- [ ] 6.12 文档: AD-M5-10 slot (5 candidate forward-binding M5→M6 promises per R2 fix TL-14 enumerated in proposal §AD-M5-10)

### T-prd-reframe (~2h)

- [ ] 6.13 PRD §M5 锁 actual scope (M5 actual_scope_locked: 5 PRD + F + G; H 推 M6)
- [ ] 6.14 PRD §User Stories 表 US-025 → done
- [ ] 6.15 PRD §M6 加 H aria-layer2-runner deploy + F.algorithm + A.advanced + C.advanced + B.advanced (deferred items)
- [ ] 6.16 prd-aria-v2.md 版本 bump (v2.1.0 → v2.2.0, M5 done milestone)

### T-deploy (Phase 6, owner-runnable, post-merge; R2 fixes TL-8/QA-13)

- [ ] 6.17 Pre-deploy: SSH light-1 + git pull + git checkout master + pip install -e refresh (per `feedback_handoff_doc_assumes_venv_ready_smell`)
- [ ] 6.18 Schema migration: 3-safeguard pattern inline (per R2 fix QA-4):
  - [ ] 6.18.1 atomic backup via Python sqlite3.backup() (WAL-safe) → /opt/aether-volumes/aria-layer1/data/backups/dispatches.db.pre-m5.<timestamp>
  - [ ] 6.18.2 integrity_check on backup → assert OK
  - [ ] 6.18.3 dry-run on copy: shutil.copy backup → /tmp/dispatches.dryrun.db → apply_migrations → assert integrity_check OK + row count unchanged
  - [ ] 6.18.4 apply on prod: same apply_migrations → assert integrity_check OK + row count unchanged + new cols present
  - [ ] 6.18.5 rollback verification (per R2 fix QA-13): backup DB 可 restore via schema_migrate.py + integrity_check PASS
- [ ] 6.19 nomadVar 配置: `ARIA_REWORK_MAX_ROUND=3` + `ARIA_SPEC_DRIFT_THRESHOLD=70` + `ARIA_FAIL_RETRY_CONFIDENCE_MIN=0.7` (per R2 fix AI-3) + 其他新增 secrets (TBD per Phase 6)
- [ ] 6.20 nomad job validate + aether dev run (aria-layer1-comment-poll + aria-layer1-reconcile redeploy with M5 code)
- [ ] 6.20.1 HCL cron syntax pre-validate (per R2 fix TL-8 Track A discovery): grep effective-cadence in alloc 第 1 个 tick logs, 验证 Next Periodic Launch ≤ 60s (5-field 1-min + --continuous) 不退化到 30min
- [ ] 6.21 Verify alloc + clean ticks (1 cron cycle + 1 comment-poll cycle + 1 reconcile cycle 都跑过, audit log 写入正常)
- [ ] 6.21.1 verify aria-runner-template (M2 era stub) alloc 存在 (per R2 fix TL-8: aria-layer2-runner 缺失但 stub 仍 work for synthetic test); 文档化 Tier-2 D.2.real 阻塞 (推 M6)
- [ ] 6.22 Smoke E2E (类比 M4 Track A): SQL inject S7 dispatch + send Feishu card + /aria changes → 验证改稿模式 cycle
- [ ] 6.23 Smoke E2E redo: SQL inject + /aria redo → 验证重做模式 cycle
- [ ] 6.24 Smoke E2E rework cap: 创建 round=3 dispatch + /aria changes round=4 → 验证 S_FAIL(rework_exceeded)
- [ ] 6.25 m5-handoff.yaml writeback: Tier-1 acceptance 字段 + audit_trail.pre_merge 填充
- [ ] 6.26 Forgejo housekeeping: M5 kickoff issue close + PR description amend (如有 audit trajectory 需校正)

### T-deploy 验收 (Tier-2 累积型, 不阻塞 Phase D.2)

- [ ] 6.27 累积 ≥3 real dispatches 含 ≥1 changes + ≥1 redo + ≥1 reject (随 owner 日常 workload 自然累积)
- [ ] 6.28 累积 ≥1 real failure 触发 Failure analysis LLM (owner 验证建议合理)
- [ ] 6.29 累积 ≥1 real spec drift detected (owner 验证 drift 真实)
- [ ] 6.30 m5-handoff.yaml writeback Tier-2 字段 + Phase D.2 final go_decision

---

## 排序依赖 (Phase A.2 task-planner 详细排序参考)

```
Phase 1 — Schema + Foundation
  ├── 1.1-1.9  schema migration + db.py helpers   ─┐
  ├── 1.10-1.13 audit log instrumentation          ├─ 串行 (1.1-1.9 必先, 1.10+ 依赖 db.py helpers)
  └── 1.14-1.15 risk-stub validate                 ─┘

Phase 2 — G + B (Phase 1 完成后并行)
  ├── 2.1-2.5  T-cron-direct (G)                  ─┐
  └── 2.6-2.16 T-failure-analysis (B)              ├─ 可并行 (G 改 comment_poll.py, B 改 reconciler.py)
                                                   ─┘

Phase 3 — D Review loop (Phase 1 完成后, Phase 2 可并行)
  ├── 3.1-3.4   schema 部分 (Phase 1 已含, 验证)
  ├── 3.5-3.11  comment-poll 协议扩展 ─┐
  ├── 3.12-3.19 changes mode           ├─ 内部串行 (协议先, 模式实现后)
  ├── 3.20-3.26 redo mode              ─┘
  └── 3.27-3.29 integration tests

Phase 4 — A Replay (依赖 Phase 1 audit log + Phase 2/3 events)
  └── 4.1-4.9  replay.py 实现 (audit log 是 source-of-truth, 必须 Phase 1+2+3 写入完整后)

Phase 5 — C Drift defense (依赖 Phase 1 audit log)
  ├── 5.1-5.5  Commit lint
  └── 5.6-5.15 Spec diff (依赖 Phase 3 D 完成, dispatch 有 PR 后才能 diff)

Phase 6 — Acceptance + Docs + Deploy
  ├── 6.1-6.4  Tier-1 acceptance
  ├── 6.5-6.12 T-docs
  ├── 6.13-6.16 T-prd-reframe
  └── 6.17-6.30 T-deploy + Tier-2 累积
```

---

## Sub-task granularity check (per Aria 规范)

每个 task ≤ 8h, 完整列表 (60+ tasks) 平均 1.5-3h/task。
最大单 task: 3.16 (重新进入 S6_REVIEW + LLM review 接入) ~6h, 仍在 ≤8h 范围内。

---

## Status

**Draft (Phase A.1)** — Ready for Phase A.2 post_spec audit (4-agent: backend-architect + tech-lead + qa-engineer + ai-engineer)。

**Approved 锁定后** → Phase A.3 准入 → Phase B.1 分支 → Phase B.2 实施。
