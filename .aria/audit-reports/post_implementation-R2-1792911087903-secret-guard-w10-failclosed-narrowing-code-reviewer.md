---
checkpoint: post_implementation
mode: single-seat
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-25T06:51:27.903Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/proposal.md
agents: [code-reviewer]
reviewed_sha: 710a36d
reviewed_hook_sha256_prefix: 834dee6db0d0
previous_report: post_implementation-R1-1792888152945-secret-guard-w10-failclosed-narrowing-code-reviewer.md
---

# post_implementation R2（单席 code-reviewer，增量复审）— secret-guard W10 尺寸误拦收窄（10CG/aria-plugin#217，TASK-005）

> **Verdict：PASS_WITH_WARNINGS**。0 Critical / 1 Major / 3 Minor，另列 1 条疑点和 1 条自报的运行影响。审查对象是 aria `710a36d`，worktree 实测 hook 的 sha256 前缀为 `834dee6db0d0`。增量面是 `2893bcc..710a36d -- hooks/`（3 个文件，+140 / −36），加上主仓 `a948862d..ba48f6e2` 里 v31 的 4 个文件。规格来源：任务书 `r217impl/BRIEF-T005r.md`。

## 审查范围与方法

- 读过的内容：hook 的全部 7 个 hunk；helper 与套件的 diff；helper 与 `v31/sc-direct.sh` 的逐行对照（V15 段逐字相同，其余差异是既有的结构差）；`sc-cases.sh`、`commentsync.py`、`impl/w14-mutants.py` 的 diff；proposal 的 What 1 补充 2、What 3 / 4 / 5、R-c、What 7 补充 2、决策 22；计划里 TASK-005 的 notes；`b2/T005f-report.md` 与 `b2/T005f2-report.md` 的未决项。
- 机械核对（`r217impl/t005r/vcheck.py`）：
  - What 7 补充 2 回填段的代码行，与 `git diff -U0 2893bcc 710a36d -- hooks/secret-guard.sh` 的 50 条 +/− 行逐字比对，缺 0。
  - What 1 补充 2 的 9 行代码在 hook 里逐字可见，缺 0。
  - CHANGELOG 草稿的 :915 与 :928 两处写了 VMAX。
- 探针（`r217impl/t005r/probe.sh`、`probe2.sh`；输出在 `probe.out`、`probe2.out`；以 `taskset -c 2,3 nice -n 19` 运行）：
  - 只直调 `_sg_relax_nowslfs`。
  - probe2 在 `unshare -rm` 建的私有挂载命名空间里叠 tmpfs，测读表耗时随挂载数怎么变。
  - 没有跑套件整轮，也没有跑坏实现。

## 阶段 1：规格符合 — PASS

| 项 | 结论 | 依据 |
|---|---|---|
| INV-1 | 通过 | hook 的非注释改动只有准入门两行与新函数，与 What 1 补充 2 的代码块逐字一致（9/9）；7 处注释与 What 7 补充 2 的回填文本逐字一致（50/50）。 |
| INV-4 | 通过 | `_sg_relax_nowslfs`（:838）在 source 闸门之上；套件与 `sc-cases.sh` 的 V11-S1 清单已补上它。 |
| What 1 补充 2 | 一致 | 代码、已知边角与五条直调用例（W1a–d、W1e）都与 proposal :97-118 对得上。 |
| What 3 / 4 / 5、R-c | 一致 | m-5、D-3、m-1 的文档补充都在：:133、:145、:154、:784，以及 CHANGELOG 草稿的 :915、:928。 |
| 范围 | 无越界 | hook 只改了上面这些。测试侧的改动对应 m-3、m-4、m-6、What 1 补充 2 的用例与四份 WSL 判据。计数（981 / 975、150）与各 ids 清单已同步。 |

## 阶段 2：代码质量与安全

### 优点

- 只在 binfmt_misc 已挂上时才看目录。W1a 用「表里只有 autofs 那一行、目录里却放了 WSLInterop」把这一点做成能变红的断言。
- 读不出挂载表时返回 1 且 stderr 为空，W1d 同时断言这两点。
- 循环体用 if 而不是 &&。W1a、W1c 的假表末行都故意不匹配，专门钉住这一点。
- V15-T1 / T2 / T3 都能为对的原因变红（见第 3 项）。T2 的余量（1.0 s）比第一轮建议的 0.5 s 更宽。
- 回填的逐字文本由 diff 机械导出，我复核过，50/50 行一致。
- 测试侧判据换了与 hook 不同的写法（cat、awk 按字段比较、ls），而且不 source hook。

