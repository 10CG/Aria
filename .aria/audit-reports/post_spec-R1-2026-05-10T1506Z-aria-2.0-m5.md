---
checkpoint: post_spec
mode: convergence
round: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: NEEDS_FIX
timestamp: 2026-05-10T15:06Z
context: openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/
agents: [aria:backend-architect, aria:tech-lead, aria:qa-engineer, aria:ai-engineer]
findings_count_total: 65
findings_critical: 11
findings_important: 34
findings_minor: 14
findings_observation: 6
---

# M5 Spec post_spec audit R1 — 2026-05-10T15:06Z

> **Spec**: aria-2.0-m5-replay-reconciler-drift-review-loop-audit (Phase A.1 draft)
> **R1 verdict**: NEEDS_FIX (3 agents NEEDS_FIX + 1 PASS_WITH_WARNINGS)
> **Recommendation**: 进 R2 fix-verify, 期望 70%+ reduction (per `feedback_audit_convergence_pattern`)

---

## Vote distribution

| Agent | Vote | Findings | Critical | Important | Minor | Obs |
|-------|------|----------|----------|-----------|-------|-----|
| aria:backend-architect | PASS_WITH_WARNINGS | 18 | 3 | 9 | 4 | 2 |
| aria:tech-lead | **NEEDS_FIX** | 14 | 2 | 6 | 4 | 2 |
| aria:qa-engineer | **NEEDS_FIX** | 20 | 4 | 11 | 4 | 1 |
| aria:ai-engineer | **NEEDS_FIX** | 13 | 2 | 8 | 2 | 1 |
| **Total** | **NEEDS_FIX** | **65** | **11** | **34** | **14** | **6** |

---

## Critical findings (11) — must close in R2

### BA (backend-architect, 3)

- **BA-1**: `rework_of INTEGER REFERENCES dispatches(rowid)` 与应用层 dispatch_id TEXT 不匹配; rowid 不稳定 (VACUUM 后变), 应改为 `REFERENCES dispatches(dispatch_id)` 或 `REFERENCES dispatches(id)` (取决于 PK 设计)
- **BA-2**: rework_round 语义边界模糊 (rework_round=0 是 parent vs child round 1?); cap=3 实际允许 3 次 rework (= 4 dispatches) 还是 3 dispatches 总?
- **BA-3**: comment-poll direct transition (G) 部分失败路径未定义 — human_decision 已 commit 但 _handle_s7_human_gate raise 时, dispatch stuck S7 with decision; reconciler 必须 explicit 处理 `state=S7 AND human_decision IS NOT NULL → re-attempt`

### TL (tech-lead, 2)

- **TL-1**: 工时算术不一致 — Phase 1 (~25h tasks vs ~30h proposal), 6 Phase 总和 128-138h vs 声称 113-118h; OD-M5-1 trigger 144h 与 PERT pessimistic 140h 仅 4h cushion
- **TL-2**: Risk-tier dual-write 写 NULL 违反 abi_compat #1 promise wording ("M5 caller 同时写 risk_tier + risk_tier_stub"); NULL 不是 written value; 必须或 (a) reframe promise 含 M5 NULL ok / (b) 写 stub literal 'always'

### QA (qa-engineer, 4)

- **QA-1**: T-acceptance 5h / 4 tasks 严重 under-resourced (M4 同 scope 是 8 个 explicit subtasks ~7-10h); 12 Tier-1 criteria 没有 1:1 mapping
- **QA-2**: retry_count 字段从 schema migration 完全缺失, 但 B 项 retry guard 依赖 `retry_count < 1`
- **QA-3**: 537 existing tests + audit log instrumentation 注入策略未定义; 高风险 mass test breakage in Phase 1
- **QA-4**: 3-safeguard pattern 仅 reference, 未 inline 到 task 1.2/6.18; 实施时容易遗漏 atomic backup 步骤

### AI (ai-engineer, 2)

