# Eval: hlp-1 Parity Check (Equal) — with_skill

## Task

> 我的项目只有 origin 一个 remote, 本地 master HEAD 和 origin master 已完全同步。请用 git-remote-helper 的 check_parity 指令检测 parity 状态并输出 JSON。

- **Working directory**: `/home/dev/Aria`
- **Target repo**: `/home/dev/Aria/aria` (submodule)
- **Branch**: `master`

## Skill Guidance Consulted

- `aria/skills/git-remote-helper/SKILL.md` — identified `check_parity` as the pure-read instruction block for parity detection
- `aria/skills/git-remote-helper/references/api.md` — confirmed script path `scripts/check_parity.sh`, parameters (`--repo`, `--branch`, `--verify-mode`, `--timeout`), and output schema
- `aria/skills/git-remote-helper/references/schema.md` — validated canonical JSON fields (`local_head`, `remotes[]`, `overall_parity`, `has_unreachable_remote`, `has_pending_push`) and `parity` enum semantics

## Pre-check Observations

The task statement mentions only `origin`, but the actual `aria` submodule has **two** remotes configured:

```
origin  ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git (fetch/push)
github  git@github.com:10CG/aria-plugin.git (fetch/push)
```

Local HEAD and both tracking refs (`refs/remotes/origin/master`, `refs/remotes/github/master`) all resolve to the same SHA:

```
19f28619f216ff16364591380255165e9e176c50
```

Therefore both remotes are in `equal` parity. The check_parity output below reflects the true multi-remote state (schema requires reporting every configured remote); the `equal` conclusion the user expected for `origin` holds, and `overall_parity: true`.

## Invocation

```bash
bash /home/dev/Aria/aria/skills/git-remote-helper/scripts/check_parity.sh \
  --repo=/home/dev/Aria/aria \
  --branch=master \
  --verify-mode=local_refs \
  --timeout=5
```

Rationale for `--verify-mode=local_refs`: task requires status detection only, no network authority check needed; local_refs mode is fast (no network) and sufficient when the user asserts sync.

## Canonical JSON Output

```json
{
  "repo_path": "/home/dev/Aria/aria",
  "branch": "master",
  "local_head": "19f28619f216ff16364591380255165e9e176c50",
  "detached_head": false,
  "shallow": false,
  "local_refs_stale": false,
  "remotes": [
    {
      "name": "github",
      "remote_head": "19f28619f216ff16364591380255165e9e176c50",
      "parity": "equal",
      "behind_count": 0,
      "ahead_count": 0,
      "reachable": true,
      "reason": null,
      "method": "local_refs"
    },
    {
      "name": "origin",
      "remote_head": "19f28619f216ff16364591380255165e9e176c50",
      "parity": "equal",
      "behind_count": 0,
      "ahead_count": 0,
      "reachable": true,
      "reason": null,
      "method": "local_refs"
    }
  ],
  "overall_parity": true,
  "has_unreachable_remote": false,
  "has_pending_push": false
}
```

## Interpretation

| Signal | Value | Meaning |
|--------|-------|---------|
| `local_head` | `19f28619…` | Current HEAD SHA |
| `detached_head` | `false` | On branch `master` normally |
| `shallow` | `false` | Full clone, commit counts are reliable |
| `local_refs_stale` | `false` | Tracking refs fresh (FETCH_HEAD mtime < 24h) |
| `remotes[].parity` | `equal` (both) | `ahead_count=0 AND behind_count=0` for each remote |
| `overall_parity` | `true` | No remote is `behind` or `diverged` |
| `has_unreachable_remote` | `false` | All remotes resolved via local tracking refs |
| `has_pending_push` | `false` | No remote is `ahead` (nothing to push) |

## Conclusion

Parity status: **EQUAL across all configured remotes**. Local `master` (`19f2861`) matches `origin/master` and `github/master` exactly. No push, fetch, or merge action required.
