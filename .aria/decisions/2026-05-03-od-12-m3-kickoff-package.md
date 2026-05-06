---
id: OD-12
title: M3 (US-023) brainstorm R1 owner decision package — RESOLVED 2026-05-03
date: 2026-05-03
status: resolved
resolved_at: 2026-05-03
relates_to: US-023, AD-M1-12 (Luxeno-only), OD-9, OD-11, AD-M2-9
---

# OD-12 — M3 Kickoff Decision Package (RESOLVED)

## 触发

US-023 R1 brainstorm 4-agent parallel (backend-architect / qa-engineer / tech-lead / ai-engineer) 完成。**4/4 NEEDS_OWNER_INPUT** 共识. R1 输出: 38 objections (4 critical / 16 important / 18 minor) + 22 open questions.

Owner one-by-one 互动展开 (2026-05-03 evening session): Q1→Q7 + Q8 全部回答, 7 主决策 + 25 细节确认。

## Owner 决策汇总 (resolved)

### Q1: Anthropic 账号 + 预算 → **D'** (Luxeno primary + Zhipu 官方 fallback + GLM 多模型 routing)

- Owner 状态: 只有 Anthropic 订阅账号 (claude.ai), 没 API key 账号; "后面需要时再加"
- 替代方案: 用 GLM 全家桶代替 Anthropic, 同 provider 内 quality routing + 跨 provider HA fallback
- **Provider chain**: Luxeno (api.luxeno.ai/v1, flat sub) primary, Zhipu 官方 (open.bigmodel.cn/api/paas/v4, per-token billing, 已充值) HA fallback
- **Model chain**:
  - S2_DECIDE → `glm-4.5-air` (cheap)
  - S3_BUILD_CMD → `glm-5-turbo` (mid-tier, 对标 Sonnet)
  - S6_REVIEW → `glm-5.1` (top-tier, 对标 Opus)
  - Fallback ladder per state: 5.1 → 5-turbo → 4.5-air
- **Fallback 触发**: 3 次 expo backoff (1s/2s/4s) 后 fallback Zhipu, 被动 fallback (非主动 race)
- **fallback_chain_json 格式**: dict-based `[{provider, model, outcome, reason, latency_ms, ts}]` (M2 字符串数组升级, schema migration v2 内 transform 旧数据)
- Secret keys: 4 → 5 (+ZHIPU_API_KEY)
- Legal: OD-9 续延, m1-legal-carryover §9 不重审 (Zhipu 也境内 vendor)
- 验收 B 测量过滤 `fallback_triggered=false` (healthy path), fallback 路径单独 metric uptime%

### Q2: M3 baseline 工时 → **E** (185h hard baseline)

