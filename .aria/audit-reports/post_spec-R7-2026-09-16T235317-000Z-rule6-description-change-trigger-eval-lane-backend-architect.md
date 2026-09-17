---
checkpoint: post_spec
mode: convergence
rounds: 7
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: PASS
timestamp: 2026-09-17T00:38:59.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [backend-architect]
---

# post_spec Round 7 — backend-architect

被审对象: proposal.md v8 (HEAD `15ab323`, R7 为 max_rounds=7 的最后一轮)。任务: 对账本席 R6 major (Impact + D5.6 的重试/告警描述与代码矛盾); 核 `claude-shim.sh` 垫片机制 (query 解析 / PID 与 kill 语义 / stdout EOF 时机 / 孤儿进程与帧丢失风险); 排查 v8 有无新引入的运行时机制描述失实。

## R6 对账

**closed 1 / partially 0 / open 0。**

R6 major (`architecture/proposal.md §Impact+§D5.6`: 「放弃后的失败类型记为 `container_crash` 且默认自动重试、反复告警, 直到 owner 手动阻止该 issue 自动派发」与代码矛盾) —— **closed**。

v7 原句 (Impact): 「代价: runner 开跑后碰到这类任务, 会被打进 S_FAIL (失败类型记为 `container_crash`) 并**默认自动重试、反复告警**, 直到 owner 手动阻止该 issue 自动派发」——已删除。

v8 新句 (Impact): 「代价 (按现行代码): 放弃后该派发进 S_FAIL, 失败类型记为 `container_crash`, 这是终态 —— **不自动重试, 默认也不告警**, Claude 在最终消息里写的原因编排器不读 ⇒ 这类任务会停在那里无人察觉。」逐句核对如下 (证据见「机制核实记录」, 本轮对每一条都重新独立读代码, 不只是复用 R6 结论):

1. 「放弃后该派发进 S_FAIL, 这是终态」——`extension.py` `TRANSITION_TABLE`(本轮重读 L274-289) 明确 `"S_FAIL": []`, 注释原文「universal sink」; 准确。
2. 「不自动重试」——`reconciler.py` `_RETRYABLE_FAIL_REASONS = frozenset({"infrastructure", "timeout"})`(本轮重新 grep+读, L1138-1141, 与 R6 时一致, 未被本 cycle 触碰) 不含 `container_crash`; 即便 LLM 判 retry, `retry_gates_ok` 因 `fail_reason not in _RETRYABLE_FAIL_REASONS` 为假, 降级为 `notify_owner`; 准确。
3. 「默认也不告警」——`reconcile_runner.py` `_build_failure_analysis_caller`(本轮重读 L100-135) 首行判断 `os.environ.get("ARIA_FAILURE_ANALYSIS_ENABLED","").lower() not in ("1","true","yes")` 为真即 `return None`(整段 LLM 扫描被跳过); 函数 docstring 原话「Disabled-by-default rationale: M5 ship is owner-gated for cost discipline」。全仓 `grep -rn ARIA_FAILURE_ANALYSIS_ENABLED` 只命中代码定义与两份文档 (`architecture-decisions.md`「默认 disabled 等 owner 显式 opt-in」、`m5-handoff.yaml`「owner choice; default off」), 没有任何 Nomad job HCL/部署配置设置它。`mark_failed` 写 `S_FAIL` 本身不发 Feishu (飞书发送点只在 `_handle_s7_human_gate` 与本函数的 `notify_owner` 分支); 准确。
4. 「Claude 在最终消息里写的原因编排器不读」——`extension.py` `_handle_s5_await` 的 `container_crash` 分支(本轮重读 L2617-2636)只写 `fail_detail = f"S5_AWAIT: alloc terminated with exit_code={exit_code} alloc_id={alloc_id} (container_crash)"`——只有退出码与 alloc id, 不含 Claude 的最终消息文本; 全仓 grep `extension.py`/`reconciler.py`/`reconcile_runner.py`/`alloc_status_provider.py` 未见任何解析 runner `result.json` 的 `outcome` 字段或 stdout 最终消息的代码路径 (唯一读 alloc 日志的地方是 redo 模式成功路径提取 `new_pr_id`, 用于绑定 PR 号, 与判定退出码/失败原因无关); 准确。

