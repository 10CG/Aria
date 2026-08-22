---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T09:52:04.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 1
minor_count: 5
---

## 摘要

**我 R5 的 Major (簇 #1, SC-13 场地) 真闭了, 而且 v6 的修法比我建议的更有底 —— 我这轮独立复测出一条前五轮没人提过的事实: `aether ci status` 命令行里没有 `--repo`, 仓由 cwd 决定, 所以「gate 在 aria-plugin 根跑」不是可选而是必需。** 但簇 #2 的修法 (SC-5 加回填断言) 在同一个 SC 里造出一对互斥子句: (b) 把 disabled 变体的 message 钉死在「路径覆盖评估已关闭」档 (该档封闭表里既无分支名也无占位符), (c) 又要求「**两变体** message 均含 `feat/x`」⇒ (b) 这一半在任何正确实现下都绿不了。

这是**连续第二轮**「上一轮的 fix 造出本轮唯一的 Major」(R4 的派生 fix → R5 的场地 Major; R5 的回填 fix → R6 的 SC 互斥)。我的 Major 数 6(+1C) → 6 → 3 → 1 → **1**, 已不再下降。按 `stop_adding_rounds_when_major_count_flattens` + `marginal_return_negative`, 这个循环现在主要在消化自己的产物。所以我的建议与投票分离, 请一并读: **票 REVISE (因为确有一条必须改), 但强烈建议不要再开 R7** —— 这一条是一行 SC 措辞, 不动任何设计, 落完由主控或 owner 单点复核即可。

本轮全部结论有实跑证据 (aria-plugin/主仓两侧 `_parse_workflow` + `_workflow_covers` 逐组合、`aether.py` 命令构造、`_result` 调用点计数、`.gitignore` 逐行、helper 默认参数), 没有一条只靠读 spec 文本。

---

## R5 处置核对

| 簇# | 来源 | 状态 | 证据 (本轮实测) |
|---|---|---|---|
| **#1** | A1-R5-M1 + A1-m5 (SC-13 场地 / CLI 无 `--state-file`) | **closed** | 见下方证据块。SC-13 现逐字「**gate 在 aria-plugin 子模块根执行**」+「**state 文件 = 主仓 `.aria/workflow-state.json` 绝对路径** (`--state-file` 显式传, 这正是「gate cwd 与 state 文件位置两回事」的活体检验)」—— 我 R5 指出的「(A) 派生 fix 的承重命题在活体里从没被拉扯过」也一并补上了 ✓。§3.2 步骤 2 「所有 CLI 调用**显式传** `--state-file <主仓根绝对路径>/.aria/workflow-state.json`」+ 3c′ 命令行内联同一旗标 ✓ (m5 闭) |
| **#2** | A2-R5-M1 + A1-m3 (`<pr_branch>` 回填零 SC) | **partial** | SC-5 确实加了 (c)(d) 两子项, (d) 与 §2.1 伪码 (`verify_note` 只在 `if out.get("gate_error")` 内追加, not_found 路径恒有 gate_error) 对得上 ✓。但 (c) 与同一行的 (b) 互斥, 且在 `dispatch_viable=false` 分支下 (a) 也不可能满足 —— **M1** |
| **#3** | A1-m1/A4-m1 · A1-m2/A4-m3 · A1-m4/A4-m2 · A4-m4 · A1-m6 · A2-R4-m1/m2 | **partial (归我的 4 条: 3 closed / 1 partial)** | **m1 (早退计数) closed** — 全文只剩一套口径: `:72` 「第七个早退 return 点 (现六点八变体之外新增一点)」/ `:134` 「既有**六个**早退 return 点 (八变体)」/ `:247` / SC-7 「六个早退 return 点 (八个变体)」, grep 全文 0 处「七个早退」✓。**m2 (`{o}/{r}`) closed** — `:126` 已是 `/repos/<owner>/<repo>/actions/workflows/<basename(file)>/dispatches`, 且补了「渲染**禁用** `str.format` — JSON 体的花括号本就在串内」, 我 R5 建议的「点一句 JSON 花括号另说」也落了 ✓。**m4 (reset 语义张力) closed** — `:152` 改成「`--observations` 只动 `no_run_observations`; `--retry-count` 置 `retry_count=0` **并置 `started_at=now`** … 具名 helper `reset_retry_count(state)` 与 `reset_no_run_observations` 对称」, 与 SC-11(d) 逐字一致 ✓ (附带落下 **m2′**, 见 minor)。**m6 (branches 第三成因) partial** — 诊断半边落了 (`:126` 「或 workflow `branches` 过滤不含本分支 (path_coverage 不建模 branches)」), 处方半边没落 (`:184` (b) 仍逐字「第二次 push 是普通 diff, paths 正常评」, 无 branches 限定), 且兄弟档 `workflow-files-changed` 的 message 未同步 → **m1** |
| #4 | A3-R5-m1/m2 · A5-R5-m1 · A2-R5-m1 (聚合判「非强制, 留 Phase B 顺手」) | **not_addressed (按聚合表本意)** | 我 grep 全文: 这三条在 v6 里没有任何落点 (无 tasks 注记 / 无实施注记段)。聚合的处置本身是「不阻塞」, 我不重开; 但「留 Phase B 顺手」= 把三条判断推到 B.2 现场 → **m5** (Rule #10 的边, 与我 R5 Verdict 第 3 点同一提醒) |

**统计 (簇粒度, 归我席的 #1/#2/#3)**: closed **1** / partial **2** / not_addressed **0**。(条目粒度: 我 R5 的 1 Major + 6 minor 中 5 条 closed, 2 条 partial。)

### 证据块 — 簇 #1 的三条独立复测 (不引 R5 结论, 全部重跑)

1. **aria-plugin 侧可达** (`cd /home/dev/Aria/aria`, `_find_workflow_files('.')` + `_parse_workflow(text)` 实跑):
   - 全仓**只有一个** workflow: `.forgejo/workflows/issue-triage-tests.yml`
   - `{'parse_ok': True, 'covered_uncertain': False, 'triggers': [{'key':'push','paths':['skills/issue-triage/**']}, {'key':'pull_request','paths':['skills/issue-triage/**']}]}` —— **push 无 `branches` 白名单** (⇒ 处方 (b) 「第二次 push 正常评」在这个仓成立), 且源文件含 `workflow_dispatch: {}` (⇒ §4 的 `dispatchable=True`, 处方 (a) 有渲染对象)
   - `_workflow_covers(p, ['skills/issue-triage/x.py']) == True`; `skills/issue-triage/` 下 `tests/ scripts/ evals/ references/ SKILL.md` 都是真文件 ⇒ **`covered`/`workflow-trigger-matched` 可构造** ✓
2. **主仓侧仍不可达** (同一 API 在 `/home/dev/Aria` 跑): 3 个 workflow, `build-aria-runner.yaml` paths `['aria-orchestrator/docker/aria-runner/**']` · `issue-triage-tests.yml` paths `['aria/skills/issue-triage/**']` · `submodule-gate-tripwire.yml` `triggers: []`; `git ls-files aria` = **1** (裸 gitlink) ⇒ 前两个前缀在超级仓索引里不可能有文件。SC-13 里那句「主仓树内构造不出 `workflow-trigger-matched` — 主仓 workflow 的 paths 全指向子模块挂载点」逐字为真 ✓
3. **新事实 (前五轮 30 份报告 (25 席位 + 5 聚合) 里 grep 零命中)**: `AetherBackend._query` 构造的命令是 `["ci","status","--branch",branch,"--json"]` (`ci_backends/aether.py:198`) —— **没有 `--repo` 之类的仓选择旗标**, 目标仓只能由进程 cwd 决定。⇒ 要让 gate 查到 aria-plugin 那条 throwaway 分支的 run 史, cwd **必须**在 aria-plugin; 「在 aria-plugin 根执行」不是 R5 建议的一个便利选项, 而是这条 SC 唯一能成立的构型。v6 的修法因此比我 R5 的建议更硬 ✓
4. 顺带复核 v6 引的三处基线数字, 全部对得上: `aether.py:218` docstring / `:225-226` `if not runs: return "pending"` ✓; `path_coverage.py:36`「共 9 个」✓ (终态 reason 实为 8: 规则 1/2/3/4/6/7/8 七个 + `internal-error`); `_result(` 调用点共 **9** 处 (`:422/432/447/459/464/468/493/498/506`) ⇒ §4「仅规则 6 调用点传 matched 子集, 其余 **8** 处不改」✓; 主仓 `.gitignore:19-21` 正是既有三条 telemetry 分区 ✓, 且 `:6` 已有 `.aria/workflow-state.json` (SC-13 不会在主仓留 untracked 文件)。

---

## 新 Findings

### 必须改

#### [A1-R6-M1] Major — SC-5 的 (b) 与 (c) 是一对互斥子句: (b) 把 disabled 变体的 message 钉在「评估已关闭」档 (封闭表里无分支名亦无占位符), (c) 又要求「两变体 message 均含 `feat/x`」⇒ 该子项在任何正确实现下都绿不了; 且 §3.5 的 `dispatch_viable=false` 删除清单漏了它

**锚点**: SC-5 (`:258`) · §2.3 message 封闭表 (`:126-131`, 特别是 pc=None 行与 empty-diff 行) · §2.1 末段回填伪码 (`:90-92`) · §3.5 删除清单 (`:195`)

**事实链 (全部取自 v6 自己的文字 + 基线源码)**

1. SC-5(b) 逐字: 「disabled → `gate_error` 在场、`path_coverage` 不在场, **message 为「评估已关闭」档**」。
2. §2.3 封闭表 pc=None 行逐字: 「远端零 run; 路径覆盖评估已关闭」——**整档没有分支名, 也没有 `<pr_branch>` 占位符**。
3. §2.1 的回填是 `message.replace("<pr_branch>", pr_branch)`: 串里没有占位符时它是 no-op。
4. ⇒ (b) 变体的 message 在正确实现下**必定不含** `feat/x`。而 SC-5(c) 逐字要求「**两变体** message 均**含** `feat/x`」。同一行 SC 的两个子句互相排斥。
5. **(a) 变体也没有稳态**: 全表里带 `<pr_branch>` 占位符的**只有** trigger-matched 档那条 dispatch 处方行, 而它受 `DISPATCH_VIABLE and dispatchable_workflows` 双重条件控制。基线测试 mixin 的 path_coverage 打桩是 `_PC_COVERED_STUB`(`tests/test_pre_merge_gate.py:50-56`: `decision=covered` / `reason=workflow-trigger-matched` / `matched_workflows=['.forgejo/workflows/stub.yml']`, **无 `dispatchable_workflows` 键**) ⇒ 照 SC-5 前置 (只说「mock backend `not_found`, 核验 mock ok, `pr_branch="feat/x"`」) 写出来的测试, (a) 也不会渲染 dispatch 行, 一样不含 `feat/x`。
6. **且 TASK-0a 若判 `dispatch_viable=false`**: §3.5 的删除清单点名了「§4 整段 + SC-8 + SC-9 的 dispatchable 部分 + `DISPATCH_VIABLE` 常量本身 + 2.3 表的 dispatch 渲染句 + **SC-2 的 dispatch 子项** + 3.3 (a) 行」, **唯独没有 SC-5(c), 也没有 §2.1 那句 `.replace`**。false 分支下全表再无任何 `<pr_branch>` 占位符 ⇒ SC-5(c) 恒红, `.replace` 成零消费方代码 —— 正是 R4 A1-m6 立下的「不留零消费方字段/常量」在它自己的兜底分支里复发 (memory `fix_recurs_in_its_own_fallback_path`)。

**为什么够 Major (逐条对门槛)**

- **两实施者必然分叉且无 SC 能区分**: spec 文本自相矛盾, 实施者**必须**做一个 spec 没授权的判断。路径 A = 把 (c) 收窄到「(a) 变体且 dispatch 行在场」; 路径 B = 照 SC 字面把 `<pr_branch>` 塞进 pc=None 档 (乃至全部档) 的 message 模板, 让 (b) 也能含分支名。两条路都能得到全绿套件, **没有任何一条既有 SC 能把它们分开**: SC-2 对 pc=None 档只断言 `verdict/pr_ci_status/kind/副本通道/含 no-run-for-branch`, 从不禁止里面多一个占位符; SC-14 是文档机检。
- **契约破坏 (路径 B)**: §2.3 那张表是「钉」死的封闭集, empty-diff 档还专门写了「(不带分支名 — compute_verdict 不知道分支名, R3 #6)」。为了让一条测试变绿去改承重的封闭表, 是 memory `assertion_swap_severs_link` 的镜像 (那次是换断言, 这次是换被断言的对象), 而被换掉的恰是这个 spec 唯一的产出物 —— 交给人的那段诊断文字。
- 诚实标注**够不上的部分**: 它不造成 fail-open, 也不造成运行时错误行为; 它在 TDD 写 SC-5 的第一分钟就会红出来。所以危害是「B.2 现场被迫替 owner 做一次规格裁量」(Rule #10 的边), 不是「静默错到生产」。

**一行修法 (不动设计, 二选一)**

- (推荐) SC-5(c) 改为: 「**(a) 变体** (前置同 SC-2 dispatch 子项: `DISPATCH_VIABLE=True` + `dispatchable_workflows` 非空) message **含** `feat/x` 且**不含**字面 `<pr_branch>`; **两变体**均 `raw_message == gate_error.message` (副本通道在 gate_check 改写后重同步)」, 并把「SC-5(c) 的回填断言 + §2.1 的 `.replace` 句」一并写进 §3.5 `dispatch_viable=false` 删除清单。
- (等价) 保留「两变体」但把断言拆成两个量: 两变体都断「不含字面 `<pr_branch>` 且 `raw_message == message`」, 只有 (a) 加断「含 `feat/x`」。

**降级条件 (写明, 免得一条一行的窄项独吞末轮配额)**: 若主控判定「SC 与 §2.3 封闭表冲突时, 实施者以封闭表为准是唯一合理读法, 且这不构成 Rule #10 意义上的临场裁量」, 那么把 M1 降为 minor —— 我的票即为 **PASS**, v6 可直接进 A.2 (前提是这条一行修改仍要落, 只是不必再走一轮五席)。

### 还能挑 (minor — 单独或全部不改都不阻塞 A.2)

- **[A1-R6-m1]** 我 R5-m6 只落了一半, 且只落在一个兄弟位置。诊断半边进了 trigger-matched 档 ✓; 但 (i) `workflow-files-changed` 档 message 仍只写「同 #152 形态或未被领」, 同一个 branches 白名单对它一样成立; (ii) §3.3 处方 (b) 仍逐字「第二次 push 是普通 diff, **paths 正常评**」, 而如果零 run 的真因是 branches 过滤, 推 commit 一定无效 —— message 刚教会读者第三种成因, 处方就默认它不存在。典型 `fix_the_class_not_the_instance`。一行修: (b) 末尾加「若 message 提示 branches 过滤成因, 推 commit 无效, 改用 (a) 或改 workflow 的 `branches:`」。
- **[A1-R6-m2]** v6 新引入的具名 helper `reset_retry_count(state)` (`:152`) **没进 Impact 的 additive 函数清单** (`:245` 只列 `_verify_branch_exists` / `_effective_prompt_threshold` / `_no_run_gate_error` / `reset_no_run_observations` + CLI)。同一句话里刚说完「与 `reset_no_run_observations` 对称」, 对称的那半却在 Impact 里落单。纯文档同步, 一个词的修。
- **[A1-R6-m3]** SC-13 收尾只写「删分支」, 没写清 gate_state。它写的是本项目**真实生产**的 `.aria/workflow-state.json` (我实测该文件当前不存在, SC-13 会按 R3 #7 新建骨架; 好消息是主仓 `.gitignore:6` 已忽略它, 不会脏工作树)。若活体走到「600s 仍无 run」那条腿而收手, 落盘 gate_state 停在 `status: waiting` ⇒ `is_gate_active()` 恒 True (`gate_state_helper.py:164-167`), 下一次真实 workflow-runner 会以为有个 pre_merge gate 待续。CLI 里现成有 `clear`, SC-13 加半句即可: 「收尾 CLI `clear` (telemetry 行保留 —— 那是 SC-16(c) 的证据)」。
- **[A1-R6-m4]** 「恒传主仓绝对路径」这条不变量落到了**调用点纪律**上, 没落到**默认值**上: §3.1 的 CLI synopsis 仍写 `python3 gate_state_helper.py <sub> --state-file .aria/workflow-state.json` (相对路径示例), 而 Python API 默认就是 cwd 相对 (`load_state(path=".aria/workflow-state.json")` / `atomic_write_state(..., path=...)` 实读确认)。§3.2 那句「所有 CLI 调用显式传」已经把风险压得很低, 所以只是 minor; 但对比 `--source` 的处理 (「**无缺省, 必填**, 缺失 → exit 2」) 就能看出还有一档没吃: 把 `--state-file` 也写成必填, 这条不变量就从纪律变成结构 (memory `invariant_needs_failclosed_default`)。
- **[A1-R6-m5]** R5 聚合簇 #4 的三条 (SC-15 两 skill 证据覆盖 / traps 日期对称 / `DISPATCH_VIABLE` 读取方式) 被判「非强制, 留 Phase B 实施时顺手」, 但 v6 全文没有它们的落点 (我 grep 过: 无实施注记段, tasks 尚未产出)。「顺手」在没有承载物的时候等于蒸发, 或者变成 B.2 现场的临场判断。建议 A.2 转 tasks 时给这三条各留一个 checklist 项 (与 §6 Phase D 待办同格式), 成本一行。

---

## Verdict

**verdict: PASS_WITH_WARNINGS · vote: REVISE** (critical 0 / major 1 / minor 5)

**#152 本体连续三轮我判可以进 A.2, 这轮同样没有一分钱新账落在它身上。** backend 单行 (`:225-226`) / compute_verdict 插入点承重注释 / 第七个早退 / CLI 签名与 `--source` 必填 / 90s→810s 时间轴 (与 `DEFAULT_INTERVALS_SECONDS = (30,60,120,300,300)` 实读一致) / basename 守卫 / `_result` 9 处调用点 / reason 族 8 / 版本引用点 —— 逐个复核过, 稳。簇 #1 我不但判 closed, 还带回了一条让它更稳的新证据 (`aether ci status` 无 `--repo` ⇒ cwd 即仓, 在 aria-plugin 跑是必需而非可选)。

**唯一的 Major 又是「上一轮 fix 的副产品」, 这是连续第二次。** R4 的派生 fix 生出 R5 的场地 Major; R5 的回填 fix 生出 R6 的 SC 互斥。我的 Major 数 6(+1C)→6→3→1→**1**, 已经平了; 而本轮 fix 引入的 major 占比 = 1/1。按 `stop_adding_rounds_when_major_count_flattens` (「加轮判据是 major 数是否还在降」) 与 `marginal_return_negative` (「本轮 fix 引入的 major 占比 >1/2 即到拐点」), 两条判据同时指向同一个结论: **这个审计循环现在的主要产出是它自己上一轮的修补痕迹, 不是 spec 里剩下的缺陷。**

**收敛建议 (与我 R4/R5 一致, 不改口径)**:

1. 落 M1 的一行 (SC-5(c) 收窄到 (a) 变体 + 把它写进 §3.5 删除清单), 顺手把 m1/m2 两处措辞补齐 (各一行), m3/m4/m5 可选;
2. **不要开 R7 五席轮** —— 这一条是 SC 措辞层面的自洽问题, 修完后由主控直接对照 §2.3 封闭表复核那一行即可判定, 或由 owner 直批;
3. 若主控采用我写明的**降级条件** (SC 与封闭表冲突时以封闭表为准, 不算 Rule #10 临场裁量), 则 M1 → minor, 我的票转 **PASS**, R6 即 5/5 全票 (视其余四席), v6 进 A.2 —— 但那一行 SC 仍应在 A.2 转 tasks 前落, 否则 B.2 的第一条测试就会撞上它。

最后一句给主控/owner: 我这轮**唯一**改变判断的输入, 是「去把那两个仓的 workflow 文件和 aether 命令行真读一遍」这个动作 —— 不是第六轮的第五个席位。前五轮 30 份报告 (25 席位 + 5 聚合) 里 `--repo` 出现 0 次 (实 grep)。若还要再投一次配额, 投在「实施期第一条测试先写 SC-5」上, 比投在第七轮审计上划算得多。
