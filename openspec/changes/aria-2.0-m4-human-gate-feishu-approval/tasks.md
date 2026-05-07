# aria-2.0-m4-human-gate-feishu-approval — Tasks

> **Spec**: [proposal.md](./proposal.md)
> **Status**: **Approved** (Phase A.3 lock 2026-05-07, R2 SCOPE_OK_R2 4/4 + R3+R4 collapsed per OD-15-equivalent)
> **Baseline**: 60h hard (per brainstorm Q8' β' + A.3 reconciliation);**OD-M4-1 reframe trigger 三档**: >72h 立即 / 60-72h 风险记录 (本 Spec 即此情况) / <60h 隐式锁
> **Audit pattern**: 同 M3 OD-15 collapse (Phase A.2 R1+R2 + R3+R4 collapse,Phase B.3 pre_merge 3-4 round 严格收敛,Phase D 1 round);post_spec audit 完成 (R1+R2 audit reports 已落盘)

---

## Phase A: 规划

### Phase A.1 — Spec drafting (NOW, ~12h)

- [x] **A.1.1** brainstorm 收敛 (`.aria/decisions/2026-05-07-us024-m4-brainstorm.md`,Q1-Q14 全部锁定 owner authorization)
- [x] **A.1.2** Spec 目录创建 `openspec/changes/aria-2.0-m4-human-gate-feishu-approval/`
- [x] **A.1.3** US-024.md 起草 (`docs/requirements/user-stories/US-024.md`)
- [x] **A.1.4** proposal.md 起草 (本 spec, 含 Why/What 10 节/Acceptance/OOS/Risks/AD-M4 slots/Phase 路线图/Owner action)
- [x] **A.1.5** tasks.md 起草 (本文件)
- [ ] **A.1.6** Forgejo Issue T0.1 创建 (M4 kickoff issue, owner action — 推 Phase B.1)
- [ ] **A.1.7** owner_username config 字段定义 (config schema,推 T-comment-poll 设计)

### Phase A.2 — post_spec audit (DONE 2026-05-07, ~3h actual)

- [x] **A.2.1** R1 4-agent multi-agent audit 触发 (backend-architect / qa-engineer / tech-lead / ai-engineer parallel, Level 3 → challenge mode per audit-engine adaptive) — **完成**: 4/4 PASS_WITH_WARNINGS, 6 critical + 21 important + 16 minor
  - 验证 Q1-Q14 brainstorm 决议是否 spec 内充分体现
  - 验证 6 验收 criteria 量化可测性
  - 验证 7 OOS 边界清晰
  - 验证 60h baseline 与任务拆解一致 (若 sum > 72h 触发 OD-M4-1)
  - 验证 PRD §170 / line 405-406 / US-025 reframe 三处一致
  - 验证 schema v3 additive 不破坏 M3 v2 ABI
  - 验证 magic-string parser 对 owner-username 仿冒 / `/aria reject` 缺 reason 等边界鲁棒
- [x] **A.2.2** R1 audit report `.aria/audit-reports/post_spec-R1-2026-05-07T1811Z-us024-m4.md` (165 行, 4-agent JSON output 汇总 + verdict 分析 + R2 fix plan)
- [x] **A.2.3** R1 fix batch (proposal/tasks 修订) — 30 新子任务 + 4 新 AD-M4 slots (AD-M4-8/9/10/11)
- [x] **A.2.4** R2 fix-verify (4-agent SCOPE_OK_R2 4/4: R1 41/43 CLOSED + 2 PARTIAL + 0 NEW critical + 1 NEW important [已 R3-trivial inline 修复] + 11 NEW minor [全 distributed/inline 修复])
- [x] **A.2.5** R2 closeout report `.aria/audit-reports/post_spec-R2-2026-05-07T1845Z-us024-m4.md`
- [x] **A.2.6** R3+R4 collapse per OD-15-equivalent (R2 4/4 SCOPE_OK_R2 直接进 A.3,无需 R3 stability + R4 strict)

### Phase A.3 — Approved 准入 (DONE 2026-05-07, ~0.5h actual)

