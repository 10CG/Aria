# 项目状态扫描 (state-scanner v3.x, scan.py 机械采集)

Step 0: `scan.py` 退出码 **10** (部分软错误, snapshot 可用)。软错误 1 条: `snapshot_consistency` — 164 条 legacy handoff track 在 `origin/feature/linked-issue-normalization` 上的 AC-5 一致性无法评估 (git 命令失败), snapshot 声称 `overall_parity=true` 但本次应**视为未验证**。这不影响版本一致性结论 (版本核对用的是本地文件, 非 parity)。

## 1. 当前状态

- 分支: `feature/linked-issue-normalization` (与 `origin` 同步, ahead 0 / behind 0)
- 工作区: 2 个未提交项 — `aria` 子模块指针未暂存 (gitlink `9e6a17c` → 本地检出 `0fe2e0d`, 同名 feature 分支, 属本轨在途变更) + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`
- 中断检测: `none`; git 中间态: `none`
- UPM: 未配置 (collector 认不到仓库根 UPM.md, 即 Aria #188 所述问题)
- 关联 OpenSpec: `linked-issue-normalization` (Draft, A.3 done, post_planning R5 不收敛, owner override 进 Phase B, 目标 v1.67.0)
- 最近提交: `826b356 docs(spec): linked-issue-normalization R5-fix 九条 (2C+7M) + owner override 进 Phase B`

## 2. 变更分析

- 变更数 2, 类型 other (子模块指针 + benchmark 结果目录), 复杂度 Level 1, 无架构影响, 无测试覆盖
- Skill 变更: 主仓 diff 未检出 SKILL.md 变更 (aria 子模块内的 state-scanner 改动属于子模块自身 diff, 本轨 Rule #6 由 spec 的 rule6 安排管)

## 3. 需求状态

- PRD: `prd-aria-v1.md` Active | `prd-aria-v2.md` Approved (归一为 pending — raw 值含长 narrative, 首段截断后仍落 pending, 属 Status 写法问题)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1
- OpenSpec 覆盖率: carry_forward_inventory 为空 (9 个活跃 change 无 carry 记录)

## 4. 架构状态

- `docs/architecture/system-architecture.md` 存在, status Active, 最后更新 2026-05-27 (88 天, 自定义检查 `m6-arch-doc-stale` 仍 OK)
- 需求链路: `chain_valid=false` (parent_prd 未声明)

## 5. OpenSpec 状态

- 活跃 9 个: approved 7 / pending (Draft) 2 (`linked-issue-normalization`, `a1-entry-claim-duplicate-work-guard`)
- 已归档 138, 待归档 0
- 设计未实施 (design_deferred) 6 个: m6-cost-model-telemetry (44d) / m6-dispatch-input-delivery (49d) / m6-e2e-resilience (41d) / m6-release-closeout (89d) / m7-agent-lifecycle (65d) / m7-fleet-aggregation (34d) — 均为 approved 但 tasks 大量未勾, 与 CLAUDE.md「卡 owner/基建门」描述一致

## 6. 审计状态

- enabled; 上次审计: `.aria/audit-reports/linked-issue-normalization-audit-trail.md` (checkpoint/verdict 未解析出 — 按 git log 为 post_planning R5 FAIL 2C+7M, max_rounds 耗尽, owner override 进 B)

## 7. 自定义检查 (10/10 通过)

issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match (badge=1.66.4) / m6-claude-md-version (2.0.0) / m6-arch-doc-stale / i18n-readme-translation-currency (3 语种 @1.66.4) / claude-md-changelog-free (151 行) / coordination-gate-invocation / config-template-key-currency / plugin-cache-currency (installed=1.66.4) — 全部 OK。

**注意**: 这 10 项全绿 ≠ 版本全一致, 它们只覆盖 badge / CLAUDE.md / i18n / 插件缓存几个面, 见第 8 块的人工核对。

## 8. 同步状态 + 文档版本一致性 (本次重点)

多远程: origin parity equal; github 对 feature 分支 `no_local_tracking_ref` (unknown, 正常 — feature 分支只推 origin); gitlink_integrity: origin/aria `orphan_unverified` (连续 1 次, 未达阻断阈值, 因本地 aria 检出领先主仓 gitlink, 属在途状态); github 三个子模块 `no_published_ref` (feature 分支未发布到 github, 预期)。

**版本一致性核对** (以 `aria/.claude-plugin/plugin.json` = SOT):

| 文件 | 值 | 结论 |
|------|-----|------|
| `aria/.claude-plugin/plugin.json` | 1.66.4 | SOT |
| `aria/.claude-plugin/marketplace.json` (两处) | 1.66.4 / 1.66.4 | 一致 |
| `aria/CHANGELOG.md` 顶条 | [1.66.4] 2026-08-22 | 一致 |
| `aria/VERSION` 头部 `**版本**` | 1.66.4 | 一致 |
| `aria/VERSION` 正文 `## 版本号` 代码块 | **1.47.0** | **不一致** (落后 19 个版本; 下方「说明」列表也止于 Minor (38) = v1.41.0 时代) |
| root `README.md` badge | Plugin-v1.66.4 | 一致 |
| `README.zh/ja/ko.md` translated-from | v1.66.4 | 一致 |
| root `CLAUDE.md` 项目状态 | 插件 v1.66.4 / 主项目 v1.7.3 / orchestrator 86bb684 | 插件一致; 见下两行 |
| root `VERSION` 头部 `**版本**` | **1.7.5** | 与同文件代码块 **1.7.3** / 对应 Tag `v1.7.3` / CLAUDE.md `v1.7.3` 三处**不一致** |
| root `VERSION` 子模块表 aria | v1.66.4 | 一致 |
| `CLAUDE.md` orchestrator SHA | 86bb684 | 实际 gitlink `237045a` (86bb684 是其祖先, 仅 docs 提交); 指针过期但无语义漂移 |

