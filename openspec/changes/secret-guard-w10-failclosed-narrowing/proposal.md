# secret-guard W10 尺寸预算收窄：超 8192 的副本在硬截止下按增长量重判（10CG/aria-plugin#217）

> **Level**: 2（本 proposal + A.2 产出的 `detailed-tasks.yaml`）
> **Status**: Draft v3.2 —— post_planning R2 判 PASS_WITH_WARNINGS（去重 0C / 20M / 24m），停止规则触发。owner 2026-10-23 选「实现优先」：R2 以 owner 覆盖收口，不开第 3 轮（Decision 19）。v3.2 只改本文与任务计划的文字，原型（`v31/W8-v31.diff`，sha256 前缀 `9f61db0e7b8b`）与证据不变；R2 的验收补强写进 TASK-002 作为必交项。owner 同日另有两项裁定：两类既有缺口点名申报（R-a，Decision 20），准入门按实测范围收紧（What 1 补充，Decision 21）。R2 审的是 v3.1（`95cf1de7`）。下一步：B.1。
> **Created**: 2026-10-21（v1 `acd6a95`）；v2 `41e9308`；v3 `910d9fa2`（2026-10-22）；v3.1 `95cf1de7`（2026-10-22）；v3.2 2026-10-23
> **Linked Issue**: `10CG/aria-plugin#217`
> **关联**：
> - W10 的来源：`10CG/aria-plugin#154`（WP-A `secret-net-l3-and-bypass-paths` TASK-014 的 M6 返工，owner 2026-10-14 裁定 fail-closed）。
> - `10CG/aria-plugin#228`：已转积压，用的是同一批真实流量证据；与本变更的接缝见 Decision 12。
> - `10CG/aria-plugin#216`：协作式时间预算（v1.76.1，已关）。`10CG/aria-plugin#219`：Windows MINGW64 实测缺口。
> - 判定语义上的既有缺口，放宽后覆盖到更多大命令：`10CG/aria-plugin#138`（逐段判定的跨段 pattern）、`10CG/aria-plugin#139`（块结构命令整串判定，credit 对整条命令共享）、`10CG/aria-plugin#140`（`ssh host '…'` / `sh -c '…'` 外壳）、`10CG/aria-plugin#141`（`&` 与换行未作切分记号）、`10CG/aria-plugin#142`（`$(…)`、反引号、heredoc 内部欠拦）、`10CG/aria-plugin#229`（风险行右边界只认空白与行尾）。`10CG/aria-plugin#230`（扩展只替换前 64 处命中）只涉及启用扩展的项目，而这类项目不放宽，所以不在此列（PP1-A20）。
>
> **认领**：`refs/aria/coordination` 上的 `claims/023236f2/s-28df@0755.yaml`，track `secret-guard-w10-failclosed-narrowing-023236f2`，`linked_issue: 10CG/aria-plugin#217`。
> **不变量**：INV-1–INV-9 见 `detailed-tasks.yaml`（INV-4–INV-7 继承自 WP-A `openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml`）。
> **证据**：`.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`——`evidence/` W0–W7（v1、v2 阶段）；`v3/` W8–W12（v3 原型，post_planning R1 审的是它，保持原样）；`v31/` W8、W9、W11–W13（v3.1 原型与实测，说明与本机依赖见 `v31/README.md`）。命令原文不入库。
> **基线**：aria `59e333c`（v1.76.1）的 `hooks/`；当前 aria master `a5ee63b`（v1.77.3）的 `hooks/` 与之零差异（2026-10-23 核：`secret-guard.sh` 的 sha256 前缀仍是 `e83c5e30f2cc`；v1.77.2 `ee9f3a9` 同），下文行号都指这一版，B.1 重锚。standards `a611136`（其后的 `630ba3a` 没有改 `conventions/secret-hygiene.md`）。
> **编号约定**：跨仓引用一律写全 `<org>/<repo>#<n>`（standards `conventions/content-integrity.md` §4.4 规则 1）；「`10CG/aria-plugin#217` 第 N 项」指该 issue 正文的条目。本文自己的条目写作 What 1–7（v3.2 另有 What 1 补充、What 7 补充）、P1–P10、BI-1–BI-23、Decision 1–21；用例写作 `V<k>-…`（`v31/sc-cases.sh` 输出的编号）；owner 裁定点写作「裁定 A–E」；审计簇写作 R1-A*n*、R2-A*n*、PP1-A*n*、PP2-*x* 与 PP2-m*n*；TL2-F4、BA2-F-12、KM-F-01 这类是各轮席位报告里的原编号，报告都在 `.aria/audit-reports/`。
> **审计**：各轮汇总在 `.aria/audit-reports/`；逐簇处置在同目录的 `dispositions.md`（只追加，不是规格）。

## Why

### 现状

v1.76.1 的 W10（变量展开第二遍）有三道尺寸上限，超限一律 fail-closed 拦截。三个常量在 `hooks/secret-guard.sh:594–596`：

| 上限 | 判据（基线代码） | 触发后 |
|---|---|---|
| `_SGV_VMAX` = 4096 | 收集到的单个值超过 4096 字符（`:645`、`:659`、`:668–669`） | `_sg_vx_collect` 返回 2 → 拦，不管变量有没有被引用 |
| `_SGV_SMAX` = 8192 | 代入中的副本**总长**超过 8192（`:685`、`:694`） | `_sg_vx_apply` 返回 2 → 拦。数的是总长，不是增长；整串模式下副本约等于整条命令 |
| `_SGV_TMAX` = 65536 | 分段模式下各段副本长度之和（`:744`） | 拦 |

后果：任何超过 8 KB、又引用了一个已赋值变量的整串模式命令都会被拦，哪怕展开只多出几个字符。

### 真实流量（本机 Claude Code 会话记录）

| 问题 | 结果 | 证据 |
|---|---|---|
| 超过 8 KB 的真实命令有多少被 W10 尺寸上限拦下 | 739 条里 130 条，占 **17.6%** | E12 |
| 超过 4 KB 的真实命令里被拦的 138 条，按原因分 | SMAX（总长）137 条，全部是整串模式；VMAX（值长）1 条 | W1 |
| 那 137 条的增长 | 全部不超过 8192（最大 6200）。W1 是按基线那一遍的计数上限量的；v3.1 重跑不设计数上限，其中 n=1053 代入全部引用后增长超过 8192，在 W12 落入增长超限 | W1；W12 |
| v3.1 原型逐条回放这 138 条（GNU/Linux、bash 5.2、无扩展；负载见 W12 页眉 2.18 2.16 1.93 → 3.49 2.95 2.36） | 放行 136 条，其余 growth 1 条、oversize 1 条；放行的墙钟中位 0.76 s、p90 1.70 s、p99 2.43 s、最慢 2.79 s。138 条的每一种结局都核对了上界 max(触发时刻, 3 s) + 0.3 s：超出 0 条 | W12 第 1 节 |
| 放宽类之外 | 抽样 300 条退出码与 stderr 逐字节相同（300 / 300）；bash 3.2 下 W1 抽 40 条逐字节相同（40 / 40） | W12 第 2、3 节 |

W12 这一轮的负载（见其页眉）高于 INV-7 的门槛 2，表中耗时只作参考，TASK-004 按 INV-7 重测。两个总体不同：E12 数的是超过 8 KB 的命令（130 条被拦），W1 数的是超过 4 KB 的命令（138 条被拦，其中 137 条是 SMAX）；4–8 KB 之间的命令展开后也会超过 8192。E12 在 `.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/evidence/E12-base-real-traffic.txt`。

### 8192 原本要防什么

M6 用「总长 > 8192 一律拦」，防的是「判定迟到 → 超过 Claude Code 的 5 s → fail-open」。判定的代价没有形状上的上界（R1、R2 实测）：

1. **逐行固定项**：`_sg_compute_credit` 对约 14 个过滤器各调用一次 `_sg_line_match`，每次对副本的每一行求一遍正则，约 0.5–0.9 ms/行。
2. **逐 token 平方项**：`:476` 的 tight 检测，一个 8000 字符的 token 单独约 1 s。
3. **跨行项**：`_SG_PS_REMOTE_T`（`:446`）的 `[^|]*` 跨空白也跨换行，包装词密集的 24 KB 文本单这一条要 2–3 s。
4. **构建项**（R2-A2）：`_sg_vx_apply` 按增长判之后，代价是「替换次数 × 串长」，多字节 locale 下再慢一个量级；61.5 K 字符、16 变量 × 16 引用的整串命令，单次 apply 在 bash 5.2 中文填充下约 12 s。

基线靠「超过 8192 就在第一次替换时停下」同时兜住了这四项。v2 只把大副本判定这一步放进硬截止，R2 证明其余几步去掉尺寸早停后都失去上界。所以从 v3 起，放宽之后的全部工作整个放进一个硬截止作业。

## What Changes

只改 `hooks/secret-guard.sh`。参考实现是 `v31/W8-v31.diff`（+187 / −49 行，新增里 4 行空行），由 `v31/mkv31.py` 从基线机械生成（生成前先校验基线的 sha256 前缀 `e83c5e30f2cc`）。「参考实现」一节逐字列出 W8 的全部逻辑 hunk，只有注释 hunk 不列（What 7 按处列出）；这份完整性由 `v31/fill31.py` 机械断言（PP1-A30）。B.2 照此落地（行号重锚），另加三类内容差：What 1 补充、What 6、What 7 补充（INV-1）。验收是 `v31/sc-cases.sh`（见 Success Criteria），TASK-002 把它搬进套件。

### 1. 触发点与准入门

**触发点**：只有基线按总长拦的两处——整串 `_sg_vx_apply` 返回 2（`:725`）、分段 `_sg_vx_apply` 返回 2（`:740`）。在这两处，若 `_sg_relax_ok` 成立，`_sg_vx_pass` 不写拦截文案，把基线的原因串和模式存进 `_SG_OV_PAT`、`_SG_OV_MODE`，返回 4；否则照基线写 oversize 文案、返回 2，一字不变。其余所有拦截（VMAX、TMAX、时间检查点、首遍、扩展）都不经过这里。

**两个顶层变量**在 hook 启动时、紧跟 `set -uo pipefail` 之后一并赋值：`_SG_P0=${EPOCHREALTIME:-}`（截止的锚点）与 `_SG_RELAXED=`（放宽标志，置空）。放宽标志从不取自环境：环境里带着 `_SG_RELAXED=1` 启动 hook，在 v3 上会让顶层直接走放宽规则、没有截止，实测 25 s 后放行（PP1-A2）。

**准入门** `_sg_relax_ok`，以下全部成立才放宽：

| 条件 | 不成立时 |
|---|---|
| 不在放宽重跑之内（`_SG_RELAXED` 为空） | 不嵌套 |
| `_sg_relax_platform "${BASH_VERSINFO[5]}" "${BASH_VERSINFO[0]}" "${BASH_VERSINFO[1]}" "<osrelease>" "<wsl>"`：x86_64 的 GNU/Linux 构建（`x86_64-*-linux-gnu*`）、bash 5.0–5.3、不在 WSL 里（WSL1 与 WSL2 都算：内核串 `/proc/sys/kernel/osrelease` 必须读得到，且不含 `Microsoft`、`microsoft`、`WSL`；也没有 WSL 的互操作标记与 WSL 的环境变量）。只用只读的构建信息与内核信息，环境改不了；`OSTYPE`、`MACHTYPE`、`HOSTTYPE` 都可以被环境改写，不用它们（PP1-A26、PP2-m8）。W8 原型里这一行仍是收紧前的 `*-linux-gnu*`，收紧见下面的 What 1 补充 | macOS、Windows 原生、WSL（WSL1 与 WSL2）、musl、Android、aarch64 等未实测的架构、bash 3.2 / 4.x / 5.4 及以后：与基线逐字节相同（裁定 E；Decision 16、21） |
| 有锚点、有 `EPOCHREALTIME`，且距截止还有时间；剩余时间封顶在 `min(预算, 3)` s，墙钟回拨也不会把截止往后推（PP1-A26） | 首遍已用完时间：按基线拦 |
| `_sg_relax_noext` 输出 `none`：只有「找不到项目根」或「项目根下没有 `.aria/secret-guard.paths`」才算没有扩展。找到了项目根，`.aria/secret-guard.paths` 以任何形态存在（空文件、目录、读不了）都按有扩展处理；找不到项目根（包括取根时 `jq` 出错）就视为没有扩展，这与扩展腿自己的判定一致（PP1-A27、PP2-m7） | 有扩展的项目与基线逐字节相同。理由：扩展对副本 > 8192 有自己的绝对尺寸门（`:1563`），放宽之后结局仍是拦，白耗时间（R2 BA2-F-12、KM-F-01） |

**What 1 补充：准入门按实测范围收紧**（v3.2，owner 2026-10-23，Decision 21）。原型（W8）的 `_sg_relax_platform` 认任何 `*-linux-gnu*` 构建，会放进没实测过的 aarch64 与 WSL（post_planning R2 PP2-m7）。TASK-002 在原型之上把 `_sg_relax_ok` 与 `_sg_relax_platform` 换成下面两段（INV-1 允许的内容差之一），直调用例按新的五个参数改写：

```bash
_sg_relax_ok() {   # status 0 when the relaxation is in effect for this command; the extension is asked inside a command substitution, like every extension call
  [[ -z "${_SG_RELAXED:-}" ]] || return 1
  local osr= wsl=
  { IFS= read -r osr < /proc/sys/kernel/osrelease; } 2>/dev/null
  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" || -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && wsl=wsl   # WSL marks; the environment can only switch the relaxation off with them
  _sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}" "${BASH_VERSINFO[1]:-0}" "$osr" "$wsl" || return 1   # read-only build and kernel facts, which the environment cannot rewrite (OSTYPE, MACHTYPE and HOSTTYPE can be)
  _sg_relax_left || return 1
  [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]
}
_sg_relax_platform() {   # MACHINE MAJOR MINOR OSRELEASE [WSL]: status 0 on an x86_64 GNU/Linux build of a bash version the mechanism was measured on, 5.0 to 5.3, outside WSL (owner ruling E, 2026-10-22 and 2026-10-23: an untested platform -- macOS, Windows, WSL1 and WSL2, musl, Android, aarch64 and other architectures, another bash -- keeps the baseline)
  [[ "${1:-}" == x86_64-*-linux-gnu* && -n "${4:-}" && "${4:-}" != *[Mm]icrosoft* && "${4:-}" != *WSL* && -z "${5:-}" ]] && (( ${2:-0} == 5 && ${3:-0} <= 3 ))
}
```

`/proc/sys/kernel/osrelease` 读不到时第四个参数为空，准入门关闭。WSL1 的内核串形如 `4.4.0-19041-Microsoft`，WSL2 形如 `5.15.153.1-microsoft-standard-WSL2`；自编内核的 WSL2 未必带这些字样，所以另看 `/proc/sys/fs/binfmt_misc/WSLInterop` 与 `WSL_DISTRO_NAME`、`WSL_INTEROP` 两个环境变量。环境变量能被改写，但它们只能把放宽关掉，不能打开。owner 2026-10-23 先选排除 WSL1，随即追加 WSL2：WSL2 虽是真 Linux 内核，也没有实测过。这是往更严方向的改动，姿态不变。

