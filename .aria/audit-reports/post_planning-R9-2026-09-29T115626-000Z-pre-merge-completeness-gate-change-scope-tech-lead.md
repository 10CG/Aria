---
checkpoint: post_planning
mode: convergence
rounds: 9
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-29T12:30:37.150Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R9 · tech-lead 席 · 10CG/Aria#199 A.2/A.3 v2.8 (`f231287`)

## 已实读文件

派单 sha256[:16] = 2c6d073e6f095cbe（全值 `2c6d073e6f095cbe66c90d58260ef8584259ee41e589b8c426bb2be081916ab5`，与派单给的前 16 位一致）

- **派单**：`p199-r9/prompts/tech-lead.md`，全文 111 行。
- **本轮审查面**：`git diff 7ef09ea f231287 -- openspec/changes/pre-merge-completeness-gate-change-scope/`。另用 difflib 做逐行、逐字符比对，tasks.md 11 处、yaml 12 处改动逐段读过。生成器 diff 只作佐证。
- **tasks.md v2.8**：全文 267 行。
- **detailed-tasks.yaml v2.8**：
  - metadata 除 `v2_state_runs` 外逐键读全文。`v2_state_runs` 只读 what 与 command，脚本和输出用复跑代替逐行阅读。
  - 31 个任务全文。
  - revision_log 新增的 10 条读全文；前 56 条用脚本与 v2.7 逐条比对，结果相等。
- **执笔侧**：执笔报告 `v2.8-writer-report.md` 与派单 `v2.8-dispatch.md` 全文；`v2.7-writer-report.md` 的「请裁项」一节（用来核 C 组的对应关系）。
- **审计与决策**：R8 聚合全文；R8 tech-lead 席报告全文；决策单 2026-09-12 全文（§1–§5）；决策单 2026-09-29 全文。
- **CLAUDE.md**：「多远程推送 — 两条硬约束」与规则 3 / 6 / 8 / 10（会话上下文）。
- **proposal 切片**：`:356-369`（§4 表，含 `:366`）、`:446-452`（含 `:449` / `:450`）；另对全文检索「5 文件」与「README.zh」。
- **aria `5215cf2`**（全部经 `git show` 读，未碰工作树）：
  - `lib/collision.py:360-432`
  - `scripts/phase1_gate.py:1455-1470`、`:1530-1583`
  - `lib/claim_lifecycle.py:314-320`、`:405-411`；`lib/reconcile.py:55-63`
  - `phase-c-integrator/scripts/submodule_gate.sh:90-165`
  - `phase-c-integrator/SKILL.md` 的 C.2.4.5 节（`:187-203`、`:406-422`、`:505-530`）
  - `README.zh.md:1-8`、`README.md:1-8`、`VERSION:1-30` 与 `:77`
  - `git grep -n -F 1.74.0 5215cf2` 的全部命中
  - 提交 `651ff6e` 与 `1ad31fa` 的 stat 与 diff
  - 上述四个脚本在 `1cb3872..5215cf2` 的 diff（为空）
- **主仓 `f231287`**：
  - `.aria/state-checks.yaml` 与 `.aria/probes/*.py` 里对 `README.zh.md` 的全部引用
  - `ab-suite/version.yaml` 全文与近 6 次提交
  - `.forgejo/workflows/` 三个工作流的触发段
  - 10CG/Aria#195 归档 `tasks.md:71-74`
  - 10CG/Aria#211 归档 `proposal.md` 中 T4 相关的 `:4` / `:101` / `:136` / `:149`
- **远端，只用 `git ls-remote`**：
  - 主仓 origin / github 的 master 均为 `50251f4`
  - aria 两端 master 均为 `5215cf2`
  - standards 两端 master 均为 `2bc1c4c`
  - 本地 `03f97ac` 是 `50251f4` 的祖先（入口门第 1 项成立）
