---
checkpoint: post_spec
mode: convergence
round: 2
agent: qa-engineer
target: openspec/changes/aria-ci-backend-abstraction/{proposal.md, tasks.md}
change_id: aria-ci-backend-abstraction
timestamp: 2026-05-28T11:04:15Z
vote: PASS_WITH_WARNINGS
critical_count: 0
major_count: 0
minor_count: 2
addressed_count: 7
partial_count: 1
not_addressed_count: 0
---

## §R1 finding verification table

| ID | Severity | Summary | Status | Rev1 fix anchor | Quality |
|----|----------|---------|--------|-----------------|---------|
| d83fe5c1 | Major | Task 3.2 class names wrong; actual 5 classes 21 methods | ADDRESSED | tasks.md §Mock target collapse: 5 numbered tasks (3.1–3.5) matching ground-truth classes; "GateCheckTests (7 methods, NOT 15)"; "TestDetectAether" dropped | Substantive. Ground-truth class split correctly reproduced. Count/name errors eliminated. |
| 8cc465f0 | Major | AC-7.2 "≥27" gap — no `test_ci_backends.py` task | PARTIAL | tasks.md Task 1.7 creates `test_ci_backends.py` with ≥11 tests; Rev1 changelog: "21 rewritten + 16 new + 11 new = 48 total (well above AC-7.2 '≥27')" | Fix is real and the ≥27 threshold is technically met (16+11=27 exactly). Two residual issues keep this PARTIAL — see §New findings NF-1 and NF-2. |
| 30f23d6b | Major | Task 5.5 dogfood commands broken: `--pr` flag wrong, no `__init__.py` | ADDRESSED | tasks.md 5.5: `python3 aria/skills/phase-c-integrator/scripts/pre_merge_gate.py --pr-branch <test-branch>`; `cd /home/dev/Aria &&` prefix; sys.path.insert used correctly in python -c commands | Flag name and invocation path are now correct. All three 5.5 commands are runnable. See NF-3 for a residual gap in 5.6. |
| 6829b550 | Major | `_compute_verdict` undefined, 3-agent CONVERGED | ADDRESSED | proposal Hard Constraint #10; §B.4 signature `compute_verdict(main_in_flight_runs, pr_ci_status, backend_name, cfg)` locked; §A.2 responsibility table: `compute_verdict()` stays in `pre_merge_gate.py`; `backend_name` replaces hardcoded `"aether-ci-cli"` | Substantive. Public function name, full signature, and `primitive_used=backend.name` path are now all specified. Backward compat path (kwargs) also documented. |
| 3686dd32 | Minor | AC-5.1 count 4 vs 5 listed | ADDRESSED | proposal AC-5.1: "4 个 member 共 1 ClassVar + 3 abstract"; `priority` field dropped; base.py pseudocode updated to remove priority | Substantive. 1 ClassVar + 3 abstract = 4 members. Terminology now Python-accurate. |
| 90394899 | Minor | `priority` field dead design | ADDRESSED | proposal §B.4 comment "no priority field (Rev1, R1 ba F-06 + qa F-06: dropped unused priority)"; Hard Constraint #10 base.py pseudocode has no priority ClassVar; AC-5.1 drops it | Substantive. Dead field removed. BACKENDS list order = explicit precedence. Note: one residual reference `{name, priority?}` remains in §D.2 sketch (line 580); see NF-4. |
| 8d648072 | Minor | `gate_check` docstring stale "exceptions caught" | ADDRESSED | tasks.md Task 4.7: "Update `gate_check()` docstring — remove 'exceptions are caught' claim; add Hard Constraint #7 'NIE propagates' explicit doc"; proposal §B.4 gate_check pseudocode docstring already shows new contract text | Substantive. Both the task and the inline pseudocode docstring reflect the new NIE-propagation contract. |
| d85d1a9f | Minor | TestProbeCacheIsolation depends on Option A/B decision | ADDRESSED | proposal Hard Constraint #11: "Option B locked — module-level `_probe_cache` + `reset_probe_cache()` helper; **禁止** `@functools.lru_cache`"; tasks.md 3.12: "Rev1 Hard Constraint #11 Option B locked"; tasks.md 3.13+3.14 make implementation explicit | Substantive. Decision is locked, no ambiguity at test fixture design time. Dependency ordering enforced by Hard Constraint #11 existing before 3.12. |

## §New findings

### NF-1 (minor) — AC-7.2 body distribution table is stale post-Rev1

**Scope**: proposal.md AC-7.2 (line 212)

**Issue**: AC-7.2 still specifies the pre-Rev1 per-module breakdown: `ci_backends/base.py (5+) + aether.py (8+) + github_actions.py stub (3+) + registry (5+) + alias normalize (3+) + pre_merge_gate integration (3+)`. Rev1 reorganized test file ownership: `test_ci_backends.py` carries base.py(4) + aether.py(3) + github_actions(2) + registry(2) = 11, while `test_pre_merge_gate.py` carries GHA-abort(3) + alias(3) + both-keys(1) + backend-registry(5) + normalize-seq(2) + probe-cache(2) = 16. A future auditor verifying AC-7.2 against the old per-module breakdown would find `aether.py (8+)` mapped to only 3 tests in `test_ci_backends.py` and mark it a failure, even though total new tests = 27 which meets the threshold.

