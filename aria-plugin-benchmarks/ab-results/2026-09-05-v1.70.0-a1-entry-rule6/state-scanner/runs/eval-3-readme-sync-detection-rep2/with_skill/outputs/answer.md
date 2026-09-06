已跑 Step 0 机械扫描 (`scripts/scan.py`, **exit 0**, `errors: []`, `snapshot_schema_version: 1.0`, 生成于 2026-09-05T23:29:45Z)。下面按 snapshot 逐区块汇报，**文档版本一致性**在第 8 区块展开（另单列一节做逐维度对账）。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 📍 当前状态

```
  分支: feature/a1-entry-claim-duplicate-work-guard (upstream origin/同名, ahead 0 / behind 0)
  模块: — (UPM 未配置)
  Phase/Cycle: B.2 — a1-entry-claim-duplicate-work-guard 31/40 (来源: 最新 handoff)
  变更: 4 项 (未暂存子模块指针 aria / aria-orchestrator / standards + 未跟踪 ab-results/2026-09-05-v1.70.0-a1-entry-rule6/)
  关联 OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 活跃未归档)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md (0.9h ago, via pointer)
  git 操作中间态: none (无 rebase/merge/cherry-pick 暂停)
  中断状态: `.aria/workflow-state.json` 为上一周期 (linked-issue-field-availability) 的 `completed` 残留, branch_anchor 不匹配当前分支 → 不触发恢复流程
```

> 三个 dirty 子模块指针是**有意保留**的（handoff §0 第 1 条：gitlink bump 归 TASK-038/8.2，要等各自合 master 之后），不要 `git add`。

## 📊 变更分析

```
  类型: 其他 4 (code 0 / test 0 / docs 0 / config 0)
  复杂度: Level 2
  架构影响: 无
  测试覆盖: 无对应测试变更
  Skill 变更 (主仓 diff 视角): 未检出 → AB 状态块本轮不触发
```

> 注意：本周期真实的 SKILL.md 改动落在 `aria` 子模块的 feature 分支上，主仓 diff 只看到一个 gitlink，所以 `changes.skill_changes.detected=false` **不等于**没有 Skill 变更。Rule #6 的实际状态见文末「阻塞项」。

## 📄 需求状态

```
  配置状态: ✅ 已配置 (docs/requirements/)
  PRD: prd-aria-v1.md (Active) / prd-aria-v2.md (Approved)
  User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
  优先项: US-026 (in_progress) / US-007 (in_progress) / US-003 (pending)
```

## 🏗️ 架构状态

```
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02 (自定义检查 m6-arch-doc-stale: OK, age=3d)
  需求链路: ✅ 完整 (PRD v1 + v2 → Architecture)
```

## 📋 OpenSpec 状态

```
  活跃变更: 7 个 (全部 approved)
    a1-entry-claim-duplicate-work-guard / aria-2.0-m6-cost-model-telemetry /
    aria-2.0-m6-dispatch-input-delivery / aria-2.0-m6-e2e-resilience /
    aria-2.0-m6-release-closeout / aria-2.0-m7-agent-lifecycle / aria-2.0-m7-fleet-aggregation
  已归档: 142 个
  待归档: 0 个
  ⚠️ 设计未实施 (design_deferred): 5 个
    - aria-2.0-m6-release-closeout   approved  staleness 103d (41/41 未勾)
    - aria-2.0-m7-agent-lifecycle    approved  staleness  65d (18/18 未勾)
    - aria-2.0-m6-cost-model-telemetry approved staleness 58d (25/38 未勾)
    - aria-2.0-m6-e2e-resilience     approved  staleness  55d (25/40 未勾)
    - aria-2.0-m7-fleet-aggregation  approved  staleness  48d (20/20 未勾)
```

## 🛡️ 审计状态

```
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
  活跃检查点: post_spec, post_planning (其余 5 个 config 显式 off)
  上次审计: pre_merge — PASS，但 converged=false
    2026-09-02T18:10:11Z · linked-issue-field-availability R5
    .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-...-aggregated.md
```

> `converged=false` 是上一周期耗尽 max_rounds 的遗留降级，非本轨新增；本周期尚未触发新审计。

## 🔧 自定义检查

```
  14/14 ✅ 全绿 (0 FAIL / 0 STALE / 0 SKIP)
```

其中与「文档版本一致性」直接相关的 6 条，逐条列在下一节。

## 🔄 同步状态

