# Post_Spec R1 Audit — AGGREGATE — aria-2.0-m6-cost-acceptance

> **Round**: R1 (Phase A.2 post_spec)
> **Spec**: aria-2.0-m6-cost-acceptance (Spec #1 of M6 four sub-Specs)
> **Spec status at audit time**: Draft (commit `6e58b75`)
> **Audit timestamp**: 2026-05-24 UTC
> **DEC reference**: DEC-20260524-001 (M6 brainstorm CONVERGED 2026-05-24)
> **Auditors (4 parallel)**: tech-lead-critic + qa-engineer + ai-engineer + code-reviewer
> **Aggregate verdict**: **NEEDS_FIX** — 4/4 NEEDS_FIX (substance-level consensus, R3 forcing function discipline confirmed)

---

## Counts

| Auditor | Verdict | Critical | Important | Minor | Observation |
|---------|---------|----------|-----------|-------|-------------|
| tech-lead-critic | NEEDS_FIX | 3 | 5 | 4 | 5 |
| qa-engineer | NEEDS_FIX | 4 | 7 | 4 | 3 |
| ai-engineer | NEEDS_FIX | 4 | 4 | 3 | 2 |
| code-reviewer | NEEDS_FIX | 1 | 4 | 5 | 7 |
| **Total raw** | — | **12** | **20** | **16** | **17** |
| **De-duplicated cross-auditor consensus themes** | — | **11 unified themes** | — | — | — |

Source reports (raw):

- `.aria/audit-reports/post_spec-R1-tl-critic-2026-05-24-aria-2.0-m6-cost-acceptance.md`
- `.aria/audit-reports/post_spec-R1-qa-2026-05-24-aria-2.0-m6-cost-acceptance.md`
- `.aria/audit-reports/post_spec-R1-ai-2026-05-24-aria-2.0-m6-cost-acceptance.md`
- `.aria/audit-reports/post_spec-R1-cr-2026-05-24-aria-2.0-m6-cost-acceptance.md`

---

## Critical themes (de-duplicated; ordered by cross-auditor consensus)

### T-R1-C1 — Schema column wrong: `provider` vs `provider_cost_model` *(3 auditors)*

**Source**: tl C-tl-2 + ai C1 + cr corroborates.
**Issue**: Multiple SQL clauses in `proposal.md` filter by `WHERE provider='zhipu'` (and `'luxeno'`). The actual `dispatches` table schema (per `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/schema.sql` and M2 T10 contract) has **no `provider` column**. It has `provider_cost_model TEXT` with enum `'subscription_flat'|'metered'`.
**Impact**: First cron run → `sqlite3.OperationalError: no such column: provider`. AC-9 fails immediately.
**Fix direction**: Replace all `WHERE provider='zhipu'` → `WHERE provider_cost_model='metered'`. Replace all `WHERE provider='luxeno'` → `WHERE provider_cost_model='subscription_flat'`. Audit every SQL fragment in proposal.md + tasks.md.

### T-R1-C2 — Luxeno `token_cost_usd` is `0.0` literal, NOT NULL *(2 auditors)*

**Source**: tl C-tl-3 + ai C2.
**Issue**: `schema.sql:101` declares `token_cost_usd REAL NOT NULL DEFAULT 0.0`. Luxeno callers explicitly pass `cost_usd=0.0` (per `db.py:1054` + `token_tracking.py:156`). Proposal AC-3 evidence (`token_cost_usd IS NULL`) returns vacuous-PASS on prod (0 rows match). §Why narrative implies the schema returns NULL → factually inverted.
**Impact**: AC-3 (Luxeno=0 false-positive prevention) is unenforceable; rationale paragraph misleads future maintainers; risk of "fix" PR breaking M2/M3 token-tracking invariants.
**Fix direction**: Distinguish two layers:
1. **In-DB**: `token_cost_usd=0.0` (preserved, M2/M3 invariant)
2. **In cost.json output**: `subscription_usd.cost_usd=null` (Spec #1's transformation)
   AC-3 must assert the **transformation** (snapshot script's null guard), not the schema column. Rewrite AC-3 evidence: "Snapshot script produces `subscription_usd.cost_usd == null` when summing `WHERE provider_cost_model='subscription_flat'`."

### T-R1-C3 — abi_compat grep file paths use bare basenames *(2 auditors)*

**Source**: tl C-tl-1 + qa I-5.
**Issue**: T5.2-T5.6 specify grep targets as bare filenames (`extension.py`, `reconciler.py`, `comment_poll.py`, `schema.sql`, `004_schema_v4_additive.sql`). Canonical paths live at `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/*` (Python) and `aria-orchestrator/hermes-extensions/aria-layer1/migrations/*` (SQL).
**Impact**: Phase B implementer either greps repo-wide (false-positive on archive copies / vendored deps) OR hits `FileNotFoundError` → silent false-PASS that defeats abi_compat enforcement.
**Fix direction**: Each task T5.2-T5.6 specify absolute (relative-to-repo-root) paths. Add `REPO_ROOT` resolution pattern (mirror `validate-m5-handoff.py::REPO_ROOT / "hermes-extensions" / "aria-layer1" / "aria_layer1"`).

### T-R1-C4 — AC-1 freshness gate timezone-naive & deprecated datetime *(2 auditors)*

**Source**: qa C-1 + cr M-3 (deprecation only).
**Issue**: AC-1 Python snippet uses `datetime.utcnow()` (deprecated Python 3.12+) and `datetime.fromisoformat(d['freshness_ts'].rstrip('Z'))`. Three failures:
1. If snapshot writes `+00:00` suffix (Python `isoformat()` default) instead of `Z`, `rstrip('Z')` no-ops, parse succeeds but mixes aware vs naive → TypeError on subtract.
2. Future `freshness_ts` (NTP clock skew) → `age < 0` → silently passes < 86400 gate.
3. Boundary semantic unspecified (`<` vs `<=`).
**Fix direction**: Use `datetime.now(timezone.utc)`; require `freshness_ts` to have explicit `tzinfo` (parse-time assert); add `age < 0` guard (clock skew → FAIL); lock boundary as `age < 86400`. Snapshot script writes `datetime.now(timezone.utc).isoformat()` (produces `+00:00`).

### T-R1-C5 — AC-5 alarm boundary semantics *(qa)*

**Source**: qa C-2.
**Issue**: `pct_used` unit undefined (0-100 int vs 0.0-1.0 float). Tests only cover at-boundary (80.0%) and below (79%); missing above-boundary (80.1%). IEEE-754 drift at non-round thresholds (e.g., 3.33 USD) can flip boundary.
**Fix direction**: Define `pct_used` as **integer 0-100** in proposal §What D and tasks T3.x. Require `decimal.Decimal` arithmetic in fixture math. Add T3.4-bis: `pct_used = 0.801 * threshold → alarm IS sent`.

### T-R1-C6 — AC-7 consecutive-days gap detection unspecified *(qa)*

**Source**: qa C-3.
**Issue**: "3 day rolling history" mechanism unspecified. UTC calendar boundary "today" undefined (23:50 UTC cron run vs 00:10 UTC validation disagree). Naive implementation: count files. A gap (Day-2 cron failed, Days 1/3/4 exist) → 3 files → false PASS.
**Fix direction**: Define "today" = `datetime.now(timezone.utc).date()`. Specify consecutive-sequence: take 3 most-recent dates, sort, each adjacent pair must differ by exactly 1 day. Add T5.10-bis: gap test cases (e.g., dates `[D-1, D-2, D-4]` → FAIL).

### T-R1-C7 — AC-9 exit code semantics *(qa)* → **OWNER DECISION Q1: Lift to Spec body**

**Source**: qa C-4.
**Issue**: AC-9 only says "non-zero on failure". Conflates AC failure (data condition) with infra failure (cost.json missing / corrupt JSON / config key missing). AD-M6-3 deferred to Phase B.
**Owner decision (Q1, 2026-05-24)**: **Lift to Spec body**. Drop AD-M6-3 defer.
**Fix direction**: Replace AC-9 + AD-M6-3 with:
- exit 0 = all AC pass
- exit 1 = data AC failure (cost threshold breached, schema mismatch, stale data)
- exit 2 = infrastructure failure (cost.json missing, corrupt JSON, config key missing, ARIA_FEISHU_WEBHOOK_URL absent — but only if alarm path is required for the AC under test)

### T-R1-C8 — `.sql` vs `.py` extension propagation glitch *(cr)*

**Source**: cr CR-R1-C1.
**Issue**: 4 surfaces of acceptance script extension:
- proposal.md:147 (§What E) → `.sql`
- proposal.md:222 (§How diagram) → `.sql`
- proposal.md:368 (AC-9 evidence: `python3 check-m6-cost-acceptance.py`) → `.py`
- tasks.md:91 (T4.1) → `.py`
AC-9 is exec-bound → `.py` is authoritative.
**Fix direction**: Propagate `.py` to all 4 surfaces (2-pass per `[[feedback_spec_v2_body_propagation_2pass]]`).

### T-R1-C9 — `cost_measurement_method` enum mislabels Zhipu *(ai)*

**Source**: ai C3.
**Issue**: Zhipu's `open.bigmodel.cn` API does NOT return `cost_usd` in responses — only `prompt_tokens / completion_tokens`. Cost computed locally via `zhipu_pricing._PRICING`. So `provider_api_billing` is a dead enum value (no Aria provider exposes per-call cost_usd). The §What F prose says "Zhipu maps to `local_token_count_x_unit_price`" — technically correct — but the enum definition includes `provider_api_billing` which serves no Aria provider.
**Fix direction**: Either (a) remove `provider_api_billing` from the enum and document the 2-value enum, OR (b) keep it as forward-compat reservation with explicit note "currently no Aria provider; reserved for future API-billed providers (e.g., Anthropic per-call cost)".

### T-R1-C10 — Unit price drift discipline *(ai)* → **OWNER DECISION Q2: Add check + Q3: USD only**

**Source**: ai C4.
**Issue**: `zhipu_pricing._PRICING_VERSION=1.0`, `_PRICING_FETCHED_AT=2026-05-06`, `_PRICING_REVIEW_DUE=2026-11-06`, `_PRICING_OWNER_VERIFIED=False`. After 2026-11-06 pricing is stale per code's own admission, but snapshot script emits numbers as authoritative.
**Owner decision (Q2, 2026-05-24)**: **Add `check_zhipu_pricing_freshness` to validate-m6-handoff.py.** Exit 1 warn if `_PRICING_REVIEW_DUE < now` OR `_OWNER_VERIFIED=False`. New task T5.11 in §5.
**Owner decision (Q3, 2026-05-24)**: **USD only.** No FX adapter in Spec #1. Zhipu public price CNY manually converted to USD by owner during pricing rotation (locked in `zhipu_pricing.py` literals). Add §Constraints clause: "All cost_usd is USD (ISO 4217); FX rotation is part of pricing review ritual, not Spec #1 runtime."

### T-R1-C11 — Dispatch volume floor missing *(ai)*

**Source**: ai I1 (escalated to Critical here because PRD §645 mandates it as 3rd cost gate sub-clause).
**Issue**: PRD §645 (post-patch a786444): "**Dispatch volume floor**: ≥10/day under flat-rate (Luxeno subscription cost-effectiveness gate; below floor → reconsider subscription vs metered routing)". Proposal §What D talks about 80% upper threshold but says nothing about lower-floor enforcement.
**Fix direction**: Add new §What D.iii "Dispatch volume floor check": daily rolling 7-day average dispatches < 10/day → emit Feishu warn ("Luxeno subscription not amortizing — reconsider routing"). Add AC-5b (boundary semantics for floor). Add T3.7 / T3.8 tasks.

---

## Important themes (selective — apply during R1 fix; non-blocking to R2 verdict if covered)

### I-R1-1 Atomic write for cost.json *(qa I-2)*

Snapshot script must `write to .tmp then os.rename()`. Add to T1.1.

### I-R1-2 File-missing vs corrupt JSON differentiation *(qa I-1, I-2)*

Add T4.5: missing cost.json → exit 2 + `[ERROR] AC-1: cost.json not found — cron has never run`. Add T4.6: corrupt JSON → exit 2 + `[ERROR] AC-1: cost.json malformed`.

### I-R1-3 ARIA_FEISHU_WEBHOOK_URL absence handling *(qa I-6)*

Caught around alarm send path (warn log + exit 0); NOT around snapshot write (which must succeed regardless of alarm capability).

### I-R1-4 AD-M6-* numbering coordination *(cr I-2)* → **OWNER DECISION Q4: Spec #1 locks AD-M6-1/2/3**

**Owner decision (Q4)**: Spec #1 locks AD-M6-1/2/3. Spec #2/#3/#4 start from AD-M6-4. Add cross-Spec coordination memo to DEC-20260524-001 (separate small Edit op). Spec #1 §How adds "AD allocation reservation: M6-1/2/3 (Spec #1) — other M6 sub-Specs use M6-4+".

### I-R1-5 Status string redundancy *(cr I-4)*

Change `**Status**: Draft (Phase A.1; pending Phase A.2 post_spec audit)` → `**Status**: Draft` (clean enum; trajectory captured in §Audit trajectory).

### I-R1-6 Concurrent writer race *(qa I-7)*

Atomic-write pattern (I-R1-1) also applies to `cost-snapshots/` archive copy. Document in AD-M6-2.

### I-R1-7 Stringified `cost_usd` from API *(qa I-4)*

Snapshot script must `float(raw['cost_usd'])` cast and assert `isinstance(float)` before sum. Add unit test.

### I-R1-8 Currency / FX *(ai I4)* → **Resolved by Q3 above**

USD only; CNY→USD conversion is part of pricing rotation ritual, not Spec #1 runtime. Add §Constraints note.

---

## Minor + Observations (deferred to R1 fix as polish; no R2 challenge expected)

See raw reports for full list (16 minor + 17 observations).

---

## Owner-locked decisions (2026-05-24, applied to R1 fix)

| Q | Decision | Affected findings |
|---|----------|-------------------|
| **Q1** | AC-9 exit code 0/1/2 lifted to Spec body; AD-M6-3 defer removed | T-R1-C7 |
| **Q2** | Add `check_zhipu_pricing_freshness` to validate-m6-handoff.py (T5.11) | T-R1-C10 |
| **Q3** | USD only; CNY→USD via pricing rotation ritual, not Spec #1 runtime | T-R1-C10 + I-R1-8 |
| **Q4** | Spec #1 locks AD-M6-1/2/3; Spec #2/#3/#4 start AD-M6-4. Add DEC carry-forward memo | I-R1-4 |

---

## R1 → R2 closure plan

1. **R1 fix**: backend-architect agent applies 11 Critical + 8 Important fixes to proposal.md + tasks.md (single revision pass, in-place edits).
2. **R2 mode**: 3-agent challenge (code-reviewer + ai-engineer + tech-lead-critic) verifies R1 fixes + surfaces residual.
3. **Convergence target**: ≥70% reduction + 0 new Critical → SCOPE_OK_R2 4/4 → Phase A.3 entry.
4. **Stability rule** (per `[[feedback_premerge_iteration_pattern]]`): if R2 introduces NEW Critical, R3 mandatory; otherwise R2 PASS sufficient for A.3 (per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` default).

---

## Cross-references

- DEC-20260524-001: `.aria/decisions/2026-05-24-us026-m6b-brainstorm.md`
- Spec #1: `openspec/changes/aria-2.0-m6-cost-acceptance/proposal.md` + `tasks.md`
- m5-handoff abi_compat: `aria-orchestrator/docs/m5-handoff.yaml:148-172`
- PRD §M6 (post-patch a786444): `docs/requirements/prd-aria-v2.md:411-446` + `638-647`

---

**Aggregate authored**: 2026-05-24 (Spec #1 R1 closeout)
**Status**: R1 NEEDS_FIX → fix-in-progress (backend-architect dispatch)
