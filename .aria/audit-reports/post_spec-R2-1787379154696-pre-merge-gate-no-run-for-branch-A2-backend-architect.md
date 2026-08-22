---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T08:10:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A2-backend-architect
critical_count: 0
major_count: 2
minor_count: 3
---

## 摘要

对 v2 (R1-fix) 做 R2 复核: (1) 逐条核对归我席的 R1 簇是否真落地; (2) 多簇合并后的条款间交叉一致性; (3) 新鲜眼睛找 v2 新引入的问题。方法与 R1 一致 —— 全部结论基于 `aria @ 400f0bc` 实读代码 + 实跑验证(`gate_state_helper.py`/`pre_merge_gate.py`/`path_coverage.py`/`.aria/state-checks.yaml`/`.aria/probes/config-template-key-currency.py`),不采信 spec 文本自述。

结论: **归我席的 R1 三条 Major + 三条 Minor 全部真实吸收(见下表), 证据扎实**(elif 插入位置有显式防呆注释 + SC-4 改钉 `gate_error.kind`; retry_count/started_at 归零机制被整体重设计为 `no_run_observations`/`no_run_escalation_done` 两新字段, `mark_no_run_escalation_done` 显式声明不碰三个既有字段; escalate 阈值改为单一校验点 + 机读字段回显)。但 R2 新鲜眼睛核查发现 **2 处新 Major**: 一处是 `no_run_escalation_done` 的**跨 `write_gate_state` 调用持久性**在 SC-11 全部子项里都没有被端到端练习到,而 `write_gate_state` 现有实现是整体重建 `gate_state` 字典(非合并写),这恰好是 R1 Critical 簇(#1)想根治的那个"至多一次"不变量的**同形姊妹坑**;另一处是纯机制性的 —— §5 指示往 `.aria/config.template.json` 加 `no_run_escalation_observations`,但全文没有一处指示同步把这个键加进 Python `DEFAULT_CONFIG`,而仓内已启用的 `config-template-key-currency` state-check 恰好反向检查"模板键 ⊆ DEFAULT_CONFIG",我实测复现了这条探针会因此 FAIL。另有 3 条 Minor(reason 计数"勘正"仍不对 / SC 交叉引用错标 / 两处 mock 目标隐性依赖既有 mixin)。均不构成"按 spec 实施必然错误行为"的 Critical 门槛,建议在进 A.2 前补两处 Major 对应的文字/断言。

## R1 处置核对

| 簇# | 内容(节选,归我席) | 状态 | 证据 |
|---|---|---|---|
| 12 (含 A2-M1) | elif 新分支须插在 `not_applicable` 之后、`main_in_flight_runs` 之前,否则 gate_error 被吞 | **closed** | v2 §2.1 伪码显式加注释「新分支必须位于...之后...之前」+ 代码防呆注释指令;SC-4 红窗声明改为「红在 `gate_error.kind`」并强制断言 kind(非仅 `verdict==wait`) —— 正是我 R1 建议的三点(1)(2)(3)逐条落地 |
| 1+13 (含 A2-M2) | `retry_count` 归零唯一路径(`clear+write`)连带重置 `started_at`,1800s 上界失效 | **closed** | v2 §3.1 整体删除「retry_count 归零」处方,改为 `no_run_observations`(int)+`no_run_escalation_done`(bool)两新字段;`mark_no_run_escalation_done` 显式声明「不触碰 `started_at`/`retry_count`/`next_check_at`」;SC-11(c) 精确钉死此不变量,且明说「坏实现=走 clear+write 路径,此条必红」。**但见下方新 Major-1,发现了同一根问题域里 R1 未覆盖的姊妹坑** |
| 4 (A2-M3) | `no_run_escalation_retries` 两个独立消费方(gate 校验 / workflow-runner 读原始 config),校验语义可能分叉 | **closed** | v2 §3.2「阈值来源: **只读** gate 输出 `gate_error.escalate_after_observations`,workflow-runner 不读原始 config key」;§2.1/§2.2 伪码显式经 `_no_run_gate_error(path_coverage, cfg, pr_branch_check)` 单一函数产出该字段 —— 实读确认 `compute_verdict` 是 `gate_check` 与直调测试(SC-2/3/4)唯一共同路径,单点校验架构上不可能分叉(cfg=None 时经同一函数回落 DEFAULT_CONFIG,与 gate_check 传入的已合并 cfg 走同一段判定代码) |
| 17 (A2-m1) | `compute_verdict` 的 `cfg=None` 默认值与 SC-2/3/4 调用不设防会 AttributeError 崩溃 | **closed** | v2 §2.1「`cfg=None` 时取 `DEFAULT_CONFIG` (R1 A2-m1)」显式写明 |
| 17 (A2-m2) | `.aria/config.template.json` 未列入 §5 同步面,且探针只单向检查 | **closed(但引出新 Major-2)** | v2 §5 显式加一行「加 `no_run_escalation_observations`;同时补 #122 漏登的 `path_coverage_enabled`」。但这条"补齐"本身产生了一个新的反方向缺口——见下方新 Major-2 |
| 17 (A2-m3) | 「六键契约逐字不变」措辞与 main 核验既有七键事实冲突 | **closed** | v2 §2.2「注意 main 核验 fail 那支本就是七键(六键 + `gate_error`),v1 把它写进「六键不变」是措辞错(R1 A1-m1/A2-m3)」逐字承认并改用 SC-7「输出键集逐字不变」措辞 |

R1 my-seat items: 6/6 closed, 0 partial, 0 not_addressed.

## 新 Findings

### [A2-R2-M1] Major — `no_run_escalation_done` 跨 `write_gate_state` 调用的持久性未被 SC-11 任何子项端到端练习到; `write_gate_state` 整体重建字典的既有写法是隐性陷阱

**锚点**: `gate_state_helper.py:131-155`(`write_gate_state` 末尾 `state["gate_state"] = {...}` 是**整体替换**而非合并写)+ proposal §3.1(`no_run_escalation_done`「跨 wait 写保持」)+ SC-11(a)(b)(c)(d)。

**问题**: 实读现有 `write_gate_state`,函数末尾无条件重建整个 `gate_state` 字典:

```python
state["gate_state"] = {
    "name": name, "status": verdict, "started_at": started_at,
    "retry_count": retry_count, "next_check_at": ...,
    "in_flight_runs": in_flight_runs or [], "primitive_used": primitive_used,
    "raw_message": raw_message,
}
```

这不是合并写(`dict.update`),是整体替换。`started_at` 之所以能在非 `is_first` 分支正确保留,是因为代码显式做了 `started_at = existing.get("started_at") or _utcnow_iso()` 再塞进新字典。`no_run_escalation_done` 要满足 spec 要求的「跨 wait 写保持」,必须走**同一种**「先从 `existing` 读出、再塞回新字典」模式——但这是我从"既有 `started_at` 怎么实现"反推出的隐含要求,spec 正文只说了行为契约("跨 wait 写保持"),没有像 `started_at` 那样明说"必须从 existing 读"。

真正的风险点在**生产序列**: 2.5 触发处方 → `mark_no_run_escalation_done(state)` 把 `no_run_escalation_done` 置 true、`no_run_observations` 归零(且不碰 `started_at`/`retry_count`,SC-11(c) 已钉死)→ 回到 polling loop → **下一次 gate_check 仍判 `no-run-for-branch`(处方没让世界变)→ workflow-runner 再次调用 `write_gate_state(gate_error_kind="no-run-for-branch")`**。这次调用如果实现者没有把 `no_run_escalation_done` 也塞进「先读 existing 再写回」的模式(例如,只写了 `no_run_observations` 的自增/归零逻辑,却忘了同时把 `no_run_escalation_done` 从 `existing` 读出来原样带进新字典——这是完全可能发生的疏漏,因为这是整个函数里*新增的第二个*需要"跨调用保持"的字段,而模式本身没有被显式点名要复用),`no_run_escalation_done` 会静默跌回默认值 `false`。接下来几轮 `no_run_observations` 重新爬到 `escalate_after_observations` 后,`should_escalate_no_run`(`obs>=threshold and not done`)会**再次判 true**——2.5 会**再次执行一次处方(dispatch/commit)**,而不是按设计走向 2.6 的 user prompt。这正是 R1 Critical 簇 #1(A1-C1+A4-C1+A3-M1+A2-M2)想根治的"退化成每周期自动 push/dispatch 循环"那个后果,只是**触发路径换了一条**(不是 R1 抓到的 `clear+write` 路径,而是 `write_gate_state` 自身重建字典时漏字段)。

**实测证据**: `sed -n '115,155p' gate_state_helper.py` 确认末尾字典是字面量整体赋值(非 `existing.copy()` 后 `update`);对照 SC-11 四个子项逐条核对——(a) 只测「连续 3 次 wait 用同一次 write 序列跑 no_run_observations 计数」,不涉及 `mark_no_run_escalation_done`;(b) 只测 `should_escalate_no_run` 纯函数在**手工构造**的 `state` 上的行为,不经过 `write_gate_state`;(c) 只测 `mark_no_run_escalation_done` 单次调用后三个既有字段不变,**不再调用一次 `write_gate_state` 检查 `no_run_escalation_done` 是否还是 true**;(d) 只测 v1.1 旧 state 缺字段时 `.get` 默认值。四项拼起来没有一条覆盖「mark 之后再 write 一次,done 是否还留着」这个序列。

**建议**: 在 SC-11 补一条 (e):「`write_gate_state(...) → mark_no_run_escalation_done(state) → write_gate_state(gate_error_kind="no-run-for-branch", ...)`(模拟处方后仍判同 kind 的下一轮)后,`no_run_escalation_done` 仍为 `true` 且 `no_run_observations` 从 0 重新计数(不因刚归零就再次满足 `should_escalate_no_run`)」;并在 §3.1 `write_gate_state` 改动描述里显式点名「`no_run_escalation_done` 必须复用 `started_at` 的『先读 existing 再写回新字典』模式,不能像 `no_run_observations` 那样每次重算」。

---

### [A2-R2-M2] Major — §5 指示模板加 `no_run_escalation_observations`,但全文无一处指示同步加进 Python `DEFAULT_CONFIG`;已启用的 `config-template-key-currency` state-check 因此会转红(已实测复现)

**锚点**: proposal §5(`.aria/config.template.json:73-91` 行「加 `no_run_escalation_observations`」)+ `pre_merge_gate.py:55-64`(`DEFAULT_CONFIG` 字面量,不含该键,`python3 -c` 直接打印验证)+ `.aria/state-checks.yaml:244-262`(`config-template-key-currency`,`enabled: true`, `severity: warning`)+ `.aria/probes/config-template-key-currency.py:73`(`unknown = sorted(set(sec) - set(pmg.DEFAULT_CONFIG) - {"_comment"})`)。

**问题**: 这条探针的判定方向是「模板键 ⊆ `DEFAULT_CONFIG`」——模板里出现任何不在 `DEFAULT_CONFIG` 里的键即 FAIL(正是我 R1 A2-m2 指出的"探针单向,只防模板漏键不防模板多键"里那个**探针确实会管**的方向)。v2 §5 采纳了 A2-m2 的建议,在文档同步面清单里加了「`.aria/config.template.json` 加 `no_run_escalation_observations`」——但通读全文(`grep -n "DEFAULT_CONFIG" proposal.md` 零命中),**没有任何一处**指示把这个新键同步写进 `pre_merge_gate.py` 的 `DEFAULT_CONFIG` 字面量。如果实现者严格按 §5 清单逐项落地(这正是清单存在的目的——机械核对不漏项),会精确地只改模板、不改 `DEFAULT_CONFIG`,产生「模板有、`DEFAULT_CONFIG` 无」的新键,直接撞上这条探针的 FAIL 条件。

**实测证据**:
```
$ python3 -c "import sys; sys.path.insert(0,'aria/skills/phase-c-integrator/scripts'); import pre_merge_gate as pmg; print(sorted(pmg.DEFAULT_CONFIG))"
['ci_backends', 'enabled', 'no_ci_fallback', 'path_coverage_enabled', 'poll_chunk_seconds', 'primitive_call_timeout_seconds', 'user_escape_hatch', 'wait_check_intervals', 'wait_timeout_seconds']
```
（确认当前无此键）。用合成模板(在既有模板基础上加 `"no_run_escalation_observations": 3`)直接跑探针:
```
$ python3 .aria/probes/config-template-key-currency.py --template <合成文件>
FAIL unknown key(s) not in DEFAULT_CONFIG: no_run_escalation_observations
```
（复现 FAIL,退出码 1)。该探针在 `.aria/state-checks.yaml:244` 确认 `enabled: true`(severity: warning,非阻断,但按 Rule #10 属已启用检查点,不应被本 spec 静默引入新的必然 FAIL)。SC-14(文档机检)只断言「`config.template.json` 含两 key」,不覆盖「`DEFAULT_CONFIG` 也含它」这个方向,SC 全集里也没有任何一条会跑这条既有探针本身。

**建议**: 在 §5(或代码落点清单)显式加一行:「`pre_merge_gate.py` `DEFAULT_CONFIG` 字面量加 `"no_run_escalation_observations": 3`(先例: `path_coverage_enabled` 引入 #122 时的同款登记)」;SC-14 加一句「运行 `.aria/probes/config-template-key-currency.py` 需 exit 0(或直接断言 `no_run_escalation_observations` in `pmg.DEFAULT_CONFIG`)」作为机械兜底,避免这条已启用的检查点在本 spec 落地后首次被绊倒才发现。

---

### [A2-R2-m1] Minor — v2 §4"R1 A3-m1 勘正"仍是错的: 实际终态 reason 只有 8 个(7 规则终态 + internal-error),不是 9

**锚点**: proposal §4(「reason 封闭集(**9 个** = 8 规则终态 + `internal-error`,R1 A3-m1 勘正)」)+ `path_coverage.py:23-33`(判定规则 1-8,其中规则 5「逐 workflow 解析」明确标注「中间步骤,不产终态」)。

**问题**: R1 A3-m1(我未参与该发现,但属于我这次要核对的"表是否真封闭"任务)指出基线 docstring「封闭集共 9 个」与代码实际的 8 个前缀矛盾,建议二选一澄清。v2 §4 给出的"勘正"是「9 个 = 8 规则终态 + internal-error」——但规则 1-8 里只有 7 条(1/2/3/4/6/7/8;规则 5 是中间步骤不产生 reason)产生终态 reason,7+1(internal-error)= **8**,不是 9。这是同一处数字错误换了个"看似解释得通"的公式又抄了一遍,并未真正勘正。

对照 §2.2 message 表按 `(decision, reason)` 实际枚举: `covered`={empty-diff, workflow-files-changed, workflow-trigger-matched}=3;`unknown`={git-diff-failed, workflow-parse-failed, internal-error}=3;`not_applicable`={no-workflow-files, no-triggering-paths}=2(结构上不可达);合计 3+3+2=**8**,与我直接 grep 代码得到的 8 个前缀完全吻合。§2.2 的表本身(按真实 8 个 reason + `pc=None` 非 reason 场景共 9 个"场景",逐格恰好落在表的 6 行里)是**封闭且不重不漏的**——问题纯粹在"9 vs 8"这句解释性文字,不影响表的可执行性(SC-9 独立对真代码做参数化断言,不会因这句文字錯而产生假绿假红)。

**建议**: 把 §4 与 SC-2/SC-9 里的「9」统一改成「8(7 规则终态 + internal-error)」,或者如果作者原意是"8 个 reason + `path_coverage=None` 这个额外分支合计 9 个测试场景",则应明确写成"8 reason(测试场景数=8+1=9,含 pc=None)"而不是让读者以为 reason 本身有 9 个。纯措辞层面,不建议单独起 AB,descriptive substitute 即可。

---

### [A2-R2-m2] Minor — §3.3「校验只在 `gate_check` cfg 合并后」引用 SC-10 作为依据,但验证该行为的实际是 SC-3

**锚点**: proposal §3.3 config 段(「非 int / <2 → 回落默认 + `warnings.warn` (**SC-10**)」)vs SC 表(`SC-3` 才是「`escalate_after_observations` == 校验后生效值...1/0/x/None→3 + warnings.warn」;`SC-10` 实际内容是「PR 分支消歧」,与阈值校验无关)。

**问题**: 纯交叉引用错标,大概率是 R1 吸收多簇时的复制粘贴错位(此段落紧邻大量 SC 编号重排)。不影响实现正确性(实现者会去读 SC 表本身,而非仅凭这一个内联引用),但会让读者在核对"这句配置校验规则由哪条 SC 把关"时对错行。

**建议**: 把该处 `(SC-10)` 改成 `(SC-3)`。

---

### [A2-R2-m3] Minor — SC-5/SC-10 的 `gate_check` 端到端测试只点名 mock `_verify_branch_exists`,未显式说明仍需依赖既有 `_ProbeCacheResetMixin.setUp()` 里对旧名 `_verify_main_branch_exists` 的全局 mock,否则会触发真实 `git ls-remote` 子进程

**锚点**: proposal §2.3(`_verify_main_branch_exists` 泛化为 `_verify_branch_exists`,旧名保留为别名,「既有调用/测试不改」)+ SC-5/SC-10 表格文字(均只写「mock `_verify_branch_exists` 为 ok」)+ `pre_merge_gate.py:449`(`gate_check` 里 main 分支核验调用**逐字不变**、仍是 `_verify_main_branch_exists(...)`,在 (a)/(b) 轴查询之前**无条件执行**)+ `tests/test_pre_merge_gate.py:75-89`(`_ProbeCacheResetMixin.setUp()` 已全局 `mock.patch.object(gate, "_verify_main_branch_exists", return_value=("ok",""))`,注释明说该核验对每次 `gate_check` 发一次真实 `git ls-remote`,实测单次 8.7 秒)。

**问题**: `gate_check` 里 main 分支核验的调用点本 spec 明确不改名(仍是 `_verify_main_branch_exists`),所以任何要跑到 `pr_ci_status=not_found` 分支的 `gate_check(...)` 级测试(SC-5、SC-10)都必须让这次 main-branch 核验先返回 `ok`,否则会在到达 (a)/(b) 轴查询之前就被 main 核验短路掉(判 fail,`kind=main-branch-*`),根本进不到要测的代码路径;若恰好实现者没有意识到需要这层 mock,又恰巧在真实 git 仓(本仓)里跑测试且 `main_branch`/`remote` 参数凑巧对应一个真实存在的分支,`_verify_main_branch_exists` 未 mock 时会退化成一次真实网络 `git ls-remote` ——要么在无网络的 CI 沙箱里直接失败/超时,要么"意外地"因为真分支存在而 accidentally 通过,把测试的确定性建立在仓库当前真实分支状态上。

好消息(降级为 Minor 的理由): 只要新测试沿用既有惯例、放进继承 `_ProbeCacheResetMixin` 的测试类(现有 `PathCoverageGateTests`/`GateCheckTests` 皆如此),`setUp()` 已经全局处理了这层 mock,新测试作者只需要**额外**再 mock `_verify_branch_exists` 一次(用于控制 pr_branch 侧结果),不需要自己重新发明 main-branch 的 mock。这是"能落地正确、但依赖读者知道有这个既有 mixin 机制"的隐性依赖,不是"必然写错"。

**建议**: 在 SC-5/SC-10 表格里补一句「沿用 `_ProbeCacheResetMixin`(main 分支核验已由 `setUp()` 统一 mock 为 ok),本条只需额外 mock `_verify_branch_exists`」,消除"新测试是否需要自己再 mock 一次旧名"的疑问。

## 未发现问题但已核验的点

- `compute_verdict` 新增 `pr_branch_check` 形参与既有测试调用签名兼容性:实测 `grep -n "compute_verdict(" test_pre_merge_gate.py` 全部 6 处调用(4 处纯位置参数 `[]`/`[{"run_id":1}]` + 2 处 kwargs `backend_name=`/`path_coverage=`),均未使用超过当前 5 个形参的位置调用,新增第 6 个带默认值的尾部形参不破坏任何一处。
- `should_escalate_no_run(state, threshold)` 与 `mark_no_run_escalation_done(state)` 的公式/字段读写与 SC-11(b)/(c) 逐字对齐,机械上可直接实现,无隐藏依赖。
- `_migrate_state`(v1.0→v1.1)在 `format_version` 已是 `"1.1"` 时是 no-op,`gate_state` 内新增两个 additive 键不触发也不需要新的 migration 分支;`format_version` 不 bump 的决定与既有 migrate 代码结构兼容(旧文件读入后两新字段经 `.get()` 防御性缺省,SC-11(d) 覆盖)。
- 2.1 elif 插入位置的伪码 + 防呆注释指令,与我 R1 用「误序 vs 正确顺序」模拟实证的失败模式(`not_found + main_inflight 非空 → gate_error 被吞`)完全对应,SC-4 现在显式要求断言 `gate_error.kind`(不能只查 `verdict==wait`)。
- `_no_run_gate_error(path_coverage, cfg, pr_branch_check)` 是 `compute_verdict` 内部唯一产出 `gate_error`(not_found 分支)的函数,`gate_check` 与直调测试(SC-2/3/4)共享同一调用路径,不存在 R1 A2-M3 所指的"两套独立校验逻辑"分叉风险。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 2 Major / 3 Minor)

vote: REVISE — 归我席的全部 R1 簇已真实收敛,但 R2 新鲜眼睛发现 2 处新 Major:一处(A2-R2-M1)是 R1 Critical 簇"至多一次升级"不变量的同形姊妹坑(触发路径不同,后果相同——退化成循环 dispatch/commit),另一处(A2-R2-M2)是机械可复现的既有 state-check 回归(已实测 FAIL)。两处都可通过给 SC-11 补一条子项 + 给 §5 补一行 DEFAULT_CONFIG 登记来收敛,不需要推翻设计;若这两处被吸收,我这一席倾向下一轮 PASS。
