---
checkpoint: post_planning
mode: convergence
rounds: 10
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-29T17:37:38.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = c26e35ee2502f7db（与派单要求一致，已核对）。

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md`（全文 269 行，含读前必看表 1-24、三处重写、判断清单 1-72、等待点表 1-18、5.1-5.9 checkbox、SC 映射表首段）
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml`（全文 2230 行；用 `PyYAML` 独立解析并与 `git show f231287:...`（v2.8）做结构化字段级比对，不复用执笔人 `struct_diff.py`）
- `git diff f231287 59a3e9b -- openspec/changes/pre-merge-completeness-gate-change-scope/`（v2.8→v2.9 全部改动，152 行，两文件，逐行读完）
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` 第 366、450 行（`git diff` 未触及部分，独立核实读前必看第 20 条依据的原文）
- `.aria/decisions/2026-09-29-199-r8-and-v2.8-owner-rulings.md` 全文
- `.aria/audit-reports/post_planning-R9-2026-09-29T115626-000Z-pre-merge-completeness-gate-change-scope-aggregated.md` 全文
- `.aria/notes/2026-09-17-199-a2-a3-tooling/writer-reports/v2.9-dispatch.md`、`v2.9-writer-report.md` 全文
- `aria/skills/phase-c-integrator/scripts/submodule_gate.sh` 第 96-158 行（`check_override_trailer` / `check_pr_label` / `check_override`，实读源码，非转述）
- `/home/dev/.npm-global/bin/forgejo`（真实 CLI wrapper，只读头部注释核实退出码约定 0/1/2/3，非仓内文件但用于核验 A3 的事实依据）
- aria 子模块 `5215cf2`（v1.74.0）：`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`VERSION`、`CHANGELOG.md`、`README.md`、`README.zh.md`（`git grep -n -F 1.74.0` 实跑，逐处核对九个取值点）
- aria 子模块 `1cb3872`（v1.73.3）：`VERSION`（`git -C aria show 1cb3872:VERSION`，核对「## 版本号」代码块历史漏改先例）
- `.aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py` 的 v2.8→v2.9 diff（`git diff --stat` 与 `@@` 块清单，只作佐证）
- 独立用 `aria/skills/state-scanner/scripts/check_bare_issue_refs.py` 对本轮新增行重跑裸引用检查（未复用执笔人产物）

实跑环境：全部命令在 `/tmp/claude-1000/-home-dev-Aria/cbe6f623-7c3c-4217-8ccb-fd07680a5525/scratchpad/audit-R10-qa-engineer/` 下我自己 `cp -a` 出的副本 `Aria/` 里执行；两份共享副本（`p199-r10/base/Aria`、`p199-r10/state-base`）只做过一次 `cp -a`，未在其中运行任何命令。真仓 `/home/dev/Aria` 全程未做任何 git 写操作。

## Findings

| id | severity | type | category | scope | 摘要 |
|---|---|---|---|---|---|
| m1 | minor | issue | implementation | detailed-tasks.yaml TASK-029 | `version.yaml` 撞号新判据（判断清单第 71 条 / TASK-023）在 5.7 实际触发点（TASK-029 前置条、`owner_gates` 第 6 项）未留锚点指回 |

**m1 详情**

- **证据**：
  - `detailed-tasks.yaml:2032`（TASK-023 的 `version.yaml` 条）与 `tasks.md:126`（判断清单第 71 条）完整写出「相等/不等」二分类判据与解法，两处均可查。
  - `detailed-tasks.yaml:2167`（TASK-029 唯一改动的「前置」verification 条）原文只到「冲突 ⇒ git merge --abort, 停下上报 (owner_gates 第 6 项)」为止，未提「若冲突文件含 version.yaml，先比对台账读数」。
  - `tasks.md:142`（等待点表第 6 项）原文仅「先例指针 aria ec72175（主仓侧冲突无先例指针，解法由 owner 定），owner 确认后重走」，同样未指回判断清单第 71 条。
  - 独立结构比对（`PyYAML` 逐字段比较 v2.8/v2.9）确认 TASK-029 本身在本轮**未被改动**（改动只落在 TASK-023/025/027/030 四个任务），`owner_gates` 19 项里唯一变化的是下标 17（对应「17 ·」标签项，非「6 ·」项）——证实这处缺口是 v2.9 遗留、非我误读旧文本。
  - 执笔人自己在「自报薄弱点」第 1 条与「请裁项」第 4 条中已如实披露同一缺口，并给出「只改善可发现性、不改动作」的理由。
