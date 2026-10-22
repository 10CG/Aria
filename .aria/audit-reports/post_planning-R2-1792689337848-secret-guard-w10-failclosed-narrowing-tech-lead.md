---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T18:55:34.335Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — tech-lead 席（10CG/aria-plugin#217，secret-guard-w10-failclosed-narrowing v3.1）

审查对象：`detailed-tasks.yaml` v3.1（主仓 `95cf1de7`）及其依据 `proposal.md` v3.1、原型 `v31/W8-v31.diff`（本席用 `mkv31.py` 重新生成，sha256 前缀 `9f61db0e7b8b`，与 W8 逐字一致）、可执行验收 `v31/sc-cases.sh` / `v31/sc-direct.sh`。本席侧重设计与计划层：Decision 14–16、INV-1–INV-9、任务顺序、owner 门与对外动作、阶段 C / D；同时按任务书做了非作者变异测试。

实验脚本与结果都在 scratch 目录 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r2/tech-lead/`（下文简称 `TL/`）。凭据形路径一律在 `TL/probes*.py` 里运行时拼装，本报告不写字面。

## 审计结论

结论：**0 Critical / 8 Major / 10 Minor**。原型在本席检查的主路径上是对的（bash 5.2.15、5.0.18 各一整轮 94/94；本席的定向探针上原型都按设计拦）。问题集中在三处：验收用例抓不住几类像真实执笔错误的坏实现（其中 5 个带安全后果）；放宽面申报漏了两类既有 W10 缺口；任务计划里有几处自相矛盾或无法证伪的验收（What 6 对 W8、证据被自己覆盖、standards 计数、对外动作的 owner 门）。

### TL2-1 for 语句计数上限在重跑里没有用例（坏实现 TL-M1 存活，带安全后果）

- type: issue｜severity: **Major**｜category: testing｜针对：**验收用例 / 证据**｜复发：PP1-A1（同一条轴）、PP1-A6（「修一处、漏兄弟位置」）
- scope：`v31/sc-direct.sh:128-138`（V9-C1 / V9-C2）、`v31/sc-cases.sh:92`（V9-E10）、`v31/shapes.py:22`（count-axis 是第 9 个**引用**）、proposal P9（`proposal.md:536`）、`v31/mutants.py` BI-17
- 摘要：What 2 / Decision 14 在重跑里取消了三个计数上限（16 个赋值、8 个 for、每变量 8 次替换），P9 的用例只覆盖赋值（V9-C1）与引用（V9-C2、V9-E10）；for 语句上限 `cf` 在重跑里没有任何用例。只漏改 `cf` 的坏实现 94 条全绿，而它在大命令里放行「藏在第 9 个 for 里的凭据读取」。
- 证据：`TL/mut/TL-M1.sh`（原型 `v31.sh:643` 的 `ca=1000000 cf=1000000` 改成 `ca=1000000`）；`TL/mutres-TL-M1.txt`：PASS 94 / FAIL 0。探针 `count-axis-for9`（`TL/probes.py`）：基线 rc 2（过大）、原型 rc 2（longline）、TL-M1 **rc 0**；对照 `count-axis-for1-ctl` 三者都拦。作者的 BI-17 一次撤掉全部三处放宽，所以抓不住「只漏一处」。
- 建议：`sc-direct.sh` 加 V9-C3（重跑里 9 个以上 for 全部收集；基线那一遍仍是 8）；e2e 加 V9-E10b（读取在第 9 个 for 里 → 拦）；`mutants.py` 把 BI-17 拆成三个各漏一处的坏实现，各自绑定指定用例。

### TL2-2 裁定 C（超长行不评估脱敏过滤）只被很弱地钉住，三个笔误全部存活

- type: issue｜severity: **Major**｜category: testing｜针对：**验收用例 / 证据**｜复发：PP1-A10（部分）
- scope：`v31/sc-cases.sh:45-48`（`kind()`）、`:97`（V7-E14）、`v31/sc-direct.sh:151-155`（V10-N2 / N4）；proposal P7、P10
- 摘要：裁定 C 只被直调 V10-N2 / N4 与一个**不带过滤器**的 e2e（V7-E14）钉住。三个像真实执笔错误的坏实现全部存活：TL-M2（整串分支调用 `_sg_vx_big_judge` 后漏了 `return $?`，落到带 credit 的普通判定）、TL-M3（只改了整串那处，分段副本不经 `_sg_vx_big_judge`）、TL-M4（量行长的 `read` 漏了 `IFS=`，前导空白不计入行长）。三者在「超长行 + 脱敏过滤」的输入上都放行；TL-M2、TL-M4 再叠加 `10CG/aria-plugin#139` 的整串 credit，bash 实际会读出凭据。
- 证据：`TL/mutres-TL-M2.txt`、`-M3`、`-M4`：均 PASS 94 / FAIL 0。探针（`TL/probes.py`）：`C-whole-filter-elsewhere` 基线 2 / 过大、原型 2 / longline、TL-M2 **0**；`C-segment-filter` 原型 2 / longline、TL-M3 **0**；`C-whole-leading-blanks` 原型 2 / longline、TL-M4 **0**。TL-M2 在 V7-E14 上把 longline 与普通命中两份文案都写出、rc 2，`kind()` 先匹配 `has a line longer than`，于是判为 longline 过关。
- 建议：加三条 e2e，期望都是 rc 2 + longline：整串超长行 + 别处 `>/dev/null`；分段超长行 + 同段 `| wc -c`；前导空白撑长的行 + 过滤器。outcome 类断言再加一条「stderr 里恰好一个 `[secret-guard] BLOCKED` 头」。

