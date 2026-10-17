---
checkpoint: post_planning
mode: convergence
rounds: 11
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-01T18:10:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = 481efbb9b72b467b

- 被审两文件全文:`tasks.md`(283 行)、`detailed-tasks.yaml`(2246 行,仅精读 v2.11 变更命中的 hunk 上下文)
- `git diff fde9c1f 09c5130 --numstat`(tasks.md +18/-4、yaml +36/-26)与 `-U0`/`-U1` 全部 hunk(tasks.md 6 处、yaml 24 处),逐处取新旧行原文比对
- `proposal.md`:9-13、429(完整未截断行)
- 决策单 `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md` 全文(74 行)、`2026-09-12-two-l2-specs-...-rulings.md` 未逐字重读(本轮未改动此部分)
- 台账 `verification-ledger.md` 第 122-264 行一带(fixture 矩阵、附录 A)
- `v2.11-dispatch.md`(95 行)、`v2.11-writer-report.md`(183 行)全文
- 源码(只读,均取自 `p199-r11/base/Aria`,aria HEAD `88689aa`):`aria/skills/audit-engine/tests/test_sibling_spec_probe.py` 全文 2058 行(`TestStructuralConstraints`、`TestSC18LayerZeroFourArms`、`_cc1bdef_available`)、`test_completeness_gate.py`(grep 计数 + DEFAULT_AUDIT/LEGACY_CHECKPOINT_MAPPING 命中行)、`completeness_gate.py`(P3-P5 结构 grep)、`openspec/archive/2026-09-04-sibling-spec-probe/{tasks.md:26,detailed-tasks.yaml:221}`
- `standards/conventions/content-integrity.md` §4.4/§4.5 全文
- `aria/skills/state-scanner/scripts/lib/spec_complete.py` 330-369 行(checkbox 正则)
- 机械核验(本会话在 `/home/dev/Aria` 实跑只读 git/python 命令,在自建 `scratchpad/audit-R11-knowledge-manager/repro` 跑最小化 Python unittest 复现,未动真仓/共享副本):TASK 计数 31、owner_gates 19、stage_cells 39(按 TASK-008/009/010/011 分组相加 13+8+2+16)、读前必看数据行 33、全文禁用字形/希腊字母扫描(0 命中)、新增 diff 行裸 `#` 引用扫描(0 命中,含一处 `Rule #6` 白名单内误判已排除)、SC-22(2) WARN 文案两处逐字节比对(`repr()` 相同)

## Findings

| id | severity | type | category | scope | 摘要 |
|---|---|---|---|---|---|
| 857e5034 | minor | issue | documentation | detailed-tasks.yaml TASK-013 | 结构约束改法制造的归档 spec 文档漂移无任何追踪 |

**857e5034 — 结构约束改法制造的归档 spec 文档漂移,未开 issue/未留痕**

