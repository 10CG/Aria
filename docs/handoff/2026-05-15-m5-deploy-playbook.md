# Aria 2.0 M5 — T-deploy playbook (owner-runnable, Phase 6 §T-deploy)

> **Status**: Layer 1 portion (Phase 1-6 implementation) complete 2026-05-15. This playbook is owner-runnable; AI does NOT auto-execute.
> **Target**: Aether `light-1` (existing M4 production deployment site)
> **Mirror pattern**: docs/handoff/2026-05-09-track-a-deploy-done.md (M4 Track A)
> **Spec ref**: openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit Phase 6 §T-deploy (Spec tasks 6.17-6.30)
> **PR / branches**: feature/aria-2.0-m5 on both repos (Aria main + aria-orchestrator submodule)

---

## TL;DR

5 owner-runnable steps + 3 smoke E2E + Tier-2 accumulation:

1. **Pre-deploy**: SSH light-1 → git pull → venv refresh → confirm aria-layer1 v0.4.0 installed
2. **Schema migration (3-safeguard)**: backup → dry-run → apply on prod → verify
3. **nomadVar config**: set 5 env vars (3 thresholds + 2 opt-in toggles)
4. **Nomad job redeploy**: validate + dispatch reconcile/comment-poll/cron jobs
5. **Smoke E2E**: 3 fixtures verifying changes/redo/cap behavior

Phase D.2 final Go decision requires + Tier-1 live LLM gates (B.1.live + C.2.live, ¥0.10) + Tier-2 N≥3 real owner dispatches.

---

## Step 1 — Pre-deploy (~15min)

```bash
# SSH to Aether light-1 (Cloudflare Access)
ssh aether-light-1

# Pull latest aria-orchestrator master (M5 ship branch will be merged here)
cd /opt/aria-orchestrator
git fetch origin
git checkout master  # or feature/aria-2.0-m5 for pre-merge smoke
git pull origin master

# Verify HEAD is M5
git log -1 --oneline
# Expected: should include "Phase 6" / "M5" in subject

# Refresh venv (the venv lives on light-1 raw_exec host — per feedback_handoff_doc_assumes_venv_ready_smell)
source /opt/aria-orchestrator/venv/bin/activate
pip install -e hermes-extensions/aria-layer1
# Verify version
python -c "from aria_layer1 import __version__ as v; print(v)" 2>/dev/null || \
  pip show aria-layer1 | grep Version
# Expected: 0.4.0
```

---

## Step 2 — Schema migration v3 → v4.1 (3-safeguard, ~10min)

**CRITICAL**: per QA-4 + AD-M5-8 + Spec 6.18, the migration MUST use the 3-safeguard pattern.

```bash
DB_PATH=/opt/aether-volumes/aria-layer1/data/dispatches.db
BACKUP_DIR=/opt/aether-volumes/aria-layer1/data/backups
TS=$(date +%Y%m%dT%H%M%S)

# --- Safeguard 1: Atomic backup via Python sqlite3.backup() (WAL-safe) ---
mkdir -p "$BACKUP_DIR"
python3 -c "
import sqlite3
src = sqlite3.connect('$DB_PATH')
dst = sqlite3.connect('$BACKUP_DIR/dispatches.db.pre-m5.$TS')
src.backup(dst)
dst.close(); src.close()
print('backup OK')
"

# --- Safeguard 2: integrity_check on backup + count rows ---
sqlite3 "$BACKUP_DIR/dispatches.db.pre-m5.$TS" "PRAGMA integrity_check;"
# Expected: ok

BACKUP_ROW_COUNT=$(sqlite3 "$BACKUP_DIR/dispatches.db.pre-m5.$TS" "SELECT COUNT(*) FROM dispatches;")
echo "backup row count: $BACKUP_ROW_COUNT"

# --- Safeguard 3: dry-run on a copy ---
cp "$BACKUP_DIR/dispatches.db.pre-m5.$TS" /tmp/dispatches.dryrun.db

python3 -c "
import sqlite3
from aria_layer1.schema_migrate import apply_migrations
conn = sqlite3.connect('/tmp/dispatches.dryrun.db')
conn.execute('PRAGMA foreign_keys=ON')
result = apply_migrations(conn)
print('dry-run applied:', result['applied'])
print('to_version:', result['to_version'])
# Verify integrity + row count
print('integrity:', conn.execute('PRAGMA integrity_check').fetchone()[0])
print('row count:', conn.execute('SELECT COUNT(*) FROM dispatches').fetchone()[0])
"
# Expected: applied includes '004' + '005'; to_version='4.1'; integrity=ok; row count == backup

# --- Apply on prod (only after dry-run PASS) ---
python3 -c "
import sqlite3
from aria_layer1.schema_migrate import apply_migrations
conn = sqlite3.connect('$DB_PATH')
conn.execute('PRAGMA foreign_keys=ON')
result = apply_migrations(conn)
print('prod applied:', result['applied'])
print('integrity:', conn.execute('PRAGMA integrity_check').fetchone()[0])
print('row count:', conn.execute('SELECT COUNT(*) FROM dispatches').fetchone()[0])
print('schema_version:', conn.execute(\"SELECT value FROM schema_meta WHERE key='schema_version'\").fetchone()[0])
"
# Expected: applied=['004','005'] (or ['005'] if 004 was already done); schema_version=4.1; row count unchanged
```

