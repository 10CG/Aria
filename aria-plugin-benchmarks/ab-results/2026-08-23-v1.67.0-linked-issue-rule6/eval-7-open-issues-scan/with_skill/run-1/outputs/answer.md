已按 state-scanner v3.0 流程跑完 `scripts/scan.py` (机械采集, 未手工替代)。退出码 **10** = 部分软错误, snapshot 仍可用; 下面按 10 个 canonical 区块展示, 重点放在你关心的 Open Issues。

> ⚠️ 软错误 (errors[] 1 条): `snapshot_consistency` — AC-5 跨 collector 自洽检查对 164 条历史 handoff 在 `github` remote 上 git 命令失败, 因此「多远程 parity=true」这个结论本次**按未核实对待**。这恰好就是 open issue Aria #176 描述的症状 (见下), 不影响 issue 扫描结果。

```
📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/linked-issue-normalization (upstream origin 同名, ahead 0 / behind 0)
  git 中间态: 无 (rebase/merge 等均 none); 工作流中断记录: 无
  变更文件: 2 (aria 子模块 gitlink 未暂存 + 1 个未跟踪目录 ab-results/…)
  UPM: 未配置 (collector 认不到根 UPM.md → 与 Aria #188 描述一致)
  关联 OpenSpec: linked-issue-normalization (Status=pending, 最近 5 个 commit 全是它的 R5 审计/收口)

📊 变更分析
───────────────────────────────────────────────────────────────
  变更类型: other x2 | 复杂度: Level 1 | 架构影响: 否 | 测试覆盖: 无
  Skill 变更: 未检出 (无 AB 待跑项)

📄 需求状态
───────────────────────────────────────────────────────────────
  PRD: prd-aria-v1 (active) / prd-aria-v2 (Approved, 归一为 pending)
  User Stories 21: done 17 / in_progress 2 / approved 1 / pending 1

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  docs/architecture/system-architecture.md 存在, Status=Active, 最后更新 2026-05-27
  需求链路: chain_valid=false (Parent PRD 未被识别 → 对应 aria-plugin #151 的正则缺陷, 文档本身有链接)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更 9: approved 7 / pending 2 (linked-issue-normalization, a1-entry-claim-duplicate-work-guard)
  已归档 138 | 待归档 0
  ⚠️ 设计未实施 6 个 (approved 但 tasks 未勾):
    m6-release-closeout (89d, 41/41 未做) · m7-agent-lifecycle (65d, 18/18) · m6-dispatch-input-delivery (49d, 30/30)
    m6-cost-model-telemetry (44d, 25/38) · m6-e2e-resilience (41d, 25/40) · m7-fleet-aggregation (34d, 20/20)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  enabled=true | 最近报告: .aria/audit-reports/linked-issue-normalization-audit-trail.md
  verdict / converged 字段读不到 (null) — 据 git log, R5 post_planning 两席 FAIL 未收敛, owner override 进 Phase B (Rule #10 已留痕)

🔧 自定义检查
───────────────────────────────────────────────────────────────
  10/10 ✅ (issue-cache-freshness / m6-version-badge-match / claude-md-changelog-free /
  coordination-gate-invocation / plugin-cache-currency / i18n-readme-translation-currency 等)

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: 与 origin 持平 | 多远程 parity: 报 true, 但本次 AC-5 未核实 (见顶部软错误)
  📝 README: aria 子模块 plugin.json 1.66.4 = README 1.66.4 ✅
  📦 standards 子模块: 已初始化 ✅
  🔗 Forgejo 配置: 检测到 forgejo.10cg.pub 远程, 但 .aria/forgejo 配置缺失 (可 /forgejo-sync 引导)
  🤝 多终端: tracks_multibranch.collision = self_multi_container
     (dev-claude ↔ simonfishgit/dev-claude; aria-runner-bot/023236f2 ↔ simonfish/bfe8285d) — 进 Phase B 前会走 phase1_gate advisory 认领
  📬 最新 handoff: 2026-08-22 (#152 pre-merge-gate-no-run-for-branch, status=active, B.1-done, 9h 前)
```

## 🎫 Open Issues

```
平台: Forgejo — 共 44 open (4 repos, scan_submodules=true)
数据来源: cache (2026-08-23 06:24Z 刚刷新) | ttl 15m | fetch_error: 无
```

**先说两个前提, 免得误判:**

1. **所有 44 条 `labels` 都是空的** — 仓库里没打 label。skill 的 `open_blocker_issues` 规则是按 `blocker/critical` label 触发的, 所以机械层**判不出任何阻塞项**。下面「阻塞性」分档是我按标题 + 对照本次扫描暴露的症状做的启发式判断 (每条 `heuristic: true`), 请当线索不当结论。
2. 配置 `limit: 20` 是**每 repo 上限**, 10CG/Aria 和 10CG/aria-plugin 都刚好 20 条 — 很可能被截断, 真实数量只多不少。要看全量把 `issue_scan.limit` 调大再扫一次。

### A. 直接影响「开发新 feature」这条流水线的 (建议先看)

