# RESULT — Rule #6 AB `spec-drafter` (v1.69.1 Level 1 carry 批), 2026-09-04

- 套件 `ab-suite/spec-drafter.json` **v1.4.0** (4 evals; eval 4 为本批新建的定向 fixture)。执行 = skill-creator 流程 (八臂 subagent + 3 个独立 grader 席 + `scripts.aggregate_benchmark`)。工作区 `ab-workspace/2026-09-04-spec-drafter-rule5-path-hunkA/` (gitignored), 本目录 `runs/` 存八份 response / grading / timing 副本。
- 臂: `with_skill` = aria `fix/level1-batch-v1.69.1` 工作树; `without_skill` (= **old_skill** 语义) = aria master `2eca24b` 的 `skills/spec-drafter/` 快照。
- `ARIA_COORDINATION_NO_PUSH`: 本套件不触 phase1_gate / release_gate; 八臂 transcript 均确认零 git / 零脚本实跑 ⇒ 不适用。

## §1 结果

| 指标 | with_skill | without_skill (old) | delta |
|---|---|---|---|
| pass_rate | **100% (16/16)** | **81.2% (13/16)** | **+0.19** |
| time | 224.7s ± 52.8s | 181.9s ± 63.5s | +42.8s |
| tokens | 82296 ± 3694 | 80894 ± 4403 | +1402 |

| eval | 臂 | pass | form_ok | tokens | s | 失败断言 (截断) |
|---|---|---|---|---|---|---|
| eval-1-level-judgment | with_skill | 2/2 | True | 77355 | 156.8 | — |
| eval-1-level-judgment | without_skill | 2/2 | True | 75327 | 86.7 | — |
| eval-2-bilingual-support | with_skill | 5/5 | True | 85456 | 284.8 | — |
| eval-2-bilingual-support | without_skill | 5/5 | True | 86089 | 214.2 | — |
| eval-3-linked-issue-field-authoring-TARGET | with_skill | 5/5 | True | 81612 | 221.6 | — |
| eval-3-linked-issue-field-authoring-TARGET | without_skill | 5/5 | True | 80847 | 209.9 | — |
| eval-4-level2-proposal-location-rule5-TARG | with_skill | 4/4 | True | 84759 | 235.7 | — |
| eval-4-level2-proposal-location-rule5-TARG | without_skill | 1/4 | True | 81312 | 216.9 | 给出的落点路径是项目自己仓内的 `openspec/changes/<feature>/proposal; 全文任何位置都没有把 `standards/openspec/changes/` 当作本次 propos; 对 (2) 给出的理由点到「standards 是共享子模块 / 项目自己的变更归项目自己」这层语义 ( |

WITHOUT_BETTER: **0**。八臂 `form_ok=true`, 形态一致 (descriptive), 全部计入 delta。

## §2 预测 vs 实测 (PREDICTION.md, 写于八臂派出前)

| 项 | 预测 | 实测 | 判读 |
|---|---|---|---|
| with_skill | 12/12 (当时套件计 12 断言) | **16/16** | 一致 (断言总数因 grader 按 eval_metadata 逐条计而为 16) |
| eval 3 断言 4 (头部四行顺序) 会不会因 B8 软化而回归 | 预测仍 PASS, 但标为**本改动的风险点** | **PASS** (with 5/5) | **风险未兑现**: 软化文本逐字保留了四字段顺序且写明「从模板起草时自然满足」 |
| eval 4 old 臂 | FAIL 60–70% (可能靠 CLAUDE.md 的 Rule #5 自纠) | **1/4 全线 FAIL** | 低估了旧 skill 的推力: old 臂不但给了 `standards/` 路径, 还用**四条引用**为它背书 (A.1.4 明文 + Level 2 预览 `Location:` + LEVEL_GUIDE 两处示例), 并称「三处口径一致, 不是笔误」 |
| delta | +0.25 | **+0.19** | 方向一致; 幅度略低 (eval 1/2/3 saturate 在 100%/100%) |

## §3 区分力解读

- **区分力 100% 来自 eval 4** (old 1/4 vs with 4/4)。eval 1/2/3 两臂全过 = 对本 hunk 零区分度 —— 符合预期 (它们不断言落点路径), 保留作回归护栏。
- **grader 席抓到一个我漏掉的类级残留**: 我只改了 `SKILL.md`, 而 `LEVEL_GUIDE.md` (示例 1/2 共三条路径) 与 `LEVEL3_TEMPLATE.md` (存放说明) 仍写旧路径 —— 旧臂正是引用它们背书。**已补修四处, 并按「measure what you ship」重跑 eval 4 的 with 臂** (仍 4/4)。eval 1/2/3 的 with 臂是补修**前**跑的, 但那次补修只动落点路径面, 而这三个 eval 无一断言该面 —— 影响面为零, 未重跑, 此处明记。
- **eval 2 存在一个未被断言看见的真实 delta** (grader 席指出): 两臂产出里 old 臂的 proposal 预览逐字写 `Location: standards/openspec/changes/dark-mode/proposal.md` (Rule #5 违规) 却仍 5/5 —— 断言集不看路径。建议给 eval 2 补一条路径断言 (它本就生成 Level 2 proposal, 近零成本)。记 follow-up, 本轮不改 (改 eval ⇒ version.yaml 再升 MINOR)。
- **其余 grader 建议** (原文见各 `grading.json` 的 `eval_feedback`):
- [1/with_skill] Should explain why Level 1 was chosen — 「解释为什么」没有可证伪判据 —— 任何一句 'because it's a trivial typo' 都能通过, 两臂因此同分。建议改成点名式: 必须引用命中的 Level 1 触发词 (`typo`) **并**显式给出 Level 2/Level 3 触发词的反向零命中核对, 才算解释成立。
- [1/with_skill]  — 本 eval 对被测 hunk (Rule #5 路径落点) 零区分力, 但两臂在输出里确实分叉且无人检查: with_skill 主动写出 '一旦后续复核把等级抬到 Level 2/3, proposal 必须落到**消费方项目自己的** `openspec/changes/`, 不能写进 `st
- [1/without_skill] Should judge as Level 1 (Skip) for trivial fix — 断言只要求出现 'Level 1'。旧臂与新臂都命中, 且两臂几乎逐段同构 (同样的关键词表、同样的跨模块四否、同样的 score<3), 说明本 eval 对本次改动完全饱和。若继续留在套件里, 应作为回归护栏而非区分项, 并在报告里标注为 non-discriminating。
- [1/without_skill]  — 本臂输出里出现了一个应当被抓到但无断言覆盖的行为: 「若被升级为 Level 2 时的产出位置 (仅备查)」段写 'Level 2: standards/openspec/changes/{feature}/proposal.md' —— 正是 Aria 不可协商规则 #5 禁止的落点 (项目变更写
- [2/with_skill]  — 没有任何断言检查 proposal 的落点路径, 而两臂恰恰只在这里分叉 —— 本臂写 'openspec/changes/dark-mode/proposal.md ... **不要**写成 `standards/openspec/changes/dark-mode/` ... (Aria 不可协
- [2/with_skill] Should correctly parse mixed Chinese/English i — 'correctly parse' 无可证伪判据 —— 一个只读英文侧、完全无视中文侧的回答也能被判『解析正确』。建议钉到可观测事实: 必须显式陈述两侧是同一需求的中英表述 (而非两条并列需求), 或指出两侧语义差集。
- [2/with_skill] Generated proposal header blockquote contains  — 断言 4/5 (Linked Issue 字段) 在旧 skill 快照里已成文 (snapshot SKILL.md 同样要求该字段与 `none` 哨兵), 因此两臂必然同过。作为回归护栏有效, 但对本次 hunk 无区分力, 报告中宜标注 non-discriminating, 以免『5/5 
- [2/without_skill]  — 本臂以 5/5 满分通过, 却在 A.1.4 预览框里写出 'Location: standards/openspec/changes/dark-mode/proposal.md' —— 把项目自身的功能变更落到共享子模块 standards, 正是 Aria 不可协商规则 #5 禁止的行为, 也正
- [2/without_skill] Should preserve the feature intent from both l — 'preserve the feature intent from both language inputs' 在两侧互为翻译时是恒真的 —— 只读一侧也能保住全部意图。要让它有判别力, 输入应改成两侧信息不对称的双语对 (例如中文侧多一句「跟随系统」), 再断言该单侧约束出现在英文 proposa
- [3/with_skill] 该行不是 markdown 链接形 (行内无 `](http`), 且不留空 — 该断言被 #2 蕴含: 值一旦逐字为 inline code span `none`, 就不可能同时是 markdown 链接形或空值。两臂均自动满足, 零区分力。若想测链接形回避, fixture 需给一个真实 issue 号 (值非 `none` 时才有构造链接形的动机)。
- [3/with_skill]  — 本 eval 在本 iteration 两臂 5/5 全过 (OLD-SKILL 臂逐字写出 `> **Linked Issue**: `none`` 并主动排除 N/A/TBD/-), 即目标行为在旧版 SKILL.md 里已被「proposal.md 头部字段要求」段覆盖 ⇒ 该 eval 对本
- [3/with_skill]  — 没有任何断言检查 Level 2 判定的产出物边界 (只出 proposal.md、不出 tasks.md)。两臂都做对了, 但一个把 tasks.md 也吐出来的错误输出仍能 5/5 通过。
- [3/without_skill]  — OLD-SKILL 臂 5/5 全过 —— 该 eval 对本次 hunk 的区分力为 0。旧 SKILL.md 已含「proposal.md 头部字段要求」全部三条写法, 两臂输出在被断言的字段上逐字节等价。作为 TARGETED eval 它当前测不出新旧差异, 建议重新定靶或标注为 basel
- [3/without_skill] 头部四行顺序 Level → Status → Created → Linked Issue — 断言只要求四行顺序与含 Created 行, 但没有要求这四行必须是**连续**的头部 blockquote (中间插入 `> **决策来源**:` 等行仍会通过), 也没有钉 `Level` 的取值形态。若顺序/连续性是机械 check 的判定输入, 值得写死。
- [4/with_skill]  — No assertion covers a discriminating Level 2 behavior that this run did get right: Level 2 must produce proposal.md ONLY, with no tasks.md. The respon
- [4/with_skill] 全文任何位置都没有把 `standards/openspec/changes/` 当作本次  — The counterexample carve-out is judgment-dependent, so two graders can split on a hedged answer (e.g. "也可以放 standards/openspec/changes/，看团队约定"). Consi
- [4/with_skill] 给出的落点路径是项目自己仓内的 `openspec/changes/<feature>/pr — As literally worded, a bare `openspec/changes/x/proposal.md` with no anchor would pass, leaving ambiguous whether it means the todo-web root or the st
- [4/without_skill] 对 (2) 给出的理由点到「standards 是共享子模块 / 项目自己的变更归项目自己」 — 本臂是该断言的边界样本: 它在「留痕」段说出了「standards 是共享子模块 / 项目自身变更该落哪一侧」这层语义, 却把它当作待 owner 复议的不确定性, 而非选路理由。若断言意图是「理由必须支撑正确落点」, 建议改写为「第 (2) 段为**所选**路径给出的理由中至少一条援引规则 #5 
- [4/without_skill]  — 本 eval 区分力良好 (with 4/4 vs old 1/4), 且失败模式可直接归因: OLD-SKILL 臂逐条引用旧 SKILL.md A.1.4 / Level 2 预览 Location / LEVEL_GUIDE 两处示例共四处 `standards/openspec/change

