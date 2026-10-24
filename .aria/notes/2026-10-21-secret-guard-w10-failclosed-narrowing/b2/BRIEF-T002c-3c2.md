# TASK-002 第三步 3c2 任务书：6 组截止回落判法改定（10CG/aria-plugin#217）

你是 TASK-002 第三步 3c2 段的执笔席（全新实例）。主控不亲写测试代码；你按本任务书改套件、实跑，主控之后独立复核。本段只改 6 组既有用例放宽支的截止回落判法（`wpa_x6`）及其注释与 Summary 行，W10 移植块不动。
3c（关门臂的参照核对、6 组截止回落判法初版、两处小改）提交在 aria 分支 `feature/secret-guard-w10-failclosed-narrowing` 的 `5afef08`；worktree 当前就在这个提交上，工作区干净。

## 为什么改（主控裁定，技术口径，不动姿态；计划 notes「3c 主控裁定」第 (1) 条）

3b 定的判法是：放宽支断言不成立时，若同一份输出满足基线支断言、且墙钟 >= 2.85 s，记截止回落。3c 报告第 6 节第 1 条指出，基线那一遍本身就慢的命令，在准入门恒关时墙钟也会 >= 2.85 s，被当成截止回落（假绿）。主控复核时又发现另一侧：2.85 s 这个数是从截止类用例抄来的，不是从 hook 推出来的，会把合法回落判红（假红）。从 hook（`af4658b6f935`）推导，因时间而回落只有三条路：

- F1 准入门因没时间关门：`_sg_relax_left` 只在 `now >= _SG_P0 + 3 s` 时返回 1（预算变量已清，截止固定 3 s）。
- F2 截止杀作业：计时器 `sleep "$_SG_LEFT"` 在 `_SG_LEFT` 算出之后才起，杀作业在 `_SG_P0 + 3 s` 之后。
- F3 重跑自己的时间检查点：作业里 `_sg_vx_collect` 重置 `_SG_T0=$SECONDS`，`_sg_over_budget` 在 `SECONDS - _SG_T0 >= 3` 时让重跑返回 3，回落成基线拦截。SECONDS 是整秒，所以检查点在重置后超过 2 s、至多 3 s 触发；重置在作业开始之后，作业开始在基线那一遍跑完之后。

测量起点 `t0` 在 hook 进程起来之前，早于 `_SG_P0`。所以：F1、F2 的墙钟 > 3.0 s；F3 的墙钟 > 基线那一遍的耗时 Tb + 2 s，可能落在 2-3 s 之间（Tb < 1 s 的命令）；任何因时间的回落墙钟都 > 2.0 s。准入门提前关（坏实现）时墙钟约等于 Tb。2.85 s 在 2-2.85 s 之间会把 F3 判红，在 2.85-3 s 之间又分不开 F3 与提前关门。改成下面的判法。

## 规格与材料（只按行号读需要的段）

- 计划 `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：TASK-002 notes 里「3b 主控裁定」「3c 主控裁定」两条（`grep -n` 定位）。
- hook（worktree `hooks/secret-guard.sh`，只读）：`_SG_P0` 在 `:189`；`_sg_over_budget` 约 `:630`；`_SG_T0` 在 `_sg_vx_collect` 里重置约 `:648`；`_sg_relax_left` 约 `:807`；`_sg_relax_job` / `_sg_relax_run` 约 `:836-866`。
- 套件 worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria/hooks/tests/secret-guard.test.sh`（**不要整份读**）：`wpa_x6_eval` / `wpa_x6` 与上方注释块约 `:2948-2982`；6 组共用注释约 `:2925-2927`；Summary 的 6 组行约 `:3732`；`sg_w10_ge` 用 `grep -n` 定位。
- 3c 的构造与驱动（可复用）：`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002e/`（`drive3.sh`、`c1-hook.sh`、`c2-hook.sh`、`c1.txt`、`c2.txt`），3c 报告 `.../r217impl/T002c-3c-report.md` 第 5、6 节；`v31/run-suite.sh`（`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`）。

## 新判法（`wpa_x6`，逐字照做）

触发点上的每条命令仍只跑一次 hook（清掉 `SECRET_GUARD_TIME_BUDGET_S`），墙钟 W 用 `EPOCHREALTIME` 量，**按微秒整数比较、不先四舍五入**（去掉 `[.,]` 后做 10# 算术；显示时保留两位小数）。

