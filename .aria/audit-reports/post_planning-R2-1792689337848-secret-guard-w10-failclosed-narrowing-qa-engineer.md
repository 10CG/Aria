---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T18:20:04.863Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — qa-engineer 席：可执行验收与非作者变异测试

范围：`v31/sc-cases.sh`、`v31/sc-direct.sh`、`v31/shim/`、`v31/shapes.py`、`v31/commentsync.py`，以及它们在 `detailed-tasks.yaml`（INV-7、TASK-002/003/004）里被依赖的方式。被测原型由 `python3 v31/mkv31.py` 重新生成（sha256 前缀 `9f61db0e7b8b`，与 W13 页眉一致，可复现）。

先说结论：验收用例对「作者想到的 23 种错误」设计得很扎实（作业协议、截止、进程组、退出码 77 这一块，我的 7 个对照变异体都被指定用例抓住，且红的原因正确）；弱点集中在三处：1. 计时类用例在共享宿主的负载下会对好实现假红，而 README、INV-7 把它写成「与负载无关」；2. 重跑内部若干「放行方向」的分支（时间检查点、增长超限、VMAX、扩展项目的两条入口、分段模式）没有任何用例能让它们变红；3. 用例脚本本身在环境不对时会空转成绿。26 个我自己想的坏实现里 19 个漏网（见「变异测试」；这不是覆盖率，是我读过用例后专挑可疑处下手的缺口清单）。

**运行环境披露**：我的全部实验都在共享的 4 核宿主上，用 `taskset -c 0,1 nice -n 19`，负载均值 8–16（其他席同时在跑，我自己的批跑也占 2 核）。每份结果首行记了负载（`scratchpad/.../qa-engineer/res/M*.txt`）。我把红分成「逻辑红」和「计时/负载红」，只有逻辑红才算抓住。**提请汇总注意**：我的运行与其他席的 `sc-cases.sh` 重叠（约 17:26–18:17 UTC），`V5-S12` / `V5-S13b` 的全进程表扫描（QA-9）与计时窗口（QA-1）可能把我的运行当成干扰源，别席若在该时段见到这几条无关红，先排除这个原因。

## 审计结论

| 序号 | severity | category | scope | 针对 | 一句话 |
|---|---|---|---|---|---|
| QA-1 | Major | testing | `sc-direct.sh:65,73-79`、`sc-cases.sh:78,82-87`、README、INV-7、TASK-003/004 验收 | 验收用例 + 任务计划 | 带窗口 / 要求「重跑在截止前完成」的用例在负载下对好实现假红；「与负载无关」的成文说法不成立；`run()` 里锚点在 `mktemp` 之前、秒表在之后 |
| QA-2 | Major | testing | `shim/delay-first`、`sc-cases.sh:82-87` | 验收用例 | `sed` 垫片的「首次调用在作业里」假设一破，10 s 停顿落进主进程，把「回落正确」报成 `rc=124` / 窗口红 |
| QA-3 | Major | testing | `sc-cases.sh:85`（V3-E5，`SECRET_GUARD_TIME_BUDGET_S=1`） | 验收用例 | 预算取 1 时 `$SECONDS` 整秒翻转会让首遍自己写出时间文案，V3-E5 对好实现间歇假红 |
| QA-4 | Major | testing | 原型 `:723,734,757`（重跑内 3 个时间检查点）；SC-V4 | 验收用例 | 3 个检查点的 `return 3` 改成 `return 0`（放行）无人察觉（M06/M07/M08 漏网） |
| QA-5 | Major | testing | 原型 `:769`、`:824`；SC-V2 | 验收用例 | 扩展项目的两条入口没被钉住：stdin `cwd` 路径（M01）与分段触发点是否问准入门（M02）；M01 在 hook 级复现了放行 |
| QA-6 | Major | testing | 原型 `:742,766,797-799`；SC-V7、SC-V8 | 验收用例 | 重跑的「通过层」行为无端到端用例：增长超限放行（M17/M18，M18 hook 级复现）、分段模式不走 `_sg_vx_big_judge`（M10，破裁定 C）、分段回落原因串（M09） |
| QA-7 | Major | testing | 原型 `:643,727,797,799`；SC-V7、SC-V9 | 验收用例 | Decision 14 新造的可达路径与边界无用例：重跑内 VMAX（M24）、for 计数（M12）、空白填充躲过「只匹配规则」（M28，hook 级复现）、8192 边界（M13）、三个常量同值（M29） |
| QA-8 | Major | testing | `sc-cases.sh:16,25,41,126-127`；TASK-002 搬入套件 | 验收用例 | 环境不对时整轮空转成绿：`SC_BASH` 不存在得 `PASS 9 FAIL 0`、`sc-direct.sh` 崩了直调用例静默消失，退出码都是 0 |
| QA-9 | Minor | testing | `sc-direct.sh:80,109` | 验收用例 | `V5-S12` / `V5-S13b` 用 `ps -eo args` 扫全机进程表，别的运行的同名桩会让它假红（已在一次变异运行里撞见） |
| QA-10 | Minor | testing | `sc-direct.sh:86-93`（V5-S10） | 验收用例 | `ulimit -u 1` 对 uid 0 不生效，root 下好实现会红；另占 15 s，上界 16.5 s |
| QA-11 | Minor | testing | `sc-direct.sh:24,39`；`sc-cases.sh:89` | 验收用例 + proposal Decision 16 | 平台毒化只覆盖 `OSTYPE`，`MACHTYPE` / `HOSTTYPE` 同样可由环境改写（M04 漏网）；`aarch64` 行把未实测平台钉成「放宽」 |
| QA-12 | Minor | testing | `v31/commentsync.py`（V12-C1） | 验收用例 | 只验「旧文字没了、新词出现过」，整块删掉注释仍 GREEN |
| QA-13 | Minor | testing | 原型 `:833,848`；`sc-cases.sh:54` | 验收用例 | KILL 改 TERM 无用例能分辨（M20/M30）；`timeout` 会重置 TERM，用例环境本来就造不出「TERM 被忽略」 |
| QA-14 | Minor | testing | `W13-sc-cases.txt` 第 2 节；`sc-direct.sh:92,102` | 证据 | 基线红集 73 条里 52 条只是「函数不存在」（127），不是行为判别；基线轮缺 `V5-S10b/S10d` 两行（92 对 94） |

