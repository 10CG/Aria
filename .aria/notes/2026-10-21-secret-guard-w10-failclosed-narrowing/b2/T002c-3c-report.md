# TASK-002 第三步 3c 报告 (10CG/aria-plugin#217)

执笔席: 3c 新实例。worktree `scratchpad/wt217/aria`, 起点 `fee1a65` (3b), **未 commit**。全部输出在 `scratchpad/r217impl/t002e/` (驱动 `drive2.sh` / `drive3.sh`, 时间线 `drive.log`, 补丁脚本 `patch3c.py`, 表格脚本 `reftab.sh`)。
工具调用 51 次。hook (`af4658b6f935`) 一字未改; `v31/run-mutants.sh` 未改。

## 0. 现状 (先写预期再测)

预期 (开跑前写下): 0a worktree `SG_W10_ONLY=.` (PATH 上的 bash 5.2.15) 136 PASS; 0b `v31/run-suite.sh` + BI-8 + `SG_W10_ONLY=^(V9-E12-vmax-unchanged)$` 下 V9-E12 PASS (漏抓)。

实测 (worktree 未改动时跑):
- 0a (13:22:02-13:22:51 UTC): PASS 136 / FAIL 0 / SKIP 0, 计时批 judged (负载 开 1.15 / 尾 1.49)。符合预期。
- 0b (13:25:51): `PASS V9-E12-vmax-unchanged hook rc=0 none 0.62s | gate-closed rc=0 none 0.63s | stderr IDENTICAL`, 套件退出 0 (BI-8 hook `ff9f7a43eb7e`, 由 mutants.py 从实现构造)。符合预期, 即主控复核实测的漏抓。
- 附记: 第一个 step0 驱动在等负载时 (尚未开跑任何一轮) 被我按它自己记下的 PID 停掉, 改由 drive2 先做基线测量、再跑 step 0; 上面是 drive2 那次的结果。

## 1. 改了哪些文件

| 文件 | 改动 | sha256 前缀 (改后) |
|---|---|---|
| worktree `hooks/tests/secret-guard.test.sh` | (a) 移植块块首注释加一段 `[reference]` 说明 (是什么、为什么: 口径 (ii) 的漏洞, BI-8 实例)。(b) 新增 `sg_w10_ref` (参照表, **按编号查表**) 与 `sg_w10_refok` (核对), 放在 `sg_w10_identity` 之前。(c) `sg_w10_identity` / `sg_w10_deadline` / `sg_w10_outcome`: 两臂跑完后、原判定之前先调 `sg_w10_refok`; 不符时: 关门臂 rc 124 记 `[timeout12]`、出现时间文案记 `[time-text]`, 都经 `sg_w10_timed` 按计时类处理 (与 `sg_w10_slow` 同一口径), 否则 `FAIL ... [reference]`, 细节写出关门臂实测 rc/文案种类与参照。`sg_w10_cases` 里的调用行不变 (查表, 不加参数)。(d) 6 组: `wpa_x_hit` 之后新增 `wpa_x6_eval` / `wpa_x6` 与计数器, 带判法与理由注释; 6 组共用注释末加一句; 放宽支 10 条触发点命令改走 `wpa_x6` (21ab 三条、21ac 4096 for 表、21ag、21aj 三条、21al / 21ao 的 8193); `wpa_x_hit` 那几条与全部基线支一字未改。(e) Summary 6 组那一行加 `deadline fallback (截止回落) N / M (组名)` | `d085afae6834` |
| worktree `hooks/tests/lib/secret-guard-w10-direct.sh` | 头注释写明 `[reference]` 与原因, 标签表加 `[reference]`; 新增 `fbref` (V6-S20 / S21 的参照); `fbt` 在原判定前先核关门调用的 `_sg_vx_pass` 返回值与 `kindf`: 不符记 `FAIL [reference]` (出现时间文案时记 `TIMED ok bad ... [time-text]`); 细节由 `(status $rb)` 改为 `(status $rb $kb)` | `213d01379695` |
| worktree `hooks/tests/lib/sg-shim/delay-first` | 只改头注释 (原 2 行 "Test shim for sc-cases.sh ..." 改为套件里的用法 4 行); 非注释行逐字节相同 (diff 去掉 `#` 行为空) | `5c5c04525a67` |
| 主仓 `v31/run-suite.sh` | 首行另记 helper 的 sha256 前缀 (`| helper <12位>`, 副本里没有 helper 时写 `missing`), 头注释同步 | — |

`v31/commentsync.py --suite-only <新套件> target`: GREEN。

