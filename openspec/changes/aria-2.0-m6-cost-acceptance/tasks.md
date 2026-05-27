# M6 Spec #1 Tasks — Cost Acceptance (dual-track schema + cron sentinel + alarm)

> **Spec**: [aria-2.0-m6-cost-acceptance](./proposal.md)
> **Level**: 3 (Full)
> **Status**: Approved (Phase A.2 CONVERGED 2026-05-24 via R3 stability; Phase A.3 agent allocation locked 2026-05-26; ready for Phase B.1)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2)
> **Estimated total**: ~12h (updated from ~10h; R1 adds T3.7/T3.8 + T4.5/T4.6 + T5.11 + T3.4-bis; see proposal §Effort baseline)
> **Agent**: backend-architect (primary impl ~11h/12h: T-schema/T-config/T-alarm/T-acceptance/T-validate; qa-engineer for AC pytest design review + Phase B test-strategy audit; knowledge-manager for T-docs AD-M6-1/2 + T-prd cross-ref verify ~1h)

---

## Task Group Overview

| Group | Topic | Scope ref | Est |
|-------|-------|-----------|-----|
| T-schema | Dual-row cost.json schema + snapshot script | §What A | ~2h |
| T-config | .aria/config.json threshold keys | §What B | ~1h |
| T-alarm | Cron sentinel + Feishu alarm + Luxeno null guard + volume floor | §What D | ~3h |
| T-acceptance | Acceptance Python script (binary-falsifiable) | §What E | ~2h |
| T-validate | validate-m6-handoff.py (5 abi_compat + P-2 + P-3 + pricing freshness + 3-day history) | §What F+G | ~3h |
| T-docs | AD-M6-* slots + doc propagation | §How AD table | ~0.5h |
| T-prd | PRD §M6 line 638-646 cross-ref verify (no PRD rewrite needed — patch already applied) | §Dependencies | ~0.5h |

---

## T-schema — Dual-row cost.json schema + snapshot script (~2h)

<!-- R1-I-1 fix: atomic write os.rename pattern specified in T1.1 -->
<!-- R1-I-6 fix: atomic write also for archive copy -->
<!-- R1-C3 fix: absolute repo-relative paths specified; REPO_ROOT resolution pattern -->
<!-- R1-C8 fix: script is .py throughout -->
<!-- R2-C-tl-N1 fix: REPO_ROOT off-by-1 corrected — HERE.parent (2 levels), NOT .parent.parent.parent -->
- [x] 1.1 Design and implement snapshot script `aria-orchestrator/acceptance/m6-cost-snapshot.py`:
  - Resolve `HERE = Path(__file__).resolve().parent; REPO_ROOT = HERE.parent` (anchors at `aria-orchestrator/`,
    mirrors `validate-m5-handoff.py:40-41` line-for-line; `__file__` is at `aria-orchestrator/acceptance/`).
  - Query SQLite dispatches table at `REPO_ROOT / "hermes-extensions" / "aria-layer1" / "aria_layer1" / "aria_layer1.db"`
    (or configured path): `SUM(token_cost_usd) WHERE provider_cost_model='metered' AND created_at > datetime('now', '-30 days')`.
  - Cast aggregate to float explicitly: `float(cursor.fetchone()[0] or 0.0)`.
  - Write dual-row cost.json to `.aria/cost.json` using **atomic write**: write to
    `.aria/cost.json.tmp` then `os.rename('.aria/cost.json.tmp', '.aria/cost.json')`.
  - Archive also using atomic write: write to `.aria/cost-snapshots/cost-YYYY-MM-DD.json.tmp`
    then `os.rename()`. Document atomic-write approach in AD-M6-2.
  - `freshness_ts` MUST be `datetime.now(timezone.utc).isoformat()` (produces `+00:00` suffix,
    e.g. `2026-05-24T12:00:00+00:00`). Never bare `Z`, never timezone-naive.

