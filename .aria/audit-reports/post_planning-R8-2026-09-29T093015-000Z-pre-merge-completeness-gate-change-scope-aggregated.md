---
checkpoint: post_planning
mode: convergence
rounds: 8
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-29T10:48:08.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 0C/1M/7m
counts_dedup: 0C/1M/7m
sibling_probe: no_sibling_found
---

# post_planning R8 聚合 — pre-merge-completeness-gate-change-scope (10CG/Aria#199, A.2/A.3 v2.7 `7ef09ea`) — 未收敛 (1 Major)

> **被审对象**: `tasks.md` + `detailed-tasks.yaml` v2.7, 主仓 `7ef09ea`, 已推送 (origin 与 github 各自 `ls-remote` 与本地一致)。
> **本轮由来**: R7 已收敛 (五席全票 PASS, 0C/0M/6m)。owner 2026-09-27 裁定 (决策单 `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md` 第 3 项) 把 R7 六条 minor、各轮未处置 minor 与 `10CG/Aria#195` 合并后的基线平移合成 v2.7; 执笔报告列出 10 条可能构成实质改动的条目。**owner 2026-09-29 裁定: 为 v2.7 再开一轮 (即本轮), 范围只限 v2.7 相对 v2.6 的改动 (`git diff 320d523 7ef09ea`), 同时授权超出本审计周期 `max_rounds = 7`; 执笔实例的 11 条请裁等本轮之后一并裁。**
> **执笔**: v2.7 由 2026-09-28 新派的执笔实例出稿 (与 v2.4 – v2.6 的实例不是同一个), 主控独立核验一致性与可复跑性后提交。
> **Sibling probe (本轮入口, 派发前实跑)**: `status=ok` / `verdict=no_sibling_found`, github 156 份 / origin 161 份 proposal, 两端完整扫描无 cap。
> **drift-checker**: convergence 未 opt-in ⇒ 跳过, `drift_check_skipped: true`。
> **并发**: 2 席滑动窗口 (code-reviewer + tech-lead → qa-engineer → backend-architect → knowledge-manager)。code-reviewer 席沿用 R6 / R7 的独立复算流程 (先对 `git diff 320d523 7ef09ea` 逐 hunk 复算, 再读执笔报告)。派单写明「这不构成应当投 PASS 的暗示, 严重度口径与前七轮完全一致, 不因范围收窄而放宽或收紧」。

## drift_metrics (Step 0 anchor 快照)

- checkpoint: post_planning
- primary_goal: 把 Approved 的 10CG/Aria#199 proposal 分解为可执行的 Level 3 双层任务, 忠实落地决策单 2026-09-12 §2 的 10CG/Aria#199 表 13 行 (连同 §5) 与 Level 3 三处连带重写
- in_scope: 任务分解与粒度 / 依赖与执行序 / agent 分配 / 验收判据可证伪性 / 裁定与重写的执行口径 / 基线复核 / 外向动作与 owner 等待点 / 发布段 (本轮限 v2.7 的改动及其与未改动文字的接缝)
- out_of_scope_hints: proposal 设计取舍本身; 13 条裁定本身
- source_sha: `7ef09ea`
- drift_ratio: null (未 opt-in)

## 判定

| 席 | verdict | counts | vote | 一句话 |
|---|---|---|---|---|
| tech-lead | PASS | 0C/0M/4m | PASS | R7 六簇全 closed; B 组 `af5e1e47` 判 partially (新理由仍与源码不符); 四条 minor: PR 标签在仓级未定义 / 第 14 项理由 / TASK-001 比对区间 / TASK-023 与 TASK-029 撞号显形点 |
| backend-architect | PASS | 0C/0M/0m | PASS | 组 2 视角内唯一改动 `elapsed_ms` 深核正确; 其余落点属实 |
| qa-engineer | PASS | 0C/0M/1m | PASS | R7 六簇与 B 组 21 行全 closed; 一条 minor: phase-d 规则比对的「根本冲突」停点未编进 `owner_gates` |
| code-reviewer | PASS_WITH_WARNINGS | 0C/1M/2m | **REVISE** | 独立复算, 三态证据与 REGEN 均复现; 一条 Major: aria `README.zh.md` 进了基线记录却不在发版文件集; 两条 minor |
| knowledge-manager | PASS | 0C/0M/0m | PASS | 发布同步面、写法规范、映射表未见新问题; 对执笔自报薄弱点的表态与执笔清单错位 (见流程记录第 7 条) |

