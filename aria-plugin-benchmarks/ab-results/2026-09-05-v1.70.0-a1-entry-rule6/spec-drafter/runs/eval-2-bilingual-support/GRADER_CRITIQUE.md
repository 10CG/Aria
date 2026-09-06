# GRADER_CRITIQUE — eval-2-bilingual-support

判定结果: **两臂 5/5 全过, 本 eval 区分力 = 0**。

- with_skill: 5/5
- old_skill: 5/5

---

## 1. 恒真 / 恒假断言点名

**断言 1「Should correctly parse mixed Chinese/English input」= 近似恒真。**
输入的两段是同一句话的中英对照, 任何能读中文的模型都会把它读成一条需求。两臂都在**第一行**就自发声明了这件事, 措辞几乎同形:

- with_skill: 「输入里的英文段和中文段是**同一条需求的翻译对**(不是两条需求), 所以只起草一份 Spec」
- old_skill: 「`Add a dark mode feature / 添加深色模式功能` 是**同一个需求的中英两种表述**, 不是两件事, 所以只起一份 Spec」

它没有可构造的失败态 (要失败得起草两份 Spec 或漏掉一种语言), 因此对技能版本差异不敏感。

**断言 3「Should preserve the feature intent from both language inputs」= 被断言 1 蕴含, 独立信息量约等于零。**
两段输入是互译, 「保留两侧意图」与「识别出它们是同一条」是同一件事的两种说法。除非某臂把 dark mode 写成了别的功能, 否则断言 1 过则 3 必过。本轮两臂皆如此。判据「它怎么会红?」答不出来。

**断言 2「Should generate proposal content in English as requested」= 弱区分。**
prompt 里「请生成英文 proposal」是明写指令, 两臂产物全篇英文, 无一处 CJK 混入正文。它只在模型忽略显式指令时才红, 属于基础指令跟随, 不测技能面。

**断言 4 / 5 (Linked Issue 行 + `none` 哨兵) = 本 eval 唯一有失败态的两条, 但两臂输出逐字节相同:**

```
> **Linked Issue**: `none`
```

(`cat -A` 核过, 两臂 proposal.md 第 6 行完全一致, 无尾随空格。)

**并且这两条大概率测的不是技能增量, 而是仓内语料可得性。** `none` 哨兵与「不留空/不删行/`N/A` 不接受」这套规则**成文在共享 SOT 模板里**, 两臂都能读到:

`standards/openspec/templates/proposal-minimal.md:55-58`

```
**Linked Issue header line (required for Level 2 / Level 3)**:
- Value is an inline code span of the form `<org>/<repo>#<n>` (e.g. `10CG/Aria#174`); several issues go in the same code span separated by `, `
- No related issue (verified): write exactly `none` — do not leave the value empty and do not delete the line (an empty value is indistinguishable from "forgot to fill it in"). `N/A` / `TBD` / `-` are **not** accepted sentinels
```

两臂的说明文字都能追溯到这段: old_skill 写「我暂填哨兵 `none` (Level 2 头部必填, 不能留空也不能删行)」, with_skill 写「`N/A` / `TBD` / `-` 不是哨兵, 会被机械 check 判不合规」—— 措辞与模板同源。这正是 `ab-baseline-leaks-via-repo-corpus` 描述的通道: 基线臂从仓内 SOT 学到目标行为, 断言因此对**技能文件**的增删失明。结论只能写成「落地前 (语料未含此规则时) 是否可区分未证; ship 态下这两条对本 eval 无边际区分力」。

**恒假断言: 无。** 五条都有臂通过, 不存在无法满足的项。

---

## 2. 断言没覆盖的重要差异

断言集完全没碰两臂**最大**的三处分歧:

**【1】A.1 认领 (claim / REQUIRE) 前置块 —— 只有 with_skill 有, old_skill 完全没有。**
with_skill 用了约三分之一篇幅做认领, 且把实参解析到可粘贴执行:

```
--raw-track-id "dark-mode-023236f2"
```

并逐项交代取值依据 (「uuid 段取 `~/.aria/container-id` 的 **`uuid` 字段** `023236f2`, 不取 `label`」)、`--linked-issue` 的两阶段取法、以及省略参数的后果读法 (「输出里 `linked_issue_overlap` **键缺席** ⇒ 措辞是「**本轮未检测**」, 不是「无碰撞」。零证据不是正证据」)。old_skill 从头到尾无一字提认领 / phase1_gate / track-id。
这是两臂之间可证伪、可复现、方向明确的**唯一实质差异**, 而断言集对它零覆盖 —— 本 eval 因此测不出技能变更的目标行为。

**【2】未执行副作用命令的上报方式。**
with_skill 显式写: 「⚠️ **本轮我没有执行这条命令**: 当前 AB 评测臂被显式禁止产生写入/推送副作用 ... 这是**执行条件不具备的上报, 不是规则豁免**」。这正是 `session-level-precondition` / `no-self-exempt-gates` 要求的形状 (不自我豁免、不静默跳过、把阻塞写清楚)。断言无一条测它。

**【3】仓内接地 (grounding) vs 通用文案 —— 两臂的 proposal 内容其实指向两个不同的世界。**
- with_skill 去读了真实文件, 并发现与字面需求相反的事实: 「它现在就是深色的」, 引用 `aria/skills/aria-dashboard/templates/dashboard.html:12` `--bg-primary: #0f1117;`。我实测该行属实 (`:root` 在 11 行, `--bg-primary: #0f1117;` 在 12 行, `--bg-secondary` 13, `--bg-card` 14), 引用未捏造。交付面全部落在真实路径上, 并把 scope 不确定性写进 proposal 的 `## Open Questions` 而不是只留在对话里。
- old_skill 未做任何仓内检测, 产出的是通用移动/桌面 App 文案: 「The product currently ships a light theme only」「Settings screen entry with a three-option theme selector」「深色模式要同时落到 mobile + web 两端并共用 `shared/` 的设计 token」。本仓不存在 settings screen, 也不存在 mobile 端; 且「currently ships a light theme only」与仓内实际 (dashboard 已是深色) **事实相反**。

