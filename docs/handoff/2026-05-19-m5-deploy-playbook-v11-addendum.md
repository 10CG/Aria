# Aria 2.0 M5 — T-deploy playbook v11 ADDENDUM (Spec X + Spec Y bundle)

> **Status**: Owner-runnable — AI does NOT auto-execute. Drafted 2026-05-19 by AI prep session (per US-025 close-gate C-path: "务实派 dry-run + 命令草稿").
> **Supersedes**: `2026-05-15-m5-deploy-playbook.md` Step 1-2 (additive image build + schema bumps) + Step 5 (real Layer 2 smoke replaces SQL-inject smoke).
> **Preserves**: `2026-05-15-m5-deploy-playbook.md` Step 3 (nomadVar config) + Step 4 (Nomad job redeploy) + Step 6 (Tier-1 live LLM gates) + Step 7 (Tier-2 accumulation) — those steps unchanged.
> **Target image**: `forgejo.10cg.pub/10CG/aria-runner:claude-m5-carry-09ff364-v11` (per handoff §6 naming)
> **Bundle**: Spec X (changes-mode) + Spec Y (redo-mode + close-old-PR + spec_drift fetcher + commit-lint retry)
> **Repos at HEAD**: Aria main `edbbfb4` · aria-orchestrator `09ff364` · aria submodule `v1.21.3` (1db66350)

---

## TL;DR — Delta vs 2026-05-15 playbook

| Step | 2026-05-15 (M5 Layer 1 only) | v11 (Spec X + Y bundle) |
|------|------------------------------|--------------------------|
| 1 Pre-deploy | aria-orchestrator master → aria-layer1 v0.4.0 | **same** (v0.4.0 unchanged) |
| **2 Schema migration** | apply 004 + 005 → v4.1 | apply 004 + 005 + **006 (new, spec_id col)** → **v4.2** |
| **2.5 Image build (NEW)** | (not in 2026-05-15) | **build claude-m5-carry-09ff364-v11 + push + update m1-handoff.yaml** |
| 3 nomadVar | 5 env vars | **same 5 env vars** (no change) |
| 4 Nomad redeploy | reconcile + comment-poll + cron | **same 3 periodic jobs** (HCL unchanged) |
| **5 Smoke E2E** | A/B/C SQL-inject (no container) | **A/B/C real Layer 2 dispatch** (verifies new image actually runs) |
| 6 Tier-1 live LLM | B.1.live + C.2.live (¥0.10) | **same** |
| 7 Tier-2 | passive accumulation | **same** |

**New steps total time**: +25min (Step 2.5 build/push ~15min + Step 5 real-container smoke +10min over SQL-inject).

---

## Step 1 — Pre-deploy (~15min) — UNCHANGED from 2026-05-15

```bash
ssh aether-light-1
cd /opt/aria-orchestrator
git fetch origin
git checkout master
git pull origin master

# Verify HEAD matches expected post-Spec-Y master
git log -1 --oneline
# Expected: "Merge pull request '#13' from feature/spec-y-..." or later
# Specifically: aria-orchestrator master HEAD == 09ff364 (Spec Y merged 2026-05-19)

# Refresh venv
source /opt/aria-orchestrator/venv/bin/activate
pip install -e hermes-extensions/aria-layer1
pip show aria-layer1 | grep Version
# Expected: 0.4.0
```

---

## Step 2 — Schema migration v4.1 → v4.2 (3-safeguard, ~10min)

> **Delta vs 2026-05-15**: migration 006 (Spec Y T0 — adds `spec_id` column for `spec_drift_input_fetcher` prod impl) is new. If you have NOT yet deployed M5 to prod, you'll apply 004 + 005 + 006 together. If you HAVE deployed M5 (so prod is at v4.1), you'll apply only 006.

