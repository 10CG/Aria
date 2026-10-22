---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T06:52:04.120Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — code-reviewer 席（#217 secret-guard-w10-failclosed-narrowing）

审查对象：`detailed-tasks.yaml`（`8ee867d`）、`proposal.md` v3（`297b5cc`）、原型 `v3/W8-v3.diff`（基线 `aria/hooks/secret-guard.sh`，hooks/ 与 `59e333c` 零差异，已核）。
实验目录（下文简称 `$S`）：`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r1/code-reviewer/`。原型副本 `$S/v3.sh` 由 `mkv3.py` 生成，与 `W8-v3.diff` 逐字节一致。

先列已核实为对的（便于主控取舍）：

- `W8-v3.diff` 可由 `mkv3.py` 逐字节复现；`proposal.md` 与 `fill.py` 现跑输出逐字节相同。
- `run-w10-w11.sh`（在 `$S/v3copy` 复制件里跑，没有覆盖仓内证据）、`w10b.sh` 复跑：S1–S8、G1–G8 全 PASS，残留 0；W11 各形状结局与仓内 `W11-adversarial.txt` 一致；P6 两个回落输入逐字节相同；P10 成立。
- `commentsync.py` baseline 模式在基线上 GREEN（14 个退役短语各 1 次，10 个应出现词 0 次），target 模式对原型 RED（22 项），与 proposal 说法一致。
- P1「两个触发点之外与基线逐字节相同」在正常环境下确由结构保证：新行为全部挂在「`_SG_RELAXED` 非空」或「触发点上 `_sg_relax_ok` 成立」之后；`_sg_judge_one` 第三参数缺省、`longline` 分支只在 kind=longline 时进入。例外见 CR-03。
- 回落文案：作业的块文本经命令替换去尾换行再 `printf '%s\n'`，模板都以恰好一个换行结尾，所以与进程内输出逐字节相同；回落路径用存下的 `_SG_OV_PAT/_SG_OV_MODE`，与基线同一触发点同一原因串。
- 作业内部 job control 关闭，判定派生的子进程都在作业的进程组内（S5 证实）；作业被外部停住（SIGSTOP）时计时器仍按时整组 KILL（`$S/e7.sh`，1.00 s 返回 4），这一点没有问题。
- owner 门（版本号、发版）在 TASK-006，位于 TASK-004/005 之后，位置正确。

## 审计结论

### CR-01 — Major — 原型 / 证据（也涉及 proposal P5、SC-V5）

- type: issue；category: implementation；scope: `W8-v3.diff` `_sg_relax_run`（W8 第 151–159 行），proposal What 3、P5、SC-V5
- 摘要：作业正常退出、但留下一个仍持有命令替换管道的后代进程时，`_sg_relax_run` 会越过截止，并在截止之后采用作业的结论。原因是 `wait` 返回后只杀计时器组，不杀作业组。
- 证据：`$S/e1.sh`。桩 `_sg_vx_pass() { sleep 4.417 & return 0; }`，截止 1 s：原型 `rc=0 wall=4.42s`（放行，越过截止 3.4 s）；带文本拦截的变体 `rc=2 wall=4.42s`。现有 W10 S5 的桩是 `sleep 6.222 & wait`，作业自己活到截止，所以测不到这一类。
- 影响：真实判定代码目前不起后台进程，所以眼下的 hook 碰不到；但 P5「作业结束后没有残留进程、不占管道」并没有机制保证，只是靠「判定代码碰巧不起后台进程」。SC-V5 写的「后台子进程继承 stderr 并睡 6 s → 在截止 + 0.3 s 内返回 4」有两种读法：桩若 `wait`，测不出这一类；桩若不 `wait`（更自然的读法），用例在参考实现上就是红的，执笔席会卡在「逐字落地」与「套件全绿」之间。
- 建议：在 `wait "$jp" 2>/dev/null; r=$?` 之后加一行 `kill -KILL -- "-$jp" >/dev/null 2>&1`，再杀计时器。已验证（`$S/v3fix.sh`）：上面两个探针都在 0.00 s 返回（各自取作业退出码），S1–S8、G1–G8 全 PASS。SC-V5 改写成两个明确的桩：「后台子进程 + 作业等它」与「后台子进程 + 作业立即返回」，后者要求在截止 + 0.3 s 内返回，且事后残留为 0。新增一个 BI：「`wait` 之后不杀作业组」。