每个参数都带缺省（2026-10-24 改，B.2 TASK-002 第一步发现）：hook 开着 `set -u`，少传一个参数就会让调用方整体中止，在 hook 里中止即退出码不是 2，等于放行；带缺省之后，缺参数时准入门关闭。

**What 1 补充 2：WSL 标记的读法不触发自动挂载，且读表的开销随挂载数线性增长**（v3.3 起于 2026-10-25 TASK-005 复审 D-1、D-2；v3.4 同日按复审第二轮 M-1、m-1 与疑点改写；技术口径，姿态不变：只会把放宽关掉，不会打开。INV-1 允许的内容差之一）。

为什么：What 1 补充里 `-e /proc/sys/fs/binfmt_misc/WSLInterop` 在多数 systemd 宿主上会穿过 autofs 自动挂载点：一般毫秒内挂上，但自动挂载没人服务时（例如继承了宿主 autofs 挂载点的容器或 chroot）stat 可能一直阻塞，hook 超过 Claude Code 的 5 s 被杀后命令就放行了，而基线从不碰这个目录、本会按尺寸拦——这是放宽带来的新放行路径（D-2）。较新的 WSL 还可能把互操作项登记成 `WSLInterop-late`（D-1）。v3.3 改为先读挂载表、只在 binfmt_misc 已挂上时看项，但用 bash 的 `while read` 逐行读 `/proc/self/mounts`：bash 读完每一行都往回 seek，procfs 每次都从头重新生成这张表，开销随挂载数成平方增长（复审第二轮 M-1；主控在私有挂载命名空间里叠 tmpfs 实测：500 条 0.34 s、1000 条 2.24 s、2000 条 17.2 s），而读表在硬截止之外——挂载多的宿主上又成了一条超时放行的路径，而且是 v3.3 自己引入的。v3.3 还有三处说法与做法不符：用通配 `WSLInterop*` 看项，环境导入的 `noglob` 会让它看不见、`failglob` 会让它报错中止（m-1）；空表或「能打开却读不出」的表按「没挂上」处理；同一挂载点上 binfmt_misc 之上若又叠了 autofs，仍会去看项、触发自动挂载（疑点）。

v3.4 的做法：
- 挂载表交给 awk 一次读完（开销线性：同样的叠挂载下 500 / 1000 / 2000 条为 0.003 / 0.008 / 0.026 s），只取该挂载点的**最后一条**（最上层的挂载）的文件系统类型；表读不出、或读出 0 行，都当作可能在 WSL 里，准入门关闭。
- 只有最上层是 binfmt_misc 时才看项，逐个看 `WSLInterop` 与 `WSLInterop-late` 两个名字，不用通配——环境导入的 shell 选项改变不了结论，目录可查不可列时也照样看得到；目录不可查（没有搜索权限，项在不在看不到）时当作有标记，准入门关闭（复审第二轮 m-1：看不了就当作有标记）。
- 这一项挪到平台判据与时间判据之后：非放宽平台、或已没有时间时，挂载表根本不读。

`_sg_relax_ok` 相对 What 1 补充，WSL 那一行换成下面第一行，并在 `_sg_relax_left` 之后加第二行：

```bash
  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl   # WSL marks in the environment; the environment can only switch the relaxation off with them
  _sg_relax_nowslfs || return 1   # the WSL mark of the file system (a WSLInterop entry under binfmt_misc, or a mount table that cannot be read), asked only where the platform and the time would relax: elsewhere the mount table is never read
```

新函数（与其余 `_sg_relax_*` 一样定义在 source 闸门之上，INV-4）：

```bash
_sg_relax_nowslfs() {   # [MOUNTS [DIR]]: status 0 only when no WSL interop entry can exist -- the mount table (default /proc/self/mounts) reads and is not empty, and the topmost mount at DIR (default /proc/sys/fs/binfmt_misc; the table's last line for it) is not a binfmt_misc file system, or it is, DIR can be searched, and it holds neither WSLInterop nor WSLInterop-late. awk reads the table in one pass: a line-by-line read of /proc/self/mounts in bash costs O(n^2) (bash seeks back after every line and procfs regenerates the table from the start), seconds on a host with a few thousand mounts, outside the hard deadline. The entries are looked at only when binfmt_misc is the topmost mount there, so the look never triggers an automount; the two names are tested one by one, not by a glob, so noglob or failglob imported from the environment cannot change the look. A table that cannot be read, or reads empty, keeps the relaxation off. The two arguments exist for the direct-call cases only; the gate calls it with none
  local d="${2:-/proc/sys/fs/binfmt_misc}" r
  r=$(awk -v d="$d" '$2 == d { t = $3 } END { print NR, t }' "${1:-/proc/self/mounts}" 2>/dev/null) || return 1
  [[ "${r%% *}" =~ ^[1-9][0-9]*$ ]] || return 1   # no line read: a table that cannot be read
  [[ "${r#* }" == binfmt_misc ]] || return 0   # binfmt_misc is not the topmost mount at DIR: no interop entry can be registered there, and nothing under DIR is looked at
  [[ -x "$d" ]] || return 1   # DIR cannot be searched: the entries cannot be seen, so they may exist
  [[ -e "$d/WSLInterop" || -e "$d/WSLInterop-late" ]] && return 1
  return 0
}
```

主控交付前在 3.2.57、5.0.18、5.2.15、5.3.20 上对这段代码实跑：真实路径 0；只有 autofs（目录里有 `WSLInterop`）0；binfmt_misc 加 `WSLInterop-late` 1；binfmt_misc 无项 0；binfmt_misc 之上叠 autofs（目录里有 `WSLInterop`）0；空表 1；读不出 1；把目录当表 1；`set -f` 下 binfmt_misc 加 `WSLInterop-late` 1；`shopt -s failglob` 下 binfmt_misc 无项 0；binfmt_misc 目录不可查（000）1；可查不可列（0311）加 `WSLInterop-late` 1；stderr 全程 0 字节（uid 1000；本机的 awk 是 mawk，程序只用 POSIX awk 的写法）。去掉 `-x` 那一行时只有目录不可查那一条变成 0。v3.3 的写法在前十种情形里有五处不符（叠 autofs 1、空表 0、目录当表 0、noglob 下 0、failglob 下报错中止，后两种情形因此没跑到；复审第二轮实测它在目录不可列时返回 0）。

直调用例（TASK-005 修复轮补）：上面各情形各一条（假挂载表与目录建在 helper 自己的临时目录下；目录不可查那一条在 uid 0 下不适用——root 可查任何目录——记 SKIP [platform]）；把 `_sg_relax_nowslfs` 桩成返回 1 时，放宽平台上的 `_sg_relax_ok` 返回 1；另有一条开销用例：在私有挂载命名空间里叠 1000 个 tmpfs 后读真实的挂载表，函数须在 0.5 s 内返回（没有 `unshare -rm` 的宿主上 SKIP [platform]）。

### 2. 放宽重跑的规则（`_SG_RELAXED=1`，只在作业里生效）

- **副本上限按增长**：`_sg_vx_apply` 入口 `lim=$_SGV_SMAX`；放宽时 `lim=$(( ${#1} + _SGV_GMAX ))`。必须用 `${#1}`，因为循环里 `s` 会被改写（BI-9）。增长恰为 8192 放行、8193 拦，两种引用拼写一致（`V8-D2`、`V8-D3`）。超限的原因串见 What 5。放宽之外 `lim` 就是 `_SGV_SMAX`，函数契约不变。
- **没有计数上限**（PP1-A1，Decision 14）：基线的三个计数上限——收集 16 个赋值、8 个 for、每个变量替换 8 次——在重跑里取消，所有赋值都收集、所有引用都代入。这三个上限原本只为封顶基线那一遍的成本；重跑的成本由截止、增长上限与 TMAX 封顶，循环每轮都消耗掉一段串，不会空转。基线那一遍（小命令）照旧有上限（`V9-C1b`、`V9-C2b`）。实现上「取消」写作把上限设为 1,000,000：要收集到这个数，命令至少要几 MB，截止远在它之前到达；到顶时静默止步，记入残余 9（PP2-m16）。
- **副本 > `_SGV_SMAX` 的判定**：`_sg_vx_big_judge` 用一个线性的 `while IFS= read -r` 循环量**副本**的最长行（BI-10）；循环一次都没跑时按超长处理（哨兵，PP1-A27）。最长行 > `_SGV_LMAX`（8192）时只匹配规则、不算 credit（裁定 C，调用 `_sg_judge_one … nocredit`）；否则是与小副本相同的普通判定（裁定 A）。
- **副本 ≤ `_SGV_SMAX`**：普通 `_sg_judge_one`。这包括缩短类（放宽面 R-b）。
- **不变的**：VMAX；TMAX（重跑里照常累计，超过就写基线的 TMAX 文案，`V9-E11`）；W12 中和；credit 语义。
- **时间检查点**：重跑里 `_sg_vx_pass` 的三个协作式时间检查点直接返回 3、不写文案，交给回落（What 4）。

`_sg_judge_one` 增加可选第三参数 `nocredit`：命中规则后、算 credit 之前，若为 `nocredit` 就写 `longline` 文案并返回 2。W12 中和在规则循环之前执行，所以 C 路径与普通路径共用同一份中和代码，也只有一份规则循环（P10，`V11-S4`）。不传第三参数时与基线逐字节相同。

### 3. 硬截止作业

- **截止**：`_SG_P0` + `min(_SG_TIME_BUDGET, 3)` 秒，微秒精度。首遍的时间也算在里面：Claude Code 的 5 s 从 hook 启动算起（BI-13，`V3-E3`）。计时器睡的是 `_sg_relax_run` 里算出的剩余时间 `_SG_LEFT`，计时器在 fork 出作业之后才起，所以杀组实际落在这个时刻之后一段 fork 延迟上；这段延迟算在下面耗时上界的 ε 里（TASK-005 m-5，2026-10-25 补）。
- **作业**：`_sg_relax_run` 在命令替换里先 `exec 2>/dev/null`（赋值语句后面的重定向管不到命令替换本身，PP1-A25），再 `set -m`，后台作业因此自成进程组。
- **自检**：作业开工前读 `/proc/$BASHPID/stat`，确认自己是进程组组长，否则以 9 退出（回落）。`set -m` 不生效的 bash 由此安全退化。这条拒绝分支在实测的五个 bash 上从不触发，由 TASK-002 补的直调用例钉住（PP2-J）。
- **计时器在作业里**：自检之后、第一步判定之前，作业自己起计时器 `( sleep "$_SG_LEFT"; kill -KILL -- "-$me" )`，并用 `kill -0` 确认它在跑，否则以 9 退出、不判定（BI-3，`V5-S10c`）。计时器写成 `sleep …; kill …` 而不是 `&&`：`sleep` 失败（不存在、或不认小数秒）时计时器立即杀组，同样是回落（`V5-S14`；BI-23）。
- **fork 失败**：bash 遇到 EAGAIN 会先自行重试（共约 15 s），再中止所在的子 shell。作业 fork 失败时中止的是命令替换，计时器 fork 失败时中止的是作业，两种情况判定都不会开始，结局是回落。计时器那一种由 `V5-S10` 实测（用 `ulimit -u 1` 制造，15.00 s 后回落）；作业那一种由 PP1 的 BA 席实测（同样约 15 s 后回落），用例里没有，因为制造它要改 `_sg_relax_run` 本身。这与基线自己的 fork 失败同类（基线遇到 fork 失败同样整体退出），不是新增的 fail-open（PP1-A4）。
- **结论只取退出码**：作业在 `_sg_vx_pass` 返回 0 时以 **77** 退出，返回 2 时以 2 退出，其余以 1 退出。`_sg_relax_run` 只把 77 当放行；2 且有文本就原样写出文本；其他一律返回 4。文本从不参与判定，裸 `0`（例如 `wait` 对一个继承来的旧 PID 返回 0）也不会被当成放行（PP1-A28，Decision 15，`V4-S11`）。
- **作业结束后再杀一次组**：`wait` 返回后对作业的进程组 `kill -KILL`，计时器与判定留下的任何后代都不会活过 `_sg_relax_run`，也不会占住管道把结论拖过截止（PP1-A3，`V5-S9`、`V5-S13b`）。组里已没有成员时这一步静默失败。
- **竞争窗口**：作业正常结束、组杀之前若恰好到点，计时器会对正在退出的进程组发一次 KILL。组内进程被回收之前 PID 不会复用，所以只会杀到本作业自己的进程，可以忽略。
- **耗时上界**：hook 结束时间 ≤ max(T_trigger, `_SG_P0` + min(预算, 3) s) + ε。T_trigger 是到达触发点的时刻，即 hook 启动 + 首遍 + 基线 W10 前段 + 准入门（含一次扩展探测）；ε 是截止之后的收尾：命令替换返回、回落文案里 fork 的 `sed`、进程退出，以及计时器起得比算出 `_SG_LEFT` 晚的那段 fork 延迟（TASK-005 m-5）。低负载实测在 0.1 s 以内，负载约 10 时实测 0.2–1.2 s（PP2-m6）；hook 启动之前的 shell 启动时间也不在上界里。首遍本身不计时，属 `10CG/aria-plugin#228`。这些项都随宿主负载变化；不随负载变化的只有截止本身（PP1-A29）。

### 4. 回落 = 基线

`_sg_relax_run` 返回 4（截止、时间检查点、自检、计时器未起、内部错误、拦截却无文本、裸 0）时，`_sg_per_segment_eval` 用存下的 `_SG_OV_PAT`、`_SG_OV_MODE` 写 oversize 文案并返回 2，与基线逐字节相同（P6）。一个例外：作业里 bash 自身的致命错误若以状态 2 退出并往 stderr 写了报错（例如内存分配失败），`_sg_relax_run` 会把它当作「2 且有文本」原样写出——结局仍是拦，文案却是 bash 的报错，不是基线文案（TASK-005 D-3，依赖 bash 的实现，未实测，2026-10-25 补）。放宽重跑放行时直接返回 0：准入门已保证没有扩展生效，扩展腿本来就是空操作。

### 5. 文案（逐字）

| 场合 | `_sg_emit_blocked` 的参数 | 模板 |
|---|---|---|
| 增长超限，整串 | `"the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" whole oversize` | oversize；`Limit hit:` 行即左列原因串 |
| 增长超限，分段 | `"a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize` | 同上 |
| 重跑里分段副本总和超过 65536 | 基线的 TMAX 原因串，一字不变 | oversize（基线文案；以前这类命令先被 SMAX 拦，现在可能看到 TMAX 文案，见 R-c） |
| 重跑里任一值超过 4096（基线那一遍只收集前 16 个赋值与前 8 个 for，后面的值看不到；重跑全部收集） | 基线的 VMAX 原因串，一字不变 | oversize（基线文案；以前这类命令先被 SMAX 拦，现在可能看到 VMAX 文案，见 R-c；TASK-005 m-1，2026-10-25 补） |
| 超长单行命中规则 | `"$pat" "$seg" "$mode" longline` | 新模板，见下 |
| 截止、时间检查点及其他失败 | （回落）基线原因串 | 基线 oversize 文案，逐字节不变 |

