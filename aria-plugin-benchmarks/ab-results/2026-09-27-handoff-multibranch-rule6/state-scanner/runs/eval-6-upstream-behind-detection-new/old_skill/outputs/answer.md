已按 state-scanner 流程跑完 scan.py（退出码 0，`errors[]` 为空，远程引用 1 分钟前刚 fetch 过，证据等级 fresh）。先说结论，再给完整状态。

## 结论（直接回答你的问题）

1. **detached HEAD：没有。** `git.detached_head=false`，当前在分支 `feature/handoff-multibranch-subdir-path-fidelity`，HEAD = `4f91772`。
2. **shallow clone：不是。** `git.shallow=false` / `sync_status.shallow=false`，计数不会因为浅克隆失效。
3. **没有进行中的 git 操作**（`git_operation_in_progress.operation=none`，无 rebase/merge 暂停态、无冲突）。
4. **你的分支没有配置 upstream**（`upstream.configured=false`，`reason=no_upstream`），所以 scan.py 按规范**不计算 ahead/behind**，这两个字段是 `null`，`branch_behind_upstream` 规则因 `reason != null` 被跳过。**这不等于"不落后"，而是"没法算"。**
5. **feature 分支自己的远程副本与本地完全一致**：origin 与 github 上这个分支都是 `4f91772`，ahead=0 / behind=0，证据 fresh。也就是说**没有别人往你这个 feature 分支推过东西，对这个分支执行 `git pull` 拉不到任何新内容**。
6. **你真正关心的"主分支 master 有没有新改动"——本次扫描没有测。** scan.py 只比较"当前分支 vs 它的 upstream"和"各远程之间是否一致"，不比较"feature 分支 vs master"。我不会用手工 git 命令替 scan.py 补这个数（skill 规定不得逐字段手工采集），下面给你一条只读命令自己确认。

**要不要 `git pull`？** 不需要，而且在这里也不是正确的工具：
- 当前分支无 upstream，直接 `git pull` 会报 "There is no tracking information for the current branch"；
- 就算配好 upstream，pull 拉的也是 `origin/feature/handoff-multibranch-subdir-path-fidelity`（已确认没有新提交），**拉不到 master 的改动**。

想把 master 的新改动并进来，应该这样做（远程引用刚刷新过，不用再 fetch）：

```bash
# 只读: 看 feature 与 origin/master 的差距, 输出 "<master 独有提交数>  <feature 独有提交数>"
git rev-list --left-right --count origin/master...HEAD
```

- 左边数字为 0 → master 没有你缺的改动，什么都不用做。
- 左边数字 > 0 → master 有新改动。由于你的分支**已经推到 origin 和 github 两个远程**，建议用 merge 而不是 rebase（rebase 会改写已推送的提交，之后得对两个远程 force push，按项目多远程约束风险高）：
  ```bash
  git merge origin/master
  ```

合并前注意下面第"同步状态"段提到的**两个未提交的子模块指针改动**，先处理掉再合并，否则容易在 `aria` / `standards` 的 gitlink 上冲突。

---

## 完整状态

### 📍 当前状态
- 分支: `feature/handoff-multibranch-subdir-path-fidelity`（HEAD `4f91772`）
- 模块 / Phase·Cycle: UPM 未配置（`upm.configured=false`）
- 变更文件数: 3（已暂存 0 / 未暂存 2: `aria`、`standards` / 未跟踪 1: `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`）
- 最近提交: `4f91772 docs(openspec): 10CG/Aria#195 台账记 owner 2026-09-27 裁定与 feature 双推`

### 📊 变更分析
- 变更类型: other×3（两个子模块指针 + 一个 AB 结果目录），无 code / test / docs
- 复杂度: Level 2 | 架构影响: 无 | 测试覆盖: 无测试变更
- Skill 变更: 未检出 SKILL.md 变更（无需 AB 状态块）

### 📄 需求状态
- 已配置 | PRD: `prd-aria-v1.md`（active）、`prd-aria-v2.md`（Approved，归一为 pending）
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

### 🏗️ 架构状态
- `docs/architecture/system-architecture.md` 存在，Active，最后更新 2026-09-02，需求链路完整（v1 + v2 PRD）

### 📋 OpenSpec 状态
- 活跃变更: 8 个（全部 approved）| 已归档: 146 | 待归档: 0
- ⚠️ 设计未实施 5 个: `aria-2.0-m6-release-closeout`（124 天）、`aria-2.0-m7-agent-lifecycle`（100 天）、`aria-2.0-m6-cost-model-telemetry`（79 天）、`aria-2.0-m6-e2e-resilience`（77 天）、`aria-2.0-m7-fleet-aggregation`（70 天）

### 🛡️ 审计状态
- 审计系统已启用 | 上次审计: `post_planning`，R7 收敛，verdict = PASS（2026-09-24）