D5.6 第 6 项新增的 8 条已知缺口 (逐条按 aria-orchestrator 代码核实) 本轮逐条重新验证, 全部准确 (含 (1)(2)(8) 与本 major 直接相关的三条, 及 (3)(4)(5) 与「新引入问题」相关的三条, 见下), 未发现失实。判 **closed**。

## Findings

无 (0 critical / 0 major / 0 阻塞 minor)。

## 观察

- **D5.6(3) 的双模式区分本轮逐字核对属实且有必要**: `initial.sh` Step 10 (L415-419) 对任何残留改动 `git add -A && git commit`, 但 SUCCESS 仍受 L524-534 五条件把关 (含 `issue.yaml` 的 `expected_file_touched`/`expected_diff_contains` 断言); 而 `changes.sh`(L269-306) 与 `redo.sh`(L294-298, L388-399) 只要 `git add -A` 后有 diff 且 push 成功即直接判 `PASS`, **完全没有断言检查**——这意味着「只停手不撤销」这条风险在 changes/redo 两模式下比 initial 模式更容易被放过 (没有 `FILE_TOUCHED_HIT`/`DIFF_CONTAINS_HIT` 这道额外闸)。v8 的措辞「changes / redo 模式有 diff 且推送成功即 PASS」准确且没有夸大, 但没有点出「比 initial 模式的闸更松」这一层, 建议 D5.6 跟进 spec 起草时留意 changes/redo 是风险更高的子情形, 不要求本轮改字。
- **`unattended` 键在 aria-orchestrator 侧零代码引用**: 全仓 `grep -rn unattended` 除一处不相关的法务备忘录 (`docs/r1-legal-memo.md`) 外零命中——不仅是「契约未定义」, 而是编排器代码里根本不存在这个概念; 默认回落 `false` 的证据在 aria-plugin 一侧 (`aria/skills/state-scanner/tests/test_coordination_default_lockin.py` + `config-loader/DEFAULTS.json`)。v8「缺失时静默回落 false...修好之前禁令在 runner 里不会触发」的表述与此完全吻合, 且比 R6 时的核实更彻底 (本轮补做了全仓 grep, R6 未做)。
- **垫片 (`claude-shim.sh`) 机制评估** (按任务第 2 部分逐项):
  - **query 解析可靠性**: 循环按「上一个 token 是否恰为字面 `-p`」捕获紧随其后的参数, 与 `run_eval.py` 实际构造 (`cmd = ["claude", "-p", query, "--output-format", "stream-json", ...]`, 已读源码确认) 完全吻合——`-p` 与 query 永远相邻且只出现一次, 不受其后追加的 `--model`/`--output-format` 等参数干扰。未发现可达的解析失败场景。
  - **PID / kill 行为一致性**: 垫片用两次「仅重定向不带命令」的 `exec`(改 stdout/stderr 目标) 加一次「带命令」的 `exec "$REAL_CLAUDE" ...`(替换进程镜像) ——全程只有一次 execve, PID 不变。`run_eval.py` 的 `process.kill()`(`run_single_query` 的 `finally` 块, 每条 return 路径都会走到) 杀的是 `Popen` 记录的那个 PID, 经垫片后这个 PID 已是真 claude 本体, 与不经垫片时的 kill 目标完全一致。
  - **stdout EOF 时机**: 经垫片时, `run_eval.py` 的 `process.stdout` 实际连的是「进程替换」子壳 (跑 `tee -p -a "$f"; printf ...`) 的输出, 不是真 claude 直连; EOF 要等 真claude 退出 → 内部管道 EOF → tee 读完退出 → 子壳跑完 `printf` 收尾行 → 子壳自身退出, 比不经垫片时多了几个纳秒级步骤, 数量级上不影响 `run_single_query` 的判定或超时逻辑 (决定性事件在到达时即返回, 不依赖等到 EOF; 唯一依赖阻塞式 `.read()` 排空的分支是 `process.poll() is not None` 那条, 即真 claude 自行退出的路径)。
  - **孤儿进程 / tee 挂住风险 (理论排查, 未发现新增风险)**: 若真 claude 在 `-p` 模式下派生的工具子进程 (如 Bash 工具调用) 继承了 fd 1 且在真 claude 被 `SIGKILL` 后继续存活, 理论上会让管道写端迟迟不关闭、tee 迟迟收不到 EOF。但这个风险 (a) 不是垫片引入的——不经垫片时, 同样的继承关系会让 `process.stdout` 直接卡住, 性质相同; (b) 即便发生, `run_eval.py` 对每条 return 路径只 `wait()` 自己直接认领的那个 PID (已被 SIGKILL, 几乎瞬间可回收), 不会等孤儿进程, 不会拖慢后续 query; (c) 本轮实测的 v6a/v6b 全部真实调用 (C1/C2 两批, 逐调用检查报告零「无判定事件」异常) 未观察到此现象。结论: 值得记录但不构成阻塞发现。
  - **v6b「日志缺结束记录」个案的可达性判断**: 已读 `run_arms_v6b.sh` 全文, 确认脚本本身 (T2b 将原样搬入的四个工具不含这份驱动脚本, 但它是四工具的唯一现存调用范例) 没有任何包一层的外部 `timeout`, `run()` 函数对每个臂新建空日志目录 (`rm -rf ...; mkdir -p ...`) 后直接同步调用 `python3 -m scripts.run_eval`。RESULT.md 原文「两次调用各耗满 120 秒, 被外层超时截断」的「外层超时」不在这份脚本或 `run_eval.py`/垫片任何一层内, 只能来自调用者 (上一轮做实验的 agent) 自己的命令级超时设置过短、没有覆盖两个并行 120 秒调用叠加的耗时。**在文档化的场景 4b 工作流里不可达**(该工作流没有更外层的固定超时), 只在「手工探针 + 过短的外层超时」这种偏离标准调用方式的场景下才会出现; 即便出现, `classify_calls.py` 的「缺垫片起止记录」判据(已读源码确认, 本轮重跑验证)会把这类日志判「不健康」, 不会被误判为健康, 是 fail-safe 而非 fail-open。
