---
seat: A1-backend-architect
round: R2-final
checkpoint: post_spec
spec: secret-guard-manifest-precision
verdict: PASS
critical_count: 0
major_count: 0
minor_count: 0
timestamp: 2026-08-22T11:00:00Z
r1_verdict: REVISE
r1_critical_count: 1
r1_major_count: 2
r1_minor_count: 2
r2_verdict: REVISE
r2_critical_count: 0
r2_major_count: 2
r2_minor_count: 0
---

# post_spec R1 审计报告 — A1 backend-architect

审计对象: `/home/dev/Aria/openspec/changes/secret-guard-manifest-precision/proposal.md` (Aria#179)
基线: aria @ `400f0bc`（真代码实读 + 实跑核验，非仅读 spec 文本）

## 摘要

透镜聚焦「机制/架构」。核心发现: **spec 自己在 Out-of-scope 里承认的 credit 系统已知面，对 claude-config 这一新增拦截目标的危险程度被系统性低估** — 用 `.env` 类比来论证「非本 spec 引入 / 不扩权治理」的类比在事实上不成立，因为 `.env` 不是合法 JSON，而 `~/.claude/settings.json` 是。这是本次最重要的发现（[A1-C1]），已用真实命令跑通验证，不是推测。另有两条 Major：`python3?` 并入既有泛化 reader 组的误报面被低估（与代码里已有的窄化先例矛盾）、前置字符类的最简实现方式在结构上可能与既有 `[[:space:]]+` 强制分隔条件冲突，存在使 SC-5 守卫用例失配的具体路径（已用规则推演定位，非猜测）。

---

## Findings

### [A1-C1] Critical — credit 系统对 claude-config 的「字段白名单」漏洞比 spec 认定的更危险，直接可一步绕开本 spec 的核心修复

**锚点**: proposal.md `## Out of scope` 第一条 + `## Success Criteria` SC-3；代码 `aria/hooks/secret-guard.sh:335-339`（jq `{...}` 形状即给 credit，不校验字段名）+ `:926-973`（`_sg_judge_one`，credit 只计算一次、整段判定）+ `:217-223`（segment 切分明确不切 `|`）。

**问题**: `_sg_compute_credit` 的 jq 规则（:337）只要求 `\|[[:space:]]*jq(...)?[[:space:]]*\{`，即「jq 前有管道 + jq 后紧跟 `{`」就给 `has_filter=1`，**完全不检查大括号里选的字段名是否安全**。而 secret-guard 对管道命令不做 `|` 切分（:217-223 注释明确写「Does NOT split on: |」），所以 `cat ~/.claude/settings.json | jq '{env: .env}'` 是单一 segment，一旦命中新增的 claude-config risky pattern，credit 计算就会命中 :337 的形状规则拿到 `has_filter=1` → **放行**，而这条命令原样把 `env` 整个子树（issue 里明确指出的 token 存放位置）吐出来 —— 这正是 SC-1 要堵的那个真实泄露，只是绕了一步管道。

**已实测验证**（用 `.bashrc` 做等价代理，因为 claude-config pattern 尚未实现；shell-rc 面同样是「reader + credit」结构，credit 逻辑与目标 pattern 共用同一份 `_sg_compute_credit`，故可外推）:

```
$ echo '{"tool_name":"Bash","tool_input":{"command":"cat ~/.bashrc"}}' | bash secret-guard.sh
BLOCKED ... exit 2          # 控制组: 光读 shell-rc 仍拦, credit 逻辑未被误触发

$ echo '{"tool_name":"Bash","tool_input":{"command":"cat ~/.bashrc | jq '\''{env: .env}'\''"}}' | bash secret-guard.sh
(no output) exit 0          # 同一份 credit 逻辑: 加一节 "| jq '{...}'" 立即放行
```

**Out-of-scope 论证为什么站不住**: spec 写「`cat settings.json | jq '{env: .env}'` … 对 .env 类同样成立, 非本 spec 引入」。这个类比在**正则形状**上成立, 但在**可利用性**上不成立: `.env` 是 `KEY=VALUE` 纯文本, 不是合法 JSON, `cat .env | jq '{...}'` 在真实 shell 里会因 JSON 解析失败而报错、拿不到任何数据 — 这条 credit 逃逸路径对 `.env` 基本是死路, 从未被真正用来泄露过。而 `~/.claude/settings.json` **就是**合法 JSON, 且字面就有一个叫 `env` 的键（issue 原文: 「`env` 节点是 Claude Code 存放 API token 的标准位置」）—— 对 claude-config, 这条路径不是「已知但边缘」的理论缺口, 而是**恰好命中本 spec 要修的那个泄露场景本身**, 攻击/误用成本是「在 SC-1 的直连命令前面加 `cat file |`」。把两者并列为「同等已知面, 不扩权治理」低估了后者的严重度。

**建议**: 不需要动 credit 系统的通用语义（spec 保留 Out-of-scope 的克制方向是对的），但至少要在 SC-3/SC-5 里补一条**反事实断言**: `cat ~/.claude/settings.json | jq '{env: .env}'`（或字段名含 `env`/`mcpServers` 等已知敏感字段的 `{...}` 投影）期望值是多少 —— 如果期望仍是「credit 放行, out of scope」, 必须把 Out-of-scope 的论证文字改掉（不能再用「与 .env 同等」这个不成立的类比）, 显式写清楚「已知且已验证对 claude-config 更危险, owner 仍选择不治理」, 让复议链有据可查; 如果期望是「应拦」, 就需要一个**限定在 claude-config 路径上**的字段名黑名单（不触碰全局 credit 语义, 只对 `.claude/settings*.json`/`.claude.json` 追加一条: `{...}` 投影里出现 `env`/`mcpServers`/`apiKey` 等键名不给 credit）, 相应补 SC-3 fixture。两种选择都行, 但当前 spec 文本里的论证依据是错的, 必须先纠正再走 B.2。

---

### [A1-M1] Major — What.1「reader 组 = 既有 11 reader + jq + python3?」把两种不同风险形状的 reader 混进同一个泛化 alternation, python3 的误报面被低估

**锚点**: proposal.md `## What Changes` 第 1 条；代码 `:709`（既有泛化 reader 组 `(cat|grep|egrep|fgrep|rg|head|tail|less|more|strings|awk|sed)[[:space:]]+[^|]*(名字)`）vs `:785`（既有 python3 专用窄化 pattern `python3?[[:space:]]+-c[^|]*(内容组)`）。

`:709` 这种「reader + `[^|]*` + 名字」的泛化结构, 对 `cat`/`grep`/`jq` 这类「参数基本就是文件名/短 flag」的命令风险可控 —— `[^|]*` 吞掉的中间内容一般很短。但 `python3` 不是这种形状: 真实用法是 `python3 -c '<一整段脚本文本>'`, 脚本文本里可以有任意长度的字符串字面量、注释、docstring, 只要文本里出现 `settings.json`/`.claude.json` 字样（哪怕只是在打印一句日志、写一段注释、拼一个不相关路径）就会被泛化 alternation 命中 —— 这正是 spec 自己在 What.3 里点名并明确声明「不在本 spec 治」的「prose 位置误报」那一类, 但 What.1 字面写法（python3? 并入 :709 式泛化组）等于在**同一个 spec 里新开一个日后必现的同类误报口子**, 而不是延续现有对 python3 的处理先例。

代码里其实已经有先例说明这个区分是有意为之: `:785` 的既有 python3 pattern **要求显式 `-c` 标志**, 且内容匹配组比 `:709` 窄得多（只匹配几个具体高危字符串, 不是任意 `[^|]*`）。这不是巧合 —— 是此前审计轮已经识别过「interpreter 类 reader 参数面太宽」而做的收窄。What.1 如果照字面「并入既有 reader 组」实现, 相当于绕开了这条已有的设计先例。

**建议**: `jq` 按 What.1 原样并入 `:709` 泛化组没问题（jq 的参数形状接近 `cat`, 风险可控, 已实测确认目前不在组内）。`python3?` 建议不并入 `:709`, 改为比照 `:785` 的窄化结构（要求 `-c`/`-m` 等标志, 或者要求文件名以命令行「最后一个非 flag 位置参数」出现, 而不是「命令行任意位置的文本」）单独成一条 pattern。至少 SC-1 里 `python3 -c ... ~/.claude.json` 这条 fixture 应该连带写一条**反向探针**: `python3 -c "print('note: see .claude.json for config docs')"` 之类的纯 prose 文本必须验证不误伤, 现在的 SC 列表里没有这条。

---

### [A1-M2] Major（有流程兜底, 非阻断）— 前置字符类若按最直白方式实现, 可能与既有 `[[:space:]]+` 强制分隔冲突, 存在使 `cat .bashrc`（SC-5 守卫用例本身）失配的路径

**锚点**: proposal.md `## What Changes` 第 3 条 + `## Success Criteria` SC-5；代码 `_sg_line_match` (`:82-88`, 纯 `[[ =~ ]]` 逐行匹配, ERE 无 lookbehind) + `:709` 既有结构 `(reader)[[:space:]]+[^|]*(名字)`。

spec 描述的前置字符类是「敏感名**前一字符** ∈ {行首,空白,",',=,/,~}」——即紧邻在名字字面量前的单个字符必须来自这个集合。ERE 没有 lookbehind, 唯一可行做法是把这个约束显式写成正则里的一个字符组, 直接放在名字组前面。如果实现时只是简单地在既有 `(reader)[[:space:]]+[^|]*(名字)` 结构里, 在 `[^|]*` 和 `(名字)` 之间**追加**一个前置字符类要求（而不是替换掉 `[[:space:]]+` 这个已有约束）, 对 `cat .bashrc` 这种「reader 和名字之间只有一个空格」的最短形态会出问题: `[[:space:]]+` 要求至少吃 1 个空白字符满足「reader 后必须有空白」这个既有约束, 而新增的前置字符类又要求名字前必须紧跟 1 个来自集合的字符 —— 两个子表达式都要「消费」同一个位置只有 1 个字符的空白, ERE 引擎在整串只有一个空格字符可用时无法把它同时分给两处不同的子表达式（该字符要么被 `[[:space:]]+` 吃掉、要么被前置字符类吃掉，不能两边都算），会导致 `cat .bashrc` 这种单空格形态在新正则下**匹配不上**, 而这恰好是 SC-5「既有真实读取形态必须仍拦」明确点名的反事实关键用例。

这不是臆测的边角情况 —— `cat .bashrc`/`cat X.env` 这类「reader+单空格+文件名」是最常见的真实调用形态, 一旦这样实现基本必现。

spec 在 What.3 已经提醒了 `_sg_line_match` 的两个已知 ERE 坑（`\b` 不可用、`^` 不锚每行), 但没有提到这第三个坑（字符消费冲突）。

**为什么不是 Critical**: Tasks 1.3 明确要求「先写 SC-5 守卫再动 pattern」, 也就是 TDD 红绿流程会在 B.2 第一次跑测试时就把这个问题炸出来（SC-5 变红）, 不会带着这个缺陷流入交付。但既然 spec 已经花了篇幅提醒两个已知 ERE 坑, 建议把这第三个坑也写进去（连带一句「前置字符类应替换而非叠加既有 `[[:space:]]+` 约束, 例如把整体结构改写为 `(reader)[^|]*[[:space:]"'=/~](名字)`, 让 reader 后的那个空白本身也能充当前置字符, 不要求额外消耗第二个字符」）, 省一轮 B.2 返工。

---

### [A1-m1] Minor — What.1「既有 11 reader」计数有误, 实际是 12 个

**锚点**: proposal.md `## What Changes` 第 1 条「reader 组 = 既有 11 reader」；代码 `:709`。

实读 `:709` 的 reader alternation: `cat|grep|egrep|fgrep|rg|head|tail|less|more|strings|awk|sed` —— 逐个数是 12 个（cat/grep/egrep/fgrep/rg/head/tail/less/more/strings/awk/sed）, 不是 11 个。不影响修复方向, 但 spec 里的事实断言应该核对准 —— 尤其这类计数后续常被 `standards/conventions/secret-hygiene.md` 之类的文档回填引用（Task 1.5 提到「计数回填」), 起点数错会顺着传递下去。

