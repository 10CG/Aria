# Aria 2.0 M6 Spec #1 — Cost Acceptance (dual-track schema + cron sentinel + alarm)

> **⚠️ POST-ARCHIVE CORRECTION (2026-05-30 emergency hotfix)**: The cost-aggregation
> SQL shown below uses `created_at > datetime(...)` — but `created_at` is **NOT a column
> on the `dispatches` table** (it only exists as a `schema_meta` key). This assumption was
> never validated against canonical `schema.sql` and shipped non-functional (smoke
> `no such column: created_at` on prod 2026-05-30). **Corrected to**
> `COALESCE(cycle_start_ts, state_entered_at) > datetime(...)` (owner-ratified). Do NOT
> copy the original SQL below. See `aria-orchestrator/acceptance/m6-cost-snapshot.py` +
> `tests/acceptance/test_m6_cost_snapshot_real_schema.py` (real-schema regression gate).

> **Level**: 3 (Full — cross-cuts aria-orchestrator + .aria/config.json + validate-m6-handoff.py + Feishu webhook + audit-log immutability cross-check)
> **Status**: **Implemented** (Phase B+C SHIPPED 2026-05-27; Phase D.2 archive 2026-05-28). Phase A.2 CONVERGED 2026-05-24 via R3 stability; Phase B+C closed via aria-orchestrator PR #19 merged at `a531f10` → Aria main submodule pointer bump `01bfd5c`; 5 B.2 commits; 87/87 tests PASS; post_impl R1 NEEDS_FIX 3/3 → 14 IDs CLOSED; R2 non-NEEDS_FIX 3/3 → 2 advisory CLOSED; 2 deferred follow-ups (I-cr-R2-1 + I-tl-R2-1) tracked separately.
> **Change ID**: `aria-2.0-m6-cost-acceptance`
> **Parent US**: [US-026](../../../docs/requirements/user-stories/US-026.md)
> **Parent PRD**: [prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) (Week 26-30, ~82h total, post `a786444` PRD patch, §638-646)
> **Predecessor Spec**: [aria-2.0-m5-replay-reconciler-drift-review-loop-audit](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/proposal.md) (M5 archived 2026-05-23)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2, CONVERGED 2026-05-24)
> **Effort baseline**: ~12h impl (updated from ~10h after R1 adds T3.7/T3.8 + T4.5/T4.6 + T5.11; see §Effort baseline). R1/R2 audit cycle adds ~1h review overhead (not impl) — single SoT per `[[feedback_spec_v2_body_propagation_2pass]]`; <!-- R2-cr-I1 fix: effort SoT unified to ~12h impl across frontmatter / §What / §Effort baseline / tasks.md -->.
> **abi_compat hard constraints**: 5 forward-binding promises from m5-handoff.yaml (validate-m6-handoff.py must cross-check all 5; source: `aria-orchestrator/docs/m5-handoff.yaml` line 151-172)
>   1. `dispatch_audit_log_immutable_promise` (line 152-155, AD-M5-8)
>   2. `rework_round_cap_default_3_promise` (line 156-159, AD-M5-2)
>   3. `spec_drift_threshold_default_70_promise` (line 160-163, AD-M5-5)
>   4. `comment_poll_direct_transition_promise` (line 164-167, AD-M5-1)
>   5. `risk_tier_dual_write_literal_always_promise` (line 168-171, AD-M5-8)
> **AD allocation reservation**: AD-M6-1 / AD-M6-2 / AD-M6-3 are reserved for **this Spec #1** only.
> Specs #2 / #3 / #4 must start from AD-M6-4 onwards. (per Q4, 2026-05-24)
> **Audit trajectory**:
>   - Phase A.2 R1 (2026-05-24, 4-agent parallel: tech-lead-critic + qa + ai + code-reviewer): NEEDS_FIX 4/4 — 12 Critical + 20 Important (de-dup → 11 themes + 8 themes); aggregate at `post_spec-R1-aggregate-2026-05-24-aria-2.0-m6-cost-acceptance.md`
>   - Phase A.2 R1-fix applied (commit `0d4a317`, backend-architect pass): 11C + 8I + Q1-Q4 owner decisions
>   - Phase A.2 R2 challenge (2026-05-24, 3-agent: cr + ai + tl-critic): SCOPE_OK_R2 conditional 3/3 — 1 NEW Critical (self-spot REPO_ROOT off-by-1) + 2 Important; 90.6% R1 reduction
>   - Phase A.2 R2-fix applied (commit `75a399d`): C-tl-N1 REPO_ROOT canonical 2-level + cr-I1 effort SoT unified ~12h impl + ai-NI-1 AC-2b orphan NULL check
>   - Phase A.2 R3 stability (2026-05-24, tech-lead-critic 1-agent scope-limited): **R3_STABLE** — 0 new C + 0 new I; 3/3 R2 fixes CLOSED + 2 trivial observations (cosmetic, non-blocking)
>   - **CONVERGED** 2026-05-24 — ready for Phase A.3 (agent allocation) → Phase B.1 (branch creation)

---

## Why

M5 shipped a production-grade autonomous dispatch loop capable of "can-run + can-be-trusted + can-self-manage"
(Track A T-deploy 2026-05-23, real LLM dispatch DEMO-M5-O3 verified). Before Aria 2.0 releases under a
"verified autonomous" label, the PRD requires evidence that the system operates within cost bounds
across both provider tiers.

The cost problem is structurally dual-track — `[[project_glm_routing_luxeno]]` established that:
- **Layer 1 (Luxeno)**: flat monthly subscription; no per-dispatch cost attribution is possible or correct.
  Attributing `cost_usd=0` per dispatch is a silent false-positive that would prevent alarms from firing.
  This is the Luxeno=0 false-alarm failure mode identified in DEC brainstorm R2 ai-CH-3.
- **Layer 2 (Zhipu / Z.AI)**: metered per-token; per-dispatch cost_usd is additive and can be summed.

