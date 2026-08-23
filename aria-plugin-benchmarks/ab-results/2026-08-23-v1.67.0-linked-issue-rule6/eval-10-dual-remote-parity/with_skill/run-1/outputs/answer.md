已按 state-scanner Step 0 机械跑 `scan.py` (退出码 10 = 软错误, snapshot 可用), 再对 snapshot 引用的 ref 做了只读核对。先说结论: **你描述的「v1.15.0 推了 Forgejo 没推 GitHub」与仓库实际状态对不上**, 真实落后面在别处。

## 📍 当前状态

- 分支: `feature/linked-issue-normalization` (主仓), 不在 master
- 工作树: 2 个变更文件 (非代码), Level 1, 无中断态 / 无进行中 git 操作
- 插件版本 SOT `aria/.claude-plugin/plugin.json` = **1.66.4** (不是 v1.15.0; 最近 tag v1.66.3, aria 子模块 HEAD = v1.66.3-17-g0fe2e0d)
- 最新 handoff: `docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md` (9h 前)
- 并发轨: `tracks_multibranch.collision.kind = self_multi_container` (dev-claude / aria-runner-bot 两组), 进 Phase B 前需走 phase1_gate 认领 (本次只扫描, 未调)

## 🔄 同步状态 (remote_refresh 8 条 leg 全部 fetch 成功, 证据等级 fresh, 1 分钟内)

**A. master 分支 — 两个 remote 完全一致, 没有落后**

| 仓库 | origin/master (Forgejo) | github/master | 判定 |
|------|------|------|------|
| 主仓 Aria | 1205ec3 | 1205ec3 | 同步 |
| aria (插件) | a0fe720 | a0fe720 | 同步 |
| standards | 334c609 | 334c609 | 同步 |
| aria-orchestrator | 237045a | 237045a | 同步 |

gitlink 完整性: origin 三个子模块 `ok`; github 三个为 `no_published_ref` (github 上没有当前 feature 分支, 所以无法对该分支验 gitlink, 不是 orphan)。

**B. 真正落后的是当前 feature 分支 — origin 有, github 没有**

| 仓库 | 本地 HEAD | origin | github | 判定 |
|------|------|------|------|------|
| 主仓 `feature/linked-issue-normalization` | 826b356 | 826b356 (equal, 0/0) | 无此分支 (`no_local_tracking_ref`) | **github 落后** |
| aria `feature/linked-issue-normalization` | 0fe2e0d | 0fe2e0d (equal, 0/0) | 无此分支 | **github 落后** |
| standards (detached) | 334c609 | = master | = master | 同步 |
| aria-orchestrator master | 237045a | equal | equal | 同步 |

**C. 本地自身的漂移 (与远端无关, 但会影响下一次 ship)**

- aria 子模块: 主仓 index 记的 gitlink = 9e6a17c, 工作树 HEAD = 0fe2e0d, 远端 master = a0fe720 —— 本地 checkout **落后远端 master 15 个 commit** (`tree_vs_remote=true`, `workdir_vs_tree=true`)。提示命令: `git submodule update --remote aria`。
- 主仓本地 `master` = 826b356 ≠ origin/master 1205ec3 (本地 master 陈旧, 不影响远端)。

**D. scan.py 软错误 (exit 10)**: `snapshot_consistency_inconclusive` —— AC-5 对 github 上 164 条 handoff track 无法核验 (github 无该 feature 分支, git 命令失败), 而 snapshot 同时报 `overall_parity=true`。按契约把 `overall_parity=true` **视为未经核验**; 上面的 master 一致性是我用已 fetch 的本地 ref 独立比对的, 可信。

## 修复命令 (只描述, 未执行; 全部走 `git -C <path>`, 双推后逐 remote `ls-remote` 核验)

(1) 把 feature 分支补推到 github (先子模块, 后主仓, 顺序不能反):

```bash
git -C /home/dev/Aria/aria push github feature/linked-issue-normalization
git -C /home/dev/Aria push github feature/linked-issue-normalization
```

(2) 推后核验, 不信 push 回执:

```bash
for r in origin github; do git -C /home/dev/Aria ls-remote $r refs/heads/feature/linked-issue-normalization; done
for r in origin github; do git -C /home/dev/Aria/aria ls-remote $r refs/heads/feature/linked-issue-normalization; done
# 两行输出 SHA 分别应为 826b356... 与 0fe2e0d...
```

(3) 如果你的本意确实是「某次 master 发布只推了 origin」: 现状 master 两边已一致, **不需要任何操作**。通用补推模板是:

```bash
git -C /home/dev/Aria/aria push github master && git -C /home/dev/Aria push github master
for r in origin github; do git -C /home/dev/Aria ls-remote $r master; git -C /home/dev/Aria/aria ls-remote $r master; done
```

(4) 本地 aria 子模块落后 15 commit, 若要对齐远端 master (会改工作树, 你自己决定时机):

```bash
git -C /home/dev/Aria submodule update --remote aria
```

## 🎯 推荐工作流

- [1] **(推荐) 只做补推**: 执行 (1)+(2), 然后重跑 `/state-scanner` 确认 `no_local_tracking_ref` 消失。不需要 OpenSpec (纯同步操作)。
- [2] 继续 feature 分支开发: 先过 phase1_gate 认领 (self_multi_container 碰撞), 再进 Phase B。
- [3] 不动: 如果这个 feature 分支本来就只打算留在 Forgejo 上评审, 那 github 落后是预期行为, 合入 master 时 C.2.5 会双推。

另请核对一下你说的 v1.15.0 从哪来 —— 仓库里版本已到 1.66.4, 两端 master 上也没有未推的发布。
