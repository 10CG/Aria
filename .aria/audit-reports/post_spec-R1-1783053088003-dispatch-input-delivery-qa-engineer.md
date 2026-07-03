---
checkpoint: post_spec
mode: convergence
round: 1
agent: qa-engineer
verdict: REVISE
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783053088003
converged: false
---

# post_spec R1 — qa-engineer audit: aria-2.0-m6-dispatch-input-delivery

## Scope of verification

Read against real code at `aria-orchestrator` HEAD `daf7c79`:
- `docker/aria-runner/modes/initial.sh` (full file, 597 lines)
- `docker/aria-runner/lib/compute-assertions.sh` (full file)
- `docker/aria-runner/prompts/RENDERING_CONTRACT.md`
- `hermes-extensions/aria-layer1/aria_layer1/extension.py` (`_handle_s4_launch`, `_handle_s5_await`, seed/Phase-1, ISSUE_URL construction, head_branch)
- `hermes-extensions/aria-layer1/aria_layer1/alloc_status_provider.py` (`get_status`, `get_alloc_logs`)
- `hermes-extensions/aria-layer1/aria_layer1/interfaces.py` (`FailReason` enum)
- `hermes-extensions/aria-layer1/aria_layer1/transitions.py`, `schema.sql`

DEC-20260702-001 read in full. Both original OBJECTION items (① Layer1-scope, ② empty-`expected_changes` false-green) verified against code and confirmed real; both are nominally "folded into C'" in proposal.md §B/§C. However, code recon surfaced a **new, more severe gap in how the two fixes interact with the existing state machine** that is not addressed by either the DEC or the current spec draft.

---

## Findings

### [CRITICAL][fix-effectiveness:AC-1↔AC-4 contradiction] Fetch-mode "cannot read SUCCESS" makes AC-1 (S9_CLOSE) structurally unreachable under the unmodified exit-code/S5_AWAIT coupling

**Verified mechanism** (not speculative — traced end to end):

1. `initial.sh:592-596` — the container's Nomad exit code is a **strict 1:1 function of `FINAL_OUTCOME`**: `exit 0` iff `FINAL_OUTCOME == "SUCCESS"`, else `exit 1`. There is no third state.
2. `initial.sh:524-536` — `FINAL_OUTCOME` becomes `SUCCESS` only if the AD-M1-4 5-AND holds, **including** `FILE_TOUCHED_HIT == "true" && DIFF_CONTAINS_HIT == "true"`. If any is false → `FINAL_OUTCOME = ASSERTION_MISMATCH`.
3. `extension.py:_handle_s5_await` (lines 2593-2638) — Layer 1's **only** signal for routing `S5_AWAIT → S6_REVIEW` vs `S5_AWAIT → S_FAIL` is the **raw Nomad alloc `exit_code`** (via `alloc_status_provider.get_status()`, whose Protocol shape is literally `{state, exit_code}` — no other field is read). `exit_code == 0` → `S6_REVIEW`; **any non-zero exit_code → `S_FAIL(fail_reason=FailReason.CONTAINER_CRASH)`**, unconditionally. `result.json`'s content (assertion_results, outcome, error.type) is **never read** by this handler.

Chain the three: per this Spec's own AC-4 ("fetch-mode outcome cannot read SUCCESS by default") and C.1's fix (empty `expected_file_touched[]`/`expected_diff_contains[]` → `unknown`/`skip`, never `true`), **every** autonomous (`ARIA-`, always-fetch) dispatch will have `FILE_TOUCHED_HIT`/`DIFF_CONTAINS_HIT` ≠ `"true"` (there is no `expected_changes` at all in fetch mode). Unless `initial.sh`'s 5-AND gate itself (step 3 above) is *also* restructured with a fetch-mode branch that bypasses the two assertion-hit ANDs and independently decides to `exit 0`, **`FINAL_OUTCOME` will always be `ASSERTION_MISMATCH` → `exit 1` → Layer 1 will always route to `S_FAIL(container_crash)`** — never `S6_REVIEW`, never `S9_CLOSE`.

This reproduces the *exact* symptom this Spec exists to fix (100% autonomous `S_FAIL`), via a new mechanism (misclassified `container_crash` instead of Step-1 regex `die`), and makes **AC-1** ("reaches S9_CLOSE with a merged PR") **and** **AC-4** ("fetch-mode outcome cannot read SUCCESS") **mutually unsatisfiable as currently worded**, unless a third path is defined and specified.

