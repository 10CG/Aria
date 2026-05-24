# M6 Spec #2 Tasks — E2E Resilience (runtime observability + crash recovery + humanized samples)

> **Spec**: [aria-2.0-m6-e2e-resilience](./proposal.md)
> **Level**: 3 (Full)
> **Status**: Draft
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2 Spec #2 + §4 P-4..P-9)
> **Estimated total**: ~29h impl (~10h TG-A + ~13h TG-B + ~6h TG-C; +1h Q-NEW-1 hybrid mock layer)
> **Agents**: backend-architect (TG-A obs + overall) + qa-engineer (TG-B crash) + knowledge-manager (TG-C samples)

---

## Phase B precondition (hard gate — do not start Phase B until this passes)

Before any Phase B branch creation:

```bash
python3 aria-orchestrator/docs/validate-m6-handoff.py --check-3-day-history
# Must exit 0: "[PASS] 3-day rolling history: PASS (N files, latest YYYY-MM-DD)"
```

This verifies Spec #1 AC-7 is satisfied (≥3 consecutive daily cost.json snapshots exist).
If this check exits non-zero, Phase B is blocked. Owner must run Spec #1 cron daily until
the 3-day history accumulates, then re-check.

---

## Task Group Overview

| Group | Topic | Scope ref | Est | Agent |
|-------|-------|-----------|-----|-------|
| TG-A-infra | Phase B precondition gate + is_synthetic migration | §What A.2, §Constraints | ~1h | backend-architect |
| TG-A-uptime | Nomad alloc uptime gate + probe structure | §What A.1, A.3, A.4 | ~3h | backend-architect |
| TG-A-dispatch | Dispatch tracker SQL + stratification + pre-flight | §What A.2, A.5, A.6 | ~3.5h | backend-architect |
| TG-A-validate | validate-m6-handoff.py paired test triple | §What A.7 | ~1h | backend-architect |
| TG-A-acceptance | check-m6-e2e-acceptance.py (--tg-a section) | §Acceptance AC-1, AC-2, AC-6, AC-7 | ~1h | backend-architect |
| TG-B-scaffold | 6-mode test scaffold + mock-layer-per-mode rationale doc | §What B.1 (P-4) | ~2h | qa-engineer |
| TG-B-infra | Infra-1/2/3 crash tests (SDK boundary, 4 WAL scenarios + shell script) | §What B.1, B.4 (P-5) | ~4.5h | qa-engineer |
| TG-B-llm | LLM-4/5/6 crash tests (SDK + HTTP layer) | §What B.1 | ~1.5h | qa-engineer |
| TG-B-statemachine | State machine det 100% cov + stochastic mocked replay + AdvancingClock DI | §What B.2, B.3 | ~4h | qa-engineer |
| TG-C-corpus | Rubric + 10 sample files from E2E run | §What C.1, C.2 | ~3h | knowledge-manager |
| TG-C-scores | 10 owner score files + median computation | §What C.3 | ~1.5h | knowledge-manager |
| TG-C-crossref | BOTH-locations cross-ref links + acceptance | §What C.3, AC-5 | ~1h | knowledge-manager |
| TG-C-acceptance | check-m6-e2e-acceptance.py (--tg-c section) | §Acceptance AC-5 | ~0.5h | knowledge-manager |
| T-docs | AD-M6-4/5/6 slots | §How AD table | ~0.5h | backend-architect |

---

## TG-A-infra — Phase B gate + is_synthetic migration (~1h)

- [ ] A-infra-1 Verify Spec #1 AC-7 gate passes before any TG-A code begins:
  ```bash
  python3 aria-orchestrator/docs/validate-m6-handoff.py --check-3-day-history
  ```
  If exit non-zero: STOP. Record block reason in `.aria/probes/m6-gate-check.md`. Do not proceed
  until gate passes.

- [ ] A-infra-2 Inspect current dispatches schema to determine `is_synthetic` tagging mechanism
  (P-7, AD-M6-4). Check whether `is_synthetic` column already exists:
  ```bash
  sqlite3 aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/aria_layer1.db \
    "PRAGMA table_info(dispatches);" | grep is_synthetic
  ```
  - If column exists: skip migration, document Mechanism A choice in AD-M6-4.
  - If column absent and migration acceptable: write
    `aria-orchestrator/hermes-extensions/aria-layer1/migrations/005_m6_synthetic_tag.sql`
    with `ALTER TABLE dispatches ADD COLUMN is_synthetic INTEGER NOT NULL DEFAULT 0;`
    (additive, backward-compatible).
  - If migration blocked: use Mechanism B (title prefix `[DEMO-M6-*]`); document in AD-M6-4.
  Document chosen mechanism in `aria-orchestrator/docs/architecture-decisions.md` AD-M6-4 slot.

- [ ] A-infra-3 If migration 005 was written: verify abi_compat promises not violated:
  ```bash
  python3 aria-orchestrator/docs/validate-m6-handoff.py --check-abi-compat
  ```
  Must exit 0 (audit trigger promises intact after migration). If exit non-zero: investigate
  before proceeding — the migration must not contain `DROP TRIGGER`.

---

## TG-A-uptime — Nomad alloc uptime gate + probe structure (~3h)

