---
checkpoint: post_planning
mode: convergence
rounds: 11
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-01T19:40:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = b70c4697dd03600d

- `git diff fde9c1f 09c5130 -- tasks.md detailed-tasks.yaml` 全量输出(v2.10→v2.11 两个计划文件逐字 diff)
- `tasks.md` 全文(283 行,含读前必看 1–33 行、判断清单 1–77 条、外向动作表、SC 映射表)
- `detailed-tasks.yaml`:TASK-003(:1653)、TASK-004(:1671-1672)、TASK-005(:1690-1691)、TASK-006(:1709-1713)、TASK-008(:1749)、TASK-010(:1773-1792)、TASK-011(:1793-1811)、TASK-012(:1812-1831,确认未改)、TASK-013(:1833-1851 全块)、TASK-020(:1988)、TASK-021(:2011)、TASK-030(:2205)、`metadata.revision_log` v2.11 五条(:839-843)、`scope_repos.surface`(:33)、`rule6_note.note`(:244)
- `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md` 全文
- `verification-ledger.md`:173-247(「组 2 收口」「停下与上报」两节)
- `v2.11-dispatch.md`:30-69(第 3 节 3A/3B/3C 全文);`v2.11-writer-report.md` 全文
- `proposal.md`:103-127(§1.0 求值总序全表)、271-325(§1.4 路由与 16 键契约,含五格表与分割证)
- `completeness_gate.py`:70-169(`DEFAULT_AUDIT`/`LEGACY_CHECKPOINT_MAPPING`/参数契约)、595-624(`EXCLUDED_CHECKPOINTS`/`_KNOWN_NON_EXCLUDED_CHECKPOINTS` 注释)、1006-1033/1571-1590(`resolve_pre_merge_axes` 定义与调用点)
- `test_sibling_spec_probe.py`:412-436(`TestStructuralConstraints`)
- `test_completeness_gate.py`:1356-1565(`test_empty_checkpoint_set_three_buckets`,含 SC-15.10 格);`grep -c '^    def test_'` 两份测试文件各自计数(104、29)
- `config-loader/DEFAULTS.json`(`audit` 块)、`config-loader/SKILL.md`:305-344(§旧配置兼容层)
- `ls aria/skills/audit-engine/scripts/` 实况
- CLAUDE.md 多远程推送两条硬约束与不可协商规则 #3/#6/#8/#10:已随 system prompt 提供全文,未重复 Read

**自我纪律说明**:会话早期在共享副本内跑过一次 `git diff fde9c1f 09c5130 -- tasks.md detailed-tasks.yaml`(只读、未留缓存、未改内容)取 v2.10→v2.11 diff;之后已停止在共享副本内运行任何 git 命令,改用 Read/grep/wc/python3 读当前工作树(工作树本就是 `09c5130`/`88689aa`,查现状不需要 git)。按派单纪律本不应在共享副本内跑 git 命令(即使只读),如实记录。

## Findings

| id | severity | type | category | scope | summary |
|---|---|---|---|---|---|
| f5aadec7 | minor | issue | documentation | tasks.md 读前必看第 32 条 | 「四个非排除 checkpoint」计数有误(裁定 1 之后实为三个),已反复出现且曾致一次真实计算出错 |

**f5aadec7** 证据:`tasks.md:48` 与决策单第 6 项「事实」都写「四个非排除 checkpoint 全显式」;而 `completeness_gate.py:605-619` 的注释与代码自证非排除 checkpoint 恰为 3 个(`_KNOWN_NON_EXCLUDED_CHECKPOINTS` = 8 个已知 checkpoint 减 5 项排除);`test_completeness_gate.py:1553` 的 commit message 同样写「four non-excluded explicit」并把裁定 1 新增的第 5 项排除 `post_brainstorm` 算了进去。`verification-ledger.md:239` 记录 `qa-corpus-C` 在 1.2 语料复算时真把 Step 3 排除集写成 4 项(漏 `post_brainstorm`),已被主控发现并记台账改正。
失败场景:后续执行者若照字面「四个非排除」枚举该集合而不回查 `EXCLUDED_CHECKPOINTS` 定义,会重复 `qa-corpus-C` 已出现过的计数错误;这次因恰好不改变最终结论而未外显,不保证下次同样无害。
不升级为 major 的理由:该短语只出现在「依据/事实」说明文字里,v2.11 真正驱动执行者动作的「执行口径」(保持 lazy、`resolved(pre_merge)` 只在 P5 求值,`tasks.md:48` 执行口径列本身)不依赖这个计数;且是逐字照录决策单原文(判断清单第 75 条明示「执行口径列逐字取裁定原文」),非 v2.11 新造。写者已在「范围外观察」第 4 条自报同一问题(只引了决策单,未引 `verification-ledger.md:239` 这一复发证据)。
建议(留给下次触碰该行的版本):决策单、`tasks.md:48`、`test_completeness_gate.py:1553` 三处改为「四键(其中 `post_brainstorm` 按裁定 1 属第 5 项排除)」,纯文本改动,不改断言。

## 对账

**3A 结构约束冲突的处置 —— closed**。dispatch 要求的 4 点逐一核验:(1) 比较并推荐——对照 `test_sibling_spec_probe.py:422-435`(当前允许集 `{sibling_spec_probe.py, __init__.py}` + 前缀)实测 (a)/(b) 两种候选改法的实际效果,(a) 保留原判据形状且改动面最小,推荐 (a) 成立。(2) 落到计划——`detailed-tasks.yaml:1833-1851`(TASK-013)未新增编号,标题/交付物/verification 均按要求扩写。(3) 连带面逐处核——`:840` 点了 `aria_zero_diff`/TASK-027/TASK-031/TASK-007/TASK-021/`rule6_note`/`scope_repos`,核对 `rule6_note.note`(:244)与 `scope_repos.surface`(:33)确已同步追加。(4) 反事实——`TASK-013:1851` 的 (i)(ii)(iii) 与我用当前 glob/集合逻辑独立推演的结果(退两项→红;加 `git_utils.py`→红;加 `completeness_gate_helpers.py`→红,因逐字比较非前缀)完全一致。

**3B 决策单第 1–6 项并入读前必看 —— closed**。逐条把 `tasks.md:41-48`(第 25–32 行执行口径列)与决策单第 1–6 节「裁定」原文并排比对,8 行执行口径全部逐字相同;第 3 项拆行(27–29 行)符合 dispatch 授权的「可拆三行或合一行,自定并说明」;第 30 行保留决策单原文、把「已被第 7 项改判」放进依据列而非篡改执行口径本身,处理得当;第 7 项本身只落在 `revision_log:839` 与 Status 行(`tasks.md:6`),未混入读前必看表。锚点链接注核对 TASK-002/004/005/006/010/011/030 均已补。

**3C Phase B 缺口登记 —— closed**。dispatch §3C 的 7 个子项逐一核验:(1) SC-15.10 登记到 TASK-006(:1710)与 SC 映射表,`stage_cells` 确认未变 39 格;TASK-020 补第 (10) 条(:1988),用测试代码核实「首个失败断言是退出码」为真。(2) `enabled_by` 断言补回 TASK-006(:1709),与 proposal:471 原文及决策单第 3 项第 3 条一致。(3) Ran-133 口径经 `grep -c` 独立计数确认(104、29)。(4) TASK-003 矩阵附录登记(:1653)。(5) 判断清单第 77 条登记推导值例外。(6) `DEFAULT_AUDIT`/`LEGACY_CHECKPOINT_MAPPING` 登记进 TASK-006/008(:1712,:1749),经读 `completeness_gate.py:76-96` 确认两常量名与取值与 `config-loader/DEFAULTS.json`、`SKILL.md:316-327` 的旧配置映射逐字相符。(7) 决策单两次提交 foreign 预期登记进 TASK-030(:2205)与读前必看第 30 行。

## 对「改变执行者动作的改动」的逐条判断

1. **TASK-013 既有结构约束条**:改法正确。新允许集 `{sibling_spec_probe.py, completeness_gate.py, __init__.py}` 对照 `ls scripts/` 实况(`completeness_gate.py`/`__init__.py`/`sibling_spec_probe.py`)恰好消除当前唯一 offender,前缀规则与用例数未变,机械自洽。
2. **TASK-013 discover 条**(Ran 恰 133、不带 skipped):改法正确。`104+29=133` 已用 `grep -c` 独立核实;`cc1bdef` 不可达导致整类跳过、Ran 129 的边界情形未被误判为通过,方向 fail-closed。
3. **TASK-013 提交条**(WIP `88689aa` 之上另起提交,只 add 该测试文件):逻辑自洽,但**超出我本轮独立核验能力**——按纪律未在任何仓内对 `88689aa` 树内容与 `git status --porcelain` 做独立 git 级核验,只核对了决策单/台账/dispatch 三方记述互相一致,未发现矛盾。
4. **TASK-013 反事实条**:改法正确。(i)(ii)(iii) 预期红/绿与我用当前测试代码的集合逻辑手工推演结果完全吻合;「未跟踪文件须显式删除,`git checkout -- .` 不删」与 git 行为常识一致。
5. **TASK-020 第 (10) 条**(eager 反事实补丁):改法正确。`test_completeness_gate.py:1556` 的 `assertEqual(proc.returncode, 1, ...)` 确是该 subTest 内第一条断言,eager 实现下返回码应为 2 而非 1,「首个失败断言是退出码」可直接从代码结构验证。

