# 决策: DEC-20260507-01 — US-024 (Aria 2.0 M4) Brainstorm 收敛

> **日期**: 2026-05-07
> **模式**: requirements
> **范围**: Aria 2.0 M4 — Human gate + Feishu 审批
> **关联**: PRD v2.1 §M4, US-023 (M3 closure), US-025 (M5 后继)
> **Provenance**: Owner explicit authorization "遵循 aria 规范进行决策和选择" → AI 按 Aria 不可协商规则 #1/#3/#4 + 小步迭代 + 解决根因 + 不 over-engineer 代决,owner 在最终 sign-off 前可否决任一项。

---

## 背景

M3 (US-023) 于 2026-05-07 完成 carryover trio 归档 (`m3-carryover-hcl-crons-sweep` / `m3-carryover-result-path-derivation` / `m3-handoff-validator-spillover`)。M3 已交付 Layer 1+Layer 2 完整 cycle (S0→S9_CLOSE) + Crash recovery (S5_AWAIT auto-resume) + GLM 多 provider HA。

PRD v2.1 §User Stories 表 (line 566) 锁定 US-024 = M4 = "Human gate + Feishu 审批",但 §实施路线图 line 405-406 仍保留早期草稿 "M4=Crash/Replay/Reconciler / M5=Human gate" — **PRD 内部冲突,brainstorm Q1 解决**。

Trust-but-verify 发现 M2/M3 已实现 S7_HUMAN_GATE 大部分基础 (state 枚举 + transitions + FeishuWebhookClient outbound + tests),M4 真实增量远小于 PRD §405 原标 80h。

---

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| Aria 规范 #1 (规范先行) | brainstorm 必须给 baseline,不可全推 A.3 | Q8'/Q11 给数字 |
| Aria 规范 #3 (文档同步) | PRD 漂移必须随 Spec 同步修复 | Q1/Q9/Q10 派生 PRD reframe 任务 |
| Aria 规范 #4 (向后兼容) | schema migration additive-only | Q11 锁 v3 同 M3 v2 模式 |
| 小步迭代 (4-8h 任务粒度) | M4 任务可分解 8-12 个 | Q8' 60h baseline 11 任务 |
| Solo-lab 实操 | owner 单人审批,无团队 | Q2 stub + Q9 OS-6 implicit out |
| Aether 私网拓扑 | 192.168.69.x 不可直接被 Feishu (公网) callback | Q10 选 Forgejo PR 评论而非 Cloudflare Tunnel |
| Feishu burned record | WebSocket / 6 mandatory configs 已有先例 | Q10 排除 D (WebSocket) |
| PRD §355 P0 幂等性 | 所有外部副作用必须 idempotent | Q6 单一键 dispatch_id |
| PRD §618 SLO | 审批中位数 < 10min | Q7 验收 A,Q10 polling 30s 不冲突 |
| Q9 锁 OS-1~OS-8 | 7 项 M5/v3 推迟 | Q11 不越界 audit log;Q12 不越界 reconciler 深度增强 |
| M3 OD-13 inflation lesson | brainstorm baseline 易低估 | Q8' β' 1.2x 缓冲 + A.3 reframe trigger |
| 已有 M2/M3 实现 (trust-but-verify) | S7_HUMAN_GATE / FeishuWebhookClient / transitions / tests 已存 | Q8' 60h reframe;Q13 PR 时序前移 |

---

## 决议汇总 (Q1-Q14)