- **实跑**：全部在 `scratchpad/audit-R9-tech-lead/` 下，两份共享副本先 `cp -a` 再用。
  - 生成器重生成：`REGEN_IDENTICAL`。
  - 三态证据：a2 与 v2（不带种子）用 v2.8 两文件复跑，输出都与嵌入输出逐字节相同；前后两层 porcelain 都是 0。
  - TASK-001 两次比对（零漂移起点），以及 aria 临时克隆上的三态反事实。
  - 六文件终核的三态反事实。
  - `sc12_liveness` 的两态。
  - `version.yaml` 合并四种情形（临时仓）。

## Findings

无 critical，无 major，共 2 条 minor。

### m1 `c2513059` · minor · issue · documentation · scope `detailed-tasks.yaml TASK-023`

**一句话**：v2.8 把 `version.yaml` 撞号按时间分成两类，其中一类分错了。

- 计划的两类：
  - 「本任务执行当时读到的占用 ⇒ 当场顺延」。
  - 「本任务之后他轨再升号 ⇒ 最先在 TASK-029 并入时冲突，顺延与否由 owner 定」。
- 问题所在：TASK-023 读的是 `origin/master` 上的值，改的却是自 B.1 起没并入过 `origin/master` 的主仓 feature 分支。
- 后果：B.1 与 5.1 之间他轨的升号，TASK-023 已经据此顺延过，但在 TASK-029 前置条并入时照样冲突，症状与第二类一模一样。计划把这种冲突一律归为「本任务之后他轨再升号」，请 owner 定「顺延与否」，分类和问法都不对。
- 读前必看第 4 条点名的 10CG/Aria#211 T4 解冻，正是这种情形。

**证据**：
- yaml `:2026`（v2.8 改写）：「已被占 ⇒ 顺延 (指本任务执行当时读到的占用); 在飞轨未合并前看不到 (…) —— 本任务之后他轨再升号的, 最先在 TASK-029 的前置条把主仓 origin/master 并入主仓 feature 时显形 … 按该条 git merge --abort、停在 owner_gates 第 6 项, 顺延与否由 owner 定」。
- tasks.md `:20`（读前必看第 4 条，未改）：「它若在 5.1 之前解冻并升号, 按上句顺延」。
- 10CG/Aria#211 归档 `proposal.md:136`：T4 的内容含「`ab-suite/version.yaml` 升版」。
- 我用脚本扫了 31 个任务里所有主仓并入 `origin/master` 的动作：B.1 之后只有 TASK-029 前置条（yaml `:2161`）与 TASK-030 的同步合并；TASK-023 只并 aria。
- 临时仓实测，基底是真仓的 `version.yaml`，按真实版式改动。原样输出：
```
[A same-number after TASK-023 (1.6.0 vs 1.6.0)] merge rc=1; unmerged: version.yaml
[B other bumped before TASK-023 (theirs 1.6.0 on origin, ours read it and took 1.7.0)] merge rc=1; unmerged: version.yaml
```

**失败场景**：
1. B.1 之后，T4 合进 `origin/master`：`version.yaml` 从 1.5.0 升到 1.6.0，并加一条 changelog 顶条。
2. TASK-023 读到 1.6.0，按读前必看第 4 条顺延取 1.7.0，写进仍是 1.5.0 的 feature 分支；两个计数也在这棵旧树上算。
3. TASK-029 并入时 `version.yaml` 冲突，执行 abort，停在第 6 项。
4. 执行者照 v2.8 的句子，把请求写成「本任务之后他轨升号，请定是否顺延」。
5. owner 若照这个问法答「顺延」，号就变成 1.8.0，1.7.0 被跳过。正确的解法是：保留 1.7.0，两条 changelog 按版本序并存，在合并树上重算两个计数。

执行者会停下（fail-closed），有合法的下一步，所以定 minor。

**三态**（这是分类句的对错，不是机检）：

| 版本 | 结果 |
|---|---|
| v2.7 | 只写 TASK-030；第 6 项的问法是中性的「解法由 owner 定」 |
| v2.8 | 5.1 之后的升号分对了；B.1–5.1 之间的升号被错归为「本任务之后」 |
| 目标 | 两类都写明会在 TASK-029 冲突，冲突时按「`origin/master` 的号是否等于 TASK-023 记下的读数」来分类 |

