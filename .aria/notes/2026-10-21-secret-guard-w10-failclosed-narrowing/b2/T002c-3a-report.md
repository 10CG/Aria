# T002c-3a 报告：v31 新用例移植进 aria 套件（10CG/aria-plugin#217 TASK-002 第三步 3a）

## 结论

- 移植完成：136 个编号（134 个用例，加装置检查 V0-H1 / V0-H2；V12-C1 按口径 (v) 不移植）。直调在 helper `hooks/tests/lib/secret-guard-w10-direct.sh`，端到端与静态在套件函数 `sg_w10_cases`；垫片、两个开关、按原因的 SKIP 计数、SC-13 改造、`v31/run-suite.sh` 均已落地。hook 未改（每轮记录 sha256 前缀 af4658b6f935），未 commit。
- 基线轮与开跑前写下的预期完全一致（第 0 节）。
- W10-only 轮（同一 worktree，`SG_W10_ONLY=.`）：5 个 bash 的计时批都在第一次就判过；5.0 / 5.1 / 5.2 / 5.3 各 136 PASS，3.2 为 78 PASS + 58 SKIP [platform]，0 FAIL。
- 整轮（同一 worktree，git 检出）：5 个 bash 总数都是 961（= 头注释的 without-zsh 数），SC-13 都是绿，旧用例的红恰为 W9 那 6 组，移植用例 0 FAIL。**但整轮里 W10 计时批全部是 SKIP [load]，任务书第 7 步「低负载、计时批判过」在整轮里没有满足**；原因与两种读法见第 6 节第 1 条，需要主控裁定。
- 等价核对（5.2，两边计时批都判过）：136 个共有编号，状态逐条相同；唯一的差异是 V12-C1 只在 v31 里（不移植）。
- 抽查能红：BI-24、BI-7、BI-11 经 `run-suite.sh` 都按 `reasons.tsv` 的原因标签变红；同样 4 个指定用例在实现上全绿。

## 0. 基线轮（改动前，先写预期再测）

预期（写于开跑前）：worktree 是 git 检出，af87cae 可达，SC-8、SC-9a 照常跑。实现 21a37ea（af4658b6f935）在 PATH 上的 bash 5.2 下放宽生效，
依据 v31/W9-suite.txt 的 impl 栏（原型；实现与原型只差 INV-1 的三类内容差，不影响这 6 组在本机放宽生效时的结局），
预期 FAIL 恰为 6 条：W10 SC-21ab、21ac、21ag、21aj、21al、21ao；SC-13 绿（头注释 831 / 825 without zsh，本机有 zsh 则总数 831，否则 825）。
即 PASS 825/831（或 819/825）、FAIL 6。风险：SC-8 是性能档（min-of-rounds），本机负载高时可能受影响。

实测（`t002c/base-suite.txt`）：2026-10-24T06:33:21Z 到 06:39:48Z，负载 3.43 → 3.84，本机无 zsh，bash 5.2.15。PASS 819 / 825，FAIL 6，恰为 SC-21ab、21ac、21ag、21aj、21al、21ao；SC-13 绿（825 = without zsh 的数）；SC-8 各档未红。与预期一致。

## 1. 改了哪些文件

aria worktree（`wt217/aria`，feature 分支 21a37ea 之上，未 commit）：

1. `hooks/tests/secret-guard.test.sh`（+331 / −4，sha256 前缀 53f1eaefaf72）
   - 头注释：Coverage 改为 `967 cases (961 without zsh)`；其后补 13 行说明：136 个移植用例、`SC_BASH`、垫片、`timeout` 依赖、两个开关、SKIP 的原因与计法。
   - `:133-:442` W10 块：编号清单、`sg_w10_rep` / `sg_w10_shape`（shapes.py 的 bash 版）、端到端与计时判定函数、`sg_w10_static`、`sg_w10_cases`（`:320`）；`:428` 起是 `SG_W10_ONLY` 过滤轮（调用函数、打印注明「FILTERED ROUND」的汇总后退出）。
   - `:3536` 在 SC-13 之前调用 `sg_w10_cases`。
   - SC-13：`sc13_total_expected=$((pass + fail + skip + 1))`（`:3548`），其上注释同步为 `pass+fail+skip+1`。
   - Summary：`total` 含 SKIP；新增 `SKIP: n / total (platform…, load…, void…, inconclusive…, root…, other…)` 与 `W10 ported cases: <SC_BASH、放宽预期、首尾负载、timing batch>` 两行。SKIP 不影响退出码。
   - 未碰：W10 旧用例块及其注释、标题（3b），其余旧用例。
