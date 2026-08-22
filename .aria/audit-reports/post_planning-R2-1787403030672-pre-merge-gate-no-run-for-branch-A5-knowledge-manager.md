---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 1787406918895
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A5-knowledge-manager
critical_count: 0
major_count: 2
minor_count: 2
---

# post_planning R2 — A5 (knowledge-manager) 审计报告

## 摘要

实读 proposal.md v7 全文 (310 行) + detailed-tasks.yaml v2 全文 (444 行，18 任务) + R1 五席单席报告 + R1 聚合处置表 (12 簇) + `.aria/config.json` + 两份归档先例 (`2026-08-22-phase-c-integrator-ci-path-coverage/detailed-tasks.yaml`、`secret-guard-manifest-precision/detailed-tasks.yaml`)。归我席的 R1 两条 Major (TASK-011 INV-3 缺标 / TASK-001 缺 verification) 与三条 Minor 在 v2 均已**实质修复**，证据见下节。

新一轮 (fresh eyes) 在 v2 自身新引入/未完全兑现的处方中发现 **2 条 Major**：(1) `dependencies` 图未覆盖 TASK-006 对 TASK-003 的真实前提——TASK-006 的 GREEN 实现调用 `compute_verdict`（TASK-003 的产出），其自身 verification（SC-5/SC-10 翻绿）结构上不可能在 TASK-003 未落地时通过，但 `dependencies: [TASK-005, TASK-001]` 未列 TASK-003，与 INV-2 自称「TDD 顺序 encoded_as: dependencies + exec_order」矛盾，且与同文件里 TASK-013 正确列出 TASK-003 的做法不一致；(2) R1 Cluster #4 的「exec_order 前移到 2 之前 (gate 轨首位)」处方未被应用到 TASK-004 的 `exec_order:` 数值字段（仍为 4，排在 TASK-002=2/TASK-003=3 之后），与新增的顶层 `execution_order:` 段落及 `parallel_tracks.tracks[0].tasks` 列表（两处都把 TASK-004 排在最前）自相矛盾——该处方只在散文层兑现，机读的 per-task 字段层未兑现。2 条 Minor：`estimation_note` 的两处数字与 v2 实际不符（"10 个 <4h" 实为 13 个；"配对合计落 4-8h" 但 TASK-008+009 = 9h）；R1 Cluster #12「agent_reason 逐任务」承诺只落地在 7/18 个任务（TASK-003/004/007a/007b/008/012/014），其余 11 个仍无 `agent_reason` 标注。

Rule #10 留痕（`audit_checkpoints_note`）经对照 `.aria/config.json` 实值逐字核验准确；`completed + N/A` 惯例经归档语料核实为真实先例（非虚指），但精确来源是同日归档的 `2026-08-22-phase-c-integrator-ci-path-coverage`，非 R1 表面提及的 #179（#179 本身不含该惯例，属另一条 note 形态的参照对象）。

## R1 处置核对

