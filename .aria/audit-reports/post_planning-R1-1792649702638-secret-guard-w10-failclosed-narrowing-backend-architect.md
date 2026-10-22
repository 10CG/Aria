---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T15:02:54.416Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — backend-architect 席（bash 语义 / 对抗耗时 / 准入门与回落 / TASK-002、TASK-004 可执行性）

审查对象：`detailed-tasks.yaml`（主仓 `a136dbf`）、`proposal.md` v3（`910d9fa`）、v3 原型。原型我用 `python3 v3/mkv3.py <基线 hook> v3.sh` 在 scratch 里重新生成（基线 `aria/hooks/secret-guard.sh` 的 sha256 前缀 `e83c5e30f2cc`，与各 W 文件页眉一致），其 diff 与 `v3/W8-v3.diff` 逐行一致。实验脚本与桩都在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r1/backend-architect/`（下称 scratch），文中引用时只写文件名。

总体判断：原型的核心机制（`set -m` 进程组、组长自检、`wait` 退出码、`kill -KILL -- -PGID`、`/proc/$BASHPID/stat` 解析、`EPOCHREALTIME` 的 locale 小数点、`printf -v`、`sleep` 小数秒、`set -u` / `pipefail` 继承）在 bash 5.2.15 上实测成立，P1、P2、P6 由结构保证，我没有找到任何**输入**能让作业放行未判定的命令、越过截止或留下残留进程。找到的问题集中在三处：一条可由环境变量触发的新 fail-open 路径（BA-1）；TASK-001 / TASK-003 / TASK-004 的验收在顺序、度量、基线来源上有六处会让验收无法证伪或做不出来（BA-2 至 BA-6）；若干文案与加固项（BA-7 至 BA-15）。0 Critical、6 Major、9 Minor。

## 审计结论

### Major

#### BA-1　`_SG_RELAXED` 从环境变量读入且从不初始化：导出该变量即把顶层通道切成进程内放宽，尺寸上限与硬截止同时失效

- type：issue　severity：Major　category：implementation　针对：**原型 / 证据**（`v3/mkv3.py` 步骤 1、`W8-v3.diff`）与 **proposal v3** What 1 准入门第 1 行（「`_SG_RELAXED` 未设」）、What 2 的代码块
- 摘要：准入门第一条假定 `_SG_RELAXED` 只会在作业里被置位，但 hook 顶部没有初始化它。bash 把进程环境里的同名变量原样导入，于是 `_SG_RELAXED=1` 出现在 hook 的环境里时，顶层 `_sg_vx_apply` 用增长上限、三个时间检查点改成返回 3、大副本在**进程内**走 `_sg_vx_big_judge`，没有作业、没有计时器、没有硬截止。
- 证据：
  - 读取点（scratch `v3.sh`）：`:682`（apply 的 `lim`）、`:713 / :724 / :747`（检查点返回 3）、`:731 / :755`（增长文案）、`:740 / :768`（`_sg_vx_big_judge`）、`:800`（`_sg_relax_ok`）；唯一赋值在 `:809`，在作业里。
  - 实测（`env -u CLAUDE_PROJECT_DIR _SG_RELAXED=1 bash v3.sh`，输入为 `v3/gen-v3.py apply-heavy-cjk`）：`rc=0`，墙钟 **25.23 s**。同一输入基线 `rc=2`，2.0–2.1 s（W11、我的复跑 2.10 s）。生产里 `aria/hooks/hooks.json` 给的 `timeout` 是 5，Claude Code 在 5 s 杀掉 hook 后放行，所以这是一条新的 fail-open。`f5like` 同样环境下 `rc=2`、4.36 s，文案是「internal error in per-segment evaluation (rc=3)」。
  - 本仓对环境变量的态度有先例：`aria/hooks/secret-guard.sh:614` 把 `SECRET_GUARD_TIME_BUDGET_S` 封顶到 4，注释写明「a huge budget must NOT be able to disable the time fail-closed」。`_SG_RELAXED` 是同一类开关，却没有封顶或初始化。
  - 现有 W10 G5 与计划里 SC-V2 的「`_SG_RELAXED` 已设」都是在 shell 内部直接赋值后调用 `_sg_relax_ok`，测不到「环境里带进来」这条路。
  - 其余内部全局变量不受影响：`_SG_P0` 在顶部无条件赋值，`_SGV_GMAX` / `_SGV_LMAX` 是常量赋值，`_SG_OV_PAT` / `_SG_OV_MODE` / `_SG_LEFT` 都在使用前赋值。
- 建议：
  1. `mkv3.py` 步骤 1 在 `_SG_P0=…` 之后加一行 `_SG_RELAXED=""`（或 `unset _SG_RELAXED`），注释写明「内部标志，不读环境」；重新生成 `W8-v3.diff`，proposal What 2 的代码块由 `fill.py` 机械更新。P1 不受影响（赋值无输出）。
  2. SC-V2 增加一个 e2e：`env _SG_RELAXED=1 hook < <超 8192 的命令>`，结局必须与基线逐字节相同或为正常回落（`rc=2` 且在 `max(首遍 + 基线前段, 3 s) + 0.3 s` 内）；TASK-003 增加 BI-14「不初始化 `_SG_RELAXED`」。
  3. 我在 scratch 用 `v3fix.sh` 验证了：加初始化后，同一输入 `rc=2`、3.04 s（正常的截止回落）；`v3unit.sh` 的 S1–S8、G1–G8 全部仍 PASS。

#### BA-2　TASK-004 没有规定「基线 hook」从哪里来：实现落地后，各脚本的 base 与 impl 会是同一个文件，所有 base-vs-impl 比较恒绿

- type：issue　severity：Major　category：testing　针对：**任务计划**（`detailed-tasks.yaml:85-87`，TASK-004 design 第一条）
- 摘要：TASK-004 要把 `run-w9 / run-w10-w11 / w10b / run-w12` 改成「接受实现 hook 路径（而不是由 mkv3.py 生成），其余不变」。这些脚本的第一个参数本来就是「基线 hook」：`run-w10-w11.sh:4-5` 先 `cp "$SRC" "$W/base.sh"` 再 `mkv3.py "$SRC" "$W/v3.sh"`，`run-w9.sh:8` 把传入的 hooks 目录同时拷成 base 与 v3 两棵树，`ident.sh`、`ident32.sh`、`w10b.sh` 都比较 `base.sh` 与 `v3.sh`。TASK-002 落地后，工作树里的 `aria/hooks/secret-guard.sh` 已经是实现，再按原用法传它，`base.sh` 与 impl 相同，P1（W9、W12 第 2 节）、P2（W12 第 3 节）、P6（w10b）的比较全部是自己对自己。
- 证据：今天 `sha256sum aria/hooks/secret-guard.sh` 的前缀是 `e83c5e30f2cc`（即基线）；`mkv3.py:11` 的 `rep()` 在替换不是恰好命中一次时直接退出，等于现在偶然充当了「传入的不是基线」的保险，改成不用 `mkv3.py` 之后这道保险消失。
- 建议：TASK-004 design 写死：基线 hook 只能来自 `git -C aria show 59e333c:hooks/secret-guard.sh`，基线套件来自 `git -C aria show 59e333c:hooks/tests/secret-guard.test.sh`；每个脚本开头断言 `sha256(base) 前缀 == e83c5e30f2cc` 且 `sha256(impl) != sha256(base)`，不满足就中止；W14 页眉同时记两个 sha256。

#### BA-3　TASK-004 的验收只覆盖 W12 与 P6，阈值与数据对不上，其中一条在构造上恒绿

- type：issue　severity：Major　category：testing　针对：**任务计划**（`detailed-tasks.yaml:88`）
- 摘要：
  - (a) 「放行数不低于原型 (136/137)」：原型证据是 W12 第 1 节 `outcome allow 137 / oversize 1`（138 条里 137 条 SMAX 类全部放行、1 条 VMAX 照旧拦），`W12b-rerun.txt` 第二次回放也是 137；「136/137」与任何一个已有数字都对不上。若本意是给 n=172（离截止最近，两次 1.554 s / 1.596 s）留一条的容差，没有写出来；若是笔误，阈值比原型低一条，会放过一个回归。
  - (b) 「无任何越过 max(首遍 + 基线前段, 3 s) + 0.3 s 的放行」：`W12-replay-138.tsv` 里放行的最大墙钟是 1.805 s（n=354），而放宽重跑的放行不可能晚于 `_SG_P0 + 3 s`（作业到点就被杀），所以对「放行」这条在构造上恒绿。真正需要约束的是**所有结局**（放行、拦截、回落）。另外「首遍 + 基线前段」在 W12 的 TSV 里没有记录：`replay138.sh` 要吃的是 `mkdbg.py` 插桩版，而 `run-w12.sh` 传的是未插桩的 `$W/v3.sh`，TSV 第 5–7 列全是 `-`。
  - (c) 设计写的是「重跑 W9–W12」，验收却没有 W9、W10、W11、W10b、commentsync 的判据：W9 应为「旧套件在实现上恰好 6 组变化（21ab、21ac、21ag、21aj、21al、21ao，非 git 副本里另有 SC-13）且逐条断言差异与 W9-suite.txt 一致、新套件全绿」；W10 应为 S1–S8、G1–G8 全 PASS 且残留 0；W11 应为每个形状的结局与墙钟不劣于原型；w10b 应为 IDENTICAL×4 与 P10 的 rc 0/2/2；commentsync target 为 GREEN。
  - (d) `TRAFFIC_DIR`（冻结语料）只在 `v3/README.md:21` 与 proposal「证据与复现」里提到，没有任何任务负责用 `traffic/extract.py` 与 `traffic/refreeze.py` 复原或校验它；新会话抽取编号会漂移，只认 W0 的 sha256。
- 建议：验收逐条列判据；(a) 写成「SMAX 类 137 条，在一分钟负载 < 2 时放行 ≥ 137，或 ≥ 136 且不放行的那条是带基线字节的回落」二选一，并说明理由；(b) 改为「所有 138 条的墙钟 ≤ max(该条首遍 + 基线前段, 3 s) + 0.3 s」，前段由 TASK-004 临时生成的插桩副本记录（见 BA-4 的度量建议）；(d) 加前置步骤「复原 `TRAFFIC_DIR` 并核对 W0 的 138 个 sha256，缺失则报告而不是跳过」。

#### BA-4　SC-V3 第二条 e2e 与 TASK-003 耗时矩阵的判据依赖自然产生的首遍耗时，在共享宿主上要么偶发红、要么无法度量；有现成的确定性做法

- type：issue　severity：Major　category：testing　针对：**proposal v3** SC 表 SC-V3 行（`proposal.md:407`）与**任务计划**（`detailed-tasks.yaml:75`）
- 摘要：SC-V3 要求「首遍约 2 s 的形状墙钟 ≤ 3.3 s」，TASK-003 的判据是「墙钟 ≤ max(首遍 + 基线前段, 3 s) + 0.3 s」。首遍耗时是自然计算量，随负载漂移 ±30–40%；「首遍 + 基线前段」没有定义怎么取。
- 证据：
  - 同一形状在已提交的 `W11-adversarial.txt` 与我的复跑里差很多：`21ab#2` 基线 3.52 s 对 2.48 s，`21ab#3` 2.51 s 对 2.73 s；在我的复跑里 v3 放行的 `21ab#2` 是 2.34 s，比同轮基线的拦截（2.48 s）还短。负载 1.2–2.4 的区间内就有这样的波动，负载上去后首遍超过 3.3 s，断言会误红。
  - `mkdbg.py` 的插桩点用的是原型的**逐字文本含行尾注释**（例如 `'_SG_P0=${EPOCHREALTIME:-}   # #217: hook-start anchor of the relaxed rerun\'s hard deadline (…)\n'`），并 `assert t.count(old) == 1`；TASK-002 一旦改了这些注释（What 7 本来就要改注释），插桩版生成会直接断言失败，TASK-003/004 的「前段」就量不出来。
  - 确定性做法已验证：PATH 里放一个 `jq` 桩，第一次调用先睡 N 秒再 exec 真 jq（scratch `shim/jq`，`JQ_SHIM_STATE` 记首次、`JQ_SHIM_DELAY` 控时长；`CLAUDE_PROJECT_DIR` 取消设置，`_sg_ext_root` 不会第二次调 jq）。`apply-heavy`（放宽重跑约需 1.4 s）：延迟 0 → `rc=0` 1.49 s；延迟 1.5 s → `rc=2` oversize、**3.02 s**；延迟 2.5 s → 3.11 s（基线 3.01 s）；延迟 3.5 s → 3.90 s（基线 3.88 s）。结局与墙钟都确定。BI-13（锚点设在 `_sg_per_segment_eval` 入口）在延迟 2.5 s 时会给作业完整的 3 s，推演结局是放行、约 4.3 s（未实跑），与正确实现的「基线回落」结局不同，不靠墙钟阈值就能分出来。
  - 对「放宽重跑后放行」的 e2e（SC-V7 的良性大命令、SC-V3 的放行形状）：截止被 `min(预算, 3)` 封顶，`SECRET_GUARD_TIME_BUDGET_S` 只能缩短不能放宽，所以负载高时这类断言必然会红；要选作业本身 ≤ 0.3 s 的形状（留 10 倍余量），并把余量记进用例注释。
