---
checkpoint: post_planning
mode: convergence
rounds: 9
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-29T12:53:14.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = `c1f732efcc8c973b`（对派单文件实算，与要求值一致）。

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md`（v2.8 全文，主仓真仓只读 + 私有副本 `git show f231287:...`）
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`（v2.8 全文，同上）
- `git diff 7ef09ea f231287 -- openspec/changes/pre-merge-completeness-gate-change-scope/`（tasks.md 113 行 + yaml 134 行 diff，全文逐行读）
- `.aria/audit-reports/post_planning-R8-...-aggregated.md` 全文（R8 八条 finding 原文与主控复核）
- `.aria/decisions/2026-09-29-199-r8-and-v2.8-owner-rulings.md` 全文
- `.aria/notes/2026-09-17-199-a2-a3-tooling/writer-reports/v2.8-dispatch.md` 与 `v2.8-writer-report.md` 全文
- proposal.md 未重读全文（本轮改动不涉及 proposal 引用行号漂移，按范围说明不必重做）；决策单 `.aria/decisions/2026-09-12-...` 未逐行重读（本轮范围不含裁定本身）
- 源码实读（均在自建副本 `aria` 子模块 HEAD `5215cf2`）：`skills/state-scanner/lib/collision.py`（358-430 行）、`skills/state-scanner/scripts/phase1_gate.py`（含 include_terminal 全部出现行、帮助文本）、`aria/README.zh.md` / `README.md` 前 8 行、六个发版文件的 `git grep -l -F 1.74.0` 结果、`README.zh.md` 近四个 tag 的版本行
- 实跑（均在自建私有副本 `/tmp/.../audit-R9-qa-engineer/base-Aria`，真仓与两份共享只读副本全程未直接操作，只 `cp -a` 后使用自己的拷贝）：
  - 独立 Python 结构化比对脚本（不采信执笔自述数字），核 metadata 键集、`owner_gates`/`revision_log` 增删位置、31 个 TASK 的 id/顺序/字段级 diff
  - 独立 bash 脚本重算 `b8cc29e0` 的双区间比对（aria_zero_diff 27、aria_shifted 9、standards_files 8、phase_d_sot 6、main_repo 7 个文件，两次比对共 5×2=10 组 `git diff --shortstat`）
  - 独立实跑 `sc12_liveness.py`（含未加与加 `--force-checked` 两态，`0c227bd6`）
  - 判断清单（70 条）、读前必看（24 条）、等待点表（19 行）三项计数与编号连续性独立复算
  - NUL / 禁用字形 / 裸引用三项对新增行的机械扫描

## Findings

| id | severity | type | category | scope | 一句话 |
|---|---|---|---|---|---|
| m1 `4fb29366` | minor | issue | testing | `detailed-tasks.yaml` `owner_gates` 第 17 项 / `TASK-030` C.2.4.5 条 | `749f8d15` 新补的两处 `forgejo GET` 标签核验只写了「返回里有/没有该名」两支，没写「这次 API 调用本身失败」这一支 |

**m1 `4fb29366` 详情**

- 证据：`owner_gates` 第 17 项（= `TASK-030` verification[4] 同文）原文——请核标签有无定义一段只写「仓级跑 `forgejo GET /repos/10CG/Aria/labels`，返回里有名为 `submodule-rollback-approved` 的一项才算已定义……组织级……读不到就请 owner 在网页确认；两级都没有 ⇒ ……」；打后核验一段只写「先跑 `forgejo GET /repos/10CG/Aria/issues/<PR 号>/labels`……返回里有该名才重跑闸……没有 ⇒ 不重跑」。两处都只区分「返回内容含该名」与「返回内容不含该名」，没有第三支「这次 GET 调用本身失败（网络错误 / 凭据过期 / 5xx）」。对照同一文件里 `hard_constraints` 第 14 条「退出码先于输出」的通则，该条第 (3) 款明文「已知形态逐处写在对应条目里，不靠本条兜」——即通则本身不承诺覆盖未列出的形态，这两处 `forgejo GET` 也确实不在第 14 条枚举的命令集合（git diff/status/ls-tree/show/ls-remote/fetch/rev-parse/grep/cat-file/unittest）里。组织级检查确有显式的 403 兜底（「读不到就请 owner 在网页确认」），仓级检查与打后核验没有对等的「调不通」兜底。
- 失败场景：执行者在 B.1/5.8 实跑仓级 `forgejo GET /repos/10CG/Aria/labels` 时若该次调用本身报错（而非返回一个不含该标签的正常列表），字面上只剩「两级都没有 ⇒ 建标签定义是另一次外向写……」这一支可套，执行者可能把「调不通」误当「已确认不存在」，在请求里让 owner 多审一项其实并不需要的「建标签定义」外向写（若标签本来就存在，则是虚假的『不存在』结论）；打后核验同理，调用失败与「标签确未挂上」在字面上不可区分。
- 严重度：minor——两处都不影响闸本身的放行判据（闸自己的 `check_pr_label` 仍会真实核验，误判只会多问 owner 一次，不会导致误合并或误放行），也不会让执行者"卡死"（总有 owner_gates 第 17 项可退），故按口径最高只能 minor。
- 建议修法：仓级检查与打后核验各加一句「该次 API 调用本身失败（非 2xx / 无法解析）⇒ 视为『核不到』而非『没有』，与组织级 403 同样处理：呈请 owner 网页确认，不按『两级都没有』直接建标签定义 / 不按『没有』直接判未挂上」。

