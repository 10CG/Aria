# TASK-005 修复轮第四段（5f4）任务书：按复审第三轮改准注释、补目录判据与三处用例（What 1 补充 2 v3.5）（10CG/aria-plugin#217）

你是 TASK-005 修复轮第四段的执笔席（全新实例）。被改的是一个**防泄密安全 hook**（Claude Code 的 PreToolUse secret-guard）。复审第三轮（报告 `/home/dev/Aria/.aria/audit-reports/post_implementation-R3-1792917861650-secret-guard-w10-failclosed-narrowing-code-reviewer.md`，审 aria `3ed6c24`）判 PASS，0 Critical、0 Major，另有 4 条 Minor。主控决定发版前改准 hook 里与代码不符的注释，并顺带收掉其余几条。规格已改成 proposal v3.5，主控在四个 bash 上实跑过新函数（13 种情形）。主控不亲写代码；你按本任务书改、实跑，主控之后独立复核。

## 规格与材料

- proposal `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md` 的 **What 1 补充 2（v3.5）**：准入门第二行与 `_sg_relax_nowslfs` 整个函数——**逐字**照抄（两个代码块，用脚本从 proposal 里取，不要手抄）；正文里的情形清单、已知边角、直调用例清单。
- 计划 `detailed-tasks.yaml` TASK-005 notes 里「复审第三轮」与「复审第三轮主控裁定」两条。
- 修复轮第三段：报告 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/T005f3-report.md`，脚本在 scratchpad 的 `r217impl/t005f3/`（`edit5f3.py`、`prove5f3.sh`、`runall3.sh`、`cmp5f3.sh`、commentsync 的导出做法都可复用）；主控复核在 `b2/t005f3-verify/`。主控 v3.5 的探针在 `r217impl/spec-probe2/`：`spec5.sh` 是 v3.5 的函数，`cases5.sh` 与 `run5.sh` 是 13 种情形，`spec3.sh` 是 v3.4 的函数。
- aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`，当前 `3ed6c24`（hook `16996eb7db21`），工作区干净。

## 要改的

**A. hook**（除下面两处外一字不改；hook 头注释里第三段补的 D-3 那句保持原样）
1. `_sg_relax_ok` 里 `_sg_relax_nowslfs || return 1` 那一行换成 v3.5 第一个代码块的第二行（只有行尾注释变）。
2. `_sg_relax_nowslfs` 整个换成 v3.5 的函数：函数头注释、读出 0 行那一行的注释、binfmt_misc 那一行的注释、`[[ -d "$d" && -x "$d" ]] || return 1` 那一行（代码与注释）。

**B. 用例**（helper 与 `v31/sc-direct.sh` 同一份代码，INV-2）
1. 新增一条（编号接着 W1，名字自拟）：DIR 是 0755 的空普通文件，假表把它列为 binfmt_misc -> 1，stderr 为空；两种模式都跑，不分 uid。
2. V15-W1l（可查不可列）：uid 0 下记 SKIP [platform]，写法照 W1k；原因写明 root 能列出任何目录，这条在 root 下区分不了逐名查与通配。
3. V15-W1n（开销）：叠挂载的循环中途停下（0 < 叠成的层数 < 1000，例如 `fs.mount-max` 偏低）时记 SKIP [platform]，不判 FAIL；一层都叠不上时照旧 SKIP；其余判法不变。
4. 测试侧四份 WSL 判据不用改（它们在「DIR 不是目录」上本来就判有标记）；但要在主控的 13 种情形上（`spec-probe2/cases5.sh`、`run5.sh`），把 hook 的函数与四份判据在 5 个 bash 上逐种对照，须全一致。
5. 新编号进各处清单（helper、套件 `SGW_EXP_DIRECT`、`v31/sc-cases.sh` 的期望清单）；套件头注释的计数随之改。
6. 每条新用例或改过的用例先证明**能红**（或**能 SKIP**）：v3.4 的函数（`spec-probe2/spec3.sh`）上新增那条应红；W1n 的 SKIP 分支用 PATH 前置一个从第 501 次起失败的 `mount` 包装来证明（应记 SKIP [platform]，不是 FAIL）；W1l 的 root 分支本机造不出（uid 1000），写明只做了代码审读。坏实现与包装只放 scratchpad。

**C. v31 工具**：`mutants.py` 与 `impl/w14-mutants.py` 的锚点若因 A 变了就改成新原文（坏实现本身不变；改完全部仍能生成）；`impl/w14-mutants.py` 的 `IMPL_SHA12` 改成新 hook 前缀；`commentsync.py` 照第三段的做法重新导出（target / baseline / proto GREEN，四个构造 RED）。

## 要跑的（输出落 `.../scratchpad/r217impl/t005f4/`；每轮先写预期）

5 个 bash 上 `bash -n`；移植用例 5 个 bash 各一轮过滤轮；整轮两轮（PATH 上的 bash；第二轮导出 `WSL_DISTRO_NAME=Ubuntu`）；`v31/sc-cases.sh`；`v31/run-mutants.sh` 两种模式（P-0 若因负载未判，低负载单跑）；`v31/impl/w14.sh`（写到你的目录）；commentsync。长跑用后台驱动，再用**阻塞的等待循环**等它跑完（每次 Bash 调用超时设 600000 毫秒，没等到就再调一次）——中途不要结束回合、不要发中间消息。

## 报告

用 Bash 写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T005f4-report.md`（中文），被拒就把全文放进最后一条消息：hook 完整 diff（相对 `3ed6c24`）、新用例与改过的用例的代码与「能红 / 能 SKIP」证明、判据对照表、各轮预期与结果与首尾负载（**预期与结果有任何不符都要逐条标出**，即使你认为是预期写错）、未做或拿不准的项。

## 纪律

- **工具调用上限 50 次；到第 40 次时停止新工作，把已完成的写进报告再收尾。**
- 输出纪律：输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行；读大文件先 `grep -n` 再按行号读，每次不超过 80 行；不要 cat 整份套件或 hook。
- **只改这些文件**：worktree 的 hook、套件、helper；主仓 v31 的 `sc-direct.sh`、`sc-cases.sh`、`commentsync.py`、`mutants.py`（只改锚点）、`impl/w14-mutants.py`。不改 proposal、计划与 `v31/README.md`；不 commit。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验；开跑前一分钟负载 < 1.2；计时类结论只在首尾负载都 < 2 时算数（INV-7）。
- Rule #7；会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：文本写进文件或运行时拼装；不要用 `# guard:ack` 绕过。Claude Code 的内置安全检查会拦下它看不透的 `bash -c '…'` 脚本：要用别的 bash 跑一段代码时，把代码写进文件再执行。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
