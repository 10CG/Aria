---
verdict: PASS_WITH_WARNINGS (0C/2M/4m)
agent: qa-engineer
round: R1
critical_count: 0
major_count: 2
minor_count: 4
---

# post_spec R1 审计 — secret-guard-nomad-var-put-echo (qa-engineer 视角)

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`

方法论: 未改任何文件; 对 `aria/hooks/secret-guard.sh` 做了真实调用验证 (baseline 现状) +
在 `/tmp/.../scratchpad/` 构建了一份按 proposal「What」章节字面实现的忠实副本
(`secret-guard-impl.sh`, 未落回仓库) 跑穷举状态空间, 并另建一份「误实现为全局 credit」
的对照副本验证 SC-9 canary 真实可证伪性。所有命令均实测取得 exit code, 非推演。

## 结论总览

设计整体扎实: SC-2/SC-3 baseline-failing 已实测确认非空真绿 (现状 exit=0); SC-9 语境守卫
canary 已实测确认在「误实现为全局 credit」下三条命令真的翻红 (0/0/0), 在正确实现下保持
exit=2 (2/2/2) —— 是一个真正可证伪的回归锚点, 非装饰性断言。但发现 2 条 Major (均是「实现
按 What 章节字面执行会产生的真实副作用」，非臆测) + 4 条 Minor，建议在 B.2 实现前收敛。

## Major

### M1 — SC-7 的 stderr 提示文案是全局共享 heredoc, `-out=none` 提示会污染所有无关 BLOCKED

`secret-guard.sh:654` 的 `cat >&2 <<EOF ... EOF`（"Acceptable filters" 清单）在
`for pat in risky_patterns` 循环内、对**任意**匹配到的 risky pattern 且 `has_filter=0`
时无条件打印 —— 它不是 nomad-put 专属消息，是全站唯一共享文案（另一处 heredoc 在
`:259` 属 Read/Edit 分支，与此无关）。

proposal「What」第 4 点写的是「既有 heredoc 的『Acceptable filters』清单加
`-out=none # nomad var put: 不渲染 (优于 redirect)`」——字面实现会让**所有**其余
~100 条 risky pattern 的 BLOCKED（`cat .env`、`vault read`、`aws secretsmanager` 等）
也附带这条与它们毫无关系的 nomad 专属提示，稀释而非澄清「Acceptable filters」列表。

这与本 spec 自称的「事故预防核心」（被拦后给出正解，而非制造更多噪音）直接冲突 ——
#170 事故的根因链正是「操作者被拦后无正解可循」，往通用列表塞入语境不相关的 flag
提示是同一失败模式的变体（信息噪音而非缺失, 但同样降低可用性）。

**SC-7 抓不到这个缺陷**：其断言「触发 BLOCKED 时 stderr 文案含 `-out=none` 字样」对
*任意* BLOCKED 命令都会字面为真（因为文案是全局共享的），是一个无差别通过的断言，
不能证明提示只在合适语境出现。

已实测确认该 heredoc 结构（非推演）：
```
$ grep -n "cat >&2 <<EOF" aria/hooks/secret-guard.sh
259:      cat >&2 <<EOF   # Read/Edit branch, unrelated
654:      cat >&2 <<EOF   # shared risky_patterns loop body — THIS one
```

**建议**: 要么把 `-out=none` 提示改成仅在匹配到 `nomad[[:space:]]+var[[:space:]]+put`
时追加的**条件性**附加行（需要在循环体内按 pattern 分支，架构改动略增），要么把
SC-7 改写为断言「非 nomad-put 的 BLOCKED 文案不含 `-out=none`」以显式接受/限定该
trade-off，二选一但不能像现在这样悄悄留白。

### M2 — SC-10 锁定的「已知限制」样例比决策表自己举的例子更弱, 二者不对齐

关键决策表原文（proposal L68）举的残余已知限制例子是:
```
vault read x && nomad var put -out=none y
```
—— 这是**跨 secret-store 家族**的复合命令：一个与 nomad 毫无关系的 `vault read`
借用同一行里 `nomad var put -out=none` 的 credit 而放行。

但 SC-10 实际锁定的是:
```
nomad var get nomad/jobs/a && nomad var put -out=none nomad/jobs/b @f
```
—— 这是**同家族**（都是 `nomad var`）的复合命令，风险直觉上远比跨家族例子温和
（都在同一工具的语境内，不是「借道」一个完全不相关的 secret store）。