### CR-02 — Major — 原型 / 证据 + proposal What 3 + SC-V5、BI-3

- type: issue；category: implementation / testing；scope: `_sg_relax_run` 的 `[[ "$tp" != "$jp" ]] || { …; exit 99; }`，proposal What 3「计时器 fork 失败」那一条，SC-V5 的「删掉计时器那一行」变异，BI-3
- 摘要：计时器的 fork 检查在真实的 fork 失败下永远不会触发。bash 不会在 fork 失败后带着旧的 `$!` 回到脚本：遇到 EAGAIN 它先重试（共睡约 15 s），然后让命令替换子 shell 中止。作业此时已在自己的进程组里运行，没有计时器管它，父进程一直读管道读到作业结束。
- 证据：`$S/e3.sh` + `$S/v3forkfail.sh`（只在副本的命令替换里、计时器那一行之前插入 `ulimit -u 1` 作故障注入）。桩判定睡 21.6 s，截止 1 s：`rc=4 wall=21.62s`；stderr 出现 4 行 `fork: retry: Resource temporarily unavailable` 和 1 行 `fork: Resource temporarily unavailable`（也说明 CR-09 的重定向不起作用）。`tp == jp` 那一支始终没有执行。
- 影响：(1) proposal 的说法「`$!` 不变，`tp == jp`，立即杀掉作业并以 99 退出」与 bash 实际行为不符。SC-V5 的变异（删掉计时器那一行）和 BI-3 检查的是一个真实 fork 失败从不会出现的状态，在这一点上验收证伪不了。(2) EAGAIN 时基线自己的 fork（`_sg_emit_blocked` 里的 `$(_sg_redact_echo …)`）同样会重试约 15 s，两边都会超过 5 s，不算新退化。但若是不重试的 fork 错误（如 ENOMEM），基线在这一点会以「internal error」exit 2 拦下，而 v3 的作业会不受截止约束地跑下去。这一条是推理，未实测：本机无法构造 ENOMEM。
- 建议（已在 `$S/v3alt.sh` 验证）：计时器挪进作业里，放在组长自检之后：`local me=$BASHPID; ( sleep "$_SG_LEFT"; kill -KILL -- "-$me" ) >/dev/null 2>&1 </dev/null &`，然后再设 `_SG_RELAXED=1` 开始判定。这样计时器没起来，判定就不会开始。`_sg_relax_run` 里改为 `exec 2>/dev/null; set -m; _sg_relax_job … &; jp=$!; wait "$jp"; r=$?; kill -KILL -- "-$jp"; exit "$r"`。注意必须用组长自检之后的 `-$me`，不要用 `kill 0`：自检失败时 `kill 0` 会杀到 hook 自己的进程组。`v3alt.sh` 上 S1–S8、G1–G8、CR-01 的两个探针全过，W11 五个形状结局不变，P6 两个回落输入与基线逐字节相同。删掉 SC-V5 的「删掉计时器那一行」变异和 BI-3，或者改写成「计时器 fork 失败时不开始判定」。EAGAIN 下的整体停顿在残余里写明，基线也一样。

### CR-03 — Major — 原型 / 证据