<!-- R1-C1 fix: query uses provider_cost_model='metered', not provider='zhipu' -->
- [x] 1.2 Implement dual-row schema (P-1): `metered_usd` with `provider='zhipu', model, input_tokens,
  output_tokens, cost_usd (float, additive — from SUM WHERE provider_cost_model='metered'), note`;
  `subscription_usd` with `provider='luxeno', model, cost_usd=null (NOT 0, NOT omitted),
  attribution_disclaimer, tokens_used (informational-only, not in cost math), window_start_iso,
  window_end_iso`; top-level `freshness_ts` written as UTC+00:00 ISO-8601 at snapshot time.
  The `subscription_usd.cost_usd=null` is a snapshot-script transformation: even though the schema
  stores `token_cost_usd=0.0` per Luxeno dispatch, the snapshot deliberately sets null to prevent
  false alarm attribution (per AC-3 Layer 1).

- [x] 1.3 Unit test: snapshot script with in-memory SQLite fixture → assert output JSON matches dual-row
  schema; assert `subscription_usd.cost_usd` is `None` (JSON null), not `0`; assert `metered_usd.cost_usd`
  equals expected float SUM from fixture rows; assert `freshness_ts` is timezone-aware with `+00:00` offset
  (parse with `datetime.fromisoformat(ts)` and assert `tzinfo is not None`); assert `metered_usd.cost_usd >= 0.0`;
  fixture includes ≥1 row WHERE `token_cost_usd IS NULL` (if SQLite fixture supports it) — verify
  SUM excludes nulls as expected; fixtures are inline Python dict literals in test function scope.
  <!-- R1-I-7 fix: cast test; R1-C4 fix: freshness_ts tzinfo assert in test -->

- [x] 1.4 Unit test: snapshot script with zero Zhipu rows in fixture → assert `metered_usd.cost_usd == 0.0`
  (valid zero sum, not null); assert `subscription_usd.cost_usd` remains null regardless.

- [x] 1.5 Unit test (R1-I-7): SQLite fixture returns the aggregate as a string type (simulate edge case) →
  assert output cost.json `metered_usd.cost_usd` is a Python `float`, not a string; the `float()` cast
  in T1.1 handles this coercion.
  <!-- R1-I-7 fix: new test for stringified cost_usd cast -->

---

## T-config — .aria/config.json threshold keys (~1h)

- [x] 2.1 Add `m6.cost_thresholds.zhipu_30d_usd` and `m6.cost_thresholds.luxeno_monthly_usd` to
  `.aria/config.json` (owner-set values; example values in config.template.json if template exists)

- [x] 2.2 Document threshold semantics in a comment-adjacent section (JSON does not support comments;
  document in `aria-orchestrator/docs/architecture-decisions.md` AD-M6-2 slot or in acceptance script
  header): `zhipu_30d_usd` = rolling 30d Zhipu metered cap; `luxeno_monthly_usd` = owner invoice
  reference threshold (manual review only, no automated alarm against it)

- [x] 2.3 Unit test: snapshot/alarm script fails with a clear error message if
  `m6.cost_thresholds.zhipu_30d_usd` is absent from config.json (not a silent zero-division or KeyError)

---

## T-alarm — Cron sentinel + Feishu alarm + Luxeno null guard + volume floor (~3h)

<!-- R1-C1 fix: query uses provider_cost_model='subscription_flat', not provider='luxeno' -->
<!-- R1-C5 fix: pct_used is integer 0-100; Decimal arithmetic in threshold comparison -->
<!-- R1-I-3 fix: ARIA_FEISHU_WEBHOOK_URL caught around alarm send only, not snapshot write -->
- [x] 3.1 Implement Feishu alarm logic in snapshot/alarm script: if
  `metered_usd.cost_usd >= 0.8 * config.m6.cost_thresholds.zhipu_30d_usd`
  (use `decimal.Decimal` for comparison to avoid IEEE-754 drift), send Feishu warning card
  via `ARIA_FEISHU_WEBHOOK_URL` (reuse existing feishu_webhook.py; do not introduce new env var);
  card fields: `provider, cost_usd, threshold, pct_used` (integer 0-100, computed as
  `int(round(cost_usd / threshold * 100))`), `freshness_ts, action_url`.
  If `ARIA_FEISHU_WEBHOOK_URL` is absent at runtime: (1) write cost.json (do NOT abort), (2) log
  `[WARN] alarm-skipped: ARIA_FEISHU_WEBHOOK_URL not configured; Feishu alarm suppressed`, (3) exit 0.
  Catch `NotConfigured` around the `feishu_send` call ONLY — not around the snapshot write path.

