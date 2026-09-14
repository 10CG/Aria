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
timestamp: 2026-09-14T12:38:40.832Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [code-reviewer]
---

# post_spec R3 — code-reviewer 席 (Phase 1 规范合规 + Phase 2 质量)

被审对象: `openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md` rework v3 @ 主仓 HEAD `0c41e53`; 基线目录 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/` (RESULT.md v3 与原始产物)。只审不改, 唯一写入是本报告。

独立性: 本轮其他席的 R3 报告未读 (目录里已有 qa-engineer 的 R3 文件, 只看到文件名, 没有打开); R2 只读了聚合报告和本席报告。下文每个数字都来自实跑, 命令与输出见「实跑记录」。

## R2 对账

范围: 本席 R2 报告 Findings 的 17 条 (2 major + 15 minor), 按 R2 报告里的顺序编号。

| 序号 | R2 条目 | v3 落点 | 状态 | 核对依据 |
|---|---|---|---|---|
| 1 | [major] D2 负控以被评 description 为参照, 严重退化被判作废、逃过 FAIL; 作废后动作与 rule6_note 取值缺 | §D2 同批负控四个子项; §D4 值域与合规规则 | closed | 负控改为绝对门槛 ≤ 5/10, 明写「不以被评 description 为参照」; 判定顺序写死为门先判, 退化先落 fail; 作废只在门通过且负控 ≥ 6/10 时发生; 作废 = 义务未完成、不得 ship、修后重跑、rule6_note 记 void、连续 2 轮升级 owner。用 14 份原始臂文件按 v3 规则回放: v3 负控当被评 → fail, v4 过宽 → fail, v1 四臂 → fail, v3 new / old / poscontrol 与 v4 realroot → pass, v2 old → void; 没有一份退化臂落进作废。残留: fail 之后怎么办没写, 作为本轮新 major, 见 Findings 第 1 条 |
| 2 | [major] SC-5 按文件 grep 恒红, 会诱导删改 SOT §6 的存量句 | §SC-5 | closed | 范围收窄到手册 §场景 4b 小节 + 三处 D1 落点行, 改用 python re。实跑: 三条 D1 新句 0 命中; 用 D2 + D3 正文模拟 4b 小节 (去掉含「不设比较判据」的行) 0 命中; 改前手册没有 4b 小节, 「不设比较判据」= 0 ⇒ 改前红、改后可绿, 不再恒红; SOT §6 和手册 §版本管理的存量句已不在范围内。「本 shell 的 grep 是 ugrep 包装, 该正则报 exceeds complexity limits」实测成立, GNU grep 3.8 可跑。残留见观察第 4、5 条 |
| 3 | [minor] Why 第 1 条全称句「对任何两个真 description 都打平」; 「对照物」方向容易读反 | proposal §Why 第 1 条; RESULT §结论 1 | partially | proposal 已改 (「两个都能让 should-trigger 饱和的 description 必然打平 (本次这一对即如此)」+「例如新版被改坏」)。RESULT v3 结论 1 仍写「对任意两个真 description 都打平, 只在对照物是坏 description 时判红」, 与本文件 §已知局限「不是『任何 description 改动都测不出』」冲突 (v2 的「任何」只换成了「任意」)。见观察第 1 条 |
| 4 | [minor] 「+4 ⇒ p 约 0.03」实算不成立 | §D2 判据子项 | closed | 改为 ≤ 5/10, 写 10 对 5 单侧 p = 0.016、10 对 6 为 0.043。复算 0.0163 / 0.0433, 一致 |
| 5 | [minor] 「42/43」分母错 | §D5.2; §Impact; §OQ-7 | closed | 改为「43 个目录、42 个含 SKILL.md, T4 后余 41」。复算: 目录 43, 含 SKILL.md 的 42, 已跟踪 SKILL.md 42; 多出的 `issue-triage-workspace` 被 `.gitignore` 的 `skills/*-workspace/` 忽略。残留见观察第 9 条 (T4 不执行时应为 42) |
| 6 | [minor] RESULT 时长区间漏 v2 | RESULT §时长与成本; proposal §Impact | closed | 「10m39s–17m39s (v2 四臂 11m26s–17m39s, v3 四臂 10m39s–12m03s, v4 两臂 13m38s–13m54s)」与 run.log 逐臂相减一致; 并行约 11–18 分钟、串行约 22–34 分钟。残留: OQ-7 (B) 还是 v2 的旧数「约 12–14 分钟」, 见观察第 3 条 |
| 7 | [minor] D3 第 3 行 97 / 12 是模型自报; manifest 的 13 未解释; 成本差混入思考输出 | §D3 第 3 行; RESULT「技能数口径」段与隔离行 | closed | D3 写明「技能数是模型自报, 不作证据」; RESULT 解释 97→13 来自未传 `--model` 的首次探针; 成本差拆为 cache 创建 27065 对 3696 与输出 1190 对 5 两部分, 均与探针 json 一致。同类新问题 (yes / no 也是自报) 见观察第 11 条 |
| 8 | [minor] SC-2 / SC-7 按字面执行对不上 | §D3 表; §SC-2; §SC-7 | closed | D3 实证格改为无省略、无通配的具名路径, 在基线目录逐个 `test -e`, 10 个全真; `[配置推导]` 恰 1 行; 加了零行判红。SC-7 改为 `grep -cF '**Version**: 1.1.0'`, 改前 1.0.0 = 1、1.1.0 = 0, 反事实成立 |
| 9 | [minor] RESULT「见 handoff (与本文件同批提交)」失实 | RESULT §已知局限末条 | closed | 已删, 改为「两项 AI 流程判断写在 Spec 的 OQ-3 与 rule6_note 段」, 两处在 proposal 里都有 |
| 10 | [minor] D4 值域缺 n/a 和作废; 「照跑」对应两行 | §D4 模板 | closed | decision_table_row 取 1 / 2 / 3 / 4 / n/a, scenario4b 含 void 与 n/a; 本 Spec 自己的 rule6_note 五个取值都在值域内 |
| 11 | [minor] 「手册 §数据组织表」锚点不存在 | §Key Deliverables; §T2 | closed | 改为「§固定测试集 vs 临时测试 表加 trigger 行」, 该小节在手册里实有。「### 目录结构」树没提, 见观察第 13 条 |
| 12 | [minor] RESULT 引用无路径无 SHA; SOT 在子模块内须写主仓全路径; §6 末句出处 | §D6; §D1 SOT 新句 | partially | D6 第三条已带「Aria 主仓」全路径和自身出处; CLAUDE.md 新句改为只指向 SOT §4.1。仍缺两处: D6 没带 RESULT v3 头部要求的「@ <提交 SHA>」; D1 的 SOT 新句写 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`, 没加「Aria 主仓」限定 (该句落在 standards 子模块里)。见观察第 2 条 |
| 13 | [minor] 「只改 description 不跑场景 1」说得太满 | §D1「只改 description 时场景 1 还跑不跑」; §OQ-6 | closed | 分成「只涉及触发面 ⇒ 不跑」与「含行为指令句 ⇒ 按指令 hunk 照跑」, 拿不准照跑; OQ-6 写了「不跑」一侧的代价 |
| 14 | [minor] OQ 推荐项不写自身代价; OQ-4 措辞; OQ-5 标「原文」实为删节 | §Open Questions | closed | OQ-1 至 OQ-8 的推荐项或已选项都写了自身代价; OQ-5 引文与 issue 验收第 2 条用 python 逐字比较, 结果 `EQUAL: True`; OQ-4 如实转述「跨模块 → 自动提升为 Level 3」与「涉及 2 个及以上模块」, 模块映射 (standards = `standards/**, .claude/**`) 与原文一致 |
| 15 | [minor] OQ-3「重跑一臂」与同批负控矛盾; OQ-6「30 分钟 / 15 美元」无出处 | §OQ-3; §OQ-6 | closed | OQ-3 改为两臂, 并行约 11–18 分钟 / 约 10 美元; OQ-6 改引 8 个 timing.json, 复算 27.11 分钟、652757 token, 与「27.1 分钟、约 65 万 token」一致 |
| 16 | [minor] D2 判据正文与 SOT §3 边界注无 SC 管; T1 / T3 的指向句重叠 | §SC-9; §SC-10; §T1; §T3 | closed | SC-9 管「≤ 5/10」「连续 2 轮」, SC-10 管四个参数串、「20 条」和 SOT「description hunk 不走本节」; 改前各为 0, 反事实成立; 四个参数串都是 run_eval.py 的真实 flag。T1 写明 CLAUDE.md 只改这一句, T3 写明只改 SOT。未覆盖的剩余项见观察第 7 条 |
| 17 | [minor] 今后新建套件要不要 owner 审没有规定 | §D2 套件子项; §OQ-7; §Impact | closed | D2 指向 OQ-7; OQ-7 把首次建套件与审阅合并成 (A) / (B) 两个选项, 各写代价; Impact 计入 owner 时间 |

合计: closed 15 / partially 2 / open 0。R2 的两条 major 都已关闭。

## Findings

- [major] implementation/proposal.md §D2 §D4 (issue): 场景 4b 判 fail 之后怎么办没写。D4 只规定 void「义务未完成、不得 ship」, fail 是合法取值却没有后果, 按字面可读成「跑完即合规」; 有意收窄触发面导致的 fail 也没有「改套件」路径。
- [minor] documentation/RESULT.md §结论 3(b) + proposal.md §Why 第 3 条 §D5.4 (issue): v3 新写入的「正文首句 `This skill handles:` 嵌入技能名」与 run_eval.py 第 66 行不符 (首句嵌的是 description); D5.4 把「首句也要改」列为上游反馈必含内容, T6 照做会把错误诊断发给上游。

计数: critical 0 / major 1 / minor 1。第 2 条是 minor, 但 T6 必须按 D5.4 的「须含」原样对外发送, 不改就进 Phase B 会把错误带出仓外, 所以列入 Findings。

## Findings 证据与修法

1. **fail 之后的处置 (major)**
   - proposal 里 fail 的出现位置: D2「被评 description 退化 ⇒ 门先判 fail … 不会落到作废」、D4 值域「<结果目录> fail」, 另有一处是手册旧句里的「fail-closed」(无关)。「不得 ship」只出现 2 次, 都挂在 void 上 (D2 作废子项、D4 合规规则)。
   - 按字面推: D2 把 void 定义为「本 cycle 的 Rule #6 义务未完成」, 反过来就是拿到非 void 结果 (含 fail) 义务即完成。CLAUDE.md 新句也只说「一律跑场景 4b」, 没说要通过。D4 列的不合规情形 (scenario4b 为空 / not_required / n/a) 也不含 fail。执行者按零裁量读字面, 可以写 `scenario4b: <目录> fail` 然后 ship。
   - 这不只是理论上的读法: Rule #6 与 SOT 对「照跑」一直只规定要跑、不规定结果门槛, 本仓的 AB 结果向来由执行者解读后决定是否 ship (例: v1.73.0 openspec-archive 那次新旧两臂 delta 0、有区分力的 expectation 0, 解读为「无回归」后 ship, 见 `10CG/aria-plugin#190` comment 22921)。场景 4b 如果不写阻断, 会沿用这个语义。
   - 作者的意图其实是阻断: OQ-1「0.5 门放过 2/3 才触发的 description」、OQ-7「套件审过才能作门」「假绿」都预设 fail 会拦住。但门最核心的后果不能只靠旁证去推。
   - 另一面是正当的 fail: 被评 description 有意收窄触发面 (比如删掉一个使用场景) 时, 套件里对应的 should-trigger 会合理地掉到 0.5 以下, 判 fail。这时该改的是套件, 不是 description; D2 / D4 都没给路径 (改套件 → 升 `ab-suite/version.yaml` → 按 OQ-7 审阅 → 重跑)。没有路径, 执行者只能临场处理: 要么不升版、不审阅就改套件, 要么带着 fail ship, 两者都违背零裁量。
   - 修法 (D2 加一个子项, T2 照抄进手册, 再加一条 SC):
     - 「fail ⇒ 不得 ship。非有意退化: 修 description 后重跑; 有意改动触发面: 先改套件 (升版, 按 OQ-7 审阅), 再重跑; rule6_note 记最后一次结果, 之前 fail 的结果目录一并列出。」
     - D4 合规规则补一句「scenario4b 为 fail ⇒ 不得 ship」。
     - SC-9 加一项: 手册 4b 小节「不得 ship」≥ 2 次 (fail 与 void 各一), 改前为 0。

2. **「首句嵌入技能名」与源码不符 (minor, 不改不能进 Phase B)**
   - run_eval.py 源码 (marketplace 与缓存 `bb335391eb83` 两份逐字节相同):
     - 第 52 行 `clean_name = f"{skill_name}-skill-{unique_id}"`, 第 54 行文件名 `f"{clean_name}.md"`
     - 第 60–64 行 frontmatter `description: |` 后接被评 description
     - 第 65 行 `f"# {skill_name}\n\n"`
     - 第 66 行 `f"This skill handles: {skill_description}\n"`
   - 所以嵌入技能名的是文件名 (即命令名) 和标题这两处; 首句嵌的是被评 description, 也就是被测变量本身。RESULT v3 在同一句里自己写了「正文首句 `This skill handles: <description>`」, 却结论为「都嵌入技能名」。
   - 来历: v2 的 RESULT (b) 写的是「命令文件名与正文 = `<skill_name>-skill-<id>` / `# <skill_name>`」两处, 这是对的; v3 采纳 R2 聚合第 17 条「漏正文标题与首句」时, 没有对源码自验。
   - 附带一点 (推断, 未实测): 按 run_eval.py 文档字符串, 命令文件是为了出现在 available_skills 列表里; 按 Claude Code 自定义命令的加载方式, 触发判定时模型看到的是命令名和 frontmatter description, 正文 (标题与首句) 要调用后才读到。v2→v3 同时换了文件名和标题, 数据分不开这两者; 有机制依据的泄漏通道只有文件名。
   - 影响: D5.4 规定上游反馈「须含」这条修复方向, 而 T6 是对外发给 Anthropic 官方插件的。任何人读第 66 行都能证伪这条诊断, 会连带削弱另两条真缺陷的可信度。
   - 修法: RESULT (b) 改回「命令文件名与正文标题嵌入技能名 (首句嵌的是 description, 不是泄漏)」, 版本号递增; proposal Why 第 3 条改为「文件名、标题嵌入技能名」; D5.4 (ii) 改为「命令文件名不嵌入真技能名 (必改); 正文标题可一并中性化 (可选)」。

## 观察 (不进收敛比较键, 不影响 vote)

1. **RESULT §结论 1 的残留全称句** (R2 第 3 条 partially): 「在饱和处, 『新版 ≥ 旧版』类比较判据对任意两个真 description 都打平, 只在对照物是坏 description 时判红」。建议照 proposal Why 第 1 条的 v3 写法改, 「对照物」改为「被评一方」。
2. **引用** (R2 第 12 条 partially): D6 第三条的出处建议写成「… RESULT.md v3 @ 0c41e53」(RESULT 头部自己要求带 SHA); D1 的 SOT 新句「判据与前置见 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` §场景 4b」建议加「Aria 主仓」, 与 D6 一致 —— standards 在 GitHub 上单独发布, 读者手里没有主仓路径的上下文。
3. **数字残留**:
   - OQ-7 (B)「审阅改动套件则重跑 (约 12–14 分钟 / 约 10 美元)」是 v2 Impact 的旧数 (`55bc9f3` 版原文「并行约 12–14 分钟」), 与 v3 Impact 和 OQ-3 的「并行约 11–18 分钟」不一致。
   - OQ-8「一臂约 12 分钟」是 10m39s–17m39s 区间里的点估, 建议写区间。
   - OQ-4「post_spec 每轮约半小时, R1 / R2 实测」: 按报告文件时间, R1 约 25 分钟 (17:36:16 → 18:01:17), R2 约 54 分钟 (11:08:40 → 12:02:58, 含额度中断后的重派)。R2 那一半支撑不了「约半小时」, 建议写「R1 约 25 分钟; R2 因中断重派约 54 分钟」。
4. **SC-5 正则的召回面窄** (不影响收敛: D2 已明写「不设比较判据」, SC-5 也有「≥ 1 次」的正向锚):
   - 我试了 6 种自然的比较句式, 命中 2 种 (「新版触发率 >= 旧版触发率」「新版本的触发率不低于旧版本」), 漏 4 种: 「新 description 的 should-trigger 命中数不低于旧 description」与「新版的 should-trigger 触发率须 ≥ 旧版」(间隔超过 20 字符); 「被评版本命中率不得低于旧版」与「新版触发率不应低于旧版」(「不得低于」「不应低于」不在比较词表里)。
   - 「两条比较句各命中 1」的自测样本没有落盘, 无法复核。
   - 「『不设比较判据』行 … 为 0」: 拿 D2 那行原文 (「不设比较判据 (如新版触发率不低于旧版) …」) 直接跑是 1 命中。SC-5 的流程会先删掉这类行, 所以不影响判定, 但自测描述与复现不符。
   - 建议: 比较词表补「不得低于 / 不应低于 / 至少」, 间隔放宽到 40, 自测样本写进 SC-5 正文。
5. **「小节」的边界没有统一定义**: SC-5 写「从 `### 场景 4b` 到下一个 `###` 或 `##` 标题」; 手册现有 `#### 场景 1 运行前置` 这样的四级标题 (全文 1 个)。T2 如果仿照它加一个 `#### 场景 4b 运行前置` 来放 D3 表:
   - 按「行以 ### 开头」截取会在四级标题处截断, D3 表落到小节外, SC-2 零行判红; SC-10 看参数串的位置, 也可能判红;
   - SC-8 如果用不锚行首的 `grep -c "### 场景 4b"`, 四级标题行也含这个子串, 计数变 2, 「恰 1 次」判红。
   - 建议在 SC 段开头统一定义: 小节 = 从 `^### 场景 4b` 起, 到下一个匹配 `^#{2,3} ` 的行为止; SC-8 写成 `grep -c '^### 场景 4b'`。
6. **T2 与 SC-2 的路径写法**: T2 写「机读实证写全路径」, SC-2 写「每个反引号路径拼上基线目录后 `test -e`」。如果「全路径」被理解成从仓库根写起, 拼接后前缀重复, 会假红; D3 本身写的是相对基线目录的完整路径。建议 T2 改为「写完整相对路径 (相对基线目录), 表前一句注明基准目录」。
7. **SC 覆盖的剩余缺口** (按反事实「没做这件事, 哪条 SC 会红」逐项试):
   - CLAUDE.md 与 SOT 两处旧句没删、只追加了新句: SC-1 仍绿, 没有 SC 变红 (手册那处由 SC-7「边界三条」= 0 兜住)。建议加两条: 旧句 `grep -cF` = 0。
   - D2「被评退化先判 fail」「作废 = 不得 ship」「修后重跑」没有 SC; D6 第三条正文只由 SC-7 的计数语间接覆盖。
8. **OQ-3「先审且审阅改了 query」这一分支没接上**: T4 要求「搬入 (逐字节同基线)」, SC-4 要求与基线文件 diff 为空, 这一分支下两者都做不到 (要重跑并以新套件为准)。Key Deliverables「仅在 OQ-3 裁为『接受』后执行」与 OQ-3 选项原文「owner 先审再 T4」字面上也不一致。未裁分支 (T4 deferred、SC-4 改判条款、OQ-3 默认「T4 不执行」) 三处一致, 没有问题。建议 SC-4 的比对对象写成「OQ-3 裁定后的套件文件 (审阅未改 = 基线文件; 审阅改动 = 重跑目录下的套件文件)」。
9. **D5.2 标题的计数**: 「41 个 skill 无 trigger 套件」只在 T4 执行后成立; OQ-3 未裁时默认 T4 不执行, 那时是 42 个。Impact 与 OQ-7 的「其余 41 个」同理。建议标题写「42 个 skill 无 trigger 套件 (T4 执行后为 41)」, 或按 ship 时的实况填。
10. **两套编号说明的落点**: D4 写「§4.1 写一句说明」(SOT), Key Deliverables 与 T2 写在手册 4b。两处都写还是只写一处, 没说清, 也没有 SC 管。
11. **探针里的「机械事实」**: RESULT「技能数口径」段说「可靠的机械事实只有一条: 默认设置源下列表含真 `openspec-archive`, project-only 下不含 (两份 json 的 `result` 字段)」。但 result 字段是模型的答复「97,yes」「12,no」, yes / no 和 97 / 12 出自同一段模型输出; 两份 json 的键里没有任何技能或命令列表 (全部键已列出核对)。真正的机读佐证只有 `cache_creation_input_tokens` 27065 对 3696 (上下文大了约 2.3 万 token)。结论方向可信 (默认设置源加载用户级插件), 但「机械事实」的说法站不住; D3 第 3 行「实证看两份 json 的 result 字段」同理。建议改为「result 字段是模型自报, 机读佐证是 cache 创建 token 差」, 或取 stream-json 的 init 事件。
12. **环境失效时判定顺序给出假红**: 按 v3「门先判」规则回放 v2 (合成名泄漏的环境), v2 new (真 v1.73.0, query 级 9/10) 判 fail, 而同批负控 9/10 已经说明这一轮数字不可用, 本应作废。方向是拦住、不放行, 只有误报代价; 修 Findings 第 1 条时如果加一句「fail 且负控 ≥ 6/10 ⇒ 按作废处理 (先修环境)」, 可以一并消除。v1 (共享项目根) 那种把所有臂压到地板的失效, 负控识别不了 (负控 0/10 反而通过门槛), 要有已知良好的正控才能识别; 可作为 SOT §6 的局限补记。
13. **映射与锚点的零碎项**: Key Deliverables 的「文件头 Version 1.0.0 → 1.1.0」仍然没有 D 锚, 只由头部 ship target 承载 (R2 映射表同题); 「§固定测试集 vs 临时测试 表加 trigger 行」挂在 D2 下, 但 D2 正文没提这张表; 手册「### 目录结构」树的 `ab-suite/` 下没加 `trigger/`。
14. **`--model` 不该算「钉死参数」**: D2「参数钉死 … 改任一参数 = 换判据, 须 owner 裁」把 `--model` 也列在里面, 而它的取值是「本 session 模型」。按字面, 每换一次 session 模型都算换判据。建议写明 model 跟着 session 走, 不属于「改了就须 owner 裁」的参数。
15. **owner「开 Level 2 cycle」这句指示在仓内没有记录**: docs/handoff、`.aria/decisions/`、`10CG/Aria#211` 的评论里都查不到。`10CG/Aria#211` 只有一条 triage 评论 (comment 23915), 写的是「属 Level 2 规范变更」, 那是 triage 的判断。不质疑这句指示的真实性, 但 OQ-4 以它为前提, 建议补记到 `10CG/Aria#211` 或 decision 文件, 方便审计。
16. **AB baseline 污染的前置提醒** (与 `10CG/aria-plugin#116` 同形): CLAUDE.md 新句「豁免与结果都写进 `rule6_note` (字段见 SOT §4.1)」会随 CLAUDE.md 自动加载进 AB 的 without_skill 臂。D5.3 那张 issue 以后给 spec-drafter / task-planner 模板加五字段时要照跑场景 1, 而 without_skill 臂可以顺着这个指向写出五字段, 导致 baseline 也过。建议 D5.3 的 issue 正文预先写明这一点, 断言按「完全没提 / 提到 / 按模板给出」分档 (SOT §6 第二条的做法)。
17. **两处未经实测的强断言**:
    - D3 标题「前五条缺一数字不可解读」: 对第 3、4 条是推导, 不是实测 —— 四轮都带着 `--setting-sources project` 跑, 没有「不加这个开关」的对照臂; 第 4 条自标 [配置推导], 而且它的后果更接近「与别的模型的结果不可比」, 而不是「不可解读」。
    - Why 第 1 条「两个都能让 should-trigger 饱和的 description 必然打平」是同义反复 (两边都饱和, should-trigger 自然相等), 不误导, 但也没提供信息。

## 优点

- R2 的两条 major 都改在了要害上: 负控改成与被评对象无关的绝对门槛, 判定顺序写死; 用 14 份原始臂文件回放, 没有一份退化臂落进作废。SC-5 改用 python re 的理由 (ugrep 包装报 complexity limits) 实测成立, 改前是红的, 不再恒红。
- 数字对账全部一致 (见下面「数字对账」): 30/30、8/30、22/30、7/10、0.0031、0.016、0.043、10m39s–17m39s、11–18 分钟、22–34 分钟、27065 / 3696、1190 / 5、27.1 分钟、约 65 万 token、42 / 41、1.0.0 → 1.1.0 都能从原始产物复算出来。
- D1 表可以机械执行: 三条旧句在三个文件里各恰 1 行; 核心句在三条新句里逐字相同; 改前三个文件的核心句各为 0。全仓 (含三个子模块) 查旧句及同义表述的副本, 规范性文本里只有这三处, 加上会被 D5.1 重写的手册 §场景 4「触发时机」行; 其余命中都是审计报告、triage 草稿和一份 AB 答卷。D1「三处同批」覆盖完整。
- OQ 段每一项都写了推荐项自身的代价; OQ-5 逐字引用; OQ-4 如实转述 LEVEL_GUIDE, 并写了两边的代价。
- 所有新 SC (SC-2 / SC-3 / SC-7 / SC-9 / SC-10) 在改前文件上实跑都是红的, 没有真空成立。

## 数字对账 (v3 proposal ↔ RESULT v3 ↔ 原始产物)

| 数字 | proposal 位置 | RESULT 位置 | 原始产物复算 | 结论 |
|---|---|---|---|---|
| 30/30 (query 10/10) | §Why 第 1 条 | 记分表 v3、§结论 1 | v3 new / old / poscontrol 各 30 (10) | 一致 |
| 8/30 (query 3/10) | §Why 第 2 条; §D2 | 记分表 v3、统计段 | v3 negctrl 8 (3), 分布 3/3、2/3、3/3 | 一致 |
| 22/30、7/10 | §Why 第 2 条 | 记分表 v4、§结论 2 | overbroad should-not 22 (7) | 一致 |
| p = 0.0031 | §Why 第 2 条 | 统计表 | 10 对 3 双侧 0.0031 | 一致 |
| p = 0.016 / 0.043 | §D2 | 对 Rule #6 处方的含义 (只写 ≤ 5/10) | 10 对 5 单侧 0.0163; 10 对 6 单侧 0.0433 | 一致 |
| 10m39s–17m39s | §Impact | §时长与成本 | run.log 10 臂 | 一致 |
| 并行 11–18 分钟 / 串行 22–34 分钟 | §Impact; §OQ-3 | §时长与成本 | 单臂区间推得 | 一致 (OQ-7 的 12–14 除外, 见观察第 3 条) |
| 27065 / 3696 | 无 (D3 引 json) | 隔离行 | 探针 cache_creation_input_tokens | 一致 |
| 1190 / 5 | 无 | 隔离行 | 探针 output_tokens | 一致 |
| 0.604 / 0.079 (0.60 → 0.08) | §Impact (0.08) | 隔离行、§结论 3(c) | total_cost_usd 0.6044 / 0.0786 | 一致 |
| 27.1 分钟、约 65 万 token | §OQ-6 | 无 | 8 个 timing.json: 27.11 分钟、652757 | 一致 |
| 42 / 41 | §D5.2; §Impact; §OQ-7 | 无 | 含 SKILL.md 的目录 42, T4 后 41 | 一致 (T4 不执行时为 42, 见观察第 9 条) |
| 1.0.0 → 1.1.0 | 头部 ship target; KD; T5; SC-7 | 无 | SOT `**Version**: 1.0.0` = 1 | 一致 |
| ab-suite 1.5.0 | §SC-4 | 无 | version.yaml `version: "1.5.0"` | 一致 |

## Verdict

**PASS_WITH_WARNINGS** —— critical 0 / major 1 / minor 1 (Findings); 观察 17 条不计入。

- **Phase 1 (规范合规): PASS**
  - `check_bare_issue_refs.py` 对 proposal 和 RESULT 都是「裸 issue 引用: 0」, rc 0。
  - 禁用字形 (U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / 希腊字母大小写): 两个文件 0 命中; NUL 字节 0。
  - 头部: Level / Status / Created / Linked Issue 四个字段的顺序与 proposal-minimal 模板一致, Linked Issue 全限定; 附加的代码落点 / ship target / 基线数据 / 溯源四行可核 (comment 23915 为 2026-09-13 的 triage 5/5; `10CG/Aria#211` 创建于 2026-09-09)。
  - Rule #5: proposal 是主仓 blob (100644), 位于主仓 `openspec/changes/`, 不在 standards 子模块里。
  - rule6_note 段: 五个取值 (n/a / no / n/a / n/a / n/a) 都在 §D4 值域内; 「本 Spec 不触发 Rule #6」成立 (aria 子模块零改动)。
  - issue 的建议 1–3 与验收 1–3 都有落点 (见映射表); 偏离验收第 2 条的已列为 OQ-5 请 owner 裁, 引文逐字。
  - 范围: `0c41e53` 相对 v2 只改 proposal 与 RESULT, 另附六份 R2 审计报告; 没有范围外变更。
- **Phase 2 (质量)**
  - 1 条 major: 门的核心后果缺失, fail 可被读成不阻断。
  - 1 条 minor: v3 新引入的一处源码事实错误, 会进入对外反馈。
  - 其余是观察。

## Vote

**REVISE** —— major 没有清零。两处都只需改文字: D2 / D4 补一句「fail ⇒ 不得 ship」加两条后续路径, 并加一条 SC; RESULT (b)、Why 第 3 条和 D5.4 (ii) 去掉「首句」。改完下一轮有望收敛。

## 映射表

### issue 条目 → D / T / SC

| issue 条目 | D | T | SC | 备注 |
|---|---|---|---|---|
| 建议 1 (拆成两个义务, 不互相替代) | D1 | T1 | SC-1, SC-5 | 完整; 形状由 A/B 改为地板守卫 (OQ-5) |
| 建议 2 (SOT 与手册同批改) | D1 三处 + D2 / D3 / D6 | T1, T2, T5 | SC-1, SC-2, SC-7 至 SC-10 | 完整; 全仓查副本只有这三处 |
| 建议 3 (rule6_note 加栏, 空着即不合规) | D4 | T3 | SC-3 | 完整; 值域含 void / n/a |
| 验收 1 (历史版本对实跑) | 头部「基线数据」 | 已完成 | 无 | RESULT v3 数字复算一致 |
| 验收 2 (区分力为零时的规定动作) | OQ-5 | 待裁 | 无 | 引文逐字; 已选项与备选项各带代价 |
| 验收 3 (负控显著下降) | D2 同批负控 | T2 | SC-9 | 基线 3/10 对 10/10, 双侧 p = 0.0031 |

### D → T → SC

| D (子项) | T | SC | 备注 |
|---|---|---|---|
| D1 三处新句 | T1 | SC-1, SC-5 | 旧句三处各 1 行; 核心句逐字一致; 改前各 0 |
| D1 手册计数语 三条 → 四条 | T1 | SC-7 | 改前「边界三条」= 1、「边界四条」= 0 |
| D1 SOT §3 边界注 | T1 | SC-10 后半 | 改前 0 |
| D1 只改 description 时不跑场景 1 | T1 (随 SOT 新句) | 无 | 取决于 OQ-6, 不需要 SC |
| D1 旧句删除 (CLAUDE.md / SOT) | T1 | 无 | 缺口, 观察第 7 条 |
| D2 通过定义 / 参数 / 20 条 | T2 | SC-10 | 参数串都是 run_eval.py 的真实 flag |
| D2 负控门槛 / 连续 2 轮升级 | T2 | SC-9 | 完整 |
| D2 不设比较判据 | T2 | SC-5 | 召回面窄, 观察第 4 条 |
| D2 退化先判 fail / 作废不得 ship / fail 后处置 | T2 | 无 | Findings 第 1 条 |
| D2 套件文件 + version.yaml | T4 | SC-4 | 未裁分支一致; 「先审且改动」分支断开, 观察第 8 条 |
| D2 手册固定测试集表加 trigger 行 | T2 | 无 | D2 正文没提该表 |
| D3 六行前置表 | T2 | SC-2 | 10 个路径 `test -e` 全真 |
| D4 §4.1 五字段模板 | T3 | SC-3 | 改前五个字段名各 0 |
| D4 CLAUDE.md 指向 | T1 | SC-1 (同一句) | 与 T3 不再重叠 |
| D4 两套编号说明 | T2 / T3 (落点不清) | 无 | 观察第 10 条 |
| D4 authoring 路径 / 过渡期 | T6 (D5.3 的 issue) | SC-6 | 完整 |
| D5.1 拆 4a / 4b | T2 | SC-8 | 行首锚定问题, 观察第 5 条 |
| D5.2 无 trigger 套件的 issue | T6 | SC-6 | 标题计数随 T4 变化, 观察第 9 条 |
| D5.3 模板 issue | T6 | SC-6 | 完整 |
| D5.4 上游反馈 | T6 | SC-6 | 内容含错, Findings 第 2 条 |
| D5.5 `10CG/aria-standards#17` 分工 | T7 | SC-6 | 该单 open, 正文确为拟加「AB 范围」节, 与转述一致 |
| D6 §6 第三条 + 计数语 | T5 | SC-7 前半 | 改前「两个已知缺陷」= 1 |
| SOT 文件头 Version | T5 | SC-7 中段 | 无 D 锚 |
| 合并 / 双推 / 逐 remote 核验 | T7 | 无 | 流程任务, 与 CLAUDE.md 多远程两条约束一致 |
| `10CG/Aria#211` 回帖 | T8 | 无 | 流程任务 |

孤儿检查:
- SC 侧没有孤儿: SC-1 至 SC-10 都能挂到 D。
- T 侧: T7 / T8 是流程任务, 可以接受。
- D 侧没有 SC 的: D1 旧句删除、D2 fail / 作废的后果、D2 手册表行、D4 两套编号说明。其中只有「fail 的后果」进 Findings。

Key Deliverables 的 D 锚: CLAUDE.md 一条 (D1 + D4)、SOT 四个子项 (D1 / D1 / D4 / D6)、手册拆 4a / 4b (D5.1) 与边界段 (D1)、套件 (D2)、issue 与留言 (D5.2 至 D5.5) 都对得上。例外三处: SOT 文件头 Version 没有 D 锚; 手册表行挂 D2 但 D2 没提; 「两套编号说明 (D4)」挂在手册名下, 而 D4 正文写在 SOT §4.1。

OQ-3 未裁时的一致性: T4「OQ-3 裁定前不执行; ship 时仍未裁 ⇒ 标 deferred 并记入 D5.2 的 issue」、SC-4「T4 标 deferred 时本条改判『deferred 已记入 D5.2 的 issue』」、OQ-3「默认 (未裁时): T4 不执行」, 三处一致。

## 实跑记录

1. `python3 aria/skills/state-scanner/scripts/check_bare_issue_refs.py <proposal>` → 「裸 issue 引用: 0」, rc 0; 对 RESULT.md 跑 → 同样结果, rc 0。
2. 禁用字形 (python 逐字符扫, 区间 U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / U+03B1–03C9 / U+0391–03A9): proposal 0, RESULT 0; NUL 字节 0 / 0。
3. D1 表 (python 按行取出三行, 再取单元格): 三条旧句单元格与现状文件逐字相等; CLAUDE.md / SOT / 手册按行命中各 1, 子串命中各 1; 三条新句各含核心句 1 次; 现状三个文件的核心句各 0。
4. 全仓副本排查 (含子模块, 排除本 spec 目录): `grep -rnF "指令流程变动"`、`"一律照跑"`, 以及 `grep -rnE "description 变动|description 或指令|零裁量照跑|description 与指令面|description/frontmatter|改 description"` 扫 standards / aria / docs 架构与需求 / 手册 / README / CLAUDE.md。规范性命中只有 CLAUDE.md 第 101 行 (Rule #6 触发清单「改 description」, 与新规则不冲突)、第 110 行 (旧句)、SOT 第 33 行 (旧句)、手册第 273 行 (§场景 4 触发时机, 随 D5.1 重写) 与第 480 行 (旧句); 其余是 `.aria/audit-reports/`、`.aria/triage-comment.md`、一份 AB 答卷、一份 handoff。
5. `type grep` → shell 函数, 转调 `ugrep 7.8.4`; SC-5 正则用 `grep -cE` → 「exceeds complexity limits」, rc 2; `/usr/bin/grep` (GNU grep 3.8) `-cE` → 1, rc 0。
6. SC-5 正则 (python re): 「新版触发率不低于旧版」1; D2「不设比较判据」行原文 1; D2 负控门槛行 0; 三条 D1 新句 0 / 0 / 0; D2 + D3 正文去掉「不设比较判据」行后 0; 六个变体见观察第 4 条。
7. 改前反事实 (GNU grep): SOT 五个字段名各 0; 「两个已知缺陷」1、「三个已知缺陷」0; `**Version**: 1.0.0` 1、`**Version**: 1.1.0` 0; 「description hunk 不走本节」0。手册「边界三条」1、「边界四条」0; `^### 场景 4a` 0、`^### 场景 4b` 0; 「≤ 5/10」0; 「连续 2 轮」0; 四个参数串与「20 条」各 0; 「不设比较判据」0; `^#### ` 1。
8. D3 路径: 在基线目录里逐个 `test -e`, 10 个全真 (v1 new.json、v2 new.json、diag02-sibling-command-collision.jsonl、v2 negctrl.json、v3 negctrl.json、neutral-skill-SKILL.md、两份探针 json、v3 new.json、RESULT.md)。
9. 原始 json 复算 (query 级命中 := `trigger_rate ≥ 0.5`):

   | 轮 / 臂 | should-trigger run 级 (query 级) | should-not run 级 (query 级) |
   |---|---|---|
   | v1 new / old / negctrl / poscontrol | 4 (0) / 7 (1) / 0 (0) / 6 (0) | 四臂均 0 |
   | v2 new / old / negctrl / poscontrol | 27 (9) / 30 (10) / 27 (9) / 30 (10) | 四臂均 0 |
   | v3 new / old / negctrl / poscontrol | 30 (10) / 30 (10) / 8 (3) / 30 (10) | 四臂均 0 |
   | v4 overbroad | 30 (10) | 22 (7), 分布 0,3,3,1,3,1,3,3,3,2 |
   | v4 realroot | 30 (10) | 0 |

   v3 负控 should-trigger 分布 0,0,0,0,0,3,0,2,0,3, 即 3/3、2/3、3/3。
10. Fisher 精确检验 (超几何): query 级 10 对 5 单侧 0.0163; 10 对 6 单侧 0.0433; 10 对 3 双侧 0.0031; run 级 30 对 8 双侧 8.3e-10; 10 对 10 为 1.0。
11. run.log 逐臂: v2 起于 16:58:33 → new 11m26s / poscontrol 15m46s / negctrl 16m30s / old 17m39s; v3 起于 17:18:18 → old 10m39s / poscontrol 11m06s / new 11m07s / negctrl 12m03s; v4 起于 17:59:49 → overbroad 13m38s / realroot 13m54s。共 10 臂, 区间 10m39s–17m39s。
12. 探针 json: default `result` "97,yes", `total_cost_usd` 0.6044, `cache_creation_input_tokens` 27065, `output_tokens` 1190; project `result` "12,no", 0.0786, 3696, 5。两份的全部键里都没有技能或命令列表。manifest 的 isolation 字段写「技能数 97→13」, num_workers 为 4 (v1 清单)。
13. `aria-plugin-benchmarks/ab-results/2026-09-04-v1.69.1-spec-drafter-rule5-hunkA/` 下 timing.json 共 8 个: `duration_ms` 合计 27.11 分钟, `total_tokens` 合计 652757。
14. skill 计数: `aria/skills` 下目录 43, 含 SKILL.md 的 42, `git -C aria ls-files 'skills/*/SKILL.md'` 42; 唯一没有 SKILL.md 的目录 `issue-triage-workspace`, 由 `.gitignore` 第 7 行 `skills/*-workspace/` 忽略。`ab-suite/version.yaml` 为 1.5.0; `ab-suite/trigger/` 不存在。
15. run_eval.py (marketplace 与缓存 `bb335391eb83` 两份 `diff -q` 相同): 第 52 行 clean_name; 第 54 行文件名; 第 60–66 行命令文件内容 (frontmatter description + `# {skill_name}` + `This skill handles: {skill_description}`); 第 147 / 164 / 166 行用 `clean_name in …` 检测; 第 232 / 234 行 did_pass; 第 261–268 行参数 (`--num-workers` 默认 10、`--timeout` 默认 30、`--runs-per-query` 默认 3、`--trigger-threshold` 默认 0.5、`--model`)。
16. `git show 55bc9f3:<RESULT>` 里的 (b): 「命令文件名与正文 = `<skill_name>-skill-<id>` / `# <skill_name>`」(两处, 没有「首句」); v3 改成三处。`55bc9f3` 版 proposal 的 Impact 原文「并行约 12–14 分钟 / 串行约 24 分钟」。
17. issue 实查: `10CG/Aria#211` open, 创建于 2026-09-09, 评论 1 条 (comment 23915, 2026-09-13, triage 5/5, 写「属 Level 2 规范变更」); OQ-5 引文与 issue 验收第 2 条用 python 逐字比较 → `EQUAL: True`。`10CG/aria-standards#17` open, 正文提议「在 skill-benchmark-exemption.md 增一节『AB 范围』」, 与 D5.5 的转述一致。
18. LEVEL_GUIDE §跨模块判断原文: 「跨模块条件 (满足任一): 涉及 2 个及以上模块 / 修改 shared/ 目录 / 需要 API 契约变更 / 影响多个子模块; 跨模块 → 自动提升为 Level 3」; §模块检测的模块映射中 standards 的路径为 `standards/**, .claude/**`, 另外三个模块是 mobile / backend / shared。
19. `grep -rn "Level 2 cycle"` (排除审计报告): 只有本 proposal 两处, 加上两份旧 handoff 里的无关用法; 2026-09-13 的 handoff 对 `10CG/Aria#211` 只写了「建议先 triage」。
20. git: `0c41e53` 的改动 = proposal + RESULT + 六份 R2 审计报告; `git ls-tree HEAD`: proposal 100644 blob, `aria-plugin-benchmarks` 040000 tree, aria / standards 160000。
21. proposal 中的 fail / 阻断类用词: fail 出现在 D2 退化子项、D4 值域、手册旧句「fail-closed」三处; 「不得 ship」2 处 (D2 作废子项、D4 合规规则), 都挂在 void 上。
22. 审计报告文件时间: R1 各席 17:48–17:58, 聚合 18:01:17 (文件名时间 17:36:16); R2 各席 11:17–11:58, 聚合 12:02:58 (文件名时间 11:08:40)。
