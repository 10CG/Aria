---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: "2026-08-22T14:25:00.000Z"
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A5-knowledge-manager
critical_count: 0
major_count: 1
minor_count: 2
---

# post_planning R3 — A5 (knowledge-manager) 审计报告

## 摘要

实读 proposal.md（v7，310 行，SOT 未变）全文 + detailed-tasks.yaml v3 全文（19 任务，8 parent，49.5h）+ 本席 R2 单席报告 + R2 五席聚合处置表（8 簇）+ R2 五席全部单席报告（A1~A4，逐条核对本席引用的 finding 内容）。对 v3 跑了独立程序化核验（非目测）：exec_order 单调性（19 任务 × 全部依赖边）、TASK-003 下游 11 任务闭包可达性、`reason` 字段覆盖率、`estimated_hours` 算术、`<4h` 计数 —— 全部与 metadata 声明的数字精确吻合，零违反。另对「TASK-016 预告的 archive-safety-net warn」做了**实测**（非仅静态 grep）：把 v3 yaml 复制一份、批量替换 `status: pending`→`status: completed`，直接调用 `aria/skills/state-scanner/scripts/lib/spec_complete.py::gate_result()` 跑一遍，取得真实 gate JSON。

**归本席的 R2 三簇（#1 / #2 / #8）在 v3 全部 closed**，证据见「R2 处置核对」。

**v3 diff 新发现 1 条 Major + 2 条 Minor**（均为「新鲜眼睛」在 v3 新增/改写文本上找到的缺口，不是 R1/R2 任何一席已报告过又漏修的旧账）：

1. **[Major]** `INV-3.rule` 与 `TASK-016.conditional_parts` 对 proposal §3.5 的「dispatch_viable=false ⇒ 整组从本 spec 删除」清单做了转录，但两处清单都**遗漏了 proposal §3.5 原文明确点名的第 9 项**——「§2.1 末段的 `<pr_branch>` `.replace`」。这段代码示例在 §2.1 正文里是无条件写法，若 dispatch_viable 判定为 false，TASK-006 的 `conditional_parts` 已经正确规定**不引入**这行 `.replace()`；但 TASK-016 归档前的自删清单没有覆盖对应的 proposal 正文段落，会导致归档件在该分支下仍描述一个从未实现的 `.replace()` 调用——直接撞上 INV-3 自己写的判据「归档件不得描述未实现能力」。这不是 v3 新引入的回归（追溯到 A1-PP2-m3 与 A4-PP2-M2 两条 R2 finding 本身给出的修复清单就已经各自遗漏了这一项，v3 只是原样继承），但从未被任何一席指出过，故作为本轮新 finding 报告。
2. **[Minor]** TASK-016 的「预告（R2 A1-m8）」条款断言归档门会「另产一条正交 archive-safety-net warn」，但实测：v3 把触发该 warn 的字面词「调用」从 TASK-005 title 里删掉（R2 disposition 簇 #8 的另一项修复）之后，**全部 19 个任务 title 对 `spec_complete.py` 的 7 个集成关键词正则零命中**；用真实合成目录跑 `gate_result()` 复核，`unverified_claims` 里只有 `runtime_probe:record` 一条，没有 `archive-safety-net-integration-claims-unverified`。R2 同一条 finding（A1-PP2-m8）本身给出的是「二选一」的两种独立修法（预告 或 改措辞），v3 把两种都采纳了，结果其中一种修法（改措辞）已经使另一种修法（预告）描述的前提不再成立——形成 memory `fixes_contradict_each_other_across_clusters` 的形状，只是后果温和（gate 输出变得比预告更干净，不产生任何需要处理的动作）。
3. **[Minor]** 新增的 `metadata.schema_note`（本身是 v3 对 R1-A1-PP2-m4 的补课）字面声称「estimated_hours 用 int」，但顶层 `metadata.estimated_hours: 49.5` 与 `TASK-000`/`TASK-000b`（0.5h）/`TASK-001`（1.5h）三个任务的 `estimated_hours` 均为非整数，schema_note 自身与它描述的数据类型不符。

三条均不产生 fail-open、不掉 SC 承载、不致 TDD 红绿失效；Major 判据落在「按 yaml 执行会违反 spec 不变量」（INV-3 的「不得描述未实现能力」）。

## R2 处置核对

