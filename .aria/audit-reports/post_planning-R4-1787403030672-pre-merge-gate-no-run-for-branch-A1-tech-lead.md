---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T14:43:35.547Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 1
minor_count: 6
---

# post_planning R4 (末轮) — A1 席 (tech-lead) · pre-merge-gate-no-run-for-branch (v4)

## 摘要

v4 的**结构层与转录层这轮全部实测通过, 零返工项**: 20 任务 / 51h / 8 parent 三项算术自洽; `exec_order`
= {0..19} 无重无缺且「每任务 > 其所有依赖」violation **0**; DAG 无环, 无悬空依赖; `TASK-003 ∈ 11 个下游
闭包` 11/11 为真且 `TASK-010a ∈ 010/011 闭包` 成立; `agent_summary` 与逐任务 `agent` 字段**双向集合相等**
(qa 6 / be 4 / km 2 / main-loop 8); 20/20 有 `reason`; proposal §5 那张 20 行文档表**逐行都有承载任务**;
主仓 14 个版本字符串点 + aria 侧 `marketplace.json:3/:16` 逐点实核值全为 `1.66.4`, 位置与 TASK-015 title
逐字吻合; 两枚缺失 tag (v1.66.1 / v1.66.4) 与 `3b97c35` 归属**双 remote ls-remote 实核属实**。

我 R3 的 3 Major + 6 minor: **closed 7 / partial 2 / not_addressed 0**。两条 partial 里:

- **M1 (负控恒红) 真的闭了** —— v4 的新 pattern 我在 9e6a17c 逐字复跑, **0 命中**, `<pr_branch>` 也 0,
  且补了 true 分支对偶断言。这是三轮里第一次一个「换量」修复经得起复跑。
- **M2 (INV-1 判别力) 方向对了、编码坏了**: v3 的 `grep -c` 恒真 → v4 换成语义谓词, 判别力回来了 ——
  但 v4 写下的**那条命令跑不起来**。我实跑得到两个独立的硬失败: 裸 exec → `KeyError "'__name__' not in
  globals"`; 补 `__name__` 后 → `ImportError: attempted relative import with no known parent package`
  (`aether.py` 有 `from .base import ...`); 而且 `_normalize_pr_ci_status` 是 `AetherBackend` 的
  **staticmethod**, 不是 module-level 名, INV-1 里那句 `_normalize_pr_ci_status([]) == 'pending'` 即使 exec
  成功也会 `NameError`。→ **本轮唯一 Major**, 修法是一行可粘贴命令 (我已把可跑形式与其 mutant 判别力实测,
  见 M1)。
- **M3(a) SC-14 位置**闭了 (TASK-010a, exec 12, 在 010/011 前, 五条断言我逐条验过**当下确实全红**);
  **M3(b) SC-15 回退手段**方向闭了 (worktree 换掉 stash), 但落成的检查两半都恒真 → 降级为 m1。

**Major 曲线 (本席): R1 1C/7M → R2 0C/3M → R3 0C/3M → R4 0C/1M** —— 三轮持平后首次下降, 且这一条不是
新缺陷类, 是同一处 (INV-1 编码) 的第二次未落地。我**不建议**排 R5: 修法已被我实跑验证 (正例 PASS / 反例
FAIL), 主控落一行后自跑两条命令即可自证, 再开一轮全席是 memory `marginal_return_negative` 的拐点右侧。

---

## R3 处置核对

