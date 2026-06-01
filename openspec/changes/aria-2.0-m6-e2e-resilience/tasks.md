# M6 Spec #2 Tasks — E2E Resilience (runtime observability + crash recovery + humanized samples)

> **Spec**: [aria-2.0-m6-e2e-resilience](./proposal.md)
> **Level**: 3 (Full)
> **Status**: Approved (Phase A.2 CONVERGED 2026-05-24 via R3 stability; ready for Phase A.3 → Phase B.1 — Phase B gated on Spec #1 AC-7 3-day rolling data precondition)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2 Spec #2 + §4 P-4..P-9)
> **Estimated total**: ~30h impl (~10.5h TG-A + ~13h TG-B + ~6h TG-C; +1h Q-NEW-1 hybrid mock layer; +1h R1 fixes: T-validate-schema-1 + AD-M6-4b)
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
| TG-A-infra | Phase B precondition gate + is_synthetic migration 007 + T-validate-schema-1 | §What A.2, §Constraints | ~1.5h | backend-architect |
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

## TG-A-infra — Phase B gate + is_synthetic migration + schema validation (~1.5h)

<!-- R1-T2-4 fix: Mechanism B removed (title column doesn't exist); AD-M6-4 locked to Mechanism A.
     Migration renamed from 005 to 006 (005 already exists in schema v4.2). Schema validation
     task T-validate-schema-1 added per [[feedback_validator_repo_drift_guard_test]]. (R1 audit 2026-05-24) -->
<!-- R1-T2-1 fix: T-validate-schema-1 added as first TG-A task to verify live dispatches
     schema columns before any SQL implementation. (R1 audit 2026-05-24) -->

- [ ] **T-validate-schema-1** (FIRST task — schema drift guard): Verify live `dispatches` schema
  column-by-column before writing any SQL:
  ```bash
  sqlite3 aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/aria_layer1.db \
    "PRAGMA table_info(dispatches);"
  ```
  Confirm: `state` column exists (NOT `final_state`); `state_entered_at` column exists (NOT
  `created_at`); NO `title`, `issue_type`, or `project_name` columns; `is_synthetic` absent
  (will be added by migration 007). Commit a schema validation test triple alongside migration 007
  (per `[[feedback_validator_repo_drift_guard_test]]`):
  ```python
  # aria-orchestrator/hermes-extensions/aria-layer1/tests/test_schema_column_guard.py
  def test_dispatches_has_state_not_final_state(db_conn):
      cols = {row[1] for row in db_conn.execute("PRAGMA table_info(dispatches)").fetchall()}
      assert 'state' in cols
      assert 'final_state' not in cols
      assert 'created_at' not in cols
      assert 'issue_type' not in cols
      assert 'project_name' not in cols
      assert 'title' not in cols
  ```
  Run against the canonical `schema.sql` applied to a fresh in-memory DB. This test is
  the schema drift regression guard and must pass before any TG-A SQL is written.

- [ ] A-infra-1 Verify Spec #1 AC-7 gate passes before any TG-A code begins:
  ```bash
  python3 aria-orchestrator/docs/validate-m6-handoff.py --check-3-day-history
  ```
  If exit non-zero: STOP. Record block reason in `.aria/probes/m6-gate-check.md`. Do not proceed
  until gate passes.

- [ ] A-infra-2 Add `is_synthetic` column via migration 007 (AD-M6-4 LOCKED to Mechanism A — no
  Mechanism B; `title` column does not exist in live schema). Write:
  `aria-orchestrator/hermes-extensions/aria-layer1/migrations/007_schema_v4.3_add_is_synthetic.sql`
  ```sql
  -- Migration 007: schema v4.2 → v5.0 (additive)
  -- Adds is_synthetic column for M6 7d run stratification tracking
  ALTER TABLE dispatches ADD COLUMN is_synthetic INTEGER DEFAULT 0;
  UPDATE schema_meta SET value='5.0' WHERE key='schema_version';
  ```
  Verify column is absent before running: skip if already present.
  Document in `aria-orchestrator/docs/architecture-decisions.md` AD-M6-4 slot: "Mechanism A
  (schema column is_synthetic, migration 007) — locked at R1 audit 2026-05-24. Mechanism B
  (title prefix) structurally invalid: no title column in dispatches schema."

- [ ] A-infra-3 Verify abi_compat promises not violated after migration 007:
  ```bash
  python3 aria-orchestrator/docs/validate-m6-handoff.py --check-abi-compat
  ```
  Must exit 0 (audit trigger promises intact after migration). If exit non-zero: investigate
  before proceeding — migration 007 must not contain `DROP TRIGGER`.

---

## TG-A-uptime — Nomad alloc uptime gate + probe structure (~3h)

<!-- R1-T2-5 fix: A-uptime-1 rewritten to use alloc.CreateTime (alloc-level, does not reset
     on task restart) + persist Day-1 anchor file. TaskStates['aria-layer1']['StartedAt']
     removed — resets on task restart, causes false-FAIL on legitimate 168h alloc.
     (R1 audit 2026-05-24) -->
- [ ] A-uptime-1 Create probe directory and alloc anchor file structure:
  ```bash
  mkdir -p .aria/probes/
  ```
  **Day-1 owner action**: record alloc anchor at Day-1 run start:
  ```bash
  nomad alloc status <ALLOC_ID> -json \
    | jq -c '{alloc_id: .ID, create_time_ns: .CreateTime}' \
    > .aria/probes/m6-7d-day-1-alloc-anchor.json
  ```
  Implement `check-m6-e2e-acceptance.py --tg-a --check-uptime` sub-check:
  - Read anchor from `.aria/probes/m6-7d-day-1-alloc-anchor.json` (exit 2 if file absent).
  - Query current alloc state via `subprocess`:
    ```python
    result = subprocess.run(
        ['nomad', 'alloc', 'status', anchored_alloc_id, '-json'],
        capture_output=True,   # per [[feedback_secrets_never_in_conversation]] pattern
        text=True, timeout=30
    )
    data = json.loads(result.stdout)
    current_alloc_id = data['ID']
    create_time_ns = data['CreateTime']   # nanoseconds since Unix epoch
    ```
  - Identity check: if `current_alloc_id != anchored_alloc_id` → `[FAIL] AC-1: alloc replaced`.
    Exit 1.
  - Compute uptime: `now_ns = time.time_ns(); uptime_s = (now_ns - create_time_ns) / 1e9`.
  - PASS condition: `uptime_s >= 604800` (168h × 3600s).
  - Emit `[PASS] AC-1: alloc uptime >= 168h (actual: <N.N>h, alloc_id=<id>)` or
    `[FAIL] AC-1: uptime <N.N>h < 168h`.
  - Exit code 1 on FAIL; exit code 2 if anchor file missing or Nomad CLI unavailable.

  REPO_ROOT pattern:
  ```python
  HERE = Path(__file__).resolve().parent    # → aria-orchestrator/acceptance/
  REPO_ROOT = HERE.parent                   # → aria-orchestrator/
  ```

- [ ] A-uptime-2 Create daily probe snapshot template. Implement a probe helper function
  `write_probe_snapshot(day_n, alloc_data, dispatch_summary)` that writes
  `.aria/probes/m6-7d-day-{N}.md` with the structure defined in proposal §A.3.
  - Day-1 probe must include the alloc anchor section (Alloc ID + CreateTime_ns + CreateTime human).
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

<!-- R1-T2-5 fix: Unit tests updated to use CreateTime-based uptime + alloc ID identity check.
     (R1 audit 2026-05-24) -->
- [ ] A-uptime-4 Unit test: `check-uptime` sub-check —
  - Fixture with same alloc_id + `uptime_s = 604800` (exactly 168h) → PASS (boundary is >=).
  - Fixture with same alloc_id + `uptime_s = 604799` (1s short) → FAIL with uptime message.
  - Fixture with **different** current alloc_id vs anchored alloc_id → FAIL with "alloc replaced" message.
  - Missing anchor file → exit 2.

- [ ] A-uptime-5 Unit test: Day-3 health gate — fixture with `has_s9=True, s_fail_rate=0.40, stuck=0`
  → PASS. Fixture with `has_s9=False` → FAIL reason contains "S0→S9". Fixture with
  `s_fail_rate=0.51` → FAIL reason contains "S_FAIL rate". Fixture with `stuck=1` → FAIL.
  Additionally: verify Day-3 acceptance check reads all 3 individual condition lines (not just
  verdict) per proposal §A.4 (I2-1 fix).

---

## TG-A-dispatch — Dispatch tracker + stratification + pre-flight (~3.5h)

<!-- R1-T2-1 fix: SQL queries rewritten — `final_state`/`created_at`/`issue_type` do not exist.
     Use `state='S9_CLOSE'`, `state_entered_at`, and dispatch_audit_log json_extract.
     (R1 audit 2026-05-24) -->
<!-- R1-T2-4 fix: Mechanism B reference removed (title column doesn't exist). (R1 audit 2026-05-24) -->
<!-- R1-T2-6 fix: Check order fixed — assert total >= 10 FIRST before any division.
     Division guarded: `synth_count / total_s9 if total_s9 > 0 else 0.0`. (R1 audit 2026-05-24) -->

- [ ] A-dispatch-1 Implement dispatch stratification SQL query in acceptance script
  (proposal §A.2, `--tg-a --check-dispatch`):
  ```python
  HERE = Path(__file__).resolve().parent    # → aria-orchestrator/acceptance/
  REPO_ROOT = HERE.parent                   # → aria-orchestrator/
  db_path = REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/aria_layer1.db"
  ```
  Query (uses live column names — `state='S9_CLOSE'`, `state_entered_at`):
  ```sql
  -- Total S9_CLOSE completed in 7d window (STEP 1 — run first before any division)
  SELECT COUNT(*) FROM dispatches
  WHERE state = 'S9_CLOSE'
  AND state_entered_at BETWEEN :start AND :end;
  ```
  Assert result >= 10 **FIRST** (before any synthetic cap calculation). Emit
  `[FAIL] AC-2: total S9_CLOSE dispatches N < 10` and exit 1 if not met.

  NOTE: SQL uses `provider_cost_model` filter only when filtering by provider type, not `provider`
  (schema column SoT: no `provider` column on dispatches table).

- [ ] A-dispatch-2 Implement synthetic cap check (STEP 2 — after total >= 10 confirmed):
  ```sql
  SELECT
    SUM(CASE WHEN is_synthetic=1 THEN 1 ELSE 0 END) as synth_count,
    COUNT(*) as total
  FROM dispatches
  WHERE state='S9_CLOSE'
  AND state_entered_at BETWEEN :start AND :end;
  ```
  Division guarded: `synth_ratio = synth_count / total_s9 if total_s9 > 0 else 0.0`.
  Assert `synth_ratio <= 0.70`. Emit `[FAIL] AC-2: synthetic ratio N/M > 70%` if exceeded.
  (Mechanism B title-prefix approach is NOT valid — `dispatches` has no `title` column.)

- [ ] A-dispatch-3 Implement stratification check per required issue types (STEP 3):
  Issue type is stored in `dispatch_audit_log.payload_json`, NOT in `dispatches` columns.
  At Phase B kickoff, verify the exact `json_extract` key against live data (see T-validate-schema-1).
  For each type_hint in `('bug', 'feature', 'stale')`:
  ```sql
  SELECT COUNT(DISTINCT d.dispatch_id)
  FROM dispatches d
  JOIN dispatch_audit_log al ON al.dispatch_id = d.dispatch_id
  WHERE d.state = 'S9_CLOSE'
  AND d.state_entered_at BETWEEN :start AND :end
  AND json_extract(al.payload_json, '$.issue_type_hint') = :type_hint;
  ```
  Assert result >= 1 per type. Emit `[FAIL] AC-2: no completed <type> dispatch in 7d window`.

- [ ] A-dispatch-4 Unit test: in-memory SQLite with schema.sql applied + 10 S9_CLOSE dispatches
  (verified via dispatch_audit_log with issue_type_hint payloads: 3 bug, 4 feature, 3 stale,
  7 is_synthetic=1, 3 is_synthetic=0) → AC-2 PASS.
  - Fixture with 9 total → FAIL (< 10). Exit 1 with total message.
  - Fixture with 8 is_synthetic=1 out of 10 (>70%) → FAIL with ratio message.
  - Fixture with 0 stale dispatch_audit_log entries → FAIL with stale message.
  - Fixture with total=0 → FAIL with total message (NOT ZeroDivisionError).

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

<!-- R1-T2-1 fix: A-dispatch-6 query rewritten — `project_name` and `final_state` do not exist
     in dispatches schema. Cross-project evidence is detected via dispatch_audit_log payload_json
     or issue_id prefix convention (Phase B implementer must verify via T-validate-schema-1 live
     probe which payload field carries project context). (R1 audit 2026-05-24) -->
- [ ] A-dispatch-6 Implement cross-project conditional acceptance (P-9):
  In acceptance script, check dispatches for cross-project evidence via `dispatch_audit_log`:
  ```sql
  SELECT d.dispatch_id,
         json_extract(al.payload_json, '$.project') as project
  FROM dispatches d
  JOIN dispatch_audit_log al ON al.dispatch_id = d.dispatch_id
  WHERE d.state = 'S9_CLOSE'
  AND d.state_entered_at BETWEEN :start AND :end
  AND json_extract(al.payload_json, '$.project') IS NOT NULL
  AND json_extract(al.payload_json, '$.project') != 'Aria'
  LIMIT 1;
  ```
  NOTE: The exact payload key for project context must be verified at Phase B via live data
  probe (T-validate-schema-1). The query above uses `$.project` as a placeholder.
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

  <!-- R1-T2-4 fix: migration number updated to 006; Mechanism B removed. (R1 audit 2026-05-24) -->
  - **Test 1** — schema.sql still contains triggers after migration 007:
    ```python
    def test_audit_triggers_survive_migration_006():
        schema = (REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/schema.sql").read_text()
        assert "audit_no_update" in schema
        assert "audit_no_delete" in schema
    ```
  - **Test 2** — migration 007 does NOT contain DROP TRIGGER:
    ```python
    def test_migration_006_no_drop_trigger():
        m007 = REPO_ROOT / "hermes-extensions/aria-layer1/migrations/007_schema_v4.3_add_is_synthetic.sql"
        assert m007.exists(), "Migration 007 must exist (Mechanism A is locked)"
        content = m007.read_text()
        assert "DROP TRIGGER" not in content, "Migration 007 must not drop audit triggers"
    ```
  - **Test 3** — validate-m6-handoff.py --check-abi-compat exits 0 after 006:
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

## TG-B — Crash-recovery coverage matrix + state-machine determinism (~2-3h) [REWORKED per #138]

<!-- TG-B Phase A rework 2026-06-01 (Forgejo 10CG/Aria #138): the original TG-B-scaffold/
     infra/llm/statemachine tasks referenced fictional mock symbols (hermes_client /
     layer2_client / recovery.py / ProcessKilledError / AllocTerminatedError — none exist;
     aria-layer1 is a Hermes PLUGIN, not a client calling Hermes) AND an incorrect
     "everything → S_FAIL" recovery model. The real architecture uses three models
     (auto-resume / WAL durability / S_FAIL), and all six PRD §634 crash modes are already
     covered by existing M2/M3 tests. This block is reworked to a coverage matrix + the one
     genuine gap + a re-scoped determinism task. Re-estimate ~13h → ~2-3h. Full rationale:
     openspec/changes/aria-2.0-m6-e2e-resilience/tgb-rework-analysis.md -->

- [x] B-matrix-1 Author `aria-orchestrator/docs/crash-recovery-coverage-matrix.md` mapping the
  six PRD §634 crash modes to (a) their correct recovery model (auto-resume / WAL durability /
  S_FAIL) and (b) the authoritative existing tests. Replaces the fictional 6-mode/9-file suite
  + FakeClock + mock-layer-rationale doc. **Done** (this Spec). The matrix is the AC-3 evidence
  artifact cited by Spec #4 release-closeout.

  Recovery-model corrections (load-bearing — the as-written §B got these wrong):
  - Infra-1 (process/Hermes SIGKILL) → **auto-resume from DB** (NOT S_FAIL). Existing:
    `test_t12_crash_recovery_s5_await_auto_resume` + `test_kill_minus_9_releases_advisory_lock`
    + `test_t7_crash_recovery.py`.
  - Infra-2 (Layer-2 alloc SIGKILL) → **S_FAIL** (correct). Existing:
    `test_t2_alloc_status_provider.py` (ExitCode 137 = SIGKILL) + S5_AWAIT routing (T6.2).
  - Infra-3 (WAL A/B/C/D) → **durability/auto-recover** (NOT S_FAIL for A/B/C). Existing:
    `test_t22_t23_orm_wal.py::test_57`.
  - LLM-4/5/6 → **S_FAIL(PROVIDER_5XX)** (correct; the invented `rate_limit_exhausted`/`HTTP_429`
    structured events do not exist). Existing: `test_t9_provider_router.py` + B-llm-1 below.

- [x] B-llm-1 Close the one genuinely-uncovered branch: the LLM handlers'
  `except Exception → S_FAIL(PROVIDER_5XX)` path for a **non-timeout** provider error
  (`TimeoutError → S_FAIL(TIMEOUT)` was already covered by
  `test_state_machine_skeleton.py::test_15d`). **Done**:
  `tests/test_crash_llm_provider_error_s_fail.py` (5 tests) drives `_handle_s2_decide` /
  `_handle_s3_build_cmd` with the REAL production exception classes (mock-shape discipline):
  `LLMRouteExhausted(chain)` / `_LLMHTTPError(429)` / `ZhipuHTTPError(503)`. 869 tests green.

- [ ] B-sm-1 State-machine **deterministic-transition** coverage (re-scoped per owner 2026-06-01:
  deterministic transition table only, NOT 100% line coverage of the 4500-line `extension.py`).
  For each deterministic state (S0_IDLE / S1_SCAN / S4_LAUNCH / S5_AWAIT / S7_HUMAN_GATE /
  S8_MERGE / S9_CLOSE / S_FAIL): assert normal outbound transition + failure-injected outbound
  transition + re-entry idempotency. Reuse `MockClock` (`aria_layer1/interfaces.py`) — the
  existing AdvancingClock DI; do NOT introduce a new `FakeClock`, and do NOT create
  `state_machine.py` (logic is distributed across extension/comment_poll/reconciler/tick_runner).
  Survey existing coverage first (`test_state_machine_skeleton.py` + `test_t12` already cover
  much of this) and add only the missing deterministic transitions. No `--cov-fail-under=100`.

- [ ] B-matrix-2 Cross-check: confirm every test referenced in the matrix exists and passes
  (`python3 -m unittest discover -s tests`). Any matrix reference that does not resolve to a real
  passing test is a matrix bug (drift guard — the failure mode this whole rework corrects).



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

<!-- R1-T2-4 fix: AD-M6-4 no longer deferred — locked to Mechanism A at R1 audit. Mechanism B
     removed. AD-M6-4b new slot for pre-flight routing strategy. (R1 audit 2026-05-24) -->
- [ ] T-docs-1 Add AD-M6-4 decision to `aria-orchestrator/docs/architecture-decisions.md` (LOCKED):
  "is_synthetic tagging mechanism: **Mechanism A — schema column** `is_synthetic INTEGER DEFAULT 0`
  added via migration `007_schema_v4.3_add_is_synthetic.sql` (schema v5.0). Mechanism B (title prefix
  `[DEMO-M6-*]`) was removed at R1 audit 2026-05-24 — `dispatches.title` column does not exist in
  live schema. No Phase B decision required — implementation must use Mechanism A."

- [ ] T-docs-1b Add AD-M6-4b decision stub to `aria-orchestrator/docs/architecture-decisions.md`:
  "Pre-flight routing strategy: default = accept Luxeno subscription billing (cost_usd=0.0 per
  dispatch, bounded zeros acceptable). If metered cost evidence required, override provider_router
  to force Zhipu for 3 pre-flight dispatches. Document actual choice in this slot."

- [ ] T-docs-2 Add AD-M6-5 decision stub: "Pre-flight dispatch fixture provenance: Deferred to
  Phase B. Option A (replay M5 O3 captures) preferred for regression continuity. Document actual
  provenance in `.aria/probes/m6-preflight-provenance.md` during Phase B kickoff."

<!-- R1-T2-2 fix: AD-M6-6 updated to reference 4-module distribution (no state_machine.py).
     (R1 audit 2026-05-24) -->
- [ ] T-docs-3 Add AD-M6-6 decision: "AdvancingClock DI injection point: clock injected at handler
  class constructor level across 4 modules (extension.py, comment_poll.py, reconciler.py,
  tick_runner.py). `aria_layer1/state_machine.py` does NOT exist (Q1 lock 2026-05-24). All
  `datetime.now()` calls in those 4 modules replaced with `self._clock.now()`. `RealClock` is the
  default (no behavior change in production)."

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
| P-7: is_synthetic tagging mechanism (Mech A LOCKED — migration 007; Mech B removed R1 audit) | DEC §4 P-7 | §What A.2 (P-7 block) | T-validate-schema-1 + A-infra-2 + AD-M6-4 |
| P-8: Pre-flight dispatch fixture provenance (Option A/B/C) | DEC §4 P-8 | §What A.5 (P-8 block) | A-dispatch-5 + AD-M6-5 |
| P-9: Cross-project Kairos/silknode acceptance conditions | DEC §4 P-9 | §What A.6 (P-9 block) | A-dispatch-6 |
| Q-NEW-1: Hybrid mock layer +1h scope | Owner Q-NEW-1 2026-05-24 | §What B.1 (hybrid table) + §Effort baseline | B-scaffold-1 + mock-layer-per-mode rationale doc |
| AD-M6-6: AdvancingClock DI at constructor | §How AD table | §What B.3 (FakeClock class) | B-scaffold-3, B-sm-1 |

---

## Status

**Approved (Phase A.2 CONVERGED 2026-05-24 via R3 stability check; ready for Phase A.3 → Phase B.1)** — Phase B kickoff gated on Spec #1 AC-7 3-day rolling data precondition (wait until ≥3 daily cron snapshots exist post Spec #1 Phase C.2 merge + cron deploy).

**Phase A trajectory** (synced from proposal.md, Status drift corrected 2026-05-26):
- A.1 Draft 2026-05-24 (commit predecessor batch leading to `c29a800`/`413dd75`)
- A.2 R1 NEEDS_FIX 4/4 (4-agent: tl + qa + ai + cr); 12C + 20I de-duped
- R1-fix applied 2026-05-24 (backend-architect agent): T2-1 SQL columns + T2-2 state_machine→4-module + T2-3 AC-6 Luxeno=0 paper-fix + T2-4 Mech B removed + T2-5 AC-1 CreateTime uptime + T2-6 check order + X-T3 mean→median + I2-1..I2-8
- A.2 R2 challenge (3-agent: cr + ai + tl-critic): SCOPE_OK_R2
- A.2 R2-fix applied
- A.2 R3 stability: R3_STABLE → **CONVERGED Approved** (commit `413dd75` 2026-05-24)
- A.3 agent allocation: frontmatter line 8 declares per-task-group (backend-architect TG-A + qa-engineer TG-B + knowledge-manager TG-C) — A.3 lock implicit via frontmatter
- B.1 branch creation: deferred until Spec #1 Phase B.2 implements + deploys snapshot cron (3-day data accumulation precondition)
