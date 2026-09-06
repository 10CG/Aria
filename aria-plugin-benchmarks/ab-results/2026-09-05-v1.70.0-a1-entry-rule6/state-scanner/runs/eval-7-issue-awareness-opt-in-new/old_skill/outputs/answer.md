已按 state-scanner v3.0 机械路径扫描完成。

Step 0 `scan.py` **exit 0**（`errors[] == []`，全部 collector 采集成功），`snapshot_schema_version = "1.0"`，与 SKILL.md 契约匹配，入口断言通过。
阶段 0 中断检测：`interrupt.status = "completed"`（上一周期 `feature-dev` / `linked-issue-field-availability` 已走完 D.4，2026-09-02 收尾），**无中断需恢复**，直接进入推荐。
`git.git_operation_in_progress.operation = "none"`，无暂停中的 rebase/merge/cherry-pick，priority 0.5 安全闸未触发。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

📍 当前状态
───────────────────────────────────────────────────────────────
```
  分支: feature/a1-entry-claim-duplicate-work-guard (upstream origin/同名, ahead 0 / behind 0)
  模块: 未配置 (UPM 未启用)
  Phase/Cycle: handoff frontmatter 记为 B.2; 上一 workflow-state 已 completed
  变更: 4 文件 — 3 个 dirty 子模块 (aria / aria-orchestrator / standards) + 1 个未跟踪目录
  OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 进度 31/40)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (0.8h ago, via pointer)
```

📊 变更分析
───────────────────────────────────────────────────────────────
```
  类型: 其他 (other × 4) — 无 code / test / docs / config 类变更
  复杂度: Level 2
  架构影响: 无
  测试覆盖: ❌ 无对应测试 (本次变更也不需要)
  Skill 变更: 未检出 SKILL.md 改动 → 不触发 Rule #6 AB 区块
```

📄 需求状态
───────────────────────────────────────────────────────────────
```
  配置状态: ✅ 已配置
  PRD: prd-aria-v1.md (active) / prd-aria-v2.md (raw "Approved" → 归一 pending)
  User Stories: 21 个 (done 17, in_progress 2, approved 1, pending 1)
  OpenSpec 覆盖: snapshot 未产出覆盖率字段 (本版 collector 无此项)
  ⏸ 有 2 个 in_progress Story 待续: US-026, US-007 (规则 resume_in_progress_us, 1.88)
```

🏗️ 架构状态
───────────────────────────────────────────────────────────────
```
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02 (3 天前)
  需求链路: ✅ 完整 (PRD v1 + v2 → Architecture)
```

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
```
  活跃变更: 7 个 (全部 approved)
    - a1-entry-claim-duplicate-work-guard   ← 当前分支这一轨, 31/40
    - aria-2.0-m6-cost-model-telemetry / m6-dispatch-input-delivery / m6-e2e-resilience
    - aria-2.0-m6-release-closeout / m7-agent-lifecycle / m7-fleet-aggregation
  已归档: 142 个 | 待归档: 0 个
  ⚠️ 设计未实施 (design_deferred): 5 个
    - aria-2.0-m6-cost-model-telemetry   approved, 陈旧 58d (25/38 任务未勾)
    - aria-2.0-m6-e2e-resilience         approved, 陈旧 55d (25/40 未勾)
    - aria-2.0-m6-release-closeout       approved, 陈旧 103d (41/41 未勾)
    - aria-2.0-m7-agent-lifecycle        approved, 陈旧 65d (18/18 未勾)
    - aria-2.0-m7-fleet-aggregation      approved, 陈旧 48d (20/20 未勾)
```

🛡️ 审计状态
───────────────────────────────────────────────────────────────
```
  审计系统: ✅ 已启用
  上次审计: pre_merge — verdict PASS, 但 converged = false (R5, 2026-09-02)
  报告: .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-
        linked-issue-field-availability-aggregated.md
  ⚠️ 规则 audit_unconverged (1.9) 触发 — 建议性提示, 非阻断:
     verdict 是 PASS 但收敛标记为 false, 进 Phase C 前值得确认是「接受当前结论」还是「补一轮」
```

