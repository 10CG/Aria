---
checkpoint: post_spec
mode: convergence
round: 2
agent: backend-architect
target: "openspec/changes/aria-ci-backend-abstraction/{proposal.md, tasks.md}"
change_id: aria-ci-backend-abstraction
timestamp: 2026-05-28T11:02:20Z
vote: PASS_WITH_WARNINGS
critical_count: 0
major_count: 0
minor_count: 1
addressed_count: 6
partial_count: 1
not_addressed_count: 0
---

# Post-Spec R2 Audit — aria-ci-backend-abstraction (backend-architect)

Spec read: `proposal.md` (660 lines, Rev1) + `tasks.md` (206 lines, Rev1).
Ground truth re-verified: `pre_merge_gate.py` L295-350 (query order).
R1 report cross-referenced: `post_spec-R1-2026-05-28T104142-289Z-aria-ci-backend-abstraction-backend-architect.md`.

---

## §R1 Finding Verification Table

| # | R1 id | Severity | Summary | Status | Rev1 fix anchor | Quality |
|---|-------|----------|---------|--------|-----------------|---------|
| 1 | `a3f8c2d1` | Major | `_compute_verdict` undefined, signature mismatch | ADDRESSED | Hard Constraint #10 + §B.4 `compute_verdict()` signature block | Adequate — public name locked, 4-param signature specified with return type `dict`, backward compat kwarg path noted. `cfg: dict | None = None` justified in docstring. No new issues. |
| 2 | `b7e19f4a` | Major | `ci_backends: []` vs missing collapse contradiction | ADDRESSED | AC-4.5 + §B.3 `resolve_ci_backend()` docstring + pseudocode `if explicit is not None:` / `if not explicit: return None` | Adequate — `config.get("ci_backends") is not None` guard correctly distinguishes `[]` (disable) from absent (auto-detect). The R1 `or []` bug is gone. AC-4.5 adds two named tests. No new issues. |
| 3 | `c1d6a8e3` | Major | §A.2 "byte-for-byte" but no responsibility table | ADDRESSED | §A.2 9-row migration table covering 8 functions + 4 constants | Adequate — table covers all symbols identified in R1 finding. Returns column clarifies `_normalize_pr_ci_status()` → stays in `query_pr_ci()` returning `CIStatus.state`. Implementer ambiguity eliminated. |
| 4 | `d4b2f7c9` | Minor | AC-5.1 "4 abstract members" counts 5 | ADDRESSED | AC-5.1 Rev1 rewrite: "4 个 member 共 1 ClassVar + 3 abstract" + `priority` dropped | Adequate — count is now correct (1 ClassVar + 3 abstract = 4 total). `priority` dropped per converged F-06. The ABC pseudocode in §A.1 no longer includes `priority`. No new issues. |
| 5 | `e5c3a1b8` | Minor | `priority` field dead design — never consumed by resolver | ADDRESSED | AC-5.1 Rev1 + §A.1 `CIBackend` docstring "no priority field (Rev1, R1 ba F-06 + qa F-06: dropped unused priority)" | Adequate — field removed entirely from ABC and all pseudocode. Hard Constraint #8 + AC-4.1 lock the BACKENDS list-order semantics. No residual `priority` found in Spec. |
| 6 | `f6d9e2a7` | Minor | §B.4 silently reverses query order (in-flight first in ground truth, PR first in pseudocode) | PARTIAL | §B.4 comment added: "Query order: PR-first then in-flight (Rule #8 (a) before (b), matches ground truth gate_check L298-300 — preserved by Rev1)" | **Paper-fix introduced a factual error.** See §New Findings #N-1 below. |
| 7 | `g2a4d8f1` | Minor | `reset_probe_cache()` signature undefined, export unspecified | ADDRESSED | Hard Constraint #11: `reset_probe_cache() -> None` + `_probe_cache.clear()` + export from `ci_backends/__init__.py`; Task 3.12 + 3.13 lock Option B | Adequate — signature is `() -> None`, idempotent `clear()` body, exported. `__all__` inclusion confirmed by §A.4 pseudocode. Workflow-runner multi-call scenario noted in HC #11. |