2. 新建 `hooks/tests/lib/secret-guard-w10-direct.sh`（477 行，sha256 前缀 265a7b8d9b63）：由 `t002c/patch3a.py` 从 v31/sc-direct.sh 逐处替换生成（每处断言恰好命中一次）。与 v31 的差异只在这些 hunk：头注释；`H=$1; MODE=$2`（去掉 BASE）；`RELAX_IDS` 清单（`:56-:68`）；V5-S13b、V5-S12 的 `ps` 前提；fbt 的关门臂（注释、basefb.sh 三行、调用与细节文字）；norelax 分支逐个输出 SKIP [platform]（`:470-:475`）。其余与 v31 逐字相同，末行哨兵仍是 `END sc-direct`。
3. 新建 `hooks/tests/lib/sg-shim/`：`delay-first` 与 v31/shim/delay-first 逐字节相同（cmp 核过，sha256 前缀 637c52c10bbf，0755）；`jq`、`sed` 是指向 `delay-first` 的相对符号链接。

主仓（未 commit）：

4. 新建 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-suite.sh`（sha256 前缀 711a0201e23b）：`run-suite.sh <aria 检出> <hook> [<工作目录>]`。复制 `<aria>/hooks` 到临时目录、用 `<hook>` 替换 `secret-guard.sh`，在副本里以 `taskset -c 0,1 nice -n 19` 跑套件；`SC_BASH`、`SG_W10_ONLY`、`SG_W10_LOG` 照传（相对路径先转绝对）；首行记日期、hook 与副本套件的 sha256 前缀、负载，末行记结束负载与套件退出码；头注释写明非 git 副本里 SC-8、SC-9a 不跑、SC-13 的总数随之不同（副本里 SC-13 红）。

过程材料（scratchpad，非交付物）：`t002c/w10-block.sh`、`patch3a.py`、`drive.sh`、`drive2.sh`。

## 2. 编号对照表

直调（helper，由 `SC_BASH` 执行；套件在 `:345` 调用、`:346-:355` 逐行解析，`TIMED` 行走负载门）：

| 编号 | helper 行 | 模式 |
|---|---|---|
| V2-G1 | :73 | 两种 |
| V2-G2-platform:*（21 条） | :77-:106（表） | 两种 |
| V2-G3 / V2-G3b | :110 / :114 | 两种 |
| V2-G4-*（4 条） | :122 | 两种 |
| V2-G5 / G6 / G7 / G8 | :126-:129 | 两种 |
| V2-G11 | :132 | 两种 |
| V2-G12 / G13 | :135 | 两种 |
| V2-G14 至 G18 | :147-:153 | 两种 |
| V11-S5 / S6 / S7 | :157 起 | 两种 |
| V3-G9 / G10 / G12 | :194 / :196 / :199 | relax |
| V4-S1 至 V5-S9（9 条） | :226-:234 | relax |
| V5-S13 / V5-S13b | :235 起 | relax（S13b 加 ps 前提） |
| V4-S11 | :244 | relax |
| V5-S10 / S10b | :255 起 | relax |
| V5-S10c / S10d | :273 起 | relax |
| V5-S14 / V5-S15 / V4-S19 | :288 / :294 / :303 | relax |
| V5-S12 | :313 | relax（加 ps 前提） |
| V4-S16 / S17 / S18 | :329-:331 | relax |
| V6-S20 / V6-S21 | :355 / :356（fbt 定义在其上） | relax（关门臂改） |
| V8-D1 至 D3（6 条）/ V8-D4 / D5 | :370-:375 / :387-:388 | relax |
| V9-C1 至 C3b（8 条）/ V9-C4 | :394-:406 / :409 | relax |
| V10-N* / V7-N*（13 条） | :421-:423 为清单，用例 :434 起 | relax |
| 上面 58 个 relax 编号在 norelax 下 | :470-:475 | SKIP [platform] |

端到端、静态与装置检查（套件 `hooks/tests/secret-guard.test.sh`）：

| 编号 | 套件行 |
|---|---|
| V7-E1 | :363（outcome） |
| V6-E2、V3-E3、V3-E4、V3-E5、V2-E6、V2-E7 | :364-:369（deadline） |
| V2-E8 / V2-E9 | :371（outcome）/ :372（identity） |
| V9-E10 / V9-E11 / V9-E12 | :374 / :375（outcome）/ :376（identity） |
| V7-E13 / E14 / E15 | :378-:380（outcome） |
| V1-E16-*（6 条） | :382（identity 循环） |
| V2-E17 | :384，函数 `sg_w10_e17`（:286） |
| V2-E18 / V5-E19 | :385（identity）/ :388（deadline，TERM 被忽略的包装） |
| V11-S1-above-gate:*（7 条）/ V11-S3 / V11-S4 | :300 / :307 / :313（`sg_w10_static`） |
| V0-H1 / V0-H2 | :356 / :400 |

与 v31 不同的断言，逐条：

1. 全部端到端用例的对照臂：v31 取 59e333c 的基线 hook；套件取同一 hook、环境里设 `WSL_DISTRO_NAME=Ubuntu`（准入门的关门开关）时的输出。断言形式（逐字节相同、墙钟窗口、rc 与文案种类）、期望值、原因标签都不变；细节文字里 `base` 改为 `gate-closed`。
2. `V2-E17-wsl-mark-keeps-baseline`：v31 是逐字节对比；套件按口径 (ii) 改判结局：退出码 2 且文案种类为 `oversize`（尺寸文案），否则 FAIL `[rc]` / `[kind]`。另外，我把 `slow()` 的两个慢宿主信号按单臂照用：rc 124 记 `[timeout12]`、出现时间文案记 `[time-text]`，按计时类处理（第 6 节第 3 条）。
3. `V6-S20`、`V6-S21`（fbt）：对照臂由「基线 hook 文件」改为「同一 hook，在 source 它的子 shell 里 `export WSL_DISTRO_NAME=Ubuntu`」；该子 shell 另设 `_SG_P0=${EPOCHREALTIME:-}`，使关门的原因只有 WSL 标记（不设锚点时准入门也会因「无锚点」关门）。断言 `[4 <mode> 0]` 与 `cmp` 逐字节不变。实测 721 字节、IDENTICAL。
4. `V11-S4-one-rule-loop`：「与基线同数」改为固定判据「hook 里恰好一处 `risky_patterns[@]`」，原因标签 `[count]` 不变。
5. `V12-C1-hook-comments`：不移植。
6. helper 的 MISSING、SETUP 在套件里记 FAIL，细节分别带 `[missing]`、`[setup]`。`SG_W10_LOG` 只有 PASS / FAIL / SKIP 三种；缺函数的坏 hook 不能记 SKIP。若 run-mutants.sh 解析这份日志，指定用例为 `FAIL [missing]` 会落到 WRONG-REASON（不算抓住），与 v31 记 SETUP 的结论同向。
7. relax 专属的 58 个直调编号：v31 在 norelax 下不输出，V0-H2 的期望清单随模式变；套件里 helper 在 norelax 下逐个输出 `SKIP <id> [platform] …`，V0-H2 用同一份 136 个编号的清单（过滤轮按 `SG_W10_ONLY` 过滤）。
8. 平台前提：`ps` 不存在时 V5-S13b、V5-S12 记 SKIP [platform]（否则残留进程数恒为 0，成了假绿）；`timeout` 不存在时端到端 24 个记 SKIP [platform]；`/proc/loadavg` 读不到时计时批不判（SKIP [load]）；`/proc` 缺失时内核串读不到，按准入门判据为 norelax，relax 专属编号记 SKIP [platform]。本机这些分支都没走到。
9. 负载门槛固定为 2（INV-7），没有 v31 的 `SC_LOAD_MAX`；套件内部不加 taskset / nice，由调用方加（run-suite.sh 加）。
10. V0-H1、V0-H2 在过滤轮里也总是跑（同 v31），所以过滤轮的总数 = 匹配的编号数 + 2。

输入生成：`sg_w10_shape` 生成的 15 个形状与 `shapes.py` 的输出逐字节相同（`t002c/shapes/{py,sh}`，`diff -rq` 无差异）；凭据形路径在运行时拼装。`grep -c python3` 改前改后都是 40。

## 3. 各轮结果与首尾负载

整轮（worktree，`SC_BASH=<bash> SG_W10_LOG=… taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh`，`t002c/full-<bash>.{txt,log}`）：

| SC_BASH | 整轮开跑负载 | W10 批开始 → 结束负载 | W10 计时批 | 总数 | PASS / FAIL / SKIP | 旧用例的红 | SC-13 | 移植用例 |
|---|---|---|---|---|---|---|---|---|
| /usr/bin/bash 5.2.15 | 0.91 | 3.14 → 2.04 | SKIP [load] | 961 | 926 / 6 / 29 | 21ab 21ac 21ag 21aj 21al 21ao | 绿 | 107 PASS + 29 SKIP [load]，0 FAIL |
| 5.0.18 | 0.91 | 4.42 → 3.33 | SKIP [load] | 961 | 926 / 6 / 29 | 同上 | 绿 | 同上 |
| 5.1.16 | 2.33（等 10 分钟未降到 1.0） | 7.59 → 7.07 | SKIP [load] | 961 | 926 / 6 / 29 | 同上 | 绿 | 同上 |
| 5.3.20 | 2.62（同上） | 2.44 → 2.35 | SKIP [load] | 961 | 926 / 6 / 29 | 同上 | 绿 | 同上 |
| 3.2.57 | 0.88 | 2.10 → 2.28 | SKIP [load]（norelax 下没有计时结果） | 961 | 897 / 6 / 58 | 同上 | 绿 | 78 PASS + 58 SKIP [platform] |

另有第一版驱动的 3 次 5.2 整轮（`round-bash-5.2.*` 是第 3 次）：同为 961 / FAIL 6 / 29 SKIP [load]；第 2 次整轮开跑 1.71，W10 批开始 2.58。

W10-only 轮（同一 worktree，`SG_W10_ONLY=.`，`t002c/w10-<bash>.{txt,log}`）：

| SC_BASH | 开始 → 结束负载 | 计时批 | 结果 |
|---|---|---|---|
| 5.2.15 | 1.43 → 1.03 | judged | 136 PASS |
| 5.0.18 | 1.03 → 0.81 | judged | 136 PASS |
| 5.1.16 | 0.81 → 1.40 | judged | 136 PASS |
| 5.3.20 | 1.40 → 1.34 | judged | 136 PASS |
| 3.2.57 | 1.34 → 1.48 | judged | 78 PASS + 58 SKIP [platform] |

均为第一次尝试，0 FAIL，没有 SKIP [load] / [void] / [inconclusive]。开发期另有两次全量过滤轮（`filt-bash-{3.2.57,5.2}.*`）结果相同。

## 4. 等价核对

- 同一 bash（/usr/bin/bash 5.2.15）：`v31/sc-cases.sh` 对实现（页眉：hook af4658b6f935、base e83c5e30f2cc、sc-cases e537079f6738、sc-direct e97513c59e58、shim 637c52c10bbf），计时批 judged（1.48 → 1.07），PASS 137 / FAIL 0（`t002c/equiv-sc-cases.txt`）；套件一侧取 W10-only 5.2 轮（judged，136 PASS）。
- 按编号对齐（`t002c/equiv-diff.txt`）：共有 136 个编号，状态逐条相同。不同只有 1 行：`only-v31 V12-C1-hook-comments PASS`，即任务书允许的不移植。
- 状态相同、但断言或对照臂按任务书改过的：V2-E17、V11-S4、V6-S20 / S21，以及全部端到端用例的对照臂（见第 2 节）。细节文字里 `base` 改为 `gate-closed`，原因标签未变。
- 逐条对齐只在 5.2 上做（任务书要求「同一 bash」）。

## 5. 抽查能红

坏实现由 `python3 v31/mutants.py <实现> t002c/mut` 从实现构造；经 `run-suite.sh <worktree 的 aria> <坏实现> t002c/copies` 加 `SG_W10_ONLY=<指定用例>` 跑（副本非 git 检出）。负载 0.92–0.93，计时批 judged。

| BI（hook 前缀） | 指定用例 | 结果与细节 | reasons.tsv 的标签 |
|---|---|---|---|
| BI-24（3a2b5da90f6a） | V2-G12-segment-trigger-asks-gate | FAIL：status/text [4 none]（want [2 oversize], never 4）`[status] [kind]` | `\[status\]`，抓住 |
| BI-7（7fb5c9bb45e3） | V6-E2-deadline-fallback-bytes | FAIL：hook rc=2 time 3.02s，gate-closed rc=2 oversize，sed-stall=job `[time-text]` | `\[time-text\]\|\[bytes\]`，抓住 |
| BI-11（2ba0bfed3d0c） | V10-N3-environ-big-judge、V11-S4-one-rule-loop | FAIL：rc=2 longline（want 0 none）`[status] [kind]`；risky_patterns 2 处（want 1）`[count]` | `\[status\]`、`\[count\]`，抓住 |

对照：这 4 个指定用例在实现上经 run-suite.sh 全 PASS（加 V0-H1、V0-H2 共 6 / 6，`t002c/ctl-impl.*`）。

## 6. 未做、拿不准、与规格字面不同的项

1. **【需主控裁定】整轮里的计时批判不过。** `sg_w10_cases` 在 SC-13 之前运行，负载在本批开始时读（照 sc-cases.sh 在本批开头读）。此前约 5 分钟的旧用例在 2 核上运行，把一分钟负载推高：5.2 整轮开跑 0.91，到 W10 批开始已是 3.14。本机是共享宿主，期间背景负载 0.9–2.6，一度到 7；在这台机器上，整轮几乎不可能在 W10 批开始时低于 2。「开跑与结束各读一次负载」有两种读法：(A) 现做法，在本批开始读，与 v31 字面一致（v31 的批开始就是整轮开跑），整轮要判过需要宿主背景负载很低；(B) 在整个套件开跑时读，第一读数干净，但结束读数仍含套件自身的负载（第一版驱动的 5.2 第 1 次：开跑 0.93，结束 2.19，照样作废）。两种读法下本机整轮都难判过。我没有改负载门的位置或口径，因为两种改法都会改规格，(B) 还相当于放宽。现有证据是：同一 worktree 的 W10-only 轮，5 个 bash 全部判过、全绿；整轮给出旧用例、SC-13、总数，以及移植用例里不计时的部分。可选做法：认可「整轮 + W10-only 轮」的组合；或改规格（把 W10 批移到套件最前，或把读数改到套件开跑并写明结束读数）；或等低负载窗口重跑整轮（INV-7：连续 3 次取不到低负载窗口，附读数上报 owner）。本段 5.2 整轮共跑 4 次，其余 bash 各 1 次，W10 批开始负载全部 ≥ 2.10。
2. **Coverage 的 967（有 zsh）没有实测。** 本机无 zsh，实测的是 961（五轮都是 961，SC-13 绿）；967 由旧值 831 加 136 推出。
3. **V2-E17 的慢宿主处理是我类推的，规格没写。** 单臂用例里 rc 124 或时间文案按计时类处理（低负载判 FAIL，高负载 SKIP [load]）。若主控要求这一条一律按 hard 判，需要改 `sg_w10_e17`。
4. **「python3 只给 SC-20 用」在改动前就不完全成立。** 我加的部分不用 python3（`grep -c python3` 改前改后都是 40）。但 HEAD 版 `:1623` 的 SC-19 census 也调用 python3（`corpus_census.py`），属于既有的不符。不在本段范围，没改，请 3b 或主控处理。
5. **run-suite.sh 首行的「两个 sha256 前缀」**，我取的是被测 hook 与副本里的套件。若指的是别的两个（例如 hook 与 helper），改一行即可。
6. **垫片原样复制，头注释没改。** 它仍写「Test shim for sc-cases.sh (installed as shim/jq and shim/sed)」。任务书要求复制；注释同步属于 3b。
7. **字符数与字节数差异的用例**（design 第 103 行：显式 `LC_ALL=C.UTF-8` 并断言 charmap）：移植的 136 个编号里没有这类用例（v31 的两份脚本都用 ASCII 填充，V11-S6 是整行字符串比较），所以没加 locale 断言，也没加对应的 SKIP 原因。
8. Summary 的 `total` 现在含 SKIP（`PASS: n / total` 的分母变了），与 SC-13 的计数一致。
9. 驱动切换：第一版驱动按「每个 bash 的整轮最多重试 3 次，直到判过」写。5.2 两次都是 SKIP [load] 后，我按记下的 PID 只停了驱动本身，等它正在跑的那一轮自然结束（没杀子进程），然后改用 drive2：W10-only 轮、等价核对、每个 bash 一次整轮。
10. 不在本段：坏实现全集、环境错误、基线红集在套件上的复跑（3c）；6 组既有用例、套件注释与标题、commentsync 套件一侧（3b）。

## 7. 复现与文件

- 整轮：`cd wt217/aria && SC_BASH=<bash> SG_W10_LOG=<file> taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh`；W10-only 轮再加 `SG_W10_ONLY=.`。
- 副本：`SC_BASH=<bash> SG_W10_ONLY=<正则> SG_W10_LOG=<file> bash v31/run-suite.sh <aria 检出> <hook> [<工作目录>]`。
- `t002c/` 下的输出：`base-suite.txt`（基线轮）、`smoke1.*`、`filt-bash-{3.2.57,5.2}.*`、`ctl-impl.*`、`mut-BI-{24,7,11}.*`、`mut/`（mutants.py 的产物与 reasons.tsv）、`round-bash-5.2.*`（第一版驱动）、`w10-bash-*.{txt,log}`、`equiv-sc-cases.txt`、`equiv-diff.txt`、`full-bash-*.{txt,log}`、`drive.log`（全部运行的时间与负载）、`collect.txt`、`shapes/{py,sh}`。
