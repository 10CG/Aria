---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T12:30:05.636Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead]
---

# post_spec Round 3 — tech-lead 席 (被审 SHA 0c41e53, rework v3)

> 只审不改; 除本报告外未写任何文件。独立性: 开审时同目录已出现 qa-engineer 的 R3 报告, 未读。R1 / R2 各席报告只用于核对「Layer 2 / AD10 以前有没有人提过」(结果: 没人提过)。

## R2 对账

我席 R2 共 9 条 (major 4 / minor 5)。结果: **closed 8 / partially 1 / open 0**。

| R2 条 | 严重度 | 判定 | v3 落点 (段名) 与核实 |
|---|---|---|---|
| 1 负控「+4 ⇒ p 约 0.03」 | major | **closed** | §D2「同批负控」改为绝对门槛: 负控 query 级命中 ≤ 5/10, 并写明「门通过时被评必为 10/10, 10 对 5 单侧 p = 0.016, 10 对 6 为 0.043 不取」。用 math.comb 重算, 两个数都对 (核实记录 1)。「门通过 ⇒ 被评 10/10」的推理成立, 因为通过门要求每条 should-trigger ≥ 0.5。「被评退化先判 fail、不落作废」同时关掉了 R2 聚合第 2 条 (严重退化被判作废, 逃过 FAIL)。相邻的新问题: fail 分支本身没有后果 → Finding 1。 |
| 2 OQ-6 代价无来源 | major | **closed** | §OQ-6 改为引用 `ab-results/2026-09-04-v1.69.1-spec-drafter-rule5-hunkA/` 下 8 个 timing.json: `duration_ms` 合计 1,626,592 = 27.11 分钟, `total_tokens` 合计 652,757 ≈ 65 万, 与文中一致。「成本未记录」如实, 没有来源的「15 美元」已删 (核实记录 4)。口径核: hunkA 跑的是 spec-drafter 套件 v1.4.0 全部 4 条 eval × 两臂 = 八臂, 确实是「单 skill 场景 1 AB」。 |
| 3 OQ-3 × OQ-7 耦合 | major | **closed** | §OQ-7 把「首次建套件」和「新套件要不要 owner 审阅」合并成 A / B 两案, 各给代价, 推荐 A, 并写明「owner 不在线即阻塞」。§D2 套件条补了「新套件是否须 owner 审阅后才能作门, 见 OQ-7」, §Impact 补了「若须 owner 审阅另加 owner 时间」。R1-4 的原命题 (硬阻落在 owner 可用性上) 已作为待裁代价如实交给 owner, 符合 Rule #10。相邻的新问题: A 案在 v2.0 自主运行时与 AD10 冲突 → Finding 3; B 案的时长数字过期、值域缺 `provisional` → Finding 5。 |
| 4 与 `10CG/aria-standards#17` 分工 | major | **closed** | 落点: §D1「本条只管深度, 不管广度」+ §D5.5 分工 + T7 留言 + SC-6 核留言。实读 #17 (open, 0 条评论, 最后更新 09-06), 它提议「照跑 = 该 Skill 的全套件 + 针对 hunk 的定向 fixture; Tier 1 全量只在跨 Skill 共享组件变更或发版审计时要求」。这确实属于广度轴, 与 §D5.5 的描述一致; 唯一交叉点 (混合改动) 已点名。standards 仓 2026-09-01 以来没有任何 ref 改过这份 SOT, 目前没有并行编辑 (核实记录 12)。 |
| 5 SC-2 不可 `test -e` | minor | **partially** | §D3 表里的省略号和通配已全部换成完整相对路径, 10 个路径拼上基线目录后都存在 (核实记录 8); SC-2 也补了「恰六行 / 恰一行 `[配置推导]` / 零行判红」。没闭合的部分: T2 写「机读实证写全路径」, 与 §D3「路径均相对基线目录」、SC-2「拼上基线目录后 `test -e`」互相矛盾 → Finding 4。 |
| 6 §D4 无机械 enforcement / 寄居 §4 | minor | **closed** | 在 SOT 新起 §4.1; 「无机械 enforcement」写进 §D4, 并列为 §D6 第三条局限。 |
| 7 手册「边界三条」计数语 | minor | **closed** | §D1 表第三行改成「边界四条」, 按 ` / ` 分项数得 4; SC-7 核「边界四条」= 1 且「边界三条」= 0。旧句 `grep -F` 命中手册第 480 行。 |
| 8 T5 与 version-management §5.1 | minor | **closed** | 文件头 ship target 声明「这是单份规范文档自己的版本行, 与 §5.1 待裁的 standards 仓级版本自称正交」。实读 §5.1: 待裁的是 `standards/openspec/project.md` 写的 2.2.2 和主仓 VERSION 子模块表写的 v2.2.3 这两处仓级自称。SOT 文件头的 `**Version**` 行不属于这一类, 「正交」成立。 |
| 9 作废无重试上限 | minor | **closed** | §D2 写明「连续 2 轮作废 ⇒ 升级 owner (AI 不得自行豁免, Rule #10)」; SC-9 核「连续 2 轮」。 |

## Findings

- [major] implementation/proposal.md §D2+§D4 (issue): 门的 fail 分支没有后果。D4 把 `<结果目录> fail` 列为合法取值, 却只把空 / not_required / n/a 判为不合规、只把 void 判为不得 ship; D2 也没写 fail ⇒ 不得 ship、改 description 后重跑、不改能否重跑。按字面读, 记下 fail 就算合规、可以 ship。
- [major] architecture/proposal.md §D1 只改 description 不跑场景 1 (decision): 「触发面 / 行为指令句」的定义只写在 proposal 里, SOT 新句没带, CLAUDE.md 与手册的新句连这条分支都没有; 能力陈述句 (本 Spec 基线的真实改动就属此类) 两类都不沾; 也缺 SOT §2 对同类放宽要求的逐行点名。「拿不准照跑」挡不住系统性误读。
- [major] architecture/proposal.md §Impact+§OQ-7 (risk): 没覆盖 v2.0 Layer 2。aria-runner-bot 已在 aria-plugin 自主提交 33 次 (含改 SKILL.md 与发版), 规则 #6 同样约束它。OQ-7 推荐的 A 案在自主运行时等于多出一个 AD10 之外的人工 gate; 4b 的前置、时长、成本全部来自 Claude 实测, 而 Layer 2 底层是 GLM via Luxeno, 没有验证过。
- [minor] testing/proposal.md §SC-2 (issue): T2 要求「机读实证写全路径」, D3 却规定「路径均相对基线目录」, SC-2 又按「拼上基线目录后 `test -e`」判定。照 T2 写全路径, SC-2 拼出的路径不存在, 恒红; 照 D3 写, 又违反 T2。任务与验收互相矛盾, 进 Phase B 前必须统一。
- [minor] documentation/proposal.md §OQ-7 (issue): B 案的重跑代价还是 v2 的「约 12–14 分钟」, v3 其余各处 (Impact / OQ-3 / RESULT v3) 已改为 11–18 分钟, 数字对不上; B 案要求 rule6_note 标 `provisional`, 但 D4 的 `scenario4b` 值域里没有这个值, owner 若选 B, 模板没地方写。

## 新问题检查 (逐项回答任务 3, 并给出 Findings 的论证)

### 作废语义、`void` 取值与 Tasks 是否对齐 (对应 Finding 1)

- **void 这条线是对齐的**。§D2 写清了触发条件 (门通过且负控 ≥ 6/10)、后果 (义务未完成, 不得 ship)、动作 (修套件或环境后重跑) 和上限 (连续 2 轮升级 owner); §D4 给出 `<结果目录> void` 取值并重申「不得 ship」; T2 / SC-9 核「≤ 5/10」和「连续 2 轮」, T3 / SC-3 核值域含 `void` 与 `n/a`。
- **fail 这条线是断的**。值域里的 `fail` 从 v2 就有 (v2 写作 `pass|fail`), 当时的合规规则同样没说 fail 的后果。v3 给 void 补上「不得 ship」, 把合规规则写成了一张明确的清单: 空 / `not_required` / `n/a` 不合规, `void` 不得 ship。fail 不在清单上。明确列出一部分, 就等于默认排除了没列的, 所以这张清单反而让 fail 的空缺更显眼。§D2 对 fail 只说了「门先判 fail」, 没写之后怎么办。对照手册现行的场景 1: 有「验收: delta.pass_rate > 0」和 Verdict 表里的「WITHOUT_BETTER ⇒ 必须修复或移除」。4b 作为一道「门」, 缺的恰好就是这一句。SC 层面也没有一条去核「fail / 作废 ⇒ 不得 ship」有没有写进手册 §4b。
- 修法 (纯文字): §D2 加一条「fail ⇒ 本 cycle 不得 ship; 改 description 后, 被评与负控两臂整批重跑; 不改 description 直接重跑须在 rule6_note 写明理由, 以最后一轮为准」(重跑规则由 owner 定, 这里只要求写明); §D4 合规规则补上 fail; SC-9 补核「不得 ship」。
- 附带 (观察, 不计 finding): 「先判 fail」会把环境原因造成的整体压低也判成 fail。拿 v1 数据按 v3 规则回放: new 各条 query 最高 1/3 ⇒ query 级 0/10 ⇒ 门 fail; 负控 0/10 ≤ 5 ⇒ 不作废 ⇒ 结论是「description 改坏了」, 而真实原因是共用根 + 4 worker 的环境缺陷 (核实记录 14)。判 fail 是偏保守的方向, 本身不危险; 但没有重跑规则的话, 很容易变成「重跑到过为止」。基线当时本来就同批跑了旧版 description, 如果把旧版固定为同批对照, 规定「旧版也 fail ⇒ 作废」, 就能把环境造成的整体压低和 description 退化分开。

### §D1「description 里的行为指令句按指令 hunk 照跑场景 1」能不能判 (对应 Finding 2)

- **定义没有写进规范本身**。两类的定义 —— 触发面 = 「何时使用 / 使用场景 / 触发短语」, 行为指令句 = 「要求执行方式的句子, 如『不要自己手工 mv』」—— 只写在 proposal 的 §D1 正文里。T1 要逐字落地的 SOT 新句只有「只涉及触发面时不跑场景 1 …, 含行为指令句的部分按指令流程 hunk 照跑场景 1, 拿不准照跑」, 两个词都没定义。CLAUDE.md 和手册的新句更简略, 只有「description ⇒ 4b / 指令流程 ⇒ 场景 1」, 连「description 里的行为指令句 ⇒ 场景 1」这条分支都没有。proposal 归档之后, 执行者手里只剩一句不带定义的 SOT。
- **拿本 Spec 自己的真实改动试判**: v1.71.1「…到正确的 archive/ 目录，自动修正 CLI bug」→ v1.73.0「…到 openspec/archive/ 目录，并做归档后落点校验」(取自 run.log 的 `Evaluating:` 行)。它既不是「何时使用 / 使用场景 / 触发短语」, 也不是祈使式的执行要求, 而是**能力陈述句** (说技能做什么)。按 proposal 的定义两类都不沾, 只能落到「拿不准 ⇒ 照跑」。这说明「不跑」这条放宽实际上只覆盖「改动全落在使用场景子句里」的情形, 比 OQ-6 交给 owner 裁的范围窄, 但文本里没说出来。
- **「拿不准照跑」够不够兜底**: 不够。它只在执行者**意识到自己拿不准**时才起作用。§D1 自己写着 description「决定 skill 何时被激活」; skill-creator SKILL.md 第 67 行写的是「description: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it」—— 连「做什么」都算进触发机制。按这个框架, 执行者会把整段 description 都当作触发面, 得到的是**有把握的错判**, 兜底根本不会触发。这是有方向性的系统误读, 不是偶然失误。而 skill-creator 与 proposal 的分歧, 恰好就落在能力陈述句这一类上。
- **缺少同类放宽已有的约束**: SOT §2「SKILL.md 有变动时的附加约束」对一个同类的放宽 (事实性同步可落第一行) 要求「在 spec 里逐行点名该变动并声明非指令语义变更」。§D1 的「不跑场景 1」放宽得更多, 却没有这一要求; §D4 的 `scenario1: not_required` 也没有写理由的位置。
- 修法 (纯文字): 把 SOT 新句改成按**位置**判断的封闭清单 ——「改动行全部落在『使用场景 / 何时使用 / 触发短语』子句内, 才不跑场景 1; 其余 (含能力陈述句) 一律照跑」; 不跑时, 在 rule6_note 逐句引用改动行并声明「只涉及触发面」; CLAUDE.md 与手册的新句补上「细则见 SOT §2」。同时写好 OQ-6 被否决时三处的替代定稿句。

### OQ-4 的新写法是否如实反映 LEVEL_GUIDE §跨模块判断 (不计 finding)

实读 `aria/skills/spec-drafter/LEVEL_GUIDE.md` §跨模块判断: 「跨模块条件 (满足任一)」共四条 —— 涉及 2 个及以上模块 / 修改 shared/ 目录 / 需要 API 契约变更 / 影响多个子模块 —— 下接「跨模块 → 自动提升为 Level 3」。OQ-4 引的结论句和第一条都是逐字的, 「条件之一」这个说法也如实。按该指南的模块映射 (mobile / backend / shared / standards; standards 的路径是 `standards/**` 与 `.claude/**`, 关键词含「规范 / 文档」), 本 Spec 只落在 standards 一个模块, 成立。OQ-4 没引的另外三条我逐条核过: 仓根没有 `shared/`; 不涉及 API 契约; 子模块只有 standards / aria / aria-orchestrator 三个, `aria-plugin-benchmarks/` 是普通目录 (`ls-tree` 模式 040000), 本 Spec 只动 standards 一个子模块。三条都不成立, 省略它们不影响结论。**判定: 如实。** 另有两点小瑕疵, 放在观察段。

### 另一处新发现: v2.0 自主运行时 (对应 Finding 3)

- 约束关系: CLAUDE.md 写明「v2.0 严格遵守全部 10 条不可协商规则 (由 Layer 2 内 aria-plugin 执行; 自主运行时无人复议, Rule #10 更硬)」。
- 不是纸面问题: `aria-runner-bot` 在 aria-plugin 仓有 33 个提交, 其中有两次发版 (v1.70.0 / v1.65.3), 至少 6 个提交改过 `skills/*/SKILL.md`, 其中 `3b102a0` 改的正是 openspec-archive (核实记录 13)。
- 冲突一 (AD10): AD10 原文是「只保留 1 个人类审批 gate, 位置在 S7_AWAITING_MERGE …… 不在 dispatch 前 (S1→S2) 设 human gate, 不在 review 中段 (S5→S6) 设 human gate」, 并以「违反自主 SDLC 前提」否决过多加一个人工 gate 的方案 (其 Option A)。OQ-7 推荐的 A 案要求「套件审过才能作门」。放到 Layer 2 里, 改 41 个无套件 skill 中任何一个的 description, 都要在 S7 之前停下来等 owner 审 20 条 query。自主模式下 Rule #10 更硬, Layer 2 不能自行豁免, 结果只能是卡住。B 案 (先暂定运行、owner 事后审) 与 AD10 相容, 但 OQ-7 没从这个角度写两案的代价。
- 冲突二 (测量基础): 4b 的前置 (`--setting-sources project`、显式 `--model`)、时长 (11–18 分钟) 和成本 (单次约 0.08 美元) 全部来自 Claude 实测。Layer 2 的底层模型是 GLM (glm-5.2) via Luxeno (CLAUDE.md 项目状态段), 这个后端的延迟是 45–54 秒 (Blocker 4)。按 `--timeout 120`、单 worker、一臂 60 次调用算, 单臂时长可能是 Claude 下的好几倍, 而且触发行为也换了模型。这些都没验证过。
- 覆盖情况: proposal 全文 grep「Layer / v2.0 / AD10 / 自主 / runner / GLM / Luxeno」零命中; aria-orchestrator/docs 里也没有「Layer 2 怎么执行 Rule #6 AB」的约定; R1 / R2 共 12 份审计报告都没提过。
- 修法 (纯文字, 不用重跑): §Impact 加一条说明 Layer 2 的影响; OQ-7 的 A / B 两案各补上「在 v2.0 自主运行时的后果」; 4b 在 Layer 2 下是否适用, 写进 SOT §6 局限, 或另开 issue。

### 两条 minor 为什么列为进 Phase B 前必须改

- Finding 4: 任务和它自己的验收互相矛盾, Phase B 执行者只能二选一 —— 照 T2 做, SC-2 恒红; 照 SC-2 做, 又违反 T2。这类冲突在 Phase B 最容易被「改测试迁就实现」悄悄吸收掉。
- Finding 5: OQ-7 要由 owner 在 Phase B 之前裁定。其中一个数字对不上 (按本轮要求, 核不上的数字要列为 finding); 而且 owner 选 B 时, §D4 模板没有可写的值, Phase B 只能临时自己编一个。

## 观察 (不进收敛比较键, 不影响 vote)

- 串行「约 22–34 分钟」: 按单臂 10m39s–17m39s 翻倍, 精确值是 21m18s–35m18s, 与并行「约 11–18」的取整方式不一致 (同一取整方式应为约 21–35)。另外, 各臂时长是在 4 路 (v2 / v3) 或 2 路 (v4) 并发下测的。近似成立, 不计 finding。
- OQ-8「一臂约 12 分钟」: 同配置的 v4 两臂实测是 13m38s / 13m54s, 写「约 14 分钟」更准。
- OQ-4「post_spec 每轮约半小时, R1 / R2 实测」: 按文件时间, R1 约 25 分钟 (17:36 → 18:01), R2 约 54 分钟 (11:08 → 12:02, 含额度中断后重派)。写「25–55 分钟」更准。
- 与 OQ-4 相关的两点: LEVEL_GUIDE 决策树 Q2 还列了「架构变更 / Breaking」, OQ-4 没讨论。抬头写「owner 2026-09-13 指示开 Level 2 cycle」, 但仓内找不到可追溯的记录 (#211 仅有的一条评论 23915 是 triage 稿里的「属 Level 2 规范变更」, latest.md 里也没有本轨记录); 文末的 Rule #10 清单却仍写「Level 2 自判 (OQ-4)」。两处只能保留一种说法; 如果确实是 owner 指示, 最好注明出处。
- `decision_table_row` 只能填一个值: SOT §5 自己的样例 #113 在同一个 cycle 里, 两个文件分别落在第一行和第三行, 单个值写不下。建议注明「可多值, 如 `[1, 3]`」。
- SC-5 正则的 20 字窗口会漏掉自然写法: 「被评 description 的 should-trigger 命中 ≥ 旧 description」这句 (主语到比较符之间隔 33 个字符) 等三个正样本都是 0 命中。窗口放宽到 `{0,40}` 后, 五个正样本全部命中, 而 §D2 正文 (去掉「不设比较判据」那行) 仍是 0 命中 (核实记录 15)。SC-5 是「计数 = 0」型检查, 漏报就是假绿。建议放宽窗口, 并把这类长主语句加进自测样本。
- D5.3 后续 AB 的 baseline 污染: §D4 在过渡期靠 CLAUDE.md 里的「字段见 SOT §4.1」传达模板, 而 CLAUDE.md 会自动加载进 without_skill 臂。这样 D5.3 (给 spec-drafter / task-planner 加五字段) 跑场景 1 时, 两臂都会产出五字段 —— 正是 SOT §6 第一条和 aria-plugin #116 描述的情形。建议在 D5.3 的 issue 正文里预先写明: 用定向 fixture; 三臂全过时, 按 §6 第二条先做语义分档, 避免「baseline 也过就删断言」。
- §D5.1「4a 原样保留」会连带保留手册现文「触发时机: 修改 Skill 的 description/frontmatter 后」, 这与「4a 是可选优化, 4b 才是义务」相矛盾。建议把 4a 这一行改成「可选; 产出须过 4b」。
- 引用写法: §D1 的 SOT 新句写「见 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 4b」, 没加「Aria 主仓」前缀, 而同一份 SOT 里 §D6 加了。RESULT v3 要求引用时写成「v3 @ <SHA>」, §D6 只写了 v3 (SHA 已知是 0c41e53)。
- 设置源隔离带来的附带差异: 两份探针的 `thinking_tokens` 是 1184 对 0。原因没核实 —— 可能是任务难度不同 (数 97 个 vs 数 12 个), 也可能是 project-only 不加载用户级的思考设置 (读用户级设置文件被 secret-guard 拦截, 我没有绕过)。如果是后者, 4b 就是在和交互会话不同的思考配置下测触发, 与 §D3 第 4 条「连带换掉默认模型」是同类问题, 应记进 RESULT 的局限。
- OQ-6 备选代价 (子代理累计分钟 + token) 和 4b 代价 (墙钟分钟 + 美元) 用的是不同的量纲。4b 两臂的累计时长约 21–35 分钟, 与 27.1 分钟在同一量级, 把两者并列写出来更方便 owner 比较。另外, hunkA 当时 spec-drafter 套件是 4 条 eval, 现在已经 6 条, 按同样口径今天约是 1.5 倍。
- Tasks 里只有 T4 挂了 OQ-3 门; T1–T3 和 T5 都没声明依赖 OQ-5 / OQ-6 的裁定。建议加上「T1 前置: OQ-5 / OQ-6 已裁」。
- 生效点: 「已 ship 的 rule6_note 不回溯」没有覆盖在 ship 那一刻正处于 Phase B / C、且含 description 改动的在途 cycle (并发轨和 aria-runner-bot 都可能有)。建议写明「生效点 = T7 gitlink bump 进入主仓 master; 此后进入 C.2 的 cycle 适用」。

## Verdict

PASS_WITH_WARNINGS —— critical 0 / major 3 / minor 2 (都是本轮新发现, 或 R2 未完全闭合的; R2 的 4 条 major 全部 closed)。

我席 R2 的 9 条闭合 8 条、部分闭合 1 条。4 条 major 全部闭合, 数字都能机械复核: 负控门槛和两个 p 值、OQ-6 的 27.1 分钟 / 65 万 token、各臂时长、探针字段、skill 计数, 逐一对上。唯一对不上的是 OQ-7 B 案沿用了 v2 的「12–14 分钟」, 已列为 Finding 5。这一轮数据层面是干净的。

仍然投 REVISE, 是因为三条新的 major。它们都出在**门的判定语义和适用范围**上, 不在数据上:

- 门判 fail 之后该怎么办没写, 而且 §D4 的合规清单让 fail 读起来像是合规的;
- 「只改 description 不跑场景 1」这条放宽的判据没有随规范一起落地, 「拿不准照跑」挡不住系统性误读;
- OQ-7 的推荐案在 v2.0 自主运行时与 AD10 冲突, 4b 的测量基础在 Layer 2 下也没验证过, 而这个仓的 Layer 2 已经在改 aria-plugin 的 SKILL.md。

三条都只需要改文字, 不需要重跑基线。

## Vote

REVISE

## 数据核实记录

核实方式: 全部直接读原始产物重算 (json.load / run.log 时间戳 / git / forgejo API), 不拿 RESULT.md 里的数字当依据。

1. **Fisher (math.comb 超几何分布, 单侧 = P(X ≥ 10))**: 10 对 5: C(15,10) / C(20,10) = 3003 / 184756 = **0.016254** → 文中 0.016 ✔; 10 对 6: 8008 / 184756 = **0.043344** → 0.043 ✔; 10 对 3 双侧 **0.003096** → §Why / RESULT 的 0.0031 ✔。附: 10 对 4 单侧 0.005418, 10 对 7 单侧 0.105263。
2. **run.log 各臂时长 (脚本解析起止时间)**: v2 new 11m26s / poscontrol 15m46s / negctrl 16m30s / old 17m39s; v3 old 10m39s / poscontrol 11m06s / new 11m07s / negctrl 12m03s; v4 overbroad 13m38s / realroot 13m54s。10 臂区间 **10m39s–17m39s** ✔ (RESULT 分轮区间「v2 11m26s–17m39s / v3 10m39s–12m03s / v4 13m38s–13m54s」逐项 ✔)。两臂并行 ≈ 较慢的那一臂 = 10.65–17.65 分钟 → 「约 11–18」✔; 串行 = 翻倍 = 21.3–35.3 分钟 → 「约 22–34」近似 (见观察)。v1 (共用根, 4 worker) 各臂 3m20s–4m14s, 配置不同, 没计入是对的。
3. **探针 json 的 `usage` 字段**: default: `cache_creation_input_tokens` **27065**, `cache_read_input_tokens` 10126, `output_tokens` **1190** (其中 `thinking_tokens` 1184), `total_cost_usd` 0.6043545; project: **3696** / 13700 / **5** (thinking 0) / 0.078603 ✔。27065 − 3696 = 23369 ≈ 「多约 2.3 万」✔。口径说明: 两边输入总量 (创建 + 读取) 相差 37191 − 17396 = 19795, 约 2.0 万; 「cache 创建多 2.3 万」按字面成立。
4. **hunkA 的 8 个 timing.json**: `duration_ms` 合计 1,626,592 = **27.11 分钟** ✔; `total_tokens` 合计 **652,757** ≈ 65 万 ✔。hunkA 的 RESULT.md 确认: 套件 v1.4.0 共 4 条 eval, 八臂 subagent, 每条 eval 每臂跑一次。benchmark.md 抬头写的「3 runs each」与 8 个 timing 文件、与「81% ± 38%」的离散度 (恰为 4 个数据点) 都对不上, 应是生成器的模板字样, 不影响求和。当前 `ab-suite/spec-drafter.json` 为 6 条 eval。
5. **skill 数**: `ls /home/dev/Aria/aria/skills/*/SKILL.md | wc -l` = **42** ✔; 目录共 43 个, 唯一缺 SKILL.md 的是 `issue-triage-workspace` ✔。`ab-suite/trigger/` 不存在; 在全仓 (基线目录除外) grep 含 `"should_trigger"` 的 JSON, 结果为 0 ⇒ 「现有 trigger 套件 0 个」✔, 42 − 1 = 41 ✔。
6. **记分重算 (逐 query 累加原始 json)**: v3 new / old / poscontrol 都是 should 30/30 (query 级 10/10)、should-not 0/30; negctrl should **8/30 (3/10)**; v4 overbroad should 30/30、should-not **22/30 (7/10)**, 整体 pass = False; realroot 30/30、0/30 ✔。与 §Why、§D2「基线 v3 负控 3/10」一致。
7. **`run_eval.py` 的 `did_pass`** (插件缓存三份副本第 230–234 行相同): should_trigger 为真时是 `trigger_rate >= trigger_threshold`, 否则是 `trigger_rate < trigger_threshold` ✔, 与 §D2 的「通过」定义一致。
8. **§D3 表的 10 个路径**: 拼上基线目录后全部存在 (与目录清单逐一比对) ✔。
9. **三处旧句与 SOT 锚点**: CLAUDE.md 第 110 行 ✔、SOT 第 33 行 ✔、手册第 480 行 ✔ (逐字); SOT §4 那句在第 55 行 ✔; SOT 第 71 行「两个已知缺陷」✔; SOT 第 3 行「> **Version**: 1.0.0」✔ (SC-7 的 `grep -cF '**Version**: 1.1.0'` 改后能命中); 手册「### 固定测试集 vs 临时测试」在第 81 行 ✔ (R2 聚合第 30 条的锚点问题已修)。
10. **OQ-7 B 案「约 12–14 分钟」**: 与 v2 proposal §Impact 的「并行约 12–14 分钟」一字不差, 而 v3 的 §Impact / §OQ-3 / RESULT v3 都已改成 11–18 分钟 ⇒ rework 时漏改, **核不上** → Finding 5。
11. **LEVEL_GUIDE §跨模块判断**: 见「新问题检查」。仓根没有 `shared/` (ls 报不存在); `.gitmodules` 只有 standards / aria / aria-orchestrator; `git ls-tree HEAD aria-plugin-benchmarks` 模式为 040000 (普通目录)。
12. **`10CG/aria-standards#17`**: API 返回 state = open, comments = 0, updated 2026-09-06, 正文如 R2 对账第 4 行所引; standards 仓 `git log --all --since=2026-09-01 -- conventions/skill-benchmark-exemption.md` 为空。
13. **Layer 2 相关**: AD10 原文见「新问题检查」(`aria-orchestrator/docs/architecture-decisions.md` §AD10); proposal grep「Layer|v2.0|AD10|自主|runner|GLM|Luxeno」= 0; aria-orchestrator/docs 里没有 Rule #6 AB 的执行约定; `git -C aria log --all --author=aria-runner-bot` 共 33 个提交, 含 `bae4ad8` (v1.70.0 发版)、`cf43551` (v1.65.3 发版); 改过 `skills/*/SKILL.md` 的至少 6 个 (`17cd3d0` / `e3d54f3` / `ae35d19` / `c8287cd` / `3b102a0` openspec-archive / `70adcbc`); R1 / R2 共 12 份报告 grep 同一组词 = 0。skill-creator SKILL.md 第 67 行原文见「新问题检查」第二节。
14. **v1 数据按 v3 规则回放**: v1 new 的 10 条 should-trigger 最高 1/3 ⇒ query 级 0/10 ⇒ 门 fail; v1 negctrl 全部 0/3 ⇒ 0/10 ≤ 5 ⇒ 不作废 ⇒ 结论为 fail。v1 old 只有一条 2/3 ⇒ 1/10, 同样 fail —— 如果同批跑旧版对照, 就能暴露这种环境造成的整体压低。
15. **SC-5 正则反事实**: 窗口 20 时, 五个正样本命中情况为 [0, 0, 0, 1, 1]; 窗口 40 时为 [1, 1, 1, 1, 1]; §D2 正文去掉「不设比较判据」那行后, 两种窗口都是 0 命中。v3 自称测过的两条正样本 (都是短句) 确实能命中, 与 v3 的说法一致; 问题出在样本覆盖面。
16. **同批提交**: `git show --stat 0c41e53` 同时包含 RESULT.md 与 proposal.md ⇒ 抬头「与本版同批提交」属实。
17. **轮次耗时 (按文件时间)**: R1 17:36 → 18:01 (约 25 分钟); R2 11:08 → 12:02 (约 54 分钟, 含额度中断后的重派)。
