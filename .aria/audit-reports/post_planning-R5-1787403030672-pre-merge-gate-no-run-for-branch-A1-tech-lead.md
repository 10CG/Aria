---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T15:58:18.596Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 0
minor_count: 5
---

# post_planning R5 (owner 加轮稳定性确认) — A1 席 (tech-lead) · pre-merge-gate-no-run-for-branch (v5)

## 摘要

**本席 R4 的 1 Major + 6 minor 在 v5 全部 closed (7/7), 零 partial, 零 not_addressed。**

三轮里第一次, 我报的 Major 不是「方向对了编码坏了」而是**逐字可复跑**:

- **INV-1 的新命令我从 yaml 里程序化抽出后原样跑了三例** —— `inv1 HEAD^ pending` exit 0 /
  `inv1 HEAD pending` exit 0 / `inv1 HEAD not_found` **exit 1 + `AssertionError: pending`**。R4 的三个
  硬失败 (`KeyError __name__` / 相对 import / staticmethod 非 module 名) 全部消失, 判别力在两个方向上都
  实测成立 (另跑「已落地」方向: `sed '226s/pending/not_found/'` 后同一管道返 `not_found` 且 assert 通过)。
- **SC-15 红窗我把整条流程跑了一遍**: `git -C aria worktree add <tmp> 9e6a17c` (无 `--detach` 亦自动
  detached, 命令字面可用) → 拷入当前 `tests/` → 追加一条模拟的 `NotFoundVerdictTests.
  test_sc2_trigger_matched_message` → 得到 **`AssertionError: 'green' != 'wait'`**, 正是 v5 要求的
  「断言失败, 非收集错误」。v5 那句「测试用 sys.path 相对导入, 对着基线 scripts/ 跑」也属实
  (`test_pre_merge_gate.py:23-24` = `sys.path.insert(0, dirname(dirname(_HERE))/"scripts")`)。

结构层再次全量机检**零问题**且这次「闭包清单」是**精确集合**而非仅子集: `TASK-003 ∈ 12 项闭包` 12/12 为真,
且反向枚举「003 在闭包里却未被 note 列出的任务」为**空集** —— R4 的 partial 项 (清单 11→12) 不只补齐, 还
恰好收敛。20 任务 / 51h / 8 parent 算术自洽; `exec_order` = {0..19} 无重无缺; 「每任务 > 其所有依赖」
violation **0**; DAG 无环; 悬空依赖 ∅; `agent_summary` 双向集合相等 (qa 6 / be 4 / km 2 / main-loop 8);
15 个 <4h 与 `estimation_note` 逐字同。

**Major 曲线 (本席): R1 1C/7M → R2 0C/3M → R3 0C/3M → R4 0C/1M → R5 0C/0M。** 五条残余全是分钟级
措辞/对称性余量, 没有一条能让实施者做出错误的东西。**vote: PASS, v5 可进 B.1。**

---

## R4 处置核对

R4 处置表 5 簇中归本席的部分 (簇 1 主责 / 簇 2、3、5 参与) + 我的 6 条 minor:

| R4 条目 | v5 落点 | 核对 (实测) | 判定 |
|---|---|---|---|
| **A1-PP4-M1** INV-1 命令三处崩 | `INV-1.encoded_as` 换成 R4 A1 实跑验证形式 (`sys.path.insert` + `__package__='ci_backends'` + `ns['AetherBackend']._normalize_pr_ci_status` + `assert`) | **从 yaml 程序化抽出后原样跑**: `inv1 HEAD^ pending` **exit 0** / `inv1 HEAD pending` **exit 0** / `inv1 HEAD not_found` **exit 1, `AssertionError: pending`**; 「已落地」方向 (`sed '226s/return "pending"/return "not_found"/'` 后同管道) 返 `not_found` assert 通过。三个 R4 失败点全消, 双向判别力成立。合取 3 前提复核: 基线 `pre_merge_gate.py` 字面 `not_found` **0 命中** (仍携带信息)。`aether.py` `:216-217` staticmethod / `:218` docstring / `:225-226` 零 run 分支逐行实读, 与 TASK-003 deliverable 行号逐字吻合 | **CLOSED** |
| **A1-PP4-m1** SC-15 红窗两半恒真 | `TASK-012.verification[0]` 改「worktree 9e6a17c + **拷入当前树 tests/** → **断言失败** (verdict==green, 非收集错误) = 真红」 | **端到端实跑**: worktree(9e6a17c) + 拷 tests/ + 追加模拟 `test_sc2_trigger_matched_message` → `AssertionError: 'green' != 'wait'` ✅ 收集成功 (`import pre_merge_gate as gate` 属性访问式, `from ci_backends import (...)` 名单在基线全在); 「收集错误」允许项已删。`git worktree add <path> <sha>` 无 `--detach` 亦 detached, 命令字面可用 | **CLOSED** |
| **A1-PP4-m2** INV-3 对偶断言 grep 源码 | `INV-3.encoded_as` + `TASK-013.verification[2]` 改「true ⇒ 调 `_no_run_gate_error(trigger-matched pc 含 dispatchable, 3)` **返回的 message** 含 `/dispatches -d` (断言渲染结果非源码 grep)」 | 两处逐字在场且互相一致; 签名与 TASK-003 title 的 `_no_run_gate_error(path_coverage, threshold)` 对得上 (2 位置参数); false 分支未动, 负控 pattern 基线**复跑仍 0 命中** (exit=1), `<pr_branch>` 仍 0 | **CLOSED** |
| **A1-PP4-m3** TASK-010a 引了 SC-14 外的 DEFAULT_CONFIG 断言 (依赖 003 的唯一理由悬空) | title 改「**六条**断言」并把 `DEFAULT_CONFIG 含 no_run_prompt_after_observations` 明确列入 + 注「此条依赖 003 故为 GREEN, 其余五条 RED」; `dependencies: [TASK-003]` (去 009); reason 注「不依赖 009」 | 我 R4 给的两条出路取了 (A) 且写死了; verification「前五条全红 / 第六条绿」与 title 顺序一致。**六条逐条基线实测**: 枚举行 `:180`/`:276` 皆 `"passing"\|"failing"\|"pending"\|"not_applicable"` 无 not_found ✅红 / `:172-183` `gate_error` 0 命中 ✅红 / 主仓 `config.template.json` 两 key 皆 0 ✅红 / DEC「前向指针」0 命中 ✅红 / `path_coverage.py:36` 逐字「⇒ 终态 reason 封闭集共 **9** 个。」✅红 (proposal §4 + §5 表均判定勘正为 **8**, yaml 写 8 正确) / DEFAULT_CONFIG 该 key 现 0 命中 ⇒ 003 落后才绿 ✅ | **CLOSED** |
| **A1-PP4-m4** exec_order_note 闭包清单漏 010a | 清单改 `005/006/007a/007b/**010a**/010/011/012/013/014/015/016` (12 项) | 程序化双向核: 12/12 为真 **且**「003 在闭包却未列」= **空集** ⇒ 清单现在是精确集合, 不只是补齐 | **CLOSED** |
| **A1-PP4-m5** helper 轨名「workflow-runner 文件域」含 phase-c 文件 | 轨名改「helper 轨 (workflow-runner 文件域 + 010a 的新建测试文件 — 文件级零共写, 并行安全; R4 A1-m5)」 | 逐字在场; 与 `parallel_tracks.note` 的验证面耦合说明 (010/010a 都依赖 003) 一致 | **CLOSED** |
| **A1-PP4-m6** TASK-001 `branch --show-current` 断言恒真 + worktree remove 不删 probe 分支 | 该断言已删; 收尾改「删远端分支 + `worktree remove` + `git -C aria branch -D probe/152-dispatch` (worktree remove 不删 -b 分支); 结束断言: `worktree list` 不含 tmp, **本地与远端 probe/\* 为空**」 | 逐字在场, 三断言齐 (与我 R4 建议同形); TASK-014 同形处置在场但表述略不对称, 见 m2 | **CLOSED** |

**计**: closed **7** / partial **0** / not_addressed **0**。

跨席簇 3/4 复核 (非本席主责, 顺手核): TASK-014 已写「worktree **基于 feature 分支 HEAD** 建 — 非 9e6a17c:
gate/path_coverage 按 cwd 取仓根, 基线树跑出的是 pending」+ 收尾 probe 清理 (簇 3 ✅);
TASK-016 `conditional_parts` 已写「**§2.1 末段的 `.replace("<pr_branch>", …)` 调用本身**…只删 .replace 调用,
不删行」—— 我实读 proposal `:93-95` 三行确实同时承载 `verify_note` 后缀与 `raw_message` 重同步, 删调用后
`m = out["gate_error"]["message"] + verify_note` 两者都保住 (簇 4 ✅)。

---

## Findings

### 必须改 (Major)

**无。** 本席 R5 零 Major。

### 还能挑 (Minor — 均不构成 REVISE 理由; 可在 B.1 前顺手落, 也可不落)

#### [A1-PP5-m1] SC-15 红窗依赖「最终版测试文件对基线 scripts/ 仍可收集」, 但 v5 只把这条性质钉在 TASK-002 (exec 4), 没钉在最终文件 (exec 16)

TASK-012 的红窗要「断言失败而非收集错误」, 前提是 `test_pre_merge_gate.py` **最终态**在基线 `scripts/` 下
import 得动。当前文件风格天然满足 (`import pre_merge_gate as gate` 属性访问 + `from ci_backends import
(...)` 名单基线全在), 我实跑确认 ✅。但 TASK-005/007a 若给模块级 from-import 加一个新符号
(如 `from pre_merge_gate import _no_run_gate_error`), exec 16 的红窗就静默退回「收集错误」——
正是 memory `fix_recurs_in_its_own_fallback_path` 的形状 (同一处第三次)。
TASK-002 的 verification 只覆盖它自己那一刻。
**建议**: 在 TASK-002 notes 或 INV-2 加一句约束「phase-c tests 新增符号一律走 `gate.<name>` 属性访问,
不得在模块级 from-import 本 spec 新增的名 (否则 TASK-012 红窗退化为收集错误)」。

#### [A1-PP5-m2] TASK-014 的收尾三项里中间一项是**动作**不是断言, 与 TASK-001 不对称

TASK-001: 「结束断言: `worktree list` 不含 tmp, **本地与远端 probe/\* 为空**」(三断言)。
TASK-014: 「`worktree list` 不含 tmp + `git -C aria branch -D probe/…` + 远端 probe/\* 为空」——
中间那项是删除动作, 没有对应的「本地 probe/\* 为空」断言。残留风险很低 (`branch -D` 就在原地),
但两处同形收尾用了两种口径。**建议**: TASK-014 对齐成 TASK-001 的措辞。

#### [A1-PP5-m3] TASK-014 没给字面 worktree 命令, TASK-001 给了

TASK-001 写死 `git -C aria worktree add <tmp> -b probe/152-dispatch 9e6a17c`; TASK-014 只写「worktree
**基于 feature 分支 HEAD** 建」。意图无歧义 (不会分叉出错误结果), 但同一形状一处可粘贴一处要自拟。
**建议**: 补 `git -C aria worktree add <tmp> -b probe/152-sc13 HEAD` 一行。

#### [A1-PP5-m4] `execution_order` 的 helper 轨仍写成 `008 → 009 → 010a → 010` 串行箭头, 而 010a 已去掉 009 依赖

v5 按 A2-m1 把 `TASK-010a.dependencies` 收成 `[TASK-003]`, 于是 010a 与 008/009 之间**没有依赖边**了,
真实可并行度比叙述宽。`exec_order` 自陈是 advisory tie-break, 所以不影响正确性 —— 但叙述层与依赖图不再
同构, 照叙述排班会白白串行。**建议**: 改成「008 → 009 ∥ 010a (只需 003) → 010」或在 note 点一句。

#### [A1-PP5-m5] INV-1 那条承重命令写在 YAML **双引号** scalar 里, 原文含 `\"` 转义 —— 直接从文件复制粘贴会坏

