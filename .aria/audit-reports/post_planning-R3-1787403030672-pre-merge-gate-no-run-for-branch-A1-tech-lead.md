---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T14:13:33.036Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 3
minor_count: 6
---

# post_planning R3 — A1 席 (tech-lead) · pre-merge-gate-no-run-for-branch (v3)

## 摘要

**v3 的结构面全部实测过关**: 19 任务 / 49.5h / 8 parent 三项算术自洽; `exec_order` 0..18 无重无缺且
**每任务 exec_order > 其所有依赖** (0 violation); `TASK-003 ∈ 11 个下游闭包` 断言逐条为真; DAG 无环;
19/19 有 `reason`; 三处顺序面 (exec_order 数字 / `execution_order` 段 / `parallel_tracks` 轨内序) 三方
一致 —— 我 R2 Verdict 里点名要主控机械复跑的两项判别式 **(i)(ii) 全部成立**。我 R2 的 3 Major 全 closed。

**但三条 Major 仍在, 且三条都长在 v3 的修复上** (第三轮同形状; memory `fix_recurs_in_its_own_fallback_path`
/ `fixes_contradict_each_other_across_clusters`):

1. 我 m2 要的「条件组负控」落了 —— 但那条 grep **在基线就已命中 1 次**, 结构上永远不可能「零命中」
   (恒红 = 零信息, memory `false_green_dual_is_permanent_red`), 而它是 INV-3 false 分支的**唯一**机械守卫。
2. 我 m1 要的「INV-1 有向核验挂到 main-loop」落了 —— 但把语义谓词具体化成 `grep -c 'return "pending"'`
   的过程中**判别力被换掉**: 该 grep 在基线返 **2**、改后返 **1**, 「命中」在改前改后都成立 ⇒ 第一个合取
   项恒真; 与第二合取项联立后, 仍存在一种拆 commit 方式两项全绿而 INV-1 被违反 (memory
   `assertion_swap_can_sever_link_to_defect` / `redfix-change-quantity`)。
3. 我 m6 要的「SC-14 脚本进 deliverables」落了 —— 但落点从 exec 13 **后移到 exec 15**, 即写在它所断言的
   文档改完之后; 同族的 SC-15「回退后转红」用的是 `git stash`, 而代码在 aria **子模块**里且届时已提交。
   ⇒ 16 条 SC 中恰有 **两条 (SC-14 / SC-15) 的红窗在 v3 编码下不可观测**。

无 Critical。三条的修法都是 verification 里一两行的量替换 + 一次任务位移。

---

## R2 处置核对

