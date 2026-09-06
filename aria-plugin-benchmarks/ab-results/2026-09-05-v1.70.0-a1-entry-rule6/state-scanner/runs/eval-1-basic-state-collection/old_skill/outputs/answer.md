已跑完 `/state-scanner` 全量扫描。

**Step 0 (机械采集)**: `python3 aria/skills/state-scanner/scripts/scan.py --output .aria/state-snapshot.json` → **exit 0** (全部采集成功), `errors[] = []`, `snapshot_schema_version = "1.0"` (与 SKILL.md 契约一致), 生成于 `2026-09-05T23:04:30Z`。

**阶段 0 (中断检测)**: `.aria/workflow-state.json` 存在但 `interrupt.status = "completed"` (上一 cycle `linked-issue-field-availability` 已于 09-02 走完 D.4) → 按决策树忽略, 不展示 Resume/Abandon 选项, 直接进推荐。`git.git_operation_in_progress.operation = "none"` → 无暂停中的 rebase/merge, 安全闸不触发。

**handoff awareness (mandatory)**: 已读 `docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` 全文 (0.5h ago, via pointer), §6 入口指引已纳入下方推荐。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 📍 当前状态

```
  分支: feature/a1-entry-claim-duplicate-work-guard (未 detached, 非浅克隆)
  模块: — (UPM 未配置, upm.configured=false)
  Phase/Cycle: UPM 无数据; 按 handoff frontmatter = Phase B.2, status=active
  变更: 4 项 (3 个 dirty 子模块 + 1 个未跟踪目录), 暂存区为空
  OpenSpec: a1-entry-claim-duplicate-work-guard (approved) — handoff 记 31/40
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (0.5h ago, via pointer, frontmatter 5 字段齐全)
  最近提交: 5d9b568 docs(handoff): §3 第 1 条补 AB 会话运行守则
```

## 📊 变更分析

```
  类型: other ×4 (code 0 / test 0 / docs 0 / config 0)
    未暂存: aria, aria-orchestrator, standards  (子模块 gitlink dirty)
    未跟踪: aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/
  复杂度: Level 2
  架构影响: 无 (architecture_impact=false)
  测试覆盖: ⚠️ 无对应测试 (本批无代码变更, 不适用)
  Skill 变更: 未检出 (skill_changes.detected=false) → 本次不插 🔬 AB 区块
```

> ℹ️ 三个 dirty 子模块**是有意保持的** (handoff §0 第 1 条): gitlink bump 归 TASK-038/8.2, 要等各自合 master 之后, **不要 `git add`**。

## 📄 需求状态

```
  配置状态: ✅ 已配置 (docs/requirements/)
  PRD:
    - prd-aria-v1.md (active)
    - prd-aria-v2.md (归一后 pending)
  User Stories: 21 个 (done: 17, in_progress: 2, approved: 1, pending: 1)
    in_progress: US-026 (M6 sub-Spec 收敛中), US-007
    pending:     US-003
  OpenSpec 覆盖率: — (snapshot 无该派生字段, 不作估算)
```

> ⚠️ **归一化提示 (非阻塞)**: `prd-aria-v2.md` 原文 Status 是 `Approved (Draft → Approved 2026-04-11, 讨论组+挑战组 4 轮收敛)`, 却被 `_normalize_status` 归为 **pending** —— 括号内的 `Draft` 抢在 `Approved` 之前被匹配, 属 status-field-guide 里点名的 substring shadow 反模式。**该 PRD 实际是 Approved**, 若要修请把 lifecycle token 放在首段最前 (`**Approved** — Draft → ...`)。

## 🏗️ 架构状态

```
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02
  需求链路: ✅ 完整 (parent PRDs = prd-aria-v1.md + prd-aria-v2.md)
```

## 📋 OpenSpec 状态

```
  活跃变更: 7 个 (全部 approved)
    - a1-entry-claim-duplicate-work-guard          ← 本轨, 31/40
    - aria-2.0-m6-dispatch-input-delivery
    - aria-2.0-m6-cost-model-telemetry
    - aria-2.0-m6-e2e-resilience
    - aria-2.0-m6-release-closeout
    - aria-2.0-m7-agent-lifecycle
    - aria-2.0-m7-fleet-aggregation
  已归档: 142 个
  待归档: 0 个
  设计未实施: ⚠️ 5 个 (design_deferred, 设计定稿但实施未做, 勿误判完成)
    - aria-2.0-m6-release-closeout    (approved, 41/41 未勾, staleness 103d)
    - aria-2.0-m7-agent-lifecycle     (approved, 18/18 未勾, staleness  65d)
    - aria-2.0-m6-cost-model-telemetry(approved, 25/38 未勾, staleness  58d)
    - aria-2.0-m6-e2e-resilience      (approved, 25/40 未勾, staleness  55d)
    - aria-2.0-m7-fleet-aggregation   (approved, 20/20 未勾, staleness  48d)
```

## 🛡️ 审计状态

