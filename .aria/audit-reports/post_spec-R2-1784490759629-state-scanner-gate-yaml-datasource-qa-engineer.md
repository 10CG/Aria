---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-19T19:49:06.665Z
context: state-scanner-gate-yaml-datasource
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R1 finding 闭合核验 (要点; 全文见编排层聚合)
F1 — CLOSED (carve-out 精确; test_both_sources_no_false_warn 与新旧行为均兼容)。F2 — 表层 CLOSED (44/44 复核精确; 但见 NEW-2 适用范围)。F3 — CLOSED (16/16 metadata 恒在 tasks: 前, 结构性排除; 行首锚定排除 prose 案例全部实测)。F4 — CLOSED (SC-3a/b/c/d 分列, 伪 yaml 对应 SC-3a)。F5 — CLOSED (精确串写死, 静态可验)。

## 新 finding

### NEW-1 Major / architecture+documentation / 决策9/SC-12 vs DEC-20260705-001 R3 先例 / issue
references/runtime-probe-declaration.md:26-30 明文「无 tasks.md 的 spec (Level 2/proposal-only) 即使写声明也不评估 — designed behavior — 集成测试锁定」; TestRuntimeProbeFoldL2ProposalOnlyEvaporates::test_l2_proposal_only_declaration_never_evaluated 锁死 (实测绿, 136 passed)。SC-8 golden 两份 (context-monitor/ai-native-estimator) proposal 自称 Level 2 proposal-only — 决策 9 正是在为该类 spec 反转 R3 结论, 全篇零披露 (未提 DEC / 未提测试类 / runtime-probe-declaration.md 不在 Impact)。细粒度: 锁定测试 fixture 是「无 tasks.md 无 yaml」裸场景, 窄读不变红; 但 reference 文档与测试类 docstring 的泛化表述在 yaml-only 子集上将成事实性错误 —「测试不变红但文档语义过期」变种。:1430 注释对裸场景仍不成立, 修复只是部分修复。fix 二选一: (a) 显式引用 DEC-20260705-001, 给出 yaml-only 子集反转理由 (与「yaml-only 一等公民」核心论点一致, 理由站得住), 同步 runtime-probe-declaration.md §前置条件 + 测试类 docstring + sibling 测试锁「yaml-only 可评估 / 裸 proposal-only 仍零痕迹」精确边界, 补入 Impact; (b) SC-12/决策9 移出 scope 作独立 follow-up。

### NEW-2 Minor / documentation / CRLF 证据适用范围 / issue
5 份带 \r 语料全部 dual-layer (precedence 排除), SC-8 golden 3 份字节级零 \r — 「CRLF 真实语料形状」对整体成立、对 yaml-only 子集零观测。SC-11 合成负控合法性不受影响; §Why/决策10 措辞须明示来源全为 precedence 排除的 dual-layer。

### NEW-3 Minor / implementation / status 空值归属 / risk
`status:` 空值/`""` → raw_status="" (str 非 None), 与缺键→None→status-missing 两条路径; 归属未定 → reason 串格式漂移。fix: 对齐 custom_checks `if rest else None` 惯例 (空→None→status-missing) + SC-3d sibling 负控。

### NEW-4 Minor / documentation / Impact 路径错误 / issue
DUAL_LAYER_SPEC.md 实际在 skills/task-planner/ 根 (无 references/ 子目录, find 核验)。fix: 订正防误建重复文件。

### NEW-5 Minor / documentation / SC-9 测试计数目标缺 / issue
项目惯例报 before→after 计数; SC-9 未量化预期新增。fix: Phase B 落地时补记。

## SCOPE_OK 判定
SCOPE_OK。NEW-1 是与既有决策的和解缺口 (soundness 维度) 非 scope 越界, 分开记账。

## Vote
REVISE。NEW-1 触及已批准+测试锁定的先前设计决策, 零披露即入 Phase B 会让文档带过期通用性声称合入主干 (feedback_spec_precedent_verify_execution_history 镜像: 这次是反转先例而非误用先例)。NEW-2~5 Minor 同版本吸收。其余设计经 17 份全量抽查 + 测试实跑 136 passed 判定扎实。
