---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T19:06:40.495Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — backend-architect 席（bash 语义与机制）

被审：`detailed-tasks.yaml` v3.1（`95cf1de7`）、proposal v3.1、原型 `v31/W8-v31.diff`（我用 `mkv31.py` 重新生成，sha256 前缀 `9f61db0e7b8b`，与 W13 页眉一致）、验收 `v31/sc-cases.sh` + `sc-direct.sh` + `shim/`。

**一句话结论**：原型的机制本身（进程组作业、作业内计时器、`kill -0` 确认、`wait` 后组杀、`exec 2>/dev/null`、退出码 77、`_SG_RELAXED` 初始化、`BASH_VERSINFO` 准入）在 bash 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 上我没有找到缺陷；**但 sc-cases.sh 不是它声称的那种验收**：我自己想的 12 个「像真实执笔错误」的坏实现（M1–M11、M14）没有一个被设计用例抓住（sc-cases.sh 94/94 全绿，只有与被测差异无关的抖动 / 负载红），其中 M1（扩展门）、M4 与 M11（裁定 C）、M9（整串增长拦截）我用端到端实证了**应拦的命令得到 rc=0**。另两个对照坏实现（M12 回落返回 0、M13 计时器打错组）被正确抓住。没有 Critical；Major 8 条（F1–F7、F13），Minor 11 条。

## 审计结论

编号 BA2-Fn。「针对」栏：计划 = detailed-tasks.yaml；proposal = proposal.md v3.1；原型 = W8-v31；验收 = sc-cases.sh / sc-direct.sh / shim / 证据。type：issue / risk / decision。

### Major

**BA2-F1** · issue · Major · testing · scope: `v31/sc-cases.sh` V2-E9、`v31/sc-direct.sh` V2-G4 · 针对：验收用例
准入门的「有没有扩展」只用 `CLAUDE_PROJECT_DIR` 驱动测试；`_sg_relax_noext` 实际经 `_sg_ext_root`，那里还有两条分支：`CLAUDE_PROJECT_DIR` 为空 → 取 stdin 的 `cwd`；`CLAUDE_PROJECT_DIR` 非空则它优先。旧套件已把这三种根解析各钉了一例（`secret-guard.test.sh:2336` SC-19g、`:2338` SC-19ap、`:2340` SC-19h），新门一例都没有。
- 变异 M1（门只认 `CLAUDE_PROJECT_DIR`，丢掉 stdin cwd 路径）：`sc-cases.sh` **94/94 全绿**。
- 行为实证：`in/ext-read-cwd.json`（JSON 里 `cwd` 指向列了该路径的项目，不设 `CLAUDE_PROJECT_DIR`）——基线 rc=2、v3.1 rc=2、M1 **rc=0（放行）**。即「有扩展的项目与基线逐字节相同」（P2/裁定 E 边界）在 cwd 路由上可被一处执笔错误悄悄破掉，而验收不红。
- 建议：加 e2e `V2-E17-extension-via-stdin-cwd`（输入带 `cwd`、不设环境变量，对基线逐字节相同）；直调 `V2-G4` 补三例（空 `CLAUDE_PROJECT_DIR` 落到 `cwd`、`CLAUDE_PROJECT_DIR` 优先于 `cwd`、仅 `cwd`）。同族：PP1-A27（该簇补了 noext 的文件状态，没补根解析）。

**BA2-F2** · issue · Major · testing · scope: `V10-N*`、`V7-E14`、`V9-E10`；P7/P10；裁定 C · 针对：验收用例
裁定 C（「代入后有超长单行又命中规则：不评估脱敏过滤，直接拦」，owner 保留 fail-closed）没有一例带脱敏过滤的用例。所有 longline 用例（N2、N4、E14、E10）的读取都不带过滤，所以「先算 credit、没有 credit 才出 longline 文案」这种顺序错误与正确实现输出完全相同。
- 变异 M4（`_sg_judge_one` 里 `nocredit` 检查挪到 credit 计算之后）：**94/94 全绿**。变异 M11（分段模式不走 `_sg_vx_big_judge`）：除一条无关抖动外 **93/94 全绿**（见 F7）。
- 行为实证（`demo-all.sh`）：读 app.ini 且带 `| wc -c`、代入后单行 > 8192 的命令——v3.1 在整串与分段模式都 rc=2 longline；M4 在整串与分段都 **rc=0 放行**；M11 在分段 **rc=0 放行**（整串仍拦）。
- 另：分段模式的「大副本走 big_judge」分支（`_sg_vx_pass` 分段循环那一行）没有任何分段 e2e 用例，所有 longline / 增长 / 回落 e2e 形状都是整串模式（开头一个括号）。
- 建议：直调 `V10-N6-filtered-long-line-rows-only`（`_sg_judge_one "<读取 | wc -c> + 超长行" whole nocredit` → rc=2 且 longline）；e2e 加整串与分段各一条「超长行 + 过滤 → 拦且 longline」（形状见 `in2/whole-longline-filtered.txt`、`seg-longline-filtered.txt`，读取路径运行时拼装）。

