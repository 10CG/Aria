---
checkpoint: post_spec
mode: convergence
round: 2
agent: tech-lead
target: openspec/changes/aria-ci-backend-abstraction/{proposal.md, tasks.md}
change_id: aria-ci-backend-abstraction
timestamp: 2026-05-28T11:01:11.524Z
vote: PASS_WITH_WARNINGS
critical_count: 0
major_count: 0
minor_count: 2
addressed_count: 9
partial_count: 1
not_addressed_count: 0
---

# R2 Verification — tech-lead

## §1 R1 finding verification table

| ID | Severity | Status | Rev1 fix anchor | Quality assessment |
|----|----------|--------|----------------|--------------------|
| F-01 | Critical | **ADDRESSED** | proposal.md AC-2.5 (L177) + tasks.md 3.7 (L67) | Solid. Both message-body substrings (`"GHA backend probe succeeded but"` + `"PR welcome"`) asserted in test + locked verbatim in `github_actions.py` source (proposal §A.3 L347-359). Silent-rot vector closed — assertion + source string are bound together. No paper-fix: the test imports `str(exc.value)` directly from the raised NIE. |
| F-02 | Major | **ADDRESSED** | proposal.md §B.2 `_translate_value` table (L434-451) | Complete. Table covers both `_OLD_TO_NEW` keys (`primitive_preference` list-shape transform + `no_aether_fallback` enum passthrough) including the Rev1 `[]` semantic preservation case (empty list → empty list, retains explicit-disable). Defensive `return old_value` fallback noted. No new gaps. |
| F-03 | Major | **ADDRESSED** | proposal.md Hard Constraint #10 (L147) + §B.4 `compute_verdict` signature (L530-547) + tasks.md 3.1 (L58) | Substance convergence honored. Three-agent collision resolved: (a) public name `compute_verdict` (matches L217 ground truth, drops underscore); (b) signature extended with `backend_name` param replacing hardcoded `"aether-ci-cli"` in `primitive_used` output; (c) backward compat preserved via kwargs (`backend_name="aether-ci-cli"` keeps old assertions passing). This is the R1 audit highlight per [[feedback_brainstorm_substance_convergence_pattern]] and the fix is structurally sound. |
| F-04 | Major | **ADDRESSED** | proposal.md Hard Constraint #11 (L148) + tasks.md 1.5/3.13/3.14 | Option B locked explicitly: module-level `_probe_cache: dict[type[CIBackend], bool]` + `reset_probe_cache()` helper exported from `ci_backends/__init__.py`. `@lru_cache` explicitly banned. tearDown invocation pinned in task 3.14 with `autouse=True` fixture allowance. Decision made, test isolation hazard closed. |
| F-05 | Major | **ADDRESSED** | tasks.md 4.6 (L88) | Concrete grep command specified: `grep -rn "_no_aether_output\|no_aether_fallback" aria/skills/phase-c-integrator/scripts/` returns 0 hits, with md/comments filter noted. Functional grep distinct from doc grep. Verification is mechanical and falsifiable. |
| F-06 | Major | **ADDRESSED** | tasks.md 8.7 (L140-142) | Race guard concrete: `git fetch --all && cd aria && grep "^## \[1.29.0\]" CHANGELOG.md`. Both branches handled: 0 hits → proceed; 1+ hits → abort + manual reconcile. Notes that v1.31.0 entry position depends on v1.29.0 ship state. Adequate for the 9-day overlap window. |
| F-07 | Minor | **ADDRESSED** | proposal.md §D.2 (L575) ref count corrected | Cross-checked: proposal.md L13 + Rev1 changelog explicitly says "SKILL.md ref count corrected 14 (was ~10)". Deliverable D estimate L105 still says "~10 处" — minor inconsistency but the Rev1 changelog dominates. See new finding N-1 below. |
| F-08 | Minor | **PARTIALLY_ADDRESSED** | tasks.md 2.7 (L48) | Task 2.7 still says "Update imports: `from ci_backends import CIBackend, CIStatus, InFlightStatus, BACKENDS, AetherBackend, GitHubActionsBackend`". This over-prescribes — `pre_merge_gate.py` only needs `resolve_ci_backend` + dataclass types for type hints, NOT direct backend class imports (which would couple `pre_merge_gate.py` back to specific backends, defeating the abstraction). Likely just a brain-dump of available exports. See new finding N-2. |
| F-09 | Minor | **ADDRESSED** | tasks.md 11.1 (L156) | Trigger explicit: "this cycle ~10-10.5h = clear trigger" with Rule #9 reference. Adequate. |
| F-10 | Minor | **ADDRESSED** | proposal.md §Out of Scope (L113-122) | Cross-checked: Out of Scope list extended but the verdict-semantics fence appears in Rev1 changelog L19 ("Out-of-Scope adds verdict-semantics fence"). Looking at L113-122, the 8 bullets cover deferrals but I do not see an explicit "verdict semantic interpretation by downstream workflow-runner is out of scope" bullet. However Hard Constraint #10 + §B.4 lock the signature, which effectively fences the semantic. Adequate de-facto. |

