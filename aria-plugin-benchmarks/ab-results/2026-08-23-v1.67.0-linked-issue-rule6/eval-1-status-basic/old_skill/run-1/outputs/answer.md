# 项目当前状态 (state-scanner v3.0, scan.py 机械采集)

> scan.py 退出码 **10** (软错误 1 条, snapshot 可用): `snapshot_consistency` 报 AC-5 在 feature 分支 `origin/feature/linked-issue-normalization` 上对 164 条 legacy track 无法核验 (git 命令失败), 因此 **`overall_parity=true` 这个判决本次视为「未核验」**。这是 Aria #176 的已知形态 (单 remote 主仓 + 双 remote 子模块布局下 feature 分支恒 exit 10), 不是本轨新问题。
> 中断检测: `interrupt.status = none`, 无挂起的 workflow-state, 无 git 中间态 (rebase/merge 等均为 none)。

## 1. 当前状态

| 项 | 值 |
|---|---|
| 分支 | `feature/linked-issue-normalization` @ `826b356` (upstream `origin/...` ahead 0 / behind 0) |
| 模块 | 无 UPM (Aria 主仓不配 UPM, `upm.configured=false`, 恒如此) |
| Phase / Cycle | 轨 `linked-issue-normalization`: **Phase B 进行中** (owner 2026-08-23 裁定 override 进 B.1, Rule #10 留痕) |
| 工作树变更 | 2 项: `aria` 子模块 gitlink 偏移 (unstaged) + `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/` (untracked, 本次 AB 工作目录) |
| 关联 OpenSpec | `openspec/changes/linked-issue-normalization/` (Level 3, proposal + tasks + detailed-tasks.yaml) |
| 最近提交 | `826b356` R5-fix 九条 + owner override 进 B / `914a4c7` post_planning R5 FAIL / `09eb919` R5 前收口 |

aria 子模块本地分支 `feature/linked-issue-normalization` @ `0fe2e0d`, 已有两个实现提交 (`8f5f5bd` TASK-001..009 归一函数 + 谓词切换; `0fe2e0d` TASK-011/012 文档同步), origin 同步 equal。

## 2. 变更分析

- 变更类型: `other` x2 (gitlink + benchmark 目录), 无代码 / 测试 / 文档文件直接改动
- 复杂度: **Level 1** (机械判定, 仅看主仓工作树; 实际工作在 aria 子模块内, 已提交)
- 架构影响: 无 | 测试覆盖: 无 (主仓层)
- Skill 变更检测: `detected=false` (主仓工作树看不到子模块内 SKILL.md 改动 — 实际 aria 侧 `state-scanner/SKILL.md:176` 括注已改, **Rule #6 AB 照跑**是本 spec 明文要求, 见下方推荐)

## 3. 需求状态

- 配置: 已配置 (`docs/requirements/`)
- PRD: `prd-aria-v1.md` = Active; `prd-aria-v2.md` = Approved (机械归一为 pending, 因 raw 里带长叙述)
- User Stories 共 21: done 17 / in_progress 2 (US-007 等) / approved 1 / pending 1 (US-003)
- OpenSpec 覆盖率: 9 个活跃变更, 全部不在 UPM (`active_change_not_in_upm` 恒亮, 同上 Aria 无 UPM)

## 4. 架构状态

- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27 (88 天, 自定义检查 `m6-arch-doc-stale` 仍 OK)
- 需求链路: `chain_valid=false` (`parent_prd=null`, 架构文档未声明父 PRD) — 长期已知, 非本轨

## 5. OpenSpec 状态

活跃变更 9 个: approved 7 / pending (Draft) 2; 已归档 138; 待归档 0。

| 变更 | 状态 | 一句话 |
|---|---|---|
| **linked-issue-normalization** | Draft → **Phase B 进行中** | 本轨。R5 九条已修, owner override 进 B.1 |
| pre-merge-gate-no-run-for-branch (#152) | Approved, B.1-done | 并行轨 (handoff 最新指向它), Phase B 17 任务约 46h 未做 |
| a1-entry-claim-duplicate-work-guard | Draft | C1/C2 owner 裁定已下, 待 rework 后进 A.2 |
| aria-2.0-m6-dispatch-input-delivery | Approved | B.2 完成, 卡 C.2 于 owner/infra 门 |
| aria-2.0-m6-cost-model-telemetry | Approved | Track-1 完成, 合并 gate input-delivery |
| aria-2.0-m6-e2e-resilience | Approved | 代码侧完成, 等 168h 运营跑 |
| aria-2.0-m6-release-closeout / m7-agent-lifecycle / m7-fleet-aggregation | Approved | 待 Phase B (受门顺序) |

设计未实施 (`design_deferred`) 6 个: 上表 6 个 aria-2.0 m6/m7 spec, staleness 34–89 天 (tasks.md 大量未勾选, status 仍 approved)。均受 M6 三门阻塞, 非本轨可动。

## 6. 审计状态

- 审计系统 enabled; 上次审计轨 `.aria/audit-reports/linked-issue-normalization-audit-trail.md` — collector 读出 verdict/checkpoint/timestamp 均为 null (frontmatter 无标量 verdict, 与上一会话 handoff 记录的已知形态一致)
- 从 git log 读真相: post_planning R5 两席 FAIL (2C+7M), `max_rounds=5` 耗尽**不收敛**; owner 裁定修九条后 override 进 Phase B (Rule #10 留痕在审计轨 §10)

## 7. 自定义检查

**10/10 通过**, 0 失败: issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match (badge=1.66.4) / m6-claude-md-version (2.0.0) / m6-arch-doc-stale (88d) / i18n-readme-translation-currency (3 语种 @1.66.4) / claude-md-changelog-free (151 行) / coordination-gate-invocation (近期 4 次 run_gate) / config-template-key-currency / plugin-cache-currency (installed=1.66.4 = sot)。

## 8. 同步状态

- 当前分支: origin ahead 0 / behind 0, 证据等级 fresh (remote refs 1 分钟前刷新, 8 条 leg 全 fetch OK)
- 多远程 parity: `overall_parity=true` 但**本次判决未核验** (见顶部 exit 10 说明)。主仓 github 侧 `unknown/no_local_tracking_ref` — feature 分支本就不推 github 镜像, 不算分叉
- 子模块漂移:
  - `aria`: 工作树 `0fe2e0d` vs 主仓 gitlink 不一致 (`workdir_vs_tree=true`, 本轨有意未提交的 bump), 且相对 origin/master **behind 15** (feature 分支基于 v1.66.4 基线, 正常)
  - `standards` `334c609` / `aria-orchestrator` `237045a`: 零漂移, 双远程 equal
  - gitlink 完整性: origin 三个子模块 ok; github 侧 `no_published_ref` (feature 分支未发布到 github, 预期)
- README 版本一致性: aria plugin.json 1.66.4 = README 1.66.4
- 插件依赖: standards 子模块已初始化且已注册
- Forgejo 配置: `.aria/forgejo.json` 缺失 (检测到 forgejo.10cg.pub remote); 需要时 `/forgejo-sync` 引导创建 — 非阻塞

## 9. Open Issues (issue_scan 开启, 2026-08-23T06:24Z 实时拉取)

open **44** 条, 跨 4 仓 (10CG/Aria, aria-plugin, aria-standards, aria-orchestrator)。与本轨有关 / 新近的:

- Aria #177 [governance] CLAUDE.md:81 发布同步面那行四错一行 — **linked_openspec = linked-issue-normalization** (本轨 5.9/5.10 版本引用面任务即回应它)
- Aria #188 [bug] 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md
- Aria #176 [bug][state-scanner] AC-5 未排除本仓不存在的 remote → feature 分支 exit 恒 10 (正是本次 exit 10 的根因)
- Aria #184 brainstorm 被共装插件静默绕过 / #182 handoff status 从不收口 / #180 heartbeat 零生产调用 / #174 跨 track-id 同源重叠
- aria-plugin #156 phase-c-integrator Rule #8 (b) 腿对未领取 main run 不可见 (linked US-025 类治理: Aria #175)

## Handoff awareness (Phase 1.15)

- 最新 handoff (pointer 权威): `docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md`, 8.9 小时前, frontmatter 完整, `misplaced_files=[]`
- **注意轨道错位**: 该 handoff 的 track-id 是 `pre-merge-gate-no-run-for-branch` (#152, claim active, owner-container `simonfish/023236f2`), 而当前分支是 `linked-issue-normalization`。两轨并行在同一 owner 下, `tracks_multibranch.collision.kind = self_multi_container` (分组 `[dev-claude, simonfishgit/dev-claude]`, `[aria-runner-bot/023236f2, simonfish/bfe8285d]`)。本轨的最新状态只在 git log (`826b356`) 和 proposal Status 行, **尚无本轨 Phase B 的 handoff**。
- 跨 worktree: 仅 1 个 worktree, 无他处 latest。

## 10. 推荐工作流

当前处于 `linked-issue-normalization` Phase B 中段: 组 1-3 (测试 / 实现 / 文档同步 TASK-001..012) 已在 aria 子模块提交, 工作树里出现的 `ab-results/2026-08-23-v1.67.0-linked-issue-rule6/` 正是 tasks.md **4.1 Rule #6 AB** 的工作目录 (12 个 eval + skill-new / skill-snapshot-old + PREDICTION.md)。

**[1] 继续 Phase B — 跑完 Rule #6 AB 后进组 5 发版准备** (推荐, 置信度约 85%)
- 执行: 4.1 `/skill-creator` 对 SKILL.md:176 hunk 照跑 AB (进行中) → 5.14 AB 门范围披露交 owner 确认 → 5.1 全量回归 (`aria/skills/state-scanner/tests/run_tests.py`, 基线 1322) → 5.9/5.10/5.11 版本面 bump v1.67.0 (aria 5 文件 + 主仓 14 引用点 + 双向差集断言) → 5.12 处置 repro 脚本 → 5.13 交 phase-c-integrator (仅 PR + pre-merge 闸门)
- 跳过: A.* (Phase A 已完成并经 owner override), B.1 (分支已建)
- 理由: 分支干净、upstream 同步、自定义检查全绿、实现提交已落 aria 子模块; 剩余就是 AB 门 + 发版同步面。Rule #6 明文「照跑不豁免」(proposal §Rule #6 表), Rule #10 不可自行降级。

**[2] 先写本轨 handoff 再继续** (置信度约 60%)
- 执行: session-closer 产出 `linked-issue-normalization` 轨 Phase B 中段 handoff, 修正「latest 指向 #152 轨」的错位, 然后回到 [1]
- 理由: 两轨并行且 latest.md 指向另一轨; 若本会话中途断, 本轨 B 进度只存在于 git log。成本小 (leaf), 但不是必须现在做。

**[3] 切回 #152 轨 (pre-merge-gate-no-run-for-branch) 从 TASK-004 起** (置信度约 30%)
- 理由: 那条轨 claim 仍 active 且 handoff 写明「下一步 TASK-004」; 但当前 checkout 是本轨, 且本轨 AB 已经开跑, 中途切换浪费上下文。仅当 owner 优先级改变时选。

**[4] 仅查看状态, 不启动工作流**

不建议的动作: `git submodule update --remote aria` — 自定义检查的「AHEAD」提示是针对 master 的通用文案, 本轨 aria 工作树故意停在 feature 分支 `0fe2e0d`, 更新会把实现提交冲掉。

(本次为只读扫描, 未调用 workflow-runner / phase1_gate; 选项确认由您决定。)