Without a dual-row schema, a single cost.json row either merges incompatible semantics (mixing additive
per-dispatch Zhipu costs with a non-attributable Luxeno flat fee) or silently omits one provider.

Three additional problems this Spec addresses:

1. **No freshness gate**: cost.json written by a previous cron tick cannot be trusted if the data is stale;
   an acceptance gate that reads a 48h-old file would silently pass with outdated numbers.

2. **No alarm path**: without an automated sentinel, owner must manually check cost.json daily.
   At ~10+ dispatches/day under Luxeno subscription, the subscription cost-effectiveness gate (PRD §645)
   depends on trending data being continuously written and monitored.

3. **No abi_compat cross-check for M6**: M5 shipped 5 forward-binding promises
   (`aria-orchestrator/docs/m5-handoff.yaml` line 151-172). M6 Spec #1 is the first Spec in M6 scope and
   must establish validate-m6-handoff.py with those 5 promise checks from day one, before any M6 code
   changes could inadvertently violate them — per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`.

**Gate role in M6 sequencing**: Spec #2 (`aria-2.0-m6-e2e-resilience`) requires ≥3 consecutive daily
cost.json snapshots already written before its 7-day E2E run begins. Spec #1 must land first, and the
owner must manually run the cron daily for ≥3 days before Spec #2 kickoff (per cr-CH-9 closure).

---

## What

### In scope (~12h impl)

#### A. Dual-row cost.json schema (2h)

<!-- R1-C8 fix: §What E and §How diagram changed from .sql to .py throughout -->
Write a cron script (`aria-orchestrator/acceptance/m6-cost-snapshot.py`) that
produces `.aria/cost.json` with exactly two top-level keys:

```jsonc
{
  "metered_usd": {
    "provider": "zhipu",
    "model": "<model_id>",
    "input_tokens": <int>,
    "output_tokens": <int>,
    "cost_usd": <float>,
    "note": "Additive per-dispatch."
  },
  "subscription_usd": {
    "provider": "luxeno",
    "model": "<model_id>",
    "cost_usd": null,
    "attribution_disclaimer": "subscription billing, no per-dispatch attribution",
    "tokens_used": <int_or_null>,
    "window_start_iso": "<ISO-8601>",
    "window_end_iso": "<ISO-8601>"
  },
  "freshness_ts": "<RFC-3339-UTC+00:00>"
}
```

Field semantics (P-1, DEC §4 ai-R3CH-2 closure):
- `subscription_usd.cost_usd` MUST be `null` — NOT zero, not omitted. `null` signals "unattributable
  per dispatch" (subscription billing). Any consumer that computes `month_to_date_cost >= 0.8 * threshold`
  for Luxeno MUST guard `if cost_usd is null: skip alarm logic` (Luxeno=0 false-positive prevention).
- `subscription_usd.tokens_used` is informational only; it MUST NOT be used to compute cost_usd.
  If the Luxeno API does not expose per-period token count, this field is `null`.
- `subscription_usd.window_start_iso` / `window_end_iso` identify the billing cycle the snapshot
  corresponds to (e.g. current calendar month). Used to correlate trending data, not for cost math.
- `metered_usd.cost_usd` is the SQLite aggregate `SUM(token_cost_usd)` for Zhipu-routed dispatches
  within the rolling 30-day window. The query filters by `provider_cost_model='metered'` (not by a
  `provider` column — the dispatches table has no `provider` column; it has `provider_cost_model`).
  The aggregate is cast to `float` explicitly: `float(cursor.fetchone()[0] or 0.0)`.
- `freshness_ts` MUST be serialized as `datetime.now(timezone.utc).isoformat()`, which produces an
  explicit `+00:00` suffix (e.g., `2026-05-24T12:00:00+00:00`). Never bare `Z`, never naive.

<!-- R1-C3 fix: absolute repo-relative paths specified here for implementer clarity -->
The cost aggregation query reads from `aria-orchestrator` SQLite (dispatches table `token_cost_usd`
column at `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/schema.sql`, already written
per-dispatch by M2 `update_token_usage` path). No new schema migration needed — this Spec is additive
(reads existing columns, writes a JSON artifact).

<!-- R1-I-1 fix: atomic write pattern required -->
<!-- R1-I-6 fix: atomic write also for archive copy -->
The snapshot script MUST use atomic write for both outputs:
1. Write to `.aria/cost.json.tmp`, then `os.rename('.aria/cost.json.tmp', '.aria/cost.json')`.
2. Write to `.aria/cost-snapshots/cost-YYYY-MM-DD.json.tmp`, then `os.rename()` to final path.
This prevents a mid-write Nomad kill from producing corrupt JSON. Concurrent reader/writer safety
is achieved via atomic rename (not file locking); document this in AD-M6-2.

#### B. Owner-set thresholds in .aria/config.json (1h)

Add key under existing `.aria/config.json`:

```jsonc
"m6": {
  "cost_thresholds": {
    "zhipu_30d_usd": <float>,      // owner-set; PRD §643 "(ii) monthly ≤ $Y"
    "luxeno_monthly_usd": <float>  // owner-set; PRD §643 "(i) monthly ≤ $X"
  }
}
```

Document the threshold semantics: `zhipu_30d_usd` applies to the rolling 30-day `metered_usd.cost_usd`
sum; `luxeno_monthly_usd` applies to the owner's actual monthly Luxeno invoice (NOT the derived null
cost_usd — it is a manual reference threshold for owner awareness, not automated computation).

#### C. freshness_ts gate (0.5h, threaded into snapshot script + acceptance check)

The cron script writes `freshness_ts` as described in §A (RFC-3339 UTC with `+00:00` suffix).

Acceptance gate definition: `now - freshness_ts > 86400 seconds` → cost.json is stale; the entire
Spec #1 acceptance check is rejected with a stale-data error. This prevents passing acceptance
on a 48h-old snapshot.

#### D. Cron sentinel + alarm path (3h)

<!-- R1-C11 fix: added §D.iii dispatch volume floor per PRD §645 -->
A Nomad periodic job (or extension to existing `aria-layer1-cron`) runs the cost snapshot script
daily.

**D.i — Zhipu 80% cost threshold alarm**

On completion, if `metered_usd.cost_usd >= 0.8 * m6.cost_thresholds.zhipu_30d_usd`, send a
Feishu warning card via the existing `ARIA_FEISHU_WEBHOOK_URL` nomad var (no new var creation).

Luxeno alarm: because `subscription_usd.cost_usd` is `null`, the 80% alarm for Luxeno is
**owner-manual** (owner reviews monthly invoice against `luxeno_monthly_usd` threshold). The cron
script MUST NOT treat `null` as 0 when evaluating the Luxeno alarm path — doing so would silence
alarms that should fire (Luxeno=0 false-positive). The script logs a reminder
`"Luxeno subscription: manual invoice review required (cost_usd not per-dispatch attributable)"`.

<!-- R1-I-3 fix: ARIA_FEISHU_WEBHOOK_URL absence caught around alarm send only, not snapshot write -->
If `ARIA_FEISHU_WEBHOOK_URL` is absent at runtime, the cron script MUST:
1. Write cost.json successfully (do NOT abort snapshot write due to missing alarm config).
2. Log `[WARN] alarm-skipped: ARIA_FEISHU_WEBHOOK_URL not configured; Feishu alarm suppressed`.
3. Exit 0 (cron must not fail due to missing alarm config).
The `NotConfigured` exception from `feishu_webhook.py` MUST be caught around the `feishu_send`
call only — not around the snapshot write path.

Feishu alarm card fields: `provider`, `cost_usd`, `threshold`, `pct_used` (integer 0-100), `freshness_ts`, `action_url`.

<!-- R1-C5 fix: pct_used defined as integer 0-100; decimal arithmetic required -->
`pct_used` is an **integer 0-100** (e.g., 80, not 0.80). Computed as `int(round(cost_usd / threshold * 100))`.
Use `decimal.Decimal` arithmetic in threshold comparisons to avoid IEEE-754 drift at non-round thresholds.

**D.ii — Luxeno manual review reminder**

The cron script always logs (regardless of alarm threshold):
`"Luxeno subscription: manual invoice review required (cost_usd not per-dispatch attributable)"`

**D.iii — Dispatch volume floor check**

<!-- R1-C11 fix: new section per PRD §645 "≥10/day under flat-rate" requirement -->
Per PRD §645 "(iii) Dispatch volume floor: ≥10/day under flat-rate (Luxeno subscription
cost-effectiveness gate; below floor → reconsider subscription vs metered routing)":

The cron script computes the 7-day rolling average of dispatches under `provider_cost_model=
'subscription_flat'`:

```sql
SELECT COUNT(*) / 7.0
FROM dispatches
WHERE provider_cost_model = 'subscription_flat'
  AND created_at > datetime('now', '-7 days')
