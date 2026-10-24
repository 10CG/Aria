# TASK-004 第二段任务书：W9 低负载重跑；W13（含全量坏实现与套件模式）；W12 真实流量（含延迟代价）；对照原型那一轮（10CG/aria-plugin#217）

你是 TASK-004 第二段的执行席（全新实例）。主控做独立复核。第一段已完成（任务书 `b2/BRIEF-T004a.md`、报告 `b2/T004a-report.md`）：语料已还原、`v31/run-evidence.sh` 已改（OUT、写文件前的各项核对、页眉记三个用例脚本的 sha）、W8 与 W11 已出、W9 因负载要重跑（见下）。

## 先读：真实流量的纪律（硬约束）

W12 回放的是从本机会话记录抽出的真实大命令，文本可能含凭据。冻结语料在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/traffic-frozen/`（即 `TRAFFIC_DIR`）。**绝不把命令文本读进对话、绝不打印**，只看计数、编号、rc、文案种类、墙钟与 sha256；不拷进任何仓库。不打印任何像凭据的值（Rule #7）。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：文本写进文件或运行时拼装；不要用 `# guard:ack` 绕过。

## 对象与材料

- 实现：aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`（提交 `2893bcc`，hook `af4658b6f935`）；基线 aria `59e333c`（`e83c5e30f2cc`）。
- 计划 `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：invariants（INV-7、INV-8 尤其）与 TASK-004 一节（design 1-8、acceptance 1-6、notes 里第一段的结果、复核与裁定）。
- 证据目录 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`：`v31/run-evidence.sh`（可整份读）、`v31/run-mutants.sh`（套件模式见头注释）、`v31/replay138.sh`、`v31/ident.sh`、`v31/ident32.sh`、`v31/mkdbg31.py`、`evidence/W1-classification.tsv`。原型那一轮的证据一律 `git show 95cf1de7:.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/<文件>`。
- 主控在低负载下跑的原型与实现旧套件输出（W9 的参照）：`.../b2/t004a-verify/suite-proto.out`、`suite-impl2.out`。

## 要改的（`v31/run-evidence.sh`，先写预期再改）

1. **W9 页眉**：现在页眉写在两轮套件跑完之后，文件里没有开始时的负载。改为开跑前取一次页眉作首行、跑完再写一次作末行（与 W11、W12、W13 一致）。
2. **W12 缺 `TRAFFIC_DIR`**（或 `$TRAFFIC_DIR/cmds` 不是目录）：在写任何文件之前退出 3，与其余核对放在一起（现在是跑到 W12 才以 1 退出）。
3. **`W12-replay-138.tsv` 的页眉**（INV-8）：首行加一行以 `#` 开头的页眉；下游读它的 awk 都跳过 `#` 行。核对：加页眉前后，W12 第 1 节的各行汇总逐字相同。
4. **W12 第 1 节加一小节「1b. latency cost」**（design 8）：同一批 138 条在基线 hook 上也回放一次（`replay138.sh` 可直接喂基线：没有探针时 T_trigger 记 `-`），按编号对齐。小节里写：
   - 进入重跑但回落成尺寸文案的结局（实现那一侧有 relax-start、rc 2、尺寸文案）：条数，逐条「编号、实现 W、基线 W、多等的秒数」，以及多等秒数的 p50 / p90 / max；
   - 进入重跑且放行的：条数与多等秒数的 p50 / p90 / max（放行换来的时间代价）；
   - 没有进入重跑的：rc 与 sha256(stderr) 和基线逐条相同的条数（验收 5「没有进入重跑的与基线逐字节相同」；需要的话让基线回放也记 stderr 的 sha256）。

## 要跑的（全部 `IMPL=<实现 hook 的一份拷贝> OUT=<主仓>/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl BASH32=/home/dev/.aria/tools/bash-3.2.57/bash`，工作目录在 scratchpad；命令加 `taskset -c 0,1 nice -n 19`；每个阶段开跑前一分钟负载 < 1.2；INV-7：阶段首尾一分钟读数任一 >= 2 即作废重跑）

1. W9（替换第一段那一份）。
2. W13，带 `MUT_SCOPE=full`（design 5：第 3 节看各坏实现的其他红，64 个变体，每个约 1 分钟）。
3. P-0 另在低负载下单跑一次（design 7）：v31 模式 `MUT_ONLY='P-0'` 与套件模式各一次，记两次读数。
4. 坏实现在移植后的套件上各跑一遍（验收 2 的后半）：`MUT_SUITE=<aria worktree> bash v31/run-mutants.sh <实现> <工作目录>`，输出连同它自己的首行存为 `v31/impl/W13-suite-mutants.txt`。
5. W12（`TRAFFIC_DIR=<traffic-frozen>`）。

## 对照（各写预期再比；有不一致就停下逐条写进报告，不要改 hook、套件或期望值）

- **W9（验收 3）**：变化恰好是 21ab、21ac、21ag、21aj、21al、21ao 六组，检查清单与主控低负载的原型、实现两轮逐条相同；与 95cf1de7 的差异只能是 SC-21ab 那 3 处（原型那一轮负载 3.59 下回落），其余逐条相同。
- **W13（验收 2）**：实现在 5 个 bash 上 FAIL 0（计时类按 INV-7，SKIP 单列）；基线红集与 95cf1de7 的 W13 第 2 节逐栏一致（缺失 / 判错），原型那一轮之后新增或改写的用例（R2 补强、TASK-003 的 V14-*）单列并逐条说明；全部坏实现（BI-1 起与 BI-24 起，等价的除外）在 sc-cases.sh（W13 第 3 节）与套件（W13-suite-mutants.txt）上都被指定用例抓住。
- **W12（验收 5、6）**：第 1 节进入重跑的结局都在 max(T_trigger, 3 s) + 0.3 s 内，没进重跑的与基线逐字节相同；SMAX 类 137 条的放行数 >= 95cf1de7 那份 W12 里的数减 1，少掉的那条必须是回落（基线字节）而不是别的拦截，记下编号；VMAX 那 1 条照旧拦；第 2、3 节 300 / 300 与 40 / 40 逐字节相同。1b 小节的数如实报出（不设门槛，随 TASK-006 的 owner 门呈报）。

## 报告

写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T004b-report.md`（中文）：`run-evidence.sh` 的 diff 与核对；各阶段首尾负载（含作废重跑）；三项对照的逐条结果；1b 的数；未做或拿不准的项。过程材料放 `.../scratchpad/r217impl/t004b/`（不含任何命令文本）。

## 纪律

- **工具调用上限 60 次；到第 48 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。长跑的阶段用后台驱动加等待，不要每分钟查一次。
- **输出纪律**：跑出的输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行；读大文件先 `grep -n` 再按行号读，每次不超过 80 行。
- **只改这一个文件**：主仓的 `v31/run-evidence.sh`；产出写进主仓 `v31/impl/`。不改 hook、套件、其他 v31 脚本、第一段与 TASK-003 的交付；不 commit。
- 同一时刻只跑一个重实验。进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