`longline` 分支插在 oversize 分支之后。它新写的只有描述：首段「为什么拦」与中文行的前半句；「Split it…」起的四行指令**逐字复用** oversize 模板的全部指令行（v3 漏了「do not repeat one long $VAR」那一条，PP1-A19），中文行以与其他模板相同的「请拆成更小的命令」收尾。逐字复用由 `V11-S3` 机械钉住。heredoc 正文如下：

```
[secret-guard] BLOCKED: command reads a secret-bearing source, and after variable
expansion it has a line longer than ${_SGV_LMAX} characters. Matched pattern: $pat

At this size the guard does not look for value-REDACTING filters (| jq 'keys',
| wc -c, >/dev/null, ...): on a line this long that check alone is too slow to
finish within the hook's time limit, so the match alone blocks the command
(fail-closed).

Split it into smaller commands and run them one at a time:
  - keep every variable value, and every command after expansion, short;
  - do not repeat one long \$VAR many times in a single command;
  - write long files with the Write / Edit tool instead of a heredoc.
命令读取含密钥的来源, 且变量展开后有超长的行, 这个尺寸下不评估脱敏过滤, 请拆成更小的命令

Command was (first 200 characters): $(_sg_redact_echo "${command:0:200}")
```

分段模式下不追加「Triggering segment」行，因为副本可能很长。

### 6. 小项：删 `:666` 的死代码（`10CG/aria-plugin#217` 小项）

删掉 `_sg_vx_collect` 链式循环里恒为假的 `[[ -z "${_SGV_V[j]}" ]] && continue`。空值在收集时已跳过（`:646`、`:660`），链式代入只会把非空串换成非空值（R1、R2 三席与 PP1 BA 席核实）。与放宽机制无关，单独提交，套件全绿即可。W8 的原型不含这一删，它是 INV-1 允许的内容差之一（PP2-N）。

### 7. 注释同步（块级封闭清单）

v3 每处只钉一个短语，同一注释里其他会失实的句子不受检查（PP1-A18）。v3.1 按**块**核对：每处是基线里的一整块注释，由锚点短语定位，并记下整块的 sha256。`v31/commentsync.py` 的 baseline 模式在基线上实跑为 GREEN（每个锚点都能找到、每块的哈希都对得上，所以检查能红）；target 模式要求锚点为 0 次、带这些哈希的块一个不剩、「应出现」的词至少 1 次。块哈希一个不剩只是锚点消失的推论，证明不了整块重写过：在锚点里各插一个字符、再加一行 ADD 词，未改动的基线就能 GREEN；整块删掉也 GREEN（post_planning R2 PP2-M）。TASK-002 把它改成每处列出全部会失实的句子（各要求 0 次），并绑定站点内必须出现的新句子。读法：先把连续的 `#` 注释行去掉前缀、连接成一行。行号为基线。

hook 的 8 处已由原型整块重写（`mkv31.py` 第 10 步），`commentsync.py --hook-only <原型> target` 为 GREEN（`V12-C1`）；所以「逐字落地原型」与「注释核对为 GREEN」不再冲突。套件的 7 块与 5 个用例标题由 TASK-002 改写。

| 处 | 位置（基线） | 定位用的锚点短语（改后 0 次） |
|---|---|---|
| 1 | hook :87-95 header W10 gap | `beyond a SIZE limit the whole command is BLOCKED as too large to scan`；`never passed` |
| 2 | hook :577-590 LENGTH BUDGET | `Beyond ANY of them the whole command is BLOCKED`；`blocking is as cheap as passing was`；`The limit counts the whole judged string, not its growth` |
| 3 | hook :597-606 time budget | `the _SGV_* size budget are unchanged` |
| 4 | hook :674-676 _sg_vx_apply | `2 = the copy would be longer than _SGV_SMAX` |
| 5 | hook :701-703 _sg_vx_pass | `ends the pass at once with an oversize BLOCK` |
| 6 | hook :826-828 _sg_emit_blocked | `_sg_emit_blocked PAT SEG MODE [oversize]` |
| 7 | hook :1492-1496 _sg_judge_one | `string to judge, $2 = mode (whole\|segment). Returns` |
| 8 | hook :1531-1536 _sg_per_segment_eval | `2. only if it allowed, the W10 variable pass (_sg_vx_pass);`；`Length budget: an overrun inside _sg_vx_pass blocks there` |
| 9 | test :2510-2518 W10 block head | `beyond a limit the command is BLOCKED`；`_SGV_SMAX 8192 = one substituted copy` |
| 10 | test :2544-2549 21aa/21ab | `the WHOLE judged string, not its growth` |
| 11 | test :2556-2562 21ac/21ad | `which is how a 4096-character list is refused` |
| 12 | test :2578-2585 21af/21ag | `Red when (21ag): the 36 KB dense copy passes` |
| 13 | test :2597-2599 21aj | `Red when (21aj): such a segment is skipped or counted instead of refused` |
| 14 | test :2628-2632 21al | `Red when (21al): the braced 8193-character whole copy passes` |
| 15 | test :2679-2681 21ao | `Red when (21ao): the 8193-character whole copy passes` |
| 16 | test :2552 21ab title（用例标题，整句） | `W10 SC-21ab bf: copy limit exceeded is refused — 8193 characters: the copy is not judged, the command is blocked as too large (no padding passes)` |
| 17 | test :2586 21ag title（用例标题，整句） | `W10 SC-21ag bf: the dense shape of the review (15 assignments of 300 B, 8 references each: a 36 KB copy; 16 x 300 B x 8 took 5.4 s) is over the copy limit and refused as too large` |
| 18 | test :2605 21aj title（用例标题，整句） | `W10 SC-21aj bf: a segment over the copy limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large and the reader is never judged` |
| 19 | test :2633 21al title（用例标题，整句） | `W10 SC-21al bf: the copy limit holds for the braced form too — a substituted whole command of exactly 8192 characters is judged and blocked, 8193 is refused as too large` |
| 20 | test :2682 21ao title（用例标题，整句） | `W10 SC-21ao bf: whole-command mode obeys the copy limit — a whole copy of exactly 8192 characters is judged and blocked, 8193 is refused as too large` |

「应出现」的词（改后至少 1 次，基线 0 次）——hook：`_SGV_GMAX`、`_SGV_LMAX`、`_SG_P0`、`hard deadline`、`nocredit`、`longline`、`_sg_relax_run`、`status 4`；套件：`_SGV_GMAX`、`longline`。

改写后的文字是否准确，由 TASK-005 的代码审查把关；这项检查只保证锚点句不再出现。

**What 7 补充：四处注释**（v3.2；INV-1 允许的内容差之一。TASK-002 在原型之上逐字落地，并为它们补上 commentsync 的核对）。原型里这四处仍按收紧前、计数上限未申报前的说法写着（post_planning R2 PP2-m4、PP2-S、PP2-m7；第 4 处是 B.2 TASK-002 第一步发现的，2026-10-24 补）：

1. W10 块头（原型 `:576-578`）：第 3 行「`# most 16 assignments and 8 replacements per variable); every segment (the whole command when it degraded) that mentions $NAME or ${NAME} is judged once more with the`」换成下面两行：

```
# most 16 assignments, 8 for lists and 8 replacements per variable in the baseline pass, none in the relaxed rerun of 10CG/aria-plugin#217); every segment (the whole
# command when it degraded) that mentions $NAME or ${NAME} is judged once more with the
```

2. `_sg_vx_replace` 的说明（原型 `:626-627`）换成：

```
# _sg_vx_replace S PAT REP [MAX] : literal replace-all of PAT in S, at most 8 replacements in the baseline pass (no bound in the relaxed rerun) -> _SG_RP; with MAX
# (characters) it stops with status 1 as soon as the result would be longer than MAX (_SG_RP is then S unchanged)
```

3. hook 头注释里「Shell variable indirection」这一条（原型 `:87-99`）整条换成：

```
#   - Shell variable indirection (`f=...; cat "$f"`) is covered only in part: literal
#     assignments are expanded in a second pass (at most 16 assignments, 8 for lists and 8
#     replacements per variable in the baseline pass; beyond those COUNTS the variable
#     passes). The SIZE of the expansion is bounded too: a value over 4096 characters, or
#     more than 65536 characters of substituted text per command, blocks the command
#     (fail-closed, owner ruling 2026-10-14). A substituted copy over 8192 characters is
#     blocked for its size only where the relaxed rerun of 10CG/aria-plugin#217 is not in
#     effect; where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL, no
#     project extension, time left), the pass is re-run under a
#     hard deadline with no count bound, the growth over the input as the limit and the
#     copy judged in full, and growth over 8192 characters, the deadline or any failure of
#     the rerun still blocks. The pass substitutes text; it does not run the shell: a
#     variable assigned twice is replaced by its FIRST value (bash reads the last), and in
#     segment mode a value holding shell syntax (`G='| jq keys'`) becomes syntax in the
#     copy, so a read can earn a filter credit that bash never applies. Both pass, in small
#     commands since the baseline and, with the rerun, in big ones (declared under owner
#     ruling A, 2026-10-23). Arrays, `read <<<`, quote-spliced paths, `cd` + a relative
#     name, globs, `set --`, `$(printf ...)` and variables across two tool calls pass;
#     the output side is left to secret-scan.sh.
```

4. 重跑块头（原型 `:792-793`，`_sg_vx_big_judge` 之前那块注释里的两行）：「`# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte. In effect only on a Linux`」与「`# build of bash 5.0-5.3 on GNU/Linux (the versions and the platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own`」换成：

```
# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte. In effect only on an x86_64
# GNU/Linux build of bash 5.0-5.3 outside WSL (the versions, architecture and platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own
```

**What 7 补充 2：TASK-005 复审指出的注释**（v3.3，2026-10-25；INV-1 允许的内容差之一。下列每处要说的意思由本节钉住，落地的逐字文本在 TASK-005 修复轮提交后回填到这里，回填前以修复轮报告为准）：

1. hook 头注释「Shell variable indirection」那条（What 7 补充 3）与套件 W10 块头：去掉「only where … not in effect」里的 only —— 放宽生效时，截止、检查点、自检等回落也按尺寸拦，重跑里还可能按 VMAX 拦（m-2 第 1 处）。
2. hook LENGTH BUDGET 块里「whenever the rerun does not finish in time」：改成「whenever the rerun neither allows nor blocks on its own (the deadline, a checkpoint, any failure)」一类的完整说法（m-2 第 2 处）。
3. `_sg_relax_noext` 的行尾注释：「or an error, keeps the relaxation off」与代码相反（取项目根出错时 `_sg_ext_root` 输出空串，本函数照样打印 none，这正是 What 1 表要的行为）。改成：项目根下的扩展文件不论什么状态都关掉放宽；找不到项目根（包括 jq 读不出 cwd）就不可能有扩展生效（m-2 第 3 处）。
4. `_sg_vx_pass` 的说明：存在 `_SG_OV_PAT` / `_SG_OV_MODE` 里的是基线的原因串与模式，不是文案（文案回落时由 `_sg_emit_blocked` 重新生成）（m-2 第 4 处）。
5. 重跑块头「an internal error, a bare 0 -- falls back to the baseline block, byte for byte」：补上 What 4 的那个例外（bash 自身致命错误以 2 退出时原样写出它的报错，仍是拦）（D-3）。
6. 准入门 WSL 那一行的注释随 What 1 补充 2 改写（代码见上）。
7. 重跑块头里与第 4 处同类的那句（「keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE」）：同样改成存的是原因与模式（TASK-005 修复轮第二段补，为不超出该段行宽写作「reason and mode」）。
8. hook 头注释「Shell variable indirection」那条：补上第 5 处的同一个例外（bash 自身致命错误以 2 退出时原样写出它的报错，仍是拦），措辞与重跑块头同义，延续该段行宽（v3.4，复审第二轮 m-2 第 2 部分）。

**落地的逐字文本**（aria `710a36d`，由 `git diff 2893bcc 710a36d -- hooks/secret-guard.sh` 机械导出，逐 hunk 列改前改后；第 6、7 处与 What 1 补充 2 的代码都在其中。v3.4 注：下面仍是 710a36d 的 v3.3 写法，与 What 1 补充 2 现行的 v3.4 代码不同是预期的；修复轮第三段提交后按新提交重新导出，覆盖本段）：

1. `-93,6 +93,9`（只有注释）

   改前：

```
#     blocked for its size only where the relaxed rerun of 10CG/aria-plugin#217 is not in
#     effect; where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL, no
#     project extension, time left), the pass is re-run under a
#     hard deadline with no count bound, the growth over the input as the limit and the
#     copy judged in full, and growth over 8192 characters, the deadline or any failure of
#     the rerun still blocks. The pass substitutes text; it does not run the shell: a
```

   改后：

```
#     blocked for its size wherever the relaxed rerun of 10CG/aria-plugin#217 is not in
#     effect, and also where it is (an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL,
#     no project extension, time left) whenever that rerun falls back. The rerun runs the
#     pass again under a hard deadline with no count bound, the growth over the input as
#     the limit and the copy judged in full: growth over 8192 characters blocks with the
#     growth text, a value over 4096 characters with the value text (the rerun reaches
#     values that the counts cut off in the baseline pass), and the deadline, a time
#     checkpoint, the self-check or any other failure of the rerun falls back to that size
#     block. The pass substitutes text; it does not run the shell: a
```

2. `-599,3 +602,4`（只有注释）

   改前：

```
# rows only: nocredit, the longline text). Elsewhere, and whenever the rerun does not finish in time, the command is blocked with the size text, byte for byte as before (the
# W9 extension's look at the substituted whole command, after the pass, blocks on such a copy only when an extension is in effect). (The COUNTS above -- 16 assignments, 8
# replacements, 8 for statements -- bound the baseline pass and still pass beyond the limit, SC-21 21y; the relaxed rerun has no count bound, the deadline caps its cost.)
```

   改后：

```
# rows only: nocredit, the longline text). Elsewhere, and whenever the rerun neither allows nor blocks on its own (the deadline, a time checkpoint, the self-check, any other
# failure), the command is blocked with the size text, byte for byte as before (the W9 extension's look at the substituted whole command, after the pass, blocks on such a
# copy only when an extension is in effect). (The COUNTS above -- 16 assignments, 8 replacements, 8 for statements -- bound the baseline pass and still pass beyond the
# limit, SC-21 21y; the relaxed rerun has no count bound, the deadline caps its cost.)
```

3. `-720,4 +724,4`（只有注释）

   改前：

