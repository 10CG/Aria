已按 state-scanner v3.x 机械路径跑完 Step 0 (`scan.py` exit **0**, `errors: []`, snapshot schema `1.0`)。先给结论, 再给全量扫描报告和这次特别关注的多远程判据。

---

## 直接回答: 哪些 remote 需要补推

**当前 checkout 的分支上, 没有任何 remote 需要补推** —— 而且这个"没有"是有新鲜证据支撑的, 不是"push 说 Everything up-to-date"式的静默通过。逐条 SHA:

| 仓 | 分支 | 本地 HEAD | origin | github | 判定 |
|---|---|---|---|---|---|
| 主仓 `.` | `feature/a1-entry-claim-duplicate-work-guard` | `5d9b568` | `5d9b568` | `5d9b568` | equal / equal (证据 fresh) |
| `aria` | 同名 | `ab3dbd0` | `ab3dbd0` | `ab3dbd0` | equal / equal (证据 fresh) |
| `standards` | 同名 | `bb5d375` | `bb5d375` | `bb5d375` | equal / equal (证据 fresh) |
| `aria-orchestrator` | `feature/m6-cost-model-telemetry` | `92acce5` | `92acce5` | (无该分支) | equal / **unknown** (`no_local_tracking_ref`) |

**唯一一处两端不对称**: `aria-orchestrator` 的 `feature/m6-cost-model-telemetry` 在 github 上**根本不存在**(fetch 成功、`--prune` 之后仍无 `refs/remotes/github/feature/m6-cost-model-telemetry`)。

- 按规则 1.35 的第三路 (`parity==unknown ∧ reason==no_local_tracking_ref ∧ evidence_grade==fresh`) 它被归为 **benign unknown**, 不触发补推建议, `overall_parity` 仍为 `true`。我把它**显式点出来而不是吞掉**: 证据新鲜的前提下, "远端没有这条分支"与"这条分支本就不该镜像"当前判据区分不了 —— 这正是 **Aria#176** 在册的形状(上一份 handoff §3 第 6 条也留了同一条实证)。
- 若该轨确实要求 GitHub 镜像, 补推命令是 `git -C aria-orchestrator push github feature/m6-cost-model-telemetry`。**但它属另一条轨** (`aria-2.0-m6-cost-model-telemetry`), 且子模块推送须 owner 逐条授权, 我不代做。

**gitlink 层同样干净**: `gitlink_integrity` 6/6 全 `ok` (2 个 enforced remote × 3 个已声明子模块) —— 主仓已发布 commit 引用的 `aria` / `standards` / `aria-orchestrator` gitlink, 在各子模块的 origin 与 github 两侧都是 branch-reachable。也就是说, 现在从 GitHub `clone --recursive` 不会断。

---

## 为什么这次不会被 "Everything up-to-date" 骗过去

你要复现的 2026-04-12 事件, 失败模式是**拿 push 回执当同步证据**。v3.x 的判据链里 push 回执没有任何投票权:

1. **Phase 0.5 `remote_refresh` 是新鲜度信号的唯一生产者**, 跑在所有 collector 之前, 对每条 (repo, remote) 腿强制 `fetch --prune`。本轮 **8/8 腿 `fetch_ok=true`, `skipped_count=0`**, `fetched_at` 均为 `2026-09-05T23:35:3x`(远程引用 1m 前同步)。`--prune` 是硬前提: 少了它, 被删/被强推的远端分支会留下陈旧 tracking ref, 把 reachability 检查骗成假绿。
2. **parity 只看 fetch 之后的本地 tracking ref** (`method: local_refs`, `refs/remotes/<remote>/<branch>` 逐 remote rev-parse 比对), 不看任何 push 输出。
3. **`equal` 本身不算正证据, 必须 `equal ∧ evidence_grade=="fresh"`** 才满足 `overall_parity` 子句 2。证据过期 (`expired`) 的 `equal` 会被 `_apply_freshness_downgrade` 改写成 `unknown` + `reason: not_refreshed` ⇒ `overall_parity=false` (fail-CLOSED)。"关掉新鲜度信号反而变绿"这条路被不变量堵死: 零证据不得当正证据。
4. **第七路 gitlink 检查** (`gitlink_integrity[]`) 才是你那个事件在主仓 bump 指针之后的正面检测面: 主仓在 R 上已发布 commit 引用的子模块 commit, 若在子模块的 R 上不可达 ⇒ `orphaned` ⇒ **恒阻断** `overall_parity`, 并给出方向正确的修法 `git -C <submodule> push <remote> <branch>`(推子模块, 不是改主仓 gitlink)。

本轮四条判据全绿, 所以结论"无需补推"是**有证据的绿**, 不是"没检查出来"的绿。

---

