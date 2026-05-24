# M6 Spec #1 Tasks — Cost Acceptance (dual-track schema + cron sentinel + alarm)

> **Spec**: [aria-2.0-m6-cost-acceptance](./proposal.md)
> **Level**: 3 (Full)
> **Status**: **Draft** (Phase A.1; pending Phase A.2 post_spec audit → Approved → Phase A.3 → B.1)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2)
> **Estimated total**: ~10h (central; see proposal §Effort baseline)
> **Agent**: backend-architect

---

## Task Group Overview

| Group | Topic | Scope ref | Est |
|-------|-------|-----------|-----|
| T-schema | Dual-row cost.json schema + snapshot script | §What A | ~2h |
| T-config | .aria/config.json threshold keys | §What B | ~1h |
| T-alarm | Cron sentinel + Feishu alarm + Luxeno null guard | §What D | ~2h |
| T-acceptance | Acceptance SQL/Python script (binary-falsifiable) | §What E | ~1.5h |
| T-validate | validate-m6-handoff.py (5 abi_compat + P-2 + P-3 + 3-day history) | §What F+G | ~2.5h |
| T-docs | AD-M6-* slots + doc propagation | §How AD table | ~0.5h |
| T-prd | PRD §M6 line 638-646 cross-ref verify (no PRD rewrite needed — patch already applied) | §Dependencies | ~0.5h |

---

## T-schema — Dual-row cost.json schema + snapshot script (~2h)

- [ ] 1.1 Design snapshot script (`aria-orchestrator/acceptance/m6-cost-snapshot.sh` or `.py`):
  query SQLite dispatches table `SUM(token_cost_usd)` WHERE provider column identifies Zhipu-routed rows,
  rolling 30-day window; write dual-row cost.json to `.aria/cost.json` + archive copy to
  `.aria/cost-snapshots/cost-YYYY-MM-DD.json`

- [ ] 1.2 Implement dual-row schema (P-1): `metered_usd` with `provider, model, input_tokens, output_tokens,
  cost_usd (float, additive), note`; `subscription_usd` with `provider: luxeno, model, cost_usd: null
  (NOT 0), attribution_disclaimer, tokens_used (informational-only, not in cost math), window_start_iso,
  window_end_iso`; top-level `freshness_ts` written at snapshot time

- [ ] 1.3 Unit test: snapshot script with in-memory SQLite fixture → assert output JSON matches dual-row
  schema; assert `subscription_usd.cost_usd` is `None` (JSON null), not `0`; assert `metered_usd.cost_usd`
  equals expected SUM from fixture rows; assert `freshness_ts` is recent (< 5s old)

- [ ] 1.4 Unit test: snapshot script with zero Zhipu rows in fixture → assert `metered_usd.cost_usd == 0.0`
  (valid zero sum, not null); assert `subscription_usd.cost_usd` remains null regardless

---

## T-config — .aria/config.json threshold keys (~1h)

- [ ] 2.1 Add `m6.cost_thresholds.zhipu_30d_usd` and `m6.cost_thresholds.luxeno_monthly_usd` to
  `.aria/config.json` (owner-set values; example values in config.template.json if template exists)

- [ ] 2.2 Document threshold semantics in a comment-adjacent section (JSON does not support comments;
  document in `aria-orchestrator/docs/architecture-decisions.md` AD-M6-2 slot or in acceptance script
  header): `zhipu_30d_usd` = rolling 30d Zhipu metered cap; `luxeno_monthly_usd` = owner invoice
  reference threshold (manual review only, no automated alarm against it)

- [ ] 2.3 Unit test: snapshot/alarm script fails with a clear error message if
  `m6.cost_thresholds.zhipu_30d_usd` is absent from config.json (not a silent zero-division or KeyError)

---

## T-alarm — Cron sentinel + Feishu alarm + Luxeno null guard (~2h)

- [ ] 3.1 Implement Feishu alarm logic in snapshot/alarm script: if
  `metered_usd.cost_usd >= 0.8 * config.m6.cost_thresholds.zhipu_30d_usd`, send Feishu warning card
  via `ARIA_FEISHU_WEBHOOK_URL` (reuse existing feishu_webhook.py; do not introduce new env var);
  card fields: `provider, cost_usd, threshold, pct_used, freshness_ts, action_url`

- [ ] 3.2 Implement Luxeno null guard (Luxeno=0 false-positive prevention, DEC R2 ai-CH-3 closure):
  when `subscription_usd.cost_usd is None`, the alarm path MUST skip Luxeno threshold evaluation
  entirely and log `"Luxeno subscription: manual invoice review required (cost_usd not per-dispatch
  attributable)"` to stdout/log; MUST NOT evaluate `None >= 0.8 * luxeno_monthly_usd` as truthy

- [ ] 3.3 Unit test: `cost_usd = 0.80 * zhipu_threshold` (boundary) → `feishu_send` IS called with
  `pct_used >= 80` (AC-5 boundary PASS); mock `feishu_send` at transport layer only (not alarm logic)
  per `[[feedback_test_mock_pattern_hides_prod_bug]]`

- [ ] 3.4 Unit test: `cost_usd = 0.79 * zhipu_threshold` (below boundary) → `feishu_send` NOT called (AC-5)

- [ ] 3.5 Unit test: `subscription_usd.cost_usd = null` → `feishu_send` NOT called for Luxeno;
  manual-review log message IS emitted (AC-3 Luxeno null guard verification)

- [ ] 3.6 Nomad cron job config: add or extend existing `aria-layer1-cron` job (or create new
  `aria-layer1-cost-sentinel` periodic job) to run snapshot+alarm script daily; document in
  AD-M6-1 slot the chosen integration approach

---

## T-acceptance — Acceptance SQL/Python script (~1.5h)

- [ ] 4.1 Implement `aria-orchestrator/acceptance/check-m6-cost-acceptance.py` that runs checks AC-1
  through AC-4 (freshness gate, dual-row schema, Luxeno null, threshold config); each check emits
  `[PASS] AC-N: <name>` or `[FAIL] AC-N: <reason>`; script exits 0 only if all checks pass

- [ ] 4.2 Unit test: run acceptance script against a known-good fixture `.aria/cost.json` (fresh,
  dual-row correct, thresholds set) → exit 0, all `[PASS]` lines

- [ ] 4.3 Unit test: run acceptance script with `freshness_ts` set to `now - 90000s` (25h, stale) →
  exit non-zero, `[FAIL] AC-1: stale (age=90000s > 86400s limit)`

- [ ] 4.4 Unit test: run acceptance script with `subscription_usd.cost_usd = 0` (invalid, should be null) →
  exit non-zero, `[FAIL] AC-2: Luxeno cost_usd must be null not 0`

---

## T-validate — validate-m6-handoff.py (5 abi_compat + P-2 + P-3 + 3-day history) (~2.5h)

- [ ] 5.1 Create `aria-orchestrator/docs/validate-m6-handoff.py` (sibling to `validate-m5-handoff.py`)
  with CLI interface: `python3 validate-m6-handoff.py [-v]` runs all checks; individual check flags:
  `--check-abi-compat`, `--check-cost-method-enum`, `--check-3-day-history`

