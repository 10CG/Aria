先说结论: **本轮扫描没有发现任何 remote 处于 `behind` / `diverged` / `ahead`，也没有 orphaned gitlink —— 也就是说，当前四个仓的「当前分支」不需要补推。** 但有三条不能被「一切正常」四个字盖过去的东西，我放在下面的 §同步状态 和 §直接回答 里逐条点名。

扫描不是靠 `git push` 的回执做的（那正是 2026-04-12 事故里骗人的那个信号）—— scan.py 先对每个 (仓, remote) 腿做 `fetch --prune`，再拿本地 HEAD 与 remote-tracking ref 逐对比较，并对每条腿标注证据新鲜度。`Everything up-to-date` 这类 push 回执从头到尾没有进入判据。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

Step 0 机械采集: `scan.py --output .../outputs/state-snapshot.json` → **exit 0**（全部采集成功，`errors[] = []`），`snapshot_schema_version = "1.0"`（与 SKILL.md 契约一致），`generated_at = 2026-09-05T23:36:46Z`。
阶段 0 中断检测: `.aria/workflow-state.json` 存在但 `status = completed`（2026-09-02 那个 `linked-issue-field-availability` 周期，停在 D.4），`branch_anchor_match = false`（锚定 `master`，当前在 feature 分支）—— 非 `in_progress`/`suspended`/`failed`，不触发 Resume/Abandon 分支，直接进阶段 2。

---

## 📍 当前状态

```
  分支: feature/a1-entry-claim-duplicate-work-guard @ 5d9b568
  模块: — (UPM 未配置, 无 active_module)
  Phase/Cycle: — (UPM 未配置; 上一周期 workflow-state 已 completed)
  变更: 4 个 (0 staged / 3 unstaged / 1 untracked)
        unstaged: aria, aria-orchestrator, standards  ← 三个 dirty 子模块指针
        untracked: aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/
  OpenSpec: a1-entry-claim-duplicate-work-guard (approved)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (1.0h ago, via pointer, status=active, phase=B.2, 31/40)
```

---

## 📊 变更分析

```
  类型: other × 4 (code 0 / test 0 / docs 0 / config 0)
  复杂度: Level 2
  架构影响: 无
  测试覆盖: ❌ 无对应测试 (本次变更是子模块指针 + 未跟踪目录, 无代码面)
  Skill 变更: 未检出 SKILL.md 变更 → 不触发 Rule #6 AB 区块
```

> 三个子模块的 dirty 是**有意**的（handoff §0 第 1 条：gitlink bump 归 TASK-038/8.2，要等各自合 master 之后），不要 `git add`。

---

## 📄 需求状态

```
  配置状态: ✅ 已配置
  PRD: prd-aria-v1.md (active)
       prd-aria-v2.md (pending — raw "Approved (Draft → Approved 2026-04-11, 讨论组+挑战组 4 轮收敛)")
  User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
    优先项 (priority_items): US-026 (in_progress) · US-007 (in_progress) · US-003 (pending)
```

---

## 🏗️ 架构状态

```
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02
  需求链路: ✅ 完整 (parent_prds = prd-aria-v1.md + prd-aria-v2.md)
```

---

## 📋 OpenSpec 状态

```
  活跃变更: 7 个 (approved: 7)
    a1-entry-claim-duplicate-work-guard        ← 本轨, 31/40
    aria-2.0-m6-cost-model-telemetry
    aria-2.0-m6-dispatch-input-delivery
    aria-2.0-m6-e2e-resilience
    aria-2.0-m6-release-closeout
    aria-2.0-m7-agent-lifecycle
    aria-2.0-m7-fleet-aggregation
  已归档: 142 个
  待归档: 0 个
  设计未实施: ⚠️ 5 个 (design_deferred — 设计定稿但实施未做, 勿误判完成)
    - aria-2.0-m6-release-closeout   (approved, 41/41 未勾, staleness 103d)
    - aria-2.0-m7-agent-lifecycle    (approved, 18/18 未勾, staleness 65d)
    - aria-2.0-m6-cost-model-telemetry (approved, 25/38 未勾, staleness 58d)
    - aria-2.0-m6-e2e-resilience     (approved, 25/40 未勾, staleness 55d)
    - aria-2.0-m7-fleet-aggregation  (approved, 20/20 未勾, staleness 48d)
```