### Critical

无。

### Major

**M-1 准入门逐行读挂载表，在 procfs 上开销超线性；挂载多的宿主上，单这一步就能把 hook 拖过 Claude Code 的 5 s，hook 被杀后命令放行**

- 位置：hook :840，`{ while IFS= read -r l; ...; } 2>/dev/null < "${1:-/proc/self/mounts}"`。调用点 :830 排在 `_sg_relax_platform`（:831）与 `_sg_relax_left`（:832）之前。
- 机制：
  - bash 的 `read` 对能 seek 的文件按块读；每读完一行，就把多读进来的部分用 `lseek` 退回去。
  - `/proc/self/mounts` 是 seq_file。向回 seek 时，内核要从第一条挂载记录起重新生成，直到目标偏移。
  - 所以每读一行的代价随行号增长，读整张表至少是平方级。
- 实测（probe.sh / probe2.sh）：
  1. 本机的表有 41 行：每次调用 2.84 ms；同样的内容拷成普通文件后 0.65 ms。
  2. 用同样的读法读 `/proc/kallsyms` 的前 500 / 1000 / 2000 行：0.074 / 0.254 / 0.700 s。同样内容的普通文件：0.005 / 0.010 / 0.020 s，是线性的。
  3. 在 `unshare -rm` 的私有命名空间里往同一个目录叠 tmpfs，再直调 `_sg_relax_nowslfs`（默认参数，读的就是真实的 `/proc/self/mounts`）：500 条 0.40 s，1000 条 2.66 s，2000 条 20.8 s。3000 那一级被我设的 90 s 超时截断。同一张表改用 `$(< /proc/self/mounts)` 整体读：0.003 / 0.008 / 0.039 s。
  4. 测量条件的说明：
     - 探针以 nice 19 运行，与别的负载共用 2、3 号核，绝对值可能偏大；整体读的对照是在同样条件下测的。
     - 叠在同一个挂载点上会让每条记录的路径计算也变贵。这是我的推断，可以解释 2000 条时接近立方的增长。所以第 3 组是偏重的情形。
     - 挂载点各不相同时，按第 1 组的数字粗略外推（假设每条记录的生成代价不变、整体按平方增长）：约 2000 条 2–3 s，约 3000 条 5–7 s。这个外推没有实测。
- 失败情形：
  - 在 k8s 节点、跑很多容器的 Docker 宿主、或挂载传播失控（上万条）的机器上，一条到达触发点的命令（展开后的副本超过 8192）光准入门这一步就要花几秒。
  - 这段读取在主进程里，在硬截止作业之外，也在 `_sg_relax_left` 之前，中间没有任何时间检查点。总耗时超过 5 s 时，hook 被 Claude Code 杀掉，命令放行。
  - 对同一条命令，基线和 2893bcc（那里只做一次 stat）都会按尺寸拦。
  - 这正是决策 22 与主控裁定「不带着 D-2 发版」针对的那一类：环境导致阻塞，hook 被杀，命令放行。而它是本轮的修法新引入的。
  - 读表排在平台判据之前，所以放宽根本不可能生效的平台（aarch64、bash 4.x 等）在每个触发点也都要付这笔开销。
  - 连带影响：挂载上千条时，relax 模式里依赖短截止的直调用例会失去余量。例如 V15-T2 把锚点前移了 2.0 s；准入门读表若超过约 1 s，门会因为没有剩余时间而关上，用例假红。
- 修法建议（按 INV-1，先改 proposal What 1 补充 2）：
  1. 整张表一次读入再匹配，例如 `{ t=$(< "${1:-/proc/self/mounts}"); } 2>/dev/null || return 1; [[ -n "$t" ]] || return 1; [[ $t == *" $d binfmt_misc "* ]] || return 0`。bash 3.2 能解析；把空表当作读不出，顺带收掉已知边角。
  2. 把这一项挪到 `_sg_relax_platform` 与 `_sg_relax_left` 之后。这是第一轮 D-2 建议的后半，本轮没有做，裁定里也没有提到。
  3. 证据：发版前可以照 probe2.sh 的做法（`unshare -rm` 加叠挂载）量一次。套件里可以加一条静态检查，钉住这个函数不对挂载表逐行 read。

