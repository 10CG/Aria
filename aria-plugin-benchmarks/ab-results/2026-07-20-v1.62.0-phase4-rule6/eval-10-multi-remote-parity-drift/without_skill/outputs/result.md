# 多 remote 同步状态扫描 (baseline 臂, 无 skill)

**扫描时间**: 2026-07-20
**扫描范围**: 主仓 `/home/dev/Aria` + 三个子模块 (`aria` / `standards` / `aria-orchestrator`)
**约束**: 只跑只读命令, 未执行 `git fetch` / `git push` / 任何写操作

---

## 1. 我是怎么查的 (方法)

多 remote 同步状态没有单一命令能直接给答案, 我拆成四步机械查证:

**(1) 枚举 remote 和 push URL**

```bash
git remote -v
```

要看的是 fetch 和 push URL 是否成对、是否指向不同 host。仅看 remote 名字不够 —— 名字可以骗人 (`github` 可能实际指向 Forgejo)。

**(2) 拿本地分支和各 remote-tracking ref 的 SHA**

```bash
git for-each-ref --format='%(refname:short) %(objectname:short) %(committerdate:iso)' \
  refs/heads/master refs/remotes/origin/master refs/remotes/github/master
```

**(3) 算每个 remote 的 ahead/behind (核心判据)**

```bash
git rev-list --left-right --count master...origin/master
git rev-list --left-right --count master...github/master
```

输出是 `<左侧独有> <右侧独有>` 两个数:

- `0  0` = 完全同步
- `N  0` = 本地领先 N 个提交 → **该 remote 落后, 需要 push**
- `0  N` = 本地落后 N 个提交 → 需要 pull/rebase
- `N  M` = 分叉, 要人工处理

**(4) 子模块逐个重复上述三步**

```bash
git submodule status
git -C aria remote -v
git -C aria rev-list --left-right --count master...github/master
```

多 remote 漏推最常发生在子模块 —— 主仓 gitlink 推上去了, 但 gitlink 指向的 commit 在镜像 remote 上不存在, 于是从 GitHub clone 的人 `submodule update` 会直接失败。所以还额外查了 gitlink 可达性:

```bash
git -C aria branch -r --contains <gitlink-sha>
```

**(5) remote-tracking ref 的新鲜度 (关键 caveat)**

```bash
ls -l --time-style=long-iso .git/FETCH_HEAD .git/refs/remotes
```

`refs/remotes/*` 是**本地缓存**, 不是远程真相。上一次 `git fetch` 之后远程发生的任何变化, 本地一概不知。所以陈旧的 tracking ref 会让 `0 0` 变成一个**假的"已同步"**结论。本次按要求没跑 fetch, 因此下面所有判定都标注了证据新鲜度。

---

## 2. 扫描结果

### 2.1 主仓 `/home/dev/Aria`

| 项目 | 值 |
|------|-----|
| 当前分支 | `master` |
| 本地 HEAD | `80bb4de` (chore(release): aria v1.62.2 gitlink bump + 主仓 SOT 同步) |
| `origin` | `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git` |
| `github` | `git@github.com:10CG/Aria.git` |

| Remote | tracking SHA | ahead / behind | 判定 |
|--------|--------------|----------------|------|
| origin (Forgejo) | `80bb4de` | 0 / 0 | 已同步 |
| github (镜像) | `80bb4de` | 0 / 0 | 已同步 |

### 2.2 子模块 `aria` (aria-plugin)

| 项目 | 值 |
|------|-----|
| gitlink (主仓记录) | `aadd56e` |
| 本地分支 | `master` @ `aadd56e` |
| `origin` | `ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git` |
| `github` | `git@github.com:10CG/aria-plugin.git` |

| Remote | tracking SHA | ahead / behind | 判定 |
|--------|--------------|----------------|------|
| origin | `aadd56e` | 0 / 0 | 已同步 |
| github | `aadd56e` | 0 / 0 | 已同步 |

gitlink 可达性: `aadd56e` 同时被 `origin/master` 和 `github/master` 包含 → 从 GitHub clone 做 `submodule update --init` 不会断。

### 2.3 子模块 `standards`

| Remote | ahead / behind (相对当前 checkout) | 判定 |
|--------|-----------------------------------|------|
| origin | 0 / 1 | checkout 落后 1 个提交 |
| github | 0 / 1 | checkout 落后 1 个提交 |

两个 remote 之间**彼此一致** (都比本地 checkout 多同一个提交), 所以这**不是多 remote 漏推**问题, 而是本地子模块 checkout 停在旧 commit (detached, 处于 `fix/nomad-docker-registry-auth-v2` 派生点)。没有需要 push 的东西。

### 2.4 子模块 `aria-orchestrator`

