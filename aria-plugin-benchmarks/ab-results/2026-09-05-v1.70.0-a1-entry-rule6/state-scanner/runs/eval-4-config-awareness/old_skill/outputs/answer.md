**先直接回答你的问题: 有。** `/home/dev/Aria/.aria/config.json` 存在 (5603 bytes, 最后修改 2026-08-23), 同目录另有 `config.template.json` 模板。它是一份**被真正使用的**配置 (不是模板占位): `issue_scan` / `coordination` / `audit` / `pre_merge_gate` 四组都显式打开了。完整解读在下方 ⚙️ 区块。

扫描已跑完 (Step 0 机械化路径): `scan.py --output .aria/state-snapshot.json` → **exit 0**, `errors: []`, `snapshot_schema_version: "1.0"`, 生成于 `2026-09-05T23:07:44Z`。以下报告全部读自该 snapshot (未用 `git status` 等手工采集替代)。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/a1-entry-claim-duplicate-work-guard
        (upstream origin/feature/a1-entry-claim-duplicate-work-guard, ahead 0 / behind 0)
  模块: — (UPM 未配置, 无 active_module)
  Phase/Cycle: B.2 (来源: handoff frontmatter; UPM 无 Phase/Cycle 块)
  变更: 4 文件 — 暂存 0 / 未暂存 3 (aria, aria-orchestrator, standards 三个子模块指针 dirty)
        / 未跟踪 1 (aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/)
  OpenSpec: a1-entry-claim-duplicate-work-guard (approved; handoff 记 31/40 任务完成)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (~0.6h ago, via pointer)
  中断状态: .aria/workflow-state.json status=completed (上一 cycle 已收尾, 无需 Resume/Abandon)
            ⚠️ git_anchor.branch=master 与当前分支不符 (branch_anchor_match=false) — 属陈旧锚点, 非中断
  git 操作: 无 (operation=none, has_conflicts=false)

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: 其他 (other 4) — code 0 / test 0 / docs 0 / config 0
  复杂度: Level 2
  架构影响: 无
  测试覆盖: ❌ 无对应测试 (本批无代码变更, 不构成缺口)
  Skill 变更: 未检出 SKILL.md 变更 → 🔬 AB 区块不输出
  说明: 三个子模块 dirty 是 handoff §0 明写的**有意状态** (gitlink bump 归 TASK-038/8.2,
        要等各子模块合 master 之后), 不要 git add。

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置 (docs/requirements/)
  PRD: prd-aria-v1.md (Active) · prd-aria-v2.md (raw="Approved ...", 归一后 pending)
  User Stories: 21 个 (done: 17, in_progress: 2, approved: 1, pending: 1)
  优先项 (priority_items): US-026 (in_progress) · US-007 (in_progress) · US-003 (pending)
  OpenSpec 覆盖率: snapshot 未产出该字段 — 优雅降级, 不展示

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02
  需求链路: ✅ 完整 (chain_valid=true; 双 parent PRD: prd-aria-v1.md + prd-aria-v2.md)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 7 个 (approved: 7)
    - a1-entry-claim-duplicate-work-guard   ← 本轨
    - aria-2.0-m6-cost-model-telemetry
    - aria-2.0-m6-dispatch-input-delivery
    - aria-2.0-m6-e2e-resilience
    - aria-2.0-m6-release-closeout
    - aria-2.0-m7-agent-lifecycle
    - aria-2.0-m7-fleet-aggregation
  已归档: 142 个
  待归档: 0 个
  设计未实施: ⚠️ 5 个 (design_deferred — 设计定稿但实施未做, 勿误判完成)
    - aria-2.0-m6-release-closeout   (approved, staleness 103d, tasks 41/41 未勾)
    - aria-2.0-m7-agent-lifecycle    (approved, staleness  65d, tasks 18/18 未勾)
    - aria-2.0-m6-cost-model-telemetry (approved, staleness 58d, tasks 25/38 未勾)
    - aria-2.0-m6-e2e-resilience     (approved, staleness  55d, tasks 25/40 未勾)
    - aria-2.0-m7-fleet-aggregation  (approved, staleness  48d, tasks 20/20 未勾)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)   ← 来源 .aria/config.json
  活跃检查点: post_spec, post_planning
              (post_brainstorm / mid_implementation / post_implementation / pre_merge / post_closure = off)
  上次审计: ⚠️ pre_merge — PASS (**未收敛**, converged=false)
    时间: 2026-09-02T18:10:11Z
    报告: .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-linked-issue-field-availability-aggregated.md
    选中方式: aggregated-filename (694 候选 / 88 aggregate, 3 条时间戳不可解析)
  建议操作 (rule audit_unconverged, priority 1.9, 非阻塞):
    - 查看报告了解未收敛原因, 或接受当前结论 (handoff 记为「R5 4/4 PASS, 全集未稳定致 max_rounds 耗尽」)

