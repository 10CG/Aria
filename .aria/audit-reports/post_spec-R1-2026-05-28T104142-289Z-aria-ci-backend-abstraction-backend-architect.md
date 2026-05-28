---
checkpoint: post_spec
mode: convergence
round: 1
agent: backend-architect
target: "openspec/changes/aria-ci-backend-abstraction/{proposal.md, tasks.md}"
change_id: aria-ci-backend-abstraction
timestamp: 2026-05-28T10:41:42Z
vote: PASS_WITH_WARNINGS
critical_count: 0
major_count: 3
minor_count: 4
---

# Post-Spec R1 Audit — aria-ci-backend-abstraction (backend-architect)

Spec read: `proposal.md` (560 lines) + `tasks.md` (196 lines).
Ground truth verified: `pre_merge_gate.py` (387 LOC, read in full).
DEC read: `.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md` (274 lines).
Prior R1 findings F-01 through F-05 from post_brainstorm audit all addressed in Spec — not re-raised here.

---

## §Findings

### MAJOR

---

**id**: `a3f8c2d1`
**severity**: Major
**category**: Contract correctness
**scope**: `proposal.md §B.4` / `pre_merge_gate.py:217-228` (existing `compute_verdict`)
**type**: Gap — function not defined, rename ambiguity
**summary**: `_compute_verdict(pr_status, in_flight, cfg)` — signature mismatch and undefined contract

**rationale**: The existing function in ground truth code is named `compute_verdict` (public, no underscore, L217) with signature `(main_in_flight_runs: list[dict], pr_ci_status: str) -> str`. It operates on raw list and raw string. The Spec's `gate_check()` pseudocode (§B.4) calls `_compute_verdict(pr_status, in_flight, cfg)` where `pr_status: CIStatus` and `in_flight: InFlightStatus` are dataclass instances, and a third argument `cfg` is added.

Three problems compound here:
1. The Spec never defines `_compute_verdict` — not in §A, §B, or the AC. There is no pseudocode body, no field access pattern, no indication of what `cfg` is used for (existing `compute_verdict` has no cfg argument at all).
2. The existing `compute_verdict` accesses `pr_ci_status` as a raw string (`"passing"`, `"failing"`, `"pending"`). After the refactor, the caller would pass `pr_status.state` (a `Literal` string from `CIStatus`). AC-5.4 states `pre_merge_gate.py` uses attribute access (`pr_status.state == "passing"`), but does `_compute_verdict` receive the dataclass and do `.state` access internally, or does it still receive a string (extracted by the caller before the call)? Both are valid designs but the Spec does not commit to either.
3. The `cfg` parameter is entirely new. The existing `compute_verdict` needs no config. The only config-dependent behavior in `gate_check()` appears to be `no_ci_fallback` (already dispatched before `_compute_verdict` is reached) and timeout values (dispatched earlier). There is no visible reason `_compute_verdict` needs `cfg`. Its presence without definition creates implementer ambiguity.

**recommended_action**: Add to proposal §B.4 (or as a separate §B.6):
- Explicit statement: "`compute_verdict` is renamed to `_compute_verdict` (private)" OR "existing `compute_verdict` is kept, `_compute_verdict` is a thin wrapper" — pick one.
- Signature locked as: `_compute_verdict(pr_status: CIStatus, in_flight: InFlightStatus) -> str` (no `cfg` — justification: all cfg-dependent branching already resolved before this call).
- One-line body sketch: `return compute_verdict([dict(r) for r in in_flight.runs], pr_status.state)` if reusing existing logic, OR inline the 4-line existing body and drop old `compute_verdict`.
- AC-5.4 should be strengthened: "all dict-key access on aether response objects is eliminated from `gate_check()` body; `_compute_verdict` receives typed dataclasses".

---