- type: issue；category: implementation；scope: W8 全部 `${_SG_RELAXED:-}` 读点（W8 第 26、51、59、66、76、83、91、104 行，以及 `_sg_relax_ok`）
- 摘要：`_SG_RELAXED` 从未初始化，从环境继承来的值会在主进程里打开放宽规则，而且不受任何截止约束。
- 证据：在 `$S/work/adv` 用 `gen-v3.py` 生成的 `apply-heavy-cjk` 跑 e2e：不带该变量时 v3 `rc=2 wall=3.04s`（回落拦截），基线约 2.2 s 拦截；带 `_SG_RELAXED=1` 时 `rc=0 wall=17.73s`。在 Claude Code 里，这条命令会在 5 s 被杀，然后 fail-open。另外三个时间检查点会返回 3，经 `:1589` 打出「internal error (rc=3)」文案，所以环境里有这个变量时，P1 也不再成立。
- 影响与威胁模型：能改 hook 环境的人本来就能用 `BASH_ENV` 等手段绕过 hook，所以新增的攻击面有限。但 hook 自己的设计原则是不让环境变量关掉时间 fail-closed（基线 `:614` 预算封顶的注释），这里违背了它；测试套件里若有人 `export _SG_RELAXED=1`，也会污染后续的 e2e 用例。
- 建议：在 `_SG_P0=${EPOCHREALTIME:-}` 同一行或下一行加 `_SG_RELAXED=`（`v3alt.sh` 已加；带同一环境变量时回到 `rc=2 wall=3.04s`）。SC-V2 增加一条 e2e：「环境带 `_SG_RELAXED=1` 时与不带时结果相同」，并对应一个 BI（不初始化）。

### CR-04 — Major — 任务计划（TASK-002 acceptance）

- type: issue；category: testing；scope: `detailed-tasks.yaml` TASK-002 acceptance「bash 3.2.57 下套件全绿」
- 摘要：这条验收照字面做不到，换一种读法又与 6 组改断言和 SC-V 新用例冲突。
- 证据：套件本身要求 bash 5。在 git 检出里 SC-8 会运行，它用到 `mapfile`（`tests/secret-guard.test.sh:1859`）和 `EPOCHREALTIME`（`:1824-1826`），而套件里没有任何 bash 版本守卫（grep `BASH_VERSINFO` 为 0 处）。如果把它理解成「套件用 5.2 跑、hook 用 3.2 跑」（`run_case` 经 shebang `env bash` 取 PATH 上的 bash，`:41`），那么 3.2 下准入门恒不成立，W9 的 6 组新断言和 SC-V3/4/5/7/8/10 的正例都会翻转（3.2 下得到的是基线文案，或立即返回 4）。计划和规格都没有说这些用例要按 hook 的 bash 版本分支。另外 bash 3.2.57 是本机自建的，不在仓里（`v3/README.md`），第三方无法复跑。旧 Spec 的同名验收实际做法是 `bash -n` 加个别行为（`secret-guard-scan-cost-and-firstpass-cap/detailed-tasks.yaml:49`）。
- 建议：改写为「套件在 bash 5.2 下全绿；bash 3.2.57 下：hook 与套件 `bash -n` 通过，并按 W12 第 3 节的方法做 e2e 逐字节对比（SC-V2 的 3.2 条款）」；依赖放宽的用例显式按 `BASH_VERSINFO[0] >= 5` 且 `OSTYPE == linux*` 分支，在其他环境里断言基线结局。

### CR-05 — Major — proposal v3（SC 表 BI-13）+ 任务计划 TASK-003

- type: issue；category: testing；scope: proposal SC-V3 行「BI-13：锚点设在 `_sg_per_segment_eval` 入口（首遍不计入截止）」
- 摘要：BI-13 的定义自相矛盾。首遍 `_sg_core_eval` 是在 `_sg_per_segment_eval` 里面跑的（基线 `:1539`），锚点放在它的入口，首遍照样计入截止。照字面构造的 BI-13 只比正确实现少算 hook 启动到入口那几十毫秒，SC-V3 的 3.3 s 判据抓不住。
- 证据：`$S/v3probe13.sh`（原型副本加三处时间戳）。从 `_SG_P0` 到 `_sg_per_segment_eval` 入口，f5like 为 0.054 s、apply-heavy 为 0.103 s；入口之后首遍分别用 0.654 s 和 0.180 s。
- 影响：TASK-003 的「BI-1..BI-13 每个都至少让一条用例变红」可能在 BI-13 上做不到；或者 qa 席照括号里的意思自己改了构造，结果 BI 与规格文字不一致。
- 建议：BI-13 改为「锚点在首遍之后取（例如在 `:1542` 的 `_SG_T0` 重置处，或在 `_sg_relax_run` 入口用当时的 `EPOCHREALTIME`）」，SC-V3 的 e2e 首遍形状照 CR-08 调整。

