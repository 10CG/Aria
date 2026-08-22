---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-22T06:37:32.839Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 1
major_count: 7
minor_count: 6
---

# post_spec R1 — A4 code-reviewer 席 (spec 与代码逐行对照 / 引用准确性 / 实施者分叉点 / 回归面)

审计对象: `openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md` (Draft v1)
基线: aria @ `400f0bc` (实核 `git rev-parse --short HEAD` = 400f0bc, 工作树干净)
基线测试: `python3 -m pytest aria/skills/phase-c-integrator/tests -q` → **119 passed** (复跑一致)

## 摘要

spec 的事实基础扎实: F1/F2/F3、`compute_verdict([], "not_found")` 基线返 `green`、`_normalize_pr_ci_status([])` 返 `pending`、Forgejo dispatch 路由 (400 `ref is empty`) / `/actions/workflows` 404 / `/actions/runs` 404 / 版本 11.0.6+gitea-1.22.0、最近 PR #115 (07-19) —— 全部本席独立复跑, 无一失真。行号引用 9 处核对 8 处准确 (1 处 ±1 行)。§1/§2/§4 的代码层设计 (backend 归一层修、显式分支、additive 键、not_applicable 短路不可达) 与 #122/#137/#126 契约无冲突。

问题集中在 **§3 处方 + workflow-runner 侧**: (1) 升级处方无「只执行一次」守卫, 按字面实施会在 runner 停摆/排队 (AD-2 自己承认的瞬态来源) 时每 ~90s 重复 dispatch / 重复 push, 与 AD-5「零 history 污染」自相矛盾 — Critical; (2) `retry_count` 计数时点、处方触发条件的归属 (C.2.4 步骤 6 vs workflow-runner 2.5 双写)、`gate_state.gate_error_kind` 的机械生产者 (`gate_state_helper.py` 未列入落点) 三处欠定, 两个独立实现者会得出不同时序与不同代码; (3) 文档同步面 §5 漏了 SKILL.md 的 YAML 摘要块 (:172-183)、第二张配置表 (:292-302)、workflow-runner 触发场景 (:313) 等; (4) Rule #6「照跑 AB」的 7 个 fixture 无一能到达新分支, 对新处方零判别力, 应按 NEG-3 先例加定向 fixture。

## Findings

### [A4-C1] Critical — 升级处方无「只执行一次」守卫: 字面实施 = runner 停摆时每 ~90s 重复 dispatch / 重复推 commit, 且 retry_count 归零可能连带 timeout 失效

