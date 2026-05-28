---
checkpoint: post_brainstorm
mode: convergence
round: 1
agent: backend-architect
target: .aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md
change_id: aria-ci-backend-abstraction
change_id_status: prospective (brainstorm phase)
timestamp: 2026-05-28T08:03:58Z
vote: PASS_WITH_WARNINGS
critical_count: 0
major_count: 2
minor_count: 3
---

## §Findings

### F-01
- **id**: `a3f7c112`
- **severity**: Major
- **category**: contract-design
- **scope**: `ci_backends/base.py` (prospective) — `CIBackend` ABC + `resolve_ci_backend()`
- **type**: Design gap — registry discovery mechanism unspecified
- **summary**: DEC selects Q3 "config-first + probe fallback" but never specifies *how* `resolve_ci_backend(config)` discovers and instantiates backend classes. Static import list? Decorator registry? The discovery mechanism is load-bearing for the `ci_backends/__init__.py` deliverable (Item A) but is absent from the DEC.
- **rationale**: The boundary-audit sketch (§修复 2) showed a `ci_backends` list in `DEFAULT_CONFIG` with `name` / `bin_name` / `priority` fields, which implies a config-driven registry loop. The DEC's deliverables table says `__init__.py` holds "registry" but does not name the pattern. This leaves the Phase B implementer with a critical design decision to make mid-sprint: static import list (simple, rigid), decorator `@registry.register("aether-ci-cli")` (extensible, no dynamic import needed), or entry-points (external-package scale, overkill here). Wrong choice introduces coupling or dead flexibility.
- **recommended_action**: Add one paragraph to the DEC's §收敛 design 整体逻辑 (or a new §Registry pattern note) specifying the chosen discovery mechanism before Phase A.1 spec-drafter consumes this DEC. Static registry (hardcoded import list in `__init__.py`) is sufficient given only 2 known backends and internal-only scope; if chosen, state it explicitly so Phase B does not over-engineer entry-points.

---

### F-02
- **id**: `b9e04d51`
- **severity**: Major
- **category**: testability
- **scope**: `tests/test_pre_merge_gate.py` — mock rewrite (Deliverable C)
- **type**: Hidden coupling — mock target mismatch risk
- **summary**: Deliverable C states "~10 `mock.patch.object(gate, 'detect_aether', ...)` → `mock.patch.object(AetherBackend, 'probe', ...)`". However, `gate_check()` currently calls `detect_aether()` **and** `verify_aether_in_flight_flag()` as two separate module-level functions. The new `AetherBackend.probe()` must absorb both. If probe() merges detection + flag-verification into one method, the `verify_aether_in_flight_flag` mock path (currently a separate `mock.patch.object(gate, "verify_aether_in_flight_flag", ...)` in 5 of the 9 test cases) also disappears. DEC does not acknowledge this second mock target, risking an incomplete rewrite and broken test isolation.
- **rationale**: Reading the test file: `GateCheckTests` has 7 test methods, each using 2–3 `@mock.patch.object` stacks: `detect_aether` + `verify_aether_in_flight_flag` + `_query_aether`. After the refactor, `_query_aether` also moves into `AetherBackend.query_branch_in_flight()` / `query_pr_ci()`. That is three mock targets collapsing, not one. If `probe()` only absorbs `detect_aether` but `_query_aether` is patched at the module level (not the instance method), the test isolation is broken — you mock the module-level helper that no longer exists. The DEC's "~10 places" count may be accurate for `detect_aether` alone but is silent on `_query_aether` and `verify_aether_in_flight_flag`.
- **recommended_action**: Before Phase B coding begins, enumerate all three collapsing mock targets (`detect_aether`, `verify_aether_in_flight_flag`, `_query_aether`) in the DEC or the forthcoming Spec's test plan. State that post-refactor tests mock `AetherBackend` at the instance/class level: `probe()` replaces the first two, and `query_pr_ci()` / `query_branch_in_flight()` replace the third. This prevents partial rewrite leaving dangling mock.patches referencing deleted symbols.

