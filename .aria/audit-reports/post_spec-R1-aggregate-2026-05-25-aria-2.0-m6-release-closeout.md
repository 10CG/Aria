# Phase A.2 R1 aggregate — aria-2.0-m6-release-closeout

> **Spec commit**: `98218fb`
> **Audit date**: 2026-05-25
> **Agents**: backend-architect + qa-engineer + code-reviewer (3-agent parallel, Level 2 proportionality per `[[feedback_agent_team_for_level1]]`)
> **R1 raw reports**: post_spec-R1-{ba,qa,cr}-2026-05-25-aria-2.0-m6-release-closeout.md

## Aggregate verdict
**NEEDS_FIX 3/3** — All 3 auditors verdict NEEDS_FIX with convergent Critical themes.

## Convergent Critical themes (≥2 agent flag)

| Theme | Agents | Unified ID | Owner Q? |
|-------|--------|-----------|----------|
| REPO_ROOT depth wrong (cross-repo file reads under wrong root) | ba + qa | C1 (ba-1 + qa-1) | No — fix unilaterally (2-var contract) |
| G-7 file format regex broken (3 of 6 surfaces) | ba + cr | C2 (ba-2 + cr-1/cr-2/cr-3) | Yes Q1 — main /VERSION stale fix path |
| `--all` flag uncontracted by siblings | ba + qa + cr | C3 (ba-1 + qa-3 + cr-4) | Yes Q3 — owner locked: invert primary path |
| G-6 stdout secret-leak path | ba + qa | C6 (ba-6 + qa-5) | No — fix per-gate capture |
| AC-3 boundary date arithmetic wrong | qa | C4 | No — fix proposal dates |
| G-5 submodule misclassification | cr | C5 | No — enumerate all 3 |
| pytest scaffolding missing | qa | C7 | No — add T-A1.4 |

## Convergent Important themes

| Theme | Agents | Unified ID |
|-------|--------|-----------|
| `--only-gate` vs `--gates` flag name | ba-3 + qa-5 | I1 (unify on `--gates`) |
| G-2 fallback aggregation semantics undefined | ba-2 + qa-6 | I2 |
| G-5 offline contradiction (proposal vs tasks) | ba-4 | I3 |
| Memory refs to non-existent files | cr-1 | I4 |
| Phase D archive ownership vs Skills | cr-2 | I5 (Q2 — owner locked: phase-d-closer delegation) |
| G-6 URL contract — RED is expected v2.0.0 | cr-3 | I6 |
| G-7 "5-files" vs actually 6 surfaces | cr-4 | I7 |
| Dry-run polarity opaque | cr-6 | I8 |
| AC-6 missing scenarios | qa-1 | I9 |
| PAT meta-test wrong | qa-2 | I10 |
| AC-10 idempotency + double-rollback gap | qa-3 | I11 |
| G-5 fixture construction unspecified | qa-4 | I12 |

## Owner Q-escalations (resolved 2026-05-25 in session)

| Q | Resolution |
|---|-----------|
| Q1 (G-7 main /VERSION stale) | **Locked**: Spec #4 Phase B T-A1.4 task reconciles before G-7 verify (preserves Spec #4 self-contained). |
| Q2 (archive runner ownership) | **Locked**: Spec #4 Python script is phase-d-closer D.2 delegation target. Document in §A.7.1. |
| Q3 (`--all` flag) | **Locked**: Invert primary/fallback — per-flag aggregation canonical (don't amend sealed sibling Specs). |
| Q-ba-1 (MAIN_REPO_ROOT method) | **Locked unilaterally**: Use `git rev-parse --show-toplevel` (robust; only adds one subprocess at startup). |
| Q-ba-2/Q-cr-3 (state-checks Spec #3 OOS-6) | **Defer**: G-5 sufficient for release-time gate; continuous state-checks probe is M7+ scope (note in OOS table). |
| Q-qa-2 (reports git-tracked?) | **Confirm**: Keep tracked (audit trail value); rely on G-6 stderr-only capture for secret hygiene. |
| Q-qa-3 (pytest dir convention) | **Confirm**: `aria-orchestrator/tests/acceptance/` (T-A1.4 creates). |
| Q-qa-4 (sub-second timestamp) | **Accept low-prob risk**: Add `%f` microseconds OR rely on `sleep 1` in test only (defer to Phase B). |

## R1-fix plan (apply to proposal.md + tasks.md)

**Proposal.md** ~15 edits:
- C1: §A + §D + §F + §G + §E REPO_ROOT 2-variable refs
- C2: §F lines 154/156 regex fix; §F line 158 main /VERSION reconcile note
- C3: §B G-1/G-2 invert; §B detail update; §Assumptions A-1/A-2 update
- C4: AC-3 dates 2026-07-22 → 2026-07-13; 2026-07-28 → 2026-07-20
- C5: §D G-5 enumerate all 3 submodules
- C6: AC-5 PAT meta-test reframe; §A summary report per-gate capture rule
- I1: AC-3 `--only-gate` → `--gates`
- I3: §D step 2 drop `--use-local-master`
- I4: §Cross-references memory list cleanup
- I5: §A NEW §A.7.1 phase-d-closer delegation doc
- I6: G-6 URL contract clarify RED-is-expected
- I7: G-7 clarify 5+1 surfaces
- I8: §H Step 4 dry-run polarity
- I9: AC-6 +3 scenarios
- AC-9 +whitespace
- AC-10 +idempotent +double-rollback

**Tasks.md** ~15 edits:
- C1: T-A2.1 REPO_ROOT 2-var
- C2: T-A2.8 regex fixes
- C3: T-A1.3 verify probe per-flag; T-A2.2/T-A2.3 primary path inversion
- C4: T-A3.4 already correct (no edit needed)
- C5: T-A2.6 drop in-tree special case
- C6: T-A2.11 per-gate capture; T-A2.7 reinforced
- C7: T-A1.4 NEW pytest scaffolding + main /VERSION reconcile
- I1: T-A3.4 use `--gates`
- I2: T-A2.3 explicit fallback aggregation
- I3: T-A2.6 offline mechanism single source
- I4: T-A6.1 candidate note already correct
- I5: §A.7.1 cross-ref to T-A4
- I9: T-A3.7 +3 scenarios
- I10: T-A3.6 PAT meta-test reframe
- I11: T-A4.4 +idempotent +double-rollback
- I12: T-A3.5 explicit fixture construction

## Phase A.2 R2 prediction

Per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` collapse criteria: R2 4/4 SCOPE_OK + R1 critical 100% closed + ≥70% reduction → collapse R3.

R1 = 17 Critical (de-dup ~7 themes) + ~12 Important. R2 expects:
- 7/7 Critical themes closed
- 12/12 Important themes closed or scope-acknowledged
- New findings ≤5 (R2 self-introduced or sibling drift catch)

If R2 unanimous SCOPE_OK_R2 + 0 new Critical + ≥70% finding reduction → collapse R3, flip Approved.

---

**Audit trail**: `[[feedback_audit_driven_fix_conventions]]` — R1-fix commit message will cite Unified IDs C1..C7 + I1..I12 for traceability.
