---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T09:40:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 2
minor_count: 3
---

## 摘要

R2 复核 v2 (R1-fix), 基线仍 aria @ `400f0bc`。实读代码 (`path_coverage.py` / `gate_state_helper.py` / `pre_merge_gate.py`)、实读 `test_gate_state_helper.py` 全文、实读 AB fixture 目录与 `phase-c-integrator-pre-merge-gate.json` 目录清单、并用 Forgejo API 拉取 aria-plugin#126/#127 原文核对先例引用。

**簇 #1/#10 (误升级有界性)**: 逐状态穷举 `no_run_observations`/`no_run_escalation_done` 在「归零后再次达阈」这条 R1 未覆盖的路径上的行为 —— 确认按 v2 的 first-match-wins 顺序 (2.5 要求 `not done`, 2.6 要求 `done AND obs>=threshold`), 归零重新计数后再次达阈**正确路由到 2.6 (交人) 而非 2.5 (再次自动处方)**。cluster #1 的核心 Critical 关切 (A1-C1) 判 **CLOSED**。cluster #10 (AD-4 阈值经验依据薄) 的「代价有界故阈值敏感度降」论证站得住, 但 SC-13 的 TASK-0 活体协议对「dispatch 2xx 但 600s 内从未出现 run」这一本 Lab 自陈的高发拥堵场景没有第三处置分支, 判 **PARTIAL**。

**簇 #9 (Rule #6 第三行)**: row 选择本身已修对 (第三行, 非零裁量第二行), fixture 计数 "7" 已勘正。但深挖三条义务的**落地完整性**发现两个未闭合的口子: (a) NEG-3 当年在同一个 catalog 文件 `phase-c-integrator-pre-merge-gate.json` 里同时获得了「独立 fixture json + `fixtures[]` 登记项 (含 `test_case_in_unit_tests`)」两件事, v2 只承诺前者, 没有把 NEG-4 登记进 catalog —— 没有登记就没有可指向的「断言」, `SC-15`「回退后转红」在这个层面无所指; (b) rule6_note 说「追加到 NEG-3 当时开的缺口 issue, 若无则新开」是没查证的猜测式措辞 —— 实查 aria-plugin#126 原文, 该缺口 issue **确凿存在且编号为 #127, 目前仍 open**, 其正文原话直接问「这类『AI 必须 surface 某事』的义务, 现有 AB 形态 (输入 fixture → 看输出) 是否是合适的验证载体」——这正是 SC-15 falsifiability 提法要回答却没有回答的问题。cluster #9 判 **PARTIAL**。

