---
checkpoint: post_planning
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-09-05T22:57:24.913Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R2 处置核对

对照 R2 聚合报告 (`post_planning-R2-2026-09-05T223208-490Z-...-aggregated.md`) 的处置表，逐条核对 v3 (`detailed-tasks.yaml` updated 字段标注 "v3: post_planning R2 rework") 落地情况：

| R2 编号 | 内容 | v3 核对 | 三态 |
|---|---|---|---|
| PP2-C1 (唯一 Critical) | `run_tests.py` 对 `test_collision.py` `countTestCases()==0`；要求双跑法 + 双计数 + RED→GREEN 用 pytest | `metadata.test_runner` 已改写为「两种跑法都必跑」+ 具体命令 (a)/(b) + 双计数判据文字；TASK-032 verification 拆成 (a)/(b) 双计数；TASK-031/rule6_note 沿用 metadata.test_runner 的 pytest 记录要求；tasks.md 4.2 同步同一文字 | **部分修复 — 见下方新 Critical-1**：文字层面的「双跑法」已写全，但**实跑**发现 (b) 分支的文档命令本身不可执行 (见下)，问题从「静默漏跑」换成了「显式报错阻断」，同一功能目标 (让 pytest 分支真正机械可执行) 仍未达成 |
| M1 (S1 兜底无承载体) | TASK-042 (5.8) 手动开 tracker issue | 新增 TASK-042，deliverables/verification 与 tasks.md 5.8、「S2 后续」表激活规则三处文字一致 (实读 tasks.md :90/:103 与 yaml TASK-042 逐句比对，无出入) | **已修复** |
| M2 (组 0 不在 merge 前置) | TASK-034/038 deps 补 TASK-000/040 | 实读 TASK-034 `dependencies: [TASK-035, TASK-037, TASK-000, TASK-040]`；TASK-038 `dependencies: [TASK-039, TASK-040]` (040 已含，000 未见于 038——038 依赖 039 之后执行，039 依赖 041/033，041 依赖 036→034→000/040，传递闭包已含 000，无需 038 直接列出) | **已修复** |
| M3 (SC-9 rule 1.54 无承载) | proposal SC-9 改文档断言；TASK-024/TASK-011 分工 | proposal v9 SC-9、TASK-011、TASK-024 三处均已重写为「文档断言」分工模式，方向正确 | **部分修复 — 见下方新 Major-1**：TASK-024 verification 对 `RECOMMENDATION_RULES.md:31` 只要求补 `identity_advisories`，未覆盖 SC-9 首句同时要求的 `cross_owner` token，三者不完全同文 |
| M4 (回帖措辞超报) | TASK-038 按形态分写 | TASK-038 verification 已写「S1 = 缺口 3 部分闭合...label 陷阱待 S2 或 tracker；S2 = 缺口 3 闭合」 | **已修复** |
| M5 (TASK-020 锚点矛盾) | 独立数据路径, 去掉对 TASK-016 依赖 | 实读 `track_board.py`：TASK-020 `dependencies: [TASK-014, TASK-009]` (016 已去掉)；deliverables 锚点改为「dedupe (:744) 前对原始 tracks 调 identity_drift_advisories，输出为 collision 段 (:796 之后) 的独立段；不进 per-track 循环」，`:744` 逐行核实命中 `_dedupe_tracks_for_collision(tracks)[0]`，`:796` 附近 (`:790-808`) 核实是 reconcile 分支收尾 + `collision_lines` 渲染循环 + `return`，「之后」的独立段落点 (return 前) 描述准确 | **已修复** |
| M6 (TASK-022 位置反惯例) | 改紧贴标题 blockquote | TASK-022 deliverables/verification 已改「紧贴 §2.3.5 标题下方的 `> **Amended**: ...` blockquote」 | **已修复** |
| M7 (TASK-041 漏 :139) | 加 CLAUDE.md :139 | TASK-041 deliverables 已加「:139 方法论轨区间端点」；实读 `CLAUDE.md:139` 当前内容确为「aria-plugin 方法论轨: v1.52.0–v1.69.1 已 ship」，`:141` 为版本行，锚点均命中 | **已修复** |

小结：R2 的 1 Critical + 7 Major 中，5 条 (M1/M2/M4/M6/M7) 完全修复；2 条 (PP2-C1、M3) 在文字层面已按决策方向重写，但**实跑/交叉核对后发现同类问题以新形态残留**——不是原地踏步，是决策执行到位但覆盖不完整。

## 审计结论