- **失败场景**：执行者跑到 5.7（TASK-029）遇到 `version.yaml` 冲突时，若只字面执行 TASK-029 与等待点表第 6 项（未主动回忆或重读判断清单第 71 条 / TASK-023 台账），会把冲突笼统上报 owner，不附「`origin/master` 此刻取值 vs 台账读数」的比对结果。owner 在信息不全时可能被迫直接回答「是否顺延」，而这正是 c2513059 原本要修复的错误分类路径——即同一个错误结论换了一条路径复发的风险（该风险是否兑现取决于执行者是否主动带上台账信息；本计划别处的「停下上报」惯例通常要求附带相关台账，故此风险有限、非必然）。
- **它怎么会红**：基线（v2.8 前）——TASK-029 冲突文本本就通用，无分类；目标（v2.9 期望）——冲突文本应能让执行者在**不额外回忆**的情况下正确套用第 71 条判据；坏实现（现状）——分类逻辑齐全但只挂在 5.1/TASK-023 一侧，5.7/TASK-029 一侧无锚点，构成单向引用（第 69 条→第 71 条有链接注，但「TASK-029 前置条→第 71 条」无）。
- **建议修法**：在 `detailed-tasks.yaml:2167`（TASK-029 前置条）与 `tasks.md:142`（等待点表第 6 项）各补一句「冲突文件含 `version.yaml` 时按 TASK-023 的 `version.yaml` 条 / 判断清单第 71 条分类呈报」，与判断清单第 69 条已有的链接注同构。成本极低（各一句话），且与本文档既有的「条目序号引用改锚点式」惯例（判断清单第 47 条）一致。

其余检查（A2 proposal 差异登记、A3 标签 GET 失败分支、B 逐取值点终核、结构范围、`revision_log` 前 66 条、禁用字形/裸引用）均未发现 critical 或 major 级问题，证据见「对账」节。

## 对账

逐条为我本人独立复核结论（未沿用执笔或主控结论）：

**`c2513059`（TASK-023 撞号新分类）—— closed（附带 m1 这一相邻缺口，不影响该键本身闭合）**
独立推演 git 三路合并语义：merge-base 处 version 为 X，若「读数之前」他轨已把 origin/master 推进到 X+1，则 TASK-023 据此读到 X+1、写入 X+2；此时 base=X、feature 侧=X+2、origin 侧=X+1，两侧都相对 base 改了同一行且取值不同 ⇒ 必冲突（与执笔人 `W/cf/a1_vyaml.py` 报告的 `merge_rc=1` 一致，我未重跑该脚本，但用独立的三路合并逻辑推导得到相同结论）。此时按新判据比较「`origin/master` 此刻值（X+1）」与「台账读数（X+1）」⇒ 相等 ⇒ 正确判定「未新增撞号」；若读数之后又有新升号（origin 现值 ≠ 台账读数）⇒ 不等 ⇒ 正确转入「请裁顺延」。两分支与 v2.8 旧逻辑（一律问顺延）相比确有修正，逻辑自洽。另核对 `detailed-tasks.yaml:830`（revision_log v2.9 条）与判断清单第 71 条逐字一致。**唯一缺口是 m1**（分类逻辑未从触发点指回）。

**`eac9f91d` + `6ff5eb7e`（proposal「aria 5 文件」差异登记）—— closed**
独立读 `proposal.md:366` 与 `:450`，确认原文字面确写「aria 5 文件」（片段：`…照执行会把 aria 5 文件 + 主仓 16 个版本点…`；`…aria 5 文件 + 主仓 16 个版本字符串点…`）。`tasks.md:36`（读前必看第 20 条）已补登「aria 发版文件为六个…proposal :366/:450 的『aria 5 文件』作废」。独立对 `tasks.md` 与 yaml 全文 `grep` 「五个文件/五文件/5 文件」，除本行引用与 `revision_log` 历史条目（v2.3/v2.4/v2.8/v2.9 自身的记录，均为如实的历史引文）及判断清单第 65 条对 `CLAUDE.md` 现状的如实引用外，无其它遗漏点。

**`4fb29366`（标签 GET 调用失败分支）—— closed**
实读 `aria/skills/phase-c-integrator/scripts/submodule_gate.sh:128-150`（`check_pr_label`）确认 `resp=$(forgejo GET ... ) || return 1` ——闸自身对调用失败与「无标签」在返回值层面本就不可分辨（fail-closed by design），与计划里「执行者手动跑的两处 GET 失败时不当作『没有』也不当作『没挂上』」是两个独立的判断点（分别在授权前的定义核实、授权后的挂载核实），不冲突。实读 `/home/dev/.npm-global/bin/forgejo` 头部注释确认退出码 0=2xx/1=两端点不可达/2=4xx-5xx/3=凭据被拒的文档与执笔人报告逐字一致。四处落点（`owner_gates` 第 17 项 `tasks.md:154`、TASK-030 `detailed-tasks.yaml:2192` 附近、等待点表第 17 行、5.8 行 `tasks.md:214`）经独立 `grep` 确认四处新增文字实质一致（核定义失败→视为核不到、不据此建定义；打后核验失败→不重跑、既不当没挂上也不当已挂上）。

