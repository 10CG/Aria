# state-scanner 扫描结果 (GitHub mirror 补推核查)

## 扫描执行

- `scan.py` 退出码 **10** (部分软错误, snapshot 可用), 输出 `eval-11-github-mirror-unpushed/old_skill/outputs/state-snapshot.json`
- Phase 0.5 `remote_refresh`: 8 条 leg (主仓 + aria / standards / aria-orchestrator 各对 origin=forgejo.10cg.pub 与 github=github.com) **全部 fetch_ok=true**, 新鲜度 `fresh`, 证据不是靠 "Everything up-to-date" 回执而是真实 fetch 后的本地 ref 比对。

## 📍 当前状态

- 分支: `feature/linked-issue-normalization` (主仓与 aria 子模块同名分支; standards detached; aria-orchestrator 在 master)
- 未提交变更 3 项 (untracked: 本 AB 结果目录)
- git 中间态: none

## 🔄 同步状态 (snapshot `sync_status.multi_remote`)

| 仓库 | origin (Forgejo) | github | 说明 |
|------|------------------|--------|------|
| 主仓 `.` | equal (826b356) | unknown / `no_local_tracking_ref` | feature 分支未发布到 GitHub (按约定 feature 分支只推 Forgejo) |
| aria | equal (0fe2e0d) | unknown / `no_local_tracking_ref` | 同上 |
| standards | unknown / `detached_head` | unknown / `detached_head` | 子模块 detached, 不做分支比对 |
| aria-orchestrator | equal (237045a) | equal (237045a) | 双远程一致 |

- `overall_parity = true`, `has_pending_push = false`
- **但 `errors[]` 里有一条 `snapshot_consistency_inconclusive`**: AC-5 对 github 侧 164 个 handoff track 无法评估 (git command failed), scan.py 自己标注 "parity 判决本次视为未验证"。这是软错误, 按退出码 10 契约照常进入推荐, 但 parity 结论要打折。
- `gitlink_integrity`: origin 侧 3 个子模块全 `ok`; github 侧 3 个全 `no_published_ref` (当前 feature 分支在 GitHub 上不存在, 无法做 gitlink 可达性检查 — 不是 orphaned)。

## 针对你的问题: 哪些 remote 需要补推?

**重要限制先说**: snapshot 的 parity 比的是**当前分支** (feature/linked-issue-normalization), 你问的是 **master** 在 GitHub mirror 是否落后。snapshot 本身回答不了 master 这个问题 —— 这正是 2026-04-12 那类事故在 feature 分支上工作时会被 state-scanner 漏看的盲区 (github 侧只给出 `unknown/no_local_tracking_ref`, 不会亮红)。

为了回答你的问题, 我在 scan.py 刚 fetch 完的本地 ref 上做了只读补充比对 (未替代任何 snapshot 字段, 只比 master):

| 仓库 | 本地 master | origin/master | github/master | 结论 |
|------|-------------|---------------|---------------|------|
| 主仓 Aria | 826b356 (落后 origin 12) | 1205ec3 | 1205ec3 | Forgejo == GitHub, **无需补推** |
| aria | 9e6a17c (落后 origin 15) | a0fe720 | a0fe720 | Forgejo == GitHub, **无需补推** |
| standards | 7f74fac (落后 origin 3) | 334c609 | 334c609 | Forgejo == GitHub, **无需补推** |
| aria-orchestrator | 237045a | 237045a | 237045a | 三方一致 |

主仓 origin/master 与 github/master 两边的 gitlink 也一致 (aria=a0fe720 / standards=334c609 / aria-orchestrator=237045a), GitHub 侧 `clone --recursive` 不会断。

**结论: 今天实际仓库里没有复现出 "GitHub mirror 落后 Forgejo" 的状态 —— 四个仓的 master 在两个远程 SHA 完全相同, 没有任何 remote 需要补推。** 反向情况倒是存在: 本地 master 落后 origin/master (主仓 12 / aria 15 / standards 3 个 commit), 这是本地陈旧, 不是镜像分叉。

如果你是要在本机人工演练 2026-04-12 场景, 需要先把某个子模块的 github/master 人为置后, 否则 snapshot 就是上面这样的 "全绿 + 一条 inconclusive 软错误"。

## 🎯 推荐工作流

仅作描述, 未执行 (本次只读):

- **[1] 推荐 — 不动远程**。无 pending push; 若想让本地 master 跟上 Forgejo 再核一次, 可用:
  - `git -C /home/dev/Aria branch -f master origin/master` (主仓; 当前在 feature 分支, 不 checkout)
  - `git -C /home/dev/Aria/aria branch -f master origin/master`
  - `git -C /home/dev/Aria/standards branch -f master origin/master`
  - 之后按约束 2 逐远程核验: `git ls-remote origin master` / `git ls-remote github master`, 两个 SHA 与本地一致才算真正同步
- [2] 若将来真出现 github/master 落后: 在对应子模块本地 `git push github master`, 再 `ls-remote` 两边核验 (禁止 Forgejo 服务端 merge, 见 CLAUDE.md 多远程两条硬约束)
- [3] 跟进 `snapshot_consistency_inconclusive` 软错误 (AC-5 对 github 侧 164 个 track 评估失败): 这条让本次 parity 判决带 "未验证" 标记, 值得单独查 git command 为何失败
- [4] 仅查看状态, 不启动任何工作流

按指令, 不调用 workflow-runner / phase1_gate, 到此为止。
