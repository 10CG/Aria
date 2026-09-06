# GRADER_CRITIQUE — eval-4 level2-proposal-location-rule5-TARGETED

评分结果: **with_skill 4/4, old_skill 4/4** (逐条证据见各臂 `grading.json`)。
本文件为 grader 对**断言集本身**与**臂间未被断言覆盖的差异**的批注, 不改变上面的评分。

---

## 1. 恒真 / 恒假断言点名

### 断言 2 —— 对本题近似恒真, 零区分力

> 「全文任何位置都没有把 `standards/openspec/changes/` 当作本次 proposal 的落点推荐 (作为反例点名说明「不该写那里」不算违反)」

题干第 (2) 问**强制**回答者写出「为什么是那个路径而不是另一个候选」, 因此两臂**必然**要点名
`standards/openspec/changes/`; 而括号里的豁免恰好把这唯一的出现形态排除在违反之外。
于是: 凡断言 1 通过的臂, 断言 2 自动通过 —— 它没有独立的失败通道, 是断言 1 的同义重述。
实测两臂 `standards/openspec` 出现处 (with_skill: 3 处; old_skill: 2 处) 全部落在反例/规则引用/边界说明,
无一处需要裁量。**建议**: 若要保留这条, 应改成可独立失败的形式 (例: 「§3 proposal 全文正文内不得出现
`standards/` 路径」, 或「不得建议在 standards 子模块内新增/提交任何文件」)。

### 断言 1、3、4 —— 非逻辑恒真, 但对**本次被测变更**恒真 (setup 层面的零区分力)

这三条测的都是 baseline 技能文件**已经**规定的行为, 不是本 change 新增的行为。实测 (aria 子模块):

- `git show master:skills/spec-drafter/SKILL.md` **:113** 已有 —— 「把项目变更写进 `standards/openspec/changes/`
  会让该变更对所有采用方可见且无人拥有」(覆盖断言 1/2/3);
- 同文件 **:116 / :146 / :344** 已有 —— 「头部 Linked Issue 字段 (必填)」+ 逐字样例
  `> **Linked Issue**: `<org>/<repo>#<n>`` (覆盖断言 4);
- `git diff --stat master..HEAD -- skills/spec-drafter/SKILL.md` = **59 插入 1 删除**, 增量**全部**是
  「前置: REQUIRE claim (A.1, MUST)」块 (phase1_gate/`--raw-track-id`/`--linked-issue` 哨兵/四态表/release_gate)。

⇒ 四条断言**没有一条**触及本 change 的增量行为。本 eval 名为 `-TARGETED`, 但它 target 的是 Rule #5 落点
(旧行为), 不是 a1-entry 入口认领 (新行为)。两臂 4/4 平局是这个设计的必然结果, **不能**读作「新技能无回归」
之外的任何结论 —— 尤其不能读作「新技能无增益」, 因为增益面根本没被测。

---

## 2. 断言没覆盖的重要差异 (逐条给出处)

**(a) 最大差异: A.1 REQUIRE claim 前置 —— with_skill 有, old_skill 完全没有。**
with_skill §0「先交代两个被跳过的 A.1 前置 (descriptive 模式声明)」整块 (answer.md:5-26) 给出
`phase1_gate.py --raw-track-id "task-list-due-date-sort-<container_uuid>" --phase A.1 --mode advisory
--include-terminal`、uuid 段取 `~/.aria/container-id` 的 `uuid` 字段而非 `label`、
`--linked-issue` 整参省略而非传哨兵 (「任何非空字符串都 truthy」)、结果四态互不相同
(键缺席 / `[]` / `unknown_schema_claims > 0` / `overlap == null` 且 `overlap_error` 非空 = 「未能核实」)、
退出义务两条 (改名 ⇒ release 旧 + acquire 新; 放弃 ⇒ `release_gate.py --status abandoned`)。
old_skill 全文**零处**提及认领/claim/phase1_gate/release_gate (grep 命中 0)。
这正是本 change 的核心行为面, 却零断言覆盖 —— **这是本 eval 最该补的缺口**。

