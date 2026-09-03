# PREDICTION — Rule #6 AB `audit-engine` (Spec sibling-spec-probe TASK-017), 写于四臂派出后、任何结果回收前 (memory `predict-then-measure`)

- 套件: `ab-suite/audit-engine.json` v1.3.0 (eval 1 α / eval 2 β, descriptive), 各 4 条 expectations
- 臂: `with_skill` = aria `feature/sibling-spec-probe` 工作树 `skills/audit-engine/` (TASK-015/016 落地后) ; `old_skill` = aria master `4c6489c` 的 `skills/audit-engine/` 快照 (`ab-workspace/…/skill-snapshot`, 无探针小节, SC-17 计数 0)
- 已知污染面: 两臂 subagent 都会被自动注入主仓 CLAUDE.md (不含探针); eval prompt 本身给出了「每轮入口的竞品 spec 探针」名称与 stdout JSON (夹具必需) ⇒ old_skill 臂**知道有个探针**, 区分度只能来自「怎么调用 / 怎么措辞 / 放哪一步」

| eval | expectation | with_skill 预测 | old_skill 预测 | 依据 |
|---|---|---|---|---|
| 1 | 1 完整命令行 (`--own-spec-dir`/`--repo-path`) | PASS | **FAIL** | 命令行只在新 SKILL.md/execution-modes.md; old 无从得知路径与参数 |
| 1 | 2 🔴 + 「已完成的 Spec」标注 | PASS | **FAIL** | 逐字措辞只在新 SKILL.md/report-format.md; old 可能写「archive 下」但不写该四字 |
| 1 | 3 不阻断 / 不改 verdict / 不改路由 | PASS | PASS | 通用审计常识 + prompt 语境, old 大概率也答对 |
| 1 | 4 不放进 Step 0, 作每轮入口 | PASS | PASS (50/50) | old 的 SKILL.md 有 Step 0「Round 1 前一次性」; prompt 说的是 Round 2 入口 ⇒ 大概率不会塞进 Step 0 |
| 2 | 1 情形 A 「未能核实」逐字 + 原因 | PASS | **FAIL** (50/50) | 逐字四字只在新指令面; old 可能写「无法核实」/「未能确认」 |
| 2 | 2 情形 B 同样「未能核实」 | PASS | **FAIL** (50/50) | 同上 |
| 2 | 3 不阻断 / 不改 verdict | PASS | PASS | 通用 |
| 2 | 4 不能断言没有竞品 | PASS | PASS | 零证据不当正证据是模型常识 |

- 预测 pass_rate: with_skill 8/8 = 1.00; old_skill 4/8 = 0.50; delta +0.50 (若 old 在 eval 2 逐字碰巧写出「未能核实」, 则 6/8, delta +0.25)
- 预测 WITHOUT_BETTER: 0
- 形态核对: 两臂均 descriptive; 任一臂实跑 git/探针 ⇒ 该 eval 不计入 delta
- 若 delta ≤ 0 或 with_skill 任一 FAIL: 不改 expectations 迁就, 原样上呈 (TASK-017 verification / Rule #10)
