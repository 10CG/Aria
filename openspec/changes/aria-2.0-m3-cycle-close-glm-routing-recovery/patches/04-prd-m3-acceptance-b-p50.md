# Patch 04 — PRD §M3 验收 B p50 baseline 'M1 ×1.5' → '47.25s + S1_SCAN→S9_CLOSE wall + fallback_triggered=false filter'

> **Spec**: aria-2.0-m3-cycle-close-glm-routing-recovery
> **Trigger**: OD-12 §Q7=C (S1_SCAN→S9_CLOSE wall + filter, 显式 methodology) + OD-11 carryover (M2 验收 D WAIVED → M3 复活)
> **Phase**: A.1.4 (起草) → T16.4 (commit, with Patch 02 §M3 detail 章节同期)
> **Status**: Draft (Phase A.1.4 起草)

## Why

OD-12 §Q7=C owner 锁定验收 B 测量 methodology:
- p50 计算: `median(cycle_end_ts - cycle_start_ts) WHERE state='S9_CLOSE' AND fallback_triggered=false`
- 阈值: `m1_demo_002_p50_s × 1.5 = 31.5 × 1.5 = 47.25s`
- 样本 size: ≥10 cycles (与验收 A 一致)
- Schema 字段已含 (cycle_start_ts + cycle_end_ts in schema v2 per Patch 02 + Spec T3)
- Methodology 写入 m3-handoff.yaml `performance_vs_m1.m3_p50_methodology` 字段

PRD §M3 原字面 "M1 ×1.5" 不带 filter 条件 (fallback_triggered) 也不锁定 wall 起止点 (S1_SCAN vs S0_IDLE, S9_CLOSE vs S_FAIL)。Phase B.2 期间任何 ambiguity 会让 audit 误报 spec drift。

R2 tech-lead R2-1 / I6: 必须 explicit methodology in PRD + Spec + handoff 三处一致 (per `feedback_spec_reframe_in_session`)。

## 操作

### 修改 PRD `docs/requirements/prd-aria-v2.md` §M3 detail (Patch 02 新增章节内)

**新增段** (在 Patch 03 "验收 A 测试 Tier" 段之后追加):

```markdown
**验收 B p50 methodology (per Q7=C)**:

| 项 | 值 |
|---|---|
| Metric | `median(cycle_end_ts - cycle_start_ts)` |
| Filter | `state='S9_CLOSE' AND fallback_triggered=false` (healthy path only) |
| Wall 起点 | S1_SCAN entry timestamp (cycle_start_ts) |
| Wall 终点 | S9_CLOSE entry timestamp (cycle_end_ts) |
| 阈值 | `m1_demo_002_p50_s × 1.5 = 31.5 × 1.5 = 47.25s` |
| 样本 size | ≥10 cycles (与验收 A 一致) |
| Post-rotation | 必须在 T13 secret rotation 后测量 (Q8d 复用) |

**Fallback 路径独立 metric**: `fallback_triggered=true` cycles 不计入 p50, 单独 metric `uptime_pct = count(state='S9_CLOSE') / total_cycles` 跟踪 (M3 不强制阈值, US-027 cost routing 接续)。

**Schema 字段** (per schema v2, Spec T3):
- `cycle_start_ts TEXT`: S1_SCAN entry 时由 `_handle_s1_scan` 设
- `cycle_end_ts TEXT`: S9_CLOSE 或 S_FAIL entry 时由 `_handle_s9_close` / `_handle_s_fail` 设
- `fallback_triggered BOOLEAN`: ProviderRouter 落 fallback 时由 wire-in code 设 (M2 已字段, M3 复用)

**m3-handoff.yaml 字段**:
- `performance_vs_m1.m3_p50_methodology`: 'S1_SCAN→S9_CLOSE wall + fallback_triggered=false filter'
- `performance_vs_m1.m3_p50_actual_s`: 实测值
- `performance_vs_m1.passed`: bool
- `performance_vs_m1.measured_post_rotation`: bool (Q8d)
```

## 验证

- [ ] PRD §M3 detail 含 "验收 B p50 methodology (per Q7=C)" 段
- [ ] 段含 metric / filter / wall 起止 / 阈值 / 样本 size / post-rotation 6 字段
- [ ] Spec proposal.md §Acceptance 表格 ID=B 行 metric 一致 ("47.25s, fallback_triggered=false 过滤")
- [ ] Spec tasks.md T14 (perf benchmark) 步骤映射 PRD methodology
- [ ] m3-handoff.yaml schema v1.0 (T16.1) 含本 4 字段 placeholder

## 引用

- OD-12 §Q7=C: `.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- OD-11 (M2 验收 D WAIVED carryover): `.aria/decisions/2026-05-03-od-11-t15-4-5-perf-reframe.md`
- M1 demo_002 baseline: `aria-orchestrator/docs/m1-handoff.yaml` (`m1_demo_002_p50_s = 31.5`)
- R2 tech-lead R2-1 / I6: `.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md`
