---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T20:32:24.701Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 审计报告 — knowledge-manager

## 审计结论

本轮镜头按派发要求聚焦「R1-fix 新写内容自身」，重点独立重核 §Rule #6 分类。**结论：该分类不成立，且是本轮最重要的一项发现。** 另发现 §引用卫生（R1 M7 的修复目标）本身在新写内容里复发同类问题。其余合规面（Rule #5 / Rule #1 / Level / D-K 版本策略 / 同形状兄弟位置枚举 / 外部 issue 状态）逐项实读核验后基本站得住，仅 Level 2 的佐证文字有过时表述。

## Verdict

**FAIL** — 1 Critical（Rule #6 分类错误，且是非可协商规则 #6 的合规判定，将作为 owner 已裁定先例记入项目历史）+ 1 Major（§引用卫生的修复本身新引入同类失实引用）+ 1 Minor。

---

## 逐项核验记录

### 1. Rule #6 档位归属 — 独立重核（结论：分类错误，应落第三行，不是第二行）

**实读的证据文件**（均已完整读取，非采信 Spec 转述）：

- `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json`（v1.1.0）
- `aria-plugin-benchmarks/ab-suite/phase-c-integrator.json`（v1.1.0）
- `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`（全文）
- `standards/conventions/skill-benchmark-exemption.md`（判据表 SOT，全文）
- `aria-plugin-benchmarks/ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json` + `benchmark.md`（该套件唯一一次历史运行记录）
- `aria-plugin-benchmarks/ab-results/2026-07-31-v1.65.0-122-rule6/grading-summary.md` + `eval-1/eval_metadata.json`（Spec 援引的"更贴切先例"的实际运行记录）
- `aria/skills/phase-c-integrator/SKILL.md`（:160-290 区间，逐行核对 Spec 引用的 :167/:242/:243/:267/:279）

**发现 1a — `phase-c-integrator-pre-merge-gate.json` 不是 AB_TEST_OPERATIONS.md 定义的 eval 套件，而是一份单元测试 fixture 映射清单，且它自己的历史运行记录明确自证"不是 AI 行为 AB"：**

- `AB_TEST_OPERATIONS.md:95-112`「Eval Case 编写规范」规定套件格式必须是 `evals[]` 数组，每条含 `prompt`（50+ 字场景）/`expected_output`/`expectations`，供 `/skill-creator benchmark` 派生 with_skill/without_skill 两个 AI subagent 执行同一 prompt 后由 grader 评分。
- 但 `phase-c-integrator-pre-merge-gate.json` 的顶层键是 `fixtures[]`，每条只有 `id`/`file`/`expected_verdict`/`test_case_in_unit_tests`/`purpose`，**全文件零个 `prompt` 字段**，结构上无法喂给 `/skill-creator` 的 with/without subagent 流程。
- 该套件**唯一一次历史运行记录** `ab-results/2026-05-10-phase-c-integrator-pre-merge-gate/benchmark.json:6` 写明 `"type": "structural_verification"`；`benchmark.md:22-23` 原话：「None of this can be reproduced in a unit-test mock environment. State-scanner-style happy-path / negative-fixture **AB measurement does not apply**.」`benchmark.md:45` 原话：「**AB measurement of LLM workflow behavior** under multi-PR concurrent CI **not feasible in mock**; deferred to production dogfood」，`benchmark.json:43-47` 明确标注 `"recorded_for_future_workflow_skill_specs": true`。
- 也就是说：这份"套件"实际测的是 `pre_merge_gate.py`/`gate_state_helper.py` 的**确定性 Python 分支逻辑**（`test_pre_merge_gate.GateCheckTests.*` 共 21 例 + `test_gate_state_helper.py` 22 例），由项目自己在同一 skill 的上一次落地（v1.19.0）中**明文裁定"对本 skill 做 LLM 行为 AB 不可行"并记为对未来同类 Spec 的约束性先例**。本 Spec 反过来引用它作为「存在专属 AB 套件」的证据，与该文件自己的第一方声明直接冲突。Spec 声称「原版从未核对该套件是否存在」暗示本版核对过——但核对结果如果读了 `benchmark.md` 就不可能得出「能 AB 测得到」的结论。

**发现 1b — `phase-c-integrator.json` 是真正的 AB 套件，但现有 3 个 eval 不覆盖本 Spec 改动的具体行为，且这个缺口已被同一套件上一次真实运行明确记录、未处理：**

- 3 个 eval（commit-generation / merge-conflict-handling / multi-remote-merge-push）分别对应 C.1 / C.2 / C.2.5，其 `prompt`/`expectations` 均未提及 `main_branch` 解析、`--remote`、`gate_error`、`not_applicable` 短路。
- `ab-results/2026-07-31-v1.65.0-122-rule6/grading-summary.md`（#122 / v1.65.0 的真实三臂 AB 运行，验证了这确实是能跑 AI subagent 的套件）里，eval-2 被评为「本次 change 定向观察面」，且确实测出了 with/old 两臂在 path_coverage 概念上的语义差异——**但该报告 §5 Caveats 第 1 条原话**：「定向新路径未被正面踩中：v1.65.0 核心新行为是 not_applicable 短路……套件内无『变更路径零 CI 覆盖』场景直接驱动短路+警告行产出。建议：ab-suite 补一条 not_applicable 正路径 eval（升 MINOR），或按 Rule #6 表 3 行以定向 fixture 补（spec 侧 rule6_note 留痕）」。
- 这条建议截至本 Spec 仍未被执行（`phase-c-integrator.json` 仍是 v1.1.0，changelog 最后一条是 2026-04-12，无 #122 或本 Spec 相关新增）。本 Spec 恰恰是把 `not_applicable` 短路作为核心新增行为之一（D-J / SC-10 / SC-11），却没有引用或处理这条已经明文记录在案、由项目自己审计流程产出的缺口。

**判据比对**（`skill-benchmark-exemption.md` §2 决策表）：

| 内容性质 | AB 套件能观测吗 | 落哪一行 |
|---|---|---|
| SKILL.md `:243`/`:167` 的 `--branch main` 字面量变更（"处方性·运行时指令面"这一步定性本身是对的，`:243` 确认逐字含 `aether ci status --branch main --in-flight --json` 且标注"无条件执行"） | **不能** —— 唯一专属套件自证非 AI 行为 AB；通用套件现有 3 eval 不覆盖，且缺口已被项目自己的上一次运行记录在案 | **第三行**，非 Spec 主张的第二行 |

第三行三件事核对（Spec 是否满足，§3 原文要求"缺一即回落照跑"）：

1. **点名行为**：**未做**。Spec 只点名了「D9 surface 措辞」缺口（proposal.md:287），这是另一个缺口（AI 该不该 surface 警告行的措辞分档），不是本条要害的「AI/操作者按 SKILL.md 指令解析主分支名 / 不硬编码 main」这个行为，也不是 grading-summary.md 已记录的「not_applicable 正路径未被踩中」这个更贴切的缺口。
2. **建定向 fixture**：**未做，且明确拒绝**——proposal.md:287「记录于此，不自行扩套件」是显式声明不做这件事。
3. **记套件缺口**：**部分做，但指向错误的缺口**——指向 #127（D9 措辞），未指向 grading-summary.md 已记录、与本 Spec 直接相关的 not_applicable 缺口，也未新开 issue 或引用 #122 audit trail 里的既有建议。

三件事里至少 2 件完全未满足（且第 3 件文不对题），按判据表本身的规则应回落"照跑"——这一点上 Spec 的**最终动作**（ship 前跑两套件）碰巧与回落结果一致，但**分类推理本身站不住**：它是以一个被源文件反证的假前提（"存在专属 AB 套件"）走的第二行"零裁量"路径，而非第三行"缺一回落"路径。两条路径终点相同，但记入项目历史的**先例陈述不同**——本 Spec 一旦以现状合并，会把「`phase-c-integrator-pre-merge-gate.json` 是可用于测 AI 行为的 AB 套件」这个假命题，作为 owner 已裁定（2026-08-08）先例写进 proposal.md 永久存档，供未来 Spec 误引（本项目对这类复合风险有专门成文纪律，见 memory `feedback_written_exception_exact_condition_match` 与 `feedback_spec_precedent_verify_execution_history`）。

