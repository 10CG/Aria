---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T19:42:05.054Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — knowledge-manager 席位报告

> 对象：`10CG/aria-plugin#217` / `secret-guard-w10-failclosed-narrowing` 的 A.2 计划（主仓 `95cf1de7`，`detailed-tasks.yaml` v3.1）及其依据 proposal v3.1、`v31/` 原型与可执行验收、`dispositions.md`。
> 侧重：文档与流程。数字 / 用例编号 / 簇号回链的一致性、`content-integrity.md` §4.4、CHANGELOG 草稿与发布同步面、`rule6_note` 块 A / 块 B 对照 SOT 与 WP-A 先例、`v31/README.md` 能否照做；任务书「审查要点」各条也覆盖。
> 纪律：只读；临时文件与坏实现全在 `/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217pp-r2/knowledge-manager/`；没有读同轮其他席位的报告，没有读真实命令语料；没有跑 W9、W12、W13 全量；除本文件外没有改仓内任何文件。

## 审计结论

**0 Critical / 4 Major / 12 Minor（共 16 条）。** 机制与设计方向本席不质疑。R1 本席（KM-1…KM-15）的主体修复都落到了：INV-6 有了可执行的核对命令、TASK-001 有 owner 门、基线红绿挪到设计阶段并实跑、`wpa_x_finding` 的区分 helper、块级注释清单、残余有载体、TASK-007 补了 D.1 / D.2 / handoff / 上线后复验。剩下的问题集中在四处「文字声称有、实际没有或跑不通」：

1. `rule6_note` 块 B 的「逐字断言」替代物只钉了 `longline` 的指令行，两条增长原因串与 `longline` 的首段、中文行没有任何用例钉住（实跑坏实现 94 / 94 全绿）——PP1-A19（KM-5）的复发。
2. 「计时判据与负载无关」不成立：同一原型在宿主负载 15 至 19 下全量跑 `sc-cases.sh` 红 8 条，`V7-E1` / `V7-E13` 三轮三红。
3. TASK-006 的 standards 计数验收命令 `grep -n 'cases'` 找不到三处里的两处（`:23`、`:352` 写的是 `self-tests`），还会命中无关的 `:317`——PP1-A23（KM-4）的复发。
4. TASK-002「搬入 sc-cases.sh 的全部用例、逐字照搬」既不能字面执行，搬进套件的那份副本也不在任何变异测试的覆盖里。

### 已核实成立（不需处置）

1. `proposal.md` 由 `v31/fill31.py` 从 `proposal-template.md` + 原型 + 证据重生成，75963 字节与已提交文件逐字节相同（`cmp` 无差异）。
2. `mkv31.py` 对当前 `aria/hooks/secret-guard.sh`（与基线 `59e333c` 零差异）生成的原型 sha256 前缀 `9f61db0e7b8b`，与 W9 / W11 / W12 / W13 页眉一致；W8 阶段在隔离环境里重跑，diff 正文逐字节相同。
3. `commentsync.py`：基线 hook + 基线套件 baseline 模式 GREEN；`--hook-only <原型> target` GREEN（`V12-C1`）。
4. `sc-cases.sh <原型>`（bash 5.2.15，起始负载 7.40 / 9.10 / 7.49）PASS 94 / FAIL 0 / SKIP 0，与 W13 一致；组合坏实现那一轮（起始负载 2.56 / 3.25 / 5.10）用时 45.8 s，与 README 的「约 45 s」一致。
5. proposal / dispositions / 任务计划里显式写出的用例编号全部存在于 `sc-cases.sh` 的输出；W13 汇总表、BI 表（23 条、指定用例、连带变红数）与 W13 第 3 节逐条对得上；P 表与 SC 表的用例集合除 KM2-12 所列外一致。
6. 数字：E12 的 739 / 130 / 17.6%、W1 的 138 = 137 + 1 且最大增长 6200、W12 的 136 + 1 + 1 与 0 / 138 越界、300 / 300 与 40 / 40、W8 的 +187 / −49 与 4 行空行、W13 的 94 / 94 / 94 / 94 / 57 与基线 19 / 73，均与证据文件一致；`ident-300.lst`、`w1-sample40.lst` 与 `v3/` 逐字节相同。
7. `dispositions.md` PP1 表 39 行与 R1 汇总的 39 簇一一对应，级别一致（A1 C；A2 至 A24 M；A25 至 A39 m）；proposal 与任务计划里引用的 PP1 簇号，语义与该簇处置行对得上。
8. `detailed-tasks.yaml` 被仓内 `lib/detailed_tasks.py` 解析为 `parse_ok: true`、7 个任务，依赖图无环；`rule6_note` 两块的五字段齐全；`agent: implementer` 在其他 change 里有 6 处先例。
9. 引用的提交哈希（`acd6a95`、`41e9308`、`910d9fa2`、`a136dbf8`、`95cf1de7`、`cddb2465`、aria `59e333c` / `68c7f65`、standards `a611136`）都存在；Why 与 What 里引用的基线行号（`:594–596`、`:645`、`:646`、`:659`、`:660`、`:666`、`:668–669`、`:685`、`:694`、`:725`、`:740`、`:744`、`:446`、`:476`、`:1563`）逐个对得上。
10. owner 裁定的引用（「选项【1】」、`post_implementation` / `pre_merge` 为 off）与 `post_spec-R2-…-aggregated.md` 的「Owner 裁定（2026-10-22）」及 `.aria/config.json` 一致。
11. 块 A 的写法（`decision_table_row: n/a`，「这是分类，不是免验主张」，验证口径为 substitute）与 WP-A 块 A 一致；块 B 的形式（第 1 行、`not_required`、「AI 自作主张、待 owner 复议」）与 WP-A 块 B 一致；`rule6_note` 在 aria 插件里没有任何代码消费方，嵌套成 `block_A` / `block_B` 不会破坏解析。

### Findings 索引

