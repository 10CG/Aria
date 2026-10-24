# TASK-003 第一段 清单（阶段 1，盲构造；QA 席，非作者）

对象：aria 实现 `hooks/secret-guard.sh`（sha256 前缀 af4658b6f935，提交 acb644b）；基线 59e333c（e83c5e30f2cc）。
每个编号 = 实现 + 一处改动（生成器 `w14-mutants.py`，逐字替换，替换前断言原文恰出现一次）。
写这份清单时只读过：实现与基线的 diff、proposal What 1-7 与 detailed-tasks 的 INV/TASK-003、run-suite.sh 头注释。没读过套件、sc-cases.sh、sc-direct.sh、mutants.py、W13、b2/pp-r2-seats/evidence。
记号：e2e = 经 stdin JSON 调 hook 的端到端；直调 = source 后直接调函数（套件的直调 helper 那一类）。「露出来」写退出码 / 文案种类（oversize、growth、longline、time、普通 BLOCKED）/ 字节 / 墙钟。

## What 1 触发点与准入门

- **Q-1** `_sg_relax_platform` 的 `${3:-0} <= 3` 改 `< 3`。类：差一（边界比较）。形状：bash 5.3.x 构建（`SC_BASH`=5.3，或直调 `x86_64-pc-linux-gnu 5 3 <osr> ""`）。露出：准入门在 5.3 上关闭，本该放宽的大命令回落成基线 oversize 拦截（退出码 2 而不是放行，文案 oversize 而非放行/growth/longline）；直调返回 1 而应为 0。5.0-5.2 上与实现无差别，PATH 上的 bash 若不是 5.3 则 e2e 看不到。
- **Q-2** `${2:-0} == 5` 改 `>= 5`。类：比较符错。形状：只有 major>=6 且 minor<=3（6.0-6.3）。露出：本该关闭的未实测大版本被放行；只有直调（MAJOR=6）看得到。`5 4` 仍被 `<= 3` 挡住，所以「5.4 保持基线」的用例看不出它。e2e 无法观察（没有 bash 6）。
- **Q-3** 构建串 glob `x86_64-*-linux-gnu*` 改 `x86_64-*-linux-*`。类：漏一个检查（把 gnu 丢了）。形状：`x86_64-pc-linux-musl` 之类 musl / 非 gnu 的 linux 构建串。露出：本该保持基线的平台被放宽；直调返回 0 而应为 1。e2e 无法观察。
- **Q-4** 内核串判据 `*[Mm]icrosoft*` 改 `*Microsoft*`。类：大小写 / 漏一个。形状：osrelease 含小写 `microsoft` 而不含 `WSL` 字样（自编内核的 WSL2，如 `5.15.0-microsoft-custom`）。露出：被放行（应关闭）。真实 WSL2 串 `…-microsoft-standard-WSL2` 因含 `WSL` 仍被 `*WSL*` 挡住，所以只用真实串的用例看不出。只有直调。
- **Q-5** 平台第一参数从 `BASH_VERSINFO[5]` 改成 `$MACHTYPE`。类：读了环境里不该信的值（环境能改写 MACHTYPE）。形状：e2e 在 x86_64 机器上导出 `MACHTYPE=aarch64-unknown-linux-gnu`（或任何非 x86_64 串）再跑大命令。露出：准入门被环境关掉，本该放宽的命令回落成基线 oversize（退出码 2、文案 oversize；应为放行或 growth/longline）。反向（环境把不受支持平台伪装成 x86_64）在本机观察不到。
- **Q-6** `_sg_relax_noext` 里 `[[ -z "$root" || ! -e … ]]` 的 `||` 改 `&&`。类：逻辑连接词错。形状：找得到项目根（`CLAUDE_PROJECT_DIR` 或 stdin cwd 指向有 `.aria` 的目录）且没有 `.aria/secret-guard.paths`。露出：放宽永不进入（只有找不到项目根才放宽），回落成基线 oversize；退出码 2 而应为放行 / growth / longline。
- **Q-7** 分段触发点 `if _sg_relax_ok; then` 改 `if false; then`。类：漏一个触发点（两处只接了一处）。形状：多段命令（含 `;` `&&`），某一段的代入副本 > 8192。露出：该段按基线 oversize 拦（Limit hit: a command segment is longer than 8192 …），应放宽（放行 / growth / longline）。整串触发点不受影响。
- **Q-8** `! -e "$root/.aria/secret-guard.paths"` 改 `! -f`。类：谓词用错（-e 与 -f）。形状：`.aria/secret-guard.paths` 是目录。露出：目录被当成没有扩展而放宽；应与基线逐字节相同（拦）。放宽下本会放行的大命令退出码 0 而应为 2；文件（空 / 不可读）两态不受影响。

## What 2 放宽重跑的规则

