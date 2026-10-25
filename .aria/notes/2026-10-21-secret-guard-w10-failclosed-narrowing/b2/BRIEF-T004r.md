# TASK-004 重跑任务书（4r）：hook 经 TASK-005 修复轮改动后，在最终实现上重新生成 W8-W14 并对照（10CG/aria-plugin#217）

你是 TASK-004 重跑段的执行席（全新实例）。TASK-005 修复轮（共四段）改了 hook（What 1 补充 2：WSL 标记的读法，现为 proposal v3.5；What 7 补充 2：注释），按 INV-8 绑定在旧 hook（`af4658b6f935`）上的 W8-W14 全部作废，要在最终实现上重新生成。主控做独立复核。（本任务书前两次派出时对象分别是 `710a36d` 与 `3ed6c24`，都在开跑后不久因复审又要改 hook 被主控停掉；这一次对象是第四段之后的定稿。）

## 先读：真实流量的纪律（硬约束）

W12 回放的是从本机会话记录抽出的真实大命令，文本可能含凭据。冻结语料在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/traffic-frozen/`（即 `TRAFFIC_DIR`；先按 `evidence/W0-corpus-manifest.tsv` 核一遍 2412 条的字节数与 sha256，缺了就按 `traffic/refreeze.py` 的做法从 `traffic-fresh/` 补）。**绝不把命令文本读进对话、绝不打印**，只看计数、编号、rc、文案种类、墙钟与 sha256；不拷进任何仓库。Rule #7。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：文本写进文件或运行时拼装；不要用 `# guard:ack` 绕过。

## 对象

- 最终实现：aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`，提交 `b1d3111`，hook sha256 前缀 `628652570ce3`。基线 aria `59e333c`（`e83c5e30f2cc`）。
- 计划 TASK-004（design 1-8、acceptance 1-6、notes 里两段的结果与裁定、「重跑」那一条）；TASK-005 notes 里修复轮的裁定 (5)：v31 模式 P-0 要在低负载下单跑补上、TASK-003（acceptance 2：耗时矩阵无一越界）、INV-1（现为五类内容差）、INV-7、INV-8。proposal 的 What 1 补充、What 1 补充 2、What 6、What 7 补充、What 7 补充 2（字面）。
- 证据目录 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`：`v31/run-evidence.sh`（已含 OUT、BASH32、TRAFFIC_DIR 核对与 W12 的 1b 小节）、`v31/run-mutants.sh`、`v31/impl/w14.sh`、`v31/impl/w14-matrix.sh`。上一版实现的证据就在 `v31/impl/` 下（它们将被覆盖；对照前先 `git show HEAD:<路径>` 取出旧版）。原型那一轮的证据用 `git show 95cf1de7:...`。

## 要跑的（全部写进 `v31/impl/`；命令加 `taskset -c 0,1 nice -n 19`；每个阶段开跑前一分钟负载 < 1.2；INV-7：阶段首尾一分钟读数任一 >= 2 即作废重跑）

1. `IMPL=<最终 hook 的拷贝> OUT=<…>/v31/impl BASH32=/home/dev/.aria/tools/bash-3.2.57/bash bash v31/run-evidence.sh <scratchpad 下的工作目录> W8 W11 W9`。
2. 同上跑 W13，带 `MUT_SCOPE=full`；P-0 另在低负载下单跑（v31 模式与套件模式各一次，存为 `W13-P0-v31.txt`、`W13-P0-suite.txt`）；套件模式的坏实现全量存为 `W13-suite-mutants.txt`；那一轮基线的原始输出存为 `W13-sc-base.txt`。
3. 同上跑 W12（`TRAFFIC_DIR=<traffic-frozen>`）。
4. TASK-003 的两份：`v31/impl/w14.sh`（写回 `W14-independent-mutants.txt`）与 `v31/impl/w14-matrix.sh full`（写回 `W14-timing-matrix.txt`，`W14_HOOK` 指向最终 hook、`W14_EXPECT_SHA` 为新前缀）。

## 对照（各写预期再比；有不一致就停下逐条写进报告，不要改 hook、套件或期望值）

- W8（验收 1）：`diff 原型 实现` 恰好是 INV-1 的五类内容差，逐 hunk 归类，每类与 proposal 的字面逐字对上。
- W11（验收 4）、W9（验收 3）、W13（验收 2）、W12（验收 5、6）：判据同 TASK-004 notes；另与上一版实现的结果逐项比：结局应完全相同（hook 的行为差只在 WSL 标记的读法：本机不在 WSL、没有 binfmt_misc 挂载，两版的准入门结论相同；v3.4 把这一项挪到平台与时间判据之后、多一次 awk 的 fork，计时类读数可能差几毫秒），差异只能在页眉与墙钟。套件与 sc-cases 多了 V15-W1f 至 W1o 十条（修复轮第三、四段；套件整轮 991，无 zsh 时 985）：与上一版比较时这十条列为新增，其余编号的结局逐项比。V15-W1n 每次在私有挂载命名空间里叠 1000 层 tmpfs（约 2 s），它自己是计时用例。1b 的数如实报出。
- W14：31 个坏实现全抓住（26 按预期 + 5 由补的用例）；耗时矩阵无一越界，与上一版的读数同量级。

## 报告

用 Bash 写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T004r-report.md`（中文），被拒就把全文放进最后一条消息：各阶段首尾负载（含作废重跑）、每项对照的结果、与上一版的逐项比较、1b 的数、未做或拿不准的项。过程材料放 `.../scratchpad/r217impl/t004r/`（不含任何命令文本）。

## 纪律

- **工具调用上限 60 次；到第 48 次时停止新工作，把已完成的写进报告再收尾。** 长跑的阶段用后台驱动加等待，不要每分钟查一次。
- 输出纪律：输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行。
- 只写 `v31/impl/` 下的证据文件；不改任何脚本、hook、套件；不 commit。
- 同一时刻只跑一个重实验；进程只按你自己记下的 PID 清理。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
