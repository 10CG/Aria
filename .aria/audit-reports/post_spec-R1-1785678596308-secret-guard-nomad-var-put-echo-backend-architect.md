---
verdict: PASS_WITH_WARNINGS
agent: backend-architect
round: R1
critical_count: 0
major_count: 1
minor_count: 2
---

# post_spec R1 审计报告 — secret-guard-nomad-var-put-echo (正则与实现机制, convergence mode)

## 审计对象

`/home/dev/Aria/openspec/changes/secret-guard-nomad-var-put-echo/proposal.md`（Aria #170 第 3 环修复, Level 2）。视角: 正则语义 + `has_filter` 实现机制。方法: 对 proposal 描述的两条新正则做 POSIX ERE 语义推导，并用 `bash -c '[[ "$s" =~ $pat ]]'` 实测多组输入交叉验证（含一次因命令行字面含 `nomad var get x` 而被真实 secret-guard.sh hook 自我拦截的意外确证 — 证明 `get|list` 既有 pattern 同样无尾部边界，佐证下方 Minor-2 的"非新引入"判断）。已读 `secret-guard.sh` 全文（L318-400 has_filter / L402-646 risky_patterns / L648-690 匹配循环）与 `hooks/tests/secret-guard.test.sh` 形态（未改代码前 grep 确认 `put`/`PUT` 关键字零命中 — proposal 对现状"零覆盖"的描述属实）。

## Major-1: AND 合取的"零架构改动"表述在 Tasks/proposal 无落地代码锚点，file 的主导代码风格是"一条件一 if"，存在被误实现成 OR 的具体路径

proposal 决策表（L68）称 `-out=none` credit "**须同时命中** `nomad var put` **且** 匹配 `-out[=[:space:]]+none`"，"守卫实现零架构改动 (仍是一条 has_filter 赋值, 只是条件为两串合取)"。这段文字本身语义正确、无歧义。

但 `secret-guard.sh` L318-400 现有 **全部 ~14 条 has_filter 赋值都是"单条件独立 if"**（jq/grep/sed/cut/awk/`>/dev/null`/`-o /dev/null`/wc/hash 各自一个 `if ... has_filter=1; fi`，互相之间语义上是 OR 叠加）。Phase B 实现者若照抄这一主导风格，最自然的写法是：

```bash
# 危险写法 A（两个独立 if = OR，不是 spec 要的 AND）
if echo "$command" | grep -qE 'nomad[[:space:]]+var[[:space:]]+put'; then has_filter=1; fi   # 荒谬但示意误实现风险点
if echo "$command" | grep -qE -- '-out[=[:space:]]+none'; then has_filter=1; fi
```

若第二个 if 独立存在（不嵌套在第一个 if 内，也不用 `&&` 合取），`-out=none` 就退化成 proposal L45 明确警告要防的"通用绕过词"——`vault read secret/x -out=none` 会被误 credit exit=0，正是 SC-9 存在的理由，也正是本 spec 的核心风险点自我复刻。

**已验证不受影响的部分**：has_filter 区块本身是无分支的线性顺序执行（L323→L400 每条都是顶层 if，无 early return/exit），所以到达 L401 循环入口时所有既有 credit 路径确定已算完——这部分问题询问的"执行顺序"本身没有结构性风险，风险点是"合取 vs 独立赋值"这个逻辑运算符层面，不是求值顺序层面。

**建议**：在 tasks.md 1.1 里显式写出（哪怕是伪代码级）"`if [[ 匹配 nomad-var-put ]] && [[ 匹配 -out=none ]]; then has_filter=1; fi` 单条件复合判断，禁止拆两个独立 if"，把 SC-9 从"实现完之后才能测出的事后闸"前移成"写代码时就避免"的显式约束。此风险不改变 proposal 结论本身的正确性，故不判 Critical。

## Minor-1: `-out[=[:space:]]+none` 缺尾部边界，`-out=none-such` / `-out=nonelegit` 会误配（实测确认）

```
MATCH: -out=none-such
MATCH: -out=nonelegit
no-match: -outfile=none   （前缀不同，不受影响）
```

`[=[:space:]]` 括号表达式对 `=` 与 `[:space:]` 类的合取写法本身合法且行为符合预期（`-out=none` / `-out none` / `-out  none` 三种写法均正确覆盖，SC-4 可达成）。缺陷仅在于正则末尾无 `\bnone\b` 或 `(none)([[:space:]]|$)` 类边界，导致以 "none" 为前缀的任意后续字符串都会被当作合法值触发 credit。