| R1 簇 | 处置承诺 | v2 实测 | 结论 |
|---|---|---|---|
| #1 skipped/done 白名单 | 禁用 `skipped`；`completed`+`notes: N/A` + `readiness_rule` + `metadata.dispatch_viable: null` | `grep skipped` 全文件仅命中 `readiness_rule` 自身的说明句（"本文件不使用 skipped"）；TASK-007a/007b `conditional_on` 含 `status: completed, notes 'N/A — …'`；`readiness_rule`/`dispatch_viable: null` 均在场 | **closed** |
| #2 INV-3 四落点 | TASK-006/011/015 加 `conditional_parts` + 依赖边→TASK-001；`INV-3.rule`/`encoded_as` 列全四落点 | 三任务均有 `conditional_parts` 且 `dependencies` 含 TASK-001（L176/288/370）；`INV-3.rule`(L35) 逐字列 TASK-007a/007b + TASK-006 `.replace` + TASK-011 三项 + TASK-015 CHANGELOG，`encoded_as`(L36) 同步列全 | **closed**（与 A3-R2 独立核验一致） |
| #3 TASK-007 拆 RED/GREEN | 拆 TASK-007a(qa)/007b(be) | 已拆，agent 分属 qa-engineer/backend-architect | **closed** |
| #4 守卫 TASK-004 | deps→[TASK-000]；钉 SHA 入 docstring；SC-7 加 mutation；**exec_order 前移到 2 之前** | 前三项均落（L142 `dependencies: [TASK-000]`；verification 含"钉 SHA 入 docstring"与"多/少一键 mutation"）；**第四项未落**：TASK-004 `exec_order: 4`（L137），仍排在 TASK-002(2)/TASK-003(3) 之后，与新增 `execution_order:`/`parallel_tracks` 两处"TASK-004 最前"矛盾 | **partial**（见 Findings M2） |
| #5 INV-1 有向检查 | 父提交 `_normalize_pr_ci_status([])=='pending'` 且本 commit 同含两文件；main-loop 验证 | `INV-1.encoded_as`(L30) 与 TASK-003 verification(L128) 逐字一致 | **closed** |
| #6 traps 三写者 | TASK-001 建节；TASK-011 插四行；TASK-014 末尾追加+终改 :241 | TASK-001 verification(L89) / TASK-011 deliverables(L284) / TASK-014 notes(L359) 三处分工陈述一致且无重叠 | **closed** |
| #7 主仓 5 类改动无分支承载 | TASK-015 (ii) feature 分支承载 5 类 + 双 remote 核验 (重试) + 不带路径 git status | TASK-015 title(L366) 列全 5 类；verification(L378-380) 含双 remote ls-remote 重试 + 不带路径 `git status` | **closed** |
| #8 SC-3 末句/SC-11(d)/INV-5 grep | TASK-005 加 SC-3 末句；TASK-008 加两条 reset 成功路径；TASK-011 verification 加 INV-5 grep | 三处均逐字命中（TASK-005 carries_sc "SC-3 末句 RED"；TASK-008 title 含两条 reset 成功路径；TASK-011 verification 含 "INV-5 grep"） | **closed** |
| #9 TASK-001 verification 缺口 (本席 R1-M2) | 加 traps 建节 + memory grep 两条 verification | TASK-001 verification 第 3/4 条(L89-90) 逐字覆盖 | **closed** |
| #10 v1.66.4 漏 tag | TASK-015 补打 v1.66.4@9e6a17c | TASK-015 title(L366) 含"补打漏掉的 v1.66.4@9e6a17c tag" | **closed** |
| #11 六处零散 minor | deps 补 010；SC-14 落脚本；措辞改"无计数"；占位；文件歧义澄清；字段文档承载；绑定名 | 逐项核对（TASK-011 deps 含 TASK-010；verification 含 `test_doc_sync_no_run.py`；§C.2.4 步骤 6 文案已是"无计数"；`dispatch_viable: null` 在场；TASK-002 deliverables 显式排除 test_ci_backends.py；TASK-011 conditional_parts 含字段文档；TASK-012 notes 含绑定名） | **closed** |
| #12 schema/estimation/exec_order/Rule#10/main-loop/execution_order 六项 | `agent_reason` 逐任务 / estimation_note+tdd_note / exec_order_note / audit_checkpoints_note / TASK-016 时窗 / agent_summary.note / execution_order+agent_summary 段 | 后 6 项全部在场且经核验准确（`audit_checkpoints_note` 与 `.aria/config.json` 逐字吻合；TASK-016 时窗条款在场；`agent_summary.note` 点名 main-loop 2 先例）；**首项未完全兑现**：`agent_reason:` 仅出现在 TASK-003/004/007a/007b/008/012/014 共 7 个任务的 notes 里，其余 11 个（000/001/002/005/006/009/010/011/013/015/016）无此标注，与"逐任务"字面不符 | **partial**（见 Findings m2） |

**汇总**: 10 closed / 2 partial / 0 not_addressed。两处 partial 均为"散文层已兑现、机读字段层未兑现"的同构缺口——建议 fix 时按 memory `fix-the-class` 一并核对是否还有第三个同形态遗留（本轮未发现第三例）。

## 已核验无误

