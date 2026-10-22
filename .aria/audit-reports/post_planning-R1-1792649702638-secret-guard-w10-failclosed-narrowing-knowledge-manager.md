---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T12:26:41.512Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — knowledge-manager 席位报告

> 对象：`10CG/aria-plugin#217` / `secret-guard-w10-failclosed-narrowing` 的 A.2 计划（主仓 `a136dbf`）及其依据 proposal v3（`910d9fa`）、原型证据 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v3/`。
> 侧重：文档与同步面、`rule6_note`、收口与载体、证据可复现性。机制正确性（进程组、准入门、时间上界）归 backend-architect 席，本席只在碰到时顺带记录。
> 纪律：只读；实验全在 scratch（`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r1/knowledge-manager/`）；Forgejo 只做 GET；没有读其他席位的报告，没有读真实命令语料。

## 审计结论

**0 Critical / 9 Major / 6 Minor。** 设计方向与选定机制本席不质疑。问题集中在「计划怎么落到文档、发版面、收口动作和验收上」：有几项 Impact 没有任何任务认领；关闭 #217 的动作没有钉死且有误关别的 issue 的风险；`rule6_note` 的「逐字断言」说法和 SC-V7 实际钉的东西对不上；What 7 的「封闭清单」并不封闭；TASK-004 的验收漏了 P1 的主证据。

### 一、已核实成立（不需处置）

1. `fill.py` 能重生成 proposal：用 `mkv3.py` 对当前 `aria/hooks/secret-guard.sh`（v1.77.1）生成原型，再 `fill.py proposal-template.md v3.sh W8-v3.diff W12-real-traffic.txt`，输出与 `proposal.md` 逐字节相同（45946 字节，`cmp` 无差异）。
2. `mkv3.py` 对当前 hook 生成的 diff 与已提交的 `W8-v3.diff` 完全一致（去掉两行文件头后 diff 为空）。`git diff --stat 59e333c..HEAD -- hooks/`（aria 子模块）为空，hook 与测试套件相对基线零差异，所以 proposal 里的基线行号可以沿用。
3. `commentsync.py`：baseline 模式在基线 hook + 套件上 GREEN；target 模式在注释未改的原型上 RED(22)。与 proposal What 7 的说法一致。
4. 在 scratch 副本里复跑 `run-w10-w11.sh <基线 hook> <工作目录>`（33 s）：`W10-mechanism.txt` 与已提交版逐行相同；`W11-adversarial.txt` 的 rc 与文案类别全部相同，只有墙钟有小幅差异（符合 README「只看结局与相对关系」）。`w10b.sh <工作目录>`（18 s）输出与 `W10b.txt` 逐行相同（P6 四条 IDENTICAL，P10 三条结果相同）。
5. `dispositions.md`：R1 的 24 行表与 `git show 41e93089:…/proposal.md` 里的表逐字相同（脚本比对 24/24），顶部四条「不同步」声明齐全，R2 的 A1–A29 共 29 行，级别与 R2 汇总抽查（A5=M、A29=m）一致。结构成立。
6. 仓自带解析器 `lib/detailed_tasks.py:parse_detailed_tasks` 解析 `detailed-tasks.yaml` 得 `parse_ok: true`、7 个任务，status 均为 `pending`。
7. proposal 引用的 16 个基线行号抽查全部对得上（`:476` 行内没有 `tight` 字样，但它正是 tight 家族判定的 `if`，`:475` 起声明 `local tight=0`）；`secret-hygiene.md` 的 `:23`、`:316`、`:352` 确为三处测试计数。
8. `#139`、`#142`、`#229`、`#230`、`#228`、`#217` 在 `10CG/aria-plugin` 均为 open（GET 核实）。

### 二、Findings 索引

