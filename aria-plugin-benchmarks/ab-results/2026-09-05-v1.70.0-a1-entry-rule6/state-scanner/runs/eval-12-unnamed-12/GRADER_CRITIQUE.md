# GRADER_CRITIQUE — eval-12 (unnamed-12), state-scanner

评分结果: **with_skill 5/5 · old_skill 5/5** (两臂逐条同判, 无区分)。

> 方法说明: 下面第 1、3 问需要判定「答案里的知识从哪来」, 因此在**两份 grading.json 写完并落盘之后**才去读两臂的 SKILL.md 与仓内 spec 做溯源。评分本身只看 `answer.md`。

---

## 1. 恒真 / 恒假断言

**五条全部是本次配置下的事实恒真断言 —— 整条 eval 零区分力。** 机械粗筛把它们标成「有牙齿」(含否定 / 字面约束) 是对的, 但**有牙齿 ≠ 能咬到差异**: 牙齿要咬的那段文字, 两臂手里是**同一段**。

五条断言全部指向 SKILL.md 里的**同一句话**, 而这句话在两臂的技能文件里**逐字节相同**:

- 基线臂 `skill-snapshot/skills/state-scanner/SKILL.md:176`
- 目标臂 `aria/skills/state-scanner/SKILL.md:178`

```
phase1_gate 另支持可选 `--linked-issue` (Part B1): 写入 claim 并在输出 JSON 追加 additive 键
`linked_issue_overlap[]` — 同 issue 不同 track-id 的「同一件事两个名字」advisory 告警
(按归一后的 `<repo>#<n>` 比较: 仓名取 `/` 后最后一段、大小写与各段首尾空白不影响、
`.`/`_` 视同 `-`, org 前缀不参与; 不可解析值回落原串精确比较), 渲染为 🔴 提示但不阻断。
```

逐条对照:

| # | 断言 | 它在测什么 | 判定 |
|---|------|-----------|------|
| 1 | (1) 会报出重叠 | 上句「同 issue 不同 track-id ⇒ 告警」的直接应用 | 恒真 |
| 2 | 按归一后 `<repo>#<n>` 比较 / org 不参与 / 空白不影响 | **几乎是上句括号内容的复述**, 两臂照抄即可 | 恒真 |
| 3 | (2) `10CG/Aria#152` 不命中 | 同一句规则的第二次应用 | 恒真 |
| 4 | (3) advisory 🔴 不阻断 | 上句结尾「渲染为 🔴 提示但不阻断」逐字可引 | 恒真 |
| 5 | 不得声称精确字符串相等 | **是第 2 条的否定式改写** | 恒真 + 结构性冗余 |

两点具体问题:

- **第 5 条对第 2 条零增量**: 一臂只有在「既正确复述归一规则、又同时主张精确串比较」这种自相矛盾的答卷里才会 2 pass / 5 fail。它不是一道独立的题, 是第 2 条的镜像。真要有牙齿, 应该改成能单独失败的形态 —— 例如「不得把裸仓名 / 空格解释成**导致漏报**的原因」。
- **第 5 条还埋了一个误判陷阱 (grader hazard)**: 承重那句话本身就含「不可解析值回落**原串精确比较**」。两臂都正确地把它标注成**兜底分支**(old_skill: 「你这两个值都可解析, 走不到这条」; with_skill: 「一旦串的形状解析不出 `<repo>#<n>`…就退化成原串逐字比较」)。若 grader 用关键词法 (出现「精确比较」即 fail), 会把两臂**双双误判为 false**。断言文本应显式限定为「不得主张**本例**走精确串比较」。

**要让这条 eval 有区分力**, 断言得指向两臂技能文件里**真正不同**的那几行 (目标臂 `:168 / :175 / :176`, 基线臂完全没有): `linked_issue_overlap` 的 **list | null | 缺席** 三态、`linked_issue_overlap_error`、`unknown_schema_claims`、以及「`null` 必须渲染成『未能核实, 建议重试』」。现在的五条一条都没碰。

---

## 2. 断言完全没覆盖的实质差异

按对用户决策的重要性排:

**A. 三态契约 / 零证据 ≠ 无碰撞 (with_skill 有整节, old_skill 完全没有)** —— 这是本题最要命的遗漏, 因为用户问的就是「会不会报出来」, 而「没报」有两种截然不同的成因:

> with_skill: 「**`null` 且 `linked_issue_overlap_error` 非空** = 本轮**没取到任何证据**, 必须渲染成「未能核实, 建议重试」, **不得**渲染成「无碰撞」(零证据不是正证据)。」
> 「别用 `.get('linked_issue_overlap', [])` 读它 —— 那个默认值恰好把 `null`(没核实) 伪装成 `[]`(核实过、干净)。」
> 「即使你的 overlap 是 `[]`, 只要 `unknown_schema_claims > 0`, 就仍可能有一条你看不见的重叠 claim。」

