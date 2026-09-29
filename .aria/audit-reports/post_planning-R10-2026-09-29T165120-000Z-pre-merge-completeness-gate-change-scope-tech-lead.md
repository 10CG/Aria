---
checkpoint: post_planning
mode: convergence
rounds: 10
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-29T17:22:12.417Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R10 · tech-lead 席 · 10CG/Aria#199 A.2/A.3 v2.9 (`59a3e9b`)

## 已实读文件

派单 sha256[:16] = a4d0400c9ad31980（全值 `a4d0400c9ad3198007db33cdb52da2237fd43faf971b64c97dab3a37e26c9bf3`，与派单给出的前 16 位一致）

- **派单**：`p199-r10/prompts/tech-lead.md`，全文 111 行。
- **本轮审查面**
  - 读了 `git diff f231287 59a3e9b` 在计划目录下的全部改动：tasks.md 7 个 hunk，yaml 9 个 hunk（含 revision_log 新增 6 条）。
  - 另用 difflib 做了逐行、逐字符比对。
  - 生成器 diff 没有逐行读，只用重新生成来佐证。
- **tasks.md v2.9**：全文 269 行（sha256 前 16 位 `590854caf4f3abab`，与真仓一致）。
- **detailed-tasks.yaml v2.9**（`ce1d37d8727b4b90`）
  - 逐字读过的 metadata 键：
    - `:1-40`（头注释到 scope_repos）
    - rulings_applied / test_runner / hard_constraints / owner_gates（`:187-236`）
    - c25_five_questions / execution_order / canonical_call（`:569-580`）
    - commit_attribution 全文（`:698-759`）
    - revision_log 的 v2.9 六条（`:827-832`）
  - revision_log 前 66 条：用脚本与 v2.8 逐条比对，全部相等。
  - 任务：TASK-001 与 TASK-023 – TASK-031 逐字读；TASK-002 – TASK-022 通读。
  - 以下内容没有逐行读：baseline_rebase / new_checks / sc12_liveness / stage_cells / coord_* 正文，以及两份三态脚本与输出。v2.9 没有碰它们，我用结构化比对确认了零改动，三态证据改用复跑。
  - c25_five_questions：v2.9 未触及，本轮没有对 SKILL.md 重做五问核验。
- **执笔侧**
  - `v2.9-dispatch.md` 与 `v2.9-writer-report.md` 全文。
  - `v2.8-writer-report.md` 的「请裁项」一节，用来核对追认注的对应关系。
- **审计与决策**
  - R9 聚合全文，R9 tech-lead 席报告全文。
  - 决策单 2026-09-12 全文（§1–§5）；决策单 2026-09-29 全文（第 1–7 项）。
- **CLAUDE.md**：「多远程推送 — 两条硬约束」与规则 3 / 6 / 8 / 10（会话上下文）。
- **proposal**
  - 切片：`:356-369`（§4 表）、`:449-451`。
  - 全文检索「5 文件 / 五个文件 / 五文件 / README.zh」，只命中 `:366` 与 `:450`。
- **aria `5215cf2`**（在我自己的 `cp -a` 副本与其临时克隆里读）
  - `phase-c-integrator/scripts/submodule_gate.sh:100-175`（check_pr_label 在 `:128-150`）
  - VERSION 的 `:1-30`、`:60-95`、`:176-186`；`1cb3872` 上的代码块
  - `plugin.json` / `marketplace.json` 头部，`CHANGELOG.md:1-14`，`README.md` / `README.zh.md` 的 `:1-8`
  - 六个文件的 `git grep -n -F 1.74.0`
  - 四次先例 `1ad31fa` / `9003a82` / `189240f` / `44f00d1` 的 VERSION diff
- **主仓 `59a3e9b`**
  - `.aria/state-checks.yaml` 里四条版本类 check 的 command
  - `.aria/probes/main-project-version-consistency.py:39-51`
  - `ab-suite/version.yaml` 与其近 6 次提交
  - 10CG/Aria#195 归档 `tasks.md` 判断清单第 34–35 条
  - 10CG/Aria#211 归档 `proposal.md` 中 T4 相关的 `:4` / `:59` / `:101` / `:116` / `:136` / `:149`
  - `standards/conventions/content-integrity.md:161-206`（§4.4–§4.5）
  - 主仓 16 个 aria-plugin 版本点的 `git grep`