实读范围：proposal.md v9 全文 (含 SC-1..SC-11 逐条、Status 行)、tasks.md 全文 (v3，S2 后续表、SC↔任务映射表)、detailed-tasks.yaml 全文 (v3，39 TASK)、`track_board.py` 指定区间 (`:334-508` `_render_collision_lines`、`:700-808` 顶层 collision 段、`:744` `:790-808`)、`RECOMMENDATION_RULES.md:31`、`references/rules/advanced-rules.md:540-580`、`CLAUDE.md:137-142`。**实跑**（本轮新增，lens 1 要求）：

1. `python3 aria/skills/state-scanner/tests/run_tests.py`（全套，主仓根）→ `Ran 1476 tests ... OK`，与 metadata/tasks.md 记录的基线数字一致。
2. `/home/dev/.local/bin/pytest -q -p no:cacheprovider aria/skills/state-scanner/tests`（metadata.test_runner / tasks.md 4.2 / TASK-032 逐字命令，主仓根）→ **`Interrupted: 12 errors during collection`**，0 个测试被收集或运行。逐一复核：12 个失败文件（`test_architecture.py` `test_audit.py` `test_changes.py` `test_custom_checks.py` `test_detailed_tasks.py` `test_forgejo_config.py` `test_gate_yaml_datasource.py` `test_gate_yaml_golden_corpus.py` `test_gate_yaml_only_source.py` `test_gate_yaml_probe_reach.py` `test_git.py` `test_git_operation_detection.py`）报错均为 `ModuleNotFoundError: No module named '_helpers'`。改用 `cd aria/skills/state-scanner && pytest tests/test_git.py`（相对路径、同目录起跑）复测，同一报错，与工作目录无关。加 `--import-mode=importlib` 复测，同一 12 个文件同一报错（说明这不是 pytest rootdir 猜测模式的问题，是更底层的路径缺失）。

**根因**：`aria/skills/state-scanner/tests/__init__.py` 存在，使 `tests/` 成为一个真 Python 包；pytest 按 dotted-name (`tests.test_xxx`) 导入时，把「有 `__init__.py` 链」的顶层目录 (`aria/skills/state-scanner/`) 插入 `sys.path`，而不是 `tests/` 目录本身——`_helpers.py` 恰恰放在 `tests/` 目录内、被各测试文件用裸 `from _helpers import ...` 引用，因此在 pytest 的这种插入方式下永远不在 `sys.path` 上。这与 metadata.test_runner 给出的补救提示「sys.path 顺序必须 scripts 后 state-scanner 在前 (双 lib 包陷阱)」是**两类不同根因**：那条提示针对的是 `lib` 包重名遮蔽（`lib/` vs `scripts/lib/`），但当前失败发生在 collection 阶段、连 `lib` 导入语句都还没执行到，`_helpers` 缺失与双 lib 包无关。也就是说，metadata.test_runner 目前唯一写出的「已知陷阱」并不能解释、也不能修复实际观测到的失败模式——这条记录本身看起来未经实跑校验（呼应本仓 memory `feedback_sot_example_commands_are_never_executed`）。

**尝试寻找可行变通**（供 B 期参考，非越权代为决策）：
- `PYTHONPATH=<tests 目录>` 单独设置：解开 `_helpers`，但转而在 `test_collision.py` / `test_coordination_no_push.py` / `test_coordination_ref_lib.py` 三个文件触发**双 lib 包遮蔽**（`ModuleNotFoundError: No module named 'lib.coordination_ref'` / `lib.claim_lifecycle`，或 `ImportError: cannot import name 'collision' from 'lib'`，指向 `scripts/lib/__init__.py`）——这正是 metadata 提示的那个陷阱，但触发条件是「先设置了正确的 PYTHONPATH 之后」，命令本身不会自动规避。
- `PYTHONPATH=<tests 目录> --import-mode=importlib`：这是本轮实际测出的、唯一让全部测试**完成收集**的组合（未见于 metadata.test_runner / tasks.md / TASK-032 任何位置的文字）。收集结果：`26 failed, 1465 passed, 1 skipped`（主项）+ `177 subtests passed`；`26+1465+1=1492`，与「全套 def test_ 1492」精确对上。但 26 个失败集中在 `test_coordination_no_push.py`（8 个）与 `test_release_by_track.py`（18 个），报错含 `fetch_failed` / `yaml_unavailable`——这两个文件是 `run_tests.py` 报告的 1476 个「OK」测试的一部分（同一 host、同一 checkout 下 `run_tests.py` 全绿），说明这 26 个失败是**这条变通命令自身引入的环境副作用**（很可能是 `PYTHONPATH` 注入影响了测试内部 `subprocess.run()` 子进程的模块解析），而不是真实回归，需要额外排查才能建立信任，不能直接当「零失败」证据使用。