**Rollback if any safeguard fails**: restore from backup `cp "$BACKUP_DIR/dispatches.db.pre-m5.$TS" "$DB_PATH"` → no schema changes applied.

---

## Step 3 — nomadVar configuration (~5min)

Set 5 env vars in Nomad job spec (`deploy/aria-layer1-*.nomad.hcl`):

```hcl
env {
  # Phase 3 D Review-loop cap (per AD-M5-2)
  ARIA_REWORK_MAX_ROUND          = "3"        # default; lock unless owner needs override
  # Phase 5 C Drift defense threshold (per AD-M5-5 + AD-M5-10 promise #3)
  ARIA_SPEC_DRIFT_THRESHOLD      = "70"       # default
  # Phase 2 B Failure-analysis retry confidence threshold (per AD-M5-6)
  ARIA_FAIL_RETRY_CONFIDENCE_MIN = "0.7"      # default
  # Phase 2 LLM opt-in toggle (cost discipline; default off per AD-M5-6)
  ARIA_FAILURE_ANALYSIS_ENABLED  = "0"        # owner choice; 1=enable
  # Phase 5 LLM opt-in toggle (cost discipline; default off per AD-M5-5)
  ARIA_SPEC_DRIFT_ENABLED        = "0"        # owner choice; 1=enable
}
```

**Owner decision**: enable LLM features post-deploy after Tier-1 live LLM gates pass? Or leave off until Tier-2 evidence?

---

## Step 4 — Nomad job validate + redeploy (~10min)

```bash
cd /opt/aria-orchestrator
# Validate HCL syntax (per feedback_nomad_hcl_validate_early)
nomad job validate deploy/aria-orchestrator.nomad.hcl
nomad job validate deploy/aria-layer1-reconcile.nomad.hcl
nomad job validate deploy/aria-layer1-comment-poll.nomad.hcl
nomad job validate deploy/aria-layer1-cron.nomad.hcl
# Expected: 0 errors

# Stop & re-run periodic jobs (forces fresh alloc with new env)
nomad job stop -purge aria-layer1-reconcile
nomad job stop -purge aria-layer1-comment-poll
nomad job stop -purge aria-layer1-cron

nomad job run deploy/aria-layer1-reconcile.nomad.hcl
nomad job run deploy/aria-layer1-comment-poll.nomad.hcl
nomad job run deploy/aria-layer1-cron.nomad.hcl

# Verify periodic dispatch within first tick (5min for cron, 1min for comment-poll, 30min for reconcile)
nomad job status aria-layer1-comment-poll
nomad job status aria-layer1-reconcile
# Expected: each shows 1+ allocations running

# Verify audit log table exists + accepts INSERTs (smoke)
sqlite3 "$DB_PATH" "SELECT name FROM sqlite_master WHERE type='table' AND name='dispatch_audit_log';"
# Expected: dispatch_audit_log

# Verify v4.1 dispatches cols
sqlite3 "$DB_PATH" "PRAGMA table_info(dispatches);" | grep -E "risk_tier|rework_"
# Expected: 5 v4 cols visible (risk_tier, rework_of, rework_round, rework_mode, rework_feedback)
```

---

## Step 5 — Smoke E2E (~30min, owner action)

Three fixtures verify the M5 review-loop wiring works end-to-end. Each fixture uses SQL inject (per feedback_smoke_dispatch_sql_inject_pattern) since aria-layer2-runner is M6-deferred.

### Smoke A — changes mode (M5 P3 Spec 3.6)

