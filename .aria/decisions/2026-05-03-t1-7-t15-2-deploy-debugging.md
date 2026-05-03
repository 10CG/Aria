---
id: SESSION-2026-05-03
title: T1.7 deploy + T15.2 E2E partial — 10 latent bugs caught & fixed
date: 2026-05-03
status: session_handoff
relates_to: AD-M2-7 (pip-install Option A), AD-M2-8 (Nomad periodic cron pivot), T1.7, T15.2, T15.3
---

# Session — T1.7 Deploy + T15.2 E2E Dogfood Findings

## TL;DR

Single owner+AI session 2026-05-02 evening → 2026-05-03 afternoon UTC.
Walked T1.7 cluster deploy + T15.2 first issue injection end-to-end on
light-1. State machine **demonstrably advanced 4 states** for issue #62
(Forgejo internal id 705): S0_IDLE → S1_SCAN → S2_DECIDE → S3_BUILD_CMD
before hitting the known T7 NomadDispatchClient stub (NotImplementedError)
at S4_LAUNCH.

10 latent bugs were caught and fixed along the way, all under 247 tests
PASS green. Decision needed: continue T7 production wiring vs accept M2
partial vs treat as M3 carry-over.

## Latent Bug Catalog (10)

| # | Bug | Symptom | Fix | Commit |
|---|---|---|---|---|
| 1 | plugin.yaml `requires_env` 4/6 names mismatched runtime source | onboarding "missing env" false-positive | rename to canonical names from feishu_webhook.py / extension.py | 88dc975 |
| 2 | HCL `nomadVar "aria-orchestrator/secrets"` outside workload identity ACL | template render silent fail at runtime | path → `nomad/jobs/aria-orchestrator` | cdfb7d4 |
| 3 | raw_exec driver does not honor nomad host_volume | alloc 100% fail "task driver does not support host volumes" | drop volume + volume_mount blocks; rely on host fs (drwxrwxrwx pre-created) | 4fbee9b |
| 4 | `_get_repo()` opens sqlite but never executes schema.sql | first list_non_terminal() crashes "no such table: dispatches" | executescript(schema.sql) on connect (idempotent CREATE IF NOT EXISTS) + makedirs | e8bb95f |
| 5 | hermes cron CLI accepts only LLM prompts/skills, not arbitrary `python -m`; on_session_start fires only on first user chat | cron never registered, scheduler silent | pivot to dedicated Nomad periodic job (AD-M2-8); register() now no-ops cron, hermes plugin remains for diagnostics | 7545c87 |
| 6 | tick() Phase 1 scan-and-seed never implemented (T1.4 was incomplete: state handler exists but nothing seeds the initial row) | seeded=0 forever, processed=0 | new _phase1_scan_and_seed: forgejo.list_issues → insert_dispatch_auto → transition S0_IDLE → S1_SCAN | 6eb2a83 |
| 7 | ForgejoCliClient subprocess'd `forgejo` CLI wrapper (dev-box CF Access tool, absent on cluster nodes) | FileNotFoundError on light-1 | rewrite _run as stdlib urllib.request to internal IP (192.168.69.200:3000); FORGEJO_USE_CLI=1 opt-in keeps dev-box path | 271a999 |
| 8 | aria-runner-bot PAT lacked read:issue scope | HTTP 403 "token does not have at least one of required scope(s): [read:issue]" | owner expanded scopes via Forgejo UI (read:issue / write:issue / read:repository) | (owner action) |
| 9 | _handle_s1_scan idempotency filter treated current-row as blocker | row stuck at S1_SCAN forever (count_active=1 was self) | skip filter when candidate_issue_id == ctx row's issue_id (per OD-5a UNIQUE invariant, count==1 + match-self → eligible) | 8647315 |
| 10 | tick_runner constructed AriaLayer1Extension() with no DI args | forgejo=None at runtime; Phase 1 silently skipped | ARIA_LAZY_WIRE=1 env opt-in (set in tick_runner) lazy-creates ForgejoCliClient | 45ad6cc |

## Pivots / Decisions Recorded

- **AD-M2-8** (`.aria/decisions/2026-05-02-ad-m2-8-nomad-periodic-cron-pivot.md`): cron scheduling owned by Nomad periodic job, not hermes cron registry. hermes cron CLI contract is incompatible with arbitrary `python -m` invocations; Layer 1 isn't a hermes skill (would require LLM-prompt wrapping per tick = wasted cost). Hermes plugin remains loaded for diagnostics.

