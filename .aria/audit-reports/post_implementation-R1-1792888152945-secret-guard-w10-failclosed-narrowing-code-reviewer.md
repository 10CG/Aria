---
checkpoint: post_implementation
mode: single-seat
rounds: 1
converged: true
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-25T00:29:12.945Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [code-reviewer]
reviewed_sha: 2893bcc
reviewed_hook_sha256_prefix: af4658b6f935
---

# post_implementation R1（单席 code-reviewer）— secret-guard W10 尺寸误拦收窄（10CG/aria-plugin#217，TASK-005）

> **Verdict：PASS**。0 Critical / 0 Major / 6 Minor，另列 3 条疑点。审查对象 aria `2893bcc`（worktree 实测 `hooks/secret-guard.sh` 的 sha256 前缀为 `af4658b6f935`），改动面 `8614066..2893bcc -- hooks/`（6 个文件，+1361 / −97）。规格来源：任务书 `r217impl/BRIEF-T005.md`。

## 审查范围与方法

- 读：hook 的全部 diff（17 个 hunk）与相关上下文；套件 diff 里的 W10 块头、六组（21ab / 21ac / 21ag / 21aj / 21al / 21ao）的注释与标题、wpa_x6 的回落判据；helper `hooks/tests/lib/secret-guard-w10-direct.sh` 的头注释、V2-G5 至 G18、V5-S10 一段与 V14；`hooks/tests/lib/sg-shim/delay-first`；`v31/sc-direct.sh` 的 root 探测分支。
- 规格：proposal What 1-7 及各补充、P1-P10、R-a / R-b / R-c、残余 1-9；detailed-tasks.yaml 的 INV-1 至 INV-9 与 TASK-005。
- 探针：`r217impl/t005/probe.sh`，只跑一次（`taskset -c 0,1 nice -n 19`，负载 1.77 → 1.79），被测 hook 即 worktree 里的 `2893bcc`。没有跑整轮，也没有跑坏实现。探针输出摘录写在各条发现里。

## 阶段 1：规格符合 — PASS

| 项 | 结论 | 依据 |
|---|---|---|
| INV-1 | 抽查通过 | What 1 补充（`_sg_relax_ok` / `_sg_relax_platform`，hook :819-830）、What 6（`_sg_vx_collect` 链式循环删的那一行）、What 7 补充四处（hook 头 :87-105、W10 块头 :584-585、`_sg_vx_replace` 说明、重跑块头两行）与 proposal 字面逐字一致。`v31/impl/W8-v31.diff` 页眉记的 hook 前缀就是 `af4658b6f935`。 |
| INV-3 | 通过 | 所有放宽分支都以 `_SG_RELAXED` 非空为条件（`_sg_vx_replace` :635、`_sg_vx_collect` :647、`_sg_vx_apply` :693，以及 `_sg_vx_pass` :724 里的三个检查点和两处 `_sg_vx_big_judge` 路由）。该标志只在作业里置位（:845），顶层 :189 清空，不取自环境。触发点只有 :751（整串）与 :775（分段），而且只在 `_sg_relax_ok` 成立时返回 4。其余改动（`_sg_judge_one` 第三参数缺省为空、`_sg_emit_blocked` 新增的 longline 分支、What 6 的死代码、注释、顶层两变量）不改变触发点之外的退出码与 stderr。准入门不成立时只多一次只读的 `/proc` 读和一次 stat；`_sg_relax_noext` 在命令替换里运行并带 `2>/dev/null`，所以输出逐字节不变。 |
| INV-4 | 通过 | 新函数 `_sg_vx_big_judge` 到 `_sg_relax_run` 位于 :801-862，`_sg_emit_blocked` 在 :940，全在 source 闸门 :1057 之上。 |
| What 1 | 一致 | 两个顶层变量紧跟在 `set -uo pipefail` 之后（:188-189）；准入门与 proposal 的字面代码块逐字一致；`_sg_relax_platform` 的每个参数都带缺省。 |
| What 2 | 一致 | 增长上限按输入长度算（:695，取 `${#1}`）；三个计数上限在重跑里设为 1,000,000；`_sg_vx_big_judge` 用线性循环量最长行，循环一次没跑就按超长处理；不超过 SMAX 的副本走普通判定；VMAX / TMAX 照旧；三个检查点在重跑里返回 3；`nocredit` 位于 W12 中和之后、算 credit 之前。 |
| What 3 | 一致 | `exec 2>/dev/null; set -m`；自检读 `/proc/$BASHPID/stat` 在 comm 之后的第 3 个字段（pgrp）；计时器写成 `sleep …; kill …`，并用 `kill -0` 确认它在跑；退出码 77 / 2 / 1；`wait` 之后再杀一次组。 |
| What 4 | 一致 | :1687-1692：返回 4 时用 `_SG_OV_PAT` / `_SG_OV_MODE` 写 oversize 文案并返回 2；放行时直接返回 0，跳过扩展腿。 |
| What 5 | 一致（另见 m-1） | 两条增长文案与表格逐字一致；longline 的 heredoc 与 proposal 正文逐字一致，没有追加 Triggering segment 行。 |
| 失败即关 | 通过（附疑点 D-3） | 逐条核过：作业不是以 77 退出（:860-862）、截止（SIGKILL，状态 137）、检查点（3 → 1）、自检（9）、读不到 `/proc/$BASHPID/stat`（9）、计时器没起来（9）、`$!` 为空（99）、run 里再查时间（:851）、拦截却没有文本——这些都返回 4，由 :1690 写基线的 oversize 文案。`/proc/sys/kernel/osrelease` 读不到时准入门关闭。`_sg_per_segment_eval` 在顶层的子 shell 里运行，0 和 2 以外的状态一律按内部错误拦（:1728-1737），所以 4 不会漏成放行。放行只有一条路：作业以 77 退出，而 77 只来自 `_sg_vx_pass` 返回 0（:847、:860）。计时器 fork 失败时，bash 要重试约 15 s 才中止作业，会超过 CC 的 5 s；proposal What 3 已按 PP1-A4 把它申报为与基线 fork 失败同类，这里不重提。 |