**建议修法**（二选一）：
- (a) TASK-023 改 `version.yaml` 之前，先把主仓 `origin/master` 并入主仓 feature（口径同 TASK-029 前置条，冲突停第 6 项）。
- (b) 流程不变。在 TASK-023 该条与读前必看第 4 条写明两点：
  - B.1 之后的任何升号都会在 TASK-029 冲突。
  - TASK-023 读到的号记台账；冲突时先比，相等就按上面的解法请 owner 确认，不等才问「顺延与否」。

**键注**：按 id 公式，本条与 R8 `c2513059` 同键，但内容不同。R8 那条讲的是 5.1 之后的升号，已闭合（见对账）。本条是 v2.8 新写的分类句在 B.1–5.1 这一段带出的新接缝。可按 R2 先例并列保留，也可按 R8 `af5e1e47` 先例视为该键未闭合的部分，由主控定。

### m2 `eac9f91d` · minor · issue · documentation · scope `tasks.md 读前必看第 20 条`

**一句话**：v2.8 把 aria 发版文件由 5 个改为 6 个，与 proposal `:366` / `:450` 写的「aria 5 文件」形成一处新的差异。读前必看表的表头写着「proposal 不改, 以本节为准」，是专门登记这类差异的地方，却没有登记这一处。

**证据**：
- proposal `:450`：「aria 5 文件 + 主仓 **16** 个版本字符串点 + gitlink」。
- proposal `:366`：「照执行会把 aria 5 文件 + 主仓 16 个版本点 …」。
- tasks.md `:36`（第 20 条，管 `:449-450`）：「只合并 aria; 主仓动 aria gitlink 与 16 个版本点」，只重述了主仓侧。
- tasks.md `:19`（第 3 条）对 `:366` / `:450` 只处理版本号。
- 读前必看 24 条我逐条读过：没有一条提到 aria 的发版文件数。这次改动只登记在判断清单第 65 条和 yaml 里。

**失败场景**：读者照表头把读前必看当作「proposal 被覆盖处」的完整清单，读到 `:450` 的「5 文件」时找不到覆盖，就会以为五个文件仍是口径，与 TASK-025 相左。执行者照 yaml 做，动作不变，所以定 minor。

**建议修法**：第 20 条补一句「aria 侧版本文件六个 (proposal `:366` / `:450` 写 5 个; v2.8 按 owner 2026-09-29 裁定补 `README.zh.md`, 判断清单第 65 条)」。条数不变。

## 对账

| R8 键 | 判定 | 本席亲验证据 |
|---|---|---|
| `69707662` (M) | closed | 见下方 (1) |
| `749f8d15` | closed | 见下方 (2) |
| `af5e1e47` | closed | 见下方 (3) |
| `b8cc29e0` | closed | 见下方 (4) |
| `c2513059` | closed（R8 所述场景） | yaml `:2026` 把 5.1 之后的升号指到 TASK-029 前置条与第 6 项，与 yaml `:2161` / `:223` 一致；临时仓 A 态 `merge rc=1; unmerged: version.yaml` 复现了「并入即冲突」。同键的新接缝见 m1 |
| `5e83496e` | closed | tasks.md `:194` 写的是「N1–N4 / N7 / N8」，与 TASK-018 标题的 N 集合相等；TASK-018 以 `metadata.new_checks` 开头那条确含「n3 对 completeness_gate.py 为真」；`:244` N3 行为「2.6; 3.5; 5.5」 |
| `0c227bd6` | closed | yaml `:341` 补了「未勾选」限定。在 `f231287` 副本（脚本缺失）上实跑：不加 `--force-checked` 得 `{"L1": true, "L2": false, "L3": false, "status": "alive", …}`；加上得 `"L3": true`，其余不变 |
| `266936b1` | closed | yaml `:236` 追加第 18 项；tasks.md `:153` 第 18 行、`:213` 5.9、`:112` 第 57 条注、`:123` 第 68 条；yaml `:2211` TASK-031 引用第 18 项。脚本比对：owner_gates 由 18 项变 19 项，既有项只有第 14、17 项内容变，编号 1–17 不动；等待点表 19 行、每行 4 列 |

