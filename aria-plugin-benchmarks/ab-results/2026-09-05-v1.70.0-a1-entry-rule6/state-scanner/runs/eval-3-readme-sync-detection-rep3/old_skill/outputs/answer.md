已跑完机械扫描 (`scan.py`, **exit 0**, `errors[] = []`, snapshot schema 1.0)，并按你的要求把**文档版本一致性**单独拉出来核了一遍。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 📍 当前状态

```
分支:        feature/a1-entry-claim-duplicate-work-guard
             (upstream = origin/同名, ahead 0 / behind 0)
HEAD:        5d9b568 docs(handoff): §3 第 1 条补 AB 会话运行守则 …
模块:        — (UPM 未配置)
Phase/Cycle: B.2 — track a1-entry-claim-duplicate-work-guard (31/40)  [来源: handoff frontmatter]
变更:        4 项 — 3 个 dirty 子模块指针 (aria / aria-orchestrator / standards)
                   + 1 个未跟踪目录 aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/
             暂存区: 空
OpenSpec:    a1-entry-claim-duplicate-work-guard (approved)
上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
             (0.9h ago, via pointer)
中断状态:    workflow-state.json 存在但 status = completed (2026-09-02 收尾), 不需要 Resume/Abandon
git 操作:    none (无暂停中的 rebase/merge/cherry-pick)
```

## 📊 变更分析

```
类型:     其他 (子模块指针 + 未跟踪的 AB 结果目录), 无代码/测试/文档文件变更
复杂度:   Level 2
架构影响: 无
测试覆盖: 无对应测试变更
Skill 变更: 主仓层面未检出 (aria 子模块内的 SKILL.md 变更已提交在子模块分支上, 不在主仓 diff 里)
```

> 三个 dirty 子模块指针是**有意保持**的 (gitlink bump 归 TASK-038 / 8.2, 要等各自合 master 之后)，不要 `git add`。

## 📄 需求状态

```
配置状态:      ✅ 已配置
PRD:           prd-aria-v1.md (active)
               prd-aria-v2.md (raw "Approved (Draft → Approved 2026-04-11 …)" → 归一 pending)
User Stories:  21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
优先项:        US-026 (in_progress) · US-007 (in_progress) · US-003 (pending)
OpenSpec 覆盖: 快照未产出机械覆盖率字段, 此处不臆造
```

## 🏗️ 架构状态

```
System Architecture: ✅ 存在
路径:                docs/architecture/system-architecture.md
状态:                Active
最后更新:            2026-09-02 (3 天前)
需求链路:            ✅ 完整 — parent PRDs = prd-aria-v1.md + prd-aria-v2.md
```

## 📋 OpenSpec 状态

```
活跃变更: 7 个 (全部 approved)
  · a1-entry-claim-duplicate-work-guard        ← 本轨, 31/40
  · aria-2.0-m6-cost-model-telemetry
  · aria-2.0-m6-dispatch-input-delivery
  · aria-2.0-m6-e2e-resilience
  · aria-2.0-m6-release-closeout
  · aria-2.0-m7-agent-lifecycle
  · aria-2.0-m7-fleet-aggregation
已归档:   142 个
待归档:   0 个
⚠️ 设计未实施 (design_deferred): 5 个
  · aria-2.0-m6-release-closeout    approved   41/41 未勾选   staleness 103d
  · aria-2.0-m7-agent-lifecycle     approved   18/18 未勾选   staleness  65d
  · aria-2.0-m6-cost-model-telemetry approved  25/38 未勾选   staleness  58d
  · aria-2.0-m6-e2e-resilience      approved   25/40 未勾选   staleness  55d
  · aria-2.0-m7-fleet-aggregation   approved   20/20 未勾选   staleness  48d
```

## 🛡️ 审计状态

```
审计系统:   ✅ 已启用 (convergence 模式, max_rounds=5)
活跃检查点: post_spec, post_planning (其余 7 个 checkpoint 显式 off)
上次审计:   pre_merge — PASS, 但 converged = false (R5, 2026-09-02T18:10)
            .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-
              linked-issue-field-availability-aggregated.md
```

⚠️ 触发规则 `audit_unconverged` (priority 1.9, 75%)：verdict 是 PASS 但**未标记收敛**。这是上一轮 `linked-issue-field-availability` 遗留的，与本轨无关；如果你已知并接受，可忽略。

## 🔧 自定义检查

```
✅ 14 / 14 通过 (0 FAIL, 0 STALE)

issue-cache-freshness ................. OK
silknode-contract-deferral-expiry ..... OK (status=superseded_by_split, 2 successor ref)
m6-version-badge-match ................ OK badge=1.69.1
m6-claude-md-version .................. OK version=2.0.0
m6-arch-doc-stale ..................... OK age=3d
i18n-readme-translation-currency ...... OK (3 份 i18n README current @ 1.69.1)
claude-md-changelog-free .............. OK (151 行 / 13316 字节, 无滚动 changelog)
coordination-gate-invocation .......... OK (7 次真实生产 run_gate 调用在册)
config-template-key-currency .......... OK (10 keys, 0 deprecated, 0 unknown)
plugin-cache-currency ................. OK installed=1.69.1 (scope=user) sot=1.69.1
main-project-version-consistency ...... OK 主项目 1.7.5 — 9 个引用点全部一致
forgejo-app-token-liveness ............ OK (2 枚应用级 token 活性正常)
linked-issue-field-availability ....... OK (7 份在范围内, 6 条在册)
plugin-version-arch-docs-match ........ OK plugin=1.69.1 (2 arch doc rows match)
```