---

## §New Findings

### N-1 — Minor: §B.4 query-order annotation is factually wrong (paper-fix introducing new error)

**severity**: Minor
**category**: Spec accuracy — annotation references wrong line and makes false preservation claim
**scope**: `proposal.md §B.4` comment block

**rationale**: The R1 finding `f6d9e2a7` asked for an explicit annotation acknowledging the reversal from ground truth (in-flight first → PR first). The Rev1 annotation reads:

```
# Query order: PR-first then in-flight (Rule #8 (a) before (b), matches
# ground truth gate_check L298-300 — preserved by Rev1)
```

Ground truth verification (re-read `pre_merge_gate.py` L295-350 for this R2):

- L309: `main_ok, main_data, main_err = _query_aether(... in_flight_only=True ...)` — **in-flight (b) runs FIRST**
- L320: `pr_ok, pr_data, pr_err = _query_aether(... in_flight_only=False ...)` — **PR CI (a) runs SECOND**

The annotation's claim "matches ground truth gate_check L298-300 — preserved by Rev1" is doubly wrong:
1. L298-300 in the ground truth is the `verify_aether_in_flight_flag` failure return block — it is not the query-order locus. The actual query order is at L309 vs L320.
2. The pseudocode order (PR first, in-flight second) is a **reversal** from ground truth, not a preservation.

The R1 recommended action was to say "NOTE: reversal from pre-refactor which ran (b) first." The Rev1 annotation instead claims preservation, which is the opposite of what the finding requested and introduces a new factual inaccuracy that implementers reading the Spec will trust.

**impact assessment**: Low severity because:
- The reversal itself is acceptable (R1 `f6d9e2a7` called it "acceptable" — "order only affects which error message surfaces first on failure")
- Tasks.md T-tests 3.3 still needs to verify mock call order per R1's recommendation — this was NOT added to tasks.md (the task says "collapse 3 stacked mocks to 2 mocks" but does not include the R1-recommended "verify mock call order" assertion)

**recommended_action**: Two-word fix in §B.4 annotation: replace "matches ground truth gate_check L298-300 — preserved by Rev1" with "reversal from pre-refactor which ran (b) first (L309 ground truth); both checks must pass, order only affects first-error-wins diagnostic". Additionally add to tasks.md T-tests 3.3 one assertion: "verify `query_pr_ci` called before `query_branch_in_flight` in mock call order". This is a one-line change in both files. Does not block Phase B start — fixable in-flight.

---

## §Final Vote

**Vote: PASS_WITH_WARNINGS**

**Justification**: Six of seven R1 findings are fully addressed with adequate fixes. The three Majors — `_compute_verdict` undefined contract (`a3f8c2d1`), `ci_backends: []` semantic ambiguity (`b7e19f4a`), and missing responsibility table (`c1d6a8e3`) — are all correctly and sufficiently resolved in Rev1. Hard Constraints #10 and #11 lock the two most contentious R1 agreements (3-agent CONVERGED `compute_verdict` signature + probe cache Option B). AC-4.5 cleanly resolves the `[]` vs missing distinction.

The single PARTIAL finding (`f6d9e2a7`) is a minor annotation error: the Rev1 comment claims the query order "matches ground truth" when it is actually a reversal. The error is cosmetic (the reversal itself was pre-approved as acceptable in R1) but it introduces a false statement into the Spec that implementers may trust. The fix is a one-sentence annotation correction and a one-line task addition — no design change required.

**Phase B gating assessment**: The Spec is implementable as-written. The annotation error in §B.4 does not block Phase B start; it can be corrected in-flight during T-refactor with zero impact on Phase B estimate. No design decisions need to be reopened.

**Convergence status**: R1 had 3 Major + 4 Minor. R2 has 0 Major + 0 Minor new substantive findings + 1 paper-fix annotation error (Minor). This is consistent with the convergence target of R2 unanimous PASS_WITH_WARNINGS. Agent withdrawal on new substantive findings is warranted — the Spec is sound.
