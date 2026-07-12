---
track-id: state-scanner-stale-refs-false-parity
linked-issue: 10CG/aria-plugin#110
owner-container: aria-runner-bot/023236f2
phase: A.1-postspec-R4
status: active
updated-at: 2026-07-12
---

# Session Handoff — state-scanner「陈旧 ref 假同步」缺陷: 发现 + Spec + post_spec R1-R4 + 拆 3 Spec

> owner /goal: 「1. 同步本地和远程仓库确保完全同步 2. 遵循 aria 规范查看项目状态给建议」。
> 状态扫描发现真缺陷 → owner 选定该线 → 走完 Phase A.1 + 4 轮 5-agent post_spec 对抗审计。

## §0 入口 (新 session 优先读)

- **本 session 干了什么**:
  1. **完全同步** 4 仓 × 2 远程 (含补齐 `aria-orchestrator` 落后 32 commit 的 github 镜像)。
  2. **发现并实证 state-scanner 一个真缺陷** —— 十步循环统一入口会报**假的「已同步」**。本 session 自身即受害者。
  3. **Phase A.1 完成**: DEC + 3 个 Spec (拆分后)。
  4. **post_spec 收敛审计 4 轮 × 5 agent** (R1 FAIL → R2 FAIL → R3 FAIL → R4 FAIL, **收敛单调**)。
- **当前态**: Spec v5 (公式已按 R4 五方发现合成修正) + 2 个拆出的 L2 Spec。**未收敛, 待 R5。**
- **下一步**: 见 §6。**R5 应当 PASS** —— 五位一致「不需要第五次换轴」, R4 全部发现已折入。

## §1 已完成

### 1.1 同步 (owner 请求 1)

| 仓库 | HEAD | origin | github |
|------|------|--------|--------|
| 主仓 Aria | `af546bd` (本 session commit) | ✅ | ✅ |
| aria (plugin) | `0964496` (v1.56.1) | ✅ | ✅ |
| standards | `9df1722` | ✅ | ✅ |
| aria-orchestrator | WIP `92acce5` | master `daf7c79` | **本 session 补齐** `b2484f2`→`daf7c79` (32 commit) |

- 开局本地落后 origin/master **4 commit** (双子星已 ship v1.56.0/v1.56.1) —— **而 `/state-scanner` 报「已同步」**。这就是缺陷本身。
- `aria-orchestrator` 的 ` M` 是**有意的 WIP feature 分支 checkout** (`feature/m6-cost-model-telemetry`), **不是待办**。

### 1.2 缺陷 (owner 请求 2 的产出)

`state-scanner` 的 `sync_status` 在本地 remote-tracking ref 陈旧时报 `parity: equal` / `overall_parity: true`, 而工作树实际落后远程 ⇒ **AI 基于落后树开工 → 重复劳动** (memory `feedback_concurrent_duplicate_audit_fetch_before_start` 的**工具层成因**)。

**核心洞察**: **新鲜度不能「测量」, 只能「获取」。** git 磁盘上**不存在** per-remote 新鲜度信号 —— 三候选经 R1 逐一实测排除 (FETCH_HEAD 是 repo 全局单值 / `refs/remotes/*` 文件 mtime 只在值变化时更新 / `pack-refs` 后 loose 文件消失)。

### 1.3 产出物

