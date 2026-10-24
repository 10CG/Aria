# T003b 报告：放宽重跑的对抗耗时矩阵（10CG/aria-plugin#217 TASK-003 第二段）

QA 席（非作者），全新实例。对象：aria worktree 的 `hooks/secret-guard.sh`（sha256 前缀 `af4658b6f935`，全程未改）。判据：有放宽重跑的结局，墙钟 W <= max(T_trigger, 3 s) + 0.3 s。
交付：`v31/impl/w14-matrix.sh`（8b0a98e6d46b）、`v31/impl/w14-shapes.py`（2f5cf9bdad16）、`v31/impl/W14-timing-matrix.txt`（d80cfac46c50，535 行），均在
`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`；`git status` 里只多这三个未跟踪文件，第一段的交付与套件未动，没有 commit。

## 1. 结论

1. 越界 0 个。236 个结局（40 个情形 x PATH 上 bash 5.2.15 各 5 次 = 200，最重的 6 个形状在 5.0.18 与 5.3.20 上各 3 次 = 36）全部在上界内，矩阵末行 `every outcome within max(trigger, 3 s) + 0.3 s: 236 of 236 (over the bound: 0)`。因此没有触发「低负载复跑确认 / 停下」流程。
2. 有放宽重跑的结局共 198 个（T_trigger 0.094 s 到 2.998 s），W 最大 3.060 s（apply-heavy-cjk，T_trigger 约 2.0 s，上界 3.300 s），离上界最近余量 0.240 s；三个 bash 版本一致（5.0.18 最大 3.053、5.2.15 最大 3.060、5.3.20 最大 3.058，余量 0.247 / 0.240 / 0.242 s）。
3. 有重跑且 W >= 2.99 s 的结局 110 个（基本都是被 3 s 硬截止终止后回落尺寸文案）：W 中位 3.017 s（5.0.18 3.025 / 5.2.15 3.017 / 5.3.20 3.019），比 3.000 s 多 17 ms（中位）到 60 ms（最大）；多字节形状略晚（中位 3.027 对 3.017）。其余 88 个有重跑的结局 W < 2.99 s，是自己提前结束（放行、longline / growth / tmax / finding 文案，或检查点放弃后回落尺寸文案）。
4. 没有进程残留：每次运行后按 cwd 扫描，236 次加补充运行 0 次发现残留；另用 stderr 走管道读到 EOF 的方式量了 6 次（multiline-cred 3.018 / 3.019 / 3.022 s，apply-heavy-cjk 3.046 / 3.052 / 3.048 s），与写文件的量法一致，没有后台进程握住管道。
5. 没进入重跑的结局（38 个）不受上界约束，但其中 23 个 W > 3 s，单列在第 5 节；与基线 hook（59e333c，sha e83c5e30f2cc）对照，耗时相同，是 #228 的基线首遍缺口，不是本变更引入。
6. 附带观察（不违反判据）：重跑来不及完成时，用户得到的仍是和以前一样的尺寸拦截文案，但要多等 2.3 到 3.0 s（见第 6 节）。

## 2. 做法