实际 scope (Q1=D' 后) 推算:
```
M2 OD-11 carryover (Layer 2 HCL/alloc_provider/migration v2/cycle E2E):  21h
PRD §M3 base scope (reconciler/crash recovery/Nomad hardening):          70h
S2/S3 prompt scaffolding (ai R1 OBJ-2):                                  18h
Q1=D' multi-model routing + benchmark:                                    8h
Q1=D' ProviderRouter abstraction + ZhipuClient:                          10h
Audit overhead (混合: Phase A.2 4-round + B.2 scope-bounded + D 4-round): 25h
Owner action items × 4 (rotation/legal/T1.6 image/sign-off):              4h
Spec drafting (Phase A.1.1+A.1.2+A.1.3):                                  8h
Phase A.2 audit (R1-R4 4-round):                                          4h
Subtotal:                                                               168h
+ 10% buffer (R1-TL-1 推荐):                                            +17h
─────────────────────────────────────────────────
OD-12 baseline:                                                         ~185h
```

历史校准: M2 PRD 100h → OD-7=b 146h → OD-8 156h → 实测 148h (5% within). M3 PRD 90h → 锁 185h (×2.06) 是 *scope discovery 后真实 inflation*, 与 M2 模式同。

时间预期: 4 周 (PRD §M3 Week 13-16) 50% 投入 = ~120h 容量, 不够 → 实际 5-6 周; 起 OD-13 if 超 6 周; secret rotation hard cap 2026-08-02 (~13 周后) 仍安全。

### Q3: Reconciler 决策方式 → **A** (机械 ~6h)

- 三阈值 default: `max_age_at_S5_AWAIT_minutes=60`, `max_total_attempts=3`, `stuck_alloc_states=('pending','queued')`
- 路由策略: 混合 — 第 1-2 次重试 (attempt_count++), 第 3 次 S_FAIL(stuck)
- 告警: stuck 检测到时 Feishu webhook 通知 owner (复用 S7 webhook)
- M5 LLM 升级预留: Strategy interface (mechanical vs LLM 切换 1 行 env var)
- LLM-decided reconciler 推 US-025 M5

### Q4: Reconciler 部署位置 → **A** (独立 Nomad periodic)

- 文件: `aria-layer1-reconcile.nomad.hcl` (与 cron 命名一致)
- Cadence: 30min (在 cron 60min 中点跑, 减撞概率)
- 锁协议: **CAS (compare-and-swap)** 模式 — `UPDATE ... WHERE rowid=X AND state='S5_AWAIT' AND last_heartbeat_at=?` 双重 check, SQLite WAL 天然支持; 不依赖文件锁
- 与 AD-M2-8 (Nomad owns scheduling) 一致
- 故障隔离: cron 挂 reconciler 仍工作, 反之亦然

### Q5: Schema migration v2 → **A** (Additive-first, schema 1.0→2.0)

- ALTER TABLE ADD COLUMN 加 5 个新 column:
  - `cycle_start_ts TEXT` (S1_SCAN entry 时设, Q7 验收 B p50 起点)
  - `cycle_end_ts TEXT` (S9_CLOSE / S_FAIL entry 时设, 终点)
  - `dispatched_job_id TEXT` (Nomad parameterized dispatch ID, forensic per AD-M2-9 §风险 #5)
  - `eval_id TEXT` (Nomad evaluation ID)
  - `provider_cost_model TEXT` (`metered` Zhipu / `subscription_flat` Luxeno)
- inline UNIQUE constraint (schema.sql:98) **保留** — 应用层 dedupe (e36beb2 commit) 续用
- schema_meta 表加 row `('schema_version', '2.0')`
- Migration runner 时机: 启动时自动检查 schema_version 升级 (简单, ALTER 失败 SQLite 自动回滚, 不需手动 rollback 脚本)
- Test fixture: T15.3 真实 11-row dispatches.db 快照 (per qa R1 OBJ-5 CanonicalDispatchesDB pattern)
- inline UNIQUE drop 推 schema v3 (M4 / US-024 自然落)

### Q6: 验收 A 测试基础设施 → **A** (Tier-1 自动化集成 only, ~6h)

- 不强制单独 Tier-2 cluster smoke gate
- cluster verification 嵌入 carryover #1 (aria-layer2-runner HCL 部署) 的 implementation 验证
- m3-handoff.yaml `acceptance_a_actual_dispatches=10` 字段填 Tier-1 fake-cycle 实测值
- Fixture 复用 M2: FakeAllocStatusProvider + FakeNomadClient + FakeSilknodeClient + 新增 FakeZhipuClient (per Q1=D')
- 隐含 risk: 不如 Q6=C 严格, 但 owner explicit 接受, 后续可升级 if needed

### Q7: 验收 B p50 测量 → **C** (S1_SCAN → S9_CLOSE wall + filter)

- p50 计算: `median(cycle_end_ts - cycle_start_ts) WHERE state='S9_CLOSE' AND fallback_triggered=false`
- 阈值: `m1_demo_002_p50_s × 1.5 = 31.5 × 1.5 = 47.25s`
- 样本 size: ≥10 cycles (与验收 A 一致)
- Schema 字段已含在 Q5 (cycle_start_ts + cycle_end_ts)
- Methodology 写入 m3-handoff.yaml `performance_vs_m1.m3_p50_methodology` 字段

### Q8: 4 个轻量决策

- **Q8a Spec 命名**: `aria-2.0-m3-cycle-close-glm-routing-recovery` (3 主题串联: cycle close + GLM routing + recovery)
- **Q8b AD-M3-* 占位**: AD-M3-1..7 (7 slot) + 留 AD-M3-8/9/10 spillover
- **Q8c Audit pattern**: 混合 (Phase A.2 4-round + Phase B.2 scope-bounded 1-round per task group + Phase D 4-round); ~25h overhead
- **Q8d Secret rotation 时机**: T13 mid Phase B.2 (一次性 rotate 全 5 keys, post-rotation 用 Q7 验收 B benchmark 顺便验证新 keys)

## 影响汇总

### Spec 命名 + scope
- Spec 目录: `openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/`
- US-023.md 改 scope (Q1=D' 不是双 Anthropic), Status: Draft → Approved Pending baseline 锁
- 验收 D 复活 (per Q7), 验收 E (schema migration zero loss) 锁定, 验收 F (secret rotation) 时机 mid-sprint

### Spec 内 phase 排序 (per tech-lead R1-TL-2 强制 carryover 优先)
```
Phase B.2.0  M2 carryover (T1-T4, ~21h):
  T1: aria-layer2-runner HCL fork from US-021 M1 (~6h)
  T2: alloc_provider production HTTP class (~4h)
  T3: schema migration v2 additive (~3h)
  T4: single-issue Layer 2 cycle smoke (~3h)
  
Phase B.2.1  M3 new scope (T5-T11, ~90h):
  T5: reconciler design + aria-layer1-reconcile.nomad.hcl (~6h)
  T6: reconciler stuck-detection + S_FAIL routing + Feishu (~8h)
  T7: crash recovery: hermes 重启 → S5_AWAIT auto-resume (~10h)
  T8: ZhipuClient (stdlib urllib mirror SilknodeClient) (~4h)
  T9: ProviderRouter abstraction + multi-model + dict fallback_chain_json (~14h)
  T10: per-provider token breakdown (US-027 prep) (~4h)
  T11: Nomad integration hardening (~8h)
  T12: reconciler integration tests + crash recovery E2E (~8h)
  
Phase B.2.Z  E2E + handoff (T13-T16, ~30h):
  T13: secret rotation execution (5 keys) (~3h)
  T14: perf benchmark vs M1 baseline (验收 B post-rotation) (~6h)
  T15: ≥10 issue full cycle Tier-1 自动化集成 (验收 A + B + D + E) (~10h)
  T16: m3-handoff.yaml v1.0 + AD-M3-1..7 backfill + Report + Spec archive (~6h)
```

### Owner action items (4 个, 预计)
1. Phase A.0a Anthropic legal reverify — *Q1=D' 后跳过* (provider 不变 OD-9 续)
2. Phase B.2.0 T1: 部署 aria-layer2-runner HCL on Aether (~30min)
3. Phase B.2.Z T13: 执行 secret rotation (5 keys, ~45min per SOP)
4. Phase D T16: M3 sign-off (~5min)

### 不影响
- M2 closeout (已 archived `openspec/archive/2026-05-03-aria-2.0-m2-layer1-state-machine/`)
- T7.5/T7.6 cluster smoke 已 PASS
- m2-handoff.yaml signoffs all populated
- 268 unit tests baseline

## 引用

- US-023.md: `docs/requirements/user-stories/US-023.md`
- m2-handoff.yaml `open_issues_for_m3`
- AD-M1-12 (Luxeno-only): supersedes AD-M1-6
- m1-legal-carryover.md §9 (4 deferred items, OD-9 续延)
- secret-rotation-deferred 90-day cap 2026-08-02 (per OD-9 + OD-11)
- M2 closeout memory: `project_aria_m2_closeout_2026-05-03.md`
- R1 4-agent transcripts (本 session): backend-architect / qa-engineer / tech-lead / ai-engineer
- R1 verdict 4/4 NEEDS_OWNER_INPUT → owner one-by-one Q1-Q8 收敛 → resolved 2026-05-03

## Next Steps

1. update US-023.md scope (Q1=D' 反映 + Status Draft → Approved Pending OD-12 lock)
2. R2 brainstorm round (基于 OD-12 输入, ~30-45min wall, 4-agent parallel verify)
3. R3-R4 收敛 (per `feedback_pre_merge_4round_convergence_template`)
4. Phase A.1 Spec proposal.md + tasks.md drafting (in `openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/`)
5. Phase A.2 post_spec audit 4-round
6. Phase A.3 OD-12 baseline final lock + Spec Status: Draft → Approved
7. Phase B.1 feature branch (`feature/aria-2.0-m3-cycle-close-glm-routing-recovery`)
8. Phase B.2 implement (~6 weeks at 50% allocation)