```

<!-- R1-C1 fix: WHERE provider_cost_model='subscription_flat' not WHERE provider='luxeno' -->
If this average is **strictly less than 10 dispatches/day**, emit a Feishu info card with
severity=info (not warning), title `"Luxeno volume floor reminder"`, body:
`"Luxeno dispatch volume below subscription-effectiveness floor (N=<avg_per_day>, floor=10); consider routing reconfiguration."`.

Volume floor check is independent of the 80% cost alarm. Both may fire in the same cron run.

#### E. Acceptance script (1.5h, binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`)

<!-- R1-C8 fix: script extension locked as .py everywhere -->
A standalone Python script `aria-orchestrator/acceptance/check-m6-cost-acceptance.py` (calling
SQLite) that emits binary PASS/FAIL for each criterion. See §Acceptance criteria for the exact
checks.

<!-- R1-C7 fix: exit code contract lifted from AD-M6-3 defer to Spec body per Q1 -->
**Exit code contract** (owner decision Q1, 2026-05-24):
- `exit 0` — all sub-checks (AC-1..AC-4) PASS.
- `exit 1` — one or more AC sub-checks FAIL (data condition: stale data, wrong schema, null guard violation, missing or invalid threshold value).
- `exit 2` — infrastructure error that prevents evaluation:
  - `.aria/cost.json` absent (emit `[ERROR] AC-0: cost.json not found — cron has never run`)
  - corrupt JSON in cost.json or config.json (emit `[ERROR] AC-0: JSON parse error: <filename>`)
  - `.aria/config.json` absent or `m6.cost_thresholds` key missing
  - `ARIA_FEISHU_WEBHOOK_URL` absent ONLY when the alarm send path is the specific sub-check under test

Each sub-check emits `[PASS] AC-N: <name>` or `[FAIL] AC-N: <reason>` (or `[ERROR] AC-0: <reason>` for infra failures).

#### F. validate-m6-handoff.py with 5 abi_compat promise checks (2h, P-3)

A new `aria-orchestrator/docs/validate-m6-handoff.py` script (sibling to `validate-m5-handoff.py`)
that cross-checks all 5 m5-handoff.yaml abi_compat promises are still honoured in the codebase.

<!-- R1-C3 fix: all grep targets use absolute repo-relative paths (REPO_ROOT resolution pattern) -->
<!-- R2-C-tl-N1 fix: REPO_ROOT off-by-1 corrected — mirrors validate-m5-handoff.py:40-41 line-for-line (HERE.parent, NOT .parent.parent.parent) -->
The script resolves paths using the canonical sibling pattern (line-for-line mirror of
`aria-orchestrator/docs/validate-m5-handoff.py:40-41`):
```python
HERE = Path(__file__).resolve().parent      # → aria-orchestrator/docs/
REPO_ROOT = HERE.parent                     # → aria-orchestrator/  (NOT main repo root /home/dev/Aria/)
```
All file targets use absolute paths anchored at `aria-orchestrator/`:
- Python sources: `REPO_ROOT / "hermes-extensions" / "aria-layer1" / "aria_layer1" / "*.py"`
- SQL migrations: `REPO_ROOT / "hermes-extensions" / "aria-layer1" / "migrations" / "*.sql"`
- Schema: `REPO_ROOT / "hermes-extensions" / "aria-layer1" / "aria_layer1" / "schema.sql"`