| R2 簇 | 承诺内容（归本席部分） | v3 证据 | 判定 |
|---|---|---|---|
| #1（A1-M1+A2-M1+A3-M1+A4-m4+**A5-M2**）：TASK-004 exec_order 未随「前移」处置改写 | exec_order 全表重编（004=3, 002=4, 003=5…）；物理块前移；TASK-002 依赖 004（机检边） | `TASK-004.exec_order: 3`（物理位置已移到 `# P1` 段首，先于 TASK-002/003）；`TASK-004.parent: "P1"`；`TASK-002.dependencies: [TASK-000b, TASK-004]`；`TASK-002.exec_order: 4`；`TASK-003.exec_order: 5`。`execution_order`/`parallel_tracks.tracks[0]` 两处散文与数值字段方向一致。程序化核验 19 任务 exec_order 全部 > 其依赖 exec_order，零违反 | **closed** |
| #2（A1-M2+A4-M1+**A5-M1**）：TASK-006 调 `compute_verdict`（003 产出）却不依赖 003 | 005/006/010 加边→003；断言 003 ∈ 11 下游闭包 | `TASK-006.dependencies: [TASK-005, TASK-003, TASK-001]` 含 TASK-003（正是我 R2 建议的确切修法）；`TASK-005.dependencies` 含 TASK-003；`TASK-010.dependencies` 含 TASK-003。程序化遍历依赖图，TASK-003 传递闭包内下游任务恰为 `{005,006,007a,007b,010,011,012,013,014,015,016}` 共 11 个，与 `exec_order_note` 声明的清单逐字一致 | **closed** |
| #8（**A3-m1/A5-m1**）：`estimation_note` 数字（"10 个 <4h" 实为 13；008+009=9h 未披露超出 4-8h 带） | 重算「19 任务中 14 个 <4h」+ 配对小计 (002+003 7h / 005+006 6h / 007a+007b 4h / 008+009 9h) 并显式承认「008+009 略超」 | 程序化统计 `<4h` 任务数 = 14（000/000b/001/004/002/005/006/007a/007b/010/013/014/015/016），与 note 数字精确匹配；四组配对小计逐一复算精确匹配；`008+009=9h` 且 note 原文已带「略超, helper CLI 为 L」的诚实披露，不再是无条件断言「近 4-8h」 | **closed** |
| #8（A3-m2/**A5-m2**/A1-m4）：`agent_reason` 仅 7/18 覆盖且非 schema 字段 | 统一改用顶层 `reason:` 字段（DUAL_LAYER_SPEC.md SOT 规定字段名），逐任务 | 程序化检查 `grep -c "^    reason:"` = 19 = 任务总数，19/19 覆盖，字段名与 SOT 一致 | **closed** |

**汇总**: r2_closed = 4 / r2_partial = 0 / r2_not_addressed = 0。归本席的全部 R2 结论在 v3 均已按建议的确切修法落地（TASK-006 依赖边、TASK-004 三处结构信号、estimation_note 重算、reason 字段改名并补齐），无一处只兑现散文层。

## 已核验无误