**BA2-F3** · issue · Major · testing · scope: SC-V8 / P8；`_sg_vx_pass` 重跑分支「增长超限」 · 针对：验收用例 + proposal 的证据列
重跑里「增长 > 8192 仍拦」（整串与分段两条文案）在 sc-cases.sh 里**没有 e2e 也没有直调**：`V8-D1`–`D3` 只测 `_sg_vx_apply` 的返回码。proposal P8 把 e2e 证据指给 W9（旧套件 21ag、21aj），但 W9 里这两例是**分段**文案（`W9-suite.txt`：`a command segment grows by more than`），**整串增长文案没有任何旧例**。`sc-cases.sh` 的 `kind()` 有 `growth` 分类，却没有任何用例期望它（死代码）。
- 变异 M9（整串、重跑内增长超限 → `return 0`，即**放行**）：**94/94 全绿**。变异 M10（分段同上）：sc-cases 无红（只有抖动），要靠 TASK-002 改完断言的 21ag/21aj 才会覆盖。
- 行为实证：形状 `(true); f=<app.ini 路径>; a=<4000 个 x>; : $a $a $a $a; cat $f`（`in2/growth-whole.txt`）——基线 rc=2 oversize、v3.1 rc=2 growth、M9 **rc=0**。
- 建议：e2e `V8-E19-growth-whole-blocked`（rc=2、`kind=growth`）与分段版；直调 `_SG_RELAXED=1` 下 `_sg_vx_pass` 对增长超限返回 2 且文案含 `grows by more than`。BI 清单补一条「重跑内增长超限放行」并指定这些用例。

**BA2-F4** · issue · Major · testing · scope: P6 / SC-V6；`V6-E2`、`V3-E3`–`E5`、`V2-E6`、`V2-E7` · 针对：验收用例
P6（「回落文案与基线逐字节相同」）只在整串模式验证。分段触发点保存的是另一条原因串（`a command segment is longer than …`），这行代码没有任何用例走到回落。
- 变异 M5（分段触发点存成整串的原因串）：**94/94 全绿**。
- 确定性实证（不靠时序）：补丁副本里把 `_sg_relax_run` 换成 `return 4`，分段形状 `p=<4000 x>; : $p $p $p`（`in2/seg-cheap.txt`）——基线 / v3.1 的 stderr sha `fe26cd8f` 相同（`Limit hit: a command segment is longer…`），M5 为 `67193bea`（`the command is longer…`）。整串形状三者相同。
- 注意：我先试了「分段 + sed shim 拖住作业」的 e2e 做法，在本机 1–4 s 的分段首遍自然耗时下（loadavg 3–8）门被关掉，demo 无法稳定出结果——分段模式的回落用 stub 做确定性用例更合适。
- 建议：`V6-E21-fallback-bytes-segment`：对 `_sg_relax_run` 打桩返回 4 的 hook 副本（`demo` 里的 python 替换一行即可），与基线 stderr 比字节。

**BA2-F5** · issue · Major · testing · scope: `_sg_relax_job` 的组长自检（W8 hunk「`/proc/$BASHPID/stat`」三行）；P5；proposal What 3 · 针对：验收用例
proposal 说「`set -m` 不生效的 bash 由此安全退化」，但**没有任何用例让这三行执行拒绝分支**。`set -m` 在五个 bash 上都生效，所以自检永不触发；去掉它，一个不是组长的作业会照常判定，计时器 `kill -- -$me` 打到不存在的组，截止形同虚设（超过 5 s → CC 杀 hook → 放行）。BI-2 同时去掉了 `set -m` 与自检，被抓的是「杀不到组」，单独去自检无人抓。
- 变异 M7（只去自检）：**94/94 全绿**。
- 直调实证（`demo78.sh`）：在非组长的前台子 shell 里调 `_sg_relax_job`——v3.1 返回 9（拒绝判定），M7 返回 **77**（照判并「放行」）。
- 建议：直调 `V5-S15-job-refuses-outside-group-leader`：`( _sg_relax_job x )` 返回 9，且桩判定的标记文件不存在。