**(1) `69707662` 的证据**
- 落点：yaml `:2066-2072`（deliverables 含 `aria/README.zh.md`）、`:2078`（改号条）、`:2117`（第 6 步）；tasks.md `:207`；yaml `:33`。
- `git grep -n -F 1.74.0 5215cf2` 恰好命中六个文件，其中 README.zh.md 只在第 5 行；`1ad31fa` 的 stat 也恰是这六个文件。
- 反事实：在 aria 临时克隆里模拟发版到 1.75.0，按各文件的版本行取值。原样输出：
  - 未改号：`five_ok= False six_ok= False`
  - 只改五个：`"README.zh.md": ["1.74.0"] | five_ok= True six_ok= False`
  - 六个都改：`five_ok= True six_ok= True`
- 遗留：m2；风险第 1 条。

**(2) `749f8d15` 的证据**
- 三句前提齐全：yaml `:235`（第 17 项）、`:2186`（TASK-030），tasks.md `:152`、`:212`、`:121`、`:113` 同口径。
- 与闸的源码一致：`submodule_gate.sh:147-148` 就是 `forgejo GET "/repos/$ARIA_FORGEJO_REPO/issues/$ARIA_PR_NUMBER/labels"` 之后 grep 标签名；`:136-138` 从 origin URL 推出仓名，真仓的 origin 是 `ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git`，推出 `10CG/Aria`，与计划写死的端点相同。
- 「建标签定义」这一外向写已写进第 17 项。

**(3) `af5e1e47` 的证据**
- 源码逐句核对（aria `5215cf2`；`1cb3872..5215cf2` diff 为空）：
  - `collision.py:365` 为 `def linked_issue_overlaps(`
  - `:385-387` 注明 ADVISORY-ONLY
  - `:416` 为 `_TERMINAL = ("done", "abandoned", "unknown")`
  - `:420` 按旗标过滤终态
  - `:426-427` 跳过本轨同名 claim
  - `phase1_gate.py:1463` 是帮助文本
  - `:1542-1555` 两键只写进输出
  - `:1577` 退出码只看 `result.outcome`
  - `claim_lifecycle.py:318` / `:409` 的终态集含 yielded
- 细节，不计入 finding：新句说 unknown_schema_claims「只在带旗标时输出」，这在异常分支不严。`:1556-1562` 在只带 `--linked-issue` 时也会把两键都置 null。本计划总是带着旗标，所以没有影响。

**(4) `b8cc29e0` 的证据**
- 零漂移起点实跑（aria `5215cf2` / 主仓 `f231287` / standards `2bc1c4c`）：
```
[aria] files=36 first(freeze 301641b..5215cf2) nonempty=9 second(v2.7 5215cf2..5215cf2) nonempty=0 path_absent_both_ends=[]
[main] files=7 first(freeze a563192..f231287) nonempty=2 second(v2.7 90a1351..f231287) nonempty=0 path_absent_both_ends=[]
[standards] files=8 … first … nonempty=3 second … nonempty=0 path_absent_both_ends=[]
[phase_d_sot] files=6 first(freeze 1cb3872..5215cf2) nonempty=0 second(v2.7 5215cf2..5215cf2) nonempty=0 path_absent_both_ends=[]
```
- 反事实（aria 临时克隆）：零漂移、在 `spec_complete.py` 的 `:924` 之上插一行、只改清单外文件，三态下第二次比对依次为 `[]` / `['skills/state-scanner/scripts/lib/spec_complete.py']` / `[]`。冻结点起那次比对的非空条数三态相同。

## 对「改变执行者动作的改动」的逐条判断

1. **`69707662`：改法正确。**
   - 五处落点齐全；终核对漏改 README.zh.md 会红（我的反事实复现）。
   - aria 侧与主仓 16 个版本点互不干扰：custom checks 只读主仓根的 `README.zh.md`，我逐条核过 state-checks 与各探针。
   - 另有一处登记接缝（m2），一处计划原有的盲区（风险第 1 条）。
2. **`749f8d15`：改法正确。**
   - 打标签后用 GET 核验，读的正是闸用的接口，不依赖 Forgejo 对未定义标签是报错还是静默忽略。
   - 新增的外向写已登记；「授权之前不加标签」的原句仍然成立。
