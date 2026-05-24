# Post-Spec R1 Audit — QA Engineer Position
# Spec: aria-2.0-m6-cost-acceptance
# Auditor: qa-engineer (R1)
# Date: 2026-05-24
# Role: Stress-test acceptance criteria falsifiability + test coverage + edge cases + production failure modes

---

## Summary

The Spec is structurally sound and motivated. The dual-track schema rationale is well-grounded in
`[[project_glm_routing_luxeno]]`. The Luxeno=0 false-positive prevention (AC-3) is correctly
identified and partially addressed. However, the Spec has 4 Critical gaps that prevent Phase B from
producing unambiguous PASS/FAIL evidence, plus 7 Important gaps that will produce flaky or
misleading test results in production conditions. All findings include a concrete rewrite.

**Verdict: NEEDS_FIX**

Critical findings must be closed before Phase A.2 R2 audit. The Spec cannot be Approved in its
current state because AC-1, AC-5, AC-7, and AC-9 are not yet binary-falsifiable as written
(`[[feedback_falsifiable_evidence_for_binary_acceptance]]`).

---

## Findings by Severity

### CRITICAL

---

#### C-1 — AC-1 freshness gate uses naive UTC with timezone-unaware comparison

**Location**: proposal.md §AC-1, inline Python snippet.

**Finding**: The inline verification script calls `datetime.datetime.fromisoformat(d['freshness_ts'].rstrip('Z'))` to strip the trailing `Z`, then compares against `datetime.datetime.utcnow()`. This is fragile in three ways:

1. `fromisoformat()` in Python < 3.11 does not accept the `+00:00` suffix that ISO-8601 UTC strings
   may carry (e.g., if the snapshot script writes `2026-05-24T12:00:00+00:00` instead of
   `2026-05-24T12:00:00Z`). `rstrip('Z')` only strips a literal trailing `Z`; it silently leaves
   `+00:00` in place, making `fromisoformat()` raise on Python 3.10 (the likely runtime per Nomad
   container image).
2. `datetime.datetime.utcnow()` is timezone-naive. If the snapshot script writes a
   timezone-aware string (even after stripping `Z`), the subtraction raises `TypeError: can't subtract
   offset-naive and offset-aware datetimes`.
3. Clock skew scenario: if `freshness_ts` is in the **future** (e.g., by 30 seconds due to NTP
   drift), `age` is negative. `negative < 86400` is `True`, so a future timestamp PASSES the
   freshness gate — this is incorrect; a future timestamp is also an anomaly that should be
   flagged.

**Binary-falsifiable gap**: An implementor must guess which string format the snapshot script
will actually emit. Three different valid ISO-8601 UTC serializations produce three different
behaviors in the verification snippet.

**Concrete rewrite for AC-1**:

Replace the inline snippet in proposal.md §AC-1 with:

```
Evidence: file `.aria/cost.json` exists AND the following check passes:
  python3 -c "
  import json, sys
  from datetime import datetime, timezone, timedelta
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
  "
The snapshot script MUST write freshness_ts as RFC-3339 UTC with explicit offset
'+00:00' (e.g., '2026-05-24T12:00:00+00:00'), not bare 'Z', to guarantee
datetime.fromisoformat() parses correctly on Python 3.9+ without the 3.11 backport.
Boundary: age STRICTLY LESS THAN 86400 seconds (i.e., < not <=). A snapshot written
exactly 86400 seconds ago is STALE.
```

Add to T1.2 in tasks.md: "freshness_ts MUST be serialized as `datetime.now(timezone.utc).isoformat()` which produces `+00:00` suffix."

---

#### C-2 — AC-5 boundary operator is ambiguous: `>= 0.80 * threshold` vs `> 0.80 * threshold`

**Location**: proposal.md §AC-5, §What D, tasks T3.3, T3.4.