- [x] **A.3.1** baseline final lock = **60h hard** (post-R2 mid 50-55h < 60h 隐式锁;upper 65-70h 在 60-72h 风险段,B.2 实测超 72h 触发 OD-M4-1)
- [x] **A.3.2** OD-M4-1 **未触发** (mid < 60h 不满足 trigger 第一档;A.3 风险记录 inline in proposal.md baseline 段落,不需独立 OD decision file)
- [x] **A.3.3** Spec proposal.md Status: Draft → **Approved** (per AD-M0-9 AI-drafted with provenance + R2 SCOPE_OK_R2 4/4 + R3+R4 collapsed per OD-15-equivalent)
- [x] **A.3.4** AD-M4-1~AD-M4-11 11 slots 主责 agent column 已在 R2 fix 中回填 (含 R2 NEW: AD-M4-8/9/10/11)
- [ ] **A.3.5** Forgejo Issue T0.1 创建 (owner action,推 Phase B.1)

---

## Phase B: 开发

### Phase B.1 — feature 分支 (~0.5h)

- [ ] **B.1.1** 主仓 + aria-orchestrator submodule 同名 feature 分支创建: `feature/aria-2.0-m4-human-gate-feishu-approval`
- [ ] **B.1.2** 双远程 push (origin + github) — state-snapshot 验证 4 repos 双 remote `parity=equal`

### Phase B.2 — 实施 (~50h component-sum)

#### T-schema — Schema migration v3 additive (~7-9h post-R2)

- [ ] **T-schema.1** `schema.sql` CREATE TABLE dispatches body 加 7 列 (含 last_polled_comment_id per R2 BA-8) + UNIQUE INDEX uq_approval_comment 定义 (per R2 BA-2/BA-9) + 2 fail_reason 注释更新 + schema_version "3.0" + migration_notes 003 INSERT (fresh-install 路径,镜像 002 dual-path)
- [ ] **T-schema.2** `migrations/003_schema_v3_additive.sql` 写 ALTER TABLE 7 列 + UPDATE schema_meta + INSERT migration_notes (text 区分 risk_tier_stub backfill vs human_* NULL per R2 BA-1/QA-4)
- [ ] **T-schema.2b** *(R2 NEW per BA-2)* `migrations/003` 加 `CREATE UNIQUE INDEX IF NOT EXISTS uq_approval_comment ON dispatches (forgejo_approval_comment_id) WHERE forgejo_approval_comment_id IS NOT NULL` (双评论 race 守护)
- [ ] **T-schema.3** `db.py from_row` + `Dispatch` dataclass 加 7 字段 (含 last_polled_comment_id, forward-compatible per 既有 from_row 模式)
- [ ] **T-schema.4** `db.py update_human_decision(dispatch_id, decision, decision_at, reject_reason=None, comment_id=None)` 新方法 (atomic single-row UPDATE);**reject_reason 不截断** (R2 BA-10/QA-9 喂 M5 训练数据完整性)
- [ ] **T-schema.5** `db.py list_stuck_s7(threshold_days=7)` 新方法 (用于 reconciler 扩展)
- [ ] **T-schema.5b** *(R2 NEW per AI-1)* `db.py update_last_polled_comment_id(dispatch_id, comment_id)` 新方法 (atomic UPDATE for SIGKILL-survival polling cursor)
- [ ] **T-schema.6** `interfaces.py FailReason` enum 加 `HUMAN_REJECT='human_reject'` + `HUMAN_TIMEOUT='human_timeout'`
- [ ] **T-schema.6b** *(R2 NEW per BA-3)* `extension.py:105` ALLOWED_TRANSITIONS 改 `S7_HUMAN_GATE: ["S8_MERGE", "S_FAIL"]` (S_FAIL 显式列入 dict 守护,虽 S_FAIL 是 universal sink 但需 dict 校验)
- [ ] **T-schema.7** 单元测试: 11+ row v2 fixture migrate 通过零数据丢失 (验收 E),**fixture 必须含 ≥1 row in S7_HUMAN_GATE (NULL=pending 验证) + ≥1 in S9_CLOSE (NULL=historical) + ≥1 in S_FAIL (existing fail_reason ∉ new enum)** per R2 QA-10
- [ ] **T-schema.8** 单元测试: update_human_decision 各 decision 路径 + reject_reason 持久化 (uncapped) + comment_id UNIQUE 守护;**fail_detail 截断显式 assert** (`reject_reason[:256] + '...'` if len > 256, R2 BA-10/QA-9)
- [ ] **T-schema.8b** *(R2 NEW per BA-2)* 单元测试: forgejo_approval_comment_id UNIQUE INDEX 双写 race → 第二次 INSERT 抛 IntegrityError
- [ ] **T-schema.9** 单元测试: list_stuck_s7 边界 (now-7d-1s 不命中 / now-7d+1s 命中 / state≠S7 不命中)
- [ ] **T-schema.10** 单元测试: FailReason enum 接受 2 新值
- [ ] **T-schema.11** *(R2 NEW per AI-1)* 单元测试: update_last_polled_comment_id atomic + cross-restart 持久 (mock subprocess restart, query last_polled_comment_id 不丢)

