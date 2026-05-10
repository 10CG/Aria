# M5 Brainstorm Decisions — Aria 2.0 M5 (US-025)

> **Date**: 2026-05-10
> **Mode**: requirements (Aria brainstorm Phase A.0)
> **Topic**: Aria 2.0 M5 — Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable
> **Predecessor**: US-024 M4 (done 2026-05-09 + Track A T-deploy 2026-05-09)
> **Parent PRD**: [docs/requirements/prd-aria-v2.md](../../docs/requirements/prd-aria-v2.md) §M5 (Week 20-25, 120h baseline lock 2026-05-07)
> **Status**: Locked — ready for Phase A.1 spec-drafter

---

## Brainstorm 决策汇总 (10 个 Q)

| Q | 决策点 | 锁定 | 估时 |
|---|---|---|---|
| Q0 | abi_compat_promises 4 条 ACK | A — 全 ACK as M5 hard constraints | 0h |
| Q1 | M5 scope inventory | 5 PRD must-have (A-E) + F + G, H 推 M6 | (各项分别) |
| Q2 | G cron cadence 优化方向 | comment-poll direct transition | 6h |
| Q3-r | D Review loop 第三种状态 | hybrid (改稿 + 重做 owner 自由选 per-rework) | 50-55h |
| Q4 | rework round cap | 3 (合并 cap, 不区分 changes/redo 模式) | (含 D) |
| Q5 | E 审计日志 storage | SQLite 新表 + INSERT-only CHECK + DB triggers | 15h |
| Q6 | A Replay framework 范围 | Deterministic state replay (不重跑 LLM) | 10h |
| Q7 | F Risk-tier 算法深度 | schema dual-write only (算法推 M6) | 5h |
| Q8 | B Reconciler 深度增强 | Failure analysis + smart retry (LLM-driven) | 15h |
| Q9 | C Drift defense 范围 | Commit lint + Spec diff (LLM-driven) | 12h |

**M5 estimated total**: ~113-118h vs 120h baseline (under 2-7h headroom, OD-M5-1 trigger 144h 远未触及)

---

## Q0 — abi_compat_promises ACK (mandatory entry, AD-M4-10 enforced)

Owner ACK 全部 4 条作为 M5 设计硬约束。validate-m5-handoff.py 将强制 cross-reference。

**Promise #1: risk_tier_stub_to_risk_tier**
- M5 必须 ADD COLUMN risk_tier (不 RENAME, SQLite < 3.25 限制)
- 不 DROP risk_tier_stub (acceptable schema bloat)
- Transitionally dual-write
- Read 接口透明 hot-swap (db.py::get_risk_tier 单行修改)
- Q7 锁定后, M5 仅做 schema dual-write,算法推 M6

**Promise #2: forgejo_approval_comment_id_unique_index**
- uq_approval_comment UNIQUE partial index 是 M4 inbound 幂等性 P0 守卫
- M5 不得 DROP; schema migration 重建 index 必须保持 partial WHERE NOT NULL 语义

**Promise #3: comment_poll_cadence_independent**
- comment_poll 30s cron + reconciler 30min cron 是独立 Nomad job
- M5 不得合并到单 cron (会破坏 PRD §618 SLO < 10min target)
- Q2 锁 comment-poll direct transition 后 仍保留 comment-poll job 独立性 (不合并到其他 job)

**Promise #4: human_decision_first_decision_wins**
- first-decision-wins: dispatch.human_decision NOT NULL → 后续命中评论全部忽略
- M5 review-loop 必须保持; Request-Changes 用新 status enum (e.g. 'changes_requested') 而非允许 human_decision 多次写
- Q3-reframe 锁 hybrid 后, 'changes' 和 'redo' 都通过 NEW dispatch row 实现 rework, 同一 row 的 human_decision 一次性写入

---

## Q1 — M5 Scope Inventory (8 candidate items → 7 in M5 + 1 推 M6)