1. 放宽支断言在这份输出上成立：这条命令通过。
2. 否则，基线支断言（else 分支里那条 `wpa_x_toolarge` 及其 limit 行）在同一份输出上不成立：记一处不符，细节写两套断言各自不符的项与 W。
3. 否则（输出是基线的拦截）：
   - (a) W >= 3.0 s：记截止回落（F1、F2，或晚到的 F3）。
   - (b) 2.0 s < W < 3.0 s：用**同一份输入**、同样的变量与目录、清掉预算变量、另加 `WSL_DISTRO_NAME=Ubuntu`（关门），再跑一次 hook，量墙钟 Tb'。Tb' <= W - 1.0 s：记截止回落（F3：重跑的检查点让它回落，W 比基线那一遍长 2 s 以上）；否则记一处不符，细节写 W 与 Tb'，并写明「关门那一遍同样慢：是准入门提前关，不是重跑的检查点」。1 s 取在 F3 的 2 s 间隔正中，两边各留 1 s 给负载抖动。
   - (c) W <= 2.0 s：记一处不符，细节写 W，并写明「因时间的回落不会这么早结束」。
4. 每组仍计一次。Summary 的 6 组行改成：`deadline fallback (截止回落) N / M`，后面列出每次回落的组名与墙钟，(b) 类另带 Tb'，例如 `(21ab 3.12s; 21ac 2.55s/Tb 0.34s)`。
5. 注释：`wpa_x6` 上方的注释块改写成上面的推导（F1-F3、测量起点早于 `_SG_P0`）与判法，删掉「2.85 s 与截止类用例同口径」的说法；6 组共用注释里的「wall >= 2.85 s」同步改。注释里写明这条判法取代 3b 的 2.85 s 下界，以及为什么（两侧各一个洞）。

## 要做的

0. **先写预期，再在 3c 的代码上跑构造 C3**（证明 C3 在旧判法下会红）。C3：hook 副本里，`_sg_relax_job` 中计时器检查（`kill -0 "$tp"` 那一行）之后、`_SG_RELAXED=1` 之前，加 `sleep 2.2; return 1`（模拟重跑的检查点在作业开始 2.2 s 后让它回落）。经 `run-suite.sh` 跑整轮（6 组只在整轮里出现；副本里 SC-13 本来就红）。预期：基线那一遍快的触发点命令（3c 的 C1 实测 21ac 0.34 s、21al 0.30 s、21ao 0.35 s、21aj 0.62 s 等）W 约等于 Tb + 2.2 s、小于 2.85 s，被判不符，6 组中至少这几组 FAIL。
1. 按上面的新判法改 `wpa_x6`、注释与 Summary 行。只改 `wpa_x6`（及需要时新加的一个小 helper）、它上方的注释块、6 组共用注释里那一句、Summary 的 6 组行；6 组的调用行、基线支、`wpa_x6_eval` 与 W10 移植块一字不改。
2. 实跑（输出全落 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002f/`），每轮先写预期：
   - C3（新代码）：6 组全部 PASS，截止回落 10 / 10；Tb 小于约 0.8 s 的命令走 (b)，其余因截止先到走 (a)。
   - C1（准入门恒关，`_sg_relax_ok` 首行 `return 1`，新代码）：6 组全部 FAIL；W < 3.0 s 的触发点命令都被判不符；W >= 3.0 s 的（基线那一遍本身超过截止，与合法的「没时间关门」输出相同、分不开）记截止回落，报告里逐条列出它们的 W。
   - C2（作业里计时器起来之后加 `sleep 4`，新代码）：6 组全部 PASS，截止回落 10 / 10，全部 W >= 3.0 s、走 (a)。
   - 实现：worktree 里 PATH 上的 bash 整轮一次（低负载）：FAIL 0，SC-13 绿，Summary 的 6 组行显示截止回落数与明细。
   - `v31/commentsync.py --suite-only <改后的套件> target` 仍为 GREEN。
3. **报告**：写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002c-3c2-report.md`（中文）：改了什么（贴 `wpa_x6` 改后全文）、各轮预期与结果、首尾负载、每轮 6 组那一行的原文、C1 里 W >= 3.0 s 的命令清单、未做或拿不准的项。

## 纪律

- **工具调用上限 40 次；到第 30 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。
- **输出纪律**：跑套件的输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的 FAIL 或判定行；读文件先 `grep -n` 再按行号读，每次不超过 80 行；不要 cat 整份套件或 hook。
- **只改这一个文件**：worktree 的 `hooks/tests/secret-guard.test.sh`（只动上面第 1 条列出的位置）。不改 hook、helper、垫片、v31 脚本；不 commit。若发现 hook 的缺陷或规格矛盾，停下写进报告。
- 构造只在 `run-suite.sh` 的 hook 副本里做，不改 worktree 的 hook。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验。开跑前看 `/proc/loadavg`，一分钟负载高于 1.2 先等（等的循环要显式 `return 0`），连续等 30 分钟仍高就照跑，并在报告里附读数。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）。把文本写进文件（Write / Edit 工具不受它影响），或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