0 Critical，8 Major，6 Minor。下面逐条。

### QA-1　Major · testing · issue　（复发：PP1-A5 未收口、PP1-A29、PP1-A36）

- **scope**：`v31/sc-direct.sh:65`（`run()`）、`:73-79`（窗口 0..0.3 / 0.85..1.3）；`v31/sc-cases.sh:78`（`outcome` 的 4.5 s）、`:82-87`（`deadline` 窗口）；`v31/README.md` 末段「计时判据由 shim 的固定延迟给出，与负载无关」；`detailed-tasks.yaml` INV-7（「sc-cases.sh 的计时判据…不受本条约束」）、TASK-003（耗时矩阵 ≤ max(T_trigger,3 s)+0.3 s）、TASK-004（W13「FAIL 为 0」）。
- **针对**：验收用例 / 证据，连带任务计划。
- **摘要**：下界由 shim 的固定延迟给出这一点是对的，但上界是绝对墙钟，而且全部在 `nice 19` 的进程上量；另有一批用例的期望是「放宽重跑在截止前跑完」。负载一高，好实现就假红。INV-7 把 `sc-cases.sh` 排除在负载门之外，README 还写着「与负载无关」，TASK-004 的验收「FAIL 为 0」因此在共享宿主上不可重复。
- **证据**：
  1. 干净对照：原型在 bash 5.2.15、负载 2.16 时 `PASS 94 FAIL 0`（45.4 s，`run0-v31-bash52.txt`）。
  2. 同一原型加一处与计时无关的改动（M01、M04、M09、M12、M29、M30 等，其行为在这些用例上与原型等价），负载 7.4–16 时下列用例变红，细节行都在 `res/M*.txt`：`V2-E7`（hook 5.40 s，窗口 3.2..4.3）、`V9-E11`（hook 3.0x s 回落，基线自己 2.0–7.8 s；空闲时基线 0.74 s）、`V3-S4`（0.84 s，下界 0.85）、`V4-S7`（0.35 s，上界 0.3）、`V5-S14`（0.53 s）、`V3-E4`（3.89 s，窗口 2.85..3.6）、`V3-E3`（3.67 / 4.19 s）、`V6-E2`、`V2-E6`、`V7-E1`（3.24 s 回落）、`V4-S2/S3`（0.55 / 0.57 s）。
  3. 机理 a（测试自身的缺陷）：`sc-direct.sh:65` 先 `_SG_P0=$EPOCHREALTIME`，再 `err=$(mktemp ...)`（一次 fork+exec），再 `t0=$EPOCHREALTIME`。截止从 `_SG_P0` 起算、秒表从 `t0` 起算，`mktemp` 在负载下慢到 160 ms，就量出 0.84 s，下界 0.85 必红。V3-S4、V5-S5、V4-S6 同形。
  4. 机理 b：`outcome` 类用例（V7-E1、V9-E10、V9-E11、V7-E13/E14）要求首遍 + 重跑在 `_SG_P0 + 3 s` 内跑完。V9-E11 空闲时仅首遍就 0.74 s，负载 ×4 就被硬截止切走，看到的是基线字节（`kind=oversize`）而不是 `tmax`。
  5. 机理 c：V2-E7 的上界 4.3 s 没有鉴别力——BI-13 靠字节不同被抓，不靠墙钟；它只增加了一个对负载敏感的假红口。
  6. 计划侧：TASK-002 要求把这些用例「断言与期望值逐字照搬」进日常套件，等于把计时窗口带进每个开发者都会跑的 `secret-guard.test.sh`。
- **建议**：1. `sc-cases.sh` 开头读 `/proc/loadavg`，一分钟负载超过核数一半（或沿用 INV-7 的 2）就把计时窗口类用例整体标 SKIP（单独计数，TASK-002 已有「SKIP 单独列出」），并在结尾再读一次，升高则作废本轮；把 INV-7 的负载门扩到 W13、TASK-003 耗时矩阵、TASK-004。2. `sc-direct.sh:65` 改为先建 `err` 文件，再 `t0=$EPOCHREALTIME; _SG_P0=$t0`。3. 删掉 V2-E7 的上界，字节比对已够；其余上界改成「截止 + 3 s」或相对基线。4. 改正 README 与 INV-7 的措辞：下界不受负载影响，上界与「重跑能否在截止前跑完」受负载影响。5. TASK-002 把计时窗口类用例放进套件里一个默认关闭的分节（例如 `SG_TIMING=1`）。

### QA-2　Major · testing · issue　（复发：PP1-A8 部分）