- [ ] A-uptime-1 Create probe directory and alloc ID file structure:
  ```bash
  mkdir -p .aria/probes/
  # Owner action: record alloc ID at Day-1 start
  echo "<ALLOC_ID>" > .aria/probes/m6-alloc-id.txt
  ```
  Implement `check-m6-e2e-acceptance.py --tg-a --check-uptime` sub-check:
  - Read alloc ID from `.aria/probes/m6-alloc-id.txt` (exit 2 if file absent).
  - Query Nomad alloc API via `subprocess`:
    ```python
    result = subprocess.run(
        ['nomad', 'alloc', 'status', alloc_id, '-json'],
        capture_output=True,   # per [[feedback_secrets_never_in_conversation]] pattern
        text=True, timeout=30
    )
    data = json.loads(result.stdout)
    started_at = data['TaskStates']['aria-layer1']['StartedAt']
    ```
  - Compute uptime: `uptime_s = (datetime.now(timezone.utc) - datetime.fromisoformat(started_at)).total_seconds()`.
  - PASS condition: `uptime_s >= 604800` (168h × 3600s).
  - Emit `[PASS] AC-1: alloc uptime >= 168h (actual: <N.N>h)` or `[FAIL] AC-1: uptime <N.N>h < 168h`.
  - Exit code 1 on FAIL; exit code 2 if alloc ID file missing or Nomad CLI unavailable.

  REPO_ROOT pattern:
  ```python
  HERE = Path(__file__).resolve().parent    # → aria-orchestrator/acceptance/
  REPO_ROOT = HERE.parent                   # → aria-orchestrator/
  ```

- [ ] A-uptime-2 Create daily probe snapshot template. Implement a probe helper function
  `write_probe_snapshot(day_n, alloc_data, dispatch_summary)` that writes
  `.aria/probes/m6-7d-day-{N}.md` with the structure defined in proposal §A.3.
  - Day-3 probe must include the health gate section filled in.
  - Function is idempotent: if file exists with same day content, no-op.

- [ ] A-uptime-3 Implement Day-3 health gate logic (proposal §A.4):
  ```python
  def check_day3_health_gate(dispatch_summary) -> tuple[bool, str]:
      """Returns (passed: bool, reason: str)."""
      total = dispatch_summary['total_dispatched']
      s_fail = dispatch_summary['s_fail_count']
      stuck = dispatch_summary['stuck_gt_4h']
      has_s9 = dispatch_summary['completed_s9'] >= 1
      s_fail_rate = s_fail / total if total > 0 else 1.0
      if not has_s9:
          return False, "no complete S0→S9 cycle observed by Day-3"
      if s_fail_rate > 0.50:
          return False, f"S_FAIL rate {s_fail_rate:.1%} > 50%"
      if stuck > 0:
          return False, f"{stuck} dispatch(es) stuck >4h"
      return True, "all Day-3 health gate conditions met"
  ```
  Acceptance sub-check: read Day-3 probe file, assert line
  `Day-3 gate verdict: PASS` exists in content. Exit 1 if line contains `FAIL`.

- [ ] A-uptime-4 Unit test: `check-uptime` sub-check with `uptime_s = 604800` (exactly 168h) →
  PASS (boundary is >= not >). `uptime_s = 604799` (1s short) → FAIL.

- [ ] A-uptime-5 Unit test: Day-3 health gate — fixture with `has_s9=True, s_fail_rate=0.40, stuck=0`
  → PASS. Fixture with `has_s9=False` → FAIL reason contains "S0→S9". Fixture with
  `s_fail_rate=0.51` → FAIL reason contains "S_FAIL rate". Fixture with `stuck=1` → FAIL.

---

## TG-A-dispatch — Dispatch tracker + stratification + pre-flight (~3.5h)

- [ ] A-dispatch-1 Implement dispatch stratification SQL query in acceptance script
  (proposal §A.2, `--tg-a --check-dispatch`):
  ```python
  HERE = Path(__file__).resolve().parent    # → aria-orchestrator/acceptance/
  REPO_ROOT = HERE.parent                   # → aria-orchestrator/
  db_path = REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/aria_layer1.db"
  ```
  Query:
  ```sql
  -- Total S9 completed in 7d window
  SELECT COUNT(*) FROM dispatches
  WHERE final_state = 'S9'
  AND created_at BETWEEN :start AND :end;
  ```
  Assert result >= 10. Emit `[FAIL] AC-2: total S9 dispatches N < 10` if not met.

  NOTE: SQL uses `provider_cost_model` filter only when filtering by provider type, not `provider`
  (schema column SoT: no `provider` column on dispatches table).

- [ ] A-dispatch-2 Implement synthetic cap check:
  ```sql
  SELECT
    SUM(CASE WHEN is_synthetic=1 THEN 1 ELSE 0 END) as synth_count,
    COUNT(*) as total
  FROM dispatches
  WHERE final_state='S9'
  AND created_at BETWEEN :start AND :end;
  ```
  Assert `synth_count / total <= 0.70`. Emit `[FAIL] AC-2: synthetic ratio N/M > 70%` if exceeded.
  If Mechanism B (title prefix): replace `is_synthetic=1` with `title LIKE '[DEMO-M6-%]'`.

- [ ] A-dispatch-3 Implement stratification check per required issue types:
  For each type in `('bug', 'feature', 'stale')`:
  ```sql
  SELECT COUNT(*) FROM dispatches
  WHERE final_state='S9' AND issue_type=? AND created_at BETWEEN ? AND ?;
  ```
  Assert result >= 1 per type. Emit `[FAIL] AC-2: no completed <type> dispatch in 7d window`.