#### T-pr-timing — PR 时序前移 (~5-9h post-R2)

- [ ] **T-pr-timing.1** `extension._handle_s6_review` PASS 末端调用 `forgejo.create_pr(branch, title, body)` → 写 dispatches.pr_id → 转移 S7
- [ ] **T-pr-timing.1b** *(R2 NEW per BA-4)* create_pr 失败路由: 5xx/network → stay-S6 (return None, retry next tick) + **幂等检查** (重试前 GET /repos/.../pulls?head=branch 检查是否已有 open PR → 有则复用 pr_id);4xx → S_FAIL(INFRASTRUCTURE 或新增 PR_CREATION_FAILED 待 OD)
- [ ] **T-pr-timing.2** `extension._handle_s8_merge` 移除 create_pr 调用,只 `forgejo.merge_pr(dispatches.pr_id)`
- [ ] **T-pr-timing.3** 更新 extension.py:2024 注释 (移除 "S6→S8 deferred M4 OD-9" stale text)
- [ ] **T-pr-timing.4** transitions.py 注释 (line 319 同步) 更新
- [ ] **T-pr-timing.5** 单元测试 (3 variants per R2 BA-4): (a) S6 PASS happy path → pr_id 写入 → S7 transition (mock ForgejoClient);(b) create_pr 5xx → stay-S6, 下一 tick 检查幂等不双写;(c) create_pr 4xx → S_FAIL
- [ ] **T-pr-timing.6** 单元测试: S8 merge 不调用 create_pr (mock ForgejoClient assert called_once_with merge_pr)
- [ ] **T-pr-timing.7** *(R2 expanded per QA-13)* 回归测试: M3 ≥11-row v2 fixture replay 走完整 cycle (确保 pr_id 在 S6→S7 边界已写入);**显式 verify**: `tests/test_t12_s7_webhook.py test_46-test_53` (S7 fixture 不受影响) + `test_49` (S7→S8 with merged PR 假设 pr_id 已存,refactored _handle_s8_merge 必须通过) + `tests/test_state_machine_skeleton.py` S6→S7 路径 + `tests/test_t1_extension_integration.py` end-to-end

#### T-comment-poll — Forgejo PR 评论 polling + magic-string parser (~7-11h post-R2)

- [ ] **T-comment-poll.1** *(R2 expanded per AI-7)* owner_username config schema 设计 + 加载: `.aria/orchestrator-config.yaml` 新字段 `authorized_approvers: list[str]` (M4 单元素 [owner],M5 加 reviewer 非 ABI break);加载顺序 file-first env-override (ARIA_AUTHORIZED_APPROVERS 逗号分隔 override file)
- [ ] **T-comment-poll.2** `comment_poll.py` 新模块: `scan_pending_s7_dispatches() -> list[Dispatch]`
- [ ] **T-comment-poll.3** `comment_poll.py`: `fetch_new_comments(forgejo, pr_id, since_comment_id) -> list[Comment]` (复用 ForgejoCliClient + **pagination 内部循环 page 直至无新评论** per R2 AI-1)
- [ ] **T-comment-poll.4** `comment_poll.py`: `parse_magic_string(comment) -> Decision | None` (strict regex,R2 fix QA-1/AI-8)
  - **regex flags**: `re.MULTILINE` 启用 (评论可能多行) + **case-sensitive** (大写变体 reject)
  - `^/aria approve\s*$` → `Decision('approve', None)`
  - `^/aria reject:\s*(.+)$` → `Decision('reject', reason=$1)` (reason 可含 `:` 或换行,greedy 匹配到行尾)
  - `^/aria reject\s*$` → `None` + side-effect "need reason" reply (POST helpful comment;**bot username 必须 ≠ owner** per QA-8)
  - **不命中 cases**: `> /aria approve` (引用块 — `^` 前 `> `);`/ARIA APPROVE` (大写);`/ａｒｉａ` (Unicode 同形);markdown code fence 中 ` ```/aria approve``` ` (虽 regex 命中但是 false positive — owner 教育文档化)
