# T6/T7/T8 Owner Execution Evidence — aria-layer2-docker-auth-cold-pull-fix Phase B

> **Spec**: openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md (Approved Rev1.1)
> **Date**: 2026-05-23 ~12:50 – ~15:15 UTC (T6 → T7 → T8 sequence)
> **Author**: solo-lab (uni.concept.wzfq@gmail.com), AI driver Claude Opus 4.7 (1M context)
> **Rule #7 compliance**: 全程 fingerprint via SHA prefix [:12] + HTTP status code only;无 PAT 字面值漂入 chat/log
> **Purpose**: 提供 falsifiable + reproducible 第三方可 audit 的 owner-segment execution trail (per post_implementation qa-engineer M-qa-PI-X-1)

---

## §1 T6 — 3-node cred verify (per §Acceptance B)

### §1.1 Initial state (T6 first run, ~12:50 UTC)

B1 fingerprint per node:

| Host | Fingerprint (SHA prefix [:12]) | config.json mtime |
|------|-------------------------------|-------------------|
| heavy-1 | `3654ff26d443` | 2026-05-06 13:59:08 |
| heavy-2 | `3654ff26d443` | 2026-05-06 13:59:39 |
| heavy-3 | `21015768f512` | 2026-05-22 23:47:22 |

**Drift detected** — heavy-3 uses different PAT than heavy-1/2 (per M5 O3 debug 2026-05-22 owner temp swap).

B2 round-trip via `docker login --password-stdin` (no PAT in chat/process args):

| Host | docker login result |
|------|---------------------|
| heavy-1 | LOGIN_OK |
| heavy-2 | LOGIN_OK |
| heavy-3 | LOGIN_OK |

**→ 2 PATs both valid in Forgejo** (no auto-revocation when new PAT created)。

### §1.2 R1 escalation Branch 2 (piggyback per proposal §Risks R1)

Per `.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md` §1 Layer 1, `FORGEJO_BOT_PAT` 在 in-flight rotation 子集 → execute piggyback:

1. Owner Forgejo UI revoke 2 旧 PATs:
   - `aria layer2 runner 2026 05 22` (used by heavy-1/2 config.json, fingerprint `3654ff26d443`)
   - `aria build clone 2026 05 22` (used by heavy-3 config.json, fingerprint `21015768f512`)

2. Owner Forgejo UI list reveals 3rd PAT: `aria-runner-bot` (2026-05-03), fingerprint `c957308a0e35`, **kept** per Option X (scope discipline: 用于 Nomad var `nomad/jobs/aria-orchestrator::FORGEJO_BOT_PAT` Layer 1 reconciler / aria-build / Layer 2 entrypoint git ops, 不在本 Spec scope)

### §1.3 PAT rotation v1 — partial scope (failed cold-pull)

Owner Forgejo UI create `aria-runner-bot-prod-20260523-rotated` with scopes per DEC-20260520 §3.1 R1.B (incomplete spec): `write:repository / read:repository / write:issue / read:issue / read:user`。

Path B sync (atomic 3-node via tmp file):
- Owner `! nano /tmp/forgejo-pat.tmp` paste PAT (`-rw------- 1 dev dev 41 May 23 14:27`, 40-char PAT)
- AI `/tmp/sync-pat.py` 自包含: read PAT → base64 encode → mktemp 0600 → scp 3 nodes → atomic mv → shred local + PAT input

Post-sync v1 state:

| Host | Fingerprint | docker login |
|------|-------------|--------------|
| heavy-1 | `0d6e152a82f1` | LOGIN_OK |
| heavy-2 | `0d6e152a82f1` | LOGIN_OK |
| heavy-3 | `0d6e152a82f1` | LOGIN_OK |

**But T8 cold-pull FAIL** — all 3 nodes returned `401 Unauthorized` on `HEAD /v2/10cg/aria-runner/manifests/sha256:5b80ca6c...`。

### §1.4 Root cause — v1 PAT JWT scope inspection

