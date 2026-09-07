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
timestamp: 2026-09-07T06:20:46.605Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [knowledge-manager]
---

# post_spec R4 单席报告 — knowledge-manager

被审对象: `/home/dev/Aria/openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (v5, 375 行 / 约 139 KB)。
席位透镜: 头部机械判据 · Rule #3 文档同步完整性 · 与 standards/conventions 及 CLAUDE.md 规则 (Rule #6 判据表选行 / Rule #10) 的冲突 · 术语与归档口径一致性 · 引用真实性。
本席为新席位, 不继承上轮结论; 所有行号一律以指定的 1.71.1 插件缓存副本 (= aria `origin/master` `301641b`) 实读为准。

## 审计结论

### Decisions

- [minor] documentation/R3 major 正文落地复核: 19 条 R3 major 的 finding id 在 proposal.md **全部命中** (`a7536535` 3 处 / `92565b30` 9 / `ebaad4a5` 6 / `b5a94a9c` 3 / `120e1171` 7 / `2af687f5` 2 / `3dd75e12` 4 / `b57e3209` 3 / `4608f5b2` 6 / `f658ae7e` 2 / `019ff413` 2 / `56845091` 3 / `17f270f5` 1 / `1ad9b4ed` 3 / `90e3b4b8` 1 / `7d909571` 3 / `db126eff` 5 / `e854a801` 2 / `334e62dc` 1); 抽样实读确认改动落在 §What / §5 / §6 / Tasks / SC 的**正文**而非批注 (证据: proposal.md:100-330 与 `.aria/audit-reports/post_spec-R3-…-aggregated.md:46-128`)
- [minor] documentation/头部机械判据与 Rule #10: `python3 aria/skills/state-scanner/scripts/linked_issue_field_probe.py . --grandfathered .aria/linked-issue-field-grandfathered.txt` 实跑 `OK (8 份在范围内, 6 条在册)`, 本 spec **不在**白名单 (`.aria/linked-issue-field-grandfathered.txt:17-22` 六条全是 M6/M7 轨); 头部 `> **Linked Issue**: \`10CG/Aria#195\`` 为单 code span、行首无空白、`>` 后恰一空格 (`cat -A` 核), 满足 `spec-drafter/SKILL.md:414-424` 写法三条; 字段序与 `standards/openspec/templates/proposal-minimal.md:3-6` 一致。审计计划行与 `.aria/config.json` `audit.checkpoints` 逐项吻合 (post_spec / post_planning = convergence, 其余 off), 8 条待复议全部上交 owner, 无 AI 自行豁免 (证据: `.aria/config.json` audit 段)
- [minor] documentation/引用真实性与载重事实独立复核: 10 个 `feedback_*` memory 文件全存在; 决策单 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md` 及两份 archive 先例 (`2026-09-06-owner-container-identity-key-and-collision-parser/` 三文件, 头部逐字含「owner 2026-09-05 裁定升 Level 3 (判据: cross-module 成立, aria + standards 两子模块)」; `2026-08-23-pre-merge-gate-no-run-for-branch/` 头部逐字 `Level: Minimal (Level 2 Spec)`) 均在; issue-195 第 21 行确点名 `_get_file_commit_date`、第 41 行 A 案原文逐字含「`filename` / `track_id` 等需要 basename 的字段另行派生」; triage `:25`「issue 未点名」与 `:53`「filename 字段另派生 basename」相符, `triage-report-195.json` = `confirmed`/`major`; schema `:1104/:1110/:1114/:1125/:1126/:1128/:1136/:46-48/:1070` 与 collector `:16-31/:35-44/:36/:42/:177-178/:246-247/:332/:494/:586-596/:619/:637-658/:748`、`scan.py:126/180-186/199-200/255/382-388`、`handoff.py:263-266/288/300-323/389/397-404/438-451/455`、`latest_md_writer.py:32/78-95/110-124/140/143/151-169/259/279/287-290/298-304`、`phase-1-collectors.md:95/102/104`、`layer-l-integration.md:101-107`、`session-handoff.md:97/171-173`、`advanced-rules.md:443-444/511-512/544/572-574`、`CHANGELOG.md:84/93-100` 逐处实读命中; Task 5.1 十六个版本点抽验 12 处行号全对 (均为 v1.71.1); `standards` `origin/master` = `21748d4` = 主仓 gitlink; `git -C aria diff --name-status 0545f86 301641b` = 29 (5 A + 24 M) 且五个触点文件 `--stat` 输出为空; ab-suite `state-scanner.json` 实为 17551 B、`tracks_multibranch` 命中 1 处 (`:214`, 题面写死 `collision.kind`), 另三词 0
- [minor] testing/SC-11(c) 新判据鉴别力实测: `grep -c 'Returns only the basename' handoff_multibranch.py` = **1** (有鉴别力), `grep -c 'path relative to'` = **0** (正向断言亦 baseline-failing), 旧判据 `'callers compose the full git-object path'` = **0** (确因跨 `:246`/`:247` 而恒绿) —— R3 `90e3b4b8` 的替换成立 (证据: handoff_multibranch.py:244-248)
- [minor] documentation/sibling probe: `openspec/changes/` 八个在制 spec 中, 引用 `Aria#195` 的只有本 spec, `grep -rln 'handoff_multibranch|latest_md_writer'` 同样只命中本 spec; 姊妹 spec `pre-merge-completeness-gate-change-scope` (Aria#199) 只引用 `standards/` 不改它, 无 standards gitlink 撞车 (证据: 全 `openspec/changes/` grep + 该 spec:288)