## Major 簇 (1)

| 定稿键 | 席位 | 内容与主控复核 |
|---|---|---|
| `69707662` | cr/M1 | v2.7 的 D 组 (基线平移) 把 aria `README.zh.md` 认定为「近几次发版都改它」的版本文件并写进 `baseline_rebase.aria_shifted`, 但发版任务的文件集仍是五个 —— TASK-025 的 deliverables 与改号条、TASK-027 第 6 步取号终核「五文件」、tasks.md 5.3「改版本 SOT 5 文件」均为 v2.6 原文、v2.7 未碰。照字面执行, 随插件分发的中文 README 版本行停在旧号, 终核「五文件等于新号」对这一漏改结构上不会红, 本计划跑的六条 custom check 也都不读这一行。**主控独立复核, 前提全部属实**: TASK-025 deliverables 恰为 plugin.json / marketplace.json / VERSION / CHANGELOG.md / README.md; aria `5215cf2:README.zh.md` 第 5 行为「版本: 1.74.0 \| 发布日期: 2026-09-28」; 最近四个改该文件的提交全是 `chore(release)` (v1.73.1 / v1.73.2 / v1.73.3 / v1.74.0); `10CG/Aria#195` 归档 `tasks.md` 判断清单第 34 条记 owner 2026-09-27 当场裁定「带上, 六个文件一次提交」; 上一会话收尾 handoff (`90a1351`) §2 把「CLAUDE.md 发版面写 5 文件而实际 6 文件」列为待 owner 定的通用口径。**性质**: 五文件集自 v1 即有; `10CG/Aria#195` 的 owner 裁定在 v2.6 之后; v2.7 的新记录让它与发版任务之间出现了可见的不一致 (接缝由 v2.7 产生, 底层缺口早于 v2.7)。席位给的修法二选一: (a) 按 `10CG/Aria#195` 先例把 aria 版本文件集写成六个 (TASK-025 / TASK-027 第 6 步 / 5.3 同改并登记判断清单); (b) 在 5.3 之前登记 owner 裁定点, 待通用口径定后再改号。两者都要求终核判据覆盖最终文件集。 |

## Minor (7 键, 无跨席同键)

