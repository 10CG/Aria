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
timestamp: 2026-09-14T13:20:04.452Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [code-reviewer]
---

# post_spec R4 — code-reviewer 席 (Phase 1 规范合规 + Phase 2 质量)

被审对象: `openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md` rework v4 @ 主仓 HEAD `e822829`; 基线目录 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/` (RESULT.md v4 与原始产物, 含新增 `v5-mildcreep-opus5/`)。只审不改, 唯一写入是本报告。

独立性: 本轮其他席的 R4 报告没有读; 共用 scratchpad 里有一个 `r4-qa/` 目录, 未打开。R3 只读了聚合报告与本席报告。下文数字都来自实跑, 命令与输出见「实跑记录」。

## R3 对账

范围: 本席 R3 报告 Findings 的 2 条。

| 序号 | R3 条目 | v4 落点 | 状态 | 核对依据 |
|---|---|---|---|---|
| 1 | [major] 场景 4b 判 fail 后没有后果; 有意改触发面导致的 fail 没有路径 | §D2「fail 的后果」子项; §D4 合规规则; §SC-9 | closed | D2 新增: fail ⇒ 不得 ship (与 void 同为义务未完成); 处置二选一 —— 修 description 直到门通过, 或 fail 来自有意收窄 / 拓宽触发面时先改套件 (升 `ab-suite/version.yaml`, 按 OQ-7 审阅) 再重跑; 两条都不走 ⇒ 升级 owner; rule6_note 记 fail 与所走的处置。D4 改为「`fail` 或 `void` ⇒ 义务未完成, 不得 ship (处置见 D2)」。R3 所说「按字面可读成跑完即合规」已没有文字依据。残留三处都不改变本条结论: SC-9 对 fail 后果没有区分力 (Findings 第 3 条); 修后重跑时 rule6_note 记哪次结果没说清 (观察第 3 条); 环境失效造成的假红现在会触发「改 description」(观察第 4 条) |
| 2 | [minor] 「正文首句 `This skill handles:` 嵌入技能名」与 run_eval.py 不符 | §Why 第 3 条; §D5.4 (ii); RESULT v4 §结论 3(b) | closed | run_eval.py (marketplace 与两份缓存, 三份逐字节相同): 第 52 行 `clean_name = f"{skill_name}-skill-{unique_id}"`, 第 54 行命令文件名 `f"{clean_name}.md"`, 第 65 行 `f"# {skill_name}\n\n"`, 第 66 行 `f"This skill handles: {skill_description}\n"`。v4 三处都改成「文件名与 `# <skill_name>` 标题两处嵌入技能名, 首句嵌的是 description」, 与源码一致。`grep -n 首句` 只剩勘正后的这几处与 RESULT 版本行。D5.4 (ii) 写「两处都要改」, 比我 R3 建议的「标题可选」更严, 没有事实错误 |

合计: closed 2 / partially 0 / open 0。

## Findings

- [major] architecture/proposal.md §OQ-7 (decision): 自主模式「(A) 与 AD10 冲突 ⇒ 可行做法只有 (B)」不成立: AD10 回滚路径 Level 2 明列「只对高风险 issue 触发的 optional human gate」; AD5 的 S_FAIL 可承接 fail-closed (无已审套件的 skill 不在自主模式改 description); 另可离线批量预审。owner 只拿到一个选项。
- [minor] documentation/proposal.md §D6 + RESULT.md §v5 (issue): v4 把「已验证的破坏类型只有两类」改成「判得出的破坏类型只有两类」; RESULT 标「按预登记」, 却把预登记原文「只承诺两类破坏」写成「只判得出」。能力上限的全称否定没有实测依据, T5 逐字写入 SOT §6。
- [minor] testing/proposal.md §SC-1 §SC-9 (issue): v4 两处实质修复没有能变红的 SC: 删掉 D2「fail 的后果」, SC-9「不得 ship ≥ 1」由作废句单独满足; 按 v3 旧版新句落地 (description 只跑 4b), SC-1 / SC-5 / SC-7 全绿。Level 2 验收只靠 SC。

计数: critical 0 / major 1 / minor 2。两条 minor 列入 Findings 的理由: 第 2 条是 T5 要逐字写进 standards (单独发布的规范仓) 的正文, ship 后再改要另走一个 cycle; 第 3 条是 v4 两处修复 (D1 回改为 fail-closed、D2 fail 后果) 唯一的机械锁, 而 Level 2 不产 tasks.md (OQ-4), T1–T8 的验收只有这组 SC。

