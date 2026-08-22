---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-22T08:13:51.671Z
context: openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A4-code-reviewer
critical_count: 0
major_count: 5
minor_count: 4
---

# post_spec R3 — A4 code-reviewer 席 (spec↔代码逐行 / 引用准确 / 实施者分叉 / 回归面 / 同步面)

审计对象: `openspec/changes/pre-merge-gate-no-run-for-branch/proposal.md` (Draft v3, R2-fix + 设计收缩)
基线: aria @ `400f0bc` (实核 `git rev-parse --short HEAD`, 工作树干净)。全部结论基于实读 `pre_merge_gate.py` / `ci_backends/aether.py` / `path_coverage.py` / `gate_state_helper.py` / 两份 SKILL.md / `workflow-state-schema.md` / AB catalog / 主仓 `state-checks.yaml` + 实跑 `scratchpad/r3_a4_demo.py` + `forgejo GET issues/177` + `git show --stat 451aba0` (上一次 PATCH ship 的同步面实证)。

## 摘要

归我席的 9 个簇 (#3 #4 #5 #6 #7 #8 #9 #10 #14) **全部 closed**: 第八早退的伪码变量名 (`in_flight.runs` / `pc` / `backend.name` / `pr_status.state`) 与 `_build_output` 七个关键字**逐字对上真代码** (`:236-245` / `:485-527`); 包装函数方案我按三处 (`:449` 关键字调用 / mixin `:85-89` 打桩 / `MainBranchExistenceTests:803` 刻意不继承 mixin 走真 ls-remote) 逐一推演**都成立**, `timeout` 默认值丢失的回归面为零 (唯一调用点显式传; `aria-orchestrator` 零引用) — A2-R3-m2 维持 minor 即可。

残余 5 条 Major 全是 v3 把散文落成具体伪码 / CLI 签名后浮出的**接缝**, 每条修法都是行级: (M1) 2.2 伪码的 `gate_error` 与 2.1 的 `verify_note` 是**同一形状**的作用域缺陷 (A2-R3-M1 只报了一个实例), 实跑证实非 `not_found` 分支必抛 `UnboundLocalError`, 两处的字符级修法在下; (M2) CLI `record --verdict wait` 与 helper 的 `GATE_STATUS_WAITING = "waiting"` **枚举不同**, spec 未钉映射, 实跑: 直传 `"wait"` ⇒ `retry_count` 恒 0 / `status` 非法 / `is_gate_active` False (resume 断) 而 SC-11 对这三项零断言; (M3) exit 2 的 `continue → reset retry_count` 在 v3「禁止手写 JSON」下**没有 CLI 路径**; (M4) 处方 (a) 的 `<file>` 实际来源 `dispatchable_workflows[]` 装的是 `.forgejo/workflows/x.yml` 相对路径, 直接拼进 `/actions/workflows/{file}/dispatches` ⇒ 404, 同时给出 `dispatch_viable` 的运行时落点 (与 A1-R3-M6 合修); (M5) 版本引用点行**误引 #177**: #177 第 2 错逐字是「漏 `CLAUDE.md:139` + `:141`」, v3 却写「`CLAUDE.md:5` 不动」(那行根本不是 #177 点名的), i18n 9 点亦未枚举 — 上一次 PATCH ship (`451aba0`) 实际触了 14 点。

## R2 处置核对

| 簇# | 状态 | 证据 |
|---|---|---|
| #3 (A4-R2-M1 + A1-R2-M2: 先判后写 90s/210s) | **closed** | §3.2 3c' 「先自增, 后求值」+ `record` 返 `should_prompt`; 时间轴 t=0/30/90 我按 `_next_check_at(retry_count)` (`helper:103-110`) 与 `write_gate_state` 递增规则复算成立。continue 后那句秒数 A1-R3-M5 已报, 不重复 |
| #4 (A4-R2-M3: 伪码 verdict 写死 / `pr_branch_check` 形参) | **closed** | 改第八早退 `_build_output(verdict=fail, gate_error={"kind":"pr-branch-not-found"})`, `compute_verdict` 无新形参; 伪码的 7 个 `_build_output` 关键字 (`verdict/pr_ci_status/in_flight_runs/primitive_used/raw_message/path_coverage/gate_error`) 与 `:236-245` 签名逐字同; 变量名 `in_flight` (`:486`) / `pc` (`:476`) / `backend.name` / `pr_status.state` (`:509/:523`) 全对。新引入的作用域缺陷 → M1 (类级, 含 A2-R3-M1 实例) |
| #5 (A4-R2-M2: 包装函数可实现性) | **closed** | 钉法逐字落地: 新主体 `_verify_branch_exists(branch, remote, timeout)` + 旧名包装保 `main_branch=` 关键字 + `:449` 不改 + PR 调新名 + 两名各打一桩。三处推演: (i) `:449-453` 关键字调用经包装 → 不 TypeError; (ii) mixin `:85-89` `patch.object(gate, "_verify_main_branch_exists")` 替换的是包装, 28 测试继续不打网络; (iii) `MainBranchExistenceTests:803-808` 刻意不继承 mixin, 经包装→新名→真 `ls-remote`, 5 条承重测试仍测到真函数体 (`subprocess.run` 仍在 `gate` 模块命名空间查找)。`timeout` 默认值 (A2-R3-m2): 回归面零 — 唯一调用点 `:452` 显式传, 测试零直调, orchestrator 零引用; 维持 minor。残余: 新名桩**放哪** 未钉 → m1 |
| #6 (A4-R2-M5: TASK-0 成环) | **closed** | TASK-0a 实现前纯 API 探针, 不依赖本 spec 代码; §4 无条件实现, SC-8/9 恒跑; 三分支结果落 traps §6。布尔的运行时消费 A1-R3-M6 已报, 我在 M4 给合并钉法 |
| #7 (A4-R2-M4: prompt 出口 / 每 interval 复弹) | **closed** | 自动动作整体删除; 2.5 是真终止型 exit condition, `continue ⇒ reset-observations` / `abort ⇒ fail` 各一行; first-match-wins 下 exit 2 先于 2.5, 结构上不双弹。残余是 prompt 占位符的数据来源 → M4 (`<file>`) / m2 (`<elapsed>`) |
| #8 (A4-R2-M7: NEG-4 未登记 / #127) | **closed** | SC-15 要求登记 `fixtures[]` + `test_case_in_unit_tests` 绑 SC-2 + 回退转红锚; rule6_note 直接点名 aria-plugin#127 (open, 实核)。R2 钉法里 catalog `version` 1.1.0→1.2.0 + `changelog` 补行 + `_consumed_by`/`_ships_with` 键被 v3 缩掉 → m4 |
| #9 (A4-R2-M6: 校验位置 / DEFAULT_CONFIG / 误引 SC-10) | **closed** | `_effective_prompt_threshold(cfg)` 唯一校验点, 两路径同经; `DEFAULT_CONFIG` (`:57-69`, 实核无该键) 列入落点; SC-10 误引已消失 (改引函数名) |
| #10 (A4-R2-M8: §5 漏 3 处) | **closed** | workflow-runner `:249-264` / `:345` / schema `:38-52` / `aether.py:218` 四处全部补进 §5 (我逐行号复核: `:247-263` JSON 块、`:345` 字段枚举、`:389` wait 分支、schema `:40` status 行均在)。另发现的漏点属代码注释与版本行 → M5 / m3 |
| #14 (A4-R2-m1~m4) | **closed** | reason 族 8 + 三档前缀匹配 ✓ (对照 `path_coverage.py:422/:432/:447/:500` 真实载荷); `pr-branch-not-found` 的 pc 随 enabled ✓; Impact 补 additive 签名 ✓ (新 artifact 漏 → m3); `:363` ✓ (实核 `test:363` 是 `[] → "pending"` 断言行); traps 为 SOT + memory 镜像 ✓ |

小计: closed 9 / partial 0 / not_addressed 0。

## 新 Findings

### [A4-R3-M1] Major — 2.2 伪码 `gate_error` 与 2.1 伪码 `verify_note` 是**同一形状**的作用域缺陷 (两实例); 逐字实现则所有非 `not_found` 路径抛 `UnboundLocalError`

- **锚点**: §2.1 伪码 `:74` (`verify_note = ...` 缩进在 `if pr_status.state == "not_found":` 内) 与 `:77` (`if verify_note and ...` 在块外) — A2-R3-M1 已报此实例; §2.2 伪码 `:91-96`: `elif pr_ci_status == "not_found": ... gate_error = _no_run_gate_error(...)` 后 `return _build_output(..., gate_error=gate_error)` — `gate_error` 只在该 `elif` 赋值, 而 `compute_verdict` 现有五个分支 (`:197-224`) 都不赋它。
- **实跑** (`scratchpad/r3_a4_demo.py`): 按 2.2 字面结构 `pr_ci_status="pending"` ⇒ `UnboundLocalError`。`ComputeVerdictTests` (`test:102`) 四条 + 全部走到 `:521` 的 gate_check 测试都会红 — SC-12「既有 119 全绿」不可能成立。
- **为什么算 Major 而不是并进 A2-R3-M1**: memory `fix-the-class`: 修一个实例必问「同形状还有几个兄弟位置」。2.1 与 2.2 是同一个 R2-fix (簇 #4) 新写的两段伪码, 各漏一个哨兵初始化; 只修 2.1 会让 2.2 在实现时原样复发。
- **字符级修法** (两处一起):
  - §2.2: 在 `raw_message = ""` (`:196`) 之后加一行 `gate_error: dict[str, Any] | None = None`; `elif pr_ci_status == "not_found":` 分支内三行不变; `return _build_output(..., path_coverage=path_coverage, gate_error=gate_error)` (其余分支 `gate_error=None` ⇒ `_build_output:273` 不入键, SC-7 键集不变)。
  - §2.1: `if pr_status.state == "not_found":` 之前加 `verify_note = ""`; 块内改为 `elif st != "ok": verify_note = _sanitize_for_json(f" (PR 分支存在性核验失败: {detail})")` (把 A1-R3-M4 的消毒一并落在这一行, 与 `:464` main 侧先消毒后拼装的顺序同形); 块外 `if verify_note and out.get("gate_error"):` 保留。
  - SC-2 已覆盖 `compute_verdict` 的 `not_found` 分支; 加一句「SC-12 既有测试是本条的红窗: 漏哨兵 ⇒ `ComputeVerdictTests` 必红」即可, 不需新 SC。

### [A4-R3-M2] Major — CLI `record --verdict wait|green|fail` 用 gate 枚举, 而 `write_gate_state` 判的是 `GATE_STATUS_WAITING = "waiting"`; 映射未钉, 直传 `"wait"` 静默冻结 `retry_count` 并让 resume 失效

- **锚点**: §3.1 CLI 签名 `record --verdict wait|green|fail`; 同段计数条件 `verdict == waiting`; §3.2 3c' `CLI record --verdict out.verdict` (`out.verdict` ∈ `{"green","wait","fail"}`, `pre_merge_gate.py:51-53`); `gate_state_helper.py:30-32` `GATE_STATUS_WAITING = "waiting"`; `:139-140` 仅 `verdict == GATE_STATUS_WAITING and existing.status == GATE_STATUS_WAITING` 时递增; `:150` `next_check_at` 仅 waiting 时按 interval 推算; `:166-168` `is_gate_active` 判 `status == "waiting"`; schema `:40/:119` status 枚举 `waiting|green|fail`; 既有 22 测试全部 `verdict="waiting"` (`test:106-161`)。
- **实跑** (同 demo): `write_gate_state(verdict="wait")` 连写三次 ⇒ `status='wait'` (schema 非法值) / `retry_count=0` (恒不增) / `is_gate_active=False` / `next_check_at=now`。后果: exit 2 的 `retry_count > max` 永不命中; Resume 语义 (`workflow-runner/SKILL.md:380-389`) 以 `gate_state.status == waiting` 为入口 ⇒ Ctrl-C 后 resume **不恢复 polling**; `should_check_now` 恒 True。
- **SC 盲区**: SC-11(a) 直调 helper (实施者自然用 `"waiting"`, 绿); SC-11(d) 经 CLI 只断言 `no_run_observations` 1→2 与 `should_prompt`, **不断言** `status`/`retry_count`/`next_check_at` ⇒ 「obs 用 CLI 传入的 `"wait"` 计数、retry 用 helper 的 `"waiting"` 判」这种双记账坏实现 (d) 也绿。两实施者分叉 (memory `spec-underdetermination`), 且失效是静默的。
- **钉法**: §3.1 CLI 段加一句「`--verdict` 取 gate 输出枚举 `wait|green|fail`; CLI 内固定映射 `wait → GATE_STATUS_WAITING` 后再调 `write_gate_state`, 其余二值原样」; SC-11(d) 加断言: 两次 `record --verdict wait` 后独立重读文件 `gate_state.status == "waiting"` 且 `retry_count == 1` (坏实现 = 直传 ⇒ `status == "wait"`, `retry_count == 0`, 必红)。

### [A4-R3-M3] Major — exit 2 的 `continue → reset retry_count` 在「不再手写 JSON / CLI 失败禁止回退手写」约束下**没有 CLI 子命令可走**

- **锚点**: §3.2 exit 2「[不变]」+ 2.5 注「`retry_count`/`started_at` 继续累计, exit 2 上界不变」; `workflow-runner/SKILL.md:356` 逐字「timeout → user prompt; continue → reset retry_count + 继续」(§5 列 `:338-358` 为同步面但只说「§3.1-3.3」); §3.1 CLI 子命令封闭集 = `record` / `reset-observations` / `clear`; R-e「若 CLI 失败 (exit 2) AI 须 surface 而非回退手写 JSON (写进 SKILL)」; AD-7「AI 经 subprocess 调 CLI 而非手写 JSON」。
- **问题**: `write_gate_state` 只有 `is_first` (name 变或 `existing` 空) 才把 `retry_count` 置 0 (`:143-146`); `reset-observations` 只动 obs; `clear` 置 `gate_state=None` ⇒ 下一次 `record` 走 `is_first` ⇒ `retry_count=0` **且 `started_at` 重置**。于是 timeout-continue 这个既有转换在 v3 下三种实现: (a) AI 手改 JSON 的 `retry_count` (违反 AD-7/R-e); (b) `clear` + 下次 `record` (顺带重置 `started_at` ⇒ `elapsed` 归零 — 与 `:356` 只说 reset retry_count 的字面不同, 但恰好修掉「elapsed 仍 > timeout ⇒ 下一轮立即再 prompt」这个既有隐患); (c) 自行加 `reset-retry` 子命令 (spec 外)。三者行为不同, 无 SC 区分。
- **钉法** (推荐 b, 最少新面): §3.2 exit 2 改「continue ⇒ CLI `clear`; 下一轮 `record` 以 `is_first` 重建 (`retry_count=0`, `started_at=now`, obs 按 kind 重算) — 即 timeout-continue 的语义是**重开一个 episode**, `:356` 文案同步改」; 若 owner 坚持只 reset `retry_count` 则选 (c) 并把 `reset-retry` 加进 CLI 封闭集 + SC-11。无论选哪种, 顺带回答 A1-R3-m4 (两个 continue 的跨条件副作用): 选 (b) 时 obs 随 episode 一起归零, 天然一致。

### [A4-R3-M4] Major — 处方 (a) 的 `<file>` 数据源 `dispatchable_workflows[]` 装的是**相对路径** (`.forgejo/workflows/x.yml`), 直接拼进 dispatches URL ⇒ 404; 且 `dispatch_viable` 的消费应落在代码而非 prompt 渲染

- **锚点**: §3.3 (a) 行 `…/actions/workflows/<file>/dispatches` 「对 `path_coverage.dispatchable_workflows` 逐文件列出」; §4 `dispatchable_workflows` = matched 中 dispatchable 者; `path_coverage.py:391-407` `_find_workflow_files` 返回 `f"{d}/{name}"` (`d` ∈ `.forgejo/workflows` 等), `:489` `matched.append(rel)` ⇒ `matched_workflows` 元素形如 `.forgejo/workflows/issue-triage-tests.yml`; F6 / §3.5 TASK-0a 用的是 `issue-triage-tests.yml` (「按文件名寻址」)。
- **问题**: 两实施者分叉 — 逐字把列表元素填进 `<file>` 的那位产出的命令对每个用户都 404 (路径里的 `/` 会改路由); 另一位取 `os.path.basename`。「可复制的处方命令」是 v3 收缩后**唯一的交付物**, SC 对 (a) 行内容零断言 (NEG-4 两条 `_target_behavior` 都不含它), 所以错的那版全绿。
- **连带 (与 A1-R3-M6 合修, 本席给运行时落点)**: `[仅当 traps §6 dispatch_viable=true …]` 若留在 prompt 文案里由 AI 读文档判断, 就是「读 references 决定运行时文案」; 钉法: `pre_merge_gate.py` 在 `DEFAULT_CONFIG` 旁加模块常量 `DISPATCH_VIABLE: bool = <TASK-0a 结果>` (注释引 traps §6 证据), `_no_run_gate_error` 按 `DISPATCH_VIABLE and dispatchable_workflows` 把已渲染的 (a) 命令 (每个元素 `os.path.basename`) 写进 `gate_error.message` 末尾 (或新 additive 键 `gate_error.remedy_commands[]`, 机读更稳); §3.3 的 (a) 行改为「引用 message 中已渲染的命令」。SC-2 `workflow-trigger-matched` 变体加一条: 当 `DISPATCH_VIABLE` 为 True 时 message 含 `workflows/issue-triage-tests.yml/dispatches` 且**不含** `.forgejo/workflows/issue-triage-tests.yml/dispatches` (坏实现必红); `empty-diff`/`unknown` 档不含 `dispatches`。这样 `dispatch_viable=false` 时 §4 字段仍有消费方 (message 渲染分支), 回答 A1-R3-M6 第二点。

### [A4-R3-M5] Major — §5 版本引用点行**误引 Aria#177**: #177 第 2 错逐字点名 `CLAUDE.md:139` + `:141`, v3 却只排除 `CLAUDE.md:5`; i18n 9 点未枚举。上一次 PATCH ship 实触 14 点

- **锚点**: §5 最后第二行「引用点口径 (Aria#177): … 主仓侧 gitlink / `VERSION` / `README.md:8` badge / `README.md:242` / i18n (仅正文实质变更才重译); `CLAUDE.md:5` 是主项目版本 (2.0.0), 本 PATCH **不动**」; R2 簇 #12 处置表 (A5-R2-M2) 原话亦是「漏 `CLAUDE.md:5` 版本行 — 注: 那是主项目版本」。
- **实读 #177** (`forgejo GET /repos/10CG/Aria/issues/177`, 本轮): 「主仓实测 **14 个引用点**: `README.md` 2 · `README.{zh,ja,ko}.md` 各 3 (translated-from + badge + `Plugin Version:` 行) · **`CLAUDE.md` 2** · `VERSION` 1」; 第 2 错逐字: 「**漏 `CLAUDE.md` 自己** — `CLAUDE.md:139` (版本区间 `v1.52.0–v1.65.5 已 ship`) + `:141` (「版本:」行) 各含版本号。自指盲区」。
- **实核现网**: `CLAUDE.md:139` = `aria-plugin 方法论轨: v1.52.0–v1.66.3 已 ship`, `:141` = `版本: 插件 aria-plugin v1.66.3 | …`; `CLAUDE.md:5` = `> **版本**: 2.0.0` (#177 从未点名它)。`git show --stat 451aba0` (v1.66.3 ship): `CLAUDE.md | 4 ++--`, `README.{ja,ko,zh}.md | 6 +++---` 各, `README.md | 4`, `VERSION | 2` — 正好 2+9+2+1 = 14 点, i18n 三文件各 3 点**每次 PATCH 都动** (`translated-from` 标记不动则 `i18n-readme-translation-currency` 实读 `:148-175` 会报 STALE), 「仅正文实质变更才重译」指的是正文, 不是这 9 个版本点。
- **为什么是 Major**: 这正是 #177 开号要治的「类」(三次复发全是「引用点清单漏同一批」), 而 v3 在**引用 #177 的那一句里**重犯了 #177 第 2 错 (memory `cite≠apply` / `critique-repeats-error`); 照 v3 ship 会留 `CLAUDE.md` 两处 `v1.66.3` 陈旧, 且无 custom check 兜 (#177 第 2 错末句)。
- **钉法**: 该行改为「主仓侧 **14 点** (#177 口径): `README.md:8/:242` · `README.{zh,ja,ko}.md` 各 `:3` translated-from + `:10` badge + `:244` Plugin Version 行 (版本点必动; 正文不重译, #140 B 档) · `CLAUDE.md:139` 区间上界 + `:141` 版本行 · `VERSION` 子模块表行; gitlink 另计」; 删「`CLAUDE.md:5`」那句 (它不在口径内, 留着会误导成「CLAUDE.md 不动」)。SC-14 加 `grep -c 1.66.3 CLAUDE.md README*.md VERSION == 0` 的发版后断言 (非账本文件)。

### [A4-R3-m1] Minor — 新名 `_verify_branch_exists` 的桩**放哪**未钉 (mixin vs 逐测试), 正是 traps #7 的形状

- §2.1 只说「测试对新名另打一桩」。若只在 SC-5/SC-10 逐测试打, 日后任何在 `_ProbeCacheResetMixin` 子类里写 `pr_state="not_found"` 的测试会走真 `ls-remote origin feature/x` (8.7s + 结果随远端) — traps §三 #7 / mixin docstring `:66-72` 明令「统一在 mixin 一处」。钉法: mixin `setUp` 加第二个 patcher `self.pr_verify = patch.object(gate, "_verify_branch_exists", return_value=("ok",""))`; SC-10 用 `self.pr_verify` 改返回值 / `assert_not_called`。

### [A4-R3-m2] Minor — prompt 模板 `<elapsed>` 无机读来源

- §3.3 「已连续 `<obs>` 次观测到零 run (~`<elapsed>`s)」: `<obs>` 来自 CLI stdout, `<elapsed>` 不在 stdout JSON (`{"retry_count","no_run_observations","should_prompt"}`) 里; AI 要么读 state 文件算 `now - started_at`, 要么按 intervals 累加, 要么省略。钉法: CLI stdout 加 `elapsed_seconds` (= now − `started_at`, 整数), 模板引用它; 零成本, 且与 A1-R3-M5 的「别在别处复述秒数」一致。

### [A4-R3-m3] Minor — 代码注释 / CLI help / Impact 新 artifact 四处同步面漏列 (R2-M8 同形, 仅注释级)

- `pre_merge_gate.py:278-288` 段首注释「main-branch existence verification (#137)」与 `:305-319` docstring 「核验 `main_branch` …」随函数体搬迁到 `_verify_branch_exists` 后主语须泛化; `:404-408` gate_check docstring 「subprocess 调用数 0 或 1」在 `not_found` 路径多一次 ls-remote 后不再准确; `:548-552` `--remote` help 「Remote to verify --main-branch exists on」须加 PR。Impact「Schema (additive)」未列三个新 artifact: `.aria/gate-state-telemetry.jsonl` / 主仓 `.aria/probes/<gate-state-helper-invocation>` / state-checks 条目 (`.gitignore` 见 A1-R3-m5)。

### [A4-R3-m4] Minor — NEG-4 登记缩掉了 R2 钉法里的三件: catalog `version` / `changelog` / fixture 元键集

- 实读 `phase-c-integrator-pre-merge-gate.json`: `version: 1.1.0`, `changelog` 只有 1.0.0 一条 (NEG-3 加入时就漏写); NEG-3 元键 8 个 (`_fixture_id / _description / _target_behavior / _why_the_distinction_matters / _discriminating_question / _arm_expectations / _consumed_by / _ships_with`), SC-15 只点 3 个。钉法: SC-15 加「`version` → 1.2.0, `changelog` 补 NEG-3 (追认) + NEG-4 两行; NEG-4 键集 = NEG-3 全集, `_ships_with: v1.66.4`」。

## 未发现问题但已核验的点

- `aether.py:225-226` `if not runs: return "pending"` ✓; `:218` docstring ✓; `base.py:29` Literal 含 `not_found` ✓。§1 翻转后**没有**既有 gate_check 测试会落到 `not_found` (全部 `query_pr_ci` 在 backend 层 mock 成显式 `CIStatus(state=…)`; `test_ci_backends.py:158-167` 只测非空 runs) ⇒ 新名未打桩不会让既有测试走网络。
- `MainBranchExistenceTests._stub_backend` 的 `query_pr_ci` 是未配置 MagicMock ⇒ `pr_status.state == "not_found"` 恒 False ⇒ 第八早退不干扰该组 5 条承重测试 (含 `assertNotIn("gate_error", out)`)。
- `:498-506` not_applicable 短路在 `:509` `query_pr_ci` 之前 ⇒ 2.3 表「`not_applicable` 结构上不可达」✓。
- `path_coverage.py` `_result` 9 调用点 / 规则 6 `:492-495` 传 matched / `:36`「共 9 个」✓ (8 个字面); `NON_AUTO_TRIGGER_KEYS` 含 `workflow_dispatch`。
- phase-c SKILL `:46-54/:172-183/:175/:180/:241/:248/:252/:255/:276/:284/:288/:290/:292-302` 与 workflow-runner SKILL `:247-263/:313/:326/:332-336/:338-358/:345/:389`、schema `:38-52/:110-131/:125` 行号全部实核准确。
- `pre_merge_gate.py:566` 输出经 `json.dumps(..., ensure_ascii=False)` ⇒ A1-R3-M4 消毒点成立 (已并入 M1 修法)。
- `DEC-20260731-001:11` 原文引 `if not runs: return "pending"` — 前向指针方案 (原文不回改) 正确处理了它。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical / 5 Major / 4 Minor) — **vote: REVISE**

归我席 9 簇全部真落地, 设计收缩后我 R2 的接缝型问题已无残留; 本轮 5 条 Major 没有一条要求重开设计, 全是「伪码少一行哨兵 / CLI 少一个映射或子命令 / 一个 basename / 一行版本点清单」级别, 但 M2 (retry 冻结 + resume 失效, 静默) 与 M4 (交付物命令 404) 是照字面实现会以缺陷形态落地的量级, 不满足「仅剩 minor」的 PASS 门槛。与 A1 同建议: **v4 定点修 (含 A2-R3-M1/M2/M3 与 A1-R3-M3/M4/M5/M6), 然后单席或 owner 直批, 不再开五席 R4**。