```
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
  活跃检查点: post_spec, post_planning  (其余 5 个 checkpoint 显式 off)
  上次审计: ⚠️ pre_merge — PASS (未收敛)
    时间: 2026-09-02T18:10:11Z
    报告: .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-
          linked-issue-field-availability-aggregated.md
    选取: aggregated-filename 法, 694 候选 / 88 汇总件, 3 条时间戳无法解析
  → 触发规则 audit_unconverged (priority 1.9, 75%)
```

> 该报告属**上一 cycle** (linked-issue-field-availability, 已归档)。`converged=false` 是 R5 耗尽 max_rounds 后的降级三选一遗留, 不阻塞本轨。

## 🔧 自定义检查

```
  ✅ 14/14 全部通过 (0 FAIL / 0 STALE / 0 SKIP)
     issue-cache-freshness ................. OK
     silknode-contract-deferral-expiry ..... OK (superseded_by_split)
     m6-version-badge-match ................ OK badge=1.69.1
     m6-claude-md-version .................. OK version=2.0.0
     m6-arch-doc-stale ..................... OK age=3d
     i18n-readme-translation-currency ...... OK (3 份 i18n README @ 1.69.1)
     claude-md-changelog-free .............. OK (151 行 / 13316 bytes)
     coordination-gate-invocation .......... OK (近期 7 次生产 run_gate 调用)
     config-template-key-currency .......... OK (10 键, 0 deprecated, 0 unknown)
     plugin-cache-currency ................. OK installed=1.69.1 sot=1.69.1
     main-project-version-consistency ...... OK 1.7.5, 9 个引用点全一致
     forgejo-app-token-liveness ............ OK (2 枚 token 活性正常)
     linked-issue-field-availability ....... OK (7 份在范围内, 6 条在册)
     plugin-version-arch-docs-match ........ OK plugin=1.69.1 (2 行匹配)
```

## 🔄 同步状态

```
  当前分支: feature/a1-entry-claim-duplicate-work-guard
            (最新, 与 origin/... 同步 — ahead 0 / behind 0, evidence_grade=fresh)
  远程引用: 1m 前同步 (remote_refresh 8 条 leg 全部 fetch_ok=true, 0 skipped)
  协调 ref: refs/aria/coordination 已 fetch (16s 前, 未降级, ref 存在)
  子模块 (tree vs remote):
    ✅ standards         @ bb5d375  同步
    ✅ aria              @ ab3dbd0  同步
    ✅ aria-orchestrator @ 92acce5  同步
    (三者 workdir_vs_tree=true = 工作区 checkout 与主仓 gitlink 不一致, 即上文的有意 dirty)
```

### 🌐 多远程一致性 (enforced remotes: github, origin)

```
  ✅ overall_parity = true
  ✅ 主仓库 (5d9b568): origin / github 两端 equal
  ✅ aria 子模块 (ab3dbd0): 两端 equal
  ✅ standards 子模块 (bb5d375): 两端 equal
  ❓ aria-orchestrator 子模块 (92acce5, 分支 feature/m6-cost-model-telemetry):
       origin = equal;  github = unknown (reason=no_local_tracking_ref, evidence_grade=fresh)
       → benign unknown: 该分支从未推 github, 不是新鲜度问题, 故不触发 multi_remote_drift(1.35)
         也不触发 has_unpublished_branch(1.36, 要求 evidence_grade != fresh)。
         如需消掉: git -C aria-orchestrator push -u github feature/m6-cost-model-telemetry
  ✅ gitlink_integrity: 6/6 (R,S) 全 ok, 0 orphaned / 0 orphan_unverified
  has_pending_push=false, has_unreachable_remote=false
```

### 📝 README 版本一致性

```
  ✅ aria 子模块: plugin.json 1.69.1 == aria/README 1.69.1
  ℹ️ root README: collector 未解析出版本号 (readme.root.version=null),
     但 custom check m6-version-badge-match 独立判定 badge=1.69.1 OK
```

### 📦 插件依赖

```
  ✅ standards 子模块: 已注册且已初始化
```

### 🔗 Forgejo 配置检查

```
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但 CLAUDE.local.md 配置缺失
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

### 🔀 多 track 协调 (tracks_multibranch)

```
  扫描 10 个分支, 998 条 track 输入 → 去重后 121 条 (legacy passthrough 224)
  collision.kind = self_multi_container
    组: ["dev-claude", "simonfishgit/dev-claude"]   ← 同一容器的两个身份串
  coordination.enabled = true (默认开启), mode = advisory
  → 本次扫描**不调用** phase1_gate (它只在你确认进 Phase B 时由编排层调用);
    届时用 handoff §6 的 carry-id 原始串 "a1-entry-claim-duplicate-work-guard"。