- **Q-9** `_sg_vx_apply`：在每个变量的循环体里用当前（已被前面变量改写的）`s` 长度重算 `lim`，而不是入口的 `${#1}`（BI-9 的反面）。类：用错变量。形状：两个及以上变量，累计增长在 8193 到 8192+第一个变量增长之间，每个变量单独增长 <= 8192（如 A 增 4000、B 增 4300）。露出：实现按增长拦（growth 文案，退出码 2），变异放行或转入判定。单变量（含 `${A}` 与 `$A` 两种拼写）看不出。
- **Q-10** `_sg_vx_collect` 重跑里 for 语句的计数上限不取消（`cf` 保持 8，只取消赋值的 16）。类：漏一处同类上限（三个计数上限只取消两个）。形状：放宽重跑里有 >= 9 条 `for X in …` 且读凭据的是第 9 条之后的循环变量。露出：该变量没被收集，读取不被判，退出码 0 而应为 2（普通 BLOCKED）。
- **Q-11** `_sg_vx_replace` 里 `gc=1000000` 那行取消（`${NAME}` 拼写的每变量 8 次上限在重跑里保留）。类：漏一处同类上限。形状：一个段 / 整串里同一变量的 `${V}` 引用 >= 9 次，读凭据的是第 9 次之后的引用。露出：第 9 次起不代入，退出码 0 而应为 2。
- **Q-12** `_sg_vx_apply` 入口去掉 `gc=1000000`（`$NAME` 拼写的 8 次上限保留）。类：同上，另一个拼写。形状：同一变量的 `$V` 引用 >= 9 次，读取在第 9 次之后。露出：退出码 0 而应为 2。
- **Q-13** `_sg_vx_big_judge`：`max > _SGV_LMAX` 改 `>=`。类：差一。形状：副本 > 8192，最长行恰为 8192 字符，行内命中规则且读取带脱敏过滤（`| wc -c`）。露出：实现走普通判定（有 credit，放行，退出码 0），变异走 nocredit（longline 拦，退出码 2）。
- **Q-14** `_sg_vx_big_judge`：`while IFS= read -r` 去掉 `IFS=`。类：漏一个（读行不保空白）。形状：某一行的长度 > 8192 只是因为首尾的空格 / 制表符（去掉后 <= 8192）。露出：实现按 nocredit 拦（longline），变异把行量短后走普通判定，credit 放行（退出码 0）或在超时下回落。
- **Q-15** `_sg_judge_one`：nocredit 分支挪到 credit 计算之后（顺序颠倒）。类：顺序颠倒。形状：一行 >= 16 KB 且命中规则的大副本（credit 的代价是长度平方，16 KB 约 3 s）。露出：结论仍是拦，但先花掉 O(n²) 的 credit：超过截止后回落成基线 oversize 文案（kind 由 longline 变 oversize），墙钟顶到约 3 s；9 KB 左右只多约 1 s（墙钟上界）。
- **Q-31** `lim` 用 `_SGV_SMAX` 代替 `_SGV_GMAX`。类：用错常量。**当前取值两者都是 8192，e2e 与字节层面等价**；只有直调时改动常量（source 后令 `_SGV_GMAX` 或 `_SGV_SMAX` 取不同值）才露出：增长限不再随 GMAX 变化。这是潜伏缺口：以后改任一常量才会发作。

## What 3 硬截止作业

- **Q-16** 计时器 `sleep "$_SG_LEFT"` 改 `sleep "$_SG_TIME_BUDGET"`。类：用错变量（剩余时间 vs 预算）。形状：首遍已花掉一段时间 t1、重跑又慢到被截止。露出：截止变成 作业启动 + 3 s 而不是 hook 启动 + 3 s，墙钟约 t1+3 s（越过 max(T_trigger,3 s)+0.3 s 的上界）；文案同回落。只有计时类用例看得到。
- **Q-17** 命令替换里去掉 `exec 2>/dev/null`。类：作用域 / 重定向漏一处。形状：作业被截止杀死（回落）。露出：bash 把「Killed」之类的作业通报写到 hook 自己的 stderr，回落输出 = 基线文案 + 多出的通报行（[bytes] 与基线不同）；正常放行 / 正常拦不受影响。
- **Q-18** `printf '%s\n' "$out" >&2` 改 `printf '%s'`。类：字节（丢结尾换行）。形状：作业以 2 退出并带文本（growth / longline）。露出：stderr 少最后一个换行，退出码与文案种类都不变；只有逐字节比对看得到。
- **Q-19** 删 `wait` 之后的 `kill -KILL -- "-$jp"`。类：漏清理。形状：判定在作业组里留下后代（持有管道的子进程），或正常结束后计时器还在睡。露出：正常流程里计时器（sleep）在 hook 结束后继续睡到截止（残留进程，最多约 3 s）；若有持管道的后代，命令替换等到它结束，墙钟越过截止。多半只有注入遗留后代的用例（规格里的 V5-S9、V5-S13b 一类）看得到。

## What 4 回落 = 基线逐字节

