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
timestamp: 2026-09-07T05:38:24.803Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [backend-architect]
---

# post_spec R4 — backend-architect 单席报告 (handoff-multibranch-subdir-path-fidelity)

**席位透镜**: 数据契约与实现可行性 —— 字段语义变更的向后兼容与消费方枚举 (自行 grep 核实)、错误路径穷举、伪代码与真代码结构对齐。

**本轮机械核验清单** (全部本席独立实跑, 不采信 proposal 自述):

1. 基线同一性: 五份 SOT 副本 (`handoff_multibranch.py` / `handoff.py` / `latest_md_writer.py` / `scan.py` / `state-snapshot-schema.md`) 与 `git -C aria show 301641b:` md5 **逐一相同**; `git -C aria diff --stat 0545f86 301641b -- <四个触点>` **输出为空**。
2. 消费方独立枚举: `grep -rln tracks_multibranch` 全插件树 24 文件, 与 §5 表逐条对照 (结果见 Issues 第 4 条)。
3. `_render_pointer` / `write_latest_md` 外部消费方枚举: 除 `writers/__init__.py` 再导出与 `test_p1_layer_h.py` 外**零命中** ⇒ 零生产调用点属实。
4. legacy 公式全树命中: `:36` / `:332` / `:494` / `schema:1104` 共 4 处 (SC-11(i) 判据成立, 行号见 Issues 第 5 条)。
5. SC-11(c) 三条 grep 基线实测: `'callers compose the full git-object path'` = 0 (跨行), `'Returns only the basename'` = 1, `'path relative to'` = 0 ⇒ R3 换掉的新判据确有鉴别力。
6. hermetic git 探针: `ls-tree -r --name-only -z` 输出原样 UTF-8 路径 + NUL 终止 (末段空串), pathspec `-- docs/handoff` **不匹配** `docs/handoff-archive/c.md` ⇒ 前缀守卫无「兄弟目录被误剥」面。
7. **反事实实跑 (本轮新增证据)**: 在 scratchpad 副本上按 Task 2.2(a) 实改 `scan.py:186`, 跑 `test_scan_integration.TestSnapshotSelfConsistencyAC5` → 基线 `Ran 11 … OK`, 改后 **`FAILED (failures=3)`**。
8. 版本面数据可用性: Task 5.1 的 16 处逐处 `sed -n` 命中 (README:8/242、三份 i18n :3/:10/:244、VERSION:24、CLAUDE.md:139/141、两处架构文档), `main-project-version-consistency.py:39-49` 的 POINTS 确实全是主项目 1.7.5 行 ⇒ 「10 处零机械兜底」属实。

---

## 审计结论

### Decisions

- [minor] architecture/基线冻结与行号可信度: 五份 SOT 副本与 aria `301641b` md5 逐一相同, 触点 diff 为空; 主仓 gitlink 实测 aria=`301641b` / standards=`21748d4`, 与头部载重断言一致 ⇒ 全文行号可信, 后续席位可直接引用 (证据: 本席 md5 对照 + `git ls-tree HEAD aria standards`; proposal.md:9-10)
- [minor] documentation/R3 十九条 major 的正文落地: 逐条对正文核验, 19 条**全部落在正文而非批注** (`a7536535` Task 2.1 两条实现路径 / `92565b30` §2.5 返回契约行 + Task 2.5(e) / `ebaad4a5` 四处公式 / `b5a94a9c` 两个 docstring 块分派 / `120e1171` 实体资格重定 / `2af687f5` standards 第三态限定 / `3dd75e12` 五处同义断言 / `b57e3209` scan.py 缺键口径 / `4608f5b2` 三处不变量条件化 / `f658ae7e` 待复议 6 / `019ff413` 待复议 7 / `56845091` SC-10 日历归因 / `17f270f5` SC-17 / `1ad9b4ed` 夹具 pin 日期 / `90e3b4b8` SC-11(c) 换判据 / `7d909571` 布局 2 机制句 / `db126eff` §6.3 撤回 / `e854a801` CHANGELOG 三段 / `334e62dc` 决策单勘正), 未见「改一处引入另一处矛盾」的回填 (证据: proposal.md:17-19,107,117,125,137,203-221,254-268,304-313)
- [minor] implementation/A′ 骨架与真代码及上游原文对得上: issue 第 41 行「`filename` / `track_id` 等需要 basename 的字段另行派生」与 triage `:53`「`filename` 字段另派生 basename」逐字支持 A′ (proposal 对 triage `:25`「issue 未点名 `_get_file_commit_date`」的勘正也属实 —— issue 第 21 行确已点名); 守卫挂点 `_render_pointer:116/121/143` 结构可容 `rel == filename` 判据; `-z` 与 pathspec 行为经 hermetic 实跑确认 (证据: issue-195.md:21,41; triage-comment-195.md:25,53; latest_md_writer.py:116,121,143)
- [minor] documentation/头部主仓 HEAD 快照已陈旧: 头部写主仓 `HEAD`/`origin/master` 均为 `ecb6296`, 实测现为 `e58ac22` (R3 席位测得 `f634d837`), 三轮三值; 但载重量 (gitlink 起点 `301641b`, 严禁回退 `0545f86`) 仍成立。建议把该句改成「起草时快照」措辞, 终止逐轮漂移 (证据: `git rev-parse HEAD` = e58ac22; proposal.md:10)