```
  当前分支: ahead 0 / behind 0 vs origin/feature/a1-entry-claim-duplicate-work-guard (evidence_grade: fresh)
  多远程 parity: ✅ overall_parity = true (enforced remotes: origin + github)
    主仓 .            5d9b568  origin ✅ equal / github ✅ equal
    子模块 aria       ab3dbd0  origin ✅ equal / github ✅ equal
    子模块 standards  bb5d375  origin ✅ equal / github ✅ equal
    子模块 aria-orchestrator 92acce5 (feature/m6-cost-model-telemetry, 另一轨)
  gitlink 完整性: 6/6 (R,S) 对全部 ok，无 orphaned / orphan_unverified
  远端刷新: 8 legs 全部 fetch_ok，refs age 1m，coordination ref 已取到
  handoff 漂移: 0 个错位文件 (canonical docs/handoff/)；跨 worktree: 仅 1 个 worktree，无他树 handoff
```

### 📝 README 版本一致性（本次重点）

**机械结论：已被覆盖的版本维度全部一致；日期维度当前无机械覆盖，是盲区。**

| 维度 | 判定 | 证据 |
|---|---|---|
| 子模块版本号 (aria/README ↔ plugin.json) | ✅ 一致 | `readme.submodules.aria`: readme_version **1.69.1** = plugin_version **1.69.1**, `version_match: true` |
| README Plugin badge ↔ plugin.json | ✅ 一致 | custom check `m6-version-badge-match`: OK badge=1.69.1 |
| 主项目版本 (root VERSION 头部 ↔ 9 个派生引用点) | ✅ 一致 | custom check `main-project-version-consistency`: OK 主项目版本 **1.7.5** — 9 个引用点全部一致 |
| 架构文档版本行 ↔ plugin.json | ✅ 一致 | custom check `plugin-version-arch-docs-match`: OK plugin=1.69.1 (system-architecture.md §2.8 + version-scheme.md 两行匹配) |
| i18n README 正文时效 ↔ plugin.json | ✅ 一致 | custom check `i18n-readme-translation-currency`: OK (3 份 i18n README current @ 1.69.1) |
| CLAUDE.md 版本头 | ✅ 一致 | custom check `m6-claude-md-version`: OK version=2.0.0 |
| 本地安装的插件副本 ↔ 版本 SOT | ✅ 一致 | custom check `plugin-cache-currency`: OK installed=1.69.1 (scope=user) sot=1.69.1 |
| **根 README.md 的版本头** | ⚠️ **无证据（不是「一致」）** | `readme.root`: `exists=true` 但 `version=null` — scan.py 的 `_VERSION_PAT`（`**版本**:` / `Version:` / `## Version:` / `> **Version**:`，含全角冒号）**没能从根 README.md 解析出版本头** |
| **README 日期 ↔ CHANGELOG.md 最新条目日期** | ⚠️ **本轮未检测** | 按 `rules/basic-rules.md §1.3` 的 `readme_date_mismatch`，日期比对的参照源是 **CHANGELOG.md 的最新条目日期**（非 wall-clock），README 侧取「最后更新: YYYY-MM-DD」。但 `collectors/readme.py` 目前只产出 `version` 字段、**不产出 date 字段**（schema `readme` 段亦无 date），所以本轮没有任何日期证据 |

两点需要点明，避免把「没测」读成「没问题」：

1. **根 README.md 的 `version=null` 是零证据，不能当正证据。** 可能是根 README 本就不带版本头（主项目版本以 `VERSION` 文件为 SOT，README 侧以 badge 呈现，这两者都另有探针在管），也可能是版本头写法落在正则覆盖外。前者无需动作，后者是探针盲点。若要确认，最省事的落法是把根 README 的版本呈现点补进 `.aria/probes/main-project-version-consistency.py` 的 `POINTS` 清单（那份清单即覆盖面），而不是靠人眼每次去看。
2. **日期一致性目前完全没有机械宿主。** 规则文档写了 `readme_date_mismatch` 且指定 CHANGELOG.md 为参照源，但 collector 侧没有实现字段 —— 这条规则现在恒不触发。这是「规则在文档里、检查不在代码里」的典型形状，建议开一条 issue（要么给 `collectors/readme.py` 补 `root.date` + `changelog_latest_date`，要么把它降级成一条自定义 check），否则 README 日期漂移永远不会被任何闸门发现。

> 另需知会：版本 SOT 现为 **1.69.1**，而本周期的发版目标是 **1.70.0**（handoff §6：Group 8 执行序 8.1 → 8.4 → 8.2）。也就是说上面这些「一致」都是相对**旧世界 1.69.1** 成立的；一旦 8.1 动了 `aria/.claude-plugin/plugin.json`，这 6 条检查会同时转红，必须按 CLAUDE.md §版本管理的发布同步面（aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README + 架构文档两行）整批同步，而不是逐个补。

