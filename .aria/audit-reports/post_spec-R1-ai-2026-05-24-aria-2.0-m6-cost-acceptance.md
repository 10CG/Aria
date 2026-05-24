# Phase A.2 post_spec R1 Audit — ai-engineer position

> **Spec**: `aria-2.0-m6-cost-acceptance` (M6 Spec #1)
> **Position**: ai-engineer (LLM provider integration / cost attribution / billing SME)
> **Round**: R1 (initial discovery)
> **Date**: 2026-05-24
> **Auditor**: Claude Opus 4.7 (1M context) as ai-engineer
> **Sources reviewed**:
> - `openspec/changes/aria-2.0-m6-cost-acceptance/proposal.md`
> - `openspec/changes/aria-2.0-m6-cost-acceptance/tasks.md`
> - `.aria/decisions/2026-05-24-us026-m6b-brainstorm.md` §2 + §4
> - `docs/requirements/prd-aria-v2.md` lines 491-512 + 638-646
> - `aria-orchestrator/docs/m5-handoff.yaml` lines 145-172
> - `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/`{schema.sql, db.py, token_tracking.py, zhipu_pricing.py, silknode_client.py, zhipu_client.py, provider_router.py, extension.py}
> - Memory: `[[project_glm_routing_luxeno]]` (3-day-old; verified against code today)
>
> **Verdict**: **NEEDS_FIX** — 4 Critical findings (block Approval), 4 Important, 3 Minor, 2 Observations.
> Most-critical finding: Spec's SQL aggregation predicate `WHERE provider='zhipu'` does NOT match the
> actual production schema (`provider_cost_model='metered'`); shipping as-spec would silently return 0
> from a column that does not exist, producing a permanent false-PASS on AC-3 and a Luxeno=0 lookalike
> on AC-2.

---

## Verdict summary

| Severity | Count | IDs |
|----------|-------|-----|
| Critical (block Approval) | 4 | C1, C2, C3, C4 |
| Important (Phase A revision) | 4 | I1, I2, I3, I4 |
| Minor (Phase B note OK) | 3 | M1, M2, M3 |
| Observation (informational) | 2 | O1, O2 |

---

## Critical findings

### C1 — `WHERE provider='zhipu'` does not match the schema; correct column is `provider_cost_model='metered'`

**Severity**: Critical.

**Where**: proposal.md §How "Cost data pipeline" (line 209: `SQLite SUM WHERE provider='zhipu' AND created_at > now-30d`) + tasks.md T1.1
(`query SQLite dispatches table SUM(token_cost_usd) WHERE provider column identifies Zhipu-routed rows`).

**Reality check** (verified against current code, 2026-05-24):
- `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/schema.sql` defines `dispatches.provider_cost_model TEXT` (line 137).
  There is **no `provider` column** on the dispatches table.
- `db.py:1059-1064` writes `provider_cost_model = 'subscription_flat'` when caller passes
  `provider='luxeno'`, and `'metered'` when `provider='zhipu'`. The original provider name is
  **dropped at the persistence layer** — it lives only in the in-memory `response['provider']` dict
  (extension.py:829) and is not retained in the dispatches row.
- A second column `fallback_chain_json` *does* contain provider identity inside event records,
  but it is a JSON blob, not a queryable predicate column.

**Impact if shipped as-spec**:
- SQLite is permissive on unknown columns only in some contexts; `SELECT SUM(token_cost_usd) FROM
  dispatches WHERE provider='zhipu'` will raise `sqlite3.OperationalError: no such column: provider`.
  This is a hard error, not a silent zero — so the cron *will* crash on first prod run.
- However, an over-eager "fix" of editing the SQL to `WHERE provider_cost_model='metered'` is
  correct (see proposed clause below), but **the Spec must say so** rather than imply a non-existent
  column.

**Why this is Critical, not Important**: AC-9 (acceptance SQL script binary-falsifiable) will fail
on first cron run with an OperationalError. The Spec's foundational data model is broken.

**Proposed clauses to add** (anti-paper-fix):
1. In proposal.md §How "Cost data pipeline", replace `WHERE provider='zhipu'` with:
   `WHERE provider_cost_model='metered' AND created_at > strftime('%s','now','-30 days')`
2. In proposal.md §What A, add field-mapping note:
   > "**Schema-to-cost.json column mapping**: dispatches table writes `provider_cost_model` (enum
   > `subscription_flat | metered`), not raw provider name. The cost snapshot script MUST filter by
   > `provider_cost_model='metered'` for the Zhipu/metered aggregate and `provider_cost_model='subscription_flat'`
   > for the Luxeno/flat row. The literal provider name (`zhipu`, `luxeno`) is written into the
   > cost.json output by the snapshot script as a constant derived from the cost-model classification,
   > not read from a non-existent `provider` column."
