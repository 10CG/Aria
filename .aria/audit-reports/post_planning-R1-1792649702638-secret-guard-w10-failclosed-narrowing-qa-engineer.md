---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T06:47:41.084Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 / qa-engineer 席 / secret-guard-w10-failclosed-narrowing

## 审计结论

### 0. 范围与可信度（先读这一节）

侧重：验收能否证伪（TASK-003、TASK-004）、SC 与 BI 的对应、时延判据在共享宿主上的稳定性。

**已实测**（全部在基线或「好原型」上，没有对任何坏实现跑过）：

1. 原型可复现：`python3 v3/mkv3.py <基线 hook> v3.sh` 生成的 diff 正文与 `v3/W8-v3.diff` 逐行一致；基线 sha256 `e83c5e30f2cc`、原型 `3eb4389103e8` 与证据页眉相符。
2. 在 scratch 拷贝里重跑 `run-w10-w11.sh`（该脚本把结果写到脚本同目录，原地跑会覆盖仓内证据，所以必须用拷贝）：S1–S8、G1–G8 全部 PASS，残留进程 0；W11 矩阵与已提交版一致（f5like 3.02 s 回落、apply-heavy-cjk 3.04 s 回落、21ab#2 与 #3 放行）。
3. `commentsync.py`：baseline 模式在基线上 GREEN；target 模式在基线上 RED(24)；对「原型 hook + 未改套件」跑 target 为 RED(22)。
4. 埋点版原型的阶段时间线（`mkdbg.py`），以及首遍耗时随命令长度的曲线。
5. 在好原型上按 SC 描述的形态各写了一份判据并跑通（不是坏实现）：SC-V7 的四个形状加多行大副本加良性大命令；SC-V10 的直调与 e2e；SC-V8 在 `_SG_RELAXED=1` 下直调 `_sg_vx_apply` 的 8 条；注入成本的 SC-V3 形状。全部 PASS，说明这些形态本身可运行、不是空判据。
6. 若干桩场景在参考实现上的行为（见 F12）；hook 闭包里没有后台启动的静态检查；standards 三处计数与套件头注释的比对；`rule6_note` 对照 SOT 与 WP-A 先例。

**纸面推演，未对坏实现实测**：下表与 F1、F4–F7、F11 里关于「某个 BI 能否被某条 SC 抓住」的结论。我本想对原型副本构造 3–4 个坏实现并跑 SC 描述的形态，这一步的一轮输出被安全分类器拦下，没有执行完；我没有重做，所以**本报告没有任何坏实现的实测数据**。涉及这类结论的 finding 都标了 type=risk 或「未对坏实现实测」，请 TASK-003 那一步（或另一席）用独立构造的坏实现来证实或推翻。scratch 目录里另有若干未用于任何结论的草稿文件，其内容不采信。

**未核实**：bash 3.2.57 下的套件；`run-w9.sh`、`run-w12*.sh`（按任务书不跑，语料也不读）；人造负载下的时延分布（避免干扰另一席的计时，改用已提交证据的负载页眉与我自己的空闲机重跑对比）；Forgejo 对跨仓关闭关键词的语义。

**无异议项**（核对过，不需要改）：

- 依赖顺序合理：TASK-003 与 TASK-005 只依赖 TASK-002，TASK-004 依赖 002 与 003，TASK-006 依赖 004 与 005；owner 门放在 TASK-006，验收第一条就是「owner 授权」。
- INV-4（新函数在 source 闸门之上）有现成的机械守卫：套件 SC-30b 的闭包是从 hook 文本推导的（`sc30_closure.awk`，「derived, never listed」），新增函数会被自动覆盖，放到闸门下面会红。TASK-002 验收第三条可证伪。
- P3 的公式与代码一致；W10 的 S1–S8 与 G1–G8 对 P2、P4 以及 P5 的一部分（桩形 A，见 F12）给出了可证伪的单测。

### SC 与 BI 对照（纸面推演；「两人写出等价用例」指两个独立执笔者按 SC 文字写出等价用例的可能性）

