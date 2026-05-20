# Production aria-orchestrator Nomad job — live spec snapshot

> **Created**: 2026-05-20 ~05:57 UTC by Phase A.4 (Rule #7 limited inspection)
> **Source**: `NOMAD_ADDR=http://192.168.69.70:4646 nomad job inspect aria-orchestrator` on light-1
> **Hygiene**: Env values NOT recorded (Rule #7); only keys listed. Template body NOT recorded; only DestPath. raw_exec args list captured (only `gateway run` — non-secret).

---

## §1 Job-level

| Field | Value |
|-------|-------|
| Name | `aria-orchestrator` |
| Status | `running` |
| Type | `service` |
| Allocation since | 2026-05-12 22:44 (per investigation §1) |
| Node placement | light-1 (alloc `d43c2a7e`) |

## §2 TaskGroup `orchestrator`

| Field | Value |
|-------|-------|
| Count | 1 |
| Group Volumes | **NONE** (no host volume refs at group level) |

## §3 Task `hermes-gateway`

| Field | Value |
|-------|-------|
| Driver | **`raw_exec`** (NOT docker — runs as native process on host) |
| Command | `/opt/aria-orchestrator/venv/bin/hermes` |
| Args | `["gateway", "run"]` |
| Resources | CPU=256, MemoryMB=384 |
| Templates | 1 template → `DestPath=secrets/aria-layer1.env`, ChangeMode=`restart`, Perms=`0600` |
| VolumeMounts | (none) |
| Container mounts | (N/A — raw_exec, no container) |

## §4 Env keys (16 total, Rule #7 — keys ONLY, no values)

```
ANTHROPIC_BASE_URL
ARIA_DB_PATH
ARIA_HERMES_CLI_BIN
ARIA_LOCK_PATH
ARIA_PROJECT_DIR
DOTENV_PATH                  ← points to rendered secrets template
FORGEJO_BASE_URL
FORGEJO_ORG
FORGEJO_REPO
HERMES_ALLOC_TIMEOUT_MIN
HERMES_HOME                  ← Hermes state path (probably /root/.hermes per §5)
HERMES_INITIAL_DELAY_SEC
HERMES_TICK_INTERVAL_SEC
HOME
LUXENO_BASE_URL
M1_HANDOFF_PATH
```

**Secret-likely tag**: NONE matched `KEY|TOKEN|SECRET|PASSWORD|API|WEBHOOK` substring. Secrets are delivered via the `secrets/aria-layer1.env` template (Nomad Variable-rendered, perms 0600) and consumed via `DOTENV_PATH`. ✅ Rule #7-clean pattern.

## §5 Host filesystem findings (for OD-3 resolution)

```
/opt/aria-orchestrator/
├── app/      ← Apr 6-8 obsolete docker-era scaffold (uid 1000=dev, no references, OD-4 = leave alone)
│   ├── Dockerfile, README.md, deploy/, schema/, scan.sh, setup-cron.sh, etc.
│   └── (referenced by NOTHING in current prod)
└── venv/     ← Python 3.11 venv (root-owned)
    └── bin/hermes  ← 237 bytes (pip entry-point shim)

/root/.hermes/                                ← ACTIVE Hermes state (root-owned, drwx------)
├── .env (605 bytes, Apr 8)
├── .models_dev_cache_xhumyzbz.tmp (1.7 MB, Apr 20)
├── .skills_prompt_snapshot.json (1071 bytes, Apr 9)
├── SOUL.md (513 bytes, Apr 7)
├── auth.json (1205 bytes, Apr 8)
├── auth.lock (0 bytes, Apr 7)
├── bin/ (Apr 7)
└── ... (last modify 2026-05-20 05:56 UTC — actively maintained)

/opt/aether-volumes/aria-layer1/
└── data/dispatches.db   (snapshot taken in Phase A.2)
```

**OD-3 resolution**: dev-source HCL `mount /opt/aria-orchestrator/hermes-data:/root/.hermes` is a docker-era artifact. Prod uses raw_exec → no docker mount → Hermes state lives directly at `/root/.hermes/` (active, healthy). **No action needed**: keep `/root/.hermes/` as-is; M5 reconcile + cron Nomad jobs must use their own state paths (probably under `/opt/aether-volumes/aria-layer1/` if persistence needed, or stateless).

**OD-4 resolution**: `/opt/aria-orchestrator/app/` is uid=1000 dev-user-owned Apr 6-8 docker-era scaffold. Zero references in current prod. **Leave alone** (no harm), add to low-pri cleanup backlog.

## §6 Implications for M5 deploy (Phase B/C)

1. **Hermes plugin entry-point disable for OD-2 (b) Pure Nomad**: aria-layer1's `plugin.yaml` registers an `on_session_start` hook that calls `hermes cron create`. For "(b) Pure Nomad", we need a way to **NOT** register that hook (env flag or config switch). **TODO**: verify in source — check `aria_layer1/__init__.py` or `plugin.yaml` for opt-out mechanism. Otherwise we ship reconcile+cron as Nomad periodic AND have Hermes-internal cron running redundantly → double dispatch risk.

2. **Hermes restart impact**: `nomad job restart aria-orchestrator` will kill the running hermes process and respawn. Hermes plugin re-init → plugin.yaml entry-point fires → if `cron create` fires unconditionally, we get a fresh internal cron job. State persists at `/root/.hermes/` so no data loss.

3. **dispatches.db path**: `ARIA_DB_PATH` env is set (key only, value unknown). Investigation §1 showed `/opt/aether-volumes/aria-layer1/data/dispatches.db` is the prod path. Likely `ARIA_DB_PATH=/opt/aether-volumes/aria-layer1/data/dispatches.db`. **Confirm before migration** by reading the rendered `secrets/aria-layer1.env` on a live alloc (Rule #7 — only read env keys, not file content) OR by checking the Nomad Variable that backs the template.

4. **New Nomad jobs for OD-2 (b)**: aria-layer1-reconcile.nomad.hcl + aria-layer1-cron.nomad.hcl exist in source `deploy/`. Need to verify they target light-1 (same class) and reference `/opt/aether-volumes/aria-layer1/data/dispatches.db` via env.

5. **Nomad data dir**: `nomad agent -config=/opt/nomad/config` — alloc dirs not at `/var/lib/nomad/`. If we ever need to read alloc working dir, find via `nomad alloc fs <alloc_id>` or read `/opt/nomad/config/` to find data_dir.

---

**Status**: Phase A.4 done. Ready to surface OD-3 + OD-4 confirmation to owner + proceed to A.5 sign-off.
