---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: "2026-08-22T14:17:45.391Z"
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 1
minor_count: 4
---

# post_planning R3 — A4 code-reviewer (R2 簇 #2/#4/#7 核对 + yaml 自洽 + v3 diff 新鲜眼睛)

## 摘要

实读 proposal.md v7 全文 + detailed-tasks.yaml v3 全文; 脚本机械核 (`scratchpad/check_yaml.py`): total_tasks 19 ✓ / estimated_hours 49.5 = 逐任务求和 ✓ / parent 8 ✓ / exec_order 0..18 唯一且每条 dependencies 的 exec_order 均小于自身 ✓ / 无悬空依赖 ✓ / TASK-003 ∈ {005,006,007a,007b,010,011,012,013,014,015,016} 11 个闭包 (与 exec_order_note 逐字同) ✓ / 19 任务 reason 非空 ✓ / `carries_sc` ↔ `sc_coverage_crosscheck` 16 条双向一致 ✓ / `agent_summary` 四 agent ↔ tasks.agent 逐一相等 ✓ / 条件字段六处 (007a·007b `conditional_on`; 006·011·015·016 `conditional_parts`) ✓ / status 全 pending ✓ / parallel_tracks gate 轨 exec 3..9 ✓。代码锚点抽样 (aria @ 9e6a17c): `test_spec_complete.py:94-104` = `parents[4]` + `_require_meta_archive` skip 先例属实, 且 `aria/skills/phase-c-integrator/tests/<f>.py` 的 `parents[4]` 恰为 meta-root ✓; SKILL.md:241 「7 条坑」= traps §一~§三 编号 #1-#7 ✓; `config.template.json:73-91` 两 key 均缺 ✓; `DEFAULT_CONFIG :57-69` 无新 key ✓; `aether.py:225-226` ✓; `path_coverage.py:36` 「共 9 个」✓; `runtime-probe-declaration.md:135-139` 预言句 ✓; DEC-20260731-001 存在 ✓; `.gitignore:19-21` 三个 telemetry 分区 ✓; fixtures 目录含 NEG-3 ✓; pytest collect phase-c 119 / gate_state_helper 22 ✓; 两 remote tags 仍只有 v1.66.0/.2/.3 (v1.66.1 与 v1.66.4 均缺) ✓。

