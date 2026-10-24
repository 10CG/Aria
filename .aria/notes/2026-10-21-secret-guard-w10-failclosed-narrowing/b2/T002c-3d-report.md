# TASK-002 第三步 3d 报告：run-mutants.sh 套件模式；坏实现、扰动、两种环境错误与基线红集在套件上复跑（10CG/aria-plugin#217）

执笔席：3d 新实例。任务书 `r217impl/BRIEF-T002c-3d.md`。输出目录 `r217impl/t002g/`。只改了主仓 `v31/run-mutants.sh`；套件、helper、垫片、hook 未动；未 commit。

## 0. 预期（先写后测；本节在任何实跑之前写下，之后不改，实测对照写在后面各节）

被测 hook 一律取 worktree（aria `df2d629`）的 `hooks/secret-guard.sh`，sha256 前缀 `af4658b6f935`，与第二步 `mut-summary.txt` 页眉里的 hook 相同，所以 mutants.py 造出的 57 个坏实现与 7 个扰动和第二步逐字节相同。

### 0.1 第 0 步（任务书要求的两条）

- (a) v31 模式（不设新变量）`MUT_ONLY='BI-8'`：BI-8 判 **CAUGHT**，指定用例 `V9-E12-vmax-unchanged=red`（reasons.tsv 列 `[bytes]`；v31 的对照臂是真基线 59e333c，BI-8 把 `_SGV_VMAX` 4096 改 8192 后被测臂 rc 0、基线 rc 2，字节不同）；汇总 `1 caught … (of 1)`；MUT_ONLY 不含 P-*，扰动轮 0 条；退出码 0。
- (b) 经 `run-suite.sh` 用 `SG_W10_ONLY=^(V9-E12-vmax-unchanged)$` 跑 BI-8：日志里 V9-E12 为 `FAIL … gate-closed arm rc=0 none, reference (59e333c) rc=2 vmax [reference]`（关门臂也是被测 hook，两臂都 rc 0、字节相同，靠参照核对抓住）；恒在的 V0-H1、V0-H2 为 PASS；套件退出码 1；负载低于 2 时计时批 judged。

### 0.2 改前改后（不设 MUT_SUITE）`MUT_ONLY='BI-8|BI-24'`

两份输出除首行时间、负载读数与各行 `load start … end …` 的读数外逐字相同；BI-8、BI-24 都 CAUGHT（同 mut-summary）；退出码都是 0。

### 0.3 套件模式全量（PATH 上的 bash，低负载）

57 个坏实现全部 CAUGHT；P-0 GREEN（过滤轮全 PASS、SKIP 0，PATH 上的 bash 放宽生效，不应有 [platform]）；其余 6 个扰动 CAUGHT。以 `[reference]` 抓住的至少有 BI-8（V9-E12）；改动落在两臂共用的代码或常量、且指定用例走关门臂的坏实现，也会报 `[reference]`，逐条见第 3 节。负载若升到 2 以上，端到端指定用例可能 NOT-JUDGED，单独重跑。

### 0.4 两种环境错误（`SG_W10_ONLY=.` 过滤轮，hook = 实现）

- e1b：`SC_BASH` 指向**父目录存在**的不存在文件：V0-H1 为 `FAIL [setup] SC_BASH does not run (…) [harness]`，移植用例不跑；FAIL 1–2 条；退出码 1。
- e1：`SC_BASH` 指向**父目录也不存在**的文件（第二步 env/e1.txt 用的就是这种）：按代码读的预测 —— `run-suite.sh` 第 18 行 `readlink -f` 对父目录不存在的路径输出空串，`SC_BASH` 被导出为空；套件第 364 行 `${SC_BASH:-$(command -v bash)}` 把空串当未设，回落到 PATH 上的 bash，整轮照常跑过、退出码 0，首行记 `SC_BASH bash on PATH` —— 环境错误被静默吞掉。若实测如此，属 `run-suite.sh` 的缺陷（不在本段可改范围），只报告。
- e2：helper 副本第一条可执行语句前加 `exit 7`：V0-H1 FAIL（末行不是哨兵、exit 7、[harness]）；V0-H2 FAIL（helper 的直调编号全缺）；端到端与静态用例照常 PASS；FAIL = 2；退出码 1。

### 0.5 基线红集（59e333c，`SG_W10_ONLY=.`，PATH 上的 bash）

先断言 sha256 前缀 `e83c5e30f2cc`。套件 136 行（v31 137 行减 V12-C1）。v31 的 74 个 MISSING 全部对应套件的 `FAIL [missing]`；v31 其余 38 个 FAIL 在套件上仍 FAIL；24 个 PASS 大体仍 PASS。预期的不同来源：口径 (ii) 对基线 hook 不产生差异（基线不认 WSL 标记，关门臂与被测臂同一字节，v31 里两臂也都是基线）；参照核对对基线恒成立（基线就是参照），`[reference]` 预期 0 条；V2-E17 在套件里改判结局（退出码 2 与尺寸文案），基线给什么以实测为准；计数上套件把 MISSING 并进 FAIL，所以套件 FAIL ≈ 38 + 74 = 112、PASS ≈ 24。

