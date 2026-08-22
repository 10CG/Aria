---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 1787406299787
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 2
minor_count: 1
---

# post_planning R2 — A2 (backend-architect) 审计报告

## 摘要

透镜 = TASK-006 `conditional_parts`+依赖闭合 / TASK-007a·007b 拆分后逐字核对 proposal §4·§2.3 / TASK-003 INV-1 有向检查可执行性 / TASK-009 CLI 签名逐字核对 proposal §3.1 v7 / v2 新增文本机制层矛盾扫描。已对 aria @ `9e6a17c` 实际代码重新抽样核对 (`pre_merge_gate.py` gate_check 全函数 `:387-529`、`compute_verdict`、`_verify_main_branch_exists`)。

结论: R1 A2-M1 (INV-3 未操作化) 与 A2-m1 (`_result :67` 未标注) **均已闭合**, 证据见下。TASK-007a/007b 拆分后行号/deliverables 与 proposal §4/§2.3 逐字核对**无漂移**, INV-2 (qa→be 配对) 与条件 scope 正确落到位。TASK-009 CLI 签名与 proposal §3.1 v7 逐字核对**无漂移**。但本轮发现 2 处新 Major: (1) TASK-004 的数值 `exec_order` 字段未随 R1 处置「前移到 2 之前」实际改写, 与顶层 `execution_order` 叙事字段自相矛盾, 且缺依赖边兜底, 存在真实的调度误序风险 (TASK-003 可能先于 TASK-004 落地, 复现 A1-M4 原本要修的「自证快照」); (2) TASK-003 的 INV-1「父提交 checkout」验证机制表述模糊, 无具体 git 命令、无自动化兜底, 依赖 main-loop 临场发挥。另 1 处 Minor: TASK-006 新引入的 `:404-408` 注释锚点是派生层自行推算 (同 R1 `_result :67` 形状), 未如后者般标注「参考锚点」。

## R1 处置核对

| R1 簇/finding | v2 处置 (声称) | 证据 | 判定 |
|---|---|---|---|
| A2-M1 (INV-3 未操作化 TASK-006 `.replace`) | TASK-006 加 `conditional_parts` + `dependencies: [TASK-005, TASK-001]` | `conditional_parts: "仅 §2.1 末段 <pr_branch> .replace 回填随 metadata.dispatch_viable: false ⇒ 不引入 .replace (...); 其余...无条件"`；`dependencies: [TASK-005, TASK-001]` 实读确认两者俱在 | **closed** |
| A2-m1 (`_result :67` 未标注) | 标注为「参考锚点」 | TASK-007b deliverables: `"_result :67 参考锚点"` | **closed** |
| A1-M5 (TASK-007 RED+GREEN 同任务同 agent) | 拆 TASK-007a(qa,RED)/TASK-007b(be,GREEN) | 实读确认 agent 字段分列 qa-engineer / backend-architect; `TASK-007b.dependencies=[TASK-007a]` | **closed** (交叉核实, 非我 R1 finding 但落在本轮核查项内) |
| A1-M4 (守卫 TASK-004 前移 + SC-7 mutation) | "exec_order 前移到 2 之前 (gate 轨首位)" | 见下方 [A2-PP2-M1] — **数值字段未改**, 仅顶层 `execution_order` 叙事字段体现前移 | **partial** |

r1_closed=3, r1_partial=1, r1_not_addressed=0 (计数范围: 本表 4 行, 含 1 行跨席交叉核实)。

## 已核验无误 (逐条抽样)

