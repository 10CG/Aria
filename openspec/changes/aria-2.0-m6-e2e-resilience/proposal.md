# Aria 2.0 M6 Spec #2 — E2E Resilience (runtime observability + crash recovery + humanized samples)

> **Level**: 3 (Full — cross-cuts runtime observability + crash recovery + humanized command samples; three internal task groups)
> **Status**: R1 fixes applied (2026-05-24) — pending R2 verification
> **Change ID**: `aria-2.0-m6-e2e-resilience`
> **Parent US**: [US-026](../../../docs/requirements/user-stories/US-026.md)
> **Parent PRD**: [prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) (Week 26-30, ~82h total, post `a786444` PRD patch, §638-646)
> **Predecessor Spec**: [aria-2.0-m5-replay-reconciler-drift-review-loop-audit](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/proposal.md) (M5 archived 2026-05-23)
> **Sibling Spec (locked dependency)**: [aria-2.0-m6-cost-acceptance](../aria-2.0-m6-cost-acceptance/proposal.md) — **Approved 2026-05-24 commit `c29a800`**; Spec #2 Phase B MUST NOT start until Spec #1 AC-7 (`--check-3-day-history`) PASS (3-day cost trending data precondition)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2 Spec #2 + §4 P-4..P-9 + §5 R3 final positions)
> **Effort baseline**: ~29h impl (~10h TG-A + ~13h TG-B + ~6h TG-C; +1h Q-NEW-1 hybrid mock layer vs 28h base). Phase A audit overhead ~1h (not impl) — single SoT per `[[feedback_spec_v2_body_propagation_2pass]]`.
> **abi_compat hard constraints**: 5 forward-binding promises from m5-handoff.yaml (lines 151-172, enforced by Spec #1 validate-m6-handoff.py; this Spec must not violate them during TG-A/B implementation):
>   1. `dispatch_audit_log_immutable_promise` — M6 must not DROP audit triggers
>   2. `rework_round_cap_default_3_promise` — ARIA_REWORK_MAX_ROUND default=3 must remain in code
>   3. `spec_drift_threshold_default_70_promise` — ARIA_SPEC_DRIFT_THRESHOLD default=70 must remain in code
>   4. `comment_poll_direct_transition_promise` — S7→S8 comment-poll direct call must remain primary
>   5. `risk_tier_dual_write_literal_always_promise` — dual-write 'always' to risk_tier_stub must remain
> **AD allocation reservation**: AD-M6-4 / AD-M6-5 / AD-M6-6 reserved for **this Spec #2** only.
> Spec #1 holds AD-M6-1/2/3 (per Q4 lock 2026-05-24). Spec #3 must start from AD-M6-7+.
> **Audit trajectory**:
>   - Phase A.2 R1 NEEDS_FIX (post_spec 4-agent parallel, 2026-05-24): 6 Critical (T2-1..T2-6) + 1 Cross-Critical (X-T3) + 8 Important (I2-1..I2-8); R1 fixes applied same session (backend-architect agent). Aggregate: `.aria/audit-reports/post_spec-R1-aggregate-2026-05-24-aria-2.0-m6-sister-specs.md`.
>   <!-- R1-fixes applied 2026-05-24: T2-1 SQL columns, T2-2 state_machine path, T2-3 AC-6 Luxeno=0, T2-4 is_synthetic Mech-B removed, T2-5 AC-1 uptime metric, T2-6 AC-2 check order, X-T3 mean→median, I2-1..I2-8 -->

---

## Why

M5 shipped a production-grade autonomous dispatch loop (Track A T-deploy 2026-05-23, DEMO-M5-O3
verified) that completes the "can-run + can-be-trusted + can-self-manage" trifecta. Before Aria 2.0
releases under a "verified autonomous" label, the PRD (§630-641) requires three additional classes
of evidence that M5 alone cannot provide:

**1. Runtime resilience evidence (7-day E2E observation)** — A single successful dispatch is not
sufficient evidence for autonomous operation. PRD §630 requires a sustained 168-hour window
demonstrating that the dispatch loop continues running without manual intervention, handles a
stratified set of real work items (bug + feature + stale reopen), and completes ≥10 full S0→S9
cycles with acceptable S_FAIL rate. No such sustained evidence exists post-M5.

**2. Crash recovery completeness (6 failure modes tested)** — The M5 state machine handles the
nominal S0→S9 path. PRD §634 enumerates 3 infra crash modes (process kill + node kill + storage
corruption) and 3 LLM failure modes (rate-limit + malformed response + provider 5xx). The 2 deferred
modes (context-window overflow + safety refusal) are explicitly out of scope. Testing crash modes
against a live system would consume real LLM cost and is non-reproducible; the brainstorm
(DEC-20260524-001 Q-NEW-1) resolved on a hybrid mock layer — 4 modes at SDK boundary + 2 modes at
HTTP layer — enabling zero-cost deterministic test coverage.

**3. Humanized command sample quality (PRD §639 rubric)** — PRD §639 requires that autonomous
commands dispatched to human developers use natural language that is indistinguishable from a
skilled human engineer. The existing system produces functional commands, but no rubric-scored
corpus exists to evidence ≥7/10 median quality. Without this corpus, the "verified autonomous" claim
cannot be substantiated and Spec #3 (docs) cannot authoritatively reference humanized-command-patterns.md.

**Gate role in M6 sequencing**: This Spec gates Spec #4 (release-closeout). Spec #4's pre-release
RED/ABORT decision consumes this Spec's 7d uptime evidence, 6 crash mode PASS results, and median
≥7/10 sample score as mandatory preconditions. Additionally, TG-C samples cross-reference Spec #3
TG-DOCS-B `standards/autonomous/humanized-command-patterns.md` (BOTH-locations design).

**Spec #1 precondition**: This Spec requires ≥3 consecutive daily cost.json snapshots already
written by Spec #1 before the 7-day E2E run begins. The Day-1 probe (`m6-7d-day-1.md`) serves
as the gate checkpoint: it must confirm Spec #1 AC-7 (`--check-3-day-history`) PASS before
the 7-day clock starts.

---

## What

### In scope (~29h impl)

#### A. TG-A: Runtime Observability (~10h)

##### A.1 7-day Nomad alloc uptime gate

<!-- R1-T2-5 fix: TaskStates['aria-layer1']['StartedAt'] resets on task restart (not alloc
     restart). A task can restart mid-week while the alloc persists, causing false-FAIL on a
     legitimate 168h alloc. Fix: use alloc.CreateTime (alloc-level, does not reset on task
     restart) + persist alloc.ID at Day-1 as the authoritative clock start. (R1 audit 2026-05-24) -->
The 7-day E2E run requires the `aria-layer1` Nomad allocation to remain up for 168 continuous
hours (per qa M-qa-R3 acceptance). The uptime check uses the Nomad Alloc `CreateTime` field
(alloc-level, not task-level), which does NOT reset on task restart:

```bash
# Day-1 probe: persist alloc ID + CreateTime as canonical clock start
nomad alloc status <ALLOC_ID> -json \
  | jq '{alloc_id: .ID, create_time_ns: .CreateTime}' \
  > .aria/probes/m6-7d-day-1-alloc-anchor.json
```

**Uptime determination logic** (acceptance script):
1. Read persisted `m6-7d-day-1-alloc-anchor.json` (exit 2 if absent).
2. Query current alloc: `nomad alloc status <alloc_id> -json | jq '.ID, .CreateTime'`.
3. If `current.ID != anchored.alloc_id` → **AC-1 FAIL** (alloc was replaced; 7d run interrupted).
4. If `current.ID == anchored.alloc_id` AND `(now - CreateTime_ns/1e9) >= 604800` → **PASS**.

`CreateTime` in Nomad JSON is nanoseconds since Unix epoch. Convert: `alloc_age_s = (now_utc_ns - CreateTime) / 1e9`.

The Day-1 probe file (`.aria/probes/m6-7d-day-1.md`) must include:
```markdown
## Alloc anchor (Day-1 canonical clock start)
- Alloc ID: <alloc_id>
- CreateTime (ns): <int>
- CreateTime (human): <ISO-8601>
```

##### A.2 Dispatch tracker with path stratification

<!-- R1-T2-1 fix: SQL columns rewrite — `final_state`/`created_at`/`issue_type` do not exist
     in live dispatches schema (schema.sql:35-239). Terminal state column is `state` with value
     `'S9_CLOSE'`; date filtering uses `state_entered_at`; issue metadata lives in
     `dispatch_audit_log.payload_json` (json_extract). (R1 audit 2026-05-24) -->
A SQL query verifies that ≥10 dispatches completed the full S0→S9 path with required stratification.

**Schema reality (live `schema.sql:35-239`)**:
- Terminal closed state: `state = 'S9_CLOSE'` (NOT `'S9'`).
- Date filter column: `state_entered_at` (ISO-8601 UTC TEXT; NOT `created_at`).
- Per-dispatch issue metadata (title, labels, project): in `dispatch_audit_log.payload_json`
  via `json_extract` — NOT top-level columns on `dispatches`.
- Synthetic flag: `is_synthetic` (added by migration 006; DEFAULT 0).

**Stratification tracking approach**: Issue type (bug/feature/stale) is stored in the
`dispatch_audit_log` `state_transition` payload at S0_IDLE entry, accessible as
`json_extract(payload_json, '$.issue_labels')` or `$.issue_type_hint`. At Phase B kickoff,
the implementer must verify the exact payload key via:
```bash
sqlite3 aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/aria_layer1.db \
  "SELECT payload_json FROM dispatch_audit_log LIMIT 3;"
```
Then update the `json_extract` key in the SQL below accordingly.

**T-validate-schema-1 (schema validation task)**: Before writing any TG-A SQL implementation,
verify live `dispatches` schema column-by-column:
```bash
sqlite3 aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/aria_layer1.db \
  "PRAGMA table_info(dispatches);"
```
This is the schema drift regression guard per `[[feedback_validator_repo_drift_guard_test]]`.
A paired test triple must be committed with the schema validation check (see TG-A-validate).

```sql
-- R1-T2-1 fix: Uses live column names (state='S9_CLOSE', state_entered_at)
-- Stratification gate: ≥10 dispatches, ≥1 per required category
SELECT
    is_synthetic,
    SUM(1) as count
FROM dispatches
WHERE
    state = 'S9_CLOSE'
    AND state_entered_at BETWEEN :run_start AND :run_end
GROUP BY is_synthetic;
-- Separate per-type queries via dispatch_audit_log join (see AC-2 and TG-A-dispatch tasks)
```

<!-- P-7 thread: is_synthetic tagging mechanism -->
<!-- R1-T2-4 fix: Mechanism B removed — `title` column does not exist in live dispatches schema
     (confirmed schema.sql:35-239). Mechanism A is the only valid approach. AD-M6-4 locked
     to Mechanism A. (R1 audit 2026-05-24) -->
**is_synthetic tagging (P-7)**: Dispatches tagged as synthetic use **Mechanism A — Schema column
ONLY** (Mechanism B is structurally invalid; see constraint below):

- **Mechanism A — Schema column (LOCKED)**: `is_synthetic INTEGER DEFAULT 0` column on the
  `dispatches` table. Value `1` = synthetic fixture dispatch; value `0` = real issue dispatch.
  A new additive migration `006_schema_v5_add_is_synthetic.sql` adds this column
  (`ALTER TABLE dispatches ADD COLUMN is_synthetic INTEGER DEFAULT 0`), targeting schema version
  5.0. This follows the M5 additive migration pattern (per `[[feedback_schema_migration_to_version_bump]]`).
  See task T-schema-1 below.

Mechanism B (title prefix `[DEMO-M6-*]`) was **removed at R1 audit (2026-05-24)**: the
`dispatches` schema (live `schema.sql:35-239`) has no `title` column, making
`CASE WHEN title LIKE '[DEMO-M6-%]' THEN 1 ELSE 0 END` structurally invalid at the SQL layer
and producing `sqlite3.OperationalError: no such column: title` on day 1. AD-M6-4 is locked
to Mechanism A (schema column) — no Phase B decision required.

The Phase B implementer runs migration 006 and verifies abi_compat promises intact (see T-schema-1 + §A.7).

**Synthetic cap**: ≤70% of the ≥10 dispatches may be synthetic (i.e., at most 7 of 10 may be
`is_synthetic=1`). The remaining ≥3 must be real issues. This cap is enforced in the acceptance
SQL query.

**Stratification requirement**: of the ≥10 completed dispatches, ≥1 must be `issue_type='bug'`,
≥1 must be `issue_type='feature'`, ≥1 must be `issue_type='stale'`. These types may be real or
synthetic but must each be represented.

##### A.3 Daily probe snapshots

Seven daily snapshot files `.aria/probes/m6-7d-day-{1..7}.md` are written by the owner (manual) or
by a cron-driven probe script. Each file records:

```markdown
# M6 7-day probe — Day N (YYYY-MM-DD)

## Alloc status
- Alloc ID: <id>
- StartedAt: <ISO-8601>
- Uptime hours: <N.N>

## Dispatch summary (Day N cumulative)
- Total S9 completed: N
- S_FAIL count: N
- Stuck (>4h): N
- is_synthetic count: N / total

## Stratification (Day N)
| issue_type | count |
|------------|-------|
| bug        | N     |
| feature    | N     |
| stale      | N     |

## Health gate (Day 3 only — filled on Day 3)
- ≥1 complete S0→S9 cycle: YES/NO
- S_FAIL rate ≤50%: YES/NO (actual: N%)
- No stuck >4h: YES/NO
- Day-3 gate verdict: PASS/FAIL
```

##### A.4 Day-3 mid-run health gate

At Day-3 (hour 72), a mid-run health gate evaluates:

- **Gate condition 1**: ≥1 complete S0→S9 cycle observed in cumulative dispatches.
- **Gate condition 2**: S_FAIL rate ≤50% (i.e., `S_FAIL count / total dispatched <= 0.50`).
- **Gate condition 3**: No dispatch stuck in a non-terminal state for >4 hours continuously.

If any gate condition fails at Day-3, the owner MUST pause the 7d run, investigate, and restart
from Day-1. The final acceptance gate (AC-1) requires all 7 days of probe files to exist with
Day-3 gate verdict = PASS.

##### A.5 Pre-flight dry-run dispatches (P-8: fixture provenance)

Before the 7-day clock starts, 3 pre-flight dispatches validate the system end-to-end with real LLM
calls (real throwaway cost; hard cap: $2 per dispatch, total ≤$6 for 3 dispatches combined).

<!-- P-8: Pre-flight dispatch fixture provenance -->
**Fixture provenance (P-8)**: The 3 pre-flight dispatches must source from one of the following
(owner decides at Phase B kickoff, documented in `.aria/probes/m6-preflight-provenance.md`):

- **Option A — Replay M5 O3 captures**: Re-dispatch the same issue payload that DEMO-M5-O3 used
  (replay from `aria-orchestrator/docs/demo-m5-o3-*.yaml` if capture files exist). This is the
  preferred option as it provides direct regression continuity.
- **Option B — Fresh synthetic issues**: Create 3 `[DEMO-M6-P*]`-prefixed issues on the Aria Forgejo
  repo specifically for pre-flight (closed/labelled after pre-flight completes to avoid polluting
  the 7d dispatch pool).
- **Option C — Cross-project Kairos/SilkNode issues**: If Option A is unavailable and cross-project
  dispatch is already operational per P-9 conditions, use ≥1 real Kairos or SilkNode issue as one
  of the 3 pre-flight dispatches (evidences cross-project capability in pre-flight log).

The pre-flight log is committed to `.aria/probes/m6-preflight-log.md` (3 dispatch IDs, fixture
source, per-dispatch outcome, per-dispatch cost < $2 cap evidence).

##### A.6 Cross-project dispatch evidence (P-9: conditional)

<!-- P-9: Cross-project acceptance conditions -->
Cross-project Kairos/SilkNode dispatch is **conditional acceptance** — it is not a required gate
for the 7-day run PASS, but its presence upgrades AC-2 from PASS to PASS-WITH-CROSS-PROJECT
evidence.

**Conditions required for cross-project dispatch to count** (per ai R2CH-3 + qa M-qa-R3-10):

1. The target project (Kairos or SilkNode) has a Forgejo repo accessible by `aria-runner-bot`.
2. The aria-orchestrator ProviderRouter can reach the target project's issue tracker without new
   PAT scope additions (existing `aria-runner-bot` scopes sufficient — see
   `[[feedback_pat_scope_canonical_from_codebase_grep]]`).
3. At least 1 cross-project dispatch completes the full S0→S9 path during the 7d window.
4. The dispatch is tagged `is_synthetic=0` (cross-project real issues only; no synthetic cross-project
   dispatches in evidence).

If conditions 1-4 are met, the acceptance script emits `[PASS+] AC-2: cross-project evidence present
(project=<name>, dispatch_id=<id>)`. If conditions are unmet, AC-2 passes on Aria-only dispatches
with `[PASS] AC-2: Aria-only 7d window (cross-project conditional not met)`.

##### A.7 validate-m6-handoff.py paired test triple

<!-- P-6: TG-A → TG-B handoff checkpoint -->
**TG-A → TG-B handoff checkpoint (P-6)**: TG-A is declared content-complete when the following
are committed and passing:

1. All `.aria/probes/m6-7d-day-{1..7}.md` files exist (owner-filled or probe-script-filled).
2. `aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --tg-a` exits 0.
3. Alloc uptime ≥168h verified.
4. Dispatch stratification ≥10 with ≥1 bug/feature/stale verified.

TG-B implementation may begin in parallel with TG-A once pre-flight (A.5) completes and the
state machine source is stable (no active TG-A-driven schema migrations pending). TG-B does not
require TG-A 7d run to complete — it uses mock-only fixtures.

<!-- R1-I2-8 fix: Explicit non-mutation contract added. Spec #2 does NOT modify
     validate-m6-handoff.py. That file is owned by Spec #1 (aria-2.0-m6-cost-acceptance,
     commit c29a800). Spec #2 only invokes it for AC-7 verification and tests it for
     abi_compat regression. Any modification to validate-m6-handoff.py must go through Spec #1.
     (R1 audit 2026-05-24) -->
