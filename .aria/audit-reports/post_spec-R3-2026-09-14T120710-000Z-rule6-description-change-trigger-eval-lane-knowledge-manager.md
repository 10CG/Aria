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
verdict: PASS
timestamp: 2026-09-14T12:52:25.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [knowledge-manager]
---

# post_spec Round 3 — knowledge-manager 席

被审 SHA `0c41e53` (rework v3)。

## R2 对账

逐条核对本席 R2 报告 4 条 minor 在 v3 的落点:

| # | R2 finding | 状态 v3 | 依据 |
|---|---|---|---|
| 1 | D5.5 未点破与 `aria-standards#17` 的正交分工 | **closed** | v3 §D1 新增「本条只管深度, 不管广度」显式声明 + §D5.5「与 `10CG/aria-standards#17` 分工」整段: 本 Spec 定深度 (按 hunk 类型跑场景 1 还是 4b), `aria-standards#17` 定广度 (场景 1 跑单 skill 全套件还是 Tier 1 全量)。已实读 `aria-standards#17` 原文核对: 该单确实只讨论「变更面落在单个 Skill 时该跑多大范围」, 未涉及 hunk 类型判断, 与本 Spec 无重叠、无冲突; 该单现状 open, comments=0, 与 T7「查并行编辑」的前提一致 |
| 2 | T1 与 T3 的 CLAUDE.md 指向句可能被误加两次 | **closed** | v3 §D1 末句明确「CLAUDE.md 新句自带「字段见 SOT §4.1」指向, **不在 CLAUDE.md 另加句子**」; Tasks 层再次双向锁定: T1 = 「CLAUDE.md 只改这一句 (含 §4.1 指向), 不另加句」, T3 = 「SOT 新增 §4.1 … —— **只改 SOT**」。两个任务的编辑范围现已互斥声明, 歧义消除 |
| 3 | D4 过渡期兜底机制与结束判据未写 | **closed** | v3 §D4 新增「authoring 路径与过渡期」段: 兜底机制 = 起草者从 CLAUDE.md 规则 #6 新句「字段见 SOT §4.1」获知模板 (CLAUDE.md 每 session 自动加载); 结束判据 = 「过渡期结束 = D5.3 那张 issue 关闭」。机制与终止条件均已显式给出 |
| 4 | 手册场景编号与 `rule6_note.decision_table_row` 两套编号体系未说明是不同轴 | **closed (叙述层)** | v3 §D4 新增一条: 「两套编号不同轴: `decision_table_row` 取 SOT §2 决策表行号; `scenario1` / `scenario4b` 是手册的场景编号。§4.1 写一句说明」—— 明确承认两轴不同并承诺在 §4.1 落一句说明。但该承诺目前无对应 Success Criteria 断言其真的落地 (§4.1 只有 SC-3 管字段名与值域), 见下方 Findings 新增项 |

**closed 4 / partially 0 / open 0**。

## Findings

- [minor] documentation/proposal.md §D1 (SOT §2 新句) (issue): 新术语「行为指令句」(要求执行方式的句子) 落入 SOT §2 正文, 但未接 SOT §1 既有「处方性 / 描述性」判据体系 (处方性定义已含「AI 读了照做」的判据, 与「行为指令句」实质同指), SOT 正文本身也无操作性定义或示例 (示例「不要自己手工 mv」只在 proposal 叙述里, 不落 SOT); 风险由「拿不准照跑」兜底限定为「误判后过度保守」而非漏跑, 但仍建议改写为直接复用 §1「处方性」术语或在 SOT 新句内联一个判例, 避免同一份 SOT 内并存两套未挂钩的分类语言。
- [minor] testing/proposal.md §D4+Success Criteria (issue): D4 承诺「两套编号不同轴」的说明句写入 SOT §4.1, 但 SC-3 只断言五个字段名与值域 (`void`/`n/a`), 未断言该说明句的存在; 该承诺在实现期可能被静默漏写而无任何 SC 检出 (与 R2 已修复的「D2 判据正文 / §3 边界注无 SC 管」同类缺口, 该轮 SC-10 已补 §3 边界注, 但 §4.1 这一句尚未补)。

## 观察

