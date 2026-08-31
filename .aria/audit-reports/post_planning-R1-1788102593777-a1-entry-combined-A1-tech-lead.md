---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-30T15:26:24.452Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 2
major_count: 6
minor_count: 4
---

## 摘要

三份 yaml 全部合法解析, 编号无重复, 依赖无悬空, 三份 DAG 均无环 (亲跑)。母 Spec 的 Phase B.1 前置 (TASK-001) 逐条命令亲跑**全部为真** (两 remote ls-remote 均 `d69091d`, gitlink 一致, `test_coordination_no_push.py` 恰 16 个 `def test_`, phase1_gate/release_gate/failure_handlers 五个行号锚点逐一命中)。跨 Spec **语义**接缝 (E0–E6 四态 → 探针分层映射 / 哨兵吃 E3 原串 / `line_no` 1-based / `--emit-arg` 空输出即省略 / 母 Spec 不消费探针输出) 三份互相咬合, 无矛盾 —— 这一面是收敛的。

问题**全部集中在两个非语义接缝**上, 而它们恰好是三席各写各的、没人负责合起来看的面:

1. **发布同步面**。三份 Spec 各自写了一份「主仓版本引用面」任务, 三份写法互不相同, 其中**两份被机械证明必红**: 探针 TASK-018 与母 TASK-038 都断言 `m6-version-badge-match` / `i18n-readme-translation-currency` 通过, 但两者的 deliverables 都不含使这两条 check 变绿所必需的文件。我在真仓上模拟了 bump 后的取值 (见实测记录): 两条 check **必然 exit 1**。母 Spec 还写了一个**仓内不存在的路径** `README.zh-CN.md` (实为 `README.zh.md`)。字段 Spec 的 TASK-024 是三份里唯一写对的 —— 同一个类, 一份对两份错 (memory `fix-the-class`)。
2. **AB 套件面**。`ab-suite/spec-drafter.json` 被三处任务并行写 (字段 TASK-016 / TASK-017 彼此无依赖边, 加母 TASK-035), 无 eval id 分配约定; `ab-suite/version.yaml` 只有探针一份 Spec 维护, 而字段 (+1 eval) 与母 (+6 eval) 都改套件却不动它 ⇒ 探针写进去的计数被后 ship 的母 Spec 必然写陈旧。

外加一条版本号撞车 (字段与母**都**自判 `v1.68.0`, 而 ship 顺序是串行三档) 与一条跨 Spec 断言矛盾 (字段两处断言 `audit-engine/` 只有两个条目, 而探针 Spec 被 mandate 在其下建 `scripts/` 与 `tests/`)。

判据: 2 critical ⇒ **FAIL**。这些**不需要重做 A.2**, 全部是 deliverables/verification 字段级订正, 建议 R2 只审这两个面。

---

## Findings