- **独立复现** (本轮新做, 未见于此前任何一轮的机制核实记录): 把 `claude-shim.sh`/`classify_calls.py`/`fake-claude`/`fault_matrix.py` 复制到 scratchpad 后直接重跑, 24 个用例全部符合、退出码 0, 与 RESULT.md 及 SC-13 的断言一致; 再把 `classify_calls.py` 里对 `result` 帧报错的判定注释掉重跑, 5 个用例 (`F1_result_error`/`S1_overbroad_fault_in_shouldnot_half`/`S2_correct_fault_on_one_should_query`/`S8_two_run_fault_should`/`S10_negctrl_two_run_fault_x6`) 转为不符、退出码 1, 与 SC-13 反事实断言逐字吻合。这不是复述 RESULT.md 的文字, 而是本席独立执行代码后得到的第一手结果。
- **T2b 范围小观察 (非阻塞)**: T2b 只搬 4 个工具文件, 不含 `run_arms_v6b.sh` 这类「驱动脚本」; 未来对新 skill 跑场景 4b 时, D2/D3 的参数表 (`--num-workers 1`/`--runs-per-query 3`/显式 `--model` 等) 已足够作为人工核对清单, 但没有可直接复用的调用脚本, 需要执行者照 D3 前置表手写。这是范围界定的取舍 (四个工具是跨 skill 通用的不变量, 驱动脚本每次的套件路径/description 文本都不同), 不是遗漏, 不要求本轮补。
- **Impact 影响面数字** (「456 个非合并提交...改了已有 skill description 的 7 个...约 1.5%; 另有 15 个提交新增 skill」) 替换了 v7 「577 次里 6 次约 1%」的错误口径——本轮独立执行 `git log --oneline --no-merges master | wc -l` 得 456, 与当前 `aria` 子模块 HEAD (`1cb3872`) 一致, 分母核实无误; 分子 (7 处 description 改动 / 15 次新增 skill) 沿用 R6 聚合报告「主控复核」逐提交 frontmatter 比对的结果, 本轮未逐提交重新展开复核 (性价比考虑: 该数字不在本席 R6 major 范围内, 且已经过 R6 聚合的主控核验), 仅做了分母级抽查。

