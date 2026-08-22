---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 1787404603790
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A5-knowledge-manager
critical_count: 0
major_count: 2
minor_count: 3
---

# post_planning R1 — A5 (knowledge-manager) 审计报告

## 摘要

透镜 = 方法论合规 / 可追溯性 / 与同日 ship precedent `secret-guard-manifest-precision` (#179) detailed-tasks.yaml 形态对照。实读 proposal.md 全文 (310 行) + detailed-tasks.yaml 全文 (17 任务) + precedent yaml 全文 (379 行) + `AGENT_MAPPING.md` + `state-scanner/scripts/lib/{detailed_tasks,spec_complete}.py` 源码，并**实跑**两个脚本对本 yaml 求值 (非纸面推断)。

结论: 0 Critical。2 Major — 均属「INV-3/INV-5 等条件性/检查点 metadata 声称『其余任务无条件』或『两任务都覆盖』, 但实际承载该内容的任务未被标注」这一形状 (与 A2-M1、A3-M3 收敛, 共同指向 TASK-011 是本 yaml 审计密度最薄的节点), 以及 TASK-001 文档/memory 修正类 deliverable 缺配套 verification。3 Minor — agent 字段命名/`main-loop` 认可性、TASK-007 `status: skipped` 与归档门 fail-closed 白名单的隐含依赖 (与 A3-m1 收敛，补充归档门代码级证据)、顶层聚合章节相对 precedent 的形态简化。Rule #10 (TASK-000)、Rule #6 第三行 (TASK-012)、归档门 runtime_probe (TASK-016) 三处落点经代码级核实均**真实存在且文字准确**，非虚指。

## 已核验无误

- **state-scanner 实际解析**: `python3 -c "...detailed_tasks.parse_detailed_tasks(text)..."` → `parse_ok=True`, `17 task(s) parsed`, 17 个 `- id:` 边界与 `status`(全 `pending`)/`title` 逐条正确切分；`conditional_on`/`notes_scope`/`gate` 等派生层新增字段、`checklist_s7_mapping`/`parallel_tracks` 等新增顶层章节均未破坏 `_tasks_block_bounds`/`_TASK_ID_LINE_RE` 的定界逻辑 (parser 只认 `tasks:` 顶层键 + 同缩进 `- id:` 项，对其余字段/章节名不敏感)。
- **归档门实际运行**: `python3 aria/skills/state-scanner/scripts/lib/spec_complete.py --gate openspec/changes/pre-merge-gate-no-run-for-branch` → `complete=false` (符合预期，17/17 pending)，`verdict="warn"`，`warnings=["runtime_probe[record]: production telemetry partition missing: .aria/gate-state-telemetry.jsonl"]`，`unverified_claims=[{"claim":"runtime_probe:record",...}]`。此结果与 proposal **SC-16 (b)** 断言 ("红窗 — SC-13 之前...probe outcome=warn + unverified_claims 含本 partition 条目") 逐字吻合，实证 frontmatter `runtime_probe:` 声明 + 本 yaml 存在的组合确实可评估、不崩溃 (SC-16(a) 前置成立)，而非纸面声称。
- **依赖图 / exec_order**: 17 个 `exec_order` 值为 0-16 连续无缺无重复；全部 17 条 `dependencies:` 目标任务的 `exec_order` 均严格小于自身，无环。`parallel_tracks` 声明的两轨 (gate 轨 TASK-002~007 / helper 轨 TASK-008~009) 文件域 disjoint 属实 (`pre_merge_gate.py`/`path_coverage.py` vs `gate_state_helper.py`)。
- **estimated_hours 算术**: 17 项逐一相加 (0.5+1.5+3+4+2+3+3+4+4+5+3+4+4+1+3+2+2) = **49**，与 `metadata.estimated_hours: 49` 精确一致；`parent_task_count: 8` (P0-P7) 与实际 parent 分组数一致；`total_tasks: 17` 与实际一致。
- **SC 覆盖面**: `sc_coverage_crosscheck` 列出 proposal SC-1~SC-16 全部 16 条，逐条与 proposal §Success Criteria 表交叉核对未见遗漏 (含 SC-16 三分支 (a)/(b)(c)/(c)复核 分别落 TASK-000-存在性/TASK-014/TASK-016 的正确拆分)。`checklist_s7_mapping` 的 4 项 (DISPATCH_VIABLE 裸引用 / 两 skill AB 覆盖 / traps 日期字段 / record 缺失文件分支单测) 逐一在对应 TASK 的 verification/notes/title 文字中找到真实落点，非空引用。
- **Rule #10 / Rule #6 / 归档门三处指定检查点**:
  - TASK-000.notes 显式点名 "coordination.enabled=true ⇒ 必须调 run_gate (Rule #10: 不得自豁)" — `run_gate` 经 `grep` 确认是 `phase1_gate.py` 中真实存在的公开函数 (`def _run_gate_impl` + `run_gate` 包装, 多处 `phase1_gate.run_gate:` 日志前缀), 非虚指函数名。
  - TASK-012 (Rule #6 第三行) 与 proposal `rule6_note` 段逐字对齐: 覆盖 SC-15 的处方性·套件覆盖外场景, 三义务 (点名行为 + NEG-4 定向 fixture + `aria-plugin#127` 缺口评论) 均在 TASK-012 title/deliverables/notes 中一一对应。
  - TASK-016 (归档门) 的 "openspec-archive (归档门评估 runtime_probe = pass, SC-16 (c) 复核) + proposal Status → Complete" 与 `spec_complete.py` 的 `_normalize_status()` 代码 (`complete`/`completed` token → `"done"`) 构成的第三条 OR 分支相符 —— 这条 Status-bump 兜底路径经代码实读确认存在，对 m2 (见下) 的 `status: skipped` 隐患构成真实缓解机制，而非我方臆测。
- **baseline_sha**: `metadata.baseline_sha: "9e6a17c"` 已正确更新为 Phase B 实际分支起点，未误沿用 proposal 正文冻结的 `400f0bc`；proposal 头部已声明二者触点字节 diff 为空 (行号继续有效)，故两处基线值不同不构成漂移。

## Findings

### [A5-knowledge-manager-PP-M1] TASK-011 未标注 INV-3 条件 scope 归属自己文件的成员 (§3.3 处方段 (a) 行)，与 metadata 声称「其余任务无条件」矛盾

- **scope**: TASK-011 / `metadata.invariants[INV-3].encoded_as`
- **问题**: `INV-3.encoded_as` 写明 "TASK-007.conditional_on = TASK-001.dispatch_viable; **其余任务无条件**"。但 proposal §3.5 明确列出 `dispatch_viable=false` 时应整组删除的内容包含 "3.3 (a) 行" —— 即 §C.2.4 步骤 6 的处方三选一段落里的 dispatch 命令行选项。而 §3.3 原文自述 "一处定义, §C.2.4 步骤 6 与 workflow-runner 2.5 共同引用"，该定义的唯一物理落点是 `phase-c-integrator/SKILL.md :252-263`，正是 TASK-011 deliverables 第一项 ("SKILL.md §C.2.4 ... 步骤 4·5·6 ... 处方段") 的字面覆盖范围。TASK-011 全文无 `conditional_on` 字段、无 `notes` 字段提及 dispatch_viable，是本 yaml 17 个任务中唯一一个"内容确实受 TASK-001 结果调制、却零标注"的任务。
- **实测**: 逐字比对 proposal §3.5 删除清单 (§4 整段 / SC-8 / SC-9 dispatchable 部分 / SC-2 dispatch 子项 / SC-5 (c2) / **3.3 (a) 行** / §2.1 `.replace`) 与本 yaml 各任务的 `conditional_on`/`notes`/`notes_scope` 字段: TASK-007 (`conditional_on` 显式) 覆盖了 §4/SC-8/SC-9/SC-2 子项/SC-5(c2)；TASK-006 (`notes_scope`) 覆盖了 §2.1 `.replace`（但同席 A2-M1 已指出该覆盖本身"未操作化, 只留一条注记"）；**唯独 "3.3 (a) 行" 这一项在全 17 任务中找不到任何标注落点**——它归属的 TASK-011 只字未提。
- **风险**: 若 B.2 执行到 TASK-001 判定 `dispatch_viable=false`（F6 已实测本 Forgejo 版本 `/actions/runs`/`/actions/workflows` 404, dispatch 可用性本身存疑, 假为较可能分支）, TASK-011 执行者若不主动回查 proposal 全文, 会照抄 §3.3 原始三选一文案（含 (a) dispatch 命令行）写进 `SKILL.md`，产生"文档记载一个代码从未实现的处方选项"的转录漂移——且这条漂移恰恰发生在 §C.2.4 处方段的**唯一权威定义处**，会被 workflow-runner 2.5 的引用方 (TASK-010) 一并带偏。同时也直接证伪 `INV-3.encoded_as` 自身"其余任务无条件"的断言。
- **收敛信号**: 与 A2-M1 (TASK-006 `.replace` 同款条件缺口)、A3-M3 (TASK-011 的 INV-5 零自动执行检查点缺失) 共同指向 TASK-011/§3.3 是本次派生里审计密度最薄的落点——三席从三个不同不变量 (INV-3/INV-3/INV-5) 各自独立命中同一任务, 建议 fix 时按"这个任务节点"整体补齐而非逐条打补丁 (memory `fix-the-class`)。
- **建议**: 在 TASK-011 补一条 `notes`（对称于 TASK-006 的 `notes_scope`）: "若 TASK-001.dispatch_viable=false, §C.2.4 步骤 6 处方段省略 (a) 行, 仅保留 (b)(c); 该省略与 TASK-007/TASK-006 同属 INV-3 条件组"，并同步改写 `INV-3.encoded_as` 为"TASK-006/TASK-007/TASK-011 条件, 其余任务无条件"以求字面自洽。

### [A5-knowledge-manager-PP-M2] TASK-001 的两项文档/memory 修正类 deliverable 无对应 verification，可追溯性缺口

- **scope**: TASK-001 (deliverables 第 2/3 项 vs verification)
- **问题**: TASK-001 列出 3 项 deliverables —— (1) throwaway 分支活体探针 (2) `pre-merge-gate-empirical-traps.md` §六新增 `dispatch_viable=<bool>` 证据行 (3) memory `reference_forgejo_new_branch_paths_filter_no_run` 按 traps 镜像修正 ("带同一证据; 容器本地")。但 `verification:` 只有 2 条，均只核验 (1) 的判定逻辑本身 (`dispatch_viable` 布尔取值规则 + 写回 `metadata.dispatch_viable`/`TASK-007.status`)，**没有任何一条核验 (2)、(3) 两处文档/memory 编辑确实发生**（例如 "traps §六新增行存在且含 HTTP 码/run id/Δt/日期四要素" 或 "memory 文件 diff 显示已按证据同步"）。
- **风险**: 这正是本次审计任务指名要查的"对 memory 修正 (TASK-001) 的可追溯要求"。项目已有实证的失败模式是"有记录"≠"有路由"、deliverable 无 verification 时容易被静默漏做而任务仍标 `done`——memory 文件本身还是容器本地 (`feedback_memory_store_is_container_local_not_shared`)，日后跨容器核对该修正是否真的发生会缺乏机读证据，只能靠人工翻 git blame/session 记忆。traps §六是本 spec 明确要求"每条不能靠读代码想出来"的仓内 SOT，若真实探针结果 (dispatch_viable) 没有落进 traps 就直接进入后续任务，SC-15/rule6_note 引用的"traps 两处证据统一日期字段"(checklist 3) 在 TASK-014 侧核验时会缺第一处证据。
- **建议**: 在 TASK-001 verification 补一条: "`grep 'dispatch_viable=' aria/skills/phase-c-integrator/references/pre-merge-gate-empirical-traps.md` 命中且同行含 HTTP 码/run id 或 `queued-unobserved`/Δt/日期四要素; memory 文件 `reference_forgejo_new_branch_paths_filter_no_run.md` 的 diff 存在且引用同一证据（无 diff 记为已核实无需修正, 而非静默跳过）"。

### [A5-knowledge-manager-PP-m1] `agent: main-loop` 未见于 `AGENT_MAPPING.md` 认可表；agent 字段命名前缀与精确 precedent 不一致

- **scope**: 全部 17 任务的 `agent:` 字段 vs `AGENT_MAPPING.md` vs precedent `secret-guard-manifest-precision` yaml
- **实测**: `AGENT_MAPPING.md`（`aria/1.66.3/skills/task-planner/AGENT_MAPPING.md`）"可用 Agent" 表仅列 6 值: `backend-architect` / `mobile-developer` / `qa-engineer` / `api-documenter` / `knowledge-manager` / `tech-lead`。本 yaml 6 处 `agent: main-loop`（TASK-000/001/012/014/015/016）不在该表中；其余任务用裸名 `qa-engineer`/`backend-architect`/`knowledge-manager`（无 `aria:` 前缀）。对照精确 precedent (#179，同日 ship) —— 该 yaml 统一用 `aria:qa-engineer`/`aria:backend-architect`/`aria:knowledge-manager`（带前缀）+ 裸 `owner`（TASK-000 owner 门），**零 `main-loop`**。
- **进一步核实**: 全仓 grep `openspec/archive/*/detailed-tasks.yaml` 发现 `agent: main-loop` 有 2 份既往归档 spec 先例（`2026-07-09-agent-router-auto-project-agent-injection`、`2026-07-09-runtime-probe-archive-gate-integration`），共 17 次出现，用途集中在 git/ship/live-probe/Phase D 收尾等"主循环自身执行、不可委派通用子 agent"的动作——与本 yaml 6 处 `main-loop` 的任务内容（phase1_gate claim / 活体探针+分支操作 / Rule#6 真跑+issue评论 / 活体 dogfood / ship 合并双推 / Phase D 收尾）语义高度吻合，判断为**沿用既有真实执行角色，非本 yaml 臆造**；`owner` 值同样在全仓语料中出现但不在 `AGENT_MAPPING.md` 表内。
- **结论/建议**: 这是 `AGENT_MAPPING.md` 文档本身的既存空缺（`main-loop`/`owner` 两个高频真实值均未收录），不是本 yaml 独有缺陷，不影响任何脚本解析（state-scanner 不读 `agent:` 字段语义）。仍建议顺手把 `main-loop`/`owner` 补进 `AGENT_MAPPING.md`"可用 Agent"表（标注"不可委派子 agent 的主循环自留动作"），并统一本 yaml 与 precedent 之间 `aria:` 前缀的有无——纯格式一致性，非阻塞项。

### [A5-knowledge-manager-PP-m2] TASK-007 `status: skipped` 分支与归档门 fail-closed 白名单的隐含依赖未点名（收敛 A3-m1，补充代码级证据）

- **scope**: TASK-007.status 未来取值 / `metadata.invariants[INV-3]` / TASK-016
- **与 A3-m1 关系**: A3 已从"下游依赖能否解析 status=skipped"的执行语义角度指出这一空白；本席从**归档门代码实现**角度补充证据，属同一根因的不同侧面, 不重复计分。
- **实测**: `state-scanner/scripts/lib/detailed_tasks.py` 的 `_DONE_FAMILY = frozenset({"done", "completed"})` 是**显式 fail-CLOSED 白名单**（模块 docstring 原文: "everything else (pending/deferred/blocked/in_progress/unknown/None) counts as residual"）——`"skipped"` 不在其中。若 `TASK-001.dispatch_viable=false` 且 TASK-007 被置为字面 `status: skipped`（INV-3 措辞），仅靠"detailed-tasks.yaml 全部 done"这一条 OR 分支，该 spec **永远无法**通过 `is_spec_complete`。全仓 20 份归档 yaml 里从无 `status: skipped` 先例，此为首次引入的状态字面量。
- **缓解证据（已核实为真实存在，非臆测）**: `spec_complete.py` 的 `is_spec_complete` 三条 OR 分支之一是 `_normalize_status(Status) == "done"`；`collectors/_status.py::_normalize_status` 的 `("done","complete","completed")` token 匹配确认 Status 头写成 `"Complete"` 会被独立归一化为 `"done"`。TASK-016 的 deliverable 已包含"proposal Status → Complete 含审计轨迹句"，这条路径**结构上能绕开** TASK-007 单个任务 `skipped` 造成的 yaml-branch 不可达问题。
- **风险**: 缓解路径成立完全依赖 TASK-016 记得执行 Status 改写这一步；这条"skipped 靠 Status 覆盖兜底"的因果链目前只存在于本审计报告与代码阅读中，yaml 自身（INV-3 / TASK-007 / TASK-016）均未写明。若未来任何人重构 TASK-016 或提前做部分归档检查（如 D.1 中期自检），会对着一个"17 项任务某一项 skipped"的 yaml 得到误导性的"未完成"判读。
- **建议**: 在 `INV-3.rule` 或 TASK-016.notes 补一句: "TASK-007 status=skipped 时, spec 完成判定不经 yaml-all-done 支路 (`skipped` 不在 done-family), 而经 D.2 的 `proposal.md Status → Complete` 归一化支路 (`_normalize_status` token 匹配) 兜底放行，此依赖须在 TASK-016 显式核对"。

### [A5-knowledge-manager-PP-m3] 顶层聚合章节相对精确 precedent 有所简化（`execution_order`/`agent_summary` 缺失；`parallel_tracks` 覆盖不全）

- **scope**: 全文顶层结构 vs precedent `secret-guard-manifest-precision` yaml 尾部
- **实测**: precedent 在 `tasks:` 块后另有 `execution_order:`（按 phase 列出 order + `parallel_groups` 细粒度并行分组）与 `agent_summary:`（agent → 任务列表的反向聚合，便于人工核对分配是否遗漏/重复）两节；本 yaml 只有 `sc_coverage_crosscheck` / `checklist_s7_mapping` / `parallel_tracks` 三节，无对应的 phase 级执行顺序总览与 agent 反向聚合。`parallel_tracks` 仅声明两轨 (gate 轨 TASK-002~007 / helper 轨 TASK-008~009)，但 TASK-010（`dependencies: [TASK-009]`，不依赖 TASK-006/007）理论上可与 gate 轨尾部 (TASK-006/007) 并行执行，未被纳入任何轨道声明——即 yaml 自身的 `dependencies` 字段已经允许比 `parallel_tracks` 文字描述更多的并行度，两者不一致（前者是权威判据，后者只是执行建议，未构成正确性问题，纯属遗漏优化机会）。
- **验证影响**: 已实测 state-scanner `parse_detailed_tasks`/`spec_complete.py --gate` 均只依据 `tasks:` 顶层键定界与 `- id:`/`status:`/`title:` 三字段取值，缺失 `execution_order`/`agent_summary` 或 `parallel_tracks` 覆盖不全**零解析影响**；纯粹是人工核对效率与跨 spec 一致性问题。
- **建议**: 非阻塞，机会性顺手补 `agent_summary:`（六 agent + main-loop → 任务列表反向索引，便于人工快速核对 6 处 `main-loop` 分配是否都对应"主循环自留动作"）；`parallel_tracks` 视 B.2 实际调度需要决定是否纳入 TASK-010。
