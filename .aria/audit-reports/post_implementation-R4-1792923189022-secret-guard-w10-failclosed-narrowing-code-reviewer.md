---
checkpoint: post_implementation
mode: single-seat
rounds: 4
converged: true
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-25T10:13:09.022Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [code-reviewer]
reviewed_sha: b1d3111
reviewed_hook_sha256_prefix: 628652570ce3
previous_report: post_implementation-R3-1792917861650-secret-guard-w10-failclosed-narrowing-code-reviewer.md
---

# post_implementation R4（单席 code-reviewer，增量复审）— secret-guard W10 尺寸误拦收窄（10CG/aria-plugin#217，TASK-005）

> **Verdict：PASS**。0 Critical，0 Major，3 Minor。其中行为 / 用例能力类 1 条（m-2），措辞类 2 条（m-1、m-3）。另列 1 条疑点和几条观察。
>
> 审查对象是 aria `b1d3111`。worktree 里 hook 的 sha256 前缀实测为 `628652570ce3`。增量面有三部分：
> - `git diff 3ed6c24 b1d3111 -- hooks/`：3 个文件，+22 / −11；
> - 主仓 `409baf36` 里 v31 的 3 个文件；
> - `b2921f62` 里的 `v31/README.md:41`。

## 审查范围与方法

- **读了什么**：
  - 上述三部分 diff；
  - proposal What 1 补充 2（:97–:135，v3.5）；
  - 计划 TASK-005 notes :232–:236：第三轮、主控裁定与停止规则、5f4、主控复核与第四段裁定；
  - 第三轮报告；
  - 5f4 报告（按关键词 grep）；
  - `b2/t005f4-verify/` 里的 PREDICT、VERIFY、RESULT-suite，以及 MD 的输出。
- **静态核对**：
  - hook 的 `_sg_relax_nowslfs` 与 proposal v3.5 的代码块用 `cmp` 比对，逐字节相同。
  - 准入门第二行整行出现在 proposal 里（`grep -xF`）。
  - hook 里与 WSL 标记相关的说法只出现在 :835 和 :841–:849，别处没有残留的旧说法。
- **探针**：
  - 都放在 `r217impl/t005r4/` 下，共三个：`probe.sh`、`probe-userns.sh`、`probe-userns2.sh`。
  - 函数是用 awk 按范围从 hook 和 helper 里摘出来再 source 的，没有 source 整个 hook。`fn-md.sh` 是坏实现 MD：把 `-d && -x` 换回 `-x`。
  - 每个探针都是毫秒级，用 `taskset -c 2,3 nice -n 19` 运行，探针期间负载 1.76–1.96。
  - **没有挂载任何东西**。noexec 那一项用的是本机现成的 `/run/lock`（tmpfs，noexec，可写）。uid 0 那几项用 `unshare -r`，只开用户命名空间，不开挂载命名空间。
  - 没有跑套件，也没有跑坏实现。
  - `probe-userns.sh` 里 0311 那一行把 `$?` 写在一个命令替换之后，读到的是 `wc` 的退出状态，这一行作废，由 `probe-userns2.sh` 重跑。

## 阶段 1：规格符合 — PASS

- hook 只改了 5 行：准入门 1 行，函数 4 行。与 v3.5 的两个代码块逐字节一致。
- 用例改动都与 What 1 补充 2 的「直调用例」段一致：
  - 新增 W1o，对应 13 种情形里的最后一种；
  - W1l 在 uid 0 下记 SKIP [platform]；
  - W1n 叠不满 1000 层时记 SKIP [platform]。
- helper 与 `v31/sc-direct.sh` 的改动相同（INV-2）；两份期望清单都加上了 W1o；`w14-mutants.py` 只换了 IMPL_SHA12。
- 套件头写的计数是 991，无 zsh 时 985，与 5f4 两次整轮的 985 相符。
- 没有范围外的改动。

## 阶段 2：代码质量与安全

### 优点