```bash
DB_PATH=/opt/aether-volumes/aria-layer1/data/dispatches.db
BACKUP_DIR=/opt/aether-volumes/aria-layer1/data/backups
TS=$(date +%Y%m%dT%H%M%S)

# --- Safeguard 1: Atomic backup via Python sqlite3.backup() (WAL-safe) ---
mkdir -p "$BACKUP_DIR"
python3 -c "
import sqlite3
src = sqlite3.connect('$DB_PATH')
dst = sqlite3.connect('$BACKUP_DIR/dispatches.db.pre-v4.2.$TS')
src.backup(dst)
dst.close(); src.close()
print('backup OK')
"

# --- Safeguard 2: integrity check + row count ---
sqlite3 "$BACKUP_DIR/dispatches.db.pre-v4.2.$TS" "PRAGMA integrity_check;"
# Expected: ok
BACKUP_ROW_COUNT=$(sqlite3 "$BACKUP_DIR/dispatches.db.pre-v4.2.$TS" "SELECT COUNT(*) FROM dispatches;")
echo "backup row count: $BACKUP_ROW_COUNT"

# --- Safeguard 3: dry-run on a copy ---
cp "$BACKUP_DIR/dispatches.db.pre-v4.2.$TS" /tmp/dispatches.dryrun.db
python3 -c "
import sqlite3
from aria_layer1.schema_migrate import apply_migrations
conn = sqlite3.connect('/tmp/dispatches.dryrun.db')
conn.execute('PRAGMA foreign_keys=ON')
result = apply_migrations(conn)
print('dry-run applied:', result['applied'])
print('to_version:', result['to_version'])
print('integrity:', conn.execute('PRAGMA integrity_check').fetchone()[0])
print('row count:', conn.execute('SELECT COUNT(*) FROM dispatches').fetchone()[0])
# v4.2 verification: spec_id column should exist
cols = [c[1] for c in conn.execute(\"PRAGMA table_info(dispatches)\").fetchall()]
print('has spec_id col:', 'spec_id' in cols)
"
# Expected (fresh prod from v3.0): applied=['004','005','006']; to_version='4.2'; integrity=ok; spec_id=True
# Expected (already on v4.1):     applied=['006'];               to_version='4.2'; integrity=ok; spec_id=True
# Expected (already on v4.2):     applied=[];                    to_version='4.2'; (no-op)

# --- Apply on prod (only after dry-run PASS) ---
python3 -c "
import sqlite3
from aria_layer1.schema_migrate import apply_migrations
conn = sqlite3.connect('$DB_PATH')
conn.execute('PRAGMA foreign_keys=ON')
result = apply_migrations(conn)
print('prod applied:', result['applied'])
print('schema_version:', conn.execute(\"SELECT value FROM schema_meta WHERE key='schema_version'\").fetchone()[0])
print('integrity:', conn.execute('PRAGMA integrity_check').fetchone()[0])
print('row count:', conn.execute('SELECT COUNT(*) FROM dispatches').fetchone()[0])
cols = [c[1] for c in conn.execute(\"PRAGMA table_info(dispatches)\").fetchall()]
print('has spec_id col:', 'spec_id' in cols)
"
# Expected: schema_version=4.2 + has spec_id col=True + row count unchanged
```

**Rollback**: `cp "$BACKUP_DIR/dispatches.db.pre-v4.2.$TS" "$DB_PATH"` — no schema changes applied.

---

## Step 2.5 — Image v11 build + push (~15min, NEW)