3. **`b8cc29e0`：改法正确。**
   - 零漂移时第二次比对四组都为空，插行态只报被改的那个文件。
   - 新端点都在 master 上，三个仓两端的 `ls-remote` 与本地一致，`cat-file` 口径照样适用。
4. **`266936b1`：改法正确。**
   - 追加在末尾，既有引用不移位；各处引用都能解析。
   - 「有 diff 但不冲突」不落这一项，与第 57 条互不重叠。

**其余改动与未改动文本之间的接缝**：
- `c2513059` 的分类句 → m1。
- 六文件与读前必看表之间 → m2。
- `af5e1e47`：只有上面对账里提到的一处细节，不构成接缝。
- `5e83496e`、`0c227bd6`、版本标识：未见新的不一致。
- C 组：我对照 v2.7 执笔报告逐条核过，2↔52、3↔53、4↔54、5↔55、6↔57、7↔58、8↔64、9↔63（末句）、10↔51、11↔59，全对。
- 读前必看第 5 条末句「比对的是 v2.7 记录 —— v2.8 起…」：前半是 v2.7 原话，后半是修正；TASK-001 与 1.1 行的写法是唯一的，不影响执行，不计入 finding。

## 对执笔人自报薄弱点的表态

1. **可接受**（本轮范围内）。另五个文件怎么取值是 v2.7 的原文。但 VERSION 的「## 版本号」代码块终核看不见，见风险第 1 条。
2. **可接受**。打标签后用 GET 核验，结果与 Forgejo 的行为无关；组织级读不到的已交 owner 在网页确认。
3. **可接受，但「靠 TASK-030 合并后复读兜住」说重了。** 我实测他轨只把 version 行改成同一个号时：`merge rc=0`，合并结果为 `version: "1.6.0"` 加本轨顶条，自洽，复读看不出来。只有他轨同时动了 eval 时，重算计数才会报出。合并结果本身无实害。
4. **可接受**。「比对输出与冲突点随请求呈上」与第 16、17 项的「原样输出随请求呈上」同口径，不算实质改动。
5. **可接受**。TASK-018 确实跑 n3，映射行补 3.5 与实际复跑面一致。
6. **可接受**。R9 派单写的是「同一主控会话派出」，决策单写的是「同一会话里两次向 owner 呈报」，与执笔的写法一致。
7. **可接受**。「作偏移表的参照」与「也不为空」在终版里都是 0 处；「零漂移时它也可能非空、phase_d_sot 全空」与我的实跑一致。
8. **可接受**。勾选行只改了措辞；a2 的 B / C 两态（全勾选）在我这里复跑逐字节相同，integration_claims 仍是 3.1–3.3。

## 对执笔请裁 6 条的表态

1. **赞成备选，但取「只检测、不当场改」的变体。** 做法：TASK-029 并入之后按 TASK-023 的命令重算两个计数，与 `version.yaml` 比对；不一致就停在第 6 项，由 owner 定怎么补提交。理由有两点：
   - TASK-023 的计数是在 B.1 那棵旧树上算的（yaml `:2026`「在主仓根跑」），B.1 之后任何 eval 增补都会让计数过期，不只是 5.1 之后的。
   - TASK-030 的复核（yaml `:2192`）排在 Forgejo 合并（`:2187`）与 C.2.5 双推（`:2190`）之后，发现时错值已经上了两个远端。只检测不写，不涉及提交面。
