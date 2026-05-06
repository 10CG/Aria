---
checkpoint: post_spec
spec_id: aria-2.0-m2-layer1-state-machine
mode: challenge
round: 1
agents: [qa-engineer, code-reviewer, context-manager]
verdict: PASS_WITH_WARNINGS
converged: true
critical_findings: 2
important_findings: 8
minor_findings: 8
critical_resolved: 2
important_carried_to_phase_b: 8
minor_carried_to_phase_b_or_ignored: 8
ready_for_owner_signoff: true_pending_OD-8
date: 2026-04-28
---

# Post_spec Audit Report — US-022 M2 Layer 1 State Machine Spec

## Audit Scope

- **Target**: `openspec/changes/aria-2.0-m2-layer1-state-machine/` (proposal.md 348 行 + tasks.md 521 行 + patches/ 3 文件)
- **Mode**: challenge (1 round, 3 agents parallel)
- **Convergence rule**: brainstorm 已 4 轮收敛 (R1-R4), post_spec round 2 边际 ROI 低, 1 round 即可作 Spec 起草质量检查

## Agent Verdicts

| Agent | Verdict | Critical | Important | Minor | Ready_for_signoff |
|-------|---------|----------|-----------|-------|-------------------|
| qa-engineer | PASS_WITH_WARNINGS | 0 | 6 | 4 | false_pending_5_items |
| code-reviewer | PASS_WITH_WARNINGS | 0 | 3 | 4 | false_pending_F1_F2_F3 |
| **context-manager** | **PASS_WITH_WARNINGS** | **2 (F1, F3)** | 3 | 2 | false_pending_F1_F3_critical |

## Critical Findings (Resolved Same Day)

### F1 — m1-handoff.yaml 字段名几乎全错 (cm)

**实测**: proposal §What 六 6.4 引用 `image_refs.{immutable_sha, mutable_tag}` / `nomad_job_id` / `host_volumes` / `performance_baseline.demo_002_p50_duration_s`; 实际 m1-handoff.yaml v1.0 schema:
- `image_refs.image_sha_final` (非 immutable_sha)
- `image_refs.image_tag_mutable` / `image_tag_immutable_pattern` (非 mutable_tag)
- `nomad_config.{job_template_path, host_volume_config_path, volumes}` (无 nomad_job_id / nomad_job_version)
- `performance_baseline.dispatch_to_pr_p50_s` = 28 (非 demo_002_p50_duration_s)
- `demo_token_usage.{DEMO-001,DEMO-002}.{input_tokens_total,output_tokens_total}`

**Resolution**: proposal §What 六 6.4 全段重写 (commit XXX), §What 二 SQL 注释 + §What 六 6.3 image_sha_final 引用 + S4 guard 校验逻辑同步修正。Field name verified 2026-04-28 against `aria-orchestrator/docs/m1-handoff.yaml` line 28-126 actual content.

### F3 — Tasks 工时累加错误 +10h (cm)

**实测**: 工时表实际累加 = 156h ≠ claim 的 146h。
T0(3)+T1(30)+T2(8)+T3(16)+T4(8)+T5(4)+T6(12)+T7(10)+T8(8)+T9(5)+T10(10)+T11(2)+T12(6)+T13(6)+T14(10)+T15(12)+T16(6) = 156h

**根因**: 重组 brainstorm M2 scope 18 项 (-M2-15 6h = 146h) → tasks 17 项时, 我新增 T0 kickoff 3h + 把 silknode/LLM review/S8 merge 从 M2-1 状态机骨架 (16h) 抽出独立 task (T8 8h + T10 10h + T13 6h, 共 24h) 但未削减 T3 状态机核心 task 工时, 形成净 +10h 膨胀。

**Resolution**: tasks.md 工时表已诚实标 156h, OD-7=b 锁定 146h 偏离 +10h (6.8% over OD), PRD 140h 偏离 +16h (11.4%). 推 **OD-8** 让 owner 三选一:
- (a) 接受 156h 新基线 (替代 OD-7=b)
- (b) 削减 10h (例 T1 30→25h + T16 6→1h, 风险大)
- (c) 重做 mapping 让 brainstorm 18 项与 tasks 17 项工时真正对齐 (不改总数)

