# TASK-004 第一段任务书：还原真实流量语料；改 run-evidence.sh；在实现上重跑 W8、W11、W9 并对照原型那一轮（10CG/aria-plugin#217）

你是 TASK-004 第一段的执行席（全新实例）。计划原定 TASK-004 由主控执行；主控把执行分段交给新实例，自己做独立复核。你按本任务书做，结果交主控复核。

## 先读：真实流量的纪律（硬约束）

本段要从本机的 Claude Code 会话记录里抽出真实的大命令，这些命令文本可能含凭据。规则：
- 命令文本**只放在 scratchpad**：`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/traffic-fresh/`（新抽取）与 `.../scratchpad/traffic-frozen/`（按清单映射后的冻结语料，即 W12 用的 `TRAFFIC_DIR`）。绝不拷进任何仓库。
- **绝不把命令文本读进对话**：不 `cat` / `head` / `grep -o` 这些文件的内容，不打印任何一条命令；只看计数、编号、字节数、sha256。工具脚本本身只打印计数（`extract.py`、`refreeze.py`、`manifest.py` 都是这样写的）。
- 不打印任何像凭据的值（Rule #7）。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：把文本写进文件（Write / Edit 工具不受它影响）或运行时拼装；不要用 `# guard:ack` 绕过。

## 对象与材料

- 实现：aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria` 的 `hooks/secret-guard.sh`（分支 `feature/secret-guard-w10-failclosed-narrowing`，提交 `2893bcc`，sha256 前缀 `af4658b6f935`）；基线 aria `59e333c`（`e83c5e30f2cc`，INV-9）。
- 计划 `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：invariants 与 TASK-004 一节（design 1-8、acceptance 1-6）。proposal 同目录（What 1 补充、What 6、What 7 补充的字面在 proposal 里，INV-1）。
- 证据目录 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`：`v31/run-evidence.sh`（55 行，可整份读）、`v31/mkv31.py`（原型生成器）、`v31/replay138.sh`、`v31/ident.sh`、`v31/ident32.sh`、`v3/matrix.sh`、`v3/gen-v3.py`、`traffic/refreeze.py`、`traffic/manifest.py`、`evidence/W0-corpus-manifest.tsv`（2412 行：编号、字节数、sha256）、`evidence/W1-classification.tsv`（138 条）、`v31/ident-300.lst`（300 个编号）、`v31/w1-sample40.lst`（40 个编号）。抽取工具在 `/home/dev/Aria/.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/traffic/extract.py`。
- 原型那一轮的证据一律用 `git show 95cf1de7:.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/<文件>` 取（design 4），不取工作树。

## 要做的

1. **还原语料**（design 1）：`TRAFFIC_DIR=<scratchpad>/traffic-fresh python3 <extract.py>`；再 `python3 traffic/refreeze.py evidence/W0-corpus-manifest.tsv <traffic-fresh> <traffic-frozen>`。报告：清单 2412 条里找到与缺失的条数；`W1-classification.tsv` 的 138 条、`ident-300.lst` 的 300 条、`w1-sample40.lst` 的 40 条各自找到多少、缺哪些编号（只列编号）。缺失或哈希不符的不跳过，照实记下（W12 里它们只能记为未判）。
2. **改 `v31/run-evidence.sh`**（design 2、6），先写预期再改：
   - 输出目录参数 `OUT`（环境变量；默认仍是脚本所在目录，以便复现 `95cf1de7` 的证据）：各阶段原来「拷到脚本旁边」的地方改为拷到 `OUT`。
   - `BASH32` 或任一被测 bash 不存在（不可执行）即报错退出（退出码 3），不得静默跳过。
   - 页眉函数 `hdr` 另记 `sc-cases.sh`、`sc-direct.sh`、`mutants.py` 的 sha256 前缀（INV-8）；W8 阶段补页眉：`W8-v31.diff` 的第一行写页眉（以 `#` 开头，`patch` / `git apply` 会跳过 diff 之前的文字）。
   - 第 8 行工作目录 `W=$(readlink -f "$1")` 改为 `readlink -m`，并核 `mkdir -p "$W"` 成功，否则退出 3（design 6）。
   - 检查（各写预期再跑）：父目录也不存在的工作目录 -> 退出 3 且没有写出任何文件；`BASH32` 指向不存在的路径跑 W12 -> 退出 3；`OUT` 不设时输出路径与原来相同（读代码核对即可）。
3. **在实现上跑 W8、W11、W9**：`IMPL=<实现 hook 的一份拷贝> OUT=<主仓>/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl bash v31/run-evidence.sh <scratchpad 下的工作目录> W8 W11 W9`（命令加 `taskset -c 0,1 nice -n 19`；开跑前一分钟负载 < 1.2）。
4. **对照**（各写预期再比）：
   - 验收 1（W8）：用 `v31/mkv31.py` 从基线生成原型，`diff 原型 实现` 恰好是 INV-1 的三类内容差（What 1 补充：`_sg_relax_ok` 与 `_sg_relax_platform` 两段；What 6：删掉 `[[ -z "${_SGV_V[j]}" ]] && continue` 那一行；What 7 补充：四处注释），与 proposal 里的字面逐字对上，别无他差。逐 hunk 归类写进报告。
   - 验收 3（W9）：旧套件（59e333c 的套件）在实现上恰好 21ab、21ac、21ag、21aj、21al、21ao 六组变化，每条变化的断言与 `git show 95cf1de7:…/v31/W9-suite.txt` 逐条相同；SC-13 的计数差（非 git 副本）在基线与原型那一轮同样出现，不算变化。
   - 验收 4（W11）：每个形状的结局与 `git show 95cf1de7:…/v31/W11-adversarial.txt` 相同（逐形状比 rc 与文案种类；墙钟不比）。
   - 有不一致：停下，逐条写进报告，不要改 hook、套件或期望值。
5. **报告**：写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T004a-report.md`（中文）：语料还原的计数；`run-evidence.sh` 的 diff 与三项检查；W8 的 hunk 归类；W9、W11 的逐条对照；各轮首尾负载；未做或拿不准的项。过程材料放 `.../scratchpad/r217impl/t004a/`（不含任何命令文本）。

## 纪律

- **工具调用上限 50 次；到第 40 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。
- **输出纪律**：跑出的输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行；读大文件先 `grep -n` 再按行号读，每次不超过 80 行；不要 cat 整份套件或 hook。
- **只改这一个文件**：主仓的 `v31/run-evidence.sh`；新产出写进主仓 `v31/impl/`（W8-v31.diff、W11-adversarial.txt、W9-suite.txt 与 run-evidence.sh 自己拷过去的文件）。不改 hook、套件、其他 v31 脚本；不 commit。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验；开跑前一分钟负载 < 1.2（等的循环要显式 `return 0`）。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
