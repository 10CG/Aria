# Patch 02 — PRD §M3 'dual provider' 字面 → 'multi-model GLM routing + cross-provider HA fallback'

> **Spec**: aria-2.0-m3-cycle-close-glm-routing-recovery
> **Trigger**: OD-12 §Q1=D' (Luxeno primary + Zhipu HA fallback + GLM 多模型 routing) + R2 tech-lead R2-1 / I6 (PRD §M3 'dual provider' 字面 与 Q1=D' divergence)
> **Phase**: A.1.4 (起草) → T16.4 (commit)
> **Status**: Draft (Phase A.1.4 起草)

## Why

PRD §M3 字面 "双 provider + Nomad integration" 暗示 **Anthropic ⇄ GLM 切换**, 但 OD-12 §Q1=D' owner 决议 supersedes:

- Owner 仅 Anthropic claude.ai 订阅, **无 API key** 账号 (Q1=D' 替代方案)
- M3 双 provider 实际为 **Luxeno (primary, flat sub) + Zhipu 官方 (HA fallback, per-token)** — 两 provider 都暴露 GLM 模型
- 同 provider 内 quality routing: S2=glm-4.5-air / S3=glm-5-turbo / S6=glm-5.1
- Anthropic provider 保留 deprecated (per AD-M1-12 supersedes AD-M1-6); M5+ 视需复活
- Legal: OD-9 续延, m1-legal-carryover §9 不重审 (Zhipu 也境内 vendor)

R2 tech-lead R2-1: 不 patch PRD 字面会导致 Phase B.2 期间 audit "Spec ↔ PRD 字面 divergence" 误报 (per `feedback_spec_reframe_in_session` 必须 3 处 reframe)。

## 操作

### 修改 PRD `docs/requirements/prd-aria-v2.md` line 404 (合并 Patch 01)

**Before**:
```
M3 (Week 13-16)   双 provider + Nomad integration (90h)
```

**After** (合并 Patch 01 工时 + Patch 02 命名):
```
M3 (Week 13-16)   Layer 2 cycle close + GLM 多模型 routing + Crash recovery (185h, OD-13 lock per US-023 §OD-12 §Q2)
```

### 修改 PRD `docs/requirements/prd-aria-v2.md` line 510 US 列表

**Before**:
```
| US-023 | Aria 2.0 M3 — 双 provider + Nomad integration + Crash recovery | M3 | HIGH |
```

**After**:
```
| US-023 | Aria 2.0 M3 — Layer 2 cycle close + GLM 多模型 routing + Crash recovery (Q1=D' Luxeno+Zhipu HA + state-aware model chain) | M3 | HIGH |
```

### 新增 PRD §M3 detail 章节 (line 467 §M2-M6 之前)

**插入位置**: 在 line 444-466 §M1 章节之后, line 467 §M2-M6 之前。

**新增内容**:
```markdown
### M3: Layer 2 cycle close + GLM 多模型 routing + Crash recovery (Week 13-16+)

> **基线**: 185h hard (OD-12 §Q2 lock 2026-05-03; OD-13 Phase A.3 立 2026-05-04)
> **Spec**: [aria-2.0-m3-cycle-close-glm-routing-recovery](../../openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md)
> **Status**: Draft (Phase A.1, 起草中)

**目的**: 将 M2 Layer 1 状态机驱动 dispatch (S0→S4_LAUNCH 真发) 升级为 **Layer 1+Layer 2 完整闭环 (S0→S9_CLOSE)** + 重启可恢复 + 双 provider HA + 多模型 quality routing。

**Provider 架构 (Q1=D')**:
- **Primary**: Luxeno (api.luxeno.ai/v1, flat subscription)
- **HA Fallback**: Zhipu 官方 (open.bigmodel.cn/api/paas/v4, per-token billing, 已充值)
- **Anthropic**: deprecated (per AD-M1-12 supersedes AD-M1-6, owner subscription-only no API key)

**模型路由 (state-aware quality routing)**:
- S2_DECIDE → `glm-4.5-air` (cheap)
- S3_BUILD_CMD → `glm-5-turbo` (mid-tier, 对标 Sonnet)
- S6_REVIEW → `glm-5.1` (top-tier, 对标 Opus)
- Per-state fallback ladder (model degrade): `5.1 → 5-turbo → 4.5-air`

**核心交付**:
- ≥10 个 synthetic issue 走完整 Layer 1+Layer 2 cycle (S0→S9_CLOSE) 含 ≥1 真实 PR merged
- Cycle p50 ≤ M1 baseline × 1.5 = 47.25s (S1_SCAN→S9_CLOSE wall, fallback_triggered=false 过滤)
- Hermes kill -9 重启实测: pre-restart S5_AWAIT 自动 resume polling
- Luxeno 5xx 模拟 → Zhipu 接管 (fallback_chain_json dict-array 含两类 entry)
- 独立 Reconciler periodic job (30min) 检测 stuck S5_AWAIT > 60min → S_FAIL(stuck) routing + Feishu 告警
- Schema migration v2 (additive-first): 5 新 col + dict fallback_chain_json transform
- Secret rotation T13 一次性 5 keys (含 ZHIPU_API_KEY, post-rotation 用 验收 B 顺便验证)

**验收**: 见 [Spec proposal.md §Acceptance](../../openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md) (A: ≥10 cycle / B: p50≤47.25s / C: crash recovery / D: HA fallback / E: schema migration zero loss / F: rotation+benchmark).

**M2 input 契约**: 见 [Spec proposal.md §M2 Input 契约](../../openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md), 复用 m2-handoff.yaml schema v1.0 (additive-only).

**Out of Scope**: M4 完整 human gate / M5 防漂移 / inline UNIQUE drop (推 v3) / LLM-decided reconciler / 其他 5 状态 crash recovery (M3 仅 S5_AWAIT)。

**Phase 路线图**:
- A.1 (~12h): proposal + tasks + 5 patches drafting
- A.2 (~4h): post_spec audit 4-round
- A.3 (~1h): OD-13 PRD patch + baseline lock + Approved
- B.1 (<0.5h): feature 分支
- B.2.0 (~21h): M2 carryover (T1-T4)
- B.2.1 (~90h): M3 new scope (T5-T12)
- B.2.Z (~30h): E2E + handoff (T13-T16)
- C+D: 集成 + 归档
```

## 验证

- [ ] PRD line 404 标题 "Layer 2 cycle close + GLM 多模型 routing + Crash recovery" 替换 "双 provider + Nomad integration"
- [ ] PRD line 510 US-023 标题 reframe 含 "Q1=D'" reference
- [ ] PRD 新增 §M3 detail 章节 (Patches 03/04/05 验收细节嵌入)
- [ ] Spec proposal.md §Why 第三段 (Anthropic 不引入) 与 PRD §M3 detail Provider 架构段一致 (3 处 reframe per `feedback_spec_reframe_in_session`)

## 引用

- OD-12 §Q1=D': `.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- AD-M1-12: `aria-orchestrator/docs/architecture-decisions.md#ad-m1-12`
- OD-9 (silknode→Luxeno reframe): `.aria/decisions/2026-05-02-od-9-silknode-luxeno-reframe.md`
- m1-legal-carryover §9: M1 closeout legal docs
- R2 closeout I6: `.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md`
