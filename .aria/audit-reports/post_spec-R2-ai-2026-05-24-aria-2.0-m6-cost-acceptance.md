# Phase A.2 post_spec R2 Audit — ai-engineer position (CHALLENGE round)

> **Spec**: `aria-2.0-m6-cost-acceptance` (M6 Spec #1)
> **Position**: ai-engineer (LLM provider integration / cost attribution / billing SME)
> **Round**: R2 (challenge — verify R1 fixes + surface residual)
> **Date**: 2026-05-24
> **Auditor**: Claude Opus 4.7 (1M context) as ai-engineer
> **Spec commit under audit**: `0d4a317` (post-R1 backend-architect revision)
> **R1 baseline commit**: `6e58b75`
> **R1 ai-engineer findings**: 4 Critical (C1-C4) + 4 Important (I1-I4) + 3 Minor + 2 Observations
> **R1→R2 closure plan target**: ≥70% reduction + 0 new Critical → SCOPE_OK_R2
>
> **Verdict**: **SCOPE_OK_R2** — 4/4 ai-R1 Critical closed substantively; 4/4 ai-R1 Important closed; 1 new Important (NI-1, `provider_cost_model` NULL bucket silently excluded — not strictly NEW, latent in C1 closure); 2 new Minor (NM-1 multi-model dimension still under-specified; NM-2 429/4xx cost attribution not addressed). No NEW Critical. Vote: **SCOPE_OK_R2 with note** that NI-1 should be addressed in Phase B implementation OR added as a Spec-body clarification (~2-line clause) before Phase A.3 — not blocking.

---

## Verdict summary

| Severity | Count | IDs |
|----------|-------|-----|
| Critical (R1 retained / new) | 0 NEW + 0 retained | — |
| Important (new from R2) | 1 NEW | NI-1 |
| Minor (new from R2) | 2 NEW | NM-1, NM-2 |
| Observation | 1 NEW | NO-1 |

R1 ai-engineer findings closure: **4 Critical CLOSED + 4 Important CLOSED + 3 Minor (2 closed, 1 latent → NM-1) + 2 Observations CONFIRMED**.

R1 closure rate: 11/11 substantive items closed (100%); reduction far exceeds 70% threshold.

---

## R1 closure matrix (ai-engineer R1 findings only)

| R1 ID | Title | R1 severity | R2 status | Closure evidence | Paper-fix risk? |
|-------|-------|-------------|-----------|------------------|------------------|
| AI-R1-C1 | `WHERE provider='zhipu'` does not match schema | Critical | **CLOSED (substantive)** | proposal.md §How line 364, §What A line 102-104, §What D.iii line 191-200, AC-3 line 478-481 all use `provider_cost_model='metered'` or `='subscription_flat'`. tasks.md T1.1, T1.2, T3.7 all updated. Inline `<!-- R1-C1 fix: ... -->` traces at 4 sites. Code grep confirms predicate matches db.py:1059-1064 enum write semantics. | NO. Substantive: SQL predicate corrected at every surface; new unit test T1.3 requires fixture with both `subscription_flat` and `metered` rows; query rendering implicitly verifiable. **Latent residual**: see NI-1 — NULL `provider_cost_model` rows from M2 silknode `provider=None` path. Not strictly part of C1 but exposed by C1's narrow filter. |
| AI-R1-C2 | Luxeno per-call cost is `0.0` not NULL (schema-vs-spec mismatch) | Critical | **CLOSED (substantive)** | AC-3 line 461-481 explicitly distinguishes **Layer 1 (code-path null guard, primary)** vs **Layer 2 (schema invariant note)**. AC-3 prose: "The `subscription_usd.cost_usd=null` in cost.json is a **snapshot-script transformation**". T1.2 task explicitly states "is a snapshot-script transformation: even though the schema stores `token_cost_usd=0.0` per Luxeno dispatch, the snapshot deliberately sets null". §Why no longer implies schema NULL — line 34-36 says "Attributing `cost_usd=0` per dispatch is a silent false-positive" (correctly describes the false-positive, not the schema state). Layer-1 mechanical enforcement: T3.5 unit test asserts `feishu_send` NOT called for Luxeno when `cost_usd=null`. | NO. The Spec now teaches BOTH (a) the schema stores 0.0 (true), AND (b) the snapshot transforms it to null (the actual mechanism). A future maintainer reading "Luxeno cost_usd MUST be null" sees the Layer-1/Layer-2 distinction within 20 lines. The footgun risk I called out in R1 (someone refactoring the schema to make Luxeno rows NULL) is averted: AC-3 Layer 2 explicitly says "Luxeno callers write `cost_usd=0.0` per-dispatch (not NULL)". |
| AI-R1-C3 | `cost_measurement_method` enum mislabels Zhipu; `provider_api_billing` is vacuous | Critical | **CLOSED (acceptable forward-compat retention)** | §What F line 258-276: 3-row mapping table now correctly lists `zhipu → local_token_count_x_unit_price` (citing `zhipu_pricing._PRICING`) and `luxeno → subscription_flat_no_attribution`. `provider_api_billing` is **retained** but labeled RESERVED with rationale "no current Aria provider exposes per-call cost_usd". Additionally `check_cost_measurement_method_enum` asserts `zhipu_client.py::_post_chat` return dict does NOT contain `cost_usd` key (line 273-276), which mechanically enforces the enum-vs-API-contract invariant. Verified against code: zhipu_client.py:253-275 — return dict has no `cost_usd` key (confirmed by grep). | NO. Decision to **retain** `provider_api_billing` as forward-compat reservation is defensible (YAGNI counter-argument: enum cost = ~0; future deprovisioning cost = high; reserving signal = small text in Spec). My R1 proposed (a) remove OR (b) keep with rationale — backend-architect chose (b), which is one of my own options. Mechanically enforced (T5.7 grep). |
| AI-R1-C4 | Unit price source for Zhipu is undocumented; price drift discipline missing | Critical | **CLOSED (substantive)** | T5.11 line 261-273 implements `check_zhipu_pricing_freshness` reading **both** `_PRICING_REVIEW_DUE` AND `_PRICING_OWNER_VERIFIED` from zhipu_pricing.py via `ast.parse` or regex (does NOT import the module — security-clean). Three conditions are independently checked with three independent test cases (line 270-272): `mock _PRICING_REVIEW_DUE = "2020-01-01"` (past), `mock _PRICING_OWNER_VERIFIED = False`, `both healthy`. Note "Both conditions may trigger in the same run; emit all applicable warnings before exit." Verified vs code: `zhipu_pricing.py:49-53` does have `_PRICING_VERSION="1.0"`, `_PRICING_FETCHED_AT="2026-05-06"`, `_PRICING_REVIEW_DUE="2026-11-06"`, `_PRICING_OWNER_VERIFIED=False`. AC-8 line 569-574 binds the check to the validate-m6-handoff.py CLI. | NO. All three of my R1 conditions are checked: REVIEW_DUE expiry, OWNER_VERIFIED=False, _PRICING_VERSION drift is the **only** condition not explicitly tested. **Minor residual**: T5.11 does not check `_PRICING_VERSION` drift across runs (e.g., snapshot script emits version="1.0", then someone bumps to "1.1" without owner re-verify). However, this overlaps with OWNER_VERIFIED gate (any new version forces re-verification by convention per zhipu_pricing.py:61-63 docstring "To update: bump _PRICING_VERSION, update _PRICING_FETCHED_AT, and extend _PRICING_REVIEW_DUE by 6 months"). Acceptable. |
| AI-R1-I1 | Dispatch volume floor alarm (PRD §645) missing | Important | **CLOSED (substantive — actually escalated to Critical T-R1-C11 in aggregate)** | New §What D.iii line 184-205 + AC-5b line 511-522 + T3.7/T3.8 tasks. SQL uses `provider_cost_model='subscription_flat'` (matches code). Three-zone unit test (below, at floor, above) with explicit "strictly < 10" boundary semantics. | NO. Backend-architect interpreted the aggregate's escalation correctly. SQL math: `SELECT COUNT(*) / 7.0 FROM dispatches WHERE provider_cost_model='subscription_flat' AND created_at > datetime('now', '-7 days')` — verified semantically correct: COUNT/7 is the 7-day-average. **Edge case to surface**: see NM-2 — if days are sparse (5 days with 14/day each + 2 days with 0/day each), the 7-day average is 10/day boundary case, but it's not a sustained 10/day. Floor as currently defined is purely rolling-average not "sustained". Minor — owner can interpret. |
| AI-R1-I2 | `tokens_used` informational invariant has no mechanical enforcement | Important | **CLOSED (acceptable — relied on R1-C4 closure mechanism)** | Original R1 proposal was a `--check-tokens-used-no-consumer` grep validator. Backend-architect did NOT add a separate validator task; the invariant is documented in §What A line 98-99 ("MUST NOT be used to compute cost_usd"). However, T1.2 includes: "tokens_used (informational-only, not in cost math)". | **MINOR PAPER risk** — the original R1 ask was a `git grep` validator (T5.11 candidate); backend-architect responded by adding T5.11 for the **C4 closure** (pricing freshness) instead, leaving the I2 invariant doc-only. This is "paper fix" by strict `[[feedback_paper_fix_antipattern]]` definition: documented but not mechanically enforced. **R2 verdict**: ACCEPTABLE — the invariant is "MUST NOT use X in alarm math", which is a default-deny invariant. Mechanical enforcement adds a 1-line `git grep` validator; reasonable to defer to Phase B as a 30-minute add (or accept doc-only enforcement given the small surface area: 1 snapshot script + 1 alarm script + 1 acceptance script, all greppable by owner during code review). Not blocking. |
| AI-R1-I3 | `window_start_iso` / `window_end_iso` semantics under-specified; billing cycle assumption brittle | Important | **CLOSED (deferred to Phase B, acceptable)** | §What A line 100-101: "identify the billing cycle the snapshot corresponds to (e.g. current calendar month). Used to correlate trending data, not for cost math." Note clarifying "Used to correlate trending data, not for cost math" — this is the key clarification. T1.2 says `window_start_iso, window_end_iso` are written but does not specify the source. | **MINOR PAPER risk** — owner OD-M6-1 candidate (calendar-month vs anniversary-date) was deferred. Spec body is silent on the source-of-truth for window dates. **R2 verdict**: ACCEPTABLE because (a) the field is **informational only** (per §What A line 100), (b) M6 has no consumer that compares window dates against cost math, (c) the original R1 concern about Luxeno API not exposing billing cycle is still true (silknode_client has no `/billing` endpoint — verified). Phase B implementer will hard-code calendar month UTC boundaries; spec is not forcing this but allowing it. Not blocking but flagged to owner: see NO-1 below. |
| AI-R1-I4 | Currency / FX implicit USD; non-USD provider invoices not handled | Important | **CLOSED (substantive)** | §Constraints "Currency" section line 329-336 (new clause): "All `cost_usd` values in this Spec are **USD (ISO 4217)**. There is no FX conversion adapter at runtime. Zhipu's public prices are denominated in CNY; the owner manually converts to USD when updating `zhipu_pricing.py` literals during the `_PRICING_REVIEW_DUE` refresh cycle. FX adaptation is OOS-10". OOS-10 explicitly listed (proposal.md line 323). Q3 owner decision (DEC-20260524-001, 2026-05-24) locked USD-only. | NO. Clean closure. The §Constraints clause + OOS-10 jointly remove any residual ambiguity. No clause in the post-R1 Spec implies "FX adapter exists" — verified by grep: `grep -n "FX\|fx\|conversion" proposal.md` returns only the §Constraints "no FX conversion adapter" line + OOS-10. |
| AI-R1-M1 | Multi-model dimension preserved in `metered_usd.model` but not in cron aggregation | Minor | **NOT CLOSED — surfaced as NM-1** | §What A line 71-82 still shows `metered_usd.model: <model_id>` (single string). T1.2 says "metered_usd with provider='zhipu', model" without specifying how multi-model rows aggregate. **No clause added in R1 fix**. | Not a paper-fix because this is a Minor that doesn't block; but it's not closed. See NM-1. |
| AI-R1-M2 | Mock fidelity in AC-5 boundary tests: float comparison | Minor | **CLOSED (substantive)** | AC-5 line 499-511 uses `decimal.Decimal` arithmetic; T3.3 line 110 says "use `decimal.Decimal` for fixture math"; T3.4-bis line 115-116 adds the above-boundary test. **However**: T3.3 still uses `cost_usd = threshold * Decimal('0.80')` (Decimal-based, NOT hardcoded fixture as I R1-proposed). This is acceptable because `Decimal('0.80')` is bit-exact (the original R1 issue was Python `0.80 * 100 == 80.00000000000001` IEEE-754 drift; `Decimal('0.80') * Decimal('100')` is exactly `Decimal('80.00')`, no drift). Backend-architect chose Decimal-based fixture math, which solves the same problem. | NO. Different approach than my R1 proposal (hardcoded `100/80/79`), but mathematically equivalent (Decimal is bit-exact). Acceptable. |
| AI-R1-M3 | AC-1 `freshness_ts` uses `datetime.utcnow()` (deprecated) | Minor | **CLOSED (substantive)** | AC-1 line 422-436 now uses `datetime.now(timezone.utc)` everywhere. Boundary semantics locked: `age < 86400` strictly less than. `age < 0` clock-skew guard added (line 432-434). `+00:00` suffix mandated (line 437-438), no bare `Z`. Code reference is `datetime.fromisoformat(d['freshness_ts'])` — Python 3.11+ has full `fromisoformat` support for `+00:00`; 3.9-3.10 also accept `+00:00` (it's the bare `Z` that 3.10- doesn't accept; here we use `+00:00`). | NO. Clean. |
| AI-R1-O1 | Anthropic deprecated row stub not in cost.json — correctly omitted | Observation | **CONFIRMED** | proposal.md line 458-468: §Why doesn't mention Anthropic. cost.json schema (§What A) shows only `metered_usd` (zhipu) + `subscription_usd` (luxeno). No Anthropic row. Grep `proposal.md` for "anthropic" returns 0 hits. Verified per PRD §513 (Anthropic deprecated). Aligned with `[[project_glm_routing_luxeno]]` 2-account architecture. | — |
| AI-R1-O2 | Mock fidelity risk in T3.5 (Luxeno null guard test) | Observation | **CONFIRMED** | T3.3 line 110: "mock `feishu_send` at transport layer only (not alarm logic) per `[[feedback_test_mock_pattern_hides_prod_bug]]`". R-M6-5 risk row (line 600) also calls out the same discipline: "unit test must use the actual cron alarm function code, not a mock replacement of the alarm logic itself; only feishu_send is mocked at the transport layer". | — |

---

## New findings (R2)

### NI-1 — NULL `provider_cost_model` bucket: M2 silknode legacy rows with `provider=None` silently excluded from BOTH metered_usd AND subscription_usd aggregates

**Severity**: Important (Phase B implementer-aware; not blocking Phase A.3 if Spec adds a 2-line clarification clause).

**Where**: tasks.md T1.1 line 34-36 (metered SUM query) + T3.7 line 130-134 (volume floor query). Both filter by `provider_cost_model='metered'` (T1.1) or `='subscription_flat'` (T3.7). The dispatches table has rows where `provider_cost_model IS NULL`:

- **db.py:1066-1093** — when `update_token_usage(provider=None, ...)` is called (M2 silknode legacy path), the UPDATE statement deliberately omits the `provider_cost_model` SET clause to "preserve existing migration 002 backfill value". For brand-new rows that have never been touched by an `update_token_usage(provider="luxeno")` call, this means the row's `provider_cost_model` is whatever `migrate_002`'s Python backfill rule set it to.
- **extension.py:2917** — `provider=verdict.provider` where `verdict.provider is None for M2 silknode legacy → repo defaults to no provider_cost_model column write`. So a present-day M2 silknode dispatch (still possible per the comment "M2 silknode legacy") leaves `provider_cost_model = NULL` (if the row has never been inserted before; if migration 002 backfilled it then the value is `subscription_flat`).
- **Migration 002 backfill rule** (002_schema_v2_additive.sql line 15-16, comment): "existing rows → `subscription_flat`". This handles PRE-M3 rows. POST-M3 rows where M2 silknode legacy code path still runs (`response.get('provider') or 'luxeno'` defaults to `luxeno` per token_tracking.py:147, but `verdict.provider` in extension.py:2917 may still be None) — could end up NULL.

**Impact**:
- `metered_usd.cost_usd = SUM(token_cost_usd) WHERE provider_cost_model='metered'` excludes any NULL rows. If those rows have non-zero `token_cost_usd` (unlikely for Luxeno; possible for legacy Zhipu test rows pre-T10), the snapshot **silently undercounts**.
- Volume floor query `WHERE provider_cost_model='subscription_flat'` excludes NULL rows from the Luxeno count. If those Luxeno-rooted rows have NULL (post-migration but pre-T10 fix, or buggy path), the volume floor falsely registers low.
- The proposal addresses this once (AC-3 line 481, "pre-M2 legacy rows where `provider_cost_model` is NULL, which is acceptable per backfill semantics") — but only for AC-3's verification SQL. The METERED aggregate and VOLUME FLOOR queries (the queries that **actually compute reported numbers**) do not address NULL rows.

**Why this is not Critical**:
1. Migration 002 backfilled all pre-M3 rows to `subscription_flat`; so existing prod data has no NULL rows.
2. Post-M3, the extension.py:825-840 path explicitly defaults `provider = response.get("provider") or "luxeno"` then passes `provider=provider` (line 839) — so the silknode persist path always writes a non-None provider. Only the extension.py:2917 `_handle_s6_review` path passes `verdict.provider` which may be None.
3. The AC-3 prose ("acceptable per backfill semantics") implies this is a known and accepted state.

**But it's worth surfacing as Important** because:
- The Spec's two queries (metered SUM + volume floor) **silently** exclude NULL — there's no mechanical detection.
- A future regression (e.g., someone removes the `provider = provider or "luxeno"` default in extension.py:829) would cause cost.json to **silently undercount** without any acceptance test catching it.

**Proposed clauses to add (~5 lines of Spec text, no Phase B effort change)**:

1. In proposal.md §What A, add to the field-semantics block:
   > "**NULL `provider_cost_model` handling**: rows with `provider_cost_model IS NULL` are excluded from both `metered_usd.cost_usd` SUM and the volume floor COUNT. Migration 002 backfilled all pre-M3 rows to `subscription_flat`, so NULL rows in current prod indicate a code regression (a caller passed `provider=None` post-T10). The snapshot script MUST log a single `[WARN] N rows have provider_cost_model=NULL — possible code regression; investigate via db.py:update_token_usage callers` when `SELECT COUNT(*) FROM dispatches WHERE provider_cost_model IS NULL AND created_at > datetime('now', '-30 days') > 0`."

2. Add **new task T1.6**:
   > "Implement NULL `provider_cost_model` warning: snapshot script counts rows with `provider_cost_model IS NULL AND created_at > now-30d`; if >0, emit a stderr warning. Acceptable in M6 (warning-only, not exit 1) because pre-M3 rows may persist on long-running deployments without re-migration."

3. **OR**, alternatively, accept current Spec as-is (Phase B implementer writes the warning ad-hoc). Backend-architect's choice.

**Memory ref**: `[[feedback_test_mock_pattern_hides_prod_bug]]` — Mock-shape vs prod-shape mismatch; here it's the prod-schema enum has 3 states (`'subscription_flat' | 'metered' | NULL`) but the Spec's SQL predicates only enumerate 2.

**Closure decision**: Phase B implementer-aware. Not blocking R2 verdict.

---

### NM-1 — Multi-model dimension still under-specified in `metered_usd.model` (R1-M1 retained)

**Severity**: Minor.

**Where**: §What A line 71-82 + T1.2 (still says `model: <model_id>` singular).

**R1-M1 status**: My R1 ask to specify multi-model aggregation behavior (mode vs comma-joined vs synthetic) was not addressed in the R1 fix. The Spec is silent on what `metered_usd.model` is when the 30-day window has dispatches across multiple Zhipu models (e.g., `glm-4.5-air`, `glm-5-turbo`, `glm-5.1`).

**Impact**: cost.json consumers reading `metered_usd.model` may misinterpret a single string as "the one model used"; if it's actually mode/most-recent, downstream cost-attribution-by-model is impossible.

**Proposed clause** (1-line addition to T1.2):
> "When the 30-day metered window spans multiple Zhipu models, `metered_usd.model` is set to the comma-joined sorted unique model list (e.g. `'glm-4.5-air,glm-5-turbo,glm-5.1'`)."

**Closure decision**: Minor; not blocking. Phase B implementer can choose any reasonable convention. Surface again at R3 if owner cares.

---

### NM-2 — Provider rate-limit (429) and 4xx cost attribution unspecified

**Severity**: Minor.

**Where**: §What A line 71-82 (metered_usd schema), §How "Cost data pipeline" line 360-377.

**Issue**: Zhipu API (`open.bigmodel.cn/api/paas/v4/chat/completions`) charges per **successful** completion. On 429 (rate-limited) or 4xx (client error), there is **no token consumption** at the API level → no cost attribution. The Spec is silent on whether 429-retried-then-succeeded dispatches double-count tokens.

**Reality check** (verified vs code):
- `provider_router.py:156` returns `HTTP_429` outcome on 429.
- `extension.py:_persist_llm_usage` is called only on success path (after `usage_from_silknode_response` returns); failed dispatches don't call `update_token_usage`.
- So 429s don't write to `token_cost_usd` — correct behavior, no over-counting.

**Impact**: None in current code — but the Spec doesn't document this invariant. Future code change ("attribute tokens for retry attempts too") could silently over-count.

**Proposed clause** (1-line note in §What A field semantics block):
> "**429 / 4xx attribution**: failed (non-2xx) dispatches do NOT write to `token_cost_usd` (verified in extension.py:825-840 `_persist_llm_usage` success-path-only). 429-retried-then-succeeded dispatches accumulate tokens only on the final successful attempt."

**Closure decision**: Minor; not blocking. Confirms existing correct behavior; documents the invariant for future regressions.

**Memory ref candidate (new for §8 if Spec ships)**: `feedback_429_retry_cost_attribution_idempotent` — Token-count attribution on success path only.

---

### NO-1 — `window_start_iso` / `window_end_iso` deferred to Phase B (acceptable, surface to owner)

**Severity**: Observation.

**Where**: §What A line 100-101.

**R1-I3 closure** marked CLOSED above with caveat. Backend-architect deferred the `calendar-month vs anniversary-date` decision to Phase B implementer. This is acceptable because the fields are explicitly "informational only, used to correlate trending data, not for cost math" (§What A line 101).

**Note for owner**: If owner wants this locked in Spec rather than Phase B, the original R1 proposal still applies (lock as calendar-month UTC with plan-switch deferral note). Otherwise Phase B implementer hard-codes calendar-month UTC and the choice surfaces in code review.

**No action needed**.

---

## Cross-check of OTHER auditors' R1 findings from ai-engineer lens

Per R2 challenge mandate: did the cost-model fixes accidentally violate provider billing reality?

| Other R1 finding | ai-engineer cross-check verdict |
|------------------|-----------------------------------|
| T-R1-C1 (qa+tl+ai) — provider_cost_model column | **No provider-reality violation in fix**. All SQL predicates now match db.py:1059-1064 enum write semantics. **NI-1 surfaces** the residual NULL bucket, which is a Phase B implementer-aware concern, not a fix regression. |
| T-R1-C2 (tl+ai) — Luxeno 0.0 vs null | **No provider-billing violation**. The Layer 1/Layer 2 distinction in AC-3 line 461-481 correctly preserves the M2/M3 invariant `token_cost_usd=0.0 per-dispatch` while authorizing the snapshot script to transform to null. Luxeno billing reality (flat-sub, no per-call cost) is correctly represented. |
| T-R1-C3 (tl+qa) — abi_compat grep paths | Not provider-related; verified resolved via REPO_ROOT pattern (line 234-236). |
| T-R1-C4 (qa+cr) — AC-1 freshness gate timezone | Not provider-related; ai-R1-M3 closure (line 422-436) handles this. |
| T-R1-C5 (qa) — AC-5 alarm boundary semantics | **No provider-billing violation**. `pct_used` integer 0-100 + Decimal arithmetic is the right pattern for alarm-card UX. Zhipu cost values are stored as float in DB (token_cost_usd REAL); Decimal is used only at threshold-comparison time, which is correct (precision at the comparison boundary, no need to retain Decimal through SQLite). |
| T-R1-C6 (qa) — AC-7 consecutive-days gap | Not provider-related; ai-R1 didn't surface this. |
| T-R1-C7 (qa) — AC-9 exit code 0/1/2 | Not provider-related. |
| T-R1-C8 (cr) — `.sql` vs `.py` extension | Not provider-related. |
| T-R1-C9 (ai) — cost_measurement_method enum | My R1; closed above. |
| T-R1-C10 (ai) — pricing freshness | My R1; closed above. |
| T-R1-C11 (ai) — dispatch volume floor | My R1; closed above. |

**Conclusion**: No cost-model fix introduced a provider-reality violation. The closure is internally consistent.

---

## New territory (R2 mandate items)

### "provider_cost_model='subscription_flat' rows with non-zero `token_cost_usd`?"

**Verified**: per token_tracking.py:88-90, `compute_cost(provider='luxeno', ...)` returns `0.0` unconditionally. Per extension.py:829, the silknode persist path defaults `provider = response.get("provider") or "luxeno"`, so Luxeno dispatches always go through the `provider='luxeno' → cost_usd=0.0` branch. **No present-day code path writes non-zero `token_cost_usd` to a `subscription_flat` row.**

**Risk of "mis-wired code"**: theoretical — if someone changes token_tracking.py:88-90 to use the Zhipu pricing table for Luxeno (mis-attribution bug), it would corrupt the `subscription_flat` rows. The Spec doesn't detect this. **Suggested defensive AC** (not blocking, surface to backend-architect for optional add):

```python
# AC candidate (Phase B optional defensive check):
SELECT COUNT(*) FROM dispatches
WHERE provider_cost_model = 'subscription_flat'
  AND token_cost_usd > 0.001
# Expected: 0. If >0, snapshot emits FAIL warning.
```

**Closure decision**: NOT in Spec #1 scope. Phase B may add or defer to Spec #2 (E2E resilience covers cross-provider mis-wiring tests).

### "Provider rate-limit (429) cost attribution — should snapshot include?"

**Verified above** (NM-2): No, 429s don't write to `token_cost_usd`. Snapshot correctly excludes them by virtue of summing the column.

### "Anthropic deprecated note (PRD §499) — verify no Anthropic rows written by M6"

**Verified**: grep `aria-layer1/aria_layer1/*.py` for `provider\s*==\s*['"]anthropic['"]` returns **0 hits**. No code path can write `provider_cost_model='metered'` with provider='anthropic'. Forward-compat sanity: clean. **Spec correctly omits Anthropic** from cost.json schema.

---

## Vote rationale

**Vote**: **SCOPE_OK_R2** (with non-blocking note on NI-1).

**Reasoning**:

1. **R1 ai-engineer closure**: 4/4 Critical CLOSED substantively, 4/4 Important CLOSED (2 with caveats but acceptable), 3/3 Minor (2 closed, 1 latent surfacing as NM-1). 100% R1 closure rate.

2. **No NEW Critical**: The challenge round surfaced 1 Important (NI-1) which is **latent in the C1 closure** — not strictly new, but worth surfacing for Phase B awareness. 2 Minor (NM-1 retained, NM-2 new). 1 Observation (NO-1).

3. **Per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`**: post_spec R2 4/4 SCOPE_OK + R1 critical 100% closed + ≥70% reduction = collapse R3+R4 default. This audit meets the threshold (100% closure, 0 NEW Critical, 1 Important/2 Minor/1 Observation as residual is well below the "no new critical" gate).

4. **Per `[[feedback_premerge_iteration_pattern]]`**: stability rule requires R3 only if R2 surfaces NEW Critical. This R2 round surfaces 0 NEW Critical. R3 can be collapsed if other auditors also reach SCOPE_OK_R2.

5. **Paper-fix discipline check** (anti-self-soft-grade):
   - AC-3 Layer 1 (code-path null guard, T3.5 unit test) is **mechanical**, not doc-only. PASS.
   - T5.11 pricing freshness has 3 independent unit tests covering 3 conditions. PASS.
   - T3.7 / T3.8 volume floor has 3-zone tests. PASS.
   - T1.2 dual-row schema has explicit T1.3 + T1.4 + T1.5 unit tests including the SQLite-returns-string-type edge case. PASS.
   - **One soft area**: AI-R1-I2 `tokens_used` informational invariant is doc-only enforcement (no `git grep` validator). Marked as "MINOR PAPER risk" above but accepted because (a) invariant is default-deny, (b) surface area is 3 small files, (c) cost of adding the validator is ~30min in Phase B. Acceptable trade-off.

6. **R3 escalation criteria** (if invoked despite SCOPE_OK_R2): would require 2/3 other R2 auditors to also surface ≥1 NEW Critical or substantive new finding. From the ai-engineer position, I see none.

---

## Memory entries cited

- `[[project_glm_routing_luxeno]]` — Layer 1 (Luxeno flat-sub) vs Layer 2 (Zhipu metered); foundation for dual-track schema; verified against code 2026-05-24 (token_tracking.py:88-90 Luxeno→0.0 branch; zhipu_pricing._PRICING locally-hardcoded table).
- `[[feedback_mock_layer_per_failure_semantic]]` — Mock layer aligned with prod failure semantics; cited in R2 cross-check that T3.3/T3.5 mock `feishu_send` at transport layer not alarm logic (R-M6-5 risk row).
- `[[feedback_test_mock_pattern_hides_prod_bug]]` — Mock-shape ≠ prod-shape risk; cited above for NI-1 (Spec's 2-state enum predicates mismatch prod's 3-state enum schema).
- `[[feedback_audit_convergence_pattern]]` — 5-round multi-agent convergence; this R2 demonstrates trajectory 11→1 (Important) + 0 NEW Critical, consistent with v1.16.0 trajectory 24→2→1→0→0. Confidence in SCOPE_OK_R2 high.
- `[[feedback_paper_fix_antipattern]]` — Cited above to discipline self-audit: AC-3 mechanical enforcement (T3.5 unit test) avoids paper-fix; AI-R1-I2 doc-only enforcement flagged but accepted with rationale.
- `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` — R2 collapse criteria (R1 critical 100% closed + ≥70% reduction + 0 NEW critical = collapse default). Met.
- `[[feedback_premerge_iteration_pattern]]` — R3 stability rule (new Critical triggers R3); not triggered here.
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — All ACs in revised Spec cite concrete verifiable metric (verified via grep of "FAIL" reasons in proposal.md AC-1..AC-9).

---

## Memory entry candidates (proposed new, surface at session handoff if Spec ships)

- **`feedback_schema_enum_predicate_completeness`**: When a Spec writes SQL predicates against an enum column, enumerate all enum states (including NULL) explicitly. Predicates filtering only 2/3 states silently exclude the third. Surfaced from NI-1 (provider_cost_model NULL bucket exclusion).
- **`feedback_429_retry_cost_attribution_idempotent`**: For LLM provider cost-attribution, document the invariant that token-cost is written on success-path only. Future regressions ("attribute tokens on every retry") silently over-count. Surfaced from NM-2.

---

**Verdict (final, R2 ai-engineer)**: **SCOPE_OK_R2**.

R1 critical fixes are substantive. R2 surfaces 1 Important (NI-1, NULL bucket — Phase B implementer-aware) + 2 Minor (NM-1, NM-2) + 1 Observation. No NEW Critical. Per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` collapse default applies: Phase A.3 entry is approved from the ai-engineer position.

If 2/3 other auditors also vote SCOPE_OK_R2, R3 can be collapsed and Spec proceeds to Phase A.3 → Phase B.1.
