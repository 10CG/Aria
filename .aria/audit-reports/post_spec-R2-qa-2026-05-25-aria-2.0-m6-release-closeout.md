# Phase A.2 R2 audit — qa-engineer — aria-2.0-m6-release-closeout

> **R1-fix commit**: `cdd2e5e`
> **Audit date**: 2026-05-25
> **Agent**: aria:qa-engineer (Sonnet 4.6 sub-agent, R2 challenge round)
> **Audit perspective**: test strategy / R1 closure verification / new test-quality risks

## Verdict
**SCOPE_OK_R2**

All 5 original Critical findings substantively closed. 2 PARTIAL findings (I-qa-2 fixture_file scoping; N-qa-3/N-qa-6 partial test additions) are testability gaps but not new failure modes. No new Critical findings.

## R1 finding closure summary

| Category | R1 Count | Closed | Partial | Not Closed |
|----------|----------|--------|---------|------------|
| Critical | 5 | 5 (100%) | 0 | 0 |
| Important | 6 | 5 | 1 (I-qa-2) | 0 |
| Minor | 8 | 5 | 2 (N-qa-3, N-qa-6) | 1 |

### Critical (all CLOSED)
- C-qa-1 REPO_ROOT depth: CLOSED via 2-var contract (verified in T-A2.1)
- C-qa-2 AC-3 dates: CLOSED — date re-arithmetic Python verified all 6 dates
- C-qa-3 --all uncontracted: CLOSED — per-flag canonical throughout
- C-qa-4 pytest dir missing: CLOSED — T-A1.4 creates __init__.py files
- C-qa-5 G-6 stdout secret leak: CLOSED — per-gate capture rule consistent across gate function + T-A2.11 + T-A3.6 test assertion

### Important (5/6 CLOSED + 1 PARTIAL)
- I-qa-1/3/4/5/6: CLOSED
- I-qa-2 PARTIAL: `fixture_text` variable undefined in PAT meta-test; needs explicit scope (R2-fix addresses)

### Minor (mixed)
- N-qa-1/2/4/5/7/8: CLOSED
- N-qa-3 PARTIAL: --gates missing from AC-1 help-text keyword list (R2-fix addresses)
- N-qa-6 PARTIAL: G-8 "totally missing" code path exists but no test added in T-A3.8 (R2-fix addresses)

## New findings (R2 independent scan)

### New Important

| ID | Severity | Location | Issue | Recommended fix |
|----|----------|----------|-------|-----------------|
| I-qa-R2-1 | Important | proposal.md §J phase-d-closer delegation diagram | Exit code 3 (NEW from R1-fix) caller behavior unspecified in delegation contract. `phase-d-closer` D.2 could silently swallow exit 3 as "non-zero failure", missing the "manual intervention required" escalation. | Add explicit caller contract for exit 3 in §J: "MUST halt + surface error verbatim + no auto-retry". |

### New Minor

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| N-qa-R2-1 | proposal.md §H or AC-10 | M6_ARCHIVE_NO_COUNTDOWN env var undocumented in proposal (only in tasks T-A4.3). | Document in §H env var surface + AC-10. |
| N-qa-R2-2 | proposal.md §Dependencies table lines 629-630 | Stale --all references (sister to C3 propagation miss). | s/--all/--per-flag/. |
| N-qa-R2-3 | proposal.md §Dependencies table line 634 | "possibly aria-orchestrator/" stale qualifier vs confirmed 3 submodules. | Drop "possibly". |

## Reduction metric
- R1 total: 19 findings (5C + 6I + 8N)
- Closed: ~15 (5C + 5I + 5N)
- Partial: 3 (1I + 2N)
- New: 4 (1I + 3N)
- Net residual: 0 Critical, 2 Important, 5 Minor
- Gross reduction: ~74%

## Collapse recommendation

**SCOPE_OK_R2** if backend-architect + code-reviewer concur. R1 Critical 100% closed, 0 new Critical, ≥70% gross reduction. Per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` → collapse R3 (with R2-fix for I-qa-R2-1 + N-qa-R2-1/2/3 first).
