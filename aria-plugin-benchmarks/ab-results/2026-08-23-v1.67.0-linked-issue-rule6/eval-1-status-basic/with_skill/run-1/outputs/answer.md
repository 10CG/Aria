# 项目状态扫描 (state-scanner v3.0, scan.py 机械采集)

> scan.py 退出码 **10** (软错误 1 条, snapshot 可用): `snapshot_consistency` — AC-5 一致性自检对 `github` remote 上 164 条 legacy handoff track 无法评估 (git 命令失败), 因此下面的「多远程 parity=true」按**未经核实**对待。这是已知问题 Aria #176 (单/双 remote 布局下退出码恒为 10), 非本次新问题。

## 1. 当前状态

- 分支: `feature/linked-issue-normalization` @ `826b356` (upstream origin 同名分支, ahead 0 / behind 0)
- 无中断的 workflow-state, 无进行中的 git 操作 (rebase/merge 等)
- 变更文件 2 个 (未提交): `aria` 子模块指针 `9e6a17c → 0fe2e0d` (未 stage) + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`
- UPM 未配置 (无 Phase/Cycle 机读块)
- 关联 OpenSpec: `linked-issue-normalization` (Draft, A.3 done; owner 2026-08-23 裁定修完 R5 九条后 override 进 B.1)
- 最近提交: `826b356` R5-fix 九条 + owner override 进 Phase B (Rule #10 留痕) / `914a4c7` post_planning R5 FAIL / `09eb919` R5 前机械收口 (ship target v1.67.0)

## 2. 变更分析

- 变更类型: other x2 (子模块指针 + benchmark 产物目录); 代码/测试/文档 0
- 复杂度: Level 1; 架构影响: 无; 测试覆盖: 无
- Skill 变更 AB 状态: 主仓工作树未检出 SKILL.md 变更 (实际 Skill 改动在 aria 子模块 feature 分支 `8f5f5bd`/`0fe2e0d` 两个提交里: `normalize_linked_issue` 导出 + `linked_issue_overlaps` 谓词切换 + claim_schema/SKILL.md 文档同步, 对应 TASK-001..012)

## 3. 需求状态

- 已配置。PRD: `prd-aria-v1.md` (Active) / `prd-aria-v2.md` (Approved, 归一为 pending)
- User Stories 21 条: done 17 / in_progress 2 / approved 1 / pending 1
- OpenSpec 覆盖率: collector 未给出数值 (carry_forward_inventory total=0)

## 4. 架构状态

- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27 (88 天, 自定义检查 m6-arch-doc-stale 仍 OK)
- 需求链路 `chain_valid=false` (Parent PRD 解析不到 — 已知 aria-plugin #151: 正则不接受带限定的变体, 文档本身有链接)

## 5. OpenSpec 状态

- 活跃变更 9 个: approved 7 / pending (Draft) 2
  - Draft: `linked-issue-normalization` (本分支轨) / `a1-entry-claim-duplicate-work-guard` (C1/C2 owner 已裁, 待 rework 后进 A.2)
  - Approved 待 Phase B 或受门: `aria-2.0-m6-dispatch-input-delivery` / `m6-cost-model-telemetry` / `m6-e2e-resilience` / `m6-release-closeout` / `m7-agent-lifecycle` / `m7-fleet-aggregation` / `pre-merge-gate-no-run-for-branch` (本地副本仍 Approved; **origin/master 上已归档**, 见第 8 节)
- 已归档 138 个; 待归档 0
- 设计未实施 (design_deferred) 6 个: m6-release-closeout 89 天 / m7-agent-lifecycle 65 天 / m6-dispatch-input-delivery 49 天 / m6-cost-model-telemetry 44 天 / m6-e2e-resilience 41 天 / m7-fleet-aggregation 34 天 — 全部卡 M6 三门 (owner/基建), 非本轨范围

## 6. 审计状态

- 审计系统 enabled。最新报告 `.aria/audit-reports/linked-issue-normalization-audit-trail.md` (collector 解析 verdict/checkpoint 为空 — 该文件是审计轨记事, 非单轮 aggregate)
- 实读审计轨 §10: post_planning R5 两席 FAIL (2C+7M, 0 条新发现, 全为前轮 fix 副产品), `max_rounds=5` 耗尽, **converged=false**; owner 2026-08-23 四选一裁定「修 9 条后 override 进 B.1」, 已按 Rule #10 留痕 (`overridden_by_user`)。九条修法已在 `826b356` 落地, 三条成文为已知限 (跨容器 memory 文件名 / run_all 基线数 / 历史 1.65.5 字面)。

## 7. 自定义检查 (10/10 通过)

issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match (badge=1.66.4) / m6-claude-md-version / m6-arch-doc-stale / i18n-readme-translation-currency / claude-md-changelog-free (151 行) / coordination-gate-invocation (近期 4 次生产 run_gate) / config-template-key-currency / plugin-cache-currency — 全部 OK。

## 8. 同步状态

- 当前分支 vs `origin/feature/linked-issue-normalization`: ahead 0 / behind 0, 证据新鲜 (本次 scan 已 fetch 全部 6 条 leg)
- 多远程 parity: 主仓 origin equal; github 无本地跟踪引用 (parity unknown, 非 unreachable); `overall_parity=true` 但受上述 AC-5 软错误影响按未核实对待
- 子模块: `aria` feature 分支 @ `0fe2e0d` 与 origin equal; `aria-orchestrator` master @ `237045a` 双远程 equal; `standards` detached @ `334c609`
- gitlink 完整性: origin 三个子模块 ok; github 三个 `no_published_ref` (本 feature 分支没推 github, 预期)
- **关键发现 (snapshot 外补核)**: 本分支 `826b356` 已被 `origin/master` 完整包含, 而 `origin/master` 已前进 **12 个提交** — 并发轨 `simonfish/023236f2` 于 2026-08-23 06:05 把 #152 `pre-merge-gate-no-run-for-branch` 走完 Phase B→D 并 **ship aria-plugin v1.66.5** (master gitlink 已到 aria `a0fe720`)。本轨 aria 分支 `0fe2e0d` 仍基于 `9e6a17c` (v1.66.4)。本地 `master` 与 `latest.md` 指针都还停在 08-22。
- README 版本一致性: aria plugin.json 1.66.4 = README 1.66.4 (本地视角); standards 子模块已初始化并注册
- Forgejo 配置: `forgejo_remote_detected=true` 但 `.aria/forgejo` 配置缺失 (可选, `/forgejo-sync` 引导)

## 9. Open Issues (live, 共 44)

- 10CG/Aria 20 / 10CG/aria-plugin 20 / 10CG/aria-orchestrator 2 / 10CG/aria-standards 2
- 与本轨 spec 关联 (linked_openspec=linked-issue-normalization): Aria #177, aria-plugin #133 / #134 / #136 / #137 (其中 #137 已在 v1.66.0 修复, R4 C3 已解除)
- 与本次扫描结果直接相关: Aria #176 (AC-5 退出码恒 10) / Aria #188 (四维一致性恒假阳性 + UPM 认不到根 UPM.md) / aria-plugin #151 (chain_valid 误报) / aria-plugin #155 (collision 把历史 handoff 当活跃 track — 本次 `tracks_multibranch.collision.kind=self_multi_container` 即此误报形态, 分组 [dev-claude, simonfishgit/dev-claude] / [aria-runner-bot/023236f2, simonfish/bfe8285d])

## Handoff 感知

- 最新 handoff (pointer 权威): `docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md` (8.9 小时前, frontmatter 齐全, 无错放文件); 单 worktree
- 但 origin/master 上已有更新的 `2026-08-23-issue152-phase-b-through-d-ship-v1.66.5.md` (track `pre-merge-gate-no-run-for-branch` D-done, 终结)。即**本地 handoff 视图已过期一个周期**, 当前全仓唯一在飞轨应为本分支的 `linked-issue-normalization`。

## 10. 推荐工作流

**[1] 推荐: 先同步 master 再继续 Phase B (linked-issue-normalization)** — 置信度 ~85%

- 匹配规则: 分支上有 Draft spec + owner 已 override 进 B.1 + 子模块 feature 分支有实现提交 → `feature_with_spec` 续做 Phase B; 叠加「并发轨已 ship 新版本」手工前置 (memory: 起 spec/继续前 fetch 全远程 + 读并发轨 handoff)
- 执行步骤:
  1. 本地 `master` 快进到 `origin/master` (`1205ec3`), 读 `2026-08-23-issue152-phase-b-through-d-ship-v1.66.5.md`, 确认 v1.66.5 触点与本轨 (state-scanner `phase1_gate.py` / claim_schema) 无重叠
  2. 本分支 merge `origin/master`; aria 子模块 feature 分支 merge `a0fe720` (v1.66.5) 并双推 (本地 merge, 禁服务端 merge, 推后 `ls-remote` 逐个核验)
  3. 重设 spec 基线 head (yaml `scope_repos[].head`: aria 9e6a17c→a0fe720), 版本目标 v1.67.0 维持 (MINOR 自判; 若裁 PATCH 改 v1.66.6 请 owner 复议)
  4. 按 `detailed-tasks.yaml` 从 B.1 起: 建 claim (`phase1_gate --linked-issue`; 注意 aria-plugin #155 collision 误报属 advisory, 不阻断) → 续 TASK-013 起 (TASK-001..012 已在 aria `8f5f5bd`/`0fe2e0d` 落地, 需核对 tasks.md 勾选与代码一致) → Rule #6: `description`/指令流程有变动照跑 AB
- 跳过: A.1/A.2/A.3 (已完成, owner override 留痕)
- 理由: 不先合 master 就继续, 会在 C.2 撞 v1.66.5 的 5 文件发布同步面 (CLAUDE.md/VERSION/README/i18n) 与 gitlink bump, 重演 #165 类冲突

**[2] 仅提交当前工作树** — 置信度 ~40%
- 工作树只有 aria gitlink 偏移 + 未跟踪 AB 产物目录; gitlink bump 属 B 阶段交付物, AB 产物目录按约定归 `aria-plugin-benchmarks/ab-results/` 提交, 但单独提交意义不大, 建议并入 [1] 的 B 进度提交

**[3] 处理 `a1-entry-claim-duplicate-work-guard` Draft rework** — 置信度 ~30%
- owner C1/C2 裁定已下, 待 rework 进 A.2; 与本轨 (linked-issue 归一) 主题相邻但独立, 建议本轨 ship 后再起, 避免两轨同时改 state-scanner 编排层

**[4] 自定义组合** — 告诉我要跑哪些步骤 (如 "B.2 + C.1")

> 按本次任务约定, 到此停止, 不调用 workflow-runner / phase1_gate。
