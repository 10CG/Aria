# PREDICTION — Rule #6 AB `audit-engine` + `phase-c-integrator` (Spec pre-merge-completeness-gate-change-scope TASK-024), 写于派臂前、任何结果回收前 (memory `predict-then-measure`)

- 套件: `ab-suite/audit-engine.json` v1.1.0 (eval 1 α / eval 2 β / eval 3 TARGETED, descriptive) + `ab-suite/phase-c-integrator.json` v1.1.0 (eval 1/2/3, descriptive); 执行 = skill-creator 流程 (12 臂 subagent 各 1 run + 逐 run grader 席 + `scripts.aggregate_benchmark` 两套件各一次)
- 臂: `with_skill` = aria feature HEAD **W = `53b8e5c`** 工作树 `skills/{audit-engine,phase-c-integrator}/`; `without_skill` (**old_skill 语义**) = aria `origin/master` **A = `268da8f`** (v1.74.1) worktree 快照 `ab-workspace/2026-10-15-pre-merge-completeness-gate-rule6/skill-snapshot/`
- 关键结构事实 (5.1 实测): `completeness_gate.py` 与其指令面**不在 A 的树里** (without 臂结构上没有新规则); sibling probe 自 v1.69.0 已在 A 中 (eval 1/2 两臂都有探针, 是回归面非区分面); C.2.5 multi-remote push 自 v1.15.0 已在 A 中
- 已知污染面: 两臂 subagent 均被注入主仓 CLAUDE.md (不含本 spec 新规则名); eval 3 prompt 自带场景事实 (他 change 报告存在 / Phase A-only diff), without 臂可凭题面部分推出断言 1/3/5 的结论 —— 区分度主要来自断言 2 (末段界定理由) 与断言 4 (`completeness_gate.py` 命令行)

## audit-engine 套件预测

| eval | expectation | with_skill 预测 | without_skill 预测 | 依据 |
|---|---|---|---|---|
| 1 (探针 α) | 1 完整命令行 | PASS | PASS | 探针在两臂 (v1.69.0+), 先例 with 4/4 |
| 1 | 2 🔴 + 已完成的 Spec | PASS | PASS | 同上 |
| 1 | 3 不阻断/不改 verdict | PASS | PASS | 同上 |
| 1 | 4 每轮入口非 Step 0 | PASS | PASS | 同上 |
| 2 (探针 β) | 1 情形 A「未能核实」逐字 | PASS | PASS | canonical 措辞两臂都有 (v1.69.0 ship) |
| 2 | 2 情形 B 同样「未能核实」 | PASS | PASS | 同上 |
| 2 | 3 不阻断/不改 verdict | PASS | PASS | 同上 |
| 2 | 4 不能断言没有竞品 | PASS | PASS | 同上 |
| 3 (TARGETED) | 1 他 change 报告不计入 ⇒ missing | PASS | **FAIL (50/50)** | 规则不在 A; 但题面自述「与本次 PR 无关」, without 可能凭推理答对 |
| 3 | 2 末段形态计入 + 理由 | PASS | **FAIL** | 末段界定规则只在 W 的指令面; without 无从引用 |
| 3 | 3 not_applicable + `[INFO]` surface | PASS | **FAIL (50/50)** | 三态 not_applicable 与 [INFO] 惯例不在 A; 题面「没有任何实现代码」可部分推出 |
| 3 | 4 completeness_gate.py 命令行含四参数 | PASS | **FAIL** | 脚本不在 A 的树; without 大概率如实说无此门或自造命令 (参数名对不上) |
| 3 | 5 一对 missing 即整体 fail exit 1 | PASS | **FAIL (50/50)** | 题面可推出 missing ⇒ fail, 但「三对全非 missing 才 pass + 拒绝放行」的机制表述只在 W |

- audit-engine 预测 pass_rate: with 13/13 = **1.00**; without = 8 + (0~2) / 13 = **0.62 – 0.77**; delta ≈ **+0.23 ~ +0.38** (> 0)
- eval 3 定向判据预测: without (0.0-0.4) **<** with (1.0) ✓
- 注: 本 delta 远小于 2026-09-03 的 +0.62 —— eval 1/2 探针自 v1.69.0 起 two-arm 都有, 已从区分面转为回归面; 本套件的区分度集中在 eval 3

## phase-c-integrator 套件预测 (回归面, 预期 delta ≈ 0)

| eval | with 预测 | without 预测 | 依据 |
|---|---|---|---|
| 1 commit-generation (3 exp) | 3/3 | 3/3 | conventional commits 两臂同源 (v1.x 早期), 本 spec 未触 |
| 2 merge-conflict-handling (3 exp) | 3/3 | 3/3 | 同上 |
| 3 multi-remote-merge-push (9 exp) | 8-9/9 | 8-9/9 | C.2.5 自 v1.15.0 两臂都有; 本 spec 仅在同文件追加 pre_merge 完整性门相关行 (:57/:754 同形改写 + 步骤 5), 不触 C.2.5 |

- phase-c 预测 delta ≈ **0** (按 rule6_note: 该套件只判回归不看 delta, 预期约 0, 如实登记不作阻断)
- WITHOUT_BETTER 预测: **0** (无 without 优于 with 的 eval; 1/2 预测持平)

## 形态与作废判据 (预登记)

- 两臂均 descriptive + 逐字附 git/forgejo 禁令; 任一臂 transcript 出现实跑 git 写命令或 fetch ⇒ 该 run 作废不计入 (场景 1 形态核对)
- transcript 核 `push_skipped` (场景 1 第 2 步): 本两套件不在 phase1_gate/release_gate 触达清单, 预期零命中; 若出现 gate 调用且 `push_skipped != true` ⇒ run 作废并 ls-remote 核远端
- 若 delta ≤ 0 或 eval 3 定向判据不成立: 不改 expectations 迁就, 原样上呈 owner (owner_gates 第 5 项)