The 5 checks (per DEC §4 backend M-ba-R3-1c):

1. `check_dispatch_audit_log_immutable` — assert `schema.sql` still contains `audit_no_update` and
   `audit_no_delete` trigger name strings (positive grep on schema.sql); assert `004_schema_v4_additive.sql`
   does NOT contain `DROP TRIGGER` (negative grep — trigger names absent from migration file means
   triggers are not dropped).
2. `check_rework_round_cap_default_3` — grep `extension.py` for literal `3` as default in
   `_read_rework_max_round`; fail if default value is not `3`.
3. `check_spec_drift_threshold_default_70` — grep `reconciler.py` for literal `70` as default in
   `_read_spec_drift_threshold`; fail if default value is not `70`.
4. `check_comment_poll_direct_transition` — grep `comment_poll.py` using
   `re.search(r'^\s*[^#]*_handle_s7_human_gate\s*\(', content, re.MULTILINE)` to exclude commented-out
   or dead-code-wrapped calls; assert match exists (call is present and non-commented).
5. `check_risk_tier_dual_write_literal_always` — grep dispatcher/db INSERT path using
   `re.search(r"INSERT.*risk_tier_stub.*'always'", content, re.DOTALL)` (anchored to INSERT context,
   not any occurrence of `'always'`); fail if pattern is absent.

In addition: `validate-m6-handoff.py` must include `check_cost_measurement_method_enum` (P-2, DEC §4
qa-M-qa-R3-3).

<!-- R1-C9 fix: provider_api_billing kept as RESERVED with explicit forward-compat note -->
**Provider → cost_measurement_method mapping (locked, no enum drift)**:

| Provider | Method | Source |
|----------|--------|--------|
| `zhipu` | `local_token_count_x_unit_price` | `zhipu_pricing._PRICING` table; Zhipu API response does NOT return `cost_usd` field — cost is computed locally from token counts |
| `luxeno` | `subscription_flat_no_attribution` | flat subscription; per-call attribution structurally impossible |
| *(reserved)* | `provider_api_billing` | RESERVED for future providers (e.g., AWS Bedrock billing export, OpenAI `/v1/usage`); **no current Aria provider** exposes per-call `cost_usd` in API response |

`check_cost_measurement_method_enum`: validates that for each provider row in cost.json, the
`cost_measurement_method` field (if present) is one of the three enum values above. If the field is
absent from cost.json (current schema does not include it), this check emits
`[WARN] cost_measurement_method field absent from cost.json; advisory in M6, promoted to FAIL in M7+`
and exits 0 (warning-only in M6).

Additionally: `check_cost_measurement_method_enum` asserts that `zhipu_client.py`'s `_post_chat`
return dict does NOT contain a `cost_usd` key — confirming `local_token_count_x_unit_price` is the
correct enum for Zhipu. This check fails if someone refactors `zhipu_client.py` to expose a
`cost_usd` field without updating the enum mapping.

<!-- R1-C10 + Q2 fix: check_zhipu_pricing_freshness added to validate-m6-handoff.py -->
`validate-m6-handoff.py` must also include `check_zhipu_pricing_freshness` (Q2, 2026-05-24):

- Parse `_PRICING_REVIEW_DUE` and `_PRICING_OWNER_VERIFIED` from
  `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/zhipu_pricing.py`.
- Exit 1 with `[WARN] zhipu_pricing: _PRICING_REVIEW_DUE ({date}) is in the past — pricing is stale; run owner pricing review ritual` if `_PRICING_REVIEW_DUE < datetime.now(timezone.utc).date()`.
- Exit 1 with `[WARN] zhipu_pricing: _PRICING_OWNER_VERIFIED=False — cost attribution unconfirmed` if `_PRICING_OWNER_VERIFIED == False`.
- This freshness check expands AC-8 (see §Acceptance criteria AC-8).

#### G. 3-day rolling history precondition for Spec #2 (0.5h documentation + manual owner step)

`validate-m6-handoff.py` includes `check_3_day_rolling_history_exists`: verifies that the directory
`.aria/cost-snapshots/` contains ≥3 files matching `cost-YYYY-MM-DD.json` with consecutive dates
ending no earlier than `today - 1 day`.

<!-- R1-C6 fix: algorithm specified precisely -->
**Algorithm** (consecutive-day check):
- "Today" is defined as `datetime.now(timezone.utc).date()`.
- Extract all dates from `cost-YYYY-MM-DD.json` filenames in `.aria/cost-snapshots/`.
- Sort descending; take the 3 most-recent dates.
- Check passes if AND ONLY IF:
  (a) ≥3 files exist matching the pattern.
  (b) The 3 most-recent dates form a consecutive sequence with no gaps:
      `date[i+1] == date[i] + timedelta(days=1)` for each adjacent pair.
  (c) The most recent date is no earlier than `today - 1 day`.
- A set of `[today-4, today-2, today-1]` files (gap at `today-3`) FAILS condition (b)
  even though it has ≥3 files — the gap is detected.

This file is a gate for Spec #2 startup: Spec #2 e2e-resilience MUST NOT start its 7-day run until
this check passes. Owner manual action: after Spec #1 ships, run the cron manually daily for ≥3 days
to accumulate the required history (OR wait for natural cron cadence).

### Out of scope (explicit drops per DEC §3 and R3 decisions)

