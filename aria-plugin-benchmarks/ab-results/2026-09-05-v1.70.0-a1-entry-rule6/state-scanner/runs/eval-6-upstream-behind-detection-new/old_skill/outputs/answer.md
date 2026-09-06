已跑完 Step 0 机械扫描 (`scan.py` exit **0**, `errors: []`, `snapshot_schema_version: 1.0`)，下面先直接回答你问的三件事，再给完整状态报告。

---

## 先回答你的三个问题

**1. 当前分支落后 upstream 吗？→ 相对它自己的 upstream：不落后。相对 master：落后 16 个 commit。**

这两件事在 state-scanner 里是**不同的字段**，而你担心的是后者：

| 比较对象 | 结果 | 来源 |
|---|---|---|
| `feature/a1-entry-claim-duplicate-work-guard` vs `origin/feature/a1-entry-claim-duplicate-work-guard` | ahead 0 / **behind 0** (`evidence_grade: fresh`) | snapshot `sync_status.current_branch` |
| 同一分支 vs `origin/master` | **behind 16 / ahead 13** (merge-base `788fac8`) | 补充实测，snapshot 无此字段 (见下方说明) |

`origin/master` 现在在 `c27826e`（2026-09-05 22:58:34 UTC，也就是**约半小时前**刚被推上去的），你的分支基线还停在 `788fac8`。**你的怀疑是对的：主分支确实有 16 个新 commit 你没拉。**

**2. 需要 `git pull` 吗？→ 需要同步，但不要用 `git pull`。**

在这个分支上直接敲 `git pull`，拉的是它自己的 upstream `origin/feature/a1-entry-...`，而那边 behind = 0 —— 这条命令会是个 **no-op**，一个 commit 都不会进来，你会误以为"已经是最新的"。要把 master 的改动并进来得显式指名：

```bash
# Phase 0.5 已经 fetch 过了，remote-tracking ref 是新鲜的 (23:20 UTC)
git merge origin/master        # 或 git rebase origin/master
```

冲突面我预扫了一下，**很轻**：
- 双方改动文件集的交集只有 **1 个**：`docs/handoff/latest.md`（一行指针文件，冲突后手改即可）
- master 那 16 个 commit **完全没动子模块 gitlink** —— 所以合并不会扰动你那三个"有意保持 dirty"的子模块指针（`aria` / `standards` / `aria-orchestrator`，按上次交接 §0 第 1 条，gitlink bump 归 TASK-038/8.2，现在不要 `git add`）
- master 侧新增的主要是并发轨 `owner-container-identity-key-and-collision-parser` 的 Spec + 40 份审计报告，以及 `aria-2.0-m6-dispatch-input-delivery` 的 tasks/yaml

**⚠️ 顺带抓到一个你没问但更容易踩的坑**：你的**本地 `master` ref 也是陈旧的** —— `master = 788fac8`，落后 `origin/master` **16 个 commit**。`git fetch` 只更新 remote-tracking ref，不会动本地分支。所以千万别 `git checkout master && git merge feature/...` 然后推 —— 那会把已经 ship 的 16 个 commit 从 master 上抹掉。要更新本地 master 用：

```bash
git fetch origin master:master     # 不切分支，直接快进本地 master
```

**3. detached HEAD / shallow clone 场景 → 本仓两个都不是，扫描结果有效。**

- `git.detached_head: false`，`sync_status.current_branch.name` 有值 ⇒ 不是 detached HEAD
- `git.shallow: false` / `sync_status.shallow: false` ⇒ 不是浅克隆
- `current_branch.reason: null` ⇒ **没有触发任何降级**，上面那个 ahead/behind 是实数不是猜测

这两个场景 state-scanner 是**显式处理**的（fail-soft，绝不假装算出了数）：

| 场景 | 字段表现 | 报告里会怎么说 |
|---|---|---|
| detached HEAD | `current_branch.name: null`，`ahead/behind: null`，`reason: "detached_head"` | "upstream 未配置，无法计算 ahead/behind" |
| 浅克隆 | `shallow: true`，`ahead/behind: null`（**覆盖**已算出的值），`reason: "shallow_clone"` | "浅克隆 — 无法计算落后数；如需完整历史 `git fetch --unshallow`" |
| 无 upstream | `upstream: null`，`reason: "no_upstream"` | 提示 `git branch --set-upstream-to=...` |

