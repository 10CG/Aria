---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 1787404189909
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 1
minor_count: 1
---

# post_planning R1 — A2 (backend-architect) 审计报告

## 摘要

透镜 = TASK-003/006/007/009 相对 proposal.md §1/§2.1/§2.2/§2.3/§3.1/§4 的转录准确性 (函数名/参数/常量名/默认值/行号/插入位置/哨兵/消毒/CLI 旗标集)。已对 aria @ `9e6a17c` 实际代码逐条抽样核对 (`ci_backends/aether.py` / `pre_merge_gate.py` / `path_coverage.py` / `gate_state_helper.py` / `tests/test_pre_merge_gate.py`)。

结论: TASK-003 / TASK-007 / TASK-009 的函数签名、行号、插入位置、哨兵/消毒模式、常量名、CLI 旗标集转录**逐字精确**, 未发现漂移。TASK-006 存在 1 处 Major (INV-3 条件 scope 组的一个成员 —— §2.1 末段 `.replace` —— 在 TASK-006 里未被操作化, 只留一条易被反向误读的 `notes_scope` 注记, 无 `conditional_on`/无对 TASK-001 的依赖声明)。另有 1 处 Minor (措辞层面)。

## 已核验无误 (逐条抽样)

- **TASK-003**: `aether.py:218` docstring / `:225-226` `if not runs: return "pending"` —— 实测行号逐字match。`pre_merge_gate.py` `DEFAULT_CONFIG` 精确跨 `:57-69`；`compute_verdict` 精确跨 `:174-233`（`_build_output` 起于 `:236`）；插入点断言核实为真——`elif pr_ci_status == "not_applicable":` 分支实测止于 `:217`，`elif main_in_flight_runs:` 实测起于 `:218`，`not_found` 新分支必须插入这一空档的防呆理由（"main 非空时被 `main_in_flight_runs` 先命中"）经代码结构验证成立。`_build_output` 当前签名已含 `gate_error: dict | None = None` 可选键（#137 遗留），但 `compute_verdict` 当前调用点未透传 `gate_error=`——proposal 「+ `_build_output` 穿 `gate_error`」的改动点精确命中。docstring 引用 `:181-194`（compute_verdict docstring 止于 194 的 `"""`）与 `:253-256`（`_build_output` 内 #137 段落）逐字核实。
- **TASK-006**: `_verify_main_branch_exists` 实测跨 `:302-352`，签名 `(main_branch: str, remote: str, timeout: int = _LS_REMOTE_TIMEOUT) -> tuple[str, str]` 与 proposal 「保关键字签名与默认值的包装」逐字吻合；调用点 `:449` 实测确为 `gate_check` 内唯一调用处；测试 mixin `:85-89` 实测确为对旧名的打桩 `("ok", "")`；`:278-288`（模块级注释块）、`:305-319`（函数 docstring）、`:548-552`（`--remote` argparse help）均逐字核对到位；`_sanitize_for_json` 签名 `(text: str) -> str` 与「消毒」用法吻合；`verify_note` 哨兵初始化模式（`= ""`）与「哨兵」措辞吻合。
- **TASK-007**: `path_coverage.py` 中 `_parse_workflow` 实测起于 `:191`，`_result` 实测起于 `:62`（TASK-007 引用的 `:67` 是任务规划者自行核算的插入锚点——`changed_files_count` 形参行——非 proposal 原文引用，但经代码核实数值准确，非漂移）；`NON_AUTO_TRIGGER_KEYS` 存在且含 `workflow_dispatch`；`DISPATCH_VIABLE` 常量落点（`pre_merge_gate.py` 模块级）与代码落点声明吻合；§7 checklist 1（裸全局引用非默认参捕获）转录准确。
- **TASK-009**: `gate_state_helper.py` 模块 docstring 实测精确跨 `:2-18`（"markdown-driven" / "Usage (Python)" 原文俱在，F7 证据成立）；`CURRENT_SCHEMA_VERSION = "1.1"` 与骨架 JSON `format_version` 值一致；`GATE_STATUS_WAITING = "waiting"` 与「`wait→GATE_STATUS_WAITING("waiting")`」映射吻合；`write_gate_state` 当前实现为**整块重建**（`state["gate_state"] = {...}` 字面量赋值，非增量 patch）——证实 proposal 「显式 carry-forward 写回 (整块重建**必须**包含该键)」的技术前提真实存在，非臆测；当前文件确无任何 `main()`/CLI/argparse（grep 全文件零命中），F7「零消费方」成立；`reset_no_run_observations`/`reset_retry_count` 确认为全新函数（当前不存在同名符号）。

## Findings

### [A2-backend-architect-PP-M1] TASK-006 未操作化 INV-3 条件 scope 组内归属自己文件的成员 (`§2.1 .replace`)

