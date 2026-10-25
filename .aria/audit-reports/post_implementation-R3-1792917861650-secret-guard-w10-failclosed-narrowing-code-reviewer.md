---
checkpoint: post_implementation
mode: single-seat
rounds: 3
converged: true
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-25T08:44:21.650Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [code-reviewer]
reviewed_sha: 3ed6c24
reviewed_hook_sha256_prefix: 16996eb7db21
previous_report: post_implementation-R2-1792911087903-secret-guard-w10-failclosed-narrowing-code-reviewer.md
---

# post_implementation R3（单席 code-reviewer，增量复审）— secret-guard W10 尺寸误拦收窄（10CG/aria-plugin#217，TASK-005）

> **Verdict：PASS**。0 Critical / 0 Major / 4 Minor，另列 2 条疑点和几条不构成发现的观察。审查对象是 aria `3ed6c24`。worktree 里 hook 的 sha256 前缀实测为 `16996eb7db21`，与 `git show 3ed6c24:hooks/secret-guard.sh` 的一致。增量面有两部分：`710a36d..3ed6c24 -- hooks/`（3 个文件，+114 / −38），以及主仓 `3117a788` 里 v31 的 5 个文件。规格来源：任务书 `b2/BRIEF-T005r3.md`；proposal v3.4 的 What 1 补充 2、What 3、What 7 补充 2；计划 TASK-005 notes 第 227–230 行。

## 审查范围与方法

- 读了以下 diff：`git diff 710a36d 3ed6c24 -- hooks/`，以及修复轮三段合起来的 `git diff -U0 2893bcc 3ed6c24 -- hooks/secret-guard.sh`；主仓 `git show 3117a788 -- v31/`。另外读了 R2 报告、5f3 报告、主控的 `t005f3-verify/VERIFY.md` 与计划里主控的裁定。
- 探针都在 `r217impl/t005r3/` 下，共 `probe.sh`、`probe2.sh`、`probe3.sh` 三个。每个只做几毫秒的直调，用 `taskset -c 2,3 nice -n 19` 运行。**没有叠挂载，没有开命名空间**，也没跑套件或坏实现。08:35 时负载为 1.40 / 1.14 / 1.14。函数是用 awk 按范围从 hook 里摘出来再 source 的，没有 source 整个 hook。
- 开销读数一律以 5f3 报告和主控复核为准，我只核对了它们自洽不自洽。

## 阶段 1：规格符合 — PASS

- `git diff -U0 2893bcc 3ed6c24 -- hooks/secret-guard.sh` 的 55 行改前与改后（去掉 `+`/`-` 前缀），在 proposal :286-442（What 7 补充 2 的回填）里都能逐字找到。主控的 mkexp 静态 diff 只差头注释那一处，与此一致。
- hook 的 :832-835 和 :841-849 与 What 1 补充 2 的两个代码块逐字相同。顺序也相同：环境变量 → 平台 → 时间 → 文件系统标记 → 扩展。
- 直调用例与 proposal 列的清单一一对应：12 种情形对应 W1a–d 与 W1f–l；「桩成返回 1」对应 W1e；开销用例是 W1n；W1m 钉住「挪到平台与时间判据之后」。W1k 在 uid 0 下 SKIP [platform]，与规格相符。
- v31 的五个文件：
  - `sc-direct.sh`、`sc-cases.sh` 的判据和用例是 helper 与套件的镜像；
  - `mutants.py` 的 BI-22 与 `impl/w14-mutants.py` 的 Q-30 只换了锚点的下一行，坏实现本身不变；
  - `commentsync.py` 只多绑定了 D-3 那一句；
  - `IMPL_SHA12` 已改为 `16996eb7db21`。
- 没有范围外的改动。
- 附带说明：主仓工作区里 `v31/impl/W8-v31.diff` 与 `v31/impl/W11-adversarial.txt` 处于已修改、未提交的状态，应该是并行的 4r 写的。这两个文件不在本轮范围，我没有审，也没有依据它们下任何结论。