**Impact**: Low — threshold is met. Risk is audit confusion 3+ months out.

**Recommended action**: Replace the AC-7.2 distribution parenthetical with the Rev1-aligned split: `test_ci_backends.py (≥11: base.py contract 4 + aether.py migrated 3 + github_actions stub 2 + registry 2) + test_pre_merge_gate.py new classes (≥16: TestGHAStubAbortNotSkip 3 + TestAliasKeyPath 3 + TestBothKeysPresentNewWins 1 + TestBackendRegistry 5 + TestNormalizeConfigSequencing 2 + TestProbeCacheIsolation 2)`.

---

### NF-2 (minor) — Rev1 changelog "48 total (well above ≥27)" overstates the margin

**Scope**: proposal.md Rev1 changelog header line 16

**Issue**: The claim "21 rewritten + 16 in test_pre_merge_gate.py new + 11 in test_ci_backends.py new = 48 total (well above AC-7.2 '≥27')" conflates rewritten and new tests. The 21 rewritten tests are existing methods being updated with new mock targets, not net-new tests. Actual new tests = 16 + 11 = 27, which exactly meets the ≥27 threshold. "Well above" is incorrect; "exactly meets" is accurate.

**Impact**: Documentation accuracy only — the threshold is met. The risk is that a future executor, believing the margin is large, may not bother tracking the exact count and inadvertently drop one test class, falling below 27 without realizing it.

**Recommended action**: Correct changelog line to: "16 in test_pre_merge_gate.py new + 11 in test_ci_backends.py new = 27 new (exactly meets AC-7.2 ≥27); plus 21 existing tests rewritten (mock target collapse, not net-new)".

---

### NF-3 (minor) — Task 5.6 NIE abort verification command missing `cd` prefix

**Scope**: tasks.md Task 5.6 second bullet (line 104)

**Issue**: The "Manual NIE abort verification" command does not have `cd /home/dev/Aria &&` prefix, unlike the other commands in 5.5 and 5.6 which all start with `cd /home/dev/Aria &&`. The command uses `sys.path.insert(0, 'aria/skills/phase-c-integrator/scripts')` — a relative path — which requires `cwd=/home/dev/Aria` to resolve correctly. An executor copy-pasting this command from a different working directory will get a `ModuleNotFoundError`. Additionally, the command imports `from unittest.mock import patch` but never uses `patch` (monkey-patching is done by direct attribute assignment instead). The unused import is harmless but mildly confusing.

**Impact**: Low. The command still correctly demonstrates NIE abort behavior when run from the right directory. This is a copy-paste hazard, not a behavioral defect.

**Recommended action**: Prefix the NIE command with `cd /home/dev/Aria &&`. Optionally drop the unused `from unittest.mock import patch` import to keep the one-liner readable.

---

### NF-4 (trivial) — Stale `priority?` reference in §D.2 SKILL.md config schema sketch

**Scope**: proposal.md line 580

**Issue**: `§D.2` SKILL.md new section sketch includes "Config schema (`ci_backends: [{name, priority?}, ...]`)". `priority` was dropped by Rev1 (Hard Constraint #8 + F-06 fix). A SKILL.md author following this sketch would add a `priority?` config example that references a non-existent field.

**Impact**: Trivial — only affects the SKILL.md skeleton, which will be written fresh. The author will see Hard Constraint #8 and the dropped-priority note in AC-5.1 and is unlikely to include it. Noted for completeness.

**Recommended action**: Change line 580 to: `Config schema (`ci_backends: [{name: "..."}]`)` (drop `priority?`).

---

## §Final vote

**PASS_WITH_WARNINGS**

All 8 R1 findings are addressed. 7 are fully resolved with substantive fixes; 1 is PARTIAL (8cc465f0 / F-02) due to the stale AC-7.2 distribution table (NF-1) and overstated test-count margin (NF-2) — but the ≥27 threshold is met and the new `test_ci_backends.py` task exists.

The 4 new findings (NF-1 through NF-4) are all minor or trivial documentation accuracy issues. None introduce safety holes, behavioral ambiguity in Hard Constraints, or AC verifiability gaps that would cause Phase B to fail. NF-1 and NF-2 are the most consequential because they could mislead a future post_implementation auditor trying to verify AC-7.2 — but both are fixable with a single sentence edit each.

The Spec is safe to proceed to Phase B implementation without another revision round. The NF-1/NF-2/NF-3/NF-4 corrections can either be applied as a quick patch before Phase B starts, or noted as implementation-time clarifications. They do not require re-audit.

**Key assurances confirmed in R2**:
- Hard Constraint #10 (`compute_verdict` signature) is precisely defined and locked
- Hard Constraint #11 (Option B probe cache) is locked with explicit implementation path
- Task 1.7 (`test_ci_backends.py`) exists and has ≥11 test case breakdown
- Dogfood commands in Task 5.5 are runnable from `cwd=/home/dev/Aria` with correct `--pr-branch` flag
- `priority` ClassVar is consistently removed from base.py pseudocode, AC-5.1, and Hard Constraint prose
- `gate_check` NIE-propagation contract is documented in both Task 4.7 and §B.4 pseudocode docstring
