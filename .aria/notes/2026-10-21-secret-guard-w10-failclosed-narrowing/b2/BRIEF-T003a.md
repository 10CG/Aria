# TASK-003 第一段任务书：非作者独立构造坏实现，预先写下抓它的用例，再上机核对（10CG/aria-plugin#217）

## 防御语境（先读）

这是对一个**防泄密安全 hook**（Claude Code 的 PreToolUse secret-guard：在命令执行前拦下读凭据文件的命令）做**变异测试**。目的只有一个：证明它的回归测试能抓住实现里的错误。你要做的「坏实现」是在 hook 副本上改一处、模拟执笔人写错的地方，只存在于 scratchpad、只用来跑测试，不安装、不进任何仓库、不碰真实凭据。凭据形的字符串（路径等）一律在运行时拼装，不出现在命令行与输出里。

你是 TASK-003 的 QA 席（非作者）。实现的作者与写测试的人都不是你；你的价值在于**独立**：坏实现的点子必须出自你自己读实现与规格时的判断，不能从现有测试或别人的坏实现清单里来。

## 对象

- 实现：aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria` 的 `hooks/secret-guard.sh`（分支 `feature/secret-guard-w10-failclosed-narrowing`，提交 `acb644b`，hook 的 sha256 前缀 `af4658b6f935`）。基线是 aria `59e333c` 的同一文件（sha256 前缀 `e83c5e30f2cc`，用 `git show` 取）。
- 规格：`/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`（What 1-7、性质 P1-P6、Success Criteria；`:240-591` 是参考实现的全部逻辑 hunk）与同目录 `detailed-tasks.yaml` 的 invariants（INV-1 至 INV-9）与 TASK-003 一节。
- 跑法：`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-suite.sh <aria 检出> <hook> [<工作目录>]`（把 hook 换进套件副本跑；`SG_W10_ONLY=<正则>` 只跑匹配编号的移植用例，`SG_W10_LOG=<文件>` 逐条结果）。先读它的头注释。

## 三个阶段（顺序不可换）

### 阶段 1：盲构造（这一阶段**禁止读**：`hooks/tests/` 下的一切、`v31/sc-cases.sh`、`v31/sc-direct.sh`、`v31/mutants.py`、`v31/W13-*`、主仓 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/` 下的 `b2/`、`pp-r2-seats/`、`evidence/`）

1. 只读实现、基线与规格，构造**至少 16 个**坏实现。每个 = 实现 + **一处**像真实执笔错误的改动（比较符写反、差一、用错变量或常量、漏一个检查、顺序颠倒、退出码映射错、单位错、吞掉错误、作用域或子 shell 用错、读了环境里不该信的值……）。覆盖面：What 1（触发点与准入门，含 What 1 补充的平台与 WSL 判据）、What 2（重跑规则）、What 3（硬截止作业）、What 4（回落 = 基线逐字节）、What 5（文案）各至少 2 个；时间预算与锚点各至少 1 个；其余自定。
2. 写成生成器 `w14-mutants.py`（放 scratchpad 的 `r217impl/t003a/`）：每个坏实现是一组「原文 -> 改文」的逐字替换，替换前断言原文在 hook 里恰好出现一次；从实现生成坏实现到工作目录。编号 `Q-1`、`Q-2`……
3. 清单 `t003a/list.md`：每个编号写「改了什么、属于哪类执笔错误、会在什么输入形状上露出来、露出来是什么样（退出码 / 文案种类 / 字节 / 墙钟）」；若你认为某个改动观察不到（等价），写出理由。
4. **冻结**：把 `w14-mutants.py` 与 `list.md` 的 sha256 写进报告，之后两者不再改（若必须改，新开编号并说明）。

### 阶段 2：预先写下谁来抓（冻结之后才允许读下面这些，且只读这些）

