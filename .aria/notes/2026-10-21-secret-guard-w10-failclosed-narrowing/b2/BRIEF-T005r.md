# TASK-005 增量复审任务书：审修复轮的 diff（10CG/aria-plugin#217）

你是 TASK-005 的复审席（不是实现、测试或修复轮的作者）。被审的是一个防泄密安全 hook（Claude Code 的 PreToolUse secret-guard）。第一轮审查（报告 `/home/dev/Aria/.aria/audit-reports/post_implementation-R1-1792888152945-secret-guard-w10-failclosed-narrowing-code-reviewer.md`，审 aria `2893bcc`）判 PASS；主控按它的 Minor 与疑点开了修复轮。按 INV-8，hook 改后要对新增的 diff 复审。你只读代码、给出核实过的发现，不改任何文件（报告除外），不 commit。

## 审什么

- aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`：`git diff 2893bcc 710a36d -- hooks/`（**审查对象 SHA = `710a36d`**，hook sha256 前缀 `834dee6db0d0`）。
- 主仓 v31 的配套改动：`git -C /home/dev/Aria diff <修复轮之前的提交>..HEAD -- .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-direct.sh .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/sc-cases.sh .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/commentsync.py .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/w14-mutants.py`（提交号用 `git log` 找「TASK-005 修复轮」那一条及其前一条）。
- 规格：proposal 的 What 1 补充 2（代码与已知边角）、What 3 / 4 / 5 的补充、R-c、What 7 补充 2（含回填的逐字文本）、决策记录第 22 条；计划 TASK-005 notes（第一轮审查结果、主控裁定、修复轮两段的结果与裁定）。修复轮报告：主仓 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/T005f-report.md`、`T005f2-report.md`。

## 重点

1. **What 1 补充 2 的正确性与安全**：`_sg_relax_nowslfs` 在各种挂载表与目录状态下的结论；是否真的不会在没挂上时看那里的项（D-2）；读不出挂载表时是否一律关掉放宽（含 stderr 为空）；`WSLInterop*` 的匹配（D-1）；`set -u`、glob 选项（nullglob / failglob）、bash 3.2 下的解析；准入门两行的短路逻辑；性能（每次到触发点多读一次挂载表）。已认可的已知边角（挂载表路径能打开却读不出时按没挂上处理）不必重提，但若你认为它比主控判断的更危险，写出具体情形。
2. **第一轮的每条 Minor 与疑点是否处置到位**：m-1（VMAX 文案的申报）、m-2（四处注释与回填文本）、m-3、m-4、m-5（只改文档）、m-6（三条直调用例能不能为对的原因变红）、D-1、D-2、D-3。逐条写结论。
3. **新用例与测试侧判据**：V15-T1 / T2 / T3、V15-W1a-e 断言的是不是名字说的东西（会不会恒真、恒红或依赖负载）；测试侧四份 WSL 判据与 hook 的函数是否同义、彼此独立。
4. **注释是否属实**：修复轮改写的每处注释与代码对得上。
5. 其余你认为要紧的。

**约束**：与你同时在跑 TASK-004 的重跑（重实验，占着 CPU 的 0、1 号核）。你不要跑套件整轮、坏实现或任何重的东西；需要确认某个发现时，只做几行的直调探针（`taskset -c 2,3 nice -n 19`），放在 scratchpad 的 `r217impl/t005r/` 下。

## 报告

写到 `/home/dev/Aria/.aria/audit-reports/post_implementation-R2-<当前毫秒时间戳>-secret-guard-w10-failclosed-narrowing-code-reviewer.md`（用 Bash 写；被拒就把全文放进最后一条消息）。头部 YAML 与第一轮报告相同字段，`rounds: 2`、`reviewed_sha: 710a36d`、`reviewed_hook_sha256_prefix: 834dee6db0d0`，另加 `previous_report: post_implementation-R1-1792888152945-secret-guard-w10-failclosed-narrowing-code-reviewer.md`。正文中文：每条发现编号（C-n / M-n / m-n），写 file:line、问题、具体的失败情形、修法建议；第 2 项逐条的处置结论。verdict：0 Critical 且 0 Major 为 PASS；0 Critical 且有 Major 为 PASS_WITH_WARNINGS；有 Critical 为 FAIL。只报核实过的，拿不准的单列为疑点。

## 纪律

- **工具调用上限 40 次；到第 32 次时停止新工作，把已完成的写进报告再收尾。**
- 读大文件先 `grep -n` 再按行号读，每次不超过 120 行；不要 cat 整份套件或 hook。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装；会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文），文本写进文件或运行时拼装，不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理。

最后一条消息用中文：verdict、各级发现条数与一句话摘要、第一轮各条的处置结论、报告路径、疑点、用了多少次工具调用。