- [ ] **T-comment-poll.4b** *(R2 NEW per AI-2)* `comment.type == "comment"` filter (skip Forgejo `review`/`activity`/`commit-pushed` pseudo-event);若无 type 字段则 fallback 'has body 且非 system author'
- [ ] **T-comment-poll.5** owner-username 验证: `comment.user.login == config.owner_username` (case-sensitive exact match,R2 QA-7)
- [ ] **T-comment-poll.5a** *(R2 NEW per BA-6)* live-verify Forgejo API GET issue/PR comments response shape: assert `user.login` 字段存在 (vs `user.username`);记录 verified field name in AD-M4-2;regression test fixture 用真实 API response shape
- [ ] **T-comment-poll.6** *(R2 LOCKED per TL-4/BA-7/QA-12/AI-1)* 主循环 = **独立 30s cron job** (非 reconciler 30min cadence;独立 nomad job spec `aria-layer1-comment-poll.nomad.hcl`,additive on existing reconcile spec);AD-M4-9 锁定
- [ ] **T-comment-poll.6b** *(R2 NEW per AI-3)* first-decision-wins 语义: dispatch 已有 human_decision IS NOT NULL → 后续命中评论(即使被编辑/删除)全部忽略;Feishu 二次告警 'decision frozen, edits ignored'
- [ ] **T-comment-poll.6c** *(R2 NEW per BA-8/AI-1)* last_polled_comment_id 持久化: 每次 poll 后 `repo.update_last_polled_comment_id(dispatch_id, max_comment_id_processed)`;polling 启动时读取 last_polled_comment_id 作为 since 起点
- [ ] **T-comment-poll.7** 幂等性: `forgejo_approval_comment_id` UNIQUE partial index (003 migration) 守护双评论 race;dispatch UNIQUE partial index uq_issue_active_partial 已存
- [ ] **T-comment-poll.8** *(R2 expanded per QA-1)* 单元测试 fixture table ≥12 cases:
  - (1) `/aria approve` → approve
  - (2) `/aria reject: bug X` → reject('bug X')
  - (3) `/aria reject` → None + "need reason" reply
  - (4) `> /aria approve` (引用块) → None
  - (5) `/ARIA APPROVE` (大写) → None
  - (6) `/ａｒｉａ approve` (Unicode 同形) → None
  - (7) `/aria approve\n` 带尾换行 → approve
  - (8) `/aria reject:\nbug X\nbug Y` (多行 reason) → reject('bug X') *(R3-trivial fix per AI-R2-3/QA-NF-2: regex `^/aria reject:\s*(.+)$` 默认 `.` 不匹配 `\n`,**MULTILINE flag 仅改 `^` `$` 行为**;case 8 仅捕获首行 'bug X'。多行 reason 不支持 — 若 owner 需要详细 reason 应单行 用 `;` 分隔。AD-M4-2 显式记录此 limitation)*
  - (9) `/aria reject: reason with: colons` → reject('reason with: colons')
  - (10) ` /aria approve` 前导空格 → None (`^` anchor)
  - (11) `/aria approve garbage` → None (`\s*$` 不容忍非空白尾)
  - (12) ``` ```/aria approve``` ``` markdown code fence → 命中(documented limitation, owner 教育)
- [ ] **T-comment-poll.9** *(R2 expanded per QA-7)* 单元测试: owner-username 仿冒评论被拒,**6 case**:
  - (a) 完全不同 username (基线)
  - (b) 大写变体 'Owner' vs 'owner' → reject
  - (c) 尾随空格 'owner ' → reject
  - (d) Unicode 同形 → reject
  - (e) 用户改名后历史评论 → reject (Forgejo 返回当前 username)
  - (f) bot username 自身评论 → reject (避免 reply-loop, R2 QA-8)
