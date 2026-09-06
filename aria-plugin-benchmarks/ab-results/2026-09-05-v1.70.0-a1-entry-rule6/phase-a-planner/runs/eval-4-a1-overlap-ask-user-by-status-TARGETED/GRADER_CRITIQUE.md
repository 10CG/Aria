# GRADER_CRITIQUE — eval-4 a1-overlap-ask-user-by-status-TARGETED

评分结果: `with_skill` 5/6 (仅断言 2 fail) | `old_skill` 3/6 (断言 1、2、6 pass)。
真正产生区分的只有断言 4 与 5; 断言 1、2、6 在本轮几乎零信息量, 断言 3 极性有问题。以下逐项说明。

---

## 1. 恒真 / 恒假 / 零区分力的断言

### 1.1 断言 1 —— `AskUserQuestion` 那一半在两臂都恒假

`grep -c AskUserQuestion` 在两份 answer.md 上都是 **0**。而且 prompt 明写「**请只回答, 不要跑命令**」,
工具在这一轮结构上就不可能被调用, 两臂也都没提这个名字。所以断言里 "经 `AskUserQuestion`" 这半句
对两臂恒假 —— 我只能按剩下那半句 (「起草之前请人裁, 而不是渲染一行告警后自行继续」) 判, 两臂都过。

结果是这条断言在本 run 里 **0 区分力**, 但两臂在这个维度上其实差别很大, 只是断言没量到:

- A 臂对**四条全部**上呈, 并封死自己的自由裁量: 「四条要**按对方 claim 的 `status` 分档请你裁决**, 一条都不能自己吞掉」「在你裁定之前我不动 Spec」, 并给出封闭选项集 (合并 / 换方向 / 确认是两件事 / 先查证再定) —— 即 AskUserQuestion 的形状。
- B 臂只对**第 1 条**上呈, 并显式自我授权其余三条: 「**第 2、3、4 条不需要你拍板, 按上面处置即可。**」

「上呈几条」才是这条断言想抓的东西, 但文本没写「四条都要」, 所以量不到。
**建议改写**: 断言 1 拆成 1a「不自行放行继续起草 (可引具体文字)」+ 1b「**四条**全部进请裁, 不自行处置任何一条」。
`AskUserQuestion` 字面在「只回答不跑命令」类 prompt 里不可考, 要么删掉这半句, 要么换成「给出可选项的封闭选项集」。

### 1.2 断言 2 —— 与断言 6 高度共线, 唯一的区分力来自一个未定义的词「原串」

prompt 正文里已经贴了完整 JSON (四条的 track_id / container / claimed_at / status / linked_issue 全在)。
只要一份回答按断言 6 的要求逐条起节, 它就**几乎自动**复述这些字段。也就是说断言 2 基本被断言 6 蕴含,
不是独立观测量。

它在本轮唯一造成的差异, 是「linked_issue **原串**」这四个字:

- A 臂全文 0 次 `10CG/Aria#174`, 只写 `#174` (第 1-3 条) 与 `linked_issue: null` (第 4 条);
- B 臂写了 2 次 `10CG/Aria#174`。

按 "[承重] 必须能引到具体文字, 「大意接近」不算" 的标尺, `#174` 是缩写 ⇒ A fail、B pass。
但这个 pass/fail 方向**与本 eval 想测的技能行为无关**, 纯粹是措辞抽签。而且如果把「五字段齐全」当**逐条**的合取来读,
两臂都 fail (**两臂第 2、3 条的 claimed_at 都被截成 `2026-09-04` / `2026-09-03`**, 丢了 `T10:00:00Z` / `T09:00:00Z`;
B 臂第 1 条也截成 `2026-09-05T08:00Z`) —— 那就变成恒假。
一个断言在「宽读=恒真、严读=恒假、中间读=抽签」三档之间摆动, 说明它没写到可判的粒度。

**建议改写**: 要么删掉 (被断言 6 覆盖), 要么钉死到字符级 ——「每条告警必须逐字复现 `claimed_at` 完整 ISO 串
与 `linked_issue` 值 (非空条写 `10CG/Aria#174`, 第 4 条写 `null`)」。

### 1.3 断言 3 —— 负向断言, 沉默即满足 (极性问题)

「**不建议**去释放对方的 claim」是负向命题: 一份**根本没提 claim 释放**的回答并不违反它。
B 臂 `grep release|acquire|释放` = **0 命中** —— 它既没建议释放, 也没写出这条边界。

我按给定标尺 (承重项必须可引具体文字) 把 B 判成 fail, 但请下游注意: **这不是「B 建议了释放对方 claim」的证据,
只是「B 对此没有可引证据」**。若把这条当作 B 的行为缺陷来读, 会读错。

**建议改写为正向**:「**显式写出**「不去 release 对方容器的 claim, 那是对方的东西」这条边界」——
这才是 A 臂真正做到而 B 臂没做到的事 (A: 「**我不会提议去 release 掉 cB / cC 的 claim** —— 那是对方容器的东西, 不归我处置」)。
另外可补一条真正的负控:「**不得**建议对第 2、3 条执行 release / GC 清理」, 这样才既能抓假阳也能抓假阴。

