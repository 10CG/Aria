## 结论先说：不需要 `git submodule update`，而且现在跑它反而有害

扫描 (scan.py exit 0，`errors[]` 为空，远程引用 1 分钟前刚 fetch 过，证据等级全部 `fresh`) 显示：**3 个子模块都没有落后远程**。
`aria` 和 `standards` 的状态是「本地比主仓记录的 gitlink **领先**」，不是落后 —— 这是你当前 feature 分支上的正在进行的工作。
如果现在执行 `git submodule update`，git 会把 `aria` / `standards` 检出回主仓记录的旧 commit (detached HEAD)，等于把你从 feature 分支上拽下来。

---

### 📍 当前状态
- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (HEAD `4f91772`)
- 变更文件数: 3 (`aria`、`standards` 两个 gitlink 显示为已修改 + 1 个未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`)
- 关联 OpenSpec: `handoff-multibranch-subdir-path-fidelity` (approved)
- git 中间态: 无 (`git_operation_in_progress.operation = none`)；中断状态: 无 (`interrupt.status = none`)

### 📊 变更分析
- 变更类型: other x3 (两个子模块指针 + 一个 benchmark 结果目录)，无代码/测试文件
- 复杂度: Level 2 | 架构影响: 否 | Skill 变更检出: 否

### 📄 需求状态
- PRD: `prd-aria-v1.md` (active) / `prd-aria-v2.md` (Approved)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

### 🏗️ 架构状态
- `docs/architecture/system-architecture.md` 存在，status Active，最后更新 2026-09-02，需求链路完整

### 📋 OpenSpec 状态
- 活跃变更 8 个 (全部 approved)，已归档 146，待归档 0
- ⚠️ 设计未实施 5 个 (例如 `aria-2.0-m6-release-closeout` 41/41 未勾、陈旧 124 天；`aria-2.0-m7-agent-lifecycle` 陈旧 100 天) —— 与本次同步问题无关，仅提示

### 🛡️ 审计状态
- 已启用；上次审计 `post_planning` R7，verdict PASS，已收敛 (2026-09-24)

### 🔧 自定义检查
- 16/16 通过，0 失败

### 🔄 同步状态 (本次重点)

**主仓**
| 远程 | 本地 HEAD | 远程同名分支 | 差距 | 证据 |
|------|-----------|--------------|------|------|
| origin (forgejo) | `4f91772` | `4f91772` | 0 领先 / 0 落后 | fresh |
| github | `4f91772` | `4f91772` | 0 领先 / 0 落后 | fresh |

注: 当前分支没有配置 upstream (`reason: no_upstream`)，所以 `git status` 不会显示 ahead/behind；但多远程比对已确认两个远程上的同名分支和本地一致。`overall_parity = true`。

**子模块 (三层对比: 工作目录 HEAD / 主仓记录的 gitlink / 远程默认分支)**
| 子模块 | 工作目录 HEAD | 主仓 gitlink | 远程默认分支 | 落后远程? | 说明 |
|--------|---------------|--------------|--------------|-----------|------|
| `aria` | `b181678` (feature 分支) | `1cb3872` | `1cb3872` | 否 (behind 0) | 工作目录比 gitlink 领先 9 个 commit |
| `standards` | `d86fc91` (feature 分支) | `940cb5b` | `940cb5b` | 否 (behind 0) | 工作目录比 gitlink 领先 2 个 commit |
| `aria-orchestrator` | `237045a` (master) | `237045a` | `237045a` | 否 | 三者完全一致 |

- `tree_vs_remote` 三个子模块全部为 `false` —— 主仓记录的 gitlink 就是远程默认分支的最新 commit，**远程没有你还没拉下来的新提交**。因此 `submodule_drift` 规则不触发。
- `aria` / `standards` 的 `workdir_vs_tree = true`：方向是本地领先 (9 个和 2 个 commit，都是 10CG/Aria#195 的文档提交)，这正是 `git status` 里 `M aria` / `M standards` 的来源。
- 这两个子模块的 feature 分支也已推到 origin 和 github 两个远程，且和本地一致 (parity equal)，不存在「只在本地」的提交。
- gitlink 完整性 (`gitlink_integrity`)：6 组 (2 个远程 x 3 个子模块) 全部 `ok`，没有孤儿 gitlink，GitHub 上 `clone --recursive` 不会断。

**所以关于 `git submodule update`：**
- `git submodule update` (不带参数)：会把 `aria` 检出到 `1cb3872`、`standards` 检出到 `940cb5b`，变成 detached HEAD，离开 feature 分支。提交不会丢 (已推远程)，但你会以为改动「没了」，还要手工切回分支。**不要跑。**
- `git submodule update --remote`：远程默认分支和 gitlink 一样，结果同上，也不要跑。
- 你说「其他协作者推送了子模块更新」—— 本次扫描在 1 分钟前 fetch 了全部 8 条 (主仓 + 3 个子模块) x (origin + github) 远程，均成功，没有看到比你本地更新的远程提交。如果协作者推的是别的分支 (不是默认分支、也不是你当前的 feature 分支)，那不在这个比对里；你可以说一下是哪个分支，我再核对。

子项: 📝 README 版本一致 (aria 插件 1.73.3 = README 1.73.3) / 📦 standards 子模块已注册且已初始化 / 🔗 Forgejo 配置: `.aria/forgejo` 配置缺失 (可用 `/forgejo-sync` 引导创建，与本次无关)

### 🎫 Open Issues
- open 49 个 (bug 标签 4 个)，最新如 10CG/Aria#221 (secret-guard 进程表旁路)、#220、#218 等；无直接关联本次同步的问题

### 多终端协调提示 (tracks_multibranch)
- 检测到 `collision.kind = self_multi_container` (同一 owner 在多个容器上有轨道，另有 aria-runner-bot 共享身份记录)。这只是 advisory 提示。
- 按流程，只有你确认进入 Phase B 时才会调用认领闸门，届时会执行 (本次未执行，仅列出):
  `python3 <plugin>/skills/state-scanner/scripts/phase1_gate.py --raw-track-id "<handoff §6 选定的 carry-id>" --phase B --mode advisory --repo-path /home/dev/Aria`
- 最新 handoff 指针指向 `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md` (约 60 小时前，内容是 #199 的轨道)，而你当前分支是 #195 的轨道 —— 如果接下来要继续 #195，建议先读那份 handoff 和 #195 的台账，确认没有另一个容器正占着这条轨道。

### 🎯 推荐工作流

**[1] 不做子模块更新，继续当前 feature 分支工作 (推荐)**
- 理由: 子模块没有落后远程；`M aria` / `M standards` 是你本分支有意推进的指针，下一步应该是把新的 gitlink 提交进主仓 (C.1)，而不是回退它们。
- 步骤: 如需提交，`git add aria standards` 后按 Conventional Commits 提交 gitlink bump (C.1)，再按多远程规则双推并对每个远程 `ls-remote` 核验。
- 跳过: `git submodule update`

**[2] 仅查看状态，不做任何动作**
- 同步已确认无问题，到此结束。

**[3] 如果你确实想让工作目录回到主仓记录的版本 (放弃在 feature 分支上看子模块改动)**
- 命令: `git submodule update --init --recursive` —— 会让 `aria`/`standards` 变 detached HEAD 在 `1cb3872` / `940cb5b`。提交已推远程不会丢，但需要之后 `git -C aria checkout feature/handoff-multibranch-subdir-path-fidelity` 切回。一般不建议。

**[4] 核对某个特定的协作者分支**
- 告诉我协作者推的是哪个子模块的哪个分支，我基于已 fetch 的远程引用比对它和你本地的差距。

请选 [1]-[4]，或给出自定义组合。