### CR-06 — Major — proposal v3（What 7）+ `v3/commentsync.py`

- type: issue；category: documentation / testing；scope: What 7 封闭清单（基线行号）
- 摘要：清单每处只钉一个短语，同一注释里其他会失实的句子不受检查；还有至少两句完全不在清单里。target 模式可以在这些句子都没改的情况下变成 GREEN，对这些位置来说这项检查恒绿。
- 证据（基线行号；均为 W8 落地后失实）：
  - `:1534-1535`「Length budget: an overrun inside _sg_vx_pass blocks there」：W8 之后，`_sg_vx_pass` 里超限会返回 4 并重跑，可能放行。不在清单里。
  - `:1532`「3. only if both allowed, the W9 project extension -- on the original command, then on the variable-substituted whole command」：放宽重跑放行后直接 `return`，扩展腿不再运行（W8 第 223 行的注释自己写了这一点）。清单第 8 处只退役了第 2 项。
  - `:580-581`「The oversize string is never built, expanded further, judged or scanned: the pass stops at the first overrun and nothing behind it is touched」：在作业里，大副本会被构建并判定。
  - `:584-585`「(2) _SGV_SMAX: a substituted copy … that would become longer blocks the command」
  - `:674-675`「(not built, _SG_SUB stays S; the caller blocks the command)」
  - `:703`「nothing behind the overrun is built or judged」
  - `:89-90`「a substituted segment up to 8192 characters」
  - 套件 21an 标题（`tests/…:2676`）「the functions hold the limits — a built copy is at most 8192 characters」：现在只在放宽重跑之外成立。
- 建议：把上面这些作为退役短语加进 `commentsync.py` 与 What 7 表，表头不再写「封闭」，除非逐句扫过；或者把核对单位改成「整条注释块重写」，即每处给出改后应出现的新句子，而不只是一个退役短语。

### CR-07 — Major — 任务计划（TASK-003 判据）

- type: issue；category: testing；scope: TASK-003 acceptance 与 design
- 摘要：判据太松，区分不了好坏实现。
- 证据：(1)「BI-1..BI-13 每个都至少让一条用例变红」：任何一条红都算，包括与该 BI 无关的断言，比如改动顺带让 commentsync、头注释计数或某条文案断言变红。(2) 对抗矩阵的判据「结局只能是放行、拦截文案或基线回落」几乎覆盖所有 exit 0/2 的结局，等于恒真；它不能发现「读凭据的命令被放行，而规格没有申报」，而这正是本轮最想抓的一类。
- 建议：(1) 改为「每个 BI 必须让 SC 表里点名它的那条 SC 变红」；SC 表里没点名的 BI（比如 CR-01/02/03 新增的），要先补一条点名它的 SC。(2) 矩阵逐输入写预期结局：读凭据形路径、又没有被申报的 credit 来源（R-a/R-b）的输入，只允许拦截或回落；最长行 > 8192 并命中规则的，必须是 `longline`；其余写明预期的放行或拦截。时间判据对所有结局都适用，不只对放行。

### CR-08 — Major — proposal v3（SC-V3、SC-V6）+ INV-7

- type: risk；category: testing；scope: SC-V3 e2e「f5like 墙钟 ≤ 3.3 s」「首遍约 2 s 的形状墙钟 ≤ 3.3 s」，SC-V6「会回落的输入」
- 摘要：这几条 e2e 的区分力取决于本机的速度和负载，换一台机器就会恒绿或恒红。
- 证据：f5like 的作业能回落，靠的是「三段各约 1 s 的 credit」，加上首遍 0.65 s，本机自然耗时约 3.7 s（`gen-v3.py` 注释；`$S/v3probe13.sh` 实测首遍 0.654 s）。在快约 2 倍的机器上，作业会在 3 s 内判完：SC-V6 取不到回落，SC-V3 也就分不出 BI-4（不进作业、在进程内跑）。反过来，「首遍约 2 s」只留了约 1 s 余量：同一个 21ab#2 形状，基线两次实测分别为 3.52 s（负载 2.4–3.6）和 2.36 s（负载约 0.6）（仓内 `W11-adversarial.txt` 与 `$S/v3copy/W11-adversarial.txt`）。而 INV-7 规定时档类测量只在负载 < 2 时跑，套件做不到这一点。
- 建议：涉及截止的 e2e 一律设 `SECRET_GUARD_TIME_BUDGET_S=1`（截止 1 s），输入的自然耗时按 ≥ 3 倍截止来构造；首遍形状取约 0.5–1 s（BI-13 仍会多出 ≥ 0.5 s）；比较 stderr 之前先断言结局类型（例如首行是基线的 oversize 行、墙钟 ≥ 截止），不满足就判 SETUP 失败，不判 PASS。

