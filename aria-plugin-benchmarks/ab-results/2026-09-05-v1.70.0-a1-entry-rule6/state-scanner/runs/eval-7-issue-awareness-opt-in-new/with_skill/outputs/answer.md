已按 state-scanner v3.0 机械路径跑完 Step 0 (`scan.py`, **exit 0 / `errors[]` 为空**), 并读了 snapshot + 最新 handoff。下面是十区块报告 —— 你关心的 Issues 在 §9, **但请先看 §9 顶部那条截断警告, 它直接决定"哪些是阻塞性的"这个问题现在能不能被可靠回答**。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 📍 当前状态

```
  分支: feature/a1-entry-claim-duplicate-work-guard (upstream origin/同名, ahead 0 / behind 0)
  模块: — (UPM 未配置)
  Phase/Cycle: — (UPM 未配置; 由 OpenSpec + handoff 推断 = Phase B.2)
  变更: 4 个 (3 个 dirty 子模块 aria/standards/aria-orchestrator + 1 个 untracked 目录)
  OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 31/40 tasks)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (0.75h ago, via pointer) — 已读
  git 中间态: none (无 rebase/merge/cherry-pick 暂停)
  中断状态: workflow-state.json 存在但 status=completed (上个 cycle linked-issue-field
            2026-09-02 已收尾), branch_anchor_match=false — 非中断, 不触发恢复流程
```

> 三个子模块的 dirty 是**有意的** (handoff §0 第 1 条: gitlink bump 归 TASK-038/8.2, 要等各自合 master 之后), **不要 `git add`**。

## 📊 变更分析

```
  类型: 其他 (other 4) — code 0 / test 0 / docs 0 / config 0
  复杂度: Level 2
  架构影响: 无
  测试覆盖: — (本次无代码变更)
  Skill 变更: 未检出 (skill_changes.detected=false) ⇒ 本次扫描不触发 Rule #6 AB 区块
```

## 📄 需求状态

```
  配置状态: ✅ 已配置 (docs/requirements/)
  PRD: prd-aria-v1.md (Active) / prd-aria-v2.md (Approved)
  User Stories: 21 个 — done 17 / in_progress 2 / approved 1 / pending 1
  优先项 (priority_items): US-026 (in_progress, v2.0 M6/M7) · US-007 (in_progress) · US-003 (pending)
```

> ⚠️ 小提醒: `prd-aria-v2.md` 的 raw status 是 `Approved (Draft → Approved 2026-04-11 …)`, 但归一后落 `pending` —— 这是 `_normalize_status` 首段截断的边界表现, 不是 PRD 真的没批。`prd_draft_blocking` 规则**未**触发 (它认 Draft, 此处不是 Draft)。

## 🏗️ 架构状态

```
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active | 最后更新: 2026-09-02
  需求链路: ✅ 完整 (PRD v1 + PRD v2 → Architecture)
```

## 📋 OpenSpec 状态

```
  活跃变更: 7 个 (全部 approved)
    - a1-entry-claim-duplicate-work-guard   ← 当前轨, 31/40
    - aria-2.0-m6-cost-model-telemetry
    - aria-2.0-m6-dispatch-input-delivery
    - aria-2.0-m6-e2e-resilience
    - aria-2.0-m6-release-closeout
    - aria-2.0-m7-agent-lifecycle
    - aria-2.0-m7-fleet-aggregation
  已归档: 142 个 | 待归档: 0 个
  ⚠️ 设计未实施 (design_deferred): 5 个
    - aria-2.0-m6-release-closeout   approved  41/41 未勾选  staleness 103 天
    - aria-2.0-m7-agent-lifecycle    approved  18/18 未勾选  staleness  65 天
    - aria-2.0-m6-cost-model-telemetry approved 25/38 未勾选 staleness  58 天
    - aria-2.0-m6-e2e-resilience     approved  25/40 未勾选  staleness  55 天
    - aria-2.0-m7-fleet-aggregation  approved  20/20 未勾选  staleness  48 天
```

> 这条对你"开发新 feature"的决策**直接相关**: 已经有 5 份批准但未实施的设计压在队列里, 其中两份 staleness 已过 100/65 天。新起一条 feature 前值得先确认它不是这 5 份里某一份的重复。

## 🛡️ 审计状态

```
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
  活跃检查点: post_spec, post_planning (其余 5 个 off)
  上次审计: pre_merge — PASS, 但 converged=false (R5, 5 轮耗尽 max_rounds 未稳定)
            2026-09-02T18:10Z · linked-issue-field-availability
```

> ⚠️ 命中规则 `audit_unconverged` (priority 1.9, 置信度 75%): verdict 是 PASS 但**收敛判定为 false** —— 是"轮数耗尽"而非"结论稳定"。handoff 记为「降级三选一待 owner (H1b)」, 仍未裁。

