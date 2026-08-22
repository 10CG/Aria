---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T10:40:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 3
minor_count: 2
---

## 摘要

对 v3 (R2-fix + 设计收缩) 做 R3 复核, 全部结论基于 `aria @ 400f0bc` 实读代码 + 实跑验证 (`pre_merge_gate.py` / `path_coverage.py` / `gate_state_helper.py` / `workflow-state-schema.md` / `.aria/config.template.json` / `.aria/probes/config-template-key-currency.py`), 不采信 spec 文本自述。

结论: R2 归我席的两条 Major(DEFAULT_CONFIG 登记 / helper 持久化不变量)在设计收缩后**真实吸收**(见下表), 且我用合成模板**复现了探针 PASS**(而非只信 spec 文字)。但 v3 把 R2 的散文承诺**首次落成具体伪码 / 具体函数签名**后, 三处新的机制层缺口浮出水面: (1) §2.1 第八早退伪码存在一处**变量作用域缺陷** —— `verify_note` 只在 `pr_ci_status=="not_found"` 分支内被赋值, 但被引用它的 `if verify_note and out.get("gate_error")` 却在该 `if` 块之外, 逐字实现会让**除 not_found 外的所有** `gate_check()` 调用(即现有 119+22 基线测试的绝大多数)抛 `UnboundLocalError`；(2) message 封闭表里 `empty-diff` 档要求消息文本嵌入真实 `<main>...<pr>` 分支名, 但沿整条调用链(`gate_check` → `compute_verdict` → `_no_run_gate_error(path_coverage, threshold)` → `path_coverage._result()`)逐个签名核对, **没有任何一环携带分支名**, 无字面数据来源；(3) CLI `record`/`reset-observations`/`clear` 在 `.aria/workflow-state.json` 不存在时的行为未定义, 且 `load_state()` 返回 `None` 时传入既有 `write_gate_state`/`clear_gate_state` 会当场 `AttributeError`, SC-11(d) 的"临时 state 文件"表述明确绕开了这个分支。三处均可用局部补丁收敛, 不牵动设计, 但都是"照字面实现会在最常见路径上直接崩"的量级, 建议进 A.2 前修正伪码/签名。另有 2 条 Minor。

## R2 处置核对