已实测确认（在按 proposal 字面实现的忠实副本上）两者都是 exit=0（都会被放行），
且进一步确认**这个 credit-借用问题并非本 spec 引入的新洞**——在完全未改动的现有
`secret-guard.sh` 上，`vault read secret/x && echo bogus >/dev/null` 今天就已经是
exit=0（`>/dev/null` credit 被同一行里毫不相关的 `vault read` 借用）：
```
$ jq -n --arg c 'vault read secret/x && echo bogus >/dev/null' \
  '{tool_name:"Bash",tool_input:{command:$c}}' | bash aria/hooks/secret-guard.sh
exit=0   # 在完全未打这个 spec 补丁的仓库当前 HEAD 上实测
```
所以决策表「这是既有 has_filter 架构对复合命令的通病，不在本 spec 收口」这句话本身
是对的、且已实证——不是新增风险，是既有架构盲区的一个新实例。

但**测试制品 (SC-10) 应该忠实反映决策表自己引用的例子**，否则未来审计者/维护者只读
测试文件会低估残余风险的形态（会误以为「已知限制」局限于「nomad 内部左右手打架」，
而实际是「任何家族的 risky pattern 都能被任何家族的 credit 借用」这一更广泛的架构级
事实）。

**建议**: SC-10 增补（或替换为）决策表原句所举的跨家族例子
`vault read x && nomad var put -out=none y`，使 spec 正文与测试制品互证，而非各说各话。

## Minor

### m1 — SC-1「回归锁」措辞与其实际保护面不符

proposal §Key Deliverables 自己承认「这 6 条正确行为当前零测试锁定」（`:56-59` 现有
用例全为 GET/wget 读向），已用 grep 核实属实——现有测试文件里没有任何 `-X PUT` /
写向 curl 用例。因此 SC-1 的 6 条实为**新增**的 characterization test（把此前隐含但
从未断言的行为首次显式锁定），不是「重新验证一个已有的、已测过的回归」。

更重要的是：本 spec 实际改动（新增 `nomad[[:space:]]+var[[:space:]]+put` pattern +
context-guard 要求同时命中 `nomad var put`）在词法上与「curl 直接打 `/v1/var/`」完全
不相交——没有任何插入的代码路径能让这 6 条 curl 用例的判定结果发生变化。所以 SC-1
结构上无法探测本 spec 引入的任何逻辑 bug，其唯一真实价值是「文件语法/作用域隔离」层面
的冒烟检查（例如新插入的 pattern 行破坏了 bash 数组语法、或 context-guard 的 `if` 块
写挂导致脚本半途退出）——这类风险 SC-8（全量回归 ~50+10 条）本身就已完全覆盖，SC-1
相对 SC-8 是冗余的窄子集。

不影响正确性，纯属测量任务的措辞精度问题：建议要么把 SC-1 重新表述为「作用域隔离
冒烟检查」而非「回归锁」，要么直接归并进 SC-8（作为其子集），避免给未来读者「SC-1
专门保护 curl 写向逻辑」的错误印象。

### m2 — `-out[=[:space:]]+none` 正则对畸形分隔符过度慷慨 credit（非可利用, 仅精度问题）

字符类 `[=[:space:]]+` 把 `=` 与空白视为可互换、可重复的同一类分隔符，导致
`-out= none`（`-out=` 后跟空格再跟独立 token `none`）也会被判定命中 credit：
```
[MISMATCH(want=2)] exit=0 :: -out= none (space after equals, malformed)
```
（已实测；此处 MISMATCH 是我探针的预期错误，不是 hook 的错——但恰恰因为「预期它该被拒」
是符合真实 nomad/getopt 语义直觉的，才值得记录）。真实 nomad CLI 对 `-out=`（空枚举值）
会解析失败并报错退出，不会真正把变量渲染吞掉，`none` 会被当成一个多余的位置参数 ——
所以这个过度慷慨的 credit 授予给的是一个「反正会先被 nomad 自己拒绝、不会真正回显」的
畸形调用，实际不可被利用为绕过路径。仅记录为正则精度层面的技术债，不阻塞发版。

