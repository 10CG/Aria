基于以上全部核查(源码级验证、机器计数独立复核、决策单与先例核实、写法规范自检),现在撰写最终报告。

---
checkpoint: post_planning
mode: convergence
rounds: 9
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-29T13:03:56.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = `049e6f0bdf1e8bc0`

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md`(全文 267 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`(v2.7→v2.8 全量 diff 135 行逐行读完;并精读现版 TASK-001/002/018/023/025/027/030/031、`owner_gates` 全文、`sc12_liveness` 全文、`scope_repos`、`rulings_applied`、`revision_log`)
- `proposal.md` `## 4. 文档同步面 (Rule #3)` 与 `## 5. 向后兼容`(:356–:392)
- 决策单 `.aria/decisions/2026-09-29-199-r8-and-v2.8-owner-rulings.md`(全文)
- R8 聚合报告 `.aria/audit-reports/post_planning-R8-2026-09-29T093015-000Z-pre-merge-completeness-gate-change-scope-aggregated.md`(全文)
- 执笔报告 `.aria/notes/2026-09-17-199-a2-a3-tooling/writer-reports/v2.8-writer-report.md`(全文)
- `v2.7-dispatch.md`、`v2.8-dispatch.md` 头部(核对 `<S>` 会话路径)
- 先例 `openspec/archive/2026-09-28-handoff-multibranch-subdir-path-fidelity/tasks.md` 第 34 条
- 源码:`aria/skills/state-scanner/lib/collision.py`(355–430 行 + 全文行号 grep)、`aria/skills/state-scanner/scripts/phase1_gate.py`(1460–1565 行 + 全文 grep `include_terminal`)、`.aria/probes/main-project-version-consistency.py`(全文)
- `standards/conventions/content-integrity.md` §4.4 / §4.5(161–210 行)

实跑(均在 `scratchpad/audit-R9-knowledge-manager/Aria` 隔离副本内):`git diff 7ef09ea f231287` 全量;带圈数字/希腊字母自检脚本;`check_bare_issue_refs.py` 对 v2.8 新增行;`#` 用法逐行 grep 核查;Python 脚本独立核验 `owner_gates`/等待点表编号一致性、`revision_log` 前 56 条逐字比对、判断清单条数连续性;"五文件/5 文件/五处"残留全文扫描。

## Findings

本轮未发现新增 finding(0 critical / 0 major / 0 minor)。

审查覆盖:R8 全部 8 条 finding 的 v2.8 修法逐条源码级/机械级核实(见「对账」);「改变执行者动作的改动」4 条逐条核实(见下节);独立机器脚本核验 `owner_gates`(19 条,编号 1–18 连续含 13a/13b)与等待点表编号逐项相等、`revision_log` 前 56 条与 v2.7 逐字相同(新增 10 条,共 66)、判断清单 70 条连续无缺口;全文"五文件/5 文件/五处"残留扫描确认仅出现在 `revision_log` 历史条目与判断清单第 65 条对 `CLAUDE.md` 已知口径差的显式陈述里,活文本无漏改;`af5e1e47` 引用的 `collision.py:365/385-387/416/420/426-427` 与 `phase1_gate.py:1542-1563/1462-1467` 逐行核对,与源码字节级相符;写法规范(带圈数字、希腊字母、裸 issue 引用、`#` 用法)对 v2.8 全部新增行自检零命中;`main-project-version-consistency.py` 的 `POINTS` 清单确认只涉主仓根路径,与 aria 子模块内 `README.zh.md` 互不相关,`69707662` 的修法不影响该探针。

## 对账