| # | severity | type | category | scope | 针对 | 一句话 |
|---|---|---|---|---|---|---|
| KM2-1 | Major | issue | testing | `detailed-tasks.yaml:26`；`proposal.md:652`、`:667`；`sc-cases.sh:115-118`；`sc-direct.sh:113-127` | 任务计划 + proposal + 验收用例 | 块 B 声称的「逐字断言」替代物不存在：增长原因串无任何断言，`longline` 首段与中文行不受钉（PP1-A19 复发） |
| KM2-2 | Major | issue | testing | `sc-cases.sh`、`sc-direct.sh` 的计时窗；`proposal.md:581`；`README.md:43`；`detailed-tasks.yaml:43`（INV-7） | 验收用例 + 文字声称 | 好实现在高负载下假红（负载 15 至 19 红 8 条），文字却说与负载无关、INV-7 还把它排除在负载纪律之外 |
| KM2-3 | Major | issue | testing | `detailed-tasks.yaml:142`、`:148`；`proposal.md:650`、`:664`、`:668` | 任务计划 | TASK-006 的 standards 计数验收命令找不到 `:23` 与 `:352`、误中 `:317`；计数是一对数而计划写「同一个 N」（PP1-A23 复发） |
| KM2-4 | Major | decision | testing | `detailed-tasks.yaml:75`、`:93`、`:114`；`sc-cases.sh:21`、`:123`；`run-mutants.sh` | 任务计划 | 「搬入…逐字照搬」有两种读法且字面做不到；搬进套件的副本不在 23 个坏实现与 TASK-003 的覆盖里 |
| KM2-5 | Minor | issue | documentation | `proposal.md:522`；`fill31.py:10-17` | proposal + 证据脚本 | 「共 19 个 hunk、5 个只改注释」应为 18 / 4：`re.split` 的首个空串被当成注释 hunk |
| KM2-6 | Minor | issue | documentation | `README.md:35`、`:37`、`:43`；`proposal.md:689`；`run-evidence.sh:17-19`、`:21` | 证据 + proposal | 复现说明与实际行为不符：成功的阶段会覆盖已提交证据、W13 静默漏掉 3.2 一轮、refreeze 指针错、无调用说明、计数口径两样 |
| KM2-7 | Minor | issue | documentation | `detailed-tasks.yaml:31-33`、`:56-62`、`:93`、`:127`、`:160-163` | 任务计划 | INV-2 的封闭清单仍漏计划自己的产出；proposal 由模板生成这件事没写进计划；W14 的脚本无名（PP1-A38 复发） |
| KM2-8 | Minor | issue | documentation | `detailed-tasks.yaml:74`、`:113`、`:115` | 任务计划 | TASK-004 的 W8 / W9 验收措辞与 What 6 的内容差、SC-13 的事实冲突；What 6 的提交次序未定 |
| KM2-9 | Minor | risk | documentation | `detailed-tasks.yaml:26`、`:56-62`、`:69`、`:160-168`；`proposal.md:569-574` | 任务计划 | 待 owner 复议的 AI 判定与关闭 #217 的动作没有载体与门；TASK-001 把无关的上呈挂在实现前面 |
| KM2-10 | Minor | issue | documentation | `proposal.md:650-651`；`detailed-tasks.yaml:142-143`、`:147-152` | proposal + 任务计划 | 发布同步面「以 v1.77.1 发版提交为样板」出处不准；`VERSION` 行与 standards 版本史 / 族清单未定 |
| KM2-11 | Minor | issue | documentation | `proposal.md:17`、`:74`、`:224`、`:542`、`:551`、`:701`；`dispositions.md:62`；`README.md:45` | proposal + 证据 + dispositions | §4.4 与编号约定：「只有 `${#1}` 一类」差一处，席位原编号未定义，dispositions 有两处裸号（KM-14.5 复发） |
| KM2-12 | Minor | issue | documentation | `proposal.md:526-539`、`:598-611` | proposal | 用例范围写法与 SC / P / BI 三表互相错位：`V2-G1`–`V2-G11` 含不存在的 G9 / G10，P5 漏 `V5-S13`，SC 到 BI 的链接有 5 处交叉 |
| KM2-13 | Minor | issue | documentation | `proposal.md:654-671` | proposal（CHANGELOG 草稿） | 占位符重名且含义不同，「以前不到 1 s 就拦」与 W11 不符，测试数没写含不含 zsh |
| KM2-14 | Minor | risk | documentation | `proposal.md:145-170`；`commentsync.py:43-51`；套件 `:2578`、`:2628-2630`、`:2679`；套件头注释 `:5-7` | proposal + 验收 | What 7 表的行范围与 commentsync 实际追踪的块不一致，套件里仍有失实的邻近注释不在任何块内（PP1-A18 残余） |
| KM2-15 | Minor | risk | architecture | `detailed-tasks.yaml:43`、`:45` | 任务计划 | INV-7 没有停止规则；INV-8 的作废规则漏了 TASK-003 的 W14，「之后」有两种读法 |
| KM2-16 | Minor | risk | documentation | `proposal.md:528`、`:571`、`:600`、`:708`；`W9-suite.txt:2`；`sc-cases.sh:30`；`detailed-tasks.yaml:59`、`:69`、`:91` | proposal + 证据 | 证据可追溯性缺口：决策 14 的「137 → 73」无物证，「旧套件恰好 6 组」的盲区未限定，W13 的 SKIP 0 是空转，三处引用 memory 名 |

### 逐条 finding

#### KM2-1　块 B 的「逐字断言」替代物不存在（PP1-A19 / R1 KM-5 复发）
- **type**：issue　**severity**：Major　**category**：testing（兼 documentation）
- **针对**：任务计划 `meta.rule6_note.block_B.note`；proposal Impact 的 Rule #6 段与 CHANGELOG 草稿的 Rule #6 行；验收用例
- **scope**：`detailed-tasks.yaml:26`；`proposal.md:652`、`:667`；`sc-cases.sh:45`、`:97`、`:115-118`；`sc-direct.sh:113-127`
- **摘要**：块 B 把 AI 可见的新文字（`longline` 模板、两条增长原因串）判为 SOT §2 第 1 行（描述性），理由是「substitute = `V11-S3`（指令行逐字相同，改一个字即红）+ SC-V7 / SC-V8 的逐字断言」。`V11-S3` 确实钉住了指令行；但「SC-V7 / SC-V8 的逐字断言」不存在：SC-V8 的 `V8-D1`–`V8-D3` 只断言 `_sg_vx_apply` 的返回码与增长字符数，一个字也不看；SC-V7 的 `V7-E14` 等只用 `grep -q 'has a line longer than'` 分类。没有任何端到端用例的期望值是 `growth`（`kind()` 能分出 `growth`，但没有用例要求它）。SOT §2 第 1 行要求替代测试「必须在场」；缺席的部分，这一行的前提就不成立。
- **证据**：实验脚本 `…/knowledge-manager/mk_km_mutants.py`，在原型上各改一处，再跑完整 `sc-cases.sh`：
  - M1：`longline` 首段（「…(fail-closed).」之后）插入一句处方句「end it with a guard:ack line and run it again」；
  - M2：整串模式的增长原因串改回基线措辞「the command is longer than $_SGV_SMAX …」；
  - M3：分段模式的增长原因串同样改回；
  - 三处合并的坏实现 `km-m123.sh`：**PASS 94 / FAIL 0 / SKIP 0**（`sc-km-m123.out`，起始负载 2.56 / 3.25 / 5.10）。组合都抓不住，单个也抓不住。
  - M4：只改 `longline` 指令行里一个字（`Edit` 改 `Edits`）：`V11-S3` 转红，「改一个字即红」对指令行成立。
  - M6：中文行前半句加一个处方分句、保留共用的「请拆成更小的命令」收尾：`V11-S3` 保持绿（它把最后一行排除在比较之外），未被抓住。
  - 旧套件改写之后，分段增长串可由 21ag / 21aj 的「names the limit that was hit」钉住（`W9-suite.txt:20-24` 已显示新串），整串增长串则没有任何位置钉它：整串模式的 21ac / 21al / 21ao 现在出 `longline`，不出增长串。