（以下各节为实测，写在实跑之后。第 0 节的预期全部成立，唯一偏差是 0.4 的 e1 —— 它照预期被静默吞掉，见 5.1。）

## 1. 改了什么

文件：`/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-mutants.sh`，66 → 104 行。改前副本 `t002g/run-mutants.orig.sh`，diff `t002g/run-mutants.diff`（78 行）。主仓 `git status --short` 只有这一个文件；worktree 仍在 `df2d629`、工作区干净；未 commit。

- **头注释加 16 行**，写明套件模式：`MUT_SUITE=<aria 检出>` 时，每个坏实现与扰动改经 `run-suite.sh <检出> <坏实现> <work dir>` 跑过滤轮，`SG_W10_ONLY` 取指定用例（P-0 与 `MUT_SCOPE=full` 取 `.`），`SG_W10_LOG` 取 `$W/<ID>.log`，判定读这份逐条结果；判定逻辑照旧，只有三处不同：
  1. `[reference]`：走关门臂的指定用例（`REFIDS`：套件 `sg_w10_ref` 表的 23 个编号加 helper `fbref` 的 V6-S20、V6-S21，以 aria df2d629 为准）明细带 `[reference]` 时，不论 reasons.tsv 列什么，也算按所列原因变红，状态记作 `red[reference]`。两点理由照任务书写进注释：(1) 套件不读 59e333c，「与基线的字节不同」由「与关门臂不同」加「关门臂给出基线的已知结局」两条合起来表达；(2) 套件先核参照、对不上就提前返回，不再做原来的判定，所以坏实现只要让关门臂偏离基线的已知结局，报出来的就是 `[reference]`，这本身就是真问题（门关时与 59e333c 不同）。注释也写了计划原先只在列 `[bytes]` 的用例上另认，主控 2026-10-24 放宽到所有走关门臂的指定用例。
  2. `[missing]`：套件把 MISSING（helper 的，以及套件自己检查函数是否定义的那处）记作 `FAIL [missing]`，把 helper 的 SETUP 记作 `FAIL [setup]`。它们按普通 FAIL 判，对不上 reasons.tsv 就落到 WRONG-REASON，和 v31 的 SETUP 一样不算抓住。
  3. P-0：所有移植用例都不许 FAIL，SKIP 只许 `[platform]`。有 FAIL 记 RED；有其他 SKIP 记 NOT-JUDGED（须重跑）。两种都计入 not as expected，退出码 1。
- **代码**：
  - 新增 `SUITE`、`RES`（判定读 `.log` 还是 `.txt`）与 `REFIDS` 三个变量。
  - 套件模式的首行另记检出路径，以及 secret-guard.test.sh、helper、run-suite.sh 的 sha256 前缀；v31 模式的首行原样保留。
  - `MUT_SUITE` 下找不到 `hooks/tests/secret-guard.test.sh` 时退出 3。
  - `runsc` 的套件分支跑前先删旧 `.log`；跑完若没有 `.log` 就建一个空文件，于是指定用例全记 absent，判 SETUP，不会读到旧结果。
  - `verdict` 的 FAIL 分支加 `ref`（只在套件模式生效）。
  - 读结果文件处一律改为 `$W/$id$RES`。
  - P-0 分支加 `skipx`（只在套件模式生效）。
- **不设 `MUT_SUITE` 时逐字相同**：改前、改后各跑一次 `MUT_ONLY='BI-8|BI-24'`（`t002g/before.txt`、`t002g/after.txt`），时间戳与负载三元组换成占位后 `diff` 为空（`before-after.diff` 0 字节）。两次退出码都是 0，BI-8、BI-24 都 CAUGHT。
- **REFIDS 与表核对**：从套件 `sg_w10_ref()` 与 helper `fbref()` 的 case 行抽出 25 个编号，与脚本里的 25 个逐个相同（`drv.sh refcheck`）。

## 2. 第 0 步：预期与实测

- (a) 预期 CAUGHT，实测 CAUGHT：`BI-8 CAUGHT VMAX relaxed too | seats: author | V9-E12-vmax-unchanged=red | load start 1.18 1.31 1.35 end 1.25 1.32 1.36 | timing batch: judged`，汇总 `1 caught … (of 1)`，退出码 0。BI-8.sh 的 sha256 前缀 `ff9f7a43eb7e`，与 3c 报告相同。
- (b) 预期 `FAIL … [reference]`，实测 `FAIL V9-E12-vmax-unchanged hook rc=0 none 0.64s | gate-closed rc=0 none 0.67s | stderr IDENTICAL | gate-closed arm rc=0 none, reference (59e333c) rc=2 vmax [reference]`。V0-H1、V0-H2 PASS，套件退出码 1，计时批 judged（负载 1.20 → 1.20）。与预期全符。