🔧 自定义检查
───────────────────────────────────────────────────────────────
  14/14 全部通过 (0 FAIL / 0 STALE / 0 SKIP)
  ✅ issue-cache-freshness            ✅ silknode-contract-deferral-expiry
  ✅ m6-version-badge-match           ✅ m6-claude-md-version
  ✅ m6-arch-doc-stale                ✅ i18n-readme-translation-currency
  ✅ claude-md-changelog-free         ✅ coordination-gate-invocation
  ✅ config-template-key-currency     ✅ plugin-cache-currency
  ✅ main-project-version-consistency ✅ forgejo-app-token-liveness
  ✅ linked-issue-field-availability  ✅ plugin-version-arch-docs-match

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/a1-entry-claim-duplicate-work-guard
            (最新, 与 origin 同步 — ahead 0 / behind 0, evidence_grade=fresh)
  远程引用: 1m 前同步 (remote_refresh 8 条 leg 全部 fetch_ok, skipped 0 — 新鲜度证据充分)
  协调 ref: refs/aria/coordination 已获取 (19s ago, 无降级)
  子模块:
    ✅ standards:         同步 (tree=remote=cc864ee; 工作区 dirty 系有意)
    ✅ aria:              同步 (tree=remote=7dd0135; 工作区 dirty 系有意)
    ✅ aria-orchestrator: 同步 (tree=remote=237045a; 工作区 dirty 系有意)

🌐 多远程一致性
───────────────────────────────────────────────────────────────
  强制远程: origin, github    overall_parity: ✅ true    待推送: 无
  ✅ 主仓库:            所有远程一致 (origin=github=5d9b568)
  ✅ aria 子模块:       所有远程一致 (origin=github=ab3dbd0)
  ✅ standards 子模块:  所有远程一致 (origin=github=bb5d375)
  ✅ aria-orchestrator: 所有远程一致 (origin=github=92acce5)
  ✅ gitlink 完整性: 6/6 (R,S) 组合全部 ok — 无 orphaned / orphan_unverified

📝 README 同步状态
───────────────────────────────────────────────────────────────
  ✅ 子模块版本号: 一致 (plugin.json v1.69.1 == aria/README v1.69.1)
  ℹ️ 主项目 README: 未解析到版本号 (readme.root.version=null) — 不判定为漂移

📦 插件依赖状态
───────────────────────────────────────────────────────────────
  standards 子模块: ✅ 正常 (已注册 + 已初始化)

🔗 Forgejo 配置检查
───────────────────────────────────────────────────────────────
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但 CLAUDE.local.md 的 forgejo 配置缺失
     (config_status=missing)
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
     注: 这与你问的 .aria/config.json 是**两份不同的配置** — 见下方 ⚙️ 区块「易混淆」一条。

🎫 Open Issues
───────────────────────────────────────────────────────────────
  平台: Forgejo — 47 open
    10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 5 · 10CG/aria-orchestrator 2
  📌 #196 [契约][aria-orchestrator] unattended 的 Layer 1→2 env 传递三腿契约未定义
  📌 #195 state-scanner: handoff_multibranch 递归枚举但只留 basename, 子目录下必然 git show 失败  [bug]
  📌 #193 同容器 git 身份漂移产生双 owner-container 串 — collision 分类并存期失灵
  📌 #192 [Archive Tracker] sibling-spec-probe — 归档残留待办
  📌 #188 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md
  📌 #176 [state-scanner] AC-5 一致性检测未排除本仓不存在的 remote
  数据来源: cache (2026-09-05T23:04:18Z, ~4m ago) | ttl: 15m | 无 blocker/critical label
  ⚠️ 计数可疑 (handoff §2 M2 在册): config `issue_scan.limit = 20`, 而 Aria 与 aria-plugin
     **恰好各报 20** = 顶到上限且无截断标记。上一 session 实测 snapshot 报 46 / 四仓 API 实拉 65。
     本次 47 同样应视为**下界**, 不是真实总数。

