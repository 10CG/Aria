# secret-guard W10 尺寸预算收窄：超 8192 的副本在硬截止下按增长量重判（10CG/aria-plugin#217）

> **Level**: 2（本 proposal + A.2 产出的 `detailed-tasks.yaml`）
> **Status**: Draft v3 —— post_spec R1 判 FAIL，改出 v2；R2 再判 FAIL（去重 2C/14M/13m），停止规则触发。owner 2026-10-22 裁定「先钉设计，再实现优先」，post_spec 以 R2 结论关闭（`overridden_by_user: true`）。v3 是设计钉死版：参考实现是一份跑过的原型（W8），下一步 A.2 + post_planning
> **Created**: 2026-10-21（v1 `acd6a95`）；v2 `41e9308`；v3 2026-10-22
> **Linked Issue**: `10CG/aria-plugin#217`
> **关联**：
> - W10 的来源：`10CG/aria-plugin#154`（WP-A `secret-net-l3-and-bypass-paths` TASK-014 的 M6 返工，owner 2026-10-14 裁定 fail-closed）。
> - `10CG/aria-plugin#228`：已转积压，用的是同一批真实流量证据；与本变更的接缝见 Decision 12。
> - `10CG/aria-plugin#216`：协作式时间预算（v1.76.1）。`10CG/aria-plugin#219`：Windows MINGW64 实测缺口。
> - 放宽后会有更多大命令落到这几个既有缺口上：`#139`（含块结构的命令整串判定，credit 对整条命令共享）、`#142`（`$(…)`、反引号、heredoc 内部欠拦）、`#229`（风险行右边界只认空白与行尾）、`#230`（扩展只替换前 64 处命中）。
>
> **认领**：`refs/aria/coordination` 上的 `claims/023236f2/s-28df@0755.yaml`，track `secret-guard-w10-failclosed-narrowing-023236f2`，`linked_issue: 10CG/aria-plugin#217`。
> **不变量继承**（WP-A `openspec/changes/secret-net-l3-and-bypass-paths/detailed-tasks.yaml` 的 invariants）：
> - INV-4：被 `_sg_judge_one` / `_sg_per_segment_eval` 直接或间接调用的函数定义在 source 闸门之上；既有 SC-8 的抽取、阈值、口径、档位不改。
> - INV-5：Rule #7——夹具里的凭据形文本运行时拼装，不打印任何像凭据的值；实验只在 scratchpad，`HOME` 指向私有目录。
> - INV-6：提交页脚与 PR 描述对 `10CG/aria-plugin#154`、`10CG/aria-plugin#203`、`10CG/Aria#221` 只写 `Refs`，不写 Closes / Fixes / Resolves。
> - INV-7：同一时刻只跑一个重实验；时档类测量只在一分钟负载低于 2 时串行跑。本变更的硬截止（P3）是绝对上界，与负载无关；收益数字随负载变化，TASK-004 按 INV-7 重测。
>
> **证据**：`.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/`——`evidence/` W0–W7（v1、v2 阶段）；`v3/` W8–W12（v3 原型与实测，说明与本机依赖见 `v3/README.md`）。命令原文不入库。
> **基线**：aria v1.76.1（`59e333c`）。v1.77.0（`f2e801d`）的 `hooks/` 与之零差异；下文行号都指这一版，B.1 重锚。standards `a611136`。
> **编号约定**：裸写的 `#n` 指 `10CG/aria-plugin#n`；「#217 第 N 项」指该 issue 正文的条目。本文自己的条目写作 What 1–7、P1–P10、BI-1–BI-13、Decision 1–13；owner 裁定点写作「裁定 A–E」。
> **审计**：R1、R2 汇总在 `.aria/audit-reports/`；逐簇处置在同目录的 `dispositions.md`（只追加，不是规格）。

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
| 那 137 条的增长 | 全部不超过 8192（最大 6200） | W1 |
<<<W12-ROWS>>>

### 8192 原本要防什么

M6 用「总长 > 8192 一律拦」，防的是「判定迟到 → 超过 Claude Code 的 5 s → fail-open」。判定的代价没有形状上的上界（R1、R2 实测）：

1. **逐行固定项**：`_sg_compute_credit` 对约 14 个过滤器各调用一次 `_sg_line_match`，每次对副本的每一行求一遍正则，约 0.5–0.9 ms/行。
2. **逐 token 平方项**：`:476` 的 tight 检测，一个 8000 字符的 token 单独约 1 s。
3. **跨行项**：`_SG_PS_REMOTE_T`（`:446`）的 `[^|]*` 跨空白也跨换行，包装词密集的 24 KB 文本单这一条要 2–3 s。
4. **构建项**（R2-A2）：`_sg_vx_apply` 按增长判之后，代价是「替换次数 × 串长」，多字节 locale 下再慢一个量级；61.5 K 字符、16 变量 × 16 引用的整串命令，单次 apply 在 bash 5.2 中文填充下约 12 s。

