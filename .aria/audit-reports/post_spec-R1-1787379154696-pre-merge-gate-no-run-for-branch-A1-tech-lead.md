---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-22T06:26:40.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 1
major_count: 6
minor_count: 6
---

## 摘要

Spec 的**主干判断是对的**, 且证据链在我这一轮全部独立复跑通过: 检测落点 (AD-1 backend 归一层)、`wait` 而非 `fail`/`green` (AD-2)、复用 `gate_error` 副本通道 (AD-3)、§1/§2 同 commit 的落地顺序硬约束 —— 后者我直调核实基线 `compute_verdict([], "not_found")` 确实返 **green**, 这条硬约束是承重的且写对了。R-a / R-c 的三条探针我逐条重跑, 结论与 spec 一致。issue 原案 A 的原文我也拉下来逐字核对, spec 对它的转述**不是**稻草人。

问题集中在**处方那一侧** —— 即 spec 从「显影」跨到「自动动作」的那半:

1. **[C1]** 升级处方无「一次性」守卫且显式 `retry_count 归零` ⇒ 在 1800s 窗口内可重复触发约 8 次。runner 真停摆时 (即 #152 最初被误诊的那个世界) 这会变成每 ~210s 自动推一个 commit / 打一次 dispatch 的循环。
2. **[M1]** 「第 2 次重查 (~90s)」与判定式 `retry_count ≥ 2` 在 workflow-runner 现有递增点 (`SKILL.md:389`, schema `:121`) 下**差一**: 实际落在第 3 次重查 t≈210s。AD-4 的整个概率论证挂在 90s 上。
3. **[M2]** message 三分支以 `decision` 为键, 但 `covered` 有 **3 个 reason**; 其中两个 (`empty-diff` / `workflow-files-changed`) 的 `matched_workflows` 恒 `[]`, 模板「变更 path-matched `<matched_workflows>`」会渲染出自相矛盾的空列表。
4. **[M3]** rule6_note 选错了判据表的行: 现有 7 条 (非 spec 所写 6 条) AB fixture **结构上到不了** `pr_ci_status=not_found`; 同套件上一版先例 (#126, NEG-3) 走的正是判据表第三行「定向可证伪 fixture + 套件缺口开 issue」。照跑现有套件产出的绿对新指令面**零信息量**。
5. **[M4]** `gate_state.gate_error_kind` 产生了但 2.5 判定式不消费 —— 「有记录无路由」; 「仍为同 kind」的跨轮语义从未落进判定式。
6. **[M5]** (a) 轴缺 PR 分支存在性核验 —— #137 在 (b) 轴钉死的「空 runs 二义」在 (a) 轴以 `no-run-for-branch` 之名被误归因。
7. **[M6]** §1 对 (b) 轴写下的「空 runs = 『main 无 in-flight』是**正确语义**」与本 spec 自己引用来支撑 AD-2 的事实 (`/actions/tasks` 只列已领任务) 直接矛盾; 该矛盾遮住的是 Rule #8 (b) 腿上一个同形状的 fail-open。

Vote **REVISE**: C1 必须在 Phase B 前定死「一次性升级」语义, M1/M2 必须把判定式与 message 键钉到字符级, M3 必须改 Rule #6 申报。

---

## Findings

### [A1-C1] Critical — 升级处方缺「一次性」守卫 + `retry_count 归零` ⇒ 1800s 内可重复自动 push/dispatch 约 8 次

**锚点**
- Spec §3 (`proposal.md:81-85`): 处方优先序 1/2/3 + 「触发后回到 `wait_recoverable` 循环 (`retry_count` 归零), 后续 run 状态正常裁决」
- Spec §3 (`proposal.md:87`): workflow-runner Exit condition 2.5
- `aria/skills/workflow-runner/SKILL.md:332-336` (Exit conditions first-match-wins), `:347` (`wait_check_intervals[min(retry_count, len-1)]`), `:389` (`wait` → 增量更新 `retry_count`)
- `aria/skills/phase-c-integrator/SKILL.md:51` (`wait_check_intervals=[30,60,120,300,300]`), `:50` (`wait_timeout_seconds=1800`)

**问题**
2.5 的判定式是 `gate_error.kind == no-run-for-branch AND retry_count ≥ no_run_escalation_retries`。处方执行完后 spec 明确要求 `retry_count` **归零**并回到同一个 polling loop。于是判定式的输入被复位, 而它的**前件 (`kind` 仍是 `no-run-for-branch`) 在处方没有真正造出 task 的世界里保持为真** —— 判定式因此会**再次成立**。spec 全文没有任何「本 episode 只升级一次」的状态位, `Out of Scope` 还把「gate 跨调用记忆」明确排除, 而 workflow-runner 侧只加了 `gate_error_kind` (一个 kind 字面量), 没有加「已升级过」的标记。

唯一的上界是 exit condition 2 的 `elapsed > wait_timeout_seconds` (1800s, 且 `started_at` 不随 `retry_count` 归零而重置 —— 这点 spec 也没写, 只是恰好没写要重置)。按 §3 的三条处方分别推演:

- **处方 1 (dispatch)**: runner 活着 → 造出 task → 下一轮 `pending`, 收敛。runner 停摆 → ActionRun 建了但无 runner 领取 ⇒ `/actions/tasks` 仍空 ⇒ `not_found` ⇒ 再次升级 ⇒ **再 dispatch**。
- **处方 2 (推实质 commit)**: 同理; runner 停摆时**每个升级周期推一个 commit**。这是外向且难撤销的动作 (aria-plugin 是双 remote 镜像仓, commit 会被推到 Forgejo + GitHub 两侧)。
- **处方 3 (提示 owner)**: 这一条是安全的 (owner 门), 但它只在 1、2 都做不了时才到达。

**按 spec 实施会怎样错**: 在「runner 真停摆」这个世界 —— 也就是 #152 现场最初被误诊成的那个世界 —— AI 会在 30 分钟里对 feature 分支执行约 8 次自动写动作。周期 = intervals[0]+[1]+[2] ≈ 210s (见 A1-M1 的递增点推演), (1800−210)/210 ≈ 7.6。若 M1 按「90s」那侧解, 周期 90s ⇒ ~19 次。处方 2 尤其糟: spec 的文案是「推一个**碰 matched path 的实质 commit** (如该分支本该带的回归测试)」—— 第一次还有真东西可推, 第 2..8 次没有, AI 只能造噪声 commit, 而 spec 又同时「**禁**空 commit」, 把它推向更坏的选择 (伪造改动)。

**实测证据**
- 读 `aria/skills/workflow-runner/SKILL.md:332-336` 确认 exit conditions 只有 4 条, `elapsed > wait_timeout_seconds` 是唯一时间上界; 无任何 per-episode 动作计数。
- 读 `references/workflow-state-schema.md:110-131` 确认 `gate_state` 字段集 (name/status/started_at/retry_count/next_check_at/in_flight_runs/primitive_used/raw_message) —— 没有可承载「已升级」的槽位, spec 新增的也只有 `gate_error_kind`。
- `sed -n '81,87p' proposal.md` 逐字确认「`retry_count` 归零」且无一次性约束。
- 「dispatch 后 task 未必立刻出现」这一前提就是 spec 自己 AD-2/AD-6 立论所用的事实 (`/actions/tasks` 只列已领任务), 我在 `/home/dev/Aether/aether-cli/internal/ci/status.go:45-47` 实读确认端点确为 `/repos/{repo}/actions/tasks`, 客户端再按 branch 过滤 (`cmd/ci_status.go:119-133`)。

**建议**
1. 在 `gate_state` 加 `no_run_escalation_done: bool` (additive), 2.5 判定式改为 `kind == no-run-for-branch AND retry_count ≥ N AND NOT no_run_escalation_done`; 处方执行后置 `true`。
2. `retry_count` 归零后**若再次命中同 kind**, 直接走 exit condition 2 的 user prompt 语义 (与 timeout 同级), 而不是二次执行处方 —— 「处方做了但世界没变」本身就是「这不是 paths 过滤问题, 是 runner/基建问题」的强信号, 正是该交给人的时刻。
3. 明确写死 `started_at` 不因归零而重置 (否则连 1800s 上界都没了)。

---

### [A1-M1] Major — 「第 2 次重查 (~90s)」与 `retry_count ≥ 2` 在现有递增点下差一, 实际是第 3 次重查 (~210s); AD-4 的论证挂在 90s 上

**锚点**
- Spec §3 (`proposal.md:81`): 「在 `wait_recoverable` 第 **2** 次重查仍为同 kind 时 (默认 `no_run_escalation_retries=2`, 即 30s+60s 后) 停止等待」
- Spec AD-4 (`proposal.md:108`): 「第 2 次重查发生在 push 后 ~90s。runner 领任务通常秒级; 90s 仍零 run 时『结构性』的后验概率远高于『还在排队』」
- Spec §3 (`proposal.md:87`): 判定式 `retry_count ≥ no_run_escalation_retries`
- `aria/skills/workflow-runner/SKILL.md:255` (`retry_count: 0` 初值), `:347` (sleep = `intervals[min(retry_count, len-1)]`), `:389` (`wait` → **增量更新** `retry_count`)
- `aria/skills/workflow-runner/references/workflow-state-schema.md:121` (「Number of completed polling cycles. Starts at 0; increments per re-invoke.」)

**问题**
判定式读的是 `retry_count`, 而 `retry_count` 的语义是「**已完成**的 polling cycle 数」, 且 `:389` 明确说是在拿到 `wait` verdict **之后**才增量更新。按这个语义展开时间轴:

| 事件 | t | 判定式求值时 `retry_count` | `retry_count ≥ 2`? |
|---|---|---|---|
| 初次 gate → wait, 建 gate_state | 0 | 0 | 否 |
| 重查 #1 (sleep `intervals[0]`=30) | ≈30 | 0 → 求值后置 1 | 否 |
| 重查 #2 (sleep `intervals[1]`=60) | ≈90 | 1 → 求值后置 2 | **否** |
| 重查 #3 (sleep `intervals[2]`=120) | ≈210 | 2 | **是** |

⇒ 判定式在**第 3 次重查、t≈210s** 才成立, 不是 spec 说的第 2 次 / ~90s。

**按 spec 实施会怎样错**: 两个实施者会分叉 —— 一个照判定式字面写 (210s), 一个照 AD-4 的叙述写 (在求值前先自增, 90s)。两者都能自称遵守 spec, 而 AD-4 的**唯一**定量论证 (「runner 领任务通常秒级, 90s 后的后验概率」) 只覆盖其中一个。R-b 已经承认阈值依据薄, 现在连阈值对应的**时刻**都是两个值。此外 `no_run_escalation_retries` 这个键名 (「retries」) 与它实际计的量 (「已完成的等待周期数」) 也不同名同义, 会把分叉固化进 config 文档。

**实测证据**
- `awk 'NR>=378 && NR<=392' aria/skills/workflow-runner/SKILL.md` → `:389` 逐字为「`wait` → 增量更新 `gate_state.retry_count` + `next_check_at`,继续 polling」(即先处理 verdict, 后自增)。
- `grep -n retry_count references/workflow-state-schema.md` → `:121` 「Starts at 0; increments per re-invoke」, 与上一致。
- `phase-c-integrator/SKILL.md:51` 确认 `wait_check_intervals` 默认 `[30,60,120,300,300]`, 前三段累计 210s。

**建议**
把判定式钉到**观测次数**而不是 `retry_count`: 例如「本 wait episode 内 gate 已连续返回 `no-run-for-branch` 的**次数** (含初次) ≥ `no_run_escalation_observations`, 默认 3 (即 t≈90s: 初次 + 重查#1 + 重查#2)」。同时把 AD-4 的 90s 论证与这个计数法逐字对齐, 并给 config 键换个与量同名的名字。若坚持用 `retry_count`, 必须在 spec 里写死「求值发生在自增**之前/之后**」并同步修 AD-4 的秒数。

---

### [A1-M2] Major — message 三分支以 `decision` 为键, 但 `covered` 有 3 个 reason; 其中 2 个会渲染出自相矛盾的文案

**锚点**
- Spec §2 message 分化表 (`proposal.md:63-69`): `decision=covered` → 「变更 path-matched `<matched_workflows>` 但远端零 run …」
- Spec §2 (`proposal.md:63`): 「**三分支封闭**, 由 `path_coverage` 决定」
- `aria/skills/phase-c-integrator/scripts/path_coverage.py:460` (规则 2 `covered/empty-diff`, `matched_workflows=[]`), `:466` (规则 3 `covered/workflow-files-changed`, `matched_workflows=[]`), `:497` (规则 6 `covered/workflow-trigger-matched`, `matched_workflows=matched`)
- `path_coverage.py:33-40` 模块 docstring: reason 封闭集 9 个

**问题**
`decision == "covered"` 在判定规则里对应**三个** reason, 只有其中一个 (`workflow-trigger-matched`) 会填 `matched_workflows`:

| reason | 触发条件 | `matched_workflows` |
|---|---|---|
| `empty-diff` (规则 2) | `main...pr` 三点 diff 为空 | `[]` |
| `workflow-files-changed` (规则 3) | 变更含 `.forgejo/.gitea/.github` 下文件 | `[]` |
| `workflow-trigger-matched` (规则 6) | 真有 workflow 命中 | 非空 |

spec 的 `covered` 文案模板写死了「变更 path-matched `<matched_workflows>`」。

**按 spec 实施会怎样错**:
- `empty-diff` × 零 run: 输出「变更 path-matched `[]` 但远端零 run — 符合 aria-plugin#152 (新分支首推 × paths 过滤)」。**没有任何变更**却断言 path-matched, 并把病因指向 #152。随后处方 2 要求「推一个碰 matched path 的实质 commit」—— 没有 matched path 可碰。
- `workflow-files-changed` × 零 run: 同样渲染空列表。这个组合还**恰恰是本 spec 自己会命中的形状** (改 `.forgejo/workflows/*` 的 PR 首推), 届时 gate 会对自己吐出一条自相矛盾的诊断。
- 三分支表因此**不封闭**: `decision` 不是判别 message 的充分变量, `reason` 才是。这是欠定 —— 一个实施者会按 `decision` 写 (踩上面两个坑), 另一个会按 `reason` 写 (三档变五档), SC-2/SC-3 都测不出差别 (它们只钉 `covered_pc` 与 `unknown`/`None`)。

**实测证据**
- 实读 `path_coverage.py::_evaluate` 全部 8 条规则 + `_result()` 签名 (`:63-77`), 确认只有规则 6 传 `matched`; 规则 2/3 传 `[]`。
- 实读模块 docstring `:23-40`, 确认 reason 封闭集 9 个、`covered` 占 3 个。

**建议**
message 键改为 `reason` (至少把 `covered` 拆成「有 matched (规则 6)」与「covered 但无 matched (规则 2/3)」两档), 并对应扩 SC-2/SC-3 的参数化到全部 9 个 reason —— §4 的 SC-9 已经在对 9 个 reason 做参数化, message 侧沿用同一张表即可, 成本很低。另: `empty-diff × not_found` 值得单独想一下语义 (空 diff 本就没东西可跑, 硬套 #152 处方是错的)。

---

### [A1-M3] Major — rule6_note 选错判据表的行, 且 fixture 数写错; 现有套件结构上到不了 `not_found`, 同套件先例 (#126) 走的正是第三行

**锚点**
- Spec `## rule6_note` (`proposal.md:139`): 「**处方性·运行时指令面** … → 判据表第二行, **照跑 AB**: `ab-suite/phase-c-integrator.json` + `phase-c-integrator-pre-merge-gate.json` (**6 fixtures**) + `workflow-runner.json`; 与 #122 (v1.65.0) 同款先例, **零裁量**」
- `CLAUDE.md` 规则 #6 判据表第三行: 「处方性 · 套件覆盖外 — 不能 [AB 测得到] — 点名行为 + 建可证伪定向 fixture + 套件缺口开 issue (缺一照跑)」
- `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json`

**问题**
我把这个套件打开逐条读了。它是 **7** 条 fixture, 不是 6: `green` / `wait` / `wait_then_green` / `fail` / `NEG-1-malformed` / `NEG-2-timeout` / `NEG-3-internal-error-surface`。而且第 7 条的 `purpose` 字段逐字写着:

> 「aria-plugin #126 — D9 surface 的 reason 分档措辞。**既有 6 fixture 结构上碰不到 path_coverage unknown 分支** (Rule #6 判据表**第三行**第 2 条义务: 定向可证伪 fixture)」

也就是说: **同一个套件、上一个版本、同一位起草人已经就「新分支现有 fixture 碰不到」这件事走过一次判据表第三行, 并因此加了第 7 条**。本 spec 引用了 #126 (Cross-references 里写「`internal-error` 自成一档的可辨性原则」), 却没有继承它的 Rule #6 处置。

前 4 条 fixture 全部通过 mock 的 main in-flight runs + PR CI status 驱动 verdict; NEG-1/2 走 malformed/timeout; NEG-3 走 path_coverage unknown。**没有任何一条能让 `pr_ci_status` 取到 `not_found`** —— 在基线里这个值根本没有生产者 (spec F2 自己说的「让这个槽位第一次有生产者」)。

**按 spec 实施会怎样错**: 照 rule6_note 执行 = 跑 7 条碰不到新分支的 fixture, 拿到一个绿。这个绿只证明「旧行为没退化」, 对 §3 新增的 surface 义务与升级处方**零信息量** —— 正是 memory `false_green_dual_is_permanent_red` 与 `mechanization_knob_must_match_granularity` 说的形状。更实际的后果是: 这是本变更**唯一**覆盖 §3 (AI 指令面) 的验证手段 —— SC-1~SC-13 全部只覆盖确定性代码层与 gate 输出, 没有一条能验证「AI 在第 N 次重查后真的停止等待并按优先序执行处方」。§3 因此会在**完全无验证**的情况下 ship。

**实测证据**
```
$ python3 -c "import json; d=json.load(open('aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json')); print(len(d['fixtures']));
             [print(' -', f['id']) for f in d['fixtures']]"
7
 - green / wait / wait_then_green / fail / NEG-1-malformed / NEG-2-timeout / NEG-3-internal-error-surface
```
NEG-3 的 `purpose` 字段原文见上。`primary_pass_gate_metric` = `wait_triggered_when_in_flight_mock_present` —— 度量的是 (b) 轴触发 wait, 与本变更的 (a) 轴 `not_found` 无关。

**建议**
按判据表**第三行**申报: (a) 点名新行为 —— 「gate 返 `kind=no-run-for-branch` 时 AI 必须 surface message 且在第 N 次重查后停止等待、按 1/2/3 优先序执行处方且任何路径不 green」; (b) 新增一条定向可证伪 fixture (建议 id `no-run-for-branch-escalation`, mock backend 返 `CIStatus(state="not_found")`, 期望「surface 含 #152 + 到点停止等待 + 不 green」, 并配一条「坏实现」变体: 等满 1800s 或直接 green 应判红); (c) 若不加 fixture, 按判据表「缺一照跑」照跑, 但必须在 spec 里写明「该绿不覆盖 §3」并开套件缺口 issue。顺带把 fixture 数从 6 改成 7。

---

### [A1-M4] Major — `gate_state.gate_error_kind` 产生但判定式不消费 (有记录无路由); 「仍为同 kind」的跨轮语义从未落进判定式

**锚点**
- Spec §3 (`proposal.md:87`): 「`gate_state` block additive 加 `gate_error_kind` (string|null) **便于跨轮比对「仍为同 kind」**」
- Spec §3 (`proposal.md:81`): 「在 `wait_recoverable` 第 2 次重查**仍为同 kind**时 …」
- Spec §3 (`proposal.md:87`) 判定式: `gate_error.kind == no-run-for-branch AND retry_count ≥ no_run_escalation_retries`
- Spec AD-2 (`proposal.md:106`): 「把『瞬态 vs 结构性』的判别交给**时间轴上的重复观测** (第 2 次重查仍零 run)」

**问题**
判定式的两个输入是「**本轮** gate 输出的 `gate_error.kind`」和「`retry_count`」。持久化字段 `gate_error_kind` **不在判定式里出现**, spec 也没写任何其它读它的地方。所以:

1. **有记录无路由**: 新增字段唯一被声明的用途 (跨轮比对) 没有任何消费者。memory `fix_recurs_in_its_own_fallback_path` 的第二半 (「有记录」≠「有路由」: 无人消费的诊断字段 = 静默) 正命中。
2. **AD-2 的立论与机制不匹配**: AD-2 说服 owner 选 `wait` 而非 `fail` 的核心论据是「**重复**观测」。但判定式只要求**当前**这轮是 `no-run-for-branch` + 累计等待轮数够 —— 它统计的是「等了多久」, 不是「连续几轮都零 run」。一个先因 (b) 轴 main in-flight 等了两轮 (那两轮没有 `gate_error`) 、第三轮才首次出现 `not_found` 的 PR, 会在**第一次**观测到零 run 时就立刻升级 —— 恰恰是 AD-2 说要避免的「推后第一秒判定」。

**按 spec 实施会怎样错**: 实施者会在 `gate_state` 里写一个死字段 (Rule #3 文档同步面还得为它改 `workflow-state-schema.md`), 而真正要防的「瞬态」在混合等待场景下防不住。此外由于没有任何测试能覆盖 AI 编排层, 这个缺口不会发红。

**实测证据**
- 逐字比对 `proposal.md:81` 的散文条件 (「仍为同 kind」) 与 `:87` 的机械判定式 —— 两者不同构。
- `grep -rn "gate_error" aria/` (排除 gate 自身/其 SKILL/tests) → 仅 `CHANGELOG.md:72` 一处叙述, 确认全仓无消费方 (这同时独立复核了 spec 的 R-a, 见「已核验的点」)。
- 缓解事实 (诚实标注): 我实测 `/repos/{repo}/actions/tasks` 返回的是**完整历史**而非近期窗口 (`10CG/SilkNode` returned=2458 / total_count=2458; `10CG/Aether` 1514/1514) ⇒ 一旦某分支有过 task 就不会再变回零 ⇒ 单个 wait episode 内 `not_found` 实际是**单调**的。所以现实风险低于字面 —— 但这条不变量 spec 从未写下, 判定式也不依赖它成立。

**建议**
二选一, 别两头挂: (a) 判定式真的用上持久化字段, 改成「**连续** N 轮 `gate_error_kind == no-run-for-branch`」(此时 `gate_error_kind` 有路由, AD-2 的「重复观测」也名实相符); 或 (b) 承认判定式只看当前轮 + 累计轮数, 那就**删掉** `gate_error_kind`, 并把 AD-2 的措辞从「重复观测」改成「给足够的领取时间窗」, 同时把「not_found 在 episode 内单调」写成显式不变量 (它是 (a) 成立的前提, 也是把 `/actions/tasks` 是全量历史这件事记进 traps 第六节的好理由)。

---

### [A1-M5] Major — (a) 轴缺 PR 分支存在性核验: #137 在 (b) 轴钉死的「空 runs 二义」被以 `no-run-for-branch` 之名在 (a) 轴重新误归因

**锚点**
- Spec §1 (`proposal.md:47`): 「分支存在性由 #137 的 2.2 步核验兜底」
- `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:302-352` (`_verify_main_branch_exists`), `:459-473` (调用点, 只对 `main_branch`)
- `aria/skills/phase-c-integrator/SKILL.md:248` (2.2 步, 逐字只讲 `main_branch`)
- Spec §2 message 模板 (`proposal.md:67`): 「… 符合 aria-plugin#152 (新分支首推 × paths 过滤, Forgejo 不建 run) 或 run 尚未被 runner 领走」

**问题**
`_verify_main_branch_exists` 只核验 `main_branch`, **从不核验 `pr_branch`**。而 #137 立案的原因逐字就是「backend 结构上无法区分『分支不存在』与『分支没有 in-flight run』—— 两者都产出空 runs」。本 spec 现在把 (a) 轴的空 runs **解码成一个具体病因** (「新分支首推 × paths 过滤」/「run 尚未被领」), 却没有对应的消歧步骤 —— 于是「PR 分支根本不存在 / 名字写错 / 还没 push」这第三种世界被静默归进 `no-run-for-branch`。

spec §1 那句「分支存在性由 #137 的 2.2 步核验兜底」是**不成立的**: 2.2 步的参数是 `main_branch`, 兜的是 (b) 轴。

**按 spec 实施会怎样错**:
- gate 会输出一条断言了假因的诊断 (「符合 #152」), 而真因是分支名写错 / 分支没推上去。#137 的教训是「缺省 `main` vs 本项目 `master`」—— `pre_merge_gate.py:387` 的 `main_branch` 默认值今天仍是 `"main"`, 同类打字/默认值错误在 `--pr-branch` 上一样会发生。
- 处方随后**在假因上动手**: 处方 1 对一个不存在的 ref 打 dispatch (Forgejo 会 4xx), 处方 2 要求「推一个碰 matched path 的实质 commit」到一个不存在的分支。结合 A1-C1 的重复触发, 这会变成一串失败动作。
- 这是 memory `fix_the_class_not_the_instance` 的教科书形状: #137 修了 (b) 轴那个实例, 没问「这形状还有几个兄弟位置」, 本 spec 走到 (a) 轴时正好踩上。

**实测证据**
- 实读 `pre_merge_gate.py:459-473`: 唯一调用点为 `_verify_main_branch_exists(main_branch=main_branch, remote=remote, ...)`; 全文件 `grep -n "_verify_main_branch_exists"` 只有定义与这一处。
- 实跑 `aether ci status --branch zzz-no-such-branch-152 --json` → `{"status":"ok","data":{...,"runs":[]}}` ⇒ 不存在的分支与「存在但零 run」的分支在 backend 出口处**逐字节同形**, 改成 `not_found` 后二者仍同形。

**建议**
把 `_verify_main_branch_exists` 泛化成 `_verify_branch_exists(branch, remote)` (函数体已经与 "main" 无关, 只需改名 + 文档), 在 `pr_ci_status == "not_found"` 时对 `pr_branch` 跑一次, 分两个 kind:
- 分支存在 → `no-run-for-branch` (本 spec 的语义, `wait` + 处方);
- 分支不存在 → 新 kind `pr-branch-not-found`, 建议 `verdict=fail` (与 `main-branch-not-found` 对称 —— 它是配置/输入错误, 不是可等的状态, 等下去毫无意义)。

这条同时让 `gate_error.kind` 封闭集从 3 变 4, 需要在 §2/§5 同步。若 owner 认为超出本 spec 范围, 至少要把 §1:47 那句错的兜底断言删掉, 并把这个缺口开成 issue。

---

### [A1-M6] Major — §1 对 (b) 轴的「空 runs = 正确语义」与本 spec 自己用来支撑 AD-2 的事实互相矛盾, 遮住 Rule #8 (b) 腿上同形状的 fail-open

**锚点**
- Spec §1 (`proposal.md:47`): 「**(b) 轴 `query_branch_in_flight` 不动**: 空 runs = 「main 无 in-flight」**是正确语义**」
- Spec Why 附注 (`proposal.md:35`): 「backend 所查 `/actions/tasks` **只列已被 runner 领走的任务** ⇒ 「零 run」还有第二种来源 = run 已建但尚未被领 (瞬态)。**这条决定了 AD-2 为什么不能判 `fail`**」
- Spec AD-2 (`proposal.md:106`): 「runner 忙时可达**分钟级**」
- Spec Impact (`proposal.md:116`): 「**不受影响**: (b) 轴 …」
- `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py:305-320` (`query_branch_in_flight`), `/home/dev/Aether/aether-cli/internal/ci/status.go:45-47`

**问题**
这两句不能同时为真。若「task 只在被 runner 领走后才存在」(spec 用它论证 AD-2), 那么 (b) 轴的空 runs 同样折叠了两个世界:
- main 上确实没有任何 CI 在跑 (真 clear);
- main 上刚 push、run 已建但**尚未被领** ⇒ `/actions/tasks` 不列 ⇒ backend 返空 ⇒ `in_flight_runs=[]` ⇒ 若 PR CI passing ⇒ **`verdict=green` ⇒ 立即 merge**。

第二种正是 Rule #8 (b) 腿存在的理由 (源事故: SilkNode PR-321 cancel PR-322 main CI Run #3161)。窗口宽度按 spec 自己的说法是「秒级, runner 忙时可达分钟级」。#137 的 2.2 步核验只能排除「分支不存在」, 排除不了「run 存在但没被领」—— 它查的是 `git ls-remote` 的 ref 列表, 与 task 有无无关。

**按 spec 实施会怎样错**: 缺陷本身是既存的, 本 spec 不制造它。但 spec 把它**书面判定为「正确语义」**并列进 Impact 的「不受影响」清单, 这条句子会随 §5 的文档同步面进入 SKILL.md/CHANGELOG, 成为下一个人查 Rule #8 (b) 腿时读到的 SOT。一个已知的 fail-open 被写成「正确」, 就再也不会有人去修它 —— memory `rationale_formula_contradiction_is_signal` 说的「理据↔公式矛盾时别默认公式对」正指这里, 而且这次矛盾的两端都在同一份 spec 里, 相隔 12 行。

**实测证据**
- 逐字并列 `proposal.md:35` 与 `:47`, 二者对同一个事实给出相反结论。
- 实读 `/home/dev/Aether/aether-cli/internal/ci/status.go:44-47` + `cmd/ci_status.go:119-133`: `GetRuns` 只打一次 `GET /repos/{repo}/actions/tasks`, 客户端 `filterCIRuns` 按 `r.Branch != branch` / `IsInFlight(status)` 过滤 —— (a) 与 (b) **共用同一个数据源**, 因此同一个盲区必然同时覆盖两轴。
- 我先假设「`/actions/tasks` 有分页截断会造成第三种零 run」, 实测**证伪**: `10CG/SilkNode` returned=2458 total_count=2458, `10CG/Aether` 1514/1514, `10CG/aria-plugin` 15/15 —— 无截断。故 (b) 轴的残余风险**只**来自「未被领取」这一条, 不是我最初猜的两条。

**建议**
把 §1:47 的理由改写成 scope 声明而非正确性声明, 例如: 「(b) 轴同样把『无 run』与『run 未被领』折叠, 但本 spec 不动它 —— (b) 轴没有等价的 `not_found` 出口 (空 = 判 clear = 放行, 改成 wait 会让每次 push 后的 merge 都停), 需要的是另一种消歧手段 (如查 `/actions/runs`—— 本 Forgejo 版本 404, 或读 head SHA 与 run 的对应)。已知缺口记 traps 第六节 + 开 issue。」同时把 Impact 里「不受影响: (b) 轴」改成「本 spec 不改 (b) 轴; (b) 轴的同形状盲区另案」。

---

### [A1-m1] Minor — §2 把「main 核验」列进「六键契约逐字不变」的早退分支, 与 SKILL.md:290 及自家 SC-7 冲突

**锚点**: Spec §2 (`proposal.md:74`) 「既有早退分支 (enabled:false / no-backend / precheck 失败 / backend query 失败 / **main 核验**) **六键契约逐字不变**」 vs `aria/skills/phase-c-integrator/SKILL.md:290` 「⚠️ 该早退分支**不属于**上一段那四类 —— 它是**第五类**, 且是**唯一一个不保持六键不变的** (它多一个 `gate_error`)」。

**问题**: main 核验分支输出的是**七**键 (六键 + `gate_error`), 见 `pre_merge_gate.py:459-473`。spec 自家的 SC-7 措辞是对的 (「输出**键集**逐字不变」), §2 的散文是错的。

**实测证据**: 读 `_build_output` (`:236-276`) 与 main 核验调用点 (`:464-473`), 确认传了 `gate_error=`; `test_pre_merge_gate.py:850/865/897` 断言该键在场。

**建议**: §2 改成「输出键集逐字不变 (main 核验分支仍为六键 + `gate_error`, 共七键)」, 免得实施者照字面把 SC-7 写成断言六键而恒红。

---

### [A1-m2] Minor — §2 说 `pc=None` (path_coverage 关闭) 走「同处方」, 但处方 1 的输入在该分支结构上不存在

**锚点**: Spec §2 message 表第 2 行 (`proposal.md:68`) 「`decision=unknown` / `path_coverage_enabled=false` (pc 为 None) → 「远端零 run, 覆盖未判定 …; **同处方**」」 vs §3 处方 1 (`proposal.md:82`) 依赖 `path_coverage.dispatchable_workflows`; §4 (`proposal.md:93`) `dispatchable_workflows` 只在 `_evaluate` 结果里, 而 `gate_check:495-497` 在 `path_coverage_enabled=false` 时根本不调 `evaluate_path_coverage`, 输出无 `path_coverage` 键。

**问题**: 「同处方」在 pc=None 与 `unknown` 两个分支下实际退化成「只有处方 2/3」。spec 没说明这点, 实施者可能写出对不存在的键取值的指令。

**建议**: 在 §3 处方 1 前加显式前置条件「`path_coverage` 在场且 `dispatchable_workflows` 非空」, 并在 §2 该行注明「处方 1 不可用, 直接从处方 2 起」。

---

### [A1-m3] Minor — §3 伪码未把 `gate_error` 穿到 `_build_output`; §4「既有调用点不改」与实际必须改的调用点冲突

**锚点**: Spec §2 代码块 (`proposal.md:57-61`) 只给 `verdict` / `gate_error` / `raw_message` 三个局部赋值, 但 `compute_verdict` 末尾的 `_build_output(...)` 调用 (`pre_merge_gate.py:225-232`) **当前不传 `gate_error` 参数**; Spec §4 (`proposal.md:93`) 「`_result()` 签名加可选参数, 默认 `[]`, **既有调用点不改**」 vs 规则 6 的 `_result("covered", "workflow-trigger-matched", n_wf, matched, n_changed)` (`path_coverage.py:495-497`) 必须改才能填 `dispatchable_workflows`。

**问题**: 两处措辞会让实施者漏改。前者 SC-2 会抓 (断言 `gate_error.kind` 在场), 后者 SC-9 会抓, 所以是 Minor 而非 Major。

**建议**: §2 伪码补一行 `_build_output(..., gate_error=gate_error)`; §4 改为「除规则 6 的调用点外不改」。

---

### [A1-m4] Minor — SC-13 活体第二段的断言与 spec 自己的 AD-2 前提冲突, 会 flaky

**锚点**: Spec SC-13 (`proposal.md:135`) 「随后 `workflow_dispatch` 该 workflow → 再跑 gate → `passing/pending` (非 not_found)」 vs Spec `:35` / AD-2 「`/actions/tasks` 只列已被领走的任务 … runner 忙时可达分钟级」。

**问题**: dispatch 之后到 runner 领取之前, gate 会**继续**返 `not_found`。SC-13 若是一次性断言, 在 runner 忙时会假红; 而假红的 SC 会被下一个人当成实现有 bug。

**实测证据**: `aether ci status --branch master --json` 实跑确认 runs 来自 `/actions/tasks`; `aria-plugin` 全仓 15 条 task, 其中 `ci-probe-run-creation` 3 条 (即 #152 的探针分支) —— 说明该端点只有被领取过的任务。

**建议**: SC-13 改成「dispatch 后**轮询**至 `pr_ci_status != not_found` 或超时 N 秒 (建议 180s); 超时则记录为『瞬态窗口 > N』并单独判定」。顺带: 这也正好补上 R-b 里承认的「未验瞬态一侧」。

---

### [A1-m5] Minor — 处方 1 把 Forgejo REST 端点硬写进 SKILL 指令面, 绕过 v1.31.0 建立的 `CIBackend` 抽象

**锚点**: Spec §3 处方 1 (`proposal.md:82`) 「`POST /repos/{o}/{r}/actions/workflows/{file}/dispatches`」; `aria/skills/phase-c-integrator/scripts/ci_backends/base.py:50-80` (`CIBackend` ABC + probe/NIE 契约); `SKILL.md §C.2.4.X` (v1.31.0 去 Aether-only 假设的整节)。

**问题**: (a) 轴的读操作 (`query_pr_ci`) 被刻意抽象到 backend 后面 (含 probe + Hard Constraint #7 的 NIE 传播), 而本 spec 新增的 (a) 轴**写**操作 (dispatch) 直接绕过抽象打 Forgejo。对 GHA backend 用户, URL 形状巧合相同但 host/认证不同; 对 stub backend, gate 早在 `query_pr_ci` 的 NIE 处 abort, 处方结构上不可达 —— 所以**今天没有实际后果**, 这是分层洁癖而非缺陷。诚实标注: `SKILL.md:498` 已有先例 (submodule gate 直调 `forgejo GET .../labels`), 所以这不是本 SKILL 的新破例。

**建议**: 若日后要机械化处方 1, 归位到 `CIBackend.dispatch_workflow(ref, workflow_file)` (默认 raise NIE, Aether 实现之), 让「这个 backend 支不支持 dispatch」变成可 probe 的事实而不是文案假设。当下最小改法: 在 §3 注明「处方 1 目前是 Forgejo/Gitea 专有路径, 非 Aether/Forgejo 环境直接从处方 2 起」。

---

### [A1-m6] Minor — AD-1 对 issue 原案 A 的转述在「信号来源」一点上失真 (结论不变)

**锚点**: Spec AD-1 (`proposal.md:105`) 「issue 原案把「感知首推」放 path_coverage, 但 git 侧**没有**「这是首推」的信号」 vs issue #152 原文候选 A 逐字: 「`path_coverage` 评估器感知「PR 分支在 remote 上**是否已有 run 历史** / 是否首推」」。

**问题**: A 自己给出的首选信号就是**远端 run 史** —— 与本 spec 采用的信号同一个。AD-1 的驳论只对 A 的「或是否首推」那半有效, 读起来却像 A 整体建立在一个不存在的 git 信号上。落点结论 (放 backend 归一层而非 path_coverage) 我认为仍然对且理由充分 (信息在 `query_pr_ci` 手里、path_coverage 拿不到远端状态), 只是理据的**一半**是打在 A 没主张的东西上。memory `narrow-owner-options` 提醒的正是这种「只引对己有利那段」。

**实测证据**: `forgejo GET /repos/10CG/aria-plugin/issues/152` 拉取原文逐字比对。同时确认 spec 对 A 的**另一半**转述 (「归 `not_applicable` 变体」) 完全属实 —— 拒绝 A 放行语义**不是**稻草人。

**建议**: AD-1 改成「A 的信号选择 (远端 run 史) 是对的, 本 spec 采纳; 分歧只在**落点** (path_coverage 拿不到远端状态, 而 `query_pr_ci` 已经拿在手里) 与**判定** (not_applicable 放行 = fail-open)」。这也与 proposal 头部「A′ = A 的『靠 run 史感知』+ B 的『处方文字』」的表述自洽。

---

## 未发现问题但已核验的点

- **落地顺序硬约束 (§1 §2 同 commit) 成立且承重** — 直调实测: `compute_verdict([], "not_found")` → `{"verdict": "green", ...}`; `compute_verdict([{...}], "not_found")` → `wait`。§1 单独落地确实会把恒 wait 变成恒 green。SC-2 把这个 green 当红窗也是对的。
- **(a)/(b) 两轴隔离在代码层真的成立** — `_normalize_pr_ci_status` 的唯一调用点是 `AetherBackend.query_pr_ci` (`aether.py:109`); `query_branch_in_flight` 走 `_translate_in_flight_run`, 不经过它。所以 §1 的单行改动在**机器层**不会渗到 (b) 轴 (与 A1-M6 批评的是 spec 的**论证**, 不是这条隔离事实)。
- **R-a 独立复核通过** — `grep -rn gate_error aria/`(排除 gate 自身 / 其 SKILL.md / tests) 只剩 `CHANGELOG.md:72` 一条叙述。全仓零外部消费方, 「gate_error 在场 ⇒ fail」的假设确实只活在 `SKILL.md:290` 的文字里。
- **R-c 三条探针全部独立复跑一致** — `GET /repos/10CG/aria-plugin/actions/runs` → **HTTP 404**; `GET .../actions/workflows` → **HTTP 404** (⇒ 处方 1 只能按文件名寻址, spec 结论正确); `POST .../actions/workflows/issue-triage-tests.yml/dispatches -d '{"ref":""}'` → **HTTP 400 `{"message":"ref is empty"}`** (路由与参数名证实, 未真触发)。
- **AD-2「瞬态零 run」的来源链在 aether-cli 侧证实** — `/home/dev/Aether/aether-cli/internal/ci/status.go:45-47` 逐字: `endpoint := fmt.Sprintf("/repos/%s/actions/tasks", repo)`, 注释「Forgejo v11.0.6: /actions/tasks works, /actions/runs returns empty」。branch 过滤在客户端 (`cmd/ci_status.go:119-133`)。**「task 只在被 runner 领走后才创建」这一步我没有做受控实验**, 它的依据是 handoff `2026-08-20-...:50` 的现场记录 + 端点语义, 标注为「项目记录事实, 未独立再测」。
- **我曾假设的第三种零 run 来源 (分页截断) 已实测证伪** — `/actions/tasks` 返回全量: `10CG/SilkNode` 2458/2458, `10CG/Aether` 1514/1514, `10CG/aria-plugin` 15/15。故不作为 finding, 但它反向支持 A1-M4 建议里的「not_found 在 episode 内单调」不变量。
- **SC-6 的不可达性在代码层成立** — `gate_check:498-506` 的 `if pc is not None and pc.get("decision") == "not_applicable":` 在 `query_pr_ci` 之前 return, `not_applicable` 路径结构上产不出 `not_found`。
- **六键早退契约不受本变更影响** — 新 `gate_error` 落在 `compute_verdict` 的最终路径, 不在任何早退分支上; `_build_output:268-274` 的 `path_coverage` / `gate_error` 两个 additive 键可以共存 (先后各自 `if not None` 插入), SC-5 的「同场」在结构上可满足。
- **spec 全部代码行号锚点核对无误** — `compute_verdict :174`, `_build_output :236`, `gate_check :387`, `_normalize_config :98`, not_applicable 短路 `:498`, `aether.py:225-226`, `base.py:29` (`Literal[..., "not_found"]` 确已存在), `SKILL.md:275/288/290`, 配置表 `:46-54`。
- **基线绿 + 红窗断言位置正确** — `python3 -m pytest skills/phase-c-integrator/tests -q` → **119 passed**; `test_empty_runs_pending` 在 `test_pre_merge_gate.py:362-363`, 断言逐字 `_normalize_pr_ci_status([]) == "pending"`, 确为本变更的红窗。
- **`workflow_dispatch` 识别可行性** — `.forgejo/workflows/issue-triage-tests.yml` 确有 `workflow_dispatch: {}`; 现有 `_parse_workflow` 已经把它认成 `NON_AUTO_TRIGGER_KEYS` 成员 (块映射形走 `path_coverage.py:288-291`, flow 列表形走 `:239-241`), §4 只需在既有分支上多记一个 bool, 不动判定语义。SC-8 的三例都落在已建模路径上。
- **config-loader 有位可落** — `skills/config-loader/SKILL.md:242-283` 已有 `phase_c_integrator.pre_merge_gate.*` 九个键的登记区, 新键是同构追加。
- **未跑 brainstorm 不构成 Rule #10 违规** — `.aria/config.json` 的 `audit.checkpoints.post_brainstorm = "off"`; `phase-a-planner/SKILL.md` 全文无 `A.1.0` / brainstorm 强制门; `standards/core/ten-step-cycle/` 亦无。这属于「结构性前提/显式 off」而非 AI 自行豁免 enabled 闸门, spec 头部已按要求留痕请复议, 处理方式正确。我这一轮**不**要求补 brainstorm。
- **对 issue 原案 A 的拒绝理由公允** — A 原文确实写「归 `not_applicable` 变体」, 而 `not_applicable` 在 #122 (`openspec/archive/2026-07-31-.../proposal.md`) 的语义封闭集里就是「结构性无 CI 覆盖」。把 path-matched 的变更归进去既是 Rule #8 fail-open 也污染 #122 的封闭集 —— 这个论证站得住 (转述瑕疵见 A1-m6)。

---

## Verdict

**FAIL** (1 Critical / 6 Major / 6 Minor)

**vote: REVISE**

必须在进 Phase B 前修订的三条 (其余可在 A.2 tasks 里承接):

1. **A1-C1** — 定死「一次性升级」: 加 `gate_state.no_run_escalation_done` (或等价), 二次命中同 kind 走 owner prompt 而非重跑处方。这是本 spec 唯一会造成外向、难撤销副作用的地方。
2. **A1-M1 + A1-M4** — 把 2.5 的判定式钉到字符级 (计什么量、在自增前还是后求值、是否要求连续同 kind), 并让 AD-4 的秒数与它一致。这两条是同一个欠定的两面, 应一起改。
3. **A1-M3** — Rule #6 申报改判据表第三行 + 补一条定向可证伪 fixture (或按「缺一照跑」并明写「该绿不覆盖 §3」+ 开套件缺口 issue)。fixture 数 6 → 7。

A1-M2 (message 键改 `reason`) 与 A1-M5 ((a) 轴分支存在性) 建议同轮吸收 —— 两者都有现成机制可复用 (SC-9 的 9-reason 参数化 / `_verify_main_branch_exists` 泛化), 边际成本很低。A1-M6 若 owner 认为超范围, 最低限度是把 §1:47 那句「是正确语义」删掉并开 issue, 不要让它随 §5 的文档同步面固化进 SKILL.md。