断言集里没有任何一条能奖励接地或惩罚事实错误。这是本 eval 最大的覆盖缺口: 一份事实错误的 proposal 和一份实测接地的 proposal 拿同样的 5/5。

**【4】次要但可记的两点:**
- 两臂都正确援引不可协商规则 #5 (变更放本项目 `openspec/changes/`, 不放 `standards/openspec/changes/`), 无差异。
- with_skill 声称对草稿实跑过 `linked_issue_field_probe.py` 并贴出 「(空输出, exit 0)」。该脚本确实存在 (`aria/skills/state-scanner/scripts/linked_issue_field_probe.py`), 但**本 eval 无 transcript**, 「真跑过」不可核验 —— 按 `pasted-evidence-is-derived` 只能记作「合理但未证」, 我未据此加分或扣分。

---

## 3. 污染判定: 两臂均**未**污染

**结论: 无任何一臂引用仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的文档。**

机械核验 (在 run 目录下 grep 全部 outputs):

```
grep -nE "a1-entry|duplicate-work|TASK-[0-9]|detailed-tasks|openspec/changes/[a-z]" */outputs/*.md
```

命中 5 行, 全部是各臂自己起草的 `openspec/changes/dark-mode/` 落点, 与在制 Spec 无关:

- `old_skill/outputs/answer.md:32` — `Location: openspec/changes/dark-mode/proposal.md`
- `old_skill/outputs/answer.md:93` — 「**落点路径**: `openspec/changes/dark-mode/proposal.md`」
- `with_skill/outputs/answer.md:9` — 「slug 逐字取 `openspec/changes/dark-mode/`」
- `with_skill/outputs/answer.md:83` — `Location: openspec/changes/dark-mode/proposal.md`
- `with_skill/outputs/answer.md:170` — 「Create this file at `openspec/changes/dark-mode/proposal.md`?」

对 `a1-entry` / `duplicate-work` / `TASK-<n>` / `detailed-tasks` 四个模式的命中数为 **0**。

**with_skill 的认领知识来源已定位, 是被测技能文件本身, 不是在制 Spec 文档:**

`aria/skills/spec-drafter/SKILL.md`
- `:84` — `--raw-track-id "<spec-slug>-<container_uuid>" \`
- `:97` — 「`--raw-track-id`: 逐字拼 `<spec-slug>-<container_uuid>` —— slug = 本 Spec 目录名」
- `:99` — 「`~/.aria/container-id` 的 **`uuid` 字段**, **不是 `label`**」
- `:101` — 「`${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/linked_issue_field_probe.py` 存在,」

「该机器 label 必须留空」这句另有独立来源: `~/.aria/container-id` 文件自身的注释写着「label MUST stay empty on this machine」。两处都属于运行环境 / 被测技能面, 不构成对在制 Spec 文档的偷看。

**但仍需记一条 baseline-leak 提示 (不是本 eval 的污染, 是套件级风险):** 断言 4/5 的目标行为已成文在 `standards/openspec/templates/proposal-minimal.md` (提交 `91096f4` / `ffed204`), 该模板对两臂同等可见。凡是把「已 ship 到共享 SOT 的规则」写成断言的 eval, 都会像本轮一样双臂满分。要恢复区分力, 断言应改为点名**只存在于新版 SKILL.md 的行为** (例如: 是否输出认领命令 / 是否在缺 `linked_issue_overlap` 键时写「本轮未检测」而非「无碰撞」 / 是否在无 issue 时**省略** `--linked-issue` 参数而不是把 `none` 当值传)。
