# Tasks — mid-post-spec-drift-checkpoint

> ✅ SHIPPED 2026-06-19 (v1.47.0, PR #88 `281388d`)。Cycle C of v1.47.0 release train。#79。新增条件触发 mid_post_spec 检查点。

## TG-A — config (DEFAULTS.json)
- [x] A1. `audit.checkpoints.mid_post_spec`: `"off"` (默认)。
- [x] A2. `audit.teams.mid_post_spec`: convergence/discussion/challenge 小队 (1-2 agent, tech-lead 为主)。
- [x] A3. `audit.mid_post_spec` trigger block (trigger: spec_drift_detected; source: 测试/SMOKE verdict_invalidated_assumptions 或 AI 识别)。

## TG-B — audit-engine SKILL.md
- [x] B1. 检查点列表加 `mid_post_spec` 行 (阶段 B, 侧重 spec 漂移校验, 调用方 phase-b-developer 条件触发)。
- [x] B2. single-round 约束说明 (类 post_closure: max_rounds=1, scope 限漂移点; mode 走 adaptive 但恒 single-round)。

## TG-C — agent-team-audit/audit-points.md
- [x] C1. 加 `## mid_post_spec` 检查点节: trigger / agents / blocking=false / 输出 append-only spec amendment → resume。

## TG-D — phase-b-developer SKILL.md
- [x] D1. B.2 后加条件触发步骤: 检测 spec 漂移 (机械 verdict_invalidated_assumptions 或 AI 识别) → 暂停 → mid_post_spec single-round → amendment → resume。

## TG-E — config-loader SKILL.md
- [x] E1. 配置表 + checkpoints 枚举 + config-example.md 同步 mid_post_spec (3-way parity)。

## TG-F — 验证 (Rule #6 substitute)
- [x] F1. structural: checkpoint 落 7→8; teams/trigger config 一致; single-round 约束记录; DEFAULTS/SKILL/example 3-way parity。
- [x] F2. dogfood-by-construction: 回放 TH v0.3.2 SMOKE-A path A drift → mid_post_spec 当时触发 → amendment → 省 4 天 stale 实施。
- [x] F3. 向后兼容: 默认 off + 旧配置映射不含 → 零影响。

## Phase B/C/D (release train)
- [x] agent-team review (tech-lead checkpoint 设计 + knowledge-manager doc 一致性)。
- [x] commit 到 release 分支。
- [x] 随 v1.47.0 批量 Phase D + close #79 + 归档。
