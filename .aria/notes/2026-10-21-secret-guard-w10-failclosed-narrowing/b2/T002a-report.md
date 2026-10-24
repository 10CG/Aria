# T002a 报告：10CG/aria-plugin#217 TASK-002 第一步（代码落地）

- 执笔：TASK-002 执笔席（全新实例）；2026-10-24，约 02:17–02:40 UTC
- 工作区：`wt217/aria`，分支 `feature/secret-guard-w10-failclosed-narrowing`，起点 `8614066`；**未提交**
- 产物目录：`r217impl/t002a/`（下文相对路径都相对它）

## 结论

结果 hook（worktree 里的 `hooks/secret-guard.sh`）的 sha256 前缀是 **`65ca336fde2a`**，全值为 `65ca336fde2a4850dbf114a43f1448298fe159f7f6872e2c00430d1fcc37a258`。文件 1738 行，权限 755 保持不变。

它等于原型 `9f61db0e7b8b` 加上 What 1 补充与 What 7 补充：相对原型有 4 个 hunk、+28/−18，没有其他差异。What 6 做成了单独的补丁 `what6.patch`，没有落进 worktree。

核对结果：
- `bash -n`：五个 bash 全部通过，负控能红。
- commentsync target：GREEN。
- 新准入门直调：8 组参数在五个 bash 上全部符合期望。
- 端到端：不设 WSL 标记时放行；设 `WSL_DISTRO_NAME=Ubuntu` 时与基线逐字节相同。
- `sc-cases.sh` 一整轮：PASS 30、FAIL 2。两条 FAIL 都是计时类，负载在 7 以上，按 INV-7 不算数。

**但这一轮的数字有误导性。** 新的 `_sg_relax_platform` 在 `set -u` 下被只传三个参数的 V2-G2 调用时，会让 `sc-direct.sh` 整体中止。结果是除 V2-G1 以外的 62 行直调用例被静默吞掉，而不是像预期那样「V2-G2 一组变红」（见 6.6、6.7 与拿不准的第 2 项）。

## 步骤

| 步 | 做法 | 结果 |
|---|---|---|
| 1 | `python3 v31/mkv31.py <worktree hook> proto.sh` | `proto.sh` 前缀 `9f61db0e7b8b`，符合（mkv31 先断言了基线前缀 `e83c5e30f2cc`） |
| 2 | `cat proto.sh > hooks/secret-guard.sh`（写入已有文件，权限位不变） | 权限 755；相对分支起点 +187/−49，与 W8 一致 |
| 3 | What 1 补充：`apply_supp.py` | 见下 |
| 4 | What 7 补充：同一脚本 | 见下 |
| 5 | What 6：`mk_what6.py` 生成 `what6.sh`，再 `diff -u` 出 `what6.patch` | 见下 |

### 第 3、4 步：提取与断言

脚本是 `apply_supp.py`，输出 `step3.sh` 与 `step4.sh`；`step4.sh` 就是结果。

- **新字面全部从 `proposal.md` 用脚本提取**：
  - What 1 补充：取「**What 1 补充：准入门按实测范围收紧**」之后、`### 2.` 之前的第一个 bash 围栏，共 12 行。断言它恰好定义 `_sg_relax_ok`、`_sg_relax_platform` 两个函数。
  - What 7 补充：取「**What 7 补充：三处注释**」下第 1、2、3 条各自后面的第一个围栏，分别是 2、2、19 行。断言三个围栏都在 `### 参考实现` 之前。
- **旧字面**：
  - 第 1 条取 proposal 里的引文「`…`」。
  - What 1 补充与第 2、3 条按锚点从原型里取：
    - What 1 补充：从 `_sg_relax_ok() {` 到 `_sg_relax_noext() {` 之前；另核对这段是 `mkv31.py` 里 NEW 块的逐字子串。
    - 第 2 条：从 `# _sg_vx_replace S PAT REP [MAX] :` 到 `_sg_vx_replace() {` 之前。
    - 第 3 条：从 `#   - Shell variable indirection` 到下一行 `#` 之前。
- **行号与 proposal 所注一致**（脚本断言）：
  - 第 1 条的旧行在原型 `:578`。`:576` 是 `# W10 -- ` 块头，所以它正是块头第 3 行。
  - 第 2 条在 `:626-627`，第 3 条在 `:87-99`。
  - What 1 补充的旧段在 `:813-821`。
