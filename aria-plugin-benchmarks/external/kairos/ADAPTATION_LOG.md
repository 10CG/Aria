# Kairos Adaptation Log

> **Project**: Kairos (AI private domain sales automation)
> **Pilot Start**: 2026-04-01
> **Tech Stack**: TypeScript / Node.js / Vitest
> **Existing Aria**: OpenSpec + UPM (partial, no plugin)

This log records all adaptations, issues, and observations during the Aria pilot in Kairos.

---

## Setup Phase

### aria-plugin Installation
- Date: 2026-04-01
- Steps taken: Created `.aria/config.json` with default settings, added `.aria/` to `.gitignore`
- Issues encountered: None — setup was trivial since Kairos already had OpenSpec + UPM

### Configuration
- Date: 2026-04-01
- .aria/config.json: workflow.auto_proceed=false, tdd.strictness=advisory
- Customizations needed: None — defaults work for Kairos

---

## Adaptation Records

### [2026-04-01] commit-msg-generator shows no quantitative delta on clear change descriptions

**Component**: commit-msg-generator
**Severity**: suggestion
**Description**: AB benchmark on 2 Kairos-specific eval cases (LLM provider bugfix + console feature) produced EQUAL verdict (delta 0.0). Both with_skill and without_skill generated correct Conventional Commits. The Skill's internal Aria delta is +0.80, suggesting its value is context-dependent.
**Adaptation**: None needed — Skill works correctly, just doesn't differentiate on straightforward scenarios.
**Recommendation**: The Skill's real value may be in ambiguous/complex scenarios (multi-module changes, scope selection for large commits). Consider adding harder eval cases that test edge cases where vanilla Claude falters. Also, with_skill produced better qualitative output: decision rationale, convention-aware scoping, and matched Kairos's Chinese commit style.

---

## Benchmark Results

| Skill | Delta | Verdict | Notes |
|-------|-------|---------|-------|
| commit-msg-generator | 0.0 | EQUAL | Qualitative advantages (scope precision, convention matching) but no pass-rate difference |
| state-scanner | +0.25 | WITH_BETTER | Interactive numbered workflow selection + confidence scoring; without_skill gives advice but no interactive format |
| spec-drafter | 0.0 | EQUAL | Both produce comprehensive Level 3 specs; with_skill correctly separates proposal.md + tasks.md |

---

## Summary

(Partial — pilot ongoing)

### What Worked
- .aria/config.json setup was zero-friction
- Kairos's existing OpenSpec + UPM structure is fully compatible
- Benchmark framework works seamlessly with external project context
- state-scanner's interactive workflow selection is genuinely useful cross-project
- spec-drafter correctly identifies Level 3 and generates separate tasks.md

### What Didn't Work
- commit-msg-generator didn't show quantitative improvement on simple scenarios
- spec-drafter content quality is matched by vanilla Claude (both excellent)

### Adaptations Required
- None — Aria tooling is compatible with Kairos out of the box

### Key Insight
**Process-oriented Skills transfer better than Content-oriented Skills.**
- state-scanner (+0.25): unique interactive workflow selection
- aria-report (+0.375 on Aria): mandatory privacy review
- commit-msg-generator (0.0): vanilla Claude already writes good commits
- spec-drafter (0.0): vanilla Claude already writes good specs

### Metrics
- commit-msg-generator: delta 0.0 (EQUAL)
- state-scanner: delta +0.25 (WITH_BETTER)
- spec-drafter: delta 0.0 (EQUAL)
- Overall: delta +0.0625 (MIXED)