基线靠「超过 8192 就在第一次替换时停下」同时兜住了这四项。v2 只把大副本判定这一步放进硬截止，R2 证明其余几步（apply 两次、扩展阶段、后续分段）去掉尺寸早停后都失去上界：基线 0.2–3 s 内拦下的输入，v2 要 7–21 s，超过 5 s 即放行（R2-A2）。所以 v3 换了结构：放宽之后的全部工作，整个放进一个硬截止作业。

## What Changes

只改 `hooks/secret-guard.sh`。参考实现是 `v3/W8-v3.diff`，由 `v3/mkv3.py` 从基线机械生成；下文的代码块、注释清单表与真实流量那两行由 `v3/fill.py` 从证据机械填入，与原型逐字一致。B.2 照此落地（行号重锚）。

### 1. 触发点与准入门

**触发点**：只有基线按总长拦的两处——整串 `_sg_vx_apply` 返回 2（`:725`）、分段 `_sg_vx_apply` 返回 2（`:740`）。在这两处，若 `_sg_relax_ok` 成立，`_sg_vx_pass` 不写拦截文案，把基线的原因串和模式存进 `_SG_OV_PAT`、`_SG_OV_MODE`，返回 4；否则照基线写 oversize 文案、返回 2，一字不变。其余所有拦截（VMAX、TMAX、时间检查点、首遍、扩展）都不经过这里。

**准入门** `_sg_relax_ok`，以下全部成立才放宽：

| 条件 | 不成立时 |
|---|---|
| 不在放宽重跑之内（`_SG_RELAXED` 未设） | 不嵌套 |
| `OSTYPE` 以 `linux` 开头（裁定 E：未实测平台维持基线拦） | Windows、macOS 等与基线逐字节相同 |
| 有锚点 `_SG_P0`，且当前 bash 有 `EPOCHREALTIME`（5.0+） | bash 3.2 / 4.x 与基线逐字节相同 |
| 距截止还有时间（见 What 3） | 首遍已用完时间，按基线拦 |
| 没有项目扩展条目生效（`_sg_ext_entries` 为空，照例在命令替换里问） | 有扩展的项目与基线逐字节相同。理由：扩展对副本 > 8192 有自己的绝对尺寸门（`:1563`），放宽之后结局仍是拦，白耗时间（R2 BA2-F-12、KM-F-01） |

### 2. 放宽重跑的规则（`_SG_RELAXED=1`，只在作业里生效）

- **副本上限按增长**：`_sg_vx_apply` 入口 `local … lim=$_SGV_SMAX`；放宽时 `lim=$(( ${#1} + _SGV_GMAX ))`。必须用 `${#1}`，因为循环里 `s` 会被改写（BI-9）。两处比较都改用 `lim`。增长超过 `_SGV_GMAX`（8192）仍拦，原因串见 What 5。放宽之外 `lim` 就是 `_SGV_SMAX`，函数契约不变，所以直调 apply 的既有探针（如 21an）不受影响。
- **副本 > `_SGV_SMAX` 的判定**：`_sg_vx_big_judge` 用一个线性的 `while IFS= read -r` 循环量副本的最长行（BI-10：量的是副本，不是原串）。最长行 > `_SGV_LMAX`（8192）时只匹配规则、不算 credit（裁定 C，调用 `_sg_judge_one … nocredit`）；否则是与小副本相同的普通判定（裁定 A）。
- **副本 ≤ `_SGV_SMAX`**：普通 `_sg_judge_one`。这包括「原串或中间副本 > 8192、最终副本 ≤ 8192」的缩短类（放宽面 R-b）。
- **不变的**：VMAX、TMAX、count 轴、W12 中和、credit 语义。
- **时间检查点**：放宽重跑里，`_sg_vx_pass` 的三个协作式时间检查点改为直接返回 3、不写文案，交给回落（What 4）。

`_sg_judge_one` 增加可选第三参数 `nocredit`：命中规则后、算 credit 之前，若为 `nocredit` 就写 `longline` 文案并返回 2。W12 中和仍在规则循环之前执行，所以 C 路径和普通路径共用同一份中和代码（P10）。不传第三参数时与基线逐字节相同。

