---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-22T19:55:00.000Z
context: openspec/changes/secret-guard-w10-failclosed-narrowing/detailed-tasks.yaml
agents: [qa-engineer, code-reviewer, tech-lead, backend-architect, knowledge-manager]
---

# post_planning R2 汇总 — secret-guard-w10-failclosed-narrowing（10CG/aria-plugin#217；任务计划与 proposal v3.1 @ `95cf1de7`，v3.1 原型与可执行验收）

> **Verdict：PASS_WITH_WARNINGS**。去重后 0 Critical / 20 Major / 24 Minor（44 簇，原始 82 条）。五席都是 PASS_WITH_WARNINGS，都有 Major，按 REVISE 计。未收敛。**停止规则触发**：Major 簇数从 23 降到 20，但其中 18 个落在 v3.1 新写的表面上，超过一半。按约定不再加轮，上报 owner（见「主控处置建议」）。
>
> 本文件是有损汇总。每个簇都回链到席位原编号：CR = code-reviewer（F*n*，下文写作 CR-F*n*），QA = qa-engineer（QA-*n*），TL = tech-lead（TL2-*n*），BA = backend-architect（BA2-F*n*），KM = knowledge-manager（KM2-*n*）；括号里是该席的定级（M = Major，m = Minor）。各席自己构造的坏实现保留原编号并加席位前缀：CR-MA–ME、QA-M01–M30、TL-M1–M10、BA-M1–M14。细节以各席报告为准（同目录、同时间戳 `1792689337848` 的五份文件）。簇号写作 PP2-*x*（Major）与 PP2-m*n*（Minor）；PP1-A*n* 是 R1 的簇号。

## 一句话

v3.1 原型的机制，第 2 轮五个全新席位都没有找到缺陷；加上第 1 轮，十个席位都没有证伪它。Decision 14–16 的技术挑战无异议。20 个 Major 簇的分布：

1. **可执行验收**（PP2-A–M，13 簇）：用例在负载下对好实现假红，且没有守住放宽重跑里的放行方向分支。五席非作者坏实现 60 个，漏网 46 个；按行为去重后约 21 类，其中 12 类会造成放行，8 类在 hook 级实测放行。这些放行都来自坏实现，原型在全部定向输入上与基线一致。
2. **计划文字**（PP2-N–R、PP2-T，6 簇）：W8 判据与 What 6 互相矛盾；TASK-004 会覆盖自己要对照的证据；移植进套件的用例从不在坏实现上跑；对外动作的 owner 门不全；standards 计数的核对命令命不中；Rule #6 块 B 声称的逐字断言不存在。
3. **放宽面申报**（PP2-S，1 簇）：两类既有 W10 缺口（重复赋值时取了第一个值；分段模式下变量值里的元字符被代入成语法）随放宽覆盖到大命令，申报里只有一句通用句，没有点名，也没有载体。

## 停止规则判定

约定（R1 汇总「成本与收敛距离」）：下一轮换全新席位；若 Major 簇数没有降到 23 以下，**或**本轮修订引入的 Major 占比超过一半，就不再加轮，按「实现优先」上报 owner。

| 条件 | 本轮 | 判定 |
|---|---|---|
| Major 簇数降到 23 以下 | 20 | 满足 |
| 本轮修订引入的 Major ≤ 1/2 | 落在 v3.1 新写的表面上（新脚本、新用例、新计划条款与新声明）：18 / 20，只有 PP2-Q（PP1-A22 未收口）与 PP2-S（v3 就有）不是。只算「新代码与新文字自身的缺陷」，不算覆盖缺口：11 / 20（A、B、C、K、L、M、N、O、P、R、T） | 两种算法都超过一半，**不满足** |

结论：不再加第 3 轮，上报 owner，选项含「实现优先」。

成因：「验收写成代码」把 R1 的散文欠定变成了能跑、能证伪的代码，这一步是有效的：R2 的每一条 Major 都有可复跑的证据，四席逐条实测。但用例集仍是作者自己想出来的，与 R1 汇总预料的同源盲区一样：作者的 23 个坏实现全部被抓住，非作者的 60 个漏网 46 个。再加一轮，审的会是新补的用例，那是新表面，Major 还会落在它上面。

## 审计结论

### Major（按 {category, scope} 去重）

