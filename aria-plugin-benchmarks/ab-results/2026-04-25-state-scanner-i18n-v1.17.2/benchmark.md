# Smoke Benchmark — state-scanner i18n v1.17.2

> **Spec**: state-scanner-i18n-status-regex (Level 2)
> **Released**: 2026-04-25
> **Plugin version**: 1.17.2
> **Benchmark type**: Smoke (inline structural assertions, 12 cases)
> **Result**: **12/12 (100%) PASS**

## Why smoke not full AB

Per `feedback_smoke_vs_full_ab_benchmark.md` and v1.16.2/3/4 + v1.17.1 patch precedent:

- **Doc-dominant Level 2 patch**: ~25 lines regex + 7 unit tests + schema doc table. No new
  Skills, no Agent prompt changes, no instruction prose. Full `/skill-creator` AB delta would
  be drowned by LLM stochasticity vs deterministic regex assertions.
- **Strong mechanical evidence already in place**:
  - 362/362 stdlib unittest tests PASS (was 355, +7 net for i18n)
  - 5 cross-collector unit tests in `test_requirements.py::TestI18nStatusRegex`
  - 2 cross-collector unit tests in `test_openspec.py` (locks shared `_status.py`
    propagation)
  - Real-world dogfooding: Kairos `US-009-tts-voice-clone.md` retest showed
    `raw_status: null → "pending"` plus 6 additional stories newly resolved
    (7/15 from 0/15)
- **Backward compatibility mathematically guaranteed**: regex character-class
  widening (`:` → `[：:]`) is a strict superset; pattern 6 is purely additive.

Full `/skill-creator` AB benchmark deferred to **v1.17.x post-release validation**
window (combined with v1.17.0 / v1.17.1 backlog), not blocking this release.

## Smoke Benchmark Cases

12 inline structural assertions exercising every pattern × halfwidth/fullwidth
colon variant + the new pattern 6 + a negative prose case.

| ID  | Label | Result |
|-----|-------|--------|
| S1  | P1 halfwidth EN: `**Status**: Active` | ✅ PASS |
| S2  | P1 fullwidth EN (i18n widening): `**Status**：Active` | ✅ PASS |
| S3  | P2 halfwidth CN: `**状态**: pending` | ✅ PASS |
| S4  | **P2 fullwidth CN (i18n primary case)**: `**状态**：pending` | ✅ PASS |
| S5  | P3 blockquote EN halfwidth: `> **Status**: done` | ✅ PASS |
| S6  | P3 blockquote EN fullwidth: `> **Status**：done` | ✅ PASS |
| S7  | P4 heading prefix: `## Status: Reviewed` | ✅ PASS |
| S8  | P4 heading fullwidth: `## Status：Reviewed` | ✅ PASS |
| S9  | P5 table CN: `\| 状态 \| active \|` | ✅ PASS |
| S10 | **P6 NEW (Kairos US-009 real sample)**: `> **优先级**：P0 \| **里程碑**：M3 \| **状态**：pending` | ✅ PASS |
| S11 | P6 NEW status mid-line EN: `> **A**: 1 \| **Status**: in progress \| **B**: 2` | ✅ PASS |
| S12 | **NEGATIVE prose mention**: `## 用户故事\n用户期望知道当前状态：可能 pending` (must NOT match) | ✅ PASS |

## Cross-project dogfooding evidence

```
Pre-fix (v1.17.1):  Kairos 15 user stories → 0 raw_status resolved (0%)
Post-fix (v1.17.2): Kairos 15 user stories → 7 raw_status resolved (47%)
                    of which Kairos US-009 (Spec acceptance criterion) ✅
                    (8 remaining genuinely lack a status field — correct unknown)
```

## Pre-merge audit history

`aria:code-reviewer` single-round verdict: **MERGE_NOW** + 2 Important + 3 Minor
(all addressed before merge):
- Important #1: SKILL.md→schema.md reframe documented (3-touchpoint per
  `feedback_spec_reframe_in_session.md`) ✅
- Important #2: proposal.md off-by-one pattern numbering corrected ✅
- Minor #1: 2 _extract_status tests added to `test_openspec.py` to lock
  cross-collector path ✅

## raw smoke results

See `smoke-results.json` for machine-readable per-case detail.
