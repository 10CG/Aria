---
checkpoint: post_spec
mode: convergence
round: 1
spec_id: concurrent-session-upm-safety
agents: [tech-lead, qa-engineer, backend-architect]
converged: false
verdict: FAIL
focus: "merged (a)/(c) sister R2-CARRY re-audit; (b) convention backbone treated as converged baseline"
timestamp: "GENERATED_AT"
---

# post_spec R1 consolidated — concurrent-session-upm-safety (focused (a)/(c) re-audit)

> 合并版 Spec 的 (b) convention 骨架已 2-round CONVERGED, 本轮只审 sister (a)/(c) 吸收后开放项。
> 全部断言经 3 agent 对真代码核验。

## Verdicts
| agent | verdict | Critical | Important |
|-------|---------|----------|-----------|
| tech-lead | PASS_WITH_WARNINGS | 0 | 5 |
| qa-engineer | NEEDS_FIX | 2 | 5 |
| backend-architect | PASS_WITH_WARNINGS | 0 | 3 |

**Aggregate**: FAIL (qa 2 Critical 在 highest-severity 聚合下成立) → converged=false → 需 Rev1 后 R2。
**实质共识**: 设计/scope/哲学/因果框架全部成立, 无架构级 Critical。全部 finding = 文档准确性 + fixture 缺口 (实施前必修, 非设计缺陷)。

## TASK 0.4 裁定 (本轮核心问题)
**不拆独立 prereq Spec** (tech-lead 明确 NO; backend-architect 支持"按风险评估"但同意无独立用户价值)。
理由: collision 持久化无独立用户价值, 纯属切口1/2 内部前置; 但**远超"抽函数"** —— 真实管线是
`tracks[] → _track_to_claim_record(lossy, 可 raise) → reconcile_all → _classify_collision`, 涉及 lib/reconcile.py 依赖。
**正确做法**: 本 Spec 内把 TASK-000 拆 (0a) collector 内联 approximation+reconcile 管线产 collision 字段 / (0b) renderer 改读 + meta-fix; 并标注该字段 advisory-only。

## Critical (聚合, 须 Rev1)
- **C1 — tasks.md 0.1 / proposal §What 工作项0 输入类型错配**: 描述 `classify(tracks)` 输入 `tracks[]`, 但真 `_classify_collision(claims: list[ClaimRecord])` (track_board.py:331). 真实需经 `_track_to_claim_record` 5 段管线。3 agent 一致发现 (qa 评 Critical / tech-lead I3 / backend IMP-1)。proposal 与 tasks 自相矛盾 (0.1 说抽函数, 0.4 说远超抽函数)。
- **C2 — layer-l-integration.md:23,69 phantom field 仍在** (`collision_type` / `has_collision`, 从未实现)。tasks.md 0.3 已排 meta-fix, 但 qa 主张**前置到 Phase 0 最先执行**, 防 AI 读旧文档继续传播 phantom。

## Important (Rev1 一并修)
- **I1 — default-branch citation 错 (phantom-reuse)**: proposal:56/tasks 5.1 cite "sync.py:36-41 symbolic-ref chain", 但全 state-scanner **0 处 symbolic-ref**; sync.py:37-41 只是 `_ORIGIN_HEAD_REFS` 常量列表, 非可调 resolver。Phase B 须自写 `git symbolic-ref refs/remotes/origin/HEAD` + fallback。
- **I2 — ahead/behind citation off-by-target**: cite "git.py:167", 真实在 git.py:147 / sync.py:146 (`rev-list --left-right --count`), 且锁死 `@{upstream}`, 切口1 需 `<old>..origin/<def>` → 复用 pattern 非调函数。
- **I3 — collision.groups 结构未定义**: proposal 写 `{kind, groups}`, 真 `_classify_collision` 返回 `(kind, emoji)` 无 groups。新 helper 返回结构 + groups 形状 (list[str]? list[dict]?) 须在 tasks 精确定义, 否则 fixture 无法断言。emoji 是 render-only, 持久化须丢弃。
- **I4 — upm.source_file null-guard 缺失**: source_file 可为 None (upm.py:326, 无 UPM 项目, Aria 自身即是)。AC-1 未要求 source_file==null fixture; self-thrash dogfood 会直接撞此 null path。
- **I5 — lossy approximation advisory-only 约束未写明**: `_track_to_claim_record` 是 visual-only lossy 近似。若持久化的 collision 当切口1 强提示触发器, 等于把近似升级为半决策输入。须显式声明持久化 collision = advisory, 不作 gating 输入。
- **I6 — disjointness 第三态 fixture 缺**: `enabled==true + collision!=none` 时切口2 不触发 (phase1_gate 处理) 的反向断言无 fixture (qa I5)。
- **I7 — credential 不泄漏无自动化验证手段**: AC-1 要求 fetch 失败"不回显 raw stderr", 但无构造含敏感 stderr 的 fixture + 断言方法 → 只能靠 code review (qa 缺口2)。
- **I8 — config `coordination.enabled` 读取插入点未定** (qa I1) + **切口1 在 phase-d-closer execution-steps.md 无插入点定义** (qa I2)。

## Minor
- M1 error_kind enum 真实 4-5 值 (network/auth_403/non_ff/git_missing[/other]), sister 报告计数失真, 不影响本 Spec。
- M2 TASK-006 对 TASK-000 hard dep 偏紧 (collision 依赖是可选 OR 分支)。
- M3 `classify(tracks)` 须显式排除 (owner,container) 同时相同的 self-serial。

## R2-CARRY 6 项处置核查 (tech-lead)
| # | 项 | 处置 |
|---|----|------|
| 1 | 拆子 Spec 评估 | ✅ 吸收 (TASK 0.4 转 Phase B → 本轮裁定不拆) |
| 2 | 修 collision 迁移描述 | ⚠️ 部分 (C1 仍错配) |
| 3 | 删 phase1_gate 共享字段说法 | ✅ 吸收 (改 enabled 互斥) |
| 4 | 修 3 citation | ❌ 未修 (I1/I2) |
| 5 | qa null-guard + 中间态 smoke | ❌ 未吸收 (I4/I6) |
| 6 | AC-4 enabled==true 侧 fixture 归属 | ⚠️ 部分 (I6) |

## 下一步
Rev1 (修 C1/C2 + I1-I8, 均为 proposal/tasks 文档订正 + 1 处 meta-fix 前置) → R2 验证收敛 → Draft→Approved → Phase A.3 → Phase B。