> **Background**: Spec X + Y modified `docker/aria-runner/` files (entrypoint.sh dispatcher + modes/{initial,changes,redo}.sh + lib/*.sh helpers + prompts/). These are COPY'd at image build time, so a new image must be built and the production HCL re-pointed to its sha256 digest. The HCL itself (`nomad/jobs/aria-layer2-runner.hcl`) does NOT change — it already reads `IMAGE_SHA` from dispatch meta. What changes is the value of `image_sha_final` in `aria-orchestrator/docs/m1-handoff.yaml` (which Layer 1's `extension.py::_read_m1_image_sha` reads at dispatch time).

### 2.5.1 — Enter aria-build container (heavy node)

```bash
# From dev machine (you, owner). aria-build container should already be running on heavy-1/2/3.
export NOMAD_ADDR="http://192.168.69.70:4646"   # per memory reference_10cg_cluster_internal_routing
ALLOC=$(nomad job status aria-build | awk '/running/{print $1; exit}')
test -n "$ALLOC" || { echo "ERR: no running aria-build alloc; deploy per nomad/jobs/aria-build-README.md Step 2"; exit 1; }
nomad alloc exec -task build -i -t "$ALLOC" /bin/sh
```

If aria-build is NOT running, follow `aria-orchestrator/nomad/jobs/aria-build-README.md` Step 2 first (registers the job with Nomad).

### 2.5.2 — Inside aria-build container: clone repo + build

```sh
# Confirm docker login already done by aria-build entrypoint
cat ~/.docker/config.json | jq '.auths | keys'
# Expected: ["forgejo.10cg.pub"]

# Confirm env vars present
env | grep -E "^(FORGEJO|ARIA)_"
# Expected: FORGEJO_BOT_USER=aria-runner-bot, FORGEJO_BOT_PAT=<set>, FORGEJO_REGISTRY=forgejo.10cg.pub, ARIA_IMAGE_REPO=10CG/aria-runner

# Clone (or pull) Aria meta-repo with submodules. The image must include aria/ submodule
# (Dockerfile line 62: COPY aria/ /opt/aria-plugin/).
mkdir -p /tmp/build && cd /tmp/build
if [ -d Aria/.git ]; then
  cd Aria
  git fetch origin
  git checkout master && git pull --ff-only origin master
  git submodule update --init --recursive
else
  # Use Forgejo internal IP (per memory: bypasses Cloudflare Access)
  git clone --recurse-submodules \
    "https://aria-runner-bot:$FORGEJO_BOT_PAT@192.168.69.200:3000/10CG/Aria.git" Aria
  cd Aria
fi

# Verify HEADs match expected (paste-time sanity)
git rev-parse --short HEAD                       # Expected: edbbfb4 (or later)
git -C aria-orchestrator rev-parse --short HEAD  # Expected: 09ff364
git -C aria               rev-parse --short HEAD # Expected: 1db66350 (aria-plugin v1.21.3)

# Compute tag
ORCH_SHA=$(git -C aria-orchestrator rev-parse --short=7 HEAD)
TAG="claude-m5-carry-${ORCH_SHA}-v11"
echo "Building tag: $FORGEJO_REGISTRY/$ARIA_IMAGE_REPO:$TAG"

# Build (build context = Aria meta-repo root per Dockerfile COPY paths)
docker build \
  --platform linux/amd64 \
  --build-arg DEPLOY_ENV=internal \
  -f aria-orchestrator/docker/aria-runner/Dockerfile \
  -t "$FORGEJO_REGISTRY/$ARIA_IMAGE_REPO:$TAG" \
  -t "$FORGEJO_REGISTRY/$ARIA_IMAGE_REPO:claude-latest" \
  .
# Expected: ~3-5min on warm cache, ~8-12min cold (apt + npm install -g @anthropic-ai/claude-code)

# Push both tags
docker push "$FORGEJO_REGISTRY/$ARIA_IMAGE_REPO:$TAG"
docker push "$FORGEJO_REGISTRY/$ARIA_IMAGE_REPO:claude-latest"

# Capture the sha256 digest (immutable pin per AD-M1-7)
docker inspect --format='{{index .RepoDigests 0}}' "$FORGEJO_REGISTRY/$ARIA_IMAGE_REPO:$TAG"
# Expected output:
#   forgejo.10cg.pub/10CG/aria-runner@sha256:<64-hex-chars>
# Copy the sha256 part — needed for Step 2.5.3.

# Optionally verify the digest pulls back correctly:
docker pull "$FORGEJO_REGISTRY/$ARIA_IMAGE_REPO@sha256:<digest-from-above>"

exit  # leave aria-build container
```

### 2.5.3 — Update m1-handoff.yaml with new image sha (back on light-1)

```bash
# Back on aether-light-1
cd /opt/aria-orchestrator

# Edit aria-orchestrator/docs/m1-handoff.yaml lines 29-35:
#   registry: "forgejo.10cg.pub/10CG/aria-runner"  (unchanged)
#   image_tag_mutable: "aria-runner:claude-latest" (unchanged)
#   image_tag_immutable_pattern: "aria-runner:claude-<sha>" (unchanged)
#   image_sha256_final: "sha256:<NEW-DIGEST>"   <-- UPDATE
#   image_sha_final: "<NEW-SHA-PREFIX>"          <-- UPDATE (orch short sha)
#
# Recommended commit:
git checkout -b ops/v11-image-deploy
sed -i "s|sha256:e46be19da4d9ab782d4be50c15f0939d34c407ffac04fa640cc9f299d4b9075e|sha256:<NEW>|" \
  docs/m1-handoff.yaml
sed -i 's|image_sha_final: "5154c13"|image_sha_final: "09ff364"|' \
  docs/m1-handoff.yaml
git diff docs/m1-handoff.yaml
# Verify diff is exactly 2 lines (image_sha256_final + image_sha_final)
git add docs/m1-handoff.yaml
git commit -m "ops(deploy): bump image_sha_final to v11 (Spec X + Y bundle, claude-m5-carry-09ff364-v11)

per docs/handoff/2026-05-19-m5-deploy-playbook-v11-addendum.md Step 2.5

Image: forgejo.10cg.pub/10CG/aria-runner:claude-m5-carry-09ff364-v11
Digest: sha256:<NEW>
Bundle: Spec X (changes-mode) + Spec Y (redo/close-old-PR/spec_drift/commit-lint)"
git push origin ops/v11-image-deploy

# Open PR via Forgejo or merge directly to master per repo convention
# After merge:
git checkout master
git pull origin master
```

> **Why the m1-handoff.yaml change**: Layer 1's `extension.py:_read_m1_image_sha` reads `image_sha_final` from this file at dispatch time and passes it as `IMAGE_SHA` meta to Nomad. The HCL pulls from `registry.10cg.pub/aria-runner@sha256:${NOMAD_META_IMAGE_SHA}` — **but the actual registry in m1-handoff.yaml is `forgejo.10cg.pub/10CG/aria-runner`**. There's a paper inconsistency between HCL `registry.10cg.pub` placeholder string and prod registry. Action item: verify which registry HCL actually pulls from at dispatch time — see "Open verification" below.

### 2.5.4 — Reload Layer 1 cached image sha (light-1)

`extension.py::_read_m1_image_sha` caches the sha in `self._cached_image_sha` after first read. Layer 1 process must be restarted so it re-reads the updated m1-handoff.yaml on next dispatch.

```bash
# Restart Hermes (aria-orchestrator job has Layer 1 loaded as Hermes extension)
nomad job restart aria-orchestrator
# Or stop+rerun for clean state:
# nomad job stop aria-orchestrator && nomad job run /opt/aria-orchestrator/deploy/aria-orchestrator.nomad.hcl

# Verify Hermes alloc is healthy + Layer 1 picked up new sha
sleep 15
nomad job status aria-orchestrator | head -20
# Spot-check log for "image_sha" mention or just rely on Step 5 smoke
nomad alloc logs $(nomad job status aria-orchestrator | awk '/running/{print $1; exit}') 2>&1 | grep -i "aria.layer1\|image_sha" | tail
```

### Open verification (BEFORE Step 5 dispatch)

```bash
# Verify aria-layer2-runner.hcl will pull from the SAME registry that was pushed to:
grep -E "image\s*=\s*\"" /opt/aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl
# Current value: image = "registry.10cg.pub/aria-runner@sha256:${NOMAD_META_IMAGE_SHA}"
# This is the M3 placeholder per HCL header note. If light-1 production still uses M1 runner template
# (forgejo.10cg.pub/10CG/aria-runner), Step 5 smoke will fail with image-pull error.
#
# REMEDIATION (if mismatched): edit HCL line 159 to
#   image = "forgejo.10cg.pub/10CG/aria-runner@sha256:${NOMAD_META_IMAGE_SHA}"
# Then nomad job run that HCL. Document the registry decision in m1-handoff.yaml.
```

---

## Step 3 — nomadVar configuration (~5min) — UNCHANGED

Per `2026-05-15-m5-deploy-playbook.md` Step 3. The 5 env vars are job-level config, not image-level:

```hcl
env {
  ARIA_REWORK_MAX_ROUND          = "3"
  ARIA_SPEC_DRIFT_THRESHOLD      = "70"
  ARIA_FAIL_RETRY_CONFIDENCE_MIN = "0.7"
  ARIA_FAILURE_ANALYSIS_ENABLED  = "0"     # owner choice; 1=enable post-Tier-1
  ARIA_SPEC_DRIFT_ENABLED        = "0"     # owner choice; 1=enable post-Tier-1
}
```

---

## Step 4 — Nomad Layer 1 job redeploy (~10min) — UNCHANGED

Per `2026-05-15-m5-deploy-playbook.md` Step 4. Run all three:

```bash
cd /opt/aria-orchestrator
nomad job validate deploy/aria-orchestrator.nomad.hcl
nomad job validate deploy/aria-layer1-reconcile.nomad.hcl
nomad job validate deploy/aria-layer1-comment-poll.nomad.hcl
nomad job validate deploy/aria-layer1-cron.nomad.hcl

nomad job stop -purge aria-layer1-reconcile
nomad job stop -purge aria-layer1-comment-poll
nomad job stop -purge aria-layer1-cron

nomad job run deploy/aria-layer1-reconcile.nomad.hcl
nomad job run deploy/aria-layer1-comment-poll.nomad.hcl
nomad job run deploy/aria-layer1-cron.nomad.hcl

# Verify v4.2 cols visible (new: spec_id)
sqlite3 "$DB_PATH" "PRAGMA table_info(dispatches);" | grep -E "spec_id|risk_tier|rework_"
# Expected: 6 cols visible — spec_id (NEW), risk_tier, rework_of, rework_round, rework_mode, rework_feedback
```

---

## Step 4.5 — Layer 2 runner template registration (NEW, only if needed)

```bash
# If aria-layer2-runner job is NOT yet registered (parameterized template),
# register it now. Idempotent — re-registering with same HCL is no-op.
nomad job validate nomad/jobs/aria-layer2-runner.hcl
nomad job run     nomad/jobs/aria-layer2-runner.hcl
nomad job status  aria-layer2-runner
# Expected: Status=running, Type=batch (parameterized), 0 allocs (template waits for dispatch)
```

---

## Step 5 — Smoke E2E (~40min, NEW: real Layer 2 dispatch)

> **Delta vs 2026-05-15**: Original smoke was SQL-inject + verify Layer 1 wiring only. v11 image now contains real Layer 2 mode handlers, so smoke is upgraded to actually dispatch the Layer 2 container and verify it executes the mode logic. SQL-inject pattern preserved as fallback if registry pull fails.

### Smoke A — changes mode real Layer 2 dispatch (M5 P3 Spec 3.6 + Spec X)

```bash
# Pre-req: a real PR on a demo issue. Create or reuse.
DISPATCH_ID="smoke-v11-changes-$(date +%s)"
ISSUE_ID="DEMO-V11-001"
PR_ID=99001  # OWNER: replace with real demo PR # (create one with trivial change)
IDEMPOTENCY_KEY="${DISPATCH_ID}-changes"

# Read current image digest from prod m1-handoff
IMAGE_DIGEST=$(grep image_sha256_final /opt/aria-orchestrator/docs/m1-handoff.yaml | awk -F'"' '{print $2}')
echo "Will dispatch with IMAGE_SHA=$IMAGE_DIGEST"

# Inject the parent dispatch row at S7 (so /aria changes: routing has a target)
sqlite3 "$DB_PATH" "
  INSERT INTO dispatches (issue_id, dispatch_id, state, state_entered_at,
                          image_sha, pr_id, risk_tier, risk_tier_stub,
                          human_gate_entered_at, notification_status)
  VALUES ('$ISSUE_ID', '$DISPATCH_ID', 'S7_HUMAN_GATE', '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
          '$IMAGE_DIGEST', $PR_ID, 'always', 'always',
          '$(date -u +%Y-%m-%dT%H:%M:%SZ)', '200');
"

# OWNER: post /aria changes: <feedback> on the Forgejo PR via Forgejo UI or CLI:
#   forgejo POST /repos/10CG/Aria/issues/$PR_ID/comments \
#     -d '{"body":"/aria changes: please refactor function X to use named args"}'

# Wait up to 60s for comment_poll to pick up the comment + create the rework dispatch
sleep 75
sqlite3 "$DB_PATH" "
  SELECT dispatch_id, state, fail_reason, rework_mode, rework_round, rework_of, rework_feedback
  FROM dispatches WHERE issue_id='$ISSUE_ID' ORDER BY attempt_count;
"
# Expected (Layer 1 wiring):
#   parent → S_FAIL changes_requested NULL 0 NULL NULL
#   child  → S4_LAUNCH NULL changes 1 $DISPATCH_ID "please refactor function X..."

# Wait up to 5min for Layer 2 dispatch to actually run (Nomad batch + image pull)
echo "Watching Layer 2 alloc..."
sleep 300
CHILD_ID=$(sqlite3 "$DB_PATH" "SELECT dispatch_id FROM dispatches WHERE rework_of='$DISPATCH_ID' LIMIT 1;")
echo "Child dispatch: $CHILD_ID"

# Find the alloc that ran for this dispatch
nomad job status -evals aria-layer2-runner | head -30
ALLOC=$(nomad eval list -job aria-layer2-runner | awk -v id="$CHILD_ID" '$0 ~ id {print $2; exit}')
# Actually best to find via meta DISPATCH_ID match — depends on Nomad CLI version:
nomad alloc status -json $ALLOC 2>/dev/null | jq -r '.JobMeta.DISPATCH_ID'

# Read alloc stderr (modes/changes.sh logs to stderr per Spec X convention)
nomad alloc logs -stderr $ALLOC | head -50
# Expected log markers (per modes/changes.sh):
#   [changes] starting REWORK_MODE=changes round=1 ...
#   [changes] fetched parent PR branch via Forgejo API
#   [changes] assembled prompt (size=NNNN bytes)
#   [changes] claude -p invocation started
#   [changes] git push --force-with-lease=... OK
#   [changes] PASS

# Confirm new commit was force-pushed to the parent PR branch
forgejo GET /repos/10CG/Aria/pulls/$PR_ID/commits | jq '.[-1] | {sha, message: .commit.message}'
# Expected: latest commit SHA different from baseline; commit author = aria-runner-bot

# Confirm audit log records rework_cycle outcome=success
sqlite3 "$DB_PATH" "
  SELECT event_type, payload_json FROM dispatch_audit_log
  WHERE dispatch_id='$CHILD_ID' ORDER BY id;
" | head
# Expected: rework_cycle event with outcome='changes_applied' (or similar per Spec X audit schema)
```

### Smoke B — redo mode real Layer 2 dispatch + close-old-PR (Spec Y T2 + T3)

```bash
# Same setup pattern as Smoke A, different issue + PR + comment
DISPATCH_ID="smoke-v11-redo-$(date +%s)"
ISSUE_ID="DEMO-V11-002"
PR_ID=99002  # OWNER: fresh demo PR

sqlite3 "$DB_PATH" "INSERT INTO dispatches ..."   # same template as Smoke A

# OWNER: post /aria redo: <feedback>
#   forgejo POST /repos/10CG/Aria/issues/$PR_ID/comments \
#     -d '{"body":"/aria redo: start fresh — the approach is wrong, do XYZ instead"}'

sleep 75
# Verify Layer 1 created the rework row with rework_mode=redo + pr_id=NULL + state=S0_IDLE
sqlite3 "$DB_PATH" "
  SELECT state, rework_mode, pr_id FROM dispatches WHERE rework_of='$DISPATCH_ID';
"
# Expected: S0_IDLE redo NULL

# Verify placeholder comment posted to old PR
forgejo GET /repos/10CG/Aria/issues/$PR_ID/comments | grep -i "superseded by a new dispatch"
# Expected: 1 match (M5 P4 inline placeholder behavior)

# Wait for Layer 2 to actually run (cron tick + full cycle: ~5-15min)
sleep 600

# Find the newly-created PR from Layer 2 redo.sh
CHILD_ID=$(sqlite3 "$DB_PATH" "SELECT dispatch_id FROM dispatches WHERE rework_of='$DISPATCH_ID';")
NEW_PR_ID=$(sqlite3 "$DB_PATH" "SELECT pr_id FROM dispatches WHERE dispatch_id='$CHILD_ID';")
echo "New PR from redo: #$NEW_PR_ID"

# Verify Spec Y T3 close-old-PR fired: old PR has '_Superseded by #<new>_' comment + state=closed
forgejo GET /repos/10CG/Aria/issues/$PR_ID | jq '.state, .closed_at'
# Expected: "closed", non-null closed_at
forgejo GET /repos/10CG/Aria/issues/$PR_ID/comments | jq '.[] | select(.body | contains("Superseded by")) | .body'
# Expected: comment body "_Superseded by #<NEW_PR_ID>_"

# Verify alloc stderr shows redo.sh markers including new_pr_id
ALLOC=$(...)  # same find-alloc pattern as Smoke A
nomad alloc logs -stderr $ALLOC | grep -E "\[redo\] PASS new_pr_id="
# Expected: "[redo] PASS new_pr_id=<NEW_PR_ID>" exact format (Spec Y T3 marker for Layer 1)

# Audit log: rework_cycle event with new_pr_id_source='alloc_logs' (per Finding #5 OD)
sqlite3 "$DB_PATH" "
  SELECT json_extract(payload_json, '\$.new_pr_id_source')
  FROM dispatch_audit_log WHERE event_type='rework_cycle' AND dispatch_id='$CHILD_ID';
"
# Expected: alloc_logs
```

### Smoke C — commit-lint retry (Spec Y T5)

```bash
# Smoke C verifies the Layer 2 bash commit-lint hook (lib/commit-lint-validate.sh + lib/commit-lint-retry.sh)
# fires when claude generates a malformed commit message. Hard to trigger deterministically — owner can either:
#   (a) Inspect a real rework dispatch logs for "[commit-lint]" markers when claude happens to produce
#       a non-conventional-commit message (passive observation; no scripted trigger).
#   (b) Use the dedicated unit test we shipped in Spec Y T6:
cd /opt/aria-orchestrator
bash docker/aria-runner/tests/commit-lint-validate.sh
# Expected: "PASS: all 24 cases" (Spec Y T6 +24 cases for commit-lint-validate)
bash docker/aria-runner/tests/changes-mode/commit-lint-retry-tests.sh 2>/dev/null || \
  echo "Note: retry-tests script name may differ; check docker/aria-runner/tests/ for the actual file"
```

### Smoke C (cap exceeded, original 2026-05-15 — RETAINED as Tier-2 corner case)

```bash
# Build 3-round chain, attempt round 4 — same as original 2026-05-15 playbook Smoke C.
# Verifies AD-M5-2 rework_max_round=3 cap fires.
# (Section unchanged; see 2026-05-15-m5-deploy-playbook.md Step 5 Smoke C.)
```

---

## Step 6 — Tier-1 live LLM gates (~5min, owner-triggered) — UNCHANGED

Per `2026-05-15-m5-deploy-playbook.md` Step 6. Set `ARIA_FAILURE_ANALYSIS_ENABLED=1` + `ARIA_SPEC_DRIFT_ENABLED=1`, run reconciler, verify audit log.

**New Spec Y benefit**: `spec_drift_input_fetcher` is now prod impl (not stub), so C.2.live actually fetches OpenSpec proposal + PR diff. Verify:

```bash
sqlite3 "$DB_PATH" "
  SELECT json_extract(payload_json, '\$.score'),
         json_extract(payload_json, '\$.outcome'),
         json_extract(payload_json, '\$.inputs_present')
  FROM dispatch_audit_log WHERE event_type='spec_drift_detected' LIMIT 1;
"
# Expected: score 0-100; outcome ∈ {clean, drift_detected, parse_failed}
#           inputs_present=true (vs M5 stub which always returned empty inputs)
```

---

## Step 7 — Tier-2 accumulation (passive) — UNCHANGED

Per `2026-05-15-m5-deploy-playbook.md` Step 7. ≥3 real owner workload dispatches with ≥1 each of changes/redo/reject paths. **D7 absorption clause**: this Tier-2 path coverage is now subsumed by US-026 M6b ≥10 dispatch verification gate.

---

## Writeback to m5-handoff.yaml (post-deploy)

```yaml
t_deploy_status:
  status: complete
  date: 2026-05-XX
  image_v11_sha256: "sha256:<NEW-DIGEST>"
  image_v11_tag: "claude-m5-carry-09ff364-v11"
  bundle: "Spec X (changes-mode) + Spec Y (redo + close-old-PR + spec_drift fetcher + commit-lint)"
  fixes_shipped: ["<any deploy-time fixes>"]
  smoke_verification:
    - "Smoke A changes mode: parent S_FAIL + child force-push verified via Forgejo PR commits API"
    - "Smoke B redo mode: old PR closed + '_Superseded by #N_' comment + new PR created + alloc_logs new_pr_id marker"
    - "Smoke C commit-lint: tests/commit-lint-validate.sh 24/24 PASS"
m5_acceptance:
  b1_live_llm_passed: true   # verdict_action + confidence verified
  c2_live_llm_passed: true   # score ∈ [0,100] verified; inputs_present=true (Spec Y prod fetcher)
```

Then run `python3 docs/validate-m5-handoff.py -v` — all 6 checks must PASS (Spec Y T7 added `spec_y_absorbed_m5_carryovers` check).

---

## Rollback paths

| Failure point | Rollback |
|---|---|
| Step 1 venv | `pip install aria-layer1==0.3.0` (pre-M5) |
| Step 2 dry-run | No prod change — investigate |
| Step 2 prod | `cp $BACKUP_DIR/dispatches.db.pre-v4.2.$TS $DB_PATH` |
| **Step 2.5 build fail** | image v9 still in registry; m1-handoff.yaml unchanged; no impact on prod |
| **Step 2.5 push fail** | Re-auth via `nomad alloc exec` aria-build container (PAT may have rotated) |
| **Step 2.5 m1-handoff update fail** | Revert `ops/v11-image-deploy` branch + redeploy; Layer 1 keeps using v9 sha |
| Step 3 nomadVar | Revert env in HCL + restart job |
| Step 4 job fail | `nomad job stop $JOB` + revert HCL + run previous version |
| **Step 5 image pull fail** | Verify HCL `image = ...` matches the registry we pushed to (see Open verification §2.5.3) |
| Step 5 smoke fail (Layer 2 logic) | Document in m5-handoff.yaml::open_issues; **do NOT** proceed to live gates |
| Step 6 LLM gate fail | `ARIA_*_ENABLED=0` + investigate audit log parse_failed |
| **Step 6 spec_drift inputs_present=false** | Verify aria-orchestrator master at 09ff364 includes Spec Y T4 commit `e536204` |

---

## Owner sign-off checklist (v11 extends 2026-05-15)

- [ ] Step 1 pre-deploy: aria-layer1 v0.4.0 installed on light-1
- [ ] Step 2 schema migration: 3-safeguard passed, schema_version=**4.2**, spec_id col present
- [ ] **Step 2.5 image build: tag claude-m5-carry-09ff364-v11 pushed to forgejo.10cg.pub/10CG/aria-runner**
- [ ] **Step 2.5 m1-handoff.yaml image_sha256_final + image_sha_final updated + committed to master**
- [ ] **Step 2.5 Hermes restarted (Layer 1 picks up new cached sha)**
- [ ] Step 3 nomadVar: 5 env vars configured (LLM toggles per owner choice)
- [ ] Step 4 Nomad jobs: 3 periodic Layer 1 jobs running
- [ ] Step 4.5 aria-layer2-runner parameterized template registered (if first deploy)
- [ ] **Step 5 Smoke A (changes mode real Layer 2): force-push verified**
- [ ] **Step 5 Smoke B (redo mode real Layer 2 + close-old-PR): new PR + Superseded comment + alloc_logs marker**
- [ ] **Step 5 Smoke C (commit-lint hook test 24/24 PASS)**
- [ ] Step 5 Smoke C-cap (rework_max_round=3 cap fires)
- [ ] Step 6 B.1.live failure_analysis verdict OK
- [ ] Step 6 C.2.live spec_drift score OK + inputs_present=true (Spec Y prod fetcher)
- [ ] m5-handoff.yaml::t_deploy_status updated to complete + image_v11_sha256 field added
- [ ] m5-handoff.yaml::m5_acceptance live LLM fields updated
- [ ] (Passive) Tier-2 accumulation: subsumed by US-026 M6b ≥10 dispatch gate per D7

---

## Cross-references

- [2026-05-15-m5-deploy-playbook.md](2026-05-15-m5-deploy-playbook.md) — original M5 Layer 1 playbook (this addendum extends it)
- [2026-05-19-spec-y-t3-t8-shipped.md](2026-05-19-spec-y-t3-t8-shipped.md) — Spec Y full A→D cycle handoff (commits captured in §1)
- [openspec/archive/2026-05-16-aria-2.0-m5-carryover-layer2-changes-mode/](../../openspec/archive/2026-05-16-aria-2.0-m5-carryover-layer2-changes-mode/) — Spec X archive
- [openspec/archive/2026-05-19-aria-2.0-m5-carryover-layer2-redo-mode-aux/](../../openspec/archive/2026-05-19-aria-2.0-m5-carryover-layer2-redo-mode-aux/) — Spec Y archive
- [aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl](../../aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl) — Layer 2 parameterized template
- [aria-orchestrator/nomad/jobs/aria-build-README.md](../../aria-orchestrator/nomad/jobs/aria-build-README.md) — build container deploy guide
- [aria-orchestrator/docker/aria-runner/Dockerfile](../../aria-orchestrator/docker/aria-runner/Dockerfile) — image build spec

---

## AI prep verification (this session, 2026-05-19)

Local sanity-checks performed by AI before this draft (no prod commands run):

| Check | Status |
|-------|--------|
| Dockerfile parses + all COPY sources exist (entrypoint.sh, modes/, lib/, prompts/, aria/) | ✅ |
| aria-plugin version baked into image (aria/.claude-plugin/plugin.json) | ✅ v1.21.3 |
| Layer 1 pkg version (aria-layer1 pyproject.toml) | ✅ 0.4.0 |
| Schema migrations list (006_schema_v4.2_add_spec_id.sql + _LATEST_SCHEMA_VERSION="4.2") | ✅ |
| aria-orchestrator HEAD = 09ff364 (Spec Y merge) | ✅ |
| Multi-remote parity (origin + github) | ✅ all equal |

## Open items — DECIDED 2026-05-19 (owner OD before addendum commit)

1. **Registry domain in HCL line 159** — **DECIDED: option (a)** — edit HCL to `forgejo.10cg.pub/10CG/aria-runner@sha256:${NOMAD_META_IMAGE_SHA}` to match prod registry. Sets up of `registry.10cg.pub` as a separate Harbor/Zot registry per AD-M3-1 intent is tracked as a **post-M6 separate spec** (no scope leak into v11 deploy). Action: owner edits HCL line 159 as part of Step 2.5.3 (or pre-Step-5 if HCL is the only blocker), commits to aria-orchestrator master (with submodule pointer bump on Aria main).

2. **Image tag convention** — **DECIDED: `claude-m5-carry-<sha>-v11` prefix.** US-025/Spec X+Y are filed under M5 carryover archive paths (`openspec/archive/2026-05-{16,19}-aria-2.0-m5-carryover-...`), so `m5-carry-` reflects authoritative archive location. Brainstorm D5's `m6a-` was internal-only naming during planning, now retired.

3. **Rule #8 pre-merge gate for the m1-handoff.yaml bump commit** — **DECIDED: run the gate.** Owner explicitly invokes `aether ci status --branch master --in-flight --json` at Step 2.5.3 before pushing the ops branch / merging the PR. Expected output: `"runs":[]` → safe. If non-empty, wait + retry per phase-c-integrator C.2.4 `wait_recoverable` semantics. This addendum itself was committed under the same gate (verified GREEN 2026-05-19 pre-commit).

---

**Drafted by**: AI prep session 2026-05-19
**Status**: Owner-runnable; awaiting execution
**ETA full execution**: ~80min (15+10+15+5+10+40 of Steps 1-5) + ~5min Step 6 + ongoing Step 7 passive