### TL2-3 放宽面申报漏了两类既有 W10 缺口：基线拦、v3.1 放行、bash 实际会读出凭据

- type: issue｜severity: **Major**｜category: architecture｜针对：**proposal v3.1**｜复发：PP1-A20 的延伸（放宽面要列全）
- scope：R-a（`proposal.md:541`）、CHANGELOG「放宽面申报」（`:665`）、残余 1–7（`:548-556`）、hook 头注释的 W10 缺口清单（原型 `v31.sh:87-97`）
- 摘要：下面两类 W10 代入语义的既有缺口既没有 issue，也不在 R-a、CHANGELOG 或 hook 头注释的清单里，v3.1 把它们带到了大命令上：
  1. **重复赋值，首值胜出**：同名变量先后赋两个值时，`_sg_vx_apply` 按收集顺序先用第一个值把全部引用换完，后一个值从不代入；bash 里读到的是后一个值。
  2. **分段模式下值里的引号元字符被代入成语法**：`G='| jq keys'` 一类的值代入读取段的副本后，副本里出现了过滤器，于是该段得到 credit；在 bash 里它们只是 `cat` 的三个参数，文件内容照常输出。这一类不属 `10CG/aria-plugin#139`：#139 说的是整串模式里命令别处的过滤器字面；这里是分段模式，读取段自己的文本里没有过滤器。
  两类在小命令上基线同样放行（既有缺口），在大命令上基线按尺寸拦、v3.1 放行。
- 证据（`TL/probes.py`、`TL/probes2.py`、`TL/probes4.py`，`TL/probe-run.sh`）：`reassign-small` 基线 0；`reassign-big`、`reassign-big-multiline` 基线 2 / 过大，原型 **0**。`seg-splice-small` 基线 0；`seg-splice-big` 基线 2 / 过大，原型 **0**；对照 `seg-noval-big-ctl`（同形、没有 G）原型 2 / 普通命中，说明放行正是来自代入进去的过滤器。本席还试过整串模式下的拼接、以及「第 9 个引用之后的 `>/dev/null`」：核实为 #139 一类（赋值里的过滤器字面本身就给整串 credit，`rev9-small` 基线也放行），已申报，不计入本条。在 Forgejo 上按 `reassign` 搜没有结果；中文关键词的搜索不可用，所以「没有对应 issue」没能穷尽核实。
- 建议：不改设计（裁定 A 的字面就是按现有语义判）。在 R-a、CHANGELOG 放宽面申报与 hook 头注释里点名这两类；TASK-001 的上呈清单加两张残余 issue（或并入已有 issue）；TASK-007 的对账评论列出。定级说明：R-a 有一句通用的「判定语义上的既有缺口覆盖到更多大命令」，裁定 A 也覆盖这一类，所以本席定为 Major；若主控认为这句通用句不构成申报，那么按任务书第 4 条，这条应升为 Critical。

### TL2-4 What 6 与 INV-1、TASK-004 的 W8 验收互相矛盾：正确实现上必红

- type: issue｜severity: **Major**｜category: implementation｜针对：**任务计划**｜复发：PP1-A38（INV-1 有两种读法）的延伸
- scope：`detailed-tasks.yaml:31`（INV-1）、`:74`（TASK-002 What 6）、`:113`（TASK-004 W8 验收）；`proposal.md:137-139`（「W8 的原型不含这一删」）
- 摘要：What 6 删掉 `:666` 那一行，是计划内的逻辑改动，而原型 W8 不含这一删。INV-1 要求「逻辑与注释逐字落地、只重锚行号」，没有给 What 6 留例外；TASK-004 的 W8 验收「实现相对原型的差只有行号漂移、没有内容差」在正确实现（含 What 6）上必然变红。执行者只有两条路：违反这条验收，或者临场认定「What 6 不算」——后者正是 Rule #10 所说的临场豁免。另外，B.1 时 aria `hooks/` 与基线零差异，正常情况下连行号漂移都不会出现，「只重锚行号」这个前提本身也不成立。
- 建议：在 INV-1 与 TASK-004 的 W8 验收里写明唯一允许的内容差就是 What 6 那一行（给出期望 diff 的字面）；或者给 `mkv31.py` 加一个可选的 What 6 步骤，TASK-004 用它生成对照。