| BI | SC | 判断 | 两人写出等价用例 | 备注 |
|---|---|---|---|---|
| BI-1 | V4 | 足够 | 高 | 参考实现通过同形桩（W10 S6），4 种桩形写得清楚 |
| BI-2 | V5 | 条件成立 | 中 | 须钉桩形，见 F12 |
| BI-3 | V5 | 条件成立 | 中 | 变异法要求候选里能定位「计时器那一行」；桩须让作业长时间占用 |
| BI-4 | V3 直调 | 足够 | 高 | 桩睡过截止，进程内实现必超 1.3 s |
| BI-5 | V2 e2e | 足够 | 高 | km-ext 形状，参考实现在扩展项目里 rc=2（W11，我复跑一致） |
| BI-6 | V2 直调 | 足够 | 高 | G2、G3 |
| BI-7 | V6 | **缺口** | 低 | F5：回落的输入没有确定性来源，且回落与「门没开」字节相同 |
| BI-8 | V1、V9 | VMAX 部分足够（21ad）；V9 的 TMAX 没有对应 BI | 低 | F7 |
| BI-9 | V8 | **缺口** | 低 | F4：方向未钉；e2e 形状天生对负载脆弱 |
| BI-10 | V7 | 足够（按构造推演） | 高 | 四个形状的原命令最长行都不到 4.3 KB，副本才超 8192 |
| BI-11 | V10 | **缺口** | 中 | F6：直调 `_sg_judge_one` 够不到 `_sg_vx_big_judge` |
| BI-12 | V11 | 弱 | 中 | F11：只匹配字面 `{8193` |
| BI-13 | V3 | **缺口** | 低 | F1、F3：字面与好实现等价；有害变体需要成本注入 |

---

### Major

#### F1 | issue | Major | testing | TASK-003 的 acceptance 与 design（detailed-tasks.yaml:73-76） | 针对：任务计划

摘要：TASK-003 的验收「每个 BI 至少让一条用例变红」区分不了「被预期用例抓住」与「被连带用例碰红」，也不核对 BI 是不是「好实现加单一改动」、是否与好实现行为等价；BI-13 按字面构造时与好实现等价，这条验收不可满足。

证据：

- detailed-tasks.yaml:76 只要求「至少让一条用例变红」。:73-75 没有「预期击杀者」、`bash -n`、单 hunk、其余用例仍全绿这类约束。语法错误、SC-13 计数、SC-30 闭包都会让某条用例红，算数。
- BI-13 字面是「锚点设在 `_sg_per_segment_eval` 入口」。该函数的第一条语句就是首遍 `_sg_core_eval "$cmd"`（基线 hook :1537-1539），锚点在它之前，首遍照样算进截止，与正确实现只差 hook 起点到函数入口之间的前处理耗时（量级毫秒到几十毫秒，未实测，远小于 SC-V3 的 0.3 s 容差）。直调用例自己设 `_SG_P0=$EPOCHREALTIME`（TASK-002 design 写明），也看不见锚点放在哪。有害的变体是锚点晚于首遍，或每次调用都取「现在加 3 s」；按推演，首遍 0.70 s 的 f5like 会被推到约 3.7 s，超 3.3 s（未对坏实现实测）。
- TASK-003 的交付物只有 `W13-bad-implementations.txt`；生成它的脚本不在 deliverables 里。TASK-005 若改 hook，矩阵无法重放。

建议：

1. 每个 BI 记录一行：`bi_id`、diff 行数（要求单 hunk）、`bash -n` 结果、实际变红的用例集合、SC 表里指定的预期击杀用例；验收改成「实际变红集合包含预期击杀用例，且不含与该 BI 无关的结构类用例（SC-13、SC-30b）」。
2. 每个 BI 加一栏「与好实现行为等价？」：等价的 BI 要么改写成真实错误，要么改由静态断言承担。BI-13 改写成「锚点晚于首遍」，并加静态断言：顶层只有一处 `^_SG_P0=` 赋值，位于 source 闸门之上，在 `_sg_line_match` 定义之前。
3. 把生成矩阵的脚本（类似 `mkv3.py`）列为交付物，并在 INV 里写「hook 变更后重跑」（见 F18）。

#### F2 | issue | Major | testing | TASK-004 的 title、design、acceptance（detailed-tasks.yaml:78-88） | 针对：任务计划

摘要：TASK-004 的标题是「重跑 W9–W12」，验收却只覆盖 W12 第 1–3 节与 P6；W9、W10、W11 没有验收条；W12 第 1 节的两条判据在现有数据上要么对不上，要么不可能红；脚本的输出位置会覆盖原型证据。