3. In tasks.md T1.1, update the predicate description to reference `provider_cost_model` explicitly.
4. Add a new unit test in T-schema (e.g. T1.5):
   > "Unit test: snapshot script SQL emits `WHERE provider_cost_model='metered'` (grep the rendered
   > query string); a snapshot run against a fixture with 1 'subscription_flat' row + 2 'metered' rows
   > returns metered_usd.cost_usd = SUM(2 metered rows) and ignores the subscription_flat row."

**Memory ref**: `[[project_glm_routing_luxeno]]` (corrected 2026-05-21 amendment); `[[feedback_test_mock_pattern_hides_prod_bug]]` — assertion shape must match prod schema.

---

### C2 — Luxeno per-call cost is structurally `0.0` (not null) in production code; the "null != 0" invariant is violated at the source

**Severity**: Critical.

**Where**: proposal.md §What A field semantics (line 92-94) + AC-3 ("Luxeno=0 false-positive prevention")
+ DEC §4 ai-R3CH-2 + brainstorm R2 ai-CH-3.

**Reality check** (verified against current code, 2026-05-24):
- `token_tracking.py:88-90`:
  ```python
  if provider == "luxeno":
      # AD-M3-7 §决策 #2: Luxeno is flat-sub baseline; per-call cost = 0
      return 0.0
  ```
- `usage_from_silknode_response()` line 147: `provider = response.get("provider") or "luxeno"`
  → defaults to Luxeno, computes cost `0.0`, then writes `token_cost_usd = 0.0` into the dispatches
  row via `update_token_usage()` (db.py:1099).
- Result: every Luxeno dispatch row in the live dispatches table has `token_cost_usd = 0.0`,
  **literal zero, not NULL**. The schema also defaults the column to `0.0 NOT NULL` (schema.sql:101:
  `token_cost_usd REAL NOT NULL DEFAULT 0.0`).

**Impact**: The Spec's central thesis is "Luxeno=0 false-positive prevention" by enforcing
`subscription_usd.cost_usd = null`. But the **source data** the snapshot script reads from is
`SUM(token_cost_usd)` where Luxeno rows store `0.0`, not NULL. Two failure modes follow:

1. **If snapshot script reads ALL rows (no `provider_cost_model` filter)**: the SUM will include
   both metered Zhipu cost AND zero-cost Luxeno rows. The Luxeno zeros are summed-in silently,
   which is benign for arithmetic (0 adds nothing) but **silently obscures** the fact that the
   "metered_usd" total includes Luxeno path identifier dispatches. Aggregation is contaminated.

2. **If snapshot script filters by `provider_cost_model='metered'`** (the C1 fix): Luxeno rows are
   correctly excluded from `metered_usd.cost_usd`, BUT the snapshot then writes
   `subscription_usd.cost_usd = null` as a **literal constant in the JSON writer**, not derived from
   the schema. AC-3's evidence statement `"SELECT COUNT(*) FROM dispatches WHERE provider = 'luxeno'
   AND token_cost_usd IS NULL produces a row count ≥ 0"` will return `0` (all Luxeno rows have
   `token_cost_usd = 0.0`, not NULL), giving a misleading PASS-by-vacuous-truth.

**The structural mismatch**: the Spec says "Luxeno cost is null" but the production code says
"Luxeno cost is 0.0". The Spec is making a claim about a database state that does not exist.

**Proposed clauses to add**:
1. In proposal.md §What A, add a "schema-grounded null derivation" subsection:
   > "**Null derivation, not null storage**: The dispatches table stores `token_cost_usd = 0.0`
   > for Luxeno subscription-flat dispatches (per token_tracking.compute_cost provider='luxeno'
   > branch, returns 0.0). The cost.json `subscription_usd.cost_usd = null` is a **derived constant
   > written by the snapshot script** to signal 'unattributable per dispatch', not a SUM over a
   > nullable schema column. The snapshot script MUST NOT compute `subscription_usd.cost_usd` as
   > `SELECT SUM(token_cost_usd) FROM dispatches WHERE provider_cost_model='subscription_flat'` —
   > that would return `0.0`, which is the exact false-positive this Spec is trying to prevent."
