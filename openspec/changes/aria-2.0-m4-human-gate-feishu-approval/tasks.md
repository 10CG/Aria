# aria-2.0-m4-human-gate-feishu-approval — Tasks

> **Spec**: [proposal.md](./proposal.md)
> **Status**: Draft (Phase A.1 起草中,2026-05-07)
> **Baseline**: 60h hard (per brainstorm Q8' β');**OD-M4-1 reframe trigger @ 72h**
> **Audit pattern**: 同 M3 OD-15 collapse (Phase A.2 R1+R2,Phase B.3 pre_merge 3-4 round 严格收敛,Phase D 1 round)

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

### Phase A.2 — post_spec audit (~4h)

- [ ] **A.2.1** R1 4-agent multi-agent audit 触发 (backend-architect / qa-engineer / tech-lead / ai-engineer parallel, Level 3 → challenge mode per audit-engine adaptive)
  - 验证 Q1-Q14 brainstorm 决议是否 spec 内充分体现
  - 验证 6 验收 criteria 量化可测性
  - 验证 7 OOS 边界清晰
  - 验证 60h baseline 与任务拆解一致 (若 sum > 72h 触发 OD-M4-1)
  - 验证 PRD §170 / line 405-406 / US-025 reframe 三处一致
  - 验证 schema v3 additive 不破坏 M3 v2 ABI
  - 验证 magic-string parser 对 owner-username 仿冒 / `/aria reject` 缺 reason 等边界鲁棒
- [ ] **A.2.2** R1 audit report `.aria/audit-reports/post_spec-R1-2026-05-XXTXXXXZ-us024-m4.md`
- [ ] **A.2.3** R1 fix batch (proposal/tasks 修订)
- [ ] **A.2.4** R2 fix-verify (R1 closure + 0 NEW critical/important + coherence PASS)
- [ ] **A.2.5** R2 closeout report
- [ ] **A.2.6** R3+R4 collapse if R2 SCOPE_OK (同 M3 OD-15 模式)

### Phase A.3 — Approved 准入 (~1h)

- [ ] **A.3.1** baseline final lock (60h or OD-M4-1 reframe value)
- [ ] **A.3.2** **OD-M4-1** (if triggered): `.aria/decisions/2026-05-XX-od-m4-1-baseline-reframe.md` + PRD line 405-406 patch (or 隐式 60h 锁)
- [ ] **A.3.3** Spec proposal.md Status: Draft → **Approved**
- [ ] **A.3.4** AD-M4-1~AD-M4-7 slot 回填 (主责 agent column)
- [ ] **A.3.5** Forgejo Issue T0.1 创建 (推 Phase B.1)

---

## Phase B: 开发

### Phase B.1 — feature 分支 (~0.5h)

- [ ] **B.1.1** 主仓 + aria-orchestrator submodule 同名 feature 分支创建: `feature/aria-2.0-m4-human-gate-feishu-approval`
- [ ] **B.1.2** 双远程 push (origin + github) — state-snapshot 验证 4 repos 双 remote `parity=equal`

### Phase B.2 — 实施 (~50h component-sum)

#### T-schema — Schema migration v3 additive (~6-8h)

- [ ] **T-schema.1** `schema.sql` 加 6 列 + 2 fail_reason 注释更新 + schema_version "3.0" + migration_notes 003 INSERT
- [ ] **T-schema.2** `migrations/003_schema_v3_additive.sql` 写 ALTER TABLE 6 列 + UPDATE schema_meta + INSERT migration_notes
- [ ] **T-schema.3** `db.py from_row` + `Dispatch` dataclass 加 6 字段 (forward-compatible per 既有 from_row 模式)
- [ ] **T-schema.4** `db.py update_human_decision(dispatch_id, decision, decision_at, reject_reason=None, comment_id=None)` 新方法 (atomic single-row UPDATE)
- [ ] **T-schema.5** `db.py list_stuck_s7(threshold_days=7)` 新方法 (用于 reconciler 扩展)
- [ ] **T-schema.6** `interfaces.py FailReason` enum 加 `HUMAN_REJECT='human_reject'` + `HUMAN_TIMEOUT='human_timeout'`
- [ ] **T-schema.7** 单元测试: 11+ row v2 fixture migrate 通过零数据丢失 (验收 E)
- [ ] **T-schema.8** 单元测试: update_human_decision 各 decision 路径 + reject_reason 持久化 + comment_id UNIQUE 守护
- [ ] **T-schema.9** 单元测试: list_stuck_s7 边界 (now-7d-1s 不命中 / now-7d+1s 命中 / state≠S7 不命中)
- [ ] **T-schema.10** 单元测试: FailReason enum 接受 2 新值

#### T-pr-timing — PR 时序前移 (~4-8h)