🔧 自定义检查
───────────────────────────────────────────────────────────────
```
  ✅ 14/14 全部通过 (0 FAIL / 0 STALE)
  issue-cache-freshness ✅ | m6-version-badge-match ✅ badge=1.69.1
  m6-claude-md-version ✅ 2.0.0 | m6-arch-doc-stale ✅ age=3d
  i18n-readme-translation-currency ✅ 3 份 @1.69.1 | claude-md-changelog-free ✅
  coordination-gate-invocation ✅ 近期 7 次真实 run_gate 调用
  config-template-key-currency ✅ | plugin-cache-currency ✅ 1.69.1
  main-project-version-consistency ✅ 1.7.5 (9 处一致)
  forgejo-app-token-liveness ✅ | linked-issue-field-availability ✅
  plugin-version-arch-docs-match ✅ | silknode-contract-deferral-expiry ✅
```

🔄 同步状态
───────────────────────────────────────────────────────────────
```
  当前分支: ahead 0 / behind 0 vs origin/feature/a1-entry-claim-duplicate-work-guard
  远程 ref 新鲜度: 1m (本次 Phase 0.5 已实拉, evidence_grade = fresh)
  多远程一致性 (enforced: origin + github), overall_parity = ✅ true
    主仓 5d9b568        — origin ✅ equal | github ✅ equal
    standards bb5d375   — origin ✅ equal | github ✅ equal
    aria ab3dbd0        — origin ✅ equal | github ✅ equal
    aria-orchestrator 92acce5 (分支 feature/m6-cost-model-telemetry)
                        — origin ✅ equal | github ❓ unknown (no_local_tracking_ref)
  gitlink 完整性: 6/6 (R × S) 全 ok — 无 orphaned gitlink
  子模块: 三个都是 workdir_vs_tree dirty、tree_vs_remote = false
          → 规则 submodule_drift 未触发; 交接注明这三处 dirty 是有意的 (gitlink bump 留给发版 8.2)

  📝 README 版本一致性: ✅ aria 子模块 README 1.69.1 == plugin.json 1.69.1
  📦 插件依赖: ✅ standards 子模块已初始化并注册
  🔗 Forgejo 配置检查: ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但 CLAUDE.local.md 缺 forgejo 配置块
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

🎫 Open Issues
───────────────────────────────────────────────────────────────
```
  平台: Forgejo (forgejo.10cg.pub) — 4 个仓库合计 47 open (⚠️ 见下方截断说明)
  数据来源: cache (6m ago) | fetched_at 2026-09-05T23:19:26Z | ttl: 15m | fetch_error: 无
  label 汇总: {bug: 1} — 其余 46 条无任何 label
```

**10CG/Aria — 20 open**（顶到 limit 上限）

```
  📌 #196 [契约][aria-orchestrator] unattended 的 Layer 1→2 env 传递三腿契约未定义
  📌 #195 state-scanner: handoff_multibranch 递归枚举但只留 basename        [bug]
  📌 #193 [反馈+询问] 同容器 git 身份漂移产生双 owner-container 串
  📌 #192 [Archive Tracker] sibling-spec-probe — 归档残留待办
  📌 #188 [bug] 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md
  📌 #184 [enhancement] aria:brainstorm 被共装插件静默绕过
  📌 #182 [缺陷] handoff frontmatter 的 status 从不收口 (31 条 5 月历史交接仍报 active)
  📌 #180 coordination claim 的 collision surface 在 30 分钟后静默失效
  📌 #178 [规范] hook 类 Spec 的 SC 须显式声明测的是哪份副本
  📌 #177 [governance] CLAUDE.md:81 发布同步面那行是漏同步面的类级根因
  📌 #176 [bug][state-scanner] AC-5 一致性检测未排除本仓不存在的 remote
  📌 #175 [governance] 契约 2 重写为「数据卫生纪律 + 法务结论适用范围声明」
          → 已关联 User Story: US-025
  📌 #174 Layer L claim 无法检测跨 track-id 的同源重叠  ← 当前这一轨的 linked issue
  📌 #173 [bug][state-scanner] gate_result: 无任何任务文件时静默 pass
  📌 #171 [知识层] 新增 convention: CLI 默认输出格式随 stdout 是否为 TTY 变化
  📌 #170 aether-build-container T4 push 凭据经 nomad var put 回显泄漏
  📌 #169 [refactor] AC-5 跨 collector 自洽检测搬出 scan.py 装配层
  📌 #168 [tracker] state-scanner-stale-refs-false-parity 归档 deferred 项
  📌 #167 FR: Forgejo API 调用层支持可插拔 HTTP 传输 (macOS curl TLS)
  📌 #165 [reliability] GitHub 镜像漏推第三次复发 → orphaned gitlink