### 6 组判法的实现要点 (`wpa_x6 <longline|pass|growth> <基线支的 limit 行> <命令>`)
- 每条触发点命令只跑一次 hook: 先建输入, 再用 `EPOCHREALTIME` 只量 hook 本身 (与 `wpa_err` 同一管道, `env` 前加 `-u SECRET_GUARD_TIME_BUDGET_S`, 截止固定 3 s)。
- 两套断言在**同一份输出**上求值: `wpa_x6_eval` 在子 shell 里把 `wpa_err` / `wpa_rc` 换成交回这份输出, 再调原来的断言 helper (`wpa_x_longline` / `wpa_x Bash 0` / `wpa_x_toolarge ... $wpa_L_gseg`, 基线支是 `wpa_x_toolarge` + 该组 else 分支的 limit 行), 所以判的正是原断言代码, 没有复写。
- 放宽支断言成立 → 通过; 否则基线支断言成立且墙钟 >= 2.85 s → 通过并计一次截止回落; 都不成立 → 该组记一处不符, 细节写两套断言各自不符的项与墙钟。每组仍计一次。

## 2. 参照表

测量: 基线 `git show 59e333c:hooks/secret-guard.sh`, sha256 前缀断言 `e83c5e30f2cc` (INV-9, 驱动里先断言)。经 `run-suite.sh` 跑 `SG_W10_ONLY='^V[0-9]+-E[0-9]|^V6-S2[01]'` 并开 `SG_W10_LOG`, 5 个 bash 各一轮 (13:17-13:18 UTC; 量的是退出码与文案种类, 没设负载门)。所用套件与 helper 就是最终的 3c 版本 (同为 `d085afae6834` / `213d01379695`), 所以基线上也跑了 `[reference]` 核对: 0 处不符 (自洽); 表里的值取自细节字段 (`gate-closed rc=<rc> <kind>`, fbt 的 `(status <rb> <kb>)`), 不是取自表本身。实现一侧取自第 3 节 5 轮过滤轮的日志。`reftab.sh` 把 10 份日志合成一张表: 25 行, **0 行有差异** (`t002e/reftab-both.txt`)。

| 编号 | 调用 | 输入 (形状) | 关门臂的变量 (5.x 放宽平台 / 3.2 回落成 identity) | 59e333c (5.0/5.1/5.2/5.3/3.2) | 实现关门臂 (同 5 个 bash) |
|---|---|---|---|---|---|
| V7-E1-benign-big-allowed | outcome | benign-big | WSL_DISTRO_NAME=Ubuntu | 2 oversize ×5 | 同 |
| V6-E2-deadline-fallback-bytes | deadline | stall-read | 5.x: 只有 WSL 标记 / 3.2: + SC_DELAY_sed=10 | 2 oversize ×5 | 同 |
| V3-E3-anchor-at-hook-start | deadline | stall-read | 3.2: + SC_DELAY_jq=1.5 SC_DELAY_sed=10 | 2 oversize ×5 | 同 |
| V3-E4-cap-3-at-budget-4 | deadline | stall-read | 3.2: + SC_DELAY_sed=10 SECRET_GUARD_TIME_BUDGET_S=4 | 2 oversize ×5 | 同 |
| V3-E5-budget-2 | deadline | stall-read | 3.2: + SC_DELAY_sed=10 SECRET_GUARD_TIME_BUDGET_S=2 | 2 oversize ×5 | 同 |
| V2-E6-flag-from-environment-ignored | deadline | stall-read | 3.2: + SC_DELAY_sed=10 _SG_RELAXED=1 | 2 oversize ×5 | 同 |
| V2-E7-no-time-left | deadline | stall-read | 3.2: + SC_DELAY_jq=3.2 | 2 oversize ×5 | 同 |
| V5-E19-deadline-with-term-ignored | deadline | stall-read (TERM 忽略的包装只加在被测臂) | 3.2: + SC_DELAY_sed=10 | 2 oversize ×5 | 同 |
| V2-E8-ostype-from-environment-ignored | outcome | benign-big | + OSTYPE / MACHTYPE / HOSTTYPE 伪值 (两种平台都传) | 2 oversize ×5 | 同 |
| V2-E9-extension-project | identity | ext-read | + CLAUDE_PROJECT_DIR=<ext> | 2 oversize ×5 | 同 |
| V2-E18-extension-via-stdin-cwd | identity | ext-read-cwd (stdin 带 cwd) | — | 2 oversize ×5 | 同 |
| V9-E10-count-axis-read-blocked | outcome | count-axis | — | 2 oversize ×5 | 同 |
| V9-E11-tmax-in-rerun | outcome | tmax-rerun | — | 2 oversize ×5 | 同 |
| V9-E12-vmax-unchanged | identity | vmax | — | 2 vmax ×5 | 同 |
| V7-E13-multiline-copy-normal-text | outcome | count-axis-ctl | — | 2 oversize ×5 | 同 |
| V7-E14-long-line-from-expansion | outcome | longline-expansion | — | 2 oversize ×5 | 同 |
| V7-E15-credit-as-normal | outcome | multiline-credit | — | 2 oversize ×5 | 同 |
| V1-E16-p1-small-benign / -p1-small-read-filter / -p1-var-mid | identity | 同名形状 | — | 0 none ×5 | 同 |
| V1-E16-p1-small-read / -p1-var-read / -p1-var-mid-read | identity | 同名形状 | — | 2 finding ×5 | 同 |
| V6-S20-segment-fallback-text | fbt (helper) | segment 副本 `cseg` + 两段 | 源入 hook 的 shell 里设 WSL_DISTRO_NAME | 2 oversize (5.0-5.3); 3.2 上该用例是 SKIP [platform], 关门调用不跑 | 同 |
| V6-S21-whole-fallback-text | fbt (helper) | whole 副本 `cwh` | 同上 | 2 oversize (5.0-5.3); 3.2 同上 | 同 |

