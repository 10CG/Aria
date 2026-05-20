# Aria 2.0 M5 — T-deploy playbook v2 (accurate, replaces v11 addendum)

> **Status**: Owner-runnable playbook for M5 (+ Spec X + Spec Y + v1.21.4) production deploy on light-1
> **Authority**: Built from `2026-05-20-prod-state-investigation.md` reality snapshot
> **Supersedes**: `2026-05-19-m5-deploy-playbook-v11-addendum.md` (v11 addendum based on incorrect prod-layout assumptions)
> **Prerequisites**: 5 owner OD decisions resolved (§OD-1 through §OD-5)
> **Target**: light-1 (192.168.69.90, light_exec class, raw_exec driver)
> **Estimated time**: 4-6h total split into 3 phases (recommended split over 2 sessions)

---

## TL;DR

Production reality (verified 2026-05-20):
- aria-layer1 v0.2.0 installed editable from `/root/Aria/...`
- Schema v3.0 with 16 production dispatches
- Layer 1 cron + reconcile **NOT** deployed as Nomad jobs (only comment-poll is)
- /root/Aria 211/258 commits behind master
- Uncommitted submodule M (aria-orchestrator: e0cc6de → 5467991)

This playbook drives prod from M3-era state → M5 + Spec X + Spec Y + v1.21.4 state.

**Three phases**:

| Phase | Scope | Time | Risk |
|-------|-------|------|------|
| **A. OD resolution + safe snapshot** | 5 owner OD decisions + DB backup + branch state preservation | ~30min | None — pre-action only |
| **B. Layer 1 only deploy** (this playbook's main scope) | Source upgrade + schema migration + Hermes restart + (optionally) reconcile/cron Nomad jobs | ~2-3h | Moderate — touches prod DB + Hermes restart |
| **C. Layer 2 image v11 + real smoke** (separate session) | aria-build container + image push + sha pin + Layer 2 dispatch smoke | ~2h | Low — image work is rollback-friendly |

---

## §OD — Owner OD prompts (resolve BEFORE Phase A starts)

### OD-1 — Uncommitted M aria-orchestrator submodule (§Investigation 2.3)

`git diff aria-orchestrator` shows bump from `e0cc6de` (M2) → `5467991` (M3 master). Bump performed but never committed.

| Option | Action |
|--------|--------|
| **(a)** Reset | `git -C /root/Aria submodule update --init aria-orchestrator` discards local bump; we'll re-bump to current master during Phase B Step 3 |
| **(b)** Commit | Create cleanup commit on `feature/aria-2.0-m2-layer1-state-machine` recording the M2→M3 bump intent, then switch to master |
| **(c)** Investigate | Defer the upgrade until originator confirms intent |

**Recommendation**: **(a) Reset** — the bump intent is preserved by the master upgrade anyway (we'll go all the way to `962cb56` M5+HCL fix). Don't muddy git history with a 1-month-stale "M2→M3 bump" commit.

**OD-1 decision**: _______________

---

### OD-2 — Cron architecture (§Investigation 2.1)

Current prod runs: aria-orchestrator (Hermes) + aria-layer1-comment-poll (Nomad periodic).

M5 needs: cron tick (`tick_runner`) + reconciler. Two patterns possible:

| Pattern | How | Pros | Cons |
|---------|-----|------|------|
| **(a) Pure Hermes-internal** (per DEPLOYMENT.md AD-M2-7) | Layer 1 plugin registers via `hermes cron create` on session start; runs `python -m aria_layer1.tick_runner` every 60min from within Hermes container | Single point of operational control; no new Nomad job; matches DEPLOYMENT.md SOP | Hermes-internal cron is opaque to Nomad — outage detection harder; no `nomad job status` visibility |
| **(b) Pure Nomad periodic** (per 2026-05-15 M5 playbook + existing comment-poll precedent) | Deploy `aria-layer1-reconcile.nomad.hcl` + `aria-layer1-cron.nomad.hcl` from `aria-orchestrator/deploy/`; Hermes-internal cron disabled or never registered | Uniform with comment-poll; Nomad-native visibility; allows per-job restart | Two Nomad jobs added + Hermes still needs to know not to register internal cron |
| **(c) Hybrid** | comment-poll stays as Nomad (M4 precedent); cron stays Hermes-internal (DEPLOYMENT.md SOP); reconcile = new Nomad periodic job | Minimal disruption to existing pattern; reconcile is heaviest so Nomad isolation helps | Confused architecture; team has to remember which is which |

**Recommendation**: **(b) Pure Nomad periodic** — comment-poll is already Nomad, so reconcile + cron should join. Removes "Hermes-internal cron" as a parallel control plane. Need to verify Hermes plugin entry-point can be turned off (env var or config flag).

**OD-2 decision**: _______________

---

### OD-3 — `/opt/aria-orchestrator/hermes-data/` missing (§Investigation 2.2)

Nomad HCL (dev container version) mounts `/opt/aria-orchestrator/hermes-data:/root/.hermes`. The host dir doesn't exist on light-1.

Hypotheses:
- (a) Live prod HCL is different from dev source (volume mount path moved)
- (b) Hermes never persisted state (cold start every alloc?) — meaning `hermes cron create` never recorded a job

Action needed: Read the LIVE Nomad job spec for aria-orchestrator and compare to dev source HCL.

**Safe inspection command** (Rule #7 — limit to TaskGroups structure, no Env):
```bash
nomad job inspect -t '{{json .Job.TaskGroups}}' aria-orchestrator | python3 -m json.tool | grep -A 3 -E "Volumes|HostPath|Mounts" | head -40
```

**OD-3 decision** (after running above): _______________ (mount path / create dir / migrate state)

---

### OD-4 — `/opt/aria-orchestrator/app/` obsolete artifact (§Investigation 2.4)

Apr 6-8 dated dir (uid 1000 = dev user) with Dockerfile, config/, deploy/, scan.sh etc. Not referenced by anything we found.

**Recommendation**: Leave alone — no harm, cleanup not blocking. Add to low-priority backlog.

**OD-4 decision**: _______________ (leave / cleanup / investigate)

---

### OD-5 — 211-commit jump strategy (§Investigation 2.5)

`/root/Aria` is 211 commits behind master. To upgrade, we need to switch + pull.

| Strategy | Description |
|----------|-------------|
| **(a) Single big leap** | `git checkout master && git pull && git submodule update --init --recursive --remote` — one shot, ~30s, then rest of deploy follows |
| **(b) Staged** | M2→M3 verify → M3→M4 verify → M4→M5 verify; ~3× the time, safer rollback at each stage |
| **(c) Fresh clone** | Clone `/root/Aria-new/` from scratch in sibling dir; rebuild venv; swap atomic via symlink or rename |

**Recommendation**: **(a) Single big leap** + **strong backup** (Phase A Step 2) + **post-leap smoke** (Phase B Step 6). The intermediate states (M3, M4) aren't independently validated checkpoints — they're snapshots in our git history but not separately tested for "can run on top of M2 prod state". Staged isn't actually safer; it's just slower with more rollback points that we've never exercised.

**OD-5 decision**: _______________

---

## §Phase A — OD resolution + safe snapshot (~30min, no prod mutation)

### A.1 — Confirm all 5 OD decisions are recorded

Fill in the 5 OD slots above. Without these, **DO NOT** proceed to Phase B.

### A.2 — Snapshot dispatches.db (CRITICAL — 16 production rows)

```bash
ssh light-1
TS=$(date -u +%Y%m%dT%H%M%S)
SNAP=/tmp/aria-layer1-snapshot-$TS
mkdir -p $SNAP
cp -a /opt/aether-volumes/aria-layer1/data/dispatches.db $SNAP/dispatches.db.pre-m5
ls -la $SNAP/

# Verify integrity of snapshot using Python sqlite3 (CLI not installed)
python3 -c "
import sqlite3
c = sqlite3.connect('$SNAP/dispatches.db.pre-m5')
print('integrity:', c.execute('PRAGMA integrity_check').fetchone()[0])
print('row count:', c.execute('SELECT COUNT(*) FROM dispatches').fetchone()[0])
print('schema_version:', c.execute(\"SELECT value FROM schema_meta WHERE key='schema_version'\").fetchone()[0])
"
# Expected: integrity=ok, row count=16, schema_version=3.0
```

### A.3 — Snapshot /root/Aria state

```bash
cd /root/Aria
git stash push -m "pre-m5-upgrade-snapshot-$(date -u +%Y%m%dT%H%M%S) (uncommitted M aria-orchestrator)" || echo "(nothing to stash)"
git branch backup/pre-m5-upgrade-$(date -u +%Y%m%dT%H%M%S) HEAD
echo "Backup branch created at: $(git branch -v | grep backup/pre-m5)"
# Expected: branch backup/pre-m5-upgrade-<TS> pointing at current feature branch tip
```

### A.4 — Snapshot Nomad job spec (Rule #7 — be careful)

Per OD-3:
```bash
# SAFE: just TaskGroups structure (no Env / Templates that leak secrets)
nomad job inspect -t '{{json .Job.TaskGroups}}' aria-orchestrator \
  | python3 -m json.tool \
  | grep -E "(Name|Driver|Volumes|HostPath|Mounts|Image)" \
  | head -50

# UNSAFE: do NOT run full inspect or write to file
# (Rule #7: nomad inspect leaks env including secrets — see feedback_nomad_inspect_secret_leak)
```

Document the output in `.aria/notes/prod-job-spec-live-2026-05-20.md` (scrub any secret-looking values).

### A.5 — Phase A sign-off checklist

- [ ] OD-1 (uncommitted M) decision recorded
- [ ] OD-2 (cron architecture) decision recorded
- [ ] OD-3 (hermes-data mount) decision + safe inspection performed
- [ ] OD-4 (app/ obsolete) decision recorded (or "ignore")
- [ ] OD-5 (jump strategy) decision recorded
- [ ] A.2 DB snapshot integrity verified (16 rows preserved)
- [ ] A.3 git backup branch created
- [ ] A.4 live Nomad job spec captured (no secrets in file)
- [ ] All 16 production dispatch IDs noted (to verify zero data loss post-migration)

---

## §Phase B — Layer 1 deploy (~2-3h, modifies prod)

### B.1 — Triage uncommitted M per OD-1

If OD-1 == (a) reset:
```bash
cd /root/Aria
git submodule update --init aria-orchestrator  # restores parent's expected SHA
git status  # should show clean
```

If OD-1 == (b) commit:
```bash
cd /root/Aria
git add aria-orchestrator
git commit -m "chore(submodule): bump aria-orchestrator e0cc6de → 5467991 (M2→M3, recovered from in-progress state pre-M5 upgrade)"
git push origin feature/aria-2.0-m2-layer1-state-machine
```

### B.2 — Switch to master + submodule update per OD-5

If OD-5 == (a) single big leap:
```bash
cd /root/Aria
git fetch origin --quiet
git checkout master
git pull origin master --ff-only  # 258 commits

# Submodule update with --remote (track each submodule's master)
git submodule update --init --recursive --remote

# Verify final state
echo "[Aria meta]"; git log -1 --oneline
echo "[aria-orchestrator]"; git -C aria-orchestrator log -1 --oneline
echo "[aria]"; git -C aria log -1 --oneline
echo "[standards]"; git -C standards log -1 --oneline

# Expected (as of 2026-05-20):
#   [Aria meta]            42d40c6501 docs(handoff): 2026-05-20 v1.21.4 + triage + v11 deploy prep
#   [aria-orchestrator]    962cb56c1b ops(deploy): lock image registry to forgejo.10cg.pub
#   [aria]                 53ab56de20 (v1.21.4 release commit)
#   [standards]            69815682d7 ...
```

If OD-5 == (b) staged: see staged sub-playbook (TODO if owner picks this option)

If OD-5 == (c) fresh clone: see fresh-clone sub-playbook (TODO if owner picks this option)

### B.3 — Refresh editable install

```bash
source /opt/aria-orchestrator/venv/bin/activate
cd /root/Aria/aria-orchestrator/hermes-extensions/aria-layer1
pip install -e . 2>&1 | tail -5

# Verify version bump
pip show aria-layer1 | grep -E "Version|Editable"
# Expected: Version: 0.4.0 + Editable project location: /root/Aria/aria-orchestrator/hermes-extensions/aria-layer1
```

### B.4 — Schema migration v3.0 → v4.2 (3-safeguard)

Per `2026-05-19-m5-deploy-playbook-v11-addendum.md` Step 2 (THIS PART of v11 is still valid),
but adjusted because **sqlite3 CLI not installed on light-1** — use Python `sqlite3` instead:

```bash
DB_PATH=/opt/aether-volumes/aria-layer1/data/dispatches.db
BACKUP_DIR=/opt/aether-volumes/aria-layer1/data/backups
TS=$(date -u +%Y%m%dT%H%M%S)

# Safeguard 1 — atomic backup
mkdir -p $BACKUP_DIR
python3 -c "
import sqlite3
src = sqlite3.connect('$DB_PATH')
dst = sqlite3.connect('$BACKUP_DIR/dispatches.db.pre-v4.2.$TS')
src.backup(dst)
src.close(); dst.close()
print('backup OK')
"

# Safeguard 2 — verify backup
python3 -c "
import sqlite3
c = sqlite3.connect('$BACKUP_DIR/dispatches.db.pre-v4.2.$TS')
print('integrity:', c.execute('PRAGMA integrity_check').fetchone()[0])
print('row count:', c.execute('SELECT COUNT(*) FROM dispatches').fetchone()[0])
"
# Expected: integrity=ok, row count=16

# Safeguard 3 — dry-run on a copy
cp $BACKUP_DIR/dispatches.db.pre-v4.2.$TS /tmp/dispatches.dryrun.db
python3 -c "
import sqlite3
from aria_layer1.schema_migrate import apply_migrations
c = sqlite3.connect('/tmp/dispatches.dryrun.db')
c.execute('PRAGMA foreign_keys=ON')
r = apply_migrations(c)
print('dry-run applied:', r['applied'])      # Expected: ['004', '005', '006']
print('to_version:', r['to_version'])         # Expected: '4.2'
print('integrity:', c.execute('PRAGMA integrity_check').fetchone()[0])
print('row count:', c.execute('SELECT COUNT(*) FROM dispatches').fetchone()[0])
cols = [c[1] for c in c.execute('PRAGMA table_info(dispatches)').fetchall()]
print('spec_id col present:', 'spec_id' in cols)
print('rework_* cols present:', sum(1 for col in cols if col.startswith('rework_')))
print('risk_tier col present:', 'risk_tier' in cols)
"
# Verify all 6 new cols (spec_id + risk_tier + 4 rework_*) present + row count = 16

# Apply on prod
python3 -c "
import sqlite3
from aria_layer1.schema_migrate import apply_migrations
c = sqlite3.connect('$DB_PATH')
c.execute('PRAGMA foreign_keys=ON')
r = apply_migrations(c)
print('prod applied:', r['applied'])
print('schema_version:', c.execute(\"SELECT value FROM schema_meta WHERE key='schema_version'\").fetchone()[0])
print('integrity:', c.execute('PRAGMA integrity_check').fetchone()[0])
print('row count:', c.execute('SELECT COUNT(*) FROM dispatches').fetchone()[0])
"
# Expected: schema_version=4.2, integrity=ok, row count=16
```

**Rollback if any safeguard fails**:
```bash
cp $BACKUP_DIR/dispatches.db.pre-v4.2.$TS $DB_PATH
# DB restored — no schema changes applied
```

### B.5 — Nomad Var configuration

Same as v11 addendum Step 3 + 2026-05-15 playbook Step 3:
```bash
# (no actual secret values posted; this is the config envelope)
# Owner sets via: nomad var put -force nomad/jobs/aria-orchestrator \
#   LUXENO_API_KEY=@/secure/path/luxeno.key \
#   ARIA_FEISHU_WEBHOOK_URL=@/secure/path/feishu.url \
#   ARIA_REWORK_MAX_ROUND=3 \
#   ARIA_SPEC_DRIFT_THRESHOLD=70 \
#   ARIA_FAIL_RETRY_CONFIDENCE_MIN=0.7 \
#   ARIA_FAILURE_ANALYSIS_ENABLED=0 \
#   ARIA_SPEC_DRIFT_ENABLED=0
#
# Verify (key names only — Rule #7):
nomad var get -out=keys nomad/jobs/aria-orchestrator | sort
```

### B.6 — Hermes restart (picks up new code)

```bash
nomad job restart aria-orchestrator
sleep 30
nomad job status aria-orchestrator | head -15
# Verify new alloc is running
```

### B.7 — Deploy missing Layer 1 Nomad jobs per OD-2

If OD-2 == (b) Pure Nomad:
```bash
cd /root/Aria/aria-orchestrator
nomad job validate deploy/aria-layer1-reconcile.nomad.hcl
nomad job validate deploy/aria-layer1-cron.nomad.hcl
nomad job run     deploy/aria-layer1-reconcile.nomad.hcl
nomad job run     deploy/aria-layer1-cron.nomad.hcl

# Verify
nomad job status aria-layer1-reconcile | head -10
nomad job status aria-layer1-cron      | head -10
```

If OD-2 == (a) Pure Hermes-internal:
- Don't deploy reconcile/cron HCLs
- Restart aria-orchestrator (B.6 already did this) — on session start Hermes plugin registers cron via DEPLOYMENT.md flow
- Verify: in Hermes alloc logs, look for "aria_layer1.register" and "hermes cron create" markers

If OD-2 == (c) Hybrid:
- Deploy reconcile HCL only; cron stays Hermes-internal
- Verify both paths active

### B.8 — Layer 1 Smoke (SQL-inject pattern, no Layer 2 needed)

Per 2026-05-15 playbook Step 5 (the SQL-inject pattern was actually correct — v11 addendum upgraded too aggressively). Smoke A / B / C verify Layer 1 wiring with synthetic dispatches.

(Full SQL-inject scripts: see `2026-05-15-m5-deploy-playbook.md` Step 5 — those are correct as-is for Layer 1-only verification.)

### B.9 — Phase B sign-off checklist

- [ ] B.1 OD-1 triage executed
- [ ] B.2 Branch switched to master + submodules at expected SHAs
- [ ] B.3 aria-layer1 shows v0.4.0
- [ ] B.4 schema_version=4.2 + 16 rows preserved
- [ ] B.5 Nomad vars set (key names verified)
- [ ] B.6 Hermes restarted + alloc healthy
- [ ] B.7 OD-2 Layer 1 jobs deployed
- [ ] B.8 Smoke A/B/C PASS
- [ ] Phase B handoff doc written (small new handoff describing what shipped)

---

## §Phase C — Layer 2 image build + real smoke (~2h, SEPARATE SESSION)

This phase is **deferred** to a dedicated session. Only start after Phase B is stable for ≥24h.

Scope (will be detailed in a Phase-C-specific playbook when triggered):
- aria-build container image build (claude-m5-carry-09ff364-v11)
- Image push to forgejo.10cg.pub/10CG/aria-runner
- Update `aria-orchestrator/docs/m1-handoff.yaml::image_sha_final`
- Register aria-layer2-runner parameterized template
- Replace Smoke A/B/C with REAL Layer 2 dispatch verification (force-push, close-old-PR, commit-lint retry)
- Tier-1 live LLM gates

This roughly maps to v11 addendum's Step 2.5 + Step 4.5 + Step 5 (real) + Step 6.

---

## §Rollback paths

| Failure | Rollback |
|---------|----------|
| OD resolution stuck | Stay on `feature/aria-2.0-m2-layer1-state-machine` — no changes made |
| A.2 DB snapshot fails | Investigate disk space / permissions — DO NOT proceed without snapshot |
| B.2 git pull fails (conflict / submodule init issue) | Roll back via backup branch from A.3: `git checkout backup/pre-m5-upgrade-<TS>` + `git submodule update --init` |
| B.3 pip install fails | Likely missing system package; check `apt list --installed` vs DEPLOYMENT.md prereqs; rollback by reverting source dir to backup branch + `pip install -e .` again |
| B.4 schema migration fails | Restore from backup: `cp $BACKUP_DIR/dispatches.db.pre-v4.2.$TS $DB_PATH` |
| B.6 Hermes won't start with new code | `nomad job stop aria-orchestrator && nomad job run /opt/aria-orchestrator/.../<old-HCL>` (need to have saved old HCL pre-A.4) |
| B.7 Layer 1 job won't deploy | `nomad job stop -purge <job>` + investigate; doesn't affect existing comment-poll |
| B.8 Smoke A/B/C fail | Document in m5-handoff.yaml; do NOT proceed to Tier-1 LLM gates |

---

## §Estimated time breakdown

| Phase | Activity | Time |
|-------|----------|------|
| OD prep | Owner reviews + decides 5 OD prompts | 15-30min |
| A.2 | DB snapshot + verify | 5min |
| A.3 | git backup + stash | 5min |
| A.4 | Nomad job spec capture | 10min |
| B.1 | Triage uncommitted M | 2min |
| B.2 | Switch master + submodule update | 5min |
| B.3 | pip install --upgrade | 3-5min |
| B.4 | Schema migration (3-safeguard) | 10-15min |
| B.5 | Nomad var config | 5min |
| B.6 | Hermes restart + wait | 5-10min |
| B.7 | Deploy Layer 1 Nomad jobs (per OD-2) | 10-15min |
| B.8 | Smoke A/B/C | 30-45min |
| Phase B handoff | Writeback m5-handoff.yaml stub + new handoff doc | 15-30min |
| **Phase A+B total** | | **~2.5-3.5h** |
| Phase C (separate session) | image v11 build + real Layer 2 smoke + Tier-1 LLM | ~2h |

---

## §Cross-references

- **Reality snapshot**: [`2026-05-20-prod-state-investigation.md`](2026-05-20-prod-state-investigation.md) — authoritative facts behind this playbook
- **Superseded**: [`2026-05-19-m5-deploy-playbook-v11-addendum.md`](2026-05-19-m5-deploy-playbook-v11-addendum.md) — kept for history, banner notes it's superseded
- **DEPLOYMENT.md** (live on light-1): `/root/Aria/aria-orchestrator/hermes-extensions/aria-layer1/DEPLOYMENT.md` — AD-M2-7 canonical
- **Predecessor Layer 1 playbook**: [`2026-05-15-m5-deploy-playbook.md`](2026-05-15-m5-deploy-playbook.md) — Step 5 SQL-inject smoke is reusable
- **Phase D writeback target**: `aria-orchestrator/docs/m5-handoff.yaml` + `aria-orchestrator/docs/validate-m5-handoff.py`
- **US-025 close gate**: Phase B + Phase C completion unblocks US-025 final Go

---

**Created**: 2026-05-20 by AI Phase A.1 investigation step
**Status**: Owner-runnable after 5 OD prompts resolved
**Authority**: Replaces v11 addendum as canonical M5 deploy playbook