---

### [A1-m2] Minor / 信息性 — 第三平面排查: 未发现第二份路径清单, 但 secret-scan.sh 是结构不同的正交防线, 对本 spec 目标凭据的兜底能力未知

**锚点**: `aria/hooks/secret-scan.sh` 全文（377 行) + `aria/hooks/*.sh` 目录扫描。

排查确认: `aria/hooks/` 下除 `secret-guard.sh` 外, 只有 `secret-scan.sh` 涉及敏感内容, 且是 **PostToolUse 内容形状检测**（正则匹配 JWT / `sk-ant-*` / 高熵字符串等**值的形状**, 见 `:147-236`), 不是像 secret-guard 那样按**文件路径清单**拦截 —— 结构上不是「第二份需要同步的清单」, 这条 spec 判断准确, 没有遗漏第三平面。

但作为信息性备注: issue 里说的 token 是「各类 `*_API_TOKEN`」内网服务令牌, 这类内部自定义格式的 token 大概率不匹配 secret-scan.sh 已收录的已知厂商 shape（Anthropic/OpenAI/JWT 等), 也就是说如果 SC-1/SC-2 的 PreToolUse 拦截万一被绕过（比如上面 [A1-C1] 那条路径), PostToolUse 这层大概率也接不住, 两层防线在这个具体凭据类型上不构成真正的纵深防御。不要求本 spec 处理（超出范围), 但建议记入 `#138` 或另开 issue, 别让「有两层防线」造成误判安全边界的错觉。