- 稳定的部分（不用改）：直调桩的截止回落——scratch `t_overshoot.sh`，截止 1 s、12 次，在两个 nice 19 的忙循环抢核时超出截止 4–11 ms；`f5like` e2e 8 次全是 3.01 s。SC-V3、SC-V5 里的「1.3 s」与「3.3 s」界限本身稳。
- 建议：SC-V3 第二条改用 jq 桩制造确定的锚点前延迟，断言**结局**（回落或放行）而不是墙钟；TASK-003 矩阵的度量写成「每个输入同时跑插桩副本，取同一次运行里的首遍与前段时刻」，并要求 `mkdbg.py` 改成按函数名与结构锚点而不是逐字注释；插桩副本由 TASK-004 对**实现**重新生成，不进仓。

#### BA-5　计划原文「直调类用例自设 `_SG_P0=$EPOCHREALTIME`」会让套件在 bash 3.2 下直接中止，而验收要求 3.2 下套件全绿；新 e2e 用例没有按能力分支的设计

- type：issue　severity：Major　category：testing　针对：**任务计划**（`detailed-tasks.yaml:60, :63`）与 **proposal v3** SC-V2（`proposal.md:406`）
- 摘要：套件顶部是 `set -u`（`secret-guard.test.sh:16`）。bash 3.2.57 没有 `EPOCHREALTIME`，`x=$EPOCHREALTIME` 在 `set -u` 下报 `EPOCHREALTIME: unbound variable`（我实测：`bash-3.2.57 -c 'set -u; x=$EPOCHREALTIME'` 报错，`${EPOCHREALTIME:-}` 正常）。照字面写，3.2 下套件中止；CHANGELOG 先例（v1.76.1「bash 3.2.57 + 5.2」）说明 3.2 下跑套件是发版动作之一。
- 另有三处缺口：
  1. 套件的 e2e 用例是直接执行 hook（`run_case`、`wpa_err` 都是 `"$HOOK"` / `"$WPA_HOOK"`，靠 shebang `#!/usr/bin/env bash`），实际用的是 PATH 里的 bash。期望 `longline`、增长文案或放行的 e2e 用例，在 PATH 上是 3.2 的环境里不可能成立；探测能力必须问**将执行 hook 的那个 bash**（例如 `bash -c 'echo ${EPOCHREALTIME:-none}'`），不是套件自己的 shell。
  2. SC-V2「bash 3.2 下 e2e 与基线逐字节相同」需要仓外的 3.2 二进制（README：自建，不在仓里，没有构建配方）。套件里只能是「没有该二进制就 SKIP」；SKIP 当 PASS 记数就是恒绿。
  3. SC-V6「回落字节与基线相同」要拿基线文案比较，若用 `git show`，在非 git 或浅克隆里会像现有 17 个用例那样静默不跑。