**Non-mutation contract**: `aria-orchestrator/docs/validate-m6-handoff.py` is owned by Spec #1
(`aria-2.0-m6-cost-acceptance`, commit `c29a800`). Spec #2 does **NOT** modify this file. Spec #2
only (a) invokes it as a subprocess for AC-7 verification and (b) tests it in TG-A-validate for
abi_compat regression. Any change to `validate-m6-handoff.py` requires a Spec #1 patch — not a
Spec #2 change.

The validate-m6-handoff.py script (Spec #1, already shipped) must have a **paired test triple**
(per backend M-ba-R3-1c): 3 unit tests that verify the abi_compat promises are still honoured
after any TG-A schema migration (particularly the `is_synthetic` column addition via migration 006):

- Test 1: schema.sql still contains `audit_no_update` and `audit_no_delete` after migration 006.
- Test 2: migration 006 does NOT contain `DROP TRIGGER`.
- Test 3: `validate-m6-handoff.py --check-abi-compat` still exits 0 after migration 006 applied
  to a test database.

---

#### B. TG-B: Crash Recovery (~13h, including +1h Q-NEW-1 hybrid)

##### B.1 6-mode crash recovery test suite

The crash recovery test suite covers all 6 modes enumerated in DEC-20260524-001 §2. All 6 modes
are **mock-only** (zero live LLM cost). The hybrid mock layer (Q-NEW-1) mocks 4 modes at the
SDK boundary and 2 modes at the HTTP transport layer.

<!-- P-4: Mock-layer-per-mode matrix -->
**Mock-layer-per-mode matrix (P-4, Q-NEW-1 hybrid rationale)**:

| Mode | ID | Failure type | Mock layer | Rationale |
|------|----|-------------|------------|-----------|
| Hermes SIGKILL mid-transition | Infra-1 | Process kill; state machine interrupted between state transitions | SDK boundary (`hermes_client.dispatch()` raises `ProcessKilledError`) | SIGKILL cannot be simulated at HTTP layer; Hermes client interface is the correct seam; reuses `test_t12` existing fixture |
| Layer 2 alloc SIGKILL | Infra-2 | Node kill; `aria-layer2` Nomad alloc forcibly terminated mid-task | SDK boundary (`layer2_client.run_task()` raises `AllocTerminatedError`; note: light-1 cannot be drained — Nomad `drain` requires node-level operator access not available in Layer 2 alloc context) | Drain API not available at alloc scope; SDK exception injection is the correct seam |
| SQLite WAL truncation | Infra-3 | Storage corruption; WAL file truncated to 0 bytes mid-checkpoint | SDK boundary (monkey-patch `sqlite3.connect()` to return a connection whose `execute()` raises `sqlite3.DatabaseError: database disk image is malformed`) | WAL manipulation requires filesystem ops; SDK-level DatabaseError injection avoids filesystem coupling; `integrity_check` rejection confirmed via `PRAGMA integrity_check` in recovery path |
<!-- R1-I2-5 fix: `llm_client.complete()` does not exist in production code. Real call sites are:
     - `silknode_client.call_llm(prompt, model)` (Luxeno path)
     - `zhipu_client.call_llm(prompt, model)` (Zhipu direct path)
     - `provider_router.call_llm(prompt, model)` / `provider_router.route_for_state(prompt, state)`
     (preferred call site for state handlers).
     Mock targets must use actual module paths. (R1 audit 2026-05-24) -->
<!-- R1-I2-6 fix: `RateLimitError` and `ProviderUnavailableError` are not defined in the
     production codebase (provider_router.py uses `LLMRouteExhausted` for exhaustion). For 429:
     `_classify_exception` maps HTTP-429 status to `HTTP_429` outcome string via `ZhipuHTTPError`
     or `_LLMHTTPError` (both have `.status` attribute). For 5xx: similarly classified as
     `HTTP_5XX` string outcome. Tests mocking LLM-4 at SDK boundary should mock the ProviderRouter
     to raise `LLMRouteExhausted` with a chain entry showing `outcome="http_429"`. Alternatively,
     mock the underlying `silknode_client.call_llm` or `zhipu_client.call_llm` to raise
     `_LLMHTTPError(status=429)` / `ZhipuHTTPError(status=429)`. (R1 audit 2026-05-24) -->
<!-- R1-I2-3 fix: LLM-4 (429) test must split Luxeno and Zhipu providers — they have different
     HTTP error classes: `_LLMHTTPError` (silknode_client) vs `ZhipuHTTPError` (zhipu_client).
     Two test files: test_crash_llm4_luxeno_429.py + test_crash_llm4_zhipu_429.py (or one
     parameterized file with explicit provider fixture). (R1 audit 2026-05-24) -->
<!-- R1-I2-4 fix: LLM-5/LLM-6 should use provider-specific httpx_mock URL patterns since
     Luxeno and Zhipu have different base URLs. Split: test_crash_llm5_luxeno.py +
     test_crash_llm5_zhipu.py (or parameterized with provider fixture). (R1 audit 2026-05-24) -->
| LLM 429 rate-limit | LLM-4 | Rate limit response mid-transition (S2/S3/S6 LLM call) | SDK boundary (mock `silknode_client.call_llm` to raise `_LLMHTTPError(status=429)` for Luxeno path; mock `zhipu_client.call_llm` to raise `ZhipuHTTPError(status=429)` for Zhipu path; OR mock `provider_router.call_llm` to raise `LLMRouteExhausted(chain=[{outcome:"http_429"}])` at router level) | 429 classified by `_classify_exception` in `provider_router.py`; LLM-4 test must cover both provider paths (two test files or parameterized fixture) |
| Invalid JSON response | LLM-5 | Malformed HTTP response body (non-JSON or truncated JSON) | HTTP layer (`httpx_mock` returns status=200, body=`"{ bad json"` on provider-specific URL pattern) | Invalid JSON arrives as valid HTTP; httpx_mock at transport layer correctly exercises JSON parse failure in SDK adapter; provider-specific URL patterns required (Luxeno ≠ Zhipu base URL) |
| Provider 5xx | LLM-6 | Provider server error mid-transition | HTTP layer (`httpx_mock` returns status=503, body=`{"error":"service_unavailable"}` on provider-specific URL) | 5xx classified as `HTTP_5XX` by `_classify_exception` in `provider_router.py`; provider-specific URL pattern required; split Luxeno+Zhipu test files |

**Mock-shape discipline (per `[[feedback_test_mock_pattern_hides_prod_bug]]`)**: Each mock must
reproduce the exact exception class and attribute shape that production code raises. For SDK-layer
mocks, use the actual exception classes from the production code path:
- `ProcessKilledError` (Infra-1 Hermes kill)
- `AllocTerminatedError` (Infra-2 layer2 kill)
- `sqlite3.DatabaseError` (Infra-3 WAL corruption)
- `_LLMHTTPError` (from `silknode_client`) or `ZhipuHTTPError` (from `zhipu_client`) with `.status=429` for LLM-4
- `LLMRouteExhausted` (from `provider_router`) for router-level exhaustion

Do not substitute `Exception`, generic `RuntimeError`, or non-existent `RateLimitError`/`ProviderUnavailableError` — mock-shape mismatch at SDK boundary hides real bugs.

For HTTP-layer mocks (LLM-5, LLM-6), `httpx_mock` must match the exact HTTP method + URL pattern
used by each provider's SDK adapter (Luxeno vs Zhipu have different base URLs). Validate mock
fixture shape against one real captured response to confirm the SDK parses the mock body through
the same code path as a real response.

##### B.2 WAL truncation scenario enumeration (P-5)

<!-- P-5: 4 WAL scenarios vs 3 -->
PRD §634 sub-clauses enumerate **4 WAL truncation scenarios** (not 3 as initially counted in R2).
The test suite must cover all 4:

| Scenario | ID | Description | Expected outcome |
|----------|----|-------------|-----------------|
| WAL truncated to 0 bytes pre-checkpoint | WAL-A | WAL file exists but is 0 bytes when connection opens | `sqlite3.DatabaseError` on first execute; state machine transitions to S_FAIL; recovery path triggers `integrity_check` PRAGMA |
| WAL truncated to 0 bytes mid-checkpoint | WAL-B | WAL file zeroed during an active checkpoint operation | `sqlite3.OperationalError: database is locked` or `DatabaseError`; same recovery path |
| WAL corrupted (non-zero, non-valid bytes) | WAL-C | WAL file contains garbage bytes (not zero-length) | `sqlite3.DatabaseError: database disk image is malformed`; same recovery path |
<!-- R1-I2-2 fix: WAL-D outcome contradiction resolved. WAL-D (deleted file) is NOT a corruption
     scenario — SQLite auto-recreates the WAL file; integrity preserved; NO S_FAIL. S_FAIL is
     reserved for WAL-A/B/C where actual corruption/lock is detected. (R1 audit 2026-05-24) -->
| WAL file deleted entirely | WAL-D | WAL file missing (not truncated, fully removed) | SQLite auto-recreates WAL on reconnect; data integrity preserved (no silent data loss); NO S_FAIL — recovery is successful; structured log `{"event":"wal_fault","scenario":"WAL-D","recovery":"wal_auto_recreated"}` |

All 4 WAL scenarios are tested via SDK-boundary mock (monkey-patch `sqlite3.connect()` to simulate
each error type). WAL-D uses `tmpdir` fixture with WAL file deleted before connection attempt.

Assertions **per scenario** (WAL-D differs from WAL-A/B/C):
- **WAL-A/B/C**: (a) state machine transitions to S_FAIL (corruption detected, not crash without
  state write); (b) `PRAGMA integrity_check` is invoked in the recovery handler; (c) structured
  log entry `{"event": "wal_fault", "scenario": "<WAL-A|B|C>", "recovery": "s_fail_set"}`.
- **WAL-D**: (a) NO S_FAIL — recovery succeeds (SQLite auto-recreates WAL); (b) subsequent clean
  connection can read/write successfully (no data corruption); (c) structured log entry
  `{"event": "wal_fault", "scenario": "WAL-D", "recovery": "wal_auto_recreated"}`.

##### B.3 State machine deterministic transition coverage

<!-- R1-T2-2 fix: `aria_layer1/state_machine.py` does NOT exist. State machine logic is
     distributed across 4 modules: extension.py, comment_poll.py, reconciler.py, tick_runner.py.
     Per Q1 lock (2026-05-24): Path B — multi-file coverage target. No new state_machine.py
     file will be extracted (zero scope creep). All references to aria_layer1.state_machine
     removed. (R1 audit 2026-05-24) -->
State machine 100% coverage targets deterministic transitions only. Stochastic states (S2/S3/S6)
have separate sub-tasks using mocked replay (zero live cost).

**State machine module distribution (Q1 lock 2026-05-24)**: The state machine logic is
distributed across 4 existing modules (verified in live codebase; `state_machine.py` does NOT
exist and will NOT be created — no scope creep):
- `aria_layer1.extension` — primary state handler dispatch (`_handle_s*` methods)
- `aria_layer1.comment_poll` — S5_AWAIT/S6_REVIEW comment polling transitions
- `aria_layer1.reconciler` — stuck detection, S7 timeout enforcement
- `aria_layer1.tick_runner` — orchestration loop, tick dispatch

**Coverage target (AC-4, Q1 locked)**:
```bash
pytest --cov=aria_layer1.extension,aria_layer1.comment_poll,aria_layer1.reconciler,aria_layer1.tick_runner \
       --cov-fail-under=100 \
       aria_layer1/tests/test_state_machine_*.py
```
Exit 0 = AC-4 PASS.

**Deterministic transition states**: S0_IDLE (initial), S1_SCAN (issue claimed), S4_LAUNCH
(PR submitted), S5_AWAIT (review received), S7_HUMAN_GATE (human gate), S8_MERGE (approved),
S9_CLOSE (merged/done), S_FAIL (terminal failure).

For each deterministic state, the test suite must cover:
- Normal outbound transition (e.g., S0_IDLE → S1_SCAN on issue claim).
- Failure-injected outbound transition (e.g., S0_IDLE → S_FAIL when Infra-2 SIGKILL during claim).
- Re-entry idempotency (e.g., S1_SCAN entered twice — second entry is a no-op, not a double-claim).

**Stochastic states (S2/S3/S6) — mocked replay sub-task**: Mocked replay uses captured LLM
response fixtures (committed to `aria-orchestrator/tests/fixtures/state_machine/`) to simulate
the S2_DECIDE/S3_BUILD_CMD/S6_REVIEW transitions deterministically. Zero live cost. Each fixture
file is a JSON capture of one real LLM response (from DEMO-M5-O3 or pre-flight captures).

<!-- AdvancingClock DI thread: per [[feedback_phase_b_velocity_patterns_2026-04-29]] -->
**AdvancingClock DI (per `[[feedback_phase_b_velocity_patterns_2026-04-29]]`)**: Any test that
exercises time-based transitions (stuck >4h detection, retry backoff, 7d window boundary) must
inject a `FakeClock` via dependency injection rather than wall-clock `datetime.now()`. The
`FakeClock` must implement:

```python
class FakeClock:
    def __init__(self, start: datetime):
        self._now = start
    def now(self) -> datetime:
        return self._now
    def advance(self, seconds: int) -> None:
        self._now += timedelta(seconds=seconds)
```

All state machine time-sensitive code paths must accept a `clock` parameter (default:
`RealClock()` which delegates to `datetime.now(timezone.utc)`). This prevents wall-clock
flakiness in CI (per `[[feedback_phase_b_velocity_patterns_2026-04-29]]`).

##### B.4 SQLite WAL fault injection shell script

<!-- M-qa-R3-8 NEW: PRD §634 cov gap -->
Per qa M-qa-R3-8, PRD §634 coverage gap: a shell script
`aria-orchestrator/acceptance/m6-wal-fault.sh` must be committed to document and verify the WAL
fault injection approach. The script:

1. Creates a temp SQLite DB with WAL mode enabled.
2. Truncates the WAL file to 0 bytes (simulates WAL-A).
3. Calls `aria_layer1` recovery handler via `python3 -m aria_layer1.recovery --wal-check <db_path>`.
4. Asserts exit code matches expected (0 = recovery successful, 1 = unrecoverable, 2 = S_FAIL set).
5. Cleans up temp files.

The shell script is committed as a regression artifact and referenced in AC-4. Its existence in
`acceptance/` is binary-verifiable.

---

#### C. TG-C: Humanized Command Samples (~6h)

##### C.1 Sample corpus collection

10 command samples are collected from the E2E run (TG-A 7d window). Each sample is a complete
autonomous command dispatched to a human developer, captured as markdown.

**Corpus structure** (committed to `aria-orchestrator/evals/m6-prompt-quality/`):

```
aria-orchestrator/evals/m6-prompt-quality/
├── rubric.md                    # PRD §639 rubric (7 dimensions, each 0-10, median scoring)
├── corpus/
│   ├── sample-01.md             # raw command as dispatched
│   ├── sample-02.md
│   ...
│   └── sample-10.md
├── score-01-owner.md            # owner scoring for sample 01
├── score-02-owner.md
...
└── score-10-owner.md
```

Each `sample-NN.md` contains:
- Dispatch ID (from `dispatches` table).
- Issue title and type (bug/feature/stale).
- Full command text as sent to developer (verbatim).
- State at dispatch time (which state transition triggered the command).
- `is_synthetic`: yes/no.

Each `score-NN-owner.md` contains:
- Sample reference: `sample-NN`.
- 7 rubric dimension scores (each integer 0-10).
- Median score (computed from 7 scores).
- Qualitative note (1-2 sentences; optional).

##### C.2 PRD §639 rubric

The rubric in `rubric.md` must codify 7 dimensions per PRD §639:

| Dim | Name | Scoring guidance |
|-----|------|-----------------|
| D1 | Naturalness | 0=robotic/template; 10=indistinguishable from skilled human |
| D2 | Specificity | 0=vague; 10=precise actionable steps with exact file/function refs |
| D3 | Tone appropriateness | 0=wrong tone for context; 10=matches request severity and relationship |
| D4 | Completeness | 0=missing required context; 10=all context a developer needs included |
| D5 | Conciseness | 0=verbose padding; 10=minimal words to convey full intent |
| D6 | Technical accuracy | 0=incorrect references; 10=all file/function/commit references correct |
| D7 | Autonomy footprint | 0=over-delegates; 10=appropriately scoped with no unnecessary asks |

**Median scoring**: median of the 7 dimension scores for a single sample. Pass threshold: ≥7.
<!-- R1-X-T3 fix: PRD §656 patched mean→median (commit e884e62, 2026-05-24) per Q4 lock.
     "median-of-medians" replaced with "median" (simpler; aligns with post-patch PRD §656).
     (R1 audit 2026-05-24) -->
**Corpus pass**: median of all 10 sample medians ≥7/10 (per post-patch PRD §656, 2026-05-24).

##### C.3 Cross-ref Spec #3 BOTH-locations design

<!-- Cross-ref Spec #3 TG-DOCS-B humanized-command-patterns.md -->
TG-C samples cross-reference Spec #3's `standards/autonomous/humanized-command-patterns.md` via
a BOTH-locations design:

- **This Spec (Spec #2)**: `aria-orchestrator/evals/m6-prompt-quality/corpus/` — raw scored
  corpus (10 samples + 10 score files + rubric). Aria-specific deployment context.
- **Spec #3 TG-DOCS-B**: `standards/autonomous/humanized-command-patterns.md` — curated
  ≥10 best samples from the corpus, rewritten as canonical patterns for Lab-wide reuse
  (anonymized of project-specific details). Spec #3 pulls from this corpus to populate patterns.

Each `sample-NN.md` in this Spec's corpus includes a footer link:
```markdown
---
*Cross-reference: [standards/autonomous/humanized-command-patterns.md](../../../../standards/autonomous/humanized-command-patterns.md)
(Spec #3 TG-DOCS-B, shipped separately)*
```

Spec #3 TG-DOCS-B `humanized-command-patterns.md` links back:
```markdown
*Source corpus: [aria-orchestrator/evals/m6-prompt-quality/](../../../aria-orchestrator/evals/m6-prompt-quality/)
(Spec #2 TG-C, M6 E2E run)*
```

This two-way linkage is verified by AC-5 (see §Acceptance criteria).

---

### Out of scope (explicit drops per DEC §3 and R3 decisions)

| ID | Description | Drop reason |
|----|-------------|-------------|
| OOS-1 | Real-time dashboard (PRD §352) | PRD §352: "M6 后考虑, MVP 不做"; zero MVP value at this stage |
| OOS-2 | Context-window overflow crash mode | Deferred to v2.1 per DEC R3 qa + ai consensus; non-deterministic reproduction cost too high |
| OOS-3 | Safety/content refusal crash mode | Deferred to v2.1 per DEC R3; provider-dependent behavior not suitable for mock-only regime |
| OOS-4 | Stochastic LLM live cost in tests (S2/S3/S6) | Replaced by mocked replay (zero live cost) per DEC R3 qa-R3 revision + ai R2CH-1 |
| OOS-5 | Cross-project E2E dispatch mandatory gate | Cross-project is conditional acceptance (P-9); not a hard PASS/FAIL gate for 7d window |
| OOS-6 | New Feishu webhook or nomad vars | No new secrets in this Spec; cost alarm path already wired by Spec #1 |
| OOS-7 | M5-OS-PB-1 carry-forward (comment_poll lazy-wire forgejo UX fix) | Owner Q6: "defer all carry-forward" — DROPPED per DEC consensus |
| OOS-8 | Aria-plugin bump | Semantic boundary: aria-plugin is tools; Aria 2.0 is autonomous infra. Spec #3 comms section covers this. |
| OOS-9 | FX adapter / cost trending extension | Spec #1's domain; this Spec only reads existing cost.json for Day-1 precondition check |

---

## Constraints

### REPO_ROOT canonical pattern

Any Python script in the `aria-orchestrator/` subtree must resolve paths using the canonical pattern
(mirrors `aria-orchestrator/docs/validate-m5-handoff.py:40-41` line-for-line; discovered and
documented via Spec #1 R2-C-tl-N1):

```python
HERE = Path(__file__).resolve().parent      # → the script's own directory
REPO_ROOT = HERE.parent                     # → aria-orchestrator/  (NOT main repo root /home/dev/Aria/)
```

For scripts in `aria-orchestrator/acceptance/` (e.g., `check-m6-e2e-acceptance.py`):
- `__file__` resolves to `aria-orchestrator/acceptance/<script>.py`
- `HERE` = `aria-orchestrator/acceptance/`
- `REPO_ROOT` = `aria-orchestrator/`

For scripts in `aria-orchestrator/docs/` (e.g., `validate-m6-handoff.py`):
- `HERE` = `aria-orchestrator/docs/`
- `REPO_ROOT` = `aria-orchestrator/`

**Do NOT use `.parent.parent` from `aria-orchestrator/acceptance/` — that would resolve to
`/home/dev/` (main repo parent), not to `aria-orchestrator/`.** The single `.parent` from the
script file always yields `aria-orchestrator/` regardless of whether the script is in `docs/`,
`acceptance/`, or `tests/`.

### Schema column SoT

The `dispatches` table column is `provider_cost_model TEXT` with enum
`'subscription_flat'|'metered'`. There is NO `provider` column. Any SQL in this Spec that filters
by provider type must use `WHERE provider_cost_model = '<value>'` (not `WHERE provider = '<value>'`).
This SoT was established in Spec #1 R1-C1 and applies to all TG-A SQL queries in this Spec.

### abi_compat hard constraints

<!-- R1-T2-4 fix: Migration renamed from 005 to 006 (migration 005 already exists in schema v4.2
     per Spec Y T0 — Spec X migration 005 drops inline UNIQUE constraint via table rebuild).
     Migration 006 targets schema v5.0. (R1 audit 2026-05-24) -->
The `is_synthetic` column addition (Mechanism A, §A.2, **locked** per R1 T2-4) must be implemented
as additive migration `006_schema_v5_add_is_synthetic.sql`:
```sql
ALTER TABLE dispatches ADD COLUMN is_synthetic INTEGER DEFAULT 0;
```
This migration must NOT drop the `audit_no_update` or `audit_no_delete` triggers (abi_compat
promise #1 from m5-handoff.yaml). The TG-A paired test triple (§A.7) verifies this. The migration
targets schema version 5.0 — `schema_meta` `schema_version` must be updated to `'5.0'`
(per `[[feedback_schema_migration_to_version_bump]]` to avoid no-op silent skip).

### Mock-shape discipline

Per `[[feedback_test_mock_pattern_hides_prod_bug]]` and `[[feedback_mock_layer_per_failure_semantic]]`:
tests must not mock at a layer that is higher than the actual failure point. The mock-layer-per-mode
matrix in §B.1 is authoritative. Deviation from the matrix requires an explicit comment
`# mock-layer-deviation-ok: <reason>` in the test file.

### Platform

Implementation target: Linux only (Nomad alloc running Python 3.9+ per aria-layer1 container image).
macOS/Windows compatibility not required. POSIX `os.rename()` atomicity assumed for any file writes.

---

## How

### Technical approach

```
TG-A Runtime Observability:
  Spec #1 AC-7 PASS (3-day history)
      │
      │ gate: --check-3-day-history exit 0
      ▼
  Pre-flight × 3 dispatches (real LLM, ≤$2/ea)  → .aria/probes/m6-preflight-log.md
      │
      │ pre-flight PASS (all 3 reach S9 or S_FAIL within 8h)
      ▼
  7-day E2E run starts (Day-1)
      │ daily probes → .aria/probes/m6-7d-day-{1..7}.md
      ├── Day-3 health gate (≥1 S0→S9, ≤50% S_FAIL, no stuck >4h)
      └── Day-7 final
      │
      ▼
  check-m6-e2e-acceptance.py --tg-a
      │ alloc uptime ≥168h
      │ dispatch ≥10 stratified (≥1 bug/feature/stale, ≤70% synthetic)
      │ Day-3 gate PASS
      └─→ PASS/FAIL

TG-B Crash Recovery (parallel, no dependency on 7d run completion):
  6-mode mock suite (4 SDK + 2 HTTP)
      │ AdvancingClock DI for time-based transitions
      │ WAL × 4 scenarios (WAL-A/B/C/D) + acceptance/m6-wal-fault.sh
      │ State machine 100% det cov + stochastic mocked replay
      └─→ pytest --cov=aria_layer1.extension,aria_layer1.comment_poll,aria_layer1.reconciler,aria_layer1.tick_runner
          --cov-fail-under=100 (Q1 lock: 4-module cov target; no state_machine.py)
          Note (I2-7): `--cov-fail-under=100` must also be declared in
          `aria-orchestrator/pyproject.toml` `[tool.pytest.ini_options] addopts` to enforce
          in CI (not just local runs)

TG-C Humanized Samples (sequential after TG-A 7d run):
  10 samples from E2E run
      │ owner scores each via rubric.md (7 dims × 10 samples)
      │ median per sample computed
      └─→ median(all 10 medians) ≥ 7/10
      │ cross-ref Spec #3 TG-DOCS-B BOTH-locations
      └─→ AC-5 cross-ref link verification
```

### Key design decisions (AD-M6-4..AD-M6-6)

| ID | Topic | Decision |
|----|-------|----------|
| AD-M6-4 | is_synthetic tagging mechanism | **LOCKED to Mechanism A** (R1 audit 2026-05-24). Mechanism B (title prefix) was removed: `dispatches.title` column does not exist in live schema. Migration 006 adds `is_synthetic INTEGER DEFAULT 0` (additive, schema v5.0). See T-schema-1 in TG-A-infra. |
| AD-M6-5 | Pre-flight fixture provenance (Option A replay vs Option B fresh synthetic vs Option C cross-project) | **Deferred to Phase B kickoff**. Check whether `aria-orchestrator/docs/demo-m5-o3-*.yaml` capture files exist from M5. If yes, prefer Option A (regression continuity). Document in `.aria/probes/m6-preflight-provenance.md`. |
| AD-M6-6 | AdvancingClock DI injection point | Clock parameter injected at handler class constructor level (e.g., `AriaExtension(clock=FakeClock(...))`) rather than per-method. State machine logic is distributed across 4 modules (extension.py, comment_poll.py, reconciler.py, tick_runner.py — per Q1 lock 2026-05-24; no `state_machine.py`). All time-sensitive internal methods in those 4 modules read `self._clock.now()` instead of `datetime.now()`. |

---

## Acceptance criteria

All criteria are binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`.
No subjective language. Each criterion cites the concrete verifiable evidence.

Exit code contract (consistent with Spec #1 AC-9):
- `exit 0` — all sub-checks PASS.
- `exit 1` — one or more AC sub-checks FAIL (data condition: thresholds not met, files wrong count, scores below rubric).
- `exit 2` — infrastructure error that prevents evaluation (required file missing, corrupt JSON, DB unavailable).

### AC-1 — 7-day uptime and probe files complete

<!-- R1-T2-5 fix: AC-1 evidence rewritten to use alloc.CreateTime (alloc-level, does not
     reset on task restart) + persisted Day-1 anchor file. TaskStates['aria-layer1']['StartedAt']
     was removed — it resets on task restart, causing false-FAIL on legitimate 168h alloc.
     (R1 audit 2026-05-24) -->

**Evidence**:

```bash
python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --tg-a --check-uptime
```

- Exit code 0.
- stdout contains `[PASS] AC-1: alloc uptime >= 168h (actual: <N>h, alloc_id=<id>)`.
- Acceptance script logic:
  1. Read persisted `m6-7d-day-1-alloc-anchor.json` (`alloc_id`, `create_time_ns`). Exit 2 if absent.
  2. Query current alloc: `nomad alloc status <alloc_id> -json | jq '.ID, .CreateTime'`.
  3. If `current_id != anchored_alloc_id` → `[FAIL] AC-1: alloc replaced (original=<id>, current=<id>)`. Exit 1.
  4. Compute `age_s = (now_utc_ns - create_time_ns) / 1e9`. If `age_s >= 604800` → PASS.
- All 7 probe files exist:
  ```bash
  for i in 1 2 3 4 5 6 7; do
    test -f ".aria/probes/m6-7d-day-${i}.md" || echo "MISSING day-${i}"
  done
  # must produce no output
  ```
<!-- R1-I2-1 fix: Day-3 gate check all 3 conditions individually, not just verdict line.
     Previous version only greps for "PASS" verdict — a Day-3 file with 2/3 passing and
     a manually-edited "PASS" would slip through. (R1 audit 2026-05-24) -->
- Day-3 probe file contains all 3 individual gate condition lines AND verdict:
  ```bash
  # Check all 3 conditions individually (not just verdict)
  grep -q "≥1 complete S0→S9 cycle: YES" .aria/probes/m6-7d-day-3.md \
    || echo "[FAIL] AC-1: Day-3 condition 1 missing or NO"
  grep -q "S_FAIL rate ≤50%: YES" .aria/probes/m6-7d-day-3.md \
    || echo "[FAIL] AC-1: Day-3 condition 2 missing or NO"
  grep -q "No stuck >4h: YES" .aria/probes/m6-7d-day-3.md \
    || echo "[FAIL] AC-1: Day-3 condition 3 missing or NO"
  grep -q "Day-3 gate verdict: PASS" .aria/probes/m6-7d-day-3.md \
    || echo "[FAIL] AC-1: Day-3 gate verdict not PASS"
  # All 4 greps must produce no output
  ```
- Day-1 probe file contains `m6-7d-day-1-alloc-anchor.json` alloc anchor data.

Non-zero exit or `MISSING` output for any day file → AC-1 FAIL.

### AC-2 — Dispatch stratification ≥10 with cap and cross-project evidence

<!-- R1-T2-1 fix: SQL columns rewritten — `final_state`/`created_at`/`issue_type`/`project_name`
     do not exist in live dispatches schema. Use `state='S9_CLOSE'`, `state_entered_at`,
     and `dispatch_audit_log` json_extract for issue metadata. (R1 audit 2026-05-24) -->
<!-- R1-T2-6 fix: Check order corrected — `assert total >= 10` runs FIRST before any division
     to prevent ZeroDivisionError. Synthetic cap division guarded with `if total_s9 > 0`.
     (R1 audit 2026-05-24) -->

**Evidence**:

```python
# Binary-falsifiable SQL gate
import sqlite3, sys
conn = sqlite3.connect('aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/aria_layer1.db')
cur = conn.cursor()

# STEP 1 (FIRST): Total S9_CLOSE dispatches in 7d window — assert before any division
cur.execute("""
    SELECT COUNT(*) FROM dispatches
    WHERE state = 'S9_CLOSE'
    AND state_entered_at BETWEEN :start AND :end
""", {"start": run_start_iso, "end": run_end_iso})
total_s9 = cur.fetchone()[0]
if total_s9 < 10:
    print(f"[FAIL] AC-2: total S9_CLOSE dispatches {total_s9} < 10")
    sys.exit(1)

# STEP 2: Synthetic cap (guarded against ZeroDivisionError)
cur.execute("""
    SELECT SUM(CASE WHEN is_synthetic=1 THEN 1 ELSE 0 END),
           COUNT(*)
    FROM dispatches
    WHERE state='S9_CLOSE' AND state_entered_at BETWEEN :start AND :end
""", {"start": run_start_iso, "end": run_end_iso})
synth_count, total2 = cur.fetchone()
synth_ratio = synth_count / total_s9 if total_s9 > 0 else 0.0
if synth_ratio > 0.70:
    print(f"[FAIL] AC-2: synthetic ratio {synth_count}/{total_s9} = {synth_ratio:.1%} > 70%")
    sys.exit(1)

# STEP 3: Per-type stratification via dispatch_audit_log json_extract
# Note: issue_type is stored in dispatch_audit_log payload_json (not a dispatches column).
# The exact json_extract key must be verified at Phase B against live data (see §A.2 T-validate-schema-1).
for type_hint in ('bug', 'feature', 'stale'):
    cur.execute("""
        SELECT COUNT(DISTINCT d.dispatch_id)
        FROM dispatches d
        JOIN dispatch_audit_log al ON al.dispatch_id = d.dispatch_id
        WHERE d.state = 'S9_CLOSE'
        AND d.state_entered_at BETWEEN :start AND :end
        AND json_extract(al.payload_json, '$.issue_type_hint') = :type_hint
    """, {"start": run_start_iso, "end": run_end_iso, "type_hint": type_hint})
    n = cur.fetchone()[0]
    if n < 1:
        print(f"[FAIL] AC-2: no completed {type_hint} dispatch in 7d window")
        sys.exit(1)

print("[PASS] AC-2")
```

Must print `[PASS] AC-2` without assertion errors.

### AC-3 — 6 crash modes all PASS

**Evidence**:

```bash
pytest aria-orchestrator/tests/test_crash_infra1.py \
       aria-orchestrator/tests/test_crash_infra2.py \
       aria-orchestrator/tests/test_crash_infra3_wal.py \
       aria-orchestrator/tests/test_crash_llm4.py \
       aria-orchestrator/tests/test_crash_llm5.py \
       aria-orchestrator/tests/test_crash_llm6.py \
  -v --tb=short
```

- Exit code 0 (all 6 test files pass).
- Each test file must contain ≥1 test for its crash mode.
- `test_crash_infra3_wal.py` must contain exactly 4 test functions (one per WAL scenario WAL-A/B/C/D per P-5).

Additionally, the WAL fault injection shell script exists and is executable:

```bash
test -x aria-orchestrator/acceptance/m6-wal-fault.sh && echo "PASS" || echo "FAIL AC-3: m6-wal-fault.sh missing or not executable"
```

Must print `PASS`.

### AC-4 — State machine deterministic transition 100% coverage

<!-- R1-T2-2 fix: `aria_layer1/state_machine.py` does not exist; cov target updated to 4-module
     list per Q1 lock (2026-05-24). State machine logic distributed across extension.py,
     comment_poll.py, reconciler.py, tick_runner.py. No new file extracted. (R1 audit 2026-05-24) -->

**Evidence**:

```bash
pytest aria-orchestrator/tests/test_state_machine_deterministic.py \
       aria-orchestrator/tests/test_state_machine_stochastic_replay.py \
  --cov=aria_layer1.extension,aria_layer1.comment_poll,aria_layer1.reconciler,aria_layer1.tick_runner \
  --cov-report=term-missing \
  --cov-fail-under=100
```

- Exit code 0.
- Coverage report shows 100% line + branch coverage for the 4-module state machine coverage
  target (`extension`, `comment_poll`, `reconciler`, `tick_runner`) — deterministic transition
  paths. Note: state machine logic distributed across 4 modules per M5 design; no
  `aria_layer1.state_machine` module exists (AD-M6-? not needed; Q1 lock 2026-05-24).
- `test_state_machine_stochastic_replay.py` uses committed fixture files only (zero live calls);
  confirmed by: `grep -r "call_llm\|call_with_routing\|provider_router" aria-orchestrator/tests/test_state_machine_stochastic_replay.py | grep -v "mock\|patch\|MagicMock"`
  returns no output (no live LLM calls in stochastic replay tests).

### AC-5 — Humanized samples: 10 files, median ≥7/10, cross-ref links present

<!-- R1-X-T3 fix: PRD §656 (line 656 post e884e62 patch) uses "median" not "mean".
     AC-5 evidence updated to use `statistics.median([...])` directly (not median-of-medians
     description). Q4 lock 2026-05-24: median is more robust for bimodal score distributions
     + Lab industry convention. (R1 audit 2026-05-24) -->

**Evidence**:

```bash
python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --tg-c
```

- Exit code 0.
- stdout contains `[PASS] AC-5: 10 samples scored, median=<N.N> >= 7.0`.
- Median computation: `statistics.median([float(s) for s in all_10_sample_medians]) >= 7.0`
  (per post-patch PRD §656 line 656).
- File count verification:
  ```bash
  ls aria-orchestrator/evals/m6-prompt-quality/corpus/sample-*.md | wc -l
  # must output 10
  ls aria-orchestrator/evals/m6-prompt-quality/score-*-owner.md | wc -l
  # must output 10
  test -f aria-orchestrator/evals/m6-prompt-quality/rubric.md && echo "PASS" || echo "FAIL"
  ```
- Cross-ref link verification:
  ```bash
  grep -l "humanized-command-patterns.md" aria-orchestrator/evals/m6-prompt-quality/corpus/sample-*.md \
    | wc -l
  # must output 10 (all samples contain cross-ref link)
  ```
  Must output `10`.

### AC-6 — Pre-flight log committed with ≤$2/dispatch evidence

<!-- R1-T2-3 fix: `assert all(c <= 2.0)` was a Luxeno=0 paper-fix re-introduction — Luxeno
     (current routing for Layer 1) returns cost_usd=0.0 for every call under subscription
     billing, so the cap assertion trivially passes. Same trap as Spec #1 R1-C2.
     Fix: add structural floor (non-null guard + bounded zeros). AD slot added for pre-flight
     routing strategy decision (Luxeno zero-cost vs Zhipu metered path).
     (R1 audit 2026-05-24) -->

**Pre-flight routing strategy (AD-M6-4b — new AD slot)**:
The 3 pre-flight dispatches route through Luxeno (Layer 1 subscription, `cost_usd=0.0` per-dispatch
attribution) unless the implementer explicitly overrides `provider_router` to force Zhipu (metered,
non-zero cost). AD-M6-4b decision: **default = accept Luxeno null semantic** with bounded-zeros
guard in acceptance check (zero-cost entries are valid but bounded to ≤3 of 3). If metered cost
evidence is required for pre-flight, Phase B implementer overrides routing to Zhipu for 3 pre-flight
dispatches and documents in AD-M6-4b.

**Evidence**:

```bash
test -f .aria/probes/m6-preflight-log.md && echo "PASS" || echo "FAIL AC-6: preflight log missing"
python3 -c "
import re, sys
content = open('.aria/probes/m6-preflight-log.md').read()
costs = [float(m) for m in re.findall(r'cost_usd:\s*([\d.]+)', content)]

# Structural floor: non-null guard (cost entries must be present, not None/missing)
assert len(costs) == 3, f'[FAIL] AC-6: expected 3 cost_usd entries, found {len(costs)}'
assert all(c is not None for c in costs), f'[FAIL] AC-6: null cost_usd entry (suppressed cost)'

# Hard cap: per-dispatch ≤\$2.00
if not all(c <= 2.0 for c in costs):
    print(f'[FAIL] AC-6: dispatch exceeds \$2 hard cap: {costs}')
    sys.exit(1)

# Bounded-zeros: Luxeno subscription billing returns 0.0 legitimately,
# but >3 zero-cost entries would indicate a parsing failure, not real data.
zero_count = sum(c == 0.0 for c in costs)
if zero_count > 3:
    print(f'[FAIL] AC-6: {zero_count} zero-cost entries > expected max 3 (parse error?)')
    sys.exit(1)

# Inform about zero-cost path (Luxeno subscription; not a failure)
if zero_count > 0:
    print(f'[INFO] AC-6: {zero_count}/3 dispatches show cost_usd=0.0 (Luxeno subscription billing; see AD-M6-4b)')

print('[PASS] AC-6')
"
```

Must print `[PASS] AC-6`. All 3 pre-flight dispatches must show `cost_usd <= 2.0` in the log.
Zero-cost entries are acceptable (Luxeno subscription) but must be bounded (≤3 of 3).

### AC-7 — abi_compat promises not violated by TG-A migrations

**Evidence**:

```bash
python3 aria-orchestrator/docs/validate-m6-handoff.py --check-abi-compat
```

- Exit code 0.
- stdout contains all 5 promise IDs without any `FAIL` line.
- This check must pass AFTER any `is_synthetic` migration (005) is applied.

---

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-M6-7 | 7-day run produces < 10 completed S9 dispatches due to low organic Lab issue volume | Medium | Synthetic cap allows up to 7/10 synthetic dispatches; pre-flight confirms dispatch pipeline is operational before clock starts |
| R-M6-8 | Day-3 health gate FAIL (S_FAIL rate >50%) requires 7-day restart, consuming 3 additional days | Medium | Pre-flight (§A.5) de-risks by confirming end-to-end dispatch health; Day-3 gate catch is preferable to a full 7d run with silent failures |
| R-M6-9 | Mock-shape mismatch in SDK-layer crash tests hides real production bug | Medium | Per `[[feedback_test_mock_pattern_hides_prod_bug]]`: validate mock exception class against production code path; matrix in §B.1 mandates exact exception class for each mode |
| R-M6-10 | WAL-D scenario (WAL file deleted) behaviour varies by SQLite version or journal mode | Low | Test uses a fresh `tmpdir` SQLite DB created in WAL mode; documents observed behavior in test docstring; assert no data corruption rather than specific error type |
| R-M6-11 | TG-C sample quality < median 7/10 requires re-run or supplemental dispatches | Medium | Acceptance only after TG-A 7d completes; if median < 7, owner can dispatch additional targeted runs (synthetic, ≤70% cap still applies) to top up corpus; rubric dimensions D1-D7 are independently scoreable — individual low scores addressable |
| R-M6-12 | Spec #1 3-day history gate blocks TG-A start if owner forgets daily cron | Low | Spec #2 Day-1 probe explicitly checks `validate-m6-handoff.py --check-3-day-history` as first step; documented in Phase B.1 checklist |
| R-M6-13 | is_synthetic column migration (Mechanism A) conflicts with in-flight M6 Spec #1 schema work | Low | Spec #1 is additive (reads existing columns, writes JSON artifact); migration 005 adds only new column with `DEFAULT 0`; verify no Spec #1 migration is pending before running 005 |
| R-M6-14 | AdvancingClock DI injection requires refactor across 4 state machine modules | Medium | AD-M6-6 decision: clock injected at constructor level of each handler class. Phase B implementer must audit all `datetime.now()` calls in `extension.py`, `comment_poll.py`, `reconciler.py`, `tick_runner.py` and replace with `self._clock.now()`; existing tests may need update to pass `FakeClock` (no `state_machine.py` — Q1 lock) |
| R-M6-15 | Spec #2 body propagation gap: P-4..P-9 precision items not carried through to tasks.md | Low | Per `[[feedback_spec_v2_body_propagation_2pass]]`: each precision item is cross-referenced to both §What sections and tasks.md task numbers in the Precision items cross-reference table |

---

## Effort baseline

```
TG-A: Runtime Observability
  A.1  Nomad alloc uptime gate + acceptance script stub          ~1h
  A.2  Dispatch tracker SQL + stratification query               ~2h
  A.3  Daily probe snapshot template + cron/manual script        ~1h
  A.4  Day-3 health gate logic (threaded into probe + acceptance)~0.5h
  A.5  Pre-flight dry-run script + provenance log                ~1.5h
  A.6  Cross-project conditional acceptance (acceptance only)    ~0.5h
  A.7  validate-m6-handoff.py paired test triple                 ~1h
  A.docs AD-M6-4/5/4b slots + is_synthetic migration 006 (locked Mech A) ~0.5h
  A.schema-validate T-validate-schema-1 (schema drift guard test)  ~0.5h
  A.tg-a-acceptance check-m6-e2e-acceptance.py --tg-a section   ~1h
TG-A subtotal                                                    ~10-10.5h

TG-B: Crash Recovery
  B.1  6-mode crash test suite scaffold + mock-layer matrix doc  ~2h
  B.1a Infra-1 (Hermes SIGKILL, SDK, reuse test_t12)            ~1h
  B.1b Infra-2 (Layer 2 alloc SIGKILL, SDK, light-1 reframe)    ~1h
  B.1c Infra-3 (WAL × 4 scenarios, SDK + m6-wal-fault.sh)       ~2h  (+1h P-5 4-scenario vs 3)
  B.1d LLM-4 (429 rate-limit, SDK)                              ~0.5h
  B.1e LLM-5 (invalid JSON, httpx_mock)                         ~0.5h
  B.1f LLM-6 (provider 5xx, httpx_mock)                         ~0.5h
  B.2  State machine det 100% cov + stochastic mocked replay     ~2.5h
  B.3  AdvancingClock DI refactor + FakeClock class              ~1.5h
  B.4  Mock-layer-per-mode rationale doc (Q-NEW-1 +1h)           ~1h
TG-B subtotal                                                    ~12.5-13h

TG-C: Humanized Samples
  C.1  Corpus structure + rubric.md (7 dims) setup               ~1h
  C.2  10 sample files collection from E2E run (owner-driven)    ~2h
  C.3  10 score files (owner scoring)                            ~1.5h
  C.4  Acceptance script --tg-c section                          ~0.5h
  C.5  Cross-ref BOTH-locations link verification                ~0.5h
  C.6  Median score computation + AC-5 check                     ~0.5h
TG-C subtotal                                                    ~6h

──────────────────────────────────────────────────────────────────────
Total (AI-implementable)                                         ~29-30h ≈ 30h
```

Phase A audit overhead ~1h is tracked separately (not impl).

Q-NEW-1 delta: +1h for hybrid mock layer rationale documentation and per-mode matrix in TG-B.
R1-fix delta: +0.5h T-validate-schema-1 schema drift guard + migration 006 (T2-1/T2-4 fixes);
+0.5h AC-6 AD-M6-4b pre-flight routing strategy AD slot (T2-3 fix). Total ~30h (vs 29h baseline).

Owner manual actions (post-ship, not in B.2):
- Fill `.aria/probes/m6-7d-day-{1..7}.md` probe files daily during 7d run.
- Score `score-{01..10}-owner.md` files after TG-A completes.
- Confirm pre-flight fixture provenance in `.aria/probes/m6-preflight-provenance.md`.

---

## Dependencies

| Dependency | Direction | Notes |
|------------|-----------|-------|
| Spec #1 `aria-2.0-m6-cost-acceptance` AC-7 (3-day rolling history PASS) | Upstream (hard gate) | Spec #2 Phase B MUST NOT start until `validate-m6-handoff.py --check-3-day-history` exits 0; Spec #1 commit `c29a800` Approved |
<!-- R1-T2-1 fix: Column list corrected — `final_state` and `issue_type` do not exist. Terminal
     state is `state='S9_CLOSE'`; issue metadata is in dispatch_audit_log.payload_json.
     Migration 006 (not "optional") adds `is_synthetic` column. (R1 audit 2026-05-24) -->
| M5 dispatches table (`token_cost_usd`, `provider_cost_model`, `state`, `state_entered_at`) | Upstream (already shipped M2+) | All SQL queries in TG-A read existing M5 columns; migration 006 adds `is_synthetic` (additive, schema v5.0, AD-M6-4 locked to Mechanism A) |
| `aria-orchestrator/docs/validate-m6-handoff.py` | Upstream (Spec #1 deliverable) | TG-A paired test triple (§A.7) tests this script; must be shipped by Spec #1 before TG-A Phase B completes |
| DEMO-M5-O3 capture files (optional) | Upstream (conditional) | `aria-orchestrator/docs/demo-m5-o3-*.yaml` used for pre-flight Option A (P-8); if absent, fall back to Option B |
| `aria-runner-bot` PAT scopes | Upstream | Cross-project dispatch (P-9) requires existing PAT scopes sufficient; no new PAT creation in this Spec |
| Spec #3 TG-DOCS-B `standards/autonomous/humanized-command-patterns.md` | Downstream cross-ref (BOTH-locations) | Spec #3 pulls from this Spec's `evals/m6-prompt-quality/corpus/`; shipping Spec #2 TG-C before Spec #3 TG-DOCS-B is preferred (provides source corpus) but not strictly blocking |
| Spec #4 `aria-2.0-m6-release-closeout` | Downstream (gates on this Spec) | Spec #4 RED/ABORT gate consumes: 7d uptime evidence (AC-1) + 6 crash mode PASS (AC-3) + median ≥7/10 (AC-5) |

---

## Cross-references

**Predecessors**:
- [openspec/archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/) — M5 shipped; abi_compat promises source
- [aria-orchestrator/docs/m5-handoff.yaml](../../../aria-orchestrator/docs/m5-handoff.yaml) line 151-172 — 5 forward-binding abi_compat promises

**Sibling Specs (M6 parallel)**:
- [aria-2.0-m6-cost-acceptance](../aria-2.0-m6-cost-acceptance/proposal.md) — **Approved 2026-05-24 commit `c29a800`**; gates this Spec via 3-day history precondition (Spec #1 AC-7)
- [aria-2.0-m6-docs](../aria-2.0-m6-docs/proposal.md) — parallel; Spec #3 TG-DOCS-B consumes TG-C corpus from this Spec (BOTH-locations design)
- [aria-2.0-m6-release-closeout](../aria-2.0-m6-release-closeout/proposal.md) — sequential after all M6 Specs done; consumes AC-1 + AC-3 + AC-5 as pre-release gates

**Decisions**:
- [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) — DEC-20260524-001 §2 Spec #2 scope (source-of-truth); §4 P-4..P-9; §5 R3 final positions
- [.aria/decisions/2026-05-15-m6-brainstorm.md](../../../.aria/decisions/2026-05-15-m6-brainstorm.md) — M6a brainstorm D1-D7 (predecessor context)

**PRD references**:
- [docs/requirements/prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) line 637-656 — E2E resilience requirements (7d uptime, crash modes, humanized commands; post-patch a786444 + e884e62)
- PRD line 648-651 — WAL crash mode enumeration (4 sub-clauses, P-5)
- PRD line 656 — humanized command rubric (median ≥7/10; post-patch e884e62 Q4 lock 2026-05-24 — median replaces "平均"/mean)

**Memory entries woven**:
- `[[feedback_phase_b_velocity_patterns_2026-04-29]]` — AdvancingClock DI in §B.3 + AD-M6-6
- `[[feedback_mock_layer_per_failure_semantic]]` — Q-NEW-1 hybrid rationale matrix in §B.1
- `[[feedback_test_mock_pattern_hides_prod_bug]]` — mock-shape discipline in §B.1 + R-M6-9
- `[[feedback_smoke_dispatch_sql_inject_pattern]]` — synthetic dispatch SQL inject pattern in §A.2
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — all ACs cite concrete evidence
- `[[feedback_spec_v2_body_propagation_2pass]]` — P-4..P-9 threaded into both §What and tasks.md
- `[[project_glm_routing_luxeno]]` — Luxeno (Layer 1) vs Zhipu (Layer 2) routing context for TG-A
- `[[feedback_pat_scope_canonical_from_codebase_grep]]` — cross-project PAT scope check in P-9