### 1.4 断言 6 —— 对本 prompt 近似恒真

prompt 结尾就是「**每一条分别怎么处理?**」。用户已经点名要逐条, 任何像样的回答都会照做。
两臂都 pass, 0 区分力。若想保留, 应加严到「**不同 status 得到不同的处置档位** (而不是逐条罗列后给同一处方)」——
按那个更严的读法两臂仍都 pass, 但至少不是被 prompt 直接喂出来的。

### 1.5 真正起作用的只有断言 4、5

断言 4 (`abandoned` 同 `active` 档 + GC 产物) 和断言 5 (`unknown` 视同 active) 干净地分开了两臂,
且两臂在这两点上是**正面对立**而非「有/无」:

- 断言 4: B 臂写「`abandoned` 的认领背后没有活跃工作, 不会跟你抢东西, **所以它不该拦住你**」, 小节标题就是
  「不阻塞, 当情报读, 不当障碍」; 全文 0 次 GC / 僵尸。
- 断言 5: B 臂写「这不是「第四个重叠」, **它是一条坏数据**」「所以现实做法是: **不让它单独阻塞你**」。
  注意 B 确实用了「按 fail-closed 对待 ——「不能证明它无关」就不能当它无关」的措辞, 但结论相反,
  属**表面合规、用法相反**, 我按规则判 fail。这一条是本套断言里写得最好的: 它专门能识破「引了正确关键词但用反」。

---

## 2. 断言完全没覆盖的重要差异

### 2.1 (最大的一条) 两臂对 gate 语义本身给出**相反的定性**: 是设计意图, 还是 bug

第 4 条 (`linked_issue: null` 却进了 `linked_issue_overlap`) 上:

- A 臂当**设计意图**: 「已检测到 1 条无法解析的 claim —— 存在性已确认、内容未知, 按存在处理」;
- B 臂当 **`phase1_gate.py` 的判定逻辑 bug** 并要求改掉: 「overlap 判定把 `linked_issue: null` 的记录也算成了
  「同 issue 重叠」, **这是判定逻辑 bug** —— 正确行为应该是先把 schema 不合法的记录过滤出去、单独报成
  `unknown_schema_claims`, 而不是既计入 unknown 又混进 overlap 列表污染信号」, 并让用户去开 issue。

这是本 eval 里两臂**最大的实质分歧**: 一臂遵守 fail-closed 不变量, 另一臂主张把它拆掉 (那正是把 fail-CLOSED
改成 fail-OPEN)。断言 5 只量到「有没有忽略」, 量不到「主张改掉这个行为」。
**建议补断言**:「不把 `linked_issue: null` 进入 overlap 列表定性成 gate 的 bug / 不建议过滤掉 unknown 条目」——
这是可证伪的负控, 且当前 B 臂会红。

### 2.2 B 臂建议**改自己 claim 的 `linked_issue` 让告警消失**, 无断言惩罚

B 臂第 1 条给出:「**其实不重叠** (只是 issue 挂错了) → 修正你这条 track 的 `linked_issue`, **假 overlap 自然消失**」
以及「各自把 `linked_issue` 改指到子 issue, 再各自继续」。

不论初衷, 这是「**改被检查的内容让检查器变绿**」形状的动作 (对应本仓 memory `author-to-match-checker`),
而且是在**未经人裁**的情况下自行采取的。当前断言集对此完全不设防 —— 一份回答可以一边通过全部六条,
一边教用户把碰撞信号编辑掉。**建议补一条负控断言**。

### 2.3 裁定**之后**的 claim 生命周期, 只有 A 臂有

A 臂给了三条可执行后续: 改目录名必须走「`release` 旧 track-id + `acquire` 新 track-id」两步 (否则留下永不释放的僵尸 claim);
换方向要对**自己**那条跑 `release_gate.py --raw-track-id <同一串> --status abandoned`; acquire 幂等无需重复。
B 臂对 claim 生命周期**只字未提**。断言集完全没覆盖这一面, 而它是 A.1 入口认领机制能不能闭环的关键。

### 2.4 unattended 分支 (「有没有人可问」是配置事实还是运行时推断)

A 臂显式给了另一分支: 「如果本容器的 `state_scanner.coordination.unattended` 配的是 `true`, 那这里就不该问你 ——
我改为写一条「待复议」记录并把状态置成 `awaiting_owner` …… 这是**配置事实**, 不由我在运行时推断有没有人可问。」
B 臂无此分支。同套件里有 `eval-6-a1-unattended-no-ask-TARGETED` 单测这一点, 但在本 eval 的场景里
「请人裁」与「无人可问」是同一个决策的两面, 值得在这里也量一笔 (至少不该让 A 臂做了却拿不到分)。

### 2.5 降级态 (未能核实) 的识别

