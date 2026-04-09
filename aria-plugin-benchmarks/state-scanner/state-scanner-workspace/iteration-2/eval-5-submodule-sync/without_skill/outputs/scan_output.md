# 项目状态扫描 — 子模块远程同步检查

扫描时间: 2026-04-09
主项目: `/home/dev/Aria`
主项目分支: `feature/state-scanner-v2.9` (= `origin/feature/state-scanner-v2.9` @ `1445da5`)

## 结论速览

**不需要运行 `git submodule update`。**

三个子模块当前 checkout 的 commit 都与主项目 `.gitmodules` 指向的 gitlink SHA 完全一致，没有发生 "superproject 指针 → submodule working tree" 的漂移。

不过扫描发现了几件值得注意的事，见下文"注意事项"。

## 子模块逐一检查

主项目记录的 gitlink SHA (`git ls-tree HEAD`):

```
160000 commit 5023bedcf89dd3dd1eefb758aaf8301f59447a87  aria
160000 commit c31a85c005b9288a1fac4f3d3ba4c2e55ae7d25a  aria-orchestrator
160000 commit 5311ecbc23535126d9f41eb56d83312eb9189c08  standards
```

### 1. `standards` — 完全同步 ✅

| 项目 | 值 |
|---|---|
| Gitlink (superproject 记录) | `5311ecb` |
| 本地 HEAD | `5311ecb` |
| `origin/master` | `5311ecb` |
| 当前分支 | `master` |
| 工作区 | clean |
| 与 origin/master 差距 | 0 ahead / 0 behind |

完全同步，无需任何操作。

### 2. `aria` — Gitlink 一致，但在 feature 分支上 ⚠️

| 项目 | 值 |
|---|---|
| Gitlink (superproject 记录) | `5023bed` |
| 本地 HEAD | `5023bed` ✅ 匹配 gitlink |
| `origin/master` (aria 仓库) | `80b268a` |
| 当前分支 | `feature/state-scanner-v2.9` |
| 上游分支 | **未配置 (no upstream)** |
| 工作区 | **有未提交的本地修改** |

与 `origin/master` 对比: 本地分支比 `origin/master` **领先 2 个 commit**，落后 0 个:

```
5023bed feat(us-006): state-scanner v2.8.0 — project-level custom health checks
e0240cf fix(version): sync VERSION file to v1.10.0 matching plugin.json
```

`git submodule update` 在这里**不会更新**任何东西 — 因为 gitlink 和本地 HEAD 已经一致；该命令只会把 submodule 重置到 gitlink 所指的 commit，而那正是当前 HEAD。

但 `aria` 子模块里**还有未提交的工作区修改**:

```
 M .claude-plugin/marketplace.json
 M .claude-plugin/plugin.json
 M CHANGELOG.md
 M README.md  README.zh.md  VERSION
 M skills/config-loader/DEFAULTS.json
 M skills/config-loader/SKILL.md
 M skills/state-scanner/RECOMMENDATION_RULES.md
 M skills/state-scanner/SKILL.md
 M skills/state-scanner/references/output-formats.md
?? skills/state-scanner/references/issue-scanning.md
?? skills/state-scanner/references/sync-detection.md
```

⚠️ **注意**: 如果你在没有提交/暂存这些修改的情况下运行 `git submodule update`，git 通常会拒绝 (or 带 `--force` 覆盖丢失工作)。不要盲目 `--force`。

### 3. `aria-orchestrator` — Gitlink 一致，但 local master 领先 remote ⚠️

| 项目 | 值 |
|---|---|
| Gitlink (superproject 记录) | `c31a85c` |
| 本地 HEAD | `c31a85c` ✅ 匹配 gitlink |
| `origin/master` | `694ee5d` |
| 当前分支 | `master` |
| 工作区 | clean |
| 与 origin/master 差距 | **2 ahead** / 0 behind |

本地 `master` 比 `origin/master` 领先 2 个 commit:

```
c31a85c fix(scan): security keyword gap + complexity_tier rename (P0)
54328c2 feat: heartbeat execution log + scan-level circuit breaker
```

同样地，`git submodule update` 不会改变什么 (gitlink 已经匹配 HEAD)。但这意味着**本地 `aria-orchestrator/master` 上有尚未推送到远程的 commit**。这与你问的情况相反——不是"落后远程"，而是"领先远程"。

你可能需要的是 `cd aria-orchestrator && git push` 把它们发布到远程。

## 回答你的原问题

> 其他协作者推送了 submodule 更新到远程，是否需要 `git submodule update`？

**根据本次扫描，不需要。** 依据:

1. `git submodule status` 没有任何子模块前缀 `+` (代表 working tree 与 gitlink 不一致的标志)。
2. 三个子模块的 `HEAD` 都精确等于主项目 `HEAD` 中的 gitlink SHA。
3. 唯一一处"落后远程"是 `aria` 子模块的 `origin/master` (但你当前在 feature 分支上，且 HEAD 已包含了所有 master 的 commit 再加 2 个新 commit)。没有任何一个 submodule 的当前分支真正落后其 upstream。

## 建议的下一步

| 操作 | 原因 | 命令 |
|---|---|---|
| (可选) 看看 aria feature 分支有没有远程镜像 | 当前没有配置 upstream，无法判断别人是否也在这分支上 push 了东西 | `cd aria && git branch -r \| grep feature/state-scanner` |
| (推荐) push `aria-orchestrator` 的本地提交 | local master 领先 remote 2 commits，避免工作丢失 | `cd aria-orchestrator && git push origin master` |
| (推荐) 处理 `aria` 子模块未提交修改 | 避免工作区污染影响后续 checkout/update | `cd aria && git status` 后决定 commit 还是 stash |
| **不建议** 运行 `git submodule update` | 当前没有漂移需要修复；盲目运行可能与未提交修改冲突 | — |

## 参考: 如果将来确实需要同步

当你看到 `git submodule status` 输出中某个子模块前缀带 `+`，或者 `git status` 在主项目显示 `modified: some-submodule (new commits)`，那才是真正需要 `git submodule update` 的信号。届时正确做法:

```bash
# 先 fetch 全部 submodule
git submodule foreach 'git fetch --all'

# 同步到主项目记录的 gitlink
git submodule update --init --recursive

# 或者如果你想让 submodule 跟随各自远程分支最新 (谨慎)
git submodule update --remote
```