## Findings 证据与修法

1. **OQ-7 自主模式「只有 (B)」(major)**
   - 原文: 「(A) 会在 S7 之外再加一个, 与 AD10 冲突。可行做法只有 (B), 并把「新套件审阅」并进 S7 的签字材料」。前半句成立 —— AD10 §决策逐字「只保留 1 个人类审批 gate ... 不在 dispatch 前 (S1→S2) 设 human gate, 不在 review 中段 (S5→S6) 设 human gate」。后半句「只有 (B)」没有依据, 至少有三条路与现行架构文书相容:
     - 条件式人工 gate: AD10 §回滚路径逐字「Level 2: 在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」, §选型理由第 4 条「可逐步收紧或放松 ... 方向对称」。「改一个没有已审套件的 skill 的 description」完全可以归为这里的高风险 issue。
     - fail-closed: AD5「S_FAIL 作为 universal sink, 可从任意状态进入, 并触发 replay / retry / escalate 决策」。自主模式遇到「改 description 而该 skill 无 owner 已审套件」时进 S_FAIL, 或由 Layer 1 triage 不派发, 回交互模式做。不新增人工 gate, 也不让 Layer 2 自建套件自己判门。
     - 离线批量预审: owner 在流水线之外成批审完套件, 自主模式只用已审套件, 流水线里没有等待点。
   - 为什么是 major: 这是事实性断言, 也是推荐项「自主模式 (B) 且审阅并入 S7」的唯一论据。(B) 在自主模式下意味着 Layer 2 自建套件并自己判门, 配合 D2 fail 处置 (2) 还能在 fail 后改套件再跑, 到 S7 才有人看。CLAUDE.md 写明「自主运行时无人复议, Rule #10 更硬」; fail-closed 这条恰是最贴合规则 #10 的选项, 却被写成不存在。owner 是在一个被收窄的选项集里做裁定。
   - 事实依据段已独立复算, 成立: aria-runner-bot 在 aria-plugin 33 次提交; 触及 SKILL.md 的非 merge 提交 6 次 (含 2 个 merge 提交为 8 次); 这些提交的 description 前后逐文件对比 0 处变化; bot 的发版提交实为 8 次 (「至少 4 次」是成立的下限)。建议注明「6 次」按非 merge 提交计。
   - 修法: 自主模式一栏改成三到四个选项, 各写代价 —— (B) 并入 S7; (C) fail-closed, 无已审套件则自主模式不改该 skill 的 description (S_FAIL / 回交互模式), 代价是自主模式在其余 41 个 skill 上暂时不能改 description; (D) 走 AD10 回滚路径 Level 2 加条件 gate, 代价是要修订 AD10; (E) 离线批量预审, 代价是 owner 一次性投入 (按 OQ-7 自估每个约 15 分钟, 41 个约 10 小时)。推荐项可以不变, 但要删掉「只有」。

2. **D6 / RESULT v5 的能力上限全称句 (minor, 不改不能进 Phase B)**
   - `git diff 0c41e53..e822829` 中 D6 引号内正文由 v3「已验证的破坏类型只有删领域词与显式强制过宽两类」改为 v4「判得出的破坏类型只有删领域词与显式强制过宽两类」。前者说的是验证范围 (实测只覆盖这两类), 后者说的是能力上限 (别的破坏判不出)。基线只测过这两类加一次自然扩张, 没有任何数据支持「其他类型判不出」。
   - 同一 Spec 里其余几处都写对了: Why 第 2 条「已验证恰两类破坏」、D2「只承诺已验证的两类破坏」、RESULT §结论 2「已验证的破坏类型恰两类」。而且 D2 fail 处置 (2) 预设「有意收窄触发面」会判 fail, 这本身就不在那两类里 (收窄一个使用场景不等于删光领域词)。
   - RESULT v5 小节第一条: 「按预登记: mildcreep 门通过 ⇒ 这是对「守卫只判得出两类破坏」这条局限的实证确认」。`PREREGISTRATION.md` 原文: 「判「在本套件上, 该幅度的自然扩张不被守卫判为改坏」—— 这是对 §D2「只承诺两类破坏」局限的实证确认」。预登记的意义在于判读跑后不改; 以「按预登记」为名改写判读, 读者分不清哪句是跑前写定的。
   - 修法: D6「判得出的」改回「已验证的」(或「已验证判得出的」); RESULT v5 那句按预登记原文写「在本套件上, 该幅度的自然扩张不被判为改坏 —— 对 §D2『只承诺两类破坏』这条局限的实证确认」, RESULT 版本号递增。

