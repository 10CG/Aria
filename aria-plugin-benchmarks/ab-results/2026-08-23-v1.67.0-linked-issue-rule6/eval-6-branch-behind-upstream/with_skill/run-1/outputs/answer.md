## 状态扫描结果 (state-scanner v3.0, scan.py exit 10 = 部分软错误, snapshot 可用)

先说结论: **你的分支相对自己的 upstream 没有落后 (0/0), 不需要 `git pull`; 但相对 master 已落后 12 个 commit, 需要 `git merge origin/master` (或 rebase) 把主分支新改动合进来。** 另外 aria 子模块也落后其 master 15 个 commit。

### 1. 当前状态

| 项 | 值 |
|---|---|
| 分支 | `feature/linked-issue-normalization` (主仓 Aria) |
| HEAD | `826b356` |
| detached HEAD | 否 (scan.py `git.detached_head = false`) |
| shallow clone | 否 (`git.shallow = false`, `sync_status.shallow = false`) |
| git 中间态 (rebase/merge 暂停) | 无 (`git_operation_in_progress.operation = none`) |
| 中断的 workflow | 无 (`interrupt.status = none`) |
| 未提交变更 | 2 项: `aria` 子模块指针 (workdir 与 tree 不一致) + 1 个未跟踪目录 (本次 AB 结果目录) |
| 关联 OpenSpec | `linked-issue-normalization` (最近 5 个 commit 都在推进它, owner 已 override 进 Phase B) |

你担心的两个特殊场景 (detached HEAD / shallow clone) 主仓都不成立, 所以 ahead/behind 的数字是可信的。唯一 detached 的是 `standards` 子模块 —— 这是 submodule 正常形态, 它和远端 `334c609` 完全一致, 不用管。

### 2. 同步状态 (remote_refresh 刚 fetch 过, 证据等级 fresh, refs 年龄 1 分钟)

**A. 分支 vs 自己的 upstream (`origin/feature/linked-issue-normalization`)**

- ahead 0 / behind 0, 本地 `826b356` = 远端 `826b356`, parity = equal
- 结论: **不需要 `git pull`**, 远端上没有你没拉下来的本分支提交。

**B. 分支 vs 主分支 `origin/master` (这才是你真正想问的)**

scan.py 只算 upstream 差, 不算与 master 的差, 我用只读 `git rev-list --left-right --count` 补了一条:

- `feature/linked-issue-normalization ... origin/master` = 你独有 0 / master 独有 **12**
- `github/master` 同样是 12, 两个远程的 master 一致 (最新 `1205ec3`, 2026-08-23 05:55 UTC, 约 1 小时前)
- master 这 12 个提交是并发轨 #152 (`pre-merge-gate-no-run-for-branch`) 的 ship 全程: aria-plugin **v1.66.5 发布同步** (gitlink `9e6a17c → a0fe720`, 14 处版本字符串: CLAUDE.md / VERSION / README badge / i18n README), 外加 #152 Phase B/D 的 spec 进度与归档、handoff 与 `latest.md` 指针。

注意你分支上没有 master 没有的提交 (0 ahead), 说明你的工作全在 `aria` 子模块里, 主仓这边只是 spec/handoff 文档。所以合并 master 冲突面小, 但 **CLAUDE.md 项目状态段 / VERSION / README badge / latest.md** 是多轨 ship 的高频冲突点, 合并后要核对这几处是否被你的 spec 文档误覆盖。

**C. aria 子模块 (你的代码主战场)**

- 子模块分支 `feature/linked-issue-normalization` @ `0fe2e0d`, 和自己的 upstream 一致 (0/0)
- 但相对 `aria` 的 `origin/master` (`a0fe720` = v1.66.5): 你独有 2 / master 独有 **15**
- 主仓 tree 记的 gitlink 是 `9e6a17c`, 你的 workdir 是 `0fe2e0d`, master 已经是 `a0fe720` —— 三个值互不相同, 这就是 scan.py 报的 `workdir_vs_tree = true` + `tree_vs_remote = true`
- 你的 spec ship target 是 v1.67.0, 而 master 已经发了 v1.66.5, 子模块那 15 个提交必须合进来, 否则你发版时版本号和 CHANGELOG 会打架。

**D. 多远程 parity**: `overall_parity = true`, origin 和 github 两端可达且无待推送; `github` 对本 feature 分支显示 `unknown / no_local_tracking_ref` 是因为 feature 分支只推了 origin, 没推 github (正常, 发版时才双推 master)。gitlink 完整性: origin 三个子模块都 `ok`; github 三个都 `no_published_ref` (同理, feature 分支未发布到 github)。

### 3. 自定义检查: 10/10 通过 (含 `m6-version-badge-match` = 1.66.4, 这是你本地旧值, 合并 master 后会变 1.66.5)

### 4. 软错误说明 (exit 10)

`snapshot_consistency` 报: 164 份 handoff 文件在 `github` 远程上无法做 AC-5 核验 (原因同上: feature 分支没推 github), snapshot 把 `overall_parity = true` 标记为「本次未核实」。这不影响分支落后判断, 只是告诉你 github 那一侧没有这个分支的证据。

### 5. 推荐工作流

- **[1] (推荐) 先同步 master, 再继续开发** —— 步骤:
  1. `git fetch --all` (scan 刚做过, 可跳)
  2. 主仓: `git merge origin/master` (你分支 0 ahead, 实际会 fast-forward 式干净合并; 若想保持线性历史用 `git rebase origin/master`, 分支未被他人基于, rebase 也安全)
  3. 子模块: `cd aria && git merge origin/master` (你有 2 个独有提交, 会产生 merge commit; 必须本地合, 禁 Forgejo 服务端合并)
  4. 核对冲突高发点: `CLAUDE.md` 项目状态段、`VERSION`、README badge、`docs/handoff/latest.md` 只保留 1 个 bare Latest 指针
  5. 合完跑一次 `/state-scanner` 确认 behind 归 0, 再继续 Phase B
- **[2] 不合并, 继续开发** —— 只适合你接下来 1-2 小时内不碰版本文件; 但 v1.66.5 已经发出去, 越晚合越多冲突, 不建议。
- **[3] 仅查看状态** (本次已完成)。
- **[4] 自定义组合**。

**理由**: upstream 本身不落后 (pull 是空操作), 真正的落后在 master (主仓 12 / aria 子模块 15), 且里面含一次版本发布, 直接影响你 v1.67.0 的 ship 面。当前 Level 1 变更 (只动 2 个非代码项), 无 git 中间态、无中断, 合并时机最好。

要我按 [1] 的步骤执行合并吗 (需要你确认, 我不会代你操作 git)?