- 建议：TASK-002 design 写明：直调用例用 `_SG_P0=${EPOCHREALTIME:-}`；依赖 `EPOCHREALTIME` 的用例按「hook 将使用的 bash 是否有 EPOCHREALTIME」二分，3.2 下改断言为基线文案（这才是 3.2 下应有的结局），并计入头注释的「无 zsh」之类的分档数；SC-V2 的 3.2 e2e 要么放进 TASK-004 的 W12 第 3 节（已有）、套件里只留能力探测，要么显式输出 `SKIP` 并不计入 PASS；SC-V6 的基线文案用内嵌的字面期望（基线 oversize 模板是静态的）而不是 `git show`。

#### BA-6　TASK-001 的验收要求「基线红 / 绿逐条记录」，但被记录的 SC-V 用例是 TASK-002 才写的

- type：issue　severity：Major　category：testing　针对：**任务计划**（`detailed-tasks.yaml:44, :46` 与 `:57-60`、`depends_on`）
- 摘要：TASK-001 design 写「SC-V2 … SC-V10 在基线上实跑为红」，验收是「基线红 / 绿逐条记录」；而 SC-V 用例由 TASK-002 落成（design 第 60 行），TASK-002 又依赖 TASK-001。TASK-001 时点没有可以在基线上跑的 SC-V 用例，该验收做不出来；能做的只是用原型的探针（`probe21.sh`、`gen-v3.py`）演示行为，不是套件红绿。SC-V11、SC-V12 也不在 TASK-001 列出的红 / 绿两个清单里。
- 建议：把「基线红绿记录」挪到 TASK-002 的最后一步（对 `git show 59e333c:hooks/secret-guard.sh` 跑**新套件**，记录红集 R 与绿集 G，R 必须包含 SC-V2 至 SC-V10 中除回归闸外的项），TASK-003 再把基线作为 BI-0 复核一遍；TASK-001 只保留认领、分支、重锚、两张残余 issue、两条留言。