- **`estimated_hours` 算术** (独立重算): 0.5+1.5+3+4+2+3+3+2+2+4+5+3+4+4+1+3+2+2 = **49**，与 `metadata.estimated_hours: 49` 一致；18 个 `- id: TASK-` 计数与 `total_tasks: 18` 一致。
- **Rule #10 留痕**: `.aria/config.json` 实测 `checkpoints` = `{post_brainstorm: off, post_spec: convergence, post_planning: convergence, mid_implementation: off, post_implementation: off, pre_merge: off, post_closure: off}`；`audit_checkpoints_note` 点名的 mid_implementation/post_implementation/pre_merge/post_closure 四项与实值逐字吻合，post_planning 本身"已排"的表述也准确。
- **`completed + N/A` 惯例溯源**: 全仓 grep 未在 archive 中找到字面 `"N/A —"`（带破折号）字符串，但在**同日归档**的 `openspec/archive/2026-08-22-phase-c-integrator-ci-path-coverage/detailed-tasks.yaml` 找到实质同构先例：`gate_condition: "...否则由 owner 置 completed 并注明 N/A"` + `"happy path 下本任务在 wave_1b 即被 owner 置 completed + N/A"` + 对 `lib/detailed_tasks.py:83` done-family fail-CLOSED 白名单的显式引用——与本 yaml `readiness_rule` 引用的机制完全一致，证实"先例惯例"非虚指，只是本 yaml 把惯例操作化为更严格的"notes 首词"约定（先例未要求首词/破折号格式），这是本 spec 自己的精化，不构成偏离。`secret-guard-manifest-precision`（#179）本身**不含**该惯例（其 metadata 只有 8 个基础字段 + `a2_entry` + `invariants`，无 `estimation_note`/`tdd_note`/`exec_order_note`/`audit_checkpoints_note`/`readiness_rule` 任何一个），R1 聚合表笼统写"先例惯例"未精确指向来源，但结论本身经核实成立。
- **INV-3 四落点与 conditional_parts 逐字对应**: TASK-006(L179)/TASK-011(L291)/TASK-015(L373) 三处 `conditional_parts` 文本与 `INV-3.rule`(L35) 删除清单逐项对应，且三任务 `dependencies` 均含 TASK-001，可在执行时读到 `metadata.dispatch_viable`（与 A3-R2 独立核验结论一致，非重复计分）。
- **`main-loop`/`agent_summary.note`**: `agent_summary.note`(L443) 准确复述本席 R1-m1 的核实结论（2 个归档先例、17 次使用），未夸大也未遗漏。
- **`parallel_tracks` 覆盖**: 本席 R1-m3 指出 TASK-010 未纳入任何轨道声明；v2 `parallel_tracks.tracks[1].tasks`(L429) 已包含 TASK-010，缺口已补齐（非官方 12 簇之列，但确认已顺手修复）。

## Findings

### [A5-knowledge-manager-PP2-M1] `dependencies` 未覆盖 TASK-006 对 TASK-003 的真实前提，与 INV-2 自称的编码方式矛盾

- **scope**: TASK-006.dependencies / INV-2.encoded_as
- **问题**: TASK-006（§2.1 `gate_check` 实现，GREEN）的控制流按 proposal §2.1 代码块直接调用 `compute_verdict(...)`（TASK-003 的产出：`compute_verdict` 新增的 `not_found` 分支）——`gate_check` 拿到 `out` 后仅在 `out.get("gate_error")` 在场时做 `<pr_branch>` 回填。若 TASK-003 尚未落地，基线 `compute_verdict` 对 `not_found` 走 fallthrough 返回 `green`（proposal §1 明文实测），`out["gate_error"]` 恒为 `None`，TASK-006 自己的 verification "**SC-5/SC-10 翻绿**" 结构上不可能通过。但 TASK-006 `dependencies: [TASK-005, TASK-001]`（L176）未列 TASK-003；追其祖先集 = {TASK-005, TASK-004, TASK-000, TASK-001}，**不含 TASK-003**。
- **对照**: `INV-2.encoded_as`（L33）自称 "dependencies + exec_order; carries_sc 标 RED/GUARD" 是 TDD 顺序（含隐含的跨对前提）的编码机制；而 TASK-013（L334，SC-12 全量测试）反而正确地把 `TASK-003` 与 `TASK-006` 都列进 `dependencies`（`[TASK-003, TASK-006, TASK-007b, TASK-009]`）——证明本 yaml 其他处确实遵循"跨对前提也要显式列出"的约定，TASK-006 独漏是不一致而非设计选择。
- **风险**: 若按 `dependencies` 驱动的调度器（而非线性通读 exec_order）执行——这正是 `exec_order_note` 明写"非串行调度"所暗示的执行模型——TASK-006 可能在 TASK-003 未落地时启动，其自身 verification 会假红，且不会被现有 Finding/Cluster 捕获（R1 12 簇均未点名此边）。同款缺口经检查后**不构成传染**：修复 TASK-006 的边后，TASK-007a 对 TASK-002（创建 `NotFoundVerdictTests`）/TASK-005（创建 `GateCheckNotFoundTests`）的隐性前提会随 TASK-006→TASK-003→TASK-002 的链条自动补上，无需再单独打补丁。
- **建议**: `TASK-006.dependencies` 改为 `[TASK-005, TASK-003, TASK-001]`（`exec_order` 数值本身已满足 3<6，无需重排，只需补边）。

