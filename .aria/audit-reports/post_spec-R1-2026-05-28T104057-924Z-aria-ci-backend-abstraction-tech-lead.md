---
checkpoint: post_spec
mode: convergence
round: 1
agent: tech-lead
target: openspec/changes/aria-ci-backend-abstraction/{proposal.md, tasks.md}
change_id: aria-ci-backend-abstraction
timestamp: 2026-05-28T10:40:57.924Z
vote: REVISE
critical_count: 1
major_count: 5
minor_count: 4
---

# Post-Spec R1 Audit — aria-ci-backend-abstraction (tech-lead perspective)

L3 baseline R1 per `[[feedback_audit_convergence_patterns]]` — Q1-Q5 brainstorm decisions are LOCKED, audit focuses on Spec quality (completeness, AC testability, task ordering, estimate calibration, cross-ship coordination, Phase B implementer ergonomics).

Overall the Spec is high-quality (DEC anchors traceable, 9 hard constraints with R1-audit provenance, AC structure mirrors AC-N -> Hard-Constraint-N). Findings below are concrete gaps an implementer would hit mid-Phase-B without DEC context.

---

## Findings

### F-01 [CRITICAL] — `gate_check()` pseudocode contradicts Hard Constraint #7 routing for the "no backend resolved" branch

- **id**: `a17c4e91`
- **severity**: Critical
- **category**: ac-coverage
- **scope**: proposal.md §B.4 + AC-2.3 + AC-2.4
- **type**: behavior-gap
- **summary**: §B.4 pseudocode routes `backend is None` through `_no_ci_output(cfg["no_ci_fallback"])` — correct — but the AC test set never covers the **boundary case where Aether probe fails AND GHA probe succeeds AND query raises NIE**. AC-2.4 tests "装 mock gh + mock auth -> gate_check -> assertRaises NIE" which assumes Aether is absent. If Aether mock returns False (or is uninstalled) and GHA stub becomes the resolved backend in a pure-Aether project that happens to also have `gh authed`, gate_check aborts via NIE — but no AC verifies the **error message** is operable (the AC just asserts the type). An implementer reading only AC-2 may write `raise NotImplementedError()` without the message body.
- **rationale**: AC-2.2 specifies the message text inside `github_actions.py` (correctly), but AC-2.4 only `assertRaises(NotImplementedError)` — type, not message. Without `assertIn("PR welcome", str(exc))` or similar, implementer may strip/shorten the message in a "cleanup" pass, violating Hard Constraint #4. The current `test_pre_merge_gate.py` style (verified — uses `mock.patch.object` 24× with assertEqual on verdict strings, no message-content assertions) lends itself to the same brittleness. Three-line stub backends without message will pass AC-2.4 but rot Hard Constraint #4.
- **recommended_action**: Add **AC-2.5**: "Test `test_gha_nie_message_contains_operable_guidance` — `assertIn('PR welcome', str(exc))` AND `assertIn('SKILL.md', str(exc))` AND `assertIn('ci_backends: []', str(exc))` on both `query_pr_ci()` and `query_branch_in_flight()` NIE instances." Add corresponding task line under T-tests 3.5 ("3.5b assert NIE message body, not just type"). This makes Hard Constraint #4 testable rather than aspirational.

### F-02 [MAJOR] — `_translate_value()` value-shape mapping is incomplete + ambiguous edge cases unaddressed