- **建议改法**：二选一。（a）补机械钉：`V11-S5` 把 `longline` 的整段 heredoc（`$pat` 与 `Command was` 行归一化后）与套件里存的期望文本逐字比较；补两条端到端形状（整串、分段各一，增长 8193）断言完整的增长原因串，期望值 `growth`。这样 WP-A 的可证伪锚点「追加处方性句子即转红」才对新文字成立。（b）把 `detailed-tasks.yaml:26`、`proposal.md:652`、`proposal.md:667` 三处改成实际存在的钉（只写 `V11-S3` 钉指令行、21ag / 21aj 钉分段增长串），并明说首段、中文行、整串增长串没有钉，因此不能按「描述性且有 substitute」声称，须交 owner 在 SOT §2 第 4 行（拿不准）与第 3 行之间复议。无论选哪个，CHANGELOG 草稿的「以逐字断言替代 AB」不能带着现在的措辞发版。

#### KM2-2　好实现在高负载下假红，文字却说与负载无关
- **type**：issue　**severity**：Major　**category**：testing（兼 documentation）
- **针对**：验收用例 + 文字声称
- **scope**：`proposal.md:581`；`README.md:43`；`detailed-tasks.yaml:43`（INV-7）；`sc-cases.sh:78`、`:82-87`；`sc-direct.sh:70-79`、`:88`
- **摘要**：三处文字都说计时判据来自注入的固定延迟、与负载无关，INV-7 还据此把 `sc-cases.sh` 排除在「一分钟负载低于 2」的纪律之外。注入的延迟只固定了「延迟落在哪」，没有固定「窗口多宽」：用例的上界仍是绝对墙钟（`0.3 s`、`1.3 s`、`3.6 s`、`4.3 s`、`4.5 s`、`16.5 s`，e2e 外层 `timeout 12`），而「放宽生效」型用例（`V7-E1`、`V7-E13`、`V7-E14`、`V9-E10`、`V9-E11`）要求真实的重跑作业在 3 s 内跑完——这取决于本机自然速度。负载一高，好实现走的是安全的回落（基线文案），用例却判红。
- **证据**（同一原型 `v31.sh`，sha256 前缀 `9f61db0e7b8b`，bash 5.2，`taskset -c 0,1 nice -n 19`，宿主同时有其他席位在跑）：

  | 轮 | 起始负载 1 / 5 / 15 分钟 | 结果 |
  |---|---|---|
  | `sc-proto.out`（全量） | 7.40 / 9.10 / 7.49 | PASS 94 / FAIL 0 |
  | `sc-km-m123.out`（全量，文本类坏实现） | 2.56 / 3.25 / 5.10 | PASS 94 / FAIL 0 |
  | `V7-E1` + `V7-E13`，`SC_DIRECT=0`，连跑 3 次 | 15.84 → 18.90 | 6 / 6 红：`V7-E1` 一次放行但墙钟 4.61 s > 4.5 s，两次回落成 `oversize`；`V7-E13` 三次都回落（hook 5.84 s / 4.72 s / 3.70 s） |
  | `sc-proto-highload.out`（全量，耗时 4 分 58 秒） | 17.46 / 13.29 / 8.74 | PASS 86 / FAIL 8：`V5-S5`（1.81 s，窗 0.85 至 1.3）、`V6-E2`、`V3-E3`、`V3-E5`、`V2-E6`（四条都撞到 `timeout 12`，rc=124）、`V3-E4`（3.68 s，窗 2.85 至 3.6）、`V2-E7`（6.02 s，窗 3.2 至 4.3）、`V9-E11`（hook 与基线都 rc=124） |

  同一轮里 `V7-E1` 放行用了 2.85 s、`V7-E15` 因接受「回落的基线字节」而没红：放行离 3 s 截止只差 0.15 s。负载 7 至 9 是这台宿主的常态（本席开工时 10.22 / 8.14 / 5.97），INV-7 的门槛是 2。
- **建议改法**：（a）改三处文字：「注入延迟固定的是延迟的位置，窗口宽度仍是绝对墙钟；放宽生效型用例要求本机在 3 s 内跑完作业」。（b）INV-7 不再豁免 `sc-cases.sh`。（c）在 `sc-cases.sh` 开头读 `/proc/loadavg`，高于阈值（数值请 TL 或 owner 定）时把窗口型与放宽生效型用例发成 `SKIP`——`res()` 已有 `SKIP` 计数（`sc-cases.sh:30`），只是从来没有用例发它（见 KM2-16）；TASK-002、TASK-004 的验收写成「SKIP 数为 0 才算数」，否则 SKIP 会变成恒绿的出口。（d）或者把窗口的上界改成相对一个空 hook 探针的实测耗时，而不是常数。

#### KM2-3　TASK-006 的 standards 计数验收命令跑不通（PP1-A23 / R1 KM-4 复发）
- **type**：issue　**severity**：Major　**category**：testing（兼 documentation）
- **针对**：任务计划 TASK-006，并牵连 proposal Impact 与 CHANGELOG 草稿
- **scope**：`detailed-tasks.yaml:142`、`:148`；`proposal.md:650`、`:664`、`:668`；`standards/conventions/secret-hygiene.md:23`、`:316`、`:317`、`:352`；套件 `:11`、`:3213-3230`
- **摘要**：验收写「`grep -n 'cases' standards/conventions/secret-hygiene.md` 的三处与套件头注释都等于 N」。实测该命令只命中 `:316`（`822 regression cases, 816 无 zsh`）和无关的 `:317`（`secret-scan.test.sh` 的 `129 regression cases`）；`:23`（`822 self-tests [816 无 zsh]`）与 `:352`（`822 self-tests (816 无 zsh)`）根本不含 `cases`。结果是：该漏的两处照样漏（v1.76.1 就是漏了这一步，R1 KM-4 的前科），而 `:317` 的 129 会让字面读法恒红。另有三处不清：
  - 每处是一对数（含 zsh / 无 zsh），套件头注释也是一对（`831 cases (825 without zsh)`），SC-13 接受二者之一等于实跑数（套件 `:3221-3226`）；计划写「同一个 N」。本机没有 zsh，实跑只能看到无 zsh 的那个数，含 zsh 的数要靠推算，计划没说怎么推。
  - 同一个字母指两个不同的量：TASK-006 `:141` 的 `<N>` 是 W12 的放行条数，`:142` 与 `:148` 的 N 是测试计数；CHANGELOG 草稿里的两个 `<N>`（`proposal.md:664`、`:668`）也是这两个不同的量（见 KM2-13）。
  - N 的出处：proposal `:650` 说「以 TASK-004 在 git 检出里实跑的 N 为准」，TASK-006 `:141` 说「TASK-002 git 检出实跑数」；TASK-004 的设计与验收里没有「在 git 检出里跑套件并记数」这一步，出处应是 TASK-002。