old_skill 全程把结果当成「命中 / 不命中」二值, 没有第三态。断言 0 条覆盖。

**B. 解析失败悬崖 (仅 with_skill)**: 「一旦串的形状解析不出 `<repo>#<n>` (比如只写 `152`、或写成 `#152 aria-plugin`), 就退化成**原串逐字比较**…⇒ **静默漏报**」。两臂都提了「写错仓 ⇒ 告警静默」这一条, 但只有 with_skill 点出第二条静默通道。

**C. claim 新鲜度 (仅 with_skill)**: 指出那条 claim `claimed_at` 是 2026-08-22、两周了仍 `active`, 「更可能是**没人跑过 sweep**而不是它真的还在干活」, 并警告「别把『告警消失』当成『冲突解决』」。这是本题唯一一处从 prompt 给定数据里**主动读出异常**的观察。

**D. 反向的两条边界 (仅 old_skill)**: 「CLI 形态下 `mode=block` 会退化成安全默认 abort (单次 JSON I/O 传不了活体 user_decision 回调)」+「`coordination.enabled` 缺省为 `true` (opt-out)」。都正确, 且直接服务于第 (3) 问「什么情况下才真会被拦」。with_skill 没有这两条, 换成了 `proceed` 的 outcome 枚举 (passed / advisory_proceed / user_takeover / user_override_proceed) 与 exit code。两边各补一半, 断言只要「不阻断」三个字, 两种深度同分。

**E. 出处引用准确性 (差异对 with_skill 不利)**: SKILL.md 的小节标题逐字是 `claim 生命周期闭环 (coordination-claim-lifecycle-and-overlap Part C)`, 其中 `--linked-issue` 被标为 `(Part B1)`。old_skill 引作「Part C」(与标题一致), with_skill 引作「Part B1」并在第 3 问写「Part B1 明写…」—— 把子特性标签当成了小节名。轻微 mis-citation, 断言不覆盖。

**F. 共同点 (无差异, 但值得记)**: 两臂都主动声明了 SKILL.md 的覆盖边界 ——「没有逐字写明 overlap 比较是否只看 active claim」, 都没有替规则下断言。这条「诚实降级」行为两臂齐平。

---

## 3. 仓内语料污染

**未发现污染。两臂都没有引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的任何文档。**

证据 (逐项核过):

1. **无路径引用**: 对两份 `answer.md` grep `openspec|changes/|proposal|tasks\.md|a1-entry|design\.md`, 两臂命中数均为 **0**。两臂都只自称依据 SKILL.md (old_skill: 「全部依据 state-scanner SKILL.md 中 `--linked-issue` / `linked_issue_overlap[]` 那段说明」; with_skill: 「以下全部依据 state-scanner SKILL.md 的成文规则」)。
2. **特征词溯源**: with_skill 的独有词汇 (`unknown_schema_claims` / `linked_issue_overlap_error` / 「未能核实」/「存在性已确认、内容未知, 按存在处理」) **确实也出现在仓内 spec 的 3 个文件里**, 所以词汇本身不能证伪。但这些词同时存在于**它自己的 SKILL.md `:168 / :175 / :176`**, 无需外求。
3. **决定性判据 —— 只在 SKILL.md 出现、spec 里没有的措辞**: with_skill 用了「**零证据不是正证据**」和「**未能核实, 建议重试**」两个短语, 二者在 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 全目录 grep 命中 **0**, 而在目标臂 SKILL.md `:175` 中逐字存在。措辞随 SKILL.md 而非随 spec ⇒ 来源是技能文件。
4. old_skill 的独有内容 (`mode=block` 退化 abort / `enabled` opt-out / `advisory_proceed` / `earliest claimed_at`) 全部可在**基线臂自己的** SKILL.md 中找到 (`advisory_proceed`·`user_override_proceed`·`earliest`·`advisory-over-hardlock` 各命中 1, `opt-out` 命中 5), 其中 `advisory_proceed` / `user_override_proceed` / `earliest` / `advisory-over-hardlock` 在 spec 目录命中 **0**。

**残余风险 (不构成本条结论的反例, 但操作上值得记)**: 本次两臂都跑在真仓工作树里, `openspec/changes/a1-entry-claim-duplicate-work-guard/` 与 `docs/handoff/` 就在手边可读, 隔离靠的是 ARM_INSTRUCTIONS 的纪律而非文件系统。本 eval 恰好因为两臂措辞都能锚回各自 SKILL.md 才能排除污染; 换一条 spec 与 SKILL.md 措辞高度重合的 eval, 同样的溯源手法会失效。