### TL2-5 TASK-004 的命令会覆盖它自己验收要对照的「原型那一轮」证据

- type: issue｜severity: **Major**｜category: testing｜针对：**任务计划 + 证据脚本**｜复发：PP1-A16（比较的两边变成同一份）、PP1-A39
- scope：`detailed-tasks.yaml:33`（INV-2）、`:45`（INV-8）、`:108`、`:113-118`；`v31/run-evidence.sh:5`、`:17-19`、`:28`、`:36`
- 摘要：TASK-004 用 `IMPL=… run-evidence.sh` 重新生成证据，脚本每个阶段成功后都把 W8 / W13 / W11 / W12 / W9 复制回 `v31/`，原型那一轮就被覆盖了。可 TASK-004 的四条验收都要与「原型那一轮」比较：W13 的基线红集、W9 的逐条断言、W11 的结局、W12 的放行数。比较对象从工作树里消失，只能去 git 历史取，计划没写；若直接拿工作树里的文件比，就成了实现那一轮自己比自己，恒绿。另外三处不一致：INV-2 只允许 `.aria/notes/…` 下的「新文件」，与 TASK-004 交付「v31/ 下的新版本」直接冲突；INV-8 说每份输出的首行都记两个 sha256，但 W8 阶段（`run-evidence.sh:17`）不写页眉；脚本头注释说 never overwrites committed evidence，实际只是在失败时不覆盖。
- 建议：TASK-004 的输出写到 `v31/impl/`（或命名为 `W*-impl.*`），验收写死对照对象是 `git show 95cf1de7:<路径>`；INV-2 加上 `v31/impl/`；W8 阶段补页眉，或在 INV-8 里写明 W8 例外。

### TL2-6 搬进套件的用例从不经坏实现验证；TASK-003 补的用例没有确定落点

- type: issue｜severity: **Major**｜category: testing｜针对：**任务计划**｜复发：PP1-A7 的延伸
- scope：`detailed-tasks.yaml:75`、`:80-84`（TASK-002）、`:93-100`（TASK-003）、`:111-114`（TASK-004）；`v31/run-evidence.sh:19-27`
- 摘要：23 个 BI 只在 `v31/sc-cases.sh` 上跑（TASK-004 的 W13），搬进 `secret-guard.test.sh` 的那一份从不在坏实现上跑。TASK-002 对移植的唯一检查是「新套件对基线的红集与 W13 第 2 节一致」，而基线上那些新函数根本不存在：一条移植时被削弱的用例在基线上照样红，在坏实现上却可能是绿的。留在仓里、守护后续改动的是套件，不是 notes 里的脚本。另外，TASK-003 发现缺口要「补用例」，没说补在套件还是 `v31/sc-cases.sh`：补在套件，TASK-004 的 W13 看不到；补在 `sc-cases.sh`，又违反 INV-2 的「只许新文件」。本席的 10 个坏实现里有 7 个存活，TASK-003 一定会走到这条路径。
- 建议：TASK-004 加一条验收：对 BI-1–23 与 TASK-003 的坏实现，在套件上按用例编号过滤、跑移植后的指定用例，全部变红。TASK-003 补的用例同时进套件与 `v31/sc-cases.sh`，INV-2 为此开口。

### TL2-7 对外动作的上呈清单不全（feature 分支推送、PR、#217 对账评论与关闭、owner 的上线动作）

- type: issue｜severity: **Major**｜category: documentation｜针对：**任务计划**｜复发：PP1-A22（部分）
- scope：`detailed-tasks.yaml:61`（TASK-001 清单 a–g）、`:140-147`（TASK-006）、`:161-162`（TASK-007）、`:41`（INV-6「每次推送前」）
- 摘要：TASK-001 上呈的只有残余 issue、载体与两条留言。计划里另有一批对外动作没有 owner 门：aria（以及主仓）的 feature 分支推送；PR 的创建；TASK-007 在 `10CG/aria-plugin#217` 上的对账评论，以及经 API 的关闭；TASK-003 / 004 的证据提交到主仓时走哪条推送路径（直推 master 还是 PR）；TASK-007 依赖 owner 亲手更新插件缓存并重启会话。先例 WP-A（`openspec/changes/secret-net-l3-and-bypass-paths/proposal.md:12`，owner 2026-09-30 第 4 项）把「feature 分支推送、开 PR、issue 评论、issue 关闭」列为需要 owner 一次性授权的四类，把「合并到任一 master（含子模块本地 merge 后的推送）、推 master、tag 与发版、主仓 PR 合并、删远端分支」列为逐次请示。本 Spec 的 TASK-006 只写了「owner 授权（版本号与发版时点）」，没有逐项列出。本席在 `.aria/decisions/` 里没有找到本 Spec 的常设授权。
- 建议：TASK-001 的 AskUserQuestion 照 WP-A 先例分两组上呈：一次性授权的四类、逐次请示的五类；TASK-006 / 007 的验收引用这次决定；TASK-007 里 owner 要做的动作写进前置条件。