- [x] 3.2 Implement Luxeno null guard (Luxeno=0 false-positive prevention, DEC R2 ai-CH-3 closure):
  when `subscription_usd.cost_usd is None`, the alarm path MUST skip Luxeno threshold evaluation
  entirely and log `"Luxeno subscription: manual invoice review required (cost_usd not per-dispatch
  attributable)"` to stdout/log; MUST NOT evaluate `None >= 0.8 * luxeno_monthly_usd` as truthy.

<!-- R1-C5 fix: Decimal fixture math; above-boundary test added as T3.4-bis -->
- [x] 3.3 Unit test: `cost_usd = threshold * Decimal('0.80')` (boundary) → `feishu_send` IS called with
  `pct_used == 80` (AC-5 boundary PASS); mock `feishu_send` at transport layer only (not alarm logic)
  per `[[feedback_test_mock_pattern_hides_prod_bug]]`; use `decimal.Decimal` for fixture math.

- [x] 3.4 Unit test: `cost_usd = threshold * Decimal('0.7999')` (below boundary) → `feishu_send` NOT
  called (AC-5 below-boundary).

- [x] 3.4-bis Unit test (R1-C5 above-boundary): `cost_usd = threshold * Decimal('0.801')` → `feishu_send`
  IS called (AC-5 above-boundary, three-zone coverage complete).
  <!-- R1-C5 fix: T3.4-bis above-boundary case added -->

- [x] 3.5 Unit test: `subscription_usd.cost_usd = null` → `feishu_send` NOT called for Luxeno;
  manual-review log message IS emitted (AC-3 Luxeno null guard verification).

- [x] 3.6 Nomad cron job config: add or extend existing `aria-layer1-cron` job (or create new
  `aria-layer1-cost-sentinel` periodic job) to run snapshot+alarm script daily; document in
  AD-M6-1 slot the chosen integration approach.

<!-- R1-C11 fix: T3.7 + T3.8 new tasks for dispatch volume floor per §D.iii + AC-5b -->
- [x] 3.7 Implement Luxeno dispatch volume floor check (§What D.iii, AC-5b): compute 7-day rolling
  average of dispatches with `provider_cost_model='subscription_flat'` using:
  ```sql
  SELECT COUNT(*) / 7.0
  FROM dispatches
  WHERE provider_cost_model = 'subscription_flat'
    AND created_at > datetime('now', '-7 days')
  ```
  If average is **strictly less than 10 dispatches/day**, emit a Feishu info card with severity=info
  (not warning), title `"Luxeno volume floor reminder"`, body:
  `"Luxeno dispatch volume below subscription-effectiveness floor (N=<avg_per_day>, floor=10); consider routing reconfiguration."`.
  Volume floor check is independent of the 80% cost alarm and runs in the same cron invocation.

- [x] 3.8 Unit tests for volume floor (AC-5b three-zone):
  - `test_volume_floor_below`: 7-day average = 9.0/day (< 10) → info Feishu card IS emitted.
  - `test_volume_floor_at_floor`: 7-day average = 10.0/day (== 10) → info card NOT emitted
    (strictly < 10 boundary).
  - `test_volume_floor_above`: 7-day average = 15.0/day (> 10) → info card NOT emitted.

---

## T-acceptance — Acceptance Python script (~2h)