**结论**：TASK-032 verification (b)「pytest 全套零失败 且收集数 ≥ 1492」当前**不可机械执行**——逐字执行文档命令得到 0 收集 + 12 报错；已知的「变通」路径本身又产出 26 个需要额外排查的新失败。R2 的初衷是让「双跑法」的 pytest 分支真正覆盖 `test_collision.py`（PP2-C1 的核心诉求），但目前 pytest 分支自己先在 collection 阶段整体失败，别说覆盖 `test_collision.py`，全套一个测试都跑不起来。

### Critical-1（新增）：metadata.test_runner / tasks.md 4.2 / TASK-032 verification (b) 文档的 pytest 命令逐字执行 0 测试收集，「双跑法」的第二条腿事实上不可执行

**实跑证据**（见上）：`/home/dev/.local/bin/pytest -q -p no:cacheprovider aria/skills/state-scanner/tests` 从主仓根直接执行 → `!!!!!!!!!!!!!!!!!!! Interrupted: 12 errors during collection !!!!!!!!!!!!!!!!!!!`，`12 errors in 1.33s`，无一测试运行。两次独立复测（默认工作目录 / cd 进 skill 目录用相对路径）与加 `--import-mode=importlib` 复测，结果一致，非偶发。

**为什么是 Critical，不是 Major**：这条命令是 R2 用来关闭上一轮唯一 Critical (PP2-C1) 的核心机制——PP2-C1 的病灶是「`run_tests.py` 单跑对 `test_collision.py` 静默零覆盖」，R2 的处置是「双跑法都必跑，pytest 负责补上 `test_collision.py`」。现在 pytest 分支本身在 collection 阶段就失败，**覆盖不到 `test_collision.py`，也覆盖不到任何其他测试**——TASK-032 (SC-7) 唯一能验证「本 Spec 改的代码 (`collision.py` / `track_board.py` / `identity.py` 等) 没有引入回归」的双保险机制，此刻只剩 `run_tests.py` 一条腿在跑（且这条腿仍然看不到 `test_collision.py` 里的 16 个裸函数，PP2-C1 的病灶原样还在），另一条腿（pytest）自己先倒下。这不是「文档写得不够细」的 Minor/Major 问题，而是「作为规范唯一权威 SC-7 判据的一半，此刻空转」的结构性缺陷——与 PP2-C1 同一严重级别，只是失败表现形式从「静默假绿」变成了「显式报错」（后者其实更安全，因为不会被误读成通过，但仍然阻塞机械判据本身）。

**建议修复**（供 B 期参考，不越权替 owner/执笔容器裁定）：(1) 在 metadata.test_runner / tasks.md 4.2 / TASK-032 中把 pytest 命令换成实测可行的具体形式（如显式 `PYTHONPATH` + 处理 26 个环境副作用失败后的净判据），而不是停留在「sys.path 顺序注意」这种不指向实际根因的提示；或 (2) 单独开一条任务，诊断并修复 `PYTHONPATH=<tests>+importlib` 组合下 `test_coordination_no_push.py` / `test_release_by_track.py` 26 个失败的真实来源，确认是否为子进程环境变量污染后再定案；或 (3) 至少在 notes 里如实记录「起草日实测：文档命令 0 收集失败；已知变通产生 26 个待排查的新失败；本 SC-7 (b) 判据在此状态下暂不可执行」，避免 B 期执行者按文档字面执行后卡在同一个坑里且找不到已知诊断记录。

### Major-1（新增）：SC-9 首句要求 `RECOMMENDATION_RULES.md:31` 同时含 `cross_owner` 与 `identity_advisories` 两个 token，TASK-024 只覆盖了后者，三者不完全同文

**实读证据**：proposal v9 SC-9 首句（逐字）：「`RECOMMENDATION_RULES.md:31` 与 `references/rules/advanced-rules.md:544-572` 的 rule 1.54 行含 token `cross_owner` 与 `identity_advisories`」——这是一条独立于「六处文档非空交集」检查之外的**更严判据**，明确要求这两个具体文件位置**同时**含两个 token。紧接着的括注「(机械只锁非空交集; `RECOMMENDATION_RULES.md:31` 今日无取值字面, 加 `identity_advisories` 一句后满足)」，实读上下文可确认该括注**只是给「六处文档非空交集」检查的机械判据打补丁说明**（非空交集只需三选一，identity_advisories 够了），并不是把首句「两个 token 都要」的要求撤销或软化。

