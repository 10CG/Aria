---
checkpoint: post_spec
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T11:40:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 0
minor_count: 3
---

## 摘要

**我 R6 的唯一 Major (SC-5 互斥) 真闭了, 而且我没有只读文本判它闭 —— 我按 v7 §2.1/§2.2/§2.3 的逐字语义写了一个「正确实现」, 把 SC-5 的 (a)(b)(c1)(c2)(d) 全部子项连同封闭表 7 个档一起跑了一遍: 7/7 变体同时满足 (c1), (c2) 只在 dispatch 变体成立, (b) 停在「评估已关闭」档, (d) 末尾带核验附注且副本通道同步。** R6 那对互斥子句在 v7 下**联合可满足**, 且我 R6 点名的「路径 B」(把占位符塞进全部档换取测试变绿) 的驱动力已被移除 —— 现在没有任何 SC 逼实施者去动那张钉死的封闭表。

`dispatch_viable=false` 兜底分支也复核过: 删除组现在含 SC-5(c2) 与 §2.1 那句 `.replace`, 我实跑 `DISPATCH_VIABLE=False` 确认 message 既不含 `dispatches` 也不含分支名 ⇒ 无零消费方残留 (R4 A1-m6 的形状没在自己的兜底路径复发)。

**票 PASS**, 与我 R6 声明的「修后转 PASS」一致。残余 3 条 minor, 全部单独或全部不改都不阻塞 A.2; 其中 1 条是 R6-m3 修法的顺手副产品 (步骤序), 1 条是我 R6-m1 只落了一半, 1 条是已被 R5/R6 判非阻塞的 Rule #6 收口面 (**我不重开, 只写清它的形状**)。

---

## R6 处置核对

我 R6 交了 1 Major + 5 minor。逐条实核 (证据全部本轮重跑, 不引 R6 结论):

| 条目 | 状态 | 本轮证据 |
|---|---|---|
| **A1-R6-M1** (SC-5 (b)(c) 互斥 + §3.5 删除清单漏项) | **closed** | v7 SC-5 拆 (c1)「所有变体: message 不含字面 `<pr_branch>` 且 `raw_message == gate_error.message`」/ (c2)「仅 `dispatch_viable=true`: enabled + **pc stub 含 dispatchable** + `DISPATCH_VIABLE=True` 变体 → 含 `feat/x`」。**仿真实跑** (见下方证据块): 一个正确实现使 (a)(b)(c1)(c2)(d) 同时绿, 互斥消失。§3.5 (`:196`) 删除组现逐字含「SC-5 (c2) + 3.3 (a) 行 + §2.1 末段的 `<pr_branch>` `.replace`」并注明「(c1) 的「不含占位」断言保留作守卫」✓ |
| **A1-R6-m1** (branches 第三成因: message 兄弟档 + §3.3 处方) | **partial** | 诊断半边**两个档都落了**: `:127` trigger-matched 与 `:128` workflow-files-changed 现在都写「或 `branches` 过滤不含本分支」✓。处方半边**仍未落**: `:185` §3.3 (b) 逐字「第二次 push 是普通 diff, **paths 正常评**」, 无 branches 例外 → 顺延为 **m2** |
| **A1-R6-m2** (Impact 漏 `reset_retry_count`) | **closed** | `:253` 现列「…`reset_no_run_observations` `reset_retry_count` + CLI」✓ 与 `:153` 的「对称」说法对齐 |
| **A1-R6-m3** (SC-13 收尾未清 gate_state) | **closed** (带一条新的步骤序 nit → m1) | `:274` 现含「**收尾 CLI `clear` 主仓 gate_state** (否则 600s 零 run 那条腿留 `status=waiting` ⇒ 下个 workflow resume 幽灵 gate)」✓。实读 `gate_state_helper.py:158-161` `clear_gate_state` = `state["gate_state"] = None` (不删文件) + `:164-167` `is_gate_active` 读 `status == "waiting"` ⇒ 我 R6 给的机理逐字成立 ✓ |
| **A1-R6-m4** (`--state-file` 从纪律变结构) | **closed** | `:151` 「**`--state-file` 必填无缺省**, 缺失 exit 2 — 与 `--source` 同形 fail-closed」+ synopsis 改 `<绝对路径>` ✓; SC-11(d) `:272` 「**缺 `--source` 或缺 `--state-file` 各 exit 2**」✓。同句「Python API 默认 cwd 相对不变」也属实 — 实读 `load_state(path=".aria/workflow-state.json")` / `atomic_write_state(..., path=...)` (`:66`/`:86`) ✓ |
| **A1-R6-m5** (三条「留 Phase B 顺手」无承载物) | **closed** | 新增 §7 (`:233-238`) 4 项, 我点名的三条 (`DISPATCH_VIABLE` 裸全局引用 / SC-15 两 skill / traps 日期字段) 全部在列, 另加 A2-R6-m1 的 `record` 单测 ✓ |

