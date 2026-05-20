# Aria 2.0 Production State Investigation (light-1) — 2026-05-20

> **Status**: Locked reality snapshot — DO NOT modify, ONLY append
> **Trigger**: O1 (T-deploy) attempt 2026-05-20 ~03:30 UTC was paused after `/opt/aria-orchestrator` turned out to NOT be a git checkout (vs addendum assumption). 7 rounds of safe diagnostic queries revealed prod state is ~211/258 commits behind master with significant architectural drift.
> **Supersedes assumption set in**: `docs/handoff/2026-05-19-m5-deploy-playbook-v11-addendum.md` (the v11 addendum was based on incorrect assumptions; **see `2026-05-20-m5-deploy-playbook-v2-accurate.md`** for the corrected playbook)
> **Authoritative for**: All future deploy / Layer 1 ship / schema migration work on light-1

---

## TL;DR — the gap

| Dimension | addendum v11 assumed | **Production reality (2026-05-20 verified)** |
|-----------|----------------------|----------------------------------------------|
| Source location | `/opt/aria-orchestrator` is git checkout | **Source at `/root/Aria/` instead** (full meta-repo + submodules) |
| `/opt/aria-orchestrator/` contents | git checkout + venv | Only `app/` (Apr 6-8 obsolete artifact) + `venv/` |
| Branch | master | **`feature/aria-2.0-m2-layer1-state-machine`** (M2-era feature, not master) |
| Commits behind master | "some" | **211 commits behind** on /root/Aria; local `master` is 258 behind origin/master |
| Submodule pointer state | clean | **Uncommitted M on `aria-orchestrator` submodule** (bumped from `e0cc6de` M2 → `5467991` M3-era but never committed) |
| aria-layer1 install | `pip install -e` editable | ✅ Editable at `/root/Aria/aria-orchestrator/hermes-extensions/aria-layer1` — but **v0.2.0** (M3 era), not 0.4.0 (M5 era) |
| Database schema | v4.1 (M5 Layer 1 deployed) | **schema v3.0** (M4 era, 16 production dispatches present) |
| Layer 1 Nomad jobs | reconcile + comment-poll + cron all running | **Only `aria-layer1-comment-poll` running** (M4 era); reconcile + cron NOT deployed |
| Architecture pattern | All-Nomad periodic | **Mixed**: Hermes-internal cron (per AD-M2-7, DEPLOYMENT.md) + Nomad periodic for comment-poll (M4 era addition) |
| `/opt/aria-orchestrator/hermes-data/` | Mount target with `cron-jobs.json` etc. | **Does not exist on light-1** ⚠️ |
| `sqlite3` CLI | Available | **Not installed** — must use Python `sqlite3` module instead |

---

## §1 Production layout (verified 2026-05-20)

### Filesystem

```
/root/Aria/                                   ← actual source location
├── .git/modules/aria-orchestrator/           ← submodule
├── aria-orchestrator/                        ← submodule @ 5467991 (heads/master)
│   ├── hermes-extensions/aria-layer1/        ← editable install source
│   │   ├── aria_layer1/                      ← Python package
│   │   ├── pyproject.toml
│   │   ├── plugin.yaml
│   │   └── DEPLOYMENT.md                     ← canonical deploy guide (per AD-M2-7)
│   └── deploy/, nomad/, docker/              ← Nomad HCL + Dockerfile
├── aria/                                     ← submodule @ 7e11e6a (v1.17.7, very old)
└── standards/                                ← submodule @ 5b56dd4

/opt/aria-orchestrator/
├── app/                                      ← Apr 6-8 OBSOLETE ARTIFACT (uid=1000 dev, not used)
│   ├── Dockerfile, README.md
│   ├── config/, deploy/aria-orchestrator.nomad.hcl, schema/, skills/, tools/
│   ├── notify-feishu.sh, scan.sh, setup-cron.sh, requirements.txt
│   └── .aria/heartbeat-scan.json
└── venv/                                     ← Python venv (Python 3.11)
    └── lib/python3.11/site-packages/
        └── aria_layer1 → /root/Aria/aria-orchestrator/hermes-extensions/aria-layer1 (editable v0.2.0)

/opt/aether-volumes/aria-layer1/data/
├── dispatches.db                             ← 77824 bytes, schema v3.0, 16 dispatch rows
└── backups/                                  ← (empty per ls; backup dir exists but no recent backups)
```

### Nomad jobs (running on light-1 via aether status)