---

### F-03
- **id**: `c2a18f73`
- **severity**: Minor
- **category**: contract-design
- **scope**: `ci_backends/base.py` (prospective) — `CIStatus` / `InFlightStatus` dataclasses
- **type**: Omission — dataclass field sets not defined in DEC
- **summary**: DEC names the two dataclasses as "substance, catch typo" but lists no fields. The Phase B implementer derives field names by reading current `_build_output()` / `_translate_in_flight_run()` return dicts — but those are internal dicts, not a public contract. If fields are mis-named (e.g., `status` vs `ci_status` vs `pr_ci_status`) the GHA stub's `raise NotImplementedError` message (Hard Constraint #4) cannot reference correct field names.
- **rationale**: Current `_build_output()` returns `{"verdict", "pr_ci_status", "in_flight_runs", "primitive_used", "primitive_version_sha", "raw_message"}`. `CIStatus` should mirror at minimum `verdict`, `pr_ci_status`, `raw_message`. `InFlightStatus` maps to `_translate_in_flight_run()` output: `run_id`, `branch`, `started_at`, `elapsed_seconds`. Without an explicit field list in the DEC, there is a risk that `AetherBackend` returns a dataclass and the callers in `gate_check()` still access dict keys — defeating the "catch typo" motivation entirely.
- **recommended_action**: Add a small field table to the DEC (or flag for the spec-drafter to include in proposal.md's contract section): `CIStatus(verdict: str, pr_ci_status: str, raw_message: str, primitive_used: str)` and `InFlightStatus(run_id: int, branch: str, started_at: str, elapsed_seconds: int)`. This is the minimum to make Hard Constraint #1 ("Aether behavior zero change") verifiable at the type level.

---

### F-04
- **id**: `d5b3e089`
- **severity**: Minor
- **category**: correctness
- **scope**: `pre_merge_gate.py:284` — `cfg` merge strategy + alias path
- **type**: Silent override risk — `{**DEFAULT_CONFIG, **config}` flat merge breaks nested keys
- **summary**: `gate_check()` merges config as `cfg = {**DEFAULT_CONFIG, **(config or {})}`. After the rename, `DEFAULT_CONFIG` will have `no_ci_fallback`; if a user passes `config={"no_aether_fallback": "abort"}`, the alias translation must happen *before* this merge or the old key is silently ignored. DEC does not specify the alias translation point.
- **rationale**: Current code: user's config overrides `DEFAULT_CONFIG` via flat dict merge. The alias path (Q2 decision) must translate `no_aether_fallback` → `no_ci_fallback` before the merge, otherwise the alias key sits alongside the canonical key and neither takes effect if both are present. Similarly, `primitive_preference` → `ci_backend` (or whatever the new canonical key is) needs the same translation. The DEC describes the alias as "reads and emits deprecation warning" but does not state whether translation happens in `_load_config_from_file()`, at the top of `gate_check()`, or in a dedicated `_normalize_config()` step.
- **recommended_action**: Specify in the Spec that alias translation is a dedicated `_normalize_config(raw: dict) -> dict` step called at the top of `gate_check()` before the `{**DEFAULT_CONFIG, **normalized}` merge. This makes the translation testable in isolation (Deliverable C alias key path test) and prevents the silent-override failure mode.

---

### F-05
- **id**: `e6f2a347`
- **severity**: Minor
- **category**: correctness
- **scope**: `ci_backends/aether.py` (prospective) — `@functools.lru_cache(maxsize=1)` on probe
- **type**: Cache rot risk in multi-invocation or test isolation context
- **summary**: DEC mentions `lru_cache(maxsize=1)` for the probe result but does not address (a) test isolation teardown, or (b) the case where `aether` binary is installed mid-process (unlikely in production, but a test concern). In test suites that mock `shutil.which`, a cached probe result from test N poisons test N+1.
- **rationale**: `lru_cache` on a classmethod or module-level function is a known pytest isolation hazard. The current `detect_aether()` is not cached, so tests freely mock it per-test. After moving to `AetherBackend.probe()` with `lru_cache`, any test that calls the real probe (e.g., a dogfood smoke test in Deliverable E) will cache a result that leaks into subsequent tests unless `AetherBackend.probe.cache_clear()` is called in tearDown. The DEC's constraint #1 ("all current test cases must PASS") may be violated if cache state leaks.
- **recommended_action**: Either (a) document `probe.cache_clear()` as required in test setUp/tearDown for any test that invokes probe directly, or (b) make `probe()` non-cached and cache at the `gate_check()` call site with a passed-in flag. Option (b) is simpler: pass `_probe_cache: dict | None = None` to `gate_check()` and let tests inject `{}` to force re-probe. This avoids the class-level cache entirely for a module that is not a long-running service.

---

## §Per-dimension verdict

**(a) Substance convergence — PASS**
The 5 decisions are internally consistent. Q1 stub × Q4 dual-method contract correctly limits blast radius. Q2 alias × Q3 config-first probe correctly preserves zero-config UX for 100% of current users (confirmed by the live `grep` survey). Q4 contract × Q5 doc 1:1 mapping is sound. No paper-fix detected: the refactor actually moves `detect_aether()` + `_query_aether()` logic into `AetherBackend`, not just renames a config key.

**(b) Hard constraints completeness — PASS_WITH_WARNINGS**
Constraints 1–7 are substantive and mostly testable. One gap: Constraint #3 says "alias old key reads and emits deprecation warning; unit test explicitly covers" but does not specify *where* the warning emits (Python `warnings.warn()` with `DeprecationWarning`? `logging.warning()`? `stderr` print?). The distinction matters for test assertions — `mock.patch("warnings.warn")` vs log capture vs `capsys`. This is minor but should be resolved before Phase A.1.

**(c) Risk identification — PASS_WITH_WARNINGS**
DEC identifies alias dead-code rot and blast radius adequately. Two risks not named: (1) `lru_cache` test isolation (F-05 above), (2) the mock rewrite incompleteness risk (F-02 above). Both are implementation risks that could cause Constraint #1 failures mid-sprint. The DEC's estimate of ~2h for Deliverable C may be tight if the triple mock-target collapse is discovered during coding rather than planning.

**(d) DEC document quality — PASS**
Alternative drop rationales are concrete and cross-referenced. The live `grep` survey result (0 hits for `no_aether_fallback` in 6 sibling repos) is a strong empirical anchor for Q2/Q3. Cross-references to predecessor handoff and boundary-audit note are present. The one gap is the registry discovery mechanism (F-01) and the dataclass field omission (F-03), which are genuine spec gaps rather than documentation style issues.

**(e) Implementation feasibility — PASS**
~8.5h estimate is credible for the selected scope. The boundary-audit sketch already produced a concrete config structure (§修复 2 code example) that can be lifted nearly verbatim into `DEFAULT_CONFIG`. `AetherBackend` is largely a file-split of existing `detect_aether()` + `_query_aether()` + `verify_aether_in_flight_flag()` — no new logic, only structural reorganization. The main risk to the estimate is Deliverable C mock rewrite (see F-02): if the triple mock-target collapse is discovered mid-sprint, it could add 1–2h. The ~8.5h lower-bound is still reachable; the ~12h upper-bound from the boundary-audit memo accounts for this.

---

## §Final vote

**PASS_WITH_WARNINGS** — The 5 decisions are coherent and the refactor is substantive; two Major gaps (registry pattern undecided, mock-target collapse unacknowledged) should be resolved in Phase A.1 proposal.md before Phase B coding begins, but neither blocks the spec-drafter from proceeding now.