1. 埋点副本：`mkdbg31.py` 生成 `impl-dbg.sh`（c329a5b830af），`diff` 核对为 +3 -0（relax-start / relax-joined / firstpass-done 三行探针）；脚本每次启动都重新生成并重新核对，不是 +3 -0 就中止，hook 的 sha 不是 af4658b6f935 也中止。
2. 量法同 `v3/matrix.sh`：一次端到端调用，JSON 经管道进 stdin，stderr 写文件，HOME 与 cwd 为每次新建的临时目录，`env -u SECRET_GUARD_RAW_GATE -u CLAUDE_PROJECT_DIR -u SECRET_GUARD_TIME_BUDGET_S`，默认 `LC_ALL=C.UTF-8`，`timeout 60`；W = 启动前到进程退出的墙钟（EPOCHREALTIME，微秒整数运算）。T_trigger = 同一次运行里第一个 relax-start 相对启动的时刻；没有 relax-start 的结局 T 取 W 本身（`run-evidence.sh` W12 的写法）。全部命令在 `taskset -c 0,1 nice -n 19` 下。
3. 形状 40 个情形：gen-v3.py 的 8 个；`w14-shapes.py` 的 26 个自有形状；另有同一形状换环境的 6 个（`cjk-bytes-lmax@C` 在 LC_ALL=C，`multiline-cred / assign-storm / late-core3` 的 `@en_US` 在 LC_ALL=en_US.UTF-8，`km-ext / km-ext-small` 的 `@ext` 带项目扩展目录，此时放宽关闭，按设计不进重跑）。每个形状想测什么写在 `w14-shapes.py` 的清单里，也逐节抄在矩阵文件里。对应任务书点名的方向：
   - 多个各自超过 8192 的分段：multi-big-seg（7 段，各 8308 字符）、tmax-edge（8 段，到 TMAX）、f5like；
   - 增长量贴 GMAX：gmax-exact（恰为 8192，放行）、gmax-over（8193，growth 文案）；
   - 长行贴 LMAX 上下：lmax-below（3 行 x 8192）、lmax-race（再加一条 4000 字符行，使重跑耗时刚好压着截止）、lmax-above（有一行 8193）、late-long3 / late-near3（8431 / 8611 字符行）、cjk-lines-lmax、cjk-bytes-lmax；
   - 计数在旧上限附近及远超：caps-old-limits（第 17 个赋值才是路径、9 个 for 列表、9 次引用）、assign-storm（3000 赋值）、forlist-storm（250 个 for 列表）、repl-storm（15000 次引用）；
   - 多字节：repl-storm-cjk、cjk-lines-lmax、cjk-bytes-lmax（含 C 区域）、degrade-late、apply-heavy-cjk；
   - 整串与分段混用：degrade-late（降级的子 shell 出现在最末）、整串形状（前置 `(true);`）对分段形状；
   - 基线首遍本身就慢、触发点晚：late-core2 / late-core3 / late-core4 / late-near3 / late-long3 / late-core2-storm、many-segs、seg-late2、seg-assign-1700；
   - 现实形状：heredoc-vars（30 KB 未加引号的 heredoc，每行两个变量引用）。
   整串形状占多数的原因：分段模式下大命令的基线首遍极慢（见第 5 节），重跑根本进不去；整串（前置子 shell）时切分器立刻放弃，首遍很快，重跑的开销才暴露出来。
4. 每个形状在 PATH 上的 bash 5.2.15 跑 5 次。「最重 4 个」任务书没有定义，我两种读法都跑了（并集 6 个）：A = 有重跑的形状里中位 W 最高的 4 个（apply-heavy-cjk、repl-storm-cjk、multiline-cred、apply-heavy；这些形状大多终于截止 3.0 s，彼此差在毫秒级，排名等于噪声）；B = 全部形状里中位 W 最高的 4 个（seg-late2、seg-assign-1700、apply-heavy-cjk、repl-storm-cjk）。这 6 个在 5.0.18 与 5.3.20 上各跑 3 次。
5. INV-7：一个批 = 一个情形在一个 bash 下的全部运行。每批开始前等到 1 分钟负载 < 1.2（全部批开跑前读数 1.10 到 1.19，共等待 925 s，分布在 36 个批前），批首批尾各记一次 /proc/loadavg；任一 1 分钟读数 >= 2.00 即作废重跑（共 1 次：seg-late2 在 5.0.18，1.16 到 2.18，第二次通过）。已接受的批里 1 分钟负载最大 1.77，5 分钟最大 1.55，15 分钟最大 1.61，三个字段都 < 2。
6. 总用时 27.5 分钟（20:49:32 到 21:17:01 UTC）。重跑整个矩阵：`cd /tmp && taskset -c 0,1 nice -n 19 bash <impl>/w14-matrix.sh full`。
7. Rule #7：凭据形路径只在运行时拼装（`"aw" + "s/cred" + "entials"`），源码与矩阵文件里没有字面路径；输出里只有文案种类与耗时，没有读取过任何 stderr 内容到对话。清理按自记标记：运行目录名带本脚本 PID，残留扫描只认 cwd 在这些目录里的进程，没有发现需要清理的进程。