| 簇 | 级别 | type | category | scope | 摘要 | 席位回链 |
|---|---|---|---|---|---|---|
| PP2-A | Major | issue | testing | `sc-cases.sh` 的窗口类用例与「重跑须在截止前跑完」类用例；`sc-direct.sh:65` 的 `run()`；INV-7「`sc-cases.sh` 的计时判据不受本条约束」；`v31/README.md`「与负载无关」；TASK-003 耗时矩阵；TASK-004「W13 FAIL 为 0」 | 下界由 shim 的固定延迟给出，确实与负载无关；上界与放行类、判定类用例依赖自然速度。负载 8–12 下，未改动的原型红 1–4 条（`V9-E11`、`V3-E3`、`V3-E5`、`V6-E2`、`V2-E7`）。`run()` 先取锚点、再 `mktemp`、后起秒表，负载下 `V3-S4` 量出 0.84 s（下界 0.85）。INV-7 把 `sc-cases.sh` 排除在负载门外，TASK-004 的「FAIL 为 0」在共享宿主上不可重复；按 TASK-002 逐字搬进套件后，日常套件里就有了时红时绿的用例 | CR-F1(M) QA-1(M) BA2-F13(M) KM2-2(M) TL2-10c(m)；复发 PP1-A5（未收口）、PP1-A29、PP1-A36 |
| PP2-B | Major | issue | testing | `shim/delay-first`（`sed` 首次调用停 10 s）；`deadline()` 类用例 | 垫片假定「第一次 `sed` 调用在作业里」。作业在写出第一份文案前被截止切掉，或准入门因时间不够而关闭时，10 s 停顿落进父进程的回落文案，墙钟 11–12 s，常撞上 `timeout 12` 得 rc=124：行为正确的回落被报成红，且与真实的越界签名分不开。把 `_sg_redact_echo` 换成纯 bash、提前渲染回落文案之类的合法重构，也会让垫片停错地方或不触发 | CR-F1(M) QA-2(M) BA2-F13(M)；复发 PP1-A8（部分） |
| PP2-C | Major | issue | testing | `sc-cases.sh:85` `V3-E5`（`SECRET_GUARD_TIME_BUDGET_S=1`）；原型 `_sg_over_budget` | 预算取 1 时，`$SECONDS` 的整秒翻转只要落在「收集重置时钟」与「首遍第一个检查点」之间，首遍就自己写出时间文案，与基线臂（默认预算）的「过大」字节不同，好实现间歇假红（QA 撞见两次；TL 推算） | QA-3(M) TL2-10a(m) |
| PP2-D | Major | issue | testing | SC-V2；原型 `:769`（分段触发点 `if _sg_relax_ok`）、`:824`（`_sg_relax_noext` 经 `_sg_ext_root`） | 准入门有两条入口没有用例：分段触发点是否真的问准入门（CR-MA、QA-M02 全绿）；项目根只由 stdin `cwd` 给出（QA-M01、TL-M8、BA-M1 全绿）。M01 一类三席各自在 hook 级复现了放行：读取扩展清单所列路径的大命令，基线与原型都拦、坏实现放行（主控重跑 QA 的演示核实） | CR-F2(M) QA-5(M) BA2-F1(M) TL2-11(m)；PP1-A27 同族 |
| PP2-E | Major | issue | testing | 原型 `:723`、`:734`、`:757`：重跑内三个协作式时间检查点；SC-V4 | 契约是「返回 3、不写文案，由回落写基线字节」。改成 `return 0`（QA-M06–M08，放行方向），或删掉（BA-M8、TL-M5：写出时间文案并返回 2），整轮都全绿；`V4-S7` 只桩掉 `_sg_vx_pass` 本身，钉的是作业对 3 的映射，不是这三行。默认预算 3 时，协作式检查点在多数相位下先于硬截止触发，是慢重跑的常规出口 | QA-4(M) BA2-F6(M) TL2-10d(m) |
| PP2-F | Major | issue | testing | SC-V7 / SC-V10、P7 / P10（裁定 C）；原型 `_sg_judge_one`（`:1636-1650`）、整串 `:750`、分段 `:778`、`_sg_vx_big_judge`（`:797-799`） | 裁定 C（代入后有超长单行又命中规则：不评估脱敏过滤，直接拦）没有一条带过滤器的用例；唯一的分段模式 e2e 不含读取。漏网而在「超长行 + 过滤器」上放行的：先算 credit（CR-MC、BA-M4）、整串分支漏 `return $?`（TL-M2）、分段不路由到 `_sg_vx_big_judge`（CR-MD、QA-M10、TL-M3、BA-M11）、量行长的 `read` 漏 `IFS=`（QA-M28、TL-M4）。另有边界 `>` 写成 `>=`（QA-M13、TL-M9、BA-M6）与「量不出行长」哨兵（QA-M14、BA-M3）无用例 | CR-F4(M) QA-6(M) QA-7(M) TL2-2(M) BA2-F2(M) BA2-F9(m) BA2-F10(m)；PP1-A10 部分 |
| PP2-G | Major | issue | testing | SC-V8 / P8；原型 `:742`（整串）、`:766`（分段）的增长超限 | 重跑里「增长 > 8192 仍拦」只有 `_sg_vx_apply` 返回码的用例，通过层与 e2e 都没有；`kind()` 的 `growth` 从未被任何用例期望。改成放行（QA-M17 / M18、BA-M9 / M10）全绿，整串一侧 hook 级放行（主控重跑 QA-M18 核实）。P8 的证据列指向 W9 的 21ag / 21aj，那两例是分段文案，整串增长文案没有旧例 | QA-6(M) BA2-F3(M) |

