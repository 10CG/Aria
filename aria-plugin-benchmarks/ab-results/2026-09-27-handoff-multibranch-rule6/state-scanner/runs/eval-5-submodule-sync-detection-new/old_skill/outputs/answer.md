# 状态扫描结果: 子模块是否落后远程

**结论先说: 不需要 `git submodule update`, 而且现在不要跑。** 三个子模块都没有落后远程。`aria` 和 `standards` 显示为 `M`, 原因是它们比主仓记录的版本**超前** (本地 feature 分支上有新提交, 已推送), 不是落后。这时候跑 `git submodule update` 会把这两个子模块切回主仓记录的旧 commit (detached HEAD), 等于把你当前的工作位置倒退 2 个和 9 个提交。

扫描方式: `scan.py` 机械采集 (退出码 **0**, `errors[]` 为空), 本轮对 `github` / `origin` 两个远程都做了 fetch。

---

## 📍 当前状态
- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (主仓, 没有配置 upstream)
- HEAD: `4f91772` docs(openspec): 10CG/Aria#195 台账记 owner 2026-09-27 裁定与 feature 双推
- 未提交变更 3 项: `aria` (gitlink 偏移) / `standards` (gitlink 偏移) / `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` (未跟踪)
- 中断状态: 无 (`interrupt.status = none`); git 操作: 无进行中的 rebase/merge
- UPM: 未配置

## 📊 变更分析
- 变更类型: other × 3 (两个 gitlink + 一个 AB 结果目录), 代码/测试 0
- 复杂度: Level 2 | 架构影响: 无 | 未检出 SKILL.md 变更

## 🔄 同步状态 (本次重点)

### 子模块逐个判定

| 子模块 | 本地 checkout (HEAD) | 主仓记录 (gitlink) | 远程默认分支 | 落后远程 | 工作区偏离 gitlink | 判定 |
|---|---|---|---|---|---|---|
| `aria` | `b181678` (feature 分支) | `1cb3872` | `1cb3872` | 0 | 是, **超前 9 个提交** | 不落后; 本地超前 |
| `standards` | `d86fc91` (feature 分支) | `940cb5b` | `940cb5b` | 0 | 是, **超前 2 个提交** | 不落后; 本地超前 |
| `aria-orchestrator` | `237045a` (master) | `237045a` | `237045a` | 0 | 否 | 完全一致 |

- 三个子模块的 `drift.tree_vs_remote` 都是 `false`, `behind_count` 都是 0, `hint` 为空 —— 也就是主仓记录的 gitlink 就等于远程默认分支最新 commit, 远程**没有**比你更新的子模块提交。
- `aria` / `standards` 的 `workdir_vs_tree = true`: 我用只读命令补查了方向 (`git rev-list --count`): gitlink..HEAD 分别为 9 和 2, HEAD..gitlink 均为 0, 说明是**纯超前**, 没有分叉。超前的提交都是本轮 10CG/Aria#195 的工作 (例如 `aria` 的 `b181678 docs(state-scanner): ... TASK-023 ...`, `standards` 的 `d86fc91 docs(conventions): ... session-handoff 第三态回填跟踪 issue 号`)。

### 多远程一致性 (`overall_parity = true`)

| 仓库 | 分支 | github | origin (Forgejo) |
|---|---|---|---|
| 主仓 `.` | feature/handoff-multibranch-subdir-path-fidelity | equal, 本轮 fetch 成功 | equal, **本轮 fetch 失败**, 用 6 分钟前 (16:59) 的数据 |
| `standards` | feature/handoff-multibranch-subdir-path-fidelity | equal, fetch 成功 | equal, **本轮 fetch 失败**, 用 16:59 数据 |
| `aria` | feature/handoff-multibranch-subdir-path-fidelity | equal, fetch 成功 | equal, fetch 成功 |
| `aria-orchestrator` | master | equal, fetch 成功 | equal, fetch 成功 |

- 所有远程的 `evidence_grade` 都是 `fresh` (1 小时新鲜度窗口内), 没有 ahead/behind, `has_pending_push = false` —— 超前的子模块提交已经推到两个远程。
- gitlink 完整性: 3 个子模块 × 2 个远程共 6 对全部 `ok`, 没有 orphaned gitlink (即 GitHub `clone --recursive` 不会断)。
- ⚠️ `has_unreachable_remote = true`: Forgejo `origin` 对主仓和 `standards` 这一轮 fetch 失败 (`error_kind: other`, 连续失败 1 次)。目前靠 6 分钟前的成功 fetch 仍算新鲜证据, 但如果协作者正好在这 6 分钟里往 Forgejo 推了东西, 本轮看不到。建议稍后重跑一次扫描确认。
- 协调 ref 拉取也因同一原因降级 (`coordination_fetch.degraded = true, fetch_failed_using_stale_cache`)。