## 阶段 2：代码质量与安全

### 优点

- 读挂载表改成 awk 一次读完，开销是线性的。命令替换的退出码用 `|| return 1` 接住，又要求 NR ≥ 1，所以「读不出」和「读出 0 行」两种情况都会关门。两个名字逐个用 `-e` 查，不用通配，`noglob` 和 `failglob` 都改变不了结论。目录不可查时当作有标记。这一项排在平台与时间判据之后。每一处改动都只会把放宽关得更严。
- 失败路径我逐一实测过，全部关门，而且 stderr 都是 0 字节：
  - PATH 上没有 awk：返回 1；
  - 假 awk 退出码为 0 但什么都不输出：返回 1；
  - 假 awk 输出一个词：返回 1。
  - 主控与 5f3 实测过的「目录当表」「空表」「读不出」这里不重复。
- 用例的设计能挡住假绿：
  - W1e 分两面，只有「之前的判据都通过」时才有意义；
  - W1m 带对照腿（平台与时间都过时必须恰好调用一次），防止桩没接上时恒绿；
  - W1g 把「最上层说了算」钉成了可红的断言；
  - W1n 把硬条件和软条件（INV-7）分开。
  - 主控准备的 9 个坏实现按预期全部变红（VERIFY.md 第 3 节）。
- 5 个 bash 上 `bash -n` 全部通过：3.2.57、5.0.18、5.1.16、5.2.15、5.3.20，对 hook、helper、套件各跑一遍，stderr 都是 0 字节。

### Critical

无。

### Major

无。

### Minor

**m-1 新函数和准入门的注释，一处说得比代码窄，两处断言了代码并不保证的「不可能」**

1. hook :835 的行尾注释写着 `the WSL mark of the file system (a WSLInterop entry under binfmt_misc, or a mount table that cannot be read)`。v3.4 还有三种情形会关门：表读出 0 行、目录不可查、`WSLInterop-late`。这里都没写。helper :652 W1e 的文案倒是列全了。
2. hook :841 的函数头写着 `status 0 only when no WSL interop entry can exist`，:845 的行尾写着 `no interop entry can be registered there`。按设计，binfmt_misc 之上若还叠着别的挂载（例如 autofs），函数不往下看、直接返回 0，而下面那层 binfmt_misc 里完全可以登记着项。W1g（helper :194）的假目录里就放着 `WSLInterop`，期望值是 0：用例自己的构造就违反了这句注释的字面意思。行为本身是有意的：为了不触发自动挂载，宁可不看。只是这两处注释把「不看」写成了「不可能有」。
- 修法：这两处都是 What 1 补充 2 代码块里的字面规格，按 INV-1 要先改规格。
  - :835 可以改成 `(see _sg_relax_nowslfs: an interop entry, a table that cannot be read or reads empty, a DIR that cannot be searched)`。
  - :845 可以改成 `... an entry under a lower mount is not looked for (looking could trigger an automount)`。
  - :841 的「can exist」可以改成「is seen」一类说法。

**m-2 `v31/README.md:41` 对 `sc-cases.sh` 判据的描述还停在 v3.3 之前**

- 原文：判据与收紧后的准入门相同，「……没有 `/proc/sys/fs/binfmt_misc/WSLInterop`，这时期望放宽生效」。这是 What 1 补充（v3.2）的单次 `-e`。
- `sc-cases.sh:50-62` 的 `wslmark` 现在实现的是 v3.4 规则：表读不出或为空、最上层是 binfmt_misc、目录可查、两个精确名。
- 这个文件最后一次提交是 `eeb67786`（3b）。修复轮第一段起就没同步，R2 没有报。第三段再次改了这份判据，仍然没同步。
- 修法：把这一句改为引用 What 1 补充 2（v3.4），或者照 `wslmark` 的头注释写。Rule #3 文档同步，不影响行为。

