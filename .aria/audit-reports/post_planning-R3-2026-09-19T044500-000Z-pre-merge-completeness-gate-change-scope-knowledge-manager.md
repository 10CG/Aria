---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-19T12:14:41.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R3 — knowledge-manager 席位报告

## 已实读文件

- `openspec/changes/pre-merge-completeness-gate-change-scope/tasks.md` 全文 (227 行)
- `openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml` 全文 (1676 行, 分 4 段读完)
- `openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md`: `:1-22`(头部)、`:153-220`(§1.1/§1.1b/§1.2/§1.2b)、`:221-271`(§1.3)、`:271-324`(§1.4)、`:356-406`(§4/§5)、`:407-452`(Tasks 17 项)、`:480-558`(rule6_note + 待 owner 复议 13 条 + 条目 0)
- `.aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md` 全文
- `.aria/audit-reports/post_planning-R2-2026-09-18T162427-983Z-pre-merge-completeness-gate-change-scope-aggregated.md` 全文
- `standards/conventions/content-integrity.md` §4.4/§4.5 全文
- `standards/conventions/skill-benchmark-exemption.md` 全文 (§1-§6, 重点 §4/§4.1)
- `docs/handoff/latest.md` (track 状态表, 核实 #195 现况)
- `aria/skills/state-scanner/scripts/lib/spec_complete.py`(`_CHECKBOX_ANY_RE` / `_iter_task_items` 定义, `:334-373`)
- `aria/skills/phase-c-integrator/SKILL.md:55-59`、`:130-134`、`:752-756`(实读, 核 N8 同形)
- `aria/skills/audit-engine/SKILL.md:421-425`(实读, 核 N8 同形)
- `standards/conventions/git-commit.md:182-210`(§6.1-§6.4, 核 Spec: trailer 写法)
- 实跑命令 (均在真仓只读; 未做任何写操作): `git diff --shortstat 21748d4 940cb5b`(standards, 逐文件)、`git diff --shortstat bf42cf4 a563192`(main_repo 七文件)、`git show a563192:.../proposal.md | sha256sum`、`git diff --shortstat 0a2ae53 a563192 -- proposal.md`、`git diff --stat 301641b 1cb3872`(aria 全量)、`python3 -B -c "..._iter_task_items..."`(对 tasks.md 实跑 31 项 checkbox 解析)、`python3 -c yaml.safe_load(...)`(校验 yaml 结构与依赖图)、禁用字形与裸 issue 引用扫描(对 tasks.md + detailed-tasks.yaml)、`git fetch origin refs/aria/coordination`(核实 claim 现况, 只读)、`git log --all --format=... | grep "^Spec:"`(核 Spec trailer 真实先例)

## Findings

| id | severity | type | category | scope | 摘要 |
|---|---|---|---|---|---|
| `699adf2f` | major | issue | documentation | `detailed-tasks.yaml TASK-001` | 基线复核清单未覆盖 standards, 与 `metadata.baseline_rebase.standards` 自己写的「必须重测」互相矛盾 |
| `a090f077` | minor | issue | documentation | `tasks.md 读前必看第 8 条` | 「§1.4 未全定义」的定位过窄, 实际字段取值分散在 §1.1(`:162`/`:170`) 与 §1.3(`:251`) |

### M1 `699adf2f` — TASK-001 基线复核清单遗漏 standards, 与本文件自己的指令矛盾

**证据**: `detailed-tasks.yaml:78` (`metadata.baseline_rebase.standards`) 逐字: 「standards 是并发轨随时会动的共享子模块, **TASK-001 必须对 B.1 当时的 gitlink 重测, 不得沿用本行数值**」; `:39`(`scope_repos` 的 standards 行) 同样写「基线复核…都以执行当时实测为准」。而 `TASK-001` 的**唯一**「基线复核」verification 条目 (`:1055`) 逐字只覆盖三组: 「对 `metadata.baseline_rebase.aria_zero_diff` 的每个文件与 `aria_shifted` 各条冒号前的文件跑 `git -C aria diff --shortstat 301641b <aria 起点> -- <文件>`, 对 `main_repo` 的文件跑 `git diff --shortstat a563192 <主仓起点> -- <文件>`」——**未出现 `standards` 字样**, 也未出现任何 `git -C standards fetch/diff` 命令。我把 TASK-001 全部 10 条 verification 逐条读完 (`:1047-1056`), 无一提及 standards; `git log`/`fetch` 的调用只对 `origin` 与 `aria` 两处。这不是孤立猜测: 我用 `python3 -B -c` 独立跑 `_iter_task_items` 只是确认 checkbox 解析, 而对文本本身的比对 (`grep -n standards`) 显示 standards 只在 `scope_repos`(`:38-40`)、`baseline_rebase.standards`(`:78`)、写法条款(`:115`)、`rule6_note.fields_basis`(`:140`)、`c25_five_questions`(`:471`,`:1645`)、`revision_log`(`:652`) 出现, TASK-001 verification 段 (`:1046-1056`) 里**零命中**。

**失败场景**: 执行者在 B.1 严格按 TASK-001 的「基线复核」条目字面操作 (三条 git diff 命令), 不会去重新 `git -C standards diff` 核对 `content-integrity.md §4.4/§4.5` 与 `skill-benchmark-exemption.md §4.1` 的当前内容。若并发轨在 `940cb5b` 之后又推进了 standards (完全不是假想: **本计划自己的历史刚发生过两次** —— `metadata.rule6_note` 与 `baseline_rebase.standards` 现在这版就是因为 `8b49562→940cb5b` 期间 `skill-benchmark-exemption.md` 升到 1.1.0、原「零 diff」断言两天内变假才诞生的 PP2-M4 修复), TASK-024/031 所依赖的 rule6_note 五字段合规判据与 TASK-018/026 隐含引用的 §4.4/§4.5 写法规则就会在一份已过期的 SOT 理解上继续执行, 而 31 个任务里**没有任何一条**会侧向发现这个漂移 (`TASK-030` 只核 standards 的 gitlink SHA 是否两端可推, 不核 §4.1/§4.4/§4.5 文本内容是否仍与本计划假设一致)。

**它怎么会红/不会红**: 基线 (今天, `940cb5b`) —— 断言与实测一致 (我已用 `git diff --shortstat 21748d4 940cb5b` 逐文件复核, 与 yaml 逐字节吻合); 目标 (B.1 时若 standards 未再动) —— 仍一致, 无害; 坏实现 (B.1 时 standards 已再动, 但 TASK-001 只字面执行三组 git diff) —— **不会红**, 因为清单里根本没有能红的断言, executor 会带着过期的 rule6_note/写法假设一路做到 TASK-024/031 才可能被 owner 或后续审计发现, 而不是在 TASK-001 当场拦下。

**建议修法**: 在 TASK-001 的「基线复核」verification 条目里补一句, 对 `metadata.baseline_rebase.standards` 点名的 6 个文件 (`content-integrity.md` / `skill-benchmark-exemption.md` 与其余四个「零 diff」文件), 在 B.1 当时的 standards gitlink 上重跑 `git -C standards diff --shortstat 940cb5b <B.1 时 gitlink> -- <六文件>`; 非空则逐处重读 §4.1/§4.4/§4.5 现文, 核对本计划的 rule6_note 结构与写法自检命令是否仍与之一致, 不一致则停下记台账走 spec 修订 (与 `aria_zero_diff`/`aria_shifted` 同等对待, 不因「本轨不改 standards」而降级)。

## R2 对账

| 键 | 判定 | 证据 |
|---|---|---|
| **PP2-M1** (claim 钉死 + `yielded` 一态失明) | **closed** | `TASK-001` 第 1/2/3 条已改为按 (本容器, 归一 track_id, `active`) 三元组运行时解析, 不引用固定文件名; `owner_gates` 第 14 项逐字覆盖 `done`/`yielded`/`abandoned` 三个终态 + 「本容器无该轨 claim」, 并对每个终态给出不同呈递措辞。我用 `git fetch origin refs/aria/coordination` 独立核验了真实协调 ref 当前状态: `claims/023236f2/s-86f7@1836.yaml` 确为 `status: yielded`(`heartbeat_at: 2026-09-17T11:54:49Z`), `claims/bfe8285d/s-73b9@1606.yaml` 确为 `status: active`(`linked_issue: 10CG/Aria#199`); 按 TASK-001 的算法在当前容器 `bfe8285d` 下逐字匹配 `track_id == pre-merge-completeness-gate-change-scope` 的候选恰为这一条 (另一条 `s-9762@1447.yaml` 的 `track_id` 带 `-bfe8285d` 后缀, 逐字比对不等, 会被正确排除), 算法在真实数据上可复现地resolve 到唯一 active claim。 |
| **PP2-M2** (`own_claim_files` 钉在失效文件上) | **closed** | `metadata.coord_ref_precheck.own_claim_files` 已改写为「TASK-001 在运行时…解析出的 claim 文件…不是写死的路径…重新认领后以新的解析结果整体替换」, 且补了 fixture-vs-生产 的反向指针 (采纳 R2 自报薄弱点 (d) 的可读性建议)。`coord_ref_precheck.code`(`:544-565`) 本身把 `own` 集合作为 `sys.argv[1:]` 传入, 结构上就是参数化的, 不含任何硬编码文件名。 |
| **PP2-M3** (`FIXED` 集放行「整条提交全落 FIXED 集」) | **closed** | `metadata.commit_attribution.code`(`:580-633`) 已重写为 exclusive/shared/foreign 三分类, `own` 现在要求 `exclusive` 路径存在**或** `Spec:` trailer 在场**且**无 `foreign` 路径, 纯 `shared` 集无 trailer 判 `shared-only`(停, 非 `own`)。我直读了 `N9` 自测输出(`:1021-1029`): 「bad: sibling release sync (shared paths only, no Spec trailer)」→ `exit=1 stop shared-only`(**正是** PP2-M3 要拦的形态); 「own release sync (shared paths only, Spec trailer present)」→ `exit=0 ok own-release-sync`; 「bad: foreign path + Spec trailer」→ `exit=1 stop`(trailer 不能洗白 foreign 路径)。`TASK-029` 新增「提交信息必须带本轨 trailer…提交后当场 `git log -1 --format=%B` 回读确认」, 且我用 `git log --all --format=... | grep "^Spec:"` 核实了 `Spec: openspec/changes/<id> (<issue>)` (无 `standards/` 前缀、无文件名后缀) 正是本仓近期真实提交(如 `10CG/Aria#211` 轨)已在用的写法, 与 `commit_attribution.TRAILER` 正则逐字匹配。 |
| **PP2-M4** (standards 零 diff 断言已失效 + `rule6_note` 散文不含 SOT 五字段) | **closed** | 两半各自独立复核: (1) `metadata.baseline_rebase.standards`(`:78`) 已重写并限定范围, 我用 `git -C standards diff --shortstat 21748d4 940cb5b` 对每个被引文件逐一实跑, 结果与 yaml 逐字节一致 (`content-integrity.md` +56/-2, `skill-benchmark-exemption.md` +21/-3, 其余四个引用文件均输出为空) —— **这个断言本身现在是真的**, 且明文声明「不是全称句」。(2) `metadata.rule6_note`(`:134-141`) 已含 SOT §4.1 要求的全部五字段 (`decision_table_row`/`description_changed`/`scenario1`/`scenario4b`/`negctrl`), 我对照 `standards/conventions/skill-benchmark-exemption.md` §4.1 原文逐字核对, 字段名、取值域与合规判据 (「`description_changed` 为 `yes` 时 `scenario1`/`scenario4b` 不得空」——本例 `description_changed: no`, 该判据不触发) 完全吻合, `fields_basis` 逐字段给出依据。**注**: 这个修复本身依赖 standards 内容在 `940cb5b` 之后不再漂移, 该风险即 M1 finding, 已单独列出。 |
| **PP2-M5** (`spec_level_undetermined` 未纳入 explicit-only 收窄) | **closed** | 读前必看第 8 条已把 explicit-only 收窄规则从「仅 S4 与 `no_spec_unverifiable`」扩到「S4、`no_spec_unverifiable`、`spec_level_undetermined` 三类被豁免的早退」; 同条给 SC-9(4) 的 fixture 补钉 `checkpoints: {post_spec: 'convergence'}`(mode 仍 adaptive) 并新增逐字断言 `checked_checkpoints == ['post_spec']`。`TASK-005`(RED 第二批)与 `TASK-011`(P5 实现)均落在既有格 `SC-9.4-level-undetermined-bypassed`(我核对 `stage_cells.cells['TASK-011']` 列表, 该格名确实已在其中), 不新增格名, 不影响既有 `stage_cells`/C1 证据。判断清单第 32 条对此变更如实记录「补钉是沿用第 23 条先例、新增的是逐字断言而非改期望值」。此修复的可证伪性论证是**读出来的**(脚本 Phase B 才存在, 无法真跑) —— 这是 Level 3 规划阶段的固有限制(见「自报薄弱点」(c)), 不因此判 open, 但值得记录。 |

## 对执笔人自报薄弱点的表态

**(a) trailer 判据把「归属」降级为提交者声明**: **可接受**。fixture 已证明「trailer 不能放行 foreign 路径」(N9 的最后一态), 而「trailer 被写在一条纯 shared 提交上却不是本轨」这一残余风险需要伪造意图且 `owner_gates` 第 2/9 项仍强制把 `git log` 清单呈给 owner ——人工复核这一关没有被撤掉; 反过来若砍掉 trailer 分支 (执笔实例自己提出的替代方案), 会让本轨自己每一次合法的发布同步提交 (TASK-029) 都必须停下请裁, 代价大于收益。

**(b) M4 的修复是记录更新不是机制**: **不可接受**, 且我已把这条具体化为独立的 major finding (`699adf2f`)——不是泛泛的「没加机械守卫」, 而是确认了 `TASK-001` 的基线复核清单**字面遗漏** `standards`, 与 `metadata.baseline_rebase.standards` 自己写的「TASK-001 必须重测」直接矛盾。这正是 PP2-M4 这个缺陷类别 (standards 断言随并发轨漂移) 第三次出现的入口点, 建议按 M1 的修法补上再进 Phase B。

**(c) SC-9(4) 的触发前提是读出来的不是跑出来的**: **可接受**。`completeness_gate.py` 是 Phase B 的产物, A.2/A.3 阶段对它的全部验收条款 (不止 SC-9(4), TASK-008~012 逐条皆然) 都只能通过文本论证反事实, 无法真跑; 这是 Level 3 规划文档的结构性限制, 不是 SC-9(4) 特有的缺陷, 也不因此拉低本条修复的可信度——反事实论证本身(P4 末尾统一装配 vs 边算边收 两个实现会给不同值)在逻辑上是自洽且可在 Phase B 落地后立即验证的。

## 风险 / 疑问

- `docs/handoff/latest.md` 实测: `10CG/Aria#195` 现况仍是「yielded (2026-09-17 交接) — A.2/A.3 已收口, **B.1 待起**」, 未完成 C.2 合并, owner 也未明示改序 ⇒ `owner_gates` 第 1 项独立于本次审计结果, 尚未满足 (与 R2 聚合报告的判断一致, 非本轮新变化)。
- R2 遗留的 8 条未动 minor (含 `TASK-029` 的 `main-project-version-consistency` 覆盖面问题) 我复核过其中的版本检查覆盖面点——`main-project-version-consistency` 探针描述里明写它验的是「主项目版本」9 个点, 与本 spec 的「aria-plugin 版本」16 个点是两个不同轴, 与 R2 结论一致, 无新证据, 不升级、不重复计入 finding。
- 执笔实例六条待裁项 (rule6_note.scenario1 占位 / scenario4b 与 negctrl 的 n/a 依赖零改动 / trailer 是声明非证明 / 5.7 漏 trailer 的新停点 / 多条 active claim 全纳入不挑不删 / TASK-030 边界切法) 均为已知且已在文中明确留痕的设计取舍, 不在我的视角判据范围内产生新 finding。

## Verdict

**PASS_WITH_WARNINGS · 0C / 1M / 1m · Vote: REVISE**

## 是否足以开始 Phase B

**不足以**——不只因为本轮 finding: `owner_gates` 第 1 项 (10CG/Aria#195 完成 C.2 或 owner 明示改序) 独立于本次审计结果, 实测仍未满足 (`docs/handoff/latest.md` 显示 #195 仍 `yielded`, B.1 待起); 且本轮新发现的 M1 (TASK-001 基线复核遗漏 standards) 建议在进 B.1 前补上, 避免 PP2-M4 这个缺陷类别第三次复发。