**统计 (条目粒度)**: closed **5** / partial **1** / not_addressed **0**。

### 证据块 — SC-5 闭合的仿真复核 (不靠读文本)

脚本 `/tmp/claude-1000/-home-dev-Aria/fe7831ec-1fd8-432f-bb97-4514f7c87e97/scratchpad/r7_a1_sc5_sim.py`: 按 §2.3 封闭表 6 档 + §2.2 + §2.1 末段回填逐字实现, 对 7 个变体跑 SC-5 全子项。

```
(a) enabled              c1-no-placeholder=True c1-copychan=True contains-feat/x=False
(b) disabled             c1-no-placeholder=True c1-copychan=True contains-feat/x=False
(c2) dispatch            c1-no-placeholder=True c1-copychan=True contains-feat/x=True
(d) verify-failed        c1-no-placeholder=True c1-copychan=True contains-feat/x=False
files-changed / empty-diff / unknown-internal-error   同 (a)
DISPATCH_VIABLE=False → message 含 dispatches? False | 含 feat/x? False
SC-5 全子项: PASS
```

三条配套实测:

1. `_sanitize_for_json` (`pre_merge_gate.py:292-299`) = `text.encode("utf-8","replace").decode("utf-8")` ⇒ 对 `feat/x` 是恒等映射, (c2) 的「含 `feat/x`」不会被消毒破坏 ✓ (前六轮没人验过这一步)。
2. (c2) 逐字要求「pc stub = trigger-matched **含 dispatchable**」—— 这正好补上我 R6 事实链第 5 点: 基线 mixin 的 `_PC_COVERED_STUB` (`test_pre_merge_gate.py:49-56`) **无** `dispatchable_workflows` 键 (本轮实读确认), 照旧 stub 写 (c2) 会恒红; v7 显式点了新 stub ✓。
3. `_build_output` (`:236-275`) 基础六键 + 两个可选键 ⇒ SC-5(a)「六键俱在」是「六个基础键都在」而非「恰好六键」, 与 (a) 同时要求 `path_coverage`+`gate_error` 在场不矛盾 ✓。

### v7 13 处 diff 稳定性 (逐处过, 只报有问题的)

Status/rounds/owner_rulings (`:13`/`:20-23`) · SC-5 拆分 (`:266`) · §3.5 清单 (`:196`) · `--state-file` 必填 (`:151`) · SC-11(d) (`:272`) · Impact (`:253`) · §2.3 files-changed 档 (`:128`) · SC-13 `clear` (`:274`) · §7 (`:233-238`) · Cross-refs R3-R6 (`:306`) · DEC 行「主仓」前缀 (`:223`) —— **全部在位**。交叉一致性 (memory `fixes_contradict_each_other_across_clusters` 的形状) 逐对查过:

- `--state-file` 必填 × telemetry 派生: 派生式 `<dirname(state-file)>/gate-state-telemetry.jsonl` 在必填后恒有定义, 且与 SC-13「state 文件 = 主仓绝对路径」+ frontmatter `partition: .aria/gate-state-telemetry.jsonl` (主仓根相对) 三者同指一个文件 ✓ 反而比 v6 更硬。
- `--state-file` 必填 × §3.2 步骤 2/3c′ 的显式传参: 不冲突, 后者变成冗余保险 ✓。
- SC-13 `clear` × SC-16(c): `clear` 只置 `gate_state=None`, 不动 telemetry 分区 ⇒ 归档门探针的 `source=production` 记录不受影响 ✓。
- 时间轴 (`:179`) 复核: 实读 `DEFAULT_INTERVALS_SECONDS = (30,60,120,300,300)` (`gate_state_helper.py:38`) ⇒ 90s / 810s 两个数逐轮实算仍对 ✓。
- 新增 §7 未与既有 §6 编号冲突; rule6_note 引的「§6.3」仍指 Phase D 待办第 3 条 ✓。

---

## 新 Findings

### 必须改

**无。** critical 0 / major 0。

### 还能挑 (minor — 全部不改也不阻塞 A.2)