**m-3 测试侧四份判据与 hook 不同义的一处：DIR 是可执行的普通文件**

- hook :846 用 `[[ -x "$d" ]]`。它对可执行的普通文件也为真，随后 `-e "$d/WSLInterop"` 得到 ENOTDIR，结果返回 0（没有标记）。
- 四份测试侧判据用 `( cd -- "$d" )`，位置是 helper :83、套件 :244、`sc-direct.sh:61`、`sc-cases.sh:60`。普通文件上 cd 失败，判为有标记。
- `probe3.sh` 实测：假表把一个 0755 的空普通文件列为 binfmt_misc，hook 返回 0，`wslmark` 返回 0（0 表示有标记）。两边结论相反。
- 影响：准入门走不到这种输入。表里最后一条是 binfmt_misc 时，DIR 是它的挂载根，必然是目录。只有直调参数能构造出来，所以没有假红也没有假绿。但四份判据的注释自称是「the rule of the hook's _sg_relax_nowslfs」，hook 的注释写的是「DIR can be searched」。
- 修法（优先级低）：hook 改为 `[[ -d "$d" && -x "$d" ]] || return 1`。这样只会更严，与测试侧也同义了，但要先改规格。或者在测试侧注释里写明这一处差异。

**m-4 V15-W1l 在 uid 0 下区分不了「逐名查」和「通配」，用例名说的情形并不成立**

- 位置：helper :205-208。期望的情形是目录模式 0311、可查不可列。
- uid 0 有 CAP_DAC_READ_SEARCH，可以列出任何目录（capabilities(7)；W1k :198 的注释用的也是同一条 root 语义）。所以在 root 下，通配写法的坏实现同样能看到 `WSLInterop-late`、返回 1，这条用例照样 PASS。
- 本机是 uid 1000，我没有以 root 实跑，结论依据的是上面的内核语义。
- 影响：已知的坏实现 MG 在 root 下仍会被 W1i、W1j 抓到，所以没有覆盖空洞。只是这条用例在 root 下只测到了 W1b 已经测过的东西。
- 修法：像 W1k 那样在 uid 0 下 SKIP [platform]，或者在注释里写明 root 下它退化成什么。

### 疑点（未核实，单列）

**疑点 1：「表里该挂载点的最后一条」不总等于「路径解析实际到达的最上层」。**

本机实测：本容器（LXC）的 /proc/self/mounts 一共 41 行，第 3 行 `/proc`、第 5 行 `/proc/sys`（又挂了一层 ro 的 proc，parent=1007），没有任何挂载点是 DIR。awk 的原始输出是 `41 `，函数返回 0，stderr 是 0 字节。

下面三种反例是按内核语义推出来的。核实需要叠挂载，任务书禁止，所以都没有核实：

1. **移动过的挂载**（`mount --move`）。它保留创建时的序号，在表里排在原位。如果一个更早建的 autofs 被移到 binfmt_misc 之上，表里最后一条仍是 binfmt_misc，函数就会去查 DIR；那层 autofs 若没人服务，就落进 D-2 的阻塞。
2. **`move_mount(MOVE_MOUNT_BENEATH)`**（6.5+）。把新建的 binfmt_misc 塞到 autofs 之下，后果同 1。
3. **父目录被重新挂载**。例如 binfmt_misc 挂上之后，又有人对 `/proc` 挂了新的 procfs（`unshare --mount-proc`、`bwrap --proc` 加 rbind 的根，都会这样）。表里 DIR 的最后一条仍是旧的 binfmt_misc，路径解析却落到新 procfs 里的空目录：不会触发自动挂载，但会漏掉被遮住的 `WSLInterop`，判成「没有标记」。

暴露面：