<<<CODE-PASS>>>

### 3. 硬截止作业

<<<CODE-FUNCS>>>

要点：

- **截止**：`_SG_P0`（hook 启动时的 `EPOCHREALTIME`，紧跟 `set -uo pipefail` 之后赋值）+ `min(_SG_TIME_BUDGET, 3)` 秒，微秒精度。首遍的时间也算在里面：Claude Code 的 5 s 从 hook 启动算起。
- **作业**：在命令替换里 `set -m`，后台作业因此自成进程组；计时器到点 `kill -KILL` 整个进程组，判定启动的外部进程（`cat`、`sed`）随之终止，不会占住管道（R2-A1、A3）。
- **自检**：作业开工前读 `/proc/$BASHPID/stat`，确认自己是进程组组长，否则返回 9（回落）。组杀的前提由此机械保证，而不是靠约定。`set -m` 只在 bash 5.2.15 上实测过；其他 5.x 若它不生效，作业就不是组长，自检让它回落，是安全的退化。
- **计时器 fork 失败**：`$!` 不变，`tp == jp`，立即杀掉作业并以 99 退出（回落）。
- **结论只取退出码**：0 放行；2 且有文本，原样写出文本；其他一律返回 4，交给回落。文本从不参与判定（R2-A1）。
- **竞争窗口**：作业正常结束、计时器尚未被杀的那一瞬间若恰好到点，计时器会对已回收的进程组发一次 KILL。作业被 `wait` 回收之前 PID 不会复用，回收后到杀掉计时器只隔一条语句；只有同一 PID 在这一瞬间被复用、并且成为新进程组的组长，才会误杀，可以忽略。
- **耗时上界**：hook 结束时间 ≤ max(首遍 + 基线 W10 前段, `_SG_P0` + min(预算, 3) s) + 写文案的几毫秒。首遍本身仍不计时，属 `#228`。

### 4. 回落 = 基线

`_sg_relax_run` 返回 4（截止、时间检查点、自检、内部错误、拦截却无文本）时，`_sg_per_segment_eval` 用存下的 `_SG_OV_PAT`、`_SG_OV_MODE` 写 oversize 文案并返回 2，与基线逐字节相同（P6）。放宽重跑放行时直接返回 0：准入门已保证没有扩展生效，扩展腿本来就是空操作。

<<<CODE-EVAL>>>

### 5. 文案（逐字）

| 场合 | `_sg_emit_blocked` 的参数 | 模板 |
|---|---|---|
| 增长超限，整串 | `"the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" whole oversize` | oversize；`Limit hit:` 行即左列原因串 |
| 增长超限，分段 | `"a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize` | 同上 |
| 超长单行命中规则 | `"$pat" "$seg" "$mode" longline` | 新模板，见下 |
| 截止、时间检查点及其他失败 | （回落）基线原因串 | 基线 oversize 文案，逐字节不变 |

放宽路径上不再出现时间模板，所以不存在 v2 的「打印 4 s、实际 3 s」问题（R2-A21）。`longline` 分支插在 oversize 分支之后，heredoc 正文如下，含三处展开（`${_SGV_LMAX}`、`$pat`、`$(_sg_redact_echo …)`）；首句按 TL2-F7 改为「读取凭据来源，且展开后有超长的行」，因为读取可以在任何一行：

<<<CODE-LONGLINE>>>

分段模式下不追加「Triggering segment」行，因为副本可能很长。

### 6. 小项：删 `:666` 的死代码（#217 小项）

删掉 `_sg_vx_collect` 链式循环里恒为假的 `[[ -z "${_SGV_V[j]}" ]] && continue`。空值在收集时已跳过（`:646`、`:660`），链式代入只会把非空串换成非空值（R1、R2 三席核实）。与放宽机制无关，单独提交，套件全绿即可。W8–W12 的原型不含这一删。

### 7. 注释同步（封闭清单）

核对方法：先把连续的 `# ` 注释行去掉前缀、连接成一行，再 grep。基线上每个「退役」短语都恰好命中一次（`v3/commentsync.py` 的 baseline 模式在基线上实跑为 GREEN，即每个退役短语都能被找到，所以这项检查能红；对未改注释的原型跑 target 模式为 RED）；改完后退役短语为 0 次、「应出现」的词至少 1 次。行号为基线。

<<<COMMENT-TABLE>>>

另外，W9 里 6 组会变用例的标题，与本节第 9、10 处的块头一起改。

## 性质（P）与放宽面