```bash
# Inject S7 dispatch + create Forgejo PR
DISPATCH_ID="smoke-m5-changes-$(date +%s)"
ISSUE_ID="DEMO-M5-001"
PR_ID=99001  # owner: create real PR with one trivial change

sqlite3 "$DB_PATH" "
  INSERT INTO dispatches (issue_id, dispatch_id, state, state_entered_at,
                          image_sha, pr_id, risk_tier, risk_tier_stub,
                          human_gate_entered_at, notification_status)
  VALUES ('$ISSUE_ID', '$DISPATCH_ID', 'S7_HUMAN_GATE', '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
          'sha256:abc123', $PR_ID, 'always', 'always',
          '$(date -u +%Y-%m-%dT%H:%M:%SZ)', '200');
"

# Owner posts /aria changes: <feedback> on the Forgejo PR
# (e.g. forgejo POST /repos/10CG/Aria/issues/$PR_ID/comments  -d '{"body":"/aria changes: please refactor"}')

# Within 30s + 1 reconciler tick (~30min worst-case):
#   parent dispatch state → S_FAIL(changes_requested)
#   new dispatch row appears with rework_mode='changes', rework_round=1, state=S4_LAUNCH
sqlite3 "$DB_PATH" "
  SELECT dispatch_id, state, fail_reason, rework_mode, rework_round, rework_of, rework_feedback
  FROM dispatches WHERE issue_id='$ISSUE_ID' ORDER BY attempt_count;
"
# Expected:
#   parent → S_FAIL changes_requested NULL 0 NULL NULL
#   child  → S4_LAUNCH NULL changes 1 $DISPATCH_ID "please refactor"

# audit log records rework_cycle event
python3 -m aria_layer1.replay_cli "$DISPATCH_ID"
# Expected: replay markdown shows rework chain depth 2 + rework_cycle event
```

### Smoke B — redo mode + placeholder comment (M5 P4 Spec 3.7)

```bash
# Inject another S7 dispatch (different issue)
DISPATCH_ID="smoke-m5-redo-$(date +%s)"
ISSUE_ID="DEMO-M5-002"
PR_ID=99002

sqlite3 "$DB_PATH" "INSERT INTO dispatches ... -- same template as Smoke A"

# Owner posts /aria redo: <feedback>
# Expected: comment_poll → _route_rework_request → posts placeholder comment to old PR:
#   "M5 review-loop notice: this PR is being superseded by a new dispatch (new_dispatch_id=..., mode=redo)..."

# Verify via Forgejo API
forgejo GET /repos/10CG/Aria/issues/$PR_ID/comments | grep -i "superseded by a new dispatch"
# Expected: 1 match

# Verify new dispatch row state=S0_IDLE (full cycle), pr_id=NULL (Layer 2 will create new PR)
sqlite3 "$DB_PATH" "
  SELECT state, rework_mode, pr_id FROM dispatches
  WHERE rework_of='$DISPATCH_ID';
"
# Expected: S0_IDLE redo NULL
```

### Smoke C — cap exceeded (M5 P2 Spec 3.8)

```bash
# Build 3-round chain manually then attempt round 4
# Round 1, 2, 3: SQL inject parent → /aria changes → verify cap_round increments
# Round 4 attempt: /aria changes on the round-3 row → expected reject

# Final verification: round-3 row state=S_FAIL(rework_exceeded)
sqlite3 "$DB_PATH" "
  SELECT fail_reason FROM dispatches WHERE dispatch_id='<round-3 id>';
"
# Expected: rework_exceeded

# Audit log records rework_cycle outcome='rejected_cap_exceeded'
```

---

## Step 6 — Tier-1 live LLM gates (~5min, owner-triggered)

After smoke A/B/C pass, run the 2 live LLM gates (per AD-M5-6 + AD-M5-5):

```bash
# Enable LLM features
export ARIA_FAILURE_ANALYSIS_ENABLED=1
export ARIA_SPEC_DRIFT_ENABLED=1

# Manually trigger reconciler (or wait 30min for natural tick)
python3 -m aria_layer1.reconcile_runner

# B.1.live: synthesize an S_FAIL dispatch with fail_reason='infrastructure'
#   → reconciler calls glm-4.5-air for failure_analysis
#   → audit log records event_type='failure_analysis' with verdict_action + confidence
sqlite3 "$DB_PATH" "
  SELECT json_extract(payload_json, '\$.verdict_action'),
         json_extract(payload_json, '\$.confidence')
  FROM dispatch_audit_log WHERE event_type='failure_analysis' LIMIT 1;
"
# Expected: action ∈ {retry, abort, notify_owner}; confidence ∈ [0,1]

# C.2.live: synthesize an S9_CLOSE dispatch with pr_id (real merged PR)
#   → reconciler calls glm-4.5-air for spec_drift
#   → audit log records event_type='spec_drift_detected' with score ∈ [0,100]
sqlite3 "$DB_PATH" "
  SELECT json_extract(payload_json, '\$.score'),
         json_extract(payload_json, '\$.outcome')
  FROM dispatch_audit_log WHERE event_type='spec_drift_detected' LIMIT 1;
"
# Expected: score is integer ∈ [0,100]; outcome ∈ {clean, drift_detected, parse_failed}

# Cost: ~¥0.05-0.10 total for 2 calls. Disable features after if owner wants
# to defer until Tier-2 accumulates.
```

