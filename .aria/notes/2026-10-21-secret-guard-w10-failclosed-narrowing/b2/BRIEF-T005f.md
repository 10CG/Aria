# TASK-005 修复轮任务书：WSL 标记读法加固（What 1 补充 2）、复审指出的注释与用例（10CG/aria-plugin#217）

你是 TASK-005 修复轮的执笔席（全新实例）。被改的是一个**防泄密安全 hook**（Claude Code 的 PreToolUse secret-guard）。独立代码审查（报告 `/home/dev/Aria/.aria/audit-reports/post_implementation-R1-1792888152945-secret-guard-w10-failclosed-narrowing-code-reviewer.md`）判 PASS（0 Critical / 0 Major / 6 Minor / 3 疑点），主控裁定开这一轮修复，规格已先改好（proposal v3.3）。主控不亲写代码；你按本任务书改、实跑，主控之后独立复核。

## 规格（逐字照做的部分以 proposal 为准）

- proposal `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`：**What 1 补充 2**（`_sg_relax_ok` 里 WSL 那一行换成两行，新函数 `_sg_relax_nowslfs`——代码**逐字**照抄，主控已在四个 bash 上实跑过这段代码）；What 3 截止那条、What 4 末尾、What 5 表里 VMAX 那行、R-c（这些只改文档，已改好）；**What 7 补充 2**（要改的注释与各自必须表达的意思；逐字文本由你写，写进报告供主控回填 proposal）；决策记录第 22 条。
- 计划 `detailed-tasks.yaml`：INV-1（已增补两类内容差）、INV-2、INV-4、INV-6、INV-8；TASK-005 notes 里的「审查结果」与「主控裁定」。
- 审查报告的 Minor、疑点与「第 5 项」（三条直调用例的写法）。
- aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`，分支 `feature/secret-guard-w10-failclosed-narrowing`，当前 `2893bcc`，工作区干净。

## 要改的

**A. hook**（`hooks/secret-guard.sh`）
1. What 1 补充 2：WSL 一行换成两行；`_sg_relax_nowslfs` 放在其余 `_sg_relax_*` 函数旁边（source 闸门之上，INV-4）。逐字照抄 proposal 里的代码与行尾注释。
2. What 7 补充 2 第 1-5 处注释（hook 头注释「Shell variable indirection」那条、LENGTH BUDGET 块那句、`_sg_relax_noext` 行尾注释、`_sg_vx_pass` 的说明、重跑块头那句）：只改注释，按各处要表达的意思写，延续周围的行宽与风格；每处改前改后的逐字文本写进报告。第 6 处（WSL 行的注释）已随第 1 条落地。
3. 除此之外 hook 一字不改；`git diff 2893bcc -- hooks/secret-guard.sh` 只能出现上面这些。

**B. 套件**（`hooks/tests/secret-guard.test.sh`）：W10 块头与 What 7 补充 2 第 1 处同义的那句（「only where … not in effect」）同样改；新用例的编号进 `SGW_EXP_DIRECT`；头注释里的用例计数随之改。

**C. 直调 helper 与 `v31/sc-direct.sh`**（两处同一份代码，INV-2）
1. m-3：V2-G12 / G13 的注释与 chk 文案改成只说关门一极（平台检查失败时 2 oversize、绝不 4），开门一极指向 V14-G1；编号不变。
2. m-4：`nproc_binds` 快路径改用真实 UID（`id -ru`），CapEff 由 bash 自己用 read 循环从 `/proc/$BASHPID/status` 读（不经 awk）；注释改成 real user ID 0。
3. m-6：三条与负载无关的直调用例（新编号 `V15-T1-…`、`V15-T2-…`、`V15-T3-…`，名字自拟）：计时器睡的恰是 `_SG_LEFT`；锚点 `_SG_P0` 只在 hook 起点取一次；作业的命令替换里 `exec 2>/dev/null`。写法照审查报告第 5 项。
4. What 1 补充 2 的直调用例（新编号 `V15-W1…`）：(a) 假挂载表在 DIR 上只有 autofs、DIR 里却有 `WSLInterop` -> 0（没挂上就不看项，这正是 D-2 要的）；(b) 假挂载表把 DIR 列为 binfmt_misc、DIR 里有 `WSLInterop-late` -> 1；(c) 挂上了但没有 `WSLInterop*` -> 0；(d) 挂载表读不出 -> 1，且 stderr 为空；(e) `_sg_relax_nowslfs` 桩成返回 1 时，放宽平台上的 `_sg_relax_ok` 返回 1。临时文件与目录建在 helper 自己的临时目录下。
5. 每条新用例都要先证明**能红**：在 scratchpad 里做对应的坏实现（例如：WSL 行恢复成旧的单行 `-e` 检查；循环里用 `&& m=1`；`< 文件` 写在 `2>/dev/null` 前面；计时器睡 3；在作业里重取锚点；去掉 `exec 2>/dev/null`），新用例在坏实现上红、在实现上绿。坏实现只在 scratchpad。
6. 编号进各处清单：helper 的编号清单、`v31/sc-cases.sh` 的期望编号清单（V0-H2）、套件的 `SGW_EXP_DIRECT`。

**D. v31 工具**（主仓 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`）
1. `mutants.py` 与 `impl/w14-mutants.py`：凡是锚点原文因 A 的改动而变了的补丁，把锚点改成新原文、错误本身保持不变；改完全部坏实现仍须「原文恰好出现一次」并能生成。只改锚点，不加不删坏实现。
2. `commentsync.py`：随 A、B 改的注释更新逐句核对的清单（旧句在 target 里须为 0 次、新句须在本站点出现；照 3b 的做法机械导出，不手打）。target 为 GREEN、baseline（59e333c）为 GREEN，对基线的两种构造（插字符绕过、整块删除）仍为 RED。

