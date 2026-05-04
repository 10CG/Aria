---
id: US-023-PHASE-A2-R1-OWNER-ADVISORY
title: US-023 / aria-2.0-m3 Phase A.2 R1 — owner advisory 7 问
date: 2026-05-04
status: pending_owner_input
relates_to: US-023, OD-12 RESOLVED, R1 audit (.aria/audit-reports/post_spec-2026-05-04T103702Z-us023-m3.md), Phase A.2 R2 next
---

# US-023 / M3 Phase A.2 R1 — Owner Advisory (7 问)

## 触发

Phase A.2 R1 4-agent post_spec audit (2026-05-04T103702Z) 完成。verdict aggregate = **BLOCK_NEED_OWNER** (qa + ai 各 1 NEEDS_OWNER_INPUT, backend + tech-lead READY_FOR_R2)。

7 个 owner-decide questions 必须答完才能进 Phase A.2 R2 fix-verify, 然后 Phase A.3 OD-12 baseline final lock + Status: Draft → Approved。

AI 已对**所有不依赖 owner 判断的 Spec 文本 fix** auto-resolve (per `feedback_ai_代填_sign_off_pattern` AD-M0-9 solo lab pattern), Spec 当前已含 default 描述 + "等 owner 确认" provenance 注。owner 答完后 R2 verify default 是否 sustain 即可。

---

## 决策清单 (7 问)

### Q1: OD-14 — Secret rotation 时机

**问**: T13 (5 keys rotation: LUXENO + 3 FEISHU + ZHIPU) 拉到 **Phase B.2.0 startup (week 1)** vs 原 OD-12 §Q8d **mid-B.2 (week 14-15)**?

**Context**:
- 90-day cap 2026-08-02 (per `secret_rotation_deferred` SOP)
- 今日 2026-05-04 → cap 距 13 周
- M3 baseline 5-6 周 50% capacity ≈ 10-12 calendar 周
- 原 mid-B.2 估 = 2026-08-12, **晚 cap 10 天**
- pull forward to startup = ~2026-05-11, 早 cap 12 周, 安全

**AI 推荐**: **YES, pull forward to B.2.0 week 1**
**Rationale**: 安全余量足, post-rotation 的 T14 perf benchmark 顺便验证 (Q8d 复用), 不损失 SOP 意图。
**影响 if YES**: tasks.md status table 已含 default (B.2.0 24h 含 T13, B.2.Z 27h 不含 T13); proposal.md owner action #3 已改 "Phase B.2.0 T13"
**影响 if NO**: 回退 default; B.2.0=21h, B.2.Z=30h; risk #5 升级为 P0

**Owner 答**: ___

---

### Q2: OD-15 — Phase A.2 audit collapse?

**问**: Phase A.2 audit 是否 collapse 到 2-round (R1+R2) 而不是 4-round (R1-R4)?

**Context**:
- OD-12 §Q8c 锁 4-round
- `feedback_pre_merge_4round_convergence_template` proportionality: R3 stability + R4 strict 在 R2 全 SCOPE_OK 时是冗余
- R1 现有 verdict: 2 READY + 2 NEEDS_OWNER_INPUT → R2 是必跑 (验 owner 答案 + 0 NEW critical), R3+R4 视 R2 决定
- R2 收敛 (0 NEW critical, ≤2 important) 时 collapse 节省 ~2-3h wall

**AI 推荐**: **defer to R2 closure** (R1 现已 BLOCK_NEED_OWNER 不算 ScopeOK; 等 owner 答 + R2 verify 后再决)
**Rationale**: 当下不能 collapse 但 R2 可能允许; 不预先锁。

**Owner 答**: ___ (推荐: defer to R2)

---

### Q3: OD-3d — silknode-integration-contract 契约 1 generalize 到 Zhipu 直连?

**问**: silknode-integration-contract §契约 1 "no-storage 透传" 字面是 "silknode (Luxeno 品牌)" — 是否 generalize 适用所有上游 LLM provider, 含 Zhipu 直连 (open.bigmodel.cn)?

**Context**:
- M3 ZhipuClient 直接打 Zhipu 官方 API, 不走 silknode 中转
- 若契约 1 仅限 silknode → ZhipuClient 内部无 storage 约束 → r1-legal-memo v1.1 IS-3/IS-4 链可能 silent 失效
- generalize 后: ZhipuClient 内部仅 in-memory buffer + meta 日志, 无 disk log payload

**AI 推荐**: **YES, generalize**
**Rationale**: IS-3/IS-4 法理一致性 (vendor 不分, 都境内); 不 generalize 开漏洞。
**影响 if YES**: T8.5 Spec 已含 default 描述 (per OD-3d generalize)
**影响 if NO**: T8.5 改 "verbatim consume 仅 silknode, ZhipuClient 不受约束" + 单独 legal disclosure 写入 m3-handoff (额外 ~2h)

**Owner 答**: ___

---

### Q4: OD-3e — T9.8 multi-model benchmark 用作 sign-off hard gate?

**问**: T9.8 multi-model benchmark (S2/S3/S6 × 3 模型 × 3 次, 9 runs/state) 用作 M3 sign-off **硬 PASS/FAIL gate** vs **exploratory only** (写 handoff 但不 block)?

**Context**:
- Luxeno 已 M2 实战稳定 (148h 实测, 11 issue dispatch); 多模型 quality 是 nice-to-have
- 硬 gate + R1-I9 budget cap $5 可能不够 (3 状态 × 3 模型 × 3 次 = 27 runs, Zhipu metered, glm-5.1 tier 较贵)
- Quality threshold AI 推荐: S2 ≥80% / S3 ≥90% / S6 ≥66% (per R1-I8)
- 改硬 gate 需 budget 升 ~$15-20