**BA2-F6** · issue · Major · testing · scope: `_sg_vx_pass` 三处「重跑里时间检查点 `return 3`」；P4/P6 · 针对：验收用例
重跑里三个协作式时间检查点（collect 链、整串、分段循环）必须返回 3、不写 time 文案，由回落写基线文案。e2e 到不了它们（整秒 `SECONDS` 检查点被硬截止抢先），sc-direct 也没有直调。
- 变异 M8（三行都删，重跑改写 time 文案并返回 2）：**94/94 全绿**。
- 直调实证：`_SG_RELAXED=1`、`SECRET_GUARD_TIME_BUDGET_S=0`、`_sg_vx_pass` 整串/分段——v3.1 返回 3、stderr 0 字节；M8 返回 2、stderr 883 字节。
- 影响：最坏是回落文案不是基线的（P6 破坏，方向仍是拦），但这是「time 文案只存在于首遍」的唯一机械保证。
- 建议：`V4-S12-rerun-checkpoints-return-3`，整串与分段各一；collect 检查点需要 ≥ 2 个变量才进链式循环。

**BA2-F7** · issue · Major · testing · scope: `sc-direct.sh` `V5-S13b`（及 `V5-S12`）· 针对：验收用例
这两条用**全局** `ps -eo args | awk '$1=="sleep" && $2=="7.777"'`（S12 是五个固定参数）判「没有残留」，且 S13b 在异步 SIGKILL 之后**立刻**观察、没有宽限。结果是：好实现上会假红，而且与同机其他套件实例互相可见。
- 实证：我的 13 次变异体整轮里，**M10 与 M11 各红一次 `V5-S13b`**（`a child … still alive right after _sg_relax_run returned: 1`），loadavg 1.9–2.6（低于 INV-7 的 2 的边缘）；这两个变异体只改 `_sg_vx_pass` 的增长 / 分段分支，S13 的桩不经过那里，所以红与被测差异无关。隔离复现（`flake.sh`，150 次，loadavg 8.5，唯一参数 `7.7773`）：1 次「返回后立刻可见、20 ms 后消失」，即纯竞态。另一席同时在跑同一套件时，固定参数还会看到对方（或 BI-15 一类变异体）的残留。
- 建议：参数带 `$$`/`$RANDOM` 唯一化，或桩把自己的 PID 写进文件、用 `kill -0` 判；加 ≤ 1 s 的轮询宽限（BI-15 的残留活 7.8 s，仍可区分）。同族：PP1-A8、A34（桩的形状）。

**BA2-F13** · issue · Major · testing / documentation · scope: INV-7（「sc-cases.sh 的计时判据…不受本条约束」）；`v31/README.md`「计时判据由 shim 的固定延迟给出，与负载无关」；`V3-E3`、`V3-E5`、`V6-E2`、`V2-E7`、`V9-E10`、`V9-E11`、`V7-E1` · 针对：计划 + 验收
这句话只对**下界**成立。上界窗口、要求「重跑在截止前完成」的放行类 / 判定类用例、以及 shim 停顿的落点，都依赖机器的自然速度；在本机这个多席位并行的状态（loadavg 常在 8–12）下**好实现会红**：
- loadavg 2.8 时截止用例的 ε（墙钟 − 3.0）= 0.02 s；loadavg 9.7–10.5 时 V6-E2 = 3.35 s（窗口 ≤ 3.6）、V3-E5 = 1.49 s（窗口 ≤ 1.6，**余量 0.11 s**）、V2-E7 = 3.76 s。
- v3.1 原型 × bash 5.0.18（loadavg 11.5→11.2）：90/94，红 V6-E2（4.14 s）、V3-E3（**rc=124，12.06 s**）、V3-E5（**11.35 s**）、V9-E11；× bash 5.3.20（11.2→9.5）：91/94，红 V3-E3（rc=124）、V3-E5（11.39 s）、V9-E11；M14（默认环境下行为同原型）× bash 5.2（10.8→11.5）：91/94，红 V2-E7（6.16 s）、V9-E10、V9-E11。除这些时间相关用例外其余 90 / 91 例全绿——是负载红，不是逻辑红。
- 机制：V3-E3 的 `SC_DELAY_jq=1.5` 吃掉截止的一半，剩下 1.5 s 要装下首遍 + 基线 W10 前段 + 准入门；V3-E5 预算 1 s 同理。机器慢到触发点晚于截止时准入门关闭（行为正确），于是 `SC_DELAY_sed=10` 的停顿落在**父进程**基线文案的第一次 `sed` 上而不是作业里，整例变成 10–12 s（V3-E3 被 `timeout 12` 杀）。V9-E10 / E11 自然耗时 0.25 s / 0.75 s，被截止截断后回落成 oversize 文案。
- 建议：(1) INV-7 与 README 改成「下界与字节比对不依赖负载；上界与放行类用例依赖自然速度，须在 loadavg < 2 下跑，或用同轮基线墙钟做校准」；(2) 套件开头量一次基线自然耗时，超阈值就把这批用例整体 SKIP 并计数（附原因），不给假红；(3) 上界放宽到 `lo + 1.0`（现有坏实现的偏差 ≥ +1.5 s，不丢区分力）；(4) V3-E3 的 jq 延迟 1.5 s 降到 1.0 s；(5) TASK-003 的「max(T_trigger, 3 s) + 0.3 s」同样挂 INV-7 的负载条件。同族：PP1-A29、A36。