- **证据**：`cd standards/conventions && grep -n 'cases' secret-hygiene.md` 只输出 `:316`、`:317`；`grep -nE '822|816'` 命中 `:23`、`:316`、`:352` 与版本史 `:465`；standards 先例（`191560e`、`c8ff650`、`faaede2`、`334c609`）每次都是「计数 A→B（C 无 zsh）」成对改，必要时同改括号里的测试族清单；版本史表在 1.1.2 之后没有再为计数同步加行（实查 `## 10. 版本历史`，只有 1.0.0 / 1.2.0 / 1.1.2 / 1.1.1 / 1.1.0）。
- **建议改法**：命令改成 `grep -nE '[0-9]+ (self-tests|regression cases)' …`，期望命中且只命中 `:23`、`:316`、`:352` 三行，其中每行的两个数分别等于套件头注释的两个数；把「N」拆成 `N_zsh` / `M_nozsh`（含 zsh 的数 = 无 zsh 的数 + 条件用例数，条件用例数写明怎么得到）；CHANGELOG 草稿的两个 `<N>` 改名；N 的出处统一成 TASK-002；顺便把 R1 KM-4 建议的「`:316` 括号里的测试族清单是否加 #216 / #217 两族」写成一句决定，v3.1 丢掉了这一句。

#### KM2-4　套件移植：「逐字照搬」做不到，移植副本不受变异测试覆盖
- **type**：decision　**severity**：Major　**category**：testing（兼 architecture）
- **针对**：任务计划 TASK-002 / TASK-003 / TASK-004
- **scope**：`detailed-tasks.yaml:75`、`:93`、`:97`、`:99`、`:114`；`proposal.md:648`；`sc-cases.sh:21`、`:30`、`:123`、`:126`；`run-mutants.sh`；套件 `:33`
- **摘要**：TASK-002 的设计（1）要求「搬入 `sc-cases.sh` 的全部用例，断言与期望值逐字照搬，`shim/delay-first` 与 `shapes.py` 的输入随之搬入 `tests/` 下」。这句话有两种读法：（A）把用例代码粘进 `secret-guard.test.sh`；（B）把 `sc-cases.sh`、`sc-direct.sh`、`shapes.py`、`shim/` 整体搬到 `aria/hooks/tests/`，由套件调用。按（A）字面做不到：
  - `sc-cases.sh:21` 取基线用 `git -C "$root/aria" show 59e333c:…`，这是主仓的目录结构；套件在 aria 仓里，`$root/aria` 不存在，会走到 `SETUP … exit 3`；
  - `V12-C1`（`:123`）调用 `$HERE/commentsync.py`，计划没有列这个文件要搬；
  - 输出协议是 `PASS|FAIL|SKIP <id> <detail>`，套件用的是 `pass` / `fail` / `failures[]` 计数，要改写。
  按（B）才有单一来源，但计划没有这么写。而按（A）搬出来的副本，不在任何变异测试里：TASK-004 的 W13 与 23 个坏实现（`run-evidence.sh` W13 阶段 → `run-mutants.sh` → `$HERE/sc-cases.sh`）跑的是 `v31/sc-cases.sh`，不是发版的套件；TASK-003 的设计没有说用哪个载体跑坏实现，「补用例」落在哪里也没说，交付物里只有 W14 一份文本。TASK-002 唯一的保真验收是「新套件对基线的红集与 W13 第 2 节一致」，那只检查基线方向，抓不到「搬运时把断言放松了」。
- **证据**：上述行号；套件 `HOOK="$(dirname "$0")/../secret-guard.sh"`（`:33`）没有覆盖口，对套件做坏实现测试要像 W9 那样复制整棵 `hooks/` 树再替换 hook。
- **建议改法**：采用（B），并写进 TASK-002：「把 `sc-cases.sh`、`sc-direct.sh`、`shapes.py`、`shim/`、`commentsync.py` 原样放到 `aria/hooks/tests/<子目录>/`，基线取法改为 aria 仓内的 `git show 59e333c:hooks/secret-guard.sh`（仍断言 `e83c5e30f2cc`），套件新增一节调用它并把 PASS / FAIL / SKIP 行并入计数」。这样 W13、23 个坏实现、TASK-003 都在同一份文件上跑。若坚持（A），则 TASK-004 须加一条：对移植后的用例子集逐个跑 BI-1 至 BI-23，并规定 TASK-003 的载体。

#### KM2-5　proposal 里的 hunk 计数差一
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：proposal + 证据脚本
- **scope**：`proposal.md:522`；`fill31.py:10-17`
- **摘要**：`proposal.md:522` 写「共 19 个 hunk：14 个逻辑 hunk … 5 个只改注释的 hunk」。`W8-v31.diff` 实有 18 个 hunk（`grep -c '^@@'` = 18），其中逻辑 14、只改注释 4（`@@ -86`、`-603`、`-823`、`-1528`）。`fill31.py:10` 的 `re.split(r'(?m)^(?=@@ )', …)` 在首个 `@@` 之前产生一个空串，`comment_only('')` 因 `all([])` 为真，被算成「注释 hunk」；`fill31.py:16` 的断言 `len(logic)+len(comm)==len(hunks)` 对这个多出来的块恒真，所以没拦住。数字是脚本生成的，照 PP1-A39 的做法「由脚本从 diff 计算」，却算错了。
- **证据**：`python3 -I` 复算：pieces 19、其中空串 1、真实 hunk 18、逻辑 14、注释 4。
- **建议改法**：`fill31.py` 过滤空片段再计数（`hunks = [h for h in … if h.strip()]`），重生成 proposal；或把句子改成只陈述逻辑 hunk 数。