| | 性质 | 原型证据 |
|---|---|---|
| P1 | 不在两个触发点上的命令，退出码与 stderr 与基线逐字节相同 | W9（只有 6 组用例变化）；W12 第 2 节 |
| P2 | 准入门任一条不成立，与基线逐字节相同 | W10 G1–G8；W11 扩展项目；W12 第 3 节（bash 3.2） |
| P3 | 放宽重跑不会越过截止：hook 在 max(首遍 + 基线前段, `_SG_P0` + 截止) 加几毫秒内结束；截止 = min(预算, 3) s | W10 S4–S6（截止 1 s，均在 1.3 s 的判据内返回）；W11 f5like、apply-heavy-cjk（截止 3 s，约 3.0 s 回落） |
| P4 | 结论只取作业退出码；被杀、拦截却无文本、内部错误一律回落 | W10 S3、S6、S7、S8 |
| P5 | 作业的子孙进程不会活过截止，也不占管道；作业结束后没有残留进程 | W10 S5，残留 0 |
| P6 | 回落文案与基线逐字节相同 | `v3/W10b.txt` |
| P7 | 放宽判定就是普通判定；最长行 > 8192 时只匹配规则（`longline`） | W9（21ab、21ac、21al、21ao → `longline`）；W11 segfinding；W12 第 1 节 |
| P8 | 增长 > 8192 仍拦，按输入长度量，两种引用拼写一致 | W9（21ag、21aj → 增长文案） |
| P9 | VMAX、TMAX、count 轴不变 | W9（除 6 组外的 W10 用例全部不变，含 VMAX 的 21ad、count 轴的 21y / 21y2）；W12 第 1 节（VMAX 那 1 条照旧拦） |
| P10 | `nocredit` 路径仍先做 W12 中和 | `v3/W10b.txt` |

**放宽了什么**（CHANGELOG 申报）：

- R-a：代入后副本 > 8192、但增长不超过 8192 的命令，改为完整判定。没有规则命中、或 credit 成立，就放行。整串模式下 credit 对整条命令共享，命令里任一处脱敏过滤（比如无关位置的 `>/dev/null`）都会给整份副本 credit，这是 `#139` 记录的既有缺口，基线放行的命令早已如此（`.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/evidence/E11-real-traffic.txt`：超过 4 KB 的真实命令里，整串模式靠 credit 放行的有 71 条）。
- R-b：缩短类，即原串或中间副本 > 8192、最终副本 ≤ 8192。按普通判定，同样受 R-a 的 credit 语义约束。R2 的 TL2-F4 构造：读一个凭据形路径，另有一处无关的 `echo done >/dev/null`，基线按尺寸拦，v3 放行，凭据会被读出（W11 shrink）。按裁定 A 的口径，这类命令也是「只因尺寸被拦」。
- R-c：这类命令被拦时，文案由「过大」变为增长、`longline` 或普通命中文案。普通命中文案照基线打印整条命令（经 `_sg_redact_echo`），大命令的拦截文本会更长。
- 放宽之后，`#139`、`#142`、`#229`、`#230` 这几个既有缺口覆盖到的流量变多。

**仍然拦**：增长 > 8192；任一值 > 4096（是否被引用都拦）；分段副本总和 > 65536；超长单行命中规则；放宽重跑没在截止前完成；准入门不成立（非 Linux、bash < 5、有扩展、时间已用完）时的一切基线拦截。

**残余（不在本变更内）**：

- 首遍不计时：`#228`。
- ≤ 8192 的判定只受协作式时间预算约束，单次判定可以超过 5 s（R2 TL2-F5：一个 8 KB、4000 行、需要算 credit 的副本，基线 e2e 7–19 s 并放行）。这是基线已有的残余；v1.76.1 CHANGELOG 的「永不 fail-open」对它不成立，本次 CHANGELOG 订正。
- #217 第 2 项（for 列表止于换行）：撤下，转残余 issue（Decision 10）。
- `_sg_vx_collect` 把 heredoc 正文里形似赋值的文本当成 shell 赋值：转残余 issue（Decision 9）。
- count 轴：不变，#217 自己建议暂不改。

## Owner 裁定点

