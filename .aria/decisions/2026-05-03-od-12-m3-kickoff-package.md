---
id: OD-12
title: M3 (US-023) brainstorm R1 owner decision package — Anthropic 路径 + scope 边界 + baseline
date: 2026-05-03
status: awaiting_owner_decision
relates_to: US-023, AD-M1-12 (Luxeno-only), OD-9, OD-11, AD-M2-9
---

# OD-12 — M3 Kickoff Decision Package

## 触发

US-023 R1 brainstorm 4-agent parallel (backend-architect / qa-engineer / tech-lead / ai-engineer) 完成。**4/4 NEEDS_OWNER_INPUT** 共识 — 在 owner 答以下 critical decisions 前 brainstorm 不能 R2 收敛 (任何 R2 都基于幽灵 dual-provider 设计是无效工作)。

R1 输出聚合: 38 objections (4 critical / 16 important / 18 minor) + 22 open questions (12 owner-blocking).

## 关键决策点 (owner 一次性回答即可)

### Q1: Anthropic 账号 + 预算 (BA-Q2 / R1-TL-3 / OBJ-R1-AI-1 / OBJ-R1-AI-6)

**问题**: 你现在有 active Anthropic Commercial 账号 + 为 M3 分配预算吗?

**预算估算 (per ai-engineer)**:
- M3 验收 demo (10 cycles): ~$2-4
- M3 development churn (100-300 calls): ~$30-90
- 双 provider benchmark: ~$7
- **Total M3 Anthropic budget: ~$50-200**

**选项**:
- **A. YES (有账号 + 预算)**: 验收 D 双 provider routing 全实施; 14 day legal IS-4 reverify (Phase A.0a); 预期 baseline +15-25h legal/integration overhead
- **B. NO (无账号或预算)**: 验收 D 重定义为 "single-provider Luxeno + reconciler + Layer 2 wire-up"; baseline 减 ~30-40h; 双 provider routing 推 M4+
- **C. DEFER**: 答 "M3 先单 provider, M4 评估"; 与 B 等价但留 review 选项

**推荐**: 取决于实际预算状态. 若 owner 有 GLM 订阅但无 Anthropic 预算 → 选 B 简化 scope (与 M2 路径一致, OD-9 reframe 延续)。

---

### Q2: M3 baseline 工时 (R1-TL-1)

**问题**: OD-12 baseline 锁多少?

**R1 共识估算**:
- backend-architect: 90h M3 baseline 偏低估, 实际 ~110-130h
- ai-engineer: +18h prompt scaffolding (S2/S3/reconcile 3 templates × 6h) NOT in 90h baseline
- tech-lead: 推荐 122h with 10% buffer
- 综合: 21h carryover + 90h M3 + 18h prompts + audit overhead 25h = **~154h actual**

**选项**:
- **A. 111h hard** (US-023 draft 字面): risk 实际超 30%
- **B. 122h with 10% buffer** (tech-lead 推荐): plausible, 留 sleep margin
- **C. 154h aggressive realistic** (4 agent 综合估): 严格符合 backend + ai + qa 估算
- **D. 选 Q1=B/C 后简化 scope** → ~90h: 取消双 provider 后碳 baseline 大降

**推荐**: 若 Q1=A → 选 154h (be honest); 若 Q1=B → 选 90h (无 dual provider) 或 105h (含 reconciler + carryover)

---

### Q3: Reconciler 决策方式 (OBJ-R1-AI-3)

**问题**: 检测到 stuck dispatch (S5_AWAIT 跨 N tick 无进展) 后如何路由?

**选项**:
- **A. 机械 (rule-based)**: ~6h. 三阈值 (max_age_at_S5 / max_total_attempts / stuck_alloc_states) 触发 S_FAIL(stuck) 或 attempt_count++ 重 enqueue
- **B. LLM-decided**: ~25h. 新 S_RECONCILE 状态 + prompt template + parse 函数 + accuracy benchmark ≥80% target

**推荐**: A (机械). LLM-decided reconciler 留 US-025 M5 (defense-in-depth + audit loop)。

---

### Q4: Reconciler 部署位置 (R1-TL-Q4 / BA-Q1 / OBJ-QA-7)

**问题**: 独立 Nomad periodic job vs in-cron-tick 子阶段?

**选项**:
- **A. 独立 Nomad periodic** (per AD-M2-8 cron pivot 一致, 隔离崩溃): +2h Nomad HCL + 锁协议扩展
- **B. In-cron-tick sub-phase** (零新锁, 简单): +0h infra, 紧耦合主 cron

**推荐**: A (独立). 与 AD-M2-8 lifecycle/locks 一致, 单 cron 失败不影响 reconciler。CAS (compare-and-swap) SQL 模式取代锁 (`UPDATE ... WHERE rowid=X AND state='S5_AWAIT'`).

---

### Q5: Schema migration v2 策略 (R1-TL-Q5 / BA-2 / OBJ-QA-5)

**问题**: 加性 (additive-first) vs 一次性 drop UNIQUE?

**选项**:
- **A. Additive-first**: v2 加 schema_version + 新 column (cycle_start_ts/cycle_end_ts/dispatched_job_id/eval_id), UNIQUE drop 留 v3 (M3 后)
- **B. 一次性 drop UNIQUE**: SQLite CREATE TABLE new + INSERT SELECT + DROP old + RENAME, atomic but recovery-risky

**推荐**: A (additive-first). 风险窗口最小; UNIQUE drop 在 M3 完成 E2E perf 后 v3 单独 migration; 符合 AD-M1-7 governance。