### Minor

#### BA-7　P5「作业结束后没有残留进程」靠「没有残留」成立，不是结构保证：作业提前退出而留下占着管道的后代时，`_sg_relax_run` 会被拖到后代结束

- type：risk　severity：Minor　category：implementation　针对：**原型**（`v3.sh:812` 起的 `_sg_relax_run`）与 **proposal v3** What 3「要点」与 P5（`proposal.md:364`）
- 证据：计时器只在到点时杀组；作业正常退出后 `wait` 返回，计时器被杀，剩下的后代没人管。scratch `t_stray.sh`：桩 `_sg_vx_pass() { sleep 4.444 & return 0; }`，截止 1 s，`_sg_relax_run` 返回 `rc=0`，墙钟 **4.45 s**；返回 2 并带文本的桩同样拖到 4.56 s。W10 S5 的桩是 `sleep 6.222 & wait`，作业自己不退出，所以没测到这一支。当前判定链路是纯 bash（`_sg_compute_credit` 用 `_sg_line_match`，无外部进程；唯一外部进程是 `_sg_redact_echo` 的 `sed`，在管道里同步结束），**输入够不到**这一支，故定 Minor；但 P5 的措辞是无条件的。
- 建议：`wait` 之后、杀计时器之前加 `kill -KILL -- "-$jp" >/dev/null 2>&1`（组内没有成员时静默失败，窗口与计时器同量级，proposal 已接受）。scratch `v3fix.sh` 验证：同一桩 0.00–0.01 s 返回；S1–S8、G1–G8 仍 PASS。补一个 S9（作业提前退出 + 后代占管道 → ≤ 0.3 s 返回）和对应 BI-15（`wait` 后不清组）。

#### BA-8　「计时器 fork 失败 → `tp == jp` → 杀作业并以 99 退出」在 bash 5.2.15 上不会发生；SC-V5 / BI-3 的「删掉计时器那一行」变异测的是一个真实失败里不会出现的状态

