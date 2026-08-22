---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T06:25:14.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 0
major_count: 3
minor_count: 3
---

## 摘要

对 `pre-merge-gate-no-run-for-branch` proposal.md 做 QA 透镜复核, 基线 aria @ `400f0bc`。**实读代码 + 实跑基线** (非仅读 spec 文本): SC-1/SC-2/SC-4/SC-6 的「基线红/绿」标注均**核实为真** —— 尤其 SC-2 声称的「`compute_verdict([], "not_found")` 基线恒 fallthrough 到 `green`」经直接调用复现, 这是 §1 与 §2 必须同 commit 落地的核心论据, 属实。SC-6 的「坏实现会红」用一个真实的 mutation-test (模拟「加新分支时手滑漏写 `return`」这一常见重构失误) 验证, 确认能被 `query_pr_ci.assert_not_called()` 抓到。

发现三类 Major: (1) §3 workflow_dispatch 处方在「dispatch 成功但 run 排队未被领走」场景下**没有幂等/去重护栏**, 而这恰是本 spec 自己在 Why 里点名的 `/actions/tasks` 语义盲区, 治病的手在同一个盲区里可能反复开同一味药; (2) `rule6_note` 把 §3 的处方性指令面判进「照跑 AB, 零裁量」, 但实查三份被点名的 AB 资产 (`phase-c-integrator.json` 3 evals / `phase-c-integrator-pre-merge-gate.json` 7 fixtures / `workflow-runner.json` 2 evals) **无一触及** `not_found`/`no-run-for-branch`/`wait_recoverable` 2.5 分支, 且同一 fixture 目录里 `NEG-3-internal-error-surface` (#126) 自己的 `_description` 字段明文记录了「既有 6 fixture 结构上碰不到新分支」正是走 Rule #6 判据表**第三行**(定向 fixture + 套件缺口 issue) 处理的先例 —— 本 spec 引 #122 而非这个更贴切的姊妹先例, 分类站不住; (3) AD-4 的 90s 升级阈值经验依据薄, SC-13 活体只验结构性一侧, spec 自己承认 (R-b) 但未给出可执行的补充观测方案, 已按要求补一份。

三类 Minor 为措辞/引用层面的不精确 (reason 封闭集「8 vs 9」计数遗留自基线文档本身的旧误差、fixture 数量引用过期、`_result()` 签名段落自相矛盾但会被 SC-9 兜底发红)。

0 Critical: 未发现「按 spec 实施会让 merge 在未经真实 CI 的情况下变绿」这类 fail-open。核心 fallthrough-green 缺陷 (F1/AD-2 描述的那个) 被 §1+§2 同 commit 的硬约束正确堵死, 且 SC-2/SC-4 的断言组合确实能钉住这一点。

## Findings

### [A3-M1] Major — workflow_dispatch 处方缺幂等/去重护栏, 恰踩中本 spec 自己诊断的盲区

**锚点**: proposal.md §3 (处方 1) + AD-5 + Risks R-c; `workflow-runner/SKILL.md §wait_recoverable` Exit conditions 2.5 (新增, "触发后回到 wait_recoverable 循环, retry_count 归零")。

**问题**: Why 部分「附」明确指出 backend 查询的 `/actions/tasks` **只列已被 runner 领走的任务**, 所以「零 run」有两种来源: 结构性零覆盖 / **run 已建但尚未被领** (瞬态)。这正是 AD-2 拒绝 `fail`、改用「重复观测 + 阈值」判别的理由。但 §3 处方逻辑对这两种来源**完全同构地反应**: 只要连续 2 次重查仍是 `not_found` (默认 ~90s), 就执行 `workflow_dispatch`, 然后把 `retry_count` 归零重新计时。问题在于: 如果 dispatch 已经成功把一个 run 排进队列, 但 runner 忙 (heavy 节点被本 Lab 自己的其它容器占满是本项目「项目状态」段落里正在发生的常态, 而非假设), 那个排队中的 run **同样不会出现在 `/actions/tasks`**, gate 仍然报 `not_found`。于是下一轮 (~90-180s 后) `retry_count` 再次达到阈值, `path_coverage.dispatchable_workflows` 依旧非空 (同一 diff、同一 workflow 文件), 处方 1 会**对同一分支同一 workflow 再发一次 `workflow_dispatch`** —— 治盲区的手, 落进了同一个盲区。

按 spec 逐字实施, 这不是实现者可能犯的错, 而是**设计本身在描述的条件下必然复现**的行为: `gate_state` 新增字段只有 `gate_error_kind` (string|null), 没有任何「本轮等待期间是否已发过 dispatch」的记忆; Out of Scope 明确把「gate 跨调用记忆」推给 workflow-runner 的 `gate_state`, 但 `gate_state` 的 additive 字段清单里没有这个记忆位。

**影响范围有限但真实**: 上层 `wait_timeout_seconds`(默认 1800s) 仍会兜底, 所以不是无限风暴 —— 但在一个 30 分钟窗口内, 若 runner 持续拥堵, 理论上可对同一分支重复 dispatch 多达 ~10-20 次 (1800s / ~90-180s), 造成 CI 资源浪费、可能的并发 run 互相干扰、以及 report 里对 owner 呈现「已处方」但实际重复执行的噪声。Risks R-c 只覆盖了「dispatch 调用本身失败 (token scope) → fall through 处方 2」, 没有覆盖「dispatch 调用成功但 run 未及时被领 → 是否该再发一次」这一支, 这正是本审计被要求重点核查的「dispatch 成功但 runner 不领」场景。

**实测证据**: 代码读证实 backend 归一化逻辑 (`aether.py:216-233`) 与 gate 输出 (`pre_merge_gate.py`) 在 `not_found` 状态下不携带任何「上次是否已 dispatch」的信号; `evaluate_path_coverage` 是无状态纯函数, 同一 diff 每次调用都会重新算出同样的 `dispatchable_workflows`; `workflow-runner/SKILL.md:307-360` 现有 `gate_state` schema (读取确认, 无 dispatch 相关字段)。

**建议**: `gate_state` additive 字段加一个去重信号, 例如 `dispatch_attempted_at: str|null` 或 `dispatch_count: int` (workflow-runner 侧维护, gate 保持无状态的既有原则不必打破), 2.5 exit condition 改为「`gate_error.kind==no-run-for-branch AND retry_count>=threshold AND (dispatch_attempted_at is null OR now - dispatch_attempted_at > 冷却期)`」再执行处方 1; 冷却期建议不小于 `wait_check_intervals` 的量级 (例如 300s), 避免同一等待周期内重复触发。若 owner 认为 ~10 次量级的重复在可接受范围内, 也应在 Risks 里显式记录这一权衡, 而不是留空。

---

### [A3-M2] Major — `rule6_note` 把 §3 处方性指令面误判进「照跑 AB, 零裁量」; 三份被点名的 AB 资产实测均测不到新行为, 且同目录已有姊妹先例本该走第三行

**锚点**: proposal.md `## rule6_note` 第一条; `standards/conventions/skill-benchmark-exemption.md` §1-§3 判据表; `aria-plugin-benchmarks/ab-suite/phase-c-integrator.json` / `phase-c-integrator-pre-merge-gate.json` / `workflow-runner.json`。

**问题**: `rule6_note` 判 §3 (`SKILL.md §C.2.4` 步骤 5/6 处方 + `workflow-runner/SKILL.md §wait_recoverable` 2.5) 为「处方性 · 运行时指令面 → 判据表第二行, 照跑 AB, 零裁量」, 并引「与 #122 (v1.65.0) 同款先例」。实测三份被点名要跑的 AB 资产内容:

- `phase-c-integrator.json`: 3 个 eval, 场景为 commit-generation / merge-conflict-handling / multi-remote-merge-push, **无一涉及 pre_merge_gate 输出或 wait 路由**。
- `phase-c-integrator-pre-merge-gate.json`: 当前**7 个** fixture (`green` / `wait` / `wait_then_green` / `fail` / `NEG-1-malformed` / `NEG-2-timeout` / `NEG-3-internal-error-surface`), 无一 `pr_ci_status` 或 `gate_error.kind` 涉及 `not_found` / `no-run-for-branch`。且该文件的 `_consumed_by` 字段大多引用一个**已被本仓自己勘正过的旧误传** (`ARIA_AETHER_MOCK_RESPONSE_FILE` 从未真实存在, 见 `openspec/changes/phase-c-integrator-ci-path-coverage/proposal.md:419` 与 `ab-results/2026-05-10-.../benchmark.md:70` 的明文勘误) —— 这 7 个条目里, 6 个 (green/wait/wait_then_green/fail/NEG-1/NEG-2) 本质是**指向真实 pytest 单测的人类参照文档**, 真正带 `_target_behavior` / `_discriminating_question` / `_arm_expectations` (with_skill vs without_skill) 这套**活体 AI 行为评测字段**的只有 `NEG-3-internal-error-surface` 一条。
- `workflow-runner.json`: 2 个 eval (完整十步循环 / 跳过 Phase A), 同样不涉及 wait_recoverable 的 exit condition 判定。

更关键的是: `NEG-3-internal-error-surface.json` 的 `_description` 字段**逐字写着**「既有 6 个 fixture (green / wait / wait_then_green / fail / NEG-1 / NEG-2) 结构上都碰不到 path_coverage 的 unknown 分支 ... 本 fixture 补这个缺口」, `purpose` 字段直接引用「Rule #6 判据表第三行第 2 条义务: 定向可证伪 fixture」。这是与本 spec **同一份 SKILL、同一个 fixture 目录**里对「既有 AB 套件结构上碰不到新分支」这一完全同构情形的**真实处置先例** —— 它选的是判据表第三行 (点名行为 + 建定向 fixture + 记套件缺口 issue), 不是第二行「照跑」。本 spec 引 #122 作为「同款先例」而不引这个在同一文件里、时间上更近、行为形态更相似 (都是「gate 输出新增一种 AI 需要识别并区别对待的状态」) 的 #126/NEG-3 先例, 分类依据选错了参照系 (memory `feedback_spec_precedent_verify_execution_history` 命中: 先例引用需核验真实执行史, #122 本身是否真的「同款」未被验证, 而更贴切的 #126 先例反而指向相反结论)。

若按 spec 字面执行 (「照跑 AB」= 重跑现有 12 个 eval/fixture 交叉引用的确定性单测), 结果会是全绿 —— 但这全绿**证明不了**「AI 在收到 `gate_error.kind=no-run-for-branch` 时会 surface 正确文案、并在 retry_count≥2 后真的执行处方而非继续写『CI pending, 等待中』然后干等 1800s」这件事, 因为没有任何 fixture 呈现过这个状态。这正是 `skill-benchmark-exemption.md` §3 末尾警告的「测量剧场」—— 无论跑几遍都不构成证据, 还会让人误以为验过了。

**实测证据**: 见上文枚举; 三文件全内容已逐条读取比对 (`python3 -c "json.load(...)"` 遍历 `evals`/`fixtures` 字段)。

**建议**: 补一条形如 `NEG-3` 的定向 fixture (例如 `no-run-for-branch.json`), 至少含 `_target_behavior`(AI 收到 `gate_error.kind=no-run-for-branch` 后应 surface 该 message、不得写通用「CI pending」、且在 `gate_state.retry_count>=no_run_escalation_retries` 时应描述/执行处方而非继续等待)、`_discriminating_question`、`_arm_expectations`; 按 §3 三条义务补齐: 点名行为 + 该 fixture 可证伪 (回退本 spec 后, 该 fixture 对应断言必须转红) + 若暂不补则开 issue 记「套件缺口」。`rule6_note` 改为第三行处置, 而非声称「零裁量照跑」。

---

### [A3-M3] Major — AD-4 阈值 (2 次/~90s) 经验依据薄, SC-13 只验结构性一侧; 补一份可执行的观测方案

**锚点**: proposal.md AD-4; Risks R-b; SC-13。

**问题**: AD-4 自陈依据是「只有 #152 一次现场 + runner 领任务秒级的常识」, R-b 也承认「阈值 2 次的经验依据薄」。SC-13 的活体验证设计 (「起一条新分支 push path-matched 变更 → 首次 gate 应为 `not_found` → `workflow_dispatch` → 再跑 gate → `passing/pending`」) 只证明了「结构性零 run (Forgejo 新分支首推不评 paths)」这一侧确实存在且会被正确显影, **没有**证明「阈值设 2 (~90s) 不会把仍在排队的瞬态 run 误判成需要升级处方」这一侧 —— 而后者恰恰是 AD-2 引入「重复观测」机制要防的假红/误处方场景, 也是 A3-M1 的风暴风险的直接放大器 (阈值越低, 处方越容易在真正只是排队慢的场景下被多次触发)。

**这个阈值可被一次观测推翻**: 若在集群较忙时段 (本项目 CLAUDE.md「项目状态」段落自陈的 168h 自主跑 + Luxeno 45-54s 延迟等拥堵迹象已是常态) 真实测得 runner 从 push 到被 `/actions/tasks` 领走的中位/尾部延迟超过 90s, AD-4 的默认值即被证伪, 且会直接放大 A3-M1 的重复 dispatch 频率。

**建议 (可执行, 不要求本 spec 必做, 但应可证伪)**:
1. 在现有 Forgejo 上做一次侧信道观测: 连续 N (≥10) 次对一个 path-matched 分支做空提交/真实提交, 用 `date +%s` 记录 push 完成时刻, 轮询 `aether ci status --branch <b> --json` 直到 `runs` 非空, 记录 Δt 分布 (p50/p90/max)。若 p90 显著 > 90s, 应把 `no_run_escalation_retries` 默认值提到能覆盖 p90 的档位 (spec AD-4 已预留 3 作为候选)。
2. 更廉价的替代: 抓取 aether-runner 侧现有的历史 job 日志 (若 Aether 侧已落盘 queued_at/started_at), 离线统计同一分布, 不需要真实占用集群。
3. 无论采用哪种, 结果 (哪怕是「p90=12s, 阈值 2 次绰绰有余」的正面结果) 应作为 AD-4 的经验依据写入 spec 或 handoff, 替换当前「常识」措辞, 否则该假设会一直悬空到下次真实事故才被验证。

**实测证据**: `docs/handoff/2026-08-20-issue-batch-181-147-145-ship-and-gate-blindspot.md` 全文搜索, 仅有定性描述 (「`/actions/tasks` 只列已被领走的任务」), 无任何延迟量化数据; `aria/skills/phase-c-integrator/SKILL.md` / `pre_merge_gate.py` 亦无相关埋点。

---

### [A3-m1] Minor — SC-9「8 个」与「参数化全 9 reason」的自相矛盾, 溯源到 `path_coverage.py` 自身既有的计数误差

**锚点**: proposal.md SC-9; `path_coverage.py:36` (「⇒ 终态 reason 封闭集共 9 个」)。

**问题**: 实读 `path_coverage.py` 判定规则 1-8 + 横切 internal-error, 实际互斥终态 reason 前缀只有 **8 个**: `git-diff-failed` / `empty-diff` / `workflow-files-changed` / `no-workflow-files` / `workflow-trigger-matched` / `workflow-parse-failed` / `no-triggering-paths` / `internal-error`。`test_path_coverage.py` 里对 `reason` 的断言 (全文 grep) 也确实只覆盖这 8 个前缀, 没有第 9 个。但模块自己的 docstring (`:36`) 写「封闭集共 9 个」, 本 spec 的 SC-9 同时写「其余 **8** 个终态 reason 下恒 `[]`」和「参数化全 **9** reason」——两个数字在同一行自相矛盾, 且都不是本 spec 引入的新问题 (baseline docstring 的「9」本身就与代码对不上), 但 SC-9 照抄了这个已有偏差而未澄清。

**建议**: 澄清 SC-9 的「9」是否指「8 个 reason 标签 + `workflow-trigger-matched` 的 dispatchable/non-dispatchable 两个子变体 = 9 组参数化 case」, 若是则明确写出来; 若只是笔误应改成「8」并顺手在 `path_coverage.py:36` 留一条勘正 (描述性, substitute 覆盖, 不需要额外 AB)。不影响任何断言的可执行性, 纯措辞层面。

---

### [A3-m2] Minor — `rule6_note` 引用的 fixture 数「6」已过期, 当前基线实为 7

**锚点**: proposal.md `## rule6_note`; `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json`。

**问题**: `rule6_note` 写「`phase-c-integrator-pre-merge-gate.json` (6 fixtures)」。实读该文件 `fixtures` 数组当前长度为 **7** (`NEG-3-internal-error-surface` 已于 #126/v1.65.3 加入, 早于本 spec 基线冻结的 `400f0bc`)。「6」是 #126 之前的历史数字, `NEG-3` 自己的 `_description` 字段里也写着「既有 6 个 fixture」(指 NEG-3 加入前的状态), 本 spec 抄了这个历史基数而非当前基线的真实计数。

**建议**: 改成「7 fixtures」。此项本身不影响 A3-M2 的结论 (无论 6 还是 7, 都不含 `not_found` 场景), 但反映了「照抄」而非「对当前基线重新点数」的痕迹, 建议顺手核对整份 spec 里其它引用既有资产数量的地方 (如有)。

---

### [A3-m3] Minor — §4 `_result()` 签名段「既有调用点不改」字面与 SC-9 要求矛盾, 但会被测试兜底发红而非静默错误

**锚点**: proposal.md §4 (`path_coverage 附带: dispatchable_workflows[]`); `path_coverage.py:494` (`workflow-trigger-matched` 的 `_result(...)` 调用点)。

**问题**: §4 原文「`_result()` 签名加可选参数, 默认 `[]`, 既有调用点不改」。字面读法会让实现者以为**所有**现存 8 处 `_result(...)` 调用都不用碰。但 SC-9 明确要求「在 matched 且 dispatchable → `dispatchable_workflows == matched 子集`」——这必然要求 `:494` 这一个调用点 (`workflow-trigger-matched` 分支) 被**修改**为计算并传入实际子集, 否则该分支恒回落到默认值 `[]`, SC-9 直接断言失败。「既有调用点不改」与「SC-9 要求 `:494` 改」在字面上冲突。

**好消息**: 这个歧义是**自纠正**的 —— 实现者若真的一字不改地保留全部 8 个调用点, SC-9 会在第一时间跑红 (不是静默通过), 不构成「测试假绿」风险, 故判 Minor 而非 Major。

**建议**: 把「既有调用点不改」改成更精确的表述, 例如「`workflow-trigger-matched` 分支 (:494) 需新增计算逻辑并传入该参数; 其余 7 个终态调用点保持默认 `[]` 不改」, 消除歧义, 省掉实现者读两遍才能发现矛盾的成本。

## 未发现问题但已核验的点

- **SC-1 基线红**: 直接调用 `AetherBackend._normalize_pr_ci_status([])` 实测返回 `"pending"`, 与 spec 声称一致 (:363 `test_empty_runs_pending` 即为待翻转断言)。
- **SC-2 基线红 (核心论据)**: 直接调用 `compute_verdict([], "not_found")` 实测返回 `{"verdict": "green", ...}`, 证实 §1 若单独落地会把「盲区」从「恒 wait」变成「恒 green」(比现状更坏的 fail-open), `raw_message` 为空字符串, 与 spec §1 加粗警示逐字吻合。
- **SC-4 基线红**: 直接调用 `compute_verdict([{"id":1}], "not_found")` 实测返回 `verdict="wait"` (因 `main_in_flight_runs` 非空触发既有 `elif` 分支), 但**不带**任何 `gate_error`/`kind` —— SC-4 若断言 `gate_error.kind` 会失败, 确认为红, 且证实这是「侥幸撞对 wait」而非「有意识识别 not_found」, 与 AD-2 的论证方向一致。
- **SC-6 可证伪性 (mutation test)**: 构造了一个真实的「坏实现」变体 —— 模拟实现者在 `not_applicable` 分支旁边加 `not_found` 分支时手滑漏写 `return` (一个非常真实的重构失误形状, 与 memory `fix_the_class_not_the_instance` 描述的失误类型吻合) —— 实测该变体确实会调用 `query_pr_ci` (`mock_backend.query_pr_ci.called == True`) 且把 `verdict` 静默改写成 `green`, 证明 `assert_not_called()` + 输出无 `gate_error` 这两条断言组合是真正有区分力的, 不是恒真断言。
- **not_applicable 结构性不可达性**: 实读 `gate_check` 源码 (`:498-509`) 确认 `not_applicable` 分支在 `query_pr_ci` 调用点 (`:509`) **之前**就 `return`, 与 SC-6 的「结构上不可达」描述一致。
- **R-a (`gate_error` 零外部消费方)**: 全仓 grep (排除 gate 自身/tests/本 spec/ab-workspace 与 ab-results 历史产物) 后, `gate_error` 唯一命中于 `phase-c-integrator/SKILL.md` 自身、`CHANGELOG.md`、以及历史 `.aria/audit-reports/`/`openspec/archive/` 文档; **`workflow-runner/SKILL.md` 全文对 `gate_error` 零命中** —— 证实「gate_error 在场 ⇒ fail」的假设目前只存在于 `phase-c-integrator/SKILL.md:290` 一处文字, R-a 的「零外部消费方」判断属实。
- **回归面 — 「空 runs → pending」隐式依赖排查**: 全文 grep `pr_state="pending"` / `main_runs=[]` / `_aether_payload([])`, 确认 `test_pre_merge_gate.py` 里所有 `gate_check` 级测试 (含 `test_case_d_pending_routes_wait`) 都通过 `_make_aether_backend_mock` 直接构造 `CIStatus(state=pr_state)`, **绕过**了真实的 `_normalize_pr_ci_status`, 不受 SC-1 翻转影响; 唯一直接调用真实 `_normalize_pr_ci_status([])` 的断言就是 `:363`, 与 spec 声称的「红窗范围」一致, 未发现额外隐藏回归面。
- **AB fixture 语义核实**: 顺带发现并核实了 `phase-c-integrator-pre-merge-gate.json` 系列 fixture 的 `_consumed_by` 字段大多引用一个本仓已自我勘正过的历史误传 (`ARIA_AETHER_MOCK_RESPONSE_FILE` 从未实现), 该背景信息被用于支撑 A3-M2, 非独立 finding。
- **path_coverage 规则 1-8 与 reason 封闭集逐字不变**: 对照 `:191-300`(`_parse_workflow`) 与 `:425-508`(`_evaluate`) 全文, 确认 §4 描述的「additive 加 dispatchable」改动不触及既有 8 条判定规则的分支条件与优先序, 与 spec「逐字不变」的承诺一致 (除 A3-m3 指出的措辞歧义外)。
- **config-loader 登记模式**: `config-loader/SKILL.md:242-283` 已有 9 个同级 `phase_c_integrator.pre_merge_gate.*` key 的登记范式, `no_run_escalation_retries` 照此模式新增, 描述性 substitute 路径可行, 无异议。

## Verdict

PASS_WITH_WARNINGS (0 Critical, 3 Major, 3 Minor)

vote: REVISE