| 定稿键 | 席位 | 内容与主控复核 |
|---|---|---|
| `749f8d15` | tl/m1 | owner 裁定的 C.2.4.5 override 默认路径 (PR 标签 `submodule-rollback-approved`) 缺一个前提: 该标签在 10CG/Aria 仓级未定义 —— 计划没要求事先核实, 没把「建标签定义」登记为外向动作, 打标签后也没有「标签确已挂上」的核验。闸 fail-closed, 不会误合并, 代价是白走一次授权往返。**主控实测**: `forgejo GET /repos/10CG/Aria/labels` 得 `['aria-auto', 'bug', 'feature', 'post-m0', 'stale']`, 无该标签 (组织级因令牌 scope 403, 未核)。**键注**: 与 R6 `749f8d15` 同键 (同 scope 同定级) 但内容不同 (R6 讲 trailer 的调用时机), 按 R2 先例并列保留。 |
| `af5e1e47` | tl/m2 | `owner_gates` 第 14 项为 `--include-terminal` 新写的理由 (「done / abandoned 不带它时被 collision 的终态过滤跳过」) 仍与源码不符: 该旗标只作用于 `linked_issue_overlaps` —— 「同一 linked issue、不同 track_id」的 advisory 重叠列表, 本轨同名 claim 在函数内直接跳过, 与本轨 claim 处于哪一终态无关。**主控实读** aria `5215cf2` `lib/collision.py:365-430` 与 `scripts/phase1_gate.py:1542-1552`, 属实。R3 `af5e1e47` 的建议句本身带着这个误读, v2.7 照建议落地一并继承。**键注**: 与 R3 `af5e1e47` 同键, 即该 minor 未闭合的部分 (见 Conflicted 第 1 条)。 |
| `b8cc29e0` | tl/m3 | TASK-001 基线复核条改为「与 v2.7 记录比对」, 但它实际跑的是 `301641b..<aria 起点>`, 而 `aria_shifted` 有 4 条的「v2.7 复测」值记的是 `1cb3872..5215cf2` —— 零漂移时两者也对不上 (席位实跑: `spec_complete.py` 在前一区间 +1/-1、后一区间空), 执行者会误报 4 个文件为新 diff 并写一份全零的偏移表。只多做、不漏。**主控实读**两处原文, 属实。 |
| `c2513059` | tl/m4 | v2.7 在 TASK-029 新加「改版本面之前先把主仓 origin/master 并入 feature」, `version.yaml` 撞号因此最先在这次并入时显形 (abort、停在第 6 项、解法由 owner 定), 而 TASK-023 该条仍写「以 TASK-030 合并时的冲突或合并后复读为准」「已被占 ⇒ 顺延」。结果在安全方向, 只是两处说法不一。**主控实读** TASK-023 该句原文, 属实。 |
| `5e83496e` | cr/m1 | v2.7 把 TASK-018 标题补成「SC-13、N1–N4 / N7 / N8 与四份 frontmatter」, 而 tasks.md 3.5 行仍是「N1 / N2 / N4 / N7 / N8」, 两层在 N3 上不一致 (v2.6 时两层同样不含 N3, 接缝由本轮造成)。执笔报告把它列为「范围外观察」, 席位不同意: tasks.md 在本轮可写集内。**主控实读** 3.5 行, 属实。 |
| `0c227bd6` | cr/m2 | `sc12_liveness.blind_spots` 与 revision_log 记「90a1351 实跑脚本缺失态: status=alive, L1 真, L2 与 L3 假」, 没注明是「未勾选」那一态; 已勾选态下 L3 为真 (席位用 `--force-checked` 实跑)。**主控实读** blind_spots 原句, 无「未勾选」限定, 属实。 |
| `266936b1` | qa/m1 | TASK-031 新增的 phase-d 规则比对分支「新 SOT 与手写路径根本冲突 ⇒ 停在本任务上报 owner」没有编进 `owner_gates` (18 项) 与等待点表, 而计划里同类停点基本都有编号; 该表作为停点唯一索引的完备性被打破。执笔自报薄弱点第 7 条已自陈。**主控实读**: 该句只在 TASK-031 verification, `owner_gates` 全文不含「根本冲突」或 `phase_d_sot`, 属实。 |

## R7 对账

**五席逐簇独立复核, 六簇五席一致 closed** (`6be9db6a` / `76949787` / `6e4535a3` + `ab143d74` / `ce6f31fc` / `bdce52c6` / `3de4b245`)。各席独立证据择要: tl 与 cr 各自按运行器解析器逐条核出 16 条 check 里可达「`##SKIP##` 配退出 0」的恰为 6 条 (与主控派单前的独立静态扫描一致); tl / qa / cr 各自用 CRLF 夹具复现两种 grep 在去 CR 前后的取值; cr 与 tl 各自复跑 v2 三态脚本 (含 N13 分叉态一对) 逐字节一致; km 构造空 `CLAUDE_CONFIG_DIR` 复现 `plugin-cache-currency` 的 `##SKIP##` 首行与退出 0。`3de4b245` 簇闭合, 但同一 override 路径上的标签前提另计为 `749f8d15` (不算该簇未闭合)。

