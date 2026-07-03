---
checkpoint: post_spec
mode: convergence
round: 2
agent: backend-architect
verdict: REVISE
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783054040265
converged: false
---

# post_spec R2 — aria-2.0-m6-dispatch-input-delivery (backend-architect)

## Scope of this review

R1 (round 1) landed 2 Major findings from this same lens (M1 ISSUE_URL construction, M2 R7
"64KB" factual inversion). This round: (a) verify both fixes actually landed in the revised
`proposal.md`/`tasks.md` against `aria-orchestrator` HEAD `daf7c79`; (b) audit the reworked
three-outcome model (§What C) and the new B.5/AC-11 material — introduced as R1 fixes for
*other* agents' findings (qa's Critical state-machine-routing concern) — for self-consistency
and fix-introduced regressions, per the parent brief's explicit ask ("这真能防污染").

## Part 1 — R1 fix verification (M1, M2)

### M1 (ISSUE_URL) — ✅ landed, verified against code

- §What B.3 now states the current-state facts precisely and they check out against `daf7c79`:
  `issue_id = str(issue.get("id") or issue.get("number") or "")` at **`extension.py:1176`**
  (exact); `forgejo_org`/`forgejo_repo` hardcoded from env at **`extension.py:2147-2148`**
  (exact); `issue_url = f"...{forgejo_org}/{forgejo_repo}/issues/{issue_id}"` at
  **`extension.py:2149-2151`** (exact, spec cites 2149-2152 — one-line-off but same statement).
- The fix direction (retain raw number as a field distinct from the composite `issue_id`; build
  `ISSUE_URL` from `{target_repo}/issues/{raw_number}`) is now an explicit AC (**AC-11**, with a
  non-`id==number` / non-Aria-repo verification requirement) and an explicit task (**TG-2.3**).
  This closes the R1 gap where the fix was hedged as "re-verify."
- `head_branch = f"aria/{issue_id}"` at **`extension.py:2989`** (exact) — B.4's unify claim holds.
- **However**, this fix's *feasibility* has a new problem — see Part 2, Finding A below.

### M2 (R7 "64KB") — ✅ landed, verified against code

- `docs/m0-report.md` §1.2 confirmed: real ceiling is Linux `MAX_ARG_STRLEN` = 128 KiB, R7
  explicitly *debunks* the old "64 KB" figure, cap applied is `META_VALUE_CAP_BYTES = 100 * 1024`
  (`prompt_render.py:42`, exact).
- The revised Alternatives-table row for `C-meta` no longer cites "64KB" as the rejection
  reason; it now reads: "*the real ceiling is Linux `MAX_ARG_STRLEN` 128 KiB — R7 ... **debunked**
  the old '64 KB' myth) + content double-write. (C' metadata fields are tiny, so no cap concern;
  C-meta rejected on double-write + unbounded-body grounds, not the debunked number.)*" — this is
  the correct framing (rejection ground is double-write, not the disproven number).
- §Prerequisite Verification's "Additional code facts" paragraph mirrors the same correct framing.
- Both landed cleanly with no new factual errors introduced. **M2: fully resolved, no residual
  concern.**

## Part 2 — New findings (three-outcome model rework, self-consistency)

The parent brief specifically asked to verify whether the reworked three-outcome model's
`assertion_verified:false` / "excluded from any verified-SUCCESS corpus metric" claim (§What C.3)
actually holds, and whether the B.3 fix is internally consistent with D.1's data-model constraint.
Both trace to real gaps, verified against code — not speculative.

### [CRITICAL][data-model:corpus-persistence] `assertion_verified:false` never reaches any DB-queryable location — the sibling Spec's AC-2 gate cannot distinguish `AUTONOMOUS_COMPLETED` from verified `SUCCESS`, reproducing OBJECTION ② one layer up

**Verified mechanism**:

1. `result.json` (which carries the new `outcome`/`assertion_verified` fields per C.2/C.3) is
   written to `OUTPUTS_DIR="${ARIA_OUTPUTS_DIR:-/opt/aria-outputs}"` (`initial.sh:33,108`) — a
   Nomad **host-volume bind mount**, same category of storage the input-delivery problem (§Why,
   this Spec's own root cause) is fixing on the *input* side.
2. This codebase already documents, twice, in its own words, that host-volume bind mounts are
   **not cross-node reachable** via the Nomad filesystem API: `alloc_status_provider.py:259-261`
   ("Layer 2 writes result.json into a Nomad host volume mount that is NOT reachable via the
   standard `/v1/client/fs/cat` API across nodes") and `extension.py:106-108` (identical wording,
   Spec Y T3.1 precedent). That is *why* `new_pr_id` is read via a stderr marker + `get_alloc_logs()`
   instead of reading `result.json` directly — the established pattern this Spec claims to follow
   (§Why: "the existing codebase already solved the output side ... with a node-agnostic channel").
3. Confirmed via code: `_handle_s5_await` (`extension.py:2596-2599`) reads **only** the Nomad
   `exit_code`; the comment states outright: *"result_path is NOT persisted: _handle_s6_review
   reads pr_diff/commit_message/acceptance_criteria from dispatch_row, not result_path; no
   downstream consumer exists. Schema lacks the column, so writing it would raise
   OperationalError."* Grepping the entire `aria_layer1` package for `assertion_verified` or
   `AUTONOMOUS_COMPLETED` returns zero hits — nothing reads these fields today, and no task in
   TG-1/TG-2/TG-3 adds a consumer or a persistence column for them.
4. The one DB-queryable acceptance gate that actually counts terminal dispatch outcomes today is
   the **sibling Spec's** (`aria-2.0-m6-e2e-resilience`) `acceptance/check-m6-e2e-acceptance.py`
   **AC-2**: `total_s9 = SELECT COUNT(*) FROM dispatches WHERE state = 'S9_CLOSE' AND
   state_entered_at BETWEEN :start AND :end` (lines ~222-226), gating on `total_s9 >=
   _MIN_DISPATCHES` (≥10) plus per-type stratification via `dispatch_audit_log` `json_extract`
   (issue_type_hint only — no assertion/outcome key). **`state` is the only signal; there is no
   `assertion_verified` column anywhere for this query to filter on.**
5. Per C.2, `AUTONOMOUS_COMPLETED → exit 0`, which — via the unmodified `_handle_s5_await`
   exit_code==0 branch — advances the dispatch to `S6_REVIEW` and, on the existing happy path,
   eventually to `S9_CLOSE`, **identically to a genuinely diff-verified `SUCCESS` dispatch**.

**Conclusion**: every `AUTONOMOUS_COMPLETED` (unverified) dispatch that reaches `S9_CLOSE` will be
counted by AC-2's `total_s9` threshold and stratification exactly like a verified `SUCCESS`
dispatch, because the one bit that distinguishes them (`assertion_verified`) is stranded in an
ephemeral/host-volume-only file that nothing in this codebase — by its own documented,
double-precedented constraint — can read cross-node. C.3's claim ("excluded from any
'verified-SUCCESS' corpus metric... prevents corpus poisoning ②") is **not backed by any
mechanism**; as specified, it is aspirational text with no implementation path. This is exactly
the corpus-poisoning hazard (qa's original OBJECTION ②, and this Spec's own stated raison d'être
per §Why point 3) reincarnated one layer higher — at the acceptance-query layer instead of the
`compute-assertions.sh` layer — and neither R1 round caught it (R1's qa Critical-1 was about
*reaching* S9_CLOSE at all, not about what happens to the acceptance corpus once there).

Note: the proposal's own parenthetical in C.3 ("AC-5 scores humanized-command quality by owner,
not assertions, so an unverified-but-completed dispatch is a valid AC-5 corpus member") is
correct **for AC-5** (confirmed: `evals/m6-prompt-quality/README.md` — the humanized-command
corpus is populated from dispatched *command text*, unrelated to `assertion_verified`) — but the
author appears to have reasoned only about AC-5 and missed **AC-2**, which is the actual
`state`-keyed corpus-count gate this Spec's §Why explicitly worries about ("false-green cycles
that silently pollute the AC-5/AC-6 corpus" — AC-2's stratified S9_CLOSE count is the corpus).

**Fix**: either (a) add a node-agnostic channel (stderr marker, mirroring the `redo.sh`
precedent this Spec already cites) so `_handle_s5_await` can persist `assertion_verified` into
`dispatch_audit_log.payload_json` at the S5→S6 transition (giving AC-2 a `json_extract` filter
to exclude `assertion_verified=false` rows, symmetric to how `issue_type_hint` already flows),
or (b) explicitly amend the sibling Spec's AC-2 acceptance gate (with its own doc-sync task) to
exclude unverified dispatches, or (c) if neither is in scope, honestly narrow C.3's claim to "not
silently mislabeled as diff-verified" (true) rather than "excluded from any corpus metric"
(currently false), and open a tracked follow-up. Given this Spec's own stated purpose is
preventing corpus pollution, silently leaving this gap unacknowledged is not acceptable — but
explicitly scoping it out (like the Telemetry Spec dependency edge already does) would be.

---

### [CRITICAL][data-model:B.3-D.1 contradiction] B.3's "raw number retained as a separate field, not parsed back out of composite `issue_id`" has no field to be retained in — D.1 explicitly rules out new columns, and `_handle_s4_launch` only has `dispatch_row`

**Verified mechanism**:

1. B.3 (the R1 fix for M1) now reads: *"Fix: retain the raw issue **number** as a separate field
   (not parsed back out of the composite `issue_id`)."* This is stated as a settled decision.
2. D.1 (unrelated recon-correction, untouched by the R1 round) states: *"the schema already
   stores `issue_id` as a single `TEXT` column ... The '(repo, number) composite' is achieved by
   embedding repo+number into the `issue_id` string value — **no structural column migration**."*
3. Confirmed via code: `_handle_s4_launch` — the exact call site B.3/TG-2.3 targets — reads
   `issue_id = ctx.dispatch_row.get("issue_id", "")` (`extension.py:2108`). It has **no** access
   to the original Forgejo `issue` dict (that only exists inside `_phase1_scan_and_seed`, a
   separate tick/function). `ctx.dispatch_row` is a DB row; confirmed via `grep` that
   `schema.sql` has **no** `issue_number`/`raw_number`/`forgejo_number` column anywhere.
4. Given (2) and (3): by the time `_handle_s4_launch` runs, the *only* way to obtain the raw
   number is to parse it out of the composite `issue_id` string — which is precisely what B.3
   explicitly forbids ("not parsed back out"). There is no third option under the current data
   model. This is not a hypothetical edge case; it is the literal, only call site B.3 targets.
5. This directly reproduces qa's **R1 MAJOR-3 finding** ("does not specify how the plain number
   is recovered ... parsing back from the string is the only available path and needs an
   explicit helper + unit test") — except the revised text now makes it *worse*: R1's draft at
   least hedged ("re-verify"); the R1 fix asserts a specific mechanism ("retain separately, don't
   parse") that is unimplementable without either (a) adding a genuinely new DB column (which
   would need its own TG-3 migration task — none exists) or (b) contradicting itself by parsing
   the string after all.
6. Compounding: **`target_repo`** has the identical problem in miniature, though lower severity —
   confirmed via `grep` that `target_repo` does not exist as a persisted field *anywhere* in this
   codebase today; every consumer (`comment_poll_runner.py`, `forgejo_client.py`,
   `extension.py` ×3, `reconcile_runner.py`) derives it from the single global `FORGEJO_REPO` env
   var. `_phase1_scan_and_seed` scans exactly one repo via one `ForgejoCliClient` instance — there
   is no multi-repo scan loop. This means `target_repo` *can* legitimately be re-read from env at
   `_handle_s4_launch` time with no new persistence (materially lower risk than raw_number, since
   it's a tick-constant, not per-dispatch data) — but it also means **AC-11's requirement to
   verify "a non-Aria `target_repo`"** is untestable against the real scan pipeline as it exists
   today (would require a synthetic/mocked dispatch_row, which is fine for a unit test but should
   be stated explicitly rather than implied as an E2E-verifiable case).

**Fix**: TG-3 needs an explicit task to add whatever field(s) actually carry `raw_number`
(and, if genuine multi-repo dispatch is intended beyond the single-scan-repo today, `target_repo`)
from seed-time to `_handle_s4_launch`-time — e.g., a new `dispatches` column (this does **not**
contradict D.1, which only forbids restructuring the `issue_id` column itself, not adding an
unrelated new column) — with its own migration entry in D.2's survey. Until that lands, B.3's
"not parsed back out" clause is aspirational, not implementable, and Phase B will hit exactly the
ambiguity qa flagged in R1.

## Part 3 — Other R2-scope checks (no new issues)

- **Retry/backoff contract (A.3)**: no existing curl-retry precedent in `initial.sh` (existing
  `curl` calls at `:396`, `:485` are single-shot), but the classified bounded-exponential-backoff
  contract is a standard, implementable bash pattern — feasible as specified, no blocking concern.
- **B.5 (`FailReason.INPUT_FETCH_FAILED`) exit_code routing**: self-consistent with C.2 —
  `AUTONOMOUS_COMPLETED` maps to `exit 0` (routes through the existing `exit_code==0 → S6_REVIEW`
  branch, untouched), so it never enters the `exit_code != 0` branch B.5 modifies. No collision
  between the "happy" and "failure" three-outcome branches.
- **AC-8 / D.2 (issue_id-keyed query survey)**: re-confirmed `check-m6-e2e-acceptance.py` AC-2's
  `json_extract('$.issue_type_hint')` path has zero `issue_id`-keyed joins (matches R1
  confirmed-accurate finding) — D.2's narrower-impact claim still holds independent of the two
  findings above (those concern `state`/new-field gaps, not `issue_id`-keyed queries).

## Verdict

**REVISE** — M1 and M2 (this agent's own R1 findings) are cleanly and correctly landed with no
residual concern. However, deeper verification of the *other* R1 round's fix (the reworked
three-outcome model, requested explicitly by the parent brief) surfaces **2 new Critical findings**
neither R1 round caught: (1) the corpus-exclusion mechanism in C.3 has no implementation path
given this codebase's own documented cross-node bind-mount constraint, and directly threatens
this Spec's own stated purpose (AC-2 corpus integrity); (2) B.3's fix, while directionally correct,
asserts an infeasible retention mechanism given D.1's schema constraint and the confirmed
`_handle_s4_launch` data-flow (dispatch_row-only, no access to seed-time `issue` dict). Both are
grounded in direct code recon (not speculative) and both are load-bearing for Phase B — an
implementer following the current text would hit an unresolved contradiction on the first (Finding
B) or ship a corpus-integrity regression indistinguishable from the exact bug this Spec exists to
fix (Finding A).