- **TASK-006 gate_check 插入范围 `:508-527`**: 实测 `def gate_check` 起于 `:387`（grep 确认），PR CI 查询 `try:` 块起于 `:508`（`pr_status = backend.query_pr_ci(pr_branch)` 在 `:509`），函数尾 `return compute_verdict(...)` 闭括号止于 `:527`——与 TASK-006 deliverables "gate_check :508-527 插入" 逐字精确匹配；proposal §2.1 给出的 `:485-497`(in-flight try)/`:498-506`(not_applicable 短路) 两段亦逐字核实无误（复核基线冻结注记为真）。
- **TASK-007a/007b 拆分对 proposal §4/§2.3 逐字核对**: `_parse_workflow` dispatchable 判定（`on:` 含 `workflow_dispatch`；标量/flow/块三种写法）→ TASK-007a 测试 + TASK-007b 实现 deliverables 逐字覆盖；`_evaluate` 加 `dispatchable_workflows`（= matched 中 dispatchable 者）→ 同上；`_result()` 加可选参数、仅规则 6 调用点传 → TASK-007b 明确限定"仅规则 6 传, 其余 8 处不改"（与 proposal "仅规则 6 调用点传 matched 子集, 其余 8 处 `_result` 调用不改" 字面一致）；§2.3 "当 `DISPATCH_VIABLE and dispatchable_workflows` 追加处方行"、"basename"、"`<owner>/<repo>` `<pr_branch>` 占位"、"禁用 `str.format`" 五要素全部逐字落在 TASK-007b deliverables/notes。`workflow-files-changed` 下 `dispatchable` 恒 `[]` 的设计限制在 TASK-007b notes 原样保留("禁扩全量列表")。INV-2 配对（qa RED → be GREEN）与 INV-3 条件 scope（`conditional_on` 挂在两任务、依赖边到 TASK-001）均对称正确。
- **TASK-009 CLI 签名 vs proposal §3.1 v7**: `--state-file` 必填无缺省（"CLI main (record/reset/clear; --state-file 与 --source 必填"）与 proposal "`--state-file` 必填无缺省, 缺失 exit 2" 一致；`reset_retry_count` 具名函数、"与 reset_no_run_observations 对称" 措辞逐字沿用；"wait→waiting 映射" 对应 proposal `wait→GATE_STATUS_WAITING("waiting")`；"骨架创建" 对应 "state 文件不存在且 verdict=wait 时先创建骨架"；"telemetry 派生路径" 对应 "路径由 CLI 从 `--state-file` 派生"；"stdout JSON 含 elapsed_seconds/next_check_at" 与 proposal stdout JSON 键集一致；exit 0/2 语义一致。TASK-008 (RED) 测试清单与 SC-11(a)-(d) 逐条比对未见遗漏或增字（"缺 `--source` 或 `--state-file` 各 exit 2" 的粒度模糊性系 proposal SC-11(d) 本身固有表述, 非派生层新引入的漂移, 不计入本轮 finding）。
- **INV-3 四落点 encoded_as**: metadata.invariants.INV-3 现列全四落点（TASK-007a/007b 整任务 / TASK-006 `.replace` / TASK-011 三处文档面 / TASK-015 CHANGELOG），且 TASK-006/011/015 均带 `dependencies` 含 `TASK-001` 的边——与 proposal §3.5 清单逐项对应，未发现遗漏或方向错误。

## Findings

### [A2-backend-architect-PP2-M1] TASK-004 数值 `exec_order` 与 R1 处置「前移」矛盾, 存在真实调度误序风险

