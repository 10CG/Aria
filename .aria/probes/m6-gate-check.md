# M6 Spec #2 Phase B precondition gate — A-infra-1 record

> Task A-infra-1: verify Spec #1 AC-7 (3-day rolling cost history) PASSES before any TG-A code.

## Verdict: ✅ PASS — Phase B unblocked

## Evidence (authoritative source: light-1 node cron)

The gate command `validate-m6-handoff.py --check-3-day-history` reads cost.json snapshots
that live **node-local on light-1** (`/opt/aether-volumes/aria-layer1/data/cost-snapshots/`,
per Blocker #2 / [[feedback_periodic_job_acceptance_data_on_durable_volume]]). The gate
therefore runs on light-1 via the 2026-05-30 crontab one-shot, not from a local checkout.

- **Gate run**: 2026-06-01T02:30:01Z (automated crontab on light-1)
- **Result**: `3-day rolling history: PASS (3 files, latest 2026-06-01)` — `EXIT=0`
- **Snapshots on node**: `cost-2026-05-30.json` / `cost-2026-05-31.json` / `cost-2026-06-01.json`
- **Recorded in**: `.aria/notes/2026-06-01-m6-phase-b-gate-result.md` (§1)

## Consequence

Spec #1 AC-7 precondition satisfied → M6 Spec #2 (e2e-resilience) Phase B is unblocked.
TG-A-infra (migration 007 + schema guard) + TG-A-validate (abi_compat triple) proceed.

> Note: the 168-hour E2E clock itself (TG-A-uptime/dispatch + pre-flight real dispatches)
> is owner-driven wall-clock and is NOT started by this code slice — it requires the owner
> to record the Day-1 alloc anchor and run pre-flight. This record only confirms the
> Phase-B-start precondition is met.
