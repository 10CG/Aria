---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: "2026-08-22T13:17:10.559Z"
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 1
minor_count: 6
---

# post_planning R1 — A4 code-reviewer (文档任务与 §5 同步表逐行对照 / 引用准确 / yaml 自洽)

## 摘要

审计对象 `detailed-tasks.yaml` (17 任务 / 49h / 8 parent) 对 proposal v7 的派生在本席透镜下**基本忠实**: §5 同步表 20 行逐行都落在某 task 的 title/deliverables; §6 三条 Phase D 待办 (§6.1 前半「A.1 批准后评论」已于 2026-08-22T12:40Z 实发 #152, 后半 + §6.2 在 TASK-016, §6.3 在 TASK-012); §7 四条 checklist 落点与 `checklist_s7_mapping` 一致; TASK-015 版本引用点 (aria 5 文件 / 主仓 14 点 + gitlink) 与 proposal L226 逐字同且**全部实核到行** (当前值 1.66.4, 行号 CLAUDE.md:139/:141 · VERSION:24 · README.md:8/:242 · i18n ×3 各 :3/:10/:244); yaml 内部计数 (total_tasks 17 / estimated_hours 49 / parent 8 / exec_order 0..16 唯一递增) 与 `carries_sc ↔ sc_coverage_crosscheck` 双向一致; 对 v1.66.4 无陈旧引用 (baseline_sha 9e6a17c / target 1.66.5)。

唯一 Major 是**条件 scope 组的文档面没被标记**: proposal §3.5 的 `dispatch_viable=false` 删除清单含三个文档/发版条目 (2.3 表 dispatch 渲染句 · 3.3 (a) 行 · Impact/CHANGELOG 不提), 它们的承载 task 是无条件的 TASK-011 / TASK-015, 而 INV-3 又明写「其余任务无条件」⇒ false 分支下 knowledge-manager 会按 title 把 (a) 行与 dispatch 渲染句照写进 SKILL.md, 文档与代码分叉且 SC-14 抓不到。其余为 Minor。

## Findings

### [A4-PP-M1] 条件 scope 组的文档面/发版面未标记 — INV-3「其余任务无条件」与 proposal §3.5 删除清单不一致 (coverage / transcription)

- **锚点**: yaml `invariants[INV-3]` (L28-30) · TASK-011 title (L259 「处方段」「:276-290 schema」) · TASK-015 title (L338 CHANGELOG) · `dependencies` of TASK-011 (L263) / TASK-013 (L306)
- **问题**: proposal §3.5 (L198) 的 false 删除清单 = `§4 整段 + SC-8 + SC-9 dispatchable 部分 + DISPATCH_VIABLE + 2.3 表的 dispatch 渲染句 + SC-2 dispatch 子项 + SC-5 (c2) + 3.3 (a) 行 + §2.1 .replace; Impact/CHANGELOG 相应不提`。INV-3.rule 转录时**漏掉** `2.3 表的 dispatch 渲染句` 与 `Impact/CHANGELOG 不提` 两项; 且 INV-3.encoded_as 写「TASK-007.conditional_on …; 其余任务无条件」。但清单里 `3.3 (a) 行` (→ §C.2.4 处方段, TASK-011) · `2.3 表 dispatch 渲染句` (→ SKILL.md :276-290 message 封闭表, TASK-011) · `CHANGELOG 不提` (→ TASK-015) 都落在**无条件**任务, 任务本体零条件标记。TASK-006 对 `.replace` 有 `notes_scope` 处理 (做得对), 文档面却没有对称处理 —— 同一形状漏了兄弟位置。
- **实测**: `grep -n "dispatch\|条件\|viable" detailed-tasks.yaml` — 条件措辞只出现在 TASK-001/003/005/006/007 与 INV-3; TASK-010/011/012/015 零命中。SC-14 机检项 (枚举行 / :172-183 / DEC / :36 / 模板) 不含「message 封闭表无 dispatch 行」断言 ⇒ false 分支下 doc-code 分叉无机械发红。
- **后果**: 实施者分叉 (Major 判据): knowledge-manager 读 TASK-011 title 「处方段」会把 proposal 3.3 的 (a) 行原样写进 SKILL.md; 同时 TASK-011 `dependencies: [TASK-006, TASK-007]` 在 TASK-007 `status: skipped` 时语义未定 (skipped 视为满足? yaml 未写), TASK-013 同。
- **建议**: (1) INV-3.rule 补齐 proposal 两项; encoded_as 改为「TASK-007 整任务条件 + TASK-011 两处 / TASK-015 一处**条件内容** (逐条点名)」; (2) TASK-011 加 `notes_scope: "dispatch_viable=false ⇒ §C.2.4 处方段不写 (a) 行; :276-290 封闭表 trigger-matched 档不写 dispatch 渲染句; SKILL.md :183 path_coverage 字段列表不加 dispatchable_workflows"`; TASK-015 加 「false ⇒ CHANGELOG/Impact 不提 dispatch」; (3) TASK-011 verification 加一条 false 分支守卫: `grep -c dispatches SKILL.md == 0`; (4) yaml 顶部或 INV-3 写明「依赖列表中 status=skipped 的 task 视为已满足」。

### [A4-PP-m1] v1.66.4 在 origin / github 两远端**均无 tag** — TASK-015「tag」步骤须含补打 (fresh)

- **锚点**: TASK-015 title (L338 「+ tag + 双推」)
- **实测**: `git -C aria tag -l 'v1.66.*'` → v1.66.0 / v1.66.2 / v1.66.3; `git ls-remote --tags origin|github` 同 (三仓一致, 非本地未 fetch); `git submodule status aria` = `v1.66.3-15-g9e6a17c`。v1.66.4 五文件同步面与 master 双推 (9e6a17c 两远端同) 已完成, 唯独 tag 缺。
- **规范**: `standards/conventions/version-management.md §4.3` 按需锚点型: 「自 v1.66.0 起恢复打 tag … tag 缺失不阻断发布, **补打即可**」。
- **建议**: TASK-015 deliverables 加「补打 `v1.66.4` @ 9e6a17c + `v1.66.5` 两 tag, 逐 remote `ls-remote --tags` 核验 tag 对象 SHA (§4.3 步骤 3)」; 或若 owner 裁 v1.66.4 由对方容器补, 在 notes 留痕。预先存在, 但 TASK-015 执行时必撞。

### [A4-PP-m2] TASK-011 verification 断言 TASK-010 的产物, 但 dependencies 不含 TASK-010; SC-14 「机检脚本」无 deliverable 路径 (ordering / executability)

- **锚点**: TASK-011 verification L273 「…config.template 两 key」 vs `dependencies: [TASK-006, TASK-007]` (L263); title L259 「SC-14 机检脚本/断言」
- **问题**: 模板两 key 由 TASK-010 (helper 轨文档) 写入; 两 task 文件域 disjoint 可并行, 仅 exec_order 10<11 偶然保证顺序。SC-14 若以脚本形式交付 (proposal 称「文档机检」, 基线须红), yaml 未给路径 (tests/ 下的 test 文件? .aria/probes/?), 实施者自选。
- **建议**: TASK-011 deps 加 TASK-010 (或把「模板两 key」断言移到 TASK-010 verification, TASK-010 已 carries `SC-14 (部分)`); SC-14 机检明确落点 (建议 `aria/skills/phase-c-integrator/tests/test_docs_sc14.py`, 与 SC-12 全量一起跑), 否则「基线红」不可复现。

### [A4-PP-m3] traps §六 三写者 + 「TASK-0a 结果行」在 TASK-001 与 TASK-011 重复点名; :241 计数更新早于 TASK-014 追加行 (fresh)

- **锚点**: TASK-001 deliverables L78 · TASK-011 title L259 「TASK-0a 结果行」· TASK-014 deliverables L326 · TASK-011 title 「:241 计数」
- **问题**: §六 由 TASK-001 (exec 1) 首建并写 dispatch_viable 行 → TASK-011 (exec 11) 写 F3/F4/(b)/F6 并再次点名「TASK-0a 结果行」→ TASK-014 (exec 14) 追加 SC-13 证据行。(a) 同一行两 task 都声称产出, 前缀式追加重放会双重插入 (memory `subagent_asked_for_diff_will_apply_it`); (b) SKILL.md :241 「7 条坑」计数在 TASK-011 改, 但 TASK-014 之后再加一行 —— SC-13 证据算「坑」还是 dispatch 行下的证据字段, yaml 未定, 计数可能终态错一。
- **建议**: TASK-011 改为「保留 TASK-001 已写的 dispatch_viable 行 (不重写), 补齐其余四条」; TASK-014 verification 加「:241 计数与 §六 终态条目数复核」; 或明写 SC-13 证据作为 dispatch 行的子字段 (不计新坑)。

### [A4-PP-m4] TASK-011 「直调不可达声明」改变了 proposal 字段级含义; TASK-010 引用的处方段在 TASK-011 才写 (transcription / ordering)

- **锚点**: TASK-011 title L259 「直调不可达声明」; TASK-010 verification L253 「§C.2.4 处方段被 2.5 引用」
- **问题**: proposal §3.3 末段 (L190) 原文 = 「交互式直调 §C.2.4 (无 workflow-runner) 时**无计数**, 读者自行按 message 与上方处方处置」—— 直调**可达**, 缺的是观测计数/prompt 触发。「直调不可达」字面上是反义, 实施者可能写成「不支持直调」。另 TASK-010 (exec 10) 让 workflow-runner 2.5 引用 §C.2.4 处方段, 该段由 TASK-011 (exec 11) 产出, 中间一步悬空引用 (两 task 同 agent 且顺序执行, 风险低)。
- **建议**: 改为「直调无计数声明」; TASK-010 notes 注明「2.5 引用的处方段锚点由 TASK-011 落, 同批提交」。

### [A4-PP-m5] yaml 自洽两处小项: metadata 无 `dispatch_viable` 占位; TASK-002 deliverable 对 :363 位置的条件句已可判定 (fresh)

- **锚点**: TASK-001 verification L82 「写进本文件 metadata.dispatch_viable 字段」 vs `metadata:` (L1-12) 无该键; TASK-002 deliverables L99 「test_ci_backends.py (若 :363 所在类在此)」
- **实测**: `grep -n "normalize_pr_ci_status(\[\])" aria/skills/phase-c-integrator/tests/*.py` → 仅 `test_pre_merge_gate.py:363`; `test_ci_backends.py` 存在但不含该断言。
- **建议**: metadata 加 `dispatch_viable: null  # TASK-001 回填, null = 未跑` (fail-if-placeholder 可机检, memory `ad_slot_backfill_checkpoint`); TASK-002 deliverables 删 test_ci_backends.py 条件句 (或改为「不动」)。

### [A4-PP-m6] `dispatchable_workflows` 字段的文档面无 task 承载 (coverage, 条件)

- **锚点**: proposal Impact L255 「`path_coverage` +`dispatchable_workflows`」; SKILL.md :183 `path_coverage: {decision, workflows_scanned, matched_workflows, changed_files_count, reason}` (实核); §5 表 row 2 (:172-183) 只写「加零 run / not_found / gate_error」
- **问题**: dispatch_viable=true 时 path_coverage 输出多一个字段, SKILL.md :183 / :276-290 schema 与 `references/` 里的 path_coverage 描述应同步, proposal §5 未点名、yaml TASK-007/TASK-011 均未列 (proposal 层既有缺口, A.2 派生未补)。
- **建议**: 并入 M1 的 TASK-011 条件 notes: 「true ⇒ :183 与 schema 的 path_coverage 字段列表加 `dispatchable_workflows`; false ⇒ 不加」。

## 已核验无误

- **§5 表 20 行 → task 落点** (逐行): rows 1-6 (phase-c SKILL.md 六处) → TASK-011 ✓; row 7 (pre_merge_gate.py :181-194/:253-256 docstring) → TASK-003 ✓; row 8 (aether.py :218) → TASK-003 ✓; row 9 (path_coverage.py :36, 实核「共 9 个」在 :36) → TASK-011 ✓ (无条件, 与 SC-14 一致; proposal 把它写在条件删除的 §4 内是 proposal 自身措辞问题, yaml 取 SC-14 口径正确); row 10 (traps §六) → TASK-001/011/014 (见 m3); rows 11-14 (workflow-runner SKILL 7 处 / schema 3 处 / config-loader + 模板 / .gitignore :19-21) → TASK-010 ✓ (七处行号 :249/:264/:313/:326/:332-336/:338-358/:345/:389 与 schema :38-52/:110-131/:125 逐一实核命中; .gitignore :19-21 = 三条 coordination telemetry 行 ✓; 模板 :73-91 = pre_merge_gate 块且确缺两 key ✓; config-loader :283 = path_coverage_enabled ✓); row 15 (gate_state_helper :2-18 docstring, 实核 L7-10 自陈 markdown-driven) → TASK-009 ✓; row 16 (runtime-probe-declaration :135-139 「未来第一个真实声明者」预言句, 实核) → TASK-011 ✓; row 17 (pre_merge_gate.py 注释 :278-288/:305-319/:404-408 + :548-552 help) → TASK-006 ✓; row 18 (DEC-20260731-001, 文件名实核存在) → TASK-011 ✓; row 19 (版本引用点) → TASK-015 ✓; row 20 (AB 套件: catalog + NEG-4 + ab-results) → TASK-012 ✓ (NEG-3 元键集实核恰 8 键且与 proposal 列举逐字同; fixtures 目录 7 个与 rule6_note「7 fixtures」同; `eval-4-c24-gate-branchname` 先例实核存在于 2026-08-16 ab-results)。
- **TASK-015 版本点逐字对照**: aria 侧 plugin.json:4 / marketplace.json:3+:16 / VERSION / CHANGELOG:5 / README 全为 1.66.4; 主仓 14 点 = CLAUDE.md:139+:141 (2) + VERSION:24 (1) + README.md:8+:242 (2) + {zh,ja,ko}:3/:10/:244 (9) ✓ 行号全部实核命中; CLAUDE.md:5 为主项目版本不动 ✓; `m6-claude-md-version` check 实核只验顶层 2.0.0, proposal「:139/:141 无 custom check 兜底」属实 ✓; custom checks 实核 10 条 (state-checks.yaml), TASK-015「10/10」与四个点名 check 名全部存在 ✓; `C.2.4.5` Submodule Pointer Regression Gate 实核 SKILL.md:185 ✓。
- **§6 / §7**: §6.1 前半已实发 (#152 唯一评论 2026-08-22T12:40:15Z, 含裁定 + spec 入口), 后半 → TASK-016 ✓; §6.2 → TASK-016, 实核 aria-plugin open issues 无既有 (b) 腿 issue (不重复立案) ✓; §6.3 → TASK-012, #127 实核 open ✓。§7 1→TASK-007 verification / 2→TASK-012 title+notes / 3→TASK-014 notes / 4→TASK-008 title+notes, 与 `checklist_s7_mapping` 一致 ✓。
- **yaml 自洽**: total_tasks 17 = TASK-000..016 ✓; estimated_hours 0.5+1.5+3+4+2+3+3+4+4+5+3+4+4+1+3+2+2 = 49 ✓; parent P0-P7 = 8 ✓; exec_order 0..16 唯一递增且每条 dependencies 的 exec_order 均小于自身 ✓; `carries_sc` 16 条 SC 与 `sc_coverage_crosscheck` 双向一致 (含 SC-14 (部分) / SC-16 (a)(b)(c) 拆分) ✓; 既有测试数 119 (phase-c) / 22 (gate_state_helper) 实核 `pytest --co` 同 ✓; `:363` 翻转目标实核在 test_pre_merge_gate.py ✓; baseline_sha 9e6a17c = aria HEAD = origin = github master ✓; 无任何 1.66.3 / 1.66.4 陈旧目标引用 ✓。
- **INV-5 在 TASK-010 verification 有可证伪断言** (文本零处自动 dispatch/commit) ✓; agent 分配 (TASK-010/011 knowledge-manager, TASK-012/014/015/016 main-loop) 符合 A.3 口径 ✓。

## Verdict

**PASS_WITH_WARNINGS** — vote **REVISE** (1 Major: 条件 scope 文档面未标记, 修法为 INV-3 补两项 + TASK-011/015 各加条件 notes + skipped 依赖语义一句, 改动 <15 行; 6 Minor 可同批吸收)。