- **锚点**: spec §3 「触发后回到 `wait_recoverable` 循环 (`retry_count` 归零), 后续 run 状态正常裁决」; AD-2 「零 run 有第二种来源 — run 已建未被领 (runner 忙时可达分钟级)」; AD-5 「dispatch 零历史污染」; `workflow-runner/scripts/gate_state_helper.py:115-155` (`write_gate_state` 无归零 API; `clear_gate_state` :158 归零的同时重置 `started_at`)
- **问题**: 处方 1 (dispatch) 或 2 (push 实质 commit) 执行后, 若 runner 未领取 (spec 自己列出的瞬态来源; 也是 #152 初诊的「runner 停摆」场景), backend 查 `/actions/tasks` 仍零 run → gate 仍 `not_found` + 同 kind → `retry_count` 归零后再等 2 次 (~90s) → 2.5 再次命中 → **再次 dispatch / 再推一个 commit**。spec 没有任何「处方已执行过 → 第二次命中直接走处方 3 (owner prompt)」的条款, 也没有 `gate_state` 里的执行计数字段。进一步: helper 里唯一的归零途径是 `clear_gate_state` → `started_at` 一并重置 → `elapsed > wait_timeout_seconds` 永不触发 → **无界循环**; 即便实现者保留 `started_at`, 1800s 内也会 dispatch ~20 次, 每次在远端建一个排队 run (或推 20 个 commit)。这与 AD-5「零历史污染」和「禁空 commit 因为是噪声」的立意直接矛盾。
- **实测证据**: `gate_state_helper.py:131-143`: `retry_count` 只在 waiting→waiting 递增, 无 reset 参数; `:158-161` `clear_gate_state` 置 null ⇒ 下次 `write_gate_state` 走 `is_first` 分支 `started_at=_utcnow_iso()` (:133-135)。memory `reference_forgejo_new_branch_paths_filter_no_run` 另记 `/actions/tasks` 只列已领任务 — 即 dispatch 成功建 run 后, 领取前 gate 仍恒 `not_found`。
- **建议** (字符级钉死):
  1. `gate_state` additive 加 `no_run_escalations` (int, 默认 0); 2.5 命中时 `+1`; **`no_run_escalations ≥ 1` 时 2.5 不再执行处方 1/2, 直接走处方 3 (owner prompt, 文案含「已 dispatch/已推 commit 一次仍零 run, 疑 runner 未领取」)**。
  2. 「`retry_count` 归零」改为「`retry_count` 归零, **`started_at` 保持不变**」(timeout 以首次 gate 为锚), 并在 helper 加 `reset_retry_count(state)` 函数 + 测试。
  3. SC 加一条: 「两次连续 2.5 命中, dispatch/push 动作恰执行 1 次 (mock 计数), 第二次产 owner prompt」— 坏实现 (无守卫) 在此红。

### [A4-M1] Major — `retry_count` 计数时点欠定: 2.5 判定用「写入前」还是「写入后」的值, 决定处方在 ~90s 还是 ~210s 触发

- **锚点**: spec §3 「第 **2** 次重查仍为同 kind 时 (默认 2, 即 30s+60s 后)」+ 2.5 条件 `retry_count ≥ no_run_escalation_retries`; AD-4; `workflow-runner/SKILL.md:338-358` 实施步骤 (3.c 重调 gate → 3.d 按 exit conditions 处理; 递增写在 Resume 段 :389「wait → 增量更新 retry_count」); `workflow-state-schema.md:121` 「Starts at 0; increments per re-invoke」; `gate_state_helper.py:139-140` (递增发生在 `write_gate_state` 调用时)
- **问题**: 首次 gate 写 `retry_count=0`; 第 1 次重查写 1; 第 2 次重查写 2。若实现者按 SKILL.md 3.c→3.d 顺序「先按 exit conditions 处理 verdict, 再 write_gate_state」, 则第 2 次重查判定时 `retry_count` 仍为 1, 2.5 不命中, 要到第 3 次重查 (30+60+120 = 210s) 才触发; 若「先 write 再判」则 90s。两个实现者按同文得出 90s vs 210s, AD-4 的整段概率论证随之失效。另: 形式化条件只有 `kind == X AND retry_count ≥ N`, 没有「连续 N 轮同 kind」— spec 文字「仍为同 kind」与形式条件不等价 (memory `rationale_formula_contradiction_is_signal`)。
- **实测证据**: `test_gate_state_helper.py:119-124` `test_subsequent_wait_increments_retry_count` 断言两次 wait 后 `retry_count == 2` — 即计数在 write 时点; SKILL.md 实施步骤没有写 write 在 3.d 之前还是之后。
- **建议**: 钉成「2.5 在 `write_gate_state` **之后**判定, 读写入后的 `retry_count`; 等价表述: gate 连续 `N+1` 次 (含首次) 返回 `gate_error.kind == no-run-for-branch`」。同时把「同 kind 连续」写进形式条件: `gate_state.gate_error_kind (上一轮) == 本轮 kind == no-run-for-branch`, 否则 `retry_count` 语义上应视为重新计数 (或明说不重计)。

### [A4-M2] Major — `gate_state_helper.py` + `test_gate_state_helper.py` 不在代码落点; `gate_state.gate_error_kind` 无机械生产者, 「仍为同 kind」的比对输入不会被生成

- **锚点**: spec 头部「代码落点」列表 (无 workflow-runner/scripts); §3 「`gate_state` block additive 加 `gate_error_kind` (string|null)」; §5 只列 `workflow-runner/SKILL.md` + `references/workflow-state-schema.md`; `gate_state_helper.py:115-155` `write_gate_state` 固定写 8 个键, 无 `gate_error_kind` 入参; `:30 CURRENT_SCHEMA_VERSION = "1.1"`; schema §8.3 迁移表 (:537-545)
- **问题**: helper 是 gate_state 的「canonical reference for any re-implementer」(docstring :8-11)。只改两份 md 不改 helper ⇒ 按参考实现走的 workflow-runner 永远不会写 `gate_error_kind`, 2.5 的「跨轮比对仍为同 kind」裁决的数据不存在 (memory `verify_predicate_inputs_exist`)。且 `gate_state` 结构变化是否 bump `format_version` 1.1→1.2 (schema §8.3 有版本表 + 迁移表) 未定 — 实现者 A 加 1.2 + 迁移行, B 当 additive 留 1.1, 两者都「合法」但 state 文件互读行为不同 (1.2 文件遇 1.1 读取器 → 「newer version, treat as absent」:521-523)。
- **实测证据**: `grep -rn gate_error_kind aria/` 零命中 (预期, 新键); `write_gate_state` 签名 `(state, *, name, verdict, in_flight_runs, primitive_used, raw_message, intervals)` — 无接收 gate 输出 `gate_error` 的通道。
- **建议**: 代码落点加 `workflow-runner/scripts/gate_state_helper.py` + `tests/test_gate_state_helper.py`; `write_gate_state` 加 `gate_error_kind: str | None = None` 关键字参数并写入 block; 明确 `format_version` **保持 1.1** (可选键 additive, 读取方 `.get()`), 在 schema §8.3 默认值表加一行 `gate_state.gate_error_kind | null | v1.1 (additive, aria-plugin #152)`; 加 helper 测试「wait 携 kind 写入 / 下一轮 kind 变化被覆盖 / green 清空」。

### [A4-M3] Major — 处方触发条件在两个 Skill 里各写一遍 (C.2.4 步骤 6 与 workflow-runner 2.5), 而 C.2.4 结构上观测不到 `retry_count`

- **锚点**: spec §3 第一段「§C.2.4 步骤 6 wait 路由加处方: … 并在 `wait_recoverable` 第 2 次重查仍为同 kind 时停止等待, 按优先序执行处方」; 第二段「workflow-runner 2.5: … → 转 §C.2.4 处方」; `pre_merge_gate.py` 输出 schema 无 `retry_count`; `references/pre-merge-gate-empirical-traps.md:50-51` (「SKILL.md 散文流程是同一算法的第二份实现」)
- **问题**: C.2.4 每轮被 workflow-runner 重新调用, 自身无状态 (Out of Scope 明言计数在 gate_state), 它无法判断「这是第 2 次重查」。把「第 2 次重查仍为同 kind」同时写进 C.2.4 步骤 6 与 workflow-runner 2.5 = 同一判定的两份实现 — 这正是 traps §五 刚记录的病 (#137 修了 `gate_check()` 而散文流程没修)。两个实现者会分叉: A 让 C.2.4 读 `.aria/workflow-state.json` 自判; B 让 workflow-runner 判后带参数调 C.2.4; 两者对「处方 1 失败 fall through 2 的状态机」也会落在不同 Skill。
- **实测证据**: `grep -n retry_count pre_merge_gate.py` 零命中; SKILL.md §C.2.4 步骤 6 (:260-263) 现只按 verdict 三路分发, 无任何轮次概念。
- **建议**: 判定**只**存在于 workflow-runner 2.5; §C.2.4 步骤 6 `wait` 路由只写两件事: (a) `gate_error.kind == no-run-for-branch` 时 surface message; (b) 「处方 1-3 的执行序与留痕要求, **入口仅为 workflow-runner 2.5 转入**, C.2.4 自身不判轮次」。2.5 条目写明「转入 phase-c-integrator §C.2.4 处方段执行 (非 fatal)」并规定处方执行结果如何回写 gate_state (见 C1 的 `no_run_escalations`)。

### [A4-M4] Major — §5 文档同步面遗漏 7 处, 实施者按清单做完仍留下可见漂移

- **锚点**: spec §5; 各处实测行号如下
- **问题 / 实测证据** (逐条 grep 核实):
  1. `phase-c-integrator/SKILL.md:172-183` YAML 摘要块: `:175 wait: main 有 in-flight CI run OR PR CI pending` 需加「OR 零 run (not_found)」; `:180 pr_ci_status: "passing" | "failing" | "pending" | "not_applicable"` 需加 `not_found`; 该块 `output:` 本就缺 `gate_error` (#137 遗留漂移, 本 spec 改写在场条件时应一并补)。§5 只点了 :276 schema / :288 / :290。
  2. 第二张配置表 `SKILL.md:292-302` (§C.2.4 配置参数) — §5 只写「配置表 (:46-54 区段)」, 实际有两张 (:46-54 顶层表 + :292-302 节内表), `path_coverage_enabled` 先例两张都登记 (:54 与 :302)。
  3. `SKILL.md:241` 「7 条实测踩出来的坑」— traps 加第六节后计数变, §5 未列。
  4. `pre_merge_gate.py:253-256` `_build_output` docstring 「仅 main 分支存在性核验判 fail 时在场 … 无 path_coverage」与 `:181-194` `compute_verdict` docstring — 代码内文档, 与 :290 同语义, §5 只改 md 不改 docstring ⇒ 代码自述与行为矛盾 (Rule #3)。
  5. `workflow-runner/SKILL.md:313` 触发场景「main 分支有 in-flight CI 或 PR CI pending」+ `:326` behavior log 文案「main 分支有 in-flight CI, 等待 X 完成」— 不含零 run 场景; §5 只列 2.5 + gate_error_kind。
  6. `workflow-state-schema.md:125` `raw_message` 字段注 (#122 时补了 not_applicable 文案注) — 本 spec 让 `raw_message` 在 wait 态携处方文案, 同款注记应补。
  7. `.aria/config.template.json:73-91` `pre_merge_gate` 块无 `no_run_escalation_retries` (也无 `path_coverage_enabled` — #122 先例同样漏; 是沿先例不加还是补两个, 须明说, 否则一半实现者会加)。
- **建议**: §5 改为逐行号清单 (上列 7 处 + 既有 7 处), 并加 SC: 「`grep -n 'pending' SKILL.md` 中所有枚举行含 `not_found`; `grep -c gate_error SKILL.md` 覆盖摘要块」。

### [A4-M5] Major — Rule #6「照跑 AB」的 7 个 fixture 无一能到达 `not_found` 分支, 对新处方零判别力; 应按 NEG-3 先例建定向 fixture

- **锚点**: spec §rule6_note 「`phase-c-integrator-pre-merge-gate.json` (6 fixtures) … 与 #122 同款先例, 零裁量」; `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json` fixtures 数组 (7 条: green / wait / wait_then_green / fail / NEG-1 / NEG-2 / NEG-3); `NEG-3-internal-error-surface.json:3` 「既有 6 个 fixture 结构上都碰不到 path_coverage 的 unknown 分支 … 本 fixture 补这个缺口」; `standards/conventions/skill-benchmark-exemption.md` 判据表第三行第 2 条义务
- **问题**: 7 个 fixture 的 `pr_ci_status` 取值为 passing/failing/pending, 无 `not_found`, 无 `gate_error.kind=no-run-for-branch`。AB 照跑只能证明「既有行为未退化」, 对本 spec 新增的运行时指令 (surface message / 停止等待 / 处方优先序 / 不得 green) 测不到 — 这恰是判据表第三行「套件覆盖外」的形状, 义务是「点名行为 + 建可证伪定向 fixture + 套件缺口开 issue」, 而非「第二行零裁量」。#126 的 NEG-3 就是同 skill 同套件的先例。另 fixture 计数 6 → 实为 7。
- **实测证据**: `grep -rn 'not_found\|gate_error' ab-suite/phase-c-integrator-pre-merge-gate-fixtures/` 零命中; `phase-c-integrator-pre-merge-gate.json` `fixtures[]` 长度 7。
- **建议**: rule6_note 改为第二行 (既有 7 fixture 照跑) **+** 第三行义务 (新建 `NEG-4-no-run-for-branch.json`: gate 输出 `verdict=wait, pr_ci_status=not_found, gate_error.kind=no-run-for-branch, path_coverage.dispatchable_workflows=[...]`, `_discriminating_question` = 「AI 是否 (a) 不写『CI pending 等待中』而点明零 run + #152; (b) 不放行 green; (c) 第 2 次同 kind 后走 dispatch 而非空 commit」); 更新 json `fixtures[]` + `changelog`。

### [A4-M6] Major — `covered` 分支 message 按 `reason` 再分欠定; 「(ii) 与 path_coverage 共存」在 `path_coverage_enabled=false` 时不成立

- **锚点**: spec §2 message 表 (`decision=covered` → 「变更 path-matched `<matched_workflows>` …」); SC-2 「message 含 `#152` 与 matched workflow 名」; §2 「(ii) … 与 `path_coverage` 共存 — 这是 gate_error 第一次与 path_coverage 同场」; `path_coverage.py:457-464` 规则 2/3 (`empty-diff` / `workflow-files-changed` 均 `covered` 且 `matched_workflows=[]`)
- **问题**: `covered` 有 3 个 reason, 只有 `workflow-trigger-matched` 带 matched 名; `empty-diff` / `workflow-files-changed` 下模板会渲染成「path-matched `[]`」(误导: 暗示没 match), 且 SC-2 的「含 matched workflow 名」结构上不可满足。实现者 A 渲染空列表, B 自行发明第四种文案 — 「三分支封闭」的封闭性实际落在 decision 而非 message。另: pc=None (评估关闭) 时 `gate_error` 在场而 `path_coverage` 不在场, §2/:290 改写文案「与 path_coverage 共存」是条件真; SC-5 若按「同场」断言两键俱在, 对 `path_coverage_enabled=false` 变体会误判。
- **实测证据**: `compute_verdict([], "not_found", path_coverage={"decision":"covered","reason":"empty-diff","matched_workflows":[]})` 基线返 green (无分支); `_result("covered","workflow-files-changed", n_wf, [], n_changed)` :464 matched 恒 []。
- **建议**: message 表按 `(decision, reason)` 钉: `covered/workflow-trigger-matched` → 列 matched (`", ".join`); `covered/workflow-files-changed` → 「变更含 workflow 文件, 按 covered」; `covered/empty-diff` → 「空 diff」; `unknown/*` 与 `pc=None` → 「覆盖未判定 (reason=<…> | 评估关闭)」。:290 改写为「(ii) … `path_coverage` 在场与否取决于评估是否执行 (`path_coverage_enabled`)」; SC-5 拆为 enabled/disabled 两变体。

### [A4-M7] Major — 处方 1 承重的 `workflow_dispatch` 原语「未真触发」, 且与 memory 既有记录矛盾; AD-5 优先序建在未验前提上

- **锚点**: spec R-c 「未真触发 … 权限面 (token scope) 未验」; AD-5 「处方优先 workflow_dispatch」; SC-13 「随后 workflow_dispatch 该 workflow → 再跑 gate → passing/pending」; memory `reference_forgejo_new_branch_paths_filter_no_run` 「`workflow_dispatch` API 在 gitea-1.22 系**不可用**」
- **问题**: 路由存在 (本席复跑: `POST …/actions/workflows/issue-triage-tests.yml/dispatches` body `{"ref":""}` → HTTP 400 `ref is empty`; `/actions/workflows` 404; `/actions/runs` 404; 版本 11.0.6+gitea-1.22.0) 只证明 handler 在, 不证明带合法 ref 会建 run、也不证明当前 token scope 够。memory 记录 (同一位 owner 的同一现场) 说它不可用 — 两条记录互斥, spec 没有调和。若真不可用, 处方 1 恒 fall through, AD-5 的「优先 dispatch, 零污染」退化为「恒走处方 2 推 commit」, 设计叙事需要重写而非只是兜底。SC-13 也依赖它成立。
- **实测证据**: 见上 (本席未真触发 — 真触发会在共享仓建 run, 属 owner 动作; memory `sync_instruction_not_push_authorization` 同形状)。
- **建议**: Phase B 开工第一步 = 在 throwaway 分支真触发一次 (ref=该分支), 记录 HTTP 码 + 是否出现 run + 领取延迟, 结果回写 R-c 并**修正 memory** (哪条对就留哪条); 若失败, AD-5 改为「处方 2 为主, dispatch 为可选」。SC-13 加时序条款 (见 m5)。

### [A4-m1] Minor — 行号 / 计数勘误三处

- **锚点**: spec §2 「SKILL.md:275 schema」→ 实为 `:276` (`"pr_ci_status": …` 行; :275 是 `"verdict"`); rule6_note 「6 fixtures」→ 7; AD-4 「第 2 次重查发生在 **push 后** ~90s」→ 应为「**首次 gate 调用后** ~90s」(push → PR 创建 → 首次 gate 之间的耗时不在 intervals 内, helper `_next_check_at` :104-112 以首次 gate 为锚)。
- **按 spec 实施会怎样错**: 行号偏差 1 行无实害; 「push 后 90s」会让阈值论证 (runner 领取秒级) 的时间轴少算一段, 实际 2.5 触发时距 push 更久, AD-4 只会更保守, 方向安全。
- **建议**: 改 :276 / 7 / 「首次 gate 后」。

### [A4-m2] Minor — SC-4 基线标「红」, 但 verdict 断言基线已绿, 只有 kind 断言红

- **锚点**: SC-4 `compute_verdict(main_runs非空, "not_found")` → 仍 wait + 同 kind | 基线: 红
- **实测证据**: 基线 `compute_verdict([{'run_id':1}], 'not_found')['verdict']` = `wait` (经 `:219 elif main_in_flight_runs` fallthrough)。
- **按 spec 实施会怎样错**: 只断言 verdict 的实现者会得到一条「基线即绿」的测试, 红窗声明失真 (memory `test_asserts_what_its_name_claims`)。
- **建议**: SC-4 基线栏改「verdict 绿 / kind 红」, 断言必含 `gate_error.kind`。

### [A4-m3] Minor — SC-10 的读取路径欠定: `compute_verdict` 直调时 `cfg=None` / 非法值如何取阈值; `DEFAULT_CONFIG` 是否加键; message 必含子串未列

- **锚点**: SC-10; `pre_merge_gate.py:178` `cfg` 参数现**未被读取** (grep 函数体无 `cfg`); `:57-69 DEFAULT_CONFIG`
- **按 spec 实施会怎样错**: SC-2/3/4 直调不传 cfg, 实现者须在 `compute_verdict` 内做 `(cfg or {}).get(key, 2)`; 若阈值校验只在 `gate_check`, 直调传 `{"no_run_escalation_retries": 0}` 会把「第 0 次」写进 message。message 只规定「要点」, 两个实现者文案不同, 测试只能断子串。
- **建议**: 钉: `DEFAULT_CONFIG["no_run_escalation_retries"] = 2`; `compute_verdict` 读 `(cfg or DEFAULT_CONFIG).get(...)` 不校验; 校验仅 `gate_check`; message 必含子串闭集: `aria-plugin#152`、`no_run_escalation_retries=<N>`、`dispatch` 或 `push` 处方关键词、matched 列表 (`", ".join`)。

### [A4-m4] Minor — SC-7 「既有 5 类早退」参数化应覆盖 7 个落点

- **锚点**: SC-7; `pre_merge_gate.py` 早退落点: `:418` enabled=false / `:428` no-backend (两种 fallback :362/:376) / `:434` precheck / `:454` main 核验 (**两 kind** :455/:458) / `:489` (b) 腿 AetherQueryError / `:512` (a) 腿 AetherQueryError
- **按 spec 实施会怎样错**: 按「5 类」参数化会漏 (a) 腿 AetherQueryError 与 `main-branch-verify-failed`, 守卫有洞。
- **建议**: SC-7 列 7 个落点 (或 8, 含 no_ci_fallback 两值)。

### [A4-m5] Minor — SC-13 活体缺时序条款: dispatch 后 `/actions/tasks` 在 runner 领取前仍零 run

- **锚点**: SC-13 「随后 workflow_dispatch → 再跑 gate → passing/pending」; Why 附注 (`/actions/tasks` 只列已领)
- **按 spec 实施会怎样错**: dispatch 后立即跑 gate 大概率仍 `not_found`, 活体会被判失败或被 retry 到通过 — flaky。
- **建议**: 「dispatch 后轮询直至 `/actions/tasks` 出现该 run (上限 N 分钟) 再跑 gate」; 记录领取延迟作为 AD-4 阈值的首个经验数据点 (顺带回应 R-b)。

### [A4-m6] Minor — `dispatchable_workflows` 在 `covered/workflow-files-changed` 下恒 `[]`, 处方 1 在该场景不可用虽仓内存在可 dispatch workflow

- **锚点**: spec §4 「仅在 covered/workflow-trigger-matched 时该列表可能非空」; `path_coverage.py:461-464`
- **按 spec 实施会怎样错**: 不分叉 (spec 已钉), 但改 workflow 文件的首推 (同样零 run) 会直接落处方 2。这是设计限制, 应在 §4 或 AD 明示, 免得实施者「顺手」扩成全量列表造成分叉。
- **建议**: §4 加一句「workflow-files-changed 下不列 (matched 为空是既有语义, 不为处方改规则 1-8)」。

## 未发现问题但已核验的点

- 基线主张逐条复跑: 119 绿 ✓; `_normalize_pr_ci_status([])` = `pending` ✓ (`aether.py:225-226`); `compute_verdict([], "not_found")` = **green** ✓ (:219-224 fallthrough, 含 `path_coverage=covered` 变体亦 green); `CIStatus.state` Literal 含 `not_found` ✓ (`base.py:29`); `test_pre_merge_gate.py:363` 断言 `== "pending"` ✓; not_applicable 短路 `:498-506` 在 `query_pr_ci` (:509) 之前 ✓; `SKILL.md:288/:290` 文字 ✓; `:46-54` 配置表 ✓; workflow-runner Exit conditions `:332-336` 四条 first-match-wins ✓; traps 文件现五节, 「第六节」编号正确 ✓。
- F3: `forgejo GET /repos/10CG/aria-plugin/pulls?state=all&sort=newest` 最新 = #115 (2026-07-19) ✓。aether 在 aria 子模块 cwd 下解析 repo = `10CG/aria-plugin`, 不存在分支返 `"runs":[]` ✓。
- Forgejo 探针: dispatch 路由 400 `ref is empty` ✓; `/actions/workflows` 404 ✓; `/actions/runs` 404 ✓; version `11.0.6+gitea-1.22.0` ✓。
- 回归面: `test_pre_merge_gate.py` 中所有 `pending` 断言 (:129/:245-249/:263) 均由 mock 直接返 `pr_state="pending"` 或早退分支硬编码, **不经** `_normalize_pr_ci_status([])`; `test_ci_backends.py` 无空 runs 用例; 翻转 :363 之外零隐含依赖 ✓。`MainBranchExistenceTests._stub_backend` (:823-833) 误写 `query_pr_ci_status` 致 `pr_ci_status` 为 MagicMock — 新 `elif == "not_found"` 分支对 MagicMock 不命中, 既有 wait 判决不变 ✓ (预存瑕疵, 非本 spec 引入)。
- AB fixtures: 7 个 fixture 无 `pending`-因-空-runs 语义 (NEG-3 的 `pending` 为字面值, 与 unknown 覆盖无因果), 本 spec 不改变任何既有 fixture 语义 ✓ (缺口见 M5)。
- 契约: #122 `not_applicable` 语义未被触碰 (短路在前, `not_found` 不可达; 规则 1-8 与 9 reason 不动) ✓; #137 `gate_error{kind,message}` + 「同文同写 raw_message」由 §2 伪码保持 ✓, `gate_error` 外部消费方 `grep -rn gate_error aria/ --exclude-dir=phase-c-integrator` 零命中 (R-a 成立) ✓; #126 `internal-error` 自成一档不受影响 ✓; (b) 轴 `query_branch_in_flight` 不动 ✓; NIE propagation 不动 ✓; 六键早退逐字不变 (early-exit 仍硬编码 `pr_ci_status="pending"`, 合约如此) ✓。
- Out of Scope vs What Changes: 「gate 保持无状态」与「gate 读 config 写阈值进 message」不矛盾 (config ≠ 跨调用状态; message 是静态模板含 N, gate 不知当前轮次) ✓; 「处方 2 仅限 feature 分支」与 AD-5 一致 ✓。
- 观察 (预存, 不计入本 spec): aether 返回的 run 对象键为 `created_at` 而非 `started_at`, `_normalize_pr_ci_status` 按 `started_at` 排序恒为 "" ⇒ 「最近 run」实为 aether 返回序首元素。与本 spec 无关, 建议另开 issue。

## Verdict

**FAIL** (1 Critical / 7 Major / 6 Minor) — **vote: REVISE**

代码层 (§1/§2/§4) 与事实基础可直接进 A.2; 阻塞在 §3 处方的状态机 (C1 重复 dispatch 无守卫) 与 workflow-runner 侧三处欠定 (M1/M2/M3), 这些决定两个实现者会写出不同时序与不同落点。修 C1 + M1-M3 后, M4-M7 为清单型补全, 不需重开设计讨论。
