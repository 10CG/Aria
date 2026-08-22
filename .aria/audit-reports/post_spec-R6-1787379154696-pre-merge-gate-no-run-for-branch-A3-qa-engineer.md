---
checkpoint: post_spec
mode: convergence
rounds: 6
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-08-22T15:10:00.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 0
minor_count: 1
---

## 摘要

R6 (max_rounds=6 末轮) 复核 v6 (R5-fix)。基线仍 `aria @ 400f0bc`（已核实 `git rev-parse HEAD` 逐字一致，工作树干净）。本轮方法：不信任 spec 自述与聚合表归纳，逐条回到真实代码/文档/AB fixture 源头重新读取，覆盖 R5 全部处置项 + v6 相对 v5 的 13 处 diff + SC-1~16 整体自洽。

## R5 处置核对（归 A3 席的两条 + 全局 4 簇复验）

| 簇# | 来源 | v6 处置 | 状态 | 证据 |
|---|---|---|---|---|
| 1 | A1-R5-M1 + A1-m5 (SC-13 地点 / `--state-file`) | SC-13 改在 aria-plugin 根跑 + 主仓绝对路径 `--state-file`；§3.2 步骤 2 + 3c′ 均显式传 | **closed** | 实读主仓 `.forgejo/workflows/issue-triage-tests.yml`（paths=`aria/skills/issue-triage/**`）与 `aria/.forgejo/workflows/issue-triage-tests.yml`（paths=`skills/issue-triage/**`，均含 `workflow_dispatch: {}`），确认 SC-13 描述的「gate 在 aria-plugin 根 + state 文件走主仓绝对路径」在真实文件结构下可行；§3.2 步骤 2 与 3c′ 两处 CLI 调用行均显式写 `--state-file <主仓根绝对路径>/.aria/workflow-state.json`，无遗漏 |
| 2 | A2-R5-M1 + A1-m3 (`<pr_branch>` 回填零 SC) | SC-5 加 (c)(d) | **closed** | SC-5(c) 断言两变体 message 均含 `feat/x`、不含字面 `<pr_branch>`、`raw_message == gate_error.message`；(d) 断言 verify-failed 后缀与同步。逐行核对 `gate_check` 现状代码（`:387-527`）确认回填逻辑位置（`out.get("gate_error")` 分支）与 `_build_output` 现状签名（`gate_error` 已是 additive 可选键, `:236-273`）完全兼容，v6 新断言精确打在真实执行路径上，非空判定 |
| 3 | 残留簇（A1-m1/A4-m1「七点」・A1-m2/A4-m3 `<owner>/<repo>`・A1-m4/A4-m2 reset 语义・A4-m4 R-e・A1-m6 branches 第三成因・A2-R4-m1/m2） | 全部吸收 | **closed** | 逐条对照 v6 正文：§2.1 标题「第七个早退 return 点」（与实读 `gate_check` 现状 6 点 8 变体 + 新增 1 点吻合，见下方 SC-7 复验）；§2.3 用 `<owner>/<repo>` 尖括号占位替换旧 `{o}/{r}`，并新增「渲染禁用 `str.format`」理由句；§3.2 exit 2 显式「`reset --retry-count` 同时置 `started_at=now`」；Risks R-e 与 §3.2 3d 逐字一致（CLI 退出码 2 → 直接 abort，禁回退手写 JSON）；§2.3 表新增「或 workflow `branches` 过滤不含本分支」第三成因；§3.1 新增 `reset_retry_count(state)` 具名函数 + `record` 在 `verdict != wait` 且文件缺失时 exit 2 —— 后两项即 R5 aggregate erratum 指出的「v6 已补 A2 两条」，实读确认真的补上了 |
| 4（本席） | **A3-R5-m1**（SC-15/rule6_note 未强制「两个 skill 各至少一次」证据覆盖） | R5 聚合裁定「非强制, 留 Phase B 实施时顺手 (不阻塞)」 | **not_addressed（属既定、非过失性延后）** | 逐字 grep v6 全文「各至少一次」「两个 skill」均无新增文字；SC-15 与 rule6_note 仍是 v5 原文表述。与 R5 聚合处置一致（该项明确未要求 v6 必须处理），非本轮新发现的疏漏，见下方 Verdict 残留项 |
| 4（本席） | **A3-R5-m2**（R4 聚合报告「全部吸收」措辞失实，实为 A2 两条 + A3 两条未采） | R5 聚合已在 frontmatter 写 `erratum_r4_aggregate` 勘正 | **closed** | 重新核对：R4 aggregate 原文「全部吸收 (A3「禁人工模拟 CLI 序列」不采, 低优先级)」暗示仅 1 条未采；实读 A2-R4 报告确认 A2-R4-m1（record 非-wait+文件缺失未定义）与 A2-R4-m2（reset --retry-count 无具名函数）在 v5 中确未处理，A2 自己在 R5 报告里也独立指出（A2-R5-m2/m3，均标 not_addressed），与我 R5 报告的发现相互印证、非同源重复；R5 聚合的 `erratum_r4_aggregate` 字段文字「实际 A2-R4-m1/m2 两条与 A3 两条未采」经交叉验证**准确**；且 v6 确实已补上 A2 的两条（见簇 3），勘正闭环 |