| Job | Type | Status | Since | Notes |
|-----|------|--------|-------|-------|
| `aria-build` | service | running | 2026-04-19 | Image build container on heavy_workload nodes |
| `aria-orchestrator` | service | running | 2026-05-12 22:44 | Hermes container, alloc d43c2a7e on light-1 |
| `aria-layer1-comment-poll` | batch/periodic | running | 2026-05-09 15:13 | Every 1min tick; many `dead` periodic-NNN children visible (normal) |
| `aria-layer1-reconcile` | — | **NOT DEPLOYED** | — | Spec'd in `aria-orchestrator/deploy/aria-layer1-reconcile.nomad.hcl` but not registered with Nomad |
| `aria-layer1-cron` | — | **NOT DEPLOYED** | — | Spec'd but not registered; cron tick may be served by Hermes-internal per AD-M2-7 |
| `aria-layer2-runner` | — | **NOT DEPLOYED** | — | parameterized template for Layer 2 dispatch; never registered |

### Database (dispatches.db)

- **Schema version**: `3.0` (M4 era — pre-M5 v4.x; pre-Spec Y v4.2)
- **Tables**: `dispatches`, `migration_notes`, `schema_meta`
- **Rows**: 16 (real production work — DO NOT corrupt)
- **State distribution**: not yet queried (next session diagnostic step before migration)

### Code versions

- **aria-layer1** installed in venv: **`0.2.0`** (M3 era)
- **aria-layer1** in source dir editable, will become whatever the source is after upgrade
- **/root/Aria HEAD**: `e416920 feat(m2): bump aria-orchestrator + tasks.md/proposal.md`
- **/root/Aria branch**: `feature/aria-2.0-m2-layer1-state-machine` (NOT master)
- **/root/Aria local master**: `b56d826 release(v1.17.6)` — 258 commits behind origin/master
- **aria-orchestrator submodule HEAD**: `5467991 fix(feishu): _compute_feishu_signature key/msg swap` (M3 era)
- **aria submodule HEAD**: `7e11e6a release(v1.17.7)` (April, very stale)
- **standards submodule HEAD**: `5b56dd4` (heads/master, age unknown)

### Connectivity

- ✅ light-1 reaches Forgejo via HTTPS (302 redirect, working)
- ✅ light-1 reaches Forgejo Container Registry (`/v2/` endpoint, working)
- ✅ light-1 reaches Nomad API at `http://192.168.69.70:4646`
- ✅ light-1 reachable from dev container via SSH (`ssh light-1`, hostname `light-1` resolves)

---

## §2 Architectural ambiguity (must resolve before deploy)

### Issue 2.1 — Hermes-internal cron vs Nomad periodic

**DEPLOYMENT.md (AD-M2-7) says**:
> "There is **no separate Nomad job** for Layer 1 — the existing `aria-orchestrator` job hosts hermes; pip-installing this package into that venv is all the runtime registration needed."
>
> Architecture: Nomad `aria-orchestrator` → Hermes → plugin entry-point → `aria_layer1.register(ctx)` → `ctx.register_hook("on_session_start", ...)` → on session start subprocess `hermes cron create` → cron fires `python -m aria_layer1.tick_runner` every 60min

**But production also has**:
- `aria-layer1-comment-poll` as an independent Nomad periodic job (added 2026-05-09, M4 era)

**Open question**: When M5 adds reconciler + cron, do they follow:
- (a) DEPLOYMENT.md AD-M2-7 pattern → register via Hermes plugin entry-point, no new Nomad job
- (b) 2026-05-15 M5 playbook pattern → independent Nomad periodic jobs (`aria-layer1-reconcile.nomad.hcl` + `aria-layer1-cron.nomad.hcl` exist in source `deploy/` dir)
- (c) Hybrid — keep comment-poll as Nomad, add reconcile + cron as Nomad too (consistent w/ M4 precedent)
- (d) Hybrid — only comment-poll as Nomad (high-frequency), reconcile + cron via Hermes-internal cron (low-frequency)

**Needs owner OD** before any deploy. Without this, we'd be picking by guess.

### Issue 2.2 — `/opt/aria-orchestrator/hermes-data/` missing

The aria-orchestrator Nomad job HCL (in dev container at `aria-orchestrator/deploy/aria-orchestrator.nomad.hcl`) mounts:
```
"/opt/aria-orchestrator/hermes-data:/root/.hermes"
```

