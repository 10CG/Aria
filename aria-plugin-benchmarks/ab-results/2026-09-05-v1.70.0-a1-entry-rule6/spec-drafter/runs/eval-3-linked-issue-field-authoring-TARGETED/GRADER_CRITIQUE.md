# Grader Critique — eval-3 `linked-issue-field-authoring-TARGETED` (spec-drafter)

评分结果: `with_skill` 5/5 · `old_skill` 5/5。

以下是对**评测本身**的批判, 不是对两臂的复述。所有引证均为本次独立实读 (答案文件 + `aria` 仓 `7dd0135` / `ab3dbd0` 两版 SKILL.md), 未沿用 PREDICTION.md 的说法。

---

## 1. 恒真 / 恒假断言

### 1.1 全部 5 条对本 cycle 的 delta 恒真 —— 结构性的, 不是运气

两臂承载本 eval 的指令面**逐字节相同**。实测:

```
$ git diff --stat 7dd0135 ab3dbd0 -- skills/spec-drafter/SKILL.md
 1 file changed, 59 insertions(+), 1 deletion(-)
$ git diff 7dd0135 ab3dbd0 -- skills/spec-drafter/SKILL.md | grep -E '^[+-]' | grep -i 'linked issue'
(无输出)
```

baseline `7dd0135` 的 SKILL.md:344-354 已经逐字含「字段顺序建议 `Level` → `Status` → `Created` → `Linked Issue`」「无关联 (已核实) 时逐字写 `` `none` ``」「`N/A` / `TBD` / `-` **不是**哨兵」「**不写** markdown 链接形」——即断言 1-5 想测的**每一条**。所以 5/5 vs 5/5 是**构造上注定**的, 与两臂的能力差无关。

这不是缺陷 (它作为回归夹具是称职的: 若任一臂掉分, 说明新增的 59 行 claim 块挤占了起草注意力), 但**它的 5 条不能进 delta 分母当信号**。本 skill 套件 30 条断言里, 这 5 条 + eval 1/4 的 6 条共 11 条是零区分度的回归位; 把它们计入总分会把真实 delta 稀释近四成。RESULT 记账时应把「回归位 pass/fail」与「区分位 delta」分开报。

### 1.2 断言 3 是断言 2 的推论 —— 零增量信息