## 3. 坏实现逐个的判定（套件模式）与 v31 的对照

首跑记录在 `t002g/all.txt`：16:10:05–16:13:34 UTC，hook `af4658b6f935`，套件 `60f7f95525cd`，helper `213d01379695`，run-suite.sh `7584c219c4ba`，PATH 上的 bash 5.2。汇总 `# 57 caught, 0 missed, 0 wrong reason, 0 not judged, 0 setup (of 57)`。逐个结果见附录 A；附录 A 由 `t002g/gen-table.py` 从 all.txt、mut-summary.txt 与两份重跑生成，没有手抄。

与 mut-summary.txt 逐个对照（判定，以及每个指定用例的状态）：57 个坏实现的判定全部相同。指定用例的状态只有一处不同：

- **BI-8**（mutants.py:52，`_SGV_VMAX=4096` 改 `8192`，"VMAX relaxed too"）。v31 为 `V9-E12-vmax-unchanged=red`，reasons.tsv 列的原因是 `\[bytes\]`；套件为 `red[reference]`。
  - 关门臂为什么偏离：v31 的对照臂是真基线 59e333c，它对 V9-E12 的输入给 rc 2 和 vmax 文案，BI-8 给 rc 0，字节不同，于是报 `[bytes]`。
  - 套件的关门臂是同一个 BI-8 加上 `WSL_DISTRO_NAME`（准入门关）。`_SGV_VMAX` 是两臂共用的常量，不随门的开关变化，所以关门臂同样放行（rc 0 none），两臂字节相同。只看逐字节比对的话这里会 PASS，这就是口径 (ii) 的漏洞。
  - 参照核对查 `sg_w10_ref`，表中 V9-E12 为 `2 vmax`，实际得到 `0 none`，于是记 `FAIL [reference]` 并提前返回。`[reference]` 说的正是「门关时与 59e333c 不同」，是真问题。

以 `[reference]` 抓住的只有 BI-8 一个。指定用例里有走关门臂用例的坏实现共 16 个：BI-2、4、5、6、7、8、10、12、13、14、16、17、18、42、43、45（描述与状态见附录 B）。其余 15 个的明细里都没有 `[reference]`，也就是关门臂对上了 59e333c 的已知结局，参照核对通过后进入原判定，并按 reasons.tsv 所列原因变红。这是数据上的结论，我没有逐个读这 15 个的改动。

`[missing]` 没有出现在任何指定用例上：57 + 6 个的指定用例状态都与 v31 相同，没有一个是 WRONG-REASON。

## 4. 扰动的结果

- **P-0**（`_SGV_GMAX=8190, _SGV_LMAX=8200`，跑全部移植用例）：
  - 首跑：NOT-JUDGED。它排在 63 个之后，起跑时一分钟负载 2.09，计时批为 SKIP [load]：29 条计时类用例 SKIP [load]，107 PASS，0 FAIL，套件退出码 0。
  - 低负载单独重跑（`MUT_ONLY='P-0'`，`t002g/p0-rerun.txt`，负载 1.03 1.27 1.32 → 0.86 1.18 1.29，计时批 judged）：GREEN，136 PASS、0 FAIL、0 SKIP。
  - 两次读数都列在附录 A。
- **其余 6 个**（P-M29、P-L-sentinel、P-L-text、P-G-limit、P-G-text-whole、P-G-text-segment）：首跑全部 CAUGHT，指定用例状态与 mut-summary 相同。
- **首跑里的负载爬升**：脚本逐个连跑，中间没有间隔。约 40 个（BI-38 是第 41 个）之后，一分钟负载越过 2。
  - 首跑中计时批未判的有：20 个 SKIP [load]（BI-39–43、BI-46–54 共 14 个，加 6 个 P-*），另有 P-0，以及 1 个 void（BI-38：起跑 1.45，收尾时 ≥ 2）。
  - 这 21 个（不含 P-0）的判定仍是 CAUGHT：计时类检查在未判过的批里记 SKIP，不会给出 FAIL，所以 CAUGHT 不受负载影响。
  - 为稳妥起见，仍在低负载下把这 21 个重跑了一遍（`t002g/rerun-load.txt`，16:20:58 起，负载 0.77 1.10 1.25 → 1.15 1.16 1.27）：21 个计时批全部 judged，判定与指定用例状态和首跑逐个相同。

## 5. 环境错误与基线红集

### 5.1 两种环境错误（`SG_W10_ONLY=.`，hook = 实现，PATH 上的 bash；输出在 `t002g/env/`）