```

**10CG/aria-plugin — 20 open**（顶到 limit 上限）

```
  📌 #169 [缺陷][Layer L] resilient_push 的 non-FF 恢复路径结构上必失败
  📌 #168 [coordination] audit-engine 轮内不触发 heartbeat
  📌 #167 [schema][Layer L] ClaimRecord 缺 swept 标记
  📌 #166 [权限面][Layer L] 跨容器定向 release 未支持
  📌 #165 [文档][phase-b-developer] B.0 的 YAML-键形态应升为标题级
  📌 #164 [增强][Layer L] unknown_schema_claims 只给 count 不给路径/身份
  📌 #163 [缺陷][文档措辞] 三处把 --sweep-stale 的 SWEEP_TTL 写成 STALE_TTL
  📌 #162 [缺陷] 汇总报告文件名约定只存在于消费方代码里 → last_audit 永久恒 null
  📌 #161 audit-engine pre_merge completeness gate 按文件名 glob 不按 spec_id 匹配
  📌 #160 [缺陷] 两个同名 lib 包在同一 pytest 进程只能绑一个 → 恒 2 collection error
  📌 #159 [规范待裁][workflow-runner] Exit condition 2.5 abort 的 status 翻转未明说
  📌 #158 [缺陷][workflow-runner] retry_count > max 的 max 从未定义
  📌 #157 [benchmark][state-scanner] ab-suite 对 Layer L / --linked-issue 段零覆盖
  📌 #156 [缺陷][phase-c-integrator] Rule #8 (b) 腿对未被领取的 main run 不可见
  📌 #154 [安全][hooks] L3 tripwire: PostToolUse 凭据形状检测-告警
  📌 #150 [benchmark] Rule #6 判据表第三行「缺一照跑」对 14/43 个 skill 不可执行
  📌 #148 [refactor] 重试循环两份实现 (pre_merge_gate.py 与 aether.py)
  📌 #146 [实现][secret-guard] ! 命令位置分支左侧无边界
  📌 #144 [可移植性][secret-guard] 非 glibc / 低版本 bash 平台两个未验证面
  📌 #143 [缺陷][secret-guard] fail-safe 判据不封闭的残余误报面
```

**10CG/aria-standards — 5 open**

```
  📌 #19 [convention] owner-container 与 claim container 段口径不统一
  📌 #18 [缺陷+enhancement] git-commit 禁止 AI 署名, 但没说与 harness 注入指令谁优先
  📌 #17 [convention] skill-benchmark-exemption: 单 Skill 局部变更的 Rule #6 AB lane 缺成文
  📌 #16 [缺陷] openspec/project.md 内部对 Level 3 交付物给出两种口径
  📌 #15 [enhancement] concurrent-session-write-safety 的 fetch 原则应扩到写操作
```

**10CG/aria-orchestrator — 2 open**

```
  📌 #31 [coordination] 自主 bot dispatch 时强制 claim — defect a 的 Layer 2 维度
  📌 #5  feat: abstract reusable "Hermes on Aether" deployment template
```

---

## 关于「哪些是阻塞性的」

这是你的核心问题，我分三层回答，**先说清哪一层是机械的、哪一层是我的判断**。

### 一、机械判定结果：0 条

state-scanner 的 `open_blocker_issues` 规则（priority 1.99）只认一件事——issue 上带 `blocker` 或 `critical` **label**。本次聚合四个仓库全部 47 条：

```
  label 汇总: {bug: 1}   ← 全部 label 就这一个
  blocker/critical 命中: 0 条  → 规则未触发, 推荐未被降级
```

也就是说，**这套仓库基本不用 label**，所以「机械阻塞检测」在这里等于恒为空——它不是在告诉你「没有阻塞项」，而是在告诉你「这个通道没有信息」。把它当成「没有阻塞」会是典型的假绿。

### 二、⚠️ 数据不完整：47 这个数字本身被静默截断了

这条必须先讲，否则上面的清单会误导你：

```
  config: state_scanner.issue_scan.limit = 20  (每仓单次拉取上限)
  实测:   10CG/Aria = 20 条, 10CG/aria-plugin = 20 条  ← 两个仓恰好各 20 = 顶到上限
  snapshot 里没有任何截断标记 (无 truncated 字段, 无 warning)