| ID | Description | Drop reason |
|----|-------------|-------------|
| OOS-1 | Real-time cost dashboard (PRD §352 explicit deferral) | PRD §352: "M6 后考虑, MVP 不做"; added complexity for zero MVP value |
| OOS-2 | Real-time alarm below 80% threshold | Only 80% warn + manual review in scope; sub-threshold monitoring is OOS |
| OOS-3 | Cross-project cost aggregation (SilkNode / Kairos) | Single-project (Aria) perspective only; per DEC §2 Spec #1 scope |
| OOS-4 | Cost projection / forecasting | Spec #2 TG-A range or v2.1; requires trending data Spec #1 does not yet have |
| OOS-5 | 3-day trending data production itself | Spec #1 ships the schema + cron; owner manually runs cron daily ≥3 days before Spec #2 starts |
| OOS-6 | New Feishu webhook nomad var | Reuse `ARIA_FEISHU_WEBHOOK_URL` only; no new secrets |
| OOS-7 | Schema migration to dispatches table | Cost aggregation reads existing M2 columns (`token_cost_usd`); no migration needed |
| OOS-8 | Luxeno per-dispatch attribution computation | Attribution is structurally null per subscription billing; computing it would be mathematically incorrect |
| OOS-9 | M5-OS-PB-1 carry-forward (comment_poll lazy-wire forgejo UX fix) | Owner Q6 decision: "defer all carry-forward"; confirmed dropped 4/4 R3 |
| OOS-10 | FX adapter (CNY → USD conversion at runtime) | USD only in Spec #1. CNY→USD conversion is part of the pricing review ritual: owner manually edits `zhipu_pricing.py` literals during `_PRICING_REVIEW_DUE` refresh. Not a Spec #1 runtime concern. (per Q3, 2026-05-24) |

---

## Constraints

<!-- R1-I-8 + Q3 fix: USD-only constraint clause added -->
### Currency

All `cost_usd` values in this Spec are **USD (ISO 4217)**. There is no FX conversion adapter at
runtime. Zhipu's public prices are denominated in CNY; the owner manually converts to USD when
updating `zhipu_pricing.py` literals during the `_PRICING_REVIEW_DUE` refresh cycle. FX adaptation
is OOS-10 (see above).

### abi_compat hard constraints (M6 must not violate)

| Promise | Requirement | Source | Enforcement |
|---------|------------|--------|-------------|
| `dispatch_audit_log_immutable_promise` | M6 must not DROP `audit_no_update` / `audit_no_delete` triggers | m5-handoff.yaml line 152-155 | `validate-m6-handoff.py::check_dispatch_audit_log_immutable` |
| `rework_round_cap_default_3_promise` | M6 must not change `ARIA_REWORK_MAX_ROUND` default=3 in code; nomadVar override only | m5-handoff.yaml line 156-159 | `validate-m6-handoff.py::check_rework_round_cap_default_3` |
| `spec_drift_threshold_default_70_promise` | M6 must not change `ARIA_SPEC_DRIFT_THRESHOLD` default=70 in code | m5-handoff.yaml line 160-163 | `validate-m6-handoff.py::check_spec_drift_threshold_default_70` |
| `comment_poll_direct_transition_promise` | M6 must not revert S7→S8 to cron-only; comment-poll direct call must remain primary | m5-handoff.yaml line 164-167 | `validate-m6-handoff.py::check_comment_poll_direct_transition` |
| `risk_tier_dual_write_literal_always_promise` | M6 must dual-write real value AND still write `'always'` to `risk_tier_stub` when algo ships | m5-handoff.yaml line 168-171 | `validate-m6-handoff.py::check_risk_tier_dual_write_literal_always` |

This Spec introduces no new abi_compat promises (cost schema is additive; no new abi_compat forward-binding to M7 identified at this stage).

### Platform

Implementation target: Linux only (Nomad alloc running Python 3.9+ per aria-layer1 container image).
macOS/Windows compatibility is not required. POSIX `os.rename()` atomicity assumed.

---

## How

### Technical approach

Cost data pipeline:
```
dispatches.token_cost_usd (per-dispatch, written by M2 ProviderRouter)
    │ SQLite SUM WHERE provider_cost_model='metered' AND created_at > now-30d
    ▼
metered_usd.cost_usd  (rolling 30d aggregate, written to .aria/cost.json)

Luxeno API (or manual input)
    │ tokens_used (informational) + window dates
    ▼
subscription_usd  (null cost_usd, written to .aria/cost.json)

.aria/cost.json  (atomic write via os.rename)
    │ daily cron writes
    │ each run also archives to .aria/cost-snapshots/cost-YYYY-MM-DD.json (atomic)
    ▼
check-m6-cost-acceptance.py  →  PASS/FAIL per criterion (exit 0/1/2)
validate-m6-handoff.py       →  5 abi_compat promise checks + pricing freshness + 3-day history gate
```

<!-- R1-C1 fix: SQL query in diagram uses provider_cost_model='metered', not provider='zhipu' -->

Alarm path:
```
cron script reads .aria/config.json m6.cost_thresholds.zhipu_30d_usd
    │ metered_usd.cost_usd >= 0.80 * threshold  (Decimal arithmetic)
    ▼
Feishu warning card via ARIA_FEISHU_WEBHOOK_URL (existing env var)
    │ Luxeno alarm: null cost_usd → NO automated alarm; log manual-review reminder only
    │
    │ ARIA_FEISHU_WEBHOOK_URL absent → log [WARN] + continue; exit 0
    ▼
Volume floor check:
    │ 7-day avg dispatches WHERE provider_cost_model='subscription_flat' < 10/day
    ▼
Feishu info card "Luxeno volume floor reminder" (severity=info, not warning)
```

<!-- R1-C1 fix: SQL in alarm path diagram uses provider_cost_model='subscription_flat', not provider='luxeno' -->

### Key design decisions (AD-M6-1..AD-M6-3)

<!-- R1-C7 + Q1 fix: AD-M6-3 removed as defer slot; exit code contract lifted to Spec body -->
<!-- R1-I-4 + Q4 fix: AD allocation reservation note added -->