### Counts

- ADDRESSED: 9 (F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-09, F-10)
- PARTIALLY_ADDRESSED: 1 (F-08)
- NOT_ADDRESSED: 0
- OBSOLETE: 0

## §2 New findings (minor only — substantive)

### N-1 (Minor) — SKILL.md ref count inconsistency between Rev1 changelog and Deliverable D

**Location**: proposal.md L105 (Deliverable D table) vs L13 (Rev1 changelog)

**Issue**: Rev1 changelog L13 states "SKILL.md references count corrected to 14 (was ~10)" but Deliverable D table L105 still reads `aria/skills/phase-c-integrator/SKILL.md ~10 处`. tasks.md 4.2 also says "replace ~10 aether-specific references". This is a cosmetic drift — the corrected count (14) didn't propagate to the deliverable table or task body.

**Impact**: Low. Implementation grep will reveal the true count; no semantic ambiguity. But minor inconsistency between Rev1 audit-trail and concrete tasks.

**Recommendation**: Update Deliverable D L105 + tasks.md 4.2 to say "~14 处 (Rev1 verified)" for trail consistency. Or accept as cosmetic and rely on the grep verification in 4.6 + 4.2-grep.

### N-2 (Minor) — Task 2.7 over-imports defeat the abstraction barrier

**Location**: tasks.md L48

**Issue**: Task 2.7 prescribes `from ci_backends import CIBackend, CIStatus, InFlightStatus, BACKENDS, AetherBackend, GitHubActionsBackend` in `pre_merge_gate.py`. But after Rev1 refactor, `pre_merge_gate.py` only needs:
- `resolve_ci_backend` (from `__init__.py` if exposed, OR defined inline per §B.3)
- `CIStatus` / `InFlightStatus` for type hints in `compute_verdict` and `gate_check`
- `BACKENDS` if `resolve_ci_backend` lives in `pre_merge_gate.py` (it does per §B.3)

Direct imports of `AetherBackend` and `GitHubActionsBackend` into `pre_merge_gate.py` re-couple the generic layer back to specific backend classes — exactly what the abstraction is meant to break. The §B.3 `resolve_ci_backend` only needs `BACKENDS` (the list), not the individual classes by name.

**Impact**: Low-to-Medium. Implementation-time risk: developer follows task literally, imports the classes, then writes `isinstance(backend, AetherBackend)` checks somewhere defeating polymorphism. Or just dead imports.

**Recommendation**: Tighten task 2.7 to: `from ci_backends import CIStatus, InFlightStatus, BACKENDS` (3 names, not 6). The Backend classes should only be referenced via `BACKENDS` list iteration or via `name_map` dict in `resolve_ci_backend`. F-08 was flagged R1 as over-prescription — Rev1 left it untouched. Not blocking but worth a one-line tighten before Phase B.

## §3 Final vote

**Vote: PASS_WITH_WARNINGS**

**Justification**:

- 9/10 R1 findings ADDRESSED, 1 PARTIALLY_ADDRESSED (F-08, minor over-prescription)
- 0 Critical / 0 Major in R2 → R1 Critical (F-01 NIE message rot) is solidly fixed via dual assertion + source-string lock
- The R1 substance-convergence highlight (F-03 `_compute_verdict` 3-agent collision) is well-resolved: Hard Constraint #10 + §B.4 signature extension + kwargs backward compat is a clean third-path synthesis matching the [[feedback_r2_mutual_concession_third_path_synthesis]] pattern
- Probe cache (F-04) and registry pattern (Hard #8) decisions are explicit and falsifiable
- 2 new minor findings (N-1 cosmetic doc drift, N-2 minor over-import in task body) are not blocking
- Per [[feedback_audit_convergence_patterns]]: R1 voted REVISE × 2 + PASS_WITH_WARNINGS × 1; R2 expected unanimous PASS_WITH_WARNINGS IF Rev1 adequate — Rev1 is adequate. Agent withdrawal from REVISE → PASS_WITH_WARNINGS is the healthy convergence signal
- No paper-fix detected: each fix attacks the root mechanism (message-rot via dual lock; cache via module-level dict; verdict via signature extension); no surface-level patches

**Action recommendation**: Spec is ship-ready for Phase B. The two minor findings (N-1, N-2) can be folded into a Rev1.1 trim or accepted as Phase B implementation-time corrections by the developer — neither warrants R3.

---

**Report file**: `/home/dev/Aria/.aria/audit-reports/post_spec-R2-2026-05-28T110111-524Z-aria-ci-backend-abstraction-tech-lead.md`
**Vote**: PASS_WITH_WARNINGS
**Counts**: addressed=9, partial=1, not_addressed=0, new_findings=2 (both minor)