断言 3 要求「行内无 `](http`, 且不留空」。任何满足断言 2 (值逐字为 inline code `` `none` ``) 的行, **自动**满足断言 3: `` `none` `` 既非空也不含 `](http`。断言 3 只能在断言 2 已经 fail 的世界里独立 fail。它不是恒真, 但**条件恒真**, 给两臂各送一分。若要保留它的独立价值, 应把它改成对 issue **存在**分支的负控 (「有关联 issue 时也不得写成 `[repo#n](url)`") —— 那才是 SKILL.md:354 真正点名、且 `NO_TOKEN` 判定真会触发的坏形态; 现在这个 `none` 分支上它无事可做。

### 1.3 断言 5 的 grep 面比它点名的缺陷宽 —— 潜在假阴性陷阱

断言 5 的括号限定是「**作为头部字段名**」, 但字面判据是「全文无 `Related Issue` / `Issue Link` / `关联 Issue`」。两者不等价, 而且差的那块**恰好是技能明文允许的**:

> SKILL.md:354 (两臂皆有): 「读取侧另认中文 alias `关联 Issue` / `无`, 但**新写一律用英文 canonical**。」

也就是说, 一个臂在正文里解释「读取侧还认 `关联 Issue` 这个 alias, 但我新写用英文」——这是**对规则理解更深**的表现——按字面 grep 会被判 fail。本轮两臂都没写这句, 所以陷阱没被触发 (with_skill 全文 `Linked Issue` 三处均英文 canonical; old_skill 两处同); 但这是靠运气不是靠设计。**建议把判据限定到头部 blockquote 那一行**, 或显式写明「正文提及 alias 不算违规」。

### 1.4 唯一有真牙齿的是断言 2

值得点出: 两版 SKILL.md 的 Level 2 预览骨架里**都逐字印着占位串** ——

```
7dd0135:146:> **Linked Issue**: `{<org>/<repo>#<n>}`
ab3dbd0:204:> **Linked Issue**: `{<org>/<repo>#<n>}`
```

—— 一个照抄骨架的臂会原样带出 `{<org>/<repo>#<n>}` 而 fail 断言 2。这条断言测的是「知道要按分支替换哨兵」而非「知道字段叫什么」, 是本 eval 里唯一可能真的红的一条。两臂都替换正确。

### 1.5 无恒假断言

5 条全部可满足且被满足, 不存在「谁都做不到」的项。

---

## 2. 断言没覆盖的重要差异

这一节比第 1 节重要: 两份答案的**实质差距很大**, 而 5/5 vs 5/5 会让只读分数的人得出「无差别」的相反结论。

### 2.1 A.1 认领前置: 一臂全程讨论, 一臂零次提及 (本 cycle 的真 delta)

`with_skill` 用整个「前置 1」段处理 REQUIRE claim, 且踩中三个非平凡点:

> 「这是**执行条件不具备**, 不是我判断「这次不值得跑」而豁免掉 —— 闸门本身仍然成立。」
> 「按四态读法, 这轮的正确措辞是「本轮未检测」, **不能**写成「无碰撞」—— 零证据不是正证据。」
> 「注意这条命令里**故意没有** `--linked-issue`: ... 哨兵 (含 `BAD_TOKEN` / `NO_TOKEN` / `NO_FIELD`) 一律**省略整个参数**」

`old_skill` 全文对 claim / `phase1_gate` / 碰撞检测**零提及**, 直接从 A.1.0 头脑风暴跳到 Level 判定。

本 eval 的 5 条断言对此**一条也没测**。这块由 eval 5/6 承担是合理分工, 但 eval 3 的结果行必须带注脚, 否则它会被当成「新版无改善」的证据。

### 2.2 引用质量: 6 处 file:line vs 0 处 —— 且我逐条复核了

`with_skill` 的 Why/What 挂在 6 个可验引用上。我独立实读全部命中:

| 答案里的引用 | 实读结果 |
|---|---|
| `.aria/config.template.json:51` 默认 `[]` | 该行逐字 `"label_filter": []` ✅ |
| `issue_scan.py:536-538` `wanted.intersection(...)` | 536-538 = `if label_filter:` / `wanted = set(...)` / 列表推导 ✅ |
| `:817` `_write_cache_atomic` | 817 行即 `_write_cache_atomic(...)` 调用 ✅ |
| `scan.py:435-462` CLI 三参数 | 435 = `def _parse_args(...)` ✅ |
| `scan.py:288` `build_snapshot(project_root)` | 逐字命中 ✅ |
| `issue_scan.py:589` `collect_issue_scan(project_root)` | 逐字命中 ✅ |

`old_skill` 对同一机制的描述在**语义上也对**(「`_fetch_repo` 在 normalize 之后、写缓存之前过滤」), 但无行号、无可核对锚点。断言集对「引用是否可核验」零覆盖。

### 2.3 一处 baseline 臂反而更强的设计, 也没被测到

`old_skill` 的 SC-4 自带负控执行要求:

> 「该断言在「把过滤误放进 `_fetch_repo`」的坏实现下必须转红 —— 实施时先构造该坏实现跑一次确认它会红, 再删掉」

`with_skill` 的 SC-3 只写了红条件 (「过滤集被持久化」), 没有要求跑坏实现验证。这正是 `check-runs-at-baseline-first` 那条方法论的核心, **baseline 臂在此项上更好**。任何只看 5/5 vs 5/5 的记账都会漏掉这个反向信号 —— 它值得进 RESULT, 因为它说明新版的注意力被 claim 块拉走后, 验收设计一侧有轻微退化的可能 (n=1, 不可外推, 但要记)。

### 2.4 其他无断言覆盖的分歧 (仅记录, 不评优劣)

- **slug 不同**: `state-scanner-issue-label-filter` vs `state-scanner-issue-label-runtime-filter`。
- **零命中呈现相反**: `with_skill` SC-4 只钉 `label_filter` 子对象形状, 未表态区块是否仍渲染; `old_skill` SC-3 明确要求区块仍出现且计数含 `0 / 5`。两种产品行为不同, 无断言仲裁。
- **新字段位置不同**: `with_skill` 新增 `issue_status.label_filter` 子对象 (原 `items`/`open_count` 不动); `old_skill` 直接改渲染视图不加子对象。
- **`--issue-label` 语法不同**: `old_skill` 额外支持逗号分隔, `with_skill` 只支持可重复传。
- 两臂都正确遵守 Rule #5 落点 (`openspec/changes/` 本项目仓) 并都判 Level 2、都未生成 tasks.md、都写了 Rule #6 AB 任务项 —— 这三项一致, 也都无断言。

---

## 3. 污染判定: 两臂均**未**引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/`

**结论: 无污染。** 逐项引证如下。

### 3.1 直接引用: 零

两份 answer.md 全文 grep `a1-entry` / `claim-duplicate-work-guard` **零命中**。两臂都没有引用、转述或点名母 Spec 的 `proposal.md` (175KB) / `tasks.md` / `detailed-tasks.yaml`。

### 3.2 看起来像污染的那批术语, 溯源到 A 臂技能文件本身

`with_skill` 大量使用 `phase1_gate.py` / `--raw-track-id` / 四态读法 / `BAD_TOKEN`·`NO_TOKEN`·`NO_FIELD` / `release_gate.py --status abandoned`, 甚至一句极具体的:

> answer.md:165 「check 按 E0 取**文档序第一条** depth-1 命中, 不限行号」

这句几乎逐字来自 A 臂 SKILL.md, 不是来自仓内 Spec:

> `ab3dbd0:skills/spec-drafter/SKILL.md:426`: 「check 按 E0 取**文档序第一条** depth-1 命中, 不限行号 —— 既有 proposal 把字段写在超长头部 blockquote 的第 45 / 61 行仍判合规。」

反证: `depth-1` 在 `openspec/changes/a1-entry-claim-duplicate-work-guard/*.md` 里 **零命中**。同理 `--raw-track-id` (SKILL.md:84,97) / 哨兵三token (SKILL.md:104) / 四态 (SKILL.md:115-125) / `release_gate.py --status abandoned` (SKILL.md:129) 全部有技能内出处。⇒ 这是**技能生效**, 不是污染。

### 3.3 一处必须记录的边缘事实: A 臂确实枚举了包含母 Spec 的目录

`with_skill` answer.md 写:

> 「落点 `openspec/changes/state-scanner-issue-label-filter/proposal.md` (**Aria 主仓内**) ... slug 与现有 **7 个** change 目录无碰撞。」

仓内 `openspec/changes/` 实测恰为 7 个目录, 其一即 `a1-entry-claim-duplicate-work-guard`。⇒ 该臂**列了**含母 Spec 的目录 (目录名可见), 但**没有读其内容**, 也没有从中取用任何东西。

对本 eval 的判定影响: **无**。断言 1-5 的目标 (字段名 / `none` 哨兵 / 非链接形 / 四行顺序 / 不译名) 在两臂 SKILL.md 里逐字都有, 母 Spec 提供不了任何增量优势 —— 即使全文读了也无从加分。

### 3.4 old_skill 侧

`old_skill` 的仓内引用只有 `docs/decisions/` (扫描无本主题决策, 属实: 20 份 DEC-* 均为其他主题)、`issue_scan.py:_fetch_repo`、`.aria/config.json`。其 Linked Issue 规则表述 (「`N/A` / `TBD` / `-` 都会被机械 check 判不合规」) 逐字对应 `7dd0135:SKILL.md:353`, 出处在自己臂内。⇒ 无污染。

### 3.5 残余风险 (对本 eval 不成立, 对 eval 5/6 成立)

AB harness 跑在**真仓**里 (无沙箱), 母 Spec 的 175KB `proposal.md` 对两臂都是可 grep 的。本 eval 因 3.3 的理由免疫; 但 eval 5/6 的目标行为恰好写在母 Spec 里, 那里的 baseline 臂**存在**通过 grep 在制文档习得目标行为的通道 (PREDICTION 已预留污染上界)。评那两个 eval 时须逐条查 baseline 臂有无仓内文档引用痕迹, 不能沿用本文的「无污染」结论。
