# 项目状态扫描 (state-scanner v3.1.1, 机械 scan.py 路径)

> scan.py 退出码 **10** (部分采集软错误, snapshot 可用)。唯一 `errors[]`: `snapshot_consistency_inconclusive` — AC-5 在 `origin/feature/linked-issue-normalization` 上对 164 条 legacy handoff track 无法评估 (git 命令失败), 而 snapshot 声称 `overall_parity=true`。**本次扫描的多远程 parity 判决按「未核实」处理**。中断检测 `interrupt.status=none`, 无挂起工作流, 直接进入推荐。

## 1. 当前状态

- 分支: `feature/linked-issue-normalization` (主仓 HEAD `826b356`, upstream `origin/feature/linked-issue-normalization` ahead 0 / behind 0)
- 模块: 无 UPM (`upm.configured=false`, Phase/Cycle 未配置)
- 变更文件: 2 (未提交) — `aria` 子模块指针 (未暂存) + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`
- 关联 OpenSpec: `linked-issue-normalization` (审计轨迹 `.aria/audit-reports/linked-issue-normalization-audit-trail.md`; 最近 3 个主仓提交都是它的 R5/post_planning 记录, ship target **v1.67.0**)
- git 中间态: 无 (operation=none, 无冲突)

## 2. 变更分析

- 变更类型: other x2 (子模块 gitlink + 基准测试输出目录); code/test/docs/config 均 0
- 复杂度: Level 1 (机械判定; 但本分支承载的 spec 本身是 Level 2+, 以 proposal 为准)
- 架构影响: 无 | 测试覆盖: 无 | Skill 变更检出: 否 (主仓视角; 子模块内的 state-scanner 改动见第 8 块)

## 3. 需求状态

- 配置: 已配置
- PRD: `prd-aria-v1.md` Active / `prd-aria-v2.md` Approved (机械归类 pending — raw 值 "Approved (Draft → Approved 2026-04-11 ...)" 首段含 Draft, 归一器判成 pending, 属已知 Status 措辞问题, 非真实状态)
- User Stories: done 17 / in_progress 2 (US-007 等) / approved 1 / pending 1 (US-003)
- OpenSpec 覆盖率: 未采集到 carry-forward 条目 (active 9, carry_forward 0)

## 4. 架构状态

- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27 (age 88d, 自定义检查 m6-arch-doc-stale 仍 OK)
- 需求链路: `chain_valid=false` (`parent_prd=null`, 文档未声明所属 PRD) — 长期存在, 非本轮引入

## 5. OpenSpec 状态

- 活跃变更: 9 个 (approved 为主; `a1-entry-claim-duplicate-work-guard` Draft 待 rework 落两项 owner 裁定后进 A.2)
- 已归档: 大量 (自 2025-12-16 起); 待归档: 0
- 设计未实施 (`design_deferred`) 6 个, 均 approved 但 tasks 未勾:
  - aria-2.0-m6-release-closeout 41/41 未做, 89d
  - aria-2.0-m7-agent-lifecycle 18/18 未做, 65d
  - aria-2.0-m6-dispatch-input-delivery 30/30 未勾, 49d (实际代码已在 orchestrator 分支, 卡 owner/infra 门, tasks.md 未回填)
  - aria-2.0-m6-cost-model-telemetry 25/38 未勾, 44d
  - aria-2.0-m6-e2e-resilience 25/40 未勾, 41d
  - aria-2.0-m7-fleet-aggregation 20/20 未做, 34d

## 6. 审计状态

- 审计系统: enabled
- 上次审计: `linked-issue-normalization-audit-trail.md` — collector 未解析出 checkpoint/verdict/timestamp (字段全 null)。按 git log: post_planning R5 两席 FAIL (2C+7M), max_rounds=5 耗尽**未收敛**, 随后 owner override 进 Phase B (Rule #10 留痕, commit `826b356`)。

## 7. 自定义检查 (10/10 通过, 0 失败 0 跳过)

issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match (badge=1.66.4) / m6-claude-md-version (2.0.0) / m6-arch-doc-stale (88d) / i18n-readme-translation-currency (3 语种 @1.66.4) / claude-md-changelog-free (151 行) / coordination-gate-invocation (4 次近期真调) / config-template-key-currency / plugin-cache-currency (installed=1.66.4 = sot 1.66.4) 全部 OK。

**注意**: 这些检查都是「本工作区内部自洽」, 对照的 SOT 是当前 checkout 的 `aria/.claude-plugin/plugin.json` (1.66.4)。它们看不到「远端 master 已经是 1.66.5」这件事, 所以全绿不等于版本是最新的 — 见下块。

## 8. 同步状态 — 文档版本一致性 (用户重点)

**结论先说: 本分支内部的版本面是自洽的, 但整体已经落后远端 master 一个 patch 版 (1.66.4 vs 1.66.5), 且 CLAUDE.md 有一处主项目版本号陈旧。**

A. aria 子模块 5 文件发布同步面 (当前 checkout `0fe2e0d`, 分支 `feature/linked-issue-normalization`) — **内部一致, 全为 1.66.4**:

| 文件 | 版本 |
|------|------|
| `aria/.claude-plugin/plugin.json` (SOT) | 1.66.4 |
| `aria/.claude-plugin/marketplace.json` (两处 version 字段) | 1.66.4 / 1.66.4 |
| `aria/VERSION` | 1.66.4 (2026-08-22) |
| `aria/CHANGELOG.md` 最新条目 | [1.66.4] - 2026-08-22 |
| `aria/README.md` 版本行 | 1.66.4 |

B. 主仓同步面 (当前分支) — 与 1.66.4 一致:

| 文件 | 值 | 判定 |
|------|----|------|
| root `README.md` Plugin badge | v1.66.4 | 与子模块一致 |
| `README.zh.md` / `README.ja.md` / `README.ko.md` translated-from | v1.66.4 x3 | 一致 |
| root `VERSION` | 主项目 **1.7.5** (2026-08-16) | — |
| `CLAUDE.md` 项目状态段 | 插件 v1.66.4 / 主项目 **v1.7.3** / orchestrator 86bb684 | **主项目版本号陈旧**: VERSION 已是 1.7.5 (1.66.2/1.66.3/1.66.4 三次 ship 都改了 VERSION 但没改这行), origin/master 上的 CLAUDE.md 同样写 v1.7.3, 属历史遗留漂移 |
| `CLAUDE.md` orchestrator SHA `86bb684` | 子模块实际 HEAD `237045a` (领先 3 个 commit, 均为 docs/legal-memo) | 轻微陈旧, 语义上 v2.0.0 未变 |

C. 远端 / 分支层面的版本落差 (**最重要的一条**):

- aria 子模块 `origin/master` 已在 `a0fe720` 发布 **v1.66.5** (#152 pre-merge gate 零 run 显影, Merge `feature/152-no-run-for-branch`), 本分支的 aria 基线 `9e6a17c` (gitlink) **落后 15 个 commit** (`drift.behind_count=15`, hint: `git submodule update --remote aria` — 但本分支不该直接 update, 见推荐)。
- 主仓 `origin/master` 领先本分支 **12 个 commit** (`2a1a0b2` v1.66.5 发布同步 → `1205ec3` #152 Phase D 归档), 其 CLAUDE.md 已写「插件 v1.66.5」, root README badge / i18n / VERSION 也已跟到 1.66.5。
- aria 子模块工作区 `0fe2e0d` 比 gitlink `9e6a17c` 多 2 个 commit (TASK-001..012 linked_issue 归一实现 + 文档) — 这是本 spec 的 Phase B 产物, **gitlink 尚未 bump, 主仓 `git status` 显示 ` M aria`**。
- 多远程 parity: `overall_parity=true` 但被 errors[] 标为未核实; github remote 对主仓/子模块均 `no_local_tracking_ref` (feature 分支没推 github, 这是预期 — 双推约束只针对 master); gitlink_integrity origin 三子模块 ok, github 三子模块 `no_published_ref` (同因)。
- 对本 spec 的直接影响: proposal 里 ship target 写 v1.67.0 是基于 1.66.4 基线起草的; 现在基线已是 1.66.5, **ship 前要重算版本号** (MINOR 仍是 1.67.0, 但 CHANGELOG 上一条须接 1.66.5 而非 1.66.4, 且 merge 时会碰 5 文件 SOT 冲突 — 与 v1.66.1 顺延先例同形)。

D. 其他子模块: standards `334c609` 三方一致 (gitlink = 工作区 = origin); aria-orchestrator `237045a` 三方一致。

条件子项: Forgejo 配置 `config_status=missing` (检测到 forgejo remote 但无 `.aria/forgejo.json`, 建议 `/forgejo-sync` 引导), 不影响版本判定。

## 9. Open Issues (issue_scan opt-in, 10CG/Aria, fetched 2026-08-23 06:24Z)

关键项: #188 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md (与本轮 `upm.configured=false` 直接相关, 可能就是 collector 认不到而非真没有) / #184 brainstorm 被共装插件静默绕过 / #182 handoff frontmatter status 从不收口 (与本轮 errors[] 164 条 legacy track 同根) / #180 coordination heartbeat 零生产调用 (a1-entry spec 在修) / #178 hook 类 Spec SC 须声明测哪份副本。均无 linked US / OpenSpec 关联 (heuristic)。

多终端协调: `tracks_multibranch.collision.kind=self_multi_container` (dev-claude 与 simonfishgit/dev-claude; aria-runner-bot/023236f2 与 simonfish/bfe8285d 各成一组) — 同 owner 多容器, advisory 级, 进 Phase B 前由 phase1_gate 认领 (本次按要求不调用)。

最新 handoff: `docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md` (8.9h 前, pointer 来源 latest.md, frontmatter 完整, 无错放文件); 跨 worktree 无其他 latest。

## 10. 推荐工作流

当前处境: `linked-issue-normalization` 已进 Phase B, aria 子模块内实现已落 (`0fe2e0d`), 但 (a) 基线落后远端 master 一个版本, (b) 主仓 gitlink 未 bump, (c) 本次扫描 parity 判决未核实。

- **[1] (推荐) 先同步基线再继续 Phase B — custom: 同步 + B.2**
  步骤: 在 aria 子模块 `git fetch origin && git rebase origin/master` (或 merge) 把 `feature/linked-issue-normalization` 叠到 v1.66.5 之上 → 跑 state-scanner 测试套件确认 linked_issue 归一实现在新基线下全绿 → 主仓 `git merge origin/master` 拿到 #152 的 12 个 commit (CLAUDE.md / README / VERSION 随之到 1.66.5) → 在 proposal 的 ship target 处记「基线 1.66.4→1.66.5, v1.67.0 不变, CHANGELOG 接 1.66.5」。
  理由: 现在不同步, 到 C.2 合并时 5 文件 SOT 必冲突且版本号要重算; 早做冲突面最小 (#152 改的是 phase-c-integrator / workflow-runner, 与本 spec 改的 state-scanner 不重叠)。跳过: A.x (spec 已 approved + owner override 进 B)。

- **[2] 不动基线, 直接继续 B.2 → C.1 (feature-dev 续跑)**
  步骤: B.2 验证 (state-scanner 测试 + Rule #6: 本 spec 改了 SKILL.md:176 括注与 claim_schema 文档, 属描述性改动, rule6_note 应在 tasks 留痕; 若 `normalize_linked_issue` 影响 phase1_gate 输出措辞则照跑 AB) → C.1 提交 gitlink bump。
  理由: 最快推进; 代价是把版本冲突推迟到 C.2, 风险同上。

- **[3] 只修文档漂移 — doc_only: Level 1 修 CLAUDE.md 两处陈旧**
  步骤: CLAUDE.md 项目状态段「主项目 v1.7.3」→ `v1.7.5` (对齐 root VERSION), orchestrator SHA `86bb684` → `237045a` (或去掉 SHA 只留 v2.0.0); 建议在 master 上单独小提交 (origin/master 的 CLAUDE.md 同样陈旧), 不混进本 feature 分支。
  理由: 这是用户问的「文档版本不一致」里唯一真正的**内容错误**; 其余都是「分支落后」而非「文档写错」。可与 [1] 并行。

- **[4] 仅查看状态, 不启动工作流**
  本次扫描到此为止; 若要再看细节可读 snapshot (`eval-3-doc-version-consistency/with_skill/outputs/state-snapshot.json`) 或 `git -C aria log 9e6a17c..a0fe720`。

建议顺序: [1] → [3] (master 上独立提交) → 回到本分支 B.2/C.1。请确认选项或自定义组合 (例如 "[1] + [3]")。本次按要求不调用 workflow-runner / phase1_gate。
