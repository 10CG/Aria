---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: REVISE
timestamp: 2026-09-05T22:01:31.682Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

审计对象: `detailed-tasks.yaml` (41 TASK) + `tasks.md`，对照 `proposal.md` v7 (commit `60808b2`)。已实读: proposal.md 全文、tasks.md 全文、detailed-tasks.yaml 全文、`aria/skills/state-scanner/tests/` 目录列表、`test_collision.py` / `test_handoff_multibranch_collision_dedupe.py` / `test_normalize_snapshot.py` / `test_phase1_gate_advisory.py` / `RECOMMENDATION_RULES.md` / `test_git_operation_rule.py` / `lib/collision.py` / `lib/identity.py` / `lib/reconcile.py` / `lib/constants.py` / `track_board.py` / `fetch_gate.py` 的相关片段，aria `7dd0135` 与 standards `cc864ee` HEAD 已核对与 metadata.scope_repos 一致。

**SC 覆盖矩阵**: 逐句核对 SC-1..SC-11 与 tasks.md「Success Criteria ↔ 任务映射」表 + yaml verification 字段，未发现无承载子句，也未发现 TASK 引用了 proposal 不存在的子句。rule6_note 五条 substitute (SC-1/2/3(S1)/4/8) 与 TASK-001/002/003/004/005/008 的对应关系（SC-2 由 TASK-002 判定臂 + TASK-005 端到端锁共同承载）内部一致，非缺陷。RED 先行声明（TASK-001/002/003/004/008 均含「先红」与对应现状描述）与 proposal 原文逐一核对一致；组 2 实现任务 verification 均写成「TASK-00x 转绿」而非空话。此两项判据通过。

以下为实读代码后发现的具体缺陷，均为 Major:

**Major-1 (行号锚点/文件定位): TASK-003 的 `test_handoff_multibranch_collision_dedupe.py` 第二个行锚 `:958-971` 不指向应改写的目标函数。** tasks.md 1.3 明确要求「`test_owner_segment_participates_in_grouping_key` 改三臂 (uuid 折叠 / 主机名不折叠 / `devbox01` 不折叠)」。实读该函数实际位于 `:1039-1050`（`grep -n` 核对），而 yaml 给出的 `:958-971` 落在 `TestDedupeFoldsAcrossSessionsWithinSameContainer` 类下的 `test_old_active_session_folds_under_newer_done_session_same_container`（`:907` 起）——一个与 owner 段分组无关的「跨 session 同容器折叠」负向对照测试。yaml 三个行锚（`:305-341` 对，`:958-971` 错）里缺失对 `:1039` 的任何指向，执行者若信锚点会漏改或错改。

**Major-2 (文件误配): TASK-004 的第二交付物 `test_normalize_snapshot.py` 与其 verification 无结构性关联。** 实读该文件（513 行）整体是 `normalize_snapshot.py` 脚本的 golden-diff 键归一测试（`DROP_KEYS`/`EPHEMERAL_PATH_KEYS`/`TIMESTAMP_KEYS`），`grep -n "collision\|identity_advisories"` 零命中；文件里没有任何 track_board / rule 1.54 / fetch_gate 相关断言基础设施。TASK-004 verification 「旧 snapshot 缺该字段时 track_board / rule 1.54 / fetch_gate 不崩」在此文件里无落点，判断为把「schema 归一工具」与「渲染/规则消费方容错」两件事误配到同一交付物。（旁证: fetch_gate 的 `run_gate` 接口只收 `collision_kind: str` 字符串参数，从不触碰 dict 字段，proposal 自身也这么写；因此该子句对 fetch_gate 是重言式, 但对 track_board 不是——track_board 要新增读 `identity_advisories` 的代码 (TASK-020), 其容错测试目前无落点文件。）

