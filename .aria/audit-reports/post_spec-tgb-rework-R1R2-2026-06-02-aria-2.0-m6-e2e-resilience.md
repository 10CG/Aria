---
checkpoint: post_spec (focused, TG-B rework per #138)
spec: aria-2.0-m6-e2e-resilience
mode: convergence
verdict: CONVERGED (PASS_WITH_WARNINGS)
rounds: 2
agents: [tech-lead-critic, qa-engineer, code-reviewer]
timestamp: 2026-06-02T05:00:00Z
---

# post_spec focused audit — M6 e2e-resilience TG-B rework (#138)

**Scope**: the TG-B Phase A rework only (proposal §B REWORK NOTE + AC-3 + AC-4 + tasks.md TG-B
block + crash-recovery-coverage-matrix.md + tgb-rework-analysis.md + the 2 new tests). NOT the
full Spec.

## R1 (3-agent, 2026-06-02)

| agent | verdict | critical |
|-------|---------|----------|
| tech-lead-critic | NEEDS_FIX | 3 |
| qa-engineer | PASS_WITH_WARNINGS | 0 |
| code-reviewer | PASS_WITH_WARNINGS | 0 |

**SPLIT** — convergent findings across agents (strong signal):

- **C1** (tl + cr + qa I-4): AC-4 not reworked — still demanded `--cov-fail-under=100` + two
  nonexistent test files (`test_state_machine_deterministic.py` / `test_state_machine_stochastic_replay.py`),
  contradicting the B-sm-1 re-scope. **Verified** against proposal.md.
- **C2** (tl + cr + qa m-2): AC-3 retained a leftover `m6-wal-fault.sh` hard requirement that the
  rework dropped (recovery.py doesn't exist). **Verified** (edit-boundary leftover).
- **C3** (tl + qa I-2): Infra-3 WAL over-claim — matrix marked `test_57` as covering Infra-3, but
  test_57 tests clean-close durability, NOT PRD §634 (a) WAL-truncation + (b) integrity_check-refuse-
  startup; corruption→S_FAIL is genuinely unimplemented + untested. **Verified** (`grep integrity_check`
  → none in aria_layer1/).
- **I1** (tl + qa): Infra-2 matrix cited the provider-parse test, not the real routing test
  (`test_t11_nomad_integration_hardening.py:220` exit 137 → CONTAINER_CRASH). **Verified**.
- **I2** (tl): Infra-1 "never S_FAIL" over-absolutized (reconciler can FAIL a stuck row).
- Minor: extension.py "4500 lines" fabricated (real 3543); short `::test_57` nodeid; LLM-5 untested.

All findings independently verified against real code before fixing (verify-first, not blind-trust).

## Rev1 (fixes, 2026-06-02)

- **C1**: AC-4 rewritten → references `test_transition_table_determinism.py` (drift-guard), removed
  `--cov-fail-under=100` + phantom files + REWORK NOTE.
- **C2**: removed the `m6-wal-fault.sh` block from AC-3; added `test_t11` + `test_transition_table_determinism`
  to the AC-3 command.
- **C3**: matrix Infra-3 row + new "Known gaps" section + AC-3 Infra-3 note + analysis §2 + §B
  REWORK NOTE all corrected to honestly state durability-covered / truncation-corruption-deferred-gap.
- **I1**: matrix + tasks.md + analysis cite `test_t11` routing (authoritative), parser test as supporting.
- **I2**: Infra-1 claims scoped to the kill-recovery path (not a blanket reconciler claim).
- **LLM-5** (qa I-3): added `test_json_decode_error_to_sfail` (real `json.JSONDecodeError`) — direct
  coverage replacing transitive-logic claim.
- Minor: 4500→~3.5K (3543) across 5 files; full nodeids; `[SUPERSEDED]` tags on §B.2/B.3/B.4.

Verification: 880 tests green (+1 json); AC-3 reworked command 98 tests OK; AC-4 command 10 tests OK.

## R2 (tech-lead-critic re-verify, 2026-06-02)

**verdict: PASS_WITH_WARNINGS, 0 Critical, 0 new Critical.**

- C1 / C2 / C3 / I1 / I2 — **all CLOSED** (verified against fixed files + live test runs).
- 0 new Critical introduced by Rev1.
- 1 residual warning (doc hygiene, non-blocking): superseded §B.2/B.3/B.4 headers lacked inline
  `[SUPERSEDED]` tags → **fixed in Rev1.1** (all 4 B.x headers now tagged).

## Convergence

R1 SPLIT (1 NEEDS_FIX, 3 Critical) → Rev1 (all Critical + Important closed) → R2 PASS_WITH_WARNINGS
(0 Critical, 0 new Critical). **CONVERGED** — substantive (dissenting agent's Criticals all closed,
verdict improved NEEDS_FIX→PASS_WITH_WARNINGS, no oscillation), L2 2-round baseline.

**Net value of the audit**: caught that the rework corrected §B/tasks/matrix but left the downstream
acceptance contract (AC-3/AC-4) describing the rejected design, AND that the Infra-3 WAL coverage was
over-claimed (truncation/corruption recovery is a genuine deferred gap, now surfaced not papered over).
The reframe's core architectural claims (auto-resume / alloc-kill→S_FAIL / LLM→S_FAIL) were verified
correct.
