已跑完 Step 0 机械扫描 (`scan.py`, **exit=0**, `errors=[]`, schema 1.0), 下面是完整状态报告。你点名关心的**文档版本一致性**在第 8 区块展开, 并单列了一条「未被机械覆盖的维度」。

---

## 📍 当前状态

```
分支: feature/a1-entry-claim-duplicate-work-guard (upstream origin/同名, 0 ahead / 0 behind)
模块: — (UPM 未配置, active_module=null)
Phase·Cycle: OpenSpec `a1-entry-claim-duplicate-work-guard` 进行中 (31/40, 见交接)
变更文件: 4 个 (未暂存 3 + 未跟踪 1)
  未暂存: aria, aria-orchestrator, standards  ← 三个子模块指针 dirty
  未跟踪: aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/
关联 OpenSpec: a1-entry-claim-duplicate-work-guard (approved)
上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
             (0.94h ago, via pointer)
git 操作中断: 无 (operation=none, has_conflicts=false)
工作流中断: 无需恢复 — `.aria/workflow-state.json` 的 status=completed
           (2026-09-02 收尾的 linked-issue-field cycle; git_anchor.branch=master 与当前分支不匹配, 属陈旧残留)
```

## 📊 变更分析

```
变更类型: other ×4 (code 0 / test 0 / docs 0 / config 0)
复杂度: Level 2
架构影响: 否
测试覆盖: 否 (本次工作区无测试文件变更)
```

> 说明: 三个子模块的 dirty 是**有意保持**的 (交接 §0 第 1 条 — gitlink bump 归 TASK-038/8.2, 要等各子模块合 master 之后), 不要 `git add`。

## 📄 需求状态

```
需求追踪: ✅ 已配置
PRD: 2 份
  - docs/requirements/prd-aria-v1.md — active
  - docs/requirements/prd-aria-v2.md — 归一为 pending ⚠️ (见下方 Status 归一提示)
User Stories: 21 条 — done 17 / in_progress 2 / approved 1 / pending 1
  in_progress: US-007, US-026
  approved: US-028 | pending: US-003
OpenSpec 覆盖: 活跃变更 7 个, 全部 approved
```

⚠️ **Status 归一提示 (与「文档一致性」同族)**: `prd-aria-v2.md` 的原始 Status 是
`Approved (Draft → Approved 2026-04-11, 讨论组+挑战组 4 轮收敛)`, 但被归一成 **pending** ——
括号里的叙述含 `Draft` token, 造成 substring shadow。这是 status-field-guide 明写的 anti-pattern。
建议把叙述移到 em-dash 之后 (`Approved — Draft → Approved 2026-04-11, ...`), 首段截断规则就会
正确归到 `approved`。目前它没有触发 `prd_draft_blocking` 规则 (未满足 ≥5 Story 条件), 属**读数失真**而非阻断。

## 🏗️ 架构状态

```
System Architecture: ✅ 存在
路径: docs/architecture/system-architecture.md
状态: Active | 最后更新: 2026-09-02 (自定义检查测得 age=3d, OK)
需求链路: ✅ 完整 (PRD v1 + PRD v2 → Architecture)
```

## 📋 OpenSpec 状态

```
活跃变更: 7 个 (approved 7)
  a1-entry-claim-duplicate-work-guard   ← 本轨
  aria-2.0-m6-cost-model-telemetry
  aria-2.0-m6-dispatch-input-delivery
  aria-2.0-m6-e2e-resilience
  aria-2.0-m6-release-closeout
  aria-2.0-m7-agent-lifecycle
  aria-2.0-m7-fleet-aggregation
已归档: 142 个 | 待归档: 0 个
```

⚠️ **设计未实施 (design_deferred) — 5 个**:

| id | status | 未勾任务 | staleness |
|----|--------|---------|-----------|
| aria-2.0-m6-release-closeout | approved | 41/41 | **103 天** |
| aria-2.0-m7-agent-lifecycle | approved | 18/18 | 65 天 |
| aria-2.0-m6-cost-model-telemetry | approved | 25/38 | 58 天 |
| aria-2.0-m6-e2e-resilience | approved | 25/40 | 55 天 |
| aria-2.0-m7-fleet-aggregation | approved | 20/20 | 48 天 |

## 🛡️ 审计状态

```
审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
活跃检查点: post_spec, post_planning (其余 off)
上次审计: pre_merge — PASS, 但 converged=false (2026-09-02T18:10:11Z)
  报告: .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-linked-issue-field-availability-aggregated.md
```

