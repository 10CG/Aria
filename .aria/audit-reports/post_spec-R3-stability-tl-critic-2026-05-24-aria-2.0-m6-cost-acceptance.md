# Post_Spec R3 Stability Check — tech-lead-critic — aria-2.0-m6-cost-acceptance

> **Auditor**: tech-lead-critic
> **Round**: R3 stability (Phase A.2 post_spec) — scope-limited to R2 fixes
> **Spec status**: Draft post-R2-fix (commit `75a399d`)
> **DEC reference**: DEC-20260524-001
> **Vote**: **R3_STABLE**

---

## Summary

R2-fix cycle (commit `0d4a317` → `75a399d`, +48/-8 across proposal.md + tasks.md) closed all three R2 findings without introducing regression: C-tl-N1 REPO_ROOT 3-level → 2-level chain (3 surfaces all byte-for-byte mirroring `validate-m5-handoff.py:40-41`), R2CH-cr-I1 effort baseline drift unified to `~12h impl` SoT across 4 surfaces with `~13h` weasel removed, R2CH-ai-NI-1 AC-2b orphan-NULL check added between AC-2 and AC-3 with T4.7/T4.8 appended cleanly (no downstream renumbering collision). Convergence trajectory R1 (11C+20I aggregate) → R2 (1C+2I) → R3 (0C+0I) — 100% Critical closure on R2 fixes verified. Spec #1 ready for Phase A.3 → Approved status flip → Phase B.1 entry.

---

## R2 fix verification matrix

| R2 ID | Closure | Evidence | Note |
|-------|---------|----------|------|
| **C-tl-N1 (REPO_ROOT 2-level)** | **CLOSED** | proposal:232 (fix-trace) + 235-237 (code block, `.resolve().parent` then `HERE.parent`, anchor comment `→ aria-orchestrator/` explicit); tasks:32-34 (T1.1 inline) + 199-202 (T5.1 inline) — all 3 surfaces byte-for-byte mirror sibling | Sibling `validate-m5-handoff.py:40` = `HERE = Path(__file__).resolve().parent`; line 41 = `REPO_ROOT = HERE.parent  # aria-orchestrator/`. Spec text matches verbatim (modulo whitespace). `.resolve()` present — NOT the partial-fix pitfall this auditor explicitly flagged. Anti-paper-fix discipline honored. |
| **R2CH-cr-I1 (effort SoT ~12h)** | **CLOSED** | proposal:10 (frontmatter, `~12h impl` + explicit "review overhead ~1h tracked separately"); proposal:63 (§What in-scope heading `~12h impl`); proposal:632-647 (§Effort baseline body: arithmetic 11.5h ≈ 12h, "single SoT; cited identically in frontmatter line 10 + tasks.md line 7 + this section"); tasks:7 (`~12h`). Grep `~13h` confirms only 1 match — the removal-trace comment line 649. Inline R2-cr-I1 trace at 2 surfaces (line 10 + line 649). | The `~1h review overhead` separation closes the SoT drift cleanly. Math reconciles: 38 leaf tasks × ~18min = 11.4h ≈ 12h. |
| **R2CH-ai-NI-1 (orphan NULL provider_cost_model)** | **CLOSED** | proposal:465-482 (new AC-2b section between AC-2 line 447 and AC-3 line 484; AC numbering integrity verified — AC-3..AC-9 unchanged); proposal:475-480 (binary-falsifiable SQL evidence: `SELECT COUNT(*) FROM dispatches WHERE provider_cost_model IS NULL` MUST return 0, non-zero → exit 1); tasks:184-189 (T4.7 impl + T4.8 unit test). Inline R2-ai-NI-1 trace at 3 surfaces. | AC-2b is structurally correct: distinct ID (not collision with AC-2), placed at logical position (data-integrity precondition before AC-3 Luxeno semantics), exit-code aligned with AD-M6-3 contract (exit 1 = AC data failure, not exit 2 infra). T4.7 SQL adds `GROUP_CONCAT(dispatch_id)` for owner triage — value-add beyond bare COUNT. |

---

## New findings (R3-introduced; should be 0 for R3_STABLE)

### Critical

*(none — R3 stable)*

### Important

*(none — R3 stable)*

### Trivial / observational (informational only, NOT blocking)

- **O-R3-1**: T4.7's evidence uses `[FAIL: AC-2b]` with colon-inside-brackets, while AC-1..AC-9 elsewhere uses `[FAIL] AC-N:` colon-outside-brackets. Cosmetic format inconsistency; acceptance script implementer will trivially normalize. Defer to Phase D.3 polish or close as ignorable. NOT a regression.
- **O-R3-2**: The new AC-2b verification query (proposal:475-480) and T4.7 SQL (tasks:185-187) are semantically identical but visually different (T4.7 adds `GROUP_CONCAT(dispatch_id)`). Implementer must use T4.7's enriched form. Trivial; surface-level note only.

Neither observation rises to Important. R3_STABLE verdict unaffected.

---

## Cross-fix interaction stability check

Three R2 fixes touched independent Spec regions (§What F + tasks T1.1/T5.1 path resolution; frontmatter + §Effort baseline word change; new AC-2b section + new T4.7/T4.8 tasks). No surface overlaps; no possibility of one fix invalidating another. Verified via diff stats: proposal.md +40/-8 lines, tasks.md +16/-2 lines — totaling 48 inserts across 6 distinct sections that don't reference each other's content beyond the matrix above.

