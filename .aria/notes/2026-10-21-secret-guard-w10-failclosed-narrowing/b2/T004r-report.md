# TASK-004 重跑段 4r（第三次派出）执行席报告 — 10CG/aria-plugin#217

- 对象: aria worktree b1d3111, hook sha256 628652570ce3 (拷贝 t004r/impl-hook.sh, 前缀已核); 基线 59e333c / e83c5e30f2cc (run-evidence.sh 自取自断言); 原型 mkv31.py 生成 9f61db0e7b8b; 上一版实现 af4658b6f935 (aria 2893bcc, 即 HEAD 里 v31/impl 的证据, 已取到 t004r/prev/); 原型那一轮 95cf1de7 (t004r/p95/)。
- 预期先写: t004r/PREDICT-4r3.md (10:07 UTC, 看任何结果之前)。
- 语料: TRAFFIC_DIR 按 evidence/W0-corpus-manifest.tsv 核 2412 / 2412 (字节数与 sha256 全对, 缺 0), 无需补。全程未读、未打印任何命令文本; replay 临时目录 (TMPDIR=scratchpad/tmp-t004r-w12) 结束后为空。
- 执行方式: 后台驱动逐阶段串行, 每次尝试前等一分钟负载 < 1.2, 命令全部 taskset -c 0,1 nice -n 19; 每次尝试写进 t004r/so/<阶段>.<次>/, 只有有效的才拷进 v31/impl (run-evidence.sh 的 OUT 指向该次的目录; W8 / W11 / W9 拆成三次调用以便逐阶段把门, 输出与一次调用相同)。未改任何脚本、hook、套件; 未 commit。

## 1. 各阶段首尾负载 (/proc/loadavg 1/5/15 分钟; INV-7 只看一分钟读数)

| 阶段 | 次 | 开始 UTC | 首 | 尾 | 结论 |
|---|---|---|---|---|---|
| W8 | 1 | 10:05:23 | 0.73 0.91 1.14 | 0.73 0.91 1.14 | 有效 (非计时) |
| W11 | 1 | 10:05:24 | 0.73 0.91 1.14 | 1.02 0.97 1.15 | 有效 |
| W9 | 1 | 10:05:44 | 1.02 0.97 1.15 | 2.41 2.00 1.58 | 作废 |
| W9 | 2 | 10:14:12 | 1.17 1.71 1.51 | 3.43 2.57 1.96 | 作废 |
| W9 | 3 | 10:23:36 | 1.19 2.02 1.83 | 2.58 2.26 2.01 | 作废 |
| W13 (MUT_SCOPE=full) | 1 | 10:32:41 | 1.18 1.90 1.91 | 1.14 1.19 1.19 | 首尾有效; 段内 BI-14 尾 / BI-15 首读数 2.47 -> 两个 NOT-JUDGED, 见 3.4 |
| P-0 v31 模式 | 1 | 11:32:39 | 1.14 1.19 1.19 | 1.06 1.16 1.18 | 有效, 已判定 |
| P-0 套件模式 | 1 | 11:33:30 | 1.06 1.16 1.18 | 1.21 1.18 1.19 | 有效, 已判定 |
| 套件模式坏实现 | 1 | 11:34:27 | 1.19 1.18 1.19 | 1.57 1.57 1.35 | 首尾 < 2, 但段内逐个读数到 2.80, 33 轮未判定 -> 按主控补充规则作废 |
| W12 | 1 | 11:38:16 | 1.11 1.46 1.32 | 2.01 1.89 1.59 | 作废 |
| W12 | 2 | 11:47:20 | 1.19 1.69 1.53 | 2.33 2.19 1.85 | 作废 |
| W12 | 3 | 11:57:10 | 1.10 1.82 1.75 | 4.77 3.37 2.55 | 作废 |
| W14 独立坏实现 (w14.sh) | 1 | 12:15:33 | 1.15 1.79 2.09 | 1.19 1.63 2.00 | 有效, 31 轮全判定 |
| W14 耗时矩阵 (w14-matrix.sh full) | 1 | 12:17:03 | 1.19 1.63 2.00 | — | 约 13:04 由我按 PID 停掉 (130 / 236), 见 3.9 |
| W12 (第 4 次) | 1 | 13:06:50 | 1.17 2.15 2.59 | 1.97 2.06 2.37 | 有效 |
| BI-14/15 重跑 | 1 | 13:17:14 | 1.14 1.74 2.22 | 1.10 1.54 2.09 | 有效, 已判定 |
| 套件模式坏实现重跑 | 1 | 13:19:01 | 1.10 1.54 2.09 | 1.50 1.60 2.01 | 未判定 -> 作废 |
| 套件模式坏实现重跑 | 2 | 13:22:51 | 1.12 1.50 1.96 | 1.63 1.68 1.95 | 未判定 -> 作废 |
| W9 (第 4 次) | 1 | 13:26:55 | 1.12 1.55 1.90 | 2.01 1.94 1.95 | 作废 |