| # | severity | category | 针对 | 一句话 |
|---|---|---|---|---|
| KM-1 | Major | documentation | 任务计划 TASK-007 / INV-6；proposal 头「编号约定」 | 关闭 #217 的机制没钉死：关键词字面、承载提交、顺序、核对命令、关闭后验证都缺，仓里无先例，裸号会关到主仓的 Aria#217 |
| KM-2 | Major | documentation | 任务计划 TASK-001 | 「开两张残余 issue」不在 owner 的一次性授权四类里，计划没有 owner 门也没引授权依据 |
| KM-3 | Major | testing | 任务计划 TASK-001 / TASK-002 | 「基线红」排在还没有用例的 TASK-001；SC-V11、SC-V12 没归类 |
| KM-4 | Major | documentation | 任务计划 TASK-006 / INV-2；proposal Impact、SC-V12 | standards 三处计数、CHANGELOG 终稿与占位符、tag 没有任何任务认领或验收；前科：v1.76.1 就漏了同一步 |
| KM-5 | Major | testing / documentation | 任务计划 `rule6_note`；proposal SC-V7 | 「逐字断言」与 SC-V7 实际只钉首行和 `Matched pattern` 行对不上；「复用两条指令行」实为 3 取 2；n/a + 散文 row 1 的写法与 WP-A 先例不同且缺复议标注 |
| KM-6 | Major | testing | 任务计划 SC-V7 / TASK-002 / TASK-003；既有套件助手 `wpa_x_finding` | `wpa_x_finding` 的两个谓词会放过 `longline` 文案，「普通命中文案」断言区分不了二者 |
| KM-7 | Major | documentation | proposal What 7；任务计划 TASK-002 / TASK-005 | 「封闭清单」漏了仍在说「never passed」的注释和 W9 六组里四组的 `Red when` 说明块 |
| KM-8 | Major | testing | 任务计划 TASK-004 / TASK-005 / TASK-006 | TASK-004 验收缺 W9 旧套件「恰好六组红」等 P1 主证据；「(136/137)」与证据 137/137 不符；证据不绑发版 hook；脚本原位覆盖原型证据 |
| KM-9 | Major | documentation | proposal 放宽面、CHANGELOG 草稿；任务计划 TASK-001 / TASK-007 | #217 关闭后，裁定 E 的放开、扩展项目整串门（评论 28512 第 2 点）和「≤ 8192 判定可超 5 s」三项残余没有载体；#230 点名不当，#138/#140/#141 漏点名 |
| KM-10 | Minor | documentation | proposal CHANGELOG 草稿 | 体例与申报精度：无 Rule #6 行、130 与 137 未对账、放行类危害没写具体、被拦命令的延迟变化没申报 |
| KM-11 | Minor | documentation | proposal Impact 发布同步面；任务计划 TASK-006 | 「照 v1.77.0 的实际改动」不准确；基线已是 v1.77.1；VERSION 与 i18n 当前已漂移；漏 tag；取号需合并前重核 |
| KM-12 | Minor | documentation | 证据 `v3/README.md` 与脚本 | 复现说明缺调用参数、会原位覆盖已提交证据、依赖清单不全、「17」「+106」两个数字不准 |
| KM-13 | Minor | documentation | 任务计划 TASK-007（阶段 D） | D.1 / D.2 / handoff / claim 释放没写；归档前任务须为 done，否则 Step 7 自动建 tracker；无 post-ship 复验腿 |
| KM-14 | Minor | documentation | 任务计划 INV-1 / INV-2 / TASK-003 / TASK-005；proposal 引用 | 几处能有两种读法，以及 E12 无路径、「71 条」口径、17 处审计簇编号 |
| KM-15 | Minor | documentation | proposal v3 与 detailed-tasks（全文） | 新文本 68 处裸 `#n`，头部「编号约定」与 standards `content-integrity.md` §4.4 规则 1 冲突 |

### 三、逐条 finding

#### KM-1　关闭 #217 的机制没钉死，且有误关别的 issue 的风险
- **type**：issue　**severity**：Major　**category**：documentation
- **针对**：任务计划（`detailed-tasks.yaml:28-29` INV-6、`:111-120` TASK-007）；proposal v3 `:22`（编号约定）、`:496`
- **摘要**：计划只说「关闭关键词只出现在阶段 D 的主仓提交」，没写关键词字面、是哪个提交、与对账评论的先后、「关键词核对」怎么做、关闭后怎么验证。仓里没有用提交关键词跨仓关闭 aria-plugin issue 的先例，同类的 #216 是评论加显式 close。若执行席按头部「裸 `#n` 指 aria-plugin」的约定写 `Closes #217`，主仓的 `Aria#217`（另一个 open 的无关 issue）会被关掉。
- **证据**：
  - TASK-007 没有 `deliverables`，两条 acceptance 都是「评论列了什么」，没有「#217 state=closed」「Aria#217 仍 open」。INV-6 的「核对」没有正则、没有范围（三个仓的提交、PR 标题与正文）。
  - 无先例：`git log --all -i -E --grep='(clos(e|es|ed)|fix(es|ed)?|resolv(e|es|ed)) +10CG/aria-plugin#[0-9]+'` 在主仓为 0 条。
  - #216 的做法（`GET /repos/10CG/aria-plugin/issues/216/timeline`）：2026-10-20T12:44:41Z 一条「## 收口 (v1.76.1…)」评论，同一秒一个 `close` 事件，无 `ref_commit`。
  - `GET /repos/10CG/Aria/issues/217` 为 open，标题是 session-closer 的 locale 缺陷，与本变更无关；`Aria#229`（guard-bypass.log 缺换行，也沾 secret-guard）、`Aria#230` 同样 open 且无关。
  - 主仓双推 GitHub，同一提交也会被 GitHub 解析；GitHub 上 `10CG/aria-plugin` 是否有同号的另一条 issue：**未核实**（本轮只读 Forgejo）。
  - 提交关键词跨仓关闭是否在本 Forgejo 实例生效：**未验证**（需要写操作），我对 Forgejo 实现的理解是写权限满足时生效，仅作推断。
- **建议**：
  1. 仿 #216：TASK-007 = 对账评论 → 显式 close（API）→ `GET …/aria-plugin/issues/217` 核 `state=closed`，`GET …/Aria/issues/217` 核仍 open；两条写进 acceptance。
  2. 若坚持用提交关键词：写死字面 `Closes 10CG/aria-plugin#217`、指认承载提交（建议 D.2 归档提交）、顺序（评论先发）、失败后备（显式 close），并先在一个测试 issue 上验证跨仓关键词会触发。
  3. INV-6 补成可执行：推送前对 aria / standards / 主仓三仓的 `git log <remote>/master..HEAD --format=%B` 和待推 PR 的标题与正文跑 `grep -inE '(close[sd]?|fix(e[sd])?|resolve[sd]?|reopen[sd]?)[[:space:]:]+(10CG/[A-Za-z-]+)?#[0-9]+'`，限定写法与裸写都要覆盖，命中即停，结果记进 notes。

