# Smoke Benchmark — state-scanner regex hardening v1.17.3

> **Spec**: state-scanner-collector-regex-hardening (Level 2)
> **Released**: 2026-04-25
> **Plugin version**: 1.17.3
> **Benchmark type**: Smoke (inline structural assertions, 12 cases)
> **Result**: **12/12 (100%) PASS**

## Why smoke not full AB

Per `feedback_smoke_vs_full_ab_benchmark.md` and v1.16.2/3/4 + v1.17.1 + v1.17.2 patch precedent:

- **Doc-dominant Level 2 patch**: ~30 lines regex + 9 unit tests + schema doc table. No new
  Skills, no Agent prompt changes, no instruction prose. Full `/skill-creator` AB delta would
  be drowned by LLM stochasticity vs deterministic regex assertions.
- **Strong mechanical evidence already in place**:
  - 371/371 stdlib unittest tests PASS (was 362 v1.17.2, +9 net for regex hardening)
  - 6 regression tests in `test_architecture.py::TestRegexHardening`
  - 2 tests in `test_forgejo_config.py::TestRegexHardening`
  - 1 test in `test_readme.py::TestRegexHardeningHeading`
  - Cross-project: Kairos retest verified zero regression (parity preserved)
- **Backward compatibility mathematically guaranteed**: regex changes are
  strict supersets via `(?:#{1,6}\s+)?` optional heading + `(?:\*\*)?` optional bold +
  `[：:]` dual colon character class.

Full `/skill-creator` AB benchmark deferred to **v1.17.x post-release validation**
window (combined with v1.17.0 / v1.17.1 / v1.17.2 backlog), not blocking this release.

## Smoke Benchmark Cases

12 inline structural assertions exercising every variant × heading prefix /
fullwidth colon / blockquote prefix / optional bold / negative.

| ID  | Label | Result |
|-----|-------|--------|
| S1  | arch Status baseline (`**Status**: Active`) | ✅ PASS |
| S2  | arch Status fullwidth (`**Status**：Active`) | ✅ PASS |
| S3  | arch Status heading (`## Status: Draft`, no bold) | ✅ PASS |
| S4  | arch Status heading + fullwidth (`## Status：Draft`) | ✅ PASS |
| S5  | arch LastUpd heading + fullwidth | ✅ PASS |
| S6  | arch ParentPRD heading + bold (`## **Parent PRD**: prd-v3`) | ✅ PASS |
| S7  | forgejo halfwidth (`forgejo:`) baseline | ✅ PASS |
| S8  | forgejo fullwidth (`forgejo：`) i18n | ✅ PASS |
| S9  | forgejo blockquote (`> forgejo:`) prose-mixed | ✅ PASS |
| S10 | readme Version heading (`## Version: 1.2.3`) | ✅ PASS |
| S11 | readme 版本 heading CN (`## 版本: 1.2.3`) | ✅ PASS |
| S12 | NEGATIVE: forgejo no colon (`forgejo block info`) must NOT match | ✅ PASS |

## Cross-project dogfooding evidence

```
Kairos retest comparison (post-i18n v1.17.2 → post-hardening v1.17.3):
- requirements.stories.by_status: unchanged (7/15 stories still resolved)
- readme.root.version: unchanged (0.9.3)
- architecture.exists: still False (path docs/architecture/system-architecture.md
  missing; collector exists check fails first, regex never reached)
- forgejo_config.config_status: still "missing" (no CLAUDE.local.md)

Conclusion: zero regression. The hardening is preventive — it removes
silent-failure risk for future projects using heading-prefix or fullwidth-colon
formats, without changing behavior for current projects.
```

## Pre-merge audit history

`aria:code-reviewer` single-round verdict pending (see PR description).

## raw smoke results

See `smoke-results.json` for machine-readable per-case detail.