- **AI-1**: Tier-1 全部 mock_llm — 重蹈 M4 Feishu HMAC paper-fix antipattern (R5 4/4 CONVERGED 仍漏); B + C 真实 ProviderRouter chain 在 deploy 前从未验证
- **AI-2**: LLM JSON parse fallback 缺失; glm-4.5-air ~5-15% 输出含 markdown fence / extra text → reconciler crash 风险

---

## Important findings (34) — should close R2-R3

### Cross-agent overlap (deduplicated themes)

#### Theme 1: abi_compat enforcement 不完整 (TL-3, TL-2, AI-3)
- 4 promises 仅 2 个 (#1 #4) 显式 enforce, #2 #3 no validate-m5-handoff.py check function
- nomadVar `ARIA_FAIL_RETRY_CONFIDENCE_MIN` 缺失 (B 项), 与 spec drift threshold 不对称

#### Theme 2: T-deploy 覆盖 Track A 7 discoveries 不全 (TL-8)
- HCL cron 6-field validate-degrades 未 pre-check
- Feishu HMAC 回归测试 未在 Tier-1
- aria-layer2-runner 缺失对 Tier-2 的影响 (TL-7) 未明示

#### Theme 3: schema 设计 (BA-4 BA-5 BA-6 QA-2)
- dispatch_audit_log 缺 event_type CHECK constraint
- rework_mode NULL 处理 (parent rows) 未明示
- fail_reason 被 repurpose 装 feedback text, 与 enum 语义冲突 (应分离 rework_feedback 列)

#### Theme 4: B 项 retry/abort/notify_owner (BA-7 QA-8 AI-8)
- system retry 错误共享 rework cap (BA-7)
- confidence 0.7 boundary / null / malformed 输出未测 (QA-8)
- ProviderRouter ladder glm-4.5-air terminal, 实际不会 fallback glm-5-turbo (AI-8) ⚠️

#### Theme 5: D 项 changes/redo 流程 (BA-8 BA-9 QA-9 AI-6)
- changes 模式 state machine 入口未定义 (S4/S6 直接? Layer 2 触发时机?)
- redo PR 关闭时序问题 (新 PR# 还没生成时不能写 "Superseded by")
- Forgejo PR 关闭失败 fallback 缺失
- changes prompt 长度限制 + truncation 策略缺失 (大 diff 风险)

#### Theme 6: 测试覆盖 (QA-5 QA-6 QA-7 QA-11 QA-15)
- commit lint 12+ fixtures 未枚举 (M4 模式: 显式列出每个 fixture 的目的)
- changes 模式 audit log 完整性测试缺
- mixed-mode card content 测试缺
- replay 跨 milestone (M4 dispatch 无 audit log) 优雅降级缺
- spec drift 触发 trigger ambiguity (S8_MERGE only vs S_FAIL 也算)

#### Theme 7: Replay completeness (AI-4 AI-9 AI-11)
- llm_call payload 缺 input_prompt + output_text → replay '不重跑 LLM' 不能 reconstruct rationale
- rework_cycle payload 缺 feedback_text + parent_pr_url
- ProviderRouter instrumentation 装饰 vs caller 模糊 → 易漏写

#### Theme 8: calibration spike (AI-3 AI-5 AI-7)
- confidence 0.7 / drift threshold 70 magic numbers 无依据
- spec drift cost (PR diff size 大) 未实测
- spec drift input slicing (proposal What/Acceptance 章节抽取) 未设计 → false positive 风险

#### Theme 9: process / governance (TL-4 TL-5 TL-6 TL-9 TL-10 TL-11)
- Phase 5 sequential dependency on Phase 3 (D 完成才能 spec diff) 未 explicit
- OD-M5-1 trigger 144h 与 PERT pessimistic 140h 距离仅 4h
- risk_tier_classified event 未 instrumentation (Phase 1 漏)
- 'AD-M5-1..M5-N' 应改 'AD-M5-1..AD-M5-11' (mechanical assert)
- AD-M5-2/4 framing 是 open slot 但 SQL 已 lock (实为 documentation, 非 decision)
- Phase 3 (50-55h, 41% budget) 缺 intra-phase audit checkpoint

---

## Minor (14) + Observation (6)

详见各 agent JSON 输出 (这里省略,R3 stability/strict 阶段处理)。

主要 minor 主题:
- FOREIGN KEY on dispatch_audit_log.dispatch_id (BA-13)
- WITH RECURSIVE 深度限制 (BA-14)
- replay output format AD slot 缺 (BA-18)
- nomadVar `ARIA_REWORK_MAX_ROUND` 边界值验证 (cap=0 行为) (QA-17)
- replay filename sanitize (path traversal) (QA-18)
- mid-impl reforecast 协议 (QA-19)
- pre-M5 dispatch replay graceful degrade (AI-12 +)

---

## Direction-alignment summary

```
4 agents 一致认为:
  ✅ Brainstorm Q0-Q9 锁定决策与 proposal/tasks 内容大致一致
  ✅ 11 AD-M5 slots 设计合理
  ✅ Phase decomposition 整体合理
  ✅ abi_compat 4 promises 在 proposal 显式列出

4 agents 一致 flag 必修 (R2 critical):
  ❌ Effort 算术不自洽 (TL-1)
  ❌ Risk-tier dual-write 与 abi_compat #1 wording 冲突 (TL-2)
  ❌ retry_count schema 缺失 (QA-2)
  ❌ T-acceptance under-resourced 5h 太薄 (QA-1)
  ❌ Tier-1 全 mock_llm 重蹈 M4 paper-fix (AI-1)
  ❌ rework_of FK rowid 不稳定 (BA-1)
  ❌ comment-poll partial failure 未守 (BA-3)
  ❌ JSON parse fallback 缺 (AI-2)
  ❌ ProviderRouter ladder glm-4.5-air terminal,fallback 不会触发 (AI-8)
  ❌ instrumentation 注入策略未定 (QA-3)
  ❌ rework_round 语义边界 (BA-2)
```

---

## Next round expectation (R2)

per `feedback_audit_convergence_pattern`:
- R1 → R2: 70-76% finding reduction (M4 实证)
- R2 verdict 期望: SCOPE_OK_R2 4/4 (所有 critical 闭合 + ≥80% important 闭合)
- R3+ stability check (per `feedback_owner_invoked_convergence_loop` 不 OD-15 collapse)

R2 fix list (R1 critical + theme-level important):
1. Fix effort arithmetic + reconcile baseline (TL-1)
2. Reframe risk-tier dual-write vs abi_compat #1 (TL-2 ↔ AD-M5-8 explicit)
3. Add retry_count schema column + helper (QA-2)
4. Expand T-acceptance to 12 explicit subtasks (QA-1)
5. Add Tier-1 live LLM acceptance (AI-1) + JSON parse fallback (AI-2)
6. Fix rework_of FK semantics (BA-1)
7. Add comment-poll partial failure recovery (BA-3) + AD-M5-9 explicit
8. Resolve ProviderRouter ladder issue (AI-8) — extend ladder OR new STATE entry
9. Define instrumentation injection strategy (QA-3)
10. Lock rework_round semantics + cap boundary (BA-2 + AD-M5-2)
11. Inline 3-safeguard pattern (QA-4)
12. Add HMAC regression + cron syntax pre-validate (TL-8)

---

## Cross-references

- agents 完整 JSON output: 详见本 R1 audit log 上下文
- M4 audit pattern reference: `.aria/audit-reports/post_spec-R1-2026-05-07T1811Z-us024-m4.md` (R1 43 → R2 SCOPE_OK_R2)
- Memory: `feedback_audit_convergence_pattern` (R_N == R_{N-1} 严格收敛)
- Memory: `feedback_owner_invoked_convergence_loop` (R3+ 真跑不 OD-15 collapse)
- Memory: `feedback_paper_fix_antipattern` (Tier-1 live LLM AI-1)