- **scope**：`v31/shim/delay-first`（`sed` 首次调用停 10 s）、`sc-cases.sh:82-87`（`SC_DELAY_sed=10`）。
- **针对**：验收用例。
- **摘要**：垫片的假设是「第一次 `sed` 调用发生在作业里（第一份拦截文案的命令回显）」。只要作业在到达第一次文案输出之前被截止切掉，或准入门因「没时间了」而关闭，第一次 `sed` 调用就落到主进程的回落 / 基线文案上，停顿 10 s 发生在主进程里，hook 墙钟 11–12 s，常常撞上 `timeout 12` 得 `rc=124`。字节其实与基线相同（行为正确），报告上却是窗口红或 `rc=124`，与 BI-4 的真实签名（墙钟越界）无法区分。
- **证据**：M11 运行：`V6-E2`、`V3-E3`、`V3-E4`、`V2-E6` 都是 `hook rc=124 none 12.0x s`，`V3-E5` 11.13 s；M20 运行：`V3-E3 rc=124 12.01 s`；M24 运行：`V3-E3 rc=124`、`V3-E5 hook rc=2 oversize 12.19 s … stderr IDENTICAL`；`xp-tick.sh` 扫描 V3-E5 的原调用 20 次（负载约 11）：9 次墙钟 11.2–12.3 s（含 1 次 `rc=124`），11 次 1.03–1.15 s。后三者的 hook 在这些用例上行为与原型等价。
- **「换一种合法实现会不会失效」**：`jq` 这一头基本可靠：`_sg_ext_root` 只在 `CLAUDE_PROJECT_DIR` 为空且输入含 `"cwd"` 时才调 `jq`，且发生在触发点之后，shapes 的输入没有 `cwd`，所以首次 `jq` 就是 stdin 解析。`sed` 这一头不可靠：任何把回落文案提前渲染、把 `_sg_redact_echo` 换成纯 bash、或改用绝对路径 `/usr/bin/sed` 的合法重构，都会让停顿落错地方或根本不触发。失效方式是大声的（红或 12 s 超时），不是静默的，但会被误读为实现缺陷。
- **建议**：1. `SC_DELAY_sed` 从 10 降到 4（截止 3 s + 余量；停顿落错地方时墙钟约 7 s，仍在 `timeout 12` 内，用例还能给出可诊断的字节与 `kind`）。2. 或让垫片只在作业进程组内停顿（沿 `/proc/$PPID` 找 pgid 等于自身 pid 且不是 `timeout` 子进程的祖先）。3. `deadline` 类用例看到墙钟 ≥ 停顿时长就判 INCONCLUSIVE 并 SKIP，不报 FAIL。4. 在 `sc-cases.sh` 头注释里写明「首次 `sed` 在作业里」是对实现的耦合。

### QA-3　Major · testing · issue

- **scope**：`sc-cases.sh:85`（`deadline V3-E5-budget-1 … SECRET_GUARD_TIME_BUDGET_S=1`）；原型 `:614-625,641,733`（`_SG_T0=$SECONDS`、`_sg_over_budget`）。
- **针对**：验收用例。
- **摘要**：时间预算检查点用整秒的 `$SECONDS`。预算取 1 时，只要一个墙钟整秒边界落在「`_sg_vx_collect` 重置时钟」到「首遍第一个检查点」之间，首遍就自己写出时间文案并退出，hook 永远走不到触发点。V3-E5 期望的是基线 oversize 文案，于是对好实现间歇假红。
- **证据**：M29 运行（M29 与原型在 V3-E5 上等价）：`FAIL V3-E5-budget-1 hook rc=2 time 10.74s … stderr DIFFERENT`；`xp-tick.sh` 扫描里相位 .05 的一次：`TIME-TEXT`。两次都是预算 1 下的时间文案；其中 10.74 s 是时间文案那次 `sed` 调用又触发了 QA-2 的停顿。空闲机器上的概率我**未实测**；按暴露窗口等于 `_sg_vx_collect` 在 16 KB 命令上的耗时估计，是百分之几量级，TASK-004 五个 bash 各跑一遍就有明显的整体失败率。
- **建议**：V3-E5 的预算改取 2（窗口改为 1.85..2.6）。它仍能区分 `cap = min(budget,3)` 与常量 3（M21 在预算 1 和 2 下都被抓），又需要连过两个整秒边界才触发，首遍的几十毫秒碰不上。

### QA-4　Major · testing · issue

- **scope**：原型 `:723`（`cr==3` 收集链检查点）、`:734`（整串）、`:757`（分段）三处 `[[ -n "${_SG_RELAXED:-}" ]] && return 3`；proposal What 2 末条（「三个协作式时间检查点直接返回 3」）；SC-V4。
- **针对**：验收用例。
- **摘要**：这三行的契约是「重跑里时间到了就回落（返回 3）」。把任意一行的 `return 3` 改成 `return 0`，重跑就在没判完时放行，且没有任何用例变红：M06、M07、M08 均漏网。`V4-S7` 只桩掉 `_sg_vx_pass` 自身，验证的是作业对退出码 3 的映射，不是这三行。
- **可达性**：检查点比较整秒的 `$SECONDS`，默认预算 3 时，在重跑重置时钟后 2–3 s 内触发，硬截止是 `_SG_P0 + 3`、`_SG_P0` 早于重置，所以对跑得久的重跑，协作式检查点在多数相位下**先于**硬截止触发——这是慢重跑的常规出口，不是边角。
- **证据**：`xp-newcases.sh` 的探针（确定性，无墙钟窗口）：T1/T2/T3 在原型上都是 `3/none`，M08/M06/M07 上都是 `0/none`；对照 T0（基线遍，`_SG_RELAXED` 为空）是 `2/time`。`SECRET_GUARD_TIME_BUDGET_S=0` 让 `_sg_over_budget` 立即为真，基线自己的套件也用这个办法。
- **建议**：直调增补三条用例：`_SG_RELAXED=1; export SECRET_GUARD_TIME_BUDGET_S=0;` 再分别对 `'a=1; b=2; : $a $b' whole`（收集链）、`'a=1; : $a' whole`、`_SG_SEGS=('a=1' ': $a'); … segment` 调 `_sg_vx_pass`，断言返回 3 且 stderr 为空。把 M06/M07/M08 加进 `mutants.py`。