```

> ℹ️ 这个 self_multi_container 撞号正是 Aria#193 在跟的「同容器 git 身份漂移产生双 owner-container 串」。

## 🎫 Open Issues

```
  open_count: 47 (source=cache, fetched 2026-09-05T23:04:18Z, 无 fetch_error)
    10CG/Aria .............. 20
    10CG/aria-plugin ....... 20
    10CG/aria-standards ..... 5
    10CG/aria-orchestrator .. 2
  label 汇总: bug ×1  (无 blocker/critical → 不触发 open_blocker_issues 1.99)

  ⚠️ 计数不可信 (已知缺陷, handoff §2 M2): config issue_scan.limit=20,
     而 Aria 与 aria-plugin **恰好各报 20** = 顶到上限且零截断标记。
     上一 session 实拉四仓合计 65。**这个 47 是下界, 不是总量。** 该项至今未开单。

  与本轨最相关的:
    - aria-plugin#169  resilient_push non-FF 恢复路径结构上必失败 (本轨上 session 开单, 未修)
    - aria-plugin#168  audit-engine 轮内不触发 heartbeat
    - aria-plugin#157  ab-suite 对 SKILL.md Layer L / --linked-issue 段零覆盖
    - Aria#195  (bug) state-scanner handoff_multibranch 只留 basename, 子目录 handoff 必失败
    - Aria#193  同容器 git 身份漂移 → 双 owner-container 串 (对应上面的 collision)
    - Aria#188  四维一致性检查恒假阳性 + UPM collector 认不到根 UPM.md
    - Aria#176  AC-5 未排除本仓不存在的 remote (与上面 aria-orchestrator github unknown 同形)
```

## 🎯 推荐工作流

命中规则 (按优先级): `audit_unconverged`(1.9) → `resume_in_progress_us`(1.88) 两条为降级/建议提示; 主工作流规则命中 `feature_with_spec`(3, 88%)。但按 handoff awareness 契约, **handoff §6 的 next-session 入口优先于 generic 规则**, 故 [1] 取本轨续做。

```
  ➤ [1] 续做 a1-entry-claim-duplicate-work-guard (推荐, 88%)
      当前: 31/40, Phase B.2, 分支已就位且三仓两端 MATCH
      执行: B.0 heartbeat → (前置解除后) Group 7 AB → 7.6 → Group 8 发版 (8.1 → 8.4 → 8.2)
      跳过: A.* (Spec 已 Approved 且 post_spec R1-R6 收敛)
      ⛔ 硬前置 (会话级, 本会话内补不上): Rule #6 AB 需要
         `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话;
         实测该 env **当前 UNSET**。这不是 Rule #6 豁免, 是执行条件不具备。
      ⚠️ 顺序约束 (handoff §3): heartbeat 必须 **先 fetch 再写**;
         AB 跑完的清理 `+` fetch 会连真 claim 一起抹掉 → 先跑 AB, 再清理, 最后才刷 heartbeat。
      claim sweep 死线: 2026-09-06T21:40Z (尚有约 22h)

  ○ [2] 修 aria-plugin#169 resilient_push non-FF 恢复路径
      理由: 影响 acquire_claim + heartbeat 两条写路径, claim 会静默丢失;
            修复面 lib/failure_handlers.py + lib/coordination_ref.py:1339
      注意: 属 aria 子模块, 与 [1] 的 Group 8 发版面重叠, 建议排在 8.1 之前或之后, 别并行

  ○ [3] 开单/直接修 issue_scan.open_count 静默截断
      理由: 上面 🎫 区块的 47 是下界; 「证据越少越宽松」与 #182/#173 同族, 至今无单

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase B" 或直接说要做什么
```

**建议先做的一件小事** (不占 [1]-[4] 名额): 三仓子模块保持 dirty 是对的, 但 `docs/handoff/latest.md` 已指向最新 doc、协调 ref 也刚 fetch 过, 所以进 [1] 前只需按 handoff §3 第 4 条刷一次 heartbeat 即可 —— 前提是本会话不打算跑 AB。

🤔 选择 [1]-[4] 或输入自定义:

---

<details>
<summary>本次扫描的诚实边界 (哪些结论是机械的, 哪些是我读出来的)</summary>

- 机械 (scan.py, exit 0): git / changes / requirements / architecture / openspec / audit / custom_checks / sync_status / multi_remote / gitlink_integrity / issue_status / handoff / handoff_worktrees / tracks_multibranch / remote_refresh / coordination_fetch。
- AI 读取 (snapshot 允许的外部文件): handoff 正文、`.aria/config.json` (audit mode / checkpoints / coordination / issue_scan.limit)。
- **未采集**: OpenSpec 覆盖率 (无该字段)、UPM Phase/Cycle (未配置)、`31/40` 进度 (来自 handoff 正文, 非 collector)。
- 单 worktree (worktree_count=1, `global_latest_elsewhere=null`) → 不输出 🌲 跨 worktree 区块。
- `skill_changes.detected=false` → 不输出 🔬 AB 区块; 但 Rule #6 AB 本身**仍欠**, 见 [1] 的硬前置。

</details>