- **`69707662`(Major)—— closed**。证据:`TASK-025.deliverables` 由 5 项增至 6 项(新增 `aria/README.zh.md`,detailed-tasks.yaml:2072);改号条明写"六个文件改为新号"并给出 `README.zh.md` 取值规则(版本行形如 `> **版本**: <号> | **发布日期**: <日期>`)与日期口径(:2078);`TASK-027` 第 6 步终核改为"六个文件...漏改它时仍是旧号而判不成立"(:2117),直接堵上 R8 指出的"五文件终核对漏改结构上不会红"的漏洞;`tasks.md` 5.3 行、`scope_repos` 的 aria 行(`版本 6 文件`)同步;判断清单新增第 65 条记落点与代价。先例 `10CG/Aria#195` 归档 `tasks.md` 判断清单第 34 条经核实字面为"owner 裁『带上, 六个文件一次提交』"(与引用一致)。反事实三态(未改号/只改五个/六个都改)与决策单裁定吻合。`TASK-029` 16 个版本点与 `main-project-version-consistency` 的 9 个主项目版本点均只涉主仓根路径,经独立读源码确认不受影响。
- **`749f8d15`(minor)—— closed**。`owner_gates` 第 17 项、`TASK-030` C.2.4.5 段、等待点表第 17 行、判断清单第 58/66 条五处口径一致地补上"请授权前核标签定义(仓级 GET /repos/10CG/Aria/labels)→组织级读不到交 owner 网页确认→两级都没有则『建标签定义』作为另一次外向写在同一请求点明→打上后先 GET 核实挂上才重跑闸"完整闭环,与 R8 聚合报告"主控实测:仓级只有 aria-auto/bug/feature/post-m0/stale 五个标签"一致。
- **`af5e1e47`(minor)—— closed**。`owner_gates` 第 14 项理由句改写为"该旗标只作用于 `linked_issue_overlaps`...与本轨 claim 处于哪一终态无关",引用的 `collision.py:365`(函数定义)/`:385-387`(ADVISORY-ONLY 声明)/`:416`+`:420`(`_TERMINAL` 定义与终态过滤)/`:426-427`(本轨同名 claim 跳过)、`phase1_gate.py:1542`/`:1550`/`:1552`(仅有的三处 `include_terminal` 使用点)/`:1462-1467`(帮助文本),经 `grep -n` 逐行核对与现版源码字节级相符。
- **`b8cc29e0`(minor)—— closed**。`TASK-001` 基线复核条改为两次比对:第一次(冻结点起)"输出原样记台账...不拿它与...『v2.7 复测』值逐值比";第二次(v2.7 复测端点起)才判定"有没有新 diff"。文中给出的零漂移实测数值(aria 组 36 个里 9 个、主仓组 7 个里 2 个、standards 组 8 个里 3 个非空,`phase_d_sot` 组 6 个全空;第二次比对四组全空)与执笔报告 B3 节数值一致。
- **`c2513059`(minor)—— closed**。`TASK-023` 的 `version.yaml` 撞号句改为"最先在 TASK-029 的前置条把主仓 origin/master 并入主仓 feature 时显形...按该条 git merge --abort、停在 owner_gates 第 6 项";核实 `TASK-029` 第一条 verification 确系 v2.7 既有内容(判断清单第 56 条,post_planning R5 `27cee280`),故此修法只是让 `TASK-023` 的文字描述与 `TASK-029` 早已存在的执行顺序对齐,不引入新执行分支。
- **`5e83496e`(minor)—— closed**。`tasks.md` 3.5 行改为"N1–N4 / N7 / N8",SC 映射表 N3 行复核列改为"2.6; 3.5; 5.5";核实 `TASK-018` verification 第二条本就写"n3 对 completeness_gate.py 为真"(detailed-tasks.yaml:1923),两处双层视图现已与既有事实一致。
- **`0c227bd6`(minor)—— closed**。`sc12_liveness.blind_spots` 补"tasks.md 未勾选(不加 `--force-checked`)"限定,并记上已勾选态下 L3 为真;核对 `sc12_liveness.code` 逻辑,L3 计算(`item["checked"]` + 关键词 + 符号抽取)确实只读 `tasks.md` 文本,与脚本文件是否存在无关,断言成立。
- **`266936b1`(minor)—— closed**。`owner_gates` 新增第 18 项、等待点表新增第 18 行、`TASK-031` verification 引用"owner_gates 第 18 项"、5.9 checkbox 引用"等待点 18"、判断清单第 57 条补链接注 + 新增第 68 条,五处闭环;经独立 Python 脚本核验 `owner_gates` 编号序列与等待点表编号序列逐项相等(`['1'..'12','13a','13b','14'..'18']`)。

## 对「改变执行者动作的改动」的逐条判断

- **`69707662`——改法正确**(证据见上「对账」)。
- **`749f8d15`——改法正确**(证据见上「对账」);另附反事实核实:执笔报告 B1 节以假 forgejo 垫片对 `check_pr_label` 函数字节原样取出测五种返回(已挂上/别的标签/空列表/近名/接口失败),新写的打后核验与闸自身判定逐一相同,不改变闸的放行方向。
- **`b8cc29e0`——改法正确**(证据见上「对账」)。
- **`266936b1`——改法正确**(证据见上「对账」)。

