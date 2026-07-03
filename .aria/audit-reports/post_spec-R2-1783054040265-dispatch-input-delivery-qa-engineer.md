---
checkpoint: post_spec
mode: convergence
round: 2
agent: qa-engineer
verdict: PASS
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783054040265
converged: false
---

# post_spec R2 (convergence) — qa-engineer — dispatch-input-delivery

**Verdict: PASS** (0 Critical / 0 Major, 3 non-blocking Minor observations). Vote: **PASS**.

Both R1 Critical findings (C-1 fetch-mode↔state-machine deadlock; C-2 AC-6 unimplementable) and the
R1 Major (M-4 compute-assertions call-site masking) are traced to landed spec text and cross-checked
against live code at `aria-orchestrator` HEAD `daf7c79` — same commit the spec cites, confirmed via
`git rev-parse HEAD`. I re-derived the fix mechanism line-by-line rather than trusting the spec's
self-report, and specifically hunted for a "fix reintroduces the same dead-end one level up" pattern
(the failure mode C-1 itself was: a naive empty-guard reproduces 100% S_FAIL in new clothing). Found
none. Mechanism is sound and every load-bearing precedent it depends on is real, not fictional.

---

## C-1 (Critical, R1) fetch-mode outcome ↔ state-machine deadlock — CLOSED, verified by trace

**Original defect** (confirmed still accurately described in spec, byte-checked):
- `initial.sh:591-596` — exit code is a strict function of `FINAL_OUTCOME`: `exit 0` iff `=="SUCCESS"`, else `exit 1`. No third state today.
- `initial.sh:524-536` — `FINAL_OUTCOME` is `SUCCESS` only under the AD-M1-4 5-AND (incl. `FILE_TOUCHED_HIT`/`DIFF_CONTAINS_HIT`).
- `extension.py:_handle_s5_await` (2593-2640, re-verified) routes purely on Nomad alloc `exit_code`: `==0 → S6_REVIEW`, `!=0 → S_FAIL(CONTAINER_CRASH)` unconditionally. `result.json` content is never read by this handler.
- `compute-assertions.sh:37-40` (re-verified, current line numbers 34-38 in the file as read) `die`s (exit 1) if `issue.yaml` absent — which it always is in fetch mode by design (A.2: always-fetch, no file written).

**Why a naive fix would have reproduced the deadlock** (this is what R1 actually objected to, and what I specifically re-checked did *not* happen in the revision): if the empty-list guard (C.1) were applied *only inside* `compute-assertions.sh`, and the call-site (`initial.sh:513-515`) still invoked it unconditionally, fetch mode has no `expected_changes` at all → `FILE_TOUCHED_HIT`/`DIFF_CONTAINS_HIT` can never be `"true"` → 5-AND always fails → `ASSERTION_MISMATCH` → `exit 1` → `S_FAIL(container_crash)`. Same terminal state as today, different proximate cause (misclassified crash instead of Step-1 regex `die`).

**Verified fix shape** (§What C.2 + C.3, TG-1.7/1.8/1.9):
1. C.2 mandates the call-site itself skip `compute-assertions.sh` entirely for `ARIA-`-prefixed (fetch) dispatches — wired at `initial.sh:513`, the exact call site, not just inside the sub-script. This decouples fetch mode from `FILE_TOUCHED_HIT`/`DIFF_CONTAINS_HIT` altogether; those variables are simply never consulted for fetch-mode outcome.
2. A **new, independent** terminal outcome `AUTONOMOUS_COMPLETED` (three conditions: `claude_exit==0 AND commit AND PR`) is defined and mapped to `exit 0`, which must be added to the `:526-536`/`:591-596` mapping as an explicit sibling branch to `SUCCESS`, not a value that flows through the 5-AND.
3. C.3 requires `AUTONOMOUS_COMPLETED` be written distinct from `SUCCESS` with `assertion_verified:false`, excluded from verified-SUCCESS corpus metrics — this is what prevents the fix from re-opening OBJECTION ② (any-commit=SUCCESS) while still letting the dispatch progress. Tracing forward: `S6_REVIEW` still runs an LLM code-review gate (`extension.py:_handle_s6_review`, confirmed present, "LLM review Layer 2 output (code quality + acceptance)") and `S7_HUMAN_GATE` still requires owner Feishu sign-off before actual merge (AD10) — so `AUTONOMOUS_COMPLETED`'s honesty label is not the *only* safety net against garbage reaching `S9_CLOSE`; there is a pre-existing review layer downstream that the spec doesn't cite but that materially reduces the blast radius of "unverified but exit-0'd." Worth noting in AD-M1-4 doc text but not a spec defect.

No path traced from this design back into the original dead-end. This is a genuine decoupling, not a relabeling.

## C-2 (Critical, R1) AC-6 unimplementable — CLOSED, precedents verified real