- **Category**: ordering
- **Scope**: TASK-004.exec_order / 顶层 `execution_order` 字段 / TASK-002/003/004 的 `dependencies`
- **问题**: R1 disposition #4（A1-M4）裁定 "exec_order 前移到 2 之前 (gate 轨首位)"——即 TASK-004（守卫, 依赖 `[TASK-000]`）必须先于 TASK-002/003 落地, 否则 "守卫落在被守护变更之后 ⇒ 自证快照"。v2 顶层 `execution_order` 叙事字段确实体现了前移: `"gate 轨: TASK-004 (守卫@基线) → TASK-002 (RED) → TASK-003 (GREEN...) → ..."`。但 **TASK-004 自身的 `exec_order:` 数值字段仍是 `4`**（未改写), 排在 TASK-002 (`exec_order: 2`) 与 TASK-003 (`exec_order: 3`) **之后**——与叙事字段直接矛盾。
  这不是纯措辞问题: `metadata.exec_order_note` 明文定义该字段是 "拓扑序的 advisory tie-break"——即当 `dependencies` 图本身不能唯一确定顺序时, 由它断歧义。实际依赖图里 TASK-002 与 TASK-004 都只依赖 `[TASK-000]`（互相之间**无边**), TASK-003 依赖 `[TASK-002]`。若调度方（含未来可能落地的机械化 tie-break, 或粗心的实施者只看数值字段）按 exec_order 数值在"就绪任务集合"中择优, 会推出 TASK-002(2) 先于 TASK-004(4)——TASK-002 完成后 TASK-003(3) 随即就绪, 又因 3<4 会**再次**被优先选中——即 TASK-003（真正修改 `aether.py`/`pre_merge_gate.py` 生产代码）可能在 TASK-004（守卫测试, 必须钉基线 `9e6a17c` 的行为快照）**落地之前**执行完毕。这正是 A1-M4 想根治的"自证快照"病灶原样复发, 只是换了一个字段掩盖。
  对比同一份 v2 里处理方式相同的另一处（traps §六三写者序, R1 disposition #6): 那里选择**显式加依赖边**（TASK-011 → TASK-001, TASK-014 → TASK-011）来钉死顺序, 而不是只改一个 advisory 数值。TASK-004 应同样处理却没有, 是"同类问题两种修法, 一种做实一种留虚"的不一致（fix-the-class 视角）。
- **实测影响**: 若主控 main-loop 严格照读顶层 `execution_order` 叙事字段执行, 不会出错; 但只要有任何一处（人工或后续自动化）改按 per-task `exec_order:` 数值排序（该字段本就是为此设计的, 参考价值不低于叙事字段), 就会复现「守卫在变更之后落」的问题, 使 TASK-004 的 SC-6/SC-7 守卫从"基线快照"退化为"看着已改代码写的自证测试"。
- **建议**: 二选一（or 二者并施）:
  (a) 给 TASK-002 补 `dependencies: [TASK-000, TASK-004]`（如 traps 写序先例, 加边而非仅调数值）——最稳健, 与已有先例手法一致；或
  (b) 把 TASK-004 的 `exec_order` 真正改写为小于 2 的值（如插入为 `1.5`，或全局重新连续编号 `TASK-000=0, TASK-001=1, TASK-004=2, TASK-002=3, TASK-003=4, ...` 并同步顺延后续所有任务的 exec_order), 使数值字段与叙事字段真正一致。
  当前状态两个字段互相矛盾, B.1 执行前应收敛为一致。

### [A2-backend-architect-PP2-M2] TASK-003 INV-1「父提交 checkout」验证机制欠具体, 无自动化兜底

- **Category**: executability
- **Scope**: `metadata.invariants.INV-1.encoded_as` / TASK-003.verification
- **问题**: R1 A1-M3 指出「两文件共现」是无向检查, v2 改为有向表述: `"该 commit 的父提交上 _normalize_pr_ci_status([]) == 'pending' 且本 commit 同时含两文件"`, TASK-003.verification 复述为 `"git stash-free 验证 = 父提交 checkout 下 _normalize_pr_ci_status([]) == 'pending' 且本 commit 同含两文件"`。
  这段文字对**做什么**表述清楚, 但对**怎么做**留了两处操作性空白:
  1. "父提交 checkout 下" 字面读法有歧义: 若真执行 `git checkout <parent_sha>`（切到 detached HEAD）核验完再切回, 存在误留在 detached HEAD 或误当作真实分支切换的风险——本项目 memory 已有 `feedback_detached_head_may_be_stale_rebase.md` 记录过 detached HEAD 掩盖问题的先例, 是本项目实证过的事故形状。"git stash-free" 这个限定词暗示作者其实想要的是**不触碰工作区**的非破坏性提取（如 `git show <parent_sha>:<path>`), 但文字没有给出具体命令, 留给 main-loop 临场发挥, 不同实施轮次可能选择不同（有的字面 checkout, 有的用 `git show`), 是"实施者分叉"的温床。
  2. 全篇没有把这条检查落成任何脚本/测试/CI 断言——它是纯 prose 步骤, 完全依赖 main-loop 在提交 TASK-003 commit 后主动记得去做这套 git 考古。没有 fail-closed 兜底（例如: 若 main-loop 忘记做这一步, 没有任何后续机制会发现 INV-1 事实上没被验证过）。