## 阶段 2：代码质量与安全

### 优点

- 放行只有一条窄路（作业退出码 77）。其余一切，包括 `wait` 对继承来的旧 PID 返回的裸 0、拦截却没有文本，都回落到基线。命令替换的结果用不带 local 的普通赋值接住，退出码不会被吞掉（:852、:859）。
- 放宽标志只在后台作业的子 shell 里置位，顶层清空、不取自环境（:189、:845），重跑规则不可能在父进程里生效。
- 计时器在判定之前起、在作业的进程组里、对整组发 KILL，`wait` 之后再杀一次组。我对照 bash 源码核了一点：后台运行的函数（`_sg_relax_job … &`）在子进程里会调用 `without_job_control()`，所以计时器和判定 fork 出的进程都留在作业的组里，组杀覆盖得到。
- `_sg_vx_big_judge` 的哨兵（读循环一次没跑就按超长处理）把 here-string 失败之类的异常导向更严的 nocredit 路径。
- 准入门只用 `BASH_VERSINFO` 和 `/proc` 的只读信息，WSL 环境变量只能把门关上；每个参数都带缺省，`set -u` 下少传参数不会让调用方中止。
- 注释里引用的编号（P、What、R-*）都对得上。套件六组的「Red when」写清了两支各自的红条件；wpa_x6 的 F1 / F2 / F3 推导与 hook 一致（F2 如实写了 kill 落在 `_SG_P0` + 3 s 之后）。

### Critical

无。

### Major

无。

### Minor

**m-1 R-c 漏申报了一类拦截文案：重跑里的 VMAX 原因串**

- 位置：hook :649-650（重跑里 ca / cf 设为 1,000,000）与 :733-736（`_sg_vx_collect` 返回 2 时写 VMAX 文案，重跑里不改道）。
- 问题：基线那一遍只收集前 16 个赋值和前 8 个 for。触发点上的大命令，如果第 17 个以后的赋值（或第 9 个以后的 for 列表）超过 4096 字符，基线那一遍看不到它，按 SMAX 拦。重跑收集全部赋值，撞上 VMAX，拦截原因变成 a variable value is longer than 4096 characters。proposal 的 R-c 与 What 5 只列了四类文案变化：增长、TMAX、longline、普通命中。
- 实测（probe.sh P1：16 个短赋值后接一个 4100 字符的值，加一个约 12 KB 的分段副本）：
  - 准入门开：exit 2，`Limit hit: a variable value is longer than 4096 …`
  - 准入门关（设 WSL_DISTRO_NAME）：exit 2，`Limit hit: a command segment is longer than 8192 …`