## v6 相对 v5 的 13 处 diff — 稳定性/新矛盾核查

逐处对照 baseline 代码重新验证，未发现新引入的假绿、fail-open 或契约破坏：

- **SC-13 地点变更**：与真实两份 workflow 文件交叉验证，可行（见簇 1）。
- **§3.2 步骤 2 + 3c′ 显式 `--state-file`**：两处调用行文本均已加，无遗漏第三处（步骤 3d 的 CLI reset 调用未提及 `--state-file`，但该行紧邻 3c′ 且未改变既有「同 3c′ 全旗标」引用关系，非新引入的不一致——3d 的 reset 调用理应继承同一 state-file 参数，spec 行文未逐字重复但未产生歧义空间）。
- **SC-5 (c)(d)**：新断言精确覆盖 `gate_check` 真实回填代码路径（见簇 2），且与 SC-10 的 verify-failed 场景不重复冲突——SC-10 验证的是 `_verify_branch_exists` 返回值消歧的通用行为（`assert_not_called`、旧名包装兼容），SC-5(d) 验证的是回填后消息内容与副本通道细节，二者互补非矛盾。
- **§2.3「六个 (八变体)」+ `<owner>/<repo>` + branches 第三成因**：实读 `gate_check` 逐个早退分支（`enabled:false`/`no-backend`/`precheck`/`main 核验`两 kind/`(b)` 腿/`(a)` 腿）精确数出 6 个 return 点、8 个变体，与 v6 SC-7 文字逐字吻合；`<owner>/<repo>` 占位替换与 `.format` 禁用理由句自洽（message 模板内含 JSON 花括号，若用 `str.format` 会与 JSON 体本身的 `{}` 冲突，这是真实的 Python 陷阱，非臆造理由）。
- **§3.1 reset 语义 + record 缺失文件**：`reset_retry_count(state)` 新具名函数与 `reset_no_run_observations` 对称；`record` 在 `verdict != wait` 且文件缺失时 exit 2，与 §3.2 步骤 2「首个 wait verdict 才建骨架」的调用序列不变量吻合，不产生新的未定义行为窗口。
- **R-e**：与 §3.2 3d 逐字一致，无残留矛盾（R4 A4-m4 指出的原不一致已消除）。

## SC-1~16 整体自洽复验