- **命中次数**：每处替换前，断言旧文本（按整行匹配）恰好出现 1 次；替换后，断言每段新文本恰好出现 1 次、旧文本 0 次。
- **产出**：`step3.sh` 前缀 `a0d4275e247e`（1731 行），`step4.sh` 前缀 `65ca336fde2a`（1738 行）。

### 第 5 步：What 6 补丁

- `what6.patch` 只有一个 hunk（`@@ -679,7 +679,6 @@`），只删结果 `:682` 的 `      [[ -z "${_SGV_V[j]}" ]] && continue`。脚本断言这一整行在结果里恰好出现 1 次。补丁标签是 `a/hooks/secret-guard.sh` 与 `b/hooks/secret-guard.sh`，可以直接 `git apply`。
- 核对：
  - `git -C <worktree> apply --check what6.patch` 通过。这一步只检查、不落盘，worktree 仍是 `65ca336fde2a`。
  - 在副本上 `patch -p1` 后与 `what6.sh` 逐字节相同。
  - `what6.sh` 前缀 `69ae80ab6da9`，五个 bash 的 `bash -n` 都是 rc=0。

## 6. 核对

### 6.1 `bash -n`

| bash | 结果 hook | 负控（在 `_sg_relax_platform` 里插一个没有 `fi` 的 `if`） |
|---|---|---|
| /usr/bin/bash 5.2.15 | rc=0，无输出 | rc=2（`line 832: '}'`） |
| 5.0.18 | rc=0 | rc=2 |
| 5.1.16 | rc=0 | rc=2 |
| 5.3.20 | rc=0 | rc=2 |
| 3.2.57 | rc=0 | rc=2 |

原型、基线和 `what6.sh` 也都是 rc=0。

第一次做负控时读数无效：`echo "$(basename …) rc=$?"` 里的 `$?` 取到的是命令替换的状态。改成运行后立即取 rc 再做了一遍，上表是重做的结果。主检查本来就是立即取 rc，不受影响。

### 6.2 相对原型的差异：`vs-proto.diff`

`diff -u proto.sh <结果>` 共 4 个 hunk，+28/−18：

| hunk | 内容 |
|---|---|
| `@@ -85,18 +85,24 @@` | What 7 补充第 3 处：头注释「Shell variable indirection」整条，13 行改为 19 行 |
| `@@ -575,7 +581,8 @@` | What 7 补充第 1 处：W10 块头第 3 行改为两行 |
| `@@ -623,8 +630,8 @@` | What 7 补充第 2 处：`_sg_vx_replace` 的两行说明 |
| `@@ -812,12 +819,15 @@` | What 1 补充：`_sg_relax_ok` 加 3 行、平台调用改为五个参数；`_sg_relax_platform` 的注释与判定 |

没有其他差异。相对基线（分支起点），`git diff --numstat` 是 +203/−55。

### 6.3 commentsync

`python3 v31/commentsync.py --hook-only <结果> target` 的结果是 **GREEN**：20 项全部 ok，exit 0（`commentsync-result-target.txt`）。

对照组说明这项检查能红：基线的 baseline 模式 GREEN，原型的 target 模式 GREEN，基线的 target 模式 RED (28)。

注意：现有 commentsync 不含 What 7 补充三处的锚点，所以 GREEN 只说明 What 7 的 8 块没有回退，不能证明三处补充已经落地。三处补充是否落地，由 `apply_supp.py` 的「新文本恰好出现 1 次」断言保证。commentsync 的改造属于 TASK-002 R2 补强 (e)。

### 6.4 新准入门直调（`direct-gate.sh`，输出 `direct-gate.txt`）

做法：
- 照 `sc-direct.sh` 的写法，用 `awk '/^_sg_relax_platform\(\) \{/,/^\}$/'` 按锚点抽出函数，不 source hook。
- 开 `set -u`，因为 hook 的函数都在 `set -u` 下运行。
- 五个参数全部显式传入。

