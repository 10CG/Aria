# TASK-002 第三步 3b 任务书：W10 批移到套件最前；6 组既有用例按平台分两支；套件注释、标题、头注释；commentsync 套件一侧逐句核对（10CG/aria-plugin#217）

你是 TASK-002 第三步 3b 段的执笔席（全新实例）。主控不亲写测试代码；你按本任务书改 aria 的回归套件并在实现上实跑，主控之后独立复核。
3a（把 v31 的 136 个编号移植进套件）已完成，提交在 aria 分支 `feature/secret-guard-w10-failclosed-narrowing` 的 `3a64827`（worktree 当前就在这个提交上，工作区干净）。3c（关门臂的基线参照核对、全部坏实现、两种环境错误、基线红集在套件上复跑）由下一个实例做，**不在本段**。

## 规格与材料（只按行号读需要的段）

- 计划 `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：`grep -n` 找 INV-1、INV-2、INV-6、INV-7；TASK-002 的 notes 里「3a 主控裁定」那一条；design 的「套件 (1) 补充」第 (iii)(iv) 条、「套件 (2)」「套件 (3)」；acceptance 前两条与 commentsync 那条。
- proposal `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`：What 1 与「What 1 补充」(`:61-96`，准入门)、What 5 (`:124-155`，文案逐字)、What 7 (`:160-192`，套件的第 9-20 处)、性质 P 一节 (`:592-627`)。6 组的新期望必须能逐条追到这里的某一条。
- v31 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`：`W9-suite.txt`（35 行，6 组在实现上红在哪几条检查）、`commentsync.py`（209 行，可整份读）。
- 3a 报告 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/T002c-3a-report.md` 第 2、6 节；主控复核 `.../b2/t002c-verify/VERIFY.md`（「代码审读」一节讲了旧用例与移植用例各自怎么起 hook）。
- 套件：worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria/hooks/tests/secret-guard.test.sh`（约 3570 行，**不要整份读**）。位置：头注释 `:1-27`；移植块 `:133-442`（`sg_w10_cases` 约 `:320`，过滤轮约 `:428`）；W10 旧用例块约 `:2836-3020`（`wpa_err` `:2428`、`wpa_x_toolarge` / `wpa_x_finding` 约 `:2844-2870`，6 组 `wpa_begin_bash_case` 在 `:2874`、`:2886`、`:2908`、`:2927`、`:2955`、`:3004`）；SC-13 与 Summary 在文件末尾。行号以 `grep -n` 为准。
- 基线套件：`git -C <worktree> show 59e333c:hooks/tests/secret-guard.test.sh`（commentsync 的 baseline 模式用；写到你的输出目录，不改 worktree）。

## 被测对象

- 实现：worktree 的 `hooks/secret-guard.sh`（sha256 前缀 `af4658b6f935`）。只读，不改。
- worktree 是 aria 的 git 检出（`af87cae` 可达），SC-8、SC-9a、SC-13 在这里照常跑。
- 旧用例经 `wpa_err` 直接执行 `$WPA_HOOK`（shebang 是 `/usr/bin/env bash`），所以跑旧用例的 bash 是 PATH 上的 bash；环境里的 `WSL_DISTRO_NAME`、`WSL_INTEROP` 原样传给 hook（`wpa_use_none` 只清 `CLAUDE_PROJECT_DIR` 等三个变量）。

## 要做的

0. **先跑一遍现状（先写预期再测）**：改之前在 worktree 里用 PATH 上的 bash 整轮跑一次，输出落文件。预期写进报告后再跑：FAIL 恰为 SC-21ab、21ac、21ag、21aj、21al、21ao；总数 961；SC-13 绿；W10 计时批多半是 SKIP [load]（3a 的诊断）。
1. **W10 批移到套件最前**（主控裁定 1，技术口径，不放宽）：`sg_w10_cases` 只在一处调用，即现在过滤轮所在的位置（移植块之后、第一条旧用例之前）；`SG_W10_ONLY` 设了时照旧打印过滤轮汇总并退出，没设时继续跑旧用例。删掉 SC-13 前的那次调用。负载门槛 2、「本批首尾各读一次」都不变。同步改所有说「just before SC-13」的注释（头注释、移植块块首、调用处）。
2. **6 组既有用例按平台分两支**（design「套件 (1) 补充」(iv) 与「套件 (2)」）：
   - 判据只算一次，与移植用例的 `SGW_RELAX` 同一套规则（What 1 与 What 1 补充），问的是**跑旧用例的那个 bash**（PATH 上的 bash，不是 `SC_BASH`）；另外，套件环境里 `WSL_DISTRO_NAME` 或 `WSL_INTEROP` 非空时一律走基线那一支（旧用例把环境原样传给 hook）。若这 6 组里有用例经 `wpa_use_proj` 设了带扩展清单的项目，也要算进判据；没有就在报告里写明。
   - 放宽生效的一支：断言新结局。每条新期望在该组注释里写明出自 proposal 的哪一条（What 编号或 P 编号）；不许只抄实现的输出。出 longline 文案的断言用新 helper（要求出现 `has a line longer than` 与 `Matched pattern:`）；出普通命中文案的断言要求出现 `value-REDACTING filter`，且不出现 `has a line longer than`；不再用 `wpa_x_finding` 区分这两种（PP1-A12）。
   - 其余平台那一支：原断言一字不改。
   - 两支的计数必须相同（每组仍是一个 `wpa_begin_bash_case`，计一次），这样 SC-13 与平台无关。
   - Summary 加一行，打印 6 组走了哪一支与判据的各项输入（bash 的 MACHTYPE 与版本、内核串、WSLInterop、环境里的两个 WSL 变量）。