## 这次扫描答不了的部分 (必须说清楚)

1. **本轮没有测量任何一个仓的 `master`。** parity 比较的 ref 是 `refs/remotes/<remote>/<当前 checkout 分支>` (`collectors/multi_remote.py:365` + `:447`)。现在主仓 / `aria` / `standards` 都在 `feature/a1-entry-claim-duplicate-work-guard`, `aria-orchestrator` 在 `feature/m6-cost-model-telemetry` —— 你复现的那个事件发生在 **master** 上, 本次 snapshot **无法**回答 "`aria/master` 在 github 上是否落后 Forgejo"。
2. **gitlink 检查的"已发布"也是当前分支口径**: `main_branch` 取主仓当前分支 (`multi_remote.py:1368`), 所以核的是 feature 分支尖端那份 gitlink, 不是 master 那份。
3. 想补测 master, 两条路 (我都没代做):
   - 切到 master 后重扫 —— 会动工作树, 需要你确认;
   - 或按 CLAUDE.md 多远程硬约束 2 逐 remote 独立取 SHA 核验(只读, 不信 push 回执):
     ```bash
     for repo in . aria standards aria-orchestrator; do
       for r in origin github; do
         printf '%s %s ' "$repo" "$r"; git -C "$repo" ls-remote "$r" refs/heads/master
       done
     done
     ```
     全部一致才算两端同步; `ls-remote` 自身失败要重试几次再下结论。
4. **三个子模块当前 `workdir_vs_tree=true`**(工作区 HEAD 领先于主仓记录的 gitlink, 即 `git status` 里那三个 dirty 子模块)。这是有意的 —— gitlink bump 归 TASK-038/8.2。因此现在**不存在** "bump 了指针但子模块没推" 的 orphan 风险窗口; 但 8.2 真去 bump 时次序必须是: 先把子模块两端推完并逐个 `ls-remote` 核验, **再** bump 主仓 gitlink(反序就是 2026-07-14 那起 orphaned gitlink 事故)。

---

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/a1-entry-claim-duplicate-work-guard
  模块: — (UPM 未配置)
  Phase/Cycle: B.2 (来源 handoff frontmatter, 非 UPM)
  变更: 4 项 (3 个 dirty 子模块指针 + 1 个未跟踪目录 ab-results/2026-09-05-...)
  OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 31/40)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (1.0h ago, via pointer)

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: 子模块指针 (未提交, 有意保持 dirty) + 未跟踪 AB 结果目录
  复杂度: Level 2
  架构影响: 无
  测试覆盖: 无对应测试 (本次无代码变更)
  Skill 变更: 未检出 (无 SKILL.md 变更 ⇒ 不触发 Rule #6 AB 条件块)

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置
  PRD: prd-aria-v1.md (Active) / prd-aria-v2.md (Approved)
  User Stories: 21 个 (done 17, in_progress 2, approved 1, pending 1)
  OpenSpec 活跃变更: 7 (全部 approved)

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02
  需求链路: ✅ PRD (v1 + v2) → Architecture 完整

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 7 个 (approved: 7)
  已归档: 142 个
  待归档: 0 个
  ⚠️ 设计未实施 (design_deferred): 5 个
     - aria-2.0-m6-cost-model-telemetry (approved, 58d, 25/38 未勾)
     - aria-2.0-m6-e2e-resilience (approved, 55d, 25/40 未勾)
     - aria-2.0-m6-release-closeout (approved, 103d, 41/41 未勾)
     - aria-2.0-m7-agent-lifecycle (approved, 65d, 18/18 未勾)
     - aria-2.0-m7-fleet-aggregation (approved, 48d, 20/20 未勾)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
  活跃检查点: post_spec, post_planning (其余 off)
  上次审计: pre_merge — PASS (2026-09-02, converged=false, R5)

🔧 自定义检查
───────────────────────────────────────────────────────────────
  ✅ 14/14 全部 OK (0 FAIL / 0 STALE), 含与本次问题相关的几条:
     ✅ m6-version-badge-match: badge=1.69.1
     ✅ plugin-version-arch-docs-match: plugin=1.69.1 (2 处架构文档版本行一致)
     ✅ main-project-version-consistency: 1.7.5 — 9 个引用点全部一致
     ✅ i18n-readme-translation-currency: 3 份 i18n README @ 1.69.1
     ✅ coordination-gate-invocation: 近期 7 次生产 run_gate 调用

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/a1-entry-claim-duplicate-work-guard
            (最新, 与 origin/feature/a1-entry-claim-duplicate-work-guard 同步, ahead 0 / behind 0)
  远程引用: 1m 前同步 (Phase 0.5 强制 fetch --prune, 8/8 腿成功, 0 跳过)
  子模块 (工作区 vs 主仓记录的 gitlink):
    ⚠️ standards: 工作区 bb5d375 领先于记录的 cc864ee (指针未提交 — 有意, 归 8.2)
    ⚠️ aria: 工作区 ab3dbd0 领先于记录的 7dd0135 (同上)
    ⚠️ aria-orchestrator: 工作区 92acce5 领先于记录的 237045a (同上)
    (三者 tree_vs_remote 均为 false ⇒ 主仓已记录的那份指针在远端都在)
  📝 README 同步状态: ✅ 子模块版本一致 (plugin.json 1.69.1 = aria/README 1.69.1)
  📦 插件依赖状态: standards 子模块 ✅ 正常 (已注册 + 已初始化)
  🔗 Forgejo 配置检查: ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)