- **`-d && -x` 只会更严**：
  - 它只是多了一个合取项，判据不成立时一律 `return 1`。
  - `-d` 走 stat(2)，对路径的最后一个分量隐含 AT_NO_AUTOMOUNT；`-x` 走 faccessat，不带 LOOKUP_AUTOMOUNT。所以两者都不会触发自动挂载，没有引入新的阻塞点。
- **与测试侧判据一致**（`probe.sh`）：下面 9 种构造上，hook 与 `wslmark` 的结论逐种一致（两者返回值的极性相反），stderr 全是 0 字节。
  - 0755 普通文件，分别放在可执行和 noexec 的文件系统上；
  - 0755 的 FIFO，同样两处；
  - 指向「装着 `WSLInterop-late` 的目录」的符号链接；
  - 指向空目录的符号链接；
  - 悬空的符号链接；
  - 指向 0755 普通文件的符号链接；
  - 模式 000 的目录；
  - 模式 0311、装着 `-late` 的目录。
- **W1l 的 uid 0 前提已实测**：在 `unshare -r` 下以命名空间 root 运行，通配能看到 0311 目录里的 `WSLInterop-late`（1 个）；uid 1000 下看到 0 个。两种情况下 hook 都返回 1。第三轮的 m-4 当时没有以 root 实跑，这次补上了。
- **W1n 的新 SKIP 分支不会掩盖函数的问题**：
  - 这个分支只看叠了几层。层数 `n` 在调用被测函数之前就已经确定，被测函数改变不了它，所以掩盖不了函数本身的回归。
  - 叠挂载的循环没有时间上限，只在 mount 失败时停下，因此不依赖负载。
  - 输出不是数字时，仍然走硬判定。
- **证据完整**：5f4 用一个从第 501 次起失败的 mount 包装，证明了这条 SKIP 确实能出现；改前的 helper 在同一个包装下是硬红。

### Critical

无。

### Major

无。

### Minor

**m-1（措辞）函数头还有两处说得过满，与 v3.5 写进规格的已知边角相矛盾；测试侧的注释也一样**

hook 一侧，`hooks/secret-guard.sh:841`（这一行也是 proposal What 1 补充 2 的逐字代码块）：

1. 原文：`The entries are looked at only when binfmt_misc is the topmost mount there, so the look never triggers an automount`。
   - 同一节已知边角的第 1 条（proposal :130）写明：遇到移动过的挂载，或者 `MOVE_MOUNT_BENEATH`，表里的「最后一条」并不是实际的最上层，「后果是可能去看一个没人服务的 autofs、落回 D-2 的阻塞」。
   - 也就是说，在这两种情形下，项恰恰是在 binfmt_misc **不是**最上层时被查看的，查看会穿过 autofs，从而触发自动挂载。注释的前后两半都与此相反。
   - 函数头前文已经写了「taken to be the table's last line for it」，这里的「only when … topmost」和「never」却没有跟着改。
2. 原文：`status 0 only when ... and it holds neither WSLInterop nor WSLInterop-late`。
   - 已知边角第 3 条（:132）写的是：LSM 拒绝对项做 getattr 时，`-e` 会判成没有。这时目录里有项，函数却返回 0。
   - 句首已经改成了「no WSL interop entry is seen」，这里的「holds neither」还是第三轮 m-1 第 2 点说的那一类：把「没看到」写成了「没有」。

测试侧：

- 四份判据的头注释和 helper 的 W1 段头里，都有同样一句「so the check / the look never triggers an automount」：helper :77、:174，套件 :238，`v31/sc-direct.sh` :55、:152，`v31/sc-cases.sh` :54。
- 四份判据的注释还写着「the rule of the hook's _sg_relax_nowslfs (What 1 supplement 2, v3.4)」，位置是 helper :74、套件 :235、`sc-direct.sh` :52、`sc-cases.sh` :51。v3.4 时，这几份判据恰好在「DIR 是普通文件」这一处与 hook 不同义（第三轮 m-3），到 v3.5 才同义，所以版本标签反了。