- **Category**: transcription / ordering
- **Scope**: TASK-006 (`detailed-tasks.yaml` + `metadata.invariants.INV-3`)
- **问题**: proposal §3.5（原文 `openspec/changes/.../proposal.md:198`）明确写: 若 `dispatch_viable=false`，"`§2.1 末段的 <pr_branch> .replace` (占位符随 dispatch 行消失, 回填无对象...), **整组从本 spec 删除**"。`§2.1 .replace` 是 `gate_check` 内的代码（`out["gate_error"]["message"].replace("<pr_branch>", ...)`），其唯一实现落点是 **TASK-006**（deliverables 明确写 "回填 `<pr_branch>` 与 `raw_message` 重同步"），而不是 TASK-007。
  但 `detailed-tasks.yaml` 里:
  1. `metadata.invariants.INV-3.rule` 原文抄录了 proposal 的删除清单，逐字包含 "`§2.1 .replace`"；但同一条 INV-3 的 `encoded_as` 字段写: `"TASK-007.conditional_on = TASK-001.dispatch_viable; 其余任务无条件"` —— 与 `rule` 字段自相矛盾（`rule` 说 `§2.1 .replace` 该组条件化, `encoded_as` 却断言"其余任务无条件"，而 `§2.1 .replace` 恰恰属于"其余任务"里的 TASK-006）。
  2. TASK-006 本身没有 `conditional_on` 字段，`dependencies` 只有 `[TASK-005]`，不含 `TASK-001`。
  3. TASK-006 的 `title`/`deliverables` 把 "回填 `<pr_branch>` 与 `raw_message` 重同步" 写成无条件动作。
  4. 唯一触及此事的是一条措辞含糊的 `notes_scope`: "回填 `.replace` 在 `dispatch_viable=false` 时仍保留为 no-op 守卫? 否 — INV-3: false 则不引入 `.replace` (...)"。这句以反问句自答形式出现, 容易被实施者反向读成"保留就好"（本审计席第一遍通读时即读反, 复核 proposal 原文后才纠正）——且即便读对方向, 它也**没有给出可操作的实现指引**（不像 TASK-007 的 `conditional_on` 那样给出明确 if/else 落点）。
- **实测影响**: 由于 `.replace("<pr_branch>", ...)` 在 `dispatch_viable=false` 时对不含该子串的字符串是真正的 no-op（SC-5 (c1) "对无占位 message 平凡真" 本身承认这点），**运行时行为不受影响**（这是我判定为 Major 而非 Critical 的原因——不会 fail-open, 不会漏测）。但这是一处货真价实的**转录漂移**: proposal 明确要求的"条件 scope 组完整性"（INV-3 本体所指向的正是这件事）在派生层的 `encoded_as` 字段与 TASK-006 的可执行字段（title/deliverables/dependencies/conditional_on）之间没有对齐，只留一条容易被误读、且不可操作化的旁注。
- **建议**: 二选一即可收敛:
  (a) 修正 `INV-3.encoded_as` 为 `"TASK-007.conditional_on = TASK-001.dispatch_viable; TASK-006 的 §2.1 .replace 子项同受此条件约束但因该子操作为可证明的 no-op, 允许无条件实现, 保留 notes_scope 存档"`，把"为什么允许不设 conditional_on"这件事从隐性注记提升为显性裁定；或
  (b) 给 TASK-006 补 `dependencies: [TASK-005, TASK-001]` + 在 deliverables 里把 "`.replace`" 一项显式标注 "`if DISPATCH_VIABLE: ...` 或按 TASK-001 结果决定是否写入该行"，与 TASK-007 的 `conditional_on` 处理方式对称。
  两者选一, 但不能保持现状的"rule 说条件化、encoded_as 说无条件、task 字段两不沾"的三方不一致。

### [A2-backend-architect-PP-m1] TASK-007 的 `_result :67` 行号锚点是任务规划者自行推算, 未在 proposal 中出现字面引用

- **Category**: transcription
- **Scope**: TASK-007 deliverables
- **问题**: TASK-007 deliverables 写 "`path_coverage.py` (`_parse_workflow` `:191-300`; `_result` `:67`; `_evaluate` 规则 6 调用点)"。proposal §4 只说 "`_result()` 加可选参数", 未给出行号。`_result` 函数定义实测起于 `:62`, `:67` 对应形参列表最后一行 `changed_files_count: int = 0,`（新增可选参数的合理插入锚点）。经代码核实该行号数值准确, **不构成漂移**, 但因为它是派生层新引入、proposal 原文不存在的具体化引用, 若后续 proposal 或代码有变动而此处未同步复核, 容易变成失效指针 (fix-the-class 视角: 派生层"自行加行号"这一形状值得在 B.2 执行前再核一遍, 尤其是 backend-architect 拿到任务时应把 `:67` 当作"建议锚点"而非"精确契约", 因为可选参数插入位置在实现时可能因风格调整而挪动 1-2 行)。
- **建议**: 无需改 yaml；backend-architect 执行 TASK-007 时把 `:67` 当参考而非断言, 以函数签名匹配为准, 不需要逐行匹配。

## Verdict

PASS_WITH_WARNINGS — vote: REVISE (1 Major 需在 A.2 定稿前对齐 INV-3.encoded_as 与 TASK-006 字段; 不阻塞若 owner/主控认为"行为无差异"可接受现状留痕推进)。
