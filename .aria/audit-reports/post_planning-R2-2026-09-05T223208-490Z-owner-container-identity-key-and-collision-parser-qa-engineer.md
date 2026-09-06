---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T22:32:08.490Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R1 处置核对

R1 (qa-engineer 单席) 提交 0 Critical / 5 Major。对照 v2 (post_planning R1 rework) 与 v1→v2 汇总处置表 (aggregated M5/M6/M7)，逐条核对三态 (已修复 / 部分修复 / 未动/新增反复):

| R1 编号 | 内容 | v2 核对 | 三态 |
|---|---|---|---|
| Major-1 | TASK-003 `test_owner_segment_participates_in_grouping_key` 行锚 `:958-971` 错, 应 `:1039` | 实读 `grep -n` 确认 `test_both_latest_active_still_reports_self_multi_container` 在 `:305`, `test_owner_segment_participates_in_grouping_key` 在 `:1039`；yaml TASK-003 deliverables 现写 `:305; ... :1039`，逐字命中 | **已修复** |
| Major-2 | TASK-004 交付物 `test_normalize_snapshot.py` 与 verification 无结构性关联 | yaml TASK-004 deliverables 改为 `test_track_board_advisories.py` (新建；与 TASK-009 共用)，两任务共同关注 `identity_advisories` 字段在 track_board 侧的容错/渲染，主题一致 | **已修复** |
| Major-3 | TASK-008 交付物 `test_phase1_gate_advisory.py` 是他 Spec 文件, 语义已占用 | yaml TASK-008 deliverables 改为新建 `test_identity_label.py` + `test_migration_inventory.py`，`grep -in "label\|migrat\|container-id"` 对 `test_phase1_gate_advisory.py` 核实零命中，两文件互不冲突 | **已修复** |
| Major-4 | TASK-011 「rule 1.54 命中」按字面无求值引擎可测, 工时/降级决策未写明 | TASK-011 改为「SC-9 代码侧回归锁 (baseline-green)」, 明确移出「先红」集合, notes 点破「rule 1.54 为散文规则(全仓 py 零命中), 触发面由 TASK-024 文档 token 断言承载」, rule6_note/组 1 抬头均不再点名 011 | **部分修复 — 见下方新 Major-1**: TASK-011 自身的降级决策已写明是修复到位的部分；但它甩给 TASK-024 承载的「触发面」在 TASK-024 里实际未落地 (SC-9 原字面子句仍无真实承载), 是本轮新开的 Major，与 R1 Major-4 同根 (「rule 1.54 无求值引擎」) 但换了破口位置 |
| Major-5 | TASK-032/033 回归跑法未定, 双 lib 包陷阱未点名 | `metadata.test_runner` 已写两种跑法 + sys.path 顺序注意事项; TASK-032 notes 写「起草日全套 1492 个 test 定义 (grep def test_)」, 已实跑核对 grep 数字 (1492) 本身准确 | **部分修复 — 见下方新 Critical**: 「写明跑法」这一字面诉求已满足, 但本轮实跑发现两种跑法覆盖的测试集合并不相同 (相差恰 16, 全部落在本 Spec 最核心的 `test_collision.py`), R1 只核对了数字一致性 (code-reviewer: 「全仓 def test_ 计数 1492 与 4.2 一致」), 未有人实际执行 `run_tests.py` 核对「Ran N tests」是否等于 1492 —— 本轮实跑执行后发现新的、更深的缺陷 |

R1 5 条 Major：**3 条完全修复 (Major-1/2/3)，2 条部分修复但派生出本轮新问题 (Major-4→新 Major-1；Major-5→新 Critical-1)**。0 条原样未动、0 条反复回退。

## 审计结论

实读范围: proposal.md v8 全文、tasks.md 全文 (v2)、detailed-tasks.yaml 全文 (v2，38 TASK)、aria `7dd0135` 与 standards `cc864ee` 匹配 `metadata.scope_repos`；`test_handoff_multibranch_collision_dedupe.py` 全部指定行区间 (`:208-241` `_build_repo` / `:305` / `:1039`)、`track_board.py` 全部指定行区间 (`:349` `:459-475` `:700-808` `:744` `:775-793`)、`collision.py:335-360`、`RECOMMENDATION_RULES.md:31`、`test_git_operation_rule.py` 全文、`state-snapshot-schema.md:1085-1125`、`.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md` 与 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 存在性、`tests/` 目录全量文件名 (新建 4 文件命名一致)、`detailed-tasks.yaml` 全部 `dependencies` 引用完整性 (脚本核实无悬空引用)、agent 计数 (15/15/8=38，脚本核实)。**实跑** `python3 aria/skills/state-scanner/tests/run_tests.py`（全套，耗时 344.9s）。

