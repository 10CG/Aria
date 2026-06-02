# TG-B Rework Analysis (Phase A) — reconcile 6-mode crash taxonomy with reality

> **Trigger**: Forgejo [10CG/Aria #138](https://forgejo.10cg.pub/10CG/Aria/issues/138) — TG-B-infra mock surface is fictional + duplicates existing M2/M3 crash-recovery coverage.
> **Author**: TG-B Phase A rework, 2026-06-01 (dev-claude)
> **Status**: Analysis — owner decision required before spec revision (does NOT yet amend proposal.md/tasks.md).
> **Method**: full code+test recon of `aria-orchestrator/hermes-extensions/aria-layer1` on `feature/aria-2.0-m6-e2e-resilience-tg-a`.

---

## 1. The two errors in the as-written TG-B

**Error A — fictional mock surface** (already in #138): `hermes_client` / `layer2_client` /
`recovery.py` / `ProcessKilledError` / `AllocTerminatedError` do not exist. aria-layer1 is a
**Hermes plugin** (`TickHandler`, `hermes_agent.plugins` entry-point) — it does NOT call Hermes,
so "mock `hermes_client.dispatch()`" is architecturally inverted.

**Error B — wrong recovery model** (deeper): TG-B asserts every crash mode routes to **S_FAIL**.
The real M2/M3 architecture uses **three distinct** recovery models, and "everything → S_FAIL" is
wrong for two of the three:

| Recovery model | Applies to | Real behaviour |
|----------------|-----------|----------------|
| **auto-resume from DB** | process/Hermes kill mid-transition | a fresh extension instance resumes the dispatch row from DB state (heartbeat advancement); advisory lock is released so the next tick re-acquires. NOT S_FAIL. |
| **durability / auto-recover** | WAL faults (committed data) | committed data survives a clean-close crash via WAL; SQLite auto-recovers. NOT S_FAIL. **Caveat (R2)**: this covers *durability*, not *truncation/corruption recovery* — PRD §634 (a)/(b) WAL-truncation + integrity_check-refuse-startup is a separate, unimplemented+untested gap (see §2 Infra-3). The original A/B/C→S_FAIL was not "wrong" so much as *aspirational* (it described a `recovery.py` that never existed). |
| **S_FAIL terminal sink** | LLM provider errors, dead/killed Layer-2 alloc | genuine unrecoverable failures route to S_FAIL. CORRECT. |

---

## 2. 6-mode × existing coverage × correction (the map)

| M6 mode | Real mechanism | Existing M2/M3 coverage | M6's model | Verdict |
|---------|---------------|-------------------------|-----------|---------|
| **Infra-1** Hermes/process SIGKILL mid-transition | crash-restart → **auto-resume from DB** + advisory-lock release | `test_t12_crash_recovery_s5_await_auto_resume` + `test_kill_minus_9_releases_advisory_lock` + `test_second_process_can_acquire_lock_after_kill` + `test_t7_crash_recovery.py` | → S_FAIL ❌ | **model WRONG + already covered.** Real evidence = auto-resume, not S_FAIL. |
| **Infra-2** Layer-2 alloc SIGKILL | alloc `terminated` / `exit_code=137` → `alloc_status_provider` → `_handle_s5_await` routing → S_FAIL(CONTAINER_CRASH) | **routing**: `test_t11_nomad_integration_hardening.py` (exit_code=137 → CONTAINER_CRASH) + `test_state_machine_skeleton::test_s5_alloc_terminated_nonzero_exit_causes_container_crash`. **provider parse**: `test_t2_alloc_status_provider` (ExitCode 137). | → S_FAIL ✅ | **model correct + covered** (R2 fix: routing cited, not just the provider-parse test). |
| **Infra-3** WAL (durability ✅ / truncation-corruption ⚠️) | WAL **durability after clean close** (committed data survives; SQLite auto-recovers) | `test_t22_t23_orm_wal.py::test_57_wal_durability_after_simulated_crash` (clean-close durability) + `test_58` (reader/writer isolation) | A/B/C → S_FAIL ❌; D → recover ✅ | **R2 honesty fix**: durability (clean close) ✅ covered. **PRD §634 (a) WAL-truncation + (b) integrity_check-refuse-startup are NEITHER implemented NOR tested → genuine deferred gap** (no `recovery.py`; test_57 ≠ truncation). The original A/B/C→S_FAIL assumed a `recovery.py` that never existed; the rework drops it but must NOT claim truncation-recovery covered. |
| **LLM-4** 429 rate-limit | provider raises → router classifies `HTTP_429` → degrade-ladder exhaust → `LLMRouteExhausted` → handler `except → S_FAIL(PROVIDER_5XX)` | `test_t9_provider_router.py` (classify + exhaust) + **NEW** `test_crash_llm_provider_error_s_fail.py` (handler S_FAIL) | → S_FAIL + invented `rate_limit_exhausted`/`HTTP_429` events | **model OK (events invented) + now covered.** |
| **LLM-5** invalid JSON | SDK parse error → handler `except → S_FAIL(PROVIDER_5XX)` | **NEW** `test_crash_llm_provider_error_s_fail.py` covers the `except` branch generically (any non-timeout exception) | → S_FAIL + invented event | **covered** (the handler catches JSON parse failure like any exception). |
| **LLM-6** provider 5xx | provider raises → router `HTTP_5XX` → exhaust → handler S_FAIL | `test_t9_provider_router.py` + **NEW** `test_crash_llm_provider_error_s_fail.py` | → S_FAIL + invented event | **covered.** |

**Net**: 5 of the 6 modes are fully exercised by M2/M3 + the new handler tests (`85b8f46` +
R2 `json.JSONDecodeError` test). The genuine previously-uncovered LLM branch (handler
`except Exception → S_FAIL(PROVIDER_5XX)` for non-timeout provider errors incl. malformed JSON) is
closed. **One genuine gap remains (R2 honesty fix)**: Infra-3 WAL **truncation/corruption** recovery
(PRD §634 (a)/(b)) is neither implemented nor tested — durability (clean close) is covered, but
truncation→graceful-S_FAIL needs a real `recovery.py` (out of #138 scope). Surfaced as a deferred
gap in the coverage matrix "Known gaps" section, NOT claimed covered.

---

## 3. What M6 actually adds beyond M2/M3 (the real TG-B value)

M6's resilience goal (PRD §634) is **evidence that the 6 failure modes are handled in a
sustained autonomous run** — not a second copy of M2/M3's unit tests. The crash-mode *unit tests*
the as-written TG-B specifies are **redundant**. M6's genuine contribution is:

1. **A crash-recovery coverage matrix** that maps the 6 PRD §634 modes to the authoritative
   existing tests (the table in §2) — so the release-closeout (Spec #4) can cite "6 modes covered"
   with traceable evidence, instead of a new fictional suite.
2. **The one genuine gap** (LLM non-timeout → S_FAIL) — shipped.
3. **AdvancingClock DI / 100% coverage** (TG-B-statemachine) — re-scoped: `MockClock` already
   exists (`interfaces.py`) and is used pervasively; `datetime.now()` audit + `--cov-fail-under=100`
   on a **~3.5K-line (3543)** `extension.py` is a multi-day effort wildly off the spec's "~4h". This needs
   an explicit scope decision (drop / target a realistic threshold / scope to changed lines).

---

## 4. Recommended revised TG-B scope (for owner approval)

| As-written | Recommended |
|-----------|-------------|
| TG-B-scaffold: 9 fictional test files + FakeClock + rationale doc (~2h) | **DROP** the 9 files + FakeClock (redundant w/ MockClock). Keep a 1-page **crash-recovery coverage matrix doc** (§2 table). |
| TG-B-infra: Infra-1/2/3 against fictional mocks (~4.5h) | **DROP as new tests.** Map to existing `test_t12` / `test_t2_alloc_status_provider` / `test_t22_t23` in the matrix. Correct the recovery model (auto-resume / durability / S_FAIL). |
| TG-B-llm: LLM-4/5/6 9-file split + invented events (~1.5h) | **DONE** via `test_crash_llm_provider_error_s_fail.py` (handler S_FAIL with real exception classes). |
| TG-B-statemachine: AdvancingClock DI + 100% cov of 4 modules (~4h) | **RE-SCOPE** with an explicit owner decision (see §3.3). MockClock already exists; 100% cov of ~3.5K-line (3543) extension.py ≠ 4h. |

**Re-estimate**: TG-B drops from ~13h to **~2–3h** (matrix doc + already-shipped gap + a scoped
coverage decision). Most of the original estimate was for tests that either don't apply or already
exist.

---

## 5. Owner decisions needed

1. **Approve the reframe** (TG-B = coverage matrix + shipped gap, not a new 6-mode suite)? If yes,
   I amend `proposal.md` §B + `tasks.md` TG-B-* accordingly and run a focused post_spec audit.
2. **TG-B-statemachine scope** (§3.3): (a) drop 100%-cov goal, (b) realistic threshold (e.g. cover
   the deterministic transition table only), or (c) changed-lines coverage? The "~3.5K-line (3543) file →
   100%" target is not viable as specified.
3. Whether the recovery-model correction (auto-resume/durability ≠ S_FAIL) also needs a note in
   `architecture-decisions.md` (it's a load-bearing semantic the spec got wrong).

---

## Cross-references
- Defect: [10CG/Aria #138](https://forgejo.10cg.pub/10CG/Aria/issues/138)
- Shipped gap: `aria-orchestrator` `85b8f46` `tests/test_crash_llm_provider_error_s_fail.py`
- Authoritative existing tests: `test_t12_reconciler_crash_recovery_integration.py` /
  `test_t7_crash_recovery.py` / `test_t2_alloc_status_provider.py` / `test_t22_t23_orm_wal.py` /
  `test_t9_provider_router.py`