### Minor

**BA2-F8** · issue · Minor · testing · scope: `_sg_relax_left` 的 `printf -v _SG_LEFT '%d.%06d'` · 针对：验收用例
变异 M2（`%d.%d`，微秒不补零）：94/94 全绿。剩余时间的小数部分 < 0.1 s 时会错成大数：实测剩余 2.05 s 时 v3.1 打印 `2.048736`，M2 打印 `2.48782`（截止晚 0.44 s，最坏晚 0.9 s，仍 < 5 s）。所有 e2e 与直调的剩余时间小数都 ≥ .5，从不走到。建议：直调 `V3-G12`：`_SG_P0 = 现在 − 0.95`、预算 3，断言 `2.0 < left < 2.1`。

**BA2-F9** · issue · Minor · testing · scope: `_sg_vx_big_judge` 的 `max > _SGV_LMAX` · 针对：验收用例
变异 M6（`>=`）：94/94 全绿。实证：副本最长行恰为 8192（`in2/lmax-8192.txt`）时 v3.1 走普通判定（`finding` 文案），M6 走 longline；8193 两者相同。V8 对 GMAX 有 8192/8193 边界对，对 LMAX 没有。建议：`V7-N6-lmax-boundary-8192-8193`（直调，8192 → finding、8193 → longline）。

**BA2-F10** · issue · Minor · testing · scope: `_sg_vx_big_judge` 的 `(( seen )) || max=…` 哨兵（PP1-A27 的产物）· 针对：验收用例
变异 M3（删哨兵）：94/94 全绿；该分支没有任何用例，也没有可触发它的手段被写进套件。我没能在本机造出真实触发（here-string 失败要 fd / 临时文件耗尽），**未核实**其可达性。有确定性办法：直调前定义一个返回 1 的 `read` 函数遮住内建，循环零次，断言走「只匹配规则」。

**BA2-F11** · issue · Minor · testing · scope: `V2-G3b`、`V2-E8` · 针对：验收用例
这两条只改 `OSTYPE` 来证明「准入门不读环境」。实测四个 5.x 里 `MACHTYPE`、`OSTYPE`、`HOSTTYPE` 都可被环境改写（`BASH_VERSINFO`、`EPOCHREALTIME` 不可）。变异 M14（平台串取 `$MACHTYPE`）与原型在所有现有用例下行为相同。结果见「变异测试」。建议：`V2-G3b` 同时设 `MACHTYPE`、`HOSTTYPE`。

**BA2-F12** · issue · Minor · testing · scope: `sc-direct.sh` 开头 · 针对：验收用例
e2e 的 `run()` 用 `env -u SECRET_GUARD_TIME_BUDGET_S` 清环境，直调部分没有。实证：调用者环境里 `SECRET_GUARD_TIME_BUDGET_S=0` 时，好实现上 `V2-G1-gate` 与 `V2-G4-project-without-extension-file` 假红（该变量是旧套件为确定性检查点用过的）。建议：`sc-direct.sh` 开头 `unset SECRET_GUARD_TIME_BUDGET_S CLAUDE_PROJECT_DIR`。

**BA2-F14** · issue · Minor · documentation · scope: TASK-002 acceptance「SC_BASH 依次取 5.0.18 / …」· 针对：计划
两种读法：旧套件约 830 例是否也经 `SC_BASH` 执行 hook？旧套件的 `wpa_rc` 直接 `"$WPA_HOOK"`（shebang 选 bash）。若只指搬入的 94 例，应写明；若指全部，TASK-002 要改的不止「搬入」。