| PP2-H | Major | issue | testing | SC-V9 / P9；原型 `:643`（`cf`）、`:727`（重跑内 VMAX 分支） | Decision 14 新造的可达路径没有用例：重跑仍收 8 个 for（CR-MB、QA-M12、TL-M1，三席各自全绿；CR-MB 与 TL-M1 在 hook 级放行「经第 9 个 for 的凭据读取」，主控重跑 CR 探针核实）；重跑内第 17 个赋值超过 4096 被忽略（QA-M24，放行）；三个常量同为 8192，用错常量名不可观察（QA-M29）。BI-17 一次撤掉三处放宽，抓不住「只漏一处」 | CR-F3(M) QA-7(M) TL2-1(M)；PP1-A1 同轴、PP1-A6 |
| PP2-I | Major | issue | testing | P6 / SC-V6；原型 `:769` 分段触发点保存的原因串 | P6（回落与基线逐字节相同）只在整串模式验证过。分段触发点存成整串那条原因串（QA-M09、BA-M5）全绿；BA 用桩把 `_sg_relax_run` 换成 `return 4` 做出确定性复现（stderr sha 与基线不同），QA 的直调探针 S1 同向 | QA-6(M) BA2-F4(M) |
| PP2-J | Major | issue | testing | `_sg_relax_job` 的组长自检（P5；What 3「`set -m` 不生效的 bash 由此安全退化」） | 五个 bash 上 `set -m` 都生效，自检的拒绝分支从不执行。只去掉自检（BA-M7）全绿；直调：在非组长 shell 里，原型返回 9（拒绝判定），坏实现返回 77（放行），计时器打向不存在的组，截止形同虚设（主控重跑核实）。BI-2 同时去掉 `set -m` 与自检，抓到的是「杀不到组」 | BA2-F5(M) |
| PP2-K | Major | issue | testing | `sc-direct.sh:80-81`、`:108-110`（`V5-S13b`、`V5-S12`） | 「没有残留进程」按全机 `ps -eo args` 匹配固定参数，且在异步 SIGKILL 之后立刻观察。同机另一份运行的同名桩会被数进来（QA、TL 各自实测；本轮几席并发时多次撞见），隔离运行也有约 1/150 的纯竞态假红（BA `flake.sh`） | BA2-F7(M) QA-9(m) TL2-9(m) CR-F8(m) |
| PP2-L | Major | issue | testing | `sc-cases.sh:16`、`:25`、`:41`、`:126-127` | 环境不对时整轮空转成绿：`SC_BASH` 指向不存在的文件，九条 e2e 全 `PASS … rc=127 … IDENTICAL`，`PASS 9 FAIL 0`，退出 0；`sc-direct.sh` 一启动就崩，直调用例整体消失，仍 `FAIL 0`、退出 0（主控重跑核实）。没有金丝雀，也没有「应出现的用例编号」断言 | QA-8(M) |
| PP2-M | Major | issue | testing | `v31/commentsync.py` 的 target 模式；`V12-C1`；TASK-002 验收「commentsync target 为 GREEN」 | target 的「旧块哈希一个不剩」是「锚点 0 次」的推论：在 13 处锚点各插一个字符、再加一行含全部 ADD 词的注释，未改动的基线 hook 即 GREEN（主控重跑核实）；整块删掉一段注释也 GREEN。套件一侧的 7 块注释与 5 个标题不在原型里，验收只有它加人工审读 | CR-F5(M) QA-12(m) KM2-14(m)；复发 PP1-A18 |
| PP2-N | Major | issue | implementation | INV-1（`detailed-tasks.yaml:31`）、TASK-002 What 6（`:74`）、TASK-004 W8 验收（`:113`）；proposal What 6 | What 6 删的 `[[ -z "${_SGV_V[j]}" ]] && continue` 仍在原型里（`v31.sh:675`），「实现相对原型只有行号漂移」在正确实现上必红；INV-1 没有为 What 6 留例外。执行者只能违反验收，或临场认定「What 6 不算」，后者正是 Rule #10 说的临场豁免。B.1 时 aria `hooks/` 与基线零差异，连「行号漂移」的前提也不成立 | CR-F6(M) TL2-4(M) KM2-8(m)；PP1-A38 延伸 |
| PP2-O | Major | issue | testing | INV-2（`:33`）、INV-8（`:45`）、TASK-004（`:108-118`）；`run-evidence.sh:5`、`:19`、`:31`、`:39`、`:52`、`:69` | `run-evidence.sh` 每段成功后把 W* 复制回 `v31/`，原型那一轮的证据被覆盖，而 TASK-004 的四条验收都要与它对照：只拿工作树里的文件比，就成了实现那一轮自己比自己。头注释「never overwrites committed evidence」只在失败时成立。另外 INV-2 只许新文件，与 TASK-004 交付「`v31/` 下的新版本」冲突；W8 阶段不写页眉；页眉不绑定 `sc-cases.sh`、`sc-direct.sh`、`mutants.py` 的哈希 | TL2-5(M) CR-F15(m) KM2-6(m)；复发 PP1-A16、PP1-A39 |
| PP2-P | Major | issue | testing | TASK-002（`:75`、`:80-84`）、TASK-003（`:93-100`）、TASK-004（`:111-114`） | 坏实现只在 `v31/sc-cases.sh` 上跑，搬进 `secret-guard.test.sh` 的那一份从不在坏实现上跑；TASK-002 对移植的唯一检查是「基线红集与 W13 第 2 节一致」，而基线上新函数根本不存在，移植时被削弱的用例照样红。留在仓里守护后续改动的是套件。TASK-003 补的用例落在套件还是 `sc-cases.sh`，计划没定。「搬入…逐字照搬」还有两种读法，且字面做不到（`sc-cases.sh` 的 e2e 依赖 `v31/` 下的 shim 与 shapes） | TL2-6(M) KM2-4(M)；PP1-A7 延伸 |
| PP2-Q | Major | issue | documentation | TASK-001 清单 (a)–(g)（`:61`）、TASK-006（`:140-147`）、TASK-007（`:161-162`）、INV-6 | 对外动作的上呈不全：aria 与主仓的 feature 分支推送、开 PR、TASK-007 在 `10CG/aria-plugin#217` 上的对账评论与经 API 关闭、证据提交走哪条推送路径、TASK-007 依赖 owner 亲手更新插件缓存并重启，都没有 owner 门。WP-A 先例（`openspec/changes/secret-net-l3-and-bypass-paths/proposal.md:12`）分「一次性授权四类」与「逐次请示五类」 | TL2-7(M) KM2-9(m)；复发 PP1-A22（部分） |
| PP2-R | Major | issue | documentation | TASK-006（`:141`、`:148`）；proposal CHANGELOG 草稿（`:664`、`:668`）；standards `conventions/secret-hygiene.md:23`、`:316`、`:317`、`:352` | 验收命令 `grep -n 'cases' …` 只命中 `:316`，外加 secret-scan 的 `:317`（129 例），命不中 `:23` 与 `:352` 的「822 self-test」；`:23`、`:316` 还各有第二个数（无 zsh）。照字面执行，要么因 129 ≠ N 恒红，要么只核到一处。CHANGELOG 草稿的 `<N>` 同时指放行条数与测试例数，`<carrier>`、`<issue>` 也各重名两次（主控核实 `<N>`） | TL2-8(M) KM2-3(M) KM2-13(m)；PP1-A23 的修法不生效 |
| PP2-S | Major | issue | architecture | R-a（`proposal.md:541`）、CHANGELOG 放宽面申报（`:665`）、残余 1–7（`:548-556`）、hook 头注释的 W10 缺口清单（原型 `:87-97`） | 两类既有 W10 缺口没有点名，也没有载体：1. 同名变量重复赋值时，代入用第一个值，bash 读的是后一个；2. 分段模式下，值里的元字符代入后成了语法，读取段因此得到 credit，而 bash 里它们只是参数。两类在小命令上基线同样放行；在大命令上基线按尺寸拦，v3.1 放行。主控重跑：`reassign-big`、`reassign-big-multiline` 基线 2 / 过大、原型 **0**；`seg-splice-big` 在负载约 12 时两边都回落为过大，未复现（TL 在低负载实测原型 0）。R-a 只有一句通用的「判定语义上的既有缺口覆盖到更多大命令」，点名的 `10CG/aria-plugin#138`–`10CG/aria-plugin#142`、`10CG/aria-plugin#229` 的标题都不是这两类（主控经 API 查过） | TL2-3(M；TL 注：若通用句不算申报，应升 Critical)；PP1-A20 延伸 |
| PP2-T | Major | issue | testing | `rule6_note` 块 B（`detailed-tasks.yaml:19-26`）；proposal `:574`、CHANGELOG `:652`、`:667`；`sc-cases.sh:115-118`（`V11-S3`） | 块 B 声称 substitute 是「`V11-S3`（指令行逐字相同）+ SC-V7 / SC-V8 的逐字断言」。`V11-S3` 存在；后者不存在：用例只按子串 `has a line longer than`、`grows by more than` 判文案类别，`longline` 描述句与两条增长原因串都没有逐字断言（主控读行核实）。三处文本改动合并的坏实现整轮 94 / 94 全绿（KM 实测）。块 B 自己又落在 SOT §2 的「拿不准」格，处置应是照跑，或走第 3 行三件套，而不是「先豁免、待 owner 复议」；CHANGELOG 里的「待 owner 复议」会随发版留在用户可见的文字里 | KM2-1(M) TL2-14(m)；复发 PP1-A19 |

