---
checkpoint: post_spec
mode: convergence
rounds: 8
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-17T09:10:16.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [backend-architect]
---

# post_spec Round 8 — backend-architect

被审对象: proposal.md v9 (仓库 HEAD `a563192`), 相对 v8 (`15ab323`) 的四处改动 (SC-9 补两个实质锚点 / SC-12 加「含新增 skill」/ T2b+T4「搬」改「复制」/ `fault_matrix.py` 非空输出目录改报错退出并重跑)。任务: 对账本席 R7 (零发现); 核四处改动有没有修对、有无带出新问题; 复核 §Impact/§D5.6 的运行时描述是否仍准确。

## R7 对账

**无 R7 条目**(本席 R7 Findings 为 0 critical / 0 major / 0 minor, 见 `post_spec-R7-...-backend-architect.md`)。

v9 的四处改动是否触及本席 R7 核实过的运行时结论 (S_FAIL 终态 / 不重试 / 默认不告警 / `fail_detail` 内容 / 垫片机制) —— **不触及**:

- `git diff 15ab323 a563192 -- openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md` 里含运行时结论的那一段 (`## Impact` 「自主运行时 (v2.0 Layer 2)」整段, 含 S_FAIL/`container_crash`/不自动重试/不告警/`fail_detail` 一句) 在 diff 里是纯上下文行 (无 `+`/`-`), 一字未改; 唯一改动是同段前一行把「RESULT.md v7」的版本号引用改成「RESULT.md v8」, 与运行时机制描述无关。
- `git diff 15ab323 a563192 --stat -- aria-orchestrator/` 零输出 —— 本席 R7 逐行核对过的 `extension.py`/`reconciler.py`/`reconcile_runner.py` 在这个区间零改动, R7 的「机制核实记录」里的行号引用继续有效。
- 垫片 (`claude-shim.sh`) 与 `classify_calls.py`/`fake-claude` 三个文件 `git diff 15ab323 a563192 --stat` 均零输出 (逐一确认, 见「机制核实记录」), R7 对垫片 query 解析 / PID kill 语义 / stdout EOF 时机的评估继续有效。

结论: R7 对账 closed 0 / partially 0 / open 0 (本席无条目); v9 的四处改动与本席已验证的运行时结论无交集, 无需重新验证。

## Findings

- [major] documentation/proposal.md §D2+SC-12 (issue): SC-12 新增的锚点只覆盖 SOT §2 侧「不做 description 改动 (含新增 skill)」句 (第 41 行); R7 major#3 同时点名的手册侧对应句 (D2 第 58 行「新增 skill 的首个 description 同样要过本场景, 其首个套件随之建立」) 仍无任何 SC 锚定 —— 通读 SC-1 到 SC-13 全文, 无一条引用该句或「首个套件」; 转录 D2 到手册时若漏写或改写掉这句, 没有 SC 会转红。owner 裁定「三条 major...现在就改」, 但本条只改了一半。
- [major] testing/RESULT.md §v6 加固记录 (issue): RESULT v8 新增一句「归档在 `fault-matrix/` 与 `fault-matrix-counterfactual/` 的就是加固后重跑的产物」, 但 `git log -1 -- <path>` 显示两个目录下的 `matrix-summary.json` 最后改动都是 R7 之前 (2026-09-15 `76959c8`), a563192 未触碰; `fault-matrix-counterfactual/` 目录里唯一的文件就是这个 `matrix-summary.json`, 即该目录没有任何文件被 a563192 改过。`fault-matrix/` 下只有 22 个 `<tag>.classify.json` 报告文件被 a563192 改过 (内嵌新的日志文件名/耗时, 证实确有一次真实重跑), 但同目录的 `.json`/`.err` 原始输出与 `matrix-summary.json` 本身未变。数值本身 (0/24 与 5/24 不符、5 个用例名) 经本席独立重跑复核仍正确 (见机制核实记录), 但「就是加固后重跑的产物」这句对 `matrix-summary.json` 不成立, 对 `fault-matrix-counterfactual/` 整体不成立。