#### KM-2　TASK-001 的外发动作没有授权依据
- **type**：issue　**severity**：Major　**category**：documentation
- **针对**：任务计划 TASK-001（`detailed-tasks.yaml:34-46`）
- **摘要**：TASK-001 含「先开两张残余 issue」，另有 #217、#228 两处留言。owner 的一次性授权只有四类：feature 分支推送、开 PR、issue 评论、issue 关闭，不含「开 issue」，范围也写的是「WP-A / WP-B / WP-C 及其后续」，没有点名本变更。计划里没有 owner 门，也没引授权条款。
- **证据**：`.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` §4；WP-A `proposal.md:396` 原文「开 issue 不在一次性授权内」；2026-10-22 的 owner 裁定（`post_spec-R2-…-aggregated.md:233` 起的「Owner 裁定（2026-10-22）」）三条都不涉及这类外发动作。
- **建议**：
  1. TASK-001 前置「两张 issue 的草稿贴给 owner，确认后再开」，或引用决策单里确实含「开 issue」的条款。
  2. 留言类动作写明依据「本变更视为 WP-A 的后续」，并注明由谁确认这个前提。
  3. 两张 issue 的正文要点进计划：评论 28512 第 1 点（多行 for 循环的触发点是值限 4096）、Decision 9（heredoc 内赋值形文本是 D 失败的根因）、Decision 10（按字面「止于换行」会截断反斜杠续行列表，新增漏检；真实流量 0 例）、基线行号。标题沿用 `[缺陷][secret-guard] …` 体例。

#### KM-3　「基线红」排在还没有用例的 TASK-001
- **type**：issue　**severity**：Major　**category**：testing
- **针对**：任务计划 TASK-001（`:44`、`:46`）、TASK-002；proposal `:399-402`、`:490`
- **摘要**：TASK-001（B.1，主控，无依赖）要求把 SC-V2/3/4/5/7/8/10 在基线上「实跑为红」、SC-V1/6/9 标回归闸。但 proposal 明写 SC 的具体形状「在 TASK-002 落进套件」，用例是 TASK-002 的执笔席写的。TASK-001 时刻没有 SC-V 用例可跑，只能拿原型证据脚本（`v3unit.sh` 等）去打基线，而这些脚本直调 `_sg_relax_run` 这类基线上不存在的函数，得到的是「命令不存在」式的假红，这正是 INV 里自己提醒过的 127 陷阱。另外 12 条 SC 只归了 10 条，SC-V11、SC-V12 没有基线口径。
- **证据**：见上列行号；`v3/README.md` 说明 `v3unit.sh` 用桩判定替换 `_sg_vx_pass`，函数在基线上不存在。
- **建议**：把「基线红」挪进 TASK-002 当先红后绿：写 SC-V 用例（只动套件）→ 在基线 hook 副本上跑，逐条记红或绿，并核对红的原因是期望不符而不是 127 → 再实现；记录落 notes。TASK-001 只留认领、建分支、重锚、issue、留言。补 SC-V11（基线上「无 `{8193`」为绿，INV-4 闭包对尚不存在的新函数是空真）、SC-V12（`commentsync.py target` 在基线为红）的归类。

#### KM-4　standards 三处计数、CHANGELOG 终稿与 tag 没有任务认领或验收
- **type**：issue　**severity**：Major　**category**：documentation
- **针对**：任务计划 TASK-002 / TASK-006 / INV-2；proposal Impact（`:416`、`:427`、`:431-448`）
- **摘要**：Impact 里的 standards 三处计数改动，INV-2 允许了，但没有任何任务把它列为 deliverable 或 acceptance：TASK-002 的产物只有 hook 和套件，TASK-006 没有 deliverables，acceptance 三条里不含它。CHANGELOG 草稿有 `1.77.x`、`<date>`、两处 `<N>`、两处 `<n>` 共 6 处占位符，同样没有「终稿零占位符」的验收。SC-V12「standards 三处计数一致」按字面读是「三处互相一致」，而它们现在就互相一致（都是 822/816），所以基线即绿，证明不了什么。
- **证据**：
  - 前科：`secret-hygiene.md:23/316/352` 仍是 822/816（最后一次计数同步 standards `191560e`，2026-10-15），而套件头注释 `secret-guard.test.sh:11` 已是「831 cases (825 without zsh)」，v1.76.1 的 CHANGELOG 写 825。v1.76.1 发版时漏了这一步，现在已差 9。这台机器没有 zsh（`which zsh` 无输出），831 = 825 + 6 个 zsh 条件用例。
  - 既有的 SC-13（`secret-guard.test.sh:3221-3231`）只校验「头注释 N 或 M 等于实跑数」，注释里明说跨仓的 standards 三处由回填时机械 grep 确认，不在套件内；本计划没有这一步。
  - `.aria/state-checks.yaml:29-56` 的 `no-unresolved-version-placeholder` 只认 `<vNEXT>`，对 `<N>`、`<n>`、`<date>`、`1.77.x` 不设防；v1.73.0 发布时残留 `<vNEXT>` 的事故是同类前科。
  - standards 是独立子模块：改动要走分支、本地合并、双推、`ls-remote` 核验，再 bump 主仓 gitlink（Impact 只有半句「standards 也变时另加一个」）。