- type：issue　severity：Minor　category：documentation　针对：**proposal v3** What 3「要点」（`proposal.md:272`）、SC-V5 / BI-3；**原型**
- 证据：bash 在非交互 shell 里 fork 失败会 `throw_to_top_level`，子 shell 以 126 退出，`[[ "$tp" != "$jp" ]]` 根本执行不到，作业留在原地、不受计时。scratch `t_timerfail.sh`（在作业与计时器两次 fork 之间用 `ulimit -S -u 0` 模拟计时器 fork 失败，作业桩睡 21 s，截止 1 s）：`_sg_relax_run` **21.3 s** 后才返回 4。`EAGAIN` 时 bash 还会先重试 1+2+4+8 = 15 s，所以这条路径下 hook 本来就活不到 5 s；非 `EAGAIN`（如 `ENOMEM`）才会立即失败。基线在自己的 fork 失败时同样退出 126（Claude Code 视为非阻断），所以这不是新增的一类 fail-open，也就只是 Minor。
  - 同时我验证并**撤回**了一条假设：「作业 fork 失败时 `jp=$!` 取到继承来的旧 PID，`wait` 对已回收的旧 PID 返回 0，被当成放行」。前半成立（进程替换会设 `$!`，hook 启动时的 `done < <(jq …)` 就设了；`wait` 对该 PID 在子 shell 里确实返回 0，scratch `t_bang.sh`），但作业 fork 失败时 bash 先 `throw_to_top_level`，子 shell 以 126 退出，最终 `rc=4` 回落（scratch `t_forkfail.sh`，15.0 s，回落）。
- 建议：把「计时器 fork 失败 → 回落」的说法改成「fork 失败时 bash 自行中止该命令替换，最坏情形与基线的 fork 失败相同（hook 以 126 退出）」；SC-V5 的变异测试保留，但标明它测的是 `tp == jp` 这个防御分支而非真实失败；可选加固：作业启动后立刻 `trap 'kill -KILL -- "-$jp" >/dev/null 2>&1' EXIT`，实测在计时器 fork 失败的路径上 EXIT trap 会执行，组被杀、无残留（`t_timerfail.sh` 的 `v3timerfail-trap.sh` 变体：15.0 s 返回，无残留 sleep）。

#### BA-9　准入门与锚点的几处加固：用 `BASH_VERSINFO` 判 bash 5、`_SG_LEFT` 夹上限、5.0 / 5.1 / 5.3 未验证

- type：risk　severity：Minor　category：implementation　针对：**原型**（`_sg_relax_left`、`_sg_relax_ok`）与 **proposal v3** What 1、CHANGELOG 草稿
- 证据与建议：
  1. 「有 `EPOCHREALTIME`」不严格等价于「bash ≥ 5」：环境里带 `EPOCHREALTIME=123.456` 时，bash 3.2.57 把它当普通变量，`_SG_P0` 与 `$EPOCHREALTIME` 都是 `123.456`，准入门打开（scratch `t_b32gate.sh`：`_sg_relax_run` 进入作业）。随后作业因 3.2 没有 `$BASHPID`（`set -u`）而 0.01 s 内失败，回落字节与基线相同（e2e 的 `f5like`、`apply-heavy` 两形状 stderr 都相同），所以是安全的，但安全来自一个巧合。建议 `_sg_relax_left` 增加 `(( ${BASH_VERSINFO[0]:-0} >= 5 ))`，让 P2 的「bash 3.2 / 4.x 不放宽」成为结构。bash 5.2 对环境导入的 `EPOCHREALTIME` 是忽略的（实测）。
  2. `EPOCHREALTIME` 是墙钟：时钟被回拨时，`left = P0 + cap − now` 可以大于 `cap`，`sleep` 会睡过 3 s。建议 `printf -v` 之前把 `now` 夹到 `cap * 1000000`。这一条是逻辑推演，未实测。
  3. 只在 5.2.15 上实测过；5.0 / 5.1 / 5.3 的 `wait`、`set -m`、`EPOCHREALTIME` 行为未验证，自检只覆盖「`set -m` 不生效」这一种退化。CHANGELOG 草稿写「bash 5.0+」，建议写成「实测 bash 5.2.15；其他 5.x 未实测，自检不过则回落」。
  4. locale：已在 `de_DE.UTF-8`（`LOCPATH` 指向 scratch 里 `localedef` 编出的副本）实测，`EPOCHREALTIME` 为 `1792668303,182211`，`${EPOCHREALTIME/[.,]/}` 与 `sleep 0.2` 都正常，e2e `apply-heavy` 放行（1.45 s）、`f5like` 回落（3.03 s，stderr sha 与基线相同）；`fa_IR.UTF-8` 的小数点是 `.`。若遇到小数点不是 `.` 或 `,` 的 locale，`_sg_relax_left` 的数字校验返回 1，回落，安全。

#### BA-10　现有 `wpa_x_finding` 同样接受 `longline` 文案，SC-V7 的「多行大副本 → 普通命中文案」需要更严的断言