- 为什么要紧：退出码不变，仍然是拦，不涉及安全。但这是一个没申报的文案变化：照 R-c 写的 CHANGELOG 会漏这一项，读文案的人（包括 AI）拿不到完整的「可能看到哪些原因」。
- 修法：在 What 5 的表、R-c 和 CHANGELOG 里加一行「重跑里任一值超过 4096：VMAX 原因串（oversize 模板）」。代码不用改：What 2 已经写明 VMAX 在重跑里不变。

**m-2 几处注释说得比代码宽，有一处与代码相反**（brief 第 3 项；commentsync 只核有没有，不核对不对）

1. hook :92-98（What 7 补充 3，proposal 字面）与套件 :2879-2880（W10 块头）都说 a copy over 8192 characters is blocked for its size **only where** the relaxed rerun is not in effect。实际上放宽生效时，截止、检查点、自检等回落同样按尺寸拦（基线 oversize 文案，P6），m-1 那一类则按 VMAX 拦。hook 那句的后半（the deadline or any failure of the rerun still blocks）与前面的「only」自相抵触；套件块头要到 :2927 才讲截止回落。建议把「only where … not in effect」改成「where … not in effect, and whenever the rerun falls back」，proposal What 7 补充 3 同步改（按 INV-1 先改规格）。
2. hook :599（LENGTH BUDGET 块）：Elsewhere, and whenever the rerun does not finish in time, the command is blocked with the size text。这里只举了截止一种回落；自检、计时器没起来、内部错误、裸 0、拦截却没有文本也都回落。不算失实，是说得不全。建议写成 whenever the rerun neither allows nor blocks on its own (the deadline, a checkpoint, any failure)。
3. hook :831（`_sg_relax_noext` 的行尾注释）：A file in any state, **or an error, keeps the relaxation off**。取项目根时 jq 出错，`_sg_ext_root` 输出空串，本函数照样打印 none，放宽是**开**的；这正是 proposal What 1 表（PP2-m7）要的行为，注释把它说反了。实测（probe.sh P6，stdin 是带 cwd 键的畸形 JSON）：输出 `[none]`。只有函数自身在命令替换里中止（例如 `set -u`）时才没有输出、门才关。建议改成：a file in any state keeps the relaxation off; no project root (also when jq cannot read the cwd) counts as no extension, as in the extension leg。
4. hook :720（`_sg_vx_pass` 的说明）：the baseline block **text** is kept in `_SG_OV_PAT` / `_SG_OV_MODE`。存的其实是原因串和模式，文案在回落时由 `_sg_emit_blocked` 重新生成（:1690）。措辞小问题，建议改成 the baseline reason and mode are kept。

其余各处逐一对过代码，都准确：hook 的 W10 块头新两行（:584-585）、`_sg_vx_replace` / `_sg_vx_apply` 的说明、时间预算块（its checkpoints fall back to the size block, never to the time text）、`_sg_emit_blocked` 的说明（time 文案确实只回显前 200 字符，:944-958）、`_sg_judge_one` 的说明、`_sg_per_segment_eval` 的 Order 段、重跑块头；套件六组的注释与标题（21ab 三条命令的长度、21ac 的约 6 KB 与 8 KB、21al 增长约 5.4 KB、21ao 约 4 KB、21aj 约 12 KB，都与 wpa_* 构造器一致）；wpa_x6 的 F1 / F2 / F3 推导。关于 no count bound：代码里是 1,000,000（:637、:650、:695），proposal 残余 9 已申报；要到达这个数需要几 MB 的命令，截止远在它之前，注释里 the deadline caps its cost 成立，不记为发现。

**m-3 V2-G12 / V2-G13 只验了关门一极，名字和注释却说成「触发点问了准入门」**（brief 第 4 项）