### Minor

**m-1 环境变量和目录权限能让「文件里的 WSL 标记」判成没有，与「环境只能把放宽关掉」相悖；failglob 下则变成内部错误拦截**

- 位置：hook :842，`for e in "$d"/WSLInterop*; do [[ -e "$e" ]] && return 1; done`。
- 实测（probe.sh）。假挂载表把一个临时目录列为 binfmt_misc，目录里放了 `WSLInterop-late`，正确结果应是 1：
  1. 环境里有 `SHELLOPTS=noglob`（bash 启动时会导入）：返回 0。
  2. 目录不可列（mode 000）：返回 0。glob 要用 opendir，只要没有读权限就静默得到空集，例如 0711，或者 LSM 禁止列目录却不禁 stat。2893bcc 的 `-e` 精确路径只需要搜索权限。
  3. 环境里有 `BASHOPTS=failglob`，目录里没有 `WSLInterop*`（挂着 binfmt_misc 的普通 Linux 宿主就是这样）：bash 报 `no match`，外面的 `( _sg_per_segment_eval … )` 子 shell 以 1 退出，顶层按 internal error 拦（:1742 起）。结局仍是拦，但文案不是基线的尺寸文案（P6），stderr 里还多一行 bash 的报错。
  4. 对照：从环境导入的 `GLOBIGNORE` 不影响结果（返回 1）；`nullglob` 下结果正确。
- 影响：
  - 第 1、2 种只有在一种 WSL2 上才会让放宽误开：内核是自编的、版本串里没有 microsoft 或 WSL，进程环境里也没有 WSL_DISTRO_NAME / WSL_INTEROP。所以实际暴露很小。
  - 但 hook :829 的注释和 What 1 都把「环境只能关、不能开」当作不变量。2893bcc 的写法不受这些影响。
- 修法：在 glob 之前加 `[[ $- == *f* ]] && return 1; shopt -q failglob && return 1; [[ -r "$d" ]] || return 1`，即看不了就当作有标记。也可以另加两个精确名的 `-e`（`WSLInterop`、`WSLInterop-late`）；这时目录已经挂上，stat 不会触发自动挂载。

**m-2 新注释有两处说得比代码宽**

1. hook :838 的函数头注释写着 `status 0 only when no WSL interop entry can exist` 和 `a mount table that cannot be read keeps the relaxation off`，:830 的行尾注释也写着 `a mount table that cannot be read`。
   - 实际上只有「打不开」时才关门；能打开却读不出时，按没挂上处理。这是主控已经认可的已知边角，这里只说措辞，不重提行为。m-1 的三种情形也会返回 0。
   - 建议改成 `cannot be opened`，并点名这个边角。What 1 补充 2 的代码块是字面规格，要先改规格。
   - 测试侧四份判据的注释自称 `the rule of the hook's _sg_relax_nowslfs`，在这个边角上两边结论相反：cat 读目录失败，判为有标记。同样只是措辞问题。
2. hook 头注释 :98-101 写着 `the deadline, a time checkpoint, the self-check or any other failure of the rerun falls back to that size block`，没有带上 What 4 与重跑块头（:795-806）写明的例外：bash 自身的致命错误以 2 退出时，原样写出它的报错。这个例外本身没有实测，所以这里只是两处注释彼此不一致。

**m-3 V15-T2 的注释把归零发生的位置说错了**

- 位置：helper :571-575（`v31/sc-direct.sh` 同一段）。注释写的是 `it reaches 0 only after 1.0 s from here to the judgement`。
- 实际：`_SG_LEFT` 是在 `_sg_relax_run`（:865）里算出的，fork 时传给作业；准入门（:832）之前也先查过一次。真正的界是从设锚点到这两次 `_sg_relax_left`。超过 1.0 s 时，要么门关上，要么 run 回落，作业里的判定根本不会运行，结果是 `_SG_LEFT []` 的假红。
- 断言本身没有问题，只需要改注释。