- type：issue　severity：Minor　category：testing　针对：**proposal v3** SC-V7（`proposal.md:411`）与**任务计划**（TASK-002）
- 证据：`secret-guard.test.sh:2522-2527` 的 `wpa_x_finding` 只断言 `reads a secret-bearing source` 在文本里、`too large to scan` 不在。`longline` 模板第一句是「command reads a secret-bearing source, and after variable expansion …」，同样含该短语，所以凡是用 `wpa_x_finding` 判大副本的用例，都分不清「普通命中」与「误路由到 `longline`」（BI-10、BI-12 的一半后果）。方向上误路由是更严的拦截，不是安全问题，但套件对它失明。
- 建议：新增 helper（或给 `wpa_x_finding` 加第二个参数），普通命中要求出现 `value-REDACTING filter`、不出现 `has a line longer than`；`longline` 要求出现 `has a line longer than` 与 `Matched pattern:`。同时 SC-V11 的 `{8193` 静态断言很容易被换个写法绕过（例如 `.{8200,}` 或运行时拼数字），应明说它只是辅助，行为判据是 SC-V7 的多行副本（实测 `[[ $v =~ .{8193,} ]]` 在 9 KB 与 60 KB 单行上都只要 25 ms，所以 BI-12 的坏处是跨换行误判，不是慢）。

#### BA-11　R2-A22 的处置声称由 TASK-002 承接，TASK-002 的文字里没有

- type：issue　severity：Minor　category：documentation　针对：**任务计划**（`detailed-tasks.yaml:57-62`）
- 证据：`dispositions.md` 的 R2 表 A22 写「涉及 locale 的用例用 `C.UTF-8`，并先断言字符集（TASK-002）」；`detailed-tasks.yaml` 与 `proposal.md` 全文没有 locale 要求。多字节填充会改变行为：`apply-heavy-cjk` 基线 2.0–2.1 s、ASCII 的 `apply-heavy` 基线 0.37–0.44 s；CJK 形状只在多字节 locale 下才会走到 3 s 回落，所以 SC-V6 与耗时矩阵若用它，结局取决于跑套件那台机器的 `LANG`。套件已有先例 `wpa_lang_only`（`secret-guard.test.sh:2092`，`LANG=C.UTF-8`）。
- 建议：TASK-002 design 补一条：凡依赖字符数与字节数差异或 CJK 填充的用例，显式设 `C.UTF-8` 并先断言 `locale charmap` 为 UTF-8，否则 SKIP 并记数。

#### BA-12　SC-V12 的「standards 三处计数一致」没有机械检查，基线上这三处已经漂移；standards 与 CHANGELOG 没有任务的 deliverable 或验收行

- type：issue　severity：Minor　category：documentation　针对：**任务计划**（TASK-002 / TASK-006）与 **proposal v3** SC-V12、Impact
- 证据：套件头注释是 `Coverage: 831 cases (825 without zsh)`（`secret-guard.test.sh:11`），standards `conventions/secret-hygiene.md:23, :316, :352` 写的是 `822` / `816 无 zsh`，今天就差 9；套件里的 SC-13 只核对头注释。standards 是子模块，改它要走自己的提交与 gitlink 更新（CLAUDE.md 多远程推送约束 1），INV-2 允许，但没有任何任务把它列为 deliverable；CHANGELOG 终稿（`<N>`、`<n>` 填值、「订正 v1.76.1『永不 fail-open』」）同样没有验收行，TASK-006 只有「按 Impact 列全」。W9 的两次运行都在非 git 副本里（实跑 814），头注释计数的核对只能在 git 检出里做。
- 建议：TASK-006 验收增加：`grep` 三处数字都等于 TASK-004 记录的实跑数 N 的命令与期望输出；CHANGELOG 终稿的三个填空与订正句各一行；TASK-002 验收注明「头注释计数在 git 检出里核对」。

#### BA-13　TASK-005 只依赖 TASK-002，TASK-003 / 004 之后的修改没有复审规则；INV-6 的关键词核对只写在 TASK-007

- type：issue　severity：Minor　category：documentation　针对：**任务计划**（`detailed-tasks.yaml:93-98`、`:119-120`、INV-6）
- 证据与建议：
  1. TASK-005 `depends_on: [TASK-002]`，与 TASK-003、TASK-004 可并行；TASK-003 / 004 发现问题后的代码改动没有重新审查的步骤，TASK-006 只要求「无未处置的 Critical / Major」。建议 TASK-005 依赖 TASK-003 与 TASK-004 的最终代码，或加一条「审查 SHA 之后的 diff 必须复审」。
  2. 「关闭关键词只出现在 TASK-007 的主仓提交」只落成了 TASK-007 design 的一句「推送前做 INV-6 关键词核对」，acceptance 没有对应行，也没有核对命令。真正会提前误关的是 TASK-002 与 TASK-006 的 aria 提交、合并提交和 PR 描述（#217 在 aria-plugin 仓）。建议每次推送前对待推提交与 PR 正文跑一条固定的 `grep -iE '(clos|fix|resolv)[a-z]*[: ]+[^ ]*#217'`（及 `#154`、`#203`、`Aria#221`），期望 0 命中，写进 TASK-002 / 006 / 007 各自的验收。