- **建议**：给 TASK-006 补 deliverables 与 acceptance：（a）standards 三处 = 套件头注释的双值（N = 实跑 + 6，M = 实跑），并走完上面的子模块流程；`secret-hygiene.md:316` 括号里的测试族清单是否加新族（#145/#153/#179 的做法是加）也在此定下，同时补上 v1.76.1 欠的时间预算族；（b）CHANGELOG 终稿对 `grep -nE '<[A-Za-z]+>|1\.77\.x'` 零命中，数字取自 TASK-004 的 W14；（c）SC-V12 第二句改成「三处都等于套件头注释的 N 与 M」。

#### KM-5　`rule6_note`：断言口径与 SC-V7 对不上，写法与 WP-A 先例不同
- **type**：issue　**severity**：Major　**category**：testing / documentation
- **针对**：任务计划 `meta.rule6_note`（`detailed-tasks.yaml:8-14`）；proposal SC-V7（`:411`）、Impact（`:429`）
- **摘要**：整体判 `n/a`（不属 Skill 变更）本身合规，与 WP-A 块 A 一致，SOT §4.1 对 `n/a` 的定义也是如此。问题在三处：
  1. 「由逐字断言替代」说的是 `wpa_x_longline`，但 SC-V7 明写只「钉首行与 `Matched pattern:` 行」。判描述性的前提是「处方部分都来自既有 oversize 模板」，而没有任何计划内的断言能在有人追加一句处方时转红（WP-A 的 13d 是这么做的）。
  2. 「复用现有 oversize 模板的两条指令行」不准：oversize 模板（`secret-guard.sh:851-865`）有三条 bullet，longline 模板（`W8-v3.diff:173-189`）只有两条，去掉了「do not repeat one long $VAR many times in a single command」。是不是有意去掉、为什么，没有披露。
  3. 三处 AI 可见文案被判 row 1，却只出现在 `note` 的散文里，YAML 五字段整体写 `n/a`。WP-A 的做法是分两块，块 B 给 hunk 单独写 `decision_table_row: 1 / scenario1: not_required / scenario4b: not_required / negctrl: n/a`，并标注「AI 自作主张，待 owner 复议：判第 1 行而非第 3 行」（Rule #10 要求自作主张的流程判断写进 handoff）。本计划引的「WP-A owner ruling」其实是决策单 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md` §3 的一句「hook 的 substitute 框定，提示文案的 hunk 单独判」，它没有裁定该 hunk 落第几行。
- **证据**：见上列行号；WP-A `proposal.md:315-343`。
- **建议**：
  1. `rule6_note` 拆两块对齐 WP-A，块 B 覆盖 `longline` 模板与两条增长原因串，写明待 owner 复议，并给出决策单的路径。
  2. 要么把第三条 bullet 补回（最稳：指令部分与 oversize 模板逐字相同），要么写明去留理由。
  3. SC-V7 增加整模板钉：归一化 `Matched pattern:` 与 `Command was` 两处动态内容后逐字比较；至少断言「Split it…」及其 bullet 行逐字等于 oversize 分支的同名行，并要求「追加一句处方句则转红」。

#### KM-6　`wpa_x_finding` 会放过 `longline` 文案
- **type**：issue　**severity**：Major　**category**：testing
- **针对**：任务计划 SC-V7 / TASK-002 / TASK-003；既有套件助手（`secret-guard.test.sh:2522-2527`）
- **摘要**：`wpa_x_finding` 只断言输出含「reads a secret-bearing source」且不含「too large to scan」。`longline` 模板的首句恰好是「command reads a secret-bearing source, and after variable…」，两条谓词都满足。于是 W9 里改成期望「普通命中」的用例，以及 SC-V7 的「多行大副本 → 普通命中文案」，对「所有大副本一律走 nocredit / longline」这类坏实现是绿的。能抓住它的只剩「良性大命令 exit 0」，而且要那条良性命令命中某条规则并带 credit 才行。TASK-003 的 BI 清单（BI-1…13）里没有对应的坏实现。
- **证据**：实验脚本 `…/knowledge-manager/finding_vs_longline.sh`，在 `mkv3.py` 生成的原型上用 21ab#1 的形状（运行时拼装路径）：`rc=2`，首行「[secret-guard] BLOCKED: command reads a secret-bearing source, and after variable」，两条谓词的结果为 yes / no（即 `wpa_x_finding` 通过），同时含「has a line longer than」。`v3/probe21.sh:16-21` 自己的分类器把 `longline` 排在 `finding` 之前，正是因为这个重叠。
- **建议**：`wpa_x_finding` 另加两条断言——首行含 `command reads a secret-bearing source without`（普通模板首行，longline 没有「without」）、全文不含 `has a line longer than`；`wpa_x_longline` 反向断言。TASK-003 增一个 BI：把 `_sg_vx_big_judge` 写成总走 nocredit（或最长行判据恒真）。

