# TASK-005 修复轮第三段（5f3）任务书：按复审第二轮改 WSL 标记的读法（What 1 补充 2 v3.4）（10CG/aria-plugin#217）

你是 TASK-005 修复轮第三段的执笔席（全新实例）。被改的是一个**防泄密安全 hook**（Claude Code 的 PreToolUse secret-guard）。复审第二轮（报告 `/home/dev/Aria/.aria/audit-reports/post_implementation-R2-1792911087903-secret-guard-w10-failclosed-narrowing-code-reviewer.md`）判 PASS_WITH_WARNINGS：Major M-1 是修复轮自己引入的——`_sg_relax_nowslfs` 用 bash 逐行读 `/proc/self/mounts`，开销随挂载数成平方增长（主控实测叠 2000 个挂载 17.2 s），读表在硬截止之外，挂载多的宿主上会超时放行。主控已把规格改成 v3.4，并在四个 bash 上实跑过新代码（正确性 12 种情形与叠挂载下的开销）。主控不亲写代码；你按本任务书改、实跑，主控之后独立复核。

## 规格

- proposal `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md` 的 **What 1 补充 2（v3.4）**：`_sg_relax_ok` 的两行与新的 `_sg_relax_nowslfs`——**逐字**照抄；正文写明了为什么改、各情形应有的结论、直调用例清单。What 3 的 ε 已补 fork 延迟（文档，已改）。
- 复审第二轮报告的 M-1、m-1、m-2、m-3 与疑点；计划 `detailed-tasks.yaml` TASK-005 notes 里「复审第二轮」与其后的主控裁定。
- 修复轮前两段：报告主仓 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/T005f-report.md`、`T005f2-report.md`，脚本与证据在 scratchpad 的 `r217impl/t005f/`、`r217impl/t005f2/`（坏实现生成、commentsync 导出 `cs/derive-5f.py`、编排 `runall2.sh` 可复用）。主控的探针在 `r217impl/spec-probe2/`（`cases3.sh` 与 `run3.sh` 是 12 种情形与假挂载表、`spec3.sh` 是 v3.4 的函数、`perf.sh` 叠挂载计时、`old.sh` 是 v3.3 的函数）。
- aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`，当前 `710a36d`（hook `834dee6db0d0`），工作区干净。

## 要改的

**A. hook**
1. `_sg_relax_ok`：WSL 那一行换成 v3.4 的第一行；在 `_sg_relax_left || return 1` 之后加 v3.4 的第二行；删掉 v3.3 那行 `[[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl`。
2. `_sg_relax_nowslfs` 整个换成 v3.4 的函数（逐字）。
3. What 7 补充 2 第 8 处（复审第二轮 m-2 第二部分）：hook 头注释「Shell variable indirection」那条（约 :93-:101）补一句 D-3 的例外（bash 自身致命错误以 2 退出时原样写出它的报错，仍是拦），措辞与重跑块头那句同义、延续该段行宽。
4. 除此之外 hook 一字不改。