**实际风险评级为 Minor 而非 Major**：nomad `-out` flag 的合法枚举是 `go-template|hcl|json|none|table`（proposal L18 引用的 CLI 文档），没有以 "none" 为前缀的其他合法值；`-out=none-such` 这类输入若真的传给 nomad，会被 nomad 自身的 flag 解析拒绝（非法枚举值 → usage error → 不执行 put → 不渲染 secret），所以即便 hook 误 credit，最终也不会真的泄漏。但这属于"运气好没被下游兜底"式的正确性，不属于 hook 自身的精确匹配——若未来 nomad CLI 新增 `-out=none2`/`-out=noneable` 之类枚举值（当前不存在，纯假设），或该正则被复制粘贴到别处语境，问题会现形。建议收紧为 `-out[=[:space:]]+none([[:space:]]|$)` 或加 `\b`。

## Minor-2: `nomad[[:space:]]+var[[:space:]]+put` 缺尾部边界，`nomad var putty` 之类会误配 —— 但这是与既有 `(get|list)` 同源的既有惯例，非本 spec 新引入的退化

```
MATCH: [nomad var put path k=v]     — 正确
MATCH: [nomad var putty x]          — 缺边界导致的假想误配
no-match: [nomad-var-put x]         — 连字符形态不匹配，符合预期（无风险）
no-match: [NOMAD VAR PUT x]         — 大小写敏感，[[ =~ ]] 默认行为，文件全局未设 nocasematch
MATCH: [echo nomad var put]         — 无行首锚定，子串任意位置命中，与全文风格一致
```

`nomad var putty`（假设存在的子命令，实际 nomad CLI 没有）会被 pattern 命中。但这个"缺尾部边界"的弱点是 **`risky_patterns` 数组里几乎所有 CLI-subcommand 类 pattern 的共性**（本次审计过程中，我自己的一条纯文本测试命令 `"nomad var getter x" ... "nomad var listing x"` 因字面包含 `nomad var get x`/子串触发了 secret-guard.sh 的真实 PreToolUse hook 直接拦截我自己的 Bash 调用——这条实证恰好说明既有 `(get|list)` pattern 同样无尾部边界，是同一族已知限制）。大小写敏感、无行首锚定同理是全文既有约定（其余 ~99 条 pattern 全部如此）。

判定：这条不是本 spec 引入的新退化，是继承既有 pattern-family 惯例，评 Minor 仅为记录在案，不构成本 spec 应改的范围（若要收紧，应作为独立的"全体 pattern 加尾部边界"重构议题，不宜掺进本次 3 处最小变更）。

## 交叠 / 遮蔽核对（无发现）

- 与既有 `nomad[[:space:]]+var[[:space:]]+(get|list)` (L406)：`put` 与 `(get|list)` 互斥字面量，不会同一子串被两条 pattern 重复命中导致行为歧义（即便双中也无害——循环对 `has_filter=1` 的命中不阻断，仅顺序决定第一条命中 pattern 的错误提示文案，无功能性冲突）。
- 与 `curl[^|]*/v1/var/` (L404) / `/v1/var/` (L405) / `nomad[[:space:]]+operator[[:space:]]+api[^|]*/var/` (L408)：语法层完全不同（CLI subcommand vs URL path），`nomad var put <path> k=v` 不含 `/v1/var/` 字面子串，不会误触发这三条。
- `-out=none` 不会被既有任何 filter-credit 正则误吞或误漏：已核对 jq/grep/sed/cut/awk（均要求前导 `\|[[:space:]]*`，`-out=none` 非管道后内容不适用）、`([^0-9&]|^)>[[:space:]]*/dev/null`（要求字面 `>`，`-out=none` 无 `>`）、`-o[[:space:]]+/dev/null`（要求 `-o` 后接空白，`-out=none` 的 `-o` 后接 `ut=none`，`u` 非空白，不匹配）——实测确认无交叉命中，这条 credit 确实是全新覆盖面，不是重复劳动。

## BLOCKED heredoc 文案增补：无 shell 转义风险

L654-682 的 heredoc 是 `cat >&2 <<EOF ... EOF`（未加引号的分隔符），会对 `$` 和反引号做替换（既有文本里 `$command` 就是刻意利用这点）。proposal L55 拟增的文案 `-out=none  # nomad var put: 不渲染 (优于 redirect)` 不含 `$`、反引号、`` ` ``，`#` 在 heredoc body 里只是普通字符（heredoc 不解析 shell 注释语法，仅做变量/命令替换），中文字符与括号也无特殊语义。确认零转义风险。

## 总结

规则设计（pattern 语义、has_filter 求值顺序、语境守卫必要性、pattern 交叠面）方向正确、无 Critical 缺陷。主要风险是"合取"这个设计意图在从 proposal 文字落到 Tasks/代码时，有被主导代码风格带偏成"两个独立 if"的具体路径（Major-1），建议 tasks.md 补一句显式约束；另两处尾部边界宽松（Minor-1/2）在当前 nomad CLI 语义下不构成实际可利用泄漏，可选择性收紧或留作已知限制显式记录（呼应 proposal 自身 SC-10 的做法）。