### QA-5　Major · testing · issue

- **scope**：原型 `:824`（`_sg_relax_noext` 经 `_sg_ext_root` 取项目根）、`:769`（分段触发点 `if _sg_relax_ok`）、`:745`（整串触发点）；`sc-direct.sh:42-46`（V2-G4）、`sc-cases.sh:90`（V2-E9）；SC-V2。
- **针对**：验收用例。
- **摘要**：「有扩展的项目与基线逐字节相同」是为了让重跑里的 `return 0` 跳过扩展腿不致漏检。该不变量的两条入口无用例：1. 项目根只由 stdin `cwd` 给出（基线 `_sg_ext_root` 同时认 `CLAUDE_PROJECT_DIR` 与 `cwd`，V2-G4、V2-E9 只用前者）；2. 分段模式的触发点是否真的问准入门（V2-E9 是整串模式，唯一把准入门当「被绕过」检出的 e2e）。
- **证据**：M01（`_sg_relax_noext` 只读 `CLAUDE_PROJECT_DIR`）与 M02（分段触发点 `if true`）整轮无逻辑红。**hook 级复现 M01**（`xp-ext.sh` 的 B 段，输入 JSON 的 `cwd` 指向列出了被读路径的扩展项目，无 `CLAUDE_PROJECT_DIR`）：基线 rc=2 oversize、原型 rc=2 oversize、M01 **rc=0**——一个被扩展列出的路径在大命令里被放行，两次复现一致。M02 在 hook 级的演示被负载冲掉（基线自己也要 6–9 s），不下结论；通过层探针 G2：原型 `2/oversize`，M02 `4/none`。M03（整串触发点绕过准入门）被 V2-E9 抓住，但只此一条。
- **建议**：增补：V2-G4b（`input='{"cwd":"<含扩展文件的目录>"}'`，不设 `CLAUDE_PROJECT_DIR`，期望准入门关闭）；V2-G12/G13（桩掉 `_sg_relax_platform` 返回 1 后对大副本调 `_sg_vx_pass`，整串与分段都期望返回 2 而不是 4，即「调用点真的问了准入门」）；e2e 形状 `ext-read-seg`（分段模式 + 扩展项目）与 `ext-read-cwd`（只给 cwd）按 identity 比对。

### QA-6　Major · testing · issue

- **scope**：原型 `:742`、`:766`（增长超限，整串 / 分段）、`:797-799`（`_sg_vx_big_judge` 的路由调用点）、`:769`（分段回落原因串）；SC-V7、SC-V8；`sc-cases.sh` 的 `kind()` 里 `growth` 从未被任何用例要求。
- **针对**：验收用例。
- **摘要**：P8（增长 > 8192 仍拦）只在函数层有用例（`V8-D*` 调 `_sg_vx_apply` 看状态码），通过层与端到端没有；分段模式的重跑（路由到 `_sg_vx_big_judge`、回落原因串）也没有任何带读取的 e2e。
- **证据**：M17（分段增长超限改 `continue`）、M18（整串增长超限改 `return 0`）、M10（分段模式重跑不走 `_sg_vx_big_judge`）、M09（分段回落原因串写成整串那条）全部漏网。通过层探针：V2 原型 `2/growth`、M17 `0/none`；V3 原型 `2/growth`、M18 `0/none`；S2 原型 `2/longline`、M10 `0/none`（分段副本里最长行 > 8192、带 `| wc -c` 过滤：M10 走普通判定拿到 credit 放行，**违反裁定 C**）；S1 原型回落串以 `a command segment is longer than` 开头，M09 以 `the command is longer than` 开头。**hook 级复现 M18**：整串读凭据形配置路径且增长 > 8192，基线 rc=2 oversize、原型 rc=2 growth、M18 **rc=0**。旧套件 W9 的 21ag/21aj/21al/21ao 改写后可能是这几条的后盾，**未核实**（W9 约 25 分钟，按任务书未跑）。
- **建议**：增补直调用例 V2/V3/S1/S2（`xp-newcases.sh` 里有可直接搬的断言）；增补分段模式 e2e 形状：`seg-longline`（读 + 超长行）、`seg-growth`、`seg-fallback`（配 `sed` 垫片），并让 `outcome` 支持 `growth` 这一 kind。

### QA-7　Major · testing · issue

