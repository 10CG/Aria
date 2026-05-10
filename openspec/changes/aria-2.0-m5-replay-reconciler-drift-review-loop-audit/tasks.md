# M5 Tasks — Aria 2.0 Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable

> **Spec**: [aria-2.0-m5-replay-reconciler-drift-review-loop-audit](./proposal.md)
> **Level**: 3 (Full)
> **Status**: Draft (Phase A.1, ready for Phase A.2 post_spec audit)
> **Brainstorm Source**: [.aria/decisions/2026-05-10-us025-m5-brainstorm.md](../../../.aria/decisions/2026-05-10-us025-m5-brainstorm.md)
> **Estimated total**: 113-118h vs 120h baseline

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
| T-acceptance | Tier-1 synthetic 验收 (各 Group 单元 + 集成测试) | ~5h | Phase 6 |
| T-docs | m5-handoff.yaml + AD-M5-1..M5-N backfill + README | ~3h | Phase 6 |
| T-prd-reframe | PRD 同步 (US-025 done + AD-M5 references) | ~2h | Phase 6 |
| T-deploy | Production deploy on Aether light-1 (owner-runnable) | (owner) | Phase 6 |

---

## Phase 1 — Schema + Foundation (~25h)

- [ ] 1.1 起草 schema migration script 004_schema_v4_additive.sql (additive only: ADD COLUMN risk_tier / rework_of / rework_round / rework_mode + CREATE TABLE dispatch_audit_log + 2 immutable triggers)
- [ ] 1.2 schema_migrate.py::apply_migrations 支持 003 → 004 升级路径 + 单元测试 (per `feedback_schema_migration_3_safeguard_pattern`)
- [ ] 1.3 db.py 新增 helper `append_audit_event(dispatch_id, event_type, payload)` (immutable INSERT, raises on UPDATE/DELETE attempt)
- [ ] 1.4 db.py 新增 helper `query_audit_log(dispatch_id?, event_type?, since?, until?)` (time-ordered audit events)
- [ ] 1.5 db.py 新增 helper `get_risk_tier(dispatch_id)` (prefer risk_tier WHERE NOT NULL else fallback risk_tier_stub) — abi_compat #1 hot-swap 接口
- [ ] 1.6 db.py 修改写入路径: 所有 dispatch INSERT 同时写 risk_tier=NULL + risk_tier_stub='always' (M5 行为不变, 抢占 abi_compat #1 dual-write)
- [ ] 1.7 单元测试: schema_migrate v3→v4 整体迁移 (in-memory DB + integrity_check + row count assert)
- [ ] 1.8 单元测试: dispatch_audit_log immutable triggers (UPDATE/DELETE 都 RAISE)
- [ ] 1.9 单元测试: append_audit_event 8 event types 各写一条 + query_audit_log 排序 + filter

## Phase 1 audit instrumentation (~10h, 与 Phase 1 串行)

- [ ] 1.10 现有代码 instrumentation: 每个 state transition 调用点 加 append_audit_event(event_type='state_transition', payload={from, to, reason})
- [ ] 1.11 现有代码 instrumentation: 每个 LLM call 调用点 加 append_audit_event(event_type='llm_call', payload={model, tokens_in, tokens_out, cost, duration_ms})
- [ ] 1.12 现有代码 instrumentation: human_decision update 调用点 加 append_audit_event(event_type='human_decision', payload={decision, comment_id, decision_at})
- [ ] 1.13 单元测试: instrumentation 不破坏 M4 单元测试 (537 个原有测试全 PASS, 不 regression)

## Phase 1 risk-stub 收尾 (~3h)

- [ ] 1.14 validate-m5-handoff.py 加 check_risk_tier_migration_acknowledged (检查 schema 含 risk_tier + risk_tier_stub 双列, M5 写入路径未启用真值)
- [ ] 1.15 文档: `aria-orchestrator/docs/architecture-decisions.md` 加 AD-M5-8 slot (risk_tier dual-write 接口边界)

---

## Phase 2 — G + B (~21h)

### T-cron-direct (G, 6h)

- [ ] 2.1 comment_poll.py::process_dispatch 在 update_human_decision 成功后 (CAS PASS) 直接 import 调用 extension._handle_s7_human_gate(dispatch_id)
- [ ] 2.2 兜底逻辑: comment-poll 进程崩溃时, reconciler 30min 仍能扫到 stuck S7 with human_decision 已写入 → 推进 transition
- [ ] 2.3 单元测试: comment-poll direct transition 端到端 (mock approve → assert state=S8_MERGE within 1 tick cycle)
- [ ] 2.4 单元测试: comment-poll 进程崩溃 + reconciler 兜底 (mock comment-poll 中断 → reconciler 下一 tick 推进)
- [ ] 2.5 文档: `aria-orchestrator/docs/architecture-decisions.md` 加 AD-M5-1 slot (comment-poll direct transition reframe, supersedes AD-M4-9 § 决策 #4)

### T-failure-analysis (B, 15h)

- [ ] 2.6 设计 Failure analysis LLM prompt template (input: fail_reason + last 5 audit events; output JSON {action, confidence, reason, suggested_owner_action})
- [ ] 2.7 prompt template 版本管理 (放 `aria-orchestrator/aria-layer1/prompts/failure_analysis.md`, 加版本号 + audit log 记录使用版本)
- [ ] 2.8 reconciler.py::_handle_failure_analysis 新方法: 当 dispatch 进入 S_FAIL 时调用 LLM analysis
- [ ] 2.9 retry 路径: action='retry' + confidence > 0.7 + retry_count < 1 + fail_reason in {'infrastructure', 'timeout'} → 创建新 dispatch (复用 D 项 rework 机制 但 mode='retry')
- [ ] 2.10 abort 路径: action='abort' → 写明确 fail_reason + final
- [ ] 2.11 notify_owner 路径: action='notify_owner' → Feishu reject 卡片含 LLM 诊断 + suggested_owner_action
- [ ] 2.12 ProviderRouter 接入: failure_analysis 用 glm-4.5-air, fallback glm-5-turbo
- [ ] 2.13 audit log 写入: event_type='failure_analysis', payload=LLM 完整输出 + 是否触发 retry
- [ ] 2.14 单元测试: 3 路径 (retry / abort / notify_owner) × mock LLM
- [ ] 2.15 集成测试: 真 fail dispatch + mock LLM → 验证完整 audit log 链路
- [ ] 2.16 文档: AD-M5-6 slot (Failure analysis LLM prompt 设计 + 版本管理)

---

## Phase 3 — D Review loop (~50-55h, 最大 workpackage)

### T-rework-loop schema (~5h)

- [ ] 3.1 schema migration 包含 rework_of / rework_round / rework_mode columns (Phase 1 已含, 此处验证)
- [ ] 3.2 db.py 加 helper `create_rework_dispatch(parent_id, mode, feedback)` (创建新 row 含 rework_of=parent_id + rework_round+=1 + rework_mode + 复用原 issue_id)
- [ ] 3.3 db.py 加 helper `count_rework_chain(dispatch_id)` (递归 query rework_of 链, 返回总轮次)
- [ ] 3.4 单元测试: rework chain 创建 + cap=3 enforcement (round 4 创建拒绝 + 当前 row → S_FAIL(rework_exceeded))

### T-rework-loop comment-poll protocol (~10h)

- [ ] 3.5 comment_poll.py::parse_magic_string 扩展 4 commands (approve / reject / changes / redo)
- [ ] 3.6 process_dispatch 路由: changes → create_rework_dispatch(mode='changes') + 当前 row S_FAIL(changes_requested)
- [ ] 3.7 process_dispatch 路由: redo → create_rework_dispatch(mode='redo') + 当前 row S_FAIL(changes_requested) + 旧 PR auto-close + comment "Superseded by #<new>"
- [ ] 3.8 cap enforcement: 创建前检查 count_rework_chain(parent_id) >= 3 → 拒绝并 S_FAIL(rework_exceeded)
- [ ] 3.9 nomadVar `ARIA_REWORK_MAX_ROUND` 接入 (default=3, override 可调)
- [ ] 3.10 audit log 写入: event_type='rework_cycle', payload={rework_of, rework_round, rework_mode, feedback}
- [ ] 3.11 单元测试: 4 commands 各路径 + cap 边界 (round=2 创建 OK, round=3 创建 OK, round=4 拒绝)

### T-rework-loop changes mode (Layer 2 二次进入) (~20h)

- [ ] 3.12 设计 changes 模式 Layer 2 entrypoint (新 mode='rework-changes' 分支, prompt = 原代码 diff + feedback)
- [ ] 3.13 Layer 2 容器启动逻辑: rework-changes mode 时, fetch 原 PR branch + 接收 feedback prompt + AI 改稿
- [ ] 3.14 git push 策略: force-push 同 branch (per AD-M5-4 锁定方向; 备选: append-commit 留 audit 历史)
- [ ] 3.15 PR diff 演进: force-push 后 PR diff 自动更新, owner 看到 v1 → v2 演进
- [ ] 3.16 重新进入 S6_REVIEW: changes 模式新 row 进入 S6 直接跑 LLM review (不重决策 S2_DECIDE / S3_BUILD_CMD), 节省 ~50% LLM cost
- [ ] 3.17 Feishu 卡片: round 显示 "rework round 2/3 — changes mode" + 原 PR 链接 + new PR diff 链接
- [ ] 3.18 集成测试: changes 模式完整 cycle (mock /aria changes → 新 row → Layer 2 容器 → PR diff 更新 → S6→S7→approve)
- [ ] 3.19 文档: AD-M5-3 slot (Layer 2 二次进入 mechanism) + AD-M5-4 slot (force-push vs append-commit)

### T-rework-loop redo mode (新 dispatch 全周期) (~12h)

- [ ] 3.20 redo 模式 Layer 2 entrypoint (mode='rework-redo', prompt = 原 issue + feedback, 不含原代码)
- [ ] 3.21 Layer 2 容器启动: redo mode 时走完整 S0 → S2 → S3 → S4 → S5 → S6 → S7 (新 PR 创建)
- [ ] 3.22 旧 PR auto-close + 添加 comment "Superseded by #<new> (redo mode)"
- [ ] 3.23 新 PR 描述自动包含原 issue + redo feedback + rework chain 完整链 (原 PR + new PR 双向链接)
- [ ] 3.24 LLM cost 计入 audit log (full 100% cost vs changes 50% cost, replay 时可见对比)
- [ ] 3.25 Feishu 卡片: round 显示 "rework round 2/3 — redo mode" + new PR 链接
- [ ] 3.26 集成测试: redo 模式完整 cycle (mock /aria redo → 新 row → 全 state machine → 新 PR → S7→approve)

### T-rework-loop integration (~5h)

- [ ] 3.27 mixed mode 测试: changes round 1 + redo round 2 + approve round 3 (验证 cap 合并计数 + 不区分模式)
- [ ] 3.28 abi_compat #4 兼容性测试: 同一 row 多次写 human_decision 应被 CAS 拒绝 (first-decision-wins)
- [ ] 3.29 文档: AD-M5-2 slot (rework_round 存储设计: 新 dispatch row vs 同 row counter)

---

## Phase 4 — A Replay (~10h)

- [ ] 4.1 设计 replay output format (markdown / JSON / both)
- [ ] 4.2 aria_layer1/replay.py::replay(dispatch_id) 主入口 (返回 markdown 字符串)
- [ ] 4.3 query audit log + dispatches 主表 join (用 db.py::query_audit_log)
- [ ] 4.4 时间序输出: state 转换 + LLM 调用 + human decisions + rework cycles + failure analysis + drift detection 全部按 ts 排序
- [ ] 4.5 rework chain 输出: 递归展开 rework_of 链 (round 1 → round 2 → round 3)
- [ ] 4.6 markdown 渲染: 表格 + 链接 + 代码块 + Forgejo PR 链接
- [ ] 4.7 文件输出: 默认 stdout, `--output-file` 选项写入 `.aria/replay-reports/{dispatch_id}.md`
- [ ] 4.8 单元测试: replay 各种场景 (无 rework / 1 round changes / 2 round mixed / 含 failure analysis)
- [ ] 4.9 集成测试: replay 真实历史 dispatch (从 M4 production 导出 1 条 + replay output)

---

## Phase 5 — C Drift defense (~12h)

### T-drift commit lint (~5h)

- [ ] 5.1 设计 commit lint 规则 (Conventional Commits + Aria scope conventions)
- [ ] 5.2 aria_layer1/commit_validator.py::validate_commit_message 实现 regex 验证
- [ ] 5.3 Layer 2 hook: AI 写 commit 前调用 validate_commit_message, 不通过则 force AI 重写 (prompt 加 violation feedback)
- [ ] 5.4 audit log 写入: event_type='commit_lint_result', payload={passed, violations, raw_message}
- [ ] 5.5 单元测试: 12+ fixtures 覆盖 (passing + various failure modes)

### T-drift spec diff (~7h)

- [ ] 5.6 设计 Spec diff LLM prompt template (input: proposal.md + PR diff; output: {compliance_score, deviations, extra_changes})
- [ ] 5.7 prompt template 版本管理 (`aria-orchestrator/aria-layer1/prompts/spec_drift.md`)
- [ ] 5.8 dispatcher.py::_check_spec_drift 新方法: dispatch S8_MERGE 后 (或 S_FAIL 后) 调用 LLM 比较
- [ ] 5.9 ProviderRouter 接入: spec_drift 用 glm-4.5-air
- [ ] 5.10 阈值判断: score < 70 → 触发 Feishu drift 警告卡片 (build_drift_alert_card)
- [ ] 5.11 nomadVar `ARIA_SPEC_DRIFT_THRESHOLD=70` 接入
- [ ] 5.12 audit log 写入: event_type='spec_drift_detected', payload={score, deviations, extra_changes}
- [ ] 5.13 单元测试: 多 score 阈值 + Feishu 卡片 mock + audit log
- [ ] 5.14 集成测试: 真 PR + 真 proposal.md → mock LLM → 完整 drift detection 链路
- [ ] 5.15 文档: AD-M5-5 slot (spec_drift 阈值 + nomadVar 调机制)

---

## Phase 6 — Acceptance + Docs + Deploy

### T-acceptance (~5h)

- [ ] 6.1 Tier-1 集成测试套件 (12 个 acceptance criteria 全覆盖)
- [ ] 6.2 单元测试 + 集成测试合计 ≥ 600 PASS (vs M4 final 537)
- [ ] 6.3 abi_compat_promises 验证: 4 promises 全部 enforced (validate-m5-handoff.py 4 个 check 函数 PASS)
- [ ] 6.4 性能测试: comment-poll direct transition p99 latency < 60s (synthetic, M4 实测 baseline 17min)

### T-docs (~3h)

- [ ] 6.5 m5-handoff.yaml schema (additive on m4-handoff schema v1.0) — 含 m5_acceptance / m5_human_gate_metrics / abi_compat_promises (M5→M6) / ad_m5_status / effort / signoffs / open_issues_for_m6 / audit_trail / m4_handoff_cross_reference
- [ ] 6.6 validate-m5-handoff.py + 单元测试 (类比 M4 validate-m4-handoff.py)
- [ ] 6.7 AD-M5-1..M5-N 全部 backfill (Phase B 实施期填充, Phase 6 verify 全 Decided)
- [ ] 6.8 README.md 同步: aria-layer1 plugin.yaml version 0.3.0 → 0.4.0 + M5 features 章节
- [ ] 6.9 architecture-decisions.md AD-M5-1..M5-11 全部填充 (slot → Decided)
- [ ] 6.10 文档: AD-M5-7 slot (Audit log retention 策略, M5 不做 archival 推 M6)
- [ ] 6.11 文档: AD-M5-9 slot (comment-poll 进程崩溃后的 reconciler 兜底契约)
- [ ] 6.12 文档: AD-M5-10 slot (新增 abi_compat_promises forward-binding M5→M6)

### T-prd-reframe (~2h)

- [ ] 6.13 PRD §M5 锁 actual scope (M5 actual_scope_locked: 5 PRD + F + G; H 推 M6)
- [ ] 6.14 PRD §User Stories 表 US-025 → done
- [ ] 6.15 PRD §M6 加 H aria-layer2-runner deploy + F.algorithm + A.advanced + C.advanced + B.advanced (deferred items)
- [ ] 6.16 prd-aria-v2.md 版本 bump (v2.1.0 → v2.2.0, M5 done milestone)

### T-deploy (Phase 6, owner-runnable, post-merge)

- [ ] 6.17 Pre-deploy: SSH light-1 + git pull + git checkout master + pip install -e refresh (per `feedback_handoff_doc_assumes_venv_ready_smell`)
- [ ] 6.18 Schema migration: 3-safeguard pattern (atomic backup + dry-run on copy + apply on prod with integrity_check + row count assert)
- [ ] 6.19 nomadVar 配置: `ARIA_REWORK_MAX_ROUND=3` + `ARIA_SPEC_DRIFT_THRESHOLD=70` + 其他新增 secrets (TBD)
- [ ] 6.20 nomad job validate + aether dev run (aria-layer1-comment-poll + aria-layer1-reconcile redeploy with M5 code)
- [ ] 6.21 Verify alloc + clean ticks (1 cron cycle + 1 comment-poll cycle + 1 reconcile cycle 都跑过, audit log 写入正常)
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