**Major-3 (文件误配, 更严重): TASK-008 的交付物 `test_phase1_gate_advisory.py`（既有文件, 未标「新建」）与「T3b 迁移 inventory 告警」测试完全不相关。** 实读该文件开头文档字符串: 「TASK-005 — P1 golden tests for run_gate advisory mode (DEC-20260704-002)」，覆盖的是 `run_gate` 编排器的 occupied / clock_skew / push_failed 三种 advisory 结果映射（另一个 Spec 的 TASK-005），`grep -in "label\|migrat\|container-id"` 零命中。TASK-008 要在此文件里加「label 非空且 `claims/<label>/` 有 active → phase1_gate 输出迁移告警」的新测试, 与该文件既有 `TestAdvisoryOccupied` / `TestAdvisoryClockSkew` 等类的语义完全是两回事（同名「advisory」但指两套不相干机制）。本审计第 3 镜头明确要求核对新建测试文件命名一致性——此处问题更进一步: 不是新文件命名不一致, 是把新测试塞进一个语义已被占用的既有文件, 会造成后续维护者误读「这是 run_gate 的 advisory 测试」。

**Major-4 (可测试性/工时低估): TASK-011 `test_recommendation_rules_collision.py`（新建, 2h）要测「`coordination.enabled=false` + `kind=cross_owner` → rule 1.54 命中」, 但仓内没有「规则触发面」的可执行测试基础设施。** 实读唯一先例 `test_git_operation_rule.py`, 其文档字符串明示: 「structural existence test... Prose AI behavior (stage-2 degrade) is verified by dogfood; this locks the *structural* contract: the rule row exists and references the collector field」——`RECOMMENDATION_RULES.md` 里的规则是喂给 AI 读的自然语言推荐, 不是被某个 Python 函数求值的确定性谓词, 仓内无「规则求值引擎」。TASK-011 verification 字面「→ rule 1.54 命中」若按字面实现（真正判定某输入让规则「命中」）在当前架构下不可行；若按既有先例降级为「表格行存在 + 触发条件文本引用正确字段」的结构性检查, 则与 SC-9/任务标题字面「触发面」「命中」不符, 这个降级决策本身没有在 yaml/tasks.md 里写明, 存在 B 期被隐性降级却仍勾选通过的风险。2h 工时估算是按字面「命中」测试估的, 若走结构性降级路线本身成本更低, 若走真判定路线则远超 2h（需新造求值机制, 越出本 Spec 范围）——两种情形都说明当前描述与工时不自洽。

**Major-5 (回归基线跑法未定, 踩坑已知): TASK-032/TASK-033 的 verification 与 notes 未写明可执行的基线跑法, 且未提及项目已知的「双 lib 包」陷阱。** TASK-032 标题写「state-scanner **pytest** 全套」, 但实读 `tests/run_tests.py` 文档字符串给出的调用方式是 `python3 tests/run_tests.py`（自研 stdlib `unittest`/`trace` 跑法, 非 pytest）——命名与实际工具不一致。更关键的是: TASK-032/033 均无 `notes` 字段, 未记录任何跑法细节, 而 CLAUDE.md 引用的项目记忆明确记载 state-scanner 存在「两个 `lib` 包」import 顺序陷阱（`feedback_state_scanner_dual_lib_package_shadow.md`）——本 Spec 恰好横跨 collector/renderer/lib 三层, `test_collision.py` 与 `test_handoff_multibranch_collision_dedupe.py` 都手写 `sys.path.insert(0, str(_SS_ROOT))` 做 shadow-proof bootstrap, 说明该陷阱在这批测试里是活跃风险。TASK-032/033 若不显式记录正确调用方式 + import 顺序注意事项, B 期大概率重踩此坑، 产生假红或假绿的回归基线。

## Verdict

REVISE — 0 Critical / 5 Major / 0 Minor。均为可定位、可修复的任务规划层缺陷（行号锚点错误 / 交付物文件误配两处 / 可测试性未澄清 / 回归跑法未定且未点名已知陷阱），不构成方法论或 SC 覆盖面的结构性缺口，但会在 B 期造成执行者误改文件、漏改函数或隐性降级验收标准，须在 A.3 内改正后再进 B.1。

## Vote

REVISE

## 轮次记录

- Round 1 (qa-engineer, convergence): REVISE — 5 Major (TASK-003 行锚错位 / TASK-004 文件误配 / TASK-008 文件误配 / TASK-011 可测试性未澄清 / TASK-032-033 回归跑法未定且未点名双 lib 包陷阱)。0 Critical。SC 覆盖矩阵、RED 先行声明、rule6_note 五条 substitute 对应关系均核实通过, 未发现问题。