### m3 — rule6_note 借用了「处方性 · AB 测不到」的决策表措辞, 但未走 §3 三件套, 有歧义风险

rule6_note 的结论（Rule #6 不适用, 走「结构性前提不成立」）本身站得住 ——
`secret-guard.sh` 没有 SKILL.md / description / 不参与 skill 触发或加载, Rule #6 的
四个触发条件（新增 Skill / 改逻辑 / 改 description / 发版审计）字面上都不指向一个
纯 hook 文件的改动, 「审计对象」（一个 Skill 制品）在这次 diff 里根本不存在, 而非
「存在但简单」——这精确对应 CLAUDE.md 规则 #10 白名单第四类的定义。

但注释原文写的是「变更对象...内容性质 = **处方性**但作用于 harness 执行层而非 AI 指令面,
AB **结构上测不到**」——这句话借用的正是 `skill-benchmark-exemption.md` §2 决策表
第三行（处方性 + 套件覆盖范围外）的措辞。按该规范 §3 明文, 走第三行**必须同时满足三条**
（点名行为 + 建可证伪定向 fixture + 开套件缺口 issue），「否则会被当成捷径滥用」——
rule6_note 没有走这三条, 直接给出「substitute: SC 级 baseline-failing 结构化测试」。

结论没错（本来就不该走第三行, 该走的是「压根不是 Skill, 规则 #6 字面不触发」这条更
根本的理由）, 但措辞混用会让未来审计者误以为「第三行被悄悄跳过了三件套」。建议把
rule6_note 改写为**优先**陈述「不是 Skill 制品」这一结构性理由, 「处方性/AB 测不到」
的表述整体删除或明确标注为「（附带说明, 非援引决策表第三行）」, 消除歧义。

### m4 — 缺少 `# guard:ack` × `nomad var put` 交互的显式回归用例

已实测确认二者无交互问题：guard:ack 检查在代码顺序上位于 risky_patterns 循环之前
（`:298-316` vs `:648`），对新 pattern 天然生效，且不依赖具体 pattern 内容——
`nomad var put -in=json ... # guard:ack: audited-by-ops-team-2026Q3` 实测 exit=0。
非阻塞项, 纯属测试完整性建议：proposal 「写向测试用例族」10 条里没有一条覆盖
guard:ack 逃生门对新 pattern 的适用性, 虽然机制通用、风险低, 但既然 spec 明确把
guard:ack 列为「缓解手段」之一（Impact 段「既有 # guard:ack: <reason> 逃生门」），
建议补 1 条用例把这个断言留痕，而不是仅靠隐含的架构一致性推定。

## 实测状态空间覆盖（本轮额外验证, 供 owner 参考）

在忠实实现副本上逐条实测，均按预期通过（除 M1/M2/m2 已单独列出者）：

| 探针 | 结果 | 备注 |
|------|------|------|
| `-out=json` / `-out json` / `-out=table` / `-out=go-template` | exit=2 | 未获 credit, 正确 |
| `-out=None`（大写)  | exit=2 | 大小写敏感, 未获 credit（未被 spec 承诺覆盖, 行为保守正确） |
| `-out=none` + `-verbose` 同时出现 | exit=0 | 二者不冲突, `-verbose` 不影响判定, 符合 nomad 语义（`-verbose` 只影响 stderr） |
| `-verbose` 单独出现（无 `-out=none`） | exit=2 | 未获 credit, 正确（默认仍是非-TTY 下 `-out=json` 渲染） |
| `-out=none` 出现在参数末尾（flag 顺序调换） | exit=0 | 正则不依赖位置, 正确 |
| `-out=non`（打字错漏一个字符） | exit=2 | 未误判为 none, 正确 |
| 空 `nomad var put`（无任何参数） | exit=2 | 与既有架构对「命令语法是否完整」不作区分的哲学一致（vault read 等所有 pattern 皆如此), 非本 spec 引入的新问题 |

## 结论

无 Critical。2 条 Major（SC-7 提示污染 / SC-10 与决策表例子不对齐）建议在 B.2 前
收敛为 spec 文本或实现细节的显式修正；4 条 Minor 供参考, 不阻塞。SC-2/SC-3/SC-9 的
核心可证伪性设计已实测验证成立，是本 spec 质量最扎实的部分。