证据：

- :88 的 acceptance 三条：放行数、第 2 与 3 节逐字节、P6。W9（套件在实现上的结果、基线套件在新 hook 上恰好 6 组红）、W10（S1–S8、G1–G8）、W11（对抗矩阵的上界）没有对应条款。没有 W9 这条，「除 6 组外既有用例全不变」（SC-V1、P1）就没有机械验收：执笔席为了变绿而改弱别的既有用例，没有任何东西会发现。
- 「放行数不低于原型 (136/137)」：W12-real-traffic.txt 的数字是放行 137、按尺寸拦 1，共 138 条；SMAX 类是 137/137。136/137 与两种口径都对不上，减 1 的容差也没有来由。
- 「无任何越过 max(首遍 + 基线前段, 3 s) + 0.3 s 的放行」：`W12-replay-138.tsv` 只有 n、rc、outcome、wall 四个有值列（放行行的后三列是 `-`），没有「首遍 + 基线前段」。这个量只能从埋点版（`mkdbg.py`）或同次运行里取，计划没引用。更要紧的是：放行行里最慢的 1.80 s 离 3.3 s 很远，这一条在这份语料上不可能红；它要防的「放行发生在截止之后」只能靠 F3 的注入形状来证伪。
- design 的「其余不变」：`run-w9.sh`、`run-w10-w11.sh`、`run-w12.sh` 把结果写在脚本同目录的 `W9-suite.txt`、`W10-mechanism.txt`、`W11-adversarial.txt`、`W12-real-traffic.txt`（`$HERE/...`），这些都是已提交的原型证据，proposal 的证据表在引用它们。我是把脚本拷到 scratch 才避免了覆盖。按「其余不变」直接跑，会改写原型证据，并与交付物 `W14-acceptance.txt` 冲突；而「不低于原型」需要的恰好是原型那一份数字（git 里可找回，但会留下一个脏 diff）。

建议：

1. 为 W9、W10、W11 各补一条验收：W9「基线套件在实现 hook 上失败的组恰为 W9-suite.txt 列出的 6 组，失败原因同向；实现套件全绿」；W10「S1–S8、G1–G8 全 PASS，残留 0」；W11「每个形状的 rc 与 kind 与原型一致（apply-heavy-cjk 与 f5like 允许放行），且墙钟不越界」。
2. W12 第 1 节：把数字改成「SMAX 类放行 ≥ 136/137 且列出与原型不同的命令编号；VMAX 那 1 条仍拦」，并说明为什么允许减 1。上界只对回落与拦截行有意义：墙钟 ≤ max(t_trigger, 3.0) + 0.3，其中 t_trigger 取同一次运行里「放宽门打开」时刻减 `_SG_P0`（埋点）。
3. 脚本的输出目录与文件名参数化（`OUT=` 之类），TASK-004 只写 W14。

#### F3 | issue | Major | testing | SC-V3（proposal.md:407）、TASK-003 design（detailed-tasks.yaml:75）、INV-7 | 针对：proposal v3 与任务计划

摘要：SC-V3 的两条 e2e 判据里，「首遍约 2 s 的形状 ≤ 3.3 s」在共享宿主上会对正确实现假红，同时对锚点或截止错误恒绿；而硬截止本身的断言在负载下是稳定的，应当与首遍相关的断言分开。

证据：

- 首遍耗时随长度超线性增长（埋点版原型，空闲机 load 1.3，单次，命令是 `echo y y y …`）：2005 字符 0.25 s，4005 字符 0.56 s，6005 字符 1.19 s，8005 字符 1.96 s，10005 字符 2.86 s，12005 字符 4.03 s。
- 同一输入的噪声：已提交的 W11（页眉负载 2.43 3.59 3.65）里，套件形状 21ab#2 的基线是 3.52 s，同次 v3 是 2.39 s；我在空闲机上重跑，基线 2.38 s、v3 2.36 s。差约 1 s，所以 3.3 s 这个绝对界对「首遍约 2 s」的形状不稳。
- 21ab#2 与 #3 上放宽重跑只花 0.03–0.05 s（埋点：firstpass-done 2.29 s、job-done 2.34 s；#3 为 2.36 s 与 2.41 s），到不了截止，对任何锚点或截止错误恒绿（对 BI-13 的有害变体也一样）。
- 硬截止本身稳定：已提交的 W10（负载 2.64 3.65 3.67）S4、S5、S6 都是 1.00 s（上界 1.3 s）；W11 的 f5like 与 apply-heavy-cjk 在负载 2.4–3.6 与空闲机上都是 3.02–3.04 s。
- 确定性替代形状我在参考实现上跑通了：在 hook 副本的 `_sg_per_segment_eval` 首遍前注入 `sleep 1.3`，在 `_sg_relax_job` 里注入 `sleep 10`，命令取 4.3 KB 的便宜形状，结果 rc=2、oversize、墙钟 3.01 s。注入的是 sleep，时长不随 CPU 争用变；套件里已有 `wpa_hook_copy` 这种按文本复制并替换 hook 的机制可用。

