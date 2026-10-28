# secret-guard-w10-failclosed-narrowing — 审计处置记录

> 本文件只追加、不改写，也不是规格。
>
> 1. 交付面以同目录 `proposal.md` 为准；这里每一节记录的是写下当时那一版规格的处置，规格之后再改，这里不回头同步。
> 2. 各节里的行号、节号、SC 编号都指当时那一版。
> 3. 处置是否落实，以 proposal 的 Decision record 和代码为准，不以本文件为准。
> 4. 审计原文与汇总在 `.aria/audit-reports/`；本文件只做「簇 → 处置」的对照。

## R1 处置对照（v1 → v2，2026-10-21）

原载于 proposal v2 末节，v3 时机械搬到本文件，表格逐字未改（R2-A28）。汇总：`.aria/audit-reports/post_spec-R1-1792577352602-secret-guard-w10-failclosed-narrowing-aggregated.md`。

| R1 簇 | 级别 | v2 处置 |
|---|---|---|
| A1 | C | 硬截止（What 2；Decision 3、4；SC-N5、SC-N9）；Why 的成本模型重写 |
| A2 | C | 撤下第 4 项（Decision 6） |
| A3 | C | D 撤回（owner；Decision 5） |
| A4 | M | 扩展的绝对尺寸门（What 4；SC-N6） |
| A5 | M | 最长行用线性的 `read` 循环（What 2；SC-N11） |
| A6 | M | C 复用 `_sg_judge_one` 的 W12 中和（What 3；Decision 8；SC-N12） |
| A7 | M | 文案逐字（What 5） |
| A8 | M | `_SG_P0` 锚 + 截止封顶；时间类 SC 改为 e2e 环境变量与直调设 `_SG_P0`（SC-N5a–f） |
| A9 | M | 冻结清单 + `refreeze.py` + 判据钉到逐条（SC-N16）；合成替身（SC-N16b） |
| A10 | M | 逐条写明 SC 的形状、bf 前提和要抓的坏实现（SC 表） |
| A11 | M | 采纳 QA 附录 C；去掉与 D、for 列表相关的 REF、CONT |
| A12 | M | 既有用例逐条预测（上表），TASK-001 实跑确认 |
| A13 | M | 9 处注释的封闭清单 + standards 三处计数（Impact；SC-N15） |
| A14 | M | TASK-006 收口与残余 issue |
| A15 | M | CHANGELOG 草稿去歧义，列全放宽面与残余 |
| A16 | M | 重写「不变量与范围外」 |
| A17 | M | Decision 3 |
| A18 | m | 更正 Why 里对 `:476` 的说明 |
| A19 | m | `lim` 入口计算、「任一中间副本」、TMAX 口径（What 1） |
| A20 | m | 逐条消歧；v1 的「一半预算」等措辞已删除 |
| A21 | m | 写明字符口径（What 2）；SC-N14 |
| A22 | m | 「证据与复现」一节 |
| A23 | m | 完整引用、互链、SC 命名空间、基线含 standards、`rule6_note` 归 A.2 |
| A24 | m | 按平台写明收益（Why 表的 W5 行；CHANGELOG 写「Linux 上全部放行」） |

## R2 处置对照（v2 → v3，2026-10-22）

汇总：`.aria/audit-reports/post_spec-R2-1792591829231-secret-guard-w10-failclosed-narrowing-aggregated.md`。R2 判 FAIL（去重 2C/14M/13m），停止规则触发。owner 2026-10-22 裁定：先钉设计、再实现优先，post_spec 以 R2 结论关闭（`overridden_by_user: true`）；未实测平台维持基线拦（裁定点 E）。v3 换了机制：只在基线本来要按尺寸拦的那一刻，才在硬截止作业里按放宽规则重跑 W10，详见 proposal v3 What 1–4。下表的 P、BI、W 编号指 proposal v3 与证据目录 `.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v3/`。

