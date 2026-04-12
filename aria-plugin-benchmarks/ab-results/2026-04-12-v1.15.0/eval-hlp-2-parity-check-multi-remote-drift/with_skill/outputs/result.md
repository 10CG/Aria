# eval-hlp-2: git-remote-helper Multi-Remote Parity Drift Detection (with_skill)

**Task**: 双 remote (origin + github) 场景下，github 落后 origin 2 个 commits。使用 `git-remote-helper` skill 的 `check_parity` 脚本检测并输出每个 remote 的独立状态。不得因 "Everything up-to-date" 文本错误合并为单一状态——必须 per-remote 独立报告。

**Skill Referenced**:
- `/home/dev/Aria/aria/skills/git-remote-helper/SKILL.md`
- `/home/dev/Aria/aria/skills/git-remote-helper/references/api.md`
- `/home/dev/Aria/aria/skills/git-remote-helper/references/schema.md`
- `/home/dev/Aria/aria/skills/git-remote-helper/scripts/check_parity.sh`

**Target Repo**: `/home/dev/Aria/aria` (submodule with `origin` + `github` remotes)

**Date**: 2026-04-12

---

## 1. Remote Topology (Pre-Check)

`aria` submodule 配置了两个独立 remote:

| Remote | URL | 角色 |
|--------|-----|------|
| `origin` | `ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git` | 主开发仓库 (Forgejo) |
| `github` | `git@github.com:10CG/aria-plugin.git` | Claude Code 插件市场镜像 |

**Branch**: `master` (本地 worktree 当前在 `feature/v1.15.0-multi-remote-parity`, 但本次检测针对 `master`)

**Local HEAD (master)**: `19f28619f216ff16364591380255165e9e176c50`

---

## 2. Drift Scenario Construction

为验证 skill 的 per-remote 独立报告能力，通过 `git update-ref` 将本地的 `refs/remotes/github/master` 回退到 `f55e130`（即 `19f2861` 之前 2 个 commits），模拟 "github 落后 origin 2 个 commits" 的场景：

```
本地 master             : 19f2861  (HEAD)
refs/remotes/origin/master : 19f2861  (与 local 相等)
refs/remotes/github/master : f55e130  (落后 local 2 个 commits)

2 commits of drift:
  19f2861 Merge PR 'release: v1.14.0 — 版本号同步 + Skill 数量修正' (#12)
  06a0edf release: v1.14.0 — Phase 1.8 README 检查增强 + Phase 1.14 Forgejo 配置检测
  f55e130 Merge PR 'feat(v1.14.0): state-scanner Phase 1.8 README 检查增强' (#11)  ← github 停在这
```

此场景真实反映 CLAUDE.md 记录的 2026-04-10 事故: aria v1.11.1 发版后仅推送 Forgejo (origin), 未推送 GitHub, 导致插件市场版本滞后。

---

## 3. check_parity.sh Invocation (local_refs 模式)

### Command

```bash
bash /home/dev/Aria/aria/skills/git-remote-helper/scripts/check_parity.sh \
  --repo=/home/dev/Aria/aria \
  --branch=master \
  --verify-mode=local_refs
```