```
# BLOCK (status 2). A copy over _SGV_SMAX ends the baseline pass too: with status 4 when the relaxation is in effect (_sg_relax_ok; the baseline block text is kept
# in _SG_OV_PAT / _SG_OV_MODE for the fallback), else with the oversize BLOCK. Inside the relaxed rerun (_SG_RELAXED) a growth overrun blocks with the growth text, a copy
# over _SGV_SMAX goes to _sg_vx_big_judge, and a time checkpoint returns 3 (no time text: the caller falls back to the baseline block). Nothing behind an overrun is built
# or judged.
```

   改后：

```
# BLOCK (status 2). A copy over _SGV_SMAX ends the baseline pass too: with status 4 when the relaxation is in effect (_sg_relax_ok; the baseline reason string and mode are
# kept in _SG_OV_PAT / _SG_OV_MODE -- not a text: on a fallback _sg_emit_blocked writes the baseline block text from them again), else with the oversize BLOCK. Inside the
# relaxed rerun (_SG_RELAXED) a growth overrun blocks with the growth text, a copy over _SGV_SMAX goes to _sg_vx_big_judge, and a time checkpoint returns 3 (no time text:
# the caller falls back to the baseline block). Nothing behind an overrun is built or judged.
```

4. `-792 +796`（只有注释）

   改前：

```
# returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs the W10 pass with the relaxed rules
```

   改后：

```
# returns 4 instead and keeps the baseline reason and mode in _SG_OV_PAT / _SG_OV_MODE; _sg_per_segment_eval re-runs the W10 pass with the relaxed rules
```

5. `-798,2 +802,4`（只有注释）

   改前：

```
# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte. In effect only on an x86_64
# GNU/Linux build of bash 5.0-5.3 outside WSL (the versions, architecture and platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own
```

   改后：

```
# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte. The one exception (What 4):
# a fatal error of bash itself inside the job that makes it exit with status 2 and write its error message is passed on as the block text -- the command is
# still blocked, but with bash's message instead of the baseline text. In effect only on an x86_64 GNU/Linux build of bash 5.0-5.3 outside WSL (the
# versions, architecture and platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own
```

6. `-823 +829,2`（含代码行：What 1 补充 2 的那部分以上文代码块为准）

   改前：

```
  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" || -e /proc/sys/fs/binfmt_misc/WSLInterop ]] && wsl=wsl   # WSL marks; the environment can only switch the relaxation off with them
```

   改后：

```
  [[ -n "${WSL_DISTRO_NAME:-}${WSL_INTEROP:-}" ]] && wsl=wsl   # WSL marks in the environment; the environment can only switch the relaxation off with them
  [[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl   # a WSLInterop* entry under a mounted binfmt_misc, or a mount table that cannot be read
```

7. `-831 +838,8`（含代码行：What 1 补充 2 的那部分以上文代码块为准）

   改前：

```
_sg_relax_noext() {   # prints "none" only when no extension can be in effect: no project root, or no .aria/secret-guard.paths under it. A file in any state, or an error, keeps the relaxation off
```

   改后：

```
_sg_relax_nowslfs() {   # [MOUNTS [DIR]]: status 0 only when no WSL interop entry can exist -- the mount table (default /proc/self/mounts) reads, and no binfmt_misc file system is mounted at DIR (default /proc/sys/fs/binfmt_misc), or one is and holds no entry named WSLInterop*. The entries are looked at only under a mounted binfmt_misc, so the look never triggers an automount (an autofs mount point there that nobody serves can hold a stat until the hook is killed, and a killed hook lets the command through); a mount table that cannot be read keeps the relaxation off. The two arguments exist for the direct-call cases only; the gate calls it with none
  local d="${2:-/proc/sys/fs/binfmt_misc}" l e m=0
  { while IFS= read -r l; do if [[ "$l" == *" $d binfmt_misc "* ]]; then m=1; fi; done; } 2>/dev/null < "${1:-/proc/self/mounts}" || return 1   # if, not &&: a last line that does not match must not make the loop's status 1 (that would read as an unreadable table); 2>/dev/null before <, so a table that cannot be opened writes nothing to stderr
  (( m )) || return 0
  for e in "$d"/WSLInterop*; do [[ -e "$e" ]] && return 1; done
  return 0
}
_sg_relax_noext() {   # prints "none" only when no extension can be in effect: no project root is found (_sg_ext_root prints nothing, which includes a cwd that jq cannot read: without a root no extension can be in effect), or there is no .aria/secret-guard.paths under it. A file there, in any state, keeps the relaxation off
```


用例一侧（不属 hook 的内容差）：V2-G12 / G13 的注释与 chk 文案改成只说关门一极，开门一极指向 V14-G1，编号不变（m-3）；helper 与 `v31/sc-direct.sh` 的 `nproc_binds` 快路径改用真实 UID（`id -ru`），CapEff 由 bash 自己从 `/proc/$BASHPID/status` 读（m-4）；补三条与负载无关的直调用例：计时器睡的恰是 `_SG_LEFT`、锚点 `_SG_P0` 只在 hook 起点取一次、作业的命令替换里 `exec 2>/dev/null`（m-6，写法见复审报告第 5 项）。

### 参考实现（`v31/W8-v31.diff` 的全部逻辑 hunk）

```diff
@@ -176,6 +180,7 @@
 fi
 
 set -uo pipefail   # NOT -e — we control exit codes
+_SG_P0=${EPOCHREALTIME:-}; _SG_RELAXED=   # 10CG/aria-plugin#217: hook-start anchor of the relaxed rerun's hard deadline (empty under a bash without EPOCHREALTIME: no relaxation); _SG_RELAXED is never taken from the environment
 
 # 复刻 `echo "$x" | grep -qE "$re"` 的记录语义: 按 \n 拆行, 任一行命中即真。
 # $1 = 正则 (不加引号代入 =~, 否则退化为字面匹配); $2 = 待判字符串 (段)
@@ -574,26 +579,27 @@
 # values substituted in. TEXT ONLY: prefix + suffix concatenation with the remainder taken BY LENGTH (${s:N}); no eval (a value may hold a command substitution or back
 # quotes: they must never run inside the hook), no ${s//p/r} (bash 5.2 patsub_replacement and the quote semantics of bash < 4.3 disagree about quotes and `&` in the
 # replacement), no ${s#*"$pat"} (O(n^2) when the hit sits late in a long string).
-# LENGTH BUDGET (review M6; fail-CLOSED, owner ruling 2026-10-14): without it the judged string is the segment plus references x value length, and one level of chaining
-# multiplies a value by 8, so a 5 KB command overran the 5 s hook timeout (and a timeout lets the command through). Three limits, counted in characters. Beyond ANY of them the
-# whole command is BLOCKED with a text of its own ("command too large to scan for secrets ... split it": _sg_emit_blocked with the 4th word oversize, status 2) and never
-# passed: a copy that is not judged is a way past the guard, and padding a value or a chain would be the recipe. The oversize string is never built, expanded further, judged
-# or scanned: the pass stops at the first overrun and nothing behind it is touched, so an overrun costs no more than the budgeted work in front of it (blocking is as cheap as
-# passing was; the 5 s timeout and its fail-open, 10CG/aria-plugin#216, are not touched). (The COUNTS above -- 16 assignments, 8 replacements, 8 for statements -- are another
-# bound and still pass beyond the limit, SC-21 21y.) (1) _SGV_VMAX: a value longer than that (as collected, or after chaining) blocks the
-# command whether or not the variable is mentioned: _sg_vx_collect stops at it and returns 2; 4096 is PATH_MAX, a longer value is not one path. (2) _SGV_SMAX: a substituted
-# copy (a segment, or the whole command) that would become longer blocks the command (status 2 of _sg_vx_apply; the W9 extension's look at the substituted whole command, after
-# the pass, blocks on it only when an extension is in effect -- without one nothing is left unjudged). 8192 because a BLOCK verdict costs the square of the copy length
-# (_sg_compute_credit on one long line: about 0.9 s at 8 KB, 3 s at 16 KB, 13 s at 32 KB) and a verdict that arrives after the timeout is lost. The limit counts the whole judged
-# string, not its growth: a segment (in whole-command mode: the command) over 8192 characters that mentions a collected variable is blocked however small the value is.
-# (3) _SGV_TMAX: all copies of one command together; once used up the command is blocked -- what many dense segments can cost is bounded too.
-# _sg_vx_collect, _sg_vx_apply and _SG_SUB are names of the contract, like _sg_vx_pass: the budget probes of the suite use them.
+# LENGTH BUDGET (review M6; fail-CLOSED, owner ruling 2026-10-14; narrowed by 10CG/aria-plugin#217): without it the judged string is the segment plus references x value
+# length, and one level of chaining multiplies a value by 8, so a 5 KB command overran the 5 s hook timeout (and a timeout lets the command through). Three limits, counted in
+# characters. (1) _SGV_VMAX: a value longer than that (as collected, or after chaining) blocks the command whether or not the variable is mentioned: _sg_vx_collect stops at it
+# and returns 2; 4096 is PATH_MAX, a longer value is not one path. (3) _SGV_TMAX: all copies of one command together; once used up the command is blocked -- what many dense
+# segments can cost is bounded too. Both block with a text of their own ("command too large to scan for secrets ... split it": _sg_emit_blocked with the 4th word oversize,
+# status 2), and the oversize string is never built, expanded further, judged or scanned. (2) _SGV_SMAX: a substituted copy (a segment, or the whole command) that would become
+# longer than 8192 characters ends the baseline pass at that copy (status 2 of _sg_vx_apply), because a BLOCK verdict costs the square of the copy length (_sg_compute_credit on
+# one long line: about 0.9 s at 8 KB, 3 s at 16 KB, 13 s at 32 KB) and a verdict that arrives after the 5 s timeout is lost. What follows depends on _sg_relax_ok: where the
+# relaxation is in effect, _sg_vx_pass returns status 4 and _sg_per_segment_eval re-runs the pass in a background job under a hard deadline (_sg_relax_run); there the copy
+# limit is the growth over the input (_SGV_GMAX), and a copy over 8192 characters is judged in full by _sg_vx_big_judge (a line longer than _SGV_LMAX is matched against the
+# rows only: nocredit, the longline text). Elsewhere, and whenever the rerun does not finish in time, the command is blocked with the size text, byte for byte as before (the
+# W9 extension's look at the substituted whole command, after the pass, blocks on such a copy only when an extension is in effect). (The COUNTS above -- 16 assignments, 8
+# replacements, 8 for statements -- bound the baseline pass and still pass beyond the limit, SC-21 21y; the relaxed rerun has no count bound, the deadline caps its cost.)
 _SGV_N=(); _SGV_V=()
 _SG_SUB=""
 _SG_RP=""
 _SGV_VMAX=4096
 _SGV_SMAX=8192
 _SGV_TMAX=65536
+_SGV_GMAX=8192   # 10CG/aria-plugin#217 relaxed rerun: a copy may grow by at most this many characters over its input
+_SGV_LMAX=8192   # 10CG/aria-plugin#217 relaxed rerun: a copy over _SGV_SMAX whose longest line is longer than this is matched against the rows only (nocredit)
 # ── Time-budget fail-closed (secret-guard-time-budget-failclosed C; resolves 10CG/aria-plugin#216) ──
 # Claude Code kills a PreToolUse hook at 5 s and then FAIL-OPENS (lets the command through, UNSCANNED). The expensive second pass (W10 variable expansion) and the W9 extension
 # look can, on a slow platform (Windows MINGW64 measured ~2.6x Linux, #219), run past 5 s on a command that is still within the SIZE budget (_SGV_*). So the guard keeps its OWN
@@ -619,9 +626,10 @@
 # _sg_vx_replace S PAT REP [MAX] : literal replace-all of PAT in S, at most 8 replacements -> _SG_RP; with MAX (characters) it stops with status 1 as soon as the result would be
 # longer than MAX (_SG_RP is then S unchanged)
 _sg_vx_replace() {
-  local s="$1" pat="$2" rep="$3" max="${4:-0}" out="" g=0 pre
+  local s="$1" pat="$2" rep="$3" max="${4:-0}" out="" g=0 pre gc=8
+  [[ -n "${_SG_RELAXED:-}" ]] && gc=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound
   _SG_RP="$s"
-  while (( g < 8 )) && [[ "$s" == *"$pat"* ]]; do
+  while (( g < gc )) && [[ "$s" == *"$pat"* ]]; do
     g=$((g+1)); pre="${s%%"$pat"*}"; out="${out}${pre}${rep}"; s="${s:$(( ${#pre} + ${#pat} ))}"
     (( max > 0 && ${#out} + ${#s} > max )) && return 1
   done
@@ -631,12 +639,13 @@
 # value at once -- the value is neither stored nor looked at again and nothing behind it is collected -- and the caller blocks the command.
 _sg_vx_collect() {
   _SG_T0=$SECONDS; _sg_time_budget   # reset the time-budget clock + resolve the budget once here: the single choke point every expensive leg (this collect's i×j chaining, _sg_vx_pass, the W9 extension look) passes first
-  local rest="$1" m name val i j n=0 dup pre
+  local rest="$1" m name val i j n=0 dup pre ca=16 cf=8
+  [[ -n "${_SG_RELAXED:-}" ]] && ca=1000000 cf=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound (the deadline caps the cost)
   local _q="'" _d='"' _b='`'
   _SGV_N=(); _SGV_V=()
   [[ "$rest" == *'$'* && "$rest" == *=* ]] || [[ "$rest" == *'$'* && "$rest" == *' in '* ]] || return 0
   local re="(^|[;&|[:space:](${_d}${_b}${_q}])((export|declare|local|readonly|typeset)[[:space:]]+(-[a-zA-Z]+[[:space:]]+)*)?([A-Za-z_][A-Za-z0-9_]*)=(${_d}([^${_d}]*)${_d}|${_q}([^${_q}]*)${_q}|\\\$\\([^)]*\\)|${_b}[^${_b}]*${_b}|[^[:space:];&|)${_d}${_b}${_q}]*)"
-  while (( n < 16 )) && [[ "$rest" =~ $re ]]; do
+  while (( n < ca )) && [[ "$rest" =~ $re ]]; do
     (( n += 1 ))
     m="${BASH_REMATCH[0]}"; name="${BASH_REMATCH[5]}"; val="${BASH_REMATCH[6]}"
     pre="${rest%%"$m"*}"; rest="${rest:$(( ${#pre} + ${#m} ))}"
@@ -652,7 +661,7 @@
   done
   rest="$1"; n=0
   local rf="(^|[;&|[:space:](])for[[:space:]]+([A-Za-z_][A-Za-z0-9_]*)[[:space:]]+in[[:space:]]+([^;&|)]*)"
-  while (( n < 8 )) && [[ "$rest" =~ $rf ]]; do
+  while (( n < cf )) && [[ "$rest" =~ $rf ]]; do
     (( n += 1 ))
     m="${BASH_REMATCH[0]}"; name="${BASH_REMATCH[2]}"; val="${BASH_REMATCH[3]}"
     pre="${rest%%"$m"*}"; rest="${rest:$(( ${#pre} + ${#m} ))}"