| 文件 | 内容 |
|------|------|
| `docs/decisions/DEC-20260712-001-...md` | 决策记录 (v2, 待更新到 v5) |
| `openspec/changes/state-scanner-stale-refs-false-parity/` | **主 Spec (L3)** — 核心机制 F1′-F6′/F9′ |
| `openspec/changes/state-scanner-snapshot-stderr-secret-leak/` | **Spec B (L2)** — Rule #7 裸 stderr 收口, **应先落地** |
| `openspec/changes/state-scanner-issue-cache-freshness-assertion/` | **Spec C (L2)** — 正交, 含新增 `generated_at` 字段 |
| `.aria/audit-reports/post_spec-R1-R2-...-aggregated.md` | R1+R2 聚合报告 |
| `.aria/audit-reports/post_spec-R3-R4-...-aggregated.md` | **R3+R4 聚合报告** (含 v5 公式合成解 + 6 条元教训) |
| **aria-plugin [#110](https://forgejo.10cg.pub/10CG/aria-plugin/issues/110)** | **缺陷追踪票** (含活体证据 / 根因 / 方案 / 4 轮审计摘要) |

## §2 未完成 / Carry-forward

- **carry-state-scanner-false-parity**: post_spec **R5** (5 agent)。R4 的全部发现已折入 v5, 五位一致「R5 应当 PASS」。R5 通过后 → owner sign-off → A.2/A.3。
  tech-lead 建议: **R5 只审 F4′ 的最终公式 + R4 的 5 个修正点**, 不必跑全量。
- ~~R3/R4 审计报告未落盘~~ **✅ 已补** (`post_spec-R3-R4-2026-07-12T2000Z-...-aggregated.md`)
- ~~缺陷无 issue 追踪~~ **✅ 已开票 aria-plugin [#110](https://forgejo.10cg.pub/10CG/aria-plugin/issues/110)**
- **DEC 需更新到 v5** (含: 删除「#109 首次活体验证」这个**已被证伪**的时间断言 —— 2026-07-09 handoff 有更早的真实生产调用 `carry-followup-99`)。
- (承前) M6 owner 4 门 / M7 D3 门 / carry-136-rotation / 168h 跑。

## §3 关键风险 / 已知陷阱

### 3.1 🔴 同一个不变量, **五次复发**

QA-C1 的不变量:「**零证据不得当正证据**」。它在本 Spec 起草过程中被违反了**五次**:

| # | 形态 | 发现于 |
|---|------|--------|
| 1 | 零证据 (all-unknown → true) | QA-C1 历史修复 |
| 2 | **陈旧证据** 当新鲜证据 | 本 Spec (原始缺陷) |
| 3 | **从未获取过的证据** (`age is None` → 判「不陈旧」) | R1 |
| 4 | v3 只豁免 `ahead`, 没问「还有哪些健康常态值落在允许集之外」 | R3-C5 |
| 5 | v4 把 `blocking_unknown` 写成**正向枚举** ⇒ 未列举值 **fail-OPEN** | R4 (四方独立收敛) |

**元教训 (值得进 memory)**:
> **「把一个不变量写进文档」≠「把它写进兜底默认值」。** 没有为「**集合的补集**」定义行为, 就是给了它一个隐式的、通常是错的默认。
>
> 修复必须**类修**不能**点修** —— 必须把取值域**摊开逐格填**, 且**枚举分区必须 fail-CLOSED** (显式列 benign 白名单, 其余一律阻断)。

**已把「逐格填」从纪律变成机制**: tasks 5.1c 加了 pin 测试 —— 构造一个**代码里不存在的** reason 值 ⇒ 必须阻断。

### 3.2 假绿的反面是恒红, 两者**同样零信息量**

本 Spec 在修「恒绿真空」时**三次过冲成恒红**:
- v2 的 D5(a) (每个 remote 必须 equal) ⇒ `ahead` 是 Phase B 常态 ⇒ 恒 false
- v3 的 ∀ (结构性 `unknown` 阻断) ⇒ `detached_head` 是**每个子模块的规范常态** ⇒ **Aria 本仓恒 false**
- Spec C v1 的 AC-3 (`generated_at <= fetched_at`) ⇒ `issue_scan` 有 900s 缓存 ⇒ **缓存路径恒红**

**判据**: **该信号在健康常态下应该是什么值?**

### 3.3 跨 agent 一致 ≠ 正确

R3 的 **tech-lead 和 code-reviewer 给出了相同的错误代码事实** (「`fetched_at` 不在 normalize 白名单会 flaky」)。owner grep 核实: 它**就在** `TIMESTAMP_KEYS:43`。qa-engineer 的相反判断是对的。
⇒ memory `feedback_cross_agent_verdict_independent_verify` 的又一次实证。**两位 agent 都在 R4 主动认了这个错。**

### 3.4 secret-guard 会在讨论 secret 模式的文档上误触发

本 session 写 Spec B 时, 一个**字面占位哨兵** (userinfo 段的假 token) 触发了 secret-guard hook。**按形状匹配, 不区分真假。**
⇒ 测试哨兵必须**运行时拼装**, 不得以完整字面量落在源文件里 (已写进 Spec B 的实施注意)。

## §4 owner 决策记录

| 决策 | 内容 |
|------|------|
| 范围 (初) | F1+F2+F3+F4 全包 / `warn_after_hours` 24→1 —— **两者后被 R1/R2 证伪推翻** (前提不成立) |
| 重设计方向 | 采纳 F3′ 并行 fetch-all (承重实测: 并行 8 腿 = 7.6s ≈ 最慢单腿, 边际 +0.6s) |
| **拆分** | **拆 3 个 Spec** (5/5 agent 共识) |
| **`ahead` 语义** | **不算正证据** —— `overall_parity` = 「本地与远端一致」; 有未推送 commit **确实不是已同步**, 报 false 是诚实的, 下游 `push` 建议是对的。与现有代码/golden fixture/AB rubric 三者一致。**本 Spec 修的是「落后时假绿」(危险), 不是「领先时假红」(无害)。** tech-lead 反方论据已存档, 若 Phase B dogfood 实测告警疲劳可重开 |

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| 主仓 | `af546bd` (Spec + DEC + 审计报告) + 本 handoff |
| aria / standards | 未变更 |
| aria-orchestrator | github 镜像**已补齐** (32 commit), WIP 分支不动 |
| 协调 ref | `state-scanner-stale-refs-false-parity` claim **仍 active** (Phase A.1 提前认领, 未释放) |

## §6 Next session 入口 + 优先级

1. **post_spec R5** (5 agent, 主 Spec + 2 个拆出的 L2 Spec)。**R4 的全部发现已折入 v5**, 五位一致「不需第五次换轴」。tech-lead 建议 **R5 只审 F4′ 的最终公式 + R4 的 5 个修正点**, 不必跑全量。
2. R5 PASS → **owner sign-off** → A.2 (task-planner) → A.3。
3. 补落盘 R3/R4 审计报告; DEC 更新到 v5。
4. **落地顺序** (agent 共识): **Spec C (独立, 随时) → Spec B (Rule #7, 须先于主 Spec) → 主 Spec**。
   ⚠️ 主 Spec 的 `error_kind` **硬依赖** Spec B 的分类器 ⇒ tasks 需加 `0.1 前置: Spec B merged`。
5. **Phase A 内必须锁死的 5 个 OQ** (A-E; 全部已给「倾向」, 待正式裁定)。

## §7 提交清单

- 主仓 `af546bd` (3 Spec + DEC + R1/R2 审计报告) + 本 handoff commit → origin + github

## §8 Memory entries (建议)

**新建**:
1. `feedback_invariant_needs_failclosed_default` — 「把一个不变量写进文档」≠「把它写进兜底默认值」。枚举分区必须 fail-CLOSED (显式豁免白名单 + 其余一律阻断), 正向枚举天然对未来新值/catch-all 值 fail-OPEN。**同一不变量在本 Spec 复发 5 次**。
2. `feedback_freshness_must_be_fetched_not_measured` — 新鲜度不能「测量」只能「获取」。git 磁盘上不存在 per-remote 新鲜度信号 (三候选实测排除)。要知道远端状态, 只能去问远端。
3. `feedback_false_green_dual_is_permanent_red` — 假绿的反面是恒红, 两者同样零信息量。修「恒绿真空」极易过冲成「恒红疲劳」。**判据: 该信号在健康常态下应该是什么值?**
4. `feedback_read_own_spec_before_generalizing` — 泛化一个既有机制前, 先找它自己的 Spec / 先 grep 全仓枚举它所有的既有实现 (本 session: 漏读 #141 two-fetch 语义; 漏发现 `issue_scan.py` 的第二个 `_classify_error`)。
5. `reference_secret_guard_false_positive_on_spec_docs` — secret-guard 按形状匹配, 会在讨论/测试 secret 模式的规范文档与测试代码上误触发。哨兵值必须运行时拼装。

**补强既有**:
- `feedback_cross_agent_verdict_independent_verify` — 追加: **两个 agent 给出相同的代码事实也可能同时错** (R3 tech-lead + code-reviewer 同错, qa 对, owner grep 裁决)。
- `feedback_test_mock_pattern_hides_prod_bug` — 追加: 事故 fixture 可能**早已在测试里**, 只是没人断言那个会暴露矛盾的字段 (`test_local_refs_stale_flag` 断言了 `local_refs_stale=True` 却从没断言 `overall_parity`)。

## Cross-references

- Spec: `openspec/changes/state-scanner-stale-refs-false-parity/` (+ `-snapshot-stderr-secret-leak/` + `-issue-cache-freshness-assertion/`)
- DEC: `docs/decisions/DEC-20260712-001-state-scanner-stale-refs-false-parity.md`
- 审计: `.aria/audit-reports/post_spec-R1-R2-2026-07-12T1850Z-...-aggregated.md`
- 承重先例 (必读): `openspec/archive/2026-06-12-state-scanner-coordination-fetch-resilience` (#141 two-fetch) / `openspec/archive/2026-04-25-state-scanner-mechanical` (AD-SSME-6: schema doc 才是 SOT)
- 下游: `openspec/changes/aria-2.0-m7-fleet-aggregation` (Approved, 消费 `overall_parity`)
- aria-plugin #109 (协调层维度, 真 disjoint 互补)
- 前序 handoff: `2026-07-12-147-live-recheck-138-rework-closeout.md`