## 3. 按结局类型分组（bash 5.2.15，200 个结局）

| 文案种类 | 重跑 | 情形 |
|---|---|---|
| size-whole / size-seg（重跑终于截止，回落到基线尺寸文案） | 全部 | apply-heavy, apply-heavy-seg, apply-heavy-cjk, f5like, lmax-race, multiline-cred, assign-storm, forlist-storm, repl-storm, repl-storm-cjk, late-core2, late-core3, late-core4, late-core2-storm, heredoc-vars, 以及 multiline-cred / assign-storm / late-core3 的 en_US 版 |
| allow（重跑在截止前判完放行） | 全部 | shrink, km-ext, lmax-below, gmax-exact, caps-old-limits, cjk-lines-lmax, cjk-bytes-lmax（含 @C）, many-segs, degrade-late, multi-big-seg |
| longline / growth / tmax / finding（重跑自己给出文案） | 全部 | lmax-above, gmax-over, tmax-edge, segfinding |
| 临界混合 | 部分 | late-near3（5 次里 4 次进重跑；1 次首遍 3.44 s 才结束，无重跑，W 3.471 s）、late-long3（重跑多在 2.78 到 2.97 s 开始并在 0.05 s 内给出 longline，有 1 次在 2.967 s 才开始，只剩不到 0.05 s，被截止杀掉后回落 size-whole） |
| 无重跑 | 0 | km-ext-small（放行）、km-ext@ext、km-ext-small@ext（扩展生效，放宽关闭）、seg-assign-1700、seg-late2 |

## 4. 每个情形一行（bash 5.2.15，5 次；矩阵文件里有逐次的 rc / W / T_trigger / 上界 / 是否越界 / 批首尾负载）