`git -C aria show \"$1:…\"` 若被人从 raw yaml 逐字粘进 bash, `\"` 是**字面双引号字符**, git 会报
`invalid object name`。程序化读 (`yaml.safe_load`) 无此问题, 我正是这么抽出来跑通的; 但 B.2 执行者大概率
是肉眼复制。这是全文件唯一带 `\"` 的长命令 (INV-3 的 grep 用单引号, 无此问题)。
**建议**: 把 `INV-1.encoded_as` 里那段命令挪进 block scalar (`encoded_as: |`), 或整条用 block scalar,
使命令在文件里就是可粘贴形态。

---

## 已核验无误 (R5 实测; 按 memory `predict-then-measure` 先写预期再跑)

1. **INV-1 命令逐字可复跑且双向有判别力** (见处置表 M1 行): 三例退出码 0/0/1, 反例
   `AssertionError: pending`, 正例 (patched) 返 `not_found`。`aether.py` 相关行号 `:216-217` staticmethod /
   `:218` docstring / `:225-226` `if not runs: return "pending"` 实读命中。
2. **SC-15 红窗端到端可复现**: worktree(9e6a17c) + 拷入当前 tests/ + 模拟绑定用例 →
   `AssertionError: 'green' != 'wait'` (1 failed), 无收集错误。`test_pre_merge_gate.py:23-24` 的
   `sys.path.insert(0, dirname(dirname(_HERE))/"scripts")` 证实 v5 那句相对导入声明属实;
   `phase-c-integrator/tests/` 无 conftest.py, 无跨仓 sys.path 污染。收尾 `worktree remove` 后
   `git -C aria worktree list` 只剩主工作树, aria 树 clean。
3. **全部机检不变量再次程序化通过**: `total_tasks` 20 = 实际 20; `exec_order` = {0..19} 唯一;
   「每任务 exec_order > 其所有 dependencies」violation **0**; 悬空依赖 **∅**; DAG **无环**;
   `TASK-003 ∈ 12 项闭包` **12/12** 且反向「未列出的闭包成员」**∅** (精确集合);
   `TASK-010a ∈ TASK-010/011 闭包` 均真; `agent_summary` ↔ 逐任务 `agent` **双向集合相等**
   (qa 6 / be 4 / km 2 / main-loop 8 = 20, 无表外 agent); `estimated_hours` 求和 **51.0** = metadata;
   parent 集合 {P0..P7} = 8; 20/20 有 `reason`; `<4h` 计数 **15** = `estimation_note` 自称。
4. **三处顺序面仍三方一致**: `exec_order` 数字 ↔ `execution_order` 四行叙述 (P0 0-2 / gate 轨 3-9 /
   helper 轨 10-13 / 汇合 011=14 → 013=15 → 012=16 → 014=17 → 015=18 → 016=19) ↔ `parallel_tracks`
   轨内序, 逐任务比对无出入 (叙述的并行度问题见 m4, 非顺序矛盾)。
5. **SC-14 六条断言逐条基线实测** (处置表 m3 行已列): 五红一「003 后转绿」, 与 v5 verification 的
   「前五条全红 / 第六条绿」逐条对得上; `path_coverage.py:36` 的「9」与 proposal §4「reason 族 = 8,
   `:36`「共 9 个」是既有错…勘正为 8」+ §5 表行「`:36`「共 9 个」→ 勘正 8」三方一致 ⇒ yaml 写「为 8」正确。
   顺带核: `:36` 的勘正**同时**登记在 §5 表 (无条件面), 所以即使 `dispatch_viable=false` 时 §4 整段被删,
   这条改动在归档件里仍有出处, 不悬空。
6. **INV-3 两态仍成立**: 负控 pattern `grep -rn -E 'DISPATCH_VIABLE|dispatchable_workflows|/dispatches -d'`
   限六落点 **exit=1 零命中**; `pre_merge_gate.py` 中 `<pr_branch>` **0**; true 分支已换成渲染结果断言。
   `references/` 豁免使 traps §六 的 F6 行 (合法提及 dispatch) 不污染负控。
7. **SC-14 断言 1 的作用域核准**: `workflow-runner/SKILL.md` 中 `pr_ci_status` **0 命中** ⇒
   「所有 SKILL.md 枚举行」实际只落 phase-c 一处 (TASK-011 承载); TASK-010 作为 SC-14 GREEN 端之一是靠
   config.template 两 key, `sc_coverage_crosscheck.SC-14 = [010a, 010, 011]` 三者各有实质承载, 无凑数。
8. **AB / Rule #6 面事实未漂移**: catalog `phase-c-integrator-pre-merge-gate.json` version **1.1.0**,
   fixtures **7** (green/wait/wait_then_green/fail/NEG-1/NEG-2/NEG-3), **7/7 都有
   `test_case_in_unit_tests` 字段** ⇒ TASK-012 的绑定在 schema 上可表达; NEG-3 元键**恰 8 个**且与
   TASK-012 title 列的八键逐字同; `ab-results/` 全 30 个目录 `grep -rl NEG-3` **零命中** ⇒ INV-7
   「NEG-3 零执行史不得复制」前提属实。
9. **TASK-015 版本面逐点复核**: `CLAUDE.md:139`/`:141` / `VERSION:24` / `README.md:8`+`:242` /
   `marketplace.json:3`+`:16` 实读全为 **1.66.4**, 与 `baseline_sha: 9e6a17c` (= v1.66.4 release commit)
   自洽, 行号与 title 逐字吻合; `target_version: 1.66.5` 一致。