建议：

1. 常驻套件里不放「结局取决于首遍耗时」的断言。SC-V3 的 e2e 改成注入形状，断言用 P3 的公式本身：墙钟 ≤ max(t_trigger, 3.0) + 0.3，t_trigger 由同一次运行里注入的时间戳给出。注入量取 0.8–1.0 s 而不是 1.3 s，给负载留余量（便宜形状的真实首遍在 3 倍负载下可到 1.7 s）。
2. f5like 保留为一条「不超过 max(…)+0.3」的 e2e 即可，不要当作 BI-13 的唯一探针。
3. 负载规矩：INV-7 只用于「收益数字」（W12 第 1 节）；截止类断言不依赖它，因为它们要常驻在任何人的机器上运行（见 F17）。

#### F4 | issue | Major | testing | SC-V8（proposal.md:412），BI-9 | 针对：proposal v3

摘要：SC-V8 里「引用全部在第 8193 字符之后」的 e2e 形状天生对负载脆弱，且文字没有说这些形状应放行还是应出增长文案；BI-9（`lim` 取被改写后的剩余串）只有在「小增长应放行」这个方向才会暴露。

证据：

- 引用在第 8193 字符之后意味着原命令至少约 8.2 KB，首遍在空闲机上至少 2.0 s（F3 的曲线），轻度负载就超过 3 s，放宽门关闭，结局从「放行或增长文案」翻成基线 oversize。我跑了一个 12.2 KB 的晚引用形状（3 个引用）：首遍 4.06 s、全程 4.08 s、结局是 oversize 而不是增长文案。8.4 KB 的单引用形状：首遍 2.10 s，可放行但余量只有 0.9 s。
- 「→ 增长文案」只写在 21ag、21aj 后面，晚引用形状的预期没有写。取剩余串会让上限变小，拦的方向仍是拦，看不出来；只有「增长很小应放行」的用例会红。
- 参考实现上，在 `_SG_RELAXED=1` 下直调 `_sg_vx_apply`（不经首遍、不受截止、毫秒级）的 8 条全部 PASS：晚引用小增长放行（`$NAME` 与 `${NAME}` 两种拼写）、晚引用大增长拦、增长恰为 8192 放行、8193 拦、三个变量各自不超限但累计超限拦、21ag 的稠密形状拦。

建议：SC-V8 改成这组直调（写明每条的预期返回值），e2e 只保留 21ag 与 21aj 两条（首遍便宜）去钉增长文案。累计超限这一条建议明确写进去：它是「`lim` 在循环里被重算」这类错误的探针，现有文字没有点名。

#### F5 | issue | Major | testing | SC-V6（proposal.md:410），BI-7 | 针对：proposal v3

摘要：SC-V6 的「会回落的输入」没有确定性来源；而回落从外部看与「放宽门没打开」字节相同（P6 本来就是这么设计的），输入若恰好没回落，用例照样绿，BI-7 就活下来。

证据：

- f5like 的余量薄：埋点显示 relax-start 在 0.71 s，作业到 3.0 s 被杀、没有 job-done，即重跑需要超过 2.29 s；生成器注释说三段各约 1 s，约 3 s，余量约 30%。换一台快机器就可能不回落。
- apply-heavy-cjk 余量大（Why 第 4 项：单次 apply 约 12 s）但依赖 UTF-8 locale，TASK-002 已有「涉及 locale 用 C.UTF-8 并先断言字符集」的要求，但没有说回落发生了要被确认。
- 回落与放宽门关闭输出相同，所以单看 stderr 无法判断回落路径被走到。