- **完整重跑 R2 核实过的三条独立于本席簇的交叉引用**（用于判断 v3 是否有跨簇回归）：A1-PP2-M1/M2（TASK-004/TASK-003 闭包）、A2-PP2-M1/M2（同类结构性问题）、A3-PP2-M1/M2、A4-PP2-M1/M2 在 v3 中的落点与本席自己核验的 exec_order/依赖闭包程序化断言完全吻合，无相互矛盾。
- **`completed + N/A` 惯例出处未被重新错误归因**：本席 R2 已勘正该惯例真实先例 = `openspec/archive/2026-08-22-phase-c-integrator-ci-path-coverage/detailed-tasks.yaml`（非 #179）。v3 `readiness_rule`/`INV-3.rule` 提到该惯例时均只写「先例惯例」不点名具体来源；`schema_note`/`estimation_note` 引用 #179 时讨论的是另外两件事（parent/reason 字段命名先例、17 任务 44h 估时方法论），与 N/A 惯例无关；`TASK-000.notes` 里的「#179 已 ship」是协调/collision 上下文的真实引用（另一容器完成的工作），不涉及本惯例。三处逐字核对，均未复发 R1 聚合表的误归因。
- **可追溯性抽检（v3 新增的全部 "R2 A?-M/m?" 字面引用，逐条去源报告核实）**：`R2 A2-M2`（INV-1.encoded_as 引用非破坏性 `git show` + detached-HEAD 先例）对应 A2-backend-architect-PP2-M2 原文（建议改用 `git show` 而非 `checkout`）——匹配；`R2 A1-m3/A4-M2`（INV-3.rule 归档件不得描述未实现能力）对应 A1-PP2-m3 与 A4-PP2-M2 两条原文——内容匹配但清单本身有遗漏（见本轮 M1）；`R2 A4-M1`（TASK-005 reason 提及"需 003"）对应 A4-PP2-M1（TASK-003 图上不可达）——匹配；`R2 A5-M1`（TASK-006 reason）对应本席自己 R2 finding——匹配；`R2 A1-M2/A4-M1`（TASK-010 reason）对应 A1-PP2-M2 第 3 点与 A4-PP2-M1 第 2 点（config-template 依赖 003）——匹配；`R2 A3-M2`（TASK-012 notes 绑定名）对应 A3-PP2-M2 原文——匹配（且已回写进产出方 TASK-002，见下）；`R2 A1-m7`（TASK-015 补 v1.66.1 tag）对应 A1-PP2-m7 原文——匹配；`R2 A4-M2`（TASK-016 conditional_parts）——同上，内容方向匹配但清单遗漏（见 M1）；`R2 A1-m8`（TASK-016 预告 warn）对应 A1-PP2-m8 原文——匹配但前提已被同批另一处修法推翻（见 m1）。九处引用无一处张冠李戴或内容捏造。
- **SC-15 绑定名（A3-M2/A1-m5 处置）双向核验**: 全文 grep `test_sc2_trigger_matched_message` 仅 2 处（TASK-002.deliverables 产出承诺 + TASK-012.notes 消费引用），拼写一致，无残留旧名 `test_trigger_matched_message`；TASK-002.title 的「参数化」与该具名非参数化用例并存，无冲突（TASK-002 deliverables 原文已用「具名非参数化」明确排除歧义）。
- **`sc_coverage_crosscheck`/`checklist_s7_mapping` 终态**：SC-1~SC-16 逐条比对 proposal.md 全部出现，16 项全部在 crosscheck 表列出且未换号；§7 表 4 项与 v3 的 4 行映射逐条对应，落点（TASK-007b/TASK-012/TASK-014/TASK-008）与 proposal §7 原文逐字一致。
- **traps §六三写者序** 与 R2 一致：TASK-001 建节 → TASK-011 上方插 F3/F4/(b)/F6 四行（不动 TASK-0a 行）→ TASK-014 末尾追加 SC-13 行 + 终改 `:241`，三处散文互指且无环、无重复建节。

## Findings

### [A5-knowledge-manager-PP3-M1] `INV-3`/`TASK-016` 的归档前自删清单遗漏 proposal §3.5 第 9 项（`§2.1 末段的 <pr_branch> .replace`），归档件在 dispatch_viable=false 分支下会继续描述一个从未实现的调用

- **scope**: `metadata.invariants.INV-3.rule` / `TASK-016.conditional_parts` vs proposal §3.5 末句
- **问题**: proposal §3.5 原文列出 dispatch_viable=false 时要「整组从本 spec 删除」的 9 项：`§4 整段` / `SC-8` / `SC-9 的 dispatchable 部分` / **`DISPATCH_VIABLE` 常量本身** / `2.3 表的 dispatch 渲染句` / `SC-2 的 dispatch 子项` / `SC-5 (c2)` / `3.3 (a) 行` / **`§2.1 末段的 <pr_branch> .replace`**（后一项原文明确带注「占位符随 dispatch 行消失, 回填无对象; (c1) 的『不含占位』断言保留作守卫」）。
  v3 的 `INV-3.rule` 转写的清单是「§4 / SC-8 / SC-9 dispatchable 部分 / SC-2 dispatch 子项 / SC-5 (c2) / 2.3 渲染句 / 3.3 (a) / Impact 两项 / §7 checklist 1 标 N/A」；`TASK-016.conditional_parts` 逐字复述同一清单。两处都**没有**列入「§2.1 `<pr_branch>` `.replace`」这一项（`DISPATCH_VIABLE` 常量本身虽未直接点名，但可认为被「Impact 两项」——Impact 里的『新 artifact: `DISPATCH_VIABLE` 常量』——间接覆盖，暂不计入本 finding）。
  代码层面这个分叉是被正确处理的：`TASK-006.conditional_parts` 明写「仅 §2.1 末段 `<pr_branch>` `.replace` 回填随 `metadata.dispatch_viable`: false ⇒ 不引入 `.replace`」——即若 dispatch_viable=false，实际代码里根本不会出现这行 `.replace()`。但 proposal.md **文档正文**（§2.1 代码示例块）是无条件展示这行 `.replace()` 的；proposal §3.5 自己也明确要求在 false 分支把这段正文一并删除。TASK-016 是全文件唯一负责「归档前编辑 proposal.md 正文」的任务，它的清单缺了这一项，意味着若 dispatch_viable 最终判定为 false，归档进 `openspec/archive/` 的 proposal.md 的 §2.1 仍会展示一行从未被实现的 `.replace("<pr_branch>", ...)` 调用——直接违反 `INV-3.rule` 自己紧接着写的判据「归档件不得描述未实现能力」，也是 proposal 自己在同一句里强调的「不留零消费方字段/常量」。