#### KM-7　What 7 的「封闭清单」并不封闭
- **type**：issue　**severity**：Major　**category**：documentation
- **针对**：proposal What 7（`:331-345`）；任务计划 TASK-002 / TASK-005
- **摘要**：清单按「退役短语」逐站点核对，但同一段落里仍然会变错的句子不在清单内，`commentsync.py target` 全绿时它们还在。另外 W9 列出的六组变更用例，其说明块只覆盖了 21ab（21aa/21ab 站点）和 21ac（21ac/21ad 站点）。
- **证据**（行号为基线）：
  - 「never passed」：`secret-guard.sh:93`（站点 1，退役短语只切到「…too large to scan」，后半句「…, never passed」留下）、`:579-580`（站点 2）、`secret-guard.test.sh:2513`（站点 9）。放宽之后超限命令可以放行，这三句都会变假。
  - `secret-guard.sh:580-581`「The oversize string is never built, expanded further, judged or scanned」：放宽重跑里它会被构建和判定，站点 2 的三个退役短语没有覆盖它。
  - 套件里四组变更用例的说明块不在任何站点：21ag（`:2585`「or is refused by another limit line」）、21aj（`:2597-2599`「refused at once… over the copy limit」）、21al（`:2632`「the edge moves by one (the two commands swap sides)」）、21ao（`:2681`同句）。新语义下这两条边不再对换，两侧都是「完整判定」。
  - `commentsync.py` 的 `runs()` 只认整行注释，行尾注释不计。对原型跑 target 模式，hook 侧的 `longline`、`_sg_relax_run`、`status 4` 在整行注释里均为 n=0，也就是说原型自带的注释满足不了「应出现」那一半，执笔席必须自己新写含这些词的整行注释，而 proposal 没有给出这些注释的内容，只给了词。
- **建议**：
  1. RETIRE 补带上下文的唯一片段（baseline 模式要求每条恰好命中一次，不能直接用「never passed」）：站点 1 `owner ruling 2026-10-14), never passed`；站点 2 `and never passed: a copy that is not judged is a way past the guard` 和 `The oversize string is never built, expanded further, judged or scanned`；站点 9 `-- never passed (the COUNT bounds`。
  2. 新增站点 11：套件里 21ag / 21aj / 21al / 21ao 的 `Red when` 说明与用例标题同改，对应补退役短语。
  3. TASK-005 的 acceptance 补一条「What 7 各站点及新增站点的文字与新行为相符」。proposal 写了「位置由 TASK-005 把关」，但任务里没有这一项，TASK-005 也没有任何审查清单。

#### KM-8　TASK-004 的验收缺项，数字与证据冲突，证据不绑发版 hook
- **type**：issue　**severity**：Major　**category**：testing
- **针对**：任务计划 TASK-004（`:78-88`）、TASK-005、TASK-006
- **摘要**：
  1. 标题写「重跑 W9–W12」，acceptance 只有 W12 第 1、2、3 节和 P6 回落。缺 P1 / SC-V1 的主证据：旧套件在实现 hook 上恰好六组失败（21ab、21ac、21ag、21aj、21al、21ao）、其余全绿；也缺 W10 机制（S1–S8 / G1–G8）和 W11 矩阵的结局。
  2. 「放行数不低于原型 (136/137)」与证据不符：`W12-real-traffic.txt` 与 `W12b-rerun.txt` 都是「size 类 137 条全部 allow，1 条 VMAX 照拦」，即 137/137，proposal Why 表也写 137 与 137。136 没有出处；若是想给 n=172 贴近截止留容差，应明写容差及依据，而不是写成「不低于原型」。
  3. TASK-004 与 TASK-005 并列依赖 TASK-002，没有「代码审查后改动了 hook 则复跑 TASK-003 与 TASK-004」的规则；TASK-006 也不核对证据对应的 hook 就是待发的 hook。CHANGELOG 里的 `<N>`（放行条数、测试数）可能取自旧代码。`W9-suite.txt` 页眉已有 hook sha256 的做法，可直接沿用。
  4. 现有脚本把输出写在 `$HERE`（已提交的证据目录）原位：`run-w10-w11.sh:8,17`、`run-w12.sh:9,17`、`run-w12b.sh:13`。计划要把它们「改成接受实现 hook 路径」后重跑，会覆盖 proposal 引用的原型证据，而 `W12-real-traffic.txt` 又是 `fill.py` 的输入，proposal 因此无法再逐字重生成。
- **建议**：acceptance 补 W9 旧套件恰好六组红且名单固定、W10 与 W11 结局同原型；W12 第 1 节写 137/137（负载 < 2），或写明容差；输出一律落 `W14`，W9–W12 冻结；W14 页眉记录 `sha256sum aria/hooks/secret-guard.sh`，TASK-006 核对一致；TASK-005 之后 hook 若有改动，TASK-003、TASK-004 复跑。