**Finding**: The §What D prose says "if `metered_usd.cost_usd >= 0.8 * m6.cost_thresholds.zhipu_30d_usd`"
(uses `>=`). AC-5 says the boundary unit test uses `cost_usd = 0.80 * zhipu_30d_usd` and asserts
`feishu_send` IS called. This is internally consistent in the Spec text but leaves open:

1. **Float precision**: `0.80 * threshold` where threshold is a float stored in JSON may not
   equal the computed value exactly due to IEEE-754 representation. If threshold=10.0,
   then `0.80 * 10.0 = 8.0` exactly, but for threshold=3.33, `0.80 * 3.33 = 2.664` which
   may differ in LSB. The test at T3.3 "boundary" could flip PASS/FAIL depending on the
   production computation order.
2. **No boundary test for EXACTLY 80.0%**: T3.4 tests `0.79 * threshold` (below). T3.3 tests
   `0.80 * threshold` (at). The test for "just above but not at" (e.g. `0.801 * threshold`) is
   absent. The boundary semantics are `>=` per §What D, but the three-zone coverage (below /
   at / above) is incomplete in tasks.

3. **pct_used field contract**: AC-5 asserts `pct_used >= 80` but does not specify the unit (0-100
   or 0.0-1.0). The Feishu card field is described as `pct_used` without a unit convention. An
   implementor who writes `pct_used = cost_usd / threshold` (range 0.0-1.0) will produce 0.80,
   not 80, and the assertion `pct_used >= 80` will fail even on correct code.

**Concrete rewrite for AC-5**:

```
AC-5 — 80% Feishu alarm fires correctly

Evidence: unit tests with exact IEEE-754-stable threshold arithmetic:

  test_alarm_at_boundary: metered_usd.cost_usd = threshold * Decimal('0.80')
    (use Python decimal.Decimal for the test fixture to avoid float drift)
    → feishu_send IS called; card field pct_used == 80 (integer, range 0-100).

  test_alarm_below_boundary: metered_usd.cost_usd = threshold * Decimal('0.7999')
    → feishu_send NOT called.

  test_alarm_above_boundary: metered_usd.cost_usd = threshold * Decimal('0.801')
    → feishu_send IS called.

Boundary semantics: alarm fires when cost_usd >= 0.80 * threshold (inclusive).
pct_used field unit: integer 0-100 (e.g., 80, not 0.80).
```

Add to T3.3 and T3.4 in tasks.md: "use `decimal.Decimal` for fixture math to avoid IEEE-754 drift in boundary comparison."

---

#### C-3 — AC-7 "3 consecutive days" semantics are under-specified: calendar days vs 72h rolling, gap handling

**Location**: proposal.md §AC-7, §What G, tasks T5.8, T5.10.

**Finding**: "consecutive dates ending no earlier than today - 1 day" is ambiguous on three axes:

1. **Calendar vs rolling**: "today - 1 day" is a calendar concept (midnight UTC boundary), but
   nothing specifies the timezone for "today". If the Nomad job runs at 23:50 UTC and the
   validator runs at 00:10 UTC the next day, "today" shifts by one calendar day between snapshot
   write and validation.

2. **Gap tolerance**: What if day-2 of the 3-day window is missing (cron failed once)? The Spec
   says "≥3 files with consecutive dates" — this implies a strict 3-consecutive-day requirement.
   But is `[2026-05-22, 2026-05-24]` (gap at 2026-05-23) treated as 2 consecutive or 3 total?
   The Spec text says "consecutive" (strict) but the word "consecutive" is not defined in the
   check algorithm. T5.8 says "≥3 files with consecutive dates" but does not specify the gap
   detection algorithm.

3. **Unit test T5.10 only tests the happy path**: T5.10 tests `today-3, today-2, today-1` (full
   coverage) and `only 2 files → exit non-zero`. It does NOT test the gap case
   `[today-4, today-2, today-1]` (3 files, 2 consecutive pairs with 1 gap). A naive
   implementation that counts files without checking date adjacency will PASS this input falsely.

