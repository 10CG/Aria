# Multi-Remote Push + Post-Push Verify Flow

## Goal

Push `master` to two remotes (`origin` = Forgejo, `github`), then **mechanically verify** that each remote's `master` HEAD SHA equals the local `master` HEAD SHA. Do **not** trust the "Everything up-to-date" string — it only means "no new commits to send from your cached remote-tracking branch", not "the remote's HEAD matches your local HEAD right now".

---

## Why textual output is insufficient

`git push` emits messages based on the **local view** of the remote (cached in `refs/remotes/<remote>/*`):

- `"Everything up-to-date"` — the local remote-tracking ref already equals local `HEAD`. But the remote-tracking ref could be stale (e.g. someone force-pushed on the remote, or a prior push was actually rejected and you didn't notice).
- A successful-looking push line like `abc123..def456  master -> master` can still be followed by a hook rejection on some servers — always check the process exit code.
- Network proxies (e.g. Cloudflare Access in front of Forgejo) can return cached responses.

The only reliable signal is: **ask each remote directly what SHA its `refs/heads/master` points to, and compare to the local SHA byte-for-byte.**

---

## Pre-flight checks

Run these before pushing. Each step uses absolute paths / `-C` form (no `cd` chain) per project convention.

```bash
# 1. Confirm we are on master and the tree is clean
git -C /home/dev/Aria rev-parse --abbrev-ref HEAD          # expect: master
git -C /home/dev/Aria status --porcelain                    # expect: empty

# 2. Confirm both remotes exist and point where we expect
git -C /home/dev/Aria remote -v
#   origin  <forgejo-url>  (fetch/push)
#   github  <github-url>   (fetch/push)

# 3. Capture local HEAD SHA — this is the "truth" we verify against
LOCAL_SHA=$(git -C /home/dev/Aria rev-parse HEAD)
echo "LOCAL_SHA=$LOCAL_SHA"

# 4. Refresh remote-tracking refs so any pre-existing divergence is visible
git -C /home/dev/Aria fetch origin  --prune
git -C /home/dev/Aria fetch github  --prune

# 5. Diagnose divergence before pushing (non-fast-forward would fail anyway)
git -C /home/dev/Aria log --oneline origin/master..HEAD | head
git -C /home/dev/Aria log --oneline github/master..HEAD | head
git -C /home/dev/Aria log --oneline HEAD..origin/master | head   # expect empty
git -C /home/dev/Aria log --oneline HEAD..github/master | head   # expect empty
```

If step 5 shows commits in `HEAD..<remote>/master`, stop — remote is ahead, a plain push will be rejected or (worse) require force. Resolve first.

---

## Push step

Push each remote separately so one remote's failure cannot be masked by the other's success. Check each exit code.

```bash
git -C /home/dev/Aria push origin master
RC_ORIGIN=$?
echo "push origin rc=$RC_ORIGIN"

git -C /home/dev/Aria push github master
RC_GITHUB=$?
echo "push github rc=$RC_GITHUB"
```

Abort verification if either `RC_*` is non-zero — fix the underlying cause (rejection, auth, network) first.

Note: do **not** use `git push --all` or `git push <remote> --mirror` here; they can silently push or delete other refs. Do **not** pass `--no-verify` unless explicitly instructed.

---

## Post-push verification (the load-bearing step)

The verification must query each remote **authoritatively**, not rely on the local remote-tracking ref that was just updated by the push itself.

### Method 1 — `git ls-remote` (preferred, no fetch side-effects)

`ls-remote` talks to the remote directly and returns its current ref list. It does not update any local ref, so it cannot be fooled by a stale cache.

```bash
LOCAL_SHA=$(git -C /home/dev/Aria rev-parse HEAD)

ORIGIN_SHA=$(git -C /home/dev/Aria ls-remote origin refs/heads/master | awk '{print $1}')
GITHUB_SHA=$(git -C /home/dev/Aria ls-remote github refs/heads/master | awk '{print $1}')

echo "LOCAL  = $LOCAL_SHA"
echo "ORIGIN = $ORIGIN_SHA"
echo "GITHUB = $GITHUB_SHA"

[ -n "$LOCAL_SHA" ]                  || { echo "FAIL: local SHA empty"; exit 1; }
[ "$ORIGIN_SHA" = "$LOCAL_SHA" ]     || { echo "FAIL: origin HEAD != local"; exit 1; }
[ "$GITHUB_SHA" = "$LOCAL_SHA" ]     || { echo "FAIL: github HEAD != local"; exit 1; }
echo "OK: both remotes match local HEAD $LOCAL_SHA"
```

Required assertions:

1. `ORIGIN_SHA` is a non-empty 40-char hex string (ref exists on remote).
2. `GITHUB_SHA` is a non-empty 40-char hex string.
3. `ORIGIN_SHA == LOCAL_SHA` (exact string equality).
4. `GITHUB_SHA == LOCAL_SHA`.

All four must pass; otherwise the multi-remote push is **not** verified regardless of what `git push` printed.

### Method 2 — API cross-check (belt-and-suspenders, recommended for Forgejo)

Because Forgejo sits behind Cloudflare Access, also query the REST API via the `forgejo` CLI wrapper. This confirms the HTTP/API view agrees with the git protocol view.

```bash
# Forgejo: GET branch -> .commit.id
ORIGIN_API_SHA=$(forgejo GET /repos/10CG/Aria/branches/master | jq -r '.commit.id')
[ "$ORIGIN_API_SHA" = "$LOCAL_SHA" ] || { echo "FAIL: forgejo API HEAD != local"; exit 1; }

# GitHub: GET ref -> .object.sha
GITHUB_API_SHA=$(gh api repos/10CG/Aria/git/refs/heads/master --jq '.object.sha')
[ "$GITHUB_API_SHA" = "$LOCAL_SHA" ] || { echo "FAIL: github API HEAD != local"; exit 1; }
```

If Method 1 and Method 2 disagree for the same remote, suspect proxy caching or a broken replication hook — investigate before declaring success.

### Method 3 — fetch + rev-parse (fallback)

If `ls-remote` is unavailable, do a fresh fetch and read the remote-tracking ref. This is weaker than Method 1 because it depends on local ref updates, but it is strictly better than reading `origin/master` without fetching.

```bash
git -C /home/dev/Aria fetch origin --prune
git -C /home/dev/Aria fetch github --prune
ORIGIN_SHA=$(git -C /home/dev/Aria rev-parse refs/remotes/origin/master)
GITHUB_SHA=$(git -C /home/dev/Aria rev-parse refs/remotes/github/master)
# then compare to LOCAL_SHA as in Method 1
```

---

## Decision matrix

| LOCAL vs ORIGIN | LOCAL vs GITHUB | Action |
|-----------------|-----------------|--------|
| equal           | equal           | SUCCESS — record SHAs in commit/release notes |
| equal           | differ          | GitHub push silently failed or was reverted. Re-push `github`; if still mismatched, check auth, branch protection, replication hooks |
| differ          | equal           | Same as above for `origin` |
| differ          | differ          | Push never succeeded despite output. Inspect `git push` exit codes, network, credentials |
| LOCAL empty/invalid | —           | Abort — we were not on a valid commit |
| remote SHA empty | —              | Branch does not exist on remote — did push create it? Check `git push -u` was used on first push |

---

## Common pitfalls this flow defends against

1. **Stale remote-tracking refs** — solved by `ls-remote` / fresh `fetch`.
2. **"Everything up-to-date" lying** — solved by comparing actual SHAs, not text.
3. **One remote succeeding, the other silently failing** — solved by pushing each remote separately, checking exit codes, and verifying each remote independently.
4. **Proxy / CDN caching (Cloudflare Access in front of Forgejo)** — solved by API cross-check (Method 2).
5. **Force-push race** (someone else force-pushed between our push and verify) — detected because their SHA will not equal our `LOCAL_SHA`.
6. **Wrong branch pushed** — `ls-remote origin refs/heads/master` pins the ref explicitly.

---

## Minimal end-to-end script (reference)

```bash
set -euo pipefail
REPO=/home/dev/Aria
BRANCH=master

git -C "$REPO" rev-parse --abbrev-ref HEAD | grep -qx "$BRANCH"
[ -z "$(git -C "$REPO" status --porcelain)" ]

LOCAL_SHA=$(git -C "$REPO" rev-parse HEAD)

git -C "$REPO" fetch origin --prune
git -C "$REPO" fetch github --prune

git -C "$REPO" push origin "$BRANCH"
git -C "$REPO" push github "$BRANCH"

ORIGIN_SHA=$(git -C "$REPO" ls-remote origin "refs/heads/$BRANCH" | awk '{print $1}')
GITHUB_SHA=$(git -C "$REPO" ls-remote github "refs/heads/$BRANCH" | awk '{print $1}')

[ "$ORIGIN_SHA" = "$LOCAL_SHA" ] || { echo "origin mismatch: $ORIGIN_SHA vs $LOCAL_SHA"; exit 1; }
[ "$GITHUB_SHA" = "$LOCAL_SHA" ] || { echo "github mismatch: $GITHUB_SHA vs $LOCAL_SHA"; exit 1; }

echo "VERIFIED: origin=github=local=$LOCAL_SHA"
```

Exit 0 from this script is the only acceptable "push succeeded" signal.
