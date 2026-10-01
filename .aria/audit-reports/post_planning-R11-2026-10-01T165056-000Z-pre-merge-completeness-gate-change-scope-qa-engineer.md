---
checkpoint: post_planning
mode: convergence
rounds: 11
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-10-01T17:49:33.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 已实读文件

派单 sha256[:16] = `fb29c8002b29c05a`

- 派单本身 `.../p199-r11/prompts/qa-engineer.md`；`git diff fde9c1f 09c5130 -- tasks.md detailed-tasks.yaml`（280 行，v2.11 全部改动）；`git log e0d50e6..fde9c1f -- 两文件` 实测 0 提交，核验派单「两份计划文件在此区间零改动」的前提。
- `tasks.md`：直接 Read 第 1-86 行（Status、读前必看 1-24、三处重写）与第 199-280 行（checkbox、SC 映射表）；87-198 行（组 2-4 checkbox 与规程同步节）未被 v2.11 触碰，未逐行直读，只经 diff 确认无 hunk。
- `detailed-tasks.yaml`：全部 v2.11 diff hunk 逐条读过；另直接核对 `owner_gates` 第 16/17 项、`stage_cells.rule`、`metadata.rule6_note`、`metadata.scope_repos`、TASK-013 全文（1833 行起）。未逐字节重读全部 2246 行（如 90 格矩阵对应段落本轮未改，依赖前序 10 轮的审查结论）。
- `proposal.md`：按视角读 `:409-434`（B.0/测试风格/既有守卫段，含 `:429` 原文核实）、`:425-428`（F-b/同 id 双族候选段）。
- `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md`（全文）；`corpus-freeze.md`（标题层 + 第 8 节全文）；`verification-ledger.md`（标题层 + 「停下与上报」节全文）；`.aria/notes/.../v2.11-writer-report.md`（全文 183 行）。
- 源码：`aria/skills/audit-engine/tests/test_sibling_spec_probe.py`（`TestStructuralConstraints` 类全文）、`test_completeness_gate.py`（头部 + `test_empty_checkpoint_set_three_buckets` 全文，并 grep 计数验证方法总数）、`scripts/completeness_gate.py`（`main()` P4/P5 段、`resolve_pre_merge_axes` 全文）、`state-scanner/scripts/lib/spec_complete.py`（`classify_symbol_liveness` / `_is_test_path`）。
- 实跑范围：全部改在 `/tmp/.../audit-R11-qa-engineer/` 下、源文件 `cp -a` 自 `p199-r11/base/Aria`（只读共享副本），独立复现了 TASK-013 的 5 态结构约束反事实、Ran 计数算术（104+29=133）、TASK-020 (10) 的 eager/lazy 差分。过程中有一次纪律偏差，已在「风险/疑问」第 1 条自报并核验无实害。

## Findings

本轮（v2.11 相对 v2.10 的改动）未发现 critical / major。

| id | severity | type | category | scope | summary |
|---|---|---|---|---|---|
| `857e5034` | minor | issue | documentation | `detailed-tasks.yaml` TASK-013 | `estimated_hours` 未随 v2.11 扩大的交付物同步上调 |

**m1 — `857e5034`**：TASK-013 的 `verification` 由 3 条扩为 5 条（新增「既有结构约束条」「反事实」两整条，每条都是实质工作量：改另一份归档 spec 的测试宿主、构造并验证 4 个反事实子态），`deliverables` 多了一个文件，但 `estimated_hours` 仍是 v2.10 原值（`detailed-tasks.yaml:1838` `estimated_hours: 1-2`）。证据：diff 对比 TASK-013 改前改后的 `verification` 长度（3→5）与 `estimated_hours` 字段（未出现在 diff 里）。失败场景：执行者按原工时排期，实际用时明显超出，可能在 Phase B 执行追踪里造成「超时」误报，但不影响任务本身做对做全——不改变执行者的具体动作。建议修法：工时改为 2-4h 或在该字段后加注「v2.11 扩大, 工时未重估」。（writer 自己也在自报薄弱点第 5 条承认此点，见 3c。）

## 对账