| R2 簇 | 级别 | v3 处置 |
|---|---|---|
| A1 | C | 不再从文本解析状态：结论取作业的退出码，文本只在退出码为 2 时使用（What 3，P4，BI-1；W10 S3、S6） |
| A2 | C | 整个放宽重跑都在同一个硬截止作业里，作业之后不再有任何步骤；扩展腿不跑，因为准入门要求没有扩展（What 1、3，P3；W11 f5like、apply-heavy-cjk；W12） |
| A3 | M | 作业自成进程组，截止杀整个组；作业开工前自检是否为组长，不是就回落（What 3，P5，BI-2；W10 S5，残留进程 0） |
| A4 | M | 截止改用 `EPOCHREALTIME`（微秒），bash 无此变量时不放宽；收益改用 W12 实测，并写明随负载变化（What 1，Decision 6；W12） |
| A5 | M | 缩短类写进放宽面，并且现在也在截止之内（放宽面 R-b；W11 shrink） |
| A6 | M | SC 表改为「性质 + 必须抓住的坏实现」；行结构由性质 P7 与 BI-10 钉住，套件新增 `wpa_x_longline`（TASK-002） |
| A7 | M | 预测表换成实跑结果（W9：6 组变化，21an 不变）；21ab 第 2、3 条结局随首遍耗时变化，TASK-002 改形状 |
| A8 | M | SC-N12 撤下；W12 中和在 `nocredit` 路径上的保持改为性质 P10，用直调验证（w10b.sh） |
| A9 | M | 对抗形状由 `gen-v3.py` 生成，并写明首遍必须便宜这一约束（f5like 的教训见 W11 页眉与 What 3 说明） |
| A10 | M | 作业的每个失败出口都有对应场景（W10 S3、S7、S8，G1–G8）与坏实现（BI-1 至 BI-4、BI-13） |
| A11 | M | TMAX 不变（P9）；验证改为直调廉价形状（TASK-002） |
| A12 | M | 最长行测量钉在副本上、线性 `read` 循环（P7、BI-10）；「不得出现 `{8193,}` 正则」改为静态断言（TASK-002） |
| A13 | M | `$NAME` 与 `${NAME}` 两种拼写、长行由展开产生，都写进 BI-9、BI-10 的构造要求 |
| A14 | M | 注释同步改为封闭清单 + 退役短语表，核对时先把续行注释连接再 grep（Impact） |
| A15 | M | SC-N16 / N16b 撤下，换成 W12 的三项脚本；第三方没有语料时，用 W8–W11 复跑（证据与复现） |
| A16 | M | TASK-001 先开残余 issue、在 #228 留言写 Decision 12 的选项、在 #217 留言指向本 Spec；TASK-007 逐项对账，含评论 28512 第 2 点；关闭关键词只出现在阶段 D 的主仓提交 |
| A17 | m | W5 由 W12 实测取代；Why 表不再给「3 s / 4 s」两列 |
| A18 | m | `lim` 写成函数入口的 local；措辞统一为「超过」（What 2） |
| A19 | m | 故障注入改用 W10 的桩判定 |
| A20 | m | SC-N13 网格撤下；「放宽类之外逐字节相同」由 P1 承担（W9、W12 第 2 节） |
| A21 | m | 放宽路径不再输出时间文案，回落一律用基线的尺寸文案；`longline` 文案按 TL2-F7 改写（What 5） |
| A22 | m | 涉及 locale 的用例用 `C.UTF-8`，并先断言字符集（TASK-002） |
| A23 | m | 随 SC 表撤下 |
| A24 | m | 本机依赖写进 `v3/README.md` |
| A25 | m | CHANGELOG 草稿按 v1.76.1 体例重写；发布同步面按 v1.77.0 的实际改动列全；发版线改为 v1.77.x |
| A26 | m | 页眉补认领行与不变量继承（INV-4 / 5 / 6 / 7 写出内容） |
| A27 | m | Rule #6 逐 hunk 判定写进 Impact，A.2 的 `rule6_note` 照此填写 |
| A28 | m | 审计叙事搬出 proposal，即本文件 |
| A29 | m | owner 裁定点 E：未实测平台维持基线拦（What 1 的准入门） |

