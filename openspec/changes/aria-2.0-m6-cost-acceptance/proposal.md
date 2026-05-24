# Aria 2.0 M6 Spec #1 — Cost Acceptance (dual-track schema + cron sentinel + alarm)

> **Level**: 3 (Full — cross-cuts aria-orchestrator + .aria/config.json + validate-m6-handoff.py + Feishu webhook + audit-log immutability cross-check)
> **Status**: **Draft** (Phase A.1; pending Phase A.2 post_spec audit)
> **Change ID**: `aria-2.0-m6-cost-acceptance`
> **Parent US**: [US-026](../../../docs/requirements/user-stories/US-026.md)
> **Parent PRD**: [prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) (Week 26-30, ~82h total, post `a786444` PRD patch, §638-646)
> **Predecessor Spec**: [aria-2.0-m5-replay-reconciler-drift-review-loop-audit](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/proposal.md) (M5 archived 2026-05-23)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2, CONVERGED 2026-05-24)
> **Effort baseline**: ~10h (DEC §2 Spec #1 central estimate)
> **abi_compat hard constraints**: 5 forward-binding promises from m5-handoff.yaml (validate-m6-handoff.py must cross-check all 5; source: `aria-orchestrator/docs/m5-handoff.yaml` line 151-172)
>   1. `dispatch_audit_log_immutable_promise` (line 152-155, AD-M5-8)
>   2. `rework_round_cap_default_3_promise` (line 156-159, AD-M5-2)
>   3. `spec_drift_threshold_default_70_promise` (line 160-163, AD-M5-5)
>   4. `comment_poll_direct_transition_promise` (line 164-167, AD-M5-1)
>   5. `risk_tier_dual_write_literal_always_promise` (line 168-171, AD-M5-8)
> **Audit trajectory**:
>   - Phase A.2 R1: pending
>   - Phase A.2 R2: pending

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

### In scope (~10h)

#### A. Dual-row cost.json schema (2h)

Write a cron script (`aria-orchestrator/acceptance/m6-cost-snapshot.sh` or Python equivalent) that
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
  "freshness_ts": "<ISO-8601-UTC>"
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
  within the rolling 30-day window queried from the dispatches table.

The cost aggregation query reads from `aria-orchestrator` SQLite (dispatches table `token_cost_usd` column,
already written per-dispatch by M2 `update_token_usage` path). No new schema migration needed — this Spec
is additive (reads existing columns, writes a JSON artifact).

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

#### C. freshness_ts gate (0.5h, threaded into snapshot script + acceptance SQL)

The cron script writes `freshness_ts` as the UTC ISO-8601 timestamp at snapshot time.

Acceptance gate definition: `now - freshness_ts > 86400 seconds` → cost.json is stale; the entire
Spec #1 acceptance check is rejected with a stale-data error. This prevents passing acceptance
on a 48h-old snapshot.

#### D. Cron sentinel + alarm path (2h)

A Nomad periodic job (or extension to existing `aria-layer1-cron`) runs the cost snapshot script
daily. On completion, if `metered_usd.cost_usd >= 0.8 * m6.cost_thresholds.zhipu_30d_usd`, send a
Feishu warning card via the existing `ARIA_FEISHU_WEBHOOK_URL` nomad var (no new var creation).

Luxeno alarm: because `subscription_usd.cost_usd` is `null`, the 80% alarm for Luxeno is
**owner-manual** (owner reviews monthly invoice against `luxeno_monthly_usd` threshold). The cron
script MUST NOT treat `null` as 0 when evaluating the Luxeno alarm path — doing so would silence
alarms that should fire (Luxeno=0 false-positive). The script logs a reminder
`"Luxeno subscription: manual invoice review required (cost_usd not per-dispatch attributable)"`.

Feishu alarm card fields: `provider`, `cost_usd`, `threshold`, `pct_used`, `freshness_ts`, `action_url`.

#### E. Acceptance SQL script (1.5h, binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`)

A standalone SQL + Python script `aria-orchestrator/acceptance/check-m6-cost-acceptance.sql` (or
Python wrapper calling SQLite) that emits binary PASS/FAIL for each criterion. See §Acceptance
criteria for the exact SQL queries.

#### F. validate-m6-handoff.py with 5 abi_compat promise checks (2h, P-3)

A new `aria-orchestrator/docs/validate-m6-handoff.py` script (sibling to `validate-m5-handoff.py`)
that cross-checks all 5 m5-handoff.yaml abi_compat promises are still honoured in the codebase.
The 5 checks (per DEC §4 backend M-ba-R3-1c):

1. `check_dispatch_audit_log_immutable` — assert `schema.sql` still contains `audit_no_update` and
   `audit_no_delete` trigger definitions; assert `004_schema_v4_additive.sql` has not been modified
   to DROP those triggers.
2. `check_rework_round_cap_default_3` — grep `extension.py` for literal `3` as default in
   `_read_rework_max_round`; fail if default value is not `3`.
3. `check_spec_drift_threshold_default_70` — grep `reconciler.py` for literal `70` as default in
   `_read_spec_drift_threshold`; fail if default value is not `70`.
4. `check_comment_poll_direct_transition` — grep `comment_poll.py` for the `_handle_s7_human_gate`
   direct call wiring; assert it is not removed or bypassed.
5. `check_risk_tier_dual_write_literal_always` — grep dispatcher/db INSERT path for `'always'`
   literal written to `risk_tier_stub`; fail if literal is absent.

In addition: `validate-m6-handoff.py` must include `check_cost_measurement_method_enum` (P-2, DEC §4
qa-M-qa-R3-3): validates that the cost snapshot output's `cost_measurement_method` field (if present
in the schema) is one of the explicit enum values:
`{provider_api_billing, local_token_count_x_unit_price, subscription_flat_no_attribution}`.
If the field is absent from cost.json (current schema does not include it), this check verifies that
the schema document explicitly lists which method applies to each provider row.