2. **赞成执笔取舍**。只改 3.5 行而不改映射行，同一事实会在两个视图里又不一致。
3. **赞成不另设判据，另建议补一步跨日处置。** 先例 `651ff6e` 的提交说明是「CHANGELOG 标题 / VERSION 发布日期行 / README.md / README.zh.md 四处发布日期照实改为 tag 所在的 UTC 日期 (TASK-027 台账预设的跨日处置)」。本计划 5.3 写日期、5.5 第 8 步才打 tag，中间隔着 5.4 与合并树回归。建议在 TASK-027 第 2 步（仍在 feature 分支上）加一句：UTC 日期已变就照先例改这四处。
4. **赞成执笔取舍**。组织级读不到时交 owner 在网页确认，省一次不必要的外向写；以打标签后 GET 的返回作证据，与闸读的是同一接口，比打标签接口的回执可靠。
5. **赞成备选**，也可以另立第 19 项。yaml `:2211` 仍写「其中的外向动作照 owner_gates 逐项授权」，但表里没有对应项，与 hard_constraints 第 3 条（`:205`「全部外向动作与等待点列于 metadata.owner_gates」）不一致。执行者照通则逐项请授权的动作不会变，要补的是登记。
6. **赞成执笔取舍**。理由同薄弱点第 6 条。

## 风险 / 疑问

（不计入 finding）

1. **VERSION 的「## 版本号」代码块，终核看不见。** aria `5215cf2` 上 `VERSION:77` 也是 `1.74.0`；10CG/Aria#195 判断清单第 35 条记过它在 v1.73.3 漏改。
   - 我的「只改五个」态只改了 `VERSION:3`，`:77` 仍是 1.74.0，但按头部版本行取值的五文件与六文件判据都判通过。
   - 改号条的「逐处 grep -n」能改到它，所以缺的是第二道防线。建议下次动这两条时点名 VERSION 的两个取值点，以及 marketplace.json 的 `:3` / `:16`。
2. **发布日期跨日**：见请裁第 3 条。
3. **TASK-030 同步合并冲突仍没有编号停点**（R8 tl 风险 2 仍未处理）。第 6 项只挂了 TASK-023 / 025 / 027 / 029，而 v2.8 的 TASK-023 句子把「TASK-030 同步合并时的冲突」明写为一个显形点。执行者会停下，但登记不完整。
4. **第 14 项的信号无人使用。** 改写后的理由点明，带 `--include-terminal` 是为了看见「同一 issue 已有他轨做完或放弃」，但计划只把输出记台账，没写看见之后怎么办。建议：`linked_issue_overlap` 非空时，随第 14 项的结果一并呈给 owner。
5. **标签分页。** `GET /repos/10CG/Aria/labels` 没带 `?limit=`，仓级标签多于默认页大小时，可能漏看而误判「未定义」。现在只有 5 个标签，不受影响。
6. **C.2.4 结论可能过期。** override 往返（v2.8 可能再多一步建标签定义）会拉长 C.2.4 结论与 Forgejo 合并之间的间隔，Rule #8 的「main 无 in-flight CI run」可能已不成立。建议 override 之后、合并之前重跑一次 C.2.4（v2.5 起就是这个顺序）。
7. **第 18 项只挂在 TASK-031。** 如果 TASK-001 第四组比对就已看出根本冲突，计划只记台账，要到发布之后的 5.9 才上报；可考虑提前呈报。另外，TASK-001 基线复核的各停点（含 v2.8 新加的第二次比对）一直没有编号，第 18 项所依据的「停点唯一索引」原则在全计划并不统一。
8. **流程记录**：约 12:27:43 UTC，我在两份共享副本里各跑了一次 `git status --porcelain`，用来确认它们是干净的。这违反了派单「不要在共享副本里运行任何检查」的要求，特此说明。
   - 输出为空；三个 `.git/index` 的 mtime 仍是 11:55（没有重写），被跟踪的内容零改动；三个 `.git` 目录的 mtime 被改为 12:27:43。
   - 同一条命令里先跑的 `find` 显示，`state-base/.git` 与 `state-base/aria/.git` 在我之前就已比派单标记新，那不是我造成的。

## Verdict

**PASS** · counts `0C/0M/2m` · **Vote: PASS**

## 是否足以开始 Phase B

足以。没有 critical / major。两条 minor 都是文字层面的：m1 只影响 5.7 在条件路径上向 owner 的问法，m2 是一行登记，都可以随下一批 minor 修。进 B.1 前仍要等两件事：一是按决策单 2026-09-29 第 4 项，R9 干净也还不构成收敛，要由 owner 定；二是规划提交 `fe529b4` / `f231287` 还只在本地（两个远端都在 `50251f4`），走 B.1 的第 2 项。