---

## 事实断言抽查核验表

| # | 断言 | 核验方式 | 结果 |
|---|---|---|---|
| 1 | `:709` shell-rc reader 列表不含 `jq` | 读 `secret-guard.sh:709` | 属实 |
| 2 | spec 称「既有 11 reader」 | 逐个计数 `:709` alternation | **不属实, 实际 12 个**（见 [A1-m1]） |
| 3 | `:546` Read/Edit 面正则同样无 claude 配置文件条目 | 读 `secret-guard.sh:546` | 属实 |
| 4 | `jq '{alias: .safe_field}'` 形状本身即获 credit, 不校验字段名安全性 | 读 `_sg_compute_credit` `:335-339` + 实跑 `cat ~/.bashrc \| jq '{env: .env}'` → exit 0 | 属实（已实测） |
| 5 | spec 称该 credit 逃逸「对 .env 同样成立」故不扩权治理 | 类比分析: `.env` 非 JSON, jq 解析会失败, 逃逸路径在 `.env` 上不可利用; 对 claude-config（合法 JSON 且字面含 `env` 键）则直接可利用 | **类比不成立, 危险度不对称**（见 [A1-C1]） |
| 6 | `_sg_line_match` 基于 `[[ =~ ]]` 逐行匹配, ERE 无 lookbehind | 读 `:82-88` | 属实, 支撑 [A1-M2] 的实现路径分析 |
| 7 | python3 既有唯一模式（`:785`）要求显式 `-c` 标志且内容匹配组比 `:709` 窄 | 对比读 `:709` 与 `:785` | 属实, 支撑 [A1-M1] |
| 8 | Bash/Read-Edit 走 `case "$tool"` 分流（`:536`）, 两平面代码路径独立 | 读 `:536-604` | 属实 |
| 9 | 命令按 `;`/`&&`/`\|\|` 切 segment, **不切 `\|`**（管道内是同一 segment） | 读 `:217-223` 注释 + `_sg_judge_one` 对整 segment 一次性算 credit（`:929-933`） | 属实, 是 [A1-C1] 可利用的结构性前提 |
| 10 | `aria/hooks/` 下无第二份「路径清单」型 manifest（除 secret-guard.sh 自身） | `grep -rln settings.json aria/hooks/*.sh` 全空; `secret-scan.sh` 是内容形状检测非路径清单 | 属实 |

