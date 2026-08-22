---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T13:00:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 1
minor_count: 3
---

## 摘要

对 v5 (R4-fix) 做 R5 (稳定性确认轮) 复核, 基线仍 `aria @ 400f0bc`, 全部结论基于实读 `pre_merge_gate.py` (`_build_output:236-273` / `compute_verdict:172-227` / `gate_check:387-527` / `_sanitize_for_json:292-299`) + `gate_state_helper.py` 全文 (`write_gate_state:115-152`, 无 `reset`, 确认 F7 仍成立) + `test_gate_state_helper.py`/`test_pre_merge_gate.py` 现状用例, 不采信 spec 文本自述。

结论: 我 R4 报的 [A2-R4-M1](DISPATCH_VIABLE/dispatchable_workflows 渲染零 SC 覆盖) **真实收敛** —— v5 SC-2 加的 dispatch 子项设计合理 (basename 负向断言 `不含 .forgejo/workflows/x.yml/dispatches` 独立承担甄别重量, 即便正向断言 `含 workflows/x.yml/dispatches` 因是后者子串而对 buggy 实现也成立, 整体仍能正确区分)。但本轮"新鲜眼睛"复查 v5 §2.1 末段**新引入**的 `<pr_branch>` 占位符回填机制 (响应 A1-R4-m2, 属吸收进 v5 但归为 minor 未强制配 SC), 发现它与 cluster #4 是**同一形状的缺陷**: 全套 SC 表 (SC-1~SC-16) 没有一条断言 `gate_check` 真的把 `gate_error.message`/`raw_message` 里的字面 `<pr_branch>` 替换成真实分支名, 也没有断言副本通道 (`raw_message == gate_error.message`) 在这次事后改写 (`out["gate_error"]["message"] = m; out["raw_message"] = m`) 之后仍然成立。这次是 v5 才出现的新机制 (v4 没有回填, `<pr_branch>` 原样留给"AI 填", A1-R4-m2 才要求 gate 顺手填), 不是 R1-R4 已报条目的重复, 判 **Major**。另有 3 条 Minor: 1 条新 (DISPATCH_VIABLE 读取机制的隐性契约), 2 条是我 R4 报过、v5 文本未见处置的原样残留。

## R4 处置核对

| 簇# | 内容 (节选) | 状态 | 证据 |
|---|---|---|---|
| 4 (A2-R4-M1) | `DISPATCH_VIABLE`/`dispatchable_workflows` 驱动的 dispatch 处方行渲染, 全 SC 表零覆盖 | **closed** | v5 SC-2 新增"dispatch 子项": `DISPATCH_VIABLE=True + dispatchable_workflows=[".forgejo/workflows/x.yml"]` → message 含 `workflows/x.yml/dispatches` 且**不含** `.forgejo/workflows/x.yml/dispatches`。逐字核验断言强度: `.forgejo/workflows/x.yml/dispatches` 本身以 `workflows/x.yml/dispatches` 收尾, 故"含"断言对 buggy(未取 basename) 实现也会为真 —— 但"不含"完整路径的断言才是真正的判别式, 且对 buggy 实现必为假 (buggy 消息恰好含有那串完整路径), 两条断言合取起来能正确二分「取了 basename」vs「没取 basename」两类实现, 不是伪造的强度。常量负控 (`DISPATCH_VIABLE=False` 或 `dispatchable_workflows=[]` → 不含 `dispatches`) 语义清楚。§3.5 的条件 scope (`dispatch_viable=false` 时整组连 SC-2 dispatch 子项一起删除) 与我 R4 建议吻合, 不产生假红。**可实现性有一条隐性依赖** (见下方新 Minor A2-R5-m1: 常量读取方式)。|
| 6 (含 A2-R4-m1) | CLI `record` 对 `verdict != wait` 且 state 文件缺失时行为未定义 | **not_addressed** | v5 §3.1 逐字仍是 v4 原文"**state 文件不存在且 verdict=wait 时**先创建骨架" (`grep 'verdict=wait 时'` 命中同一句, 未见任何针对 `--verdict green`/`--verdict fail` + 文件缺失的新增描述)。聚合表把它归进"簇 6 全部吸收", 但 spec 正文未见相应改动 —— 认定 not_addressed, 非 partial (partial 需要至少留下部分文字变化)。|
| 6 (含 A2-R4-m2) | `reset --retry-count` 无对应具名 helper 函数, 与 `reset_no_run_observations` 不对称 | **not_addressed** | v5 §3.1 `gate_state_helper.py` 改动清单仍只具名列出 `reset_no_run_observations(state)`; `reset --retry-count`(以及新增的 "同时置 `started_at=now`" 行为) 未给出对应函数名, 也未补一句"两个 reset 目标均走 CLI 内联赋值"这类显式取舍声明(我 R4 建议的两种解法任一)。同样认定 not_addressed。|