3. **套件 7 块注释与 5 个标题**（What 7 第 9-15 处、第 16-20 处，以及 commentsync 里 KM2-14 的第 21、22 处）：
   - 按 proposal 表里的锚点短语定位（表里的行号是基线的，已过时）；
   - 整块改写成在两支上都为真的文字：放宽生效处是什么结局、其余平台是什么结局，各引 proposal 出处；
   - 改后每个锚点短语、每个旧标题整句在套件里出现 0 次；`_SGV_GMAX`、`longline` 至少各出现 1 次。
4. **commentsync.py 套件一侧补到逐句核对**（主仓 `v31/commentsync.py`）：照 hook 一侧 `HOOK_TEXT` 的做法，加 `SUITE_TEXT`：
   - 每处一个定位（紧挨某行代码的注释段，或含某短语的注释段）；
   - 旧句：从基线套件对应注释段里机械切句（在 `.` 与 `;` 之后切），列出改写删掉的句子，target 模式下全文 0 次，baseline 模式下在原段里至少 1 次；
   - 新句：你改写后的句子，target 模式下必须出现在该处自己的注释段里，baseline 模式下 0 次。
   - 第 16-20 处的标题检查与 `ADD_SUITE` 照旧。改动只加不删：hook 一侧与现有锚点、哈希检查不动。
5. **头注释**：
   - Coverage 两个数改为 git 检出里实跑的总数。本机没有 zsh，「有 zsh」的那个数只能推算，报告里写明推算方式。
   - `Expects` 行改准。改动前这句就不实：除了 SC-20，SC-19 的 census（约 `:1623`）也调用 python3。改成逐个列出套件实际依赖的外部工具：jq；python3（SC-20 与 SC-19 census）；timeout（移植的端到端用例）；ps（两条移植用例，没有时记 SKIP [platform]）。以 `grep -n` 实查为准。
6. **实跑**（输出全落 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002d/`）：
   - **5 个 bash 各一整轮**：在 worktree 里跑 `bash hooks/tests/secret-guard.test.sh`，`SC_BASH` 依次取 `/usr/bin/bash` 与 `/home/dev/.aria/tools/bash-{5.0.18,5.1.16,5.3.20,3.2.57}/bash`，加 `SG_W10_LOG`。要求：
     - FAIL 0；
     - 计时批判过（批开始负载 < 2，结束 < 2）；
     - SKIP 只有 3.2 上的 58 个 [platform]；
     - SC-13 绿，五轮总数相同。
   - **WSL 一轮**：`WSL_DISTRO_NAME=Ubuntu` 导出后，用 PATH 上的 bash 整轮跑一次。要求：
     - FAIL 0；
     - Summary 显示 6 组走了基线那一支；
     - 移植用例的编号数与上面五轮相同；
     - SC-13 绿。
   - **commentsync**：
     - `python3 v31/commentsync.py <worktree hook> <worktree suite> target` 为 GREEN；
     - baseline 模式对 59e333c 的 hook 与套件为 GREEN；
     - 三种构造都须报 RED：worktree 套件里改掉一条新句中的一个字符；删掉一整块改写后的注释；59e333c 的套件跑 target 模式。构造只在复制出来的文件上做，不改 worktree。
7. **报告**：写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002c-3b-report.md`（中文），内容：
   - 改了哪些文件；
   - 6 组两支的断言对照表，每条新期望注明 proposal 出处；
   - 注释与标题改写前后对照（只列句子）；
   - 各轮结果与首尾负载；
   - commentsync 各模式与构造的结果；
   - 未做或拿不准的项。

## 纪律

- **工具调用上限 70 次；到第 55 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。
- **输出纪律**：
  - 跑套件的输出一律重定向到文件，对话里只看 `tail -6`、`grep -c`，以及不超过 20 行的 FAIL 行；
  - 读文件先 `grep -n` 定位，再按行号读，每次不超过 80 行（commentsync.py、W9-suite.txt 除外）；
  - 不要 cat 整份套件或整份 hook。
- **只改这些文件**：worktree 的 `hooks/tests/secret-guard.test.sh`；主仓的 `v31/commentsync.py`。不改 hook、helper、垫片、`v31/run-suite.sh`（3c 的事）；不 commit。若发现 hook 的缺陷或规格矛盾，停下写进报告。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验。整轮约 7 分钟；开跑前看 `/proc/loadavg`，一分钟负载高于 1.2 先等（等的循环要显式 `return 0`），连续等 30 分钟仍高就先做不依赖墙钟的部分，并在报告里附读数。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）。把文本写进文件（Write / Edit 工具不受它影响），或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
