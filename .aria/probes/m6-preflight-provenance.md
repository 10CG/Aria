# M6 Pre-flight provenance (TG-A A-dispatch-5 / AD-M6-5)

> Owner fills this at Phase B kickoff, BEFORE the 7-day clock starts.
> Decides which of the 3 pre-flight dispatch fixtures (proposal §A.5, AD-M6-5) to use.

Selected option: [A|B|C]      <!-- A = replay M5 O3 / B = fresh synthetic / C = cross-project -->
Rationale: ...

Fixture source: [path or "fresh synthetic [DEMO-M6-P*]" or "cross-project Kairos/SilkNode issue"]

## Option reference (per proposal §A.5)
- **A — Replay M5 O3 captures** (preferred for regression continuity): re-dispatch the
  DEMO-M5-O3 payload if `aria-orchestrator/docs/demo-m5-o3-*.yaml` capture files exist.
- **B — Fresh synthetic issues**: 3 `[DEMO-M6-P*]`-prefixed issues on the Aria Forgejo repo,
  closed/labelled after pre-flight (kept out of the 7d dispatch pool).
- **C — Cross-project**: ≥1 real Kairos/SilkNode issue if cross-project dispatch is operational
  (P-9 conditions met).

## Hard cost cap
Each pre-flight dispatch ≤ $2.00; total ≤ $6.00 for all 3. Record per-dispatch cost in
`m6-preflight-log.md` (graded by `check-m6-e2e-acceptance.py --tg-a --check-preflight`).