- **不是 v3 新引入的回归，但从未被指出过**：追溯 R2 两条相关 finding 的原始建议文本——A1-PP2-m3 给出的 TASK-016 清单是「proposal §4 / SC-8 / SC-9 / SC-2 dispatch 子项 / SC-5 (c2) / 2.3 dispatch 行 / 3.3 (a) 行」（7 项，同样缺这两项）；A4-PP2-M2 给出的清单是「删 §4 整段 / SC-8 / SC-9 dispatchable 子句 / SC-2 dispatch 子项 / SC-5 (c2) / 3.3 (a) 行 / Impact 的 dispatchable_workflows 与 DISPATCH_VIABLE 两项」（也不含 §2.1 `.replace`）。v3 的清单是这两条 R2 finding 建议的并集，忠实执行了两位审计者各自开出的处方——但两张处方本身都遗漏了 proposal §3.5 原文的这一项，故 v3 原样继承了这个盲区。这是本轮（R3、fresh eyes）第一次被指出。
- **为什么是 Major 而非 Critical**: 只在 `dispatch_viable` 最终判定为 **false** 时才会实际发生（TASK-0a 尚未跑，proposal F6 明确「未验」，真实概率不确定）；且只影响 D.2 归档产物的文档准确性，不影响 B.1-C.2 期间任何运行时行为、不产生 fail-open、不掉任何 SC 的承载（`sc_coverage_crosscheck` 表本身不含这一项，因为它是文档正文，不是 SC）。但它确实是「按 yaml 字面执行会违反 spec 已写明的不变量（INV-3 的『不得描述未实现能力』）」，够格本轮 Major 门槛。
- **建议**: 在 `INV-3.rule` 与 `TASK-016.conditional_parts` 两处清单里补上一项，如「§2.1 末段 `<pr_branch>` `.replace` 段落」，与 proposal §3.5 原文 9 项对齐（保留 `DISPATCH_VIABLE` 常量是否算入「Impact 两项」的判断留给下一轮，若不确定可一并显式列出，成本近零）。

### [A5-knowledge-manager-PP3-m1] TASK-016「预告」的 archive-safety-net warn 已被同批另一处修法（TASK-005 title 改措辞）消除，预告条款与实测矛盾

- **scope**: `TASK-016.verification`（"预告 (R2 A1-m8)"一行）vs `TASK-005.title`
- **问题**: R2 A1-PP2-m8 原始 finding 指出：归档合成目录跑 `spec_complete.py --gate` 会稳定产出一条 `archive-safety-net-integration-claims-unverified` warn，根因是 TASK-005 的 title 含「调用」二字命中集成类关键词正则；该 finding 给出**两种互斥的替代修法**（原文用"或"字连接）：(a) 在 TASK-016 加一句「预告」声明这条 warn 属既有启发式、非缺陷；(b) 把 TASK-005 title 里的「调用」改成不触发词。
  v3 把两种修法**都采纳了**：TASK-016.verification 加了预告句（"归档门对本 yaml 会另产一条正交 archive-safety-net warn (标题含「调用」类集成关键词的任务)"），TASK-005.title 也把原来的「旧名包装关键字调用可用」改写成「旧名包装以关键字**形参** `main_branch=` 仍可用」（不含「调用」）。
  **实测**（非仅静态判断）：(1) 用 `spec_complete.py` 里实际使用的 `_INTEGRATION_KEYWORD_PATTERNS` 七条正则（`集成(?!测试)` / `接线` / `wire` / `integration` / `调用` / `registered` / `hook`）逐一扫描 v3 全部 19 个任务的 `title` 字段，**零命中**；(2) 把 v3 yaml 复制一份、全部 `status: pending` 替换为 `status: completed`（模拟归档时全 done 状态），直接调用 `aria/skills/state-scanner/scripts/lib/spec_complete.py::gate_result()` 跑真实 gate，输出 `unverified_claims` 里只有一条 `runtime_probe:record`（telemetry 分区缺失，SC-16 (b) 红窗预期内），**没有** `archive-safety-net-integration-claims-unverified`。
  也就是说：TASK-005 title 改措辞这一项修复本身是**正确且完全生效**的（归档门确实不会再产出这条 warn）；但 TASK-016 的预告句现在描述的是一个已经不会发生的事件，读者（尤其是无人值守的 main-loop）如果在 D.2 严格按预告行事，会白等一条永远不出现的 warn，属 memory `fixes_contradict_each_other_across_clusters` 的形状（两处方合并后互相抵消/矛盾），只是后果温和：不出现该 warn 本身是更干净的结果，不需要任何补救动作，不影响 SC-16 (b)/(c) 的机读判定（两者都只看 `runtime_probe` 轴，不看 archive-safety-net 轴）。