## 对执笔人自报薄弱点的表态

1. 反事实补丁是自造候选,(b) 写复杂些能多抓 `lib.py` 但抓不到 `git_utils.py`——可接受:不影响「取 (a)」结论,`git_utils.py` 是该用例 docstring 自举的红例,(b) 抓不到即是决定性证据。
2. eager 补丁自造,SC-15.10 只锁「Level 解析不出」半边,「mode 写错」半边未锁——可接受:代价已在决策单第 6 项写明为已知权衡,补另一半需改 `test_completeness_gate.py`,超出本轮三项授权范围。
3. Ran 129 是独立克隆测的,真仓组 2 收口是 Ran 133——可接受:只是对主数字 133 的边界情形说明,不影响主张。
4. 读前必看第 33 条超出派单明列范围、属自我判断——可接受:恰是读前必看表自身定义(「proposal 正文与执行口径的差异」)该收的那类差异,非无依据扩权。
5. TASK-013 多两步但工时仍写 1-2、未调——可接受(纯估时滞后,不影响正确性)。
6. revision_log 第 83 条「复跑相同」以终版三文件为准,再改字要重跑——可接受,是对自检范围的如实限定。
7. Status 行「待主控核验」提交后过期、沿用旧写法——可接受,v2.1 起历版一贯写法,非本轮新增问题。

## 对执笔请裁 8 条的表态

1. 修法取 (a),备选 (b)——赞成执笔取舍:(b) 连自己 docstring 举的红例 `git_utils.py` 都测不出来,(a) 更保真、改动面更小。
2. 新增读前必看第 33 条,备选不加——赞成执笔取舍:成本是一行表格,不加则「proposal:11 未列该文件」这一差异无处可查。
3. TASK-020 补独立第 (10) 条,备选沿用测试作者本人实测——赞成执笔取舍:判断清单第 13 条要求反事实作者与实现者、测试作者都不同,沿用作者自己的实测不满足该约束。
4. 第 3 项拆三行,备选合一行——赞成执笔取舍:拆开后各 TASK 的链接注能指到单条,避免「同一引用随版本腐坏」(判断清单第 47 条已吃过这个亏)。
5. 第 4 项原文照录 + 改判写依据列,备选不收——赞成执笔取舍:保留可追溯历史优于静默省略一条已被部分改判的裁定。
6. WIP 保留另起提交,备选压进 2.6 一个提交——赞成执笔取舍:WIP `88689aa` 已记入台账(:196)成为既成事实,压缩会改写已记录的 SHA。
7. Ran 要求「恰 133、不带 skipped」,备选「≥133 并逐条归因」——赞成执笔取舍:恰等于比「≥」更 fail-closed,与本计划一贯偏好精确相等而非模糊阈值同一哲学(如第 27 条 SC-4 恰 22)。
8. lazy/eager「mode 写错」半边要不要补格——无意见,倾向维持现状留给 owner:本轮三项授权范围不含修改 `test_completeness_gate.py`,现在补等于自我扩权。

## 风险 / 疑问

1. 「四个非排除 checkpoint」的计数误差(详见 Findings f5aadec7)已证明会在无人察觉时产生真实(这次无害)的计算错误,建议 owner 下次触碰相关文字时一并勘正决策单、`tasks.md:48`、测试 commit message 三处。
2. `verification-ledger.md:181`(写者「范围外观察」第 3 条)记录 state-scanner 回归从 A.2 基线 `Ran 1605 OK(skipped=1)` 变为 `Ran 1627 OK`,skip 数也变了;v2.11 未改 TASK-021 相应文字,但其原有「Ran 数变化逐条归因」是通用要求,本覆盖三条命令,4.3 执行时须把这条也归因清楚,不止归因 audit-engine 的 133。
3. TASK-013「提交条」的 WIP 既成事实(`88689aa` 树内容、porcelain 结果)本席未做独立 git 级核验(见 3b 第 3 条与自我纪律说明),只做了三方文档互证;如三方共享同一盲点,核验覆盖不到。

## Verdict

PASS — 0C/0M/1m — **Vote: PASS**

## 是否足以开始 Phase B

足以。v2.11 范围内(结构约束处置、决策单并入、缺口登记)在我的视角(组 2 实现对 proposal 的忠实度)下均与实际代码、实际测试文件、config-loader 真实文件逐一核对一致;`resolved(pre_merge)` 的 lazy/eager 取舍有 proposal §1.4 格 C 与分割证第 (3) 条正文支撑;TASK-013 的结构约束修法经我用当前 `test_sibling_spec_probe.py` 代码独立推演验证可信。唯一记录的发现是不影响执行动作的文档措辞问题。