| ID | Topic | Decision |
|----|-------|----------|
| AD-M6-1 | cost.json snapshot script language + integration | Python (same as aria_layer1 runtime; enables unittest mocking). Integrates with existing `aria-layer1-cron` as a new sub-command rather than a new Nomad job. |
| AD-M6-2 | cost-snapshots/ archive naming + retention | Files named `cost-YYYY-MM-DD.json`. Retention: keep last 30 files (30-day rolling); cleanup on each cron run. Atomic write via `os.rename()` for both cost.json and archive copy. Concurrent reader/writer safety via atomic rename (no file locking needed). |
| AD-M6-3 | *(removed)* | Exit code contract lifted to §What E (Spec body) per owner Q1. No Phase B decision needed. |

---

## Acceptance criteria

All criteria are binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`.
No subjective language. Each criterion cites the concrete verifiable evidence.

### AC-1 — cost.json exists and is fresh

<!-- R1-C4 fix: timezone-aware datetime.now(timezone.utc); tzinfo assert; age<0 guard; boundary < 86400 -->
**Evidence**: file `.aria/cost.json` exists AND the following check passes:
```python
import json, sys
from datetime import datetime, timezone
d = json.load(open('.aria/cost.json'))
ts = datetime.fromisoformat(d['freshness_ts'])
if ts.tzinfo is None:
    print('FAIL AC-1: freshness_ts is timezone-naive; snapshot script MUST write UTC+00:00', file=sys.stderr)
    sys.exit(1)
now = datetime.now(timezone.utc)
age = (now - ts).total_seconds()
if age < 0:
    print(f'FAIL AC-1: freshness_ts is in the future (skew={abs(age):.1f}s); verify system clock', file=sys.stderr)
    sys.exit(1)
sys.exit(0 if age < 86400 else 1)
```
The snapshot script MUST write `freshness_ts` as `datetime.now(timezone.utc).isoformat()` (produces
`+00:00` suffix, e.g. `2026-05-24T12:00:00+00:00`). Never bare `Z`, never timezone-naive.
Boundary: `age STRICTLY LESS THAN 86400` seconds (a snapshot exactly 86400 seconds old is STALE).

### AC-2 — dual-row schema correct

**Evidence**:
```python
import json, sys
d = json.load(open('.aria/cost.json'))
assert 'metered_usd' in d, 'missing metered_usd'
assert 'subscription_usd' in d, 'missing subscription_usd'
assert d['metered_usd']['provider'] == 'zhipu', 'metered provider must be zhipu'
assert d['subscription_usd']['provider'] == 'luxeno', 'subscription provider must be luxeno'
assert d['subscription_usd']['cost_usd'] is None, 'Luxeno cost_usd must be null (not 0)'
assert 'attribution_disclaimer' in d['subscription_usd'], 'missing attribution_disclaimer'
assert isinstance(d['metered_usd']['cost_usd'], (int, float)), 'Zhipu cost_usd must be numeric'
assert d['metered_usd']['cost_usd'] >= 0.0, 'Zhipu cost_usd must not be negative'
print('PASS')
```
Must print `PASS` without assertion errors.

### AC-2b — No orphaned NULL `provider_cost_model` rows

<!-- R2-ai-NI-1 fix: NULL provider_cost_model rows would be silently excluded from both metered + subscription_flat aggregates -->

The dispatches table MUST NOT contain rows with `provider_cost_model IS NULL` (M2 migration 002
backfilled historical rows to `subscription_flat`; new inserts always set provider_cost_model).
Such rows would be invisible to AC-2's `WHERE provider_cost_model='metered'` and
`WHERE provider_cost_model='subscription_flat'` aggregates, silently under-counting cost.

Evidence (binary-falsifiable):
```sql
SELECT COUNT(*) AS orphan_rows
FROM dispatches
WHERE provider_cost_model IS NULL;
-- Must return 0. Non-zero → exit 1 (data integrity violation, manual investigation required)
```
Acceptance script reports `[FAIL: AC-2b] orphaned rows=N` with the offending dispatch_ids surfaced
for owner triage (per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`).

### AC-3 — Luxeno=0 false-positive prevention

<!-- R1-C2 fix: AC-3 now asserts the snapshot script's transformation (null guard in code), not the schema column -->
**Evidence**: The snapshots script's null guard is verified at two layers:

**Layer 1 — Code path (primary)**: The cron alarm script, when given a cost.json with
`subscription_usd.cost_usd = null`, does NOT evaluate `null >= 0.8 * threshold` as truthy and
does NOT send a Feishu alarm card for Luxeno. Verified by unit test: mock `cost_usd=null` input
→ assert `feishu_send` was NOT called for the Luxeno row (T3.5).

**Layer 2 — Schema invariant note**: The dispatches table stores `token_cost_usd REAL NOT NULL
DEFAULT 0.0` (schema.sql line 101). Luxeno callers write `cost_usd=0.0` per-dispatch (not NULL).
The `subscription_usd.cost_usd=null` in cost.json is a **snapshot-script transformation**: the
script deliberately sets this field to `null` when the `provider_cost_model='subscription_flat'`
aggregate is computed, because `0.0` would be a false attribution (the schema stores 0.0 per
dispatch as a sentinel, not as a real cost). The null in cost.json is distinct from the 0.0 in
the schema. AC-3 validates the transformation, not the schema column value.

<!-- R1-C1 fix: AC-3 SQL uses provider_cost_model='subscription_flat', not provider='luxeno' -->
Verification query (schema layer): `SELECT COUNT(*) FROM dispatches
WHERE provider_cost_model = 'subscription_flat' AND token_cost_usd IS NOT NULL`
must return 0 after a schema-compliant backfill (or >= 0 for pre-M2 legacy rows where
`provider_cost_model` is NULL, which is acceptable per backfill semantics).

### AC-4 — .aria/config.json thresholds set