- **scope**：原型 `:643`（`ca/cf` 计数放开）、`:727`（`cr==2` VMAX 分支）、`:797`（`IFS= read -r line`）、`:799`（`max > _SGV_LMAX`）；proposal What 2、P7、P9。
- **针对**：验收用例。
- **摘要**：Decision 14 放开重跑里的计数上限后，一些原来到不了的路径变得可达，用例没跟上：
  1. **M24 重跑内 VMAX**：第 17 个赋值的值 > 4096，基线只收集前 16 个所以不会触发 VMAX，重跑收集全部才第一次碰到它；`cr==2` 被忽略则部分收集后继续，后面的赋值（读取所在）没被收集就放行。`V9-E12` 只覆盖基线遍里的 VMAX。探针 V1：原型 `2/vmax`，M24 `0/none`。
  2. **M12 for 计数**：重跑只放开赋值计数、保留第 9 个 for 不收集；`V9-C1` 数赋值、`V9-C2` 数引用，没有数 for 的。探针 C1：原型收集 9，M12 收集 8。
  3. **M28 空白填充躲过裁定 C**：行长循环写成 `read -r line`（漏 `IFS=`，经典执笔错误）会把行首行尾空白削掉，一条被尾部空白撑到 > 8192 的行量出来很短，走普通判定拿到 `| wc -c` 的 credit。**hook 级复现**：`(true); F=<凭据形配置路径>; cat $F | wc -c` 后接 9000 个空格，基线 rc=2 oversize、原型 rc=2 longline、M28 **rc=0**；对照（用 `z` 填充）原型与 M28 都是 longline，所以判别量确实是空白。V10/V7-N5 的长行没有首尾空白。
  4. **M13 边界 `>=`**：无用例探 8192 / 8193。探针 L2：原型 `2/finding`，M13 `2/longline`。
  5. **M29 常量同值**：`_SGV_SMAX`、`_SGV_LMAX`、`_SGV_GMAX` 都是 8192，用错常量名不可观察，探针也分不开。
- **建议**：增补 V9-C3（第 17 个赋值 > 4096 → 重跑返回 2，文案为 VMAX）、V9-C4（第 9 个 for）、V7-N6（带首尾空白的长行路由到只匹配规则）、V7-N7/N8（8192 走普通判定、8193 走只匹配规则）；另跑一轮「常量扰动」：对原型副本把 `_SGV_GMAX` 改 8190、`_SGV_LMAX` 改 8200，让每个用法各自可观察。

### QA-8　Major · testing · issue

- **scope**：`sc-cases.sh:16`（`SC_BASH` 只 `readlink -f`）、`:25`（用 `read` 取版本，失败无检查）、`:41`（`2>/dev/null`、进程替换退出状态被丢弃）、`:126-127`（只按 FAIL 计数退出）；TASK-002 把整套搬进 `secret-guard.test.sh`。
- **针对**：验收用例。
- **摘要**：没有金丝雀，也没有「应出现的用例编号」断言。环境不对时，基线与被测 hook 以同样方式失败，`identity` 比对成立，整轮是绿的。
- **证据**（`xp-harness.sh`）：H1：`SC_BASH` 指向不存在的文件 → 九条 e2e 全 `PASS … rc=127 … stderr IDENTICAL`，`# totals: PASS 9 FAIL 0`，退出码 0。H2：把 `sc-direct.sh` 换成一个立刻 `exit 1` 的脚本 → 直调用例整体消失，`# totals: PASS 6 FAIL 0`，退出码 0。`taskset`、`timeout`、`jq`、`python3` 缺失是同一类（两边都 127）。
- **建议**：1. 起手跑一次金丝雀：`"$SC_BASH" -c :` 必须成功；基线对 `p1-small-read` 必须 rc=2 且 `kind=finding`、对 `p1-small-benign` 必须 rc=0，否则 `SETUP` 退出 3。2. `sc-direct.sh` 末行输出哨兵 `END sc-direct`，缺哨兵或退出状态非 0 即 FAIL。3. 每个模式（relax / norelax）维护期望的用例编号清单，缺一条即 FAIL；注意基线轮本来就少 `V5-S10b/S10d`（QA-14）。4. 检查 `taskset`、`timeout`、`jq`、`python3`、小数秒 `sleep` 的存在。

### QA-9　Minor · testing · issue

- **scope**：`sc-direct.sh:80`（`ps -eo args | awk '$1=="sleep" && $2=="7.777"'`）、`:109`（五个固定秒数）。
- **摘要**：扫的是整机进程表，按参数文本匹配。别的运行（另一个终端、另一席、并行 CI）里同名的桩 `sleep` 会被算进来。
- **证据**：`xp-harness.sh` H3：自己起一个 `sleep 2.718`，V5-S12 的扫描数出 1（用例要求 0）。野外撞见一次：M10 运行里 `FAIL V5-S12-no-leftovers … alive after the cases: 1`，与 M10 无关，当时我这边只有该批的运行器本身，来源大概率是别席并行的 `sc-direct.sh`（无法证明具体进程）。
- **建议**：桩用每次运行唯一的时长（`sleep 7.777$$` 之类），或用 `/proc/*/stat` 的 session / pgid 限定在本次运行的进程组。

### QA-10　Minor · testing · risk

- **scope**：`sc-direct.sh:86-93`（V5-S10 用 `ulimit -u 1` 制造 fork 失败，等 bash 重试约 15 s，上界 16.5 s）。
- **摘要**：本机 `getrlimit(2)` 的 man 页写着「RLIMIT_NPROC 对 CAP_SYS_ADMIN、CAP_SYS_RESOURCE 或 real uid 为 0 的进程不生效」。root 下 fork 不会失败，计时器照常起来，桩判定照常放行，`V5-S10` 得 rc=0，`V5-S10b` 得「判定已开始」，好实现红。容器里以 root 跑套件是常态；README 的依赖清单没有写「非 root」。我没有 root 环境，未实跑；本机 uid=1000 下实测 15.00 s 通过。
- **建议**：起手探测 `( ulimit -u 1; : & wait ) 2>/dev/null` 是否真的 fork 失败，不失败就 SKIP 并单独计数；上界加宽到 20 s。

### QA-11　Minor · testing · decision