**BA2-F15** · issue · Minor · documentation · scope: TASK-002 套件头注释 · 针对：计划
搬入后套件新增依赖 `taskset`、`nice`、`timeout`、`ps -eo args`、`readlink -f`、`mktemp -p`、`python3`、GNU `sleep` 小数秒；旧套件头注释只要求 jq（python3 限一处）。hook 声明支持 macOS / Windows，套件在这些平台上的处置（SKIP 并计数）计划里只写了 locale 一种。另：`sc-cases.sh` 默认从 `git -C <root>/aria show 59e333c:hooks/secret-guard.sh` 取基线（主仓布局）；搬进 aria 仓后该路径不存在，浅克隆里也没有该提交，现在是 `SETUP` 直接 `exit 3`——应改为 SKIP 并计数（旧套件的 SC-8 / SC-9a 已有先例）。建议在 TASK-002 的 design 里列依赖、基线来源与非 Linux / 无历史时的 SKIP 规则。

**BA2-F16** · risk · Minor · architecture · scope: Decision 16；`_sg_relax_platform`；CHANGELOG 草稿「实测过的版本」· 针对：proposal
准入是 major.minor（5.0–5.3），证据是四个具体构建（5.0.18 / 5.1.16 / 5.2.15 / 5.3.20，均 x86_64）。补丁级与架构（`V2-G2` 表把 aarch64 glibc 记为放宽）没有实测。运行期自检（组长 + 计时器在跑）把「机制在此 bash 上失效」兜成回落，方向是 fail-closed，所以我不认为这是风险点，只是措辞与范围不等。建议 CHANGELOG 写成「bash 5.0–5.3（实测 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20，x86_64）」。

**BA2-F17** · issue · Minor · testing · scope: `V7-E15` · 针对：验收用例
判据是「放行，或（deadline 截断时）与基线字节相同」。一个永远回落的实现也过 E15；它证明的「credit 照常」要靠 `V7-E1` 才间接成立。可保留（为抗负载），但应在注释里写明它不单独证明 credit，或再配一条有 shim 保证不被截断的 credit 用例。

**BA2-F18** · risk · Minor · testing · scope: `V5-S10`、`V5-S10b`（`ulimit -u 1`）· 针对：验收用例
用 `ulimit -u 1` 制造 fork 失败，要求调用者既非 uid 0 也无 CAP_SYS_RESOURCE（`man 2 setrlimit`：RLIMIT_NPROC 对这类进程不执行）。多数 CI 容器以 root 跑，那时注入无效：计时器照常起来、桩判定照常执行，`V5-S10` 期望 rc=4 实得 0，`V5-S10b` 期望标记文件不存在而它存在——好实现恒红。`sc-direct.sh` 只检查注入文本被替换（`*"ulimit -u 1"*`），不探测注入是否生效，也没有 SKIP 路径。aria 当前 CI（`.forgejo/workflows/` 只有 `issue-triage-tests.yml`）不跑这套件，所以是潜在风险；**未在 root 下实跑**（本机 uid 1000），依据是 man 文档。建议：先用 `( ulimit -u 1; /bin/true & wait $! )` 探测 fork 是否真被拒绝，没被拒绝就 SKIP 并计数。

**BA2-F19** · risk · Minor · architecture · scope: 截止封顶 `min(预算, 3)`；proposal What 3「耗时上界」· 针对：proposal
CC 的 5 s 给回落路径留 2 s 余量，而 ε 的实测只有轻负载数字（≤ 0.1 s）。本机 loadavg ≈ 10、nice 19 + 2 核下，hook 内部时间线（jq 首次调用起算，`shimlog2/` 记录）显示截止后 0.19–0.53 s 才开始写回落文案（bash 5.0.18 / 5.2.15 / 5.3.20 分别 0.53 / 0.24 / 0.19 s），端到端收尾 3.3–4.1 s。离 5 s 仍有 ≥ 0.9 s，我不认为越界，但余量不宽：ε 一旦 > 2 s，结果是 CC 超时放行，而基线对这类命令是 < 1 s 就拦。建议 TASK-003 的耗时矩阵在 loadavg ≥ 8 下记 ε 的分布并把「余量 ≥ X」写进验收（INV-7 的负载门槛不适用于测量余量本身）；若尾部 > 1 s，把封顶从 3 s 降到 2.5 s 属技术级决定。

## 变异测试