**id**: `b7e19f4a`
**severity**: Major
**category**: API design corner case
**scope**: `proposal.md §B.3` — `resolve_ci_backend()` empty-list vs missing distinction
**type**: Gap — spec distinguishes implicitly but AC does not test the boundary
**summary**: `ci_backends: []` (explicit disable) vs `ci_backends` missing (auto-detect) — behavior differs but AC has no test for the `[]` case

**rationale**: The Spec's `DEFAULT_CONFIG` sets `"ci_backends": []` (empty list). The `resolve_ci_backend()` pseudocode (§B.3) uses `explicit = config.get("ci_backends") or []` — this means BOTH `ci_backends: []` (explicit empty in user config) and `ci_backends` missing from user config (falls back to DEFAULT which is `[]`) produce `explicit = []`, and both take the auto-detect path. This is the correct behavior per Q3: "config-first + probe fallback". However:

1. The `or []` guard at `config.get("ci_backends") or []` means a user who explicitly writes `ci_backends: []` to **disable all backends** (as documented in AC-2.2's NIE message: "set ci_backends: [] in .aria/config.json to explicitly disable") is **not** actually disabling — they get auto-detect, which will probe Aether and GHA and potentially hit NIE. This is a contradiction between the NIE message text (which implies `[]` = disable) and the actual `resolve_ci_backend()` behavior (which implies `[]` = auto-detect).

2. The Spec does not define what "explicit disable" looks like. If `[]` means auto-detect (which the pseudocode implies), then the NIE message guidance is wrong. If `[]` means disable, the pseudocode needs a special-case check: `if config.get("ci_backends") is not None and config["ci_backends"] == []: return None`.

3. AC-4.2 says "config 显式 `ci_backends: [{name: "..."}]` 时按 config 顺序" but says nothing about `ci_backends: []` case. No test covers `TestBackendRegistry` with the explicit-empty-list case.

**recommended_action**: Pick one semantic and lock it:
- Option A (simpler): `ci_backends: []` = auto-detect (same as missing). Then fix the NIE message in `github_actions.py` to say "set ci_backends: [{name: 'aether-ci-cli'}] to pin to Aether only" rather than implying `[]` disables.
- Option B (matches NIE message): `ci_backends: []` = explicit disable (return None immediately). Pseudocode in §B.3 needs: `if config.get("ci_backends") is not None and not config["ci_backends"]: return None`.
Add AC-4.5: `test_explicit_empty_ci_backends_list_behavior` covering whichever semantic is chosen. Add to `TestBackendRegistry` in tasks.md T-tests 3.8.

---

**id**: `c1d6a8e3`
**severity**: Major
**category**: Estimate calibration
**scope**: `tasks.md T-refactor ~1h` — Aether logic migration completeness
**type**: Underestimate risk — subprocess + retry + in-flight flag verification non-trivial
**summary**: The 1h T-refactor estimate assumes trivial relocation of Aether logic, but `verify_aether_in_flight_flag()` + `_run_aether_with_retry()` + `_normalize_pr_ci_status()` + `_translate_in_flight_run()` require careful splitting between `aether.py` and `pre_merge_gate.py`

**rationale**: Reading the actual `pre_merge_gate.py` (387 LOC), the Aether-specific logic that must migrate to `aether.py` includes:
- `detect_aether()` (L57-68, 12 lines — straightforward)
- `verify_aether_in_flight_flag()` (L71-100, 30 lines — retry loop, subprocess, flag grep)
- `_run_aether_with_retry()` (L103-130, 28 lines — retry backoff loop, TimeoutExpired handling)
- `_query_aether()` (L133-157, 25 lines — subprocess call, JSON parse, error path)
- `_normalize_pr_ci_status()` (L160-185, 26 lines — sort-by-started_at logic)
- `_translate_in_flight_run()` (L188-214, 27 lines — ISO 8601 parsing, field mapping)
- `AETHER_CLI_MIN_SHA` + `AETHER_CLI_MIN_DATE` constants (L33-34)
- `RETRY_BACKOFF` + `MAX_RETRY_ATTEMPTS` constants (L37-38)

Total: ~150+ lines of logic to migrate into `AetherBackend`, plus the responsibility boundary question: does `_normalize_pr_ci_status()` return a raw string (staying in `pre_merge_gate.py`) or does `query_pr_ci()` return it already normalized into `CIStatus.state`? The Spec says "Preserves subprocess + retry + JSON parsing logic byte-for-byte" but does not say where `_normalize_pr_ci_status()` and `_translate_in_flight_run()` live post-refactor.

The AC-5.3 `InFlightStatus.runs: list[dict]` field implies `_translate_in_flight_run()` still runs (since runs are translated dicts, not raw aether objects), but this translation must happen either inside `AetherBackend.query_branch_in_flight()` or in `gate_check()` before building `InFlightStatus`. Neither path is specified.

At 1h this migration is tight but feasible if the developer is familiar with the code. The risk is mid-sprint decisions on `_normalize_pr_ci_status` / `_translate_in_flight_run` placement triggering scope creep into T-tests (the mock collapse in 3.2 depends on knowing whether these helpers are in `aether.py` or stay in `pre_merge_gate.py`).

**recommended_action**: Add to proposal §A.2 a responsibility table:

| Helper | Migrates to | Returns |
|--------|------------|---------|
| `detect_aether()` | `AetherBackend.probe()` classmethod | `bool` |
| `verify_aether_in_flight_flag()` | `AetherBackend.probe()` (absorbed) | (bool already) |
| `_run_aether_with_retry()` | `aether.py` private helper | unchanged |
| `_query_aether()` | `aether.py` private helper | unchanged |
| `_normalize_pr_ci_status()` | called inside `query_pr_ci()` | state string → `CIStatus.state` |
| `_translate_in_flight_run()` | called inside `query_branch_in_flight()` | dict → remains dict in `InFlightStatus.runs` |
| Constants `AETHER_CLI_MIN_*` | `aether.py` module level | — |
| Constants `RETRY_BACKOFF` / `MAX_RETRY_ATTEMPTS` | `aether.py` module level | — |

This table resolves the AC-5.4 dict-key vs attribute-access question at the boundary and eliminates mid-sprint decisions. Tasks.md T-refactor should reference this table (no estimate change needed — 1h is correct with this clarity).

---

### MINOR

---

**id**: `d4b2f7c9`
**severity**: Minor
**category**: Contract correctness
**scope**: `proposal.md §A.1` — `CIBackend` ABC member count inconsistency
**type**: Spec inconsistency — AC-5.1 lists 5 members but claims "4 abstract member"
**summary**: AC-5.1 states "4 abstract member" but then lists 5 items

**rationale**: AC-5.1 reads: "`CIBackend` ABC 仅含 4 个 abstract member: `name: ClassVar[str]` + `priority: ClassVar[int]` + `@classmethod probe(cls) -> bool` + `query_pr_ci(pr_ref) -> CIStatus` + `query_branch_in_flight(branch) -> InFlightStatus`". Counting: name + priority + probe + query_pr_ci + query_branch_in_flight = 5 items. The count "4" is wrong.

Additionally, `name` and `priority` are `ClassVar` attributes, not abstract methods — they are class variable declarations (no `@abstractmethod`). Python ABC does not enforce `ClassVar` annotations via `abstractmethod`; a subclass can omit `name` without triggering `TypeError`. If the Spec intends enforcement, the implementation must use `@property @abstractmethod` or a `__init_subclass__` check. The ground truth pseudocode in §A.1 uses `name: ClassVar[str]` without `@abstractmethod`, which is correct Python but does NOT enforce that subclasses define `name`.

**recommended_action**: Fix "4 abstract member" → "5 class members (2 ClassVar + 3 abstract methods)". Add a comment in `base.py` pseudocode noting that `name` and `priority` are unenforced ClassVar annotations by design (enforcement via `__init_subclass__` check is out of scope for this Spec). This prevents implementers from mistakenly trying to apply `@abstractmethod` to ClassVar fields.

---

**id**: `e5c3a1b8`
**severity**: Minor
**category**: Future extension friction
**scope**: `proposal.md §A.4` — `priority` field in `CIBackend` vs actual resolution logic
**type**: Dead field risk — `priority` ClassVar declared but never used by `resolve_ci_backend()`
**summary**: `priority: ClassVar[int]` on `CIBackend` is never consumed by `resolve_ci_backend()` — list order is the actual precedence, making `priority` misleading

**rationale**: The `resolve_ci_backend()` pseudocode (§B.3) iterates `BACKENDS` list (or user config list) in order and returns the first `probe()=True`. It never reads `backend_cls.priority`. The `__init__.py` `BACKENDS = [AetherBackend, GitHubActionsBackend]` list order is the actual precedence mechanism. The `priority` field on the ABC (100 for Aether, 50 for GHA per §A.3) is never consulted.

This is not a bug (list order works correctly), but it creates two problems:
1. A future 3rd backend implementer will set `priority` expecting it to affect probe order, and be surprised when it doesn't.
2. The field is documented in the class contract but not in `resolve_ci_backend()` docstring, creating a false expectation.

For adding a 3rd backend (e.g. GitLab CI), the actual steps are: subclass `CIBackend` + add to `BACKENDS` list at the desired position. `priority` has no operational role. The Spec's `resolve_ci_backend` docstring does not mention this, and neither does the proposed §C.2.4.X SKILL.md section.

**recommended_action**: Either (a) remove `priority: ClassVar[int]` from `CIBackend` ABC entirely (it adds no runtime value and creates false expectations), or (b) keep it as documentation-only and add an explicit comment in `base.py`: "# NOTE: priority is documentation-only; actual probe order is determined by BACKENDS list position in ci_backends/__init__.py". Also add to proposed §C.2.4.X SKILL.md "Adding a 3rd backend" instructions: "add to `BACKENDS` list at desired position; `priority` field is informational only".

---

**id**: `f6d9e2a7`
**severity**: Minor
**category**: Spec completeness — NIE propagation order
**scope**: `proposal.md §B.4` gate_check pseudocode
**type**: Semantic ordering question — confirmed correct but unattested
**summary**: `query_pr_ci` runs before `query_branch_in_flight` in §B.4; semantic correctness per Rule #8 order is (a) PR check THEN (b) branch check — this is correct but the Spec should attest it explicitly

**rationale**: The audit focus question asks whether NIE thrown from `backend.query_pr_ci(pr_ref)` aborts before `backend.query_branch_in_flight(branch)` runs. Reading §B.4 pseudocode:

```python
pr_status = backend.query_pr_ci(pr_ref)            # raises NIE → propagate
in_flight = backend.query_branch_in_flight(branch)  # raises NIE → propagate
```

The sequential order is: (a) PR CI check first, (b) in-flight check second. This matches Rule #8 ordering ("(a) 本 PR CI 已 passing; (b) main 分支无 in-flight CI run"). If `query_pr_ci` raises NIE, `query_branch_in_flight` never runs — the caller gets an abort exception, which is the correct Hard Constraint #7 behavior.

However, comparing to the current `gate_check()` implementation (L308-342 in `pre_merge_gate.py`), the **actual current order** is reversed: main in-flight query runs FIRST (L309: `_query_aether(binary, branch=main_branch, in_flight_only=True, ...)`), then PR CI query (L320). The Spec pseudocode reverses this order to (a) PR first, (b) main second.

This reversal is acceptable (both checks must pass; the order only matters for which error message surfaces first on failure), but it is an unannounced behavioral change from the current implementation. If the refactor silently changes query order, existing test assertions on error message content or call order may need updating.

**recommended_action**: Add a one-line comment in §B.4 pseudocode: "# Order: PR CI (a) first → in-flight (b) second — NOTE: reversal from pre-refactor which ran (b) first. Both must pass; order only affects first-error-wins diagnostic message." Add to tasks.md T-tests 3.2: "verify mock call order: `query_pr_ci` called before `query_branch_in_flight`" to make the reversal explicit and tested.

---

**id**: `g2a4d8f1`
**severity**: Minor
**category**: Probe cache isolation
**scope**: `proposal.md §C (tasks.md 3.11-3.12)` — lru_cache strategy
**type**: Incomplete spec — same-process multi-call scenario not addressed
**summary**: Option B (module-level `_probe_cache` dict) recommended in tasks.md 3.11 but the reset API (`reset_probe_cache()`) is not defined; also the same-process multi-gate-check scenario raised in audit focus is not mitigated

**rationale**: The audit focus raises: "Same process invokes `gate_check` for Spec #1 then Spec #2. Probe cached from first call. If env state changed (e.g. aether uninstalled between calls), wrong." The Spec acknowledges the lru_cache hazard in test isolation (tasks.md 3.11-3.12) but the proposed mitigation is test-teardown only — it does not address the production runtime scenario where multiple `gate_check()` calls in the same long-running process could use stale probe results.

For this Spec's scope (CLI invocation = one `gate_check` per process), cache staleness between calls is not a problem because each CLI run is a fresh process. However, the `gate_check()` function is also callable from Python (workflow-runner embedded calls), where multi-call in same process is real.

The module-level `_probe_cache` dict (Option B in tasks.md 3.11) is the right choice — it makes the cache explicit and resettable. But `reset_probe_cache()` is only mentioned in passing; its signature, export status, and whether it appears in `__init__.py`'s `__all__` is unspecified.

**recommended_action**: In proposal §C (or tasks.md 3.11), add: "Option B implementation: `_probe_cache: dict[type[CIBackend], bool] = {}` at module level in `ci_backends/__init__.py` + `def reset_probe_cache() -> None: _probe_cache.clear()`. Export `reset_probe_cache` in `__all__`. Callers (workflow-runner) that invoke `gate_check()` in a loop should call `reset_probe_cache()` between calls if env state may change. Not needed for CLI single-invocation mode." This is a minor clarification, not a design change.

---

## §Per-dimension verdict

**(a) Spec completeness — Implementation outline pseudocode actually compiles + runs?**

The pseudocode in §A.1 (base.py), §A.3 (github_actions.py), §A.4 (__init__.py), §B.1 (DEFAULT_CONFIG), §B.2 (_normalize_config), §B.3 (resolve_ci_backend), §B.4 (gate_check) is syntactically valid Python and would compile. The main gap is §B.4's call to `_compute_verdict(pr_status, in_flight, cfg)` — this function has no definition anywhere in the Spec (Major finding `a3f8c2d1`). The pseudocode would fail at runtime with `NameError: _compute_verdict` unless the implementer knows to keep/rename the existing `compute_verdict`. **Verdict: Mostly complete, one defined-but-undefined function (Major).**

**(b) Contract correctness — `CIBackend` ABC + `CIStatus` + `InFlightStatus` field sets sufficient and minimal?**

`CIStatus` dataclass (state + run_id + url + checked_at) is sufficient and minimal for the PR CI check use case. `InFlightStatus` (runs + checked_at + has_runs property) is sufficient. The `CIBackend` ABC has a minor count error ("4 abstract member" when there are 5, including ClassVars) — Minor finding `d4b2f7c9`. The `priority` ClassVar is present but unused by the resolution algorithm — Minor finding `e5c3a1b8`. Overall contract is sound. **Verdict: Sufficient; two minor precision gaps.**

**(c) Module boundary — `ci_backends/` package boundary clean?**

The package boundary (base.py + aether.py + github_actions.py + __init__.py) is clean. The `__init__.py` re-exports `CIBackend`, `CIStatus`, `InFlightStatus`, `AetherBackend`, `GitHubActionsBackend`, `BACKENDS` — sufficient for `pre_merge_gate.py`'s import in T-refactor 2.7. The `_normalize_pr_ci_status()` and `_translate_in_flight_run()` helpers need boundary assignment (stay in `pre_merge_gate.py` or migrate to `aether.py`) — addressed in Major finding `c1d6a8e3`. The boundary is clean structurally; responsibility table gap is the only issue. **Verdict: Clean boundary; one unresolved helper placement.**

**(d) Estimate calibration — T-backends 3h + T-refactor 1h adequate?**

T-backends 3h: Reading the full `pre_merge_gate.py`, the Aether logic to migrate is ~150 LOC (8 functions/helpers + 4 constants). At 3h this is achievable if the developer is familiar with the code. The `verify_aether_in_flight_flag()` function (L71-100) has retry logic that needs careful absorption into `probe()` or a separate helper — tight but feasible. **T-backends 3h: marginal but acceptable.**

T-refactor 1h: The refactor is genuinely small (replace DEFAULT_CONFIG + add _normalize_config + add resolve_ci_backend + replace gate_check body + rename _no_aether_output). The risk is mid-sprint decisions on helper placement (Major `c1d6a8e3`). With the responsibility table added to §A.2, 1h holds. **T-refactor 1h: acceptable if §A.2 table is added.**

**(e) API design corner cases — `ci_backends: []` vs missing?**

The `ci_backends: []` vs missing distinction is a genuine gap (Major finding `b7e19f4a`). The `or []` guard in `resolve_ci_backend()` collapses both to auto-detect, which contradicts the NIE message text that implies `[]` disables. No AC covers this boundary. Must be resolved before Phase B. **Verdict: Gap confirmed; needs resolution.**

**(f) Future extension friction — Adding a 3rd backend?**

Steps to add GitLab CI: subclass `CIBackend` in a new `gitlab.py` + add `GitLabCIBackend` to `BACKENDS` list in `__init__.py`. That is genuinely all that is needed — the Spec correctly keeps registry static and import-order-based. The `priority` field is a mild friction point (Minor `e5c3a1b8`) because future implementers will set it expecting it to matter. The proposed §C.2.4.X SKILL.md section should include "Adding a 3rd backend" steps. **Verdict: Low friction; one documentation clarification needed.**

---

## §Final vote

**Vote: PASS_WITH_WARNINGS**

**Justification**: The Spec is structurally sound and all 9 Hard Constraints from DEC + R1 brainstorm audit are properly encoded in ACs and implementation pseudocode. The three findings from the prior brainstorm audit that affected my domain (F-01 registry pattern, F-04 alias merge ordering, F-05 lru_cache isolation) are all correctly addressed. The pseudocode would compile and is implementable.

The three Major findings are genuine gaps that need resolution before Phase B:

1. `_compute_verdict` is called in §B.4 but never defined — implementer would need to infer the rename from `compute_verdict`. Easy fix: add one sentence to §B.4 specifying it as a rename + locked signature.

2. `ci_backends: []` semantic (explicit disable vs auto-detect) contradicts the NIE message text — requires a one-line design decision and one new AC test.

3. `_normalize_pr_ci_status()` / `_translate_in_flight_run()` placement in `aether.py` vs `pre_merge_gate.py` is unspecified — a responsibility table in §A.2 resolves this completely.

None of these require reopening brainstorm decisions (Q1-Q5 are unaffected). All three are fixable with targeted §A.2 and §B.4 additions. The Spec does not need a full redraft — targeted amendments suffice.

**Recommended path**: Fix three Majors (+ Minor `d4b2f7c9` count error) in proposal.md before Phase B start. Minor `e5c3a1b8` (priority field) + Minor `f6d9e2a7` (query order comment) + Minor `g2a4d8f1` (reset_probe_cache export) can be fixed in-flight during Phase B T-backends and T-tests without blocking start.
