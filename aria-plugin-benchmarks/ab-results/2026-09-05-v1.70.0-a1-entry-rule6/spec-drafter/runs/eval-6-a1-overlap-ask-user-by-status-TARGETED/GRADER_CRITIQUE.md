# GRADER_CRITIQUE — eval 6 `a1-overlap-ask-user-by-status-TARGETED`

评分结果: A 臂 (`with_skill`) 6/6 · B 臂 (`old_skill`) 1/6 (仅非承重的第 6 条通过)。
本次只读了 `eval_metadata.json` / `prompt.txt` / `with_skill/outputs/answer.md` / `old_skill/outputs/answer.md`;
按指示**未读** `with_skill_prefix/`。所有 evidence 均已用 `substring in answer` 逐字校验通过。

## 1. 恒真 / 恒假断言点名

- **第 6 条「不把四条压成一句」= 本轮近乎恒真, 零区分力**。prompt 结尾直接写着「**每一条分别怎么处理?**」——
  格式已被提问钉死, 任何按条作答的回答都过。实测 A/B 双过。它测的是「听懂了问题」, 不是「装了 skill」。
  若要保留, 应改成能被违反的形式 (例如「四条的**处置动作**至少出现三种不同结论, 而非四条都指向同一动作」)。
- **无恒假断言**: A 臂 6/6 全过, 证明六条都在被测 skill 的能力范围内可满足。
- **第 2 条的判据不在断言文本里**。断言只写「含 … `linked_issue` 原串」, 未写「`claimed_at` 不得截断」。
  B 臂之所以判 false, 承重点其实是 grader prompt 外挂的那句「`claimed_at` 截断成日期也不算」。
  两个 grader 拿同一条断言会得到不同结论 —— 建议把「五要素逐字、`claimed_at` 不截断、`linked_issue` 不缩写」
  写进断言文本本体 (SOT 在 `aria/skills/spec-drafter/SKILL.md:133-135`)。
- **第 4 条措辞与它引用的 SOT 有语义错位**: 「`abandoned` … 注明该终态可能是 GC 产物**而非真的做完**」——
  「做完」是 `done` 的语义, `abandoned` 的对应说法应是「而非真的放弃」。A 臂写的正是
  「`abandoned` 也可能是 GC 产物而非真的主动放弃」(语义正确) —— 若某个 grader 逐字卡「做完」二字就会造成假阴。
  该断言宜改为「…可能是 GC 产物而非真终态」。(SKILL.md:141 把 done/abandoned 合并成一行, 断言直接继承了那行的措辞。)
- **第 3 条是否定式断言, 天然难取正证据**。「不建议去释放对方的 claim」在「压根没提释放」的回答上,
  无正证据也无反证据。我按承重规则 (必须能引到具体文字) 判 B false, 并在 evidence 里写明「没提议释放 ≠ 正证据」。
  建议改写成可正向取证的形式, 如「明确说明对方的 claim 只能由对方容器释放」。
  另: 该断言只挂在 `done` 那条, 而 SKILL.md:141 是 `done` / `abandoned` 同格 —— 断言比 SOT 窄。
- **本轮最接近的一次判定 = B 臂第 5 条**。B 写了「在核实之前视为「可能存在未知并发」, 不要因为字段是空的就当它不存在」,
  满足断言后半段「不因读不懂就忽略」; 但承重前半段「**视同 `active` 处理**」被 B 自己的
  「**它既不能被当成「第四个 overlap」**, 也不能被当成「无冲突」。它是不可判定的」直接否定,
  且它给的是「先核实 → 条件性升级」的第三条 lane (「确认是真 claim 的损坏副本 → 它升级成第二个需要协调的对象」),
  不是 active 同档。承重项要求逐字可引, 故判 false。这条断言若想避免争议, 应拆成两条 (「不忽略」/「入 active 档」)。

## 2. 断言没覆盖的重要差异 (AB 差值被低估的部分)

1. **退出义务完全没被测**。A 臂给了裁定回来后的动作: 「`release_gate.py --raw-track-id <与认领时逐字相同的那串>
   --status abandoned`。不释放 = 留下一条永不释放的僵尸 claim」, 以及「改名就是换了 track-id, 必须**两步走**:
   release 旧串 + acquire 新串, 不能只改目录」。B 臂零覆盖。这是 SKILL.md:127-129 的承重内容, 断言集漏测。
2. **B 臂给出了断言 3 想防的那类动作, 但落在断言覆盖范围外**: 对第 4 条它写「确认是空壳残留 → **清掉它**,
   并在 handoff 里记一笔」—— 提议处置别人写下的 claim 记录。断言只把这条禁令钉在 `done` 上, 所以这处没被扣分。
3. **两臂都识别出 prompt 的口误, 未被测**。用户说「四条都和我的 `linked_issue: 10CG/Aria#174` 同一个 issue」,
   实际第 4 条是 `null`。A: 「第 4 条的 `linked_issue` 是 `null`, **不是** `10CG/Aria#174`」;
   B: 「你不知道它挂的是不是 #174 (`linked_issue` 是 null …)」。双方都过, 但这项「不跟着用户口误走」的能力值得单列。
4. **B 臂有断言测不到的正向内容**: scope≠issue 的区分 (「同一个 issue 下的 claim 不等于同一份工作」)、
   把 `unknown_schema_claims` 的无人消费判为静默并主张开单、要求在 claim 记录里留处置留痕。
   这些是通用并发协调推理, 不来自 skill。只看断言分 (6/6 vs 1/6) 会低估 B 的绝对可用性 ——
   但断言测的是 skill 规定动作 (请裁 lane / 五要素 / GC 产物 / unknown 入 active 档), 该方向的分差是真实的。
5. **B 臂的元认知诚实未计分**: 「spec-drafter 目前没有关于 A.1 入口认领 / `linked_issue_overlap` /
   `unknown_schema_claims` 的成文判据 … 上面按 `status` 分档的处置是我从并发协调的一般原则推出来的, 不是引用规范」。
   基线臂没有伪造规范来源, 这是 baseline 行为的正确形态, 评分时既未加分也未扣分。

## 3. 污染判定 (是否引用了仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/`)

**结论: 两臂均未引用该 Spec 文档, 本轮未观察到 co-landing 文档污染。**

- 字符串核验: 两份 `answer.md` 里 `a1-entry-claim-duplicate-work-guard` 命中 0 次;
  `proposal.md` / `tasks.md` / `detailed-tasks.yaml` 三个文件名均未被指名引用。
- 仅有的 `openspec/changes/` 出现属通用起草落点, 非引用该 Spec:
  A 臂「我才进入 A.1 起草(`openspec/changes/<slug>/proposal.md`, 落在本项目仓内)」;
  B 臂「以及 `openspec/changes/` 下它是否已有落地的 proposal」。
- **A 臂的全部承重内容都能在被测 skill 内逐字定位**, 无需假设它读过仓内 Spec:
  `aria/skills/spec-drafter/SKILL.md:121`「存在性已确认、内容未知, **按存在处理**」·
  `:131`「**overlap 非空时按对方 claim 的 `status` 分档请裁**(经 `AskUserQuestion`, 不自行放行)」·
  `:133-135` 五要素 + 「org 段不参与匹配, **回显原串是人工判别「误配」的唯一手段**」·
  `:139`「读不懂其 schema, **视同 `active`** 处理(存在性已确认)」·
  `:141`「注明该终态也可能是 GC 产物而非真的做完。**不要提议去释放对方的 claim** —— 那是对方的东西」·
  `:84/:97/:127-129` `--raw-track-id` 与退出义务两条。A 臂答案是这几行的忠实展开。
- **语料重叠告警 (不改变本轮结论, 但影响后续可比性)**: 短语「早于投入」「存在性已确认」「GC 产物」「僵尸 claim」
  **同时**存在于 SKILL.md 与仓内 `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md`,
  因此这些措辞本身无法区分「读了 skill」与「读了仓内 Spec」, 不能当污染证据用。
  反向证据: B 臂 (基线) 对这四个短语**零命中**, 且全文 0 次 `AskUser` / 0 次 `GC` / 0 次「释放」,
  说明基线臂本轮确实没有从仓内在制 Spec 语料里学到目标行为 ——
  memory `ab-baseline-leaks-via-repo-corpus` 所警的那条通道在本 eval 未被激活, 本轮区分力结论可用。