| | 内容 | 裁定 |
|---|---|---|
| A | 大而不膨胀的命令：由「一律拦」改为「完整判定后按结果判」 | 放宽（2026-10-21） |
| B | 时间护栏：判定来不及完成就拦 | 保留 fail-closed（2026-10-21）。v3 的实现方式是硬截止作业 + 回落基线拦截，姿态不变 |
| C | 代入后有超长单行（> 8192）又命中规则：不评估脱敏过滤，直接拦 | 保留 fail-closed（2026-10-21） |
| D | 放行未被引用的超大值 | 撤回（2026-10-21，Decision 9） |
| E | 硬截止未实测的平台（Windows、macOS 等） | 维持基线拦（2026-10-22）；实测通过后另行放开 |
| — | post_spec 闸门 | R2 结论下由 owner 关闭（2026-10-22，`overridden_by_user: true`）；A.2 与 post_planning 照配置跑。post_implementation 与 pre_merge 在配置里是关的，代码阶段的复核由 TASK-003、TASK-005 自愿补上 |

## Success Criteria

每条 SC 写「性质 + 必须抓住的坏实现」两栏。具体形状在 TASK-002 落进套件；坏实现由非作者在 TASK-003 独立构造（memory `adversarial-fixture`：坏实现要像真实的执笔错误）。原型已对每条性质实测（上表），B.2 在真实实现上重跑。

| SC | 性质 | 套件里的形态 | 必须抓住的坏实现 |
|---|---|---|---|
| SC-V1 | P1 | 既有用例除 6 组外全不变；6 组按 W9 改断言 | BI-8：把 VMAX 也放宽（21ad 变红） |
| SC-V2 | P2 | 直调：`OSTYPE` 设为 darwin / msys、`_sg_ext_entries` 桩返回一条、`_SG_RELAXED` 已设、锚点为空、预算 0、锚点前移到截止之前，都不放宽；e2e：扩展项目里的大命令（读扩展所列路径）必须拦；bash 3.2 下 e2e 与基线逐字节相同 | BI-5：准入门漏扩展检查（扩展项目里那条读取被放行）；BI-6：漏平台检查 |
| SC-V3 | P3 | 直调：桩判定睡过 1 s 截止，`_sg_relax_run` 在 1.3 s 内返回 4；e2e：f5like 形状（首遍便宜，后续分段昂贵）墙钟 ≤ 3.3 s；首遍约 2 s 的形状墙钟 ≤ 3.3 s | BI-4：放宽重跑不进作业、在进程内跑；BI-13：锚点设在 `_sg_per_segment_eval` 入口（首遍不计入截止） |
| SC-V4 | P4 | 直调桩：末尾写 `0` 后睡过截止 → 4；返回 2 但无文本 → 4；`set -u` 未定义变量 → 4；返回 3 → 4 | BI-1：从输出文本最后一行解析状态（v2 写法） |
| SC-V5 | P5 | 直调桩：后台子进程继承 stderr 并睡 6 s → 在截止 + 0.3 s 内返回 4，事后按进程名与参数精确计数残留为 0；变异：去掉 `set -m` → 立即返回 4；变异：删掉计时器那一行 → 立即返回 4 | BI-2：只杀作业、不杀进程组且没有组长自检；BI-3：没有计时器 fork 检查 |
| SC-V6 | P6 | e2e：会回落的输入，stderr 与基线逐字节相同 | BI-7：回落时写时间文案，或什么都不写 |
| SC-V7 | P7 | 21ab#1、21ac#3、21al#2、21ao#2 → `longline`（新增 `wpa_x_longline`，钉首行与 `Matched pattern:` 行）；多行大副本 → 普通命中文案；良性大命令 → exit 0 | BI-10：最长行量的是原串（长行由展开产生时漏判） |
| SC-V8 | P8 | 21ag、21aj → 增长文案；引用全部在第 8193 字符之后、分别用 `$NAME` 和 `${NAME}` 两种拼写 | BI-9：`lim` 取被改写后的剩余串 |
| SC-V9 | P9 | 21ad 不变；TMAX 直调廉价形状（1 KB 值 × 8 引用 × 至少 8 段） | BI-8 |
| SC-V10 | P10 | 直调 `_sg_judge_one <超长单行> whole nocredit`：`os.environ.get(...)` 单键读取 → 0；凭据路径读取 → 2 且为 `longline`。`risky_patterns`、`_sg_judge_one`、`_sg_redact_echo` 在 source 闸门之下，须照 SC-8 按锚点抽取后再调（否则返回 127，是假失败；见 `v3/w10b.sh`） | BI-11：`nocredit` 分支绕过 W12 中和 |
| SC-V11 | 结构 | 静态：hook 里没有 `{8193` 形的正则；新函数在 source 闸门之上（INV-4，沿用 SC-30 的闭包检查） | BI-12：用 `[[ =~ .{8193,} ]]` 量行长 |
| SC-V12 | 同步 | 套件头注释计数 = 实跑数；standards 三处计数一致；What 7 的注释清单核对（先连接续行再 grep） | — |