### Critical-1 (新增): SC-7 声明的「正规跑法」`run_tests.py` 对本 Spec 最核心的 `test_collision.py` 静默零覆盖，TASK-032 的回归锁在该文件上是空判据

**实跑证据**: `python3 aria/skills/state-scanner/tests/run_tests.py` 输出 `Ran 1476 tests ... OK`。`grep -rn "^    def test_\|^def test_"` 对 `tests/` 全目录计数 **1492**（与 TASK-032 notes「起草日全套 1492 个 test 定义」逐字一致，本身准确）。**1492 − 1476 = 16**，AST 脚本核实这 16 个恰好全部是 `tests/test_collision.py` 里的**模块级裸函数**（非 `unittest.TestCase` 方法），且 `python3 -c "unittest.TestLoader().discover('tests', pattern='test_collision.py').countTestCases()"` 直接返回 **0**。`test_collision.py` 自身文档字符串写明其运行方式是 `python3 -m pytest tests/test_collision.py -v` 或 `python3 tests/test_collision.py`（文件自带 `run_all()` fallback，`if __name__ == "__main__": run_all()`），**从未提及** `run_tests.py`。用 `pytest --collect-only tests/test_collision.py` 核实可收集全部 16 个（pytest 不要求 `TestCase`）。

**为什么是 Critical, 不是 Major**: `test_collision.py` 不是普通文件——它是 **TASK-001 / TASK-002 / TASK-004 / TASK-007** 四个任务的**唯一**交付物落点，而这四个任务正是 rule6_note 五条 Rule #6 substitute（SC-1 / SC-2 含族键臂 / SC-4 / SC-8）里的**三条**（SC-1/SC-2/SC-8）的载体，也是 TASK-012/013/014（`split_owner_container` / `identity_key` / `classify_claims` / `identity_drift_advisories` 的核心实现）事实上的唯一单元测试锁。`metadata.test_runner` 把 `run_tests.py` 定为「正规跑法」，TASK-032 verification 要求「`run_tests.py` 零失败 (点名改写项外零新增红)」——但这句判据对 `test_collision.py` 是**空判据**：无论 TASK-013/014/016（都会改动 `collision.py`，`test_collision.py` 正是覆盖它的测试）引入什么回归，`run_tests.py` 的 `Ran N tests ... OK` 都不会反映，因为这 16 个测试从未被计入过那个 N。这不是「跑法要写清楚」的文档问题（R1 Major-5 已经解决了那部分），而是**声明为权威的 CI 等价物结构性看不见本 Spec 自己的核心回归锁**。

**旁证 (风险不是假设性的)**：TASK-032 verification 写「pytest 备选同结论」，语义上把 `run_tests.py` 当主、pytest 当"确认"角色 (备选)；`run_tests.py` 报 `OK` 会被合理误读为「regression clear」，而实际上对 `test_collision.py` 这唯一一次核对全靠"备选"跑法是否真的被执行到、且执行者是否真的去核对了它的输出而非把 `run_tests.py` 的 `OK` 当作已经足够。

- **建议修复** (供 B 期参考，不越权替 owner/执笔容器裁定): (1) TASK-032 verification 改为明确要求 `pytest -q` 对 `tests/` 全目录跑通且 collected 数 == 1492 (或改后的准确数字) 作为**唯一**权威判据，`run_tests.py` 降级为「补充」；或 (2) 单独一条 TASK 把 `test_collision.py` 转成 `unittest.TestCase` 子类使其能被 `run_tests.py` discover（改动面更大，且本 Spec 已经在改这个文件，一次到位风险可控）；或 (3) 至少在 `metadata.test_runner` / TASK-032 notes 里显式记录「`run_tests.py` 对 `test_collision.py` countTestCases()==0，SC-1/2/8 的回归锁只能靠 pytest」，把「备选」改叫「唯一权威」，避免被误读。

### Major-1 (延续自 R1 Major-4 破口位置转移): SC-9「rule 1.54 触发面测试」子句在 v2 里没有任何任务真正承载

