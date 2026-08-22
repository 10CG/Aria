---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-22T13:15:06.932Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 1
major_count: 7
minor_count: 7
---

# post_planning R1 — A1 席 (tech-lead) · pre-merge-gate-no-run-for-branch

## 摘要

透镜 = 不变量编码 / 依赖 DAG / 分轨 / 流程契约。总体判断: **DAG 结构本身健康** (无环、17 任务、49h 与
metadata 自洽、两轨文件域实测 disjoint、SC 全覆盖、checklist 4 项真落地), 但**条件分支
(`dispatch_viable=false`) 的执行与收口契约是整份文件最薄的一段** —— INV-3 的 `encoded_as` 只钉了
TASK-007 一个任务, 而它的 rule 文本自己列出的落点跨 3 个任务; 它处方的 `status: skipped` 既不在
task-planner SOT 的 status 枚举内, 也不在 state-scanner 的 done-family 白名单内 (实跑证实产出假残留)。

其次是三处**不变量维度/时序错配**: INV-1 的机械检查是无向共现 (对时序错误免疫)、SC-6/SC-7 守卫排在它
要守的变更之后、TASK-007 把 RED 与 GREEN 合进一个任务一个 agent。最后是一处**交付面缺口**: 4 类主仓
改动没有任何任务承载提交/推送。

本席对 yaml 做了机械实跑 (state-scanner parser / spec_complete gate / identity / 测试计数 /
custom checks), 结论以实测为准而非阅读推断; 详见「已核验无误」。

---

## Findings

### [A1-PP-C1] INV-3 处方的 `status: skipped` 落在 done-family 白名单外 —— false 分支归档产出假残留, 且全程无收口步骤

- **锚点**: `metadata.invariants[].id=INV-3` (rule 文本 `标 status: skipped + 理由`) · `TASK-007.conditional_on`
  (`false ⇒ status: skipped, 整组不做, INV-3`) · `TASK-016` (Phase D 归档) · `sc_coverage_crosscheck`
- **问题**: `skipped` 不是本项目工具链认得的终态。两条独立证据:
  1. **schema SOT**: `aria/skills/task-planner/DUAL_LAYER_SPEC.md:165` 字段表 —
     `status | ✅ | enum | pending / in_progress / completed / blocked`。`skipped` 不在枚举内。
  2. **归档门**: `aria/skills/state-scanner/scripts/lib/detailed_tasks.py:83`
     `_DONE_FAMILY = frozenset({"done", "completed"})` (注释自陈 fail-CLOSED 白名单),
     `spec_complete.py:215` `non_done = [t for t in tasks if not is_done_status(...)]`。
- **实测** (把本 yaml 复制到 scratchpad, 全部 status→completed 后再单独把 TASK-007 改为 skipped,
  跑 `python3 lib/spec_complete.py <dir>` 与 `--gate`):

  | 变体 | `complete` | 说明 |
  |---|---|---|
  | 17/17 completed | `true` | `"全 done (17 task(s), 无 carry-forward/defer 注释)"` |
  | TASK-007 = `skipped` | **`false`** | `"has 1/17 non-done task(s)"`; `--gate` 同时产出 `d_payload.deferred_items[0] = {parent_id: TASK-007, reason: "status=skipped"}` |

  `--gate` 的 `verdict` 仍是 `warn`/exit 0 (fail-toward-warn 不硬阻断), 但归档记录会带一条**语义错误的
  carry-forward**: 一个按 spec §3.5 主动裁掉的 scope 被登记成「未完成的残留工作」, 并进 archive-tracker。