```

最近一次交接（`docs/handoff/2026-09-05-2200-...md` §2 M2）已实测过同一现象：snapshot 报 46，四仓 API 实拉合计 **65**（aria-plugin 34 / Aria 25 / aria-orchestrator 2 / aria-standards 4）。也就是说**大约还有 18 条 open issue 根本没进这份清单，而且是无声消失的**。

结论：**在把 `limit` 提上去重扫之前，「哪些是阻塞性的」这个问题在机械层面无法被完整回答。** 修法一行：

```jsonc
// .aria/config.json
"state_scanner": { "issue_scan": { "limit": 100 } }   // 或 ≥ 各仓 open 数
```

改完重跑 `/state-scanner`（缓存 ttl 15m，需要立刻生效可先删 `.aria/cache/issues.json`）。

### 三、我的启发式分级（非机械，基于标题+你「要开新 feature」这个目标）

以下是我读标题给出的判断，**不是 snapshot 字段**，请当作待核对的候选而非结论。按「会不会挡住你开新 feature 并把它交付出去」排：

**A. 会直接挡住「开发→合并→发布」这条路（建议开工前先看）**

| Issue | 为什么挡路 |
|---|---|
| Aria #165 | GitHub 镜像漏推第三次复发 → orphaned gitlink，`clone --recursive` 断裂。新 feature 一旦动子模块就会踩 |
| aria-plugin #161 | pre_merge completeness gate 按文件名 glob 不按 spec_id 匹配 → **历史报告让门恒通过**（已有真实漏拦案例）。Rule #8 的门在漏 |
| aria-plugin #162 | 汇总报告文件名约定只存在于消费方代码里 → `last_audit` 永久恒 null |
| aria-plugin #156 | Rule #8 (b) 腿对未被领取的 main run 不可见 → 分钟级 fail-open |
| Aria #173 | gate_result 无任务文件时静默 pass —「证据越少越宽松」 |
| Aria #176 | AC-5 未排除本仓不存在的 remote → 单/双 remote 混合布局下退出码恒 10 |

**B. 会挡住「多终端/并发安全地开一条新轨」（你这台机器现在正处在这个场景，见下）**

| Issue | 为什么 |
|---|---|
| aria-plugin #169 | `resilient_push` 的 non-FF 恢复路径**结构上必失败**，影响 `acquire_claim` + `heartbeat` 两条写路径 → 并发下 claim 静默丢失 |
| Aria #174 | Layer L claim 检测不到跨 track-id 的同源重叠 → 两个容器可能对同一件事各起一个 change，双方 gate 都 passed |
| Aria #180 | claim 的 collision surface 30 分钟后静默失效（heartbeat 零生产调用点） |
| Aria #182 | handoff frontmatter 的 status 从不收口，31 条 5 月的交接仍报 active → **「多 track」判据不可用** |
| Aria #193 / aria-standards #19 | 同容器 git 身份漂移产生双 owner-container 串 → collision 分类失灵 |
| aria-plugin #168 / #167 / #166 / #164 | heartbeat 盲窗、swept 标记缺失、跨容器 release、诊断字段不给身份 |
| aria-orchestrator #31 | 自主 bot dispatch 时强制 claim（Layer 2 维度） |

**C. 治理 / 规范类（不挡代码，但会让流程判断出错）**
Aria #177（CLAUDE.md 发布同步面那行是类级根因）· #175 · #178 · aria-standards #15 / #16 / #17 / #18

**D. 安全类（独立于本次 feature，但不宜久拖）**
aria-plugin #154 / #146 / #144 / #143（secret-guard 系列）· Aria #170（凭据经 `nomad var put` 回显泄漏）

**E. 跟踪 / 清理 / 增强（可延后）**
Aria #192 / #188 / #184 / #171 / #169 / #168 / #167 / #195 / #196 · aria-plugin #163 / #165 / #157 / #158 / #159 / #160 / #150 / #148 · aria-orchestrator #5

> 补充一条你多半用得上：aria-plugin **#157** 说的是 AB 套件对 Layer L 段零覆盖，aria-plugin **#150** 说的是 Rule #6 兜底对 14/43 个 skill 不可执行。若你的新 feature 涉及 Skill 改动，这两条会直接影响你能不能过 Rule #6。

---

## ⚠️ 两条进 Phase B 之前必须知道的事

**1. 本仓当前存在协调 collision（多容器同轨）**

```
  tracks_multibranch.collision.kind = self_multi_container
  分组: ["dev-claude", "simonfishgit/dev-claude"]   ← 恰好就是 Aria #193 描述的身份漂移形态
  config: state_scanner.coordination.enabled = true, mode = advisory
