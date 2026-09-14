---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T13:38:11.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [knowledge-manager]
---

# post_spec Round 4 — knowledge-manager 席

被审 SHA `e822829` (rework v4)。

## R3 对账

| # | R3 finding (本席) | 状态 v4 | 依据 |
|---|---|---|---|
| 1 | 新术语「行为指令句」落入 SOT §2 新句正文, 未接 SOT §1 处方性/描述性判据体系 | **closed** | 实读 v4 proposal.md 全文, `grep -n "行为指令句"` 在仓库正文 (非审计报告历史文件) 命中 0。R3 聚合报告 rework 计划第 2/10 条「行为指令句一词整体删除」已执行: D1「只改 description 时场景 1 还跑不跑」回改为**照跑**、不设放宽分支 (第 32 行), 放宽可能性整体移到 OQ-6 (逐行点名 + owner 裁), 该术语连同它试图区分的「触发面 / 行为指令句」二分法一并消失, 不存在需要挂接 SOT §1 的残留概念 |
| 2 | D4 承诺「两套编号不同轴」写入 §4.1, 但 SC-3 未断言该说明句的存在 | **closed** | v4 SC-3 新增子句「且 §4.1 含说明两套编号不同轴的一句 (`grep -cF "两套编号"` ≥ 1)」(proposal.md 第 134 行); D4 正文第 86 行仍保留该说明句本体「两套编号不同轴: `decision_table_row` 取 SOT §2 决策表行号; `scenario1` / `scenario4b` 是手册的场景编号。§4.1 写一句说明。」承诺与验证现已配对, 反事实 (现行 SOT 五字段名均 0 命中) 也已写入 SC-3 |

**closed 2 / partially 0 / open 0**。

## Findings

- [major] documentation/proposal.md §D2 (issue): D2 转述 v5 自然措辞扩张测试短语与 RESULT.md v4 §v5 表 / 结论 2 不符——proposal 只写「多加『相关文档 / 整理项目收尾材料 / 收尾整理』」(3 项, 且丢了「与」字前缀), 漏掉 RESULT.md 实际记录的第四项「整理归档文档」; 该第四项恰是四项里唯一直接命中被测 skill (openspec-archive) 自身领域词的措辞, 遗漏它会让读者 (含未来据此裁 OQ-7/OQ-8 的 owner) 低估这次自然扩张测试实际逼近领域词的程度, 属事实转述不成立, 建议 Phase B 落地前订正为与 RESULT.md v4 逐字一致的四项列表。

## 观察

