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

## Follow-up (optional, non-blocking)

If methodology team wants strict Rule #6 closure for H0 retroactively:
- Run structural metric benchmark (mtime sort accuracy on fixture set + misplaced detection precision/recall) per the redefined T8.2 in archived tasks.md, store in `aria-plugin-benchmarks/ab-results/2026-05-XX-h0-handoff-stage/`
- Tracked as carry-forward H4 in handoff (low priority)

## References

- CLAUDE.md Rule #6
- Memory: `feedback_rule6_framing_differs_by_skill_type`, `feedback_meta_cycle_dogfood_self_consistency`
- Archived spec: `openspec/archive/2026-05-15-aria-ten-step-session-handoff-stage/tasks.md` (T8.2 redefined metrics)
- pre_merge R1 qa audit (flagged tautological): `.aria/audit-reports/pre_merge-R1-2026-05-14T1500Z-aria-ten-step-session-handoff-stage-qa.md`