### Issues

- [major] testing/§3 缺键口径 · Task 2.2(a) · SC-10 — `scan.py:186`: 照 Task 2.2(a) 实改 (`rel_path = t.get("rel_path")` + `if not rel_path: continue`, 无 `or filename` 兜底), `test_scan_integration.TestSnapshotSelfConsistencyAC5` **三条当场转红** —— `test_contradiction_is_reported` / `test_unevaluable_track_is_recorded_not_swallowed` / `test_detection_uses_enforced_set_not_hardcoded_origin`, 根因是 `HEALTHY_TRACKS` 只有 `track_id`/`filename`/`branch` 三键、无 `rel_path`, 整行被早退跳过 ⇒ `errs` 由 1 变 0。这与 §3 自述「写 `.get()` 则照绿但测不出拼进命令行的是哪个字段」**直接矛盾** (照绿只在「不早退、把 `None` 拼进路径」这一被 Task 2.2(a) 禁止的写法下成立), 也与 SC-10 把该模块以「回归面身份…只保证不被打红」纳入点名集矛盾; 夹具补 `rel_path` 这一动作全文无任务承接。修法: Task 2.2 明写「同批给 `HEALTHY_TRACKS` 补 `rel_path`」(与 Task 2.1(ii) 改四处 mock 同型), 并把 §3 那句「照绿」删掉 (证据: 本席 scratchpad 副本实跑 基线 `Ran 11 … OK` → 改后 `FAILED (failures=3)`; tests/test_scan_integration.py:164-166,194-201,256-274,286-319; proposal.md:125,257,304)
- [major] testing/§7 · SC-16 · SC-13 — `rel_path` 恒存在 的第二构造点无覆盖: §7 与 §6.5 CHANGELOG 段都把 `rel_path` 声明为「每行 track 多一个键 / 恒存在」, 但 §4 删掉 git-show 失败行之后, TrackEntry 仍有**两个**构造点 —— frontmatter 分支 (`handoff_multibranch.py:665-676`) 与无 frontmatter 的 legacy 分支 (`:687-698`)。SC-1 / SC-8 后半只覆盖前者 (SC-8 的夹具是否带 frontmatter 未写死), SC-13 造了两份无 frontmatter 文件却只断言 `track_id` 与 `updated_at`, SC-16 是「`tracks[]` 每一行」的**全称谓词而夹具组成未钉死** ⇒ 夹具若只放带 frontmatter 的文件即**真空满足**。后果具体: legacy 行漏填 `rel_path` 时, 按 Task 2.2(a) 的无兜底早退, `scan.py` 的 AC-5 会**静默跳过全部 legacy 行** —— 正是本 spec 立案要修的 F1 无声失效, 只是换了人群。对照 SC-14 为 `unreadable_count` 的「恒存在」专设错误路径断言, 此处的不对称是缺口。修法: SC-16 夹具明写「至少一份带 frontmatter + 一份不带」, 或在 SC-13 追加 `rel_path` 断言 (证据: handoff_multibranch.py:665-676,687-698; proposal.md:227,302,308,311)
- [major] architecture/§2.5 裁定块 · Task 2.5(e) · SC-15 布局 1 与 3 — `degraded_reason` 与正文可不一致且无 SC 捕获: 守卫落在 `_render_pointer` (返回 `str`), 而 `degraded_reason` 要出现在 `write_latest_md` 的返回 dict (`:316-320`); 两者如何连接 (改 `_render_pointer` 的返回形状, 还是在 `write_latest_md` 里**重算**同一谓词) 全文未指定 —— 而本 spec 对同类选择 (Task 2.1 的 (i)/(ii)、Task 2.2 的缺键口径) 都坚持「选型后果不能对实施者不可见」。若实施者重算, 就出现第二处独立谓词, 与 §3 自己点名的「两处独立字面量靠巧合一致」同型; 而 SC-15 **只在布局 2 断言该键**, 布局 1 (a)(b)(c) 与布局 3 (g) 都不断言 `degraded_reason is None`, 三条反事实也无一针对它 ⇒ 「正文写真指针、机读键报 `target_in_subdir`」这种镜像谎言全绿通过, 正是 R3 `92565b30` 要根除的形态。修法: Task 2.5(e) 明写传播路径 (推荐 `_render_pointer` 返回 `(content, reason)`), 并给布局 1 / 3 各加一条 `degraded_reason is None` 断言 + 一条反事实 (证据: latest_md_writer.py:110-148,151-169,298-320; proposal.md:137,144,260,310,316,322,326)
- [minor] architecture/§5 消费方枚举 · Task 4.5 — 漏 `phase-d-closer/SKILL.md:218`: D.3 pointer 判定有两份成文面, §5 只登记了 `handoff-mechanics.md:116-121` 的三行决策表, 漏了 SKILL.md 里的摘要行「子步骤 2 Pointer 更新 (conditional by `snapshot.tracks_multibranch` multi-track detection)」。§5 自己对 `advanced-rules.md` 与 `RECOMMENDATION_RULES.md` 用的正是「同一判定的两份登记面, 须一并复核措辞」口径, 这里应同办 (Task 4.5 的复核清单也该含它)。注: 它不改变 Rule #6 的 AB 范围结论 (本 spec 不改其文本), rule6_note 说的「SKILL.md 三处」限于 state-scanner 的 SKILL.md, 该限定属实 (证据: phase-d-closer/SKILL.md:218; state-scanner/SKILL.md:117,149,153; proposal.md:185-186,268)
- [minor] documentation/§6.2 · Task 4.2 · SC-11(i) — dedupe 论据句行号偏移: legacy 公式的第三处被反复写作 `:495-496`, 实读该字面量落在 **`:494`** (`:495-496` 是后半句「so two legacy rows can never share a dedupe key with each other or with a real track」)。SC-11(i) 的 grep 判据不受影响 (全树 4 处命中, 改完合计为 0), 但按行号定位的实施者会打开错误的两行 (证据: handoff_multibranch.py:493-496; proposal.md:117,205,305)
- [minor] testing/Task 1.2 红测名单 与 rule6_note 十一实体不闭合: 同一 bullet 内「五族」与「⚠️『全红』只限定到上列**四族**」并存 (R3 加 SC-17 后的更新未清干净); 更实质的是, rule6_note 列的十一条 baseline-failing 实体中, **SC-6 / SC-9 / SC-14 / SC-16 与 SC-4 后半 / SC-8 后半**既不在「必须全红的五族」也不在「本就为绿的例外清单」, 其红态验收无人承接 —— 而 R3 `120e1171` 引入例外清单的初衷正是消除这类灰区 (证据: proposal.md:254,338)
- [minor] documentation/SC-11 未覆盖新增的 writer 契约面: SC-11 (a)-(j) 把 schema 字段表、fail-soft 形状、Change history、collector 两个 docstring 块、新 soft_error kind、standards 第三态全都上了 grep, 唯独 Task 2.5(e) 新增的四处 `action` 契约面 (`latest_md_writer.py:32` / `:279` / `:287-290` 与 `references/phase-1-collectors.md:102`) 没有机检判据 —— 恰是本轮新增的机读契约面, 只靠任务勾选兜底 (证据: latest_md_writer.py:32,279,287-290; phase-1-collectors.md:102; proposal.md:260,305)

