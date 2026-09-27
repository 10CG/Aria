╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

> Step 0: `scan.py` 退出码 **0** (全部采集成功, `errors[]` 为空), `snapshot_schema_version = "1.0"` 与契约一致。
> 阶段 0 中断检测: `interrupt.status = none`; `git_operation_in_progress.operation = none` (无暂停中的 rebase/merge)。

**结论先说**: 16 条自定义检查全绿, 插件版本在 README (含 3 份 i18n) / badge / marketplace / aria VERSION / CHANGELOG / 两份架构文档 / 本地插件缓存上**全部是 1.73.3, 一致**。但我额外对「发布同步面」逐个核对时发现 **1 处真实漂移没有任何检查守着**: 主仓 `VERSION` 的「子模块版本」表里 aria 行还写着 **v1.73.0** (应为 v1.73.3)。另有 1 处 standards 版本两处不一致是已登记未修的老问题 (`10CG/Aria#206`)。详见 §同步状态 与 §推荐。

---

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: `feature/handoff-multibranch-subdir-path-fidelity` (HEAD `4f91772`, 无 upstream 跟踪; 相对 `origin/master` 领先 13 / 落后 12)
  模块: — (本仓无运行时 UPM, `upm.configured=false`)
  Phase/Cycle: — (UPM 未配置); 按 handoff: `10CG/Aria#195` 处于 Phase B 组 5, 下一步 TASK-026 (Rule #6 AB)
  变更: 3 项, 均非代码文件
    - ` M aria` (工作区检出 feature `b181678`, gitlink 仍指 `1cb3872`)
    - ` M standards` (工作区检出 feature `d86fc91`, gitlink 仍指 `940cb5b`)
    - `?? aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` (未跟踪的 AB 结果目录)
  OpenSpec: `handoff-multibranch-subdir-path-fidelity` (approved)
  上次 handoff: `2026-09-24-session-close-199-post-planning-converged.md` (60.1h ago, via pointer)
  ⚠️ 这份是**本工作树**里的最新 handoff, 但它属于另一条轨 (`10CG/Aria#199`)。本分支落后 master 12 个提交, master 上有三份更新的 `#195` handoff, 最新为 `2026-09-27-session-close-195-task025-legacy-issue-204.md` (我已用 `git show origin/master:...` 读过, 下面的推荐以它为准)。这正是 `10CG/aria-plugin#204` / `10CG/Aria#218` 描述的读侧缺口: collector 只读当前工作树, 看不到其他分支上的更新 handoff。

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: other ×3 (两个子模块指针中间态 + 一个未跟踪 AB 结果目录)
  复杂度: Level 2 (scan.py 判定)
  架构影响: 无
  测试覆盖: 不适用 (无代码变更)
  说明: `M aria` / `M standards` 按 09-27 handoff 是**正常中间态** —— gitlink bump 归 TASK-030/031, **不要 `git add` 它们**。

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置
  PRD: `prd-aria-v1.md` (Active) / `prd-aria-v2.md` (原文 "Approved (Draft → Approved 2026-04-11 …)", 被归一化成 pending)
    ⚠️ 这是 status 归一化缺陷: 括号里的状态历史参与了归类, PRD v2 实际是 Approved。已登记 `10CG/aria-plugin#198`, 非文档本身问题。
  User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02 (25 天前, `m6-arch-doc-stale` 检查判 OK)
  需求链路: ✅ PRD v1 + PRD v2 → Architecture 完整

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 8 个 (全部 approved)
  已归档: 146 个
  待归档: 0 个
  设计未实施: ⚠️ 5 个
    - aria-2.0-m6-release-closeout — approved, 41/41 任务未勾, 124 天
    - aria-2.0-m7-agent-lifecycle — approved, 18/18 未勾, 100 天
    - aria-2.0-m6-cost-model-telemetry — approved, 25/38 未勾, 79 天
    - aria-2.0-m6-e2e-resilience — approved, 25/40 未勾, 77 天
    - aria-2.0-m7-fleet-aggregation — approved, 20/20 未勾, 70 天
    (与 CLAUDE.md 项目状态一致: M6/M7 受 owner/基建门阻塞, 非新漂移)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ✅ 已启用 (convergence 模式)
  活跃检查点: post_spec, post_planning
  上次审计: post_planning — PASS (收敛, R7) — `pre-merge-completeness-gate-change-scope`, 2026-09-24

🔧 自定义检查 (16/16 通过)
───────────────────────────────────────────────────────────────
  与「文档版本一致性」直接相关的 7 条:
  ✅ m6-version-badge-match: OK badge=1.73.3
  ✅ i18n-readme-translation-currency: OK (3 i18n READMEs current @ 1.73.3)
  ✅ plugin-version-arch-docs-match: OK plugin=1.73.3 (2 arch doc rows match)
  ✅ main-project-version-consistency: OK 主项目版本 1.7.5 — 9 个引用点全部一致
  ✅ m6-claude-md-version: OK version=2.0.0
  ✅ no-unresolved-version-placeholder: rc=0
  ✅ plugin-cache-currency: OK installed=1.73.3 (scope=user) sot=1.73.3
  其余 9 条: issue-cache-freshness / skill-md-sha-backlink-literal-sync / silknode-contract-deferral-expiry / m6-arch-doc-stale / claude-md-changelog-free / coordination-gate-invocation / config-template-key-currency / forgejo-app-token-liveness / linked-issue-field-availability — 全部 OK。

  ⚠️ 注意: 全绿只说明「这 16 条判据」成立, 不说明所有版本引用点都一致 —— 下面 §README 同步状态 里的 `VERSION` 漂移就落在所有检查的覆盖面之外。

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: 无 upstream (`no_upstream`), ahead/behind 不可判
  多远程 parity: ✅ `overall_parity = true` (新鲜度 fresh, refs 1 分钟前刷新)
    - 主仓 `4f91772`: github = origin = 本地
    - standards `d86fc91` / aria `b181678` / aria-orchestrator `237045a`: 两端均 equal
    - gitlink 可达性: 6/6 ok (3 子模块 × 2 remote)
    - 小提示: standards 的 origin leg 上一代 fetch 失败过一次 (`consecutive_unverified=1`), 本代已成功, 不影响结论
  子模块 drift: aria / standards 为 `workdir_vs_tree=true` (即上述 feature 检出中间态), 与远端无偏差

  📝 README / 文档版本一致性 (本次重点, snapshot + 只读逐个核对)
  | 引用点 | 值 | 结论 |
  |---|---|---|
  | `aria/.claude-plugin/plugin.json` (SOT) | 1.73.3 | — |
  | `aria/.claude-plugin/marketplace.json` (两处 version) | 1.73.3 / 1.73.3 | ✅ |
  | `aria/VERSION` | 1.73.3 | ✅ |
  | `aria/CHANGELOG.md` 顶部条目 | [1.73.3] - 2026-09-13 | ✅ |
  | `aria/README.md` | 1.73.3 | ✅ (snapshot `version_match=true`) |
  | 主仓 `README.md` Plugin badge | v1.73.3 | ✅ |
  | `README.zh/ja/ko.md` badge + translated-from 标记 | v1.73.3 ×3 | ✅ |
  | `docs/architecture/system-architecture.md` §2.8 | v1.73.3 | ✅ |
  | `docs/architecture/version-scheme.md` | v1.73.3 | ✅ |
  | aria 子模块 tag | 最新 `v1.73.3` | ✅ |
  | **主仓 `VERSION` 第 24 行「子模块版本」表 aria 行** | **v1.73.0** | ❌ **漂移 (落后 3 个 patch)** |
  | 主仓 `VERSION` 头部 `**版本**` | 1.7.5 | ✅ (9 个引用点一致) |
  | 主仓 `VERSION` standards 行 vs `standards/openspec/project.md` | v2.2.3 vs 2.2.2 | ⚠️ 不一致, 已登记 `10CG/Aria#206` 待裁 |
  | `standards/conventions/session-handoff.md` Version | 1.3.0 | ⚠️ 已知滞后, `10CG/aria-standards#20`; owner 09-27 已裁在 TASK-027 升 1.4.0 |

  关于 `VERSION` 那一行的判断依据:
  - CLAUDE.md §版本管理 把「主仓 VERSION」列为发布同步面之一。
  - `git log -S'v1.73.0' -- VERSION` 显示它最后一次被改是 v1.73.0 发版 (`6a7ab16`), 之后 v1.73.1 / .2 / .3 三次 patch 都没跟上; `origin/master` 上也是 v1.73.0, 不是本分支特有。
  - 为什么检查没抓到: `main-project-version-consistency` 只核主项目版本 1.7.5; `plugin-version-arch-docs-match` 只核两份架构文档; `m6-version-badge-match` 只核 README badge —— **没有一条检查读 `VERSION` 里的子模块表**。
  - snapshot 的 `readme.root.version = null`: collector 没能从主仓 README 解析出主项目版本号 (主仓 README 只有 Plugin badge), 这一项由 custom check 覆盖, 不算漂移。

  📦 插件依赖: standards 子模块 ✅ 已注册且已初始化
  🔗 Forgejo 配置: ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md 配置块
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)