- 1 和 2 要有人刻意对 DIR 做挂载操作。systemd 不会在已经是挂载点的路径上启动 automount（R2 已提到）。
- 3 只在一种 WSL2 上才有后果：内核是自编的、版本串里没有 microsoft 或 WSL、环境里也没有 WSL 变量。
- 读表与查项之间恰好被卸载的竞态，仍是 R2 疑点 1 说过的残余。

建议：在 What 1 补充 2 里把「最后一条 = 最上层」写明为近似，列出这几种已知边角。不建议本轮再改代码：用 mountinfo 的 parent 关系判最上层同样解决不了第 3 种。

**疑点 2：LSM 允许查目录、却拒绝对项做 getattr 时，`-e` 会判成没有。**

- `[[ -x ]]` 走 faccessat，会过 ACL 和 LSM 的 search 检查；`[[ -e ]]` 走 stat。stat 遇到 EACCES 和 ENOENT 都返回假，结果都是返回 0。
- SELinux 的 `file getattr`、较新 AppArmor 的 getattr 规则，理论上都能造出这种情形。
- 本机没有可用的 LSM，没有核实。实际暴露面与 m-1 同类：只在不带标记的 WSL2，再加上被约束的 Claude Code 时才有后果。
- 至于 root，faccessat 对目录的搜索权限与查找时的判断一致，ACL 两边也一致，这两项没有发现问题。

### 观察（不构成发现）

- 输出缺分隔符的 awk。假 awk 只输出 `5` 时，`${r#* }` 原样返回 `5`，被当作「最上层不是 binfmt_misc」，函数返回 0（`probe2.sh`）。符合 POSIX 的 awk 执行 `print NR, t` 一定会输出 OFS，所以不会出现这种输出。想再严一点，可以用 `[[ $r =~ ^[1-9][0-9]*\ (.*)$ ]]` 一次把格式和类型都校验掉。
- awk 实现。本机只有 mawk 1.3.4。`/usr/bin/nawk` 存在，没查它指向哪个实现。gawk 和 busybox 都不在，没有实测。程序只用了 POSIX 写法。按 gawk 文档，非 POSIX 模式下 gawk 遇到目录参数会警告并跳过，此时 NR=0，同样关门。
- awk 依赖不是新增的：hook 在 `710a36d` 里就有 12 处非注释行调用 awk。环境若导出一个名为 `awk` 的函数（`BASH_FUNC_awk%%`），就能左右这一项的结论；但 hook 对 jq、sed 一直是同样的信任模型，属于既有问题，不在本轮范围。
- W1n 的硬条件是 `w1nn == 1000`（helper :669）。在把 `fs.mount-max` 调到「现有挂载数 + 1000」以下的宿主上，循环会中途停下，结果是硬 FAIL 而不是 SKIP。默认值是 100000，本机也是 100000，所以正常主机不会误红。建议 0 < n < 1000 时记 SKIP [platform]。
- 转义。内核把字段里的空格、制表符、换行、反斜杠转成八进制，所以别的行不会被误拆出 `$2 == DIR`。默认 DIR 里不含这些字符。直调参数里如果含有它们就永远匹配不上，这只影响用例：`$X` 带空格时，W1b、W1i、W1l 会假红。这是第一段起就有的问题。

## 第 1 项：`_sg_relax_nowslfs` 逐点

- **挂载表与目录状态**：主控在 5 个 bash 上实跑的 12 种情形，与 W1a–l 一一对应。我另外补跑了几种（`probe.sh`、`probe2.sh`、`probe3.sh`）：
  - 只有一行空行的表：返回 0；
  - 末行没有换行的 binfmt_misc 表、目录为空：返回 0；
  - 没有 awk：返回 1；
  - awk 不输出：返回 1；
  - awk 输出异常：返回 1（只有上面那种缺分隔符的输出例外）；
  - 以上 stderr 全部为 0 字节。