🌐 多远程一致性  (enforced_remotes_resolved = [github, origin], 无 read-only 排除)
───────────────────────────────────────────────────────────────
  ✅ 主仓库: 所有远程一致 (origin, github) — 5d9b568 = 5d9b568, 证据 fresh
  ✅ aria 子模块: 所有远程一致 (origin, github) — ab3dbd0 两端一致, 证据 fresh
  ✅ standards 子模块: 所有远程一致 (origin, github) — bb5d375 两端一致, 证据 fresh
  ❓ aria-orchestrator 子模块: github 上未见该分支的 tracking ref
     当前: origin=92acce5 (equal) | github=unknown (no_local_tracking_ref, 证据 fresh)
     判定: benign unknown (规则 1.35 第三路) — 不阻断 overall_parity, 但按 Aria#176
           这一档"新鲜证据下的缺失分支"当前无法与"本就不该镜像"区分, 故在此点名
  ✅ gitlink 完整性: 6/6 (R × S) = ok — 已发布 gitlink 在两端子模块上均 branch-reachable
  裁决: overall_parity = true | has_pending_push = false | has_unreachable_remote = false

🎫 Open Issues
───────────────────────────────────────────────────────────────
  平台: Forgejo — 47 open (live, 刚刚获取)
    10CG/aria-plugin  20   10CG/Aria  20   10CG/aria-standards  5   10CG/aria-orchestrator  2
  ⚠️ 计数存疑: 两个仓恰好各报 20 = 顶到 config `issue_scan.limit=20` 且无截断标记
     (上一份 handoff §2 M2 已实测复现同一现象: 报 46 vs 实际 65)。真实 open 数应更高。

🧭 会话协调 (tracks_multibranch)
───────────────────────────────────────────────────────────────
  collision.kind = self_multi_container (组: dev-claude / simonfishgit/dev-claude)
  说明: 该 collision 的处置接线点在 **Phase B 入口** (AI 编排层调 phase1_gate advisory 闸门),
        本轮是只读状态扫描, 未进 Phase B ⇒ 未调用 run_gate, 也未做 claim heartbeat。
        若确认进入 Phase B, 按 handoff §3 第 4 条: 先 fetch 协调 ref 再刷 heartbeat (顺序反了会被冲掉)。
  中断状态: workflow-state.json 存在但 status=completed (2026-09-02 那轮 Phase D 已收), 无需 resume。
```

---

## 🎯 推荐工作流

结论是"无需补推", 所以推荐回到本 cycle 主线。以下选项按 handoff §6 的入口优先级排:

**[1] 继续本 cycle 主线: Rule #6 AB (H1)** — 推荐
  - 前置未满足: `ARIA_COORDINATION_NO_PUSH` 仍 UNSET(会话级前置, 会话内 export 补不上, handoff §3 第 1 条已实测)。
  - 处置: 由 owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话后经 `/skill-creator` 跑六个套件; 跑完再执行手册第 3 条的清理 fetch, **之后**才刷本轨 heartbeat。
  - AB 过关 → 7.6 (TASK-036) 依赖解除 → Group 8 发版 (vNEXT = 1.70.0, 执行序 8.1 → 8.4 → 8.2)。

**[2] 把 master 的多远程 parity 补测掉**(直接对应你这次的问题)
  - 只读路径: 上面那段 `ls-remote` 循环, 逐 remote 独立取 SHA 比对;
  - 完整路径: 切 master 后重跑 `/state-scanner`(会动工作树, 需你确认; 且当前三仓 feature 分支在制)。

**[3] 处理 aria-orchestrator 的 github 缺失分支**
  - `git -C aria-orchestrator push github feature/m6-cost-model-telemetry`(需 owner 逐条授权);
  - 或确认该轨不镜像 GitHub, 则维持现状 —— 但建议把这条判据写进 Aria#176 作为又一条实证。

**[4] 自定义组合** — 直接说步骤即可(如 "只核 master" / "B.2 + C.1")。

选哪个?
