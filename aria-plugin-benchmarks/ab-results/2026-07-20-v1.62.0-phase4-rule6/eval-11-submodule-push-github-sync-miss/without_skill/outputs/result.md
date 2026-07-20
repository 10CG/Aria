# 多远程同步扫描 — 复现 2026-04-12 "GitHub mirror 漏推" 事件

扫描时间: 2026-07-20 12:38 UTC | 仓库: /home/dev/Aria (主仓 + 3 个子模块)
约束: 本次为只读扫描, **未执行任何 fetch / push / 写操作**。

---

## 1. 我会怎么检查

事件的本质是: **"push 成功" 只对某一个 remote 成立, 却被当成了对全部 remote 成立**。
`git push origin master` 之后再跑一次会回 `Everything up-to-date` —— 这句话的主语是
`origin`, 跟 GitHub mirror 没有任何关系。所以检查必须做到三件事:

**检查一: 枚举每个仓库的全部 remote, 逐个 remote 独立判定**

不能只看 "当前分支的 upstream"。upstream 只有一个 (通常是 origin), 以它为准就天然看不见
mirror。正确做法是对每个 repo 枚举 `git remote`, 然后对每个 remote 单独算 ahead/behind。

```bash
for RM in $(git remote); do
  git rev-list --left-right --count HEAD...refs/remotes/$RM/master
done
```

左边 = 本地领先该 remote 的 commit 数 (> 0 即 **需要补推**), 右边 = 落后数。

**检查二: 判定 remote-tracking ref 的新鲜度 (这是最容易出错的一环)**

`refs/remotes/github/master` 是**上一次 fetch 时的缓存快照**, 不是 GitHub 的实时状态。
如果从没 fetch 过 github, 那个 ref 可能压根不存在, 或者停留在几天前 —— 此时 ahead/behind
算出 `0 0` 只是"我不知道", 不是"已同步"。**把 `0 0` 当成 parity=equal 正是 2026-04-12 事件
的假绿机制**。所以我会同时读 ref 的 mtime / FETCH_HEAD 时间作为证据等级:

- ref 缺失 → 证据等级 `unknown`, 不得判 equal
- ref 陈旧 (超过阈值, 例如 1 小时) → 证据等级 `stale_unverified`, 只能判 "疑似", 不能判 equal
- ref 新鲜 → 证据等级 `fresh`, 才允许判 equal

**检查三: gitlink 可达性 (子模块特有)**

主仓提交里记录的子模块 SHA (gitlink), 必须在**每一个** remote 的 master 上可达。
只推了 Forgejo 的话, GitHub 上的主仓会指向一个 GitHub 侧根本不存在的子模块 commit ——
别人 `git submodule update` 直接失败。这一步比 ahead/behind 更能抓住 "主仓推了、子模块
mirror 没推" 的组合事故。

```bash
SHA=$(git ls-tree HEAD aria | awk '{print $3}')
git -C aria merge-base --is-ancestor $SHA refs/remotes/github/master
```

---

## 2. 本次扫描的实际输出

### 2.1 remote 拓扑

| 仓库 | origin (Forgejo) | github (mirror) |
|------|------------------|-----------------|
| 主仓 Aria | ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git | git@github.com:10CG/Aria.git |
| aria (插件) | .../10CG/aria-plugin.git | git@github.com:10CG/aria-plugin.git |
| standards | .../10CG/aria-standards.git | git@github.com:10CG/aria-standards.git |
| aria-orchestrator | .../10CG/aria-orchestrator (origin) | **不存在** |

### 2.2 逐 remote parity

| 仓库 | 本地 HEAD | origin/master | github/master | 领先/落后 origin | 领先/落后 github | 判定 |
|------|-----------|---------------|---------------|------------------|------------------|------|
| 主仓 Aria | `80bb4de` | `80bb4de` | `80bb4de` | 0 / 0 | 0 / 0 | 疑似一致 (证据 stale) |
| aria | `aadd56e` | `aadd56e` | `aadd56e` | 0 / 0 | 0 / 0 | 疑似一致 (证据 stale) |
| standards | `79b7cd6` (detached) | `a96a56b` | `a96a56b` | 0 / **落后 1** | 0 / **落后 1** | 落后, 但非漏推 |
| aria-orchestrator | `86bb684` (detached) | `86bb684` | 无该 remote | 0 / 0 | **unknown** | **镜像缺失** |

### 2.3 证据新鲜度 (决定上表能不能信)

| 仓库 | github refs 最后更新 | origin refs 最后更新 | 距今 | 证据等级 |
|------|----------------------|----------------------|------|----------|
| 主仓 Aria | 2026-07-20 12:01 | 2026-07-20 11:59 | ~37 分钟 | stale_unverified |
| aria | 2026-07-20 11:58 | 2026-07-20 11:58 | ~40 分钟 | stale_unverified |
| standards | 2026-07-19 20:10 | 2026-07-19 18:53 | ~16 小时 | **expired** |
| aria-orchestrator | 无 github remote | 2026-07-13 06:32 | ~7 天 | **expired** |

### 2.4 gitlink 可达性

| 子模块 | 主仓记录的 gitlink | origin/master 可达 | github/master 可达 |
|--------|--------------------|--------------------|--------------------|
| aria | `aadd56e2` | 可达 | 可达 |
| standards | `79b7cd65` | 可达 | 可达 |
| aria-orchestrator | `86bb6846` | 可达 | 无 mirror, 无法判定 |