**PRD-mandated must-have (5 项, 锁定在 M5)**:
- **A. Replay / Differential testing framework** (M4-OS-3 carryforward)
- **B. Reconciler 深度增强** — LLM-decided routing + multi-state stuck detection (M4-OS-4)
- **C. 防漂移 / Drift defense** — commit lint + spec diff + LLM 自审 daily (M4-OS-5)
- **D. Review loop** — Request-Changes / Re-roll / PR review trinary (M4-OS-2)
- **E. 审计日志 immutable / replayable** (M4-OS-8)

**扩展候选 (锁 1 项 in M5, 1 项 in M5 浅, 1 项推 M6)**:
- **F. Risk-tier 真实分层** (M4-OS-1, abi_compat #1) — schema dual-write only, 算法 M6
- **G. cron cadence vs SLO** (Track A discovery 2026-05-09) — IN M5
- **H. aria-layer2-runner deploy** (Track A discovery 2026-05-09) — 推 M6 (deploy infra task,与 M5 features 异质,与 features 同 milestone 增加 context switching)

---

## Q2 — G cron cadence 优化方向

**锁定**: comment-poll direct transition (~6h)

comment_poll.py 在 update_human_decision 后**直接调** _handle_s7_human_gate, 不再依赖 cron 推进 S7→S8。

**理由**:
1. SLO 最优: 30s vs 30min tail, 远超 PRD §618 < 10min target
2. abi_compat #3 兼容: comment-poll 仍独立 cron job, 责任扩展不算合并
3. Cost 合理: ~6h vs ~2h (cron 加速) / ~4h (hybrid), 换 SLO 大幅 headroom
4. Reframe 是正向 governance: AD-M4-9 注释 "No state-machine transition writes" 是 M4 设计选择, M5 升级是合理演进 (per `feedback_spec_reframe_in_session` 三处文档化原则)
5. race condition 已有 first-decision-wins 守卫 (per abi_compat #4)

**实施细节**:
- comment_poll.py 在 update_human_decision (CAS) 成功后, 直接 import 并调用 extension._handle_s7_human_gate(dispatch_id)
- 等价于 cron 1 次 tick 的 S7 处理逻辑
- 失败兜底: 仍保留 reconciler 30min cron 扫 stuck S7 (避免 comment-poll 进程崩溃后 S7 永远不进 S8)
- AD-M5-1 文档化此 reframe (M4 AD-M4-9 § 决策 #4 → M5 superseded)

---

## Q3-reframe — D Review loop 双模式 hybrid

**锁定**: 双模式 hybrid — owner 自由选 改稿 / 重做 per-rework (~50-55h)

**Comment 协议** (M5 expands M4):
- `/aria approve` → S8_MERGE (M4 行为不变)
- `/aria reject: <reason>` → S_FAIL(human_reject) (M4 行为不变)
- `/aria changes: <feedback>` → 改稿 (B 模式: 同 PR force-push)  **M5 新增**
- `/aria redo: <feedback>` → 重做 (A 模式: 新 PR 从零)              **M5 新增**

**改稿模式 (changes)**:
- 当前 dispatch row 终态写入 human_decision='changes_requested', reject_reason=feedback
- 新建 dispatch row (rework_of=old_id, rework_round+=1, rework_mode='changes')
- Layer 2 重启容器, prompt = 原代码 diff + owner feedback
- AI 在原稿上改, force-push 同 branch, PR diff 累计演进
- 重新进入 S6_REVIEW → S7
- LLM 成本: ~50% (跳过 S0-S3 决策阶段)

**重做模式 (redo)**:
- 当前 dispatch row 终态写入 human_decision='changes_requested', reject_reason=feedback
- 新建 dispatch row (rework_of=old_id, rework_round+=1, rework_mode='redo')
- Layer 2 重启容器, prompt = 原 issue + owner feedback (不含原代码)
- AI 从零重新写, 创建新 PR, 旧 PR 自动 close + comment "Superseded by #<new>"
- LLM 成本: ~100% (全新 cycle)

**理由 (Q3-r 决策依据)**:
1. Owner Q3 答 "Q1=愿付钱 / Q2=要 PR diff 演进 / Q3=高频 rework", 3/3 align with B (改稿)
2. Q3-reframe 后 owner 想 "选择权" → A+B hybrid
3. 业界 Cursor / OpenAI Codex / Devin 都有 redo + tweak 区分

**abi_compat #4 兼容**:
- 每 round 创建 NEW dispatch row, 同 row 的 human_decision 一次性写入 (无 multi-write)
- /aria approve on round-N's row 触发 S8_MERGE on round-N (round-1 已是终态 'changes_requested')
- first-decision-wins 完全保持

---

## Q4 — rework round cap = 3 (合并 cap)

**锁定**: cap = 3, 不区分 changes/redo 模式 (合并 counter)

**实施**:
- schema: `dispatches.rework_round INTEGER DEFAULT 0`
- nomadVar: `ARIA_REWORK_MAX_ROUND=3` (运行时可调, 不需重 deploy)
- 触发: rework_round >= ARIA_REWORK_MAX_ROUND → fail_reason='rework_exceeded'
- Feishu 卡片当前 round 显示: "rework round 2/3 (changes mode)" 或 "rework round 2/3 (redo mode)"

**理由**:
1. 业界 norm: GitHub Copilot Chat 默认 3 轮反馈, Cursor 也类似
2. AI 改稿规律: 第 1 轮捕捉大方向, 第 2 轮微调, 第 3 轮还不行通常是需求模糊不是实施问题
3. 成本上限可预测: 单 issue 上限 ≤ ¥4-22 (M4 实测单 dispatch ¥3-15, 后续 0.5x cost)
4. 可演进: M5 ship 后 owner 实测调整 (config 化即可)

---

## Q5 — E 审计日志 SQLite immutable 新表

**锁定**: SQLite 新表 dispatch_audit_log + INSERT-only CHECK + DB triggers (~15h)

**Schema**:
```sql
CREATE TABLE dispatch_audit_log (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  dispatch_id TEXT    NOT NULL,
  ts          TEXT    NOT NULL,
  event_type  TEXT    NOT NULL,
  payload_json TEXT   NOT NULL,
  CHECK (json_valid(payload_json))
);
CREATE INDEX idx_audit_dispatch_ts ON dispatch_audit_log(dispatch_id, ts);

-- Immutable triggers
CREATE TRIGGER audit_no_update BEFORE UPDATE ON dispatch_audit_log
  BEGIN SELECT RAISE(ABORT, 'audit log immutable'); END;
CREATE TRIGGER audit_no_delete BEFORE DELETE ON dispatch_audit_log
  BEGIN SELECT RAISE(ABORT, 'audit log immutable'); END;
```

**Event types** (M5 写入点):
- `state_transition` (state from → to + reason)
- `llm_call` (model + tokens_in + tokens_out + cost + duration_ms)
- `human_decision` (approve/reject/changes/redo + comment_id + decision_at)
- `rework_cycle` (rework_round + rework_mode + parent_dispatch_id)
- `failure_analysis` (LLM 输出: action + reason + confidence)  **B 项 写入**
- `risk_tier_classified` (tier + algorithm_used)  **F schema 占位用 'always' tier_only_stub_value**
- `spec_drift_detected` (compliance_score + deviations)  **C 项 写入**
- `commit_lint_result` (passed/failed + violations)  **C 项 写入**

**db.py helpers**:
```python
def append_audit_event(dispatch_id: str, event_type: str, payload: dict) -> None:
    """immutable INSERT, raises on UPDATE/DELETE attempt"""

def query_audit_log(dispatch_id: str = None, event_type: str = None,
                    since: datetime = None, until: datetime = None) -> list[dict]:
    """time-ordered audit events for replay (A 项)"""
```

**理由**: DB-native immutable + Replay (A 项) 直接 SQL query + 与 M4 schema 风格一致 + DB 膨胀可推 M6

---

## Q6 — A Replay framework Deterministic state replay only

**锁定**: Deterministic state replay, 不重跑 LLM (~10h)

**功能**:
- 输入: dispatch_id (单个) 或 dispatch_ids 列表
- 输出: 时间序状态变化的 markdown / JSON report
  - 每个状态 entry/exit timestamp
  - 关键 metadata (LLM model + tokens + cost + fallback)
  - human decisions 时间线
  - rework chain (parent → children)
  - failure analysis 结果 (B 项 输出)
  - drift detection 结果 (C 项 输出)

**实施**:
- 新模块 aria_layer1/replay.py
- query audit log (Q5 表) + dispatches 主表 join
- 输出 format: stdout markdown / `.aria/replay-reports/{dispatch_id}.md` 文件

**M6 升级路径** (本 M5 不做):
- LLM stub replay (用录制 response 重放, 用于 unit test): +20h
- Differential testing (改 prompt 后跑老 dispatch 比较输出): +25h

**理由**:
1. Solo lab 实际频率: 每周看几次 "AI 当时怎么决策"
2. Audit log 已锁 E (Q5), replay 主要是 query + format
3. Budget 友好: 留 ~34h 给 B+C
4. 可演进: M6 加 method 不破坏方向 1 API

---

## Q7 — F Risk-tier schema dual-write only

**锁定**: 仅做 schema dual-write 满足 abi_compat #1, **算法推 M6** (~5h)

**M5 实际做**:
1. Schema migration v3 → v4: ALTER TABLE dispatches ADD COLUMN risk_tier TEXT
2. db.py 加 helper: `get_risk_tier(dispatch_id)` (prefer risk_tier WHERE NOT NULL else fallback risk_tier_stub)
3. 写入路径: M5 dispatcher 写 risk_tier=NULL, risk_tier_stub='always' (M4 行为不变)
4. validate-m5-handoff.py 验证 schema 满足 abi_compat #1

**M5 不做**:
- 任何 risk classification 算法 (rule-based / LLM-based)
- B Reconciler / Feishu 卡片 / replay 用 risk_tier 做差异化
- Owner 反问 "我没看到分级价值" 已在 brainstorm 解释清楚 — Q-c 路径 W

**M6 升级路径**:
- 真有清晰 use case 时再决定算法 (rule / LLM / hybrid)
- 接口 (db.py::get_risk_tier) 不变, 只动写入路径 + 应用层 routing

**理由**:
1. Owner question 了分级价值 (3 个 use case 选项 X/Y/Z 都未确定哪个最有价值)
2. M5 budget 紧 (~91h locked + B/C 仍开放), 砍 5-15h 给其他更明确的功能
3. abi_compat schema 已替 M6 打地基 (装接口不接路由器, 类比说明)
4. PRD §M5 没强制要求算法, 只 m4-handoff 说 routes_to:M5

---

## Q8 — B Reconciler Failure analysis + smart retry

**锁定**: Failure analysis + smart retry (~15h)

**功能**:
- 当 dispatch 进入 S_FAIL 时, reconciler 加一步 LLM 分析:
  - 输入: fail_reason + fail_detail + last 5 audit log events
  - 输出: `{action: 'retry'|'abort'|'notify_owner', confidence: 0-1, reason: string, suggested_owner_action: string}`
- **retry**: 自动 re-dispatch (仅当 fail_reason in {'infrastructure', 'timeout'} 等可恢复类 + retry_count < 1 + LLM confidence > 0.7)
- **abort**: 写明确 final reason, 不再 retry
- **notify_owner**: Feishu reject 卡片含 LLM 诊断 + 建议 (e.g. "建议: 此 issue 可能描述模糊, 建议 owner 重写后重启")

**LLM 调用**:
- model: glm-4.5-air (便宜稳定), fallback glm-5-turbo
- 频率: per-failure (~10-20 次/月)
- 成本: ~¥1-3/月

**M5 写入 audit log**:
- event_type='failure_analysis', payload=LLM 完整输出 + 是否触发 retry

**理由 (Q8 决策)**:
1. 匹配 owner 真实痛点 (M4 historical 13 条 S_FAIL 都没后续)
2. LLM 用得在刀刃上 (per-failure 不是 per-dispatch)
3. 复用 audit log E (Q5 已锁)
4. 给 C 留 14h 做 commit lint + spec diff
5. M6 升级路径: 加 risk_tier 调整 retry threshold

---

## Q9 — C Drift defense Commit lint + Spec diff

**锁定**: Commit lint + Spec diff (~12h)

**Commit lint** (~5h):
- AI 写 commit 后, 用 regex/parser 验证 Conventional Commits + Aria 规范:
  - type prefix (feat/fix/docs/chore/refactor/style/test)
  - scope 含 milestone (e.g. "feat(M5): ...")
  - title ≤ 70 字
  - body 含 issue 引用 (Closes #N)
- 不通过 → Layer 2 dispatcher 拒绝该 commit, force AI 重写
- 实施位置: aria-orchestrator/aria-layer1/commit_validator.py + Layer 2 hook

**Spec diff** (~7h):
- Dispatch 完成 (PR merged 或 closed) 后, 用 LLM 比较:
  - 输入: openspec/changes/<id>/proposal.md + PR diff
  - 输出: `{compliance_score: 0-100, deviations: [...], extra_changes: [...]}`
- score < 70 → Feishu 警告卡片 "Spec drift detected, owner 检视"
- 写入 audit log event_type='spec_drift_detected' (Q5 表)
- LLM model: glm-4.5-air, ~¥1-3/月

**M5 不做** (M6/M7 升级):
- Daily LLM 自审 (检测 prompt drift / behavior drift)
- 量化趋势分析 (token usage / commit length 时间序列)

**与 D Review loop 的协同**:
- 改稿/重做 cycle 完成后, spec diff 也跑 (不只是 final approve)
- audit log 含每个 rework cycle 的 spec drift score, replay 时一目了然

**理由 (Q9 决策)**:
1. 覆盖最重要的 2 类 drift (code + commit)
2. prompt/behavior drift 是长期累积, M5 ship 后才有数据 → M6/M7 再加有的放矢
3. Budget 健康: 113-118h locked, 留 2-7h headroom
4. PRD §M5 中等达标 (2/4 主要 drift 类型)

---

## M5 全 Scope Sequencing (建议, Phase A.1 spec-drafter 详细排序)

**Phase 1 — Schema + Foundation (week 20, ~30h)**:
1. Schema migration v3 → v4: 加 risk_tier (F) + dispatch_audit_log (E)
2. db.py helpers: append_audit_event / query_audit_log / get_risk_tier
3. Audit log 写入点 instrumentation (state_transition + llm_call + human_decision)

**Phase 2 — G + B (week 21, ~21h)**:
4. G cron cadence: comment-poll direct transition (~6h)
5. B Failure analysis + smart retry (~15h)

**Phase 3 — D Review loop (week 22-23, ~50-55h)**:
6. Schema 加 rework_round / rework_of / rework_mode columns
7. Comment-poll 协议扩展 (4 commands)
8. /aria changes (改稿模式) Layer 2 二次进入
9. /aria redo (重做模式) 新 dispatch + 旧 PR close
10. rework_round cap=3 enforcement
11. Feishu 卡片 round 显示

**Phase 4 — A Replay (week 24, ~10h)**:
12. aria_layer1/replay.py
13. query audit log + dispatches 主表 join
14. markdown report 生成

**Phase 5 — C Drift defense (week 24-25, ~12h)**:
15. Commit lint validator + Layer 2 hook
16. Spec diff LLM call + Feishu drift 卡片

**Phase 6 — T-deploy + acceptance (week 25, owner-runnable)**:
- Production deploy (含 schema migration v3→v4 with 3-safeguard pattern per `feedback_schema_migration_3_safeguard_pattern`)
- Tier-2 N≥3 real owner workload accumulate (含 ≥1 changes + ≥1 redo + ≥1 reject)

---

## Open items for spec-drafter (Phase A.1)

以下 detail 由 Phase A.1 spec-drafter 在 proposal.md / tasks.md 展开 (本 brainstorm 不再 deep dive):

- [ ] 改稿模式具体: Layer 2 git rebase + force-push 还是 append-commit?
- [ ] rework chain UI: Forgejo PR description 自动维护 rework 历史链
- [ ] failure_analysis LLM prompt template 版本管理
- [ ] spec_drift LLM prompt template 设计
- [ ] commit_validator 接入 hermes 还是 standalone?
- [ ] 11 个 AD-M5 slot 预留 (per AD-M0-9 brainstorm-to-spec 标准)
- [ ] T-deploy 检查清单 (含 schema v3→v4 migration 3-safeguard)

---

## Cross-references

**Predecessor decisions**:
- [.aria/decisions/2026-05-07-us024-m4-brainstorm.md](2026-05-07-us024-m4-brainstorm.md) (US-024 M4 brainstorm Q1-Q14)
- [.aria/decisions/2026-05-09-od-m4-2-underbaseline-retrospective.md](2026-05-09-od-m4-2-underbaseline-retrospective.md) (M4 effort ratio 0.47 retrospective)
- [openspec/archive/2026-05-09-aria-2.0-m4-human-gate-feishu-approval/](../../openspec/archive/2026-05-09-aria-2.0-m4-human-gate-feishu-approval/) (M4 archived Spec)
- [aria-orchestrator/docs/m4-handoff.yaml](../../aria-orchestrator/docs/m4-handoff.yaml) (含 abi_compat_promises 4 forward-binding)
- [docs/handoff/2026-05-09-track-a-deploy-done.md](../../docs/handoff/2026-05-09-track-a-deploy-done.md) (Track A T-deploy + 3 production fixes)

**Memory entries (M5 design relevant)**:
- `feedback_phase_a_depth_drives_b_velocity` (深度 brainstorm → mechanical translation)
- `feedback_owner_invoked_convergence_loop` (audit 收敛模式参考)
- `feedback_paper_fix_antipattern` (test + code + doc 三位一体)
- `feedback_spec_reframe_in_session` (M5 reframe AD-M4-9 § 决策 #4)
- `feedback_feishu_hmac_key_msg_swap` (M5 LLM call 测试 oracle 设计)
- `feedback_handoff_doc_assumes_venv_ready_smell` (T-deploy 必显式列 venv refresh)
- `feedback_schema_migration_3_safeguard_pattern` (schema v3→v4 migration 模板)

---

## Sign-off

- [x] Owner ACK Q0 abi_compat 4 promises (Q0 reply: A)
- [x] Owner lock Q1 scope = 5 PRD + F + G, H 推 M6 (Q1 reply: 同意推荐)
- [x] Owner lock Q2 G = comment-poll direct transition (Q2 reply: 2)
- [x] Owner lock Q3-reframe D = hybrid (Q3-r reply: 同意推荐)
- [x] Owner lock Q4 rework cap = 3 (Q4 reply: 2 cap=3)
- [x] Owner lock Q5 E = SQLite immutable 新表 (Q5 reply: 2)
- [x] Owner lock Q6 A = state replay only (Q6 reply: 1)
- [x] Owner lock Q7 F = schema only (Q7 reply: A)
- [x] Owner lock Q8 B = failure analysis (Q8 reply: 2)
- [x] Owner lock Q9 C = commit lint + spec diff (Q9 reply: 2)
- [x] Owner approve 进 Phase A.1 spec-drafter (final reply: 1)

**Status**: Locked — Ready for Phase A.1 spec-drafter
**Next**: `/aria:spec-drafter` 起草 openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/