```

按 Layer L 编排契约，**当你确认进入 Phase B 时**（不是现在、不在只读扫描里），我会经 subprocess 调一次 advisory 闸门：

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<handoff §6 选定的 carry-id 原始串>" --phase B --mode advisory \
  --repo-path /home/dev/Aria
```

advisory = 放行 + 写推自己的 claim + 返回 surface 告警；最终仲裁仍归 reconcile（earliest `claimed_at` 胜）。本次扫描是只读的，**我没有调用它，也没有写任何 claim**。

另外交接 §3 第 5 条点名：`owner-container-identity-key-and-collision-parser`（owner `aria-runner-bot`，容器 `bfe8285d`，09-05T13:55Z 认领，linked issue 就是 Aria #193）在飞。**如果你的新 feature 落在 owner-container / collision 解析这一带，动手前先去看对方进度，别重复实现。**

**2. 交接给出的优先级与「开新 feature」有冲突，我不替你裁**

最新 handoff §6 的排序是：

```
  1. ⭐ a1-entry-claim-duplicate-work-guard 续做 (31/40)
     先决: owner 以 ARIA_COORDINATION_NO_PUSH=1 claude ... 重启会话跑 Rule #6 AB
           —— 这是会话级前置, 会话内补不上
     AB 过关 → 7.6 依赖解除 → Group 8 发版 (vNEXT = 1.70.0, 执行序 8.1 → 8.4 → 8.2)
  2. carry-issue-scan-open-count-truncation  ← 恰好就是上面第二层那个截断问题
  3. carry-resilient-push-non-ff-recovery (aria-plugin #169)
```

也就是说：当前 cycle **31/40 未完**，而你想开新 feature。这是产品级取舍，我按 Rule #10 不自行改序，把选项摆出来由你定。

---

🎯 推荐工作流
───────────────────────────────────────────────────────────────

```
  ➤ [1] 补全 issue 数据, 再回答「哪些阻塞」(推荐)
      执行: 改 issue_scan.limit (20 → 100) → 删 .aria/cache/issues.json → 重跑 /state-scanner
            → 对候选阻塞项跑 /issue-triage 逐条核对
      理由: 你的问题现在答不完整 —— 47 是截断后的数, 约 18 条不可见, 且 label 通道为空
            使机械 blocker 检测恒空。这一步同时闭掉 handoff §6 第 2 条。成本约 10 分钟
      不动: 任何代码 / 分支

  ○ [2] full-cycle — 直接开新 feature
      执行: A.1 (spec-drafter, Rule #1 要 Level 2/3 OpenSpec) → A.2 → A.3 → B.1 → B.2 → C.1 → C.2
      前置: 进 B.1 前跑 phase1_gate advisory 认领 (当前有 self_multi_container collision)
      理由: 符合你的原始意图; 但要接受「在 47 条(实为 ~65 条)未分诊的 backlog 上再叠一轨」
      风险: 上面 A 组那 6 条门缺陷会在 C.2 合并时找上门

  ○ [3] 续做 a1-entry-claim-duplicate-work-guard (handoff §6 排第 1)
      执行: Rule #6 AB (H1) → 7.6 (H2) → Group 8 发版 8.1 → 8.4 → 8.2
      阻塞: ⛔ ARIA_COORDINATION_NO_PUSH 是会话级前置, 本会话内补不上
            需 owner 以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启
      理由: 交接把它排第一; 31/40, 发版在望 (vNEXT = 1.70.0)

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase B" 或直接说你想先看哪几个 issue
```

🤔 选择 [1-4] 或输入自定义：

---

<sub>本次扫描：`scan.py` exit 0，`errors[] = []`，snapshot schema 1.0；issue 数据来自 cache（6m ago，ttl 15m，未过期）。全程未写任何 claim、未推任何 ref、未改动仓库文件。</sub>