我 R2 报的 3 Major + 8 minor 共 11 条 (对应 R2 聚合簇 #1-#7 中归本席的部分):

| R2 条目 | v3 落点 | 核对 (实测) | 判定 |
|---|---|---|---|
| **A1-PP2-M1** exec_order 未前移 | 全表重编 (004=3 / 002=4 / 003=5 …) + `TASK-002.dependencies` 加 TASK-004 + 物理块移到 P1 首位 | 机检 19 任务: exec_order 集合 = {0..18} 无重无缺; **exec_order > 所有依赖 violation = 0**; 三处顺序面逐条一致 (gate 轨 `[004,002,003,005,006,007a,007b]` = 3..9 / helper 轨 = 10..12 / 汇合 = 13..18) | **CLOSED** |
| **A1-PP2-M2** TASK-003 闭包丢失 | 005/006/010 → 003 边; 014 → 013 | 传递闭包实算 11 个目标: 003 ∈ 005/006/007a/007b/010/011/012/013/014/015/016 **全为真**; 002/004 亦在全部闭包内; 无环 | **CLOSED** |
| **A1-PP2-M3** B.1 分支零承载 (aria 侧尤甚) | 新 **TASK-000b** (exec 1, 两仓分支, main-loop); 002/004/008/001 依赖之; TASK-015 (ii) 改「在 TASK-000b 建的分支上」 | 两仓 deliverables 齐; verification 断言两仓 `git branch --show-current` + `aria HEAD == 9e6a17c`; notes 引 `detached_head_may_be_stale_rebase`; parser 实跑对 `TASK-000b` 这个非纯数字 id 解析正常 (19/19) | **CLOSED** |
| A1-PP2-m1 INV-1 无 main-loop 承载 | 移到 `TASK-013.verification` (agent = main-loop) + `INV-1.encoded_as` 具体化为 `git show` | 承载归位 ✅ (main-loop 任务里有了、失败会发红了) —— 但具体化后的**量**不判别 | **PARTIAL** → M2 |
| A1-PP2-m2 conditional_parts 无负控 | `TASK-013.verification[2]` grep 负控 | 负控在场 ✅ —— 但基线实测已 1 命中 ⇒ 恒红; 且 TASK-006 的 `.replace` 那半仍无任何核验 (无害, 见 m5) | **PARTIAL** → M1 |
| A1-PP2-m3 proposal 自删零承载 | `TASK-016.conditional_parts` | 逐条比对 proposal §3.5 清单: §4 整段 / SC-8 / SC-9 dispatchable / SC-2 子项 / SC-5 (c2) / 2.3 渲染句 / 3.3 (a) / Impact 两项 / §7 checklist 1 标 N/A —— **9 项齐**, 且 TASK-016 依赖 TASK-001 | **CLOSED** |
| A1-PP2-m4 reason 7/18 + 无 schema_note | 逐任务 `reason:` 字段 + `metadata.schema_note` | 机检 **19/19 有 reason**; `schema_note` 在场并逐项声明三处偏离 (parent 保留 / int hours / reason 字段) 的先例出处 | **CLOSED** |
| A1-PP2-m5 SC-15 绑定名在产出任务无承诺 | `TASK-002.deliverables` 点名 `test_sc2_trigger_matched_message` | 两处同名逐字一致 (TASK-002 deliverable ↔ TASK-012 notes `NotFoundVerdictTests.test_sc2_trigger_matched_message`), 且明标「非参数化具名用例」 | **CLOSED** |
| A1-PP2-m6 SC-14 脚本不在 deliverables + km 写测试 | 移进 `TASK-013.deliverables` (agent main-loop, reason 注「qa 子 agent 写」) + TASK-013 依赖 011 | deliverable 在场 ✅、013 闭包含 011 ✅ (SC-12 计数会包含它) —— 但落点 exec 13 → **15**, 红窗更远 | **PARTIAL** → M3 |
| A1-PP2-m7 v1.66.1 同缺 tag | TASK-015 title 补打两 tag | 「v1.66.4@9e6a17c 与 v1.66.1@<plugin.json 首次 =1.66.1 的 commit>」在场, 引 version-management §4.3 | **CLOSED** |
| A1-PP2-m8 归档门正交 warn 未预告 | `TASK-016.verification[2]` 预告 | **两态实测**: v3 原文合成全 completed → `unverified_claims` 只有 `runtime_probe:record`, **无** `archive-safety-net-integration-claims-unverified`; 把「调用」塞回 TASK-005 title → 该 claim 立刻复现 ⇒ 簇 #8 的改词与簇 #7 的预告互相抵消, 预告现为**假预期** | **PARTIAL (反向)** → m1 |

**计**: closed **7** / partial **4** / not_addressed **0**。

---

## Findings

### [A1-PP3-M1] INV-3 false 分支的唯一机械守卫 (`TASK-013` grep 负控) **在基线就已命中 1 次** —— 恒红, 且更硬的合法命中会在 TASK-011 写 traps 时进来

- **锚点**: `TASK-013.verification[2]`「条件组负控 (dispatch_viable=false 时): `grep -rn dispatches
  aria/skills/phase-c-integrator aria/skills/workflow-runner` **零命中**」· `INV-3.encoded_as` 末句
  (「TASK-013 对 false 分支做 grep 负控」) · 我 R2-m2 的处方
- **实测** (逐字复跑 verification 里的命令, 主仓根, 当前基线 9e6a17c, 本 spec 一行未落):

  ```
  $ grep -rn dispatches aria/skills/phase-c-integrator aria/skills/workflow-runner
  aria/skills/phase-c-integrator/scripts/submodule-tripwire-audit.sh:6:# 5/5 dispatches: the Forgejo Actions runner cannot clone the `ssh://forgejo@...`
  $ … | wc -l → 1
  ```

  该命中与 dispatch 处方毫无关系 —— 是 tripwire 脚本注释里英文动词 "dispatches"。⇒ **该负控在
  `dispatch_viable` 取任何值时都不可能通过**。
- **第二处 (更难绕开)**: 即便排除上面这行, `TASK-011.title` 明写「traps §六 … 插入 F3 / F4 / (b) 轴同形 /
  **F6 404+basename** 四行」, 而 F6 的事实本体 (proposal Why 表 F6) 就是
  「`POST …/actions/workflows/{file}/dispatches` 路由存在, 按文件名寻址」; TASK-001 的 traps 证据行也要记
  dispatch POST 的 HTTP 码。这些是**该留下的**内容, 却全在 grep 的覆盖目录 (`references/` 在
  `phase-c-integrator` 下) 内。
- **为什么是 Major**: 这是 INV-3 false 分支唯一会发红的东西。恒红的检查等价于假绿 (memory
  `false_green_dual_is_permanent_red`): 执行者要么被一条与缺陷无关的命中挡住去查, 要么学会「这条本来就红,
  跳过」—— 后者一旦发生, INV-3 从此无人守。两个执行者对「该怎么缩小 grep 范围」必然给出不同答案 (分叉)。
- **建议** (memory `redfix-change-quantity`: 别在同一个量上调阈值, **换量**), 三条一起:
  (a) 把量从「全目录 `dispatches` 零命中」换成**生成面**零命中:
  `grep -rn '/dispatches' aria/skills/phase-c-integrator/scripts aria/skills/phase-c-integrator/tests` == 0
  且 `grep -c DISPATCH_VIABLE aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` == 0;
  (b) 文档面改成**限定段落**: SKILL.md §C.2.4 步骤 6 处方段 + 2.3 message 表内零命中 (不含 `references/`);
  (c) 明写豁免清单与理由: `references/pre-merge-gate-empirical-traps.md` (§六 F6/TASK-0a 证据本就该提
  dispatch 端点) 与 `scripts/submodule-tripwire-audit.sh:6` (既有无关英文)。
  并补 **true 分支的对偶断言** (`dispatch_viable=true` 时上述生成面命中 ≥1), 使这条检查两态都有信息。

---

### [A1-PP3-M2] INV-1 有向核验的机械形式 `grep -c 'return "pending"'` **在改前改后都命中** —— 第一合取项恒真, 与第二项联立仍有一条两全绿而 INV-1 被违反的拆分

- **锚点**: `INV-1.encoded_as`「非破坏性 `git show <commit>^:skills/…/aether.py | grep -c 'return "pending"'`
  在父提交版本命中「零 run → pending」行, 且 `git show --stat <commit>` 同含两文件」·
  `TASK-013.verification[1]` (同义中文版) · `TASK-003.verification[1]`
- **实测** (aria @ 9e6a17c):

  ```
  $ grep -n 'return "pending"' skills/phase-c-integrator/scripts/ci_backends/aether.py
  226:            return "pending"      ← 零 run 分支 (§1 要改的那行)
  238:        return "pending"          ← 未知 status 的兜底 (proposal §1「其余映射不变」⇒ 本 spec 不动)
  $ grep -c … → 2   (改后 → 1)
  ```

  ⇒ 「命中」(count ≥ 1) 这个谓词在**父提交已经改过 aether.py 的情况下同样为真**。第一合取项因此不携带
  任何关于「§1 是否已提前落地」的信息 —— 而它存在的全部理由正是判定这一点。
- **联立后的漏洞 (为什么第二合取项兜不住)**: 取拆分 A = `aether.py:225-226`(行为) 单独一个 commit,
  B = `aether.py:218`(docstring) + `pre_merge_gate.py`。则对 B:
  `git show --stat B` **同含两文件** ✅; `git show B^:aether.py | grep -c 'return "pending"'` = 1 ⇒ **命中** ✅。
  两项全绿, 而在 commit A 那一刻树的状态正是 `backend → not_found` + 旧 `compute_verdict` =
  **`verdict=green`** —— proposal §1 硬约束和 INV-1 存在的唯一目的 (「§1 单独落地 = 盲区从恒 wait 变恒
  green, 更坏的 fail-open」) 被完整地违反了。
- **与 R2 的关系 (必须说明白)**: 我 R2 「已核验无误 #13」判过这条检查「维度匹配、判别力成立」—— 那是对
  **语义谓词**「父提交上 `_normalize_pr_ci_status([]) == 'pending'`」的判定, 它确实成立。v3 把它换成
  `grep -c` 这个**代理量**时判别力丢了 (memory `assertion_swap_can_sever_link_to_defect`)。这不是我 R2 判错,
  是 v3 换量引入的新缺陷; 但也说明「语义谓词 → 命令行」这一步本身需要复核, 不能默认无损。
- **建议** (三选一, 都是一行):
  (a) **直接跑语义谓词** (最贴 INV-1 原文):
  `git show <c>^:skills/phase-c-integrator/scripts/ci_backends/aether.py > /tmp/base_aether.py` →
  `python3 -c "…exec…; assert _normalize_pr_ci_status([]) == 'pending'"`;
  (b) 换成**带上下文的量**: `git show <c>^:…/aether.py | grep -A1 'if not runs:' | grep -q 'return "pending"'`;
  (c) 退而求其次: 断言 **count == 2** (基线值) 而非「命中」。
  另请在同处钉死「`<TASK-003 commit>` 如何识别」(建议: commit message 含 `TASK-003` 且 `--stat` 含
  `ci_backends/aether.py`), 否则「哪个是那个 commit」本身就是分叉点。

---

### [A1-PP3-M3] 类级: 16 条 SC 里恰有两条 (**SC-14 / SC-15**) 的「基线必红」在 v3 的编码下**观测不到** —— 一条因任务位移, 一条因回退手段对子模块无效

proposal Success Criteria 段的契约是「红窗 = 基线 `400f0bc` 必红; 每条能答『它怎么会红』」。我按这条对
16 条 SC 逐条查了承载任务的落点顺序与回退手段, **恰好两条不满足**:

**(a) SC-14 — 断言脚本写在它所断言的改动之后 (INV-2 反序)**

- **锚点**: `TASK-010.exec_order: 12` (改 config.template / .gitignore / workflow-runner 文档) →
  `TASK-011.exec_order: 13` (改 SKILL.md / traps / DEC / `path_coverage.py:36`) →
  `TASK-013.exec_order: 15` deliverables 才产出 `tests/test_doc_sync_no_run.py` (SC-14 grep 断言)
- **问题**: 这正是 R1-A1-M4 让 TASK-004 从 exec 4 前移到 exec 3 所要根治的形状 —— **守卫落在被守护的变更
  之后 = 自证快照**。写脚本的人读到的是**已经改好的**文档, 断言会长成「文档现在写了什么」而不是「proposal §5
  那张 20 行表要求写什么」(memory `test_asserts_what_its_name_claims`)。`TASK-013.verification` 里也没有
  任何一句要求它红过。`INV-2` 自己的措辞 (「测试先落且对基线 RED」) 在这一对上被违反。
- 附注: v2 里这脚本还只是 `TASK-011.verification` 的一句话 (exec 13); v3 为闭我的 m6 把它升成 deliverable,
  顺带**推后了两格** —— 修复自身把红窗推得更远。

**(b) SC-15 — 「回退本 spec 代码 (git stash) 后测试转红」用的手段够不着代码所在的仓**

- **锚点**: `TASK-012.verification[0]`「回退本 spec 代码 (**git stash**) 后 `test_case_in_unit_tests`
  指向的测试转红」
- **问题 (决定性的一半)**: 该测试与被回退的代码都在 **aria 子模块**里。主仓根的 `git stash` 默认**不递归
  子模块** (需 `--recurse-submodules` / `submodule.recurse`), 对 `aria/skills/phase-c-integrator/**`
  的工作树改动**零作用** ⇒ 测试不会转红 ⇒ 这条验收按字面执行必然失败。
- **问题 (叠加的一半)**: 即便在子模块内跑 `git -C aria stash`, 到 TASK-012 (exec 14) 时 TASK-003 的改动
  **大概率已提交** —— INV-1 要求它是一个可被 `git show <TASK-003 commit>` 指名的 commit。stash 对已提交内容
  是 no-op。cwd (主仓根 / 子模块) × 提交时点 (已提交 / 未提交) 四种组合里**三种是 no-op**, 只有一种偶然可行。
- **建议** (合并修):
  1. SC-14: 把 `test_doc_sync_no_run.py` 从 TASK-013 拆出, 新建一个 qa-engineer 的 RED 任务放在
     **TASK-010 之前** (依赖 TASK-003, exec ≈ 11.5), 与 004/002/005/008 同形; 或**最小改动**版 ——
     在 `TASK-013.verification` 加一条「脚本落地后, 先对 TASK-010/011 的文档改动做一次临时回退
     (`git -C aria stash push -- skills/` + 主仓 `git stash push -- .aria docs/`) 跑一次**必红**, 再还原」。
  2. SC-15: 把 `git stash` 换成对**基线树**求值 —— `git -C aria worktree add /tmp/base 9e6a17c` 后在
     基线树跑那条用例 (或 `git -C aria checkout 9e6a17c -- skills/phase-c-integrator/scripts/` → 跑 → 还原),
     并在 verification 里点明「代码在子模块, 主仓 stash 不递归」这条陷阱。
  3. 类级 (memory `fix-the-class`): 落完后对 **16 条 SC 逐条**问一遍「它的承载任务真能观测到那次红吗」——
     我这轮查下来其余 14 条都满足 (见「已核验无误」#7), 但这个 sweep 应该写进 v4 的自检而不是靠审计席复现。

---

### [A1-PP3-m1] `TASK-016` 的归档门 warn 预告已被同一轮的另一条修复抵消, 现为假预期 (且它预先授权了「不当失败处理」)

`TASK-016.verification[2]` 预告「归档门对本 yaml 会另产一条正交 `archive-safety-net` warn (标题含「调用」
类集成关键词的任务) — 属既有启发式 … 记 handoff **不当失败处理**」。**两态实测** (合成全 completed 目录跑
`spec_complete.py --gate`):

| 版本 | `unverified_claims` |
|---|---|
| v3 原文 | 只有 `runtime_probe:record` — **无** integration claim |
| 把「调用」塞回 TASK-005 title | `archive-safety-net-integration-claims-unverified` **立刻复现** |

机检 19 个 title 对 `spec_complete.py:320-327` 的七个关键词 (`集成(?!测试)`/`接线`/`wire`/`integration`/
`调用`/`registered`/`hook`) **零命中** —— R2 簇 #8 改掉 TASK-005 的「调用」之后, 簇 #7 的预告就过期了。
影响不大 (D.2 执行者会看到比预告更干净的输出), 但那句「记 handoff 不当失败处理」是**对一条尚未出现的
gate warn 的预先豁免**, 与 Rule #10 的方向相反。建议改成「预期 `unverified_claims` 仅 `runtime_probe:record`
一条 (活体后应为空); 若出现 `archive-safety-net-*` 属新情况, 上报不自行消解」。

### [A1-PP3-m2] 边补了, 散文没补: `parallel_tracks.note` 仍只讲「文件域 disjoint」

R2-M2 的处方两半 —— 补 `TASK-010 → TASK-003` 边 ✅ 已落; 「note 里记一句两轨在 TASK-010 处有**验证面**
耦合 (`config-template-key-currency` 断言 模板键 ⊆ `DEFAULT_CONFIG`)」未落。`note` 现文仍是「两轨文件域
disjoint, 可并行」。按边调度的执行者没事; 按 note 调度的 (它就写在 `parallel_tracks` 里) 会以为 helper 轨
可以整轨先跑完。一句话的事。

### [A1-PP3-m3] `TASK-013` 是 main-loop 任务却挂着一个测试文件交付物, `reason` 自陈「由 qa 子 agent 写」

`agent: main-loop` + `deliverables[1] = tests/test_doc_sync_no_run.py` + `reason` 里「SC-14 脚本由 qa 子
agent 写 (测试任务)」= 一个任务两个执行者, `agent_summary` 只记 main-loop。这是 v3 为闭我 m6 的「km 写测试
越界」而做的折中, 但把越界换成了口径外的隐式转派。若按 M3(a) 把脚本拆成独立 qa 任务, 这条自然消失。

### [A1-PP3-m4] `INV-6` 的「§7 四项不得蒸发」没带 false 分支的例外句

动作面已经有了 (`TASK-016.conditional_parts` 写明 false ⇒ §7 checklist 1 标 N/A), 但 `INV-6.rule` 本身仍是
无条件全称句 (「§7 checklist 4 项各挂到具体 task 的 notes, **不得蒸发**」), 而 `checklist_s7_mapping.1`
指向的 `TASK-007b.verification` 在 false 分支整任务 N/A。不变量文本与它自己的例外不同步, 补半句即可。

### [A1-PP3-m5] `TASK-006.conditional_parts` 的 false 分支 (不引入 `.replace`) 全文无任何核验

`TASK-013` 的负控只 grep `dispatches`, 抓不到残留的 `.replace("<pr_branch>", …)`。实质无害 (无占位符时
`.replace` 是 no-op, R2 A2 已实证), 但这是 `conditional_parts` 四处里唯一一处**声称了条件行为却无人守**的。
可在 M1 的负控里顺手加一句 `grep -c '<pr_branch>' scripts/pre_merge_gate.py == 0`。

### [A1-PP3-m6] `execution_order` 的「TASK-012 ∥ TASK-013」与 TASK-012 的工作树回退动作互斥

TASK-012 要做全树回退 (M3(b) 修完后是 worktree/checkout), TASK-013 要跑全量 pytest —— 真并行会互相污染。
实际无害 (两者同为 main-loop, 单线程串行), 但既然 M3(b) 会把回退手段改得更重, 建议把 `∥` 改成
「TASK-013 → TASK-012 (回退动作独占工作树)」。

---

## 已核验无误 (实测; 按 memory `predict-then-measure` 先写预期再跑)

1. **三项机检不变量全部成立** (逐字实现 `exec_order_note` 的断言): 19 任务 `exec_order` = {0,…,18} 无重
   无缺; 「每任务 exec_order > 其所有依赖」**violation = 0**; 「TASK-003 ∈ 005/006/007a/007b/010/011/012/
   013/014/015/016 依赖闭包」**11/11 为真**; 附带 002/004 也在全部 11 个闭包内; DFS 无环。
2. **三处顺序面三方一致** (我 R2 Verdict 点名的判别式 (ii)): `exec_order` 数字序 == `execution_order`
   四行叙述 == `parallel_tracks` 两轨内部序, 逐任务比对无出入。
3. **算术自洽**: 19 = `total_tasks`; 逐项 `estimated_hours` 求和 = **49.5** = metadata; parent 集合
   {P0..P7} = 8 = `parent_task_count`; `estimation_note` 的「19 个里 14 个 <4h」实数 = 14; 四组配对
   (002+003=7 / 005+006=6 / 007a+007b=4 / 008+009=9) 全部对得上; `agent_summary` 四个 agent 的任务集合
   与逐任务 `agent:` 字段**集合相等** (qa 5 / be 4 / km 2 / main-loop 8 = 19)。
4. **机读面未被 v3 新字段搞坏**: `lib/detailed_tasks.parse_detailed_tasks` 实跑 → `parse_ok=True,
   "19 task(s) parsed"`, 19 个 id/status 全对 —— 含新 id **`TASK-000b`** (非纯数字后缀) 与四处新
   `conditional_parts` 长串; 合成全 completed 目录跑 `spec_complete.py` → `complete: true (19 task(s),
   无 carry-forward/defer 注释)`, `d_payload.deferred_items = []`。
5. **代码锚点抽样逐字命中** (aria @ 9e6a17c): `aether.py:225-226` = `if not runs: return "pending"` ✅;
   `:218` 即该 docstring 首行 ✅; `DEFAULT_CONFIG` 在 `:57-69` 且现无 `no_run_prompt_after_observations` ✅;
   `test_pre_merge_gate.py:363` = `test_empty_runs_pending` 的断言行 ✅; `path_coverage.py:36` 逐字为
   「⇒ 终态 reason 封闭集共 **9** 个」(TASK-011 勘正 8 的对象存在) ✅; 全量实跑 **phase-c 119 passed /
   workflow-runner 22 passed** —— 与 SC-12 / TASK-013 title 的「119+N / 22+N」一致。
6. **TASK-015 的「14 个版本字符串点」逐点实核**: `CLAUDE.md:139` + `:141` / `VERSION:24` /
   `README.md:8` + `:242` / `README.{zh,ja,ko}.md` 各 3 (`:3` translated-from + `:10` badge +
   `:244` Plugin Version) = **1+2+2+9 = 14**, 与 title 数字与行号逐一吻合 (当前值全为 v1.66.4, 与
   `baseline_sha` 一致); aria 侧 5 点表述同 proposal §5。
7. **其余 14 条 SC 的红窗承载都在正确的一侧** (M3 的 sweep 结果): SC-1..4 (TASK-002 RED 在 003 前) /
   SC-5·SC-10 (005 在 006 前) / SC-8·SC-9 (007a 在 007b 前) / SC-11 (008 在 009 前) 四对均「测试先落 +
   verification 明写基线红」; SC-6/SC-7 是 GUARD 且带坏实现对照 (mutation 必红); SC-12 无红窗概念;
   SC-13/SC-16 由 TASK-014 两态断言。
8. **SC-16 (b) 的红窗不会被 TASK-009 的测试写入毁掉** (我先预测「probe 只计 production, 故 (b) 仍 warn」
   再实读): `lib/runtime_probe.py` docstring + 实现明确「only `source == "production"` records count」,
   `symbol` 只是消息标签不过滤记录 ⇒ TASK-009 verification 里那次 `--source test` 写入既不污染分区语义,
   也不会让 (b) 提前变 pass。合成目录实跑 `--gate` → `runtime_probe: {outcome: "warn", count: 0}` +
   `unverified_claims` 含 `runtime_probe:record` ⇒ (b) 的机读断言可执行。
9. **INV-3 的 proposal §3.5 十项在 v3 仍 10/10 有承载**, 且新增了归档件自删那条 (TASK-016);
   `readiness_rule` 使 `completed + 'N/A —'` 视为已满足, false 分支下 011/013 对 007b 的边不停摆;
   全文 `skipped` 只剩 `readiness_rule` 里的禁令本身。
10. **`test_spec_complete.py:94-104` 的 `parents[4]` + `SkipTest` 先例属实** (TASK-011 verification 引它
    为主仓文件断言的写法依据): 实读该文件, `_ARIA_META_ROOT = Path(__file__).resolve().parents[4]`,
    `_require_meta_archive()` 在目录不存在时 `raise unittest.SkipTest` —— standalone aria-plugin 下 skip 不红,
    引用准确。
11. **`audit_checkpoints_note` 仍属实**: `.aria/config.json` 的 mid_implementation / post_implementation /
    pre_merge / post_closure 四个确为 `off`, post_planning 为 convergence ⇒ 不排 B/C/D 审计任务是 Rule #10
    白名单第一类。
12. **三写者对 traps §六 的顺序无环且互相点名**: TASK-001 建节 (exec 2) → TASK-011 在其上方插四行
    (exec 13, 明写「不动 TASK-0a 行」) → TASK-014 末尾追加 SC-13 证据行并终改 SKILL.md `:241` 计数
    (exec 16, 口径「证据行不计入 N 条坑」)。

---

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 3 Major / 6 Minor) — **vote: REVISE**

R1 1C/7M → R2 0C/3M → R3 0C/3M。**Major 持平**, 而且这三条的来源分布比数字本身更值得看:
**三条全部落在 v3 的修复上, 其中两条 (M1 / M2) 直接长在我 R2 那两条 minor 的处方里** —— 负控被落成了
恒红的量, 语义谓词被落成了不判别的 grep。这已经是连续第三轮同一形状 (R2 我报的三条 Major 里也有两条是
v2 修复自身造成的), 命中 memory `stop_adding_rounds_when_major_count_flattens` 的判据: **major 数不再降 =
每轮 fix 在引入约等量同形状缺陷**, 该换手段而不是加轮。

具体地, 建议 v4 之后**不要再靠阅读判断**这一类, 改用两条可机械执行的收口 (成本都在分钟级):

1. **每条 verification 命令逐字实跑一次** (在基线树上), 记录返回值 —— M1 (grep 返 1 不是 0)、
   M2 (`grep -c` 返 2 不是 0/1 二态)、M3(b) (`git stash` 对子模块无输出) 三条**全都会在第一次实跑时暴露**。
   这轮我抓到它们靠的就是这一件事, 不是更聪明的阅读。
2. **对 16 条 SC 跑一遍「红窗可观测吗」sweep** (承载任务的落点在被断言的变更之前吗 / 回退手段够得着代码
   所在的仓吗), 结果写进 yaml 的一个 note, 让下一轮可复核而不必重算。

v3 的结构层 (拓扑、闭包、算术、机读、条件 scope 十项、版本点 14 个) 我这轮**全部实测通过**, 没有一条
需要返工; 三条 Major 都只动 `verification` 字段的量或一个任务的位置, 不触任何任务的 title/deliverables/
依赖结构。落完这三条 + 六条 minor 后即可进 B.1, 我不建议再排第四轮全席审计。