| # | 参数 | 期望 | 五个 bash 上的返回码 |
|---|---|---|---|
| 1 | x86_64-pc-linux-gnu 5 2 6.17.9-1-pve 空 | 0 | 0，符合 |
| 2 | aarch64-unknown-linux-gnu 5 2 6.1.0 空 | 1 | 1，符合 |
| 3 | x86_64-pc-linux-gnu 5 2 4.4.0-19041-Microsoft 空 | 1 | 1，符合 |
| 4 | x86_64-pc-linux-gnu 5 2 5.15.153.1-microsoft-standard-WSL2 空 | 1 | 1，符合 |
| 5 | x86_64-pc-linux-gnu 5 2 空 空 | 1 | 1，符合 |
| 6 | x86_64-pc-linux-gnu 5 2 6.17.9-1-pve wsl | 1 | 1，符合 |
| 7 | x86_64-pc-linux-gnu 5 4 6.17.9-1-pve 空 | 1 | 1，符合 |
| 8 | x86_64-apple-darwin23 5 2 23.0.0 空 | 1 | 1，符合 |

补充核对（指令里没有要求）：核对 `_sg_relax_ok` 实际传给平台检查的五个参数。
- 做法：抽出 `_sg_relax_ok`，把平台检查换成记录参数的桩，把 `_sg_relax_left` 与 `_sg_relax_noext` 换成放行桩，在本机真实的 `/proc` 下运行。
- 参数：没有 WSL 标记时传的是 `<机器>|<主>|<次>|6.17.9-1-pve|`；设了 `WSL_DISTRO_NAME` 或 `WSL_INTEROP` 时，第五个参数是 `wsl`。
- 换回真实的平台检查后：5.0–5.3 无标记返回 0、有标记返回 1；3.2 一律返回 1。
- 五个 bash 全部符合。

负控：同一脚本对原型跑一遍（`direct-gate-negctl-proto.txt`），第 2–6 组全红（原型会放进 aarch64、WSL1、WSL2、空内核串和带 WSL 标记的环境），参数核对也红。

本机事实：`/proc/sys/kernel/osrelease` 是 `6.17.9-1-pve`；没有 `/proc/sys/fs/binfmt_misc/WSLInterop`；环境里没有 `WSL_*` 变量。

### 6.5 端到端（`e2e-wsl.sh`，输出 `e2e-wsl.txt`，输入输出文件在 `e2e/`）

做法：
- 输入是 `v31/shapes.py benign-big`，8219 字符。
- 按 Claude Code 的方式，以 JSON 喂给 `/usr/bin/bash <hook>`。
- 环境照 `sc-cases.sh` 的 `run()`，去掉 `CLAUDE_PROJECT_DIR`、`_SG_RELAXED`、`SECRET_GUARD_TIME_BUDGET_S`，另外去掉 `WSL_*`。
- HOME 指向私有空目录（INV-5），跑完仍是空的。

| 运行 | rc | stderr | 判定 |
|---|---|---|---|
| 结果 hook，不设 WSL 标记 | 0 | 0 B | 放行，符合 |
| 结果 hook，`WSL_DISTRO_NAME=Ubuntu` | 2 | 721 B | 与基线逐字节相同，符合（`Limit hit: the command is longer than 8192 characters after variable expansion`） |
| 基线（59e333c），设与不设该变量 | 2 / 2 | 721 B，两次相同 | 基线不看 WSL 标记，符合 |

这一轮的负载是 5.7–5.8，所以墙钟只作参考：结果 hook 设标记那次是 1.80 s，基线是 0.34 s。交替重测三次，结果 hook 为 0.96 / 0.38 / 0.33 s，基线为 0.45 / 0.34 / 0.69 s，看不出系统性差异，三次的字节也都相同，判断为负载噪声。

### 6.6 正式一轮：`SC_BASH=/usr/bin/bash bash v31/sc-cases.sh <结果>`（输出 `sc-cases-run1.txt`）

- 实际命令另加了 `taskset -c 0,1 nice -n 19` 与 `HOME=<私有空目录>`（INV-5），其余照指令。BASE 用默认值，即 aria `59e333c`，由脚本自己断言前缀。
- 负载：开始时 `7.25 5.24 3.13`，结束时 `7.78 5.89 3.52`（02:30:13Z–02:31:19Z，共 66 s）。高于 INV-7 的门槛 2，所以计时类的红不算数。
- 汇总：**PASS 30、FAIL 2、SKIP 0，exit 1**，共 32 行。作为对照，W13 里原型在 5.2.15 上是 94 行全绿，其中直调段 63 行。

**最重要的发现：V2-G2 没有变红，而是让直调段几乎整段静默消失。**