### Minor

| 簇 | type | category | scope | 摘要 | 席位回链 |
|---|---|---|---|---|---|
| PP2-m1 | issue | testing | `sc-cases.sh:70` `deadline()` | 非放宽的 bash 上丢掉了附加的环境变量：3.2 那一轮里 `V2-E6`、`V3-E4`、`V3-E5` 名不副实，只是 `V6-E2` 的重复；`outcome()` 同一分支会传 `"$@"`，两处不一致（主控核实） | CR-F7 |
| PP2-m2 | risk | testing | `sc-direct.sh` `V5-S10` / `V5-S10b` / `V5-S10c`；`run-mutants.sh` | `ulimit -u 1` 对 uid 0 与 CAP_SYS_RESOURCE 不生效，root 下好实现恒红，且没有探测与 SKIP；按字面文本注入计时器，文本一变输出 `SETUP`，`run-mutants.sh` 把它当作「抓住」 | CR-F8 QA-10 BA2-F18 |
| PP2-m3 | issue | documentation | `fill31.py:10-17`；proposal `:522` | 「每个 hunk 要么被引用、要么只改注释」的断言恒真；`re.split` 的首个空串被算成一个 hunk，W8 实为 18 个 `@@`（14 逻辑 + 4 纯注释），proposal 写成 19 与 5；heredoc 里以 `#` 开头的行会被当成注释（主控核实计数与恒真） | CR-F9 KM2-5 |
| PP2-m4 | issue | documentation | 原型 `:576-578`（W10 块头）、`:626`（`_sg_vx_replace`） | 两块注释仍写「at most 16 assignments and 8 replacements」「at most 8 replacements」，重跑里这些上限已取消；不在 What 7 的封闭清单里，会原样发出去（主控核实） | CR-F10 |
| PP2-m5 | issue | documentation | proposal `:40`（引 W1）、`:41`（引 W12） | W1 的增长是在基线计数上限下测的；v3.1 重跑不设上限，n=1053 的增长超过 8192，在 W12 落入 growth。两行并列而没有解释 | CR-F11 |
| PP2-m6 | risk | architecture | What 3 的耗时上界与 ε；回落路径 | 截止之后父进程还要收尾命令替换、fork `sed`、写文案；负载约 10 时 ε 实测 0.2–1.2 s，hook 启动之前的时间不在上界里，离 Claude Code 的 5 s 余量约 0.9–2 s。建议在启动作业前预算好回落文案，并把「ε 随负载增长」写进已知限制 | CR-F12 BA2-F19 |
| PP2-m7 | decision | documentation | Decision 16、What 1、CHANGELOG「放宽条件」；`sc-direct.sh:24` | `*-linux-gnu*` 判的是 bash 的构建三元组：放进了未实测的 aarch64 / armhf，以及 WSL1 / WSL2、gVisor 这类内核没实测过的环境；`V2-G2` 却把 aarch64 钉成「放宽」。自检不验证整组 kill 真的生效。建议写明「实测 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20，x86_64」，WSL 是否算在内要写明；「探测出错按有扩展处理」有两种读法 | CR-F13 TL2-13 BA2-F16 |
| PP2-m8 | issue | testing | `V2-G3b`、`V2-E8` 的平台毒化 | 只毒 `OSTYPE`；`MACHTYPE`、`HOSTTYPE` 同样能由环境改写，把平台实参换成 `$MACHTYPE` 的坏实现（QA-M04、BA-M14）全绿 | QA-11 BA2-F11 |
| PP2-m9 | issue | testing | `V7-E15`（`sc-cases.sh:98-104`） | 判据「放行，或与基线字节相同」，一个永远回落的实现也能过，测不出「多行副本照常评估 credit」；它在基线上也是绿的 | CR-F14 TL2-10b BA2-F17 |
| PP2-m10 | issue | testing | W13 第 2 节；`sc-direct.sh:92`、`:102` | 基线红集 73 条里 52 条只是「函数不存在」（状态 127），不是行为判别；基线轮缺 `V5-S10b` / `V5-S10d` 两行（92 对 94）。TASK-002 的「红集一致」据此逐栏核时分不出「缺失」与「判错」 | QA-14 |
| PP2-m11 | issue | documentation | `run-evidence.sh:17-21`、`:47`；`v31/README.md:35`、`:37`、`:43`；proposal `:689` | `BASH32` 未设置时 W13 静默只跑 4 个 bash；W12 的上界核对对没有进入重跑的结局恒真；README 的复现说明与脚本行为不符（`refreeze` 指针错，W8 新增行数 183 与 187 口径相反） | CR-F15 KM2-6 |
| PP2-m12 | risk | testing | 原型计时器与组杀的 `kill -KILL`；`sc-cases.sh:54` | 改成 `kill -TERM`（QA-M20 / M30）用例分不开；`timeout` 会重置 TERM 处置，用例环境造不出「TERM 被忽略」，而那时截止被架空（实测 10.8–11.2 s） | QA-13 |
| PP2-m13 | issue | testing | `_SG_LEFT` 的 `%d.%06d` | 零填充没有用例：写成 `%d.%d` 的坏实现（BA-M2）把剩余 2.05 s 打成 2.48782，截止晚 0.44 s，最坏晚约 0.9 s | BA2-F8 |
| PP2-m14 | issue | testing | `sc-direct.sh` 开头 | 直调不清 `SECRET_GUARD_TIME_BUDGET_S`，环境里设为 0 时 `V2-G1`、`V2-G4` 对好实现假红 | BA2-F12 |
| PP2-m15 | issue | documentation | TASK-002（`:75`）；套件头注释 `secret-guard.test.sh:5-7` | 「搬入 shapes.py 的输入」可读成搬 Python 生成器，也可读成改写为 bash；搬 Python 会让头注释「python3 只给 SC-20 用」失实。新增依赖、基线取自 `git show 59e333c`（浅克隆会 `exit 3`）、非 Linux 的 SKIP 规则都没写；旧套件约 830 例是否也按 `SC_BASH` 跑有两种读法 | TL2-18 BA2-F14 BA2-F15 |
| PP2-m16 | decision | architecture | Decision 14、What 2；原型 `:630`、`:643`、`:689` | 「没有计数上限」其实是 1,000,000 的上限，到顶时静默止步，形状上又回到 fail-open；3 s 内到不了，但正确性不该依赖机器速度：到顶应返回 3 走回落。「全部代入」也不等于语义完整（见 PP2-S） | TL2-12 |
| PP2-m17 | risk | architecture | INV-7（`:43`）、INV-8（`:45`）；TASK-003 | INV-7 只说「负载 ≥ 2 就作废重跑」，没有次数或时长上限，也没有升级路径（本机今天连续数小时负载 7–10）；TASK-003 的耗时矩阵不受 INV-7 约束；INV-8 的作废规则漏了 TASK-003 的 W14 | TL2-15 KM2-15；PP1-A36 部分 |
| PP2-m18 | issue | architecture | TASK-006 design（`:138-145`） | 阶段 C 的顺序没有写死：主仓 gitlink bump 必须排在 aria、standards 各自双推并逐个 `ls-remote` 核验之后（CLAUDE.md 约束 1）；aria 合并开不开 PR、Rule #8 的 C.2.4 是否适用也没写 | TL2-16 |
| PP2-m19 | issue | architecture | TASK-007（`:161`、`:165`） | 上线后复验用的形状读的是真实可能存在的凭据路径，计划没要求先断言诱饵路径在复验主机上不存在；「各跑一次」有两种读法；没有插件缓存新鲜度探针（WP-A 先例有） | TL2-17 |
| PP2-m20 | issue | documentation | INV-2（`:31-33`）、TASK-001（`:56-62`）、TASK-003（`:93`）、TASK-005（`:127`）、TASK-007（`:160-163`） | INV-2 的封闭清单仍漏了计划自己的产出；「proposal 由 `fill31.py` 从模板生成」没写进计划，执笔席可能直接改 proposal；TASK-003 的 W14 脚本没有名字 | KM2-7；复发 PP1-A38 |
| PP2-m21 | issue | documentation | proposal `:650-651`；TASK-006；主仓 `VERSION` | 「以 v1.77.1 发版提交为样板」出处不准（分散在三个提交）；主仓根 `VERSION` 的 aria 行至今停在 v1.76.1，发版时是否同步未定 | KM2-10 |
| PP2-m22 | issue | documentation | proposal `:17`、`:74`、`:224`、`:542`、`:551`、`:701`；`dispositions.md:62`；`v31/README.md:45` | 「`check_bare_issue_refs.py` 报出的只有 bash 取长度写法一类」差一处（`:224` 引用的基线 hook 注释里还有一个裸号）；席位原编号（CR-03、TL2-F4 等）在 proposal 里没有定义；dispositions 有两处裸号（历史段，追加式不改写） | KM2-11 |
| PP2-m23 | issue | documentation | proposal `:526-539`（P 表）、`:598-639`（SC / BI 表） | `V2-G1`–`V2-G11` 含不存在的 G9 / G10；P5 漏 `V5-S13`；SC 到 BI 的对应有 5 处交叉 | KM2-12 |
| PP2-m24 | issue | documentation | proposal `:528`、`:571`、`:600`、`:708`；`W9-suite.txt:2`；`sc-cases.sh:30` | Decision 14 的「137 → 73」没有物证；「旧套件恰好 6 组」没限定非 git 副本的盲区（SC-8、SC-9a 未跑）；W13 的「SKIP 0」是空转（没有任何用例会 SKIP）；proposal 里引用了 memory 名，对第三方是悬空引用 | KM2-16 |