🎫 Open Issues (缓存, 2026-09-27 16:54Z; 每仓最多列 20 条)
───────────────────────────────────────────────────────────────
  共 49 条: 10CG/Aria 20 / 10CG/aria-plugin 20 / 10CG/aria-standards 7 / 10CG/aria-orchestrator 2; 带 bug 标签 4 条, 无 blocker/critical
  与本次「版本一致性」相关:
  - `10CG/Aria#206` standards 版本号两处不一致 (VERSION v2.2.3 vs project.md 2.2.2), 无机械检查守护
  - `10CG/aria-standards#20` session-handoff.md 两次实质增量未升 Version (已裁并入 TASK-027)
  - `10CG/aria-plugin#198` `_normalize_status` 把 "Approved (Draft → Approved …)" 判成 pending (解释了 PRD v2 显示为 pending)
  - `10CG/aria-plugin#183` README 同步状态区块在 SKILL.md 与 output-formats.md 定义冲突
  与当前轨相关: `10CG/aria-plugin#204` (#195 遗留缺口单, linked `handoff-multibranch-subdir-path-fidelity`)

🔀 多终端协调 (tracks_multibranch)
───────────────────────────────────────────────────────────────
  collision.kind = `self_multi_container` —— 容器身份 `023236f2` 与 `bfe8285d` 各自同时出现在 `simonfish` 与 `aria-runner-bot` 两个 owner 名下 (advisory, 不阻断)。
  按 09-27 handoff: 本轨 claim `claims/bfe8285d/s-48ca@0612.yaml` (phase B) 与 `#199` 的 `s-73b9@1606.yaml` 均 active, 最后心跳 2026-09-27 12:35Z 左右, **最晚 2026-09-28 12:35Z 前需要在一个普通会话里刷新**。
  入口心跳: 本会话未持有 claim, 按 SKILL.md 触发条件不调用; 另外 handoff 明确要求 **AB 会话 (带 `ARIA_COORDINATION_NO_PUSH=1`) 内跳过心跳和 `phase1_gate`**。

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  背景: 你关心的文档版本问题只有 1 处需要动手 (`VERSION` aria 行), 它是 Level 1 级别的文字修正; 但当前分支是 `#195` 的 feature 分支, 且 handoff 要求 TASK-026 (AB) 之后的提交都在 feature 上按顺序走, 所以**不建议在当前分支顺手改**。

  ➤ [1] quick-fix 修 VERSION 行 + 补检查 (推荐)
      执行: 在 master 上 B.2 → C.1 (Level 1, 无需 OpenSpec)
        (1) `VERSION` 第 24 行 `v1.73.0` → `v1.73.3`
        (2) 把 `VERSION` 子模块表的 aria 行加进 `plugin-version-arch-docs-match` (或同类) 检查的覆盖面, 否则下次发版还会漏
        (3) 提交遵循 Conventional Commits; 按 owner 09-27 裁定**不加** `Co-Authored-By` 行
      跳过: A.* (Level 1), B.3 (无架构变更)
      理由: 这是已有发布同步面上的确定性漂移, 修法唯一; 在 master 修不打乱 `#195` 的任务顺序。注意需先 `git checkout master` —— 切换前请确认当前不是 AB 进程 (AB 进程内不应改动工作区)
      代价: 多一次 master 推送 (须 owner 授权 + 双推后逐 remote `ls-remote` 核验)

  ○ [2] 并入 `#195` 的 TASK-027 发版面同步
      执行: 不单独动手; TASK-027 做 MINOR bump 时连同 `VERSION` 子模块表一起改到新版本号
      理由: TASK-027 本来就要改 `VERSION`, 一次改齐, 不多一次推送
      代价: 在那之前 `VERSION` 继续错着; 且检查缺口不修的话, 这类漏改仍会复发 —— 选这个也建议开一条 issue 记检查缺口

  ○ [3] 继续 `#195` 主线: TASK-026 Rule #6 AB
      执行: 按 09-27 handoff §2 H1 —— owner 以 `ARIA_COORDINATION_NO_PUSH=1` 新起进程, 先核 `git ls-remote origin refs/aria/coordination` 等于本地 `refs/aria/coordination`, 再按 `detailed-tasks.yaml` TASK-026 verification 逐条走
      理由: 这是 handoff 写明的下一步 (未跟踪的 `ab-results/2026-09-27-handoff-multibranch-rule6/` 目录看起来 AB 已经开跑)
      说明: 若进入 Phase B 相关步骤且不在 AB 会话, 编排层会先调用以下命令 (本次评测不执行, 仅列出):
        `python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase B --mode advisory --repo-path "/home/dev/Aria"`

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase B"; 例如「只开 issue 记 VERSION 行漂移和检查缺口, 暂不改文件」

🤔 选择 [1-4] 或输入自定义:
