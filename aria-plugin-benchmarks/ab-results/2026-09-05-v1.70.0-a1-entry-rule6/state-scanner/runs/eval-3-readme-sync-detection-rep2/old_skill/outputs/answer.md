已执行 `/state-scanner` 全量扫描 (Step 0 机械采集: `scan.py` **exit 0**, `errors[] = []`, snapshot schema 1.0, 生成于 2026-09-05T23:30:46Z)。下面是十区块报告，**文档版本一致性单独展开为专项**。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 📍 当前状态

```
  分支: feature/a1-entry-claim-duplicate-work-guard (与 origin 同步, ahead 0 / behind 0)
  模块: 未配置 UPM (upm.configured=false), 无 active module
  Phase/Cycle: 无 UPM 机读区块 —— 进度以 OpenSpec 为准 (a1-entry 母 Spec 31/40)
  变更: 4 个 (3 个 dirty 子模块 gitlink: aria / standards / aria-orchestrator
        + 1 个未跟踪目录 ab-results/2026-09-05-v1.70.0-a1-entry-rule6/), 暂存区为空
  关联 OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 活跃)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (0.93h ago, via pointer) —— 已读, 其 §6 入口指引已纳入下方推荐
  中断状态: .aria/workflow-state.json 存在但 status=completed (2026-09-02 那轮 Phase D 收尾记录),
            git_anchor.branch=master ≠ 当前分支 → 非活跃中断, 不触发 Resume/Abandon 流程
  git 操作: 无进行中的 rebase/merge/cherry-pick (operation=none, 无冲突)
```

## 📊 变更分析

```
  类型: 其他 (4 个变更全部落 other 桶: 子模块指针 + 未跟踪目录), 无 code / test / docs / config 变更
  复杂度: Level 2
  架构影响: 无
  测试覆盖: 不适用 (本次工作树无代码变更)
  Skill 变更: 未检出 SKILL.md 变更 → 本次不触发 Rule #6 AB 区块
  ℹ️ 三个 dirty 子模块是**有意保持**的 (gitlink bump 属 Spec 的 8.2, 要等各子模块合 master 后再做),
     不要 git add —— 依据上次 handoff §0 第 1 条。
```

## 📄 需求状态

```
  配置状态: ✅ 已配置 (docs/requirements/)
  PRD: prd-aria-v1.md (active) / prd-aria-v2.md (raw: "Approved (Draft → Approved 2026-04-11…)")
  User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
  续作候选 (priority_items): US-026 (in_progress, M6 sub-Spec 收敛轨) · US-007 (in_progress) · US-003 (pending)
  OpenSpec 覆盖: 活跃 7 / 已归档 142 (v2.0 的 US-020~027 仍在起草分区)

  ⚠️ 文档状态标注漂移 (与你关心的"一致性"同族, 但属 status 行而非版本号):
     prd-aria-v2.md 的 Status 行原文是 "Approved (Draft → Approved 2026-04-11, 讨论组+挑战组 4 轮收敛)",
     但归一化结果是 **pending** —— 因为括号内 narrative 里的 "Draft" 是更高优先级 token,
     而圆括号和逗号都不是首段分隔符, 整行都参与了归类 (substring shadow)。
     后果: 该 PRD 在机读侧被当成"未开始", 有触发 prd_draft_blocking 规则的风险。
     修复: 把 lifecycle keyword 单独放首段, narrative 移到 em-dash 之后 ——
           > **Status**: Approved — Draft → Approved 2026-04-11, 讨论组+挑战组 4 轮收敛
     依据: references/status-field-guide.md §lifecycle-head 截断 + §Anti-pattern substring shadows
```

## 🏗️ 架构状态

```
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active | 最后更新: 2026-09-02 (自定义检查 m6-arch-doc-stale: OK, age=3d)
  需求链路: ✅ 完整 (chain_valid=true; 上溯 prd-aria-v1.md + prd-aria-v2.md 两份 PRD)
```

## 📋 OpenSpec 状态

