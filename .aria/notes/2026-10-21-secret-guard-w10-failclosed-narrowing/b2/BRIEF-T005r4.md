# TASK-005 第四轮增量复审任务书：审修复轮第四段的 diff（10CG/aria-plugin#217）

你是 TASK-005 第四轮的复审席（全新实例；不是实现、测试或修复轮的作者，也没有参加前三轮）。被审的是一个防泄密安全 hook（Claude Code 的 PreToolUse secret-guard）。第三轮（审 aria `3ed6c24`，报告 `/home/dev/Aria/.aria/audit-reports/post_implementation-R3-1792917861650-secret-guard-w10-failclosed-narrowing-code-reviewer.md`）判 PASS，0 Critical、0 Major、4 条 Minor；主控决定发版前改准注释并收掉这几条，规格改为 proposal v3.5，修复轮第四段据此改了 hook 与用例。按 INV-8 要对新增的 diff 复审。你只读代码、给出核实过的发现，不改任何文件（报告除外），不 commit。

## 审什么

- aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`：`git diff 3ed6c24 b1d3111 -- hooks/`（**审查对象 SHA = `b1d3111`**，hook sha256 前缀 `628652570ce3`）。
- 主仓 v31 的配套改动：`git -C /home/dev/Aria log --oneline -8` 找「修复轮第四段」那一条提交，`git show <它> -- .aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`；另看 `b2921f62` 里 `v31/README.md` 第 41 行的改动（第三轮 m-2）。
- 规格：proposal 的 What 1 补充 2（v3.5：两个代码块、13 种情形、已知边角、直调用例清单）；计划 `detailed-tasks.yaml` TASK-005 notes 里「复审第三轮」「复审第三轮主控裁定」（含停止规则）与第四段的结果和主控复核。第四段报告：主仓 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/T005f4-report.md`；主控复核：`b2/t005f4-verify/`。

## 重点

1. **注释是否属实**：准入门第二行与 `_sg_relax_nowslfs` 的每处注释，逐句对照代码（第三轮 m-1 就是注释说得比代码宽或窄）。
2. **`[[ -d "$d" && -x "$d" ]]`**：是否只会更严；在 root、ACL、LSM、符号链接下的语义；与测试侧四份判据是否在全部输入上同义。
3. **第三轮各条是否处置到位**：m-1、m-2、m-3、m-4，观察一（W1n 叠不满 1000 层）、观察二（路径含空白，主控裁定只记录），疑点 1、2（主控裁定写进已知边角、不改代码）。逐条写结论；若你认为某条记录而不改的处置不够，写出具体的失败情形。
4. **新用例与改过的用例**：新增那条（DIR 是普通文件）、W1l 的 uid 0 分支、W1n 的 SKIP 分支——断言的是不是名字说的东西，会不会恒真、恒红、依赖负载或依赖 uid。
5. 其余你认为要紧的。

**停止规则（主控已定）**：本轮之后若只剩注释措辞类 Minor，记录后不再开修复轮。所以请把发现分清「行为 / 用例能力」与「措辞」两类。

**约束**：与你同时可能在跑 TASK-004 的重跑（重实验，占着 CPU 的 0、1 号核，而且在做计时测量）。你不要跑套件整轮、坏实现或任何重的东西；**不要叠挂载、不要做任何超过几秒 CPU 的探针**。需要确认某个发现时，只做几行的直调探针（`taskset -c 2,3 nice -n 19`），放在 scratchpad 的 `r217impl/t005r4/` 下。

## 报告

写到 `/home/dev/Aria/.aria/audit-reports/post_implementation-R4-<当前毫秒时间戳>-secret-guard-w10-failclosed-narrowing-code-reviewer.md`（用 Bash 写；被拒就把全文放进最后一条消息）。头部 YAML 与第三轮报告相同字段，`rounds: 4`、`reviewed_sha: b1d3111`、`reviewed_hook_sha256_prefix: 628652570ce3`、`previous_report: post_implementation-R3-1792917861650-secret-guard-w10-failclosed-narrowing-code-reviewer.md`。正文中文：每条发现编号（C-n / M-n / m-n），写 file:line、问题、具体的失败情形、修法建议，并标明「行为 / 用例能力」还是「措辞」；第 3 项逐条的处置结论。verdict：0 Critical 且 0 Major 为 PASS；0 Critical 且有 Major 为 PASS_WITH_WARNINGS；有 Critical 为 FAIL。只报核实过的，拿不准的单列为疑点。

## 纪律

- **工具调用上限 35 次；到第 28 次时停止新工作，把已完成的写进报告再收尾。**
- 读大文件先 `grep -n` 再按行号读，每次不超过 120 行；不要 cat 整份套件或 hook。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装；会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文），文本写进文件或运行时拼装，不要用 `# guard:ack` 绕过。Claude Code 的内置安全检查会拦下 `bash -c '…'` 形式的脚本：把代码写进文件再执行。
- 进程只按你自己记下的 PID 清理。

最后一条消息用中文：verdict、各级发现条数与一句话摘要（分「行为 / 用例能力」与「措辞」）、第三轮各条的处置结论、报告路径、疑点、用了多少次工具调用。