| Q | 主题 | 锁定值 | 关键依据 |
|---|------|--------|----------|
| **Q1** | M4 范围 | **A** Human gate-focused + PRD line 405-406 reframe | §M3 Out of Scope (archived) + §User Stories 表 + 规范 #1/#3/#4 |
| **Q2** | 触发范围 | **D** always require + risk-tier stub for M5 | 小步迭代单变量 + PRD §170 兼容 + 不 over-engineer |
| **Q3** | 7d 超时行为 | **A** auto-reject + S_FAIL(human_timeout) + Feishu 二次告警 | fail-safe + 复用 M3 S_FAIL 路径 + 显式 deadline |
| **Q4** | PR 边界 | **A** PR 在 S6_REVIEW 末端创建,S7=审批入口 | 不重造 Forgejo PR review UI + 最小新概念 + 审计完整 |
| **Q5** | 审批 UX | **A** Binary [Approve/Reject] + reject_reason 持久化 | 不越界 M5 review-loop + 复用 S_FAIL + 为 M5 喂数据 |
| **Q6** | 幂等性 | **A** 单一幂等键 = `dispatch_id` | PRD §355 P0 + 单一真理来源 + Feishu uuid 原生支持 |
| **Q7** | 验收标准 | **β + I** 6 项验收 (A-F) + N≥5 dispatches | 同 M3 6-criterion validated pattern |
| **Q8'** | 工时基线 (reframe) | **β' 60h** baseline + A.3 OD reframe trigger @ 72h | M2/M3 已实现部分 + 小步迭代 + Feishu 集成 buffer |
| **Q9** | Out of Scope | **β** 7 项 (OS-1~OS-5 + OS-7 + OS-8) | 同 M3 line 510 validated pattern |
| **Q10** | Feishu callback 入站架构 | **B** Forgejo PR 评论作为 approval source-of-truth (Feishu 仅通知) | 解决根因 (复用 polling) + 小步迭代 + 零新基础设施 + Feishu WebSocket burned |
| **Q11** | Schema migration v3 列定义 | **A** 6 列 + 2 fail_reason 值 + schema 3.0 bump + migration_notes 003 | 同 M3 v2 6-列 validated pattern + 含 Q2 stub + 不越界 OS-8 |
| **Q12** | Reconciler 7d 扫描扩展 | **A** 复用 M3 reconciler 30min,加 S7 stuck 分支 | 解决根因 + 不越界 OS-4 + AD-M2-7 关注点分离 |
| **Q13** | PR 时序前移 | **A** T-pr-timing 任务把 `create_pr` 从 S8→S6 末端 | Q4 锁的实证派生;现状 extension.py:2024 confirmed PR at S8 |
| **Q14** | Forgejo PR 评论协议 | **A** `/aria approve` / `/aria reject: <reason>`,仅 owner username 评论采信 | Q10 B 派生;explicit semantics 优于 emoji 易误点;PAT scope 已实证 |

---

## M4 整体形态 (合并 Q1-Q14)

```
S6_REVIEW (LLM PASS)
   ├── 创建 Forgejo PR (新: Q13 T-pr-timing 前移)
   └── 写 dispatches.pr_id

  ↓

S7_HUMAN_GATE
   ├── Feishu 卡片 (out, 复用 FeishuWebhookClient + dispatch_id uuid 幂等)
   │     └── 含 PR link + diff stats + "在 PR 评论 /aria approve|reject: <reason>" 提示
   ├── human_gate_entered_at = now (新列, 7d timeout 起点)
   ├── risk_tier_stub = 'always' (新列, M5 接入真实分层不破坏 ABI)
   └── 等待:
         ├── Forgejo PR 评论 polling (复用 M2 T15.x polling, +magic-string parser)
         │     ├── /aria approve   → S8 (写 human_decision='approve' + decision_at + forgejo_approval_comment_id)
         │     └── /aria reject: X → S_FAIL(human_reject) (写 reject_reason='X')
         └── reconciler tick (复用 M3 30min, +S7 stuck 分支)
               └── now - human_gate_entered_at > 7d → S_FAIL(human_timeout) + Feishu 二次告警

  ↓ (Approve path)

S8_MERGE
   └── merge_pr(dispatches.pr_id) — 已实现, 不变

  ↓

S9_CLOSE (terminal)
```

---

## 6 项验收标准 (PRD §M3 同模式 commit)

