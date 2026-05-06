# Patch 03 — PRD §M3 验收 A 'cluster smoke gate' → 'Tier-1 自动化集成 + carryover #1 cluster verification embedded'

> **Spec**: aria-2.0-m3-cycle-close-glm-routing-recovery
> **Trigger**: OD-12 §Q6=A (Tier-1 only, ~6h, owner explicit 接受 weakness)
> **Phase**: A.1.4 (起草) → T16.4 (commit, with Patch 02 §M3 detail 章节同期)
> **Status**: Draft (Phase A.1.4 起草)

## Why

OD-12 §Q6=A owner 决议: M3 验收 A (≥10 issue 走完整 cycle) **不强制 Tier-2 cluster smoke gate**, 而是 **Tier-1 自动化集成 only** + cluster verification 嵌入 carryover #1 (T1 aria-layer2-runner HCL 部署) implementation 验证。

理由:
- Tier-1 fake-cycle test (≥10 cycle 模拟 mock provider) 已能 fully exercise 状态机 + alloc 状态映射 + 计算 cycle_start_ts/cycle_end_ts
- Tier-2 cluster verification 在 T1 deploy 验证 aria-layer2-runner job dispatch + alloc launch 已经覆盖关键真链路径
- Owner explicit 接受 Tier-1 only weakness: 后续可升级 if needed (T15 stretch 提供 Tier-1 + Tier-2 同时, ~12-14h, 不强制)

R2 qa-engineer R2 OBJ-3 / OBJ-9 raised Tier-2 缺失 weakness, owner Q6=A 锁定接受 → Phase A.2 audit 不再 reopen。

## 操作

### 修改 PRD `docs/requirements/prd-aria-v2.md` §M3 detail (Patch 02 新增章节内)

**新增段** (在 Patch 02 新增 §M3 detail 章节末尾, "Out of Scope" 段之后追加):

```markdown
**验收 A 测试 Tier**:
- **Tier-1 自动化集成 (主)**: ≥10 issue 走完整 S0→S9_CLOSE in fake-cycle test (FakeAllocStatusProvider + FakeNomadClient + FakeSilknodeClient + FakeZhipuClient)
- **Tier-2 cluster verification (副, embedded in T1)**: aria-layer2-runner HCL deploy on Aether 后, sample dispatch 实测 alloc launch + alloc state 推进 (carryover #1 implementation 验证)
- **不强制独立 Tier-2 cluster smoke gate**: Q6=A explicit waive, T15 stretch 可选提供 ≥12-14h
- **Test infrastructure**: 复用 M2 fixtures (FakeAllocStatusProvider / FakeNomadClient / FakeSilknodeClient) + 新增 FakeZhipuClient (per Q1=D' 双 provider)
- **m3-handoff.yaml 字段**: `acceptance_a_actual_dispatches=10` (Tier-1 实测), `acceptance_a_tier2_carryover_verified=true` (T1 部署后)
- **Risk**: Tier-1 only 弱于 Tier-1+2, owner 接受
```

## 验证

- [ ] PRD §M3 detail 含 "验收 A 测试 Tier" 段
- [ ] 段中显式 Tier-1 / Tier-2 分工 + Q6=A waive 注
- [ ] Spec proposal.md §Acceptance 表格 ID=A 行 Tier 字段一致 (Tier-1 自动化集成 only)
- [ ] Spec tasks.md T15.1 / T15.2 / T15.3 与本 Patch 段描述一致

## 引用

- OD-12 §Q6=A: `.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- R2 qa OBJ-3 / OBJ-9: `.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md`
