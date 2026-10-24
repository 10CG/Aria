# TASK-002 第三步 3d 任务书：run-mutants.sh 的套件模式；坏实现、两种环境错误与基线红集在套件上复跑（10CG/aria-plugin#217）

你是 TASK-002 第三步 3d 段的执笔席（全新实例）。主控不亲写测试代码；你给 `v31/run-mutants.sh` 加套件模式，在移植后的 aria 套件上复跑坏实现、环境错误与基线红集，主控之后独立复核。
套件已由前三段改好并提交在 aria 分支 `feature/secret-guard-w10-failclosed-narrowing`：3a `3a64827`、3b `fee1a65`、3c `5afef08`、3c2 `df2d629`；worktree 当前就在 3c2 提交上，工作区干净。3c2 只改了 6 组既有用例的截止回落判法，它们只在整轮里出现；本段的坏实现、扰动、环境错误与基线红集都是过滤轮（`SG_W10_ONLY`），不经过 6 组。本段**不改套件、helper 与 hook**。

## 规格与材料（只按行号读需要的段）

- 计划 `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：`grep -n` 找 INV-7、INV-9；TASK-002 notes 里的「口径 (ii) 的漏洞」与 3c 的几条；design「套件 (1) 补充」与「最后一步」；acceptance 的坏实现、环境错误、基线红集三条。
- v31 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`：`run-mutants.sh`（66 行，可整份读）、`run-suite.sh`（可整份读）、`mutants.py`（只读头注释与三张表怎么写出）、`README.md`。
- 第二步在 v31 脚本上的结果（对照用）：`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/t002b-verify/mut-summary.txt`（57 个坏实现与 7 个扰动的判定）、`.../b2/t002b-verify/base-5.2.15.txt`（基线红集：PASS 24 / FAIL 39 / MISSING 74）、`.../b2/t002b-verify/env/`（两种环境错误）。
- 3c 报告 `.../b2/T002c-3c-report.md`：`[reference]` 是什么、哪些用例走关门臂（也就是套件里 `sg_w10_ref` 表列出的 23 个编号，加上 helper `fbref` 的 V6-S20、V6-S21）。
- worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`（只读）。

## 要做的

0. **先跑现状（先写预期再测）**：v31 模式（不设新变量）对 BI-8 跑一次 `MUT_ONLY='BI-8'`，预期 CAUGHT；经 `run-suite.sh` 用 `SG_W10_ONLY=^(V9-E12-vmax-unchanged)$` 跑 BI-8，预期 V9-E12 为 `FAIL … [reference]`。预期写进报告后再跑。
1. **`v31/run-mutants.sh` 加套件模式**：
   - `MUT_SUITE=<aria 检出>` 时，每个坏实现与扰动经 `run-suite.sh <aria 检出> <坏实现>` 跑：`SG_W10_ONLY` 取指定用例（P-0 取 `.`），`SG_W10_LOG` 取逐条结果，判定逻辑照旧。
   - 原因表照用 `reasons.tsv`，只有一处放宽：指定用例走关门臂时，不论 `reasons.tsv` 列的是什么，另认 `\[reference\]`。哪些用例走关门臂以上面那张表为准。脚本头注释写明这一条与两点理由：一是套件里「与基线的字节不同」由「与关门臂不同」加「关门臂偏离基线的已知结局」两条合起来表达；二是套件先核参照、对不上就提前返回，不再做原来的判定，所以一个坏实现只要让关门臂偏离了基线的已知结局，报出来的就是 `[reference]`，而这本身就是真问题（关门时与 59e333c 不同）。（主控 2026-10-24 改定：计划 notes 里原写「reasons.tsv 列 [bytes] 的这些用例上另认」，按 3c 的提前返回放宽到全部走关门臂的指定用例。）报告里逐条列出以 `[reference]` 抓住的坏实现、v31 的原因标签，并对照坏实现的改动说明关门臂为什么偏离。
   - 套件里 helper 的 MISSING 记作 `FAIL [missing]`。它对不上原因表时落到 WRONG-REASON，与 v31 的 SETUP 同样不算抓住。头注释写明。
   - P-0 在套件模式下须无 FAIL（SKIP 只许 [platform]）。
   - 不设 `MUT_SUITE` 时，行为与现在逐字相同：改前改后各跑 `MUT_ONLY='BI-8|BI-24'`，比对两份输出（时间与负载读数之外）。
2. **实跑**（输出全落 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002g/`）：
   - **全部坏实现与扰动，套件模式**：PATH 上的 bash，低负载。要求 57 个全部 CAUGHT，P-0 GREEN，其余 6 个扰动 CAUGHT。NOT-JUDGED（负载）的在低负载下单独重跑，两次读数都记下。逐个与 `mut-summary.txt` 对照，指定用例的结论或原因标签与 v31 不同的逐条列出并解释。
   - **两种环境错误，套件上**（`SG_W10_ONLY=.` 的过滤轮即可）：
     - `SC_BASH` 指向不存在的文件；
     - helper 一启动就崩：复制一份 aria 检出（只需 `hooks/`），在副本的 helper 第一条可执行语句前加一行 `exit 7`，用 `run-suite.sh` 跑这份副本。
     两种都须报 FAIL、退出码非 0。记下 FAIL 数，以及 V0-H1、V0-H2 的细节。
   - **基线红集，套件上**：经 `run-suite.sh` 对 59e333c 的 hook 跑 `SG_W10_ONLY=.`（PATH 上的 bash）。基线取 `git show 59e333c:hooks/secret-guard.sh`，先断言 sha256 前缀 `e83c5e30f2cc`（INV-9）。与 `base-5.2.15.txt` 按编号对齐：v31 的 MISSING 对应套件的 `FAIL [missing]`；V12-C1 不移植。其余每一处不同逐条解释：口径 (ii)、参照核对、计数方式等。
3. **报告**：写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002c-3d-report.md`（中文），内容：
   - 改了什么；
   - 坏实现逐个的判定，与 v31 的对照；
   - 扰动的结果；
   - 环境错误与基线红集的对照表；
   - 各轮首尾负载；
   - 未做或拿不准的项。

## 纪律

- **工具调用上限 70 次；到第 55 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。
- **输出纪律**：
  - 跑套件与坏实现的输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行；
  - 读文件先 `grep -n` 再按行号读，每次不超过 80 行（`run-mutants.sh`、`run-suite.sh` 除外）；
  - 不要 cat 整份套件或 hook。
- **只改这些文件**：主仓的 `v31/run-mutants.sh`。不改套件、helper、垫片、hook；不 commit。若发现套件或 hook 的缺陷、或规格矛盾，停下写进报告。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验。
  - 开跑前看 `/proc/loadavg`，一分钟负载高于 1.2 先等；等的循环等过之后要显式 `return 0`。
  - 连续等 30 分钟仍高，就先做不依赖墙钟的部分，并在报告里附读数。
- Rule #7：
  - 不打印任何像凭据的值；凭据形字符串只在运行时拼装。
  - 会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）。把文本写进文件（Write / Edit 工具不受它影响），或运行时拼装。
  - 不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