- [ ] 5.2 Implement `check_dispatch_audit_log_immutable` (P-3, promise #1): grep `schema.sql` for
  `audit_no_update` and `audit_no_delete` trigger keyword presence; grep `004_schema_v4_additive.sql`
  to assert triggers are not dropped; exit with named promise ID in stdout on PASS/FAIL

- [ ] 5.3 Implement `check_rework_round_cap_default_3` (P-3, promise #2): grep `extension.py` for
  literal `3` as default in `_read_rework_max_round`; fail if absent

- [ ] 5.4 Implement `check_spec_drift_threshold_default_70` (P-3, promise #3): grep `reconciler.py`
  for literal `70` as default in `_read_spec_drift_threshold`; fail if absent

- [ ] 5.5 Implement `check_comment_poll_direct_transition` (P-3, promise #4): grep `comment_poll.py`
  for `_handle_s7_human_gate` call wiring presence; fail if absent or commented out

- [ ] 5.6 Implement `check_risk_tier_dual_write_literal_always` (P-3, promise #5): grep
  dispatcher/db INSERT path source files for `'always'` literal written to `risk_tier_stub`; fail
  if literal is absent from the dispatch INSERT code path

- [ ] 5.7 Implement `check_cost_measurement_method_enum` (P-2, DEC §4 qa-M-qa-R3-3):
  verify that for each provider in cost.json, the applicable `cost_measurement_method` is one of
  `{provider_api_billing, local_token_count_x_unit_price, subscription_flat_no_attribution}`;
  method resolution: if `cost_measurement_method` field present in cost.json use it; else verify
  schema documentation (acceptance script header or AD comment) explicitly declares the method per
  provider (Zhipu → `local_token_count_x_unit_price`, Luxeno → `subscription_flat_no_attribution`)

- [ ] 5.8 Implement `check_3_day_rolling_history_exists` (§What G, AC-7): scan
  `.aria/cost-snapshots/` for files matching `cost-YYYY-MM-DD.json`; verify ≥3 files with
  consecutive dates ending no earlier than today - 1 day; emit
  `"3-day rolling history: PASS (N files, latest YYYY-MM-DD)"` on success

- [ ] 5.9 Unit test: run `validate-m6-handoff.py --check-abi-compat` against the committed codebase
  (canonical instance test per `[[feedback_validator_repo_drift_guard_test]]`) → exit 0, stdout
  contains all 5 promise IDs without any `FAIL` line

- [ ] 5.10 Unit test: run `validate-m6-handoff.py --check-3-day-history` with a mock
  `.aria/cost-snapshots/` containing exactly 3 consecutive-date files (today-3, today-2, today-1) →
  exit 0; with only 2 files → exit non-zero

---

## T-docs — AD-M6-* slots (~0.5h)

- [ ] 6.1 Add AD-M6-1 slot to `aria-orchestrator/docs/architecture-decisions.md`:
  "cost.json snapshot script integration choice (bash vs Python, standalone vs cron extension)"

- [ ] 6.2 Add AD-M6-2 slot: "cost-snapshots/ archive naming + retention policy"

- [ ] 6.3 Add AD-M6-3 slot: "validate-m6-handoff.py exit code semantics + output format"

---

## T-prd — PRD cross-ref verify (~0.5h)

- [ ] 7.1 Verify PRD §M6 lines 638-646 already reflect the Q-final-2 Path a dual-track cost gate patch
  (metered_usd + subscription_usd language); if not yet patched, note for owner action (owner-blocking,
  not AI-runnable per `[[feedback_t15_owner_blocking_pattern]]`)

- [ ] 7.2 Verify US-026 `docs/requirements/user-stories/US-026.md` references Spec #1 change ID
  `aria-2.0-m6-cost-acceptance`; update if missing

---

## Ordering dependencies

```
T-schema (1.1-1.4)          — no upstream Spec code deps; reads existing dispatches schema
    │
    ├── T-config (2.1-2.3)  — parallel with T-schema
    │
    └── T-alarm (3.1-3.6)   — depends on T-schema (reads cost.json) + T-config (reads thresholds)
            │
            └── T-acceptance (4.1-4.4)  — depends on T-schema + T-config outputs

T-validate (5.1-5.10)       — depends on T-schema (cost.json format known) but independent of T-alarm
                              (5.1-5.8 can proceed in parallel with T-alarm)
                              5.9 canonical instance test requires codebase to be committed with M5 code
                              (already true — M5 archived 2026-05-23, no further changes expected)

T-docs (6.1-6.3)            — parallel with all above (documentation slots)
T-prd (7.1-7.2)             — parallel with all above (verify-only, no code change)
```

---

## Precision items cross-reference

| Precision item | DEC source | §What section | Task(s) |
|----------------|------------|---------------|---------|
| P-1: subscription.tokens_used informational + window dates | DEC §4 ai-R3CH-2 | §What A (field semantics block) | T1.2 |
| P-2: cost_measurement_method enum in validate-m6-handoff.py | DEC §4 qa-M-qa-R3-3 | §What F (validate check description) | T5.7 |
| P-3: validate-m6-handoff.py cross-check all 5 m5-handoff.yaml abi_compat promises | DEC §4 backend M-ba-R3-1c | §What F + §Constraints | T5.2–T5.6, T5.9 |

---

## Status

**Draft (Phase A.1)** — Ready for Phase A.2 post_spec audit (2-agent recommended: backend-architect + qa-engineer per Spec #1 scope; or 4-agent per full Aria default).

**Approved 锁定后** → Phase A.3 → Phase B.1 branch creation → Phase B.2 implementation.