---

## Verdict

**REVISE** — Critical=1（[A1-C1]），Major=2（[A1-M1]/[A1-M2]），触发「任一 Critical 或 ≥2 Major → REVISE」判据双重命中。

核心诉求: (1) 修正/补齐 Out-of-scope 关于 credit-`.env`-类比的论证, 显式对 claude-config 的 `jq '{...含 env 类字段}'` 管道逃逸给出**有据**的期望值（拦或放行都行, 但不能继续用不成立的类比当理由）; (2) What.1 里 `python3?` 的并入方式改用既有窄化先例, 并补一条 prose-only 反向 fixture; (3) What.3 的 ERE 实现提醒里补上「前置字符类应替换而非叠加 `[[:space:]]+`」这一条, 避免 B.2 返工。

---

## R2 (v2) 复核

复核对象: proposal.md v2（`## Status` 已标 v2, R1 三席 findings 去重处置表见 `.aria/audit-reports/post_spec-R1-1787375602111-secret-guard-manifest-precision-aggregated.md`）。本节逐条回答 Q1（v2 落地是否忠实于 R1 处置表所写的方向）+ Q2（我 R1 原处方本身是否站得住）, 再用架构透镜单独审 v2 新文本自身（What.1b 的段级 credit 收紧在真实控制流里能不能落地、SC-3 新断言表与 What.1b 语义是否一致）。

### [A1-C1] credit 逃逸

- **Q1 忠实吗**: 忠实。What.1b（proposal.md:29）逐句对应 R1 的诊断（形状判定不查字段名 / `.env` 类比不成立的理由原样保留）, 并采纳了我 R1 给的两个选项之一（选项 b: claude-config 作用域字段黑名单, 而非只改论证文字）。Out-of-scope 里 v1 的错误论证已被明确划掉（`~~credit 系统语义不动~~`), 通用面维持不动的边界也写清楚了。SC-3（proposal.md:56）把 `jq '{env: .env}'` → 2 列为 baseline-failing 核心断言, 并保留 `.env` 源同款命令 → 不变的对照组 —— 这正是我 R1 要求的「反事实断言 + 类比不能再站不住脚」。
- **Q2 我原判对不对**: 对。诊断（形状判定不查字段名, `.env`/claude-config 危险度不对称）和处方（两个选项）都被后续证明成立且可执行, 没有需要推翻的地方。
- **结论**: R1 [A1-C1] 视为已解决, 但解决方式本身在真实控制流里能否落地是一个新问题 —— 见下方 [A1-R2-1]（新 finding, 非对 R1 结论的推翻, 是对 v2 新增实现指令的独立审查）。

### [A1-M1] python3 并入方式

- **Q1 忠实吗**: 忠实。What.1（proposal.md:27）明确「python3/node 不并入」既有泛化 reader 组, 改为扩展 `:785`/`:786` 既有窄先例（`python3? -c` / `node -e` + 源组, 追加三条 claude-config 字面量）—— 与我 R1 建议的「沿用窄化先例, 不并入泛化组」完全一致, 且比我原建议更干净（我原来还给了「要求 `-c` 或定位到最后一个非 flag 位置参数」两个方向, v2 直接选了最简单、风险最低的「复用已有 `-c` 结构」, 不引入新形状）。
- **Q2 我原判对不对**: 对, 且 v2 采纳的实现路径比我给的两个选项里更保守的那个还稳（不新造正则形状, 只扩展既有内容组）。
- **附带核查**: 我 R1 建议补一条 prose-only 反向 fixture（`python3 -c "print('note: see .claude.json ...')"` 不应误拦）。v2 没有单独列这条 SC fixture, 但 What.3 的范围边界 (a)「prose 位置完整路径文本… 不治, 走 `# guard:ack:`」已经把这类残余显式声明为**沿用既有已知限**（`:785` 结构本来就有这个残余, 不是这次新引入的), 不是被遗漏, 是合并进了已声明的边界里。判定: 忠实, 不需要单独追加。
- **结论**: R1 [A1-M1] 已解决, 无新增问题。