建议：二选一，最好都做。（a）用注入形状（F3）让回落确定发生，并用函数入口计数（套件已有 `wpa_marker_case`）确认 `_sg_relax_run` 被进入并返回 4；（b）直调：桩 `_sg_relax_run` 返回 4，调 `_sg_per_segment_eval`，对比基线 stderr 的 sha256。两者都要在好实现上绿、在 BI-7 上红；TASK-003 的 BI-7 构造两种坏法（写时间文案、什么都不写）都要覆盖。

#### F6 | risk | Major | testing | SC-V10（proposal.md:414），BI-11，Decision 11 | 针对：proposal v3（未对坏实现实测）

摘要：SC-V10 只直调 `_sg_judge_one … nocredit`，触及不到 `_sg_vx_big_judge` 的「仅匹配规则」分支；若实现把这条分支写成自己的规则循环（Decision 11 禁止的形状），而 `_sg_judge_one` 的 nocredit 分支仍然正确，直调用例全绿。

证据：

- 被测对象只是 `_sg_judge_one`；`_sg_vx_big_judge` 里的分支在它的调用者里。这是结构上的事实，不依赖实测。
- 能够到达该分支的便宜 e2e 形状我在参考实现上跑通了：原命令约 4.1 KB（一个 4000 字符变量引用两次，加上 `python3 -c 'import os; print(os.environ.get("HOME"))'` 与填充），副本超过 8192 且最长行超过 8192，期望放行；结果 rc=0，0.69 s，首遍便宜，对负载不敏感。
- BI-11 的后果是多拦（os.environ 单键读取被 `.env` 前缀误拦），方向是 fail-closed，不是漏检，所以定为 Major 而不是 Critical。

建议：SC-V10 增加这条 e2e，或增加一条直调 `_sg_vx_big_judge` 的用例；TASK-003 的 BI-11 要求两种落点都构造（改 `_sg_judge_one`、改 `_sg_vx_big_judge`）。

#### F7 | issue | Major | testing | SC-V9（proposal.md:413）与 BI 清单 | 针对：proposal v3

摘要：SC-V9 的 TMAX 形状有二义，且 BI 清单里没有「重跑里丢掉或放宽 TMAX」这一项；重跑内的 TMAX 目前没有任何用例守着。

证据：

- 「1 KB 值 × 8 引用」若取 1024：我在基线函数上直调，值 1000 字符时 `_sg_vx_apply` 返回 0、副本 8012 字符；值 1024 时返回 2（撞 SMAX，副本不构建）。也就是说取 1024 的形状撞的是 SMAX，不是 TMAX。
- 既有 21ah 与 21ai 的每段副本都不超过 8192，永远不进放宽重跑；基线里 TMAX 超限发生在首遍的 W10 里，也不触发放宽。所以「重跑内仍受 TMAX 约束」只能由 SC-V9 的直调形状来守，而 BI-8 说的是 VMAX。
- 在重跑里把 TMAX 丢掉不会漏检（判定仍在截止内），但会让放宽面比规格宣称的更大，也违反 P9。

建议：SC-V9 写成确定的直调形状：`_SG_RELAXED=1` 下直调 `_sg_vx_pass`，9 段，每段副本约 8100（值取 1000 字符，不是 1 KB），期望出 TMAX 文案；BI 清单补一项「重跑内不计 TMAX」。

#### F8 | decision | Major | testing | TASK-002 acceptance「bash 3.2.57 下套件全绿」（detailed-tasks.yaml:63）与套件 SC-13 | 针对：任务计划

摘要：bash 3.2 没有 `EPOCHREALTIME`，不放宽；那么 6 组改写的用例与新增的放宽依赖用例（SC-V3 e2e、V7、V8 e2e、V10 e2e）断言的是放宽后的结局，在 3.2 下必红，除非按版本分支；计划没说怎么分。

证据与后果：

- 若选「3.2 下跳过」：SC-13 的头注释计数断言接受「N」或「N（无 zsh）」两个值之一等于实跑总数（suite :3213-3232），跳过数不同会让它在 3.2 上变红；再加一个 bash 版本维度，头注释就需要第三个值，计划没有安排。
- 「3.2 下的套件」怎么跑也没写：hook 的 shebang 是 `#!/usr/bin/env bash`，只有 PATH 里 3.2.57 在前，hook 本身才在 3.2 下运行。
- 这是一个需要裁的口径，所以标 decision。