| Remote | ahead / behind | 判定 |
|--------|----------------|------|
| origin | 0 / 0 | 已同步 |
| github | **没有配置该 remote** | 不适用 |

`aria-orchestrator` 只有 `origin` 一个 remote。按 CLAUDE.md, 它是 10CG Lab 内部运行时, 不对外发布, 所以**没有 GitHub 镜像是符合设计的**, 不是缺陷。

---

## 3. 结论 (要诚实说的一点)

**你描述的 "v1.15.0 只推了 Forgejo、漏推 GitHub" 这个 drift, 在当前仓库里我没有扫到。**

具体不吻合的地方有两处:

1. **版本对不上。** 当前 aria-plugin 是 **v1.62.2** (`aadd56e`), 主仓 HEAD 是 `80bb4de` "aria v1.62.2 gitlink bump"。v1.15.0 是很早以前的版本, 那次发版早已被后续几十个版本覆盖。
2. **parity 对不上。** 主仓和 `aria` 子模块的 `origin` 与 `github` 两个 remote 的 tracking ref 都指向**同一个 SHA**, ahead/behind 全是 `0 0`。也就是说按当前本地证据, 没有任何一个 remote 落后。

所以我不会给你一份"修 v1.15.0 漏推"的命令 —— 那会是在修一个不存在的问题。前提事实先核实, 再动手。

### 一个必须说清的证据边界

上面所有 `0 0` 都是基于**本地 remote-tracking ref**。这些 ref 的最后刷新时间:

- 主仓 `.git/FETCH_HEAD`: 2026-07-20 12:32
- `refs/remotes/github/`: 2026-07-20 12:01
- `refs/remotes/origin/`: 2026-07-20 11:59
- `aria` 子模块 `.git/modules/aria/FETCH_HEAD`: 2026-07-20 11:51 (空文件)

时间戳都是今天、几十分钟内, 所以证据算新鲜, 结论可信度较高。但严格讲, **不 fetch 就没有远程真相**。如果你要一个够硬的结论 (比如发版前的放行判定), 应该先刷新再判:

```bash
# 本次未执行 —— 你手动跑
git fetch --all --prune
git -C aria fetch --all --prune
git -C standards fetch --all --prune
```

刷新后重跑第 3 步的 `rev-list --left-right --count`, 若仍是 `0 0`, 那就是确凿的已同步。

---

## 4. 给你的建议

### 4.1 真出现漏推时的修复命令 (备用模板)

假设某次真的只推了 Forgejo, 按"子模块先、主仓后"的顺序补:

```bash
# 先补子模块 (gitlink 必须在镜像上可达, 否则主仓推上去也是断链)
git -C aria push github master
git -C standards push github master   # 仅当 standards 有变更

# 再补主仓
git push github master

# 若发了 tag 也要单独补, push 不会自动带 tag
git push github --tags
```

顺序不能反: 主仓 gitlink 先落地而子模块 commit 还没到 GitHub, 那段时间内从 GitHub clone 的人会拿到一个指向不存在 commit 的 gitlink。

### 4.2 事后核验 (别只看 push 命令退出码)

```bash
git rev-parse master
git ls-remote github master        # 两者 SHA 必须逐字符相同
git -C aria rev-parse master
git -C aria ls-remote github master
```

`ls-remote` 直接问远端, 不经过本地缓存 —— 这是唯一不会被陈旧 tracking ref 骗到的核验方式。

### 4.3 从根上防复发

漏推 GitHub 这类事故的成因是"多仓 + 多 remote 的手工步骤太多"。三个方向, 从轻到重:

- **push 时永远带上全部 enforced remote**, 写成一条组合命令而不是分两次敲, 少一次"敲完第一条就被打断"的机会。
- **在发版检查清单里加一条机械核验**: 用上面 4.2 的 `ls-remote` 对比, 而不是靠"我记得推过了"。
- **配 Forgejo 侧的自动 mirror push**, 让 GitHub 镜像由服务端保证, 彻底移除人工步骤 —— 这是最彻底的解, 代价是要在 Forgejo 仓库设置里配 push mirror 凭据。

### 4.4 顺带发现的两个小事项 (与本次问题无关)

- `standards` 子模块 checkout 落后两个 remote 各 1 个提交, 且处于 detached 状态。如果不是刻意 pin, 建议 `git submodule update --remote standards` 后确认是否需要 bump 主仓 gitlink。
- `aria` 子模块本地有 14 个 feature 分支, 其中若干 (如 `feat/v1.47.0-issue-sweep`、`feature/agent-router-baseline-semantics-99`) 已无对应上游或早已合并。不影响同步判定, 但可以清理以减少扫描噪音。