⚠️ `verdict=PASS` 而 `converged=false` = R5 用尽 max_rounds 全集仍未稳定, 交接记为「降级三选一待 owner (H1b)」——
这条**尚未闭环**, 触发 `audit_unconverged` 降级提示 (priority 1.9)。

## 🔧 自定义检查

**14 项全过 (0 FAIL / 0 STALE)**, 其中 7 项直接就是版本/文档一致性守卫:

```
✅ m6-version-badge-match            OK badge=1.69.1
✅ i18n-readme-translation-currency  OK (3 份 i18n README 均 @ 1.69.1)
✅ plugin-version-arch-docs-match    OK plugin=1.69.1 (2 处架构文档版本行匹配)
✅ main-project-version-consistency  OK 主项目版本 1.7.5 — 9 个引用点全部一致
✅ m6-claude-md-version              OK version=2.0.0
✅ plugin-cache-currency             OK installed=1.69.1 (scope=user) sot=1.69.1
✅ m6-arch-doc-stale                 OK age=3d
✅ claude-md-changelog-free          OK (无滚动 changelog; 151 行 / 13316 字节)
✅ config-template-key-currency      OK (10 键, 0 deprecated, 0 unknown)
✅ linked-issue-field-availability   OK (7 份在范围内, 6 条在册)
✅ coordination-gate-invocation      OK (近期 7 次生产 run_gate 调用)
✅ issue-cache-freshness             OK
✅ forgejo-app-token-liveness        OK (2 枚应用级 token 活性正常)
✅ silknode-contract-deferral-expiry OK (superseded_by_split)
```

## 🔄 同步状态

```
当前分支: 0 ahead / 0 behind origin/feature/a1-entry-claim-duplicate-work-guard (evidence_grade=fresh)
多远程 parity: ✅ overall_parity=true (enforced: origin + github)
  主仓        5d9b568 → origin ✅ equal / github ✅ equal
  aria        ab3dbd0 → origin ✅ equal / github ✅ equal
  standards   bb5d375 → origin ✅ equal / github ✅ equal
  aria-orchestrator 92acce5 (分支 feature/m6-cost-model-telemetry)
              → origin ✅ equal / github ⓘ unknown (reason=no_local_tracking_ref, evidence_grade=fresh)
gitlink 完整性: 6/6 (R,S) 全 ok — 无 orphaned / 无 orphan_unverified
新鲜度: Phase 0.5 remote_refresh 8 条 leg 全部 fetch_ok, 0 skipped ⇒ 全部证据为 fresh
子模块 drift: 三个都是 workdir_vs_tree=true / tree_vs_remote=false ⇒ 只是工作区指针未 bump, 不是落后远端
```

ⓘ aria-orchestrator 在 github 上的 `unknown` 是 benign: 该分支属另一条在飞的轨 (m6-cost-model-telemetry),
本地无对应 tracking ref。`evidence_grade=fresh` ⇒ **不**触发 `has_unpublished_branch` (1.36, 要求非 fresh),
也不触发 `multi_remote_drift` (1.35, `overall_parity` 为 true)。

### 📝 README / 文档版本一致性 (你点名关心的部分)

**结论: 已被机械覆盖的版本维度全部一致, 但「日期」维度目前没有任何机械覆盖。**

一致的部分:

```
✅ 子模块版本号: 一致 — aria/.claude-plugin/plugin.json = 1.69.1, aria/README = 1.69.1 (version_match=true)
✅ 根 README Plugin badge: 一致 — badge=1.69.1, 与 plugin.json SOT 相同
✅ i18n README (3 份): 正文与 1.69.1 同步, translated-from 标记当前
✅ 架构文档版本行: system-architecture.md §2.8 + version-scheme.md 两行 = plugin 1.69.1
✅ 主项目版本: VERSION = 1.7.5, 9 个引用点 (含 root README badge / 架构文档等) 全部一致
✅ CLAUDE.md 版本头: 2.0.0
✅ 已装插件副本: installed 1.69.1 = SOT 1.69.1 (无缓存陈旧)
```

需要你知道的两个**读数边界** (不是故障, 是覆盖面问题):

```
ⓘ readme.root.version = null
   根 README.md 顶部没有可解析的 `**版本**:` / `## Version:` 行 —— 它的版本是由徽章承载的。
   所以「主项目版本号一致性」不是由 readme collector 给出的, 而是由自定义检查
   m6-version-badge-match (badge vs plugin.json) + main-project-version-consistency
   (VERSION vs 9 个引用点) 两条一起兜住的。两条都 OK ⇒ 版本维度是真绿, 不是"没测到所以绿"。

