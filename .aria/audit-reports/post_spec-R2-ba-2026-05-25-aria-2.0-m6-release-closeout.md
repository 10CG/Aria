# Phase A.2 R2 audit — backend-architect — aria-2.0-m6-release-closeout

> **Spec commits audited**: original `98218fb` (R1), R1-fix `cdd2e5e` (current)
> **Audit date**: 2026-05-25
> **Agent**: aria:backend-architect (Sonnet 4.6 sub-agent, R2 challenge round)
> **Audit perspective**: orchestrator architecture / subprocess semantics / gate composition / atomic archive runner / R1 closure verification

## Verdict
**SCOPE_OK_R2**

All 2 Critical findings CLOSED with concrete, code-level precision. All 6 Important findings CLOSED with task-level substance. All 4 Minor findings addressed (N-ba-2 PARTIAL — self-check prose without task wire, addressed by R2-fix). The R1-fix introduced no new Critical issues. One new Important emerges from R1-fix (I-ba-R2-1 G-4 ABORT message template inconsistency between code block and AC-3 Tests 5/6).

## R1 finding closure verification

| ID | R1 finding | R2 verdict | Evidence |
|----|-----------|------------|----------|
| C-ba-1 | REPO_ROOT depth off-by-one | CLOSED | proposal §"REPO_ROOT 2-variable resolution" (~lines 318-352) + tasks T-A2.1 (~lines 60-79). ORCH_ROOT + MAIN_REPO_ROOT both defined via git rev-parse --show-toplevel with CLAUDE.md sanity check + fallback. Code-level, not advisory. |
| C-ba-2 | G-7 aria/VERSION + aria/README.md regexes wrong | CLOSED | Live format verified independently 2026-05-25: aria/VERSION = `> **版本**: 1.27.0` (Chinese MD blockquote); aria/README.md = `> **Version**: 1.27.0 | ...` (English). Both regexes rewritten with anchored `^>\s*` prefix + capture group. All 6 surfaces table updated. |
| I-ba-1 | --all flag uncontracted | CLOSED | G-1/G-2 tables (lines 78-80) + detail (lines 85-87) all use per-flag canonical. Optional fast-path documented. Assumptions A-1/A-2 verify individual flags. |
| I-ba-2 | G-2 fallback aggregation ambiguous | CLOSED | G-2 detail explicit: "any returncode 2 → ABORT; any returncode 1 (no 2) → RED; all 0 → PASS". Tasks T-A2.3 matches. |
| I-ba-3 | --only-gate vs --gates flag name | CLOSED | All occurrences unified on --gates G-N. AC-3 evidence + T-A2.1 argparse + T-A3.4 tests. |
| I-ba-4 | G-5 offline mechanism contradiction | CLOSED | Removed --use-local-master CLI flag idea. Automatic RED-on-ls-remote-failure is single mechanism. |
| I-ba-5 | §H step 1 env var vs CLI arg | CLOSED | "forwarding --owner-override CLI arg" explicit. |
| I-ba-6 | G-6 stdout suppression contradiction | CLOSED | T-A2.11 per-gate capture rules; G-6 stderr ONLY; report writer handles stdout=None placeholder. AC-5 negative assertion added. |
| N-ba-1 | UTC assumption undocumented | CLOSED | AC-3 boundary semantics adds UTC explanation. |
| N-ba-2 | G-8 doesn't verify self | PARTIAL | proposal §G says "checked separately" but G-8 code only loops REQUIRED_SIBLINGS (3 names), not self. Self-check is documented prose-only, not wired to code or AC. (Addressed by R2-fix N-ba-2.) |
| N-ba-3 | 3s sleep no test escape hatch | CLOSED | M6_ARCHIVE_NO_COUNTDOWN env var added. |
| N-ba-4 | G-4 boundary tests no gate isolation | CLOSED | --gates G-4 selector used in all 6 boundary tests. |

## New findings (R2 independent scan)

### Important

| ID | Severity | Location | Issue | Recommended fix |
|----|----------|----------|-------|-----------------|
| I-ba-R2-1 | Important | proposal.md §C G-4 code block (lines 105-110) vs AC-3 Test 5/6 | G-4 ABORT branch in code block emits `"buffer_days d < 14d"` for ALL ABORT cases. AC-3 Test 5 (cap-day) asserts `"buffer 0d"` (no `< 14d` suffix). AC-3 Test 6 (past-cap) asserts `"cap exceeded by N days"`. Code block ≠ AC assertions. | Either split ABORT branch into two subcases (buffer_days==0 + buffer_days<0 + 0<buffer_days<14), OR update AC tests to match single-branch format. Code-block-authoritative is architecturally cleaner. |

### Minor

| ID | Severity | Location | Issue | Recommended fix |
|----|----------|----------|-------|-----------------|
| N-ba-R2-1 | Minor | tasks.md T-A4.1 step 5 rollback code block | `raise SystemExit(...)` hardcodes exit 2, but proposal §H step 5 + T-A4.5 specify exit code 3 for inconsistent-state. Code block contradicts exit-code contract. | Update rollback to `sys.exit(3)` + add summary-log call before exit. |

## Reduction metric

- R1 findings: 2 Critical + 6 Important + 4 Minor = 12 total
- R2 CLOSED: 11 (92%)
- R2 PARTIAL: 1 (N-ba-2 prose-only)
- R2 NOT_CLOSED: 0
- R2 new Critical: 0
- R2 new Important: 1 (I-ba-R2-1 G-4 message format)
- R2 new Minor: 1 (N-ba-R2-1 exit code 2 vs 3 in rollback block)

## Q-escalations

| Q | Question |
|---|----------|
| Q-ba-R2-1 | G-4 ABORT branch: code block authoritative (single template) or AC assertions authoritative (distinct messages per cap-day / past-cap)? AC-authoritative cleaner. |

## Collapse recommendation

**SCOPE_OK_R2** + 0 new Critical + 92% reduction (11/12 CLOSED). Per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` → recommend **collapse R3 default**. The 1 new Important is message-format-only (verdict logic untouched).

If owner prefers explicit fix: ~10min to split G-4 ABORT branch + 5min rollback exit code; no cross-cutting ripple.