- **`/home/dev/.npm-global/bin/forgejo`**：只读了文本（头注释 `:1-71`、主体 `:129-319`），没有调用。
- **远端（只用 `git ls-remote`）**：主仓 origin 与 github 的 master 都是 `d7ab0c0`；aria origin master 为 `5215cf2`，`v1.74.0^{}` = `5215cf2`。
- **实跑**：全部在 `scratchpad/audit-R10-tech-lead/` 下进行，两份共享副本先 `cp -a` 再用。
  - `REGEN_IDENTICAL`。
  - 三态证据：a2 与 v2（不带种子）用 v2.9 的两个文件复跑，输出都与嵌入输出逐字节相同，前后两层 porcelain 都是 0。
  - 归档门：v2.8 与 v2.9 对比。
  - 结构化比对。
  - 我自己写的取值器，跑了 22 个 tag 与 9 态反事实。
  - `version.yaml` 冲突分类的临时仓，含 6 态与一条链式情形。
  - 标签 GET 的 7 态垫片。
  - 在 `189240f` 上模拟改标，再跑写法自检。
  - 对未推送的两个提交跑 `commit_attribution`。

## Findings

无 critical，无 major，共 2 条 minor。

### m1 `1b31a399` · minor · issue · implementation · scope `detailed-tasks.yaml TASK-023`

**一句话**：台账读数只在 5.1 记一次。owner 裁「顺延」之后，读数不随之更新。此后本 cycle 里 `version.yaml` 再冲突时，比对基准已经过期，只会判「不等」，分类退回 v2.8 的错问法。

**证据**：
- yaml `:2032` 写了两句：
  - 「读到的 version 与读取时 origin/master 的 SHA 记台账 (v2.9)」
  - 「不等 ⇒ 读数之后 origin/master 又升了号, 才请 owner 定顺延与否」
- 全条没有「顺延落地后改记读数」一类的句子。tasks.md `:20`（读前必看第 4 条）与 `:126`（判断清单第 71 条）也一样。
- 链式实测：`cf/tl_vyaml_chain.py`，我自己写的。
  - 基底是主仓真实的 `ab-suite/`，origin 用临时裸仓。
  - 顺延按第 71 条第 (1) 点的做法，落在合并提交里。
  - 原样输出：
```
[1st TASK-029] {"ledger_reading": "1.5.0", "origin_now": "1.6.0", "feature_version": "1.6.0", "v2.9 class": "不等"}
[restart TASK-029 after 顺延] {"ledger_reading": "1.5.0", "origin_now": "1.6.0", "feature_version": "1.7.0", "v2.9 class": "不等"}
```

**失败场景**：
1. 5.1 读到 1.5.0，取 1.6.0。
2. 读数之后，他轨把 `origin/master` 升到 1.6.0。5.7 并入时冲突，判「不等」，owner 裁顺延。本轨改为 1.7.0，在合并提交里落地，然后从 5.7 开头重走。
3. 在此期间，另有他轨只加 eval、改了计数、没有升号。重走时再次并入，又冲突。
4. `origin/master` 此刻是 1.6.0，台账读数是 1.5.0，于是判「不等」。执行者照原文呈报「读数之后又升了号，请定顺延与否」。
5. 实际上，上次顺延以来并没有新的升号。正确分类是「相等」：保留 1.7.0，重算计数。owner 若照问法再次顺延，就会跳过 1.7.0。

执行者会停在第 6 项，有合法的下一步，不会自行跳号，所以与 R9 同机制的那一条同理，定 minor。

**三态**：

| 版本 | 结果 |
|---|---|
| v2.8 | 所有冲突都问「顺延与否」，没有分类 |
| v2.9 | 第一次冲突分类正确；一经顺延，之后的 `version.yaml` 冲突都判「不等」（origin 的号只增不减，永远不会再等于旧读数） |
| 目标 | 顺延落地后，读数改记为顺延所依据的 origin 值；同一链式情形判「相等」 |

