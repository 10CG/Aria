# TASK-005 修复轮第二段（5f2）任务书：最后一处同类注释、测试侧的 WSL 判据、V15-T2 余量、INV-4 静态清单（10CG/aria-plugin#217）

你是 TASK-005 修复轮第二段的执笔席（全新实例）。被改的是一个**防泄密安全 hook**（Claude Code 的 PreToolUse secret-guard）。修复轮第一段（5f）已做完、未提交：报告 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T005f-report.md`（先读，尤其第六节），证据在同级 `t005f/`（含坏实现生成 `mkbad.py`、commentsync 导出 `cs/derive-5f.py`、编排 `runall.sh`）。本段收它第六节的第 4、5、7、8 条，并同步 2 条与 commentsync。主控不亲写代码，之后独立复核。

## 现状

- aria worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria`：hook（sha256 前缀 `50ce186a28c9`）、套件、helper 有 5f 的未提交改动，起点 `2893bcc`。
- 主仓 `/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`：`sc-direct.sh`、`sc-cases.sh`、`commentsync.py`、`impl/w14-mutants.py` 有 5f 的未提交改动。
- 规格：proposal 的 What 1 补充 2（hook 的 `_sg_relax_nowslfs`）与 What 7 补充 2；审查报告 `/home/dev/Aria/.aria/audit-reports/post_implementation-R1-1792888152945-secret-guard-w10-failclosed-narrowing-code-reviewer.md`。

## 要改的

1. **hook 只改一行注释**（5f 第六节第 4 条）：重跑块头约 :796 的「returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE」改成与 What 7 补充 2 第 4 处同义（存的是基线的原因串与模式，不是文案）。保持该段行宽；hook 别处一字不改。改前改后逐字记进报告。
2. **测试侧的 WSL 文件判据**（第 5 条）：helper :73 的 `WSLM`、套件 :375 的 `WSLF` 与 :2933 的 `wpa_rx6_wslf`、`v31/sc-cases.sh` :47 的 `WSLF`（及其 :9 的注释），现在都用 `-e /proc/sys/fs/binfmt_misc/WSLInterop`。改成与 hook 的 `_sg_relax_nowslfs` **同一语义、独立写成**（不 source、不调用 hook 来算它）：挂载表 `/proc/self/mounts` 读不出 -> 当作有 WSL 标记；`/proc/sys/fs/binfmt_misc` 上挂着 binfmt_misc 文件系统、且其中有以 `WSLInterop` 开头的项 -> 有；其余 -> 没有；没挂上时绝不去看那里的项。套件两处共用一个小函数；每处的函数都接受可选的挂载表路径与目录参数（与 hook 一样只为验证用，默认值即真实路径）。注释同步改写。
   - 证明：用 5f 的 W1a-d 四种假挂载表与目录，把每份测试侧实现与 hook 的 `_sg_relax_nowslfs` 逐种对照，结论一致（测试侧「有」对应 hook 返回 1）；在本机真实路径上结果仍是「没有」（与改前相同）。
3. **V15-T2 的余量**（第 7 条）：锚点改成「现在减 2.0 s」，断言 0 < `_SG_LEFT` <= 1.0 s；注释写明理由（坏实现重取锚点会得到约 3 s；主机慢只会让这个值更小）。helper 与 `sc-direct.sh` 同改；5f 的 B5、B7、B8 坏实现上仍红、实现上仍绿。
4. **INV-4 的静态清单**（第 8 条）：把 `_sg_relax_nowslfs` 加进「必须定义在 source 闸门之上」的那份清单（`grep -n` 找到它在 helper / `sc-direct.sh` / 套件里的位置）；证明：把它挪到闸门之下的坏实现上，这个静态检查变红。
5. **`impl/w14-mutants.py` 的 `IMPL_SHA12`** 改成第 1 条之后的新 hook 前缀。
6. **commentsync**：照 5f 的做法重新导出（`cs/derive-5f.py`），让第 1 条那句进清单；target、baseline、proto 都 GREEN，四个构造仍 RED。

## 要跑的（输出落 `.../scratchpad/r217impl/t005f2/`；每轮开跑前先写预期）

- 5 个 bash 上 `bash -n`；移植用例 `SG_W10_ONLY=.` 5 个 bash 各一轮（3.2 只许 [platform] SKIP，计时批判过）。
- 整轮：PATH 上的 bash 一轮（FAIL 0，SC-13 绿）；导出 `WSL_DISTRO_NAME=Ubuntu` 一轮（FAIL 0，6 组走基线支）。
- `v31/sc-cases.sh` 在实现上（基线 59e333c）全过。
- `v31/run-mutants.sh` v31 模式与套件模式各一遍指定用例（P-0 若因负载 NOT-JUDGED，低负载下单跑）；`v31/impl/w14.sh`（`W14_OUT`、`W14_DIR` 指向你的目录）31 个全抓住。
- commentsync：target、baseline、proto 与四个构造。

## 报告

用 Bash（python 或 heredoc）写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T005f2-report.md`（中文）；若写文件被拒，把报告全文放进最后一条消息。内容：每处改了什么（hook 那一行的改前改后、测试侧判据的代码）、四项证明、各轮预期与结果、首尾负载、未做或拿不准的项。

## 纪律

- **工具调用上限 50 次；到第 40 次时停止新工作，把已完成的写进报告再收尾。**
- **输出纪律**：输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的判定行；读大文件先 `grep -n` 再按行号读，每次不超过 80 行。
- **只改这些文件**：worktree 的 hook（只第 1 条那一行）、套件、helper；主仓 v31 的 `sc-direct.sh`、`sc-cases.sh`、`commentsync.py`、`impl/w14-mutants.py`。不改 proposal 与计划；不 commit。坏实现只在 scratchpad。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验；开跑前一分钟负载 < 1.2；计时类结论只在首尾负载都 < 2 时算数（INV-7）。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）：文本写进文件或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径（或「报告全文见本消息」）、未完成或拿不准的项、用了多少次工具调用。