- **[A1-R7-m1]** *(R6-m3 修法的副产品)* **SC-13 的收尾步骤序把证据抄录排在 `clear` 之后**。`:274` 末段字面顺序是「删分支; **收尾 CLI `clear` 主仓 gate_state**; **证据 (workflow-state 片段 + telemetry 行 + Δt) 抄进 traps §6**」。实读 `clear_gate_state` 是 `state["gate_state"] = None` ⇒ 照字面顺序执行, 「workflow-state 片段」这项证据在抄录时已被清空; 而活体是一次性的 (throwaway 分支已删、600s 那条腿不可重放), 只能重跑一遍才能补。**一行修**: 把证据抄录挪到 `clear` 之前, 或在 `clear` 那句前加「(证据须先抄, `clear` 会把 gate_state 置 null)」。
- **[A1-R7-m2]** *(我 R6-m1 未闭的那半)* **§3.3 处方 (b) 与刚补进 §2.3 的第三成因不一致**。`:127`/`:128` 现在都告诉读者「可能是 `branches` 过滤不含本分支」, 而 `:185` 的处方 (b) 仍逐字「第二次 push 是普通 diff, **paths 正常评**」—— 若真因是 branches 过滤, 推 commit 一定无效, 读者会照处方白推一次。诊断已经三成因, 处方仍两成因。**一行修**: (b) 末尾加「若 message 提示 branches 成因, 推 commit 无效, 改用 (a) 或改 workflow 的 `branches:`」。典型 `fix_the_class_not_the_instance` 的剩余半边。
- **[A1-R7-m3]** *(已被 R5/R6 判非阻塞, **我不重开**, 只写清形状供 A.2 取舍)* **§7 item 2 的义务强于 SC-15 的绑定文本**。rule6_note (`:281`) 点名**两条**可证伪行为 (phase-c surface `gate_error.message` 原文 / workflow-runner `should_prompt=true` 时出 prompt), 但 SC-15 (`:276`) 只要求 NEG-4 进 `phase-c-integrator-pre-merge-gate.json` 的 `fixtures[]` 并把 `test_case_in_unit_tests` 绑到 SC-2 的 trigger-matched 用例 —— 我实读该 catalog (7 fixtures, `version 1.1.0`) 与 NEG-3 的 `_consumed_by` (「Documentation + eval prompt data」), 结构上一个 fixture 可同时喂两个 skill 的 eval, 但 **SC-15 字面不要求**, 所以「SC-15 全绿而 workflow-runner 那条行为零覆盖」是可达状态。§7 item 2 正是要防这一点, 但它是 checklist 不是 SC。**若要收口, 一行** = 把「覆盖 phase-c-integrator (surface) 与 workflow-runner (should_prompt) 两 skill」并进 SC-15 的断言句; 不收口也可以 —— 那就是 Rule #6 第三行「缺一照跑」的照跑路径, 需在 A.2 明记选了哪条。

---

## Verdict

**verdict: PASS · vote: PASS** (critical 0 / major 0 / minor 3)

我 R6 写了「修后转 PASS」, 这轮把话兑现前先做了实证而不是复述: **SC-5 的闭合是仿真跑出来的, 不是读出来的**。我 R6 的事实链有 6 环 (封闭表无占位 / `.replace` no-op / (b) 恒红 / (a) 因 stub 缺键也不含分支名 / false 分支删除清单漏项 / 两实施者分叉), v7 逐环都有对应动作: (c1) 换成「不含占位 + 副本同步」两个所有变体都成立的量 (memory `redfix_change_quantity` 的正确形状 —— 换量而不是调阈值), (c2) 点名新 stub 补上第 4 环, §3.5 清单补上第 5 环。第 6 环「两实施者必然分叉」随之消失: 规格自洽后两人都照 §2.3 走, 不再需要替 owner 做规格裁量。

**Major 轨迹 6(+1C) → 6 → 3 → 1 → 1 → 0** (我席)。本轮 3 条 minor 里, 1 条是上轮 fix 的副产品 (m1), 1 条是上轮 fix 只落一半 (m2), 1 条是早已被判非阻塞的老账 (m3) —— **没有一条是 spec 本体的新缺陷**。这正是 `marginal_return_negative` 描述的拐点之后的画面: 本轮产出的 100% 是上一轮修补痕迹的尾巴。R7 作为形式全票确认轮已经完成它的职能, **不应再有 R8**; m1/m2 两行措辞由主控或 A.2 起草时顺手落即可, m3 在 A.2 转 tasks 时二选一并写明。

给主控的一句判定输入: 我这轮唯一有可能改变票型的动作是那次仿真 (7 变体 × 4 子项), 它的结论是「联合可满足」。若有第八轮, 它能查的东西我这轮已经用一个 60 行脚本查完了 —— 剩下的不确定性全在 B.2 的第一条测试里, 不在第八份报告里。
