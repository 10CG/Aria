---
agent: code-reviewer
round: R1
verdict: REVISE
scope_check: SCOPE_OK
critical_count: 0
major_count: 2
minor_count: 4
---

# post_spec 审计 R1 — code-reviewer

核实通过 (实码/实跑): pre_merge_gate.py:187 / aether.py:223-224 / base.py Literal (not_applicable 从不来自 backend, D1 成立) / 测试基线 62 (25+37, 无 exact-dict 断言, additive 新键可共存) / 评估点与 gate_check 控制流自洽 / 语料表 4 行中 3 行吻合 / 授权链 _lane :101 逐点吻合 / SKILL.md :291 race / :218 SilkNode / :248 wait_recoverable / stdlib 先例实存 / plugin.json 1.64.1 / #122 open / Rule #6 定性正确 (决策表第二行)。

## Major

**CR-1 — 语料表 build-aria-runner 行事实错误, D7 证据错引**
实读: on: 含 workflow_dispatch **和** push (branches: [feature/aria-2.0-m0-prerequisite], paths: ['aria-orchestrator/docker/aria-runner/**'])。非 dispatch-only。D7 实证只剩 tripwire; 照错表建 fixture = 假绿前提。
修法: 表改「dispatch + push(branches+paths)」; D7 只引 tripwire; build-aria-runner 纳为「混合触发 (仅自动触发臂参与判定)」第三形态语料。

**CR-2 — D2 文字与 §1 返回契约 / SC-7 / SC-8 直接矛盾 (covered vs unknown 归属)**
D2 说「解析失败/git 失败→covered」, §1/SC-7/SC-8 说 → unknown。gate 行为等价但 decision 字面只能取一。实现者照 D2 写则 SC-7/8 红; 照 SC 写则 D2 空话。
修法: D2 改写 —「fail-toward-covered 指行为退回现状; decision 值分档: per-workflow 级不确定 → 该 workflow 记 covered; 全局级失败 (文件不可解析/git 失败) → 整体 unknown; 两档 gate 行为均=现状」。

## Minor

**CR-3 — 「§C.2.4 五处同步」计数与 §5 六项不自洽**; SKILL.md 真实结构顶层 4 块 (verdict/路由是执行流程内步骤 5/6)。统一计数口径; 「verdict 计算表」改「verdict 计算 (bullet list)」。

**CR-4 — rule6_note「ab-suite 5 evals」与套件现状不符**: phase-c-integrator.json v1.1.0 source_evals_count=5, selected_count=3, 实际 3 条; 另有 phase-c-integrator-pre-merge-gate.json (6 fixtures)。改「3 selected (source 5)」+ 明确 fixture 套件是否入执行面。

**CR-5 — 「covered 路径逐字段不变」与「path_coverage 键恒在」字面冲突**: 统一为「既有字段逐字段不变 + additive 新键」; SC-11 注明断言口径=既有字段; 顺带承认 covered 路径新增 1 次 git diff subprocess + IO 的行为面增量。

**CR-6 — SKILL.md :262 schema 枚举与 CIStatus Literal 预存漂移 (缺 not_found)**: 非本 spec 引入, 但 §5 改写同一行时应一并处置 (入 enum 或注明来源层)。

## 结论

指涉密度高且绝大多数实码核验准确, 机制设计无结构性问题。CR-1 (语料一格事实错且被 D7 引为实证) 与 CR-2 (总原则与 SC 打架) 都会直接进 fixture 与实现: **REVISE**, 按修法改后 R2 可过。