## 对账

| R8 键 | 判定 | 我的证据 |
|---|---|---|
| Major `69707662` | **closed** | 独立读 `TASK-025.deliverables`（6 项，含 `aria/README.zh.md`）、`TASK-025.verification[2]`、`TASK-027.verification[6]`、`scope_repos[0].surface`、tasks.md 5.3 行、判断清单 #65，全部已改为六文件口径；实读 aria `5215cf2` 的 `README.zh.md` 第 5 行确为 `> **版本**: 1.74.0 \| **发布日期**: 2026-09-28`，与 `README.md` 第 5 行同形；`git -C aria grep -l -F 1.74.0` 六文件全命中；`git -C aria log --oneline -- README.zh.md` 与四个 tag 逐一核实版本行确随 v1.73.1/v1.73.2/v1.73.3/v1.74.0 同步；确认 `aria/README.zh.md` 不是主仓路径（`git ls-files README.zh.md aria/README.zh.md` 只返回主仓根那份），`TASK-029`/16 个版本点不受影响；全文残留扫描「五文件/5 文件/五处/五个文件」只剩历史 revision_log 条目与 v2.8 自身的对比性叙述，无漏改活文本 |
| `749f8d15` | **closed**（原三项诉求均已满足；我另发现一处相邻的新缺口，登记为本轮 m1 `4fb29366`，不视为本键未闭合） | 读 `owner_gates` 第 17 项 / `TASK-030` verification[4] / tasks.md 等待点第 17 行 / 5.8 行 / 判断清单 #58（追认注）#66（新条），三处前提（授权前核标签定义、未定义时登记外向写、打后核验）逐一落地；标签「仓级未定义」的事实由 R8 tech-lead 与执笔各自独立 `forgejo GET` 实测一致（我本轮未重复外呼，理由见「风险/疑问」） |
| `af5e1e47` | **closed** | 独立实读 aria `5215cf2` 的 `skills/state-scanner/lib/collision.py`：`:365` `def linked_issue_overlaps`、`:385` ADVISORY-ONLY 段、`:416` `_TERMINAL = ("done","abandoned","unknown")`、`:420` `if not include_terminal and c.status in _TERMINAL`、`:426` `if c.track_id == own_track_id: continue`，与 `skills/state-scanner/scripts/phase1_gate.py`：`:1542/1550/1552` 的 `include_terminal` 用法、`:1542-1563` 只写两个 advisory 键、`~:1463` 帮助文本——`owner_gates` 第 14 项新写的每一处行号引用与行为描述逐字对得上源码 |
| `b8cc29e0` | **closed** | 独立写脚本重算双区间比对（不采用执笔或 R8 的脚本），结果与计划新写文字完全一致：第一次比对（冻结点起）aria 组 36 个里 9 个非空、主仓组 7 个里 2 个、standards 组 8 个里 3 个、phase_d_sot 组 6 个全空；第二次比对（v2.7 复测端点起）五组全空 |
| `c2513059` | **closed** | 读 `TASK-029.verification[0]`（本任务未被 v2.8 触碰，逐字确认其「先并入 origin/master」前置条确实存在且在 `TASK-023` 之后执行），与 `TASK-023.verification[2]` 新写的「最先在 TASK-029 的前置条……显形」互相对得上，逻辑自洽 |
| `5e83496e` | **closed** | 读 `TASK-018.title`（未被 v2.8 触碰，本就写「N1–N4」）、tasks.md 3.5 行（已同步为「N1–N4 / N7 / N8」）、SC 映射表 N3 行（已改「2.6; 3.5; 5.5」）；逐一核 `TASK-008`(2.1)/`TASK-013`(2.6)/`TASK-018`(3.5)/`TASK-027`(5.5) 的 verification 原文，确认三个复核列都有对应的 n3 检查点（`TASK-027` 第 7 步经引用 `TASK-018` 的「全部文档机检」间接覆盖） |
| `0c227bd6` | **closed** | 亲自在自建副本执行 `sc12_liveness.py`：不加 `--force-checked` 得 `{"L1": true, "L2": false, "L3": false, "status": "alive", "alive_categories": ["code_reference", "generic_path_call"]}`；加 `--force-checked` 得 `L3: true`，其余不变——与 `blind_spots` 新写文字逐值相符；另确认 `aria/skills/audit-engine/scripts/completeness_gate.py` 此刻确实不存在（Phase B 未跑），符合「脚本缺失态」前提 |
| `266936b1` | **closed**（本键为我自己 R8 所提） | 独立结构化比对确认 `owner_gates` 18→19 项，新增第 18 项内容与 `TASK-031` 原有「新 SOT 与手写路径根本冲突 ⇒ 停在本任务上报 owner」逐字对应；等待点表新增第 18 行；`TASK-031.verification[1]` 唯一改动即插入 `(owner_gates 第 18 项; v2.8 补编号...)` 六字级差异，其余原文逐字未变；判断清单 #57 加链接注、#68 新条 |

