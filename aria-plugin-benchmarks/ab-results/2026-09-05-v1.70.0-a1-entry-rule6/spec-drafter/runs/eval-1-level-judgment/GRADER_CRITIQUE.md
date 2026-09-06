# GRADER_CRITIQUE — eval-1-level-judgment

Prompt: `判断规范等级: 用户请求 '修复登录页面一个 typo'`
断言 2 条 (均无 `[承重]` 标注)。评分结果: 两臂 2/2 全 pass。

---

## 1. 恒真 / 恒假断言 (零信息量)

**两条断言在本 eval 上都是事实恒真, 区分力 = 0。** 不是「碰巧两臂都过」, 是这道题的结构决定了任何
可用回答都会过:

- **断言 1「Should judge as Level 1 (Skip) for trivial fix」= 恒真。** 提示词几乎逐字复制了
  `aria/skills/spec-drafter/LEVEL_GUIDE.md:294` 的示例 3 (`用户请求: "Fix typo in README"` →
  Level 1), 且触发词表 `:57` 直接列了 `typo, fix typo`。`LEVEL_GUIDE.md` **两臂共用、本次变更未动**,
  所以两臂拿到的判定依据完全相同。即便完全不加载技能文件, 「一个 typo → 最低等级」也是常识判定。
  实测两臂给出的是同一句式: 「Level 1 (Skip) —— 不需要 Spec」/「Level 1 (Skip) —— 不需要写 Spec」。
- **断言 2「Should explain why Level 1 was chosen」= 恒真。** 断言未规定解释必须命中哪条判据
  (决策树? 权重公式? 关键词冲突规则?), 只要给出**任何**理由即 pass。两臂都走了同一条链: Q1 → YES →
  不进 Q2, 再套 `score < 3`。凡是给判定的回答几乎不可能只给结论不给理由, 因此该断言无法证伪。

**推论**: 本 eval 对本轮被测变更 (A.1 入口认领块) **零覆盖**, 它只能起「非退化回归」作用 ——
而在「回归」这个用途上它同样偏弱, 因为它判的那部分逻辑 (`LEVEL_GUIDE.md`) 本轮根本没改。
若要让它有信息量, 断言需下钻到可证伪的点, 例如「须点名 Q1 而非仅给权重分」「须识别
`一个` 是范围限定词」「须给出至少一条会把判定顶到 Level 2/3 的反例条件」。

---

## 2. 断言完全没覆盖的重要差异

两臂在**断言测量的那部分 (等级 + 理由) 上几乎无差异**; 全部实质差异都落在断言之外:

**(a) A.1 前置认领 (claim) —— 最大的一处, 完全未覆盖。**
`with_skill` 用了一整节处理它, `old_skill` 一个字都没提。`with_skill` 逐字写道:

> 「本次是**直接调用** `spec-drafter`，没有经过 `phase-a-planner`，所以 SKILL 里那条「起草之前先认领」的
> MUST 落在我这一侧；而且该块**没有 Level 1 例外**」

并给出完整命令 (`phase1_gate.py --raw-track-id ... --phase A.1 --mode advisory --include-terminal
--repo-path`)、`container-id` 取 **`uuid` 字段不是 `label`** 的实参规则、`--linked-issue`「输出为空 ⇒
整个参数省略」「绝不传哨兵」、以及退出义务 `release_gate.py --raw-track-id <同一串> --status abandoned`。
这些是本轮变更的**全部行为面**, 而两条断言对它们不置一词。

**(b) 认领 MUST 的执行 vs 上报 —— 未覆盖, 且是一个真实的判断分歧点。**
`with_skill` 明确**没有**跑那条命令, 理由是「判定结果是 Level 1 ⇒ 本次不会起草任何产物…也就没有可
投入的工作面需要防重复」, 但同时拒绝自行认定豁免: 「所以我**没有**执行下面这条命令，把它连同判断一并
交给你复议，而不是自行认定豁免」。这与 SKILL.md `:73`「**起草之前**先认领, 不可跳过」+ `:80`
「**因此本块无 Level 1 例外**」构成张力 —— 到底该算「正确的不自我豁免上报」还是「MUST 未执行」,
需要评测方明确定义。**当前断言集对此完全失明**: 无论该臂是跑了、没跑、还是跑错参数, 两条断言都照样 pass。

**(c) 升级条件的完整度与终点等级。**
`old_skill` 给 3 条边界, **全部指向 Level 2**; `with_skill` 给 4 条, 且区分终点等级 —— 多出
「同一处错字在多处复制存在，需要跨模块 sweep (前端 + 后端错误码文案等) —— 触发跨模块条件，直接 Level 3」
与「改的不是展示文案而是**标识符**: 表单 `name`、API 字段名、事件埋点名、CSS class、路由 path」,
并提示 `level_override=2` 覆盖开关。断言 2 只要求「解释为什么是 Level 1」, 对反例质量不作要求。

**(d) 「Level 1 只跳 Spec, 不跳其余闸门」这一条只有一臂说。**
`with_skill`: 「Level 1 只是「跳过 Spec」，**不跳过十步循环的其余闸门** —— B.2 验证、C 集成
(含 pre-merge gate, 规则 #8)、D 收尾照走」。这是防「Level 1 = 什么都不做」误读的关键护栏, 断言未覆盖。
相对地 `old_skill` 更主动推进执行: 「要我直接帮你起分支并改吗？」——「继续问 vs 直接干」这条产品性差异
也无断言。

**(e) commit type 精度。** `with_skill` 分档: 「UI 可见字符串用 `fix(login): ...`；若只是注释/文档里的
拼写则用 `docs: ...`」; `old_skill` 只给 `fix(login): 修正登录页文案 typo`。未覆盖。

**(f) 成本 (timing.json, 未覆盖)。** `with_skill` 79,159 tok / 129.0s / 6 tool_uses vs
`old_skill` 73,187 tok / 60.1s / 5 tool_uses —— **耗时 2.15×, token +8.2%**, 换来的是 (a)(c)(d)(e)。
在一道**两条断言都恒真**的题上, 这个代价没有任何断言把它记进账。

---

## 3. 仓内语料污染核查 (`openspec/changes/a1-entry-claim-duplicate-work-guard/`)

**结论: 两臂的 `answer.md` 中都没有出现指向该变更目录的引用; `with_skill` 的认领内容可被
`spec-drafter/SKILL.md` 逐条完整解释, 不需要读该目录即可产生。但因无 transcript, 不能排除工具层曾读过。**

逐项核对 `with_skill` 认领块的每个非平凡 token, 全部在技能文件内有逐字来源:

| `with_skill` 答案中的文字 | 来源 (实读) |
|---|---|
| 「该块**没有 Level 1 例外**」 | `aria/skills/spec-drafter/SKILL.md:80` 「**因此本块无 Level 1 例外**」 |
| 「直调路径的设计前提是「进来时还没有 Level 判定」」 | `SKILL.md:77-80` 幂等分工段 + 「直调路径没有 Level 判定」 |
| `phase1_gate.py --raw-track-id / --phase A.1 --mode advisory / --include-terminal / --repo-path` | `SKILL.md:83-89` 命令块逐字 (含 `:87` `--include-terminal`) |
| 「取 `~/.aria/container-id` 的 `uuid` 字段，不是 `label`」 | `SKILL.md:99` 「`~/.aria/container-id` 的 **`uuid` 字段**, **不是 `label`**」 |
| 「按规则「输出为空 ⇒ 整个参数省略」，绝不传哨兵」 | `SKILL.md:102` 「(**输出为空 ⇒ 整个参数省略**)」+ `:103-105` 哨兵段 |
| `linked_issue_field_probe.py` | `SKILL.md:101` |
| 「补 `release_gate.py --raw-track-id <同一串> --status abandoned`」「僵尸 claim」 | `SKILL.md:129` + `:127` 「缺一就留下永不释放的僵尸 claim」 |

且该臂**自报的出处就是技能文件**: 「SKILL 里那条「起草之前先认领」的 MUST」—— 引的是 SKILL, 不是 proposal/tasks。

**需要留意的两个反向证据 (不足以定性, 但不应隐去):**

1. 短语「Level 1 例外」在仓内**同时**存在于技能文件与变更文档
   (`openspec/changes/a1-entry-claim-duplicate-work-guard/tasks.md:61` 「同款字面量 + 幂等谓词; 无 Level 1 例外」;
   `proposal.md:370` 「`spec-drafter` 直调路径无 Level 判定 ⇒ 不适用本例外」), 因此该短语**不具备区分来源的能力**。
   本次判定依据的是 `with_skill` 的整段措辞与 `SKILL.md:77-80` 的**结构逐句对应**, 而非单个短语命中。
2. 本 AB harness 跑在真仓上, 两臂都有工具权限 (6 / 5 次 tool_uses), 而**本 eval 未保存 transcript**,
   `answer.md` 即全部可见证据。因此「答案文本无污染痕迹」只能支持「未在输出中引用变更文档」,
   **不能证明** 未在工具层读取 `openspec/changes/a1-entry-claim-duplicate-work-guard/` (该目录三份文件共 ~370KB)。
   若要闭合这一问, 需在 harness 侧保留 transcript 或对该目录做读取拦截 —— 建议开单。

`old_skill` 一侧: 全文无任何 claim / phase1_gate / openspec 变更目录相关内容, 无污染痕迹可查。
