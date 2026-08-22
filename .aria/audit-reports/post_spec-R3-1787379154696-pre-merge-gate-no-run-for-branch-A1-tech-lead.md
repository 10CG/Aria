---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T08:00:29.221Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A1-tech-lead
critical_count: 0
major_count: 6
minor_count: 5
---

## 摘要

**设计收缩是对的**, 且执行得干净: 我 R2 报的 C1 + 6 Major 里, 有 5 条是随「自动写动作」子设计一起被删掉的 (不是被打补丁掩盖), 归我席的 9 个簇 **closed 8 / partial 1**。第八早退 (簇 #4) 我复核插入点**唯一可推** (`pr_status.state` 只在 `:508-518` try/except 之后存在, 末尾 `compute_verdict` 在 `:521`, 中间只有一个位置); 包装函数方案与 `:449` 关键字调用、mixin `:85-89` 打桩两侧都对得上; 时间轴 t=0/30/90 我按 `_next_check_at(retry_count)` 的实际语义逐轮重算**成立** (R1-M1→R2-M2 那个 off-by-N 这轮真被钉死了)。

残余问题集中成一束: **v3 为回答 R2-C1 而新建的「运行时证据机器」(CLI + telemetry + 主仓 state-check) 自己不成立** —— 它自称「镜像 `coordination-gate-invocation`」, 但把先例里**承重的三件**都漏了: 记录里的 `source` 分区字段 (先例的 probe 只计 `source=="production"`)、production 分区的结构性不可达保证 (先例的 anti-spoof 是审计 Critical 修出来的)、以及 `enabled_when` 式跳过条件。再叠上一条实测: 162 篇 handoff 里只有 2 篇 (均 5 月, 本机制自己的开发周期) 出现过 `gate_state`/`wait_recoverable`, 而 `C.2.4` 出现在 35 篇 —— **这个探针的健康常态值是红**。memory `delegate-verify` / `cite≠apply` 的形状: 引了先例, 但没去先例源码核「它到底靠什么成立」。

另有 4 条独立 Major: CLI 参数面缺 `--name`/`--intervals` (恰是 `write_gate_state` 的两个承重输入) · verify-failed 追加串漏消毒 (伪码对安全串消毒、对危险串不消毒) · 「continue 后 ~210s 再次 prompt」实算 t≈810 · 处方 (a) 行的开关 `dispatch_viable` 只活在一个 authoring-time references 文档里。

诚实标注边际产出: 我这轮 6/6 Major 仍全在 v3 新写的文字上 (拐点判据再次命中)。但与 R2 不同 —— **这轮的修法是 5 处行级修补 + 1 处 scope 切除, 不是又一个子系统**。所以我的处置建议是 v4 定点修 + **单席复核 (或 owner 直批), 不再开五席 R4** (见 Verdict 末段)。Vote **REVISE**。

---

## R2 处置核对

| 簇# | 状态 | 证据 |
|---|---|---|
| **#1** (F7 helper 运行时零消费方) | **partial** | 方向对: §3.1 加 CLI (`record`/`reset-observations`/`clear`) + §3.2 步骤 2/3c'/3d 明写「经 subprocess 调 CLI, 不再由 AI 手写 JSON」+ R-e 写了 CLI 失败不得回退手写。**但接线的三个接缝都不闭**: 参数面缺 `--name`/`--intervals` (→ M3); telemetry 缺 `source` 分区且单测经同一 CLI 写同一分区 (→ M1); 探针健康常态=红 (→ M2)。「谁调/何时」已定, 「失败怎么办」已定, 「探针真能红」**不成立** |
| **#2** (`done` 字段跨写丢失 / 不落盘) | **closed** | `done` 随自动动作一并删除; 只剩 `no_run_observations`, 由 CLI `record` 单点读-改-写 (沿用 `atomic_write_state`); SC-11(d) 逐字要求「坏实现 (整块重建漏 carry-forward) 必红」—— 这正是我 R2 实测 `write_gate_state` 整块重建会静默丢键的那条, 现在有测了 |
| **#3** (求值 vs 自增顺序 / t≈90 vs 210) | **closed** | 3c' 明写「先自增, 后求值」且 `record` 返回 `should_prompt`; 我按 `_next_check_at(retry_count)` (`gate_state_helper.py:103-110`, `idx=min(retry_count, len-1)`) 与 `write_gate_state` 的 retry_count 语义逐轮重算: t=0 (retry 0, obs 1, next +30) → t=30 (retry 1, obs 2, next +60) → t=90 (retry 2, obs 3) ⇒ **prompt 确在 t≈90**。⚠️ 同一段里 continue **之后**那句的算术是错的 → 新 M5 (不回退本簇) |
| **#4** (2.1 伪码 verdict 写死 / `pr_branch_check` 形参) | **closed** | 改为第八早退 `_build_output(verdict=fail, kind=pr-branch-not-found)`; `compute_verdict` 无新形参 (「不感知分支核验」逐字写明)。插入点唯一性我复核: `pr_status` 只在 `:508-518` 之后存在, 唯一位置在 `:519`–`:521` 之间; `_build_output` (`:236-275`) 的 `path_coverage`/`gate_error` 都是 `is not None` 才入键 ⇒ 「pc 在场 ⇔ enabled」结构上成立。⚠️ 该伪码新引入消毒不对称 → 新 M4 |
| **#6** (TASK-0 成环 / 失败分支连锁) | **closed** | TASK-0a 改为**实现前纯 API 探针**, 不依赖本 spec 代码 ⇒ 环解开; §4 改「无条件实现」⇒ 字段恒算、SC-8/9 恒跑, 不再随布尔取舍。⚠️ 「唯一影响面 = (a) 行」这个主张只在半个意义上成立 → 新 M6 |
| **#7** (2.5 不退出的 exit condition / 双弹) | **closed** | 2.5 变成真终止型 exit condition, `continue`/`abort` 语义各写死一行; 2.6 与自动动作一并删除 ⇒ 同形 prompt 只剩一处定义。**双弹核对**: SKILL `:331` 现文逐字「优先级 first-match-wins」, 2.5 插在 2 与 3 之间 ⇒ 同一轮里 exit 2 (timeout) 恒先命中, 结构上不可能双弹 ✓。⚠️ 两个 `continue` 的**跨条件**副作用未定义 → 新 m4 |
| **#8** (NEG-4 未登记 / 无路由) | **closed** | SC-15 要求 fixture **且登记进** catalog `fixtures[]` 含 `test_case_in_unit_tests` 绑到 SC-2 用例 + 「回退本 spec 后该测试转红」的可证伪锚; 点名行为收缩为两条单步可证伪; #127 (open) 追加评论, 「若无则新开」已删 |
| **#9** (`DEFAULT_CONFIG` 落点 / 校验点矛盾) | **closed** | `_effective_prompt_threshold(cfg)` 为唯一校验点, `compute_verdict` 与 `gate_check` 同经它 (SC-3 末条直接断言两路径回显同值); `DEFAULT_CONFIG` (`:57-69`) 列入落点 (我复核该 dict 确无该键, state-check `config-template-key-currency` 会红); §3.3 误引 SC-10 已勘正 |
| **#14** (12 条 minor) | **closed** | 逐条抽查: reason 族 = 8 (§4 + `path_coverage.py:36` 勘正 + SC-9 参数化 8 reason) ✓ / 三档前缀匹配 ✓ (2.3 逐字) / 四个 kind 均遵守副本通道 ✓ / `pr-branch-not-found` 的 pc 随 enabled 条件化 ✓ / `:363` 勘正 ✓ (与实际 `test_pre_merge_gate.py:363` 相符) / traps 不收 F1 ✓ / 直调 §C.2.4 无计数声明 ✓ / unknown 三档不出 (b) 行 ✓ (等价于旧 `remedies=[]`) / 新旧两名各打一桩 ✓ |

**统计**: closed 8 / partial 1 / not_addressed 0。

---

## 新 Findings

### [A1-R3-M1] Major — 「镜像 `coordination-gate-invocation`」漏掉了先例赖以成立的三件之二: telemetry 记录无 `source` 分区字段, 且 SC-11(d) 的单测经同一 CLI 写同一分区

**锚点**: spec §3.1 (`record` → 「追加一行 `.aria/gate-state-telemetry.jsonl` (`{ts, sub, verdict, kind, no_run_observations, should_prompt}`)」/「主仓 `.aria/state-checks.yaml` 加 `gate-state-helper-invocation` (warning; 14d 内 telemetry ≥1 条, **镜像 `coordination-gate-invocation`**)」) · SC-11(d) (「telemetry 两行」) · SC-16

**实读先例** (本轮实读, 非引用)
- `aria/skills/state-scanner/scripts/lib/runtime_probe.py:44-46` docstring 逐字: 「malformed JSONL lines are skipped, not fatal; **only `source == "production"` records count**」。
- `.aria/coordination-telemetry.jsonl` 实际记录: `{"ts": "...", "source": "production", "arm": "manual", "outcome": "passed", ...}` —— `source` 是每条记录的第二个字段。
- `phase1_gate.py:934-947` 的分区注释 + `coordination_probe.py:17-28`「Partition guarantee」段: production 分区**结构上**只能从私有 `_gated(_source="production")` 到达, 公共 API `run_gate` **没有** `source` 形参、`run_gate_synthetic` 强制 `harness`; `tests/test_phase1_gate_telemetry.py:3-12` 的整个文件目的就是锁这条 (「anti-spoof lock (R2-Major-C / PP-R2-qa-Major)」) —— 即**先例的这一半是被上一轮审计判 Major 才补出来的**。

**问题** v3 的记录形状里**没有 `source`**, 也没有 production/harness 分区。两条路都走不通:
- 若新探针复用 `lib/runtime_probe.py` (spec 未说用不用): 它只计 `source=="production"`, 而 v3 一条都没有 ⇒ **恒 0 ⇒ 恒红**, SC-16 的「SC-13 之后 pass」当场不成立。
- 若自写一份计数逻辑: 就丢掉了先例花一轮审计补出来的不可伪造性。而 v3 恰好把伪造口开在最容易踩的地方 —— **SC-11(d) 是一条经 CLI 跑两次并断言「telemetry 两行」的单元测试**。CLI 是唯一写入者, 于是「测试调 CLI」与「生产调 CLI」逐字节同形。telemetry 文件路径以什么为根 spec 也没写 (`--state-file` 给的是 state 路径; 记录路径写作裸 `.aria/gate-state-telemetry.jsonl`) ⇒ 若按 cwd 解析, 在仓根跑一次 pytest 就把探针刷绿。

**按 spec 实施会怎样错**: 要么探针恒红被静音, 要么 `pytest` 一跑就绿 —— 两种都回到 R2-C1 要治的病 (「勾选 ≠ 真被生产调用」), 只是从 helper 挪到了探针。memory `false_green_dual_is_permanent_red` + `completion_signals_vs_runtime_invocation`。

**附带 (同一 finding 的第三件)**: §5 把探针放 **主仓 `.aria/probes/`**, 而生产者 (CLI) 在 **aria-plugin**。先例是反过来的 —— `coordination_probe.py` 与 `phase1_gate.py` 同仓同目录树, 记录形状变了两边一起 ship。跨仓放置 = 插件改一个字段名, 主仓探针静默错解析且无版本握手 (子模块 bump 时无人核)。

**建议**: (i) 记录加 `"source"`, CLI 的生产入口写 `production`, 测试路径显式走另一个值/另一分区 (可直接照抄 `phase1_gate.py:950-987` 的 `_telemetry_path` 两分区写法, 8 行); (ii) 明写 telemetry 路径以 `--state-file` 的父目录为根 (与 state 同仓同目录, 不受 cwd 影响); (iii) 探针与生产者同仓 (放 `aria/skills/workflow-runner/scripts/`, state-checks.yaml 按 `coordination_probe.py` 那行的形式调用), 或明确记下跨仓耦合的代价并加一条 schema 断言测试。

---

### [A1-R3-M2] Major — 这个探针的健康常态值是**红**: 它测的事件 (workflow-runner wait 循环) 在本仓近三个月的实际语料里几乎不发生, 而它没有先例那样的 skip 条件

**锚点**: spec §3.1 (「14d 内 telemetry ≥1 条」) · SC-16

**实测语料** (本轮实跑)
```
$ grep -rl "wait_recoverable\|gate_state" docs/handoff/ | wc -l     → 2   (均 2026-05, 本机制自己的开发周期)
$ ls docs/handoff/*.md | wc -l                                       → 162
$ grep -rl "C.2.4" docs/handoff/ | wc -l                             → 35
$ ls -la .aria/workflow-state.json                                   → 不存在
$ git log --diff-filter=A -- .aria/workflow-state.json               → 从未提交 (且 .gitignore:6 忽略)
```
即: C.2.4 gate 本身高频 (35/162), 但**写 `gate_state` 的那条路径 (workflow-runner wait 循环) 近三个月零留痕**。`record` 只在 wait 循环里被调 ⇒ 14 天窗口内命中概率极低。对照先例: `.aria/coordination-telemetry.jsonl` 最近两条是 08-08 / 08-19 —— `phase1_gate` 挂在**每次 Phase B 入口**, base rate 高一个量级。

**问题** 先例还有一层 v3 没有的保护: `enabled_when: state_scanner.coordination.enabled`, 关掉时探针恒 OK (`coordination_probe.py:main()` 的 `skipped` 分支)。v3 的探针没有任何 skip 分支 —— 而它需要的 skip 条件 (「本窗口内根本没发生过 wait 循环」) 恰恰只能由它自己要测的那份 telemetry 回答, 逻辑上取不到。结果: SC-13 dogfood 后绿 14 天, 然后**永久红**。memory `false_green_dual_is_permanent_red` (「恒红同样零信息」) + `mechanization_knob_must_match_granularity` (「开关作用域要恰等于情形集」)。

**按 spec 实施会怎样错**: 主仓 `/state-scanner` 多一条永远红的 warning, 三次之后没人再看它 —— 于是真退化成死代码时它也不会被注意到, 净负。

**建议** (三选一, 须在 AD 里选定): (a) **降级为一次性 ship 证据**: 删 14d liveness 探针, 把 SC-13 活体输出 (state 文件片段 + telemetry 行) 抄进 traps §6 或 spec, 作 tracked、可评审的证据 —— 与 TASK-0a 的证据处置同构; (b) 把探针的**量**换掉: 断言「若窗口内存在 C.2.4 wait 留痕则必有 telemetry」(条件式, 无 wait 则 skip/exit 2), 注意这需要一个 wait 计数源, 成本不小; (c) 保留 liveness 但把窗口放到与 base rate 匹配的量级并明写「无事件即 skip」的判据。我推荐 (a) —— 它把这条 Major 与 M1 一起消掉, 且不给 #152 加一个与它无关的子系统。

---

### [A1-R3-M3] Major — CLI `record` 的参数面漏掉 `write_gate_state` 的两个承重输入 (`name` / `intervals`); 照签名实施会静默丢掉配置的 `wait_check_intervals`, 并让旧 state 在 resume 时重置计时预算

**锚点**: spec §3.1 (`record --verdict wait|green|fail [--gate-error-kind K] [--threshold N] [--raw-message …] [--in-flight-runs JSON]`) · §3.2 步骤 2/3c'

**实读被调函数** (`gate_state_helper.py:115-155`)
- `def write_gate_state(state, *, name, verdict, in_flight_runs=None, primitive_used="aether-ci-cli", raw_message="", intervals=DEFAULT_INTERVALS_SECONDS)` —— `name` 是**必填 keyword-only**, `intervals` 有默认值。
- `is_first = not existing or existing.get("name") != name` (`:143`); is_first ⇒ `retry_count = 0` **且** `started_at = _utcnow_iso()`。
- `next_check_at = _next_check_at(retry_count, intervals)`, 而 `_next_check_at` 用 `intervals[min(retry_count, len-1)]`。

**问题** 两个参数 CLI 都没有暴露, 于是实施者只能硬编码:
1. **`intervals` 丢失 ⇒ 配置被静默忽略。** `wait_check_intervals` 是 config 键 (`pre_merge_gate.py:63` `DEFAULT_CONFIG["wait_check_intervals"] = [30,60,120,300,300]`), workflow-runner SKILL 步骤 1 明写「读 config」、步骤 3a 明写「sleep = `wait_check_intervals[min(retry_count, len-1)]`」。接线后: **AI 侧 sleep 用配置值, helper 侧 `next_check_at` 用硬编码默认值** —— 同一个循环里两个时钟。而 Resume 语义 (`workflow-runner/SKILL.md:387-389`) 判「是否过期」读的正是 `next_check_at`。任何非默认 intervals 的采用方, resume 后的行为都会错。这是接线**引入的回归** (今天 AI 手写 JSON 时用的是配置值)。
2. **`name` 硬编码 ⇒ 破坏 `gate_state` 的通用化契约 + resume 归零。** SKILL `:249-264` 的 schema 块里 `"name": "pre_merge"`, 且逐字声明「schema 通用化为未来 `pre_release` / `pre_deploy` 预留扩展」。CLI 里钉死一个常量既堵死该扩展, 又意味着**升级前的 state 文件** (name=`pre_merge`) 在升级后第一次 `record` 时 `is_first=True` ⇒ `retry_count` 与 `started_at` 双双归零 ⇒ exit condition 2 的两个上界 (`retry_count > max`, `elapsed > wait_timeout_seconds`) 一起重置。

**按 spec 实施会怎样错**: 两个实施者会给出不同的 CLI 签名 (memory `spec_underdetermination_two_implementer_test`), 且两条后果都不会有测试发红 —— SC-11 全部在默认 intervals + 单一 name 下跑。

**建议**: `record` 加 `--name` (默认 `pre_merge`, 与 schema 现值一致) 与 `--config .aria/config.json` (CLI 自己读 `phase_c_integrator.pre_merge_gate.wait_check_intervals`, 顺带可把 `--threshold` 变成交叉校验而非唯一来源); `--primitive-used` 同理 (今天默认 `aether-ci-cli`, 非 Aether backend 会写错值)。SC-11 加一条: 传入非默认 intervals 时 `next_check_at` 跟随 (坏实现 = 忽略 intervals, 必红)。

---

### [A1-R3-M4] Major — 2.1 伪码对**安全**串消毒、对**危险**串不消毒: `verify-failed` 的 `detail` 是 surrogateescape 解码的 git stderr, 直接 `+=` 进 `gate_error.message`

**锚点**: spec §2.1 伪码两行 ——
```
msg = _sanitize_for_json(f"PR branch '{pr_branch}' not found on remote '{remote}'")      # 消毒了
...
out["gate_error"]["message"] += verify_note                                              # 没消毒
```
其中 `verify_note = f" (PR 分支存在性核验失败: {detail})"`。

**实读证据**
- `detail` 的来源 (`pre_merge_gate.py:340-344`): `stderr = (proc.stderr or b"").decode("utf-8", errors="surrogateescape")` → `return "verify-failed", f"git ls-remote rc={proc.returncode}: {stderr.strip()}"`。即 **detail 里装的是任意远端/本地 git 的 stderr, 且刻意用 surrogateescape 解码**。
- `_sanitize_for_json` 的 docstring (`:292-300`) 逐字说明它存在的理由: 「那些码位会在 **json.dumps 时**炸 UnicodeEncodeError —— 离现场很远。故在出口就地净化。」
- 既有 main 侧同类分支 (`:456-465`) 的写法: 先拼 `msg`(含 `mb_detail`)、**再 `msg = _sanitize_for_json(msg)`**、然后才 `_build_output`。

**问题** v3 恰好把顺序做反了: 被消毒的是由 `pr_branch`/`remote` 拼出的可控串, 不被消毒的是 `git ls-remote` 的原始 stderr。gate 输出最终要 `json.dumps` (CLI/`--json` 消费方), 于是这条路径把 `_sanitize_for_json` 当初要治的那个 bug **在自己新写的分支里原样复发** (memory `fix_recurs_in_its_own_fallback_path`), 且触发点 = 远端不可达 —— 正是最需要看到诊断的时刻。

**建议**: 伪码改为 `note = _sanitize_for_json(f" (PR 分支存在性核验失败: {detail})")` 后再拼, 并在 SC-10 的 `verify-failed` 变体里注入一个含代理对/控制字节的假 detail, 断言 `json.dumps(out)` 不抛 (坏实现必红)。

---

### [A1-R3-M5] Major — 「`continue` 后再 3 次连续观测 (~210s 后) 再次 prompt」算错; 按同一套 interval/retry 语义实算是 t≈810 (720s 后)

**锚点**: spec §3.2 时间轴段末句。

**逐轮重算** (用 `write_gate_state` 的 retry_count 递增 + `_next_check_at(retry_count)`, intervals `[30,60,120,300,300]`):

| 轮 | t | retry_count (写后) | next_check_at | obs |
|---|---|---|---|---|
| 初次 | 0 | 0 | +30 → 30 | 1 |
| #1 | 30 | 1 | +60 → 90 | 2 |
| #2 | 90 | 2 | +120 → **210** | 3 ⇒ **prompt** ✓ (t≈90 对) |
| — | 用户 `continue` ⇒ obs 归 0, retry_count **不动** | | | 0 |
| #3 | 210 | 3 | +300 → 510 | 1 |
| #4 | 510 | 4 | +300 → 810 | 2 |
| #5 | 810 | 5 | +300 → 1110 | 3 ⇒ **第二次 prompt** |

⇒ 第二次 prompt 在 **t≈810** (距第一次 720s), 不是 210s。「~210s 后」无论读成「t≈210」还是「再过 210s」都不对 —— 210 恰是 `continue` 后**第一次**重查的时刻, 那时 obs 才 1。

**为什么算 Major 而不是 typo**: 这个数会被抄进 `workflow-runner/SKILL.md` 2.5 与 config 注释 (§5 明列这两处), 是给人看的行为承诺; 且 AD-4「代价有界 = `continue` 即回到等待」的说服力直接依赖它。更要紧的是形状: 时间轴 off-by-N 这是**第三次**复发 (R1-M1 → R2-M2 → 本条), 前两次修在「初次是否计数」和「先写后判」上, 这次跑到 `continue` 之后的那段新文字里 (memory `fix_recurs_in_its_own_fallback_path` + `perpetual_red_fix_must_change_the_quantity_not_the_threshold`)。

**建议**: 把该句改为「`continue` 后计数从 0 重来, 下一次 prompt 落在**再 3 次重查之后**; 默认 intervals 下 ≈ t 810s (间隔已进入 300s 档) —— 精确值随 `wait_check_intervals` 与阈值变化, 不要在别处复述秒数」。另: `wait_timeout_seconds` 默认 1800 下这条路径仍有余量 (810 < 1800), 值得在 spec 里点一句, 免得实施者以为 2.5 会被 exit 2 吃掉。

---

### [A1-R3-M6] Major — 处方 (a) 行的开关 `dispatch_viable` 只存在于一个 **authoring-time** references 文档里, 运行时渲染 prompt 时无任何机制保证它在上下文中; 且它=false 时 §4 沦为零消费方字段

**锚点**: spec §3.3 (a) 行的方括号条件「仅当 traps §6 `dispatch_viable=true` 且列表非空」· §3.5 末句「`dispatch_viable` 唯一影响面 = 3.3 处方 (a) 行是否出现; §4 与全部 SC **不随之变化**」· R-c

**实读证据**: `references/pre-merge-gate-empirical-traps.md` 在 `phase-c-integrator/SKILL.md` 里**只被引用一次** (`:240`), 措辞逐字是「📌 **改这段代码前先读**」—— 这是**给改代码的人**的 authoring-time 指引, 不是 C.2.4 运行时的加载指令。runtime prompt 的其余变量都有机读来源 (`gate_error.message`、`prompt_after_observations`、`path_coverage.dispatchable_workflows` 全在 gate 输出里), 唯独这一个布尔靠「AI 恰好读过那份 reference」。

**问题**
1. **两种实现分叉**: 一个实施者恒列 (a), 另一个恒不列, 两者都能通过全部 SC (没有一条 SC 覆盖 (a) 行的条件化)。这是把 R2 #6 从「TASK-0 成环」解出来后, 布尔的**消费侧**没跟着解。
2. **「唯一影响面」主张只成立一半**: `dispatch_viable=false` 时, §4 新加的 `dispatchable_workflows` 就**没有任何消费方**了 —— 而 SC-8/SC-9 仍在它上面取绿。这正是本项目反复点名的「有记录无路由」形状 (memory `fix_recurs_in_its_own_fallback_path` 的后半句)。§4 无条件实现是对的 (它解了环), 但 Risks/R-c 应当诚实写出这个分支后果, 而不是声称影响面只有一行。

**建议** (二选一): (a) 把开关搬到有运行时通道的地方 —— 最省的是让 `_no_run_gate_error` 直接把 (a) 行**已渲染好的命令串**放进 message/`gate_error`, 由代码按 `dispatchable_workflows` 是否非空决定 (dispatch_viable 则退化为「TASK-0a 若判 false, 实施时不生成该串」的 authoring 决定, 落在代码而非 prompt 渲染时); (b) 保留文档开关, 但在 §3.3 明写「渲染 prompt 前必须读 traps §6」并把这句放进 SKILL 的运行时步骤 (不是 references 链接), 同时在 R-c 补一句 `dispatch_viable=false ⇒ §4 字段暂无消费方, 保留理由是 (…)`。我倾向 (a)。

---

### 次要 (minor)

- **[A1-R3-m1]** 3c' 无条件解引用 `out.gate_error.kind` / `out.gate_error.prompt_after_observations`, 但**最常见**的 wait 路径 (`pr_ci_status=pending`) 根本没有 `gate_error` (`_build_output` 仅 `is not None` 时入键)。应明写「`gate_error` 缺席时省略这两个旗标; CLI 无 `--gate-error-kind` ⇒ obs 归 0」并给 `--threshold` 定默认。
- **[A1-R3-m2]** `verify-failed` 仍报 `kind=no-run-for-branch`, 与 2.3 自己的二维消歧表矛盾 —— 表逐字说「**分支存在** × run 不存在 = `no-run-for-branch`」, 而 verify-failed 恰恰是「没能证明分支存在」。要么表改成「分支存在或未能证否」, 要么承认 kind 封闭集应为 5 (加 `pr-branch-verify-failed`, 仍 `verdict=wait`)。另: 追加后缀使 message 不再是 2.3 封闭表的成员, 该表应注明「verify-failed 时为表项 + 后缀」。
- **[A1-R3-m3]** SC-7 的总体自相矛盾: 标题说「七个早退落点」, 列了 **8** 个行号, 而这 8 个实际只覆盖 **6** 个不同落点 (`:418` enabled / `:363`+`:376` no-backend 两变体 / `:434` precheck / `:455`+`:458` main 核验的两个 kind —— 但这两支共用**同一个** `return` (`:465`), 与「no-backend 两 fallback 算一落点两变体」的计数法不一致 / `:489` in-flight query err / `:512` pr query err), 且漏了 `not_applicable` 短路 (`:498-506`)。SKILL `:288/:290` 的既有 taxonomy 又是「四类 + 第五类」。断言前先钉计数法 (memory `critique_repeats_the_error_it_names`)。
- **[A1-R3-m4]** 两个 `continue` 的跨条件副作用未定义: exit 2 的 `continue` 逐字是「reset `retry_count` + 继续」(SKILL `:356`), 对 `no_run_observations` 无规定; 2.5 的 `continue` reset obs 而不动 retry_count。于是 timeout prompt 用户选 continue 后, 下一轮 obs 可能立刻达阈 ⇒ 30s 内连出两个不同 prompt。应明写 exit 2 的 continue 是否一并 reset obs (我建议一并 reset, 与「用户刚表态继续等」的语义一致)。
- **[A1-R3-m5]** §5 落点漏 `.gitignore`: 现有三个 telemetry 分区全在 `.gitignore:19-21`, `workflow-state.json` 在 `:6-7`。新 `.aria/gate-state-telemetry.jsonl` 不登记 ⇒ 要么污染 `git status` (state-scanner 会报)、要么被误提交。连带: SC-13/SC-16 的证据落在**未受版本控制**的本地文件上, 评审时不可见 —— 活体证据应抄一份进 spec 或 traps §6 (与 TASK-0a 的证据处置同构)。

---

## Verdict

**verdict: PASS_WITH_WARNINGS · vote: REVISE** (critical 0 / major 6 / minor 5)

设计收缩这一步走对了, 且我 R2 的 C1 方向被真正采纳 (不是文字打补丁)。但 v3 为「证明接线是真的」而新建的那台机器 —— CLI telemetry + 主仓 14d liveness 探针 —— 自身有 M1/M2 两个结构性问题, 而它并不是 #152 的必要组成。

**距离最短的处置 (请一并上呈 owner, 我的推荐是 ①)**

1. **切掉 liveness 探针子设计 + 5 处行级修补** (推荐)。删 §3.1 的 state-check + 14d 窗口与 SC-16, 改为: CLI 照建、SKILL 照改 (真接线不动)、SC-13 活体产出的 state 片段与 telemetry 行**抄进 traps §6 作 tracked 证据**。这一步同时消掉 M1+M2+m5 的一半。其余 M3 (CLI 加两个旗标) / M4 (一处 `_sanitize_for_json`) / M5 (一句秒数) / M6 (开关搬进代码或搬进运行时步骤) 都是行级。预计 v4 diff < 40 行。
2. **保留探针但补齐先例的三件**: 加 `source` 分区 + 分区路径定死 + 探针与生产者同仓 + 给出「无 wait 事件即 skip」的判据。这是把 M1/M2 修完整的路, 代价是再引入一小块子系统 (照 R1→R3 的经验, 它自己会再生一批审计面), 且需要为「skip 条件」找一个 wait 计数源。
3. **原样进 A.2, 六条 Major 转成 tasks 的实施注记**。可行但违背 post_spec 的用途 —— M3/M4 会以缺陷形态落地 (静默配置回归 / 远端不可达时崩在 json.dumps), M1/M2 会以「一条没人看的红 warning」落地。

**关于再开一轮**: 我这轮 6/6 Major 仍全在 v3 新文字上 (memory `marginal-return-negative` 的拐点判据再次命中)。但与 R2 的情形不同 —— 这轮没有「子设计整体是缺陷发生器」的信号, 修法是定点的。建议 **v4 由主控直接落上述 ①, 然后单席 (我或换新鲜眼睛一席) 只复核这 5 处 + 切除后的残留前提, 不再开五席 R4**; 若 owner 选 ②, 则应换席位复核 (同一批眼睛对同一台机器的边际产出已经很低)。