**R9 五席共同风险第 1 条（发版终核逐取值点）—— closed**
独立在 aria `5215cf2` 上跑 `git grep -n -F 1.74.0 -- .claude-plugin/plugin.json .claude-plugin/marketplace.json VERSION CHANGELOG.md README.md README.zh.md`，命中恰好 9 处，与计划列出的 9 个锚点一一对应。独立核实 `VERSION` 头部行 `> **版本**:` 全文件唯一（`grep -c` = 1），`marketplace.json` 的 `plugins` 数组当前只有 1 个条目（`aria`），两个「第一处匹配」锚点在当前数据下均无歧义。独立核实「当前发布行取第一条」锚点的鲁棒性：`grep -c '^> \*\*发布日期\*\*:'` 与去掉「(旧)」标记后的计数均为 20，其中新发布行插入后始终排在最前（插入点紧跟头部版本行）——不会因为后续再次发版而失效。独立核实历史先例：`git -C aria show 1cb3872:VERSION` 确认 v1.73.3 头部为 1.73.3、「## 版本号」代码块仍为 1.73.2，与 10CG/Aria#195 判断清单第 35 条所述一致，构成「每文件取一个值会漏检」的真实历史证据。`TASK-029` 的「16 个版本点」（`detailed-tasks.yaml:2169`）核实为逐点枚举（README.md 两处 / 三份 i18n README 各三处 / CLAUDE.md 两处 / VERSION 一处 / 两份架构文档各一处 = 16），本就没有「每文件一值」的旧问题，「不受影响」的说法成立。

## 对「改变执行者动作的改动」的逐条判断

1. **`c2513059`（TASK-023 撞号分类）** —— 改法基本正确，有问题：TASK-029/`owner_gates` 第 6 项未指回分类逻辑（即 m1，已计入 Findings）。核心「相等/不等」判据本身的正确性已独立验证（见「对账」）。
2. **逐个取值点终核（B）** —— 改法正确。九个取值点的锚点定义、"取第一处匹配"的鲁棒性、历史先例均已用真实数据独立核验，未发现遗漏或歧义。
3. **`4fb29366`（标签 GET 调用失败分支）** —— 改法正确。已用真实 `submodule_gate.sh` 源码与真实 `forgejo` wrapper 头注释独立核验，四处落点一致。

**v2.9 其余改动是否与未改动文本产生新接缝**：独立结构化比对（`PyYAML` 逐字段）确认本轮唯一改动的 4 个任务（TASK-023/025/027/030）均只改了各自 `verification` 列表中的 1 条、列表长度不变；`metadata` 除 `title`/`container`/`owner_gates`（仅第 17 项）/`revision_log`（仅追加）/`updated` 外逐键相同；`revision_log` 前 66 条与 v2.8 逐字相同（`PyYAML` 列表逐项 `==` 比较，非文本 diff）。未发现除 m1 外的新接缝。

## 对执笔人自报薄弱点的表态

1. 「A1 的分类没有从停点指回来……仍安全，但丢了分类」—— **不可接受，已提升为 Findings m1**：虽然执笔人对"最坏后果有限"的判断我认同（故仍定为 minor 而非 major），但"仍安全"的前提是执行者会主动带上台账信息，这一假设未被文本本身保证，值得作为独立缺陷记录而非仅作自述。
2. 「A1 相等类的解法没写全：没写 `last_modified` 取哪一侧」—— **可接受**：独立核实真实 `version.yaml`（`aria-plugin-benchmarks/ab-suite/version.yaml`）确有 `last_modified` 字段，但计划全文没有任何检查读取或校验该字段，遗漏不会导致验收结论出错，留给 owner 确认时一并处理是合理取舍。
3. 「A1 实测里的他轨改动是模拟的……不受其余内容影响」—— **可接受**：模拟基于真实 `ab-suite/` 目录结构，且分类判据本身（只比较 `version` 字段取值）确实与 changelog/计数等其余字段内容无关，结论具备可推广性。
4. 「B 只核取值，不核原行是否改标『(旧)』」—— **可接受**：该限制已在判断清单第 72 条末句显式声明，且历史标记正确性不影响任何后续判据（无消费方读取该标记）。
5. 「B 的取值函数是我写的」—— **可接受，且已被本席部分缓解**：我用独立的 `git grep`/`grep -c` 命令重新核验了全部 9 个取值点位置与历史先例数据，未依赖执笔人的 `vpoints.py`，结论一致。
6. 「A3 的垫片不是真实网络失败」—— **可接受，且已被本席独立佐证**：我直接读取了真实 `/home/dev/.npm-global/bin/forgejo` 脚本头部的退出码文档（非垫片），与执笔人转述逐字一致，缓解了"约定可能漂移"的担忧本身不构成本轮缺陷。
7. 「B 的历史核验覆盖有限：只有 22 个 tag」—— **可接受**：这是复核范围的客观限制（早期 tag 在浅克隆里不存在），不影响当前 9 点判据对现有数据的正确性，且核验的核心目的（证明"每文件一值"确有历史漏检先例）已用 v1.73.3 这一个案例充分达成。

## 对执笔请裁 6 条的表态

1. 「判断清单第 71 条两点补定：计数重算放进合并提交、不另起提交；『相等』覆盖只改计数未升号的冲突」—— **赞成执笔取舍**：另起提交必须带 `Spec:` trailer 且漏写即判 `shared-only`（`detailed-tasks.yaml` 既有 `commit_attribution` 规则），并入现有合并提交是更少接缝的选择；「相等」覆盖计数变动一支，我独立验证过该分支不依赖 changelog/version 字段以外的内容，纳入合理。
2. 「判断清单第 72 条第 (1) 点：当前发布行说明里的号算取值点」—— **赞成执笔取舍**：已用真实四次发版 diff 模式（执笔人转述）及我自己对 `VERSION` 文件当前 20 条候选行、"取第一条"规则鲁棒性的独立核验，算作取值点是唯一能拦住"漏插当前发布行"这一失败模式的选择。
3. 「A2 登记在读前必看第 20 条而非第 3 条」—— **赞成执笔取舍**：第 3 条管版本号取值本身，第 20 条管发布面文件集合，两者概念上确属不同问题，归类合理。
4. 「TASK-029 前置条和第 6 项不加指回分类的锚点」—— **倾向赞成备选（建议补锚点）**：即 m1。执笔人「只改善可发现性、不改动作、但会给 R10 多一个接缝」的顾虑成立，但补一句锚点引用的改动面极小（不新增编号、不改变任何判据），风险收益比优于不补；供 owner 参考裁定，不阻塞收敛。
5. 「`tasks.md` 的 5.3/5.5 行不写『九个取值点』」—— **赞成执笔取舍**：与全文档"tasks.md 粗粒度、yaml 细粒度"的既定分层（文件头部 `Level: 3` 说明）一致，非本轮引入的例外。
6. 「`hard_constraints` 第 14 条 (3) 已知形态清单没有补入『forgejo 退出 0 但解析不成 JSON 列表』」—— **赞成执笔取舍（不改）**：该款自身声明「已知形态逐处写在对应条目里，不靠本条兜」，是一份辅助性索引而非权威判据来源；实际判据已完整落在 `owner_gates` 第 17 项与 TASK-030（已独立核实），遗漏该索引项不影响任何执行结论。

## 风险 / 疑问

- （不计入 finding）判断清单第 71 条「确认后照等待点 6 重做那次并入…再从 TASK-029 开头重走」一句信息密度很高：第二次执行到同一冲突点时，执行者需要记得"这次不再 abort，而是手动按解法解决冲突"。我逐字重读后认为逻辑自洽（先 abort 拿到 owner 确认，再重跑并在确认的解法下完成合并），但这依赖执行者对"重走"一词的正确理解；若未来还要再修订，建议把"这次不再 abort"这一点显式写出。
- （不计入 finding）R9 五席共同风险第 2-4 条（发布日期跨 UTC 日、标签列表 GET 无 `limit`、TASK-030 同步合并冲突无编号停点等）按决策单第 6 项明示不纳入本轮，v2.9 范围外观察第 1-7 条如实列出未动，我核对与决策单口径一致，不重复计入。
- （不计入 finding）`hard_constraints` 第 14 条 (3) 的目的是"已知 gotcha 索引"，本轮起该索引本身已出现至少一次滞后（见请裁项 6）；若后续版本继续新增此类分支而不同步索引，索引的可信度会逐渐降低，属于长期可维护性观察，非本轮问题。

## Verdict

**verdict: PASS**　counts: 0C/0M/1m　**Vote: PASS**

（无 critical、无 major，1 条 minor m1；按严重度口径「有 critical ⇒ FAIL；无 critical 有 major ⇒ PASS_WITH_WARNINGS；否则 PASS」，本轮判 PASS。）

## 是否足以开始 Phase B

**足以**——本轮 v2.9 相对 v2.8 的四处改动（TASK-023 撞号分类、TASK-025/027 逐取值点终核、TASK-030 标签 GET 失败分支）经独立核验逻辑正确、与真实源码/真实数据一致，结构范围precise（仅 4 个任务的各 1 条 verification、`owner_gates` 仅第 17 项、`revision_log` 前 66 条不变），未发现 critical 或 major 级问题；唯一的 m1（锚点缺口）属于可发现性问题而非正确性缺陷，不构成阻塞。