3. **两处实质修复没有能变红的 SC (minor, 不改不能进 Phase B)**
   - 反事实 A (内存中模拟, 未写文件): 把 D2 小节里「fail 的后果」那一条删掉, 「不得 ship」从 2 处降到 1 处 (作废子项那处), SC-9「各 ≥ 1 次」仍然绿。反过来删掉作废子项, 也还剩 1 处, 同样绿。SC-9 这一项是 v4 为锁住 R3 major 加的, 结果两边都锁不住。SC-3 只查 §4.1 的字段名、`void` / `n/a` 与「两套编号」, 不查 D4 那条「`fail` 或 `void` ⇒ 不得 ship」—— SOT 落点上 fail 的后果完全没有 SC。
   - 反事实 B: 用 v3 (`0c41e53`) 的三条新句替换三处旧句 (即 CLAUDE.md「`description` 变动一律跑场景 4b」、SOT「只涉及触发面时不跑场景 1」、手册「description 变动零裁量跑场景 4b」), SC-1 三处核心句各 1、SC-5 三行各 0、SC-7「边界四条」1 /「边界三条」0, SC-10 后半不受影响 —— 全绿。v4 的 D1 回改 (回应 R3 聚合 major 第 2 条) 在 SC 层面与 v3 分不开。
   - 修法: SC-1 改为三条新句按整句 `grep -cF` 各 = 1 (手册那条先去掉表格里外层的代码标记, 见观察第 11 条); 整句相等就同时锁住核心句与「照跑场景 1 / 另须跑场景 4b」。SC-9 改为「不得 ship」在 4b 小节 ≥ 2 次, 或按行判 (含「fail」的行里有「不得 ship」, 含「作废」的行里也有)。SC-3 补一项: §4.1 含「`fail` 或 `void`」那条合规句。三处改前都是 0, 反事实成立。

## 观察 (不进收敛比较键, 不影响 vote)

