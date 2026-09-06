# Grader 复评批注 — eval-4 `a1-overlap-ask-user-by-status-TARGETED` (仅 `with_skill` 臂重评)

> 评测对象: `with_skill/outputs/answer.md` (52 行)。未读 `with_skill_prefix/`, 未改动 `old_skill/`。
> 结果: 6/6 assertions `passed: true` (见 `with_skill/grading.json`)。
> 本文件回答三个批注问题, 不是对该臂的复述。

---

## 1. 有没有断言在这份回答上是恒真的?

有 **2 条低区分力**, 其中 1 条实质恒真。

**1. 「不把四条压成一句『有 4 条重叠』了事 —— 不同 status 的处置不同」= 实质恒真。**
prompt 末句逐字写着「**每一条分别怎么处理?**」。逐条展开是 prompt 的直接指令, 不是技能知识;
任何听懂题面的臂 (含无技能基线) 都会分四段答。该断言测的是「有没有读题」, 不是「有没有加载
A.1 认领规则」。真正有区分力的是**处置内容**是否按 status 分档 (done/abandoned 同档、unknown
视同 active), 而那三点已由第 3/4/5 条断言各自承载 —— 所以这条在断言集里既不独立也不排他。

**2. 「告警内容含五要素 + linked_issue 原串」= 高风险近恒真, 但本次判 pass 有实据。**
风险在于: 五要素的**全部字面值** (含 `10CG/Aria#174`、`2026-09-05T08:00:00Z`) 都印在 prompt 的
JSON 里。任何臂把输入表格照抄一遍就能满足「含」这个谓词, 而照抄不需要知道「原串不可缩写」这条规则。
断言的判据写成了**包含**, 但它想测的是**克制** (不缩成 `#174`、不截断成日期) —— 包含谓词对
「照抄」与「守规」不可分辨。

本次仍判 pass, 是因为该臂给了照抄给不出的证据: 它显式声明了规则本身 ——
「所以我不把它缩写成 `#174`, `claimed_at` 也保留完整时间戳不截断成日期」, 并给出了理由
「org 段本身不参与匹配, 逐字回显是判别误配的唯一手段」。即证据不止于「串在场」。

**建议 (给套件维护者, 非本次评分变更)**: 若要保住这条的区分力, 应把断言改成对**缩写行为**的负控
—— 例如「答案中不出现裸 `#174` 形态」+「`claimed_at` 不以 `2026-09-05` 形态单独出现」, 或把
prompt 里的 issue 串换成一个**答案必须自己保持完整**才谈得上区分的形态。当前形态在
「输入即答案」的 fixture 上天然弱。

其余 4 条 (A1 起草前 AskUserQuestion / A3 不释放对方 claim / A4 abandoned 同档 + GC 产物 /
A5 unknown 视同 active) **不恒真**: 四者都是 prompt 未提供、须从技能规则带入的处方性内容,
且都存在自然的反面答案 (渲染告警后继续起草 / 建议 sweep 掉僵尸 claim / 把终态当「无碰撞」放行 /
读不懂就跳过)。这 4 条是本 eval 的实际承重面。

---

## 2. 这份回答里有没有重要内容是断言完全没覆盖的?

有, 至少 5 项, 其中 2 项是**正确性相关**而非锦上添花:

**2.1 `unattended == true` 的配置分支 (正确性相关, 未覆盖)。**
答案第 3 节括号里写: 「若 `state_scanner.coordination.unattended == true`, 我就不发问, 改为写一条
「待复议」记录并置 `awaiting_owner` …… 这是配置事实, 不由我在运行期推断「现在能不能问」。」
这对应 SKILL.md 的 skip 第 3 条。断言集只有「必须经 AskUserQuestion 请裁」一句, **没有任何断言
覆盖这条例外**。风险是双向的: 一个只学到「必须问」的臂会在 unattended 场景下答错, 而断言集给它满分;
反过来, 一个正确加了该限定的臂也拿不到额外分。这是断言集对承重规则的**单侧覆盖**。

**2.2 退出义务两条 (未覆盖)。**
第 5 节: 「若裁「换方向」并改了 Spec 目录名: **release 旧 track-id + acquire 新 track-id**, 两步都要走,
只 acquire 会留下永不释放的僵尸 claim」/「用 `release_gate.py --raw-track-id <同一串> --status abandoned`
释放**我自己**这条」。这是 SKILL.md「退出义务 (两条, 缺一就留下永不释放的僵尸 claim)」的完整落地,
且它与 A3 (不释放**对方**的 claim) 构成一对易混淆的边界 —— 「能 release 谁」正是这题最容易答反的地方。
断言集完全没测。

