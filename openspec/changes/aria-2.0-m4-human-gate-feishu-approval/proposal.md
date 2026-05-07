# aria-2.0-m4-human-gate-feishu-approval — Aria 2.0 M4 Human gate + Feishu 审批

> **Level**: Full (Level 3 Spec)
> **Status**: **Approved** (Phase A.3 lock 2026-05-07, AI-drafted per AD-M0-9 with provenance; owner final sign-off implicit per `feedback_ai_代填_sign_off_pattern` 若无 owner objection within session;R3+R4 collapsed per OD-15-equivalent after R2 4/4 SCOPE_OK_R2 SCOPE_OK_R2)
> **Created**: 2026-05-07
> **Approved**: 2026-05-07 (Phase A.2 R2 SCOPE_OK_R2 4/4 + R3+R4 collapse per M3 OD-15 模式; audit trail `.aria/audit-reports/post_spec-R1-2026-05-07T1811Z-us024-m4.md` + `.aria/audit-reports/post_spec-R2-2026-05-07T1845Z-us024-m4.md`)
> **Parent Story**: [US-024](../../../docs/requirements/user-stories/US-024.md)
> **Target Version**: v2.0.0-m4
> **Source**:
>   - [Brainstorm 2026-05-07](../../../.aria/decisions/2026-05-07-us024-m4-brainstorm.md) — Q1-Q14 全部锁定 (owner 授权 AI 按 Aria 规范代决)
>   - [PRD v2.1 §M4 / line 405-406 (待 reframe) / line 566 / line 510](../../../docs/requirements/prd-aria-v2.md)
>   - [PRD §170 S7_HUMAN_GATE](../../../docs/requirements/prd-aria-v2.md) (待 M4 reframe 双语义)
>   - [PRD §618 SLO < 10min](../../../docs/requirements/prd-aria-v2.md)
>   - [feedback_feishu_hermes_gotchas](../../../.claude/projects/-home-dev-Aria/memory/feedback_feishu_hermes_gotchas.md)
>   - [reference_10cg_cluster_internal_routing](../../../.claude/projects/-home-dev-Aria/memory/reference_10cg_cluster_internal_routing.md) (Aether 192.168.69.x 私网)
>   - [aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/](../../../aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/) (M2/M3 已实现 S7/Feishu/transitions/tests)
> **Forgejo Issue**: _Pending T0.1 (M4 kickoff issue 创建)_
> **Related**:
>   - **前置 (硬门控)**: [US-023](../../../docs/requirements/user-stories/US-023.md) M3 carryover trio CLOSED 2026-05-07
>   - **后继**: US-025 (M5 Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable)
>   - **跨 milestone**: US-027 (Cost routing — M4 不直接涉及)
> **Owner Decisions**: brainstorm Q1-Q14 全部锁定 2026-05-07 (provenance: AI 按 Aria 不可协商规则 #1/#3/#4 + 小步迭代 + 解决根因 + 不 over-engineer 代决, owner 在最终 sign-off 前可否决任一项)

> **Baseline (Q8' + A.3 reconciliation 2026-05-07)**: **60h hard** (component-sum post-R2 mid 50-55h × 1.2 缓冲);**OD-M4-1 reframe trigger 三档边界精确化 (per R2 TL-2)**:
> - A.1 component upper-end sum > 72h ⇒ **立即触发** OD-M4-1 baseline reframe
> - A.1 mid-end sum 60-72h ⇒ **风险记录** (写入 A.3 sign-off note,本 Spec 即此情况),不立即 OD,但 B.2 实测超 72h 触发
> - A.1 mid-end sum < 60h ⇒ 隐式确认 60h 锁
> - **A.3 当前判定**: post-R2 mid 50-55h < 60h → **隐式锁 60h 通过**;upper 65-70h 在 60-72h 风险段,B.2 实施期 sum 实测一旦超 72h 立即立 OD-M4-1。无需 A.3 立即触发 OD reframe。

> **Trust-but-verify 关键发现 (2026-05-07 brainstorm)**: M2/M3 已实现 S7_HUMAN_GATE 大部分基础 (state 枚举 + S6→S7→S8 转移 + FeishuWebhookClient 348-line outbound + 647-line t12_s7_webhook tests + DI feishu/forgejo 注入点)。M4 真实增量 ≈ inbound 评论 polling + 7d reconciler 扩展 + reject_reason + schema v3 + PR 时序前移,远小于 PRD §405 原标 80h 假设。

---

## Why

US-023 M3 (2026-05-07 done) 完成 Layer 1+Layer 2 完整 cycle (S0→S9_CLOSE) + 双 provider HA (Luxeno + Zhipu) + crash recovery (S5_AWAIT auto-resume) + GLM 多模型 quality routing。但 M3 的 S7_HUMAN_GATE 仅是"占位"状态 (`block-until-PR-merge` per t12 test name),没有真实人类审批 gate — owner 必须手动监控 dispatches.db 和 Forgejo PR,与 PRD §32 v2.0 "人类只在关键节点审批" 的核心安全语义不符。

M4 的核心价值: 把 "S7 占位" 升级为 "完整 human gate + Feishu 通知 + Forgejo PR 评论决策 + 7d auto-reject 安全网", 让 AI dispatch 的 PR 必须经 owner 显式批准才能合并, 同时为 M5 review-loop / 防漂移 / 审计日志 immutable 提供数据基座 (reject_reason 持久化即是 M5 训练样本)。

具体变化:

| 维度 | M3 (S7 占位) | M4 (完整 human gate) |
|------|-------------|---------------------|
| S7 语义 | block-until-PR-merge (实质 owner 必须手动 merge) | 显式 Feishu 通知 + Forgejo PR 评论决策 (`/aria approve` / `/aria reject: <reason>`) |
| PR 创建时序 | S8 入口 (extension.py:2024 "S6→S8 deferred M4 OD-9") | S6_REVIEW PASS 末端 (T-pr-timing 前移) |
| reject 路径 | 不存在 (owner 关 PR ≠ orchestrator-aware) | S_FAIL(human_reject) + reject_reason 持久化 |
| 7d timeout | 不存在 (owner 度假 = stuck S7 永久积累) | Reconciler 扩展 30min cadence + S7 stuck > 7d → S_FAIL(human_timeout) + Feishu 二次告警 |
| 幂等性 | 出站 Feishu HTTP 200 (notification_status) | 出站 dispatch_id uuid + 入站 forgejo_approval_comment_id |
| 审批源 | 隐式 (PR merged = 接受) | 显式 (Forgejo PR 评论 magic-string,owner-username 验证) |
| Schema | v2.0 (M3 add cycle/eval/job/cost columns) | v3.0 (additive 6 列 + 2 fail_reason 值) |
| 风险分层 | 不存在 | risk_tier_stub='always' (M5 真实分层 ABI 预埋) |
| Acceptance | M3 § A-F (cycle/perf/recovery/HA/migration/secret) | M4 § A-F (SLO/timeout/idempotency/cycle/migration/PRD-reframe) |

**为什么 Forgejo PR 评论而非 Cloudflare Tunnel webhook** (per Q10=B):
- Aether 192.168.69.x 私网,Feishu (公网) 无法直接 callback,需 Cloudflare Tunnel 引入新基础设施 (~12-18h);
- 复用 M2 T15.x 已实证 Forgejo PR polling + ForgejoCliClient stdlib HTTP (~4-8h);
- 审计完整 (PR 评论永久记录,优于 Feishu 卡片可能过期);
- Solo-lab 维护负担最小 (零新组件);
- PRD §170 字面"Feishu 卡片审批" 实质语义保留 (Feishu 仍是入口,只是决策 commit 走 PR 评论) — 通过 PRD §170 reframe 显式说明。

**Aria dogfooding 边界声明 (R2 fix AI-9)**: M4 仅作用于 Aria orchestrator 派发的 `issue → dispatch → PR` cycle (S0_IDLE → S9_CLOSE 状态机)。**不影响**:
- Aria 自身工程开发 PR 流程 (phase-c-integrator 不变,owner 直接 git push + Forgejo PR + manual merge)
- aria-plugin / standards / aria-orchestrator submodule 的人写代码提交链路
- M4 spec drafting / B.2 实施期的 commit + push 流程 (本 Spec 自身实施不走 S7_HUMAN_GATE)

**M4 出 scope 时的 deliverable**:
- ≥5 dispatches 走完整 S0→S7→S9_CLOSE cycle (含 ≥1 reject + ≥1 timeout 路径覆盖)
- Feishu 审批 SLO median < 10min 实测 (PRD §618 同模式)
- 7d auto-reject Tier-1 fake-cycle test 全 PASS (AdvancingClock pattern, M3 已实证)
- 幂等性 Tier-1 test: SIGKILL mid-S7 + 双评论 → 不重发 + 不重写
- Schema v3 backward-compat: M3 v2 fixture (≥11-row) migrate 零数据丢失
- PRD §170 + line 405-406 + US-025 表条目 三处 reframe done

## What

### 一、Schema migration v3 additive (T-schema, ~7-9h post-R2)

**7 新列** (R2 fix per BA-8/QA-2/AI-1: last_polled_comment_id added for SIGKILL survival):

| 列 | 类型 | 默认值 | 用途 |
|----|------|--------|------|
| `human_decision` | TEXT | NULL | `'approve'` / `'reject'` / `'timeout'` / NULL (NULL=pending) |
| `decision_at` | TEXT (ISO8601 UTC) | NULL | SLO median 计算终点 (验收 A) |
| `reject_reason` | TEXT (uncapped per R2 fix BA-10/QA-9) | NULL | owner 提供的拒绝原因 (Q5) — M5 review-loop 训练样本 |
| `human_gate_entered_at` | TEXT (ISO8601 UTC) | NULL | 7d timeout 起点 (Q3) + SLO 起点 (验收 A) |
| `forgejo_approval_comment_id` | INTEGER | NULL | Q10=B 决策来源评论 ID (审计追溯) — UNIQUE partial index 守护 (BA-2) |
| `risk_tier_stub` | TEXT NOT NULL | `'always'` | M5 真实分层接口预埋 (Q2);DEFAULT 在 SQLite ALTER 时 backfill 所有历史行 |
| `last_polled_comment_id` | INTEGER | NULL | R2 fix: SIGKILL 后 polling 增量起点;cross-restart 持久化 (per AI-1/QA-2/BA-8/AI-10) |

**reject_reason 截断政策 (R2 BA-10/QA-9)**: `dispatches.reject_reason` 列存原文不截断 (M5 review-loop 训练数据完整性);`dispatches.fail_detail` 在 mark_failed 时存 `reject_reason[:256] + '...' if len > 256 else reject_reason` (256-char cap 同 M3 fail_detail pattern,显式 truncation indicator)。

**fail_reason enum 扩展** (additive 不破坏既有 9 值):
- `human_reject` (Q5,owner 显式拒绝)
- `human_timeout` (Q3,7d 无 ack 自动拒绝)

**ALLOWED_TRANSITIONS 扩展 (R2 fix BA-3)**: extension.py:105 当前 `S7_HUMAN_GATE: ["S8_MERGE"]`,M4 改为 `S7_HUMAN_GATE: ["S8_MERGE", "S_FAIL"]`。S_FAIL 是 universal sink 但需显式列入 dict 守护 (转移校验函数读 dict 而非 S_FAIL 通配)。

**schema_meta**: `schema_version` "2.0" → "3.0"

**SQLite version 前置 (R2 AI-5)**: Aether Nomad image SQLite 版本 ≥ 3.25 (2018-09-15) 才支持 RENAME COLUMN。M4 不需 RENAME (additive only),但 M5 风险分层时若改名 risk_tier_stub→risk_tier 需 ≥ 3.25。**T-deploy 增 SQLite version probe 子任务**;若 < 3.25 → M5 用 ADD risk_tier + 双写 + 不 DROP risk_tier_stub (与 AD-M4-6 ABI 承诺一致)。

**migrations/003_schema_v3_additive.sql** (additive only, no DROP / ALTER COLUMN; R2 fix BA-2/BA-9/BA-1/QA-4):
```sql
-- additive columns (7, R2 + last_polled_comment_id)
ALTER TABLE dispatches ADD COLUMN human_decision TEXT;
ALTER TABLE dispatches ADD COLUMN decision_at TEXT;
ALTER TABLE dispatches ADD COLUMN reject_reason TEXT;
ALTER TABLE dispatches ADD COLUMN human_gate_entered_at TEXT;
ALTER TABLE dispatches ADD COLUMN forgejo_approval_comment_id INTEGER;
ALTER TABLE dispatches ADD COLUMN risk_tier_stub TEXT NOT NULL DEFAULT 'always';
ALTER TABLE dispatches ADD COLUMN last_polled_comment_id INTEGER;

-- UNIQUE partial index for forgejo_approval_comment_id (R2 fix BA-2 — 验收 C 双评论 race 守护)
-- SQLite 3.8.9+ supports partial unique index (Aether ≥ 3.25 满足)
CREATE UNIQUE INDEX IF NOT EXISTS uq_approval_comment
  ON dispatches (forgejo_approval_comment_id)
  WHERE forgejo_approval_comment_id IS NOT NULL;

UPDATE schema_meta SET value = '3.0' WHERE key = 'schema_version';

-- self-doc: human_reject / human_timeout enum 扩展 (additive,non-collision)
INSERT OR IGNORE INTO schema_meta (key, value) VALUES (
  'fail_reason_v3_additions',
  '["human_reject","human_timeout"]'
);

INSERT INTO migration_notes (key, note, applied_at) VALUES (
  '003.human_gate_columns_backfill',
  'M4 schema v3 additive 7 cols. Backfill semantics differ by column:
   (a) human_decision/decision_at/reject_reason/human_gate_entered_at/forgejo_approval_comment_id/last_polled_comment_id: NULL for ALL existing rows (pre-M4 historical AND pending). Distinguish via state: state="S7_HUMAN_GATE" AND human_decision IS NULL → pending decision; otherwise pre-M4 historical.
   (b) risk_tier_stub: NOT NULL DEFAULT "always" — ALL existing rows backfill to "always" (no NULL semantics). M5 ABI commitment per AD-M4-6: ADD new risk_tier column + UPDATE backfill, no DROP risk_tier_stub.
   Acceptance E fixture must include ≥1 row each in S7_HUMAN_GATE (NULL=pending), S9_CLOSE (NULL=historical), S_FAIL (existing fail_reason ∉ new enum) per QA-10.',
  strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);
```

**schema.sql canonical update (R2 fix BA-9)**: T-schema.1 必须更新 schema.sql CREATE TABLE dispatches body 含 7 新列(fresh-install 路径) + UNIQUE INDEX 定义,镜像 002 migration 双路模式。fresh DB 不跑 003 migration 但通过 schema.sql 直接落 v3。

### 二、PR 时序前移 (T-pr-timing, ~4-8h)

**当前实现 (extension.py:2024)**: PR 在 `_handle_s8_merge` 入口由 ForgejoClient.create_pr() 创建。注释明示 "S6→S8 direct collapse NOT implemented (deferred M4, OD-9)"。

**M4 改造**:
- `_handle_s6_review` PASS 末端调用 `forgejo.create_pr(branch, title, body)` → 写 `dispatches.pr_id` → 转移到 S7_HUMAN_GATE
- `_handle_s7_human_gate` 入口写 `human_gate_entered_at = now()`,推送 Feishu 卡片 (含 PR link + diff stats + magic-string 提示)
- `_handle_s8_merge` 不再 create PR,只调用 `forgejo.merge_pr(dispatches.pr_id)`

**失败路由 (R2 fix BA-4 + R3-trivial fix BA-NEW per R2 SCOPE_OK_R2)**: `_handle_s6_review` PASS → create_pr 抛异常时:
- 5xx / network timeout: stay-in-S6 (return None,下一 tick 重试);**幂等检查**: 重试前查 dispatches.pr_id IS NOT NULL 或 Forgejo `GET /repos/.../pulls?head=branch` 是否已有同分支 open PR → 有则复用 pr_id 不重建
- 4xx (e.g. 422 invalid params): 视为永久失败 → **S_FAIL(FailReason.INFRASTRUCTURE)** (复用既有 enum 不引入新值,fail_detail 含 4xx HTTP code + Forgejo error body 前 256 chars)
- T-pr-timing.5 测试覆盖: `(a) 5xx → stay-S6 + retry 幂等;(b) 4xx → S_FAIL(INFRASTRUCTURE);(c) 已存在 PR → 复用 pr_id`

**回归验证 (R2 fix QA-13)**: M3 ≥11-row v2 fixture 走完整 cycle 确认 pr_id 在 S6→S7 边界已写入。**显式列出影响测试** (T-pr-timing.7 sub-list):
- `tests/test_t12_s7_webhook.py` test_46-test_53 (M3 直接插入 S7 state 的 fixture 不受影响)
- `tests/test_t12_s7_webhook.py` test_49 (S7→S8 with merged PR — **必须 verify**: refactored _handle_s8_merge 假设 pr_id 已存)
- `tests/test_state_machine_skeleton.py` 任何 S6→S7 路径
- `tests/test_t1_extension_integration.py` end-to-end fixtures

### 三、Forgejo PR 评论 polling + magic-string parser (T-comment-poll, ~7-11h post-R2)

**架构锁定 (R2 fix TL-4 + BA-7 + QA-12 + AI-1, 见 AD-M4-9)**: **独立 30s cron job** (非 reconciler 30min cadence,SLO-compatible);独立 nomad job spec `aria-layer1-comment-poll.nomad.hcl` (additive on existing reconcile job spec)。

**polling 主循环**:

- 扫描 `dispatches WHERE state='S7_HUMAN_GATE' AND human_decision IS NULL`
- 对每个 dispatch,GET `/repos/{repo}/issues/{pr_id}/comments?since={last_polled_comment_id || '1970-01-01T00:00:00Z'}` (Forgejo API,PR 评论挂在 issue endpoint;增量基于 since 参数 OR 客户端 filter `comment.id > last_polled_comment_id`)
- 增量 polling 起点 (R2 fix BA-8/QA-2/AI-1/AI-10): **DB 持久化** `dispatches.last_polled_comment_id` (新 schema v3 第 7 列,M4 schema migration 一并),**非 in-memory** — SIGKILL 后从 last_polled_comment_id 续扫,不重扫历史
- 解析每条新评论:
  - **comment.type filter (R2 fix AI-2)**: 仅消费 `comment.type == "comment"` (skip Forgejo `review`/`activity`/`commit-pushed` 等 pseudo-event;若无 type 字段则 fallback 'has body 且非 system author');加 fixture 含 review-event payload assert 不命中
  - **owner-username 验证 (R2 fix BA-6 + QA-7)**: `comment.user.login == config.owner_username`;**字段名活 verify**: T-comment-poll.5a 子任务 — live curl 一次 Forgejo API GET issue comments,assert response 真有 `user.login` 字段 (vs `user.username`),记录 verified field name in AD-M4-2;**case-sensitive exact match** (无 trim/normalize),边界 case (大小写变体 / 尾随空格 / Unicode 同形 / 改名后历史评论) 全 reject
  - **magic-string parser** (strict, R2 fix QA-1 + AI-8):
    - **regex flags**: 默认 `re.MULTILINE` (评论可能含引用 `> previous comment\n/aria approve`,但 `> /aria approve` 应**不命中** — `^` anchor 前不能有 `> `);**case-sensitive** (大写变体 reject)
    - `^/aria approve\s*$` → human_decision='approve' + decision_at=now() + forgejo_approval_comment_id=comment.id → S8 transition
    - `^/aria reject:\s*(.+)$` → human_decision='reject' + decision_at=now() + reject_reason=$1 (uncapped, M5 喂数据;fail_detail 截断 256 chars per BA-10) + forgejo_approval_comment_id=comment.id → S_FAIL(human_reject)
    - `^/aria reject\s*$` (无 reason) → 触发"need reason"提示评论 (POST 一条 helpful 评论);不消费 dispatch 状态;**bot username 区分 (R2 fix QA-8)**: bot 评论 author 必须 ≠ config.owner_username,即 bot 用专用 PAT 账户 (e.g. `aria-bot`);若 owner PAT 与 bot 共享则 polling 必须 filter `comment.user.login == bot_username` 跳过自身评论 (T-comment-poll.10 测试 fixture)
  - **first-decision-wins 语义 (R2 fix AI-3)**: dispatch 已有 human_decision IS NOT NULL → 后续命中评论(即使被编辑/删除)**全部忽略**;Feishu 二次告警 'decision frozen, edits ignored';**不**记录 comment.body snapshot (silknode contract no-storage 兼容)
  - **评论编辑/删除 (R2 fix AI-3)**: Forgejo comment edit 保留 id,polling 拿到时 dispatch 已 transition → first-decision-wins 拒绝二次消费;评论删除后 forgejo_approval_comment_id 仍指向 deleted comment,审计可追溯 PR + comment_id (即便 body 不可读),不破坏 evidence 链
- **Pagination (R2 fix AI-1)**: Forgejo API GET comments 默认 page size 30,长 PR (>30 评论) 必须翻页或 `since` 参数;实现 `fetch_new_comments(forgejo, pr_id, since_comment_id) -> list[Comment]` 内部循环 page 直至无新评论
- 幂等性 (R2 fix BA-2 强化): `forgejo_approval_comment_id` UNIQUE partial index (003 migration) 守护双评论 race;dispatch_id 已经过 S7→S8 转移则拒绝再消费 (UNIQUE partial index uq_issue_active_partial 已存)

### 四、reject_reason 持久化路径 (T-reject-flow, ~2-4h)

- `db.py update_human_decision(dispatch_id, decision, decision_at, reject_reason=None, comment_id=None)` 新方法 (atomic single-row update)
- transitions.py 加 S7_HUMAN_GATE → S_FAIL(human_reject) 转移 (含 fail_reason='human_reject', fail_detail=reject_reason 前 256 chars)
- Feishu reject 二次告警: `feishu_webhook.send` 二次推送含 reject_reason 摘要 (复用 outbound,fire-and-forget 语义同 M3)

### 五、Reconciler S7 stuck 分支 (T-reconciler, ~4-6h)

复用 M3 `reconciler.py` 30min periodic 同 cadence,加分支 (R2 fix BA-5: pseudocode 修正 expected_state CAS 参数):

```python
def _detect_stuck_s7_human_gate(self, repo: DispatchRepository, clock: Clock) -> list[str]:
    """Scan S7_HUMAN_GATE dispatches with human_gate_entered_at > 7d ago.

    CAS 守护 (R2 BA-5): expected_state='S7_HUMAN_GATE' 防 race —
    若 dispatch 在 list_stuck_s7 与 cas_mark_failed_stuck 之间已 transition
    到 S8/S9_CLOSE/S_FAIL,CAS 返回 0 → 跳过该 row,不误标 HUMAN_TIMEOUT。
    """
    stuck = repo.list_stuck_s7(threshold_days=7)  # WHERE state='S7_HUMAN_GATE' AND human_gate_entered_at < now-7d
    marked = []
    for row in stuck:
        cas_ok = repo.cas_mark_failed_stuck(
            issue_id=row['issue_id'],
            dispatch_id=row['dispatch_id'],
            expected_state='S7_HUMAN_GATE',  # R2 fix BA-5
            fail_reason=FailReason.HUMAN_TIMEOUT,
            fail_detail=f"S7_HUMAN_GATE entered at {row['human_gate_entered_at']}, exceeded 7d ack window",
            failed_from_state='S7_HUMAN_GATE',
        )
        if cas_ok:
            self._feishu.send(build_timeout_alert_card(row))  # fire-and-forget
            marked.append(row['dispatch_id'])
    return marked
```

**Feishu 二次告警幂等性 (R2 BA-8 partial)**: timeout alert 与 reject alert 都是 fire-and-forget 出站,无 dedupe 守护。CAS 锁保证 transition 只发生一次 → Feishu send 也只调用一次。SIGKILL 在 cas_mark_failed_stuck 成功后 + Feishu send 前重启的窗口内 timeout alert 会丢失 (acceptable,fail_reason='human_timeout' 已持久化,owner 可从 dispatches.db 查到)。

### 六、risk_tier_stub 接口契约 (T-risk-stub, ~3-4h post-R2)

**M4 实现** (stub):
- 进入 S7_HUMAN_GATE 时 `risk_tier_stub = 'always'` (DEFAULT 自动 backfill)
- 所有 dispatch 走 human gate
- M5 spec drafting 时引入真实 `risk_tier` enum (`'high' | 'medium' | 'low'` 待 M5 brainstorm 锁) + 决策 logic;additive 加新列,**不 DROP** risk_tier_stub

**ABI 兼容承诺 (R2 fix AI-5,写入 AD-M4-6 6-section 模板)**:
- M5 migration: ADD COLUMN `risk_tier` (新列) + UPDATE backfill (基于 risk_tier_stub 值映射,e.g. `'always'` → `'high'` 强制别名)
- **不 RENAME** (SQLite 限制 + 双写期 truth-source 一致性) — 双写 risk_tier_stub + risk_tier,M5 实施期 dispatch_repo 必须保持 1:1 mapping
- **不 DROP** risk_tier_stub — 长期 schema column (acceptable schema bloat per AD-M4-6 trade-off)
- M5 spec 起草必须 cross-reference AD-M4-6 (validate-m4-handoff.py 加 abi_compat_promises 字段强制读取,per R2 TL-10)

**SQLite version 前置 (R2 AI-5)**: Aether image SQLite 版本 probe (T-deploy 子任务) — 若 ≥ 3.25 则 RENAME 选项理论可用 (但 ABI 承诺仍排除 RENAME);若 < 3.25 则 RENAME 不可用 (但 M4 不需 RENAME)。Probe 结果记入 AD-M4-6 environmental note。

### 七、Acceptance 实测 (T-acceptance, ~4-6h)

- ≥5 synthetic dispatches 走完整 S0→S7→S9_CLOSE cycle
- 含 ≥1 approve / ≥1 reject / ≥1 timeout 路径覆盖
- SLO median 测试 (验收 A): `median(decision_at - human_gate_entered_at)` 计算 + assert < 10min
- 6 验收脚本 (per `tasks.md` T-acceptance.x)

### 八、Docs (T-docs, ~4-6h)

- AD-M4-1~AD-M4-7 决策记录 (见下)
- m4-handoff.yaml schema v1.0 (additive on m3-handoff.yaml schema, 复用 M2 T16 模式)
- aria-layer1 README 更新 (S7 human gate 章节)
- decision records: brainstorm 已存,A.3 后追加 OD-M4-1 (if triggered) + final sign-off

### 九、PRD reframe (T-prd-reframe, ~2-3h)

**three-spot reframe**:

1. **PRD line 405-406** (实施路线图):
   - 旧: `M4 (Week 17-21) Crash recovery + Replay + Reconciler (80h)` / `M5 (Week 22-27) Human gate + Review loop + Drift defense (100h)`
   - 新: `M4 (Week 17-19) Human gate + Feishu 审批 (60h)` / `M5 (Week 20-25) Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable (~120h, M3+M4 carryover scope 重估)`

2. **PRD §170** (S7_HUMAN_GATE 占位):
   - 旧: `S7_HUMAN_GATE: Feishu 审批卡片 (唯一人类介入点)`
   - 新: `S7_HUMAN_GATE: Feishu 卡片 (通知 + 入口) + Forgejo PR 评论 (决策真理来源, /aria approve | /aria reject: <reason>)`,owner-username 验证;7d ack auto-reject

3. **PRD §User Stories 表 line 567** (US-025):
   - 旧: `US-025 | Aria 2.0 M5 — 防漂移 + 审计日志 + Review loop | M5 | MEDIUM`
   - 新: `US-025 | Aria 2.0 M5 — Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable | M5 | MEDIUM` (含 M4 OS-1~OS-5/OS-8 carryover)

### 十、Owner deploy (T-deploy, ~2-3h owner-only)

- Feishu env vars 配置 (Aether Nomad Variables): `ARIA_FEISHU_WEBHOOK_URL` + `ARIA_FEISHU_SIGNING_SECRET`
- owner_username 配置项 (config schema 由 A.1 设计)
- aria-layer1 nomad job 重启 + Consul service health check pass
- 6 mandatory feishu+hermes configs 复检 (memory burned record 防御)

---

## Acceptance Criteria

R2 fix QA-6/QA-11/AI-6: 加 Tier 标签 (Tier-1=自动化 fake-cycle / Tier-2=real-dispatch evidence);A 拆 A.1 synthetic + A.2 owner real。

| ID | 验收 | Tier | 量化 metric |
|---|---|---|---|
| **A.1** | SLO 公式正确性 (synthetic) | Tier-1 | fake-cycle 注入 ≥5 dispatch (decision_at = entered_at + Δ),验 `median(Δ) < 10min` 公式可计算 + assert SQL 正确 |
| **A.2** | SLO 真实人决策延迟 | Tier-2 | T-deploy 后 owner 实操 ≥3 dispatches → `median(decision_at - human_gate_entered_at) < 10min` 实测 (推迟 Phase B.3 acceptance window OR Phase D 收尾验证) |
| **B** | 7d auto-reject 验证 | Tier-1 | fake-cycle: 插入 row with `human_gate_entered_at = clock.now() - 7d - 1s` → 单次调 `_detect_stuck_s7_human_gate()` → outcome=S_FAIL(human_timeout) + Feishu 二次告警 sent + dispatches.db `fail_reason='human_timeout'` (per QA-5: **不**用 AdvancingClock 推进 336 ticks,镜像 M3 t6 reconciler timestamp-comparison 模式) |
| **C** | 幂等性验证 (dispatch_id) | Tier-1 | (a) **subprocess SIGKILL** (per QA-3): `subprocess.Popen(hermes-cli) + os.kill(SIGKILL) + restart 新 subprocess + 共享 DB` → Feishu Fake Webhook call count == 1;(b) 双 PR 评论 test → human_decision 仅写一次 (forgejo_approval_comment_id UNIQUE partial index 守护);(c) Hermes restart with `last_polled_comment_id` wiped (R2 AI-10) → 不重发 'need reason' 提示评论 (DB 持久化保护) |
| **D** | ≥5 dispatches 走完整 S0→S7→S9_CLOSE cycle | Tier-1 (≥3) + Tier-2 (≥2) | `count(state=S9_CLOSE WHERE human_decision='approve') + count(state=S_FAIL WHERE fail_reason='human_reject') + count(state=S_FAIL WHERE fail_reason='human_timeout') ≥ 5`;**至少 1 approve + 1 reject + 1 timeout 路径覆盖**;Tier-2 推迟到 T-deploy 后 |
| **E** | Schema migration v3 backward-compat | Tier-1 | M3 dispatches.db fixture (≥11-row v2,**含 ≥1 row in S7_HUMAN_GATE + ≥1 in S9_CLOSE + ≥1 in S_FAIL** per QA-10) migrate 零数据丢失 + 7 新列 present (含 last_polled_comment_id) + fail_reason enum 加 2 值 self-doc + schema_version 3.0 + UNIQUE INDEX uq_approval_comment created |
| **F** | PRD 文档同步 reframe | Tier-1 (grep) | line 405-406 reframe + §170 reframe + US-025 表条目同步 + §409 总预算 reconciliation 算术校验 (per R2 TL-3) |

---

## Out of Scope

| ID | 项 | 路由 | 锚点 |
|----|---|------|------|
| OS-1 | Risk-tier 真实分层逻辑 (M4 仅 stub `risk_tier="always"`) | M5 (US-025) | Q2 锁 D + Q11 stub schema |
| OS-2 | Request-Changes / Re-roll path (PR review trinary) | M5 (US-025 review loop) | Q5 锁 A + PRD §568 |
| OS-3 | Replay / Differential testing framework | M5 (US-025) | PRD §405 stale text reframe + Q1 |
| OS-4 | Reconciler 深度增强 (LLM-decided routing / multi-state stuck detection) | M5 (US-025) | Q12 锁 A + PRD §330 |
| OS-5 | Drift defense (拟人化命令漂移检测) | M5 (US-025) | PRD §568 |
| OS-7 | Non-Feishu **notification** channel (Slack/Discord/Email/Forgejo native vote) | 永久 out (solo-lab Feishu only) | Q10 锁 B + PRD §618 |

> **OS-7 边界澄清 (R2 fix TL-8)**: Forgejo PR 评论作为 *decision-commit channel* 是 **in-scope** per Q10=B (审批真理来源,owner-username 验证 + magic-string parser);Feishu 是 *notification channel*。OS-7 锁的是 *notification* channel — 不接 Slack/Email/etc.推送。"channel for decision" = Forgejo PR 评论 (in-scope), "channel for notification" = Feishu only (OS-7)。
| OS-8 | Audit log immutable / replayable | M5 (US-025 审计日志) | Q11 不越界 |

---

## Risks & Mitigations

(见 [US-024.md §风险与缓解](../../../docs/requirements/user-stories/US-024.md))

---

## AD-M4 Slots (R2 expanded: 7→11, 待 A.2/A.3 audit + sign-off 后回填)

| AD | 主题 | 关联 brainstorm Q / R2 finding | 主责 agent |
|----|------|----------------------------|------------|
| **AD-M4-1** | Feishu callback 入站路径选择 (Forgejo PR 评论 vs Cloudflare Tunnel) | Q10 | tech-lead + backend-architect |
| **AD-M4-2** | Magic-string 协议设计 (`/aria approve` / `/aria reject: <reason>` + owner-username 验证 + comment.user.login field-name verified + first-decision-wins + bot username 区分) | Q14 + R2 (BA-6/QA-7/QA-8/AI-3/AI-8) | backend-architect |
| **AD-M4-3** | PR 创建时序前移 (S8 → S6 末端) + create_pr 失败路由 (5xx stay-S6 / 4xx S_FAIL / 已存复用 pr_id) | Q4 + Q13 + R2 (BA-4) | backend-architect |
| **AD-M4-4** | 7d auto-reject + reconciler 扩展 (复用 M3 30min cadence) + CAS expected_state='S7_HUMAN_GATE' | Q3 + Q12 + R2 (BA-5) | backend-architect + qa-engineer |
| **AD-M4-5** | schema v3 additive 7 列 (含 last_polled_comment_id) + 2 fail_reason 值 + UNIQUE partial index uq_approval_comment + ALLOWED_TRANSITIONS S7→S_FAIL 扩展 + reject_reason 截断政策 | Q11 + R2 (BA-1/BA-2/BA-3/BA-8/BA-9/BA-10/QA-2/QA-4/QA-9/QA-10) | backend-architect |
| **AD-M4-6** | risk_tier_stub 接口预埋 + M5 ABI 兼容承诺 (ADD COLUMN + 双写 + 不 RENAME 不 DROP) + SQLite version probe environmental note | Q2 + Q11 + R2 (AI-5) | tech-lead |
| **AD-M4-7** | Feishu 集成 burned record 防御 (T-deploy 6 mandatory configs 复检, 含 ops/deploy hygiene per AD-M0-9 solo-lab role merging per R2 TL-9) | Q10 + R2 (TL-9) | qa-engineer |
| **AD-M4-8** *(R2 NEW per TL-1)* | Cross-cutting idempotency 三层契约 (dispatch_id outbound + forgejo_approval_comment_id inbound + UNIQUE partial index uq_approval_comment) | Q6 + R2 (BA-2/TL-1) | backend-architect |
| **AD-M4-9** *(R2 NEW per TL-4 + AI-1; R3-trivial 优先级注记 per AI-R2-2)* | Comment polling cadence: 独立 30s cron job (非 reconciler 30min cadence) + last_polled_comment_id DB 持久化 + pagination + **first-decision-wins guard 优先级高于 since 增量 cursor 推进** (即 polling 拿到 edited comment 时若 dispatch.human_decision IS NOT NULL → short-circuit 拒绝再消费,即使 forgejo since 返回该 comment) | R2 (TL-4/BA-7/QA-12/AI-1/BA-8) + R3-trivial (AI-R2-2) | backend-architect + ai-engineer |
| **AD-M4-10** *(R2 NEW per TL-6 + TL-10)* | m4-handoff.yaml schema additive on m3-handoff (human gate 7 字段 + 2 fail_reason 值) + abi_compat_promises 字段 (forward-binding M5) + validate-m4-handoff.py 强制 cross-reference | R2 (TL-6/TL-10) | tech-lead |
| **AD-M4-11** *(R2 NEW per AI-7)* | owner_username config 来源 + schema (`.aria/orchestrator-config.yaml` `authorized_approvers: list[str]`,M4 单元素 [owner],M5 加 reviewer 非 ABI break) + 加载顺序 file-first env-override | R2 (AI-7) | backend-architect + ai-engineer |

---

## Phase 路线图 (R2 fix TL-5: audit overhead 4→4-6h)

- **A.1** (~12h): proposal + tasks 起草 (本文件) + AD-M4 slots placeholder + Forgejo Issue T0 (owner action)
- **A.2** (~4-6h, R2 fix TL-5): post_spec audit (4-agent parallel R1+R2 + 可选 R3 stability + R4 strict;collapse 决策见 R2 SCOPE_OK 后)
- **A.3** (~1h): owner sign-off (implicit per `feedback_ai_代填_sign_off_pattern` if no objection) + AD-M4-1~AD-M4-11 slot 回填 + OD-M4-1 (if triggered, baseline reframe per TL-2 trigger 边界)
- **B.1** (~0.5h): feature 分支 `feature/aria-2.0-m4-human-gate-feishu-approval` 双远程 push
- **B.2** (~50h component-sum mid / ~65h upper): T-schema / T-pr-timing / T-comment-poll / T-reject-flow / T-reconciler / T-risk-stub / T-acceptance / T-docs / T-prd-reframe / T-deploy
- **B.3** (~4-6h, R2 fix TL-5): pre_merge audit (3-4 round convergence 同 v1.16.0 trajectory 24→2→1→0→0 模式;允许 R3+R4 stability 不强制 collapse)
- **C.1** (~2h): commit + dual-remote push (origin + github,2 远程 parity)
- **C.2** (~3h): PR + merge (Forgejo + GitHub mirror;single-PR-per-spec 模式)
- **D.1** (~1h): UPM 进度更新 + AB benchmark (Skill-only,M4 不引入 Skill 变更可能豁免)
- **D.2** (~1h): Spec archive + retrospective + memory commit

**总 baseline**: 60h hard;**OD-M4-1 reframe trigger (R2 TL-2 精确化)**:
- A.1 component upper-end sum > 72h ⇒ **立即触发** OD-M4-1 baseline reframe
- A.1 mid-end sum 60-72h ⇒ **风险记录** (写入 A.3 sign-off note),不立即 OD,但 B.2 实测超 72h 触发
- A.1 mid-end sum < 60h ⇒ 隐式确认 60h 锁
- A.1 当前 mid sum ≈ 50-55h (R2 fix 后 +3-5h: T-schema +2-3h, T-comment-poll +2-3h, T-acceptance +1-2h);upper sum ≈ 65-70h **接近触发边界**,A.3 须显式重新 reconcile

---

## Owner action items (前置 / 阻塞)

- [ ] T-deploy: Aether Nomad Variables 配置 `ARIA_FEISHU_WEBHOOK_URL` + `ARIA_FEISHU_SIGNING_SECRET` (前置 acceptance 实测)
- [ ] config: 提供 owner Forgejo username 字面值 (T-deploy.3 写入 `authorized_approvers: ["<owner-username>"]`,推 T-deploy 阶段) — *R3-trivial fix per TL-R2-3*
- [ ] (可选) bot PAT 账户 (e.g. `aria-bot`) 创建并配置 PAT (per AD-M4-2 bot username 区分;若与 owner PAT 共享则 polling 必须 filter 自身评论)
- [ ] T0.1: Forgejo M4 kickoff issue 创建 (推 Phase B.1)
- [ ] (post-merge) Feishu 6 mandatory configs 复检 (memory burned record 防御)