- **失败情形**：没有行为后果。读者会误以为查看项在任何情况下都不会触发自动挂载，并且返回 0 就说明目录里没有项。
- **修法**：hook 一侧要先改规格（INV-1）。
  - 第 1 处可以改为 `so the look does not trigger an automount where the table's last line is the topmost mount (see the known edges)`。
  - 第 2 处可以改为 `and neither WSLInterop nor WSLInterop-late is seen in it`。
  - 测试侧把「v3.4」改成「v3.5」，「never」照上面改。
  - 按停止规则，记录即可。

**m-2（用例能力）W1o 能不能抓到「去掉 `-d`」，取决于临时目录所在的文件系统是不是 noexec**

- **位置**：helper :212–:215（对应 `v31/sc-direct.sh` :190–:193）。W1o 用一个 0755 的空普通文件充当 DIR，注释写的是「-x alone is true for such a file」。
- **原因**：对 noexec 挂载上的**普通文件**，内核的 `access(X_OK)` 一律返回 EACCES（fs/open.c 的 `do_faccessat`，只针对 S_ISREG）。所以在 noexec 文件系统上，`[[ -x 普通文件 ]]` 为假，坏实现 MD 也会返回 1，与好实现相同，W1o 照样 PASS。
- **实测**（`probe.sh`）：
  - `/run/lock`（本机现成的 noexec tmpfs）上的 0755 普通文件：`-x=no hook=1 md=1`，两者相同；
  - 同一目录下 0755 的 FIFO：`-x=yes hook=1 md=0`；
  - 可执行文件系统上的普通文件：`-x=yes hook=1 md=0`。
  - `$X` 来自 `mktemp -d`（helper :28），会落在 `$TMPDIR` 或 `/tmp` 下。
- **影响**：
  - 在 `/tmp`（或 TMPDIR）挂成 noexec 的宿主上（这是常见的加固配置），整个套件没有任何用例能抓到 MD。MX 仍然会被 W1k 和 W1o 抓到。
  - 好实现不会因此假红。
  - 规格已写明准入门走不到「DIR 不是目录」这种输入，所以 MD 漏网也不会改变准入门的行为，因此定为 Minor。
  - 本机的 `/tmp` 在 ext4 根分区上，不是 noexec。主控复核里 MD 在 W1o 上变红的结果有效，4r 不受影响。
- **修法**（二选一，两份直调用例要同步改，INV-2）：
  - DIR 改用 `mkfifo -m 0755 "$w1o"`。noexec 只管普通文件，FIFO 上 `-x` 为真、`-d` 为假，所以在任何 uid、任何挂载选项下都能区分 MD（实测见上）。用例名里的 regular-file 要相应改。
  - 或者保留普通文件，先加一个判断：`[[ -x "$w1o" ]] || out SKIP … "[platform] …"`。

**m-3（措辞，规格）已知边角最后一条「这几种都只在……WSL2 上才有后果」，把前两种也概括了进去**

- **位置**：proposal :133，What 1 补充 2 已知边角的最后一条。
- **问题**：
  - :130 自己写明，前两种情形（`mount --move`、`MOVE_MOUNT_BENEATH`）的后果是「可能去看一个没人服务的 autofs、落回 D-2 的阻塞」。
  - 这种后果出现在准入门一路放行到「查看项」的那条路径上，也就是放宽生效的非 WSL 平台。阻塞到 Claude Code 的 5 s 时 hook 被杀，命令就被放行了（即「为什么」段里的 D-2）。这与 WSL 无关。
  - 只有「漏看 WSLInterop」一类的后果才限于不带其他标记的 WSL2，包括第三种情形、下层的项不看、LSM 这三项。
- **失败情形**：
  - 一台普通的 x86_64 Linux 宿主上，有人把一个更早建好的 autofs 用 `mount --move` 移到 `/proc/sys/fs/binfmt_misc` 上，或者用 MOVE_MOUNT_BENEATH 把 binfmt_misc 塞到 autofs 下面，而这个 autofs 没人服务。
  - 这时表里的最后一条仍是 binfmt_misc。`-e "$d/WSLInterop"` 会穿过 autofs、触发自动挂载并阻塞，D-2 的超时放行就重现了。
  - 前提是有人刻意对 DIR 做挂载操作，所以不升级严重度。但最后一条的概括会让读者以为，非 WSL 宿主不受任何已知边角影响。
