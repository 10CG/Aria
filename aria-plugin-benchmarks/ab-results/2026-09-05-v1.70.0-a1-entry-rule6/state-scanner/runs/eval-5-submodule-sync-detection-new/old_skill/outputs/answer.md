已跑完状态扫描 (Step 0 机械采集: `scan.py` exit 0, `snapshot_schema_version = 1.0`, `errors[] = []`)。

**先直接回答你的问题: 不需要跑 `git submodule update`, 而且现在跑它是有害的。** 三个子模块的 `tree_vs_remote` 全部为 `false`、`behind_count` 全部为 `0` —— 主仓记录的 gitlink 和各子模块远程默认分支**完全一致**, 没有"落后远程"这回事。你看到的三个 dirty 子模块是另一种偏差 (工作区 checkout ≠ 主仓记录), 详见下面第 8 区块和末尾的结论段。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: `feature/a1-entry-claim-duplicate-work-guard` (与 `origin/…` 同名 upstream, ahead 0 / behind 0)
  模块: — (UPM 未配置)
  Phase/Cycle: — (UPM 未配置; 按 handoff frontmatter 实际处于 **B.2**)
  变更: 4 项 (3 个 dirty 子模块 `aria` / `standards` / `aria-orchestrator` + 1 个未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/`); 暂存区为空
  OpenSpec: `a1-entry-claim-duplicate-work-guard` (approved)
  上次 handoff: `2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md` (0.7h ago, via pointer)
  上一次工作流状态: `.aria/workflow-state.json` = `completed` (D.4 收尾完毕), 无需 Resume / Retry

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: 子模块指针 / 未跟踪产物 (code 0 / test 0 / docs 0 / config 0 / other 4)
  复杂度: Level 2
  架构影响: 无
  测试覆盖: 本次变更无对应测试 (无代码变更)
  Skill 变更: 未检出 SKILL.md 变更 → 无 Rule #6 AB 触发

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置
  PRD: `prd-aria-v1.md` (active) / `prd-aria-v2.md` (Approved, 归一为 pending)
  User Stories: 21 个 (done: 17, in_progress: 2, approved: 1, pending: 1)
  OpenSpec 覆盖: 活跃变更 7 个, 全部 approved

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ✅ 存在
  路径: `docs/architecture/system-architecture.md`
  状态: Active | 最后更新: 2026-09-02
  需求链路: ✅ PRD (v1 + v2) → Architecture 完整

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 7 个 (approved: 7)
  已归档: 142 个 | 待归档: 0 个
  ⚠️ 设计未实施 (`design_deferred`) 5 个:
    - `aria-2.0-m6-release-closeout` (approved, 41/41 未勾, staleness 103d)
    - `aria-2.0-m7-agent-lifecycle` (approved, 18/18 未勾, staleness 65d)
    - `aria-2.0-m6-cost-model-telemetry` (approved, 25/38 未勾, staleness 58d)
    - `aria-2.0-m6-e2e-resilience` (approved, 25/40 未勾, staleness 55d)
    - `aria-2.0-m7-fleet-aggregation` (approved, 20/20 未勾, staleness 48d)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ✅ 已启用
  上次审计: `pre_merge` — **PASS**, 但 `converged = false` (R5, 2026-09-02T18:10Z)
  报告: `.aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-linked-issue-field-availability-aggregated.md`
  ⚠️ 命中规则 `audit_unconverged` (priority 1.9, 降级提示): verdict 是 PASS 但全集未稳定 (max_rounds 耗尽), 不是"已收敛"。属已知项, 不阻断。

🔧 自定义检查
───────────────────────────────────────────────────────────────
  14 项全部通过 (passed 14 / failed 0), 摘录:
    ✅ m6-version-badge-match: OK badge=1.69.1
    ✅ main-project-version-consistency: OK 主项目版本 1.7.5 — 9 个引用点全部一致
    ✅ plugin-version-arch-docs-match: OK plugin=1.69.1 (2 arch doc rows match)
    ✅ i18n-readme-translation-currency: OK (3 份 i18n README current @ 1.69.1)
    ✅ claude-md-changelog-free: OK (151 行 / 13316 字节)
    ✅ coordination-gate-invocation: OK (近期 7 次生产 `run_gate` 调用)
    ✅ config-template-key-currency / plugin-cache-currency / forgejo-app-token-liveness / linked-issue-field-availability / issue-cache-freshness / silknode-contract-deferral-expiry / m6-claude-md-version / m6-arch-doc-stale

🔄 同步状态  ← **你问的就是这一块**
───────────────────────────────────────────────────────────────
  当前分支: `feature/a1-entry-claim-duplicate-work-guard` (最新, 与 `origin/feature/a1-entry-claim-duplicate-work-guard` 同步, ahead 0 / behind 0)
  远程引用: 本轮扫描 Phase 0.5 刚刷新 —— 8 条 fetch leg (2 remote × 4 repo) **全部 `fetch_ok=true`, 0 条 skipped**, 所有 parity 结论的 `evidence_grade` 均为 `fresh` (即: 不是"陈旧的 equal")
  子模块 (主仓记录 gitlink vs 子模块远程默认分支):
    ✅ standards: 同步 (tree=remote=`cc864ee`, behind 0 / ahead 0)
    ✅ aria: 同步 (tree=remote=`7dd0135`, behind 0 / ahead 0)
    ✅ aria-orchestrator: 同步 (tree=remote=`237045a`, behind 0 / ahead 0)
  ⚠️ 工作区偏离主仓记录 (`workdir_vs_tree = true`, 三个子模块都有 —— 这才是 `git status` 里那三行 ` M`):
    - standards: 工作区 HEAD `bb5d375` (分支 `feature/a1-entry-claim-duplicate-work-guard`) ≠ 主仓记录 `cc864ee`
    - aria: 工作区 HEAD `ab3dbd0` (分支 `feature/a1-entry-claim-duplicate-work-guard`) ≠ 主仓记录 `7dd0135`
    - aria-orchestrator: 工作区 HEAD `92acce5` (分支 `feature/m6-cost-model-telemetry`) ≠ 主仓记录 `237045a`
  规则判定: `submodule_drift` (priority 1.97) **未触发** —— 它的触发条件是 `tree_vs_remote == true`, 这里三个全是 `false`。

🌐 多远程一致性 (enforced remotes: `github`, `origin`)
───────────────────────────────────────────────────────────────
  ✅ 主仓库: 所有远程一致 (`github` = `origin` = `5d9b568`, 均 `fresh`)
  ✅ standards 子模块: 所有远程一致 (`bb5d375`, 两端 equal)
  ✅ aria 子模块: 所有远程一致 (`ab3dbd0`, 两端 equal)
  ℹ️ aria-orchestrator 子模块: `origin` equal (`92acce5`); `github` = `unknown` / `no_local_tracking_ref` —— 该 feature 分支只推了 origin, 没推 github。证据是 `fresh`, 属 benign unknown, **不触发** `multi_remote_drift` (1.35) 也不触发 `has_unpublished_branch` (1.36, 它要求 `evidence_grade != fresh`)。
  ✅ gitlink 完整性: 6 个 (remote, submodule) 组合全部 `ok`, 无 `orphaned` / `orphan_unverified`
  **`overall_parity = true`**

  📝 README 版本一致性: ✅ aria 子模块 plugin.json (1.69.1) = README (1.69.1)
  📦 插件依赖: ✅ standards 子模块已注册且已初始化
  🔗 Forgejo 配置检查: ⚠️ 检出 Forgejo 远程 (`forgejo.10cg.pub`) 但 `CLAUDE.local.md` 缺 forgejo 配置块 — 建议: 运行 `/forgejo-sync` 可引导创建 (需确认)

🎫 Open Issues (issue_scan opt-in, 已启用)
───────────────────────────────────────────────────────────────
  open_count: 47 (platform: forgejo, 来源 cache @ 2026-09-05T23:04Z, 含子模块仓)
  label 汇总: bug × 1 → **无 blocker / critical**, `open_blocker_issues` (1.99) 不触发
  与本次问题相关的几条: Aria#195 (state-scanner `handoff_multibranch` basename 缺陷) / Aria#193 (owner-container 身份漂移) / Aria#196 (Layer 1→2 env 三腿契约)
  ⚠️ 口径提醒: 上一份 handoff §2 M2 记录 `open_count` 存在**静默截断** (config `limit=20`, 单仓顶格时无截断标记), 这个 47 是下界不是精确值。

🤝 多终端协调
───────────────────────────────────────────────────────────────
  `tracks_multibranch.collision.kind = self_multi_container` (分组: `dev-claude` / `simonfishgit/dev-claude`, 同一人不同容器身份串)
  `coordination.enabled = true` + `mode = advisory` → 规则 1.54 `concurrent_churn_detected` 不触发 (它只在显式 opt-out 时触发); 取而代之: **你确认进 Phase B 时**, 我会先跑 `phase1_gate.py --raw-track-id a1-entry-claim-duplicate-work-guard --phase B --mode advisory` 认领闸门, 并把 surface 告警逐条回显给你。本次只是状态扫描, 未进 Phase B, 故**未调用**该闸门 (不写、不推 claim)。
  跨 worktree: `global_latest_elsewhere = null` (仅 1 个 worktree), 无跨树交接。

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] 什么都不动 (推荐)
      执行: —
      理由: 子模块同步维度全绿, `overall_parity = true`, 没有任何需要 `submodule update` 的落后项。你担心的"协作者推了子模块更新"在本轮 fresh 证据下不成立。

  ○ [2] feature-dev — 继续 `a1-entry-claim-duplicate-work-guard` (B.2)
      执行: B.2 → C.1 (跳过 A.*, 已有 approved Spec; 跳过 B.1, 分支已建)
      理由: 上一份 handoff §2 记录母 Spec **31/40**, 剩余 9 条。
      ⛔ 注意前置: handoff §2 H1 写明 Group 7 的 Rule #6 AB 评测**阻塞于会话级前置** (`ARIA_COORDINATION_NO_PUSH` 未设, 会话内补不上, 须 owner 以该 env 重启会话); H2 (7.6) 依赖 7.5, 现在做等于改序。

  ○ [3] 处置未收敛审计 (`audit_unconverged`)
      执行: 读 R5 聚合报告 → 接受结论 / 加轮 / 降级三选一
      理由: 上次 `pre_merge` verdict PASS 但 `converged = false`, 结论尚未稳定。

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase B"

🤔 选择 [1-4] 或输入自定义:

---

## 结论: 关于 `git submodule update`

**不需要, 并且建议不要跑。** 两条命令在当前状态下都会造成损失:

| 命令 | 它会做什么 | 在当前状态下的后果 |
|------|-----------|-------------------|
| `git submodule update --remote` | 把子模块拉到**远程默认分支**最新并更新 gitlink | 远程默认分支 = 主仓已记录的那个 commit (`cc864ee` / `7dd0135` / `237045a`), **没有任何新东西可拉**; 但会把三个子模块的工作区从各自 feature 分支挪走 |
| `git submodule update` (不带 `--remote`) | 把子模块工作区**重置**到主仓 HEAD 记录的 gitlink | 三个子模块会从 feature 分支切成 detached HEAD, 你正在做的 in-flight 工作从工作区消失 |

判据来自 snapshot 三个字段, 方向是明确的:

- `tree_vs_remote = false` (三个子模块全部) —— 主仓记录的 gitlink 与子模块远程一致, **不落后**;
- `behind_count = 0` / `ahead_count = 0` —— 无方向性偏差, 故 `hint` / `hint_type` 均为 `null`, 规则引擎不发 `update --remote` 建议;
- `evidence_grade = fresh` (全部 leg) —— 本轮 Phase 0.5 刚 fetch 过 8 条腿且全部成功, 这个 "equal" 是**本轮验证过的**, 不是陈旧引用推出来的。

那三个 ` M` 是 `workdir_vs_tree = true`, 语义完全不同: **子模块工作区停在自己的 feature 分支上, 而主仓 HEAD 记录的还是合并前的 master 侧 commit**。这是多仓并行开发的正常中间态 (上一份 handoff §0 也明确写着"全部有意, 不要 `git add`" —— gitlink bump 要等各子模块合入各自 master 之后再做)。

补充两点值得留意, 但都不需要现在动手:

1. `aria-orchestrator` 的 `feature/m6-cost-model-telemetry` 只推了 `origin`, `github` 没有对应 tracking ref (parity `unknown` / `no_local_tracking_ref`)。这是另一条 track 的分支, 不属于你问的"落后远程", 证据也是 fresh, 所以规则未触发。真要双远程对齐时再 `git -C aria-orchestrator push github feature/m6-cost-model-telemetry`。
2. 若你之后确实要把子模块推进到远程新版本, 正确顺序是先在子模块内 `git -C <path> fetch && git -C <path> log --oneline HEAD..origin/master` 确认有新 commit, 再决定合并策略, 最后在主仓 `git add <path>` bump gitlink —— 而不是用 `submodule update --remote` 一把梭, 因为后者会覆盖工作区当前的分支位置。