### [A1-M2] 前置字符类 / `[[:space:]]+` 争用

- **Q1 忠实吗**: 忠实。What.3 新增「ERE 陷阱点名 (R1 A1-M2)」条目（proposal.md:37）逐句复述了我 R1 给出的机制（白名单类与既有 `[[:space:]]+[^|]*` 争用空白字符, `cat .bashrc` 单空格裸文件名形态structurally 失配), 并把它升格为 SC-5 的显式必测 fixture（proposal.md:58: 「`cat .bashrc`（单空格裸文件名, R1 A1-M2 争用形态）」)、外加 Task 1.3 顺序约束「先写 SC-5 守卫再动 pattern」。这正是我 R1 建议的「至少要点名 + 用测试兜底」, 采纳完整。v2 没有像我在 R1 报告里那样给出具体的正则改写建议（把 `[^|]*` 和前置字符类合并、复用同一个空白字符), 这是合理的取舍 —— Minimal 级 spec 不该把具体正则写进 proposal.md, TDD 顺序本身就能在 B.2 第一次跑测试时暴露问题, 不需要 spec 越俎代庖。
- **需要在 Q2 里主动纠正的一处不准**: 我 R1 报告把 ERE-无-lookbehind 这个事实锚定在 `_sg_line_match`（:82-88）身上。这次复核 v2 时连带重读了控制流才发现: `risky_patterns` 的实际匹配路径是 `_sg_judge_one` 里的裸 `[[ "$seg" =~ $pat ]]`（:930), **不经过** `_sg_line_match`（这是 A2-C1 在 R1 独立指出的, 已体现在 v2 What.3「实现路径语义」条目, proposal.md:36）。我 R1 引用 `_sg_line_match` 只是用它举例证明「这套 hook 用的正是无 lookbehind 的 bash ERE」, 不是声称 risky_patterns 匹配经过它 —— 但原文写法容易让人误读成后者, 是我 R1 报告的一处引用不够精确, 在此更正: 结论（字符消费冲突会导致 `cat .bashrc` 失配）不受影响（两条路径底层是同一个 ERE 引擎, 冲突机制一样), 但佐证引用应该是 `:930` 的直接匹配, 不是 `:82-88`。
- **结论**: R1 [A1-M2] 已解决（诊断成立, 处置方式合理), 引用锚点在此勘正。

### [A1-m1] 「既有 11 reader」计数

- **Q1 忠实吗**: 忠实。Why 表格（proposal.md:20）与 What.1（proposal.md:27）均已改为「12 个 reader」。连带 R3 席指出的 `:546` 计数（17→29）也一并勘正（proposal.md:21: 「29 个分支」), 我已重新逐项数过 `:546` 的顶层 `|` 分支, 确认 29 属实。
- **Q2 我原判对不对**: 对, 且这次连带验证了另一席（A3）的计数勘正也准确。
- **结论**: 已解决。

### [A1-m2] secret-scan.sh 第三平面排查

- **Q1 忠实吗**: 忠实（且正确）。这条本来就是「不需要动作」的信息性备注（我 R1 原文即写「不要求本 spec 处理」), 聚合处置表第 10 行明确标「不动作」, v2 正文也没有新增/修改与 secret-scan.sh 相关的条目 —— 符合处置预期本身就是「保持不变」。
- **Q2 我原判对不对**: 对。
- **结论**: 无需 v2 动作, 已确认无遗漏。

---

### 架构透镜: v2 新文本自身审查

#### [A1-R2-1] Major — What.1b「段内命中 claude-config 源时跳过 `:337` 形状分支」在真实控制流里缺一个「源判定」信息通道, 且未覆盖混合来源 segment 的顺序依赖

**锚点**: proposal.md What.1b（:29）「实现按段判定: 段内命中 claude-config 源时跳过 `:337` 形状分支」；代码 `_sg_judge_one`（`:926-933`）+ `_sg_compute_credit`（`:306-392`, 尤其 `:337`）。

**控制流实测重读**（回答协调者的具体问题「源命中判定在哪个变量可得」）:

```
for pat in "${risky_patterns[@]}"; do
    if [[ "$seg" =~ $pat ]]; then
      if [[ -z "$credit" ]]; then
        if _sg_compute_credit "$seg"; then credit=1; else credit=0; fi
      fi
      ...
```

`_sg_compute_credit` 的形参只有 `$seg`（`:306`: `local seg="$1"`)。哪一条 `risky_patterns` 命中触发了这次判定（即 `$pat`）**只存在于 `_sg_judge_one` 的局部作用域, 从未传给 `_sg_compute_credit`**。所以「段内命中 claude-config 源」这个判据, 目前代码里**没有现成变量可读** —— 必须新增信息通道, 有两条路:

- (a) 改调用点签名, 把 `$pat`（或从 `$pat` 派生的「源类别」标记）传给 `_sg_compute_credit`, 让 `:337` 分支按「触发本次 credit 计算的那条 pattern 是不是 claude-config 条目」来决定要不要跳过。
- (b) `_sg_compute_credit` 内部独立地对 `$seg` 重新跑一次 claude-config 字面量识别（例如 `_sg_line_match "\.claude/settings\.json|\.claude/settings\.local\.json|\.claude\.json" "$seg"`), 不依赖调用点传入什么, 直接自己判「这段文本里有没有 claude-config 路径字面量」。

**两条路的取舍, spec 没写, 但差别是真实的**:

(a) 路径依赖「credit 只按第一个命中的 pattern 算一次, 之后 memoize 复用」这个既有结构（`:931` `if [[ -z "$credit" ]]`）—— 如果一个 segment 同时含 claude-config 字面量和其他源字面量（例如 `cat ~/.claude/settings.json ~/.env | jq '{env: .env}'`, 一条命令读了两个文件), risky_patterns 数组里**先命中哪一条**（数组书写顺序, 不是语义优先级）就决定了 credit 用哪套规则算 —— 如果 `.env` 相关 pattern 排在 claude-config pattern 前面, 这个 memoize 机制会用「.env 源」的（未收紧）credit 规则算出 `credit=1`, 然后这个已经算好的值会被复用到后面 claude-config pattern 命中时的判定上, **绕开刚收紧的 :337 跳过逻辑** —— 相当于给 What.1b 自己开了一个「加一个陪读文件」就能重新拿到 credit 的旁路, 而这个旁路恰好和 [A1-C1] 是同一形状的问题, 只是从「单一 claude-config 源」换成了「混合源」。

- (b) 路径不依赖命中顺序 —— 只要 `$seg` 文本里出现 claude-config 字面量（无论是不是本次触发匹配的那条 pattern), 就统一关掉 `:337` 分支, 天然规避上面的顺序依赖, **是更安全、也更符合「段内命中 claude-config 源」这句话字面意思的实现**。代价是: claude-config 的三个字面量集合会同时存在于 `risky_patterns` 数组（检测用）和 credit 函数内部（收紧用）两处, 后续如果这个字面量集合变动（比如以后加第四个 claude 配置文件路径), 两处必须同步改, 没有机制强制保持一致 —— 是可控的维护成本, 不是设计缺陷, 但 spec 没提示, 容易在 B.2 漏改一处。

**建议**: 在 Task 1.1 或 What.1b 里明确指定走 (b) 路（段内独立重识别, 不依赖命中顺序), 并加一句提示「claude-config 字面量集合需要在检测用 pattern 与 credit 收紧判据两处保持同步, 或提炼成共享变量避免两地硬编码漂移」; SC-3 补一条混合源 fixture 锁定顺序无关行为, 例如 `cat ~/.claude/settings.json ~/.env | jq '{env: .env}'` → 2（不能因为数组里先命中 `.env` 相关 pattern 就漏判）。

**严重度**: Major, 非 Critical —— 触发条件比 [A1-C1] 更窄（需要操作者/agent 主动构造「同一条命令里混读 claude-config + 别的敏感源」这种不算自然的组合), 但一旦触发, 后果和 [A1-C1] 同级（整段泄露 env）, 且当前 v2 文本和 SC-3 都没有覆盖这个分支, 不是「TDD 会自动测出来」的那类问题（因为 SC-3 现有 fixture 全是单一来源, 不会意外撞上这条路径依赖）。

#### [A1-R2-2] Major — What.1b「有效 credit **仅**: 名字面类/计数/哈希/丢弃」的「仅」字面读法, 与既有 grep 锚点/sed s×/cut/awk `$N` 等真过滤 credit 规则的关系没写清楚, SC-3 未消歧

**锚点**: proposal.md What.1b（:29）「有效 credit 仅: 名字面类 (`jq 'keys'`/`length`/`paths`), 计数 (`wc`), 哈希 (`sha*sum`), 丢弃 (`>/dev/null` 族)」；代码 `_sg_compute_credit` 里另外还有 `:348-367` 的 grep 锚点 / grep -v / sed s×或d / cut -d/-f / awk `$N` 等「已校验为真过滤」的 credit 分支, What.1b 的「仅」枚举里完全没提这几条。

**问题**: 这句话字面上是「有效 credit **仅**这四类」, 如果按字面实现, 意味着对 claude-config 源, 像 `cat ~/.claude/settings.json | grep '^model='`（锚点 grep, 真实按行过滤, 不是形状判定漏洞, 语义上和 `.env` 场景的 `grep '^SAFE_PREFIX='` 是一回事）这种货真价实的过滤命令也会被新收紧逻辑连带堵死 —— 但 What.1b 的问题陈述通篇只讲「`jq '{...}'` 形状判定不查字段名」这一个逃逸口, 从没论证过 grep 锚点/sed s×/cut/awk 这几条也需要收紧（它们本来就要求「真的做了字段级过滤」, 不是纯形状判定, 不存在 `:337` 那种「只看语法形状不看内容」的漏洞）。SC-3（:56）目前只写了 `keys`/`wc`/`>/dev/null`/直读四种断言, 没有任何一条 fixture 去验证 grep 锚点这类既有真过滤规则对 claude-config 源到底是「仍然有效」还是「被 What.1b 的『仅』字面收紧掉了」—— 两种读法都能自洽地通过现有 SC-3, 是真实的歧义, 不是我过度解读。