### 疑点（未核实，单列）

**疑点 1：表里「有一行」不等于「最上层就是它」。**

- :840 只要表里任意一行是挂在 DIR 上的 binfmt_misc，就会去列目录。
- 如果同一个挂载点上，binfmt_misc 之后又叠了一层 autofs（表里排在后面），实际可见的是 autofs，列目录会触发自动挂载，这正是 D-2 要避开的。
- 假表实测：binfmt_misc 那行在前、autofs 那行在后时，函数照样去看目录（返回 1）。
- 真实环境里是否会这样叠，我无法核实（systemd 对已经是挂载点的路径会拒绝启动 automount）。读表与列目录之间恰好被卸载的竞态，情况相同。
- 如果按 M-1 改成整表读，可以顺手改成取挂载点为 DIR 的最后一行来判类型。

**自报的运行影响（不是代码问题）：**

- probe2 在本机时间 06:42:35–06:44:05 占用 2、3 号核约 90 s。1 分钟负载从 1.60 升到 6.94，06:44:55 回落到 4.23。
- 叠挂载期间，每次 mount 都要短暂持有内核全局的 namespace_sem，而新 hook 的准入门恰好要读挂载表。
- 如果 4r 在这段时间里有计时类测量，请按 INV-7 复核首尾负载，必要时重跑。
- 我已用 pgrep 核对，没有残留进程；私有命名空间里的挂载随进程退出一并消失。

## 第一轮各条的处置结论

| 条 | 结论 | 说明 |
|---|---|---|
| m-1（VMAX 申报） | 到位 | 已补在 What 5 表 :154、R-c :784、CHANGELOG 草稿 :915 / :928；hook 头注释 :96-98 也写了 value text。 |
| m-2（四处注释） | 到位 | 四处都已改，意思与代码对得上；另外补了重跑块头的同类一句（:796）。回填文本 50/50 行逐字一致。新注释另有两处偏宽，见本轮 m-2。 |
| m-3 | 到位 | 注释与 chk 文案改为 closed pole，并点名 open pole 是 V14-G1；ids 未动；helper 与 sc-direct.sh 一致。 |
| m-4 | 到位 | 改用 `id -ru`；CapEff 由 bash 自己从 `/proc/$BASHPID/status` 读（只在 relax 模式、bash 5.x 下运行）；sc-direct.sh :259-260 已同步。 |
| m-5（只改文档） | 到位 | What 3 :133 写明 fork 延迟计入 ε。:141 的 ε 定义还只列了「命令替换返回、sed、进程退出」，建议顺手补上这一项，不单列为发现。 |
| m-6 | 到位 | T1 / T2 / T3 都能为对的原因变红（第 3 项）；T2 会因 M-1 连带假红。 |
| D-1 | 到位 | 改为匹配 `WSLInterop*`，W1b 钉住 `WSLInterop-late`。 |
| D-2 | 部分到位 | 核心部分（只在已挂上时看项、读不出就关门）已做，并由 W1a / W1d 钉住。第一轮建议的后半「挪到平台判据之后」没有做，裁定里也没有提。修法本身又引入了 M-1。另见疑点 1。 |
| D-3 | 到位（文档） | What 4 :145 与重跑块头（:795-806）写明了例外；头注释没有带上，见本轮 m-2 第 2 处。 |

## 第 1 项：What 1 补充 2 逐点

- 各种状态下的结论：
  - 表打不开：返回 1，stderr 为空（W1d）。
  - 表能打开却读不出：返回 0（已知边角）。我认为它不比主控判断的更危险：WSL 主要靠内核串识别，这一项只在自编内核上起作用。M-1 的整表读法可以顺带把它收掉。
  - 表里没有 DIR 上的 binfmt_misc（包括只有 autofs 一行）：返回 0，不看目录（W1a）。
  - 已挂上且有 `WSLInterop*`：返回 1（W1b）。已挂上但没有：返回 0（W1c）。
  - 已挂上但目录不可列：返回 0（m-1）。上面又叠了 autofs：照样看目录（疑点 1）。
  - 末行没有换行：那一行不参与匹配（read 的语义）。真实的 /proc 表与几张假表都以换行结尾，不构成问题。