| ID | 验收 | 量化 metric |
|----|------|------------|
| **A** | Feishu 审批 SLO | `median(decision_at - human_gate_entered_at) < 10min` over N≥5 real-or-synthetic dispatches |
| **B** | 7d auto-reject 验证 | Tier-1 fake-cycle test: AdvancingClock 推进 7d → outcome=S_FAIL(human_timeout) + Feishu 二次告警 sent + dispatches.db `fail_reason='human_timeout'` |
| **C** | 幂等性验证 (dispatch_id) | Tier-1: Hermes mid-S7 SIGKILL → restart → Feishu 不二次发送 (assert message_id 不变);双 PR 评论 test → human_decision 仅写一次 (UNIQUE 约束守护) |
| **D** | ≥5 dispatches 走完整 S0→S7→S9_CLOSE cycle | `count(state=S9_CLOSE WHERE human_decision='approve') ≥ 5` (含 ≥1 reject + ≥1 timeout 路径覆盖) |
| **E** | Schema migration v3 backward-compat | M3 dispatches.db fixture (≥11-row v2) migrate 零数据丢失 + 6 新列 present (`human_decision`/`decision_at`/`reject_reason`/`human_gate_entered_at`/`forgejo_approval_comment_id`/`risk_tier_stub`) + fail_reason enum 加 2 值 (`human_reject`/`human_timeout`) self-doc |
| **F** | PRD 文档同步 reframe | line 405-406 reframe to "M4=Human gate / M5=Replay+Reconciler+防漂移+Review loop"; PRD §170 reframe 为 "Feishu 卡片=入口 + Forgejo PR 评论=决策真理来源"; US-025 表条目同步 |

---

## 7 项 Out of Scope (M4 边界)

| ID | 项 | 路由 |
|----|---|------|
| OS-1 | Risk-tier 真实分层逻辑 (M4 仅 stub `risk_tier="always"`) | M5 (US-025) |
| OS-2 | Request-Changes / Re-roll path (PR review trinary) | M5 (US-025 review loop) |
| OS-3 | Replay / Differential testing framework | M5 (US-025) |
| OS-4 | Reconciler 深度增强 (LLM-decided routing / multi-state stuck detection) | M5 (US-025) |
| OS-5 | Drift defense (拟人化命令漂移检测) | M5 (US-025) |
| OS-7 | Non-Feishu approval channel (Slack / Discord / Email / Forgejo native vote) | 永久 out (solo-lab Feishu only) |
| OS-8 | Audit log immutable / replayable | M5 (US-025 审计日志) |

---

## 工时基线 (Q8')

**Baseline**: 60h (component-sum mid 50h × 1.2 缓冲)

**A.3 OD reframe trigger**: spec-drafter A.1 任务拆解后 component sum > 72h → 触发 `OD-M4-1: M4 effort baseline reframe` (同 M3 OD-13 模式)。

**任务拆解 (草案,A.1 spec-drafter 据此精化):**

| 任务组 | 区间 |
|--------|------|
| T-schema (v3 migration: 6 列 + 2 enum + schema_meta 3.0 + migration_notes 003) | 6-8h |
| T-pr-timing (S8→S6 末端前移 create_pr + tests) | 4-8h |
| T-comment-poll (Forgejo PR 评论 polling + magic-string parser + owner-username 验证 + idempotency) | 6-10h |
| T-reject-flow (reject_reason 持久化 + S_FAIL routing + Feishu reject 二次告警) | 2-4h |
| T-reconciler (M3 reconciler S7 stuck 分支 + 7d timeout + Feishu 二次告警 + tests) | 4-6h |
| T-risk-stub (risk_tier_stub 接口契约 + tests; M5 ABI 兼容承诺) | 2-3h |
| T-acceptance (≥5 dispatch E2E + SLO median 测试 + 6 验收脚本) | 4-6h |
| T-docs (AD-M4-1~AD-M4-N + m4-handoff.yaml + README + decision records) | 4-6h |
| T-prd-reframe (PRD §170 + line 405-406 + US-025 表 + decision/govern docs) | 2-3h |
| T-deploy (owner action: Feishu env vars 配置 + Aether 部署验证) | 2-3h owner |
| **Sum (mid)** | **~50h** |
| **Sum (upper)** | **~65h** |

---

## AD-M4 Slots (待 A.1 spec-drafter 起草时回填)

