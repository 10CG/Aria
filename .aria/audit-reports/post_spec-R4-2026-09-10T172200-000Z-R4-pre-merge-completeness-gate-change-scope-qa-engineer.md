---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T20:15:07.539Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [qa-engineer]
---

# post_spec R4 — qa-engineer 席位报告

被审对象: `/home/dev/Aria/openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md` (v4, R3 rework 后)。本席为新席位, 不继承上轮结论; 全部事实以实读/实跑复算为准, 基线 = 插件缓存 `~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` (= aria `301641b`)。

**R3 落地总判**: 3 Critical + 12 Major **全部落在正文**, 不是批注 —— 逐条核到 §1.0 求值总序 (:89-103)、§1.3 Level 三判据 (:180-182) 与四值优先级链 (:169-175)、§1.1 S3 三条核验 + `--anchor-base` (:84,:111)、§1.4 stderr/stdout 分流 (:239)、SC-13 分块计数 (:347)、Tasks unittest 风格 (:315) 均有实体条款。正文引用的语料数字我全部独立复算, 除一处外逐个吻合。**新问题集中在两处**: (1) R3 为修 `506ce733` 新钉的求值总序, 其下游 fixture 前提没跟着补齐 (Issue 2 / Risk 1); (2) R3 为修 `affceac8` 新钉的 B.0 无人值守仲裁规则, 反过来把 SC-2 依赖的两个语料族结构性剔空 (Issue 3)。另有一条 R2 时代就存在、五轮无人命中的作用域求值序漏洞 (Issue 1)。

## 审计结论

### Decisions

- [minor] testing/R3 Critical 落地核验: 3 条 Critical 均落正文非批注 —— Level 三判据 (proposal.md:180-182) / 四值优先级链 (:169-175) / S3 三条核验 + `--anchor-base` (:84,:111)。本席按判据自写解析器全枚举 153 份 `openspec/{changes,archive}/*/proposal.md`: 解析成功 144 / 失败 9 (与正文点名的 9 个归档件逐字同集) / 首命中 >15 恰 **7** 份 (含 `2026-09-06-a1-entry-claim-duplicate-work-guard` L58, 实读逐字 `> **Spec Level**: 2`) / 含 `Spec Level` **15** 份 / 行首形态 **139-3-2-0** —— 与 A1 订正后的正文全部一致, 与聚合席的 6 份/138-3-2-1 不一致 (执笔席的不采纳理由成立) (证据: proposal.md:180-184; openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/proposal.md:58)
- [minor] testing/R-h 与 SC-22(1) 的失效方向: 本席 hermetic 复跑 (tmp 仓 origin/master=c3、本地 master 强制退到 c1、feature 从 origin/master 开出) —— `git diff --name-only --no-renames $(git merge-base HEAD master)` 输出 **4** 个文件 (含他人 `openspec/changes/other/proposal.md`), 换 `origin/master` 输出 **2** 个 ⇒ 「陈旧 base ⇒ merge-base 更旧 ⇒ diff 超集 ⇒ 作用域膨胀 ⇒ `missing` 假红」方向成立, SC-22(1)(i) 的 fixture 可构造 (证据: proposal.md:299,356)
- [minor] testing/SC-12 既有测试基线: 今日实跑三套件全绿 —— `audit-engine/tests` 104 tests OK, `phase-c-integrator/tests` 148 tests OK, `state-scanner/tests` 1593 tests OK, 0 failure ⇒ SC-12 不存在需要 carve-out 的既有失败项; `run_all_tests.sh --list` 现把 audit-engine 归为 `(unittest)`, Tasks 的 unittest 风格约束与现状一致 (证据: proposal.md:346,315; aria/skills/run_all_tests.sh:41-45)
- [minor] testing/语料与契约事实复核: 独立复算全部对上 —— `.aria/audit-reports/` 顶层 **837** 份 `.md`; 末段族 (stem 以 `-{id}` 结尾) **62** 份; unattributed 全 8 checkpoint 口径 **170** 份、本仓 `checked={post_spec,post_planning}` 口径 **160** 份; 真 2-field legacy **6** 份; `C` 今日 **153** (正文冻结快照 152, 差 1 = 本 spec 自身目录)。9 个 `error_kind` 逐个有 SC 承接。AB 面复核: `ab-suite/version.yaml` 仍 `1.5.0` (同伴轨未再 bump)、`audit-engine.json` `version 1.0.0` 2 evals、`phase-c-integrator-pre-merge-gate.json` 无 `evals` 键 / 8 `fixtures` / `type: workflow_skill_subextension` (证据: proposal.md:52,143,232,264; aria-plugin-benchmarks/ab-suite/version.yaml:1)

### Issues

- [major] implementation/§1.1 S2-S3 + SC-7: S3 的前提逐字是「S2 为空且 `--no-spec`」, 而 S2 的条件是「无显式 id」—— 传 `--no-spec` 时并没有显式 id, 所以单仓形态下只要 diff 触到 `openspec/changes/<id>/`, **S2 先命中并返回 `scope_source=diff`**, `--no-spec` 被静默吞掉, `no_spec_contradicted` 永不触发。SC-7 却断言「`--no-spec` 且 diff 触 change 目录 → exit 2 `no_spec_contradicted`」⇒ 该格按本文钉死的 first-match 序**不可达**, Phase B 要么这条测试必红, 要么实现者私自把 `--no-spec` 提到 S2 之前 (改变已定契约)。这与 R3 minor `d081c6d9` 修的是**同一个失效** (「S1 的 first-match 会静默吞掉 `--no-spec`」), 只封了 argparse 那一半; 跨仓格 (SC-17(4)) 因子模块内无 `openspec/` 才碰巧可达。待 owner 复议 #2 对残余强度的估价同样建立在「该守卫在单仓可达」的前提上 (证据: proposal.md:110,111,341,351,369)
- [major] testing/§1.0 P1 与 §1.4 格 A 的前置条件冲突 + 十条 SC fixture 缺 `enabled`: §1.0 P1 逐字把「`audit.enabled != true` ⇒ `audit_not_enabled` exit 2」提为**无条件前置**并注明「刻意排在作用域之前」(:96), 而 §1.4 该表仍挂在标题「**纳入集为空**: 按成因分三格」之下 (:220) —— 同一份文档给出两种合法读法: 按 P1 是无条件, 按 §1.4 只在空集时。这个差别是承重的, 因为 SC-1 (`post_implementation=convergence`)、SC-3、SC-4 (`{mode:'manual', checkpoints:{…}}`)、SC-5、SC-6、SC-8、SC-16、SC-17、SC-19、SC-22 的 fixture config **字面都没有 `enabled: true`** (只有 SC-15 与逐字引用官方场景 A/B/C 的 SC-15(3)/SC-20(1)(2) 有, 因为 `config-example.md:386,407,426` 自带该键)。按 P1 读法这十条一律先落 `audit_not_enabled` exit 2, 与各自期望的 exit 0/1 直接冲突; 而 §1.0 末段的两条 fixture 硬约束 (:103) 只钉了 `audit.mode` 与 Level 行, Tasks 的「既有 SC fixture 前提全量回扫」(:316) 也只列这两条 + 作用域, **`enabled` 这一格无任何任务承接** (证据: proposal.md:96,103,220,316,335,337,338,342,350; config-loader/config-example.md:386)
- [major] testing/Tasks B.0 仲裁规则结构性剔空 SC-2 的 F-e 与 F-f 两族: B.0 规则 (b) 逐字「两列不一致 **或** 第一列取不到 ⇒ 该文件整份剔出 SC-2/SC-4 的 fixture 样本池……不是供人裁, 是当场剔除」(:313)。但第一列的两个来源 (frontmatter `context:`/`spec_id:`/`change_id:`, 或写盘时刻的活跃 change 目录 git 历史) **只能产出一个 change_id**, 而 F-e (真 legacy) 与 F-f (unattributed) 这两族的正确标注按定义就是 `legacy` / `unattributed` ⇒ 两列**恒不一致**, 全族被剔。这不是假想: 本席实测 6 份 legacy 里 3 份带 `context: openspec/changes/auto-audit-system/proposal.md` 一类字段, 170 份 unattributed 里 **106** 份带指向真 change 的独立字段 (如 `post_spec-R1-1783541662234-agent-router-injection-tech-lead.md` → `agent-router-auto-project-agent-injection`), 其余的第一列取不到 —— 两条通道都落进规则 (b)。规则 (c) 的兜底是「换 id 重新采样, 换不到则该族降为 **≥1** 份」, 在 0 样本时无解, 且明写「不得为了凑数把争议条目放回去」⇒ 无人值守的 Phase B 在这两族上没有任何合法动作。而 SC-4 的「两个计数分离」正是 R1 Critical-1 的封口, 失去这两族的真实语料样本后只剩手造名字, B.0 想防的「自指恒绿」以更软形态回来 (证据: proposal.md:313,336,338)
- [major] documentation/§1.3 校准数字与自身判据 2 矛盾: 判据 2 明写「取值前先剥掉 `~~…~~` 删除线片段」(:181), 但紧接着的「本轮对真实语料的实跑校准 (可复现)」给的分布是 **Level 3 → 57 / Level 2 → 86 / Level 1 → 1** (:184)。本席按判据 2 实现解析器复算得 **58 / 85 / 1**; 关闭剥离才得到 57/86/1 —— 差的那份正是判据 2 自己举的 `openspec/archive/2026-08-16-premerge-gate-branch-existence/proposal.md:29` (`> **Spec Level**: ~~2 (proposal only)~~ → **3**`)。同段「另实跑『严格判据 vs 原稿宽松正则』逐份对照, 144 份取值**逐个相同**, 判据收窄未引入取值漂移」因此也是假的: 恰好这一份翻档 (2 → 3), 而这正是 A2 新增该子规则的全部理由。Phase B 若照 :184 的数字复核会得出「我的解析器错了」并可能删掉剥离规则 (证据: proposal.md:181,184; openspec/archive/2026-08-16-premerge-gate-branch-existence/proposal.md:29)
- [major] testing/两条 R3 新增规范条款零 SC 承接: (1) `--change-id` 与 `--no-spec` argparse 互斥 + exit 2 + 指定文案 (:87, 修 minor `d081c6d9`); (2)「迭代口径 = 逐对, 不是叉乘」并明写「不得被实现读成并集 × 全部 change_id —— 那会对本该 off 的那一对判 missing 假红」(:190, 修 minor `d3eeec78`)。SC-1~SC-22 全表对这两条**零断言** (`叉乘` 0 命中; `互斥` 的 2 处命中分别是 SC-10 与 SC-13 里描述断言互斥的行, 与 argparse 无关)。第 2 条被误读的后果是混合 Level 多 change PR 上的假红阻断合并, 属于本 spec 反复强调要钉死的失效族 (证据: proposal.md:87,190,344,347)
- [minor] testing/SC-2 选样硬约束在真实语料上不可满足: SC-2 要求「所选 id 在 fixture 中必须**同时**有 F-a 与 F-b 两族样本」且每族 ≥3。本席对 837 份全枚举: 同时满足 F-a≥3 且 F-b≥3 的 id **只有** `state-scanner-mechanical` (F-a 6 / F-b 8) —— 与 B.0 item 4 的「唯一候选」判断一致; 而该族 15 份**全部无 frontmatter** 且写盘时刻目录名是 `state-scanner-mechanical-enforcement` (git 历史实证: `32422df` 首次落 `openspec/changes/state-scanner-mechanical-enforcement/proposal.md`), 15/15 两列不一致被剔。剔除后仍同时具两族的 id 只剩 **`state-scanner-inter-cycle-surfacing`** (F-a 2 / F-b 3), 正文未点名它 ⇒ Phase B 只能自行摸索或改造 hermetic 样本 (证据: proposal.md:313,336)
- [minor] testing/SC-4 截断文案与逐字模板不一致: §1.2 计数表 (:143) 与 §1.4 trail 行 (:243) 给的 WARN 模板逐字以「, … 其余 K 份见 stdout 的 `unattributed`」结尾, 而 SC-4 的附加断言写「stderr 的 WARN 行只列前 20 个文件名并以 `… 其余 2 份` **收尾**」(:338) ⇒ 按 endswith 写的断言在正确实现上必红, 按 contains 写又漏掉了模板后半段 (证据: proposal.md:143,243,338)
- [minor] documentation/Tasks 测试风格对既有守卫的引述失准: Tasks 写「`:303-316` `TestNoPytestImport` 断言**本目录源码**不含顶层 `^(import|from)\s+pytest`」(:315), 实读该用例只读自己 (`src = Path(__file__).read_text()`, test_sibling_spec_probe.py:315), 对同目录新文件失明; 真正覆盖新文件的是 `TestRunAllTestsDiscovery` 经 `run_all_tests.sh:43-45` 的**目录级** grep (`grep -lq '^import pytest\|^from pytest' "$1"/test_*.py` + `conftest.py` 探测)。结论 (必须 unittest、禁 pytest import 与 conftest) 不变, 但引述需订正, 否则 Phase B 可能以为改自己那份文件就能绕开 (证据: proposal.md:315; aria/skills/audit-engine/tests/test_sibling_spec_probe.py:303,309-316,319-336; aria/skills/run_all_tests.sh:41-45)
- [minor] testing/SC-13「Step 4 围栏块切片」在 SOT 里没有对应物: SC-13 要求「对 `execution-modes.md` **只在 Step 4 的围栏块切片内**计数字面串 `scripts/completeness_gate.py`, 恰 1」(:347)。实读 SOT: Step 1~Step 5 全部在**同一个**围栏内 (execution-modes.md:23 开、:66 闭), Step 4 不是独立围栏块 ⇒ 「切片」的起止无定义, 两个合法实现 (按 `Step 4:`~`Step 5:` 文本切 vs 按整块切) 计数不同, 护栏本身可判决相反。建议改为「以 `Step 4:` 行起、`Step 5:` 行止的行区间内恰 1」这类可机械复现的界定 (证据: proposal.md:347; execution-modes.md:23,54,63,66)

### Risks

- [minor] testing/SC-15(2)(3)/SC-19/SC-20/SC-22(2) 的作用域缺口只挂在任务上: §1.0 明写「本 spec 钉死如下全序……**全部 SC 的期望值按此顺序取**」(:89-103), 但这几条 SC 的 fixture 至今没有作用域来源 (`--change-id` + 锚点 / 触 change 目录的 diff / `--no-spec`), 按 P2 会先落 `change_scope_unresolved` exit 2 —— 例如 SC-15(2) 期望 `pre_merge_not_enabled`、SC-19(a) 期望 `matched_count == 1`、SC-20(1) 期望 `checked_checkpoints` 含 `post_implementation`, 三者都到不了。修正被推给 Tasks 的「既有 SC fixture 前提全量回扫」(:316), 由**无人值守**的 Phase B 自行改写期望值。这就是 B.0 想防的「标注者与实现者同体」在 SC 期望值上的翻版: 期望值一旦由实现者按自己的实现重算, 反事实就失去独立性。缓解建议: 把这几条的 fixture 与期望值在 spec 内当场补全 (与 SC-3/SC-4/SC-9 同等待遇), 不留给 Phase B (证据: proposal.md:89-103,316,349,353,354)

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **5** / Minor **4** (另 1 条 Risk(minor) + 4 条 Decision 不计入缺陷数)。

rationale: 本 spec 的机制设计在 R3 之后已相当扎实 —— 三条 Critical 的修法都落到了可实现的条款上, 我按其判据自写解析器与 hermetic fixture 复跑, 关键事实 (Level 判据分布、陈旧 base 的超集方向、语料四个计数、AB 套件形态、既有三套件全绿) 逐条对得上, 没有发现「SC 恒绿导致假绿」这一类致命项, 故不判 FAIL。但五条 Major 都落在**可测性**这条主线上: 一条作用域求值序漏洞使 SC-7 的一个格不可达 (且与本轮刚修的 `d081c6d9` 同型), 一条新前置 (P1) 与十条 SC 的 fixture 前提脱节且无任务承接, 一条新仲裁规则把 SC-2 依赖的两个语料族剔成空集, 一条校准数字与自己的判据自相矛盾, 两条新契约条款没有任何断言承接。按 post_spec 的 blocking:false 语义这不阻断流程, 但 Phase B 是无人值守, 这五条会以「测试必红 → 实现者自行改期望值」的形式落地, 正是本 spec 自己反复钉的自指恒绿路径, 故投 REVISE。

## 轮次记录

### Round 4: Agents

- Agents: qa-engineer (五席之一; 本报告仅代表本席, 不含汇总)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 14 (Decisions 4 / Issues 9 / Risks 1)
- Vote: REVISE