#### KM2-6　`v31/README.md` 的复现说明与实际行为不符
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：证据 README + proposal 的「证据与复现」
- **scope**：`README.md:35`、`:37`、`:43`；`proposal.md:689`；`run-evidence.sh:17-19`、`:21`、`:26`、`:30`；`W8-v31.diff:1-2`
- **摘要**：照 README 的命令能跑通，但有六处说明与行为不符或缺失：
  1. 成功的阶段会覆盖 `v31/` 里已提交的证据。README `:35` 写的「失败或中断不会覆盖」是对的，但 `proposal.md:689` 写「不会原地覆盖已提交的证据（PP1-A39）」就说过头了——`run-evidence.sh` 每个阶段末尾都 `cp … "$HERE/"`。本席在隔离的目录里（`git init` 的空仓 + 指向真实 `aria/` 的符号链接，以便 `git rev-parse --show-toplevel` 与 `git -C $ROOT/aria show` 成立）跑了 `bash run-evidence.sh <工作目录> W8`：阶段结束后 `v31/W8-v31.diff` 被替换。
  2. `W8-v31.diff` 的头两行带着作者当时的临时目录路径（`…/scratchpad/ev31/base.sh`），重跑时换成了新的工作目录路径，所以任何复现都在已提交文件上留下两行伪差异；diff 正文逐字节相同。
  3. W13 的第五轮（bash 3.2）靠环境变量 `BASH32`：`run-evidence.sh:21` 的 `${BASH32:-}` 不设就展开成空，循环静默只跑四个 bash，不报错。README 只在 W12 处提到 `BASH32`（`:37`），TASK-004 的验收却要求「5 个 bash 上 FAIL 为 0」。
  4. 同一行写死了 `/home/dev/.aria/tools/bash-<版本>/bash` 与 `/usr/bin/bash`（`:26`、`:30`），没有存在性检查；脚本只能在 Aria 主仓的检出里运行（`git rev-parse --show-toplevel`），README 没写。
  5. README `:37` 把「抽取与复原」都指向 `2026-10-20-…/traffic/`；`extract.py` 在那里，复原用的 `refreeze.py` 在本变更自己的 `2026-10-21-…/traffic/`。三步配方（抽取、按 W0 清单复原、设 `TRAFFIC_DIR`）没写。`mkv31.py`、`fill31.py`（四个位置参数）、`commentsync.py`、`mutants.py` / `run-mutants.sh`（含 `MUT_ONLY`）都没有调用行。
  6. `run-evidence.sh:18-19` 的控制台输出是「added 183 (blank 4) removed 49」，其中 183 不含空行；proposal 写「+187 / −49，新增里 4 行空行」，187 含空行。两个数是同一件事，口径相反，TASK-004 的执行者会以为丢了 4 行。
- **建议改法**：README 加「复现命令」节，逐个脚本写参数与输出落点；W8 的头两行用固定字符串（`--- baseline` / `+++ impl`）；`run-evidence.sh` 在 `BASH32` 未设或某个 bash 不存在时直接报错退出；`proposal.md:689` 改成「失败或中断的阶段不会覆盖」；统一「added」的口径。

#### KM2-7　INV-2 的封闭清单仍漏计划自己的产出（PP1-A38 / R1 KM-14 复发）
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：任务计划
- **scope**：`detailed-tasks.yaml:31`（INV-1）、`:33`（INV-2）、`:56-62`（TASK-001）、`:93`（TASK-003）、`:108`（TASK-004）、`:127`（TASK-005）、`:160-163`（TASK-007）
- **摘要**：INV-2 列出改动面后写「其余文件不动，需要动时停下上报」。计划自己要求改或新增的这些不在清单里：TASK-001 验收要把编号「写进 proposal 与 CHANGELOG 草稿的占位」（两者都在 `proposal.md` 里）并把决定「记进本任务 notes」（路径未定）；TASK-005 的交付物是 `.aria/audit-reports/` 下的报告；TASK-007 要把 `detailed-tasks.yaml` 全部置 done、归档 change 目录、写 `docs/handoff/`、释放认领；INV-1 又授权「改 proposal」。另外 `proposal.md` 是 `fill31.py` 从 `proposal-template.md` 生成的（本席已验证逐字节可重生成），手改 `proposal.md` 会在下次生成时被冲掉，计划没说改模板再重生成。TASK-003 的交付物「由脚本生成」没有点名脚本、也没说放哪（R1 KM-14.3 已提过）。
- **建议改法**：INV-2 的清单补上 `openspec/changes/…` 下的三个文件（说明 `proposal.md` 只通过改模板再 `fill31.py` 重生成）、`.aria/audit-reports/`、`docs/handoff/`、归档目录、协调 ref；TASK-001 写明决定记在哪个 notes 文件；TASK-003 写明脚本名与位置（建议 `v31/` 下新文件）。

#### KM2-8　TASK-004 的 W8 / W9 验收措辞与事实冲突，What 6 次序未定
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：任务计划
- **scope**：`detailed-tasks.yaml:74`、`:113`、`:115`；`proposal.md:135-137`；`W9-suite.txt:6-7`、`:33-34`
- **摘要**：（1）TASK-004 的 W8 验收「`diff 原型 实现` 只出现行号漂移，没有内容差」：实现比原型多一处内容差，即 What 6 删掉的那行死代码（W8 原型不含这一删，`proposal.md:137`）；`run-evidence.sh` 的 W8 阶段产出的是 基线对实现 的 diff，不是 原型对实现，执行者得自己再生成原型。（2）W9 验收「另一个差异只能是非 git 副本里的 SC-13 计数」：SC-13 在基线（`W9-suite.txt:6-7`）与实现（`:33-34`）上以同样的消息红，它不是差异；基线到实现的差恰好是六组。（3）What 6「单独一个提交」排在原型落地之前还是之后，计划没说。排在之前，工作树里的 hook 不再等于基线，`mkv31.py` 的 sha 断言会拒绝它，「逐字落地原型」就不能整体拷贝；排在之后才顺。
- **建议改法**：W8 验收改成「实现 = 原型 − What 6 的那一行（逐行核对），行号以外无其他差」，并给出生成原型的命令；W9 验收改成「基线到实现的差恰好六组；SC-13 在两边同样红」；TASK-002 写明 What 6 最后做。

#### KM2-9　待 owner 复议的 AI 判定与关闭 #217 的动作没有载体与门
- **type**：risk　**severity**：Minor　**category**：documentation
- **针对**：任务计划
- **scope**：`detailed-tasks.yaml:8`、`:26`、`:56-62`、`:69`、`:160-168`；`proposal.md:569-574`；`standards/conventions/configured-gate-authority.md:109-113`
- **摘要**：（1）Rule #10 §5 要求 AI 任何自作主张的流程判断都写进 session handoff（「跳了什么 + 理由 + 请 owner 复议」）。本变更有：块 B 判第 1 行（`proposal.md:574`、`rule6_note` 的「AI 自作主张、待 owner 复议」）；决策 14 至 16（「已向 owner 通报，owner 可改判」，`detailed-tasks.yaml:8`）。TASK-001 的上呈清单（a 至 g）与 TASK-007 的 handoff 项都没有把它们列为必写内容；在 `.aria/decisions/`、`docs/handoff/` 里也查不到任何一条记录（grep 为空），目前只存在于聊天与 R1 汇总。（2）TASK-007 的对账评论与关闭 #217 是对外动作；TASK-001 把同类的 (g) 留言放进了 owner 门，TASK-007 却没有门，也没引 2026-09-30 决策单 §4 的一次性授权（范围是「WP-A / WP-B / WP-C 及其后续」）。（3）TASK-001 若有载体未获放行（「记为未决」），TASK-007 的验收（`:167`「转 <编号>」）就无法满足，会重演 PP1-A20（关闭后残余无载体）；计划没有「载体不全则不关 #217」的规则。（4）排序：TASK-002 依赖整个 TASK-001（`:69`），而 TASK-001 含 7 项只给 CHANGELOG 占位符与 TASK-007 对账用的上呈，代码实现被与代码无关的 owner 答复挡住。
- **建议改法**：TASK-007 的 handoff 项写明必含「块 B 分类、决策 14 至 16、自愿补上的复核」三类；TASK-001 的清单加 (h) 对账评论与关闭 #217（时点 TASK-007），或在 TASK-007 引一次性授权并说明本变更属其「后续」由谁确认；加规则「载体未获放行则 TASK-007 不关 #217，改为上呈」；把 TASK-001 拆成 001a（认领、新鲜度、建分支、重锚）与 001b（上呈），TASK-002 只依赖 001a，TASK-006 与 TASK-007 依赖 001b。

