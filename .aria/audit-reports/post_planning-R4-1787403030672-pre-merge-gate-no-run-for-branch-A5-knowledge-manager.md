---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: "2026-08-22T14:54:45.000Z"
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A5-knowledge-manager
critical_count: 0
major_count: 0
minor_count: 1
---

# post_planning R4 (末轮) — A5 (knowledge-manager) 审计报告

## 摘要

实读 v4 `detailed-tasks.yaml` 全文（20 任务 51h）+ proposal.md 全文（310 行，SOT 未变，§3.5/§4/§7/Impact/Risks 逐段核对）+ R3 五席单席报告（A1~A5 全部 finding 标题）+ R3 聚合报告（6 簇处置表）。对本轮任务清单（TASK-016 §3.5 全清单 / 撤 warn 预告措辞 / schema_note / INV-6 例外 / 可追溯 / v4 diff 新矛盾）逐项做了**独立程序化核验**（非目测）：

- 用真实 `9e6a17c` worktree 实测负控 pattern `DISPATCH_VIABLE|dispatchable_workflows|/dispatches -d`（限 6 个子目录，`references/` 豁免）—— **0 命中**，且 `pre_merge_gate.py` 中 `<pr_branch>` 同样 0 命中，与 v4 `INV-3.encoded_as` 的断言完全吻合。
- 程序化重跑 exec_order 单调性（20 任务全边）、TASK-003/TASK-010a 下游闭包、`agent_summary` 双向一致、`reason` 覆盖率（20/20）、`estimated_hours` 求和（51=51）、`<4h` 计数（15/20，与 `estimation_note` 四组配对小计逐一吻合）—— 全部通过，**除一处**（见 Findings）。
- 逐字核对 proposal §3.5 原文 9 项清单与 `TASK-016.conditional_parts` v4 新文本，确认第 9 项（`§2.1 <pr_branch> .replace`）已补入，且额外覆盖了 Impact/L31/R-c 四处衍生提及（超出 R3 处置表摘要的「四处提及」字面数，但方向一致，属加固而非矛盾）。
- 逐字核对 `TASK-016.verification` 撤预告新文案「按其文案处置并留痕，不预先豁免」，未见其与 Rule #10（不得自行豁免已启用闸门）冲突——新文案没有替 AI 预判"这条 warn 不算数"，而是把处置权交还给「warn 若出现时」的当下裁决，方向正确。
- 逐字核对 `schema_note` 新文本「estimated_hours 用数值 (int 或 .5, 无 validator)」，与实际 20 个 `estimated_hours` 值集合（{0.5, 1, 1.5, 2, 3, 4, 5}，非整数均为 X.5 形）精确吻合，不再自相矛盾。
- 逐字核对 `INV-6.rule` 新增的「唯一例外」子句，与 `checklist_s7_mapping[1]`/`TASK-007b.conditional_on`/`INV-3` 三处对 checklist-1 的处置逻辑一致（false 时 TASK-007b 整体 `completed(N/A)`，checklist-1 随之 N/A，非蒸发）。
- 可追溯性抽检：yaml 内全部 14 处 R1-R3 post_planning 引用（`R2 A4-M1`/`R2 A5-M1`/`R1 A1-M5`/`R2 A1-M2/A4-M1`/`R2 A1-m3/A4-M2`/`R2 A3-M2`/`R2 A1-m7`/`R2 A4-M2`/`R3 A1-M2/A2-M1`/`R3 A1-M3`/`R3 A3-M1`/`R3 A1-m6`/`R3 A4-m4`/`R3 A5-M1`/`R3 A1-m1/A5-m1`/`R3 A1-m2`/`R3 A4-m2`）逐条去 A1~A4 原始 R3/R2/R1 报告核实——**全部真实存在且内容方向匹配**，另有 2 处跨检查点引用（`R7 A1-m1` 指 post_spec R7、proposal.md 内 `R6 A1-M1/A4-m1` 等指 post_spec R6）确认对应报告文件确实存在，无捏造。