结论: 每处 59e333c 与实现关门臂逐处相同; **没有因 bash 不同的项**, 也没有因模式 (放宽平台的原调用 vs 3.2 的 identity 回落, 后者多带变量) 不同的项, 所以表按编号一列即可。3.2 上 SC_DELAY_* 在 identity 回落里不起作用 (垫片不在 PATH), 预算 2 / 4 与 `_SG_RELAXED=1` 会到 hook, 实测不改结局。V2-E17 单臂、已判绝对结局, 不在表内。

## 3. 各轮结果与首尾负载 (全部判过)

| 轮 | 结果 | 负载 开 / 尾 (一分钟) | 计时批 |
|---|---|---|---|
| 实现 5.0.18, SG_W10_ONLY=. (worktree) | PASS 136 / FAIL 0 / SKIP 0, [reference] 0 | 1.03 / 1.95 | judged |
| 实现 5.1.16 | 136 / 0 / 0, [reference] 0 | 1.10 / 1.24 | judged |
| 实现 5.2.15 | 136 / 0 / 0, [reference] 0 | 1.18 / 1.21 | judged |
| 实现 5.3.20 | 136 / 0 / 0, [reference] 0 | 1.16 / 1.18 | judged |
| 实现 3.2.57 | PASS 78 / FAIL 0 / SKIP 58 (全是 [platform]), [reference] 0 | 1.18 / 1.71 | judged |
| 整轮, worktree, PATH 上的 bash 5.2.15 (13:48:33-13:54:22) | PASS 961 / 961, FAIL 0, SKIP 0; SC-13 绿; 6 组那行: `relaxed branch (new outcomes) ... | deadline fallback (截止回落) 0 / 10` | W10 批 1.07 / 1.63; 整轮结束时 2.35 | judged |

每轮开跑前等到一分钟负载 < 1.2 (`waitlow`, 每次都在 30 分钟内等到)。

## 4. 坏实现抽查 (mutants.py 从实现 `af4658b6f935` 构造, 写在 `t002e/mut/`; 经改后的 run-suite.sh, PATH bash)

| 坏实现 | 指定用例 | 结果 | 与要求 |
|---|---|---|---|
| BI-8 (`_SGV_VMAX` 4096 -> 8192), hook `ff9f7a43eb7e` | V9-E12 | `FAIL ... hook rc=0 none | gate-closed rc=0 none | stderr IDENTICAL | gate-closed arm rc=0 none, reference (59e333c) rc=2 vmax [reference]` | 由 `[reference]` 抓住, 符合 |
| BI-5, hook `0ac3c4adf007` | V2-G4, V2-E9 | V2-G4 `FAIL status 0 (want 1) [status]`; V2-E9 关门臂 2 oversize = 参照, 走原判定 `FAIL ... stderr DIFFERENT [bytes]` | 与 reasons.tsv (`[status]` / `[bytes]`) 一致 |
| BI-45, hook `7529c4e49cf2` | V6-S20 | 关门调用 `status 2 oversize` = 参照, 走原判定 `FAIL ... 713 bytes vs ... 719 bytes: DIFFERENT [bytes]` | 与 reasons.tsv (`[bytes]`) 一致 |
| 实现 | 同上 4 个用例 | 全 PASS | 符合 |

