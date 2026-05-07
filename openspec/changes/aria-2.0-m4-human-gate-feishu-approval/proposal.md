# aria-2.0-m4-human-gate-feishu-approval — Aria 2.0 M4 Human gate + Feishu 审批

> **Level**: Full (Level 3 Spec)
> **Status**: Draft (Phase A.1 起草中,2026-05-07)
> **Created**: 2026-05-07
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

> **Baseline (Q8')**: 60h hard (component-sum mid 50h × 1.2 缓冲);**OD-M4-1 reframe trigger @ 72h** (同 M3 OD-13 模式 — A.1 任务拆解 sum > 72h 触发 baseline reframe)

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

**M4 出 scope 时的 deliverable**:
- ≥5 dispatches 走完整 S0→S7→S9_CLOSE cycle (含 ≥1 reject + ≥1 timeout 路径覆盖)
- Feishu 审批 SLO median < 10min 实测 (PRD §618 同模式)
- 7d auto-reject Tier-1 fake-cycle test 全 PASS (AdvancingClock pattern, M3 已实证)
- 幂等性 Tier-1 test: SIGKILL mid-S7 + 双评论 → 不重发 + 不重写
- Schema v3 backward-compat: M3 v2 fixture (≥11-row) migrate 零数据丢失
- PRD §170 + line 405-406 + US-025 表条目 三处 reframe done

## What

### 一、Schema migration v3 additive (T-schema, ~6-8h)

**6 新列** (additive,同 M3 v2 模式 ALTER TABLE):

| 列 | 类型 | 默认值 | 用途 |
|----|------|--------|------|
| `human_decision` | TEXT | NULL | `'approve'` / `'reject'` / `'timeout'` / NULL (NULL=pending) |
| `decision_at` | TEXT (ISO8601 UTC) | NULL | SLO median 计算终点 (验收 A) |
| `reject_reason` | TEXT | NULL | owner 提供的拒绝原因 (Q5) — M5 review-loop 训练样本 |
| `human_gate_entered_at` | TEXT (ISO8601 UTC) | NULL | 7d timeout 起点 (Q3) + SLO 起点 (验收 A) |
| `forgejo_approval_comment_id` | INTEGER | NULL | Q10=B 决策来源评论 ID (审计追溯) |
| `risk_tier_stub` | TEXT | `'always'` | M5 真实分层接口预埋 (Q2) |

**fail_reason enum 扩展** (additive 不破坏既有 9 值):
- `human_reject` (Q5,owner 显式拒绝)
- `human_timeout` (Q3,7d 无 ack 自动拒绝)

**schema_meta**: `schema_version` "2.0" → "3.0"

**migration_notes**: 新增 row `003.human_gate_columns_backfill` — 区分 pre-M4 历史行 NULL 与 pending S7 NULL。

**migrations/003_schema_v3_additive.sql** (additive only, no DROP / ALTER COLUMN):
```sql
ALTER TABLE dispatches ADD COLUMN human_decision TEXT;
ALTER TABLE dispatches ADD COLUMN decision_at TEXT;
ALTER TABLE dispatches ADD COLUMN reject_reason TEXT;
ALTER TABLE dispatches ADD COLUMN human_gate_entered_at TEXT;
ALTER TABLE dispatches ADD COLUMN forgejo_approval_comment_id INTEGER;
ALTER TABLE dispatches ADD COLUMN risk_tier_stub TEXT NOT NULL DEFAULT 'always';
UPDATE schema_meta SET value = '3.0' WHERE key = 'schema_version';
INSERT INTO migration_notes (key, note, applied_at) VALUES (
  '003.human_gate_columns_backfill',
  'M4 schema v3 additive 6 cols. Pre-M4 historical rows have NULL human_* cols (= "real null"); pending S7 dispatches also have NULL human_decision (= "pending decision"). Distinguish via state column: state="S7_HUMAN_GATE" AND human_decision IS NULL → pending; otherwise pre-M4 historical.',
  strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
);
```

### 二、PR 时序前移 (T-pr-timing, ~4-8h)

**当前实现 (extension.py:2024)**: PR 在 `_handle_s8_merge` 入口由 ForgejoClient.create_pr() 创建。注释明示 "S6→S8 direct collapse NOT implemented (deferred M4, OD-9)"。

**M4 改造**:
- `_handle_s6_review` PASS 末端调用 `forgejo.create_pr(branch, title, body)` → 写 `dispatches.pr_id` → 转移到 S7_HUMAN_GATE
- `_handle_s7_human_gate` 入口写 `human_gate_entered_at = now()`,推送 Feishu 卡片 (含 PR link + diff stats + magic-string 提示)
- `_handle_s8_merge` 不再 create PR,只调用 `forgejo.merge_pr(dispatches.pr_id)`

**回归验证**: M3 ≥11-row v2 fixture 走完整 cycle,确认 pr_id 在 S6→S7 边界已写入。

### 三、Forgejo PR 评论 polling + magic-string parser (T-comment-poll, ~6-10h)

**polling 主循环** (复用 M2 T15.x ForgejoCliClient + reconciler 同 30min cadence,或独立 1min 轻 poll):

- 扫描 `dispatches WHERE state='S7_HUMAN_GATE' AND human_decision IS NULL`
- 对每个 dispatch,GET `/repos/{repo}/issues/{pr_id}/comments` (Forgejo API,PR 评论挂在 issue endpoint)
- 增量 polling: 维护 `last_polled_comment_id_per_dispatch` (in-memory 或 DB 列;A.1 设计决策)
- 解析每条新评论:
  - **owner-username 验证**: `comment.user.login == config.owner_username` (PAT scope 已实证模式)
  - **magic-string parser** (strict):
    - `^/aria approve\s*$` → human_decision='approve' + decision_at=now() + forgejo_approval_comment_id=comment.id → S8 transition
    - `^/aria reject:\s*(.+)$` → human_decision='reject' + decision_at=now() + reject_reason=$1 + forgejo_approval_comment_id=comment.id → S_FAIL(human_reject)
    - `^/aria reject\s*$` (无 reason) → 触发"need reason"提示评论 (POST 一条 helpful 评论);不消费 dispatch 状态
- 幂等性: `forgejo_approval_comment_id` UNIQUE 守护双评论 race;dispatch_id 已经过 S7→S8 转移则拒绝再消费 (UNIQUE partial index 已存)

### 四、reject_reason 持久化路径 (T-reject-flow, ~2-4h)

- `db.py update_human_decision(dispatch_id, decision, decision_at, reject_reason=None, comment_id=None)` 新方法 (atomic single-row update)
- transitions.py 加 S7_HUMAN_GATE → S_FAIL(human_reject) 转移 (含 fail_reason='human_reject', fail_detail=reject_reason 前 256 chars)
- Feishu reject 二次告警: `feishu_webhook.send` 二次推送含 reject_reason 摘要 (复用 outbound,fire-and-forget 语义同 M3)

### 五、Reconciler S7 stuck 分支 (T-reconciler, ~4-6h)

复用 M3 `reconciler.py` 30min periodic 同 cadence,加分支:

```python
def _detect_stuck_s7_human_gate(self, repo: DispatchRepository, clock: Clock) -> list[str]:
    """Scan S7_HUMAN_GATE dispatches with human_gate_entered_at > 7d ago."""
    stuck = repo.list_stuck_s7(threshold_days=7)
    for row in stuck:
        repo.cas_mark_failed_stuck(
            issue_id=row['issue_id'],
            dispatch_id=row['dispatch_id'],
            fail_reason=FailReason.HUMAN_TIMEOUT,
            fail_detail=f"S7_HUMAN_GATE entered at {row['human_gate_entered_at']}, exceeded 7d ack window",
            failed_from_state='S7_HUMAN_GATE',
        )
        self._feishu.send(build_timeout_alert_card(row))
    return [row['dispatch_id'] for row in stuck]
```

### 六、risk_tier_stub 接口契约 (T-risk-stub, ~2-3h)

**M4 实现** (stub):
- 进入 S7_HUMAN_GATE 时 `risk_tier_stub = 'always'` (DEFAULT)
- 所有 dispatch 走 human gate
- M5 spec drafting 时把 `risk_tier_stub` 替换为真实 enum (`'high' | 'medium' | 'low'`) + 决策 logic;additive,不破坏 ABI

**ABI 兼容承诺** (写入 AD-M4-6):
- 列名 `risk_tier_stub` 在 M5 改名为 `risk_tier` 时,M5 migration 必须 ADD COLUMN + UPDATE backfill,不 DROP
- 默认值 `'always'` 在 M5 仍保留为合法 enum 值 (= "all dispatches require approval"),向后兼容

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

| ID | 验收 | 量化 metric |
|---|---|---|
| **A** | Feishu 审批 SLO | `median(decision_at - human_gate_entered_at) < 10min` over N≥5 real-or-synthetic dispatches |
| **B** | 7d auto-reject 验证 | Tier-1 fake-cycle test: AdvancingClock 推进 7d → outcome=S_FAIL(human_timeout) + Feishu 二次告警 sent + dispatches.db `fail_reason='human_timeout'` |
| **C** | 幂等性验证 (dispatch_id) | Tier-1: Hermes mid-S7 SIGKILL → restart → Feishu 不二次发送 (assert message_id 不变);双 PR 评论 test → human_decision 仅写一次 (UNIQUE 约束守护) |
| **D** | ≥5 dispatches 走完整 S0→S7→S9_CLOSE cycle | `count(state=S9_CLOSE WHERE human_decision='approve') ≥ 5` (含 ≥1 reject + ≥1 timeout 路径覆盖) |
| **E** | Schema migration v3 backward-compat | M3 dispatches.db fixture (≥11-row v2) migrate 零数据丢失 + 6 新列 present + fail_reason enum 加 2 值 self-doc + schema_version 3.0 |
| **F** | PRD 文档同步 reframe | line 405-406 reframe + §170 reframe + US-025 表条目同步 |

---

## Out of Scope

| ID | 项 | 路由 | 锚点 |
|----|---|------|------|
| OS-1 | Risk-tier 真实分层逻辑 (M4 仅 stub `risk_tier="always"`) | M5 (US-025) | Q2 锁 D + Q11 stub schema |
| OS-2 | Request-Changes / Re-roll path (PR review trinary) | M5 (US-025 review loop) | Q5 锁 A + PRD §568 |
| OS-3 | Replay / Differential testing framework | M5 (US-025) | PRD §405 stale text reframe + Q1 |
| OS-4 | Reconciler 深度增强 (LLM-decided routing / multi-state stuck detection) | M5 (US-025) | Q12 锁 A + PRD §330 |
| OS-5 | Drift defense (拟人化命令漂移检测) | M5 (US-025) | PRD §568 |
| OS-7 | Non-Feishu approval channel (Slack/Discord/Email/Forgejo native vote) | 永久 out (solo-lab Feishu only) | Q10 锁 B + PRD §618 |
| OS-8 | Audit log immutable / replayable | M5 (US-025 审计日志) | Q11 不越界 |

---

## Risks & Mitigations

(见 [US-024.md §风险与缓解](../../../docs/requirements/user-stories/US-024.md))

---

## AD-M4 Slots (待 A.2/A.3 audit + sign-off 后回填)

| AD | 主题 | 关联 brainstorm Q | 主责 agent |
|----|------|------------------|------------|
| **AD-M4-1** | Feishu callback 入站路径选择 (Forgejo PR 评论 vs Cloudflare Tunnel) | Q10 | tech-lead + backend-architect |
| **AD-M4-2** | Magic-string 协议设计 (`/aria approve` / `/aria reject: <reason>` + owner-username 验证) | Q14 | backend-architect |
| **AD-M4-3** | PR 创建时序前移 (S8 → S6 末端) | Q4 + Q13 | backend-architect |
| **AD-M4-4** | 7d auto-reject + reconciler 扩展 (复用 M3 30min cadence) | Q3 + Q12 | backend-architect + qa-engineer |
| **AD-M4-5** | schema v3 additive 6 列 + 2 fail_reason 值 (3.0 bump) | Q11 | backend-architect |
| **AD-M4-6** | risk_tier_stub 接口预埋 + M5 ABI 兼容承诺 | Q2 + Q11 | tech-lead |
| **AD-M4-7** | Feishu 集成 burned record 防御 (T-deploy 6 mandatory configs 复检) | Q10 | qa-engineer |

---

## Phase 路线图

- **A.1** (~12h): proposal + tasks 起草 (本文件) + AD-M4 slots placeholder + Forgejo Issue T0 (owner action)
- **A.2** (~4h): post_spec audit (4-agent parallel R1+R2 collapse 同 M3 OD-15 模式;Level 3 → challenge mode per audit-engine adaptive)
- **A.3** (~1h): owner sign-off (implicit per `feedback_ai_代填_sign_off_pattern` if no objection) + AD-M4 slot 回填 + OD-M4-1 (if triggered, baseline reframe)
- **B.1** (~0.5h): feature 分支 `feature/aria-2.0-m4-human-gate-feishu-approval` 双远程 push
- **B.2** (~50h component-sum): T-schema / T-pr-timing / T-comment-poll / T-reject-flow / T-reconciler / T-risk-stub / T-acceptance / T-docs / T-prd-reframe
- **B.3** (~4h): pre_merge audit (3-4 round convergence 同 v1.16.0 trajectory 24→2→1→0→0 模式)
- **C.1** (~2h): commit + dual-remote push (origin + github,2 远程 parity)
- **C.2** (~3h): PR + merge (Forgejo + GitHub mirror;single-PR-per-spec 模式)
- **D.1** (~1h): UPM 进度更新 + AB benchmark (Skill-only,M4 不引入 Skill 变更可能豁免)
- **D.2** (~1h): Spec archive + retrospective + memory commit

**总 baseline**: 60h hard;**OD-M4-1 reframe trigger**: 任务拆解后 sum > 72h。

---

## Owner action items (前置 / 阻塞)

- [ ] T-deploy: Aether Nomad Variables 配置 `ARIA_FEISHU_WEBHOOK_URL` + `ARIA_FEISHU_SIGNING_SECRET` (前置 acceptance 实测)
- [ ] config: `owner_username` 字段值 (per Forgejo 账号,A.1 spec drafter 设计 config schema)
- [ ] T0.1: Forgejo M4 kickoff issue 创建 (推 Phase B.1)
- [ ] (post-merge) Feishu 6 mandatory configs 复检 (memory burned record 防御)