- 位置：helper :136-145（`v31/sc-direct.sh` 同段）。注释 both trigger points ask the gate (R2 PP2-D)，以及 id 里的 trigger-asks-gate。
- 问题：两例把 `_sg_relax_platform` 桩成失败，断言结局是「2 oversize，绝不 4」。一个**从不问**准入门、永远照基线拦的触发点也能通过这两例；「问了门」要靠 V14-G1（门桩成开，要求 4）才钉得住。注释冒号后面那半句是准确的，标题那半句过宽。
- 为什么要紧：读用例清单的人会以为 G12 / G13 单独就钉住了「触发点调用准入门」。哪天 V14-G1 被删掉或降成 SKIP，不会有人意识到开门一极已经没人管。
- 修法：id 保持不变（证据链已经引用它们），只改注释和 chk 文案，例如 with the gate closed both trigger points keep the baseline size block, never 4 (the closed pole; the open pole, status 4 with the gate open, is V14-G1)。

**m-4 root 探测的快路径与 getrlimit(2) 的判据不一致（只会假红，不会假绿；uid 0 下不误判）**（brief 第 2 项）

- 位置：helper :252-257 的 `nproc_binds`；`v31/sc-direct.sh` :230-235 是同一段。
- 问题：按 getrlimit(2)（以及 kernel/fork.c 的 copy_process），RLIMIT_NPROC 对**真实** UID 为 0、或持有 CAP_SYS_RESOURCE / CAP_SYS_ADMIN 的进程不生效。快路径用的是 `id -u`（**有效** UID）；CapEff 则交给 awk 去读 /proc 下 self 那一项的 status 文件，而 self 在 awk 里指的是 awk 自己的进程，不是要 fork 计时器的那个 bash。实测（probe.sh P3）：bash 的 PID 是 1284891，awk 从同一文件读到的 Pid 是 1284978。awk 经 execve 启动，非 root 时只保留 ambient 集里的 capability。所以在 bash 有、awk 没有这些 capability 的环境里（文件 capability），以及真实 UID 与有效 UID 不同的环境里，快路径会判成「受限」并跳过探针。
- 后果：只出现在这些少见环境里：V5-S10 / V5-S10b 照常运行，但 `ulimit -u 1` 实际不生效，计时器 fork 成功，桩判定被调用，两例 FAIL（假红）。反方向——把受限误判为不受限——不会发生，那个方向由第 255 行的真实 fork 探针决定，它才是权威。
- uid 0：真 root 时 `id -u` 为 0，快路径不命中；探针 fork 成功，判为不受限，SKIP [root]，正确。user namespace 里的「root」（宿主上不是 0）：探针 fork 失败，判为受限，照常运行，也正确，因为这种环境下限制确实生效。
- 修法：快路径改用 `id -ru`，CapEff 改由 bash 自己用 read 循环从 `/proc/$BASHPID/status` 读；或者干脆去掉快路径，只留探针（sh 是 dash 时 fork 失败是即时的）。注释里的 It does not for uid 0 改成 real user ID 0。

**m-5 计时器的截止比 `_SG_P0` + min(预算, 3) s 晚一段 fork 延迟**

- 位置：hook :851 在 `_sg_relax_run` 里算出 `_SG_LEFT`；:852-853 才 fork 命令替换和作业，:838 读 `/proc`，:842 才起 `sleep "$_SG_LEFT"`。
- 问题：kill 实际落在 `_SG_P0` + cap +（起计时器的时刻 − 算 `_SG_LEFT` 的时刻）。proposal What 3 写的是「截止：`_SG_P0` + min(…) 秒，微秒精度」，说得略宽；套件 F2 那段已经如实写了 the kill comes after `_SG_P0` + 3 s。
- 为什么要紧：低负载下只差毫秒；高负载下 fork 可能要上百毫秒，叠加在 P3 的 ε 上。ε 的实测已经包含这一段（负载约 10 时 0.2-1.2 s），离 CC 的 5 s 还有约 2 s 余量，所以只是精度问题，不是放行风险。
- 修法：在作业里起计时器之前再调一次 `_sg_relax_left`（失败就以 9 退出），让 sleep 从真正的起点量剩余时间；或者在 proposal What 3 / P3 里把这段延迟明确写进 ε。