其余标记「不改变执行者动作」的改动,逐条核实:
- **`af5e1e47`**:只改 `owner_gates` 第 14 项的理由句,`--include-terminal` 参数三态统一带上这一执行动作本身在 v2.7/v2.8 均不变——认同。
- **`c2513059`**:`TASK-029` 的"先并入"verification 是 v2.7 既有内容,改动只对齐 `TASK-023` 的文字描述,不引入新的执行分支——认同。
- **`5e83496e`**:`TASK-018` verification 本就含 n3,3.5 行与 SC 映射表只是补齐既有事实的文字枚举——认同。
- **`0c227bd6`**:只给 `blind_spots` 记录补限定语,不改变任何判据或命令——认同。
- **C 组(owner 追认记录)**:判断清单第 51–59、63–64 条各自只追加"(owner 2026-09-29 追认...)"括注,原文一字未改(独立 diff 逐行核对属实)——认同。

**接缝检查**:系统扫描以下潜在接缝点,均未发现 v2.8 改动与未改动文本之间的新不一致:(1)"五文件/5 文件/五处"全文残留扫描,命中全部落在 `revision_log` 历史条目或判断清单第 65 条对 `CLAUDE.md` 口径差的显式讨论里,`TASK-025`/`TASK-027`/`scope_repos`/5.3 行等活文本处无一遗漏;(2)`owner_gates`(19 条)与等待点表编号逐项相等;(3)`TASK-018` 与 3.5 行、SC 映射表 N3 行三处一致;(4)`owner_gates` 第 17 项(yaml)与等待点表第 17 行(md)的标签前提句逐字对应;(5)`owner_gates` 第 18 项(yaml)与等待点表第 18 行(md)均含"比对输出与冲突点随请求呈上"这句(见下节自报薄弱点第 4 条的表态)。

## 对执笔人自报薄弱点的表态

1. 原文复述:终核的"取值"只对 `README.zh.md` 写明了行形,另外五个文件(如 `marketplace.json` 两处 version、`VERSION` 头部行与"## 版本号"代码块)的取值方式计划原本就没写,反事实用的是执笔自定规则。—— **可接受**:这是继承自 v1–v2.6 的既有空白,不是 v2.8 引入的新缺口;`README.zh.md` 本身的取值判据(本轮新增部分)是完整且可证伪的,不受此空白影响。
2. 原文复述:给 PR 打未定义标签时 Forgejo 的真实行为(报错还是静默忽略)未实测,打后核验的反事实靠假垫片;组织级标签定义因令牌缺 `read:organization` 读不到(403),"没有这个标签"只对仓级成立。—— **可接受**:派单禁止外向写操作,执笔无法在本轮做真实打标签实验,属环境约束而非失职;仓级结论(GET 到 5 个标签、无该标签)是可复核的只读实测,组织级留白已如实标注,不构成隐瞒。
3. 原文复述:`TASK-023` "并入即冲突"有前提——两轨都在 changelog 顶部加条目(现有六条 changelog 均如此);若他轨只改 version 行且取号相同,并入不冲突,这种情况靠 `TASK-030` 合并后复读兜住。—— **可接受**:前提有现状实证支持,遗漏场景有下游复核机制兜底,不构成漏项。
4. 原文复述:第 18 项"比对输出与冲突点随请求呈上"是执笔自补的请求内容,比 v2.7 原句多,算不算实质改动请 R9 判断。—— **判断:属轻微的改变执行者动作的改动,但方向是良性收紧(明确停点请求应附带的材料,不放松也不收紧执行路径本身),且经核实已同步写入 `owner_gates` 第 18 项(yaml)与等待点表第 18 行(md)两处、无内部不一致。可接受**,建议执笔本应在「改变执行者动作的改动」表格中单独列出而非隐含于 `266936b1` 一行内,但不影响本轮 verdict。
5. 原文复述:SC 映射表 N3 行超出了席位点名的落点。—— **可接受**:不这样做会让"3.5 行改了、SC 映射表未同步"成为新接缝,执笔的扩面是为避免接缝而非随意扩权,理由充分(见请裁项 2 的表态)。
6. 原文复述:`metadata.container` 与 Status 行没有照派单写"新会话新派",而是写"与 v2.7 同在一个主控会话里派出,但不是同一实例";依据两条——v2.7/v2.8 两份派单的 `<S>` 同属会话 `cbe6f623-…`,决策单也写"同一会话里两次向 owner 呈报"。—— **可接受**:两条依据均已独立核实属实(`v2.7-dispatch.md` 与 `v2.8-dispatch.md` 的 `<S>` 路径确实同属该会话 scratchpad 前缀;决策单开头原文确系"来由: 同一会话里两次向 owner 呈报"),改写后的描述比原"新会话新派"更准确。
7. 原文复述:第一稿把第一次比对误写为"作偏移表的参照"(不准确,写偏移表靠逐处实读,用不到这份 shortstat),且"零漂移时它也不为空"对 `phase_d_sot` 组不成立,已用 `edit_v28b.py` 改正并对终版全部重跑,请对 `TASK-001` 条与 `revision_log` v2.8 第 4 条重点复核。—— **改法正确**:已重点核对修正后的 `TASK-001` 基线复核条,措辞准确区分了"第一次比对只记台账"与"第二次比对才判定有无新 diff、才写偏移表";给出的四组数值中 `phase_d_sot` 组确实是"6 个里 0 个"(全空),与"该组零漂移下不成立"的自我纠正吻合,未见残留错误。
8. 原文复述:归档门只在 tasks.md 未勾选的副本上跑过,全勾选态由 A.2 阶段的 B/C 两态覆盖,本轮勾选行只改了措辞。—— **可接受**:v2.8 对勾选行的改动确属文字层面(如"五文件"改"六个文件"字样),不涉及 checkbox 勾选状态或归档门判据逻辑本身,依赖历史覆盖的验证范围声明合理。