**为什么这个歧义值得在 ship 前定死**: 如果 B.2 实现者按「仅」字面理解（四类之外全部收紧), 会制造一批**新的假阳性**（真实按字段过滤的 grep/sed/awk 命令被误拦), 而这既不在 SC-1..SC-7 任何一条要求里, 也不是 issue #179 要修的问题, 属于无意中扩大了行为变更面; 如果按「仅列举核心新增示例, 其余既有真过滤规则不受影响」理解（更可能是本意), 那措辞需要改成不产生歧义的写法, 且 SC-3 应该补一条正面断言锁定这个理解。

**建议**: What.1b 该句改写为「对 claude-config 源, `:337` 的『`jq '{...}'` 形状即给 credit』规则不适用；既有 grep 锚点 / `sed s×`/`d` / `cut -d/-f` / `awk $N` / `jq keys/length/paths/leaf_paths` / `wc` / `sha*sum` / `>/dev/null` 族等『内容层面确实做了过滤或丢弃』的 credit 规则不受影响, 照常适用」, 消除「仅」的歧义; SC-3 补一条 `cat ~/.claude/settings.json | grep '^model='` → 0（真过滤仍应放行）的正面 fixture。

**严重度**: Major —— 两种读法都会产出一个能过当前 SC-3 全部断言、但违背作者真实意图的实现（要么误拦要么漏拦), 且不属于「TDD 会自动暴露」的类型（因为没有对应 fixture 去撞这个歧义点), 需要 spec 层面在 B.2 之前明确澄清。

---

### R2 最终判定

**verdict: REVISE**（较 R1 的 1C+2M+2m 降为 0C+2M+0m, R1 全部 5 条已忠实落地且原处方经复核成立, 仅在 v1→v1 的引用锚点上做了一处自我勘正; 新开 2 条 Major 均出自「架构透镜审 v2 新增文本」而非对已收敛条目的反悔）。触发 REVISE 判据: ≥2 Major。

两条新 Major 都定位在同一处（What.1b 的「按段跳过 :337」这句话）: 一条是「怎么实现」缺信息通道 + 顺序依赖未覆盖（[A1-R2-1]), 一条是「跳过多少」的「仅」字面歧义（[A1-R2-2]）。两条都建议在 What.1b 原地补一两句消歧文字 + SC-3 各补一条 fixture, 改动量小, 不影响已收敛的双平面清单 / 前置字符类 / python3 处置方向, 预期可以在 R3（如需要）一轮内收敛。

---

## R2 终判 (v3)

复核对象: proposal.md v3 的 What.1b（:29-31）+ SC-3（:58）。逐条判 R2 两条 Major closed / not-closed, 并单独扫一遍这两段新文本本身有无引入新问题。

### [A1-R2-1]（credit 判定缺信息通道 + 混合源顺序依赖）— **closed**

v3 What.1b 新增「机制写死 (R2 A1-R2-1: 无顺序依赖)」一段, 逐句对应我 R2 的诊断: 明确点出 `_sg_compute_credit` 只接收 `$seg`、没有「哪条 pattern 触发」的信息通道 (与我复核控制流后写的结论一字不差), 并采纳了我给的两条路里更安全的那条 (b) —「credit 计算内对 `$seg` 重匹配 claude-config 源名组, 命中即进入收紧模式」—— 不依赖 risky_patterns 数组书写顺序, 从根上消除「先命中 .env pattern 导致 memoize 到宽松 credit, 再复用到 claude-config 命中」这个旁路。混合源显式收敛为「恒收紧」（更严方向, 无旁路), 与我建议的处理方向一致。

SC-3 新增 fixture `cat ~/.env ~/.claude/settings.json | jq '{env: .env}'` → 2, 正是我要求的「混合源无顺序依赖」锁定断言, 逐字对应。

我在 R2 报告里还带了一句次要建议（claude-config 字面量集合会同时存在于 risky_patterns 检测面和 credit 收紧判据两处, 建议提示未来维护要同步或提炼共享变量）—— v3 文本没有单独写这句提示。这不影响本条关闭判定: 那是我原文里明确标注的「可控的维护成本, 不是设计缺陷」的附带建议, 不是构成 Major 的核心诉求（核心诉求是「信息通道缺失 + 顺序依赖」, 已解决）。可以作为 B.1 入场时的一条隐性检查项自然带到（新增 pattern 行时同步改两处), 不需要为此在 spec 层面二次打回。

### [A1-R2-2]（收紧模式「仅」的字面歧义）— **closed**

