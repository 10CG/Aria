# M5 T-deploy Phase A — Production snapshot record

> **Created**: 2026-05-20 ~05:55 UTC
> **Authority**: Phase A.2/A.3/A.4 of v2 playbook
> **No prod mutation** (snapshot/backup only)

---

## A.2 — `dispatches.db` snapshot ✅

**Snapshot path** (on light-1):
```
/tmp/aria-layer1-snapshot-20260520T055525/dispatches.db.pre-m5
```

**Source**:
```
/opt/aether-volumes/aria-layer1/data/dispatches.db   77824 bytes (May 9 17:21)
```

**Integrity verification** (via Python `sqlite3.connect.PRAGMA integrity_check`):
- integrity: **ok**
- row count: **16** ✅ (matches investigation)
- schema_version: **3.0** ✅ (M4 era)
- tables: `dispatches`, `migration_notes`, `schema_meta`

**Snapshot retention**: snapshot in `/tmp/` — may be reaped on host reboot. **Recommend cp to `/opt/aether-volumes/aria-layer1/backups/` post-Phase-A.5 sign-off** (durable path mounted by Nomad volume).

---

## A.2-supplement — 16 production dispatches (post-migration zero-loss verification)

**Issue IDs** (sorted):
```
705
715
716
717
718
719
720
721
722
723
724
811
821
838
839
smoke-m4-pr97
```

**State distribution**:
- `S9_CLOSE`: 1 (issue_id 705 likely — the one successful close)
- `S_FAIL`: 15

**Migration history recorded in DB**:
- `002.provider_cost_model_backfill` (M3 era, 2026-05-09)
- `002.cycle_start_ts_terminal_backfill` (M3 era)
- `003.human_gate_columns_backfill` (M4 era — 7 cols additive: human_decision / decision_at / reject_reason / human_gate_entered_at / forgejo_approval_comment_id / risk_tier_stub / last_polled_comment_id)

**Schema v3.0 metadata**:
- created_at: 2026-05-02T19:17:39Z
- `fallback_chain_outcome_enum`: `["ok","http_5xx","http_429","http_4xx","timeout","network_error","quality_degrade"]`
- `fail_reason_v3_additions`: `["human_reject","human_timeout"]`

**Expected migrations to apply (Phase B Step 5)**:
- 004: v3.0 → v4.0
- 005: v4.0 → v4.1
- 006: v4.1 → v4.2 (Spec Y T0 `spec_id` column)

**Post-migration verification target**:
- row count remains 16
- All 16 `issue_id` values preserved
- 15 `S_FAIL` + 1 `S9_CLOSE` preserved
- new columns (spec_id + Spec Y additions) populated per migration logic, not corrupting existing rows
- `migration_notes` table records new entries for 004/005/006

---

## A.2 column inventory (34 columns — current v3.0 baseline)

`issue_id`, `dispatch_id`, `attempt_count`, `state`, `state_entered_at`, `last_heartbeat_at`, `prompt_path`, `image_sha`, `alloc_id`, `notification_status`, `pr_id`, `fail_reason`, `fail_detail`, `failed_from_state`, `token_usage_input`, `token_usage_output`, `token_cost_usd`, `model_used`, `fallback_triggered`, `fallback_chain_json`, `retry_count`, `cycle_start_ts`, `cycle_end_ts`, `dispatched_job_id`, `eval_id`, `provider_cost_model`, `attempt_history_json`, `human_decision`, `decision_at`, `reject_reason`, `human_gate_entered_at`, `forgejo_approval_comment_id`, `risk_tier_stub`, `last_polled_comment_id`

(Note: `risk_tier_stub` is M5 ABI commitment — migrations ADD `risk_tier` separately + UPDATE backfill; NO DROP of `risk_tier_stub`)

---

## A.3 — Git backup branch ✅

**Backup branch** (on light-1 `/root/Aria`):
```
backup/pre-m5-upgrade-20260520T055622   →   e416920 feat(m2): bump aria-orchestrator + tasks.md/proposal.md — T7.5 HTTP dispatch + AD-M2-9
```

**`git stash`**: skipped — default stash doesn't pick up submodule pointer-only changes. M aria-orchestrator preserved in working tree; OD-1 (a) Reset will discard during Phase B Step 1.

**State at backup time**:
- Current branch: `feature/aria-2.0-m2-layer1-state-machine` (13 behind origin/feature, 258 behind origin/master)
- HEAD: `e416920` feat(m2): T7.5 HTTP dispatch + AD-M2-9
- Parent index (gitlinks):
  - `aria-orchestrator` @ `e0cc6de3a2049d434e408020233628b35d9c9498` (M2 expected)
  - `aria` @ `7e11e6a7c30dbc755aade5e19565ed0c0951e631` (v1.17.7)
  - `standards` @ `5b56dd4616105a6f59f3a2ebd45411cfcf820591`
- **Uncommitted M aria-orchestrator** → working tree at `54679910de6b3c06d8ee5fc9d611493c122c51f4` (M3 era "fix(feishu): _compute_feishu_signature key/msg swap")