#### BA-14　文案：`rule6_note` 与 Impact 对 `longline` 复用「两条指令行」的说法不精确；CHANGELOG 草稿漏了两个用户可见变化

- type：issue　severity：Minor　category：documentation　针对：**任务计划**（`detailed-tasks.yaml:14` `rule6_note.note`）与 **proposal v3** Impact、CHANGELOG 草稿
- 证据与建议：
  1. `rule6_note` 的格式合规：`decision_table_row: "n/a"`（SOT §4.1：n/a 即不属 Skill 变更）、`description_changed: "no"`、其余 `n/a`，hook 不是 Skill，逐 hunk 判为描述性 + 逐字断言替代的论证成立。但文字说 `longline` 「reuses the two instruction lines of the existing oversize template verbatim」，现有 oversize 模板的指令是「Split it…」一行加**三**条要点；`longline` 复用的是首行与其中两条，去掉了「do not repeat one long \$VAR many times」。建议改成「复用首行与其中两条要点，省去第三条」，免得 TASK-005 逐字核对时产生争议。
  2. CHANGELOG 草稿「行为变更」没有写出回落的代价：被拦的放宽类命令墙钟由基线的不到 1 s 变为约 3 s（`f5like` 0.75 s → 3.01 s，`apply-heavy-cjk` 2.0 s → 3.04 s）；对小 `SECRET_GUARD_TIME_BUDGET_S` 的用户，截止同样缩短（预算 1 → 约 1.0 s，2 → 约 2.0 s，我实测过）。
  3. 本机依赖（Linux、`/proc`、GNU 风格的小数秒 `sleep`、`kill` 内建）只在 `v3/README.md`。我用一个拒绝小数秒的 `sleep` 桩实测，`apply-heavy`、`f5like` 的 stderr 与基线逐字节相同、墙钟同基线，即安全地整体失效而不报错；建议 CHANGELOG 注明「缺这些依赖时放宽不生效，行为同旧版」。

#### BA-15　可选加固：让「放行」需要一个专用的非零退出码，而不是裸 `0`

- type：risk　severity：Minor　category：architecture　针对：**proposal v3** What 3 / Decision 5 与**原型**
- 摘要：当前结论只取退出码，`0` = 放行。`0` 也是 bash 在若干异常下的默认值：我实测过 `wait` 对已回收的旧 PID 在命令替换里返回 `0`（`t_bang.sh`）。本次分析里这条路径被 bash 的 `throw_to_top_level` 堵住了（见 BA-8），但这是对 5.2.15 行为的依赖，5.0 / 5.1 / 5.3 没有验证。
- 建议（不改变既定机制，只是编码）：作业在 `_sg_vx_pass` 返回 0 时以固定的专用码（例如 77）退出，命令替换把 77 映射为放行，裸 `0` 与其余非 2 的码一律回落。成本一行，P4 变成「放行需要正向确认」，也符合 memory 里「不变量要有 fail-closed 默认」的做法。是否采用由执笔与 owner 取舍，不影响本轮结论。

## 已核实无问题（供去重参考）