| 情形 | 有重跑的次数 | 文案种类 | W 最小 / 中位 / 最大 (s) | T_trigger 范围 (s) |
|---|---|---|---|---|
| apply-heavy | 5/5 | size-whole | 3.017 / 3.019 / 3.021 | 0.373..0.454 |
| apply-heavy-seg | 5/5 | size-whole | 3.018 / 3.019 / 3.025 | 0.398..0.542 |
| apply-heavy-cjk | 5/5 | size-whole | 3.041 / 3.048 / 3.060 | 1.983..2.094 |
| shrink | 5/5 | allow | 0.154 / 0.158 / 0.160 | 0.094..0.102 |
| segfinding | 5/5 | finding | 1.117 / 1.160 / 1.204 | 0.676..0.741 |
| f5like | 5/5 | size-seg | 3.014 / 3.015 / 3.017 | 0.717..0.743 |
| km-ext | 5/5 | allow | 0.235 / 0.248 / 0.253 | 0.142..0.158 |
| km-ext-small | 0/5 | allow | 0.073 / 0.075 / 0.078 | - |
| lmax-below | 5/5 | allow | 2.748 / 2.871 / 2.892 | 0.153..0.163 |
| lmax-race | 5/5 | size-whole | 3.015 / 3.016 / 3.018 | 0.167..0.211 |
| lmax-above | 5/5 | longline | 0.222 / 0.229 / 0.268 | 0.150..0.187 |
| gmax-exact | 5/5 | allow | 1.674 / 1.728 / 1.792 | 0.137..0.167 |
| gmax-over | 5/5 | growth | 0.202 / 0.204 / 0.212 | 0.140..0.154 |
| caps-old-limits | 5/5 | allow | 2.101 / 2.154 / 2.243 | 0.184..0.194 |
| multiline-cred | 5/5 | size-whole | 3.016 / 3.020 / 3.021 | 0.307..0.519 |
| assign-storm | 5/5 | size-whole | 3.015 / 3.016 / 3.017 | 0.190..0.214 |
| forlist-storm | 5/5 | size-whole | 2.471 / 2.971 / 2.974 | 0.273..0.428 |
| repl-storm | 5/5 | size-whole | 3.017 / 3.018 / 3.020 | 0.226..0.254 |
| repl-storm-cjk | 5/5 | size-whole | 3.020 / 3.023 / 3.027 | 0.472..0.569 |
| cjk-lines-lmax | 5/5 | allow | 1.159 / 1.208 / 1.713 | 0.704..0.974 |
| cjk-bytes-lmax | 5/5 | allow | 0.704 / 0.720 / 0.724 | 0.271..0.295 |
| late-core2 | 5/5 | size-whole | 3.014 / 3.015 / 3.022 | 1.722..1.885 |
| late-core3 | 5/5 | size-whole | 3.016 / 3.017 / 3.020 | 2.622..2.969 |
| late-core4 | 5/5 | size-whole | 3.015 / 3.015 / 3.016 | 2.744..2.901 |
| late-near3 | 4/5 | size-whole,longline | 3.006 / 3.016 / 3.471 | 2.944..2.998 |
| late-long3 | 5/5 | longline,size-whole | 2.869 / 2.897 / 3.019 | 2.778..2.967 |
| late-core2-storm | 5/5 | size-whole | 3.016 / 3.017 / 3.023 | 1.983..2.089 |
| seg-assign-1700 | 0/5 | size-seg | 6.805 / 6.951 / 7.029 | - |
| seg-late2 | 0/5 | size-seg | 10.794 / 10.901 / 11.458 | - |
| many-segs | 5/5 | allow | 2.703 / 2.766 / 2.817 | 1.900..1.967 |
| degrade-late | 5/5 | allow | 0.428 / 0.460 / 0.549 | 0.329..0.447 |
| multi-big-seg | 5/5 | allow | 0.907 / 0.948 / 1.026 | 0.678..0.741 |
| tmax-edge | 5/5 | tmax | 1.016 / 1.026 / 1.043 | 0.777..0.797 |
| heredoc-vars | 5/5 | size-whole | 2.801 / 2.971 / 2.975 | 0.251..0.295 |
| cjk-bytes-lmax@C | 5/5 | allow | 0.396 / 0.403 / 0.434 | 0.102..0.116 |
| km-ext@ext | 0/5 | size-whole | 0.150 / 0.157 / 0.196 | - |
| km-ext-small@ext | 0/5 | ext-finding | 0.097 / 0.107 / 0.122 | - |
| multiline-cred@en_US | 5/5 | size-whole | 3.016 / 3.018 / 3.021 | 0.318..0.364 |
| assign-storm@en_US | 5/5 | size-whole | 3.014 / 3.017 / 3.018 | 0.193..0.216 |
| late-core3@en_US | 5/5 | size-whole | 3.014 / 3.015 / 3.023 | 2.737..2.862 |

### 跨 bash 版本（最重的 6 个形状；文案种类、有重跑的次数、最大 W）

| 形状 | 5.0.18（3 次） | 5.2.15（5 次） | 5.3.20（3 次） |
|---|---|---|---|
| apply-heavy | size-whole，重跑 3/3，最大 W 3.025 | size-whole，重跑 5/5，最大 W 3.021 | size-whole，重跑 3/3，最大 W 3.019 |
| apply-heavy-cjk | size-whole，重跑 3/3，最大 W 3.053 | size-whole，重跑 5/5，最大 W 3.060 | size-whole，重跑 3/3，最大 W 3.058 |
| multiline-cred | size-whole，重跑 3/3，最大 W 3.020 | size-whole，重跑 5/5，最大 W 3.021 | size-whole，重跑 3/3，最大 W 3.019 |
| repl-storm-cjk | size-whole，重跑 3/3，最大 W 3.031 | size-whole，重跑 5/5，最大 W 3.027 | size-whole，重跑 3/3，最大 W 3.026 |
| seg-assign-1700 | size-seg，重跑 0/3，最大 W 6.742 | size-seg，重跑 0/5，最大 W 7.029 | size-seg，重跑 0/3，最大 W 7.382 |
| seg-late2 | size-seg，重跑 0/3，最大 W 13.988 | size-seg，重跑 0/5，最大 W 11.458 | size-seg，重跑 0/3，最大 W 17.217 |