10. **§7 checklist 四项落点仍在位**: 1 → `TASK-007b.verification`「DISPATCH_VIABLE 读法 = 裸全局引用
    (monkeypatch 负控能红)」/ 2 → `TASK-012.title`「覆盖 phase-c surface + workflow-runner should_prompt
    两 skill」/ 3 → `TASK-014.notes`「traps 两处证据统一日期字段」/ 4 → `TASK-008.notes`「record 缺失文件
    + verdict≠wait 分支单测」; INV-6 的「唯一例外」句 (checklist 1 随 007b 整体 N/A) 逐字在场。
11. **TASK-016 §3.5 全清单仍完整**: v5 新增的第 9 项「只删 `.replace` 调用本身」我对 proposal `:93-95`
    逐行实读验证 —— 那三行确实同时承载 `verify_note` 与 `raw_message` 重同步, 删整行会连带删掉两个
    **无条件**行为; 删调用后剩 `m = out["gate_error"]["message"] + verify_note`, 语义正确。
    R4 我列的 14 处 proposal 提及, 该删的仍全在清单内, 该留的 (F6 事实行 / §3.5 规则本体 /
    SC-5 (c1) 守卫) 仍未被误列。
12. **`metadata.post_planning` 的 owner 裁定留痕在场**: `rounds_so_far: 4` +
    `owner_ruling_2026-08-23: "max_rounds=4 耗尽 … 选 [2] 加 1 轮 R5 稳定性确认 (max_rounds 4→5)"` ——
    Rule #10 要求的「AI 不自豁 / owner 决定入档」这条做到了 (加轮是 owner 的, 不是 AI 的)。
13. **`audit_checkpoints_note` 仍属实**: `.aria/config.json` 的 mid_implementation / post_implementation /
    pre_merge / post_closure 四个显式 `off` (Rule #10 白名单第一类), 故不排 B/C/D 审计任务成立。

---

## Verdict

**PASS** (0 Critical / 0 Major / 5 Minor) — **vote: PASS**

**「必须改」: 零条。** v5 是本 spec 三轮以来第一次, 我报的问题**全部**以「实跑过的字面量」形式落地, 而不是
以「更好的措辞」落地 —— 我把 INV-1 命令从 yaml 里程序化抽出后原样跑通并验了两个方向的判别力, 把 SC-15
红窗端到端复现出 `AssertionError: 'green' != 'wait'`。这两条恰是 R4 全席 6 个 Major 里最承重的两个,
它们从「写着但跑不了」变成「跑得了且会红」。

**五条 minor 都不构成 REVISE 理由**: m1 是一条预防性约束 (当前风格天然满足, 我实测过), m2/m3 是同形任务
两处口径不齐, m4 是叙述层并行度保守, m5 是 YAML 引号形态。**没有一条会让实施者做出错误的东西** ——
最坏情况是多串行一步 (m4) 或粘贴命令时手动去两个反斜杠 (m5)。

**处置建议 (给主控)**: **收敛, 进 B.1**。理由三条:
(a) 本席 Major 曲线 7→3→3→1→**0**, 且 R5 是**稳定性确认**语义 —— v5 相对 v4 的五簇改动我逐簇实测,
    零回归、零新矛盾, 也没有出现「上轮 fix 引入同等量新缺陷」(memory `marginal_return_negative` 的拐点
    判据: 本轮 5 条 minor 中只有 m2/m4 两条源自 v5 新写文本, 占比 2/5 < 1/2, 且都在措辞层);
(b) 五条 minor 是可选的分钟级清理, 建议**顺手落但不重跑审计** —— 落 m1 (一句约束) 与 m5 (改 block scalar)
    收益最高, m2/m3/m4 纯整洁;
(c) 结构层 (拓扑/闭包/算术/双向 agent) 与转录层 (SC-14 六断言 / §5 表 / 行号锚点 / 14+2 版本点 / AB 元键)
    这轮我做了与 R4 同宽的复测, **零漂移**; 继续加轮已无可发现的量。

**给 B.2 执行者的一句提醒** (非 finding, 进 handoff): v5 里两条最承重的检查 (INV-1 四合取 / SC-15 红窗)
在本轮**已被实跑证明可执行且会红**, 执行时若遇到它们不红, 第一反应应是「我改的东西不对」而不是
「检查写错了」—— 前三轮的经验相反, 这次方向翻过来了。