2. Replace AC-3 second evidence clause with the correct invariant:
   > "Additionally: `SELECT COUNT(*) FROM dispatches WHERE provider_cost_model='subscription_flat'
   > AND token_cost_usd = 0.0` produces a row count ≥ 0 without error; this confirms the schema
   > stores Luxeno per-dispatch cost as literal 0.0 (NOT NULL), and the cost.json `null` is therefore
   > a snapshot-script-derived signal, not a database-stored value."
3. Add a new unit test in T-schema (e.g. T1.6):
   > "Unit test: with fixture `[{provider_cost_model: 'subscription_flat', token_cost_usd: 0.0}, ...]`
   > → snapshot script output `subscription_usd.cost_usd` is JSON `null` (Python `None`), NOT the
   > number `0`, even though every source row has `token_cost_usd = 0.0`. Assert
   > `json.dumps(out)['subscription_usd']['cost_usd']` is the literal string `'null'`."

**Why this is Critical, not Important**: the entire premise of DEC ai-R3CH-2 is that null ≠ 0
prevents silent false-alarm. The current Spec wording ("MUST be null") will be implemented by writing
a literal `None` in the snapshot script — that part is fine — but the **rationale paragraph implies
the null comes from the schema**, which is not true. Future maintainers reading "Luxeno cost_usd
MUST be null" may "fix" the dispatches schema to make Luxeno rows store NULL, breaking the M2/M3
token-tracking invariants. This is a 6-month-latent footgun.

**Memory refs**: `[[project_glm_routing_luxeno]]` 2026-05-21 verification; `[[feedback_paper_fix_antipattern]]`
— don't paper-fix the symptom; surface the schema-vs-spec gap explicitly.

---

### C3 — `cost_measurement_method` enum for Zhipu is wrong: Spec says `provider_api_billing` but production uses `local_token_count_x_unit_price`

**Severity**: Critical (mis-labels billing method, confuses future cost reconciliation).

**Where**: proposal.md §What F (lines 169-174) + AC-8 + tasks.md T5.7.

**Reality check** (verified 2026-05-24):
- `zhipu_client.py:252-256` parses the upstream response `usage_raw.get('prompt_tokens')` /
  `'completion_tokens'`. The upstream Zhipu API (`open.bigmodel.cn/api/paas/v4/chat/completions`)
  returns OpenAI-compatible `usage: {prompt_tokens, completion_tokens, total_tokens}` — **no `cost_usd`
  field** in the API response.
- `token_tracking.py:92-95`: `compute_cost(provider='zhipu', ...)` → calls
  `zhipu_pricing.compute_zhipu_cost(input_tokens, output_tokens, model)` which multiplies tokens by
  the **locally-hardcoded** `_PRICING` table (`zhipu_pricing.py:_PRICING` dict, line 67-80).
- Therefore Zhipu cost in Aria's dispatches table is **`local_token_count_x_unit_price`** by every
  reasonable definition of that enum value — the cost is computed locally from token counts and a
  local price table, NOT read from a provider-returned billing field.

**Impact**: AC-8 (proposal.md line 360-362) says "Zhipu row maps to `local_token_count_x_unit_price`",
which IS correct. So the AC is fine. **But** the field-name choice and the §What F prose imply that
"provider_api_billing" is a possible Zhipu state. It isn't. The Zhipu Chat Completions API does not
return `cost_usd`. This dead enum value will confuse future devs into thinking they should refactor
to "read cost from provider response" — which is impossible at the API contract level.

**Additional concern (Anthropic)**: PRD line 513 (`Anthropic: deprecated per AD-M1-12 supersedes
AD-M1-6, owner subscription-only no API key`). The Spec correctly does NOT include Anthropic in
cost.json. But Anthropic's API (for users who DO have a key) returns `usage: {input_tokens, output_tokens}`
without cost_usd — same as Zhipu. So `provider_api_billing` as an enum value is **vacuous**: no
production provider in scope returns a `cost_usd` field. (Major providers that do: AWS Bedrock,
GCP Vertex with billing export, OpenAI's `/v1/usage` endpoint — none of which Aria uses.)

**Proposed clauses to add**:
1. In proposal.md §What F, add explicit per-provider mapping table:
   > "**Provider → cost_measurement_method mapping (locked, no enum drift)**:
   > | Provider | Method | Source |
   > |----------|--------|--------|
   > | zhipu | `local_token_count_x_unit_price` | `zhipu_pricing._PRICING` table; API does not return cost_usd |
   > | luxeno | `subscription_flat_no_attribution` | flat subscription; per-call attribution structurally impossible |
   > | (provider_api_billing) | RESERVED for future providers (e.g. AWS Bedrock billing export); no current Aria provider exposes per-call cost_usd in API response |
   > "
2. In AC-8, add a falsifiable evidence claim:
   > "Additionally: validate-m6-handoff.py `--check-cost-method-enum --verify-provider-mapping`
   > asserts that the Zhipu API response shape (verified by inspecting `zhipu_client.py:_post_chat`
   > return dict keys) does NOT contain `cost_usd`; this confirms `local_token_count_x_unit_price`
   > is the only correct value for Zhipu. Test fails if anyone refactors `zhipu_client.py` to add
   > a `cost_usd` field without updating this enum mapping."
3. Memory ref to add: `[[project_glm_routing_luxeno]]` 2026-05-21 amendment.

---

### C4 — Unit price source for Zhipu is undocumented in the Spec; price drift discipline missing

**Severity**: Critical (cost attribution can drift silently for 6+ months unnoticed).

**Where**: proposal.md does not specify where `unit_price` is stored or how/when it is updated.

**Reality check** (verified 2026-05-24):
- `zhipu_pricing.py` defines `_PRICING_VERSION = "1.0"`, `_PRICING_FETCHED_AT = "2026-05-06"`,
  `_PRICING_REVIEW_DUE = "2026-11-06"`, `_PRICING_OWNER_VERIFIED = False`.
- The pricing table is hardcoded in Python source, not in `.aria/config.json` or a separate
  price-table file.
- The review-due metadata is read by **nobody** — there is NO automated enforcement that the
  snapshot script warns or fails when `today > _PRICING_REVIEW_DUE`.
- `_PRICING_OWNER_VERIFIED = False` means the entire Zhipu metered cost in the dispatches table
  is, by the code's own admission, an unverified AI estimate.

**Impact**:
- M6's `metered_usd.cost_usd` aggregate is built on a 6-month-old AI-snapshot pricing table that
  the owner has never confirmed. If owner reads `cost.json` showing `metered_usd.cost_usd = $42.17`,
  they may believe that's a billable amount, when it could be off by 2-5× depending on Zhipu real
  pricing drift.
- After 2026-11-06, the pricing is officially stale per the code's own review-due, but the snapshot
  script will continue emitting numbers as if authoritative.
- Owner-set thresholds (`zhipu_30d_usd`) will be compared against unverified estimates — a 50% pricing
  drift could cause false 80% alarms (over-warning) or missed alarms (under-warning).

**Why this is Critical, not Important**: Spec #1's **entire reason for existence** is "operates within
cost bounds" (proposal.md line 27-28). If the cost numbers themselves have unbounded drift, the cost
gate is theatre.

**Proposed clauses to add**:
1. In proposal.md §What A, add a "Unit price provenance" subsection:
   > "**Unit price source**: Zhipu per-token rates are stored in
   > `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/zhipu_pricing.py::_PRICING`
   > (Python source, NOT `.aria/config.json`). The table snapshots `open.bigmodel.cn` public prices
   > at `_PRICING_FETCHED_AT` with a 6-month `_PRICING_REVIEW_DUE` rotation trigger. The cost
   > snapshot script MUST read `_PRICING_VERSION`, `_PRICING_FETCHED_AT`, `_PRICING_REVIEW_DUE`,
   > `_PRICING_OWNER_VERIFIED` and emit them in cost.json metadata as
   > `metered_usd.pricing_provenance: {version, fetched_at, review_due, owner_verified}`."
2. Add a new acceptance criterion **AC-10 — pricing freshness gate**:
   > "If `today > _PRICING_REVIEW_DUE` (currently 2026-11-06), the cron snapshot MUST emit a Feishu
   > warning card with provider='pricing-table-stale' (separate from the 80% cost alarm) and log the
   > stale state to `cost.json.metered_usd.pricing_provenance.stale_warning = true`. The acceptance
   > script `--check-pricing-freshness` exits 0 only if `_PRICING_REVIEW_DUE` is in the future OR
   > `_PRICING_OWNER_VERIFIED` is True."
3. Add a new task **T1.7**:
   > "Unit test: snapshot script run with `_PRICING_REVIEW_DUE` set to `today - 1 day` (stale) →
   > `feishu_send` IS called with provider='pricing-table-stale'; cost.json contains
   > `metered_usd.pricing_provenance.stale_warning: true`."
4. Memory ref to surface as new entry candidate: `feedback_unit_price_provenance_in_cost_artifacts`
   (proposed for §8 of session handoff if this Spec ships).

---

## Important findings (Phase A revision before Approval)

### I1 — Dispatch volume floor alarm (PRD §645 "≥10/day under flat-rate") missing from §What D

**Severity**: Important.

**Where**: PRD §644-645 (verified lines, post Q-final-2 Path a patch):
> "(iii) **Dispatch volume floor**: ≥ 10/day under flat-rate (Luxeno subscription cost-effectiveness gate;
> below floor → reconsider subscription vs metered routing)"

Spec #1 §What D only implements the **above-threshold** alarm (`cost_usd >= 0.8 * threshold`).
The **below-floor** alarm (`luxeno dispatch count < 10/day` → "subscription is uneconomic, reconsider")
is **completely absent** from §What, tasks.md, and AC-1..AC-9.

**Impact**: PRD requires (iii) as a first-class gate. Spec #1 silently drops it. If Luxeno dispatch
volume falls to 3/day (e.g. owner uses Aria less in a given month), the subscription's flat fee
becomes uneconomic, but no alarm fires — the gate is paper-only.

**Brainstorm trace**: DEC §1 Q-final-2 explicitly locks "(iii) dispatch volume ≥ 10/day under flat-rate".
Spec #1 §What D omits it. This is a brainstorm-decision → spec-drafter propagation gap per
`[[feedback_spec_v2_body_propagation_2pass]]`.

**Proposed clauses to add**:
1. In §What D, add subsection "D.2 — Luxeno dispatch volume floor alarm":
   > "**D.2 Luxeno dispatch volume floor**: The cron script computes
   > `daily_luxeno_dispatch_count = SELECT COUNT(*) FROM dispatches WHERE provider_cost_model='subscription_flat'
   > AND created_at > strftime('%s','now','-1 day')`. If `count < 10`, send a Feishu **info card**
   > (not warning — different severity) with provider='luxeno-volume-floor', body
   > 'Luxeno dispatch volume below subscription-effectiveness floor (N=<count>, floor=10);
   > reconsider subscription vs metered routing if sustained <10/day for ≥7 days.'"
2. Add **AC-11 — dispatch volume floor alarm**:
   > "Unit test: fixture with 3 Luxeno dispatches in last 24h + 0 below threshold →
   > `feishu_send` called once with provider='luxeno-volume-floor' AND
   > `feishu_send` NOT called for above-threshold (no Zhipu cost). Complementary: 15 Luxeno
   > dispatches → `feishu_send` NOT called."
3. Add **task T3.7** under T-alarm:
   > "Implement Luxeno volume floor check per AC-11. Distinct from 80% threshold; emit info-level
   > Feishu card with severity=info (not warning), title 'Luxeno volume floor reminder'."

---

### I2 — `tokens_used informational` semantic has no enforcement; mis-wired consumer can still cause Luxeno=0 false-positive

**Severity**: Important.

**Where**: proposal.md §What A field semantics line 95-96 ("`subscription_usd.tokens_used` is
informational only; it MUST NOT be used to compute cost_usd").

The Spec states the rule but provides no test asserting it. A future PR could add
`if subscription_usd.tokens_used > N: send_alarm(...)` and break the invariant silently.

**Proposed clauses to add**:
1. Add **AC-12 — tokens_used not consumed by alarm logic**:
   > "Unit test: snapshot script + cron alarm script + acceptance script have zero references to
   > `subscription_usd.tokens_used` in any branching/comparison expression. Verified by:
   > `git grep -E "subscription_usd\['tokens_used'\]|subscription_usd\.tokens_used" -- '*.py'`
   > should return only the snapshot script writer (which writes the field) and no consumer."
2. Add task **T5.11** under T-validate:
   > "validate-m6-handoff.py `--check-tokens-used-no-consumer`: greps the alarm/acceptance/snapshot
   > Python files for any read of `subscription_usd['tokens_used']` or `.tokens_used` attribute access
   > outside the snapshot writer; fails if found (paper-trail enforcement of P-1 invariant)."

---

### I3 — `window_start_iso` / `window_end_iso` semantics under-specified; billing cycle assumption is brittle

**Severity**: Important.

**Where**: proposal.md §What A line 97-98 ("identify the billing cycle the snapshot corresponds to
(e.g. current calendar month)").

**Issues**:
- "e.g. current calendar month" is non-binding. Luxeno may bill on a 30-day rolling cycle from
  subscription anniversary date, not calendar month. The Spec doesn't say which is canonical.
- If owner switches plans mid-month (e.g. coding-plan → enterprise), the window crosses billing
  schemes — does the snapshot script split the row? Show the latest window? Show the union?
- No source-of-truth for the dates: does the script query the Luxeno API for billing-cycle metadata
  (which doesn't exist per current `silknode_client.py` — no billing endpoint), or hard-code calendar
  month boundaries, or read from `.aria/config.json`?

**Proposed clauses to add**:
1. In §What A, replace the window prose with a locked decision:
   > "**Billing window dates** (AD-M6-4 to be filled in Phase B):
   > - `window_start_iso`: first day of current calendar month at 00:00:00 UTC, ISO-8601
   >   (e.g. `2026-05-01T00:00:00Z`).
   > - `window_end_iso`: last day of current calendar month at 23:59:59 UTC, ISO-8601
   >   (e.g. `2026-05-31T23:59:59Z`).
   > - **Rationale**: Luxeno does not expose a billing-cycle metadata endpoint
   >   (verified via `silknode_client.py` — no `/billing` route exists). Calendar month is the
   >   simplest deterministic windowing aligning with owner's monthly review cadence per PRD §644
   >   '(i) Luxeno monthly_usd'.
   > - **Plan-switch behaviour**: If owner switches Luxeno plans mid-month (e.g. coding → enterprise),
   >   the snapshot continues using calendar month boundaries; `attribution_disclaimer` is appended
   >   with a free-text note. No splitting or proration. (Owner-acknowledged limitation per
   >   `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — defer plan-switch reconciliation
   >   to v2.1.)"