| # | repo | 标题摘要 | 为什么算阻塞 |
|---|------|---------|------------|
| #188 | Aria | 四维一致性检查恒假阳性 + UPM collector 认不到根 UPM.md | 本次扫描 UPM 就显示「未配置」, 症状已现 |
| #176 | Aria | AC-5 未排除本仓不存在的 remote → 退出码恒 10 | 本次 exit 10 + 164 条 handoff 报错就是它; parity 结论因此不可信 |
| #165 | Aria | GitHub 镜像漏推第三次复发 (子模块服务端合并 + gitlink 无序) | 发版路径事故, 你 ship 新 feature 时会踩 |
| #136 | aria-plugin | branch-manager 走服务端 API merge, 硬约束 1 在插件层零实现 | #165 的疑似根因; 已挂到 linked-issue-normalization spec |
| #137 | aria-plugin | pre_merge_gate `--main-branch` 缺省 main, 本仓是 master → Rule #8 (b) 腿恒绿 | commit 09eb919 说「已修 C3 解除」但 issue 仍 open, 需确认关闭 |
| #156 | aria-plugin | Rule #8 (b) 腿看不见未被领取的 main run (分钟级 fail-open) | 已有 spec pre-merge-gate-no-run-for-branch, 正在 Phase B (#152 轨) |
| #173 | Aria | gate_result 无任务文件时静默 pass | 归档门假绿 |
| #180 / #174 | Aria | claim heartbeat 零调用 30 分钟失效 / 跨 track-id 同源重叠检测不到 | 本次已检出 self_multi_container collision, 这两条决定认领闸门是否真能防撞车 |
| #135 / #155 | aria-plugin | 认领机制三处缺口 / 历史 handoff 当活跃 track 永久误报 | 同上, 多终端场景 |
| #31 | aria-orchestrator | 自主 bot dispatch 时强制 claim | aria-runner-bot 与你同仓接活的撞车面 |

### B. 安全 / 凭据类 (不挡开发, 但不该继续拖)

- Aria #136 cost-sentinel 日志打印完整 Feishu webhook URL (轮换 + 脱敏)
- Aria #170 aether-build-container push 凭据经 `nomad var put` 回显泄漏
- Aria #151 两个 10cg-ci-bot token 归属确认
- aria-plugin #154 L3 tripwire (PostToolUse 凭据形状告警)
- aria-plugin #138 ~ #146 secret-guard 残余面 8 条 (跨段 fail-open / 块结构 / `ssh -c` 逃逸 / `$(…)` heredoc / `&` 换行 / 误报面 / 可移植性 / `!` 边界)

### C. 已挂在活跃 Spec 上的 (有人接手, 跟踪即可)

- → `linked-issue-normalization` (当前分支): Aria #177, aria-plugin #133 / #134 / #136 / #137
- → `pre-merge-gate-no-run-for-branch`: aria-plugin #156
- → US-025: Aria #175 (契约 2 重写, 需 Level 2 spec)

### D. 规范 / 知识层 / 重构 / 功能请求 (非阻塞)

- 规范: Aria #178 / #171 / #164 / #184 / #182; aria-standards #16 / #15
- 重构与 tracker: Aria #169 / #168; aria-plugin #148 / #149 / #150 / #151
- 功能与采用: Aria #167 (Forgejo API 可插拔传输) / #120 (切到 aether-build-container); aria-orchestrator #5

## 🎯 推荐工作流

匹配到的规则 (按优先级): `audit_unconverged` (1.9, 当前轨 R5 未收敛) → `architecture_chain_broken` (1.8, 疑为 collector 缺陷) → `feature_with_spec` (3, 有 7 个 approved spec)。`open_blocker_issues` 因无 label 未触发。

- **[1] 推荐: 先立项再开发 (feature-dev, 从 Phase A.1 起)** — 置信度 80%
  你要做的新 feature 目前没有 spec (Rule #1), 且当前分支是别人的在飞轨 `linked-issue-normalization`。步骤: `/brainstorm` 或 `/spec-drafter` 起 Level 2 proposal → A.2/A.3 → 进 B.1 时 phase1_gate advisory 认领 (collision 已检出, 会给你 surface 告警)。
  理由: 44 条 open issue 里没有一条机械判定为 blocker; 真正会挡你的是流水线类 (A 档), 它们多数已有 spec/轨在修, 不必等。
- **[2] 先修 A 档里「本次扫描已复现」的两条 (#176 / #188), quick-fix Level 1-2** — 置信度 70%
  好处: 之后每次 `/state-scanner` 不再恒 exit 10, parity 结论可信。代价: 新 feature 推迟半天到一天。
- **[3] 切回 master 再起新分支, 不动 linked-issue-normalization** — 置信度 65%
  当前工作树是并发轨的分支 (R5 未收敛、owner override 进 B), 在上面开新 feature 会混入对方提交; 先 `git checkout master` (需你确认, 我不代操作)。
- **[4] 仅查看, 不启动工作流** — 把 `issue_scan.limit` 调到 50 重扫, 给 A 档 issue 打 `blocker` label, 让下次扫描机械判定。

要继续的话告诉我选哪项; 我这次只扫描 + 展示, 没有调 workflow-runner, 也没改任何文件。