@@ -671,27 +680,29 @@
   done
   return 0
 }
-# _sg_vx_apply S : S with the collected values substituted -> _SG_SUB. Status 0 = a copy was built, 1 = nothing to substitute, 2 = the copy would be longer than _SGV_SMAX (not
-# built, _SG_SUB stays S; the caller blocks the command). Per variable: ${NAME} through _sg_vx_replace, then $NAME with the same prefix accumulation (the already substituted text is never scanned again;
-# the remainder keeps the character that ended the match, so $f$f works), at most 8 times.
+# _sg_vx_apply S : S with the collected values substituted -> _SG_SUB. Status 0 = a copy was built, 1 = nothing to substitute, 2 = the copy would be over the limit (not
+# built, _SG_SUB stays S; the caller decides): the limit is _SGV_SMAX in the baseline pass and the input length + _SGV_GMAX in the relaxed rerun (_SG_RELAXED). Per
+# variable: ${NAME} through _sg_vx_replace, then $NAME with the same prefix accumulation (the already substituted text is never scanned again; the remainder keeps the
+# character that ended the match, so $f$f works), at most 8 times in the baseline pass and with no count bound in the relaxed rerun.
 _sg_vx_apply() {
-  local s="$1" i n v m tail pre out guard changed=1
+  local s="$1" i n v m tail pre out guard changed=1 lim=$_SGV_SMAX gc=8
+  [[ -n "${_SG_RELAXED:-}" ]] && lim=$(( ${#1} + _SGV_GMAX )) gc=1000000   # 10CG/aria-plugin#217 relaxed rerun: the limit is the growth over the input (${#1}: s is rewritten below)
   _SG_SUB="$s"
   (( ${#_SGV_N[@]} )) || return 1
   [[ "$s" == *'$'* ]] || return 1
   for (( i = 0; i < ${#_SGV_N[@]}; i++ )); do
     n="${_SGV_N[i]}"; v="${_SGV_V[i]}"
     [[ -n "$v" ]] || continue
-    if [[ "$s" == *"\${$n}"* ]]; then _sg_vx_replace "$s" "\${$n}" "$v" "$_SGV_SMAX" || return 2; s="$_SG_RP"; changed=0; fi
+    if [[ "$s" == *"\${$n}"* ]]; then _sg_vx_replace "$s" "\${$n}" "$v" "$lim" || return 2; s="$_SG_RP"; changed=0; fi
     out=""; guard=0
-    while (( guard < 8 )) && [[ "$s" =~ \$${n}([^A-Za-z0-9_]|$) ]]; do
+    while (( guard < gc )) && [[ "$s" =~ \$${n}([^A-Za-z0-9_]|$) ]]; do
       (( guard += 1 ))
       m="${BASH_REMATCH[0]}"; tail="${BASH_REMATCH[1]}"
       if [[ -z "$tail" ]]; then pre="${s%"$m"}"; else pre="${s%%"$m"*}"; fi
       s="${s:$(( ${#pre} + ${#m} - ${#tail} ))}"
       [[ "$pre" == *\\ ]] && pre="${pre%\\}"
       out="${out}${pre}${v}"; changed=0
-      (( ${#out} + ${#s} > _SGV_SMAX )) && return 2
+      (( ${#out} + ${#s} > lim )) && return 2
     done
     (( guard )) && s="${out}${s}"
   done
@@ -699,13 +710,17 @@
   return $changed
 }
 # _sg_vx_pass CMD MODE : the second pass -- judge the substituted copies. MODE is whole or segment, as _sg_core_eval left it in _SG_MODE (in segment mode _SG_SEGS holds
-# the segments). The function name is a contract: the fault-injection and evaluation-order probes locate it by name. An overrun of the length budget (a value, a copy, the total)
-# ends the pass at once with an oversize BLOCK (the size text of _sg_emit_blocked, status 2): nothing behind the overrun is built or judged.
+# the segments). The function name is a contract: the fault-injection and evaluation-order probes locate it by name. A value or total overrun stops the pass with an oversize
+# BLOCK (status 2). A copy over _SGV_SMAX ends the baseline pass too: with status 4 when the relaxation is in effect (_sg_relax_ok; the baseline block text is kept
+# in _SG_OV_PAT / _SG_OV_MODE for the fallback), else with the oversize BLOCK. Inside the relaxed rerun (_SG_RELAXED) a growth overrun blocks with the growth text, a copy
+# over _SGV_SMAX goes to _sg_vx_big_judge, and a time checkpoint returns 3 (no time text: the caller falls back to the baseline block). Nothing behind an overrun is built
+# or judged.
 _sg_vx_pass() {
   local cmd="$1" mode="$2" seg rc ar cr spent=0
   _sg_vx_collect "$cmd"
   cr=$?
   if [[ $cr -eq 3 ]]; then   # time-budget fail-closed: the chaining in _sg_vx_collect ran out of time
+    [[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block
     _sg_emit_blocked "time" "$cmd" "$mode" timeout
     return 2
   fi
@@ -716,20 +731,30 @@
   (( ${#_SGV_N[@]} )) || return 0
   if [[ "$mode" == whole ]]; then
     if _sg_over_budget; then   # time-budget fail-closed before the O(copy^2) whole-command judgement
+      [[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block
       _sg_emit_blocked "time" "$cmd" whole timeout
       return 2
     fi
     _sg_vx_apply "$cmd"
     ar=$?
     if [[ $ar -eq 2 ]]; then
+      if [[ -n "${_SG_RELAXED:-}" ]]; then
+        _sg_emit_blocked "the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" whole oversize
+        return 2
+      fi
+      if _sg_relax_ok; then _SG_OV_PAT="the command is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=whole; return 4; fi
       _sg_emit_blocked "the command is longer than $_SGV_SMAX characters after variable expansion" "$cmd" whole oversize
       return 2
     fi
-    if [[ $ar -eq 0 ]]; then _sg_judge_one "$_SG_SUB" whole; return $?; fi
+    if [[ $ar -eq 0 ]]; then
+      if [[ -n "${_SG_RELAXED:-}" ]] && (( ${#_SG_SUB} > _SGV_SMAX )); then _sg_vx_big_judge "$_SG_SUB" whole; return $?; fi
+      _sg_judge_one "$_SG_SUB" whole; return $?
+    fi
     return 0
   fi
   for seg in "${_SG_SEGS[@]}"; do
     if _sg_over_budget; then   # time-budget fail-closed before each per-segment _sg_vx_apply / _sg_judge_one (the O(copy^2) hot leg)
+      [[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block
       _sg_emit_blocked "time" "$cmd" segment timeout
       return 2
     fi
@@ -737,6 +762,11 @@
     ar=$?
     [[ $ar -eq 1 ]] && continue
     if [[ $ar -eq 2 ]]; then
+      if [[ -n "${_SG_RELAXED:-}" ]]; then
+        _sg_emit_blocked "a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize
+        return 2
+      fi
+      if _sg_relax_ok; then _SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4; fi
       _sg_emit_blocked "a command segment is longer than $_SGV_SMAX characters after variable expansion" "$cmd" segment oversize
       return 2
     fi
@@ -745,13 +775,84 @@
       _sg_emit_blocked "the command segments together are longer than $_SGV_TMAX characters after variable expansion" "$cmd" segment oversize
       return 2
     fi
-    _sg_judge_one "$_SG_SUB" segment
+    if [[ -n "${_SG_RELAXED:-}" ]] && (( ${#_SG_SUB} > _SGV_SMAX )); then _sg_vx_big_judge "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi
     rc=$?
     [[ $rc -ne 0 ]] && return "$rc"
   done
   return 0
 }
 
+# 10CG/aria-plugin#217 relaxed rerun. When the relaxation is in effect (_sg_relax_ok), a copy over _SGV_SMAX is not blocked for its size alone: _sg_vx_pass
+# returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs the W10 pass with the relaxed rules
+# (_SG_RELAXED: the copy limit is the growth over the input, _SGV_GMAX; a copy over _SGV_SMAX is judged in full, _sg_vx_big_judge; the counts -- 16
+# assignments, 8 for statements, 8 replacements per variable -- are not bounded, so every reference is expanded) in a background job under a HARD
+# deadline: _SG_P0 (hook start) + min(_SG_TIME_BUDGET, 3) s. The job leads its own process group (set -m); its timer runs inside the group and is started
+# before the first expensive step; the deadline kills the whole group, and so does _sg_relax_run once the job has ended, so nothing of the job outlives it
+# or holds the pipe. The verdict is the job's exit status, never parsed from text: 77 allows, 2 blocks with the job's own text; any other outcome -- the
+# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte. In effect only on a Linux
+# build of bash 5.0-5.3 on GNU/Linux (the versions and the platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own
+# absolute limit anyway), and with time left before the deadline.
+_sg_vx_big_judge() {   # COPY MODE: the longest line (one linear read loop) routes the copy -- longer than _SGV_LMAX: rows only, no credit; otherwise the normal judgement
+  local line max=0 seen=0
+  while IFS= read -r line; do seen=1; (( ${#line} > max )) && max=${#line}; done <<< "$1"
+  (( seen )) || max=$(( _SGV_LMAX + 1 ))   # the length could not be measured: rows only, never the cheaper-to-pass credit path
+  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit; else _sg_judge_one "$1" "$2"; fi
+}
+_sg_relax_left() {   # sets _SG_LEFT to the time left before the deadline, as seconds with 6 decimals; status 1 when there is no anchor or no time left
+  local now p0 cap
+  [[ -n "${_SG_P0:-}" && -n "${EPOCHREALTIME:-}" ]] || return 1
+  _sg_time_budget
+  now=${EPOCHREALTIME/[.,]/}; p0=${_SG_P0/[.,]/}
+  [[ "$now" =~ ^[0-9]+$ && "$p0" =~ ^[0-9]+$ ]] || return 1
+  cap=$(( _SG_TIME_BUDGET < 3 ? _SG_TIME_BUDGET : 3 ))
+  now=$(( 10#$p0 + cap * 1000000 - 10#$now ))
+  (( now > 0 )) || return 1
+  (( now > cap * 1000000 )) && now=$(( cap * 1000000 ))   # a clock that went backwards never extends the deadline
+  printf -v _SG_LEFT '%d.%06d' $(( now / 1000000 )) $(( now % 1000000 ))
+}
+_sg_relax_ok() {   # status 0 when the relaxation is in effect for this command; the extension is asked inside a command substitution, like every extension call
+  [[ -z "${_SG_RELAXED:-}" ]] || return 1
+  _sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}" "${BASH_VERSINFO[1]:-0}" || return 1   # read-only build facts, which the environment cannot rewrite (OSTYPE can be)
+  _sg_relax_left || return 1
+  [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]
+}
+_sg_relax_platform() {   # MACHINE MAJOR MINOR: status 0 on a GNU/Linux build of a bash version the mechanism was measured on, 5.0 to 5.3 (owner ruling E: an untested platform -- macOS, Windows, musl, Android, another bash -- keeps the baseline)
+  [[ "$1" == *-linux-gnu* ]] && (( ${2:-0} == 5 && ${3:-0} <= 3 ))
+}
+_sg_relax_noext() {   # prints "none" only when no extension can be in effect: no project root, or no .aria/secret-guard.paths under it. A file in any state, or an error, keeps the relaxation off
+  local root
+  root="$(_sg_ext_root)"
+  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi
+}
+_sg_relax_job() {   # CMD: body of the background job; refuses to judge (status 9) unless it leads its own process group, which is what the deadline kills
+  local st f
+  { IFS= read -r st < "/proc/$BASHPID/stat"; } 2>/dev/null || return 9
+  st="${st##*) }"; f=( $st )
+  [[ "${f[2]:-}" == "$BASHPID" ]] || return 9
+  local me=$BASHPID tp
+  ( sleep "$_SG_LEFT"; kill -KILL -- "-$me" ) >/dev/null 2>&1 </dev/null &
+  tp=${!:-}
+  [[ -n "$tp" ]] && kill -0 "$tp" 2>/dev/null || return 9   # no running timer, no judgement: the deadline must exist before the first expensive step
+  _SG_RELAXED=1
+  _sg_vx_pass "$1" "$_SG_MODE"
+  case $? in 0) return 77 ;; 2) return 2 ;; *) return 1 ;; esac   # allow only as 77: a bare 0 reaching _sg_relax_run from anywhere else falls back
+}
+_sg_relax_run() {   # CMD: status 0 = allowed (the job exited 77), 2 = blocked (the job exited 2 with a text, now on stderr), 4 = fall back to the baseline block
+  local out rc
+  _sg_relax_left || return 4
+  out="$( exec 2>/dev/null; set -m
+          _sg_relax_job "$1" 2>&1 </dev/null &
+          jp=${!:-}
+          [[ -n "$jp" ]] || exit 99
+          wait "$jp"; r=$?
+          kill -KILL -- "-$jp"   # the timer and anything the judgement left behind: nothing of the job outlives it or holds the pipe
+          exit "$r" )"
+  rc=$?
+  [[ $rc -eq 77 ]] && return 0
+  [[ $rc -eq 2 && -n "$out" ]] && { printf '%s\n' "$out" >&2; return 2; }
+  return 4
+}
+
 # W9 -- project-level extension <project root>/.aria/secret-guard.paths: one LITERAL substring per line; it can only ADD blocks (the built-in verdict always comes first).
 # ALL extension code lives in _sg_ext_* functions that are called ONLY through command substitution $( ... ): an internal error (set -u, exit, command not found) kills
 # that subshell alone, and the caller treats every output other than the literal sentinel BLOCK as "extension not in effect". The built-in verdict and its fail-closed
@@ -866,6 +968,26 @@
 EOF
     return 0
   fi
+  if [[ "$kind" == longline ]]; then
+    cat >&2 <<EOF
+[secret-guard] BLOCKED: command reads a secret-bearing source, and after variable
+expansion it has a line longer than ${_SGV_LMAX} characters. Matched pattern: $pat
+
+At this size the guard does not look for value-REDACTING filters (| jq 'keys',
+| wc -c, >/dev/null, ...): on a line this long that check alone is too slow to
+finish within the hook's time limit, so the match alone blocks the command
+(fail-closed).
+
+Split it into smaller commands and run them one at a time:
+  - keep every variable value, and every command after expansion, short;
+  - do not repeat one long \$VAR many times in a single command;
+  - write long files with the Write / Edit tool instead of a heredoc.
+命令读取含密钥的来源, 且变量展开后有超长的行, 这个尺寸下不评估脱敏过滤, 请拆成更小的命令
+
+Command was (first 200 characters): $(_sg_redact_echo "${command:0:200}")
+EOF
+    return 0
+  fi
   cat >&2 <<EOF
 [secret-guard] BLOCKED: command reads a secret-bearing source without a
 value-REDACTING filter. Matched pattern: $pat
@@ -1491,11 +1613,14 @@
 
 # _sg_judge_one() — evaluate one string (whole command in "whole" mode, or one
 # top-level segment in "segment" mode) against risky_patterns + credit. $1 =
-# string to judge, $2 = mode (whole|segment). Returns 0 = allow, 2 = blocked
-# (BLOCKED message already written to stderr; mode=whole reproduces canonical
-# stderr byte-for-byte, zero new lines).
+# string to judge, $2 = mode (whole|segment), $3 = nocredit or empty: with
+# nocredit (10CG/aria-plugin#217: a big copy with a line longer than _SGV_LMAX)
+# a matched row blocks at once with the longline text and credit is not
+# evaluated; the W12 neutralisation still runs first. Return 0 = allow,
+# 2 = blocked (BLOCKED message already written to stderr; mode=whole reproduces
+# canonical stderr byte-for-byte, zero new lines).
 _sg_judge_one() {
-  local seg="$1" mode="$2" pat
+  local seg="$1" mode="$2" pat nocredit="${3:-}"
   local credit="" subj="$1" _w
   # W12 (secret-net-l3-and-bypass-paths): an os.environ single-key read (.environ.get( / .environb.get( / .environ[ / .environb[) is the same information as the
   # allowed os.getenv, but its `.env` prefix trips the interpreter rows. Every occurrence of the four literal substrings is cut out of the COPY that is
@@ -1510,6 +1635,10 @@
   fi
   for pat in "${risky_patterns[@]}"; do
     if [[ "$subj" =~ $pat ]]; then
+      if [[ "$nocredit" == nocredit ]]; then   # 10CG/aria-plugin#217: a big copy with a line longer than _SGV_LMAX -- the match alone blocks, credit is not evaluated
+        _sg_emit_blocked "$pat" "$seg" "$mode" longline
+        return 2
+      fi
       if [[ -z "$credit" ]]; then
         if _sg_compute_credit "$seg"; then credit=1; else credit=0; fi
       fi
@@ -1543,6 +1675,12 @@
   if [[ "$_SG_MODE" != none ]]; then
     _sg_vx_pass "$cmd" "$_SG_MODE"
     rc=$?
+    if [[ $rc -eq 4 ]]; then   # 10CG/aria-plugin#217: a copy over _SGV_SMAX and the relaxation is in effect -> the relaxed rerun decides; any failure falls back to the baseline block
+      _sg_relax_run "$cmd"
+      rc=$?
+      [[ $rc -eq 4 ]] && { _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 2; }
+      return "$rc"   # 0 also skips the extension look below: the relaxation is in effect only when no extension is
+    fi
     [[ $rc -ne 0 ]] && return "$rc"
   fi
   _x="$( _sg_ext_pass "$cmd" 2>/dev/null )"
```

（共 18 个 hunk：14 个逻辑 hunk 全部列在上面，4 个只改注释的 hunk 见 What 7。）

## 性质（P）与放宽面

| | 性质 | 证据（`v31/W13-sc-cases.txt` 的用例；其余 W 文件在 `v31/`） |
|---|---|---|
| P1 | 不在两个触发点上的命令，退出码与 stderr 与基线逐字节相同 | `V1-E16-*`；W9（旧套件只有 6 组变化；W9 是非 git 副本，SC-8 与 SC-9a 没跑，6 组只对其余用例成立）；W12 第 2 节（真实流量 300 条） |
| P2 | 准入门任一条不成立，与基线逐字节相同；放宽规则只在作业里生效，环境变量打不开它 | `V2-G*`、`V2-E6`–`V2-E9`；W13 第 1 节 bash 3.2 一轮；W12 第 3 节 |
| P3 | 放宽重跑不越过截止：hook 在 max(T_trigger, `_SG_P0` + min(预算, 3) s) + ε 内结束 | `V3-S4`、`V3-G9`、`V3-G10`、`V3-E3`–`V3-E5`、`V2-E7`；W12 第 1 节（138 条逐条对上界） |
| P4 | 结论只取作业退出码：77 放行，2 且有文本按文本拦，其余一律回落 | `V4-S1`–`V4-S3`、`V4-S6`–`V4-S8`、`V4-S11` |
| P5 | 作业的任何后代都不会活过 `_sg_relax_run`，也不占管道；计时器没起来就不判定；`sleep` 失败时计时器立即杀组 | `V5-S5`、`V5-S9`、`V5-S10`–`V5-S10d`、`V5-S12`、`V5-S13`、`V5-S13b`、`V5-S14` |
| P6 | 回落文案与基线逐字节相同 | `V6-E2`、`V3-E3`–`V3-E5`、`V2-E6`、`V2-E7` |
| P7 | 放宽判定就是普通判定；按**副本**的最长行路由，最长行 > 8192 时只匹配规则（`longline`） | `V7-E1`、`V7-E13`–`V7-E15`、`V7-N5`；W9（21ab、21ac、21al、21ao → `longline`）；W12 第 1 节 |
| P8 | 增长 > 8192 仍拦，按输入长度量，两种引用拼写一致 | `V8-D1`–`V8-D3`；W9（21ag、21aj → 增长文案） |
| P9 | VMAX、TMAX 不变；基线那一遍的计数上限不变；重跑里没有计数上限 | `V9-E11`、`V9-E12`、`V9-C1`、`V9-C1b`、`V9-C2`、`V9-C2b`、`V9-E10`；W9（21ad、21y、21y2 不变） |
| P10 | `nocredit` 路径仍先做 W12 中和，只有一份规则循环 | `V10-N1`–`V10-N4`、`V11-S4` |

**放宽了什么**（CHANGELOG 申报）：

- R-a：代入后副本 > 8192、但增长不超过 8192 的命令，改为完整判定。没有规则命中、或 credit 成立，就放行。判定沿用现有语义，所以判定语义上的既有缺口覆盖到更多大命令：块结构命令整串判定、命令里任一处脱敏过滤（比如无关位置的 `>/dev/null`）都会给整份副本 credit（`10CG/aria-plugin#139`；`.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/evidence/E11-real-traffic.txt`：超过 4 KB 的真实命令里，整串模式靠 credit 放行的有 71 条，是基线已放行的命令）；`10CG/aria-plugin#138`、`10CG/aria-plugin#140`、`10CG/aria-plugin#141`、`10CG/aria-plugin#142`、`10CG/aria-plugin#229` 同理。另有两类 W10 自身的代入语义缺口（post_planning R2 PP2-S；owner 2026-10-23 裁定点名申报，Decision 20）：同名变量赋值两次时，代入用第一个值，bash 读的是后一个；分段模式下，值里的 shell 语法（如 `G='| jq keys'`）代入后成了语法，读取段因此得到一个 bash 并不施加的过滤 credit。两类在小命令上基线就放行；在大命令上基线按尺寸拦，现在放行。载体见残余 8。
- R-b：缩短类，即原串或中间副本 > 8192、最终副本 ≤ 8192。按普通判定，同样受 R-a 的 credit 语义约束。R2 的 TL2-F4 构造：读一个凭据形路径，另有一处无关的 `echo done >/dev/null`，基线按尺寸拦，现在放行，凭据会被读出（W11 shrink）。这正是裁定 A 的字面：「只因尺寸被拦」的命令改为完整判定、按结果判。
- R-c：这类命令被拦时，文案由「过大」变为增长、TMAX、VMAX、`longline` 或普通命中文案（VMAX 一类 2026-10-25 补，TASK-005 m-1）。普通命中文案照基线打印整条命令（经 `_sg_redact_echo`），大命令的拦截文本会更长。
- count 轴：大命令在重跑里没有计数上限，读取藏在第 9 个引用之后也会被看到（TL 的构造：基线按尺寸拦，v3 放行，v3.1 按普通命中拦，`V9-E10`）。所以放宽**没有**把 count 轴的既有缺口带到大命令上；小命令一侧的缺口不变，见残余。

**仍然拦**：增长 > 8192；任一值 > 4096（是否被引用都拦）；分段副本总和 > 65536；超长单行命中规则；放宽重跑没在截止前完成；准入门不成立时的一切基线拦截。

**残余（不在本变更内；载体已于 2026-10-24 在 TASK-001 定，见各条）**：

1. 首遍不计时：`10CG/aria-plugin#228`。
2. ≤ 8192 的判定只受协作式时间预算约束，单次判定可以超过 5 s（R2 TL2-F5：一个 8 KB、4000 行、需要算 credit 的副本，基线 e2e 7–19 s 并放行）。这是基线已有的 fail-open，与 `10CG/aria-plugin#228` 同类，记在它的留言里；v1.76.1 CHANGELOG 的「永不 fail-open」对它不成立，本次 CHANGELOG 订正。
3. count 轴，小命令一侧：第 17 个赋值、每个变量第 9 次引用、第 9 个 for 不收集也不代入，读取藏在它们后面就看不到（基线已有，`10CG/aria-plugin#217` 正文建议暂不改）。载体：`10CG/aria-plugin#231`。
4. `10CG/aria-plugin#217` 第 2 项（for 列表止于换行）：撤下（Decision 10），续行感知转 `10CG/aria-plugin#231`。
5. `_sg_vx_collect` 把 heredoc 正文里形似赋值的文本当成 shell 赋值（Decision 9）；载体 `10CG/aria-plugin#231`。
6. 裁定 E 的放开：macOS、Windows、musl 等平台要放宽，先要一个不依赖 `/proc` 的组长自检与实测；aarch64 等其他架构与 WSL（WSL1、WSL2）要放宽，先要在该平台上实测（What 1 补充）。记在 `10CG/aria-plugin#219` 的留言里（与它的「仅 Linux 验证」同类）。
7. 评论 28512 第 2 点（扩展项目整串口径）：已评估，维持扩展的绝对尺寸门；放宽对扩展项目不生效。
8. 两类既有代入语义缺口（重复赋值时首值胜出；分段模式下值里的 shell 语法被代入），见 R-a。小命令与大命令一并修，载体 `10CG/aria-plugin#231`。
9. 截止之后的收尾 ε 随负载增长，hook 启动之前的 shell 启动时间不在耗时上界里（PP2-m6）；重跑的计数上限实为 1,000,000，到顶静默止步，几 MB 以下的命令到不了（PP2-m16）。

## Owner 裁定点

| | 内容 | 裁定 |
|---|---|---|
| A | 大而不膨胀的命令：由「一律拦」改为「完整判定后按结果判」 | 放宽（2026-10-21） |
| B | 时间护栏：判定来不及完成就拦 | 保留 fail-closed（2026-10-21）。实现是硬截止作业 + 回落基线拦截，姿态不变 |
| C | 代入后有超长单行（> 8192）又命中规则：不评估脱敏过滤，直接拦 | 保留 fail-closed（2026-10-21） |
| D | 放行未被引用的超大值 | 撤回（2026-10-21，Decision 9） |
| E | 硬截止未实测的平台（Windows、macOS 等） | 维持基线拦（2026-10-22）；实测通过后另行放开。v3.1 按同一原则把范围落到实测过的 GNU/Linux bash 5.0–5.3（Decision 16）；2026-10-23 再收紧到实测过的 x86_64，WSL（WSL1、WSL2）一律维持基线（What 1 补充，Decision 21） |
| — | post_spec 闸门 | R2 结论下由 owner 关闭（2026-10-22，`overridden_by_user: true`）；A.2 与 post_planning 照配置跑。post_implementation 与 pre_merge 在配置里是关的，代码阶段的复核由 TASK-003、TASK-005 自愿补上 |
| — | post_planning 闸门 | R2 结论下由 owner 关闭（2026-10-23，`overridden_by_user: true`），走实现优先（Decision 19） |
| — | 两类既有代入语义缺口（R2 PP2-S） | 点名申报（2026-10-23，Decision 20） |

**主控按技术决定处理、已向 owner 通报的**（owner 可随时改判）：

1. PP1-A1 count 轴：TL 席把它定为 owner 的姿态题，给了「申报放行」与「计数触顶即回落」两个选项。主控取第三种（Decision 14）：重跑里取消计数上限，判定完整后按结果判。这是裁定 A 的字面，判不完就回落拦截（裁定 B）。与 v3 相比，大多数情形是多拦：藏在第 9 个引用之后的读取被看到。也有反方向的个例：脱敏过滤（如 `>/dev/null`）藏在第 9 个引用之后时，v3 看不到它、照拦，v3.1 看到它、给 credit 后放行——这与小命令的判定完全一致，属 R-a 申报的 credit 语义（`10CG/aria-plugin#139`），不是新的一类。真实流量收益：v3 137 条，「触顶即回落」73 条（post_planning R1 汇总「主控核验与补充」PP1-A1 行，主控在 v3 原型的变体上重放；原始输出未入库），v3.1 见 W12 第 1 节。
2. 放行用专用退出码 77（Decision 15）、bash 版本只认实测过的 5.0–5.3（Decision 16）：都是 fail-closed 方向的编码与范围限定。post_planning R2 五席对 Decision 14–16 的技术挑战无异议。

**Rule #6 块 B**（v3.2 改判，技术判定，已通报 owner）：AI 可见的新文字（`longline` 描述句、两条增长原因串）与路由带来的文案变化落在 SOT §2 的「拿不准」格。v3.1 先按第 1 行豁免、待复议，声称的逐字断言其实不存在（post_planning R2 PP2-T）。v3.2 改按第 3 行三件套处理：点名行为（见 `rule6_note`）；可证伪的定向 fixture（`V11-S3`，加上 TASK-002 补的逐字断言，R2 的 KM-M1–M3、M6 必须在其上变红）；「AB 套件不覆盖 hook 文案」的 issue 已开（`10CG/Aria#261`）。三件缺一，照跑。

## Success Criteria

**验收就是代码**（Decision 17）：`v31/sc-cases.sh <hook>` 把每条性质写成可执行用例，分三类：

- **直调**（`v31/sc-direct.sh`，在被测的 bash 里 source hook）：准入门、截止值、桩判定下的作业机制（截止 1 s）、增长与计数、只匹配规则路径。
- **端到端**：用被测的 bash 执行 hook，输入是 JSON，与 Claude Code 的调用方式相同。要比对字节的用例，同一输入在基线上也跑一遍；下界来自 `v31/shim/` 注入的固定延迟——`jq` 的首次调用（stdin 解析，在锚点之后、触发点之前）与 `sed` 的首次调用（作业里第一份拦截文案的命令回显）——与负载无关。上界与「重跑须在截止前跑完」类用例依赖本机速度：负载 8–12 下，未改动的原型也会红（post_planning R2 PP2-A、PP2-B）。这批用例按 INV-7 在低负载下跑，TASK-002 给它们加负载门与单独的 SKIP 计数（PP1-A5、A8 未收口的部分）。
- **静态**：新函数都在 source 闸门之上（INV-4）；`longline` 的指令行与 oversize 逐字相同；规则循环只有一份；hook 注释块级核对。

被测的 bash 决定期望值：x86_64 GNU/Linux（不在 WSL 里）上的 5.0–5.3 期望放宽生效（原型与 `v31/sc-cases.sh` 仍按收紧前的 `*-linux-gnu*`，TASK-002 随 What 1 补充一起改）；其他任何 bash 期望准入门关闭、端到端结局与基线逐字节相同（PP1-A13）。

**W13 的结果**（`v31/W13-sc-cases.txt`）：

| 被测 hook × bash | 结果 |
|---|---|
| v3.1 原型 × bash 5.0.18（期望放宽：是） | PASS 94、FAIL 0、SKIP 0 |
| v3.1 原型 × bash 5.1.16（期望放宽：是） | PASS 94、FAIL 0、SKIP 0 |
| v3.1 原型 × bash 5.2.15（期望放宽：是） | PASS 94、FAIL 0、SKIP 0 |
| v3.1 原型 × bash 5.3.20（期望放宽：是） | PASS 94、FAIL 0、SKIP 0 |
| v3.1 原型 × bash 3.2.57（期望放宽：否） | PASS 57、FAIL 0、SKIP 0 |
| 基线 × bash 5.2（基线作为被测 hook） | PASS 19、FAIL 73：FAIL 的即基线红集，PASS 的是回归闸（P1 抽样、VMAX、基线那一遍的计数上限等），明细见 W13 第 2 节 |
| 23 个坏实现 × bash 5.2 | 23 个被各自的指定用例全部抓住，0 个漏网（下表） |

W13 的 SKIP 目前恒为 0：没有任何用例会 SKIP。TASK-002 加入负载门与 root 探测之后，这个计数才有意义（PP2-m24）。

| SC | 性质 | 用例（`v31/sc-cases.sh` 编号） | 必须抓住的坏实现 |
|---|---|---|---|
| SC-V1 | P1 | `V1-E16-*`（6 条不经触发点的命令）；另：旧套件在实现上恰好 6 组变化，即 21ab、21ac、21ag、21aj、21al、21ao，每条变化的断言与 W9 一致 | BI-8 |
| SC-V2 | P2 | `V2-G1`–`V2-G8`（含 `V2-G3b`）、`V2-G11`、`V2-E6`–`V2-E9`；bash 3.2 下整轮 | BI-5、BI-6、BI-16、BI-20、BI-22 |
| SC-V3 | P3 | `V3-S4`、`V3-G9`、`V3-G10`、`V3-E3`–`V3-E5`、`V2-E7` | BI-4、BI-13、BI-14、BI-21 |
| SC-V4 | P4 | `V4-S1`–`V4-S3`、`V4-S6`–`V4-S8`、`V4-S11` | BI-1、BI-19 |
| SC-V5 | P5 | `V5-S5`、`V5-S9`、`V5-S10`–`V5-S10d`、`V5-S12`、`V5-S13`、`V5-S13b`、`V5-S14` | BI-2、BI-3、BI-15、BI-23 |
| SC-V6 | P6 | `V6-E2`（另见 SC-V3 各 e2e 的字节比对） | BI-7 |
| SC-V7 | P7 | `V7-E1`、`V7-E13`–`V7-E15`、`V7-N5` | BI-10、BI-12 |
| SC-V8 | P8 | `V8-D1`–`V8-D3` | BI-9 |
| SC-V9 | P9 | `V9-C1`、`V9-C1b`、`V9-C2`、`V9-C2b`、`V9-E10`–`V9-E12` | BI-8、BI-17、BI-18 |
| SC-V10 | P10 | `V10-N1`–`V10-N4` | BI-11 |
| SC-V11 | 结构 | `V11-S1`（7 个新函数在 source 闸门之上）、`V11-S3`、`V11-S4` | BI-11（第二份规则循环） |
| SC-V12 | 同步 | `V12-C1`（hook 注释块级核对）；另：套件注释块级核对（`commentsync.py --suite-only`）、套件头注释计数 = 实跑数、standards 三处计数 = 实跑数（TASK-006，核对命令见任务计划） | — |

「必须抓住的坏实现」一列与下面 BI 表的指定用例有 5 处交叉：BI-8 的指定用例在 SC-V9；BI-4、BI-2 的指定用例含 `V6-E2`（属 SC-V6）；BI-11 横跨 SC-V10 与 SC-V11。以 BI 表的指定用例为准（PP2-m23）。

**post_planning R2 的补强（TASK-002 必交）**：五席另行构造的 60 个坏实现漏网 46 个，去重后 12 类在放行方向（R2 汇总「非作者变异测试汇总」）。TASK-002 为每一类补确定性用例，把这些坏实现并入 `mutants.py`（从 BI-24 起编号），并补上计时类用例的负载门、金丝雀与用例编号清单、残余进程用例的唯一参数、commentsync 的逐句核对、块 B 的逐字断言；明细见 `detailed-tasks.yaml` TASK-002。

**坏实现清单**（每个都是「v3.1 原型 + 一处改动」，由 `v31/mutants.py` 构造。这是作者自建的自检，证明用例能红；非作者独立构造仍是 TASK-003）：

| BI | 坏实现（v3.1 + 一处改动） | 指定用例（须全部变红） | W13 | 连带变红的其他用例 |
|---|---|---|---|---|
| BI-1 | verdict read from the last line of the output text (v2) | `V4-S6-spoofed-tail-0` | 抓住 | — |
| BI-2 | no process group and no group-leader self-check: the job PID alone is killed | `V5-S5-pipe-holder`、`V6-E2-deadline-fallback-bytes` | 抓住 | 8 |
| BI-3 | the judgement starts without checking that the timer runs | `V5-S10c-dead-timer-no-judgement`、`V5-S10d-no-judgement-with-dead-timer` | 抓住 | — |
| BI-4 | the relaxed rerun runs in-process: no job, no hard deadline | `V6-E2-deadline-fallback-bytes` | 抓住 | 8 |
| BI-5 | the gate does not ask about a project extension | `V2-G4-extension-file-with-entry`、`V2-E9-extension-project` | 抓住 | 2 |
| BI-6 | the platform is read from the environment (OSTYPE, EPOCHREALTIME present) | `V2-G3-gate-calls-platform`、`V2-G3b-gate-uses-build-facts`、`V2-E8-ostype-from-environment-ignored` | 抓住 | 1 |
| BI-7 | the fallback writes a time text of its own instead of the baseline size text | `V6-E2-deadline-fallback-bytes` | 抓住 | 4 |
| BI-8 | VMAX relaxed too | `V9-E12-vmax-unchanged` | 抓住 | — |
| BI-9 | the growth limit is recomputed from the rewritten string, per variable | `V8-D3-growth-8193-plain`、`V8-D3-growth-8193-braced` | 抓住 | — |
| BI-10 | the longest line is measured on the raw command, not on the copy | `V7-E14-long-line-from-expansion` | 抓住 | — |
| BI-11 | rows only through a rule loop of its own, which skips the W12 neutralisation | `V10-N3-environ-big-judge`、`V11-S4-one-rule-loop` | 抓住 | — |
| BI-12 | the line length is tested with [[ =~ .{8193,} ]] (it matches across newlines) | `V7-N5-read-big-judge-short-lines`、`V7-E13-multiline-copy-normal-text` | 抓住 | 1 |
| BI-13 | the deadline is anchored after the stdin parse, not at the hook start | `V3-E3-anchor-at-hook-start` | 抓住 | 1 |
| BI-14 | the deadline uses the whole budget, not min(budget, 3) | `V3-G10-cap-3`、`V3-E4-cap-3-at-budget-4` | 抓住 | — |
| BI-15 | the group is not killed after the job ends | `V5-S9-child-left-behind`、`V5-S13b-nothing-outlives-the-run` | 抓住 | — |
| BI-16 | the relaxed flag is taken from the environment (not initialised) | `V2-G11-flag-not-from-environment`、`V2-E6-flag-from-environment-ignored` | 抓住 | — |
| BI-17 | the count bounds also hold inside the rerun | `V9-C1-assignments-rerun`、`V9-C2-references-rerun-c12`、`V9-E10-count-axis-read-blocked` | 抓住 | 1 |
| BI-18 | TMAX is not checked inside the rerun | `V9-E11-tmax-in-rerun` | 抓住 | — |
| BI-19 | a bare 0 from the job counts as allowed | `V4-S11-bare-zero` | 抓住 | — |
| BI-20 | an empty extension file counts as no extension | `V2-G4-empty-extension-file` | 抓住 | — |
| BI-21 | a clock that went backwards extends the deadline (time left not capped) | `V3-G9-clock-backwards` | 抓住 | — |
| BI-22 | the gate does not ask for time left | `V2-G6-no-time-left`、`V2-G7-no-anchor`、`V2-G8-budget-0` | 抓住 | — |
| BI-23 | the timer kills only after a successful sleep (&& instead of ;): a failing sleep leaves no deadline | `V5-S14-failing-sleep-kills-at-once` | 抓住 | 1 |

## Impact

- **版本**：v1.77.x PATCH（当前已发 v1.77.3，2026-10-23）。版本号与发版时点由 owner 定（TASK-006）。
- **aria `hooks/secret-guard.sh`**：
  - 改：`_sg_vx_collect`（重跑内无计数上限；死代码另行提交）、`_sg_vx_replace`（重跑内无计数上限）、`_sg_vx_apply`、`_sg_vx_pass`、`_sg_per_segment_eval`、`_sg_judge_one`（第三参数）、`_sg_emit_blocked`（`longline` 分支）。
  - 新：常量 `_SGV_GMAX`、`_SGV_LMAX`；顶层 `_SG_P0`、`_SG_RELAXED`；函数 `_sg_vx_big_judge`、`_sg_relax_left`、`_sg_relax_ok`、`_sg_relax_platform`、`_sg_relax_noext`、`_sg_relax_job`、`_sg_relax_run`。
  - 注释：What 7 的 8 块与 What 7 补充的 4 处；准入门按 What 1 补充收紧。
- **aria `hooks/tests/secret-guard.test.sh`**：搬入 `v31/sc-cases.sh` 的全部用例（含 `shim/` 与 `shapes.py` 的输入）；6 组既有用例按 W9 改断言，标题与注释块按 What 7 改写；新增区分普通命中与 `longline` 的断言 helper（`wpa_x_finding` 会把 `longline` 文案当成普通命中，PP1-A12）；头注释计数；post_planning R2 的补强用例（TASK-002 必交，见 Success Criteria）。
- **aria `CHANGELOG.md`**：草稿见下，终稿归 TASK-006。
- **standards `conventions/secret-hygiene.md`**：`:23`、`:316`、`:352` 三处测试计数改为发版时实跑的权威值。基线上已经漂移（三处写 822 / 816，套件头注释写 831，非 git 副本实跑 814），所以一律以 TASK-006 在待发版 SHA 的 git 检出里现跑的数为准，每处两个数（含 zsh / 无 zsh）。改它要走 standards 自己的提交与 gitlink 更新（TASK-006）。
- **发布同步面**（owner 门，TASK-006）：以 v1.77.2 的发版提交为样板逐项列出（主仓 `028b458a` 与 `e360908c`，后者修了主仓根 `VERSION` 表）——aria 侧 `.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`VERSION`、`CHANGELOG.md`、`README.md`、`README.zh.md`；主仓侧 `VERSION`、`README.md` 与 i18n README（只改徽章与版本行，正文不重译）、`CLAUDE.md` 项目状态段、`docs/architecture/system-architecture.md` §2.8、`docs/architecture/version-scheme.md`、aria gitlink（standards 也变时另加一个）；tag 按 `standards/conventions/version-management.md`。机械兜底：`m6-version-badge-match`、`i18n-readme-translation-currency`、`plugin-version-arch-docs-match`。
- **Rule #6**：改的是 hook，不是 Skill。逐 hunk 判，分两块（WP-A 先例），写进 `detailed-tasks.yaml` 的 `rule6_note`：块 A 是逻辑、套件、注释、文档，不属 Skill 变更；块 B 是 AI 可见的文字（`longline` 模板、两条增长原因串）与路由带来的文案变化，按 SOT §2 第 3 行三件套处理（见 Owner 裁定点）。路由变化让原来看到「过大」文案的大命令现在可能看到普通命中文案（含「Acceptable filters」与 `# guard:ack` 指引），这一点在块 B 里点名。

**CHANGELOG 草稿**（v1.76.1 体例；终稿与占位符的取值归 TASK-006）：

```
## [1.77.x] - <date> — secret-guard W10 尺寸误拦收窄 (`10CG/aria-plugin#217`; PATCH: 只因尺寸被拦的大命令改为完整判定; 判定语义的既有缺口随之覆盖更多大命令, 见放宽面申报)

### Security — PreToolUse secret-guard (W10 尺寸预算按增长量判 + 硬截止重判)

- **问题**: W10 (变量展开第二遍) 的副本上限按**总长**计: 任何超过 8192 字符、又引用了已赋值变量的命令都按「过大」拦下, 哪怕展开只多几个字符。维护者本机会话记录里 > 8 KB 的 Bash 命令有 17.6% 因此被拦 (739 条中 130 条); > 4 KB 的命令里被拦的 138 条中 137 条属这一类 (另 1 条是值过长)。
- **修复**: 在原来按总长拦的两处, 若满足放宽条件, 改为在一个硬截止作业里按放宽规则重判 W10: 副本上限改按增长 (`_SGV_GMAX` = 8192); 重判里不设计数上限 (所有赋值与引用都代入); 超过 8192 的副本照常完整判定, 其中行长超过 8192 的只匹配规则、不评估脱敏过滤 (新 `longline` 文案)。截止 = hook 启动 + min(`SECRET_GUARD_TIME_BUDGET_S`, 3) s; 作业自成进程组, 到点整组终止; 截止前没判完、或任何异常, 一律按原来的「过大」文案拦 (逐字节相同)。
- **放宽条件**: x86_64 GNU/Linux 上的 bash 5.0–5.3 (实测 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20), 不在 WSL 里、项目没有启用 `.aria/secret-guard.paths` 扩展、hook 启动后未满截止。其他平台 (macOS / Windows 原生 / WSL1 与 WSL2 / musl / aarch64 等其他架构)、其他 bash 版本、启用扩展的项目: 行为与之前完全相同。还依赖 `/proc` 与支持小数秒的 `sleep`; 缺了它们放宽不生效, 行为同旧版。
- **行为变更**: 本机真实流量里, 被尺寸上限拦下的 137 条命令在 Linux 上放行 <N_allowed> 条 (TASK-004 实测); 这类命令被拦时, 文案由「过大」变为增长超限、TMAX、VMAX、`longline` 或普通命中文案; 重判没在截止前完成的, 照旧按「过大」拦, 但要等到截止 (约 3 s; 以前在触发点当即拦, 通常 2 s 以内); `SECRET_GUARD_TIME_BUDGET_S` 设为 4 时截止仍封顶 3 s, 设得更小时截止随之缩短。
- **放宽面申报**: 这些大命令沿用现有的判定语义, 所以判定语义上的既有缺口覆盖到更多大命令 —— 块结构命令整串判定、命令里任一处脱敏过滤都会给整条命令 credit (`10CG/aria-plugin#139`; 例: 读一个凭据路径的命令, 只要别处有一个无关的 `>/dev/null`, 就会放行并读出凭据); `10CG/aria-plugin#138` / `10CG/aria-plugin#140` / `10CG/aria-plugin#141` / `10CG/aria-plugin#142` / `10CG/aria-plugin#229` 同理。原串或中间副本超过 8192、代入后变短的命令同样按普通判定。另有两类 W10 代入语义的既有缺口同样覆盖到大命令: 同名变量赋值两次时代入用第一个值 (bash 读后一个); 分段模式下值里的 shell 语法 (如 `G='| jq keys'`) 代入后成了语法, 读取因此得到 bash 并不施加的过滤 credit (载体 `10CG/aria-plugin#231`)。
- **已知限制**: 首遍判定不计时 (`10CG/aria-plugin#228`); 不超过 8192 的副本判定只受协作式时间预算约束, 单次可超过 5 s —— v1.76.1 条目里的「永不 fail-open」对此不成立, 特此订正 (载体 `10CG/aria-plugin#228`); 小命令的 count 轴缺口不变, for 列表跨换行误拦与 heredoc 内赋值形文本误收集同样未修 (载体 `10CG/aria-plugin#231`); 截止之后的收尾随负载增长 (负载约 10 时实测 0.2–1.2 s)。
- **Rule #6**: hook 不是 Skill; 逻辑与套件不属 Skill 变更。AI 可见的新文字 (`longline` 模板、两条增长原因串) 与路由带来的文案变化按 Rule #6 SOT §2 第 3 行处理: 点名行为、逐字断言作定向 fixture、AB 套件不覆盖 hook 文案的缺口记在 `10CG/Aria#261`。
- 测试: `secret-guard.test.sh` <N_cases> 例 (无 zsh <N_cases_nozsh> 例; 新增 <n_new> 例; 6 组既有用例按新语义改断言); bash 3.2.57 + 5.0.18 + 5.1.16 + 5.2.15 + 5.3.20; 真实流量回放 (只出汇总)。

Refs 10CG/aria-plugin#217, 10CG/aria-plugin#228, 10CG/aria-plugin#139, 10CG/aria-plugin#231, 10CG/Aria#261
```

## 证据与复现

| 文件 | 内容 | 生成方式 |
|---|---|---|
| `evidence/W0-corpus-manifest.tsv` | 冻结语料：2412 条 > 4096 字节的真实命令，每条记 `n`、字节数和 sha256，不含原文 | `traffic/manifest.py` |
| `evidence/W1`–`W3` | 138 条的分类、只匹配规则的结果、最长行 | `traffic/` 下同名脚本 |
| `v3/` | v3 原型与证据（post_planning R1 审的对象，原样保留） | `v3/README.md` |
| `v31/W8-v31.diff` | v3.1 原型相对基线的全部改动 | `v31/run-evidence.sh` W8（`mkv31.py`） |
| `v31/W13-sc-cases.txt` | 验收用例：原型在 bash 5.0 / 5.1 / 5.2 / 5.3 / 3.2 上各一轮；基线作为被测 hook 的一轮（基线红集）；全部坏实现逐个的结果 | `run-evidence.sh` W13（`sc-cases.sh`、`sc-direct.sh`、`run-mutants.sh`、`mutants.py`） |
| `v31/W11-adversarial.txt` | v3 的对抗形状在 v3.1 上的 e2e 矩阵（`C.UTF-8`） | `run-evidence.sh` W11 |
| `v31/W12-real-traffic.txt`、`v31/W12-replay-138.tsv` | 真实流量：138 条回放（埋点版，含触发时刻与每条对上界的核对）、300 条逐字节、bash 3.2 下 40 条逐字节 | `run-evidence.sh` W12（`mkdbg31.py`、`replay138.sh`、`ident.sh`、`ident32.sh`） |
| `v31/W9-suite.txt` | 旧套件在基线与原型上各跑一遍 | `run-evidence.sh` W9 |
| `v31/commentsync.py` | What 7 的块级核对 | — |

**复现**：

1. 所有 W 文件由 `v31/run-evidence.sh <工作目录> [阶段…]` 生成：基线一律取自 aria `59e333c` 并断言 sha256 前缀；被测 hook 默认是 `mkv31.py` 的原型，设 `IMPL=<hook>` 即换成真实实现（TASK-004）；输出先写工作目录，阶段成功后复制回 `v31/`：失败或中断的阶段不覆盖，成功的阶段会覆盖已提交的同名证据（post_planning R2 PP2-O；PP1-A39 只修了一半）。TASK-004 先给脚本加输出目录参数，实现那一轮写到 `v31/impl/`，对照对象取 `git show 95cf1de7:<路径>`。W8 的头两行带生成时的临时路径，复现时只在这两行有差异；每份输出的首行记日期、平台、两个 sha256 与负载。
2. W12 还需要仓外的冻结语料 `TRAFFIC_DIR`（用 `.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/traffic/extract.py` 抽取，按 W0 的 sha256 用本变更自己的 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/traffic/refreeze.py` 复原编号；新会话会让抽取编号漂移，只认哈希）与一个 bash 3.2 二进制 `BASH32`（W13 的第五轮也靠它；不设时脚本静默只跑四个 bash，TASK-004 改为报错退出）。
3. 本机依赖与自建的 bash 版本见 `v31/README.md`。

## Decision record

1. **先量真实流量，再设计**（`10CG/aria-plugin#228` 的教训）：137/138 是总长上限的误伤，增长量都很小。
2. **不直接调大 SMAX**：判定成本没有形状上的上界（Why 第 1–4 项），调大只会让构造出来的输入重新「判定迟到 → fail-open」。
3. **用硬截止承载裁定 B**：贵的是判定与构建本身，判定前看表看不到它；硬截止到点就拦，失败方向都是拦。姿态不变，按技术裁定采用，已向 owner 通报。
4. **基线先跑，放宽重跑**（R2-A2）：放宽只在基线本来要按尺寸拦的那一刻触发，其余路径一行不动，P1 由结构保证；重跑的全部工作都在同一个截止里。代价是放宽类命令的前段会做两遍，这部分有尺寸早停，很便宜。
5. **结论只取退出码，作业自成进程组**（R2-A1、A3）：v2 从输出最后一行解析状态，残留子进程可以冒充；又只杀判定子 shell，残留子进程会占住管道。v3 起两处都从机制上消除，并用组长自检兜住 `set -m` 失效的情况；v3.1 再补上作业结束后的组杀（PP1-A3）。
6. **截止用 `EPOCHREALTIME`**（R2-A4）：整秒 `SECONDS` 让实际截止落在 2–4 s 之间。没有 `EPOCHREALTIME` 的 bash 不放宽，由 Decision 16 的版本范围保证。
7. **有扩展的项目不放宽**（R2 KM-F-01、BA2-F-12）：扩展对副本 > 8192 有绝对尺寸门，放宽之后结局仍是拦，却要先花几秒；不放宽就与基线逐字节相同，扩展腿也不必进截止。v3.1 让「有没有扩展」判不出时按有扩展处理（PP1-A27）。
8. **回落一律用基线文案**：截止、时间检查点、自检、内部错误，都回到「过大」拦截，逐字节与基线相同。放宽路径不需要自己的时间文案，也就没有 v2「Nothing was matched」与「4 s」两处失实（R2-A21）。
9. **撤回 D**（owner 二次裁定，2026-10-21）：「未被引用」认不全 shell 读变量的方式；能挡住反例的保守判定把真实流量里唯一救下的那 1 条也拦下，收益为 0。根因是 `_sg_vx_collect` 把 heredoc 正文里形似赋值的文本当成赋值，转残余。
10. **撤下「for 列表止于换行」**（R1-A2）：照字面实现会截断反斜杠续行的列表，新增漏检；真实流量 0 例。转残余。
11. **C 复用 `_sg_judge_one`**：W12 中和只有一份代码，`nocredit` 路径不另写规则循环（`V11-S4` 钉住）。
12. **整体硬截止留给 `10CG/aria-plugin#228`**：v3 起是「首遍之后全部步骤进截止」这一中间选项，只对基线本来就拦的那一类命令生效，所以不改任何基线放行命令的姿态。把同一机制推广到所有命令（含首遍），会把首遍超时从放行改成拦，改变基线放行类命令的姿态，属 owner 的决定；真实流量里首遍超时只出现过 1 次（测试探针），收益接近 0。
13. **count 轴的小命令一侧不在范围内**：`10CG/aria-plugin#217` 正文建议维持现状；大命令一侧由 Decision 14 处理。
14. **重跑里取消计数上限**（PP1-A1）：三个选项实测对比——申报放行（TL 构造的读取被放出去）、计数触顶即回落（真实流量收益 137 → 73，见 post_planning R1 汇总的复跑表）、重跑里不设计数上限（该构造被拦，收益见 W12 第 1 节）。取第三种：计数上限只为封顶基线那一遍的成本，重跑的成本已由截止、增长上限与 TMAX 封顶；判定完整就是裁定 A 的字面，判不完就回落（裁定 B）。代价：引用密集的大命令要代入全部引用，可能在截止前判不完——v3 的 apply-heavy 两个形状（16 个变量各 32 处引用、约 60 KB）在 v3 上 1.4 s 放行，在 v3.1 上 3.0 s 回落拦截（W11）；真实流量里没有这种形状（W12 第 1 节）。
15. **放行用专用退出码 77**（PP1-A28）：放行要正向确认。`0` 是 bash 在若干异常下的默认值（例如 `wait` 对继承来的旧 PID 返回 0），用它表示放行等于把「没判」当成「判过且放行」。
16. **只在实测过的 GNU/Linux bash 5.0–5.3 上放宽**（PP1-A26，按裁定 E 的原则）：本机用签名校验过的 GNU 源码另建了 5.0.18、5.1.16、5.3.20（连同系统的 5.2.15），整套用例在四个版本上全绿，3.2.57 上准入门关闭、端到端与基线逐字节相同（W13 第 1 节）。macOS、Windows、musl、Android 与其他 bash 版本维持基线，实测通过后另行放开。v3.2 再收紧到实测过的 x86_64，WSL 一律维持基线（Decision 21）。
17. **验收写成代码**（PP1-A5–A14、A33–A36）：post_spec R2 的 Major 有 8/11、post_planning R1 有 13/23 落在用文字描述的 SC 与 BI 上——两个执笔者照同一段文字会写出不同的用例，时延判据随机器快慢变化，基线红绿排在用例写出来之前。所以在设计阶段就把用例写成代码，并在基线、原型、坏实现三种 hook 上实跑（W13）；计时判据的下界一律由注入的固定延迟给出。post_planning R2 证明这一步有效：每条 Major 都有可复跑的证据。它也证明用例集仍有同源盲区：作者的 23 个坏实现全被抓住，非作者的 60 个漏网 46 个；计时类用例的上界仍随负载变化。补强写进 TASK-002（Decision 19）。
18. **`longline` 原样复用 oversize 的全部指令行**（PP1-A19）：新写的只有描述句，AI 看到的指令与现有模板逐字相同；指令行的逐字相同由 `V11-S3` 钉住。描述句与两条原因串的逐字断言 v3.1 声称有、其实没有，由 TASK-002 补；块 B 也改按 SOT 第 3 行处理（PP2-T）。
19. **post_planning R2 之后实现优先**（owner 2026-10-23）：R2 的 Major 簇从 23 降到 20，但 18 个落在 v3.1 新写的表面上，停止规则触发。再审一轮审的会是新补的用例，所以不开第 3 轮：v3.2 只改文字，验收补强写进 TASK-002 作必交项，由新执笔席用五席的探针补齐；实现之后由 TASK-003、TASK-005 的新席位复核（本项目 config 的 post_implementation 检查点为 off，这两项是 owner 2026-10-22 选的自愿补位）。
20. **两类既有代入语义缺口点名申报**（owner 2026-10-23）：它们在小命令上本来就放行；按裁定 A「沿用现有判定语义」，大命令同样放行。不为它们改设计，申报并给载体（R-a、残余 8）。
21. **准入门按实测范围收紧**（owner 2026-10-23）：`*-linux-gnu*` 会放进没实测过的 aarch64 与 WSL。按裁定 E 收紧到 x86_64，WSL 一律维持基线：WSL1 是翻译层，WSL2 虽是真 Linux 内核也没有实测过（owner 先选排除 WSL1，随即追加 WSL2）。往更严方向，姿态不变（What 1 补充）。
22. **WSL 标记读法加固与复审指出的注释**（2026-10-25，主控，技术口径；TASK-005 复审 D-1、D-2、m-1–m-6、D-3）：`/proc/sys/fs/binfmt_misc` 在 systemd 宿主上多是自动挂载点，`-e` 穿过它可能在自动挂载没人服务时一直阻塞，hook 被 Claude Code 超时杀掉即放行——基线从不碰这里，这是放宽带来的新放行路径。改为先读挂载表、只在 binfmt_misc 已挂上时看 `WSLInterop*` 项、读不出挂载表即当作 WSL（What 1 补充 2）。只会把放宽关得更严，姿态不变，不另请 owner 裁定，告知 owner。同轮补申报 VMAX 文案（What 5、R-c），并按 What 7 补充 2 改正注释。

## Tasks（A.2 细化为 detailed-tasks.yaml）

| 任务 | 阶段 | 内容 | 执行 |
|---|---|---|---|
| TASK-001 | B.1 | 入场：续用认领、建分支、重锚行号；对外动作照 WP-A 先例分两组上呈（一次性授权四类、逐次请示五类），残余 issue、载体与留言得到放行后再做；上呈不阻塞 TASK-002 开工 | 主控 + owner |
| TASK-002 | B.2 | 按 W8 落地 What 1–5、7，加上 What 1 补充与 What 7 补充；What 6 单独提交；把 `v31/sc-cases.sh` 的全部用例搬进套件并按 post_planning R2 补强（必交），6 组既有用例按 W9 改断言，套件注释与标题按 What 7 改写 | 新执笔席 |
| TASK-003 | B.2 | 非作者对抗复核：独立构造坏实现（BI 清单之外再想），逐个在实现上跑；对抗耗时矩阵 | qa 席（非作者） |
| TASK-004 | B.2 | 验收：`IMPL=<实现> run-evidence.sh` 重跑 W8–W13，逐条对判据 | 主控 |
| TASK-005 | B.2 | 独立代码审查（post_implementation / pre_merge 闸门为 off，自愿补上）；审查之后的任何改动须复审 | code-reviewer 席 |
| TASK-006 | C | 发版（owner 门）：版本号、CHANGELOG 终稿、standards 计数、发布同步面、tag、双推与 `ls-remote` 核验 | owner + 主控 |
| TASK-007 | D | 收口：上线后运行时复验；`10CG/aria-plugin#217` 逐项对账后关闭；认领释放、归档、周期 handoff | 主控 |