#### KM-9　#217 关闭后，放宽外延的缺口和残余的载体
- **type**：risk　**severity**：Major　**category**：documentation
- **针对**：proposal 放宽面（`:371-380`）、裁定 E（`:396`）、CHANGELOG 草稿（`:443`）；任务计划 TASK-001 / TASK-007
- **摘要**：逐项回答「是否仍有载体」：
  - `#139`、`#142`、`#229`：open，有载体。
  - `#230`：open，但它是 W9 扩展的 `_sg_ext_subst` 只替换前 64 处命中，而准入门第 5 条要求没有扩展条目生效，放宽路径永远不跑扩展腿。点名「放宽后覆盖流量变多」不成立（proposal 头部「关联」、`:376`、CHANGELOG 草稿「`#142` / `#229` / `#230` 同理」三处）。
  - 同类却没点名：`#138`（跨段 pattern fail-open）、`#140`（`ssh host '…'` / `sh -c` 外壳逃逸）、`#141`（`&` / 换行未切分），均 open。大副本改走普通判定后，普通判定的全部既有欠拦缺口都同样适用，按类表述比逐个点名更稳。
  - **无载体 1，裁定 E 的「实测通过后另行放开」**：只翻 `OSTYPE` 不够，作业开工前的组长自检读 `/proc/$BASHPID/stat`，macOS 没有 `/proc`，会永远回落（`v3/README.md:19` 把 `/proc` 列为依赖）。`#219` 讲的是 Windows 上 5 s 超时放大，不是放宽的启用条件；macOS 没有任何 issue。
  - **无载体 2，评论 28512 第 2 点**（扩展项目的整串绝对门）：TASK-007 只在对账评论里「写明残余」，评论挂在要被关闭的那条 issue 上。
  - **无载体 3，「≤ 8192 的判定只受协作式预算约束，单次可超 5 s」**：CHANGELOG 草稿把它归「`#228` 及新开残余 issue」，但 `#228` 的正文和三条评论（29792、29840、29957）里没有 R2 TL2-F5 的具体情形（8 KB、4000 行、需要算 credit，基线端到端 7–19 s 后放行），TASK-001 计划的 #228 留言又只写「Decision 12 的选项 + 证据位置」。
- **建议**：
  1. 放宽面改按类写：「大副本改走普通判定，#138 #139 #140 #141 #142 #229 的既有欠拦缺口同样适用」，删去 #230 或注明因准入门排除扩展项目而不适用。
  2. 载体：在 #219 留言或新开 issue，写明非 Linux 启用放宽需要可移植的组长自检、`kill` 语义实测、macOS 无 `/proc`；28512 第 2 点并入同一张或另开「扩展项目整串绝对门」；TASK-001 的 #228 留言加入 TL2-F5 情形及证据位置（post_spec R2 的 TL2 席报告）。
  3. TASK-007 的对账评论里，这三项都写「转 #NNN」，不要只在评论里写明。

#### KM-10　CHANGELOG 草稿的体例与申报精度
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：proposal Impact 的 CHANGELOG 草稿（`:431-448`）
- **摘要与证据**：
  1. 骨架按 v1.76.1（问题 / 修复 / 行为变更 / 已知限制 / 测试 + Refs）是对的，但缺 Rule #6 行：v1.77.1、v1.77.0、v1.75.0 都有（v1.75.0 的 `rule6_note` 行还带着「AI 自行判定，已列入待复议」的披露），v1.76.1 没有。
  2. 「739 条中 130 条（17.6%）」与「137 条放行 <N> 条」并列，口径不同：前者来自 E12，> 8192 **字节**共 739 条；后者来自 W1，> 4096 字节被尺寸上限拦下共 138 条（137 条总长 + 1 条值长）。读者会以为同一总体对不上。
  3. 放行类的危害写得抽象。proposal R-b 有具体构造（W11 的 shrink：读一个 AWS 凭据文件路径，加一处无关的 `>/dev/null`，基线 rc=2，原型 rc=0；本轮复跑结果相同），CHANGELOG 只写「沿用 credit 语义」。WP-A 的 CHANGELOG 做的是逐条「双向申报」，这里宜写一个具体例子。标题的「不新增 fail-open」也宜说明口径：失败路径一律回落为拦，但普通判定的既有欠拦现在覆盖到大命令。
  4. 没申报延迟变化：回落为基线拦截的大命令现在最长要多等到截止（约 3 s）。W11：f5like 基线 0.77 s、原型 3.03 s；apply-heavy-cjk 基线 2.02 s、原型 3.04 s；这两条的结局都还是 rc=2 且文案为基线 oversize。
  5. What 6 的死代码清理没出现在 CHANGELOG，而 Impact 写了它。
- **建议**：补上述五点；最后一行 Refs 保持，但按 KM-9 的结论调整被点名的 issue。

#### KM-11　发布同步面：来源标注不准，基线已漂移，漏 tag，取号需重核
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：proposal Impact（`:420`、`:428`）；任务计划 TASK-006
- **证据**：
  - 「照 v1.77.0 的实际改动列全」：v1.77.0 主仓同步 `ae746262` 改了 CLAUDE.md、README×4、aria、两份架构文档共 8 个文件，没有 `VERSION`；v1.77.1 的 `0bd647a6` 只改了 README.md、aria、两份架构文档（外加该特性自己的文件），没改 `VERSION`、i18n README、CLAUDE.md。proposal 列的 9 个文件（含 `VERSION`）其实是 v1.76.1 的 `878f8d99`。
  - 当前基线漂移：根 `VERSION` 的子模块表仍写 aria v1.76.1；`i18n-readme-translation-currency` 现在就是 STALE（三份 i18n README 的 `translated-from` 是 1.77.0，插件 1.77.1，我在 scratch 里按 `.aria/state-checks.yaml:188-235` 的逻辑复算过）。TASK-006 的「三项机械检查全绿」其实是在补 v1.77.1 的欠账，应明说。
  - 「基线已是 v1.77.0」已过期：aria 子模块是 v1.77.1（`68c7f65`），v1.77.1 的 tag 在 origin 与 github 两端都在；下一个号是 v1.77.2 或更高。`meta.baseline_freeze`、TASK-001 的「v1.77.0 的 hooks/ 与 59e333c 零差异」同理（实测 `59e333c..HEAD` 的 `hooks/` 零差异，结论仍成立）。
  - TASK-006 没提 tag。`version-management.md` §4.3 自 v1.66.0 起恢复给 aria 打 tag，v1.76.1 的收口评论就核对了 tag 的双端 SHA。
  - 2026-09-30 决策单 §5：版本号在 ship 时刻取，合并前重新核 `plugin.json`；本计划写「版本号由 owner 定」，没写重核。现状有多条并行 track。