三个版本上文案种类完全一致，重跑终于截止的 W 相差在 10 ms 以内；差别只在没有重跑的基线首遍（seg-late2：5.0.18 最大 14.0 s、5.2.15 11.5 s、5.3.20 17.2 s）。

## 5. 没进入重跑、W 超过 3 s 的结局（单列；不受上界约束）

| 情形 \| bash | 次数 | W 范围 (s) |
|---|---|---|
| late-near3 \| 5.2.15 | 1 | 3.471 - 3.471 |
| seg-assign-1700 \| 5.0.18 | 3 | 6.601 - 6.742 |
| seg-assign-1700 \| 5.2.15 | 5 | 6.805 - 7.029 |
| seg-assign-1700 \| 5.3.20 | 3 | 6.983 - 7.382 |
| seg-late2 \| 5.0.18 | 3 | 13.487 - 13.988 |
| seg-late2 \| 5.2.15 | 5 | 10.794 - 11.458 |
| seg-late2 \| 5.3.20 | 3 | 14.097 - 17.217 |

1. seg-assign-1700（分段模式，1700 个赋值词，约 14 KB）与 seg-late2（分段模式，两行带字面路径的 8131 字符行加一个触发段，约 18 KB）的时间几乎全在 `_sg_core_eval`（firstpass-done 探针与 W 只差几十毫秒），这一段是基线原样代码。对照基线 hook（`git show 59e333c:hooks/secret-guard.sh`，sha e83c5e30f2cc），用 `v3/matrix.sh` 各跑 2 次：seg-late2 基线 11.18 / 10.76 s、实现 10.81 / 10.89 s；seg-assign-1700 基线 7.04 / 6.92 s、实现 7.28 / 8.60 s（后一个值那时负载升到 1.88）。结论：实现与基线同样慢，属 #228。
2. 这两个形状的耗时远超 hook 自己写的 Claude Code 5 s 超时（超时会让命令未经扫描通过），是 #228 缺口的具体样本：十几 KB 的分段模式命令就能到 7 到 17 s。校准阶段的单次试跑（不入矩阵，timeout 20 s，负载未闸）还见到：分段模式 26 KB（3000 个赋值词）首遍 18 s，11 KB 的 1000 个极短段 13 s，45 KB 的 15000 次引用、57 KB 的 300 个 for 列表、38 KB 的 3000 段引用加末尾子 shell 等 20 s 内跑不完。整串（前置 `(true);`）的同类命令首遍除了刻意放了 credit 行的 late-* 之外都在 0.1 到 1.5 s。
3. late-near3 的 1 次 W 3.471 s：首遍到 3.44 s 才结束，截止已过，没有重跑，直接回落基线文案。它与第 3 节的临界混合是同一个形状。

## 6. 附带观察（不违反判据，供上呈时参考）