#### G. 3-day rolling history precondition for Spec #2 (0.5h documentation + manual owner step)

`validate-m6-handoff.py` includes `check_3_day_rolling_history_exists`: verifies that the directory
`.aria/cost-snapshots/` contains ≥3 files matching `cost-YYYY-MM-DD.json` with consecutive dates
ending no earlier than `today - 1 day` (i.e., at least the prior 3 calendar days have a snapshot).

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

---

## How

### Technical approach

Cost data pipeline:
```
dispatches.token_cost_usd (per-dispatch, written by M2 ProviderRouter)
    │ SQLite SUM WHERE provider='zhipu' AND created_at > now-30d
    ▼
metered_usd.cost_usd  (rolling 30d aggregate, written to .aria/cost.json)

Luxeno API (or manual input)
    │ tokens_used (informational) + window dates
    ▼
subscription_usd  (null cost_usd, written to .aria/cost.json)

.aria/cost.json
    │ daily cron writes
    │ each run also archives to .aria/cost-snapshots/cost-YYYY-MM-DD.json
    ▼
check-m6-cost-acceptance.sql  →  PASS/FAIL per criterion
validate-m6-handoff.py        →  5 abi_compat promise checks + 3-day history gate
```

Alarm path:
```
cron script reads .aria/config.json m6.cost_thresholds.zhipu_30d_usd
    │ metered_usd.cost_usd >= 0.80 * threshold
    ▼
Feishu warning card via ARIA_FEISHU_WEBHOOK_URL (existing env var)
    │ Luxeno alarm: null cost_usd → NO automated alarm; log manual-review reminder only
```

### Key design decisions (AD-M6-1..AD-M6-3, to be filled during Phase B)

| ID | Topic | Phase | Status |
|----|-------|-------|--------|
| AD-M6-1 | cost.json snapshot script language (bash vs Python) + integration with existing cron job | Phase B | _slot_ |
| AD-M6-2 | cost-snapshots/ archive naming + retention (how many days kept, cleanup policy) | Phase B | _slot_ |
| AD-M6-3 | validate-m6-handoff.py: exit code semantics + stdout format (machine-readable vs human prose) | Phase B | _slot_ |

---

## Constraints (abi_compat hard constraints, M6 must not violate)

| Promise | Requirement | Source | Enforcement |
|---------|------------|--------|-------------|
| `dispatch_audit_log_immutable_promise` | M6 must not DROP `audit_no_update` / `audit_no_delete` triggers | m5-handoff.yaml line 152-155 | `validate-m6-handoff.py::check_dispatch_audit_log_immutable` |
| `rework_round_cap_default_3_promise` | M6 must not change `ARIA_REWORK_MAX_ROUND` default=3 in code; nomadVar override only | m5-handoff.yaml line 156-159 | `validate-m6-handoff.py::check_rework_round_cap_default_3` |
| `spec_drift_threshold_default_70_promise` | M6 must not change `ARIA_SPEC_DRIFT_THRESHOLD` default=70 in code | m5-handoff.yaml line 160-163 | `validate-m6-handoff.py::check_spec_drift_threshold_default_70` |
| `comment_poll_direct_transition_promise` | M6 must not revert S7→S8 to cron-only; comment-poll direct call must remain primary | m5-handoff.yaml line 164-167 | `validate-m6-handoff.py::check_comment_poll_direct_transition` |
| `risk_tier_dual_write_literal_always_promise` | M6 must dual-write real value AND still write `'always'` to `risk_tier_stub` when algo ships | m5-handoff.yaml line 168-171 | `validate-m6-handoff.py::check_risk_tier_dual_write_literal_always` |

This Spec introduces no new abi_compat promises (cost schema is additive; no new abi_compat forward-binding to M7 identified at this stage).

---

## Acceptance criteria