## 🔧 自定义检查

```
  ✅ 14/14 全部通过 (0 FAIL / 0 STALE / 0 SKIP)
     issue-cache-freshness · silknode-contract-deferral-expiry · m6-version-badge-match
     m6-claude-md-version · m6-arch-doc-stale · i18n-readme-translation-currency
     claude-md-changelog-free · coordination-gate-invocation · config-template-key-currency
     plugin-cache-currency · main-project-version-consistency · forgejo-app-token-liveness
     linked-issue-field-availability · plugin-version-arch-docs-match
```

## 🔄 同步状态

```
  当前分支: ahead 0 / behind 0 vs origin/feature/a1-entry-claim-duplicate-work-guard
  remote refs 新鲜度: 1m (Phase 0.5 remote_refresh 本轮真实 fetch, evidence_grade=fresh)
  多远程 parity: ✅ overall_parity = true
    主仓        origin ✅ equal 5d9b568 | github ✅ equal 5d9b568
    standards   origin ✅ equal bb5d375 | github ✅ equal bb5d375
    aria        origin ✅ equal ab3dbd0 | github ✅ equal ab3dbd0
    aria-orch.  origin ✅ equal 92acce5 | github ⚪ unknown (no_local_tracking_ref)
  gitlink 完整性: ✅ 6/6 ok (3 子模块 × 2 remote, 无 orphaned)
  子模块 drift: 3/3 tree_vs_remote=false (workdir_vs_tree=true = 上面说的有意 dirty)

  📝 README 版本一致性: ✅ aria 子模块 plugin.json 1.69.1 == README 1.69.1
  📦 插件依赖: ✅ standards 子模块已初始化并注册
  🔗 Forgejo 配置检查: ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但配置缺失
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
```

> `aria-orchestrator` 的 github `unknown` 属 benign (那是另一条轨 `feature/m6-cost-model-telemetry` 尚未推 github), `evidence_grade=fresh` ⇒ 既不触发 `multi_remote_drift` 也不触发 `has_unpublished_branch`。

## 🎫 Open Issues

```
  平台: Forgejo — snapshot 报 47 open (跨 4 repo 聚合, scan_submodules=true)
  数据来源: cache (6m ago) | ttl: 15m | fetch_error: null
  label 分布: bug × 1 —— 其余 46 条**完全没有 label**
```

### ⛔ 第一件事: 这份清单是**被静默截断**的, 不能用来判断"有没有阻塞项"

我拿 Forgejo API 逐仓复核了一遍真实 open 数, 与 snapshot 对不上:

| 仓库 | snapshot 报 | API 实际 | 被吞掉 |
|------|------------|---------|--------|
| 10CG/Aria | 20 | **26** | 6 |
| 10CG/aria-plugin | 20 | **41** | 21 |
| 10CG/aria-orchestrator | 2 | 2 | 0 |
| 10CG/aria-standards | 5 | 5 | 0 |
| **合计** | **47** | **74** | **27 (36%)** |

根因: `.aria/config.json` 的 `state_scanner.issue_scan.limit = 20` 是**逐仓上限**, 两个大仓恰好顶满 20 —— 而 snapshot **不带任何截断标记** (没有 `truncated` 字段, `fetch_error` 是 `null`, `warning` 是 `null`)。也就是说, 它把"我只看到 20 条"和"这里一共就 20 条"呈现成了同一件事。

这不是新问题: 上一份 handoff §2 M2 已实测过一次 (当时 46 报 / 65 实), **至今仍未开单**。今天这轮是第二次复现, 且差额扩大到 27 条。它和 Aria#182 / Aria#173 是同一族("证据越少反而越宽松")。

**对你的问题的直接影响**: 被吞掉的 27 条里, 至少有 4 条我判断优先级不低于清单里的任何一条 —— 包括一条 secret 泄漏 (`Aria#136`) 和一条"状态扫描器自己报假绿" (`aria-plugin#110`)。所以下面的分级我用的是**API 全量 74 条**, 不是 snapshot 的 47 条。

### 机械规则的判定 (先说清楚它为什么等于没说)

`open_blocker_issues` 规则 (priority 1.99) 找 `blocker` / `critical` label —— **零命中, 未触发**。但这不是"没有阻塞项"的证据: 这四个仓**根本没在用严重度 label** (74 条里只有 1 条带 label, 内容是 `bug`)。规则在这个语料上**结构性恒绿**, 属于零信息量, 不能当作正证据。

所以下面这份分级是我**按 issue 内容**做的启发式判断, 不是机械输出 —— 你可以推翻任何一条。