- [ ] **T-pr-timing.1** `extension._handle_s6_review` PASS 末端调用 `forgejo.create_pr(branch, title, body)` → 写 dispatches.pr_id → 转移 S7
- [ ] **T-pr-timing.2** `extension._handle_s8_merge` 移除 create_pr 调用,只 `forgejo.merge_pr(dispatches.pr_id)`
- [ ] **T-pr-timing.3** 更新 extension.py:2024 注释 (移除 "S6→S8 deferred M4 OD-9" stale text)
- [ ] **T-pr-timing.4** transitions.py 注释 (line 319 同步) 更新
- [ ] **T-pr-timing.5** 单元测试: S6 PASS → pr_id 写入 → S7 transition (mock ForgejoClient)
- [ ] **T-pr-timing.6** 单元测试: S8 merge 不调用 create_pr (mock ForgejoClient assert called_once_with merge_pr)
- [ ] **T-pr-timing.7** 回归测试: M3 ≥11-row v2 fixture replay 走完整 cycle (确保 pr_id 在 S6→S7 边界已写入)

#### T-comment-poll — Forgejo PR 评论 polling + magic-string parser (~6-10h)

- [ ] **T-comment-poll.1** owner_username config schema 设计 + 加载 (`.aria/orchestrator-config.yaml` 新字段;A.1 决策位置)
- [ ] **T-comment-poll.2** `comment_poll.py` 新模块: `scan_pending_s7_dispatches() -> list[Dispatch]`
- [ ] **T-comment-poll.3** `comment_poll.py`: `fetch_new_comments(forgejo, pr_id, since_comment_id) -> list[Comment]` (复用 ForgejoCliClient)
- [ ] **T-comment-poll.4** `comment_poll.py`: `parse_magic_string(comment) -> Decision | None` (strict regex)
  - `^/aria approve\s*$` → `Decision('approve', None)`
  - `^/aria reject:\s*(.+)$` → `Decision('reject', reason=$1)`
  - `^/aria reject\s*$` → `None` + side-effect "need reason" reply (POST helpful comment)
- [ ] **T-comment-poll.5** owner-username 验证: `comment.user.login == config.owner_username` (PAT scope 已实证模式)
- [ ] **T-comment-poll.6** 主循环 (集成到 reconciler 或独立 cron job — A.1 决策): 每 30s scan + parse + apply
- [ ] **T-comment-poll.7** 幂等性: `forgejo_approval_comment_id` UNIQUE 守护双评论 race;dispatch UNIQUE partial index 已存
- [ ] **T-comment-poll.8** 单元测试: parse_magic_string 边界 (大小写敏感 / 空格容忍 / 反引号 / emoji / 多行)
- [ ] **T-comment-poll.9** 单元测试: owner-username 仿冒评论被拒 (assert no state transition)
- [ ] **T-comment-poll.10** 单元测试: `/aria reject` 无 reason → 触发 "need reason" reply + dispatch 状态不变
- [ ] **T-comment-poll.11** Integration test: 模拟 Forgejo PR + comment seed → poll → assert S7→S8 OR S7→S_FAIL

#### T-reject-flow — reject_reason 持久化 + S_FAIL routing + Feishu 二次告警 (~2-4h)

- [ ] **T-reject-flow.1** transitions.py 加 S7_HUMAN_GATE → S_FAIL(human_reject) 转移 (fail_reason='human_reject', fail_detail=reject_reason 前 256 chars)
- [ ] **T-reject-flow.2** Feishu reject 二次告警: `feishu_webhook.send_reject_alert(dispatch_id, reject_reason)` 复用 outbound (fire-and-forget)
- [ ] **T-reject-flow.3** 单元测试: reject decision → human_decision='reject' + reject_reason 持久化 + Feishu 调用断言 + S_FAIL 转移

#### T-reconciler — Reconciler S7 stuck 分支 (~4-6h)

- [ ] **T-reconciler.1** `reconciler.py` 加 `_detect_stuck_s7_human_gate()` 方法,调用 `repo.list_stuck_s7(threshold_days=7)`
- [ ] **T-reconciler.2** 触发 `repo.cas_mark_failed_stuck(fail_reason=FailReason.HUMAN_TIMEOUT)` + Feishu 二次告警 (复用 `feishu_webhook.send_timeout_alert`)
- [ ] **T-reconciler.3** `reconcile_runner.py` 主循环加 S7 stuck 分支 (与 S5_AWAIT stuck 并列)
- [ ] **T-reconciler.4** 单元测试: AdvancingClock 推进 7d → mock dispatch transitioned to S_FAIL(human_timeout) + Feishu 调用断言 (验收 B Tier-1 fake-cycle test)
- [ ] **T-reconciler.5** 单元测试: now-7d-1s 不触发 / now-7d+1s 触发 (边界精确)
- [ ] **T-reconciler.6** 单元测试: dispatch 已在 S8 / S9_CLOSE / S_FAIL → 不再 stuck-mark (CAS 锁实证)

#### T-risk-stub — risk_tier_stub 接口契约 (~2-3h)

- [ ] **T-risk-stub.1** S7_HUMAN_GATE 入口写 `risk_tier_stub = 'always'` (DEFAULT 已在 schema, transitions 显式写入留 ABI 锚点)
- [ ] **T-risk-stub.2** AD-M4-6 决策记录 (M5 ABI 兼容承诺): 列名改 `risk_tier_stub` → `risk_tier` 在 M5 必须 ADD 新列 + UPDATE backfill,不 DROP;默认值 `'always'` 在 M5 仍保留为合法 enum 值 ("all dispatches require approval")
- [ ] **T-risk-stub.3** 单元测试: 进入 S7 → assert risk_tier_stub='always';查询 list_stuck_s7 不依赖该列 (interface 解耦)

#### T-acceptance — Acceptance 实测 (~4-6h)

- [ ] **T-acceptance.A** SLO median test (验收 A): N≥5 synthetic dispatches → median(decision_at - human_gate_entered_at) < 10min assert
- [ ] **T-acceptance.B** 7d auto-reject Tier-1 fake-cycle (验收 B): AdvancingClock 推进 7d → outcome=S_FAIL(human_timeout) + Feishu 二次告警 + fail_reason='human_timeout' assert
- [ ] **T-acceptance.C** 幂等性 Tier-1 (验收 C): SIGKILL mid-S7 + restart → Feishu 不二次发送;双 PR 评论 → human_decision UNIQUE
- [ ] **T-acceptance.D** ≥5 dispatches 完整 cycle (验收 D): 含 ≥1 approve + ≥1 reject + ≥1 timeout 路径覆盖
- [ ] **T-acceptance.E** Schema v3 backward-compat (验收 E): M3 ≥11-row v2 fixture migrate 零数据丢失 + 6 新列 present + fail_reason 2 新值 + schema_version 3.0
- [ ] **T-acceptance.F** PRD reframe 三处 (验收 F): line 405-406 + §170 + US-025 表 (T-prd-reframe 完成时同步 close)

#### T-docs — Docs (~4-6h)

- [ ] **T-docs.1** AD-M4-1~AD-M4-7 决策记录回填 (`aria-orchestrator/docs/architecture-decisions.md`)
- [ ] **T-docs.2** m4-handoff.yaml schema v1.0 (additive on m3-handoff schema, 复用 M2 T16 模式)
- [ ] **T-docs.3** validate-m4-handoff.py (stdlib, 同 M2 T16.2 模式;复用 m3 validator 95% 代码)
- [ ] **T-docs.4** aria-layer1 README S7 human gate 章节 (含 magic-string protocol + owner-username + 7d timeout)
- [ ] **T-docs.5** README.md 主仓 + aria-orchestrator submodule 版本号同步 (post-Phase D)

#### T-prd-reframe — PRD 文档同步 (~2-3h)

- [ ] **T-prd-reframe.1** PRD line 405-406 reframe (M4=Human gate / M5=Replay+Reconciler+防漂移+Review loop+审计日志 immutable)
- [ ] **T-prd-reframe.2** PRD §170 reframe (S7 双语义: Feishu=入口 + Forgejo PR 评论=决策真理来源)
- [ ] **T-prd-reframe.3** PRD §User Stories 表 line 567 (US-025 标题更新含 carryover)
- [ ] **T-prd-reframe.4** PRD §409 总预算更新 (845h baseline 校验,M4 60h 占比 7.1%)

#### T-deploy — Owner deploy (~2-3h owner-only)

- [ ] **T-deploy.1** Aether Nomad Variables 配置 `ARIA_FEISHU_WEBHOOK_URL` (`nomad var put ... >/dev/null 2>&1` 同 secret-hygiene 规范)
- [ ] **T-deploy.2** Aether Nomad Variables 配置 `ARIA_FEISHU_SIGNING_SECRET` (同上)
- [ ] **T-deploy.3** owner_username 配置项写入 (Aether config map 或 Nomad Variables)
- [ ] **T-deploy.4** aria-layer1 nomad job 重启 + Consul service health check pass
- [ ] **T-deploy.5** 6 mandatory feishu+hermes configs 复检 (memory `feedback_feishu_hermes_gotchas` 引用)

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

## Status Table

| Phase | Tasks | Done | Pending | Blocked |
|-------|-------|------|---------|---------|
| A.1 | 7 | 5 | 2 (A.1.6 owner-action, A.1.7 推 T-comment-poll) | - |
| A.2 | 6 | 0 | 6 | A.1 done |
| A.3 | 5 | 0 | 5 | A.2 done |
| B.1 | 2 | 0 | 2 | A.3 done |
| B.2 | ~80 | 0 | ~80 | B.1 done |
| B.3 | 3 | 0 | 3 | B.2 done |
| C.1 | 2 | 0 | 2 | B.3 STABLE |
| C.2 | 5 | 0 | 5 | C.1 done |
| D.1 | 2 | 0 | 2 | C.2 merged |
| D.2 | 4 | 0 | 4 | D.1 done |
| **Total** | **~116** | **5** | **~111** | - |

---

## Owner action items (前置 / 阻塞 inline)

- [ ] A.1.6: Forgejo M4 kickoff issue 创建 (推 Phase B.1)
- [ ] A.3.5: 同上,owner action 触发
- [ ] T-deploy.1~5: Aether 部署配置 (推 Phase B.3 acceptance 实测)
- [ ] (post-merge) Feishu 6 mandatory configs 复检 (memory 防御)