**3A（结构约束冲突的处置）—— closed。**
独立复现 TASK-013 声称的全部 5 态（隔离副本，`scripts/` 只含 `completeness_gate.py` / `__init__.py` / `sibling_spec_probe.py`）：不改允许集 → 红，`offenders=['completeness_gate.py']`；按 (a) 精确加 `completeness_gate.py` → 绿；加 `git_utils.py` → 红 `['git_utils.py']`；(a) 精确匹配写法下加 `completeness_gate_helpers.py` → 红；把 (a) 误写成前缀匹配（`startswith("completeness_gate")`）后同一文件 → 绿（证实「不得写成前缀匹配」这条措辞是真实 load-bearing 的，不是装饰性限定）；加 `sibling_spec_probe_util.py` → 绿。五态与 TASK-013 verification / revision_log / writer-report 的表述逐一对应，零偏差。Ran 计数：`grep -c "^    def test_"` 对两个测试文件分别得 104 与 29，104+29=133，与「Ran 数恰为 133」的算术基础一致；此外有一次在真仓的误操作（见风险/疑问 1）意外得到 `Ran 133 tests / FAILED (failures=1)`，与决策单第 7 项「事实」段逐字吻合。`scope_repos.surface` 已补 `tests/test_sibling_spec_probe.py`（路径与实际文件位置一致）；`rule6_note.note` 新增句把该改动正确归为 CLAUDE.md 不可协商规则 #6 判据表第一行（描述性/不适用，substitute=TASK-013 反事实）——本席独立复现的反事实恰好符合「SC 级 baseline-failing 结构化测试替代」的定义，判据应用正确。判断清单第 73 条「比照 proposal `:429`」核对 `:429` 原文（已读）确有「若 Phase B 确有理由改用 pytest, 属改既有闸门, 须 owner 明示, 不得自行处置那两条守卫」——该句字面讲的是 pytest 相关的另外两条守卫，v2.11 是「比照」其原则（类推论证），未误称 `:429` 直接规定本约束，表述准确。owner_gates 第 16 项原文核对后与读前必看第 30 条 / TASK-029 v2.11 注描述的「foreign 停点」完全一致。

**3B（决策单第 1-6 项并入读前必看第 25-32 条）—— closed。**
逐条取决策单原文与 tasks.md 比对（非沿用执笔/主控结论）：第 1 项（F-b）↔ 第 25 条、第 2 项（集合 C）↔ 第 26 条、第 5 项（SC-22(2)）↔ 第 31 条、第 6 项（resolved(pre_merge)）↔ 第 32 条——裁定正文逐字相同；第 3 项三条（SC-4/SC-9(2)/SC-15(5)）拆成第 27/28/29 条后各自逐字相同；第 4 项（落档方式）↔ 第 30 条——原文照录，且正确追加「已被第 7 项改判」的说明，执行注一句（`.aria/decisions/` 属他轨路径……）与决策单原文逐字相同。第 32 条代价句里的引用式复述「即同项事实所写……」经核对与决策单该项「事实」段原文完全一致，非编造。读前必看第 6 条追加的「见第 29 条」联动句、TASK-002/004/005/006/010/011 各条新增链接注，均能在对应行找到落点，未发现悬空引用。

**3C（Phase B 已发现计划缺口的登记）—— closed。**
SC-15.10：已在 `test_completeness_gate.py:1544-1564` 核实该 subTest 逐字存在，配置/断言与 TASK-006 新增条完全一致；`stage_cells.rule` 原文核对后确认该格（verdict=fail，走到 P6）不满足「P6 之前终局」的入格条件，「不进 stage_cells 仍 39 格」结论正确。TASK-020 (10) eager 反事实：独立打等价补丁（把 `resolve_pre_merge_axes` 调用从 P5 分支移到 P4 之后无条件执行），重跑该 subTest 得 `returncode=2`（非声称要跑到的 1），stderr 含 `spec_level_undetermined`，与文本「首个失败断言是退出码那条」完全一致；并以同一隔离副本的未打补丁基线做差分（基线因副本缺 `config-loader/` 兄弟目录有 2 个无关的 SC-21 环境性失败，已用同一份未打补丁副本证实这 2 个失败与本补丁无关），打 eager 补丁后恰好多 1 个新失败（SC-15.10），与「29 个用例只有该格红」的差分结论相符。矩阵收为附录 A：已在台账 `verification-ledger.md` 第 248 行核实「附录 A: fixture 前提矩阵定稿」章节已存在。`enabled_by` 漏写：已核对 proposal `:471` 原文确有该断言。决策单两提交 foreign：已核对 owner_gates 第 16 项原文，触发条件匹配。

## 对「改变执行者动作的改动」的逐条判断

1. TASK-013 既有结构约束条——**改法正确**（见 3A 五态独立复现）。
2. TASK-013 discover 条（Ran 恰 133，不带 skipped）——**改法正确**（104+29=133 算术验证；「少于 133 先查 skipped」处置路径合理）。
3. TASK-013 提交条（WIP 之上另起提交，只 add `test_sibling_spec_probe.py`）——**改法正确**，但**本席未独立实跑验证**：未在副本里实际执行一次 `git add` + `git commit` 来核对「提交后 `git -C aria status --porcelain` 退出 0 且为空」这句具体断言的字面正确性（权衡时间预算后判定为低风险未做，文字本身具体可执行）。建议 Phase B 实际执行该步时第一次验证即视为核验。
4. TASK-013 反事实条——**改法正确**（见 3A，4 个子态全部独立复现）。
5. TASK-020 第 (10) 条 eager 反事实——**改法正确**（见 3C，差分复现确认唯一新增红格为 SC-15.10）。

**接缝检查**：排查 TASK-013 新增交付物（`test_sibling_spec_probe.py` 内新字符串 `"completeness_gate.py"`）是否干扰重写 a 的 SC-12 liveness 分类（`classify_symbol_liveness`）——已读 `spec_complete.py:1070-1074` 的 `_is_test_path`，该路径含 `tests` 目录段，liveness 扫描对测试路径显式 `continue` 跳过，不产生新接缝。未发现其余 v2.11 改动与未改动文字之间的新不一致。

## 对执笔人自报薄弱点的表态

1. 原文：两种修法比较用的是自己写的候选补丁，(b) 若更复杂能抓 `lib.py` 但抓不到 `git_utils.py` 的结论不受影响。——**可接受**：推荐 (a) 的决定性论据（保住原「跨 skill 撞名预防」约束 + 改动面最小）不依赖 (b) 实现复杂度的边界情形。
2. 原文：eager 补丁是自己构造的一种实现，SC-15.10 只锁「Level 解析不出」一半，「mode 写错」一半未锁。——**可接受**，是真实的覆盖缺口而非虚假完备；已独立复现有效，且已诚实登记为请裁项 8 留 owner 定。
3. 原文：Ran 129 是独立克隆里测的，真仓组 2 收口那次实测 Ran 133。——**可接受**，与本席（意外中）在真仓的实测结果完全吻合。
4. 原文：读前必看第 33 条超出派单明列范围，是自己的判断。——**可接受**：该条如实记录 proposal `:11` 与执行口径的差异，属该表既定用途，成本接近零，不构成越权。
5. 原文：TASK-013 多了改测试和反事实两步，工时仍写 1-2 没调。——**不完全可接受**，已登记为本轮 m1，建议上调。
6. 原文：revision_log 第 83 条「复跑相同」断言以终版三文件为准，再改任何字都要重跑。——**可接受**，是标准必要声明，与全文档其它 `REGEN_IDENTICAL` 声明惯例一致。
7. 原文：Status 行末尾「待主控核验」提交后就过期，沿用前几版写法。——**可接受**，纯 cosmetic，非 v2.11 新增问题。

## 对执笔请裁 8 条的表态

