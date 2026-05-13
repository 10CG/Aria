---
checkpoint: post_spec
mode: convergence
round: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: SCOPE_OK_R2
timestamp: 2026-05-12T23:51Z
context: openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/
agents: [aria:backend-architect, aria:tech-lead, aria:qa-engineer, aria:ai-engineer]
r1_findings_total: 65
r2_findings_closed: 60
r2_findings_partial: 3
r2_findings_open: 2  # AI-13 docs-only / BA-11 model key validation
r2_new_findings: 14  # 0 critical + 1 important (QA-R2-2) + 13 minor/obs
r1_critical_closed: 11/11  # 100%
r1_important_closed: ~31/34  # 91%
reduction_rate: 92.3%
---

# M5 Spec post_spec audit R2 — 2026-05-12T23:51Z

> **R2 verdict**: SCOPE_OK_R2 4/4 (PASS_WITH_WARNINGS / APPROVE / LGTM_WITH_NOTES / MERGE_NOW)
> **Reduction**: 92.3% (R1 65 → R2 effective ~5 unresolved important+minor)
> **Compare M4 precedent**: M4 R2 was 70-76% reduction → 本 R2 92.3% 是更强收敛

---

## Vote distribution

| Agent | R1 Vote | R2 Vote | R1 Findings | R2 New | Closure |
|-------|---------|---------|-------------|--------|---------|
| aria:backend-architect | PASS_WITH_WARNINGS | **PASS_WITH_WARNINGS** | 18 (3C+9I+4m+2o) | 4 (1I+3m+o) | 91.7% |
| aria:tech-lead | NEEDS_FIX | **APPROVE** | 14 (2C+6I+4m+2o) | 4 minor | 11/12 closed |
| aria:qa-engineer | NEEDS_FIX | **LGTM_WITH_NOTES** | 20 (4C+11I+4m+1o) | 3 (1I+2m) | 14/20 closed |
| aria:ai-engineer | NEEDS_FIX | **MERGE_NOW** | 13 (2C+8I+2m+1o) | 3 minor | 92.3% |
| **Total** | NEEDS_FIX | **SCOPE_OK_R2** | 65 | 14 | **92.3%** |

---

## R1 Critical 11/11 全部 CLOSED ✅

| R1 ID | Theme | R2 Status | Evidence |
|-------|-------|-----------|----------|
| BA-1 | rework_of FK rowid → dispatch_id | ✅ Closed | proposal §SQL line 179 changed; AD-M5-2 doc lock |
| BA-2 | rework_round semantics + cap meaning | ✅ Closed | proposal §rework_round semantics lock lines 214-219; round=4 reject 边界 unambiguous |
| BA-3 | comment-poll partial failure recovery | ✅ Closed | tasks 2.2 + AD-M5-9 explicit; 2.4 unit test |
| TL-1 | Effort 算术 113-118 vs 128-138 | ✅ Closed | proposal §136 Total 133h table; baseline 130h; OD trigger 156h |
| TL-2 | Risk-tier dual-write 写 NULL 违反 abi_compat #1 | ✅ Closed | task 1.6 writes 'always' literal; AD-M5-8 lock |
| QA-1 | T-acceptance 5h under-resourced | ✅ Closed | task 6.1-6.1.15 expanded to 16 subtasks, ~10-12h budget |
| QA-2 | retry_count column 缺失 | ✅ Closed | proposal §SQL ADD COLUMN retry_count |
| QA-3 | 537 tests + instrumentation 注入策略 | ✅ Closed | task 1.10 AuditLogger middleware + NullAuditLogger shim |
| QA-4 | 3-safeguard 仅 reference 未 inline | ✅ Closed | task 6.18.1-6.18.5 fully inlined |
| AI-1 | Tier-1 全 mock_llm 重蹈 M4 HMAC paper-fix | ✅ Closed | proposal Tier-1 + B.1.live + C.2.live + HMAC.1 gates; tasks 2.15.6 + 5.14.5 + 6.1.2 + 6.1.5 + 6.1.15 |
| AI-2 | LLM JSON parse fallback 缺失 | ✅ Closed | task 2.6.5 + 5.12.5 fallback chain (parse → regex → safe default) |

---

## R1 Important 91% closed (31/34)

**全 closed themes** (各 agent 一致):
- abi_compat 4 promises enforcement complete (TL-3): tasks 6.6.1-6.6.4 + 6.6.5 mechanical assert
- T-deploy Track A 7 discoveries 全覆盖 (TL-8): HMAC oracle + cron pre-validate + layer2 stub
- Schema 设计 (BA-4/5/6 BA-13 QA-2): event_type CHECK + rework_mode NULL + rework_feedback 分离 + FK
- B 项 retry/abort/notify_owner (BA-7 QA-8 AI-8): retry_count separate + JSON parse fallback + ladder terminal lock
- D 项 changes/redo (BA-8 BA-9 QA-9 AI-6): state machine entry + PR close timing + Forgejo failure + prompt length cap
- 测试覆盖 (QA-5/6/7/11/15): commit lint 12 fixtures + audit completeness + mixed mode card + cross-milestone graceful degrade + drift trigger
- Replay completeness (AI-4/9/11): llm_call payload prompt+response + rework_cycle payload + ProviderRouter middleware
- Calibration spikes (AI-3/5/7): cost spike + confidence calibration + false-positive validation
- Process / governance (TL-4/6/7/9/10/11): Phase 5 deps + risk_tier_classified instrumentation + Tier-2 H.dep.note + AD-M5 1..11 explicit + Framing column + Phase 3 mid-checkpoint