### TL2-8 standards 计数的验收命令命不中目标；`<N>` 一个占位符指两个量

- type: issue｜severity: **Major**｜category: documentation｜针对：**任务计划 + proposal（CHANGELOG 草稿）**｜复发：PP1-A23（修法不生效）
- scope：`detailed-tasks.yaml:141`、`:148`；`proposal.md:664`、`:668`；standards `conventions/secret-hygiene.md:23`、`:316`、`:317`、`:352`
- 摘要：TASK-006 的验收命令 `grep -n 'cases' standards/conventions/secret-hygiene.md` 只命中 `:316`，外加 `:317` 的 secret-scan「129 regression cases」；命不中 `:23`（写的是「822 self-tests [816 无 zsh]」）和 `:352`（「822 self-test」）。`:23` 与 `:316` 各自还有第二个数（无 zsh），「都等于 N」没有覆盖。照字面执行，要么因为 129 ≠ N 恒红，要么只核到三处里的一处，另两处的陈旧值永远核不出来。另外，CHANGELOG 草稿里的 `<N>` 既指放行条数（`:664`），又指测试例数（`:668`），而 TASK-006 只给了 `<N>` 一个取值来源，机械替换会把放行数写进测试数。
- 建议：验收改为按行号核对三处的两个数（含 zsh 与不含 zsh），数值取自 TASK-006 在待发版 SHA 的 git 检出里现跑的结果，而不是 TASK-002 时的数（TASK-003 可能还会加用例）；占位符改名为 `<N_allowed>`、`<N_cases>`、`<n_new>`。

### TL2-9 「没有残留进程」的两条用例数的是全机进程：同机并发运行时，正确实现会假红（已实测）

- type: issue｜severity: Minor｜category: testing｜针对：**验收用例**
- scope：`v31/sc-direct.sh:80-81`（V5-S13b）、`:108-110`（V5-S12）
- 摘要：两条用例用全机 `ps -eo args` 按 `sleep 7.777` 等精确参数计数，数到的是本机所有用户、所有并发运行的进程。同机另有一份套件在跑时（另一个审计席、TASK-003 与 TASK-004 并行、CI 并行），对方的同名桩会让正确实现假红。套件搬进仓后，这个问题跟着进仓。
- 证据：`TL/conc-demo.txt`：起两个与桩同参数的替身进程（模拟并发运行），然后在原型上跑 `SC_ONLY='V5-S1[23]'`：V5-S13b FAIL（数到 1），V5-S12 FAIL（数到 2）；当时负载 2.40。
- 建议：桩的参数带上本轮唯一的后缀（例如小数位编码运行 id），或者按本轮的进程组 / 会话过滤。

### TL2-10 计时窗口与「逃生口」：可能假红的、claim 没钉住的，以及两个非安全存活者

- type: risk｜severity: Minor｜category: testing｜针对：**验收用例**
- scope：`v31/sc-cases.sh:68-73`、`:85`、`:98-104`；hook `_sg_over_budget`（基线 `:616-617`）
- 摘要：
  - (a) V3-E5（预算 1）：父进程那一遍的整秒检查点 `SECONDS - _SG_T0 >= 1` 只要碰巧跨过秒界，就会写出时间文案，与基线臂（默认预算）的「过大」字节不同，正确实现因此假红。概率约为父进程 collect 耗时 / 1 s，负载越高越大。这是推算，未复现。
  - (b) V7-E15 接受「放行，或基线字节」两种结果，「credit 路径总是超时」的坏实现也能过关，用例名声称的「credit 照常」并没有被钉住。
  - (c) deadline 类窗口的上沿只留 0.6 s 余量，用来吸收进程启动与收尾，而这两项随负载变化。W13 是在负载 1.3–2.5 下取得的；本席在负载 4.7–5.5 下跑了两轮（bash 5.2.15、5.0.18），都是 94/94；负载 9–10 下未测。
  - (d) 两个没有安全后果的坏实现存活：TL-M5（重跑里分段那处检查点仍写出时间文案，违反 P6 的逐字节回落）、TL-M9（LMAX 判据误写成 `>=`）。
- 建议：V3-E5 的基线臂也带 `SECRET_GUARD_TIME_BUDGET_S=1`，或者把时间文案也算作可接受的回落；V7-E15 换成「必须放行」的确定形状；加 LMAX 8192 / 8193 的边界用例，再加一条把 `_sg_over_budget` 打桩、在重跑里触发真实检查点的用例。

### TL2-11 准入门的「从 stdin cwd 取项目根」没有用例（坏实现 TL-M8 存活，会绕过扩展）

