---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-07T00:54:19.424Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md
agents: [tech-lead]
---

# post_spec 单席审计报告 — tech-lead (Round 2)

被审对象: `/home/dev/Aria/openspec/changes/handoff-multibranch-subdir-path-fidelity/proposal.md` (v3, 271 行, Aria #195, Level 2)。本席为 Round 2 新席位, **不继承 R1 结论**, 全部事实逐条对 SOT 副本 (`~/.claude/plugins/cache/10CG-aria-plugin/aria/1.71.1/` = aria `origin/master` `301641b`) 与真仓 checkout 实读/实跑。

## 本轮实际核验面 (只审不改, 未触碰任何仓库文件)

- 全文读: proposal v3、R1 聚合报告、R1 rework 记录、决策单 `.aria/decisions/2026-09-07-handoff-multibranch-filename-semantics-and-pointer-guard.md`。
- 代码实读: `collectors/handoff_multibranch.py:1-50,174-182,230-345,420-470,575-710` · `collectors/handoff.py:260-340,370-500` · `writers/latest_md_writer.py:70-180,240-320` · `scripts/scan.py:118-300` · `renderers/track_board.py:180-192` · `collectors/_common.py:395-425` · `tests/test_p1_layer_h.py:225-320` · `references/state-snapshot-schema.md:1100-1145` · `references/json-diff-normalizer.md:236-246` · `references/phase-1-collectors.md:88-104` · `phase-d-closer/references/handoff-mechanics.md:4,102-136`。
- 实跑: `python3 -m unittest test_p1_layer_h` (真仓 `/home/dev/Aria/aria`, HEAD=`301641b`) → **24 tests OK**; 静态 `def test_` 计数 4 模块 = 78; ab-suite 四词逐词计数; 全仓 `write_latest_md` / `writers` 引用面 grep; `git rev-parse` / `ls-tree` / `ls-remote --tags` / 远端分支 ahead-behind。

---

## 审计结论

### Decisions

- [minor] architecture/主仓实况与 gitlink 起点: 实测 `git rev-parse HEAD origin/master` 均 `2c8eaa6` (proposal 头部记的 `ecb6296` 是 2026-09-06 快照, 已被本轨自身两个 commit `813e82c` / `2c8eaa6` 推进 — 属正常时效, 非错误); `git ls-tree origin/master aria` = `301641b` = `git -C aria rev-parse origin/master` ⇒ Task 5.2「从 `301641b` 前进, 严禁回退 `0545f86`」成立。远端最高 tag = `v1.71.1` ⇒ §待复议 6 的 `v1.71.2` 候选未被占用。两条 ahead>0 的 aria 远端分支 (`feat/69-exfil-coverage-corpus` ahead=1/behind=270, 末次 2026-05-30; `feature/secret-guard-per-segment-evaluation` ahead=8/behind=98, 末次 2026-08-16) 均为陈旧分支, **非同伴容器在飞轨**, 与本 spec 触点无竞用 (证据: `git -C aria log -1 --date=iso` / `rev-list --count`)
- [minor] implementation/F1 四处硬编码前缀: `grep -rn '"docs/handoff|docs/handoff/{' --include=*.py scripts/ lib/` 全命中集 = `collectors/handoff.py:34,254` (display 常量 `CANONICAL_DIR`) · `collectors/handoff_multibranch.py:178` · `writers/latest_md_writer.py:271` (docstring) · `scripts/scan.py:186` (唯一在 collector 之外用 `tracks[].filename` 拼 git 对象路径的消费方) ⇒ F1「第四处」成立, 无第五处。`collectors/handoff_worktrees.py:83,285` 复用 `handoff.py::_scan_md_files`, 不消费 `tracks[].filename` (证据: `handoff_worktrees.py:83,285`)
- [minor] testing/SC-10 基线与 fail-soft 六键: 静态 `def test_` 计数 `test_handoff_multibranch_collision_dedupe`=21 / `test_handoff`=27 / `test_handoff_worktrees`=25 / `test_track_board_advisories`=5, 合计 **78**, 与 SC-10 (含分模块拆分) 逐项相符; `handoff_multibranch.py:588-595` 早退 dict 逐字为 `{exists, tracks, branches_scanned, legacy_count, collision, errors}` 且 `state-snapshot-schema.md:1136` 同六键 ⇒ §4「恒存在必须把错误路径一起改」与 Task 2.4 / SC-14 的前提成立 (证据: `handoff_multibranch.py:588-595`, `state-snapshot-schema.md:1136`)
- [minor] architecture/A′ 核心取舍本身成立, 不需推翻: `filename` 保持 basename + additive `relpath` + 四个 git 路径消费方改读 `relpath`, 与 issue-195 正文第 41 行 / triage `:53` 的原案一致, 且 `_dedupe_sort_key:428-455` 第 3 级仍吃 basename ⇒ tie-break 面确实不受影响 (证据: `handoff_multibranch.py:455`)。本席全部 critical/major 均落在 **§2.5 守卫这一 v3 增量** 与 **裁定后未清理的 A 分支残留** 上, 骨架无须重做

### Issues

- [critical] architecture/§2.5 pointer 写侧守卫落在无生产调用点的模块: `write_latest_md` 在全插件的**非测试**引用面为空 —— `grep -rn "from writers|import writers|writers\." --include=*.py .` (排除 `tests/`) 零命中, 全仓提及仅 `tests/test_p1_layer_h.py` / `scripts/writers/__init__.py` / 两份 reference 文档。这是刻意设计: `references/phase-1-collectors.md:95` 「`latest_md_writer` 是 **deliberately D.3-scoped** —— 不在 scan.py 内自动触发, **不在 P1 内引入 production call-site**」, `:104` 「phase-d-closer D.3 集成实施由 TASK-029 或独立 follow-up task 承担」(至今未落地), `references/layer-l-integration.md:107` 同。**D.3 真实的 pointer 写入面是 AI 按处方指令手写**: `phase-d-closer/references/handoff-mechanics.md:114-124` 的「子步骤 2 (conditional): Pointer 行 (`**Latest**:` 字段) 更新」3 行决策表, 且 `:4` 声明该文档是 phase-d-closer 与 session-closer **共享的 handoff-write 机制 SOT**; 两个 closer 目录下 `grep "latest_md_writer|write_latest_md"` 零命中。后果三层: (1) Impact.Risk 第 2 条「缓解: 已裁定 A′ 并配 §2.5 写侧守卫 (使这类指针压根不写出)」在生产路径上为假 —— 守卫保护的是一条生产不执行的函数 (memory `feedback_completion_signals_vs_runtime_invocation`); (2) R1 critical `63d1ce08` 本身的生产可达性从未被核实, 而 v3 据它设了 Phase B 前置门 (Task 2.0)、由 AI 代裁并开了决策单 —— 决策单全文亦无一句涉及可达性; (3) 若要真修生产面, 落点是 `handoff-mechanics.md` 的处方决策表 = **运行时指令面** ⇒ Rule #6 须照跑 AB, 而 rule6_note 的免跑论据只 grep 了 state-scanner `SKILL.md` 里的 `tracks_multibranch`, 从未审视 phase-d-closer / session-closer 指令面 (证据: `references/phase-1-collectors.md:95,104`; `phase-d-closer/references/handoff-mechanics.md:4,114-124`; proposal.md:130 Impact.Risk 行 / :123-134 §2.5 / :241-247 rule6_note)
- [major] testing/SC-15 子目录布局未定义导致 (e) 恒绿、(f) 不可满足、反事实为假: SC-15 的子目录布局只写「唯一 active track 的文件在 `archive/`」, 未规定顶层是否仍留 `.md`, 而两种夹具下断言含义相反。归档-only (= R1 tech-lead 变体 A 的形态): `handoff.py::_scan_md_files:300,318,323` 非递归且过滤 `latest.md` ⇒ `canonical_files` 为空 ⇒ `collect_handoff` 在 `:438-451` 早返回 `exists: False`, **`_resolve_latest` (`:455`) 根本不执行** ⇒ `handoff_pointer_target_missing` (`:397-404`) 结构上不可能产生, 与守卫有没有实现无关 ⇒ (e) **恒绿**, 其写明的反事实「去掉 §2.5 守卫 ⇒ (e) 因 `handoff_pointer_target_missing` 出现而红」**为假**; 同时 (f)「`handoff.exists` 与 `tracks_multibranch.exists` 不互相矛盾」在该布局下**改后仍然为假** (False vs True — 正是 R1 指出的「零 soft_error 自相矛盾」, 守卫压根不碰它), SC 永远不能转绿。只有混合布局 (顶层留旧件) 下 (e) 才有鉴别力、(f) 才成立。另: (f) 未给出任何可执行谓词, 「不互相矛盾」由实施者自定 ⇒ 不可证伪。rule6_note 已把 SC-15 计入 baseline-failing 实体的第十条, 该计数随之失准 (证据: `collectors/handoff.py:300,318,323,438-451,455,397-404`; proposal.md:239 SC-15 / :246 rule6_note)
- [major] implementation/守卫判据在 `relpath` 缺失时语义未定义, 会打红一个不在 SC-10 范围内的既有测试: §2.5 表与 Task 2.5、决策单 `:59` 只写「仅当 `relpath == filename` 才写真指针」「判据必须是数据事实 `relpath != filename`」, **未规定 `relpath` 键不存在时的行为**。既有 `tests/test_p1_layer_h.py:230-240` 的 `_active_track()` 构造的 track dict 无 `relpath` 键; 字面实现下 `None == "2026-05-20-my-spec.md"` 为假 ⇒ 走 `_render_pointer_unavailable` (`latest_md_writer.py:151-169`, 只渲染 track_id 不含 filename) ⇒ `test_b1_single_track_pointer_action` 的 `:270` `assertIn("2026-05-20-my-spec.md", content)` 必红 (而 `:264` 的 `action=="pointer"` 与 `:269` 的 `**Latest**:` 仍绿, 因 `write_latest_md:302-304` 的 action 只看 `n_active`、降级文案 `:162` 也含 `**Latest**:` —— 假象更难归因)。该模块**现为基线绿**: 真仓 checkout 实跑 `Ran 24 tests … OK`。而 SC-10 点名的 4 个模块 (78 tests) **不含 `test_p1_layer_h.py`** —— 它恰是唯一覆盖 `write_latest_md` 的模块, 也正是 §2.5 改动的落点。语义面同样未裁: 缺 `relpath` 的快照 (旧版本产出, 或落盘后被后续 D.3 读) 在严判据下整体丢 pointer, 在宽判据下守卫对老快照恒不生效, 两种后果不同 (证据: `tests/test_p1_layer_h.py:230-240,264,269-270`; `writers/latest_md_writer.py:151-169,302-304`; proposal.md:127-131 §2.5 / :201 Task 2.5 / :232 SC-10)
- [major] architecture/A′ 裁定后未清理 A 分支残留, Task 4.1 会把一条正确文档改错: A′ 下 `tracks[].filename` 恒为 basename (§候选表 A′ 行 + 决策单 `:15`), 于是 (a) **SC-7 / Task 3.2** 要求构造 `filename` 为 `archive/2026-07-19-x.md` 的行 —— 该取值在 A′ 的真实输出里**结构上不会出现**, SC-7 退化成对手搓 dict 的行为记录, 而它自称覆盖的 Impact.Risk 第 1 条本文已标「(仅 A 案)」; (b) **Task 4.1 无条件列出「`:1125` tie-break 论据订正」**, 但实读 `state-snapshot-schema.md:1125` 原文「Handoff filenames are `YYYY-MM-DD-...`-prefixed, so the lexicographically greater name is also the later-authored one among same-day files」在 A′ 下 **仍然为真** (filename 仍是日期前缀 basename), 照 Task 4.1 执行等于把一条正确不变量改成错的; §6 第 1 条自己写的条件是「在 **A 案**的相对路径下直接变假」, 条件已不成立, 但 Task 与 §待复议 4 仍是无条件措辞。属 memory `feedback_spec_rework_leaves_downstream_ac_drift` 形态 (证据: `state-snapshot-schema.md:1125`; `handoff_multibranch.py:455`; proposal.md:82 候选表 A′ 行 / :163 §6 第 1 条 / :207 Task 3.2 / :210 Task 4.1 / :225 SC-7 / :259 待复议 4)
- [major] testing/Rule #6 判定的机械证据现已为假 — ab-suite 对 `tracks_multibranch` 命中 1 次: 头部 Rule #6 行与 rule6_note「套件覆盖实测」均称 `ab-suite/state-scanner.json` 对 `handoff_multibranch` / `tracks_multibranch` / `legacy` / `basename` **四词零命中**。逐词实测 (文件 17551 B, `git log -1` 显示自 `5697477` 2026-09-05 起未变, `git show 813e82c:` 同为 17551 B): `handoff_multibranch` 0 / `tracks_multibranch` **1** / `legacy` 0 / `basename` 0。命中处 = eval id 13 `a1-heartbeat-on-entry-TARGETED` 的问题 (C)「本次扫描的 `tracks_multibranch.collision.kind` 是空的 —— 这会改变 (A) 的答案吗?」。R1 聚合报告记的「15518 B / 命中全 0」(4 席一致) 与当前文件不符, v3 原样继承 (memory `feedback_spec_inherits_upstream_dec_errors`)。substitute 结论本身仍站得住 —— 该命中句问的是 heartbeat 触发条件, 本 spec 不改 `collision.kind` (假 legacy 行 `owner_container` 恒 `unknown`, `lib/collision.py:480-486` 本就排除) —— 但按 audit-points 横切「数据可用性」条款, 机械可核的规模断言与实测不符必须载重 REVISE, 不能只记一笔 (证据: `aria-plugin-benchmarks/ab-suite/state-scanner.json` 逐词计数; proposal.md:12 头部 Rule #6 行 / :244 rule6_note 第 2 条)
- [minor] documentation/Impact 首行与 SC-12 在「子目录仓能否 exit 0」上互相矛盾: Impact 第 1 条 Positive 仍写「不能承诺不再恒 exit 10 …… 该承诺的最终范围由待复议 2 的裁决决定」, 而待复议 2 已在 v3 裁定 (A′ + 守卫) 且 SC-12 已改成「断言 exit 0」。裁定后未回头同步该行, 实施者拿到两条相反指示 (证据: proposal.md:184 Impact 首行 / :237 SC-12)
- [minor] testing/SC-1 与 SC-8 仍保留 A / A′ 双分支断言取值: SC-1「`filename` 断言随裁决取值 (A: `"archive/…"` / A′: `filename == basename` 且 `relpath == …`)」与 SC-8 后半同形。§候选表下的裁定注写「保留双分支供复议对照, 实施以 A′ 为准」—— 对 §Why / §5 的**记述面**成立, 但**验收判据**保留二义会让实施者可挑低约束那支, SC 应单值化到 A′ (证据: proposal.md:221 SC-1 / :227 SC-8 / :91 裁定注)

### Risks

- [minor] architecture/A′ 引入的第二个字段契约本身需要被钉: 决策单 `:54` 自认「多一个输出字段 `relpath`, 消费方需要知道『拼 git 路径用 `relpath`, 展示用 `filename`』, 否则就是本 spec 自己制造的第二个契约错配」。当前 SC 里只有 SC-1 / SC-8 顺带断言两字段取值, **没有一条 SC 钉住「平铺仓 `relpath == filename` 恒成立」这一不变量本身** —— 而决策单 `:58` 把它列为 Phase B 落地约束。SC-2 的冻结语料比对不覆盖新键 (基线里没有 `relpath`)。建议补一条最小断言 (证据: `.aria/decisions/2026-09-07-…md:54,58`; proposal.md:222 SC-2)

---

## Verdict

**FAIL** — Critical **1** / Major **4** / Minor **2** (另 4 条 decision + 1 条 risk 按 R1 同规则不计入缺陷 severity 表)。

rationale:

- **Critical 落在 v3 唯一的新增设计上, 而非骨架**。A′ 的核心 (filename 保持 basename + additive `relpath` + 四个 git 路径消费方改读) 经实读成立, 与 issue/triage 原案一致, 不需推翻。但 §2.5 写侧守卫 —— 它是 R1 唯一 critical 的处置、是 Phase B 前置门的裁定内容、是 AI 代裁并开决策单请 owner 追认的那件事 —— 加在一个**全仓无生产调用点**的函数上, 而该「无调用点」是 `phase-1-collectors.md:95` 白纸黑字的既有设计决定; 生产 D.3 的 pointer 由 AI 按 `handoff-mechanics.md:114-124` 的处方决策表手写, 两个 closer 目录对 writer 零引用。于是 proposal 写进 Impact.Risk 的缓解承诺「使这类指针压根不写出」在生产上为假, SC-15 也只能在自己调 writer 的夹具里验证它。这不是措辞问题: 它决定 Task 2.5 该不该做、决定 owner 追认时看到的代价估算对不对、也决定「真要修生产面就得动处方指令面 ⇒ Rule #6 照跑 AB」这条判定该不该改判。
- **4 条 Major 分两类, 均可在 Phase A 内改 spec 消解**: (1) 验收判据面 —— SC-15 的子目录夹具未定义使两条断言分别恒绿/恒红且写错了反事实, 守卫判据在 `relpath` 缺失时未定义且会打红一个 SC-10 未纳入的基线绿测试模块; (2) 裁定后残留面 —— SC-7 / Task 3.2 钉一个 A′ 下不可能出现的取值, Task 4.1 要求「订正」一条 A′ 下仍为真的 schema 论据 (照做即引入文档错误), rule6_note 的四词零命中在今天的 ab-suite 上已为假。
- **本席未复现任何 R1 已处置项的回归**: R1 的两条 critical 与 15 条 major 中, 本席独立复核了基线 78 (静态计数一致)、fail-soft 六键形状、F1 符号与四处前缀、`:1125` 原文、`:177/:178` 注释错配、`_run` 编码、`handoff.py` 扁平三点 (`:288` / `:300,318` / `:389`)、gitlink 与 tag —— 均已在正文落地且落地正确, 无「加批注不改正文」的情况。新增的 critical/major 全部是 v3 增量或裁定后的下游漂移。

---

## 轮次记录

### Round 2: tech-lead

- Agents: `[tech-lead]` (本报告为单席; post_spec 团队 5 席由 `.aria/config.json` `teams.post_spec` 定义, 实读确认 `audit.checkpoints.post_spec = convergence`, `max_rounds = 5`, 与 proposal.md:14「审计计划」逐项一致 ⇒ Rule #10 白名单第一类, 无 AI 自行豁免)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: **10** 条 (Decisions 4 / Issues 7 中含 Critical 1 + Major 4 + Minor 2 / Risks 1)
- Vote: **REVISE**
