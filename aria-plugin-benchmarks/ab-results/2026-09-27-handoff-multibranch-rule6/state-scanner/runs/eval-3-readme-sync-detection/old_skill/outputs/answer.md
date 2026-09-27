已跑 `scan.py`，退出码 0（全部采集成功，`errors[]` 为空）。snapshot schema 版本 `1.0`，与契约一致。数据时间 2026-09-27T16:58Z。

先说你特别问的结论：**文档版本有 2 处不一致，而扫描器的 README 检查和 16 条自定义检查都没有抓到它们**。另有 1 处扫描器没能读出版本（不是一致，是没验证）。详见下方「同步状态」里的 README 版本一致性小节。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/handoff-multibranch-subdir-path-fidelity (HEAD 4f91772)
  模块: — (本仓无运行时 UPM, upm.configured=false)
  Phase/Cycle: — (无 UPM); 从近期提交看本分支是 10CG/Aria#195 轨,
               组 3/组 4 已完成, owner 2026-09-27 裁定已记账, feature 已双推
  变更: 3 项未提交 (均为 other 类)
    - aria        子模块指针变动 (工作区 b181678 ≠ 已提交 gitlink 1cb3872)
    - standards   子模块指针变动 (工作区 d86fc91 ≠ 已提交 gitlink 940cb5b)
    - aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/ (未跟踪, Rule #6 AB 结果目录)
  OpenSpec: handoff-multibranch-subdir-path-fidelity (approved)
  git 操作: 无暂停中的 rebase/merge 等 (operation=none)
  中断恢复: 无 (.aria/workflow-state.json 不存在)
  上次 handoff: 2026-09-24-session-close-199-post-planning-converged.md
               (60.1h 前, via pointer, status=done)

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: 子模块指针 + AB 结果目录 (code 0 / test 0 / docs 0 / other 3)
  复杂度: Level 2
  架构影响: 无
  测试覆盖: — (主仓本身无代码变更; 测试在 aria 子模块的 feature 提交里)
  Skill 变更: 主仓视角未检出 SKILL.md 变更 (改动在 aria 子模块内部提交里,
             对应的 Rule #6 AB 结果目录已在工作区, 尚未提交)

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置
  PRD: prd-aria-v1.md (Active)
       prd-aria-v2.md (原文 "Approved (Draft → Approved 2026-04-11 …)",
                       扫描器归为 pending —— 这是已知误判, 见 10CG/aria-plugin#198)
  User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
    续作项: US-026 (in_progress, M6 剩 Spec #2 + #4), US-007 (in_progress), US-003 (pending)

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02
  需求链路: ✅ 完整 (引用 prd-aria-v1.md + prd-aria-v2.md)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 8 个 (全部 approved)
  已归档: 146 个
  待归档: 0 个
  设计未实施: ⚠️ 5 个 (design_deferred —— 设计已定稿但实施没做完, 不要误判为完成)
    - aria-2.0-m6-release-closeout   (approved, 41/41 未勾, 124d)
    - aria-2.0-m7-agent-lifecycle    (approved, 18/18 未勾, 100d)
    - aria-2.0-m6-cost-model-telemetry (approved, 25/38 未勾, 79d)
    - aria-2.0-m6-e2e-resilience     (approved, 25/40 未勾, 77d)
    - aria-2.0-m7-fleet-aggregation  (approved, 20/20 未勾, 70d)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ✅ 已启用 (convergence 模式)
  活跃检查点: post_spec, post_planning
  上次审计: post_planning R7 (pre-merge-completeness-gate-change-scope)
            — PASS (收敛), 2026-09-24

🔧 自定义检查
───────────────────────────────────────────────────────────────
  16/16 全部通过 (0 失败, 0 跳过)。与版本相关的几条:
  ✅ m6-version-badge-match: OK badge=1.73.3
  ✅ main-project-version-consistency: 主项目版本 1.7.5 — 9 个引用点全部一致
  ✅ plugin-version-arch-docs-match: plugin=1.73.3 (2 处架构文档版本行一致)
  ✅ i18n-readme-translation-currency: 3 份 i18n README 均 @ 1.73.3
  ✅ plugin-cache-currency: installed=1.73.3 sot=1.73.3
  ✅ no-unresolved-version-placeholder: 无残留 <vNEXT>
  ✅ m6-claude-md-version: CLAUDE.md 版本 2.0.0
  其余 9 条 (issue 缓存新鲜度 / token 活性 / claude-md 卫生 / 协调闸调用等) 均 OK

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: 未配置 upstream (no_upstream)
  多远程 parity: ✅ 一致 (overall_parity=true, 证据新鲜, 1 分钟前 fetch)
    主仓 feature 分支: origin = github = 本地 4f91772
    子模块 aria / standards (feature 分支) / aria-orchestrator (master):
      两端均与本地一致
    gitlink 可达性: 3 个子模块 × 2 个 remote 全部 ok
  子模块漂移: aria、standards 工作区领先已提交 gitlink (本轨在飞改动, 属预期);
              三个子模块均未落后远程

  📝 README / 文档版本一致性  ← 本次重点
  ─────────────────────────────
  扫描器结果 (readme collector):
    ✅ 子模块版本号: 一致 (aria plugin.json 1.73.3 = aria/README 1.73.3)
    ⚠️ 主项目 README 版本: 未能解析 (readme.root.version = null)
       —— 这是「没验证」, 不是「一致」。README.md 第 241 行实际写着
          "Project Version: 1.7.5", 与 VERSION 1.7.5 相同, 但该一致性只由
          自定义检查 main-project-version-consistency 兜住, 不来自 README collector。
    ℹ️ README 日期: 本次 snapshot 未输出日期比对项

  按 snapshot 线索补读原文后发现的漂移 (扫描器与 16 条检查均未覆盖):
    ⚠️ VERSION「子模块版本」表 aria 行: 写 v1.73.0, 实际 plugin.json = 1.73.3
       (marketplace.json / aria/VERSION / README badge / 两份架构文档都已是 1.73.3)
       最后一次改这一行是 6a7ab16 (2026-09-08, v1.73.0 发版); 之后
       v1.73.1 ~ v1.73.3 三次 patch 发版都没同步这张表。
       原因: main-project-version-consistency 只管主项目版本号 (1.7.5) 的 9 个点,
       m6-version-badge-match 只管 README badge —— VERSION 里的子模块表没有任何检查守。
    ⚠️ standards 版本: VERSION 表写 v2.2.3, standards/openspec/project.md 头部写 2.2.2
       —— 已有 open issue 10CG/Aria#206 记录, 至今仍未处理, 且同样无机械检查守。
       哪一侧才对需要 owner 裁 (issue 里写的是「已成文待裁」)。
    ℹ️ VERSION 的「对应 Tag」段自述: git tag 最新仍是 v1.5.0, v1.6.0 ~ v1.7.5 未补 tag
       (VERSION 里已标注由 owner 决定, 不是新问题)。
    ℹ️ VERSION 头部「最后更新: 2026-08-16」早于 09-08 的改动 —— 日期字段也没跟着动。

  📦 插件依赖: standards 子模块 ✅ 已注册且已初始化
  🔗 Forgejo 配置: ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)

🎫 Open Issues
───────────────────────────────────────────────────────────────
  共 49 个 open (缓存 2026-09-27T16:54Z; bug 标签 4 个; 无 blocker/critical)
    10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 7 · 10CG/aria-orchestrator 2
  与本次「文档版本一致性」直接相关:
    - 10CG/Aria#206       standards 版本号两处不一致 (v2.2.3 vs 2.2.2), 无机械检查守
    - 10CG/aria-plugin#183 README 同步状态区块在两份文档里定义冲突, 实际输出率 3/30
    - 10CG/aria-plugin#198 _normalize_status 把 "Approved (Draft → Approved …)" 判成 pending
  与当前分支相关:
    - 10CG/aria-plugin#204 (关联 handoff-multibranch-subdir-path-fidelity) 读侧遗留缺口, 本轨明确不修
```

**多终端 / handoff 提示**

- 最新 handoff (09-24, 会话层, status=done) 讲的是 `10CG/Aria#199` 轨; 它的 §6 把 `handoff-multibranch-subdir-path-fidelity` (`10CG/Aria#195`) 列为「待认领、B.1 未起」。但当前分支上今天 (09-27) 已有 #195 的多个提交 (组 3/组 4 完成、owner 裁定记账、feature 双推) —— **handoff 落后于 git 实际进度约 3 天**, 以 git 为准; 这一轨当前的交接内容没写进 handoff。
- `tracks_multibranch.collision.kind = self_multi_container` (同一身份多机: `simonfish/023236f2` 与 `simonfish/bfe8285d`; 另有 aria-runner-bot 与 simonfish 共用身份键的信息级说明)。`coordination.enabled=true`, 所以按契约**不走** 1.54 规则, 而是在你确认进入 Phase B 时由编排层调认领闸。本次评测不执行它, 会执行的命令是:
  ```bash
  python3 "<aria>/skills/state-scanner/scripts/phase1_gate.py" \
    --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase B --mode advisory --repo-path "/home/dev/Aria"
  ```
- 若本会话持有该轨的 active claim, 入口处应刷一次心跳 (同样本次不执行):
  ```bash
  python3 "<aria>/skills/state-scanner/scripts/phase1_gate.py" \
    --heartbeat-only --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase A.1 --repo-path "/home/dev/Aria"
  ```
  handoff 反复提醒过: 心跳按会话触发, 新会话不刷容器 claim, 开工先查心跳年龄。

```
🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] doc-update: 修正 VERSION 子模块版本表 (推荐, 置信度约 85%, 对应 readme_outdated 类)
      执行: 把 VERSION「子模块版本」表 aria 行 v1.73.0 → v1.73.3 (并视情况更新头部「最后更新」)
            → C.1 提交 (docs(version): …)
      跳过: A.* (Level 1 小修, 无需 Spec), B.3 (无架构变更)
      注意: 当前分支是 #195 feature 分支, 不建议把这条无关修复混进去 ——
            要么另起分支单独修, 要么留给 #195 发版时的「发布同步面」(主仓 VERSION 在清单里) 一起改。
      理由: 你本次最关心的就是文档版本一致; 这是唯一一处事实确定、无需裁决的漂移。

  ○ [2] 请 owner 裁 10CG/Aria#206 (standards 版本号 v2.2.3 vs 2.2.2)
      执行: 核对 standards 最近一次版本 bump 的提交, 给出「哪一侧是 SOT」的证据, 交 owner 拍板;
            拍板后按裁定改一侧
      理由: 哪边对不能由 AI 自己定 (issue 状态为「已成文待裁」)。

  ○ [3] 补一条自定义检查, 守 VERSION 子模块表 (aria / standards 两行)
      执行: 在 .aria/state-checks.yaml 增加检查 (或扩 main-project-version-consistency 的 POINTS 清单),
            比对 VERSION 表 ↔ aria/.claude-plugin/plugin.json 与 standards 版本头
      理由: 这两处漂移能存在, 正是因为没有机械检查守; 不补的话下次 patch 发版还会漏。
            属于新增检查, 按规矩需要先有 OpenSpec (Level 2)。

  ○ [4] 继续当前 #195 轨 / 自定义组合
      当前轨下一步大致是: Rule #6 AB 结果落盘 → C.1 提交子模块指针 + AB 结果 → C.2 (须过 pre-merge gate)
      输入格式: "B.2 + C.1" 或 "Phase C"

🤔 选择 [1-4] 或输入自定义:
```

说明: 以上 [1]-[3] 都不会自动执行 (auto_proceed=false), 需要你选择。评测环境只读, 我没有修改任何文件, 也没有调用 phase1_gate.py。