**m-6 有三处性质只被计时类端到端用例抓住，缺与负载无关的直调用例**（brief 第 5 项；建议补，详见下面「第 5 项」）

- 不记为 Major 的理由：覆盖是有的，负载达到 2 时整批 SKIP 是显式计数的，不是静默；INV-7 要求发版前的证据轮在低负载窗口里跑。缺的是「忙机器上的回归轮次也看得住」这一半。

### 疑点（未核实，单列）

**D-1 WSL 互操作标记的名字。** 较新的 WSL 在启用 systemd 的发行版上，可能把 binfmt 项登记为 `WSLInterop-late`；只认 `WSLInterop` 会漏看。只有在「自编内核（内核串里没有 microsoft / WSL）、进程环境里也没有 WSL_DISTRO_NAME / WSL_INTEROP」的 WSL2 上，放宽才会因此误开（等于在没实测的平台上放宽，违背裁定 E）。本机不是 WSL，无法核实。低成本加固：改成看 `/proc/sys/fs/binfmt_misc/` 下有没有以 WSLInterop 开头的项。这一项无论怎么读，都只能把放宽关掉，不能打开；竞态（项在两次读之间出现或消失）只会让同一条命令在基线与放宽之间切换，两边的结局都不越出规格。

**D-2 `/proc/sys/fs/binfmt_misc` 的自动挂载。** 多数 systemd 宿主把它设成 autofs 自动挂载点；`-e` 穿过它时会触发挂载。正常情况下挂载在毫秒内完成，而且开机后通常已经挂上。但如果自动挂载没人服务（有报告见于部分继承了宿主 autofs 挂载点的容器或 chroot），stat 可能一直阻塞，hook 超过 CC 的 5 s 被杀后就放行了——而这条命令基线本来会按尺寸拦。本容器的 mountinfo 里既没有 binfmt_misc 也没有 autofs（probe.sh P4），无法核实。建议：先看挂载表里是否已经挂着 binfmt_misc 再去 stat（读挂载表不会触发自动挂载）；并把这项检查挪到 `_sg_relax_platform` 的廉价判据之后，让非 x86_64、非 bash 5.0-5.3 的平台根本不碰它（现在 :823 在平台判据之前，任何平台的触发点都会执行它）。若属实，这是放宽引入的新放行路径，建议发版前在一台真实的 systemd 宿主上确认，或者先做上面的加固。

**D-3 以状态 2 退出的 bash 内部致命错误。** bash 的 fatal_error（例如 xmalloc 分配失败）以状态 2 退出，并往 stderr 写报错。这发生在作业里时，`_sg_relax_run` 会把它当作「2 且有文本」原样写出：结局仍是拦，不会放行，但文案是 bash 的报错而不是基线的回落文案，与重跑块头 an internal error … falls back to the baseline block, byte for byte 的说法不符。这一点依赖 bash 的内部实现，没有实测。若属实，最小的处理是改那句注释；让作业的拦截改用专属退出码再在 run 里映射成 2，则需要先改 proposal P4。

## 第 5 项：三处要不要补与负载无关的直调用例——建议补

理由：这三处现在只靠计时类端到端用例抓；按 INV-7，负载达到 2 时它们整批 SKIP，所以在忙机器上的回归轮次里事实上没人看着。三处都能写成确定性的直调检查，每条只要几行：