---

## 🛡️ 审计状态

```
  审计系统: ✅ 已启用 (convergence 模式, max_rounds 5)
  活跃检查点: post_spec, post_planning  (其余 5 个 off)
  上次审计: pre_merge — PASS (2026-09-02T18:10Z), ⚠️ converged = false
            .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-linked-issue-field-availability-aggregated.md
            (R5 4/4 PASS 但全集未稳定, max_rounds 耗尽 — 降级三选一仍待 owner)
```

---

## 🔧 自定义检查

```
  ✅ 14/14 OK (0 FAIL / 0 STALE / 0 SKIP)
     含 m6-version-badge-match (badge=1.69.1) · plugin-version-arch-docs-match (2 行匹配)
        i18n-readme-translation-currency (3 语种 @1.69.1) · claude-md-changelog-free
        coordination-gate-invocation (近期 7 次真实 run_gate 生产调用)
```

---

## 🔄 同步状态

```
  当前分支: feature/a1-entry-claim-duplicate-work-guard
            (最新, 与 origin/feature/a1-entry-claim-duplicate-work-guard 同步 — ahead 0 / behind 0)
  远程引用: 1m 前同步 (本轮 8 条 fetch 腿, 7 成 1 败)
  ⚠️ has_unreachable_remote = true — 主仓 → github 本轮 fetch 失败 (error_kind = network)
     该腿证据来自上一代 (generation 118 vs 本轮 119), fetched_at = 23:35:34Z (约 72s 前),
     落在 1h 证据窗内 ⇒ evidence_grade 仍判 fresh, 不阻断; 但「本轮没有亲自验证过」是事实。
  子模块 (Phase 1.12 drift):
    ✅ standards        : 与远程同步 (tree == remote = cc864ee)
    ✅ aria             : 与远程同步 (tree == remote = 7dd0135)
    ✅ aria-orchestrator: 与远程同步 (tree == remote = 237045a)
    ℹ️ 三者 workdir_vs_tree = true (工作区 checkout 与主仓记录的 gitlink 不同) — 有意, 见上
```

### 🌐 多远程一致性

```
  enforced remotes: origin, github  (excluded_read_only: 无)

  ✅ 主仓库 (.)            @ 5d9b568
       origin = 5d9b568  equal / fresh / fetch_ok=true
       github = 5d9b568  equal / fresh / fetch_ok=FALSE ← 本轮 fetch 失败, 结论基于上一代 ref
  ✅ aria 子模块            @ ab3dbd0   origin equal / github equal  (均 fresh, fetch_ok=true)
  ✅ standards 子模块       @ bb5d375   origin equal / github equal  (均 fresh, fetch_ok=true)
  ❓ aria-orchestrator 子模块 @ 92acce5 (分支 feature/m6-cost-model-telemetry)
       origin = 92acce5  equal / fresh
       github = —        unknown, reason = no_local_tracking_ref (github 上没有这个分支)

  gitlink 完整性 (Phase 2A, 6 对 = 2 remote × 3 子模块): ✅ 6/6 = ok
       — 主仓在 origin / github 上已发布的 commit 所引用的子模块 gitlink,
         在各自子模块的同名 remote 上全部可达 ⇒ 不存在 orphaned gitlink,
         从任一 remote `clone --recursive` 都不会断裂。

  裁决: overall_parity = TRUE · has_pending_push = FALSE · has_unreachable_remote = TRUE
```

### 📝 README 版本一致性

```
  ✅ aria 子模块版本号: 一致 (plugin.json 1.69.1 = aria/README 1.69.1)
  ℹ️ root README: 存在, 未解析出版本号 (version=null) — 由 custom check m6-version-badge-match 兜住 (OK, badge=1.69.1)
```

### 📦 插件依赖

```
  ✅ standards 子模块: 已注册 + 已初始化
```

### 🔗 Forgejo 配置检查