两条 not_addressed 均为 Minor 级 (原始 R4 报告已标 Minor), 未过 R5 门槛的 Major 判据 (不构成错误行为/fail-open/契约破坏/两实施者不可分辨的分叉) —— 归入下方 Minor Findings 重申, 不重复计入新 Major。

## 新 Findings

### [A2-R5-M1] Major — `gate_check` 对 `<pr_branch>` 占位符的事后回填 + 副本通道重同步, 全 SC 表零覆盖

**锚点**: proposal §2.1 末段伪码 (新增于 v5, 响应 A1-R4-m2):
```python
if out.get("gate_error"):
    m = out["gate_error"]["message"].replace("<pr_branch>", _sanitize_for_json(pr_branch)) + verify_note
    out["gate_error"]["message"] = m; out["raw_message"] = m
return out
```
+ §2.2 (`compute_verdict` 明确"不感知分支核验 (无新形参)", 故 `_no_run_gate_error` 产出的 message 对 `workflow-trigger-matched` 档必然带字面 `<pr_branch>` 占位) + §2.3 dispatch 行模板 (`-d '{"ref":"<pr_branch>"}'`) + SC 表全表。

**问题**: 这段回填逻辑是 v5 才有的新机制 (v4 里 `<pr_branch>` 全程不填, 只留给 AI; A1-R4-m2 指出"gate_check 知道分支名, 该顺手填掉", 判为 minor 吸收进 v5)。但逐一核对 SC 表, **没有一条 SC 断言这段回填/重同步真的发生**:

- SC-2 直调 `compute_verdict(...)` (不经过 `gate_check`) —— 按设计, 这一层的 message 本就**应该**还带字面 `<pr_branch>` (因为替换是 `gate_check` 的职责), 所以 SC-2 无法也不该覆盖这个机制, 这是纯函数分层的正确产物, 不是 SC-2 的疏漏。
- SC-5 (`gate_check` 端到端, "新名核验 mock (`"ok"`,`""`)" —— 恰好是触发回填代码路径的精确场景: `pr_status.state=="not_found"` 且 `_verify_branch_exists` 返回 `"ok"` (`verify_note` 留空, 走到 `out.get("gate_error")` 分支)) 的断言只写"(a) enabled → `path_coverage` 与 `gate_error` 同场, 六键俱在; (b) disabled → ... message 为「评估已关闭」档"——**完全没有检查 message 内容里字面 `<pr_branch>` 是否已被替换成真实分支名, 也没有检查替换后 `raw_message == gate_error.message` 是否仍然成立**。
- SC-10 覆盖的是 `_verify_branch_exists` 返回 `"not-found"`(走另一条提前 `return`, 根本不经过 `compute_verdict`, 消息内联构造无占位符) 与 `"verify-failed"`(断言只查"核验失败"子串是否出现, 不查 `<pr_branch>` 是否消失) 两种**分支不存在/核验失败**场景, 唯独漏了"分支存在, 回填正常发生"这条**最常见的生产路径** (F5/F4 描述的典型场景: PR 分支确实存在, 只是零 run)。
- SC-14 是纯文本 grep, 不执行代码, 不可能验证运行时替换。