**建议修法**：
- 在 TASK-023 该条「不等」分支末尾补半句：「owner 裁顺延并落地后，台账读数改记为 `origin/master` 此刻的 version 及其 SHA；之后的比较一律用最新一条读数」。读前必看第 4 条同步。
- 同一句还能覆盖另一种情形：TASK-023 因第 6 项从开头重走而重新读数时，台账里会有两条读数。

**键注**：本条与 `c2513059` 是同一机制。`c2513059` 所述的 B.1–5.1 场景已经闭合（见对账）。本条是 v2.9 的新规则在「不等 → 顺延」这条支路上带出的新缺口，所以另立一个键。

### m2 `21d502b5` · minor · issue · documentation · scope `detailed-tasks.yaml TASK-025`

**一句话**：v2.9 新写了「原当前发布行只把标签改为 (旧)，其余字不动」。当前一版的发布行带裸 issue 引用时，这句与 hard_constraints 第 12 条、content-integrity §4.4、TASK-026 第一次自检三处规定互相冲突。

**证据**：
- yaml `:2084` 原文：「原当前发布行只把标签改为 > **发布日期(旧)**:, 其余字不动」。
- yaml `:214`（hard_constraints 第 12 条）：「新写或改动的文字: issue / PR 引用写 <org>/<repo>#<n>」。
- `standards/conventions/content-integrity.md:181-182`：「新写或本次改动到的文字按上面两条写; 存量文档不做批量回改, 改到哪段顺手改哪段」。
- yaml `:2100`（TASK-026 第一次自检）：
  - 导出 `git -C aria diff <aria 起点>..HEAD` 的 + 行，再跑 `check_bare_issue_refs.py`。
  - 「退出 1 = 有命中, 逐条改为全限定写法或注明属 Rule #N 例外」。
  - 改了标签的 (旧) 行也是 + 行，会被一起检查。