**AI 推荐**: **exploratory only** (m3-handoff `multi_model_benchmark_gate=false`)
**Rationale**: M3 主要价值是 cycle-close + crash recovery + HA fallback, multi-model 是辅; 留 US-027 cost routing 做硬 gate。
**影响 if exploratory**: T9.8 已含 default; budget cap $5 sustain
**影响 if hard gate**: 改 m3-handoff + 升 budget cap $15 + Patch 05 加验收 D-extension

**Owner 答**: ___

---

### Q5: OD-3f — Zhipu pricing constants snapshot vs runtime API?

**问**: Zhipu pricing constants module (`zhipu_pricing.py`) 用 **snapshot 取数** (T10 实施日固定值, 6-month review trigger) vs **runtime API 拉取** (启动时实时 fetch)?

**Context**:
- Zhipu pricing 历史多次调整
- snapshot: 简单, 可 audit, 但 6 月内 silent 漂移
- runtime: 始终最新, 但 API 不稳定时启动 fail; 需额外 retry + cache

**AI 推荐**: **snapshot at T10 实施日 + 6-month review trigger**
**Rationale**: 简单 robust; 6 月 review 与 secret rotation 90-day cap 同 cadence; runtime fetch 引入 dep 不值。
**影响 if snapshot**: T10.3 已含 default `_PRICING_VERSION=1.0` + `_PRICING_FETCHED_AT=<T10 day>` + URL comment
**影响 if runtime**: 加 `aria_layer1/llm/zhipu_pricing_fetcher.py` (~3h) + retry policy + offline fallback to snapshot

**Owner 答**: ___

---

### Q6: OD-3g — ZhipuClient timeout policy

**问**: ZhipuClient per-call timeout 接受 AI 推荐 default `connect_timeout=5s` + `read_timeout=60s`, 还是自定义?

**Context**:
- Per-call hanging 会阻塞 ProviderRouter 整 retry budget (3 次 expo backoff 1s/2s/4s)
- ProviderRouter total fallback wall ≤ `3 × 65s = 195s` (cron tick 60min headroom 充裕)
- Default 与 SilknodeClient 同 baseline (M2 实战)

**AI 推荐**: **接受 default**
**Rationale**: 实战 baseline 校准; 60min tick 195s 占 5%; 充裕。
**影响 if default**: T8.6 已含 default
**影响 if 自定**: 改 T8.6 数值 (例如 connect=10s/read=120s); ProviderRouter total wall 重算

**Owner 答**: ___

---

### Q7: Q-NEW-1 — T12.4 kill -9 test scope: unit vs integration?

**问**: T12.4 (Hermes kill -9 lock test) 是 **unit test** (subprocess+SIGKILL+FakeAllocStatusProvider) vs **Tier-2 integration test** (real Hermes process on cluster)?

**Context**:
- Acceptance C (crash recovery) per Q6=A 默认 Tier-1 自动化集成 only
- T12.1 已是 unit (5-step harness with fresh hermes-extension instance)
- T12.4 区别: T12.1 是 fresh-restart (cleanup), T12.4 是 mid-state-kill (forced)
- unit 用 `subprocess.Popen + os.kill(pid, signal.SIGKILL)` 完全可重现, FakeAllocStatusProvider 注入 via env var
- integration 需 cluster + Hermes 进程权限, ~6h 额外

**AI 推荐**: **unit (subprocess + SIGKILL)**
**Rationale**: Q6=A Tier-1 sufficient; subprocess + signal 完全可重现; integration 推 T15 stretch (T15.7 已留位)
**影响 if unit**: T12.4 已含 default
**影响 if integration**: T15 stretch 加 ~6h Tier-2 cluster smoke; m3-handoff 加 `acceptance_c_tier2_evidence` field

**Owner 答**: ___

---

## 答完后流程

1. Owner 答 Q1-Q7 (建议直接 reply 简短 "Q1=YES, Q2=defer, Q3=YES, Q4=exploratory, Q5=snapshot, Q6=accept, Q7=unit", 或对每问独立答)
2. AI 把 owner 答案 inline 入 Spec (如有 deviate from default 才需改; sustain default 仅 commit 答案 record)
3. Phase A.2 **R2 fix-verify** (4-agent parallel, 各自 verify R1 closure + 0 NEW critical)
4. R2 verdict:
   - 4/4 SCOPE_OK_R2 (0 critical / ≤2 important) → 直接 Phase A.3 (collapse R3+R4 per OD-15)
   - ≥1 BLOCK or ≥3 important → R3 fix + stability
5. Phase A.3 OD-13 立 + baseline final lock + Approved (~1h)
6. Phase B.1 feature 分支 + Phase B.2 实施

## 引用

- R1 audit synthesis: `.aria/audit-reports/post_spec-2026-05-04T103702Z-us023-m3.md`
- OD-12 RESOLVED: `.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- R2 closeout (2026-05-03): `.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md`
- secret_rotation_deferred SOP: `.aria/decisions/2026-05-02-secret-rotation-deferred.md`
- Spec proposal: `openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md`
- Spec tasks: `openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/tasks.md`
- Aria 规范引用: `feedback_ai_代填_sign_off_pattern`, `feedback_pre_merge_4round_convergence_template`, `feedback_smoke_benchmark_truthiness`, `feedback_ad_slot_backfill_checkpoint`, `feedback_validator_repo_drift_guard_test`
