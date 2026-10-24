# TASK-002 第三步 3a 任务书：把 v31 的新用例搬进 aria 套件（10CG/aria-plugin#217）

你是 TASK-002 第三步 3a 段的执笔席（全新实例）。主控不亲写测试代码；你按规格把 `v31/` 的验收用例移植进 aria 的回归套件，在实现上实跑；主控之后独立复核。3b（6 组既有用例、套件注释与标题、commentsync 套件一侧）与 3c（坏实现、环境错误、基线红集在套件上复跑）由后面的实例做，**不在本段**。

## 规格与材料（只按行号读需要的段）

- 计划 `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：先 `grep -n` 找到 INV-1、INV-2、INV-5、INV-7，以及 TASK-002 的 design「套件 (1) 搬入方式」「**套件 (1) 补充**」（主控定下的六条口径，本段照做）「依赖字符数与字节数差异的用例」，和 acceptance 前两条。
- v31 验收（被移植的对象）`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`：`sc-cases.sh`（266 行）、`sc-direct.sh`（450 行）、`shapes.py`（47 行）、`shim/delay-first`（36 行）、`README.md`。这几份可以整份读。
- 第二步报告 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002b-report.md`：第 1 节 (a)(d)(f) 与第 5 节，讲了垫片、负载门、慢宿主信号、`V5-S13` 预算等为什么这样写。
- 套件：worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria/hooks/tests/secret-guard.test.sh`（3245 行，**不要整份读**）。需要的位置：头注释 `:1-15`；`run_case` 等 helper `:30-70`；SC-T 段结尾与 SC-13 断言、Summary 在文件末尾约 `:3200-3245`；W10 旧用例块约 `:2510-2700`（本段只读不改）。

## 被测对象

- 实现：`wt217/aria/hooks/secret-guard.sh`（feature 分支 `21a37ea`，sha256 前缀 `af4658b6f935`）。只读，不改。
- worktree 是 aria 的 git 检出（`af87cae` 可达），SC-8、SC-9a、SC-13 在这里照常跑。

## 要做的

0. **先在基线上跑一遍（先写预期再测）**：改任何东西之前，在 worktree 里对实现原样跑一次现有套件（输出落文件），记下 PASS/FAIL 与总数。依据 `v31/W9-suite.txt`，预期只有 21ab、21ac、21ag、21aj、21al、21ao 六组红；先把预期写进报告，再跑。
1. **垫片**：`v31/shim/delay-first` 复制为 `hooks/tests/lib/sg-shim/delay-first`，`jq`、`sed` 用相对符号链接指向它。
2. **直调 helper**：由 `v31/sc-direct.sh` 改出 `hooks/tests/lib/secret-guard-w10-direct.sh`，由 `SC_BASH` 执行。编号、断言、期望值、原因标签照旧，末行哨兵照旧。要改的只有：
   - 需要基线文件的那一臂（`fbt`，即 `V6-S20`、`V6-S21`）改成同一 hook 在准入门关着时的拦截文案，关门方法是在 source 它的子 shell 里设 `WSL_DISTRO_NAME`；
   - 每个编号在两种模式下都报一次：模式不适用的记 `SKIP <id> [platform] …`；平台缺 `/proc` 等前提时同样记 SKIP，不记 FAIL。
3. **端到端与静态用例**：写进 `secret-guard.test.sh`，定义成一个函数，放在 helper 区之后；正常跑时在 SC-13 断言之前调用。要点：
   - 「与基线逐字节相同」的一臂，取同一 hook 在环境里设了 `WSL_DISTRO_NAME=Ubuntu` 时的输出。`V2-E17` 因此改判结局：退出码 2，且是尺寸文案。
   - 新用例按 `SC_BASH`（缺省为 PATH 上的 bash）执行 hook；旧用例照旧。
   - 每次起 hook 都清掉 `WSL_DISTRO_NAME`、`WSL_INTEROP`、`CLAUDE_PROJECT_DIR`、`_SG_RELAXED`、`SECRET_GUARD_TIME_BUDGET_S`，只有专门的用例自己设。
   - 输入生成改写成 bash 函数，不用 python3。凭据形路径照 `shapes.py` 的做法在运行时拼装。
   - 计时批按 INV-7 处理：开跑与结束各读一次负载，`SKIP [load]` / `[void]` 照 `sc-cases.sh`。慢宿主信号与 INCONCLUSIVE 规则照第二步。
   - 静态检查：`V11-S1`、`V11-S3` 照旧；`V11-S4` 改成固定判据，hook 里恰好一处 `risky_patterns[@]`；`V12-C1` 不移植。
   - 装置检查：`V0-H1` 查 helper 跑到哨兵且退出 0；`V0-H2` 查编号清单，任何平台都是同一份清单，缺、多、重复都 FAIL。
4. **计数与输出**：
   - 加 `skip` 计数，按原因分；Summary 单列 SKIP，SKIP 不影响退出码。
   - SC-13 的总数改为 `pass + fail + skip + 1`。头注释的 Coverage 两个数改成在 worktree 里实跑的总数，再在头注释里补几句说明：新用例、`SC_BASH`、垫片、两个开关、SKIP 怎么计。头注释里「python3 只给 SC-20 用」必须仍然成立（`grep -n python3` 核对）。
5. **两个开关**：
   - `SG_W10_ONLY=<正则>`：只跑编号匹配的移植用例。旧用例与 SC-13 都不跑，Summary 注明这是过滤轮。实现办法：在文件靠前处判断，调用上面那个函数后退出。
   - `SG_W10_LOG=<文件>`：把每条移植用例的结果按 v31 格式写进该文件，一行一条：`PASS|FAIL|SKIP <id> <detail>`，原因标签照旧，供 `run-mutants.sh` 解析。
6. **`v31/run-suite.sh`**（主仓，新文件）：`run-suite.sh <aria 检出目录> <hook> [<工作目录>]`。
   - 把 `<aria>/hooks` 复制到临时目录，用 `<hook>` 替换 `secret-guard.sh`，然后跑套件。
   - `SC_BASH`、`SG_W10_ONLY`、`SG_W10_LOG` 照传，套 `taskset -c 0,1 nice -n 19`。
   - 首行记日期、两个 sha256 前缀、负载；末尾记结束负载。
   - 头注释写明：非 git 副本里 SC-8、SC-9a 不跑，SC-13 的总数随之不同。
7. **实跑**（输出全落 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002c/`）：
   - **5 个 bash 各一轮**：在 worktree 里 `bash hooks/tests/secret-guard.test.sh`，`SC_BASH` 依次取 `/usr/bin/bash` 与 `/home/dev/.aria/tools/bash-{5.0.18,5.1.16,5.3.20,3.2.57}/bash`。要求：
     - 低负载、计时批判过；
     - 移植用例全 PASS（3.2 上 relax 专属的编号为 `SKIP [platform]`）；
     - 旧用例只有 W9 那 6 组红；
     - SC-13 绿，五轮总数相同。
   - **等价核对**：同一 bash 上，套件的逐条结果（`SG_W10_LOG`）与 `v31/sc-cases.sh` 对实现的逐条结果按编号对齐。逐条列出不同（应只有本任务书允许的几处）。
   - **抽查能红**：用 `v31/mutants.py` 从实现构造坏实现（写到 t002c 下）。经 `run-suite.sh` 加 `SG_W10_ONLY=<指定用例>` 跑 BI-24（直调）、BI-7（端到端回落字节，须低负载）、BI-11（`V10-N3` 与 `V11-S4`），三者都须按 `reasons.tsv` 的原因标签变红。全部坏实现的复跑在 3c。