- **建议**：来源改写为「照 v1.76.1 的 `878f8d99`」，并列出已漂移的两处；TASK-006 补 tag 创建、双推、`ls-remote --tags` 核验，以及「取号在合并前一刻重核 `plugin.json` 与三远端 tag」。

#### KM-12　证据复现说明的缺口
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：证据 `v3/README.md` 与脚本
- **摘要与证据**：复现本身可行（见「已核实」第 4 项），但 README 不足以让第三方按它复跑：
  1. 没给调用参数：`run-w10-w11.sh` 需要 `<基线 hook> <工作目录>`（脚本第二行注释），`w10b.sh` 需要前者产出的工作目录且输出到 stdout，README 只写了脚本名。
  2. 按 README 从证据目录原位运行，会覆盖已提交的 `W10-mechanism.txt`、`W11-adversarial.txt`（脚本写 `$HERE`），产生只因计时变化而来的伪 diff。本轮是先拷贝再跑才避开。
  3. 依赖清单没列 `ps` / `pgrep`（procps）、`timeout`、`git`（`run-w9.sh`）、GNU `date -r`；列了 `shuf`，但 v3 脚本里没用到。没说明需要 UTF-8 locale：`apply-heavy-cjk` 形状依赖字符计数，本机 `LC_ALL=en_US.UTF-8`，脚本里到处 `grep -v setlocale` 说明别的环境会有告警。
  4. 「实跑 814，头注释写 831，17 个依赖 git show 的用例不运行」：831 − 814 = 17，但这台机器没有 zsh，6 个 zsh 条件用例本来就不跑，正常 checkout 的实跑数是 825，所以非 git 副本少跑的是 11 个而不是 17 个。此条是算术推断，**未核实**（没有跑全套件）。
  5. `W8-v3.diff` 的「+106 / −6」是不含空白加行的计数，含空白行是 +110 / −6。
  6. bash 3.2.57 是本机自建，没有构建配方，TASK-002 与 TASK-004 的 acceptance 都依赖它。
- **建议**：README 加「复现命令」节，逐个脚本写参数和输出落点，并建议先拷贝目录；补依赖与 locale；改正 17 与 +106；bash 3.2.57 的获取与构建方式写进 `.aria/tools/` 或 README。

#### KM-13　阶段 D 的内容没写进 TASK-007
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：任务计划 TASK-007（`:111-120`）
- **摘要与证据**：
  1. 只有 #217 的对账与关闭，没有 D.1 进度更新、D.2 归档、周期 handoff（Rule #9）、claim 释放（`release_gate`）、CLAUDE.md 项目状态覆写（受 `claude-md-hygiene` 约束）。
  2. 归档顺序有坑：`openspec-archive/SKILL.md:282-296` 的 Step 7 对「`tasks.md` 缺失时 `detailed-tasks.yaml` 非 done 的任务」自动建 Forgejo tracker issue（headless 亦然）。本计划 7 个任务全是 `pending`；若关闭关键词所在的归档提交先于任务标 done，会意外多出一张 issue。WP-A 在 `proposal.md:396` 对此有明文警示。#201 说明 Level 2 的 proposal 内 deferred 项这个门看不到，所以残余必须靠 TASK-001 的显式 issue（KM-9）。
  3. WP-A 有 post-ship 复验腿（用真实 harness 钩链打一条惰性诱饵）；本计划没有。放宽路径依赖 `set -m`、`/proc`、bash ≥ 5，且 hook 经 `$SHELL` 重入 bash，直接 `bash hook` 的 e2e 复现不了 harness 的进程环境。此条可选，进程环境的正确性归 backend 席，本席**未核实**。
- **建议**：TASK-007 补 D.1 / D.2 / handoff / claim 释放，写明「任务全部标 done 之后再归档」；评估是否加一条 post-ship 复验。