### Risks

- [minor] architecture/待复议 7 (Level 2 vs 3) 的判据面比正文写的更宽: `LEVEL_GUIDE.md:156-162` 的跨模块条件是「满足任一」, 本 spec 命中的不止「影响多个子模块」—— 新增 `rel_path` / `unreadable_count` / `degraded_reason` 三个机读契约字段 + `write_latest_md` 返回形状变化同时命中「需要 API 契约变更」这一条。待复议 7 只援引前者, 建议把第二条判据一并列出交 owner, 免得「Task 4.4 判 deferred ⇒ 跨模块不成立 ⇒ 维持 Level 2」这条出路被误当成必然成立 (证据: spec-drafter/LEVEL_GUIDE.md:155-163; proposal.md:355,361)

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **3** / Minor **5** (另 4 条 decision 不计入)。

rationale: 本 spec 的事实底座经本席独立机械核验**全部成立** (基线冻结、行号、消费方零生产调用点、grep 判据鉴别力、`-z` 与 pathspec 行为、16 处版本点), R3 的 19 条 major 逐条落在正文而非批注, A′ 与 issue/triage 原文一致且骨架挂得上真代码 —— 无「方案错误」「破坏生产消费方」「SC 恒绿假绿」三类 critical。

3 条 major 全部落在**本轮新增/改写内容的下游**, 且都是可证伪的具体缺口而非风格意见: (1) `scan.py:186` 的处方与既有夹具冲突, 本席实跑取到 3 条转红, 且 spec 里同时写着一句与之矛盾的「照绿」断言; (2) `rel_path` 的「恒存在」在第二个构造点没有任何 SC 承接, 且承接它的 SC-16 是可真空满足的全称谓词 (本仓 memory `feedback_universal_predicate_vacuous_truth_on_empty_set` 同型); (3) 新增的机读键 `degraded_reason` 缺传播路径规定与负向断言, 可与正文不一致而全绿。三条都不需要推翻设计, 修法均为「明写一句 + 加一条断言」。