### 各席一致确认的代码事实（不是 finding）

- **原型可复现**：四席各自用 `mkv31.py` 重新生成原型，sha256 前缀都是 `9f61db0e7b8b`，与 W13 页眉、W8 逐字一致。
- **机制成立**：作业是自己进程组的组长；计时器、计时器里的 `sleep`、判定留下的子进程都在这个组里，`wait` 后的组杀一并清掉；放行与截止两条路径之后都没有残留；给 hook 一个控制 tty 结果不变（BA 在 5.0.18 / 5.1.16 / 5.2.15 / 5.3.20 上实测，CR 在 5.0 / 5.2 / 5.3 上实测）。退出码 77 只在 `_sg_vx_pass` 返回 0 之后出现，不会上抛到 hook 的退出码。
- **Decision 14–16 的技术挑战**：TL、BA 明确无异议，CR、QA 没有提出挑战。重跑取消计数上限只会多看，代价落到截止后回落拦截（裁定 B），父进程那一遍仍有上限；没有找到把它们变成 fail-open 的路径。措辞与细节见 PP2-m7、PP2-m16。
- **作者的 23 个坏实现与作业协议一块的用例是实的**：各席放进去当对照的坏实现（CR-ME、QA-M03 / M05 / M11 / M16 / M19 / M21 / M22、TL-M6 / M7 / M10、BA-M12 / M13）都被预先写下的用例抓住，红的原因与预期一致。
- **shim 的注入点属实**（TL、QA）：`jq` 的首次执行是 stdin 解析，在锚点之后；`sed` 的首次调用落在作业里的 `_sg_redact_echo`。这依赖 INV-1 的逐字落地，见 PP2-B。
- **期望值随 `SC_BASH` 而定的逻辑**与准入门同一判据，3.2 走 identity，是对的（TL、QA）。

## 主控核验与补充（汇总时新增）

### 复跑

均在本机 bash 5.2.15、`taskset -c 0,1 nice -n 19` 下，负载 3–12（其他席并发）。凭据形路径一律由席位脚本在运行时拼装，主控只看 rc 与文案类别。