- 证据:TASK-013(v2.11)将 `test_scripts_helper_files_are_namespaced` 的允许集从 `{sibling_spec_probe.py, __init__.py}` 改为三项(加 `completeness_gate.py`)。但 `openspec/archive/2026-09-04-sibling-spec-probe/detailed-tasks.yaml:221` 原文仍是「`scripts/` 下除 `sibling_spec_probe.py` 与 `__init__.py` 外的每个 `.py` 文件名以 `sibling_spec_probe_` 起首」,`tasks.md:26` 同义复述。此事实已由执笔人在 `v2.11-writer-report.md`「风险最高的一处改动」与「范围外观察」第 2 条自报:「归档里的 `detailed-tasks.yaml:221` 和 `tasks.md:26` 仍写两项允许集,归档目录不在本轮范围内,没有同步」。我核对 TASK-031 的七张 issue 清单(`detailed-tasks.yaml` TASK-031 verification 第一条),逐条读完均与 10CG/aria-plugin 或 10CG/Aria 的 adaptive 推导/config 注册/AB 覆盖缺口相关,没有一条覆盖「归档 spec 文档因本次改动过期」这件事;判断清单 73-77 条与「请裁项」8 条里也都没有把它列为待裁或待登记项。
- 失败场景:v2.11 合入后,`openspec/archive/2026-09-04-sibling-spec-probe/` 的两份计划文件会继续宣称该用例只放行两个文件名,但实际测试代码已放行三个且已随 aria master 分发;未来任何人(含 AI agent)按 Rule #5「项目变更放本项目」去读该归档 spec 以理解「audit-engine/scripts/ 的命名约束现状」时,会依据过期文档得出错误结论,且因为没有 issue/记录锚点,这个漂移不会被任何现有机制重新发现或提醒修正。
- 该 finding 不影响本轮执行者在 v2.11/后续 Phase B 里会做错/做漏/卡住(改动范围、提交面、测试判据全部自洽、已验证正确),故封顶 minor。
- 建议修法:TASK-031 的七张 issue 之一(或新开第八张)登记「completeness_gate.py 加入 sibling-spec-probe 允许集后,归档 spec 的 tasks.md:26/detailed-tasks.yaml:221 描述过期」,或在台账「停下与上报」节补一句存证指针;二选一皆可,产出一个可追溯锚点即解决。

## 对账

**3A 结构约束冲突的处置 —— closed。** 两种修法(a 允许集加入口脚本名 / b 通用不重名规则)比较表六个维度均有数据支持,我逐项用源码独立复核:当前(88689aa)允许集确为二项(`test_sibling_spec_probe.py:430`);`completeness_gate.py` 确在 `scripts/` 下且不在允许集中,会判 offender(`:431-435`);(a)方案下 `git_utils.py`/`completeness_gate_helpers.py`/`lib.py` 三个反事实均应判红、`sibling_spec_probe_util.py` 应判绿——按允许集精确匹配 + 前缀规则逐一推演均与报告一致。TASK-013 由三条验证扩为五条、deliverables 加一个文件、31 个 TASK 编号不变,已用 `grep -c '^\s*- id: TASK-'` 核实恰为 31。proposal `:429` 的「改既有闸门须 owner 明示」原文经我完整取出核对,确实支持本次「归档 spec 测试宿主须经 owner 裁定才能改」的授权链引用。连带面(aria_zero_diff/TASK-027/TASK-031/TASK-007/TASK-021/rule6_note/scope_repos)逐处核对后与 yaml 实际改动一致。

**3B 决策单第 1–6 项并入读前必看第 25–32 条 —— closed。** 我将决策单 1-6 项原文与 tasks.md 新增第 25-32 行逐字对比(含 SC-22(2) 的 WARN 文案做了 `repr()` 字节级比对),全部逐字一致,无转述走样、无漏项、无顺序错位;第 3 项拆三行(27-29)分别对应 SC-4/SC-9(2)/SC-15(5),锚点可独立引用;第 4 项原文照录且在依据列正确注明已被第 7 项改判。相应 TASK(002/004/005/006/010/011/030)均补了锚点式链接注,未改动作。
> 3B 逐条核对(读前必看第 25-32 条 vs 决策单原文第 1-6 项):第 25 条(SC-2 F-b 降 0)、第 26 条(SC-7(b) 集合 C 加 aria-orchestrator)、第 27-29 条(SC-4/SC-9(2)/SC-15(5) 三处口径)、第 30 条(落档方式,含改判注记)、第 31 条(SC-22(2) WARN 全文)、第 32 条(resolved(pre_merge) 保持 lazy)——六项均逐字匹配决策单对应段落,无一处失真。

