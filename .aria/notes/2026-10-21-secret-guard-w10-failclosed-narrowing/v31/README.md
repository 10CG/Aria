# 10CG/aria-plugin#217 v3.1 原型与证据（W8、W9、W11–W13）

本目录是 proposal v3.1 的设计钉死所依据的可运行原型、可执行验收与实测结果。v3 的原型与证据在 `../v3/`，那是 post_planning R1 审的对象，保持原样。所有 `W*` 文件都由本目录的 `run-evidence.sh` 生成，不手写、不手改；命令原文不入库，真实流量只出汇总与编号。v3.2 起（TASK-002 第二步，2026-10-24），验收脚本按 post_planning R2 的补强改写，被测对象换成 aria 分支上的实现；`W8`、`W9`、`W11`–`W13` 仍是 v3.1 脚本（`95cf1de7`）在原型上的结果，实现上的结果由 TASK-004 写到 `impl/`。

## 文件

| 文件 | 内容 |
|---|---|
| `mkv31.py` | 从基线 hook 机械生成 v3.1 原型（先断言基线 sha256 前缀 `e83c5e30f2cc`，每处替换必须恰好命中一次）；第 10 步整块重写 What 7 的 8 处 hook 注释 |
| `sc-cases.sh`、`sc-direct.sh` | 验收用例（proposal 的 Success Criteria，v3.2 共 137 个编号）：直调（准入门、截止、桩判定下的作业机制、增长、计数、只匹配规则、文案逐字）、端到端（用被测的 bash 执行 hook）、静态检查，外加两条装置检查（`V0-H1`：直调段跑到末行哨兵；`V0-H2`：每个应有的编号恰好报一次）。输出每条一行 `PASS/FAIL/MISSING/SETUP/SKIP <编号> <细节>`：MISSING 是被测 hook 里没有该用例要调的函数（基线红集用），SETUP 是用例搭不起来 |
| `shapes.py` | 端到端用例的命令文本；凭据形路径运行时拼装，hook 只判文本、从不执行命令 |
| `shim/delay-first`（`shim/jq`、`shim/sed`） | 在已知位置注入固定延迟：`jq` 的首次调用是 stdin 解析（锚点之后、触发点之前），`sed` 只在重跑作业的进程组里停顿（组外的调用不停，也不占「第一次」），停顿开始写 `sed.stall`，停满写 `sed.uncut`；停满说明截止没切断作业，判 FAIL。下界由它决定，不依赖本机速度 |
| `mutants.py`、`run-mutants.sh` | 57 个坏实现，各在被测 hook（实现）上改一处：BI-1–23 是作者自建（BI-17 拆成 17a、17b、17c），BI-24–54 是 post_planning R2 五席漏网的 45 个（逐字节相同的写法合成一个，列出全部席位编号）；另有 7 个常量扰动变体（P-0 必须全绿，其余 6 个各用错一处常量）。逐个只跑指定用例；指定用例全红、且失败细节带 `reasons.tsv` 写明的原因标签，才算抓住。是对用例的自检，不替代 TASK-003 |
| `commentsync.py` | What 7 与 What 7 补充的逐句核对（`--hook-only`、`--suite-only`；baseline / proto / target 模式）。hook 一侧 10 个站点：被改写删掉的旧句须为 0 次，新句须出现在本站点的注释段里；句子从基线、原型与 proposal 机械导出。套件一侧目前只核旧句与旧标题，新句等套件移植写出后再绑定 |
| `run-suite.sh` | 在 aria 回归套件（移植了本目录用例的 `hooks/tests/secret-guard.test.sh`）上跑任意 hook：把 `<aria>/hooks` 复制到临时目录、换上被测 hook 再跑；`SC_BASH`、`SG_W10_ONLY`（只跑编号匹配的移植用例）、`SG_W10_LOG`（逐条结果，本目录格式）照传。副本不是 git 检出，SC-8、SC-9a 不跑，SC-13 在副本里必红，只看 git 检出里的整轮（TASK-002 第三步） |
| `mkdbg31.py`、`replay138.sh`、`ident.sh`、`ident32.sh` | W12：埋点副本（按代码行锚定）、138 条回放、逐字节对比 |
| `fill31.py`、`proposal-template.md` | 从模板与证据生成 proposal：代码块、注释清单表与实测数字都机械填入，并断言 W8 的每个逻辑 hunk 都被引用 |
| `run-evidence.sh` | 生成全部 W 文件；见下 |
| `build-bash.sh` | 本机另建 bash 5.0 / 5.1 / 5.3 的配方（GNU 源码与全部官方补丁，`gpgv` 校验签名） |
| `W8-v31.diff` | 原型相对基线的全部改动 |
| `W13-sc-cases.txt` | v3.1 脚本的验收用例：原型在 bash 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 / 3.2.57 上各一轮；基线作为被测 hook 的一轮（基线红集）；23 个坏实现逐个的结果 |
| `W11-adversarial.txt` | v3 的对抗形状（`../v3/gen-v3.py`）在 v3.1 上的 e2e 矩阵，`LC_ALL=C.UTF-8` |
| `W12-real-traffic.txt`、`W12-replay-138.tsv` | 真实流量：138 条回放（TSV 列：编号、rc、结局、墙钟、首遍完成、触发时刻、作业耗时；单位秒，从调用起算）、300 条逐字节、bash 3.2 下 40 条逐字节 |
| `W9-suite.txt` | aria `59e333c` 的旧套件在基线与原型上各跑一遍（非 git 副本） |
| `ident-300.lst`、`w1-sample40.lst` | 抽样清单（只有编号，与 `../v3/` 相同） |