```
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但 CLAUDE.local.md 缺少 forgejo 配置块
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

---

## 🎫 Open Issues

```
  平台: Forgejo — 47 open (数据来源: cache, 23:35:52Z 取, ttl 15m)
    10CG/Aria              20 open
    10CG/aria-plugin       20 open
    10CG/aria-standards     5 open
    10CG/aria-orchestrator  2 open
  与本次提问直接相关:
    📌 Aria#165 [reliability] GitHub 镜像漏推第三次复发 — 子模块服务端合并 + gitlink bump 无序
               → orphaned gitlink (clone --recursive 断裂)          ← 就是你要复现的那一类
    📌 Aria#176 [bug][state-scanner] AC-5 一致性检测未排除本仓不存在的 remote
               — 单 remote 主仓 + 双 remote 子模块布局下退出码恒为 10
  ⚠️ 计数存疑: config `limit = 20`, 而 Aria 与 aria-plugin 恰好各报 20 = 顶到上限且无截断标记
     (handoff §2 M2 实测: 四仓真实合计 65)。上面的 47 是下界, 不是真值。
```

---

## 🔎 直接回答: 哪些 remote 需要补推

**严格按本轮证据: 一个都不需要。** 没有任何 (仓, remote) 对落在 `behind` / `diverged`，`has_pending_push = false`，`gitlink_integrity` 6/6 `ok`。你要复现的 2026-04-12 形态（Forgejo 合并成功 + 本地已同步 Forgejo + GitHub mirror 落后 ⇒ 主仓 bump gitlink 后产生 orphaned gitlink）**当前不存在**。

但「不需要补推」这句话有三条边界，我不打算用一个绿勾把它们盖掉：

**【1】主仓 → github 这条腿本轮 fetch 失败了，它的 `equal` 是上一代证据。**
`remote_refresh` 里主仓 github 腿 `fetch_ok = "false"`（`error_kind = network`，`generation_fetched = 118` vs 本轮 `scan_generation = 119`，`consecutive_unverified = 1`）。它之所以还判 `parity = equal / evidence_grade = fresh`，是因为上一代成功 fetch 的时间戳（23:35:34Z）距今约 72 秒，落在 1h 证据窗内。这**不是**假绿：机制是 fail-CLOSED 的 —— 若这条腿继续失败，`fetched_at` 一旦跌出证据窗就降到 `stale_unverified`，再跌出豁免窗（代际 > k_eff 或墙钟 > 7d）就变 `expired`，届时 `_apply_freshness_downgrade` 会把 `equal` 改写成 `unknown / not_refreshed`，`overall_parity` 随之转 `false`。但就此刻而言，诚实的说法是「主仓 github 侧比对用的是 72 秒前的 ref，本轮没亲自核过」。想要一个本轮亲验的结论，重跑一次 `/state-scanner`（网络恢复后那条腿会回到 generation 119）。

**【2】aria-orchestrator 的 `feature/m6-cost-model-telemetry` 在 github 上根本不存在。**
`parity = unknown, reason = no_local_tracking_ref, remote_head = null`，而这条腿本轮 fetch 是**成功**的（23:37:14Z，fresh）—— 也就是说，刚拉过一遍，github 上确实没有这个分支的 ref。按 v9 六路分派，`no_local_tracking_ref + evidence_grade == fresh` 归 **benign unknown**（零证据不当负证据），所以 `multi_remote_drift` (1.35) 与 `has_unpublished_branch` (1.36) 都不触发，规则层不给方向性建议。

我这里补一句规则层不会说的话：这条分支属于**另一条轨**（M6 遥测轨，handoff §7 明确写着「另一轨，本 session 未动」），它没推 github 大概率是有意的，不是漏推。若你确实要让 GitHub mirror 也带上它：

```bash
git -C aria-orchestrator push -u github feature/m6-cost-model-telemetry
git ls-remote github refs/heads/feature/m6-cost-model-telemetry   # 逐 remote 核验, 不信 push 回执
```

**【3】最要紧的一条 —— 本轮扫描根本没覆盖 `master`。**
`multi_remote` 比对的是**每个仓当前 checkout 的那条分支**，而现在四个仓全在 feature 分支上（主仓 / aria / standards 在 `feature/a1-entry-claim-duplicate-work-guard`，aria-orchestrator 在 `feature/m6-cost-model-telemetry`）。**没有任何一个仓在 master 上。** 而你要复现的 2026-04-12 事件恰恰是 **master↔master 的镜像漂移**。所以对「aria 的 master 在 github 上是不是落后 Forgejo」这个问题，本次 scan 给不出答案 —— 它既没说是，也没说不是，它压根没看。

这是本次扫描相对该场景的**真实覆盖缺口**，也正好是 Aria#176 那条 issue 的邻近形状。要闭合它，按 CLAUDE.md 多远程硬约束 2（推后逐个 `ls-remote` 核验，不信 push 回执）显式核一遍：

```bash
# 主仓
git rev-parse master; git ls-remote origin master; git ls-remote github master
# 三个子模块同法
for s in aria standards aria-orchestrator; do
  echo "== $s"; git -C $s rev-parse master
  git -C $s ls-remote origin master; git -C $s ls-remote github master
