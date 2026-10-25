# TASK-005 第三轮增量复审任务书：审修复轮第三段的 diff（10CG/aria-plugin#217）

你是 TASK-005 第三轮的复审席（全新实例；不是实现、测试或修复轮的作者，也没有参加前两轮）。被审的是一个防泄密安全 hook（Claude Code 的 PreToolUse secret-guard）。第一轮（审 aria `2893bcc`）判 PASS；修复轮第一、二段后，第二轮（审 `710a36d`，报告 `/home/dev/Aria/.aria/audit-reports/post_implementation-R2-1792911087903-secret-guard-w10-failclosed-narrowing-code-reviewer.md`）判 PASS_WITH_WARNINGS：Major M-1 是 `_sg_relax_nowslfs` 逐行读 `/proc/self/mounts` 的开销随挂载数成平方增长。主控把规格改成 proposal v3.4，修复轮第三段按它改了 hook 与用例。按 INV-8 要对新增的 diff 复审。你只读代码、给出核实过的发现，不改任何文件（报告除外），不 commit。

## 审什么

- aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`：`git diff 710a36d 3ed6c24 -- hooks/`（**审查对象 SHA = `3ed6c24`**，hook sha256 前缀 `16996eb7db21`）。需要时也看 `git diff 2893bcc 3ed6c24 -- hooks/secret-guard.sh`（修复轮三段合起来的 hook 改动）。
- 主仓 v31 的配套改动：`git -C /home/dev/Aria log --oneline -8` 找「修复轮第三段」那一条提交，`git show <它> -- .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`。
- 规格：proposal `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md` 的 What 1 补充 2（v3.4：为什么、代码、主控实跑的 12 种情形、直调用例清单）、What 3 的耗时上界与 ε、What 7 补充 2（第 8 处与回填的逐字文本）；计划 `detailed-tasks.yaml` TASK-005 notes（第二轮结果与主控裁定、第三段的结果与主控复核）。第三段报告：主仓 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/T005f3-report.md`；主控复核：`b2/t005f3-verify/`。

## 重点

1. **v3.4 的 `_sg_relax_nowslfs` 的正确性与安全**：在各种挂载表、目录状态与 shell 选项下的结论；只取该挂载点最后一条是否真等于「最上层」，有没有反例（例如挂载在 DIR 的父目录或更上层、`/proc/self/mounts` 里的转义、移动过的挂载）；会不会在 binfmt_misc 不是最上层时碰 DIR 下的东西（D-2）；awk 的各种失败（不存在、读不出、输出异常、不同 awk 实现：本机是 mawk）是否一律关掉放宽且 stderr 为空；`[[ -x ]]` 与 `-e` 在 root、ACL、LSM 下的语义；bash 3.2 下的解析。
2. **准入门的顺序**：这一项挪到 `_sg_relax_platform` 与 `_sg_relax_left` 之后，有没有让某条路径在 WSL 上放宽（环境变量那一行仍在平台判据之前、经 `$wsl` 传给它）；`_sg_relax_left` 之后多了一次 awk 的 fork，What 3 的上界是否仍成立（run 里还会再查一次时间）。
3. **第二轮各条是否处置到位**：M-1、m-1、m-2（两部分）、m-3、疑点 1。逐条写结论。
4. **新用例与测试侧判据**：新增与改过的 V15 用例断言的是不是名字说的东西（恒真、恒红、依赖负载、依赖 uid）；W1e 两面是否真让前面的判据都过；开销用例的界是否既抓得住逐行读又不会在正常主机上误红；测试侧四份 WSL 判据与 hook 的函数是否同义。
5. **注释是否属实**：第三段改写的每处注释与代码对得上（含 hook 头注释补的 D-3 例外）。
6. 其余你认为要紧的。

**约束**：与你同时在跑 TASK-004 的重跑（重实验，占着 CPU 的 0、1 号核，而且在做计时测量）。你不要跑套件整轮、坏实现或任何重的东西；**不要叠挂载、不要做任何超过几秒 CPU 的探针**（第二轮的叠挂载探针把一分钟负载推到 6.94，干扰了并行的计时测量）。开销方面以第三段报告与主控复核里的读数为准，你可以核对它们的做法与数字是否自洽。需要确认某个发现时，只做几行的直调探针（`taskset -c 2,3 nice -n 19`），放在 scratchpad 的 `r217impl/t005r3/` 下。

## 报告

写到 `/home/dev/Aria/.aria/audit-reports/post_implementation-R3-<当前毫秒时间戳>-secret-guard-w10-failclosed-narrowing-code-reviewer.md`（用 Bash 写；被拒就把全文放进最后一条消息）。头部 YAML 与第二轮报告相同字段，`rounds: 3`、`reviewed_sha: 3ed6c24`、`reviewed_hook_sha256_prefix: 16996eb7db21`、`previous_report: post_implementation-R2-1792911087903-secret-guard-w10-failclosed-narrowing-code-reviewer.md`。正文中文：每条发现编号（C-n / M-n / m-n），写 file:line、问题、具体的失败情形、修法建议；第 3 项逐条的处置结论。verdict：0 Critical 且 0 Major 为 PASS；0 Critical 且有 Major 为 PASS_WITH_WARNINGS；有 Critical 为 FAIL。只报核实过的，拿不准的单列为疑点。

## 纪律

- **工具调用上限 40 次；到第 32 次时停止新工作，把已完成的写进报告再收尾。**
- 读大文件先 `grep -n` 再按行号读，每次不超过 120 行；不要 cat 整份套件或 hook。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装；会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文），文本写进文件或运行时拼装，不要用 `# guard:ack` 绕过。Claude Code 的内置安全检查会拦下 `bash -c '…'` 形式的脚本：把代码写进文件再执行。
- 进程只按你自己记下的 PID 清理。

最后一条消息用中文：verdict、各级发现条数与一句话摘要、第二轮各条的处置结论、报告路径、疑点、用了多少次工具调用。
