---
checkpoint: post_spec
mode: convergence
round: 3
agent: backend-architect
verdict: PASS
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783055160721
converged: false
---

# R3 Convergence Review — backend-architect

## Vote: PASS (0 Critical, 0 Major)

## Scope of this round

R2 raised two Critical findings (both mine). This round re-verifies, against the live
codebase at `aria-orchestrator` HEAD `daf7c79` (matches the Spec's recon provenance
claim), whether the R2-revised `proposal.md`/`tasks.md` actually closes both gaps with a
real implementation path — not just improved prose.

## Critical A (corpus exclusion had no implementation path) — VERIFIED CLOSED

R2 claim: `assertion_verified:false` written to `result.json`, but (a) `result.json`
lives on a host-volume mount that is cross-node-unreadable, (b) `_handle_s5_await` never
reads it, and (c) sibling AC-2's `total_s9 = COUNT(*) WHERE state='S9_CLOSE'` cannot
distinguish `AUTONOMOUS_COMPLETED` from a verified `SUCCESS` — so the corpus-poisoning
problem (§Why item 3) would simply resurface at the acceptance layer.

Revised fix (§What B.6/C.3, AC-4c, TG-2.6/2.7): route the outcome class through the
stderr-marker channel Layer 1 already reads, persist it in the DB, make the acceptance
query outcome-class-aware. I checked each link:

- `get_alloc_logs()` is real and **already consumed today**, not just defined:
  `alloc_status_provider.py:251-281` implements it, and `extension.py:2716-2723`
  (`_spec_y_handle_redo_terminal`) already calls
  `alloc_provider.get_alloc_logs(...)` via a `hasattr` Protocol-plus check to parse the
  `redo.sh` `PASS new_pr_id=...` marker. This is a live, exercised precedent for
  "container writes stderr marker → Layer 1 greps it via this exact API" — not a novel,
  unproven mechanism.
- `_handle_s5_await` (`extension.py:2593-2640`) today genuinely reads **only**
  `exit_code` (`==0 → S6_REVIEW`, else `S_FAIL(CONTAINER_CRASH)` via the closed
  `FailReason` enum, `interfaces.py:67-94`, currently 11 values, no fetch/input
  variant) and never touches `result.json` — confirms the Spec's premise is accurate,
  not overstated.
- The `dispatch_audit_log.payload_json` route is real and precedented at the exact
  granularity needed: migration `004_schema_v4_additive.sql` creates the table with a
  `CHECK (event_type IN (...))` enum (8 fixed values, `state_transition` among them) but
  **no schema constraint on payload_json's internal fields** (only `json_valid`). The
  `#147 B4` `issue_type_hint` precedent (`db.py:622`, `extension.py` seed loop
  `audit_extra={"issue_type_hint": issue_type_hint}`) shows a new key added to an
  *existing* `state_transition` event's payload — exactly the pattern `outcome_class`
  would follow. This means writing `outcome_class` requires **no** new migration to the
  `event_type` CHECK enum (which would otherwise be a real SQLite table-rebuild cost) —
  it rides inside an already-permitted event's JSON blob.
- The acceptance-query side is concretely feasible, not hand-waved: I read
  `check-m6-e2e-acceptance.py`'s live AC-2 implementation — STEP 3's per-type
  stratification already does
  `JOIN dispatch_audit_log al ON al.dispatch_id = d.dispatch_id ... json_extract(al.payload_json, '$.issue_type_hint')`.
  Extending STEP 1's `total_s9` count with an analogous `NOT EXISTS (... json_extract(...,'$.outcome_class')='AUTONOMOUS_COMPLETED')`
  filter is a straightforward extension of an existing, working query shape — same table,
  same join key, same `json_extract` idiom.

No `result.json` dependency remains in the fix chain. The label is load-bearing at the
query Layer 1/Spec #2 actually run. **Critical A closes.**

## Critical B (B.3 vs D.1 contradiction; no persisted field for target_repo) — VERIFIED CLOSED

R2 claim: raw issue number as an independent field + "no migration" + "no composite
parsing" cannot all be true simultaneously, and `target_repo` had no persistence path at
all.

Revised fix (§What B.2/B.4, D.1 clarification, TG-2.1/2.4, AC-11/AC-12): additive nullable
columns (`raw_issue_number`/`target_repo`/`base_branch`/`files_hint`) via the established
`migrations/00N_schema_vN_additive.sql` pattern; `_handle_s4_launch` reads them from
`dispatch_row`; `ISSUE_URL` built from the persisted `raw_issue_number` + `target_repo`
(no parsing of the composite `issue_id`).

- The additive-migration precedent is **real and exact**: I read all three existing
  migrations (`002_schema_v2_additive.sql` M3, `003_schema_v3_additive.sql` M4,
  `004_schema_v4_additive.sql` M5) — each is a straight `ALTER TABLE dispatches ADD
  COLUMN` block (nullable or `NOT NULL DEFAULT`) + `schema_meta` self-doc + version bump,
  wrapped by a Python runner in a transaction. A `005_schema_v5_additive.sql` following
  this exact shape is not a new pattern being invented for this Spec — it is the fourth
  instance of an established one. The claim "M3 v2 / M4 v3 / M5 all added forensic
  columns this way" is accurate (verified line-by-line).