**Partial / Open**:
- BA-11 (ProviderRouter model key validation): partial — ladder terminal addressed via AI-8, but explicit input key boundary validation still untasked
- TL-5 (OD trigger cushion): partial — raised 144h→156h but pessimistic also moved to 155h, cushion only 1h (direction reversed)
- AI-13 (B.advanced trigger condition): partial — documentation-only, not M5 active feature

---

## R2 New findings (14)

### Important (1)
- **QA-R2-2** prompt redaction 与 4KB truncation 执行顺序未定义 (security-sensitive, but blocks_phase_a3=false per qa-engineer)
  - 建议 fix: redaction MUST apply BEFORE 4KB truncation

### Minor (10)
- BA-R2-1 FK / immutable triggers 在 dispatch delete 场景未定义 (推 AD-M5-7 retention)
- BA-R2-2 create_rework_dispatch retry mode rework_round=0 helper signature inconsistency
- BA-R2-3 count_rework_chain 应 filter rework_mode!='retry'
- BA-R2-4 comment-poll protocol table 还提 reject_reason=feedback 应改 rework_feedback (doc inconsistency)
- TL-R2-1 Phase 6 subtask sum ~18.5h exceeds Phase 6 table 13h (range 12-15h) — 重算
- TL-R2-2 OD-M5-1 trigger 156h vs PERT pessimistic 155h cushion only 1h
- TL-R2-3 Duplicate AD-M5-2 task 3.3 + 3.29 verbatim content
- TL-R2-4 Baseline 130h vs Phase total 133h doc inconsistency
- QA-R2-1 tasks.md 总览表 T-acceptance 显示 ~5h 应改 ~10-12h
- QA-R2-3 calibration spike 用 M4 historical S_FAIL 实际无 audit context (是 synthetic, 不是真 replay)
- AI-R2-1 prompt redaction pattern enumeration 不完整 (含 OAuth/JWT/SSH key)
- AI-R2-2 B.1.live + C.2.live cost 估算缺
- AI-R2-3 'prompt 摘要' 算法未定义 (建议 first 500 chars + metadata)

### Observation (3)
- 与 minor 部分重叠

---

## SCOPE_OK_R2 verdict rationale

per `feedback_audit_convergence_pattern` + `feedback_pre_merge_4round_convergence_template`:
- ✅ R1 critical 100% closed (11/11)
- ✅ R1 important ≥80% closed (~91%)
- ✅ 0 R2 new critical
- ✅ 4 agents 全无 NEEDS_FIX (PASS/APPROVE/LGTM/MERGE_NOW)
- ✅ Reduction 92.3% > 70% threshold
- ⚠️ 1 R2 new important (QA-R2-2 security-sensitive) — blocks_phase_a3=false 但应解决

---

## Convergence path forward

### 推荐 Path A (R2 lock + Phase A.3 entry)

R2 fixes 应用 14 minor/observation 文档级 polish (~30min), 然后:
- Phase A.3 准入 sign-off
- Phase B.1 分支
- Phase B.2 实施

理由:
- M4 precedent: R2 SCOPE_OK_R2 4/4 后 OD-15 collapse R3+R4 (但 owner 后续要求真跑 R5)
- M5 R2 比 M4 R2 收敛更强 (92.3% vs 70-76%)
- 14 个 R2 finding 全 minor + documentation polish, 不阻塞 Phase B 起步

### 备选 Path B (owner-invoked R3 stability)

per `feedback_owner_invoked_convergence_loop`: 不轻信 OD-15 collapse, 真跑 R3 验证 stability (R3 == R2 才算真收敛)。
- R3 期望 ~5 findings (R2 polish 后), 全 PASS 4/4
- 多 ~10min 4 agents 并行重审

owner 决策点。

---

## Cross-references

- R1 report: `.aria/audit-reports/post_spec-R1-2026-05-10T1506Z-aria-2.0-m5.md`
- M4 R2 precedent: `.aria/audit-reports/post_spec-R2-2026-05-07T1845Z-us024-m4.md`
- Memory: `feedback_audit_convergence_pattern` (R_N == R_{N-1} 严格收敛)
- Memory: `feedback_owner_invoked_convergence_loop` (R3+ 真跑 vs OD-15 collapse)
- Memory: `feedback_paper_fix_antipattern` (Tier-1 live LLM AI-1 已 close)