| 情形 | 做法 | 退出码 | FAIL 数 | V0-H1 | V0-H2 | 负载 起 → 止 |
|---|---|---|---|---|---|---|
| e1b | `SC_BASH=t002g/env/bash-not-here`（父目录存在） | 1 | 135：134 条移植用例全为 `FAIL [setup] SC_BASH does not run (…)`，加 V0-H1 | `FAIL [setup] SC_BASH does not run (…/bash-not-here); [harness]` | `PASS all 134 expected case ids reported once (mode norelax; …)` | 1.20 → 1.18 |
| e2 | helper 副本在第 23 行插入 `exit 7`，位于第一条可执行语句 `H=$1; MODE=$2` 之前（第 1 行是 shebang，2–22 行是注释和空行） | 1 | 2（V0-H1、V0-H2）；另有 33 PASS（端到端与静态用例） | `FAIL … (relax): last line [] (want END sc-direct), exit 7 (want 0); stderr:  [harness]` | `FAIL expected 134 ids, reported 33; missing: [V2-G1-gate …]`（缺 101 个直调编号）`[harness]` | 1.18 → 1.12 |
| **e1** | `SC_BASH=t002g/env/nope/bash`（父目录也不存在；第二步 env/e1.txt 用的就是这种） | **0** | **0**：136 PASS，首行记 `SC_BASH bash on PATH` | PASS | PASS（mode relax） | 1.12 → 1.84 |
| e1d（对照） | 同 e1 的 SC_BASH，但不经 run-suite.sh，直接在 hooks 副本里跑套件 | 1 | 135 | `FAIL [setup] SC_BASH does not run (…/nope/bash); [harness]` | PASS | 0.77 → 0.77 |

v31 的对照（第二步 `env/`）：e1、e1b 下 sc-cases.sh 都报 `SETUP: SC_BASH does not run`；e2 下 PASS 10、FAIL 2（V0-H1、V0-H2）。

**发现：run-suite.sh 有缺陷（fail-open），按纪律未改。**

- 位置：run-suite.sh 第 18 行 `[[ -n "${SC_BASH:-}" ]] && export SC_BASH="$(readlink -f "$SC_BASH")"`。
- 原因：GNU `readlink -f` 要求除最后一段外各段路径都存在。父目录不存在时它输出空串并退出 1（实测 `readlink -f t002g/env/nope/bash` 输出为空，rc=1）。
- 后果：SC_BASH 被导出为空串。套件第 364 行 `${SC_BASH:-$(command -v bash)}` 把空串当作未设，回落到 PATH 上的 bash，于是整轮全过、退出码 0，环境错误被静默吞掉。
- 定位：e1d 证明套件本身对同一个值会正确报 FAIL [setup]，缺陷只在 run-suite.sh 的路径规范化。
- 同形状的兄弟：第 19 行对 SG_W10_LOG 做同样的处理，父目录不存在时日志被静默丢弃。run-mutants.sh 的套件模式不受影响：`$W` 恒存在，而且没有日志时指定用例全为 absent，判 SETUP，方向是 fail-closed。
- 修法建议（由主控定）：规范化失败时保留原值，例如 `x=$(readlink -f "$SC_BASH") || x=$SC_BASH`，或改用 `readlink -m`。
- 对验收的影响：验收要求「两种环境错误下，套件报 SETUP 或 FAIL、退出码非 0」。e1b 与 e2 成立；e1 这种写法经 run-suite.sh 不成立。

### 5.2 基线红集（`t002g/base/`）

INV-9：基线取 `git -C <worktree> show 59e333c:hooks/secret-guard.sh`，sha256 前缀 `e83c5e30f2cc`，断言通过。经 run-suite.sh 跑 `SG_W10_ONLY=.`，PATH 上的 bash 5.2，负载 1.12 → 1.73，计时批 judged，套件退出码 1。

| | v31 `base-5.2.15.txt` | 套件 `base.log` |
|---|---|---|
| PASS | 24 | 24 |
| FAIL | 39（含 V12-C1） | 112（其中 `[missing]` 74） |
| MISSING | 74 | —（记作 FAIL [missing]） |
| 合计 | 137 | 136 |
| `[reference]` | — | 0 |
| 计时批 | judged | judged |

按编号对齐，结果在 `base/align.txt`，用 LC_ALL=C 排序后 join。第一次用默认 locale 排序时 join 报 not sorted，那份结果作废并已重做。