- **scope**：`sc-direct.sh:39-40`（V2-G3b 只设 `OSTYPE=darwin21`）、`sc-cases.sh:89`（V2-E8 只设 `OSTYPE`）、`sc-direct.sh:24`（`aarch64-unknown-linux-gnu 5 2 → 放宽`）。
- **摘要**：1. bash 的 `OSTYPE`、`MACHTYPE`、`HOSTTYPE` 都能从环境导入。原型读 `${BASH_VERSINFO[5]}` 是对的，但把它换成 `$MACHTYPE` 的坏实现（M04）与 `OSTYPE` 毒化互不相干，整轮无逻辑红。探针 G4（`MACHTYPE=x86_64-apple-darwin23.0.0 HOSTTYPE=aarch64`）：原型准入门开（0），M04 关（1）；hook 级同向（原型 rc=0，M04 rc=2）。2. Decision 16 的字面是「只认**实测过的** GNU/Linux」，而实测只在 x86_64 上做过（W13 页眉），测试表却把 `aarch64` 钉成「放宽」，实际由模式 `*-linux-gnu*` 决定。
- **建议**：V2-G3b、V2-E8 的毒化加上 `MACHTYPE`、`HOSTTYPE`；`aarch64` 行要么去掉，要么在 Decision 16 里写明「按模式而非按实测」。

### QA-12　Minor · testing · issue

- **scope**：`v31/commentsync.py` 的 target 模式（V12-C1）。
- **摘要**：target 模式只验三件事：旧锚点短语为 0、旧块的 sha256 不在、ADD 词在任意注释里出现过。删除而不是改写一整块注释它照样 GREEN。脚本头注释已承认「改写后的文字由 TASK-005 复核」。
- **证据**：把 `LENGTH BUDGET` 一块 13 行注释整段删掉（`mut/C01.sh`），`commentsync.py --hook-only … target` 输出 `GREEN`，退出 0。
- **建议**：给每个站点绑定必须出现的新短语（站点内），或在 TASK-005 的清单里明写「核对每块注释存在且表述与代码一致」，不要让 V12-C1 的绿被当成文档同步的证据。

### QA-13　Minor · testing · risk

- **scope**：原型 `:833`（计时器）、`:848`（作业结束后的组杀）；`sc-cases.sh:54`（`timeout 12 "$SC_BASH"`）。
- **摘要**：把两处 `kill -KILL` 改成 `kill -TERM`（M20，或只改计时器的 M30），在默认处置下行为一样，用例分不开。更糟的是用例环境造不出差别：`timeout` 会给子进程重置 TERM 处置，所以即便外层 `trap '' TERM` 也传不进 hook。
- **证据**（`xp-term.sh`，`bash termwrap.sh` 放在 `timeout` 之后忽略 TERM）：原型：默认 3.62 s 回落，TERM 被忽略 4.22 s 仍回落；M20：TERM 被忽略时 **11.24 s** 才出放宽文案；M30：10.80 s。截止被架空、hook 超过 Claude Code 的 5 s 后被杀并放行，是这类坏实现的后果。要求环境里 TERM 被忽略，所以只列 Minor。
- **建议**：加一条 `deadline` 用例，用 `timeout … bash -c 'trap "" TERM; exec bash <hook>'` 起 hook，期望仍在窗口内回落。

### QA-14　Minor · testing · issue（证据质量）

- **scope**：`W13-sc-cases.txt` 第 2 节；`sc-direct.sh:92,102`；TASK-002 末步「红集与 W13 第 2 节一致」。
- **摘要**：我用脚本把基线红集的 73 条分类：**52 条是「函数不存在」**（V2-G* 25 条、V3-G9/G10、V3-S4 与 V4-/V5- 桩 14 条、V10-N3/N4、V7-N5、V11-S1 七条、V11-S3），只有 21 条是行为 / 文案判别（V8-D1/D2 四条、V9-C1/C2 三条、V10-N2、七条以上的 e2e、V2-G11、V12-C1）。负向的准入门用例（期望状态 1）在基线上红，只因 127 ≠ 1，而不是因为基线「放宽」了。另外基线轮只有 92 行：`V5-S10b` / `V5-S10d` 只在注入锚点找得到时才输出，基线上走 `SETUP` 分支，所以这两条无法在基线上变红。`V7-E15`（`|| same`）在基线上也是绿的。
- **建议**：直调用例把状态 127 单独记成 `MISSING`，红集分「缺失」与「判错」两栏；TASK-002 的对照据此逐栏核；QA-8 的编号清单对基线轮另列。

## 变异测试

**方法**：被测是 `mkv31.py` 生成的原型（`v31.sh`）；每个坏实现 = 原型 + 一处改动（`mkmut.py`、`mkmut2.py`，每处替换断言恰好命中一次）；**运行前**先把预期抓住它的用例与理由写进 `predictions.tsv` / `predictions2.tsv`；再对每个坏实现跑一次未改动的 `sc-cases.sh`（bash 5.2.15，直调 + e2e + 静态，约 45 s 空闲、60–180 s 负载下）。红分两类：逻辑红（算抓住）与计时 / 负载红（见 QA-1/2/3，不算）。我是读过用例之后专挑可疑处下手的，所以这不是盲测，也不是覆盖率；漏网清单可直接并入 `mutants.py` 当 BI-24 以后。TASK-003 仍应保持盲构造。