## Impact

- **版本**：v1.77.x PATCH（基线已是 v1.77.0）。版本号由 owner 定。
- **aria `hooks/secret-guard.sh`**：
  - 改：`_sg_vx_apply`、`_sg_vx_pass`、`_sg_per_segment_eval`、`_sg_judge_one`（第三参数）、`_sg_emit_blocked`（`longline` 分支）、`_sg_vx_collect`（删死代码，单独提交）。
  - 新：常量 `_SGV_GMAX`、`_SGV_LMAX`、锚点 `_SG_P0`；函数 `_sg_vx_big_judge`、`_sg_relax_left`、`_sg_relax_ok`、`_sg_relax_job`、`_sg_relax_run`。
  - 注释：What 7 的封闭清单。
- **aria `hooks/tests/secret-guard.test.sh`**：SC-V1–V12；6 组既有用例（21ab 第 2、3 条改成首遍便宜的形状，否则结局随首遍耗时变化）；`wpa_x_longline`、`wpa_L_grow_whole`、`wpa_L_grow_seg`；新用例插在 SC-13 断言之前；头注释计数。
- **aria `CHANGELOG.md`**：草稿见下。
- **standards `conventions/secret-hygiene.md`**：`:23`、`:316`、`:352` 三处测试计数改为发版时实跑的权威值。沿用以往计数同步的做法，只改三处，不加版本行。
- **发布同步面**（owner 门，TASK-006）：照 v1.77.0 的实际改动列全——aria 侧 `.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`VERSION`、`CHANGELOG.md`、`README.md`、`README.zh.md`；主仓侧 `VERSION`、`README.md` 与 i18n README（ja / ko / zh：徽章、Plugin Version 行、translated-from 标记）、`CLAUDE.md` 项目状态段、`docs/architecture/system-architecture.md` §2.8、`docs/architecture/version-scheme.md`、aria gitlink（standards 也变时另加一个）。机械兜底：`m6-version-badge-match`、`i18n-readme-translation-currency`、`plugin-version-arch-docs-match`。
- **Rule #6**（逐 hunk）：改的是 hook，不是 Skill，按 substitute 处理。面向 AI 的文字有三处：`longline` 模板、两条增长原因串。`longline` 的指令行（「Split it…」两条）逐字复用现有 oversize 模板，新增的只是「为什么拦」的描述；两条原因串是 `Limit hit:` 行的描述。判为描述性，以 SC-V7、SC-V8 的逐字断言替代 AB。`rule6_note` 照此写进 A.2 的 `detailed-tasks.yaml`。

**CHANGELOG 草稿**（v1.76.1 体例）：

```
## [1.77.x] - <date> — secret-guard W10 尺寸误拦收窄 (`10CG/aria-plugin#217`; PATCH: 收窄误拦, 不新增 fail-open)

### Security — PreToolUse secret-guard (W10 尺寸预算按增长量判 + 硬截止重判)

- **问题**: W10 (变量展开第二遍) 的副本上限按**总长**计: 任何超过 8192 字符、又引用了已赋值变量的命令都按「过大」拦下, 哪怕展开只多几个字符。维护者本机会话记录里 > 8 KB 的 Bash 命令有 17.6% 因此被拦 (739 条中 130 条)。
- **修复**: 在原来按总长拦的两处, 若满足放宽条件, 改为在一个硬截止作业里按放宽规则重判 W10: 副本上限改按增长 (`_SGV_GMAX` = 8192); 超过 8192 的副本照常完整判定, 其中行长超过 8192 的只匹配规则、不评估脱敏过滤 (新 `longline` 文案)。截止 = hook 启动 + min(`SECRET_GUARD_TIME_BUDGET_S`, 3) s; 作业自成进程组, 到点整组终止; 截止前没判完、或任何异常, 一律按原来的「过大」文案拦 (逐字节相同)。
- **放宽条件**: Linux、bash 5.0+ (`EPOCHREALTIME`)、项目没有启用 `.aria/secret-guard.paths` 扩展、hook 启动后未满截止。其他平台、bash 3.2 / 4.x、启用扩展的项目: 行为与之前完全相同。
- **行为变更**: 本机真实流量里, 被尺寸上限拦下的 137 条命令在 Linux 上放行 <N> 条 (TASK-004 在一分钟负载 < 2 时实测; 原型在负载 2–4 下的数字见证据 W12), 没在截止前判完的按原「过大」文案拦; 这类命令被拦时, 文案由「过大」变为增长超限、`longline` 或普通命中文案; `SECRET_GUARD_TIME_BUDGET_S` 设为 4 时, 截止仍封顶 3 s。
- **放宽面申报**: 这些大命令沿用现有的 credit 语义; 含块结构的命令整串判定, 命令里任一处脱敏过滤都会给整条命令 credit (`#139` 既有缺口, 现覆盖到更多大命令), `#142` / `#229` / `#230` 同理。原串或中间副本超过 8192、代入后变短的命令同样按普通判定。
- **已知限制 (归 `#228` 及新开残余 issue)**: 首遍判定不计时 (`#228`); 不超过 8192 的副本判定只受协作式时间预算约束, 单次可超过 5 s —— v1.76.1 条目里的「永不 fail-open」对此不成立, 特此订正; for 列表跨换行误拦与 heredoc 内赋值形文本误收集 (残余 issue `#<n>`、`#<n>`); Windows / macOS 未实测, 维持原行为。
- 测试: `secret-guard.test.sh` <N> (SC-V1–V12; 6 组既有用例按新语义改断言); bash 3.2.57 + 5.2; 真实流量回放 (只出汇总)。