1. **D5.5 首句是 v3 口径残留**: 「本 Spec 定**深度** (按 hunk 类型跑场景 1 还是 4b)」里的「还是」是 v3 的二选一, 与 v4 D1「description hunk ⇒ 场景 1 另加场景 4b」不一致。紧接的「交叉点: 凡跑场景 1 (包括只改 description 时)」是 v4 口径, 通读能纠正。但 T7 给 `10CG/aria-standards#17` 的分工留言是照 D5.5 写的, 建议改为「(按 hunk 类型决定是否另加场景 4b)」。`grep -n hunk` 全文只有这一处残留。三条新句、D1 正文、Impact、OQ-6 与 rule6_note 的 AI 流程判断清单口径一致 (清单删去了 v3 的「只改 description 时不跑场景 1」, 新增 v5 换模型一项)。
2. **D4 合规规则没跟上 D1 回改**: v3 允许只改 description 时 `scenario1: not_required`, 所以 D4 只写了 scenario4b 的不合规情形。v4 已不设放宽, §4.1 仍只写「`description_changed: yes` 而 `scenario4b` 为空 / not_required / n/a ⇒ 不合规」。审阅者照 §4.1 看 `description_changed: yes` + `scenario1: not_required` + `scenario4b: <目录> pass` 会判合规。建议补一句「`description_changed: yes` 而 `scenario1` 为 `not_required` 或 `n/a` ⇒ 不合规」。同一 SOT 的 §2 新句已写明照跑场景 1, 所以不列 Findings。
3. **fail 后重跑怎么记**: D2 写「rule6_note 记 `scenario4b: <结果目录> fail` 与所走的处置」, 而 D4 的 scenario4b 是单值, 且「fail ⇒ 不得 ship」。修好后重跑通过时, 按字面这一格仍是 fail, 永远不能 ship; 改写成 pass 又丢了 fail 的记录。建议写明「scenario4b 记最后一次结果, 之前 fail 的目录与处置写在同行注释」。另外处置 (1)「修正 description 直到门通过」没有轮数上限 (作废有「连续 2 轮」), 每轮约 10 美元、11–20 分钟。
4. **环境失效的假红现在会驱动错误动作** (R3 观察第 12 条, v4 未采纳, 后果变重): 判定顺序是门先判, 负控只在门通过后才起作用。按 v4 规则回放 v2 (合成名泄漏): v2 new (真 v1.73.0) query 级 9/10 ⇒ fail, 而同批负控 9/10 已说明这一轮不可用。v3 时 fail 没有后果, 只是误报; v4 下 fail ⇒ 不得 ship + 修 description, 执行者会去改一份正确的 description, 甚至改得更「pushy」来压过坏环境。D3 前置能排除已知的两种失效, 排除不了未知的。建议加「fail 且负控 ≥ 6/10 ⇒ 按作废处理 (先修环境)」, 并在 fail 时加跑现行 description 作对照 (现行也 fail ⇒ 查环境与套件, 不改 description)。
5. **D2 处置 (2) 与 OQ-7 (B) 叠加**: 因 fail 而改的套件按 D4 属「未经 owner 审阅」, 重跑结果是 `pass provisional`, 不在「不得 ship」之列。OQ-7 若在交互模式裁 (B), 执行者就能 fail → 改自己的考卷 → ship, owner 事后才审。OQ-7 (B) 写的代价只覆盖「首次建套件偏弱」, 没覆盖这种情况。建议 D2 写「因 fail 而改的套件不适用 provisional, 须 owner 审后再作门」, 或把这一点写进 OQ-7 (B) 的代价。自主模式下 S7 在 merge 前, 能兜住。
6. **D2 新增的「近似误触须覆盖最可能被扩到的相邻任务」与 T4 / SC-4 / OQ-8 推荐冲突**: D2 自己的括号写着「v5: 本套件对『整理收尾材料』这一幅度的扩张不敏感」。OQ-3 若裁「接受」, T4 按 SC-4 逐字节搬入基线套件, 按 D2 新要求入库当天就不合规; 而 OQ-8 的推荐是「判据不改」、不补套件。建议 OQ-3 / OQ-8 各写一句这层关系。该要求本身是判断性的 (谁来定「最可能」), 没有 SC, 也难写成 SC。
7. **v5 被评 description 的改动没有全部披露**: mildcreep 相对 new 除了四处增补, 还把「`openspec/archive/` 目录」改成了「`archive/` 目录」(删掉 `openspec/`, 这本身也是一处扩张)。RESULT v5 表写「原文 + ...」, §结论 2 与 D2 都没提; D2 只列了四处增补中的三处 (漏「整理归档文档」)。不影响结论 (扩张更多仍不判红), 但被测 description 应逐字给出或写全差异。
8. **RESULT 头部「模型」行没更新**: 仍只写 `claude-fable-5-1`, v5 用的是 `claude-opus-5` (只在 v5 小节写了)。D3 第 6 行要求产物写明工具版本; 建议头部改为「v1–v4 fable / v5 opus-5」, 并补 v5 的 Claude Code 版本 (本机当前 2.1.269)。已核对五份运行脚本都显式传了 `--model`: v1–v4 为 fable, v5 为 opus-5。
9. **OQ-9 两处**: 「与 v3 同构的三臂」不准, v3 是四臂 (new / old / negctrl / poscontrol), 所说「一个坏 description」对应的是 v4 的过宽臂; 建议写「v3 配置下 正确 / 负控 / 过宽 三臂」。另外「先验证再启用」没说验证完成前自主模式遇到 description 变动怎么办 (阻断? 跑并标 provisional?); 跳过 4b 属于规则 #10 所禁的自行豁免, 过渡期行为需要写明。
10. **SC-10 的空集**: 「含『参数钉死』的那一行须同时含 ...」—— 如果 T2 写参数时没用「参数钉死」这个词, 机械实现可能真空成立。建议仿 SC-2 写「恰 1 行, 0 行判红」。
11. **D1 表第 3 行的代码标记**: 手册那一行的旧句与新句在表里被外层反引号包成代码, 第 1、2 行的反引号则是原文的一部分。按单元格原样 `grep -F`, 第 3 行命中 0; 去掉外层反引号后命中 1 (第 480 行)。「各恰 1 次」成立, 但要按这个约定执行。建议表前加一句说明 (Findings 第 3 条的整句 SC 也用得上)。
12. **几处措辞可再收**: D1「能观测后一半」—— with-skill 臂读到 description 原文, 说明有作用面; 断言测不测得到取决于套件, 唯一的历史数据点 (`10CG/aria-plugin#190` comment 22921) 是 0 条有区分力的 expectation。建议写「有作用面」。Why 第 2 条与 D2 的「守卫判得出什么, 由套件里的近似误触决定」只说了 should-not 一侧, should-trigger 一侧由 should-trigger query 决定。「执行者无法可靠判断」只有一个例子支撑, 但推出的是 fail-closed (多跑), 方向保守, 可以接受。
13. **时长区间的算法没写**: 并行区间用单臂区间向上取整 (fable 10m39s→11、17m39s→18; opus 15m18s→16、19m41s→20), 串行区间用最快两臂与最慢两臂之和四舍五入 (fable 21m45s→22、34m09s→34; opus 33m34s→34、37m57s→38)。两组模型用的是同一套做法, 可复算; 建议 RESULT 时长段注一句。
14. **R3 观察中 v4 未动的** (都不阻塞): 第 4 条 (SC-5 自测描述「『不设比较判据』行 ... 为 0」, 该行原样实跑仍是 1); 第 5 条 (小节边界与 SC-8 行首锚定); 第 8 条 (OQ-3「先审且改动」分支与 SC-4 接不上); 第 9 条 (T4 不执行时应为 42 个); 第 14 条 (`--model` 列在「参数钉死」里); 第 16 条 (D5.3 那张 issue 的 AB baseline 污染提示)。另外 OQ-4「post_spec 每轮约半小时」: 按报告文件时间, R2 约 54 分钟, R3 约 50 分钟 (文件名时间 12:07:10, 聚合 12:57)。