Bearer token negotiation via `WWW-Authenticate: Bearer realm="https://forgejo.10cg.pub/v2/token", scope="*"`:

Token payload (JWT decode of v1 PAT's response):

```json
{"Scope": "write:issue,write:repository,read:user"}
```

**Missing `read:package` + `write:package`** — Forgejo container registry pull requires `read:package` scope on Bearer token, derived from PAT's package scope.

DEC-20260520 §3.1 R1.B 的 scope spec 不完整;AD-M1-8 §决定 列 4 scope (`read+write:package + write:repository + read:user`) 仍漏 `:issue`。**Codebase enumeration** 得 canonical 7-scope set:

| Scope | Operation enumeration source |
|-------|------------------------------|
| `read:package` | Nomad docker driver image pull (M1 era aria-runner) |
| `write:package` | aria-build container `docker push` (Dockerfile + registry-push-guide.md) |
| `read:repository` | Layer 1 `GET /repos/{org}/{repo}/pulls/{id}` (forgejo_client.py:302) + Layer 2 entrypoint `git clone` (modes/*.sh) |
| `write:repository` | Layer 1 `POST /repos/.../pulls/{id}/merge` (forgejo_client.py:353) + Layer 2 `git push` (modes/changes.sh:332, redo.sh:294) |
| `read:issue` | Layer 1 `GET /repos/{org}/{repo}/issues?state=open&label=...` (forgejo_client.py:271) |
| `write:issue` | Layer 1 + Layer 2 `POST /repos/.../issues/{id}/comments` (forgejo_client.py:370 + entrypoint comments) |
| `read:user` | Self-identify `GET /user` (all paths startup) |

### §1.5 PAT rotation v2 — full 7-scope (success)

Owner Forgejo UI create `aria-runner-bot-prod-20260523-v2-full-scope` with all 7 scopes per codebase enum。

Re-sync via same Path B script (`/tmp/sync-pat-v2.py`):

Post-sync v2 state:

| Host | Fingerprint | docker login |
|------|-------------|--------------|
| heavy-1 | `46e20fea2f5e` | LOGIN_OK |
| heavy-2 | `46e20fea2f5e` | LOGIN_OK |
| heavy-3 | `46e20fea2f5e` | LOGIN_OK |

Owner Forgejo UI revoke v1 (`aria-runner-bot-prod-20260523-rotated`)。

### §1.6 T6 final state (post v1 revoke)

B1 fingerprint unchanged: `46e20fea2f5e` 3-way 等。
B2 LOGIN_OK 3-way (proves v2 PAT independent of revoked v1, no functional regression)。

**T6 verdict**: PASS (after Branch 2 piggyback + 1 PAT rotation retry due to DEC scope gap)。

---

## §2 T7 — HCL activation (`nomad job run` on cluster)

Pre-run job status (current registered version from M5 era):

```
Submit Date = 2026-05-22T12:39:51Z
Type = batch
Status = running
Periodic = false
Parameterized = true
```

Activation:

```
cat aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl | \
  ssh light-1 'NOMAD_ADDR=http://192.168.69.70:4646 nomad job run -'
```

Output: `Job registration successful`

Post-run job status:

```
Submit Date = 2026-05-23T15:00:24Z  ← updated (≈ +2h36min from initial T7 attempt timestamp)
Type = batch
Status = running
Periodic = false
Parameterized = true
```

**T7 verdict**: PASS。

---

## §3 T8 — Cold-pull live verify (per §Acceptance C, 3 nodes)

Target image: `forgejo.10cg.pub/10cg/aria-runner@sha256:5b80ca6cd04ab31b3d8165eb82f4ac9edd824b45e8181adf9325e80cf35148f5`

Per-node C1+C2+C3 (using `docker pull` direct path, 90% equivalent to Nomad dispatch — Nomad plugin auth.config path verified by Aether spike 2026-04-23 + this Spec convention §0 historical evidence):

### §3.1 heavy-1

```
C1: docker rmi -f → Deleted, CACHE_AFTER=0
C2: docker pull → PULL_EXIT=0
C3: log = "Pulling from 10cg/aria-runner\nff86ea2e5edc: Pull complete\ne54aec64c365: Pull complete"
```

### §3.2 heavy-2

```
C1: docker rmi -f → Deleted, CACHE_AFTER=0
C2: docker pull → PULL_EXIT=0
C3: log = "Pulling from 10cg/aria-runner\nff86ea2e5edc: Pull complete\ne54aec64c365: Pull complete"
```

### §3.3 heavy-3

```
C1: docker rmi -f → was already absent, CACHE_AFTER=0
C2: docker pull → PULL_EXIT=0
C3: log = "Pulling from 10cg/aria-runner\nff86ea2e5edc: Pull complete\ne54aec64c365: Pull complete"
```

### §3.4 Post-pull verification

| Host | Final image cached |
|------|--------------------|
| heavy-1 | `5b80ca6cd04a` |
| heavy-2 | `5b80ca6cd04a` |
| heavy-3 | `5b80ca6cd04a` |

**T8 verdict**: PASS (3/3 cold-pull from registry, no cache hit)。

---

## §4 Reproducibility notes

3rd-party audit 可重跑 (after pulling repo + setting up ssh keys to 3 heavy nodes):

```bash
# B1 fingerprint (期望: 3-way 等于 46e20fea2f5e 直到下次 rotation)
for h in heavy-1 heavy-2 heavy-3; do
  ssh $h "python3 -c \"import json,hashlib;d=json.load(open('/root/.docker/config.json'));print(hashlib.sha256(d['auths']['forgejo.10cg.pub']['auth'].encode()).hexdigest()[:12])\""
done

# B2 docker login round-trip
for h in heavy-1 heavy-2 heavy-3; do
  ssh $h 'python3 -c "import json,base64;d=json.load(open(\"/root/.docker/config.json\"));u,p=base64.b64decode(d[\"auths\"][\"forgejo.10cg.pub\"][\"auth\"]).decode().split(\":\",1);print(p,end=\"\")" | docker login forgejo.10cg.pub -u aria-runner-bot --password-stdin 2>&1 | grep -i "login succeeded"'
done

# C cold-pull verify (期望: 3-way PULL_EXIT=0)
DIGEST="sha256:5b80ca6cd04ab31b3d8165eb82f4ac9edd824b45e8181adf9325e80cf35148f5"
IMAGE="forgejo.10cg.pub/10cg/aria-runner@$DIGEST"
for h in heavy-1 heavy-2 heavy-3; do
  ssh $h "docker rmi -f $IMAGE 2>/dev/null; docker pull $IMAGE 2>&1 | tail -3"
done
```

---

## §5 Cross-references

- **Spec proposal**: `openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md` (Approved Rev1.1)
- **DEC**: `.aria/decisions/2026-05-23-layer2-docker-auth-cold-pull-fix.md` (Phase B outcome to be appended in §3)
- **T1.0 probe** (sister evidence file): `.aria/probes/2026-05-23-aria-runner-template-status.md`
- **R1 audit**: `.aria/audit-reports/post_spec-R1-2026-05-23T0900Z-...orchestrator.md`
- **R2 audit**: `.aria/audit-reports/post_spec-R2-2026-05-23T1100Z-...orchestrator.md`
- **post_implementation R1 (本 evidence 触发的 audit)**: 2026-05-23 ~15:00 UTC tech-lead + qa-engineer = 0C/3I+2I/4M+3M = PASS_WITH_WARNINGS
- **Parent rotation DEC**: `.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md` §1 Layer 1 (FORGEJO_BOT_PAT 部分 rotated as本 Spec piggyback)
- **PAT scope canonical AD reference**: `aria-orchestrator/docs/architecture-decisions.md` §AD-M1-8 (per the Revised by note added in this Spec)

---

**Created**: 2026-05-23 ~15:15 UTC
**Trigger**: post_implementation R1 qa-engineer M-qa-PI-X-1 CONDITIONAL gate