方法：每个坏实现 = v3.1 原型（`mkv31.py` 生成）+ 一处改动，写在 `mut.py`（每处替换断言恰好命中一次）；**预测先写进 `mut/predictions.tsv`，再跑**。跑法：`taskset -c 0,1 nice -n 19 bash sc-cases.sh <坏实现>`，bash 5.2.15，一次一个。这些坏实现只存在于 scratch 目录。负载列为该轮首尾的一分钟 loadavg。

| # | 改动（一句话） | 预期抓住它的用例（先写） | 实际 | 负载 |
|---|---|---|---|---|
| M1 | 门的项目根只取 `CLAUDE_PROJECT_DIR`，丢掉 stdin cwd 路径 | 无（V2-E9 / V2-G4 都设环境变量）→ 漏网 | **漏网**：94/94；行为：cwd 路由 rc=0（基线 rc=2） | 1.1→1.3 |
| M2 | `_SG_LEFT` 用 `%d.%d`（微秒不补零） | 无（剩余时间小数都 ≥ .5）→ 漏网 | **漏网**：94/94；直调 2.05 s → 打印 2.48782 | 1.3→2.5 |
| M3 | 删 big_judge 的「量不出长度 → 只匹配规则」哨兵 | 无 → 漏网 | **漏网**：94/94（可达性未核实） | 2.5→3.2 |
| M4 | `nocredit` 检查挪到 credit 计算之后 | 无（所有 longline 用例都无过滤）→ 漏网 | **漏网**：94/94；行为：带 `\| wc -c` 的超长行读取整串与分段都 rc=0 | 3.2→3.6 |
| M5 | 分段触发点保存整串原因串 | 无（回落用例全是整串）→ 漏网 | **漏网**：94/94；stub 回落 sha 67193bea ≠ 基线 fe26cd8f | 3.6→2.4 |
| M6 | `max > LMAX` → `>=` | 无（无 8192 边界）→ 漏网 | **漏网**：94/94；8192 行 finding→longline | 2.4→2.2 |
| M7 | 删组长自检，留 `set -m` | 无（`set -m` 总生效）→ 漏网 | **漏网**：94/94；非组长 shell 里 9→77 | 2.2→1.7 |
| M8 | 删重跑里三处时间检查点 `return 3` | 无（e2e 到不了，无直调）→ 漏网 | **漏网**：94/94；直调 3/0 字节 → 2/883 字节 | 1.7→3.0 |
| M9 | 整串重跑增长超限 `return 0`（放行） | 无（V8-D* 只测 apply 返回码）→ 漏网 | **漏网**：94/94；行为：growth-whole rc=0（基线 2、v3.1 2） | 3.0→1.9 |
| M10 | 分段重跑增长超限 `return 0`（放行） | 无（旧 21ag/21aj 要改完断言才覆盖）→ 漏网 | **漏网**：无设计红；仅 `V5-S13b` 抖动 1 红（见 F7）；行为未能稳定复现（分段首遍在当时负载下吃光 3 s，门关） | 1.9→2.0 |
| M11 | 分段模式不走 `_sg_vx_big_judge` | 无 → 漏网 | **漏网**：仅 `V5-S13b` 抖动 1 红；行为：分段超长行 + 过滤 rc=0 | 2.0→2.6 |
| M12 | 回落写基线文案但返回 0（fail-open） | V6-E2 | **抓住**：5 红（V6-E2、V3-E3/E4/E5、V2-E6） | 2.6→2.6 |
| M13 | 计时器 `kill -- -$$`（hook 的 pid）而非 `-$BASHPID` | V6-E2 一族 | **抓住**：10 红（V3-S4、V5-S5、V4-S6、V5-S10、V5-S14、V6-E2、V3-E3/E4/E5、V2-E6） | 2.6→4.1 |
| M14 | 平台串取 `$MACHTYPE` | 无（V2-G3b 只改 OSTYPE）→ 漏网 | **漏网**：无设计红；那一轮 loadavg 10.8–11.5，另有 3 条**负载红**（V2-E7 墙钟 6.16 s、V9-E10 与 V9-E11 因重跑被截止截断而回落成 oversize），见 F13；M14 在默认环境下与原型行为相同，这 3 条不是它造成的 | 10.8→11.5 |

M12、M13 是我特意放的「应当被抓」的对照，用来证明我的跑法看得见红；M1–M11、M14 的预测全部应验。M1 / M4 / M5 / M7 / M8 / M9 / M2 / M6 另有独立的行为实证（脚本见 scratch：`demo-all.sh`、`demo2.sh`、`demo78.sh`、`demo23.sh`、`stub-*.sh`），不是等价变异体。

**v3.1 原型 × bash 5.0.18 / 5.3.20 的独立复现**：见「机制核对」与 F13（loadavg 9.5–11.5 下各一轮，红的全是时间相关用例）。