Refs 10CG/aria-plugin#217, 10CG/aria-plugin#228, 10CG/aria-plugin#139
```

## 证据与复现

| 文件 | 内容 | 生成方式 |
|---|---|---|
| `evidence/W0-corpus-manifest.tsv` | 冻结语料：2412 条 > 4096 字节的真实命令，每条记 `n`、字节数和 sha256，不含原文 | `traffic/manifest.py` |
| `evidence/W1`–`W3` | 138 条的分类、只匹配规则的结果、最长行 | `traffic/w10-traffic.sh`、`rowhit-traffic.sh`、`expline-traffic.sh` |
| `evidence/W4`–`W7` | v2 阶段的硬截止可行性、代价估算、参考实现实测、D 的那一条 | `traffic/` 下同名脚本（历史证据，v3 不再引用其数字） |
| `v3/W8-v3.diff` | v3 原型相对基线的全部改动 | `v3/mkv3.py` |
| `v3/W9-suite.txt` | 套件在基线与原型上各跑一遍 | `v3/run-w9.sh` |
| `v3/W10-mechanism.txt`、`v3/W10b.txt` | 作业机制单测（桩判定）；回落逐字节、`nocredit` 中和 | `v3/run-w10-w11.sh`、`v3/w10b.sh` |
| `v3/W11-adversarial.txt` | 对抗输入矩阵与套件形状 | `v3/run-w10-w11.sh`（输入由 `v3/gen-v3.py` 生成） |
| `v3/W12-real-traffic.txt`、`v3/W12-replay-138.tsv` | 真实流量：138 条回放、300 条逐字节、bash 3.2 下 40 条逐字节 | `v3/run-w12.sh` |
| `v3/W12b-rerun.txt`、`v3/W12b-replay-138.tsv` | 同一原型对 138 条的第二次独立回放，列出两次结局不同的命令 | `v3/run-w12b.sh` |
| `v3/commentsync.py` | What 7 的注释封闭清单核对（基线模式与目标模式） | — |

**复现**：

1. 没有语料的第三方：W8–W11 只需要基线 hook 与本目录脚本（`run-w9.sh`、`run-w10-w11.sh`、`w10b.sh`），见 `v3/README.md`。
2. 有本机会话记录的维护者：用 `.aria/notes/2026-10-20-secret-guard-scan-cost-and-firstpass-cap/traffic/extract.py` 抽到仓外的 `TRAFFIC_DIR`，用 `traffic/refreeze.py` 按 W0 的 sha256 复原编号，再跑 `v3/run-w12.sh`。新会话会让抽取编号漂移，所以只认哈希。
3. 本机依赖（bash 5.2、自建 bash 3.2.57、`/proc`、coreutils `sleep` 小数秒、`taskset`、`jq` 等）与负载口径见 `v3/README.md`。

## Decision record

1. **先量真实流量，再设计**（`#228` 的教训）：137/138 是总长上限的误伤，增长量都很小。
2. **不直接调大 SMAX**：判定成本没有形状上的上界（Why 第 1–4 项），调大只会让构造出来的输入重新「判定迟到 → fail-open」。
3. **用硬截止承载裁定 B**：贵的是判定与构建本身，判定前看表看不到它；硬截止到点就拦，失败方向都是拦。姿态不变，按技术裁定采用，已向 owner 通报。
4. **基线先跑，放宽重跑**（R2-A2）：放宽只在基线本来要按尺寸拦的那一刻触发，其余路径一行不动，P1 由结构保证；重跑的全部工作都在同一个截止里，不再有截止之外的步骤。代价是放宽类命令的前段（collect、截至超限的 apply）会做两遍，这部分有尺寸早停，很便宜（全程耗时见 W12 第 1 节）。
5. **结论只取退出码，作业自成进程组**（R2-A1、A3）：v2 从输出最后一行解析状态，残留子进程可以冒充；又只杀判定子 shell，残留子进程会占住管道。v3 两处都从机制上消除，并用组长自检兜住 `set -m` 失效的情况。
6. **截止用 `EPOCHREALTIME`，没有它就不放宽**（R2-A4）：整秒 `SECONDS` 让实际截止落在 2–4 s 之间。bash 3.2 / 4.x 维持基线，是 fail-closed 方向的技术限定；配合裁定 E，只在 Linux 上放宽。
7. **有扩展的项目不放宽**（R2 KM-F-01、BA2-F-12）：扩展对副本 > 8192 有绝对尺寸门，放宽之后结局仍是拦，却要先花几秒；不放宽就与基线逐字节相同，扩展腿也不必进截止。
8. **回落一律用基线文案**：截止、时间检查点、自检、内部错误，都回到「过大」拦截，逐字节与基线相同。好处是放宽路径不需要自己的时间文案，也就没有 v2「Nothing was matched」与「4 s」两处失实（R2-A21）。
9. **撤回 D**（owner 二次裁定，2026-10-21）：「未被引用」认不全 shell 读变量的方式；能挡住反例的保守判定把真实流量里唯一救下的那 1 条也拦下，收益为 0。根因是 `_sg_vx_collect` 把 heredoc 正文里形似赋值的文本当成赋值，转残余 issue。
10. **撤下「for 列表止于换行」**（R1-A2）：照字面实现会截断反斜杠续行的列表，新增漏检；真实流量 0 例。转残余 issue。
11. **C 复用 `_sg_judge_one`**：W12 中和只有一份代码，`nocredit` 路径不另写规则循环。
12. **整体硬截止留给 `#228`**：v3 是「首遍之后全部步骤进截止」这一中间选项，但只对基线本来就拦的那一类命令生效，所以不改任何命令的放行姿态。把同一机制推广到所有命令（含首遍），会把首遍超时从放行改成拦，改变基线放行类命令的姿态，属 owner 的决定；真实流量里首遍超时只出现过 1 次（测试探针），收益接近 0。作为 `#228` 重启时的选项，TASK-001 在 `#228` 留言记录。
13. **count 轴不在范围内**：#217 自己建议维持 fail-open。