- 136 个共有编号：状态全部对应。v31 的 MISSING 对应套件的 FAIL，套件明细的末标签都是 `[missing]`（74/74）。38 对 FAIL/FAIL 的末标签逐个相同，24 个 PASS 两边都是 PASS。
- 只在 v31 里有：V12-C1-hook-comments（FAIL [text]），不移植。
- 其余的不同：没有。预期里列的几种来源为什么都没有产生差异：
  - 口径 (ii)：套件的逐字节比对臂是同一个 hook 加 WSL_DISTRO_NAME。59e333c 不认 WSL 标记，所以关门臂与被测臂字节相同；v31 里两臂也都是 59e333c，结论相同。V2-E17 在套件里改判结局：v31 为 `PASS … hook rc=2 oversize | base rc=2 oversize | stderr IDENTICAL`，套件为 `PASS … rc=2 oversize (want rc=2 text=oversize …)`，两边都 PASS。
  - 参照核对：参照表就是在 59e333c 上实测出来的，关门臂（就是 59e333c 本身）必然对上，所以 `[reference]` 为 0。
  - 计数方式：套件汇总把 MISSING 并进 FAIL（112 = 38 + 74），v31 分列（FAIL 39 含 V12-C1，MISSING 74）。按编号逐条看没有差别。
- 原因表与 `[missing]` 的交叉核对：reasons.tsv 共 86 行，逐行取该用例在 59e333c 上的 `FAIL [missing]` 明细去匹配所列正则，没有一行匹配，也没有空正则。所以在现有原因表下，`FAIL [missing]` 一律落到 WRONG-REASON，不会被算作抓住。

## 6. 各轮首尾负载（一分钟 / 五分钟 / 十五分钟）

| 轮 | 时间 (UTC) | 起 | 止 | 计时批 |
|---|---|---|---|---|
| 0(a) v31 BI-8 | 16:07:47 | 1.18 1.31 1.35 | 1.25 1.32 1.36 | judged |
| 0(b) 套件 BI-8 / V9-E12 | 16:08 | 1.20 1.31 1.35 | 1.20 1.31 1.35 | judged |
| 改前 `BI-8\|BI-24` | 16:08:02 | 1.20 1.31 1.35 | 1.27 1.33 1.36 | judged ×2 |
| 改后 `BI-8\|BI-24` | 16:09 | 0.68 1.11 1.28 | 0.71 1.11 1.27 | judged ×2 |
| 冒烟：套件模式 `BI-1\|BI-8\|BI-24` | 16:09:54 | 0.71 1.11 1.27 | 0.73 1.10 1.27 | judged ×3 |
| 全量套件模式 | 16:10:05–16:13:34 | 1.07 1.17 1.29 | 2.08 1.56 1.41 | 42 judged、21 SKIP [load]（含 P-0）、1 void（BI-38） |
| e1 / e1b / e2 | 16:13–16:17 | 1.12 / 1.20 / 1.18 | 1.84 / 1.18 / 1.12 | — |
| 基线红集 | 16:13–16:17 | 1.12 1.33 1.35 | 1.73 1.46 1.39 | judged |
| P-0 重跑 | 16:19:09 | 1.03 1.27 1.32 | 0.86 1.18 1.29 | judged |
| e1d（对照） | 16:20 | 0.77 1.10 1.25 | 0.77 1.10 1.25 | judged |
| 21 个计时批未判的重跑 | 16:20:58 | 0.77 1.10 1.25 | 1.15 1.16 1.27 | 21 judged |

每轮重实验开跑前都等到一分钟负载 ≤ 1.2（`drv.sh` 的 waitload：等过之后显式 `return 0`，30 分钟上限，本次最长只等了 110 s）。所有命令都加了 `taskset -c 0,1 nice -n 19`，同一时刻只跑一个重实验。

## 7. 未做或拿不准的项

1. **run-suite.sh 的 e1 缺陷**（5.1）：未改，因为本段只许改 run-mutants.sh。验收的环境错误一条在 e1 这种写法下不成立，修不修、怎么修由主控定。
2. **REFIDS 是硬写的**（25 个，以 df2d629 为准，本次已与表核对相同）。3e 或以后若改了 `sg_w10_ref` / `fbref`，REFIDS 要同步。
   - 漏列一个编号：该编号的 `[reference]` 会落到 WRONG-REASON，偏严，方向是 fail-closed。
   - 多列一个编号：只有当套件在那里仍会报 `[reference]` 时才会多认。
   - 另一个做法是运行时从检出里解析这张表，我没有采用，由主控定。