- type: issue｜severity: Minor｜category: testing｜针对：**验收用例**
- scope：`v31/sc-direct.sh:42-46`、`v31/sc-cases.sh:53`、`:90`
- 摘要：扩展探测只用 `CLAUDE_PROJECT_DIR` 测过。`_sg_ext_root` 的另一条路（没有该变量时取 stdin 里的 `cwd`）没有用例；e2e 又全部 `env -u CLAUDE_PROJECT_DIR`，输入也不带 `cwd`，走的都是「找不到项目根」，而生产里实际走的是「有根、没有扩展文件」（这一条只有直调 V2-G4 覆盖）。坏实现 TL-M8（项目根只取 `CLAUDE_PROJECT_DIR`）94 条全绿；对于只能从 stdin `cwd` 得知的扩展项目，它放行了读取扩展所列路径的大命令，原型则照基线拦。生产里 Claude Code 会设置 `CLAUDE_PROJECT_DIR`，所以暴露面窄。
- 证据：`TL/mutres-TL-M8.txt` PASS 94；探针 `ext-via-cwd`：基线与原型 rc 2（过大），TL-M8 **rc 0**。
- 建议：V2-G4 加 `cwd` 变体；e2e 加一条 identity 用例：输入带 `cwd`、不设 `CLAUDE_PROJECT_DIR`、项目有扩展。

### TL2-12 Decision 14、15 技术上成立，没有改变姿态；剩两处细节

- type: decision｜severity: Minor｜category: architecture｜针对：**proposal v3.1 + 原型**
- scope：What 2（`proposal.md:79-80`）、Owner 通报第 1 条（`:571`）、Decision 14 / 15（`:708-709`）；原型 `v31.sh:630`、`:643`、`:689`
- 摘要：
  - Decision 14 成立：基线那一遍的计数上限本身是 fail-open（超出部分不看）；重跑里取消它，只会多收集、多代入。代价变大只会落到截止，然后回落拦截（裁定 B）；父进程里那一遍仍有上限，没有新增无上界的工作；放行只来自完整判定的结果，这正是裁定 A 的字面。
  - Owner 通报里「过滤器藏在第 9 个引用之后时 v3.1 放行，与小命令的判定一致」这一说法本席实测过：整串模式下，赋值里的过滤器字面本身就让小命令得到 credit（`rev9-small` 基线放行），说法成立。
  - Decision 15（退出码 77）成立：77 只会出现在 `_sg_vx_pass` 返回 0 之后；桩用例 V4-S11 / BI-19 能钉住裸 0。
  - 细节 (a)：「没有计数上限」其实是 1,000,000 的上限，到顶时静默止步，形状上又回到了 fail-open。3 s 内到不了这个数，但正确性不该依赖机器速度：到顶应返回 3，走回落。
  - 细节 (b)：「所有赋值都收集、所有引用都代入」不等于语义完整，见 TL2-3。
- 建议：把三处 `1000000` 改为「到顶即 `return 3`」，或者在注释与 What 2 里写明到顶时的行为；What 2 的措辞改为「重跑不再因计数止步」。

### TL2-13 Decision 16 按 bash 构建三元组判平台：WSL 与仿真内核会放宽；CHANGELOG 里「Windows 相同」的说法不准确

- type: risk｜severity: Minor｜category: architecture｜针对：**proposal v3.1 + 原型**
- scope：Decision 16（`proposal.md:710`）、CHANGELOG「放宽条件」（`:663`）；原型 `v31.sh:819-820`、`:827-835`
- 摘要：`*-linux-gnu*` 判的是 bash 的构建三元组，而机制真正依赖的是内核的进程组与 `/proc` 语义。WSL1（系统调用翻译层）、WSL2、gVisor 这类「跑 GNU/Linux 二进制、但内核没实测过」的环境都会放宽，所以 CHANGELOG 里「其他平台 (macOS / Windows / musl) … 行为与之前完全相同」对在 WSL 里运行的 Claude Code 不成立。自检只验证「自己是进程组组长」，不验证「整组 kill 真的生效」：如果某个仿真内核上组 kill 静默失败，截止就不存在，判定可以越过 5 s，结局是 fail-open。这一点没有实测，属于风险。
- 建议：CHANGELOG 写明 WSL 视同 Linux；或者按裁定 E 的原则，在 `/proc/sys/kernel/osrelease` 含 `microsoft` 时不放宽。在残余 6 里记下「运行时自检组 kill 是否生效」的思路。

### TL2-14 rule6_note 块 B 落在「拿不准」格，却按「先豁免、待 owner 复议」处理