- 独立复核确认 v3 对 R2 三处数值/引用类 major 的修复均为真修复而非文字调整: (1) D2 负控门槛「10 对 5 单侧 Fisher p = 0.016 (10 对 6 为 0.043)」经 scipy 独立重算逐位吻合; (2) OQ-6 引用的 `2026-09-04-v1.69.1-spec-drafter-rule5-hunkA/` 8 份 `timing.json` 求和 = 652,757 token / 1,626,592 ms, 与正文「约 65 万 token」「27.1 分钟」吻合; (3) SC-5 正则 `(新版|新 description|被评)…(≥|>=|不低于|高于|优于|不差于)…(旧版|旧 description)` 用 python `re` 独立重跑, 对两条正例各命中 1、对「不设比较判据」整行命中 1 (证明必须先剔除该行, 设计自洽)、对负控门槛行与 D2 判据正文命中 0, 与自测声明完全一致。
- D3 六行前置表 (`v1-shared-root-4workers/` … `RESULT.md`) 逐路径 `test -e` 核对全部存在; `ab-suite/version.yaml` 现值确认为 `1.5.0`, 与 SC-4「大于改前 1.5.0」的前提一致。
- CLAUDE.md 卫生复核: 现状 151 行 / 13316 字节; D1 表内 CLAUDE.md 新句替换后单行净增约 177 字节, 总量升至约 13493 字节, 不产生新物理行 (原句本就是段内一整行)。远低于 `claude-md-hygiene.md` §3 的 200 行 / 24000 字节双预算红线, 不触发 `claude-md-changelog-free`; 该规则第 3 条「skill 设计内部术语不入内」也不适用——rule6_note 字段名是**规则执行元数据**, 不是 skill 设计术语, 且已用「见 SOT §4.1」指针化, 未在 CLAUDE.md 内联展开五字段, 符合 §2.4 进货口纪律。
- SOT §2 新句、手册「边界与留痕」新句代入原文后逐句可读, 「三条→四条」与「两个→三个已知缺陷」两处计数语经 grep 反事实核对现状均为可整改的单一命中点, 不存在 SC-7 会误伤的同形句。
- D1 关于「只改 description 时不跑场景 1」的拆分 (纯触发面不跑 / 含行为指令句照跑) 与手册场景 1 现文「with_skill: 加载 SKILL.md 后执行任务」核对一致——with-skill 臂确实会读到 description 全文, 故该拆分是对 R2 code-reviewer「说得太满」意见的实质修正而非文字规避, 论证站得住 (但引入的新术语仍是上方 Findings 第 1 条)。

## Verdict

PASS — 0 critical / 0 major / 2 minor。R2 遗留本席 4 项 minor 全部 closed (aria-standards#17 正交分工 / T1+T3 指向句去重 / D4 过渡期兜底与结束判据 / 两套编号不同轴的叙述层澄清), 且逐条溯源核验非文字表演: 统计量、token/时长求和、文件存在性、正则行为、CLAUDE.md 字节预算均独立重算吻合。本轮新发现两条 minor, 均为「已在叙述层解决但缺收尾动作」性质 (新术语未挂靠既有词表 / 新承诺未配 SC), 不构成结构性缺陷, 亦有「拿不准照跑」等既有安全网兜底, 不阻断进入 Phase B; 建议在 Phase B 落地三处新句时顺手带上。

## Vote

PASS

## 术语与关系对照表

| 术语/概念 | proposal.md v3 | RESULT.md v3 | SOT/CLAUDE.md/手册 (拟改文本) | 一致性 |
|---|---|---|---|---|
| 地板守卫 | Why 第 3 条 / D1 核心句 / D2 标题 / D6 | 结论 2 首提, 已知局限重述 | 三处 D1 新句逐字含「地板守卫」 | 一致 |
| 核心句「只验证触发面没被改坏, 不验证 description 改得更好」 | D1 表三处新句逐字相同 (SC-1 grep 目标) | 不含逐字句 (RESULT 是三处核心句的语义来源, 非宿主) | 三处落点文本即核心句本体 | 一致, 溯源清晰 |
| 只承诺已验证的两类破坏 | Why 第 3 条 / D2 / D6 | 结论 2「已验证的破坏类型恰两类」/ 已知局限末条 | D6 追加进 SOT §6 第三条 | 一致 |
| 行为指令句 (新, v3 独有) | D1 两处 + OQ-6, 唯一示例「不要自己手工 mv」只在此处 | 未出现 (RESULT 不涉及场景 1/4b 分工) | 将写入 SOT §2 新句正文, 但 SOT §1 既有「处方性/描述性」判据未与之挂钩 | **不完全一致, 见 Findings 第 1 条**——新词与旧词并存但未声明关系 |
| 场景 4a / 4b | D5.1 定义: 4a=现状 run_loop.py (保留), 4b=新地板守卫 (D2/D3) | 不使用该编号, 但结论 2 是 4b 的直接来源 | SC-8 要求手册两标题各恰 1 次; 现状手册 0 次出现, 无命名冲突 | 一致 |
| 两套编号 (`decision_table_row` vs `scenario1`/`scenario4b`) | D4 明确「不同轴」并承诺 §4.1 写说明句 | 不涉及 | 承诺尚无 SC 断言其落地 | **叙述层一致, 验证层有缺口, 见 Findings 第 2 条** |
| rule6_note 值域 (`pass`/`fail`/`void`/`not_required`/`n/a`) | D2 (fail/void 语义) + D4 模板 (完整值域) 双向一致 | 不涉及 | SC-3 要求值域含 `void` 与 `n/a`, 与 D4 模板一致 | 一致 |
| 与 `10CG/aria-standards#17` 的分工 | D5.5「本 Spec 定深度, #17 定广度」 | 不涉及 | — | 一致, 已用 issue 原文独立核对 (见 R2 对账 #1) |
