# H0 handoff collector — structural benchmark (Rule #6 deterministic)

**Date**: 2026-05-17 | **Collector**: `collectors/handoff.py` @ aria-plugin v1.21.3 (post-H5 pointer-priority)
**Type**: deterministic-type Rule #6 (per memory `feedback_rule6_framing_differs_by_skill_type` — pure stdlib function → structural metrics, NOT LLM with/without AB)
**Closes**: owner-directed T8.2 skip (`.aria/decisions/2026-05-15-h0-rule6-benchmark-skip.md` §Follow-up) — H4 carry-forward

## Result

**14/14 PASS — pass_rate 1.0**

| Metric group | Result | What it proves |
|--------------|--------|----------------|
| M1 mtime-sort accuracy | 2/2 | Newest-by-mtime correctly picked when no pointer (5-file + single-file) |
| M2 pointer-priority | 2/2 | `latest.md` target wins over newer-mtime predecessor (`./`-prefixed + bare filename forms) |
| M3 misplaced precision (no FP) | 2/2 | Clean `docs/handoff/` → no false misplaced; non-`.md` in `.aria/handoff/` not flagged |
| M4 misplaced recall (no miss) | 2/2 | All `.aria/handoff/*.md` detected + sorted; drift state (both dirs) correct |
| M5 latest.md exclusion | 2/2 | Pointer file never a candidate (only-latest.md → exists=false); never flagged misplaced |
| M6 fallback/edge robustness | 4/4 | Stale pointer → soft_error + mtime fallback; no pointer → mtime; empty dir; absent dir |

## Why this is the right Rule #6 framing for H0

The H0 collector is a pure `stdlib` filesystem function. An LLM with/without AB would be tautological (the field exists iff the collector runs) — flagged in the pre_merge R1 qa audit and recorded in the Rule #6 decision memo. The meaningful question for a deterministic Skill is **mechanical correctness across the input space**: does it pick the right "latest" under pointer/mtime/stale/empty/drift conditions, and classify misplaced files with precision=recall=1.0. This benchmark answers exactly that.

## Relationship to unit tests

`test_handoff.py` (19 unit tests) and this structural benchmark are complementary, not redundant:
- Unit tests = white-box, fast CI regression guard, per-function
- Structural benchmark = black-box scenario matrix stored in `ab-results/` as the **Rule #6 artifact** (the auditable "is the Skill mechanically correct" record the methodology requires), covering the post-H5 pointer-priority behavior end-to-end

## Verdict

**Rule #6 retroactively satisfied for H0** (deterministic framing). The owner-directed T8.2 skip is now closed with a positive structural result — no defect found, collector is correct across all 14 fixture scenarios including the H5 pointer-priority + stale-pointer fallback paths. No code change, no version bump (validation activity per CLAUDE.md Rule #6: "运行 benchmark 是验证活动").