#### KM2-10　发布同步面的样板出处不准，`VERSION` 行与 standards 版本史未定
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：proposal + 任务计划
- **scope**：`proposal.md:650-651`；`detailed-tasks.yaml:142-143`、`:147-152`；主仓 `VERSION:24`
- **摘要**：`proposal.md:651` 与 TASK-006 写「以 v1.77.1 的发版提交为样板逐项列出」，并列了主仓 `VERSION`、i18n README、`CLAUDE.md` 项目状态段。v1.77.1 的主仓同步分散在三个提交：`0bd647a6`（README.md、aria gitlink、`system-architecture.md`、`version-scheme.md`）、`cf84934f`（三个 i18n README，提交信息自称「补 0bd647a 漏步」）、`09a43d54`（`CLAUDE.md` 状态覆写，随周期收尾）。三者都没有改 `VERSION`；v1.77.0 的 `ae746262` 也没改，并写明「主项目版本 1.7.5 不随插件发版 bump（惯例）」。主仓 `VERSION` 的子模块表至今仍是 `aria (插件) | v1.76.1`，三条机械检查（`m6-version-badge-match`、`i18n-readme-translation-currency`、`plugin-version-arch-docs-match`）都不看这一行。CLAUDE.md「版本管理」把主仓 `VERSION` 列为同步面，近两次发版又没做：执行者会有两种读法。R1 KM-4(a) 建议定下的「`secret-hygiene.md:316` 括号里的测试族清单是否加新族」和 standards 文档自身的版本史行，v3.1 都没提；先例里有的版本史写「计数同步（零语义变更）」（1.1.2），近四次计数同步没写。
- **建议改法**：TASK-006 把样板改成「CLAUDE.md『版本管理』的发布同步面清单（SOT）+ 三个提交的并集」，逐项列文件；明确 `VERSION` 子模块表那一行改不改（建议改，并顺手补 v1.76.1 到当前版本的欠账，或明说不改）；写一句 `:316` 族清单与 standards 版本史行的决定。

#### KM2-11　§4.4 与编号约定：三处小缺口
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：proposal + 证据 README + dispositions
- **scope**：`proposal.md:17`、`:74`、`:224`、`:542`、`:551`、`:701`；`dispositions.md:62`；`README.md:45`；`dispositions.md:113`（PP1-A31）
- **摘要**：（1）README `:45` 与 dispositions 的 PP1-A31 行（`:113`）都说 `check_bare_issue_refs.py` 对 proposal 报出的「只有 bash 取长度写法」。实跑报 5 处：4 处 `${#1}`（`proposal.md:78`、`:277` 各 2 次），另有 1 处 `proposal.md:224` 的 `#219`，那是 diff 代码块里引用的基线 hook 注释原文（存量文字，按 §4.4 执行口径不必回改），但「只有这一类」差一。（2）`proposal.md:17` 的编号约定只定义了 `R1-A*n*`、`R2-A*n*`、`PP1-A*n*`；正文还用 `KM-F-01`、`BA2-F-12`（`:74`、`:701`）、`TL2-F4`（`:542`）、`TL2-F5`（`:551`）四种席位原编号，没有定义（R1 KM-14.5 提过，建议加一句「XX-F-n = 各席原始编号」）。（3）`dispositions.md:62`（R2 节 A16 行）有两处裸号 `#228`、`#217`，正是 R1 KM-15 报过的同两处；该文件只追加不改写，所以应在 PP1 节追加一行订正或在头部声明存量豁免，而不是声称「全文写全」。主仓里裸 `#217` 指向 `10CG/Aria#217`（一张开着的无关 issue），这是 INV-6 防的同一种错。
- **建议改法**：README 与 PP1-A31 的措辞改成「4 处 `${#1}` 加 1 处引用基线注释原文的 `#219`」；编号约定补席位原编号；dispositions 追加订正行。

#### KM2-12　用例范围写法与 SC / P / BI 三表互相错位
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：proposal 的 P 表、SC 表、BI 表
- **scope**：`proposal.md:526-539`、`:598-611`、`:615-639`
- **摘要**：用脚本把三张表展开后与 `sc-cases.sh` 的输出比对（`xref.py`、`sc_bi.py`、`p_sc.py`）：（1）SC-V2 的 `V2-G1`–`V2-G11` 含不存在的 `V2-G9`、`V2-G10`（真实编号是 `V3-G9`、`V3-G10`，列在 SC-V3）；（2）P5 的证据列漏了 `V5-S13`（SC-V5 有）；（3）SC 行的「必须抓住的坏实现」与 BI 表的「指定用例」交叉：SC-V1 要求抓 BI-8，BI-8 的指定用例只有 `V9-E12`（属 SC-V9），SC-V1 的任何用例在 W13 里都不抓它；SC-V3 要求抓 BI-4、SC-V5 要求抓 BI-2，两者的指定用例含 `V6-E2`（属 SC-V6），SC-V3 的各用例对 BI-4 只是「连带变红」，按 PP1-A7 自己的口径（无关断言碰红不算抓住）不能算；BI-11 的指定用例横跨 SC-V10 与 SC-V11。
- **建议改法**：范围改写成逐个列出或改成真实编号；SC 表的「必须抓住」列改成「该 SC 行自己的用例会红的 BI」，与 BI 表指定用例对齐，或在 BI 表加一列「所属 SC」。