AC numbering integrity check: `grep ^### AC-` shows AC-1, AC-2, AC-2b, AC-3, AC-4, AC-5, AC-5b, AC-6, AC-7, AC-8, AC-9 — clean sequence with `b`-suffix subordinate IDs (AC-2b under AC-2, AC-5b under AC-5 from R1). No accidental AC-3 → AC-4 renumber. T4 task sequence (T4.1..T4.8) clean with R1-I-2 fixes preserved at T4.5/T4.6 and R2-NI-1 fixes appended at T4.7/T4.8.

Inline-trace audit: All 6 R2 fix comments (`R2-C-tl-N1` ×3 surfaces, `R2-cr-I1` ×2 surfaces, `R2-ai-NI-1` ×3 surfaces) present and content-accurate per `[[feedback_audit_driven_fix_conventions]]`. No contradiction between trace text and actual content change.

---

## Convergence trajectory

- R1: 32 findings aggregate across 4 agents (11C + 20I + 16m + 17o); my R1: 3C + 5I + 4m + 5o — NEEDS_FIX 4/4 unanimous
- R1-fix (`0d4a317`): 100% C/I addressed per R2 verification 4/4 agents
- R2: 3 findings (1 NEW C self-spotted: C-tl-N1 REPO_ROOT off-by-1; 2 I: R2CH-cr-I1 + R2CH-ai-NI-1) — SCOPE_OK_R2 conditional 3/3 agents
- R2-fix (`75a399d`): 3/3 R2 findings CLOSED (this verification)
- **R3 stability: R3_STABLE — 0 new C + 0 new I introduced by R2-fix cycle**

R1 → R2 Critical reduction: 11 → 1 (91%, satisfies `[[feedback_premerge_iteration_pattern]]` ≥70% threshold).
R2 → R3 Critical reduction: 1 → 0 (100%, terminal convergence).
Per `[[feedback_premerge_iteration_pattern]]` "首个 0-finding 轮不能直接声称收敛" — R2 was 1-Critical-finding round, R3 is the mandatory first-zero-finding stability round. R3 verifies stability achieved.

---

## Vote rationale

**R3_STABLE — Spec #1 ready for Phase A.3 → Approved status flip → Phase B.1 entry.**

All three R2 fixes verified CLOSED with surface-by-surface evidence:

1. **C-tl-N1 byte-for-byte match**: Spec writes `HERE = Path(__file__).resolve().parent; REPO_ROOT = HERE.parent` at 3 surfaces (proposal §What F code block + tasks T1.1 + tasks T5.1). `.resolve()` is present (not the partial-fix omission this auditor explicitly flagged as the anti-paper-fix discipline trigger). Sibling `validate-m5-handoff.py:40-41` matches verbatim modulo whitespace. Anchor comments `→ aria-orchestrator/` make the resolved-path explicit, preventing future regression. `grep parent\.parent\.parent` confirms remnants exist only in 3 explicit removal-trace comments ("NOT .parent.parent.parent") — zero actual code references the 3-level chain.

2. **R2CH-cr-I1 SoT discipline**: `~12h impl` appears identically at 4 surfaces (frontmatter L10 + §What L63 + §Effort baseline body L645 + tasks L7). The `~1h review overhead tracked separately` framing closes the original drift cleanly without inventing a 4th synthesis number. `~13h` survives only in 1 explicit removal-trace comment. Math reconciles (38 leaves × 18min = 11.4h).

3. **R2CH-ai-NI-1 binary-falsifiable AC-2b**: New AC section structurally clean (between AC-2 and AC-3, no downstream renumbering, distinct `b`-suffix subordinate ID). SQL evidence `WHERE provider_cost_model IS NULL` returning 0 is binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`. T4.7 implementation task adds `GROUP_CONCAT(dispatch_id)` for owner triage (exceeds spec floor). T4.8 unit test covers both positive (1 NULL row → exit 1) and negative (0 NULL → PASS) cases.

No new Critical or Important findings introduced. Two cosmetic observations (O-R3-1 `[FAIL: AC-X]` bracket-colon vs `[FAIL] AC-X:` format inconsistency, O-R3-2 T4.7 SQL enrichment) are not regressions — they are pre-existing trivial polish items deferrable to Phase D.3.

**Recommendation**: Proceed to Phase A.3. State flip Spec #1 `Draft` → `Approved`. Assign backend-architect for T-schema / T-config / T-alarm / T-acceptance / T-validate / T-docs / T-prd (single-agent Spec per DEC §6, ~12h baseline implementation budget, AI compounding factor ×0.5-0.7 → ~6-9h actualized per `[[feedback_phase_budget_compounding]]`).

Phase B.1 branch creation may begin immediately upon owner Approved-status confirmation.

---

## Memory refs cited

- `[[feedback_premerge_iteration_pattern]]` — first-zero-finding stability round mandatory after R2 surfaced 1 new C; R3 satisfies this discipline (0C+0I confirmed terminal convergence)
- `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` — owner-invoked R3 stability check (not full re-audit) executed as scope-limited 3-fix verification, completed in time budget (~7min vs ~5-8min target)
- `[[feedback_paper_fix_antipattern]]` — explicitly verified `.resolve()` present in C-tl-N1 fix (the partial-fix pitfall this auditor pre-flagged)
- `[[feedback_audit_driven_fix_conventions]]` — all 8 R2 inline trace comments verified accurate and traceable
- `[[feedback_spec_v2_body_propagation_2pass]]` — C-tl-N1 propagated to 3 surfaces with consistency; R2CH-cr-I1 propagated to 4 surfaces with consistency
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — AC-2b binary-falsifiable SQL evidence verified
- `[[feedback_phase_budget_compounding]]` — ~12h baseline math reconciles (38 × 18min = 11.4h ≈ 12h)