### CR-09 — Minor — 原型 / 证据

- type: issue；category: implementation；scope: `_sg_relax_run` 的 `out="$( … )" 2>/dev/null`
- 摘要：赋值语句上的 `2>/dev/null` 不作用于命令替换本身的 stderr（bash 5.2 实测），所以它不提供注释里暗示的保护。P6 目前成立，是因为命令替换在正常路径上什么都不往 stderr 写（`$S/notif.sh`：`set -m` 作业被 KILL 后，即使 `wait` 不重定向也不打印通知）。
- 证据：`$S/e1.sh` 的 E0 行（`x=$( echo … >&2 ) 2>/dev/null` 照样打到 stderr）；CR-02 实验里 fork 重试信息漏到了调用方的 stderr。
- 建议：命令替换首句写 `exec 2>/dev/null`（作业自己的 `2>&1` 不受影响；已在 `$S/v3alt.sh` 验证 P6）。

### CR-10 — Minor — 原型 / 证据

- type: issue；category: implementation；scope: `_sg_relax_left`、`_sg_relax_ok`
- 摘要：(1) 截止按墙钟（`EPOCHREALTIME`）计算，而剩余时间没有封顶。hook 启动后到触发点之间，墙钟若往回跳，截止会顺延同样的量。(2) 准入门检查的是 `EPOCHREALTIME` 变量非空，而不是 bash 版本。bash 4.x 从环境继承一个同名变量时，时钟是静态的，截止就变成「触发时刻 + 3 s」。
- 证据：`$S/e6.sh` 把 `_SG_P0` 设在 2 s 之后（等价于墙钟回拨 2 s），截止上限 1 s，算出的 `_SG_LEFT=2.998887`，桩被杀前跑了 3.00 s。bash 3.2 继承该变量时，结局仍与基线逐字节相同，因为作业在 `$BASHPID` 上未绑定而回落（已实测）；bash 4.x 本机没有，未核实。
- 建议：在 `_sg_relax_left` 里加 `(( now <= cap * 1000000 )) || return 1`；`_sg_relax_ok` 加 `(( BASH_VERSINFO[0] >= 5 ))`。

### CR-11 — Minor — 任务计划（TASK-004）

- type: issue；category: testing / documentation；scope: TASK-004 design 与 acceptance
- 摘要与证据：
  - (1)「放行数不低于原型 (136/137)」与证据不符：W12 和 W12b 都是 137 条放行、1 条 VMAX 拦截（即 SMAX 类 137/137）；「136/137」在证据、proposal、dispositions 里都找不到，只出现在 `detailed-tasks.yaml:88`。两种读法会差 1 条。
  - (2) 时间判据只看放行；回落和拦截越过上界的情况查不到（虽然真实流量里不太会出现）。
  - (3)「run-w9 / run-w10-w11 / w10b / run-w12 改成接受实现 hook 路径…其余不变」：这些脚本都把结果写到 `$HERE`，即仓内已跟踪的 `W9-suite.txt`、`W10-mechanism.txt`、`W11-adversarial.txt`、`W12-*`（`run-w10-w11.sh:8,17`、`run-w9.sh:24`、`run-w12.sh:9-17`）。照做会覆盖 proposal 引用的原型证据，也会失去「不低于原型」的比较基准，与交付物 `W14-acceptance.txt` 也不一致。INV-2 没有列出对 `.aria/notes` 脚本的改动。
