---
checkpoint: post_planning
mode: convergence
rounds: 11
converged: true
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS
timestamp: 2026-10-01T18:21:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
counts_raw: 0C/0M/10m
counts_dedup: 0C/0M/8m
sibling_probe: no_sibling_found
---

# post_planning R11 聚合 — pre-merge-completeness-gate-change-scope (10CG/Aria#199, A.2/A.3 v2.11 `09c5130`) — **CONVERGED**

> **被审对象**: `tasks.md` + `detailed-tasks.yaml` v2.11, 主仓 feature 分支 `feature/pre-merge-completeness-gate-change-scope` 的本地提交 `09c5130` (未推送; 计划规定组 1 – 4 期间 feature 分支不推)。
> **本轮由来**: R10 收敛后进入 Phase B。2.6 收口时, 目录全量回归被另一份已归档 spec 的既有结构约束 (`test_sibling_spec_probe.TestStructuralConstraints.test_scripts_helper_files_are_namespaced` 的 `scripts/` 允许集) 拦下。owner 2026-10-01 裁定 (决策单 `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md` 第 7 项): 停下回 Phase A 出 v2.11, 范围三项 (结构约束冲突的处置 / 决策单第 1 – 6 项并入读前必看 / 登记 Phase B 已发现的计划缺口); 之后开本轮 R11, 只审 v2.11 相对 v2.10 的改动 (`git diff fde9c1f 09c5130 -- <两份计划文件>`)。
> **执笔**: v2.11 由新派的执笔实例 (动态工作流里的 general-purpose 代理) 出稿, 主控独立核验一致性与可复跑性后提交; 修法对不对留给本轮判断。
> **Sibling probe (本轮入口, 派发前实跑)**: `status=ok` / `verdict=no_sibling_found`, github 157 份 / origin 162 份 proposal, 两端完整扫描无 cap。
> **drift-checker**: convergence 未 opt-in ⇒ 跳过。
> **并发**: 2 席滑动窗口 (tech-lead + backend-architect → qa-engineer → code-reviewer → knowledge-manager), 席位类型 `aria:<role>`, 派单以文件路径下发。

## drift_metrics (Step 0 anchor 快照)

- checkpoint: post_planning
- primary_goal: 把 Approved 的 10CG/Aria#199 proposal 分解为可执行的 Level 3 双层任务, 忠实落地决策单 2026-09-12 §2 的 10CG/Aria#199 表 13 行 (连同 §5) 与 Level 3 三处连带重写
- in_scope: 同前十轮 (本轮限 v2.11 的改动及其与未改动文字的接缝)
- out_of_scope_hints: proposal 设计取舍本身; 13 条裁定本身; 决策单 2026-09-30 第 1 – 7 项裁定本身
- source_sha: `09c5130`
- drift_ratio: null (未 opt-in)

## 判定

| 席 | verdict | counts | vote | 一句话 |
|---|---|---|---|---|
| tech-lead | PASS | 0C/0M/4m | PASS | 三项范围全 closed (自建 worktree 复现四跑与 eager 两种放法); 四条 minor: 结构约束条的 diff 边界 / 未跟踪补丁的 diff 记录 / 请裁 6、7 未进判断清单 / 第 73 条把 R11 列为授权来源 |
| backend-architect | PASS | 0C/0M/1m | PASS | 组 2 视角逐项对实际代码核对一致; 一条 minor: 读前必看第 32 条「四个非排除 checkpoint」实为三个 |
| qa-engineer | PASS | 0C/0M/1m | PASS | 五态结构约束反事实、Ran 算术、eager 差分全部独立复现; 一条 minor: TASK-013 工时未随交付物上调 |
| code-reviewer | PASS | 0C/0M/3m | PASS | 五处动作改动全部实测成立, 37 处引用抽查一致, 三态证据逐字节复跑; 三条 minor: 反事实缺正向对照 / 第 73 条授权来源 / 反事实实例要求与第 13 条不一 |
| knowledge-manager | PASS | 0C/0M/1m | PASS | 机械不变量与 133 / 129 推导独立复核; 一条 minor: 归档 spec 文档因本次改动过期却无追踪锚点 |

