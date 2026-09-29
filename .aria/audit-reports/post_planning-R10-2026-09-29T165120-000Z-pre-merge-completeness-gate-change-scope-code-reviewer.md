---
checkpoint: post_planning
mode: convergence
rounds: 10
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-29T17:19:53.005Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = f06c2303cba6f0ee

- 派单 `/tmp/claude-1000/-home-dev-Aria/cbe6f623-7c3c-4217-8ccb-fd07680a5525/scratchpad/p199-r10/prompts/code-reviewer.md`，全文 112 行。
- 被审 diff：`git diff f231287 59a3e9b -- openspec/changes/pre-merge-completeness-gate-change-scope/`，逐 hunk 做了字符级定位。tasks.md 共 9 处改动，yaml 共 9 处改动。
- `/home/dev/Aria/openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md`：全文 1–269 行。
- `/home/dev/Aria/openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`，分段读：
  - 1–832 行 (metadata)：revision_log 中 v1–v2.7 各条只看了每条前 400 字，v2.8 与 v2.9 各条读了全文。
  - 833–1580 行 (v2_state_runs)：没有逐行人工通读。用 `yaml.safe_load` 取出脚本全文，读了头部说明与 gate 调用段，然后复跑。
  - 1581–2230 行 (31 个 TASK)：全文。TASK-023 到 TASK-031 用 python 原样打印，避免长行被截断。