But on light-1 prod, that host dir does NOT exist. Two possibilities:
- (a) Docker creates the dir on first container start (default behavior) and Hermes persists state there; the dir SHOULD exist if Hermes has ever started — its absence suggests Hermes container uses a *different* HCL or volume mount on prod
- (b) The actual prod aria-orchestrator job HCL is different from the dev-container source — we'd need to read the live job spec via `nomad job inspect aria-orchestrator -t '{{.Job.TaskGroups}}'` (BUT this risks leaking secrets — must use `--tmpl` carefully or just describe at higher level)

**Needs investigation** to confirm Hermes session state location.

### Issue 2.3 — Uncommitted M aria-orchestrator submodule

`git status` shows `M aria-orchestrator`. `git diff aria-orchestrator` shows:

```
- Subproject commit e0cc6de3a2049d434e408020233628b35d9c9498   (parent index expects)
+ Subproject commit 54679910de6b3c06d8ee5fc9d611493c122c51f4   (actual checkout)
```

Submodule was bumped from `e0cc6de` (M2 era) to `5467991` (M3 era / "heads/master" per submodule status). This bump was performed but never committed.

**Possible origins**:
- (a) Someone (you?) ran `git -C aria-orchestrator pull` at some point without committing the parent bump
- (b) Mid-flight upgrade that got interrupted
- (c) The parent commit `e416920 feat(m2)` was written before the submodule actually got bumped, and the bump happened later

**Needs owner OD**: Reset (discard uncommitted M, accept whatever new branch we switch to) / Commit (record as a separate cleanup commit on feature branch before switch) / Investigate originator (low value 1+ month later).

### Issue 2.4 — `/opt/aria-orchestrator/app/` obsolete artifact

Contents: Dockerfile + config/ + deploy/ + skills/ + scan.sh + .aria/heartbeat-scan.json (all Apr 6-8).

**Hypothesis**: This was an early M1-era deployment scaffold from when aria-orchestrator was conceived as a docker-deployed app. Got superseded by AD-M2-7 pip-install-in-venv pattern. Never cleaned up.

**Verdict**: Safe to leave alone OR cleanup. Doesn't affect deploy. Note for cleanup in low-priority backlog.

### Issue 2.5 — 211-258 commit jump strategy

`/root/Aria` is on `feature/aria-2.0-m2-layer1-state-machine` (13 behind origin/feature). `master` is 258 behind origin/master. To upgrade:

- Switch to master → git pull 258 commits
- Submodule update: aria-orchestrator `5467991` → `962cb56` (M5 + HCL fix); aria `7e11e6a` (v1.17.7) → `53ab56d` (v1.21.4); standards advanced

This is **211+ commits of code changes across 3 repos** including: M3 ship + M4 ship + M5 Phase 1-6 ship + Spec X + Spec Y + multiple v1.17.x/v1.20.x/v1.21.x patches + secret rotation + Nomad var config changes + many hooks/skills additions.

**Risk**: hidden assumptions could break. E.g.: maybe an env var was renamed at some point and not in DEPLOYMENT.md. Or maybe a host volume dir name changed.

**Owner OD options**:
- (a) Single big leap: switch + update + reload + test
- (b) Staged: M3 first → verify → M4 → verify → M5 → verify (much slower but safer)
- (c) Fresh clone in /root/Aria-new/ + venv rebuild + switch over (preserves /root/Aria/ for diff inspection)

---

## §3 Migration plan starting point (NOT executed, for v2 addendum)

Once §2 ambiguities are resolved by owner OD, the abstract path is:

1. **Triage uncommitted M** per §2.3 OD
2. **Snapshot prod state** before any change:
   - `cp -a /opt/aether-volumes/aria-layer1/data/ /tmp/aria-layer1-data-snapshot-$(date +%Y%m%dT%H%M%S)/`
   - `git -C /root/Aria stash push -m "pre-upgrade-snapshot"` (if uncommitted to keep)
   - `nomad job inspect aria-orchestrator > /tmp/aria-orchestrator-job-$(date +%Y%m%dT%H%M%S).json` (BUT ⚠️ Rule #7 — may contain runtime env vars; if used, immediately gzip + chmod 600 + delete after 7d)
3. **Switch /root/Aria to master + submodule update** per §2.5 chosen strategy
4. **pip install --upgrade** the editable install (since source path stays same, but version metadata refreshes)
5. **Schema migration v3.0 → v4.2** via Python (sqlite3 CLI not installed):
   - Apply 004 (v3 → v4)
   - Apply 005 (v4 → v4.1)
   - Apply 006 (v4.1 → v4.2; Spec Y T0 spec_id column)
   - Verify schema_meta + row count + new columns present
6. **Hermes restart** to pick up new aria-layer1 code:
   - `nomad job restart aria-orchestrator`
   - OR more invasive: stop + rerun with refreshed Nomad var template
7. **Deploy missing Layer 1 Nomad jobs** per §2.1 OD:
   - aria-layer1-cron (low frequency, was Hermes-internal — needs OD)
   - aria-layer1-reconcile (was Hermes-internal — needs OD)
8. **Smoke (Layer 1-only, SQL-inject pattern)** per 2026-05-15 playbook Step 5:
   - Smoke A: changes mode wiring (parent → S_FAIL + child rework row)
   - Smoke B: redo mode wiring (placeholder comment posted)
   - Smoke C: rework_max_round cap fires
   - **NO Layer 2 alloc** — Step 5 dispatches via SQL inject only
9. **Tier-1 live LLM gates** (`ARIA_FAILURE_ANALYSIS_ENABLED=1` + `ARIA_SPEC_DRIFT_ENABLED=1`):
   - Manually trigger reconciler
   - Verify B.1.live + C.2.live audit log entries
10. **Writeback m5-handoff.yaml + validate**
11. **Defer to next-next session**: Layer 2 image v11 build + Step 5 real Layer 2 smoke (only after Layer 1 stable)

---

## §4 Key facts to surface in addendum v2

These MUST be top of addendum v2 so the next implementer doesn't re-discover them:

1. `cd /root/Aria` (NOT `/opt/aria-orchestrator`)
2. `ssh light-1` (NOT `ssh aether-light-1` — alias doesn't exist; SSH wildcard `light-*` already configured)
3. `export NOMAD_ADDR=http://192.168.69.70:4646` (not in default env)
4. NO `sqlite3` CLI — use `python3 -c "import sqlite3; ..."` instead
5. DB schema starts at **v3.0** (not v4.1 as addendum assumed) — need 3 migrations (004 + 005 + 006)
6. aria-layer1 install is editable from `/root/Aria/aria-orchestrator/hermes-extensions/aria-layer1` (DEPLOYMENT.md flow)
7. **211 commits to git pull** + 3 submodule updates — this is M3 → M4 → M5 + Spec X + Y + v1.21.4 all at once
8. **Layer 2 image build is SEPARATE** from this session's scope; current addendum v11 Step 2.5 must be split out
9. **Hermes-internal vs Nomad cron architecture must be owner-OD'd** before deploy
10. **16 production dispatches in DB** — backup before migrating

---

## §5 What this session accomplished re: prod deploy

- ✅ Discovered prod state (above)
- ✅ Verified light-1 reachable, Forgejo + Nomad reachable, source dir exists
- ❌ DID NOT touch prod (zero modifications to /root/Aria, /opt, dispatches.db)
- ❌ DID NOT deploy
- ⏸ Paused before 211-commit jump + schema migration on 16-row real DB at 04:30 UTC after ~10h session

**This is the safe outcome** — locked reality without breaking anything.

---

## §6 Cross-references

- **Superseded v11 addendum** (DO NOT use as authority): [`2026-05-19-m5-deploy-playbook-v11-addendum.md`](2026-05-19-m5-deploy-playbook-v11-addendum.md) — based on incorrect assumptions about prod layout
- **Companion v2 addendum** (use this for next deploy attempt): [`2026-05-20-m5-deploy-playbook-v2-accurate.md`](2026-05-20-m5-deploy-playbook-v2-accurate.md)
- **DEPLOYMENT.md** (live source at `/root/Aria/aria-orchestrator/hermes-extensions/aria-layer1/DEPLOYMENT.md`) — AD-M2-7 canonical pattern
- **M5 Layer 1 playbook (M4-era predecessor)**: [`2026-05-15-m5-deploy-playbook.md`](2026-05-15-m5-deploy-playbook.md) — assumes M4 already deployed, doesn't directly apply
- **M4 Track A deploy playbook**: [`2026-05-09-track-a-deploy-playbook.md`](2026-05-09-track-a-deploy-playbook.md) — earliest viable M4 reference, may match this prod's setup history
- **Aria PRs / commits informing this gap**:
  - aria-plugin v1.21.4 release: aria submodule master `53ab56de20`
  - aria-orchestrator HCL registry-lock: master `962cb56c1b`
  - Aria main master: `42d40c6501`

---

**Created**: 2026-05-20 ~04:30 UTC by AI investigation step (no prod modifications)
**Status**: Authoritative reality snapshot — supersedes addendum v11 assumptions