直调段只输出了一行 `PASS V2-G1-gate`。原因如下（我在运行前写下了预测，实测与之一致，见 `sc-cases-prediction.txt`）：
1. `sc-direct.sh` source 了 hook，所以它的 shell 开着 `set -u`。
2. 它的 V2-G2 循环每次只传三个参数，第一行是 `x86_64-pc-linux-gnu 5 0`。
3. What 1 补充里的 `_sg_relax_platform` 在 `$1` 匹配 `x86_64-*-linux-gnu*` 之后，会展开没有默认值的 `"$4"`，于是报 `$4: unbound variable`。
4. `sc-direct.sh` 因此整体退出。单独实测时，`bash -c` 下的退出码是 127。

后果：V2-G2 一行都没有输出，后面从 V2-G3 起的 48 行直调用例也全部丢失，一共少了 62 行。`sc-cases.sh` 目前没有哨兵，也没有「应出现的用例编号」清单（这是 R2 补强 (d)，还没做），所以这些用例既不算 FAIL，也不报 SETUP。汇总因此看起来「只红了 2 条」。

两条 FAIL：
1. `V3-E3-anchor-at-hook-start`：墙钟 3.72 s，超出窗口 2.85..3.6；stderr 与基线逐字节相同。
   - 属于计时上界类，负载在 7 以上，按 INV-7 不算数。
   - 之后在负载 7.7–8.8 下复跑四次（原型两次、结果两次），都在窗口内（3.06–3.20 s），没有复现。
2. `V9-E11-tmax-in-rerun`：结果 hook 给出的是 oversize 回落文案（与基线逐字节相同），用时 5.43 s；用例期望在 4.5 s 内给出 tmax 文案。
   - 原因：高负载下首遍就用掉约 2.6 s，重跑在 `_SG_P0 + 3 s` 的截止前做不完，于是回落到基线文案。这是设计内的行为。
   - 它属于「重跑须在截止前跑完」类，按 INV-7 不算数。
   - 在同样负载下对**未改动的原型**跑同一用例两次，也都是红（`ab-timing.txt`），所以不是这次改动造成的。

其余端到端用例与静态用例全部 PASS：V7-E1、V6-E2、V3-E4、V3-E5、V2-E6、V2-E7、V2-E8、V2-E9、V9-E10、V9-E12、V7-E13、V7-E14、V7-E15、V1-E16 共 6 条、V11-S1 共 7 条、V11-S3、V11-S4、V12-C1。

### 6.7 诊断补跑（指令里没有要求，只在 scratch 里做）

目的：让被吞掉的那些直调用例在结果 hook 上也有结论。

做法：把 `sc-direct.sh` 复制到 `diag/sc-direct-g2wrap.sh`，只改两处。
1. V2-G2 那一次调用包进子 shell：`( _sg_relax_platform … )`。
2. 文件末尾加一行哨兵输出。

用例与期望都不改。按顺序在结果与原型上各跑一遍（`diag/summary.txt`）：

| 被测 | 负载（开始 → 结束） | 行数 | PASS | FAIL | 哨兵 |
|---|---|---|---|---|---|
| 结果 | 7.68 → 7.29 | 63 | 58 | 5 | 有 |
| 原型 | 7.29 → 7.81 | 63 | 62 | 1 | 有 |

读法：
- 结果的 5 个 FAIL，恰好是 V2-G2 里期望返回 0 的 5 行：x86_64-pc-linux-gnu 的 5.0、5.1、5.2、5.3，以及 aarch64-unknown-linux-gnu 5.2，都返回了 1。这才是主控预计的「V2-G2 一组红」。
  - aarch64 那一行变红，正是收紧要达到的效果。
  - x86_64 那四行变红，是因为三参数调用拿不到内核串。
- **碰巧绿的四行**：V2-G2 里期望返回 1 的 x86_64 5.4、6.0、4.4 与 x86_64-unknown 3.2 四行显示 PASS，但它们的 1 来自子 shell 里 unbound 中止的退出状态，不是判定逻辑给出的。
  - 我事先预测这里会是 127（从 `bash -c` 顶层的实测类推），实测子 shell 里是 1。预测在这一点上错了，已记在 `sc-cases-prediction.txt`。