## post_planning R1 处置对照（v3 → v3.1，2026-10-22）

汇总：`.aria/audit-reports/post_planning-R1-1792649702638-secret-guard-w10-failclosed-narrowing-aggregated.md`。R1 判 FAIL（去重 1C/23M/15m，39 簇，原始 90 条）。v3.1 的处置分三类：原型改动（`v31/mkv31.py`，每处改动都有直调或端到端用例）；验收写成可执行用例 `v31/sc-cases.sh`，在设计阶段对基线、原型、23 个坏实现实跑（W13）；任务计划按簇改写。用例编号指 `v31/sc-cases.sh` 的输出，BI 编号指 v3.1 的坏实现清单。

| PP1 簇 | 级别 | v3.1 处置 |
|---|---|---|
| A1 | C | 重跑里取消三个计数上限（What 2；Decision 14；`V9-C1`、`V9-C2`、`V9-E10`；BI-17）。TL 给的两个选项与第三种实测对比后取第三种，按技术决定处理并已通报 owner。放宽面加 count 轴一条；小命令一侧列为残余 3，载体由 owner 在 TASK-001 定 |
| A2 | M | 锚点行同时把 `_SG_RELAXED` 置空（What 1；`V2-G11`、`V2-E6`；BI-16） |
| A3 | M | `wait` 之后组杀作业（What 3；`V5-S9`、`V5-S13b`；BI-15） |
| A4 | M | 计时器挪进作业，第一步判定前用 `kill -0` 确认它在跑，否则以 9 退出（What 3；`V5-S10`–`V5-S10d`；BI-3）；fork 失败的说明按实测改写（bash 先重试约 15 s 再中止子 shell，判定不会开始）；另补一条：`sleep` 失败时计时器立即杀组（`V5-S14`；BI-23） |
| A5 | M | 计时判据改由 `shim/` 注入固定延迟（`V3-E3`–`V3-E5`、`V6-E2`、`V2-E7`），不再依赖自然的首遍耗时；BI-13 重定义为「锚点设在 stdin 解析之后」，由 `V3-E3` 抓 |
| A6 | M | BI 清单扩到 23 个（截止漏 `min(…, 3)`、作业结束后不清组、准入门从环境读平台、不初始化标志、计时器用 `&&` 等），每个都有指定用例，W13 第 3 节实跑 |
| A7 | M | 每个 BI 绑定指定用例，W13 的判据是「指定用例全部变红」；TASK-003 的验收改为「被预先写下的用例抓住、且红的原因与预期一致」，无关断言碰红不算 |
| A8 | M | 回落的输入由 `sed` shim 制造（作业必然判不完），并以墙钟下界证明作业确实跑到了截止（`V6-E2` 的窗口 2.85–3.6 s） |
| A9 | M | 增长判据改为在重跑状态下直调 `_sg_vx_apply`，写明方向：增长 8192 放、8193 拦，两种引用拼写各一组；引用在第 8193 字符之后、增长适中，须放（`V8-D1`–`V8-D3`；BI-9） |
| A10 | M | 新增经过 `_sg_vx_big_judge` 的直调用例（`V10-N3`、`V10-N4`）与「只有一份规则循环」的静态检查（`V11-S4`）；BI-11 实跑被抓 |
| A11 | M | R-c 与 What 5 补上 TMAX 文案；TMAX 用例改为重跑里的端到端形状（`V9-E11`；BI-18） |
| A12 | M | 套件新增区分普通命中与 `longline` 的 helper（TASK-002 design）；`sc-cases.sh` 按 `has a line longer than` 与 `value-REDACTING filter` 分类 |
| A13 | M | 期望值随执行 hook 的 bash 而定（`SC_BASH`）；直调用例用 `${EPOCHREALTIME:-}`；SKIP 单独计数；W13 在 bash 3.2 上整轮实跑 |
| A14 | M | 用例在设计阶段写成代码，基线红绿由 W13 第 2 节实跑给出；TASK-001 不再承担此项，TASK-002 末步用新套件复核基线红集 |
| A15 | M | TASK-004 验收逐条列判据（W8、W9 恰好 6 组、W11、W12 的全部结局对上界、W13）；W12 第 1 节对 138 条的每一种结局核对上界；语料复原列为前置 |
| A16 | M | INV-9；`run-evidence.sh` 的基线一律取自 `59e333c` 并断言 sha256 前缀 |
| A17 | M | INV-8：证据绑定 hook 的 sha256，改动一个字节即作废重跑并复审；TASK-005 改为依赖 TASK-003 |
| A18 | M | 块级封闭清单（`v31/commentsync.py`）；原型整块重写 hook 的 8 处（`V12-C1` GREEN）；套件补齐 4 块 `Red when` 与 5 个用例标题 |
| A19 | M | `longline` 补回第三条指令，四行指令逐字复用（`V11-S3`）；`rule6_note` 拆成块 A / 块 B，块 B 标「AI 自作主张、待 owner 复议」 |
| A20 | M | 放宽面改为点名 `10CG/aria-plugin#138`、`10CG/aria-plugin#139`、`10CG/aria-plugin#140`、`10CG/aria-plugin#141`、`10CG/aria-plugin#142`、`10CG/aria-plugin#229`，`10CG/aria-plugin#230` 移出（只涉及启用扩展的项目）；残余 1–7 列全，载体上呈 owner（TASK-001） |
| A21 | M | INV-6 改为「关闭关键词白名单为空」：`10CG/aria-plugin#217` 由 TASK-007 在对账后经 API 显式关闭；每次推送跑固定的 grep；TASK-007 验收核对 `10CG/aria-plugin#217` 已关、`10CG/Aria#217` 状态未变 |
| A22 | M | TASK-001 的全部对外动作先上呈 owner，未放行的不做 |
| A23 | M | TASK-006 认领 CHANGELOG 终稿、standards 三处计数与 tag，验收给出核对方式 |
| A24 | M | TASK-007 补上线后复验、D.1 / D.2、认领释放与周期 handoff |
| A25 | m | 命令替换内首行 `exec 2>/dev/null`（What 3） |
| A26 | m | 准入门改用只读的 `BASH_VERSINFO`，范围定为 GNU/Linux 上的 bash 5.0–5.3：另建 5.0.18、5.1.16、5.3.20 并整轮实测（Decision 16）；剩余时间封顶（`V3-G9`；BI-21） |
| A27 | m | `_sg_relax_noext` 只在「无项目根 / 无扩展文件」时放宽（`V2-G4`；BI-20）；`_sg_vx_big_judge` 加哨兵 |
| A28 | m | 采用：放行用专用退出码 77（Decision 15；`V4-S11`；BI-19） |
| A29 | m | 耗时上界补齐锚点之前、准入门与计时器启动各项，删掉「与负载无关」的说法（What 3） |
| A30 | m | `fill31.py` 断言 W8 的每个逻辑 hunk 都被引用；proposal 新增「参考实现」一节逐字列出 |
| A31 | m | 全文跨仓引用写全；`check_bare_issue_refs.py` 报出的剩余项只有代码里的 bash 取长度写法 |
| A32 | m | CHANGELOG 草稿补 Rule #6 行、130 / 137 的总体说明、危害举例、回落耗时变化与本机依赖；标题改成准确表述 |
| A33 | m | 删掉 `{8193` 的字面检查；行为判据放在 `V7-N5`、`V7-E13`，BI-12 实跑被抓 |
| A34 | m | 桩形写死在 `sc-direct.sh`（`V5-S5`、`V5-S9`、`V5-S13`） |
| A35 | m | TASK-002 design 写明 `C.UTF-8` 与字符集断言；W11 的 CJK 形状在 `C.UTF-8` 下跑 |
| A36 | m | INV-7 补定义：开始与结束各记一次负载，任一读数 ≥ 2 即作废重跑；计时用例不受负载影响 |
| A37 | m | 发布同步面以 v1.77.1 的发版提交为样板；补 tag；合并前重核版本号与新鲜度（TASK-006） |
| A38 | m | INV-1、INV-2 重写，与任务交付物不再冲突；E12 写出路径；「71 条」注明是基线已放行的命令 |
| A39 | m | `run-evidence.sh` 先写工作目录、阶段完成才复制；README 重写；W8 的行数由 `fill31.py` 从 diff 计算；「17」改为只陈述 SC-8 与 SC-9a 两组在非 git 副本里不跑 |

