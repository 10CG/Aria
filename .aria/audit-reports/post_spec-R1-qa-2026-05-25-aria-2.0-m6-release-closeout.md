# Phase A.2 R1 audit — qa-engineer — aria-2.0-m6-release-closeout

> **Spec commit**: `98218fb`
> **Audit date**: 2026-05-25
> **Agent**: aria:qa-engineer (Opus 4.7 sub-agent)
> **Audit perspective**: test strategy / binary-falsifiability / boundary coverage / mock-vs-live infrastructure / fixture leakage

## Verdict
**NEEDS_FIX**

## Summary

The Spec has strong structural bones — binary-falsifiable intent is present throughout, mock strategy is correctly placed at the subprocess transport layer, and the three-state verdict contract is well-reasoned. However, five testability defects are severe enough to allow bugs to ship undetected: wrong REPO_ROOT depth (silent file-missing ABORTs), provably wrong AC-3 dates (test labeled RED actually exercises ABORT), uncontracted `--all` flag on sibling scripts, G-6 stdout/G-3 secret-leak risk, and missing pytest scaffolding directory.

## Critical findings

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| C-qa-1 | tasks.md T-A2.1 line 50 | REPO_ROOT wrong depth (same as C-ba-1). All G-3/G-5/G-7/G-8 main-repo file access silently resolves under aria-orchestrator/. | Two-variable contract: ORCH_ROOT / MAIN_REPO_ROOT. |
| C-qa-2 | proposal.md AC-3 lines 355-361 | AC-3 dates arithmetically wrong vs tasks.md T-A3.4. `2026-07-22` → 11d = ABORT (not RED as labeled). `2026-07-28` → 5d = ABORT (correct verdict but label "13d" wrong). Proposal contradicts tasks.md (which has correct 2026-07-13 / 2026-07-20). | Fix proposal AC-3 dates: Test 2 → 2026-07-13 (20d RED); Test 3 → 2026-07-20 (13d ABORT). |
| C-qa-3 | proposal.md G-1/G-2 + tasks T-A2.2/T-A2.3 | `--all` flag uncontracted on sibling scripts (same as I-ba-1). | Invert primary path. |
| C-qa-4 | tasks.md T-A3 line 136 | `aria-orchestrator/tests/acceptance/` directory doesn't exist; no task creates it; T-A3 24 pytest entries unable to discover. | Add T-A1.4: create `aria-orchestrator/tests/` + `aria-orchestrator/tests/acceptance/__init__.py`. |
| C-qa-5 | proposal.md §A line 69 + tasks T-A2.11 vs T-A2.7 | G-6 stdout secret-leak path (same as I-ba-6). | T-A2.11 explicit per-gate: G-6 stderr-only. |

## Important findings

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| I-qa-1 | proposal.md AC-6 | Only 1 stale scenario; missing: marketplace[0] stale, plugin.json missing, 2-stale (multi-drift). | Add 3 scenarios. |
| I-qa-2 | proposal.md AC-5 + tasks T-A3.6 | PAT meta-test regex (`forgejo_pat_\w+`) is wrong: Forgejo PATs have no unique prefix; meta-test passes even with leaked token. | Reframe: assert no env-var refs to FORGEJO_TOKEN/ARIA_PAT + mock `forgejo` subprocess (never live call). |
| I-qa-3 | proposal.md AC-10 + tasks T-A4.4 | Idempotency not tested (twice `--execute`); rollback-also-fails not tested. | Add `test_archive_IDEMPOTENT` + `test_archive_ROLLBACK_also_fails`. |
| I-qa-4 | proposal.md §D G-5 + tasks T-A3.5 | G-5 fixture construction unspecified (local bare repo vs mock). Mock return-shape risk per `[[feedback_test_mock_pattern_hides_prod_bug]]`. | Prescribe: use `git init --bare` + `git submodule add file:///path`. |
| I-qa-5 | proposal.md AC-3 vs tasks T-A2.1 | `--only-gate` vs `--gates` (same as I-ba-3). | Unify on `--gates`. |
| I-qa-6 | proposal.md §B G-2 | G-2 `--all` exit code aggregation undefined for 3 TG groups. | Lock aggregation: any 2 → ABORT; any 1 → RED; all 0 → PASS. |

## Minor findings

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| N-qa-1 | proposal.md AC-3 title | "3 boundary tests" vs tasks 6 tests. | Rename AC-3 title to "6 boundary + edge tests". |
| N-qa-2 | proposal.md AC-3 line 363 | Cap-day-itself (buffer=0) not explicitly tested. | Add `test_G4_ABORT_cap_day_itself`. |
| N-qa-3 | proposal.md AC-1 | Help-text string assertions brittle. | Case-insensitive substring + add `--gates`. |
| N-qa-4 | proposal.md AC-9 | Whitespace-only rationale not covered. | Add `test_override_whitespace_only_rejected`. |
| N-qa-5 | proposal.md §H step 6 | Dry-run reads "last file" but dry-run doesn't write — could find stale file. | Step 6 skip entirely in dry-run mode. |
| N-qa-6 | proposal.md AC-7 + tasks T-A3.8 | G-8 missing "totally missing" scenario (neither changes/ nor archive/). | Add `test_G8_ABORT_totally_missing`. |
| N-qa-7 | tasks T-A4.3 | 3-second sleep test-time footgun. | Env var `M6_ARCHIVE_WARN_DELAY=0`. |
| N-qa-8 | proposal.md §A line 49-50 | `--gates` list notation unspecified (comma vs nargs). | Lock: comma-separated string parsed at runtime. |

## Q-escalations

| Q | Question |
|---|----------|
| Q-qa-1 | Should sibling Specs receive `--all` amendment (re-open sealed Specs)? |
| Q-qa-2 | Should `.aria/m6-release-readiness/*.md` reports be git-tracked? |
| Q-qa-3 | Is `aria-orchestrator/tests/acceptance/` the canonical pytest dir, or follow `hermes-extensions/aria-layer1/tests/`? |
| Q-qa-4 | Sub-second timestamp collision risk in summary report filename? |

---

**Audit trail**: `[[feedback_audit_driven_fix_conventions]]`