### 🔧 自定义检查
- 16 项全部 ✅ OK（0 失败 / 0 跳过）

### 🔄 同步状态
```
当前分支: feature/handoff-multibranch-subdir-path-fidelity (upstream 未配置)
远程引用: 1m 前同步 (fresh)
⚠️ 当前分支无 upstream 配置，无法计算 ahead/behind
   如需配置: git branch --set-upstream-to=origin/feature/handoff-multibranch-subdir-path-fidelity
ℹ️ 非浅克隆、非 detached HEAD、无进行中的 git 操作
子模块 (与远程对比):
  ✅ standards: 同步 (behind 0 / ahead 0)
  ✅ aria: 同步 (behind 0 / ahead 0)
  ✅ aria-orchestrator: 同步
  ⚠️ aria / standards: 工作区 checkout 与主仓记录的 gitlink 不一致 (workdir_vs_tree=true)
     aria:      主仓记录 1cb3872 → 子模块当前 b181678
     standards: 主仓记录 940cb5b → 子模块当前 d86fc91
     即 git status 里的 " M aria" / " M standards"，属于未提交的指针改动
```
提醒：配置 upstream 之后，以后扫描能算出"feature 分支 vs 它自己的远程副本"的 ahead/behind，**但仍然不会告诉你 master 有没有新改动**，那个要用上面的 `rev-list` 命令看。

🌐 多远程一致性
```
✅ 主仓库: 所有远程一致 (origin, github) — 4f91772
✅ standards 子模块: 所有远程一致 (origin, github) — d86fc91
✅ aria 子模块: 所有远程一致 (origin, github) — b181678
✅ aria-orchestrator 子模块: 所有远程一致 (origin, github) — 237045a
✅ gitlink 完整性: 6 组 (remote × 子模块) 全部 ok
overall_parity = true | 无待推送 | 无不可达远程
```

📦 插件依赖: standards 子模块已注册且已初始化 ✅
📝 README: aria 子模块 plugin.json 与 README 版本一致（1.73.3）✅
🔗 Forgejo 配置: ⚠️ 检测到 Forgejo 远程（forgejo.10cg.pub）但缺少本地配置（CLAUDE.local.md），可运行 `/forgejo-sync` 引导创建（需确认）

### 🎫 Open Issues
- open 49 个（其中 bug 标签 4 个），最新几条: #221 secret-guard 进程列举旁路 / #220 latest.md History prepend 无机械核验 / #219 只读机读进度接口 / #218 state-scanner handoff 无指针时按 mtime 判最新

### 交接状态（handoff awareness）
- 最新 handoff: `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md`（经 latest.md 指针定位，约 60 小时前）；无其他 worktree 的更新交接
- 多终端: `tracks_multibranch.collision.kind = self_multi_container`（simonfish 与 aria-runner-bot 在同一身份键上都有轨道）。这只在你确认进入 Phase B 时才需要走认领闸，本次只是查同步状态，不触发。若进入 Phase B，编排层会执行（本次未执行）：
  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
    --raw-track-id "<handoff §6 选定的 carry-id>" --phase B --mode advisory --repo-path "/home/dev/Aria"
  ```
  若本会话持有 active claim，每次扫描入口还应刷一次心跳（本次未执行）：
  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
    --heartbeat-only --raw-track-id "<carry-id>" --phase A.1 --repo-path "/home/dev/Aria"
  ```

### 🎯 推荐工作流

**[1] 先核实与 master 的差距，按需 merge（推荐）**
- 步骤:
  1. `git rev-list --left-right --count origin/master...HEAD`（只读）
  2. 左边数字 > 0 时：先处理 `aria` / `standards` 两个未提交的子模块指针（提交或还原），再 `git merge origin/master`
  3. 合并后跑一遍 `/state-scanner` 复核多远程一致性，再按项目约束双推（`git push origin && git push github`）并逐个 `git ls-remote` 核对 SHA
- 跳过: `git pull`（无 upstream 且拉不到 master）、rebase（分支已推到两个远程，改写历史需双远程 force push）
- 理由: scan 已确认 feature 分支自身无远程新提交、非浅克隆、非 detached，唯一没覆盖的就是 master 维度

**[2] 给当前分支配置 upstream**
- `git branch --set-upstream-to=origin/feature/handoff-multibranch-subdir-path-fidelity`
- 作用: 以后扫描能自动算出 feature 分支 vs 它远程副本的 ahead/behind；不解决 master 维度的问题

**[3] 暂不同步，继续当前 #195 工作**
- 适合: 你打算在提 PR 前再统一合 master；代价是越晚合，冲突面越大

**[4] 自定义组合**
- 例如 [1] + [2] 一起做

我没有替你执行任何 git 操作（merge / pull / set-upstream 都需要你确认后自己跑或让我执行）。
