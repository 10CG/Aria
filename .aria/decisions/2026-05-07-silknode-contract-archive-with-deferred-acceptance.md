---
type: deferred_acceptance_waiver
spec_id: aria-2.0-silknode-integration-contract
expires_at: 2026-08-05T23:59:59Z
sign_off_mechanism: pr_approval
approved_by: solo-lab (uni.concept.wzfq@gmail.com) via archive commit
status: deferred
audit_loop_rounds: 3
audit_loop_outcome: converged
---

# Owner Decision — silknode-integration-contract Archived with Explicit Waiver

> **Date**: 2026-05-07
> **Decider**: solo-lab (uni.concept.wzfq@gmail.com)
> **Type**: Governance disposition (Spec lifecycle closure with deferred acceptance)
> **Trigger**: 3-round multi-agent Spec discussion loop converged 2026-05-07 (4 agents: legal-advisor + tech-lead [discussion] / backend-architect + qa-engineer [challenge])
> **Status**: Active deferral until 2026-08-05 (90-day hard cap matching `2026-05-02-secret-rotation-deferred.md` precedent)

---

## 决策

将 `openspec/changes/aria-2.0-silknode-integration-contract/` (Draft 2026-04-14) 归档为 `openspec/archive/2026-05-07-aria-2.0-silknode-integration-contract/`, Status 改 Draft → Complete (Archived-with-Waiver), **接受其 4 项 acceptance criteria 中 3+4 项为 deferred-acceptance 状态** (非 silent drop)。

**Contract 2 (业务数据分类约束) was never mechanically enforced in M2 development and carries explicit waiver until 2026-08-05.**

## Acceptance Criteria 逐项判定

| # | Acceptance | 判定 | 证据 |
|---|------------|------|------|
| (a) | US-022 起草时 proposal.md 含 §契约 1 原文 | ✅ **MET** | `openspec/archive/2026-05-03-aria-2.0-m2-layer1-state-machine/proposal.md` L223-230 verbatim 引用 §契约 1 (line 31-40 of source Spec); 10 grep hits 累计 (含 acceptance §E + tasks T8/T9/T10 inheritance) |
| (b) | US-023 起草时 fallback 路径含 §契约 1 | ✅ **MET (retroactively confirmed)** | `openspec/archive/2026-05-06-aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md` L132 OD-3d **generalize** 契约 1 至所有 LLM provider (含 ZhipuClient direct-connect); marker `(deprecated)` at L369 reflects superseded-by-generalization, NOT abandonment. R3 owner ack: see `.aria/decisions/2026-05-02-od-9-luxeno-reframe.md` retroactive ack section appended 2026-05-07 |
| (c) | US-025 起草时 tasks.md 含 `silknode_storage_check` + `business_data_classification_check` | 🟡 **DEFERRED with detection stub** | US-025 not yet kicked off. Minimum-viable detection stub added in same commit as this waiver: `.aria/state-checks.yaml::silknode-contract-deferral-expiry` (WARN-on-expiry-or-trigger-met). Full audit checks remain US-025 scope when started |
| (d) | PRD v2.0 / CLAUDE.md 修订时 §契约 2 原文写入 | 🟡 **WAIVED until 2026-08-05** | grep against `CLAUDE.md` + `docs/requirements/prd-aria-v2.md` returns 0 hits for "silknode" / "no-storage" / "business_data_classification". US-026 not yet scoped. **Contract 2 was never mechanically enforced in M2; explicit waiver applies until 2026-08-05 hard cap or US-026 kickoff (whichever first)** |

## 触发条件 (强制 — 任一命中即重新评估)

仿 `2026-05-02-secret-rotation-deferred.md` §触发条件 4 项 pattern:

1. **US-025 kickoff** (Phase A.1 起 Spec, 包含 audit-engine `silknode_storage_check` + `business_data_classification_check` 实施任务)
2. **M5 production launch milestone 评审** (Aria 2.0 production launch 决议时点)
3. **r1-legal-memo expires_at 到期** 或 **业务范围变化** (Aria 2.0 处理类别从"技术工单/代码/方法论"扩展至 PII/支付/医疗/重要数据等任一)
4. **2026-08-05 硬时限护栏** (90 天, dev 期不无限拖延; 即使 1/2/3 都未触发也强制重审)

## 决策理由

| 因素 | 说明 |
|------|------|
| Discussion loop convergence | 3-round 4-agent Spec discussion 最终 R3 CONSENSUS REACHED (challenge group 0 objections); direction ALIGNED 全 3 rounds |
| Memo v1.1 audit chain | 保持完整 (Memo → Spec waiver → Code US-022/023 → Audit detection stub) — 不 sever bidirectional binding |
| Aria 小步迭代原则 | US-025 / US-026 设计深度需独立 Spec; 本 waiver 不强制设计这些 Spec |
| 1-人 lab 资源 | per AD-M0-9, owner = decision authority = PR approver; pr_approval 即 sign-off mechanism |
| Detection stub feasibility | `.aria/state-checks.yaml` 探针 ~15 行 YAML, 当前 commit 落地, 防 scaffold-helpers-drift 反 pattern (`feedback_scaffold_helpers_drift_without_callers`) |
| 90-day vs 180-day | 选 90d 与 secret-rotation precedent 对称 (`feedback_audit_driven_fix_conventions` 治理一致性优先于 Memo 年度 cadence) |