原则是"**零证据不当正证据**"：这三种情况下 behind 一律置 `null` 并带 `reason`，**不会**因为算不出来就报"已同步"。多远程层同理 —— 新鲜度信号缺失时 `evidence_grade` 落 `expired`，`parity` 会被降级成 `unknown`，`overall_parity` 恒 `false`。

---

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 📍 当前状态

```
  分支: feature/a1-entry-claim-duplicate-work-guard @ 5d9b568
  模块: — (UPM 未配置)
  Phase/Cycle: B.2 (来自 handoff frontmatter，UPM 无 cycle 数据) — 母 Spec 31/40
  变更: 4 个 (3 个 dirty 子模块 + 1 个未跟踪目录)
        未暂存: aria, aria-orchestrator, standards
        未跟踪: aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/
        已暂存: 无
  OpenSpec: a1-entry-claim-duplicate-work-guard (approved)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (0.8h ago, via pointer)
  中断状态: interrupt.status = completed (上一轮 workflow 已收尾，无需 Resume)
            注: git_anchor.branch = master ≠ 当前分支，仅说明那份 state 属于旧周期
```

## 📊 变更分析

```
  类型: 其他 4 (code 0 / test 0 / docs 0 / config 0) — 三个是子模块指针，一个是评测产物目录
  复杂度: Level 2
  架构影响: 无
  测试覆盖: 无对应测试变更
  Skill 变更: 未检出 (skill_changes.detected = false) ⇒ 本次不触发 Rule #6 AB 闸门
```

## 📄 需求状态

```
  配置状态: ✅ 已配置
  PRD:
    - docs/requirements/prd-aria-v1.md (Active)
    - docs/requirements/prd-aria-v2.md (Approved — 归一为 pending)
  User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
  优先项 (priority_items): US-026 (in_progress) · US-007 (in_progress) · US-003 (pending)
  OpenSpec 覆盖率: snapshot 未产出该比值字段 — 不代填
```

## 🏗️ 架构状态

```
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02
  需求链路: ✅ 完整 (parent PRD ×2: prd-aria-v1.md / prd-aria-v2.md, chain_valid = true)
```

## 📋 OpenSpec 状态

```
  活跃变更: 7 个 (approved: 7)
  已归档: 142 个
  待归档: 0 个
  设计未实施: ⚠️ 5 个 (design_deferred)
    - aria-2.0-m6-cost-model-telemetry     (approved, 25/38 未勾, staleness 58d)
    - aria-2.0-m6-e2e-resilience           (approved, 25/40 未勾, staleness 55d)
    - aria-2.0-m6-release-closeout         (approved, 41/41 未勾, staleness 103d)
    - aria-2.0-m7-agent-lifecycle          (approved, 18/18 未勾, staleness 65d)
    - aria-2.0-m7-fleet-aggregation        (approved, 20/20 未勾, staleness 48d)
```

> 📌 与本次同步问题直接相关：`origin/master` 上还有**第 8 个**活跃 Spec —— `owner-container-identity-key-and-collision-parser`（09-05 当天从 A.1 一路跑到 post_planning R2）。它没出现在上面的 7 个里，**正是因为你的分支没拉 master**。

## 🛡️ 审计状态

```
  审计系统: ✅ 已启用 (convergence 模式, max_rounds 5)
  活跃检查点: post_spec, post_planning (其余 5 个 off)
  上次审计: pre_merge — PASS  ⚠️ 未收敛 (converged = false)
    时间: 2026-09-02T18:10:11Z
    报告: .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-linked-issue-field-availability-aggregated.md
  → 命中规则 audit_unconverged (优先级 1.9, 非阻塞)
    说明: 那轮属已 ship 的 linked-issue-field-availability，R5 是 max_rounds 终局而非新问题
```

## 🔧 自定义检查

```
  14 项全部通过 (passed 14 / failed 0 / skipped 0)
  ✅ issue-cache-freshness            ✅ silknode-contract-deferral-expiry
  ✅ m6-version-badge-match (1.69.1)  ✅ m6-claude-md-version (2.0.0)
  ✅ m6-arch-doc-stale (age 3d)       ✅ i18n-readme-translation-currency (3 份 @ 1.69.1)
  ✅ claude-md-changelog-free         ✅ coordination-gate-invocation (7 次生产调用)
  ✅ config-template-key-currency     ✅ plugin-cache-currency (installed=sot=1.69.1)
  ✅ main-project-version-consistency (1.7.5, 9 个引用点一致)
  ✅ forgejo-app-token-liveness       ✅ linked-issue-field-availability
  ✅ plugin-version-arch-docs-match
```