v3 采纳的是我给的两种读法里**更严的那一种**（不是我举例倾向的「grep 锚点等既有真过滤规则不受影响」那一种), 但这不构成 not-closed —— 我 R2 原文的核心诉求是「歧义必须消掉 + 给出理由 + 落 SC 断言」, 没有预设方向。v3「行级过滤 credit (grep 锚/`grep -v`/sed/cut/awk) 显式排除」给出的理由（JSON 值可跨行、可同行内嵌, 行/列级过滤对 JSON 结构不构成可靠脱敏, 不像 `.env` 那种一行一条 KV 场景）经复核站得住: `jq -c` 紧凑输出整份 JSON 可以压成一行, 缩进/换行不是 JSON 的结构性字段边界保证, 通用 grep 锚点/`cut -f`/`awk $N` 这类行列启发式对 `.env` 成立、对 JSON 不成立 —— 本质上和 [A1-C1] 当初打掉 `jq '{...}'` 形状 credit 是同一类论证（「命令形状看着像过滤, 但不保证真的把敏感字段过滤掉」), 这次把同一论证延伸套用到 grep/sed/cut/awk 上, 逻辑自洽, 不是临时拍板。

`收紧模式` 被写成一个整体 mode gate（命中 claude-config 源 ⇒ 只认 4 类白名单, 其余全部分支一律不算 credit), 比我 R2 报告里设想的「只单独 gate `:337` 一个分支, 其余分支各自判断是否需要收紧」更简单、耦合面更小 —— 一个布尔开关切换整个函数的判定集合, 不需要逐分支单独决定「这条要不要因为 claude-config 而额外加条件」, 实现和后续审计都更省心, 是比我原方案更好的收敛方式。

SC-3 新增 `... | grep '^  "model"'` → 2、`... | cut -d: -f1` → 2 两条 fixture, 覆盖了「行级过滤对 claude-config 源不生效」这一断言, 满足「≥2 条」要求, 也和 v3 选的「排除」方向一致（若实现按字面「仅」跑通白名单模式, 这两条会真的从基线 0 翻到 2, 是有效的 baseline-failing 断言, 不是摆设）。

### 逐条核对 v3 新文本的行号引用（防止本轮说理本身带错的数字）

对照 `aria/hooks/secret-guard.sh` @ `400f0bc`（与 spec 冻结基线一致的行号体系):

| 引用 | 位置 | 内容核对 |
|---|---|---|
| jq 名字面类 `:332` | `_sg_compute_credit` | 属实, `keys\|length\|paths\|leaf_paths` 规则（枚举漏写 `leaf_paths` 字面, 纯文字省略, 规则本身按 `:332` 整条引用未受影响, 不构成错误, 仅顺带一提） |
| `wc -[clw]` `:384` | 同上 | 属实 |
| `sha*/md5sum` `:387` | 同上 | 属实 |
| 丢弃族 `:373-380` | 同上 | 属实, 覆盖 `>/dev/null`/`&>/dev/null`/`-o /dev/null` 三条 |
| grep 锚 `:348` | 同上 | 属实 |
| `grep -v` `:351` | 同上 | 属实 |
| sed `:354` | 同上 | 属实 |
| cut `:358` | 同上 | 属实 |
| awk `:362`/`:365` | 同上 | 属实（`$N` 引用规则 + `/regex/` 规则两条各自独立） |

无行号引用错误, 无新事实断言问题。

### 有无引入新错（架构透镜扫描, 非仅核对既定诉求）

- 「恒收紧」/「收紧模式全关」都是朝**更严**方向收敛（漏判 → 拦, 不是拦 → 放), 与本 spec「漏报优先于误报」的既定取舍方向一致, 没有反向引入新的 fail-open 面。
- 收紧模式由 credit 函数内对 `$seg` 独立重扫 claude-config 字面量触发, 不依赖触发本次 credit 计算的具体是哪条 `risky_patterns` —— 意味着一个纯粹读 `.bashrc`、但命令文本里**恰好**在无关位置（例如注释）提到 `.claude.json` 字样的命令, 也会被拖进收紧模式而失去行级过滤 credit。这是过度收紧的边角误伤, 但方向仍是「该拦的沒漏, 可能多拦几个不该拦的」, 与 hook 自身文档已声明的「Over-redaction is acceptable, 漏判不可接受」哲学一致, 不是本轮新引入的独立问题类别, 不单独开 finding。
- SC-3 对照组「`.env` 源单独的 `\| jq '{...}'` 行为不变」仍保留在 v3 文本里, 与「收紧模式只在检测到 claude-config 字面量时进入」的机制描述一致, 未被新增内容意外覆盖或弱化。
- v2→v3 的 diff 只集中在 What.1b 与 SC-3；重新核对 What.1 / What.3 / Out-of-scope / Tasks 等其余段落文本与 R2 复核时读到的版本逐字一致, R1 [A1-M1]/[A1-M2]/[A1-m1]/[A1-m2] 的已收敛结论未被本轮改动波及, 无需重新开启。

### 最终判定

**verdict: PASS**（R2 两条 Major 全部 closed, 复核未发现 v3 新文本引入的新 Critical/Major/Minor; R1 五条 finding 与 R2 两条 finding 累计七条全部收敛, 本席无未闭合项）。

**未闭合项: 无。**