- OQ-7 新引入的「交互模式」「自主模式」与 proposal 自身及 CLAUDE.md 既有词不完全同形: §Impact (第 116 行) 用「自主运行时 (v2.0 Layer 2)」, 与 CLAUDE.md「自主运行时」(项目本质段、项目状态段) 同形一致; 但 OQ-7 正文 (第 152-154 行) 改用「交互模式 (v1.x, 人 + Claude Code)」「自主模式 (v2.0 Layer 2, aria-runner)」两个新词——CLAUDE.md 全文没有「交互模式」(只有英文括注 `(interactive)`), 「自主模式」也只是「自主运行时 / 自主执行者」的又一变体。三处均各自括注了 v1.x / v2.0 Layer 2, 读者不会误读, 不构成阻断, 但同一份 proposal 内部对同一概念 (v2.0 Layer 2 自主运行) 前后用了两个不同中文标签。建议 Phase B 落地或后续同类 spec 统一复用 CLAUDE.md 既有的「自主运行时」, 不再新造「XX 模式」变体, 减少长期术语增殖。
- 三处 D1 新句代入原文后逐句通读, 均可读、无歧义: (1) CLAUDE.md 规则 #6 表后行替换后紧接原有「跑 benchmark 本身不需要 OpenSpec」句, 衔接自然; (2) SOT §2 末句替换后与 §3 开头「AB 套件覆盖不到这个行为」不冲突, 且 SOT §3 另按 D1 承诺追加边界注 (「description hunk 不走本节」, 由 SC-10 第二子句管, 现状 grep 命中 0, 待写入); (3) 手册「边界与留痕」行的旧句/新句在 proposal 表格里均以尾部斜杠截断 (截到「拿不准照跑」之前), 是有意的前缀替换写法——替换后「/ 拿不准照跑) 见 CLAUDE.md 规则 #6…」原样保留在四项末尾, 逐字代入验证语法与括号配对均正确, 「边界三条→四条」计数语同步。
- 核心句「只验证触发面没被改坏, 不验证 description 改得更好」在 proposal.md 全文命中 5 次 (非 3 次): 第 38-40 行三处表格新句逐字相同, 另在第 42 行「核心句 = …」定义句与第 132 行 SC-1 断言本身各自重复引用同一字符串作说明, 共 5 处但字符串本体完全一致、无变体, SC-1 真正约束的是落地后 CLAUDE.md/SOT/手册三个目标文件 (现状三处均为 0 命中, 待 T1 写入), 不是 proposal.md 自身出现次数, 无歧义。
- CLAUDE.md 卫生复核 (按实际文件重算): 现状 151 行 / 13316 字节 (`wc` 实测); 规则 #6 表后句旧句 92 字节 → 新句 244 字节, 净增 152 字节, 替换后总量约 13468 字节、行数不变 (原句本就是段内一整行, 不产生新物理行)。远低于 `claude-md-hygiene.md` §3 的 200 行 / 24000 字节双预算, 不触发 `claude-md-changelog-free`。新增的「场景 1」「场景 4b 地板守卫」等词属 AB 测试方法论词汇 (与规则 #6 原有的「AB」「decision 表」同类), 不是 §2.4 第 3 条所指的「skill 设计内部术语」(该条防的是具体 skill 内部实现细节污染 without_skill baseline, 实证案例 aria-plugin#116), 不违反该条。
- D5.4 上游反馈修正后的措辞 (「文件名与 `# <skill_name>` 标题两处都要改」「`This skill handles:` 首句嵌的是 description, 不是技能名, 不在修复范围」) 已对照当前插件缓存里的 `run_eval.py` 源码逐行核实: 第 52-54 行 `clean_name = f"{skill_name}-skill-{unique_id}"` 且用于 `command_file` 文件名, 第 66 行 `f"This skill handles: {skill_description}\n"` 确认首句内嵌变量是 `skill_description` 而非 `skill_name`; 与 RESULT.md v4 结论 3(b) 逐字一致, 无新漂移。
- D2「fail 的后果」(修 R3 major #1) 与 D4 rule6_note 模板互相反向引用 (D2→D4 约定记录格式, D4→D2「处置见 D2」), 双向闭环无缺口; void 需「连续 2 轮」才升级、fail 则「两条都不走」即升级, 两者升级门槛不同属有意设计 (void 是测量不可用、需多次尝试排除套件/环境噪声; fail 是已明确判负、需要主动补救), 不是不一致。
- `provisional` 后缀的定义实际落在 D4 第 84 行 (紧跟 rule6_note YAML 模板之后, 非 D2), 与 OQ-7 引用「(D4)」的落点核对一致, R3 minor #7 (tech-lead 提) 「provisional 不在 D4 值域」已确认修复; 时长数字「11–20 分钟」在 OQ-3 / OQ-7(B) / §Impact 三处统一, 同一 minor 的时长半部分也已同步, 无残留旧数。
- OQ-7 引用 `aria-orchestrator/docs/architecture-decisions.md` §AD10、OQ-9 引用 CLAUDE.md 项目状态「Blocker 4」均已核对存在且原文措辞一致: AD10 第 756 行「Aria 2.0 流水线只保留 1 个人类审批 gate, 位置在 S7_AWAITING_MERGE」与 OQ-7「AD10 规定整条流水线只有 S7_AWAITING_MERGE 一个人工 gate」相符; CLAUDE.md 第 135 行「Blocker 4: Luxeno 后端延迟 45-54s」与 OQ-9「Luxeno 延迟 45–54 秒 / 次」相符。两处引用均可定位、无偏差。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 1 major / 0 minor。R3 遗留本席 2 项 minor 全部 closed (行为指令句术语随 D1 回改整体删除; 两套编号不同轴现已配对 SC-3 断言)。本轮新发现 1 项 major: D2 转述 v5 实验措辞漏掉 RESULT.md v4 实际记录的第四项测试短语「整理归档文档」, 且该项恰是四项里最贴近被测 skill 领域词的一条, 影响读者 (含 owner) 对 OQ-7/OQ-8 自然扩张风险的判断基准, 建议 Phase B 落地前订正使 proposal 与 RESULT.md v4 逐字一致。其余检查 (三处新句可读性、CLAUDE.md 卫生预算、fail/void/provisional 值域闭环、AD10/Blocker 4 引用可定位性、D5.4 与 run_eval.py 源码核对) 均通过, 未发现新增阻断性问题。

## Vote

REVISE

## 术语与关系对照表

| 术语/概念 | proposal.md v4 | RESULT.md v4 | SOT/CLAUDE.md/手册 (拟改文本) | 一致性 |
|---|---|---|---|---|
| 核心句「只验证触发面没被改坏, 不验证 description 改得更好」 | D1 表三处新句逐字相同 (第 38-40 行, SC-1 grep 目标; 全文含定义句/SC 断言句共 5 次引用, 字符串本体一致) | 不含逐字句 (语义来源, 非宿主) | 三处落点文本即核心句本体, 现状均 0 命中, 待 T1 写入 | 一致 |
| 行为指令句 (v3 遗留术语) | v4 已整体删除 (仓库正文 grep 命中 0) | 未出现 | 不再涉及 | 一致 (以删除方式收敛), R3 minor 1 closed |
| 两套编号 (`decision_table_row` vs `scenario1`/`scenario4b`) | D4 第 86 行「不同轴」说明句 + SC-3 新增子句断言其存在 | 不涉及 | §4.1 拟写入该说明句 | 一致, R3 minor 2 closed |
| fail / void / provisional (rule6_note 值域) | D2 (通过/fail 后果/作废判据) + D4 (模板 + provisional 后缀, 第 84 行) 双向引用闭环 | 不涉及 | SC-3 管字段与值域, SC-9 管「不得 ship」措辞出现 ≥ 1 次 | 一致 |
| 场景 4a / 4b | D5.1 定义 4a=现状 run_loop.py 保留, 4b=新地板守卫 (D2/D3) | 结论 2 是 4b 判据的直接来源, 不使用该编号本身 | SC-8 要求手册两标题各恰 1 次, 现状手册 0 次出现, 无命名冲突 | 一致 |
| v5 自然措辞扩张具体测试短语 | D2 只列 3 项「相关文档 / 整理项目收尾材料 / 收尾整理」 | §v5 表 + 结论 2 均为 4 项「与相关文档 / 整理项目收尾材料 / 整理归档文档 / 收尾整理」 | 不涉及 (proposal 转述层问题, 不影响 SOT/手册/CLAUDE.md 落点) | **不一致, 见 Findings**——proposal 遗漏「整理归档文档」 |
| 交互模式 / 自主模式 (OQ-7 新词) | OQ-7 正文 (152-154 行) 用「交互模式」「自主模式」, §Impact (116 行) 用「自主运行时」 | 不涉及 | CLAUDE.md 现有「自主运行时」「自主执行者」「(interactive)」, 无「交互模式」原形 | **proposal 内部不完全同形, 见观察**——各自括注 v1.x / v2.0 Layer 2, 不构成误读但建议统一 |
| AD10 / Blocker 4 引用 | OQ-7 引 AD10, OQ-9 引 CLAUDE.md Blocker 4 | 不涉及 | `aria-orchestrator/docs/architecture-decisions.md` 第 752/756 行; CLAUDE.md 第 135 行 | 一致, 均可定位、原文措辞相符 |
| D5.4 上游反馈措辞 (文件名 + 标题两处嵌技能名, 首句嵌 description) | D5.4 已按 R3 rework 修正 | 结论 3(b) 逐字一致 | — | 一致, 已对照 `run_eval.py` 源码 (第 52-54/66 行) 核实 |
