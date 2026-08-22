---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T07:37:37.191Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 8
minor_count: 4
---

# post_spec R2 — A4 code-reviewer 席 (spec 与代码逐行对照 / 引用准确性 / 实施者分叉点 / 回归面 / 文档同步面)

审计对象: `openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md` (Draft v2, R1-fix)
基线: aria @ `400f0bc` (实核 `git rev-parse --short HEAD`, 工作树干净); 基线测试复跑 **119 passed** (phase-c) + **22 passed** (gate_state_helper) — SC-12 计数准确。

## 摘要

v2 把 R1 的 Critical (重复处方无守卫) 与四个欠定点 (计数量 / 判定单点 / 消歧 / 同步面) 都落成了具体条款, 方向正确, 行号引用 (phase-c SKILL `:46-54` / `:172-183` / `:175` / `:180` / `:241` / `:248-263` / `:276-290` / `:288` / `:290` / `:292-302`; `pre_merge_gate.py` `:174-233` / `:181-194` / `:253-256` / `:302-352` / `:498-506` / `:418` / `:434` / `:455` / `:458` / `:489` / `:512`; `aether.py:225-226`; `test:363`; workflow-runner `:313` / `:326` / `:332-336` / `:389`; schema `:110-131` / `:125`; config.template `:73-91`) **逐条核对全部准确** (唯 `:362` 是 `if` 行, return 在 `:363`, 无实害)。F1-F6 事实未变, 本席未再复跑网络探针 (R1 三席已独立复跑, v2 未改主张)。