(机读: t004r/phases.tsv 10:05 之后的行与 t004r/driver.log 10:05 之后的行; 两个文件里更早的行是前两次 4r 派出留下的, 不是本次。)
负载来源: 宿主机 5 分钟负载在 12:50-13:00 一度到 3.94; 抽查 top 时只有本席的被测进程占 CPU, 其余负载来源无法归因。W9 与 W12 在两核上本身就把一分钟负载推到 2 上下 (四次 W9 尾读数 2.01-3.43)。

## 2. 主控补充核对: 计时批是否被判 (逐轮)

- W13 的 sc-cases.sh 六轮 (5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 / 3.2.57 与基线): 页脚 6 行全是 "timing batch: judged"; 汇总 SKIP 0 (load 0, void 0, inconclusive 0, root 0)。
- W13 第 3 节 run-mutants.sh: "# 55 caught, 0 missed, 0 wrong reason, 2 not judged, 0 setup (of 57)" -> BI-14 (V3-E4-cap-3-at-budget-4=skip[void], 读数 1.34 -> 2.47, "timing batch: void (SKIP [void]): run again") 与 BI-15 (V5-S9-child-left-behind=skip[load], 读数 2.47 -> 1.73, "timing batch: SKIP [load]")。重跑 (MUT_SCOPE=full, MUT_ONLY 两个编号, v31 模式): "# 2 caught, 0 missed, 0 wrong reason, 0 not judged, 0 setup (of 2)", 两行都是 "timing batch: judged"。其余 55 行全是 judged。
- P-0 v31 模式: "# totals: PASS 161  FAIL 0  MISSING 0  SETUP 0  SKIP 0 (load 0, void 0, inconclusive 0, root 0)", "timing batch: judged"。
- P-0 套件模式: 套件汇总行 1 行, "timing batch: judged"; suite exit 0。
- 套件模式坏实现 (64 轮, 每轮一份套件输出): 第一轮 judged 31 / SKIP [load] 32 (BI-23 至 BI-54) / void 1, P-0 NOT-JUDGED ("SKIP other than [platform]: V4-S1-allow V4-S2-block-with-text …"); 重跑 1: judged 52 / SKIP [load] 11 / void 1, P-0 不符 1; 重跑 2: judged 50 / SKIP [load] 13 / void 1, P-0 GREEN。三轮都不满足补充规则, 全部作废。
- W14 独立坏实现: 31 份套件输出的汇总行全是 "timing batch: judged"; 页尾 "not judged 0"。
- 逐行原文 (每轮一行, 只含编号、计数与文案种类) 在 t004r/so/<阶段>.<次>/work/*.txt 与 t004r/so/W14i.1/w14dir/ 里, 可用 grep 'W10 ported cases' 取出。

## 3. 对照结果 (预期见 PREDICT-4r3.md; 不一致处另列第 4 节)

### 3.1 W8 (验收 1) — 成立
- v31/impl/W8-v31.diff 页眉: hook 628652570ce3, base e83c5e30f2cc, sc-cases.sh 54f6038db77d, sc-direct.sh 1572616e5262, mutants.py 9e832c0f7bfa, load 0.73。正文打到基线上得 628652570ce3 (patch 核对)。基线 -> 实现 19 个 hunk, +218 / -56 (上一版 19 个, +199 / -56)。
- 原型 (9f61db0e7b8b) -> 实现: 8 个 hunk, +58 / -30, 逐 hunk 归类 (每个新增行都在 proposal 对应节的正文里逐字找到; 机械比对脚本 t004r/w8cls.py, 逐行结果 t004r/w8cls-proto-impl.txt):
  1. @@ -85,18 +85,30 @@ +24 -12: (3) What 7 补充 12 行 + (5) What 7 补充 2 12 行 (头注释)
  2. @@ -575,7 +587,8 @@ +2 -1: (3) What 7 补充
  3. @@ -589,9 +602,10 @@ +4 -3: (5) What 7 补充 2
  4. @@ -623,8 +637,8 @@ +2 -2: (3) What 7 补充
  5. @@ -672,7 +686,6 @@ +0 -1: (2) What 6 (删 :666 那一行)
  6. @@ -711,10 +724,10 @@ +4 -4: (5) What 7 补充 2
  7. @@ -783,14 +796,16 @@ +5 -3: What 7 补充的那一处被 What 7 补充 2 改写, 新增 5 行全在 What 7 补充 2 里 -> (3)+(5)
  8. @@ -812,14 +827,27 @@ +17 -4: (1) What 1 补充 5 行 + (4) What 1 补充 2 10 行 (同时出现在 What 7 补充 2 的逐字文本里) + (5) 1 行注释 + 1 行通用行 (右花括号一类)
- 上一版 (af4658b6f935) -> 实现: 5 个 hunk, +37 / -18, 新增行只在 What 1 补充 2 与 What 7 补充 2 里 -> 只有 (4)(5) 两类, 与预期一致 (t004r/w8cls-prev-impl.txt)。
- 说明: 比对是行级逐字子串匹配 (行内容出现在该节正文里), 不是语义核对; 第 1 个 hunk 删掉的 12 行原型注释在 proposal 里找不到 (proposal 的参考实现只列逻辑 hunk), 删除行由原型的 sha 9f61db0e7b8b 担保。

### 3.2 W11 (验收 4) — 成立
- 18 个结局 (规范化后 24 行) 的 rc 与文案种类与上一版、与 95cf1de7 都逐行相同, 差异只在页眉与墙钟。首尾 0.73 / 1.02。

### 3.3 W9 (验收 3) — 本次没有有效轮
- 四次尝试都因尾读数 >= 2 作废 (2.41 / 3.43 / 2.58 / 2.01)。四次的内容 (去掉页眉、屏蔽小数) 都与上一版逐行相同: 基线 813 / 814 (1 FAIL, SC-13 非 git 副本), 实现 807 / 814 (7 FAIL: SC-13 与六组); 与 95cf1de7 只差 SC-21ab 那 3 处检查 (exit code want 2 got 0 / names the limit / says to split), 与第一段主控的负载解释相同。
- v31/impl/W9-suite.txt 未替换, 仍是上一版 (af4658b6f935) 的那份。
- INV-7: 连续 4 次 (前 3 次连续) 取不到首尾都 < 2 的结果, 按规定附读数上报; 未放宽判据。

### 3.4 W13 (验收 2) — 基本成立, 新增编号的数目与任务书不符
- 第 1 节: 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 各 PASS 161, FAIL 0, MISSING 0, SETUP 0, SKIP 0, relaxation expected yes; 3.2.57 PASS 93, 全 0, relaxation expected no。上一版 142 / 79。
- 第 2 节: 基线红集 43、绿集 25 与上一版逐编号相同; MISSING 93 (上一版 74)。W13-sc-base.txt (那一轮基线原始输出, 首行记全部 sha) 与上一版比: 原有 142 个编号状态 0 处变化; 新增 19 个编号, 在基线上全是 MISSING: V11-S1-above-gate:_sg_relax_nowslfs、V15-T1-timer-sleeps-time-left、V15-T2-anchor-taken-once-at-hook-start、V15-T3-job-errors-silenced、V15-W1a 至 V15-W1o (15 条)。与 95cf1de7 的关系同上一版 (旧编号逐个不变, 这次没有另做 95cf1de7 的逐栏比对)。
- 第 3 节 (MUT_SCOPE=full): 55 CAUGHT + 2 NOT-JUDGED (BI-14、BI-15, 负载, 见第 2 节), 0 missed / wrong reason / setup; P-0 GREEN (PASS 161); 扰动轮 0 个不符。其余编号的判定与指定用例状态与上一版逐项相同。"其他红"与上一版比: 旧编号无增减; 只多了新编号: BI-6 +V15-W1m、BI-22 +V15-W1m、BI-13 +V15-T2。
- BI-14 / BI-15 低负载重跑 (补充证据 v31/impl/W13-rerun-BI-14-15.txt, 新文件): 都 CAUGHT, 指定用例 V3-G10-cap-3=red V3-E4-cap-3-at-budget-4=red / V5-S9-child-left-behind=red V5-S13b-nothing-outlives-the-run=red, 与上一版相同; 两者的"其他红"与上一版逐个相同。
- P-0 单跑: v31 模式 GREEN (PASS 161, judged); 套件模式 GREEN (judged)。上一版 v31 模式 PASS 142。
- 套件模式坏实现: 三轮的 57 个判定都是 CAUGHT, 指定用例状态与上一版逐项相同; 但三轮都有 SKIP [load] / void, 按主控补充规则作废。第一轮的文件曾拷进 v31/impl (当时补充规则未到), 收到规则后已用 HEAD 版复原 (该轮原样留在 t004r/so/Msuite.1/)。v31/impl/W13-suite-mutants.txt 现在仍是上一版的。

### 3.5 W12 (验收 5、6) — 成立 (第 4 次尝试有效)
- 页眉 hook 628652570ce3; 首 1.17 / 尾 1.97。
- 第 1 节: allow 136 / growth 1 / oversize 1; W1 类 size -> allow 136, size -> growth 1, value -> oversize 1; 越界 0 / 138; 逐编号的 rc、文案种类、是否进入重跑与上一版 0 处不同, 基线回放 138 条也 0 处不同。SMAX 类 137 条放行 136 (与原型那一轮相同, 没有少掉的); VMAX 那 1 条照旧拦; 没进重跑的 1 条与基线逐字节相同 (1 / 1)。
- 1b 延迟代价 (如实): 进入重跑并放行 n=136, 比基线多等 p50 0.287 s、p90 0.703 s、max 1.856 s (上一版 0.272 / 0.638 / 1.771); 进入重跑后回落成基线尺寸文案 0 条; 其他结局 1 条 (growth, 编号与上一版相同); 138 条的逐字节比对 identical=1 different=137 (与上一版相同)。三次作废轮的同一行: p50 0.257 / 0.282 / 0.305, p90 0.541 / 0.620 / 0.576, max 1.026 / 1.473 / 1.159 (只作参考)。
- 第 2 节 identical=300 different=0; 第 3 节 identical=40 different=0。
- 前三次作废轮的逐编号结局也与上一版 0 处不同 (第 3 次尾读数 4.77 时 ident 一遍有 4 条与基线相同, 负载使然, 该轮作废)。

### 3.6 W14 独立坏实现 (TASK-003 验收 1) — 成立
- 页眉 impl 628652570ce3, suite 2f5cc04cf8d2, helper 28b0788a0a6c, w14-mutants.py 9e34b75b9d04, predict.md 627580356dcd (与上一版同一份)。31 个: 26 按预期抓住 + 5 由补的用例抓住, caught elsewhere 0, not judged 0, NOT CAUGHT 0。逐个判定与预测、实测栏与上一版完全相同。W14_DIR 设在 t004r/so/W14i.1/w14dir (没有动 t003a), predict.md 与 gapmap.tsv 取自 t003a。

### 3.7 W14 耗时矩阵 (TASK-003 验收 2) — 未完成
- 跑到 130 / 236 个有效结局 (另有 145 行因负载作废重跑) 时, 为给 W12 与重跑让出机器、并守住调用上限, 我按自己记下的进程组号停掉了它; v31/impl/W14-timing-matrix.txt 仍是上一版的。
- 已有的 130 个结局 (t004r/so/W14m.1/w14m/rows.tsv): 越界 0; 进入重跑的最大墙钟 3.060 s (上一版也是 3.060 s); 没进入重跑而墙钟 > 3 s 的 5 个 (属上一版已记的基线首遍既有缺口 10CG/aria-plugin#228 一类); 进程残留 0。这是部分结果, 不能当验收。

## 4. 与预期不符之处 (逐条)
1. 新增编号: 任务书写套件与 sc-cases 多了 V15-W1f 至 W1o 十条; 与 v31/impl 里的上一版证据 (af4658b6f935) 比, 实际多了 19 条 (另有 V15-W1a 至 W1e、V15-T1 至 T3、V11-S1-above-gate:_sg_relax_nowslfs 九条, 推测来自修复轮第一段 710a36d, 未核实)。按旧编号逐项比的结论不受影响, 新编号单列。
2. W13 第 3 节有 2 个 NOT-JUDGED (预期 0), 低负载重跑后判定为 CAUGHT。
3. 套件模式坏实现: 判定与上一版相同, 但三轮计时批都没判全 (上一版 64 轮全 judged), 没有可用的一轮。
4. W9: 预期有效; 四次都作废 (内容与上一版相同)。
5. W12 的 1b: p90 比上一版多 65 ms、max 多 85 ms, 比预期的"几毫秒到几十毫秒"略大; 其余与预期一致。
6. 耗时矩阵没跑完。
- 其余 (W8 五类、W11、W12 结局、W14 独立坏实现、P-0) 与预期一致。

## 5. 未做或拿不准的项 (请主控裁)
1. W9 与补充规则: 59e333c 的旧套件没有 "W10 ported cases … timing batch" 那一行。若补充规则第 1 条也适用于 W9 ("缺这一行"即作废), W9 永远不会有效; 若只适用于移植后的套件, W9 只按 INV-7 首尾负载判。我没有选, W9 第 4 次的输出只留在 t004r/so/W9r.1/ (反正它也因尾读数 2.01 作废)。另: W9 在两核上本身就把负载推到 2 以上, 四次尾读数 2.01-3.43, 照现行判据很难取得有效轮。
2. 补充规则第 2 条的重跑单位: 我只重跑了未判定的两个坏实现 (run-mutants.sh 自己的 "run it again" 做法), 没有重跑整轮 W13 (约 1 小时)。若要整轮重跑, 请另派。补充证据的文件名 W13-rerun-BI-14-15.txt 是我起的, 可改可弃。
3. 主控规则的作用对象: 套件模式第一轮在阶段首尾都 < 2, 是段内逐个读数到 2.80; 按补充规则作废, 已把 v31/impl 里那份复原成 HEAD 版。
4. 未完成, 需要另找低负载时段: W9 (验收 3)、套件模式坏实现 (W13-suite-mutants.txt)、耗时矩阵 (W14-timing-matrix.txt)。这三份在 v31/impl 里仍是上一版 (af4658b6f935) 的, 按 INV-8 不能用。
5. INV-7 的三次规则: W9 连续 4 次、套件模式在补充规则下连续 3 次没取到有效轮, 按规定附读数上报 owner (读数见第 1 节)。W12 前三次作废、第 4 次有效; 第 4 次是否合乎"连续 3 次即上报"的本意, 请主控确认。

## 6. 进程、文件与纪律
- v31/impl 现状 (git status): 修改 W8-v31.diff、W11-adversarial.txt、W12-real-traffic.txt、W12-replay-138.tsv、W12-replay-138-base.tsv、W12-ident-138.txt、W13-sc-cases.txt、W13-sc-base.txt、W13-P0-v31.txt、W13-P0-suite.txt、W14-independent-mutants.txt; 新增 W13-rerun-BI-14-15.txt; 未变 W9-suite.txt、W13-suite-mutants.txt、W14-timing-matrix.txt。
- 进程: 只按自己记下的 PID 停过三次: driver2 (3916765, 尚在等待, 未跑任何东西)、driver2b (4043097, 同上)、driver.sh 的进程组 3266708 (在跑耗时矩阵); 停后按工作目录扫描无残留。收尾时 driver3 已自行结束, 没有本席的进程在跑。
- t004r 里原有前两次 4r 的材料 (driver.log 与 phases.tsv 的早期行、ev-*、wd、compare.py、PREDICT.md 等), 本席没有动; prev/、p95/、proto.sh、impl-hook.sh、work-base.sh、prev-2893bcc.sh 这几个同名文件被本席重新生成过。
- 驱动起初把 setsid 的 PID 记成了驱动 PID (3266706), 发现后改为 3266708; 没有影响任何运行。
- 过程材料: /tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t004r/ (驱动 driver*.sh、日志、so/ 各次尝试、比对脚本与结果); 不含命令文本。