**(b) proposal 结构差异**: old_skill 的 proposal 全文含 `## Framework Constraints` 与 `## Open Questions`
两段 (answer.md:80-88, 118-122); with_skill 把 Framework Constraints 移出 proposal、降级为答复正文 §4 的
「需要你确认的地方」(answer.md:128), proposal 内**不含**该段, 也无 Open Questions。哪种更合规 (SOT 模板
是否要求 Framework Constraints 入正文) 断言未表态, 两种写法都能拿 4/4。

**(c) 误区排除广度**: old_skill 额外排除了 `docs/` 与 `.aria/` 两个落点 (answer.md:40);
with_skill 只处理 `standards/` 一个候选, 但多给了一条可迁移判据 —— 「问『这次变更交付完成后,
谁的行为改变了』」(answer.md:52)。断言 3 只要求「点到语义」, 对这类推广度差异不敏感。

**(d) 标题语言**: with_skill proposal 标题为英文 `# Task List Due Date Sort` (answer.md:71),
old_skill 为中文 `# 任务列表按截止日期排序` (answer.md:47)。命名/语言约定无断言。

**(e) 输出形态**: with_skill 在 proposal 全文前另加一个 `SPEC DRAFT PREVIEW (Level 2)` box
(answer.md:59-66, 含 `Location:` 行), old_skill 用目录树图示 (answer.md:20-26)。可机读性差异无断言。

**(f) 成本**: with_skill `total_tokens` 79921 / `duration_ms` 127522 / 5 tool_uses;
old_skill 81372 / 191464 / 7 tool_uses。(两个 `timing.json` 的 `total_duration_seconds` 字段值为空,
是坏 JSON —— `{"total_duration_seconds": ,` —— 顺带记一笔, 会让下游解析脚本崩。)

---

## 3. 污染判定 (是否有臂引用仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/`)

**结论: 两臂均未引用该目录下的文档 —— 未见污染证据; 但两臂各有不可见的 tool_uses, 只能就 answer.md 文本判定。**

- 逐字检索: 两臂 answer.md 对 `a1-entry` / `claim-duplicate` / `openspec/changes/a1` 的 grep 命中均为 **0**。
- 唯一需要辨别的是 with_skill §0 那批高度具体的认领细节。核对后判定为**技能文件来源 (预期处理效应)**,
  非仓内在制 proposal 语料:
  - with_skill:9 「十步循环那 10 轮闸门审的都是「这份产物做得对不对」, 没有一条问过「它该不该存在」」
    ↔ 工作树 `aria/skills/spec-drafter/SKILL.md:92`「它们审的都是**这份产物做得对不对**, 从不问**它该不该存在**」
    —— **逐字同构**;
  - 而仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:46` 的同义句措辞不同
    (「10 轮闸门的入口断言里**没有任何一条**问过「远端是否已出现同 issue 的竞品 Spec」。SCOPE_OK / anchor
    固化都在审**这份产物做得对不对**, 从不问**它该不该存在**。」) —— with_skill 的措辞更贴 SKILL.md 而非它;
  - `~/.aria/container-id` 的 `uuid` 字段而非 `label`、四态表、`release_gate.py --status abandoned`
    亦逐条对应 SKILL.md:97-129; `[repo#42](url) 会被判 NO_TOKEN` 对应 SKILL.md:424。
- **保留意见**: 本 eval 无 transcript, with_skill 5 次 / old_skill 7 次工具调用内容不可见, 且 AB harness 跑在真仓
  (memory `ab-harness-real-repo`), 因此只能说「答案文本中无仓内 spec 文档的引用或独有措辞」, 不能证明两臂
  未读过该目录。若要能证伪, 需保留 transcript 或在 harness 层隔离 `openspec/changes/`。