## Tasks（A.2 细化为 detailed-tasks.yaml）

| 任务 | 阶段 | 内容 | 执行 |
|---|---|---|---|
| TASK-001 | B.1 | 入场：续用认领、建分支、重锚行号。开残余 issue（for 列表续行感知；collect 误收 heredoc 内赋值形文本），号写进 CHANGELOG 草稿。在 `#228` 留言（Decision 12 的选项与证据位置），在 `#217` 留言（指向本 Spec 与裁定 A–E）。SC-V 中能在基线上红的项先在基线实跑为红 | 主控 |
| TASK-002 | B.2 | 按 W8 落地 What 1–5、7；What 6 单独提交；套件按 SC-V1–V12 与 Impact 改写 | 新执笔席 |
| TASK-003 | B.2 | 非作者对抗复核：独立构造 BI-1–BI-13，逐个在实现上跑，全部要被抓住；另做一张对抗耗时矩阵（W11 的形状加执笔席自己想到的形状） | qa 席（非作者） |
| TASK-004 | B.2 | 验收：在真实实现上重跑 W9–W12 的脚本（W12 第 1 节按 INV-7 在负载 < 2 时跑）；bash 3.2 逐字节 | 主控 |
| TASK-005 | B.2 | 独立代码审查（本项目 post_implementation / pre_merge 闸门为 off，自愿补上） | code-reviewer 席 |
| TASK-006 | C | 发版（owner 门）：版本号、发布同步面、双推与 `ls-remote` 核验 | owner + 主控 |
| TASK-007 | D | 收口：在 `#217` 逐项对账后关闭——第 1 项完成；小项完成；第 2 项转残余 issue；第 3 项由 owner 撤回；count 轴不变；评论 28512 第 2 点（扩展整串口径）已评估、维持绝对门、写明残余。关闭关键词只出现在阶段 D 的主仓提交，不在发版提交；`#154`、`#203`、`10CG/Aria#221` 只用 `Refs`（INV-6），每次推送前做关键词核对 | 主控 |