| 坏实现 | 改动 | 运行前预期抓住它的用例 | 实际 | 备注 |
|---|---|---|---|---|
| M01 | `_sg_relax_noext` 只读 `CLAUDE_PROJECT_DIR`，不走 `_sg_ext_root` | 无（V2-G4 / V2-E9 只用环境变量路径） | 漏网 | 无关红 V2-E7（负载）。探针 G1：1 对 0；hook 级放行复现 |
| M02 | 分段触发点 `if _sg_relax_ok` → `if true` | 无（V2-E9 是整串） | 漏网 | 全绿。探针 G2：`2/oversize` 对 `4/none` |
| M03 | 整串触发点同上 | V2-E9 | 抓住：V2-E9 | 对照；无关红 V9-E11（负载） |
| M04 | 平台实参 `${BASH_VERSINFO[5]}` → `${MACHTYPE}` | 无（只毒 OSTYPE） | 漏网 | 无关红 5 条（负载）。探针 G4：0 对 1 |
| M05 | 小版本上限 `<= 3` → `<= 9` | V2-G2 的 5.4 行 | 抓住 | 对照 |
| M06 | 整串检查点 `return 3` → `return 0` | 无 | 漏网 | 探针 T2：3 对 0 |
| M07 | 分段检查点同上 | 无 | 漏网 | 探针 T3 |
| M08 | 收集链检查点同上 | 无 | 漏网 | 探针 T1 |
| M09 | 分段回落原因串写成整串那条 | 无 | 漏网 | 无关红 V3-E3（负载）。探针 S1 |
| M10 | 分段模式重跑不走 `_sg_vx_big_judge` | 无 | 漏网 | 无关红 V5-S12（QA-9 的跨运行干扰）。探针 S2：`2/longline` 对 `0/none` |
| M11 | 整串模式重跑不走 `_sg_vx_big_judge` | V7-E14 | 抓住：V7-E14（`kind=finding`） | 对照；另有负载 + QA-2 的 `rc=124` |
| M12 | 重跑放开赋值计数、保留 for 计数 | 无 | 漏网 | 无关红 V3-E3（负载）。探针 C1：9 对 8 |
| M13 | 行长边界 `>` → `>=` | 无 | 漏网 | 全绿。探针 L2 |
| M14 | 量不出行长时哨兵 `max=_SGV_LMAX+1` → `max=0` | 无 | 漏网 | 全绿；未探（需让 here-string 失败，bash 5.0 用临时文件） |
| M15 | 重跑拦截文案不带末尾换行 | 无 | 漏网 | 无关红 V9-E11（负载）；未探（差异显然） |
| M16 | 退出码 2 且无文本也当拦 | V4-S3 | 抓住 | 对照 |
| M17 | 分段增长超限 → `continue` | 无 | 漏网 | 全绿。探针 V2：`2/growth` 对 `0/none` |
| M18 | 整串增长超限 → `return 0` | 无 | 漏网 | 无关红 V9-E11（负载）。探针 V3；hook 级放行复现 |
| M19 | 去掉 `exec 2>/dev/null` | V6-E2（若 bash 打印作业终止通告） | 抓住：V5-S5、V4-S6、V4-S11、V5-S10、V5-S10c、V5-S14（stderr 非空）；V6-E2、V3-E4、V2-E6（字节不同） | 预测对 |
| M20 | 计时器与组杀都用 TERM | 无 | 漏网 | 无关红 V7-E1、V3-E3（负载 / QA-2）。TERM 被忽略：11.24 s |
| M21 | `cap=3` 常量 | 无（**预测错**） | 抓住：V2-G6、V2-G8、V3-G9、V3-S4、V5-S5、V4-S6、V3-E5 | 我误以为预算 ≠ 3 的用例看不到它；这些用例用的正是预算 1 / 0 |
| M22 | 作业写死 `whole` 模式 | V9-E11 | 抓住：V9-E11（`kind=growth`） | 对照；V6-E2、V3-E4 的红是负载 |
| M24 | 重跑内 `cr==2`（VMAX）被忽略 | 无 | 漏网 | 红全是计时。探针 V1：`2/vmax` 对 `0/none` |
| M28 | 行长循环 `IFS= read` → `read` | 无 | 漏网 | 红全是计时。探针 L1；hook 级放行复现 |
| M29 | 只边界处 `_SGV_LMAX` → `_SGV_SMAX`（同值 8192） | 无（等价） | 漏网（等价） | V3-E5 出时间文案（QA-3） |
| M30 | 只计时器用 TERM，组杀仍 KILL | 无 | 漏网 | TERM 被忽略：10.80 s |

合计 26 个：抓住 7 个（M03、M05、M11、M16、M19、M21、M22），漏网 19 个。预测与结果一致 25 个，错 1 个（M21）。19 个漏网里，行为差异被探针或 hook 级演示证实的 16 个（M01、M02、M04、M06、M07、M08、M09、M10、M12、M13、M17、M18、M24、M28，以及 TERM 的 M20、M30）；M14、M15 只按构造判定有差异、未探；M29 目前等价。放行方向（fail-open）的漏网：M01、M02、M06、M07、M08、M10、M17、M18、M24、M28。

**建议用例的可证伪性**（`xp-newcases.sh`：直调、确定性、无墙钟窗口；「原型」是用例该有的绿，「坏实现」是它该变红的值）：