- **D-2**：
  - 最上层不是 binfmt_misc 时（叠了 autofs，或只有 autofs），:845 直接返回，`-x` 和 `-e` 都不会执行；
  - 只有 autofs 那种是 W1a；表里最后一条为 autofs 的那种是 W1g；
  - 反例见疑点 1。
- **shell 选项**：已经没有通配和单词拆分。`nocasematch`、`extglob` 对 `[[ == binfmt_misc ]]` 没有影响。IFS 不从环境导入。`set -u` 下各变量都有值。
- **bash 3.2**：能通过 `bash -n`。`=~` 右侧没有加引号的正则在 3.2 下语义正确。主控在 3.2.57 上实跑 12 种情形，0 处不符。

## 第 2 项：准入门顺序与 What 3 上界

- 环境变量那一行（:832）仍在平台判据（:833）之前，经 `$wsl` 让平台判据关门。文件系统标记（:835）失败时直接 return 1。凡是 v3.3 里关门的路径，v3.4 里仍然关门；新顺序只是在平台或时间已经关门时省掉读表，这一点由 W1m 钉住。WSL 上没有新增的放宽路径。
- 关于 What 3 的上界：
  - `_sg_relax_run` 在 :870 先重新调用一次 `_sg_relax_left`，再 fork 作业；计时器睡的是那时算出的 `_SG_LEFT`。
  - 准入门里多出的一次 awk fork（毫秒级）和扩展探测都算进 T_trigger。超出截止就回落，所以「hook 结束 ≤ max(T_trigger, `_SG_P0` + min(预算, 3) s) + ε」仍然成立。
  - proposal :152 已经写明准入门包含这一次读表。
  - 作业里有 `_SG_RELAXED=1`，`_sg_relax_ok` 第一行就返回，所以每次触发只 fork 一次 awk。
- 关于开销：
  - 5f3 的 perf-good 实测 < 0.1 s，perf-v33fn 约 2 s，首尾负载都 < 2；
  - 主控用自己的 hook 跑负控，W1n 为 0.009 s；坏实现 MW 为 3.126 s，界是 0.5 s；
  - proposal 里 awk 的三档读数是 0.003 / 0.008 / 0.026 s。
  - 这些数彼此一致：1000 条时 0.008 对 0.009；逐行读 1000 条时，主控取三次最好为 2.238 s，R2 测得 2.66 s，MW 在套件里测得 3.126 s，都是同一个数量级。
  - 叠在同一个挂载点上时，内核每生成一条记录都要沿整串挂载向上算路径，所以一次读完在内核侧仍是 O(n²)，但常数很小，读数也证实如此。

## 第 3 项：第二轮各条的处置结论

| 条目 | 结论 | 依据 |
|---|---|---|
| M-1 | 到位 | awk 一次读（:843）；挪到平台与时间之后（:835）；W1n 硬加软两层，坏实现 MW 能变红（3.126 s 对 0.5 s）；读数自洽（见第 2 项）。准入门仍在硬截止之外，但现在是线性开销，并且已经算进 What 3 的 T_trigger。 |
| m-1 | 到位 | 逐个查精确名，加了 `-x`；W1i、W1j、W1k、W1l。残余见 m-4（W1l 在 root 下）和疑点 2（LSM）。 |
| m-2 第 1 部分 | 到位（随行为消解） | 能打开却读不出，现在也关门：mawk 读目录以 2 退出；读出 0 行由 NR 检查兜住。测试侧在这个边角上已经和 hook 一致（W1h）。本轮新出现一处不同义，见 m-3，但准入门走不到。 |
| m-2 第 2 部分 | 到位 | 头注释 :101-104 新补的例外与 `_sg_relax_run` 的代码相符（:880，rc 为 2 且有文本时原样写出、仍然拦），与重跑块头 :805-807 同义，commentsync 也已绑定。 |
| m-3 | 到位 | T2 的注释改成两次 `_sg_relax_left`（准入门 :834、run :870），作业拿的是 run 算出的值，与代码相符。 |
| 疑点 1 | 基本到位 | 改成取最后一条，并由 W1g 钉住「叠了 autofs 就不看」。残余的特殊情形见本轮疑点 1。 |