## 优点

- 两条 R3 Findings 都改在要害上: fail 的后果写成与 void 同级的「不得 ship」, 并给了有意改触发面时的正当路径 (改套件、升版、审阅); 「首句」一处按源码改正, Why / D5.4 / RESULT 三处同步。
- v5 按预登记补跑, 做法规范: 预登记文件 mtime (12:28:13.730Z) 早于第一份结果 (12:43:31Z); 仓内 v5 产物与 scratchpad 原件逐字节相同; 三臂同批、只做臂间比较; 换模型写进了 rule6_note 的 AI 流程判断清单。
- D1 回改为 fail-closed 后与 issue 原建议 1 逐项一致; rule6_note 清单同步删掉了已不成立的「只改 description 时不跑场景 1」。
- OQ-7 的事实依据经独立复算成立; Impact 新增「Layer 2 适用性未验证」一条, 并单开 OQ-9。
- 新增数字全部可以从原始产物复算 (见数字对账)。

## 数字对账 (v4 proposal ↔ RESULT v4 ↔ 原始产物)

| 数字 | proposal 位置 | RESULT 位置 | 原始产物复算 | 结论 |
|---|---|---|---|---|
| v5 new 30/30 (10/10), should-not 0/30 | §OQ-8 | v5 表 | new.json: 30 (10) / 0 (0), 20/20 pass | 一致 |
| v5 negctrl 0/30 (0/10) | §D2 负控构造; §OQ-8 | v5 表 | negctrl.json: 0 (0) / 0 (0), 10/20 pass | 一致 |
| v5 mildcreep 30/30, should-not 全 0/3 | §Why 第 2 条; §D2; §OQ-8 | v5 表; §结论 2 | mildcreep.json: 30 (10) / 0, 十条分布全 0 | 一致 |
| 15m18s–19m41s | §Impact | v5 小节; §时长与成本 | run.log: mildcreep 15m18s / new 18m16s / negctrl 19m41s | 一致 |
| opus 并行 16–20 / 串行 34–38 分钟 | 无 (并进区间) | §时长与成本 | 单臂区间向上取整; 最快两臂 33m34s、最慢两臂 37m57s | 一致 (算法见观察第 13 条) |
| 并行 11–20 / 串行 22–38 分钟 | §Impact; §OQ-3; §OQ-7 | 无 (按模型分列) | fable 11–18 与 opus 16–20 取并; 22–34 与 34–38 取并 | 一致 |
| 13 臂 | §Impact | 无 | v2 四 + v3 四 + v4 二 + v5 三 | 一致 |
| 五轮九臂 | §Why | 无 | v1–v4 六个臂名 + v5 三臂 | 一致 |
| 33 / 6 / 至少 4 / 0 | §OQ-7 | 无 | 33; 非 merge 6 (含 merge 8); 发版提交 8; description 变化 0 | 一致 (计数口径见 Findings 第 1 条) |
| 约 180 次 / 约 50 分钟 | §OQ-9 | 无 | 3 × 60; 60 × 45–54 秒 = 45–54 分钟 | 一致 |
| 30/30、8/30、22/30、0.0031、0.016 / 0.043、27.1 分钟 | 未改 | 未改 | R3 已复算 | 一致 |

## Verdict

