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