**Concrete rewrite for AC-7 / T5.8**:

```
AC-7 — 3-day rolling history exists before Spec #2 kickoff

Definition: "3 consecutive calendar days" means the 3 most-recent snapshot dates form
an unbroken sequence (date[i+1] == date[i] + timedelta(days=1)), evaluated in UTC at
validation time. "today" is defined as datetime.now(timezone.utc).date().

The check passes if AND ONLY IF:
  (a) ≥3 files exist in .aria/cost-snapshots/ matching cost-YYYY-MM-DD.json
  (b) The 3 most-recent dates (sorted descending) form a consecutive sequence
      with no gaps
  (c) The most recent snapshot date is no earlier than today - 1 day (i.e.,
      either today or yesterday in UTC)

A set of [today-4, today-2, today-1] files (gap at today-3) FAILS condition (b)
even though it has ≥3 files.

Add to T5.10: test case with gap:
  mock files: [today-4, today-2, today-1] → exit non-zero (gap detected)
  mock files: [today-3, today-2, today-1] → exit 0 (consecutive)
  mock files: [today-2, today-1, today]   → exit 0 (including today)
  mock files: [today-5, today-4, today-3] → exit non-zero (most recent is today-3, too old)
```

---

#### C-4 — AC-9 exit code semantics unspecified; "non-zero" conflates infra failure with AC failure

**Location**: proposal.md §AC-9, tasks T4.1-T4.4, AD-M6-3 slot (deferred to Phase B).

**Finding**: AC-9 states "exit code non-zero when any check fails" without differentiating exit
codes. AD-M6-3 defers "exit code semantics" to Phase B. This creates a falsifiability gap: if
Phase B implements `sys.exit(1)` for AC failures and `sys.exit(2)` for infra errors (missing file,
corrupt JSON, missing config key), the acceptance check in CI cannot distinguish "the system is
not meeting cost acceptance" from "the environment is broken". By deferring the decision to Phase B,
the acceptance script's semantics are underspecified at approval time, meaning the audit cannot
verify that the implementation will produce unambiguous PASS/FAIL evidence.

Per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`, exit code semantics are a contract
that must be specified before implementation, not discovered during implementation.

**Concrete rewrite for AC-9**:

```
AC-9 — acceptance script is binary-falsifiable

Exit code contract (must be specified in this Spec, not deferred to AD-M6-3):
  0   — all sub-checks (AC-1..AC-4) PASS
  1   — one or more AC sub-checks FAIL (data condition: stale, wrong schema, null violation, missing threshold)
  2   — infrastructure error that prevents evaluation (missing .aria/cost.json, corrupt JSON,
         missing .aria/config.json, missing m6.cost_thresholds key)

A CI gate that exits non-zero because cost.json is missing should produce exit 2, not 1.
Exit code 1 is reserved for "file exists, parseable, but data does not meet criteria."