| 核验对象 | 做法 | 结果 |
|---|---|---|
| CR-F3（CR-MB）、CR-F4（CR-MC） | 重跑 CR 的 `probes/run.sh`：`for9-read`、`longline-credit` × 基线 / 原型 / 坏实现 | 基线 2 / 过大，原型 2 / finding 与 2 / longline，坏实现 **0**：成立 |
| QA-6（QA-M18）、QA-7（QA-M28） | 重跑 QA 的 `xp-fo.sh M18 M28 M28c` | 基线 2 / 过大，原型 2 / growth 与 2 / longline，坏实现 **0**；对照 M28c（用 `z` 填充）两边都是 longline，说明判别量确实是空白：成立 |
| QA-5（QA-M01） | 重跑 QA 的 `xp-ext.sh` B 段（项目只经 stdin `cwd` 给出） | 基线 2、原型 2、M01 **0**：成立。A 段（分段 + M02）在负载约 6 时三者都回落为过大，基线自己就要 4.98 s |
| QA-8 | 重跑 QA 的 `xp-harness.sh` | H1：`PASS 9 FAIL 0`、退出 0；H2：`PASS 6 FAIL 0`、退出 0；H3：替身进程被数进 1 个：成立 |
| BA2-F5（BA-M7）、BA2-F6（BA-M8） | 重跑 BA 的 `demo78.sh` × 原型 / M7 / M8 | 原型：9；3、无文本。M7：**77**。M8：状态 2、有 stderr：成立 |
| TL2-3（PP2-S） | 重跑 TL 的 `probe-run.sh` × 基线 / 原型，六个形状 | `reassign-big`、`reassign-big-multiline`：基线 2 / 过大，原型 **0**，成立；`reassign-small`、`seg-splice-small` 两边都放行（既有缺口）；`seg-splice-big` 与对照在负载约 12 时两边都回落为过大（基线 4.24 s），未复现 |
| CR-F5（PP2-M） | `commentsync.py --hook-only base-anchor-tweak.sh target` | GREEN（未改动的基线 target 为 RED 28）：成立 |
| CR-F1 | 读 CR 的 `run-proto-52.txt` 与各坏实现的整轮结果 | 未改动的原型红 `V9-E11`（kind=oversize：重跑被截止截断后回落）；MA 94 / 0；MB 只红同一条；MC、MD、ME 的红都在计时类用例上：成立 |
| CR-F6、CR-F7、CR-F9、CR-F10、TL2-5、TL2-7、TL2-8 | 读行核对：`detailed-tasks.yaml:31 / :74 / :113`、`v31.sh:675`、`sc-cases.sh:70`、W8 的 `@@` 数、`v31.sh:576-578 / :626`、`run-evidence.sh` 的复制回写、secret-hygiene.md 的四行 | 全部成立 |
| `10CG/aria-plugin#138`–`10CG/aria-plugin#142`、`10CG/aria-plugin#229` | Forgejo API 读标题 | 都不是 PP2-S 的两类 |

### 事件记录

- **报告落盘**：code-reviewer 席的工具集不含 Write，报告由主控按席位最后一条消息原文落盘（通知通道里的 HTML 实体已还原），文件末尾有主控注。其余四席自己写盘。
- **仓内误建文件**：TL 席一条命令写错，在主仓根目录生成了 `conc-demo.txt`（一行报错，从未进 git），已由该席删除；主控核实不存在，`git status` 只有本轮报告。
- **并发干扰**：几席的 `sc-cases.sh` 在 17:26–19:05Z 间多次重叠，本身就是 PP2-K 的实证来源；各席已把「负载红」与「逻辑红」分开记，只有逻辑红算抓住。
- **心跳**：认领心跳推送又失败一次（`10CG/aria-plugin#169` 同形：非快进后 fetch 失败），主控用临时 ref 把心跳提交重放到远端最新之上并推送，`ls-remote` 一致。

## 非作者变异测试汇总

五席各自构造坏实现（原型 + 一处改动），运行前写下预期，再对每个坏实现跑一整轮未改动的 `sc-cases.sh`。只有「逻辑红」算抓住，负载造成的红不算。

| 席位 | 坏实现 | 抓住 | 漏网 | 其中放行方向 | 预测命中 |
|---|---|---|---|---|---|
| CR | 5（MA–ME） | 1 | 4 | 3（MA、MB、MC；MD 在本机负载下回落，未证实） | 5 / 5 |
| QA | 26（M01–M30，缺号未用） | 7 | 19 | 10 | 25 / 26 |
| TL | 10（TL-M1–M10） | 3 | 7 | 5 | 10 / 10 |
| BA | 14（BA-M1–M14） | 2 | 12 | 6（M1、M4、M7、M9、M10、M11；M3 的可达性未核实） | 14 / 14 |
| KM | 5（KM-M1–M4、M6；M1–M3 合并成一轮跑） | 1（M4：指令行改一个字，`V11-S3` 红） | 4 | 0（都是 AI 可见文字的改动，见 PP2-T） | 5 / 5 |
| 合计 | 60 | 14 | 46 | — | — |

被抓住的 13 个里大多是各席特意放的对照（作业协议、截止、进程组、77 一块），说明这一块的用例是实的。漏网的 46 个按行为去重后约 21 类，其中放行方向 12 类：