<!-- R1-C8 fix: script named .py throughout -->
<!-- R1-C7 + Q1 fix: exit codes 0/1/2 specified in tasks -->
<!-- R1-I-2 fix: T4.5 missing file + T4.6 corrupt JSON tasks added -->
- [x] 4.1 Implement `aria-orchestrator/acceptance/check-m6-cost-acceptance.py` that runs checks AC-1
  through AC-4 (freshness gate, dual-row schema, Luxeno null, threshold config); each check emits
  `[PASS] AC-N: <name>` or `[FAIL] AC-N: <reason>` or `[ERROR] AC-0: <reason>`;
  exit code contract: 0 = all pass, 1 = AC data failure, 2 = infrastructure error (missing file,
  corrupt JSON, missing config key). If `.aria/cost.json` is absent, emit
  `[ERROR] AC-0: cost.json not found — cron has never run` and exit 2. Catch `json.JSONDecodeError`
  → `[ERROR] AC-0: JSON parse error: <filename>` + exit 2.
  <!-- R1-C4 fix: AC-1 check in script uses datetime.now(timezone.utc); age<0 guard included -->
  AC-1 implementation in script: parse `freshness_ts` with `datetime.fromisoformat()`, assert
  `tzinfo is not None`, compute `age = (datetime.now(timezone.utc) - ts).total_seconds()`, guard
  `age < 0` → exit 1 with clock-skew message, boundary is strict `< 86400`.

- [x] 4.2 Unit test: run acceptance script against a known-good fixture `.aria/cost.json` (fresh,
  dual-row correct, thresholds set) → exit 0, all `[PASS]` lines; fixture is inline Python dict.

- [x] 4.3 Unit test: run acceptance script with `freshness_ts` set to `now - 90000s` (25h, stale) →
  exit 1, `[FAIL] AC-1: stale (age=90000s > 86400s limit)`.

- [x] 4.4 Unit test: run acceptance script with `subscription_usd.cost_usd = 0` (invalid, should be null) →
  exit 1, `[FAIL] AC-2: Luxeno cost_usd must be null not 0`.

- [x] 4.5 Unit test (R1-I-2): `.aria/cost.json` file does not exist → exit 2,
  `[ERROR] AC-0: cost.json not found — cron has never run`.
  <!-- R1-I-2 fix: T4.5 missing-file → exit 2 test -->

- [x] 4.6 Unit test (R1-I-2): `.aria/cost.json` contains corrupt JSON (partial write simulation) →
  exit 2, `[ERROR] AC-0: JSON parse error: .aria/cost.json`.
  <!-- R1-I-2 fix: T4.6 corrupt JSON → exit 2 test -->

<!-- R2-ai-NI-1 fix: AC-2b orphan provider_cost_model check + test -->
- [x] 4.7 Implement AC-2b orphan-rows check in `check-m6-cost-acceptance.py`:
  `SELECT COUNT(*), GROUP_CONCAT(dispatch_id) FROM dispatches WHERE provider_cost_model IS NULL`.
  If count > 0 → `[FAIL: AC-2b] orphaned rows=N (ids: ...)` + exit 1.
- [x] 4.8 Unit test (R2-NI-1): fixture DB with 1 NULL `provider_cost_model` row → exit 1 +
  `[FAIL: AC-2b]` in stdout; fixture with 0 NULL rows → AC-2b PASS.

---

## T-validate — validate-m6-handoff.py (5 abi_compat + P-2 + P-3 + pricing freshness + 3-day history) (~3h)