## 对「改变执行者动作的改动」的逐条判断

执笔报告本节列出 4 条：

1. **`69707662`——改法正确。** 多改一个文件（README.zh.md 版本行 + 发布日期）、终核多核一项，证据见「对账」表；未发现新接缝。
2. **`749f8d15`——改法正确，但我在其新写文字内部发现一处新的完备性缺口（计入本轮 m1 `4fb29366`）。** 三项诉求（授权前核实、登记外向写、打后核验）本身都已正确落地，只是两处 `forgejo GET` 核验没有显式区分「调用失败」与「调用成功但结果不含该名」；不影响闸本身的放行安全性，判 minor（详见 Findings）。
3. **`b8cc29e0`——改法正确。** 双区间比对的端点、cat-file 口径、写偏移表的触发条件（第二次比对非空才写）逻辑自洽，且我独立重算的十组数字与文字完全吻合。
4. **`266936b1`——改法正确。** 编号追加在末尾、既有编号不移位，且新增的「比对输出与冲突点随请求呈上」一句（执笔自报薄弱点 #4）经核对属于对既有「上报」动作的信息完整化，不构成新的实质要求（见下节表态）。

**v2.8 其余改动是否与计划里未改动的文本产生新接缝**：除上面 m1 一条外，未发现其它接缝。专项核对过的组合：TASK-027 第 7 步（未改）引用 TASK-018（未改）「全部文档机检」是否自动覆盖 N3（覆盖，无需枚举）；`hard_constraints` 第 3/14 条（未改）与新写的标签前提/双比对文字是否矛盾（不矛盾，第 3 条是通用要求已满足，第 14 条明文不兜底特例）；`TASK-030` 其余 verification 条目（未改）是否残留与新标签流程冲突的旧叙述（无，「标签」字样只在被改的 idx4 出现）；全文对「五文件/5 文件/五处」「N 项/18 项」类计数残留的复扫（无漏改）。

## 对执笔人自报薄弱点的表态

1. 终核取值只对 README.zh.md 写明行形，另五个文件的取值方式计划本就没写——**可接受**：这是 v1 起就有的既有缺口（`marketplace.json` 两处版本号、`VERSION` 头部行与代码块），v2.8 没有扩大它，且对新增的 README.zh.md 反而写得比另外五个都精确，不在本轮 v2.7→v2.8 改动范围内。
2. 未定义标签打上去 Forgejo 是报错还是静默忽略没有实测，组织级 403 读不到——**可接受**：下游有「打后核验」兜底（不论打标签这步行为如何，最终看的是核验 GET 的结果），实际风险已被中和；403 的应对（转交 owner 网页确认）已明确写出。
3. TASK-023「并入即冲突」的前提（两轨都在 changelog 顶部加条目）——**可接受**：已如实指出反例（只改 version 不加 changelog 顶条时不冲突），且已写明由 TASK-030 合并后复核兜底，不是自欺欺人的假设。
4. 第 18 项「比对输出与冲突点随请求呈上」是补的内容，请 R9 判断——**可接受**：核对 `TASK-031.verification[1]` 原文，这句信息（diff 输出）在该条紧邻上文本就会被计算出来（「有输出 ⇒ 逐处实读 diff……」），新句只是把「上报」这个动作里本该带的证据明确写出，不产生新的计算或新的外向动作，属于合理的编制体例延伸（`owner_gates` 其它各项本就都遵循「触发条件 + 处置内容」的格式）。
5. SC 映射表 N3 行超出席位点名的落点——**可接受，且是必要的**：若不补，`tasks.md` 3.5 行与 SC 映射表 N3 行会在本轮改出新的两视图不一致（正是本轮要防的接缝类型），详见「对账」`5e83496e` 行的证据。
6. `metadata.container` 与 Status 行没有照 v2.8 派单模板写「新会话新派」——**可接受，且核实后执笔人的改写更准确**：我自己收到的 R9 派单背景事实原文就是「与 v2.7 的实例不是同一实例, 同一主控会话派出」，与执笔人最终写法一致；v2.8-dispatch.md 模板里的「新会话新派」措辞才是不准的一方。
7. 第一稿把第一次比对误写成「作偏移表的参照」，终版已改并全部重跑——**可接受**：已独立核对终版 `TASK-001.verification[8]` 与 revision_log v2.8 `b8cc29e0` 条，全文搜索「作偏移表的参照」零残留，措辞现已准确区分两次比对各自的用途。
8. 归档门只在未勾选的副本上跑过，全勾选态由 a2 的 B/C 两态覆盖——**可接受**：v2.8 只改了勾选行的措辞、不改勾选状态本身，而归档门只按 token 抽取判定（不解析措辞语义），全勾选态的回归风险面未被本轮触及。