Re-verified every mechanism the fix depends on exists today, not just in spec prose:
- `get_alloc_logs()` precedent is **real and already consumed**: `alloc_status_provider.py:251` implements it; `extension.py:2716-2723` (`_spec_y_handle_redo_terminal`) already calls it via `hasattr()` Protocol-plus detection, exactly the pattern §What B.5 proposes reusing for `_handle_s5_await`'s `exit_code != 0` branch.
- `self._alloc_provider` (not `ctx.alloc_provider`) is directly in scope inside `_handle_s5_await` at the point the `CONTAINER_CRASH` branch currently fires (verified at `extension.py:2617-2632`) — the call site B.5 targets is reachable with no additional plumbing.
- The stderr-marker pattern has a live precedent: `redo.sh` echoes `[redo.sh] PASS ...` / `[redo.sh] FAIL ...` markers to stderr, parsed back via a dedicated extractor (`_extract_new_pr_id_from_logs`) on the Layer 1 side. A2/task 1.10's "emit stderr marker (cf. redo.sh precedent)" is not a hand-wave — it's citing a pattern that already ships.
- `FailReason` (`interfaces.py:67-90`) is confirmed a plain `str, Enum` with **no DB CHECK constraint** backing it (`schema.sql` only has self-documenting audit rows, e.g. `fail_reason_v3_additions`/`fail_reason_v4_additions`, not a hard constraint) — adding a 12th value (`INPUT_FETCH_FAILED`) is additive with zero migration risk, consistent with the documented "M3 9 + M4 2 additive, no implicit fallthrough" design.
- **Test double already exists** for exercising this exact fixture without touching real Nomad: `FakeAllocStatusProvider.set_logs()` / `get_alloc_logs()` (`interfaces.py` ~321-370) is purpose-built for "inject deterministic stderr content, assert routing." AC-6's fixture test (marker-present → `INPUT_FETCH_FAILED`; marker-absent → `CONTAINER_CRASH`) is directly buildable today with zero new test infrastructure.

This closes my R1 concern cleanly: the fix is not just "named," it is wired to real, reusable code paths that already exist in the codebase — recon-grounded per `[[feedback_recon_real_code_before_implementing_spec_test_suite]]`.

## M-4 (Major, R1) compute-assertions call-site masking — CLOSED

My R1 concern was specifically that a RED test exercising `compute-assertions.sh` in isolation could pass while the real `initial.sh` call site never reached the fixed logic (because `issue.yaml` never exists in fetch mode, so the standalone script would just `die` at its own file-existence guard before the empty-list fix logic runs). The revision resolves this by **removing the call entirely** for fetch mode (C.2, task 1.8, "wire the skip at `initial.sh:513`") rather than trying to make the sub-script tolerate a missing file — a cleaner fix than what I suggested in R1 (stub yaml vs. skip-and-inline; the spec chose skip-and-inline). AC-4a explicitly requires the RED test to exercise "the real `initial.sh` call-site... not just the script in isolation," which is the exact discipline that prevents the false-coverage trap I flagged. TG-1.7 (file-mode defense-in-depth) and TG-1.8 (fetch-mode skip) are now correctly split into two separate tasks instead of conflated.

---

## Non-blocking observations (Phase-B detail, does not affect PASS)

1. **[Minor][schema-consistency]** Adding `FailReason.INPUT_FETCH_FAILED` follows an established self-documenting convention in this codebase (`schema.sql` rows `fail_reason_v3_additions` for M4, `fail_reason_v4_additions` for M5) that TG-2.5/TG-5 don't mention continuing (e.g. a `fail_reason_v5_additions` row). Not a correctness gap (no DB constraint depends on it) — purely a documentation-pattern consistency nit for whoever executes TG-2.5.
2. **[Minor][observability]** `initial.sh`'s crash trap (`write_partial_result_json`, lines 65-96) unconditionally writes `outcome: "INFRA_FAILURE"` / `error.type: "crashed_before_result_write"` for *any* early exit, including a Step-2 fetch failure. Since `_handle_s5_await` never reads `result.json` (confirmed — it only reads Nomad alloc `exit_code`/logs), this doesn't affect AC-6's Layer-1-side routing correctness, but it means `result.json` itself would mislabel an `INPUT_FETCH_FAILED` case identically to any other early crash — worth a one-line trap update in Phase B for corpus-review readability, not required for AC-6 to pass.
3. **[Minor][test-infra sizing]** `compute-assertions.sh` has an existing fixture-matrix test harness (`docker/aria-runner/tests/compute-assertions/test.sh`, 7 fixtures). No equivalent harness exists today for `initial.sh` as a whole — AC-4a's "real call-site" requirement (which I demanded in R1 and is now correctly specified) will require Phase B to build new end-to-end test scaffolding for `initial.sh`, not just extend the existing compute-assertions fixtures. This is a real but appropriately-scoped Phase B lift; tasks.md doesn't call out the scaffolding effort explicitly, but Level 3 spec granularity doesn't require it — flagging for task-planner sizing awareness only.

None of the three rise to Major: none block AC-1/AC-4/AC-6 as specified, none reopen a corpus-poisoning or dead-end hazard, and none require Spec-level rework.

## Rationale for PASS

Both R1 Criticals are closed by a genuine architectural decoupling (fetch-mode outcome is now an
independent branch skipped-at-call-site, not a byproduct of the shared 5-AND), not a relabeling that
reintroduces the same dead-end — I specifically traced for that failure mode given it's exactly what
happened once already in this Spec's history (Step-1 regex `die` → misclassified `container_crash`
would have been the second incarnation had the naive fix landed). The R1 Major (call-site masking) is
closed by the stronger of the two remedies I offered in R1. Every code precedent the fixes lean on
(`get_alloc_logs`, `redo.sh` marker pattern, `FakeAllocStatusProvider.set_logs`, additive `FailReason`
enum with no DB constraint) is verified to exist in the actual codebase at the cited HEAD, not asserted
from spec prose alone. 0 Critical / 0 Major → PASS.