## E2E Trajectory (issue 705)

```
Tick 1 (Phase 1): seed → S1_SCAN, dispatch_id=ccba74aeb0f98885
Tick 2 (initial): no advance (self-row filter bug)
Tick 3 (post fix #9): S1_SCAN → S2_DECIDE (eligible, schema_ok)
Tick 4 (LLM ~12s): S2_DECIDE → S3_BUILD_CMD
Tick 5 (next):    S3_BUILD_CMD → (S4_LAUNCH stub blocked or S_FAIL TBD)
```

DB at handoff time: `('705', 'S3_BUILD_CMD', None, None, None, '2026-05-03T14:51:01...')`

## Remaining Latent (Known)

- **T7 NomadDispatchClient.dispatch is NotImplementedError stub** — S4_LAUNCH will raise. Production HTTP dispatch (POST /v1/job/{id}/dispatch) is ~2-4h work. Tasks.md T7 was marked done but only meta-size guard + prompt rendering + bind mount logic were implemented; HTTP I/O is stubbed.
- **m1-handoff.yaml not at /opt/aether-volumes/aria-layer1/data/** — Phase 1 falls back to sentinel image_sha. T11 image_sha guard would reject the dispatch. Owner can `cp` the handoff into the host volume to fix (1 line).
- **M1 issue validator path hardcoded to /home/dev/Aria/...** (308 dev box, absent on light-1) → fail-soft skip. T1.5 needs path env-configurable or package the validator.

## Test State

- 247 tests PASS (was 239 before T1.7 fixes)
- +8 regression guards added this session:
  - `test_schema_auto_init.py` (3 tests, fix #4)
  - `test_phase1_scan_and_seed.py` (5 tests, fix #6)
- 0 regressions

## Owner Action Items Performed (this session)

1. Created `aria-auto` label on 10CG/Aria (id=27)
2. Set `LUXENO_API_KEY` + `ARIA_FEISHU_WEBHOOK_URL` in `nomad/jobs/aria-orchestrator` (Forgejo UI)
3. Created Feishu group bot webhook (URL stored in #2)
4. `pip install -e` aria-layer1 into `/opt/aria-orchestrator/venv` on light-1
5. `aether dev run aria-orchestrator-light.nomad.hcl` (T1.7 service start)
6. `aether dev run aria-layer1-cron.nomad.hcl` (AD-M2-8 periodic)
7. Expanded `aria-runner-bot` PAT scope (read:issue / write:issue / read:repository)
8. Pulled multiple times on light-1, cleared __pycache__

## Next Session Decision

Three paths (presented to owner end-of-session, awaiting answer):

**A. Stop & checkpoint** (THIS DOCUMENT) — done.

**B. T7 production wiring** — implement NomadDispatchClient HTTP dispatch.
   - Effort: 2-4h
   - Unblocks: S4_LAUNCH and the rest of E2E
   - Risk: each subsequent state (S5/S6/S7/S8) likely has its own latent gaps;
     time to "≥10 dispatch full cycle" probably 6-12h with surprises

**C. M2 partial + M3 carry-over** — accept skeleton-verified scope.
   - Effort: 1h
   - Cost: PRD baseline divergence requires owner re-acknowledgment

## Next Session Entry Point

`aria:state-scanner` will detect:
- Spec aria-2.0-m2-layer1-state-machine still Approved/in_progress
- 247 tests PASS on feature branch
- Recent commits trail: T1.7 deploy fixes (10 commits), AD-M2-8 file present
- This decision file (latest in `.aria/decisions/`)
- m2-handoff.yaml gaps still at `<pending T15>` for metrics

Recommended path: open this file first, then decide A/B/C.

## Session Stats

- Commits to aria-orchestrator: ~10 (88dc975 ... 8647315)
- Commits to main repo: ~10 (3d27a1f ... 4e34849)
- Dual remotes (Forgejo + GitHub): in parity end-of-session
- Test count: 239 → 247 (+8)
- Spec status unchanged: still Approved, Phase B.2 (now ~95% complete instead of 95%-T1.7-blocked)