**后果 (为何达 Major 门槛)**: 两个独立实现者面对 v5 同一段伪码, 一个逐字照抄(`.replace(...)` + 双写 `out["gate_error"]["message"]`/`out["raw_message"]`), 一个犯以下任一种真实可能的实现漏洞——
  (a) 漏写 `.replace()`, 直接 `m = out["gate_error"]["message"] + verify_note`(message 里 `<pr_branch>` 原样留下, 交给人的 dispatch 命令行字面写着 `-d '{"ref":"<pr_branch>"}'`, 是一条不可执行的坏命令, 直接抵消 v3 收缩"给人可复制处方"这个唯一还留着的自动化价值), 或
  (b) 只改了 `out["gate_error"]["message"] = m` 忘了同步 `out["raw_message"] = m`(违反 AD-3 明文的副本通道契约, 两个字段从这一刻起永久分叉, 只读 `raw_message` 的消费方看到的是替换前的旧文本)——
两者跑 SC-1~SC-16 全绿, 无法区分。这正是 memory `feedback_spec_underdetermination_two_implementer_test` 的形状, 也是我 R4 报告 A2-R4-M1 抓到的同一类缺陷 (新机制引入时 SC 表未跟进), 这次落在 v5 自己新增的那段代码上, 印证 memory `feedback_fix_the_class_not_the_instance`(修一个位置的同形状问题, 没推广到 v5 自己顺手加的新位置)。

**建议**: 在 SC-5 的 (a) 分支追加断言 (不需要新增 SC 编号, 现有 SC-5 已经处在正确的调用层与正确的 mock 组合上, 只是断言不够): 选一个能产出 `workflow-trigger-matched` + 非空 `dispatchable_workflows` 的 `path_coverage` fixture, 断言最终 `out["gate_error"]["message"]` (i) **不含**字面 `<pr_branch>`; (ii) 含调用时传入的真实 `pr_branch` 值; (iii) `out["raw_message"] == out["gate_error"]["message"]`。同时在 SC-10 的 "verify-failed" 分支旁补一句"该场景下 `<pr_branch>` 同样必须已被替换" (verify_note 只是追加后缀, 不能成为跳过占位替换检查的理由)。改动局限于 SC-5/SC-10 文字, 不牵动 owner 已裁定的设计, 预期一轮内可收敛。

## Minor Findings

### [A2-R5-m1] Minor (新) — `DISPATCH_VIABLE` 常量的读取方式 (裸全局引用 vs 默认参数捕获) 未被 spec 钉死, 同文件先例恰好示范了相反模式

`_no_run_gate_error(path_coverage, threshold)` 调用点 (§2.2) 只传 2 个位置参数, `DISPATCH_VIABLE` 必须在函数体内以某种方式读取。若实现者在函数体内写裸全局引用 (`if DISPATCH_VIABLE and ...`), SC-2 的 `mock.patch.object(gate, "DISPATCH_VIABLE", False)` 负控能正确生效 (Python 全局名字在调用时才解析, 走 `__globals__`/模块 `__dict__`, 这正是既有 `evaluate_path_coverage` 打桩先例 (`pre_merge_gate.py:36-38` 注释自陈) 依赖的同一机制)。但**同一文件里紧邻的 `_verify_main_branch_exists`(→改名后的 `_verify_branch_exists`) 恰好示范了对立模式**: `timeout: int = _LS_REMOTE_TIMEOUT` 是**默认参数值**, 在模块 import 时一次性绑定——`grep` 全测试文件确认目前没有任何测试对 `_LS_REMOTE_TIMEOUT` 做 monkeypatch, 这个模式此前从未被验证过是否"可 patch"。若实现者照抄这个离得最近的先例, 把 `dispatch_viable: bool = DISPATCH_VIABLE` 也写成默认参数, `monkeypatch.setattr(gate, "DISPATCH_VIABLE", False)` 之后默认值仍是 import 时绑定的旧值, SC-2 dispatch 负控子项会对着一份功能上完全合规的实现持续报红——但这**不会**造成"两实现分叉且全绿不可区分"(Major 门槛): TDD 红→绿纪律会强迫实现者定位并修正这处 Python 求值时机坑, 修正后收敛到与裸全局引用等价的行为, 不存在"错误实现蒙混过关"的路径, 只是徒增排查成本。降级 Minor。建议 spec 在 §3.5 或 SC-2 旁补一句实现约束: "`_no_run_gate_error` 须以模块级裸名称读取 `DISPATCH_VIABLE`(不得作为函数默认参数值捕获), 与 `evaluate_path_coverage` 打桩先例同款", 消除对 Python 语义细节的隐性依赖。