- **AD-M4-1**: Feishu callback 入站路径选择 (Q10=B,Forgejo PR 评论而非 Cloudflare Tunnel)
- **AD-M4-2**: Magic-string 协议设计 (Q14)
- **AD-M4-3**: PR 创建时序前移 (Q13/Q4,S8→S6 末端)
- **AD-M4-4**: 7d auto-reject + reconciler 扩展 (Q3+Q12)
- **AD-M4-5**: schema v3 additive 6 列 + 2 fail_reason 值 (Q11)
- **AD-M4-6**: risk_tier_stub 接口预埋 + M5 ABI 兼容承诺 (Q2)
- **AD-M4-7**: Feishu 集成在 Aria 中的 burned record 防御 (memory feedback_feishu_hermes_gotchas 引用)

---

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| Feishu API 集成隐性坑 (memory 已记 6 mandatory configs burned) | Q10 B 选 Forgejo PR 评论路径,Feishu 仅 outbound 通知 (复用已实现 FeishuWebhookClient);A.3 spec-drafter 须显式列 owner action item: 检查 6 mandatory configs |
| PR 评论 polling SLO 漂移 | 30s polling × 人决策时间 ≫ 30s,SLO 不冲突 (Q10 分析);若实测中位数接近 10min 阈值,A.3 reframe polling interval 至 10s |
| owner-username 仿冒评论 | T-comment-poll 任务必须验证评论 author == 配置中 owner_username (PAT scope 已实证模式) |
| Magic-string 解析歧义 (`/aria reject` 不带 reason) | A.1 spec-drafter 设计明确语法 (`/aria reject: <reason>` 必填,无 reason 触发"need reason"提示评论);实现 strict parser + 友好错误 |
| Schema migration v3 数据丢失 | T-schema 单元测试: 11+ row v2 fixture migrate 通过零数据丢失 (验收 E);additive-only 同 M3 v2 模式 |
| 7d timeout 跨 Hermes 重启计时丢失 | Q12 A 选 reconciler-driven (DB-driven), `human_gate_entered_at` 持久化 = 跨重启不丢 |
| risk_tier_stub 在 M5 真实接入时 ABI 破坏 | T-risk-stub 任务必须写明 ABI 兼容承诺 + M5 spec drafting 时 cross-reference |
| Spec discovery 暴露真实 scope 远高于 60h | A.3 OD-M4-1 reframe trigger @ 72h 同 M3 OD-13 模式 |

---

## 依赖与前置

- ✅ M3 (US-023) 完成 (carryover trio 已归档 2026-05-07)
- ✅ FeishuWebhookClient outbound 已实现 (M2/M3)
- ✅ DispatchState.S7_HUMAN_GATE 状态枚举已存
- ✅ M3 reconciler periodic job 已部署 (aria-layer1-reconcile.nomad.hcl)
- ✅ Forgejo PR polling 已实证 (M2 T15.x)
- ✅ schema_meta + migration_notes 表已存
- ⏳ Feishu env vars (`ARIA_FEISHU_WEBHOOK_URL` + `ARIA_FEISHU_SIGNING_SECRET`) — owner Aether 部署时配置 (T-deploy)
- ⏳ owner_username 配置项 — A.1 spec-drafter 设计 config schema

---

## Phase A.1 准入条件

✅ 本决策记录 owner 授权 + Aria 规范驱动 + provenance 注记完整
✅ Q1-Q14 全部锁定
✅ 6 验收 + 7 OOS + 任务草案 + AD slots 齐备
✅ 风险与缓解列出 7 项
✅ 60h baseline 含 OD reframe trigger 路径

→ **可启动 spec-drafter (Phase A.1) 起草 OpenSpec proposal + tasks.md**

Spec 路径: `openspec/changes/aria-2.0-m4-human-gate-feishu-approval/`

---

## 版本历史

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v0.1 | 2026-05-07 | brainstorm 收敛初稿,Q1-Q14 全部锁定 | AI (per owner explicit authorization) |

---

**Provenance summary**: Owner 在 brainstorm 全程 (Q1-Q14) 显式授权 AI 按 Aria 不可协商规则 (#1/#3/#4) + 小步迭代 + 解决根因 + 不 over-engineer 代决,owner 保留最终 sign-off 否决权。本记录每个决议附 Aria 锚点和理由,便于 owner 审阅和未来 audit 反查。