R2 剩下的问题全是**接缝型**: 多簇 fix 各自成立, 合在一起后在四处产生新的实施者分叉 —— (1) 计数搬进 helper 解决了「谁自增」, 但「2.5 判定在写入前还是后」原样保留 (R1 #2 的 90s-vs-210s 分叉换了个位置复发); (2) `_verify_branch_exists` 别名方案按字面不可实现 (既有调用点关键字 `main_branch=` 直接 TypeError; 改调用点则 28 个 mixin 打桩测试失效); (3) §2.1 伪码硬编码 `verdict=WAIT` 与 §2.3 `pr-branch-not-found → fail` 互斥, 且 `pr_branch_check: dict` 与函数返回的 tuple 形状不一致; (4) 升级后的状态回写只写了「处方成功」一个出口, 处方落到 prompt / prompt 后 continue 两个出口与既有 `:356` 「continue → reset retry_count」交互会变成每个 interval 重复弹窗。另 TASK-0 与 SC-13「合并执行」在时序上不可执行 (SC-13 需要新代码, TASK-0 是前置)。无 Critical, 无 Rule #8 fail-open 方向的问题。

## R1 处置核对

| 簇# | 状态 | 证据 |
|---|---|---|
| #1 (A4-C1) | **closed** | §3.1 `no_run_observations` + `no_run_escalation_done`; `mark_no_run_escalation_done` 不触碰 `started_at`/`retry_count`/`next_check_at` (SC-11c 坏实现=`clear+write` 必红, 对照 helper `:158-161` 确实是唯一归零路径); §3.2 2.6 再命中交人; AD-4 「误升级代价有界」成立。残余接缝 (prompt 后出口) 见 A4-R2-M4, 不重开 |
| #2 (A4-M1) | **partial** | 计数单点 = `write_gate_state` ✅ 解决「谁自增」; 但 2.5 读 `state` 是写入前还是写入后仍未钉 — workflow-runner SKILL `:351-352` (3.c 重调 gate → 3.d 按 exit conditions 处理) 与 `:389` (wait → 增量更新) 的自然读法是**先判后写** ⇒ t=90 时 obs 仍为 2, 升级落到 t=210; 见 M1 |
| #5 (A4-M3) | **closed** | §3.2 2.5 唯一判定 + `should_escalate_no_run` 唯一机械实现; §3.3 步骤 6 只做 surface + 承载处方, 「入口仅为 2.5 转入」✅ |
| #6 (A4-M6) | **closed** | §2.2 按 `(decision, reason)` 5 档封闭表 (对照 `path_coverage.py:459/:464/:493` matched 恒 [] 的两档各自有文案) ✅; `:290` 改三类在场条件 ✅; SC-5 拆 enabled/disabled ✅。同形复发于新条款 §2.3 (ii) 见 m2 |
| #9 (A4-M5) | **partial** | 第三行 + 点名行为 + `NEG-4` + 缺口 issue 三义务 ✅, 7 fixtures 计数 ✅, NEG-3 先例引用逐字属实 (`_description` 实读)。未落: suite json `fixtures[]` 注册 / `test_case_in_unit_tests` 指向 / 缺口 issue 实为已开的 aria-plugin **#127**; 见 M7 |
| #10 (A4-m5) | **closed** | SC-13 「轮询至非 not_found 或 600s」+ Δt 记录 ✅ |
| #11 (A4-M7) | **partial** | TASK-0 两结果各写了落点 ✅ (memory 内容实读: 「`workflow_dispatch` API 在 gitea-1.22 系不可用」与 F6 互斥属实)。但失败分支的连锁 (§4 / SC-8 / SC-9 / SC-2 remedies 表 / AD-4 文案) 未列, 且与 SC-13 的执行时序矛盾; 见 M5 |
| #12 (A4-m2) | **closed** | §2.1 伪码标注插入位置 + 防呆注释 ✅ (对照 `:219 elif main_in_flight_runs` 确实不检查 pr_ci_status); SC-4 红窗改「在 kind」✅ |
| #13 (A4-M4 + A4-M2) | **partial** | 14 处逐行号全部准确 ✅; `write_gate_state(gate_error_kind=)` 入参 ✅; `format_version` 不 bump + 防御 `.get()` ✅ (helper 测试无整 dict 相等断言, additive 键安全; `grep gate_state --include=*.py` 仓内无其他消费方)。仍漏 4 处: 见 M8 |
| #17 A4-m1 | **closed** | `:276` ✅ / fixtures 7 ✅ / 「首次 gate 调用后 ~90s」✅ |
| #17 A4-m3 | **partial** | 子串闭集 (`#152` / `no-run-for-branch`) ✅; 但「校验只在 `gate_check`」与 SC-3 直调 `compute_verdict` 互斥, `DEFAULT_CONFIG` 加键未列; 见 M6 |
| #17 A4-m4 | **closed** | SC-7 七落点 + 「main 核验两 kind 为七键」✅ (`:465-472` 实核) |
| #17 A4-m6 | **closed** | §2.2 第二行「禁扩成全量 workflow 列表」✅ |

小计: closed 8 / partial 5 / not_addressed 0 (按簇计: closed 6 / partial 4, #17 内部四条分计)。

## 新 Findings

### [A4-R2-M1] Major — 2.5 判定相对 `write_gate_state` 的先后未钉, R1 #2 的 90s/210s 分叉原样复发

- **锚点**: §3.1 「仅此函数自增/归零 (单一计数点 — 解决 R1 #2 的『自增在 verdict 前/后』欠定)」; §3.2 2.5 `should_escalate_no_run(state, …)`; §3.3 config 「默认在首次 gate 调用后 ~90s: 初次 t=0 + 重查 #1 t≈30 + 重查 #2 t≈90」; workflow-runner SKILL `:351-352` / `:389`
- **问题**: 计数点单一只回答了「谁自增」, 没回答「2.5 读的是自增前还是自增后的 state」。SKILL 既有流程 `:351 c. 重新调 gate → :352 d. 处理 verdict 按 exit conditions` 再到 `:389 wait → 增量更新 retry_count`: 写入是「处理 verdict 为 wait」的后果, 自然落在 exit conditions **之后**。按此顺序: t=0 写 obs=1; t=30 判 (obs=1) 再写 obs=2; t=90 判 (obs=2, 不升级) 再写 obs=3; t=210 判 (obs=3) 才升级。AD-4 的「~90s」与 SC-3 的阈值 3 都按「先写后判」算。两实施者各按一种顺序实现, SC-11 (只测 helper) 对此分叉**两边都绿**。
- **钉法**: §3.2 开头加一句: 「每轮 gate 返回后**先** `write_gate_state(..., gate_error_kind=gate_error.kind)` **再**评 exit conditions; 2.5/2.6 读写入后的 state (含初次: 首次 wait 写 obs=1)」; §5 workflow-runner 行加 `:352` (3.d 前插 3.c′ 写 state) 与 `:389` 文案同步; 加 SC-11(e): 「按 SKILL 顺序模拟 3 轮 (写→判), 第 3 轮 `should_escalate_no_run` 为 true; 按『判→写』模拟为 false」—— 这条测的是散文顺序, 用 helper 组合复现即可。

### [A4-R2-M2] Major — `_verify_branch_exists` 「泛化 + 旧名别名 + 既有调用/测试不改」三者字面不可同时成立

- **锚点**: §2.3 「泛化为 `_verify_branch_exists(branch, remote, timeout)` (旧名保留为别名, 既有调用/测试不改)」; `pre_merge_gate.py:449-453` 既有调用以关键字 `main_branch=main_branch` 调用; `test_pre_merge_gate.py:85-89` `_ProbeCacheResetMixin` 按名 `gate._verify_main_branch_exists` 统一打桩 (docstring `:66-72`: 28 处既有测试经此, 单次真 ls-remote 8.7s)
- **实测** (scratchpad `alias_demo.py`): (a) `_verify_main_branch_exists = _verify_branch_exists` 且参数改名为 `branch` ⇒ `:449` 关键字调用 **`TypeError: unexpected keyword argument 'main_branch'`**; (b) mock 语义: patch 旧名**不**拦截经新名的调用 (两个模块属性各自绑定)。于是实施者 A (调用点改调新名) ⇒ 28 个 mixin 测试失去打桩, 套件从 4s 变分钟级且随网络漂移, 「测试不改」被迫破; 实施者 B (调用点保留旧名、仅 PR 核验调新名) ⇒ 「泛化」只是名义, 且 SC-5 须同时 mock 两个名。SC-10 的「`_verify_branch_exists` 对 pr_branch `assert_not_called`」只在 B 方案下有意义 (A 方案同一 mock 也承载 main 调用, `assert_not_called` 恒红)。
- **钉法** (字符级): 「`_verify_branch_exists(branch, remote, timeout)` 为新主体; 旧名定义为**包装函数** `def _verify_main_branch_exists(main_branch, remote, timeout=_LS_REMOTE_TIMEOUT): return _verify_branch_exists(main_branch, remote, timeout)` (保关键字签名); `gate_check` `:449` main 调用点**字面不改**; PR 核验调用 `_verify_branch_exists(pr_branch, remote, timeout)`; 打桩点: main 仍 `gate._verify_main_branch_exists` (mixin 不动), PR = `gate._verify_branch_exists`; SC-10 对新名 `assert_not_called`, SC-5 两名同 mock」。

### [A4-R2-M3] Major — §2.1 伪码 `verdict = VERDICT_WAIT` 硬编码与 §2.3 `not-found → verdict=fail` 互斥; `pr_branch_check` 类型与 `_verify_*` 返回形状不一致

- **锚点**: §2.1 伪码 `elif pr_ci_status == "not_found": verdict = VERDICT_WAIT; gate_error = _no_run_gate_error(path_coverage, cfg, pr_branch_check)`; §2.1 「签名 additive 加 `pr_branch_check: dict | None = None`」; §2.3 表 `not-found` 行 `verdict=fail` + `kind=pr-branch-not-found` + `path_coverage` 在场; `pre_merge_gate.py:302-352` 返回 `tuple[str, str]` = `(status, detail)`, status ∈ {`ok`, `not-found`, `verify-failed`}
- **问题**: 三处分叉。(i) 谁产 `fail`: 按 §2.1 在 `compute_verdict` 内 verdict 恒 WAIT, `_no_run_gate_error` 只产 gate_error ⇒ `pr-branch-not-found` 会以 `verdict=wait` 输出; 按 §2.3 应 fail。实施者 A 在 `gate_check` 查到 `not-found` 就早退 `_build_output(fail, …)` (不进 compute_verdict, `pr_branch_check` 只剩 ok/verify-failed 两值); B 在 `compute_verdict` 内分支。(ii) `pr_branch_check` 声明 `dict`, 源头是 tuple, 转换键名未定 (`{"status","detail"}`? `{"kind","detail"}`?) — SC-10 直接 mock `_verify_branch_exists` 返 tuple, 但 compute_verdict 直调 (SC-2/SC-4) 传 dict, 两套 fixture 形状不同。(iii) `None` 的语义 (未核验 ≡ ok? 还是 ≡ verify-failed 附注?) 未写; SC-2 不传该参数却期望纯 `no-run-for-branch` 文案 ⇒ 隐含 None ≡ ok, 应明写。另: `pr-branch-not-found` 的 `gate_error` 是 2 键 (`{kind,message}`, 与 main-* 同形) 还是 4 键 (含 `escalate_after_observations`/`remedies_available`)? `in_flight_runs` 取已查得的 (b) 轴结果还是 `[]`? 均未钉, SC-10 不断言。
- **钉法**: 选 A (推荐, 与 `:454-472` main 早退同形): 「`gate_check` 在 `pr_status.state == "not_found"` 时调核验; `not-found` → **直接** `_build_output(verdict=fail, pr_ci_status="not_found", in_flight_runs=in_flight.runs, path_coverage=pc, gate_error={"kind":"pr-branch-not-found","message":msg}, raw_message=msg)` 早退 (2 键 gate_error, 与 main-* 同形; 这是**第八个早退落点**, SC-7 计数 7→8); `ok`/`verify-failed` 才进 `compute_verdict(..., pr_branch_check={"status": s, "detail": d})`; `pr_branch_check=None ≡ {"status":"ok"}`」。§2.1 伪码随之只处理 wait 两变体。

### [A4-R2-M4] Major — 升级状态回写只钉了「处方成功」一个出口; prompt 出口与 `:356` continue 语义交互后会每个 interval 重复弹窗

- **锚点**: §3.2 2.5 「执行后 `mark_no_run_escalation_done`」; 2.6 「user prompt (与 exit 2 同级: continue / abort)」; §3.3 处方 3 「user prompt (与 2.6 同形)」+ 「任一 4xx/5xx → 视为处方 1 失败, fall through 2」; workflow-runner SKILL `:356` 「timeout → user prompt; continue → reset retry_count + 继续」; helper `:139-140` retry_count 只在 waiting→waiting 递增
- **问题**: (i) 2.5 命中但 remedies 落到处方 3 (`[]` 或 1/2 皆 fall through) 时是否调 `mark_…`? 不调 ⇒ done 仍 false、obs ≥ 阈 ⇒ 下一轮 2.5 再命中 ⇒ 再 prompt; 调 ⇒ obs 归零, 3 次后 2.6 再 prompt。两实施者不同。(ii) 2.6 / 处方 3 的 prompt 选 continue 后 `no_run_observations` 怎么办? spec 沉默。若沿 `:356` 只 reset `retry_count`: obs 仍 ≥ 阈且 done=true ⇒ **每个 interval (30s 起) 都命中 2.6 重新弹窗**, 直到 timeout; 若顺手把 obs 归零则 ~3 个 interval 后再弹。这是 R1 #1 「重复动作」的 prompt 版, 不是 fail-open 但在无人值守 (R-d) 下等同死循环 abort。(iii) 处方 1 对多个 `dispatchable_workflows` 逐个 POST, 「任一 4xx/5xx → fall through 2」: 两个 2xx + 一个 4xx ⇒ 已建 2 个 run 还再推 commit (重复动作)。
- **钉法**: 「(a) 2.5 转入后**无论落到哪条处方 (含 3)** 都调 `mark_no_run_escalation_done` 恰一次; (b) 2.6 / 处方 3 prompt 的 continue = `no_run_observations=0` (helper 加 `reset_no_run_observations(state)` 或让 `mark_…` 幂等再调), **不** reset `retry_count` (与 exit 2 的 continue 不同, 明写差异); abort = stop; (c) 处方 1: 至少一个 2xx ⇒ 视为已执行, 不 fall through; 全部非 2xx 才 fall through 2」; SC-11 加 (e)(f) 两条对应断言 (坏实现 = continue 后不归零 ⇒ 模拟下一轮 2.6 立即为 true, 必红)。

### [A4-R2-M5] Major — TASK-0 「前置」与 SC-13 「合并执行」时序不可执行; TASK-0 失败分支的连锁落点不全

- **锚点**: §3.4 「Phase B TASK-0 (前置, AI 可跑)」; SC-13 「**活体** (TASK-0 合并执行): … `pre_merge_gate.py --pr-branch <b>` 实测 `pr_ci_status=not_found` + kind 在场 (基线产 pending)」; §3.4 失败分支「AD-5 改『处方 2 为主』; `remedies_available` 永不含 dispatch」; §4 `dispatchable_workflows`; SC-8/SC-9; §2.2 表第一行; AD-4 「至多一次 dispatch」
- **问题**: (i) SC-13 的第一半 (`not_found` + kind) 需要 §1+§2 已落地; TASK-0 是 Phase B 第一步, 此时 gate 仍产 `pending`。「合并执行」= 同一条 throwaway 分支上既要看基线红又要看新代码绿, 但 TASK-0 的结论 (dispatch 可用否) 又决定 §2.2 remedies 表与 SC-2 的期望值, 必须在写 SC-2 之前得到。顺序是环。(ii) 失败分支只改了 AD-5 与 remedies, 没说: §4 `dispatchable_workflows` 是否仍加 (成了「有记录无路由」的死字段, R1 #3 同形); SC-8/SC-9 是否删; SC-13 dispatch 半段改为「推 commit 后轮询」; §3.3 处方 1 整段删或标「保留待上游」; AD-4 「至多一次 dispatch」改「至多一次 commit」; §2.2 第一行 `["dispatch","commit"]` 档消失 ⇒ SC-2 期望表随之缩。
- **钉法**: 拆两步: 「TASK-0a (实现前, 只需 `forgejo` CLI + throwaway 分支 A): 首推 path-matched 变更 (本仓唯一 workflow `issue-triage-tests.yml` 声明 `skills/issue-triage/**`, 含 `workflow_dispatch: {}` 块形) → 基线 gate 记录 `pending` (红窗留证) → 真 dispatch 记 HTTP 码/是否建 run/Δt → 删分支; 结论回写 §2.2/§3.3/§4/SC-2/SC-8/SC-9/AD-4/AD-5 (失败分支逐条列上述 6 处处置); SC-13 (实现后, 分支 B): 只验 `not_found` + kind + (若 TASK-0a 成功) dispatch→轮询至非 not_found」。

### [A4-R2-M6] Major — 阈值校验位置「只在 `gate_check`」与 SC-3 经 `compute_verdict` 取值互斥; `DEFAULT_CONFIG` 加键未列落点; §3.3 误引 SC-10

- **锚点**: §3.3 config 「校验**只在** `gate_check` cfg 合并后 (`_normalize_config` 只做 alias, 不是校验点): 非 int / <2 → 回落默认 + `warnings.warn` (**SC-10**)」; §2.1 「`cfg=None` 时取 `DEFAULT_CONFIG`」; SC-3 「`gate_error.escalate_after_observations` == 校验后生效值: cfg 缺省→3; `{…: 5}`→5; `1`/`0`/`"x"`/`None`→3 + warn 各一次」; `pre_merge_gate.py:57-69` `DEFAULT_CONFIG` (无该键); `:416` `cfg = {**DEFAULT_CONFIG, **user_normalized}`
- **问题**: SC-2/SC-3/SC-4 的写法都是直调 `compute_verdict(…, cfg=…)`。若校验真的只在 `gate_check`, 直调 `compute_verdict(cfg={"no_run_escalation_observations": 0})` 会把 0 回显进 `escalate_after_observations` 且不 warn ⇒ SC-3 红; 要 SC-3 绿就得在 `_no_run_gate_error` 里校验 ⇒ 违反「只在 gate_check」。实施者二选一。另: `cfg=None → DEFAULT_CONFIG` 要拿到 3 必须给 `DEFAULT_CONFIG` 加键, §5 / 代码落点未列 `:57-69`; `{…: None}` 经 `{**DEFAULT, **user}` 会覆盖默认 (SC-3 列了此例, 正确, 但须校验函数接住 None)。§3.3 括号引 SC-10 是引用错误 (SC-10 是 PR 分支消歧), 应为 SC-3。
- **钉法**: 「校验落在纯函数 `_effective_escalation_threshold(cfg) -> int` (非 int 或 <2 → `warnings.warn` + 3), **由 `_no_run_gate_error` 调用** (故 gate_check 路径与直调路径同一校验点); `DEFAULT_CONFIG["no_run_escalation_observations"] = 3` (`:57-69`, §5 加行); workflow-runner 仍只读输出字段 (R1 #4 不变)」; §3.3 「(SC-10)」→「(SC-3)」。

### [A4-R2-M7] Major — NEG-4 只要求文件存在, 未要求注册进 suite json `fixtures[]`; 缺口 issue 已存在 (#127) 却写「若无则新开」

- **锚点**: 代码落点仅列 `…-fixtures/NEG-4-no-run-for-branch.json`; SC-15 「存在且含 `_target_behavior` / `_discriminating_question` / `_arm_expectations`」; rule6_note 「套件缺口 issue (追加到 NEG-3 当时开的缺口 issue, 若无则新开)」; `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json` `fixtures[]` (7 条, 每条 `id / file / expected_verdict / test_case_in_unit_tests / purpose`; NEG-3 条目 `test_case_in_unit_tests = test_path_coverage.InternalErrorReasonTests.test_internal_error_has_own_reason`; suite `version: 1.1.0`); NEG-3 文件另含 `_fixture_id` / `_consumed_by` / `_ships_with`; `forgejo GET /repos/10CG/aria-plugin/issues?q=NEG-3` → **#127 open** 「phase-c-integrator AB 两套件均覆盖不到 C.2.4 的 D9 surface 措辞」(#126 body 亦引 #127)
- **问题**: 按 v2 做完, fixture 文件在盘上但 `fixtures[]` 不含它 ⇒ 套件跑不到 = 「有记录无路由」(R1 #3 同形; memory `completion_signals_vs_runtime_invocation`)。SC-15 「回退本 spec 后其对应断言转红」没指名哪条断言 — 先例是 `test_case_in_unit_tests` 字段, 应指向 SC-2/SC-4 的具体测试名。缺口 issue 是可核事实, 本席已核为 #127, spec 不该留「若无则新开」的悬置。
- **钉法**: 代码落点加 `ab-suite/phase-c-integrator-pre-merge-gate.json` (`fixtures[]` 追加 NEG-4 条目, `version` 1.1.0→1.2.0, `changelog` 补 NEG-3/NEG-4 两行 — NEG-3 当时漏写); NEG-4 键集 = NEG-3 全集 (`_fixture_id` / `_consumed_by` / `_ships_with: v1.66.4`); SC-15 改「suite `fixtures[]` 含 `id=NEG-4-no-run-for-branch` 且 `test_case_in_unit_tests` 指向的测试在回退后红」; rule6_note 直接写 aria-plugin **#127**。

### [A4-R2-M8] Major — §5 14 处全准, 但仍漏 4 个同步面 (同形: 字段枚举/JSON 示例块)

- **锚点**: 逐 grep 实核
- **漏点**: (1) `workflow-runner/SKILL.md:249-264` gate_state JSON 示例块 (两新字段); (2) `workflow-runner/SKILL.md:345` 实施步骤 2 「started_at / retry_count / next_check_at / in_flight_runs[] 全部填充」(字段枚举, 须加两字段; 连同 M1 的 `:352` 顺序句); (3) `workflow-state-schema.md:38-52` 顶部 JSON 结构块 (§5 只列 `:110-131` 字段表与 `:125`); (4) `ci_backends/aether.py:218` docstring 「Map aether CIRun list → passing | failing | pending」(代码自述, 与 §5 第 7 行 `pre_merge_gate.py` 两处 docstring 同理由)。可选: `phase-c-integrator/SKILL.md:349-366` config schema 示例 jsonc (#122 先例未加 `path_coverage_enabled`, 沿先例可不加, 但应明说)。
- **钉法**: §5 加 4 行; SC-14 加 `grep -n 'retry_count' workflow-runner/SKILL.md references/workflow-state-schema.md` 命中的字段枚举/JSON 块行均含 `no_run_observations`。

### [A4-R2-m1] Minor — `unknown` 三档 reason 带 `: <detail>` 后缀, §2.2 表与 SC-2 须按前缀匹配; 「9 reason」实为 8 个不同字面

- **锚点**: `path_coverage.py:422` `internal-error: {type}: {exc}` / `:432,:447` `git-diff-failed: {err}` / `:500` `workflow-parse-failed: a, b`; §2.2 第四行 「`internal-error` 时点明『请报 issue』」; §4 「reason 封闭集 (9 个 = 8 规则终态 + internal-error)」; #122 spec `:72` 「8 条规则中产生终态判定的 7 条」; 模块 docstring `:36` 「共 9 个」
- **问题**: 按 `reason == "internal-error"` 实现永不命中 (生产值带后缀), 而 SC-2 fixture 若用裸字面则两种实现都绿 (memory `test_mock_pattern_hides_prod_bug`)。计数: 7 (规则 5 无终态) + 1 = **8** 个不同 reason 字面; `:36` 的 9 是 #126 误计 (9 = `_result` 调用点数), v2 照抄并给了错误推导。SC-2 「全 9 reason × covered/unknown」中 `not_applicable` 两 reason 与 covered/unknown 不可配, 实际 6 reason + None。
- **钉法**: 「reason 档位按 `reason.split(":", 1)[0]` 取; SC-2 unknown 变体用带后缀真实形态」; 计数改「8 个字面 (7 规则终态 + internal-error); `:36` 顺手勘正」。

### [A4-R2-m2] Minor — §2.3 (ii) `pr-branch-not-found` 「**有** `path_coverage`」在 `path_coverage_enabled=false` 下不成立 (R1 #6 同形复发于新条款)

- **锚点**: §2.2 在场条件 (ii) 「**有** `path_coverage`」; §2.3 表 「`path_coverage` 在场 (评估已执行)」; `gate_check:476-480` pc=None 当 enabled=false
- **钉法**: (ii) 改「`path_coverage` 在场与否同 (iii)」; SC-10 加 disabled 变体 (键不在场)。

### [A4-R2-m3] Minor — Impact 「Schema (additive)」清单与 §2-§5 新增面不一一对应

- **漏**: config.template.json `+path_coverage_enabled` (§5 明写补登, 用户可见); `compute_verdict +pr_branch_check` / `write_gate_state +gate_error_kind` / `_result +dispatchable_workflows` / `_parse_workflow +dispatchable` 四个签名 additive 与 `_verify_branch_exists` 新名 + 旧名包装 (若 Impact 只算输出 schema, 加一句「内部签名 additive 见 §2.1/§3.1/§4」)。
- **多**: 无。

### [A4-R2-m4] Minor — 两处小勘误

- SC-7 `:362` 是 `if no_ci_fallback == "abort":` 行, return 在 `:363` (`:376` 准确)。
- TASK-0 成功分支「修正 memory」: memory store 是容器本地 (memory `memory_store_is_container_local_not_shared`), 不是仓内 SOT; 应写「traps §6 为 SOT, memory 随之镜像修正」, 否则另一容器的 AI 看不到修正。

## 未发现问题但已核验的点

- F1 `aether.py:225-226` ✅ / F2 `base.py:29` ✅ / `test:363` ✅ / `compute_verdict :174-233` + `:219 elif main_in_flight_runs` 不检查 pr_ci_status ✅ / `_build_output :236-275` gate_error 已有入参 (伪码「穿到 _build_output」可直接成立) ✅ / 早退七落点 `:418 / :363 / :376 / :434 / :455 / :458 / :489 / :512` ✅ (main 核验两 kind 七键 `:465-472`) / not_applicable 短路 `:498-506` 在 `query_pr_ci :509` 之前 ✅。
- `path_coverage.py`: `_result` 9 个调用点, 规则 6 = `:492-495` 传 `matched` ✅ (「规则 6 调用点必改, 其余 8 不改」准确); `NON_AUTO_TRIGGER_KEYS :56` 含 `workflow_dispatch`; 标量形 `:235` / 块形 `:288` 两处 `pass` 是加 `dispatchable` 的落点, SC-8 三形态可达 ✅; 本仓唯一 workflow `issue-triage-tests.yml` 为块形 `workflow_dispatch: {}` + paths `skills/issue-triage/**` (SC-13 throwaway 分支须碰此路径)。
- `gate_state_helper.py`: `write_gate_state :131-143` 整体重建 dict ⇒ `no_run_escalation_done` 须从 `existing` 显式带过 (§3.1 已写「跨 wait 写保持」✅); `clear_gate_state :158-161` 是唯一归零路径 (SC-11c 坏实现对照成立) ✅; 既有 22 测试无整 dict 相等断言, additive 键零回归 ✅。
- `_verify_main_branch_exists :302-352` 函数体与 "main" 无关 (仅 `target = "refs/heads/" + main_branch`) — 泛化本身成立, 问题只在别名/调用点 (M2) ✅。
- #122 / #126 / #137 契约: `not_applicable` 短路不动 ✅; `gate_error` 副本通道 ✅; `internal-error` 自成一档 ✅; (b) 轴不动 ✅。
- DEC 文件实际路径 `docs/decisions/` (主仓) 与代码落点写法一致 ✅; config-loader `:242-283` pre_merge_gate 段存在 (登记点明确) ✅; config.template `:73-91` 无 `path_coverage_enabled` (§5 「补两个」属实) ✅。
- aria-plugin #127 (open) 即 NEG-3 当时开的套件缺口 issue — 可直接点名 (M7)。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 8 Major / 4 Minor) — **vote: REVISE**

R1 的 Critical 与四个结构性欠定已真落地, 方向无需重开; R2 剩余全是条款间接缝 (写/判顺序、别名可实现性、伪码 vs 表、prompt 出口、TASK-0 时序、校验位置), 每条都是「两实施者按 v2 文本会写出不同代码」的分叉而非设计分歧, 字符级钉法已给, 一轮 R2-fix 可收; 不建议加审计轮, 建议 R3 改单席定向复核 M1-M6 六处钉死文字。