- [ ] **T-comment-poll.10** *(R2 expanded per QA-8)* 单元测试: `/aria reject` 无 reason → 触发 "need reason" reply + dispatch 状态不变;**bot 评论不触发 reply-loop**: bot 用专用 PAT 账户 `aria-bot`,polling filter `comment.user.login == bot_username` 跳过自身;assert `last_polled_comment_id` 推进过 bot 自身评论
- [ ] **T-comment-poll.11** Integration test: 模拟 Forgejo PR + comment seed → poll → assert S7→S8 OR S7→S_FAIL
- [ ] **T-comment-poll.12** *(R2 NEW per AI-3)* 单元测试: 评论编辑/删除 first-decision-wins 验证 — (a) approve 后 owner 编辑同 comment.id 为 reject:body → polling 拿到但拒绝二次消费;(b) approve 后 owner 删除评论 → polling 已记录 forgejo_approval_comment_id 不破坏 evidence 链
- [ ] **T-comment-poll.13** *(R2 NEW per AI-2)* 单元测试: review-event payload (`comment.type == "review"`) → parser 跳过;commit-pushed pseudo-event → 跳过

#### T-reject-flow — reject_reason 持久化 + S_FAIL routing + Feishu 二次告警 (~3-5h post-R2)

- [ ] **T-reject-flow.0** *(R2 NEW per BA-3)* verify extension.py:105 ALLOWED_TRANSITIONS dict — `S7_HUMAN_GATE` 当前 ['S8_MERGE'] only,M4 必须扩展为 ['S8_MERGE', 'S_FAIL'] (虽 S_FAIL 是 universal sink 但 dict 校验函数读 dict);在 T-schema.6b 完成
- [ ] **T-reject-flow.1** transitions.py 加 S7_HUMAN_GATE → S_FAIL(human_reject) 转移 (fail_reason='human_reject', **fail_detail=reject_reason[:256] + '...' if len > 256 else reject_reason** per R2 BA-10/QA-9 显式截断 indicator)
- [ ] **T-reject-flow.2** Feishu reject 二次告警: `feishu_webhook.send_reject_alert(dispatch_id, reject_reason)` 复用 outbound (fire-and-forget;reject_reason markdown sanitize per R2 AI-4 — escape `[]()` 等 markdown 控制字符)
- [ ] **T-reject-flow.3** 单元测试: reject decision → human_decision='reject' + reject_reason 持久化 (uncapped) + fail_detail 截断断言 (≤ 256 chars + 'truncated' 标识) + Feishu 调用断言 + S_FAIL 转移

#### T-reconciler — Reconciler S7 stuck 分支 (~4-6h)

- [ ] **T-reconciler.1** `reconciler.py` 加 `_detect_stuck_s7_human_gate()` 方法,调用 `repo.list_stuck_s7(threshold_days=7)`
- [ ] **T-reconciler.2** *(R2 fix BA-5)* 触发 `repo.cas_mark_failed_stuck(expected_state='S7_HUMAN_GATE', fail_reason=FailReason.HUMAN_TIMEOUT, ...)` (CAS expected_state 参数显式传 'S7_HUMAN_GATE' 防 race) + Feishu 二次告警 (复用 `feishu_webhook.send_timeout_alert`,fire-and-forget)
- [ ] **T-reconciler.3** `reconcile_runner.py` 主循环加 S7 stuck 分支 (与 S5_AWAIT stuck 并列)
- [ ] **T-reconciler.4** *(R2 corrected per QA-5)* 单元测试 (timestamp-comparison 模式,**不**用 AdvancingClock 推进 336 ticks): 插入 row with `human_gate_entered_at = clock.now() - timedelta(days=7, seconds=1)` → 单次调 `_detect_stuck_s7_human_gate()` → assert dispatch transitioned to S_FAIL(human_timeout) + Feishu 调用断言 (验收 B Tier-1 fake-cycle test;镜像 M3 test_t6_reconciler.py timestamp-comparison 模式)
- [ ] **T-reconciler.5** 单元测试: now-7d-1s 不触发 / now-7d+1s 触发 (边界精确)
- [ ] **T-reconciler.6** 单元测试 (R2 BA-5 强化): dispatch 在 list_stuck_s7 与 cas_mark_failed_stuck 之间 transition 到 S8 → CAS expected_state='S7_HUMAN_GATE' 不匹配 → CAS 返回 0 → 不误标 HUMAN_TIMEOUT (race 守护实证)

#### T-risk-stub — risk_tier_stub 接口契约 (~2-3h)

- [ ] **T-risk-stub.1** S7_HUMAN_GATE 入口写 `risk_tier_stub = 'always'` (DEFAULT 已在 schema, transitions 显式写入留 ABI 锚点)
- [ ] **T-risk-stub.2** AD-M4-6 决策记录 (M5 ABI 兼容承诺): 列名改 `risk_tier_stub` → `risk_tier` 在 M5 必须 ADD 新列 + UPDATE backfill,不 DROP;默认值 `'always'` 在 M5 仍保留为合法 enum 值 ("all dispatches require approval")
- [ ] **T-risk-stub.3** 单元测试: 进入 S7 → assert risk_tier_stub='always';查询 list_stuck_s7 不依赖该列 (interface 解耦)

#### T-acceptance — Acceptance 实测 (~5-7h post-R2 含 Tier 拆分)

- [ ] **T-acceptance.A.1** *(R2 split per QA-6/AI-6)* SLO 公式正确性 (Tier-1 synthetic): fake-cycle 注入 ≥5 dispatches with `decision_at = entered_at + Δ`,assert `median(Δ) < 10min` SQL/Python 公式正确;**不**测真实 polling latency
- [ ] **T-acceptance.A.2** *(R2 split, 推迟 Tier-2)* SLO 真实人决策延迟 (Tier-2 real-dispatch): T-deploy 后 owner 实操 ≥3 dispatches → `median(decision_at - human_gate_entered_at) < 10min` 实测;推迟到 Phase B.3 acceptance window 或 Phase D.2 收尾验证
- [ ] **T-acceptance.B** *(R2 corrected per QA-5)* 7d auto-reject Tier-1 fake-cycle (验收 B): timestamp-comparison 模式 — 插入 row with `human_gate_entered_at = clock.now() - 7d - 1s` → 单次调 reconciler → outcome=S_FAIL(human_timeout) + Feishu 二次告警 + fail_reason='human_timeout' assert (**不**用 AdvancingClock 推进 336 ticks)
- [ ] **T-acceptance.C** *(R2 expanded per QA-3/AI-10)* 幂等性 Tier-1 (验收 C): (a) **subprocess SIGKILL**: `subprocess.Popen(hermes-cli) + os.kill(SIGKILL) + restart 新 subprocess + 共享 DB` → Feishu Fake Webhook call count == 1 (**not** in-process Extension re-instantiation);(b) 双 PR 评论 race → human_decision 仅写一次 (forgejo_approval_comment_id UNIQUE INDEX 守护);(c) Hermes restart with `last_polled_comment_id` wiped → DB 持久化保护,不重发 'need reason' 提示评论
- [ ] **T-acceptance.D.1** ≥3 dispatches Tier-1 完整 cycle (Tier-1 fake): 含 ≥1 approve + ≥1 reject + ≥1 timeout 路径覆盖
- [ ] **T-acceptance.D.2** *(R2 split, 推迟 Tier-2)* ≥2 dispatches Tier-2 real (T-deploy 后): owner 实操 ≥1 approve + ≥1 reject (timeout 难真实复现, Tier-1 即可)
- [ ] **T-acceptance.E** *(R2 expanded per QA-10)* Schema v3 backward-compat (验收 E): M3 ≥11-row v2 fixture (**含 ≥1 row in S7_HUMAN_GATE + ≥1 in S9_CLOSE + ≥1 in S_FAIL** 三类必备) migrate 零数据丢失 + 7 新列 present (含 last_polled_comment_id) + fail_reason 2 新值 self-doc + schema_version 3.0 + UNIQUE INDEX uq_approval_comment created
- [ ] **T-acceptance.F** PRD reframe 三处 (验收 F): line 405-406 + §170 + US-025 表 + **§409 总预算 reconciliation 算术校验** (T-prd-reframe 完成时同步 close, R2 TL-3)

#### T-docs — Docs (~5-7h post-R2 含 4 新 AD slots)