## 观察

- **独立端到端重跑复现结论**(本轮新做, 非转述): 把加固后的四个工具文件复制到 scratchpad, 用 `--suite` 指向基线套件真实执行 `fault_matrix.py` (非模拟): 24 用例、0 不符、退出码 0, `matrix-summary.json` 逐字段与归档版本比对一致; 再复制一份 `classify_calls.py` 删掉「result 帧报错」判定 (`if ev.get("is_error")...: errored = True` 改 `pass`) 重跑: 24 用例、5 不符、退出码 1, 不符用例名 (`F1_result_error`/`S1_overbroad_fault_in_shouldnot_half`/`S2_correct_fault_on_one_should_query`/`S8_two_run_fault_should`/`S10_negctrl_two_run_fault_x6`) 与归档 `fault-matrix-counterfactual/matrix-summary.json`、RESULT.md、SC-13 逐字吻合。这证明加固改动 (`--out` 处置) 对分类逻辑零影响, 且底层结论本身确实可复现——上面的 major 只是「归档文件是不是这次重跑写出来的」这一层溯源声明有问题, 不是数字本身有问题。
- **直接复现 R7 minor 报的场景**: 在一个有文件的临时目录里对加固后的 `fault_matrix.py` 跑 `--out .`, 输出「输出目录已存在且非空, 请换一个 --out」, 退出码 2, 目录内原文件毫发无损——R7 minor 点名的「`--out .` 会删空当前目录」场景已被正确堵住。
- **matrix-summary.json 与逐条 `<tag>.classify.json` 的形状差异先做了排除**: 前者是 `classify_calls.py` 打到 stdout 后被 `fault_matrix.py` 解析进汇总表的精简 JSON (只有计数/结论字段, 没有 `calls` 明细列表), 后者是 `--report` 落盘的完整报告 (含每次调用的文件名/耗时明细)。两者形状本来就不同, 不能因为 `matrix-summary.json` 里没有 `calls` 明细就断言它「缺 calls 数据」——真正的判据是 git 历史 (谁在哪次提交动过这个文件), 不是内容形状对比; 这一步排除避免了一次误判。
- **T2b / T4「搬」→「复制」的修法做了全文件扫描**: `grep -n "搬" proposal.md` 零命中, 确认没有遗漏的旧措辞; 且 T2b/T4 现在都点名了各自依赖方 (SC-13/D3 前置表第 3 行、SC-4), 与 SC-2 (`test -e` 要求基线文件还在)、SC-4 (`diff` 要求基线文件还在)、SC-13 (`cmp` 要求基线文件还在) 三条判据的前提一致, 无内部矛盾。
- **SC-9 两个新锚点用反事实验证有效**: 写脚本模拟 SC-9 的复合判据 (需排除 proposal.md 里 SC-9 自身定义那一行的自引用, 否则该行会自我满足全部锚点词造成假绿——这是所有 grep 类 SC 直接对 proposal.md 模拟时的通病, 真实执行目标是转录后的手册/SOT 文件, 不含 `- SC-` 行, 不受此影响, 非 v9 新引入的问题)。排除自引用后: 真实 v9 文本全绿; 把「作废」行的括号语义悄悄改回 R7 否定的旧规则「即存在任一次不健康的调用」, 转红; 把 `classify_calls.py` 那一行的「两种可能」措辞替换掉 (保留大意), 也转红。两个新锚点都按预期工作。
- **SC-12 新锚点本身 (SOT 侧) 验证通过**: SOT 新句第 41 行原文含「不做 description 改动 (含新增 skill)」, 「含新增 skill」与其余五个锚点词同在一行, 去掉括号内容会使该锚点单独转红 (字符串包含关系直接可判, 未见反例)。这部分修复正确, 只是覆盖面不够 (见 Findings)。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 2 major / 0 minor。

## Vote

REVISE

## 机制核实记录

