## Remote Parity Check

**Note**: 用户声称"只有 origin 一个 remote"，但 `git remote -v` 显示实际有 2 个 remote (origin + github)。以下输出以实际 git 状态为准。

### Raw Git Commands

```bash
$ git rev-parse --abbrev-ref HEAD
feature/v1.15.0-multi-remote-parity

$ git remote -v
github  git@github.com:10CG/Aria.git (fetch)
github  git@github.com:10CG/Aria.git (push)
origin  ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git (fetch)
origin  ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git (push)

$ git rev-parse HEAD
5b7a5f7e7fa030a1f7996ade2c7ce170190a7960

$ git rev-parse origin/master
5b7a5f7e7fa030a1f7996ade2c7ce170190a7960

$ git rev-parse github/master
5b7a5f7e7fa030a1f7996ade2c7ce170190a7960
```

### Parity Result (JSON)

```json
{
  "branch": "master",
  "local_head": "5b7a5f7e7fa030a1f7996ade2c7ce170190a7960",
  "current_branch": "feature/v1.15.0-multi-remote-parity",
  "remotes": [
    {
      "name": "origin",
      "url": "ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git",
      "ref": "origin/master",
      "sha": "5b7a5f7e7fa030a1f7996ade2c7ce170190a7960",
      "status": "EQUAL"
    },
    {
      "name": "github",
      "url": "git@github.com:10CG/Aria.git",
      "ref": "github/master",
      "sha": "5b7a5f7e7fa030a1f7996ade2c7ce170190a7960",
      "status": "EQUAL"
    }
  ],
  "parity": "EQUAL",
  "all_remotes_in_sync": true,
  "notes": [
    "User claimed only 'origin' remote exists, but 'git remote -v' shows 2 remotes: origin (Forgejo) + github (GitHub).",
    "All remote-tracking refs (origin/master, github/master) match local HEAD SHA.",
    "Remote-tracking refs reflect last fetch state; run 'git fetch --all' for freshest comparison."
  ]
}
```