| 类 | 坏实现（各席编号） | 后果 | 证实到哪一层 | 簇 |
|---|---|---|---|---|
| 1 | 分段触发点不问准入门：CR-MA、QA-M02 | 扩展项目与未实测平台在分段模式进入放宽，扩展腿被跳过 | hook 级（CR：4 次里 2 次放行）；QA 通过层探针 | PP2-D |
| 2 | 项目根只取 `CLAUDE_PROJECT_DIR`：QA-M01、TL-M8、BA-M1 | 只经 stdin `cwd` 得知的扩展项目，读取扩展所列路径的大命令放行 | hook 级，三席各自复现；主控核实 | PP2-D |
| 3 | 重跑仍收 8 个 for：CR-MB、QA-M12、TL-M1 | 经第 9 个 for 的凭据读取放行 | hook 级（CR、TL）；主控核实 | PP2-H |
| 4 | 重跑内 VMAX 被忽略：QA-M24 | 第 17 个赋值超长后，部分收集即放行 | 通过层探针（hook 级演示被负载冲掉） | PP2-H |
| 5 | 重跑内时间检查点返回 0：QA-M06 / M07 / M08 | 慢重跑没判完就放行 | 通过层探针，确定性 | PP2-E |
| 6 | 先算 credit、再看 longline：CR-MC、BA-M4 | 超长行 + 过滤器放行，裁定 C 被破 | hook 级（CR、BA）；主控核实 | PP2-F |
| 7 | 整串分支漏 `return $?`：TL-M2 | 同上 | hook 级（TL） | PP2-F |
| 8 | 分段不路由到 `_sg_vx_big_judge`：CR-MD、QA-M10、TL-M3、BA-M11 | 分段超长行 + 过滤器放行 | hook 级（TL、BA）；QA 通过层 | PP2-F |
| 9 | 量行长的 `read` 漏 `IFS=`：QA-M28、TL-M4 | 首尾空白撑长的行 + 过滤器放行 | hook 级（QA、TL）；主控核实 | PP2-F |
| 10 | 重跑内增长超限放行：QA-M17 / M18、BA-M9 / M10 | 增长超过 8192 的读取放行 | hook 级（QA-M18、BA-M9）；主控核实 | PP2-G |
| 11 | 去掉组长自检：BA-M7 | `set -m` 不生效的 bash 上截止形同虚设，越过 5 s 被杀即放行 | 直调 77 对 9；主控核实 | PP2-J |
| 12 | 计时器与组杀改用 TERM：QA-M20 / M30 | TERM 被忽略时截止被架空 | 外层忽略 TERM 的演示（10.8–11.2 s） | PP2-m12 |

另 9 类不在放行方向：AI 可见的新文字（`longline` 描述句、两条增长原因串、中文行的处方分句，KM-M1–M3、M6，PP2-T）、平台实参取 `$MACHTYPE`（PP2-m8）、分段回落原因串（PP2-I）、重跑检查点写出时间文案（PP2-E）、LMAX 边界与「量不出行长」哨兵（PP2-F）、回落文案缺末尾换行（QA-M15）、`_SG_LEFT` 不补零（PP2-m13）、三常量同值（QA-M29，等价）。

**这些放行都出自坏实现，不出自原型**：原型在全部定向输入上与基线、与声明一致（PP2-S 的两类除外：那是基线判定语义本身的缺口）。照 INV-1 逐字落地，再经 W8 diff 与 TASK-005 复审，这些偏离本应被 diff 发现；问题在于 W8 判据照字面不可满足（PP2-N），而落地之后长期守护这个 hook 的只剩搬进套件的用例。

**可直接取用的材料**：QA 的 `xp-newcases.sh` 有 17 个确定性直调探针（无墙钟窗口），每个都在原型上绿、在对应坏实现上红；BA 的 `demo78.sh`、`stub-*.sh`，TL 的 `probes*.py`，CR 的 `probes/mk.py` 可改写成用例。各席的坏实现都在各自的 scratch 目录（`mut/`），连同预测文件，可直接并入 `mutants.py` 当 BI-24 以后。

## 主控处置建议

### 判断

- **设计不用动**。两轮十席没有证伪机制；Decision 14–16 无异议；PP2-m16（计数上限到顶时静默止步）与 PP2-m6（ε）是细节，不改姿态。
- **R2 的 Major 都能在不改设计的前提下修掉**，而且大多已经有现成材料：QA 的 17 个确定性直调探针，BA、TL、CR 的演示脚本，五席的坏实现与预测文件。
- **再审一轮的边际产出是负的**：要审的会是新补的用例与新改的条款，正是本轮 Major 的来源。验收用例真正的长期宿主是 aria 套件，它在 B.2 才写进仓；post_implementation 审计（已配置开启）会用新席位去审它。

### 若 owner 选「实现优先」，主控的做法

1. **计划与 proposal 小修**（v3.2，只改文字与核对口径，不改设计，不再开一轮 post_planning）：
   - PP2-N：INV-1 与 TASK-004 写明唯一允许的内容差是 What 6 那一行，给 `mkv31.py` 加一个可选的 What 6 步骤，TASK-004 拿实现与「原型 + What 6」比。
   - PP2-O：实现那一轮的证据写到 `v31/impl/`，对照对象写死为 `git show 95cf1de7:<路径>`；INV-2 相应开口；W8 补页眉；页眉加用例脚本的哈希。
   - PP2-P：TASK-004 加一条：移植进套件的用例也要在全部坏实现上跑，指定用例全部变红；TASK-003 补的用例同时进套件与 `sc-cases.sh`。
   - PP2-Q：TASK-001 照 WP-A 先例分两组上呈：一次性授权的四类（feature 分支推送、开 PR、issue 评论、issue 关闭），逐次请示的五类（合并到任一 master、推 master、tag 与发版、主仓 PR 合并、删远端分支）；TASK-007 里 owner 要亲手做的事写进前置条件。
   - PP2-R：standards 计数按行号核三处，每处两个数；占位符改名为 `<N_allowed>`、`<N_cases>`、`<n_new>`、`<carrier_count_axis>` 等，一个名字只指一样东西。
   - PP2-T：块 B 改走 SOT §2 第 3 行三件套：点名行为；补逐字断言作可证伪的定向 fixture（`longline` 描述句、两条增长原因串、中文行全文）；「AB 套件不覆盖 hook 文案」的 issue 随 TASK-001 上呈。删掉 CHANGELOG 里的「待 owner 复议」。
   - PP2-S：按 owner 对第 2 问的决定改 R-a、CHANGELOG 申报与 hook 头注释。
   - Minor 里的文字项：PP2-m3、m4、m5、m7、m11、m15、m17–m24。