**B. 用例（helper 与 `v31/sc-direct.sh` 同一份代码，INV-2）**
1. 现有 V15-W1a-d 按 v3.4 的结论核对（a 0、b 1、c 0、d 1），需要时改说明文字。
2. **V15-W1e 改成两面**：v3.4 把这一项挪到了平台与时间判据之后，若测试环境里时间判据先失败，桩返回什么准入门都关，用例就恒真了。所以要保证前面的判据都过（锚点、预算、平台照放宽平台的要求，`_sg_relax_noext` 桩成 none），桩返回 0 时准入门须为 0，桩返回 1 时须为 1。
3. 新增（编号接着 W1，名字自拟）：空表 -> 1；同一挂载点 binfmt_misc 之上又叠 autofs、目录里有 `WSLInterop` -> 0（不看项）；把目录当表 -> 1；`set -f` 下 binfmt_misc 加 `WSLInterop-late` -> 1、`shopt -s failglob` 下 binfmt_misc 无项 -> 0，两条 stderr 都为空；binfmt_misc 目录不可查（`chmod 000`）-> 1（uid 0 下不适用，SKIP [platform]，沿用 helper 既有的 root 探测）；可查不可列（`chmod 0311`）加 `WSLInterop-late` -> 1（用例结束前把权限改回，免得临时目录删不掉）；**顺序**：平台判据失败、或没有时间时，`_sg_relax_nowslfs` 根本不被调用（桩成记一次调用）；**开销**：`unshare -rm` 里叠 1000 个 tmpfs 后读真实挂载表，函数 0.5 s 内返回（没有 `unshare -rm` 的宿主上 SKIP [platform]；参照主控的 `spec-probe2/perf.sh`）。
4. 每条新用例或改过的用例都要先证明**能红**：v3.3 的函数（`spec-probe2/old.sh`，空表、叠 autofs、目录当表、noglob / failglob、开销各条应红）、v3.4 去掉 `[[ -x "$d" ]]` 那一行（目录不可查那条应红）、把这一项挪回平台判据之前（顺序那条应红）、W1e 的两面各一个对应的坏实现。坏实现只在 scratchpad。
5. **测试侧的 WSL 判据**（helper / `sc-direct.sh` 的 `wslmark`、套件的 `sg_w10_wslfs`、`v31/sc-cases.sh` 的 `wslmark`）改成与 v3.4 同义：只看该挂载点的最后一条、目录不可查算有、逐个看两个名字、空表或读不出算有。在主控的 12 种情形上（`spec-probe2/cases3.sh`、`run3.sh`）与 hook 的函数逐种对照一致。
6. m-3：V15-T2 的注释把「归零」的位置改准（run 与准入门里那两次 `_sg_relax_left`）。
7. 编号进各处清单（helper、套件 `SGW_EXP_DIRECT`、`v31/sc-cases.sh` 的期望清单）；套件头注释计数随之改。

**C. v31 工具**：`mutants.py` 与 `impl/w14-mutants.py` 的锚点若因 A 变了就改成新原文（错误本身不变；改完全部仍能生成）；`impl/w14-mutants.py` 的 `IMPL_SHA12` 改成新 hook 前缀；`commentsync.py` 照前两段的做法重新导出（target / baseline / proto GREEN，四个构造 RED）。

## 要跑的（输出落 `.../scratchpad/r217impl/t005f3/`；每轮先写预期）

5 个 bash 上 `bash -n`；移植用例 5 个 bash 各一轮；整轮两轮（PATH 上的 bash；导出 `WSL_DISTRO_NAME=Ubuntu`）；`v31/sc-cases.sh`；`v31/run-mutants.sh` 两种模式指定用例（P-0 若因负载未判，低负载单跑）；`v31/impl/w14.sh`（写到你的目录）；commentsync。长跑用后台驱动，再用**阻塞的等待循环**等它跑完（每次 Bash 调用超时设 600000 毫秒，没等到就再调一次）——中途不要结束回合、不要发中间消息。

## 报告

用 Bash 写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T005f3-report.md`（中文），被拒就把全文放进最后一条消息：hook 完整 diff（相对 `710a36d`）、新用例代码与「能红」证明、测试侧判据的对照、各轮预期与结果与首尾负载、未做或拿不准的项。

## 纪律

- **工具调用上限 60 次；到第 48 次时停止新工作，把已完成的写进报告再收尾。**
- 输出纪律：输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行；读大文件先 `grep -n` 再按行号读，每次不超过 80 行；不要 cat 整份套件或 hook。
- **只改这些文件**：worktree 的 hook、套件、helper；主仓 v31 的 `sc-direct.sh`、`sc-cases.sh`、`commentsync.py`、`mutants.py`（只改锚点）、`impl/w14-mutants.py`。不改 proposal 与计划；不 commit。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验；开跑前一分钟负载 < 1.2；计时类结论只在首尾负载都 < 2 时算数（INV-7）。开销用例要建 1000 个挂载，会推高负载：放在各轮之间单独跑，跑完等负载回落再进下一轮。
- Rule #7；会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：文本写进文件或运行时拼装；不要用 `# guard:ack` 绕过。Claude Code 的内置安全检查会拦下它看不透的 `bash -c '…'` 脚本：要用别的 bash 跑一段代码时，把代码写进文件再执行。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