- **修法**：
  - 最后一条只覆盖「漏看」类的后果。
  - 在 :130 写明前两种「与平台无关，前提是有人刻意对 DIR 做挂载操作」。
  - 底层情形是第三轮疑点 1 按内核语义推出来的，核实需要叠挂载，本轮仍未核实。本条指的只是规格里两处文字互相矛盾。

### 疑点（未核实，单列）

**疑点 1：LSM 允许搜索 DIR、却拒绝对 DIR 本身做 getattr 时，hook 比测试侧更严。**

- hook 的 `-d` 走 stat，会被拒绝，于是判为「有标记」。
- 测试侧的 `( cd -- "$d" )` 在 bash 非 POSIX 模式下，先按逻辑路径做规范化（`sh_canonpath` 带 PATH_CHECKEXISTS，会做 stat），失败后退回到对原路径直接 chdir。chdir 不需要 getattr，所以会成功，判为「可查」。
- 后果只是证据在这种宿主上假红，方向是安全的。
- 结论依据的是 bash 源码与内核语义。本机没有可用的 LSM，未核实。

### 观察（不构成发现）

- **`[[ -d && -x ]]` 在 root、ACL、符号链接下的语义**：
  - root：有 CAP_DAC_READ_SEARCH 或 CAP_DAC_OVERRIDE 时，目录的 `-x` 不看模式位，与 chdir 一致。`unshare -r` 下，模式 000 的目录 `-x` 为真。
  - ACL：faccessat 与 chdir 走同一个 `inode_permission`，结果一致。本机没有第二个用户，未实测。
  - 符号链接：`-d`、`-x`、`cd` 都跟随链接；链接悬空时三者都失败（实测）。
  - noexec 不影响目录的搜索权限。
- **测试侧的 `cd` 默认走逻辑路径**：如果 DIR 参数里出现「符号链接后面接 `..`」，结论可能与 `-d`、`-x` 按物理路径得出的不同。准入门的默认 DIR 和现有的所有用例都不会出现这种参数。
- **W1k、W1l 的 SKIP 按 `id -ru` 判断**，而权限语义实际看的是有效能力（CapEff 的第 1、2 位）。helper :332 已经有按 CapEff 判断的写法。两者不一致的情形有两种：
  - 非 root 但有 DAC 能力：W1l 照常运行，但区分不了坏实现 MG（MG 仍会被 W1i、W1j 抓到）；
  - root 但去掉了两项 DAC 能力：两条用例都会多 SKIP 一次。
  - 两种情形下，好实现都不会假红或假绿。W1k 在前一种情形下的假红，主控已裁定为已知边角。
- **准入门 :835 的行尾注释**写的是「a DIR there that cannot be searched」，没有写「不是目录」。这与主控第四段裁定 (3) 处理的 helper W1 段头是同一类：字面成立，而且准入门走不到非目录，所以不另列。
- **观察二（假表路径含空白）的假红范围**：除了 W1b、W1i、W1l、W1o，期望 1 的 W1k 也会假红；期望 0 的几条不受影响。它只会造成假红、不会造成假绿，所以「只记录」足够。

## 第 3 项：第三轮各条的处置结论