8. **报告**：写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002c-3a-report.md`（中文），内容：
   - 改了哪些文件；
   - 编号对照表：编号 → helper 或套件里的位置，与 v31 不同的断言逐条说明；
   - 各轮结果与首尾负载；
   - 等价核对与抽查结果；
   - 未做或拿不准的项。

## 纪律

- **工具调用上限 70 次；到第 55 次时停止新工作，把已完成的写进报告再收尾。** 上一段的实例上下文涨到 79 万、调用 168 次，代价很高；本段的上限是硬的。
- **输出纪律**：
  - 跑套件、跑用例的输出一律重定向到文件，对话里只看 `tail -3`、`grep -c`，以及不超过 20 行的 FAIL 行；
  - 读文件先 `grep -n` 定位，再按行号读，每次不超过 80 行（v31 那几份小脚本除外）；
  - 不要 cat 整份套件或整份 hook。
- **只改这些文件**：
  - worktree 的 `hooks/tests/secret-guard.test.sh`；
  - 新建的 `hooks/tests/lib/secret-guard-w10-direct.sh`；
  - 新建的 `hooks/tests/lib/sg-shim/`；
  - 主仓新建的 `v31/run-suite.sh`。

  不改 hook；不碰 W10 旧用例块、注释与标题（3b 的事）；不 commit。若移植暴露 hook 的缺陷，停下写进报告。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验。计时类按 INV-7：开跑前看 `/proc/loadavg`，高于 2 先做不依赖墙钟的部分。注意：自己写「等负载降下来」的循环时，等过之后函数要显式 `return 0`。第二步的 `lowload.sh` 和主控的复核脚本都栽在这里。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）。把文本写进文件（Write / Edit 工具不受它影响），或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