### [A5-knowledge-manager-PP2-M2]（R1 Cluster #4 partial）TASK-004 `exec_order` 未按处方前移，与新增 `execution_order`/`parallel_tracks` 段自相矛盾

- **scope**: TASK-004.exec_order / `execution_order:` 段 / `parallel_tracks.tracks[0]`
- **问题**: R1 聚合表 Cluster #4 处方第四项明文"exec_order 前移到 2 之前 (gate 轨首位)"，理由是 A1-M4 指出"守卫落在被守护变更之后会退化成自证快照"。v2 中 TASK-004 的其余三项处方均已兑现（deps→[TASK-000]、SHA 钉入 docstring、SC-7 mutation），**唯独 `exec_order:` 数值仍为 `4`**（L137），排在 TASK-002 (`exec_order: 2`) 与 TASK-003 (`exec_order: 3`) 之后。而 v2 新增的两处顶层结构都把 TASK-004 排在最前：`execution_order:`(L434) "gate 轨: **TASK-004** (守卫@基线) → TASK-002 (RED) → TASK-003 (GREEN)…" 与 `parallel_tracks.tracks[0].tasks`(L427) `[TASK-004, TASK-002, TASK-003, …]`。同一文件内三处对"TASK-004 该排第几"给出了两种相反的答案。
- **风险影响有限但真实**: `exec_order_note` 自称该字段是"拓扑序的 advisory tie-break"；由于 TASK-004 与 TASK-002/003 之间本就没有 `dependencies` 边（三者互不依赖，只共同依赖 TASK-000），实际执行安全性主要靠 TASK-004 verification 里"钉 SHA 9e6a17c 入 docstring, 在该 SHA 上核验绿"这条**与时序无关**的核验方法兜底——即便真按数值顺序先做 002/003 再做 004，只要 004 按其 verification 对准 9e6a17c 校验，"自证快照"风险仍被规避。但这只是**运气好，不是处方被兑现**：R1 聚合表白纸黑字承诺的"exec_order 前移"这一项被跳过且无任何说明，若后续再有人依据 per-task `exec_order:` 数值（而非读散文段）生成执行顺序，会重新引入 A1-M4 指出的语义混乱（即便实际不产生错误结果，也会误导阅读者）。
- **建议**: 把 TASK-004 的 `exec_order` 改为 `2`，TASK-002 改 `3`，TASK-003 改 `4`（其余任务数值顺延，或采用非整数插入 `1.5` 避免连锁重排）；三处（数值字段 / `execution_order:` / `parallel_tracks`）保持字面一致。

### [A5-knowledge-manager-PP2-m1] `estimation_note` 两处数字与 v2 实际任务表不符