- proposal (sha256 与 `a563192` 上的相同，均为 `d3c9b4f2…6f34`)：读了 `:16` `:366` `:368` `:449` `:450` 的切片，并全文检索「5 文件 / 五个文件」一类写法。
- 决策单：
  - `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文 (116 行)。
  - `.aria/decisions/2026-09-29-199-r8-and-v2.8-owner-rulings.md` 全文 (77 行)。
- 审计与执笔材料：
  - R9 聚合报告全文。
  - R9 tl / qa / cr 三席的 Findings 节，cr 的风险节，以及 tl 报告 `:208`。
  - v2.8 执笔报告的「请裁项」与「自报薄弱点」两节。
  - 工具 README 全文。
  - 独立复算做完后，才读了 v2.9 派单全文与执笔报告全文。
- aria `5215cf2` 上的文件 (在本席副本里读)：
  - `VERSION`：1–12 行、70–82 行，以及全文里的发布行。
  - `.claude-plugin/marketplace.json` 全文，`.claude-plugin/plugin.json` 1–8 行。
  - `CHANGELOG.md` 1–14 行，以及所有小节标题。
  - `README.md:5`，`README.zh.md:5`。
  - `skills/phase-c-integrator/scripts/submodule_gate.sh` 125–175 行。
  - `skills/state-scanner/scripts/collectors/remote_refresh.py` 375–400 行。
  - 四个先例提交的 VERSION diff，以及 22 个 tag 的六个发版文件。
- aria `1cb3872` 上的文件：`VERSION` 73–77 行，另抽读了 10 处行号引用 (见下文「引用抽查」)。
- 主仓其他文件：
  - `.aria/state-checks.yaml` 340–367 行。
  - `.aria/probes/main-project-version-consistency.py` 的 POINTS 段。
  - `openspec/archive/2026-09-28-handoff-multibranch-subdir-path-fidelity/tasks.md:72-73`。
  - `aria-plugin-benchmarks/ab-suite/version.yaml` 全文。
  - `/home/dev/.npm-global/bin/forgejo` 的 1–37、125–170、250–319 行 (没有读凭据行)。

## Findings

Critical：无。Major：无。Minor：1 条。

### m1 · `97ab93ca` · minor · issue · documentation · scope `tasks.md 判断清单第 71 条`

同一说法也出现在 yaml `metadata.revision_log` 的 v2.9 第一条。

**一句话**：v2.9 新写的代价句称，「他轨读数之后只把 version 行改成与本轨同号、不加 changelog」这一边角形态「仍靠 5.8 合并后的复核」。实测 5.8 (TASK-030) 的合并后复核在这个形态下全绿，看不见它。

**证据**：
- tasks.md:126 (第 71 条) 原文：「他轨读数之后只把 `version` 行改成与本轨同号、不加 changelog 的边角形态并入不冲突 (同一临时仓实测), 仍靠 5.8 合并后的复核」。
- yaml:827 原文：「⇒ 不冲突 (边角形态, 仍由 TASK-030 合并后复核兜住)」。
- 被引的复核 (yaml:2198，v2.9 未改) 只做两件事：
  - 重算两个计数，与 `version.yaml` 比对；
  - 读 `version` 与 changelog 顶条。
- 本席临时仓实跑。基底是真实的 `ab-suite/`，origin 是临时裸仓，情形是他轨只把 `version` 改成本轨的 1.6.0。原样输出：
```
TASK-030 复核: 重算计数 (32, 85) version.yaml 计数 (32, 85) 一致
version = 1.6.0 | changelog 顶条 = 1.6.0 this spec | 本轨号 = 1.6.0
origin/master 上他轨写的 version 行: version: "1.6.0" | 他轨 changelog 顶条: 1.5.0
```
- R9 tl 报告 `:208` 对 v2.8 执笔报告里的同一说法已经指出：「「靠 TASK-030 合并后复读兜住」说重了……复读看不出来。只有他轨同时动了 eval 时，重算计数才会报出。合并结果本身无实害」。v2.9 把这个说法写进了计划正文。

**这条复核怎么会红**：
| 情形 | 复核结果 |
|---|---|
| 他轨未改 | 绿 |
| 他轨只把 version 行改成同号、不加 changelog | 仍绿，区分不出来 |
| 他轨同时改了 eval 计数 | 才会红 |

**失败场景**：owner 或执行者按第 71 条的代价句，以为这一形态在 5.8 有复核兜底。真遇到时，5.8 全绿放行，两轨同号，而 changelog 只记本轨的改动。执行者的动作不变，合并结果也无实害，所以定 minor。

**建议修法**：两处都改为「并入不冲突、合并结果自洽，5.8 合并后复核看不出 (只有他轨同时改了 eval 时重算计数才会报)；合并结果本身无实害，接受」。

## 对账

| 键 | 判定 | 亲验证据 |
|---|---|---|
| `c2513059` (新内容) | closed | 见下方「c2513059 的证据」 |
| `eac9f91d` + `6ff5eb7e` | closed | 见下方「eac9f91d + 6ff5eb7e 的证据」 |
| `4fb29366` | closed | 见下方「4fb29366 的证据」 |
| 共同风险第 1 条 (逐取值点) | closed | 见下方「逐取值点的证据」 |

**c2513059 的证据**
- 改动落点：
  - yaml:2032 新增台账记录 (读数与读取时的 SHA)，并写了按比对结果分类。
  - tasks.md:20 (读前必看第 4 条) 同步。
  - tasks.md:126 新增第 71 条。
- 本席脚本扫过 B.1 到 5.7 之间的主仓并入：唯一一次是 TASK-029 前置条 (yaml:2167)，所以「自 B.1 起未并入过 origin/master」这句属实。
- 本席在临时仓独立复现六种形态：
  | 形态 | 并入 | 比对结果 |
  |---|---|---|
  | 他轨升号在读数之前 | 冲突 | 相等 |
  | 他轨升号在读数之后 | 冲突 | 不等 |
  | 读数前后各升一次 | 冲突 | 不等 |
  | 他轨只改计数 | 冲突 | 相等 |
  | 他轨只改无关文件 | 不冲突 | — |
  | 他轨改成同号、不加 changelog | 不冲突 | — |
- 两个「相等」形态按计划的解法合并后：
  - 合并提交是双亲，第二父是 origin/master；
  - 重算的计数与合并树相符；
  - yaml 原码 `commit_attribution` 输出 `{"verdict": "ok", "commits": 2, "kinds": ["sync-merge", "own-release-sync"]}`。
- 残留：m1 (代价句不准)，以及执笔自报第 1 条 (停点没有指回)。

**eac9f91d + 6ff5eb7e 的证据**
- tasks.md:36 在第 20 条的执行口径列末尾追加了一句，编号仍是 24 条。
- 全文检索 proposal，「5 文件」只出现在 `:366` 与 `:450`，两处都在追加句里点名。
- 第 65 条的链接注 (tasks.md:120) 补上了落点与代价。

**4fb29366 的证据**
- 五处落点逐一核过，都已写入：
  - yaml:235 (owner_gates 第 17 项)，两支；
  - yaml:2192 (TASK-030 的 C.2.4.5 条)，两支；
  - tasks.md:154 (等待点表第 17 行)；
  - tasks.md:214 (5.8 行)；
  - tasks.md:121 (判断清单第 66 条)。
- 包装脚本的退出码约定 (`forgejo:11-18`)：0 = 2xx，1 = 两端都不可达，2 = 4xx / 5xx 等，3 = 凭据类端点被拒。
- `forgejo:256-258`：只有 2xx 才会退出 0。
- 闸这一侧：`submodule_gate.sh:147-148` 在调用失败时 `|| return 1`，按无标签处置。
- 本席用假垫片对闸的原函数跑了八种返回：
  - 只有「已挂上」时闸放行 (rc=0)，计划也在这时重跑闸；
  - 挂了别的 / 空列表：闸不放行 (rc=1)，计划不重跑；
  - 不可达 / 500 / 凭据被拒 / 退出 0 的 HTML / 退出 0 的 JSON 对象：闸都不放行，计划都走「调用失败」一支。
- 5.8 行新写的字不影响归档门：a2 三态的 C 态仍只有 `['3.1', '3.2', '3.3']` 三条集成声明；全勾选时 v2.8 与 v2.9 的门输出完全相同。

**逐取值点的证据**
- 改动落点：yaml:2084 (TASK-025 改号条)、yaml:2123 (TASK-027 第 6 步)、tasks.md:127 (第 72 条)。
- 本席按 TASK-025 末段的锚点字面，另写了一个取值器 (与执笔无共享代码)：
  - 对 22 个 tag (v1.66.0 – v1.74.0)，九个点零处取不到；
  - 与 tag 号不等的只有真实漏改：17 个 tag 的代码块停在 1.47.0、`README.zh.md` 停在 1.41.0；v1.73.3 的代码块停在 1.73.2。
- 本席模拟发版到 1.75.0，做了 7 种反事实，结果与执笔逐项相同：
  - 只改 VERSION 头部行 (其余五个文件全改)、只漏改代码块、只漏插当前发布行、只漏改 marketplace 第二处：旧的「每文件一值」终核通过，逐点终核判红；
  - 只漏改 `README.zh.md`、未改号：两种终核都红；
  - 全改：两种终核都绿。
- 决策单第 6 项要求的最小集 (代码块与 marketplace 两处) 已覆盖。另加的「当前发布行」有四个先例支撑：`1ad31fa` / `9003a82` / `189240f` / `44f00d1`，本席逐个看过 diff，都是新插一行、原行改标「(旧)」。

**引用抽查 (32 处，全部一致)**
- v2.9 新写的引用：
  - proposal `:366`、`:450` (「aria 5 文件」)。
  - `submodule_gate.sh:147-148`。在 `5215cf2` 上核，`1cb3872..5215cf2` 零 diff。
  - aria `5215cf2` 上的九处命中：`plugin.json:4`、`marketplace.json:3/:16`、`CHANGELOG.md:13`、`README.md:5`、`README.zh.md:5`、`VERSION:3/:4/:77`。
  - `1cb3872` 的 `VERSION:76`，值为 1.73.2。
  - 10CG/Aria#195 归档判断清单第 34、35 条。
  - 四个先例提交。
  - 「20 条 / 19 条旧行 (v1.47.0 – v1.60.0)」。
  - 22 个 tag。
  - 探针正则 `main-project-version-consistency.py:40`。
  - TASK-027 第 3 步的 `grep -oE` 写法。
  - `commit_attribution` 的双亲分支 (yaml:743-746)。
  - 包装脚本退出码 (`:11-18`)。
  - 决策单 2026-09-29 第 3、5、6、7 项。
  - v2.8 请裁 1–6 与判断清单第 69 / 70 / 65 / 66 / 68 条的对应 (第 6 条没有对应条目)。
  - v2.8 自报薄弱点第 3 条。
- 在 `1cb3872` 上另抽的既有引用：
  - `phase-b-developer/SKILL.md:214`；
  - `phase-c-integrator/SKILL.md:132` / `:57` / `:754`；
  - `audit-engine/SKILL.md:423`；
  - `spec_complete.py:273`；
  - `state-scanner/SKILL.md:182` / `:191`；
  - `state-scanner/lib/constants.py:58`；
  - `test_pre_merge_gate.py:266`。

**机械核验**
- 在本席副本上按工具 README 跑生成器，得 `REGEN_IDENTICAL`。
- a2 三态脚本 (取自 yaml 全文) 按其 `command` 复跑，与嵌入的 `output` 逐字节一致 (2396 字节，rc=0)。
- v2 脚本不带种子复跑，同样逐字节一致 (9957 字节，rc=0)。两次跑完副本都自行复原。
- v2.9 新增文字：禁用字形 0，裸引用 0，NUL / CR 0。

## 对「改变执行者动作的改动」的逐条判断

1. **`c2513059` 撞号分类**：改法正确 (证据见对账)。分类判据能把两类分开，解法产生的合并提交判 `sync-merge`。附带的代价句不准，已计为 m1。
2. **逐个取值点终核**：改法正确。
   - 锚点在真实数据上唯一，也可执行；
   - 照先例写的四个 tag (v1.73.0 / v1.73.1 / v1.73.2 / v1.74.0) 全部通过，不会误红；
   - 四种漏改形态在逐点口径下都判红，有区分力；
   - 代码块的锚点与主仓探针的正则同形。
3. **`4fb29366` 标签 GET 的调用失败一支**：改法正确 (证据见对账)。计划的新分支与闸自身的判定逐一对应，没有新增外向动作。

**v2.9 其余改动与未改动文字之间的接缝**
- m1 算接缝：新写的句子称未改动的 TASK-030 复核能覆盖这一形态，实际覆盖不到。已计入本轮。
- TASK-029 前置条、tasks.md 5.7 行、第 6 项都没有指回 TASK-023 的比对步骤。这是执笔自报第 1 条 / 请裁第 4 条，不重复计。
- hard_constraints 第 14 条 (3) 的已知形态清单没有同步。这是请裁第 6 条。
- 以下改动与未改动文字无新的不一致：A2 (差异登记)、C (追认注)、版本标识、metadata.container。
- 在活文本里检索「取值一致 / 每文件一值」一类旧口径：只剩 yaml:2084 里 v2.9 自述改动时的引语。
- 结构比对 (机器输出)：
  - owner_gates 仍 19 项，只有第 17 项变；
  - TASK-023 / 025 / 027 / 030 各变一条，所有任务的 verification 条数与 deliverables 不变；
  - 读前必看仍 24 条，只动第 4、20 条；
  - 判断清单由 70 条变 72 条，第 65 / 66 / 68 / 69 / 70 条只加注；
  - 等待点表 19 行，只动第 17 行；勾选行 31 条，只动 5.8；
  - stage_cells 仍 39 格；revision_log 由 66 条变 72 条，前 66 条逐字相同。

## 对执笔人自报薄弱点的表态

1. 原文：分类与解法只写在 TASK-023 和读前必看第 4 条，5.7 的停点没有指回；执行者只看停点时会中性呈报。——**可接受**。方向安全，读前必看第 4 条在执行前必读的范围里。但本席倾向补一句指回 (见请裁 4)。
2. 原文：相等类的解法没写 `last_modified` 取哪一侧。——**可接受**。该字段不进任何判据 (TASK-030 复核只看计数、version 与 changelog 顶条)，owner 确认解法时一并定即可。
3. 原文：临时仓里的他轨改动是模拟的，真实的 T4 还会在 `ab-suite/trigger/` 下加套件。——**可接受**。本席另建临时仓独立复现，结论一致。冲突只取决于两侧都改了 version 行与 changelog 顶部；计数命令只数 `ab-suite/*.json` 顶层，不受子目录影响。
4. 原文：只核取值，不核原行是否改标「(旧)」。——**可接受**。只漏改标时第一条匹配仍是新插的行；漏插却改了标时，第一条匹配会落到 v1.60.0 的旧行，照样判红；原位改写旧行的情形第 72 条已登记为代价。
5. 原文：反事实与历史核验用的取值函数是执笔自己写的。——**可接受**。本席按字面另写的取值器，在 22 个 tag 和 7 种反事实上结果逐项相同。
6. 原文：垫片不是真实的网络失败，包装脚本改约定时「退出非 0 = 非 2xx」会漂移。——**可接受**。本席从包装脚本源码核实了当前约定。计划的判据是「退出非 0 即失败」，即使将来退出码的含义再细分，方向仍然安全。
7. 原文：历史核验只有 22 个 tag。——**可接受**。这 22 个 tag 覆盖了当前版式下的全部发版，并含两类真实漏改。

## 对执笔请裁 6 条的表态

1. 原文：计数重算放进合并提交，「相等」也覆盖只改计数的冲突。——**赞成执笔**。实测合并提交判 `sync-merge`；另起单亲提交会多一次漏写 trailer 的机会。
2. 原文：当前发布行说明里的号算取值点。——**赞成执笔**。四次先例都新插这一行；漏插时它是九点里唯一会红的一处，代价小。
3. 原文：A2 登记在读前必看第 20 条，不放第 3 条。——**赞成执笔**。第 20 条管发布面；追加句已点名 `:366` / `:450`，查找不受影响。
4. 原文：TASK-029 前置条与第 6 项不加指回分类的锚点。——**赞成备选**。比对是 5.7 冲突时必须在呈报前做的动作，现在只写在 5.1 的条目里。在 TASK-029 冲突分支补一句「冲突文件含 version.yaml 时按 TASK-023 的 version.yaml 条比对后呈报」，不改变动作，只是把指令放到执行点，最能保住这次修法的意图。不补也不构成 finding。
5. 原文：tasks.md 5.3 / 5.5 行不写九个取值点。——**赞成执笔**。这两行是粗粒度摘要，字面与逐点口径不冲突；九个点只在一处定义，避免两处漂移。
6. 原文：hard_constraints 第 14 条 (3) 的清单不补「退出 0 但返回解析不成 JSON 列表」。——**无意见，略倾向备选**。执行面已写进第 17 项与 TASK-030，补一项只是让索引保持完整。

## 风险 / 疑问 (不计入 finding)

1. **相等类「重做那次并入」与 origin/master 前进的时序**。
   - 计划写「仍是第二父为当时 origin/master 的合并提交」，但没有要求在比对时把 origin/master 的 SHA 记台账。
   - owner 确认若跨了会话，新会话会按 hard_constraints 第 4 条调 `/state-scanner`。它的 `remote_refresh.py:391` 会跑 `git fetch origin --no-tags --prune`，远程跟踪的 origin/master 随之前进。
   - 这时若对前进后的 origin/master 重做并入，并套用已确认的「保留本轨号」解法，而他轨恰在这段窗口里升到同号并加了 changelog，撞号会被静默吸收。
   - 照字面「当时 origin/master」做不会出错 (reflog 也能找回)，所以只记为风险。建议补半句：比对时记下 origin/master 的 SHA，重做前若已前进就重新比对。
2. **「# 之后的第一个 x.y.z」有一点解释余地**。`VERSION:4` 的说明里还有 issue 引用的 `#` (如 `10CG/aria-plugin#204`)。若误取最后一个 `#`，会取不到值而判红，方向安全；按先例版式没有歧义。
3. **发布日期跨 UTC 日仍无处置步骤**。按决策单第 6 项不纳入，维持 R9 的登记。
4. **归档门与 Step 7**：
   - 全勾选预演判 `warn` 不判 `block`，与计划一致；
   - 真实态 (C 态) 的 warn 只来自 4.4 行 dogfood 一条；脚本缺失的快照另有 3.1–3.3 三条 unclassified，属快照前提；
   - Step 7 的 tracker issue 已由第 11 项登记，v2.9 未改。
5. **B.1 前须推送 `c271cfe`**。本席在副本上跑 `commit_attribution origin/master master`，得 `{"verdict": "stop", "commits": 2, "kinds": ["own", "foreign"]}`：`c271cfe` 只含 `.aria/decisions/`，判 foreign。与 R9 cr 风险第 5 条同一机制。
6. **流程自陈**：
   - 本席所有实跑都在 `audit-R10-code-reviewer/` 下。两份共享副本只 `cp -a` 读取，没有在其中运行任何命令。
   - 真仓只跑了 `git diff` (两提交之间)、`git show`、`git log`、`git ls-remote`。
   - 一次字符级扫描超时转入后台，它只读真仓 `git show` 的输出，已被终止 (退出码 144)，没有写入。

## Verdict

- **Verdict**：PASS · counts `0C/0M/1m` · **Vote: PASS**
- **规范合规**：PASS。R9 三簇 minor 与共同风险第 1 条全部落地；决策单第 7 项的追认注对应正确；改动只在三个计划 / 生成器文件与本轨工具目录内，没有范围外改动。
- **代码质量**：0C / 0M / 1m。

## 是否足以开始 Phase B

足以。本轮零 Major，三处改变执行者动作的改动经独立复现都成立。唯一的 minor 是代价句不准，不改变执行者的动作。B.1 之前仍须按惯例授权推送 `c271cfe` / `59a3e9b` 与本轮报告。