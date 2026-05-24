# Aria 2.0 M6 Spec #2 — E2E Resilience (runtime observability + crash recovery + humanized samples)

> **Level**: 3 (Full — cross-cuts runtime observability + crash recovery + humanized command samples; three internal task groups)
> **Status**: Draft
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
>   - Phase A.2 R1 pending (post_spec 4-agent parallel audit)
>   <!-- R1 audit aggregate to be inserted here after Phase A.2 -->

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

The 7-day E2E run requires the `aria-layer1` Nomad allocation to remain up for 168 continuous
hours (per qa M-qa-R3 acceptance). The uptime check queries the Nomad Alloc API:

```bash
nomad alloc status <ALLOC_ID> -json \
  | jq '.TaskStates["aria-layer1"].StartedAt' \
  2>/dev/null
```

The `StartedAt` timestamp from the Nomad API response is compared against `datetime.now(timezone.utc)`.
Uptime >= 168h (604800 seconds) is the PASS condition. This is an owner-manual check (owner records
alloc ID in `.aria/probes/m6-alloc-id.txt` at Day-1); the acceptance script reads it for final
verification.

##### A.2 Dispatch tracker with path stratification

A SQL query verifies that ≥10 dispatches completed the full S0→S9 path with required stratification:

```sql
-- Stratification gate: ≥10 dispatches, ≥1 per required category
SELECT
    issue_type,
    SUM(1) as count
FROM dispatches
WHERE
    final_state = 'S9'
    AND created_at BETWEEN :run_start AND :run_end
    AND is_synthetic IN (0, 1)   -- include both real and synthetic
GROUP BY issue_type
HAVING SUM(1) >= 1;
-- Required: results contain ≥1 row with issue_type='bug',
--           ≥1 with issue_type='feature', ≥1 with issue_type='stale'
-- AND total COUNT(*) across all rows >= 10
```

<!-- P-7 thread: is_synthetic tagging mechanism -->
**is_synthetic tagging (P-7)**: Dispatches tagged as synthetic use one of two mechanisms (owner
chooses at Phase B based on schema column availability):

- **Mechanism A — Schema column**: `is_synthetic INTEGER NOT NULL DEFAULT 0` column on the
  `dispatches` table. Value `1` = synthetic fixture dispatch; value `0` = real issue dispatch.
  If this column does not already exist, a new migration `005_m6_synthetic_tag.sql` adds it
  (additive, backward-compatible: `ALTER TABLE dispatches ADD COLUMN is_synthetic INTEGER NOT NULL DEFAULT 0`).
- **Mechanism B — Title prefix convention**: If schema migration is deferred, synthetic dispatches
  use the `[DEMO-M6-*]` title prefix (e.g. `[DEMO-M6-001]`). The acceptance SQL query detects
  synthetic status via `CASE WHEN title LIKE '[DEMO-M6-%]' THEN 1 ELSE 0 END`.

The Phase B implementer documents which mechanism was chosen in AD-M6-4. Both mechanisms are
mutually exclusive (no mixing within the same 7d run).

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