The script must also handle: corrupt JSON (catch json.JSONDecodeError → exit 2, print
[ERROR] AC-0: corrupt JSON: <filename>).
```

Close AD-M6-3 in Phase A (move from "slot" to defined): specify the above 3-code contract in the
proposal.md §How AD table before Phase A.2 R2.

---

### IMPORTANT

---

#### I-1 — cost.json missing entirely: AC-1 check raises FileNotFoundError, not exit 1

**Location**: proposal.md §AC-1 inline snippet; tasks T4.1, T4.2.

**Finding**: The AC-1 Python snippet calls `json.load(open('.aria/cost.json'))` without a try/except.
If the file does not exist (cron has never run — a legitimate production failure mode per audit
focus area 3), the script raises `FileNotFoundError` which produces a Python traceback and exit
code 1. However, this is indistinguishable from an AC-1 data failure because the script also exits
1 for stale data. Per C-4 above, file-missing should be exit 2. But even before C-4 is resolved,
the current snippet provides no labeled `[FAIL]` output — just a raw traceback. This fails the
requirement in AC-9 that each check emits `[PASS]` or `[FAIL: <reason>]` labelled output.

T4.2 only tests the "known-good fixture" path. There is no task requiring a test for the
file-missing scenario.

**Rewrite**: Add to T4.1: "if `.aria/cost.json` is absent, emit `[ERROR] AC-1: cost.json not found — cron has never run` and exit 2." Add T4.5: unit test for file-missing → exit 2 with expected error label.

---

#### I-2 — corrupt JSON production failure mode not tested anywhere

**Location**: proposal.md §Risks (not listed), tasks (no task covers corrupt JSON input).

**Finding**: cost.json written by the cron script could be partially written if the cron job is
interrupted mid-write (Nomad alloc kill during json.dump). A corrupt JSON file will cause
`json.JSONDecodeError` in the acceptance check, the freshness gate (AC-1), and validate-m6-handoff.py
(AC-8 cost_measurement_method check). None of the test tasks (T1.3, T4.2-T4.4, T5.9) cover this
case. The atomic-write pattern (write to `.aria/cost.json.tmp` then `os.rename()`) should be
specified in T1.1 to prevent partial-write corruption. This is a production failure mode classified
in audit focus area 3.

**Rewrite**: Add to T1.1: "snapshot script MUST use atomic write: write to `.aria/cost.json.tmp` then `os.rename('.aria/cost.json.tmp', '.aria/cost.json')` so a mid-write kill cannot produce corrupt JSON." Add T4.6: unit test for corrupt JSON input → `[ERROR] AC-0: JSON parse error` + exit 2.

---

#### I-3 — NULL token_cost_usd in SQLite source data not handled

**Location**: proposal.md §What A (cost aggregation query description), tasks T1.3.

**Finding**: The cost aggregation reads `SUM(token_cost_usd)` from the dispatches table for
Zhipu-routed rows. If any Zhipu-routed dispatch has `token_cost_usd IS NULL` (possible for
dispatches written before the M2 `update_token_usage` path was active, or for failed dispatches
that never reached token accounting), `SUM()` in SQLite silently ignores NULL rows. This means
`metered_usd.cost_usd` will be the sum of non-NULL rows only, potentially undercounting actual
cost. The Spec does not specify whether the query should `COALESCE(token_cost_usd, 0)` explicitly
or rely on SUM's NULL-ignoring behavior.

T1.3 tests "fixture rows" but does not include a fixture with NULL token_cost_usd rows. The test
will pass with any SUM implementation, including one that silently undercounts.

**Rewrite**: Add to T1.3: "fixture includes ≥1 row WHERE token_cost_usd IS NULL; assert the computed `metered_usd.cost_usd` equals the SUM of non-NULL rows only (not including nulls as 0); document explicitly in T1.1 that `COALESCE` is intentionally NOT used because NULL rows are excluded from cost attribution per dispatch lifecycle semantics." Alternatively, add a row-count annotation to the output JSON: `"null_cost_rows_excluded": N` so anomalies are visible.

---

#### I-4 — Zhipu cost_usd as string (API returns "12.34" not 12.34): type coercion unspecified

**Location**: proposal.md §AC-2 (isinstance check), tasks T1.2, T1.3.

**Finding**: AC-2 asserts `isinstance(d['metered_usd']['cost_usd'], (int, float))`. If the
aggregation query returns a string (e.g., if the snapshot script reads a cached API response where
Zhipu serializes cost as a JSON string rather than a number, or if the SQLite aggregate returns a
Python `Decimal` type), the isinstance check will fail and the acceptance script exits non-zero
despite correct data.

More critically: if the snapshot script writes `cost_usd` as a string by accident (e.g.,
`json.dumps` receives a `str` value from a row fetch without explicit `float()` cast), the JSON
file will contain `"cost_usd": "12.34"` — a valid JSON file that passes `json.load` but fails
AC-2. T1.3 does not test this path.

**Rewrite**: Add to T1.1/T1.2: "the snapshot script MUST cast `token_cost_usd` aggregate result to `float` explicitly: `metered_usd_cost = float(cursor.fetchone()[0] or 0.0)`. If the source data returns a string representation, float() will coerce it; if it returns None (no rows), `0.0` is used." Add T1.5: unit test where the SQLite fixture returns the aggregate as a string → assert output cost.json has a float value.

---

#### I-5 — validate-m6-handoff.py abi_compat grep checks have high false-negative risk for in-comment matches

**Location**: proposal.md §What F (checks 1-5), tasks T5.2-T5.6.

**Finding**: Per audit focus area 8, each of the 5 grep-based abi_compat checks can produce false
negatives or false positives:

- T5.5 (`check_comment_poll_direct_transition`): greps for `_handle_s7_human_gate` call presence.
  If this function is defined in the file but the call is wrapped in a condition that makes it
  unreachable (e.g., `if False: _handle_s7_human_gate()`), the grep passes but the promise is
  violated. The Spec says "assert it is not removed or commented out" but grep cannot detect
  dead-code wrapping.

- T5.6 (`check_risk_tier_dual_write_literal_always`): greps for `'always'` literal in
  `dispatcher/db INSERT path source files`. The string `'always'` may appear in a docstring,
  comment, or test mock without being in the INSERT path. The false-positive risk is high.
  The `validate-m5-handoff.py` sibling (which this Spec creates a sibling to) uses `re.search`
  with context-specific patterns around the INSERT statement; the Spec does not specify an
  equivalently precise pattern for T5.6.

- T5.2 (`check_dispatch_audit_log_immutable`): greps `004_schema_v4_additive.sql` to "assert
  triggers are not dropped." A file that contains neither `DROP TRIGGER` nor the trigger
  definition passes the check by absence, which is correct only if the triggers are defined
  elsewhere (schema.sql). The logic is: (a) schema.sql contains trigger keyword PRESENT +
  (b) 004 file does not contain DROP. But the check for (b) absence is not specified — the
  task says "grep 004 to assert triggers are not dropped" which could be interpreted as
  "assert the trigger NAMES appear in 004" (wrong: 004 is additive, not where triggers live)
  or "assert DROP TRIGGER does not appear in 004" (correct). The intent must be made explicit.

**Rewrite**: Add to each of T5.2-T5.6 a required pattern precision note:
- T5.2: "assert `schema.sql` contains `audit_no_update` and `audit_no_delete` trigger names; assert `004_schema_v4_additive.sql` does NOT contain `DROP TRIGGER` (negative grep, not positive grep)."
- T5.5: "grep pattern must match a non-commented, non-dead-code function call; use `re.search(r'^\s*[^#]*_handle_s7_human_gate\s*\(', content, re.MULTILINE)` to exclude comment lines."
- T5.6: "grep pattern must be scoped to the INSERT statement block, not any occurrence of `'always'`; minimum pattern: `re.search(r\"INSERT.*risk_tier_stub.*'always'\", content, re.DOTALL)` or equivalent that anchors to the INSERT context."

---

#### I-6 — Feishu alarm: ARIA_FEISHU_WEBHOOK_URL missing at runtime silently raises NotConfigured

**Location**: proposal.md §What D (alarm path), §Constraints (OOS-6), tasks T3.1.

**Finding**: The existing `feishu_webhook.py` raises `NotConfigured` (a `RuntimeError` subclass)
at `send()` time if `ARIA_FEISHU_WEBHOOK_URL` is not set. This is correct fail-fast behavior.
However, the cost alarm script (T3.1) must handle this exception; if it does not, the cron job
will crash with an unhandled exception rather than logging a clear error message. The Spec does
not specify whether an uncaught `NotConfigured` in the alarm path should (a) abort the entire
cron run (preventing cost.json from being written), or (b) log a warning and continue writing
cost.json without sending the alarm.

If (a), a misconfigured `ARIA_FEISHU_WEBHOOK_URL` Nomad var causes cost.json to never be updated,
which cascades to a stale-data AC-1 failure — masking the root cause (missing webhook config).
If (b), cost data is written but the alarm silently fails.

**Rewrite**: Add to T3.1: "if `ARIA_FEISHU_WEBHOOK_URL` is absent at runtime, the cron script MUST: (1) write cost.json (do not abort), (2) log `[WARN] alarm-skipped: ARIA_FEISHU_WEBHOOK_URL not configured; Feishu alarm suppressed`, (3) exit 0 (cron should not fail due to missing alarm config). The NotConfigured exception must be caught around the `feishu_send` call only, not around the snapshot write."

Add a unit test T3.7: `ARIA_FEISHU_WEBHOOK_URL` absent + cost above threshold → `feishu_send` NOT called; warning log IS emitted; cost.json IS written; process exit 0.

---

#### I-7 — Concurrent write race: cron script + Spec #2 reader have no file-lock contract

**Location**: proposal.md §What A (archive pattern), §Dependencies (Spec #2 upstream dependency).

**Finding**: The cron script writes `.aria/cost.json` and archives to `.aria/cost-snapshots/cost-YYYY-MM-DD.json`. Spec #2's runtime observability (TG-A `check_3_day_rolling_history_exists`) reads these files. If both run concurrently (Nomad periodic job + Spec #2 Phase B validation), there is a read-during-write window. The Spec does not specify a file-locking or atomic-write contract for the archive step.

This is partially mitigated by the atomic-write recommendation in I-2 above (for cost.json). However, the archive copy step `cost-snapshots/cost-YYYY-MM-DD.json` also needs an atomic pattern or a documented non-concurrent assumption.

**Rewrite**: Add to T1.1: "Archive write is also atomic: write to `.aria/cost-snapshots/cost-YYYY-MM-DD.json.tmp` then `os.rename()`. Document in AD-M6-2 that concurrent reader/writer safety is achieved via atomic rename, not file locking."

---

### MINOR

---

#### m-1 — AC-3 second sub-check (SQLite SELECT) is a schema existence test, not a falsifiable acceptance test

**Location**: proposal.md §AC-3 second paragraph.

**Finding**: The SQLite query `SELECT COUNT(*) FROM dispatches WHERE provider = 'luxeno' AND token_cost_usd IS NULL` verifies that the column exists and null semantics work. It returns a count of 0 or more and the Spec says "produces a row count ≥ 0 without error" — this always passes as long as the column exists, even if there are no Luxeno rows at all. It does not verify that no Luxeno rows have `token_cost_usd = 0` (a non-null false value). This is not a meaningful acceptance test; it is a schema sanity check. The correct test would be `SELECT COUNT(*) FROM dispatches WHERE provider = 'luxeno' AND token_cost_usd IS NOT NULL` → assert count is 0 (no non-null Luxeno cost rows).

**Rewrite**: Replace the second paragraph of AC-3 with: "Additionally: `SELECT COUNT(*) FROM dispatches WHERE provider = 'luxeno' AND token_cost_usd IS NOT NULL` must return 0. A non-zero count would mean Luxeno dispatches have been incorrectly written with a cost value, violating the null-attribution contract."

---

#### m-2 — T5.7 cost_measurement_method check has ambiguous fallback logic

**Location**: tasks.md T5.7.

**Finding**: T5.7 specifies: "if `cost_measurement_method` field present in cost.json use it; else verify schema documentation (acceptance script header or AD comment) explicitly declares the method per provider." The "else" branch (verify documentation) is not binary-falsifiable by a Python script — a script cannot meaningfully verify that an "AD comment" exists and is accurate. This fallback degenerates to a doc-reading exercise that passes trivially if any comment containing the method name is present.

**Rewrite**: Add to T5.7: "If `cost_measurement_method` is absent from cost.json, the check MUST fail with `[WARN] cost_measurement_method field absent from cost.json; add field or this check will be promoted to FAIL in M7+`. The documentation verification fallback is advisory only in M6 (downgraded to warning, not hard fail) because the current schema (§What A) does not include this field. If the field IS added to the schema, the check is a hard fail on invalid enum values."

---

#### m-3 — AD-M6-1/AD-M6-2/AD-M6-3 all deferred to Phase B: three critical decisions left open

**Location**: proposal.md §How AD table; tasks T6.1-T6.3.

**Finding**: All three AD slots are deferred to Phase B. AD-M6-3 (exit code semantics) is Critical
per C-4 above. AD-M6-1 (bash vs Python, standalone vs cron extension) and AD-M6-2 (archive naming
+ retention) affect testability: if the script is bash, the unit test framework and mock layer
strategy (T3.3-T3.5) differ from Python. Deferring until Phase B means T-schema and T-alarm tasks
start without the fundamental implementation contract locked.

**Rewrite**: Resolve AD-M6-1 and AD-M6-3 in proposal.md before Approved status. Proposed resolution:
- AD-M6-1: Python (same language as existing aria_layer1; bash would require subprocess mocking in tests; aligns with `[[feedback_lib_dir_script_relative_default]]`). Integrate with existing cron job as a new sub-command rather than a new job.
- AD-M6-3: 3-code exit convention per C-4 rewrite above.
- AD-M6-2: can remain Phase B (archive naming is non-blocking for other tasks).

---

#### m-4 — Negative cost_usd (refund / accounting correction) not handled

**Location**: proposal.md §AC-2, tasks T1.3.

**Finding**: AC-2 asserts `isinstance(d['metered_usd']['cost_usd'], (int, float))` but does not assert `>= 0`. If Zhipu billing ever returns a credit/refund (negative value), `SUM(token_cost_usd)` could be negative. A negative `cost_usd` would pass the isinstance check and would fail the `>= 0.8 * threshold` alarm comparison silently (negative < any positive threshold). This is a silent failure mode.

**Rewrite**: Add to T1.3: "assert `metered_usd.cost_usd >= 0.0`; if the SQL aggregate returns a negative value (refund or accounting error), the snapshot script should log `[WARN] negative cost aggregate detected: {value}; clamping to 0.0 for alarm evaluation` and write `0.0` to cost.json rather than a negative value, to prevent silent alarm suppression."

---

### OBSERVATION

---

#### O-1 — Test fixture provenance is unspecified: inline JSON literals vs fixture files

**Location**: tasks T1.3, T4.2, T5.9, T5.10.

**Finding**: Tasks reference "fixture" or "in-memory SQLite fixture" and "known-good fixture `.aria/cost.json`" without specifying whether fixtures are inline Python literals in the test code or separate fixture files. Per `[[feedback_pre_draft_bug_hunt_discipline]]`, schema changes require touching N tests if fixtures are inline. The M5 pattern used `importlib` dynamic load and committed canonical instances (per `[[feedback_python_script_importlib_smoke]]`). This Spec should follow the same pattern.

**Suggestion**: Add to T1.3 and T4.2: "fixtures are inline Python dict literals in the test function scope; cost.json schema is simple enough that file separation adds overhead without benefit at this scale."

---

#### O-2 — Cross-platform declaration absent

**Location**: proposal.md (no platform section).

**Finding**: Per audit focus area 10, the Spec does not declare that Phase B runs exclusively on
Linux (Nomad/Aether). The snapshot script, acceptance checks, and validate-m6-handoff.py all use
POSIX paths. If a contributor were to run tests on Windows or macOS, `Path()` constructs and
`os.rename()` semantics differ. Since all prior Aria specs run on Nomad Linux only, this is low
risk but should be documented.

**Suggestion**: Add a single line to §Constraints or §Dependencies: "Implementation target: Linux only (Nomad alloc running Python 3.x per aria-layer1 container image). macOS/Windows compatibility is not required."

---

#### O-3 — Multiple snapshots within same second (cron jitter) not specified

**Location**: proposal.md §What A (archive naming), tasks T1.1.

**Finding**: Archive files are named `cost-YYYY-MM-DD.json`. If the cron job fires twice in the
same day (e.g., manual re-run + scheduled run), the second write silently overwrites the first.
The Spec does not specify whether overwrite is intentional (always keep latest per day) or
an error. The AC-7 check relies on date-uniqueness; if overwrite is allowed, it functions
correctly. But if a partial overwrite occurs (first run succeeds, second run crashes mid-write),
the atomic-write pattern from I-2 must apply to the archive step as well (already covered there).

**Suggestion**: Document in AD-M6-2: "archive naming is date-unique; multiple runs on the same day overwrite the prior file (latest snapshot per day is retained). This is intentional: the daily snapshot reflects the most recent state of the rolling 30d window."

---

## Verdict

**NEEDS_FIX**

4 Critical findings (C-1 through C-4) prevent this Spec from being Approved. They collectively
produce a Phase B where key acceptance criteria — AC-1 (freshness gate), AC-5 (alarm boundary),
AC-7 (3-day history), and AC-9 (exit code semantics) — cannot produce unambiguous binary PASS/FAIL
evidence as required by `[[feedback_falsifiable_evidence_for_binary_acceptance]]`.

## Verdict Rationale

The Spec's architecture and motivation are sound. The dual-track schema design correctly handles the
Luxeno null-attribution problem. The abi_compat cross-check structure follows the validated M5
precedent in `validate-m5-handoff.py`. The Risks section correctly identifies R-M6-5 (mock-shape
mismatch per `[[feedback_test_mock_pattern_hides_prod_bug]]`) and R-M6-6 (Spec body propagation
per `[[feedback_spec_v2_body_propagation_2pass]]`).

The gaps are in test-boundary specification and production failure mode coverage — precisely the
areas where the qa-engineer audit role is expected to add value. Concretely:

- C-1: Without UTC-aware freshness comparison, the Python < 3.11 runtime in the Nomad container
  will raise TypeError on the first real production run, blocking acceptance evidence entirely.
- C-2: Without `decimal.Decimal` and three-zone boundary coverage, a `>=` vs `>` implementation
  bug at exactly 80% will survive all specified tests.
- C-3: Without gap-detection in the consecutive-day check, an operator who missed one cron run
  gets a false PASS for the Spec #2 gate condition, allowing Spec #2 to start with incomplete data.
- C-4: Without a differentiated exit code contract, CI cannot distinguish "cost threshold exceeded"
  from "environment is broken" — both show as exit 1, making the acceptance signal ambiguous.

The 7 Important findings address production failure modes that are likely to occur in the first
week of operation (missing cost.json, corrupt JSON, NULL SQLite rows, string cost_usd, missing
webhook env var, concurrent write) and grep-pattern precision for the abi_compat checks.

Recommended path to R2: author closes C-1 through C-4 with the exact rewrites provided above,
addresses I-2 (atomic write) and I-6 (NotConfigured handling) as they affect correctness, and
documents the resolution. R2 audit can proceed with a 4/4 SCOPE_OK verdict if those items are
closed.

---

**Auditor**: qa-engineer (R1)
**North-star memory refs**: `[[feedback_falsifiable_evidence_for_binary_acceptance]]`,
`[[feedback_mock_layer_per_failure_semantic]]`, `[[feedback_test_mock_pattern_hides_prod_bug]]`,
`[[feedback_schema_migration_3_safeguard_pattern]]`
**Filed**: 2026-05-24
