# Phase A.2 R1 audit — code-reviewer — aria-2.0-m6-release-closeout

> **Spec commit**: `98218fb`
> **Audit date**: 2026-05-25
> **Agent**: aria:code-reviewer (Opus 4.7 sub-agent)
> **Audit perspective**: spec compliance / sibling AC byte-exactness / memory citation validity / cross-ref line numbers / Aria convention adherence

## Verdict
**NEEDS_FIX**

## Summary

Spec #4 is structurally well-organized and propagates effort SoT correctly, but contains 5 Critical byte-exactness violations against sibling Spec contracts (G-7 5-files SemVer probe has 3 broken regex patterns vs reality, G-1/G-2 invoke `--all` flags that NO sibling Spec actually ships, and G-5 misclassifies aria-orchestrator submodule as in-tree). Two cited memory entries flagged as "candidates" are confirmed non-existent, and one cross-Skill Phase D mechanism conflict (T-A4 archive runner duplicates `aria:phase-d-closer` + `aria:openspec-archive`) is not resolved.

## Critical findings

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| C-cr-1 | proposal.md:154 + tasks.md:102 | G-7 `aria/VERSION` regex zero matches against actual `> **版本**: 1.27.0` Chinese markdown blockquote format. | Fix regex to `(?<=\*\*版本\*\*: )([\d.]+)` (mirrors Spec #3 Probe 2 line 202 verified pattern). |
| C-cr-2 | proposal.md:156 + tasks.md:104 | G-7 `aria/README.md` regex `^\*\*Version\*\*:\s*v?(\S+)` zero matches. Actual: `> **版本**: 1.27.0 \| ...` Chinese blockquote (lines from live grep). | Fix regex same Chinese format. |
| C-cr-3 | proposal.md:158 + tasks.md:105 | G-7 main `/VERSION` regex correctly extracts but value is **currently stale** (v1.23.1 vs plugin.json v1.27.0). G-7 will ABORT day-1 of Phase B testing. | Owner Q-lock: T-A1.4 reconcile main /VERSION row to current plugin.json SoT version before Phase B G-7 verify (decided). |
| C-cr-4 | proposal.md G-1/G-2 + A-1/A-2 + tasks T-A2.2/T-A2.3 | Sibling scripts don't ship `--all` flag (live grep verified: Spec #1 = 4 individual flags; Spec #2 = 3 `--tg-*` flags only). | Invert primary path (owner Q-lock confirmed). |
| C-cr-5 | proposal.md:118 | G-5 misclassifies `aria-orchestrator/` as in-tree, but `.gitmodules` declares it as submodule (3 submodules total: aria/, standards/, aria-orchestrator/). G-5 silently skips most-likely-to-drift submodule. | Enumerate all 3 submodules unconditionally; drop in-tree special case. |

## Important findings

| ID | Location | Issue | Recommended fix |
|----|----------|-------|-----------------|
| I-cr-1 | proposal.md:535-536 | Two cited `[[memory-name]]` references don't exist as files: `feedback_release_phase_d_5_files_synchronization` + `feedback_pre_release_orchestrator_gate_pattern`. | Mark as "(NEW candidate, to be written T-A6.1)" parenthetical OR drop from §Memory entries (already listed in T-A6.1 slot). |
| I-cr-2 | proposal.md:191-203 + tasks T-A4 | Phase D archive runner duplicates `aria:phase-d-closer` D.2 + `aria:openspec-archive` Skills. Ownership unclear. | Add §A.7.1: "Script is phase-d-closer D.2 delegation target" (owner Q-lock confirmed). |
| I-cr-3 | proposal.md:134-135 + AC-5 line 380 vs Spec #3 §A.5 line 160 | G-6 URL contract ambiguous: Spec #3 §A.5 says URL posting is owner-action; RED on missing URL is EXPECTED v2.0.0 behavior, not exception. FAQ heading regex too strict. | Document RED-is-expected-v2.0.0; loosen regex to `^#+\s+.*Forgejo Discussion FAQ`. |
| I-cr-4 | proposal.md:30/144/388/452 + tasks function name | G-7 named "5-files" but actually verifies 6 surfaces (5 derived + main /VERSION). | Clarify: "5-files SoT + main /VERSION row (6 surfaces total)". |
| I-cr-5 | tasks.md:286 + OOS-7 | OOS-7 says "Forgejo Issue closure ... text-only recommendation" but §H archive runner Step 6 makes recommendation-only pattern asymmetric. | Extend §H Step 7 to emit Forgejo Issue closure recommendation symmetrically. |
| I-cr-6 | proposal.md:307 vs tasks.md:194 | Dry-run polarity opaque: proposal says `--dry-run` flag (default False?); tasks says default True with explicit `--execute` required. | Update proposal §H Step 4 to "dry-run is implicit default; `--execute` required to mutate". |
| I-cr-7 | proposal.md:11 + OOS-6 | TG-DOCS-B v2.0.1-deferrable alignment with Spec #3. ✅ Passing — no fix needed. | None. |

## Minor findings

| ID | Issue | Recommended fix |
|----|-------|----------------|
| N-cr-1 | A-1 verify command non-deterministic (`exits 0 OR exits 2`) | Use `--help 2>&1 \| grep -q -- '--all'` for falsifiability. |
| N-cr-2 | Effort SoT verified consistent across 4 places | None — passing audit. |
| N-cr-3 | AD-M6-10/11/12 allocation verified clean vs siblings | None — passing. |
| N-cr-4 | Phase A.1 closing note correct re audit collapse | None — passing. |
| N-cr-5 | REPO_ROOT canonical pattern matches Spec #1/#2 | (Note: C-ba-1/C-qa-1 challenge this — script depth differs from Spec #1) |
| N-cr-6 | §Constraints missing "Mock-shape discipline" | Add Constraint per `[[feedback_test_mock_pattern_hides_prod_bug]]`. |
| N-cr-7 | T-A4.3 escape hatch memory ref valid | None — passing. |
| N-cr-8 | Spec #1 commit ref `c29a800` verified | None — passing. |
| N-cr-9 | G-6 §A.5 line 160 cross-ref verified | None — passing. |
| N-cr-10 | Frontmatter parity missing `Audit trajectory` field | Add placeholder. |

## Q-escalations

| Q | Question |
|---|----------|
| Q-cr-1 | `--all` flag: invert primary path OR re-open sealed siblings for amendment? |
| Q-cr-2 | Spec #4 archive runner: phase-d-closer D.2 delegation target OR standalone bypass? |
| Q-cr-3 | Main `/VERSION` stale row pre-fix now OR T-A1 reconcile task OR risk-accept? |

---

**Audit trail**: `[[feedback_audit_driven_fix_conventions]]`
