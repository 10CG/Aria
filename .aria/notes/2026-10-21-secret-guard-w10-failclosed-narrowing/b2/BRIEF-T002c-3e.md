# TASK-002 第三步 3e 任务书：关门重跑的重试；注释去掉 hook 前缀；run-suite.sh 不再吞掉环境错误（10CG/aria-plugin#217）

你是 TASK-002 第三步 3e 段的执笔席（全新实例）。主控不亲写测试代码；你按本任务书改套件与主仓的 `v31/run-suite.sh`、实跑，主控之后独立复核。套件里只改 6 组截止回落判法里 (b) 那一支的关门重跑与 `wpa_x6` 上方的注释块，别处一字不改。
3c2（6 组截止回落按 hook 推出的三条路判）提交在 aria 分支 `feature/secret-guard-w10-failclosed-narrowing` 的 `df2d629`；3d（`v31/run-mutants.sh` 的套件模式）只改了主仓，没动套件。worktree 当前就在 `df2d629` 上，工作区干净。

## 为什么改（主控裁定，技术口径，不动姿态；计划 notes「3c2 主控裁定」）

`wpa_x6` 的 (b)：输出是基线拦截、墙钟 W 在 2-3 s 之间时，同一输入关门再跑一次量 Tb'，Tb' <= W - 1.0 s 才认截止回落（重跑自己的时间检查点让它回落）。3c2 的构造 C3 里有一条 W 2.86 s、Tb' 1.74 s：那条命令平时约 0.66 s，关门那一遍被主机卡了约 1.1 s，离界只差 0.12 s。合法的 (b) 只在重跑被拖过 2 s 时出现，那时主机正忙，紧接着量的 Tb' 也容易被卡，两者相关；只量一次，真实的 (b) 有可观的假红机会。另一处：注释块里「Worked out from the hook (sha256 af4658b6f935)」钉了 hook 前缀，下次改 hook 后会静默过时，没有检查发现得了。

另一处来自 3d（计划 notes「3d 主控裁定」）：`v31/run-suite.sh` 第 18、19 行用 `readlink -f` 把 `SC_BASH`、`SG_W10_LOG` 改成绝对路径；路径的父目录也不存在时 `readlink -f` 输出空串，`SC_BASH` 被清空后回落到 PATH 上的 bash，套件照常全过、退出 0（环境错误被吞掉，fail-open）；`SG_W10_LOG` 被清空后日志静默丢失。同一个值直接跑套件会正确报 FAIL，所以问题只在 `run-suite.sh`。

## 规格与材料（只按行号读需要的段）

- 计划 `/home/dev/Aria/openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml`：TASK-002 notes 里「3c 主控裁定」「3c2 主控裁定」两条（`grep -n` 定位）。
- 套件 worktree `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria/hooks/tests/secret-guard.test.sh`（**不要整份读**）：`wpa_x6` 上方注释块、`wpa_x6_hook`、`wpa_x6` 约 `:2949-3030`（`grep -n` 定位）；Summary 的 6 组行用 `grep -n 'deadline fallback'` 定位。
- 3c2 的报告与材料：`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/T002c-3c2-report.md`、`.../b2/t002f/`（构造 C1、C3 的改动 `c1-hook.diff`、`c3-hook.diff`，驱动脚本可复用）；主控的构造 `.../b2/t002f-verify/c5-hook.diff`（作业在计时器起来后 0.5 s 以 1 结束）。
- `v31/run-suite.sh`（`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`）。

## 要改的（逐字照做）

1. (b) 的关门重跑改为**至多 3 次**：每次与现在相同（同一份输入、同样的变量与目录、清掉预算变量、另加 `WSL_DISTRO_NAME=Ubuntu`），量 Tb'；两次之间 `sleep 1`。某次 0 < Tb' <= W - 1.0 s（微秒整数比较）即记截止回落，不再往下跑；3 次都不满足记一处不符，细节列出全部读数（例如 `gate-closed Tb' 2.33s, 2.41s, 2.38s`），原有的中文句保留。
2. Summary 的 (b) 回落项写成 `W/Tb Xs`，第 k 次（k > 1）才满足时再加 `(try k)`。
3. 注释块：(b) 的说明改成上面的重试，写明理由（只量一次时主机一卡就把合法回落判红；合法的 (b) 只在主机忙时出现，与 Tb' 的卡顿相关；准入门提前关时每次读数都约等于 W，照样红；假绿仍须 W 自身被拖长 1 s 以上）；删掉「(sha256 af4658b6f935)」，保留函数名。6 组共用注释那一句若提到「a gate-closed run」，改成与重试一致的说法。
4. 别处（`wpa_x6` 的 (1)(2)(3a)(3c)、`wpa_x6_eval`、6 组调用行、基线支、W10 移植块）一字不改。
5. `v31/run-suite.sh`：`SC_BASH`、`SG_W10_LOG` 改用 `readlink -m`（只规范成绝对路径，不要求存在），把原值原样交给套件，由套件自己报错；`SG_W10_LOG` 的所在目录不存在时，`run-suite.sh` 以退出码 3 结束并在 stderr 说明（显式要的日志写不出来，不能静默丢失）。头注释同步写明这两条与原因。再用 `grep -n 'readlink -f'` 查 v31 下其余脚本：对可选的环境变量或可能不存在的路径用 `readlink -f`、且没有先核存在的地方，逐处列进报告（不改，主控定夺）。