## B 组 (R2 – R5 未动的 20 个键 / 21 行) 对账

五席对 21 行都核了「落点确实改了、修法对题」, 视角内的行深核。除一行外全部 closed:

- **B12 `af5e1e47`**: tl 判 partially (附源码证据), cr / qa / km 判 closed, ba 只做落点核验。主控裁断见 Conflicted 第 1 条: 采 tl, 未闭合部分计为本轮 minor `af5e1e47`。
- 另有四行 closed 但引出接缝, 已各自计为本轮 minor: B1 → `5e83496e`; B11 / B17 → `0c227bd6`; B20 → `c2513059`; B21 → `266936b1`。

## 10 条实质改动候选: 五席判断

| # | 候选 | tl | ba | qa | cr | km |
|---|---|---|---|---|---|---|
| 1 | `27cee280` 主仓 feature 先并入 | 正确 (接缝 → `c2513059`) | 视角外 | 正确 | 正确 (接缝已注, 不计 finding) | 正确 |
| 2 | `ae4753f5` phase-d SOT 比对 | 正确 | 视角外 | 正确 (停点编号 → `266936b1`) | 正确 | 正确 |
| 3 | `34b92188` elapsed_ms | 正确 | **正确 (深核)** | 正确 | 正确 | 视角外 |
| 4 | `9c0dcb27` N13 | 正确 (复跑) | 视角外 | 正确 | 正确 (复跑) | 视角外 |
| 5 | track-id 先去 CR | 正确 (夹具) | 视角外 | 正确 (夹具) | 正确 (实测) | 正确 |
| 6 | 对齐后重解析 | 正确 | 视角外 | 正确 | 正确 | 正确 |
| 7 | PR 标签默认路径 | 写法正确, 标签前提缺 (→ `749f8d15`) | 视角外 | 正确 (风险: 标签不分子模块的流程摩擦) | 正确 (风险: 标签可能尚不存在) | 正确 |
| 8 | 首行口径与占位符检查 | 正确 | 视角外 | 正确 | 正确 (实跑) | 正确 (实跑) |
| 9 | History 节交 `10CG/Aria#220` | 正确 | 视角外 | 正确 | 正确 | 正确 |
| 10 | D 组基线平移 | 比对口径有问题 (→ `b8cc29e0`) | 视角外 | 正确 | **有问题 (→ Major `69707662`)** | 正确 |

**汇总**: 10 条里 8 条在所有深核过的席位都判正确; 第 7、10 两条引出 finding (tl `749f8d15` / `b8cc29e0`, cr `69707662`)。五席均未判定任何一条改动推翻 proposal 或 13 条裁定。

## 执笔自报薄弱点 (10 条): 五席表态

- **第 5 条 (PR 标签只在垫片上测)**: tl 判不可接受 —— 垫片恰好掩盖了「仓级未定义该标签」这一真实前提, 计为 `749f8d15`; 其余席位判可接受。
- **第 7 条 (phase-d 停点无编号)**: qa 判不可接受, 计为 `266936b1`; km 判可接受但建议补编号; tl 判可接受并建议补一句外向动作写法; ba / cr 判可接受。
- 其余八条: 五席均判可接受 (km 的表态清单与执笔原文错位, 见流程记录第 7 条)。

## 执笔请裁 11 条: 五席表态 (供 owner 审后一并裁, 不计入 finding)