---

### Q6: 验收 A 测试基础设施 (OQ-QA-1)

**问题**: ≥10 issue 完整 cycle 测试方式?

**选项**:
- **A. Tier-1 集成 (FakeAllocStatusProvider 自动推进 + MockClock fast-forward)**: CI-runnable, 无 cluster 依赖, 验证状态机闭合
- **B. Tier-2 cluster smoke (≥1 真实 issue + 真实 Nomad alloc)**: owner 部署 + 验证, 实际 PRD 验收 A intent
- **C. 两层 gate (推荐)**: A=自动 sign-off, B=Go-with-revision 必需; 仿 M2 T7.6 模式

**推荐**: C. M2 已实证 cluster smoke gate 价值 (T7.6 catch latent UNIQUE constraint bug)。

---

### Q7: Acceptance B p50 测量方法 (OQ-QA-2 / OBJ-QA-2)

**问题**: M3 cycle p50 测量起点?

**选项**:
- **A. S0_IDLE → S9_CLOSE wall** (full cycle 含 cron 等待 + LLM + Nomad alloc + Layer 2 exec)
- **B. S4_LAUNCH → S9_CLOSE wall** (仅 dispatch 后, 无 cron 等待)
- **C. S1_SCAN → S9_CLOSE wall** (不含 Phase 1 seed wait, 含 LLM 状态)

**推荐**: C. 与 M1 DEMO_002 应该一致 (m1_demo_002_p50_s = 31.5s 大概是这范围). m3-handoff.yaml 加 `cycle_start_ts` (S1_SCAN entry) + `cycle_end_ts` (S9_CLOSE/S_FAIL entry) 持久化字段, 后续可机械计算。

---

### Q8: 4 个轻量决策

| ID | 问题 | 推荐 |
|---|---|---|
| Q8a | Spec 命名 | `aria-2.0-m3-double-provider-crash-recovery` (Q1=A) 或 `aria-2.0-m3-layer2-cycle-close-recovery` (Q1=B) |
| Q8b | AD-M3-* 占位 | AD-M3-1..7 (per tech-lead R1-TL-6) |
| Q8c | 二段 audit pattern | scope-bounded 1-round per task group + Phase D 4-round |
| Q8d | Secret rotation 时机 | T13 mid-sprint (NOT T16), 给 perf benchmark 用 post-rotation keys |

---

## R1 完整 findings 索引

**Critical (4)**:
- BA-3: HCL meta key inventory + IMAGE_SHA pin 契约未定义
- BA-5: Reconciler 锁竞争 (Option A in-process 推荐)
- R1-TL-2: 单一 Spec + Phase B.2.0 强排序 carryover 优先
- R1-TL-3: Anthropic legal IS-4 reverify 必 Phase A.0 gate
- OBJ-QA-1: 验收 A 真实 cluster 还是 fake alloc 自动推进
- OBJ-QA-2: 验收 B p50 测量方法 + cold-start
- OBJ-R1-AI-1: AD-M1-12 supersession 状态 + Anthropic 预算
- OBJ-R1-AI-2: S2/S3 stub prompt 不能直接接真 LLM (18h 缺工)

**Important (16)**:
- BA-2/4/6/7/8 (schema / router / 恢复 / additive / token wiring)
- R1-TL-1/4/5/6/8 (估算 / rotation / audit / AD slots / owner actions)
- OBJ-QA-3/4/5/6/7 (crash / fallback / migration / rotation / lock)
- OBJ-R1-AI-3/4/5/6 (reconciler 决策 / pricing / 单 prompt 跨 provider 风险 / legal)

**Minor (18)**: 详 R1 4 agent 输出 (略, 不阻塞决策)

## Owner Action

请回答 Q1-Q7 (Q8 可全选推荐). 单字符回答即可:

**示例 1 (单 provider 简化)**: Q1=B, Q2=D-90h, Q3=A, Q4=A, Q5=A, Q6=C, Q7=C, Q8=defaults
**示例 2 (双 provider 完整)**: Q1=A, Q2=C-154h, Q3=A, Q4=A, Q5=A, Q6=C, Q7=C, Q8=defaults

回答后, AI 自动:
1. 把 OD-12 status: awaiting_owner_decision → resolved
2. 启动 R2 (基于 owner 输入收敛 scope)
3. R2 → R3 → R4 收敛后起 Spec proposal.md + tasks.md
4. Phase A.2 audit 4-round 收敛
5. Phase A.3 OD-12 baseline 锁 + Spec Status: Draft → Approved → 启动 Phase B.1+B.2

## 不影响

- M2 closeout 已完成 (Spec archived, m2-handoff signoffs filled)
- T7.5/T7.6 cluster smoke 已 PASS
- US-023 Draft 文件已存在 (待 OD-12 后 Phase A.1 改写)

## 引用

- US-023.md 草稿: `docs/requirements/user-stories/US-023.md`
- m2-handoff.yaml `open_issues_for_m3` 列表
- AD-M1-12 (Luxeno-only): `aria-orchestrator/docs/architecture-decisions.md#ad-m1-12`
- m1-legal-carryover.md §9 (4 deferred items)
- secret-rotation-deferred 90-day cap 2026-08-02
- M2 closeout memory: `project_aria_m2_closeout_2026-05-03.md`
- R1 4-agent transcripts: 本 session (backend-architect / qa-engineer / tech-lead / ai-engineer)