**PASS_WITH_WARNINGS** —— critical 0 / major 1 / minor 2 (Findings); 观察 14 条不计入。

- **Phase 1 (规范合规): PASS**
  - `check_bare_issue_refs.py` 对 proposal 与 RESULT 各跑一次, 都是「裸 issue 引用: 0」, rc 0。
  - 禁用字形 (U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / 希腊字母大小写): proposal、RESULT、PREREGISTRATION 三个文件 0 命中; NUL 字节 0。
  - 头部: Level / Status / Created / Linked Issue 四字段顺序不变; Status 写到「R3 ... 0C / 5M / 6m (去重后) → rework v4 (本版), 待 R4」, 与 R3 聚合报告一致; 基线数据指向 RESULT v4。
  - rule6_note: 五个取值 `n/a` / `no` / `n/a` / `n/a` / `n/a` 都在 §D4 值域内; 「本 Spec 不触发 Rule #6」成立 (本范围 aria gitlink 零改动, 本地 aria HEAD `1cb3872` 与 origin master 一致)。
  - D1 表三条旧句在三个现状文件里各恰 1 次 (第 3 行需去外层代码标记, 观察第 11 条); 核心句在三条新句里逐字相同, 各 1 次; 三个现状文件的核心句各 0。
  - 范围: `e822829` = proposal + RESULT + `run_arms_v5.sh` + `v5-mildcreep-opus5/` 五个文件 + 六份 R3 审计报告; CLAUDE.md、手册、SOT 自 R3 以来未改动; 没有范围外变更。
  - T7 的合并与推送步骤 (本地 `--no-ff` merge、双推、逐 remote `ls-remote` 比对 SHA) 与 CLAUDE.md 多远程两条约束一致。
- **Phase 2 (质量)**
  - 1 条 major: OQ-7 用一条不成立的「只有」收窄了 owner 的选项。
  - 2 条 minor: 一处要写进 SOT 的全称句退回到 v3 之前的写法; v4 两处修复没有能变红的 SC。

## Vote

**REVISE** —— major 没有清零。三处都只改文字, 不需要新的实跑: OQ-7 自主模式一栏补上 (C) fail-closed 等选项并删掉「只有」; D6 与 RESULT v5 分别改回「已验证的」与预登记原文; SC-1 改整句判、SC-9 改 ≥ 2 次 (或按行判)、SC-3 补 fail 句。

## 映射表

### issue 条目 → D / T / SC

| issue 条目 | D | T | SC | 备注 |
|---|---|---|---|---|
| 建议 1 (拆成两个义务, 不互相替代) | D1 | T1 | SC-1, SC-5 | v4 与原建议逐项一致; 形状为地板守卫 (OQ-5); SC 分不开 v3 / v4 (Findings 第 3 条) |
| 建议 2 (SOT 与手册同批改) | D1 三处 + D2 / D3 / D6 | T1, T2, T5 | SC-1, SC-2, SC-7 至 SC-10 | 完整 |
| 建议 3 (rule6_note 加栏, 空着即不合规) | D4 | T3 | SC-3 | 值域含 void / n/a; 合规规则缺 scenario1 一项 (观察第 2 条) |
| 验收 1 (历史版本对实跑) | 头部「基线数据」 | 已完成 | 无 | RESULT v4 数字复算一致 |
| 验收 2 (区分力为零时的规定动作) | OQ-5 | 待裁 | 无 | 引文未改 (R3 已逐字比对) |
| 验收 3 (负控显著下降) | D2 同批负控 | T2 | SC-9 | 基线 3/10 对 10/10, 双侧 p = 0.0031; v5 新构造负控 0/10 |

### D → T → SC

