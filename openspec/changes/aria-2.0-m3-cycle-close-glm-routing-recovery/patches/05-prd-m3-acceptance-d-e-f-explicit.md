# Patch 05 — PRD §M3 验收 D/E/F 显式化

> **Spec**: aria-2.0-m3-cycle-close-glm-routing-recovery
> **Trigger**: OD-12 §Q1=D' (验收 D HA fallback) + §Q5=A (验收 E schema migration) + §Q8d (验收 F secret rotation post-benchmark)
> **Phase**: A.1.4 (起草) → T16.4 (commit, with Patches 02/03/04 §M3 detail 章节同期)
> **Status**: Draft (Phase A.1.4 起草)

## Why

PRD §M3 字面 (line 510 US 列表) 仅含 "Crash recovery" 一项验收暗示, 不含:
- 验收 D: GLM 多 provider HA fallback (Q1=D' 锁定)
- 验收 E: Schema migration v2 backward-compat (Q5=A 锁定)
- 验收 F: Secret rotation 完成 + post-rotation perf benchmark (Q8d 锁定)

Spec proposal.md §Acceptance 表格已含 6 行 (A/B/C/D/E/F), 但 PRD 字面缺失会让任何 PRD↔Spec audit 报 "PRD 验收清单不完整" (per `feedback_spec_reframe_in_session` 3 处一致)。

R2 tech-lead R2 5 patches §5 explicit 提及: "PRD §M3 验收 D/E/F 显式化"。

## 操作

### 修改 PRD `docs/requirements/prd-aria-v2.md` §M3 detail (Patch 02 新增章节内)

**新增段** (在 Patch 04 "验收 B p50 methodology" 段之后追加, 与 Patches 03/04 同 §M3 detail 章节):

```markdown
**验收 D — GLM 多 provider HA fallback (per Q1=D')**:

| 项 | 值 |
|---|---|
| Metric | `fallback_chain_json` 含 `provider=luxeno` + `provider=zhipu` 两类 entry (≥1 cycle) |
| 触发模式 | Luxeno 5xx 模拟 (test 用 `LuxenoFailureInjector` fixture) → 3 次 expo backoff (1s/2s/4s) → fallback Zhipu |
| Test matrix | parameterized 3 state × 5 fallback path × 6 dict field assertion ≥ 12 cases (per R2 I8) |
| Fallback 触发条件 | 被动 fallback (非主动 race), 仅 5xx + 429 + timeout 触发 |
| Schema 字段 | `fallback_chain_json TEXT` (schema v2 dict-array, write-time exhaustive transform from v1 字符串数组) |

**验收 E — Schema migration v2 backward-compat (per Q5=A)**:

| 项 | 值 |
|---|---|
| Metric | T15.3 实际 11-row dispatches.db 快照 fixture migration test PASS, **0 数据丢失** |
| Migration 模式 | additive-first (5 新 col + dict transform, 同 transaction) |
| Rollback | SQLite ALTER 失败自动回滚, 不需手动 rollback 脚本 |
| Backfill rules | 历史 row `provider_cost_model='subscription_flat'` (per AD-M1-12) + 历史 S9_CLOSE/S_FAIL row `cycle_start_ts=state_entered_at` (placeholder 注 in `migration_notes` table) |
| inline UNIQUE 处理 | 保留 (drop 推 schema v3 / M4 / US-024) — 应用层 dedupe (e36beb2) 续用 |
| schema_meta | `INSERT ('schema_version', '2.0')` |

**验收 F — Secret rotation 完成 + post-rotation perf benchmark (per Q8d)**:

| 项 | 值 |
|---|---|
| Metric | `rotation_completed=true` + date 在 m3-handoff.yaml + post-rotation 验收 B PASS |
| Rotation scope | 一次性 5 keys: LUXENO_API_KEY + 3 FEISHU_* + ZHIPU_API_KEY |
| 时机 | T13 mid Phase B.2 (per OD-12 §Q8d, 不晚于 secret_rotation_deferred 90-day hard cap 2026-08-02) |
| Post-rotation verify | T14 perf benchmark (验收 B) 复用 — 验证新 keys 有效 |
| SOP 引用 | `.aria/decisions/2026-05-02-secret-rotation-deferred.md` (canonical) |
| Tier | Tier-2 (依赖 cluster + Nomad Variable update) |

**完整 6-验收 (A/B/C/D/E/F) 总表**: 见 [Spec proposal.md §Acceptance](../../openspec/changes/aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md)

**M3.done** = (A ∧ B ∧ C ∧ D ∧ E ∧ F) ∧ (m3-handoff.yaml validator PASS) ∧ (owner sign-off + tech-lead co-sign + 268 → 300+ tests baseline)
```

## 验证

- [ ] PRD §M3 detail 含 "验收 D / E / F" 三段
- [ ] 每段独立表格 (Metric / 触发 / Schema / Test / Tier 字段)
- [ ] Spec proposal.md §Acceptance 表格 6 行 vs PRD §M3 detail 6 段一对一一致 (per `feedback_spec_reframe_in_session` 3 处)
- [ ] m3-handoff.yaml schema v1.0 (T16.1) 含本 6 验收所有 metric 字段 placeholder
- [ ] Spec tasks.md T13/T14/T15/T9/T3 与本 Patch 段描述一致

## 引用

- OD-12 §Q1=D' / §Q5=A / §Q8d: `.aria/decisions/2026-05-03-od-12-m3-kickoff-package.md`
- secret_rotation_deferred SOP: `.aria/decisions/2026-05-02-secret-rotation-deferred.md`
- R2 closeout 5 patches §5: `.aria/decisions/2026-05-03-r2-closeout-phase-a1-readiness.md`
- Spec proposal.md §Acceptance: `../proposal.md`