建议（我倾向 A）：A. 放宽依赖用例在 3.2 下改为断言基线结局（版本条件期望，用例仍计数，SC-13 不变）；SC-V2 的「3.2 下 e2e 与基线逐字节相同」保留。B. 跳过并把头注释改成三值。无论选哪个，写进 TASK-002 的 design 与 acceptance。（3.2 下套件未实跑。）

#### F9 | issue | Major | documentation | SC-V12（proposal.md:416）「standards 三处计数一致」 | 针对：proposal v3 与任务计划

摘要：这一半没有宿主：没有任何测试或任务去核对它；基线上已经漂移；口径还有两种相反的读法。

证据：

- 套件的 SC-13 只核头注释，其注释自称 standards 三处靠回填时机械 grep（「跨仓，不在本 test 内断言」）。detailed-tasks.yaml 里没有任务产出或运行这个 grep：TASK-002 的交付物不含 standards，TASK-006 没有 deliverables。
- 漂移已存在：standards（a611136）`conventions/secret-hygiene.md` 的 :23、:316、:352 写的都是 822（816 无 zsh），套件头注释是 831（825 无 zsh），v1.76.1 的 CHANGELOG 写 825。
- 「一致」可读成「三处彼此一致」（基线上已满足，恒绿），也可读成「等于套件实跑数」（基线上已红）。proposal Impact 写的是后者。

建议：钉口径为「等于套件头注释两值之一」；TASK-006 加一条小脚本 grep 三处数字并与头注释比对，在基线上跑一次留下「红（822 对 831）」的证据；standards 是独立子模块，它的提交、本地合并、gitlink 提升写进 TASK-006 的步骤。

#### F10 | issue | Major | documentation | CHANGELOG 终稿无人认领（INV-2、TASK-001/002/006） | 针对：任务计划

摘要：INV-2 允许改 `aria/CHANGELOG.md`，但没有任何任务把它列为交付物或验收对象；草稿里的占位符来自四个不同任务。

证据：TASK-002 的交付物只有 hook 与套件；TASK-006 没有 deliverables，验收是 owner 授权、三项机械检查、双推一致，不含 CHANGELOG 内容。草稿里有 `<date>`、`1.77.x`、`<N>`（放行数，来自 TASK-004）、测试数（来自 TASK-002）、`#<n>`（残余 issue，来自 TASK-001）。草稿承载两件披露：放宽面申报，以及更正 v1.76.1「永不 fail-open」；没有验收条验证它们出现。

建议：TASK-006 deliverables 加 `aria/CHANGELOG.md` 终稿；acceptance 加断言「无 `<…>` 占位；含放宽面申报段、更正句、两个残余 issue 号」。

---

### Minor

#### F11 | risk | Minor | testing | SC-V11（proposal.md:415），BI-12 | 针对：proposal v3（未对坏实现实测）

摘要：静态判据只匹配字面 `{8193`；对用常量构造重复次数等其他写法没有约束。这类检查的维度（拼写）与错误的维度（算法代价）不匹配。BI-12 真正的危害是代价，行为侧的网是 SC-V7 的「良性大命令在时限内放行」，是否足够未实测。

建议：静态断言改成「`=~` 右侧不得出现大计数的重复量词」（不依赖具体数字的拼写），并加一条行为用例：约 60 KB 的良性副本在重跑里的耗时上界。

#### F12 | issue | Minor | testing | SC-V5（proposal.md:409）的桩形 | 针对：proposal v3

摘要：「后台子进程继承 stderr 并睡 6 s」有两种写法，参考实现只对其中一种绿。

证据（参考实现，截止 1 s，我跑的）：

- 形 A，桩自己等子进程（`sleep N & wait`）：rc=4，1.00 s，返回后立即计数残留为 0（不需要像 v3unit.sh 那样先等 1.6 s）。
- 形 B，桩立即返回、子进程仍占 stderr：rc=0，墙钟 3.71 s（等于子进程寿命）。原因是作业已正常结束，计时器已被杀，命令替换在等管道 EOF。
- 形 C，子进程脱离 stderr、作业正常返回：rc=0，0.00 s，子进程残留 1 个。
- B 与 C 在生产里不可达：对 hook 非注释行检查，后台启动与进程替换只出现在 `_sg_ext_*` 与输入解析，放宽作业的调用闭包里没有。但 SC-V5 的文字对 A、B 都合法，照 B 写会让参考实现自己红。

