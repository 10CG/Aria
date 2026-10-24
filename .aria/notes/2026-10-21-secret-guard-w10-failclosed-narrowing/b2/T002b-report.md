# T002b 报告：10CG/aria-plugin#217 TASK-002 第二步（按 post_planning R2 补强可执行验收）

- 执笔：TASK-002 执笔席（全新实例），2026-10-24 约 03:00 起。
- 改动范围：只改主仓 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/` 下的 6 个文件：`sc-cases.sh`、`sc-direct.sh`、`shim/delay-first`、`mutants.py`、`run-mutants.sh`、`commentsync.py`。`shapes.py` 没有改（新用例沿用已有形状，带 `cwd` 的 JSON 在 `sc-cases.sh` 里生成）。没有改 hook，没有改仓内其他文件，没有提交。
- 被测实现：worktree `wt217/aria/hooks/secret-guard.sh`，sha256 前缀 `af4658b6f935`（只读）。基线取自 aria `59e333c`（`e83c5e30f2cc`）。
- 过程产物：`r217impl/t002b/`（下文相对路径都相对它）。原始脚本备份在 `orig/`。

> 第 1–3 节写于负载 9–20 的时段；05:06–05:19 UTC 负载降到 0.8–1.8，计时类整批在低负载下跑完（第 4.6 节），结论已按低负载轮更新。

## 结论

- R2 补强 (a)–(f) 全部写进脚本；用例由 94 条增至 137 条（新增 43 条，`V3-E5` 改了后缀），坏实现 57 个（BI-1–23、BI-17a/b/c、BI-24–54），另有 7 个常量扰动变体。
- **实现在 5 个 bash 上整轮全绿，计时批在低负载下判过**：5.2.15、5.0.18、5.1.16、5.3.20 各 PASS 137、FAIL 0、SKIP 0（5.3.20 第一次结束负载 2.39，按 INV-7 作废重跑，第二次通过）；3.2.57 走 identity，PASS 79。
- **基线红集**（低负载，判过）：PASS 24、判错 FAIL 39、缺失 MISSING 74。W13 第 2 节的 73 红全部仍红（MISSING 51、FAIL 22，`V3-E5` 按新名计）；W13 的 19 绿里，`V7-E15` 改判后变红、`V5-S13b` 变为 MISSING，其余 17 条仍绿。
- **坏实现**：低负载一次跑完全部 57 个（只跑指定用例），57 个都被抓住，且每条指定用例的红都带着 `reasons.tsv` 写明的原因标签（坏实现 78 条、扰动变体 8 条，合计 86 条指定用例全红；64 轮的计时批全部「judged」）。常量扰动：P-0 全量 137 条全绿，6 个用错常量的变体全部被抓住。
- **两种环境错误**：`SC_BASH` 指向不存在的文件 → `SETUP`、退出码 3；`sc-direct.sh` 一启动就崩 → `V0-H1`、`V0-H2` 两条 FAIL、退出码 1。旧版 `_sg_relax_platform` 函数体（无缺省）放回副本后，直调段在 three-args 行中止，被 `V0-H1`（哨兵缺失，附 `$4: unbound variable`）与 `V0-H2`（缺 20 个编号）报出。
- **commentsync**：实现 target GREEN（105 项）；未改动基线上的「插字符绕过」（R2 CR 席的构造）与「整块删除」两种构造，旧版都是 GREEN（复现 PP2-M），新版分别 RED (64)、RED (57)。
- 拿不准、与规格字面不同的地方见第 5 节（INCONCLUSIVE 的范围、e2e 的慢宿主信号、`V5-S13` 预算、套件一侧 commentsync 未绑定新句子等），请主控复核。

## 1. 逐条：R2 补强 (a)–(f) 与 PP2 簇

### (a) 计时类（PP2-A、PP2-B、PP2-C）

| 改了什么 | 钉住它的用例 | 在哪个坏实现上验证 |
|---|---|---|
| **负载门**（`sc-cases.sh`）：开跑时读一分钟负载；低于 `SC_LOAD_MAX`（缺省 2，INV-7）才判计时类，否则这批整体记 `SKIP [load]`，单独计数。结束时再读一次，若批次已判而结束负载 ≥ 门槛，这批结果改记 `SKIP [void]`（作废重跑）。结果先缓存，最后统一输出。 | 所有计时类：直调作业用例（`V4-S1`…`V4-S19` 中走作业的 15 条）与 e2e 的 `deadline`／`outcome` 类 | 高负载下各轮的 `SKIP [load]` 计数（第 4.1 节）；低负载下全部判过（第 4.6 节） |
| **硬／软拆分**：`sc-direct.sh` 对计时类输出 `TIMED <id> <hard> <soft>`；hard = 退出码、文本、字节、下界、桩是否被截止切断（与负载无关，任何负载下错即 FAIL）；soft = 上界与「必须在截止前跑完」（要求 0 或 2 却得到裸回落 4、或 e2e 得到基线字节）。 | 同上 | BI-1、BI-3、BI-19、BI-49 等在负载 10 下仍被 hard 部分抓住（第 4.3 节） |
| `sc-direct.sh` 的 `run()` 改为 `jrun()`：先建临时文件，再在同一时刻取锚点与起秒表（`t0=$EPOCHREALTIME; _SG_P0=$t0`）。 | `V3-S4`、`V5-S5`、`V4-S6` 的下界 | — |
| **sed 垫片只在作业的进程组里停顿**（`shim/delay-first`）：读 `/proc/$$/stat` 取自身进程组，组长的命令行与组长父进程的命令行相同（作业是 hook 命令替换的 fork）才停；组外的调用（父进程的回落文案、基线、不是组长的作业）不停、也不占用「第一次」。停顿开始写 `sed.stall`，停满写 `sed.uncut`。`deadline()` 见到 `sed.uncut` 判 FAIL [uncut]（截止没切断作业）。 | 全部 `deadline` 类（`V6-E2`、`V3-E3`、`V3-E4`、`V3-E5`、`V2-E6`、`V5-E19`） | 拟态脚本（`shimtest/mimic.sh`）：有 `set -m` 时停在作业里（记下组号、停满写 uncut），无 `set -m` 时不停、主进程调用也不停 |
| INCONCLUSIVE：`deadline` 类墙钟 ≥ 停顿时长、且没有「停满」记录时记 `SKIP [inconclusive]`，不判 FAIL；有「停满」记录时判 FAIL。理由见第 5 节第 1 条（拿不准）。 | 同上 | — |
| `V3-E5` 预算改为 2、窗口 1.85..2.6；编号保留 `V3-E5`，后缀由 `budget-1` 改为 `budget-2`（名称要与所测一致，CR-F7 同类）。 | `V3-E5-budget-2` | — |
| 另补（实测发现，规格未写）：e2e 字节比对中，若任一臂撞上装置的 `timeout 12`（rc 124），或 hook 自己的整秒时间预算只在一臂触发（时间文案），按计时类处理（低负载判、高负载 SKIP）。负载 15–20 时实测：实现与基线在同一形状上分别给出时间文案／rc 124，字节比对因负载而假红。见第 5 节第 2 条。 | 全部 e2e | BI-7（回落写时间文案）仍要在低负载下判红，原因标签 `[time-text]` |

### (b) 放行方向 12 类（PP2-D 到 PP2-J、PP2-m12），每类至少一条确定性用例

| R2 类 | 新用例（直调，除注明外） | 坏实现 |
|---|---|---|
| 1 分段触发点不问准入门 | `V2-G12-segment-trigger-asks-gate`（平台桩失败时分段副本超长须得 2 + oversize，不是 4）；整串对照 `V2-G13` | BI-24（CR-MA）、BI-25（QA-M02） |
| 2 项目根只经 stdin cwd | `V2-G14-cwd-extension-file-with-entry`；对照 `V2-G15`、`V2-G16`（环境变量优先）；e2e `V2-E18-extension-via-stdin-cwd`（identity） | BI-26（QA-M01 = TL-M8 = BA-M1） |
| 3 重跑内 for 计数 | `V9-C3-for-statements-rerun`（12 个全收）；对照 `V9-C3b`（基线遍 8 个） | BI-17b（CR-MB = QA-M12 = TL-M1） |
| 4 重跑内 VMAX | `V9-C4-value-limit-in-rerun`（第 17 个赋值超 4096：2 + vmax） | BI-27（QA-M24） |
| 5 重跑内三个时间检查点 | `V4-S16`（收集链）、`V4-S17`（整串）、`V4-S18`（分段）：预算 0，须返回 3 且 stderr 为空 | BI-28/29/30（QA-M06/07/08）、BI-31（BA-M8）、BI-32（TL-M5） |
| 6 先算 credit 再看 longline | `V10-N6-filtered-long-line-rows-only`、`V7-N7-big-judge-filtered-long-line` | BI-33（CR-MC = BA-M4） |
| 7 整串分支漏 `return $?` | `V7-N8-whole-branch-returns-big-judge`（2、longline、恰好一个 BLOCKED 头） | BI-34（TL-M2） |
| 8 分段不路由到 big_judge | `V7-N9-segment-routes-to-big-judge` | BI-35（CR-MD = TL-M3 = BA-M11）、BI-36（QA-M10） |
| 9 量行长漏 `IFS=` | `V7-N10-blank-padded-long-line`（首尾各 4600 个空格） | BI-37（QA-M28 = TL-M4） |
| 10 增长超限放行 | `V8-D4-growth-text-whole`、`V8-D5-growth-text-segment`（2 + 增长文案首行逐字） | BI-38（QA-M18 = BA-M9）、BI-39（QA-M17）、BI-40（BA-M10） |
| 11 非组长 shell 里的作业 | `V5-S15-job-refuses-outside-group-leader`（返回 9、判定未开始） | BI-41（BA-M7） |
| 12 TERM 被忽略时截止仍生效 | e2e `V5-E19-deadline-with-term-ignored`（hook 经 `trap "" TERM; exec` 启动，计时器若用 TERM 则停顿停满 → `[uncut]`／字节不同） | BI-42（QA-M20）、BI-43（QA-M30） |
| 其余：分段回落原因串（PP2-I） | `V6-S20-segment-fallback-text`（门打开时存下的原因串渲染的回落文案，与基线 hook 对同一副本自己的拦截文案逐字节相同）；整串对照 `V6-S21` | BI-45（QA-M09 = BA-M5） |
| 其余：LMAX 8192／8193 边界、量不出行长的哨兵 | `V7-N11-lmax-edge-normal`（恰 `_SGV_LMAX` 字符 → 普通命中）、`V7-N12`（多 1 → longline）、`V7-N13-unmeasured-length-rows-only`（遮住 `read -r line`，循环零次 → 只匹配规则） | BI-46（QA-M13 = TL-M9 = BA-M6）、BI-47（QA-M14）、BI-48（BA-M3） |
| 其余：重跑拦截文案的末尾换行 | `V4-S19-block-text-bytes`（stderr 恰为文本 + 一个换行） | BI-49（QA-M15） |

### (c) 坏实现（`mutants.py`）

- 改为从**实现**构造（读入的 hook 即被测 hook）；每处替换断言恰好命中一次（按给出顺序）。BI-1–23 语义不变，锚点随实现（BI-6 的锚点换成五参数调用行）。
- **BI-17 拆三个**：BI-17a 只漏赋值上限（`V9-C1`）、BI-17b 只漏 for 上限（`V9-C3`，与 CR-MB、QA-M12、TL-M1 逐字节相同）、BI-17c 只漏替换次数上限（`_sg_vx_replace` 与 `_sg_vx_apply` 两处，`V9-C2-…-c12` 与 `-cb12` 各钉一处）。
- **BI-24–54**：五席漏网的 45 个（不含 QA-M29）。几席逐字节相同的构造合成一个 BI，列出全部席位编号；`mutants.py` 对每个席位的写法分别构造，断言字节相同（不同即退出）。另用 `seatcheck.sh` 把每个 BI 的改动行与该席位在原型上的改动行逐个比对：43／45 完全相同，余下 QA-M04、BA-M14 两个只因所改的那一行被 What 1 补充改成了五参数，改动本身（第一个实参换成 `$MACHTYPE`）相同（`dev/seatcheck.txt`）。
- 每个 BI 绑定指定用例，且在 `reasons.tsv` 里写明每条指定用例 FAIL 时必须出现的原因标签（如 `[status]`、`[text]`、`[bytes]`、`[uncut]`）：`run-mutants.sh` 据此判「红的原因与指定的一致」，无关断言碰红记 WRONG-REASON，不算抓住。
- **QA-M29 不入 BI**，改为常量扰动一轮：P-0 = 实现 + `_SGV_GMAX=8190`、`_SGV_LMAX=8200`（须全绿：用例从 hook 读常量；`V8-D2/D3` 的边界长度、`V7-N11/N12` 的行长、`V8-D4/D5` 与 `V11-S5/S7` 的文本都按读到的常量构造）。其上各叠一处「用错常量」：P-M29（行长边界用 SMAX，即 QA-M29）、P-L-sentinel、P-L-text、P-G-limit、P-G-text-whole、P-G-text-segment，各绑定指定用例。

### (d) 用例脚本自身（PP2-K、PP2-L、PP2-m2）

- 残余进程：桩的参数带本轮进程号（`sleep 7.777$U` 等，`U=$$`），只数本轮的；观察前留不超过 1 s 的宽限轮询（每 0.1 s 一次）。
- 金丝雀：起手检查工具（jq、sed、python3、timeout、taskset、nice、小数秒 sleep 等），`"$SC_BASH" -c :` 必须成功，否则 `SETUP` 退出 3。
- `sc-direct.sh` 末行输出哨兵 `END sc-direct`；`sc-cases.sh` 要求末行是哨兵且退出码 0，否则 `FAIL V0-H1-direct-complete`（附末行与 stderr 末三行）。
- 每种模式（relax／norelax）维护应出现的用例编号清单（`EXP_*`，写死在 `sc-cases.sh`），按 `SC_ONLY` 过滤后逐个核对；缺一、多出、重复都记 `FAIL V0-H2-case-list`。
- `SETUP` 单列，不计 FAIL；`run-mutants.sh` 把 SETUP 与 MISSING 记为「未抓住（SETUP）」。
- root 探测：uid 0 或持有 CAP_SYS_RESOURCE／CAP_SYS_ADMIN 时先探测 `ulimit -u 1` 是否真的让 fork 失败，不生效则 `V5-S10`、`V5-S10b` 记 `SKIP [root]`。本机 uid 1000，走不到这一支（第 5 节第 6 条）。
- 注入锚点找不到时，`V5-S10`/`S10b`、`V5-S10c`/`S10d` 两组都输出 `SETUP` 行（原来只输出一行，基线轮因此少两行，PP2-m10）。
- 规格未写、顺带做的：`sc-direct.sh` 支持 `SC_ONLY`，跳过未选中的慢用例（`V5-S10` 的 15 s 重试等），供坏实现只跑指定用例。

### (e) 文字核对（PP2-M、PP2-T）

- **commentsync 改成逐句核对**（`commentsync.py`）：hook 一侧 10 个站点（What 7 的 8 处，加 What 7 补充自成站点的两处 `_sg_vx_replace` 与重跑块头；补充第 1、3 处在站点 2、1 内）。每个站点列出旧文本里被改写删掉的全部句子（共 29 句，各要求 0 次）与新文本的全部句子（共 48 句，须出现在本站点的注释段里；站点由「紧挨着的代码行」或「含某短语的段」定位）。句子由 `cs/derive.py` 从基线、原型（`9f61db0e7b8b`）与规格目标（原型 + What 7 补充四处，取自 proposal）机械导出（`cs/derived.txt`），新文本是 proposal 的，不是从实现抄的。v3.1 的锚点、段哈希、ADD 词保留为附加检查。
- 新增 `proto` 模式：原型上 What 7 的新句子在、补充的新句子不在，证明补充四处的核对能红（原型在 target 模式下 RED (13)，恰好是补充四处）。
- 套件一侧：在原有 7 段 + 5 个标题之外，加入 R2 KM2-14 指出的两处相邻失实注释（21al 段首「the copy limit holds for the braced form ${NAME} too」、21ao 段首「whole-command mode … obeys the same copy limit」）。套件的新句子要等套件移植时写出后再绑定（第 5 节第 4 条）。
- **Rule #6 块 B 的逐字断言**：`V11-S5-longline-head-verbatim`（描述段）、`V11-S6-longline-chinese-line-verbatim`（中文行全文）、`V11-S7-longline-text-verbatim`（整段文案）——期望文本写在 `sc-direct.sh`，已机械核对与 proposal What 5 的 heredoc 渲染后逐字相同（`textcheck/`）；两条增长原因串由 `V8-D4`、`V8-D5` 逐字断言 `Limit hit:` 行。KM-M1（BI-51）、KM-M2（BI-52）、KM-M3（BI-53）、KM-M6（BI-54）在其上变红（第 4.3、4.6 节）。

### (f) 准入门收紧与其余（What 1 补充、PP2-m1、m8、m9、m10、m13、m14）

- `V2-G2` 表按五个参数改写：原 14 行保留编号（`aarch64-unknown-linux-gnu:5.2` 的期望改为 1），新增 7 行：WSL1 内核串、WSL2 内核串、2020 年的 WSL2 内核串（只含小写 microsoft）、只含 WSL 字样的自编内核串、WSL 标记、空内核串、只传三个参数（缺参数须关门、不得中止调用方）。
- `RELAX` 改为与收紧后的准入门同一判据：`BASH_VERSINFO[5]` 为 `x86_64-*-linux-gnu*`、bash 5.0–5.3、`/proc/sys/kernel/osrelease` 读得到且不含 Microsoft／microsoft／WSL、没有 `/proc/sys/fs/binfmt_misc/WSLInterop`。
- `run()` 起 hook 时清掉 `WSL_DISTRO_NAME`、`WSL_INTEROP`（还清 `CLAUDE_PROJECT_DIR`、`_SG_RELAXED`、`SECRET_GUARD_TIME_BUDGET_S`，并把 HOME 指向私有目录，INV-5）；只有 `V2-E17-wsl-mark-keeps-baseline` 设 `WSL_DISTRO_NAME`。直调另有 `V2-G17`、`V2-G18`（两个环境变量各自关门）。`sc-direct.sh` 起手清掉同样几个变量（含 PP2-m14 的预算变量）。
- 环境毒化同时改 `OSTYPE`、`MACHTYPE`、`HOSTTYPE`（`V2-G3b` 直调记录五个实参；`V2-E8` e2e）。本机核实：四个 5.x 与 3.2 都从环境导入这三个变量，`BASH_VERSINFO[5]` 不受影响。
- `deadline()` 在非放宽的 bash 上把附加变量也传给 hook（`identity "$id" "$s" "$@"`）。
- `V7-E15` 改为必须放行（`outcome … multiline-credit 0 none`）；低负载实测该形状 0.5 s 放行。
- 基线红集把「被测函数不存在」记为 `MISSING`，与 `FAIL`（判错）分栏；直调用例先 `need` 检查所需函数。
- `_SG_LEFT` 零填充：`V3-G12-time-left-zero-padded`，用停住的时钟（unset 后的 `EPOCHREALTIME` 失去特殊含义）在锚点后 0.95 s、预算 3 时求剩余时间，须恰为 `2.050000`，与负载无关。

## 2. 用例编号

原有 94 个编号，现有 137 个（`ids-orig.txt`、`ids-new.txt`）：保留 93 个；`V3-E5-budget-1` 改名为 `V3-E5-budget-2`；新增 43 个。

- 装置检查（2）：`V0-H1-direct-complete`、`V0-H2-case-list`。
- 准入门与文案（直调，两种模式都跑，17）：`V2-G2-platform:x86_64-pc-linux-gnu:5.2:` 加 `osrelease-wsl1`、`osrelease-wsl2`、`osrelease-wsl2-2020`、`osrelease-WSL-tag`、`wsl-mark`、`osrelease-empty`、`three-args`（7 行）；`V2-G12-segment-trigger-asks-gate`、`V2-G13-whole-trigger-asks-gate`、`V2-G14-cwd-extension-file-with-entry`、`V2-G15-cwd-project-without-extension-file`、`V2-G16-environment-root-before-cwd`、`V2-G17-wsl-distro-name-closes-gate`、`V2-G18-wsl-interop-closes-gate`；`V11-S5-longline-head-verbatim`、`V11-S6-longline-chinese-line-verbatim`、`V11-S7-longline-text-verbatim`。
- 只在放宽的 bash 上（直调，21）：`V3-G12-time-left-zero-padded`；`V5-S15-job-refuses-outside-group-leader`、`V4-S16-rerun-collect-checkpoint`、`V4-S17-rerun-whole-checkpoint`、`V4-S18-rerun-segment-checkpoint`、`V4-S19-block-text-bytes`；`V6-S20-segment-fallback-text`、`V6-S21-whole-fallback-text`；`V8-D4-growth-text-whole`、`V8-D5-growth-text-segment`；`V9-C3-for-statements-rerun`、`V9-C3b-for-statements-baseline`、`V9-C4-value-limit-in-rerun`；`V10-N6-filtered-long-line-rows-only`、`V7-N7-big-judge-filtered-long-line`、`V7-N8-whole-branch-returns-big-judge`、`V7-N9-segment-routes-to-big-judge`、`V7-N10-blank-padded-long-line`、`V7-N11-lmax-edge-normal`、`V7-N12-lmax-edge-rows-only`、`V7-N13-unmeasured-length-rows-only`。
- 端到端（3）：`V2-E17-wsl-mark-keeps-baseline`、`V2-E18-extension-via-stdin-cwd`、`V5-E19-deadline-with-term-ignored`。
- 改了判据而编号不变的既有用例：`V2-G2-platform:aarch64-unknown-linux-gnu:5.2`（期望 0 → 1）、`V2-G3b`（毒化三个变量、记录五个实参）、`V2-E8`（毒化三个变量）、`V7-E15`（必须放行）、`V8-D2/D3`（边界按 `_SGV_GMAX` 算）、`V5-S12/S13b`（唯一参数 + 宽限；`V5-S13` 这一对的预算改为 3，见第 5 节第 3 条）、全部计时类（硬／软）。

## 3. 坏实现清单（BI-17a/b/c 与 BI-24 起）

| BI | 改动 | 指定用例（原因标签） | 原席位编号 |
|---|---|---|---|
| BI-17a | 重跑内只漏赋值上限（仍 16） | `V9-C1`（[value]） | 作者（BI-17 拆） |
| BI-17b | 重跑内只漏 for 上限（仍 8） | `V9-C3`（[value]） | CR-MB、QA-M12、TL-M1 |
| BI-17c | 重跑内只漏替换次数上限（两函数） | `V9-C2-…-c12`、`-cb12`（[value]） | 作者（BI-17 拆） |
| BI-24 | 分段触发点不问准入门，无条件返回 4 | `V2-G12`（[status]） | CR-MA |
| BI-25 | 分段触发点 `if true` | `V2-G12`（[status]） | QA-M02 |
| BI-26 | 准入门的项目根只取 `CLAUDE_PROJECT_DIR` | `V2-G14`（[status]） | QA-M01、TL-M8、BA-M1 |
| BI-27 | 重跑内 VMAX（收集返回 2）被忽略 | `V9-C4`（[status]） | QA-M24 |
| BI-28 | 重跑内整串时间检查点返回 0 | `V4-S17`（[status]） | QA-M06 |
| BI-29 | 重跑内分段时间检查点返回 0 | `V4-S18`（[status]） | QA-M07 |
| BI-30 | 重跑内收集链检查点返回 0 | `V4-S16`（[status]） | QA-M08 |
| BI-31 | 三个检查点的 `return 3` 删掉（写时间文案） | `V4-S16`、`S17`、`S18`（[status]） | BA-M8 |
| BI-32 | 分段检查点的 `return 3` 删掉 | `V4-S18`（[status]） | TL-M5 |
| BI-33 | 先算 credit，credit 为 0 才出 longline | `V10-N6`、`V7-N7`（[status]） | CR-MC、BA-M4 |
| BI-34 | 整串分支调 big_judge 后漏 `return $?` | `V7-N8`（[status]） | TL-M2 |
| BI-35 | 分段不路由到 big_judge（整行换成普通判定） | `V7-N9`（[status]） | CR-MD、TL-M3、BA-M11 |
| BI-36 | 分段 if/else 两支都是普通判定 | `V7-N9`（[status]） | QA-M10 |
| BI-37 | 量行长的 `read` 漏 `IFS=` | `V7-N10`（[status]） | QA-M28、TL-M4 |
| BI-38 | 整串增长超限放行 | `V8-D4`（[status]） | QA-M18、BA-M9 |
| BI-39 | 分段增长超限跳过（continue） | `V8-D5`（[status]） | QA-M17 |
| BI-40 | 分段增长超限放行（return 0） | `V8-D5`（[status]） | BA-M10 |
| BI-41 | 去掉作业的组长自检 | `V5-S15`（[status]） | BA-M7 |
| BI-42 | 计时器与作业后的组杀都用 TERM | `V5-E19`（[uncut] 或 [bytes]） | QA-M20 |
| BI-43 | 只计时器用 TERM | `V5-E19`（[uncut] 或 [bytes]） | QA-M30 |
| BI-44 | 平台实参取 `$MACHTYPE` | `V2-G3b`（[value]） | QA-M04、BA-M14 |
| BI-45 | 分段触发点存整串原因串 | `V6-S20`（[bytes]） | QA-M09、BA-M5 |
| BI-46 | 行长边界 `>=` | `V7-N11`（[kind]） | QA-M13、TL-M9、BA-M6 |
| BI-47 | 量不出行长时 `max=0` | `V7-N13`（[status]） | QA-M14 |
| BI-48 | 删掉量不出行长的哨兵 | `V7-N13`（[status]） | BA-M3 |
| BI-49 | 重跑拦截文案去掉末尾换行 | `V4-S19`（[bytes]） | QA-M15 |
| BI-50 | `_SG_LEFT` 不补零（`%d.%d`） | `V3-G12`（[value]） | BA-M2 |
| BI-51 | longline 描述段加处方句 | `V11-S5`、`V11-S7`（[text]） | KM-M1 |
| BI-52 | 整串增长原因串改回基线措辞 | `V8-D4`（[text]） | KM-M2 |
| BI-53 | 分段增长原因串改回基线措辞 | `V8-D5`（[text]） | KM-M3 |
| BI-54 | 中文行加处方分句 | `V11-S6`、`V11-S7`（[text]） | KM-M6 |

席位覆盖：五席漏网 46 个，去掉等价的 QA-M29 是 45 个，全部落在上表（BI-24–54 覆盖 42 个，BI-17b 覆盖 3 个）。被抓住的 14 个（CR-ME、QA-M03/05/11/16/19/21/22、TL-M6/M7/M10、BA-M12/M13、KM-M4）不并入。BI-1–23 的指定用例与原因标签见 `mutants.py`／`reasons.tsv`。

常量扰动（不编 BI）：P-0（`_SGV_GMAX=8190`、`_SGV_LMAX=8200`，须全绿）；P-M29（行长边界用 `_SGV_SMAX`，即 QA-M29）→ `V7-N11`；P-L-sentinel → `V7-N13`；P-L-text → `V11-S5`、`V11-S7`；P-G-limit → `V8-D3` 两条；P-G-text-whole → `V8-D4`；P-G-text-segment → `V8-D5`。

## 4. 各轮结果与负载

全部以 `taskset -c 0,1 nice -n 19` 跑、一次一个；每轮首尾的一分钟负载记在各轮输出与 `runs/*/summary.txt`。4.1–4.5 的轮次负载在 4–20 之间，计时类一律 `SKIP [load]`、不作结论，只看不依赖墙钟的部分；计时批见 4.6（低负载，全部补齐）。

脚本的最终 sha256 前缀（本报告写入时）：`sc-cases.sh` `e537079f6738`、`sc-direct.sh` `e97513c59e58`、`shim/delay-first` `637c52c10bbf`、`mutants.py` `2060d2e0c17f`、`run-mutants.sh` `201c646c5a41`、`commentsync.py` `cdab1c8debca`（`shapes.py` 未改，`12ec06e470da`）。4.1 与 4.3 的直调轮是在 `sc-direct.sh` 最后两处修正（第 5 节第 3 条与 `V6-S20` 的输出格式）之前跑的；修正后对受影响的用例与坏实现重跑过（4.3）。

### 4.1 实现：确定性部分（直调 + 静态 + 装置检查，`SC_ONLY='-[GSDCNH][0-9]'`，`runs/det-impl/`）

| bash | 结果 | 负载 首 → 尾 |
|---|---|---|
| 5.2.15 | PASS 98、FAIL 0、MISSING 0、SETUP 0、SKIP 15 [load] | 9.73 → 11.09 |
| 5.0.18 | 同上 | 11.09 → 10.32 |
| 5.1.16 | 同上 | 10.32 → 10.52 |
| 5.3.20 | 同上 | 10.52 → 9.15 |
| 3.2.57（norelax） | PASS 55、其余 0（门关、文案、静态、装置） | 9.15 → 9.30 |

另：实现在 5.2 上的全量一轮（`runs/full-impl-hi/`，负载 7.99 → 5.83，64 s）：PASS 108、FAIL 0、SKIP 29 [load]。6 条 `deadline` 用例都是 `sed-stall=job`（垫片停在作业里），墙钟 3.03–3.06 s（`V3-E5` 2.03 s、`V2-E7` 3.38 s），字节与基线相同；`V9-E11` 回落为基线字节，记 `[fallback]`。

### 4.2 基线红集：确定性部分（`runs/det-base/`，5.2，负载 9.41 → 9.58）

PASS 13、FAIL（判错）26、MISSING 74。

- MISSING 74：准入门、截止值、作业机制、`_sg_vx_big_judge` 一族、`V11-S1` 七条等，即被测函数在基线里不存在。
- FAIL 26：`V2-G11`（环境里的标志没被重置）；`V11-S3`、`V11-S5`、`V11-S6`、`V11-S7`（没有 longline 文案）；`V4-S16/S17/S18`（基线写时间文案、返回 2）；`V6-S20/S21`（基线没有回落路径，状态 2）；`V8-D1` 两条、`V8-D2` 两条、`V8-D4`、`V8-D5`；`V9-C1`、`V9-C2` 两条、`V9-C3`、`V9-C4`；`V10-N2`、`V10-N6`、`V7-N8`、`V7-N9`；`V12-C1`。
- PASS 13：`V2-G12/G13`（基线一律按尺寸拦，与「触发点问准入门」的结局相同）、`V5-S12`、`V8-D3` 两条、`V9-C1b`、`V9-C2b` 两条、`V9-C3b`、`V10-N1`、`V11-S4` 与两条装置检查。
- 与 W13 第 2 节的对照：W13 的 73 红里有 62 条直调与静态用例，本轮全部仍红，分栏为 MISSING 51、FAIL 11（`w13-red-direct.txt`）；其余 11 条是 e2e，见「低负载轮」。W13 的 19 绿里，直调与静态的 `V5-S12`、`V8-D3` 两条、`V9-C1b`、`V9-C2b` 两条、`V10-N1`、`V11-S4` 本轮仍绿；`V5-S13b` 在 W13 里是绿，本轮是 MISSING（它要调用基线里不存在的 `_sg_relax_run`，原来的写法不检查函数是否存在，数到 0 个残留就算绿）。
- commentsync 「插字符绕过」一行的 RED (64) = 旧句 15 + 新句 48 + 站点 10（重跑块头，基线里不存在）1。

### 4.3 坏实现（`run-mutants.sh`，只跑指定用例）

- 直调／静态指定的 42 个（`runs/mut-dir-52/`，负载 10.12 → 10.45）：40 CAUGHT，BI-15 MISSED，BI-45 WRONG-REASON。两者都是用例脚本的问题，已改（第 5 节第 3 条；`V6-S20` 的失败细节原先跨了两行，原因标签落在第二行）。改后重跑（`runs/mut-fix1/`）：BI-45 CAUGHT；BI-15 的 `V5-S13b` 变红（[leftover]），`V5-S9` 是计时类，留待低负载。
- e2e 指定的 15 个（`runs/mut-e2e-hi/`，负载 10.35 → 8.83）：10 个在高负载下已被 hard 部分抓住（BI-4、5、8、10、12、16、17、18、42、43；BI-42/43 的 `V5-E19` 为 `sed-stall=uncut`、墙钟 10.3 s），5 个 NOT-JUDGED（BI-2、6、7、13、14：指定用例里有计时类或 e2e 回落），留待低负载。
- 常量扰动（`runs/pert-det/`）：P-M29、P-L-sentinel、P-L-text、P-G-limit、P-G-text-whole、P-G-text-segment 全部 CAUGHT；P-0 的确定性部分 PASS 98、FAIL 0（`V8-D2/D3` 的边界跟着 `_SGV_GMAX=8190` 走，`V7-N11/N12` 跟着 `_SGV_LMAX=8200` 走）。P-0 全量与上面留待低负载的 6 个坏实现，都在 4.6 补齐。

### 4.4 环境错误（`env/`）

| 构造 | 输出 | 退出码 |
|---|---|---|
| `SC_BASH` 指向不存在的文件（两种：父目录不存在、父目录存在） | `SETUP: SC_BASH does not run: …` | 3 |
| `sc-direct.sh` 一启动就 `exit 1`（v31 脚本的副本） | `FAIL V0-H1-direct-complete`（末行为空、exit 1）、`FAIL V0-H2-case-list`（缺 41 个编号） | 1 |
| 旧版 `_sg_relax_platform` 函数体（无缺省）放回实现副本（`env/impl-old-platform-body.sh`，`5f7ca38b26e9`） | 直调段在 `three-args` 行中止：`FAIL V0-H1`（末行停在 `osrelease-empty`，stderr `line 829: $4: unbound variable`）、`FAIL V0-H2`（缺 20 个编号）；对照：实现本身同一选择 44 条全 PASS | 1 |

### 4.5 commentsync（`cs/`）

| 对象 | 模式 | 结果 |
|---|---|---|
| 基线 hook | baseline | GREEN（95 项） |
| 原型 | proto | GREEN（105 项） |
| 实现 | target | **GREEN（105 项）** |
| 原型 | target | RED (13)：恰好是 What 7 补充的四处 |
| 基线 hook | target | RED (103) |
| 基线 hook + R2 CR 席的「插字符绕过」（`pp-r2-seats/code-reviewer/base-anchor-tweak.diff`） | target | 旧版 GREEN；**新版 RED (64)**（15 句旧句仍在、48 句新句缺失、1 处） |
| 基线 hook + 整块删除 What 7 的 9 段注释并加一行 ADD 词（`cs/mk_delete.py`） | target | 旧版 GREEN；**新版 RED (57)**（48 句新句缺失、9 个站点找不到） |
| 基线套件 | `--suite-only` baseline | GREEN（26 项） |

### 4.6 低负载轮（计时批，INV-7；`runs/low/`、`runs/low2/`、`runs/mut-all-low/`）

等待：04:41 起 `lowload.sh` 等一分钟负载低于 1.5（给本轮自身的负载留余量）。负载 04:41–05:05 在 4–10，05:06 降到 1.3。每轮开跑前要求负载 < 1.5，结束时由 `sc-cases.sh` 自己判：首尾任一读数 ≥ 2 即作废（`SKIP [void]`），作废的轮重跑（每轮最多 3 次）。第一版 `lowload.sh` 有一处缺陷（`waitlow` 在等过之后返回非 0，跳过了实现的 5 轮与计时坏实现一轮，只跑了基线与 P-0），改成 `lowload2.sh` 后补跑。

| 轮 | 结果 | 负载 首 → 尾 | 时刻（UTC） |
|---|---|---|---|
| 基线 × 5.2.15 | PASS 24、FAIL 39、MISSING 74，judged | 1.32 → 1.70 | 05:06:20–05:06:35 |
| P-0 × 5.2.15（全量） | PASS 137、FAIL 0、SKIP 0，judged | 1.44 → 1.37 | 05:06:55–05:07:44 |
| 实现 × 5.2.15 | PASS 137、FAIL 0、SKIP 0，judged | 1.27 → 1.42 | 05:08:00–05:08:50 |
| 实现 × 5.0.18 | 同上 | 1.42 → 1.76 | 05:08:50–05:09:39 |
| 实现 × 5.1.16 | 同上 | 1.32 → 1.69 | 05:09:59–05:10:49 |
| 实现 × 5.3.20 第 1 次 | **作废**：结束负载 2.39，29 条计时结果记 `SKIP [void]`（其余 108 PASS） | 1.43 → 2.39 | 05:10:59–05:11:49 |
| 实现 × 5.3.20 第 2 次 | PASS 137、FAIL 0、SKIP 0，judged | 1.35 → 0.76 | 05:13:09–05:13:58 |
| 实现 × 3.2.57（identity） | PASS 79、FAIL 0 | 0.76 → 1.44 | 05:13:58–05:14:33 |
| 计时类坏实现 BI-2、6、7、13、14、15 | 6／6 CAUGHT，judged | 1.44 → 1.22 | 05:14:33–05:15:01 |
| 全部 57 个坏实现 + 常量扰动 7 个（汇总一轮） | 57／57 CAUGHT；P-0 GREEN；6／6 CAUGHT；64 轮全部 judged | 1.11 → 1.48 | 05:15:20–05:18:53 |

实现在 5.2.15 上的计时细节：6 条 `deadline` 用例都是 `sed-stall=job`，墙钟 3.02 s（`V3-E5` 2.02 s，`V2-E7` 3.30 s），字节与基线相同；`V9-E11` 在 1.00 s 给出 tmax 文案；`V7-E15` 0.41 s 放行；`V3-S4` 1.01 s；`V5-S10` 15.00 s。五个 bash 的数值相近（`runs/low2/impl-*.txt`）。

基线红集的 e2e 部分：FAIL 13 = W13 的 11 条（`V3-E5` 按新名）+ `V7-E15`（改判为必须放行，基线拦）+ `V5-E19`（基线不经停顿、0.10 s 就拦，`[wall<lo]`）；PASS 11 = `V2-E7`、`V2-E9`、`V9-E12`、`V1-E16` 六条，以及新增的 `V2-E17`、`V2-E18`。与 W13 第 2 节逐栏对照：W13 的 73 红全部仍红（MISSING 51、FAIL 22）；19 绿中 17 条仍绿，`V7-E15` 变红（判据改了，R2 PP2-m9 的本意），`V5-S13b` 变 MISSING（见 4.2）。

## 5. 拿不准、与规格字面不同、或没做的

1. **INCONCLUSIVE 的范围（规格有两种读法，按能同时满足 (a) 与 (b) 的读法做了，请主控复核）。** (a) 写「sed 垫片停顿前核对自己在作业的进程组里，不在就不停（或停顿缩到 4 s），deadline 类用例见到墙钟 ≥ 停顿时长判 INCONCLUSIVE」。我选了前一种（组内才停）。若再按字面「墙钟 ≥ 停顿时长一律 INCONCLUSIVE」，就与 (b)「TERM 被忽略时截止仍生效」冲突：QA-M20/M30 的特征正是作业里的停顿没被切断、停满 10 s（墙钟 10.3 s），字面规则会把它们记成 INCONCLUSIVE，永远抓不住。所以现在的规则是：垫片记录「停满」（`sed.uncut`）时判 FAIL [uncut]；墙钟 ≥ 停顿时长而没有「停满」记录时才记 `SKIP [inconclusive]`。对正确实现两种读法结果相同（组内停顿总被截止切断）；对 BI-2、BI-4（没有作业进程组）也相同（不停顿，靠字节抓住）。
2. **e2e 字节比对里加了「慢宿主」信号（规格未写）。** INV-7 的前提是「字节比对不受负载影响」。负载 15–20 时实测不成立：hook 自己的整秒时间预算会在一臂触发（时间文案），或撞上装置的 `timeout 12`（rc 124），两臂字节因此不同（第一次整轮在实现上因此红了 `V9-E12`、`V5-E19`）。现在这两种情形按计时类处理：低负载判 FAIL，高负载 `SKIP [load]`。副作用：BI-7（回落写时间文案）只能在低负载轮判红（原因标签 `[time-text]`）。
3. **`V5-S13`／`V5-S13b` 的预算改为 3（规格未写）。** (d) 要求观察前留不超过 1 s 的宽限；直调作业的截止是 1 s，宽限一满，正确实现与 BI-15（作业结束后不杀组）都靠作业自己的计时器在 1 s 时把残留杀掉，`V5-S13b` 因此抓不住 BI-15（实测 MISSED）。改为只对这一对用预算 3：宽限仍是 1 s，计时器 3 s 才到。改后 BI-15 的 `V5-S13b` 变红，实现仍绿。
4. **套件一侧的 commentsync 只做了一半。** 旧句 0 次（含 KM2-14 的两处）已写；「站点内必须出现的新句子」要等套件移植时写出新注释后才能绑定，本步没有、也不应由我先替套件定文字。`proposal.md` 的 What 7 也没有给套件 7 段的目标全文。套件移植那一步须补上，否则套件一侧的整块删除仍会 GREEN。
5. **编号**：`V3-E5` 的后缀由 `budget-1` 改为 `budget-2`（预算改了，名字跟着改；编号 `V3-E5` 不变）。新增的准入门用例接在 `V2-G11` 之后从 `V2-G12` 编；`V2-G2` 表的新行用 `V2-G2-platform:<机器>:<版本>:<变体>`。若主控要求后缀也不动，需改回并在报告里说明「名不副实」。
6. **root 分支没有实测。** 本机 uid 1000、无相关 capability，`nproc_binds` 的探测分支走不到；判据比规格的「root」宽一点（uid 0，或持有 CAP_SYS_RESOURCE／CAP_SYS_ADMIN，与 getrlimit(2) 一致）。
7. **`/proc/sys/fs/binfmt_misc/WSLInterop` 这一条 WSL 标记没有用例**：本机无 root，造不出这个文件；`_sg_relax_ok` 里读它的那一项只有代码审读覆盖（TASK-005）。环境变量两条有直调（`V2-G17`、`V2-G18`）与 e2e（`V2-E17`）。
8. **`V3-G10` 未改**：它在真时钟上量剩余时间（下界 2.9 依赖两条语句之间的耗时），极高负载下理论上可能假红；本步各轮都是绿。`V3-G12` 用的是停住的时钟。
9. **`README.md` 未改**（不在本步可改的文件里）。以下几行已与脚本不符，需主控或下一步更新：第 12 行（垫片现在只在作业的进程组里停顿）、第 13 行（坏实现由实现构造，57 个 + 7 个扰动变体，按原因标签判抓住）、第 14 行（commentsync 逐句、新增 proto 模式）、第 37 行（`RELAX` 已按收紧后的准入门推导；新增 `SC_LOAD_MAX`）、第 44–45 行（计时类在负载 ≥ 2 时整批 SKIP；整轮用时）。
10. **坏实现的「其他红」**（W13 第 3 节那一栏）没有统计：本步按指定用例跑（`MUT_SCOPE=designated`），全量跑法（`MUT_SCOPE=full`）在高负载下每个约 1–7 分钟，留给 TASK-004 的 W13。
11. **套件移植（`aria/hooks/tests/secret-guard.test.sh`）不在本步**，TASK-002 验收里「移植后的套件上各跑一遍指定用例」也不在本步。
12. **单轮耗时**：负载 15–20 时整轮 `sc-cases.sh` 约 7 分钟（超出任务书「约 2 分钟」），负载 6–8 时约 64 s。

## 6. 复现与文件

- 实现一轮：`SC_BASH=<bash> taskset -c 0,1 nice -n 19 bash v31/sc-cases.sh <hook>`（基线默认取 aria `59e333c`）；只跑确定性部分加 `SC_ONLY='-[GSDCNH][0-9]'`。
- 坏实现：`SC_BASH=/usr/bin/bash bash v31/run-mutants.sh <hook> <工作目录>`（`MUT_ONLY=<正则>` 只跑部分，`MUT_SCOPE=full` 跑全量并列出其他红）。
- commentsync：`python3 v31/commentsync.py --hook-only <hook> target`（`baseline`／`proto` 模式见脚本头注释）。
- 本步脚本：`runsc.sh`（逐个 bash 跑一轮、首尾记负载）、`lowload.sh`（等负载低于 1.5 再跑计时批，每轮最多 3 次直到「timing batch: judged」）、`dev/seatcheck.sh`、`cs/derive.py`、`cs/gen_literal.py`、`cs/mk_delete.py`、`shimtest/mimic.sh`、`textcheck/`。
- 各轮输出：`runs/det-impl/`、`runs/full-impl-hi/`、`runs/det-base/`、`runs/mut-dir-52/`、`runs/mut-fix1/`、`runs/mut-e2e-hi/`、`runs/pert-det/`、`env/`、`cs/`；低负载轮 `runs/low/`（基线、P-0；`log` 记每轮首尾负载）、`runs/low2/`（实现 5 轮与计时坏实现；`log` 同上，含作废与重跑）、`runs/mut-all-low/`（57 个坏实现与常量扰动的汇总一轮，`summary.txt`）。低负载轮所用脚本的 sha256 与第 4 节开头列的最终值相同（各轮输出首行）。
- 清理：所有运行都在 scratch 里；进程只按自己记下的 PID 处理，没有按模式批量杀进程；`git -C /home/dev/Aria status` 只有本步改的 6 个 v31 文件。