- V2-G2 以外的 49 行（含 V2-G1）在结果 hook 上全部 PASS。这包括作业机制（V4、V5）、增长（V8）、计数（V9）、只匹配规则（V10）与 V7-N5。
- 原型唯一的红是 `V3-S4-slow-judgement`：墙钟 1.32 s，窗口 0.85..1.3。这是计时上界类，负载约 7.3，按 INV-7 不算数。

## 与规格不一致或拿不准的地方（都没有自行处理）

1. **What 1 补充之后还有一处注释失实，而它不在 What 7 补充的三处清单里。**
   - 位置：结果 `:799-800`，即原型新增的 relaxed-rerun 块注释的末尾。
   - 现在写的是「In effect only on a Linux build of bash 5.0-5.3 on GNU/Linux (the versions and the platform measured), …」；收紧后实际范围是 x86_64、不在 WSL 里。
   - INV-1 只允许三类内容差，所以我没有改。要改，需要先补 proposal，在 What 7 补充里加第 4 处。
   - 我在全文搜了 `Linux build|GNU/Linux|linux-gnu|WSL|x86_64|aarch64`，旧说法只剩这一处；`:94` 的头注释与 `:820-830` 的两个函数已经是新说法。
2. **`_sg_relax_platform` 里的 `"$4"` 没有默认值。** proposal 原文如此，我逐字落地。
   - 后果：在 `set -u` 下，只要 `$1` 匹配 `x86_64-*-linux-gnu*` 而参数不足 4 个，它不会返回 1，而是中止调用它的 shell。
   - hook 本身不受影响：`_sg_relax_ok` 总是传 5 个已赋值的参数（`local osr= wsl=` 先置空）。
   - 受影响的是测试工装：v31 `sc-direct.sh` 的 V2-G2（见 6.6），以及将来任何少传参数的直调用例。
   - 是否改成 `${4:-}` 属于规格层面的决定（INV-1），我没有改。
   - 建议：下一步改写 V2-G2 时必须传满五个参数，并且同时补上 R2 补强 (d) 的哨兵与应出现编号清单；否则同类中止还会把整段用例静默吞掉。
3. **`v31/sc-cases.sh` 的期望判定与运行环境仍按收紧前的准入门。**
   - `RELAX` 的判定仍是 `*-linux-gnu*` 加 5.0–5.3。
   - `run()` 没有去掉 `WSL_DISTRO_NAME` 与 `WSL_INTEROP`。
   - 本机是 x86_64、没有 WSL 标记，所以碰巧与新准入门一致。换到 aarch64 或 WSL 上，或者环境里带着 WSL 变量时，期望就会错。这属于下一步改用例的范围（R2 补强 (f)）。
4. **commentsync 还没有覆盖 What 7 补充的三处**（见 6.3）。
5. **一处观感问题。** What 7 补充第 3 处的新文本里，「…the pass is re-run under a」这一行明显偏短，下一行接着是「hard deadline …」。这是 proposal 原文，逐字保留。
6. **负载。** 本步所有运行期间，一分钟负载都在 5.7–8.8，来自宿主上其他会话的 claude、python、postgres 进程；没有等到低于 2 的窗口。按 INV-7，本报告里所有计时结论（包括通过的窗口）都不能当证据，计时类需要在低负载时重跑。
7. **我自己的一处数错。** 运行前的预测写的是「其余 61 条直调用例被丢掉」，实际是除 V2-G1 以外的 62 行（V2-G2 14 行加其他 48 行）。预测文件里另追加了更正，本报告以 62 为准。

## 清理与边界

- **改动范围**：只改了 worktree 里的 `hooks/secret-guard.sh`，没有提交；`git -C <worktree> status` 只显示 ` M hooks/secret-guard.sh`。
- **没有碰的东西**：共享检出 `/home/dev/Aria/aria`（`git status` 干净）、主仓（干净），以及 `v31/` 下的任何文件。
- **临时目录**：正式一轮里 `sc-direct.sh` 中止后，留下了一个空的临时目录 `/tmp/tmp.zzPaiJaRB0`。它创建于 02:30:22.9，与那次运行对得上，已用 `rmdir` 删除。
- **进程**：没有残留进程，也没有用 `pkill` 这类按模式批量杀进程的命令。
- **Rule #7**：凭据形路径只在 `shapes.py` 里运行时拼装，没有打印任何凭据形的值。三个私有 HOME（`home-sc`、`home-diag`、`e2e/home`）跑完都是空的。
- **成本**：墙钟约 23 分钟，子代理调用 0 次。