## 要跑的（输出落 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t005f/`；每轮先写预期）

- 移植用例 `SG_W10_ONLY=.`：5 个 bash（`/home/dev/.aria/tools/bash-{5.0.18,5.1.16,5.3.20,3.2.57}/bash` 与 PATH 上的 5.2.15）各一轮，全过（3.2 上只许 [platform] 的 SKIP），计时批判过。
- 整轮：worktree 里 PATH 上的 bash 一轮（FAIL 0，SC-13 绿）；导出 `WSL_DISTRO_NAME=Ubuntu` 再一轮（FAIL 0，6 组走基线支）。
- `v31/sc-cases.sh` 在实现上（基线取 59e333c）全过。
- 坏实现：`v31/run-mutants.sh` 的 v31 模式与套件模式（`MUT_SUITE=<worktree>`）各一遍指定用例，全部 CAUGHT、P-0 GREEN、扰动如预期；`v31/impl/w14.sh`（写到 scratchpad：`W14_OUT`、`W14_DIR` 指向你的目录）31 个全抓住。
- commentsync：target、baseline 与两种构造。

## 报告

写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T005f-report.md`（中文）：每个文件改了什么（hook 贴完整 diff）；What 7 补充 2 每处的改前改后逐字文本；新用例代码与「能红」的证明；mutants / w14 锚点改了哪些；各轮预期与结果、首尾负载；未做或拿不准的项。

## 纪律

- **工具调用上限 70 次；到第 55 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。
- **输出纪律**：跑出的输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行；读大文件先 `grep -n` 再按行号读，每次不超过 80 行；不要 cat 整份套件或 hook。
- **只改这些文件**：worktree 的 hook、套件、helper；主仓 v31 的 `sc-direct.sh`、`sc-cases.sh`、`mutants.py`、`commentsync.py`、`impl/w14-mutants.py`。不改 proposal 与计划（逐字文本写进报告，主控回填）；不 commit。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验；开跑前一分钟负载 < 1.2；计时类结论只在首尾负载都 < 2 时算数（INV-7）。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：文本写进文件（Write / Edit 工具不受它影响）或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