**五席全票 PASS, 五席无一立 Major 或 Critical** (Findings 节严重度标注与各席自报 counts 机械核对一致)。

## Major 簇

**无。** R9、R10、R11 连续三个零 Major 轮。

## Minor (raw 10 条 → 8 键)

| 定稿键 | 席位 | 内容与主控复核 |
|---|---|---|
| `6c7e3a62` | tl/m1 | TASK-013 既有结构约束条的机检「`git -C aria diff` 只落在 `TestStructuralConstraints` 类内」与条文约束对不上: 该类有两个用例 (另一个是 `test_no_lib_or_collectors_directories_under_audit_engine`), 误改它仍能过这条机检; 又不限文件, 而提交条要求「WIP 之后 `scripts/completeness_gate.py` 或 `tests/test_completeness_gate.py` 若另有改动, 一并 add」—— 若续跑前另有改动 (例如采纳请裁 8 补格), 两条指令互相冲突。修法 (席位): 拆成「`--name-only` 文件集包含于该测试文件 ∪ 台账已列的 WIP 后改动文件」与「该测试文件每个 hunk 只落在允许集一行、该用例 docstring 或类 docstring 内」两条。**主控实读** yaml:1847 / :1850 与 aria `88689aa` 的该类 (两个用例), 属实。 |
| `63a8700c` | tl/m2 | 反事实 (ii)(iii) 的补丁是未跟踪文件, 而所引 TASK-019 三步法要求「记副本 HEAD 与补丁 diff」; `git diff` 对未跟踪文件退出 0、输出为空 —— 正是 hard_constraints 第 14 条第 (3) 点要逐处写明的「退出 0 却没比成」形态。修法: (ii)(iii) 的补丁记录取 `git status --porcelain` 与 `git diff --no-index /dev/null <文件>` 的原样输出。**主控实读** yaml:1851 / :1961, 属实 (未跟踪文件不进 `git diff` 是 git 的既有行为)。 |
| `09d6a438` | cr/m1 | 反事实四跑没有「带 `sibling_spec_probe_` 前缀的辅助模块仍绿」这条正向对照: 实现若删掉前缀子句, 四跑全部符合期望, 发现不了; 漏网后果是将来按归档约束新增前缀 helper 时假红 (fail-closed 方向)。修法: 补一跑 (iv) 加空文件 `sibling_spec_probe_util.py` ⇒ 仍绿。**主控复现** (aria `88689aa` 经 `git archive` 取出两份, 不碰仓库): 正确改法 + 该文件 ⇒ OK; 删掉前缀子句的坏改法 + 该文件 ⇒ FAILED `['sibling_spec_probe_util.py']`; 坏改法不加该文件 ⇒ OK (与正确改法同态)。属实。 |
| `f89a8d20` | cr/m3 | 反事实条新写「补丁由既有结构约束条的执笔实例之外的实例或主控构造」, 比未改动的判断清单第 13 条 (「既非实现者也非测试作者的新实例」) 与 TASK-019 第 2 条 (「qa-engineer 的新实例, 未参与 TASK-004~006 与组 2」) 都宽, 且没注明是例外; 照字面可让组 2 的实现实例构造补丁。修法: 注明「本条是第 13 条的例外, 理由: 补丁不需要实现知识」, 或改为「既非组 2 实现者、也非该条执笔实例的实例, 或主控」。**主控实读** yaml:1851 / tasks.md:77 / yaml:1962, 属实。**键注**: 席位标题里的 scope 是缩写, 按其实际所用 scope「`detailed-tasks.yaml TASK-013 反事实条 / tasks.md 判断清单第 13 条`」复算吻合。 |
| `4a37c9ec` | tl/m4 + cr/m2 **跨席同键同内容** | 判断清单第 73 条写「授权来源是上述第 7 项裁定与本版经 post_planning R11」。R11 是 AI 审计, 不是 owner 明示; 决策单第 7 项只要求执笔「比较并推荐」, 没有预选 (a); 该条自己比照的 proposal `:429` 口径是「属改既有闸门, 须 owner 明示 (Rule #10)」。若 owner R11 后只说「续跑」而未对请裁 1 表态, 执行者会把 (a) 当作已获授权。Status 行已要求由 owner 裁定续跑, 实际后果有限。修法: 改为「第 7 项裁定 + R11 之后 owner 对请裁第 1 条的裁定 (记台账)」。**主控实读** tasks.md:137 与 proposal `:429`, 属实 (`:429` 原文针对改用 pytest 一事, 本条是比照引用)。 |
| `f49493cf` | tl/m3 | v2.11 有两项流程取舍 —— 请裁 6「WIP 保留、另起提交」与请裁 7「Ran 恰为 133 且不带 skipped」—— 没进判断清单, 第 77 条末句反而写「TASK-013 的 Ran 口径不属判断」; owner 对这两条的裁定无条目可挂, 5.9 照录判断清单进周期 handoff 时这两项 AI 取舍缺席 (Rule #10 §5 的留痕面)。修法: 补登或新增第 78 条写明取舍、备选与代价, 删去第 77 条末句里的「与 TASK-013 的 Ran 口径」。**主控实读** tasks.md:141, 属实。 |
| `f5aadec7` | ba/m1 | 读前必看第 32 条逐字照录决策单第 6 项的「四个非排除 checkpoint 全显式」; 裁定 1 之后非排除的 checkpoint 只有三个 (`post_spec` / `post_planning` / `post_implementation`), 第四个显式键 `post_brainstorm` 属第 5 项排除。该误数在 1.2 语料复算时曾真的致 `qa-corpus-C` 把排除集写成 4 项 (台账已记已改)。执行口径列不依赖这个数, 定 minor。修法: 决策单、tasks.md:48、`test_completeness_gate.py` 中 SC-15.10 夹具提交说明三处改为「四键 (其中 `post_brainstorm` 按裁定 1 属第 5 项排除)」。**主控实读** tasks.md:48、aria `88689aa` 的 `completeness_gate.py` (`_KNOWN_NON_EXCLUDED_CHECKPOINTS` 注释写「8 个已知 checkpoint 去掉五项排除 = 3 个」) 与 `test_completeness_gate.py` SC-15.10 夹具提交说明「four non-excluded explicit」, 属实。决策单第 6 项「事实」段的误数出自主控的核实文字。tl / km 也在风险节记了同一点, 执笔范围外观察第 4 条已自报。**键注**: 按席位实际所用 scope「`tasks.md 读前必看第32条`」(数字两侧无空格) 复算吻合。 |
| `857e5034` | qa/m1 + km/m1 **跨席同键, 两种内容** | (1) qa: TASK-013 的 `verification` 由 3 条扩为 5 条、`deliverables` 多一个文件, `estimated_hours` 仍为 `1-2` (yaml:1838); 不改执行动作。即执笔自报薄弱点第 5 条。(2) km: 本次把 `completeness_gate.py` 加进 sibling-spec-probe 允许集后, 归档 `openspec/archive/2026-09-04-sibling-spec-probe/detailed-tasks.yaml:221` 与 `tasks.md:26` 仍写两项允许集, 而 TASK-031 的七张 issue、判断清单与请裁都没有给这条漂移留追踪锚点。修法: TASK-031 登记一张 issue, 或台账补一句存证指针。tl / cr 在风险节的看法是「归档是冻结记录, 不构成 Rule #3 的同步义务, 来由靠 TASK-013 要求补写的 docstring (写 10CG/Aria#199) 交代」, 与 km 的修法不冲突。**主控实读** yaml:1838 与归档两处原文, 均属实。**键注**: 两席四元组完全相同 (`documentation` / `detailed-tasks.yaml TASK-013` / `minor` / `issue`), 内容是两件事; 按 R7 `6be9db6a` 先例同键并列记录, 不改口径。 |

## 三项范围对账

**五席对 v2.11 的三项范围逐项独立复核, 一致 closed**:

- **结构约束冲突的处置**: 五席核允许集改法 (三项逐字比较、前缀规则与 glob 不变)、discover 恰 133 (104 + 29) 与 129 / skipped=1 的拦截、提交条与反事实条。tl / qa / cr 各自在隔离副本复现四跑; km 用最小脚本实证 `setUpClass` 抛 `SkipTest` 时整类只计 1 次 skip、不计入 Ran (104 − 4 + 29 = 129); 判据缺口另计为 `6c7e3a62` / `63a8700c` / `09d6a438` / `f89a8d20`。
- **决策单第 1 – 6 项并入读前必看**: 五席逐字对照决策单原文; 「四个」误数另计为 `f5aadec7`; 第 73 条授权措辞另计为 `4a37c9ec`。
- **登记 Phase B 已发现的计划缺口**: 五席核登记条与链接注; 第 77 条与请裁 6、7 的口径另计为 `f49493cf`; 归档漂移的追踪锚点另计为 `857e5034` 第 (2) 项。

## 执笔「改变执行者动作的改动」5 处: 五席判断

| 改动 | 判断 |
|---|---|
| TASK-013 既有结构约束条 | 五席判改法正确 (tl 另立 `6c7e3a62` 判据边界) |
| TASK-013 discover 条 (恰 133、不带 skipped) | 五席判改法正确 |
| TASK-013 提交条 (WIP 之上另起提交) | tl / cr / km / qa 判改法正确 (cr 实测 WIP `88689aa` 只含两个文件, 按旧写法提交后 porcelain 会剩测试文件); ba 只做了三方文档互证, 自陈未做 git 级核验; qa 自陈未实跑提交后 porcelain 为空一句 |
| TASK-013 反事实条 | tl / ba / qa / km 判改法正确; cr 判预期值全部复现但有问题 (`09d6a438` / `f89a8d20`), tl 另立 `63a8700c` |
| TASK-020 第 (10) 条 eager 反事实 | tl / qa / cr 各自构造 eager 补丁复现「29 个用例只 SC-15.10 红, 首个失败断言是退出码 2 != 1」; ba 从代码结构核对; km 自陈超出视角未深核 |

接缝: 除上述 8 键外, 五席未发现 v2.11 改动与未改动文字之间的新不一致 (tl 与 cr 各自整族扫描了「TASK-0NN 第 N 条」类位置式引用, 被插入条目的 TASK 没有被指错)。

## 执笔自报薄弱点 (7 条): 五席表态

**第 1、3、4、6、7 条五席全部判可接受。** 第 2 条前半 (eager 补丁写法) 五席可接受, 后半 (「mode 写错」那一半没有格锁住) 五席确认属实, 转为请裁第 8 条。第 5 条 (TASK-013 工时未调): qa 判不完全可接受并立为 `857e5034` 第 (1) 项; km 判「不可接受但未达 finding 门槛」; tl / ba / cr 判可接受 (tl 建议下次改为 2-3, cr 估多出的两步约 0.5 – 1h)。

## 执笔请裁 8 条: 五席表态 (供 owner 裁定, 不计入 finding)

| # | 请裁项 (执笔取舍) | 表态 |
|---|---|---|
| 1 | 结构约束修法取 (a) 允许集逐字加入口脚本名, 不取 (b) 与其它 skill 的 `scripts/` 不重名 | 五席赞成执笔 (a)。cr 建议同时按 `09d6a438` 补正向对照。**按 `4a37c9ec`, 本条须 owner 明示, R11 不构成授权** |
| 2 | 新增读前必看第 33 条 (记代码落点差异) | 五席赞成执笔 |
| 3 | TASK-020 补第 (10) 条 eager 反事实 (由非测试作者复验) | 五席赞成执笔 |
| 4 | 决策单第 3 项拆成三行 | 五席赞成执笔 |
| 5 | 决策单第 4 项原文照录、改判写在依据列 | 五席赞成执笔 |
| 6 | WIP 提交 `88689aa` 保留、另起提交 | 五席赞成执笔。tl / cr 提示: WIP 提交正文「只在本地, 不推送」在 5.6 推送后不再成立, cr 建议在 2.6 提交正文注明 WIP 已被接续; `wip` 不在 git-commit.md §2 类型表, aria master 上已有 13 个先例, 两席均不判违规 |
| 7 | discover 的 Ran 要求「恰为 133、不带 skipped」 | 五席赞成执笔。tl / cr 提示: 若请裁 8 的补格写成新测试方法, Ran 变为 134, 本条与提交条须同步改; 写成 subTest 则不变 |
| 8 | lazy / eager 分歧里「mode 写错」那一半要不要另补一格 | **tl 赞成补格** (实测: 三个非排除键显式、`pre_merge` 不写、`mode: convergnce` ⇒ exit 1、`error_kind` 为 None, 没有任何格锁住; 若把 mode 校验挪到配置加载时, 这一半会静默翻转而全绿); **cr 倾向补格, 由 owner 定** (写成 subTest, 不改 Ran); ba / qa / km 无意见 (ba 倾向维持现状: 本轮授权不含改 `test_completeness_gate.py`; qa 建议若补则比照 SC-15.10 构造) |

## 单席风险 (不计入 finding, 供 owner 定是否跟进)

1. **上游已前进** (tl): aria 到 v1.74.1 (10CG/aria-plugin#182), 主仓到 `0748dbc`。该段上游对 `skills/audit-engine` 零改动; 对 `config-loader/SKILL.md` 只加两行注释, 不在 SC-21 读取的 audit 段; 5.1 / 5.3 的取号与并入按既有条款处理。主控核对本地远程跟踪 ref: 主仓 origin/master `0748dbc`、aria origin/master `268da8f` (均 2026-09-30 fetch)。
2. **state-scanner 回归的 skip 数也变了** (ba / qa / km; 执笔范围外观察第 3 条): A.2 基线 `Ran 1605 OK (skipped=1)`, 组 2 收口实测 `Ran 1627 OK`; TASK-021 既有「Ran 数变化逐条归因」已覆盖, 4.3 归因时须连 skip 数一起算。
3. **组 3 会改 `test_sibling_spec_probe.py` 读取的文档** (cr): 该文件 `TestSC17*` / `TestSC20*` 类读 `execution-modes.md` 与 `SKILL.md` 的内容, 组 3 会改这两份文件; v2.10 就有的风险, 由 TASK-021 兜住。
4. **反事实四跑可能被读成累积应用** (qa): 「依次为 绿 / 红 / 红 / 红」应读作各自相对 (a) 修复后的基线; 与全文既有反事实多子态的行文惯例一致, 预期不致误操作。
5. **SC-21 读取的常量名只做了文本核对** (qa): 若对不上, Phase B 跑 SC-21 时以 AssertionError 变红, 不会假绿。

## Conflicted

**无对称分歧。** `857e5034` 两种内容同键 (见上表); 请裁 8 两席倾向补格、三席无意见, 属取舍未定而非事实分歧; 归档漂移 (km 要锚点, tl / cr 认为归档冻结无同步义务) 两种看法可同时满足。

## 流程记录 (不计入 verdict)

1. **派单指纹五席全部吻合**: 派单以文件路径下发, 各席对文件实算 sha256 前 16 位写进报告 —— tl `10fc3fb0e30dc7cc` / ba `b70c4697dd03600d` / qa `fb29c8002b29c05a` / cr `b88919277e205647` / km `481efbb9b72b467b`, 与主控对派单文件的复算一致。
2. **qa 席重派一次**: 首个 qa 实例 17:17 – 17:31 运行后中断, 工作流自动重派新实例, 本轮 qa 报告出自重派实例。
3. **报告格式**: 五份均以 frontmatter 开头, 为各席最终回复原样, 主控从运行记录取出落盘, 未作规整。ba 的 frontmatter `timestamp` 写作 `19:40:00Z`, 晚于其实际返回时刻 (运行记录 17:17:25Z), 不采信, 以运行记录为准。
4. **finding id 按内容四元组重算**: raw 10 条全部可复算。其中 cr/m3 与 ba/m1 按 Findings 表里展示的 scope 不吻合, 按席位实际所用 scope 吻合 (见各键注)。跨席同键两处: `4a37c9ec` (同内容) 与 `857e5034` (两种内容)。raw 10 → 去重 8 键。
5. **计数防伪核对**: Findings 节严重度标注 tl 4 / ba 1 / qa 1 / cr 3 / km 1 条 minor, 与各席自报 counts 一致。
6. **主控独立核实的前提**: 8 键的前提逐条实读属实 (见表内「主控实读」); `09d6a438` 另经主控复现 (正确改法与坏改法在加前缀 helper 时分别为 OK 与 FAILED)。
7. **工作区冻结与纪律**: 真仓全程 HEAD `09c5130`、aria HEAD `88689aa`、协调 ref `c91fab6` 未动, 工作区始终为 ` M aria` 与未跟踪台账两项; 派发标记 (16:49:02Z) 之后两仓无任何 ref 更新 (reflog 与 `refs/aria` 下无新条目, 两仓 index 文件时间早于标记), aria 工作树无新于标记的文件; 两份共享副本从派发到最后一席返回**零改动**。主控按运行记录逐席扫描命令, 有四处越出派单纪律, 均只读、无残留:
   - qa (重派实例) 约 17:33 在真仓 aria 子模块的测试目录里跑了一次 `python3 -B -m unittest discover` (自陈; 派单禁止在真仓运行检查与 fetch), 输出含探针的 fetch 字样, 其来源未逐一追查; 无论来源, 两仓没有留下任何 ref 或文件变化。
   - ba 在共享副本里跑了只读 `git diff fde9c1f 09c5130` 和一段读 JSON 的 python (派单禁止在共享副本里运行脚本、检查或 git 命令)。
   - qa 首个实例在共享副本里跑了只读 `git log` 与 `git submodule status`。
   - km 在共享副本的 aria 里跑了只读 `git log --oneline -1`; 另在真仓跑了只读的 `git show` / `git diff` 与读文件的 python (真仓只读不在禁止之列)。
   - tl 与 cr 对共享副本只做了 `ls` / `du` 与 `cp -a`。
8. **各席耗时**: tl 约 45 分钟 / ba 约 26 分钟 / qa 约 14 分钟 (中断) + 21 分钟 (重派) / cr 约 33 分钟 / km 约 18 分钟。

## 收敛判断

**已收敛 (converged: true)** —— 口径与 R1 – R10 完全一致, 未作任何调整:
1. `conclusions_stable` = (R11 Major 键集 == R10 Major 键集) = (∅ == ∅) ⇒ **True**。
2. `unanimous_pass` = 5 PASS / 0 REVISE ⇒ **True**。
3. 振荡检测: 不适用。

**Major 题数轨迹**: 10 (R1) → 5 → 4 → 4 → 5 → 0 → 0 (R7 收敛) → 1 (R8) → 0 (R9) → 0 (R10 收敛) → **0 (R11, 收敛)**。本周期 `max_rounds` 经三次授权为 11, 本轮为第 11 轮。

## 执笔实例归属 (R1 定的判据)

本轮无 Major ⇒ 判据不适用。

## 下一步 (待 owner 裁定)

1. **post_planning 检查点再次收敛**, v2.11 的审计流程到此完成。按 Status 行, 续跑 Phase B (从 2.6 / TASK-013 起) 由 owner 裁定。
2. **请裁第 1 条须 owner 明示** (`4a37c9ec`): 修法 (a) 改的是另一份已归档 spec 的测试守卫, 授权来源只能是 owner。
3. **请裁第 2 – 7 条**: 五席一致赞成执笔取舍。
4. **请裁第 8 条**: 补不补「mode 写错」那一格 (补则写成 subTest, 由非实现者的测试实例在 2.6 提交前补, 4.2 加一个反事实)。
5. **本轮 8 键 minor**: 其中 4 键 (`6c7e3a62` / `63a8700c` / `09d6a438` / `f89a8d20`) 落在紧接着要执行的 TASK-013 上。按决策单 2026-09-27 第 3a 项, 只含 minor 的返修不重开 post_planning。
6. **决策单第 6 项「事实」段的「四个非排除 checkpoint」**: 是否以追加勘误的方式改正 (随 `f5aadec7`)。
7. **推送**: 组 1 – 4 期间 feature 分支不推; 本轮报告随主仓 feature 分支在 5.6 推送。

## 席位报告

同目录 `post_planning-R11-2026-10-01T165056-000Z-pre-merge-completeness-gate-change-scope-{tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md` (各席最终回复原样; sha256 前 16 位: tl `b39335a704413262` / ba `46126cef42f205bb` / qa `854e0c8240e62757` / cr `a07448edde3d5fa6` / km `12828b83d347af56`)。