- **P1 由结构保证**：逐 hunk 看了 `W8-v3.diff` 的每一处：`_SG_P0` 赋值、两个新常量、`_sg_vx_apply` 的 `lim`（非放宽时仍是 `_SGV_SMAX`）、`_sg_vx_pass` 的三处 `[[ -n "${_SG_RELAXED:-}" ]] && return 3`（非放宽时为假、落回基线分支）、两个触发点（`_sg_relax_ok` 为假则写基线文案）、`_sg_judge_one` 的 `nocredit="${3:-}"`、`longline` 分支（只有 `kind=longline` 进入）、`_sg_per_segment_eval` 的 `rc -eq 4` 分支（基线从不返回 4）。非放宽路径没有可观察差异。前提是 BA-1 的初始化。
- **回落字节相同，所有失败出口**：除 W10b 的截止回落外，我另造了三个出口并比较 stderr sha：自检失败（去掉 `set -m`）、作业内部错误（`: "$undefined"`）、作业返回 2 但无文本，`f5like` 与 `apply-heavy` 两个形状都与基线 IDENTICAL；预算 `0 / 1 / 2 / 4 / abc / 空` 六种取值下 stderr 相同（墙钟 0.75 / 1.01 / 2.01 / 3.01 / 3.01 / 3.01 s）。拒绝小数秒的 `sleep` 桩下同样 IDENTICAL。
- **机制**：`set -m` 在命令替换里使作业与计时器各自成组，非 tty 与 pty 控制终端两种环境（`script -qec`）结果相同；`wait` 的退出码在 3000 次快作业循环里无异常（0 / 2 各 1500 次全部正确）；`/proc/$BASHPID/stat` 的解析在 comm 为 `x) y 1 2 3.sh` 的直接 shebang 执行下仍取对 pgrp；子 shell 的运行时错误（未定义变量、坏数组下标、`${x:?}`、坏算术）退出码都是 1，不会撞上「2 且有文本」；父进程的 EXIT trap 不会在命令替换、作业或计时器子 shell 里触发（套件的 `rm -rf "$_TEST_HOME"` 不受影响）。
- **时间上界**：`f5like` 8 次均 3.01 s；作业截止超出量 4–11 ms（含 CPU 争抢）；`_sg_ext_entries` 在最大合法扩展文件（200 条、30.6 KB）上 33 ms。用 jq 桩把首遍前延迟拉到 1.5 / 2.5 / 3.5 s，v3 的总墙钟都不超过 `max(延迟 + 前段, 3 s) + 0.15 s`。P3 的上界表述漏了 `_sg_relax_ok` 的几十毫秒与 fork 开销，在 0.3 s 余量内，不单列。输入侧没有找到能让作业放行未判定命令、越过截止或留下残留进程的构造；hook 本身有 64 KB 命令上限（`aria/hooks/secret-guard.sh:1157`），副本最大约 73 KB，所有放宽重跑的工作量有界。
- **复现便宜的三项**：`run-w10-w11.sh`（scratch 副本里跑，约 34 s，负载 1.9）：W10 S1–S8、G1–G8 全 PASS，残留 0；W11 结局与已提交文件一致，墙钟差在 ±0.3 s 内（`21ab#2` 基线 2.48 s 对已提交的 3.52 s）。`w10b.sh`：P6 四行 IDENTICAL，P10 rc 0 / 2 / 2。`commentsync.py` 基线模式 GREEN；目标模式在未改注释的原型上 RED（22 项）。
- **bash 3.2.57**：四个形状（`f5like`、`apply-heavy`、`shrink`、`segfinding`）stderr 与基线相同。
- **文案与计划覆盖**：`longline` 模板、两条增长原因串与代码块一致；What 6 的「死代码」论断成立（值只会由非空串换成非空串）；What 7 的 `commentsync` 对「应出现」词只数整行注释，原型本身的新增注释只满足 `_SGV_GMAX`、`_SG_P0` 两个，其余需要 TASK-002 在退役位置写新注释（计划已写「位置由 TASK-005 把关」）。

## Verdict

**PASS_WITH_WARNINGS**。0 Critical，6 Major（BA-1 至 BA-6），9 Minor（BA-7 至 BA-15）。

没有 Critical 的理由：BA-1 需要控制 hook 的进程环境，该位置本身已能绕过守卫（例如设 `BASH_ENV`），属于对既有环境变量态度（时间预算封顶）的一致性问题，且一行即可修；BA-6、BA-5 是计划顺序与措辞问题，改计划即可，不影响实现可行性。BA-1 至 BA-6 建议在 TASK-001 / TASK-002 开工前就改进计划与 `mkv3.py`，否则会在 TASK-003 / 004 才暴露。

## 轮次记录

- 做了什么：读任务书、`detailed-tasks.yaml`、`proposal.md` 全文、`v3/README.md`、`mkv3.py`、`gen-v3.py`、`mkdbg.py`、`commentsync.py`、各运行脚本与 W9 至 W12b 证据文件、`dispositions.md`、基线 hook 的相关段（W10 区、时间预算、`_sg_ext_*`、`_sg_emit_blocked`、`_sg_judge_one`、`_sg_per_segment_eval`、主流程）、套件头部与 W10 段 helper、`hooks.json`、`skill-benchmark-exemption.md`；在 scratch 里用 `mkv3.py` 重新生成原型并与 `W8-v3.diff` 核对；跑了便宜的三项复现和上面列的机制、对抗、locale、pty、bash 3.2、桩 `jq` / `sleep` 实验。所有改动只在 scratch，没有改仓内任何文件；进程只按自己记下的 PID 清理（两个 nice 19 的忙循环由 `$!` 记下并 `kill`），没有 `pkill`；实验都加了 `taskset -c 0,1 nice -n 19`，单个不超过 1 分钟，未并发开重实验（唯一的一次 15–21 s 的 fork 失败模拟是单独跑的）。
- 没读：另外两席与 tech-lead 席的报告；会话临时目录里的语料副本（禁止）。
- 没跑：`run-w9.sh` 全套件（约 12 分钟）、`run-w12.sh` / `run-w12b.sh`（需要语料）。W12 第 1 至 3 节的数字、W9 的 813 / 807 都是引用已提交证据，**未核实**。
- 未核实：bash 5.0 / 5.1 / 5.3；macOS、Windows、busybox / musl（只用桩模拟了不支持小数秒的 `sleep`）；真实 Claude Code 在 5 s 超时时的行为（依据 `hooks.json` 的 `timeout: 5` 与仓内既有假设）；`ENOMEM` 型 fork 失败（只用 `ulimit -S -u 0` 模拟了 `EAGAIN` 型）；时钟回拨（BA-9 第 2 条为推演）；BI-13 在延迟桩下的放行结局（BA-4 为推演）。
- 工具调用：约 100 次（含少量并行调用）。