**3C Phase B 已发现计划缺口登记 —— closed。** 决策单第 7 项裁定文本列出的六类缺口(SC-15.10 新格/TASK-006 漏写 enabled_by/TASK-013 的 Ran 数口径/矩阵作为台账附录/测试里推导值的标注/测试经 importlib 读取的模块常量名)在 v2.11 中全部有落点:前三类分别落在判断清单第 76 条 + TASK-006、TASK-006 的 SC-15(5) 行(revision_log 直记)、TASK-013 discover 条(revision_log 直记);后三类落在判断清单第 77 条 (1)(2)(3)。`DEFAULT_AUDIT`/`LEGACY_CHECKPOINT_MAPPING` 两个常量名经 grep 确认确实出现在 `test_completeness_gate.py:2237-2302`。附录 A 的「第六版、90 格、六条矩阵勘误」经读取台账第 230/248/252 行确认均属实。唯一的缺口是上面 857e5034 号 finding(归档 spec 文档漂移未被登记),故本项判定为 closed 而非完全无保留——缺口本身轻微,不影响整体判 closed。

## 对「改变执行者动作的改动」的逐条判断

- **TASK-013 既有结构约束条**:改法正确。允许集改法、恰三项精确匹配、docstring 补写,均与源码实测吻合。
- **TASK-013 discover 条(Ran 恰 133)**:改法正确。我用 `grep -c '^\s*def test_'` 独立核实 `test_sibling_spec_probe.py`=104、`test_completeness_gate.py`=29,104+29=133;并用最小化 Python 脚本实证 `setUpClass` 抛 `SkipTest` 时整个类(无论含几个方法)只计 1 次 skip 且不计入 Ran——据此 104-4(`TestSC18LayerZeroFourArms` 恰 4 个方法)+29=129,与「cc1bdef 不可达时 Ran 129 skipped=1」的断言精确吻合,非臆测。
- **TASK-013 提交条(WIP 之上另起提交)**:改法正确。与硬约束「不静默改写历史」一致,WIP 88689aa 保留、新提交只 add 一个文件,逻辑自洽。
- **TASK-013 反事实条**:改法正确。(i)/(ii)/(iii) 三档红绿推演与允许集精确匹配逻辑吻合;「`git checkout -- .` 不删未跟踪文件」是真实 git 行为,无误。
- **TASK-020 第 (10) 条(eager 反事实)**:超出我视角未深核。我确认了 `completeness_gate.py` 当前实现 P4/P5 分离、pre_merge 的 resolved_mode 确在 P5 求值(`:610` 注释佐证),但未独立编写 eager 补丁重放该用例,对「29 个用例只此格红、首个失败断言是退出码 2!=1」这一具体运行时断言未做独立复验,留给实现/测试类审计席核实。
- **接缝检查**:除 857e5034 号 finding 外,未发现 v2.11 改动文字与 v2.10 未改文字之间产生新的矛盾——checkbox 正则(`spec_complete.py:336-337`)对改写后的 2.6 行仍正常解析;TASK-014 依赖字段指向 TASK-013(编号未变,依赖链天然正确);proposal `:11`/`:429` 两处引用均逐字核实为真。

## 对执笔人自报薄弱点的表态

1. 原文:(b)方案反事实补丁写得简单,写复杂些能抓到 `lib.py`,但不影响「抓不到 `git_utils.py`」的结论。可接受——(b)是落选方案,不影响最终决策质量,且已如实披露。
2. 原文:eager 补丁是自己构造的一种实现,SC-15.10 只锁住「Level 解析不出」半边,「mode 写错」半边无格锁定。可接受——限制已写入判断清单第 76 条正文并转交owner(请裁项第 8 条),未被掩盖。
3. 原文:Ran 129 是在独立克隆里测的,真仓组 2 收口那次跑得到的是 Ran 133。可接受——我已用 unittest 语义独立验证 129 这个数字的推导过程站得住脚,用于覆盖"少于 133 先查 skipped"分支合理且必要。
4. 原文:读前必看第 33 条超出派单明列范围,是自己的判断。可接受——该表功能本就是系统性记录"proposal 正文与执行口径的差异",第 33 条所述事实(proposal:11 确未列该测试文件)经我核实为真,属恰当延伸而非越权。
5. 原文:TASK-013 多了改测试和反事实两步,工时仍写 1-2 小时未调。不可接受但未达 finding 门槛——`estimated_hours` 非机械判据字段,不影响执行路径,建议顺手改掉,未单独开 finding。
6. 原文:revision_log 第 83 条「复跑相同」的断言只对终版三文件成立,主控再改要重跑。可接受——这是复跑类证据的通用时效性限定,非本轮特有缺陷。
7. 原文:Status 行末尾「待主控核验」提交后就过期,沿用前几版写法。可接受——纯状态提示文字,不输入任何机械判据,且本轮主控核验已实际发生。