The validate-m6-handoff.py script (Spec #1, already shipped) must have a **paired test triple**
(per backend M-ba-R3-1c): 3 unit tests that verify the abi_compat promises are still honoured
after any TG-A schema migration (particularly the `is_synthetic` column addition):

- Test 1: schema.sql still contains `audit_no_update` and `audit_no_delete` after migration 005.
- Test 2: migration 005 (if written) does NOT contain `DROP TRIGGER`.
- Test 3: `validate-m6-handoff.py --check-abi-compat` still exits 0 after 005 applied to a
  test database.

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
| LLM 429 rate-limit | LLM-4 | Rate limit response mid-transition (S2/S3/S6 LLM call) | SDK boundary (`llm_client.complete()` raises `RateLimitError` with `retry_after=30`) | 429 is returned by provider before HTTP body; SDK exception is the correct abstraction; avoids httpx_mock coupling to specific 429 body format |
| Invalid JSON response | LLM-5 | Malformed HTTP response body (non-JSON or truncated JSON) | HTTP layer (`httpx_mock` returns status=200, body=`"{ bad json"`) | Invalid JSON arrives as valid HTTP; SDK would normally parse the body; httpx_mock at transport layer correctly exercises the JSON parse failure path in the SDK adapter |
| Provider 5xx | LLM-6 | Provider server error mid-transition | HTTP layer (`httpx_mock` returns status=503, body=`{"error":"service_unavailable"}`) | 5xx response is an HTTP-level failure; httpx_mock at transport layer matches actual failure semantics; SDK converts 5xx to `ProviderUnavailableError` |

**Mock-shape discipline (per `[[feedback_test_mock_pattern_hides_prod_bug]]`)**: Each mock must
reproduce the exact exception class and attribute shape that production code raises. For SDK-layer
mocks, use the actual exception classes from the production code path (`ProcessKilledError`,
`AllocTerminatedError`, `sqlite3.DatabaseError`, `RateLimitError`). Do not substitute `Exception`
or generic `RuntimeError` — mock-shape mismatch at SDK boundary hides real bugs.

For HTTP-layer mocks (LLM-5, LLM-6), `httpx_mock` must match the exact HTTP method + URL pattern
used by the SDK adapter under test. Validate mock fixture shape against one real captured response
to confirm the SDK parses the mock body through the same code path as a real response.

##### B.2 WAL truncation scenario enumeration (P-5)

<!-- P-5: 4 WAL scenarios vs 3 -->
PRD §634 sub-clauses enumerate **4 WAL truncation scenarios** (not 3 as initially counted in R2).
The test suite must cover all 4:

| Scenario | ID | Description | Expected outcome |
|----------|----|-------------|-----------------|
| WAL truncated to 0 bytes pre-checkpoint | WAL-A | WAL file exists but is 0 bytes when connection opens | `sqlite3.DatabaseError` on first execute; state machine transitions to S_FAIL; recovery path triggers `integrity_check` PRAGMA |
| WAL truncated to 0 bytes mid-checkpoint | WAL-B | WAL file zeroed during an active checkpoint operation | `sqlite3.OperationalError: database is locked` or `DatabaseError`; same recovery path |
| WAL corrupted (non-zero, non-valid bytes) | WAL-C | WAL file contains garbage bytes (not zero-length) | `sqlite3.DatabaseError: database disk image is malformed`; same recovery path |
| WAL file deleted entirely | WAL-D | WAL file missing (not truncated, fully removed) | SQLite reopens WAL-mode DB without WAL; behaviour depends on SQLite WAL mode; test asserts no data corruption visible to subsequent clean connection |

All 4 WAL scenarios are tested via SDK-boundary mock (monkey-patch `sqlite3.connect()` to simulate
each error type). WAL-D uses `tmpdir` fixture with WAL file deleted before connection attempt.
Each scenario must assert: (a) state machine transitions to S_FAIL (not crash without state write),
(b) `PRAGMA integrity_check` is invoked in the recovery handler, (c) a structured error log entry
is written with `{"event": "wal_fault", "scenario": "<WAL-A|B|C|D>", "recovery": "s_fail_set"}`.

##### B.3 State machine deterministic transition coverage

State machine 100% coverage targets deterministic transitions only. Stochastic states (S2/S3/S6)
have separate sub-tasks using mocked replay (zero live cost).

**Deterministic transition states**: S0 (initial), S1 (issue claimed), S4 (PR submitted), S5
(review received), S7 (human gate), S8 (approved), S9 (merged/done), S_FAIL (terminal failure).

For each deterministic state, the test suite must cover:
- Normal outbound transition (e.g., S0 → S1 on issue claim).
- Failure-injected outbound transition (e.g., S0 → S_FAIL when Infra-2 SIGKILL during claim).
- Re-entry idempotency (e.g., S1 entered twice — second entry is a no-op, not a double-claim).

**Stochastic states (S2/S3/S6) — mocked replay sub-task**: Mocked replay uses captured LLM
response fixtures (committed to `aria-orchestrator/tests/fixtures/state_machine/`) to simulate
the S2/S3/S6 transitions deterministically. Zero live cost. Each fixture file is a JSON capture
of one real LLM response (from DEMO-M5-O3 or pre-flight captures).

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
**Corpus pass**: median(sample-01..10 medians) ≥7/10.

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

Any `is_synthetic` column addition (Mechanism A, §A.2) must be implemented as an additive
migration (`ALTER TABLE dispatches ADD COLUMN is_synthetic INTEGER NOT NULL DEFAULT 0`) that
does not violate the 5 abi_compat promises from m5-handoff.yaml. Specifically: the migration
must NOT drop the `audit_no_update` or `audit_no_delete` triggers (promise #1). The TG-A paired
test triple (§A.7) verifies this.

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
      └─→ pytest --cov-fail-under=100 on deterministic transitions

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
| AD-M6-4 | is_synthetic tagging mechanism (Mechanism A schema column vs Mechanism B title prefix) | **Deferred to Phase B**. Phase B implementer must inspect current dispatches schema and choose: if schema migration cost is acceptable and aligns with M6 timeline, use Mechanism A (`is_synthetic` column). If migration is blocked (e.g., pending migrations in flight), fall back to Mechanism B. Document choice in AD-M6-4 slot. |
| AD-M6-5 | Pre-flight fixture provenance (Option A replay vs Option B fresh synthetic vs Option C cross-project) | **Deferred to Phase B kickoff**. Check whether `aria-orchestrator/docs/demo-m5-o3-*.yaml` capture files exist from M5. If yes, prefer Option A (regression continuity). Document in `.aria/probes/m6-preflight-provenance.md`. |
| AD-M6-6 | AdvancingClock DI injection point (clock parameter on state machine vs on individual transition methods) | Clock parameter injected at state machine class constructor level (`AriaStateMachine(clock=FakeClock(...))`) rather than per-method. This minimizes API surface change while enabling full deterministic time control. All time-sensitive internal methods read `self._clock.now()` instead of `datetime.now()`. |

---

## Acceptance criteria

All criteria are binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`.
No subjective language. Each criterion cites the concrete verifiable evidence.

Exit code contract (consistent with Spec #1 AC-9):
- `exit 0` — all sub-checks PASS.
- `exit 1` — one or more AC sub-checks FAIL (data condition: thresholds not met, files wrong count, scores below rubric).
- `exit 2` — infrastructure error that prevents evaluation (required file missing, corrupt JSON, DB unavailable).

### AC-1 — 7-day uptime and probe files complete

**Evidence**:

```bash
python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --tg-a --check-uptime
```

- Exit code 0.
- stdout contains `[PASS] AC-1: alloc uptime >= 168h (actual: <N>h)`.
- All 7 probe files exist:
  ```bash
  for i in 1 2 3 4 5 6 7; do
    test -f ".aria/probes/m6-7d-day-${i}.md" || echo "MISSING day-${i}"
  done
  # must produce no output
  ```
- Day-3 probe file contains line `Day-3 gate verdict: PASS`.

Non-zero exit or `MISSING` output for any day file → AC-1 FAIL.

### AC-2 — Dispatch stratification ≥10 with cap and cross-project evidence

**Evidence**:

```python
# Binary-falsifiable SQL gate
import sqlite3, sys
conn = sqlite3.connect('aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/aria_layer1.db')
cur = conn.cursor()

# Total S9 dispatches in 7d window
cur.execute("""
    SELECT COUNT(*) FROM dispatches
    WHERE final_state = 'S9'
    AND created_at BETWEEN :start AND :end
""", {"start": run_start_iso, "end": run_end_iso})
total = cur.fetchone()[0]
assert total >= 10, f"FAIL AC-2: total S9 dispatches {total} < 10"

# Synthetic cap
cur.execute("""
    SELECT SUM(CASE WHEN is_synthetic=1 THEN 1 ELSE 0 END),
           COUNT(*)
    FROM dispatches
    WHERE final_state='S9' AND created_at BETWEEN :start AND :end
""", {"start": run_start_iso, "end": run_end_iso})
synth_count, total2 = cur.fetchone()
assert synth_count / total2 <= 0.70, f"FAIL AC-2: synthetic ratio {synth_count}/{total2} > 70%"

# Stratification: ≥1 per required type
for issue_type in ('bug', 'feature', 'stale'):
    cur.execute("""
        SELECT COUNT(*) FROM dispatches
        WHERE final_state='S9' AND issue_type=? AND created_at BETWEEN ? AND ?
    """, (issue_type, run_start_iso, run_end_iso))
    n = cur.fetchone()[0]
    assert n >= 1, f"FAIL AC-2: no completed {issue_type} dispatch in 7d window"

print("PASS AC-2")
```

Must print `PASS AC-2` without assertion errors.

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

**Evidence**:

```bash
pytest aria-orchestrator/tests/test_state_machine_deterministic.py \
       aria-orchestrator/tests/test_state_machine_stochastic_replay.py \
  --cov=aria_layer1.state_machine \
  --cov-report=term-missing \
  --cov-fail-under=100
```

- Exit code 0.
- Coverage report shows 100% line + branch coverage for `aria_layer1/state_machine.py`
  deterministic transition paths.
- `test_state_machine_stochastic_replay.py` uses committed fixture files only (zero live calls);
  confirmed by: `grep -r "llm_client.complete" aria-orchestrator/tests/test_state_machine_stochastic_replay.py`
  returns no output (no live LLM calls in stochastic replay tests).

### AC-5 — Humanized samples: 10 files, median ≥7/10, cross-ref links present

**Evidence**:

```bash
python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --tg-c
```

- Exit code 0.
- stdout contains `[PASS] AC-5: 10 samples scored, median=<N.N> >= 7.0`.
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

**Evidence**:

```bash
test -f .aria/probes/m6-preflight-log.md && echo "PASS" || echo "FAIL AC-6: preflight log missing"
python3 -c "
import re, sys
content = open('.aria/probes/m6-preflight-log.md').read()
costs = [float(m) for m in re.findall(r'cost_usd:\s*([\d.]+)', content)]
assert len(costs) == 3, f'FAIL AC-6: expected 3 cost entries, found {len(costs)}'
assert all(c <= 2.0 for c in costs), f'FAIL AC-6: dispatch exceeds \$2 hard cap: {costs}'
print('PASS AC-6')
"
```

Must print `PASS AC-6`. All 3 pre-flight dispatches must show `cost_usd <= 2.0` in the log.

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
| R-M6-14 | AdvancingClock DI injection requires refactor of state machine constructor | Medium | AD-M6-6 decision: clock injected at constructor level. Phase B implementer must audit all `datetime.now()` calls in `state_machine.py` and replace with `self._clock.now()`; existing tests may need update to pass `FakeClock` |
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
  A.docs AD-M6-4/5 slots + is_synthetic migration (Mech A)      ~0.5h
  A.tg-a-acceptance check-m6-e2e-acceptance.py --tg-a section   ~1h
TG-A subtotal                                                    ~9-10h

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
Total (AI-implementable)                                         ~28-29h ≈ 29h
```

Phase A audit overhead ~1h is tracked separately (not impl).

Q-NEW-1 delta: +1h for hybrid mock layer rationale documentation and per-mode matrix in TG-B.

Owner manual actions (post-ship, not in B.2):
- Fill `.aria/probes/m6-7d-day-{1..7}.md` probe files daily during 7d run.
- Score `score-{01..10}-owner.md` files after TG-A completes.
- Confirm pre-flight fixture provenance in `.aria/probes/m6-preflight-provenance.md`.

---

## Dependencies

| Dependency | Direction | Notes |
|------------|-----------|-------|
| Spec #1 `aria-2.0-m6-cost-acceptance` AC-7 (3-day rolling history PASS) | Upstream (hard gate) | Spec #2 Phase B MUST NOT start until `validate-m6-handoff.py --check-3-day-history` exits 0; Spec #1 commit `c29a800` Approved |
| M5 dispatches table (`token_cost_usd`, `provider_cost_model`, `final_state`, `issue_type`) | Upstream (already shipped M2+) | All SQL queries in TG-A read existing M5 columns; no new migrations required except optional `is_synthetic` (AD-M6-4) |
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
- [docs/requirements/prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) line 630-641 — E2E resilience requirements (7d uptime, crash modes, humanized commands)
- PRD §634 — WAL crash mode enumeration (4 sub-clauses, P-5)
- PRD §639 — humanized command rubric (7 dimensions, median ≥7/10)

**Memory entries woven**:
- `[[feedback_phase_b_velocity_patterns_2026-04-29]]` — AdvancingClock DI in §B.3 + AD-M6-6
- `[[feedback_mock_layer_per_failure_semantic]]` — Q-NEW-1 hybrid rationale matrix in §B.1
- `[[feedback_test_mock_pattern_hides_prod_bug]]` — mock-shape discipline in §B.1 + R-M6-9
- `[[feedback_smoke_dispatch_sql_inject_pattern]]` — synthetic dispatch SQL inject pattern in §A.2
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — all ACs cite concrete evidence
- `[[feedback_spec_v2_body_propagation_2pass]]` — P-4..P-9 threaded into both §What and tasks.md
- `[[project_glm_routing_luxeno]]` — Luxeno (Layer 1) vs Zhipu (Layer 2) routing context for TG-A
- `[[feedback_pat_scope_canonical_from_codebase_grep]]` — cross-project PAT scope check in P-9