## 文件（都在 `r217impl/t002a/`）

- **hook 各版本**：
  - `proto.sh`：原型。
  - `step3.sh`：What 1 补充之后。
  - `step4.sh`：结果。
  - `what6.sh`：结果再删 What 6 那一行。
  - `base.sh`：基线，取自 aria `59e333c`。
- **补丁与差异**：`what6.patch`、`vs-proto.diff`。
- **脚本**：
  - `apply_supp.py`：第 3、4 步。
  - `mk_what6.py`：第 5 步。
  - `direct-gate.sh`、`e2e-wsl.sh`：直调与端到端核对。
  - `diag/sc-direct-g2wrap.sh`：诊断副本。
- **输出**：
  - commentsync：`commentsync-result-target.txt`。
  - 直调：`direct-gate.txt`、`direct-gate-negctl-proto.txt`。
  - 端到端：`e2e-wsl.txt` 与 `e2e/`。
  - 正式一轮：`sc-cases-run1.txt`、`sc-cases-run1-load.txt`、`sc-cases-prediction.txt`、`ab-timing.txt`。
  - 诊断补跑：`diag/direct-result.txt`、`diag/direct-proto.txt`、`diag/summary.txt`。
- `pl.sh` 只是验证 `set -u` 行为时抽出来的 `_sg_relax_platform`，没有别的用途。

## 第二轮（2026-10-24 约 02:42–02:52 UTC，主控改规格之后）

主控按第一轮报告的第 1、2 件改了 proposal：
- What 1 补充：`_sg_relax_platform` 的每个参数都带缺省。
- What 7 补充：新增第 4 处。

proposal 修改时间是 02:41:59，sha256 前缀 `eb326a389787`。本轮照新字面落地，仍未提交。**本节取代第一轮的结果 hash：worktree 里的 hook 现在是 `238d97cfb92d`。**

### 落地方法（`apply_supp2.py`，输出 `round2.sh`）

我走了两条路径，并断言两者逐字节相同：
- A 路：从原型重建，加上整段新的 What 1 代码块和 What 7 补充第 1–4 处。
- B 路：在第一轮结果上只做增量修改，即只换 `_sg_relax_platform` 的函数体那一行和第 4 处。

两路相同，也就证明了 What 1 代码块里除函数体这一行之外，与第一轮没有任何区别。

新字面全部用脚本从 proposal 提取：
- 函数体行：取 What 1 代码块里 `_sg_relax_platform() {` 的下一行。
- 第 4 处的旧两行：取 proposal 里第 4 条的两个引文「`…`」。
- 第 4 处的新两行：取第 4 条后面的围栏。
- 定位用的标题已换成新的「**What 7 补充：四处注释**」。

断言：
- 每处替换恰好命中一次。
- 第 4 处的旧两行在原型 `:792-793`，与 proposal 所注一致。它们位于 `_sg_vx_big_judge` 正上方那块注释里，这块注释从 `:785` 起，以 `# 10CG/aria-plugin#217 relaxed rerun.` 开头。
- 结果里新的 What 1 整块与四处新文本各恰好出现 1 次，所有旧文本出现 0 次。
- 第 1–3 处的行号（`:576-578` 第 3 行、`:626-627`、`:87-99`）复核仍然一致。

写入方式：`cat round2.sh > hooks/secret-guard.sh`，权限仍是 755。

**新的 sha256 前缀是 `238d97cfb92d`**，全值为 `238d97cfb92dc94b5f966b82e5e0cafeb430e205f18294d3672c2a877b31a9ba`。文件 1738 行，行数不变。相对第一轮，只改了 `:799-800`（第 4 处）和 `:830`（函数体）。

### 核对

