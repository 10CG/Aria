# Phase A.2 R2 aggregate — aria-2.0-m6-release-closeout

> **R1-fix commit**: `cdd2e5e`
> **Audit date**: 2026-05-25
> **Agents**: backend-architect + qa-engineer + code-reviewer (3-agent challenge)
> **R2 raw reports**: post_spec-R2-{ba,qa,cr}-2026-05-25-aria-2.0-m6-release-closeout.md

## Aggregate verdict
**SPLIT 2 SCOPE_OK_R2 + 1 NEEDS_FIX_R2**

Per `[[feedback_cross_agent_verdict_independent_verify]]` 1/N NEEDS_FIX MUST owner-verify. Owner verified code-reviewer's 2 new Important findings TRUE 2026-05-25:
- **I-NEW-r2-1**: §Dependencies (proposal.md:629-630) + Risk-mit checklist (tasks.md:399-400) still say `--all` while R1-fix body inverted to per-flag canonical — paper-fix antipattern propagation
- **I-NEW-r2-2**: AD-M6-10 lock says "exit 0/1/2" + AC-1 says "No other exit codes" — but R1-fix introduced exit 3 (archive inconsistent-state) + exit 20 (hard pre-condition); AD lock vs reality gap

## R1 closure aggregate

| Agent | R1 Closed | Reduction |
|-------|-----------|-----------|
| backend-architect | 11/12 (1 PARTIAL N-ba-2) | 92% |
| qa-engineer | 15/19 (3 PARTIAL: I-qa-2, N-qa-3, N-qa-6) | 74% |
| code-reviewer | 19/22 (2 PARTIAL: I-cr-6, N-cr-10) | 77% |

Consolidated R1 Critical closure: **5/5 (100%)** across all 3 agents.

## New findings (R2 unified)

### Important (4 themes, all owner-verified TRUE)

| Unified ID | Source | Issue | R2-fix path |
|-----------|--------|-------|-------------|
| **R2-I1** | cr-NEW-r2-1 | §Dependencies + Risk-mit `--all` stale (paper-fix propagation) | Replace stale text in 4 locations |
| **R2-I2** | cr-NEW-r2-2 | AD-M6-10 + AC-1 exit code contract incomplete (missing exit 3 + 20) | Amend AD-M6-10; rewrite AC-1 exit code section |
| **R2-I3** | ba-R2-1 | G-4 ABORT branch code vs AC-3 Test 5/6 message format mismatch | Split ABORT branch into 2 subcases (positive-but-<14d + negative past-cap) |
| **R2-I4** | qa-R2-1 | phase-d-closer exit code 3 caller behavior unspecified | Add §H Phase D.2 caller contract table for all exit codes |

### Minor (6 themes)

| Unified ID | Source | Issue |
|-----------|--------|-------|
| R2-N1 | cr-NEW-r2-1 | AC-9 heading "env var" stale (CLI flag is mechanism) |
| R2-N2 | cr-NEW-r2-2 + qa-R2-2 | 4 residual "5-files" literals (proposal:31/392/591 + tasks:342) |
| R2-N3 | cr-NEW-r2-3 | `<R1-FIX-COMMIT-PENDING>` placeholder in Audit trajectory line 17 |
| R2-N4 | ba-R2-1 | rollback exit code 2 vs 3 in T-A4.1 code block |
| R2-N5 | qa-R2-1 | M6_ARCHIVE_NO_COUNTDOWN env var undocumented in proposal |
| R2-N6 | qa-R2-3 | "possibly aria-orchestrator/" stale qualifier in Dependencies table |

Plus R1 PARTIALs (close in R2-fix):
- ba-N-ba-2: G-8 self-check prose-only — wire to T-A2.9 + AC-7 + add test_G8_ABORT_self_missing
- qa-I-qa-2: PAT meta-test fixture_file scoping — explicit `pathlib.Path(__file__).parent.glob('*.py')`
- qa-N-qa-3: --gates missing from AC-1 keyword list
- qa-N-qa-6: test_G8_ABORT_totally_missing missing

## R2-fix scope (committed `<R2-FIX-COMMIT-PENDING>`)

**Proposal.md edits** (~12):
- Audit trajectory frontmatter: replace placeholder + add R2 status
- §Why bullet 3: 5-files → 6-surfaces
- §C G-4 code block: split ABORT into 2 subcases (positive + negative)
- §H Step 7+: Phase D.2 caller contract table for exit codes 0/1/2/3/20
- AC-1 exit code contract: explicit enumeration of 0/1/2/3/20
- AD-M6-10: amend to include exit 3 + 20 with `phase-d-closer` D.2 caller contract reference
- AC-9 heading: env var → CLI flag
- §How diagram: 5-files → 6-surfaces, add per-flag annotations
- R-M6CL-4: 5-files → 6-surfaces
- §Dependencies G-1/G-2 rows: --all → per-flag canonical
- §G G-8 PASS condition: wire self-check
- AC-7: add test_G8_ABORT_totally_missing + test_G8_ABORT_self_missing
- AC-1 help text: add --gates keyword
- AC-5 PAT meta-test: explicit fixture_file scope

**Tasks.md edits** (~6):
- Risk-mit checklist A-1/A-2: --all → per-flag
- CLAUDE.md insert template (T-A5.3): 5-files → 6-surfaces
- T-A3.6 PAT meta-test: explicit pathlib glob
- T-A2.9: REQUIRED_SIBLINGS → 4 entries (3 + self)
- T-A3.8: 4 scenarios (PASS + prearchived + totally_missing + self_missing)
- T-A3.2: --gates keyword added

Diff: +70/-28 lines. Per `[[feedback_3round_early_convergence]]` <100 lines + 0 logic change qualifies for R3 stability check.

## R3 stability plan

Per `[[feedback_pre_merge_4round_convergence_template]]` adapted to post_spec: R3 = 1-agent scope-limited (tech-lead-critic OR code-reviewer) verifies R2-fix:
1. Does R2-fix substantively close R2-I1..R2-I4 + R2-N1..R2-N6?
2. Does R2-fix introduce NEW Critical?
3. Are byte-exact (regex / line numbers / paths) still consistent?

If R3 returns R3_STABLE (0 new C + 0 new I + 3/3 confirmed CLOSED), Spec flips Draft → **Approved**.

## Collapse decision

Per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`:
- ❌ R2 4/4 SCOPE_OK requirement: SPLIT (2/3 SCOPE_OK_R2, 1 NEEDS_FIX_R2)
- ✅ R1 critical 100% closed (5/5)
- ✅ ≥70% reduction (77-92% across agents)
- ✅ 0 new Critical
- ✅ All NEW findings owner-verified TRUE + substance-level fixable

**Decision (owner-invoked convergence loop per `[[feedback_owner_invoked_convergence_loop]]`)**: do NOT collapse R3 default; run R3 stability check post R2-fix per `[[feedback_3round_early_convergence]]` allowance (R2-fix <100 lines + 0 logic). Spec flips Approved only if R3_STABLE.