**Evidence**:
```python
import json, sys
cfg = json.load(open('.aria/config.json'))
t = cfg['m6']['cost_thresholds']
assert isinstance(t['zhipu_30d_usd'], (int, float)) and t['zhipu_30d_usd'] > 0
assert isinstance(t['luxeno_monthly_usd'], (int, float)) and t['luxeno_monthly_usd'] > 0
print('PASS')
```
Must print `PASS`.

### AC-5 — 80% Feishu alarm fires correctly

<!-- R1-C5 fix: pct_used is integer 0-100; decimal arithmetic in fixture math; above-boundary test added -->
**Evidence**: unit tests with exact IEEE-754-stable threshold arithmetic:

- `test_alarm_at_boundary`: `metered_usd.cost_usd = threshold * Decimal('0.80')` → `feishu_send`
  IS called; card field `pct_used == 80` (integer, range 0-100).
- `test_alarm_below_boundary`: `metered_usd.cost_usd = threshold * Decimal('0.7999')` →
  `feishu_send` NOT called.
- `test_alarm_above_boundary` (T3.4-bis): `metered_usd.cost_usd = threshold * Decimal('0.801')` →
  `feishu_send` IS called.

Boundary semantics: alarm fires when `cost_usd >= 0.80 * threshold` (inclusive ≥).
`pct_used` field unit: integer 0-100 (e.g., 80, NOT 0.80).
Fixtures use `decimal.Decimal` to avoid IEEE-754 drift at non-round thresholds.

### AC-5b — Dispatch volume floor alarm fires correctly

<!-- R1-C11 fix: new AC-5b for volume floor boundary per §D.iii -->
**Evidence**: unit test:
- `test_volume_floor_below`: 7-day average < 10/day → Feishu info card IS emitted with title
  `"Luxeno volume floor reminder"`.
- `test_volume_floor_at_floor`: 7-day average == 10/day → info card NOT emitted (boundary:
  alarm fires on strictly < 10).
- `test_volume_floor_above`: 7-day average > 10/day → info card NOT emitted.

Floor semantics: info card fires when 7-day rolling average is **strictly less than 10 dispatches/day**.

### AC-6 — validate-m6-handoff.py exits 0 with all 5 promise IDs

**Evidence**:
```bash
python3 aria-orchestrator/docs/validate-m6-handoff.py --check-abi-compat
```
- Exit code 0
- stdout contains all 5 promise IDs:
  `dispatch_audit_log_immutable_promise`,
  `rework_round_cap_default_3_promise`,
  `spec_drift_threshold_default_70_promise`,
  `comment_poll_direct_transition_promise`,
  `risk_tier_dual_write_literal_always_promise`
- No line reads `FAIL` or `ERROR`.

### AC-7 — 3-day rolling history exists before Spec #2 kickoff

<!-- R1-C6 fix: algorithm is precisely specified; consecutive-day semantics locked -->
**Evidence**:
```bash
python3 aria-orchestrator/docs/validate-m6-handoff.py --check-3-day-history
```
- Exit code 0
- stdout contains `"3-day rolling history: PASS (N files, latest YYYY-MM-DD)"` where N ≥ 3.
- The 3 most-recent snapshot dates form a consecutive sequence (no gaps).
- The most recent date is no earlier than `datetime.now(timezone.utc).date() - timedelta(days=1)`.

Gap case: `[today-4, today-2, today-1]` (gap at `today-3`) → exit non-zero, `[FAIL] 3-day history:
consecutive gap detected`.

This check MUST pass before Spec #2 `aria-2.0-m6-e2e-resilience` Phase B is permitted to start.

### AC-8 — cost_measurement_method enum documented and pricing freshness validated (P-2)

<!-- R1-C10 + Q2 fix: AC-8 expanded to cover pricing freshness check -->
**Evidence**:
```bash
python3 aria-orchestrator/docs/validate-m6-handoff.py --check-cost-method-enum
```
- Exit code 0 if `cost_measurement_method` field is absent from cost.json (warning emitted, not
  hard fail, in M6).
- Exit code 1 if `cost_measurement_method` is present but contains an invalid enum value.
- Asserts `zhipu_client.py` `_post_chat` return dict does NOT contain `cost_usd` key (confirms
  `local_token_count_x_unit_price` correctness).

```bash
python3 aria-orchestrator/docs/validate-m6-handoff.py --check-pricing-freshness
```
- Exit code 0 if `_PRICING_REVIEW_DUE >= today` AND `_PRICING_OWNER_VERIFIED == True`.
- Exit code 1 (warn) if `_PRICING_REVIEW_DUE < today` OR `_PRICING_OWNER_VERIFIED == False`,
  with labelled `[WARN]` messages.

### AC-9 — acceptance script is binary-falsifiable

<!-- R1-C7 + Q1 fix: exit code contract fully specified; AD-M6-3 defer removed -->
**Evidence**:
```bash
cd aria-orchestrator/acceptance && python3 check-m6-cost-acceptance.py
```
- Exit code 0 when all checks pass.
- Exit code 1 when any AC sub-check fails (data condition).
- Exit code 2 when infrastructure error prevents evaluation (cost.json missing, corrupt JSON,
  config key missing, or env var absent when alarm path is the sub-check under test).
- Script embeds checks for AC-1 through AC-4 as named sub-checks with
  `[PASS] AC-N: <name>` / `[FAIL] AC-N: <reason>` / `[ERROR] AC-0: <reason>` labelled output per check.