| 簇# | 内容 (节选, 归我席/我核验) | 状态 | 证据 |
|---|---|---|---|
| 2 (A1-R2-M1+A2-R2-M1 后续) | 删自动动作 ⇒ 删 `no_run_escalation_done`, 只剩 `no_run_observations`, CLI `record` 单点读-改-写 | **closed (结构层)，但新鲜眼睛在 CLI 具体化后发现新缺口** | v3 §3.1 确认 `done` 字段已从设计中整体删除 (无残留字段/无跨调用布尔持久性问题, R2-M1 的原始触发面随设计收缩一并消失); `write_gate_state` 仍是整块重建字面量 (`gate_state_helper.py:145-154` 实读确认), 但 `no_run_observations` 只是"算出新值塞进同一份字面量"而非"必须原样保留一个布尔标记", 风险量级显著低于 R2-M1 所指的姊妹坑。**但** CLI 化后新出现 M3 (state 文件缺失路径未定义), 见下 |
| 9 (A2-R2-M2 + A2-R2-m2) | `DEFAULT_CONFIG` 未列 `no_run_prompt_after_observations` 致 `config-template-key-currency` FAIL; `_effective_prompt_threshold` 单校验点 | **closed (实测复现修复有效)** | v3 §2.2 明写"`DEFAULT_CONFIG` (`:57-69`) 加该键"。我用合成模板 (在现网模板基础上加 `no_run_prompt_after_observations`+`path_coverage_enabled`) 跑探针: 修前 `FAIL unknown key(s)…: no_run_prompt_after_observations`(复现现状), 修后(临时给 `DEFAULT_CONFIG` 补该键)`unknown: []`, `dep: []` —— 探针真会转绿。`_effective_prompt_threshold(cfg)` 作 `compute_verdict`/`gate_check` 唯一校验点, 两路径 cfg 来源(`None`→`DEFAULT_CONFIG` vs `gate_check` 合并后字典, 后者已含该键)在该函数内收敛, 架构上不会分叉 |
| 4/5 (A1-R2-M3/A4-R2-M2 后续) | PR 分支不存在改第八早退 + `_verify_branch_exists` 改名, 旧名包装保关键字签名 | **partial** | `_build_output(...)` 在第八早退里的调用逐参数核对(`verdict/pr_ci_status/in_flight_runs/primitive_used/raw_message/path_coverage/gate_error`)与真实签名 `_build_output(verdict, pr_ci_status, in_flight_runs, primitive_used, raw_message="", primitive_version_sha="", path_coverage=None, gate_error=None)`(`:236-245`)逐字吻合, 全 kwargs 调用零错位。但该早退分支下游的 `verify_note` 后处理代码存在作用域 bug (见 M1); 别名包装字面代码丢失了原 `timeout` 参数的默认值(见 m2, 低影响) |
| 14 (message 表 8 档) | `(decision, reason 前缀) → 档` 完整映射 | **partial** | 6 行表覆盖真实 8 reason + `pc=None` 共 9 种输入组合, 逐格核对与 `path_coverage.py` 判定规则 1-8 的 reason 字面量(`empty-diff`/`workflow-files-changed`/`workflow-trigger-matched`/`git-diff-failed`/`workflow-parse-failed`/`internal-error`/两个 `not_applicable` 理由)**无交叉无遗漏**; `workflow-files-changed` 恒 `matched_workflows=[]` (`path_coverage.py:464` 实读确认)与表内"不列具体 workflow 名"的措辞一致。但 `empty-diff` 档的 `<main>...<pr>` 字面量在整条签名链上找不到数据源 (见 M2) |
| R2-A2-m1 (reason 族数) | `path_coverage.py:36`「共 9 个」勘正 | **closed** | v3 §4 干净地写「reason 族 = **8** (7 条规则终态 + internal-error; 模块 docstring `:36`「共 9 个」是既有错」, 不再是"9=8+1"式的自我矛盾表述 |
| R2-A2-m2 (SC 引用错标) | §3.3 误引 SC-10 应为 SC-3 | **closed** | v3 §3.4 改为直接引函数名 `_effective_prompt_threshold`, 不再有内联 SC 编号, 原错标位置已消失, 无法复发 |
| R2-A2-m3 (mixin 隐性依赖) | SC-5/SC-10 未提示复用 `_ProbeCacheResetMixin` 的 main-branch mock | **not_addressed** | SC-5/SC-10 表格文字仍只提"mock 新名 `_verify_branch_exists`", 未加一句提示复用既有 mixin。维持 Minor, 未升级(现有测试基础设施已覆盖, 只是文档提示缺失) |

## 新 Findings

### [A2-R3-M1] Major — §2.1 第八早退伪码: `verify_note` 变量作用域缺陷, 逐字实现会使**几乎全部**非 `not_found` 的 `gate_check()` 调用崩溃

**锚点**: proposal §2.1 伪码 (`:63-79`):
```python
if pr_status.state == "not_found":
    st, detail = _verify_branch_exists(pr_branch, remote=remote, timeout=...)
    if st == "not-found":
        ...
        return _build_output(...)
    verify_note = "" if st == "ok" else f" (PR 分支存在性核验失败: {detail})"
out = compute_verdict(main_in_flight_runs=in_flight.runs, pr_ci_status=pr_status.state,
                      backend_name=backend.name, cfg=cfg, path_coverage=pc)
if verify_note and out.get("gate_error"):
    out["gate_error"]["message"] += verify_note; out["raw_message"] = out["gate_error"]["message"]
return out
```

**问题**: `verify_note` 的唯一赋值点(`:74`)缩进在 `if pr_status.state == "not_found":` 块内部, 而引用它的 `if verify_note and out.get("gate_error"):`(`:77`)缩进在该 `if` 块**之外**、与 `out = compute_verdict(...)` 同级。当 `pr_status.state != "not_found"` 时 —— 这是 `gate_check()` 绝大多数调用的真实取值(`"passing"` / `"pending"` / `"failing"` / `"error"`, `"not_applicable"` 已在更早的 `:498-506` 短路掉, 不会走到这段代码)—— `verify_note` 从未被赋值, Python 会在 `:77` 抛 `UnboundLocalError: local variable 'verify_note' referenced before assignment`(函数作用域内, 局部变量在赋值前被读取即报此错, 不是 `NameError`)。

这不是边角场景: SC-7 的七个既有早退落点测试、SC-9 的 path_coverage 参数化测试、SC-12 声明的"既有 119+22 全绿"回归基线, 只要走到这段新插入代码之后(即 PR CI 状态不是 `not_found` 的每一次 `gate_check()` 端到端测试), 照此伪码实现都会在这一行崩溃。

**实测证据**: 逐字对照 `pre_merge_gate.py:508-527`(基线, 未改动前的 `gate_check` 尾段)确认现状代码里 `pr_status = backend.query_pr_ci(pr_branch)` 之后直接 `return compute_verdict(...)`, 没有任何中间变量; v3 伪码是在这段代码中间**插入**了一个只在一个分支内赋值、却在分支外被读取的变量, 是纯粹的转录疏漏(不是设计缺陷 —— `st == "ok"` 时 `verify_note=""` 、`st == "verify-failed"` 时非空字符串, 这两条分支内的逻辑本身是对的, 唯独忘了给 `pr_status.state != "not_found"` 这条路径一个初始值)。

**建议**: 在 `if pr_status.state == "not_found":` 之前加一行 `verify_note = ""`(或将 `:75-79` 的整段后处理挪进 `if pr_status.state == "not_found":` 块内, 因为 `verify_note` 只有该分支才可能非空, 挪进去逻辑等价且不需要哨兵初始化)。这是一行/一处缩进的修正, 不影响任何 SC 的断言内容, 建议在 A.2 前把伪码改对, 以免实现者机械照抄。

---

### [A2-R3-M2] Major — message 封闭表 `empty-diff` 档要求嵌入 `<main>...<pr>` 真实分支名, 但沿完整调用链没有任何签名携带分支名

**锚点**: proposal §2.3 message 表 (`covered` / `empty-diff` 行: 「`<main>...<pr>` 三点 diff 为空, 无变更可跑; 远端零 run」) + §2.2 (`gate_error = _no_run_gate_error(path_coverage, _effective_prompt_threshold(cfg))`) + `compute_verdict` 签名 (`pre_merge_gate.py:174-180`: `main_in_flight_runs, pr_ci_status, backend_name, cfg, path_coverage` — 无分支名参数, v3 未提出扩展) + `path_coverage._result()` (`path_coverage.py:63-73`: `decision, workflows_scanned, matched_workflows, changed_files_count, reason` — 无 `main_branch`/`pr_branch` 字段) + `evaluate_path_coverage`/`_evaluate` (`path_coverage.py:410-451`: 只把 `main_branch`/`pr_branch` 用于 `git diff` 命令本身, 从不写回返回字典)。

**问题**: 本文档内其余占位符(`<下表>` / `<obs>` / `<elapsed>`)的用法惯例都是"运行时用真实值替换"; `empty-diff` 档的 `<main>...<pr>` 按同一惯例理应是把真实的 `main_branch`/`pr_branch` 字符串以三点 diff 形式嵌进消息(类比现有 `_verify_main_branch_exists` 系错误消息里"main branch 'master' not found on remote 'origin'"的做法, 分支名都是从调用方形参直接拿到的)。但 `_no_run_gate_error(path_coverage, threshold)` 的签名(§2.2 明文)只接受这两个参数; `path_coverage` 字典逐字段核对(`_result()` 的 5 个键)不含分支名; `compute_verdict` 自身签名也不含分支名; `gate_check` 虽然握有 `main_branch`/`pr_branch` 局部变量, 但 v3 并未提议把它们下传到 `compute_verdict`/`_no_run_gate_error`。三层签名逐一核对下来, `<main>...<pr>` 在实现时**没有字面数据来源**——两个独立实现者面对这条表格行, 一个可能给 `_no_run_gate_error` 偷偷加第三个参数(与 §2.2 明文签名冲突), 另一个可能干脆把字符串写死成字面量 `"<main>...<pr>"`(通过 SC-2 的字符串包含断言测试, 因为 SC-2 没有对这一档做分支名内容断言), 产生分叉的实现且都"过测试"。

**实测证据**: `grep -n "def compute_verdict\|def _result\|def evaluate_path_coverage" pre_merge_gate.py path_coverage.py` 三处签名逐一读取(见上); `python3 -c` 打印 `_result()` 返回字典键集确认恒为 `{decision, workflows_scanned, matched_workflows, changed_files_count, reason}`, 从不含分支名。

**建议**: 三选一并在 spec 明写: (a) 给 `_no_run_gate_error` 加 `main_branch: str, pr_branch: str` 两个新形参(需要 `compute_verdict` 同步加并从 `gate_check` 透传, 是本 spec 目前"不改 `compute_verdict` 签名"这条隐含约束的一次显式打破, 需要在 Impact 的 additive 签名列表里补上); (b) 把这两个字段加进 `path_coverage._result()`(需要在 §4 的 additive 字段列表里显式登记, 且要过一遍 SC-9 的"decision/reason/matched_workflows 与基线逐字同"断言不受影响的检查); (c) 放弃在纯 Python 消息里嵌入真实分支名, 改成通用措辞不引用 `<main>`/`<pr>`(与其余五档统一, 分支名留给 §3.3 由 AI 组装最终 prompt 时自行补充, 那一层本就握有 `pr_branch`)。三者选一后同步改 SC-2 对 `empty-diff` 档加一条内容断言, 防止两个实现分叉都"过测试"。

---

### [A2-R3-M3] Major — CLI `record`/`reset-observations`/`clear` 在 `.aria/workflow-state.json` 不存在时行为未定义, 且沿用既有函数会当场崩溃; SC-11(d) 未覆盖此分支

**锚点**: proposal §3.1(CLI 命令列表: `record --verdict … [--gate-error-kind K] [--threshold N] [--raw-message …] [--in-flight-runs JSON]`; `reset-observations`; `clear` — 均描述为"读-改-写, 沿用文件内 atomic write") + `gate_state_helper.py:66-83`(`load_state` 在 `FileNotFoundError` 时显式 `return None`) + `write_gate_state:131`(`existing = state.get("gate_state") or {}` —— 若 `state` 本身是 `None` 而非 `dict`, `.get` 调用即 `AttributeError: 'NoneType' object has no attribute 'get'`) + `clear_gate_state:160`(`state["gate_state"] = None` —— 若 `state=None`, `TypeError: 'NoneType' object does not support item assignment`) + SC-11(d)(「临时 state 文件两次调用」— 用词已预设文件在调用前存在)。

**问题**: 三个 CLI 子命令若照最自然的写法实现(`state = load_state(path); state = <mutator>(state, ...); atomic_write_state(state, path)`), 当 `.aria/workflow-state.json` 尚不存在时 `load_state` 返回 `None`, 传入 `write_gate_state`/`clear_gate_state`/`reset_no_run_observations` 会立即崩溃退出(非 spec 承诺的"exit 2 输入错"这种可控失败, 而是未捕获异常的 traceback)。这不是纯理论场景: `workflow-state-schema.md` 明确"gate_state 是既有 workflow session 内的一个可选子块", 但 `gate_state_helper.py` 是从 v1.0 起就设计为**可独立于完整 workflow 生命周期被调用**的 reference 实现(docstring 自陈"the actual workflow-runner skill is markdown-driven"), 而 v3 §3.3 也明确承认"交互式直调 §C.2.4(无 workflow-runner)"是一个被认可的使用形态 —— 在这种直调场景下, `.aria/workflow-state.json` 完全可能从未被创建过。即便在正常 workflow-runner 会话内, "首个 wait verdict 也经 CLI record 创建 gate_state"(§3.2 步骤 2)这句表述本身就暗示 `record` 需要处理"gate_state 子块不存在"(这个有防御 —— `existing = state.get("gate_state") or {}` 处理得了), 但没有一处文字处理"state **文件本身**不存在"这个更外层的缺失。

SC-11(d) 用"临时 state 文件"措辞, 意味着测试会在调用前预先放一个文件, 天然不会跑到这个分支, 所以这个缺口目前对 SC 全绿。

**实测证据**: 直接读 `load_state`(`:66-83`)确认 `FileNotFoundError → return None`; `write_gate_state`(`:131`)与 `clear_gate_state`(`:160`)都没有 `state is None` 的防御分支, 对 `None` 输入必崩。

**建议**: 在 §3.1 CLI 描述里显式补一句: `record`/`reset-observations`/`clear` 读到 `load_state() is None` 时的行为 —— 建议 `record` 视为"新建 gate_state 但拒绝新建整个 workflow-state 文件"(不是这个 helper 的职责, workflow-runner 才管 `session`/`workflow`/`git_anchor` 的初始化), 因此应该以 **exit 2 + 明确错误信息**(如"state file absent; run within an active workflow session or workflow-runner init first")失败, 而不是让 `AttributeError`/`TypeError` 裸露到调用方; `reset-observations`/`clear` 同理(状态本就不存在时清除是 no-op, 可以直接返回成功而非报错, 但需要 spec 明确选哪种)。并在 SC-11 补一条子项覆盖"state 文件不存在时 `record` 的确切退出码与 stdout/stderr"。

## Minor Findings

### [A2-R3-m1] Minor — SC-11(d)「坏实现(整块重建漏 carry-forward)必红」未明确要求独立重读持久化文件, 对"stdout 自洽但未真正落盘"的坏实现留有漏洞

若 CLI `record` 的自然实现是"打印 `write_gate_state` 返回值里的字段", 则 stdout 与持久化文件天然一致, 此时 SC-11(d) 现有措辞("stdout JSON obs 1→2, 文件落盘")足以抓住"整块重建漏字段"这类 bug。但如果实现者反而是"CLI 自己在本地重算一遍 obs 用于打印, 同时把 obs 传给 `write_gate_state` 写文件"这种双记账写法(与 R1/R2 反复出现的"计算对了但没塞进字面量"同形), stdout 可能自洽而持久化文件才是错的那份。建议 SC-11(d) 显式加一句"第二次调用后**独立重新打开状态文件**读取 `gate_state.no_run_observations`, 与 stdout 值分别断言(不得只信 CLI 自己的回执)", 呼应 memory `feedback_output_hygiene_no_raw_control_bytes` 的"回执非 ground truth"原则。

### [A2-R3-m2] Minor — `_verify_main_branch_exists` 兼容包装丢失原函数的 `timeout` 默认值

proposal §2.1 给出的包装字面代码 `def _verify_main_branch_exists(main_branch, remote, timeout): return _verify_branch_exists(main_branch, remote, timeout)` 中 `timeout` 没有默认值, 而基线原函数签名是 `timeout: int = _LS_REMOTE_TIMEOUT`(`pre_merge_gate.py:303`)。经核实, 当前仓内唯一真实调用点(`gate_check:449-453`)与全部测试(`grep _verify_main_branch_exists(` 测试文件零命中直调, 均走 `mock.patch.object` 整体打桩)都会显式传 `timeout=`, 所以此改动**不会**造成任何现有路径回归, 纯粹是"函数签名对未来直接调用者的防御性"退化。建议顺手在包装里补回默认值 `timeout: int = _LS_REMOTE_TIMEOUT`, 零成本消除这个降级。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 3 Major / 2 Minor)

vote: **REVISE** — R2 归我席的两条 Major 已通过设计收缩与实测复现真实收敛(DEFAULT_CONFIG 探针用合成模板验证过 FAIL→PASS 两态; helper 的持久化风险随 `done` 字段删除而显著降低)。但 v3 首次把 R2 的散文承诺写成具体伪码/具体签名后, 三处新的机制层缺口浮出水面, 且三处都是"照字面实现会在常见路径/首次调用上直接崩溃或产生数据源缺失"的量级(非风格/measure-only 级别的 minor), 不满足我这一席的 PASS 门槛。三处修法都局部(补一行初始化 / 补两个字段或改措辞 / 补一段 exit-2 文字 + 一条 SC), 不牵动 owner 已裁定的 A′ 设计或 v3 的设计收缩决定, 预期一轮内可收敛。