proposal v8 SC-9 字面仍保留：「rule 1.54 触发面测试 (`coordination.enabled=false` + `kind=cross_owner` → 命中)」——这句话在 v7→v8 同步清单（Status 行只列出「S2 项改为激活后追加 / SC-7 例外 / 决策单路径勘正」三处）里**未被编辑**。而 TASK-011（1.11）notes 明确写「rule 1.54 为散文规则无求值引擎 ⇒ 其触发面由 3.4 的文档 token 断言承载」，把球踢给 TASK-024（3.4）；但实读 TASK-024 verification：「SC-9 文档: 五文件各与 {`cross_owner`, `self_multi_container`, `identity_advisories`} 交集非空且上下文与 §2.3.5 同义…」——这是一个通用的「取值措辞与规范同义」文档一致性检查，**从未提及** `coordination.enabled`，也不检查 `RECOMMENDATION_RULES.md:31`（rule 1.54 那一行）的触发条件文本是否覆盖 `cross_owner`。

实读 `RECOMMENDATION_RULES.md:31`（grep 核实行号命中）: `concurrent_churn_detected | 1.54 | ... | tracks_multibranch.collision.kind != none 且 config coordination.enabled == false ... |`——该行今天已经含 `coordination.enabled == false` 与 `kind != none`（`cross_owner` 是 `kind` 的一个取值, 被 `!= none` 泛化覆盖, 但字面上从不出现 `cross_owner` 这个 token），T7/TASK-024 计划只「加 `identity_advisories` 一句」，不改这行的判据文本本身。全仓 `grep -rn "concurrent_churn_detected\|1\.54"` 对 `tests/` 目录核实零命中——没有任何既有测试、也没有任何本 Spec 新建测试覆盖这一行的判据文本结构（对照先例 `test_git_operation_rule.py::test_trigger_references_collector_field` 这种「断言规则行引用了正确字段名」的结构性锁，本 Spec 完全没有对等物）。

**结果**: TASK-011 说"触发面归 3.4"，TASK-024 的判据里没有"触发面"这回事——两个任务互相指认对方承载，实际上都没做，SC-9 这一个子句是空判据，和 R1 Major-4 揭示的问题（「rule 1.54 命中」不可字面测试）同根，只是 R1 修复动作把破口从 TASK-011 本身移到了 TASK-011↔TASK-024 的分工缝隙里，没有真正消解。

- **建议修复**: 仿照 `test_git_operation_rule.py` 的结构性先例，在 TASK-024（或单独一条任务）里加一条**结构性**断言：`RECOMMENDATION_RULES.md:31` 同时含 token `coordination.enabled` 与 `tracks_multibranch.collision.kind`（或更贴合地：`kind != none`），锁住"这一行判据条件引用了正确字段，`cross_owner` 是 `kind` 的可达取值之一"，而不是尝试对不存在的求值引擎做行为测试；同时 proposal SC-9 的字面「命中」措辞应该软化为与这条结构性断言一致的说法，避免下一轮审计再原地打转。

### Major-2 (新增): TASK-020 新增行锚 `:459-475` 与依赖 `TASK-016`，与同一轮 backend-architect 自己核实过的架构结论直接矛盾

v1 (R1) 里 TASK-020 的 `dependencies` 是 `[TASK-014, TASK-009]`（不含 TASK-016），backend-architect 在 R1 Finding 4 里**专门核实并排除**了「TASK-020 隐藏依赖 TASK-016」的假设，原文：「⚪ 行渲染基于 `identity_drift_advisories(tracks)` 输出, 按 `identity_key`…而 TASK-016 归一的 `tracks_by_tid` 字典是按剥离后 `track_id` 索引、供 `_render_collision_lines` 的 collision 行标签用, 与 ⚪ 行渲染是两条独立数据路径。因此 TASK-020 现有 dependencies `[TASK-014, TASK-009]` 已足够, **不**存在对 TASK-016 的隐藏依赖」。

v2 里 TASK-020 的 `dependencies` 却变成了 `[TASK-014, TASK-016, TASK-009]`（新增 TASK-016），且 deliverables 新增了行锚「插入点 `:459-475` (kind 分支旁) + dedupe 前调用 `:744`」。实读 `track_board.py`：