- The PK/index claim is confirmed: `schema.sql:245` `PRIMARY KEY (issue_id, dispatch_id)`
  + `schema.sql:273` `CREATE UNIQUE INDEX uq_issue_active_partial ON dispatches
  (issue_id)`. Adding nullable columns via `ALTER TABLE ADD COLUMN` touches neither the
  PK nor this index — D.1's "no key restructure" and B.2's "additive input columns" are
  not in tension; they operate on disjoint parts of the schema. This resolves the R2
  contradiction cleanly, not just rhetorically.
- `_handle_s4_launch` (`extension.py:2093-2170`) already reads `dispatch.get(...)` for
  several fields (`image_sha`, `rework_mode`) from `ctx.dispatch_row` — reading the new
  persisted columns the same way is consistent with the existing code shape, not a new
  access pattern.
- Current `ISSUE_URL` construction (`extension.py:2143-2152`, confirmed live) uses
  `forgejo_org`/`forgejo_repo` from env (`FORGEJO_ORG`/`FORGEJO_REPO`) and interpolates
  `issue_id` directly — confirms the Spec's diagnosis of the current bug is accurate.
  B.4's fix (build from persisted `raw_issue_number` + `target_repo`, no composite
  parsing) is a coherent replacement given B.2 now supplies those fields.
- AC-11's honesty check holds up: `_phase1_scan_and_seed` (`extension.py:1110`) does
  iterate a single `self._forgejo` client bound to one `FORGEJO_REPO`/`FORGEJO_ORG` via
  env — so "cross-repo dispatch deferred, single-repo seed pipeline" is an accurate
  self-report, not an evasion.

**Critical B closes.**

## New observation this round (Minor, non-blocking)

B.2's phrasing "the raw issue **number**, `target_repo`, `base_branch`, and `files_hint`
known at seed (`_phase1_scan_and_seed`)" overstates uniformity across the four fields.
Recon shows:
- `raw_issue_number` — genuinely available (`issue.get("number")` in the seed loop).
- `target_repo` — only available as the single hardcoded `FORGEJO_REPO` env constant
  (not per-issue derived); acceptable given AC-11's honest single-repo scoping, but not
  "known" in the same sense as the issue number.
- `base_branch` — **not computed anywhere today**. I grepped the full seed path and
  `forgejo_client.py`; the only `base_branch` references are a hardcoded `"master"`
  default parameter in PR-creation helpers, not a per-issue lookup. There is no existing
  Forgejo `default_branch` API call in Layer 1 at seed or elsewhere.
- `files_hint` — **does not exist anywhere in the codebase today** (`grep -rn
  "files_hint"` outside `openspec/` returns nothing); it has no analogue to derive from
  at seed for a real (non-fixture) issue.

This does not break the fix: `base_branch` has a stated container-side fallback (A.5,
Forgejo `default_branch` API) that is independent of whether Layer 1's persisted column
is populated, and `files_hint` is optional prompt context (not consumed by the
fetch-mode assertion path, which is skipped entirely per C.2) — so both fields degrading
to `NULL` at seed for the foreseeable future is architecturally tolerable, matching
AC-12's own "historical rows (NULL) degrade gracefully" clause extended to "not-yet-
computed fields." I am not raising this as blocking — it is a documentation-precision
nit (the wording implies parity across four fields that isn't there), worth a one-line
tightening in B.2 during Phase B write-up, but it does not reopen the B.3-vs-D.1
mechanism I flagged in R2, which is what closes here.

## No new Critical/Major introduced by the R2 rework

Checked specifically for regressions the schema-migration + dual-channel-outcome rework
could introduce:
- No collision: `outcome_class` / `raw_issue_number` / `target_repo` do not already
  exist as columns (grepped `schema.sql`/`db.py`/`extension.py` — only a same-named
  local variable in an unrelated function, no DB field).
- No `dispatch_audit_log.event_type` CHECK-enum migration is required (payload-JSON
  route sidesteps it, per Critical A analysis above).
- Migration numbering is consistent: current schema is v4.0 (004); a new v5.0 (005)
  additive migration is the correct next increment, no gap or renumbering conflict.
- `FailReason.INPUT_FETCH_FAILED` is a plain new enum member on a `TEXT` DB column
  (fail_reason is validated at the application layer per the M4/M5 precedent comment in
  `interfaces.py`/migration 004) — no SQL-level enum constraint to fight.

## Rationale for PASS

Both R2 Criticals are closed with mechanisms I independently traced through the live
`daf7c79` codebase, not just re-worded in the prose. The fixes reuse two real,
already-exercised precedents (the `redo.sh`/`get_alloc_logs` stderr-marker channel, and
the `#147 B4`/`issue_type_hint` audit-payload `json_extract` pattern) plus one
well-established precedent (the three prior additive schema migrations), rather than
inventing new unproven mechanisms. The one new observation (uneven "known at seed"
phrasing for `base_branch`/`files_hint`) is a wording-precision Minor with no functional
consequence given the stated fallbacks — it does not warrant another REVISE round.
