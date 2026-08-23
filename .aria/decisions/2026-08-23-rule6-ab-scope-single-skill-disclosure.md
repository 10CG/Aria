# 决策: linked-issue-normalization 的 Rule #6 AB 门范围 = 单 Skill 全套件 + 定向 fixture (披露: 未跑 Tier 1 全量)

- **日期**: 2026-08-23 | **裁定人**: owner (AskUserQuestion 四选一) | **执行容器**: bfe8285d
- **Spec**: `openspec/changes/linked-issue-normalization` TASK-027 (5.14) | **关联**: TASK-013 (4.1), aria-plugin#157, aria-standards#17

## 事实

- 本 change 对 AI 指令面的唯一改动 = `aria/skills/state-scanner/SKILL.md:176` 一个括注 (Part B1 段, `--linked-issue` 重叠告警的比较规则)。其余改动是 `lib/collision.py` / `lib/claim_schema.py` 的 Python 代码与 docstring (substitute 路径, 证据见 `.aria/repro/archive/sc-baseline-linked-issue-normalization-REPORT.md`)。
- `AB_TEST_OPERATIONS.md:397` 要求「Tier 1: 核心 Skills (10 个, 每次发版必测)」, `:545` 要求发版前「Tier 1 Skills 全量 AB 测试已执行」。
- 本次实跑: state-scanner **全套件 11 条** + **新建定向 eval-12**, 两臂 24 run (iteration-1) + 2 run (iteration-2)。结果见 `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/RESULT.md`。**未跑**其余 9 个 Tier 1 Skill。

## 裁定

单 Skill 全套件 + 定向 fixture + 本文件披露 + 开 convention issue (aria-standards#17)。**不**补跑 Tier 1 全量。

## 理由 (owner 采纳 AI 建议)

1. 其余 9 个 Skill 在本 change 里零改动面; 对它们跑 AB 测不到本 hunk (维度不匹配的投入), 且 #117/#127/#157 三条在案 issue 已证套件对局部 hunk 结构上不可见。
2. 两次先例 (v1.65.0 #122 / v1.66.0 #137) 同样只跑单 Skill, 但无披露; 本次是第三次, 按 memory `feedback_written_exception_exact_condition_match` 不披露地偏离是最坏选项 ⇒ 披露 + 立案成文。
3. ⛔ 本裁定**不是**「改动小 / 纯括注 / 性价比」降级 (Rule #10 禁止的理由): 该 hunk **照跑了** AB, 且因 iteration-1 承重断言 1 两臂皆败而改写括注重跑 (iteration-2 5/5) —— AB 真正改变了交付物。

## 留痕

- proposal.md §rule6_note 同步追加本裁定指针 (TASK-027 deliverables)。
- convention 修订归 aria-standards#17, 不在本 change 内改规范。