⚠️ 「文档日期一致性」当前零覆盖
   output-formats 定义的 README 日期检查, 其**期望值来源是 CHANGELOG.md 顶部条目的日期**
   (格式: `期望: <date> (来源: CHANGELOG.md)` vs README 的「最后更新」)。
   但 snapshot schema 1.0 的 `readme` 字段只有 root.version + submodules.aria.{readme_version,
   plugin_version, version_match} —— **没有 date 维度**, 14 条自定义检查里也没有一条比对
   README 日期 vs aria/CHANGELOG.md 日期 (m6-arch-doc-stale 只管架构文档自身的 age, 不做跨文件比对)。
   ⇒ 现在说「日期一致」是没有证据的; 我按「零证据不算正证据」如实报为**未核实**。
   建议: 在 .aria/state-checks.yaml 加一条检查, 以 aria/CHANGELOG.md 最新条目日期为期望源,
   比对 aria/README.md 与根 README.md 的「最后更新 / Last Updated」。
```

发版视角的一句提醒: 交接 §6 写明 `<vNEXT> = 1.70.0`。现在这套「处处 1.69.1」是**已 ship 态的一致**;
一旦进 Group 8 发版 (执行序 8.1 → 8.4 → 8.2), 需要同步的是 aria 子模块 5 文件 + 主仓 16 个版本点 + gitlink,
届时上面这 7 条检查会同时变红, 属预期。

### 📦 插件依赖状态

```
standards 子模块: ✅ 正常 (registered=true, initialized=true)
```

### 🔗 Forgejo 配置检查

```
⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md 配置块 (config_status=missing)
   建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

### 🤝 多终端协调 (advisory)

```
扫描分支 10 条 | 轨道 998 条 → 去重后 121 (legacy 224)
collision.kind = self_multi_container
  分组: ["dev-claude", "simonfishgit/dev-claude"]  ← 同一容器的两种 owner-container 写法并存
```

这正是 Aria#193 记录的身份漂移形状 (交接 §0 第 6 条)。`coordination.enabled=true` + `mode=advisory`,
所以 **`phase1_gate` 的认领闸门会在你确认进入 Phase B 时**由编排层调用 (advisory: 放行 + 写推自己的 claim + 返回 surface),
不在本次只读扫描里跑。

**心跳: 本次未执行, 显式声明而非静默跳过。** 本轨确实持 active claim
(`a1-entry-claim-duplicate-work-guard`, 上次刷新 2026-09-05T21:40:06Z, sweep 死线 2026-09-06T21:40Z),
按 A.1 集成本应每次入口刷一次。没跑的原因是交接 §3 第 1 条的成文约束: AB 评测会话全程
`ARIA_COORDINATION_NO_PUSH=1`, 期间任何 claim 写入都只落本地, 而跑完必做的 `+refs/aria/coordination`
强制 fetch 会把本地未推的**真** claim 一并冲掉。正确次序是「跑 AB → 清理 fetch → 之后再刷心跳」。
死线还有 ~22h, 不紧张。需要手动刷时 (注意先 fetch 后写):

```bash
git fetch origin '+refs/aria/coordination:refs/aria/coordination'
python3 -B aria/skills/state-scanner/scripts/phase1_gate.py \
  --raw-track-id "a1-entry-claim-duplicate-work-guard" \
  --phase A.1 --heartbeat-only --repo-path /home/dev/Aria
```

### 🌲 跨 worktree 交接

```
worktree 数: 1 | 其他 worktree 的更新 handoff: 无 (global_latest_elsewhere=null)
```

## 🎫 Open Issues

```
open_count: 47 (platform=forgejo, source=cache, fetched_at 2026-09-05T23:19:26Z)
  10CG/Aria           20 ⚠️
  10CG/aria-plugin    20 ⚠️
  10CG/aria-standards  5
  10CG/aria-orchestrator 2
label 汇总: bug ×1 | blocker/critical: 0 ⇒ 不触发 open_blocker_issues 降级
近期关键 issue:
  Aria#196  [契约] unattended 的 Layer 1→2 env 传递三腿契约未定义
  Aria#195  [bug] state-scanner handoff_multibranch 只留 basename → 子目录 handoff 必 git show 失败
  Aria#193  同容器 git 身份漂移产生双 owner-container 串 (对应上面的 collision 分组)
  Aria#188  四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md
```

⚠️ **47 这个数字不可信**: config `issue_scan.limit=20`, 而 Aria 与 aria-plugin **恰好各报 20** = 顶到上限,
且 snapshot 无任何截断标记。交接 §2 M2 已实测过同款 (报 46 / 实 65), **至今未开单**。
真实 open 数应显著高于 47。

