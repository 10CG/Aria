---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T08:52:24.000Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 1
minor_count: 5
---

# post_spec R4 (末轮) — A4 code-reviewer 席 (spec↔代码逐行 / 引用准确 / 实施者分叉 / 同步面)

审计对象: `openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md` (Draft v4, R3-fix)
基线: aria @ `400f0bc` (实核 `git rev-parse --short HEAD`, 工作树干净)。全部结论基于实读 `pre_merge_gate.py:40-580` / `gate_state_helper.py` 全文 / `path_coverage.py:18-40,455-510` / `ci_backends/{aether,base}.py` / 两份 SKILL.md / `workflow-state-schema.md:30-133` / `runtime-probe-declaration.md` + `lib/runtime_probe.py:183-191,258-291` / AB catalog + NEG-3 fixture / 主仓 `.gitignore` `config.template.json` `config-loader/SKILL.md:242-283` `state-checks.yaml:244-264` / `forgejo GET issues/177` 全文 / 主仓 `grep -rn 1.66.3` + 实跑 `scratchpad/r4_a4_sim.py` (在真 helper 上叠 v4 §3.1 语义复算 SC-11(a) 与 90/810 时间轴)。

## 摘要

归我席的 7 个簇 (#2 #3 #4 #5 #8 #9 #10) **全部 closed**; 簇 #8 按 #177 全文逐点对照 + `grep 1.66.3` 实核: 主仓 14 个版本字符串点 (`CLAUDE.md:139,:141` 2 + `VERSION:24` 1 + `README.md:8,:242` 2 + i18n 3×3=9) 一个不多一个不少, aria 侧 5 文件 6 点 (`marketplace.json:3/:16`) 亦对。簇 #2/#3/#4 的字面我在真 helper 上模拟实跑: obs 1/2/0/1、retry 0/1/2/3、`started_at` 不变 (SC-11(a) 成立), 首次 prompt t=90 / 第二次 t=810 / 第三次 t=1710 (<1800) 全部复算成立。2.3 表 trigger-matched 档与 3.3 (a) 行字符级一致 (basename / `{o}/{r}` / `<pr_branch>` 两处同形, 分工「gate 渲染、AI 填两占位」两处同说)。

残余 **1 条 Major**: v4 把 gate_state 的写入权**整体**交给 CLI (AD-7「不再手写 JSON」) 之后, §3.2 的两条 CLI 调用行 (步骤 2 / 3c') 都**没传** `--in-flight-runs` 与 `--raw-message` —— 这两个旗标在 §3.1 签名里有、在调用行里没有; 照 SKILL 字面执行, 生产 `gate_state.in_flight_runs` 恒 `[]`、`raw_message` 恒 `""`, 与基线 `:345`「in_flight_runs[] 全部填充」和 v4 自己 §5 row 12「wait 态携处方文案注」两处契约相悖, 且 SC-11(d)/SC-13 零断言。修法一行。其余 5 条 minor 全是行级 (旗标传递条件 / 既有 timeout-continue 的 `started_at` / SC-2 计数 / 四处引用漂移 / `ts` 格式与 helper 自述)。

A1 本轮已报的 telemetry 根 (A1-R4-M2)、`--source` 缺省与「镜像 anti-spoof」措辞 (A1-R4-M3)、exit 2 双义 (A1-R4-m4)、gitlink 14/15 断句 (A1-R4-m3)、A2 已报的 dispatch 渲染 SC 零覆盖 (A2-R4-M1) —— 我独立核到同样的事实, **不重复立项**, 只在核对表注明。

## R3 处置核对

| 簇# | 状态 | 证据 (实读 v4 + 源码) |
|---|---|---|
| #2 (A1-R3-M3 + A4-R3-M2 + A4-R3-m2: CLI 漏 `--name`/`--intervals`、wait≠waiting、`elapsed_seconds`) | **closed** | §3.1 签名封闭: `record --name pre_merge --verdict {wait\|green\|fail}` + 「CLI 内映射 wait→`GATE_STATUS_WAITING("waiting")`, green/fail 同名」(对照 `helper:32-34` 三常量 ✓); `--intervals JSON` 默认 `DEFAULT_INTERVALS_SECONDS` (`:38` ✓); stdout 五键含 `elapsed_seconds`; SC-11(d) 独立重读断言 `status == "waiting"` 且 `retry_count == 1` —— 我 R3 点名的双记账坏实现 (obs 用 "wait" 计、retry 用 "waiting" 判) 在此必红 ✓。模拟实跑 (`r4_a4_sim.py`): 映射后 4 次调用 retry 0/1/2/3 递增、`is_gate_active` 为真 |
| #3 (A1-R3-M4 + A2-R3-M1 + A4-R3-M1: 两处哨兵 + 消毒) | **closed** | §2.1 `verify_note = ""` 位于 `if pr_status.state == "not_found":` 之前 (插入点 = `:518` 与 `:521` 之间 ✓); `elif st != "ok": verify_note = _sanitize_for_json(f" (…{detail})")` 整段后缀经消毒, 与 `:464` main 侧先消毒后拼装同形 ✓; §2.2 注释「`gate_error` 在函数开头初始化为 None」= 紧邻 `:196 raw_message = ""` ✓, 其余五个分支经 `_build_output:273` 不入键 ⇒ SC-7 键集不变 ✓ |
| #4 (A1-R3-M5 + A1-R3-m4 + A4-R3-M3: 810s / exit 2 reset 路径 / 双 prompt) | **closed** | `reset [--observations] [--retry-count]` 子命令 (至少一旗标) 进封闭集; exit 2 continue = 两者都 reset, 2.5 continue = 只 reset obs; 时间轴 90/810 模拟实跑成立 (第三次 1710, 仍 <1800)。first-match-wins 下 exit 2 先于 2.5 ✓。残余: timeout-continue 不重置 `started_at` 是**既有** `:356` 的缺陷, v4 只是把它机械化 → m2 (minor, 非本 spec 引入) |
| #5 (A1-R3-M6 + A4-R3-M4 + A3-R3-M1: basename / `dispatch_viable` 运行时落点 / 布尔映射) | **closed** (机制) | `DISPATCH_VIABLE` 模块常量 + `_no_run_gate_error` 在 `DISPATCH_VIABLE and dispatchable_workflows` 时渲染进 message, 路径取 basename (对照 `path_coverage.py:489` `matched.append(rel)` 元素确为 `.forgejo/workflows/x.yml` ✓); `dispatch_viable := 600s 内观测到 run`, `queued-unobserved` 标签 ✓; 2.3 表 ↔ 3.3 (a) 字符级一致 (见摘要)。**SC 零覆盖**已由 A2-R4-M1 立项, 本席不重复; `false` 时常量零消费 A1-R4-m6 已报 |
| #8 (A4-R3-M5 + A5-R3-M1: 版本引用点 cite≠apply) | **closed** | 逐点对照 #177 原文 + 现网 grep (本轮实跑): 主仓 `CLAUDE.md:139`「v1.52.0–v1.66.3 已 ship」+ `:141`「版本: 插件 aria-plugin v1.66.3」/ `VERSION:24` / `README.md:8` badge + `:242` Plugin Version / `README.{zh,ja,ko}.md` 各 `:3` translated-from + `:10` badge + `:244` Plugin Version = **14**, 与 #177「14 个引用点」逐字吻合, **无漏无多**; gitlink 另计 (#177 不计它, A1-R4-m3 已指断句歧义); aria 侧 `plugin.json:4` / `marketplace.json:3,:16` / `VERSION:3` / `CHANGELOG:13` / `README.md:5` ✓。「`CLAUDE.md:5` 非 #177 所指, 不动」现在是附注而非替代, 正确 |
| #9 (A3-R3-M2 + A4-R3-m4: NEG-3 零执行 / catalog version·changelog·元键集) | **closed** | SC-15「真跑一次 + 落 `ab-results/<date>-…/`」+ catalog `version` bump + `changelog` 行 + `test_case_in_unit_tests` 绑 SC-2 ✓ (实读 catalog: `version 1.1.0`, `changelog` 仅 1.0.0 一条, 7 fixtures ✓)。残余: 「元键集 = NEG-3 全集」后的枚举只列 6 个, 实物 8 个 → m4 |
| #10 (A4-R3-m1/m2/m3 等 minors) | **closed** | 新名桩进 mixin「默认 `("ok","")`, 逐测试按需覆盖」✓; `elapsed_seconds` 入 stdout ✓; `:278-288`/`:305-319`/`:404-408` 注释 + `:548-552` help 成 §5 row 15 ✓ (行号实核: 段首注释 278, docstring 303-319, 「subprocess 调用数 0 或 1」在 407, help 551); Impact 新 artifact 五项 ✓; Why 段「~2/3」改「15-19 条 (34%-43%)」✓ |

小计: closed 7 / partial 0 / not_addressed 0。

## 新 Findings

### [A4-R4-M1] Major — §3.2 两条 CLI 调用行 (步骤 2 / 3c') 漏传 `--in-flight-runs` 与 `--raw-message`: AD-7 把写入权整体交给 CLI 后, 生产 `gate_state` 的两个快照字段恒空, 与基线 `:345` 和 v4 自己的 §5 row 12 互斥, 零 SC

- **锚点**: §3.1 CLI 签名含 `[--in-flight-runs JSON] [--raw-message S]`; §3.2 步骤 2「首个 wait verdict → 创建 gate_state **也经** CLI record (is_first ⇒ retry_count=0, obs=1 若带 kind) # 非 AI 手写 JSON」; 3c' 逐字 `record --name pre_merge --verdict out.verdict --intervals <cfg.wait_check_intervals> [--gate-error-kind … --threshold …]` —— 方括号把可选旗标**显式**列出, 这两个不在其中; 3d「禁止回退手写 JSON」; AD-7「AI 经 subprocess 调 CLI 而非手写 JSON」。
- **与之相悖的三处契约**: (i) 基线 `workflow-runner/SKILL.md:345`「started_at / retry_count / next_check_at / in_flight_runs[] **全部填充**」(§5 row 11 把 `:345` 列为同步面, 但改成什么没写); (ii) `workflow-state-schema.md:123`「`in_flight_runs` … Snapshot of upstream in-flight CI runs from last check」(Required when present); (iii) **v4 自己** §5 row 12「`:125` raw_message 注 | … **wait 态携处方文案注**」—— 要让 `gate_state.raw_message` 在 wait 态携带处方文案, 3c' 必须传 `--raw-message out.raw_message`, 而它没有。
- **实施后果**: `write_gate_state(:151-153)` 对未传参数写 `in_flight_runs=[]` / `raw_message=""`。照 SKILL 字面跑, 每个 wait episode 的 `gate_state` 都丢失 main in-flight 快照与 gate 文案 —— `verdict=fail` 时「保留 gate_state 给 audit trail」(`:355`) 留下的是一个空壳; resume / 别的终端读 state 看不到 gate 在等什么。基线 (AI 手写) 有这两个字段, 这是**静默回归**。
- **两实施者分叉, 无 SC 区分**: 读签名的那位会传 (state 有快照); 照 3c' 抄进 SKILL 的那位不传 —— 而 SKILL 文本就是生产指令。SC-11(d) 只断言 obs / status / retry_count / next_check_at / telemetry / should_prompt; SC-13 只断言 `no_run_observations` 出现。两版全绿。
- **修法 (一行 + 一句 SC)**: 步骤 2 与 3c' 都补 `--in-flight-runs '<json(out.in_flight_runs)>' --raw-message '<out.raw_message>'` (`raw_message == gate_error.message` 副本通道, 正好落实 row 12); SC-11(d) 加「record 带 `--in-flight-runs '[{"run_id":1}]' --raw-message x` 后独立重读 `gate_state.in_flight_runs == [{"run_id":1}]` 且 `raw_message == "x"`」; §5 row 11 对 `:345` 写明改后文案「五字段全部由 CLI record 填充 (AI 传 out 的 in_flight_runs / raw_message)」。

### [A4-R4-m1] Minor — 3c' 「两旗标仅 out 含 gate_error 时传」对 `fail` 类 kind 不成立: `pr-branch-not-found` / `main-branch-*` 的 `gate_error` **无** `prompt_after_observations` 键

- 2.3 钉死只有 `no-run-for-branch` 带 `prompt_after_observations`; 而 3c' 在 3d 之前执行 (「先自增, 后求值」), gate 重查若返 `fail + gate_error.kind=pr-branch-not-found`, 字面规则要求传 `--threshold out.gate_error.prompt_after_observations` —— 键不存在。AI 传空/None ⇒ CLI exit code 2 ⇒ 按 R-e 走「CLI 失败 prompt」, 在一个本该直接 stop 的 fail verdict 上多弹一次。修法: 改为「两旗标仅当 `out.gate_error.kind == "no-run-for-branch"` 时传」。

### [A4-R4-m2] Minor (既有缺陷, 非本 spec 引入) — exit 2 `continue ⇒ reset --retry-count --observations` 不重置 `started_at`, 而 exit 2 的判据之一 `elapsed > wait_timeout_seconds` 用的正是 `now − started_at`

- `DEFAULT_CONFIG` / 两张配置表都**没有** `max` 旗标 (`retry_count > max` 无配置来源), exit 2 实际只由 `elapsed` 触发。timeout-continue 后 `reset` 只动两字段 (v4「只动指定字段」), 下一轮 (30s 后) `record.elapsed_seconds` 仍 >1800 ⇒ exit 2 再弹, 每 30s 一次。v4 为 2.5 专门写了「避免 30s 内再弹」, 同形状留在 exit 2 自己身上。基线 `:356` 同病 (AI 手写时亦未定义), 故判 minor; 顺手修法一行: `reset --retry-count` 同时置 `started_at = now` (timeout-continue 语义 = 重开计时), 或加 `--started-at` 旗标并在 exit 2 continue 传。

### [A4-R4-m3] Minor — SC-2「参数化 8 reason + None」与 2.3 封闭表只定义 6 个 reason 的档位矛盾

- reason 族 8 = covered×3 + unknown×3 + not_applicable×2 (`no-workflow-files` / `no-triggering-paths`, 实读 `path_coverage.py:466-509`); 2.3 表对 `not_applicable` 只写「结构上不可达, SC-6 钉死」, 没有 message 行。直调 `compute_verdict([], "not_found", path_coverage={"decision":"not_applicable",…})` 时 `_no_run_gate_error` 该返什么, 两实施者一个 KeyError 一个兜底文案, SC-2 写 8 就必须给后两档一个期望值。修法二选一: SC-2 改「表内 6 reason + None」(不可达档由 SC-6 覆盖); 或 2.3 加一行防御性默认档「其它 decision → 『远端零 run; 覆盖判定非预期 (decision=…)』」(fail-closed 兜底, memory `invariant_needs_failclosed_default`)。

### [A4-R4-m4] Minor — v4 diff 级四处引用漂移 (稳定性核查)

1. §5 标题「逐位置, **17 处**」, 表实有 **18** 行 (v4 新增 `.gitignore` 行未计入; `awk` 实数)。
2. §5 row 18「元键集 = NEG-3 全集: `_description`/`_target_behavior`/`_discriminating_question`/`_arm_expectations`/`_consumed_by`/`_ships_with`」列 6 个, 实读 NEG-3 为 **8** 个 (漏 `_fixture_id` / `_why_the_distinction_matters`); 「= 全集」为准, 枚举应补齐或删枚举。
3. §5 row 5「`:255-263` 步骤 4/5/6」— 实核步骤 4 在 **`:252`**, 步骤 5 `:253`, 步骤 6 `:260`; 应为 `:252-263`。
4. §5 row 13「`config-loader/SKILL.md` … 登记两 key」— `config-loader/SKILL.md:283` **已有** `path_coverage_enabled`, 只缺 `no_run_prompt_after_observations`; 「同时补 #122 漏登的 `path_coverage_enabled`」只对 `.aria/config.template.json` (`:73-91` 实核确无) 成立。另: §5 表里 row 13/14/16/17/18 是**主仓**文件、其余是 aria-plugin 文件, 建议加「仓」列 —— `.gitignore:19-21` 只在主仓成立 (aria/.gitignore 仅 16 行)。

### [A4-R4-m5] Minor — telemetry `ts` 格式与 helper 自述未钉

- `lib/runtime_probe.py:183-191` 只认 `datetime.fromisoformat(ts.replace("Z","+00:00"))` 可解析的**字符串**; 写 epoch 数值 ⇒ 记录永不计入 ⇒ SC-16 恒 warn (红窗在 D.2, 太晚)。修法: §3.1 钉「`ts` = helper `_utcnow_iso()` 格式 (`%Y-%m-%dT%H:%M:%SZ`)」并在 SC-11(d) 加「telemetry 行 `ts` 经 `fromisoformat` 可解析」。
- `gate_state_helper.py:2-18` 模块 docstring 自陈「markdown-driven (LLM caller handles state)」「Usage (Python)」—— F7 就是拿它做证据的; CLI 接线后这段成反证据, §5 未列。加进 row 11 或新行 (描述性, substitute 归 SC-14 机检亦可)。

## 未发现问题但已核验的点

- §2.1 伪码变量/关键字 (`in_flight.runs` / `pc` / `backend.name` / `pr_status.state` / `_build_output` 七关键字) 与 `:485-527` 逐字同; `not_applicable` 短路 `:498` 在 `:509` `query_pr_ci` 之前 ⇒ 2.3「结构上不可达」✓。
- SC-7 「六个 return 点 / 八个变体」行号 (`:418/:428/:363/:376/:434/:454/:455/:458/:489/:512`) 全部指向各早退的控制行或 return 行 (±2 行内), 键集断言「前五类六键, main 核验七键」与 `_build_output:266-275` 一致。
- `_effective_prompt_threshold` 语义 (2.2) ↔ SC-3 五例 + 缺键不 warn 一致; `DEFAULT_CONFIG:57-69` 确无该键, `config-template-key-currency` 探针 (`state-checks.yaml:244-264`) 对「模板键 ⊆ DEFAULT_CONFIG」fail-closed, 落点顺序提醒成立。
- `runtime_probe:` 三字段符合 `runtime-probe-declaration.md` schema (2-space 缩进 / 行尾 ` #` 注释剥离 / 无 `enabled_when` ⇒ 恒跑); `symbol` 仅标签, 不做记录级过滤 ✓。
- R1/R2/R3 簇号引用 (R1 #6 / R1 A2-M1 / R2 #1-#3,#4/#5,#6,#9,#14 / R3 #1-#7,#9) 与三份聚合表逐一对上; Status 行「R3 5/5 REVISE (0 Critical, 10 簇)」✓。
- DEC-20260731-001 小节「退役裁定 (2026-07-31)」`:21` 存在, 先例 DEC-20260702-001:124-128 前向指针格式存在 ✓。
- `path_coverage.py:36`「共 9 个」实为 8 (7 终态 + internal-error), 勘正方向正确 ✓。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 1 Major / 5 Minor) — **vote: REVISE**

归我席 7 簇全部真落地, 版本引用点与 CLI/哨兵/时间轴三组反复复发的点本轮按源码与模拟实跑钉住。唯一 Major (M1) 是 v4 新机制 (写入权整体交 CLI) 的接缝: 调用行漏两个旗标 ⇒ 生产 state 两字段静默回归, 且与 v4 自己 row 12 的承诺互斥 —— 满足「契约破坏 + 两实施者分叉 + 无 SC 区分」门槛, 修法一行 + 一句 SC, 不动任何设计。五条 minor 全可在 A.2/Phase B 顺手钉。**建议主控**: 与 A1 (3 Major, 全在探针配件) / A2 (1 Major, dispatch SC) 合并为一次定点修 (预计 <20 行), 不必再开第五席轮。