| # | 请裁项 (执笔取舍) | 表态 |
|---|---|---|
| 1 | 10 条候选是否重开 post_planning | 已由本轮落实, 五席无意见 |
| 2 | `test -d`: 5.7 保留、5.5 删去 | 五席赞成 |
| 3 | track-id 断言接受 CRLF 正确值, 不守行尾 | 五席赞成 (tl 另建议同条的值非空检查一并去 CR) |
| 4 | 重新认领前先重解析 | 五席赞成 |
| 5 | elapsed_ms 语义与上下界由执笔钉定 | tl / ba / qa / cr 赞成, km 无意见 |
| 6 | phase-d SOT 有 diff 时重做映射, 根本冲突才停 | 五席赞成 |
| 7 | PR 标签可由主控在 owner 授权下打 | tl / cr 赞成但须先补标签前提 (`749f8d15`); ba 赞成; qa / km 无意见 |
| 8 | 守卫正则不放宽 | 五席赞成 |
| 9 | 计划不写字面目标版本号 | 五席赞成 |
| 10 | `main-project-version-consistency` 保留并写明作用 | 五席赞成 |
| 11 | SC-11 的 post_planning 子断言改称观察项 | 五席赞成 |

## Conflicted

1. **R3 `af5e1e47` 是否闭合**: tl 判 partially 并附源码证据; cr / qa / km 判 closed; ba 未深核。**事实层**: cr 本人在对账里写的是「`--include-terminal` 只影响 `linked_issue_overlaps` 与计数」—— 这恰恰支持 tl 的论点; qa 核的是三处 `_TERMINAL` 定义各自是否含 yielded, 没核该旗标作用于哪个函数; km 注明本轮未重读 `collision.py`。**主控裁断**: 采 tl, 依据是主控对 `collision.py:365-430` 与 `phase1_gate.py:1542-1552` 的实读; 未闭合部分计为本轮 minor `af5e1e47`。该分歧不影响本轮 Major 计数。
2. **执笔自报薄弱点第 7 条与第 5 条的可接受性**: 分别由 qa 与 tl 立为 minor, 其余席位判可接受。事实层无分歧 (停点确无编号 / 标签确未定义, 均经主控实测); 分歧只在「自陈过的缺口算不算 finding」。按 R7 的处理 (「事实断言不实另计为 finding」), 两条都计入, 定级均为 minor。

## 流程记录 (不计入 verdict)

1. **派单指纹五席全部吻合**: tl `4631e7fd6c98fbe2` / ba `e531cf50610efc9b` / qa `57c6c4ad8be31e26` / cr `e526fb126bc78071` / km `1aae0c9ddb0b2272`。派单由工具目录的席位模板生成 (固定节逐字保留, 只换背景事实、容器路径、本轮范围与四个必答节), 生成脚本与五份派单留在会话 scratch。
2. **报告写入方式与前七轮不同**: 五席的 Write 均被 harness 拒绝 (`aria:code-reviewer` 按定义本就没有 Write 工具), 席位按派单不绕过, 把报告全文作为最终回复; 主控从各席运行记录里原样取出落盘, 未作任何规整。格式差异如实保留: tl / cr 以 frontmatter 开头; ba / qa 的 frontmatter 在代码块内且前有一段说明; km 的 frontmatter 前有一段说明。
3. **finding id 按内容四元组重算**: 8 条全部与席位登记一致。
4. **计数防伪核对**: 五份报告 Findings 节内标注的严重度 (cr 1 major + 2 minor / tl 4 minor / qa 1 minor / ba 与 km 无) 与各席自报 counts 一致。
5. **主控独立核实的前提**: 8 条 finding 的前提逐条核实属实 (见 Major 与 Minor 表的「主控」字样处), 其中 `749f8d15` 为只读 API 实测、`af5e1e47` 为源码实读, 其余为计划原文实读。
6. **工作区冻结**: 真仓全程 HEAD `7ef09ea`、工作区干净、协调 ref `8013d3b` 未动; 各席报告称未写仓内任何文件。两份只读共享副本 (主仓全量副本与三态证据基准快照) 的跟踪内容全程零改动; 第一窗口 (tl + cr) 期间出现 `.git` 目录时间戳变化 (cr 自陈 09:35 的只读 `git status` 所致) 与一个被 gitignore 的缓存文件 `.aria/probes/__pycache__/main-project-version-consistency.cpython-311.pyc` (09:47:14; cr 否认, 归属未定, 时间窗指向 tl)。此后每派一席前重设时间标记, 并在后三席的调用提示里加一句「不要在共享副本里运行任何脚本」(派单文件本身未改, 指纹不变), 后两个窗口零改动。
7. **km 对执笔自报薄弱点的表态与执笔清单错位**: 其第 1、2 条 (「track-id 逐字断言只守文件内容、不守提交归属」「协调 ref 对齐通则只枚举两处例外」) 不在执笔的 10 条里; 执笔的第 1 条 (出稿前才补的 `6ad0a84b` 勘正) 与第 3 条 (未跑 unittest) 未获表态; 其余八条按内容可对上。不影响其 findings 与投票。
8. **轮次上限**: 本轮超出本周期 `max_rounds = 7`, 由 owner 2026-09-29 随「再开一轮」的裁定一并授权。
9. **各席耗时**: tl 约 36 分钟 / cr 约 38 分钟 / qa 约 23 分钟 / ba 约 17 分钟 / km 约 19 分钟。