## 机制核对（没有缺陷的部分，给执笔与复审用）

- **进程组与计时器**：`exec 2>/dev/null; set -m` 后作业是自己进程组的组长（5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 上 `ps` 看到作业 pid = pgid）；作业里的 `( sleep …; kill … ) &` 与作业**同组**（作业内异步子进程不带 job control），所以 `wait` 后的 `kill -KILL -- -$jp` 同时清掉计时器与它的 `sleep`。放行路径之后无 `N.NNNNNN` 形 `sleep` 残留（`exp1.sh`，四个 bash）；截止路径（shim 让作业停顿 10.4242 s）结束后也没有 shim 的 `sleep` 与计时器的 `sleep` 残留（5.0.18 / 5.2.15 / 5.3.20，loadavg 9.6）。
- **环境改不了的构建信息**：四个 5.x 上 `EPOCHREALTIME` 从环境导入被忽略，`BASH_VERSINFO` 不受影响；`MACHTYPE` / `OSTYPE` / `HOSTTYPE` 可被改写（见 F11）。
- **控制终端**：用 `script` 给 hook 一个控制 tty（stdin / stdout / stderr 仍是文件），放行与截止两条路径在 5.0.18 / 5.2.15 / 5.3.20 上结果与无 tty 相同（rc=0 无输出；rc=2 基线 oversize 文案）。
- **耗时上界**：未发现越过 `max(T_trigger, P0 + min(预算, 3)) + ε` 的路径。放行后无后续工作（评估在 `( … )` 子 shell 里，77 只在 `_sg_relax_run` 内部流转，hook 本身只会 exit 0 / 2）；bash fork 重试（约 15 s）与基线同类，非新增。
- **commentsync**：`--hook-only <原型> target` GREEN，`--hook-only <基线> baseline` GREEN（复现）。
- **sc-cases.sh 复现**：原型 × bash 5.2.15，94/94，loadavg 2.75→2.87（`sc-v31-bash52.txt`）。原型 × bash 5.0.18 与 5.3.20 在 loadavg 9.5–11.5 下各复现一轮：90/94 与 91/94，红的全是时间相关用例（V3-E3、V3-E5、V6-E2、V9-E11，见 F13），其余用例（含全部直调、静态、P1 抽样）全绿，没有逻辑红。

## 对 Decision 14–16 的技术挑战结论

- **14（重跑取消计数上限）**：方向是更严（更多被看见），成本由截止封顶，我没有找到把它变成 fail-open 的路径；代价是含数百个赋值的大命令在重跑里稳定吃满 3 s 后回落（仍是拦，较基线慢）。无异议。
- **15（专用退出码 77）**：成立；`_sg_relax_job` 只在 `_sg_vx_pass` 返回 0 时 `return 77`，77 不会上抛到 hook 的退出码。BI-19 / V4-S11 钉住。无异议。
- **16（只在 GNU/Linux bash 5.0–5.3 放宽）**：成立，见 F16 的措辞建议。

## 计划层核对（审查要点 1–5 的覆盖）

1. **覆盖**：What 1–5、7 → TASK-002；What 6 → TASK-002 单独提交；P1–P10 / SC-V1–V12 → sc-cases.sh（TASK-002 搬入）+ TASK-004；BI-1–22 → W13；Impact / CHANGELOG / 发布同步面 → TASK-006；残余 1–7 → TASK-001 清单 (a)–(g) + TASK-007 对账。INV-1–INV-9 彼此自洽（INV-2 的文件面与 TASK-006 的同步面不冲突；INV-3 与 What 6 不冲突，死代码删除行为不变）。覆盖层面我没有发现遗漏。
2. **顺序与依赖**：TASK-005 只依赖 TASK-003，TASK-004 与 005 可并行，INV-8 管住「之后改一个字节即作废」，成立。owner 门在 TASK-001（对外动作）与 TASK-006（版本与发版）。
3. **rule6_note**：块 A 的 `decision_table_row: n/a` + substitute 口径、块 B 的第 1 行 + `not_required`，与 SOT §4.1 模板、WP-A 先例的分块方式一致；块 B 自己点名了「路由变化让 AI 看到含 `# guard:ack` 指引的普通命中文案」并交 owner 复议，我不另提。
4. **证据复跑**：见上「机制核对」。W9 / W12 / W13 全量按任务书未跑。
5. **措辞**：F13、F14、F15。另 TASK-003 判据「墙钟 ≤ max(T_trigger, 3 s) + 0.3 s」没有挂 INV-7 的负载条件（本机 loadavg ≈ 10 时端到端 ε 达 0.35–1.1 s），建议加上。

