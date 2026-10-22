---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T18:11:01.157Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — code-reviewer 席（全新实例）

侧重：原型 v3.1（`v31/W8-v31.diff`）逐 hunk 的代码正确性；验收与证据脚本（`sc-cases.sh`、`sc-direct.sh`、`mutants.py`、`run-mutants.sh`、`fill31.py`、`commentsync.py`、`run-evidence.sh`）的代码缺陷；非作者变异测试。

下文 scratch 指 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r2/code-reviewer/`。原型由 `mkv31.py` 在 scratch 里重新生成为 `v31.sh`，sha256 前缀 `9f61db0e7b8b`，与 W13 页眉一致；`diff -u base.sh v31.sh` 与 `W8-v31.diff` 逐字节相同。下文 `v31.sh:<n>` 指原型的行号，`base.sh:<n>` 指基线 `59e333c` 的行号。

**总体判断**：原型的作业机制本身我没有找到错误。在 bash 5.0、5.2、5.3 上实测，作业是独立进程组的组长，计时器、计时器里的 `sleep`、判定留下的子进程以及命令替换都在这个组里（scratch `pg.sh`）。退出码 77、回落、组杀、自检这几处逐行核对也都成立。问题集中在可执行验收上，分三类：

1. 用例依赖本机速度和负载。在这台负载较高的宿主上，未改动的原型就会假红。
2. 4 个像真实执笔错误的坏实现没有被任何语义相关的用例抓住。其中 3 个已用定向探针证实会造成新的放行：基线拦、原型拦、坏实现放行。
3. `commentsync.py` 的「块级」核对、`fill31.py` 的「逻辑 hunk 全部引用」断言都不能按它们声称的那样变红。

另外，TASK-004 的 W8 判据和 What 6 相互矛盾。

## 审计结论

### F1 — 计时判据依赖本机速度与负载；INV-7 对 `sc-cases.sh` 的豁免前提不成立

- **type**: issue；**severity**: Major；**category**: testing
- **scope**: `v31/sc-cases.sh` 的 `outcome()`（:74-79）、`deadline()`（:68-73）及其窗口；`shim/delay-first`；detailed-tasks.yaml INV-7、TASK-002 / TASK-004 / TASK-003 的 acceptance
- **针对**：验收用例 / 证据，以及任务计划
- **复发**：PP1-A5（时延判据依赖自然速度）
- **摘要**：proposal 的 Success Criteria 说「计时判据全部来自注入的固定延迟……而不是本机的自然速度」，INV-7 据此把 `sc-cases.sh` 排除在负载纪律之外。两者都不成立，原因有三：
  - `outcome()` 类用例要求重跑在截止（P0 + 3 s）前自然跑完。
  - `deadline()` 类用例要求作业在截止前跑到它的第一份拦截文案，sed 垫片的 10 s 停顿才落在作业里；作业没跑到，停顿就挪到父进程回落文案的 `_sg_redact_echo` 里，hook 总耗时约 13 s，被 `timeout 12` 杀掉，rc=124。
  - 固定窗口（2.85–3.6 s、0.85–1.6 s、3.2–4.3 s）假定 ε 很小。
- **证据**：均在 loadavg 7.5–11.9 下实测（`taskset -c 0,1 nice -n 19`，与另一席同时跑）。
  - 未改动的原型跑整轮：`FAIL V9-E11-tmax-in-rerun hook rc=2 oversize 3.03s`，见 scratch `run-proto-52.txt`。
  - 同一用例单独重跑 3 次，2 次 FAIL：hook 5.97 s（基线 3.64 s）与 4.27 s，1 次 PASS（2.16 s）。
  - 在不经过各自改动点的路径上，坏实现那几轮也出现同样的假红（`run-MB.txt`、`run-MC.txt`、`run-MD.txt`、`run-ME.txt`）：
    - `run-MB.txt`：V9-E11 红。
    - `run-MC.txt`：V9-E11 红；V2-E8 走的是 benign 路径，也红在 3.18 s。
    - `run-MD.txt`：MD 只改分段分支，但 4 条整串模式的 stall-read 用例越窗——V3-E3 4.01 s、V2-E6 4.09 s、V3-E5 2.22 s（截止 1 s）、V2-E7 4.64 s。
  - rc=124 的机制见 `run-MC.txt`：V3-E3、V3-E4、V2-E6 都是 `hook rc=124 none 12.0xs`。
  - 埋点（scratch `timeit.sh`、`v31-dbg.sh`）显示，tmax-rerun 的首遍单独就要 1.4–2.3 s。
  - W13 本身是在负载 1.27 → 2.46 下生成的，所以全绿。
- **影响**：
  - TASK-002「套件在 git 检出里全绿（5 个 bash）」与 TASK-004「W13 实现在 5 个 bash 上 FAIL 为 0」在负载下不稳定，好实现也会红。
  - 用例按 TASK-002「逐字照搬」进套件后，安全 hook 的套件里就有了时红时绿的用例。
  - TASK-003 耗时矩阵的判据「≤ max(T_trigger, 3 s) + 0.3 s」没有负载纪律，同样会假红。
- **建议**：
  - (a) INV-7 扩展到 `sc-cases.sh`、TASK-003 矩阵与 W13：开始和结束各记一次 loadavg，越线就作废重跑。删去「不受本条约束」。
  - (b) 用例改用埋点副本取到的 T_trigger 来判，不用固定窗口。T_trigger 不在作业里，或剩余时间小于某个余量时，记 SKIP（单独计数），不记 FAIL。
  - (c) 垫片在停顿前把自己的进程组号写进状态目录，`deadline()` 断言停顿发生在作业的组里；不在作业里就记 SKIP，并给出原因。

### F2 — 两个触发点是否都问准入门，没有用例；分段触发点漏问准入门的坏实现 MA 全绿，并造成新的放行

- **type**: issue；**severity**: Major；**category**: testing
- **scope**: SC-V2（`V2-G*` 全部直调 `_sg_relax_ok`；`V2-E9` 用的 `ext-read` 以 `(` 开头，是整串模式）；原型 `v31.sh:769`
- **针对**：验收用例
- **摘要**：在 `_sg_vx_pass` 的分段分支里删掉 `if _sg_relax_ok; then … fi`，改成无条件 `return 4`，`sc-cases.sh` 结果是 PASS 94、FAIL 0。原因有三：
  - 准入门函数本身没变，所以 V2-G* 照绿。
  - 整串模式的 V2-E9 不经过这一行。
  - bash 3.2 下 `_sg_relax_run` 的 `_sg_relax_left` 失败，照样回落为基线字节。
- **安全影响**：用定向探针 `probes/seg-ext-read.json` 实测：扩展项目，分段模式，读的正是扩展清单里列的路径。共 4 次，MA 2 次 rc=0（放行），另 2 次在截止处回落；原型和基线 4 次都是 rc=2（oversize）。这是新的放行：重跑放行后直接 `return`，扩展腿被跳过。同一处遗漏还会让未实测平台在分段模式下进入放宽，违反裁定 E 与 Decision 16。条件是该平台有 `EPOCHREALTIME` 与 `/proc`，例如 Linux 上的 bash 5.4，或 Cygwin / MSYS 上的 bash 5.x。
- **建议**：
  - 加 `V2-E9b`：分段模式、扩展项目，期望与基线逐字节相同（形状可用 `probes/mk.py` 的 seg-ext-read）。
  - 加一个直调用例：把 `_sg_relax_ok` 桩成返回 1，对一个超 8192 的分段调用 `_sg_vx_pass`，期望状态 2 与基线 oversize 文案，而不是 4。
  - 把 MA 并入 BI 清单，指定上面这两条用例。

### F3 — P9「重跑里没有计数上限」没有覆盖 for 语句这一轴；坏实现 MB 全绿，并造成新的放行

- **type**: issue；**severity**: Major；**category**: testing
- **scope**: SC-V9（`V9-C1` 只数赋值，`V9-C2` 只数引用，`V9-E10` 的读取经由赋值）；原型 `v31.sh:643`
- **针对**：验收用例
- **复发**：PP1-A1 的第三条轴（「第 9 个 for 不收集也不代入」）在验收这一侧没有落地
- **摘要**：把 `ca=1000000 cf=1000000` 改成 `ca=1000000`，也就是重跑里仍收 8 个 for。这是很像真实执笔错误的一处遗漏。`sc-cases.sh` 只红了 V9-E11，见 `run-MB.txt`。那条是 F1 的负载假红，tmax-rerun 里没有 for，与这处改动无关。
- **安全影响**：定向探针 `probes/for9-read.json` 是一条整串模式的大命令：8 个占位 for，第 9 个 for 的变量指向 APPINI 路径，然后 `cat $f`。结果：基线 rc=2（oversize），原型 rc=2（finding），MB rc=0（放行）。
- **建议**：
  - 加 `V9-C3`：直调，12 个 for，重跑里应收 12 个，基线那一遍应收 8 个。
  - 加 `V9-E10b`：端到端，经第 9 个 for 变量的读取，期望 rc=2。
  - 把 MB 列入 BI 清单。

### F4 — 裁定 C 的定义性质（长行命中即拦，不看脱敏过滤）没有任何用例；坏实现 MC 只因计时副作用碰红，MD 未被抓住

- **type**: issue；**severity**: Major；**category**: testing
- **scope**: SC-V7 / SC-V10。`V10-N2`、`V10-N4`、`V7-E14` 与 stall-read 都只有读取、没有脱敏过滤；唯一的分段模式端到端形状 tmax-rerun 里没有读取。原型 `v31.sh:1636-1650`（`_sg_judge_one`）、`v31.sh:778`（分段路由）
- **针对**：验收用例
- **摘要**：
  - **MC**：先算 credit，只在 credit 为 0 时才按 nocredit 写 longline 文案。这是对「不评估脱敏过滤」的一种误读。`V10-N2`、`V10-N4`、`V7-E14` 全部仍绿。红掉的是 stall-read 的截止类用例（rc=124），以及 V2-E7、V2-E8、V9-E11 这些与改动无关的负载假红（`run-MC.txt`）。stall-read 那几条红，是因为在 16 KB 单行上算 credit 太慢，作业在写出文案前就被截止杀掉，垫片停顿挪进了父进程。换一台更快的机器，或者用更短的长行，MC 就会全绿。按 TASK-003 自己的规则（「无关断言碰红不算抓住」），MC 算漏网。
  - **MD**：分段分支对所有副本都调 `_sg_judge_one`，不再路由。没有相关用例变红（`run-MD.txt`）。4 条红都在整串模式路径上，属于 F1 的负载假红；V9-E11 这一轮是绿的。
- **安全影响**：
  - MC：定向探针 `probes/longline-credit.json` 是整串模式的一行，代入后超过 8192，含 `cat $F`，另有一处无关的 `>/dev/null`。结果：基线 rc=2（oversize），原型 rc=2（longline），MC rc=0（0.32 s 放行，凭据会被读出）。
  - MD：在本机负载下，`probes/seg-tee-credit.json` 两次都在截止处回落为 oversize，没有放行。它会不会放行取决于机器速度，未核实。
- **建议**：
  - 加 `V10-N5`：直调 `_sg_vx_big_judge`，输入是一行超过 8192 的副本，含读取，并带一处无关的 `>/dev/null`，期望 rc=2 且文案为 longline。
  - 加一个分段模式的端到端 longline 用例：分段内用 `|`，或用不作切分记号的 `&` 接读取。
  - 把 MC、MD 列入 BI 清单。

### F5 — `commentsync.py` 的块级核对可以被改一个字符绕过；PP1-A18 复发

- **type**: issue；**severity**: Major；**category**: documentation（testing）
- **scope**: `v31/commentsync.py` 的 `check()`（:62-80）；proposal What 7；TASK-002 acceptance「commentsync.py target 为 GREEN（hook 与套件两部分）」
- **针对**：验收用例 / 证据，以及任务计划
- **复发**：PP1-A18
- **摘要**：target 模式第 2 条（「带这些哈希的块一个不剩」）是第 1 条（「锚点 0 次」）的逻辑推论。锚点就在块里，去掉或改动锚点，块的哈希必然变。所以 What 7 说的「整块重写过，不是只换一个短语」并没有被机械地保证。
- **证据**：对未改动的基线 hook 只做两件事：在 13 处锚点出现位置各插入一个字符 `~`，再加一行包含全部 ADD 词的注释（scratch 里的 python 片段，产物 `base-anchor-tweak.sh`）。结果 `commentsync.py --hook-only base-anchor-tweak.sh target` 为 **GREEN**，而 8 个块其余的旧说法都还在。
- **影响**：hook 一侧有 INV-1 的逐字落地和 W8 的 diff 兜底。套件一侧的 7 块注释与 5 个标题不在原型里，它们的验收只有 commentsync GREEN 加 TASK-005 的人工审读；照字面做最小改动就能通过。
- **建议**：
  - hook 一侧，直接比对实现与原型的注释 run（比 W8 diff 更直接）。
  - 套件一侧，在 proposal 里写出 7 块与 5 个标题的目标全文，逐字比对。
  - 退一步，至少给每个块列出所有会失实的句子（不止一个锚点），全部要求 0 次。

### F6 — TASK-004 的 W8 判据与 What 6 矛盾，正确实现必然红

- **type**: issue；**severity**: Major；**category**: implementation（计划）
- **scope**: detailed-tasks.yaml TASK-004 acceptance「W8: 实现相对原型的差只有行号（diff 原型 实现 只出现行号漂移，没有内容差）」；TASK-002 design「What 6：删 :666 死代码，单独一个提交」；proposal What 6「W8 的原型不含这一删」；INV-1
- **针对**：任务计划
- **摘要**：What 6 要删 `[[ -z "${_SGV_V[j]}" ]] && continue`（`base.sh:666` / `v31.sh:675`）。实现删了这一行，原型没有删，所以 `diff 原型 实现` 一定多出这一行的删除，TASK-004 的判据照字面不可满足。INV-1「逻辑与注释逐字落地，只重锚行号」也没有为 What 6 留出例外。W8 diff 是本计划防止偏离原型最强的一道闸：它照字面红了，执笔席就只能自行解释或放宽，F2–F4 那几类偏离就可能借这个口子过去。
- **建议**：
  - 给 `mkv31.py` 加一个可选步骤（What 6），TASK-004 拿实现与「原型 + What 6」比对。
  - 或者把判据改成「差只有行号漂移，加上 What 6 那一行的删除」，并在 INV-1 里写明这个例外。

### F7 — `deadline()` 在非放宽的 bash 上丢掉了附加环境变量，用例名与所测不符

- **type**: issue；**severity**: Minor；**category**: testing
- **scope**: `v31/sc-cases.sh:70`：`if [[ $RELAX != yes ]]; then identity "$id" "$s"; return 0; fi`
- **针对**：验收用例
- **摘要**：bash 3.2 那一轮里，V2-E6 的 `_SG_RELAXED=1`、V3-E4 的预算 4、V3-E5 的预算 1 都没有传给 hook。这三条在 3.2 上只是 V6-E2 的重复：「环境变量打不开放宽」在 3.2 上实际只由直调的 V2-G11 覆盖。`outcome()` 在同一分支里会传 `"$@"`，两处不一致。
- **建议**：改为 `identity "$id" "$s" "$@"`；不应带到基线上的变量（如 shim 设置）在 `identity` 内另行区分。

### F8 — `sc-direct.sh` 的几条用例对运行环境有隐含假设

- **type**: issue；**severity**: Minor；**category**: testing
- **scope**: `v31/sc-direct.sh:86-103`（V5-S10、V5-S10c 的文本注入）、:80 与 :109（全局 `ps` 扫描）；`run-mutants.sh:11-12`
- **针对**：验收用例 / 证据
- **摘要**：
  - (a) V5-S10 / V5-S10b 靠 `ulimit -u 1` 让 fork 失败。RLIMIT_NPROC 对 uid 0（或持有 CAP_SYS_RESOURCE 的进程）不生效，所以以 root 跑套件时（容器里常见）好实现也会红。
  - (b) V5-S10 与 V5-S10c 按字面文本定位计时器（`local me=$BASHPID tp`、`( sleep "$_SG_LEFT";`）。文本一变就输出 `FAIL … SETUP`，`run-mutants.sh` 把它当作被抓住。W13 里 BI-23 的连带红 V5-S10c 就是 SETUP 失败（由代码推得；ME 一轮实证了同一机制，见 `run-ME.txt`）。
  - (c) V5-S12 / V5-S13b 扫全局进程表找 `sleep 7.777` 等。两轮并发运行（例如本轮两个审计席同时跑）会互相看到对方的进程，造成假红。
- **建议**：
  - root 下记 SKIP。
  - SETUP 单列一种状态，不计为 FAIL，`run-mutants.sh` 也不把它算作抓住。
  - 桩里的 sleep 时长加上每轮不同的随机数。

### F9 — `fill31.py`「每个逻辑 hunk 都被引用」的断言不会红；proposal 的 hunk 计数有误

- **type**: issue；**severity**: Minor；**category**: documentation
- **scope**: `v31/fill31.py:10-17`；proposal :522「（共 19 个 hunk：14 个逻辑 hunk 全部列在上面，5 个只改注释的 hunk 见 What 7。）」
- **针对**：验收用例 / 证据，以及 proposal v3.1
- **复发**：PP1-A30 一侧（机械断言的强度）
- **摘要**：
  - `len(logic) + len(comm) == len(hunks)` 对任何输入都成立。logic 与 comm 本来就是同一判据切出来的两半，所以这条断言是恒真的，不能证明任何东西。
  - `re.split` 切出的首个空串被当成一个「只改注释的 hunk」。W8 实际有 18 个 `@@`，其中 14 个逻辑 hunk、4 个纯注释 hunk（-86、-603、-823、-1528），proposal 写成 19 与 5。
  - `comment_only` 会把 heredoc（拦截文案）里以 `#` 开头的行当成注释。合成 hunk 已验证会被判为只改注释，这类改动会从 proposal 里静默消失。
  - 现状核对：proposal 确实逐字包含了全部 14 个逻辑 hunk（scratch 内 python 核对为 True）。所以这不是现存的漏引，而是断言强度达不到它声称的水平。
- **建议**：去掉空元素；断言 hunk 数等于 `@@` 行数；按 heredoc 状态分类，或断言纯注释 hunk 与 What 7 各处一一对应。

### F10 — 原型里还有两块注释在重跑里失实，不在 What 7 的封闭清单内

- **type**: issue；**severity**: Minor；**category**: documentation
- **scope**: 原型 `v31.sh:576-578`（W10 块头：「at most 16 assignments and 8 replacements per variable」）、`v31.sh:626`（`_sg_vx_replace`：「at most 8 replacements」）
- **针对**：原型，以及 proposal What 7
- **摘要**：重跑里这三个计数上限都已取消（gc / ca / cf = 1000000），这两块注释却没有改写，也不在 What 7 的 20 处里。INV-1 要求注释逐字落地，它们会原样发出去。
- **建议**：把这两块列为 hook 的第 9、10 处，在 `mkv31.py` 第 10 步里一并改写，并补进 commentsync 的锚点。

### F11 — Why 表「137 条增长全部不超过 8192」与 W12 的「growth 1 条」没有对上

- **type**: issue；**severity**: Minor；**category**: documentation
- **scope**: proposal :40（引 W1）与 :41（引 W12）
- **针对**：proposal v3.1
- **摘要**：W1 的增长是在基线计数上限下测的（n=1053，W1 记增长 6200）。v3.1 在重跑里取消了计数上限，这条命令的增长于是超过 8192，在 W12 里落入 growth（`W12-replay-138.tsv` 中 `1053 2 growth`）。只有 R1 汇总的核验表里提过这一点，proposal 正文的两行并列而没有解释。
- **建议**：在 Why 那一行注明「W1 是基线计数上限下的增长」，并说明 n=1053 在 v3.1 下因此被增长上限拦下。

### F12 — ε 没有上界，回落路径在截止之后仍要 fork

- **type**: risk；**severity**: Minor；**category**: architecture
- **scope**: proposal What 3「耗时上界……ε 实测在 0.1 s 以内」；原型 `_sg_per_segment_eval` 的回落 `_sg_emit_blocked … oversize`（经 `$(_sg_redact_echo …)` fork 出 `sed`）
- **针对**：原型，以及 proposal v3.1
- **摘要**：放宽之后，回落拦截从约 T_trigger 推迟到约 P0 + 3 s；截止之后父进程还要收尾命令替换、fork `sed`、写文案。在本机高负载（nice 19、两个核、loadavg 约 10）下，整串模式回落路径实测的 ε 约 1.0–1.2 s（见 F1 的 MD 一轮数字），tmax-rerun 还出现过一次 5.97 s（同输入基线 3.64 s，那一次没有分段埋点，不能完全归因）。hook 启动之前的时间不在上界里：`$SHELL -c` 启动、`BASH_ENV`、zsh 下的 re-exec。这些项合起来与 Claude Code 的 5 s 之间只剩约 2 s 余量。我的测量条件比生产苛刻，生产里 hook 不带 nice 19，所以只记为风险。截止值本身已定，不重提。
- **建议**：
  - 在启动作业之前预先算好回落文案（至少预算好 `_sg_redact_echo "${command:0:200}"`），让截止之后的路径不再 fork。
  - 把「ε 随负载增长，hook 启动之前的时间不计入」写进残余或 CHANGELOG 的已知限制。
  - TASK-003 的耗时矩阵带上负载纪律（见 F1）。

### F13 — 平台判据与准入门的措辞各有两种读法

- **type**: decision；**severity**: Minor；**category**: documentation
- **scope**: proposal What 1 准入门表；Decision 16；`sc-direct.sh` V2-G2 表（:24 期望 aarch64 放宽）
- **针对**：proposal v3.1，以及验收用例
- **摘要**：
  - (a) `*-linux-gnu*` 放进来的不只是实测过的 x86_64，还包括 aarch64 / armhf，以及 WSL1 / WSL2 里的 Linux 构建（WSL1 是 Windows 上的 Linux ABI）。Decision 16 写的是「只在实测过的……上放宽」，裁定 E 点名了 Windows，V2-G2 却把 aarch64 当成应当放宽。机制是同一套 Linux 语义，失败方向有自检和截止兜住，所以只算措辞问题。
  - (b) What 1 写「文件存在（即使为空）、是目录或探测出错，都按有扩展处理」，但 `_sg_relax_noext` 在找项目根失败时（例如 `_sg_ext_root` 里的 jq 出错）输出的是 `none`，放宽照常生效。这与扩展腿自己的判定是一致的（找不到根，扩展也不生效），只是「探测出错」有两种读法。
- **建议**：写明「GNU/Linux」包括哪些架构，以及 WSL 是否算在内（或按 `/proc/sys/kernel/osrelease` 排除 WSL）；把 (b) 改写为「项目根找不到，即视为无扩展」。

### F14 — V7-E15 在基线上也是绿的，测不出「credit 照常评估」

- **type**: issue；**severity**: Minor；**category**: testing
- **scope**: `v31/sc-cases.sh:98-104`；W13 第 2 节基线绿集里有 V7-E15
- **针对**：验收用例
- **摘要**：「rc=0，或与基线字节相同」这个条件，一个根本不放宽的实现也能满足。所以 V7-E15 只能抓住拦截文案不对的实现（例如 BI-12 的连带红），测不出名字所说的「多行副本照常评估 credit」。
- **建议**：用埋点的 T_trigger 判断剩余时间；剩余时间充足时要求 rc=0，否则记 SKIP。

### F15 — `run-evidence.sh` 的几处证据约束偏弱

- **type**: issue；**severity**: Minor；**category**: testing
- **scope**: `v31/run-evidence.sh:21`、:47、`hdr()`
- **针对**：证据，以及任务计划 TASK-004
- **摘要**：
  - (a) W13 在 `BASH32` 未设置时静默只跑 4 个 bash，没有任何断言保证 TASK-004 要求的 5 行齐全。
  - (b) W12 的上界核对对没有 relax-start 的结局恒真（`t = wall`），「138 条每一种结局都核对了上界」实际只核对了进入重跑的那些。
  - (c) 页眉只绑定两个 hook，没有绑定 `sc-cases.sh`、`sc-direct.sh`、`mutants.py` 的哈希。TASK-002 会把用例改写进套件，TASK-004 却仍用 `v31/` 下的原脚本，两者没有一致性核对。
- **建议**：W13 断言 `BASH32` 已设置；W12 那句话里注明只统计进入重跑的结局；页眉加上脚本的 sha256；TASK-002 加一条判据：套件跑出的 `V*` 用例清单与 `sc-cases.sh` 相同。

## 变异测试

均在 bash 5.2.15、scratch 内运行。预测在运行前写入 scratch `PREDICTIONS.txt`；坏实现在 `mut/`，由 scratch 内的 python 片段生成，每处替换都断言恰好命中一次。运行时 loadavg 为 7.5–11.9，另一席同时在跑，所以「其他红」里混有 F1 的负载假红，表中逐条区分。

| 编号 | 坏实现（v3.1 + 一处改动） | 预测 | 实际（`run-<编号>.txt`） | 定向探针（`probes/run.sh`，结局 rc） |
|---|---|---|---|---|
| MA | `_sg_vx_pass` 分段触发点不问 `_sg_relax_ok`，直接 `return 4`（`v31.sh:769`） | 不会被抓住：V2-G* 直调准入门函数，V2-E9 是整串模式，3.2 上回落为基线字节 | **未被抓住**：PASS 94、FAIL 0 | 扩展项目 seg-ext-read，共 4 次：基线 4 次都是 2，原型 4 次都是 2，**MA 2 次 0**，另 2 次截止回落为 2 |
| MB | 重跑只取消赋值上限，仍收 8 个 for（`v31.sh:643` 去掉 `cf=1000000`） | 不会被抓住：V9-C1 只数赋值，V9-C2 只数引用，V9-E10 经由赋值 | **未被抓住**：唯一的红是 V9-E11，属负载假红，与改动无关 | for9-read：基线 2（oversize），原型 2（finding），**MB 0** |
| MC | `_sg_judge_one` 先算 credit，只在 credit 为 0 时写 longline 文案（nocredit 不再跳过 credit） | 不会被抓住：所有 longline 用例都没有脱敏过滤 | **按语义未被抓住**：V10-N2、V10-N4、V7-E14 仍绿。红的是 V3-E3、V3-E4、V2-E6、V3-E5（rc=124 或约 12 s：16 KB 行上算 credit 慢，作业在写文案前被截止杀掉，sed 停顿挪进父进程），以及 V2-E7、V2-E8、V9-E11（负载假红，与改动无关） | longline-credit：基线 2，原型 2（longline），**MC 0**（0.32 s） |
| MD | 分段分支对所有副本都调 `_sg_judge_one`，不再路由（`v31.sh:778`） | 不会被抓住：分段模式的端到端只有 tmax-rerun，里面没有读取 | **未被抓住**：红的 V3-E3、V3-E5、V2-E6、V2-E7 都走整串模式，不经过改动点（负载假红）；V9-E11 绿 | seg-tee-credit：本机负载下 MD 在截止处回落为 2（oversize），原型 2（longline）；会不会放行取决于机器速度，**未核实** |
| ME | 计时器从作业开始睡 min(预算, 3)，而不是剩余时间 `_SG_LEFT` | 会被 V3-E3 抓住：jq 停 1.5 s，回落推迟到约 T_trigger + 3 s，超出 2.85–3.6 s | **抓住**：V3-E3 hook 5.45 s，原因与预测一致。另有 V5-S10c 的 SETUP 红（按字面文本定位计时器，见 F8b）和若干负载假红 | — |

结论：5 个坏实现里，4 个没有被语义相关的用例抓住；其中 MA、MB、MC 已用探针证实会造成「基线拦、原型拦、坏实现放行」。对照 TASK-003 的 acceptance（「无关断言碰红不算抓住」），F2、F3、F4 是需要补用例的缺口。

## Verdict

**PASS_WITH_WARNINGS**：0 Critical，6 Major（F1–F6），9 Minor（F7–F15）。

没有判 Critical 的理由：照计划逐字落地原型（INV-1），再经 TASK-004 的 W8 diff 与 TASK-005 审查，F2–F4 的偏离会被 diff 发现；原型本身没有找到会造成安全退化的错误。但 W8 判据照字面不可满足（F6），而落地之后长期守护这个 hook 的只剩搬进套件的用例，它们在 F1–F5 上有缺口。所以这 6 条 Major 应在 B.2 开工前修掉，至少是 F1、F2、F3、F4、F6。

## 轮次记录

- **读过的**：
  - 任务书。
  - `detailed-tasks.yaml` 全文。
  - proposal v3.1：:1-262，以及 :505-724（参考实现中段是 W8 的逐字拷贝，改由机械核对代替逐行阅读）。
  - `dispositions.md` 文件头。
  - R1 汇总中 PP1-A1、A4、A5、A8、A12、A13、A18、A30 的行。
  - `v31/` 下：README、W8-v31.diff 全文、`sc-cases.sh`、`sc-direct.sh`、`shapes.py`、`shim/delay-first`、`mutants.py`、`run-mutants.sh`、`fill31.py`、`commentsync.py`、`run-evidence.sh`、`mkdbg31.py`、`replay138.sh`、W9、W11、W12、W13。
  - 原型 `v31.sh` 的 W10 函数、新函数、`_sg_emit_blocked`、`_sg_judge_one`、`_sg_per_segment_eval`、主流程的解析段与扩展函数。
  - 套件 SC-8 与 30b 段（按行号）。
  - WP-A 的 INV-4。
- **做过的**：
  - 重生成原型，核对哈希与 W8。
  - `sc-cases.sh` 在原型上跑 1 整轮，单独重跑 3 次。
  - 用 bash 5.0 / 5.2 / 5.3 实测进程组成员。
  - 埋点计时 5 次。
  - 5 个坏实现各跑 1 整轮 `sc-cases.sh`。
  - 7 组定向探针，共约 20 次端到端调用。
  - commentsync 绕过实验 1 次；fill31 分类器与 proposal 引用的机械核对。
  - 证据都在 scratch（`run-*.txt`、`PREDICTIONS.txt`、`mut/`、`probes/`、`base-anchor-tweak.sh`、`timeit.sh`、`v31-dbg.sh`、`pg.sh`）。3 次单独重跑、埋点计时与探针的数字只输出到会话里，没有另存文件；复现命令即对应脚本。
- **未核实的**：
  - `rule6_note`（块 A、块 B）与 SOT §2、§4.1 的对照（不在本席侧重）。
  - INV-1–INV-9 的整体自洽，以及 What 1–7 / P / SC / BI / 残余到任务的完整覆盖。只核对了与代码相关的部分。
  - 套件里 SC-8、SC-9a 在原型上的表现：W9 是非 git 副本，没有跑它们，我也没有跑。
  - MD 在更快的机器上会不会放行。
  - bash 3.2 下的整轮（只读了代码路径）。
  - WSL 上的实际行为。
  - 低负载下的复跑（宿主负载在整个审计期间都在 7.5–11.9）。
- **工具调用**：约 61 次。全部命令带 `taskset -c 0,1 nice -n 19`（`sc-cases.sh` 内部默认也带）。没有按模式批量清理进程；收尾按精确参数核对过，没有本席残留的 `sc-cases.sh` 或 `sc-direct.sh` 进程。Write 工具在本会话不可用，本报告由主控按原路径落盘。

> 主控注：本席位的工具集不含 Write，报告正文由主控按席位最后一条消息原文落盘（通知通道里的 HTML 实体 `&gt;` `&lt;` `&amp;` 已还原为原字符），内容未改动。