- 建议：阈值写成「137/137（SMAX 类全部放行），VMAX 那 1 条照拦」；时间判据覆盖全部结局；脚本加一个输出目录参数，结果写成 `W14-*`，原型证据只读；INV-2 补上证据目录。

### CR-12 — Minor — 任务计划（TASK-001 / TASK-004）

- type: issue；category: testing；scope: TASK-001「基线红」
- 摘要：TASK-001 要求 SC-V 在基线上实跑为红，但这些用例要到 TASK-002 才写；计划里也没有任何一步要求最终的套件对基线 hook 跑一遍。Rule #6 的 substitute 正是靠「baseline-failing 的 SC 级测试必须在场」成立的（SOT §2 第 1 行）。
- 建议：TASK-004 增加一步：用最终套件对 `59e333c` 的 hook 跑一遍，逐条记录 SC-V 的红/绿，与 TASK-001 的预期对照。TASK-001 只保留「预期红/绿表」。

### CR-13 — Minor — proposal v3（What 2/3 代码块）

- type: issue；category: documentation；scope: proposal 第 88–206 行与第 210–265 行
- 摘要：W8 里分段循环那一行改动（`if [[ -n "${_SG_RELAXED:-}" ]] && (( ${#_SG_SUB} > _SGV_SMAX )); then _sg_vx_big_judge "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi`）在 proposal 里没有出现。原因是 `fill.py` 用 `is_funcs` 剔掉了整个 `@@ -745,13 +765,68 @@` hunk，函数体又是直接从 hook 文本里截取的，这一行两边都没取到（grep proposal 为 0 处）。
- 影响：「代码块与原型逐字一致」对已列出的部分成立，但 Spec 不完整；INV-1 又规定「冲突时以 Spec 为准」。按 Spec 实现的人会漏掉分段模式的 C 路由。好在 SC-V7 的 21ab#1 会抓住。
- 建议：`fill.py` 把这个 hunk 的非函数部分也放进 What 2 的 diff 块，或者在 What 2 的文字里点名分段模式的分派。

### CR-14 — Minor — proposal v3（SC-V9）

- type: issue；category: testing；scope: SC-V9「TMAX 直调廉价形状（1 KB 值 × 8 引用 × 至少 8 段）」
- 摘要：「1 KB × 8 引用」使每段副本约 8204 字符，超过 SMAX。不在放宽重跑里直调时，第一段就停在触发点（返回 4 或 2），永远到不了 TMAX。
- 建议：写明在 `_SG_RELAXED=1` 下直调 `_sg_vx_pass`（即模拟作业内部），或者每段取 ≤ 8192 的副本、段数 ≥ 9。

### CR-15 — Minor — proposal v3（SC-V11）

- type: issue；category: testing；scope: SC-V11「hook 里没有 `{8193` 形的正则」
- 摘要：静态 grep 只抓字面写法；用变量拼出来的写法（如 `re=".{$(( _SGV_LMAX + 1 )),}"`），代价相同，却能通过检查。
- 建议：grep 再加上 `\{[0-9]{4,},` 和 `\{\$\(\(`，或者对 `_sg_vx_big_judge` 加一条只有约 70 KB 单行输入的计时断言。

### CR-16 — Minor — 任务计划（处置落地）

- type: issue；category: documentation；scope: `dispositions.md` R2 A22
- 摘要：A22 的处置是「涉及 locale 的用例用 `C.UTF-8`，并先断言字符集（TASK-002）」，但 proposal v3 和 `detailed-tasks.yaml` 里都没有这一条（grep `C.UTF-8|locale|字符集` 只在 Why 第 4 项命中一次）。`_sg_vx_big_judge` 与 SMAX、LMAX 的比较都按字符计数，多字节用例在 C 与 UTF-8 下的走向不同。
- 建议：TASK-002 design 补上这一条。

### CR-17 — Minor — 任务计划（残余 issue）