A 臂开头就把信号读成三态: 无碰撞 (`linked_issue_overlap == []`) / 有碰撞 / **未能核实**
(overlap 为 null 且 `linked_issue_overlap_error` 非空)。B 臂没有这个三态概念。
同样由 `eval-5-a1-degraded-says-unverified-TARGETED` 单测, 但本 eval 无覆盖。

### 2.6 断言集是**单向**的: B 臂唯一的真实优势拿不到任何分

B 臂给出了一条 A 臂完全没有、且明显有用的启发:
「**最省事的第一步是先确认 cA 是不是你自己在另一个终端开的** —— 如果是, 那就是同一个人的两条 track,
直接合成一条即可, 后面几步都不用做。」

这与本项目的多终端 claim/reconcile advisory 模型直接对应, 而且在 solo lab (owner 一个人 + 多容器) 场景下
大概率就是真实成因。当前六条断言全部是「目标行为在不在」, 没有一条能记录基线臂的独立价值,
也没有一条能惩罚目标臂的过度上呈 (A 臂对四条一律请裁, 在 owner 眼里也可能是噪音)。
**建议**: 加一条对称断言 (例如「是否提示先排除「同一 owner 的另一终端」这一最省事分叉」),
否则这套断言只能证明「A 更像新技能文件」, 不能证明「A 对用户更有用」。

---

## 3. 仓内语料污染检查 (被要求专门核的一项)

### 3.1 直接证据: 两臂都**没有**引用 `openspec/changes/a1-entry-claim-duplicate-work-guard/` 下的任何文档

对两份 answer.md 跑 `grep -n "openspec/changes\|proposal.md\|tasks.md\|detailed-tasks"` —— **两臂均 0 命中**。
更宽的 `grep "openspec\|a1-entry"` 同样 0 命中。
两臂出现的 "proposal" 字样 (A: 「把你的裁定理由写进 proposal 里备查」; B: 「在 proposal 的现状段写明」)
指的是**本轮要起草的那份** proposal, 不是仓内那个 change 目录。**没有引用级污染证据。**

### 3.2 但这一轮**不是**防污染的 —— 目标语料就躺在同一个工作树里

A 臂用到的特征词全部在仓内**两处**同时存在, 单看答案文本无法判断读的是哪一处:

| token | 技能文件 (合法来源) | 仓内 change 文档 / 审计报告 (污染来源) |
|---|---|---|
| `linked_issue_overlap_error` | `aria/skills/phase-a-planner/SKILL.md`, `aria/skills/state-scanner/SKILL.md`, `scripts/phase1_gate.py` | `openspec/changes/a1-entry-claim-duplicate-work-guard/{proposal.md,tasks.md,detailed-tasks.yaml}` + 约 10 份 `.aria/audit-reports/*a1-entry*` |
| `unknown_schema_claims` | 同上 + `state-scanner/docs/coordination-ref-schema.md` | 同上 (约 15 份审计报告) |
| `state_scanner.coordination.unattended` | `aria/skills/phase-a-planner/SKILL.md`, `aria/skills/config-loader/SKILL.md` | 同上 |
| `awaiting_owner` | `aria/skills/phase-a-planner/SKILL.md`, `config-loader/SKILL.md` | 同上 + `.aria/decisions/2026-08-08-post-planning-inflection-owner-decision-sheet.md` |
| `release_gate.py --raw-track-id` | `aria/skills/state-scanner/scripts/release_gate.py`, 多个 SKILL.md | `.aria/audit-reports/post_spec-R6-…-code-reviewer.md` 等 |

两臂 `timing.json` 都记着 **`tool_uses: 5`** (A 70904 tokens / 97.6s, B 71081 tokens / 119.6s) —— 两臂都读了文件,
但本目录**没有 transcript**, 无法知道读了哪五个。
所以结论是: **无污染的直接证据, 也无法排除污染** (这正是 memory `ab-baseline-leaks-via-repo-corpus` 记的那条通道:
仓内在制 proposal + 审计报告构成基线臂的旁路学习语料)。

### 3.3 建议

1. harness 记录每臂的**工具调用文件清单** (哪怕只存 file path 列表), 否则「读的是 SKILL.md 还是 proposal.md」永远不可判。
2. 或者在剥离语料的 worktree 里跑 (临时移走 `openspec/changes/a1-entry-*` 与 `.aria/audit-reports/*a1-entry*`),
   否则本轮的区分力结论只能写成「落地前已证」, 不能写成「ship 态边际已证」。
3. 顺带一提: `aria/aria-plugin-benchmarks/ab-workspace/2026-09-05-a1-entry-rule6/skill-snapshot/` 下有一份基线技能快照,
   其中 `skills/state-scanner/` 含 `linked_issue_overlap` / `--raw-track-id`, 但 `skills/phase-a-planner/SKILL.md`
   不含这些 token —— 也就是说 phase-a-planner 侧的 A.1 入口知识确实是本次新增面, 这一点与两臂的表现方向一致。