**本轮之外的一条**：用户转来旁路便条，问「构造命令拖过 5 秒」该不该作为 owner 的选择上呈。核对结论：时间护栏的姿态已由裁定 B（2026-10-21）与裁定 E（2026-10-22）定下，v3 起的硬截止就是它的实现；本轮找到的三个截止旁路（A2–A4）都已修成拦。与 `10CG/aria-plugin#228` 同类、仍待 owner 的只有「≤ 8192 的判定可超 5 s」这一残余的载体，已列入 TASK-001 的上呈清单。

## post_planning R2 处置对照（v3.1 → v3.2，2026-10-23）

汇总：`.aria/audit-reports/post_planning-R2-1792689337848-secret-guard-w10-failclosed-narrowing-aggregated.md`。R2 判 PASS_WITH_WARNINGS（去重 0C/20M/24m，44 簇，原始 82 条），停止规则触发。owner 2026-10-23 选「实现优先」：R2 以 owner 覆盖收口，不开第 3 轮；v3.2 只改计划与 proposal 的文字，原型（W8，sha256 前缀 `9f61db0e7b8b`）与证据不变。处置分三类：

1. **TASK-002 必交**：验收补强由新执笔席用五席的探针补齐，在实现上验证（下表写「TASK-002 (x)」，x 指 `detailed-tasks.yaml` TASK-002 的「R2 补强」各条）。
2. **文字修正**：计划、proposal 模板与 README 在 v3.2 已改（下表写「已改」）；proposal 由 `fill31.py` 重新生成。
3. **owner 当日裁定**：两类既有缺口点名申报；准入门按实测范围收紧，WSL（WSL1 与 WSL2）一律维持基线。