## 🔄 同步状态

```
  当前分支: feature/a1-entry-claim-duplicate-work-guard
    vs origin/feature/a1-entry-claim-duplicate-work-guard: 超前 0 / 落后 0 (evidence_grade: fresh)
    upstream_configured: true | reason: null | diverged: false
    ⚠️ 但 vs origin/master: 落后 16 / 领先 13 —— 见开头，这才是你要的答案

  远程引用: Phase 0.5 本轮已 fetch，8 条腿全部 fetch_ok=true (23:20:08–23:20:13 UTC)
    腿覆盖: (主仓 · standards · aria · aria-orchestrator) × (origin · github)
    skipped 0 | 无 no_matching_remote
    注: sync_status.remote_refs_age = "1m" 是 DEPRECATED 字段 (测的是本轮 scan 自己刚做的
        fetch)，新鲜度判据以 evidence_grade 为准

  分支健康: detached HEAD 否 · shallow 否 · git 中间态 operation=none / has_conflicts=false

  子模块 (工作目录 vs 主仓记录 vs 远程):
    ⚠️ standards          workdir_vs_tree=true  (HEAD bb5d375 ≠ tree cc864ee) · tree_vs_remote=false
    ⚠️ aria               workdir_vs_tree=true  (HEAD ab3dbd0 ≠ tree 7dd0135) · tree_vs_remote=false
    ⚠️ aria-orchestrator  workdir_vs_tree=true  (HEAD 92acce5 ≠ tree 237045a) · tree_vs_remote=false
    三者 behind_count = ahead_count = 0，hint = null ⇒ 不触发 submodule_drift 规则
    这三个 dirty 是上次交接明写的"有意状态"(gitlink bump 归 8.2)，不要 git add
```

### 🌐 多远程一致性

```
  overall_parity: ✅ true   (enforced remotes: origin, github)
  ✅ 主仓库:            origin = github = 5d9b568 (equal, fresh)
  ✅ standards 子模块:  origin = github = bb5d375 (equal, fresh)
  ✅ aria 子模块:       origin = github = ab3dbd0 (equal, fresh)
  ℹ️ aria-orchestrator: origin equal @92acce5 (分支 feature/m6-cost-model-telemetry)
       github → parity=unknown, reason=no_local_tracking_ref, evidence_grade=fresh
       ⇒ 判为 benign unknown（该分支在 github 上还没有 tracking ref，属另一条轨）
         既不触发 multi_remote_drift (1.35) 也不触发 has_unpublished_branch (1.36)
  ✅ gitlink 完整性: 6/6 ok（3 子模块 × 2 remote，无 orphaned / orphan_unverified）
  has_pending_push: false | has_unreachable_remote: false
```

### 📝 README 版本一致性

```
  ✅ aria 子模块: plugin.json 1.69.1 = README 1.69.1
  ℹ️ 根 README: 存在，但未解析出版本号 (readme.root.version = null)
```

### 📦 插件依赖

```
  ✅ standards 子模块: 已注册且已初始化
```

### 🔗 Forgejo 配置检查

```
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但配置缺失 (config_status: missing)
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

## 🎫 Open Issues

```
  平台: Forgejo — 47 open（数据来源: cache，2026-09-05T23:19:26Z 获取，ttl 15m）
  分组: 10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 5 · 10CG/aria-orchestrator 2
  label 汇总: bug ×1 —— 无 blocker / critical ⇒ open_blocker_issues (1.99) 不触发
  近期关键项:
    #196 [契约][aria-orchestrator] unattended 的 Layer 1→2 env 传递三腿契约未定义
    #195 [bug] state-scanner: handoff_multibranch 只留 basename，子目录下的 handoff 必然 git show 失败
    #193 [反馈] 同容器 git 身份漂移产生双 owner-container 串 — collision 分类失灵
    #176 [bug][state-scanner] AC-5 一致性检测未排除本仓不存在的 remote
    #175 [governance] 契约 2 重写 (linked US-025)

  ⚠️ 计数存疑: Aria 与 aria-plugin **各恰好报 20**，而 config limit = 20 ⇒ 大概率顶到上限被
     静默截断，真实 open 数应大于 47（上次交接 §2 M2 已实测过一次：报 46 / 实 65，仍未开单）