2. **验收用例的修补并入 TASK-002，作为它的硬性交付**。由新执笔席做（proposal 的任务表本来就写着「新执笔席」），材料取自五席的探针，不由本计划的作者补写：
   - 12 类放行方向的漏网，每类至少一条确定性用例，优先直调，不靠墙钟；PP2-E、I、J 也一样。
   - 五席漏网的坏实现并入 `mutants.py`，从 BI-24 起编号，每个绑定指定用例。等价的 QA-M29 除外，改用常量扰动跑一轮。
   - 计时类用例：下界与字节比对保留；上界与「重跑须跑完」类改成按同轮基线的自然耗时校准，或在负载超过门槛时整批 SKIP 并单独计数（PP2-A）；`run()` 先建文件再取锚点；垫片只在作业的进程组里停顿，或停顿缩到 4 s（PP2-B）；`V3-E5` 的预算改为 2（PP2-C）。
   - 金丝雀与「应出现的用例编号」清单，`sc-direct.sh` 末行哨兵（PP2-L）；残留进程用例用每轮唯一的参数，再加不超过 1 s 的宽限（PP2-K）。
   - commentsync 改成每个站点绑定必须出现的新句子，套件一侧 7 块与 5 个标题的目标全文写进 proposal（PP2-M）。
   - 验收：原型上整套全绿（5 个 bash，负载按 INV-7）；每个坏实现在指定用例上变红；TASK-004 在实现上复验同一件事。
3. **TASK-003 的盲构造保留**。本轮五席读过用例后专挑可疑处下手，他们的清单是 TASK-003 的最低要求，不是替代。

### 待 owner 的事项

1. **第 2 轮之后怎么走**：停止规则已触发，选项见回复。主控建议「实现优先」。
2. **PP2-S 的两类既有缺口**：在小命令上它们本来就放行；放宽之后，大命令也照此放行。
   - 一种处理：按裁定 A 的字面（只因尺寸被拦的命令改为完整判定、沿用现有语义），在申报里点名，并在 TASK-001 为它们各给一个载体。
   - 另一种处理：重跑里遇到这两种形状就回落拦截。这要改设计，真实流量收益待测。
   - 这是姿态问题，由 owner 定。主控建议前者。
3. **通报（技术判定）**：
   - Rule #6 块 B 改按 SOT 第 3 行处理（PP2-T）。
   - 「AB 套件不覆盖 hook 文案」的 issue 随 TASK-001 的对外动作一起上呈。
   - 「Decision 14–16 不变」同样是技术判定，通报在此。

## Verdict

**PASS_WITH_WARNINGS**：0 Critical，有 Major。

计算依据（去重后）：

- Critical：0。PP2-S 的定级见该行：TL 定为 Major，并注明「若通用句不算申报应升 Critical」。主控维持 Major，理由有三：R-a 与 CHANGELOG 标题都写明「判定语义上的既有缺口覆盖到更多大命令」；裁定 A 的字面就是沿用现有语义；原型本身没有偏离基线语义。但点名与载体必须补（见「待 owner」第 2 条）。
- Major：20。
- Minor：24。

## 轮次记录

### Round 2

- 对象：`detailed-tasks.yaml` v3.1 与 proposal v3.1 @ `95cf1de7`；原型、可执行验收与证据在 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/`；基线 aria `59e333c`（与 v1.77.1 的 `hooks/` 零差异）。
- Agents：qa-engineer、code-reviewer、tech-lead、backend-architect、knowledge-manager，5/5 全新实例，均未参与 post_spec 与 post_planning R1；并发 ≤ 2（QA + CR 先发；TL、BA、KM 依次补位）。
- Sibling probe：已完整扫描，未发现同 issue 竞品（`no_sibling_found`）。
- Drift guard：config 未配置 `audit.drift_guard`，convergence 模式默认不跑 drift-checker。
- Conclusions：去重后 44 条（原始 82 条：CR 15、QA 14、TL 18、BA 19、KM 16）。
- Vote：REVISE × 5（五席都是 PASS_WITH_WARNINGS，都有 Major）。
- 与 R1 比：Critical 1 → 0；Major 簇 23 → 20；R1 的 PP1-A1–A4（放宽面漏一类、截止的三个旁路）没有复发；复发或未收口的有 PP1-A5、A8、A16、A18、A19、A22、A23、A38、A39 的部分内容（见各行回链）。
- Duration：约 8790 s（2026-10-22 17:15:37Z → 19:42:05Z）。
- 汇总落盘时的基线状态：主仓 master 已由别的会话推进到 `dbabfd79`（aria-plugin v1.77.2 发布，gitlink aria `ee9f3a9`、standards `630ba3a`）。aria 的 `hooks/` 在 `68c7f65..ee9f3a9` 之间零差异，`secret-guard.sh` 的 sha256 前缀仍是 `e83c5e30f2cc`，基线冻结照旧成立；`detailed-tasks.yaml` 的 `baseline_freeze` 行写的是 v1.77.1 `68c7f65`，v3.2 时更新。各席引用的 standards 行号以 `a611136` 为准。

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 2（本 checkpoint） |
| 本轮耗时 | 约 8790 s |
| Agent 参与率 | 5/5 |
| 去重前 / 后 issues | 82 / 44 |
| Critical / Major / Minor | 0 / 20 / 24 |
| Major 簇落在 v3.1 新写表面上的占比 | 18 / 20（只算新代码与新文字自身的缺陷：11 / 20） |
| 非作者坏实现：总数 / 漏网 / 放行方向的类 | 60 / 46 / 12 |
| 收敛轮次 | N/A（未收敛；停止规则触发） |

## 成本与收敛距离

- **本轮成本**：5 席，墙钟约 2.4 小时（并发 ≤ 2），席位报告合计 177 KB。
  - 各席耗时与工具调用：CR 约 60 分钟 / 61 次，QA 约 68 分钟 / 73 次，TL 约 41 分钟 / 84 次，BA 约 43 分钟 / 109 次，KM 约 48 分钟 / 139 次。
  - 各席结束时上下文：CR 约 36 万、QA 约 45 万、TL 约 39 万、BA 约 48 万、KM 约 54 万 token；BA、KM 超过「40–50 万即换实例」的线。
  - 主控：复跑核验 10 组（见「主控核验与补充」），1 次心跳补推。
- **累计**：post_spec 2 轮加 post_planning 2 轮；本 Spec 的审计报告约 774 KB（不含本文件）；规格 76 KB，任务计划 18 KB，处置记录 14 KB；仓里的实现代码仍是 0 行，参考实现以 W8 diff（+183 / −49）的形式存在于证据目录。
- **距离**：
  - 机制层面：两轮十席没有证伪；R1 的 Critical 没有复发。
  - 剩下的工作是可执行验收的补强与计划文字的修正，修法大多已有现成材料，不需要新的设计决定；只有 PP2-S 的处理与是否「实现优先」需要 owner 定。
  - 按停止规则，不再加第 3 轮。