### 📦 插件依赖状态

```
  standards 子模块: ✅ 已注册且已初始化
```

### 🔗 Forgejo 配置检查

```
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md 配置块
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

## 🎫 Open Issues

```
  open_count: 47 (来源: cache, fetched_at 2026-09-05T23:19:26Z, platform=forgejo)
  按仓分组: 10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 5 · 10CG/aria-orchestrator 2
  label 汇总: bug 1
  关联需求: Aria#175 → US-025
  近期与本轨相关: Aria#196 (Layer 1→2 env 三腿契约) / Aria#195 (handoff_multibranch basename) /
                  Aria#193 (owner-container 身份漂移) / Aria#176 (AC-5 未排除不存在的 remote)
```

> ⚠️ 这个数字**很可能被静默截断**：config `issue_scan.limit = 20`，而 Aria 与 aria-plugin **恰好各报 20**（顶到上限），且 snapshot 无截断标记。上一份 handoff 已实测过同一形状（报 46 vs 四仓实拉 65，M2 条目，尚未开单）。把 47 当作「至少 47」来读。

## 🎯 推荐工作流

当前是一次以「文档版本一致性」为焦点的状态检查，版本面已全绿、无阻断性发现，因此推荐偏向**把发现落成动作**而不是启动开发流：

- ➤ **[1] 仅状态检查，到此为止（推荐）**
  - 执行: 无后续步骤
  - 理由: 你问的是状态 + 版本一致性，答案已给全：7 个已覆盖维度全部一致 (plugin 1.69.1 / 主项目 1.7.5)，2 个维度是盲区而非漂移。当前工作树没有待提交的实质变更（3 个 dirty 子模块指针是有意保留的）。

- ○ **[2] doc-update：补齐两个版本一致性盲区**
  - 执行: 给 `collectors/readme.py` 补 date 维度（README「最后更新」↔ CHANGELOG.md 最新条目日期），并把根 README 的版本呈现点纳入 `main-project-version-consistency` 的 POINTS 清单
  - 理由: 规则 1.3 写了 `readme_date_mismatch` 却没有代码宿主，这条检查现在恒不触发；顺手把 `issue_scan.open_count` 截断（M2）一并开单
  - 提示: 属需求变更 → 需 Level 2 OpenSpec；非阻塞，可稍后做

- ○ **[3] 续做当前周期 a1-entry-claim-duplicate-work-guard (31/40)**
  - 执行: B.2 剩余 → Group 7 跑评测 → Group 8 发版 (8.1 → 8.4 → 8.2, vNEXT = 1.70.0)
  - ⛔ **前置未满足**: Rule #6 AB 阻塞于**会话级前置** —— `ARIA_COORDINATION_NO_PUSH` 未设置，会话内补不上（`export` 只影响单个 Bash 子进程，改不了 subagent 的继承环境）。须由 owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话后经 `/skill-creator` 跑六个套件。**这不是 Rule #6 豁免，是执行条件不具备。**
  - 另: TASK-036 (7.6) 的 `dependencies: [TASK-035]` 明写依赖 7.5 跑完，现在开工等于改序 (Rule #10)，需 owner 显式放行

- ○ **[4] 自定义组合**
  - 输入格式: "B.2 + C.1" 或 "Phase B"

**🤔 请选择 [1]-[4] 或输入自定义:**

---

### 两条需要你知晓的协调面信号

1. **多容器 track 碰撞 (`collision.kind = self_multi_container`)**：分组 `["dev-claude", "simonfishgit/dev-claude"]` —— 同一容器的两种 owner-container 写法被判成两个身份，正是 Aria#193 描述的身份漂移，不是真的两个人在抢。按 advisory 语义只提示、不阻断。本轮**未调用** `phase1_gate` —— 闸门的成文触发点是「用户确认进入 Phase B 时」，本次只做状态检查，没有进 B；`--heartbeat-only` 同样未调用（本会话不持 active claim，且当前处于 AB 运行语境，任何 claim 写入都不会被推到远端）。
2. **另一条在飞的轨道**：`aria-2-0-m6-dispatch-input-delivery`（owner `aria-runner-bot/bfe8285d`，B.2，2026-09-05 更新）与本轨并行，文件域无交集，但若接下来要动 aria-orchestrator 需先协调。