1. **计时器睡的是 `_SG_LEFT`。** 在 source 过 hook 的 shell 里定义一个 sleep 函数（子 shell 会继承），把第一个参数写进文件后再 `command sleep`；桩掉 `_sg_relax_left`，让它把 `_SG_LEFT` 设成一个独特的值（例如 1.234567）；桩判定立即返回 0；调 `_sg_relax_run`，断言记下的参数恰好是 1.234567。坏实现（`sleep 3`、`sleep "$_SG_TIME_BUDGET"`）立即变红，与负载无关。
2. **锚点 `_SG_P0` 只在 hook 起点取一次。** （a）静态检查：hook 里给 `_SG_P0` 赋值的地方恰好一处，而且就在 `set -uo pipefail` 的下一行。（b）直调检查：用 awk 把 `_SG_P0` 设成「现在 − 2.5 s」（V2-G6 的写法）；桩作业把它看到的 `_SG_LEFT` 写出来，然后以 77 退出；调 `_sg_per_segment_eval` 让它走到触发点；断言 `_SG_LEFT` 不超过 0.5 s。任何在准入门、run 或作业里重新取锚点的坏实现都会给出约 3 s。中间有 2.5 s 的余量，负载只会让这个值更小，不会让结果翻转。
3. **命令替换里的 `exec 2>/dev/null`。** 桩作业为 `kill -KILL "$BASHPID"`（效果与截止相同），断言 `_sg_relax_run` 返回 4 且 stderr 为空。我已经用探针核实这条能分辨好坏（probe.sh P2）：真实现 stderr 为空、返回 4；去掉 `exec 2>/dev/null` 的坏实现，stderr 多出一行 `kill: (-1284970) - No such process`（`wait` 之后的组杀撞上一个已经空了的组），同样返回 4。端到端用例看到的是 P6 字节比对失败，直调用例看到的是 stderr 不为空。

原有的计时类用例要保留：它们验的是整条链在真实时间里成立；直调用例补的是与负载无关的那一半。

## 第 6 项：其余

- 作业、计时器与进程组：除 m-5 外没发现问题。hook 如果在截止前被外部杀掉，作业和计时器在自己的进程组里最多活到截止（计时器照常杀组），之后不留任何进程；作业的标准输出是命令替换的管道，父进程不在时再写会收到 SIGPIPE。`wait` 返回后组杀撞上 PID 复用的窗口只有微秒级，与 proposal「竞争窗口」一节同类，可以忽略。
- `set -u`：新代码对可能为空的量都带了缺省（`${!:-}`、`${f[2]:-}`、`${BASH_VERSINFO[5]:-}`、`${EPOCHREALTIME:-}`）；BASHPID 只在准入门要求 bash 5.x 之后才用到，bash 3.2 上的解析与运行不受影响。
- 子 shell 与命令替换里的状态：`_SG_OV_PAT` / `_SG_OV_MODE` 在父进程里写（`_sg_vx_pass` 不在子 shell 里调用），回落时可用；重跑的所有状态都留在作业里。
- 性能上界：触发点之外只多一次顶层赋值；准入门关时多一次只读的 `/proc` 读和一次 stat；平台与时间都满足时才多一次命令替换（取项目根，可能 fork 一次 jq）。重跑的成本由截止封顶。
- 可维护性：1,000,000 在三处重复（:637、:650、:695），建议提成一个具名常量（例如 `_SGV_RELAX_NMAX`），与 `_SGV_GMAX` / `_SGV_LMAX` 放在一起。不影响行为，不记为发现。

## 建议汇总（按优先级）

1. 补第 5 项的三条直调用例（m-6）。
2. 确认或加固 D-2（若属实，是放宽带来的新放行路径）；顺手做 D-1 的加固。
3. 在 proposal What 5、R-c 和 CHANGELOG 里补 VMAX 那一行（m-1）。
4. 改 m-2 的四处注释。其中第 1 处是 proposal What 7 补充 3 的字面，按 INV-1 要先改 proposal 再改代码。
5. 改 G12 / G13 的注释与 chk 文案（m-3）；修 `nproc_binds` 的快路径（m-4，helper 与 `v31/sc-direct.sh` 两处）。按 INV-8，hook 只要再改一个字节，本报告就要对新增的 diff 复审。

## 评估

**是否可以继续？** 可以（Yes）。

**理由**：实现与规格逐条一致，放行只经作业退出码 77，核实过的每一条出错路径都回落到基线拦截。6 条发现都是 Minor（申报漏一类文案、注释与用例命名过宽、测试辅助脚本在少见环境里的假红、截止的毫秒级漂移、计时类用例缺直调补位），不阻塞发版。D-2 未核实；它若在 systemd 宿主上属实，就是一条新的放行路径，建议发版前确认或先做低成本加固。

附：探针 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t005/probe.sh`（运行一次，负载 1.77 → 1.79）。