done
```

三个 SHA 全部一致才算 master 层真的同步；任一 remote 缺失或落后，就是需要补推的那个。`ls-remote` 自身失败要重试几次再下结论。

**顺带一条已被机制盖住的**：2026-04-12 那次真正致命的不是「github 落后」本身，而是主仓 bump gitlink 之后产生的 orphaned gitlink。这一层现在有 `gitlink_integrity[]` 逐 (remote, 子模块) 对覆盖，本轮 6/6 `ok`、`consecutive_unverified` 全 0，`orphaned` 会恒阻断 `overall_parity`。所以即便 github 真落后，只要它落后到 gitlink 不可达的程度，`overall_parity` 会直接翻 `false`，不会静默通过。

---

## 🎯 推荐工作流

```
  ➤ [1] verify-remote-parity (推荐)
        执行: 对 master 逐 remote ls-remote 核验 (上面 §3 的命令) → 重跑 /state-scanner
              让主仓 github 腿拿到本轮新鲜证据
        理由: 你问的是「哪些 remote 需要补推」, 而本轮扫描只覆盖了 feature 分支 +
              主仓 github 腿本轮 fetch 失败。这两个缺口不补, 「不需要补推」这个结论
              就只在当前分支、且带一代旧证据的前提下成立。
        置信度: 高 — 只读核验, 零副作用, 直接把结论从「大概率」抬到「已验证」

  ○ [2] continue-cycle — 续做 a1-entry-claim-duplicate-work-guard (31/40)
        执行: H1 Rule #6 AB (7.1/7.2/7.4 + 7.3·7.5 后半) → H2 (7.6, 依赖解除后) → H3 Group 8 发版 (8.1 → 8.4 → 8.2, vNEXT = 1.70.0)
        ⛔ 前置未满足: handoff §3 第 1 条 —— `ARIA_COORDINATION_NO_PUSH` 实测 UNSET,
           这是**会话级**前置, 会话内 export 补不上 (只影响单个 Bash 子进程, 改不了 subagent
           继承环境)。须 owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话。
           这不是 Rule #6 豁免, 是执行条件不具备。
        规则依据: feature_with_spec (优先级 3, 88%) + handoff §6 第 1 项

  ○ [3] cleanup-advisories — 清本轮亮起的三条降级项
        执行: forgejo_config_missing (1.45) 跑 /forgejo-sync 补 CLAUDE.local.md
              audit_unconverged (1.9) 处置 2026-09-02 pre_merge converged=false 的三选一
              resume_in_progress_us (1.88) US-026 / US-007 仍 in_progress
        理由: 都非阻塞, 但都会在每次扫描持续亮

  ○ [4] 自定义组合
        输入格式: "B.2 + C.1" 或 "Phase B"

🤔 选择 [1-4] 或输入自定义:
```

> **进 Phase B 前会先过闸门**: `tracks_multibranch.collision.kind = self_multi_container`
> （group: `dev-claude` ↔ `simonfishgit/dev-claude`，即 Aria#193 那条同容器身份漂移），且
> `coordination.enabled = true` ⇒ 若你选了会进 Phase B 的选项，我会先按契约调 `phase1_gate.py
> --raw-track-id a1-entry-claim-duplicate-work-guard --phase B --mode advisory` 并把 surface
> 告警渲染出来。本次只做扫描 + 回答同步问题，**未调用** run_gate。
> 另注 handoff §3 第 1 条：AB 会话期间不要做真实 heartbeat / acquire —— 跑完清理用的
> `+refs/aria/coordination` 强制 fetch 会连本地未推的真 claim 一起抹掉。本轨 sweep 死线
> `2026-09-06T21:40Z`，时间充裕，不必抢。