| 项 | 结果 |
|---|---|
| `bash -n` | 五个 bash 都是 rc=0。负控（插一个没有 `fi` 的 `if`）五个都是 rc=2。 |
| `diff -u proto.sh <结果>` | 5 个 hunk，+30/−20：`@@ -85` 是 What 7 第 3 处，`@@ -575` 是第 1 处，`@@ -623` 是第 2 处，`@@ -789` 是第 4 处，`@@ -812` 是 What 1 补充。没有其他差异。已覆盖保存为 `vs-proto.diff`。 |
| 准入门直调（`direct-gate2.sh`，输出 `direct-gate2.txt`） | 五个 bash 各 15 条，共 75 条全部 PASS。原来 8 组照旧。新增的 G9 只传三个参数 `(x86_64-pc-linux-gnu 5 2)`，在 `set -u` 下、在调用方自己的 shell 里直接调用（不包子 shell）：返回 1，后面的 `ALIVE` 哨兵行打了出来，脚本 exit 0。补充的 6 条参数核对也照旧全部 PASS。 |
| 直调负控 | 同一脚本对第一轮结果（`step4.sh`）跑，在 G9 处中止（`$4: unbound variable`），G9 行和哨兵行都没有出现，exit 1（`direct-gate2-negctl-round1.txt`）。 |
| 端到端 benign-big（`e2e-wsl-round2.txt`，`e2e2/`） | 不设标记时 rc 0、无输出。设 `WSL_DISTRO_NAME=Ubuntu` 时 rc 2，721 B 与基线逐字节相同，也与第一轮的 stderr 相同。私有 HOME 跑完为空。负载 7.2，墙钟只作参考。 |
| `what6.patch` | 对新结果 `git apply --check` 通过。用新结果重新生成的补丁与原补丁逐字节相同，所以不用换。打补丁后的副本（`what6-r2.sh`）前缀 `af4658b6f935`，五个 bash 的 `bash -n` 都通过。worktree 没有打补丁。 |

补充核对（不在要求清单里）：
- commentsync `--hook-only` target 仍是 GREEN（`commentsync-round2-target.txt`）。
- 用 GNU grep 搜平台措辞，只剩新说法，旧的「Linux build … on GNU/Linux」一处不剩。
- 7 个新函数（`:802`–`:850`）都在 source 闸门（`:1058`）之上。
- 用**未改动的** `v31/sc-direct.sh` 跑新结果（`diag/direct-round2-unmodified.txt`，负载 5.6 → 5.3，用时 20 s）：
  - exit 0，63 行全部出现，用例编号与原型那次逐一相同。
  - FAIL 恰好是 V2-G2 里期望 0 的 5 行：x86_64-pc-linux-gnu 的 5.0、5.1、5.2、5.3 和 aarch64-unknown-linux-gnu 5.2，都返回 1。其余 58 行 PASS。这与事先写下的预测一致（`sc-cases-prediction.txt` 末行）。
  - 第一轮那种整段被静默吞掉的问题不再出现。下一步把 V2-G2 改成五个参数、按新准入门改写期望之后：x86_64 那四行补上内核串后应当转绿；aarch64 那行按 What 1 补充，期望应改为 1。

### 本轮要说明的事

1. **交互 shell 里的 `grep` 被 harness 换成了 shell 函数。** 它调用 claude 内置的 ugrep（参数 `-G --ignore-files --hidden -I`），对模式中间 `$` 的处理与 GNU grep 不同。我有一次闸门位置检查因此取不到行号（`'^if \[\[ "${BASH_SOURCE\[0\]}" != "$0" …'` 命中 0 次；`/usr/bin/grep` 命中 `:1058`）。
   - 这个函数没有 export，所以 `sc-cases.sh`、`sc-direct.sh` 和我写的脚本里用的都是 GNU grep，不受影响。
   - 我在交互 shell 里用正则做过、且结论依赖它的检查（措辞残留、闸门位置、CR 计数、hunk 计数），都已用 `/usr/bin/grep` 重做，结论不变；第一轮「只剩 `:799-800` 一处旧说法」的结论在 GNU grep 下同样成立。
   - 主控复核时如果在交互 shell 里用 grep，需要注意同一点：改用 `/usr/bin/grep` 或 `command grep`。
2. **清理**：直调负控在第一轮结果上中止后，在 scratch 里留下了临时目录 `t002a/tmp.uRTU0afnYH`（里面只有抽出来的 `ok.sh`、`pl.sh`），已删除。本轮在 `/tmp` 下没有新的残留，也没有残留进程。
3. **负载**：本轮仍在 5.3–7.7，没有做计时类判定，墙钟只作参考。
4. **状态**：`git -C <worktree> status` 只显示 ` M hooks/secret-guard.sh`，没有提交。除此之外没有拿不准的地方：新字面与 proposal 标注的行号全部对得上。
5. **成本**：本轮墙钟约 10 分钟，子代理调用 0 次。