<!-- R1-C3 fix: all grep tasks use absolute repo-relative paths via REPO_ROOT pattern -->
- [x] 5.1 Create `aria-orchestrator/docs/validate-m6-handoff.py` (sibling to `validate-m5-handoff.py`)
  with CLI interface: `python3 validate-m6-handoff.py [-v]` runs all checks; individual check flags:
  `--check-abi-compat`, `--check-cost-method-enum`, `--check-3-day-history`, `--check-pricing-freshness`.
  <!-- R2-C-tl-N1 fix: REPO_ROOT off-by-1 corrected — HERE.parent (2 levels), NOT .parent.parent.parent -->
  Resolve `HERE = Path(__file__).resolve().parent; REPO_ROOT = HERE.parent` (anchors at
  `aria-orchestrator/`, mirrors `validate-m5-handoff.py:40-41` line-for-line; `__file__` is at
  `aria-orchestrator/docs/`). All file access uses absolute paths:
  `REPO_ROOT / "hermes-extensions" / "aria-layer1" / "aria_layer1" / <file>`
  and `REPO_ROOT / "hermes-extensions" / "aria-layer1" / "migrations" / <file>`.

<!-- R1-C3 fix: explicit absolute paths; negative grep for DROP TRIGGER in 5.2 -->
- [x] 5.2 Implement `check_dispatch_audit_log_immutable` (P-3, promise #1):
  - Positive grep: `REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/schema.sql"` contains
    both `audit_no_update` and `audit_no_delete` trigger name strings.
  - Negative grep: `REPO_ROOT / "hermes-extensions/aria-layer1/migrations/004_schema_v4_additive.sql"`
    does NOT contain `DROP TRIGGER` (if `DROP TRIGGER` is absent from the migration, triggers are safe).
  - Emit `[PASS] dispatch_audit_log_immutable_promise` or `[FAIL]` with reason.

<!-- R1-C3 fix: absolute path for extension.py -->
- [x] 5.3 Implement `check_rework_round_cap_default_3` (P-3, promise #2): grep
  `REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/extension.py"` for literal `3` as default
  in `_read_rework_max_round`; fail if absent.

<!-- R1-C3 fix: absolute path for reconciler.py -->
- [x] 5.4 Implement `check_spec_drift_threshold_default_70` (P-3, promise #3): grep
  `REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/reconciler.py"` for literal `70` as default
  in `_read_spec_drift_threshold`; fail if absent.

<!-- R1-C3 fix: absolute path for comment_poll.py; non-comment grep pattern added -->
- [x] 5.5 Implement `check_comment_poll_direct_transition` (P-3, promise #4): grep
  `REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/comment_poll.py"` using
  `re.search(r'^\s*[^#]*_handle_s7_human_gate\s*\(', content, re.MULTILINE)` to exclude commented-out
  or dead-code-wrapped calls; assert match exists (call is present and non-commented); fail if absent.

<!-- R1-C3 fix: absolute db/extension path; INSERT-scoped grep pattern -->
- [x] 5.6 Implement `check_risk_tier_dual_write_literal_always` (P-3, promise #5): grep
  dispatcher/db INSERT path source files at
  `REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/db.py"` (and/or `extension.py`) using
  `re.search(r"INSERT.*risk_tier_stub.*'always'", content, re.DOTALL)` (anchored to INSERT context,
  not any occurrence of `'always'`); fail if pattern is absent.

- [x] 5.7 Implement `check_cost_measurement_method_enum` (P-2, DEC §4 qa-M-qa-R3-3):
  If `cost_measurement_method` field present in `.aria/cost.json`, verify it is one of
  `{provider_api_billing, local_token_count_x_unit_price, subscription_flat_no_attribution}`;
  hard fail (exit 1) on invalid enum value. If field absent, emit
  `[WARN] cost_measurement_method field absent from cost.json; advisory in M6, promoted to FAIL in M7+`
  and exit 0 (warning-only in M6).
  Additionally: verify `zhipu_client.py` `_post_chat` return dict does NOT contain `cost_usd` key
  (grep `REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/zhipu_client.py"` for
  `'cost_usd'` in the response parsing context; if found, emit FAIL — confirms local pricing is needed).

<!-- R1-C6 fix: consecutive-day algorithm fully specified in T5.8 -->
- [x] 5.8 Implement `check_3_day_rolling_history_exists` (§What G, AC-7): scan
  `.aria/cost-snapshots/` for files matching `cost-YYYY-MM-DD.json`; extract dates from filenames;
  sort descending; take 3 most-recent. Check passes if AND ONLY IF:
  (a) ≥3 files exist;
  (b) The 3 most-recent dates form a consecutive sequence: `date[i+1] == date[i] + timedelta(days=1)`;
  (c) The most recent date >= `datetime.now(timezone.utc).date() - timedelta(days=1)`.
  "Today" = `datetime.now(timezone.utc).date()`.
  Emit `"3-day rolling history: PASS (N files, latest YYYY-MM-DD)"` on success.
  Emit `[FAIL] 3-day history: consecutive gap detected` if condition (b) fails.
  Emit `[FAIL] 3-day history: most recent snapshot is too old (latest YYYY-MM-DD)` if (c) fails.

<!-- R1-C10 + Q2 fix: T5.11 new task for check_zhipu_pricing_freshness -->
- [x] 5.9 Unit test: run `validate-m6-handoff.py --check-abi-compat` against the committed codebase
  (canonical instance test per `[[feedback_validator_repo_drift_guard_test]]`) → exit 0, stdout
  contains all 5 promise IDs without any `FAIL` line.

<!-- R1-C6 fix: gap test cases added to T5.10 -->
- [x] 5.10 Unit tests for `--check-3-day-history`:
  - `[today-3, today-2, today-1]` → exit 0 (consecutive, recent).
  - Only 2 files `[today-2, today-1]` → exit non-zero (insufficient count).
  - Gap case `[today-4, today-2, today-1]` → exit non-zero (gap detected at today-3).
    <!-- R1-C6 fix: T5.10-bis gap test case added -->
  - `[today-2, today-1, today]` → exit 0 (including today is valid).
  - `[today-5, today-4, today-3]` → exit non-zero (most recent is too old: today-3 > today-1 allowed).

- [x] 5.11 Implement `check_zhipu_pricing_freshness` (Q2, 2026-05-24): parse `_PRICING_REVIEW_DUE` and
  `_PRICING_OWNER_VERIFIED` from
  `REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/zhipu_pricing.py"` (use `ast.parse` or
  regex to extract literal values; do not import the module).
  - If `_PRICING_REVIEW_DUE < datetime.now(timezone.utc).date()`:
    emit `[WARN] zhipu_pricing: _PRICING_REVIEW_DUE ({date}) is in the past — pricing is stale; run owner pricing review ritual` and exit 1.
  - If `_PRICING_OWNER_VERIFIED == False`:
    emit `[WARN] zhipu_pricing: _PRICING_OWNER_VERIFIED=False — cost attribution unconfirmed` and exit 1.
  - Both conditions may trigger in the same run; emit all applicable warnings before exit.
  Unit test: mock `_PRICING_REVIEW_DUE = "2020-01-01"` (past) → exit 1 with expected `[WARN]` text.
  Unit test: mock `_PRICING_OWNER_VERIFIED = False` → exit 1 with expected `[WARN]` text.
  Unit test: both values healthy → exit 0.
  <!-- R1-C10 + Q2 fix: T5.11 new task -->

---

## T-docs — AD-M6-* slots (~0.5h)

<!-- R1-C7 + Q1 fix: T6.3 removed as AD-M6-3 is now Spec-body defined -->
<!-- R1-I-4 + Q4 fix: AD allocation reservation note added to proposal; T6.1/T6.2 updated -->
- [x] 6.1 Add AD-M6-1 decision to `aria-orchestrator/docs/architecture-decisions.md`:
  "cost.json snapshot script: Python; integrated with existing aria-layer1-cron as new sub-command"
  (decision already resolved per §How AD table in proposal).

- [x] 6.2 Add AD-M6-2 decision: "cost-snapshots/ archive naming = `cost-YYYY-MM-DD.json`; retention =
  last 30 files; atomic write via `os.rename()` for both cost.json and archive copy;
  concurrent reader/writer safety via atomic rename (no file locking)."

---

## T-prd — PRD cross-ref verify (~0.5h)

- [x] 7.1 Verify PRD §M6 lines 638-646 already reflect the Q-final-2 Path a dual-track cost gate patch
  (metered_usd + subscription_usd language); if not yet patched, note for owner action (owner-blocking,
  not AI-runnable per `[[feedback_t15_owner_blocking_pattern]]`)

- [x] 7.2 Verify US-026 `docs/requirements/user-stories/US-026.md` references Spec #1 change ID
  `aria-2.0-m6-cost-acceptance`; update if missing

---

## Ordering dependencies

```
T-schema (1.1-1.5)          — no upstream Spec code deps; reads existing dispatches schema
    │
    ├── T-config (2.1-2.3)  — parallel with T-schema
    │
    └── T-alarm (3.1-3.8)   — depends on T-schema (reads cost.json) + T-config (reads thresholds)
            │
            └── T-acceptance (4.1-4.6)  — depends on T-schema + T-config outputs

T-validate (5.1-5.11)       — depends on T-schema (cost.json format known) but independent of T-alarm
                              (5.1-5.8 can proceed in parallel with T-alarm)
                              5.9 canonical instance test requires codebase to be committed with M5 code
                              (already true — M5 archived 2026-05-23, no further changes expected)

T-docs (6.1-6.2)            — parallel with all above (documentation slots)
T-prd (7.1-7.2)             — parallel with all above (verify-only, no code change)
```

---

## Precision items cross-reference

| Precision item | DEC source | §What section | Task(s) |
|----------------|------------|---------------|---------|
| P-1: subscription.tokens_used informational + window dates | DEC §4 ai-R3CH-2 | §What A (field semantics block) | T1.2 |
| P-2: cost_measurement_method enum in validate-m6-handoff.py | DEC §4 qa-M-qa-R3-3 | §What F (validate check description) | T5.7 |
| P-3: validate-m6-handoff.py cross-check all 5 m5-handoff.yaml abi_compat promises | DEC §4 backend M-ba-R3-1c | §What F + §Constraints | T5.2–T5.6, T5.9 |
| Q1: exit code 0/1/2 contract | Owner 2026-05-24 | §What E (exit code contract) | T4.1 |
| Q2: check_zhipu_pricing_freshness | Owner 2026-05-24 | §What F + AC-8 | T5.11 |
| Q3: USD-only constraint | Owner 2026-05-24 | §Constraints + OOS-10 | T1.1, T1.2 |
| Q4: AD-M6-1/2/3 reservation | Owner 2026-05-24 | §How AD table + frontmatter | T6.1, T6.2 |

---

## Status

**Approved (Phase A.2 CONVERGED 2026-05-24 via R3 stability; Phase A.3 agent allocation locked 2026-05-26)** — Ready for Phase B.1 branch creation → Phase B.2 implementation.

**Phase A trajectory**:
- A.1 Draft 2026-05-24 (commit `c29a800` predecessor batch)
- A.2 R1 NEEDS_FIX 4/4 (4-agent: tl + qa + ai + cr); 12C + 20I → 11+8 themes
- A.2 R1-fix `0d4a317`: 11C + 8I + Q1-Q4 owner decisions closed
- A.2 R2 SCOPE_OK_R2 3/3 (3-agent: cr + ai + tl); 1 new C (REPO_ROOT off-by-1) + 2 I
- A.2 R2-fix `75a399d`: C-tl-N1 + cr-I1 + ai-NI-1 closed
- A.2 R3 stability (tl-critic 1-agent): R3_STABLE 0 new C + 0 new I → **CONVERGED Approved**
- A.3 agent allocation lock 2026-05-26: backend-architect primary + qa-engineer review + knowledge-manager for docs/PRD groups

**Phase B kickoff order (per Track G + Spec #4 closeout handoff)**: branch `feature/m6-cost-acceptance` in
`aria-orchestrator` submodule; Phase B.1 priority = cron-daily kick to begin 3-day data accumulation
(Spec #2 AC-7 precondition; ≥3 daily runs unblock Spec #2 Phase B start).
