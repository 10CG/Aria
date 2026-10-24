# TASK-003 第一段 预测（阶段 2，写在上机之前）

冻结物：`w14-mutants.py` 与 `list.md` 的 sha256 已在 `FROZEN.sha` 记下（4327121c903c43995e1b84fe62608d03ea92b398c3663989b749a9529853a5e4 / 1cfb36dd3819c3cd2198eff4984a068e1a0376269c546cf1a6cd55e75b388361），之后未再改。
阶段 2 读过的范围（只这些）：套件 `hooks/tests/secret-guard.test.sh` 的 W10 移植块块首注释（`:136-195`，含原因标签 `[reference]` 的说明与各组用例编号清单）与 `sg_w10_cases` 的调用行（`:359-436`，没读 `sg_w10_identity/deadline/outcome` 等断言函数体）；helper `hooks/tests/lib/secret-guard-w10-direct.sh` 的头注释（`:1-24`，含原因标签清单）与用例编号行（grep 到的行，每行只看前 120-170 字符）。
原因标签（helper 头注释）：[status] [rc] [stderr] [bytes] [value] [kind] [text] [count] [judged] [leftover] [wall<lo] [wall>hi] [fallback] [reference]；套件另有 [platform] [load] [void] [inconclusive] [root] 的 SKIP 与 [missing] [setup]。
表的格式：用例列空格分隔（`-` = 预计无用例能抓，即缺口）；标签列用 `/` 分隔备选（我对个别标签只能猜，没读断言体，写了备选）；确信度：高 = 用例名与断言意图直接对着这处错误；中 = 靠用例名推断；低 = 猜。