**Rollback path** (if Phase B fails catastrophically):
1. `git -C /root/Aria checkout backup/pre-m5-upgrade-20260520T055622` → returns to e416920
2. `git -C /root/Aria submodule update --init --recursive` → restores e0cc6de / 7e11e6a / 5b56dd4
3. Restore `dispatches.db` from snapshot `/tmp/aria-layer1-snapshot-20260520T055525/dispatches.db.pre-m5`
4. `nomad job stop aria-layer1-reconcile aria-layer1-cron` (if deployed during Phase B)
5. `nomad job restart aria-orchestrator` to revert to old aria-layer1 v0.2.0 editable install (will re-pip-install from rolled-back source)

## A.4 — Nomad job inspect (next step)

Will record TaskGroup structure (Rule #7 scrubbed) once executed.

---

**Status**: A.2 + A.3 + A.4 done. A.5 sign-off pending.

---

## A.4 — Nomad job inspect ✅

Live spec captured in `.aria/notes/prod-job-spec-live-2026-05-20.md` (Rule #7 hygiene: env keys only, no values; template DestPath only, no body).

Headline:
- Driver: **`raw_exec`** (NOT docker)
- Command: `/opt/aria-orchestrator/venv/bin/hermes gateway run`
- 16 env keys, 0 secret-likely
- Hermes state at **`/root/.hermes/`** (active, last write 2026-05-20 06:06)
- `/opt/aria-orchestrator/hermes-data/` mount is dev-source HCL docker-era artifact, **not applicable to prod raw_exec**

## A.6 — Hermes plugin opt-out verification (OD-3 i resolution)

**M5 source v0.4.0** (`aria_layer1/__init__.py:60-70`):
- `on_session_start` hook is **explicit no-op** for hermes_cli VALID_HOOKS contract
- Comment line 46-52: AD-M2-7 / 2026-05-02 M2 deploy pivot → cron scheduling owned by Nomad periodic job (`deploy/aria-layer1-cron.nomad.hcl`), hermes cron CLI only accepts LLM prompts/skills
- `extension.py:402+ register_cron()` function still exists but is **not called** from `__init__.register()`. Dead code (or kept for future skill-based integration).

**Prod current state** (live `/root/.hermes/cron/jobs.json`):
- Only **1 active cron**: `aria-heartbeat` (id `48ed7e826bc3`, 995 completions, last ok 05:42)
  - Runs `./scan.sh /opt/aria-orchestrator/app --json` via skill `heartbeat-scan` every 60min
  - Delivers to feishu
  - **NOT aria-layer1** — this is M0/M1-era heartbeat-scan, orthogonal to Layer 1 state machine
- 7 other cron output dirs (Apr 7-8 dated) are dead cron jobs from initial setup; safe to ignore (no entries in jobs.json)
- **aria_layer1_tick is NOT registered** in jobs.json — v0.2.0 prod never registered hermes-internal cron (extension.py register_cron path wasn't hit)

**Conclusion for OD-2 (b)**:
- ✅ **Zero double-cron risk** for M5 reconcile + cron Nomad jobs
- ✅ v0.4.0 upgrade naturally maintains Pure Nomad pattern (no-op stub)
- ⚠️ **aria-heartbeat is orthogonal active prod tooling** — must NOT delete `/opt/aria-orchestrator/app/` (it runs every 60min)

## A.6-supplement — OD-4 re-classification

**Investigation §2.4 was WRONG**: `/opt/aria-orchestrator/app/` is NOT obsolete. It is **actively used by the aria-heartbeat cron** (running every 60min, 995 successful executions to date).

**Updated OD-4 (a) "Leave alone" rationale**: Active prod tooling — `scan.sh` + skill `heartbeat-scan` registered in /root/.hermes/cron/jobs.json. **DO NOT delete or modify** during M5 deploy. Add to "verified active, do not cleanup" registry (NOT cleanup backlog).

**Action item for future cleanup session** (out of scope today): consolidate aria-heartbeat into the M5 / Layer 1 architecture or formally retire as separate operational tool. Not a M5 deploy blocker.

---

## A.5 — Phase A sign-off checklist (in progress)

- [x] OD-1 (uncommitted M) decision recorded → (a) Reset
- [x] OD-2 (cron architecture) decision recorded → (b) Pure Nomad periodic
- [x] OD-3 (re-defined) decision recorded → (i) Phase A.6 verification → ✅ Pure Nomad is FREE (no aria-layer1 hermes-cron exists, v0.4.0 stub natural)
- [x] OD-4 (app/ obsolete) decision recorded → (a) Leave alone, **reclassified as "active by aria-heartbeat, DO NOT delete"**
- [x] OD-5 (jump strategy) decision recorded → (a) Single big leap + strong backup
- [x] A.2 DB snapshot integrity verified (16 rows preserved)
- [x] A.3 git backup branch created (backup/pre-m5-upgrade-20260520T055622)
- [x] A.4 live Nomad job spec captured (no secrets in file)
- [x] 16 production dispatch IDs noted (705, 715-724, 811, 821, 838, 839, smoke-m4-pr97)
- [x] A.6 Hermes plugin opt-out verified (M5 source v0.4.0 already Pure Nomad)
- [ ] Owner final go/no-go for Phase B