- [ ] A-dispatch-4 Unit test: in-memory SQLite with 10 completed dispatches (3 bug, 4 feature, 3 stale,
  7 synthetic, 3 real) → AC-2 PASS. Fixture with 9 total → FAIL (< 10). Fixture with 8 synthetic
  out of 10 (>70%) → FAIL. Fixture with 0 stale → FAIL.

- [ ] A-dispatch-5 Implement pre-flight provenance script (proposal §A.5):
  Create `.aria/probes/m6-preflight-provenance.md` template (owner fills at Phase B kickoff):
  ```markdown
  # M6 Pre-flight provenance

  Selected option: [A|B|C]
  Rationale: ...
  Fixture source: [path or "fresh synthetic" or "cross-project"]
  ```
  Create `.aria/probes/m6-preflight-log.md` structure (3 dispatch entries, each containing
  `dispatch_id`, `fixture_source`, `outcome`, `cost_usd`).
  Implement acceptance sub-check (`--tg-a --check-preflight`):
  - File exists: exit 2 if absent.
  - Parse 3 `cost_usd` entries: assert all <= 2.0.
  - Emit `[PASS] AC-6: preflight log committed, all 3 dispatches <= $2.00`.

- [ ] A-dispatch-6 Implement cross-project conditional acceptance (P-9):
  In acceptance script, check dispatches for cross-project evidence:
  ```sql
  SELECT dispatch_id, project_name FROM dispatches
  WHERE final_state='S9'
  AND project_name != 'Aria'
  AND created_at BETWEEN :start AND :end
  LIMIT 1;
  ```
  If row found: emit `[PASS+] AC-2: cross-project evidence present (project=<name>, dispatch_id=<id>)`.
  If no cross-project row: emit `[PASS] AC-2: Aria-only 7d window (cross-project conditional not met)`.
  Neither outcome is a FAIL — cross-project is conditional, not mandatory.

- [ ] A-dispatch-7 Unit test: pre-flight check with 3 entries all `cost_usd <= 2.0` → PASS.
  Fixture with one entry `cost_usd = 2.01` → FAIL with hard cap message. Missing file → exit 2.

---

## TG-A-validate — validate-m6-handoff.py paired test triple (~1h)

<!-- P-6: TG-A → TG-B handoff checkpoint -->
These tests verify abi_compat promises remain intact after any TG-A schema migrations.

- [ ] A-validate-1 Implement paired test triple in
  `aria-orchestrator/tests/test_validate_m6_handoff_tga_compat.py`:

  - **Test 1** — schema.sql still contains triggers after migration 005:
    ```python
    def test_audit_triggers_survive_migration_005():
        schema = (REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/schema.sql").read_text()
        assert "audit_no_update" in schema
        assert "audit_no_delete" in schema
    ```
  - **Test 2** — migration 005 does NOT contain DROP TRIGGER (if file exists):
    ```python
    def test_migration_005_no_drop_trigger():
        m005 = REPO_ROOT / "hermes-extensions/aria-layer1/migrations/005_m6_synthetic_tag.sql"
        if not m005.exists():
            pytest.skip("Migration 005 not written (Mechanism B in use)")
        content = m005.read_text()
        assert "DROP TRIGGER" not in content, "Migration 005 must not drop audit triggers"
    ```
  - **Test 3** — validate-m6-handoff.py --check-abi-compat exits 0 after 005:
    ```python
    def test_validate_m6_abi_compat_after_tga_migration(tmp_path):
        result = subprocess.run(
            ["python3", str(REPO_ROOT / "docs/validate-m6-handoff.py"), "--check-abi-compat"],
            capture_output=True, text=True   # per [[feedback_secrets_never_in_conversation]] pattern
        )
        assert result.returncode == 0, f"abi_compat check failed:\n{result.stdout}\n{result.stderr}"
        for promise_id in [
            "dispatch_audit_log_immutable_promise",
            "rework_round_cap_default_3_promise",
            "spec_drift_threshold_default_70_promise",
            "comment_poll_direct_transition_promise",
            "risk_tier_dual_write_literal_always_promise",
        ]:
            assert promise_id in result.stdout
    ```

  REPO_ROOT pattern for test file (located at `aria-orchestrator/tests/`):
  ```python
  HERE = Path(__file__).resolve().parent    # → aria-orchestrator/tests/
  REPO_ROOT = HERE.parent                   # → aria-orchestrator/
  ```

---

## TG-A-acceptance — check-m6-e2e-acceptance.py --tg-a section (~1h)