```

## 📜 Session Handoff

```
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
  写入时间: 2026-09-05T22:35:22Z (~0.8h ago)
  来源: pointer (docs/handoff/latest.md)
  漂移文件: 无 (misplaced_files = [])
  ✅ 已读取本 doc，§6 next-session 入口已纳入下方推荐

  跨 worktree: 仅 1 个 worktree，全局最新 handoff 就在当前树 ⇒ 无跨树告警
```

**handoff §6 给出的优先级**（优先于通用推荐规则）：
1. ⭐ `a1-entry-claim-duplicate-work-guard` 续做 31/40。**先决条件**：Rule #6 AB 需以 `ARIA_COORDINATION_NO_PUSH=1` **重启会话**才能跑（会话级前置，会话内补不上）。AB 过关 → 7.6 依赖解除 → Group 8 发版（vNEXT = 1.70.0，执行序 8.1 → 8.4 → 8.2）。
2. `carry-issue-scan-open-count-truncation` —— 上面那条 open_count 截断。
3. `carry-resilient-push-non-ff-recovery` —— aria-plugin#169。

**多终端提示**：`tracks_multibranch.collision.kind = self_multi_container`（同一 owner 的两个 container 串 `dev-claude` / `simonfishgit/dev-claude`，即 Aria#193 的身份漂移）。`coordination.enabled = true`，所以不走 rule 1.54 的 advisory，而是**在你确认进入 Phase B 时**由编排层调 `phase1_gate.py --mode advisory` 认领。另有并发轨 `aria-2-0-m6-dispatch-input-delivery`（aria-runner-bot/bfe8285d, B.2）在飞 —— **master 那 16 个 commit 主要就是它和 identity-key 轨推的**。

## 🎯 推荐工作流

> 匹配到的规则（按优先级）：`audit_unconverged` (1.9, 非阻塞) → `resume_in_progress_us` (1.88, 建议) → `feature_with_spec` (3, 88%)。
> `branch_behind_upstream` (1.98) **未命中** —— 它的判据是 `current_branch.behind >= 5`，而那个字段比的是同名 upstream（behind 0）。**这条规则对"落后 base 分支"结构性失明**，所以下面的 [1] 是我根据补充实测手工加的，不是规则引擎给的。

```
  ➤ [1] sync-from-master (推荐)
        执行: git merge origin/master   (或 git rebase origin/master)
              + git fetch origin master:master  (顺手把陈旧的本地 master 快进)
        理由: 分支落后 origin/master 16 commits，其中含并发轨刚 ship 的 Spec；
              文件交集只有 docs/handoff/latest.md 一处，且不动 gitlink，现在合成本最低。
              越往后拖，与 identity-key 轨在 openspec/ 和 .aria/ 下的接触面越大。
        风险: 低。合并后请核对 latest.md 指针指向你这份 2200 的 handoff。

  ○ [2] feature-dev (续 B.2, 不同步)
        执行: B.2 → C.1
        跳过: A.* (Spec 已 approved 且 post_planning R4 CONVERGED)
        理由: 母 Spec 31/40，但 §6 第 1 条的 Rule #6 AB 卡在会话级前置 ——
              需要 owner 用 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话。
              本会话内做不了，硬跑会把合成 claim 推到生产 refs/aria/coordination。

  ○ [3] inspect-only (只看不动)
        执行: git log --oneline HEAD..origin/master
              git diff --stat HEAD...origin/master
        理由: 先摸清那 16 个 commit 的接触面再决定 merge 还是 rebase。

  ○ [4] 自定义组合
        输入格式: "B.2 + C.1" 或 "Phase B"
```

> `auto_execute_enabled = false` 且 `workflow.auto_proceed = false` ⇒ 不会自动执行，等你选。

**🤔 选择 [1-4] 或输入自定义：**

---

### 附：一条值得记下的观察

`sync_status.current_branch.behind` 只对 **configured upstream** 计算。在 feature 分支上，这个值几乎永远是 0（因为你自己刚推过），于是报告显示"✅ 同步"、`overall_parity: true`、`branch_behind_upstream` 不触发 —— 而真正会咬人的"落后 base 分支 16 个 commit"**在整个 snapshot 里没有任何字段承载**。

这跟 Aria#176 是同一族形状（"证据不覆盖的维度被当成正常"）。如果你要开单，判据可以写成：`sync_status` 应增加 per-branch 的 `vs_base_branch` 腿（base 从 upstream 的 remote + 默认分支推出），缺失时按 fail-CLOSED 报 `unknown` 而不是让 `overall_parity` 报 `true`。
