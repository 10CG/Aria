---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T21:40:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 2
minor_count: 2
---

## 摘要

R2 复核范围: proposal.md 全文 (SOT, 未变) + detailed-tasks.yaml v2 全文 (18 任务); 对 aria@9e6a17c 做了 3 处实读抽样核对行号 (`aether.py:225-226` / `pre_merge_gate.py` compute_verdict 插入点 :217-219 一线之间 / `:302` `_verify_main_branch_exists` def + `:449` 调用点 / test 文件 `:363` `test_empty_runs_pending` / mixin `:85-89`) —— 均与 proposal 行号引用逐字一致, 基线复核 (400f0bc..9e6a17c 触点 diff 为空) 成立, 无新鲜代码漂移。

**R1 归我席的三簇 (聚合簇 #8 / #1 参与 / #11 参与) 全部核验落地**: SC-3 末句跨路径断言已落 TASK-005 (carries_sc 显式标注 + deliverables 点名 "A3-M1")、SC-11(d) reset 成功路径已逐字补进 TASK-008 title、INV-5 grep 已补进 TASK-011 verification 且与 TASK-010 对称; `skipped`→`completed(N/A)` + `readiness_rule` 的改动直接解决了我 R1-m1 关注的「条件跳过后下游依赖解析语义」空白。

但 R2 通读发现 **2 处新的 Major**: (1) TASK-004 的**结构性排序信号全部未跟随** disposition #4「exec_order 前移到 2 之前」的承诺实际改动 —— exec_order 字段仍为 4 (晚于 TASK-002=2/TASK-003=3)、物理文件位置仍在 TASK-002/003 之后、P-group 仍标 P2 (晚于 P1), 只有 execution_order 散文段/parallel_tracks 列表/TASK-004 自身 notes 三处口头声明「先做」, 四个结构信号里三个仍指向错误方向, 复现的正是该守卫本要防止的「落在被守护变更之后 ⇒ 自证快照」缺陷形状。(2) SC-15 的绑定名约定 (R1 A3-m2 处置) 把具体测试名 `NotFoundVerdictTests.test_trigger_matched_message` 写进了**下游消费任务** TASK-012 (exec_order 13) 的 notes, 但真正**产出**该测试的 TASK-002 (exec_order 2) 的 title 明确要求「6 档+None **参数化**」(单一 parametrize 方法, 而非按 case 分立命名的方法) —— 绑定名约定没有回写进产出方, 到 TASK-012 执行时该名字大概率不存在 (parametrize 产生的是 `test_xxx[workflow-trigger-matched]` 形态的 node id, 不是裸方法名), 复现的是 R1 原始那条「跨任务耦合未落显式约定」, 只是把地址错误地钉在了消费端而非产出端。

另有 2 处 Minor (数值/覆盖度): estimation_note 声称「10 个 <4h 任务」但实数 13; agent_reason 承诺「逐任务」但仅 18 个任务中 7 个实际带有该字段。

## R1 处置核对

| 归我席簇 | R1 内容 | v2 处置 | R2 核验 |
|---|---|---|---|
| #8 (A3-M1) | SC-3 末句跨路径一致断言未落任何 task | TASK-005 加用例 | **已落**: carries_sc 含 "SC-3 末句 (gate_check 路径回显 == compute_verdict 路径) RED"; deliverables 点名 "SC-3 跨路径一致性用例 — A3-M1"; sc_coverage_crosscheck.SC-3 含 "TASK-005 (末句跨路径一致)" |
| #8 (A3-M2) | SC-11(d) reset 成功路径未列 TASK-008 | TASK-008 加两条 | **已落**: title 逐字含 "reset --observations 成功路径 obs=0 其余键逐字不变 / reset --retry-count 成功路径 retry_count=0 + started_at 更新 + 其余不变" |
| #8 (A3-M3) | INV-5 只复制到 TASK-010, 未复制到 TASK-011 | TASK-011 加 grep | **已落**: TASK-011.verification 含 "INV-5 grep: 本任务产出文本零处出现「自动 dispatch / 自动推 commit」类指令 (A3-M3)", 与 TASK-010 对称 |
| #1 (A3-m1 参与) | TASK-007 conditional_on=skipped 时下游依赖解析语义未声明 | 禁用 skipped; readiness_rule 写进 metadata | **已落**: `readiness_rule: "dependencies 就绪 = 依赖任务 status ∈ {done, completed} (含「completed + notes: N/A」的条件跳过)"` 直接消解原顾虑; TASK-007a/007b conditional_on 明确 false 分支为 `status: completed` 非 `skipped` |
| #11 (A3-m2 参与) | SC-15 绑定名约定未落显式约定 | 绑定名 `NotFoundVerdictTests.test_trigger_matched_message` | **部分落, 新问题**: 名字写进了 TASK-012 (消费方) 而非 TASK-002 (产出方), 见下方 [A3-qa-engineer-PP2-M2] |

## Findings

### [A3-qa-engineer-PP2-M1] TASK-004 前移的执行承诺未落实到机检字段, 结构信号 3/4 仍指向旧序

- **scope**: TASK-004 (`exec_order`, 物理位置, `parent`) vs 处置表 #4 / execution_order / parallel_tracks / TASK-004.notes
- **问题**: R1 聚合处置表第 4 行明确承诺「exec_order 前移到 2 之前 (gate 轨首位)」, 用以修复「守卫 TASK-004 依赖 TASK-003 (落在被守护变更之后 ⇒ 自证快照)」。v2 实际只改了 `dependencies: [TASK-000]` (从依赖 TASK-003 改为依赖 TASK-000), 但四个可判定「执行顺序」的结构信号中三个仍未跟随:
  1. **exec_order 数值**: TASK-004=4, 晚于 TASK-002=2、TASK-003=3 (未前移, 承诺落空)。
  2. **物理文件位置**: yaml 内 TASK-004 仍物理排在 TASK-002/TASK-003 **之后** (`# ══ P1 backend + verdict ══` 段落含 002/003, 其后才是 `# ══ P2 gate_check 早退 + 回填 ══` 段含 004)。
  3. **parent P-group**: TASK-004.parent="P2", 晚于 TASK-002/003 的 "P1"; metadata.parent_task_count 注释行序 "P0/P1/P2/…" 本身也暗示 P1 先于 P2。
  4. 只有 `execution_order` 顶层散文段落 (`"gate 轨: TASK-004 (守卫@基线) → TASK-002 (RED) → TASK-003 (GREEN...)"`) 与 `parallel_tracks.tracks[0].tasks` 列表 (`[TASK-004, TASK-002, TASK-003, ...]`) 以及 TASK-004 自身 `notes` (「守卫必须先于 TASK-003/006 落」) 三处**散文**正确声明了顺序。

  `exec_order_note` 把 `exec_order` 定义为「拓扑序的 advisory tie-break」——用于在多个已就绪任务间排优先级。TASK-002/TASK-004 都只依赖 TASK-000, 二者在 TASK-000 完成后**同时就绪**; 此时唯一的机读排序信号就是 exec_order, 而它现在把 TASK-002 排在 TASK-004 之前。若实施者 (或另一个不通读 execution_order 散文段的 subagent) 按「就绪任务里 exec_order 小的先做」这条本文件自己定义的 tie-break 规则调度, 会先做 TASK-002 (RED) 甚至 TASK-003 (GREEN, 代码已改), 再回头做 TASK-004 —— 这正是 A1-M4 想防止的「守卫落在被守护变更之后, 退化为自证快照 (跑守卫时被测代码已经变了)」。

- **实测**: 逐字比对 yaml 中 TASK-004 的 `exec_order: 4` 字段值、其在文件中的物理行位置 (紧跟 TASK-003 之后)、`parent: "P2"` 字段, 与 `execution_order`/`parallel_tracks` 两个独立顶层字段的散文声明进行交叉核对, 确认三个机检字段未变而两个散文字段已改 —— 这是「新增文本 (散文修复) 掩盖了未落实的机检字段修复」的具体案例, 与本轮任务点名的「TASK-004 前移后 GUARD 语义可执行」直接相关: 语义本身 (基线 9e6a17c 绿 + mutation 红) 已正确编码在 verification 里, 但「前移」这个排序修复本身未被编码进任何机检字段。
- **建议**: 把 TASK-004 的 `exec_order` 改为小于 2 的值 (如 1.5, 或整体重排为 1/2/3/4...并把 TASK-001 之后紧跟 TASK-004), 并将其物理移到 TASK-002 之前、`parent` 改为与其执行位置一致的分组 (或至少在 parent 命名上不再暗示「P1 先于 P2」)。若保留现有 P-group 语义 (P 代表关注域而非时序), 建议在 `parent_task_count` 注释或 `exec_order_note` 里显式声明「exec_order 与 parent 编号在本文件中不同源, 不可假设后者隐含前者」, 消除歧义。

### [A3-qa-engineer-PP2-M2] SC-15 绑定名约定钉在消费任务而非产出任务, 与产出任务的「参数化」设计冲突

- **scope**: TASK-012.notes (`test_case_in_unit_tests 绑定名约定`) vs TASK-002.title (「6 档+None **参数化**」)
- **问题**: R1 A3-m2 (簇 #11) 指出 SC-15 要求 `NEG-4-no-run-for-branch.json` 的 `test_case_in_unit_tests` 字段绑定「SC-2 的 trigger-matched 用例」, 但产出该用例的 TASK-002 没有要求「该用例需具名/稳定可引用」。v2 处置 (聚合报告第 11 行) 给出具体绑定名 `NotFoundVerdictTests.test_trigger_matched_message`, 但落点是 **TASK-012** (Rule #6 任务, exec_order 13) 的 `notes`, 而不是 **TASK-002** (真正编写该测试的任务, exec_order 2) 的 title/deliverables/verification。TASK-002.title 逐字要求「compute_verdict not_found 6 档+None **参数化**」—— proposal SC-2 原文本身也用「参数化」措辞。标准 `pytest.mark.parametrize` 对 6+1 个 reason 档产出的是**单一测试方法**, 其 node id 形如 `NotFoundVerdictTests::test_xxx[workflow-trigger-matched]` (方括号 id), 而不是一个字面命名为 `test_trigger_matched_message` 的独立方法。TASK-002 的 title/deliverables/verification 三处均未提及需要为 trigger-matched 档单独命名一个可稳定引用的方法或 parametrize id, 也未要求「显式 `ids=[...]`」(这正是我在 R1 m2 里给出的具体建议, 未被采纳到 TASK-002 里)。
- **实测**: 逐字核对 TASK-002 全字段 (title/deliverables/verification/notes) 无一处出现 "trigger_matched_message" / "ids=" / "可引用" 等字样; 而 TASK-012.notes 逐字写死了这个方法名, 且 TASK-012.verification 依赖它 ("回退本 spec 代码 (git stash) 后 test_case_in_unit_tests 指向的测试转红" —— 若该名字不存在, 此验收步骤在 exec_order=13 时才会发现「指向的测试压根不存在」, 造成 11 个任务之后的返工)。
- **建议**: 把绑定名要求**回写进 TASK-002** 的 deliverables (如: 「trigger-matched 档必须可被稳定引用 —— 或拆一个独立方法 `test_trigger_matched_message`, 或对 parametrize 显式传 `ids=[...]` 并在 TASK-012 按 node id (含方括号) 引用, 与 TASK-012 约定的绑定名二选一钉死」), 使产出方在编写时就知道下游有一个精确到方法/id 级别的引用契约, 而不是只在消费方留一句事后才会撞见的假设。

## 已核验无误

- SC-3 末句 / SC-11(d) 两条 reset 成功路径 / INV-5 (TASK-011) 三处 R1 Major 逐字核验已落, 表述与 proposal 原文 (SC-3 末句、SC-11(d)、INV-5 rule) 一致, 无二次漂移。
- `sc_coverage_crosscheck` 与 `checklist_s7_mapping` 随 TASK-007a/007b 拆分同步更新, 全部引用写作 "TASK-007a/007b (条件)" 形态, 无残留对已废弃单一 "TASK-007" 的引用; checklist_s7_mapping 4 项逐一在对应任务 (TASK-007b/TASK-012/TASK-014/TASK-008) 落点核实存在。
- INV-3 条件 scope 四落点 (TASK-007a/007b.conditional_on, TASK-006/011/015.conditional_parts) 与 rule 原文逐字对应, 且 TASK-006/011/015 均正确加了到 TASK-001 的依赖边, 可在执行时读到 `metadata.dispatch_viable`。
- `skipped`→`status: completed` + `notes: 'N/A — ...'` 的改法配合新 `readiness_rule` 字段, 完整消解了我 R1-m1 提出的「下游依赖一个条件跳过任务时算不算就绪」的语义空白 (readiness_rule 明确 completed 视为就绪)。
- TASK-002 deliverables 补充说明 "test_ci_backends.py 不动", 消解了 A4-m5 提出的歧义。
- TASK-011.dependencies 已补 TASK-010; SC-14 机检脚本已落 `tests/test_doc_sync_no_run.py`; `dispatchable_workflows` 字段文档已落 TASK-011.conditional_parts。
- 代码行号抽样核对 (aether.py:225-226 / pre_merge_gate.py compute_verdict 插入点 / `:302` `_verify_main_branch_exists` / `:449` 调用点 / test `:363` / mixin `:85-89`) 在 aria@9e6a17c 上逐字成立, 与 proposal 引用一致, 无新鲜代码漂移。
- `metadata.estimated_hours: 49` 经逐任务求和复核 (0.5+1.5+3+4+2+3+3+2+2+4+5+3+4+4+1+3+2+2) 精确等于 49, 无算术错误。
- traps §六 三写者顺序 (TASK-001 建节 → TASK-011 中段插入 → TASK-014 末尾追加 + 终改 `:241`) 三处描述互相一致, 无重复建节或错序。

## Verdict

PASS_WITH_WARNINGS — vote: REVISE

无 Critical。R1 归我席的三簇 (SC-3/SC-11(d)/INV-5) 均已忠实落地, 但本轮通读发现 2 处新 Major: (1) TASK-004「前移」承诺在机检字段 (exec_order/物理位置/parent) 层面未真正执行, 三个结构信号仍与两个散文声明矛盾, 有复现原缺陷的风险; (2) SC-15 绑定名约定钉在消费方而非产出方, 与产出方的参数化设计存在结构性不匹配, 可能导致该名字到 TASK-012 执行时并不存在。均为可在 B.1 前用几行文本修复的收敛期缺陷, 不建议现在放行进 B.1。