**附带观察**：即便按 Spec 现有方案字面执行「照跑两套件」，`phase-c-integrator-pre-merge-gate.json` 一侧按其自身既定方法论（`benchmark.md` 记载的"structural verification"）实际就是重跑/扩展 `test_pre_merge_gate.py` 等单元测试并统计通过率——这与proposal.md:269 已经要求的「SC-1..12 baseline-failing 集合须于 Phase B 实跑留证」在效果上高度重叠。也就是说，"跑两套件"这个动作即使照办，也不会为 Rule #6 本来要盯的"AI 读了新指令行为有没有变好"这个维度提供任何 SC 之外的增量证据——这进一步印证了正确归类应是第三行而非第二行。

---

### 2. 其余合规面

**Rule #5**：Spec 文件位于 `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md`（主仓自身目录，非 `standards/openspec/changes/`）。✅ 合规。

**Rule #1 / Level 判定**：目录下只有 `proposal.md`，无 `tasks.md`，格式与声明的 Level 2 一致（`standards/openspec/project.md:21` Level 3 才要求 `tasks.md`+`detailed-tasks.yaml`）。范围核对：Impact 表（proposal.md:324-334）落点全部在 `phase-c-integrator` skill 目录内（`pre_merge_gate.py`/`test_pre_merge_gate.py`/`SKILL.md`/同目录 `path_coverage.py`，经核实 `path_coverage.py` 确实位于 `aria/skills/phase-c-integrator/scripts/path_coverage.py`，同一 skill），未跨 skill（`workflow-runner` 被显式排除在改动范围外，只留 follow-up）。**Level 数字（2）本身站得住**。

⚠️ **Minor**：proposal.md:5 的 Level 判定理由文字「单文件 + 其测试」在 R1 重写后已过时——实际落点是 4 个文件（代码/测试/`SKILL.md`/`path_coverage.py` docstring）+ 1 处外部 issue 编辑 + 2 条 follow-up issue。不影响 Level 数字，但佐证文字应同步。

**§引用卫生**（proposal.md:291-296，R1 M7 的修复）：**核验失败，发现新的引用失实**。

- 声称「§3 的『零证据不得当正证据』」是就地写出的判据本体——**全文检索 `proposal.md` 零命中「零证据」**，§3 实际正文里没有这句话或字面等价表述（§3 最接近的表述是"解析不出主分支名时闸门没有能力判断，正确输出是阻断而不是放行"，语义相关但非 Spec 自己引用的那句原文）。这是一处指向不存在内容的引用。
- 声称「判据见 `standards/conventions/` 的 fail-CLOSED 原则」——**核验失败**。`grep -rn "不变量写进文档\|枚举分区必须" standards/conventions/` 零命中；`standards/conventions/` 下含"fail-CLOSED"字样的三个文件（`configured-gate-authority.md`/`skill-benchmark-exemption.md`/`shell-jq-crlf-hygiene.md`）均无这条原则的字面陈述。经查，这条原则唯一的成文出处仍是容器本地 memory `feedback_invariant_needs_failclosed_default`——且我用 `forgejo GET /repos/10CG/aria-plugin/issues/137` 直接核实，**issue #137 原文本身就是用这个 memory 名字面引用的**（"本项目成文判据: memory `feedback_invariant_needs_failclosed_default` —— 「不变量写进文档 ≠ 写进兜底默认值; 枚举分区必须 fail-CLOSED」"）。
- 结论：本节意图消灭 R1 指出的"memory 名作承重引用"问题，但实际操作是把同一条 memory 的内容改写措辞后，挂到一个查无此内容的 `standards/conventions/` 泛指上——而不是按本节自己声明的另一条处置路径（"确需指向 Lab 内部经验时明确标注『Lab 内部，第三方不适用』"）诚实标注来源。这比直接写 memory 名更容易误导第三方读者（读者会去 `standards/conventions/` 里找这条原则而找不到，且不会意识到是文档错误）。**这正是本项目实证反复出现的模式——fix 轮最易在自己新写的内容里复发同形状缺陷**（本例甚至复发在"修复引用失实"这件事本身上）。