```
  活跃变更: 7 个 (approved: 7)
    - a1-entry-claim-duplicate-work-guard      ← 本轨, 31/40
    - aria-2.0-m6-cost-model-telemetry / m6-dispatch-input-delivery / m6-e2e-resilience
    - aria-2.0-m6-release-closeout / m7-agent-lifecycle / m7-fleet-aggregation
  已归档: 142 个 | 待归档: 0 个
  ⚠️ 设计未实施 (design_deferred): 5 个
    - aria-2.0-m6-release-closeout      approved  41/41 未勾选  停滞 103 天
    - aria-2.0-m7-agent-lifecycle       approved  18/18 未勾选  停滞 65 天
    - aria-2.0-m6-cost-model-telemetry  approved  25/38 未勾选  停滞 58 天
    - aria-2.0-m6-e2e-resilience        approved  25/40 未勾选  停滞 55 天
    - aria-2.0-m7-fleet-aggregation     approved  20/20 未勾选  停滞 48 天
```

## 🛡️ 审计状态

```
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
  活跃检查点: post_spec, post_planning (其余 post_brainstorm / mid_implementation /
              post_implementation / pre_merge / post_closure 均为 off)
  上次审计: pre_merge — PASS (R5, 2026-09-02T18:10Z)
  ⚠️ converged=false (第 5 轮判 PASS 但未标记收敛) → 触发 audit_unconverged 建议性提示 (优先级 1.9)。
     该报告对应的是 linked-issue-field-availability 那一轮, 已随 2026-09-02 Phase D 归档,
     不阻塞当前工作; 如需处置: 查报告 / 重跑审计 / 显式接受结论三选一。
     报告: .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-linked-issue-field-availability-aggregated.md
```

## 🔧 自定义检查

```
  14 项全部通过 (0 FAIL / 0 STALE), 其中 6 项直接覆盖文档/版本一致性:

  ✅ m6-version-badge-match            OK badge=1.69.1
  ✅ plugin-version-arch-docs-match    OK plugin=1.69.1 (2 处架构文档版本行匹配)
  ✅ main-project-version-consistency  OK 主项目版本 1.7.5 — 9 个引用点全部一致
  ✅ i18n-readme-translation-currency  OK (3 份 i18n README 均为 1.69.1)
  ✅ m6-claude-md-version              OK version=2.0.0
  ✅ plugin-cache-currency             OK installed=1.69.1 (scope=user) sot=1.69.1
  ✅ m6-arch-doc-stale                 OK age=3d
  ✅ claude-md-changelog-free          OK (无滚动 changelog; 151 行 / 13316 字节)
  ✅ config-template-key-currency      OK (10 键, 0 deprecated, 0 unknown)
  ✅ linked-issue-field-availability   OK (7 份在范围内, 6 条在册)
  ✅ coordination-gate-invocation      OK (近期 7 次生产 run_gate 调用)
  ✅ issue-cache-freshness / silknode-contract-deferral-expiry / forgejo-app-token-liveness  OK
```

## 📝 文档版本一致性 (专项 — 你重点关注的部分)

**结论: 当前所有版本引用面一致, 未检出漂移。** 逐面证据:

| 版本面 | SOT | 派生/引用点 | 实测值 | 判定 |
|--------|-----|------------|--------|------|
| aria-plugin | `aria/.claude-plugin/plugin.json` = **1.69.1** | `aria/README.md` | 1.69.1 | ✅ 一致 (`readme.version_match=true`) |
| aria-plugin | 同上 | root `README.md` Plugin badge | v1.69.1 | ✅ 一致 (m6-version-badge-match) |
| aria-plugin | 同上 | 3 份 i18n README 正文 + `translated-from` 标记 | 1.69.1 | ✅ 全部 current |
| aria-plugin | 同上 | `system-architecture.md §2.8` + `version-scheme.md` 两行 | 1.69.1 | ✅ 2 行匹配 |
| aria-plugin | 同上 | 本机已安装 plugin 副本 (user scope) | 1.69.1 | ✅ 与 SOT 同版 |
| 主项目 Aria | root `VERSION` 头部 = **1.7.5** | 9 个引用点 (含 root README `Project Version` 行 / 对应 Tag 块等) | 1.7.5 | ✅ 9/9 一致 |
| 方法论文档 | `CLAUDE.md` 头部 | **版本**: 2.0.0 | 2.0.0 | ✅ 符合期望值 |
| 架构文档新鲜度 | — | `system-architecture.md` Last Updated | 2026-09-02 (3 天) | ✅ 未陈旧 |

三点需要你知道的**限定条件**, 不影响上面的"一致"结论, 但影响它的解读:

1. **root README 没有独立的"版本"行** —— `readme.root.version` 采集为 `null`。它的版本信息是以
   badge (`Plugin-v1.69.1`) 和正文 `Project Version: 1.7.5 / Plugin Version: 1.69.1` 两种形态呈现的,
   分别由 `m6-version-badge-match` 与 `main-project-version-consistency` 两个探针覆盖。
   也就是说这一格的"一致"来自**自定义检查**, 不是来自 readme collector 的版本字段本身 ——
   readme collector 在 root 这一层是零信息的, 不要把它的沉默当正证据。

2. **这是"发版前的一致", 不是"发版后的一致"。** 上次 handoff §6 写明 `<vNEXT>` = **1.70.0**,
   Group 8 三条 (8.1 CHANGELOG + 版本 SOT 5 文件 → 8.4 aria 本地 merge + 双推 + tag → 8.2 主仓
   16 个版本点 + gitlink bump) **都还没做**。一旦开始 bump, 上表里每一行都要在同一批里改完 ——
   CLAUDE.md §版本管理「发布同步面」列的就是这张表, 历史上漏同步的正是 i18n README 与架构文档两行。

3. **PRD v2 的 Status 归一漂移** (见 📄 需求状态 段) —— 版本号一致, 但文档**状态标注**这一维有一处
   机读与人读不一致, 属同族问题, 一并列出。

## 🔄 同步状态

```
  当前分支: feature/a1-entry-claim-duplicate-work-guard (最新, 与 origin/同名分支 同步)
  远程引用: 1m 前同步 (本轮 Phase 0.5 实拉 8 条 leg, 全部 fetch_ok=true, evidence_grade=fresh,
            skipped 0 —— 下面所有 parity 结论都是本轮验证过的, 不是陈旧 equal)
  子模块 (tree vs remote):
    ✅ standards: 同步        ✅ aria: 同步        ✅ aria-orchestrator: 同步
  ℹ️ 三者 workdir_vs_tree=true —— 工作树 checkout 与主仓记录的 gitlink 不同, 即上面说的"有意 dirty"。
```

## 🌐 多远程一致性

```
  强制远程: origin (forgejo.10cg.pub) + github (github.com), overall_parity = ✅ true
  ✅ 主仓库:            origin=5d9b568 | github=5d9b568   (equal, evidence=fresh)
  ✅ aria 子模块:       origin=ab3dbd0 | github=ab3dbd0   (equal, evidence=fresh)
  ✅ standards 子模块:  origin=bb5d375 | github=bb5d375   (equal, evidence=fresh)
  ❓ aria-orchestrator (分支 feature/m6-cost-model-telemetry):
       origin=92acce5 (equal) | github=unknown (no_local_tracking_ref)
       解读: 该分支从未推过 github, 不是漂移 —— 且 evidence_grade=fresh, 因此**不触发**
             has_unpublished_branch 规则 (该规则要求 evidence_grade != fresh)。它属于另一条在飞的
             track (m6 遥测), 本轨未动。若要发布到 github: git -C aria-orchestrator push -u github <branch>
  ✅ gitlink 完整性: 6/6 (R × S) 全部 ok, 无 orphaned / orphan_unverified —— 主仓已发布 commit
     引用的子模块 gitlink 在两个远程都可达 (这是 CLAUDE.md 硬约束 1 要防的那类断裂)。
```

## 📦 插件依赖 / 🔗 Forgejo 配置

```
  standards 子模块: ✅ 已注册且已初始化
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但 CLAUDE.local.md 缺少 forgejo 配置块
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认) —— 非阻塞, 历史上一直如此
```

## 🎫 Open Issues

```
  open_count: 47 (source=cache, fetched 23:19:26Z, ~11 分钟前 —— 缓存新鲜, 未过 TTL 900s)
  按 repo: 10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 5 · 10CG/aria-orchestrator 2
  标签汇总: bug ×1 —— 无 blocker/critical, 不触发 open_blocker_issues 降级
  近期与本轨相关:
    - Aria#196  unattended 的 Layer 1→2 env 传递三腿契约未定义 (本轨昨日新开)
    - Aria#195  state-scanner: handoff_multibranch 只留 basename, 子目录 handoff 必然 git show 失败
    - Aria#193  同容器 git 身份漂移产生双 owner-container 串 (与下方 collision 直接相关)
    - Aria#188  四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md
    - Aria#177  CLAUDE.md 发布同步面那行是漏同步面的类级根因 ← 与本次"版本一致性"主题直接相关
  ⚠️ 计数可信度: Aria 与 aria-plugin **恰好各报 20** = 顶到 config `issue_scan.limit=20` 上限,
     而 snapshot 里没有任何截断标记。上次 handoff 的 M2 条目实测过同款情形 (报 46 / 实 65)。
     所以 47 应读作"**至少** 47", 不是全量。这一条本身还没开单。
```