| D (子项) | T | SC | 备注 |
|---|---|---|---|
| D1 三处新句 | T1 | SC-1, SC-5 | 核心句各 1; 落 v3 旧版新句也全绿 (Findings 第 3 条) |
| D1 只改 description 也照跑场景 1 / 不设放宽 | T1 | 无有效 SC | Findings 第 3 条 |
| D1 旧句删除 (CLAUDE.md / SOT) | T1 | 无 | 手册一处由 SC-7「边界三条」= 0 兜住 (R3 观察第 7 条) |
| D1 手册 三条 → 四条 | T1 | SC-7 | 改前「边界三条」1、「边界四条」0 |
| D1 SOT §3 边界注 | T1 | SC-10 后半 | 改前 0 |
| D2 通过定义 / 参数 / 20 条 | T2 | SC-10 | 按行判; 空集未写 (观察第 10 条) |
| D2 负控门槛 / 连续 2 轮 | T2 | SC-9 | 完整 |
| D2 fail 的后果 / 作废不得 ship | T2 | SC-9 (无区分力) | Findings 第 3 条 |
| D2 不设比较判据 | T2 | SC-5 | 三条新句与 D2 + D3 正文均 0 |
| D2 近似误触须覆盖相邻任务 | T2 | 无 | 判断性要求 (观察第 6 条) |
| D2 套件文件 + version.yaml | T4 | SC-4 | 未裁分支三处一致 |
| D2 手册固定测试集表加 trigger 行 | T2 | 无 | D2 正文未提 (R3 观察第 13 条) |
| D3 六行前置表 | T2 | SC-2 | 只取第三列; v4 只改了第 4 行文字 (v3 → v4), 路径不变 |
| D4 §4.1 五字段 / 值域 / 两套编号 | T3 (手册说明随 T2) | SC-3 | 改前五个字段名各 0 |
| D4 fail / void 不得 ship; provisional 后缀 | T3 | 无 | Findings 第 3 条修法含 SC-3 补项 |
| D4 authoring 路径 / 过渡期 | T6 (D5.3 的 issue) | SC-6 | 完整 |
| D5.1 拆 4a / 4b | T2 | SC-8 | 行首锚定问题仍在 (R3 观察第 5 条) |
| D5.2 / D5.3 两张 issue | T6 | SC-6 | 标题计数随 T4 变 (R3 观察第 9 条) |
| D5.4 上游反馈 | T6 | SC-6 | 内容已勘正 (R3 对账第 2 条) |
| D5.5 `10CG/aria-standards#17` 分工 | T7 | SC-6 | 首句残留 v3 口径 (观察第 1 条) |
| D6 §6 第三条 + 计数语 | T5 | SC-7 前半 | 第三条正文无 SC; 措辞见 Findings 第 2 条 |
| SOT 文件头 Version | T5 | SC-7 中段 | 无 D 锚 (R3 观察第 13 条) |
| 合并 / 双推 / 逐 remote 核验 | T7 | 无 | 流程任务 |
| `10CG/Aria#211` 回帖 | T8 | 无 | 流程任务 |

孤儿检查:
- SC 侧没有孤儿: SC-1 至 SC-10 都挂得到 D。
- T 侧: T7 后半与 T8 是流程任务, 可以接受。
- D 侧没有有效 SC 的: D1 回改、D1 旧句删除 (CLAUDE.md / SOT)、D2 fail 后果、D2 近似误触要求、D2 手册表行、D4 合规规则、D6 第三条正文。其中 D1 回改与 D2 fail 后果进 Findings 第 3 条。

## 实跑记录