## 5. 两个构造 (只在 run-suite.sh 的副本里做: hook 副本经 run-suite.sh 换进临时目录, worktree 不动)

- C1 `_sg_relax_ok` 首行加 `return 1` (准入门恒关), hook `93c7f2fac02a`, 14:02:02-14:06:37 (负载 1.16 -> 4.56): **6 组全部 FAIL** (21ab、21ac、21ag、21aj、21al、21ao 各一条 FAIL)。但 Summary 显示 `deadline fallback (截止回落) 1 / 10 (21ab)`: 21ab 的「f=x; echo $f + 9000 字符填充」那条在准入门关着时墙钟也 >= 2.85 s, 同一份输出满足基线支断言, 被记成截止回落; 21ab 仍 FAIL, 是靠它另两条 (`wpa_vx_cmd 159` 墙钟 0.69 s、4500 个「 a」那条 2.60 s)。其余各组触发点命令的墙钟: 21ac 0.34、21ag 1.10、21aj 0.62 / 1.02 / 1.62、21al 0.30、21ao 0.35 s。任务书要求的组级结果 (各组都须 FAIL) 成立; 「触发点命令立刻得到基线拦截、墙钟 < 2.85 s」对 10 条里的 1 条**不成立** (见第 6 节第 1 条)。
- C2 `_sg_relax_job` 里计时器起来之后、判定之前加 `sleep 4` (放宽重跑拖过截止), hook `f76baeb0e1c8`, 14:09:57-14:16:50 (负载 1.16 -> 5.66): **6 组全部 PASS**, `deadline fallback (截止回落) 10 / 10 (21ab 21ab 21ab 21ac 21ag 21aj 21aj 21aj 21al 21ao)`, 截止回落数 = 触发点命令数, 符合要求。
- 两轮的其他红在预期内: 副本不是 git 检出, SC-13 在副本里红 (run-suite.sh 头注释已写明); C1 另有 W10 移植批的放宽类用例变红 (共 25 FAIL); C2 只有 SC-13 一条 FAIL, W10 计时批因结束负载 2.53 记 29 个 SKIP [void]。

## 6. 未做或拿不准的项 (请主控复议)

1. **2.85 s 下界分不开「准入门关、立刻基线拦截」与「截止回落」, 当基线那一遍本身就要 >= 2.85 s 时** (C1 实测: 21ab 的 9000 字符填充那条; probe.txt 里同类命令关门时 2.39-3.08 s)。21ab 有三条触发点命令, 这次另两条照样红, 所以组级仍抓得住; 但一个只对这类慢命令关门的坏实现, 能借截止回落让那条命令通过。判法是主控定的, 我没改。可能的补法 (供参考, 未做): 截止回落另要求一个只在走截止路径时才有的正向迹象, 或把下界改成按 hook 内 `_SG_P0` 计算的截止时刻。
2. fbt 不符参照时, 若关门调用出现时间文案, 我按计时类记 `TIMED ok bad ... [time-text]` (任务书写「helper 的 fbt 同样加 [reference]」, 我理解「同样」包括计时例外; fbt 没有 12 s 超时)。若主控要求 fbt 一律记 `[reference]`, 删掉那一支即可。
3. 行为变化 (按任务书字面): identity 里两臂**都**出现时间文案时, 以前逐字节相同即 PASS, 现在关门臂对不上参照 (`2 oversize`), 按计时类处理 (未判批 SKIP [load], 已判批记 FAIL)。负载低时不会发生, 本次各轮都没出现。
4. 参照表按编号查表、不分 bash 与模式, 依据是第 2 节实测在 5 个 bash 与两种模式下全同; 日后若某处因 bash 而不同, 需要改成按 bash 分开的表。表里没有的编号记 `unrecorded`, 走 `FAIL [reference]` (失败即关)。
5. reasons.tsv 里 BI-8 / V9-E12 仍是 `[bytes]`; 按计划 notes, 套件模式要在列 `[bytes]` 的这些用例上另认 `[reference]`, 那是 3d 的 run-mutants.sh 套件模式, 本段未做。
6. 全部坏实现与扰动、两种环境错误、基线红集在套件上复跑、导出 WSL 变量的整轮: 3d 与主控最终整轮, 本段未做。
7. C1 / C2 两轮跑的过程中负载升到 4.56 / 5.66 (套件自身占满 2 核, 外加主机上其他会话); 6 组没有负载门, 构造的墙钟是在这个负载下量的。C1 那一条越过 2.85 s 与负载有关, 低负载下可能不越过。