3. **P-0「其他 SKIP」的判定词**：任务书只写了「须无 FAIL（SKIP 只许 [platform]）」，没有给判定词。我用 NOT-JUDGED（仿照 BI 的 SKIP 记法），它与 RED 一样计入 not as expected，退出码 1。请主控确认。
4. **全量连跑会推高负载**：在这台共享 4 核机器上，连跑约 40 个（BI-38 是第 41 个）套件过滤轮就会让一分钟负载越过 2，排在最后、耗时最长的 P-0 在全量轮里大概率是 NOT-JUDGED。可以把 P-0 单独跑，或者让脚本在两次运行之间留间隔。任务书没有要求，我没有做。
5. 套件模式下，P-0 那一行里的摘要是 `$W/P-0.txt` 的末行（run-suite.sh 的收尾行：负载与套件退出码），不是 v31 的 totals 行，只影响显示。
6. 附录 A 的「与 v31 同」比的是判定词，以及每个指定用例的 `id=状态`。mut-summary 对已匹配的用例只记 `red`，不记匹配到的明细，所以「原因相同」的意思是两边都匹配了 reasons.tsv 的同一条正则，不是明细逐字节相同。
7. 草稿脚本 `t002g/drv.sh`（驱动）与 `t002g/gen-table.py`（生成附录 A）只在 scratch 里，不进任何仓库。

## 附录 A：逐个判定（gen-table.py 生成；首跑 all.txt，重跑 rerun-load.txt / p0-rerun.txt，v31 = mut-summary.txt）

