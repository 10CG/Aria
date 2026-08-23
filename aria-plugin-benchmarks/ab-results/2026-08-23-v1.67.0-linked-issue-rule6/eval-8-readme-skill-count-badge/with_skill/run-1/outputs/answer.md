# 项目状态扫描 (state-scanner v3.0, scan.py 机械采集 exit=10)

> 先纠正一个前提: 你说的「刚发布 v1.14.0」和仓库事实不符。`aria/.claude-plugin/plugin.json` 当前版本是 **1.66.4** (2026-08-22 发布); v1.14.0 是 2026-04-12 的老版本, 而且那一版的 CHANGELOG 写的是「state-scanner README 检查增强」, 没有新增 3 个 Skill。下面一律按仓库真实状态 (1.66.4) 核对。

## 📍 当前状态

- 分支: `feature/linked-issue-normalization` (upstream origin 同步, ahead 0 / behind 0)
- 未提交变更 2 项: `aria` 子模块 gitlink 未暂存 (9e6a17c → 0fe2e0d, 本地 checkout 比主仓记录新 17 个提交, 即 v1.66.3-17); 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`
- 无 git 中间态 (rebase/merge), 无中断 workflow-state
- UPM 未配置 (`upm.configured=false`)

## 📊 变更分析

变更类型 other x2 / 复杂度 Level 1 / 无架构影响 / 无测试覆盖 / 未检出 SKILL.md 变更 (`skill_changes.detected=false`)

## 📝 README 一致性专项核验 (你点名的三项)

| 检查项 | 实际值 | README 声明 | 结论 |
|--------|--------|-------------|------|
| 1. plugin badge 版本 (主项目 `README.md:8`) | plugin.json = 1.66.4 | `Plugin-v1.66.4-blue` | 一致 (custom check `m6-version-badge-match` 也报 OK) |
| 2. `aria/README.md` 版本行 (第 5 行) | 1.66.4 | `Version: 1.66.4 \| Released: 2026-08-22` | 一致 (`readme.submodules.aria.version_match=true`) |
| 3. Skill 数量 (`aria/README.md:44`) | `aria/skills/` 下 42 个含 SKILL.md 的目录 (43 个目录里 `issue-triage-workspace` 只是 issue-triage 的工作区, 无 SKILL.md, 不算 Skill); 其中 `user-invocable: false` 7 个 | `35 user-facing + 7 internal = 42 total` | 数量一致 |
| 4. Skill 列表完整性 (`aria/README.md:47-110`) | 42 个 Skill | 正文列了 38 条 + 引言行里点名的 2 个内部 skill (agent-team-audit / audit-engine) = 40 | **缺 2 个**: `issue-triage` (v1.19.0 加入) 和 `session-closer` (v1.49.0 加入) 都没有出现在列表任何分组里 |
| 5. 主项目 `README.md` Skill 表 (第 133-142 行) | 42 | `42 Skills (35 user-facing + 7 internal)`, 表里含 issue-triage | **缺 `session-closer`** |

结论: 版本和数量都对, 唯一的漂移是**两个老 Skill 从未补进 README 列表** —— 这不是「刚发版漏更新」, 是 v1.19.0 / v1.49.0 两次发版时就漏了, 只靠总数核对抓不到 (总数是手工改对的, 列表没跟着改)。

## 📄 需求状态

PRD 2 份 (v1 active / v2 approved 待归类) / User Stories: done 17, in_progress 2, approved 1, pending 1

## 🏗️ 架构状态

`docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27 (88 天); `chain_valid=false` (未标 parent_prd)

## 📋 OpenSpec 状态

活跃变更 0 / 待归档 0 / 已归档 138 / ⚠️ 设计未实施 6 个 (全部 approved, tasks 未勾完): aria-2.0-m6-cost-model-telemetry (44d) / m6-dispatch-input-delivery (49d) / m6-e2e-resilience (41d) / m6-release-closeout (89d) / m7-agent-lifecycle (65d) / m7-fleet-aggregation (34d) —— 与 CLAUDE.md 项目状态段描述一致 (卡 owner/基建门)

## 🛡️ 审计状态

审计系统 enabled; 最近 trail: `.aria/audit-reports/linked-issue-normalization-audit-trail.md` (最新 commit 显示 post_planning R5 不收敛, owner override 进 Phase B, Rule #10 已留痕)

## 🔧 自定义检查

10/10 pass: issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match (badge=1.66.4) / m6-claude-md-version / m6-arch-doc-stale / i18n-readme-translation-currency (3 语种 @1.66.4) / claude-md-changelog-free / coordination-gate-invocation / config-template-key-currency / plugin-cache-currency (installed=1.66.4 = sot)

## 🔄 同步状态

- 当前分支与 origin 同步; 多远程 `overall_parity=true` 但 **scan.py 报软错误** (exit 10): `snapshot_consistency_inconclusive` —— 164 条 legacy track 的 AC-5 在 github 远程上无法核验 (git 命令失败), 本次 parity 判决视为未验证
- 子模块: aria 对 origin equal, 对 github 无本地 tracking ref (parity unknown); standards detached HEAD (parity unknown); aria-orchestrator 两远程 equal
- gitlink 完整性: origin 三子模块 ok; github 三子模块 `no_published_ref` (本分支未推 github, 预期内)
- handoff: 最新 `docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md` (9 小时前, pointer 权威)
- 多 track 碰撞: `self_multi_container` (dev-claude vs simonfishgit/dev-claude; aria-runner-bot/023236f2 vs simonfish/bfe8285d) —— 同 owner 多容器, 进 Phase B 前 phase1_gate 会 advisory 提示

## 🎫 Open Issues

44 个 open (Forgejo 10CG/Aria, 06:24Z 刷新)。与本次相关: #177 「CLAUDE.md 发布同步面那行是漏同步面的类级根因」(linked_openspec=linked-issue-normalization) —— 本次发现的 README 列表漏项正是那类问题的又一实例。

## 🎯 推荐工作流

匹配规则: `readme_outdated` (Skill 列表不完整, info 级) + 变更 Level 1 (仅 gitlink 未暂存)。

- **[1] 推荐: 文档修补 (Level 1, 跳过 OpenSpec)** —— 在 `aria/README.md` 补 `issue-triage` (建议放 Requirements 组) 和 `session-closer` (建议放 Ten-Step Cycle Core 旁, 注明「会话收尾, 与 Phase D 正交」); 在主项目 `README.md:133-142` 表加 `session-closer`。不改 description / 不改 Skill 逻辑, Rule #6 不触发 (README 不是运行时指令面)。因属 aria 子模块改动, 走本地 merge + 双推 + ls-remote 核验 (CLAUDE.md 多远程两条硬约束)。顺手把当前未暂存的 aria gitlink 处理掉 (它是当前分支 in-flight 工作的一部分, 建议并入该轨道提交而非单独提)。
- [2] 继续当前轨道 (linked-issue-normalization Phase B), README 漏项挂到 #177 作为补充证据, 等该轨 ship 时一起修
- [3] 仅记录: 把漏项写进本 session handoff, 不动代码
- [4] 自定义组合

理由: 问题确凿但影响仅为文档可读性, 无用户可见功能影响; 当前分支已有 in-flight 工作, 最省事的是并入同轨 (选项 1 或 2)。另外 scan.py 的 `snapshot_consistency_inconclusive` 软错误与你的问题无关, 但 parity 判决本次不可信, 推送前请重扫一次。

请选择 [1]-[4]。