| 条目 | 第四段的处置 | 结论 |
|---|---|---|
| m-1 | :835 列全了各种关门情形；:841 改成「is seen」，并加上「taken to be」与「lower mount … counts as none」；:844 加上「or reads empty」；:845 改写 | 到位。第三轮点名的三处现在都与代码相符。函数头另有两处同类说法，第三轮没有点名，见本轮 m-1 |
| m-2 | `b2921f62` 改写了 `v31/README.md:41` | 到位。描述与 `wslmark` 的规则一致：表读得出且不为空、取最后一条、目录可查、两个精确名 |
| m-3 | hook 改为 `[[ -d && -x ]]`；新增 W1o | 到位。只会更严，9 种构造上与测试侧逐种一致。残余：W1o 在 noexec 上抓不到 MD（m-2）；LSM 下还有一处不同义，方向偏严（疑点 1） |
| m-4 | W1l 在 uid 0 下记 SKIP [platform] | 到位。前提已在 `unshare -r` 下实测成立 |
| 观察一（W1n 叠不满 1000 层） | 叠到 1–999 层时记 SKIP [platform]；补全了截断的注释 | 到位。不依赖负载，也掩盖不了函数本身的回归 |
| 观察二（路径含空白） | 只记录（第三轮裁定 (4)、第四段裁定 (5)） | 足够。只会假红；记录里可以补上 W1k |
| 疑点 1 | 写进已知边角，不改代码 | 足够，因为前提苛刻。但已知边角最后一条的概括有误，见 m-3 |
| 疑点 2 | 写进已知边角，不改代码 | 足够。要同时满足特定的 LSM 策略和「不带其他标记的 WSL2」两个条件 |

## 第 4 项：新用例与改过的用例

- **W1o**：
  - 断言的就是用例名说的情形：表里把 binfmt_misc 列在一个普通文件上，期望返回 1，stderr 为空。
  - 任何 uid 下，好实现都返回 1，因为 `-d` 为假。
  - 不是恒真：MX 在任何文件系统上都会让它变红；MD 在可执行文件系统上会让它变红，主控复核和本轮 `probe.sh` 都看到了。
  - 在 noexec 上抓不到 MD，见 m-2。不依赖负载。
- **W1l 的 uid 0 分支**：SKIP 的理由属实，实测见「优点」。非 0 uid 的分支与改前逐字节相同。它依赖 uid 的方式与 W1k 相同，见「观察」。
- **W1n 的 SKIP 分支**：见「优点」。`3ed6c24` 里截断的那句注释已经补全，与代码相符。

## 建议

1. m-2 改起来最便宜，改用 FIFO 只需一行。是否为它开修复轮，由主控按停止规则决定：它属于用例能力类，不是措辞类；但它不影响准入门的行为，也不影响本机的证据。也可以等下次因为别的原因改 helper 时一并修改。
2. m-1、m-3 记录即可。下次改规格时，把「never」「holds neither」和最后一条的概括一起改准。
3. 下面是一个未经核实的设计想法，供以后参考，本轮不建议改代码。疑点 1 的三种边角也许可以这样一并处理：
   - 改读 mountinfo，取 DIR 的最后一条；如果它是 binfmt_misc，就把它的 `major:minor` 与 `stat` DIR 得到的 st_dev 比较。
   - 对不上就当作有标记，并且不去查看项。stat 对路径的最后一个分量不会触发自动挂载。
   - 前两种情形里 st_dev 是 autofs 的，第三种情形里 st_dev 是新 procfs 的，都会对不上，从而关门。
   - 代价是多起一个外部 `stat` 进程。

## 评估

**是否可以继续？** Yes。

**理由**：v3.5 的代码改动只会更严，并且与规格逐字节一致；第三轮的 4 条 Minor 和观察一都处置到位，疑点 1、2 与观察二「记录、不改代码」的处置足够。本轮剩下两条措辞类 Minor，以及一条用例能力类 Minor：它不影响准入门的行为，只在临时目录是 noexec 时削弱一条用例。这些都不阻塞 4r 与 TASK-006。

## 运行影响自报

- 共 3 个探针，另有摘出的 `fn.sh`、`fn-md.sh`、`wm.sh`、`fn-spec.sh`，都在 `r217impl/t005r4/` 下。每个探针都是毫秒级，用 `taskset -c 2,3 nice -n 19` 运行。
- 没有挂载，没有开挂载命名空间，没有跑套件和坏实现。在 `/run/lock` 下建的临时目录已经删除。
- 工具调用共 21 次，含写本报告和更正这一行计数的一次。
