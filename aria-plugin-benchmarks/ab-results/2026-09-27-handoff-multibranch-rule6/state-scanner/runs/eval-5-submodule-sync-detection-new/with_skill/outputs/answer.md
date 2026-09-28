# 状态扫描结果: 子模块同步情况

已按 state-scanner 流程运行 `scan.py`，退出码为 0，`errors[]` 为空。扫描前已对 8 个远程分支 (主仓和 3 个子模块，每个都有 origin 和 github) 做了新鲜 fetch，全部成功，证据等级都是 `fresh`，refs 是 1 分钟前的。下面的判断基于刚拉到的远程数据，不是旧缓存。

## 结论: 不需要运行 `git submodule update`，而且现在运行反而有害

- **3 个子模块都没有落后远程。** 主仓记录的子模块版本 (gitlink) 和各子模块远程默认分支的最新提交完全一致 (`tree_vs_remote=false`)，`behind_count` 都是 0，`submodule_drift` 规则没有触发。协作者如果推过子模块更新，这些更新已经被主仓的 gitlink 记录了。
- **`aria` 和 `standards` 显示 `M` (有修改)，原因是本地领先，不是落后。** 这两个子模块现在检出的是你正在开发的 feature 分支，比主仓记录的版本多出几个提交:

| 子模块 | 本地 HEAD | 主仓记录的版本 (= 远程 master) | 关系 |
|---|---|---|---|
| aria | `b181678` (feature/handoff-multibranch-subdir-path-fidelity) | `1cb3872` | 本地领先 9 个提交，落后 0 |
| standards | `d86fc91` (同名 feature 分支) | `940cb5b` | 本地领先 2 个提交，落后 0 |
| aria-orchestrator | `237045a` (master) | `237045a` | 完全一致 |

- **如果现在运行 `git submodule update`:** `aria` 和 `standards` 会被强制切回 `1cb3872` / `940cb5b`，并进入 detached HEAD 状态。你 #195 这条线的 9 个和 2 个提交会从工作目录里消失。这些提交已经推送到两个远程 (见下文的 parity)，所以不会真的丢，但工作区会被回退，还得手动切回 feature 分支。
- `git submodule update --remote` 也没有意义，因为远程 master 并没有比 gitlink 更新的内容。

## 状态区块

**📍 当前状态**
- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (没有设置 upstream，`reason=no_upstream`)
- 变更: 3 项 = `aria`、`standards` 两个 gitlink 变化 + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 没有进行中的 git 操作 (rebase/merge 等)；没有中断的工作流 (`interrupt.status=none`)

**📊 变更分析**: 复杂度 Level 2；没有代码或测试文件变更；没有检出 SKILL.md 变更；不涉及架构

**📋 OpenSpec**: 8 个活跃变更，0 个待归档；⚠️ 5 个「设计未实施」，例如 `aria-2.0-m6-release-closeout` 已停滞 124 天，`aria-2.0-m6-cost-model-telemetry` 已停滞 79 天

**🛡️ 审计**: 已启用；上次是 post_planning R7，结果 PASS，已收敛 (2026-09-24)

**🔧 自定义检查**: 16/16 通过

**🔄 同步状态** (本次重点)
- 主仓 feature 分支 与 origin、github: 两边都一致 (`4f91772`)，没有未推送的提交
- 子模块多远程 parity: aria `b181678`、standards `d86fc91`、aria-orchestrator `237045a` 在 origin 和 github 上都一致
- `gitlink_integrity`: 3 个子模块 × 2 个远程，结果全部 `ok` (主仓已发布的 gitlink 在各远程都能找到，不存在孤儿 gitlink)
- `overall_parity = true`，`has_pending_push = false`
- 📝 README 版本一致 (aria-plugin 1.73.3)；📦 standards 子模块已注册并初始化
- 补充 (只读的 `git rev-list`，不属于 snapshot 字段): 主仓 feature 分支比 `origin/master` 和 `github/master` **落后 12 个提交、领先 13 个提交**。协作者最近的推送主要在主仓 master 上，但这 12 个提交**没有改动子模块指针** (master 上 3 个 gitlink 与本分支记录的相同)。所以要跟上的是主仓 master，不是子模块。
- 🔗 Forgejo 配置: 缺少 `.aria/forgejo` 配置 (检测到 forgejo.10cg.pub 远程)，可以用 `/forgejo-sync` 引导创建

**多终端提示 (advisory)**: `tracks_multibranch.collision.kind = self_multi_container`。track 身份 `023236f2` 和 `bfe8285d` 同时被 `simonfish` 和 `aria-runner-bot` 认领过，说明同一仓库里还有别的容器或自主运行时在干活。开始新的 Phase B 之前应该先看对方的 handoff。

**Handoff**: 最新一份是 `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md` (约 60 小时前)

## 🎯 推荐工作流

子模块本身不需要做任何操作。按你的实际意图选:

- **[1] (推荐) 什么都不更新，继续当前 #195 工作**: 保持 `aria`、`standards` 在 feature 分支上。等 #195 合并时，按项目规则先在子模块**本地** `git merge` 到 master 并双推，用 `ls-remote` 逐个核验，然后再在主仓提交 gitlink bump。
  - 理由: 子模块没有落后，`M` 是正常的开发中状态。
- **[2] 同步主仓 master (合入协作者的 12 个提交)**: 在主仓把 `origin/master` 合并进当前 feature 分支。因为 master 没有改动 gitlink，合并后子模块指针仍然是你的版本，不需要 `submodule update`。
  - 注意: 合并前先把未跟踪的 AB 结果目录提交或保留好。
- **[3] 只想把子模块对齐到主仓记录的版本 (放弃在 feature 上的状态)**: 这时才运行 `git submodule update`，也就是 `git submodule update --init --recursive`。
  - 代价: `aria` 和 `standards` 会 detach 到 `1cb3872` / `940cb5b`，#195 的 9 个和 2 个提交会离开工作区 (远程上还在)。**不推荐**。
- **[4] 自定义**: 例如只做 C.1 提交 (gitlink 和 AB 结果目录)，或者先看多终端对方的 handoff。

说明: 如果选 [1] 或 [2] 并进入 Phase B，按 skill 流程会调用 `phase1_gate.py` 做认领 (`--raw-track-id "<handoff §6 carry-id>" --phase B --mode advisory --repo-path /home/dev/Aria`)。本次是只读扫描，没有执行这一步。