**结论**: 插件 5 文件同步面 (plugin.json / marketplace / CHANGELOG / README badge / i18n) 全部一致, 机械检查没说谎。漏网的是两处**机械检查不读的正文**:

- A. `aria/VERSION` 的 `## 版本号` 代码块停在 `1.47.0`, 头部已是 1.66.4 — 同一文件自相矛盾。`m6-version-badge-match` 只读 badge, `plugin-cache-currency` 读 plugin.json, 没有检查读这个代码块, 所以多版本一直漏。
- B. root `VERSION` 头部 1.7.5 (最后更新 2026-08-16) vs 同文件代码块 / Tag / CLAUDE.md 的 1.7.3 — 某次 bump 只改了头部一行。
- C. (次要) CLAUDE.md 的 orchestrator SHA `86bb684` 落后于 gitlink `237045a`。

## 9. Open Issues (issue_scan 开启, fetched 2026-08-23T06:24Z)

open 44 条 (含 10CG/Aria + aria-plugin 两仓)。与本次相关: **#188** 「四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md」 — 本次 scan 的 `upm.configured=false` 正是其复现; #182 handoff frontmatter status 从不收口 (本次 164 legacy track 的 AC-5 软错误与之同源); #184 brainstorm 被共装插件绕过。

## Handoff awareness

最新 handoff: `docs/handoff/2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md` (8.9h 前, latest.md pointer 权威, frontmatter 完整)。多 track 碰撞: `self_multi_container` (dev-claude 与 simonfishgit/dev-claude; aria-runner-bot 与 simonfish 容器) — 进 Phase B 时 phase1_gate advisory 会认领, 本次只读不触发。

## 10. 推荐工作流

当前分支是 `linked-issue-normalization` 的 Phase B 在途轨 (owner 已 override 进 B), 本次你的意图是「看状态 + 查版本」, 不建议在这条 feature 分支上顺手改版本文件 (会把 Level 1 文档修复混进 Level 3 spec 的 PR)。

- **[1] 推荐: 只读收尾, 把两处版本漂移记账** — 不改文件; 把 A/B 两条写进本轨 handoff 或开一张 Aria issue (标题建议「VERSION 文件正文版本块与头部不一致: aria/VERSION 1.47.0 vs 1.66.4; root VERSION 1.7.5 vs 1.7.3」), 后续独立 Level 1 doc_only cycle 处理。理由: 漂移已存在多版本, 不阻塞本轨; 且并发轨 (dev-claude2 / aria-runner-bot) 可能也在动 VERSION, 先登记再改。
- [2] 立即修: 切到 master 开 `fix/version-file-body-drift` 分支, 改 `aria/VERSION` 代码块 1.47.0→1.66.4 (附带清理止于 Minor (38) 的说明列表, 改为指向 CHANGELOG), 改 root `VERSION` 头部 1.7.5→1.7.3 (或反向统一到 1.7.5, 由 owner 裁定哪个是真意图 — 2026-08-16 的 bump 提交能说明), 走 doc_only lane 合并。
- [3] 补机制: 给 `.aria/state-checks.yaml` 加一条 check, 读 `aria/VERSION` 与 root `VERSION` 的 `## 版本号` 代码块并与各自头部/SOT 比对 (当前 10 项检查对这两个正文块全盲, 这正是漂移能存活 19 个版本的原因)。可并入 [2] 同 cycle, 或挂到 #188 的「一致性检查」议题下。
- [4] 继续本轨 Phase B (`linked-issue-normalization`), 版本问题留 handoff。

需要我执行哪一项? (按约定本次只展示推荐, 不自动进 workflow-runner。)