2. Add **AC-13 — window dates are calendar-month UTC**:
   > "Unit test: snapshot script run on 2026-05-15T12:00:00Z → output `subscription_usd.window_start_iso
   > == '2026-05-01T00:00:00Z'` AND `window_end_iso == '2026-05-31T23:59:59Z'`. (Boundary test:
   > run on 2026-05-31T23:59:00Z → still May window. Run on 2026-06-01T00:00:00Z → June window.)"
3. Add **AD-M6-4 slot** in §How (currently only AD-M6-1..3): "Billing window date semantics +
   plan-switch behaviour".

---

### I4 — Currency is implicit USD; non-USD provider invoices not handled

**Severity**: Important.

**Where**: proposal.md §What B (line 113-114) labels thresholds `zhipu_30d_usd` and
`luxeno_monthly_usd`, but never declares the currency standard.

**Reality**: Zhipu (`open.bigmodel.cn`) is a Chinese company; its public price page lists CNY
prices and the API contract is silent on currency. Luxeno (10CG-owned per `[[project_glm_routing_luxeno]]`)
likely bills in USD or CNY depending on the contract — Spec does not say.

If the snapshot script multiplies token counts by a USD-denominated `_PRICING` table but Zhipu's
real invoice is in CNY, the threshold comparison is meaningless without an FX rate.

**Proposed clauses to add**:
1. In proposal.md §What A, add currency clause:
   > "**Currency**: All `cost_usd` fields are USD (ISO 4217 currency code USD). Provider invoices
   > received in non-USD currencies (e.g. CNY) MUST be converted at the snapshot time using the
   > daily mid-rate from a deterministic FX source (per AD-M6-5 to be filled Phase B). For Aria 2.0
   > M6, the Zhipu `_PRICING` table is pre-converted to USD at snapshot time 2026-05-06 (FX rate
   > documented in `zhipu_pricing.py::_PRICING_FX_SOURCE` — currently absent, to be added per task
   > T1.8). Luxeno subscription threshold (`luxeno_monthly_usd`) MUST be owner-supplied in USD;
   > if owner pays Luxeno in CNY, owner converts before writing the threshold to `.aria/config.json`."
2. Add task **T1.8**: "Add `_PRICING_FX_SOURCE` and `_PRICING_FX_RATE_USD_PER_CNY` constants to
   `zhipu_pricing.py` with provenance comment; if Zhipu pricing is verified as USD-denominated
   at source, set source='zhipu-public-page-is-usd' and rate=1.0."
3. Add **AD-M6-5 slot**: "Currency conversion provenance for non-USD provider invoices".

---

## Minor findings (Phase B acceptable, no Approval block)

### M1 — Multi-model dimension preserved in `metered_usd.model` but not in cron aggregation

**Severity**: Minor.

**Where**: proposal.md §What A line 71 shows `metered_usd.model: <model_id>` (single string field),
not an array. But DEC §2 Spec #1 schema implies the field could host multiple models if Zhipu were
queried per-model.

**Issue**: If the snapshot aggregates ALL Zhipu metered rows (regardless of which glm-5-turbo /
glm-5.1 / glm-4.5-air model was used), the single `model` field cannot represent multiple. The
Spec doesn't say if `model` is:
- the most-frequent model in the window (mode), or
- a comma-joined list of all models seen, or
- a synthetic value like `"zhipu-multi-model"`.

**Proposed clause**: In §What A, add: "When the metered aggregate spans multiple models,
`metered_usd.model` is the comma-joined sorted unique model list (e.g. `'glm-4.5-air,glm-5-turbo,glm-5.1'`).
If a single model dominates (≥80% of dispatches in window), `model` is that single id."

This is Minor because the alarm logic doesn't read `model`, only `cost_usd`.

---

### M2 — Mock fidelity in AC-5 boundary tests: 0.80 boundary uses `>=` not `>`; verify Python float comparison

**Severity**: Minor.

**Where**: tasks.md T3.3 (`cost_usd = 0.80 * zhipu_threshold` boundary → `feishu_send` IS called).

**Issue**: Per `[[feedback_mock_layer_per_failure_semantic]]`, mock-layer alignment matters. The
test writes `cost_usd = 0.80 * threshold` and asserts `pct_used >= 80`. But Python float arithmetic:
`0.80 * 100 == 80.0` is exact (binary representation of 0.8 has rounding, but `0.8 * 10 == 8.0`
exact; `0.8 * 100 == 80.00000000000001` on some platforms). The boundary test may flake.

**Proposed clause**: In T3.3, replace `0.80 * threshold` with a hardcoded fixture pair:
`threshold=100, cost_usd=80` → expect alarm; `threshold=100, cost_usd=79` → expect no alarm.
Avoid floating-point boundary computation in the test setup.

---

### M3 — AC-1 `freshness_ts` uses `datetime.utcnow()` (deprecated in Python 3.12+)

**Severity**: Minor.

**Where**: proposal.md AC-1 evidence line 272: `(datetime.datetime.utcnow() - ts).total_seconds()`.

**Issue**: `datetime.utcnow()` is deprecated since Python 3.12 in favour of
`datetime.now(datetime.UTC)`. If the cron host runs Python 3.12+, this will emit a DeprecationWarning;
in 3.14+ it may be removed entirely.

**Proposed clause**: Replace `datetime.datetime.utcnow()` with
`datetime.datetime.now(datetime.timezone.utc)` in AC-1 and all snapshot/acceptance scripts.
Also strip handling: ISO-8601 with explicit `+00:00` offset, not `Z` suffix
(per Python's `fromisoformat` quirk).

---

## Observations (informational, no action required)

### O1 — Anthropic deprecated row stub not in cost.json — correctly omitted

**Where**: PRD line 513 (`Anthropic: deprecated per AD-M1-12 supersedes AD-M1-6, owner subscription-only no API key`).

**Observation**: Spec #1 correctly does NOT include an Anthropic row in cost.json. Some Specs in
similar industries (e.g. SaaS billing) include zero-cost stubs for deprecated providers for
schema-stability reasons. Aria's choice (2-row schema, no Anthropic stub) is **correct** because:
- The dispatches table will not have Anthropic rows post-AD-M1-12.
- A zero stub would add noise to the alarm path.
- If Anthropic is re-enabled later, schema extension is trivial (add row).

No action; calling out as confirmed-correct.

### O2 — Mock fidelity risk in T3.5 (Luxeno null guard test)

**Where**: tasks.md T3.5, R-M6-5 risk row.

**Observation**: The Spec correctly anticipates `[[feedback_test_mock_pattern_hides_prod_bug]]` —
risk R-M6-5 calls out "mock only feishu_send at transport layer, not alarm logic itself". This is
the **right discipline**.

One additional refinement (informational, not blocking): the mock should be at the `feishu_webhook.send_card`
or `httpx.post` level, NOT at `alarm_logic.check_threshold(...)`. The Spec is already aligned; just
ensure tasks.md T3.5 wording stays at "transport layer".

No action; aligned with the right pattern.

---

## Cross-cutting consensus signals (R1 ai-engineer position)

**Substantive findings expected to surface in qa-engineer / backend-architect R1**:
- C1 (schema column mismatch) — backend-architect should also catch this.
- C2 (Luxeno=0 vs null semantic gap) — qa-engineer should catch this if testing rigorously.
- I1 (dispatch volume floor missing) — qa-engineer should catch via PRD §645 traceability check.

**Findings specific to ai-engineer (unlikely to be caught by other positions)**:
- C3 (cost_measurement_method enum mismatch with provider API contracts) — requires LLM provider SME knowledge.
- C4 (unit price provenance) — requires understanding LLM pricing-table lifecycle.
- I4 (currency / FX handling) — requires understanding non-USD provider billing.
- M1 (multi-model per provider) — requires familiarity with model-tier routing patterns.

---

## Recommended Phase A.2 next steps

1. **Spec-drafter revises proposal.md + tasks.md** addressing C1-C4 explicitly (with the proposed
   clauses verbatim or improved).
2. **R2 audit** (this Spec is owner-flagged Level 2-3 borderline + ~10h scope) can be **2-agent**
   (backend-architect + qa-engineer) per DEC tasks.md line 207 unless C1-C4 trigger escalation to
   full 4-agent (recommend escalation if C1+C2 both unresolved by R1 revision).
3. **R3** likely needed only if R2 surfaces new substantive findings; per
   `[[feedback_audit_collapse_r3_r4_when_r2_clean]]`, R3 collapse OK if R2 has 0 NEW critical.
4. **Owner OD candidates** if revision is contentious:
   - OD-M6-1: confirm calendar-month vs anniversary-date billing window (I3).
   - OD-M6-2: confirm Zhipu pricing-table currency is USD or needs FX conversion (I4).
   - OD-M6-3: confirm pricing review-due trigger should be Feishu warn (C4) vs hard-fail acceptance.

---

## Memory entries cited

- `[[project_glm_routing_luxeno]]` — authoritative source for Layer A (Hermes/Z.AI) vs Layer B (aria-layer1/Luxeno) routing; 2026-05-21 amendment confirmed two-account architecture; verified against code 2026-05-24.
- `[[feedback_test_mock_pattern_hides_prod_bug]]` — mock-shape ≠ prod shape risk; cited for C1 (schema column), C2 (null vs 0 storage), C3 (provider response shape).
- `[[feedback_mock_layer_per_failure_semantic]]` — mock layer must align with failure semantic; cited for M2 (boundary float).
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — acceptance bool must cite metric; cited for I3 plan-switch deferral.
- `[[feedback_paper_fix_antipattern]]` — code+test+doc 三位一体; cited for C2 to prevent symptom-only fix.
- `[[feedback_spec_v2_body_propagation_2pass]]` — brainstorm decision → §What → tasks.md propagation; cited for I1 (PRD §645 floor dropped).
- `[[feedback_audit_collapse_r3_r4_when_r2_clean]]` — R3 collapse criteria; cited for recommended next steps.

---

## Memory entry candidates (proposed new, to surface at session handoff if Spec ships)

- **`feedback_unit_price_provenance_in_cost_artifacts`**: When emitting cost-aggregate JSON from
  a locally-computed token×price product, embed pricing-table provenance (`version`, `fetched_at`,
  `review_due`, `owner_verified`) inline in the artifact. Surfaced from C4.
- **`feedback_schema_column_vs_spec_predicate_mismatch`**: When a Spec writes SQL predicates against
  a dispatches table, grep the schema.sql for the literal column name before Approval. Surfaced
  from C1.

---

**Verdict (final, R1 ai-engineer)**: **NEEDS_FIX**.

Critical findings C1-C4 require Spec revision before Approval. If Spec-drafter accepts the proposed
clauses verbatim, R2 should converge in 1-2 agents without further escalation. If revision is
contentious (e.g. owner pushes back on currency clause I4 or pricing freshness AC-10), escalate to
4-agent R2 + owner OD candidates listed above.

Estimated revision effort: ~1-2h Spec-drafter time (additive prose; no §Why or §How architecture change).