| id | severity | category | scope | type | 描述 + 证据 + 处方 |
|---|---|---|---|---|---|
| `a257ffa4` | critical | architecture | `openspec/changes/sibling-spec-probe/detailed-tasks.yaml` | issue | **TASK-018 的发布同步面缺主仓整片引用面, 且其自身两条断言被证明必红。** deliverables = `aria/CHANGELOG.md` + `plugin.json` + `marketplace.json` + `aria/VERSION` + `aria/README.md` + `CLAUDE.md` —— **缺主仓 `VERSION`、root `README.md` badge、i18n ×3**, 而 CLAUDE.md §版本管理逐字规定发布同步面 = 「aria 子模块 5 文件 + 主仓 gitlink + **主仓 VERSION** + **root README badge** + **i18n README**」。同任务 verification 第 2 条却断言 `m6-version-badge-match` / `i18n-readme-translation-currency` **通过**, 并逐字写「i18n README 仅正文实质变更才重译 — 本次无正文变更 ⇒ **不重译**」。**证据 (实跑, 见实测记录)**: `i18n-readme-translation-currency` 读的是 `<!-- translated-from: vX.Y.Z -->` **标记**, 不是正文 (`.aria/state-checks.yaml:161-173`); 三份 i18n README 当前标记均 `1.67.2`。模拟 `plugin.json` 升 `1.69.0` ⇒ `stale=[README.zh.md@1.67.2, README.ja.md@1.67.2, README.ko.md@1.67.2]` ⇒ `sys.exit(1)`; 同时 `README.md` badge 仍 `1.67.2` ⇒ `m6-version-badge-match` `DRIFT` ⇒ exit 1。⇒ **该任务按写法执行必然使两条 check 红, 而它断言它们绿 —— 自相矛盾, 且把主仓留在漂移态。** **处方**: TASK-018 deliverables 补 `VERSION` / `README.md` / `README.zh.md` / `README.ja.md` / `README.ko.md`; 把「不重译」一句改为「**正文不重译, 但 `translated-from` 标记与两处版本串必须同批改**」(#140 B 档管的是正文, 不是标记); 或直接照抄字段 TASK-024 的 12 点口径 |
| `73809784` | critical | architecture | `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml` | issue | **TASK-038 deliverable 含一个仓内不存在的路径, 缺两个语种, 并同样断言必红的 check 为绿。** deliverables = `.gitmodules` / `VERSION` / `README.md` / **`README.zh-CN.md`**。**证据**: `ls README*` ⇒ `README.ja.md README.ko.md README.md README.zh.md` —— **`README.zh-CN.md` 不存在**; `.aria/probes/main-project-version-consistency.py:44-46` 与 `i18n-readme-translation-currency` (`.aria/state-checks.yaml:156`) 两处 POINTS 清单逐字都是 `README.zh.md` / `README.ja.md` / `README.ko.md`。verification 第 1 条断言 `i18n-readme-translation-currency` 绿, 但 ja/ko 根本不在 deliverables, zh 又写错名 ⇒ 与 `a257ffa4` 同一机制, **bump 后必红** (实跑同上)。另: **`.gitmodules` 不承载 gitlink** —— 实读其全文只有三组 `path`/`url` (无 SHA), gitlink 是 index/tree 条目 (`git ls-files -s aria` ⇒ `160000 d69091d… aria`), bump 它不产生 `.gitmodules` diff。**处方**: `README.zh-CN.md` → `README.zh.md`, 补 `README.ja.md` / `README.ko.md` / `CLAUDE.md`; 删 `.gitmodules`, 改为 verification 里已有的「gitlink bump」表述 (deliverables 写 `aria` 子模块条目本身, 参照字段 TASK-022 的写法) |
| `3221f943` | major | architecture | `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml` | issue | **字段 Spec 与母 Spec 都自判 `v1.68.0`, 而 ship 顺序是串行三档。** 证据: 字段 `tasks.md:7` 逐字「ship target: aria-plugin **v1.68.0**」+ yaml `metadata.ship_target`; 母 `tasks.md:80/:89/:195` 与 yaml `TASK-037` 标题「A.2 自判 MINOR **v1.68.0**」+ verification `grep -rn '1.68.0'`; 母 `metadata.ship_order` 逐字「linked-issue-field-availability → sibling-spec-probe → 本 Spec」。三份串行 ship ⇒ 号段只能是 1.68.0 / 1.69.0(或 .1) / 1.70.0, 两份不可能同为 1.68.0。母 Spec 的 **TASK-031~035 五处 deliverable 目录字面量** `ab-results/<YYYY-MM-DD>-v1.68.0-a1-entry-rule6/…` 是**未加对冲的**硬编码 (TASK-037 标题虽写「号段落地时计算」)。⇒ 按写法执行会把母 Spec 的 AB 结果归档到一个属于字段 Spec 的版本目录下, 且 `grep -rn '1.68.0'` 断言指向错误号段。**处方**: 母 Spec 三处 (TASK-037 verification / 五处目录字面量 / tasks.md:195) 一律去掉 `1.68.0` 字面量, 改为「= 本 Spec 落地时 `plugin.json` 计算所得号段」; 探针 Spec 的写法 (「号段落地时算, 不预写」+ 档位待 owner) 是三份里唯一无风险的, 建议统一到它。**owner 决策项**: 三份是否合并为一次发版 (一次 MINOR) 而非三次 —— 三次串行 bump 意味着三轮完整发布同步面 + 三次双推核验 |
| `c23f47ce` | major | testing | `openspec/changes/linked-issue-field-availability/detailed-tasks.yaml` | issue | **字段 Spec 两处断言 `audit-engine/` 目录内容, 而姊妹探针 Spec 被 mandate 往里面建两个目录 —— 跨 Spec 断言直接矛盾, 且是对 proposal 的过度派生。** 证据: 字段 yaml `:268` (TASK-008 verification) 与 `:526` (TASK-020 **全量回归**) 逐字「`ls aria/skills/audit-engine/` 仍只有 references/ + SKILL.md」/「== references/ SKILL.md (:278)」; 而探针 yaml TASK-010 deliverables = `aria/skills/audit-engine/scripts/sibling_spec_probe.py` + `scripts/__init__.py`, TASK-004 deliverables = `aria/skills/audit-engine/tests/test_sibling_spec_probe.py`。**派生偏离**: 字段 proposal `:278` 原文只约束「`audit-engine` 内**不得新建名为 `lib/` 或 `collectors/` 的顶层目录**」—— 它管的是同名包碰撞, 不是目录条目总数; 探针 TASK-004 的渲染 (`not (AUDIT_ENGINE/'lib').exists() and not (AUDIT_ENGINE/'collectors').exists()`) 才是忠实派生。⇒ 字段 Spec 把一条包名约束收紧成「姊妹不许交付」的不变量, 放进了自己的**回归门**; 该断言在探针 ship 当天永久转红, 且红的原因与字段 Spec 无关 (memory `false_green_dual_is_permanent_red`)。**处方**: 字段 yaml 两处一律改为与探针 TASK-004 同形的「`audit-engine/` 下不存在顶层 `lib/` 与 `collectors/`」, 删掉「只有 references/ + SKILL.md」的字面; 同步改 `tasks.md:57` 与 `:129` 那一行 |
| `6698004d` | major | testing | `aria-plugin-benchmarks/ab-suite/version.yaml` | risk | **三份 Spec 都改 `ab-suite/`, 只有一份维护 `version.yaml` 的计数, 且它维护的口径本身就是陈旧基线。** 证据: 探针 yaml TASK-003 deliverables 含 `version.yaml`, 其 `tasks.md:33` 逐字「skills_covered **29→30**, total_eval_cases **58→60**」; 而同任务 verification 又断言「`ls ab-suite/*.json | wc -l` == **32**」。实测当前值: `ls ab-suite/*.json | wc -l` = **31**, 逐文件累加 `evals` = **73**, 而 `version.yaml` 声称 `skills_covered: 29` / `total_eval_cases: 58` ⇒ 基线已漂 2 skill / 15 case。「29→30」与「31→32」在同一任务内自相矛盾。更关键的是**跨 Spec**: 字段 TASK-017 (`spec-drafter.json` 新增 eval id 3) 与母 TASK-035 (`phase-a-planner.json` +4 / `spec-drafter.json` +2) **都不把 `version.yaml` 列为 deliverable** ⇒ 按 ship 顺序 (字段 → 探针 → 母), 探针写进 `version.yaml` 的数字会被后 ship 的母 Spec **必然**写成陈旧。三份 Spec 无任何一条 seam rule 涉及此文件。**处方**: (a) 探针 TASK-003 的增量口径从「29→30 / 58→60」改为「按实测重算 (`ls *.json | wc -l` 与逐文件 `len(evals)` 求和)」, 消除同任务内 29 vs 31 的自相矛盾; (b) 字段 TASK-017 与母 TASK-035 各补 `ab-suite/version.yaml` 为 deliverable 并各自重算; (c) 三份 metadata 各加一条 seam rule: 「任何改 `ab-suite/*.json` 的任务同批改 `version.yaml`」。若 owner 判此属既有欠账 (#150) 则至少落 (c) |
| `35dad35d` | major | testing | `aria-plugin-benchmarks/ab-suite/spec-drafter.json` | issue | **同一 JSON 被三处任务写, 其中两处在同一 Spec 内无依赖边并行, 跨 Spec 无 eval id 分配约定。** 证据: 字段 TASK-016 (`deps=[TASK-014, TASK-015]`, deliverable 含该文件, 「eval id 2 expectations 同批更新」) 与字段 TASK-017 (`deps=[TASK-014, TASK-015]`, 同 deliverable, 「新增 eval id 3」) —— **两者互不依赖**, 是并行分支上的同文件写 (违反 memory `workflow-file-domain`「同文件串行」)。母 TASK-035 (deliverable 同文件, 「spec-drafter.json 增 (a)(b) 两 eval」) 未指定 id, 其 verification 只写「不修改既有 eval 1/2 文本」——**没提 eval 3** (字段 ship 在前, 落地时该文件已有 3 条)。实测当前 `spec-drafter.json` 的 `evals` = id 1 (`level-judgment`) / id 2 (`bilingual-support`), `selected_count: 2`。另: 字段 TASK-016 标题与母 TASK-032 标题都写「**2 evals**」, 而字段自己的 TASK-017 落地后即为 3 条 —— 母 TASK-032 的 「2 evals」口径在其执行时点已陈旧 (其 verification 虽提到「若已随字段 Spec ship 则用其新版套件」, 但计数未同步)。**处方**: (a) 字段给 TASK-017 加 `dependencies: [TASK-016]` (同文件串行); (b) 母 TASK-035 verification 补一条「新 eval id 从当时套件 `max(id)+1` 起分配, 不与字段 Spec 的 id 3 冲突」并把「不修改既有 eval 1/2」扩为「不修改任何既有 eval」; (c) 母 TASK-032 标题的「2 evals」改为「当时套件全部 eval」; (d) 母 metadata `external_dependencies[linked-issue-field-availability].seam_rules` 补一条覆盖 `ab-suite/spec-drafter.json` (现有两条只覆盖 `spec-drafter/SKILL.md`) |
| `05b5c605` | major | implementation | `openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml` | risk | **TASK-018 的接缝 verification 在母 Spec 自己声明为合法的分支下不可求值, 且无 fallback。** 证据: TASK-018 verification 第 3 条逐字「新块与字段 Spec 的 hunk A (字段必填声明) / hunk B (:127-162 Level 2 预览围栏) **不相邻**: 三者之间各隔 ≥1 个既有标题」; 而同一 yaml 的 `external_dependencies[linked-issue-field-availability].blocking: false` + `ship_order_note` 逐字「对本 Spec **非阻塞**…字段缺席时主体退化为零输入」明确允许「字段 Spec 未 ship」这一分支 —— 该分支下 hunk A/B 根本不存在, 断言无对象可求值 (既非真也非假, 属恒真式)。对照: 字段 TASK-014 对**同一条**接缝写了显式两分支 ——「若母 Spec 分支已存在: `git merge-tree` 干跑核验两 hunk 无冲突; **不存在则在 PR 说明记「未核验, 母 Spec 落地时复核」**」, 且 `tasks.md:161` 明写「不能预先断言零冲突」。母侧 `metadata.seam_rules` 第 2 条却把它写成既成事实:「两 Spec 的 spec-drafter hunk 物理不相邻, **任意顺序 merge 无冲突**」——**一侧断言, 另一侧说这断言做不了** (memory `split-makes-seams` / `delegate-verify`)。**处方**: 母 TASK-018 补对称的两分支处置 (字段 hunk 存在 ⇒ 断言不相邻 + `git merge-tree` 干跑; 不存在 ⇒ 记「未核验」并在字段 ship 后补核), 并把 `seam_rules` 第 2 条从断言式改为义务式 (「落地时须以 merge-tree 核验」) |
| `96ecdeb4` | major | architecture | `openspec/changes/linked-issue-field-availability/detailed-tasks.yaml` | risk | **SOT placeholder `{<org>/<repo>#<n>}` 的「同批改」义务只写在消费侧, 生产侧全文零提及。** 证据: 探针 proposal §3 与 yaml TASK-011 verification 逐字「`_RAW_KEY_BLACKLIST` = `{'{<org>/<repo>#<n>}'}` ∪ 哨兵集合 … 模块顶部注释写明『与姊妹 Spec §2 哨兵集合 + §3 模板 placeholder **同源, 任一改动须同批改另一侧**』」。而该串的**两个写入宿主都在字段 Spec**: TASK-013 (`standards/openspec/templates/proposal-minimal.md` 插入行) 与 TASK-015 (`spec-drafter/SKILL.md` 预览骨架 `:140` 后)。实测: 字段 `detailed-tasks.yaml` 与 `tasks.md` **全文 0 处**出现 `SC-19` 或 `_RAW_KEY_BLACKLIST` 或任何指向探针黑名单的同批改义务 (`grep -n "SC-19" ⇒ 无命中`)。⇒ 改 placeholder 的那只手看不见它会打断谁 —— 这正是「拆 Spec 自造接缝、任一侧执笔席都看不见」的形状。**额外放大因子**: placeholder 的 SOT 在 `standards` 子模块 (独立发布节奏, 实测无 VERSION/CHANGELOG/tag), 黑名单常量在 `aria` 子模块 (跨项目分发) —— 两者版本可独立漂移, 下游采用方的 standards 版本与 aria 版本不必同步。**处方**: 字段 TASK-013 与 TASK-015 各补一条 verification:「本串是 `sibling-spec-probe` SC-19 `_RAW_KEY_BLACKLIST` 的同源常量, 改动须同批改 `aria/skills/audit-engine/scripts/sibling_spec_probe.py`」; 并在字段 `metadata` 建 `exports_for_siblings.seam_rules` 收录 (当前该键下无 seam_rules) |
| `1246445b` | minor | implementation | `openspec/changes/sibling-spec-probe/detailed-tasks.yaml` | decision | **答复 `a2_discretions (i)` 上呈 post_planning 的复核请求, 并指出随之而来的字面冲突。** 复核结论: **A.2 的判断成立 —— 在同一代码块内追加第四个符号 `is_sentinel` 不违反 proposal §3 的约束**。依据 (逐字): §3 的约束句是「两条路径的插入与三条 import **只在这一个代码块里出现一次, 不得拆到两处各写各的**」, 约束对象是**位置唯一性** (禁第二处 `sys.path` 操作与第二份 import), 不是符号计数; 第四个符号来自**同一模块 `lib.linked_issue_field`**, 不新增路径、不新增 import 语句位置, 且它替代的恰是「自写第二份哨兵谓词」(§3 反复禁止的第二定义点)。**但字面须一处收口**: 探针 TASK-010 verification 逐字钉「紧接**三条** import … **三符号**不复制」, 与 `a2_discretions (i)` + TASK-001 (「可选导出核对 `is_sentinel`… 成功 ⇒ TASK-011 走 (i) 的 import 路径」) + TASK-011 (「优先 `is_sentinel(token_str)` (姊妹导出)」) 三处冲突; 且字段 yaml `exports_for_siblings.functions` 已把 `is_sentinel` 列为承诺导出、TASK-007 标题亦含它 ⇒ 该分支几乎必然成立。**处方**: TASK-010 verification 改为「三条 import 语句 (`lib.collision` / `lib.linked_issue_field` / `collectors.multi_remote`); 其中 `lib.linked_issue_field` 一条按 `a2_discretions (i)` 可为 `extract_linked_issue_field, is_sentinel` 两符号 —— 计数断言钉 `sys.path.insert` 出现次数 (== 1) 与 import 语句所在行块唯一, 不钉符号数」 |
| `970d3368` | minor | implementation | `openspec/changes/linked-issue-field-availability/detailed-tasks.yaml` | issue | **ship 号字面量被写进交付代码的 SKIP 文案, 与同 Spec 的「不锁字面量」自相冲突。** 证据: TASK-008 verification 逐字要求探针的 import 兜底打印 `'##SKIP## 归一 SOT 不可导入 (aria 侧 lib/collision.py 或 lib/linked_issue_field.py 缺失 / **版本 < v1.68.0**)'`; 而同 Spec TASK-021 verification 逐字「ship 号 = MINOR (v1.68.0) 除非 owner 改判 PATCH … **落地时以当时 plugin.json 计算, 不抄本文件字面量**」, `tasks.md:7` 亦写「本文件不锁字面量」。若 owner 改判 PATCH (→ v1.67.3) 或因 `3221f943` 的撞车而顺延号段, 该 SKIP 文案会**在已发布的代码里说谎**。**处方**: SKIP 文案去掉版本数字, 改为「(aria 侧 `lib/linked_issue_field.py` 缺失 — 需本 Spec 所在版本或更高)」, 或在落地时按实际号段回填并在 PR 点名 |
| `95f02272` | minor | documentation | `openspec/changes/linked-issue-field-availability/detailed-tasks.yaml` | issue | **`CLAUDE.md` 只出现在 verification, 不在 deliverables, 且不计入「12 点」口径。** 证据: TASK-024 标题「VERSION:24 + README.md 2 点 + i18n ×3 各 3 点」= 1+2+9 = **12**, deliverables 五个文件不含 `CLAUDE.md`; 但同任务 verification 末条逐字「CLAUDE.md 项目状态「版本:」行同步 (只改版本号, 不加术语)」, TASK-021 亦有同款一句。实测 `CLAUDE.md` 承载插件版本的点有 **2 处** (`:139` `v1.52.0–v1.67.2 已 ship` / `:141` `插件 aria-plugin v1.67.2`), 12+2 = **14** —— 与发布先例 (主仓 `086ee32` commit message 逐字「14 版本字符串点 (CLAUDE.md:139/:141, VERSION:24, README.md:8/:242, i18n ×3 各 badge/Plugin Version/translated-from)」) 恰好吻合。⚠️ 这两点**无机械兜底**: `.aria/probes/main-project-version-consistency.py` 的 `CLAUDE.md` 条目正则是 `主项目 v(\d+\.\d+\.\d+)` (:42), 只管主项目版本, **不覆盖插件版本**; 漏改是静默的。**处方**: TASK-024 deliverables 补 `CLAUDE.md`, 标题口径 12 → 14 (照 `086ee32` 先例)。探针 TASK-018 已把 `CLAUDE.md` 列进 deliverables, 三份对齐即可 |
| `af9f0c47` | minor | documentation | `openspec/changes/sibling-spec-probe/detailed-tasks.yaml` | issue | **`interface_expected` 对 `token_elements` 提了一个字段 Spec 没在该字段上承诺的义务。** 证据: 探针 `metadata.external_dependencies[…].interface_expected.token_elements` 逐字「姊妹 E4 按 ASCII ',' split + 各段 strip 后的列表; **BAD_TOKEN 时须能点名坏元素**」; 而字段侧把「点名」放在 **additive 字段 `bad_elements`** (字段 yaml `:47` 与 `tasks.md:141` 逐字「`FieldVerdict` 在 proposal 钉的 4 字段外追加 additive 字段 `bad_elements`… 否则 `BAD_TOKEN`『点名那个元素』要么在探针里重跑一遍 E5 循环, 要么无处输出」), 且探针自己在下一行声明「**探针只消费 proposal 钉的四个字段名**」(不含 `bad_elements`)。⇒ 两句在同一段落里互相取消: 既要求 `token_elements` 能点名, 又声明不消费点名字段。实际不构成实现障碍 (探针在 TASK-011 里对每个元素自跑 `normalize_linked_issue` 即可分辨), 但作为**接缝契约**它表述了一个不存在的义务。**处方**: 改为「`token_elements` = 全部元素 (含不可解析者); 坏元素的**点名**由字段 Spec 的 additive 字段 `bad_elements` 承担, 本探针不消费它 —— 层 1 的原串键由本探针自行对每元素跑归一得出」 |

---

## 实测记录

全部命令在 `/home/dev/Aria` 主仓根 (HEAD `c120f9e` 工作树, `aria` @ `d69091d`, `standards` @ `334c609`) 亲跑。

**1. 三份 yaml 机械体检 (全部通过)**

```
python3 (yaml.safe_load ×3 + 依赖闭包 + DFS 环检测)
=== linked-issue-field-availability tasks= 25 meta total= 25  dup ids: []  dangling deps: []  cycles: []
=== sibling-spec-probe              tasks= 18 meta total= 18  dup ids: []  dangling deps: []  cycles: []
=== a1-entry-claim-duplicate-work-guard tasks= 39 meta total= 39  dup ids: []  dangling deps: []  cycles: []
```

**2. 母 Spec TASK-001 (Phase B.1 前置) 逐条亲跑 — 全部为真**

```
git -C aria log --oneline -5      ⇒ d69091d (Merge fix/phase1-gate-no-push) · 7bd5dc1 (release v1.67.2)  ✓
grep -n no_push .../phase1_gate.py ⇒ :35 docstring · :362 形参 · :554 · :848 (+:82/:121/:228/:842/:887)  ✓
git -C aria ls-remote origin master ⇒ d69091dfdeb0c6cd83b03da2492812d33cec3712
git -C aria ls-remote github master ⇒ d69091dfdeb0c6cd83b03da2492812d33cec3712        (两 remote 一致 ✓)
git submodule status aria           ⇒ d69091dfdeb0c6cd83b03da2492812d33cec3712 (v1.67.2)  ✓
git -C aria show origin/master:.../test_coordination_no_push.py | grep -c 'def test_' ⇒ 16  ✓ (Spec 称 16)
release_gate.py: no_push 形参 :92 ✓ / --no-push :255-264 ✓ ; failure_handlers.py no_push_requested_by_env :95 ✓
```

**3. 发布同步面 — bump 后两条 custom check 的取值模拟 (支撑 `a257ffa4` / `73809784`)**

```
plugin.json now = 1.67.2
  if plugin==1.67.2: i18n stale=[]                                   badge=1.67.2 badge_match=True
  if plugin==1.69.0: i18n stale=[('README.zh.md','1.67.2'),
                                 ('README.ja.md','1.67.2'),
                                 ('README.ko.md','1.67.2')]          badge=1.67.2 badge_match=False
```
逻辑逐字取自 `.aria/state-checks.yaml:148-173` (`i18n-readme-translation-currency`, `stale ⇒ sys.exit(1)`) 与 `:94-98` (`m6-version-badge-match`, `DRIFT ⇒ exit 1`)。文件名清单实测:
```
ls README*  ⇒ README.ja.md  README.ko.md  README.md  README.zh.md      (无 README.zh-CN.md)
CLAUDE.md:139 / :141 承载插件版本 v1.67.2 ; VERSION:24 ; README.md:8 badge / :242 Plugin Version
i18n ×3 各 3 点 (:3 translated-from / :10 badge / :244 Plugin Version)  ⇒ 合计 14 点 (= 086ee32 先例)
.aria/probes/main-project-version-consistency.py POINTS: CLAUDE.md 条目正则 = `主项目 v(...)` (:42)
   ⇒ CLAUDE.md 的**插件**版本两点无机械兜底
```

**4. `.gitmodules` / gitlink (支撑 `73809784`)**

```
cat .gitmodules            ⇒ 三组 [submodule] 仅 path/url, 无任何 SHA
git ls-files -s aria standards ⇒ 160000 d69091d… aria / 160000 334c609… standards   (gitlink 在 index)
```

**5. AB 套件面 (支撑 `6698004d` / `35dad35d`)**

```
ls ab-suite/*.json | wc -l ⇒ 31        逐文件 sum(len(evals)) ⇒ 73
ab-suite/version.yaml      ⇒ version 1.1.0 / skills_covered 29 / total_eval_cases 58   (已漂 2 / 15)
spec-drafter.json          ⇒ selected_count 2, evals = [id 1 level-judgment, id 2 bilingual-support]
探针 tasks.md:33 «29→30, 58→60»  vs  探针 TASK-003 verification «ls *.json|wc -l == 32»  (同任务内矛盾)
字段 TASK-016 / TASK-017 : deps 同为 [TASK-014, TASK-015], deliverable 同为 spec-drafter.json (无串行边)
```

**6. 跨 Spec 语义接缝 — 逐字对照, 未发现矛盾 (无 finding, 存证)**

- `normalize_linked_issue` 实跑 (`aria/skills/state-scanner/lib/collision.py:178`):
  `'10CG/Aria#174'→('aria',174)` · `'10CG/a#1'→('a',1)` · `'none'→None` · `'无'→None` · `'N/A'→None` · `'{<org>/<repo>#<n>}'→None` · `'[b](url)'→None`
  ⇒ 母 TASK-002 的 `--emit-arg` 期望 (stdout 逐字节 `10CG/Aria#174`) 与字段 E5/E6 一致; SC-19 黑名单要挡的 placeholder 确实落 `BAD_TOKEN` 且原串键会相等 ✓
- 母 proposal 唯一 depth-1 字段行 = `:13` (`grep -nE '^> \*\*(Linked Issue|关联 Issue)\*\*:'` ⇒ 母 1 行 / 探针 1 行 (`:6` `none`) / 字段 3 行 (`:6` `none`, `:97` 语料引文, `:118` 模板样例) —— E0 谓词 3「文档序第一条」使字段 Spec 自身仍判 `OK`+哨兵 ✓, 与字段 proposal `:472/:474` 的自陈一致
- 哨兵吃 E3 原串: 字段 proposal `:199` (E5) 逐字「判定对象是 E3 未加工的 token 串本身」+ `:542` SC-4(f) `` `none ` `` ⇒ `BAD_TOKEN`; 探针 TASK-001 verification 逐字「对 `> **Linked Issue**: \`none \`` 得 `token_str == 'none '` 且 `verdict == BAD_TOKEN`」⇒ **两侧一致** ✓
- `line_no` 1-based: 字段 proposal `:241` 只给 `FieldVerdict(verdict, token_str, token_elements, line_no)` 未定基; 字段 A.2 补钉 (`yaml:47` / TASK-007 verification「E0 谓词 3: … line_no 1-based」); 探针 `interface_expected.line_no` **明写**「姊妹 proposal 未成文… 以实物核对 (TASK-001)」⇒ 缺口已被双侧记名 + 有落地核验任务, 不再是盲缝 ✓
- 跨 skill import: 探针 `_SS_ROOT = parents[2]/"state-scanner"` —— 对 `aria/skills/audit-engine/scripts/sibling_spec_probe.py` 求值 ⇒ `aria/skills/state-scanner` ✓ (与先例 `session-closer/scripts/handoff_autofill.py:403-407` 同形); 同名包双方今天都在: `state-scanner/lib/` (含 `collision.py`) 与 `state-scanner/scripts/lib/` (含 `runtime_probe.py`) ⇒ 插入顺序 `(_SS_SCRIPTS, _SS_ROOT)` 使 root 排最前, 与 memory `ss-two-lib-pkgs` 一致 ✓; 探针 TASK-004 配了反序负控 ✓
- 母 Spec 引用的 aria 锚点逐一实读: `linked_issue_overlaps` `:230-234` ✓ · `if not own_linked_issue:` `:265` / `return []` `:266` ✓ · `STALE_TTL: int = 1800` `:36` ✓ · `spec-drafter/SKILL.md:10 allowed-tools: Read, Write, Glob, Grep, AskUserQuestion` ✓ (母 TASK-018 目标串 = 其 + `, Bash` ✓) · `phase-a-planner/SKILL.md:9 allowed-tools: Read, Write, Glob, Grep, Task, Skill` ✓ (母 TASK-017 目标串 = 其 + `, Bash, AskUserQuestion` ✓) · `A.1 - Spec 管理:` `:63` / `skill: spec-drafter` `:64` / `Level1` `:67` ✓
- 字段 Spec 引用的锚点: `spec-drafter/SKILL.md` 438 行 ✓ · `### Level 2 预览` 围栏内头部两行 `:139-140` ✓ · `## tasks.md 格式要求` `:336` ✓ · `## 相关文档` `:424` / proposal-minimal 链接 `:429` ✓ · `standards/openspec/templates/proposal-minimal.md` 头部 `:3` Level / `:4` Status / `:5` Created (故 TASK-013 插在 `:5` 后 ⇒ 新头部 `:3-6`, 与 TASK-015「与 SOT :3-6 一致」自洽) ✓ · 该模板 `grep -c "Linked Issue"` = **0** (baseline 必红成立) ✓ · `## Template Usage Notes` `:40` ✓
- `.aria/state-checks.yaml` 现有 `grep -c '^  - name:'` = **12** ⇒ 字段 TASK-011 的「== 13」增量断言成立 ✓
- 母 Spec 的 advisory 措辞已清账: `tasks.md:33` 逐字「**advisory, 不阻塞**」, `:190` 记录「阻塞」来自主控指令误写已撤回; `phase_b_preconditions` P2/P3 均为 advisory ⇒ **无残留「阻塞」** ✓
- ship 顺序 ↔ 依赖链: 字段无外部前置 (可先 ship) ✓ · 探针 `phase_b1_preconditions` + TASK-001 对字段模块 **fail-closed** (「缺席 ⇒ 本 Spec 不进 B.2, 且不得在 audit-engine 内写任何 E0–E6 替身」) ✓, 与 owner O-4 (i) 硬前置一致 ✓ · 母 Spec 对两子 Spec 非阻塞且**不消费**探针输出 (与探针 §1 依赖方向第 1/2 条互指一致) ✓
- Agent ↔ deliverables 域: 抽查两处「代码文件挂 knowledge-manager / qa-engineer」均已在 verification 里显式钉为**零改动或注释-only** (母 TASK-009 `release_gate.py` ⇒「`git diff --stat` 为空」; 母 TASK-020 `constants.py` ⇒「`git diff` 只含注释行」) ⇒ 不构成域错配 ✓

---

## Verdict

**FAIL** (≥1 critical)。critical 2 / major 6 / minor 4。

两条 critical 同属一个类 (「发布同步面的 deliverables 与其自身 check 断言不自洽」), 三份 Spec 里字段 TASK-024 写对、探针 TASK-018 与母 TASK-038 写错 —— 建议按 memory `fix-the-class` 一次性以字段 TASK-024 的 14 点口径统一三份, 而不是逐条打补丁。

六条 major 全部落在**「三席各写各的、没人合起来看」的两个面** (发布/版本面 + AB 套件面) 与**两条单侧接缝** (`audit-engine/` 目录断言、placeholder 同批改义务)。**语义接缝面 (E0–E6 ↔ 四态分层 ↔ CLI 实参 ↔ 依赖方向) 已收敛, 建议 R2 不再复审该面**, 只审本报告点名的两个面 + 版本号裁定。

**给 owner 的决策项 (不代裁)**: 三份 Spec 是否合并为**一次** MINOR 发版? 现写法是三次串行 bump ⇒ 三轮完整发布同步面 (14 点 ×3) + 三次双推 + 三次 `ls-remote` 逐 remote 核验; 而三份改的是同一批 skill、同一批 AB 套件文件。合并一版可同时消解 `3221f943` (号段撞车)、`6698004d` (version.yaml 反复陈旧)、`35dad35d` (eval id 分配) 三条中的两条半。

## Vote

**REVISE**