- **id**: `b3d8af07`
- **severity**: Major
- **category**: implementation-gap
- **scope**: proposal.md §B.2 + AC-3 + tasks.md 2.3
- **type**: spec-ambiguity
- **summary**: `_translate_value()` handles `primitive_preference: ["aether-ci-cli"]` → `[{"name": "aether-ci-cli"}]`. But what if a user wrote `primitive_preference: ["foo", "bar"]` (non-Aether legacy entries)? What if it's `[]` (legacy explicit-empty)? What if old value is None or a non-list scalar (mis-typed config that was previously silently coerced)? AC-3 mandates the warning and translation but doesn't pin the value-shape edge cases — implementer must guess. Same for `no_aether_fallback`: legal values are presumably `skip_with_warning` / `abort`, but if an old config has typos, do we translate the typo verbatim and let downstream validation reject, or do we sanitize?
- **rationale**: An implementer mid-Phase-B will hit this in 30 minutes. The proposal correctly identifies the 1 happy-path mapping but leaves 4 edge cases undefined: (1) unknown backend names in `primitive_preference`, (2) empty-list legacy value, (3) non-list legacy type (None/string/dict), (4) invalid `no_aether_fallback` enum value. Without spec guidance, the implementer's default will be inconsistent across runs (or worse, between R1 reviewer's mental model and actual code, only surfacing at Phase C review or in dogfood).
- **recommended_action**: Add **§B.2.1 "Edge cases in _translate_value()"** block specifying: (a) unknown backend names → preserve as `{"name": "<unknown>"}` (let `resolve_ci_backend` skip them since name_map.get() returns None — already safe per §B.3); (b) empty-list `[]` → `[]` (preserve); (c) non-list types → raise TypeError with explicit message naming the offending config key (fail loud — don't silently coerce); (d) `no_aether_fallback` is passed through unchanged (no enum validation here — `_no_ci_output` validates downstream). Add 1 task line under T-refactor 2.3 referencing these edges + 1 AC under AC-3 ("AC-3.6: Test 4 edge cases per §B.2.1").

### F-03 [MAJOR] — `_compute_verdict()` is referenced but never specified — field-access change is the highest-blast-radius hidden refactor

- **id**: `c5217b39`
- **severity**: Major
- **category**: implementation-gap
- **scope**: proposal.md §B.4 + AC-5.4 + tasks.md 2.5
- **type**: undeclared-deliverable
- **summary**: §B.4 pseudocode ends with `return _compute_verdict(pr_status, in_flight, cfg)`. There is no §B.6 / §A.5 specifying that `_compute_verdict()` exists, its signature, its current state (is this a rename of existing logic? a new function?), or how it converts the current dict-based PR-status structure to `CIStatus.state == "passing"` attribute access (AC-5.4). The current `pre_merge_gate.py` (verified — 387 LOC) does NOT have a function named `_compute_verdict`; verdict logic lives inline inside `gate_check()`. So this is a **new function extraction** that's not separately tasked or estimated.
- **rationale**: This is the field-access change called out in the audit prompt's specification-gaps focus. Implementer reads "call site changes from dict-key to attribute access" (AC-5.4) but the actual refactor — extracting verdict-computation logic from current `gate_check()` body (likely 40-80 LOC) into a new `_compute_verdict(pr_status: CIStatus, in_flight: InFlightStatus, cfg: dict) -> dict` — is hidden inside the §B.4 pseudocode line. The 1h estimate for T-refactor cannot absorb this. Also, the current verdict computation reads multiple aether-specific JSON fields (run_id, conclusion, etc.) — these need a mapping to `CIStatus` fields, but AC-5.2 only specifies the new dataclass field names, not the mapping from existing `_query_aether` dict outputs into them.
- **recommended_action**: Add **§B.6 "Extract _compute_verdict()"** specifying: (a) signature `_compute_verdict(pr_status: CIStatus, in_flight: InFlightStatus, cfg: dict) -> dict` returning the existing verdict dict shape; (b) mapping table from current inline verdict logic's dict keys to `CIStatus`/`InFlightStatus` attributes; (c) explicit statement that verdict semantics (green/wait/fail thresholds) are unchanged. Bump T-refactor estimate from 1h to **1.5h** to absorb the extraction. Add tasks.md 2.5b ("Extract _compute_verdict() from current inline gate_check body; preserve verdict semantics"). Add AC-5.5 ("Test `test_compute_verdict_preserves_pre_refactor_outputs` — table-driven 6 cases covering each (CIStatus.state × InFlightStatus.has_runs) combination").

### F-04 [MAJOR] — Probe cache strategy decision (Option A vs Option B) is `Recommended` not `Decided` — leaves implementer with open architectural choice

- **id**: `d04f9e62`
- **severity**: Major
- **category**: spec-quality
- **scope**: tasks.md 3.11 + proposal §C
- **type**: spec-ambiguity
- **summary**: Task 3.11 reads "Choose lru_cache strategy: Option A ... OR Option B ... **Recommended Option B**". For an L3 Spec at post_spec stage, "Recommended" leaves a non-trivial architectural choice (hidden state via lru_cache decorator vs explicit module-level dict + reset helper) un-decided. Verified current `pre_merge_gate.py` has no `lru_cache` on existing `detect_aether()`, so this is a **forward-looking** decision tied to whether new `CIBackend.probe()` classmethod should be cached. Either choice has different downstream impacts: Option A is invisible state (callers can't reset without knowing about the decorator); Option B is explicit (callers see `reset_probe_cache()` in `__init__.py` exports).
- **rationale**: An implementer at Phase B has two acceptable paths and may pick either, but the test design (T-tests 3.12 "Add tearDown ensuring probe cache reset") is shape-coupled to the choice. R1 backend-architect F-05 already flagged this; the proposal acknowledged it but deferred the decision to the implementer. For mid-sprint pickup (audit prompt's stated concern), this is exactly the kind of unspec'd decision that produces inconsistent code across iterations.
- **recommended_action**: Lock the decision: **Option B (module-level `_probe_cache: dict[type[CIBackend], bool]` + `reset_probe_cache()` helper exported from `ci_backends/__init__.py`)**. Rationale: explicit > implicit per Hard Constraint #8 spirit (static registry pattern = "no decorator magic"); test isolation becomes a fixture, not a `tearDown` boilerplate. Rewrite task 3.11 from "Choose ... Recommended B" to "Implement Option B: module-level `_probe_cache` dict in `ci_backends/__init__.py` + `reset_probe_cache()` helper exported." Add AC-4.5 ("Test `test_reset_probe_cache_clears_state`").

### F-05 [MAJOR] — `_no_ci_output()` rename signature change impact on workflow-runner integration unaddressed

- **id**: `e6f81b48`
- **severity**: Major
- **category**: cross-system-impact
- **scope**: proposal.md §B.5 + tasks.md 2.6 + AC-6
- **type**: undeclared-blast-radius
- **summary**: §B.5 says "Rename `_no_aether_output()` → `_no_ci_output()` (preserve all behavior)". But this is a **public-ish symbol** — `workflow-runner` skill consumes pre_merge_gate via the integration mentioned in CLAUDE.md Rule #8 ("by `wait_recoverable` 错误类型处理"). The audit prompt explicitly flagged "`_no_ci_output()` rename impact on workflow-runner integration" as a specification-gap concern. The proposal does not include a grep-verified statement of whether workflow-runner (or any other in-repo consumer) imports/references `_no_aether_output` by name, nor a task to update such call sites if they exist.
- **rationale**: If `_no_aether_output` is imported by name (`from pre_merge_gate import _no_aether_output`) by any other skill, the rename silently breaks that import at runtime — not at test time, since cross-skill imports rarely have unit-test coverage. Even if no one imports it (highly probable since it's prefixed with `_` private), the Spec should affirm this via a one-line grep result, not assume it. The current §B.5 reads as a 1-line afterthought; for a deliverable touching Rule #8 enforcement, blast-radius affirmation is cheap insurance.
- **recommended_action**: Add **§B.5.1 "Blast-radius verification"** with explicit grep result: `grep -rn '_no_aether_output\b' aria/ standards/ docs/ openspec/` (expected: only references inside pre_merge_gate.py and its test). If any external references exist, add T-refactor task 2.6b updating them. Equally important: grep `detect_aether\b` — verified in this audit, only `tests/test_pre_merge_gate.py` references it (24× via `mock.patch.object`). Document this in §B.5.1 so reviewer/implementer can re-verify if state drifts between audit and Phase B start.

### F-06 [MAJOR] — Cross-ship CHANGELOG ordering reasoning is correct but insufficient for v1.29.0 block-flip race

- **id**: `f7a9c051`
- **severity**: Major
- **category**: cross-ship-coordination
- **scope**: proposal.md §Why now + §Risk + tasks.md 6.4 + AC-8.2
- **type**: race-condition
- **summary**: The Spec correctly notes (a) v1.29.0 reserved for 2026-06-07 D+14 block-flip, (b) v1.31.0 entry goes **above** v1.30.0, (c) v1.29.0 placeholder block must not be touched. But it does not specify the **literal location** in CHANGELOG.md (line number or anchor) where v1.31.0 entry should be inserted, nor how to handle the case where v1.29.0 block-flip ship happens **before** this Spec ships (which would push v1.31.0 → above v1.30.0 → above v1.29.0). Sister terminal could ship v1.29.0 block-flip out-of-order if D+14 trigger fires while this Spec is mid-Phase-B.
- **rationale**: Per memory `[[feedback_claude_md_project_status_high_contention]]`, CHANGELOG is high-contention during overlap windows. The Spec's mitigation ("v1.29.0 placeholder 不动") covers the static case but not the dynamic case: what if v1.29.0 block-flip ships first and writes a real v1.29.0 block? Then v1.31.0 ordering is no longer "above v1.30.0" — it should still be top-of-file, but the rebase-merge of this Spec's CHANGELOG diff against sister's may produce a conflict that auto-merges incorrectly. AC-8.2 should explicitly cover this.
- **recommended_action**: Strengthen AC-8.2: "v1.31.0 CHANGELOG entry inserted at top-of-file (above whichever of v1.29.0/v1.30.0 is currently topmost). Phase C.2 task 8.6 must include `git diff origin/master -- aria/CHANGELOG.md` inspection pre-merge to detect sister-terminal v1.29.0 block-flip and re-verify ordering. If conflict detected, manual semantic merge per `[[feedback_claude_md_project_status_high_contention]]` — do not let auto-merge resolve." Add 1 line to tasks.md 6.4 referencing this race scenario explicitly.

### F-07 [MINOR] — SKILL.md aether reference count is "~10" but ground-truth grep returns 14

- **id**: `f12d9a45`
- **severity**: Minor
- **category**: spec-accuracy
- **scope**: proposal.md §Current state table L56 + §D.2 + tasks.md 4.2
- **type**: estimate-precision
- **summary**: Proposal §Current state table says "SKILL.md references | ~10 处含 `aether-ci-cli` / `aether ci status` / `no_aether_fallback`". Actual `grep -c "aether-ci-cli\|aether ci status\|no_aether_fallback\|primitive_preference" aria/skills/phase-c-integrator/SKILL.md` = **14**. Tasks.md 4.2 says "replace ~10 aether-specific references" — same off-by-4. Not material to AC outcome (grep-verify-post-edit is the test, count is informational), but R1 audit explicitly verified "23" in test file and "~10" in SKILL.md — the spec author trusted DEC's count rather than re-grepping.
- **rationale**: Spec accuracy hygiene — if other counts (e.g. "21 existing test methods" in AC-1.1, "23 detect_aether mocks" in §C) are similarly stale, downstream metric assertions in T-tests could be off. Verified count of `detect_aether` mocks in test file = 24, not 23. Small drift but should be tightened before Phase B.
- **recommended_action**: Re-grep all numeric claims in proposal §Current state table + tasks.md before sealing Spec: (a) SKILL.md references actual = 14; (b) test file mock count actual = 24; (c) `pre_merge_gate.py` LOC = 387 (confirmed correct). Update §Current state column to reflect ground truth and tasks.md 4.2 grep target list to include `primitive_preference` (currently omitted from D.2 grep). One-line fixes.

### F-08 [MINOR] — Task 2.7 import statement is too prescriptive — couples implementer to exact symbol list

- **id**: `08ab2f7e`
- **severity**: Minor
- **category**: spec-quality
- **scope**: tasks.md 2.7
- **type**: over-prescription
- **summary**: Task 2.7 reads `from ci_backends import CIBackend, CIStatus, InFlightStatus, BACKENDS, AetherBackend, GitHubActionsBackend`. Concrete class imports (`AetherBackend`, `GitHubActionsBackend`) are unnecessary in `pre_merge_gate.py` if the dispatch logic uses only `BACKENDS` + `resolve_ci_backend()` (which it does per §B.3). Importing the concrete classes creates a tighter coupling than `BACKENDS` registry needs — defeats some of Hard Constraint #8's "static registry abstracts which backend wins" intent.
- **rationale**: Implementer copies task verbatim and over-couples. Static registry pattern means callers shouldn't need to name individual backends — `BACKENDS[0]` or `resolve_ci_backend(cfg)` is the abstraction. The proposal §B.4 pseudocode correctly uses only `resolve_ci_backend` + `BACKENDS` (implicitly), but task 2.7 forces unused imports.
- **recommended_action**: Rewrite 2.7: "Update imports: `from .ci_backends import CIBackend, CIStatus, InFlightStatus, BACKENDS, resolve_ci_backend, reset_probe_cache` — concrete backend classes (`AetherBackend`, `GitHubActionsBackend`) NOT imported in pre_merge_gate.py (per Hard Constraint #8 registry abstraction)." Note: `resolve_ci_backend` lives in `pre_merge_gate.py` per §B.3 — adjust if it moves to `__init__.py`.

### F-09 [MINOR] — Phase D.3 handoff trigger evaluation under-specified for Rule #9 boundary

- **id**: `2b6e1937`
- **severity**: Minor
- **category**: rule-9-compliance
- **scope**: tasks.md 11.1 + Risk table
- **type**: convention-coverage
- **summary**: Task 11.1 says "Evaluate Rule #9 handoff trigger (this cycle ~10-10.5h = clear trigger)". Rule #9's trigger formula is `session > 4h OR ≥2 cycles/US OR ≥2 phases`. The "~10-10.5h Phase B" satisfies trigger 1, but the task line doesn't make clear which trigger fires — important because the handoff template's §0 entry pointer mentions trigger reason. Also, if the cycle ends up running ≤4h (over-estimate) AND only covers 1 US AND 1 phase, no handoff is needed — but the task list pre-commits to writing one.
- **rationale**: Minor pedantic point but Phase D.3 has cost (~15-30min) and zero-exception Rule #9 makes the "skip handoff" path narrow. State the trigger explicitly so reviewer can verify the trigger fired.
- **recommended_action**: Rewrite 11.1: "Evaluate Rule #9 handoff trigger. Expected primary trigger: session duration > 4h (per ~10-10.5h Phase B estimate). Fallback triggers also satisfied: cross-2-phase (Phase B + Phase C/D = 3 phases). Document the firing trigger in handoff §0 frontmatter." This pins the Rule #9 evaluation outcome and removes ambiguity for Phase D execution.

### F-10 [MINOR] — Out-of-scope item list omits "`_compute_verdict` extraction not a refactor of verdict semantics"

- **id**: `5c1e8a02`
- **severity**: Minor
- **category**: scope-fence
- **scope**: proposal.md §Out of Scope
- **type**: defensive-fence
- **summary**: §Out of Scope correctly fences GHA real impl, GitLab/Forgejo backends, GitProvider ABC, etc. Given F-03 (added `_compute_verdict` extraction), the Out-of-Scope should explicitly say: "verdict computation semantics unchanged — `_compute_verdict` is a mechanical extraction, not a redesign. Threshold values + green/wait/fail mapping logic are bit-for-bit identical to current inline `gate_check()` body."
- **rationale**: Refactor blast-radius defense. Without this fence, an implementer extracting `_compute_verdict` may also "improve" the verdict logic (add edge cases, change thresholds) because they're touching the code anyway. Explicit fence prevents scope creep into the high-risk Rule #8 enforcement core.
- **recommended_action**: Add to §Out of Scope: "❌ Verdict semantics changes — `_compute_verdict` extraction (per §B.6, if added) must preserve current inline logic bit-for-bit. Any threshold/edge-case improvement is a separate Spec."

---

## Per-dimension verdict

### (a) Spec completeness — **PARTIAL**

Strong: Why/What/Out-of-scope/Hard-constraints sections are thorough, DEC anchors traceable, 9 Hard Constraints with R1-audit provenance. Reference list is comprehensive (DEC + boundary memo + handoff predecessor + R1 reports + 8 memory anchors).

Gaps: §B.4 references `_compute_verdict()` without specifying it (F-03) — this is the highest-impact omission. §B.2 `_translate_value()` happy path only, edge cases undefined (F-02). §B.5 `_no_ci_output` rename lacks blast-radius verification (F-05).

Verdict: completeness gaps are concrete and addressable in 1-2 paragraph spec additions; not aspirational, not architectural.

### (b) AC testability — **PARTIAL**

Strong: 8 AC groups each map 1:1 to Hard Constraints. AC-1.1 (21 existing tests PASS) + AC-2.4 (NIE assertRaises) + AC-4.4 (grep verification) are concrete and individually verifiable.

Gaps: AC-2.4 tests NIE type but not NIE message body (F-01) — Hard Constraint #4 "操作可message" is aspirational without message assertions. AC-3 edge cases (F-02) not tested. AC-5 lacks `_compute_verdict` field-mapping AC (F-03). AC-8.2 doesn't cover dynamic v1.29.0 race (F-06).

Verdict: most ACs testable; 4 add-on ACs (2.5, 3.6, 4.5, 5.5) required to close gaps.

### (c) Task ordering correctness — **PASS**

Critical path (8 steps in tasks.md §Task ordering) is correct and implementable in order. T-backends 1.2 (base.py) → 1.3/1.4 (siblings) → 1.5 (registry) → T-refactor 2.4 (resolve_ci_backend) is correctly DAG-ordered. Phase C/D ordering per `[[feedback_sequenced_multirepo_gitlink_bump]]` (aria PR merge first → main gitlink bump second) is correctly captured in tasks 7-11.

Minor: Tasks lack a sub-step for `_compute_verdict` extraction (F-03) and probe-cache option B implementation (F-04). Parallel opportunities are reasonable; no false dependencies.

### (d) Estimate calibration — **PARTIAL**

The 10-10.5h headline is reasonable for the visible scope. Per-deliverable:
- A (3h, ci_backends/) — realistic (4 files ~150 LOC total + careful Aether migration)
- B (1h, pre_merge_gate refactor) — **under-estimated** if `_compute_verdict` extraction is included (F-03 adds ~30-45min). Revised: 1.5h.
- C (3-3.5h, tests) — realistic for 21 collapse + 6 new test classes + ~30 cases
- D (1.25h, docs) — realistic
- E (1.5-2h, Rule #6 substitute) — realistic
- F (0.5h, SOT bump) — realistic

If F-03 (compute_verdict extraction + AC + tests) is added, total becomes **~11h** (still within DEC's "~8-12h" boundary). Buffer is thin but acceptable for L3.

### (e) Cross-ship coordination — **PARTIAL**

Strong: §Risk table correctly identifies (a) CHANGELOG v1.31.0 vs v1.29.0 placeholder, (b) sister terminal CLAUDE.md contention, (c) M6 file collision risk. Mitigation table cites `[[feedback_claude_md_project_status_high_contention]]` correctly.

Gaps: Static "don't touch v1.29.0 placeholder" mitigation does not defend against dynamic case where v1.29.0 block-flip ships first during Phase B/C (F-06). No pre-Phase-C `git fetch` for the aria-plugin submodule specifically — only main repo.

### (f) Specification gaps for Phase B (mid-sprint pickup) — **PARTIAL**

Audit prompt explicitly flagged 3 concerns:
1. `_translate_value()` value-shape mapping completeness — **GAP CONFIRMED** (F-02)
2. `_no_ci_output()` rename impact on workflow-runner integration — **GAP CONFIRMED** (F-05)
3. `_compute_verdict()` field-access change — **GAP CONFIRMED** (F-03)

All three are real implementer-blocking ambiguities. F-03 is the most material (a hidden refactor that isn't even named in deliverables). F-02 + F-05 are addressable with one paragraph each.

---

## Final vote

**REVISE** — with 1 Critical + 5 Major findings, all addressable in additive Spec edits (no architectural rework needed). Q1-Q5 decisions remain LOCKED — findings target Spec quality gaps, not brainstorm re-litigation.

Required R2 changes (estimate 30-45min Spec edit + R2 audit):
1. Add §B.6 `_compute_verdict()` extraction spec + AC-5.5 + tasks 2.5b (F-03 — critical for Phase B implementability)
2. Add §B.2.1 `_translate_value()` edge cases + AC-3.6 + tasks 2.3b (F-02)
3. Add AC-2.5 NIE message body assertions (F-01 — the only Critical)
4. Lock probe cache Option B + AC-4.5 + rewrite task 3.11 (F-04)
5. Add §B.5.1 blast-radius grep + verify external `_no_aether_output` references = 0 (F-05)
6. Strengthen AC-8.2 + tasks.md 8.6 with dynamic v1.29.0 race defense (F-06)

Minors (F-07/08/09/10) can be folded into the same R2 edit pass cheaply.

Per `[[feedback_audit_convergence_patterns]]` L3 baseline R1 = REVISE is expected. R2 should converge to PASS_WITH_WARNINGS or PASS pending sister-agent (backend-architect, qa-engineer) findings alignment. Substance-convergence checkpoint: if other R1 reviewers independently raise F-03 (`_compute_verdict` hidden refactor) or F-01 (NIE message body), that's strong signal per `[[feedback_brainstorm_substance_convergence_pattern]]` that R2 anchor is correct.