### 扫描覆盖不到的一个盲区
子模块的「远程」比较的是子模块远程默认分支 (master)。如果协作者的「子模块更新」是指**在主仓 master 上 bump 了 gitlink**, 那要看主仓 master 是否领先你的分支, 而你当前在 feature 分支上、且没配置 upstream, 本次扫描不比较主仓 master。想确认的话可以跑这条只读命令 (我没有替你跑):

```bash
git fetch origin master && git log --oneline HEAD..origin/master -- aria standards aria-orchestrator
```

有输出 = master 上有人改过 gitlink, 那时要做的是把 master 合进/变基到你的分支, 而不是 `git submodule update`。

### 📝 README / 🔗 Forgejo 配置
- `aria` 插件版本 `1.73.3`, README 版本一致
- Forgejo 配置文件缺失 (`config_status: missing`), 可用 `/forgejo-sync` 引导创建

## 📄 需求状态
- PRD: `prd-aria-v1.md` (active) / `prd-aria-v2.md` (Approved, 归一为 pending)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

## 🏗️ 架构状态
- `docs/architecture/system-architecture.md` 存在, Active, 最后更新 2026-09-02, 需求链路完整

## 📋 OpenSpec 状态
- 活跃变更 8 个, 已归档 146 个, 待归档 0 个
- ⚠️ 设计未实施 (design_deferred): `aria-2.0-m6-cost-model-telemetry` (79 天) / `aria-2.0-m6-e2e-resilience` (77 天) / `aria-2.0-m6-release-closeout` (124 天) / `aria-2.0-m7-agent-lifecycle` (100 天) 等

## 🛡️ 审计状态
- 审计系统已启用; 上次审计 `post_planning`, verdict **PASS**, 已收敛 (R7, 2026-09-24)

## 🔧 自定义检查
- 16 项全部 ✅ 通过, 0 项失败

## 🎫 Open Issues
- Forgejo 共 49 个 open issue; 最近的有 #221 (secret-guard 进程表旁路, bug) / #220 (latest.md History prepend 无机械核验) / #218 (state-scanner handoff 无指针时按 mtime 判最新, bug)

## 交接感知
- 最新 handoff (按 pointer): `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md`, 距今约 60 小时
- 当前分支今天的提交都在推进 10CG/Aria#195, 比这份 handoff 更新 —— 进入下一步前建议先读 `docs/handoff/latest.md` 和 #195 的任务台账, 对齐进度
- 多 track 碰撞: `tracks_multibranch.collision.kind = self_multi_container` (同一 owner 在多个容器下有 track: 身份键 `023236f2` / `bfe8285d` 同时出现在 `simonfish` 和 `aria-runner-bot` 下)。按流程, 真正进入 Phase B 前编排层会跑 advisory 认领闸门:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<handoff §6 选定的 carry-id>" --phase B --mode advisory --repo-path "/home/dev/Aria"
```

  本次只是查询同步状态, 没有进 Phase B, 所以**没有执行**这条命令。

---

## 🎯 推荐工作流

**[1] 不做 submodule update, 继续当前 #195 track (推荐)**
- 理由: 远程没有新的子模块提交; `aria`/`standards` 的偏移是你自己的超前提交, 且已双推。
- 步骤: 按 #195 任务台账继续; 到 C.1 提交时把 `aria` / `standards` 的 gitlink bump 一并提交 (`git add aria standards`), 让主仓记录跟上子模块。注意按项目规则: 子模块分支先本地 merge 到子模块 master 并双推, 再在主仓 bump gitlink, 推后逐个 `git ls-remote` 核对 SHA。
- 跳过: 子模块更新。

**[2] 先确认主仓 master 有没有人 bump 过 gitlink, 再决定**
- 步骤: 跑上面那条 `git log HEAD..origin/master -- aria standards aria-orchestrator`; 有输出就把 master 合入/变基当前分支 (会带来 gitlink 冲突, 需要手工选版本), 没输出就回到 [1]。

**[3] 稍后重跑状态扫描**
- 理由: Forgejo `origin` 对主仓和 `standards` 本轮 fetch 失败, 只拿到 6 分钟前的数据。等网络恢复后重跑 `/state-scanner`, 让两个远程都拿到本轮新鲜证据。

**[4] 只是想让子模块跟随远程 master (不推荐, 会丢掉当前工作位置)**
- 命令: `git submodule update --remote aria standards`
- 后果: 两个子模块会切到 master 的 `1cb3872` / `940cb5b` 并进入 detached HEAD, 你在 feature 分支上的 9 + 2 个提交不会丢 (已推送、分支还在), 但工作目录会离开 feature 分支, 后续 #195 工作要重新 `git -C aria checkout feature/...` 才能继续。只有你确认要放弃当前 track 时才选这个。

也可以自定义组合, 例如「[3] + [1]」: 先重跑扫描确认 Forgejo 那一侧, 再继续当前 track。