- type: issue；category: documentation；scope: proposal「残余」第 2 条（TL2-F5：≤ 8192 的判定单次可超 5 s，基线 e2e 7–19 s 并放行）
- 摘要：这是一个已知的基线 fail-open，只写进了 CHANGELOG 的订正，没有跟踪 issue。TASK-001 只开两张残余 issue（for 列表、heredoc），`#228` 管的是首遍，不是这一段。
- 建议：TASK-001 再开一张，或者在 `#228` 的留言里明确把它纳入范围，并在 CHANGELOG 写上号。

### CR-18 — Minor — 任务计划（TASK-006）

- type: issue；category: documentation；scope: TASK-006
- 摘要：SC-V12 的「standards 三处计数一致」没有归属任务和验收，standards 子模块的提交、双推、`ls-remote` 和主仓 gitlink 也没有点名。验收「origin / github 两边 ls-remote 一致」没说是哪几个仓（aria、standards、主仓）。主仓若走 PR，Rule #8 的 C.2.4 pre-merge gate 也没写。
- 建议：TASK-006 的 design 与 acceptance 逐仓列出；把「三处计数等于实跑数」列为验收项；主仓 PR 合并前跑 C.2.4。

### CR-19 — Minor — 任务计划（INV-6 / TASK-007）

- type: issue；category: documentation；scope: INV-6，TASK-007 design 与 acceptance
- 摘要：「关闭关键词只在阶段 D 的主仓提交」这一约束，只在 TASK-007 写了「推送前做关键词核对」，没有给命令；TASK-002 与 TASK-006 的提交和 PR 描述没有核对步骤。TASK-007 的验收也不检查 #217 是否真的已关闭。主仓提交里的跨仓关键词（`10CG/aria-plugin#217`）在 Forgejo 上会不会生效，推到 GitHub 镜像后又按哪边的编号解析，都未核实。
- 建议：每次推送前在待推范围上跑 `git log --format=%B <range> | grep -inE '(close[sd]?|fix(e[sd])?|resolve[sd]?)[^0-9]*#?217'`，期望为空（TASK-007 的那次除外）；TASK-007 的验收加上「#217 状态为 closed，否则手工关闭」，并核对 GitHub 一侧没有误关同号 issue。

### CR-20 — Minor — 任务计划（rule6_note）/ proposal What 5

- type: decision；category: documentation；scope: `meta.rule6_note`，`longline` 模板
- 摘要：`rule6_note` 的字段形式符合 SOT §4.1（`decision_table_row: n/a` 表示不属 Skill 变更，`description_changed: no`，其余为 n/a），逐 hunk 判为描述性的理由也基本成立。有一处不严谨：说 longline「逐字复用 oversize 模板的两条指令行，只新增描述」，可它被用在原本拿 oversize 文案的命令上，相比之下删掉了第三条指令「do not repeat one long $VAR many times in a single command」。而这条恰恰对「展开产生的长行」最相关。对这些命令来说，AI 收到的指令少了一条，严格讲不是纯描述性的变化。
- 建议：把这条指令原样补回 longline 模板，第 1 行描述性的判定就站得住；或者在 note 里点名「删去一条指令」并按 §3 处理。`decision_table_row: n/a` 而 note 里写 row 1，可以接受，但最好在 note 里写一句「n/a 指整体，row 1 指 AI 面向的 hunk」。

### CR-21 — Minor — 任务计划（依赖）

- type: issue；category: architecture；scope: TASK-005 `depends_on: [TASK-002]`，TASK-004
- 摘要：TASK-003 可能促成修改（补用例、修实现），而 TASK-005 只依赖 TASK-002，审到的可能是修改之前的版本；TASK-004 也没有写「修复后重跑」。
- 建议：TASK-005 改为依赖 TASK-003，或要求对 TASK-003 之后的增量再审一次；TASK-004 写明以最终提交为准。

### CR-22 — Minor — proposal v3（What 3 耗时上界）

- type: issue；category: documentation；scope: What 3「耗时上界」、P3
- 摘要：上界公式 max(首遍 + 基线 W10 前段, `_SG_P0` + min(预算, 3)) 漏了两项：准入门里 `_sg_ext_entries` 的开销（`_sg_ext_root` 会 fork jq，在截止之外），以及 `_SG_P0` 之前的启动时间（`$SHELL` 为 zsh 时还有 re-exec）。在 Claude Code 的 5 s 里这两项都要算。两项都不大，但 TASK-003 的判据以这个公式为准。
- 建议：公式里加上「+ 准入门开销」，并注明 `_SG_P0` 取在 re-exec 之后。