| 编号 | v31 判定 (mut-summary) | 套件首跑判定 | 首跑计时批 (起始一分钟负载) | 低负载重跑 (计时批, 起始负载) | 指定用例 = 套件首跑状态 (\* = 走关门臂) | 与 v31 |
|---|---|---|---|---|---|---|
| BI-1 | CAUGHT | CAUGHT | judged (1.07) | — | `V4-S6-spoofed-tail-0`=red | 同 |
| BI-2 | CAUGHT | CAUGHT | judged (1.07) | — | `V5-S5-pipe-holder`=red `V6-E2-deadline-fallback-bytes`\*=red | 同 |
| BI-3 | CAUGHT | CAUGHT | judged (0.99) | — | `V5-S10c-dead-timer-no-judgement`=red `V5-S10d-no-judgement-with-dead-timer`=red | 同 |
| BI-4 | CAUGHT | CAUGHT | judged (0.99) | — | `V6-E2-deadline-fallback-bytes`\*=red | 同 |
| BI-5 | CAUGHT | CAUGHT | judged (0.99) | — | `V2-G4-extension-file-with-entry`=red `V2-E9-extension-project`\*=red | 同 |
| BI-6 | CAUGHT | CAUGHT | judged (0.99) | — | `V2-G3-gate-calls-platform`=red `V2-G3b-gate-uses-build-facts`=red `V2-E8-ostype-from-environment-ignored`\*=red | 同 |
| BI-7 | CAUGHT | CAUGHT | judged (0.99) | — | `V6-E2-deadline-fallback-bytes`\*=red | 同 |
| BI-8 | CAUGHT | CAUGHT | judged (1.07) | — | `V9-E12-vmax-unchanged`\*=red[reference] | 判定同；原因由 [reference] 认定 |
| BI-9 | CAUGHT | CAUGHT | judged (1.07) | — | `V8-D3-growth-8193-plain`=red `V8-D3-growth-8193-braced`=red | 同 |
| BI-10 | CAUGHT | CAUGHT | judged (1.07) | — | `V7-E14-long-line-from-expansion`\*=red | 同 |
| BI-11 | CAUGHT | CAUGHT | judged (1.15) | — | `V10-N3-environ-big-judge`=red `V11-S4-one-rule-loop`=red | 同 |
| BI-12 | CAUGHT | CAUGHT | judged (1.15) | — | `V7-N5-read-big-judge-short-lines`=red `V7-E13-multiline-copy-normal-text`\*=red | 同 |
| BI-13 | CAUGHT | CAUGHT | judged (1.15) | — | `V3-E3-anchor-at-hook-start`\*=red | 同 |
| BI-14 | CAUGHT | CAUGHT | judged (1.05) | — | `V3-G10-cap-3`=red `V3-E4-cap-3-at-budget-4`\*=red | 同 |
| BI-15 | CAUGHT | CAUGHT | judged (0.97) | — | `V5-S9-child-left-behind`=red `V5-S13b-nothing-outlives-the-run`=red | 同 |
| BI-16 | CAUGHT | CAUGHT | judged (1.05) | — | `V2-G11-flag-not-from-environment`=red `V2-E6-flag-from-environment-ignored`\*=red | 同 |
| BI-17 | CAUGHT | CAUGHT | judged (1.05) | — | `V9-C1-assignments-rerun`=red `V9-C2-references-rerun-c12`=red `V9-E10-count-axis-read-blocked`\*=red | 同 |
| BI-17a | CAUGHT | CAUGHT | judged (1.21) | — | `V9-C1-assignments-rerun`=red | 同 |
| BI-17b | CAUGHT | CAUGHT | judged (1.21) | — | `V9-C3-for-statements-rerun`=red | 同 |
| BI-17c | CAUGHT | CAUGHT | judged (1.21) | — | `V9-C2-references-rerun-c12`=red `V9-C2-references-rerun-cb12`=red | 同 |
| BI-18 | CAUGHT | CAUGHT | judged (1.21) | — | `V9-E11-tmax-in-rerun`\*=red | 同 |
| BI-19 | CAUGHT | CAUGHT | judged (1.27) | — | `V4-S11-bare-zero`=red | 同 |
| BI-20 | CAUGHT | CAUGHT | judged (1.27) | — | `V2-G4-empty-extension-file`=red | 同 |
| BI-21 | CAUGHT | CAUGHT | judged (1.27) | — | `V3-G9-clock-backwards`=red | 同 |
| BI-22 | CAUGHT | CAUGHT | judged (1.27) | — | `V2-G6-no-time-left`=red `V2-G7-no-anchor`=red `V2-G8-budget-0`=red | 同 |
| BI-23 | CAUGHT | CAUGHT | judged (1.25) | — | `V5-S14-failing-sleep-kills-at-once`=red | 同 |
| BI-24 | CAUGHT | CAUGHT | judged (1.29) | — | `V2-G12-segment-trigger-asks-gate`=red | 同 |
| BI-25 | CAUGHT | CAUGHT | judged (1.29) | — | `V2-G12-segment-trigger-asks-gate`=red | 同 |
| BI-26 | CAUGHT | CAUGHT | judged (1.27) | — | `V2-G14-cwd-extension-file-with-entry`=red | 同 |
| BI-27 | CAUGHT | CAUGHT | judged (1.27) | — | `V9-C4-value-limit-in-rerun`=red | 同 |
| BI-28 | CAUGHT | CAUGHT | judged (1.27) | — | `V4-S17-rerun-whole-checkpoint`=red | 同 |
| BI-29 | CAUGHT | CAUGHT | judged (1.27) | — | `V4-S18-rerun-segment-checkpoint`=red | 同 |
| BI-30 | CAUGHT | CAUGHT | judged (1.27) | — | `V4-S16-rerun-collect-checkpoint`=red | 同 |
| BI-31 | CAUGHT | CAUGHT | judged (1.48) | — | `V4-S16-rerun-collect-checkpoint`=red `V4-S17-rerun-whole-checkpoint`=red `V4-S18-rerun-segment-checkpoint`=red | 同 |
| BI-32 | CAUGHT | CAUGHT | judged (1.48) | — | `V4-S18-rerun-segment-checkpoint`=red | 同 |
| BI-33 | CAUGHT | CAUGHT | judged (1.48) | — | `V10-N6-filtered-long-line-rows-only`=red `V7-N7-big-judge-filtered-long-line`=red | 同 |
| BI-34 | CAUGHT | CAUGHT | judged (1.48) | — | `V7-N8-whole-branch-returns-big-judge`=red | 同 |
| BI-35 | CAUGHT | CAUGHT | judged (1.45) | — | `V7-N9-segment-routes-to-big-judge`=red | 同 |
| BI-36 | CAUGHT | CAUGHT | judged (1.45) | — | `V7-N9-segment-routes-to-big-judge`=red | 同 |
| BI-37 | CAUGHT | CAUGHT | judged (1.45) | — | `V7-N10-blank-padded-long-line`=red | 同 |
| BI-38 | CAUGHT | CAUGHT | void (SKIP [void]): run again (1.45) | CAUGHT (judged, 0.79) | `V8-D4-growth-text-whole`=red | 同 |
| BI-39 | CAUGHT | CAUGHT | SKIP [load] (2.05) | CAUGHT (judged, 0.79) | `V8-D5-growth-text-segment`=red | 同 |
| BI-40 | CAUGHT | CAUGHT | SKIP [load] (2.05) | CAUGHT (judged, 0.79) | `V8-D5-growth-text-segment`=red | 同 |
| BI-41 | CAUGHT | CAUGHT | SKIP [load] (2.05) | CAUGHT (judged, 0.79) | `V5-S15-job-refuses-outside-group-leader`=red | 同 |
| BI-42 | CAUGHT | CAUGHT | SKIP [load] (2.37) | CAUGHT (judged, 0.79) | `V5-E19-deadline-with-term-ignored`\*=red | 同 |
| BI-43 | CAUGHT | CAUGHT | SKIP [load] (2.22) | CAUGHT (judged, 1.20) | `V5-E19-deadline-with-term-ignored`\*=red | 同 |
| BI-44 | CAUGHT | CAUGHT | judged (1.88) | — | `V2-G3b-gate-uses-build-facts`=red | 同 |
| BI-45 | CAUGHT | CAUGHT | judged (1.88) | — | `V6-S20-segment-fallback-text`\*=red | 同 |
| BI-46 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.01) | `V7-N11-lmax-edge-normal`=red | 同 |
| BI-47 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.01) | `V7-N13-unmeasured-length-rows-only`=red | 同 |
| BI-48 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.01) | `V7-N13-unmeasured-length-rows-only`=red | 同 |
| BI-49 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.09) | `V4-S19-block-text-bytes`=red | 同 |
| BI-50 | CAUGHT | CAUGHT | SKIP [load] (2.29) | CAUGHT (judged, 1.09) | `V3-G12-time-left-zero-padded`=red | 同 |
| BI-51 | CAUGHT | CAUGHT | SKIP [load] (2.27) | CAUGHT (judged, 1.09) | `V11-S5-longline-head-verbatim`=red `V11-S7-longline-text-verbatim`=red | 同 |
| BI-52 | CAUGHT | CAUGHT | SKIP [load] (2.27) | CAUGHT (judged, 1.09) | `V8-D4-growth-text-whole`=red | 同 |
| BI-53 | CAUGHT | CAUGHT | SKIP [load] (2.27) | CAUGHT (judged, 1.09) | `V8-D5-growth-text-segment`=red | 同 |
| BI-54 | CAUGHT | CAUGHT | SKIP [load] (2.27) | CAUGHT (judged, 1.17) | `V11-S6-longline-chinese-line-verbatim`=red `V11-S7-longline-text-verbatim`=red | 同 |
| P-0 | GREEN | NOT-JUDGED | SKIP [load] (2.09) | GREEN (judged, 1.03) | （全部移植用例） | 首跑因负载不同，重跑同 |
| P-M29 | CAUGHT | CAUGHT | SKIP [load] (2.09) | CAUGHT (judged, 1.17) | `V7-N11-lmax-edge-normal`=red | 同 |
| P-L-sentinel | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.17) | `V7-N13-unmeasured-length-rows-only`=red | 同 |
| P-L-text | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.17) | `V11-S5-longline-head-verbatim`=red `V11-S7-longline-text-verbatim`=red | 同 |
| P-G-limit | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.15) | `V8-D3-growth-8193-plain`=red `V8-D3-growth-8193-braced`=red | 同 |
| P-G-text-whole | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.15) | `V8-D4-growth-text-whole`=red | 同 |
| P-G-text-segment | CAUGHT | CAUGHT | SKIP [load] (2.08) | CAUGHT (judged, 1.15) | `V8-D5-growth-text-segment`=red | 同 |