## §4 污染面 / 已知限

- 两臂均自动注入主仓 `CLAUDE.md` (其中含 Rule #5 原文) —— old 臂**有**自纠的知识条件却没自纠, 反而被 skill 内的四处字面推向错误答案。这条比「基线不知道规则」更有说服力: 区分力来自**skill 文档主动误导 vs 主动纠正**, 不是知识有无。
- **harness 缺陷 (本轮实测发现, 已处置)**: 首轮 eval 1 的基线臂把目录名 `without_skill/` 读成「不加载任何 skill」, 拒绝读旧版快照, 与其余三条基线臂形态不一致。该产物已标 `response.INVALID-no-skill-read.md` 并用显式说明「这是 OLD-SKILL 臂, 目录名只是聚合脚本要求」的 prompt 重跑。**后续跑 AB 时 prompt 必须显式声明臂身份, 不能靠目录名传达。**
- 单 run/臂 (n=1), 无方差估计; `without_skill` 的 ±38% 是 4 个 eval 之间的离散 (eval 4 拉低), 不是重复实验方差。

## §5 结论 (Rule #6)

- 路径勘正 + hunk A 软化两处均为**处方性 · 运行时指令面** ⇒ 照跑 AB, 零裁量。`delta.pass_rate = +0.19 > 0` ⇒ **通过**, 不申请豁免。
- eval 4 是判据表第三行要求的「可证伪定向 fixture」, 套件缺口 (spec-drafter 套件对落点路径面零覆盖) 随该 eval 在本批闭合, 故不另开 issue。
- 未拆条、未改既有 expectations 迁就结果; `version.yaml` 停在 1.4.0。