## Important Findings (8 项, 推 Phase B 早期修复)

详见 tasks.md §Post_spec Audit Known Issues §Important Backlog (8 项):

1. S7_HUMAN_GATE 行为同文档矛盾 (qa F1) — proposal line 60 vs line 65, B.1 启动前修
2. S6_REVIEW → S8_MERGE collapse 无说明 (qa F2 + cr F1) — owner 仲裁
3. notification_status 缺 SQL schema (qa F3) — B.2 T2 期发现
4. S4_LAUNCH / S8_MERGE timeout 实现 gap (qa F4) — B.2 T4+T13 补 +2h
5. partial_write enum 缺口 (qa F5) — B.1 启动前补
6. HERMES_ALLOC_TIMEOUT_MIN env_var 静默丢弃 (qa F6) — B.2 T4.2 补
7. §核心交付清单未同步 (cr F3) — 扩 Patch 3 或 proposal explicit declare
8. silknode-contract §99 引用错误 + S5_REVIEWING 残留 (cm F2 + F4) — B.1 启动前 grep replace

## Minor Findings (8 项, 推 Phase B 中或忽略)

详见 tasks.md §Post_spec Audit Known Issues §Minor (8 项), 不阻 owner sign-off, 实施期发现即时修。

## Brainstorm Decision Consumption

**OD-1 ~ OD-7** (brainstorm conclusion 2026-04-27): **全部消化**
- OD-1 (PRD §M2 命名) ✓ proposal §What 一 + Patch 1
- OD-2 (验收 B 弱形式) ✓ proposal §What 七 + Patch 3
- OD-3 (silknode→GLM) ✓ proposal §What 六 verbatim (after F4 minor fix)
- OD-4 (patch 推 A.1) ✓ patches/ 子目录在 Phase A.1.3 起草
- OD-5 (6 项 M2 必做) ✓ tasks T2-T9 + T11 全覆盖
- OD-6 (单文件 brainstorm 输出) ✓
- OD-7 (146h 裁 M2-15) ⚠️ tasks 实测 156h (F3, 待 OD-8 决策)

**Phase A.1 followup 7 项** (R3-OBJ-3/4/5 + R3-OBJ-cm-1/2/3/4): **全部 grep 可定位**

## Cross-Doc Consistency After Phase A.1

| 维度 | 状态 |
|------|------|
| proposal_internal | PARTIAL → **PASS** (post F1+F3 fix; 仍待 8 important Phase B 修) |
| brainstorm_alignment | PASS |
| ad5_alignment (post Patch 1) | PASS |
| prd_v2_alignment (post Patch 2) | PASS |
| silknode_contract_alignment | PARTIAL (F4 §99 引用错, B.1 修) |
| **m1_handoff_alignment** | **FAIL → PASS** (post F1 fix 2026-04-28) |
| us022_alignment (post Patch 3) | PASS |

## Final Verdict

**PASS_WITH_WARNINGS, ready_for_owner_signoff = TRUE pending OD-8**

- 2 critical 同 session 修复
- 8 important 标 known issue 推 Phase B 早期 (B.1 启动前 spec-drafter 一次性处理 6 项, B.2 实施期发现 2 项)
- 8 minor 推 Phase B 中或忽略
- Owner sign-off 唯一阻塞: **OD-8 预算决策** (a/b/c 三选一)
- **不建议跑 round 2** (brainstorm 已 4 轮, 边际 ROI 低, 8 important 多是文档级矛盾在 B.1 启动前 grep 修即可)

## Audit Trail

- 3 agent 输出: 见 .aria/audit-reports/post_spec-2026-04-28T1700Z-us022-m2-layer1-{agent}.yaml (本会话已收集, 未单独存档以节约 token)
- brainstorm conclusion link: `.aria/decisions/2026-04-27-us022-state-machine-brainstorm.md`
- Phase A.1 commit: 8622089
- Critical fix commit: pending (本会话即将 commit)