#### KM2-13　CHANGELOG 草稿：占位符重名、一处不准的表述
- **type**：issue　**severity**：Minor　**category**：documentation
- **针对**：proposal 的 CHANGELOG 草稿
- **scope**：`proposal.md:654-671`（`:664`、`:666`、`:668`）；`W11-adversarial.txt:6`
- **摘要**：（1）占位符重名但含义不同：`<N>` 出现两次（`:664` 是 W12 放行条数，`:668` 是测试条数），`<carrier>` 两次（`:666` 一个是「≤ 8192 判定可超 5 s」的载体，一个是 count 轴小命令一侧的载体），`<issue>` 两次（for 列表、heredoc 误收集）。TASK-006 `:141` 只用文字区分，执笔席容易填成同一个值。（2）「但要等到截止（约 3 s；以前不到 1 s 就拦）」：W11 里基线 `apply-heavy-cjk` 是 1.97 s（`W11-adversarial.txt:6`），不到 1 s 只对 `f5like`（0.74 s）等成立；R1 KM-10.4 引的是 0.77 与 2.02 两个数。（3）「测试：`secret-guard.test.sh` `<N>` 例」没说含不含 zsh（v1.76.1 的先例写「825（无 zsh）」）。Rule #6 一行见 KM2-1。
- **建议改法**：占位符改名（`<N_allow>`、`<N_cases_nozsh>`、`<carrier_8192>`、`<carrier_count>`、`<issue_for>`、`<issue_heredoc>`）；「以前不到 1 s」改「以前通常 2 s 以内」；测试数写明口径。

#### KM2-14　What 7 的表与 commentsync 的块范围不一致（PP1-A18 残余）
- **type**：risk　**severity**：Minor　**category**：documentation
- **针对**：proposal 与验收（`commentsync.py`）
- **scope**：`proposal.md:145-170`；`commentsync.py:31-58`；基线套件 `:2578`、`:2628-2630`、`:2679-2680`、`:5-7`
- **摘要**：`commentsync.py` 的「块」是基线里一串连续的 `#` 注释行（被代码行或空行打断就换一块）。把 `proposal.md` 表里的「位置（基线）」与实际块范围逐个比对：站点 3、4、5、6、7、9、10、11、13 与标题 16 至 20 对得上；站点 1（实际是 2 至 163 的整个头注释）、2（实际 571 至 590）、8（实际 1526 至 1536）的块比表里写的大——安全；站点 12（表 `:2578-2585`，实际块只有 `:2585` 一行）、14（表 `:2628-2632`，实际只有 `:2632`）、15（表 `:2679-2681`，实际只有 `:2681`）的块比表里写的小——`:2578`（21ag 的形状说明）、`:2628-2630`（21al 的「the copy limit holds for the braced form too … exactly 8192」）、`:2679`（21ao 的「obeys the same copy limit …」）不在任何被追踪的块里，而后两处在新语义下（8192 与 8193 两侧都完整判定，边界只剩 `longline` 的行长界）已经失实。执笔席照表里的行范围改写则覆盖得到，只改被追踪的那一行 `commentsync` 也是绿的。另外套件头注释 `Expects: … python3 … used only by the #128 SC-20 … no other case depends on it`（`:5-7`）在移植后（`shapes.py`、`commentsync.py` 要 python3）会失实，不在清单里。
- **建议改法**：表里的「位置」列改成与工具一致的块范围，并把 `:2578`、`:2628-2630`、`:2679-2680` 与头注释 `Expects` 段加入追踪（给出各自的 sha256 前缀）；或在 TASK-005 的验收里写明审查这几处。

#### KM2-15　INV-7 没有停止规则，INV-8 的作废规则漏了 W14
- **type**：risk　**severity**：Minor　**category**：architecture
- **针对**：任务计划
- **scope**：`detailed-tasks.yaml:43`、`:45`；`proposal.md:44`；`W12-real-traffic.txt` 首行与末行
- **摘要**：（1）INV-7 要求 W12 第 1 节在一分钟负载低于 2 时跑，「任一读数 ≥ 2 即作废重跑」，没有重试上限或兜底。本席开工时这台宿主的负载是 10.22 / 8.14 / 5.97；原型作者自己的 W12 一轮也是 2.18 起、3.49 止（proposal `:44` 已承认高于门槛）。门槛本身继承自 WP-A，但没有「重试 K 次仍不满足就上呈 owner」的出口，执行者要么无限等，要么违规。（2）INV-8 的作废对象写成「TASK-004 或 TASK-005 之后 hook 只要再改一个字节，两者都作废」：TASK-003 的 W14 也记 hook sha256，却不在作废清单里；「之后」既可读作「完成后」也可读作「期间」。
- **建议改法**：INV-7 加「同一窗口最多重试 3 次，仍不满足则记录负载并上呈」；INV-8 把 W14 列入，并写明「TASK-003 完成之后 hook 的任何改动」。

#### KM2-16　证据可追溯性缺口
- **type**：risk　**severity**：Minor　**category**：documentation
- **针对**：proposal + 证据
- **scope**：`proposal.md:528`、`:571`、`:600`、`:708`；`W9-suite.txt:2`；`sc-cases.sh:30`；`detailed-tasks.yaml:59`、`:69`、`:91`、`:78`
- **摘要**：（1）决策 14 与 owner 段（`:571`、`:708`）写「计数触顶即回落：真实流量收益 137 → 73」，出处只有 R1 汇总里的一行（`post_planning-R1-…-aggregated.md:98`），`v31/` 里没有脚本也没有输出；owner 被告知可以改判，却复现不了这组对比。（2）P1 与 SC-V1 说「旧套件在实现上恰好 6 组变化」（`:528`、`:600`），这是在非 git 副本上测得的（`W9-suite.txt:2` 自己写明）：SC-8（性能基准，经 `git show af87cae` 取旧侧，并从新 hook 里按锚点抽出 `_sg_judge_one` 与 `_sg_per_segment_eval`，也就是原型改动的函数）、SC-9a、含 zsh 的条件用例没有跑；正文没限定，首次覆盖是 TASK-002 的 git 检出全量。本席没有跑它们（未核实）。（3）W13 每一行的 `SKIP 0` 是空转：`sc-cases.sh` 里没有任何路径发 `SKIP`（`:30` 只有计数器），dispositions PP1-A13 与 TASK-002 `:78` 的「SKIP 单独计数」针对的是依赖 locale 的用例，而被移植的集合里没有（填充全是 ASCII）。（4）TASK-001 `:59`、TASK-002 `:69`、TASK-003 `:91` 把 `stale-local-main`、`fix-writer-bottleneck`、`adversarial-fixture` 三个 memory 名当依据；memory 库在容器本地，不在仓里（`feedback_memory_store_is_container_local_not_shared`），换容器的执笔席读不到。各处也有就地说明，所以只算 Minor。
- **建议改法**：决策 14 的对比脚本与输出放进 `v31/`（或在文字里写明出处是 R1 汇总第 98 行）；P1 / SC-V1 加限定「非 git 副本，SC-8、SC-9a 与 zsh 条件用例未覆盖」；`SKIP` 要么用起来（见 KM2-2），要么 W13 里删掉这一列；memory 名换成就地一句话理由。

## 变异测试