## Verdict

**PASS_WITH_WARNINGS**：0 Critical / 8 Major（CR-01–CR-08）/ 14 Minor（CR-09–CR-22）。

选定机制（基线先跑，在两个触发点、准入门成立时，于自成进程组的后台作业里按放宽规则重跑，硬截止）本身没有被证伪。W8 在正常环境下，对 W11 的全部形状都守住了截止、回落逐字节相同、P1 由结构保证。没有判 Critical，理由是：CR-01、CR-02、CR-03 都能做出越过截止乃至放行的实测，但前提分别是「判定留下后代进程」（现有判定代码不会）、「计时器 fork 失败」、「hook 环境被注入」，正常运行碰不到。不过这三条都与 proposal 给出的机制保证（P3、P5、计时器 fork 检查）直接矛盾；计划又要求「逐字落地」，所以应在 B.2 之前改进原型（`mkv3.py` → W8 → `fill.py` 重新生成 proposal）。三处改法已在 `$S/v3alt.sh` 合并验证（S1–S8、G1–G8、W11 五形状、P6 均通过）。CR-04–CR-08 是验收层面的缺口：bash 3.2 验收做不到、BI-13 自相矛盾、注释封闭清单不封闭、TASK-003 判据近乎恒真、e2e 时延断言依赖本机速度。都是改文字就能解决，不需要改机制。

## 轮次记录

- **读了什么**：任务书；`detailed-tasks.yaml` 全文；`proposal.md` 全文；`v3/README.md`、`W8-v3.diff`、`v3unit.sh`、`run-w10-w11.sh`、`w10b.sh`、`commentsync.py`、`fill.py`、`gen-v3.py`，以及 W9、W10、W10b、W11、W12、W12b 的输出；`dispositions.md` R2 段；基线 hook 的 `:80-189`、`:560-954`、`:1486-1590`；套件的 `:33-60`、`:1780-1890`、W10 标题行，以及多处按 grep 定位的行；`skill-benchmark-exemption.md` §1–§5；`secret-hygiene.md` 的三处计数。
- **跑了什么**（全部在 `$S` 下，`taskset -c 0,1 nice -n 19`，同一时刻只跑一个实验）：
  - `mkv3.py` 重新生成并与 W8 逐字节比对；
  - `fill.py` 重新生成并与 `proposal.md` 逐字节比对；
  - `run-w10-w11.sh`（复制件，33 s）、`w10b.sh`、`commentsync.py` 的 baseline 与 target 两种模式；
  - 自写实验：`e1.sh`（赋值重定向语义、遗留后代）、`notif.sh`、`e3.sh` + `v3forkfail.sh`（计时器 fork 失败注入）、`_SG_RELAXED` 环境注入 e2e、`v3probe13.sh`（首遍位置计时）、bash 3.2 环境注入、`e6.sh`（墙钟回拨模拟）、`e7.sh`（作业被停住）；
  - 修复验证：`v3fix.sh`（只加作业组 KILL）与 `v3alt.sh`（计时器进作业 + 作业组 KILL + `exec 2>/dev/null` + 初始化 `_SG_RELAXED`），跑了 v3unit、E1 探针、W11 五形状、P6。
  - 进程清理只按自己记下的 PID 或精确参数（各实验结束时残留均为 0）。没有改动仓内任何文件，只写了本报告。
- **没跑、没核实的**：
  - `run-w9.sh`（整套件）与 `run-w12*.sh`（需要语料）按任务书没跑；
  - bash 4.x 下的 CR-10（2）（本机没有 4.x）；
  - CR-02 的 ENOMEM 分支（无法构造），只做了推理；
  - CR-19 关闭关键词的跨仓、双远端解析行为；
  - SC-30 闭包 awk 能否识别 `_sg_relax_job … &` 这种调用形式（新函数都在闸门之上，不影响结论）。
- **工具调用**：约 72 次。