- [ ] A-acceptance-1 Create `aria-orchestrator/acceptance/check-m6-e2e-acceptance.py` with
  CLI interface:
  - `--tg-a` runs all TG-A checks (AC-1, AC-2, AC-6, AC-7).
  - `--tg-c` runs all TG-C checks (AC-5).
  - `--tg-a --check-uptime` / `--check-dispatch` / `--check-preflight` for individual sub-checks.
  - Exit code contract: 0 = all pass, 1 = AC data fail, 2 = infrastructure error.
  - Each sub-check emits `[PASS] AC-N: <name>` or `[FAIL] AC-N: <reason>` or `[ERROR] AC-0: <reason>`.

  REPO_ROOT pattern (mandatory, mirrors Spec #1 pattern):
  ```python
  HERE = Path(__file__).resolve().parent    # → aria-orchestrator/acceptance/
  REPO_ROOT = HERE.parent                   # → aria-orchestrator/
  ```

- [ ] A-acceptance-2 Implement AC-7 sub-check in acceptance script (`--check-abi-compat`):
  Delegate to `validate-m6-handoff.py --check-abi-compat` via subprocess:
  ```python
  result = subprocess.run(
      ["python3", str(REPO_ROOT / "docs/validate-m6-handoff.py"), "--check-abi-compat"],
      capture_output=True, text=True
  )
  if result.returncode != 0:
      print(f"[FAIL] AC-7: abi_compat promises violated:\n{result.stdout}")
      sys.exit(1)
  print("[PASS] AC-7: all 5 abi_compat promises verified")
  ```

- [ ] A-acceptance-3 Integration test: run `check-m6-e2e-acceptance.py --tg-a` against a full
  passing fixture (in-memory SQLite with ≥10 stratified dispatches, probe files present and
  correct, Day-3 gate PASS, preflight log committed) → exit 0, all `[PASS]` lines. This test
  exercises the complete TG-A acceptance path end-to-end.

---

## TG-B-scaffold — 6-mode scaffold + mock-layer rationale doc (~2h)

<!-- P-4: Mock-layer-per-mode matrix thread -->
- [ ] B-scaffold-1 Write mock-layer-per-mode rationale document
  `aria-orchestrator/docs/crash-recovery-mock-layer-rationale.md` (Q-NEW-1 deliverable):

  Document the complete matrix from proposal §B.1 (6 rows: ID, failure type, mock layer, rationale).
  Include a section "Mock-shape discipline" citing `[[feedback_test_mock_pattern_hides_prod_bug]]`
  and `[[feedback_mock_layer_per_failure_semantic]]` — exact exception class + attribute shape for
  each SDK-boundary mock must match production code. Any deviation in a test must use
  `# mock-layer-deviation-ok: <reason>` comment.

- [ ] B-scaffold-2 Create test file scaffold (empty test functions with docstrings) for all 6 modes:
  - `aria-orchestrator/tests/test_crash_infra1.py` (Hermes SIGKILL, SDK)
  - `aria-orchestrator/tests/test_crash_infra2.py` (Layer 2 alloc SIGKILL, SDK)
  - `aria-orchestrator/tests/test_crash_infra3_wal.py` (WAL × 4 scenarios, SDK)
  - `aria-orchestrator/tests/test_crash_llm4.py` (429 rate-limit, SDK)
  - `aria-orchestrator/tests/test_crash_llm5.py` (invalid JSON, httpx_mock)
  - `aria-orchestrator/tests/test_crash_llm6.py` (provider 5xx, httpx_mock)

  Each file begins with:
  ```python
  # Mock layer: [SDK|HTTP] per crash-recovery-mock-layer-rationale.md
  # Failure mode: <description>
  ```

  Verify scaffold structure is correct before filling in tests.

- [ ] B-scaffold-3 Add `FakeClock` class to `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/testing.py`
  (or create file if absent). Class definition per proposal §B.3:
  ```python
  class FakeClock:
      def __init__(self, start: datetime):
          self._now = start
      def now(self) -> datetime:
          return self._now
      def advance(self, seconds: int) -> None:
          from datetime import timedelta
          self._now += timedelta(seconds=seconds)

  class RealClock:
      def now(self) -> datetime:
          return datetime.now(timezone.utc)
  ```

---

## TG-B-infra — Infra-1/2/3 crash tests + WAL shell script (~4.5h)

<!-- P-5: 4 WAL scenarios -->
- [ ] B-infra-1 Implement `test_crash_infra1.py` (Hermes SIGKILL, SDK boundary):
  - Reuse `test_t12` existing fixture structure if available.
  - Mock `hermes_client.dispatch()` to raise `ProcessKilledError` at a mid-transition checkpoint.
  - Assert: (a) state machine transitions to S_FAIL; (b) S_FAIL state is written to DB before
    exception propagates (state write is atomic); (c) structured error log entry written with
    `{"event": "process_killed", "recovery": "s_fail_set"}`.
  - Mock at SDK boundary: `unittest.mock.patch('aria_layer1.hermes_client.HermesClient.dispatch',
    side_effect=ProcessKilledError('simulated SIGKILL'))`.
  - Do NOT use generic `Exception` as the mock — use exact `ProcessKilledError` class (mock-shape
    discipline per `[[feedback_test_mock_pattern_hides_prod_bug]]`).

- [ ] B-infra-2 Implement `test_crash_infra2.py` (Layer 2 alloc SIGKILL, SDK boundary):
  - Light-1 node CANNOT be drained (Nomad drain requires node-level operator access, not alloc scope).
    Reframe: alloc kill is simulated as `AllocTerminatedError` from `layer2_client.run_task()`.
  - Assert: (a) state machine to S_FAIL; (b) S_FAIL state written; (c) structured log entry
    `{"event": "alloc_killed", "node": "light-1", "recovery": "s_fail_set"}`.
  - Document the light-1 drain reframe with comment:
    ```python
    # light-1 cannot be drained via alloc API (requires node-level access).
    # Alloc kill is the correct failure semantic for this test.
    # See crash-recovery-mock-layer-rationale.md Infra-2.
    ```

- [ ] B-infra-3 Implement `test_crash_infra3_wal.py` (WAL truncation × 4 scenarios, SDK boundary):
  Must contain exactly 4 test functions, one per scenario (P-5):

  - `test_wal_truncated_0_bytes_pre_checkpoint` (WAL-A):
    - `tmpdir` fixture: create SQLite DB in WAL mode, truncate WAL to 0 bytes.
    - Monkey-patch `sqlite3.connect()` to return connection that raises
      `sqlite3.DatabaseError('database disk image is malformed')` on first execute.
    - Assert: state machine → S_FAIL; `PRAGMA integrity_check` invoked in recovery handler;
      log entry `{"event": "wal_fault", "scenario": "WAL-A", "recovery": "s_fail_set"}`.

  - `test_wal_truncated_0_bytes_mid_checkpoint` (WAL-B):
    - Simulate WAL zeroed during active checkpoint: mock `sqlite3.connect()` to raise
      `sqlite3.OperationalError('database is locked')`.
    - Same assertions as WAL-A.

  - `test_wal_corrupted_garbage_bytes` (WAL-C):
    - `tmpdir` fixture: create SQLite DB in WAL mode, write garbage bytes to WAL file.
    - Same mock pattern as WAL-A.
    - Same assertions.

  - `test_wal_file_deleted` (WAL-D):
    - `tmpdir` fixture: create SQLite DB in WAL mode, delete WAL file entirely.
    - Assert: SQLite reopens DB without WAL (no corruption visible); a subsequent clean
      connection can read/write successfully (no data corruption).
    - Assert: structured log entry `{"event": "wal_fault", "scenario": "WAL-D", "recovery": "wal_auto_recreated"}`.

- [ ] B-infra-4 Write `aria-orchestrator/acceptance/m6-wal-fault.sh` (M-qa-R3-8, AC-3):
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  # M6 WAL fault injection shell script (AC-3 artifact)
  # Creates a temp SQLite DB, truncates WAL to 0 bytes, calls recovery handler.
  TMPDIR=$(mktemp -d)
  DB="${TMPDIR}/test.db"
  sqlite3 "${DB}" "PRAGMA journal_mode=WAL; CREATE TABLE t (id INTEGER);" >/dev/null 2>&1
  WAL="${DB}-wal"
  truncate --size=0 "${WAL}"    # WAL-A simulation
  # Call recovery handler
  python3 -m aria_layer1.recovery --wal-check "${DB}"
  STATUS=$?
  rm -rf "${TMPDIR}"
  if [ "${STATUS}" -eq 0 ] || [ "${STATUS}" -eq 1 ]; then
      echo "[PASS] m6-wal-fault.sh: recovery handler returned expected status ${STATUS}"
      exit 0
  else
      echo "[FAIL] m6-wal-fault.sh: unexpected exit code ${STATUS}"
      exit 1
  fi
  ```
  Make executable: `chmod +x aria-orchestrator/acceptance/m6-wal-fault.sh`.

---

## TG-B-llm — LLM-4/5/6 crash tests (~1.5h)

- [ ] B-llm-1 Implement `test_crash_llm4.py` (429 rate-limit, SDK boundary):
  - Mock `llm_client.complete()` to raise `RateLimitError(retry_after=30)` when called during
    an S2/S3/S6 LLM call.
  - Use `FakeClock` to advance time past `retry_after` and verify retry attempt.
  - Assert: (a) initial 429 → state machine pauses (not → S_FAIL immediately); (b) after
    `retry_after` seconds elapsed (via `FakeClock.advance(31)`), retry is attempted; (c) if
    retry succeeds, state continues normally; (d) if retry raises `RateLimitError` again
    (2nd consecutive), state machine → S_FAIL with log entry
    `{"event": "rate_limit_exhausted", "recovery": "s_fail_set"}`.

- [ ] B-llm-2 Implement `test_crash_llm5.py` (invalid JSON, httpx_mock at HTTP layer):
  - Use `pytest_httpx` (or equivalent httpx mock) to intercept the provider HTTP call:
    ```python
    httpx_mock.add_response(
        method="POST",
        url=re.compile(r"https://.*api.*"),
        status_code=200,
        content=b"{ bad json ["     # malformed response body
    )
    ```
  - Assert: (a) SDK adapter raises JSON parse error (not generic `Exception`); (b) state
    machine → S_FAIL; (c) log entry `{"event": "llm_response_malformed", "recovery": "s_fail_set"}`.
  - Mock at HTTP layer (not SDK): validates the SDK adapter's JSON parsing path is exercised
    (per `[[feedback_mock_layer_per_failure_semantic]]`).
  - Add comment:
    ```python
    # Mock layer: HTTP (httpx_mock). Invalid JSON arrives as valid HTTP 200.
    # SDK adapter's response parsing is the code under test.
    # See crash-recovery-mock-layer-rationale.md LLM-5.
    ```

- [ ] B-llm-3 Implement `test_crash_llm6.py` (provider 5xx, httpx_mock at HTTP layer):
  - `httpx_mock.add_response(status_code=503, json={"error": "service_unavailable"})`.
  - Assert: SDK converts 5xx to `ProviderUnavailableError`; state machine → S_FAIL; log entry
    `{"event": "provider_unavailable", "status_code": 503, "recovery": "s_fail_set"}`.
  - Add comment:
    ```python
    # Mock layer: HTTP (httpx_mock). 5xx is an HTTP-level failure.
    # SDK ProviderUnavailableError conversion is the code under test.
    # See crash-recovery-mock-layer-rationale.md LLM-6.
    ```

---

## TG-B-statemachine — State machine coverage + AdvancingClock DI (~4h)

- [ ] B-sm-1 Audit `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/state_machine.py`
  for all `datetime.now()` calls. Replace each with `self._clock.now()`.
  Add `clock` parameter to `AriaStateMachine.__init__`:
  ```python
  def __init__(self, ..., clock=None):
      self._clock = clock or RealClock()
  ```
  Per AD-M6-6: injection at constructor level (not per-method) minimizes API surface change.
  Document all replaced call sites in a comment block at top of state_machine.py:
  ```python
  # AdvancingClock DI: all datetime.now() calls replaced with self._clock.now()
  # to prevent wall-clock flakiness (per [[feedback_phase_b_velocity_patterns_2026-04-29]]).
  # Replaced sites: [list file:line references here]
  ```

- [ ] B-sm-2 Implement `test_state_machine_deterministic.py`:
  For each deterministic state (S0, S1, S4, S5, S7, S8, S9, S_FAIL), write tests covering:
  - Normal outbound transition: e.g., `test_s0_to_s1_on_claim` — state machine in S0, issue
    claim succeeds → S1.
  - Failure-injected outbound transition: e.g., `test_s0_to_sfail_on_infra2_kill` — state
    machine in S0, `AllocTerminatedError` raised during claim → S_FAIL.
  - Re-entry idempotency: e.g., `test_s1_reentry_is_noop` — state machine in S1, second
    entry attempt → remains S1 (no double-claim side effect).

  Use `FakeClock` for all time-sensitive transitions. Zero live LLM calls.
  Run with `--cov-fail-under=100` for `aria_layer1/state_machine.py` deterministic paths.

- [ ] B-sm-3 Implement `test_state_machine_stochastic_replay.py` (S2/S3/S6 mocked replay):
  Commit fixture files to `aria-orchestrator/tests/fixtures/state_machine/`:
  - `s2_plan_response.json` — captured LLM response for S2 (planning) transition.
  - `s3_code_response.json` — captured LLM response for S3 (code generation) transition.
  - `s6_review_response.json` — captured LLM response for S6 (review processing) transition.
  (Source: DEMO-M5-O3 captures or pre-flight captures from TG-A §A.5. If pre-flight captures
  not yet available at test time, use placeholder fixtures and update in Phase B.2.)

  Tests use `unittest.mock.patch` to return fixture JSON from `llm_client.complete()` without
  any real HTTP call. Assert state transitions S2→S3, S3→S4, S6→S7 fire correctly.

  Verify zero live calls: add `conftest.py` fixture that fails the test if any real HTTP call
  is made to provider URLs:
  ```python
  @pytest.fixture(autouse=True)
  def no_live_llm_calls(httpx_mock):
      """Fail if any live LLM HTTP call is attempted in stochastic replay tests."""
      yield
      # httpx_mock raises AssertionError if any unmatched request is made
  ```

- [ ] B-sm-4 Run full TG-B test suite and verify AC-4:
  ```bash
  pytest aria-orchestrator/tests/test_state_machine_deterministic.py \
         aria-orchestrator/tests/test_state_machine_stochastic_replay.py \
    --cov=aria_layer1.state_machine \
    --cov-report=term-missing \
    --cov-fail-under=100
  ```
  Must exit 0. If coverage < 100%, identify uncovered lines and add targeted tests before
  declaring TG-B complete.

---

## TG-C-corpus — Rubric + 10 sample files (~3h)

<!-- TG-C tasks: knowledge-manager agent -->
- [ ] C-corpus-1 Create corpus directory structure:
  ```bash
  mkdir -p aria-orchestrator/evals/m6-prompt-quality/corpus/
  ```

- [ ] C-corpus-2 Write `aria-orchestrator/evals/m6-prompt-quality/rubric.md` with 7 rubric
  dimensions per proposal §C.2:
  - Header: `# M6 Humanized Command Rubric (PRD §639)`
  - Table: Dim | Name | Scoring guidance (7 rows, each integer 0-10 scale).
  - Section: "Scoring procedure" — score each sample on all 7 dims; compute median; record in
    corresponding `score-NN-owner.md`.
  - Section: "Pass threshold" — corpus passes if `median(all 10 sample medians) >= 7.0`.
  - Section: "Scoring rationale" — brief note that D1 (naturalness) and D6 (technical accuracy)
    carry independent weight; a sample may score 10 on D1 but 0 on D6 and still fail median gate.

- [ ] C-corpus-3 Create 10 sample file templates:
  `aria-orchestrator/evals/m6-prompt-quality/corpus/sample-{01..10}.md`

  Each file template:
  ```markdown
  # Sample NN — [issue title placeholder]

  - **Dispatch ID**: [fill from dispatches table after E2E run]
  - **Issue type**: [bug|feature|stale]
  - **State at dispatch**: [S2/S3/S6/etc.]
  - **is_synthetic**: [yes|no]
  - **Dispatched**: [ISO-8601 timestamp]

  ## Command text (verbatim)

  [FILL: full autonomous command text as sent to developer]

  ---
  *Cross-reference: [standards/autonomous/humanized-command-patterns.md](../../../../standards/autonomous/humanized-command-patterns.md)
  (Spec #3 TG-DOCS-B, shipped separately)*
  ```

  The cross-reference footer is mandatory in all 10 sample files (verified by AC-5 grep check).
  After the TG-A 7-day run completes, owner fills in actual dispatch data from `dispatches` table.

---

## TG-C-scores — 10 owner score files + median (~1.5h)

- [ ] C-scores-1 Create 10 owner score file templates:
  `aria-orchestrator/evals/m6-prompt-quality/score-{01..10}-owner.md`

  Each file template:
  ```markdown
  # Score NN — owner scoring

  - **Sample**: sample-NN
  - **Scorer**: owner (uni.concept.wzfq@gmail.com)
  - **Scored**: [ISO-8601 date]

  ## Dimension scores

  | Dim | Name | Score (0-10) |
  |-----|------|-------------|
  | D1 | Naturalness | [FILL] |
  | D2 | Specificity | [FILL] |
  | D3 | Tone appropriateness | [FILL] |
  | D4 | Completeness | [FILL] |
  | D5 | Conciseness | [FILL] |
  | D6 | Technical accuracy | [FILL] |
  | D7 | Autonomy footprint | [FILL] |

  **Median score**: [computed from above 7 scores]

  ## Qualitative note (optional)
  [1-2 sentences]
  ```

  Score files are filled by owner after TG-A E2E run completes and samples are collected.

- [ ] C-scores-2 Implement median computation in acceptance script (--tg-c):
  ```python
  import statistics, re
  score_files = sorted(
      (CORPUS_DIR.parent).glob("score-*-owner.md")
  )
  assert len(score_files) == 10, f"Expected 10 score files, found {len(score_files)}"
  medians = []
  for f in score_files:
      content = f.read_text()
      scores = [int(m) for m in re.findall(r'\|\s*D\d\s*\|[^|]+\|\s*(\d+)\s*\|', content)]
      assert len(scores) == 7, f"Expected 7 scores in {f.name}, found {len(scores)}"
      medians.append(statistics.median(scores))
  corpus_median = statistics.median(medians)
  if corpus_median >= 7.0:
      print(f"[PASS] AC-5: 10 samples scored, median={corpus_median:.1f} >= 7.0")
  else:
      print(f"[FAIL] AC-5: median={corpus_median:.1f} < 7.0 (corpus below rubric threshold)")
      sys.exit(1)
  ```

---

## TG-C-crossref — BOTH-locations cross-ref links + verification (~1h)

<!-- Cross-ref Spec #3 TG-DOCS-B BOTH-locations design -->
- [ ] C-crossref-1 Verify all 10 `corpus/sample-*.md` files contain the cross-reference footer link
  to `standards/autonomous/humanized-command-patterns.md`. If any sample file is missing the link,
  add it before finalizing TG-C.

- [ ] C-crossref-2 Verify that Spec #3 TG-DOCS-B `standards/autonomous/humanized-command-patterns.md`
  (when it ships) contains the reciprocal link back to
  `aria-orchestrator/evals/m6-prompt-quality/`. This is a coordination checkpoint:
  - If Spec #3 has not shipped yet: add a TODO comment in `rubric.md`:
    ```markdown
    <!-- TODO: After Spec #3 ships, verify humanized-command-patterns.md contains reciprocal
    link to aria-orchestrator/evals/m6-prompt-quality/ -->
    ```
  - If Spec #3 has shipped: grep verify and remove the TODO.

- [ ] C-crossref-3 Document BOTH-locations design in `aria-orchestrator/evals/m6-prompt-quality/README.md`
  (create if absent):
  ```markdown
  # M6 Prompt Quality Corpus

  This directory contains the M6 E2E run humanized command corpus (10 samples, rubric, scores).

  ## BOTH-locations design

  - **Here** (`aria-orchestrator/evals/m6-prompt-quality/corpus/`): raw scored corpus,
    Aria-specific deployment context, including all dispatch metadata.
  - **Spec #3** (`standards/autonomous/humanized-command-patterns.md`): curated canonical
    patterns for Lab-wide reuse, anonymized of project-specific details. Source: this corpus.

  ## See also

  - [rubric.md](rubric.md) — PRD §639 scoring rubric (7 dimensions)
  - [standards/autonomous/humanized-command-patterns.md](../../../../standards/autonomous/humanized-command-patterns.md)
  ```

---

## TG-C-acceptance — check-m6-e2e-acceptance.py --tg-c section (~0.5h)

- [ ] C-acceptance-1 Implement `--tg-c` section in `check-m6-e2e-acceptance.py`:
  - File count checks (10 samples, 10 scores, rubric.md existence).
  - Cross-ref link grep (all 10 samples contain `humanized-command-patterns.md`).
  - Median score computation (per C-scores-2 logic above).
  - Exit code: 0 = all PASS, 1 = AC data fail (missing files, low median), 2 = infrastructure
    error (directory missing, score parse error).

- [ ] C-acceptance-2 Unit test: run `--tg-c` against complete passing fixture (10 samples with
  cross-ref footers, 10 score files each with 7 scores all = 8, rubric.md exists) → exit 0,
  `[PASS] AC-5: 10 samples scored, median=8.0 >= 7.0`.

- [ ] C-acceptance-3 Unit test: fixture with only 9 sample files → exit 1 or 2 with count error.
  Fixture with 10 samples but corpus median = 6.5 → exit 1 `[FAIL] AC-5: median=6.5 < 7.0`.
  Fixture with sample missing cross-ref footer → exit 1 `[FAIL] AC-5: N samples missing cross-ref link`.

---

## T-docs — AD-M6-* slots (~0.5h)

- [ ] T-docs-1 Add AD-M6-4 decision stub to `aria-orchestrator/docs/architecture-decisions.md`:
  "is_synthetic tagging mechanism: Deferred to Phase B. Mechanism A (schema column) preferred if
  migration cost acceptable; Mechanism B (title prefix) fallback. Document actual choice in this
  slot during Phase B kickoff."

- [ ] T-docs-2 Add AD-M6-5 decision stub: "Pre-flight dispatch fixture provenance: Deferred to
  Phase B. Option A (replay M5 O3 captures) preferred for regression continuity. Document actual
  provenance in `.aria/probes/m6-preflight-provenance.md` during Phase B kickoff."

- [ ] T-docs-3 Add AD-M6-6 decision: "AdvancingClock DI injection point: clock injected at
  `AriaStateMachine` constructor level. All `datetime.now()` calls in `state_machine.py` replaced
  with `self._clock.now()`. `RealClock` is the default (no behavior change in production)."

- [ ] T-docs-4 Verify US-026 `docs/requirements/user-stories/US-026.md` references
  `aria-2.0-m6-e2e-resilience` change ID; update if missing.

---

## Ordering dependencies

```
Phase B precondition gate (A-infra-1)
    │
    │ Spec #1 --check-3-day-history PASS required before any Phase B work
    │
    ▼
TG-A-infra (A-infra-2, A-infra-3)     — establish is_synthetic mechanism (AD-M6-4)
    │
    ├── TG-A-uptime (A-uptime-1..5)   — Nomad alloc gate + probe structure
    │       │
    │       └── TG-A-dispatch (A-dispatch-1..7)  — SQL queries + pre-flight + cross-project
    │               │
    │               └── TG-A-validate (A-validate-1)  — paired test triple (after migration 005 if any)
    │                       │
    │                       └── TG-A-acceptance (A-acceptance-1..3)  — acceptance script TG-A section
    │
    ├── TG-B-scaffold (B-scaffold-1..3)  — parallel with TG-A-dispatch; no dependency on 7d run
    │       │
    │       └── TG-B-infra (B-infra-1..4)  — depends on scaffold + FakeClock
    │               │
    │               ├── TG-B-llm (B-llm-1..3)  — parallel with B-infra
    │               │
    │               └── TG-B-statemachine (B-sm-1..4)  — depends on FakeClock (B-scaffold-3)
    │
    └── TG-C-corpus (C-corpus-1..3)  — sequential after TG-A 7d run completes (needs real samples)
            │
            └── TG-C-scores (C-scores-1..2)  — owner fills after corpus collected
                    │
                    └── TG-C-crossref (C-crossref-1..3)  — after scores + Spec #3 coordination
                            │
                            └── TG-C-acceptance (C-acceptance-1..3)

T-docs (T-docs-1..4)  — parallel with all above (documentation slots)
```

**TG-A → TG-B decoupling**: TG-B can proceed independently of TG-A's 7-day run. TG-B uses
mock-only fixtures and does not require live dispatch data. TG-B may begin after pre-flight (§A.5)
confirms state machine is stable (TG-A-dispatch A-dispatch-5 complete).

**TG-C sequencing**: TG-C requires real sample data from the TG-A 7d run. TG-C cannot be
meaningfully started until Day-7 probe is written and dispatches table has ≥10 completed S9 entries.
TG-C-corpus templates (C-corpus-1..3) may be written in advance; sample content is filled post-run.

---

## Precision items cross-reference

| Precision item | DEC source | §What section | Task(s) |
|----------------|------------|---------------|---------|
| P-4: Mock-layer-per-mode matrix (Q-NEW-1 hybrid 4 SDK + 2 HTTP) | DEC §4 + Q-NEW-1 | §What B.1 (full table) | B-scaffold-1, B-infra-1..3, B-llm-1..3 |
| P-5: 4 WAL scenarios (WAL-A/B/C/D) vs 3 enumeration | DEC §4 P-5 + PRD §634 | §What B.2 (4-scenario table) | B-infra-3 |
| P-6: TG-A → TG-B handoff checkpoint contract | DEC §4 P-6 | §What A.7 (checkpoint list) | A-validate-1, TG-B-scaffold start condition |
| P-7: is_synthetic tagging mechanism (Mech A schema column vs Mech B title prefix) | DEC §4 P-7 | §What A.2 (P-7 block) | A-infra-2 + AD-M6-4 |
| P-8: Pre-flight dispatch fixture provenance (Option A/B/C) | DEC §4 P-8 | §What A.5 (P-8 block) | A-dispatch-5 + AD-M6-5 |
| P-9: Cross-project Kairos/silknode acceptance conditions | DEC §4 P-9 | §What A.6 (P-9 block) | A-dispatch-6 |
| Q-NEW-1: Hybrid mock layer +1h scope | Owner Q-NEW-1 2026-05-24 | §What B.1 (hybrid table) + §Effort baseline | B-scaffold-1 + mock-layer-per-mode rationale doc |
| AD-M6-6: AdvancingClock DI at constructor | §How AD table | §What B.3 (FakeClock class) | B-scaffold-3, B-sm-1 |

---

## Status

**Draft** — Ready for Phase A.2 post_spec R1 audit (4-agent parallel: tech-lead-critic + qa + ai + code-reviewer).

**Approved 锁定后** → Phase A.3 agent allocation → Phase B.1 branch creation (after Phase B precondition gate PASS).
