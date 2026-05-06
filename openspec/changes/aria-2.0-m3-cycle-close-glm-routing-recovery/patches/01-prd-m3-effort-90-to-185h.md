# Patch 01 — PRD §M3 effort 90h → 185h (OD-13 立)

> **Spec**: aria-2.0-m3-cycle-close-glm-routing-recovery
> **Trigger**: OD-12 §Q2 baseline lock (185h) + R2 tech-lead R2-3 / I7 (OD-13 应 Phase A.3 立, 不等 mid-sprint)
> **Phase**: A.3 (commit 时机 — 不在 Phase B.2)
> **Status**: Draft (Phase A.1.4 起草)

## Why

OD-12 §Q2 owner 锁定 M3 baseline = **185h hard** (相对 PRD §M3 字面 90h, ×2.06 inflation):
- M2 OD-11 carryover (Layer 2 HCL/alloc_provider/migration v2/cycle E2E): 21h
- PRD §M3 base scope (reconciler/crash recovery/Nomad hardening): 70h
- S2/S3 prompt scaffolding (ai R1 OBJ-2): 18h
- Q1=D' multi-model routing + benchmark: 8h
- Q1=D' ProviderRouter abstraction + ZhipuClient: 10h
- Audit overhead (混合 Phase A.2 4-round + B.2 scope-bounded + D 4-round): 25h
- Owner action items × 4: 4h
- Spec drafting (Phase A.1.1+A.1.2+A.1.3): 8h
- Phase A.2 audit (R1-R4 4-round): 4h
- Subtotal: 168h
- 10% buffer (R1-TL-1 推荐): +17h
- **Total**: 185h

历史校准: M2 PRD 100h → OD-7=b 146h → OD-8 156h → 实测 148h (5% within), ×1.48 inflation。M3 ×2.06 是 *scope discovery 后真实 inflation*, 与 M2 同模式。

R2 tech-lead I7: OD-13 应 **Phase A.3 立, 不等 mid-sprint**, 否则 PRD 字面与实施 baseline diverge 让 Phase B.2 期间任何状态扫描误标 in_progress 工时偏离 (state-scanner 预期值校准 misalign)。

## 操作

### 修改 PRD `docs/requirements/prd-aria-v2.md` line 404

**Before** (current):
```
M3 (Week 13-16)   双 provider + Nomad integration (90h)
```

**After**:
```
M3 (Week 13-16)   Layer 2 cycle close + GLM 多模型 routing + Crash recovery (185h, OD-13 lock per US-023 §OD-12 §Q2)
```

> **注**: title 变化与 Patch 02 合并 commit (同一 line); 工时 90h → 185h 单独立 OD-13 in Phase A.3。

### 修改 PRD `docs/requirements/prd-aria-v2.md` 注释段 (line 412 附近)

**Before**:
```
**注**: 工时估算基于 R3 挑战组实测重估 (R3 讨论组估 380h, Code Reviewer 实测 750h)。选取实测值作为 PRD 工时。
```

**After** (在末尾追加):
```
**注**: 工时估算基于 R3 挑战组实测重估 (R3 讨论组估 380h, Code Reviewer 实测 750h)。选取实测值作为 PRD 工时。

**M3 OD-13 update (Phase A.3, 2026-05-04)**: M3 工时由 90h → 185h, 因 US-023 brainstorm OD-12 §Q2 揭露 scope discovery 后真实 inflation (×2.06, 与 M2 ×1.48 同模式)。新基线见 [US-023.md §估算](../requirements/user-stories/US-023.md) 与 [aria-2.0-m3-cycle-close-glm-routing-recovery proposal.md](../../openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md) Phase 路线图。
```

### 全 PRD 总工时 line 409 同步

**Before**:
```
合计:             ~750h ≈ 30 周单人 / 9 月 50% 投入
```

**After**:
```
合计:             ~845h ≈ 33 周单人 / 10 月 50% 投入 (M3 90→185h per OD-13 2026-05-04)
```

## 验证

- [ ] PRD line 404 显示 "(185h, OD-13 lock per ...)"
- [ ] PRD §里程碑概览注释段含 OD-13 update 段
- [ ] PRD line 409 总工时同步到 845h
- [ ] OD-13 立: `.aria/decisions/2026-05-04-od-13-prd-m3-effort-90-to-185h.md` (Phase A.3 配套)
- [ ] Spec proposal.md `OD-13 PENDING` 改为 `OD-13 RESOLVED 2026-05-04` (Phase A.3 闭合)

## 引用

- OD-12 §Q2 baseline: `.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- R2 closeout I7: `.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md`
- M2 history (×1.48): PRD 100h → OD-8 156h → 实测 148h