| PP2 簇 | 级别 | v3.2 处置 |
|---|---|---|
| A | M | TASK-002 (a)：上界类用例在负载超门槛时整批 SKIP 并单列，`run()` 先建文件再取锚点。INV-7 扩到 W13、套件计时类与 TASK-003 矩阵，并加「取不到低负载窗口就上报」；proposal Success Criteria 与 README 改正「与负载无关」的说法（已改） |
| B | M | TASK-002 (a)：垫片只在作业的进程组里停顿（或缩到 4 s），deadline 类用例见到停顿时长判 INCONCLUSIVE，不判 FAIL |
| C | M | TASK-002 (a)：`V3-E5` 的预算改为 2，窗口 1.85..2.6 |
| D | M | TASK-002 (b)：分段触发点问准入门、项目根只经 stdin `cwd` 给出，各一条用例；对应坏实现从 BI-24 起并入 |
| E | M | TASK-002 (b)：重跑内三个时间检查点返回 3 且不写文案的直调用例 |
| F | M | TASK-002 (b)：超长行加过滤器在整串与分段都拦（含首尾空白撑长的行）；整串分支返回 `_sg_vx_big_judge` 的结论；LMAX 8192 / 8193 边界与量不出行长时的哨兵 |
| G | M | TASK-002 (b)：增长超限在整串与分段都拦（kind=growth） |
| H | M | TASK-002 (b)、(c)：重跑内的 for 计数与 VMAX 各一条用例；BI-17 另拆出三个各漏一处的坏实现；等价的 QA-M29 改跑一轮常量扰动 |
| I | M | TASK-002 (b)：分段回落原因串与基线逐字节相同（桩掉 `_sg_relax_run` 的确定性用例） |
| J | M | TASK-002 (b)：作业在非组长 shell 里返回 9 的直调用例；proposal What 3 写明这条拒绝分支在实测的 bash 上从不触发（已改） |
| K | M | TASK-002 (d)：桩用每轮唯一的参数（含进程号），观察前留不超过 1 s 的宽限 |
| L | M | TASK-002 (d)：金丝雀、`sc-direct.sh` 末行哨兵、应出现的用例编号清单；TASK-002 验收加「两种环境错误下报 SETUP 或 FAIL、退出码非 0」（已改） |
| M | M | TASK-002 (e)：commentsync 改为逐句核对并绑定站点内的新句子，覆盖 What 7 补充；proposal What 7 改正对它能力的描述；验收要求插字符绕过与整块删除两种构造都报 RED（已改） |
| N | M | INV-1 改为「原型 + 三类且仅三类内容差」（What 1 补充、What 6、What 7 补充，字面在 proposal）；TASK-004 的 W8 判据同步（已改） |
| O | M | INV-2 开出 `v31/impl/`；TASK-004 先给 `run-evidence.sh` 加输出目录参数，对照对象写死为 `git show 95cf1de7:<路径>`；INV-8 加用例脚本的哈希与 W14；proposal「证据与复现」与 README 改正「不会覆盖」的说法（已改） |
| P | M | TASK-002 验收加「每个坏实现在移植后的套件上也变红」；搬入方式写定（shapes 改写成 bash，shim 复制，只有新用例按 `SC_BASH`）；TASK-003 补的用例两边都写（已改） |
| Q | M | TASK-001 照 WP-A 先例分两组上呈授权（一次性四类、逐次五类）；TASK-007 的评论与关闭挂到一次性授权上；owner 亲手更新插件缓存写成前置；上呈不阻塞 TASK-002 开工（已改） |
| R | M | TASK-006 按三处锚点、每处两个数核对，secret-scan 那一行不动；CHANGELOG 草稿的占位改名，一个名字只指一样东西（已改） |
| S | M | owner 2026-10-23 裁定点名申报：R-a、CHANGELOG 放宽面申报、残余 8 与 hook 头注释（What 7 补充第 3 条）都点名这两类；载体由 TASK-001 定（已改，Decision 20） |
| T | M | 块 B 改按 SOT §2 第 3 行三件套（技术判定，已通报 owner）：逐字断言由 TASK-002 (e) 补，AB 套件缺口的 issue 随 TASK-001 上呈，三件缺一即照跑；CHANGELOG 删去「待 owner 复议」（已改） |
| m1 | m | TASK-002 (f)：`deadline()` 在非放宽的 bash 上也传附加变量 |
| m2 | m | TASK-002 (d)：root 下先探测 `ulimit -u` 是否生效，不生效则 V5-S10 一组 SKIP；SETUP 单列，不算抓住 |
| m3 | m | `fill31.py` 去掉空元素，并断言 hunk 数等于 `@@` 行数；proposal 重新生成，计数为 18 / 14 / 4；heredoc 内以 `#` 开头的行的分类限制写进脚本头注释（已改） |
| m4 | m | 两处注释列为 What 7 补充第 1、2 条（已改） |
| m5 | m | Why 表 W1 一行注明是基线计数上限下量的增长，n=1053 在 W12 落入增长超限（已改） |
| m6 | m | proposal What 3 的 ε 改写：低负载 0.1 s 以内，负载约 10 时 0.2–1.2 s，hook 启动前的时间不在上界里；列入残余 9 与 CHANGELOG 已知限制。启动作业前预算回落文案属逻辑改动，不在 v3.2 范围（已改） |
| m7 | m | 作为姿态题上呈：owner 2026-10-23 裁定按实测范围收紧，只放宽 x86_64 的 GNU/Linux，WSL（WSL1 与 WSL2）一律维持基线（What 1 补充，Decision 21）；「探测出错」改写成「找不到项目根即视为无扩展」（已改） |
| m8 | m | What 1 补充只用只读的构建信息与内核信息；TASK-002 (f) 的环境毒化把 `OSTYPE`、`MACHTYPE`、`HOSTTYPE` 一起改 |
| m9 | m | TASK-002 (f)：`V7-E15` 换成必须放行的确定形状 |
| m10 | m | TASK-002 的最后一步与 TASK-004 的 W13 验收都分「缺失 / 判错」两栏 |
| m11 | m | TASK-004 给 `run-evidence.sh` 加 `BASH32` 与各 bash 的存在性检查、W8 页眉；W12 的上界只核对进入重跑的结局，其余与基线逐字节相同；README 补上复原脚本的位置与行数口径（已改） |
| m12 | m | TASK-002 (b)：TERM 被忽略时截止仍生效的用例 |
| m13 | m | TASK-002 (f)：`_SG_LEFT` 零填充的直调用例 |
| m14 | m | TASK-002 (f)：直调用例先清掉环境里的 `SECRET_GUARD_TIME_BUDGET_S` |
| m15 | m | TASK-002 的搬入方式写定，见 P（已改） |
| m16 | m | proposal What 2 写明「取消」实为 1,000,000 的上限、到顶静默止步，列入残余 9；改成到顶回落属逻辑改动，不在 v3.2 范围（已改） |
| m17 | m | INV-7 加「取不到低负载窗口就上报」，TASK-003 的耗时矩阵纳入；INV-8 加 W14（已改） |
| m18 | m | TASK-006 的阶段 C 顺序写成编号步骤（已改） |
| m19 | m | TASK-007 的上线后复验：先核插件缓存里 hook 的 sha256，断言诱饵路径不存在，经 harness 发出调用（已改） |
| m20 | m | INV-2 列出计划自己的产出，并写明 proposal 由模板生成、不手改；W14 的脚本命名为 `v31/impl/w14.sh`（已改） |
| m21 | m | 发布同步面的样板改为 v1.77.2（主仓 `028b458a`、`e360908c`，后者修了主仓根 `VERSION` 表）；TASK-006 含主仓根 `VERSION` 的 aria 行（已改） |
| m22 | m | 编号约定里定义席位原编号；README 改正「只有一类」；本文件「R2 处置对照（v2 → v3）」一节里的两处裸号属只追加的旧段，不改写（其余已改） |
| m23 | m | SC-V2 改为真实编号，P5 补上 `V5-S13`，SC 表下注明与 BI 表的 5 处交叉以 BI 表为准（已改） |
| m24 | m | 「137 → 73」注明出处（R1 汇总的复跑表，原始输出未入库）；「6 组」限定为非 git 副本里跑到的用例；W13 的 SKIP 恒为 0 已注明；计划里不再引用 memory 名（已改） |

**说法勘误**：上呈 owner 的选项里写了「实现完成后照常做 post_implementation 审计」。本项目 config 的 post_implementation 检查点是 off，实际对应的是 TASK-003（非作者对抗）与 TASK-005（独立代码审查），两项都用新席位；已向 owner 更正，R2 汇总同步勘误。

**旁路提醒的处置**：用户转来旁路便条，指出准入门按 `*-linux-gnu*` 判平台，WSL 里也会放宽，与裁定 E 可能冲突，而 owner 的主力机是 Windows。核对结论：WSL1 已在第一问里排除；WSL2 是主控在选项里按「真 Linux 内核」默认放进放宽的，选项描述没有写明，等于替 owner 收窄了决定空间。随即单独上呈，owner 选 WSL 一律维持基线（判据另看 WSL 的互操作标记与环境变量，它们只能把放宽关掉）。