All criteria are binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`.
No subjective language. Each criterion cites the concrete verifiable evidence.

### AC-1 — cost.json exists and is fresh

**Evidence**: file `.aria/cost.json` exists AND:
```bash
python3 -c "
import json, datetime, sys
d = json.load(open('.aria/cost.json'))
ts = datetime.datetime.fromisoformat(d['freshness_ts'].rstrip('Z'))
age = (datetime.datetime.utcnow() - ts).total_seconds()
sys.exit(0 if age < 86400 else 1)
"
```
Exit code 0 = PASS; exit code 1 = stale (fail acceptance).

### AC-2 — dual-row schema correct

**Evidence**:
```bash
python3 -c "
import json, sys
d = json.load(open('.aria/cost.json'))
assert 'metered_usd' in d, 'missing metered_usd'
assert 'subscription_usd' in d, 'missing subscription_usd'
assert d['metered_usd']['provider'] == 'zhipu', 'metered provider must be zhipu'
assert d['subscription_usd']['provider'] == 'luxeno', 'subscription provider must be luxeno'
assert d['subscription_usd']['cost_usd'] is None, 'Luxeno cost_usd must be null (not 0)'
assert 'attribution_disclaimer' in d['subscription_usd'], 'missing attribution_disclaimer'
assert isinstance(d['metered_usd']['cost_usd'], (int, float)), 'Zhipu cost_usd must be numeric'
print('PASS')
"
```
Must print `PASS` without assertion errors.

### AC-3 — Luxeno=0 false-positive prevention

**Evidence**: the cron alarm script, when given a cost.json with `subscription_usd.cost_usd = null`,
does NOT evaluate `null >= 0.8 * threshold` as truthy and does NOT send a Feishu alarm card for
Luxeno. This is verified by unit test: mock `cost_usd=null` input → assert `feishu_send` was NOT
called for the Luxeno row.

Additionally: `SELECT COUNT(*) FROM dispatches WHERE provider = 'luxeno' AND token_cost_usd IS NULL`
produces a row count ≥ 0 without error (column existence + null semantics), confirming the existing
schema does not store Luxeno per-dispatch cost as 0.

### AC-4 — .aria/config.json thresholds set

**Evidence**:
```bash
python3 -c "
import json, sys
cfg = json.load(open('.aria/config.json'))
t = cfg['m6']['cost_thresholds']
assert isinstance(t['zhipu_30d_usd'], (int, float)) and t['zhipu_30d_usd'] > 0
assert isinstance(t['luxeno_monthly_usd'], (int, float)) and t['luxeno_monthly_usd'] > 0
print('PASS')
"
```
Must print `PASS`.

### AC-5 — 80% Feishu alarm fires correctly

**Evidence**: unit test where `metered_usd.cost_usd = 0.80 * zhipu_30d_usd` (boundary) → assert
`feishu_send` IS called with `pct_used >= 80`. Complementary: `cost_usd = 0.79 * threshold` →
`feishu_send` NOT called. Both assertions pass.

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

**Evidence**:
```bash
python3 aria-orchestrator/docs/validate-m6-handoff.py --check-3-day-history
```
- Exit code 0
- stdout contains `"3-day rolling history: PASS (N files, latest YYYY-MM-DD)"` where N ≥ 3.
- Files `.aria/cost-snapshots/cost-YYYY-MM-DD.json` for ≥3 consecutive days exist on disk.

This check MUST pass before Spec #2 `aria-2.0-m6-e2e-resilience` Phase B is permitted to start.

### AC-8 — cost_measurement_method enum documented (P-2)

**Evidence**: `validate-m6-handoff.py --check-cost-method-enum` exits 0, verifying that for each
provider row in cost.json, the method is one of
`{provider_api_billing, local_token_count_x_unit_price, subscription_flat_no_attribution}`.
Zhipu row maps to `local_token_count_x_unit_price` (SQLite aggregate of per-dispatch token_cost_usd).
Luxeno row maps to `subscription_flat_no_attribution`.

### AC-9 — acceptance SQL script is binary-falsifiable

**Evidence**:
```bash
cd aria-orchestrator/acceptance && python3 check-m6-cost-acceptance.py
```
- Exit code 0 when all checks pass.
- Exit code non-zero when any check fails (stale data, schema violation, or null-guard violation).
- Script embeds at least the queries for AC-1 through AC-4 as named sub-checks with
  `[PASS]` / `[FAIL: <reason>]` labelled output per check.

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
A. Dual-row cost.json schema + cron script       ~2h
B. .aria/config.json threshold keys              ~1h
C. freshness_ts gate (threaded into A + E)       ~0.5h
D. Cron sentinel + alarm path                    ~2h
E. Acceptance SQL script                         ~1.5h
F. validate-m6-handoff.py (5 abi_compat + P-2)  ~2h
G. 3-day history check (threaded into F)         ~0.5h
─────────────────────────────────────────────────────
Total (AI-implementable)                         ~9.5h ≈ 10h
Owner manual action (post-ship, not in B.2):
  - Set .aria/config.json thresholds
  - Run cron daily × ≥3 days to accumulate history
```

---

## Dependencies

| Dependency | Direction | Notes |
|------------|-----------|-------|
| M5 dispatches table `token_cost_usd` column | Upstream (already shipped M2+) | Cost aggregation reads this column; no migration needed |
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