- `:744` (`_dedupe_tracks_for_collision(tracks)[0]`) 确认命中，是 `render_track_board()` 顶层函数体内、dedupe 发生前的位置，与 proposal §D3「dedupe 前调用」的要求吻合，**这半个锚点是对的**。
- `:459-475` 落在 `_render_collision_lines(verdicts, tracks_by_track_id)`（`:334-508`）函数体内，是 `for tid in sorted(verdicts.keys())`（`:366` 起）这个**按 track_id 遍历**的循环体里的 `elif collision_kind == "none": pass` / `else` 兜底分支——这个函数的两个入参 `verdicts`／`tracks_by_track_id` 都来自**已 dedupe 后**的 `all_collidable`（`:754-757`，源头是 `:743-744` dedupe 之后的 `collision_input_tracks`），且函数签名不接收原始 `tracks`。`identity_drift_advisories()` 的输出是按 `identity_key`（uuid 容器）聚合、需要 dedupe **前**的原始 `tracks`（proposal §D3 原文、TASK-009 verification「fixture 渲染恰 2 条 ⚪ (`023236f2` / `bfe8285d`)」也是按容器 identity_key 而非 track_id 计数）——这与 `_render_collision_lines` 的每 track_id 一行的渲染模型是两个不同的迭代维度，函数当前签名无法在 `:459-475` 处拿到 identity_advisories 数据，除非另外改签名（yaml 未提及）。

也就是说，v2 为了补上 R1 backend-architect Finding 4 提出的「TASK-020 缺锚点」这个 Minor gap，新加的锚点和依赖**恰好精准踩进了同一轮审计明确验证过是错误方向的假设**——即"⚪ 渲染应该挂在 `tracks_by_tid`/`_render_collision_lines` 附近"。如果 B 期执行者信这个锚点在 `:459-475` 处按"kind 分支旁"字面插入代码，要么插不进去（缺数据），要么被迫在错误的每-track_id 循环里做去重/单例判断把 ⚪ 行渲染成多份或者漏渲染，与 SC-10「恰 2 条 ⚪ 行」的反事实要求（"对 dedupe 后行算 → 0 行"）在逻辑上正好是这个循环天然会踩中的坑（`tracks_by_tid` 就是 dedupe 后的数据）。

- **建议修复**: 撤销 TASK-020 对 TASK-016 的依赖，恢复为 `[TASK-014, TASK-009]`（backend-architect R1 结论）；`:459-475` 锚点删除或改写为「`render_track_board()` 顶层，`:744` dedupe 调用前后新增 `identity_drift_advisories(tracks)` 调用 + 在 `:805-806` 组装 `collision_lines` 前追加渲染出的 ⚪ 行」这类准确描述实际数据流的位置，不落在 `_render_collision_lines` 内部。

## Verdict

FAIL — 1 Critical / 2 Major / 0 Minor。Critical 是本轮实读+实跑（lens 5 明确要求）新发现，不是 R1 遗留反复；2 条 Major 都是 R1 Major-4/5 的「部分修复」在别处派生出的新问题（球被踢到了没接住的地方），不是原地踏步。R1 的 3/5 Major（行锚/文件误配三处）已完全、干净地修复，SC 覆盖矩阵、rule6_note 点名集、组 1/组 4 依赖闭包、5.x 发布顺序、i18n 主仓同步面等 R1 其余争议点在本轮复核均成立，无新问题。

## Vote

REVISE

## 轮次记录

- Round 1 (qa-engineer, convergence): REVISE — 0 Critical / 5 Major (TASK-003 行锚错位 / TASK-004 文件误配 / TASK-008 文件误配 / TASK-011 可测试性未澄清 / TASK-032-033 回归跑法未定且未点名双 lib 包陷阱)。
- Round 2 (本轮, qa-engineer, convergence): FAIL — 1 Critical (新增: `run_tests.py` 对 `test_collision.py` 静默零覆盖, 实跑 `Ran 1476 tests` vs grep `1492` 差 16, AST+`countTestCases()==0` 双重核实) / 2 Major (SC-9 rule 1.54 触发面子句无承载, TASK-011↔TASK-024 互相指认落空; TASK-020 新锚点 `:459-475`+新依赖 TASK-016 与同轮 backend-architect 自己验证过的架构结论矛盾)。R1 5 Major 中 3 条 (行锚/文件误配) 完全修复, 2 条 (可测试性/回归跑法) 部分修复但派生新问题, 0 条反复回退。