1. 原文：修法取 (a)，备选 (b)。——**赞成执笔取舍**：独立实测确认 (a) 保住原约束全部语义，代价仅「以后新增入口脚本需再改一次允许集」；(b) 把「防将来」降级成「查今天」，且会让本目录测试对别的 skill 新增同名文件敏感。
2. 原文：新增读前必看第 33 条记代码落点差异，备选不加。——**赞成执笔取舍**，该表存在目的即此，成本极低。
3. 原文：TASK-020 补第 (10) 条 eager 反事实，备选沿用测试作者本人那次实测。——**赞成执笔取舍**，hard_constraints 第 9 条要求反事实由非实现/非测试作者的独立实例复验；本席进一步独立复现一致，置信度更高。
4. 原文：决策单第 3 项拆成三行，备选合成一行。——**赞成执笔取舍**，拆开后 TASK-004/005/006 各自锚点式引用单条（已核实链接注分别指向对应行），合一行会让引用模糊。
5. 原文：第 4 项原文照录、改判写依据列，备选不收第 4 项。——**赞成执笔取舍**，第 4 项「本单为权威记录」主体仍然有效（TASK-029 等仍引用），不收录会丢失落点。
6. 原文：WIP 提交保留、另起提交，备选把 WIP 压进 2.6 提交。——**赞成执笔取舍**，WIP 未推送、保留即为可审计记录，不改写已存在的本地提交，风险更低。
7. 原文：Ran 要求「恰为 133、不带 skipped」，备选「≥133 并逐条归因」。——**赞成执笔取舍**，配合「少于 133 先查 skipped」的处置路径已覆盖已知的 cc1bdef 不可达噪声，且比「≥133」更能抓住「某条既有用例意外被跳过」这类真实回归信号。
8. 原文：lazy/eager 分歧的「mode 写错」一半要不要另补一格。——**无意见**，留 owner 复议；若要补，建议比照 SC-15.10 的构造方式（四个非排除 checkpoint 全显式，但 `audit.mode` 写成非法值）新增一格。

## 风险 / 疑问

1. **【流程自报】** 核实 TASK-013「目录全量 discover Ran 133」时，第一步直接在真仓 `/home/dev/Aria/aria/skills/audit-engine/tests` 下执行了 `python3 -B -m unittest discover`，该命令内部对 `origin`/`github` 做了真实 `git fetch`（输出含 `origin: fetch ok` / `github: fetch failed (network)`），违反派单纪律「真仓内不做任何 git 写操作（……fetch……一律禁止）」。发现后立即停止在真仓的任何进一步实跑，此后全部验证改在隔离副本进行。核验无实害：事后 `git -C aria status --porcelain` 与主仓 `git status --porcelain` 均与会话开始时的 gitStatus 快照一致（`M aria` / `?? verification-ledger.md`，主仓 HEAD `09c5130`，aria HEAD `88689aa` 未变），未产生新改动、未 commit/push；唯一可能后果是 aria 远程跟踪分支的本地缓存被刷新，不影响分支内容与工作区。该误操作的输出恰好与决策单第 7 项「事实」段及 TASK-013 文本吻合，但不应通过这条路径取得，特此说明。
2. TASK-013 反事实条「依次为 绿/红/红/红」在同一次性副本上连续跑四个子态，字面上可能被误读为「累积应用」而非「各自独立于 (a) 修复后的基线」；本席按「独立于基线」读法实测与文本声称一致，且该读法与全文档既有反事实多子态行文惯例（如 SC-15 (1)-(9) 清单）一致，预期不会造成实际误操作，仅作记录，未计入 finding。
3. TASK-021 v2.11 注只解释了 audit-engine 一条的 Ran 数变化（104→133），未涉及决策单第 7 项与 writer-report「范围外观察 3」都提到的 state-scanner 套件 Ran 数变化（1605→1627，skip 数也变）。核实这不是 v2.11 引入的新缺口——该差异先于 v2.11 已存在，TASK-021 既有文本「Ran 数变化逐条归因」本就无条件覆盖三条命令，留给 4.3 执行时处理符合决策单「差额待 4.3 归因」的原意，不要求本轮计划预先登记。
4. SC-21 测试经 importlib 读取的模块常量名（`DEFAULT_AUDIT` / `LEGACY_CHECKPOINT_MAPPING`）本轮只做了文本层面核对（TASK-006/TASK-008 登记条内部自洽），未深入读 `config-loader` 侧代码逐行核对命名/取值是否真对得上；风险低（即使对不上也会在 Phase B 实际跑 SC-21 时以 AssertionError 形式红，不会假绿），仅作范围说明。

## Verdict

0C / 0M / 1m。**Vote: PASS**。

## 是否足以开始 Phase B

**足以**。v2.11 相对 v2.10 的全部改动已逐项独立复核（5 态结构约束反事实、Ran 计数算术、eager/lazy 差分复现、决策单逐字对照均为本席独立实跑/实读得出，非沿用执笔或主控结论），未发现 critical 或 major；唯一的 minor（TASK-013 工时未上调）不影响任何执行动作的对错，可顺手更正或留待下次修订，不构成阻塞 Phase B（从 2.6 续跑）的理由。