## 收敛判断

**未收敛 (converged: false)** —— 口径与 R1 – R7 完全一致:
1. `conclusions_stable` = (R8 Major 键集 == R7 Major 键集) = ({`69707662`} == ∅) ⇒ **False**。
2. `unanimous_pass` = 4 PASS / 1 REVISE ⇒ **False**。
3. 振荡检测: 不适用 (没有回到更早的键集)。

**Major 题数轨迹**: 10 (R1) → 5 (R2) → 4 (R3) → 4 (R4) → 5 (R5) → 0 (R6) → 0 (R7) → **1 (R8)**。本轮的 Major 属「返修的新记录让既有缺口显形」一类 (见 Major 簇的性质说明), 修法是小改, 但改法在「按先例扩为六个文件」与「先定通用口径」之间需要 owner 选择。按 R7 聚合修正后的可执行收敛判据 (「无 Major 轮 + 下一轮无 Major 且全票 PASS」), 若修复后再审, 至少还需两轮干净轮才能判收敛。

## 执笔实例归属 (R1 定的判据)

判据: 某轮 Major 中若过半由上一轮返修自身引入 ⇒ 下一轮换执笔实例。本轮 1 条 Major, 接缝由 v2.7 的新记录产生, 底层五文件集早于 v2.7, 归属属边界情形。实际不受影响: v2.7 的执笔实例是一次性派发的, 下一次返修按惯例另派新实例并由主控独立核验 (执笔与核验分离)。

## 下一步 (待 owner 裁定)

1. **Major `69707662` 的修法**: (a) 按 `10CG/Aria#195` 先例把 aria 发版文件集写成六个; (b) 在 5.3 之前设 owner 裁定点, 等通用口径 (CLAUDE.md §版本管理写「aria 子模块 5 文件」, 实际近四次发版都是六个) 定了再改。
2. **七条 minor**: 与 Major 同批进 v2.8, 或部分延后。
3. **收敛路径**: v2.8 之后是否再审 —— 按收敛判据继续审 (至少两轮干净轮), 或由 owner 按 `audit-engine` 降级策略接受当前结论。
4. **执笔 11 条请裁** (owner 2026-09-29 定为审后一并裁): 五席表态见上表。
5. **入口门第 1 项已满足** (`03f97ac` 是 `7ef09ea` 的祖先); B.1 仍待以上裁定。

## 席位报告

同目录 `post_planning-R8-2026-09-29T093015-000Z-pre-merge-completeness-gate-change-scope-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md` (各席最终回复原样; sha256 前 16 位: tl `d3f46e77b7c128ed` / ba `2c045c62569d2f27` / qa `17071f76f62e3cf4` / cr `d3257c974d7b0b2b` / km `686e938c1774a48d`)。