| 编号 | 预计抓住的用例 | 预计的原因标签 | 确信度与理由 |
|---|---|---|---|
| Q-1 | V2-G2-platform:x86_64-pc-linux-gnu:5.3 | [status]/[value] | 高。名字就是 5.3 被放行的平台行；变异把 5.3 挡掉 |
| Q-2 | V2-G2-platform:x86_64-pc-linux-gnu:6.0 | [status]/[value] | 高。清单里有 6.0 一行；变异把 6.0（minor 0）放行 |
| Q-3 | V2-G2-platform:x86_64-alpine-linux-musl:5.2 | [status]/[value] | 高。musl 串 x86_64-alpine-linux-musl 会被 x86_64-*-linux-* 匹配 |
| Q-4 | V2-G2-platform:x86_64-pc-linux-gnu:5.2:osrelease-wsl2-2020 | [status]/[value] | 中。假定 2020 年 WSL2 内核串是小写 microsoft 且不含 WSL（4.19.x-microsoft-standard）；若该用例用的串含 WSL，则无用例能抓（缺口） |
| Q-5 | V2-G3b-gate-uses-build-facts V2-E8-ostype-from-environment-ignored | [value]/[status]/[bytes] | 中。G3b 的说明里点名 OSTYPE、MACHTYPE；E8 在 x86_64 上导出 MACHTYPE=x86_64-apple-darwin23.0.0，变异读它则准入门关闭，benign-big 由放行变拦 |
| Q-6 | V2-G4-project-without-extension-file V2-G15-cwd-project-without-extension-file | [status] | 高。「有项目根、没有扩展文件」应放宽，变异下永不放宽 |
| Q-7 | V2-G12-segment-trigger-asks-gate | [status]/[value]/[judged] | 中。名字是「分段触发点会问准入门」；标签只能猜 |
| Q-8 | V2-G4-extension-path-is-a-directory | [status] | 高。目录态应当关闭，变异下 -f 为假而放宽 |
| Q-9 | V8-D3-growth-8193-plain V8-D3-growth-8193-braced | [status]/[rc]/[value] | 中高。D2/D3 的夹具是 a=…; b=…; : $a $a $b，两个变量累计增长恰 8193，应拦；变异下第二个变量的限随第一个的增长上移，放行 |
| Q-10 | V9-C3-for-statements-rerun | [count]/[value] | 高。直调 _sg_vx_collect 数 12 条 for，变异只收 8 |
| Q-11 | V9-C2-references-rerun-cb12 | [value] | 高。cb12 = 大括号拼写，12 个引用，走 _sg_vx_replace；变异后剩余引用未展开 |
| Q-12 | V9-C2-references-rerun-c12 | [value] | 高。c12 = 普通拼写，走 _sg_vx_apply 的 $NAME 循环 |
| Q-13 | V7-N11-lmax-edge-normal | [rc]/[kind]/[status] | 中高。最长行恰为 LMAX 应走普通判定；变异走 nocredit |
| Q-14 | V7-N10-blank-padded-long-line | [rc]/[kind]/[status] | 高。名字就是空白填充的长行 |
| Q-15 | V7-E14-long-line-from-expansion | [kind]/[wall>hi] | 低。变异只改顺序，结论仍是拦；只有长行大到 credit 在截止前算不完（回落成 oversize）或墙钟越界才红；夹具大小我不知道，可能是缺口 |
| Q-16 | V3-E3-anchor-at-hook-start | [wall>hi] | 中高。jq 垫片先拖 1.5 s，截止应在 hook 启动 + 3 s；变异的计时器从作业启动再睡 3 s。计时类，负载 >= 2 时 SKIP [load] |
| Q-17 | V6-E2-deadline-fallback-bytes V6-S20-segment-fallback-text | [bytes] | 中。依赖 bash 在被杀的作业上往 stderr 写「Killed」通报；若 bash 不写，则这条变异在这些用例上等价（缺口） |
| Q-18 | V4-S19-block-text-bytes | [bytes] | 高。名字与断言说明都是字节与最后一个字节 |
| Q-19 | V5-S13b-nothing-outlives-the-run V5-S9-child-left-behind | [leftover]/[wall>hi] | 中高。S13b 数 _sg_relax_run 返回 1 s 后还活着的子进程；S9 的子进程持有管道 |
| Q-20 | V6-S20-segment-fallback-text | [bytes]/[text]/[fallback] | 高。分段回落文案与关闭准入门时的基线块比字节 |
| Q-21 | V8-D5-growth-text-segment | [text] | 高。逐字比分段 growth 文案 |
| Q-22 | - | 缺口 | 中。longline 路径上只有 [kind]（有 has a line longer than 的文案种类）和返回码被检；V11-S5/S6/S7 直调 _sg_emit_blocked，不经 _sg_judge_one 的调用点，所以 pat 与 seg 对调看不到 |
| Q-23 | V11-S7-longline-text-verbatim | [text] | 低。整份文案与 What 5 逐字比；若直调时 seg 与 command 是同一个串，则变异不可见（缺口） |
| Q-24 | V3-E3-anchor-at-hook-start | [wall>hi] | 中高。名字就是「锚点在 hook 启动」；jq 垫片拖慢首遍。计时类 |
| Q-25 | V2-G11-flag-not-from-environment V2-E6-flag-from-environment-ignored | [value]/[bytes]/[wall>hi] | 高。两条都点名「标志不取自环境」；E6 带 _SG_RELAXED=1 跑 stall-read |
| Q-26 | V3-G10-cap-3 V3-E5-budget-2 V3-E4-cap-3-at-budget-4 | [value]/[wall>hi] | 高。G10 直测预算 4 时剩余 <= 3.0；E5 预算 2 的截止 1.85-2.6 s |
| Q-27 | V3-G12-time-left-zero-padded | [value]/[status] | 高。断言是 "0 2.050000" |
| Q-28 | V3-G9-clock-backwards | [value]/[status] | 高。锚点在 5 s 之后的时钟，剩余应 <= 1 |
| Q-29 | V6-E2-deadline-fallback-bytes V6-S20-segment-fallback-text V6-S21-whole-fallback-text | [status]/[rc]/[fallback] | 高。任何经 _sg_per_segment_eval 的回落都会漏出状态 4 |
| Q-30 | V2-G6-no-time-left V2-G7-no-anchor V2-G8-budget-0 | [status] | 高。直调准入门，无剩余时间 / 无锚点 / 预算 0 都应返回 1；变异返回 0 |
| Q-31 | - | 缺口 | 中高。GMAX 与 SMAX 同为 8192，夹具没有改常量的探针；我预计没有用例能区分 |

## 预测小结

- 预计无用例能抓（缺口）：Q-22、Q-31；预计可能是缺口（低确信度）：Q-15、Q-23、Q-4、Q-17。
- 计时类（负载 >= 2 时 SKIP [load]，需低负载重跑）：Q-15、Q-16、Q-19（S9）、Q-24、Q-26（E4、E5）。
- 其余按用例名与断言意图直接对应，预计一次抓住。