- `git diff 15ab323 a563192 -- openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md`(全文, 非片段) 与 `... -- aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/RESULT.md` 全文核对四处改动的确切文本。
- `git diff 15ab323 a563192 --stat`(整个仓库) 核对本次 v9 commit 实际触碰的文件集合 (68 个文件, 含大量并发容器合并进来的 `handoff-multibranch-subdir-path-fidelity` 审计报告与 `#195 A.2/A.3` 材料, 与本 Spec 无关, 已排除)。
- `git diff 15ab323 a563192 --stat -- aria-orchestrator/`、`.../claude-shim.sh`、`.../classify_calls.py`、`.../fake-claude` 均零输出, 逐一确认 (支持「R7 对账」结论)。
- 完整读 `fault_matrix.py` 加固后的 diff (7 行) 与全文 (176 行), 确认新逻辑: `out` 存在且非空 → 打印错误、返回 2; 不存在 → `mkdir(parents=True)`; 存在且为空 → 直接进入子目录创建 (安全, 因为空目录意味着子目录必然不存在, 不会撞 `FileExistsError`)。
- **独立重跑 A (加固后脚本, 正常)**: 复制四工具到 `/tmp/.../scratchpad/r8-backend-architect/tool-copy/`, `python3 fault_matrix.py --suite <基线套件> --out <scratch>/fm-normal` → 24 用例、0 不符、退出码 0; 逐字段比对 `matrix-summary.json` 与归档版本一致 (含 `F1_result_error` 行的 `classify` 子对象完全相等); `.json`/`.err` 原始输出与归档版本 `diff` 零输出 (证实 `fake-claude` 行为确定性, 与是否重跑无关)。
- **独立重跑 B (加固后脚本, 反事实)**: 复制一份 `classify_calls.py` 到 `tool-copy-counterfactual/`, 把 `if ev.get("is_error") or str(ev.get("subtype","")).startswith("error"): errored = True` 改成 `pass`(仅此一处), 重跑 → 24 用例、5 不符、退出码 1, 不符用例与归档 `fault-matrix-counterfactual/matrix-summary.json` 的 5 条逐一相同。
- **溯源核查**: 对 `fault-matrix/` 与 `fault-matrix-counterfactual/` 目录下每个文件跑 `git log --format='%h %ad' -1 -- <file>`: `fault-matrix/` 下 22 个 `<tag>.classify.json`(不含 F8/M1) 显示 `a563192 2026-09-17`, 其余全部文件 (`.json`/`.err`/`matrix-summary.json`/F8 与 M1 的 classify.json) 与 `fault-matrix-counterfactual/matrix-summary.json` 均显示 `76959c8 2026-09-15`(早于 R7)。逐字段比对 `matrix-summary.json` 内嵌的 `classify` 子对象 (F1 行) 与独立重跑结果完全相等, 排除「内容形状不同致误判」后确认这是溯源 (谁写的) 问题, 不是数值 (对不对) 问题。
- **R7 minor 场景复现**: `mkdir` 一个非空临时目录, `cd` 进去后对加固后的 `fault_matrix.py` 跑 `--out .`, 得到「输出目录已存在且非空, 请换一个 --out: .」与退出码 2; `ls` 确认目录内原有文件未被触碰。
- **SC-9 反事实模拟**: 写 `check_sc9_v2.py`(排除 `- SC-` 自引用行) 对 (1) 真实 v9 文件、(2) 把「作废」行括号语义改回旧规则、(3) 把「两种可能」替换掉 三个版本各跑一次, 结果分别为 绿 / 红 / 红, 与 SC-9 意图一致。
- **SC-12 覆盖面核查**: `grep -n "新增 skill" proposal.md` 列出全部 4 处出现 (Why 段 1 处、D1 表新句 1 处、D2 正文 1 处、SC-12 定义 1 处、OQ-9 讨论 1 处, 共 5 处); 通读 `## Success Criteria` 整节 (SC-1 至 SC-13 全文), 确认只有 SC-12 引用「新增 skill」且只锚定 D1 表新句 (SOT 侧), D2 正文那一句 (手册侧) 无 SC 引用。
- `grep -n "搬" proposal.md` 零命中 (T2b/T4 修法的完整性扫描)。