### Full JSON Output

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
      "remote_head": "f55e13022937de4289ede769852c4d6634b015e3",
      "parity": "ahead",
      "behind_count": 0,
      "ahead_count": 2,
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
  "has_pending_push": true
}
```

---

## 4. Per-Remote Independent Status Table

**关键断言: 每个 remote 有独立的 `parity` / `ahead_count` / `behind_count` / `remote_head` 字段，彼此不聚合。**

| 字段 | `github` | `origin` |
|------|----------|----------|
| `name` | `github` | `origin` |
| `remote_head` | `f55e13022937de4289ede769852c4d6634b015e3` | `19f28619f216ff16364591380255165e9e176c50` |
| `parity` | **`ahead`** (local 领先 github) | **`equal`** |
| `ahead_count` | **`2`** (local 比 github 多 2 个 commit) | `0` |
| `behind_count` | `0` | `0` |
| `reachable` | `true` | `true` |
| `reason` | `null` | `null` |
| `method` | `local_refs` | `local_refs` |

### 语义解读

- `github.parity = "ahead"` + `ahead_count = 2` → 本地 HEAD 领先 github remote 2 个 commits，等价于 **github 落后本地（及 origin）2 个 commits** — 精确命中任务描述的场景。
- `origin.parity = "equal"` → origin remote 与本地 HEAD 完全一致，无漂移。
- 两个 remote 的状态**完全独立存储在 `remotes[]` 数组的独立对象中**，没有被合并为单一 "repo-level" parity 标签。

### 聚合字段 (Meta-Level, 但不替代 per-remote 报告)

| 字段 | 值 | 含义 |
|------|-----|------|
| `overall_parity` | `true` | 因为无 remote 处于 `behind` 或 `diverged` 状态 (`ahead` 不算 parity 失败, 只是 pending push) |
| `has_unreachable_remote` | `false` | 两个 remote 都可达 |
| `has_pending_push` | **`true`** | 至少一个 remote (`github`) 处于 `ahead` 状态，需要推送 |

**重要**: `has_pending_push=true` 是 per-remote 漂移的精确聚合信号；`overall_parity=true` 并不掩盖 github 落后的事实 — consumer (如 state-scanner Phase 1.12) 必须检查 `has_pending_push` 和遍历 `remotes[]` 来发现漂移，不能只看 `overall_parity`。

---

## 5. 验证 "Everything up-to-date" 陷阱 Has Not Occurred

Skill 的 `check_parity.sh` (纯读路径) 完全**不调用 `git push`**，因此不存在 "Everything up-to-date" 文本问题。其 parity 判定基于:

```
ahead_count  = git rev-list --count <remote>/<branch>..HEAD
behind_count = git rev-list --count HEAD..<remote>/<branch>
parity       = f(ahead_count, behind_count)  # 见 schema.md parity 枚举
```

这是确定性 SHA-level 比较，无文本歧义。

`push_all_remotes.sh` 指令块 (写路径) 在 api.md 中明文规定:

> **`success` 判定规则 (严格)**:
> `success = (exit_code == 0) AND (post_remote_head == pre_local_head)`
> 不依赖 "Everything up-to-date" 文本

即使 `git push` 输出 "Everything up-to-date"，success 判定仍基于 `post_remote_head == pre_local_head` 的 SHA 比较，不会因文本误判。

---

## 6. Skill Contract Compliance Checklist

| Schema 要求 (references/schema.md) | 实际输出 | Pass? |
|-----------------------------------|---------|-------|
| 顶层 `repo_path` (string) | `"/home/dev/Aria/aria"` | ✅ |
| 顶层 `branch` (string) | `"master"` | ✅ |
| 顶层 `local_head` (full SHA) | 40-char SHA | ✅ |
| 顶层 `detached_head` (bool) | `false` | ✅ |
| 顶层 `shallow` (bool) | `false` | ✅ |
| `remotes` (array) | 2 objects (github, origin) | ✅ |
| 每个 remote 有独立 `name` | `github`, `origin` | ✅ |
| 每个 remote 有独立 `remote_head` | 两个不同 SHA | ✅ |
| 每个 remote 有独立 `parity` 枚举 | `ahead` vs `equal` | ✅ |
| 每个 remote 有独立 `behind_count` | `0` vs `0` | ✅ |
| 每个 remote 有独立 `ahead_count` | `2` vs `0` | ✅ |
| 每个 remote 有独立 `reachable` | `true` vs `true` | ✅ |
| 每个 remote 有 `method` 字段 | `local_refs` | ✅ |
| `overall_parity` 按 schema 定义 (non-behind/diverged) | `true` (因 ahead 不算失败) | ✅ |
| `has_pending_push` 反映 ahead 状态 | `true` | ✅ |

**结论**: 输出完全符合 canonical schema；per-remote 独立性得到保证。

---

## 7. Cleanup

检测完成后立即恢复 `refs/remotes/github/master` 至真实值 `19f28619f216ff16364591380255165e9e176c50`，未对 remote 产生任何副作用 (`check_parity` 为纯读指令块)。

```
$ cd /home/dev/Aria/aria
$ git update-ref refs/remotes/github/master 19f28619f216ff16364591380255165e9e176c50
$ git rev-parse refs/remotes/github/master
19f28619f216ff16364591380255165e9e176c50
```

---

## 8. Final Answer (Per-Remote Independent Report)

在模拟 "github 落后 origin 2 个 commits" 的场景下，`git-remote-helper` 的 `check_parity.sh` 正确地：

1. **为每个 remote 独立输出完整 parity 状态** — `github` 和 `origin` 各自拥有独立的 `parity`/`ahead_count`/`behind_count`/`remote_head` 字段，不合并为单一 "repo parity"。
2. **精确定位漂移**: `github.ahead_count=2`（即 github 落后本地 2 个 commits），`origin.parity=equal`。
3. **`has_pending_push=true` 作为聚合告警**: 任何 remote 处于 `ahead` 状态时置位，consumer 必须遍历 `remotes[]` 识别具体落后的 remote。
4. **不依赖 "Everything up-to-date" 文本**: 所有判定基于确定性 SHA 比较 (`rev-list --count`)，不受 git push 输出文本歧义影响。
5. **`overall_parity` 不掩盖 per-remote 漂移**: 其定义仅在 `behind`/`diverged` 时置 false; `ahead` 产生的待推送状态由 `has_pending_push` 独立反映。Consumer 必须同时检查 `has_pending_push` 和每个 `remotes[].parity`。

此行为与 CLAUDE.md feedback「多仓库 git 操作必须用 git -C <path>, "Everything up-to-date" 必须验证」的要求一致，解决了 2026-04-10 aria v1.11.1 事故的根因。