📜 Session Handoff
───────────────────────────────────────────────────────────────
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
  写入时间: 2026-09-05T22:35:22+00:00 (~0.6h ago)
  路径: docs/handoff/2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
  来源: pointer (docs/handoff/latest.md 指向, 非 mtime 猜测)
  frontmatter: track-id=a1-entry-claim-duplicate-work-guard · phase=B.2 · status=active
  ✅ AI 已读取本 doc 全文, §6 next-session 入口指引已纳入下方推荐
  ✅ 无漂移文件 (misplaced_files=[], 无 .aria/handoff/ 残留)
  ℹ️ 跨 worktree: 仅 1 个 worktree, 全局最新 handoff 即当前树 — 无需切换
```

---

## ⚙️ 配置状态 — 你问的 `.aria/config.json`

**✅ 存在**, 且被本次扫描实际消费。逐组解读 (未列出的键走 config-loader `DEFAULTS.json` 合并):

| 组 | 关键取值 | 对本次扫描的实际影响 |
|---|---|---|
| `version` | `"1.0"` | — |
| `workflow.auto_proceed` | `false` | Phase 间**不**自动推进, 每步都要你确认 |
| `state_scanner.confidence_threshold` | `90` | 置信度阈值 |
| `state_scanner.auto_execute_enabled` | `false` | **不自动执行** — 即使推荐置信度 ≥90% 也必须等你选 |
| `state_scanner.auto_execute_rules` | `[commit_only, quick_fix, doc_only]` | 上一条为 false, 本表当前无效 |
| `state_scanner.audit_log_path` | `.aria/audit.log` | — |
| `state_scanner.mechanical_mode` | **未显式设置 → 默认 `true`** | 本次走 `scan.py` 机械路径 (非 v2.x prose 回退) |
| `state_scanner.sync_check.*` | `enabled=true / check_submodules=true / check_remote=false` | ⚠️ **这三个键是惰性的** — `sync.py` 从不读取它们, Phase 1.12 恒开启不可关闭 (它承载 US-008 方向性数据丢失护栏)。所以 `check_remote=false` 并没有关掉远程检测, 上面 🔄/🌐 两块照常产出 |
| `state_scanner.issue_scan` | `enabled=true, platform=forgejo, hosts=[forgejo.10cg.pub], limit=20, cache_ttl=900s, stage_timeout=20s, api_timeout=5s, scan_submodules=true, cache=.aria/cache/issues.json` | 🎫 区块因此才显示; `limit=20` 正是上面「47 是下界」的成因; `scan_submodules=true` 让三个子模块仓的 issue 一并进表 |
| `state_scanner.coordination` | `enabled=true, mode=advisory` | Layer L 认领闸门开启。本次 `tracks_multibranch.collision.kind = self_multi_container` (非空) ⇒ **一旦你确认进 Phase B, 编排层须先调 `phase1_gate.py --mode advisory`**, 见推荐 [1] 的前置 |
| `tdd.strictness` | `advisory` | TDD 仅告警不阻断 |
| `benchmarks` | `require_before_merge=true, skill_change_block_mode=warn` | 合并前需 benchmark (Rule #6); Skill 变更以 warn 而非 block 呈现 |
| `experiments.agent_team_audit` | `false` (points=[pre_merge]) | 实验开关关闭 |
| `audit` | `enabled=true, mode=convergence, max_rounds=5`; checkpoints: `post_spec`/`post_planning` = convergence, 其余五个 off; 两个 checkpoint 各 5 席 team | 🛡️ 区块的「已启用/活跃检查点」即来自这里。注意文件内自带一条注释: **AI 不得自行豁免已 enabled 的 checkpoint** (CLAUDE.md 规则 #10) |
| `orchestrator.dispatch_policy` | `tier1=dispatch_ready, tier2=approval_required, tier3=human_only, dry_run=false` | v2.0 运行时派发策略 |
| `phase_c_integrator.pre_merge_gate` | `enabled=true, ci_backends=null, no_ci_fallback=skip_with_warning, wait_timeout=1800s` | Rule #8 闸门开启; 文件内注明 `no_ci_fallback` 尚是**待 owner 裁决的开放问题**, AI 不擅自翻此键 |

**几点值得单独说**:

1. **配置是「真在用」而非模板残留** — 同目录的 `config.template.json` 才是模板; 当前 `config.json` 里带了 4 条 `_comment` / `_lane` 说明各开关的启用日期与依据 (issue_scan 2026-04-09 dogfood 起、coordination 因 DEC-20260704-002 起、audit 分步 rollout、C.2.4 裁决史), 是有维护痕迹的活配置。
2. **易混淆的两份「配置」** — 上面 🔗 区块报的 `config_status: missing` 指的是 **`CLAUDE.local.md` 里的 forgejo 块**, 不是 `.aria/config.json`。后者存在且完好, 前者缺失。两者互不影响, 别把那条 ⚠️ 读成「没有 .aria/config.json」。
3. **缺失字段的行为** — config-loader 对文件缺失是静默回落全默认值; 字段类型错 / 超范围则告警 + 用默认值 / clamp。本次未出现任何配置告警。

---

```
🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] 续做本 cycle: a1-entry-claim-duplicate-work-guard (推荐)
        执行: B.2 剩余 (Group 7 跑评测) → 7.6 (TASK-036) → Group 8 发版 8.1 → 8.4 → 8.2
        跳过: A.* (Spec 已 approved, post_spec R1–R6 已收敛)
        理由: handoff §6 第 1 项点名的续棒入口 (31/40); 叠加 rule feature_with_spec
              (priority 3, 置信度 88%) —— 有 approved OpenSpec + 工作区有在制变更
        ⛔ 先决条件 (会话级, 本会话内补不上):
           Rule #6 AB 需要 ARIA_COORDINATION_NO_PUSH=1 才能跑, 该变量当前 UNSET。
           必须由你以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话, 否则被测
           Skill 会把合成 claim 推到生产 refs/aria/coordination。这**不是** Rule #6 豁免,
           是执行条件不具备。
        ⚠️ 进 Phase B 前两件事:
           (a) coordination.enabled=true 且 collision.kind=self_multi_container
               ⇒ 编排层须调 phase1_gate.py --raw-track-id "a1-entry-claim-duplicate-work-guard"
                 --phase B --mode advisory
           (b) 刷 heartbeat 必须**先 fetch 再刷** (handoff §3 第 4 条; 顺序反了会被强制
               fetch 冲掉, 已有实证)。当前 claim sweep 死线 2026-09-06T21:40Z, 时间充裕

  ○ [2] 修 issue_scan open_count 静默截断
        执行: 开单或直修 (limit=20 顶格 + 零截断标记, 本次 47 即为下界)
        理由: handoff §6 第 2 项 (M2), 且本次扫描再度复现该形状

  ○ [3] 修 aria-plugin#169 — resilient_push non-FF 恢复路径结构必失败
        执行: lib/failure_handlers.py + lib/coordination_ref.py:1339
        理由: handoff §6 第 3 项; 影响 acquire_claim 与 heartbeat 两条写路径, claim 会静默丢失

  ○ [4] 自定义组合 / 仅看状态
        输入格式: "B.2 + C.1" 或 "Phase B", 或直接说「就看看, 不动」

🤔 选择 [1-4] 或输入自定义:
```

> 注: `auto_execute_enabled=false` + `workflow.auto_proceed=false` ⇒ 无论置信度多高都不会自动执行, 上面四项都在等你点头。另: 🛡️ 区块那条 `converged=false` 是非阻塞 advisory, 你可以选择接受现状继续 [1], 不必先处理它。