### Issues

- [major] documentation/`proposal.md §rule6_note` 第 1 条 (:334): 该条逐字写「变更本体仍全是 collector / scan 代码 + 输出 schema 文档。**无** `description` 变动, **无** SKILL.md / references 的文本变动」—— 后半与前半**同句自相矛盾** (「输出 schema 文档」就是 `references/state-snapshot-schema.md`), 且被 R3 rework 新增的任务进一步证伪: Task 4.1 (:264) 改 `references/state-snapshot-schema.md`; Task 2.5(e) (:260) 改 `references/phase-1-collectors.md:102`; Task 4.4 (:267) 改 `references/layer-l-integration.md:103`; Task 4.5 (:268) 视复核结果可能改 `references/rules/advanced-rules.md` 与 `RECOMMENDATION_RULES.md`。后者正是 Rule #6 SOT 明列的**处方性**类 (`standards/conventions/skill-benchmark-exemption.md:20`「`references/rules/*` 的 dispatch 表、判定规则 …… 与 SKILL.md 正文同性质」), 一旦 4.5 落编辑, 正确落行是判据表**第二行「处方性·运行时指令面 ⇒ 照跑 AB, 零裁量」**(`:29`), 而非现写的**第四行「拿不准 ⇒ 照跑」**(`:31`)。照跑这一处置结论不变 (两行同去处), 但 SOT §4 强制留痕的 rule6_note 载的是一条假前提, 后续复议 / 重跑 benchmark 会据它误判范围 (证据: proposal.md:334 / proposal.md:260,264,267,268 / standards/conventions/skill-benchmark-exemption.md:20,29,31)
- [major] documentation/`latest_md_writer` 两处函数 docstring 未入 Rule #3 同步清单 (§6.2 / Task 2.5 :260 / Task 4.2 :265): §2.5 守卫给 `_render_pointer` 增加第二个降级原因 (`target_in_subdir`), 但两处自述「唯一原因 = 缺 filename」的 docstring 既不在 §6 同步清单也无任何 SC —— `latest_md_writer.py:111-114` 逐字「Falls back to a "(pointer 不可用)" banner when the filename cannot be determined from the track dict (edge case: legacy track missing filename)」, `:152` 逐字「Fallback when single active track has no filename.」。清单现只列 `:32` / `:279` / `:287-290` (action 契约, R3 `92565b30`) 与 `:159` / `:164` (正文文案与硬编码原因, R3 `3dd75e12` / Task 2.5(c)(f))。落地后这两句在被改函数头上直接为假, 与 R3 判 major 的 `ebaad4a5` (`:332` `_make_legacy_track_id` 自身 docstring)、`b5a94a9c` (docstring 块归位) 同型; 本 spec 对同类漏改 (`:20` / `:177` / `:313`) 一律逐条点名, 唯独漏此两处 ⇒ 属缺口而非取舍 (证据: latest_md_writer.py:110-114,151-152 实读 / proposal.md:206,260,265)
- [minor] documentation/`proposal.md Task 1.2` (:254): 同一条目内计数自相矛盾 —— 前半列出五族并写「**这五族**对 `301641b` 全红」, 粗体警示却写「**⚠️「全红」只限定到上列四族**」, 而该警示自己的括注又写「(v4 原写「四族」也已随 SC-17 更新为五族)」。SC-17 由 R3 `17f270f5` 新增后遗漏的计数订正 (证据: proposal.md:254)
- [minor] documentation/行号引用 `:495-496` (proposal.md:117 / 206 / 257 / 265 / 305 五处): dedupe 透传论据句里的 `` legacy:<branch>:<filename> `` 字面实际落在 `handoff_multibranch.py:494`; `:495-496` 两行内容为「so two legacy rows can never share a dedupe key with each other or with a / real track, and every legacy row's `owner_container` is `"unknown"`」, **不含**该字面 (实读 488-500)。SC-11(i) 走 grep 不受影响, 但 Task 4.2 会把实施者指到错行 (证据: handoff_multibranch.py:493-499 / proposal.md:265)
- [minor] documentation/决策单勘正的复议入口不完整 (头部 `334e62dc` 块 :19): 该块称三处勘正「随本 spec 一并请 owner 追认 (§待复议 2 第 (5) 问)」, 但实读 §待复议 2 第 (5) 问只写「字段名 `rel_path` 追认」; 另两条**载重**勘正 —— (a) 守卫判据不得照决策单第 2 条写 `relpath != filename`; (b) SC-15 断言须换成顶层留非-active 件的夹具 —— 未在待复议清单出现。owner 只读复议清单即会漏签这两条 (证据: proposal.md:19 与 §待复议 2 第 (5) 问 / `.aria/decisions/2026-09-07-…-pointer-guard.md:56-61`)
- [minor] documentation/SC-11 机检未覆盖 R3 新增的两处 references 文档面 (SC-11 :305): Task 2.5(e) 要求同步 `references/phase-1-collectors.md:102` (实读逐字 `Return dict: {action: "pointer"|"banner"|"skipped", path: str, content_lines: int}`), Task 4.4 要求同步 `references/layer-l-integration.md:103`; 但 SC-11(h) 只点名 `standards/conventions/session-handoff.md`, 两者只有任务勾没判据。与 R2 `7cba5aa4` / R3 `cc313a28` 判「只靠尾句兜底不算判据」为同型缺口 (证据: proposal.md:260,267,305 / phase-1-collectors.md:102 / layer-l-integration.md:103)
- [minor] documentation/§6.1 Change history 口径陈述过强 (:200): 该条写「该表既有口径是**每次** schema 变更加一行」, 被最近一次同 collector 家族的 schema 变更证伪 —— v1.70.0 (2026-09-06) 往 schema 加了恒存在字段 `identity_advisories` (`state-snapshot-schema.md:1091`) 并改写 dedupe 键语义 (`:1120,:1122,:1128`), 而 `## Change history` 末行仍是 **2026-07-19** (`:1168`, 全文件即 1168 行)。要求本 spec 补一行本身正确 (SC-11(g) 可证伪), 但援引的「既有口径」不成立 (证据: state-snapshot-schema.md:1091,1156-1168 / proposal.md:200)