## 复现

```
bash run-evidence.sh <工作目录> [W8 W13 W11 W12 W9]     # 默认全部阶段
IMPL=<实现的 hook> bash run-evidence.sh <工作目录> …     # TASK-004：在真实实现上重跑
SC_BASH=<bash> bash sc-cases.sh <hook> [基线 hook]       # 单独跑验收用例；基线默认取自 aria 59e333c
SC_BASH=<bash> bash run-mutants.sh <hook> <工作目录>    # 坏实现与常量扰动；MUT_ONLY=<正则> 只跑部分，MUT_SCOPE=full 跑全量并列出其他红
python3 commentsync.py --hook-only <hook> target        # What 7 逐句核对；baseline、proto 模式见脚本头
SC_BASH=<bash> SG_W10_ONLY=<正则> bash run-suite.sh <aria 检出> <hook> [<工作目录>]   # 在移植后的 aria 套件上跑
```

- 基线一律取自 aria `59e333c`（`git show` / `git archive`）并断言 sha256 前缀，不读工作树里的 hook。实现落地后工作树里就是实现，拿它当基线会让所有对比变成自己比自己。
- 每个阶段先写工作目录，成功后复制回本目录：失败或中断不会覆盖已提交的证据，成功的阶段会覆盖同名证据（post_planning R2 PP2-O）。TASK-004 先给脚本加输出目录参数，实现那一轮写到 `impl/`，对照对象取 `git show 95cf1de7:<路径>`。每份输出首行记日期、平台、两个 sha256 前缀与负载；W8 的头两行带生成时的临时路径，复现时只有这两行不同。脚本只能在 Aria 主仓的检出里运行（它用 `git rev-parse --show-toplevel` 找 aria 子模块）。
- W8 的行数：proposal 写 +187 / −49（含 4 行空行）；`run-evidence.sh` 的控制台输出写 `added 183 (blank 4)`，183 不含空行，两者说的是同一件事。
- `sc-cases.sh` 的环境变量：`SC_BASH` 是执行 hook 的 bash，期望值随它而定。判据与收紧后的准入门相同：x86_64 GNU/Linux 构建的 bash 5.0–5.3，内核串读得到且不含 Microsoft、microsoft、WSL，没有 `/proc/sys/fs/binfmt_misc/WSLInterop`，这时期望放宽生效；其余期望与基线逐字节相同。每次起 hook 都清掉 `WSL_DISTRO_NAME`、`WSL_INTEROP`、`CLAUDE_PROJECT_DIR`、`_SG_RELAXED`、`SECRET_GUARD_TIME_BUDGET_S`，HOME 指向私有目录；只有 WSL 用例自己设变量。`SC_ONLY` 按编号过滤；`SC_DIRECT=0` 跳过直调用例；`SC_NICE=0` 不加 `taskset` 与 `nice`；`SC_LOAD_MAX` 是计时批的负载门（缺省 2）。本目录的原型（`mkv31.py`）仍按收紧前。
- W12 需要 `TRAFFIC_DIR`（冻结语料，仓外；抽取用 `../../2026-10-20-secret-guard-scan-cost-and-firstpass-cap/traffic/extract.py`，按 W0 的 sha256 复原编号用 `../traffic/refreeze.py`，只认哈希）与 `BASH32`（bash 3.2 二进制）。W13 的第五轮（bash 3.2）也靠 `BASH32`：不设时脚本静默只跑四个 bash。

## 本机依赖

- GNU/Linux；系统 bash 5.2.15；`/proc`；coreutils `sleep`（小数秒）；`taskset`、`nice`、`jq`、`python3`、`sha256sum`、`gpgv`（只用于构建）、awk、`git`。
- 另建的 bash：`~/.aria/tools/bash-5.0.18`、`bash-5.1.16`、`bash-5.3.20`（`build-bash.sh`，2026-10-22 构建，签名均已校验）；`bash-3.2.57` 由本机更早的会话构建，配方没有留下记录。
- 计时判据的下界由 shim 的固定延迟给出，与负载无关；上界与「重跑须在截止前跑完」类用例依赖本机速度（负载 8–12 下未改动的原型也会红，post_planning R2 PP2-A）。`sc-cases.sh` 开跑时一分钟负载低于 `SC_LOAD_MAX` 才判这一批，否则整批记 `SKIP [load]`；结束时负载到了门槛，这批改记 `SKIP [void]`，须重跑（INV-7）。端到端字节比对里，若一臂撞上装置的 12 s 超时，或 hook 自己的整秒时间预算只在一臂触发，也按计时类处理。真实流量的收益与耗时数字同样随负载变化，每份输出的首行都记了负载。
- `sc-cases.sh` 的 `V5-S10` 用 `ulimit -u 1` 制造 fork 失败，bash 会先重试约 15 s。以 uid 0 或持有 CAP_SYS_RESOURCE、CAP_SYS_ADMIN 运行时，先探测 `ulimit -u 1` 是否真的生效，不生效记 `SKIP [root]`（本机 uid 1000，这一支没有实测）。整轮用时：负载 1–2 约 50 s，负载 6–8 约 64 s，负载 15–20 约 7 分钟；`run-mutants.sh` 跑全部坏实现与扰动、只跑指定用例，负载 1–2 约 4 分钟。
- `check_bare_issue_refs.py` 会把代码里的 bash 取长度写法（如 `${#1}`）当成裸 issue 引用；对 proposal 运行时报出的是这一类，外加 proposal 引用的一处基线 hook 注释里的裸号（共 5 处）。