本席以文档与流程为主，只构造了一组「文字钉住与否」的坏实现，验证 `rule6_note` 块 B 的替代物主张；它们是对测试的变异测试，目的是证明测试能抓住错误，坏实现只存在于 scratch 目录。每个坏实现 = v3.1 原型 + 一处改动，先写下预期再跑。

| 坏实现 | 改动 | 预期 | 实际 |
|---|---|---|---|
| KM-M1 | `longline` 首段末尾插入一句处方句（含 `guard:ack` 提示） | 没有用例抓住：`V11-S3` 只比较 `Split it…` 之后的指令行，`V7-E14` 等只 grep 一个短语 | 未抓住（并入 M123 的全量：0 红） |
| KM-M2 | 整串增长原因串改回基线措辞 | 没有用例抓住：`V8-D*` 只看返回码，没有端到端用例期望 `growth` | 未抓住（并入 M123） |
| KM-M3 | 分段增长原因串改回基线措辞 | 同上（`sc-cases.sh` 层面；旧套件 21ag / 21aj 改写后才会钉住） | 未抓住（并入 M123） |
| KM-M123 | 上三处合并 | 全绿 | 全量 PASS 94 / FAIL 0 / SKIP 0（`sc-km-m123.out`） |
| KM-M4 | `longline` 指令行改一个字（`Edit` → `Edits`） | `V11-S3` 转红 | `V11-S3` 红，符合预期；同轮 `V7-E13` 因宿主高负载回落而红，与此改动无关（见 KM2-2） |
| KM-M6 | `longline` 中文行前半句加处方分句，保留共用收尾 | 没有用例抓住 | `V11-S3` 仍绿，未抓住；同轮另有 `V7-E1`、`V7-E13` 两条红，同样是高负载所致 |

KM-M4、KM-M6 用 `SC_ONLY='^V11|^V7|^V10'` 过滤报告，静态用例 `V11-S3` 不受过滤影响。对应 finding：KM2-1（M1 至 M3、M6 未抓住即缺口），M4 说明对指令行「改一个字即红」的主张成立。

另外，本席在未改动的原型上重复跑 `V7-E1` / `V7-E13`（3 次）与全量（1 次），得到 KM2-2 的数据——这些不是坏实现，是好实现在高负载下的假红。

## Verdict

0 Critical + 4 Major + 12 Minor → **PASS_WITH_WARNINGS**。

本席没有发现会造成安全退化或让计划做不出来的问题。4 个 Major 都是「声称有而实际没有」：KM2-1 与 KM2-3 是 R1 簇（PP1-A19、PP1-A23）的修复不彻底或引入新缺陷，KM2-2 是 R1 的 PP1-A5（计时判据）修复后留下的假红面，KM2-4 是 TASK-002 把验收搬进套件这一步的保真问题。建议下一版一并吸收，其中 KM2-1 至 KM2-3 各自只需改文字加一两个用例，改动小。

## 轮次记录

- **读了**：任务书；`detailed-tasks.yaml` 全文；`proposal.md` 全部 724 行；`dispositions.md`；`v31/README.md`、`sc-cases.sh`、`sc-direct.sh`、`shapes.py`、`shim/`、`run-evidence.sh`、`fill31.py`、`commentsync.py`、`run-mutants.sh` 与 `mutants.py` 头部、`build-bash.sh`；`W9`、`W11`、`W12`（含 TSV）、`W13` 证据文件与 `W8-v31.diff` 的计数；`evidence/W1`、`W-summary.txt`、E12；R1 汇总全文与本席 R1 报告全文；`skill-benchmark-exemption.md` 全文；WP-A `proposal.md` 的 `rule6_note` 节与相关行；`content-integrity.md` §4.4；`configured-gate-authority.md` §5；`version-management.md` §2；2026-09-30 决策单 §4；`post_spec-R2-…-aggregated.md` 的 Owner 裁定；`.aria/config.json` 的 audit 段；`.aria/state-checks.yaml` 的版本类检查；aria `CHANGELOG.md` 的 v1.76.1 与 WP-A 条目；主仓 `0bd647a6`、`cf84934f`、`ae746262`、`878f8d99` 的文件清单；standards `191560e` 与 `secret-hygiene.md` 的计数行；基线套件的 SC-8 / SC-9a / SC-13 段与 What 7 各站点周边注释。
- **跑了**（全在 scratch，`taskset -c 0,1 nice -n 19`；起始负载见 KM2-2）：`mkv31.py`（得 `9f61db0e7b8b`）；`fill31.py` 重生成 proposal 并 `cmp`；`commentsync.py` 的 baseline、`--hook-only target`、全量 target（基线套件，预期 RED 22）三种；`sc-cases.sh <原型>` 全量 3 次（7.40 起 PASS 94；高负载 17.46 起 PASS 86 / FAIL 8；另有组合坏实现一轮 PASS 94）；`V7-E1` / `V7-E13` 子集 3 次；KM-M4、KM-M6 的子集各 1 次；`check_bare_issue_refs.py` 对五个文件；INV-6 的 grep 对 16 个样例消息；`run-evidence.sh W8` 在隔离的假仓里 1 次；`xref.py`、`sc_bi.py`、`p_sc.py` 三个交叉核对脚本；hunk 计数、行号核对、`lib/detailed_tasks.py` 解析、依赖图拓扑检查。
- **没读**：同轮其他席位的报告；真实命令语料；`W9`、`W12`、`W13` 全量的输出（只读了已提交的证据文件）。
- **没跑 / 未核实**：旧套件在原型上的 SC-8（性能上限）、SC-9a 与含 zsh 的条件用例（W9 是非 git 副本，没有覆盖；本席按任务书没有跑整套件）；`sc-cases.sh` 在 bash 5.0 / 5.1 / 5.3 / 3.2 上的各一轮（只跑了 5.2）；W12 的语料复原与 `BASH32` 路径；`build-bash.sh` 的构建（只确认了四个二进制存在且版本、MACHTYPE 与文档一致）；Forgejo 是否对跨仓关闭关键词生效（INV-6 自己也写「未核实」，需要写操作）；INV-6 的 grep 对 PR 正文的使用方式（计划没给命令，本席只验证了对提交信息样例的行为：`Closes 10CG/aria-plugin#217` 等命中，`Refs …`、`fix(scope): …` 不命中，`Reopens …` 与关键词在行尾而编号在下一行的写法不命中）；standards 文档版本史行是否必须随计数同步而升（只按先例推断）；KM2-2 的数字是在宿主负载异常高、且有其他席位同时运行时取得的，不代表 CI 或发版机器。
- **工具调用**：约 110 次（含 1 次误用 `find /` 后立即用 TaskStop 中止、2 次因宿主高负载被转入后台的命令；没有使用 `pkill` 或按模式批量 kill，收尾时按精确进程名与参数核对没有残留 stub 进程；没有改仓内任何文件，除本报告外无新增）。