### 分级 A — 真正卡住"现在能不能往前走"的 (3 条 + 1 个非 issue 的门)

| 项 | 为什么卡 |
|---|---|
| **(非 issue) Rule #6 AB 的会话级前置** | `ARIA_COORDINATION_NO_PUSH` 实测 UNSET, **会话内补不上**。这才是当前 v1.70.0 发版的真正阻塞点, 不是任何一条 issue。处置见下方推荐 [2]。 |
| **aria-plugin#169** resilient_push non-FF 恢复路径结构上必失败 | 影响 `acquire_claim` + `heartbeat` **两条 claim 写路径**; 多容器并发时 claim 静默丢失 —— 而多容器并发正是 Layer L 存在的理由。已开单未修。 |
| **aria-plugin#135** 认领机制三处缺口致跨容器重复劳动 4 次 | **被截断掉了**。它是当前这条轨 (a1-entry-claim-duplicate-work-guard) 的母问题, 却没出现在扫描结果里。 |
| **aria-plugin#107** heartbeat 生产接线 / heartbeat_at 冻结在 acquire | **被截断掉了**。同域, 且与 #169 / #168 构成同一个失效面。 |

> 值得单独指出: 与当前轨最相关的三条 (#135 / #107 / #109) **恰好全在被截断的那 27 条里**。截断不是随机丢失, 它按 issue number 降序取前 20, 于是**老的、更根本的问题系统性地看不见**。

### 分级 B — 安全 / 凭据 (不卡开发, 但有时间成本, 建议插队)

| 项 | 内容 |
|---|---|
| **Aria#136** | cost-sentinel 在 INFO 日志打印完整 Feishu webhook URL (secret-in-logs) — 需轮换 + 脱敏。**被截断掉了**。 |
| **Aria#170** | aether-build-container T4 push 凭据经 `nomad var put` 回显泄漏 |
| **Aria#151** | 两个 10cg-ci-bot token 归属待确认。**被截断掉了**。 |
| **aria-plugin#138/139/140/141/142/143/144/146** | secret-guard 家族 8 条 (跨段 fail-open / 外壳逃逸 / 切分记号 / 块结构欠拦 / 非 glibc 可移植性) — 其中 #138–#142 **全被截断掉了** |

### 分级 C — 假绿 / 闸门失效 (会让你误判"没问题", 危害等同分级 A 但更隐蔽)

| 项 | 内容 |
|---|---|
| **aria-plugin#110** | `sync_status` 撒谎: 陈旧 remote-tracking ref 下报 `parity=equal` / `overall_parity=true` —— **就是本报告 §8 那个绿勾的可信度问题**。**被截断掉了**。 |
| **aria-plugin#161** | audit-engine pre_merge completeness gate 按文件名 glob 不按 spec_id 匹配 ⇒ 门恒通过 (真实漏拦案例) |
| **aria-plugin#162** | 汇总报告文件名约定只存在于消费方代码里 ⇒ `last_audit` 可能永久恒 null |
| **aria-plugin#156** | Rule #8 (b) 腿对未被领取的 main run 不可见 ⇒ 分钟级 fail-open |
| **Aria#173** | gate_result 无任务文件时静默 pass (证据越少越宽松) |
| **Aria#176** | AC-5 一致性检测未排除本仓不存在的 remote ⇒ 退出码恒 10 |
| **Aria#188** | 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md |
| **Aria#182** | handoff frontmatter 的 status 从不收口 —— **本轮实测佐证: `tracks_multibranch` 里有 106 条 track 仍报 `active`**, 其中大量是 5 月的历史交接。「多 track」判据事实上不可用。 |
| **(未开单)** | 本报告刚复现的 `issue_scan` 静默截断本身 |

### 分级 D — 其余按主题 (不阻塞, 队列项)

- **协调 / Layer L**: aria-plugin#163 (SWEEP_TTL 措辞) · #164 (unknown_schema_claims 缺路径) · #166 (跨容器定向 release) · #167 (ClaimRecord swept 标记) · #168 (audit-engine 轮内不触发 heartbeat) · #109 (claim 强制点在成本点下游, 被截断) · aria-orchestrator#31 · aria-standards#19
- **benchmark / Rule #6**: aria-plugin#150 (判据表兜底对 14/43 skill 不可执行) · #157 (ab-suite 对 Layer L 零覆盖) · #127 · #117 (被截断) · aria-standards#17
- **规范 / governance**: Aria#175 (关联 **US-025**) · #177 (CLAUDE.md:81 发布同步面四错一行) · #178 · #171 · aria-standards#15/#16/#18
- **可靠性 / 发布**: Aria#165 (GitHub 镜像漏推第三次复发, orphaned gitlink) · #196 (Layer 1→2 env 三腿契约) · #195 · #193 · #192 · #184 · #180 · #174 · #169 · #167
- **功能 / 采纳**: Aria#5 (Pulse 集成, 被截断) · #59 · #120 · #164 · aria-orchestrator#5

### 关联性

`issue_status.items[]` 里 **linked_us / linked_openspec 命中率极低** —— 47 条里只有 1 条有关联 (`Aria#175 → US-025`), 其余全为 `null`。启发式靠正文里出现 `US-NNN` 或 change 名, 而这批 issue 的正文基本不写这两样。所以"这条 issue 属于哪个 Spec"目前得靠人读。

## 🎯 推荐工作流

**先说明两件影响选择的事** (来自 handoff, 不是机械字段):

1. **本容器持有一条 active claim**: `a1-entry-claim-duplicate-work-guard` (owner `simonfish/023236f2`, phase B.2), 上次 heartbeat `2026-09-05T21:40:06Z`, **sweep 死线 `2026-09-06T21:40Z`**。本次扫描是只读的, **没有**替你刷心跳。要刷请**先 fetch 再刷** (顺序反了会被强制 fetch 冲掉, 已有实证):
   ```bash
   git fetch origin '+refs/aria/coordination:refs/aria/coordination'
   python3 -B aria/skills/state-scanner/scripts/phase1_gate.py \
     --raw-track-id "a1-entry-claim-duplicate-work-guard" \
     --phase A.1 --heartbeat-only --repo-path /home/dev/Aria
   ```
2. **`tracks_multibranch.collision.kind = self_multi_container`** (组: `dev-claude` / `simonfishgit/dev-claude`), 且 `coordination.enabled=true` ⇒ 你**确认进入 Phase B 时**, 我会经 `phase1_gate` CLI 跑一次 advisory 认领闸门 (放行 + 写推 claim + 返回 surface 告警), 不是现在跑。另有一条在飞的轨 `aria-2-0-m6-dispatch-input-delivery` (`aria-runner-bot/bfe8285d`, B.2)。

```
  ➤ [1] fix-issue-scan-truncation (推荐)
      执行: A.1 (Level 2 proposal) → B.1 → B.2 → C.1
      理由: 你这次的问题是"哪些 issue 是阻塞性的", 而现在**这个问题答不可靠** —— 扫描
            少给了 36% 的 issue 且零告警, 被吞掉的恰恰包含一条 secret 泄漏和一条
            "扫描器自报假绿"。handoff §6 优先级 2 点名的就是这条, 且它不受 AB 门阻塞。
            最小修复面: limit 语义改为"逐仓上限并在顶满时置 truncated 标记", 或分页拉全量。
      置信度: 中高 — 缺陷已两次实测复现 (46/65 → 47/74), 但尚无 issue 编号

  ○ [2] 续做 a1-entry-claim-duplicate-work-guard (31/40)
      执行: Group 7 (Rule #6 AB) → 7.6 → Group 8 发版 (8.1 → 8.4 → 8.2, vNEXT = 1.70.0)
      ⛔ 前置阻塞: `ARIA_COORDINATION_NO_PUSH` 未设, **本会话内补不上**。
         需以 `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话后, 经 /skill-creator
         跑六个套件。跑完必做 `git fetch origin +refs/aria/coordination:refs/aria/coordination`
         清理合成 claim —— 且**清理之后**才刷本轨 heartbeat (强制 fetch 会连真 claim 一起抹掉)。
      理由: handoff §6 优先级 1; 但今天在这个会话里推不动

  ○ [3] 开新 feature (你原本的意图)
      执行: A.1 → A.2 → A.3 → B.1 → B.2 → C.1 → C.2 → D.1 → D.2 (full-cycle)
      ⚠️ 三点提醒:
         a. 队列里已有 **5 份 approved 未实施**的设计 (staleness 48-103 天), 起新轨前
            先确认不是其中之一的重复;
         b. 本容器仍持 a1-entry 的 active claim。要么先 release 它, 要么接受两条轨并存
            (进 Phase B 时闸门会 advisory 告警, 不阻断);
         c. 建议先做 [1] —— 否则新 feature 的"有没有相关 open issue"这个前置调研,
            用的还是那份少 36% 的清单。
      置信度: 低 — 需求未给出, 无法匹配 feature_with_spec (那需要已有 approved Spec)

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase B" 或直接说你想做的事
```

**同时命中但未选为主推荐的降级提示**:
- `audit_unconverged` (1.9): pre_merge R5 `converged=false` 待 owner 三选一裁定 (handoff H1b)
- `resume_in_progress_us` (1.88): US-026 / US-007 处于 in_progress, 可续做

🤔 选择 [1]-[4] 或输入自定义:
