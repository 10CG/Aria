---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T12:10:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 1
minor_count: 2
---

## 摘要

对 v4 (R3-fix) 做 R4 (max_rounds 末轮) 复核, 全部结论基于 `aria @ 400f0bc` 实读代码 (`pre_merge_gate.py:160-527` / `_sanitize_for_json:292-299` / `gate_state_helper.py` 全文) 逐字对照 v4 伪码, 不采信 spec 文本自述。

结论: 我在 R3 报的三条 Major (verify_note 作用域 / empty-diff 分支名无数据源 / CLI 对文件缺失未定义) 与两条 Minor (SC-11(d) 独立重读 / 包装丢 timeout 默认值) **全部真实收敛**, 逐字核对无残留。但本轮新鲜眼睛发现一处**新引入**的机制层缺口: v4 为响应 R3 簇 #5 新增了 `DISPATCH_VIABLE` 模块常量 + `dispatchable_workflows` 驱动的 dispatch 处方行渲染逻辑(嵌进 `_no_run_gate_error` 的 `workflow-trigger-matched` 档), 但整个 SC 表(SC-1~SC-16)里**没有任何一条**断言这段渲染逻辑的存在/内容/basename 用法——SC-2 只测 `workflow-trigger-matched` 档含 `#152` + 全部 matched 名, 从不触碰 dispatch 行本身; SC-8/SC-9 测的是 `path_coverage.py` 里 `dispatchable`/`dispatchable_workflows` 字段的生成, 不是 `pre_merge_gate.py` 里 `_no_run_gate_error` 对它们的消费。这正是"两实施者必然分叉且无 SC 能区分"的量级: 一个实现者可以完全跳过 dispatch 行渲染(当作可选装饰), 另一个可以重犯簇 #5 本身要修的那个 basename bug(逐字拼 `.forgejo/workflows/x.yml` 而非 basename), 全套 SC 无一变红。属新引入(v4 才有 `DISPATCH_VIABLE` 机制), 非 R1-R3 已报条目的重复。另有 2 条 Minor(均为"结构上不可达但未显式声明"类, 防御性质)。

## R3 处置核对

| 簇# | 内容(节选) | 状态 | 证据 |
|---|---|---|---|
| 3 (含 A2-R3-M1) | §2.1 `verify_note` 作用域 / §2.2 `gate_error` 分支外读取 UnboundLocalError; verify-failed `detail` 绕过 `_sanitize_for_json` | **closed** | v4 §2.1 在 `if pr_status.state == "not_found":` **之前**加 `verify_note = ""` 哨兵(逐字核对 `pre_merge_gate.py:508-527` 真实插入点, 现状代码 `pr_status = backend.query_pr_ci(pr_branch)` 后直接 `return compute_verdict(...)`, 插入位置与 R3 anchoring 一致); §2.2 明写"`gate_error` 在函数开头初始化为 None", 即紧邻真实 `compute_verdict` 现有的 `raw_message = ""`(`:196`)一行, 覆盖所有 elif 分支包括未改动的 `failing/error/pending/passing` 路径。`verify_note` 赋值改为 `_sanitize_for_json(f" (PR 分支存在性核验失败: {detail})")`——整个后缀经过消毒函数(逐字核对 `_sanitize_for_json`(`:292-299`, `encode("utf-8","replace").decode("utf-8")`)与既有 main 分支消毒同款用法(`:464` `msg = _sanitize_for_json(msg)`)一致, 不是新造的消毒方式) |
| 5 (DISPATCH_VIABLE 机制本体, 非渲染覆盖) | `dispatch_viable` 运行时不可达; `dispatchable_workflows` 相对路径拼 URL 会 404 | **partial** | 机制本体(模块常量 + `_no_run_gate_error` 内 `DISPATCH_VIABLE and dispatchable_workflows` 条件 + basename 要求)在 §2.3/§3.5 文字层面已写清, 但**零 SC 覆盖这段渲染逻辑**——见新 Finding A2-R4-M1, 判 partial 非 closed |
| 6 (含 A2-R3-M2) | `empty-diff` 档 `<main>...<pr>` 占位无数据来源 | **closed** | v4 §2.3 表已改「main…PR 三点 diff 为空, 无变更可跑; 远端零 run」——逐字确认**不再带尖括号占位符**(对比同表其余仍用 `<下表>`/`<obs>`/`<elapsed_seconds>` 风格的真替换占位), 现在是纯字面固定文案, 不需要任何签名携带分支名; 三层签名(`compute_verdict`/`_no_run_gate_error`/`path_coverage._result()`)确实都不携带分支名(与我 R3 实测一致), 但因为不再需要替换, 数据源问题结构性消失 |
| 7 (含 A2-R3-M3, A2-R3-m1) | CLI 对 state 文件缺失未定义行为(`load_state`→`None`→`AttributeError`/`TypeError`); SC-11(d) 未独立重读 | **closed** | v4 §3.1 明写 `record` 在 `verdict=wait` 且文件不存在时"先创建骨架 `{"format_version": "1.1", "gate_state": null}`"——实读 `gate_state_helper.py:145-155` `write_gate_state` 的 `existing = state.get("gate_state") or {}` 对该骨架安全(不会 AttributeError); `atomic_write_state`(`:86-101`)对全新文件路径也安全(`os.makedirs(...exist_ok=True)`覆盖目录不存在场景); `reset`/`clear` 对缺失文件 exit 2, 消除了 `clear_gate_state`/`reset_no_run_observations` 对 `None` 输入的裸崩溃路径。SC-11(d) 现在明写"**独立重读**落盘文件断言 `gate_state.no_run_observations == 2`"且专门点名"stdout 自洽未落盘"这类双记账坏实现必红——闭合我 R3-m1 |
| 10 (含 A2-R3-m2) | `_verify_main_branch_exists` 包装丢失 `timeout` 默认值 | **closed** | v4 §2.1 包装字面代码已补全: `def _verify_main_branch_exists(main_branch, remote, timeout=_LS_REMOTE_TIMEOUT): return _verify_branch_exists(main_branch, remote, timeout)`——默认值与基线原函数签名(`:303` `timeout: int = _LS_REMOTE_TIMEOUT`)逐字一致 |
| 1/2/4/8/9(非我 R3 主责簇, 快速核验) | 运行时探针形态 / CLI 签名 / 时间轴 / 版本引用点 / NEG-3 执行 | 表面 closed(spec 文字已按 R3 处置表逐条改写, 未做独立深度实读复算——留给 A1/A3/A4/A5 各自 owner 簇) | 未发现与我的 A2 视角(schema/API/性能)冲突的残留问题 |