**执行建议（对主控）**：F1–F7 与 F13 的用例改动只动 `sc-cases.sh` / `sc-direct.sh` / BI 清单，与 INV-1（原型逐字落地）不冲突；按 Decision 17「验收写成代码、设计阶段实跑」应在 TASK-002 开始前并入并重跑 W13（含对基线的红集），否则这些缺口只会在 TASK-003 里被晚发现。

## Verdict

0 Critical，8 Major（BA2-F1 至 F7、F13），11 Minor（F8 至 F12、F14 至 F19）→ **PASS_WITH_WARNINGS**。

没有 Critical 的依据：照计划（原型逐字落地）实现不会造成安全退化——我找到的所有放行方向的错误都是「执笔偏离原型」时验收抓不住，而不是原型本身有；机制层没有发现新的 fail-open、残留进程或越过截止的路径。

## 轮次记录

- 读：任务书、v31 README、W8 diff 全文、sc-cases.sh、sc-direct.sh、shapes.py、shim、mutants.py、run-mutants.sh、run-evidence.sh（头部与 W13 段）、W13 / W9 输出、detailed-tasks.yaml 全文、proposal.md 的 Why / What / P / 裁定 / SC / Impact / CHANGELOG / Decision（跳过 172–523 的参考实现正文，由 fill31 机械保证）、dispositions.md 的 PP1 表、SOT 豁免规范 §2 / §3 / §4.1、WP-A 的 rule6_note 片段、hook 基线的预置段与主流程、hooks.json（timeout=5）、旧套件 SC-19g/ap/h 与 21ag/21aj 片段。
- 跑：`mkv31.py`；`sc-cases.sh` × 原型 × bash 5.2（94/94）；13 个变异体 × `sc-cases.sh`（`mut.py`、`runmut.sh`）；`exp1.sh`（残留进程）、`exp2.sh`/`exp2b.sh`（作业内进程组视图）、`exp3.sh`（控制终端）、`demo-all.sh`/`demo2.sh`/`demo3.sh`/`demo78.sh`/`demo23.sh`（行为实证）、`flake.sh`（V5-S13b 竞态）、环境改写核对、`commentsync.py` 两个模式。另跑了 `shimlog/`、`shimlog2/` 记录 shim（调用时间线与 ε）、`exp3.sh`（控制终端）、`batch2.sh`（M14 与 5.0.18 / 5.3.20 复现，后台一次一个）。工具调用约 90 次。
- 负载：开始 7–10，中段 1.1–4，后段（行为实证与耗时实证）8–12；所有「负载红」的论断都标了读数。负载红与逻辑红的区分：(a) 逻辑红只有 M12、M13 两个对照坏实现的设计红；(b) F7 的 M10 / M11 两红与被测差异无关（抖动，loadavg 约 2）；(c) loadavg 9.5–11.5 的三轮（M14、原型 × 5.0.18、原型 × 5.3.20）里全部红都是时间相关用例（V2-E7、V3-E3、V3-E5、V6-E2、V9-E10、V9-E11），非时间相关用例零红；这三轮没有在低负载下复跑，所以这些用例在 5.0.18 / 5.3.20 上的绿由作者的 W13（loadavg 1.2）提供，我没有独立确认。
- **未核实**：(1) 逗号小数点 locale 下 `EPOCHREALTIME` / `sleep` 的行为（本机没有这类 locale）；(2) bash 4.x 对新增语法的解析（没有二进制）；(3) 补丁级与 aarch64；(4) F10 哨兵的真实可达性；(5) 真实 Claude Code 进程的 stdio / 进程组（用 `script` 近似）；(6) 旧套件 21ag / 21aj 在 TASK-002 改完断言后能否抓住 M10（推断，未跑）；(7) fork 失败（V5-S10）未单独重跑，只在整轮里 PASS；(8) 大命令的块文案体积对 CC 的影响（基线首遍块也会回显整条命令，非新增）；(9) 另一席是否同时在跑同一套件，F7 的互相可见只有机制推理，无直接证据；(10) 原型 × bash 5.1.16 的完整 sc-cases 没有复跑（只做了 exp1 / exp2 机制探针）；(11) V5-S10 在 root 下的行为（F18，依据 man 文档）；(12) 低负载下 V3-E3 / V3-E5 / V9-E10 / V9-E11 在 5.0.18 / 5.3.20 的绿（见上）。
