# 状态扫描结果 (state-scanner v3.0, scan.py exit 10 = 部分软错误, snapshot 可用)

## 📍 当前状态
- 主仓分支: `feature/linked-issue-normalization` (HEAD `826b356`), 无 git 中间态 (rebase/merge), 无中断的 workflow
- 未提交: 2 项 —— `aria` 子模块指针 (unstaged, 工作目录 HEAD 与主仓记录不同) + 本次 AB 结果目录 (untracked)
- Phase 1.12 同步检测恒开, Phase 0.5 已对 4 个仓 x 2 个 remote (origin=forgejo / github) 共 8 条 leg 全部 fetch 成功, 证据等级全部 `fresh` —— 下面的结论是刚 fetch 过的新鲜数据, 不是陈旧 ref

## 🔄 同步状态

**主仓**: `feature/linked-issue-normalization` 与 `origin/...` ahead 0 / behind 0, 完全同步 (github 无此分支的 tracking ref, 属 feature 分支未双推的正常情况)。

**三个子模块逐个看** (tree = 主仓记录的 gitlink / head = 本地实际检出 / remote = 远程默认分支):

| 子模块 | 主仓记录 (tree) | 本地检出 (head) | 远程 master | 落后 | 结论 |
|--------|----------------|-----------------|-------------|------|------|
| `standards` | `334c609` | `334c609` | `334c609` | 0 | 同步, 不用动 |
| `aria-orchestrator` | `237045a` | `237045a` | `237045a` (origin + github 一致) | 0 | 同步, 不用动 |
| `aria` | `9e6a17c` (v1.66.4 release) | `0fe2e0d` (feature 分支) | `a0fe720` (v1.66.5, #152 合并) | **15 commits** | **落后, 但不要直接 `submodule update`** (见下) |

**多远程 parity**: `overall_parity=true`; gitlink 完整性 origin 侧 3/3 `ok`, github 侧 3 条 `no_published_ref` (feature 分支没推 github, 非 orphaned, 不阻断)。

## ⚠️ `aria` 子模块的细节 —— 这是唯一需要处理的地方

它不是简单的"本地落后远程", 而是三个点各不相同:

1. 主仓记录的 gitlink `9e6a17c` = v1.66.4 release 提交
2. 本地实际检出的 `0fe2e0d` 在 `aria` 子模块自己的 `feature/linked-issue-normalization` 分支上, 比 gitlink 多 2 个 commit (本轨 #128/linked-issue 的工作), 且与 `origin/feature/linked-issue-normalization` 同步
3. 远程 `origin/master` 已前进到 `a0fe720` = v1.66.5 (`#152 pre-merge gate 零 run 显影` 合并), 比 gitlink 和本地 feature 分支都多 15 个 commit; 这 15 个 commit **不包含**在本地 feature 分支里

所以 "协作者推送的 submodule 更新" 指的就是 aria 的 master 多了 15 个 commit (v1.66.5)。本地 feature 分支基于 v1.66.4, 已经落后一个发布版本。

## 🎯 推荐

**不建议直接跑 `git submodule update --remote aria`** (虽然 scan.py 的 drift hint 是这条)。原因: 这条命令会把 aria 子模块 detached 到 `origin/master` (`a0fe720`), 把你当前检出的 feature 分支切走 —— 2 个本轨提交不会丢 (分支还在), 但工作现场会被替换, 而且你的本轨目标是 v1.67.0, 要的是把 v1.66.5 并进来, 不是切过去。

另两个子模块 (`standards` / `aria-orchestrator`) 已经和远程一致, 对它们跑 `submodule update` 是 no-op。

建议做法 (只读扫描已完成, 以下操作请你自己执行):

```bash
# 在 aria 子模块内, 把远程 master (v1.66.5) 并进本轨 feature 分支
git -C aria fetch origin
git -C aria merge origin/master        # 或 rebase, 按你本轨的习惯
# 主仓的 aria gitlink 等本轨 ship 时再一次性 bump (C.2 / 发版同步面), 现在不用动
```

并后重跑 `/state-scanner`, 预期 `aria.drift.behind_count` 归 0。

**其他提示** (非阻塞):
- `tracks_multibranch.collision.kind = self_multi_container`: 同一 owner 的多个容器 (`dev-claude` / `aria-runner-bot`) 在同仓有并行轨; 进 Phase B 时 phase1_gate 会做 advisory 认领, 本次只读扫描不触发。
- scan.py exit 10 的软错误: `snapshot_consistency` 对 github remote 上 164 条 legacy handoff track 做 AC-5 核对时 git 命令失败, 属 github 侧没有 feature 分支 ref 的副作用; 对上面子模块结论无影响, parity 判决视为"未经该项交叉验证"。
- 10 项自定义检查全部 PASS (版本 badge 1.66.4 一致、i18n README 同步等), 这次没有新的问题。

一句话回答: **需要同步的只有 `aria` 子模块 (落后远程 master 15 个 commit, v1.66.4 → v1.66.5), 但因为你正在它的 feature 分支上干活, 应该在子模块内 merge/rebase `origin/master`, 而不是跑 `git submodule update`; `standards` 和 `aria-orchestrator` 已与远程一致, 不需要更新。**