- type: decision｜severity: Minor｜category: documentation｜针对：**任务计划 + proposal**｜复发：PP1-A19（部分）
- scope：`detailed-tasks.yaml:19-26`（块 B）、`proposal.md:574`、`:667`；SOT `standards/conventions/skill-benchmark-exemption.md` §2 第 4 行、§3、§4
- 摘要：块 B 自己点名了一处行为变化：大命令现在可能看到普通命中文案，其中含「Acceptable filters」与 `# guard:ack` 指引。它同时标了「AI 自作主张、待 owner 复议」，暂按第 1 行处理。这正是 SOT 的「拿不准」格，那一格的处置是「照跑」，不是「先豁免、等复议」。hook 文案 AB 结构上测不到，诚实的落点是第 3 行的三件套：行为已经点名；V7-E13 / V7-E14 就是可证伪的定向 fixture（BI-12 / BI-10 能把它们打红）；只差一张「AB 套件不覆盖 hook 文案」的 issue（本席没找到现成的，`10CG/aria-plugin#225` 讲的是别的缺口）。把这项归类推给 owner，也不符合「技术级由 AI 直接裁」的分工；而 CHANGELOG 草稿里的「待 owner 复议」会随发版永久留在用户可见的文字里。
- 建议：块 B 改按第 3 行处理并附上 issue 链接；删掉 CHANGELOG 里的「待 owner 复议」。

### TL2-15 INV-7 没有上限也没有升级路径；TASK-003 的耗时矩阵不受 INV-7 约束

- type: risk｜severity: Minor｜category: architecture｜针对：**任务计划**｜复发：PP1-A36（部分）
- scope：`detailed-tasks.yaml:43`（INV-7）、`:97-100`（TASK-003）
- 摘要：INV-7 规定开始或结束时任一负载读数 ≥ 2 就作废重跑，但没有次数或时间上限，也没有升级路径。本机今天连续数小时负载在 7–10 之间（本席开工时 9.13，写报告时 9.28），W12 第 1 节可能一直做不成。TASK-003 的对抗耗时矩阵（ε = 0.3 s）不受 INV-7 约束，在高负载下会假红，或诱使执行者临场放宽判据。
- 建议：INV-7 加一条：N 次或 T 小时内取不到低负载窗口，就附上当时的负载读数上报 owner；TASK-003 的耗时矩阵纳入 INV-7。

### TL2-16 阶段 C 的顺序没有写死

- type: issue｜severity: Minor｜category: architecture｜针对：**任务计划**
- scope：`detailed-tasks.yaml:138-145`（TASK-006 design）
- 摘要：主仓的 gitlink bump 必须排在 aria 与 standards 各自双推、并逐个 `ls-remote` 核验之后，CLAUDE.md 约束 1 讲的孤儿 gitlink 正出在这一步；计划只把「双推后核验」写成一条并列要点。aria 的合并开不开 PR、Rule #8 的 C.2.4 是否适用，计划也没写：aria 没有覆盖 `hooks/` 的 CI，按路径覆盖规则 (a) 会是 not_applicable，但 (b) 仍然要查。
- 建议：TASK-006 改写成编号步骤：aria 本地合并 → 双推 → 两边 `ls-remote`；standards 同样三步；然后主仓 bump → 推送或开 PR → C.2.4 → `ls-remote`。

### TL2-17 上线后复验：没要求惰性诱饵，「跑」有两种读法，也没有缓存新鲜度探针

- type: issue｜severity: Minor｜category: architecture｜针对：**任务计划**
- scope：`detailed-tasks.yaml:161`、`:165`（TASK-007）；`v31/shapes.py:8`、`:22`；WP-A `proposal.md:388`（plugin-cache-currency 探针、惰性诱饵）
- 摘要：
  - 上线后复验用 count-axis（期望拦），它读的是 Forgejo 配置路径，在真实部署里可能存在。复验要测的恰恰是「hook 可能没拦」，所以这项复验失败时的后果就是在会话里读出真凭据。计划没要求先断言该路径在复验主机上不存在：本机上不存在，本席只核了存在性、没读；但计划里没写这一步。
  - 「各跑一次」有两种读法：AI 经 harness 发出 Bash 调用，或者直接执行插件缓存里的 hook。
  - 计划也没有 WP-A 那样的插件缓存新鲜度探针（`.aria/probes/plugin-cache-currency.py`），无法确认生效的是新版。
- 建议：写明三点：经 harness 发出调用；先断言诱饵路径不存在；先跑缓存新鲜度探针。

### TL2-18 「搬入 shapes.py 的输入」有两种读法；套件头注释会因此失实

- type: issue｜severity: Minor｜category: documentation｜针对：**任务计划**
- scope：`detailed-tasks.yaml:75`；套件头注释 `aria/hooks/tests/secret-guard.test.sh:5-7`
- 摘要：「shapes.py 的输入随之搬入 tests/ 下」可以读成把 Python 生成器搬进去，也可以读成改写为 bash 生成。若搬 Python，套件头注释里「python3 只给 #128 SC-20 用，no other case depends on it」就失实了；这句不在 What 7 的封闭清单里，commentsync 也查不到。另外，`shim/jq`、`shim/sed` 是指向 `delay-first` 的符号链接，搬进仓时要说明是否保留符号链接。
- 建议：写明取哪种读法；若搬 Python，把那句头注释列入 What 7 的清单。

### 核过、未成问题的几项（供汇总参考）

