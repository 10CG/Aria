# Decision: H0 cycle T8.2 Rule #6 benchmark skip (owner-directed)

**Date**: 2026-05-15
**Cycle**: H0 `aria-ten-step-session-handoff-stage`
**Decision type**: Process deviation (CLAUDE.md Rule #6 不可协商)
**Decided by**: Owner (explicit direction "跳过 T8.2,直接进 T8.3")
**Status**: Accepted with substitution evidence

---

## Context

CLAUDE.md Rule #6 (不可协商): **Skill 基准测试必须使用 `/skill-creator`**。
触发时机包括 "修改 Skill 逻辑 / 发版前质量审计"。

H0 cycle modified Skill logic:
- `state-scanner`: new `collectors/handoff.py` (Phase 1.15)
- `phase-d-closer`: new §D.3 step + template

Per literal Rule #6, T8.2 should run `/skill-creator` AB benchmark before v1.21.0 ship.

## Decision

T8.2 `/skill-creator` benchmark **skipped** per owner direction.

## Rationale

1. **Tautological for deterministic collectors**: `handoff.py` is a pure stdlib Python function (filesystem scan + mtime sort). LLM with/without-Skill AB would trivially show +100% (collector adds the field; absent collector lacks it). This was flagged independently by pre_merge R1 qa-M2 as "tautological benchmark". Aligns with memory `feedback_rule6_framing_differs_by_skill_type` — deterministic Skills warrant structural/deterministic metrics, not LLM with/without.

2. **Stronger substitute evidence already present**:
   - 442 Python unit tests (incl. 4 dedicated audit-fix tests) — 100% pass
   - 10 shell hook smoke tests — 100% pass
   - Live dogfood: state-scanner Phase 1.15 correctly surfaces handoff on Aria self (5 dogfood incidents, incl. cycle self-producing its own closeout)
   - 3-agent pre_merge R1 SCOPE_OK_R1 + 3-PR aria:code-reviewer audit

3. **Rule #6 intent satisfied**: the rule exists to answer "did the Skill change improve/not-regress quality". Deterministic unit tests + live dogfood answer this more precisely than an LLM AB for a non-LLM-driven Skill.

## What was NOT done (honest record)

- No `/skill-creator` benchmark run
- No entry in `aria-plugin-benchmarks/ab-results/` for H0
- The literal Rule #6 text ("必须使用 /skill-creator") was not followed

## Compensating controls

- This decision memo (audit trail per Aria "结构化决策记录" principle)
- Surfaced in closeout handoff §3 (known deviation, next-session aware)
- If future H-series cycle adds a **capability-type** Skill change (LLM-driven), Rule #6 `/skill-creator` benchmark is NOT waivable — this skip is scoped to deterministic collector/structural changes only

## Follow-up — ✅ RESOLVED 2026-05-17 (H4)

Structural Rule #6 closure executed retroactively:
- `aria-plugin-benchmarks/ab-results/2026-05-17-h0-handoff-structural/` —
  14/14 PASS (pass_rate 1.0) across 6 metric groups: mtime-sort accuracy,
  pointer-priority, misplaced precision (no FP), misplaced recall (no miss),
  latest.md exclusion, fallback/edge robustness. Covers post-H5
  pointer-priority + stale-pointer fallback.
- No defect found → no code change / version bump (validation activity).
- The owner-directed T8.2 skip is now **positively closed** with a
  deterministic structural result, not just a deferral rationale. This
  decision memo remains the record of the original skip + its scope
  (deterministic-only; capability-type still non-waivable — proven in H3
  iteration-3 which DID run a full capability AB).

## References

- CLAUDE.md Rule #6
- Memory: `feedback_rule6_framing_differs_by_skill_type`, `feedback_meta_cycle_dogfood_self_consistency`
- Archived spec: `openspec/archive/2026-05-15-aria-ten-step-session-handoff-stage/tasks.md` (T8.2 redefined metrics)
- pre_merge R1 qa audit (flagged tautological): `.aria/audit-reports/pre_merge-R1-2026-05-14T1500Z-aria-ten-step-session-handoff-stage-qa.md`