- 重新走查 `compute_verdict:174-233` 真实 elif 链（`failing/error` → `pending` → `not_applicable` → `main_in_flight_runs` → 兜底 `green`），确认 v6 §2.2 要求的插入点（`not_applicable` 之后、`main_in_flight_runs` 之前）与真实代码结构精确匹配，SC-2/SC-4 的红窗声明（基线 `[] → fallthrough green`）成立不变。
- `path_coverage.py:36`「共 9 个」勘正为 8：实读 docstring 规则 1-8，其中规则 5（逐 workflow 解析）明确「中间步骤, 不产终态」不贡献 reason 字符串，故 7 条终态规则 + 1 个横切 `internal-error` = 8，原「9」确系计数错误（把不产生 reason 的规则 5 也计入了）。v6 的勘正是真实修正，非引入新错误。
- `_result()` 调用点实测 9 处（`:422/432/447/459/464/468/493/498/506`），仅规则 6（`:493`，`workflow-trigger-matched`，持有 `matched` 变量）符合「传 matched 子集」的落点要求，其余 8 处不变——与 v6 §4「仅规则 6 调用点传 matched 子集, 其余 8 处不改」逐字吻合。
- `DEFAULT_CONFIG` 现状 `:57-69`、`config.template.json` 现状 `:73-91`（两个新 key 均缺，含 #122 遗留的 `path_coverage_enabled`）、`.gitignore:19-21`（现有 3 个 telemetry 分区）、`_build_output` 现状已支持 `gate_error` additive 键——均与 v6 引用的行号/事实逐字对应，无脱靶引用。
- rule6_note 的 AB 覆盖数字重新实测：`phase-c-integrator.json` 3 evals、`workflow-runner.json` 2 evals、`phase-c-integrator-pre-merge-gate.json` 7 fixtures（`green/NEG-1/NEG-2/wait_then_green/fail/wait/NEG-3`），与 v6 文字「3 evals / 7 fixtures / 2 evals」完全一致；`NEG-3` 元键集实测 8 键，`wait_then_green._consumed_by` 现状确为「no consumer」——均非臆测引用。
- 条件 scope 组（`dispatch_viable=false` 时 §4 整段 + SC-8 + SC-9 dispatch 部分 + `DISPATCH_VIABLE` 常量 + §2.3 dispatch 渲染句 + SC-2 dispatch 子项 + 3.3(a) 行一并删除）内部列举完整，逐条核对确认没有遗漏「删了常量但留了消费点」或反向遗漏。

## 新 Findings

无新增 Critical / Major。唯一残留是延续性 Minor（非本轮新发现，见下）。

## Verdict

**PASS**（0 Critical / 0 Major / 1 Minor）。

- v6 相对 v5 的全部 2 条 Major 簇（A1-R5-M1 SC-13 地点、A2-R5-M1 回填零 SC）与残留簇（A1/A4/A2 共 6+ 条 minor）经独立实读代码/文档/AB fixture 源头核验，**全部 closed**，证据在 baseline `400f0bc` 或 v6 正文中真实存在，非纸面自证；R4→R5 聚合报告的一处失实（「全部吸收」措辞）已被 R5 aggregate 的 `erratum_r4_aggregate` 字段准确勘正，且 v6 确认已补上被遗漏的 A2 两条。
- 逐条重新走查 v6 相对 v5 的 13 处 diff 与 SC-1~16 全集，未发现新引入的假绿、fail-open、契约破坏，或「两实施者必然分叉且无 SC 能区分」的末轮 Major 门槛问题。核心正确性主张（compute_verdict elif 插入点、六点八变体、path_coverage reason 计数勘正、`_result()` 调用点分布、AB 套件覆盖数字）逐一在真实代码/配置文件上重新验证，均与 v6 文字精确对应。
- 残留 1 条 Minor（A3-R5-m1，SC-15/rule6_note 未强制「两个 skill 各至少一次」证据覆盖）：R5 聚合已明确裁定为「非强制, 留 Phase B 实施时顺手, 不阻塞」，本轮未见新处理也未见新恶化，维持既定非阻塞延后，不影响本轮门槛判定。
- v6 可批准进 A.2。

vote: **PASS**