## 第 4 项：新用例与测试侧判据

- **W1f / W1h**：空表和目录当表都期望 1。去掉 NR 检查（坏实现 ME）时 W1f 变红；目录当表在 mawk 下由退出码兜住。
- **W1g**：用例与疑点 1 的关系，见 m-1 第 2 点。断言本身确实证明了「没有去看」：要是看了，就会返回 1。
- **W1i / W1j**：选项在同一个子 shell 里先 eval 再调用，所以选项确实生效。failglob 那条另外断言 stderr 为空。
- **W1k**：按 uid 判是否 root；有 CAP 的非 root 上会假红（不会假绿），主控已经裁定为已知边角。**W1l**：见 m-4。
- **W1m**：三条腿，`1 0`、`0 1`、`0 0`。坏实现 MO（挪回平台判据之前）会让它红出 `[platform] [time]`。只有把读表塞进被桩掉的函数内部才能骗过它，这不现实。
- **W1e**：子 shell 里清掉了 `_SG_RELAXED` 与 WSL 变量，显式把预算设为 3（`_sg_time_budget` 在调用时才读环境），并把 noext 桩成输出 none，所以「前面的判据都通过」确实成立。两面分别能抓到「忽略返回值」（MS）和「取反」（MI）。
- **W1n**：0.5 s 的界，对好实现（约 0.01 s）余量约 50 倍，离逐行读（2–3 s）也有约 4–6 倍。软条件按 INV-7 看负载。没有 `unshare -rm`、或 tmpfs 挂不上时记 SKIP。mount-max 的边角见「观察」。
- **测试侧四份判据**：去掉注释后，函数体逐字相同。主控测得 md5 前缀 `d53dfae530f5`。我按含首行算的 md5，helper 与两份 v31 的三份一致；套件那份只是首行行尾的注释不同。在 12 种情形上与 hook 同义，主控在 5 个 bash 上测得 0 处不符。我补的空行表、末行无换行，按代码推演两边也一致。唯一不同义的是 m-3。

## 第 5 项：注释

- 头注释 D-3 例外：属实（见上表）。
- T2：属实。
- W1n 注释里说 v3.3 要 2.2 s，与主控的 2.238 s 相符。
- W1 块头与 W1m 块头：属实。
- 新函数与准入门的注释：见 m-1。

## 建议汇总（按优先级）

1. m-1 和 m-3 可以一起改，都在 What 1 补充 2 的规格文本里：`-x` 改成 `-d && -x`，:835、:841、:845 三处注释改准，然后照 INV-1 落到 hook，再机械重导出 What 7 补充 2。
2. m-2：同步 `v31/README.md:41`。
3. m-4：W1l 在 uid 0 下记 SKIP [platform]，或者在注释里写明。
4. W1n 在 0 < n < 1000 时记 SKIP，不记硬 FAIL（见「观察」）。
5. 疑点 1 写进 What 1 补充 2，作为已知边角。

## 评估

**是否可以继续？** Yes。

**理由**：v3.4 消除了 R2 的 M-1：读表变成线性，并且排在平台与时间判据之后。R2 的 m-1、m-2、m-3 与疑点 1 也都按裁定处置到位。新代码的每条失败路径都关门，且 stderr 为空。本轮只剩注释与用例层面的 Minor，加上需要刻意改挂载才会出现的疑点。都不改变「只会关、不会开」的姿态，不阻塞 4r 与 TASK-006。

## 运行影响自报

- 3 个探针脚本都在前台运行，每个的 CPU 时间都 < 0.1 s，跑在 2、3 号核上，nice 19。没有挂载，没有命名空间，没有留下后台进程。
- 共用了 27 次工具调用。