## 落地工件 (本 commit)

1. **本文件** `.aria/decisions/2026-05-07-silknode-contract-archive-with-deferred-acceptance.md`
2. **新增 state-scanner 探针** `.aria/state-checks.yaml::silknode-contract-deferral-expiry` (WARN if `expires_at < now()` OR 触发条件命中)
3. **OD-9 retroactive owner ack** 段追加 (resolves acceptance #(b) Phase A.2 conditional)
4. **Spec 归档** `openspec/changes/aria-2.0-silknode-integration-contract/` → `openspec/archive/2026-05-07-aria-2.0-silknode-integration-contract/` + Status: Draft → Complete (Archived-with-Waiver)

## 重新评估时 SOP (任一触发条件命中后)

1. 读取本文件 §Acceptance Criteria 逐项判定表
2. 检查 deferred items (c+d) 当前状态:
   - (c) US-025 是否已 kickoff? 若是 → 验证 `silknode_storage_check` + `business_data_classification_check` 任务已写入 US-025 tasks.md
   - (d) US-026 / PRD v2.0 / CLAUDE.md 是否含 §契约 2 原文? grep 验证
3. 决定: 关闭 waiver (acceptance 全 MET) / 续期 waiver (新文件, 新 expires_at) / upgrade 至 standards/governance/silknode-no-storage.md
4. 更新本文件 `status` 字段 + 写 closure 段

## Audit Trajectory (3-round convergence)

| Round | Discussion group (legal-advisor + tech-lead) | Challenge group (backend-architect + qa-engineer) | Outcome |
|-------|----------------------------------------------|-------------------------------------------------|---------|
| **R1** | archive-as-absorbed (US-022 verbatim consumed + US-023 OD-3d generalized) | backend-architect: PARTIAL CONCUR (demand explicit waiver in `.aria/decisions/`); qa-engineer: OBJECTION (#d FAIL grep 0, #c UNTESTABLE, counter-proposal HOLD OPEN) | NOT_CONVERGED → R2 |
| **R2** | archive-with-explicit-waiver (legal-advisor: granular PASS/DEFER/WAIVE per criterion; tech-lead: 4 trigger conditions + 180-day hard cap) | backend-architect: BLOCKING — 90d not 180d + verbatim language + sign_off_mechanism field; qa-engineer: 4 OBJECTIONS (Phase A.2 papered over / #c stub commitment / expires_at machine-readable / explicit owner sig) | NOT_CONVERGED → R3 |
| **R3** | unified: 90d (concede to backend-architect) + verbatim "never mechanically enforced" + sign_off_mechanism: pr_approval + #b retroactive OD-9 ack + #c detection stub in-scope + expires_at YAML + audit trajectory | backend-architect: CONSENSUS REACHED 0 objections; qa-engineer: CONSENSUS REACHED 0 objections | **CONVERGED** |

Per `feedback_audit_convergence_pattern.md` strict definition: discussion group internally consistent across R3 + challenge group 0 objections + direction ALIGNED 4/4 全 3 rounds = 收敛达成.

## 跨引用

- `r1-legal-memo.md` v1.1 (`aria-orchestrator/docs/r1-legal-memo.md`) — 本 Spec 的源头依据
- `openspec/archive/2026-05-03-aria-2.0-m2-layer1-state-machine/proposal.md` — Acceptance (a) 证据
- `openspec/archive/2026-05-06-aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md` L132 + L369 — Acceptance (b) 证据 (OD-3d generalize)
- `.aria/decisions/2026-05-02-od-9-luxeno-reframe.md` — retroactive owner ack 段 (本 commit 追加, resolves Acceptance (b) Phase A.2 conditional)
- `.aria/decisions/2026-05-02-secret-rotation-deferred.md` — waiver 模板先例
- `.aria/state-checks.yaml::silknode-contract-deferral-expiry` — 机械检测探针 (本 commit 落地)
- `feedback_audit_convergence_pattern.md` / `feedback_audit_driven_fix_conventions.md` / `feedback_ad_slot_backfill_checkpoint.md` / `feedback_scaffold_helpers_drift_without_callers.md` — 方法论 anchors

## 版本历史

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05-07 | 初版. 3-round Spec discussion loop converged. Acceptance (a)+(b) MET, (c)+(d) deferred-with-waiver until 2026-08-05. Detection stub `.aria/state-checks.yaml::silknode-contract-deferral-expiry` 同 commit 落地. |