- 先例：`189240f` 与 `9003a82` 改标时，把「(aria-plugin#194)」「(aria-plugin#197)」原样保留了。我用脚本核过，四次先例里改标后的行都逐字出现在新文件中。
- 实测：
  - 在 aria `189240f` 的临时克隆上，照 v2.9 的写法模拟一次发版。那一版的当前发布行含「(aria-plugin#197)」。
  - 导出 + 行后自检，原样输出：
```
  relabel_added.txt:3 #197  +> **发布日期(旧)**: 2026-09-13  # patch: v1.73.2 state-scanner 扫描后本地协调 ref 不更新却报已刷新 (aria-plugin#197) — 
裸 issue 引用: 1
rc=1
```
  - 对照：`5215cf2` 的当前发布行（VERSION:4）改标后自检，结果为「裸 issue 引用: 0」、rc=0。
  - 所以本轨若直接在 v1.74.0 之上发版，不会触发。只有 B.1 之后另有一次发版、且那一版的发布行带裸引用时才会触发。

**失败场景**：
- 执行者照 TASK-025 只改标签，5.4 的自检报 1 处。
- TASK-026 要求把它改成全限定写法，这就动了「其余字」，与 TASK-025 的字面相反。
- 若坚持「其余字不动」，就违反 hard_constraints 第 12 条。而且 TASK-026 能注明的例外只有 Rule #N 一类，这里注不了。
- 无论哪种做法，九个取值点都不受影响：旧行不是取值点，终核照常通过，所以定 minor。

**建议修法**（二选一）：
- 在 TASK-025 该句后补一句：「(旧) 行内若有裸 issue 引用，按 hard_constraints 第 12 条补全为全限定，不算违反『其余字不动』」。
- 或在 TASK-026 第一次自检里写明：只改了标签的行，照 §4.4「改到哪段顺手改哪段」处理。

## 对账

| 键 | 判定 | 本席亲验证据 |
|---|---|---|
| `c2513059`（新内容） | closed | 见下方 (1) |
| `eac9f91d` + `6ff5eb7e` | closed | 见下方 (2) |
| `4fb29366` | closed | 见下方 (3) |
| 发版终核逐个取值点（R9 五席共同风险第 1 条，owner 纳入） | closed | 见下方 (4) |

**(1) `c2513059`**
- 落点：
  - yaml `:2032` 改为：B.1 之后他轨的升号，不论落在读数之前还是之后，都最先在 TASK-029 前置条并入时显形。冲突文件含 `version.yaml` 时，先比 origin 此刻的号与台账读数：
    - 相等 ⇒ 呈 owner 确认「保留本轨号、两轨 changelog 按版本序并存、在合并树上重算两个计数」，并在那次的合并提交里落地。
    - 不等 ⇒ 才问顺延与否。
  - tasks.md `:20` 与 `:126` 同口径。
- 前提核实：我用脚本枚举了 31 个任务里的全部 merge 动作。主仓把 `origin/master` 并入 feature，只发生在 TASK-029 前置条（yaml `:2167`）与 TASK-030 的同步合并；TASK-023 的「开 AB 会话之前」条并入的是 aria。
- 独立实测：`cf/tl_vyaml.py`，自写，没有用执笔的脚本。原样输出（摘行）：
```
[B 他轨升号在 B.1 之后、读数之前] {"reading": "1.6.0", "ours": "1.7.0", ... "unmerged": ["aria-plugin-benchmarks/ab-suite/version.yaml"], "origin_now": "1.6.0", "class": "相等", "resolved_version": "1.7.0", "changelog_top": ["1.7.0", "1.6.0", "1.5.0"], "counts_file": [32, 86], "counts_real": [32, 86], "commit_attribution": [0, "{\"verdict\": \"ok\", \"commits\": 2, \"kinds\": [\"sync-merge\", \"own-release-sync\"]}"]}
[A 他轨升号在读数之后] {"reading": "1.5.0", "ours": "1.6.0", ... "origin_now": "1.6.0", "class": "不等"}
[C 读数前后各升一次] {"reading": "1.6.0", "ours": "1.7.0", ... "origin_now": "1.7.0", "class": "不等"}
[E 他轨读数之前只加 eval 改计数] {... "origin_now": "1.5.0", "class": "相等", "resolved_version": "1.6.0", ... "counts_file": [32, 87], "counts_real": [32, 87], "commit_attribution": [0, "{... \"sync-merge\", \"own-release-sync\"]}"]}
[D 无他轨改动] {"reading": "1.5.0", "ours": "1.6.0", "is_ancestor_rc": 0}
```
- 结论：新判据能把两类冲突分开。解法产生的合并提交判 `sync-merge`，不会触发第 16 项。代码核实：yaml `:744` 对多亲提交只检查第二个及之后的父提交是否在基准上。
- 遗留：m1。

**(2) `eac9f91d` + `6ff5eb7e`**
- tasks.md `:36`：读前必看第 20 条的执行口径列追加了「aria 发版文件为六个 (含 README.zh.md), proposal :366 / :450 的「aria 5 文件」作废」。我用脚本核过，读前必看仍是 24 条。
- tasks.md `:120`：判断清单第 65 条的链接注补上了这一落点与相应代价。
- proposal 复读：`:366` 与 `:450` 各有一处「aria 5 文件」，全文只有这两处。
- 附注，不计 finding：第 20 条的 proposal 列仍只写 `:449-450`，按行号 `:366` 反查时会先落到第 3 条。执行口径列已经点名了两处，不影响执行。

**(3) `4fb29366`**
- 落点五处齐全：
  - yaml `:235`：第 17 项，核定义与打后核验各一支。
  - yaml `:2192`：TASK-030 的 C.2.4.5 条，同样两支。
  - tasks.md `:154`：等待点第 17 行。
  - tasks.md `:214`：5.8 行。
  - tasks.md `:121`：第 66 条链接注。
- 「调用本身失败」判据的依据：
  - 包装脚本头注释 `:11-18` 写明了退出码约定。
  - 只有 2xx 且传输完整时才退出 0（内网 `:258`，外网 `:311`）。
  - 4xx / 5xx 与外网的 3xx 都退出 2，两端都不可达时退出 1。
- 与闸的判定一致：`submodule_gate.sh:147` 是 `resp=$(forgejo GET ...) || return 1`，`:148` 再 grep 标签名。
- 我自建了 7 态垫片（不联网，子进程只给最小环境）。原样输出：
```
attached | gate_rc=0 | plan=有
none | gate_rc=1 | plan=没有
empty | gate_rc=1 | plan=没有
unreach | gate_rc=1 | plan=调用失败(rc=1)
http500 | gate_rc=1 | plan=调用失败(rc=2)
html200 | gate_rc=1 | plan=调用失败(解析不成)
jsonobj | gate_rc=1 | plan=调用失败(非列表)
```
- 结论：计划只在闸会放行时才「重跑闸」。四种调用失败的形态下，闸都不放行，计划也不重跑，两者不冲突。

**(4) 发版终核逐个取值点**
- 落点：
  - yaml `:2084`：写出了九个取值点、各自的锚点、两处新写的位置与先例。
  - yaml `:2123`：TASK-027 第 6 步改为逐点核。
- 独立取值器：我按计划原文另写了 `cf/tl_points.py`，对克隆里全部 22 个 v1.66.0 – v1.74.0 tag 各取九点。
  - 零处取不到。
  - 与 tag 号不等的只有真实漏改：v1.66.0 – v1.71.1 的代码块是 1.47.0、README.zh.md 是 1.41.0；v1.73.3 的代码块是 1.73.2。
- 反事实：`cf/tl_counterfactual.py`，在 aria `5215cf2` 上模拟发版到 1.75.0。原样输出：
```
[未改号] 每文件一值: 不通过 | 九点: 不通过 [...九点全部...]
[全改] 每文件一值: 通过 | 九点: 通过
[只漏改 VERSION 代码块] 每文件一值: 通过 | 九点: 不通过 ['VERSION code block']
[只漏插当前发布行] 每文件一值: 通过 | 九点: 不通过 ['VERSION release line']
[只改 VERSION 头部 (漏代码块+漏插发布行)] 每文件一值: 通过 | 九点: 不通过 ['VERSION release line', 'VERSION code block']
[只漏改 marketplace 第二处] 每文件一值: 通过 | 九点: 不通过 ['marketplace plugins[aria].version']
[只漏改 marketplace 顶层] 每文件一值: 不通过 | 九点: 不通过 ['marketplace .version']
[只漏改 README.zh.md] 每文件一值: 不通过 | 九点: 不通过 ['README.zh.md']
[只漏加 CHANGELOG 新节] 每文件一值: 不通过 | 九点: 不通过 ['CHANGELOG first section']
全改态 grep -c -F 1.75.0 六文件: 9 | 行命中: 9
```
- 锚点事实：
  - `5215cf2` 上，九个取值点恰是 `git grep -n -F 1.74.0` 的九处命中；`1cb3872` 的代码块在第 76 行，值为 1.73.2。
  - 不带「(旧)」的发布行有 20 条：首条在第 4 行，其余 19 条是 1.47.0 – 1.60.0 的旧行。
  - 代码块锚点与 `main-project-version-consistency.py:40` 的正则同形。
  - 四次先例逐字核对：新行都插在第 4 行（头部版本行之后），原当前行改标后原样保留。
- 遗留：m2。

## 对「改变执行者动作的改动」的逐条判断

1. **`c2513059` 的撞号分类：改法正确。**
   - 分类可以证伪：A / B / C / E 四态分得开（见对账 (1)）。
   - 解法落在合并提交里，判 `sync-merge`；没有新增外向动作。
   - 「相等」一类给的只是请 owner 确认的建议解法，与第 6 项「解法由 owner 定」不冲突。
   - 遗留：m1。
2. **逐个取值点终核：改法正确。**
   - 三态分得开（未改号为红，全改为绿，漏改代码块为红）。
   - 锚点对真实数据零处取不到。
   - 与第 3 / 6 步的 `comm -23` 互补：后者守的是旧小节没丢。
   - 遗留：m2。
3. **`4fb29366` 的标签 GET 调用失败分支：改法正确。**
   - 7 态垫片下，计划的「重跑与否」与闸的「放行与否」逐一一致。
   - 核定义时调用失败不再被读成「仓级没有」，少了一次不必要的建标签外向写。

**其余改动与未改动文本之间的接缝**：
- m2：新写的「其余字不动」与 hard_constraints 第 12 条、TASK-026 之间。
- 第 20 条 proposal 列的行号：见对账附注，不计。
- tasks.md `:6` 的 Status 行尾「— 待主控核验」：沿用 v2.8 的写法，提交后即过期，不影响执行，不计。
- 追认注：我对照 v2.8 执笔报告的「请裁项」逐条核过，对应关系是 1↔69、2↔70、3↔65（发布日期一句）、4↔66、5↔68，第 6 条记在 revision_log，全对。
- 结构化比对（v2.8 对 v2.9）：
  - metadata 只有 title / container / owner_gates（仅第 17 项）/ revision_log（前 66 条相等，追加 6 条）四个键变了。
  - 任务里只有 TASK-023 第 [2] 条、TASK-025 第 [2] 条、TASK-027 第 [6] 条、TASK-030 第 [4] 条各变一条。
  - 依赖、工时、agent、deliverables 都不变；依赖只指向前序任务。
  - 等待点表 19 行，与 owner_gates 的编号逐项相等；判断清单 72 条连续。
- 归档门：v2.9 与 v2.8 的 `--gate` 输出只在 `d_payload` 的 5.8 一行不同，verdict=pass，warnings 为 0。
- 新增行扫描：禁用字形 0、NUL 0、裸引用 0（`check_bare_issue_refs.py` 退出 0）。

## 对执笔人自报薄弱点的表态

1. 原文：A1 的分类没有从停点（TASK-029 前置条、第 6 项）指回来，执行者若只看停点，会中性呈报。**可接受**。读前必看第 4 条也载有这一分类；漏看时退回到 v2.7 的中性呈报，方向安全。仍建议补一句指回（见请裁第 4 条）。
2. 原文：相等类的解法没写 `last_modified` 取哪一侧。**可接受**。这是信息性字段，不参与任何判据：TASK-030 合并后复核只比计数、version 和 changelog 顶条。我的临时仓取本轨的值，复核全部通过。
3. 原文：A1 实测里的他轨改动是模拟的，真实 T4 还会在 `ab-suite/trigger/` 下加套件。**可接受**。10CG/Aria#211 归档 proposal `:116` / `:136` 写明 T4 是新增 `trigger/openspec-archive.json` 加升版，`trigger/` 下的文件不进 `ls ab-suite/*.json` 的计数。冲突只取决于两侧都改了 version 行，我另写的临时仓结果相同。
4. 原文：B 只核取值，不核原行是否改标「(旧)」，原位改号也能过。**可接受**。旧行不是取值点，原位改号只会少一行发布史，不影响任何对外的版本值；TASK-025 已明写要新插一行。改标这句另有 m2。
5. 原文：B 的取值函数是执笔自己写的。**可接受**。我按计划原文另写了一个取值器，22 个 tag 与 9 态反事实的结果与执笔逐项一致。
6. 原文：A3 的垫片不是真实的网络失败，包装脚本若改了退出码约定，这句会漂移。**可接受**。我实读了包装脚本：只在 2xx 且传输完整时退出 0。计划写的是「退出非 0」而不是具体的码，只要 2xx 仍退出 0，这句就仍然成立。
7. 原文：B 的历史核验只覆盖 22 个 tag。**可接受**。这 22 个已经覆盖了代码块与 README.zh.md 两类真实漏改，足以证伪锚点；我的克隆里 tag 也只有 v1.6.0 与 v1.66.0 起的这些。

## 对执笔请裁 6 条的表态

1. 原文：判断清单第 71 条的两点补定（计数重算放进合并提交，不另起提交；「相等」也覆盖只改计数的冲突）。**赞成执笔取舍**。我实测合并提交判 `sync-merge`；另起一个只改 `version.yaml` 的单亲提交必须带 trailer，多一个漏写即停第 16 项的面。
2. 原文：第 72 条第 (1) 点，当前发布行说明里的号算取值点。**赞成执笔取舍**。四次先例都新插了这一行；我的反事实「只漏插当前发布行」在每文件一值时判通过，只有逐点才判红。
3. 原文：A2 登记在读前必看第 20 条，而不是第 3 条。**赞成执笔取舍**。文件数属于发布面；可以顺手把 `:366` 补进第 20 条的 proposal 列（对账附注），不影响执行。
4. 原文：TASK-029 前置条与第 6 项不加指回分类的锚点。**赞成备选**，即在 TASK-029 前置条的冲突分支补半句「冲突文件含 version.yaml 时按 TASK-023 的 version.yaml 条分类后呈报」。理由：分类是「呈报前」的动作，执行点在 5.7 的停点，按任务分解的局部性，应在停点处看得见；代价只有一句。可以随下一次必要的返修一并做，不必单为它开一轮。
5. 原文：tasks.md 的 5.3 / 5.5 行不写「九个取值点」。**赞成执笔取舍**。粗粒度行与 yaml 不冲突，yaml 是单一 SOT；加括注反而多一个两视图同步面。
6. 原文：hard_constraints 第 14 条 (3) 的已知形态清单没有补入「forgejo 退出 0 但返回解析不成 JSON 列表」。**赞成执笔取舍**。这份清单本来就不穷举：TASK-024 快照条自 v2.5 起的「forgejo GET 另须输出可解析的 JSON 数组」也不在其中。该款的义务是把形态写进对应条目，v2.9 已写进第 17 项与 TASK-030。

## 风险 / 疑问

（不计入 finding）

1. **主仓侧 16 个版本点，存在与 R9 共同风险第 1 条同类的盲区。**
   - TASK-029 只要求「逐处 grep -n 实测后改」，改完后没有逐点等于新号的终核。
   - 三条版本类 check 我都读了 command，只覆盖 16 点里的 6 点：`README.md:8` 徽章、三份 i18n 的 `:3` translated-from、两份架构文档各一行。
   - 其余 10 点漏改时机械层看不见：`README.md:242`、三份 i18n README 的 `:10` 与 `:244`、`CLAUDE.md:138` / `:142`、`VERSION:24`。
   - 决策单第 6 项的依据只点了 aria 六文件，所以不在本轮范围。建议 owner 定是否给 TASK-029 补一条逐点终核（口径同 TASK-027 第 6 步，成本很低）。
2. **撞号分类只写在 TASK-029 前置条这一个显形点。** TASK-030 的同步合并若同样冲突（R9 tl 风险 3，仍然没有编号停点），同一比对照样适用，但目前没有文字把分类延伸过去。
3. **「相等」一类的建议解法只覆盖 `version.yaml`。** 若他轨同时改了 `ab-suite/audit-engine.json`，两个文件一起冲突时，后者的解法仍全由 owner 定。方向安全，但呈报时需要一并列出。
4. **B.1 之前需要推送。**
   - `c271cfe`（只含 `.aria/decisions/`）与 `59a3e9b` 仍只在本地，两个远端的 master 都在 `d7ab0c0`。
   - 我在副本里跑 `commit_attribution d7ab0c0 59a3e9b`，得到 `{"verdict": "stop", "commits": 2, "kinds": ["own", "foreign"]}`，与 R9 共同风险第 3 条同形。
   - 若到 B.1 时仍未推送，TASK-001 的回落路径会停在第 16 项。
5. **流程记录**：
   - 对两份共享副本，我只做过 `du -sh` 与 `cp -a`，没有在其中运行任何 git 命令或脚本。
   - 真仓里做过的操作：`git ls-remote`、只读的 `sha256sum`，以及约 17:21:54 UTC 的一次 `git -C /home/dev/Aria status --porcelain`（用来确认真仓干净）。这一次违反了「真仓只读、远端事实只用 ls-remote」的精神，特此说明。
   - 那次 status 的结果：输出为空，HEAD 为 `59a3e9b`；`.git/index` 的 mtime 仍是 16:50:45（没有重写），`.git` 目录的 mtime 变为 17:21:54。
   - forgejo 包装脚本只读了文本，没有调用。

## Verdict

**PASS** · counts `0C/0M/2m` · **Vote: PASS**

## 是否足以开始 Phase B

**足以**。没有 critical / major。两条 minor 都在条件路径上：m1 要在「顺延之后再冲突」时才触发，m2 要在「前一版发布行带裸引用」时才触发，都可以随下一次必要的返修修掉，或先在台账里记下处置口径。

进 B.1 之前还要两件事：
- 按决策单 2026-09-29 第 5 项，由 owner 确认收敛。
- 经授权推送 `c271cfe`、`59a3e9b` 与 R10 报告；不推送，TASK-001 的回落路径会停在第 16 项。