- 短路逻辑：`[[ -n "$wsl" ]] || _sg_relax_nowslfs || wsl=wsl` 是对的。环境里已有标记时不读表；只有函数返回 1 才置 wsl；W1e 钉住「函数失败就关门」。hook 用的是 `set -uo pipefail`，没有 -e，不受 errexit 影响。
- set -u：`l` 和 `e` 声明为未赋值的 local，只在赋值之后才引用；两个参数都有缺省值。
- glob 选项：nullglob 下结果正确；noglob 与 failglob 见 m-1。
- bash 3.2：只用了 `[[`、`(( ))`、`local` 和 for-in，3.2 能解析。5f2 在 3.2.57 上实跑 83 PASS 加 67 SKIP，我没有复跑。
- 性能：见 M-1。

## 第 3 项：新用例与测试侧判据

- **V15-W1a–d**：断言的就是名字说的事。哪些坏实现会让它们变红：
  - 不看挂载与否就去列目录：W1a 红。
  - 只认精确名 `WSLInterop`：W1b 红。
  - 挂上了就判有：W1c 红。
  - 循环体写成 &&：W1a 与 W1c 红，因为末行不匹配。
  - 读不出表反而放行，或报错漏到 stderr：W1d 红。
  - 这几条与负载无关，两种模式都会运行。
- **V15-W1e**：把函数桩成返回 1 时，门必须关上。在准入门里取反、或者忽略返回值，都会变红。这条只在 relax 模式下运行。
- **V15-T1**：sleep 函数会被计时器所在的子 shell 继承；判定桩一直等到计时器记下参数才返回。睡 3 s、睡整个预算、或者计时器没起来，都会变红。等计时器的窗口是 3 s，基本与负载无关。
- **V15-T2**：静态部分数 `_SG_P0=` 的赋值行，以及它是否紧跟在 `set -uo pipefail` 之后。动态部分在准入门、run 或作业里重取锚点时会得到约 3 s，因而变红。负载方面的余量是 1.0 s；注释的措辞见 m-3，连带问题见 M-1。
- **V15-T3**：作业自杀之后，`wait` 之后的组杀会碰上一个空组；去掉 `exec 2>/dev/null`，stderr 就会出现报错，因而变红。与负载无关。
- **测试侧四份判据**（helper :73 与 `sc-direct.sh` :51 的 `wslmark`、套件 :234 的 `sg_w10_wslfs`、`sc-cases.sh` :49 的 `wslmark`）：
  - 与 hook 的函数同义，只在已知边角上结论相反（见 m-2）。
  - 不 source hook，独立于 hook。但四份是同一段文本的拷贝，彼此并不独立：规则本身写错，四处会一起错。
  - 与 hook 函数的对照只在一次性证据 `b2/t005f2/prove-w1.sh` 里（5 个 bash 上 7/7）。套件里没有任何地方带参数调用这些判据。

## 第 4 项：注释

hook 里改写的 7 处注释我逐一对过代码：头注释 :92-101、LENGTH BUDGET :602 起、`_sg_vx_pass` 说明 :724 起、重跑块头 :795-806、准入门两行 :829-830、`_sg_relax_nowslfs` 函数头 :838、`_sg_relax_noext` 函数头。除 m-2 的两处之外都属实。其中 `_sg_relax_noext` 的新说法（找不到项目根时，包括 jq 读不了 cwd，算作没有扩展）与第一轮 P6 的实测相符。

## 建议汇总（按优先级）

1. M-1：整表一次读入，并把这一项挪到平台与时间判据之后；先改 proposal，发版前用 unshare 加叠挂载量一次。
2. m-1：glob 之前，对 noglob、failglob 和不可读目录一律关门。
3. m-2、m-3：只改措辞。
4. 按 INV-8，hook 再改之后，需要重跑 W8-W14，并对新增的 diff 再复审。

## 评估

**是否可以继续？** 需要先修复（M-1），再进入 TASK-006。

**理由**：本轮修法把 D-2 要防的「autofs 卡住 stat」处理对了。但逐行读挂载表在 procfs 上是超线性的，又排在所有廉价判据与时间检查之前，在挂载多的宿主上形成同一类「hook 被杀即放行」的路径。改法只需几行，而且能顺带收掉已知边角。其余各项都是 Minor。
