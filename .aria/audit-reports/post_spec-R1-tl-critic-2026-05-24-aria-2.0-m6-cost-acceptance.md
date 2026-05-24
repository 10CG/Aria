# Post_Spec R1 Audit — tech-lead-critic — aria-2.0-m6-cost-acceptance

> **Auditor**: tech-lead-critic
> **Round**: R1 (Phase A.2 post_spec)
> **Spec**: aria-2.0-m6-cost-acceptance (Spec #1 of M6 four sub-Specs)
> **Spec status at audit time**: Draft (commit 6e58b75)
> **Audit timestamp**: 2026-05-24T12:31:21Z
> **DEC reference**: DEC-20260524-001
> **Verdict**: **NEEDS_FIX**

## Summary

Spec is structurally coherent and binary-falsifiable; AC vector (9 items) is genuinely
verifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`. However, R1 surfaces
**3 Critical** structural defects that block Phase B as written: (1) `validate-m6-handoff.py`
grep targets in tasks T5.2–T5.6 reference incorrect file paths (`extension.py` plain instead of
`hermes-extensions/aria-layer1/aria_layer1/extension.py`) — the script will silently grep nothing
and return PASS on a missing file, defeating the abi_compat enforcement gate; (2) the SQL
filter design for `metered_usd.cost_usd` does not specify how Zhipu rows are identified — the
dispatches table has no `provider` column, only `provider_cost_model` (M2 T10 schema reality);
the Spec's "WHERE provider='zhipu'" prose query is non-executable as written; (3) AC-3 evidence
clause contradicts production reality (`token_cost_usd=0.0` IS stored for Luxeno per
db.py:1054 contract; the Spec's claim "the existing schema does not store Luxeno per-dispatch
cost as 0" is factually wrong). These are concrete code-grounded errors, not stylistic
quibbles. Plus 5 Important findings (config.json location ambiguity, helper-without-caller
risk on cost_measurement_method field, P-15 DAG cross-Spec gating under-specified, freshness_ts
ISO format under-specified, T7.1 PRD verify mis-scoped). Effort baseline ~10h is credible.

## Findings

### Critical

- **C-tl-1**: validate-m6-handoff.py grep targets cite **wrong file paths** — tasks T5.2–T5.6
  will produce silent false PASS.
  - Location: `tasks.md` T5.2 ("grep `schema.sql`"), T5.3 ("grep `extension.py`"), T5.4
    ("grep `reconciler.py`"), T5.5 ("grep `comment_poll.py`"), T5.6 ("grep
    dispatcher/db INSERT path"); `proposal.md` §What F lines 159–166.
  - Why critical: The canonical files live at
    `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/{schema.sql, extension.py,
    reconciler.py, comment_poll.py, db.py}` and migrations at
    `…/aria_layer1/migrations/004_schema_v4_additive.sql`. The sibling `validate-m5-handoff.py`
    correctly resolves these via `REPO_ROOT / "hermes-extensions" / "aria-layer1" /
    "aria_layer1"` (verified at `docs/validate-m5-handoff.py` lines 40–55). Spec #1 tasks
    citing the bare basenames will lead the Phase B implementer to either (a) glob
    repo-wide (false positives — `extension.py` exists in plugins, samples, archives) or
    (b) `Path("extension.py")` relative (file not found → grep returns 0 matches → check
    treats absence as PASS by misinterpretation). Without explicit canonical paths, a
    PASS result is not evidence of abi_compat compliance — it is evidence the grep target
    was wrong, exactly the failure mode `[[feedback_validator_repo_drift_guard_test]]`
    warns against.
  - Suggested fix: Edit `proposal.md` §What F and `tasks.md` T5.2–T5.6 to cite the full
    canonical paths verbatim: `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/
    schema.sql`, `…/extension.py`, `…/reconciler.py`, `…/comment_poll.py`,
    `…/migrations/004_schema_v4_additive.sql`. Mirror the path-construction pattern from
    `validate-m5-handoff.py` lines 40–55. Add T5.9 explicit clause: the canonical
    instance test MUST fail (exit non-zero) when any of the 5 target files is missing
    OR contains 0 matches for its specific regex — the test must distinguish "file
    absent" from "file present + literal absent" to avoid the silent-PASS path.

- **C-tl-2**: Zhipu cost aggregation SQL has **no provider filter column** — query is
  non-executable as written.
  - Location: `proposal.md` §How "Technical approach" lines 209–211 (`SQLite SUM WHERE
    provider='zhipu' AND created_at > now-30d`); `tasks.md` T1.1 ("query SQLite dispatches
    table `SUM(token_cost_usd)` WHERE provider column identifies Zhipu-routed rows");
    `tasks.md` T1.2 (dual-row schema spec, refers to `provider`).
  - Why critical: The actual `dispatches` schema (verified at
    `hermes-extensions/aria-layer1/aria_layer1/schema.sql` lines 56–140) has NO `provider`
    column. The closest column is `provider_cost_model` (added by migration
    `002_schema_v2_additive.sql`), which holds `subscription_flat` (Luxeno) or
    `metered` (Zhipu) — NOT the literal string `zhipu`. The other potential filter is
    `model_used` (lines 102, holds `glm-4.7-air` / `glm-4.7-flashx` for Luxeno OR Zhipu
    indistinguishably depending on routing). The Spec assumes a column that does not
    exist. Phase B will either (a) discover this during T1.1 and stall pending a
    cross-Spec decision, or (b) silently invent a wrong filter (e.g. `model_used LIKE
    'glm-%'` which matches both providers) — false metered_usd values would flow into
    cost.json and feed the 80% alarm gate. This is the
    `[[feedback_scaffold_helpers_drift_without_callers]]` pattern in reverse: a caller
    designed without verifying the column its SQL depends on.
  - Suggested fix: Two options, both require Spec edit before Phase B:
    1. **Filter by `provider_cost_model = 'metered'`** (preferred — already populated
       per M2 T10 contract at db.py:1062). Add this exact predicate to proposal.md
       §How technical-approach block and tasks.md T1.1. Document in §What A field
       semantics that Zhipu attribution is computed via `provider_cost_model='metered'`,
       with one-paragraph rationale + code reference to db.py update_token_usage
       lines 1054–1080.
    2. **Add `provider` column via Spec scope expansion** — rejected; this expands
       scope beyond DEC §2 Spec #1 ("no schema migration needed") and conflicts with
       OOS-7. Option 1 is correct.

- **C-tl-3**: AC-3 evidence clause **contradicts production reality** — Luxeno rows DO
  store `token_cost_usd=0.0` (not NULL).
  - Location: `proposal.md` AC-3 lines 304–306 ("`SELECT COUNT(*) FROM dispatches WHERE
    provider = 'luxeno' AND token_cost_usd IS NULL` produces a row count ≥ 0 without
    error … confirming the existing schema does not store Luxeno per-dispatch cost as 0").
  - Why critical: Verified at `hermes-extensions/aria-layer1/aria_layer1/db.py` line 1026
    docstring ("For Luxeno calls, callers SHOULD pass cost_usd=0.0") and
    `token_tracking.py` lines 5, 156. `token_cost_usd` is declared `REAL NOT NULL DEFAULT
    0.0` in schema.sql line 101 — it CANNOT be NULL. Every Luxeno row has
    `token_cost_usd=0.0` literal, exactly the failure mode AC-3 is supposed to prevent
    in cost.json. AC-3 as written would silently FAIL on any production DB (no NULL rows
    exist to count), which means Phase B would either (a) chase a phantom bug, or (b)
    rewrite AC-3 mid-implementation — exactly the
    `[[feedback_test_mock_pattern_hides_prod_bug]]` anti-pattern (Spec contract diverges
    from prod data shape). This also undermines the §Why narrative ("Attributing
    `cost_usd=0` per dispatch is a silent false-positive" line 32) — the existing
    dispatches table already does exactly this, and that is the actual condition the
    cost.json null-guard is defending against, not preventing.
  - Suggested fix: Rewrite AC-3 to verify the **cost.json output** has Luxeno
    `cost_usd: null`, NOT verify dispatches table semantics. Specifically: split AC-3
    into AC-3a (cost.json subscription_usd.cost_usd is None — already covered in AC-2,
    so could fold) and AC-3b (the cron alarm logic skips Luxeno when `cost_usd is None`
    — covered by T3.5 unit test). Remove the SQL verification clause entirely (it
    cannot pass against prod data and reflects misunderstanding of M2 T10 contract).
    Update §Why narrative to read "the existing dispatches.token_cost_usd column
    contains 0.0 for Luxeno rows by M2 T10 contract; merging these into cost.json
    metered_usd would understate metered cost and create the Luxeno=0 silent-false-
    positive failure mode" — this is the truthful framing.

### Important

- **I-tl-1**: `.aria/config.json` **physical location not disambiguated** — root project
  vs aria-orchestrator submodule.
  - Location: `proposal.md` §What B line 108, §Dependencies row "`.aria/config.json`
    existing structure"; `tasks.md` T2.1.
  - Why important: Two `.aria/config.json` files could plausibly exist:
    `/home/dev/Aria/.aria/config.json` (verified present, project-root) and
    `aria-orchestrator/.aria/...` (no such file currently). The snapshot script and
    cron sentinel will run from a Nomad alloc context where `cwd` is unclear; the Spec
    does not specify whether it reads root-project `.aria/config.json` (which currently
    has `state_scanner`, `issue_scan`, etc.) or expects a new `aria-orchestrator/.aria/
    config.json`. If the cron extends `aria-layer1-cron`, that nomad job has its own
    workdir convention. Spec needs explicit absolute path (or `${ARIA_CONFIG_PATH}` env
    var with default).
  - Suggested fix: §What B opening sentence must specify: "Add key under
    `/home/dev/Aria/.aria/config.json` (project-root, NOT aria-orchestrator-local;
    same file used by state-scanner and issue-scan today)." Also add to §Dependencies
    a row clarifying the file is project-root, with cross-reference to existing keys
    `state_scanner.issue_scan.*`. Update tasks.md T2.1 with the same path. Add to
    AD-M6-1 (snapshot script integration) the explicit decision item: "config.json
    discovery method (hard-coded relative path from script location vs env var)".

- **I-tl-2**: `check_cost_measurement_method_enum` (P-2) is a **helper without a caller**
  — the cost.json schema doesn't include `cost_measurement_method` field.
  - Location: `proposal.md` §What F lines 169–174 (P-2 check); `tasks.md` T5.7.
  - Why important: The Spec defines a check that validates an enum value, but the
    cost.json schema (§What A lines 68–89) does NOT include a `cost_measurement_method`
    field. T5.7 acknowledges this gap ("if `cost_measurement_method` field present in
    cost.json use it; else verify schema documentation … explicitly declares the
    method"). This second branch ("verify schema documentation") is paper-fix per
    `[[feedback_paper_fix_antipattern]]` — a doc-only check is not enforceable; it
    would PASS as long as some markdown file contains the literal strings. Per
    `[[feedback_scaffold_helpers_drift_without_callers]]`, this is exactly the
    "helper ahead of caller" pattern: the validator function exists but no production
    code path produces the field it validates.
  - Suggested fix: Either (a) ADD `cost_measurement_method` as a 4th sub-field within
    `metered_usd` and `subscription_usd` in the cost.json schema (§What A lines 70–89),
    populated by the snapshot script (Zhipu → `local_token_count_x_unit_price`, Luxeno
    → `subscription_flat_no_attribution`). This grounds the validator in real produced
    data. (b) DROP P-2 from Spec #1 scope, deferring to a real-cost-rationale-doc Spec
    later. Option (a) preferred; +5 minutes of T1.2 work, eliminates paper-fix risk.

- **I-tl-3**: **Cross-Spec DAG (P-15) under-specified** — AC-7 gates Spec #2 in prose
  but no mechanical enforcement exists yet, and Spec #4 release-closeout dependency
  on Spec #1 cost RED gate is not declared.
  - Location: `proposal.md` §Dependencies last row, §Cross-references "Sibling Specs"
    lines 427–430; `tasks.md` §Ordering dependencies lines 175–191.
  - Why important: DEC §4 P-15 mandates "Sub-Spec dependency DAG (Phase A.2 task-planner
    必须显化)". The Spec mentions Spec #2 gates on AC-7 (text) and lists Spec #4
    "sequential after all M6 Specs done" (text). But: (a) Spec #2 has no obligation
    declared here that its Phase B.1 will run `validate-m6-handoff.py --check-3-day-
    history` as precondition (the Spec #2 proposal does not yet exist; this is
    forward-binding to a future Spec). (b) Spec #4 release-closeout uses the
    `m6.cost_thresholds.luxeno_monthly_usd` and `zhipu_30d_usd` AS RED gates per DEC §2
    Spec #4 scope, but proposal.md does not declare this downstream dependency. If
    the cost.json schema field set later changes (e.g., the threshold key renames),
    Spec #4 silently breaks.
  - Suggested fix: Add to §Dependencies a "Downstream contract" sub-section listing:
    (a) Spec #2 `aria-2.0-m6-e2e-resilience` Phase B.1 MUST run
    `validate-m6-handoff.py --check-3-day-history` and abort on non-zero; (b) Spec #4
    `aria-2.0-m6-release-closeout` reads cost.json + `m6.cost_thresholds.*` for RED
    pre-release gate evaluation — exact field names: `metered_usd.cost_usd`,
    `subscription_usd.cost_usd` (null-aware), `freshness_ts`,
    `m6.cost_thresholds.zhipu_30d_usd`, `m6.cost_thresholds.luxeno_monthly_usd`.
    These constitute a forward-binding contract from Spec #1; any rename in Phase B
    requires amending future Specs.

- **I-tl-4**: `freshness_ts` **ISO format under-specified** — AC-1 evidence Python
  parses `d['freshness_ts'].rstrip('Z')` (assumes trailing Z), but §What A line 87
  says "ISO-8601-UTC" with no format mandate.
  - Location: `proposal.md` §What A line 87; AC-1 lines 264–276.
  - Why important: Python `datetime.fromisoformat` in 3.11+ supports `Z` suffix
    natively; the `.rstrip('Z')` in AC-1 is a 3.10-compat workaround. But more
    fundamentally: there are several legal ISO-8601 UTC encodings (`2026-05-24T12:00:00Z`,
    `2026-05-24T12:00:00+00:00`, `2026-05-24T12:00:00.123456Z`). If the snapshot
    script emits `+00:00` and AC-1 `rstrip('Z')` is no-op, then `fromisoformat` of
    `2026-05-24T12:00:00+00:00` returns a tz-AWARE datetime, but `datetime.utcnow()`
    is tz-NAIVE — subtraction raises `TypeError`. AC-1 would crash with `TypeError`
    on a perfectly valid snapshot. This is a [[feedback_test_mock_pattern_hides_prod_bug]]
    risk: the spec mock uses one format; prod could use another.
  - Suggested fix: §What A line 87 mandate exact format: "ISO-8601 UTC with `Z`
    suffix, no fractional seconds, no `+00:00` form. Format string:
    `datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')`." Update AC-1 evidence Python
    to use timezone-aware comparison: `datetime.datetime.now(datetime.timezone.utc)`
    paired with `datetime.fromisoformat(d['freshness_ts'].replace('Z', '+00:00'))`,
    or simply enforce the strftime format above and use the original tz-naive
    approach consistently. Update T1.2 to cite the exact format string.

- **I-tl-5**: T7.1 "PRD §M6 cross-ref verify" is **wrongly framed as task** — the
  patch is already applied (commit `a786444`).
  - Location: `tasks.md` T7.1 ("Verify PRD §M6 lines 638-646 already reflect the
    Q-final-2 Path a dual-track cost gate patch … if not yet patched, note for owner
    action").
  - Why important: Git log shows commit `a786444 docs(prd-v2): M6 reframe + cost
    gate dual-track patch (DEC-20260524-001)` already landed. T7.1 is therefore a
    no-op task that the implementer either (a) skips (silently) or (b) burns 0.5h
    verifying obvious facts. Per `[[feedback_phase_a_depth_drives_b_velocity]]`,
    tasks must do real work; ghost tasks dilute velocity tracking.
  - Suggested fix: Remove T7.1 entirely; replace with: "T7.1 PRD §M6 line 638-646
    grep-verify: run `grep -n 'm6.cost_thresholds.zhipu_30d_usd\|m6.cost_thresholds.luxeno_monthly_usd'
    docs/requirements/prd-aria-v2.md` and assert non-empty output (provides a
    drift sentinel: if a future PRD edit accidentally renames the threshold key,
    this task's CI re-run would catch it)." That makes T7.1 a real drift-guard,
    not a verify-yesterday's-work no-op. Effort 0.1h not 0.5h; recover 0.4h to
    the buffer.

### Minor

- **m-tl-1**: §What G + AC-7 say "consecutive dates ending no earlier than today - 1
  day" — the boundary case "ending today" vs "ending today - 1" is ambiguous when
  the cron runs after midnight UTC. If the cron just ran 5 minutes ago and produced
  `cost-2026-05-24.json`, the latest is today; AC-7 says "no earlier than today - 1",
  which is satisfied by today, but also by today - 1 if cron hasn't yet run today.
  Tighten to: "the most recent snapshot date >= today - 1 day (UTC), AND ≥3 distinct
  consecutive dates total".

- **m-tl-2**: §What D cron alarm fields list `action_url` but the cron has no obvious
  action endpoint to link to. Either define what `action_url` points to (e.g., the
  Forgejo cost.json file in repo, or an internal Aria dashboard URL once one
  exists), or remove `action_url` from the field list (and from T3.1) to avoid a
  helper-without-caller pattern.

- **m-tl-3**: §How "AD-M6-1..AD-M6-3" table marks all 3 as `_slot_` for Phase B.
  AD-M6-2 (cost-snapshots/ archive retention) and AD-M6-3 (validate-m6-handoff.py
  exit-code semantics) are reasonable Phase B decisions. AD-M6-1 (bash vs Python
  for the snapshot script) is materially the only decision needed for Phase A.3
  agent assignment; punting it to Phase B means T1.1 implementer chooses
  arbitrarily. Recommend: decide language inline in Spec (Python preferred —
  matches sibling `validate-m5-handoff.py` and unit-testability is far easier than
  bash) and remove AD-M6-1 slot. Keeps Phase A bounded, Phase B unambiguous.

- **m-tl-4**: `proposal.md` line 13 cites m5-handoff.yaml "line 151-172" but the
  actual abi_compat_promises block starts at line 151 (verified) — wording is
  fine but cite a stable anchor (`# 4. abi_compat 承诺` section header at line
  149) in addition to line range, for resilience to upstream edits.

### Observations

- **O-tl-1**: The Spec correctly applies `[[feedback_falsifiable_evidence_for_binary_acceptance]]`
  — every AC has a runnable assertion. This is the right pattern for future M6 sibling
  Specs to mirror. Recommend extracting an "AC evidence patterns" subsection into
  `standards/openspec/project.md` after Spec #1 lands, so Spec #2 / #3 / #4 don't
  have to rediscover this template.

- **O-tl-2**: The §Risks table is well-formed but R-M6-1 (Luxeno API doesn't expose
  per-period token count) has Severity=Low; in practice, owner cannot easily fill
  `subscription_usd.tokens_used` without a manual scrape of Luxeno's web console.
  Either elevate R-M6-1 to Medium with a concrete mitigation ("if tokens_used is
  null, snapshot still proceeds; no fail mode") or document the manual scrape
  workflow as an owner-task in §What B. Not blocking for Phase B but a
  documentation-completeness gap.

- **O-tl-3**: Multi-terminal coordination (dev-claude2 Track E follow-ups): commits
  `a4abf66`, `c8a5f03`, `e54ace7` indicate Track E follow-ups already merged
  pre-this-session. No active dev-claude2 branch is shipping concurrently in
  `git branch -a` output. Recommend Spec #1 Phase B.1 branch creation runs
  state-scanner Phase 1.16/1.17 multi-terminal sweep before branching, to confirm
  no parallel writer to `aria-orchestrator/docs/` (`validate-m6-handoff.py` is in
  that dir). Not a blocking finding for Phase A; a Phase B operational hygiene
  note.

- **O-tl-4**: Effort baseline ~10h (9.5h reconciled) is credible given task count
  (32 leaf tasks at ~18 min each = 9.6h, exact match). Per
  `[[feedback_phase_budget_compounding]]`, single-phase Spec budgets at this size
  typically actualize at ×0.6-0.7 = ~6-7h AI time. Owner manual actions
  (config.json threshold set + 3 cron runs over 3 days wall-clock) are correctly
  excluded from the AI baseline. No under-estimation cascade risk identified.

- **O-tl-5**: §Constraints table lists abi_compat enforcement column "`validate-m6-handoff.py::
  check_*`". This is a forward-binding declaration — the script doesn't exist yet
  (creation is T5.1). Consider adding a §Constraints footnote: "Enforcement is
  the validate-m6-handoff.py contract; this Spec creates it. M7+ Specs must
  cross-check via the same script." Helps M7 spec author understand the chain.

## Verdict rationale

NEEDS_FIX (not BLOCK, not NEEDS_MAJOR_FIX). The three Critical findings are concrete
code-grounded errors with one-paragraph patch directions — they do not require
re-litigating DEC-20260524-001 §2 scope nor rewriting any §Why narrative beyond AC-3
framing. The 5 Important findings are scope-bounded edits (mostly path
disambiguation + format pinning).

What unblocks Phase B from my seat (in priority order):
1. **C-tl-1** patched: full canonical paths cited for all 5 grep targets, with a
   "file-missing distinguishes file-found-with-zero-matches" assertion in T5.9.
2. **C-tl-2** patched: SQL filter clause defined as `provider_cost_model='metered'`
   with rationale citing db.py:1062 contract.
3. **C-tl-3** patched: AC-3 split/rewritten to verify cost.json output only;
   §Why narrative truthfully describes the dispatches table's `0.0` storage.
4. **I-tl-1 / I-tl-2 / I-tl-4** addressed inline (config path + P-2 field decision +
   freshness_ts format).
5. I-tl-3 / I-tl-5 / minors as time permits.

After these edits, Phase A.3 agent assignment is clean (backend-architect can
implement without surprise mid-Phase-B reframes per `[[feedback_spec_reframe_in_session]]`).
Without them, Phase B T1.1 will stall on T-tl-2 within the first hour
(non-executable SQL) and T5.2 will silently PASS without enforcing anything
(undetected until M7 abi_compat regression).

R2 collapse eligibility: if R2 verifies these 3 Critical patches are applied and
no NEW critical surfaces, R2 4/4 SCOPE_OK is plausible per the Aria-default
collapse rule (R3+ skipped unless owner-invoked per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`).