## 对执笔请裁 6 条的表态

1. `c2513059` 可选句不采（判断清单 #69）——**赞成执笔取舍**：采纳可选句需要额外定义「重算出的 version.yaml 怎么提交」「不一致时停在哪个等待点」两个新问题，会把一个 minor 修法的范围继续扩大；现有的 TASK-030 合并后复核已是等价的安全网，方向一致只是发现得晚一步，可接受。
2. SC 映射表 N3 行补 3.5（#70）——**赞成执笔取舍**：备选（只改 3.5 行、不改映射表）会让两个视图重新出现本轮本该修掉的那类不一致，不赞成备选。
3. README.zh.md 发布日期与 VERSION 同口径、不另设判据（#65）——**赞成执笔取舍**：计划对另外几处发布日期本就没有判据，单独给这一个新文件加判据是不对称的扩面，超出本轮「改五为六」这个具体缺口的范围。
4. 组织级标签读不到时交 owner 网页确认、以打后 GET 为「已挂上」证据（#66）——**赞成执笔取舍**：备选（组织级一律按未定义处理）在标签其实已在组织级定义、只是本机令牌看不到的情况下会产生假阴性，误导 owner 多做一次不必要的「建标签」决策；现有做法更准确。
5. 第 18 项只收「根本冲突」一个停点（#68）——**赞成执笔取舍**：「重做映射时出现新的外向动作」已经由 `TASK-031` 原文「其中的外向动作照 owner_gates 逐项授权」这句通则覆盖（这些新动作会落在它们各自对应的既有 owner_gates 项，不是本停点的范畴），并入第 18 项反而会把两类不同性质的停点混在一起。
6. `metadata.container` 会话描述用词与派单模板不同——**同自报薄弱点第 6 条判断，无需复议**：执笔人的写法经核实更准确。

## 风险 / 疑问

- 本轮对 `749f8d15` 的「仓级标签未定义」这一事实本身，我没有再次实跑 `forgejo GET` 复核，而是采信 R8 tech-lead 的独立实测与执笔报告的独立复测两者一致的结果——理由：我收到的派单硬性纪律未像 v2.8 执笔派单那样显式豁免只读 `forgejo GET`（只写了「不开 issue、不发评论」），且该事实已有两次独立且方法不同的确认（真实 API 调用 + 另一次真实 API 调用），第三次重复调用边际价值低，故从严不做，改为在此明示依赖链，供主控判断是否需要三验。
- gen_yaml.py 我只做了取出编译（`py_compile` 通过）与改动行数量级核对，未逐行审查其生成逻辑、也未重新跑一遍生成器核对 `REGEN_IDENTICAL`——理由：本轮范围说明「生成器的 diff 只作佐证」，且我已经对生成结果（两版 yaml 本身）做了远比「重新生成一遍」更直接的独立结构化比对与内容正确性验证（含两处实际执行复算），认为对最终交付物的核验强度已经足够。
- 自报薄弱点 #1（另外五个文件取值方式不精确）虽判为可接受、不计入本轮 finding，但这是一个跨版本都存在的老风险，如果 Phase B 实际执行时 `marketplace.json` 或 `VERSION` 出现部分位置漏改，现有「复验六个文件的取值一致」判据能否真的抓到，取决于执行者对「取值」的实现选择——建议后续（不必本轮）针对这五个文件也各自钉一条取值规则。

## Verdict

verdict: PASS — 0C / 0M / 1m
Vote: **PASS**

## 是否足以开始 Phase B

**足以**——v2.8 相对 v2.7 的全部改动（A 组 Major 1 条、B 组 minor 7 条、C 组追认记录）经独立复核与两次实际重算，均忠实且正确落地；本轮新发现的 1 条 minor（`4fb29366`）不影响闸的放行安全性、不会造成执行者卡死或误判，可与其它历史 minor 一并留待 Phase B 顺带修或 Phase D 前补，不构成阻断理由。