- [ ] **T-docs.1** *(R2 expanded per TL-1/TL-4/TL-6/AI-7)* AD-M4-1~**AD-M4-11** 决策记录回填 (含 R2 NEW: AD-M4-8 cross-cutting idempotency / AD-M4-9 polling cadence 30s 独立 cron / AD-M4-10 m4-handoff additive + abi_compat_promises forward-binding / AD-M4-11 owner_username config + list 预埋 M5)
- [ ] **T-docs.2** m4-handoff.yaml schema v1.0 (additive on m3-handoff schema, 复用 M2 T16 模式) + **abi_compat_promises 字段** (per R2 TL-10: 显式列 risk_tier_stub→risk_tier additive-only, M5 spec drafter 必读)
- [ ] **T-docs.3** validate-m4-handoff.py (stdlib, 同 M2 T16.2 模式;复用 m3 validator 95% 代码) + **abi_compat_promises 强制 cross-reference 检查** (M5 spec drafting 时若未引用则 validator 报错)
- [ ] **T-docs.4** aria-layer1 README S7 human gate 章节 (含 magic-string protocol + owner-username + 7d timeout + 30s polling cadence + first-decision-wins 语义) + **known limitations** 章节 (R3-trivial per AI-R2-1/QA-NF-1): (a) markdown code fence 中 `/aria approve` 会被 strict regex 命中 — owner 教育 不在评论中黏 code fence 含 magic-string;(b) `/aria reject:` reason 仅支持单行,多行 reason 用 `;` 分隔
- [ ] **T-docs.5** README.md 主仓 + aria-orchestrator submodule 版本号同步 (post-Phase D)

#### T-prd-reframe — PRD 文档同步 (~2-4h post-R2)

- [ ] **T-prd-reframe.1** PRD line 405-406 reframe (M4=Human gate / M5=Replay+Reconciler+防漂移+Review loop+审计日志 immutable)
- [ ] **T-prd-reframe.2** PRD §170 reframe (S7 双语义: Feishu=入口 + Forgejo PR 评论=决策真理来源)
- [ ] **T-prd-reframe.3** *(R2 expanded per TL-7)* PRD §User Stories 表 line 567 (US-025 标题更新含 carryover);**渲染验证**: 截图对比 GitHub + Forgejo 表渲染,若超列宽 → ASCII line break 或 footnote 拆分
- [ ] **T-prd-reframe.4** *(R2 expanded per TL-3)* PRD §409 总预算 845h **reconciliation 算术校验**: 列 M0-M6 旧 vs 新 effort 表 (M4 旧 80h → 新 60h, M5 旧 100h → 新 ~120h, 净增 ≈0),确认 845h 总和差距 ≤ ±10h 或显式标 reframe rationale

#### T-deploy — Owner deploy (~3-4h owner-only post-R2)