## 附录 B：指定用例里有走关门臂用例的 16 个坏实现（all.txt 原行摘录：编号、判定、描述 | 指定用例状态）

- BI-2 CAUGHT no process group and no group-leader self-check: the job PID alone is killed |V5-S5-pipe-holder=red V6-E2-deadline-fallback-bytes=red
- BI-4 CAUGHT the relaxed rerun runs in-process: no job, no hard deadline |V6-E2-deadline-fallback-bytes=red
- BI-5 CAUGHT the gate does not ask about a project extension |V2-G4-extension-file-with-entry=red V2-E9-extension-project=red
- BI-6 CAUGHT the platform is read from the environment (OSTYPE, EPOCHREALTIME present) |V2-G3-gate-calls-platform=red V2-G3b-gate-uses-build-facts=red V2-E8-ostype-from-environment-ignored=red
- BI-7 CAUGHT the fallback writes a time text of its own instead of the baseline size text |V6-E2-deadline-fallback-bytes=red
- BI-8 CAUGHT VMAX relaxed too |V9-E12-vmax-unchanged=red[reference]
- BI-10 CAUGHT the longest line is measured on the raw command, not on the copy |V7-E14-long-line-from-expansion=red
- BI-12 CAUGHT the line length is tested with [[ =~ .{8193,} ]] (it matches across newlines) |V7-N5-read-big-judge-short-lines=red V7-E13-multiline-copy-normal-text=red
- BI-13 CAUGHT the deadline is anchored after the stdin parse, not at the hook start |V3-E3-anchor-at-hook-start=red
- BI-14 CAUGHT the deadline uses the whole budget, not min(budget, 3) |V3-G10-cap-3=red V3-E4-cap-3-at-budget-4=red
- BI-16 CAUGHT the relaxed flag is taken from the environment (not initialised) |V2-G11-flag-not-from-environment=red V2-E6-flag-from-environment-ignored=red
- BI-17 CAUGHT the count bounds also hold inside the rerun |V9-C1-assignments-rerun=red V9-C2-references-rerun-c12=red V9-E10-count-axis-read-blocked=red
- BI-18 CAUGHT TMAX is not checked inside the rerun |V9-E11-tmax-in-rerun=red
- BI-42 CAUGHT the timer and the group kill after the job use TERM instead of KILL |V5-E19-deadline-with-term-ignored=red
- BI-43 CAUGHT the timer uses TERM instead of KILL (the group kill after the job keeps KILL) |V5-E19-deadline-with-term-ignored=red
- BI-45 CAUGHT the segment-mode trigger point keeps the whole-command reason string for the fallback text |V6-S20-segment-fallback-text=red