### Risks

- [minor] documentation/待复议积压与无人值守: 8 条待 owner 复议中, R3 已定 4 条「须 owner 或 R4 拍板后才进 Phase B」(`019ff413` Spec Level 2 vs 3 / `f658ae7e` 版本级别 PATCH vs MINOR / `334e62dc` 决策单勘正 / `56845091` 是否顺手补 `now=`)。Level 若升 3 需另补 `tasks.md` (A.2) + `detailed-tasks.yaml` (A.3) + post_planning; 版本级别定错会连坐 Task 5.1 的 16 个版本点、tag 与 CHANGELOG 标题。审计席无权代裁 (Rule #10), R4 之后仍须 owner 闭合才能进 B.1 (证据: proposal.md §待 owner 复议 7/6/2/8 与 R3 聚合报告 Verdict 段末句)

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **2** / Minor **5** (另 5 条 decision + 1 条 risk 不计入 severity)。

rationale: 按 `references/verdict-format.md` 的 `0 Critical + >=1 Major ⇒ PASS_WITH_WARNINGS`。方案骨架 (A′ = `filename` 保持 basename + additive `rel_path` + 四个 git 路径消费方改读 + git show 失败不再伪造 legacy + 写侧守卫) 从本席透镜复核成立, 无推翻主张。R3 的 19 条 major **全部落进正文**, 且抽样复核的机械替换 (SC-11(c) 的三条 grep 计数、`json-diff-normalizer.md:241` 属历史记述的定性、`legacy:<branch>:<filename>` 四处、CHANGELOG v1.70.0 三段先例、standards `:171-173`/`:97` 两态、`write_latest_md` 零生产调用点) 逐条经本席独立实读实跑确认为真, 未见回填矛盾以外的新事实错误。

两条 major 都是 **R3 落地动作自身的下游**, 不触碰设计骨架, 可在 Phase A 内改 spec 消解: 一条是 rule6_note 的前提句没随「Task 4.4 / 2.5(e) 新增 references 触点」同步 (Rule #6 留痕载假前提); 一条是守卫落点的两处函数 docstring 漏出 Rule #3 同步清单 (本 spec 对同类漏改一贯逐条点名, 唯此两处漏)。五条 minor 全属措辞 / 行号 / 交叉引用 / 判据覆盖面, 零方案风险。

`post_spec` 为 `blocking: false`, 本 verdict **不阻断**后续流程; 但按 Rule #10, 上述两条 major 与「须 owner 拍板的 4 条待复议」不得由实施者以「Level 低 / 代码面小 / session 已长」自行降格、跳过或改序。

## 轮次记录

### Round 4

- **Agents**: knowledge-manager (本席; 五席之一)
- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品
- **Conclusions**: 12 条 (Issues 7 = Major 2 / Minor 5; Decisions 5; Risks 1)
- **Vote**: REVISE