**What's missing from the Spec**: Task 1.8 ("Fetch-mode independent outcome semantic — does not reuse AD-M1-4 5-AND default-true hits") *names* the problem but does not specify:
- the actual new outcome/exit-code mapping for fetch-mode dispatches that both (a) is not literally `"SUCCESS"` in the assertion sense (satisfying AC-4) and (b) still yields `exit 0` so Nomad/Layer 1 treat it as healthy completion (satisfying AC-1);
- any change to `_handle_s5_await`'s alloc-exit_code-only routing, which today cannot distinguish "fetch-mode healthy completion" from "genuine container crash" — both are `exit_code != 0` under the naive reading, or both are `exit_code == 0` under a "just make it exit 0" reading, either of which reintroduces a masking hazard;
- a companion amendment to **AD-M1-4** itself (the proposal's §How table lists AD-M6-10 new + AD-M0-5 amend, but **not** AD-M1-4, even though C.2 is a direct carve-out of AD-M1-4's frozen 5-AND SUCCESS definition — Rule #3 gap).

**Fix**: Before Phase B, the Spec must pin down a concrete third outcome (e.g. a value distinct from both `SUCCESS` and `ASSERTION_MISMATCH`, along with the explicit exit-code it maps to) and trace it through `initial.sh:524-596` **and** `extension.py:_handle_s5_await`. Add an explicit task under TG-1/TG-2 for this wiring, and an AC (or tighten AC-1/AC-4) with an integration test asserting: synthetic fetch-mode dispatch, claude succeeds + commits + opens PR, zero `expected_changes` → container exits with the code that reaches `S6_REVIEW` (not `S_FAIL`). Add AD-M1-4 amendment to §How / TG-5.

---

### [CRITICAL][testability:AC-6 unimplementable] No Layer-1-side task exists to make fetch failures distinguishable from container crashes

`extension.py:_handle_s5_await`'s only failure classification on non-zero exit is the single hardcoded `FailReason.CONTAINER_CRASH` (line 2632). The `FailReason` enum (`interfaces.py`) is a closed, explicitly-additive list (docstring: "no implicit 'other' fallthrough... each failure path must set an explicit reason") with no fetch-related value. The one precedent for a **richer cross-node signal** than alloc `exit_code` is `alloc_status_provider.get_alloc_logs()` (Spec Y T3), and it is wired **only** into the redo-path's specific `[redo.sh] PASS ...` stderr-marker read — not into the generic terminal-exit-code branch that all dispatches (including fetch-mode) go through.

TG-1 (1.3/1.4) implements `FETCH_FAILED` detection **inside the container only**. No task in TG-2 (or anywhere else) adds a `FailReason` value, extends `_handle_s5_await` to read a distinguishing marker/log line, or otherwise gives Layer 1 the means to tell "fetch failed (infra)" apart from "claude crashed (agent)" — both currently collapse to the identical `S_FAIL(container_crash)` via the identical exit-code path.

**Fix**: Add an explicit TG-2 task: (a) new `FailReason` value(s) for fetch-mode infra failure; (b) `initial.sh` echoes a stderr marker (mirroring the existing `[redo.sh] PASS ...` precedent) on `FETCH_FAILED`; (c) `_handle_s5_await` (or a sibling classifier) reads alloc logs via the existing `get_alloc_logs()` primitive on non-zero exit and maps the marker to the new `FailReason`, falling back to `CONTAINER_CRASH` only when no marker is found. Add a corresponding AC-6 test (fixture: alloc terminated non-zero + stderr contains `FETCH_FAILED` marker → distinct fail_reason vs. no marker → `CONTAINER_CRASH`).

---

### [MAJOR][correctness:ISSUE_URL reconstruction] Composite `issue_id` → plain-number extraction for `ISSUE_URL` is asserted but not specified or tasked

`extension.py:_handle_s4_launch` builds `issue_url` directly from `dispatch_row.issue_id`:
```python
issue_url = f"{self.forgejo_base_url.rstrip('/')}/{forgejo_org}/{forgejo_repo}/issues/{issue_id}"
```
Today `issue_id` is the raw Forgejo number (seeded at `issue_id = str(issue.get("id") or issue.get("number") or "")`, extension.py ~L1177). Task 2.1 changes the *seed point* to store the composite `ARIA-<repo>-<number>` string as `issue_id` (matches D.1's "value-level reformat, no schema column" decision). Task 2.2 says "fix ISSUE_URL to use issue number (already number today ..., but re-verify against new id scheme)" — but does not specify **how** the plain number is recovered at this consumption site once `issue_id` is the composite string (D.1 explicitly rules out a separate DB column to hold the raw number, so parsing back from the string is the only available path and needs an explicit helper + unit test).

Compounding this: `forgejo_org`/`forgejo_repo` here come from **global env vars** (`FORGEJO_ORG`, `FORGEJO_REPO`, default `"10CG"`/`"Aria"`), not from the dispatch's `target_repo`. The DEC's stated rationale for the `<repo>` component ("prevents cross-repo number collision") implies genuine multi-repo dispatch, yet `issue_url` construction doesn't consume per-dispatch repo info at all — even after a correct parse-back fix, cross-repo dispatches would build a URL against the wrong repo.

Because this only manifests as a fetch pointing at the wrong/nonexistent issue (loud failure, not silent corpus pollution), AC-1's E2E dogfood would likely surface it — but there's no dedicated task/AC guarding it, risking a wasted dogfood round and leaving cross-repo correctness unverified.

**Fix**: Add explicit task: parse helper (e.g. `parse_issue_id(s) -> (repo, number)`) with unit tests (round-trip with the format task 2.1 produces); rebuild `issue_url` from the parsed `(repo, number)` (or from `target_repo` META, which Layer 1 already has per B.2) instead of global env defaults; add an AC/test for a non-default `target_repo` case.

---

### [MAJOR][testability:compute-assertions call-site wiring] Fetch-mode never has an `issue.yaml` — compute-assertions.sh's own guard clause will `die` before the C.1 fix logic ever runs

`compute-assertions.sh:37-40`:
```bash
if [[ ! -f "$ISSUE_YAML" ]]; then
    echo "ERROR: issue yaml not found: $ISSUE_YAML" >&2
    exit 1
fi
```
`initial.sh:513-515` unconditionally invokes this script with `"$ISSUE_YAML"` = `${INPUTS_DIR}/${ISSUE_ID}/issue.yaml`. Per A.2, `ARIA-` prefix dispatches are **always-fetch, ignore any existing file** — meaning no `issue.yaml` is ever materialized for autonomous dispatch. Under the current call site, `compute-assertions.sh` would hit this guard and exit 1 for every fetch-mode dispatch **before ever reaching** the (fixed) empty-list detection logic that C.1/1.7's RED test targets.

The Spec/tasks never state whether the intended design is (a) synthesize a stub `issue.yaml` with an explicit empty `expected_changes:` block for fetch mode so the existing script + its fixed logic can run unmodified, or (b) branch in `initial.sh` to skip `compute-assertions.sh` entirely for fetch mode and hardcode the fetch-mode outcome inline. Both are legitimate designs, but the choice is load-bearing for how the RED test (1.7) should be constructed and is currently unstated — the RED test could pass in isolation (testing the script directly with a crafted empty-list yaml) while the actual call site in fetch mode never reaches that code path at all, giving a false sense that C.1/AC-4 is "covered."

**Fix**: Add an explicit task specifying the fetch-mode call-site behavior (stub yaml vs. skip-and-inline), and require an AC-4/dogfood-adjacent test that exercises the actual `initial.sh` call site (not just `compute-assertions.sh` standalone) under a synthetic fetch-mode run with zero `expected_changes`.

---

## Assessment against the qa audit brief

1. **RED-first / false-green repro (C.1/C.2, AC-4)** — the underlying false-green in `compute-assertions.sh:94-120` is real and RED-testable in isolation (confirmed by direct code read: `FILE_HIT=true`/`DIFF_HIT=true` never flipped when the expected lists are empty, due to `<<<` here-string producing one blank-skipped iteration). The **script-level** fix is sound. What's not sound is the **integration**: (a) whether the fixed script is even reached in fetch mode (MAJOR finding above), and (b) whether the resulting non-`SUCCESS` outcome can still let the dispatch progress through the state machine (CRITICAL finding above) — this second point is the qa OBJECTION ② concern reincarnated one layer up: the fix that stops false-green risks re-breaking real-green.
2. **① Layer1/container co-dependency** — TG-1+TG-2 are correctly scoped as co-dependent for the *regex* half of ①. However, recon found a **third**, unaddressed half: even with both TG-1 (regex) and TG-2 (id format/META/head_branch) landed, the Layer 1 state-machine consumption of the container's terminal signal is untouched and will misroute fetch-mode successes to `S_FAIL` (see CRITICAL-1). AC-1's "E2E dogfood, not unit-only" requirement is the right instinct and would catch this at practice time, but at the cost of a very likely failed first dogfood attempt if not fixed before Phase B.
3. **Fetch infra-fail vs agent-fail distinguishability (AC-6)** — not testable as currently scoped; no implementation task exists on the Layer 1 side (CRITICAL-2).
4. **AC testability** — AC-1/2/3/4/5/7/9/10 are each concretely testable/falsifiable given the surrounding code. AC-6 is not implementable/testable as scoped (see above). AC-8 ("surveyed") is a documentation-style AC consistent with prior Spec norms in this project (#147 D.2 precedent) — acceptable, not flagged.
5. **Missed failure modes** — no additional injection/CRLF/length-cap gaps found; A.4's sanitization pipeline has a working precedent in this codebase (`REWORK_FEEDBACK` 4KB codepoint-aware truncation, extension.py ~L2180) and each failure class in AC-7 is independently unit-testable.

## Verdict

**REVISE** — 2 Critical + 2 Major. The Critical findings are not nitpicks: as currently specified, a literal implementation of C.1+C.2 (the qa OBJECTION ② fix) will make AC-1 (the single most important gate, per the Spec's own words) structurally unreachable via a state-machine routing conflict that neither the DEC's 4-agent review nor the current spec draft addresses. This must be resolved (concrete third outcome + exit-code mapping + Layer1 consumption logic, plus the companion AD-M1-4 doc amendment) before Phase B, or the 168h run will again produce 100% `S_FAIL` — just relabeled `container_crash` instead of regex `die`.