- [ ] **T-deploy.1** Aether Nomad Variables 配置 `ARIA_FEISHU_WEBHOOK_URL` (`nomad var put ... >/dev/null 2>&1` 同 secret-hygiene 规范 #7)
- [ ] **T-deploy.2** Aether Nomad Variables 配置 `ARIA_FEISHU_SIGNING_SECRET` (同上)
- [ ] **T-deploy.3** *(R2 expanded per AI-7)* `authorized_approvers` 配置项写入 (`.aria/orchestrator-config.yaml` `authorized_approvers: ["owner-username"]`,Aether config map 或 Nomad Variables file-based)
- [ ] **T-deploy.4** aria-layer1 nomad job 重启 + Consul service health check pass
- [ ] **T-deploy.4b** *(R2 NEW per AD-M4-9)* 部署独立 `aria-layer1-comment-poll.nomad.hcl` (30s cron) + Consul service health check
- [ ] **T-deploy.5** 6 mandatory feishu+hermes configs 复检 (memory `feedback_feishu_hermes_gotchas` 引用)
- [ ] **T-deploy.5b** *(R2 NEW per AI-5)* SQLite version probe: `sqlite3 .aria/dispatches.db 'SELECT sqlite_version();'` 记录 Aether image SQLite 版本;若 < 3.25 → 记入 AD-M4-6 environmental note (M5 RENAME 不可用,但 ABI 承诺无 RENAME 需求所以兼容)
- [ ] **T-deploy.6** *(R2 NEW per AD-M4-2 BA-6)* live verify Forgejo API GET issue/PR comments response shape: `forgejo GET /repos/{repo}/issues/{n}/comments` → assert `user.login` 字段存在;记录 verified field name in AD-M4-2 environmental note

### Phase B.3 — pre_merge audit (~4h)

- [ ] **B.3.1** R1 4-agent multi-agent pre_merge audit (Level 3 → challenge mode)
  - 验证 6 验收 criteria 全 PASS (实测,非声明)
  - 验证 schema v3 migration 0 数据丢失
  - 验证 magic-string parser 边界鲁棒性
  - 验证 7d timeout 跨重启不丢
  - 验证 PRD reframe 三处一致
  - 验证 m4-handoff.yaml 同 m3 schema 兼容
- [ ] **B.3.2** R2/R3 fix-verify + 稳定性确认轮 (per `feedback_audit_convergence_pattern` + `feedback_premerge_iteration_pattern`)
- [ ] **B.3.3** STABLE convergence 确认 (R_N == R_{N-1} + 0 findings)

---

## Phase C: 集成

### Phase C.1 — Commit (~2h)

- [ ] **C.1.1** strategic commit grouping (per Aria #1 + 各任务组 atomic commit)
- [ ] **C.1.2** 双 submodule 同步 (aria-orchestrator + 主仓 pointer bump)

### Phase C.2 — Merge (~3h)

- [ ] **C.2.1** Forgejo PR 创建 (single-PR-per-spec 同 M3 模式)
- [ ] **C.2.2** PR audit 收敛 + merge
- [ ] **C.2.3** 主仓 PR + merge
- [ ] **C.2.4** post-merge SHA verify (双远程 parity)
- [ ] **C.2.5** 双远程推送 enforced (origin + github,per Aria #1.4 governance — phase-c-integrator C.2.5 自动)

---

## Phase D: 收尾

### Phase D.1 — 进度更新 (~1h)

- [ ] **D.1.1** UPM 进度更新 (US-024 status: pending → done with verdict)
- [ ] **D.1.2** AB benchmark 决策 (M4 是否引入 Skill 变更?若否 → Level 2 patch 豁免 per `feedback_level2_patch_no_benchmark`)

### Phase D.2 — Spec archive (~1h)

- [ ] **D.2.1** Spec archive `openspec/archive/2026-XX-XX-aria-2.0-m4-human-gate-feishu-approval/`
- [ ] **D.2.2** retrospective: M4 component sum vs 60h baseline 实测对比 (M2 ×1.06 / M3 ×2.06 inflation pattern 校验)
- [ ] **D.2.3** memory commit (project_us024_m4_closeout_2026-XX-XX.md)
- [ ] **D.2.4** US-025 (M5) brainstorm 准入 (M4 carryover 如有 → US-025 scope 输入)

---

## Status Table (R2 expanded)

| Phase | Tasks | Done | Pending | Blocked |
|-------|-------|------|---------|---------|
| A.1 | 7 | 5 | 2 (A.1.6 owner-action, A.1.7 完成于 T-comment-poll.1) | - |
| A.2 | 6 | 6 (R1+R2 全完成,R3+R4 collapsed per OD-15) | 0 | DONE |
| A.3 | 5 | 4 | 1 (A.3.5 owner action — Forgejo M4 kickoff issue) | A.2 done |
| B.1 | 2 | 0 | 2 | A.3 done |
| B.2 | ~110 (R2: T-schema +5 / T-pr-timing +1 / T-comment-poll +5 / T-reject-flow +1 / T-reconciler +1 / T-acceptance +3 / T-docs +0 增强 / T-prd-reframe +0 增强 / T-deploy +3) | 0 | ~110 | B.1 done |
| B.3 | 3 | 0 | 3 | B.2 done |
| C.1 | 2 | 0 | 2 | B.3 STABLE |
| C.2 | 5 | 0 | 5 | C.1 done |
| D.1 | 2 | 0 | 2 | C.2 merged |
| D.2 | 4 | 0 | 4 | D.1 done |
| **Total** | **~146** | **9** | **~137** | - |

**R2 增量总结**: 30 新子任务(critical 修复 + important fix + AD-M4-8/9/10/11 4 新 slot 派生);component sum mid 保持 ~50-55h (+3-5h vs R1) / upper ~65-70h (接近 OD-M4-1 trigger 边界 72h, A.3 须显式 reconcile)。

---

## Owner action items (前置 / 阻塞 inline)

- [ ] A.1.6: Forgejo M4 kickoff issue 创建 (推 Phase B.1)
- [ ] A.3.5: 同上,owner action 触发
- [ ] T-deploy.1~5: Aether 部署配置 (推 Phase B.3 acceptance 实测)
- [ ] (post-merge) Feishu 6 mandatory configs 复检 (memory 防御)