## 🌀 多终端协调 (advisory)

```
  tracks_multibranch: 扫描 10 个分支, 121 条去重后 track (legacy 224 直通)
  collision.kind = self_multi_container
    分组: ["dev-claude", "simonfishgit/dev-claude"] —— 同一容器被记成两个身份串 (即 Aria#193)
  config: coordination.enabled=true, mode=advisory
  → 因此**不**走 rule 1.54 的 advisory 提示, 而是在你确认进入 Phase B 时, 由编排层调
    phase1_gate.py --raw-track-id "a1-entry-claim-duplicate-work-guard" --phase B --mode advisory
    本次是只读状态扫描, 未进 Phase B, 故本轮**未调用** run_gate, 也未写任何 claim。
  ⚠️ 本轨 claim 的 sweep 死线是 2026-09-06T21:40Z (handoff §0 第 2 条)。若要刷 heartbeat,
     顺序必须是「先 fetch 再刷」, 反了会被强制 fetch 冲掉 (aria-plugin#169 已实证)。
```

## 🎯 推荐工作流

上次 handoff §6 的入口指引优先于通用规则, 三条候选按它的排序给出:

```
  ➤ [1] continue-cycle: a1-entry-claim-duplicate-work-guard (推荐, 匹配 feature_with_spec, 88%)
        执行: Group 7 (Rule #6 AB 六套件) → 7.6 (TASK-036) → Group 8 发版 1.70.0 (序: 8.1 → 8.4 → 8.2)
        跳过: A.* (Spec 已 approved 且已过 post_planning R4 收敛)
        理由: 母 Spec 31/40, 唯一活跃开发轨, handoff §6 第 1 优先级
        ⛔ 先决条件 (会话级, 本会话内补不上): AB 必须在设了 ARIA_COORDINATION_NO_PUSH=1 的
           **新起 claude 进程**里跑 (export 只影响单个 Bash 子进程, 传不进 subagent)。
           验收方式: eval transcript 里 phase1_gate/release_gate 的 JSON 应含
           "push_skipped": true, "push_skipped_reason": "env_var"; 见到 false 则该 run 作废。
           这**不是** Rule #6 豁免 —— 本批改了 allowed-tools (能力面扩权), 照跑档不变。
        ⚠️ 发版那一步会同时改动上面「文档版本一致性」表里的每一行, 建议 8.1 落地后立即重跑
           /state-scanner 复验 6 个版本探针, 而不是等 8.2 结束再一起看。

  ○ [2] fix: aria-plugin#169 resilient_push non-FF 恢复路径结构必失败
        执行: B.1 → B.2 → C.1 (修复面 lib/failure_handlers.py + lib/coordination_ref.py:1339)
        理由: 影响 acquire_claim 与 heartbeat 两条写路径, claim 会静默丢失; 不受 [1] 的会话级前置阻塞

  ○ [3] triage/fix: issue_scan.open_count 静默截断 (handoff M2, 尚未开单)
        执行: 先开 issue, 或直接改 limit/加截断标记
        理由: 本轮再次复现 (两个 repo 恰好各 20 = 顶到上限且零标记); 与 #182/#173「证据越少越宽松」同族

  ○ [4] 自定义组合
        输入格式: "B.2 + C.1" 或 "Phase B" 或直接说你想做的事
```

**关于你问的版本一致性, 一句话总结**: 六个版本探针 + README collector 全绿, aria-plugin 1.69.1 与主项目
1.7.5 在全部 9 + 5 个引用点上一致, 没有需要现在修的漂移; 真正的风险不在"现在", 而在 [1] 里的 1.70.0
发版 —— 那一步会同时动上表每一行, 历史上漏的就是 i18n README 和架构文档那两行 (Aria#177 在册)。

🤔 请选择 [1]-[4], 或直接说你想做什么。