- 套件 `hooks/tests/secret-guard.test.sh` 里 W10 移植块的块首注释（原因标签的含义）与用例调用行（`grep -n` 找 `sg_w10_identity`、`sg_w10_deadline`、`sg_w10_outcome` 等调用行与 `sg_w10_cases` 里的编号；不读断言函数的函数体）；helper `hooks/tests/lib/secret-guard-w10-direct.sh` 的头注释与用例编号行（`grep -n` 编号）。
- 对每个坏实现写下：预计由哪个（些）用例编号抓住、红的原因标签（如 `[status]`、`[bytes]`、`[kind]`、`[fallback]`、`[wall>hi]`、`[reference]`）；或写「预计无用例能抓（缺口）」。写进 `t003a/predict.md`，把它的 sha256 写进报告后再跑。

### 阶段 3：上机核对与补缺口

1. 每个坏实现经 `run-suite.sh` 跑预计的那些用例（`SG_W10_ONLY='^(编号|编号)$'`，带 `SG_W10_LOG`）；结果分四类：**按预期抓住**（预计的用例红、原因标签一致）、**别处抓住**（只在别的用例或别的原因上红）、**未抓住**、**未判**（计时类用例因负载 SKIP：低负载下重跑）。「别处抓住」与「未抓住」都按缺口处理（无关断言碰红不算抓住）；可以另跑一次 `SG_W10_ONLY=.` 看全部红，写进报告供判断。
2. 缺口：补一个**定向用例**，同时写进套件的 W10 移植块（新编号 `V14-…`）与 `v31/sc-cases.sh`（同编号；直调类写进 helper 与 `v31/sc-direct.sh`）—— INV-2。要求：在实现上绿、在该坏实现上红、红的原因就是这处错误。补用例要跟上套件里已有的约定（编号清单 V0-H2、SKIP 的平台原因、计数与 SC-13、commentsync），改完 `v31/commentsync.py --suite-only <套件> target` 仍 GREEN。
3. 补完后：套件在实现上 `SG_W10_ONLY=.` 跑 PATH 上的 bash 与 `SC_BASH=/home/dev/.aria/tools/bash-3.2.57/bash` 各一轮，全绿（3.2 上只许 [platform] 的 SKIP）；`v31/sc-cases.sh` 在实现上同样全绿；全部坏实现在套件上再跑一遍，此时都应「按预期抓住」或「由补的用例抓住」。

### 交付

- `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14.sh`（新建）：由 `w14-mutants.py` 生成全部坏实现，经 `run-suite.sh` 逐个跑预计用例，写出 `v31/impl/W14-independent-mutants.txt`。输出首行记日期、负载，以及基线、实现、套件、helper、`sc-cases.sh`、`sc-direct.sh`、`mutants.py`、`w14-mutants.py` 的 sha256 前缀（INV-8）；之后每个坏实现一行：编号、改动摘要、预计用例与原因、实际结果、结论。`w14-mutants.py` 也放进 `v31/impl/`。
- 报告 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T003a-report.md`（中文）：两个冻结的 sha256、清单与预测（可贴表）、逐个结果、缺口与补的用例（贴用例代码）、补用例前后各轮结果与首尾负载、未做或拿不准的项。

## 纪律

- **工具调用上限 70 次；到第 55 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。缺口太多做不完时，先保证全部坏实现都跑过、结果分好类，未补的缺口在报告里列清楚。
- **输出纪律**：跑套件的输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行；读大文件先 `grep -n` 再按行号读，每次不超过 80 行；不要 cat 整份套件或 hook。
- **只改这些文件**：scratchpad 的 `r217impl/t003a/` 下随意；worktree 的 `hooks/tests/secret-guard.test.sh`（只在 W10 移植块里加用例与必需的编号清单）、`hooks/tests/lib/secret-guard-w10-direct.sh`（只加直调用例）；主仓的 `v31/sc-cases.sh`、`v31/sc-direct.sh`（只加用例）与新建的 `v31/impl/w14.sh`、`v31/impl/w14-mutants.py`、`v31/impl/W14-independent-mutants.txt`。**不改 hook**（实现）；不 commit。若发现实现本身的缺陷（不是坏实现，是实现就错了）或规格矛盾，停下写进报告。
- 坏实现只生成在 scratchpad；不拷进 aria 或主仓。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验。开跑前看 `/proc/loadavg`，一分钟负载高于 1.2 先等（等的循环要显式 `return 0`）；计时类用例的结论只在开始与结束负载都 < 2 时算数（INV-7）。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）。把文本写进文件（Write / Edit 工具不受它影响），或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