## 对执笔请裁 8 条的表态

1. 原文:修法取 (a),备选 (b)。赞成执笔取舍——(a) 完整保留原约束意图、改动面最小、可证伪性最强,已独立核实。
2. 原文:新增读前必看第 33 条记代码落点差异,备选不加。赞成执笔取舍——省略会在该表功能完整性上留一个可核实的空洞,成本极低。
3. 原文:TASK-020 补第 (10) 条独立 eager 反事实,备选沿用测试作者本人那次实测。赞成执笔取舍——沿用测试作者自证会违反 hard_constraints 第 9 条「反事实须由非实现者非测试作者构造」的独立性要求。
4. 原文:决策单第 3 项拆成三行,备选合成一行。赞成执笔取舍——拆开后可精确锚点引用到单个子口径,符合判断清单第 47 条"序号引用改锚点式"的既定原则。
5. 原文:决策单第 4 项原文照录、改判写依据列,备选不收第 4 项。赞成执笔取舍——保留历史裁定原文 + 依据列注明改判,是对"执行口径逐字取裁定原文"原则的正确落实,且更利于可追溯性。
6. 原文:WIP 提交保留、另起提交,备选把改动压进 2.6 提交(WIP 未推送)。赞成执笔取舍——WIP 已是被本轮审计引用的既有历史事实,改写它与"不静默改写历史"原则冲突,另起提交成本更低风险更小。
7. 原文:Ran 判据取"恰 133、不带 skipped",备选"≥133 并逐条归因"。赞成执笔取舍——与本计划一贯的 fail-closed 风格一致,能在第一时间抓住 cc1bdef 不可达等环境异常。
8. 原文:lazy/eager 分歧中"mode 写错"那一半是否要另补格锁定,本轮未动。无意见——缺口真实存在(经核实决策单原文确实提到两种触发条件),但是否值得为未触发的理论分支新增测试覆盖属产品投入产出判断,留给 owner。

## 风险 / 疑问

- 决策单第 6 项「事实」段写「四个非排除 checkpoint」,但裁定 1 排除五项后非排除的应只剩三个(post_spec/post_planning/post_implementation)。读前必看第 32 条逐字照录了这个数字。这是决策单本身用词的潜在不准(执笔人在「范围外观察」第 4 条已自报),但按本轮 scope「13 条裁定本身对不对不在审查范围」,不计入 finding,仅在此存证供 owner 一并留意。
- `state-scanner` 回归数从 A.2 基线 1605 变为实测 1627(`skipped=1`→未知,writer report「范围外观察」第 3 条已标注待 4.3 一并归因);这不是 v2.11 本身要处理的事项,但提醒 R11 之后 Phase B 执行到 4.3 时需要同时核对 skip 数变化,不只是 Ran 数。

## Verdict

verdict: PASS;counts: 0C/0M/1m;**Vote: PASS**

## 是否足以开始 Phase B

足以——v2.11 对结构约束冲突的处置、决策单并入、Phase B 缺口登记三项范围均已忠实且自洽地落地,机械不变量(31 TASK/19 owner_gates/39 stage_cells/33 读前必看行)与关键数值判据(Ran 133/129 的推导)经独立复核全部准确,唯一的 minor 缺口(857e5034,归档 spec 文档漂移未留痕)不影响继续执行,可在 TASK-031 顺手补一张 issue 或在台账补一句存证即可,无需卡在本轮。