## 新 Findings

### [A2-R4-M1] Major — `DISPATCH_VIABLE`/`dispatchable_workflows` 驱动的 dispatch 处方行渲染逻辑, 全 SC 表零覆盖, 两实施者必然分叉且不可区分

**锚点**: proposal §2.3 message 表 `workflow-trigger-matched` 行(`「变更 path-matched … 但远端零 run …」; **当 `DISPATCH_VIABLE and dispatchable_workflows`** 追加处方行: 每文件一行 `forgejo POST /repos/{o}/{r}/actions/workflows/<basename(file)>/dispatches -d '{"ref":"<pr_branch>"}'`(路径取 **basename** …)`) + §3.5(`DISPATCH_VIABLE` 模块常量落点) + SC 表全表(SC-1~SC-16)。

**问题**: `_no_run_gate_error(path_coverage, threshold)` 现在内部需要读取一个模块级常量(`DISPATCH_VIABLE`)并对 `path_coverage.get("dispatchable_workflows")` 做条件渲染(含 `os.path.basename()` 提取), 这是 v4 才新增的分支(v3 没有, 是本轮 R3 簇 #5 fix 引入的机制)。但逐一核对 SC 表:

- SC-2(`compute_verdict` 参数化 8 reason + None)对 `workflow-trigger-matched` 档的内容断言只有「含 `#152` + 全部 matched 名」, 从未断言 dispatch 行的存在、格式或 basename 用法——`DISPATCH_VIABLE=True` 与 `DISPATCH_VIABLE=False` 两态下跑同一条 SC-2 用例, 断言结果完全相同(因为断言是"contains", dispatch 行加不加都满足)。
- SC-8(`_parse_workflow` 的 `dispatchable` 字段)与 SC-9(`evaluate_path_coverage` 的 `dispatchable_workflows` 字段)测的是 **`path_coverage.py`** 模块的数据生成, 不是 **`pre_merge_gate.py`** 里 `_no_run_gate_error` 对这些数据的**消费**。两者是调用链上下游不同的函数, 后者的正确性不能由前者的 SC 担保。
- SC-14(文档机检)是纯文本 grep, 不执行代码, 不可能验证 basename 提取逻辑。
- rule6_note 讨论的 AB 套件覆盖(§3.2/3.3)针对的是 workflow-runner 的 prompt 触发行为, 不是 `pre_merge_gate.py` 内 message 字符串的构造细节。

结果: 全套 SC 对"dispatch 行到底有没有被正确渲染进 message"这件事**零红窗**。两个独立实现者面对同一份 v4 文本, 一个可以完全不实现这段条件渲染(把它当成锦上添花跳过), 另一个可以实现但重犯簇 #5 本身要根治的 bug(逐字拼 `.forgejo/workflows/x.yml` 而非 `basename(file)`, 导致 §3.3 处方文案里的 dispatch 命令 404) —— 两者跑 SC-1~SC-16 全绿, 无法区分。这正是 memory `feedback_spec_underdetermination_two_implementer_test` 描述的形状, 也是本 spec 自己反复标榜的"可证伪; 每条能答「它怎么会红」"原则在这一处未被自己满足。

**实测证据**: `grep -n "dispatch\|DISPATCH"` 全文核对(见上锚点), SC 表逐行读取确认 SC-2/SC-8/SC-9/SC-14 措辞不含 dispatch 行相关断言。

**建议**: 在 SC-2 追加一条子项(或新增 SC-2b), 参数化 `DISPATCH_VIABLE` 的 True/False 两态 × `dispatchable_workflows` 非空/空 两态, 断言: (a) `DISPATCH_VIABLE=True` 且非空时, message 含形如 `.../actions/workflows/<basename>/dispatches` 的行, 且**不含**完整相对路径 `.forgejo/workflows/`(防回归簇 #5 的 basename bug); (b) 其余三种组合(False, 或非空但 False, 或 True 但空列表)message **不含** `dispatches` 子串。§3.5 已写明"若 TASK-0a 结果为 false, §4 整段 + SC-8/SC-9 dispatch 部分从本 spec 删除"——若 owner/实现者按此路径走, 新增的 SC-2b 也应随之删除(与 §4 同一条件 scope), 不会造成"true 才需要的 SC 在 false 世界里恒红"的假红问题, 因为该子项本就整段跟随 dispatch_viable 结果一起进退。

## Minor Findings

### [A2-R4-m1] Minor — CLI `record` 对 `verdict != wait` 且 state 文件缺失时的行为未显式定义

§3.1 只写"state 文件不存在**且 verdict=wait** 时先创建骨架"。按 §3.2 描述的调用序列(首次 `record` 恒在首个 wait verdict 时触发, 见步骤 2), `record --verdict green` 或 `--verdict fail` 撞上文件缺失在现有文档描述的调用点下结构上不可达。但 §3.3 承认"交互式直调 §C.2.4(无 workflow-runner)"是被认可的使用形态, 若有人在这种直调场景下把 `record` 当独立工具首次调用且 gate 直接给出 green/fail(未经过 wait), 现有描述没有兜底(沿用 `write_gate_state`/`load_state` 现状会 `AttributeError`)。建议顺手补一句"非 wait 且文件缺失 → exit 2, 语义同 reset/clear", 消除对"record 恒先以 wait 触发"这一隐含调用序列不变量的依赖。

### [A2-R4-m2] Minor — CLI `reset --retry-count` 无对应具名 helper 函数, 与 `reset_no_run_observations` 的显式具名模式不一致

`gate_state_helper.py` 改动清单具名列出了 `reset_no_run_observations(state)`, 但 `reset --retry-count` 对应的字段重置未给出对应函数名(Impact additive 函数列表同样未列出)。实现者大概率会在 CLI 层内联 `state["gate_state"]["retry_count"] = 0`, 功能上可行, 但与 `no_run_observations` 走独立可测试函数的模式不对称。建议要么补一个 `reset_retry_count(state)` 具名函数保持对称, 要么在 §3.1 明写"两个 reset 目标均走 CLI 内联赋值, 不新增 helper 函数", 消除风格假设。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 1 Major / 2 Minor)

vote: **REVISE** — 我在 R3 报的全部 3 条 Major + 2 条 Minor 均已真实收敛(逐字核对哨兵初始化位置、消毒函数复用、包装默认值、CLI 骨架创建与独立重读断言, 均与真实代码/真实基线签名吻合, 非采信 spec 自述)。但 v4 为响应 R3 簇 #5 新引入的 `DISPATCH_VIABLE` 渲染机制在全套 SC 表里零覆盖, 满足"两实施者必然分叉且无 SC 能区分"的 Major 门槛, 且与本 spec 自身反复强调的"可证伪"设计原则相悖。修法局部(SC-2 追加一条参数化子项, 且天然与 §4/SC-8/SC-9 共享同一条件 scope, 不产生新的假红面), 不牵动 owner 已裁定的 A′ 设计或 v3/v4 的任何结构决定, 预期一轮内可收敛。