**独立新问题**: `path_coverage.py:20-33` docstring 明写规则 5「不产终态」, 因此终态只有 7 条规则 + `internal-error` = **8** 个 (与我 R1 grep `test_path_coverage.py` 得到的 8 个前缀一致); v2 §4 声称的「R1 A3-m1 勘正」写成「9 个 = 8 规则终态 + internal-error」——这个「勘正」换了措辞但仍得出错误的 "9", 且与同一 docstring 里「规则 5 不产终态」自相矛盾。该错误数字被 SC-2 与 SC-9 两条验收标准逐字继承 ("参数化全 9 reason"), R1 聚合表把这条 (A3-m1+A4-m1, 簇 #17) 标记「逐条吸收」, 经本轮复核**该标记不成立** —— 判 partial/未真闭合, 严重度因牵连两条 Success Criteria 的可执行性而升至 Major (R1 时判 Minor, 当时未追踪到它会被 SC-2/SC-9 逐字继承)。

0 Critical: 未发现新的 fail-open 路径; §1+§2 同 commit 硬约束、AD-2 wait 结论、cluster #1 的一次性守卫核验均成立。

## R1 处置核对

| 簇# | 状态 | 证据 |
|---|---|---|
| #1 (升级处方一次性守卫, 含 A3-M1) | **closed** | 状态机穷举: `mark_no_run_escalation_done` 后 `done=true` 跨 wait 写保持 (仅 `is_first` 时复位), 之后即便 `no_run_observations` 因某轮非 `no-run-for-branch` 而归零、再重新累积到阈值, `should_escalate_no_run`(2.5, 要求 `not done`) 恒假, 只有 2.6 (要求 `done AND obs>=threshold`) 会命中 → 交人, 不会二次自动 dispatch/commit。`write_gate_state` 整字典重建的实现模式下, 两新字段若被遗漏不写入会被 SC-11(a) 的三连 wait 断言直接钉红, 无静默丢字段风险。 |
| #9 (Rule #6 第三行, 含 A3-M2/A3-m2) | **partial** | row 选择 + fixture 计数「7」已修对 (CLOSED 部分)。但: (a) v2 「代码落点」与 §5 文档同步表均未把 `phase-c-integrator-pre-merge-gate.json` (catalog manifest) 列为改动点, NEG-4 不会像 NEG-3 一样获得 `fixtures[]` 登记项 + `test_case_in_unit_tests` 绑定, 也就没有一个可核验的「断言」去承接 SC-15 的「转红」; (b) `forgejo GET /repos/10CG/aria-plugin/issues/126` 原文第 3 条义务明写「套件缺口开 **#127**」, 该 issue 目前 **open**, 且正文明确留了「AB 输入-输出 fixture 这种形态是否是 AI-surface 类义务的合适验证载体」这个未决问题 —— v2 rule6_note 用「若无则新开」带过, 既没有确认 #127 存在也没有回应它提出的根本问题, SC-15 的可证伪性主张因此仍然悬空 (详见新 Findings A3-R2-M1)。 |
| #10 (AD-4 阈值 + SC-13 flaky, 含 A3-M3) | **partial** | 「代价有界降低阈值敏感度」的论证成立 (由 #1 的一次性守卫保证)。SC-13 的「轮询至非 not_found 或 600s」修复了 R1 指出的「立即重跑必 flaky」问题, 但 TASK-0 §3.4 的二分结果 (成功 / 失败∈{4xx, run 形态不同}) 没有覆盖「dispatch 返 2xx 且 600s 内从未出现 run」这一分支 —— 这不是刁钻边角: CLAUDE.md「项目状态」段自陈的 heavy 节点持续拥堵 + Luxeno 45-54s 延迟已是本项目常态, 该分支被真实撞到的概率不低, 撞到时 TASK-0 执行者无章可循 (详见新 Findings A3-R2-m1)。 |

## 新 Findings

### [A3-R2-M1] Major — SC-15 的可证伪性主张对 NEG-4 这类「AI 行为」fixture 缺落地路径; rule6_note 第三义务「套件缺口 issue」未核实即已存在的 #127, 且该 issue 已经问了 SC-15 假装已解决的问题

**锚点**: proposal.md `rule6_note` 第一条; SC-15; 「代码落点」行; §5 文档同步表; aria-plugin#126/#127 (Forgejo 实查)。

**问题**:

1. **catalog 登记缺失, SC-15「转红」无所指**。`aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate-fixtures/NEG-3-internal-error-surface.json` 不是孤立文件——它同时是 `phase-c-integrator-pre-merge-gate.json`(catalog manifest)`fixtures[]` 数组里的第 7 项, 该项显式携带 `"test_case_in_unit_tests": "test_path_coverage.InternalErrorReasonTests.test_internal_error_has_own_reason"`(实读该 json 确认)。这个字段才是「回退后转红」在 NEG-3 身上唯一有据可查的落点——NEG-3 自己的 `_consumed_by` 字段也明写「确定性侧由 [这条 pytest] 覆盖……本 fixture 覆盖的是 AI 的 surface 措辞行为——两者正交, 不互替」, 即: NEG-3 文件里的 `_target_behavior`/`_arm_expectations` 这套字段**本身不是可机械判红的断言**, 它是喂给 `/skill-creator` 做 with_skill/without_skill LLM 判优比较的 prompt 数据, 而真正机械可证伪的是 catalog 里绑定的那条 pytest。
   v2 proposal.md 的「代码落点」与 §5 文档同步表**只列了独立文件** `ab-suite/phase-c-integrator-pre-merge-gate-fixtures/NEG-4-no-run-for-branch.json`, 全文 grep 确认没有一处提到要同步编辑 `phase-c-integrator-pre-merge-gate.json`(catalog)——即不打算给 NEG-4 加 `fixtures[]` 条目, 更不会有 `test_case_in_unit_tests` 绑定。结果: NEG-4 会成为一个**孤儿文件**, 既不出现在 `/skill-creator` 会读取的 fixture 清单里 (无法被真正跑到), 也没有任何 pytest 断言与它绑定。SC-15 写「回退本 spec 后其对应断言转红」——但如果这个「断言」根本不存在 (无 catalog 项、无 `test_case_in_unit_tests`), 这句话就是一个悬空指称, 无法回答「它怎么会红」。

2. **rule6_note 第三义务未经核实, 且回避了已存在的根本疑问**。rule6_note 原文:「套件缺口 issue (追加到 NEG-3 当时开的缺口 issue, **若无则新开**)」——这个「若无则新开」暴露了起草时没有去查证 NEG-3 当时是否真的开过缺口 issue。本次 R2 用 `forgejo GET /repos/10CG/aria-plugin/issues/126` 实查, #126 正文第三条义务原话:「套件缺口开 **#127**」; 再拉 `#127`, 状态 **open**, 标题「phase-c-integrator AB 两套件均覆盖不到 C.2.4 的 D9 surface 措辞——该义务自 v1.65.0 起零 eval 覆盖」。#127 正文「本 issue 要的是什么」一节末尾原话:

   > 「更根本的: 这类『AI 必须 surface 某事』的义务, 现有 AB 形态 (输入 fixture → 看输出) 是否是合适的验证载体, 还是需要另一种 eval 形态。」

   这正是本席被指派要回答的问题 (「对一个 AI 行为 fixture 这如何可证伪」)——项目自己的 issue tracker 已经在 2026-08 之前把它列为**未决**根本问题, 而 v2 的应对方式是「再加一个同形态的 NEG-4」, 这是该模式的**第三次**重复 (NEG-3 是第二次「先加 fixture, 缺口 issue 留着」; 若 NEG-4 不动这个根本问题, 就是原地重复而非推进)。既没有点名 #127, 也没有安排一个动作 (哪怕只是在 #127 下追加评论说明 NEG-4 是该模式的又一实例, 供该 issue 的「维度盘点」用), §5 文档同步表里对「issue #152」有专门一行 (评论/收尾留言的具体动作), 对 #127 却什么都没有——第三条义务因此比第二条 (SC-15) 更弱, 连一个可检查的行动项都没留。

**影响**: 不影响 merge 安全性 (0 Critical 判断不变), 但直接削弱 SC-15 作为「可证伪性」验收标准的实际含金量, 且是本项目 Rule #6 非协商规则第三行落地方式上一个**可核实的、非猜测的**缺口——不是「拿不准该不该跑」, 是「该做的两件具体事 (catalog 登记 / 点名 #127) 都可以现在就查清楚, 但没有查」。

**建议**:
1. §5 文档同步表加一行: `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json` — `fixtures[]` 追加第 8 项 `NEG-4-no-run-for-branch`, 含 `test_case_in_unit_tests` 指向 SC-2/SC-4 覆盖新分支的具体 pytest 用例 (哪怕是复用同一条测试, 也要写实名, 不写「另案」)。
2. rule6_note 把「追加到 NEG-3 当时开的缺口 issue, 若无则新开」改成实名「追加到 aria-plugin#127」, 并在 §5 issue 同步行里给 #127 一条具体动作 (评论指出 NEG-4 是同类第三实例)。
3. 若 Phase B/D 团队认为回答 #127 的根本问题 (fixture 输入输出格式是否是合适验证载体) 超出本 spec 范围, 应在 spec 里显式写明「本 spec 不解决 #127, 只是又一个同形态实例」, 而不是用「若无则新开」掩盖已经存在且已经问到点子上的疑问。

---

### [A3-R2-M2] Major — reason 封闭集「9」未真正勘正; 与源码同一 docstring 内「规则 5 不产终态」自相矛盾, 且被 SC-2/SC-9 逐字继承

**锚点**: `path_coverage.py:20-33` (@400f0bc); proposal.md §4; SC-2; SC-9; R1 聚合表簇 #17 (A3-m1+A4-m1) 「逐条吸收」标记; aria-plugin#126 原文。

**问题**: 实读 `path_coverage.py:20-33` docstring:

```
判定规则 1-8 (...):
  1. git diff 失败              → unknown,        reason=git-diff-failed
  2. diff 成功但输出为空        → covered,        reason=empty-diff
  3. 变更含 workflows 目录下文件 → covered,        reason=workflow-files-changed
  4. 零 workflow 文件 (前置短路) → not_applicable, reason=no-workflow-files
  5. 逐 workflow 解析 (中间步骤, 不产终态)
  6. 任一 workflow 判 covered   → covered,        reason=workflow-trigger-matched
  7. 无 covered ∧ 有 parse 失败 → unknown,        reason=workflow-parse-failed
  8. 全解析成功且全不触发       → not_applicable, reason=no-triggering-paths
横切: 评估器自身内部异常 → unknown, reason=internal-error
```

规则 5 被同一份 docstring 自己标注**「不产终态」**——即产生终态 reason 的规则只有 1/2/3/4/6/7/8 共 **7 条**, 加横切的 `internal-error` = **8** 个终态 reason (逐字与我 R1 grep `test_path_coverage.py` 得到的 8 个前缀吻合: `git-diff-failed`/`empty-diff`/`workflow-files-changed`/`no-workflow-files`/`workflow-trigger-matched`/`workflow-parse-failed`/`no-triggering-paths`/`internal-error`)。

再查这个「9」的历史源头: `forgejo GET /repos/10CG/aria-plugin/issues/126` 原文写「终态封闭集 **8 → 9**」——即 #126 自己的 issue 叙事就已经把 `internal-error` 独立成档前后的计数写错了一位 (真实应为「7 → 8」: 独立前 `internal-error` 借用 `git-diff-failed` 的壳, 可辨别终态是 7 个; 独立后是 8 个)。v2 proposal.md §4 试图勘正 R1 A3-m1 (我在 R1 指出的「8 vs 9 矛盾」), 写成:「reason 封闭集 (**9 个 = 8 规则终态 + internal-error**, R1 A3-m1 勘正)」——这不是勘正, 这是把同一个错误数字用一种新的、且与同一 docstring 内「规则 5 不产终态」直接矛盾的方式重新表达 (「8 规则终态」意味着 1/2/3/4/5/6/7/8 全部产终态, 但规则 5 自己说没有)。

这个数字被两条 Success Criteria 逐字继承:
- SC-2:「参数化 **全 9 reason** × covered/unknown + None」
- SC-9:「`evaluate_path_coverage` 参数化**全 9 reason**」

两条都要求 9 个参数化用例, 但实际只有 8 个互斥的 (decision, reason) 组合存在于代码里。R1 聚合表把这一条 (簇 #17, A3-m1+A4-m1) 标记「逐条吸收」——本轮实读证实**该标记不成立**, v1→v2 只是换了措辞, 底层错误原封不动地被搬进了两条验收标准。

**按 spec 实施会怎样错**: Phase B 实现者若照字面写 9 组 `pytest.mark.parametrize` 用例, 会在枚举到第 8 个真实 (decision, reason) 组合后找不到第 9 个, 只能: (a) 猜测式拆分某个已有 reason 的子变体凑数 (例如把 `workflow-trigger-matched` 的 dispatchable/non-dispatchable 当成两条「reason」, 但这两者的 `reason` 字符串其实相同, 只是 `dispatchable_workflows` 不同, 这是**混淆了两个不同维度的字段**), 或 (b) 沉默地只写 8 条而让 SC-9 的文字描述与测试代码永久脱节。两者都不是"测试跑起来自然会发现"的那种自纠正错误 (不同于 A3-m3 的情形)——因为没有一个独立断言去检查「参数化用例数是否恰为 N」, 这个数字本身只活在 spec 散文和实现者的记忆里。

**建议**: §4 与 SC-2/SC-9 统一改成「8 个 = 7 规则终态 + internal-error」; 顺手在 `path_coverage.py:36` (「⇒ 终态 reason 封闭集共 9 个」) 留一条勘正 (描述性改动, substitute 覆盖, 不需要额外 AB), 并在 aria-plugin#126 补一条评论修正其正文的「8→9」为「7→8」(该 issue 已 closed 但正文错误计数会被后续检索者继续引用, 本 spec 自己就是一个实例)。

## 未发现问题但已核验的点 (R2 新增核验)

- **`test_gate_state_helper.py` 22 测试无隐藏回归面**: 全文读取确认无一条测试对 `write_gate_state` 返回 dict 做 exact-keys 断言 (`assertEqual(set(gate.keys()), {...})` 一类); 全部断言按字段取值 (`gate["retry_count"]` 等), 新增 `no_run_observations`/`no_run_escalation_done` 两键不会使既有 22 测试变红, SC-12「既有 22 全绿」在这一维度可信。`_migrate_state` 只检查 `format_version=="1.0"`, 不检查 `gate_state` 内部形状, `format_version` 不 bump 与两新字段是可并存的设计。
- **`write_gate_state` 整字典重建模式对新字段遗漏是自纠正的**: 该函数当前实现是 `state["gate_state"] = {...9个键的字面量...}`(非增量 merge), 若 Phase B 实现疏忽把两新键漏写进这个字面量, SC-11(a) 的连续 3 次 wait 断言 (`no_run_observations` 应 1/2/3) 会立即失败, 不构成静默丢字段风险。
- **SC-6 not_applicable 结构性不可达**: 复核 `gate_check` 早退分支顺序, 与 R1 结论一致, 未见新问题。
- **SC-14「pending」枚举行定位**: `grep -n '"pending"' SKILL.md` 在当前基线精确命中 2 行 (`:180`/`:276`), 与 §5 文档同步表声明的两个落点一致, 该子句可执行。**但**同一 SC 的另一子句「`grep -c gate_error SKILL.md` 覆盖 `:172-183` 摘要块」字面只是全文计数, 不核验命中行是否落在该行号区间 (`gate_error` 目前在文件其它 3 处已有引用) ——若 Phase B 漏改 `:172-183` 摘要块本身, 但改了别处 (如 `:290`), 全文计数仍会增加, 该子句会误判通过。判 Minor (见下)。

## 补充 Minor (未构成独立编号, 并入判定)

- **[m] SC-13 TASK-0 缺「dispatch 2xx 但 600s 内零 run」分支**: 详见「R1 处置核对」簇 #10 一行; 建议 §3.4 补第三处置: 该分支记录为「inconclusive — 阈值默认维持, 计入 Risks R-b 待下次机会重测」, 避免执行者临场发明判据。
- **[m] SC-14「grep -c gate_error 覆盖摘要块」子句应改写为行号范围检查** (如 `sed -n '172,183p' SKILL.md | grep -c gate_error`), 而非全文计数, 见上「未发现问题但已核验的点」。
- **[m, 信息性] 多容器并发操作同一 PR 的边界未声明**: cluster #1 的「≤1 次自动处方 / episode」有界性建立在 `gate_state` 是单容器本地文件这一前提上; 若两个 workflow-runner 会话 (容器) 意外同时对**同一 PR** 跑 wait_recoverable (与本 spec 认领时排查的「同一 Spec 多容器撞车」是不同维度——这里是同一 PR 的 gate 轮询被重复), 各自本地状态互不可见, 理论上会各自独立地各处方一次。本项目当前的单-PR-单会话协作模型下大概率不会发生, 且不属于本次 R1/R2 讨论范围, 记录为观察项, 不要求本 spec 处理。

## Verdict

PASS_WITH_WARNINGS (0 Critical, 2 Major, 3 Minor)

vote: REVISE
