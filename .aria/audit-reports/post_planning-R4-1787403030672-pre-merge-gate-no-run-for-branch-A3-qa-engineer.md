---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-23T00:15:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 1
minor_count: 1
---

## 摘要

R4 (post_planning max_rounds 末轮) 复核范围: v4 `detailed-tasks.yaml` 全文 (20 任务, 51h) 对我 R3 归属簇 (A3-PP3-M1, TASK-013 的 SC-14 agent 归属分叉) 的处置核验, 加对 v4 diff (新增 TASK-010a + SC-15 worktree 回退) 的新鲜眼睛复核。核验方法以实读 aria @ 9e6a17c 源码/文档字节 + 程序化断言 (python 解析 yaml 图) 为主, 不采信散文自述。

**我 R3 归属簇 (A3-PP3-M1) 已彻底闭合**: v3 中 TASK-013 (agent: main-loop) 内隐式转派 qa 子 agent 写 SC-14 脚本的分叉, v4 采纳了我建议的方案 (a) ——新增独立的 **TASK-010a** (`agent: qa-engineer`, exec_order 12, 依赖 TASK-003/TASK-009, 早于 TASK-010/011), 承载 `test_doc_sync_no_run.py` 全部 5 条 RED 断言; `agent_summary.qa-engineer` 已把 TASK-010a 计入; TASK-013 的 deliverables/reason 已不再提及脚本或「qa 子 agent」字样。实读确认: TASK-010a 的 deliverable 路径 `aria/skills/phase-c-integrator/tests/test_doc_sync_no_run.py` 精确命中 `AGENT_MAPPING.md` §qa-engineer 的 `**/tests/**/*.py` 规则, 无残留歧义。

**新发现 1 处 Major + 1 处 Minor**（均为 v4 diff 新引入, 非 R1-R3 遗留延续）:

1. **[Major]** SC-15 的 worktree 红窗核验 (TASK-012, R3 A1-M3(b) 的修复) 用 `git -C aria worktree add <tmp> 9e6a17c` 替换了失效的 `git stash` 方案, 但按字面指令执行时, 该 worktree 里的 `test_pre_merge_gate.py` **是 9e6a17c 时的旧版本**, 根本不含 TASK-002 新加的 `NotFoundVerdictTests.test_sc2_trigger_matched_message` —— 这与「先在被测代码上跑新测试再判断红绿」的本意相反, 会导致检验退化为对任何实现质量都恒真的「找不到测试」而非真实回归证明。详见 Findings M1。
2. **[Minor]** `metadata.exec_order_note` 里 TASK-003 下游闭包的手写枚举清单 (`005/006/007a/007b/010/011/012/013/014/015/016`, 11 项) 在 v4 插入 TASK-010a 后未同步更新——程序化重算得到的真实闭包是 12 项 (多了 TASK-010a, 它确实依赖 TASK-003)。不影响真实调度 (`dependencies` 字段本身正确), 纯文本备注漂移。

## R3 处置核对