| 探针 | 原型 | 坏实现 |
|---|---|---|
| G1 stdin `cwd` 指向扩展项目时准入门 | 1（关） | M01：0（开） |
| G2 分段触发点问准入门（平台桩失败时 `_sg_vx_pass`） | 2 / oversize | M02：4 |
| G3 整串触发点同上 | 2 / oversize | M03：4 |
| G4 `MACHTYPE=apple` `HOSTTYPE=aarch64` 下准入门 | 0（开） | M04：1 |
| T1 / T2 / T3 重跑内三个时间检查点（预算 0） | 3 / 3 / 3 | M08 / M06 / M07：0 |
| T0 基线遍的检查点（对照） | 2 / time | — |
| V1 第 17 个赋值 > 4096 | 2 / vmax | M24：0 |
| V2 / V3 分段 / 整串增长超限 | 2 / growth | M17 / M18：0 |
| L1 尾部空白撑长的行 + `\| wc -c` | 2 / longline | M28：0 |
| L2 恰 8192 字符的行 | 2 / finding | M13：2 / longline；M29 同原型 |
| L3 恰 8193 字符的行 | 2 / longline | M13、M29 同原型 |
| S1 分段回落原因串 | 4 / `a command segment is longer than` | M09：4 / `the command is longer than` |
| S2 分段副本最长行 > 8192 带过滤 | 2 / longline | M10：0 |
| C1 重跑内第 9 个 for | 收集 9 | M12：8 |

另：作者的 BI-1..BI-23 我没有重跑，沿用 W13 第 3 节的结果；对照类坏实现（M03、M05、M11、M16、M19、M21、M22）被指定用例抓住且红的原因与预期一致，说明作业协议、截止、进程组、退出码 77 这一块的用例是实的。

## Verdict

**PASS_WITH_WARNINGS**（0 Critical，8 Major，6 Minor）。

没有 Critical：我没有发现「照计划逐字落地原型就会出现新的 fail-open、漏检或越过截止」的缺陷；原型本身在我能构造的输入上与基线 / 声明一致（M01、M02、M18、M24、M28 的放行都是**坏实现**造成的，不是原型）。Major 的共同点是：现有验收挡不住这些执笔错误，或者在合理的运行条件下对好实现假红。按影响排序，建议先做：1. QA-1 / QA-2 / QA-3（让计时类用例在共享宿主上可重复，否则 TASK-004 的「FAIL 为 0」没法当闸门）；2. QA-4 到 QA-7 增补确定性直调用例（`xp-newcases.sh` 里的探针已验证能分开好坏）并把 16 个漏网坏实现并入 `mutants.py`；3. QA-8 的金丝雀与编号清单（TASK-002 搬进套件之前）。保持不变的部分：作业协议 / 截止 / 进程组 / 77 的用例设计、准入门各条件的单独隔离、期望值随 `SC_BASH` 而定的逻辑（`RELAX` 的推导与准入门同源，五个 bash 上自洽）。

## 轮次记录

- **做了什么**：1. 读任务书、`v31/README.md`、`sc-cases.sh`、`sc-direct.sh`、`shapes.py`、`shim/`、`mutants.py`、`run-mutants.sh`、`commentsync.py`、`run-evidence.sh`、`W13-sc-cases.txt`、`W8-v31.diff` 全文；`detailed-tasks.yaml` 第 1–130 行、`proposal.md` 的 What 1–5、P1–P10、SC-V1–V12、BI 表、Impact、Decision record；`dispositions.md` 的 PP1 处置表（只取 A5/A7/A8/A13/A29/A36 的行）；原型 `v31.sh` 的相关函数与 `secret-guard.test.sh` 的头部。2. 用 `mkv31.py` 重新生成原型（sha256 前缀 `9f61db0e7b8b`），在 bash 5.2.15 上跑一遍未改动的 `sc-cases.sh`：负载 2.16，`PASS 94 FAIL 0`，45.4 s，复现 W13。3. 构造并运行 26 个坏实现，每个一遍完整 `sc-cases.sh`（`runmut.sh`，结果在 `res/`）。4. 实验：`xp-harness.sh`（H1/H2/H3）、`xp-ext.sh`、`xp-fo.sh`、`xp-newcases.sh`、`xp-tick.sh`、`xp-term.sh`、MACHTYPE 毒化、commentsync 删块、基线红集分类脚本。
- **工件位置**：`/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r2/qa-engineer/`（`mkmut.py`、`mkmut2.py`、`predictions.tsv`、`predictions2.tsv`、`mut/`、`res/`、`xp-*.sh`、`xp-out.txt`、`xp-out2.txt`、`run0-v31-bash52.txt`）。坏实现只存在于该目录。
- **没核实**：1. 其他 bash（5.0.18 / 5.1.16 / 5.3.20 / 3.2.57）上的用例结果，我只在 5.2.15 上跑；W13 第 1 节对它们的 PASS 94 / 57 未独立复现。2. 旧套件 W9（21ag/21aj/21al/21ao 等改写后的断言）能否抓住 M17/M18 等，按任务书未跑。3. 空闲机器上 V3-E5 的间歇红概率（QA-3）。4. root 下 V5-S10 的行为（QA-10 引的是 `getrlimit(2)` 本机 man 页，没有 root 环境）。5. 逗号小数点的 locale（本机没装；`de_DE` 源在 `/usr/share/i18n`，我没用 `localedef` 建）。6. M02、M17、M24 的 hook 级放行：演示被负载冲掉（基线自己要 6–12 s），只有通过层探针；M01、M18、M28 的 hook 级放行是干净复现。7. M14（here-string 失败）、M15 只按构造判定有差异。8. R1 汇总报告全文没读，复发簇号只对照了 `dispositions.md` 的处置行。9. W11 / W12 未审。10. 我的运行与别席重叠，对其造成的干扰（QA-9）无法逐条核对。
- **提醒**：我的变异体是读过 `sc-cases.sh` 之后设计的（按任务书要求），TASK-003 里的独立席应保持盲构造；本报告的漏网清单可作为它的最低要求。
- **工具调用**：约 66 次（含被拒的一次前台 `sleep` 等待）。