建议：钉成形 A；P5 的「作业结束后没有残留进程」限定为「被截止杀死的作业」。

#### F13 | issue | Minor | testing | TASK-001 的基线红绿清单（detailed-tasks.yaml:44） | 针对：任务计划

摘要：清单把 SC-V1 标成基线绿，但 SC-V1 同时包含「6 组按 W9 改断言」，改后的 6 组在基线上必红；SC-V3、V4、V5、V10 的「基线红」是因为函数不存在（127），不是断言能判别行为；SC-V6 在基线上恒绿（基线输出等于基线），单靠它抓不住 BI-7。

建议：清单按「SC-V1 的两部分」分别标；注明 SC-V6 只作回归闸，须配 F5 的非空性断言；红的原因写明是「缺函数」还是「断言判别」。

#### F14 | issue | Minor | documentation | `rule6_note`（detailed-tasks.yaml:8-14） | 针对：任务计划

结论：合规，但有两处不完整。

- 合规部分：五个字段齐全，值域合法；`decision_table_row: "n/a"` 对「本 spec 不属 Skill 变更」成立（SOT §4.1），与 WP-A 的块 A 相同；改动对象是 hook、套件、注释、CHANGELOG，没有 SKILL.md、description、references。
- 不完整 1：note 引用了 WP-A 先例「面向 AI 的文案逐 hunk 判」。WP-A 把这类 hunk 写成独立的块 B（`decision_table_row: 1`，scenario 字段 not_required），并把该判断列入「待 owner 复议」（Rule #10：AI 自作主张的流程判断须入 handoff）。本计划把「row 1」只写在自由文本 note 里，结构化字段没有记录，也没有登记复议。
- 不完整 2：note 称 longline 模板「逐字复用现有 oversize 模板的两条指令行」，但 SC-V7 只钉首行与 `Matched pattern:` 行；两条指令行（模板里唯一带处方性的部分）与中文行没有断言，「逐字」不可证伪。SOT §2 第 1 行要求「baseline-failing 的结构化测试在场」，这里在场的测试没有覆盖处方性那几行。

建议：按 WP-A 拆成块 A（hook 与测试）和块 B（三处面向 AI 的文案，row 1）；块 B 的断言加「Split it…」两条与中文行（或整段模板的 sha256）；在 handoff 登记「AI 判块 B 为 row 1」待复议。

#### F15 | issue | Minor | documentation | What 7 / `commentsync.py`（proposal.md:331-354） | 针对：proposal v3 与原型

摘要：（a）INV-1「逐字落地原型」与 TASK-002「commentsync target 为 GREEN」不能同时满足；（b）「应出现」的词只核对出现；（c）封闭清单之外仍有陈旧注释。

证据：

- 对原型 hook 跑 target 模式，「应出现」词里 `_SGV_LMAX`、`hard deadline`（原型写的是大写 `HARD deadline`，区分大小写）、`nocredit`、`longline`、`_sg_relax_run`、`status 4` 六个在 hook 注释里是 0 次：commentsync 只读整行注释，原型把说明写成了代码行尾的注释。执笔席必须另写整行注释，计划没有点出。
- 「应出现」只核对出现，不核对位置，可以把词塞进任何注释行过关（迁就检查器的措辞）。
- 陈旧注释：hook :1534-1535（`_sg_per_segment_eval` 头注释）写着「Length budget: an overrun inside _sg_vx_pass blocks there」，放宽后 SMAX 超限会返回 4 并交给重跑；它在第 8 处的范围（:1528-1536）内，但第 8 处的退役短语只取了前一句。

建议：INV-1 写明「注释以 What 7 为准，允许与原型不同」；第 8 处加一条退役短语；「应出现」词要求出现在同一注释块里。

#### F16 | issue | Minor | process | INV-6 与 TASK-007（detailed-tasks.yaml:29、:118-120） | 针对：任务计划