- **scope**: `metadata.estimation_note`(L12)
- **问题**: 该 note 称"10 个 <4h 任务是 TDD 配对刻意拆分…配对合计落 4-8h 粒度带"。逐任务清点 `estimated_hours`（18 项：0.5/1.5/3/4/2/3/3/2/2/4/5/3/4/4/1/3/2/2），**<4h 的任务实为 13 个**（000/001/002/004/005/006/007a/007b/010/013/014/015/016），非 10 个；而这 13 个里只有 5 个（002/005/006/007a/007b）真正属于 qa→be 的 RED/GREEN 配对成员，其余 8 个（000/001/004/010/013/014/015/016）是前置/守卫/文档/全量测试/活体/发版/收尾类任务，与"TDD 配对拆分"这一归因无关（各自有其他合理理由，但不是这条 note 声称的理由）。"配对合计落 4-8h 粒度带"对 (TASK-008, TASK-009) 这一对也不成立: 4h+5h=**9h**，超出 8h 上限。
- **推断根因**: "10 个 <4h" 与 R1 A1-m2 报告里对 **v1**（17 任务，TASK-007 尚未拆分）的原始清点数字（"17 任务中 10 个 <4h"）字面相同——v2 把 TASK-007 拆成 007a/007b 后任务总数变为 18 且粒度分布已变化，这条 note 疑似原样沿用了 v1 的旧统计，未针对 v2 重新核算。
- **建议**: 重新计数并改写为准确数字（"13 个 <4h，其中 5 个是 TDD RED/GREEN 配对成员"），或改用非绝对数字的定性表述（"多数 <4h 任务源于 TDD 配对拆分，另有若干前置/收尾类任务因职责单一而天然 <4h"）避免和文件本体脱节；"4-8h 粒度带"如需保留，需说明 (TASK-008,009) 例外或改用"4h 起"等更宽松措辞。

### [A5-knowledge-manager-PP2-m2]（R1 Cluster #12 partial）`agent_reason` 承诺"逐任务"，实际只覆盖 7/18

- **scope**: 全部 18 任务的 `notes` 字段
- **问题**: R1 聚合表 Cluster #12 处方明写"agent_reason 逐任务"（回应 A1-m1 "本文件零任务带 reason，A.3 分配理据不可复核"）。v2 中 `grep agent_reason` 只命中 7 处：TASK-003/004/007a/007b/008/012/014，其余 11 个任务（TASK-000/001/002/005/006/009/010/011/013/015/016）的 `notes` 字段无 `agent_reason:` 标注。集中在 P0/helper 轨/文档轨/ship 轨的任务未获标注（例如 TASK-011 由 knowledge-manager 承接文档+决策面双料内容，是本文件里 agent 分配理据最值得写一句的位置之一，却缺失）。
- **风险**: 属可追溯性缺口而非正确性缺口（不影响脚本解析、不影响执行）。但既然处方原文用的是"逐任务"这一全称表述，只兑现 39%（7/18）容易被后续读者误判为"已完成"，且与 R1-m1 想解决的"A.3 分配理据不可复核"问题相比仍有 11 处理据不可复核。
- **建议**: 为剩余 11 个任务各补一句 `agent_reason:`（多数可归纳成模板：main-loop 类 = "凭据/commit 权限动作"；qa/be 无 note 的几个 = "纯测试任务"/"纯实现任务"；knowledge-manager 的 TASK-010/011 = "文档同步任务"），或在 `estimation_note`/新增一条 note 里显式声明"仅对分配到非默认/易混淆 agent 的任务标注 agent_reason，其余按 agent 字段自明"，把范围收窄写清楚，避免"逐任务"被字面误读。

## Verdict

PASS_WITH_WARNINGS（0 Critical / 2 Major / 2 Minor）。归我席的 R1 两条 Major 与三条 Minor 已全部 closed；R1 12 簇中 10 closed / 2 partial（Cluster #4 exec_order 数值未前移、Cluster #12 agent_reason 未逐任务落地——均为"散文层兑现、机读字段层未兑现"的同构缺口）；新发现 1 条 Major（TASK-006 缺 TASK-003 依赖边，违反 INV-2 自称的编码完整性）。两条 Major 均不产生 fail-open 或 SC 漏承载（Critical 门槛未触发），但依 severity 定义（"依赖错序致 TDD 红绿失效"）够格 Major，建议再落一版修订两处后可进 B.1。

**vote: REVISE**