**v4 diff 新发现 1 条 Minor**（新鲜眼睛，v4 结构性新增 TASK-010a 后遗留的两处散文枚举未回填，与真实依赖图脱节）：v4 为响应 R3 簇 #3（SC-14 自证快照）新插入了 TASK-010a 并给它接了 `dependencies: [TASK-003, TASK-009]` 这条真实边——这条边本身完全正确，但两处此前被 A1 在 R3 明确核实为「精确吻合」的枚举式散文（`metadata.exec_order_note` 的「TASK-003 ∈ {11 项}闭包」清单、`parallel_tracks.note` 的耦合说明）都还停在 v3 的 11 项/单任务表述，没有把新成员 TASK-010a 补进去。真实闭包已变成 12 项（TASK-003→005/006/007a/007b/**010a**/010/011/012/013/014/015/016），且 `parallel_tracks.note` 只提到「TASK-010 依赖 003」，没提到 TASK-010a 同样依赖 003（且是 helper 轨里第一个要等 gate 轨的任务）。不影响实际执行（`dependencies` 字段本身完整正确，拓扑序不受影响），纯属描述性枚举滞后于结构编辑，够不上本轮 Major 门槛（不违反不变量、不掉 SC 承载、不致红绿失效、不致实施者分叉——真正驱动执行顺序的是 `dependencies` 字段，不是这两条散文），归 Minor。

三条既往归本席的 R3 结论（M1 / m1 / m2）全部 closed，证据见「R3 处置核对」。

## R3 处置核对

| R3 簇 | 内容（归本席部分） | v4 证据 | 判定 |
|---|---|---|---|
| #5（**A5-M1** + A4-m1）：TASK-016 归档自删清单漏 §3.5 第 9 项（`§2.1 <pr_branch> .replace`）| `conditional_parts` 改为 §3.5 全清单 | `TASK-016.conditional_parts`（:451）逐字含「§4 整段 / SC-8 / SC-9 dispatchable 部分 / SC-2 dispatch 子项 / SC-5 (c2) / 2.3 表 dispatch 渲染句 / 3.3 (a) 行 / **§2.1 末段 `<pr_branch>` `.replace` 三行**（标注 R3 A5-M1，§3.5 第 9 项）/ Impact 两处提及 + 两内部签名 / L31 代码落点 / R-c 提及」，proposal §3.5 原文 9 项经逐字比对全部覆盖（含此前用「Impact 两项」间接覆盖的 `DISPATCH_VIABLE` 常量本身，现额外被 `§7 checklist 1 标 N/A` 显式兜底），并扩展覆盖了 §3.5 末句「Impact/CHANGELOG 相应不提」这一此前只有笼统措辞、无具体落点的要求 | **closed**（且比 R3 处置表摘要的「四处提及」覆盖更全） |
| #6 之一（A1-m1 + **A5-m1**）：TASK-016 归档 warn「预告」与 TASK-005 改词矛盾, 且构成 Rule #10 反向（预先豁免）| 撤预告改「若出现按文案处置不预先豁免」 | `TASK-016.verification`（:458）「归档门若另产 warn（archive-safety-net 启发式等），按其文案处置并留痕，**不预先豁免**（R3 A1-m1/A5-m1: TASK-005 改词后实测该 warn 不再触发，原「预告」撤销）」。全文 grep `预告`/`archive-safety-net` 仅此一处，无残留旧措辞；新文案未预判 warn 是否出现，只规定「若出现如何处置」，符合 Rule #10「不得自行豁免」的字面要求（不是不裁决，是不预先裁决） | **closed** |
| #6 之一（A4-m3 + **A5-m2**）：`schema_note`「estimated_hours 用 int」与实际数据（0.5/0.5/1.5/49.5）矛盾 | schema_note 改「数值」| `metadata.schema_note`（:11）「estimated_hours 用数值 (int 或 .5, 无 validator)」。程序化核验 20 个 `estimated_hours` 实际取值集合 = `{0.5, 1, 1.5, 2, 3, 4, 5}`，非整数值全部形如 X.5，与新措辞精确吻合，不再有类型断言与数据的矛盾 | **closed** |

**其余三簇（本席仅一般核验，非本席主责）**：#1（负控 pattern 换基线零命中）——本轮**实地重跑** `git -C aria worktree add <tmp> 9e6a17c` 后对 6 个子目录跑新 pattern，0 命中，`<pr_branch>` 亦 0 命中，与 `INV-3.encoded_as` 声明吻合，**closed**；#2（INV-1 四合取语义谓词）——`INV-1.encoded_as` 文本内部四个 `git -C aria show` 分句自洽，`-C aria` 缺失（A2-M1）与 `grep -c` 恒真（A2-m1）两处均已消除，**closed**；#4（SC-15 `git worktree` 替代 `git stash`）——`TASK-012.verification` 已改用 `git -C aria worktree add <tmp> 9e6a17c` 起红绿窗对照，**closed**。

