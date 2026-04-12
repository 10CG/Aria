# Multi-Remote Parity Check Report

**Date**: 2026-04-12
**Repository**: /home/dev/Aria
**Current branch**: feature/v1.15.0-multi-remote-parity
**Local HEAD**: `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960`

---

## Per-Remote Independent Status

> Methodology: Each remote is queried **independently** via `git ls-remote` + `git rev-list --count` to avoid conflating state. We do NOT trust a single aggregate "Everything up-to-date" message.

### Remote 1: `origin` (Forgejo - primary dev)

| Field | Value |
|-------|-------|
| URL (fetch) | `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git` |
| URL (push)  | `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git` |
| Remote `refs/heads/master` SHA | `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960` |
| Local `origin/master` SHA      | `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960` |
| Commits local HEAD is ahead of `origin/master`  | `0` |
| Commits local HEAD is behind `origin/master`    | `0` |
| Fetch status | OK (exit 0) |
| Verdict | **IN SYNC with local HEAD** |

Top commit on `origin/master`:
```
5b7a5f7 chore: v1.14.0 版本号同步 + aria submodule pointer → 19f2861
```

### Remote 2: `github` (GitHub - plugin marketplace mirror)

| Field | Value |
|-------|-------|
| URL (fetch) | `git@github.com:10CG/Aria.git` |
| URL (push)  | `git@github.com:10CG/Aria.git` |
| Remote `refs/heads/master` SHA | `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960` |
| Local `github/master` SHA      | `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960` |
| Commits local HEAD is ahead of `github/master`  | `0` |
| Commits local HEAD is behind `github/master`    | `0` |
| Fetch status | OK (exit 0) |
| Verdict | **IN SYNC with local HEAD** |

Top commit on `github/master`:
```
5b7a5f7 chore: v1.14.0 版本号同步 + aria submodule pointer → 19f2861
```

---

## Cross-Remote Drift Analysis

Independent comparison between the two remote refs (NOT aggregated):

| Comparison | Command | Result |
|-----------|---------|--------|
| `origin/master` ahead of `github/master` | `git rev-list --count origin/master ^github/master` | **0** commits |
| `github/master` ahead of `origin/master` | `git rev-list --count github/master ^origin/master` | **0** commits |
| Direct SHA equality (ls-remote both)     | `5b7a5f7…` == `5b7a5f7…` | **EQUAL** |

**Drift verdict**: No drift detected between `origin/master` and `github/master` at fetch time 2026-04-12.

---

## Important Caveat Regarding the Task Premise

The task description stated: *"github 落后 origin 2 个 commits"*.

**That condition is NOT observed in the current repository state.** Evidence:

1. `git ls-remote origin refs/heads/master`  → `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960`
2. `git ls-remote github refs/heads/master`  → `5b7a5f7e7fa030a1f7996ade2c7ce170190a7960`
3. `git rev-list --count origin/master ^github/master` → `0`
4. `git rev-list --count github/master ^origin/master` → `0`

Both remotes are currently at identical SHAs on `master`. If a 2-commit drift was expected as a test fixture, the fixture was not applied to this working tree, OR the drift was already reconciled by a prior push. Per the task's own directive — do NOT collapse state into a single "up-to-date" claim — each remote is reported independently above; the conclusion for each happens to coincide.

If the user needs a demonstration of drift handling, the following commands would isolate it even when present:

```
# Per-remote absolute SHA (source of truth — does NOT depend on local tracking refs)
git ls-remote origin refs/heads/master
git ls-remote github refs/heads/master

# Asymmetric ahead/behind (always report both directions separately)
git rev-list --left-right --count origin/master...github/master
# → "<N>  <M>"  where N = origin-only commits, M = github-only commits

# List the drifting commits by SHA + subject (per direction)
git log --oneline origin/master ^github/master   # on origin but not github
git log --oneline github/master ^origin/master   # on github but not origin
```

---

## Local Working Tree Status (context, not parity)

Current branch `feature/v1.15.0-multi-remote-parity` has uncommitted local changes and untracked files (OpenSpec change dirs, US-012, AB result scaffolding). These do NOT affect remote parity since they are unpublished, but they are noted for completeness:

- Modified: `CLAUDE.md`, `aria` (submodule), `aria-plugin-benchmarks/ab-suite/phase-c-integrator.json`, `aria-plugin-benchmarks/ab-suite/state-scanner.json`, `docs/architecture/system-architecture.md`
- Untracked: `.aria/audit-reports/…`, `aria-plugin-benchmarks/ab-results/2026-04-12-v1.15.0/`, `aria-plugin-benchmarks/ab-suite/git-remote-helper.json`, `docs/requirements/user-stories/US-012.md`, `openspec/changes/phase-c-integrator-push-enforcement/`, `openspec/changes/state-scanner-multi-remote-parity/`

Neither `origin` nor `github` reports these — they exist only in the local working tree.

---

## Summary Table (single glance)

| Remote | Remote SHA | Local tracking SHA | Δ vs local HEAD | Δ vs other remote | Verdict |
|--------|-----------|---------------------|-----------------|------------------|---------|
| origin | `5b7a5f7` | `5b7a5f7` | 0 ahead / 0 behind | 0 vs github | IN SYNC |
| github | `5b7a5f7` | `5b7a5f7` | 0 ahead / 0 behind | 0 vs origin | IN SYNC |

**Bottom line**: Both remotes are independently verified to be at commit `5b7a5f7` on `master`. No push required. If a future drift appears, repeat the per-remote `ls-remote` + `rev-list --count` procedure above — never rely on `git push`'s "Everything up-to-date" because that phrase is emitted per-remote and can mask the fact that *other* remotes were never contacted.