我 R3 报 3 Major + 6 minor = 9 条 (对应 R3 聚合簇 #1 #2 #3 #4 #6 中归本席的部分):

| R3 条目 | v4 落点 | 核对 (实测) | 判定 |
|---|---|---|---|
| **A1-PP3-M1** 负控 grep 基线已 1 命中 ⇒ 恒红 | `INV-3.encoded_as` pattern 换 `DISPATCH_VIABLE\|dispatchable_workflows\|/dispatches -d`, 限 `{phase-c,workflow-runner}/{scripts,tests,SKILL.md}`, `references/` 豁免 | **逐字复跑 @ 9e6a17c: 0 命中** (`grep` exit=1); 对照裸 `dispatches` 仍 1 命中 (`submodule-tripwire-audit.sh:6`) 已被新 pattern 排除; `<pr_branch>` 在 `pre_merge_gate.py` 实测 **0**; true 分支对偶断言在场 | **CLOSED** |
| **A1-PP3-M2** INV-1 `grep -c` 恒真 | 改四合取语义谓词 (`git -C aria show … \| python3 exec` 跑函数) | 方向正确 (合取 1 恢复判别力) —— 但**命令不可执行**, 两个独立失败 + 一个 NameError, 见下 M1; 附带核: 合取 3 (`pre_merge_gate.py` 含字面 `not_found`) 基线 **0 命中** ⇒ 该项不恒真 ✅ | **PARTIAL** → M1 |
| **A1-PP3-M3 (a)** SC-14 脚本落在被断言文档之后 | 新 **TASK-010a** (qa-engineer, exec 12, deliverable `tests/test_doc_sync_no_run.py`), 010/011 依赖之, TASK-013 去掉该 deliverable | 顺序 12 < 13 < 14 ✅; 依赖边在 ✅; **五条断言逐条实测当下全红**: SKILL.md `:180`/`:276` 两枚举行无 `not_found` / `:172-183` 无 `gate_error` / 主仓 `config.template.json` 两 key 皆缺 / `path_coverage.py:36` 为「9」/ DEC 无前向指针; `parents[4]+SkipTest` 先例实读 `test_spec_complete.py:94,107` 属实且深度相同 | **CLOSED** |
| **A1-PP3-M3 (b)** SC-15 `git stash` 对子模块 no-op | `TASK-012.verification[0]` 改 `git -C aria worktree add <tmp> 9e6a17c` | 手段够得着仓了 ✅ —— 但基线树里**绑定测试本身也不存在**, 「红」被文本明确允许为「收集错误」⇒ 恒红; 「当前树→绿」在 TASK-013 全量绿之后恒真 ⇒ 两半都零信息 | **PARTIAL** → m1 |
| A1-PP3-m1 归档门 warn 预告是预先豁免 | `TASK-016.verification[2]` 撤预告, 改「若出现按其文案处置并留痕, **不预先豁免**」 | 逐字在场, 且注明「TASK-005 改词后实测该 warn 不再触发」—— 与我 R3 两态实测一致 | **CLOSED** |
| A1-PP3-m2 parallel note 未记验证面耦合 | `parallel_tracks.note` 补「**验证面**有一处耦合: TASK-010 的 `config-template-key-currency` 探针 import `DEFAULT_CONFIG`, 故 010 依赖 003」 | 逐字在场 | **CLOSED** |
| A1-PP3-m3 TASK-013 (main-loop) 挂测试交付物 = 隐式转派 | 脚本移出到 TASK-010a (qa); TASK-013 deliverables 只剩「测试运行记录」 | `agent_summary` 双向一致校验通过, qa 6 个任务含 010a; TASK-013 无测试文件交付物 | **CLOSED** |
| A1-PP3-m4 INV-6 全称句无例外 | `INV-6.rule` 加「**唯一例外**: checklist 1 随 TASK-007b 在 `dispatch_viable=false` 时整体 N/A …, 非蒸发」 | 逐字在场; `checklist_s7_mapping` 四项落点逐条复核在位 (1→007b.verification / 2→012.title / 3→014.notes / 4→008.notes) | **CLOSED** |
| A1-PP3-m5 TASK-006 false 分支 (`.replace`) 无核验 | `INV-3.encoded_as` 加「false ⇒ … 且 `pre_merge_gate.py` 中 `'<pr_branch>'` 0」 | 在场, 且基线实测该值为 0 (红窗方向正确: 落了 `.replace` 才会非 0) | **CLOSED** |
| A1-PP3-m6 012 ∥ 013 与独占工作树互斥 | `TASK-012.dependencies` 加 `TASK-013`; exec 013=15 → 012=16; `execution_order` 改「013 → 012 (回退核验独占工作树, 需 013)」 | 三处顺序面 (exec_order 数字 / `execution_order` 四行 / `parallel_tracks` 轨内序) 机检**三方一致** | **CLOSED** |

**计**: closed **7** / partial **2** / not_addressed **0**。

---

## Findings

### 必须改 (Major)

#### [A1-PP4-M1] `INV-1` 四合取里前两项的命令**跑不起来** —— 三个独立失败点, 而合取 1 恰是唯一能抓住「§1 先单独落地」这个 fail-open 的那一项

- **锚点**: `INV-1.encoded_as`「非破坏性 `git -C aria show <c>^:skills/phase-c-integrator/scripts/ci_backends/aether.py` 管道进 python exec 后 `_normalize_pr_ci_status([]) == 'pending'` (父提交语义) 且 `git -C aria show <c>:…aether.py` 同法 == 'not_found'」· `TASK-013.verification[1]` (唯一执行入口)
- **实测** (aria @ 9e6a17c, 主仓根):

  | # | 逐字复跑的形式 | 结果 |
  |---|---|---|
  | 1 | `… \| python3 -c "exec(sys.stdin.read(), {})"` | `KeyError "'__name__' not in globals"` |
  | 2 | 命名空间补 `{'__name__': 'x'}` | `ImportError: attempted relative import with no known parent package` (`aether.py:29` = `from .base import CIBackend, CIStatus, InFlightStatus`) |
  | 3 | exec 成功后按 INV-1 字面取 `_normalize_pr_ci_status` | **不存在**于 module 命名空间 —— 它是 `AetherBackend` 的 `@staticmethod` (`aether.py:216-217`, 类定义在 `:42`), 裸名必 `NameError` |

- **为什么是 Major (而不是「实施者顺手改改就行」)**: 这是 spec 里唯一一条被 proposal §1 标成「⚠️ 落地顺序
  **硬约束**」的不变量, 而它的**全部机械承载**就是 `TASK-013.verification[1]` → `INV-1.encoded_as` 这一串。
  我在 R3-M2 里证过: 对「拆分 A = `aether.py:225-226` 单独一 commit / B = `:218` docstring +
  `pre_merge_gate.py`」这条真实存在的坏拆分, **合取 3 (B 含字面 `not_found`) ✅ + 合取 4 (`--stat` 含两文件)
  ✅ 都通过**, 只有**合取 1 (父提交语义 == pending) 会红**。所以合取 1 跑不起来 ⇒ 四合取退化回 R3 已判定
  不足的两项 ⇒ 「§1 单独落地 = 盲区从恒 wait 变恒 green」这个**比现状更坏的 fail-open** 在 B.2 无人守。
  执行者在 exec 15 撞到 `KeyError` 时的两条出路都不好: 自造变体 (分叉, 且没有基线可比), 或退回 R3 已被
  否决的弱代理 —— 后者正是 memory `fix_recurs_in_its_own_fallback_path` 的形状 (同一处第二次)。
- **建议 (可粘贴, 我已实跑过正例与反例)** —— 在主仓根执行, `<c>` = TASK-003 commit:

  ```bash
  inv1_semantic() {   # $1 = git 对象 (<c>^ 或 <c>); $2 = 期望值
    git -C aria show "$1:skills/phase-c-integrator/scripts/ci_backends/aether.py" | python3 -c "
  import sys
  sys.path.insert(0, 'aria/skills/phase-c-integrator/scripts')      # 让 ci_backends 成为可导入包
  ns = {'__name__': 'ci_backends._hist', '__package__': 'ci_backends'}   # 缺这两键 → KeyError / ImportError
  exec(sys.stdin.read(), ns)
  got = ns['AetherBackend']._normalize_pr_ci_status([])              # staticmethod, 非 module-level 名
  assert got == '$2', f'INV-1 FAIL: got {got!r}, want $2'
  print('ok', '$1', got)"
  }
  inv1_semantic "<c>^" pending      # 合取 1
  inv1_semantic "<c>"  not_found    # 合取 2
  ```

  三处相对 v4 原文的必要修正: (a) `sys.path` 插 `scripts/` + `__package__='ci_backends'` (解相对 import);
  (b) 经 `AetherBackend.` 取 staticmethod; (c) 用 `assert` 而非打印, 使失败 = 非零退出码 (否则「跑了」和
  「过了」不可区分)。
  **实测证据**: 正例 —— 该形式在 9e6a17c 上返回 `pending`, 断言通过; 反例 —— 把源码里零 run 分支 `sed`
  成 `return "not_found"` 后同一形式**如期 FAIL**, 判别力成立。
  注 (写进 encoded_as 一句即可): 本形式让历史版 `aether.py` 与**当前树**的 `ci_backends/base.py` 组合
  —— 本 spec 不动 `base.py`, 可接受; 两次调用是两个进程, 无 `sys.modules` 串味。

---

### 还能挑 (Minor — 不构成 REVISE 理由, 建议随 M1 一起顺手落)

#### [A1-PP4-m1] `TASK-012` 的 SC-15 红窗两半都恒真 (基线树里绑定测试**本身不存在**; 「当前树绿」已被 013 保证)

`TASK-012.verification[0]`: 「`git -C aria worktree add <tmp> 9e6a17c` 在基线工作树跑
`test_case_in_unit_tests` 指向的测试 → 红 (**收集错误**或断言失败); 当前树 → 绿」。绑定名 =
`NotFoundVerdictTests.test_sc2_trigger_matched_message`, 由 TASK-002 新建; 9e6a17c 的
`test_pre_merge_gate.py` 里没有这个类 ⇒ `pytest …::NotFoundVerdictTests::test_sc2_trigger_matched_message`
必然 `ERROR: not found` (exit 4)。文本又明确把「收集错误」算作红 ⇒ **一个 vacuous 的绑定测试同样能通过
这条检查**; 而「当前树→绿」在 TASK-013 全量绿 (exec 15) 之后同样恒真。两半都零信息 (memory
`false_green_dual_is_permanent_red` 的对称形态)。
**不判 Major 的理由**: SC-15 真正想要的判别性红窗**已在 TASK-002 成立且写死了口径** ——
「基线 9e6a17c 上 SC-2 的红是 `verdict==green` (不是 AttributeError)」, 那次红发生在测试在树、生产码在
基线的正确组合上。所以本条只是重复核验退化, 不漏承载。
**建议**: 在基线 worktree 里把 feature 分支的测试文件取回来再跑, 使红是断言失败而非收集错误 ——
`git -C <tmp> checkout <feature-sha> -- skills/phase-c-integrator/tests/` → 跑 → 期望
`AssertionError: 'green' != 'wait'`; 并删掉「收集错误或」这半个允许项。

#### [A1-PP4-m2] `INV-3` true 分支的对偶断言 grep 的是**源码**而不是**渲染结果**

`INV-3.encoded_as` 末句: 「true ⇒ `_no_run_gate_error` 含 `'/dispatches -d'`」。若实现把处方行写成相邻字符串
字面量拼接或分行, `/dispatches -d` 在源码里就不连续, 这条会假红; 反过来, 把该串写进注释也能假绿。
SC-2 的 dispatch 子项已经断言**渲染后的 message** 含 `workflows/x.yml/dispatches`, 是更好的量。
**建议**: 对偶断言改成调用 `_no_run_gate_error(<trigger-matched pc>, 3)` 后断言返回 message 含
`/dispatches -d` (与 false 分支的「生成面 0 命中」对称, 两态都测行为而非文本)。

#### [A1-PP4-m3] `TASK-010a.verification` 引了一条 SC-14 里不存在的「`DEFAULT_CONFIG` 断言」, 它同时是该任务依赖 TASK-003 的唯一理由

title 列的是 SC-14 的五条 (SKILL.md 枚举 / `:172-183` / 两 key / DEC / `path_coverage.py:36`), 里面没有
`DEFAULT_CONFIG`; verification 却写「五条断言全红 (文档尚未改); **`DEFAULT_CONFIG` 断言绿 (003 已落)**」。
两种读法 (脚本另写第六条 SC-14 外断言 / 根本没这条断言) 都能自圆, 但后者会让 `dependencies: [TASK-003]`
失去依据、也让这句 verification 无法求值。**建议**: 二选一写死 —— 要么把「`DEFAULT_CONFIG` 含
`no_run_prompt_after_observations`」明确列进 title 的断言清单 (并说明它是 SC-14 之外的附带守卫), 要么删掉
这句并把 `TASK-003` 从依赖里去掉 (010a 只读文档与主仓 config, 排在 helper 轨 exec 12 即可)。

#### [A1-PP4-m4] `exec_order_note` 的 003 闭包枚举没跟着 TASK-010a 更新

`metadata.exec_order_note` 仍写「TASK-003 ∈ 005/006/007a/007b/010/011/012/013/014/015/016 的依赖闭包」
(11 个, v3 原样)。TASK-010a 直接依赖 003, 却不在这份枚举里。我实算 11/11 为真 **且** 010a 亦为真, 所以是
清单不全而非断言错 —— 但照着这条 note 写机检脚本的人会漏掉新任务。补一个 id 的事。

#### [A1-PP4-m5] `parallel_tracks` 「helper 轨 (**workflow-runner 文件域**)」现在含一个 phase-c-integrator 文件域的任务

TASK-010a 的交付物是 `aria/skills/phase-c-integrator/tests/test_doc_sync_no_run.py`, 却被排进 helper 轨。
**文件级 disjoint 仍成立** (新文件, 无人共写, 并行安全), 所以不影响调度正确性 —— 但轨名括号里的「文件域」
声明对这一员为假, 而这条声明正是「可并行」的论据。建议轨名改「helper + 文档机检轨」或在 note 里点一句
「010a 的文件在 phase-c 目录下, 但为新建文件, 与 gate 轨零共写」。

#### [A1-PP4-m6] `TASK-001` 的收尾断言 `git -C aria branch --show-current == feature/…` 在换成 worktree 之后已恒真; 且 `worktree remove` 不删本地 probe 分支

这句断言是 v3 用 `checkout -b` 时代的遗留守卫 (那时确实会把主工作树切走)。v4 改成
`git -C aria worktree add <tmp> -b probe/152-dispatch 9e6a17c` 之后, 主工作树 HEAD 从头到尾没被碰过 ⇒
该断言不可能红。同时 `git -C aria worktree remove` 只删工作树, **本地分支 `probe/152-dispatch` 会留下**
(TASK-014 同形)。建议把收尾断言换成有信息的量: `git -C aria worktree list` 不含 `<tmp>` **且**
`git -C aria branch --list 'probe/*'` 为空 **且** 远端 `git ls-remote origin 'refs/heads/probe/*'` 为空。

---

## 已核验无误 (实测; 按 memory `predict-then-measure` 先写预期再跑)

1. **主控点名的五条机检判别式全部成立** (yaml 实解析后程序化断言): `exec_order` 唯一且 = {0..19};
   「每任务 `exec_order` > 其所有 dependencies」**violation 0**; `TASK-003 ∈ 005/006/007a/007b/010/011/
   012/013/014/015/016` **11/11**; `TASK-010a ∈ TASK-010 与 TASK-011 闭包` **均为真**;
   `agent_summary` ↔ 逐任务 `agent` **双向集合相等** (qa 6 / be 4 / km 2 / main-loop 8 = 20);
   `estimated_hours` 求和 **51.0** = metadata; `total_tasks` 20 ✅; parent 集合 {P0..P7} = 8 ✅;
   DAG 无环; 悬空依赖 = ∅; 20/20 有 `reason`。
2. **`estimation_note` 的数字属实**: 「20 任务中 **15** 个 <4h」实数 = 15; 四组配对 002+003=7 / 005+006=6 /
   007a+007b=4 / 008+009=9 与 note 逐字同。
3. **三处顺序面三方一致**: `exec_order` 数字 == `execution_order` 四行叙述 (P0 0-2 / gate 轨 3-9 /
   helper 轨 10-13 / 汇合 14-19) == `parallel_tracks` 轨内序, 逐任务比对无出入。
4. **v4 负控 pattern 基线 0 命中** (M1 处置的核心): 逐字复跑
   `grep -rn -E 'DISPATCH_VIABLE|dispatchable_workflows|/dispatches -d'` 限六个落点 → exit=1 零命中;
   对照裸 `dispatches` 仍命中 `submodule-tripwire-audit.sh:6` (已被排除); `<pr_branch>` 在
   `pre_merge_gate.py` = 0。两态设计 (false ⇒ 0 / true ⇒ 对偶) 在场。
5. **SC-2 / SC-4 的红窗前提是真的** (proposal §1 硬约束的事实基础, 本轮首次实跑):
   `compute_verdict([], "not_found")` @ 9e6a17c 返 **`green`** ✅ (SC-2「基线 green」成立);
   `compute_verdict([{"run_id":1}], "not_found")` 返 `wait` 但 `gate_error is None` ✅
   (SC-4「红窗在 kind」成立); 输出键名是 `verdict` 而非 `pre_merge_verdict`, 与 SKILL.md `:276` 一致。
6. **INV-1 合取 3 不恒真**: 基线 `pre_merge_gate.py` 中字面 `not_found` **0 命中** ⇒ 该项落地后才为真,
   携带信息 (与合取 1 的病灶不同)。
7. **SC-14 五条断言在 TASK-010a 时点逐条实测全红**: SKILL.md `:180`/`:276` 两条 `pr_ci_status` 枚举行
   均为 `"passing" | "failing" | "pending" | "not_applicable"` 无 `not_found` (`:288` 归层注记里的
   `not_found` 不是枚举行, 不污染红窗); `:172-183` 无 `gate_error`; 主仓 `.aria/config.template.json:73-91`
   两 key 皆缺; `path_coverage.py:36` 逐字为「共 **9** 个」; 主仓 DEC 无前向指针。
8. **proposal §5 的 20 行文档表逐行有承载**: 6 行 phase-c SKILL.md → TASK-011 (`:241` 计数由 TASK-014 终改) /
   `pre_merge_gate.py` docstring → 003, 注释与 `--remote` help → 006 / `aether.py:218` → 003 /
   `path_coverage.py:36` → 011 / traps §六 → 001 建节 + 011 四行 + 014 证据行 (三写者有序且互相点名) /
   workflow-runner SKILL.md 七个锚点 + schema 三段 → 010 / config-loader + 主仓 template + `.gitignore`
   → 010 / `gate_state_helper.py:2-18` docstring → 009 / `runtime-probe-declaration.md:135-139` → 011 /
   DEC → 011 / CHANGELOG + 版本点 → 015 / AB 套件 → 012。**零遗漏**。
9. **文档锚点行号逐个实读命中** (转录漂移检查): phase-c SKILL.md `:46-54` 顶层配置表 (`:54` =
   `path_coverage_enabled` 先例) / `:292-302` 节内配置表 / `:172-183` YAML 摘要块 (`:180` 枚举 · `:183`
   `path_coverage` 行 —— TASK-011 `conditional_parts` 里的「`:183` dispatchable_workflows 字段文档」指的
   正是这行) / `:248` = 「2.2 Main 分支存在性核验」; workflow-runner SKILL.md `:249` JSON 块起 / `:313`
   触发场景 / `:326` log 文案 / `:332-336` Exit conditions / `:338-346` 实施步骤 (`:345` = 字段枚举行) /
   `:389` wait 分支; `workflow-state-schema.md:38` / `:110` gate_state 小节 / `:125` raw_message;
   `config-loader/SKILL.md:283` = `path_coverage_enabled`; 主仓 `.gitignore:19-21` = 三条既有 telemetry 分区。
10. **TASK-015 的版本面逐点实核**: 主仓 14 点 = `CLAUDE.md:139`+`:141` / `VERSION:24` / `README.md:8`+`:242` /
    `README.{zh,ja,ko}.md` 各 3 (`:3` translated-from + `:10` badge + `:244` Plugin Version) —— 一个不多
    一个不少, 当前值**全为 v1.66.4** (与 `baseline_sha` 自洽), 行号与 title 逐字吻合; aria 侧
    `marketplace.json:3` 与 `:16` 实读均为 `"1.66.4"`。
11. **两枚缺 tag 与 `3b97c35` 归属属实**: 本地 tag 仅 v1.66.0/.2/.3; `git ls-remote --tags` 对 **origin 与
    github 双 remote** 结果相同 (无 v1.66.1 / v1.66.4); `git show 3b97c35:.claude-plugin/plugin.json` = 1.66.1
    而其父 = 1.66.0 ⇒ 「plugin.json 首次 =1.66.1 的 commit」判定精确。
12. **Rule #6 面的事实全部对得上**: AB catalog `phase-c-integrator-pre-merge-gate.json` version 1.1.0,
    fixtures **7** 条 (green/wait/wait_then_green/fail/NEG-1/NEG-2/NEG-3) —— 与 rule6_note 的「7 fixtures」
    一致; NEG-3 的下划线元键**恰 8 个**且与 TASK-012 title 列的八键逐字同; `ab-results/` 五个目录里
    **无任何 NEG-3 执行记录** ⇒ INV-7「NEG-3 零执行史不得复制」的前提属实。
13. **TASK-002 的两处实核声明属实**: `_normalize_pr_ci_status` 在 tests 下**只出现在**
    `test_pre_merge_gate.py` (6 处), 无 `test_ci_backends.py`; `:363` 正是
    `test_empty_runs_pending` 的 `assertEqual(..., "pending")` 行。
14. **`_build_output` 已支持 `gate_error=` 形参** (`:236-245`) ⇒ TASK-003 的「`_build_output` 穿
    `gate_error`」是接线而非改签名, 不构成额外风险面 (main 核验那支本就在用)。
15. **`parents[4] + SkipTest` 先例引用准确且深度相同**: `state-scanner/tests/test_spec_complete.py:94`
    `_ARIA_META_ROOT = Path(__file__).resolve().parents[4]`, `:107` `raise unittest.SkipTest`;
    `phase-c-integrator/tests/` 与 `state-scanner/tests/` 在同一层, TASK-010a 直接沿用无需换深度。
16. **`TASK-016.conditional_parts` 对 proposal §3.5 是全清单**: 我 grep 出 proposal 全文
    `DISPATCH_VIABLE|dispatchable|dispatches` 共 14 处, 逐处判去留 —— 该删的 (L31 代码落点 / L129 2.3 渲染句 /
    L186 3.3 (a) / L200-202 §4 / L237 §7 checklist 1 / L255-256 Impact 两处 / L265 SC-2 子项 / L268 SC-5 (c2) /
    L271 SC-8 / L272 SC-9 部分 / §2.1 `.replace` / R-c) **全在清单内**; 该留的 (L51 F6 事实 / L198 §3.5 规则
    本体 / SC-5 (c1) 的「不含占位」守卫) 均未被误列。
17. **`audit_checkpoints_note` 仍属实**: `.aria/config.json` 的 mid_implementation / post_implementation /
    pre_merge / post_closure 四个显式 `off` (Rule #10 白名单第一类), 故不排 B/C/D 审计任务成立。

---

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 1 Major / 6 Minor) — **vote: REVISE**

**「必须改」只有一条**: `INV-1.encoded_as` 里的语义谓词命令不可执行 (M1)。它满足 Major 门槛的理由是
唯一的但也是硬的 —— 那条命令是 spec 唯一标注为「硬约束」的不变量的**唯一机械承载**, 而它守的正是
「比现状更坏的 fail-open」; 合取 3/4 已被 R3 证明单独不足, 所以合取 1 跑不起来 ⇒ INV-1 在 B.2 实质无守。
**六条 minor 都不构成 REVISE 理由**, 列出来是因为它们成本都在分钟级、且四条 (m1/m2/m4/m6) 是同一族
「检查恒真/恒假」的余量, 建议随 M1 一起清掉。

**处置建议 (给主控)**: 落 M1 的可粘贴命令 (我已实跑正例 PASS / 反例 FAIL, 无需再验证判别力) + 六条
minor, 然后**直接进 B.1, 不排 R5**。依据: (a) 本席 Major 曲线 7→3→3→**1**, 三轮持平后首次下降;
(b) 这一条不是新缺陷类, 是同一处 (INV-1 编码) 第二次未落地, 而这次的修法是**已验证过的字面量**, 不含设计
裁量; (c) v4 的结构层、转录层、覆盖层这轮我做了迄今最宽的一次实测 (拓扑/闭包/算术/双向 agent 一致性 /
§5 20 行 / 十余处行号锚点 / 14+2 版本点 / 双 remote tag / AB 元键 / 五条 SC-14 红窗 / 基线 verdict=green),
**零新增结构问题** —— 继续加轮已在 memory `marginal_return_negative` 的拐点右侧 (本轮 6 条 minor 里有 4 条
是「上一轮 fix 的余量」, 占比已过半)。

**给 B.2 执行者的一句提醒** (非 finding, 但值得进 handoff): v4 里凡是「某某检查」的地方, 这三轮的经验是
**先在基线树逐字跑一遍记下返回值, 再写进 yaml** —— R3 的三条 Major 与本轮的 M1 全部是第一次实跑就暴露的,
没有一条需要更聪明的阅读。