## Verdict

PASS — 0 critical / 0 major / 0 minor。

## Vote

PASS

## 机制核实记录

- 完整重读 `aria-orchestrator/docker/aria-runner/modes/initial.sh` L280-596 (本轮): Step 6 `CLAUDE_ARGS` 构造、Step 8 NO_OP 判定 (L350-377)、Step 10 「若 claude 没 commit 但 working tree 有 changes, runner 补 stage+commit」注释原文与其下 `git add -A`/`git commit`(L415-419)、Step 10 push 分类与 PR 创建 (L420-503)、SUCCESS 五条件 (L524-536)、退出码 (L591-596)。
- 完整读 `aria-orchestrator/docker/aria-runner/modes/changes.sh` 全文 (308 行, 本轮首次为本 Spec 系统读): T4.3 `git add -A` 后 `git diff --cached --quiet` 空则 `fail_with "no_changes"`(L269-272); 否则 commit + `commit_lint_retry_loop` + force-with-lease push, 成功则 `outcome:"PASS"`, 失败则 `fail_with "force_push_stale_ref"`(L292-306); 全脚本没有对 diff 内容的断言检查。
- 完整读 `aria-orchestrator/docker/aria-runner/modes/redo.sh` 全文 (403 行, 本轮首次为本 Spec 系统读): 同 changes.sh 模式, `git add -A` 后空 diff → `fail_with "no_changes"`(L294-298); 新分支 push 成功 + PR 创建成功 → `outcome:"PASS"`(L388-399); 同样没有断言检查。
- 完整读 `aria-orchestrator/docker/aria-runner/prompts/issue-dispatch.md` 全文 (39 行): 第 5 条 Execution constraint 原文「If the task cannot be completed, do NOT make a commit with partial work; exit with a clear reason in your final message so the runner can classify as `CLAUDE_REFUSAL` or `CLAUDE_NO_OP`」, 确认与 runner 自身补提交行为存在张力 (提示词假设「不 commit = 安全」, 但 Step 10/changes.sh/redo.sh 都会把工作区里的残留 diff 捡起来)。
- 重读 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/reconciler.py` L1120-1373 (`_RETRYABLE_FAIL_REASONS`/`_OWNER_INITIATED_FAIL_REASONS`/`_handle_failure_analysis_for_row` 全函数体, 本轮逐行重读非复用 R6 笔记): 确认 `fail_detail` 被喂进 `render_prompt(...)` 生成 LLM 输入, `verdict.action=="retry"` 但 `fail_reason not in _RETRYABLE_FAIL_REASONS` 时降级 `effective_action="notify_owner"`, 走 `build_reject_alert_card(..., reject_reason=f"[M5 failure_analysis] {verdict.reason} (suggested: {verdict.suggested_owner_action})", ...)`; 卡片文案由 LLM 生成, LLM 的输入 (`fail_detail`) 对 `container_crash` 只有退出码与 alloc id。
- 重读 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/extension.py` `_handle_s5_await` container_crash 分支 (L2617-2636, 本轮重读): `fail_reason=FailReason.CONTAINER_CRASH`, `fail_detail=f"S5_AWAIT: alloc terminated with exit_code={exit_code} alloc_id={alloc_id} (container_crash)"`。
- 重读 `TRANSITION_TABLE`(`extension.py` L274-289): `"S_FAIL": []`, 注释「universal sink」。
- 全仓 grep `result\.json|CLAUDE_NO_OP|outcome.*==.*SUCCESS` 于 `extension.py`/`reconciler.py`/`reconcile_runner.py`/`alloc_status_provider.py`: 除文档注释与 redo 模式读 alloc stderr 提取 `new_pr_id`(与判定无关) 外, 无任何代码路径解析 runner 自报的结果枚举或 Claude 最终消息。
- 重读 `reconcile_runner.py` `_build_failure_analysis_caller` L100-135: `ARIA_FAILURE_ANALYSIS_ENABLED` 未设为 `1/true/yes` 时直接 `return None`; docstring 明写「Disabled-by-default...cost discipline」; 额外还要求 `extension._silknode` DI 存在, 否则同样回退 `None`。
- 全仓 grep `ARIA_FAILURE_ANALYSIS_ENABLED`: 仅命中代码定义处与两份文档 (`architecture-decisions.md` L3687/3723, `m5-handoff.yaml` L62), 无任何 `.hcl`/`.nomad`/`.yaml` 部署配置设置该变量。
- 全仓 (`aria-orchestrator/`) grep `unattended`: 仅命中一处不相关文档 (`docs/r1-legal-memo.md`), 代码零命中; 交叉确认 `aria/skills/state-scanner/tests/test_coordination_default_lockin.py` 与 `aria/skills/config-loader/DEFAULTS.json` 存在 (aria-plugin 一侧维护默认回落 `false` 的锁定测试)。
- 读 `aria-orchestrator/docker/aria-runner/Dockerfile`(grep `COPY`/`skill-creator`): 只 `COPY aria/ /opt/aria-plugin/` 与 runner 自身脚本, 未见任何 skill-creator 安装步骤; 确认 D5.6(5)。
- 完整读基线目录 `v6-per-call-health-opus5/claude-shim.sh`(21 行全文) 与 skill-creator `run_eval.py`(`~/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator/scripts/run_eval.py`) 的 `run_single_query`/`run_eval` 两个函数全文: 确认 `cmd = ["claude","-p",query,...]` 构造、`finally: process.kill(); process.wait()` 每条 return 路径必经、`except Exception` 才打印 `Warning: query failed`。
- 完整读基线目录 `v6-per-call-health-opus5/classify_calls.py`(全文 155 行): `classify_file()` 的「缺垫片起止记录」「无判定事件」「耗时达到超时阈值」「result 帧报错」四类不健康判据, `judge()` 的 evaluated (`pass_worst`/`pass_best`)/negctrl (`hits_min`/`hits_max`) 双端判定与 `unmapped`/`mismatch` 触发 void 的逻辑。
- 读 `v6-per-call-health-opus5/run_arms_v6b.sh` 全文: 确认无外层 `timeout` 包裹 `run_eval`, 每臂 `rm -rf` 后新建日志目录。
- **独立重跑** (本轮新做): 复制四工具文件到 scratchpad, `python3 fault_matrix.py --suite <基线套件路径> --out <scratch>/fm` → 24 用例、0 不符、退出码 0; 修改 scratch 副本 `classify_calls.py` 注释掉 `result` 帧报错判定后重跑 → 24 用例、5 不符 (`F1_result_error`/`S1_overbroad_fault_in_shouldnot_half`/`S2_correct_fault_on_one_should_query`/`S8_two_run_fault_should`/`S10_negctrl_two_run_fault_x6`)、退出码 1 —— 与 RESULT.md「v6b」段与 SC-13 反事实描述逐字吻合, 独立验证而非转述。
- 独立执行 `git log --oneline --no-merges master | wc -l`(aria 子模块) = 456, `git rev-parse HEAD` = `1cb387218935433312fde4067c276754b77686a8`, 与 Impact 段引用的提交数/SHA 一致。
- 全文比对 `git diff c3a5903 15ab323 -- openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md`(178 行完整 diff, 非局部片段), 逐个 hunk 核对本轮涉及的运行时机制描述改动。
