---
round: R2
checkpoint: post_planning
mode: convergence
spec: pre-merge-gate-no-run-for-branch
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
seats: [A1-tech-lead, A2-backend-architect, A3-qa-engineer, A4-code-reviewer, A5-knowledge-manager]
verdicts: {A1: PASS_WITH_WARNINGS, A2: PASS_WITH_WARNINGS, A3: PASS_WITH_WARNINGS, A4: PASS_WITH_WARNINGS, A5: PASS_WITH_WARNINGS}
votes: {A1: REVISE, A2: REVISE, A3: REVISE, A4: REVISE, A5: REVISE}
verdict: PASS_WITH_WARNINGS
converged: false
incomplete: false
r1_disposition: {closed: 33, partial: 8, not_addressed: 0}
totals: {critical: 0, major: 10, minor: 20}
dedup_clusters: 8
timestamp: 2026-08-22T21:30:00Z
---

# post_planning R2 聚合 — detailed-tasks.yaml v2 → v3

五席 REVISE, 0 Critical。R1 12 簇全部方向落地; Major 集中在两类「声称 ≠ 字段」: (a) TASK-004 exec_order 前移只改了散文没改机检字段 (四席命中; memory `scoped_git_add_splits_claim` 同形); (b) 换依赖边时切断了 TASK-003 的传递闭包 (三席命中)。v3 起用**程序化断言**取代人工核: exec_order > 所有依赖 / TASK-003 ∈ 11 个下游闭包 / 逐任务 reason / total_tasks 一致。

## 处置表 (→ v3, 已落, 断言通过)

| # | 来源 | 内容 | v3 处置 |
|---|---|---|---|
| 1 | A1-M1 + A2-M1 + A3-M1 + A4-m4 + A5-M2 | TASK-004 exec_order 仍 4 / 物理位置 / parent 未随处置动 | exec_order 全表重编 (004=3, 002=4, 003=5 …); 物理块移到 P1 首位; parent P1; TASK-002 依赖 004 (机检边) |
| 2 | A1-M2 + A4-M1 + A5-M1 | TASK-003 闭包丢失: 005/006/010/012/014 不经 003; TASK-006 调 compute_verdict 却不依赖 003 | 005/006/010 加边 → 003; 014 加边 → 013 (013 依赖 003/011); 断言 003 ∈ 11 个下游闭包 |
| 3 | A1-M3 + A4-m2 | B.1 分支创建零承载 (aria 子模块分支 + 主仓分支); 「B.1 起主仓分支」写在 exec_phase C | 新 TASK-000b (B.1, 两仓分支, detached-HEAD 守则); 002/004/008/001 依赖 000b; TASK-015 (ii) 改「在 000b 建的分支上」 |
| 4 | A4-M2 + A1-m3 | false 分支 proposal 自删 (§3.5「整组从本 spec 删除」) 零承载, 归档件会描述未实现能力 | INV-3 rule 改写; TASK-016 加 conditional_parts (归档前按 §3.5 删文本 + checklist 1 N/A) + 依赖 001 |
| 5 | A2-M2 + A1-m1 | INV-1 验证「父提交 checkout」模糊且挂在不 commit 的 agent 上 | 非破坏性 `git show <commit>^:path` 核验; 落 TASK-013 (改 agent main-loop) verification |
| 6 | A3-M2 + A1-m5 | SC-15 绑定名钉在消费任务, 产出任务无承诺且要求参数化 | TASK-002 deliverables 承诺具名非参数化用例 `test_sc2_trigger_matched_message`; TASK-012 引用之 |
| 7 | A1-m2 / A1-m6 / A4-m1 / A4-m3 / A1-m7 / A1-m8 | 条件组无 grep 负控 / SC-14 脚本无 deliverable 且 km 写测试越界 / 主仓断言 standalone 红 / :241 口径 / v1.66.1 也无 tag / 归档门正交 warn 未预告 | TASK-013 负控 + SC-14 脚本 deliverable (qa 子 agent) + parents[4]+skip 先例; TASK-014 :241 口径 + deliverable; TASK-015 补打两 tag; TASK-016 预告 warn |
| 8 | A3-m1/A5-m1 · A3-m2/A5-m2/A1-m4 · A2-m1 · A1-m2 · A1-m8 | estimation_note 数字 (13/14 个 <4h; 008+009=9h) / agent_reason 仅 7/18 且非 SOT 字段 / `:404-408` 参考锚点 / schema 偏离声明 / TASK-005 title「调用」命中归档门集成关键词 | estimation_note 重算 (19 任务 14 个); 逐任务 `reason` 字段 (断言); 参考锚点标注; schema_note; TASK-005 title 改措辞 |

## 席位实测亮点

- A1: 依赖闭包实算 (012/014 不含 003); ls-remote 两 remote 无 v1.66.1/v1.66.4 tag; 合成全 completed 目录实跑归档门 → 正交 warn 来源定位。
- A2: `.replace` no-op 实证; detached-HEAD 先例对 checkout 验证的风险。
- A3: readiness tie-break 实算 (002 先于 004); 绑定名所在任务错位。
- A4: config-template 探针 import DEFAULT_CONFIG 实读 (010 需 003); `test_spec_complete.py:94-104` 先例。
- A5: `completed + N/A` 惯例真实出处 = `openspec/archive/2026-08-22-phase-c-integrator-ci-path-coverage/detailed-tasks.yaml` (勘正 R1 写的 #179)。

## 收敛判定

R2 REVISE (5/5, 0C) → v3 (8 簇 + 程序化断言) → R3。