- 原型可复现：`mkv31.py` 在当前 aria `hooks/` 上生成成功（基线 sha256 前缀 `e83c5e30f2cc`），与 W8 逐字一致。commentsync 的 baseline 模式在基线 hook + 套件上为 GREEN；target 模式在「原型 + 未改的套件」上为 RED 22 项，符合预期，因为套件要到 TASK-002 才改写。
- shim 的注入位置属实：基线里 `jq` 的首次执行是 `:1003` 的 stdin 解析（`:931` 的 `command -v jq` 是内建，不执行 jq），在锚点之后；sc-cases 的输入不带 `cwd`，所以 `_sg_ext_root` 不会提前调用 jq。`sed` 的首次调用落在作业里的 `_sg_redact_echo`。这依赖 INV-1 的逐字落地：实现若在触发点之前调用 sed，deadline 类用例会假红（10 s 延迟落进父进程）。
- 期望值随 `SC_BASH` 而定的逻辑（`sc-cases.sh:25-26`）与 hook 的准入门同一判据，3.2 走 identity，是对的。
- 归档门（`aria/skills/state-scanner/scripts/lib/spec_complete.py`）：本 Spec 没有 `tasks.md`，yaml 只检查任务标题里的集成类关键词（含 `hook`）；7 个标题都不含，所以全部置为 done 后 `d_payload` 为 null。TASK-007「先置 done、否则会自动建 tracker」的说法成立。

## 变异测试

方法：每个坏实现 = 原型 + 一处改动，由 `TL/mkmut.py` 生成，每处替换都断言恰好命中一次。运行前，本席先把设想与预期写进 `TL/prereg-mutants.txt`：第一段写于读用例之前，第二段写于读完用例与 `mutants.py`、跑坏实现之前，并去掉了与作者 BI 重复的项。然后用 `bash 5.2.15` 在每个坏实现上跑一整轮 `sc-cases.sh`（`TL/run-mut.sh`，串行，每轮约 46 s，负载 1.1–3.3，见 `TL/run-mut.log`）。有安全含义的，再用定向探针（`TL/probe-run.sh`）比对基线、原型与坏实现。

| 编号 | 坏实现（一句话） | 改动（原型 `v31.sh` 行） | 预先写下的预期 | 实际（94 条） | 定向探针上的后果 |
|---|---|---|---|---|---|
| TL-M1 | 只放开赋值上限，漏了 for 上限 | `:643` 去掉 `cf=1000000` | 存活（没有 for 计数用例） | **存活**，FAIL 0 | `count-axis-for9`：原型拦，坏实现**放行**（凭据读取） |
| TL-M2 | 整串分支调 `_sg_vx_big_judge` 后漏 `return $?` | `:750` | 存活（V7-E14 没有过滤器；`kind()` 先认 longline） | **存活**，FAIL 0 | `C-whole-filter-elsewhere`：原型 2 / longline，坏实现**放行**（叠加 #139，读出凭据） |
| TL-M3 | 分段那处没改（只改了整串） | `:778` 改回 `_sg_judge_one "$_SG_SUB" segment` | 存活 | **存活**，FAIL 0 | `C-segment-filter`：原型 2 / longline，坏实现**放行**（违反裁定 C） |
| TL-M4 | 量行长的 `read` 漏了 `IFS=` | `:797` | 存活 | **存活**，FAIL 0 | `C-whole-leading-blanks`：原型 2 / longline，坏实现**放行**（叠加 #139，读出凭据） |
| TL-M5 | 重跑里分段那处检查点仍写时间文案（三处漏一处） | `:757` 删掉放宽分支的 `return 3` | 存活（只有桩 V4-S7） | **存活**，FAIL 0 | 无安全后果：仍是拦截，只是文案不再与基线逐字节相同（P6） |
| TL-M6 | `_sg_relax_run` 对 rc 2 不再要求有文本 | `:852` | V4-S3 抓住 | 抓住：仅 `V4-S3-block-without-text` | — |
| TL-M7 | 命令替换里漏了 `exec 2>/dev/null` | `:843` | V6-E2 等抓住（可能偶发） | 抓住：11 条，含 V6-E2、V3-E4、V3-E5、V2-E6、V3-S4、V5-S5（V3-E3 未红） | — |
| TL-M8 | 项目根只取 `CLAUDE_PROJECT_DIR` | `:824` | 存活 | **存活**，FAIL 0 | `ext-via-cwd`：原型 2 / 过大（= 基线），坏实现**放行**（绕过扩展） |
| TL-M9 | LMAX 判据误写成 `>=` | `:799` | 存活（没有边界用例） | **存活**，FAIL 0 | 更严的方向，无安全后果 |
| TL-M10 | 扩展探测用 `-f` 代替 `-e` | `:825` | `V2-G4-extension-path-is-a-directory` 抓住 | 抓住（只有这一条） | — |