归我席三簇 (#2 A4-M1 闭包 / #4 A4-M2 false 分支 proposal 自删 / #7 A4-m1·m3 + #1 A4-m4 + #3 A4-m2) 在 v3 **6/6 closed** (证据见处置表)。新鲜眼睛抓到一条 Major: v3 为 INV-3 false 分支新加的**唯一机械负控** `grep -rn dispatches aria/skills/phase-c-integrator aria/skills/workflow-runner` 零命中 —— 在基线 9e6a17c 上就已命中 1 处 (`scripts/submodule-tripwire-audit.sh:6` 「5/5 dispatches」, 与本 spec 无关), 且 TASK-011 **无条件**要往同目录 traps §六 写 F6 行 (端点 `…/workflows/{file}/dispatches`) ⇒ 该负控在 false 分支**恒红**, 零信息量 (memory `false_green_dual_is_permanent_red`), 实施者必须临场改写或跳过 (分叉)。修法 1 行: 换量 (memory `redfix-change-quantity`), 见 M1。另 4 条 Minor。

## R2 处置核对

| 簇 | R2 条目 (本席) | v3 处置 (聚合表) | R3 实核 | 状态 |
|---|---|---|---|---|
| #2 | A4-PP2-M1 TASK-003 对 005/006/010/014 在依赖图不可达 | 005/006/010 加边 → 003; 014 加边 → 013; 断言 003 ∈ 11 闭包 | TASK-005 `[TASK-004, TASK-003]` (L183) ✓ · TASK-006 `[005, 003, 001]` (L201) ✓ · TASK-010 `[009, 003]` (L298) ✓ · TASK-014 `[009, 010, 011, 013]` (L387) ✓; 脚本算闭包: 003 ∈ 11 个下游 (005/006/007a/007b/010/011/012/013/014/015/016), 与 `exec_order_note` (L15) 逐字同; 我 R2 指的三处 verification (006 GREEN / 010 探针 / 014 活体) 现均在图上位于 003 之后 ✓; `execution_order` L477-479 与 deps 一致 (「005 需 003」「010 需 003」「014 需 013」) ✓ | **closed** |
| #4 | A4-PP2-M2 false 分支 proposal 自删 + Impact 零承载 | INV-3 rule 改写; TASK-016 `conditional_parts` + 依赖 001 | INV-3.rule (L36) 现含「proposal.md 自身在 TASK-016 归档前按 §3.5 删除对应文本 (…) — 归档件不得描述未实现能力」✓; TASK-016 `conditional_parts` (L434) 列 §4 / SC-8 / SC-9 dispatchable / SC-2 子项 / SC-5 (c2) / 2.3 渲染句 / 3.3 (a) / Impact 两项 / §7 checklist 1 N/A ✓, deps `[015, 001]` (L430) ✓。残: 清单少 §3.5 明列的「§2.1 末段 `.replace`」与 `DISPATCH_VIABLE` 常量各处提及 (见 m1, 因 conditional_parts 已写「按 proposal §3.5」为源, 执行者会回读 §3.5, 降 minor) | **closed** (minor 残) |
| #7 | A4-PP2-m1 SC-14 脚本无 deliverable / 需 parents[4]+skip 先例 | SC-14 脚本 deliverable 落 TASK-013 (qa 子 agent) + parents[4]+skip 先例 | TASK-013 deliverables (L373) `tests/test_doc_sync_no_run.py (SC-14 grep 断言; 主仓文件断言 parents[4]+skip 先例)` ✓; TASK-011 verification (L334) 「沿 test_spec_complete.py:94-104 parents[4]+skip 先例, standalone aria-plugin 下 skip 不红」✓; 先例行号实核属实 (L94 `parents[4]`, L98-106 `_require_meta_archive` skip) ✓; carries_sc/crosscheck 「SC-14 (脚本)」→ TASK-013 ✓。(agent 归属分叉由 A3-PP3-M1 报, 本席不重复) | **closed** |
| #7 | A4-PP2-m3 TASK-014 deliverables 缺 SKILL.md / :241 口径 | TASK-014 :241 口径 + deliverable | deliverables (L393) 「SKILL.md :241 终计数 (= §一~§五 7 条 + §六 坑条目数, 不含证据行)」✓ + (L392) 「口径: 证据行不计入」✓; notes (L398) 把 TASK-001 行也归「证据」⇒ §六 坑 = F3/F4/(b)/F6 四条, 终值可定 (= 11) ✓ | **closed** |
| #3 | A4-PP2-m2 aria 子模块分支无承载; 主仓分支写在 C | 新 TASK-000b 两仓分支 | TASK-000b (L73-90): aria `git -C aria checkout -b feature/152-no-run-for-branch` @ 9e6a17c (HEAD 实核 = 9e6a17c) + 主仓同名分支; verification 两仓 `--show-current` + aria HEAD 断言 ✓; 002/004/008/001 依赖 000b ✓; TASK-015 (ii) 改「在 TASK-000b 建的分支上」(L405) ✓; memory `feedback_detached_head_may_be_stale_rebase` 存在 ✓ | **closed** |
| #1 | A4-PP2-m4 exec_order tie-break 002 先于 004 | 全表重编 004=3 | 004 exec 3 < 002 exec 4, 且 002 deps 含 004 (机检边) ✓; 物理块在 P1 首位 ✓ | **closed** |

r2_closed = 6, r2_partial = 0, r2_not_addressed = 0。

## Findings

### [A4-code-reviewer-PP3-M1] INV-3 false 分支的唯一机械负控 (`grep -rn dispatches …` 零命中) 在基线就命中 1 处, 且 TASK-011 无条件写入的 F6 行必再命中 — 恒红检查零信息, 实施者必须临场改写或跳过 (fresh · executability)

- **锚点**: TASK-013 verification[2] (L377) 「条件组负控 (dispatch_viable=false 时): `grep -rn dispatches aria/skills/phase-c-integrator aria/skills/workflow-runner` 零命中」· INV-3.encoded_as (L37) 「TASK-013 对 false 分支做 grep 负控 (代码/文档零 'dispatches' 渲染)」· TASK-011 title/deliverables (L315, L326) traps §六 「F6 404+basename」(无条件) · proposal F6 (L51) 「`POST …/actions/workflows/{file}/dispatches` 路由存在」
- **实测** (aria @ 9e6a17c, 本 spec 零改动): `grep -rn dispatches skills/phase-c-integrator skills/workflow-runner` → **1 命中** `skills/phase-c-integrator/scripts/submodule-tripwire-audit.sh:6` (`# 5/5 dispatches: the Forgejo Actions runner cannot clone …`, v1.28.0 tripwire 注释, 与 #152 无关)。再者 TASK-011 要把 F6 (端点字面 `…/workflows/{file}/dispatches` 是 F6 的内容本身) 写进 `references/pre-merge-gate-empirical-traps.md §六`, 该写入**不在条件组内** (INV-3 清单没有 traps), 两分支都发生 ⇒ false 分支下 grep 至少 2 命中。
- **后果**: 这条负控是 v3 为 R2 簇 #7 (A1-m2 「条件组无 grep 负控」) 新造的, 也是 INV-3.encoded_as 里 false 分支**唯一**的机械守卫。恒红 = 假绿的对偶 (memory `false_green_dual_is_permanent_red`): 实施者跑到它时只能 (a) 判「基线本来就红, 跳过」(Rule #10 形状的自豁) 或 (b) 临场缩 grep 范围 / 换词 —— 两者都是 yaml 没写的裁量, 且 (b) 的选法因人而异 (排除哪些文件? 换 `dispatches -d`? 换 `DISPATCH_VIABLE`?) ⇒ 实施者必然分叉。同 memory `redfix-change-quantity`: 修恒红不能在同一个量上调阈值 (「≤1 命中」会把 F6 行也盖掉), 要换量。
- **建议** (1 行, 换量): 负控改为断言**本 spec 引入的 token** 在**渲染面**零命中: `grep -rn -E 'DISPATCH_VIABLE|dispatchable_workflows|/dispatches -d' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py aria/skills/phase-c-integrator/scripts/path_coverage.py aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py aria/skills/phase-c-integrator/tests/test_path_coverage.py aria/skills/phase-c-integrator/SKILL.md aria/skills/workflow-runner/SKILL.md aria/skills/workflow-runner/references/workflow-state-schema.md` = 0 (false 分支), 并注明「traps §六 F6 行的端点字面与 `submodule-tripwire-audit.sh:6` 基线命中不在此量内」; INV-3.encoded_as 同句改「零 `DISPATCH_VIABLE`/`dispatchable_workflows`/处方行」。true 分支对照可顺手加 `≥1` (`_no_run_gate_error` 渲染处), 使同一检查两分支都有判别力。

### [A4-code-reviewer-PP3-m1] TASK-016 `conditional_parts` 删除清单是 proposal §3.5 的真子集 (transcription)

- **锚点**: TASK-016 L434 vs proposal §3.5 L198 · Impact L255-256 · 代码落点 L31
- **实测**: §3.5 明列且 L434 未列的两项: (i) 「§2.1 末段的 `<pr_branch>` `.replace`」(proposal L93-95 三行 + L129 「由 gate_check 事后回填 (2.1 末段)」); (ii) 「`DISPATCH_VIABLE` 常量本身」— 「Impact 两项」只覆盖 Impact 的 `path_coverage +dispatchable_workflows` 与「新 artifact … `DISPATCH_VIABLE` 常量」, 但 Impact L255 还有内部签名 `_parse_workflow["dispatchable"]` / `_result(dispatchable_workflows=)` 两项, 代码落点 L31 与 Risks R-c 也提 `DISPATCH_VIABLE`。同形也出现在 INV-3.rule (L36) 的括号清单。
- **建议**: L434 改「按 proposal §3.5 **全清单**删除 (§4 / SC-8 / SC-9 dispatchable / SC-2 子项 / SC-5 (c2) / 2.3 渲染句 / 3.3 (a) / §2.1 末段 `.replace` 三行 / `DISPATCH_VIABLE` 与 `dispatchable*` 在 L31·Impact (4 处)·R-c 的提及), §7 checklist 1 标 N/A」。执行者既已被指向 §3.5, 不致漏做, 故 minor。

### [A4-code-reviewer-PP3-m2] TASK-001 / TASK-014 的 throwaway 分支生命周期未写「回到 feature 分支」, TASK-000b 的分支断言只在 000b 时刻成立 (executability)

- **锚点**: TASK-001 deliverables[0] (L105) 「aria-plugin throwaway 分支 … 删分支」· TASK-014 title (L383) 「throwaway 分支首推 … 再删分支」· TASK-000b verification (L89)
- **实测**: 两任务都在 aria 工作树上建/推/删 throwaway 分支, 但都没写分支从哪起、在哪 checkout、删后回到哪; TASK-001 (exec 2) 紧接在 000b 之后、TASK-004 (exec 3, 「在 9e6a17c 绿」) 之前 —— 若 throwaway 在 `aria/` 工作树内 checkout, 删分支前须先切走, 切到哪没写; 切错 (留在 throwaway 提交 / detached) 则后续 qa/be 子 agent 的改动与主控 commit 落在错误分支, 正是 000b notes 引的 memory 形状。
- **建议**: TASK-001/014 各加一句「throwaway 用 `git -C aria worktree add <tmp> -b <b> feature/152-no-run-for-branch` (或结束后 `git -C aria checkout feature/152-no-run-for-branch` + `git branch --show-current` 核), 不动主工作树」。

### [A4-code-reviewer-PP3-m3] v3 新增 `schema_note` 「estimated_hours 用 int」与文件自身 0.5/0.5/1.5 及总计 49.5 矛盾 (fresh)

- **锚点**: metadata.schema_note (L11) vs TASK-000/000b/001 `estimated_hours` (L60/L80/L99) 与 L8 `49.5`
- **实测**: 仓内无 validator 要求 int (`grep estimated_hours aria/skills/*/scripts/*.py` 零命中; task-planner DUAL_LAYER_SPEC.md:166 甚至写 string 区间), 故仅是自述失真。
- **建议**: schema_note 改「estimated_hours 用数值 (允许 .5)」, 或三任务取整并把总计改 51。

### [A4-code-reviewer-PP3-m4] TASK-015 v1.66.1 补 tag 目标留占位 `<plugin.json 首次 =1.66.1 的 commit>`, 现可钉 SHA (executability)

- **锚点**: TASK-015 title (L405)
- **实测**: `git -C aria log -S'"version": "1.66.1"' -- .claude-plugin/plugin.json | tail -1` → **`3b97c35`** (`chore(release): #128 v1.66.1 — secret-guard 逐段 fail-safe`), 且 `merge-base --is-ancestor 3b97c35 9e6a17c` 成立; 两 remote ls-remote 今日均无 v1.66.1 / v1.66.4 (只有 v1.66.0/.2/.3)。「首次 =1.66.1」有两种算法 (`-S` 首次引入 vs 按 VERSION 文件), 钉死可免实施者各查各的。
- **建议**: 改 「v1.66.1@3b97c35」。

## 补证 (不计数)

- **A2-PP3-M1** (`git show` 缺 `-C aria`): 从主仓根实跑 `git show 9e6a17c^:skills/phase-c-integrator/scripts/ci_backends/aether.py` → `fatal: invalid object name '9e6a17c^'` (子模块 SHA 不在主仓对象库); 同意修法 `git -C aria show …`。
- **A2-PP3-m1** (`grep -c 'return "pending"'` 命中 2): 实核 aether.py :226 (零 run 分支) 与 :238 (尾部兜底) 两处, 计数不定位分支 ✓。
- **A3-PP3-M1** (TASK-013 SC-14 脚本「qa 子 agent」vs `agent: main-loop`): 本席 R2 m1 要求的是 deliverable + 先例引用, 两者已落; agent 归属分叉由 A3 承载, 不重复计数。

## 已核验无误

- **依赖边四处** (005/006/010→003, 014→013) 与闭包断言: 见处置表 #2; 新边不成环, 不改任何 RED→GREEN 配对内序 (005 RED 仍先于 006 GREEN; 002 RED 先于 003 GREEN; 007a 先于 007b; 008 先于 009)。
- **TASK-000b**: 两仓分支 + HEAD==9e6a17c 断言 + 下游 001/002/004/008 依赖边 ✓。
- **INV-1 有向核验**落 TASK-013 (main-loop): 非破坏性 `git show` 思路正确 (cwd 与 grep 精度由 A2 报)。
- **:241 口径**: 「7 + §六 坑条目, 证据行不计」; 实核 7 = traps §一~§三 编号 #1-#7 (§四两条无编号 bullet、§五为形状叙述不在 7 内, 「§一~§五 7 条」措辞松但数字钉死); TASK-001 行按 TASK-014 notes 归证据 ⇒ 终值 11 可定。
- **SC-14 承载**: crosscheck `[010, 011, 013 (脚本)]` ↔ carries_sc 三任务 ✓; 断言面 (枚举行 not_found / :172-183 gate_error / DEC 前向指针+📌 / path_coverage.py:36=8 / config.template 两 key) 与 proposal SC-14 (L277) 逐项同 ✓; 主仓文件断言用 parents[4]+skip ✓。
- **v3 新引用**: R2 簇/席位引用 (A4-M1/A4-M2/A5-M1/A1-M2/A1-m7/A1-m8/A2-M2/A3-M2) 均对应聚合表 ✓; memory 两条 (`feedback_detached_head_may_be_stale_rebase`, `workflow-file-domain`) 存在 ✓; 行号引用 (aether :218/:225-226 · pre_merge_gate :57-69/:174-233/:302-352/:449/:508-527/:548-552 · path_coverage :36/:56 · SKILL.md :46-54/:172-183/:241/:248/:252-263/:276-290/:292-302 · workflow-runner SKILL :249-264/:313/:326/:332-336/:338-358/:345/:389 · schema :38-52/:110-131/:125 · config.template :73-91 · .gitignore :19-21 · runtime-probe-declaration :135-139 · test_spec_complete :94-104) 抽样 9 处全中 ✓; 版本点 (5 aria + 14 主仓) 与 proposal L226 口径同 ✓; 无 1.66.3/1.66.4 作为 target 的陈旧引用 (baseline 9e6a17c / target 1.66.5) ✓; 测试基数 119/22 ✓。
- **INV-3 条件组六处字段**与 §3.5 清单: 007a/b `conditional_on` ✓ · 006 `.replace` 仅条件 ✓ · 011 三文档项 ✓ · 015 CHANGELOG ✓ · 016 proposal 自删 ✓ (m1 残)。
- **INV-4/5/6/7**: 009 `--state-file` 必填 + 014 主仓绝对路径 ✓; 010/011 INV-5 grep ✓; 16 SC 全承载 + §7 四项映射落点实存 (007b verification / 012 title+notes / 014 notes / 008 notes) ✓; 012 「ab-results 含执行记录」✓。
- **parallel_tracks.note** 仍说「两轨文件域 disjoint」而 010→003 跨轨: 文件域陈述为真, 跨轨时序已在 `execution_order` L478 显式写明「010 需 003」, 不构成矛盾 (同 A2 判断)。
- **TASK-016 时窗** 14d 与 frontmatter `max_age_days: 14` 同 ✓; 归档门正交 warn 预告 ✓。

## Verdict

**PASS_WITH_WARNINGS** — vote **REVISE**。R2 归我席 6 条全部 closed, v3 机械自洽 (19/49.5/exec_order/闭包/crosscheck/agent_summary 全绿), 派生层对 spec 的转录无方向性/数字漂移。但 v3 为 INV-3 false 分支新造的唯一机械负控在基线即恒红 (M1, 1 行换量可修); 4 条 Minor 可同批吸收。修 M1 (+ A2-M1 的 `-C aria`, A3-M1 的 agent 归属) 后可进 B.1。