- **Q-20** 分段触发点存的原因串改成整串那句（`the command is longer than …`，二者是相邻两行的复制粘贴）。类：复制粘贴。形状：多段命令的分段触发点之后回落（截止、自检失败、时间检查点等）。露出：回落输出的 `Limit hit:` 行是 whole 的措辞，与基线的 `a command segment is longer than …` 字节不同（[bytes]）；退出码仍 2。整串回落不受影响。
- **Q-29** `_sg_per_segment_eval` 里 `[[ $rc -eq 4 ]]` 改 `-eq 3`。类：退出码映射错。形状：任何回落（截止、自检、计时器未起…）。露出：不写基线文案，`return 4` 漏给调用方：退出码不再是 2、stderr 无文案（fail-open）；[status] 与 [bytes] 同时红。
- **Q-30** `_sg_relax_ok` 里去掉 `_sg_relax_left || return 1`。类：漏一个检查。**hook 输出层面等价**：触发点得到 4，`_sg_relax_run` 自己先测剩余时间，没有时间就返回 4 走同一段基线文案，字节与退出码都相同。只有直调 `_sg_relax_ok`（无剩余时间时应返回 1，变异返回 0）才露出。

## What 5 文案

- **Q-21** 分段 growth 文案改成整串措辞（`the command grows by more than …`）。类：复制粘贴。形状：多段命令里某段增长 > 8192。露出：`Limit hit:` 行措辞不对，文案种类（oversize）与退出码不变。
- **Q-22** `_sg_emit_blocked "$pat" "$seg" "$mode" longline` 的 pat 与 seg 对调。类：参数顺序颠倒。形状：任何 longline 拦。露出：`Matched pattern:` 后面是整份展开后的副本（> 8 KB，含展开出的路径），stderr 体积暴涨，规则本身不见了；首行文案种类不变。
- **Q-23** longline 模板里 `Command was` 一行的 `${command:0:200}` 改 `${seg:0:200}`。类：用错变量。形状：展开后的副本前 200 字符与原命令前 200 字符不同（分段模式下读取那一段；或命令开头就引用变量）。露出：回显的是展开副本（含展开出的值）而不是原命令；退出码、种类不变，只有 `Command was` 一行的字节不同。

## 时间预算与锚点

- **Q-26** `cap=$(( budget < 3 ? budget : 3 ))` 改 `>`（min 变 max）。类：比较符写反。形状：`SECRET_GUARD_TIME_BUDGET_S` 取 1 / 2（预算 < 3）或 4。露出：截止仍是 3 s（预算 1 时应约 1 s），预算 4 时变成 4 s（应 3 s）；默认预算 3 时等价。墙钟。
- **Q-27** `printf -v _SG_LEFT '%d.%06d'` 改 `'%d.%d'`。类：格式 / 单位。形状：剩余时间的小数部分 < 0.1 s（如 1.05 s 写成 `1.50000`）。露出：计时器多睡最多约 0.9 s；`_SG_LEFT` 字符串不对。e2e 随机出现（约十分之一），确定性复现要直调 `_sg_relax_left` 并选好 `_SG_P0`。
- **Q-28** 去掉「时钟回拨不延长截止」那一行封顶。类：漏一个检查。形状：`_SG_P0` 在未来（直调把它设成现在 + N s；EPOCHREALTIME 不能赋值，e2e 造不出）。露出：`_SG_LEFT` 超过 cap（最多 N+3 s），截止被推后；真实场景里意味着越过 Claude Code 的 5 s 而 fail-open。只有直调。
- **Q-24** 在 `_sg_vx_collect` 开头与 `_SG_T0=$SECONDS` 并排重取 `_SG_P0`（锚点从 hook 启动变成 W10 一遍的开始）。类：锚点取错时刻。形状：首遍（hook 启动、解析、`_sg_core_eval`）本身就慢，重跑又被截止。露出：首遍的时间不再算进 3 s，墙钟 = 首遍 + 3 s；文案同回落。首遍快时差几毫秒，看不出；需要造慢首遍（BI-13、V3-E3 一类）。
- **Q-25** 顶层 `_SG_RELAXED=` 改 `_SG_RELAXED=${_SG_RELAXED:-}`。类：读了环境里不该信的值。形状：e2e 在环境里带 `_SG_RELAXED=1` 启动 hook，再给一条大命令。露出：顶层直接按放宽规则走：没有准入门、没有截止、没有计数上限，文案是 growth（或放行）而不是基线 oversize；慢命令可拖到很久（规格里实测 25 s 后放行，PP1-A2）。

## 等价性与可观察性小结

- 我认为 e2e 与字节层面等价的：**Q-30**（理由见上，`_sg_relax_run` 兜同一结局）、**Q-31**（常量当前同值，只有直调改常量露出）。这两个若在套件里「红」，要么套件有直调探针，要么我的等价判断错了，两种都要看。
- 只有直调能看见的：Q-2、Q-3、Q-4、Q-28、Q-27（确定性）、Q-30、Q-31；e2e 随主机而异的：Q-1（需 5.3）。这几个的价值在于看直调 helper 覆盖了多少参数组合。
- 未选的点子：`/proc/sys/fs/binfmt_misc/WSLInterop` 的路径写错 / 去掉。非 WSL 主机上这条分支永远为假，e2e 与直调都造不出这个文件，所以它在本机不可观察；记作「不可测的一条」，不构造。