1. 重跑来不及完成时，用户拿到的是与基线逐字相同的尺寸文案，但要多等：用 `v3/matrix.sh` 对照，heredoc-vars 基线 0.27 / 0.26 s、实现 2.34 / 2.95 s；multiline-cred 基线 0.31 / 0.32 s、实现 3.02 / 3.02 s。矩阵里终于截止的 110 个结局都是这个代价。这是硬截止设计的直接后果，不是缺陷，但「现实形状」heredoc-vars（30 KB heredoc，每行两个引用，增长 7250，在 GMAX 之内）在 5 次里 5 次没能判完（W 2.801 / 2.971 / 2.975 s 后回落尺寸文案），即放宽对这一类现实命令没有收益，只增加延迟。
2. 5.3.20 上的首遍普遍比 5.2.15 慢（credit 行密集的 late-near3 在 5.3.20 的有效块里 3 次有 2 次首遍已过截止、没进重跑，另外 3 次在作废块里全部如此；5.2.15 上 5 次里 1 次）。属基线首遍，不影响判据。
3. 补充运行（不入矩阵、不计入 236）：bash 5.0.18 上 late-near3 / late-core4 / late-long3 各 3 次（开跑 0.68、结束 0.98，有效）全部在上界内（late-core4 W 3.015 到 3.017 s；late-near3 与 late-long3 重跑在 2.56 到 2.76 s 开始，W 2.62 到 2.82 s）。bash 5.3.20 上第一块结束时负载 3.19，按 INV-7 作废；重跑（开跑 1.18、结束 1.60，有效）late-long3 5 次全部有重跑、W 2.91 到 2.99 s，late-near3 3 次里 1 次有重跑（T 2.952 s，W 3.016 s）、2 次首遍已过截止（W 4.322、3.193 s，无重跑）。作废块里出现过的一次 6.134 s 首遍在低负载重跑中没有再现，判为外部负载所致。
4. 校准阶段把形状从分段模式改为整串，是因为分段模式的基线首遍太慢（第 5 节）；校准、补充、对照三类运行都没有走批闸门，只有补充与对照记了开跑前后读数，结论里只引用了读数有效的那几块（对照块：开跑 0.75，结束 1.88；管道块：开跑 1.88 高于 1.2 的开跑线，结束 1.70，只作旁证）。

## 7. 拿不准 / 未完成

1. 「最重的 4 个形状」没有定义，取了两种读法的并集（6 个）；若期望严格 4 个，A 读法的 4 个是 apply-heavy-cjk、repl-storm-cjk、multiline-cred、apply-heavy。
2. 矩阵末行 `N of M`：W12 里同样的行是「N of M over the bound」（N 是越界数），按字面读又可以是「N 个在上界内」。我写成 `236 of 236 (over the bound: 0)`，两种读法同时给出。
3. T_trigger 取第一个 relax-start；236 个结局里没有一个出现过两个 relax-start，所以取第一个或最后一个等价。
4. INV-7 的「读数」我按 1 分钟字段判，同时核了 5 / 15 分钟字段（已接受的批里最大 1.55 / 1.61，均 < 2），两种读法下结论相同。「批」我定义为一个情形在一个 bash 下的全部运行。
5. 未覆盖：CPU 争用下的运行（INV-7 禁止同时跑第二个重负载；截止后 0.3 s 余量在争用下是否够用没有测）；hook 被 `sh -c` / zsh 拉起再 re-exec 到 bash 的路径（P0 在 re-exec 之后记，外层 shell 的启动时间不在 3 s 内）；非 x86_64 Linux 或 bash 5.0 到 5.3 之外的版本（放宽按设计关闭）；`SECRET_GUARD_TIME_BUDGET_S` 取其他值。
6. 量法限制：nice 19 加 2 核的结果与不降优先级的运行不一定可比；主机是共享的（外部负载在 0.7 到 3.2 之间波动，已用闸门与作废规则处理）；残留进程的扫描靠 cwd，若有进程自行 `cd` 离开则扫不到（管道量法作了侧面印证）；埋点探针本身的开销（三次 printf）未单独量，但未埋点的实现在 multiline-cred 上 3.02 s，与埋点副本的 3.018 到 3.021 s 一致。
7. 多字节形状的截止后开销比 ASCII 形状大约多 10 ms（apply-heavy-cjk 3.046 到 3.060 s），原因没有查。
8. 工具调用共 30 次（含读任务书，未到 40 次的收尾线）。

## 8. 文件

- `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-matrix.sh`
- `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-shapes.py`
- `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/W14-timing-matrix.txt`
- 本报告：`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T003b-report.md`
- 原始数据（微秒）：scratchpad 的 `r217impl/t003b/rows.tsv`（列：bash 版本、情形、尝试、序号、rc、文案、W、T_trigger、重跑数、job 时长、首遍、上界、越界、残留、状态），埋点副本 `impl-dbg.sh`，输入 `shapes/`，对照输出 `cmp-base.txt` / `cmp-impl.txt`。