实读 `RECOMMENDATION_RULES.md:31` 当前内容：`... tracks_multibranch.collision.kind != none 且 config coordination.enabled == false ...`——**没有字面 `cross_owner`**（`kind` 用泛化的 `!= none` 表达，`cross_owner` 只是 `kind` 的一个可达取值，字面 token 不出现）。实读 `advanced-rules.md:544-572` 当前内容：conditions 块注释 `# TASK-000 持久化字段 (cross_owner | self_multi_container)`——**已经含 `cross_owner`**，只缺 `identity_advisories`。

再实读 TASK-024（3.4）：
- deliverables 仅写「`RECOMMENDATION_RULES.md   # :31 加 identity_advisories 句`」——**未提及需要同时补 `cross_owner`**；
- verification 仅写「rule 1.54 行含 identity_advisories」（单 token），以及独立的「五文件各与 {cross_owner, self_multi_container, identity_advisories} 交集非空」（这条对 `RECOMMENDATION_RULES.md` 只需 identity_advisories 一个 token 即可满足，不要求 cross_owner）。

结果：如果 B 期执行者只照 TASK-024 的 deliverables/verification 逐字执行，会给 `RECOMMENDATION_RULES.md:31` 加上 `identity_advisories`（满足 TASK-024 写出的两条判据），但**不会**给它加上 `cross_owner`——SC-9 首句对这一行「两个 token 都要」的要求就落空了。`advanced-rules.md` 那一行则相反，天然已经有 `cross_owner`，只要 TASK-024 补上 `identity_advisories` 即满足首句要求，不受影响。也就是说这个缺口**只在 `RECOMMENDATION_RULES.md:31` 这一处**，且恰好是 SC-9/TASK-024/TASK-011 三方分工链条里，proposal 首句写得最严、任务文字写得最松的那一个交叉点——与 R2 M3 揭示的问题（proposal 与任务文字不同文）同类，只是从「整条子句完全没有承载」缩小为「一个具体 token 的遗漏」。

**建议修复**：TASK-024 的 `RECOMMENDATION_RULES.md` deliverables/verification 改为「:31 加 `identity_advisories` 一句，且行内保留/补足 `cross_owner` 字面 token（可用 `kind == cross_owner` 或等价改写替换/补充现有 `kind != none` 泛化表达，需与 §2.3.5 三行同义）」，使其与 SC-9 首句「两文件的 rule 1.54 行都要含两个 token」逐字对齐。

## Verdict

FAIL — 1 Critical / 1 Major / 0 Minor。Critical 由本轮实跑（lens 1 明确要求）首次发现：R2 用来关闭上一轮唯一 Critical 的双跑法机制，其 pytest 分支的文档命令逐字执行 0 测试收集，是同一功能目标 (SC-7 双保险机制真正机械可执行) 的延续性未达成，非独立新缺陷、亦非反复回退。Major 由三方同文核对（lens 2 明确要求）发现，是 R2 M3 处置在一个具体 token 上的遗留缺口。R2 其余 6 项处置 (M1/M2/M4/M5/M6/M7) 全部完全、干净修复，TASK-020 独立数据路径锚点、TASK-042 tracker 承载、CLAUDE.md :139 锚点等本轮逐行实读均命中。SC-1..SC-11 全表复核：11 条在 yaml 中均有 `SC-` 字面引用承载，未见脱钩；TASK-042 未挂 SC 编号，但与 TASK-038/040 等同组「流程类」任务同形，是合理的非 SC 归属，不构成缺口。

## Vote

REVISE

## 轮次记录

- Round 1 (qa-engineer, convergence): REVISE — 0 Critical / 5 Major。
- Round 2 (qa-engineer, convergence): FAIL — 1 Critical (`run_tests.py` 对 `test_collision.py` 静默零覆盖) / 2 Major (SC-9 rule 1.54 无承载；TASK-020 锚点与依赖矛盾)。
- Round 3 (本轮, qa-engineer, convergence): FAIL — 1 Critical (新增，实跑发现: pytest 双跑法第二条腿的文档命令逐字执行 0 测试收集，`_helpers` 模块找不到；变通路径又产出 26 个待排查新失败，SC-7 (b) 判据当前不可机械执行) / 1 Major (新增，三方同文核对发现: SC-9 首句要求 `RECOMMENDATION_RULES.md:31` 同时含 `cross_owner`+`identity_advisories`，TASK-024 只写了后者)。R2 的 1 Critical (PP2-C1) 与 7 Major 中 6 项 (M1/M2/M4/M5/M6/M7) 完全修复；PP2-C1 与 M3 在文字/决策方向层面已重写，但覆盖不完整，各自派生出本轮新发现，未反复回退到原样。