## 🔄 同步状态

```
当前分支:   ahead 0 / behind 0 vs origin/feature/a1-entry-claim-duplicate-work-guard
远程 refs:  1m 前刷新 (remote_refresh 8 条 leg 全部 fetch_ok, 0 skipped, evidence_grade=fresh)
多远程 parity (enforced: origin + github): ✅ overall_parity = true
  主仓 .                5d9b568   origin ✅ equal   github ✅ equal
  standards             bb5d375   origin ✅ equal   github ✅ equal
  aria                  ab3dbd0   origin ✅ equal   github ✅ equal
  aria-orchestrator     92acce5   origin ✅ equal   github ℹ️ unknown (no_local_tracking_ref)
gitlink 完整性: ✅ 6/6 ok (3 子模块 × 2 remote), 无 orphaned / orphan_unverified
子模块 drift:  tree_vs_remote 全 false; workdir_vs_tree 三处 true = 上面说的有意 dirty
```

> `aria-orchestrator@github` 的 `unknown` 是 `feature/m6-cost-model-telemetry`（另一条轨）在 github 上没有本地 tracking ref；`evidence_grade=fresh` ⇒ 属 benign unknown，既不触发 `multi_remote_drift` (1.35) 也不触发 `has_unpublished_branch` (1.36)。

### 📝 README / 文档版本一致性

```
✅ aria 子模块:  README 1.69.1  ==  .claude-plugin/plugin.json 1.69.1   (version_match=true)
✅ Plugin badge: README.md:8  Plugin-v1.69.1  ==  plugin.json 1.69.1
✅ i18n README:  3 份全部 current @ 1.69.1 (无待重译)
✅ 主项目版本:   1.7.5 — 9 个引用点全部一致
✅ CLAUDE.md:    **版本**: 2.0.0 (符合 Diff 9 期望值)
✅ 架构文档版本行: plugin=1.69.1, 2 处 arch doc 行匹配 (system-architecture.md §2.8 + version-scheme.md)
✅ 插件缓存:     installed 1.69.1 (user scope) == SOT 1.69.1
✅ 架构文档新鲜度: age=3d (未 stale)
ℹ️ 根 README:    readme.root.version = null
```

### 📦 插件依赖状态

```
standards 子模块: ✅ 已注册 + 已初始化
```

### 🔗 Forgejo 配置检查

```
⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但 CLAUDE.local.md 缺少 forgejo 配置 (config_status=missing)
   建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

---

## 🔎 文档版本一致性 — 专项结论 (你点名要看的)

**结论: 当前 8 个机械版本核对点全绿, 未发现任何版本漂移。** 全仓当前收敛在这三个数上：

| 面 | 版本 | 一致性证据 |
|----|------|-----------|
| aria-plugin | **1.69.1** | plugin.json (SOT) = aria/README = 根 README badge = 3 份 i18n README = 2 处架构文档行 = 本机已装插件缓存 |
| 主项目 Aria | **1.7.5** | `main-project-version-consistency` 实测 9 个引用点全一致 |
| aria-orchestrator | **2.0.0** | CLAUDE.md `**版本**: 2.0.0` 与 `m6-claude-md-version` 期望值一致 |

两点需要你知道，但**都不是漂移**：

1. **`readme.root.version = null` 不是不一致，是解析形态问题。** collector 只认 `**版本**: x.y.z` / `## Version: …` / `> **Version**: …` 这三种形态；根 `README.md` 表达版本的方式是 badge (`README.md:8`) 加一个纯文本代码块 (`README.md:241-242` 的 `Project Version: 1.7.5` / `Plugin Version: 1.69.1`)，两种都不在 pattern 里，所以 collector 报 null。真正的判定由 `m6-version-badge-match` + `main-project-version-consistency` 两条自定义检查覆盖，且都是 OK。所以 `readme_outdated` 规则 (priority 1.3) **未触发**，是对的。
2. **一致 ≠ 已发版。** 上一份 handoff §6 写明本轮的 `<vNEXT>` = **1.70.0**，Group 8 发版三条 (8.1 CHANGELOG + 版本 SOT 5 文件 → 8.4 aria 本地 merge + 双推 + tag → 8.2 主仓 16 个版本点 + gitlink bump) 都还没做。也就是说：**现在的"全一致"是 1.69.1 这个旧世界的一致**，一旦开始 8.1，版本同步面会瞬间张开 21+ 个点，那时才是这批检查真正吃力的时候。

---

## 🎫 Open Issues

