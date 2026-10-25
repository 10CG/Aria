# TASK-005 任务书：独立代码审查（10CG/aria-plugin#217）

你是 TASK-005 的独立审查席（不是实现或测试的作者）。本项目的 post_implementation / pre_merge 审计闸门为 off；这次审查是 owner 2026-10-22 选的自愿补上（计划 TASK-005 的 reason）。你只读代码、给出发现，不改任何文件（报告除外），不 commit。

## 审什么

- aria worktree：`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`，分支 `feature/secret-guard-w10-failclosed-narrowing`，**审查对象 SHA = `2893bcc`**（hook `hooks/secret-guard.sh` 的 sha256 前缀 `af4658b6f935`）。改动面：`git -C <worktree> diff 8614066..2893bcc -- hooks/`（`8614066` 是分支起点，它的 `hooks/` 与基线 aria `59e333c` 零差异）。文件：`hooks/secret-guard.sh`、`hooks/tests/secret-guard.test.sh`、`hooks/tests/lib/secret-guard-w10-direct.sh`、`hooks/tests/lib/sg-shim/`。
- 规格：`/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`（What 1-7 与各「补充」、性质 P1-P10、「放宽了什么」R-a / R-b / R-c 的申报、残余清单）与同目录 `detailed-tasks.yaml`（invariants INV-1 至 INV-9；TASK-005 的 design 与 acceptance）。已由 owner 裁定、申报过的放宽后果（例如 R-b：读凭据形路径另有无关 `>/dev/null` 的大命令现在放行）不是缺陷，不要重提；但实现若越出申报的范围，就是缺陷。
- 已有的验证（供参考，不必重做）：TASK-002 的整轮与坏实现、TASK-003 的独立坏实现与耗时矩阵、TASK-004 的 W8-W13，都在 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`（`v31/impl/`、`b2/`）。

## 两个阶段

**阶段 1：规格符合。**逐条对实现：INV-1（实现 = 原型 + 三类内容差，W8 已核，可抽查）；INV-3（放宽只在 What 1 的两个触发点进入，触发点之外的代码路径行为逐字节不变）；INV-4（被判定函数直接或间接调用的函数都在 source 闸门之上）；What 1-5 的行为与代码一致；**每一条出错路径都失败即关**（作业失败、截止、检查点、自检、内部错误、读不到 /proc、计时器起不来……都回落成基线拦截，绝不放行；放行只经状态 77）。

**阶段 2：代码质量与安全。**重点（计划 TASK-005 design 点名的，加主控转来的两项）：
1. `_sg_relax_ok` 里 `/proc/sys/fs/binfmt_misc/WSLInterop` 那一项（无 root 造不出该文件，测试覆盖不到）：读法、竞态、在各种 WSL / 非 WSL 状态下是否只会把放宽关掉。
2. helper 与 `v31/sc-direct.sh` 的 root 探测分支（本机 uid 1000，没跑过）：判据是否与 getrlimit(2) 一致、uid 0 下会不会误判。
3. What 7 改写后的 hook 注释与套件注释**说的是不是真的**（commentsync 只核有没有，不核对不对）：逐处对代码核，指出失实或过宽的说法。
4. 用例名字与注释的准确性：V2-G12 / G13 只验关门一极（平台检查失败时 2 oversize、绝不 4），开门一极在 V14-G1；名字或注释若说得比验的宽，记为发现。
5. 只被计时类端到端用例抓住的三处（计时器睡的是剩余时间 `_SG_LEFT`、锚点 `_SG_P0` 只在 hook 起点取一次、作业里 `exec 2>/dev/null`）：要不要补与负载无关的直调用例，给出你的建议与理由。
6. 其余你认为要紧的：作业 / 计时器 / 进程组的竞态与信号、`set -u` 一类的交互、子 shell 与命令替换里的状态、性能上界、可维护性。

可以在 scratchpad 的 `r217impl/t005/` 下写小探针确认某个发现（命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个，不跑整轮或坏实现全量）；不改 hook、套件与 v31 脚本。

## 报告

写到 `/home/dev/Aria/.aria/audit-reports/post_implementation-R1-<当前毫秒时间戳>-secret-guard-w10-failclosed-narrowing-code-reviewer.md`。头部 YAML（与同目录已有报告一致，再加两项）：`checkpoint: post_implementation`、`mode: single-seat`、`rounds: 1`、`converged: true`、`oscillation: false`、`overridden_by_user: false`、`degraded: false`、`verdict: <PASS | PASS_WITH_WARNINGS | FAIL>`、`timestamp: <ISO>`、`context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md`、`agents: [code-reviewer]`、`reviewed_sha: 2893bcc`、`reviewed_hook_sha256_prefix: af4658b6f935`。正文中文：每条发现编号（C-n / M-n / m-n 对应 Critical / Major / Minor），写 file:line、问题、为什么要紧（具体的失败情形）、修法建议；阶段 1 逐条的结论；第 5 项的建议。verdict：0 Critical 且 0 Major 为 PASS；0 Critical 且有 Major 为 PASS_WITH_WARNINGS；有 Critical 为 FAIL。只报你核实过的发现，拿不准的单列为「疑点」。

## 纪律

- **工具调用上限 50 次；到第 40 次时停止新工作，把已完成的写进报告再收尾。**
- **输出纪律**：读大文件先 `grep -n` 再按行号读，每次不超过 120 行；diff 按文件、按段读；不要 cat 整份套件或 hook。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：文本写进文件或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。

最后一条消息用中文：verdict、各级发现的条数与一句话摘要、报告路径、疑点、用了多少次工具调用。
