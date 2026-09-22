---
checkpoint: post_planning
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-22T15:35:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

> `drift_check_skipped` 填 `true`: 本轮独立复核 `.aria/config.json` 的 `audit` 块 (`python3 -c "import json; d=json.load(open('.aria/config.json')); print(sorted(d['audit'].keys()))"` → `['_comment', 'checkpoints', 'enabled', 'max_rounds', 'mode', 'teams']`), 无 `drift_guard` 键, 与 R1–R5 结论一致 (R5 聚合「流程记录」#1 已记录模板与实值的分裂, 本行按实值填, 不按模板)。

## 已实读文件

派单 sha256[:16] = 90bab48da83a01d7

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` (v2.5 全文, `git show e7a1782:...`, 240 行, 含读前必看 1–23 条、AI 流程判断清单 1–45 条、SC↔任务映射表、等待点表、范围边界表)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` (v2.5 全文, `git show e7a1782:...`, 1982 行)
- `git diff b686185 e7a1782 -- openspec/changes/pre-merge-completeness-gate-change-scope/ .aria/notes/2026-09-17-199-a2-a3-tooling/gen_yaml.py` 全 hunk (tasks.md 122 行、yaml 578 行 diff, 逐段读完, 未抽样)
- `.aria/audit-reports/post_planning-R5-2026-09-22T034038-000Z-pre-merge-completeness-gate-change-scope-aggregated.md` (全文)
- `.aria/audit-reports/post_planning-R5-2026-09-22T034038-000Z-pre-merge-completeness-gate-change-scope-qa-engineer.md` (我自己 R5 报告全文, 核对本轮有无新证据重提)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: SC-8~SC-14 表格全文 (`:463-469`)、§1.2 B.0 语料冻结 `:409-428` 全文
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` (全文 116 行)
- `aria/skills/phase-c-integrator/scripts/submodule_gate.sh` (全文 335 行, 逐段读: 头注释 exit code 表 `:1-30`、pre-flight `:55-68`、fetch/refspec `:185-217`、per-submodule 循环与 mode dispatch `:218-334`)
- `aria/skills/audit-engine/tests/test_sibling_spec_probe.py:290-340`(`TestNoPytestImport` / `TestRunAllTestsDiscovery` 全文)
- `aria/skills/run_all_tests.sh:1-72`(`is_pytest_suite()` 全文与调用处)
- `aria/skills/state-scanner/SKILL.md:178-193`(Layer L A.1 heartbeat 集成: 触发条件 `:182`、fail-soft `:191`)
- `aria/skills/state-scanner/lib/constants.py`(`grep SWEEP_TTL` 定位 `:58`, 与 `gc.py`/测试文件交叉核实)
- CLAUDE.md「多远程推送 — 两条硬约束」与不可协商规则 #3/#6/#8/#10 (系统提示已含全文, 本轮逐条核对 C.2.4.5 与 owner_gates 改动是否符合)
- **实跑核验**(全部在 `/tmp/claude-1000/-home-dev-Aria/82379761-f707-4902-a23a-45070cee8ae7/scratchpad/audit-R6-qa-engineer/` 下, 真仓内零写入; 官方 `state-base` 副本 `cp -a` 到自己目录后使用):
  1. 用官方 README 配方重新生成 yaml: 从已提交 yaml 抽出 `a2_state_runs`/`v2_state_runs` 的 script+output 落盘, 补 5 个 CLI 参数跑生成器 —— `cmp` 逐字节 **REGEN_IDENTICAL**(独立复现, 未采信主控自报)
  2. 把 `state-base`(主仓 `a563192` + aria `1cb3872` 嵌套 clone)`cp -a` 到自己目录, 用真实 `tasks.md`/`detailed-tasks.yaml` 重跑 `a2_state_runs.py`(重写 a 的 A/B/C/D/D2/E/F 七态 + N1/N2/N3) —— 与 yaml 内嵌 `output` **逐字节 IDENTICAL**
  3. 同一份 `state-base` 副本重跑 `a2_v2_checks.py`(N4/C1/N6/N7/N8/N9/N10/**N11**, 含 v2.5 新增/重写的三态) —— 与 yaml 内嵌 `output` **逐字节 IDENTICAL**, 含 N9 新态(基准 ref 不存在 ⇒ exit 2)、N10 重写(钉主仓根 + rc 判据 + 「TASK-021 order」子态)、N11 全部 12 行(会话入口强制对齐、claim 被 sweep 后的 resolve/precheck/heartbeat/release 六态)
  4. `submodule_gate.sh` 源码核对: `MODE="${ARIA_SUBMODULE_GATE_MODE:-block}"`(缺省 block, 与头注释「缺省 warn」不符, 代码为准)、exit code 0/1/2/3/4/64/65 逐一在源码定位、`OK:`/`GATE:`/`PASS:`/`BLOCK:` 输出前缀逐一定位
  5. `! grep -rn '<vNEXT>' aria/ ...` (`.aria/state-checks.yaml:38`) 语义核对: 路径不存在时 grep exit 2 经 `!` 反转为 0、无输出, 与「通过」同形, 核实 TASK-027/029 新加的 `test -d aria/skills` 前置断言的必要性
  6. 对当前 (v2.5) yaml 全文做「为空/无输出/零命中/零输出」与 `porcelain`/`ls-remote`/`wc -l`/`comm -23` 的独立 python 正则扫描 (方法与执笔人自述的「词形扫描」不同, 作交叉验证), 唯二两处命中经上下文核实均为历史注释/事实陈述, 非现行判据缺口
  7. 用 python 脚本按 parent 编号建立 TASK 分块, 对 SC-1~SC-22 + N1/N2/N4/N7/N8/N3/N10 在 tasks.md 映射表列出的每个 (SC, 承载任务) 组合逐条查 yaml 对应 TASK 是否覆盖 (逐条核, 非抽查); 对 TASK-012 等「blanket 全绿」式覆盖与 TASK-004/005/006 的「用例名列表」式覆盖分别核实其达到等价的可核验性

## R5 对账

| 项 | 判定 | 我亲验的证据 |
|---|---|---|
| R5-M1 (`9c294cca`, 等待点 13「同批」时序冲突) | **closed** | yaml `owner_gates` 现列独立的 13a(D.2b, release 之前, 逐项授权)与 13b(latest.md 单独提交产生之后, 附其 diff); tasks.md 等待点表同步拆两行; TASK-031 的 claim 条明确「release 之前单独请 owner_gates 第 13a 项」, latest.md 提交条明确「该提交产生之后请等待点 13b」。我对现文全文做了 `第 ?13 ?项[^ab]` / `等待点 ?13[^ab]` 的正则扫描: yaml 命中 6 处、tasks.md 命中 6 处, 逐条读原文确认全部带「原」字限定词或落在 `revision_log` 的 v2.4 历史条目内(如实保留历史记录, 与 revision_log 自述的收尾断言一致), 无一处是当前有效判据里的裸引用 |
| R5-M2 (`3e6a8483`, claim 存活只在 TASK-001 核一次) | **closed** | `hard_constraints` 新增第 4 条: Phase B–D 每个会话入口做「三元组解析 → 协调 ref 前置检查 → 强制对齐后重跑解析 → 心跳并核验」, 0 条 active 或 `claim_not_found` ⇒ 第 14 项(挂载扩到任意会话), 例外覆盖 TASK-024 AB 会话与 TASK-031 release 之后。我独立重跑 N11(见上「实跑核验」3), 12 行输出与嵌入值逐字节相同, 直接复现了 R5-M2 要修的场景: 「stale local, v2.4 order (no alignment)」心跳 `push_success=False`(旧序失败), 「v2.5 order」经强制对齐后 `push_success=True` 且 `remote_equals_local=True`; claim 被 sweep 后旧序 `resolve` 仍读到 `active`(看不见 sweep), 新序对齐后正确读到 `abandoned`(`active=0`)。另核实 `aria/skills/state-scanner/SKILL.md:182`(触发条件「本会话持 active claim」)与 `:191`(fail-soft, 只记遥测)、`lib/constants.py:58`(`SWEEP_TTL: int = 86400 # seconds (24h)`)三处源码事实与 yaml 论证逐字相符 |
| R5-M3 (`3782becc`, C.2.4.5 已启用闸被计划静默略过) | **closed** | TASK-030 新增 C.2.4.5 条: 本仓未配置 → 缺省 `block`, 由主控在 C.2.4 green 之后、Forgejo 合并之前在主仓根显式跑 `submodule_gate.sh`; owner_gates 新增第 17 项(block/未跑成/缺结论行 ⇒ 不合并, override 只由 owner)。我直接读脚本源码 335 行核对: `MODE="${ARIA_SUBMODULE_GATE_MODE:-block}"`(:33, 缺省 block, 与头注释「读配置缺省 warn」不符——yaml 原文已点破这一不符并声明「以代码为准」, 核实为真); exit code 0/1/2/3/4/64/65 逐一在源码找到落点(`:63-64` 65、`:201` 2、`:214` 3、`:281`/`:287` 4、`:312`+汇总段 1、`:226` 0); `OK:`/`GATE:`/`PASS:`/`BLOCK:` 前缀分别在 `:259`/`:263`/`:267`/`:308` 逐一核实, 与 yaml 「放行需逐子模块结论行齐」的判据描述一致 |
| R5-M4 (`c287d217`, TASK-027(b) 与 R4-M1 同构假绿; 系我 R5 自己提出的 finding) | **closed** | TASK-027 第 4 步 (b) 现改为: 先对 `A`、`S3` 各跑 `cat-file -e`, 非 0 ⇒ 停; `diff --stat` 非 0 ⇒ 「没比成」停(不再放行); 0 且有输出 ⇒ 停并按第 4 项重跑; 0 且空 ⇒ 过。新增 (c) feature 一侧(即同处 minor `1453c41f`, 见下)。`sc12_liveness.guard_config_hooks` 重写为钉 `git -C <主仓根>`、判据看 `rc=` 行(0/1 且其前无输出才算过)。我独立重跑 N10(见「实跑核验」3), 新增的「从 `aria/skills/audit-engine/tests` 跑(TASK-021 order)」子态在 v2.5 命令下 `rc=0 hits=1 verdict=stop`(正确挡住), 旁注 v2.4 旧命令在同一态下 `output_lines=0`(旧读法会放行)——两者对照证实修法确实堵住了我 R5 报告点名的失效模式; TASK-021 第 2 条(三条 unittest)现补「三条各放子 shell...跑完当前目录仍是主仓根」, 与第 3 条(guard 钉主仓根)顺序上自洽 |
| 同处 minor `1453c41f`(TASK-027(b) 未比 feature 一侧) | **closed** | TASK-027 新增第 4 步 (c): 对 `W`/feature 现值/TASK-024 结果提交各 `cat-file -e`, 再比 aria 两个 skill 目录(`W..feature`)与主仓 `ab-suite/audit-engine.json`(结果提交 vs **工作树**, 非 HEAD——文本明确解释「主仓侧没有先提交 TASK-026 改动的一步, 比到 HEAD 会漏掉未提交的改动」), 非空则逐 hunk 按 Rule #6 判据表分类。owner_gates 第 6 项同步补触发条件。此设计正确预判了 TASK-026 首次自检的修复会以未提交状态留在工作树这一事实, 我核对 TASK-026 verification 全文确认它确实不含 commit 动作 |
| 同处 minor `118d1d64`(TASK-031 deliverables 漏列 latest.md) | **closed** | TASK-031 的 `deliverables` 现含 `docs/handoff/latest.md`(与 v2.4 对 TASK-029「只列本任务提交的文件」同口径), diff 中该行为新增行, 我在 `git show e7a1782:...` 的当前文本里核实该路径确在列表内 |
| 同族扫描声称覆盖项 `ac2e8dcb`(owner-container 粘贴无失败回退) | **closed** | TASK-031 周期 handoff 起稿条现补: 「该命令失败时打印空串并退出 1...粘贴前先看退出码: 退出非 0 或输出为空 ⇒ 按 handoff-mechanics.md 同段的回退, 照模板派生规则手填」; E1 自校验条新增一条值非空检查(`grep -cE '^(...): *[^ ]'` 须 `==5`, 区别于原 E1 只验字段在不在)。两处改动逐字读到, 且新旧两条断言(存在性 E1 + 非空 E1')分工清楚、不冲突 |
| 同族扫描声称覆盖项 `11c3a29f`(`aria_shifted` 第 6 条三文件名连写误判零 diff) | **closed** | metadata 中该条目现拆为三条独立文件(`plugin.json`/`marketplace.json`/`README.md`), 且 TASK-001 基线复核条新增「每个文件另先确认它至少在两个端点之一存在: `git cat-file -e <端点>:<文件>`...两端都退出非 0 ⇒ 路径写错或不是单个路径, 停下上报」, 直接对应该 finding 描述的失效模式(两端都不存在的路径 `diff` 同样退出 0 输出为空) |

**结论**: R5 五个 Major 簇、两条同处 minor、同族扫描点名的两个具体候选, **全部 closed**, 且本轮对其中三处(R5-M2/M4 涉及的 N10/N11、R5-M3 的脚本源码)做了独立于执笔自述与主控自报的第一手复核(实跑复现 + 源码逐行核对), 未发现自报证据与实况不符之处。

## Findings

本轮我的视角(验收设计与可证伪性: SC↔任务映射、RED 批次可证伪性、反事实设计、三处重写与 N1–N3、B.0 语料冻结、SC-12 环境排序)**未发现新的 critical 或 major**。具体核验过程与依据见下方「已实读文件」实跑记录与「风险/疑问」。以下按视角逐项记录结论(均非 finding, 供交叉核对):

1. **SC-1~SC-22 + N1/N2/N4/N7/N8/N3/N10 映射一致性**: 用脚本对 tasks.md 映射表列出的每个 (SC, 任务) 组合逐条核对 yaml 对应 TASK 是否覆盖(29 个 SC 行 × 各自 1–4 个任务列 = 逐条核, 非抽查)。发现的"未直接命中 SC 编号字面"的情形(如 TASK-012 用「SC 方法级全绿」blanket 断言覆盖 SC-1~SC-22 的转绿列、TASK-004/005/006 用测试用例名列表而非逐条点 SC 号覆盖 RED 列)逐一读原文确认属等价的、可核验的覆盖方式,非缺口。此表未被 v2.5 触碰(diff 确认零变更),与 R1–R5 历轮结论一致。
2. **RED 批次可证伪性 + 测试风格约束**: 直接重读 `test_sibling_spec_probe.py:290-340` 的 `TestNoPytestImport`/`TestRunAllTestsDiscovery` 两条守卫与 `run_all_tests.sh:33-36` 的 `is_pytest_suite()`,与 tasks.md「测试一律 `unittest.TestCase`, 不 import pytest、不建 conftest.py」的约束逐字相符,未被 v2.5 触碰。
3. **反事实设计(4.1/4.2, TASK-019/020)**: 未被 v2.5 触碰(diff 确认零变更),R1–R5 历轮(含我自己 R4/R5 的 `git worktree remove` 脏工作树实测)已核实三步法可执行,本轮未发现新证据推翻。
4. **三处重写与 N1–N3(含 v2.5 新的 N9/N10/N11)**: 见上方「实跑核验」2/3——独立重跑 a2_state_runs.py 与 a2_v2_checks.py 均逐字节吻合嵌入值。重写 a 的 L1/L2/L3 区分力核对: 六个坏态(D/D2/E/F 加 baseline-as-written/baseline-checked)分别被 L1(D/D2)或 L2(E, 因 `generic_path_call` 类别不等于要求的 `aria_plugin_integration`)或 L3(F, 脚本失去自身 token)之一拦住,TASK-021/031 要求 L1+L2+L3 全真的组合判据下无遗漏组合。重写 c 的区分力(hermetic 快照的 missing/not_applicable 两态)未被 v2.5 触碰。
5. **B.0 语料冻结(1.2/TASK-002)**: 未被 v2.5 触碰(diff 确认零变更)。重读 TASK-002 verification 确认三步算法(来源定序/归一化/判定)逐字对应 proposal `:416-419`,标注者/实现者分离写为可执行断言(「由未参与标注的另一实例...同一实例复算不算」)。
6. **SC-12 回归命令环境排序**: 读前必看第 12 条(非判断清单第 12 条)明确 state-scanner 三条测试须在不带 `ARIA_COORDINATION_NO_PUSH` 的会话跑; TASK-021/TASK-027 第 7 步均显式重申此约束,TASK-031 的 SC-12 liveness 检查(重写 a 的 L1/L2/L3,非三条 unittest 本身)不受此环境变量影响,顺序与 v2.4 一致,v2.5 未引入新排序问题。

**本轮重点(新机制间交互)**: 逐一验证 13a/13b 拆分、会话入口 claim 核验、C.2.4.5 闸、TASK-027(b)/(c)、workspace 迁移这五处新机制之间的交互点(AB 会话边界的心跳交接、release 后免入口核验的时间窗、C.2.4.5 与 Forgejo 合并例外的顺序、claim 已释放但会话延续到 latest.md 提交前的中间态),均找到明确写死的处置文字或结构性排除,未发现卡死或恒绿组合。

## 对执笔人自报薄弱点的表态

1. **强制对齐依赖前置检查无盲区**: 可接受。我独立重跑 N11 证实对齐只在 `coord_ref_precheck` 已判定「本地领先的只有本轨心跳」(`verdict=ok kinds=['own-heartbeat']`)之后才做,丢弃范围有实测边界。
2. **入口核验防不住会话间隔期(>24h 只能事后发现)**: 可接受。这是 advisory + 最终一致协调哲学(非硬锁)下的结构性代价,不是本次修法能消除的,修法已把"事后发现"路由到明确的 owner_gates 第 14 项而非静默继续。
3. **13a/13b 中间态只记台账、无防止机制**: 可接受。与本计划全程"停下上报 + 记台账"的一致处置口径同构,建"防止机制"需要代码层修改(超出本 Spec 范围的文档/流程变更)。
4. **C.2.4.5 判据绑定脚本当前输出行格式,脚本一改就误停**: 可接受,且方向正确(fail-closed 而非 fail-open)——我直接读脚本源码确认当前输出前缀(`OK:`/`GATE:`/`PASS:`/`BLOCK:`)与判据描述一致,若未来脚本改格式,后果是"误停请人核实"而非"误放行漏检",符合本 gate 防止 gitlink 静默回退的设计初衷。
5. **同族扫描靠词形,首版曾漏两处,仍可能漏网**: 可接受。我用独立于执笔词表的正则方法(为空/无输出/零命中/零输出 + porcelain/ls-remote/wc -l/comm -23)对现文做了交叉扫描,两处命中经核实均非现行判据缺口,为本轮扫描覆盖度提供了独立佐证,但无法证明"零剩余"(词法枚举类扫描结构上不可能证明完备)。
6. **hard_constraints 第 14 条通则依赖执行者知道每条命令结果码,未知形态靠一般表述兜底**: 可接受。这是任何无法穷举失败模式的规则集的共性限制,通则的默认方向是"未知退出码⇒停下"(fail-closed),不是"未知⇒放行"。
7. **"Ran 数不得少于基线"在上游合法删测试时会误停**: 可接受。这是有意的保守设计——"测试数量下降"信号本身有歧义(真回归 vs 合法删除),对一个以"防止完整性静默丢失"为主题的 Spec 而言,把这类歧义信号导向人工核实而非自动放行是正确的默认方向。
8. **N11 是合成态(sweep 靠改 heartbeat_at 到 2000 年), 证明分支逻辑非生产时序**: 可接受,这也是我自己独立复现 N11 时采用的评估口径——TTL 类逻辑用时间改写而非真实等待 24 小时是标准且合理的测试手法,分支逻辑本身(对齐前后 resolve 结果不同、心跳/release 对 `claim_not_found` 的处置)已被我验证为真实可复现,自述的"非生产时序证据"限定措辞准确、未夸大。
9. **同体自检不能证明没有下一处**: 可接受,本轮为此提供一条新的、方向不确定的证据——我以独立方法(源码直读 + 脚本重跑 + 交叉正则扫描,而非重读执笔论证)覆盖了我分派到的视角,本轮未发现新的"下一处",但这只对我的视角(验收设计/可证伪性)成立,不能推广到其余四席的视角,也不构成"未来不会再有下一处"的证明。

## 风险 / 疑问

- **(A, dispatch 已知项) TASK-031 第 10 条"track-id 写错⇒停在 owner_gates 第 16 项"在 Phase D 不可达**: 本轮未发现新证据,严重度评估维持我 R4/R5 报告的结论(不到 major——一个照字面正确执行的执行者不会因此做错任何事,只是失去一层不存在的安全网幻觉),不重开 finding。
- **(B, dispatch 已知项) 执笔实例十条请裁**(`docs/handoff/2026-09-18-...` 与本轮 handoff 新增的十条): 均属待 owner 裁定的流程判断登记,不在我的视角(验收设计)下逐条评估,不作为 finding。
- **TASK-024 尾部"下个会话须做入口核验"的说明放在 TASK-024 verification 列表倒数第二条、而非 TASK-025 自身首条**: 组织位置上略微增加了跨任务追溯成本,但内容完整、顺序正确(bullet 7 强制对齐+entry check 逻辑上先于 bullet 8 的结果提交), 且即便被跳过也会在下一次 claim 相关检查点(TASK-030/031)被动检出而非静默通过——不构成"做漏"意义上的 finding,记录于此供参考。
- **TASK-030 C.2.4.5 是纯手动步骤(不像 C.2.4 那样有已有的自动调用路径)**: 残留风险是"执行者忘记手动跑这一步",此风险在文档/流程类 Spec(不改代码)下无法被本 Spec 自身消除,只能靠新增的 owner_gates 第 17 项与 5.8 行文本本身的显著性缓解;这是本仓 Rule #10(已启用闸不得自行豁免)与"本 Spec 不改代码只改流程文档"两个约束交叉下的结构性残留,非本轮新发现的缺陷。

## Verdict

verdict: **PASS**(0C / 0M / 0m)

**Vote: PASS**

## 是否足以开始 Phase B

**从我的视角(验收设计与可证伪性)足以**: R5 五个 Major、两条同处 minor、两个同族扫描候选,本轮经独立复核(含两次完整脚本重跑逐字节吻合、submodule_gate.sh 源码逐行核对、state-scanner 三处源码事实核对、SC 映射表全量交叉核对)全部确认 closed；v2.5 新引入的五处机制(13a/13b 拆分、会话入口 claim 核验、C.2.4.5 闸、TASK-027 (b)/(c) 重写、workspace 迁移)之间的交互点逐一检查未发现卡死或恒绿组合。与本视角无关的 `owner_gates` 第 1 项(10CG/Aria#195 完成 C.2 或 owner 明示改序)仍是独立于本次审计结论的外部前置门,不影响本视角的"足以"判断。