## 要做的

0. **先写预期，再在 3c2 的代码上跑构造 C6**（证明 C6 在单次判法下会红）。C6 = C3 的 hook（作业开始 2.2 s 后返回 1）外面再包一层：只对设了 `WSL_DISTRO_NAME` 的调用，按输入内容（stdin 的摘要）记一个标记文件，同一输入的第一次关门调用先 `sleep 1.5` 再交给 C3 的 hook，之后的不停（模拟主机只在第一次量 Tb' 时卡顿）。标记目录每轮新建。经 `run-suite.sh` 跑整轮（6 组只在整轮里出现；副本里 SC-13 与 W10 移植批里依赖重跑的用例本来就红，只看 6 组）。预期：走 (b) 的命令（基线那一遍快的，约 7 条）Tb' 约为 Tb + 1.5 s，超过 W - 1.0 s，被判不符。
1. 按上面改套件。
2. 实跑（输出全落 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002h/`），每轮先写预期：
   - C6（新代码）：6 组全部 PASS，截止回落 10 / 10，走 (b) 的那些带 `(try 2)`。
   - C1（准入门恒关，新代码）：6 组全部 FAIL；W < 3.0 s 的触发点命令都判不符，(b) 窗口里的列出 3 次读数；W >= 3.0 s 的记回落（固有限度），逐条列出。
   - C5（主控的快速失败构造，新代码）：6 组全部 FAIL。
   - 实现：worktree 里 PATH 上的 bash 整轮一次（低负载）：FAIL 0，SC-13 绿，截止回落数与明细。
   - `v31/commentsync.py --suite-only <改后的套件> target` 仍为 GREEN。
   - `run-suite.sh` 的三项检查（各先写预期）：`SC_BASH` 指向父目录也不存在的路径、`SG_W10_ONLY=.`：套件报 FAIL、退出码非 0，首行记下原路径；`SG_W10_LOG` 指向不存在的目录：退出 3；正常的过滤轮（`SG_W10_ONLY='^V1-E16'`，带 `SG_W10_LOG`）改前改后各跑一次，日志逐行相同（时间与负载读数之外）。
3. **报告**：写到 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T002c-3e-report.md`（中文）：改了什么（贴 `wpa_x6` 改后全文与注释块的改动处、`run-suite.sh` 的 diff）、`readlink -f` 的清单、各轮预期与结果、首尾负载、每轮 6 组那一行的原文（由脚本提取）、未做或拿不准的项。

## 纪律

- **工具调用上限 45 次；到第 35 次时停止新工作，把已完成的写进报告再收尾。** 上限是硬的。
- **输出纪律**：跑套件的输出一律落文件，对话里只看 `tail`、`grep -c` 与不超过 20 行的 FAIL 或判定行；读文件先 `grep -n` 再按行号读，每次不超过 80 行；不要 cat 整份套件或 hook。
- **只改这两个文件**：worktree 的 `hooks/tests/secret-guard.test.sh`（只动上面「要改的」列出的位置）与主仓的 `v31/run-suite.sh`。不改 hook、helper、垫片与其他 v31 脚本；不 commit。若发现 hook 的缺陷或规格矛盾，停下写进报告。
- 构造只在 `run-suite.sh` 的 hook 副本里做（包装脚本里引用的 hook 用绝对路径，放在你的输出目录下），不改 worktree 的 hook。
- 命令加 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验。开跑前看 `/proc/loadavg`，一分钟负载高于 1.2 先等（等的循环要显式 `return 0`），连续等 30 分钟仍高就照跑，并在报告里附读数。
- Rule #7：不打印任何像凭据的值；凭据形字符串只在运行时拼装。会话自带的旧版 secret-guard 会拦截含凭据形文本或 `| jq …` 一类写法的 Bash 命令行（含 heredoc 正文）。把文本写进文件（Write / Edit 工具不受它影响），或运行时拼装；不要用 `# guard:ack` 绕过。
- 进程只按你自己记下的 PID 清理，禁止 `pkill -f` 一类按模式批量杀。
- 规格有两种读法、或照做会违反某条 INV 时，停下写进报告，不要自行选择。

最后一条消息用中文：各项结论一句话、报告路径、未完成或拿不准的项、用了多少次工具调用。