```
open_count: 47 (platform=forgejo, source=cache, fetched 2026-09-05T23:19:26Z, 无 fetch_error)
按仓分组: 10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 5 · 10CG/aria-orchestrator 2
label 汇总: bug ×1

关键 issue:
  Aria#195   [bug] state-scanner: handoff_multibranch 递归枚举只留 basename → 子目录 handoff 必然 git show 失败
  Aria#196   [契约] unattended 的 Layer 1→2 env 传递三腿契约未定义 (缺 import 静默 fallback false)
  Aria#193   同容器 git 身份漂移产生双 owner-container 串 — collision 分类失灵
  Aria#188   [bug] 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md
  aria-plugin#169  [缺陷][Layer L] resilient_push non-FF 恢复路径结构上必失败
  aria-standards#19 [convention] owner-container 与 claim container 段口径不统一
无 blocker/critical label ⇒ 未触发 open_blocker_issues 规则
```

⚠️ **这个 47 有可能是被截断的**：`issue_scan.limit = 20`，而 Aria 与 aria-plugin **恰好各报 20**（顶到上限），且快照里没有任何截断标记。上一份 handoff 的 M2 项记录了同一现象（报 46 vs 四仓实拉 65），至今未开单。把它当下限看。

---

## 🤝 上一次 handoff (0.9h ago, via pointer)

`docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md`
frontmatter: track `a1-entry-claim-duplicate-work-guard` · owner-container `simonfish/023236f2` · phase **B.2** · status **active**

它写明的续作优先级（**优先于通用推荐规则**）：

- **H1 ⛔ Rule #6 AB 六个套件仍未跑，且明确不是豁免。** 阻塞点是**会话级前置**：`ARIA_COORDINATION_NO_PUSH` 实测 UNSET，会话内 `export` 只影响单个 Bash 子进程，改不了 subagent 继承的环境。必须由你以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启进程才能跑。
- **H2 7.6 (TASK-036) 依赖阻塞**：`dependencies: [TASK-035]`，7.5 未跑完；现在开单等于改序 (Rule #10)。要放行需要你显式说一句。
- **H3 Group 8 发版三条**，gate 在 AB 过关之后，执行序 8.1 → 8.4 → 8.2。

另外两条硬提醒（handoff §3）：
- **AB 会话期间不要做真实 heartbeat / acquire** —— 那期间 `NO_PUSH=1` 使所有 claim 只落本地，而跑完必做的 `+refs/aria/coordination` 强制 fetch 会连真 claim 一起冲掉。正确次序：跑 AB → 清理 fetch → **之后**才刷 heartbeat。
- 本轨 claim heartbeat 最后刷于 `2026-09-05T21:40:06Z`，sweep 死线 **2026-09-06T21:40Z**，还有余量。

**多 track 情况**：`tracks_multibranch` 扫 10 个分支，collision.kind = `self_multi_container`（`dev-claude` 与 `simonfishgit/dev-claude` 同组）。`coordination.enabled = true / mode = advisory` ⇒ **你确认进 Phase B 时**我会先经 `phase1_gate.py --raw-track-id "a1-entry-claim-duplicate-work-guard" --phase B --mode advisory` 走一次 advisory 认领闸门；现在只是状态查询，未调用。

---

## 🎯 推荐工作流

```
➤ [1] continue-cycle — 续做 a1-entry-claim-duplicate-work-guard (推荐, 88%)
      执行: B.0 heartbeat (先 fetch 后刷) → Rule #6 AB 六套件 → 7.6 → Group 8 发版
      跳过: A.* (Spec 已 approved 且 post_spec/post_planning 均已 CONVERGED)
      理由: handoff §6 首选项 + 唯一 in-flight cycle (31/40)
      ⛔ 前置未满足: ARIA_COORDINATION_NO_PUSH 需在**进程启动时**注入。
         选 [1] 我可以做的是 AB 之外的部分 (heartbeat / 8.1 草稿准备);
         真要跑 AB, 请先 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话。

○ [2] quick-fix — 修 aria-plugin#169 (resilient_push non-FF 恢复路径结构必失败)
      执行: B.1 → B.2 → C.1
      理由: 已开单未修, 影响 acquire_claim + heartbeat 两条写路径, 与本轨强相关

○ [3] doc-update / 开单 — 处理 issue_scan.open_count 静默截断 (handoff M2)
      执行: B.2 → C.1
      理由: 连续两轮实测复现且至今未开单; 属"证据越少越宽松"同族 (与 #182/#173 同形)

○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase B"
```

置信度 88% < 阈值 90%，且 `auto_execute_enabled=false` ⇒ 不自动执行，等你确认。

🤔 选择 [1]-[4] 或输入自定义：

---

**一句话回答你的问题**：文档版本**是一致的** —— 1.69.1 / 1.7.5 / 2.0.0 三条线上 8 个机械核对点全绿，唯一的 `null` 是根 README 用 badge 而非 `**版本**:` 行导致的解析形态问题，不是漂移；真正要当心的是 1.70.0 发版时那 21+ 个同步点。
