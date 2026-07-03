---
checkpoint: post_spec
mode: convergence
round: 3
agent: qa-engineer
verdict: PASS
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783055160721
converged: false
---

# post_spec R3 (convergence) — qa-engineer — dispatch-input-delivery

**Verdict: PASS** (0 Critical / 0 Major, 1 Important non-blocking finding, 1 Minor non-blocking
observation). Vote: **PASS**.

This round's revision responds to backend-architect's R2 two Criticals (A: `assertion_verified`
stranded on cross-node-unreadable `result.json`, never reaching AC-2's DB query; B: B.3's "retain
raw number separately" had no field to retain it in, given D.1's no-key-restructure constraint and
`_handle_s4_launch`'s `dispatch_row`-only access). My mandate this round: confirm the DB-persistence
redesign actually closes both without reopening my own R1/R2 concerns (fetch-mode↔state-machine
deadlock, empty-`expected_changes` false-green) in a new form. Re-verified against `aria-orchestrator`
HEAD `daf7c79` (confirmed via `git rev-parse HEAD`) — same commit the spec cites.

---

## Critical A fix (outcome_class DB persistence) — verified real, not aspirational

Traced the full mechanism against live code, not spec prose:

- `SELECT * FROM dispatches ...` is the universal row-fetch pattern (`db.py:339,353,364,389,411,431,1026,1147`) — confirmed `_handle_s4_launch`'s `ctx.dispatch_row` and any future S5/S6 handler reading a dispatch row would automatically see new additive columns with zero query-list edits. B.2's additive-column claim is mechanically sound.
- Additive-migration precedent is real, not invoked loosely: `migrations/002_schema_v2_additive.sql`, `003_schema_v3_additive.sql`, `004_schema_v4_additive.sql` all exist and follow the exact `ALTER TABLE dispatches ADD COLUMN ... ` (nullable) pattern the spec cites (M3/M4/M5 precedent, confirmed by reading `004`'s header comment listing 5 additive columns + a new table).
- `dispatch_audit_log` is confirmed **INSERT-only** (`audit_no_update`/`audit_no_delete` triggers per `004`'s own header) with a working `payload_json` write path (`db.py:1324-1339`) and an established `json_extract` read-back precedent the sibling acceptance script already uses for `issue_type_hint` (`check-m6-e2e-acceptance.py:246-258`, confirmed live: `json_extract(al.payload_json, '$.issue_type_hint')`). C.3/B.6's "reuse the #147 B4 pattern" is citing a mechanism that ships today, not a hoped-for one.
- The sibling's AC-2 gate is confirmed **exactly** as backend-architect described: `total_s9 = SELECT COUNT(*) FROM dispatches WHERE state = 'S9_CLOSE' AND state_entered_at BETWEEN :start AND :end` (`check-m6-e2e-acceptance.py:222-227`), with **zero** `outcome_class`/`assertion_verified` filter today. TG-2.7 targets a real, currently-unguarded gate — not a straw man — and the fix shape (mirror the existing `issue_type_hint` `json_extract` join pattern already at lines 246-258) is directly analogous to code that already exists in the same file. This is the correct, minimal-risk fix.
- Precedent for writing an audit event from inside a terminal S5_AWAIT branch already exists: `_spec_y_handle_redo_terminal` (called from the `exit_code==0` branch, `extension.py:2617` region) already emits its own `state_transition` audit row before the S6_REVIEW transition returns — B.6's proposed outcome_class write slots into the same call site with a live precedent, not a novel injection point.

**Conclusion**: Critical A's fix mechanism is grounded in real, exercised code paths at every step
(row-fetch, migration pattern, audit-log write, json_extract read-back, sibling query location).
This is not the "aspirational text with no implementation path" backend-architect correctly flagged
in R2 — it now has one.

## Critical B fix (raw_issue_number / target_repo persistence) — verified real, resolves the D.1 tension

- `_phase1_scan_and_seed` (`extension.py:1110+`) is confirmed to hold the full Forgejo `issue` dict at seed time (`issue.get("id")`, `issue.get("number")`, `issue.get("labels")` all read in the function body I inspected) — exactly what B.2 needs to persist `raw_issue_number` as an additive column. This closes backend-architect's Critical B: the raw number now has a real column to land in, written at the point where the data is actually available, read later via the same `SELECT *`/`dispatch_row` mechanism `_handle_s4_launch` already uses. No parsing of the composite `issue_id` is required — B.3's "not parsed back out" clause is now implementable as stated.
- D.1's clarification ("no key restructure ≠ no additive columns") is the correct, minimal resolution — it does not contradict itself; `issue_id`'s `TEXT` column + partial-unique index is untouched, while `raw_issue_number`/`target_repo`/`base_branch`/`files_hint` are unrelated new columns. I re-confirmed via `grep` that `schema.sql`'s composite-key structure and B.2's additive columns are orthogonal (no column-name collision, no index dependency change).
- `target_repo`'s "lower severity, can legitimately re-read from env" carve-out (backend-architect Part 2 finding 6) is preserved unmodified in this revision and not contradicted by adding it as a column anyway (B.2 still adds `target_repo` as a persisted column for uniformity/future multi-repo — consistent, not redundant, since seed-time-persisted-then-read is strictly more robust than re-reading env at S4 time if env ever changes tick-to-tick).

## No new deadlock — verified via the generic exception wrapper

I specifically re-checked whether adding a marker-read step to the `exit_code==0` branch (a
previously trivial `return (S6_REVIEW, {})`) could stall a dispatch in `S5_AWAIT` if the read throws.
It cannot silently hang: the per-dispatch tick loop wraps each handler call in a broad
`try/except Exception` that calls `repo.mark_failed(..., reason=FailReason.OTHER, ...)` on any
unhandled exception (confirmed in the tick loop body, same function that calls `_phase1_scan_and_seed`
and the S-state handlers). Worst case for a marker-read bug is a dispatch failing outright (reliability
regression), not an infinite S5_AWAIT loop — the deadlock failure mode I was specifically primed to
re-check does not reappear in this revision.

## No false-green reopened at the mechanism level — confirmed, with one residual gap (see Important finding)

C.2's skip-the-assertion-script-entirely design for fetch mode (my R2 C-1/M-4 closure) is untouched
by this round's changes — B.6/C.3 only add a *persistence* step downstream of the already-decided
`AUTONOMOUS_COMPLETED`/`SUCCESS` classification, they do not touch how that classification is computed.
I re-confirmed no new code path lets `compute-assertions.sh`'s empty-list defaults leak back into fetch
mode. That part of the false-green fix remains sound.

---

## Important (non-blocking) — undefined fallback when the exit_code==0 marker is absent/malformed

§What B.6 and TG-2.6 specify a **binary** discrimination on `exit_code==0`: read the marker,
classify as `AUTONOMOUS_COMPLETED` or `SUCCESS`. Neither the spec text nor the task list states what
happens if the marker is **absent, truncated, or unparseable** on this branch (as opposed to the
`exit_code!=0` branch, where AC-6 already pins the fallback explicitly: marker-present →
`INPUT_FETCH_FAILED`, marker-absent → `CONTAINER_CRASH`).

This matters specifically for the concern this whole round exists to close: **if an implementer's
natural default is "no explicit AUTONOMOUS_COMPLETED marker found → treat as (legacy) SUCCESS"** —
which is the path of least resistance, since it reproduces pre-fix behavior (`exit_code==0` always
meant `SUCCESS`) — then any dispatch whose marker write is skipped, truncated, or lost (e.g. Nomad
log buffer truncation under load, a transiently-stale container image during the TG-1→TG-4 rollout
window, or a `get_alloc_logs()` call that returns empty rather than raising) would silently
re-enter the verified-SUCCESS corpus. That is OBJECTION ② reincarnated a *third* time — smaller in
probability than the original 100%-rate bug (post-freeze, the container should always emit the
marker on success per task 1.10), but the failure mode is structurally identical: an unlabeled gap
defaults to the wrong side of the "verified" line.

Contrast with the `exit_code!=0` branch, where I confirmed in R2 (and re-confirm here) that
`FakeAllocStatusProvider.set_logs()` gives a ready-built fixture for exactly this ambiguity and AC-6
already requires testing both the marker-present and marker-absent cases. No equivalent AC/task
requires the analogous fixture pair (marker-clear-SUCCESS / marker-clear-AUTONOMOUS_COMPLETED /
marker-absent-or-malformed) on the success branch.

**Recommendation** (does not block R3 convergence, should land before Phase B task-planning
finalizes TG-2.6's detail): explicitly state in TG-2.6 (or a clarifying line in §What B.6) that a
missing/malformed outcome-class marker on `exit_code==0` must **fail closed** — i.e. must **not**
default to `SUCCESS` — e.g. persist as `outcome_class=NULL`/`UNKNOWN` and have TG-2.7's acceptance
query treat `NULL`/`UNKNOWN` the same as `AUTONOMOUS_COMPLETED` for corpus-exclusion purposes
(excluded from verified-SUCCESS, not silently counted). Add a corresponding fixture case to AC-4's
test matrix. This is a one-line spec clarification + one extra fixture test, not a design rework —
consistent in scope with the kind of gap R1/R2 closed at Phase-A granularity.

## Minor (non-blocking) — carried forward from R2, still open

R2's Minor #1 (schema-consistency: `fail_reason_v5_additions` self-documenting row for the new
`INPUT_FETCH_FAILED` enum value, mirroring `fail_reason_v3_additions`/`fail_reason_v4_additions`) and
Minor #2 (`result.json` crash-trap mislabeling `INPUT_FETCH_FAILED` as generic `INFRA_FAILURE`) remain
unaddressed by this round's text — expected, since this round's scope was narrowly the two Criticals.
Re-flagging only so they aren't lost by Phase B; neither blocks R3.

---

## Rationale for PASS

Both R2 Criticals are closed by mechanisms I traced end-to-end against live code, not spec
self-report: Critical A's `outcome_class` now has a real DB-queryable landing spot
(additive column or `dispatch_audit_log` payload, both with working precedent in this codebase) and
a real, currently-unguarded consumer to fix (`check-m6-e2e-acceptance.py`'s `total_s9` query,
confirmed by reading it). Critical B's raw-number retention now has a real field to retain it in
(seed-time additive columns, written where the data actually exists, read via the pre-existing
`SELECT *`/`dispatch_row` pattern), resolving the D.1 tension without contradicting D.1's
no-key-restructure constraint. Neither fix reopens my R1/R2 deadlock or false-green concerns at the
*classification-logic* level (C.2's skip-the-assertion-script design is untouched). I found one
genuine gap the new *persistence* layer introduces — an unspecified fail-open/fail-closed choice for
marker-absent-on-success — but it is a bounded, low-probability edge case with an existing test
fixture pattern to extend, not a structural contradiction on the order of the two Criticals this
round fixed. It does not block convergence; it should be locked down as a one-line clarification
before Phase B implements TG-2.6. 0 Critical / 0 Major → **PASS**.