结果：10 个坏实现的预测全部命中，3 个被抓住、7 个存活。存活的 7 个里，5 个有安全后果（TL-M1、TL-M2、TL-M3、TL-M4、TL-M8，见 TL2-1、TL2-2、TL2-11），2 个没有（TL-M5、TL-M9，见 TL2-10）。没有一个是「被无关断言碰红」的情形：被抓住的 3 个都是红在预先写下的用例上。

另做的放宽面探针（基线 / 原型，不涉及坏实现；见 TL2-3）：

| 探针 | 基线 | 原型 | 说明 |
|---|---|---|---|
| `reassign-small` | 0 | 0 | 重复赋值、首值胜出：小命令上是既有缺口 |
| `reassign-big`、`reassign-big-multiline` | 2 / 过大 | **0** | 大命令：基线拦，v3.1 放行；bash 读的是后一个值 |
| `seg-splice-small` | 0 | 0 | 分段模式，值里的元字符代入成语法：小命令上是既有缺口 |
| `seg-splice-big` | 2 / 过大 | **0** | 大命令：基线拦，v3.1 放行；对照 `seg-noval-big-ctl` 原型 2 / 普通命中 |
| `rev9-small`、`rev9-big`、`rev1-small` | 0 / 2 / 0 | 0 / 0 / 0 | 整串 + `>/dev/null` 字面：属 #139，已申报（用来核 Owner 通报第 1 条） |

## Verdict

**PASS_WITH_WARNINGS**：0 Critical、8 Major（TL2-1 至 TL2-8）、10 Minor（TL2-9 至 TL2-18）。

设计主线（基线先跑、准入门、硬截止作业、77、只在实测平台上放宽、取消重跑计数上限）技术上成立，没有改变 fail-open / fail-closed 姿态；原型在本席检查的路径上是对的。阻碍「照计划实现即可放心」的是三类问题：

1. 验收用例抓不住 5 个带安全后果的真实笔误（TL2-1、TL2-2），而且计划没有把坏实现验证延伸到移植进套件的用例上（TL2-6）。
2. 放宽面申报漏了两类既有缺口（TL2-3）。
3. 任务计划里有自相矛盾或无法证伪的验收：TL2-4、TL2-5、TL2-8；对外动作的 owner 门也不全（TL2-7）。

这些都可以在不改设计的前提下修掉。

## 轮次记录

- **读过**：任务书；`detailed-tasks.yaml` 全文；`proposal.md` 按节全文（What 1–7、参考实现部分、P 与放宽面、Owner 裁定点、Success Criteria、Impact、CHANGELOG 草稿、证据、Decision 1–18、Tasks）；`v31/W8-v31.diff` 全文；`v31/README.md`、`sc-cases.sh`、`sc-direct.sh`、`shapes.py`、`shim/delay-first`、`mutants.py` 全文；`run-evidence.sh` 的相关行；`dispositions.md` 的 post_planning R1 节；R1 汇总的簇表；SOT `skill-benchmark-exemption.md` 全文；WP-A proposal 的授权段与 rule6_note 段；基线 hook 的 `:170-200`、`:616-672`、`:760-775`、`:926-1060`；`spec_complete.py` 归档门相关段；standards `secret-hygiene.md` 的计数行。
- **跑过**：
  - `mkv31.py`：原型 sha256 前缀 `9f61db0e7b8b`，与 W8 一致。
  - `sc-cases.sh` 原型 × bash 5.2.15：94 / 0，47 s，负载 4.85 → 4.66（`TL/run1-proto-52.txt`）；原型 × bash 5.0.18：94 / 0，负载约 4–5.5（`TL/run2-proto-50.txt`）。
  - 10 个坏实现各一整轮（`TL/mutres-TL-M*.txt`）。
  - 定向探针：基线、原型与相关坏实现（`TL/probes*.py`）。
  - `commentsync.py` 的 baseline 与 target 两种模式。
  - 并发假红演示（`TL/conc-demo.txt`）。
  - 两次只读的 Forgejo 查询（issue 搜索、`#225` 标题）。
  - 本席记下的后台进程（PID 3766991、3854077、3833867、3833868、3837325、3837326）均已核实退出，没有按模式匹配杀过任何进程。
- **按任务书没有跑**：W9、W11、W12、W13 全量。bash 5.1.16、5.3.20、3.2.57 的整轮依赖 W13，未复跑。
- **未核实**：
  - 负载 9–10 下计时窗口是否假红：本席实测的最高负载是 5.5。
  - V3-E5 整秒检查点假红的实际概率：只是推算。
  - WSL1 / WSL2 / gVisor 上组 kill 与 `/proc` 的行为：没有环境。
  - TL2-3 的两类缺口是否已有 issue：Forgejo 的中文搜索不可用。
  - INV-6 的 grep 是否覆盖 URL 形式的关闭语法（`Closes https://…/issues/217`），以及 Forgejo 是否识别这种写法。
- **负载**：开工时 9.13；坏实现整轮期间 1.1–3.3；写报告时 9.28（另一席并发）。
- **工具调用**：约 75 次。