| 归我席簇 | R3 内容 (A3-PP3-M1) | v4 处置 | R4 核验 |
|---|---|---|---|
| A3-PP3-M1 (与 R3 聚合簇 #3 = A1-M3(a)+A3-M1+A1-m3 合并处置) | TASK-013 (`agent: main-loop`) 内隐式转派 qa 子 agent 写 SC-14 脚本, `agent_summary` 未纳入, `AGENT_MAPPING.md` 无「任务内子分派」先例 | 新增独立 TASK-010a (`agent: qa-engineer`, exec_order 12, deps [TASK-003, TASK-009]), 承载全部 5 条 SC-14 RED 断言; TASK-013 deliverables/reason 已清空脚本相关文字; `agent_summary.qa-engineer` 含 TASK-010a; total_tasks 19→20 | **已落**: (1) 实读 TASK-013 全字段, 无「qa 子 agent」/`test_doc_sync_no_run.py` 残留; (2) 程序化核对 `agent_summary` 20/20 任务双向一致 (脚本核验, 零 mismatch); (3) TASK-010a 路径命中 `AGENT_MAPPING.md` `**/tests/**/*.py`; (4) TASK-010a 是 TASK-010 与 TASK-011 依赖图的直接前驱, INV-2 (dependencies 编码测试→实现配对) 正确落地 |

**结论**: r3_closed=1 (我唯一的 R3 finding 完全闭合), r3_partial=0, r3_not_addressed=0。

## Findings

### [A3-qa-engineer-PP4-M1] SC-15 worktree 红窗 (TASK-012) 按字面指令跑会「找不到测试」而非「测试失败」, 检验对任何实现质量恒真

- **scope**: TASK-012.verification[0] (SC-15 红窗) + INV-7 (`NEG-4 必须真跑一次`) + proposal SC-15「回退本 spec 后 `test_case_in_unit_tests` 指向的测试转红」
- **实测链**:
  1. TASK-012 verification 原文: `"红窗 (R3 A1-M3: 主仓 git stash 对子模块 no-op): git -C aria worktree add <tmp> 9e6a17c 在基线工作树跑 test_case_in_unit_tests 指向的测试 → 红 (收集错误或断言失败); 当前树 → 绿; 用后 worktree remove"`。
  2. `test_case_in_unit_tests` 字段格式已由既有 catalog 确认 (`aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json:22` 等) 为 `<module>.<ClassName>.<method>` dotted 引用, TASK-012.notes 钉定 NEG-4 的值为 `test_pre_merge_gate.NotFoundVerdictTests.test_sc2_trigger_matched_message` (TASK-002 承诺产出)。
  3. `NotFoundVerdictTests` 类是 TASK-002 **新增**到既有文件 `test_pre_merge_gate.py` 里的类 (TASK-002 deliverables: "新 NotFoundVerdictTests")。在基线 SHA `9e6a17c` (本 spec 任何改动落地之前), 该文件**存在**但**不含**这个类 —— 实读确认 (`git -C aria show 9e6a17c:.../tests/test_pre_merge_gate.py` 不含 `NotFoundVerdictTests` 字面串; 该类是本 spec 要新写的)。
  4. 因此若字面执行 `git -C aria worktree add <tmp> 9e6a17c` 后直接在该目录跑 `test_case_in_unit_tests` 指向的测试 (不额外拷入当前测试文件), pytest 对该测试路径的结果是**「未收集到匹配用例」**(exit code 5 / 0 selected) —— 这既不是 verification 里枚举的「收集错误」(collection error = import/语法失败, 通常 exit 2), 也不是「断言失败」(exit 1), 是**第三种、验收条款未覆盖的结果**。更严重的是：**这个「找不到」的结果与被守护的生产代码是否真正实现了 SC-1~SC-14 完全无关** —— 无论 TASK-003/006/007b/009/010/011 是否正确实现, 只要 worktree 停在 9e6a17c 且不拷入新测试文件, 该指令的输出永远一样。这正是 memory `false_green_dual_is_permanent_red` / `feedback_verify_assertions_reject_bad_implementations` 点名的「对好坏实现都给同一答案 = 零信息量的伪红」——恰是 R3 A1-M3(b) 本想根治的 `git stash` no-op 病灶的**同构复发**, 只是换了一层壳 (worktree 而非 stash)。
  5. 一个能让「收集错误」真实发生并携带信号的做法**存在**且本 yaml 自己在别处已经用过同类技巧 —— INV-1.encoded_as 用 `git -C aria show <c>^:...aether.py` 把旧版文件内容管进 python `exec` 后直接调函数断言, 而不是整树 checkout。对 SC-15 若把 TASK-012 的当前 (HEAD) 测试文件内容拷进 (或 `git show` 管入) `<tmp>` worktree 再跑, 该测试会因为 import/引用了 TASK-003/007b 才新增的符号 (`_no_run_gate_error` / `DISPATCH_VIABLE` / `gate_error.kind=="no-run-for-branch"` 等) 而在旧代码上产生**真实**的 `AttributeError`/`ImportError`/断言失败 —— 这才是「收集错误或断言失败」两个枚举分支真正对应的语义。但 yaml 里缺这一步「拷入当前测试文件」的显式指令。
- **后果 (实施者分叉 + TDD 红绿失效)**: 两个独立实施者读同一句话, 一个字面执行「只 checkout 不拷贝」(得到恒真的伪红, SC-15/INV-7「真跑一次证明回退会红」的初衷落空但字段级检查表面通过), 另一个额外做「拷入当前测试文件」(得到有信息量的真红) —— 产出的**质量保证记录**完全不同, 而 yaml 本身两种读法都不违反字面文字。这与我 R3 findings 里点名的「无字段能区分两种执行路径哪个对」是同一形状的缺陷 (memory `feedback_fix_the_class_not_the_instance`)。
- **建议**: 在 TASK-012.verification 里显式加一步, 例如: `"拷入当前测试文件: git -C aria show feature/152-no-run-for-branch:skills/phase-c-integrator/tests/test_pre_merge_gate.py > <tmp>/skills/phase-c-integrator/tests/test_pre_merge_gate.py 后再跑 test_case_in_unit_tests 指向的测试"` (与 INV-1.encoded_as 已用的 `git show` 管道技巧同构, 零新增机制); 或至少把「收集错误」的判据改窄为「导入/属性错误 (ModuleNotFoundError/AttributeError), 非『0 selected』」并显式要求先确认拷贝步骤已执行, 使「用后 worktree remove」前多一步「diff 前后 pytest 收集数量不同」的自证。

## 已核验无误 (程序化 + 实读)

- `agent_summary` 双向一致性: 20 任务的 `agent` 字段值与其在 `agent_summary` 对应桶内出现位置逐一核对 (python 脚本解析 yaml), 零 mismatch, 零遗漏/重复计入。
- `exec_order` 单调性: 全部 19 条依赖边逐一核验「每任务 exec_order > 其所有依赖的 exec_order」, 零违反。
- `estimated_hours` 求和: 20 任务逐项精确求和 = 51.0, 与 `metadata.estimated_hours: 51` 精确匹配。
- `sc_coverage_crosscheck`: 逐条比对 proposal.md 抽取的 SC-1~SC-16 (grep 全文), 16 条全部在 v4 crosscheck 表出现, 未换号/未合并/未蒸发; SC-14 三任务 (TASK-010a RED / TASK-010 / TASK-011) 与 INV-2 配对语义一致。
- `checklist_s7_mapping`: proposal §7 (line 235-240) 4 项逐条核对 (DISPATCH_VIABLE 裸全局引用 → TASK-007b / SC-15 两 skill 覆盖 → TASK-012 / traps 两处证据统一日期 → TASK-014 / record 缺失文件分支单测 → TASK-008), 全部字段级精确对应, 无缺项无错位。
- TASK-010a 的 5 条 RED 断言逐条实读基线 9e6a17c 核验**确为红**: (1) `phase-c-integrator/SKILL.md` 的 `pr_ci_status` 枚举行 (`:180`, `:276`) 均为 `"passing" | "failing" | "pending" | "not_applicable"`, 不含 `not_found`; (2) `:172-183` YAML 摘要块 (`output:` 起于 `:177`, 讫于 `path_coverage` `:183`) 不含字面 `gate_error` (全文 `gate_error` 命中仅在 `:248/:284/:290`, 均在此区间外); (3) 主仓 `.aria/config.template.json` 的 `phase_c_integrator.pre_merge_gate` 块不含 `no_run_prompt_after_observations` 也不含 `path_coverage_enabled` (grep 零命中); (4) `docs/decisions/DEC-20260731-001-c24-wait-adjudication-retirement.md` 文件**已存在**(#122 遗留), 但全文无「前向指针」字样、无 `📌`; (5) `path_coverage.py:36` 当前文案为「共 **9** 个」, 非 8。五条断言全部为真红。
- TASK-010a 的第 6 条隐含断言 (`DEFAULT_CONFIG 断言绿, 003 已落`) 语义自洽: 实读 `pre_merge_gate.py` 当前 (基线) `DEFAULT_CONFIG` 无 `no_run_prompt_after_observations`; 而 TASK-003 (TASK-010a 的直接依赖) 的 deliverables 明确会把该键加进 `DEFAULT_CONFIG` (Python dict, 非文档), 故 TASK-010a 运行时该键已在场, 与「003 已落」一致, 不构成矛盾 (这条断言检的是**代码**而非**文档**, 与另外 5 条文档断言分属不同的落地任务, 无需在 TASK-010a 标题里单列第 6 项)。
- TASK-016 (归档自删清单, R3 簇 #5) §3.5 全清单核对: proposal §3.5 (`:198`) 枚举的 9 类待删项 (§4 整段 / SC-8 / SC-9 dispatchable 部分 / DISPATCH_VIABLE 常量 / 2.3 渲染句 / SC-2 dispatch 子项 / SC-5 (c2) / 3.3 (a) 行 / §2.1 `.replace`) 与 TASK-016.conditional_parts 逐条对应, 无缺项。
- 负控 pattern (INV-3, R3 簇 #1) 基线实测: `grep -rn -E 'DISPATCH_VIABLE|dispatchable_workflows|/dispatches -d'` 限定 yaml 声明的路径范围, 实跑命中数 = 0, 与「基线 0 命中」的声明一致。
- INV-1 (R3 簇 #2) `return "pending"` 现状: `aether.py:226` 与 `:238` 各一处, 与 TASK-003/013 描述的「两处」计数一致; 四合取有向检验设计 (`git show` 管入 exec 后调函数) 优于 v3 的 `grep -c` 计数法, 不再受行数增删影响。

## Verdict

PASS_WITH_WARNINGS — vote: REVISE

无 Critical。我 R3 归属的唯一簇 (TASK-013 agent 归属分叉, A3-PP3-M1) 已完全闭合, 证据充分。但本轮通读发现 1 处新 Major: TASK-012 承载 SC-15 worktree 红窗核验的具体指令缺「拷入当前测试文件」这一步, 按字面执行会退化成对任何实现质量都给同一答案的伪红 (与 R3 A1-M3(b) 想根治的 `git stash` no-op 同构复发, 只是换壳), 违反 INV-7「NEG-4 必须真跑一次」的实质要求且构成实施者分叉风险。另有 1 处 Minor (`exec_order_note` 闭包枚举漏 TASK-010a, 纯文本备注未随图更新, 不影响真实调度)。Major 修复成本很低 (yaml 加一行 `git show` 管道指令, 与 INV-1 已用的同款技巧同构), 建议 v5 补上后可进 B.1; 若 owner 认为该 worktree 细节可留 B.2 执行时口头澄清 (类似 §7 checklist「留 Phase B 顺手」惯例), 也是可接受的降级路径, 但需显式留痕而非静默假设实施者会自行补上这一步。
