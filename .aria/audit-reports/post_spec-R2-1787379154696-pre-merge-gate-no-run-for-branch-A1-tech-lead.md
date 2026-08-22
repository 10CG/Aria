---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-22T07:20:42.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 1
major_count: 6
minor_count: 6
---

## 摘要

v2 的**显影半边** (§1 backend `not_found` / §2.1 插入位置 / §2.2 五档 message 封闭表 / §2.3 PR 分支消歧 / §4 `dispatchable_workflows`) 我这轮逐条复核, **质量很高**: 归我席的 10 个簇里 6 个真闭 (#3 #6 #8 #10 #12 #17), 且 #12 的红窗声明我直调复跑确认 (`compute_verdict([{'run_id':1}], 'not_found')` 基线已是 `wait` ⇒ 红窗确在 `kind`)。#8 的 (b) 轴措辞三处 (§1 / Impact / Out of Scope) 一致改成 scope 声明, 没有残留「正确语义」的断言。

问题**全部集中在处方/升级那半边 (§3)**, 而且是同一个根:

**§3 把「判定单点 + 计数单点」建在 `gate_state_helper.py` 上, 但这个文件在运行时零消费方。** 我实测: `grep -rn "gate_state_helper|write_gate_state" aria/skills --include=*.md` → **零命中**; `grep -rn "import gate_state_helper" aria/` → 只有它自己的测试。`workflow-runner/SKILL.md` 全文不出现 `scripts/` / `.py` / `helper` 任何一处 (对照: `phase-c-integrator/SKILL.md:270` 明写「**Helper 实现**: `scripts/pre_merge_gate.py`」)。helper 自己的 docstring 逐字说「the actual workflow-runner skill is **markdown-driven (LLM caller handles state)**; this helper exists **so the behavior is testable** and serves as a canonical **reference** for any re-implementer」。⇒ AD-7 的两个「单点」是**文档级**的, 不是运行时级的; SC-11 的四条断言会在一段生产从不执行的代码上变绿。

由此派生的 6 条 Major 里有 5 条 (M1/M2/M4/M6 + 部分 M5) 都是「这台机器不存在」的下游症状: 一次性守卫可被抹掉且无 SC 守 (M1, 已实测 `write_gate_state` 整体重建 `gate_state` 会静默丢弃未知键)、求值/自增顺序仍欠定致 90s vs 210s 分叉 (M2, R1-M1 的同一个 off-by-one 换了个量重犯)、NEG-4 对三条点名行为中的两条结构上不可证伪 (M4)、2.6 的 continue 语义空缺 (M6)。

诚实标注边际产出: 我这轮 6 条 Major **6/6 都是 v2 自己的 fix 引入的**, 按 memory `audit_marginal_return_goes_negative` 的判据 (本轮 fix 引入的 major 占比 > 1/2) 已到拐点 —— 再加同一批席位的轮次预期净负。所以我在 Verdict 里给的不是「再修一轮」, 而是一个**缩短距离**的范围选项 (见末段), 请一并上呈 owner。

Vote **REVISE**。

---

## R1 处置核对

| 簇# | 状态 | 证据 |
|---|---|---|
| **#1** (A1-C1 一次性守卫) | **partial** | 语义三件都写对了: 2.5 判定含 `not no_run_escalation_done` (至多一次) / `mark_no_run_escalation_done` 不触碰 `started_at` (SC-11c 钉死) / 2.6 处方后再命中交人。但守卫的**载体**在两处可被抹掉, 且无 SC 覆盖 → R2-M1; 且判定/计数的运行时不存在 → R2-C1 |
| **#2** (A1-M1 计数量与时刻) | **partial** | 量换对了 (`no_run_observations` 含初次, 键名同量); 默认 3 ↔ t≈90 的算术在「先写后判」下成立 (我按 `wait_check_intervals=[30,60,...]` 重推: 初次 t=0 obs=1 / 重查#1 t≈30 obs=2 / 重查#2 t≈90 obs=3 ✓)。**但求值相对自增的顺序仍未钉**, 而现有 SKILL.md 步骤序给出的是「求值在前」⇒ t≈210 → R2-M2 |
| **#3** (A1-M4 有记录无路由) | **closed** | `gate_error_kind` 字段确已删除 (3.2 明写「不加」), 改为 `write_gate_state` 的**入参**; 判定式真消费 `no_run_observations`; 「episode 内 `not_found` 单调」入 traps §6 (§5 表 + F4)。⚠️ 同一形状在 TASK-0 失败分支上会复发 → R2-M5 |
| **#6** (A1-M2 message 键) | **closed** | 2.2 按 `(decision, reason)` 五档封闭表; `empty-diff` 行**不含** `#152` 且 `remedies=[]`; `workflow-files-changed` 行明示 matched 恒 `[]` 且禁扩全量; pc=None 单列; SC-2 参数化到全 reason + SC-5 拆 enabled/disabled 两变体。残留: reason 三个是前缀族 → R2-m1 |
| **#7** (A1-M5 PR 分支消歧) | **partial** | 2.3 三分支处置与 #137 三禁令**一致** —— 我实读 `_verify_main_branch_exists` (`:302-352`) 函数体确与 "main" 无关, 判据落在**解析出的 ref 名列表精确比对** (`target in ref_names`), 泛化改名不动这三条。插入点**唯一可推** (`pr_status.state` 只在 `query_pr_ci` 返回后存在 ⇒ 只能落 `:509` 的 try/except 结束 (`:519`) 与末尾 `compute_verdict` (`:521`) 之间)。但 2.1 伪码与 2.3 冲突 → R2-M3; `pr_branch_check` 形状与副本通道未定 → R2-m2 |
| **#8** (A1-M6 (b) 轴 scope) | **closed** | §1 第一 bullet 逐字为「这是 scope 声明, 不是正确性声明」并**主动承认**同形分钟级 fail-open; Impact 改「**不改 (非「不受影响」)**」; Out of Scope 与 traps §6 与 Phase D issue 三处口径一致。无残留正确性断言 |
| **#9** (A1-M3 Rule #6) | **partial** | 已改判据表第三行 + 点名行为 + 缺口 issue + fixtures 数 6→**7** 勘正 + 引 NEG-3 先例。但定向 fixture 对三条点名行为中的**两条**结构上不可证伪, 且漏登记 manifest → R2-M4 |
| **#10** (阈值依据 / SC-13 flaky) | **closed** | SC-13 改「轮询至非 `not_found` 或 600s」+ 记 Δt 作 AD-4 首个数据点; AD-4 论证从「阈值准」改成「**代价有界**」。⚠️ 「代价有界」整个挂在 #1 的一次性守卫上, 守卫破则本条回退 |
| **#12** (A2-M1 插入位置) | **closed** | 2.1 明写「`not_applicable` 之后、`main_in_flight_runs` 之前」+ 要求代码内防呆注释; SC-4 红窗改「红在 kind」。我直调基线复跑: `compute_verdict([{'run_id':1}], 'not_found')` → `wait` (verdict 侧无红窗), `compute_verdict([], 'not_found')` → `green` (§1 单独落地的 fail-open 属实) |
| **#17** (我的 6 条 minor) | **closed 6/6** | m1 六键措辞 → 2.2 尾注 +「main 核验那支本就是七键」+ SC-7 括注; m2 pc=None 处方 1 不可用 → 2.2 表该行 `remedies=["commit"]`; m3 伪码穿 `gate_error` + `_result` 调用点 → 2.1 补 `return _build_output(..., gate_error=gate_error)` / §4 改「规则 6 的调用点**必改**, 其余 8 个不改」(我复数确认 `_result` 调用点确为 9 处); m4 SC-13 → 见 #10; m5 dispatch 绕过 `CIBackend` → AD-5 明写 + Out of Scope; m6 AD-1 转述 → Why 段与 AD-1 都改成「信号相同 (R1 A1-m6 勘正), 分歧在落点与处置」 |

**统计**: closed 6 / partial 4 / not_addressed 0。

---

## 新 Findings

### [A1-R2-C1] Critical — AD-7 的「判定单点 + 计数单点」建在一个运行时零消费方的 helper 上; §3 的整台机器在生产路径上不存在

**锚点**
- Spec AD-7 (`proposal.md:187`): 「升级判定只存在于 workflow-runner 2.5 且**机械实现为** `should_escalate_no_run`; 计数只在 `write_gate_state` 内」
- Spec §3.1 (`:126`): 「`should_escalate_no_run(...)` —— 这是 2.5 判定的**唯一**机械实现, SKILL 散文**引用它**而非重述」
- Spec §5 (`:171`): workflow-runner SKILL.md `:389` 改动写作「**调** `write_gate_state(gate_error_kind=...)`」
- `aria/skills/workflow-runner/scripts/gate_state_helper.py:9-12` (docstring)

**实测证据** (全部本轮实跑, 基线 `400f0bc`)
```
$ grep -rn "gate_state_helper\|write_gate_state\|should_check_now\|is_gate_active" aria/skills --include=*.md
(无输出)
$ grep -rn "import gate_state_helper\|from gate_state_helper" aria/
aria/skills/workflow-runner/tests/test_gate_state_helper.py:19
aria/skills/workflow-runner/scripts/gate_state_helper.py:14   ← 自己 docstring 里的 usage 示例
$ grep -n "scripts/\|\.py\|helper" aria/skills/workflow-runner/SKILL.md
(无输出)
```
helper docstring `:9-12` 逐字: 「the actual workflow-runner skill is **markdown-driven (LLM caller handles state)**; this helper exists **so the behavior is testable** and serves as a canonical **reference** for any re-implementer.」

对照组: `phase-c-integrator/SKILL.md:270` 有「**Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py`」—— 那条 SKILL 是真把算法委托给脚本的; workflow-runner **没有**任何等价句子。

**问题**
运行时的判定者是 LLM 读 `workflow-runner/SKILL.md` 的散文, 运行时的计数者是 LLM 自己写 `workflow-state.json`。`should_escalate_no_run` / `write_gate_state` 今天不被任何生产路径调用。于是:

1. **「单一计数点」没有任何机制支撑。** 「含初次」「非同 kind 归零」都只是散文约定, 两次 LLM 运行可以给出不同的 `no_run_observations`。R1 #2 要治的欠定被搬了个家, 没被消灭。
2. **SC-11 是在不可达代码上取绿。** 四条子断言 (a)(b)(c)(d) 全部只跑 helper 函数; 生产行为 (LLM 按散文写 JSON) 零覆盖。memory `completion_signals_vs_runtime_invocation` 逐字命中 (「单测/structural benchmark ≠ 代码真被生产调用; 集成型验 runtime invocation」)。
3. **AD-7 引 traps §五 是误引。** traps §五 (`references/pre-merge-gate-empirical-traps.md:44-51`) 讲的**不是**「判定在两个 Skill 各写一遍」, 它逐字讲的是「SKILL.md §C.2.4 里那条『AI 照着敲命令』的散文流程是**同一算法的第二份实现**, 它没有这道核验 ⇒ 不得据本次修复认为 #137 已闭环」。AD-7 说「两份实现的病 (traps §五) 不再犯」, 而 §五 那个病 (**代码实现 vs SKILL 散文实现**) 恰恰是本 spec 正在扩大的那个 —— §3.3 又往 §C.2.4 步骤 4/5 追加了一份 verdict 映射散文。memory `delegate-verify` / `cite≠apply` 正指这种「引一行说它讲的就是这件事」。
4. **§5 把一个运行时接线改动藏在文档同步表的一行里。** 「workflow-runner SKILL.md `:389` → **调** `write_gate_state(gate_error_kind=...)`」如果照字面实施, 是把 workflow-runner 从「LLM 自己写 JSON」改成「LLM shell out 到 python helper」—— 这是该 Skill 的**运行时契约变更**, 却没有 AD、没进 Impact「行为变化面」、没有 SC、也不在 rule6_note 的点名行为里。同时 2.5 那边只说「散文**引用它**」(≠ 调用), 两处不同构。

**按 spec 实施会怎样错**: 实施者跑完 SC-1~SC-15 全绿、AB NEG-4 也绿, 但真实 168h 无人值守跑里, 「至多一次」「阈值 3」「非同 kind 归零」有没有被执行**没有任何机械保证**, 也没有任何信号会发红。R1-C1 (外向、难撤销的自动 push/dispatch) 的唯一护栏因此是纸面的。

**建议** (三选一, 须显式选定并写进 AD)
- (a) **真接线**: 在 `workflow-runner/SKILL.md` 加与 `phase-c-integrator/SKILL.md:270` 同形的「Helper 实现」句, 明写 wait 分支与 2.5 判定**必须**经 `gate_state_helper` 执行 (`python3 scripts/gate_state_helper.py ...` 或等价), 并补一条能验「helper 真被调用」的 SC (例如活体跑后断言 `workflow-state.json` 的 `integrity.state_hash` 与 helper 计算值一致 —— 手写 JSON 算不出它)。这条同时顺手治了 traps §五 点名的老病。
- (b) **承认是散文机器**: 删掉 AD-7 里「机械实现」「单点」的措辞, 改成「散文规范 + helper 为参考实现」, 并把 SC-11 的定位从「验证」降级为「参考实现自洽性」, 在 rule6_note 里把 2.5/2.6 列为**无机械验证面**的行为 (进而影响 M4 的处置)。
- (c) 把 §3 整体移出本 spec (见 Verdict 末段的范围选项)。

---

### [A1-R2-M1] Major — 「每 episode 至多一次」的守卫位在两条路径上会被静默抹掉, 且没有任何 SC 断言它活下来

**锚点**: Spec §3.1 (`:125` 「`no_run_escalation_done` 跨 wait 写保持, `is_first` 时 false」/ `:127` `mark_no_run_escalation_done`); SC-11 (`:210`); `gate_state_helper.py:115-155` (`write_gate_state`)

**实测证据** (本轮实跑)
```
$ python3 -c "... st={}; gs.write_gate_state(st,name='C.2.4',verdict='waiting');
              st['gate_state']['no_run_observations']=1;
              gs.write_gate_state(st,name='C.2.4',verdict='waiting');
              print(sorted(st['gate_state'].keys()))"
['in_flight_runs','name','next_check_at','primitive_used','raw_message','retry_count','started_at','status']
extra field survived? False
```
`write_gate_state` 是**整块重建**: `state["gate_state"] = { ...固定 8 键... }`, 任何 additive 键在下一次写时被静默丢弃。

**问题** 两条独立路径都能让「至多一次」退回「每次都可以」:

1. **写覆盖**: spec 已预见并要求「跨 wait 写保持」(措辞正确), 但 **SC-11 里没有一条断言这件事** —— (a) 只测 obs 的 1/2/3 与归零; (b) 只测 `should_escalate_no_run` 在给定 state 上的取值; (c) 只测 `mark` 不触碰另外三个字段; (d) 只测旧 state 缺字段时 `.get` 默认。**「`mark` 之后再 `write_gate_state`, `done` 仍为 true」这条序列没有测**, 而它恰是唯一会被基线实现 (整块重建) 破坏的那条。memory `test_asserts_what_its_name_claims` 的判据「它怎么会红?」: SC-11 现有四条对这个缺陷全都不会红。
2. **不落盘**: `mark_no_run_escalation_done(state)` 与 `clear_gate_state(state)` / `write_gate_state(state, ...)` 同形 —— 只改内存 dict, 落盘要另调 `atomic_write_state`。2.5 逐字只说「执行后 `mark_no_run_escalation_done`, 回到 polling loop」, 没说落盘。于是磁盘上的状态在处方执行后仍是 `obs=3, done=false` (= **已武装, 立即可再升级**), 而这个窗口有 ≥ `intervals[3]=300s` 那么宽, 且 workflow-runner 的 Ctrl-C 检测 (exit condition 1, 最高优先级) 正是设计来在这段 sleep 里生效的。具体复现: t≈90 升级 (dispatch/commit) → `mark` (仅内存) → sleep 300s → t≈95 Ctrl-C → suspended → resume (Resume 语义 §2「已过期 → 立即重新调 C.2.4 gate」) → 加载磁盘 state (`done=false`, `obs=3`) → 2.5 再次成立 → **第二次 dispatch / 第二次 push commit**。每一次 interrupt+resume 加一次。

**按 spec 实施会怎样错**: R1-C1 被关掉的那个后果 (对双 remote 镜像仓的 feature 分支重复自动 push) 在 v2 自己新建的守卫路径上原样复发 —— memory `fix_recurs_in_its_own_fallback_path` 的教科书形状。

**建议**: (i) SC-11 加第 (e) 条: `mark_no_run_escalation_done` → `write_gate_state(verdict='waiting', gate_error_kind='no-run-for-branch')` → 断言 `done is True` **且** `no_run_observations == 1`; 坏实现 = 基线整块重建 (不 carry-forward), 此条必红 —— 这条同时给出「它怎么会红」的答案。(ii) 3.1 明写 `mark_no_run_escalation_done` 后**必须立即 `atomic_write_state` 再执行处方** (先落盘后动手, fail-closed 顺序), 并在 2.5 里逐字写这个顺序。

---

### [A1-R2-M2] Major — 「求值 vs 自增」的顺序仍未钉死; 按现有 SKILL.md 的步骤序读, 默认 3 落在 t≈210 而不是 spec 声称的 t≈90 (R1-M1 的 off-by-one 换了个量重犯)

**锚点**
- Spec §3.1 (`:125`): 「仅此函数自增/归零 `no_run_observations` (**单一计数点 — 解决 R1 #2 的「自增在 verdict 前/后」欠定**)」
- Spec §3.3 config (`:146`): 「默认 **3** (含初次 ⇒ 默认在首次 gate 调用后 **~90s**: 初次 t=0 + 重查 #1 t≈30 + 重查 #2 t≈90)」
- `workflow-runner/SKILL.md:332-336` (Exit conditions), `:338-357` (实施步骤 3a-3d: 「d. **处理 verdict 按 exit conditions 优先级**」), `:389` (Resume §3 「`wait` → **增量更新** `gate_state.retry_count` + `next_check_at`, 继续 polling」)

**问题** 「单一计数点」解决的是**谁**自增, 不是**何时**求值。2.5 的求值发生在实施步骤 **3d** (exit conditions), 自增发生在 wait 分支的「增量更新」(`:389`) —— 这是**两个不同的步骤**, 而 SKILL.md 把 exit conditions 放在 3d 的**开头**, 「增量更新…继续 polling」是 wait 落地后的动作。按这个字面序展开:

| 事件 | t | 求值时磁盘/内存 obs | `obs >= 3`? | 求值后写入 |
|---|---|---|---|---|
| 初次 gate → wait (步骤 2 建 gate_state) | 0 | — (未过 exit conditions) | — | obs=1 |
| 重查 #1 (sleep `intervals[0]`=30) | ≈30 | 1 | 否 | obs=2 |
| 重查 #2 (sleep `intervals[1]`=60) | ≈90 | 2 | **否** | obs=3 |
| 重查 #3 (sleep `intervals[2]`=120) | ≈210 | 3 | **是** | — |

⇒ **t≈210**, 与 R1-M1 算出的数字**一模一样**。spec 声称的 t≈90 只在「本轮先写后判」时成立。

**按 spec 实施会怎样错**: 两个实施者分叉 (90s vs 210s), 而 AD-4「误升级代价有界」的整段论证与 config 注释里的 `~90s` 都只覆盖其中一个; TASK-0 要拿的 Δt 数据点也无法与阈值对齐 (「若 Δt p90 > 90s, 默认提到 4 (对应 ~210s)」这句在另一种读法下自相矛盾 —— 4 在「先判后写」下是 ~510s)。更糟的是 spec **明文宣称这个欠定已被解决**, 下一个读者不会再去核。SC-11 只测 helper 单调自增, 结构上测不到编排层的求值时点 (且见 C1: 编排层根本不是代码)。memory `perpetual_red_fix_must_change_the_quantity_not_the_threshold` 的反面教材 —— 换了量, 没换那个真正欠定的维度。

**建议**: 在 §3.2 的 2.5 前加一句零歧义的时序断言, 例如「**本轮 gate 返回后先 `write_gate_state`(含自增/归零) 并落盘, 再求值 exit conditions 1→2→2.5→2.6→3→4**」, 并同步改 `workflow-runner/SKILL.md` 实施步骤 3d 的措辞 (§5 表里给 `:332-336` 与 `:389` 两处加这条约束)。然后把 3.3 的秒数表 (t=0/30/90) 与 AD-4 的「Δt p90 > 90s → 提到 4」逐字重算一遍并写进 spec。

---

### [A1-R2-M3] Major — 2.1 伪码把 `verdict = VERDICT_WAIT` 写死, 与 2.3 的「PR 分支不存在 → `verdict=fail`」直接冲突 (两个簇的 fix 之间的接缝)

**锚点**: Spec 2.1 (`:62-65`) vs Spec 2.3 表第 2 行 (`:102`)

2.1 的伪码逐字:
```python
elif pr_ci_status == "not_found":
    verdict = VERDICT_WAIT                      # 不论 main in-flight 与否 ((a) 轴未知态)
    gate_error = _no_run_gate_error(path_coverage, cfg, pr_branch_check)   # 见 2.2 / 2.3
    raw_message = gate_error["message"]
```
2.3 表逐字: `not-found` → 「`verdict=fail` + `gate_error.kind = "pr-branch-not-found"`」。

**问题** 2.1 被 spec 自己标注为「**插入位置承重**」的规范性伪码 (还要求把注释抄进代码), 但它在 `pr_branch_check == not-found` 时给出的 verdict 是 `wait`, 与 2.3 相反。`_no_run_gate_error` 这个名字也只承诺产 `no-run-for-branch`, 没说它会改 verdict 或产第二个 kind。一个照 2.1 实施的人得到「PR 分支不存在也 wait」, 一个照 2.3 实施的人得到 fail。

这是 memory `fixes_contradict_each_other_across_clusters` 的形状: 簇 #12 的 fix (钉死伪码与插入位置) 与簇 #7 的 fix (新增 fail 分支) 各自单看都对, 后者违反了前者伪码的隐含前提 (「这条分支恒 wait」)。R1 的分席审计不会抓它 —— 接缝落在两个角度之间。

**缓解 (诚实标注)**: SC-10 第一句会红 (它断言 `verdict=fail` + `kind=pr-branch-not-found`), 所以不会 ship 出去。定 Major 而非 Critical 的理由在此; 但 2.1 是本 spec 唯一的规范性伪码且要求逐字抄注释, 让它留着一句与 SC 相反的断言, 代价不对称。

**建议**: 2.1 伪码改成三行分支 (`pr_branch_check` 为 `not-found` → `verdict = VERDICT_FAIL` + `kind="pr-branch-not-found"`; 其余 → `WAIT`), 或把 verdict 的产出也收进 `_no_run_gate_error` 的返回值并改名 (例如 `_not_found_gate_outcome(...) -> (verdict, gate_error)`), 名字与职责对齐。

---

### [A1-R2-M4] Major — NEG-4 对 rule6_note 三条点名行为中的**两条**结构上不可证伪 (序列型 fixture 无 consumer, 实测), 且未登记进 manifest ⇒ 判据表第三行第 2 条义务未达成

**锚点**: Spec rule6_note (`:218`) 三条义务与三条点名行为; SC-15 (`:214`); 代码落点行 (`:16`) 只列 `.../phase-c-integrator-pre-merge-gate-fixtures/NEG-4-no-run-for-branch.json`

**实测证据** (本轮实跑)
1. 套件是**两件套**: 目录 `ab-suite/phase-c-integrator-pre-merge-gate-fixtures/` (7 个 per-fixture json) **+** 清单 `ab-suite/phase-c-integrator-pre-merge-gate.json` (含 `fixtures[]` 数组, 每项 `id/file/expected_verdict/test_case_in_unit_tests/purpose`, 另有 `version` 与 `changelog`)。先例 NEG-3 是**两处都加**的 (清单 `fixtures[6]` 逐字在场, `version` 已从 1.0.0 → 1.1.0)。v2 只列了文件, **没列清单登记**。未登记的 fixture 文件不会被枚举 ⇒ 义务纸面达成 (memory `completion_signals_vs_runtime_invocation`)。
2. 三条点名行为里, 只有第一条 (`kind=no-run-for-branch` 时 surface 原文、不得写通用「CI pending」) 可由 NEG-3 那种**单帧 gate 输出**型 fixture 证伪。另两条 (「在 2.5 成立时执行一次处方而非等满 1800s」「2.6 成立时交人」) 本质是**多轮序列 + 持久状态**行为, 需要 `wait_then_green` 那种 `_sequence` 形态。而 `wait_then_green.json` 自己逐字写着:
   > `"_status": "ASPIRATIONAL — integration test pending"` … `"_consumed_by": "**Currently no consumer.** When the mock-injection mechanism ships…"` … 「Requires a mock-injection mechanism in pre_merge_gate.py (e.g. `ARIA_AETHER_MOCK_RESPONSE_FILE` env var with sequence stepping) that **does NOT yet exist**」

   ⇒ 序列型 fixture 在本套件里**没有执行面**。NEG-4 若写成序列形, 与 `wait_then_green` 同命 (再造一个无人消费的 ASPIRATIONAL 文件); 若写成单帧形, 它证伪不了那两条行为。
3. 附带: 两条不可证伪的行为属 **workflow-runner** 的指令面, 而 fixture 被放进 **phase-c-integrator** 的套件目录 —— 归属也不对 (`workflow-runner.json` 只有 2 条 full-cycle/phase-skip eval, 无 gate 相关面)。

**问题**: 判据表第三行的三条义务是「点名行为 + 建**可证伪**定向 fixture + 套件缺口开 issue (**缺一照跑**)」。按上面的实测, 第 2 条对 2/3 的点名行为不成立 ⇒ 触发「缺一照跑」。spec 现在把三条行为打包声称已履行, 等于用一条只覆盖 1/3 的 fixture 换掉整段 AB。memory `mechanization_knob_must_match_granularity` 的处方是「诚实交付一半 (声明留痕) + 开 issue, 并**明说哪半是哪半**」。

**建议**:
- 落点补 **清单登记** (`phase-c-integrator-pre-merge-gate.json` 的 `fixtures[]` 追加一项 + `version` 1.1.0→1.2.0 + `changelog` 追加), SC-15 相应加「清单 `fixtures[]` 含 id=NEG-4 且 `file` 指向实际存在的文件」。
- rule6_note 拆两半明写: **surface 行为** → NEG-4 单帧 fixture (可证伪, 履行第三行); **2.5/2.6 升级与交人行为** → 套件**结构上无执行面** (引 `wait_then_green._consumed_by` 为证), 按「缺一照跑」处置 —— 照跑 `workflow-runner.json` + `phase-c-integrator.json` 并在 spec 里逐字写明「该绿不覆盖 2.5/2.6」, 同时把「序列型 fixture 缺 mock-injection 机制」并进套件缺口 issue。
- (若采纳 C1 的 (c) 范围选项, 本条自动降为只剩 surface 一条行为, 处置大幅简化。)

---

### [A1-R2-M5] Major — TASK-0 失败分支只写了 AD-5/remedies 的落点, 没写 §4 / 2.2 / SC-8 / SC-9 / SC-13 怎么办 ⇒ `dispatchable_workflows` 会变成新的「有记录无路由」

**锚点**: Spec §3.4 (`:153`) 「**失败** → AD-5 改『处方 2 为主, dispatch 不列入 remedies』; `remedies_available` **永不含** `dispatch`」; §4 (`:157`); 2.2 表第 1 行的条件式 remedies; SC-8 / SC-9 / SC-13

**问题** TASK-0 是 Phase B 的**前置**任务, 它有一半概率 (403/权限/形态不同) 判定 dispatch 不可用。那一刻:
- §4 新增的 `_parse_workflow["dispatchable"]` 与 `_evaluate["dispatchable_workflows"]` **失去唯一消费方** (它们只被处方 1 与 2.2 表第 1 行的条件式读)。这正是 R1 #3 (A1-M4) 让 spec 删掉 `gate_error_kind` 的那条判据 —— 「有记录无路由 = 静默」。v2 在自己的条件分支上把它请了回来。
- 2.2 表第 1 行的「`["dispatch","commit"]` 若 `dispatchable_workflows` 非空, 否则 `["commit"]`」整条退化成恒 `["commit"]`, 但表还留着那个分叉 ⇒ SC-2 的「`remedies_available` 按 2.2 表逐档相等」在两种世界里期望值不同, spec 没说以哪个为准。
- SC-8 / SC-9 (dispatchable 的两条结构化断言) 是否还要写? SC-13 的 dispatch 半段是否还要跑? 都没说。
- §3.3 处方 1 那一整段 (含 F6 的按文件名寻址细节) 是否从 SKILL.md 删除? 没说。§5 的 14 行同步面也没有条件分支。

**按 spec 实施会怎样错**: TASK-0 失败后, 实施者最省事的读法是「AD-5 改一句话, 其余照做」—— 于是 ship 出一个解析并输出了 `dispatchable_workflows`、写了处方 1 全套文档、但代码路径永不采用的版本; 文档里留一条对读者承诺存在、实际不会执行的处方。这类残留正是下一轮审计的原料。

**建议**: §3.4 的失败分支补一张**明确的删除清单**: 「§4 的 `dispatchable` / `dispatchable_workflows` 整段撤回 (含 SC-8/SC-9); 2.2 表第 1 行 remedies 恒 `["commit"]` (条件式删除); §3.3 处方 1 整段从 SKILL.md 删除, 优先序变 2→3; SC-13 只留 `not_found` 显影半段; §5 同步面相应减 N 处」。或反过来: 明写「即使 dispatch 不可用也保留 §4, 因为 <某个别的消费方>」—— 但今天不存在这个消费方, 所以只有前者站得住。

---

### [A1-R2-M6] Major — 2.6 的「与 exit 2 同级: continue / abort」没有定义 continue 之后状态怎么变 ⇒ 要么每轮复触发 prompt, 要么退化成静默

**锚点**: Spec §3.2 的 2.6 (`:132`); `workflow-runner/SKILL.md:333` (exit condition 2) 与 `:356` (「timeout → user prompt;continue → **reset retry_count** + 继续;abort → stop」)

**问题** 2.6 的前件是 `kind == no-run-for-branch AND done == true AND obs >= threshold`。用户选 continue 之后, 这三个条件**没有任何一个会因为 continue 而改变** (spec 没说 continue 要重置 `no_run_observations`, 也没说置任何抑制位)。于是:
- 若 continue 就是「继续 polling」: 下一轮 obs=threshold+1, 三条件仍真 ⇒ **每一个 polling 周期弹一次 prompt**, 直到 exit 2 的 1800s。
- 若 continue 照 exit 2 的既有语义「**reset retry_count** + 继续」: `retry_count` 归零 ⇒ `intervals[min(retry_count,4)]` 回到 30s ⇒ prompt 频率从每 300s 变成每 30s (最坏 ~50 次)。而且这条 reset 还会把 R1-C1 明确要保住的「`retry_count` 不动」的不变量破掉 (spec 3.1 只钉了 `mark_no_run_escalation_done` 不动 `retry_count`, 没钉 2.6 的 continue)。

同时 2.6 与 2.5 的第 3 条处方 (`remedies_available == []` 时「user prompt (与 2.6 同形)」) 在 `empty-diff` 档下**会连续弹两次同形 prompt** (第一次消耗一次性预算并 `mark done=true`, 第二次由 2.6 触发), 二者的信息内容完全一样。

**按 spec 实施会怎样错**: 交互模式下 prompt 风暴; 无人值守下 (R-d: prompt == abort) 第一次就 abort, 2.6 成为死条款 —— 也就是说 spec 花了一条 exit condition 写的「交人」路径, 在它主要面向的 v2.0 运行时里由 2.5 的处方 3 抢先执行了。

**建议**: 2.6 明写三件事: (i) continue 的语义 (建议: **不重置 `retry_count`/`started_at`**, 只置一个抑制位或把 `no_run_observations` 重置并要求下一次再攒满 threshold 才能再问, 二选一并写死); (ii) abort 的落地态 (`session.status`); (iii) `remedies_available == []` 时 2.5 **不消耗一次性预算**, 直接落到 2.6 一条路径 (避免同形双 prompt) —— 或者反过来, 明写 remedies 为空时 2.5 不成立。

---

### [A1-R2-m1] Minor — reason 「封闭集 9 个」的算术仍不对 (实为 8 个族), 且其中 3 个是**前缀族**而非字面量 ⇒ 按相等匹配写 2.2 表会在生产上恒不命中

**锚点**: Spec §4 (`:157`) 「reason 封闭集 (**9 个** = 8 规则终态 + `internal-error`, R1 A3-m1 勘正)」; SC-2 / SC-9 「参数化**全 9 reason**」; `path_coverage.py:23-40` 模块 docstring

**实测**: `_result(` 调用点 **9 处** (`:422/432/447/459/464/468/493/498/506`), 但**不同的 reason 族只有 8 个** —— `git-diff-failed` 出现两次 (`_repo_root` 失败 + `git diff` 失败)。规则 1-8 中规则 5 是中间步骤不产终态 ⇒ 规则终态 7 个 + `internal-error` = 8。「8 规则终态」这个中间量本身就错了 (v2 的「勘正」把源 docstring 的同一处错误照抄了 —— memory `critique_repeats_the_error_it_names`)。

更要紧的是形态: 三个 reason 是**带载荷的前缀**, 不是字面量 —
`f"git-diff-failed: {err}"` / `"workflow-parse-failed: " + ", ".join(files)` / `f"internal-error: {type(exc).__name__}: {exc}"`。
2.2 表第 4 行要求「`internal-error` 时点明『请报 issue』」(继承 #126 的分档义务), 这必须写成 `reason.startswith("internal-error")`。若实施者按相等比对, 生产上永不命中, 而 SC-2 若用字面 `"internal-error"` 造 pc 则测试照绿 —— memory `test_mock_pattern_hides_prod_bug` 的形状。

**建议**: §4 改「reason **族** 8 个 (`_result` 调用点 9 处, `git-diff-failed` 占两处)」; 2.2 表加一行注: 「`git-diff-failed` / `workflow-parse-failed` / `internal-error` 三档在运行时是**带载荷前缀** (`<族>: <detail>`), 判据用 `startswith`, **禁**相等比对」; SC-2/SC-9 的参数化 fixture 必须带载荷 (例: `"internal-error: RuntimeError: x"`), 并加一条坏实现对照 (相等比对版必红)。

---

### [A1-R2-m2] Minor — `pr_branch_check` 的 dict 形状未定; `pr-branch-not-found` 那支的 `raw_message` 副本通道契约 (#137 「同文同写」) 也没写

**锚点**: Spec 2.1 (`:70`) 「`compute_verdict` 签名 additive 加 `pr_branch_check: dict | None = None` (2.3 的结果)」; 2.3 表 (`:100-103`); `_verify_main_branch_exists` 返回 `tuple[str, str]`

**问题**: `_verify_branch_exists` 返回的是 `(status, detail)` 元组, spec 却要求参数是 `dict`, 键名未定。而 detail 是承重的 —— 2.3 第 3 行要求 message 追加「(PR 分支存在性核验失败: `<detail>`)」。两个实施者会给出 `{"status":..,"detail":..}` / `{"state":..,"message":..}` 等不同形状, SC-10 的 mock 也就写不成同一份 (memory `spec_underdetermination_two_implementer_test`)。另: 既有 main 核验那支是 `raw_message = msg` 且 `gate_error.message = msg` 同文同写 (`:459-473` 实读); 2.3 的新 fail 支没写这条, SC-10 也没断言 —— #137 副本通道契约在新 kind 上出现缺口。

**建议**: 2.1 明写形状 (建议 `{"status": "ok"|"not-found"|"verify-failed", "detail": str}`, 由 `gate_check` 从元组包装, 并说明它只在 `pr_ci_status == "not_found"` 时非 None); 2.3 补一句「`pr-branch-not-found` 与核验失败两档同样遵循 #137 副本通道: `raw_message == gate_error["message"]`」; SC-10 加该断言。

---

### [A1-R2-m3] Minor — 3.3 说阈值校验「只在 `gate_check` cfg 合并后」, 与 SC-3 直调 `compute_verdict` 的调用面矛盾; 且引了错的 SC 号

**锚点**: Spec 3.3 (`:146`) 「校验**只在** `gate_check` cfg 合并后 … 非 int / <2 → 回落默认 + `warnings.warn` (**SC-10**)」 vs SC-3 (`:202`) 「`gate_error.escalate_after_observations` == 校验后生效值: cfg 缺省→3; `{"no_run_escalation_observations": 5}`→5; `1`/`0`/`"x"`/`None`→3 + `warnings.warn` 各一次」 + SC-2 (`:201`) `compute_verdict([], "not_found", cfg=None, ...)`

**问题**: 两处不能同真。SC-2/SC-3 是直调 `compute_verdict`(cfg=…) 取 `gate_error.escalate_after_observations`, 那么校验必须发生在 `compute_verdict`/`_no_run_gate_error` 里 (2.1 自己也写了「`cfg=None` 时取 `DEFAULT_CONFIG`」—— 这已经是 `compute_verdict` 内的第二个合并点)。若照 3.3 字面把校验放进 `gate_check`, SC-3 直接红。另: 该句括注的 (SC-10) 是 PR 分支消歧那条, 阈值校验的判据是 **SC-3** —— 交叉引用漂移。

**建议**: 3.3 改「校验点唯一 = `_no_run_gate_error` (被 `compute_verdict` 调用); `_normalize_config` 只做 alias, 不是校验点; `gate_check` 的合并只保证 `cfg` 完整」, 并把 (SC-10) 改成 (SC-3)。

---

### [A1-R2-m4] Minor — 2.5 是一条「不退出的 exit condition」, 与该列表「first-match-wins 决定 loop 如何结束」的既有类型不同构

**锚点**: `workflow-runner/SKILL.md:332-336` (「**Exit conditions** (优先级 first-match-wins)」, 四条全部终止 polling); Spec §3.2 的 2.5 (「执行后 `mark_no_run_escalation_done`, **回到 polling loop**」)

**问题**: 把一条「执行副作用后继续循环」的条款插进一个「决定 loop 如何结束」的封闭列表, 改变了这张表的类型。今天靠散文一句「回到 polling loop」兜住, 但对下一个读表的人 (以及照表实现的 LLM) 这是歧义源: 2.5 命中后是否还要评估 2.6 / 3 / 4? (按 first-match-wins 是不评估, 恰好也是对的, 但没人写下来。)顺带记录一个既有事实: exit condition 2 的左析取项「`retry_count > max`」里的 `max` 在 `DEFAULT_CONFIG` (`pre_merge_gate.py:57-69`) 中**不存在任何对应 key** —— spec 把 2.5/2.6 的插入点锚在这条上, 值得知道它半边是悬空的 (既有缺陷, 不归本 spec)。

**建议**: 把 2.5/2.6 从 "Exit conditions" 拆成一个并列小节 (例如「**In-loop escalation** (在 exit conditions 2 与 3 之间求值, first-match-wins 语义共享)」), 或在 2.5 后补一句「命中 2.5 即停止本轮 exit condition 求值, 不再评估 2.6/3/4」。

---

### [A1-R2-m5] Minor — 处方段「入口仅为 workflow-runner 2.5 转入」使 §C.2.4 被**独立调用**时整段结构不可达, spec 未声明这一事实

**锚点**: Spec 3.3 (`:139`) 「(b) 承载处方段, **入口仅为 workflow-runner 2.5 转入**」; `phase-c-integrator/SKILL.md` §C.2.4 是可被 `/phase-c-integrator` 直接触发的一段流程 (不经 workflow-runner 时无 `gate_state`)

**问题**: 交互式跑 Phase C (不经 workflow-runner) 时没有 `gate_state`、没有 `no_run_observations`、2.5 不存在 ⇒ 处方段永不执行, 只剩 (a) surface 义务。这可能正是设计意图 (人在场, 交给人), 但 spec 没写, 而 §C.2.4 的读者会看到一整段带优先序与 HTTP 细节的处方却无从知道它何时生效。

**建议**: 3.3 (b) 补一句「非 workflow-runner 编排 (交互式直调 §C.2.4) 时本段不执行 —— 无 `gate_state` 即无计数, AI 只履行 (a) surface 义务并把处置交给在场的人」。

---

### [A1-R2-m6] Minor — `unknown/workflow-parse-failed` 档的处方 2 指示「任一 workflow 声明的 paths」, 而该档的成因恰是那些 workflow 解析不了

**锚点**: Spec 3.3 处方 2 (`:142`) 「`unknown`/pc=None: **任一 workflow 声明的 paths**」; `path_coverage.py:498` (规则 7: 无 covered ∧ 有 parse 失败 → `workflow-parse-failed: <files>`)

**问题**: `unknown` 有三个成因。`workflow-parse-failed` 那一支意味着**解析器读不懂那些 workflow 的 `on:`/`paths:`** —— 这时叫 AI「挑任一 workflow 声明的 paths 去碰」是让 AI 手工做刚失败的那件事, 且没有任何校验说明它做对了。`internal-error` 支同理 (评估器自身炸了)。只有 pc=None (评估被关掉) 这一支是干净的。

**建议**: 处方 2 的 `unknown` 档细化: `git-diff-failed` / pc=None → 「任一 workflow 声明的 paths」; `workflow-parse-failed` / `internal-error` → 降级为「碰**已知**必触发路径 (仓内任一 workflow 目录下的文件本身)」或直接跳到处方 3, 因为此时对「什么路径会触发」没有可信信息。

---

## 未发现问题但已核验的点

- **基线仍是 `400f0bc`** (`git rev-parse HEAD` in `aria/`), 工作树干净; `pytest skills/phase-c-integrator/tests -q` → **119 passed**, `skills/workflow-runner/tests -q` → **22 passed** —— SC-12 的两个基数属实。
- **§1/§2 同 commit 的落地顺序硬约束依旧承重且写对** — 本轮直调复跑: `compute_verdict([], "not_found")` → `green`, 输出六键; `compute_verdict([{'run_id':1}], "not_found")` → `wait`。SC-2 的红窗 (green) 与 SC-4 的红窗 (kind 而非 verdict) 都定位正确。
- **2.3 与 #137 三禁令一致** — 三条禁令逐字在 `pre_merge_gate.py:284-287` 注释 (SKILL.md`:248` 只复述其中两条 —— 退出码与 glob, 未复述 `--exit-code` 那条, 既有缺口不归本 spec); `_verify_main_branch_exists` 函数体的判据是 `target in ref_names` 的精确比对 (`:350`), 与分支名无关 ⇒ 泛化为 `_verify_branch_exists` 不动任何一条禁令。旧名保留别名的做法与「既有调用/测试不改」自洽。
- **2.3 的插入点唯一可推** — `pr_status.state` 只在 `:509` 的 `query_pr_ci` 返回后存在, 后面只剩末尾 `compute_verdict(...)` 一处 (`:521`) ⇒ 插入点是 `:519` (except 块结束) 与 `:521` 之间, 无第二候选。timeout 参数按 main 支对称取 `cfg.get("primitive_call_timeout_seconds", _LS_REMOTE_TIMEOUT)` 亦可唯一推出。
- **2.2 的 `not_applicable` 不可达仍成立** — `gate_check:499-506` 的短路在 `query_pr_ci` 之前 `return`, 结构上产不出 `not_found`; SC-6 的坏实现对照 (漏 `return`) 判据正确。
- **2.1 插入位置的 first-match 序无冲突** — `compute_verdict:197-222` 现序为 `failing/error` → `pending` → `not_applicable` → `main_in_flight_runs` → else; 新 `not_found` 插在 `not_applicable` 与 `main_in_flight_runs` 之间, 与 2.6/exit-2 亦无重叠 (2.5/2.6 只在 verdict=wait 下可能成立, exit 3/4 分别要求 fail/green)。
- **`gate_error` 与 `path_coverage` 同场在结构上可满足** — `_build_output:271-274` 两个 additive 键各自 `if not None` 插入, SC-5(a) 的「六键 + 两键」可达; SC-5(b) 的 pc=None 变体亦可达。
- **`format_version` 不 bump 的判断不引入新消费方风险** — `grep -rln gate_state aria/skills/` 只命中 workflow-runner 自己的 4 个文件; `workflow-state-schema.md:4` 写的「Consumers: state-scanner, workflow-runner, phase-c-integrator」中 state-scanner 与 phase-c-integrator **实际都不读 `gate_state`** (零命中)。所以两个 additive 字段的读者集合 = workflow-runner 自身, R1 #13 的定案成立。
- **AB 套件的既有 7 条 fixture 确实到不了 `not_found`** — 逐条复看: green/wait/wait_then_green/fail 由 mock 的 in-flight + PR CI 驱动, NEG-1/2 走 malformed/timeout, NEG-3 走 path_coverage unknown; `primary_pass_gate_metric = wait_triggered_when_in_flight_mock_present` 度量的是 (b) 轴。rule6_note 对「照跑产出的绿零信息」的判断属实 (问题只在处置的完整性, 见 M4)。
- **traps 现为五节 / SKILL.md:241 写「7 条坑」** — 新增 §六 与计数更新的落点存在且不冲突。
- **`.aria/config.template.json` 确缺 `path_coverage_enabled`** — §5 要求「补两个」属实。
- **Rule #10 定性无变化** — `post_brainstorm = off` 属白名单第一类, spec 头部留痕方式正确, 本轮不要求补 brainstorm。
- **AD-2 / AD-3 / AD-6 / Level 2 判定 / Why 段事实链 (F1-F6)**: 本轮无新质疑, 与 R1 一致。

---

## Verdict

**FAIL** (1 Critical / 6 Major / 6 Minor)

**vote: REVISE**

R1 归我席的 10 簇: **closed 6 / partial 4 / not_addressed 0** —— 吸收质量本身是好的, 没有一簇被漏。但四条 partial 与全部 6 条新 Major 收敛到同一个根: **§3 (处方/升级) 是为一台不存在的机器写的规格**。`gate_state_helper.py` 运行时零消费方 (实测), workflow-runner 是散文驱动的; 于是「判定单点」「计数单点」「至多一次」「阈值 3 = 90s」四个承重结论各自都只到文档层为止, 而验证它们的 SC-11 跑在生产从不执行的代码上。

**边际产出诚实标注**: 我这轮 6 条 Major **6/6 由 v2 自己的 fix 引入** (M1←#1, M2←#2, M3←#7×#12 接缝, M4←#9, M5←#11, M6←#1)。按 memory `audit_marginal_return_goes_negative` 的判据 (本轮 fix 引入的 major 占比 > 1/2), 同一批席位再加轮预期净负; 若 owner 要 R3, 应换新鲜眼睛而非同席复审 (memory `stop_adding_rounds`)。

**给 owner 的范围选项 (三档都合法, 我推荐 B; 列全是因为 memory `narrow-owner-options` 提醒选项集会被悄悄收窄)**

- **A — 照修**: 逐条修 C1/M1..M6 再 R3。代价: C1 的 (a) 档要给 workflow-runner 建真正的机械执行面 (SKILL 接线 + 可验「helper 真被调用」的 SC), 那是本 spec 之外的一块工程; 不做 (a) 就只能做 (b) 承认是散文机器, 那时 M1/M2/M4/M6 的「修」都只是把散文写得更细, 不产生机械保证。
- **B — 缩范围 (推荐)**: 本 spec 只 ship **显影半边** —— §1 + §2.1/2.2/2.3 + §4 + 对应的 SC-1~SC-10 / SC-12 / SC-14 + 文档同步面 + surface 义务 (rule6_note 只剩一条点名行为 + NEG-4 单帧 fixture, 判据表第三行的三条义务这时**真能履行**)。#152 的实际危害是「等满 1800s 且看不见真因」, 显影半边就把它变成「30 秒内看见带 #152 归因与处置建议的诊断, 且 fail-closed 不放行」——#152 当天的实际收敛手段本来就是人推了一个实质 commit。§3 (`no_run_observations` / 一次性守卫 / 2.5/2.6 / 处方 1-3 / config 旋钮 / TASK-0) 连同「workflow-runner 需要机械状态执行面」一起另立一个 spec。这条把交付距离从「一台新机器」缩到「5 行 backend + 一个新 elif + 一次 ls-remote」, 且 C1/M1/M2/M4(2/3)/M5/M6 **全部消失** (不是被修, 是不再存在)。⚠️ 诚实标注: 这不是 memory `no_ruling_shortens` 警告的那种「为降复杂度而拆 spec」—— 拆的动机是「后半段的验证面结构上不存在」, 不是「文件太大」。
- **C — 维持全范围但降级承诺**: 保留 §3 全部条款, 但把 AD-7 从「机械单点」改成「散文规范 + 参考实现」, 在 spec 里逐字写明 2.5/2.6/一次性守卫**无机械验证面**、其正确性依赖 LLM 遵循散文, 并把这一点写进 CHANGELOG 与 traps §6 (让下一个人知道)。风险: 这些条款控制的是**外向、难撤销**的自动 push/dispatch, 在 v2.0 无人值守下无人复议 (CLAUDE.md「自主运行时无人复议, Rule #10 更硬」)。我不推荐把这一类动作交给无机械保证的散文。

无论选哪档, **C1 必须在 Phase B 前有明确处置** —— 它决定 SC-11 到底在验证什么。