---

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-M6-1 | Luxeno API does not expose per-period token count → `tokens_used` always null | Low | Field is marked optional/informational; null is a valid schema value; not used in alarm logic |
| R-M6-2 | `.aria/config.json` threshold not set by owner before acceptance → AC-4 fails | Medium | tasks.md includes task to set example thresholds in config template; acceptance script emits clear error message identifying missing key |
| R-M6-3 | Cron daily run omitted for 3 days → Spec #2 blocked on AC-7 | Medium | Spec #2 Phase B.1 pre-condition explicitly gates on `--check-3-day-history` PASS; documented in Spec #2 proposal (to be written) |
| R-M6-4 | validate-m6-handoff.py grep patterns stale if M5 refactor renames functions post-archive | Low | Script targets archived M5 code (no further changes expected to M5 module after archival 2026-05-23); `[[feedback_scaffold_helpers_drift_without_callers]]` pattern: tests run against committed canonical paths |
| R-M6-5 | mock-shape mismatch in unit test for Luxeno null guard → paper-fix pattern | Medium | Per `[[feedback_test_mock_pattern_hides_prod_bug]]`: unit test must use the actual cron alarm function code, not a mock replacement of the alarm logic itself; only feishu_send is mocked at the transport layer |
| R-M6-6 | Spec body propagation gap: P-1/P-2/P-3 precision items not carried through to tasks.md | Low | Per `[[feedback_spec_v2_body_propagation_2pass]]`: each precision item is explicitly cross-referenced to both §What sections and tasks.md task numbers below |

---

## Effort baseline

```
A. Dual-row cost.json schema + cron script (+ atomic write)      ~2h
B. .aria/config.json threshold keys                              ~1h
C. freshness_ts gate (threaded into A + E)                       ~0.5h
D. Cron sentinel + alarm path (+ vol floor T3.7/T3.8)           ~3h  (+1h from ~2h)
E. Acceptance script (+ T4.5/T4.6 infra failure tests)          ~2h  (+0.5h from ~1.5h)
F. validate-m6-handoff.py (5 abi_compat + P-2 + pricing T5.11)  ~2.5h  (+0.5h from ~2h)
G. 3-day history check (threaded into F)                         ~0.5h
──────────────────────────────────────────────────────────────────────
Total (AI-implementable)                                         ~11.5h ≈ 12h
```

R1 delta: +~2h from original ~10h. Sources: D +1h (T3.7/T3.8 volume floor), E +0.5h (T4.5/T4.6),
F +0.5h (T5.11 pricing freshness). **Implementation baseline: ~12h** (single SoT; cited identically
in frontmatter line 10 + tasks.md line 7 + this section). R1/R2 audit review overhead ~1h is tracked
separately (audit-engine cost, not Phase B implementation). Documented per
`[[feedback_phase_budget_compounding]]` + `[[feedback_spec_v2_body_propagation_2pass]]`.
<!-- R2-cr-I1 fix: effort SoT unified to ~12h impl; removed "~13h conservatively" weasel that drifted across surfaces -->.

Owner manual action (post-ship, not in B.2):
  - Set .aria/config.json thresholds
  - Run cron daily × ≥3 days to accumulate history

---

## Dependencies

| Dependency | Direction | Notes |
|------------|-----------|-------|
| M5 dispatches table `token_cost_usd` + `provider_cost_model` columns | Upstream (already shipped M2+) | Cost aggregation reads these columns; no migration needed |
| `ARIA_FEISHU_WEBHOOK_URL` nomad var | Upstream (already set M4+) | Alarm path reuses; no new var creation |
| `.aria/config.json` existing structure | Upstream | New `m6.cost_thresholds` key added additively |
| `aria-orchestrator/docs/m5-handoff.yaml` | Upstream (archived M5) | validate-m6-handoff.py reads promises from lines 151-172 |
| Spec #2 `aria-2.0-m6-e2e-resilience` | Downstream (gates on AC-7) | Spec #2 Phase B must not start until `--check-3-day-history` PASS |

---

## Cross-references

**Predecessors**:
- [openspec/archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/) — M5 shipped, abi_compat promises source
- [aria-orchestrator/docs/m5-handoff.yaml](../../../aria-orchestrator/docs/m5-handoff.yaml) line 151-172 — 5 forward-binding abi_compat promises

**Sibling Specs (M6 parallel)**:
- [aria-2.0-m6-e2e-resilience](../aria-2.0-m6-e2e-resilience/proposal.md) — gates on Spec #1 AC-7 (3-day history)
- [aria-2.0-m6-docs](../aria-2.0-m6-docs/proposal.md) — parallel, no hard dependency on Spec #1
- [aria-2.0-m6-release-closeout](../aria-2.0-m6-release-closeout/proposal.md) — sequential after all M6 Specs done

**Decisions**:
- [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) — DEC-20260524-001 §2 Spec #1 scope (source-of-truth)
- [.aria/decisions/2026-05-15-m6-brainstorm.md](../../../.aria/decisions/2026-05-15-m6-brainstorm.md) — M6a brainstorm D1-D7 (predecessor context)

**PRD references**:
- [docs/requirements/prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) line 638-646 — M6 cost gate dual-track (Q-final-2 Path a patch)

**Memory entries**:
- `[[project_glm_routing_luxeno]]` — Luxeno (Layer 1 flat subscription) vs Zhipu (Layer 2 metered) routing; foundational for dual-track schema rationale
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — acceptance bools must cite concrete verifiable metric; all ACs in this Spec comply
- `[[feedback_test_mock_pattern_hides_prod_bug]]` — Luxeno=0 false-positive: mock-shape must align with real null semantics; unit test must mock only transport, not alarm logic
- `[[feedback_scaffold_helpers_drift_without_callers]]` — validate-m6-handoff.py grep targets must be verified against committed codebase, not hypothetical paths
- `[[feedback_spec_v2_body_propagation_2pass]]` — P-1/P-2/P-3 precision items are propagated to both §What subsections and tasks.md task numbers (see tasks T1.2/T5.2/T6.1)
- `[[feedback_audit_driven_fix_conventions]]` — inline R1-C*/R1-I-* traces applied throughout this document for R2 auditor traceability
- `[[feedback_phase_budget_compounding]]` — effort baseline bumped ~10h → ~12h after R1 adds net 3 task groups (T3.7/T3.8, T4.5/T4.6, T5.11)