## 🔬 Skill 变更 AB 状态

```
snapshot: skill_changes.detected = false, modified_skills = []
```

⚠️ 这条**不能读成「本轨没改 Skill, 不用跑 AB」**: 主仓工作区只看得到 `aria` 这个 gitlink 变更,
真正的 `aria/skills/*` 改动已提交在 aria 子模块的同名 feature 分支上, collector 看不进去。
交接 H1 明确写着 **Rule #6 AB 仍未跑, 且仍不是豁免** (本批改了 `allowed-tools` = 能力面扩权, 照跑档),
阻塞在会话级前置 `ARIA_COORDINATION_NO_PUSH` 未设 —— 会话内 `export` 补不上, 只能重启会话。

---

## 🎯 推荐工作流

匹配到的规则 (按优先级): `resume_in_progress_us` (1.88) → `audit_unconverged` (1.9) → `feature_with_spec` (3)。
但按 handoff awareness 契约, 上一 session 的 §6 入口优先于通用规则, 所以主推荐取自那里。

```
➤ [1] 解除 Rule #6 AB 阻塞 (推荐, 置信度 ~85%)
    执行: 退出当前会话 → `ARIA_COORDINATION_NO_PUSH=1 claude --resume`
          → /skill-creator 跑 6 个套件 (phase-a-planner / spec-drafter / state-scanner /
            phase-b-developer / branch-manager / phase-d-closer)
          → 结果落 ab-results/2026-XX-XX-v1.70.0-a1-entry-rule6/<skill>/ (每目录跑前先写 PREDICTION.md)
          → 跑完执行 `git fetch origin +refs/aria/coordination:refs/aria/coordination` 清理合成 claim
          → 之后才刷本轨 heartbeat
    理由: 母 Spec 31/40, 剩余 9 条里 H1(7.x 跑评测) 是唯一的解锁点 —— AB 过关才解除 7.6 (H2) 的
          dependencies, 才轮得到 Group 8 发版 (H3, 执行序 8.1 → 8.4 → 8.2, vNEXT=1.70.0)。
          这是**会话级前置**, 在当前会话里补不上, 不是可以绕开的判断题。
    ⚠️ 验收 env 真进了会话: eval transcript 里 phase1_gate/release_gate 的 JSON 应含
       "push_skipped": true, "push_skipped_reason": "env_var"; 见到 false ⇒ 该 run 作废。

  ○ [2] 补齐「文档日期一致性」这块空白 (doc-update, 置信度 ~70%)
    执行: 在 .aria/state-checks.yaml 增一条检查 — 以 aria/CHANGELOG.md 最新条目日期为期望源,
          比对 aria/README.md 与根 README.md 的「最后更新」; 顺手把 prd-aria-v2.md 的
          Status 叙述移到 em-dash 之后, 消掉 Draft substring shadow。
    理由: 你这次点名问「文档版本是否一致」—— 版本维度 7 条守卫都绿, 唯独日期维度**结构上无人看**。
          这是覆盖面缺口, 不是本次运气好。且两处都不碰 aria 子模块, 不影响 [1] 的 AB 基线。

  ○ [3] 收掉 audit_unconverged 尾巴 (置信度 ~75%)
    执行: 读 pre_merge-R5-...-aggregated.md → 在「接受当前结论 / 再跑一轮 / 降级」三选一里拍板 (H1b)
    理由: 2026-09-02 的 pre_merge 是 PASS 但 converged=false, 至今悬着; 属 owner 决策项。

  ○ [4] 仅查看状态, 不进工作流
    理由: 你只是要一次体检 —— 上面报告即完整结果。
```

`auto_execute_enabled=false` 且 `workflow.auto_proceed=false`, 所以我停在这里等你选。
回复编号即可, 也可以自定义组合 (例如 "先 [2] 再 [1]" —— [2] 不碰 aria 子模块, 不会污染 [1] 的 AB 基线)。

---

### 一句话总结

**版本一致性: 干净。** plugin 1.69.1 / 主项目 1.7.5 两条版本链的全部机械引用点 (badge、i18n README ×3、
架构文档 2 行、VERSION 9 个引用点、CLAUDE.md、已装插件副本) 全部对齐, 14/14 自定义检查通过。
**但请注意两点**: 一是「文档日期」维度**根本没有检查在看**, 现在的绿是"没测", 不是"测过了"
(期望源应是 aria/CHANGELOG.md); 二是 `issue_scan.open_count=47` 因 `limit=20` 被静默截断, 别拿它做判断。