摘要：关闭关键词只能出现在阶段 D 主仓提交里，这条约束落在 INV-6 和 TASK-007 design 的一句「推送前做 INV-6 关键词核对」，没有命令、没有验收；TASK-002、005、006 的推送都先于 TASK-007，却没有同样的核对。

另：TASK-007 的 title 是「对账后关闭」，acceptance 里却没有「#217 已处于 closed」。#217 在 10CG/aria-plugin，而关键词放在主仓（10CG/Aria）的提交里，跨仓关闭的语义（Forgejo 与 GitHub 镜像）我没有核实。

建议：给一条可复制的核对命令（对每个将推送的仓库，在 `origin/master..HEAD` 上用 `git log --grep -E` 查「关闭类动词加 154、203、217、221」），写进 TASK-002、006、007 的验收；TASK-007 加「#217 状态为 closed」；若依赖关键词关闭，先在一个一次性 issue 上验证跨仓语义，否则改用 API 直接关闭。

#### F17 | risk | Minor | process | INV-7（detailed-tasks.yaml:31）与 TASK-004 | 针对：任务计划

摘要：「一分钟负载 < 2」可以执行，但定义不全。证据本身是在负载 2.4–3.6 下取的（W12 页眉 2.40 3.47 3.61 与 2.47 2.77 3.26，W10、W11 页眉同量级）；我这次会话空闲时读数在 0.5–1.3 之间。没有写在哪个时刻量（实验自己会给一分钟均值加约 1），也没有写违反时怎么办。

建议：起止各记一次 `/proc/loadavg`，任一 ≥ 2 即作废重跑；等待窗口用轮询，不靠人工判断。确定性断言（F3）不依赖 INV-7。

#### F18 | risk | Minor | process | TASK-003、004、005 的并行与失效 | 针对：任务计划

摘要：TASK-003 与 TASK-005 都只依赖 TASK-002，TASK-005 的修订会改 hook，使 TASK-003 与 TASK-004 的结果失效，计划没有「证据绑定 hook 的 sha256，hook 变更后重跑」的规则。

建议：INV 里加一条；TASK-006 验收核对 W13、W14 页眉里的 hook sha256 等于待发版的 hook（W9 页眉已经在记 sha256，可沿用）。

---

## Verdict

PASS_WITH_WARNINGS（0 Critical、10 Major、8 Minor）。

没有发现「照计划实现会造成安全退化」的 Critical：放宽的失败方向仍是拦；本席看到的问题集中在验收能否证伪，以及几条 SC 的形状会让好实现假红或让坏实现恒绿。需要在进入 B.2 之前修的是 F1–F10；其中 F3、F4、F5 影响 TASK-002 的用例怎么写，F2、F8 影响 TASK-004 与 TASK-002 的验收，改计划比事后补用例便宜。

## 轮次记录

做了什么：读任务书、`detailed-tasks.yaml`、proposal v3 全文、`dispositions.md`、`v3/README.md`、`mkv3.py`、`v3unit.sh`、`run-w10-w11.sh`、`matrix.sh`、`gen-v3.py`、`mkdbg.py`、`probe21.sh`、`w10b.sh`、`commentsync.py`、W9–W12 与 W10b 结果文件、基线 hook 的 W10 段（:570-960）与判定段（:1488-1590）、套件的 `wpa_*` 辅助函数与 21aa–21ap、SC-13 与 SC-30b、`skill-benchmark-exemption.md` 全文、WP-A 的 `rule6_note` 先例、standards 的 secret-hygiene.md 三处计数、v1.76.1 的 CHANGELOG 条目。

实验（脚本都在 scratch 目录 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r1/qa-engineer/`）：`tl.sh` 与 `v3dbg.sh`（阶段时间线）、`shapes.sh`（SC 形态的好实现对照）、`inject.py`（成本注入）、`v3extra.sh`（桩形 A、B、C）。仓内没有改任何文件；`git status` 对 `.aria/notes` 保持干净。没有启动任何后台进程需要清理（桩的子进程在几秒内自行结束）。

没核实：见 0 节「未核实」；另外 bash 3.2 下的套件、人造负载下的时延分布、`run-w9.sh` 与 `run-w12*.sh`、Forgejo 跨仓关闭语义。**所有 BI 与 SC 的对应判断都是纸面推演，没有坏实现的实测数据。**

工具调用约 50 次。
