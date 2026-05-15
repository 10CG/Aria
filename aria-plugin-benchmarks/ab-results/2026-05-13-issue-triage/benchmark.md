# Skill Benchmark: issue-triage (iteration 1)

**Model**: claude-opus-4-7[1m]
**Date**: 2026-05-13
**Cycle**: aria-issue-triage-sop (T8 per Rule #6)
**Configurations**: with_skill (full SKILL.md + scripts/) vs without_skill (no skill, general engineering)
**Evals**: 3 (aria-101-direct-ref / silknode-207-url-only / ambiguous-recent-bug-ref)
**Assertions per eval**: ~8 lenient (capability) + 5 discriminating (structure) = ~13 total

## Summary

| Metric | with_skill | without_skill | Delta |
|---|---|---|---|
| **Overall pass rate** | 91.9% | 70.1% | **+21.8pp** |
| Lenient (capability) | 100% | 100% | +0.0pp (non-discriminating) |
| **Discriminating (structure)** | **80.0%** | **26.7%** | **+53.3pp** |
| Time (s, mean) | 140.2 | 76.9 | +63.3 (+82%) |
| Tokens (mean) | 64,112 | 40,437 | +23,675 (+59%) |

## Per-eval breakdown

| Eval | with_skill | without_skill | Δ |
|---|---|---|---|
| eval-1 (aria #101 direct ref) | 92.3% (12/13) | 76.9% (10/13) | +15.4pp |
| eval-2 (silknode #207 cross-repo) | 91.7% (11/12) | 66.7% (8/12) | +25.0pp |
| eval-3 (ambiguous #89/#90) | 91.7% (11/12) | 66.7% (8/12) | +25.0pp |

## Discriminating assertion breakdown

| Dimension | with_skill | without_skill | What it captures |
|---|---|---|---|
| D1 JSON output | 3/3 | 0/3 | Machine-readable triage-report.json |
| D2 dedicated triage-comment.md | 3/3 | 0/3 | Ready-to-post artifact vs mixed prose |
| D3 schema conformance | 0/3 | 0/3 | jsonschema validation pass (BOTH fail — see notes) |
| D4 canonical enums (3/3) | 3/3 | 1/3 | verdict + severity + recommended_action all from enum |
| D5 multi-artifact workflow | 3/3 | 3/3 | ≥2 distinct output files |

## Analyst observations

1. **Lenient assertions are non-discriminating** on Opus 4.7 with contextual evidence. Issue #101 had prior triage comments (#5972 manual + #6019 dogfood) — baseline agents read them and replicated the pattern. For sharper future evals, use issues with NO prior triage context.

2. **Discriminating delta is strong** (+53.3pp). The Skill's value is structure, machine-readability, and downstream automation potential — exactly what Rule #6's "is the Skill actually helping" question should measure for SOP-type Skills.

3. **D3 schema validation regression** (0/3 with_skill). All 3 with_skill agents hand-wrote JSON instead of invoking `scripts/triage.py`. Missing required field `body` in `steps.step1_issue`. SKILL.md needs explicit "MUST run scripts/triage.py for Step 0; do not hand-author JSON" — carry-forward to iteration-2.

4. **Cost asymmetry** (with_skill +82% time, +59% tokens). For a SOP/process Skill this is expected: structure has overhead. The value pays off in downstream automation (CI gating, audit trail, comment auto-post), not in single-shot speed.

5. **Cross-repo evals (eval-2 silknode + eval-3 ambiguous)** show stronger delta (+25pp each) than the direct-ref eval (+15.4pp). The Skill's value increases when context is sparser — confirming it's a useful guide for less-obvious cases.

## Rule #6 verdict

**PASS** — delta > 0 on overall pass rate (+21.8pp) and structural value (+53.3pp). The Skill provides real value beyond what Opus 4.7 produces with no scaffolding, primarily on structure and machine-readability dimensions.

**Caveat**: capability-level delta on this dataset is 0pp because Opus is strong enough to perform 6-step triage naturally when given good context. The Skill ships for SOP consistency, downstream automation, and as a teaching artifact for less-capable models or less-experienced reviewers — not as a capability uplift on Opus.

**Carry-forward to iteration-2 / Phase B follow-up**:
- SKILL.md emphasize "MUST run scripts/triage.py, do not hand-author JSON" (D3 regression cause)
- Add a non-contextualized eval (fresh issue, no prior triage comments) to strengthen capability-delta measurement
- Re-evaluate cost trade-off after CI / automation use cases land (where structural value compounds)