按 `verdict-format.md`「0 Critical + >=1 Major ⇒ PASS_WITH_WARNINGS」判定; post_spec 非阻塞, 不阻断后续流程, 但本席 **vote = REVISE** (Major > 0)。

---

## 轮次记录

### Round 4

- **Agents**: backend-architect (本席; 五席之一, 新席位, 不继承上轮结论)
- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品
- **Conclusions 数**: 12 (Issues 7 / Risks 1 / Decisions 4) —— 其中 Major 3, Minor 5, Decision 4
- **Vote**: REVISE

**与 R3 的关系**: 本席 7 条 issue 与 R3 的 19 major + 7 minor **交集 0**。3 条 major 均落在 R3 rework 引入的新面上 —— `b57e3209` 定的 scan.py 缺键口径 (本席实跑证伪其配套的「照绿」断言)、`92565b30` 定的 `degraded_reason` 加键支 (缺传播路径与负向断言)、以及 A′ 全程未被任何轮次覆盖的 legacy 行 `rel_path`。R3 的 19 条 major 本席逐条复核确认落在正文, 未重开。

**未越界声明**: 本轮只审不改, 未编辑 proposal 或任何仓库文件; 全部实跑在 scratchpad 副本 (`scratchpad/probe/`, `scratchpad/gitprobe/`) 内完成, 未触碰 `.aria/config.json`、`refs/aria/coordination` 或 aria / standards 子模块工作区。