**汇总**: r3_closed = 6 / r3_partial = 0 / r3_not_addressed = 0（6 簇全部在 v4 落地且经证据核验；本席主责的 #5 与 #6 两条子簇尤其扎实，覆盖面超出处置表摘要的最低要求）。

## 已核验无误

- **TASK-016 §3.5 全清单可追溯性**：proposal.md `:198` 原句「若 false: §4 整段 + SC-8 + SC-9 的 dispatchable 部分 + DISPATCH_VIABLE 常量本身 + 2.3 表的 dispatch 渲染句 + SC-2 的 dispatch 子项 + SC-5 (c2) + 3.3 (a) 行 + §2.1 末段的 `<pr_branch>` `.replace`」9 项逐一在 `TASK-016.conditional_parts` 中找到对应落点（第 4 项「DISPATCH_VIABLE 常量本身」经 `§7 checklist 1 标 N/A` 与 `Impact 的 DISPATCH_VIABLE` 双重覆盖）。`TASK-015.conditional_parts`（CHANGELOG 层）与 `TASK-016.conditional_parts`（归档正文层）分工清晰，无重叠也无遗漏。
- **Rule #10 合规性抽查**：全文 grep `豁免`/`自豁`/`预先` 共 3 处（`TASK-000.notes` 的「Rule #10: 不得自豁」/ `metadata.audit_checkpoints_note` 的白名单说明 / `TASK-016.verification` 的「不预先豁免」），三处方向一致、无自相矛盾，且 `audit_checkpoints_note` 明确交代了 `mid_implementation`/`post_implementation`/`pre_merge`/`post_closure` 四个已 `off` 的检查点为何本清单不排（Rule #10 白名单第一类：config 显式 off），未见任何「本次不值得跑」式的临场自我豁免语言。
- **INV-6 例外条款一致性**：`INV-6.rule` 新句「唯一例外: checklist 1 随 TASK-007b 在 dispatch_viable=false 时整体 N/A」与 `TASK-007b.conditional_on`（false ⇒ `status: completed`）、`checklist_s7_mapping[1]`（指向 `TASK-007b.verification`）三处指称一致，无循环引用也无悬空指针。
- **schema_note 与顶层/任务级 `estimated_hours` 双向核验**：`metadata.estimated_hours: 51` 为整数，20 个任务级值中 4 个为 X.5（TASK-000/000b/001/010a），其余 16 个为整数——与新 schema_note「int 或 .5」逐字吻合，求和 51 = 51（程序化验证）。
- **可追溯性抽检（详见摘要，14 处 post_planning R1-R3 引用 + 2 处跨检查点 post_spec 引用）**：全部去源核实，无张冠李戴，无内容捏造；`R3 A4-m1` 虽未被 `TASK-016.conditional_parts` 显式点名（只点了 `R3 A5-M1`），但两条 R3 finding（A4-m1「conditional_parts 是 §3.5 真子集」/ A5-M1「漏第 9 项」）本就是同一缺口的两个角度，v4 的修复已同时回应两者，未点名 A4-m1 属引用完整性的可挑剔项而非内容错误，够不上本轮门槛。
- **v4 结构性新增（TASK-010a）对既有断言面的影响面扫描**：programmatically 复核 exec_order 唯一性（0-19 无缺重）、每任务 `exec_order` > 全部 `dependencies` 的 `exec_order`（0 违反）、`agent_summary` 与逐任务 `agent:` 字段双向集合相等（0 不一致）、`sc_coverage_crosscheck`/`checklist_s7_mapping` 随 TASK-010a 插入后的落点更新（SC-14 三个承载任务列全，含新任务）——**仅 `exec_order_note` 与 `parallel_tracks.note` 两处枚举未跟上**（见 Findings），其余全部同步正确，说明这不是系统性遗漏，只是两处独立散文的局部滞后。

## Findings

### [A5-knowledge-manager-PP4-m1] v4 新增 TASK-010a 后，`metadata.exec_order_note` 的 TASK-003 下游闭包枚举与 `parallel_tracks.note` 的耦合说明均未回填新成员，与真实依赖图脱节