- **实测影响**: 不影响运行时行为（INV-1 关注的是"提交历史"而非产品代码行为), 也不会造成 fail-open; 但如果 main-loop 真的把 §1（aether.py）与 §2.2（compute_verdict）分两次提交（例如中途被打断、或子 agent 各自提交后由不同轮次的 main-loop 分别处理), 现有机制在"分两次提交"真实发生时**既不会阻止**也**不会被要求去验证**——因为验证本身是可选的口头步骤, 不是任何测试或 gate 的必经路径。
- **建议**: 补一条具体、可复制粘贴的非破坏性命令到 TASK-003.verification, 例如: `git show <this_sha>^:aria/skills/phase-c-integrator/scripts/ci_backends/aether.py | grep -A2 "if not runs"`（确认父提交仍返回 `pending`）+ `git show --stat <this_sha> | grep -c "aether.py\|pre_merge_gate.py"`（确认本 commit 同含两文件, 期望值 2）——避免任何形式的实际 `git checkout`（无论是否 detached), 且把"这两条命令"钉为唯一合法验证方式, 不留解读空间。

### [A2-backend-architect-PP2-m1] TASK-006 新引入的 `:404-408` 注释锚点系派生层自行推算, 未标注为参考锚点

- **Category**: transcription
- **Scope**: TASK-006 deliverables
- **问题**: TASK-006 deliverables 写 "`:278-288`/`:305-319`/`:404-408` 注释"。前两个行号 (`:278-288`、`:305-319`) 直接来自 proposal §2.1 原文（"`:278-288` / `:305-319` 注释与 `:548-552` `--remote` help 随之更新"), R1 已核实精确。但 `:404-408` **不在 proposal 任何位置出现**——是任务规划者新增的自行推算行号。经代码核实（`gate_check` docstring 内 "Query order" 段落, 描述 `:498-506` not_applicable 短路的既有说明), 数值本身**准确**且落点合理（这段文档确实是新增 PR 分支核验行为的自然文档落点), 不构成漂移。但这与 R1 已被指出并修正过的同类问题（TASK-007b 的 `_result :67`, 该处已改标"参考锚点"以提示"以函数契约匹配为准, 不需精确行号"）是**同一形状**, 这里却没有同样标注, 三个行号被并列写成同等确定性的"事实引用", 容易让实施者把 `:404-408` 当作和 `:278-288` 一样的、来自 proposal 的精确契约。
- **建议**: 无需改 yaml 语义；backend-architect 执行 TASK-006 时把 `:404-408` 当作"建议插入区间"而非精确契约（若代码在 TASK-003/004/005 落地后因插入行数偏移而挪动，以"docstring 内 Query order 段落"这一结构性描述为准，不做逐行匹配）。

## Verdict

PASS_WITH_WARNINGS — vote: REVISE（2 Major 需在 A.2 定稿/B.1 起跑前收敛: TASK-004 exec_order 与叙事字段矛盾必须二选一消除；TASK-003 INV-1 验证步骤应补具体非破坏性命令。两者均不阻塞已收敛良好的 TASK-006/007a/007b/009 派生质量，若主控/owner 认为"主控执行时会正确读叙事字段+会用非破坏性方式做 git 考古"可接受现状风险留痕推进）。