**§同形状兄弟位置**（proposal.md:309-318）：

- `phase-d-closer/scripts/fetch_gate.py:55` 实读确认：`_DEFAULT_BRANCH_FALLBACKS = ("master", "main")`，与 Spec 描述逐字一致。✅
- `state-scanner/scripts/collectors/sync.py:46-50` 实读确认：`_ORIGIN_HEAD_REFS` 含 `"refs/remotes/origin/master"`/`"refs/remotes/origin/main"` 两个候选，属同族但非逐字相同结构（sync.py 是"候选 ref 探测顺序"，非"字面量兜底"；docstring 明确自称"fail-soft，无 network"是有意设计，非隐藏缺陷）。Spec 原文措辞是"同族"/"同上"而非声称逐字相同，**这处表述是准确的，未夸大**。
- 枚举完整性：用 `grep -rlE '"main"'` 交 `"master"` 双字面量共现搜索 `aria/skills/*/scripts/*.py`，仅命中 `fetch_gate.py` 一处（sync.py 因字面量嵌在 `"refs/remotes/origin/main"` 路径里未被此严格模式捕获，但已通过直读确认存在）。未发现 Spec 未列出的第三处。**这只是 grep 模式匹配的尽力检查，非语义穷举，不能证明"确实只有两份"，但至少未证伪 Spec 的"已有两份"陈述。**

**D-K 版本号策略**（不预写字面量，落地时按 `plugin.json` 当前版本 patch+1 计算）：与 `standards/conventions/version-management.md` 核对无冲突——该文档 §2.3 将"缺陷修复/文档修正"归为 PATCH，与 D-K 的 PATCH 定性一致；§4.3 的"分发型组件"（aria 插件走 tag，VERSION 与 tag 严格一致）也不禁止"落地时才计算具体号段"这种做法，反而符合 CLAUDE.md 自身"版本 SOT = `plugin.json`"的精神，且能规避该文档 §4.3 提到的"非单调"历史教训类型。未发现冲突。

**外部记录 — aria-plugin #137**：`forgejo GET /repos/10CG/aria-plugin/issues/137`（只读）核实：issue body 当前**未加删除线**，原文首段仍逐字保留"两条腿在本项目上都不触发，且都失败为绿"的表述，也未见指向 comment 18015 的指针。**这与 Spec 的描述一致**——Spec 本就是把这个编辑动作列在 §Impact「落地时」执行，未声称现在已经做了，此项核验为"确认现状符合计划"，非缺陷。

**R1 数字核对**：proposal.md 状态行与 §R1 审计吸收记录声称"5 席 5/5 REVISE，聚合 verdict FAIL，去重后 5C+10M+6m=21"，经读取 `.aria/audit-reports/post_spec-R1-1786216818583-...-aggregate.md:44-61` 核实逐字一致。✅

---

## 轮次记录

| 轮 | 本席位 vote | 本席位 verdict | Critical | Major | Minor |
|---|---|---|---|---|---|
| R1 | REVISE | PASS_WITH_WARNINGS | 0 | 3 | 2 |
| R2 | REVISE | FAIL | 1 | 1 | 1 |

R1→R2 non-convergent：R1 本席位未发现 Critical，R2 独立重核 Rule #6 分类后发现 1 项新 Critical（结构性重写后 §Rule #6 整节为新写内容，且是本轮派发明确要求"从零重核"的项目）。此为本轮范围内的新发现，非振荡。