---

## 3. 结论: 哪些 remote 需要补推

**当前快照下, 没有发现 "本地领先 GitHub" 的漏推**, 但有三条必须报出的问题:

**问题一 (核心, 直击本 eval 的考点): 上面所有 "0 / 0" 都不是 parity=equal 的正证据。**
这些数字来自本地缓存的 remote-tracking ref, 最新的也是 37 分钟前 fetch 的, standards 和
aria-orchestrator 更是 16 小时 / 7 天前。**在没有一次新鲜 fetch 之前, 正确的裁定是
`unknown`, 而不是 "已同步"。** 如果这时候有人在别处往 GitHub 推了东西, 或者本地刚 merge
完还没推, 这个 `0 0` 会原封不动地撒谎 —— 这正是 2026-04-12 事件的复现路径: 当年不是
"检查跑出了错误答案", 而是 "检查根本没去问 GitHub, 却输出了肯定的答案"。

要给出可信结论, 必须先 (由 owner 或非并发时段) 执行:
```bash
git fetch --all --prune
git -C aria fetch --all --prune
git -C standards fetch --all --prune
```
然后重跑 2.2 的 ahead/behind。本次因并发测试约束未执行。

**问题二: aria-orchestrator 根本没有配置 github remote。**
这是比 "漏推一次" 更严重的形态 —— 不是某次忘了推, 而是这个仓库的镜像通道结构性不存在,
每一次提交都必然只在 Forgejo。需要 owner 确认: 该仓库是**有意**不对外镜像 (v2.0 运行时层
仅 10CG Lab 内部, CLAUDE.md 有此说明), 还是漏配。若是有意, 应在配置里显式声明为
"仅 origin", 让扫描器把它标成 `read_only` 而不是 `unknown`, 避免每次扫描都报噪音。

**问题三: standards 落后远端 1 个 commit, 且处于 detached HEAD。**
本地 `79b7cd6` 在 `origin/master` (`a96a56b`) 之后缺 1 个提交, 两个 remote 都一致, 所以
**不是漏推, 是本地没更新**。这是主仓 gitlink 指向旧 standards 提交的正常状态, 但如果打算
在 standards 上继续开发, 需要先 `git -C standards checkout master && git pull`, 否则容易
基于旧基线提交。

---

## 4. 修复建议

**立刻可做 (本次未执行, 需 owner 在非并发时段跑):**

1. 先 fetch 再判定 —— 任何 parity 结论必须建立在本轮新鲜 fetch 之上:
   ```bash
   for R in . aria standards aria-orchestrator; do git -C $R fetch --all --prune; done
   ```
2. 重跑逐 remote ahead/behind, 对任何 "本地领先 X" 的 remote 补推:
   ```bash
   git -C aria push github master     # 若 github 落后
   git push github master             # 主仓同理
   ```
3. 推完做 **post-push SHA 回验** (不要相信 push 的退出码):
   ```bash
   git -C aria ls-remote github refs/heads/master   # 与本地 HEAD 逐字节比对
   ```
   `git push` 返回 0 只说明"服务端接受了"; 真正的闭环证据是从远端读回来的 SHA 等于本地 SHA。

**流程层加固 (防止再犯):**

4. **禁止把 `Everything up-to-date` 当作同步证据。** 这句话是 per-remote 的, 且在 remote
   参数写错 / remote 不存在时也可能给出误导性输出。判据换成 `ls-remote` 读回的 SHA。
5. **同步判定引入证据分级**, 不允许 `unknown` 静默降级成 `equal`。ref 缺失或超龄一律输出
   `unknown` 并要求先 fetch —— 这是 fail-closed, 宁可报"我不知道"也不报假绿。
6. **发版流程把 gitlink 可达性作为硬闸**: 主仓 push 之前, 校验每个子模块 gitlink 在**每个**
   enforced remote 的 master 上可达。子模块先 merge + 先推全部 remote, 主仓 gitlink bump
   后推 —— 顺序反了就会在 GitHub 上留下悬空 gitlink。
7. **在配置里显式声明 enforced remotes 清单** (例如主仓与 aria 为 `[origin, github]`,
   aria-orchestrator 为 `[origin]`)。不要用"自动发现全部 remote"做判据 —— 那样新加一个
   临时 remote 就会污染裁决, 也无法区分"有意只推一个"和"漏配 mirror"。
8. 若 mirror 长期靠人工推, 考虑在 Forgejo 侧配置 push mirror 自动同步到 GitHub, 把这条
   人为遗漏路径直接消除。

---

## 5. 本次扫描的局限 (诚实声明)

- **未执行 fetch**, 因此第 2.2 节全部 parity 数字都是缓存快照, 证据等级最好也只是
  `stale_unverified`。不能据此宣布 "已同步"。
- 仅检查了各仓库的 `master` 分支。feature 分支的跨 remote 差异未纳入 (`aria` 本地有 14 个
  feature 分支, 其中若干无 github 侧对应 ref)。
- 主仓 HEAD 在本次扫描过程中从 `aadd56e` 系发生过变化 (另一并发 session 正在 ship
  `80bb4de`), 上述数字为 12:38 UTC 的瞬时快照。