1. `python3 aria/skills/state-scanner/scripts/check_bare_issue_refs.py <proposal>` → 「裸 issue 引用: 0」, rc 0; 对 RESULT.md 跑 → 同样, rc 0。
2. 禁用字形 (python 逐字符扫, 区间 U+2460–24FF / U+2776–2793 / U+3251–325F / U+32B1–32BF / U+03B1–03C9 / U+0391–03A9): proposal 0、RESULT 0、PREREGISTRATION 0; NUL 字节 0 / 0 / 0。
3. D1 表 (python 取三行单元格): CLAUDE.md 旧句子串 1 次 (第 110 行); SOT 1 次 (第 33 行); 手册按单元格原样 0 次, 去外层反引号后 1 次 (第 480 行, 第三项「拿不准照跑」在第 481 行); 三条新句各含核心句 1 次; 三个现状文件核心句各 0。
4. SC-5 正则 (python re): 三条 v4 新句 0 / 0 / 0; D2 + D3 正文去掉含「不设比较判据」的行后 0; 「不设比较判据」行原样 1。
5. 反事实落地 (内存中字符串替换, 未写文件): 落 v4 新句 → SC-1 1 / 1 / 1、SC-5 0 / 0 / 0、「边界四条」1、「边界三条」0; 落 v3 (`0c41e53`) 新句 → 结果完全相同。
6. SC-9 反事实 (取 v4 D2 小节): 「不得 ship」2 处; 删「fail 的后果」子项后 1; 删作废子项后 1; 门槛 ≥ 1, 两种删法都仍绿。SC 段含「fail」的只有 SC-9 一条。D2 含「参数钉死」的行 1 行。
7. `run_eval.py`: marketplace 与缓存 `bb335391eb83`、`unknown` 三份 `diff -q` 相同; 第 51–54 行 (uuid / clean_name / 命令文件名), 第 60–67 行 (frontmatter description + `# {skill_name}` + `This skill handles: {skill_description}`), 第 147 / 152 / 164 / 166 行检测, 第 231–234 行 did_pass, 第 264–268 行参数默认值。
8. `grep -n 首句`: proposal 只在 D5.4 (ii) 勘正括号内; RESULT 只在 §结论 3(b) 勘正括号内与版本行。
9. v5 原始 json: new should 30 (10) / should-not 0 (0), 20/20 pass; negctrl 0 (0) / 0 (0), 10/20 pass; mildcreep 30 (10) / 0 (0), 20/20 pass, should-not 十条全 0; 三份 `skill_name` 都是 `helper`, 每 query 3 runs。scratchpad 中三份 `.err` 的 `Warning` 计数均为 0, 末行 `Results: 20/20` / `10/20` / `20/20`。
10. run.log 逐臂: v2 new 11m26s / negctrl 16m30s / poscontrol 15m46s / old 17m39s; v3 poscontrol 11m06s / old 10m39s / negctrl 12m03s / new 11m07s; v4 overbroad 13m38s / realroot 13m54s; v5 mildcreep 15m18s / new 18m16s / negctrl 19m41s。共 13 臂。
11. 预登记时序: scratchpad `trigger-results-v5/PREREGISTRATION.md` mtime 2026-09-14T12:28:13.730Z, `run_arms_v5.sh` 12:28:13.739Z, run.log 起始 12:28:13Z, 第一份结果 `mildcreep.json` 12:43:31Z。仓内 PREREGISTRATION / 三份 json / run.log / `run_arms_v5.sh` 与 scratchpad 原件 `cmp` 全部相同。
12. description 差异 (difflib): mildcreep 相对 new = 插入「与相关文档」、删除「openspec/」、插入「，整理项目收尾材料」、插入「、"整理归档文档"、"收尾整理"」; v5 new 与 v3 new 的 description 逐字相同。
13. 五份运行脚本的 `--model`: `run_arms.sh` fable (2 处, `--num-workers 4`), v2–v4 fable (`--num-workers 1`), v5 `claude-opus-5` (`--num-workers 1`)。
14. aria-runner-bot (aria 子模块, `git log --all`): 33 次提交; 触及 SKILL.md 的 8 次, 其中 2 次是 merge (`b9f5446d`、`36948718`), 非 merge 6 次; 逐文件比对 frontmatter description 前后, 11 个文件次全部未变; 作者为 bot 的 `chore(release)` 提交 8 次 (v1.54.0 至 v1.70.0); 时间跨度 2026-07-05 至 2026-09-06。本地 aria HEAD `1cb3872` 与 `git ls-remote origin` 的 master 相同。
15. 架构文书: `aria-orchestrator/docs/architecture-decisions.md` §AD10 决策段 (「只保留 1 个人类审批 gate ... 不在 dispatch 前 (S1→S2) 设 human gate, 不在 review 中段 (S5→S6) 设 human gate」), §回滚路径「Level 2: 在 S5_REVIEWING 中间插入一个 optional human gate (只对高风险 issue 触发)」(第 812 行), §选型理由第 4 条「可逐步收紧或放松」; §AD5「S_FAIL 作为 universal sink, 可从任意状态进入, 并触发 replay / retry / escalate 决策」(第 401 行)。
16. 手册现状锚点: `### 目录结构` 第 42 行, `### 固定测试集 vs 临时测试` 第 81 行, `#### 场景 1 运行前置` 第 222 行, `### 场景 4: Description 触发准确率优化` 第 263 行 (尚无 4a / 4b), 「边界与留痕」第 480–481 行。
17. `git diff --stat 0c41e53..e822829`: 14 个文件 (proposal、RESULT、`run_arms_v5.sh`、v5 目录 5 个文件、六份 R3 审计报告); `git log 0c41e53..HEAD -- CLAUDE.md aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 为空; standards 中 SOT 最后一次改动为 `b98cf73`。
18. `forgejo GET /repos/10CG/Aria/issues/211`: open, 创建于 2026-09-09, 评论 1 条 (comment 23915)。
19. `ab-suite/version.yaml` 为 `1.5.0`, `ab-suite/trigger/` 不存在; `claude --version` 为 2.1.269。
20. R3 报告文件时间: 各席 12:26–12:53, 聚合 12:57, 文件名时间 12:07:10。