#### KM-14　措辞上有两种读法的地方，以及引用精度
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：任务计划 INV-1 / INV-2 / TASK-003 / TASK-005；proposal 引用
- **摘要与证据**：
  1. INV-1「原型与 Spec 冲突时以 Spec 为准并上报」与 TASK-002「以 `mkv3.py` 的补丁为准逐字落地」优先级相反，执笔席可以读成原型至上。
  2. INV-2「文档面只限 CHANGELOG、standards 三处计数与发布同步面」与 TASK-001「号写进 proposal」冲突；proposal 由 `fill.py` 从 `proposal-template.md` 生成，改 proposal 应改模板再重生成，计划没说，手改会让二者漂开。
  3. TASK-003 / TASK-004 的 deliverable 写「由脚本生成」，没点名脚本、没说放哪。TASK-005 没有任何审查清单（KM-7 要补的 What 7 核对属于这里）。
  4. proposal Why 表引的 `E12` 没给路径，它在另一个变更的 notes 里：`.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/evidence/E12-base-real-traffic.txt`。放宽面写的「超过 4 KB 的真实命令里，整串模式靠 credit 放行的有 71 条」引自 E11，而 E11 的 71 条是「R1 闸门新拦的 86 条里归 a-credit 类的」，不是全部 > 4 KB 命令里靠 credit 放行的总数，口径应写成下界。
  5. proposal 正文还有 17 处审计簇编号（`R2-A1`、`TL2-F7`、`KM-F-01` 等），头部「编号约定」没有说明它们的含义；`dispositions.md` 说「审计叙事搬出 proposal」，与现状不完全相符。
- **建议**：逐条消歧；在编号约定里加一句「R2-A# = post_spec R2 汇总簇号，XX-F-# = 各席原始编号」。

#### KM-15　新文本里 68 处裸 `#n`，与 standards §4.4 规则 1 冲突
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：proposal v3（头部 `:22` 及全文）、detailed-tasks.yaml、dispositions.md
- **证据**：`standards/conventions/content-integrity.md` §4.4 规则 1（2026-09-13 起生效，owner 裁定）：跨仓一律写 `<org>/<repo>#<n>`，新写或本次改动到的文字按此写。proposal 头部却反过来立了约定「裸写的 `#n` 指 `10CG/aria-plugin#n`」。`check_bare_issue_refs.py` 对三个文件的计数：proposal 50、detailed-tasks 16、dispositions 2。危害已在 KM-1 里落到实处：主仓里存在同号的 `Aria#217`、`Aria#229`、`Aria#230`，且 open、含义不同。§4.4 同时说明该工具不是闸门，Spec 不得把「整份文件 rc 0」写成验收门槛，所以这里不要求验收，只要求新文本按规则写。
- **建议**：新文本改全限定（可脚本替换，注意 `Rule #N` 豁免）；删去头部的反向约定。

## Verdict

**PASS_WITH_WARNINGS**（0 Critical，9 Major，6 Minor）。

本席没有发现会造成安全退化或让计划做不出来的问题。9 个 Major 里，KM-3 的「基线红」排序和 KM-8 的验收缺项最影响实现与验收的可信度；KM-1、KM-2 是外发动作的授权与误关风险，落地前必须钉死；KM-4、KM-9 是「决定了却没人接」的类型，前科（v1.76.1 漏 standards 计数）说明它们会真漏；KM-5、KM-6、KM-7 是 Rule #6 substitute、测试区分力和注释同步的口径问题。建议在下一版计划里一并吸收，再决定是否需要第 2 轮。

## 轮次记录

- **读了**：任务书；`detailed-tasks.yaml` 全文；`proposal.md` 全部 496 行；`dispositions.md`；`v3/README.md`；`skill-benchmark-exemption.md` 全文；WP-A `proposal.md` 的 `rule6_note` 与相关节；aria `CHANGELOG.md` 的 v1.77.1 / v1.77.0 / v1.76.1 / v1.75.0 条目；hook 的头注释、W10 常量与 `_sg_vx_collect` / `_sg_emit_blocked` 相关段；套件头部、21a* 说明块、`wpa_x_*` 助手、SC-13；`.aria/state-checks.yaml` 的版本类检查；`standards/conventions/secret-hygiene.md` 的三处计数与版本史；`content-integrity.md` §4.4；`.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`；`post_spec-R2-…-aggregated.md` 的 owner 裁定段；`openspec-archive/SKILL.md` Step 7；`lib/collision.py` 的 `normalize_linked_issue`；主仓与 aria 的发版提交的文件清单。
- **跑了**（全在 scratch，加 `taskset -c 0,1 nice -n 19`）：`mkv3.py` 重生成原型并与 `W8-v3.diff` 比对；`fill.py` 重生成 proposal 并 `cmp`；`commentsync.py` baseline / target 两种模式；`run-w10-w11.sh`（拷贝副本，33 s）；`w10b.sh`（18 s）；`finding_vs_longline.sh`；`check_bare_issue_refs.py`；`parse_detailed_tasks`；若干统计脚本。Forgejo 只做 GET：`aria-plugin` 的 #217、#228（含评论）、#216（含 timeline）、#139、#142、#229、#230、#219、#154、#203 与 open issue 列表，`Aria` 的 #217、#228、#139、#142、#229、#230。
- **没读**：其他席位的 post_planning 报告；真实命令语料。
- **没跑**：`run-w9.sh`、`run-w12*.sh`（任务书禁止）；全套件（所以 825、11 对 17 都是推断）；bash 3.2.57 的任何实验。
- **未核实**：GitHub 侧的同号 issue 与提交关键词行为；本 Forgejo 实例上跨仓提交关键词是否关闭 issue（需要写操作）；`secret-hygiene.md` 是否在其他位置也有陈旧计数（只核了 `:23/:316/:352`）；进程组、准入门、时间上界等机制正确性（归 backend 席）。
- **工具调用**：约 110 次（含失败一次：会话自带的旧版 secret-guard 拦下了一条同时 grep 配置文件的命令，已拆开重跑，没有用 `# guard:ack`）。