- **同仓先例已解过同题**: `openspec/archive/2026-08-22-phase-c-integrator-ci-path-coverage/detailed-tasks.yaml`
  TASK-014 `gate_condition` 明文 ——「置 `blocked` 并**由 owner** 在 Phase D 归档前改为 `completed` +
  N/A 备注」, 并附「**不得**通过删弱 AC 让套件变绿 (Rule #10 反模式)」。本 yaml 没有等价收口条款。
- **建议**: 二选一, 写进 INV-3 的 `encoded_as` 与 TASK-016 的 deliverables:
  (A) 直接把 false 分支的终态定为 `status: completed` + `notes: "N/A — TASK-001 dispatch_viable=false,
  §3.5 条件 scope 组整组不做"` (SOT 枚举内, 归档门绿, 语义靠 notes 承载); 或
  (B) 保留过渡态 `blocked`, 并在 TASK-016 增一条显式收口步骤「归档前把 TASK-007 改 `completed` +
  N/A 备注」——但 `blocked` 同样非 done-family, 收口步骤漏做即复发, 且该收口按先例属 **owner 触点**。
  推荐 (A) (无中间态、无收口窗口)。⚠️ 无论选哪个, 都**不要**保留 `skipped`。

---

### [A1-PP-M1] 条件任务的下游就绪性规则缺失 —— TASK-011 / TASK-013 依赖一个会被跳过的任务, 执行者三向分叉

- **锚点**: `TASK-007.conditional_on` · `TASK-011.dependencies: [TASK-006, TASK-007]` ·
  `TASK-013.dependencies: [TASK-003, TASK-006, TASK-007, TASK-009]`
- **问题**: yaml 定义了「TASK-007 可能不执行」, 但**没有定义它不执行时下游怎么算就绪**。
  按字面 `dependencies` 判就绪的执行者会看到 TASK-011/TASK-013 卡在一个永不进 done-family 的前置上
  (C1 已证 `skipped` 非 done-family), 于是 SC-14 (TASK-011) 与 SC-12 (TASK-013) 的承载连带停摆,
  再连带 TASK-012 → TASK-015 → TASK-016 整条尾巴。三种执行者行为都真实存在:
  (i) 严守图 ⇒ 停摆; (ii) 自行跳过 ⇒ 正是 Rule #10 反模式 (无成文 lane 的 AI 流程裁量);
  (iii) 把 TASK-007 硬标 completed 应付 ⇒ 记录失真。
- **先例**: 同一形状在 2026-08-22 archive 的 post_planning 里被 R4 (cr-F1) / R5 (tl#1) / R6 (qa-R6-C)
  连抓三轮, 最终写法是**把就绪性判定规则写成文**: 「字面 `dependencies:` 字段不移除 …… 本规则只在
  证否分支的就绪性评估中应用」+ 明确替代前置。本 yaml 只有结论 (`整组不做`) 没有规则。
- **建议**: 在 INV-3 `encoded_as` 或 `parallel_tracks` 旁加一条判定规则, 例如:
  「TASK-007 处于 skipped/N-A 终态时, 其在 `dependencies` 中**视为已满足** (字面字段不移除);
  TASK-011 / TASK-013 的就绪性改判为其余前置全部 done」。同时 TASK-011 / TASK-013 的
  `verification` 各补一句 false 分支下的期望 (TASK-013: 测试计数不含 SC-8/SC-9 新增)。

---

### [A1-PP-M2] INV-3 的 `encoded_as`「其余任务无条件」与它自己的 rule 文本互斥 —— 条件组两个落点没有承载

- **锚点**: `INV-3.rule` (列出 `…… + DISPATCH_VIABLE 常量 + §2.1 .replace + 3.3 (a) 行整组不做`)
  vs `INV-3.encoded_as` (`TASK-007.conditional_on = TASK-001.dispatch_viable; 其余任务无条件`)
- **问题**: rule 列的落点跨三个任务, encoded_as 只钉一个, 并**主动声明其余任务无条件**:

  | §3.5 条件组成员 | 实际归属任务 | yaml 的处置 |
  |---|---|---|
  | §4 path_coverage / SC-8 / SC-9 dispatchable / `DISPATCH_VIABLE` / 2.3 渲染句 / SC-2 子项 / SC-5 (c2) | TASK-007 | ✅ `conditional_on` |
  | §2.1 末段 `<pr_branch>` 的 `.replace` | **TASK-006** | ⚠️ 只有 `notes_scope` 一句文字裁定, **无 `conditional_on`, 且无依赖边到 TASK-001** |
  | 3.3 (a) 处方行 (`§C.2.4 步骤 6` 处方段) | **TASK-011** | ❌ **零处置、零提及** |

- **实测**: TASK-011 的 title 覆盖 `:252-263 步骤 4·5·6 surface 义务+处方段`, deliverables 含
  `phase-c-integrator/SKILL.md`; 全任务体 (title/deliverables/verification/notes) grep 无
  `dispatch` / `dispatch_viable` / `条件` 字样。⇒ 按 yaml 字面执行, false 分支下 knowledge-manager
  会把 3.3 (a) 行原样写进 SKILL.md, 而 gate 永远不渲染 dispatch 行 ⇒ 一条**零消费方的处方文本**,
  与 proposal §3.5「不留零消费方字段/常量, R4 A1-m6」直接冲突。
- 另一半 (TASK-006): `notes_scope` 的裁定内容是对的, 但它**不是 schema 字段**、不被任何 verification
  检查, 且 TASK-006 `dependencies: [TASK-005]` 里没有 TASK-001 —— 一个任务的**交付内容取决于另一个
  任务的产出却无边**, 只靠 `exec_order 1 < 6` 的巧合成立。
- **建议**: (a) TASK-011 加 `conditional_scope:` 一行, 点名「false 时 §C.2.4 步骤 6 处方段不含 (a) 行,
  且 (b) 行的『改分支名或走 (a)/(c)』改写为『改分支名或 (c)』」, 并在 `verification` 加一条可 grep 的
  负控 (`false 分支: SKILL.md 步骤 6 处方段不含 "dispatches"`); (b) TASK-006 把 `notes_scope` 升为
  `conditional_scope`, `dependencies` 补 TASK-001; (c) INV-3 的 `encoded_as` 删掉「其余任务无条件」,
  改列三个落点的承载任务。

---

### [A1-PP-M3] INV-1 的机械检查维度不匹配错误的维度 (无向共现 vs 时序), 且检查被派给一个不提交的 agent

- **锚点**: `INV-1.encoded_as` (`…… B.2 commit 粒度检查`) · `TASK-003.verification[1]`
  (`git show --stat 该 commit 同时含 aether.py 与 pre_merge_gate.py (INV-1)`) ·
  `parallel_tracks.note` (`子 agent 不 commit, 主控统一提交; TASK-003 的 INV-1 同 commit 由主控保证`)
- **问题 (维度)**: INV-1 要防的错误是**时序性**的 ——「存在一个只含 §1 的 commit」。
  `git show --stat <一个 commit>` 是**无向共现**检查: 序列 `commit1 = aether.py only` →
  `commit2 = pre_merge_gate.py (+aether.py docstring)` 下, 对 commit2 跑该检查**全绿**, 而 commit1
  正是 INV-1 点名的 fail-open 中间态 (实测确认前提成立: 9e6a17c 上 `compute_verdict([], "not_found")`
  走 `else` 分支返 `VERDICT_GREEN`, `pre_merge_gate.py:229-233`)。这正是
  memory `invariant_dimension_must_match_error_dimension` 的形状 (无向检查对方向性/时序错误免疫)。
- **问题 (归属)**: 该 verification 挂在 `agent: backend-architect` 的任务上, 而 `parallel_tracks.note`
  明文子 agent 不 commit。执行时验证者手上根本没有 commit 可 `git show` —— 检查与执行者错位,
  最可能的结果是这条 verification 被静默略过 (`delegate-verify` 形状: 写「由主控保证」但没去主控那侧
  钉一个会发红的动作)。
- **建议**: 把检查换成方向敏感且可在主控侧跑的断言, 例如
  `git log --format=%H <base>..HEAD -- .../ci_backends/aether.py` 得到的**每一个** commit 都必须同时
  出现在 `git log --format=%H <base>..HEAD -- .../pre_merge_gate.py` 里 (等价: 触 aether.py 的
  commit 集 ⊆ 触 pre_merge_gate.py 的 commit 集); 并把它挂到主控侧 (TASK-013 或 TASK-015 的
  verification), TASK-003 只保留「交付物同时含两文件」。

---

### [A1-PP-M4] SC-6/SC-7 守卫排在它要守的变更之后, 且 SC-7 没有「拒绝能力」证明 —— 快照恒绿风险

- **锚点**: `TASK-004.dependencies: [TASK-003]` · `TASK-004.verification` (`基线绿; SC-6 对 mutation
  (短路漏 return) 实跑红`) · `INV-2.rule` (`测试先落且对基线 …… GREEN (守卫, 且已证明对坏实现会红)`)
- **问题**:
  1. **时序**: 守卫的价值来自「在被守护的代码变更之前就固化住契约」。TASK-004 依赖 TASK-003,
     意味着 qa-engineer 面对的是**已改过的 compute_verdict/`_build_output` 调用面**去写「基线快照」。
     `基线绿` 里的「基线」没有钉 SHA ⇒ 极易退化成「对当前树取快照再断言等于自己」= 恒真
     (memory `false_green_dual_is_permanent_red` / `predict_before_measure_for_self_check`)。
  2. **拒绝能力**: SC-6 有 mutation 对照 (短路漏 `return` 必红) ✅; **SC-7 没有任何坏实现对照**,
     它只有「八变体键集快照」。按 memory `verify_assertions_reject_bad_implementations`, 一条不证明
     自己会拒绝坏实现的快照测试, 与恒绿无法区分。
  3. 两个守卫在基线上**已经可写**: 实测六个早退点 (`_build_output` 调用 @ `:363 :376 :419 :436
     :465 :490 :513`) 与 `not_applicable` 短路 (`:498-506`) 在 9e6a17c 上全部存在, 不需要 TASK-003
     的任何产物。
- **建议**: `TASK-004.dependencies` 改 `[TASK-000]` (与 TASK-002 并列, 顺带多一条并行边);
  `verification` 把「基线绿」钉成「在 **9e6a17c** 上跑全绿」; SC-7 补一条 mutation 对照
  (例: 给某个早退点多塞一个键 / 少一个键 ⇒ 必红), 与 SC-6 对称。

---

### [A1-PP-M5] TASK-007 把 RED 测试与实现合并进单一任务、单一 agent —— INV-2 的配对在条件轨上失效

- **锚点**: `TASK-007` (`title: … SC-8/SC-9 RED→GREEN: …`, `agent: backend-architect`,
  `carries_sc: ["SC-8 RED", "SC-9 RED (…)", …]`, deliverables 同时含 `path_coverage.py`
  与 `tests/test_path_coverage.py`)
- **问题**: 其余四对都严格遵守「qa-engineer 写测试 → backend-architect 实现」
  (002→003 / 004 / 005→006 / 008→009), 唯独 TASK-007 由 backend-architect 同时写测试和实现。后果:
  1. **无红窗证据**: `carries_sc` 标 `SC-8 RED`, 但同一任务里 RED 立刻转 GREEN, 没有任何一个时点/
     交付物能证明 SC-8 在基线上真红 (proposal SC-8 基线判定 = 红)。verification 两条都只管绿侧
     (`SC-9 与基线逐字同` / `DISPATCH_VIABLE monkeypatch 负控能红`)。
  2. **同人写测同人实现**: memory `test_asserts_what_its_name_claims` 与 `spec_underdetermination`
     指向的正是这种自洽闭环 —— 断言容易被写成对已完成实现的描述。
  3. 与 INV-2 的 `encoded_as` (`dependencies + exec_order; carries_sc 标 RED/GUARD`) 自相矛盾:
     标签体系要求 RED 与 GREEN 分居两任务, 这里同居。
- **建议**: 拆成 TASK-007a (qa-engineer, SC-8/SC-9 RED + SC-2 dispatch 子项 + SC-5 (c2), 2h) →
  TASK-007b (backend-architect, 实现 + `DISPATCH_VIABLE`, 2h), 两者共享同一
  `conditional_on: TASK-001.dispatch_viable == true`; 4h 总额不变。

---

### [A1-PP-M6] `pre-merge-gate-empirical-traps.md §六` 有三个生产者、一处职责重叠、一条缺边

- **锚点**: `TASK-001.deliverables[1]` (traps §六 增 `dispatch_viable=<bool>` 行) ·
  `TASK-011.title` (`traps §六 (F3 / F4 / (b) 轴同形 / F6 404+basename / **TASK-0a 结果行**)`) ·
  `TASK-014.deliverables[0]` (traps §六 SC-13 证据行) · `TASK-011.dependencies: [TASK-006, TASK-007]`
- **问题**:
  1. **缺边**: TASK-011 与 TASK-001 交付物文件交集非空 (同一文件同一节), 但 TASK-011 的
     `dependencies` 里没有 TASK-001。按同仓先例钉死的机械核对法 ——「唯一可靠的机械核对是**逐
     deliverable 求同文件交集, 交集非空**⇒必须有边」(2026-08-22 archive, wave 备注) —— 这是缺边。
     现在只靠 `exec_order 1 < 11` 兜住, 而 exec_order 与 dependencies 在本文件里没有约束关系声明。
  2. **双写/职责重叠**: TASK-001 说自己写 `dispatch_viable=<bool>` 行, TASK-011 又说自己写
     「TASK-0a 结果行」—— 同一行两个生产者, 且执行者不同 (main-loop vs knowledge-manager 子 agent)。
     谁**创建** §六 这一节也没定 (TASK-001 早于 TASK-011, 但 TASK-001 的措辞是「§六 增…行」,
     隐含 §六 已存在 —— 实际 traps 现无 §六)。knowledge-manager 若按 title 重建整节, 会覆盖
     TASK-001 已写的证据行 (memory `rewrite_silently_discards_prior_fixes` 形状)。
  3. TASK-014 那侧有边 (`deps 含 TASK-011`) ✅, 且 `notes` 已处理日期字段一致性 ✅。
- **建议**: (a) `TASK-011.dependencies` 补 TASK-001; (b) 把 §六 的**建节权**明确给 TASK-001
  (「新建 §六 骨架 + 写入 TASK-0a 结果行」), TASK-011 改为「**追加** F3 / F4 / (b) 轴 / F6 四条,
  不重写 TASK-001 已写的结果行」, 并在 verification 加一句「§六 内 TASK-0a 结果行逐字保留」。

---

### [A1-PP-M7] 主仓 4 类交付物没有提交/推送承载, 且全程无主仓侧 B.1 分支

- **锚点**: `TASK-010.deliverables` (`主仓 .aria/config.template.json / .gitignore`) ·
  `TASK-011.deliverables` (`主仓 docs/decisions/DEC-20260731-001-*.md`) ·
  `TASK-012.deliverables` (`aria-plugin-benchmarks/ab-suite/… + ab-results/…`) ·
  `TASK-015.deliverables` (`aria master @ v1.66.5 (origin==github); 主仓 master gitlink + 14 点`) ·
  `TASK-016.deliverables` (handoff + archive)
- **实测**: `.gitmodules` 只声明 3 个子模块 (standards / aria / aria-orchestrator);
  `aria-plugin-benchmarks/` **无 `.git`** ⇒ 是主仓普通目录。故主仓侧改动共 5 类:
  ① `.aria/config.template.json` + `.gitignore` (TASK-010) ② `docs/decisions/DEC-…` (TASK-011)
  ③ `aria-plugin-benchmarks/ab-suite/` + `ab-results/` (TASK-012) ④ spec 目录本身 (Rule #5)
  ⑤ 版本串 14 点 + gitlink (TASK-015)。**TASK-015 的 deliverables 只覆盖 ⑤**, ①②③④ 无任何任务
  声明它们何时进 commit、进哪个分支、由谁推。
- **为什么这条会真出事**: memory `scoped_git_add_splits_claim_from_landing` 记录的两次实证之一,
  就是「AB fixture 从未提交却三处声称已做」—— 与本处 ③ 完全同形。同 memory 的处方
  (收尾跑不带路径的 `git status`) 在本 yaml 里也没有任何 verification 承载。
- **另一半 (B.1)**: 十步循环 B.1 = 分支创建。TASK-000 (`exec_phase: B.1-entry`) 只做 claim,
  TASK-001 (`B.1-前置`) 只做探针, 之后直接进 B.2。aria 子模块侧分支起点有交代
  (metadata `baseline_sha: 9e6a17c` + proposal「Phase B 在 9e6a17c 起分支」), **主仓侧连起点都没有** ——
  当前主仓在 `master`, 按 yaml 字面执行等于让子 agent 直接改主仓 master 工作树, 再由 TASK-015 推
  master。这触到 memory `sync_instruction_not_push_authorization` (推共享 master 需显式授权,
  「低风险 doc」不能自我授权)。
- **建议**: (a) TASK-000 的 deliverables 补两条分支创建 (aria 子模块 `feature/152-*` @ 9e6a17c +
  主仓同名分支), 或新增 TASK-000b; (b) TASK-015 的 deliverables 显式列全主仓 5 类交付物, 并加一条
  verification「在主仓根跑**不带路径**的 `git status --porcelain` 为空 (无未提交的 ①②③④)」;
  (c) 明确主仓落地路径 (feature 分支 + Forgejo PR merge —— 主仓是 CLAUDE.md 硬约束 1 的**例外**,
  可走服务端合并; 子模块那侧仍是本地 merge)。

---

### [A1-PP-m1] schema 偏离 `DUAL_LAYER_SPEC.md` 三处 (parent / estimated_hours / reason)

- `DUAL_LAYER_SPEC.md:96` 路径 B 输出明文 =「detailed-tasks.yaml (**无 parent 字段**)」, 且 `:176`
  parent 格式规则 = `^\d+\.\d+$`。本文件 `datasource: "proposal.md"  # 路径 B` 却给每个任务
  `parent: "P0".."P7"` —— 既是路径 B 不该有的字段, 值也不符格式。同仓先例的 `schema_note` 专门写过
  「`parent` 按 SOT 路径 B 规定省略」。
- `DUAL_LAYER_SPEC.md:166` `estimated_hours | ✅ | string | 工时范围 (如 "2-4")`; 本文件用
  int/float (`0.5` / `3` / `4`)。先例用 `"1-3"` 字符串 + `estimation_note` 声明锚点。
- `DUAL_LAYER_SPEC.md:170` `reason | ⚠️ | string | Agent 分配理由 (A.3 阶段)` —— 本文件**零任务**
  带 `reason`, 而 metadata 自称 `planned_by: "task-planner (A.2+A.3)"`。A.3 的产出只剩 `agent:` 一个值,
  分配理据不可复核。
- **建议**: 删 `parent` 改用注释分组 (`# ══ P0 ══` 已在); 或若要保留分组语义, 换个不撞 SOT 的键名
  (如 `group:`)。`estimated_hours` 与 `reason` 按 SOT 补齐, 或在 metadata 加 `schema_note` 声明偏离理由。

### [A1-PP-m2] 任务粒度普遍低于 CLAUDE.md 的 4-8h 约定且未声明

17 任务中 **10 个 < 4h** (0.5 / 1 / 1.5 / 2×3 / 3×4), 均值 2.9h。CLAUDE.md 协作原则明文
「小步迭代 (任务 4-8h 粒度)」。细粒度在此处是**有理由的** (TDD 红绿对必须可独立观测, 见 M5 的相反方向),
但理由没写下来 ⇒ 下一份 spec 无法判断这是范式还是疏漏。先例用 `metadata.estimation_note`
(`S≈3h / M≈6h / L≈10h; canonical effort 轴为 token`) + `tdd_note` 显式声明。建议照抄这两个 note。

### [A1-PP-m3] `exec_order` 与 `parallel_tracks` 存在互斥读法

helper 轨 (TASK-008 / 009) 拿到 `exec_order` 8 / 9, 排在 gate 轨 (2-7) **之后**, 而
`parallel_tracks` 说两轨可并行。两者都合法但语义冲突: 严格按 exec_order 调度 ⇒ 并行性归零
(helper 轨的真实前置只有 TASK-000, `dependencies` 已正确写明)。文件里没有一句说明
`exec_order` 是 advisory tie-break 而非硬序。建议加一行 `order_note`, 或把 helper 轨的
exec_order 改成与 gate 轨交错的值 (如 2.5 / 3.5) 让并行结构在数字上可见。

### [A1-PP-m4] TASK-002 deliverable 引入了一个可实测消除的未决歧义

`TASK-002.deliverables[1]` = `tests/test_ci_backends.py (**若 :363 所在类在此**)`。
**实测**: `grep -rn "_normalize_pr_ci_status" skills/phase-c-integrator/tests/` 命中 6 处,
**全部**在 `test_pre_merge_gate.py` (`:348 :352 :356 :359 :360 :363`), `:363` =
`test_empty_runs_pending` 的 `assertEqual(..., "pending")`; `test_ci_backends.py` 零命中。
proposal §1 末行也已明说「基线 `test_pre_merge_gate.py:363`」。派生层的这个「若」是新引入的,
建议删掉第二条 deliverable。

### [A1-PP-m5] TASK-015 的硬约束 2 落实不完整 (只断言 origin / 无 ls-remote 重试)

`TASK-015.verification` 写「merge 前断言 local master == origin/master (stale-local-main)」——
只覆盖 origin, 未含 github。镜像分叉是本项目 3 次复发的事故形状
(memory `mirror_sync_needs_mechanical_backstop` / `partial_push_creates_mirror_divergence`),
merge 基线判定应对**两个** remote 各取一次 ls-remote 后再下结论。另 CLAUDE.md 硬约束 2 明文
「ls-remote 自身失败 → 重试几次再下结论」, verification 未写。建议把断言改成
「fetch 双 remote → `git ls-remote origin master` 与 `git ls-remote github master` 与 local
三者一致 (任一 ls-remote 失败重试 ≥3 次)」, 推后同法各跑一次。

### [A1-PP-m6] B/C/D 侧 audit checkpoints 全 off 是正确的, 但缺 Rule #10 白名单留痕

**实测** `.aria/config.json`: `mid_implementation / post_implementation / pre_merge / post_closure`
四个 checkpoint **均为 `off`** ⇒ 计划里不排审计任务**完全正确** (Rule #10 白名单第一类)。
但 yaml 没有像 proposal 对 post_brainstorm 那样留一句声明。后果: 读者 (含未来的 R2 审计席与
无人值守 Layer 2) 无法区分「config 显式 off」与「计划漏排」, 而 Rule #10 的判据恰恰要求这个区分可查。
建议在 `metadata.a2_entry` 旁加一行
`audit_checkpoints_note: "mid_implementation/post_implementation/pre_merge/post_closure = off (.aria/config.json, Rule #10 白名单第一类) ⇒ B/C/D 无审计任务"`。

### [A1-PP-m7] `runtime_probe` 的 14 天时窗跨 TASK-014→TASK-016 无人看管

proposal frontmatter `max_age_days: 14`, 探针核验「近 14d 有 `source=production` 记录」。
production 记录由 **TASK-014** 产生, 归档门在 **TASK-016** 评估, 中间隔着 TASK-015 (ship, 含双推 +
主仓同步面 + 可能的 owner 触点)。若这段跨 14 天, `runtime_probe.outcome` 回 `warn`, SC-16 (c)
的复核 (TASK-016 verification「gate JSON 显示 probe pass」) 直接失效, 且**重跑活体的成本是整个
TASK-014**。R-f 只提了探针实现缺陷风险, 没提时窗。建议 TASK-014 或 TASK-016 的 notes 加一句
「TASK-014 至归档须 ≤14d, 超期须重跑 SC-13 活体产生新 production 记录」。

---

## 已核验无误 (实测, 非阅读推断)

按 memory `predict_before_measure_for_self_check`: 下列各项先写下预期再实跑, 结果与预期一致。

1. **yaml 可被生产 parser 正确读取**: `state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks`
   实跑 → `parse_ok=True, "17 task(s) parsed"`, 17 个 id/status/title 全部正确抽出。
   **特别核查**: `metadata.invariants[].id = INV-1..7` 这 7 行 `- id:` **不会**被
   `_TASK_ID_LINE_RE` 误计 —— `_tasks_block_bounds` 先按 `_TOP_KEY_RE` 把文本收窄到 `tasks:` 块,
   INV 条目在 `metadata:` 内被排除; 块内 base-indent 直接项计数 == `- id:` 匹配数, 未触
   `structural self-inconsistency`。(这正是 2026-08-22 archive R4 cr-F4 记录的 footgun, 本文件未复发。)
2. **DAG 结构**: 无环; 16 条 dependency 边的前置 `exec_order` 全部 < 本任务; TASK-012 / 013 / 014 /
   015 / 016 对实现层任务的依赖经**传递闭包**全部覆盖 (TASK-014 未直连 TASK-003/006, 但经
   TASK-011→006→005→004→003 可达)。`sc_coverage_crosscheck` 16 条 SC 全部有承载任务。
3. **两轨文件域实测 disjoint**: gate 轨 = {`test_pre_merge_gate.py`, `test_ci_backends.py`,
   `aether.py`, `pre_merge_gate.py`, `path_coverage.py`, `test_path_coverage.py`};
   helper 轨 = {`test_gate_state_helper.py`, `gate_state_helper.py`}; 交集 = ∅。
   `parallel_tracks.note` 引 memory `workflow-file-domain` 与「子 agent 不 commit」的用法正确。
4. **算术自洽**: 17 任务 = `total_tasks`; 估时合计 **49.0h** = `estimated_hours`;
   P0-P7 八组 = `parent_task_count`。
5. **checklist_s7_mapping 4 项在目标任务实文可查** (逐条打开核对):
   1→`TASK-007.verification[1]` (裸全局 monkeypatch) ✅ / 2→`TASK-012.title` (两 skill 覆盖) ✅ /
   3→`TASK-014.notes` (traps 两处证据统一日期) ✅ / 4→`TASK-008.notes` + title (record 缺文件
   verdict≠wait exit 2 单测) ✅。无一蒸发。
6. **SC-16 的机读输入真实存在** (memory `verify_predicate_inputs_exist` 两层核: 逻辑对吗 +
   它要判的输入真会被生成吗): `python3 lib/spec_complete.py --gate <spec_dir>` 实跑返回
   `runtime_probe: {"outcome": "warn", "count": 0, "reason": "production telemetry partition
   missing: .aria/gate-state-telemetry.jsonl", "symbol": "record", "ts": …}` +
   `unverified_claims` 含 `{"claim": "runtime_probe:record", …}`。⇒ SC-16 (b) 的红窗
   **确实可机读**, TASK-014 verification 的「机读 gate JSON」可执行。
7. **INV-1 的前提事实成立**: `pre_merge_gate.py:174-233` 实读 —— `compute_verdict([], "not_found")`
   不命中任何 `elif`, 落 `else` 返 `VERDICT_GREEN`; 且 `elif main_in_flight_runs:` 确在
   `elif pr_ci_status == "not_applicable":` **之后**, 故 SC-4「误序实现此条红」的推理成立,
   TASK-003 title 里的插入位置描述与代码一致。
8. **既有测试计数**: `pytest` 实跑 phase-c-integrator 三文件 = **119 passed**,
   workflow-runner = **22 passed** ⇒ SC-12 与 TASK-013 的「119+N / 22+N」基数准确。
9. **TASK-000 的 container id 准确**: `lib.identity.get_identity()` 实测返回
   `Identity(owner='simonfish', container_id='023236f2', session_id='s-3d51@1310')` ——
   与 deliverable 里的 `container 023236f2` 逐字一致 (不是抄来的旧值)。
10. **TASK-016 的 `release_gate claim 释放` 落位正确**: `release_gate.py` 真实存在
    (`state-scanner/scripts/release_gate.py`), 且 `state-scanner/SKILL.md:176` 明确它是
    acquire (phase1_gate, Phase B-entry) 的对偶, **由 phase-d-closer D.2b 调** —— 与 TASK-016
    的 exec_phase `D` 吻合。
11. **TASK-015 的两个数字准确**: `.aria/state-checks.yaml` 实测 **10 个 check 全部 enabled**
    (`enabled: false` 出现 0 次) ⇒「custom checks 10/10」正确; 主仓版本串行号实测
    `CLAUDE.md:139` / `:141` / `VERSION:24` / `README.md:8` / `:242` 五处全部命中且现值 v1.66.4
    ⇒ 「14 点」拆分 (2+1+2+9) 与 proposal §5 逐字一致。
12. **agent 分配符合 A.3 分工预期**: qa-engineer = 002/004/005/008/013 (纯测试);
    backend-architect = 003/006/007/009 (纯实现); knowledge-manager = 010/011 (纯文档);
    main-loop = 000/001/012/014/015/016 (认领/活体/AB/ship/Phase D)。无越界。
13. **CLAUDE.md 硬约束 1 在 TASK-015 被正确编码**: 「本地 `--no-ff` merge (禁 Forgejo 服务端合并)」
    对子模块 aria 的写法正确 (子模块无 PR ⇒ 不产生 orphaned gitlink 的那条路径), 且
    gitlink bump 排在双推核验**之后** —— 顺序与硬约束 1 的事故根因分析一致。

---

## Verdict

**FAIL** (1 Critical / 7 Major / 7 Minor) — **vote: REVISE**

C1 与 M1/M2 是同一个根: **条件分支 (`dispatch_viable=false`) 只被当成「TASK-007 不做」, 没被当成一个
需要完整执行契约的分支**。三者合起来在 false 分支上会同时产生: 归档假残留 (C1)、下游就绪性分叉 (M1)、
零消费方文档行 (M2)。这三条建议一并修, 不要逐条打补丁 —— 修法就是给 INV-3 补一段「false 分支执行契约」:
终态用 SOT 枚举内的值、下游就绪性判定规则写成文、三个落点各挂承载任务与负控。

M3/M4/M5 是**不变量维度与时序**的三处同形错配 (无向共现代替时序 / 守卫落在被守护变更之后 /
RED 与 GREEN 同居), 修法都很便宜, 但按 memory `fix_the_class_not_the_instance`, 建议在
`metadata` 加一条 `invariant_check_note`, 要求「每条 INV 的机械检查, 其维度须与它要防的错误维度相同
(时序错误不能用共现检查)」, 一次性覆盖三处。

M6/M7 是**交付面归属**问题 (同文件多生产者缺边 / 主仓交付物无提交承载), 与 memory
`scoped_git_add_splits_claim_from_landing` 同形, 属于「不修就会在 C 阶段发现东西没提交」的类别。

Minor 全部可在同一轮吸收, 其中 m1 (schema 偏离 SOT) 与 m6 (Rule #10 留痕) 成本近零、收益是让后续
审计席与无人值守 Layer 2 可复核, 建议不要留到下一轮。