## 对执笔请裁 6 条的表态

1. 原文复述:`c2513059` 的可选句(5.7 并入后 `ab-suite/` 有变则当场重算两个计数)不采,理由是当场重算的 `version.yaml` 不在 5.7 那一提交里、会带出新接缝,他轨同期改动已由 `TASK-030` 合并后复核兜住。—— **赞成执笔取舍**:不采纳避免了提交面归属的新接缝,兜底机制(合并后复核)经核实确实存在且判据明确(按 `TASK-023` 命令重算并与 `version.yaml` 比对,不一致即停下上报)。
2. 原文复述:SC 映射表 N3 行补 3.5(而非只改 3.5 行本身)。—— **赞成执笔取舍**:理由同自报薄弱点第 5 条,避免双层视图新增不一致。
3. 原文复述:`README.zh.md` 的发布日期与 `VERSION`、`README.md` 同口径、不另设判据。—— **赞成执笔取舍**:计划对全部版本文件的发布日期此前均无判据,维持现状不扩面,不构成退步;该缺口已被执笔列入"范围外观察第 3 条"如实记录(`651ff6e` 跨 UTC 日先例)。
4. 原文复述:组织级标签定义读不到时交 owner 网页确认,以打后 GET 的返回(而非打标签接口的回执)作为"已挂上"的证据。—— **赞成执笔取舍**:回执不保证生效,打后 GET 是更可靠的证据来源;组织级读取受令牌 scope 限制,升级给 owner 是合理路径。
5. 原文复述:第 18 项只收"根本冲突"这一个停点,不并入"重做映射时出现新的外向动作"。—— **赞成执笔取舍**:核实"外向动作缺对应项"属 v2.7 既有问题(执笔已在"范围外观察第 1 条"如实记录,归因于 tl 对薄弱点第 7 条的建议),本轮保持第 18 项范围窄可控,避免引入新复杂度,已知缺口未被掩盖。
6. 原文复述:`metadata.container` 的会话描述与派单用词不同(即自报薄弱点第 6 条)。—— **同自报薄弱点第 6 条表态:可接受**,两条依据均已独立核实属实。

## 风险 / 疑问

- `CLAUDE.md` §版本管理仍写"aria 子模块 5 文件",与本轨 `TASK-025`/`TASK-027` 现行"六个文件"口径不一致。此为 owner 在决策单 2026-09-29 第 3 项明确认可的暂时状态("通用口径不在本单裁定范围"),不构成本轮 finding,但建议 owner 在后续某个 Spec 里显式跟踪这条 `CLAUDE.md` 更新(目前只是"上一会话收尾 handoff 留下的待裁项",未见对应 issue 号)。
- 执笔自报薄弱点第 1 条指出的"另外五个文件取值方式计划原本未写"(如 `marketplace.json` 两处 version)是跨版本长期存在的空白,建议未来某轮补齐,但不影响本轮判断。
- 执笔"范围外观察"第 3 条指出的"计划对发布日期无判据"(`651ff6e` 跨 UTC 日先例)同上,留作已知空白,不影响本轮。

## Verdict

verdict: PASS — 0C/0M/0m。**Vote: PASS**。

## 是否足以开始 Phase B

本席判断:就 knowledge-manager 视角(文档同步面、发布同步面、映射表、13 条裁定、读前必看、写法规范)而言,v2.8 相对 v2.7 的全部改动均忠实、准确、无接缝地落地了 R8 的 1 条 Major 与 7 条 minor,足以支持进入 Phase B。但收敛判断取决于五席聚合结果与 owner 按 `audit-engine` 降级策略的最终裁定(决策单第 4 项已预告"R9 即使干净也还不构成收敛"),本席投票不单独构成开工许可。