---

## Step 7 — Tier-2 accumulation (passive, ≥3 real dispatches)

Per Spec 6.27-6.30: collect ≥3 real owner workload dispatches with ≥1 each of changes/redo/reject path. **This is passive — owner does normal workload; no scripted action.** When count ≥ 3, update `m5-handoff.yaml::m5_review_loop_metrics` + sign off Phase D.2.

---

## Writeback to m5-handoff.yaml (post-deploy)

Once smoke + Tier-1 live gates pass, update `docs/m5-handoff.yaml`:

```yaml
t_deploy_status:
  status: complete
  date: 2026-05-XX
  fixes_shipped: ["<any deploy-time fixes>"]
  smoke_verification:
    - "smoke A changes mode: parent S_FAIL + new row S4_LAUNCH"
    - "smoke B redo mode: placeholder comment posted to old PR"
    - "smoke C cap exceeded: round-4 attempt rejected"
m5_acceptance:
  b1_live_llm_passed: true   # verdict_action + confidence verified
  c2_live_llm_passed: true   # score ∈ [0,100] verified
```

Then run `python3 docs/validate-m5-handoff.py -v` — all 5 checks must PASS for D.2 sign-off.

---

## Rollback paths

| Failure point | Rollback |
|---|---|
| Step 1 venv install | Pin to v0.3.0: `pip install aria-layer1==0.3.0` |
| Step 2 dry-run | No prod change — investigate dry-run error, don't apply |
| Step 2 prod | Restore from backup: `cp $BACKUP_DIR/dispatches.db.pre-m5.$TS $DB_PATH` |
| Step 3 nomadVar wrong | Revert env in HCL + restart job |
| Step 4 job fail | `nomad job stop $JOB` + revert HCL + run previous version |
| Step 5 smoke fail | Document in m5-handoff.yaml::open_issues_for_m6; don't proceed to live gates |
| Step 6 LLM gate fail | Set `ARIA_*_ENABLED=0` to disable, investigate parse_failed in audit log |

---

## Owner sign-off checklist

- [ ] Step 1 pre-deploy: aria-layer1 v0.4.0 installed on light-1
- [ ] Step 2 schema migration: 3-safeguard passed, schema_version=4.1
- [ ] Step 3 nomadVar: 5 env vars configured (LLM toggles per owner choice)
- [ ] Step 4 Nomad jobs: 3 periodic jobs running (reconcile / comment-poll / cron)
- [ ] Step 5 Smoke A changes mode passed
- [ ] Step 5 Smoke B redo mode + placeholder comment passed
- [ ] Step 5 Smoke C cap exceeded passed
- [ ] Step 6 B.1.live failure_analysis verdict OK
- [ ] Step 6 C.2.live spec_drift score OK
- [ ] m5-handoff.yaml::t_deploy_status updated to complete
- [ ] m5-handoff.yaml::m5_acceptance live LLM fields updated
- [ ] (Passive) Tier-2 accumulation: ≥3 real dispatches over coming weeks

---

**Cross-references**:
- [aria-orchestrator/docs/m5-handoff.yaml](../../aria-orchestrator/docs/m5-handoff.yaml) — machine-readable handoff
- [aria-orchestrator/docs/validate-m5-handoff.py](../../aria-orchestrator/docs/validate-m5-handoff.py) — mechanical checks
- [aria-orchestrator/docs/architecture-decisions.md](../../aria-orchestrator/docs/architecture-decisions.md) — AD-M5-1..11
- [aria-orchestrator/docs/m4-handoff.yaml](../../aria-orchestrator/docs/m4-handoff.yaml) — parent
- [M4 Track A playbook (2026-05-09)](2026-05-09-track-a-deploy-playbook.md) — predecessor pattern

**Created**: 2026-05-15 — Phase 6 P6 (Spec 6.17-6.30)
**Status**: Owner-runnable; awaiting execution
