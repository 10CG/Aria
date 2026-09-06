已执行 Step 0 机械扫描 (`scan.py`, **exit 0**, `errors[] = []`, `snapshot_schema_version = "1.0"`), 下面是完整状态报告 + 你问的两件事的答案。

**直接回答你的问题**: 是的, 有遗漏 —— `forgejo_config.config_status = **missing**`。本仓 `origin` 指向 `forgejo.10cg.pub`, 但仓库根**没有** `CLAUDE.local.md`。state-scanner 是只读的, **不会**替你把这个文件建出来, 只报状态 + 建议。设置办法见文末「如何设置 Forgejo 集成」。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/a1-entry-claim-duplicate-work-guard (HEAD 5d9b568)
  模块: — (UPM 未配置)
  Phase/Cycle: — (UPM 未配置; .aria/workflow-state.json = completed, 上一 cycle
                linked-issue-field-availability 已收尾至 D.4)
  变更: 4 个 (3 个 dirty 子模块指针 aria / aria-orchestrator / standards
             + 1 个未跟踪目录 aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/)
  OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 进度 31/40)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (0.8h ago, via pointer)

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: other × 4 (code 0 / test 0 / docs 0 / config 0)
  复杂度: Level 2
  架构影响: 无
  测试覆盖: ❌ 无对应测试变更
  Skill 变更: 未检出 (`changes.skill_changes.detected = false`) → 本次不触发 Rule #6 AB 判定

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置
  PRD: prd-aria-v1.md (Active) / prd-aria-v2.md (Approved — 归一为 pending)
  User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
  优先项 (priority_items): US-026 (in_progress) · US-007 (in_progress) · US-003 (pending)
  OpenSpec 覆盖: ⚠️ 不可机械计算 — Story 条目只有 id/path/status, snapshot 无 Story↔OpenSpec
                 链接字段 (与 Aria#188 的 `active_change_not_in_upm` 恒亮属同一类缺链)

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02
  需求链路: ✅ PRD → Architecture 完整 (parent: prd-aria-v1.md, 另关联 v2)

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 7 个 (approved: 7)
    a1-entry-claim-duplicate-work-guard · aria-2.0-m6-cost-model-telemetry
    aria-2.0-m6-dispatch-input-delivery · aria-2.0-m6-e2e-resilience
    aria-2.0-m6-release-closeout · aria-2.0-m7-agent-lifecycle
    aria-2.0-m7-fleet-aggregation
  已归档: 142 个
  待归档: 0 个
  ⚠️ 设计未实施 (design_deferred): 5 个
    - aria-2.0-m6-release-closeout   approved  103 天  (41/41 任务未勾)
    - aria-2.0-m7-agent-lifecycle    approved   65 天  (18/18 未勾)
    - aria-2.0-m6-cost-model-telemetry approved 58 天  (25/38 未勾)
    - aria-2.0-m6-e2e-resilience     approved   55 天  (25/40 未勾)
    - aria-2.0-m7-fleet-aggregation  approved   48 天  (20/20 未勾)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
  活跃检查点: post_spec, post_planning (其余 5 个显式 off — 这是 owner 的配置决定,
              我不会自行开关或跳过, CLAUDE.md 规则 #10)
  上次审计: pre_merge — PASS, 但 converged=false (R5 耗尽轮数, 2026-09-02T18:10Z)
            报告: .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-…-aggregated.md

🔧 自定义检查
───────────────────────────────────────────────────────────────
  14/14 全部 ✅ (0 FAIL / 0 STALE), 其中与本次提问直接相关的两条:
  ✅ forgejo-app-token-liveness: OK   ← Forgejo token 本身是活的
  ✅ issue-cache-freshness: OK
  其余: silknode-contract-deferral-expiry · m6-version-badge-match · m6-claude-md-version ·
        m6-arch-doc-stale · i18n-readme-translation-currency · claude-md-changelog-free ·
        coordination-gate-invocation · config-template-key-currency · plugin-cache-currency ·
        main-project-version-consistency · linked-issue-field-availability ·
        plugin-version-arch-docs-match — 均 OK

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/a1-entry-claim-duplicate-work-guard
            (与 origin/同名 同步, ahead 0 / behind 0, evidence_grade=fresh)
  远程引用: 1m 前同步 (Phase 0.5 remote_refresh 8 条 leg, 0 skipped)
  多远程 parity: ✅ overall_parity = true (enforced: origin + github, 无待推, 无不可达)
    主仓  @5d9b568 — origin ✅ equal (fresh) / github ✅ equal (fresh)
    standards @bb5d375 — origin ✅ equal / github ✅ equal
    aria      @ab3dbd0 — origin ✅ equal / github ✅ equal
    aria-orchestrator @92acce5 (分支 feature/m6-cost-model-telemetry)
        — origin ✅ equal / github ⚠️ **unknown** (reason: no_local_tracking_ref)
          ↳ 逐条点名而非只报汇总: 这条不是 "equal", 是 "没有证据"。该分支属另一条在飞的
            track (M6 遥测), 本轨未动它。
  gitlink 完整性: ✅ 6/6 ok (3 子模块 × 2 remote), 0 orphaned / 0 orphan_unverified
  子模块工作区: 3 个 workdir_vs_tree=true (指针 dirty) —— 与 handoff §0 一致, **有意保留**
                (gitlink bump 归 8.2, 要等各自合 master 之后), 不要 `git add`
  交接位置: ✅ docs/handoff/ canonical, misplaced_files = 0
  跨 worktree: 仅 1 个 worktree, 无 "global_latest_elsewhere" —— 无需切树

  📝 README 版本一致性
    ✅ aria 子模块: plugin.json 1.69.1 == aria/README 1.69.1
    ℹ️ 主仓 README: 未解析出版本号 (`readme.root.version = null`) — 见下方「其他配置缺口」

  📦 插件依赖
    ✅ standards 子模块: 已注册 + 已初始化

  🔗 Forgejo 配置检查
    ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md
       建议: 运行 /forgejo-sync 可引导创建配置 (需确认)

🎫 Open Issues
───────────────────────────────────────────────────────────────
  平台: Forgejo — 47 open (4 仓聚合)
    10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 5 · 10CG/aria-orchestrator 2
  📌 Aria #195  state-scanner: handoff_multibranch 递归枚举但只留 basename  [bug]
  📌 Aria #196  [契约] unattended 的 Layer 1→2 env 传递三腿契约未定义
  📌 Aria #193  同容器 git 身份漂移产生双 owner-container 串
  📌 aria-plugin #169  resilient_push 的 non-FF 恢复路径结构上必失败 (影响 claim 两条写路径)
  📌 aria-standards #19  owner-container 与 claim container 段口径不统一
  数据来源: cache (2026-09-05T23:19:26Z, 约 6m ago) | ttl: 15m | 无 fetch_error
  ⚠️ **计数存疑**: Aria 与 aria-plugin **恰好各 20**, 等于 config `issue_scan.limit = 20`
     顶格且无截断标记 —— 上一份 handoff (§2 M2) 实测四仓真实合计 **65**。所以 "47 open"
     应读作 "≥47"。这是一个配置缺口, 见下。

🌐 多终端协调 (advisory)
───────────────────────────────────────────────────────────────
  collision.kind = self_multi_container (分组: dev-claude / simonfishgit/dev-claude)
  coordination.enabled = true, mode = advisory
  ℹ️ 本次是只读扫描, **未**调用 phase1_gate —— 按契约闸门只在你确认进入 Phase B 时才跑。
     真要进 Phase B 前, 请先按 handoff §3 第 4 条 "先 fetch 再刷 heartbeat" 的顺序刷一次
     claim (本轨 sweep 死线 2026-09-06T21:40Z)。
```

---

## 一、遗漏的配置 (按重要度)

**[1] 🔴 Forgejo API 访问未配置 — 你问的那个, 已确认**

| 字段 | 值 |
|------|-----|
| `forgejo_remote_detected` | `true` |
| `instance` | `forgejo.10cg.pub` |
| `config_status` | **`missing`** |
| `suggestion` | 运行 `/forgejo-sync` 可引导创建配置 (需确认) |

我另做了一次独立核实 (不是只信 snapshot): `git remote -v` 的 origin 是
`ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git`, 而 `ls CLAUDE.local.md` 报 No such file。
两边一致。

**[2] 🟡 `CLAUDE.local.md` 没有被 gitignore —— 建文件之前必须先补**

我实测 `git check-ignore -v CLAUDE.local.md` 返回 rc=1 (不匹配任何规则), `.gitignore` 里
也搜不到 `CLAUDE.local`。也就是说, 你现在照着建出这个文件, 它会以**未跟踪文件**的身份出现在
`git status` 里, 一次 `git add -A` 就进仓了。**先补 .gitignore, 再建文件** —— 顺序反了,
本地配置 (以及任何不小心写进去的凭据) 就有入库风险。

**[3] 🟡 `issue_scan.limit = 20` 太小, 且截断无标记**

Aria 与 aria-plugin 各报恰好 20 条 = 顶到上限。collector 没有输出 "被截断" 的标记, 所以
`open_count` 会静默少报 (上一份 handoff 实测: 报 46 vs 实 65)。这既是配置值偏小, 也是
collector 的缺陷 (handoff §2 M2 记为 "仍未开单")。**这条不用我改配置** —— 调 `limit` 是
你的决定, 我只报告。

**[4] 🟢 UPM 未配置 (`upm.configured = false`)**

后果不是报错而是**恒亮 advisory**: `consistency_check` 会对 7 个活跃变更持续报
`active_change_not_in_upm` (Aria#188 在册)。当前不阻塞任何流程。

**[5] 🟢 主仓 README 版本号解析不出 (`readme.root.version = null`)**

`main-project-version-consistency` 与 `m6-version-badge-match` 两条自定义检查都是 pass, 所以
不是版本不一致, 而是 collector 没从主仓 README 里抓到可比的版本串。低优先级。

**明确不算遗漏的**: 5 个 `off` 的审计检查点 (post_brainstorm / mid_implementation /
post_implementation / pre_merge / post_closure) 是 `.aria/config.json` 里的显式配置决定, 不是
漏配。我不会自行开启或跳过已启用的闸门 (CLAUDE.md 规则 #10)。

---

## 二、Forgejo 检测是怎么做的 (你能预期它什么时候报什么)

Phase 1.14 `forgejo_config` collector, 三步, 输出四态**互斥**:

1. 跑 `git remote get-url origin`, 看 URL 里有没有已知 Forgejo 主机名。已知主机名的解析优先级是
   `ARIA_FORGEJO_HOSTS` 环境变量 (逗号分隔) > `.aria/config.json` 的
   `state_scanner.issue_scan.platform_hostnames.forgejo` > 内置默认 `forgejo.10cg.pub`。
   SSH (`ssh://git@host/…`, `git@host:…`) 与 HTTPS 两种写法都能识别。
   **注意它只看 `origin`** —— 本仓的 `github` remote 不参与这一判定。
2. 命中 → 查仓库根有没有 `CLAUDE.local.md`。没有 → `config_status: missing`。
3. 有 → 查文件里有没有 `forgejo:` 这个 YAML 顶层键 (半角 `:` 和全角 `：` 都认, 允许 `>` 引用
   前缀), 或 `# forgejo` ~ `### forgejo` 这样的 Markdown 标题 (大小写不敏感)。
   有 → `configured`; 没有 → `incomplete`。
   ⚠️ 关键细节: **围栏代码块 (三反引号包起来的部分) 会先被剔除再匹配** —— 你把一段示例 YAML
   贴进 CLAUDE.local.md 当参考, 不会被误判成 "已配置", 建议提示也就不会消失。

四态对应的输出行:

| config_status | 输出 |
|---------------|------|
| 远程不是 Forgejo | 整个 🔗 区块**不显示** (非 Forgejo 项目零噪音) |
| `missing` | ⚠️ 检测到 Forgejo 远程 (host) 但缺少 CLAUDE.local.md → 建议 `/forgejo-sync` 创建 |
| `incomplete` | ⚠️ CLAUDE.local.md 存在但缺少 forgejo 配置块 → 建议 `/forgejo-sync` 追加 |
| `configured` | ✅ Forgejo 配置: 已配置 (host) |

两个 fail-soft 保证: 任何 git 错误 / 超时 / 文件系统错误都会塌缩成 "不是 Forgejo 项目"
(整块静默跳过), 绝不中断扫描; 以及 —— **state-scanner 全程只读, 不会自动帮你创建或修改
`CLAUDE.local.md`**。创建是 `/forgejo-sync` 的职责, 且需要你确认。

---

## 三、如何设置 Forgejo 集成

**推荐路径 (引导式)**

```
/forgejo-sync
```

(在 Aria 仓内可直调; 装成 Plugin 的其他项目用 `/aria:forgejo-sync`。) 它会引导创建
`CLAUDE.local.md` 并写入 forgejo 配置块 —— 需要你确认, 不会静默落盘。

**手工路径 (你想自己控制内容时)**

1. **先补 `.gitignore`** (上面 [2] 那条):
   ```
   # 本地私有配置, 不提交
   CLAUDE.local.md
   ```
2. 在仓库根建 `CLAUDE.local.md`, 写一个**顶层** `forgejo:` 键。别把它包进三反引号围栏 ——
   围栏内的内容会被检测器当成文档示例剔除, 结果仍是 `incomplete`。大致形状 (字段以
   `/forgejo-sync` 实际引导的为准):
   ```
   forgejo:
     instance: https://forgejo.10cg.pub
     owner: 10CG
     repo: Aria
   ```
3. **凭据不写进这个文件** (CLAUDE.md 规则 #7 / `standards/conventions/secret-hygiene.md`):
   token 走环境变量 / `.env` / Nomad Variables, 文件里只放非敏感的 instance / owner / repo。
   本仓调 Forgejo API 走 CF Access 后面的 CLI wrapper, 不需要在配置文件里放 token:
   ```bash
   forgejo GET /repos/10CG/Aria/pulls
   ```
   顺带一提: `forgejo-app-token-liveness` 这条自定义检查现在是 ✅, 说明 token 侧本身是活的,
   缺的**只是**这个本地配置文件。
4. 重跑 `/state-scanner` 验证 —— 🔗 区块应变成
   `✅ Forgejo 配置: 已配置 (forgejo.10cg.pub)`。

---

## 🎯 推荐工作流

  ➤ **[1] 补 Forgejo 配置** (推荐 — 对应你这次的意图)
      执行: `.gitignore` 补 `CLAUDE.local.md` → 跑 `/forgejo-sync` → 重跑 `/state-scanner` 验证
      理由: 唯一一条 ⚠️ 级配置缺口, 影响面小、可当场闭环; 且 gitignore 那步有顺序要求,
            适合现在一起做掉

  ○ **[2] 续做当前 cycle: a1-entry-claim-duplicate-work-guard (31/40)**
      来源: 最新 handoff §6 的首选项 (0.8h 前写的)
      ⛔ **前置未满足**: Rule #6 AB 阻塞于**会话级**前置 —— `ARIA_COORDINATION_NO_PUSH`
         当前 UNSET, 会话内 `export` 补不上 (只影响单个 Bash 子进程, 改不了 subagent 继承
         环境)。需要你以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话。
         这**不是** Rule #6 豁免, 是执行条件不具备。
      解除后的顺序: AB (H1) → 7.6 依赖解除 (H2) → Group 8 发版 (vNEXT = 1.70.0, 序 8.1 → 8.4 → 8.2)
      注: 进 Phase B 前先按 handoff §3 第 4 条 "先 fetch 再刷" 刷 heartbeat

  ○ **[3] 处理 carry-forward 缺陷**
      执行: aria-plugin#169 (`resilient_push` non-FF 恢复路径结构必失败, 影响 claim 两条写路径)
            或 `issue_scan.open_count` 静默截断 (M2, 尚未开单)
      理由: #169 优先级不低且已定位到 `lib/failure_handlers.py` + `lib/coordination_ref.py:1339`

  ○ **[4] 自定义组合**
      输入格式: "B.2 + C.1" 或 "Phase B"

🤔 选择 [1-4] 或输入自定义:
