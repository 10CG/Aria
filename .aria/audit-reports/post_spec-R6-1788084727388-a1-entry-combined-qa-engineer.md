---
checkpoint: post_spec
round: 6
role: qa-engineer
verdict: REVISE
scope_ok: true
counts: 0C/3M/2m
---

# post_spec R6 (combined) — a1-entry 三份 Spec · qa-engineer 席

## (a) 本席镜头

对抗夹具三态 (baseline 红/绿 vs Spec 自述) + 两臂 (好实现/点名坏实现) 可辨性, 聚焦母 SC-22、字段 SC-1/SC-4/SC-6、探针 SC-17/SC-18/SC-19/SC-20, 外加哨兵/字段名不对称的可分辨性意见。**方法**: 对每条重点 SC 用 Python 忠实重实现其判定逻辑 (E0–E6 / SC-22 的六字面量 + 块边界 / SC-18 三臂), 在 `/tmp` 独立跑, 用真实语料 + 构造夹具双向验证, 从不只读 prose 就下结论。全部命令见下, 均可复跑; 未修改仓内任何文件。

---

## (b) Findings (按严重度排序)

**Critical: 0。** 本席对 8 条重点 SC 做了忠实重实现 + 多组坏实现对抗测试, 没有找到「无论好坏实现都绿」「无论好坏实现都红」或「断言不可构造」的情形——全部经得住测试。以下 3 条 Major + 2 条 minor 是**边界/文档层面**的真实缺口, 不是机制性缺陷。

---

### 字段 M1 — §Why「两级假阳性剔除」自证数字与自引行号, 对当前树重跑不可复现 (且这不是"语料自修改"能开脱的那种漂移)

**位置**: `openspec/changes/linked-issue-field-availability/proposal.md:34-86` (§Why「重测 — 终值」+「两级假阳性剔除」)。

**逐字引文** (`sed -n '58,59p'`):
```
openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:88:   > > **关联 Issue**: [10CG/aria-plugin #122](https://forgejo.10cg.pub/10CG/aria-plugin/issues/122) (open; ...)
```
以及 (`sed -n '65,68p'`, 引号内是文件自己贴的 grep 输出):
```
openspec/changes/linked-issue-field-availability/proposal.md:6    ← 真字段 (dogfood)
openspec/changes/linked-issue-field-availability/proposal.md:65   ← §1 引用的 markdown 链接形反例 (围栏内)
openspec/changes/linked-issue-field-availability/proposal.md:86   ← §1 的模板占位示例 (围栏内)
```

**实跑核验** (逐字复跑文件自己给出的命令, 对**当前工作树**):
```bash
$ grep -rnE '^> \*\*关联 Issue\*\*:' --include=proposal.md openspec/ | grep linked-issue-field-availability
openspec/changes/linked-issue-field-availability/proposal.md:95:> **关联 Issue**: [10CG/aria-plugin #122](...)   # 不是 :65！

$ sed -n '65p' openspec/changes/linked-issue-field-availability/proposal.md
（当前是「与探针 Spec 计数差异」段落里的一句话，不是 markdown 链接形反例）

$ sed -n '86p' openspec/changes/linked-issue-field-availability/proposal.md
（当前是「计数法不同」的解释句，不是模板占位示例）

$ grep -rl '\*\*关联 Issue\*\*' --include=proposal.md openspec/ | wc -l   # 松谓词·文件
17   （文件自称 17，一致）
$ grep -rn '\*\*关联 Issue\*\*' --include=proposal.md openspec/ | wc -l   # 松谓词·行
33   （文件自称 37，不一致，少 4）
$ grep -rlE '^> \*\*关联 Issue\*\*:' --include=proposal.md openspec/ | wc -l   # 严谓词·文件
15   （文件自称 17，不一致，少 2）
$ grep -rnE '^> \*\*关联 Issue\*\*:' --include=proposal.md openspec/ | wc -l   # 严谓词·行
15   （文件自称 19，不一致，少 4）
```

**根因** (已定位, 非猜测): field-Spec 自己的 §Why 数字是用**纯中文拼写**的 grep 命令 (`**关联 Issue**`) 算出来的, 但 2026-08-30 owner 裁定 6i/O-2 落版后, **field-Spec 自己文件头部的 dogfood 字段 (`:6`) 与母 Spec 的 dogfood 字段都已改写成英文 canonical `**Linked Issue**`**——而这条 grep 命令永远不会再匹配到它们。用双拼写口径重跑同一批统计:

```bash
$ grep -rlE '^> \*\*(关联 Issue|Linked Issue)\*\*:' --include=proposal.md openspec/ | wc -l   # 17
$ grep -rnE '^> \*\*(关联 Issue|Linked Issue)\*\*:' --include=proposal.md openspec/ | wc -l   # 19
```
——这才precisely等于文件自称的「17 / 19」。**即文件当初记的数字，恰好是"双拼写口径的今天"，而不是"它自己写的命令的今天"。**「不得把数字本身当规范, 复核一律以下方命令为准」这条自救条款在这里失效了: 字面重跑给出**第三个**数字 (15/15), 既不等于文件冻结的 (17/19), 也不等于双拼写现实 (17/19 恰好同, 但行数 19 对 19 是巧合, 文件里另有的「行」维度 37 vs 33 就对不上)。

**是否波及机制层**: 不波及。§3 的 E0–E6 规则定义本身**已经**是双拼写口径, 我独立按双拼写口径重算的规则原型分布 (`NO_FIELD=132 / NO_TOKEN=14 / OK=3`) 与文件「当日观测值」表里的**同一行数字精确一致** (见下方 SC 三态表 SC-6 行的实跑记录)。受影响的只是 §Why 上半部分的「两级假阳性剔除」教学式演算 (18 行/2 行的剔除步骤) 和它引用的两个行号 (`:65`/`:86`)——这段是**论证脚手架**，不是任何 SC 的断言宿主。

**对照** (好实践的反例): `sibling-spec-probe` 的对应引用 (`grep -n "本轮实测"` 一带, `proposal.md:41-51`) 把同款演示钉死在**不可变的 commit SHA `cc1bdef`** 上 ("本轮实测口径... 主仓 `cc1bdef`")。我验证过 `git show cc1bdef:.../a1-entry.../proposal.md | sed -n '75p'` 精确复现探针 Spec 引用的那一行 (`git cat-file -t cc1bdef` = commit, `git ls-tree -r cc1bdef openspec | grep proposal.md|wc -l` = 147, 与探针 Spec 数字完全对上)。**同一份"三 Spec 合审"语料里, 一份 Spec 把证据钉在 SHA 上活到了今天, 另一份钉在"当前工作树"上五天就失效**——这正是本仓 memory `feedback_freshness_must_be_fetched_not_measured` 的反面教材, 但角色反了 (这次是"测量"→写死成叙述, 而不是该测的没测)。

**建议 (只建议)**: 把 §Why「两级假阳性剔除」一节的引用行号改为指向一个具体 SHA (如 field-Spec 自己已经用的 `cc1bdef`, 或本轮工作树落盘后的新 SHA), 或者把命令改为双拼写口径并显式标注"6i 落版后需双拼写"。不影响任何 SC 的可交付性, 纯粹是文档自洽性。

---

### 字段 M2 — SC-4(f) 的正确判定依赖 E5 对「哨兵」的检查吃 E3 的原始 token_str、而非 E4 已 strip 的 token 元素；此细节未被「它怎么会红」列出的坏实现覆盖，本席亲手踩中

**位置**: `openspec/changes/linked-issue-field-availability/proposal.md:193,195,197,539`。

**逐字引文** (`sed -n '193p;195p;197p'`):
```
193: E3 — token 串: = 该 code span 的内容 ... 不含两端反引号, 不 strip, 不做任何加工。
195: E4 — token 元素: token 串按 ASCII 逗号 (U+002C) split, 每段各自 str.strip()。
197: E5 — 合法性: token 串合法当且仅当 —— 是哨兵 (... 两端无空白、无其他字符 ...), 或 每个 token 元素经 normalize_linked_issue() 返回非 None。
```
SC-4 (`sed -n '539p'`) 第 (f) 分支: `` `none ` `` (尾随空白), 期望 `BAD_TOKEN` (集合封闭; (f) 按 E3「不 strip」+ E5「两端无空白」)。

**实跑**: 我按 E1→E6 的**线性顺序**写了一版"忠实"实现——即拿到 E4 产出的 `token_str.strip()` 之后的元素列表，再对**这个列表**里的元素做 E5 的"是哨兵"判定。这是最自然的管道写法 (E3→E4→E5 顺次消费上一步输出)。跑 6 个 SC-4 夹具:

```
(a) `无`         : OK, sentinel=True   PASS
(b) 裸 `无`       : NO_TOKEN            PASS
(c) `none`       : OK, sentinel=True   PASS
(d) `None`       : OK, sentinel=True   PASS
(e) `N/A`        : BAD_TOKEN           PASS
(f) `none ` (尾随空白): OK, sentinel=True   ← 应为 BAD_TOKEN，红！
```

原因: E4 对元素做了 `str.strip()`，"none " 变成 "none"，此时如果 E5 的"是哨兵"判定复用 E4 的输出（而非 E3 未 strip 的原始 `token_str`），尾随空白已经在到达 E5 之前就被悄悄吃掉，"两端无空白"这条子句永远不会被违反。**把 E5 的"是哨兵"分支的检查对象换成 E3 的原始 `token_str`** 后，六个分支全部转绿。

这不是我编的稻草人——这是我**第一次**尝试忠实实现 E1–E6 时真实产出的 bug，而且是"看起来完全合理"的实现路径（E1→E2→E3→E4→E5 顺次传递）。SC-4 的「它怎么会红」列举了 (a)(b)(c)(d)(e) 五个分支各自对应的坏实现，唯独没有点名 (f) 对应的这个真实存在、我亲手踩中的坏实现形状（"E5 哨兵检查复用了 E4 已 strip 的值"）。**好消息是 fixture (f) 本身有效——它确实能把这个坏实现打红**，缺的只是"它怎么会红"这一栏没有替下一个实现者把这个陷阱明写出来。

**建议 (只建议)**: 在 E5 或 SC-4(f) 的"它怎么会红"补一句，例如："若实现在 E5 的哨兵分支误用 E4 已 `strip()` 的 token 元素而非 E3 未加工的 `token_str` 本身，会在 (f) 上误判为合法哨兵——必须让哨兵判定吃原始 `token_str`。"

---

### 字段/探针 M3 — 哨兵折叠大小写而字段名不折叠：这个不对称对英文 AI 写手有一个具体、可命名的假阴性来源，字段 Spec 自己给的理由没覆盖它 (仅为意见, owner 定)

**位置**: 字段 Spec `§2`(`:154`)、`§3 E0 谓词1`(`:164`)、「本轮引入的新表面」#7(`:591`一带)。

**设计** (逐字, `sed -n '591p'` 一带): "已知限: ASCII 大小写折叠只对 `none` 做, 字段名拼写不折叠 (集合封闭, SC-1(f)) —— 两个不对称是有意的 (哨兵是值, 常见 `None` 写法; 字段名是键, 松了就是第二谓词面)。"

**我的分析**:

1. **哨兵折叠大小写是对的、低风险的**——"none"在任何大小写组合下语义都不含糊 (没有"None 表示 A、NONE 表示 B"这种分裂), 折叠不会引入新歧义, 我在 M2 之外没有找到反例。

2. **字段名不折叠的理由本身有个漏洞**: owner 决策单里否决"只认中文"时给出的反驳 2 逐字是——"『单一谓词面』论证混淆了『拼写唯一』与『判定唯一』…别名在读取侧归一…只多一行正则, 谓词仍是一个"。**这条反驳对"字段名大小写折叠"同样成立**: 把 `linked issue`/`LINKED ISSUE`/`Linked issue` 都归一判定为"命中 Linked Issue 字段", 依然是**一个**语义判定 (是不是这个字段), 只是多几行正则/一次 `.casefold()`——不会像 D9 原来担心的那样制造"写入侧两种教法"的问题, 因为写入侧的模板/SKILL.md 依然只展示 canonical 大小写。field-Spec 自己在决策单反驳 2 上站的立场，和它给字段名画的"折叠=第二谓词面"红线，两者之间有一条没有被回应的张力。

3. **具体、可命名的假阴性来源**——GitHub 的 PR/Issue 侧栏原生功能名就叫 "**Linked issues**" (大写 L、小写 i、复数)。这是训练语料里极高频出现的字符串, 一个不严格照抄模板、凭"这个仓库大概想要类似 GitHub 的 linked issue 功能"去补全字段名的 AI (尤其是面向纯英文项目、SKILL.md 上下文没被完整带入的场景), 有真实概率写出 `Linked issue` (单数、小写 i, SC-1(f) 已覆盖) 或 `Linked issues` (复数, **未被任何 SC-1 分支覆盖**——SC-1 只测了 (f) 小写 i 单数, 没有测复数)。两者都会被判 `NO_FIELD`, 且因为大小写/复数不折叠, 无法被 E0 归一, 是**静默的假阴性**——不是崩溃, 是 check 报警但报警文案 (`NO_FIELD`) 不会告诉作者"你大概是拼错了字段名", 而是笼统地说"没找到字段"。

4. **后果的严重度是"烦"不是"错"**: 这条 check 是 advisory warning (SC-5 的 (a) 分支只是 exit 1 + 点名 path, 不阻断 A.1/A.2), 所以假阴性只造成一次多余的人工/AI 排错循环, 不会污染 `linked_issue_overlap` 的匹配结果 (那条路径由 `--linked-issue` 实参单独把关, 字段名拼错只影响"能不能自动抽出 token", 不会让错误 token 参与比对)。

**我的意见 (仅供参考, owner 裁)**: 我认为把字段名的 E0 谓词1 也做 ASCII 大小写折叠 (但**不**放宽单复数——"Issues"复数在语义上确实可能指向别的东西, 折叠代价更高) 是一个低风险、有真实证据支撑的加固, 且不违反 owner 已经在决策单里对"拼写≠判定"给出的论证。但这终究是"要不要多接受一种拼写"的范围决策, 按 Rule #10 不该由我这轮自行拍板——留给 owner。**如果 owner 认为现状可接受**, 建议至少在 SC-1 里补一个 "(g) `Linked issues`(复数, 集合外)" 分支, 让"单复数"这个额外的真实假阴性来源被显式测到, 而不是只测大小写这一个轴。

---

### 母 m1 (minor) — SC-22 ⑤ 的定位依据「`A.1 - Spec 管理:` 项下」在 `phase-a-planner/SKILL.md` 里对应 7 个 \`\`\`yaml 围栏中的哪一个, 需要显式的"按锚点搜围栏"提示, 否则容易被写成"抓第一个 yaml 围栏"

**位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:605` SC-22 ⑤。

**实测**: `phase-a-planner/SKILL.md` (d50f9c3) 全文有 **7 处** `` ```yaml `` 围栏 (`grep -n '```yaml' pa-planner.md` → `:47 :62 :103 :146 :161 :230 :249 :265`, 8 处围栏开始标记中 7 个是 yaml)。SC-22 ⑤ 要断言的目标在 `:62` 一带的围栏 (含 `A.1 - Spec 管理:`)。我第一次写检查脚本时用 `re.search(r'```yaml(.*?)```', text, re.S)` (非贪婪, 抓文件里**第一个**yaml 围栏) 去找 `precondition:` 字面——抓到的是 `:47-58` 那个不相关的围栏, 断言在"好实现"夹具上误判为红。改成"先按 `A.1 - Spec 管理:` 定位含它的那个围栏, 再在其内查 `precondition:`"后, 好实现正确转绿。

SC-22 ⑤ 的文字本身**是**给了锚点 ("`A.1 - Spec 管理:` 项下")，一个仔细的实现者按字面就不会踩这个坑——所以这不是断言设计缺陷，而是"给下一个写测试宿主的人一个更直白的提示"的机会。

**建议**: 在 SC-22 ⑤ 后加一句实现提示，例如："宿主实现须先定位含 `A.1 - Spec 管理:` 的那个 \`\`\`yaml 围栏 (文件内共 7 处 yaml 围栏, 不可抓第一个), 再在其内检查 `precondition:` 字面。"

---

### 母 m2 (minor) — SC-3/SC-15 的"怎么会红"未点名"负控 (第三方 claim) 与正控用同一个 track_id 前缀"这种夹具构造错误, 但影响很小

**位置**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md:586` SC-15。

SC-15 要求"另起一条无关的第三方 active claim 作负控", 断言改名两步后"第三方 claim 仍 active"。我按夹具描述实现时发现: 如果第三方 claim 的 track_id 与"旧串"/"新串"共享字符串前缀 (例如都用同一个 `<container_uuid>` 段), 且被测实现内部用了子串匹配而非精确相等去定位 claim, 负控会被误伤。Spec 原文没有强制"第三方 claim 的 track_id 必须与旧/新串在任何前缀/后缀上都不同"这一条夹具构造约束。**这是很窄的一个点**——`release_claim_by_track` 现有实现 (`lib/claim_lifecycle.py:377` 起) 走的是精确匹配 `(container, 归一 track_id)`，不是子串匹配, 所以今天不会真的触发；只是"未来某个坏实现用子串匹配"这一种假实现方式不会被本条 SC 的字面要求排除。不影响当前判定为绿/红的结论, 标 minor 仅供夹具设计参考。

---

## (c) 逐条 SC 三态表

图例: 「实跑」= 本席写代码/跑命令独立复现; 「grep 核验」= 本席直接对源码/文档跑核验命令但未做完整对抗夹具模拟; 「文本自洽」= 仅读 prose 判断逻辑自洽性, 未独立执行。

### 母 Spec `a1-entry-claim-duplicate-work-guard`

| SC | 类别 | baseline 实测 | Spec 自述 | 两臂可辨? | 备注 |
|---|---|---|---|---|---|
| SC-1 | ⛔撤销(1A) | — | 无对象 | n/a | 确认表内保留、编号未复用 |
| SC-2 | 代码(CLI全链路) | **绿**(实跑: `--linked-issue`/`linked_issue_overlaps` 今天已接线, `--include-terminal` 今天 0 命中—新增) | baseline 即绿(回归守卫) | 可辨(读 collision.py:265-266/278-279 逐字确认) | 逐字命中 |
| SC-3 | 代码 | 未独立实跑(需真实 identity.py 环境), 文本自洽 | — | 文本自洽 | `identity.py:191/222/242/244` 逐字核对全部命中 |
| SC-4 | ⛔撤销(1A) | — | 无对象 | n/a | — |
| SC-5/6/7 | 代码 | **红**(grep核验: `claim_lifecycle.py` 今天无 `by_track` heartbeat 变体, 只有 `heartbeat()` 按 (container,session)) | baseline 必红 | 文本自洽(SC-7 第二臂设计合理, 已有回归测试`test_release_by_track.py:380`不会误配合) | `:228` 逐字命中 |
| SC-8 | 代码(CLI) | **绿**(grep核验: `_TERMINAL=("done","abandoned","unknown")` 今天不含 yielded) | 该子例baseline即绿 | 文本自洽 | `:268` 逐字命中 |
| SC-9 | 行为 | n/a(无代码宿主, 诚实标注) | 行为类 | 文本自洽, 分类诚实 | — |
| SC-10 | 代码(CLI) | **红**(grep核验: 全文 `error=` 赋值无一处是 `"fetch_degraded"`, 该 token 仅出现在 :210 docstring) | baseline必红 | 文本自洽 | 逐字命中 |
| SC-11/12 | 行为 | n/a | 行为类 | 文本自洽 | — |
| SC-13 | ⛔迁出 | — | 已迁字段Spec | n/a | — |
| SC-14 | 代码(a)+行为(b) | 未独立实跑 | — | 文本自洽 | (a)臂逻辑清楚, 与SC-23同根 |
| SC-15 | 代码(回归守卫) | **绿**(grep核验: `release_claim_by_track:377`、`acquire_claim:99` 均实存) | baseline即绿 | 可辨, 但见母m2(夹具前缀构造的窄边界) | 行号逐字命中 |
| SC-16~19 | ⛔迁出/由SC-29承接 | — | — | n/a | — |
| SC-20 | ⛔撤销 | — | — | n/a | — |
| SC-21 | 行为 | n/a | 行为类, 两臂(挂载/未挂载)描述清楚 | 文本自洽 | — |
| SC-22 | 代码 | **红(实跑, 见(b)镜头详述)**: ①-⑥全部逐字核实baseline 0命中; 5 种坏实现(塞入YAML动作列表/`--phase B`残留/`编排层记忆`式弱化谓词/字面量置于块外/heading仅存在于fence示例内)全部被正确打红; GOOD夹具全部转绿 | baseline必红 | **可辨(5/5坏实现全部正确判红, 实跑证实)** | 见 m1: ⑤的yaml围栏定位需要显式提示 |
| SC-23 | 代码(CLI) | **红**(grep核验: A.1原串≠carry-id现状确认, `claim_lifecycle.py:377/425`匹配键逻辑核对) | baseline必红 | 文本自洽 | — |
| SC-24 | 代码(CLI) | **红**(grep核验: `unknown_schema_claims` 全文0命中) | baseline必红 | 文本自洽 | — |
| SC-25 | 代码+行为 | **红**(grep核验: `linked_issue_overlap_error` 全文0命中; `:1236-1238`确认except写`out["linked_issue_overlap"]=[]`) | baseline必红 | 文本自洽 | — |
| SC-26 | 行为 | n/a | 行为类 | 文本自洽 | — |
| SC-27 | ⛔撤销(1A) | — | 无对象 | n/a | — |
| SC-28 | 行为 | n/a | 行为类,两臂(遵守/无视opt-out)描述清楚 | 文本自洽 | — |
| SC-29 | 代码(CLI,回归守卫) | **绿**(grep核验: `collision.py:278-279` 逐字确认自排除已实存) | baseline即绿 | 文本自洽(负控实现方式`删掉:278-279`已明确给出) | 逐字命中 |
| SC-30/31 | ⛔撤销(1A) | — | 无对象 | n/a | — |
| SC-32/33 | 代码 | **红**(grep核验: `unknown_schema_claims`/心跳telemetry写入均0命中) | baseline必红 | 文本自洽 | — |

### 字段 Spec `linked-issue-field-availability`

| SC | 类别 | baseline 实测 | Spec 自述 | 两臂可辨? | 备注 |
|---|---|---|---|---|---|
| SC-1 | 代码 | **红(实跑)**: 6分支(a-f)全部按忠实E0实现验证, 3种坏实现(松谓词/fence正则漏`(?:> ?)?`/字段名大小写不敏感)全部被(b)(c)(d)/(d)/(f)正确捕获 | baseline必红 | **可辨(实跑证实)** | 详见(b)节 |
| SC-2 | 代码 | **红(实跑)**: "任意位置code span"坏实现在此夹具上误抽`confirmed`, 正确实现返回NO_TOKEN | 该形状真实语料6条 | **可辨(实跑证实)** | — |
| SC-3 | 代码 | **红(实跑)**: (a)(b)双臂验证, "整串不分逗号直接归一"坏实现在(a)上误判 | — | **可辨(实跑证实)** | — |
| SC-4 | 代码 | **红(实跑, 找到M2)**: (a)-(e)全部转绿; (f)在"E4→E5顺序管道"坏实现上意外转绿(即M2), 修正顺序后6分支全绿 | baseline必红 | **(a)-(e)可辨; (f)可辨但需注意E3/E4/E5数据流顺序(见M2)** | — |
| SC-5 | 代码(CLI) | 未独立实跑脚本(脚本不存在), 文本自洽 | baseline必红 | 文本自洽, 四臂逻辑分离清楚 | (e)/(e1)/(e2)的fail-open修正在R4已入版, 文本读来自洽 |
| SC-6 | 代码 | **红(实跑)**: `grep -c "Linked Issue" standards/openspec/templates/proposal-minimal.md` = 0; `grep -c "关联 Issue"` = 0; 模板确认有Level/Status/Created三行头部+Impact段, 无字段行 | baseline必红 | 文本自洽 | 见(b) M1: §Why上方数字表已漂移, 但此SC本身独立核验为真 |
| SC-7 | 行为 | n/a(诚实标注, 无代码宿主) | 行为类 | 文本自洽 | — |
| SC-7a | 代码 | **红(grep核验)**: `spec-drafter/SKILL.md:127-162`预览围栏精确核对, `:139-140`仅两行(Level/Status), 无Created/Linked Issue | baseline必红 | 文本自洽, 块边界定义清楚(D17①) | 行号精确命中 |
| SC-8 | 代码 | 未独立实跑(check尚不存在), 文本自洽 | baseline必红 | 文本自洽, (b)分支专门钉住"D3改判不得被悄悄退回" | — |
| SC-9 | 代码(CLI) | **红(实跑逻辑验证)**: K8四态分派表逻辑经我的corpus_scan.py交叉验证一致 | baseline必红 | 文本自洽 | 与探针SC-19同源黑名单需求已核对一致 |

### 探针 Spec `sibling-spec-probe`

| SC | 类别 | baseline 实测 | Spec 自述 | 两臂可辨? | 备注 |
|---|---|---|---|---|---|
| SC-1~6 | 代码 | 未独立实跑(脚本不存在), 文本自洽 | baseline必红/绿描述清楚 | 文本自洽 | SC-5自命中排除与母SC-29同一形状, 逻辑一致 |
| SC-7/SC-8 | 代码 | **绿(grep核验/corpus_scan.py交叉验证)**: `archive/2026-07-31-.../proposal.md:6`与`archive/2026-08-22-.../proposal.md:22`两行确认存在, 冒号后首字符为`[` | 立项案例 | 文本自洽 | 与我的corpus_scan.py分类结果(url_fallback桶)一致 |
| SC-9/10/11 | 代码 | 未独立实跑, 文本自洽 | — | 文本自洽 | 层1.5与层2互斥关系读来自洽, 与我的分类脚本"none_sentinel"独立于"url_fallback"设计一致 |
| SC-12/13/14 | 代码 | **红(grep核验)**: `git symbolic-ref refs/remotes/github/HEAD` 结构性验证依赖真实git环境未独立复现, 但`resolve_enforced_remotes`函数确认存在于`multi_remote.py:255` | baseline必红 | 文本自洽 | 行号精确命中 |
| SC-15 | 代码 | 文本自洽 | — | 文本自洽 | — |
| SC-16 | 行为 | n/a(诚实标注) | 行为类 | 文本自洽 | — |
| SC-17 | 代码 | **红(实跑)**: `grep -c "每轮入口: 竞品 spec 探针" execution-modes.md` = 0; 确认`## Convergence 模式`(:84)与`## Challenge 模式`(:113)两节及各自围栏块存在 | baseline必红 | 文本自洽(计数=2的保守性质已被Spec自己在"新表面"#5坦承) | — |
| SC-18 | 代码 | **实跑, 见(b)节及corpus_scan.py**: (a)臂在当前149篇语料上得no_field=132/url_fallback=13/no_token_no_url=1/簇=3(不含母Spec)——与文件147篇口径的133/13/1有1的出入(总体差异, 非矛盾, 见M1同源问题); (c)臂"只在首`---`前找"复现"簇降为1"的质变; (b)臂(宽松匹配)在**当前**语料上未复现母Spec假阳性(因该行已被rework v4移除, 需查`cc1bdef`历史快照复现, 我已验证`cc1bdef:75`逐字命中) | 三臂+第四臂设计描述 | **可辨(a)(c)质变明确; (b)臂需要固定在cc1bdef快照上复现，探针Spec本身已正确锚定cc1bdef，不是探针的缺陷** | 第四臂(合成夹具, 围栏排除)逻辑与字段SC-1(b)/(d)同源, 已在字段测试中验证 |
| SC-19 | 代码 | **红(实跑)**: 无黑名单guard时两份placeholder proposal确认产生真实碰撞(`("r","{<org>/<repo>#<n>}")`两侧相等); 加guard后碰撞消失 | baseline必红 | **可辨(实跑证实)** | 与字段SC-9同源约束一致 |
| SC-20 | 代码 | **红(grep核验)**: `audit-engine/SKILL.md`全文0命中"per-round 入口探针"/"sibling_spec_probe"; 确认`audit-engine`目录在d50f9c3上确实只有references/(7文件)+SKILL.md=8文件, 无scripts/无tests/ | baseline必红 | 文本自洽(与SC-22同构的块边界机制, 已在母SC-22验证过同类机制可靠) | 逐字命中"全目录8个文件" |

---

## (d) 本席核验为真、无 finding 的清单

- 母 SC-22 的①-⑥全套断言 (heading正则+fence排除+块边界切片+六字面量+④负控+⑤yaml定位+⑥两行退出义务字面) 经 5 种坏实现对抗测试全部正确打红, GOOD夹具全部转绿——**这是本轮验证强度最高的一条 SC, 设计健全**。
- 字段 SC-1 的三条谓词 (深度锚定/围栏排除含`(?:> ?)?`前缀/取文档序第一条) 经 3 种坏实现 (松谓词/fence正则漏blockquote前缀/字段名大小写不敏感) 对抗测试, 每种坏实现都被恰好设计用来抓它的那个分支正确捕获，没有交叉污染或漏判。
- 字段 SC-2 (E2"冒号后第一个非空白必须是反引号"而非"行内任意code span") 的设计正确防住了真实语料6条`triage \`confirmed\`` 误抽的形状。
- 字段 SC-4 的哨兵×大小写×集合封闭三个轴经六分支验证全部正确 (含M2指出的顺序陷阱修正后)。
- 字段 SC-6、母 SC-6/spec-drafter预览骨架相关的全部行号引用 (`:429`、`:127-162`、`:139-140`) 逐一 `sed -n` 核对，无一处失实。
- 母 spec 关于 `identity.py:191/222/242/244`、`collision.py:265-266/278-279`、`track_id.py:61-76`、`claim_lifecycle.py:99/228/274/377`、`branch-manager/SKILL.md:146`、`phase-b-developer/SKILL.md:86-96`、`multi_remote.py:255` 等**十余处**逐字行号引用，本席逐条 `git show d50f9c3:<path> | sed -n 'Np'` 核对，**全部精确命中，无一处漂移**——这是极高的事实断言精度，值得记录为正面信号。
- 探针 Spec 把动机语料证据钉在不可变 SHA `cc1bdef` 上 (而非"当前工作树")，本席验证该锚点百分之百可复现 (`git cat-file -t cc1bdef`=commit, 文件计数/行内容精确匹配)——这是**好实践**，与字段 M1 指出的反例形成鲜明对照。
- R5 聚合报告要求的三条机械不变量 (「每个 SC-NN 在 SC 表内」「每个 --flag 在 Impact 表内」「同一枚举全文一种拼写」) 本席在 rework v4 母 Spec 上独立复跑，**三条全部为真** (SC-1~33 无遗漏; `--flag`/`--is-ancestor`/`--spec-slug` 三个疑似缺口经核查均为误报或已在Impact表内; `wu_empty`/`bad_token_union`/`none_sentinel` 拼写全文统一)。**R5-1 指出的"落版未回灌三张表"问题在rework v4 已经修复**。
- 探针 SC-19 与字段 SC-9 的常量黑名单需求同源一致，两份 Spec 互相点名交叉核对无遗漏。
- 探针 SC-17 的「计数恰2」保守性质、探针 SC-18 的第四臂 (围栏排除) 设计与字段 SC-1(b)(d) 完全同构，跨 Spec 复用同一机制而非各自造轮子。

---

## (e) 收敛判断

**本轮 3 条 Major 中, 2 条 (字段M2的docstring补白、字段/探针M3的哨兵×字段名不对称) 直接命中 2026-08-30 当天新写/新扩的文本** (M2 的(f)分支是6i裁定新增的`none`哨兵测试用例; M3 是"本轮引入的新表面#7"自己列出的已知限)；**第 3 条 (字段M1) 是老文本 (2026-08-25 §Why) 被同一份文件里 2026-08-30 新写的 dogfood 改动间接波及导致失效**——三条全部与 2026-08-30 当天改动直接或间接相关, 没有一条落在更早 (R1-R5) 就已经审过、本该被抓住却被漏掉的老问题上。

结合：(1) 0 Critical；(2) 本轮验证强度最高的两条断言 (母SC-22、字段SC-1/4) 经过最严格的多坏实现对抗测试，全部经受住考验；(3) R5 聚合报告点名的"三张表未回灌"问题，本席独立复核确认 rework v4 已经修复；(4) 我的 3 条 Major 全部是"新文本第一次被对抗夹具照面"时出现的正常边界问题, 不是"设计层面根本性想错了"——**本席同意"设计侧已收敛"的判断**。这三条更像是把一份已经想清楚的设计，从"prose 自洽"打磨到"字节级可执行、可被下一个实现者无歧义复现"过程中必然会暴露的最后一层毛边，而不是新的设计缺陷。

也因此本席 verdict 定为 REVISE 而非 PASS：3 条 Major（尤其是 M3，owner 明确要求"给出意见供裁决"）需要 owner 过目定夺，但不认为需要再开一整轮通用审计——性质上更接近 R5 结论"剩下是机械活"的延伸：这次是"三处文档自洽性小修 + 一个待裁的范围问题"，均可在清账/落版阶段一次性处理，不需要新一轮 R7。

---

## (f) Counts

**0 Critical / 3 Major / 2 minor**

- Major: 字段M1 (§Why 自证数字/行号对当前树不可复现)、字段M2 (SC-4(f) E4/E5数据流顺序陷阱未被"它怎么会红"点名)、字段/探针M3 (哨兵×字段名折叠不对称的假阴性意见，仅供裁决)
- minor: 母m1 (SC-22⑤的yaml围栏定位提示)、母m2 (SC-15负控夹具前缀构造的窄边界提示)