### [A2-R5-m2] Minor (R4 残留, not_addressed) — CLI `record` 对 `verdict != wait` 且 state 文件缺失时行为仍未定义

同 R4 报告 A2-R4-m1。v5 §3.1 文本逐字未变。结构上仍主要靠"`record` 的首次调用恒在首个 wait verdict 时触发"(§3.2 步骤 2) 这条隐含调用序列不变量兜底, 只有交互式脱离 workflow-runner 直调 CLI 时才可达。维持 Minor, 建议补一句"非 wait 且文件缺失 → exit 2, 语义同 reset/clear"。

### [A2-R5-m3] Minor (R4 残留, not_addressed) — `reset --retry-count` 缺对应具名 helper 函数或显式风格声明

同 R4 报告 A2-R4-m2。v5 `gate_state_helper.py` 改动清单仍只具名列出 `reset_no_run_observations(state)`, `reset --retry-count`(含新补的 "同时置 `started_at=now`") 没有对应函数名, 也没有"两个 reset 目标统一走 CLI 内联赋值"这类显式取舍声明。维持 Minor。

## v5 新增机制层专项复核 (按 R5 任务要求, 记录未发现问题的部分)

- **CLI `reset --retry-count` 同时置 `started_at=now`**: 实读 `write_gate_state`(`gate_state_helper.py:115-152`) 确认其 `started_at` 持久化逻辑 (`started_at = existing.get("started_at") or _utcnow_iso()`) 只在"不是 `reset`"的正常 `write_gate_state` 调用链里生效; `reset --retry-count` 是独立 CLI 子命令, 显式覆盖 `started_at` 不会破坏 `write_gate_state` 自身"同一 episode 内 `started_at` 不变"的既有不变量 (SC-11(a) 测的是 `write_gate_state` 连续调用, 与 `reset` 分属不同函数/不同 SC 子项(d), 二者断言不矛盾)。`grep started_at tests/test_gate_state_helper.py` 确认现状测试文件里没有任何"`started_at` 全局只读一次"式断言会被这条新行为打破。SC-11(d) 已显式断言"`reset --retry-count` 后 `started_at` 更新", 覆盖到位。**判定: 无新问题, 已闭合。**
- **`compute_verdict` 纯函数契约**: `_no_run_gate_error` 的调用完全在 `compute_verdict` 内部完成, 不做 I/O, 参数只有 `path_coverage`/`threshold`, 保持纯函数性质; 真正对分支名敏感的回填逻辑被正确放在 `gate_check`(非纯函数, 已持有 `pr_branch`/`remote` 等上下文) 里, 分层本身architecturally 自洽, 问题只在 SC 覆盖不足 (即上方 A2-R5-M1), 不是分层设计错误。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 1 Major / 3 Minor)

vote: **REVISE** —— 我 R4 报的 A2-R4-M1 (DISPATCH_VIABLE 渲染 SC 覆盖) 真实收敛, 但本轮新鲜眼睛在 v5 自己新增的 `<pr_branch>` 回填机制上发现了同一形状 (新机制引入零 SC 覆盖) 的新 Major, 且证据显示 v4→v5 修一个位置 (DISPATCH_VIABLE) 时没有把"新机制必须配 SC"这条准则推广到同一批次里另一个新机制 (`<pr_branch>` 回填, 响应 A1-R4-m2 时引入)。修法局部 (SC-5/SC-10 各补 2-3 句断言, 复用已有的 mock 组合与调用层, 不新增 SC 编号), 不牵动 owner 已裁定的 A′ 设计或任何 v3/v4/v5 结构决定, 预期一轮内可收敛。另 2 条 R4 Minor (record 非-wait+文件缺失未定义 / reset --retry-count 无具名函数) 在 v5 文本里仍未处置, 连同 1 条新 Minor (DISPATCH_VIABLE 读取机制隐性契约) 一并列出, 均不影响批准门槛。