**2.3 幂等 (未覆盖)。** 「不会重复 acquire —— 本 session 的 claim 已是 active, 幂等生效。」

**2.4 回显原串的**理由**(未覆盖)。** 断言只要求「含原串」, 不要求答出「org 段不参与匹配, 回显是判别
误配的唯一手段」。理由是把「含」从格式动作升格为可迁移规则的关键, 却不在评分面上。

**2.5 该臂自己新增的推理 (无处安放, 也无处证伪)。**
「三条的 slug 各不相同 (`oauth-login` / `social-login` / `oauth2-spike`), 但**名字不同不等于不是同一件事**」
以及「它的 slug 带 `spike` 字样, 看起来像探路, 若它留下过结论, 直接影响我该不该重走一遍」。
这两句**不在 SKILL.md 也不在仓内 Spec 文档中** (已 grep 确认), 是该臂自生的推理。它们方向正确
(碰撞判据是 issue 不是名字), 但断言集既不奖励也不检查。
另: 答案把第 4 条与 `unknown_schema_claims == 1` **绑定为同一条** (「它对应的就是 `unknown_schema_claims == 1`
这一条」) —— 这是合理推断但 prompt 未明示两者同一; 属未被任何断言检验的**推断性断言**。

---

## 3. 该臂是否引用了仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档?

**未发现引用。判定: 没有。**

核验方式与结果:

1. 对 `answer.md` grep `openspec` / `proposal.md` / `tasks.md` / `detailed-tasks` / `a1-entry-claim`
   —— **零命中** (exit 1)。答案通篇没有出现任何仓内路径、Spec 目录名、审计轮次、spike 编号、
   `FIX-nn` 编号、owner 裁定日期等 Spec 文档特征标记。
2. 逐条回溯答案中所有非 prompt 来源的技术内容, **全部落在 `aria/skills/phase-a-planner/SKILL.md`**:
   - 「已检测到 1 条无法解析的 claim: 存在性已确认、内容未知, 按存在处理」 → `SKILL.md:103` (措辞近逐字)
   - 「按 `active` 同档请裁 …… GC 产物 …… 不要提议去释放对方的 claim —— 那是对方的东西」 → `SKILL.md:123`
   - 「`unknown` …… 视同 `active` 处理(存在性已确认)」 → `SKILL.md:122` 档位表
   - 「合并方向 / 换方向 / 确认确实是两件事」三选一 → `SKILL.md:121` `active` 行
   - 「release 旧 + acquire 新」「`release_gate.py --raw-track-id <同一串> --status abandoned`」 → `SKILL.md:110-111`
   - 「`state_scanner.coordination.unattended == true` ⇒ 不发问 / `awaiting_owner` / 不做运行期推断」 → `SKILL.md:129-131`
   - 「不重复 acquire, 幂等」 → `SKILL.md:88-94` 幂等块
   - 「五要素 + 逐字回显原串, 不缩成 `#174`, `claimed_at` 不截断」 → `SKILL.md:114-116`
   - 「认领必须早于投入」 → `SKILL.md:73-76` 「为什么在这里」段 (`:75` 「认领必须**早于投入**」)
3. **唯一需要辨别的重叠点**: 「org 段不参与匹配, 回显原串是判别误配的唯一手段」这句同时出现在
   `SKILL.md:116` 和 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:277`。
   逐字比对后 **SKILL.md 是更近的来源**: SKILL.md 写「org 段不参与匹配, **回显原串是人工判别「误配」
   的唯一手段**; 缩写与截断正好把这个手段消掉」, 答案写「org 段本身不参与匹配, 逐字回显是判别误配的
   唯一手段」并紧接着点名「不缩写成 `#174` / 不截断成日期」—— 与 SKILL.md 同段同序; proposal.md:277
   那行是并列条目式表述且不含「缩写/截断」这一对处方。故**不构成仓内 Spec 文档泄漏的证据**。

补充 (与 `ab-baseline-leaks-via-repo-corpus` 相关): 本次核验只能证明 **`with_skill` 臂**的输出可由
SKILL.md 完全解释, 不能反过来证明基线臂没有从仓内 `proposal.md:277` 学到同一条 —— 该行确实在仓内,
且措辞与目标行为高度接近。若基线臂在「五要素/原串」上表现意外地好, 应优先怀疑这条通道, 而不是
判定技能无增量。此为对 eval-4 区分力结论的**已知污染面**, 建议在本轮 AB 汇总里显式记一笔。