- **scope**: `metadata.exec_order_note` / `parallel_tracks.note` vs `TASK-010a.dependencies`
- **问题**: v4 为响应 R3 簇 #3（SC-14 自证快照）新插入 `TASK-010a`，其 `dependencies: [TASK-003, TASK-009]` 是一条真实且正确的边——TASK-010a 的 SC-14 机检脚本需要 `DEFAULT_CONFIG` 断言绿（`TASK-003` 已落），故必须在 `TASK-003` 之后。但两处此前被 A1 在 R3「已核验无误」明确逐项核实为「11/11 为真」「精确吻合」的枚举式散文都还停留在 v3 状态，未把这个新成员补进去：
  1. `metadata.exec_order_note`（:15）字面写「TASK-003 ∈ 005/006/007a/007b/010/011/012/013/014/015/016 的依赖闭包」——仍是 v3 的 11 项枚举。本轮独立程序化重算 TASK-003 的真实下游闭包（沿 `dependencies` 边做 DFS）：`{005, 006, 007a, 007b, 010a, 010, 011, 012, 013, 014, 015, 016}`，共 **12 项**，`TASK-010a` 未被列入。该 note 自称「机检不变量 (v3 起程序化断言)」，即声明每轮都会重新程序化核验这条枚举——如同 A1 在 R3 对 v3 版本做的那样（11/11 为真）；v4 结构性新增一个真实下游成员后，这条自我声明为「程序化断言」的枚举没有同步更新。
  2. `parallel_tracks.note`（:490）「两轨**文件域** disjoint 可并行, 但**验证面**有一处耦合: TASK-010 的 config-template-key-currency 探针 import DEFAULT_CONFIG, 故 010 依赖 003 (helper 轨 008/009 可先跑, 010 须等 gate 轨的 003)」——只点名 `TASK-010` 需要等 `TASK-003`，未提及 `TASK-010a`（`helper` 轨里实际第一个需要等 gate 轨 `TASK-003` 的任务，其 `verification` 明写「DEFAULT_CONFIG 断言绿 (003 已落)」）同样存在这条耦合。
- **为什么是 Minor 而非 Major**: 真正驱动执行顺序与 TDD 红绿的是 `dependencies` 字段本身（`TASK-010a.dependencies: [TASK-003, TASK-009]` 完整且正确，程序化核验 exec_order 单调性 0 违反），这两处是**描述性**散文（面向未来审计者/人类读者的说明性 note，非任何 task 的 `verification:` 里会被实际跑起来产生 PASS/FAIL 的机检语句）。不违反任何不变量、不掉 SC 承载（`sc_coverage_crosscheck.SC-14` 已正确列入 `TASK-010a`）、不致红绿失效、不致实施者分叉——B.2 执行者只会读 `dependencies`/`exec_order` 字段决定顺序，不会去读这两条 note 反推执行序。风险仅在于：下一位需要复核「TASK-003 影响面有多大」的审计者或人类，如果直接采信这条 note 的枚举而不重新做 DFS，会漏看 TASK-010a 这一个下游成员。
- **建议**: 两处各补一处：`exec_order_note` 改为「...的依赖闭包 (**含 010a**, 共 12 项)」或直接把 `010a` 插入列表；`parallel_tracks.note` 改为「(helper 轨 008/009 可先跑, **010a 与 010 均须**等 gate 轨的 003)」。改动量各一行，无需重新设计。

## Verdict

**PASS_WITH_WARNINGS**（0 Critical / 0 Major / 1 Minor）。归本席的 R3 三条结论（M1「TASK-016 §3.5 第 9 项遗漏」/ m1「归档 warn 预告与实测矛盾」/ m2「schema_note 类型声明矛盾」）在 v4 全部 closed，且 M1 的修复覆盖面超出 R3 处置表摘要要求（额外覆盖 Impact/L31/R-c 四处衍生提及）；m1 的撤预告新文案核验符合 Rule #10「不预先豁免」的字面要求；m2 的 schema_note 新措辞与实际数据精确吻合。另核验了非本席主责的三簇（负控 pattern 基线 0 命中实测、INV-1 四合取语义谓词、SC-15 worktree 回退）与 INV-6 新例外条款，均 closed。

v4 新发现 1 条 Minor：`exec_order_note`/`parallel_tracks.note` 两处描述 TASK-003 下游闭包/耦合的散文，未随 v4 结构性新增 `TASK-010a` 同步回填（真实闭包 12 项，note 仍写 11 项/单任务耦合）——纯描述性滞后，不影响实际执行顺序或 TDD 红绿，够不上本轮 Major 门槛，可与归档收尾一并顺手改。

残余仅 1 条 Minor，符合本轮「PASS = v4 可进 B.1」判据。

**vote: PASS**
