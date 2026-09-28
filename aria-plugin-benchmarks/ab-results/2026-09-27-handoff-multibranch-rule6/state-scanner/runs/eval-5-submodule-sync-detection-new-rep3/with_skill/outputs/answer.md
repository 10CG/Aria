# 状态扫描结果：子模块是否需要 `git submodule update`

**结论：不需要。** 三个子模块都**没有落后远程**，主仓记录的子模块版本和两个远程 (origin / github) 的 master 完全一致。`aria` 和 `standards` 显示为 `M` 是因为它们的工作区**领先**主仓记录 (在 feature 分支上多了新提交)，不是落后。这时跑 `git submodule update` 反而会把这两个子模块从 feature 分支切走。

扫描方式：`scan.py` 机械采集，退出码 0 (全部采集成功，`errors[]` 为空)。扫描时刚对 4 个仓库 (主仓 + 3 子模块) × 2 个远程共 8 路做了 fetch，全部成功，证据等级 `fresh` (远程引用约 1 分钟前刷新)。所以下面的"是否落后"判断用的是最新远程数据，不是过期的本地缓存。

---

## 当前状态

| 项 | 值 |
|----|----|
| 分支 | `feature/handoff-multibranch-subdir-path-fidelity` (HEAD `4f91772`) |
| 未提交变更 | 3 项：`aria` (gitlink 变动)、`standards` (gitlink 变动)、未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` |
| git 中间态 | 无 (没有暂停中的 rebase/merge) |
| 中断的工作流 | 无 |
| 变更分析 | 0 代码 / 0 文档 / 3 其他；无 Skill 文件变更，不需要 AB 基准 |

## 同步状态 (本次重点)

### 子模块和远程的对比

| 子模块 | 主仓记录的版本 (gitlink) | 远程 master | 子模块工作区 HEAD | 落后远程 | 领先远程 | 工作区偏离主仓记录 |
|--------|------|------|------|------|------|------|
| `aria` | `1cb3872` | `1cb3872` | `b181678` (feature 分支) | 0 | 0 | 是，工作区多 9 个提交 |
| `standards` | `940cb5b` | `940cb5b` | `d86fc91` (feature 分支) | 0 | 0 | 是，工作区多 2 个提交 |
| `aria-orchestrator` | `237045a` | `237045a` | `237045a` (master) | 0 | 0 | 否 |

怎么读这张表：

- **"主仓记录的版本 = 远程 master"** (三个都是) → 子模块**没有落后远程**。扫描器的 `submodule_drift` 规则 (只在 `behind_count > 0` 时触发) **没有触发**，也没有生成 `git submodule update --remote` 提示。
- **"工作区偏离主仓记录"** (`aria`、`standards`) → 子模块当前 checkout 的是 feature 分支上更新的提交。我额外用只读的 `git merge-base --is-ancestor` 核对过方向：主仓记录的 `1cb3872` / `940cb5b` 分别是工作区 HEAD 的祖先，也就是说工作区在记录版本**之后**，是**领先**，不是分叉或落后。`git status` 里的 ` M aria` / ` M standards` 就是这个原因。

### 多远程一致性 (origin = forgejo.10cg.pub，github = github.com)

| 仓库 | 本地 HEAD | origin | github | 结论 |
|------|------|------|------|------|
| 主仓 (当前 feature 分支) | `4f91772` | `4f91772` | `4f91772` | 一致 |
| `aria` (feature 分支) | `b181678` | `b181678` | `b181678` | 一致 (已双推) |
| `standards` (feature 分支) | `d86fc91` | `d86fc91` | `d86fc91` | 一致 (已双推) |
| `aria-orchestrator` (master) | `237045a` | `237045a` | `237045a` | 一致 |

- `overall_parity = true`，没有待推送的提交 (`has_pending_push = false`)，没有连不上的远程。
- gitlink 完整性：主仓在两个远程上发布的提交所引用的 3 个子模块版本，在对应子模块的两个远程上都能找到，6 组检查全部 `ok`。别人 `clone --recursive` 不会断。
- 主仓当前分支**没有设置 upstream** (`no_upstream`)，所以"当前分支 ahead/behind"这一项没有数据；不过多远程对比已经确认同名远程分支和本地一致。

### 其他同步项

- README 版本：`aria` 插件 `1.73.3` 与 README 一致。
- Forgejo 配置：检测到 forgejo 远程，但 `.aria` 下没有 Forgejo 配置 (提示可运行 `/forgejo-sync` 引导创建；和本问题无关)。

## 其他区块 (简要)

- **需求状态**：PRD 2 份 (v1 Active / v2 Approved)；User Story：done 17、in_progress 2、approved 1、pending 1。
- **架构状态**：`docs/architecture/system-architecture.md` 存在，Active，最后更新 2026-09-02，需求链路完整。
- **审计状态**：审计已启用；上次审计 `post_planning`，已收敛，结论 PASS (2026-09-24)。
- **自定义检查**：16 项全部通过。
- **交接 (handoff)**：最新交接文件 `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md` (约 60 小时前)；没有其他 worktree 上更新的交接。
- **多终端协调提示**：`tracks_multibranch.collision.kind = self_multi_container`，即同一 owner 的两个容器 (`simonfish` 与 `aria-runner-bot`) 在相同轨道标识 (`023236f2`、`bfe8285d`) 上都有记录。这只是提醒，不会阻止操作。如果接下来要进入 Phase B，编排层会运行下面这条命令做 advisory 认领 (本次是只读扫描，**没有执行**)：
  ```bash
  python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py \
    --raw-track-id "<交接文件 §6 选定的 carry-id 原始串>" --phase B --mode advisory --repo-path /home/dev/Aria
  ```

## 推荐工作流

**[1] 不做 submodule update，继续当前 feature 分支上的工作 (推荐)**
- 理由：三个子模块都没落后远程，没有需要拉取的内容。`aria` / `standards` 在 feature 分支上领先的 9 / 2 个提交已经推到两个远程。
- 如果你担心的"协作者推送了子模块更新"指的是其他分支 (不是 master)，可以先告诉我是哪个分支。扫描器对比的是子模块远程 master (`origin/master`、`github/master`)，这两者都等于主仓记录的版本。

**[2] 让子模块回到主仓记录的版本：`git submodule update`**
- 后果：`aria` 会切到 detached `1cb3872`，`standards` 会切到 detached `940cb5b`，也就是离开 feature 分支。已提交的内容不会丢 (在 feature 分支上，而且已双推)，但工作区会回退到旧版本，当前 feature 工作会中断。
- 只有你确实想放弃当前子模块的 feature 状态时才选这个。**不建议** `git submodule update --remote`：它会跳到远程 master 的最新版本，而那也就是 `1cb3872` / `940cb5b`，效果和上面一样。

**[3] feature 完成后，把子模块的新提交正式记入主仓 (Phase C 路径)**
- 步骤：子模块先在**本地**合并到 master，然后双推 (项目硬约束 1：子模块禁用 Forgejo 服务端合并)。推完后对每个远程逐个用 `git ls-remote <remote> master` 核对 SHA (硬约束 2)。全部一致之后，再在主仓提交 gitlink 更新。
- 注意：未跟踪的 AB 结果目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` 要一起决定是否纳入提交。

**[4] 只查看，不做任何操作**
- 本次扫描已经回答了你的问题，可以直接结束。

跳过项：不需要 `submodule_drift` 相关修复步骤 (规则未触发)；不需要 Skill AB 基准 (没有 Skill 变更)。