- **为什么是 Minor**: 不违反任何不变量、不掉 SC 承载、不致红绿失效；`TASK-016.verification` 里这句「预告」是纯提示性文字，不是任何断言的输入，D.2 执行者即便发现预告落空也没有需要执行的补救步骤（原文本身写的是「非缺陷, 记 handoff 不当失败处理」，即便 warn 缺席也同样不构成需要处理的失败）。
- **建议**: 把这句预告改成过去式陈述或直接删除（例如改成「TASK-005 title 已避开集成关键词正则 (R2 A1-m8 二选一修法之一)，归档门预期不再产出 archive-safety-net-integration-claims-unverified；已用合成全 completed 目录实测确认」），避免与实测结果矛盾。

### [A5-knowledge-manager-PP3-m2] 新增 `schema_note` 声称「estimated_hours 用 int」，但顶层与 3 个任务的实际值均为非整数

- **scope**: `metadata.schema_note` vs `metadata.estimated_hours` / `TASK-000`/`TASK-000b`/`TASK-001`.`estimated_hours`
- **问题**: v3 新增的 `schema_note`（本身是为回应 R1 A1-PP2-m4「两处 schema 偏离无声明」而补的一条元信息）字面写「estimated_hours 用 int」。但实测：`metadata.estimated_hours: 49.5` 本身非整数；19 个任务里 `TASK-000`（0.5）、`TASK-000b`（0.5）、`TASK-001`（1.5）三个也是非整数。`schema_note` 想声明的应该是「本文件用**数值**（而非 SOT 规定的字符串区间，如 "2-3h"）表示 `estimated_hours`」，但字面写成了「int」，与文件里实际存在的浮点数据自相矛盾。
- **风险**: 属描述准确性缺口，不影响任何机读解析（无脚本按 `schema_note` 的字面内容做类型校验），不产生执行分叉——但下一个读者（含 R4+ 审计席位）若信了这句话去写校验脚本断言 `isinstance(x, int)`，会对 3 个任务和顶层聚合值产生假红。
- **建议**: 把 `schema_note` 该分句改为「estimated_hours 用数值 (int/float 均可, 非 SOT 的字符串区间)」或类似措辞，消除与实际数据的类型不一致。

## Verdict

**PASS_WITH_WARNINGS**（0 Critical / 1 Major / 2 Minor）。归本席的 R2 三簇（#1 / #2 / #8）全部 closed，且用程序化断言（非仅目测）复核了 exec_order 单调性、TASK-003 11 任务下游闭包、`reason` 字段覆盖率、算术、`<4h` 计数五项机检不变量，零违反。v3 新发现 1 条 Major：`INV-3`/`TASK-016` 对 proposal §3.5 归档自删清单的转录遗漏了「§2.1 `<pr_branch>` `.replace`」一项，这是 R1→R2 两轮相关 finding（A1-PP2-m3/A4-PP2-M2）各自处方本身就带的盲区，v3 原样继承，首次在本轮被指出，修法为一行级补漏。2 条 Minor（TASK-016「预告」条款与实测矛盾；`schema_note` 类型声明与实际数据不符）均不阻塞、可与 Major 一起顺手改。

**vote: REVISE**
