# workflow-runner §wait_recoverable — 第 3 次重查后的下一步

> 输入: `inputs/gate-output.json` (C.2.4 本轮 out) + `inputs/record-stdout.json` (步骤 3c' `gate_state_helper.py record` stdout)。
> 依据: `aria/skills/workflow-runner/SKILL.md` §`wait_recoverable` Exit conditions (first-match-wins, 五条) + 实施步骤 3d;处方段引用 `aria/skills/phase-c-integrator/SKILL.md` §C.2.4 步骤 6 (唯一定义处)。
> 本回答零写操作: 未 reset / 未 clear / 未 dispatch / 未 merge。所有动作都排在用户答复之后。

---

## (1) 命中的 exit condition 判定与理由

### 输入字段

| 来源 | 字段 | 值 |
|------|------|----|
| out | `verdict` | `wait` |
| out | `pr_ci_status` | `not_found` (远端零 run) |
| out | `in_flight_runs` | `[]` (master 无 in-flight, (b) 轴干净) |
| out | `gate_error.kind` | `no-run-for-branch` |
| out | `gate_error.prompt_after_observations` | `3` |
| out | `path_coverage.decision / reason` | `covered` / `workflow-trigger-matched`, matched = `.forgejo/workflows/issue-triage-tests.yml`, `dispatchable_workflows` 非空 |
| record | `retry_count` | `2` (第 3 次 wait: 0 → 1 → 2) |
| record | `no_run_observations` | `3` (连续三轮同 kind, 含初次) |
| record | `should_prompt` | `true` (3 ≥ threshold 3) |
| record | `elapsed_seconds` | `92` (≈ intervals 30 + 60) |
| config (实读 `.aria/config.json`) | `wait_timeout_seconds` | `1800`; `wait_check_intervals` 未覆盖 → 默认 `[30,60,120,300,300]` |

### 逐条 first-match

1. **user Ctrl-C** — 未命中。走到步骤 3c'/3d 说明本轮 sleep chunk 循环里 `.aria/.workflow-interrupt` flag 不存在 (存在则已在 3b break 转 suspended, 根本不会调 gate 与 record)。
2. **retry_count > max OR elapsed > wait_timeout_seconds** — 未命中。`elapsed 92 < 1800`;SKILL 在本条括号里明示「exit 2 实际只由 elapsed 触发」, retry_count=2 不构成触发。
3. **2.5 `out.gate_error.kind == "no-run-for-branch"` AND `record.should_prompt`** — **命中**。两个合取项逐字匹配: kind 字面相等, `should_prompt` 为 `true` (helper 按 `no_run_observations >= --threshold` 求值, 3 ≥ 3)。与 SKILL 时间轴注「默认阈值 3 + intervals [30,60,120,…] ⇒ 首次 gate 后 ~90s 交人」一致 (实测 92s)。
4. 条件 3 (`verdict=fail`) / 4 (`verdict=green`) 不再求值 (first-match-wins)。

### 为什么是「交人」而不是别的

- 不是 fatal: `verdict=wait`, SKILL 明言「等待外部 CI 完成是协作正常态, 不当 fatal error」;no-run 态只在用户答 `abort` 时才取 fail 语义。
- 不自动 dispatch / 不推 commit: 处方段写死「由你执行; AI 不自动执行」。
- 不因「前两次同样结果」自行跳过或继续静默等: gate 是 config `enabled: true` 的闸门, Rule #10 不得以「结果重复 / 变更小」自我豁免; 而 2.5 的设计意图正是在第 3 次同形观测时把决定权交出去, 而非第 30 次。
- 不 reset / 不 clear: `reset --observations` 只在用户答 `continue` 后执行; `clear` 只在 green 合并后。

### 处方各项在场判定 (决定 (2) 里哪几行出现)

- **(a)**: `gate_error.message` 第二行含 `处方 (a): forgejo POST /repos/<owner>/<repo>/actions/workflows/issue-triage-tests.yml/dispatches ...` → (a) 出现。AI 只填 `<owner>/<repo>`: 合并对象是 aria-plugin 子模块分支, 子模块 `origin` = `ssh://forgejo@forgejo.10cg.pub/10CG/aria-plugin.git` → `10CG/aria-plugin`。
- **(b)**: `path_coverage.reason == workflow-trigger-matched` → (b) 出现, 并按处方写 matched workflow 声明的 paths。实读 `aria/.forgejo/workflows/issue-triage-tests.yml` (当前工作树): `on.push.paths` / `on.pull_request.paths` 均为 `skills/issue-triage/**`, **无 `branches` 过滤**, 另含 `workflow_dispatch: {}` (与 (a) 可 dispatch 一致)。因此「推 commit 无效」的例外不成立 (此为人核结论, path_coverage 不建模 branches)。
- **(c)**: 恒出现。

---

## (2) 对用户输出的内容 (原文)

```
🔴 C.2.4: `no-run-for-branch: 变更 path-matched .forgejo/workflows/issue-triage-tests.yml 但远端零 run — 符合 aria-plugin#152 (新分支首推 × paths 过滤, Forgejo 不建 run), 或 run 尚未被 runner 领走, 或 workflow branches 过滤不含本分支
处方 (a): forgejo POST /repos/<owner>/<repo>/actions/workflows/issue-triage-tests.yml/dispatches -d '{"ref":"fix/147-issue-triage-regression"}'`。已连续 3 次观测到零 run (~92s)。处方 (择一, 由你执行; AI 不自动执行):

(a) dispatch 命令行 (gate 已渲染, 我只填了 <owner>/<repo> = 10CG/aria-plugin):
    forgejo POST /repos/10CG/aria-plugin/actions/workflows/issue-triage-tests.yml/dispatches -d '{"ref":"fix/147-issue-triage-regression"}'
    ⚠️ 活体实测一次 dispatch 产生成对 run 且 started_at 相同 (phase-c-integrator references/pre-merge-gate-empirical-traps.md §六), gate 取最近 run 时 tie 可能读到 failure — 请按 run id / 状态综合看, 不要只看 gate 的第一眼判定。

(b) 推一个碰 CI 触发路径的实质 commit 到 fix/147-issue-triage-regression (workflow-trigger-matched: issue-triage-tests.yml 声明的 paths = skills/issue-triage/**)。第二次 push 是普通 diff, paths 正常评。我读了该 workflow: 无 branches 过滤, 推 commit 有效 (path_coverage 不建模 branches, 此为人核)。

(c) 继续等待 (continue) / 放弃 (abort)。

状态: 第 3 次重查 (retry_count=2), 距首个 wait 92s, 整体上界 wait_timeout_seconds=1800s; master 无 in-flight run (in_flight_runs=[]), 仅 PR 分支零 run 这一腿卡住。
- 回答 continue: 我只把 no_run_observations 归零 (retry_count / started_at 继续累计), 回 loop 下一轮 120s 后重查; 若你已执行 (a) 或 (b), 也请回答 continue, 我会在重查时看到 run。再连续 3 次零 run 会在 ~810s 时再问你一次。
- 回答 abort: 按 verdict=fail 语义结束 workflow (session failed, 保留 gate_state 作 audit trail), 不 merge、不推送、不删分支/PR。
```

---

## (3) 用户答复后的具体动作

### 用户答 `continue`

1. 归零观测计数 (只 `--observations`, **不**带 `--retry-count` — 2.5 明确 retry_count / started_at 继续累计, exit 2 上界不变):

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/workflow-runner/scripts/gate_state_helper.py" reset \
     --state-file /home/dev/Aria/.aria/workflow-state.json \
     --observations
   ```

   期望 stdout `{"ok": true}`。退出码 2 (state 文件缺失 / 无活跃 gate_state) → surface 错误并直接 abort 分支, **禁止**回退手写 JSON (步骤 3d)。`--state-file` 必须是主仓根绝对路径 (helper 默认相对 cwd, 子模块 cwd 下会静默另起 state)。

2. 回 polling loop 步骤 3a: 本轮 sleep = `wait_check_intervals[min(retry_count, len-1)]` = `[30,60,120,300,300][2]` = **120s**, 按 `poll_chunk_seconds=5` 拆块, 每块末 `os.path.exists("/home/dev/Aria/.aria/.workflow-interrupt")`, flag 出现即 break → `session.status=suspended`, 保留 gate_state 与 flag。

3. sleep 结束 → 重调 phase-c-integrator C.2.4 gate (执行上下文 = 子模块根 `/home/dev/Aria/aria`, `main_branch=master` 显式传真值, `pr_branch=fix/147-issue-triage-regression`) → 得新 `out`。

4. 记录 (两旗标仅当新 out 的 kind 仍为 `no-run-for-branch` 时传; `in_flight_runs` / `raw_message` 必须透传):

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/workflow-runner/scripts/gate_state_helper.py" record \
     --state-file /home/dev/Aria/.aria/workflow-state.json \
     --name pre_merge \
     --verdict "<out.verdict>" \
     --intervals '[30,60,120,300,300]' \
     --in-flight-runs '<json(out.in_flight_runs)>' \
     --raw-message "<out.raw_message>" \
     --source production \
     [--gate-error-kind no-run-for-branch --threshold 3]   # 仅 out.gate_error.kind == "no-run-for-branch" 时
   ```

5. 再按五条 exit conditions 处理 (输入 = 新 out + 新 record):
   - 用户执行了 (a)/(b) 且 run 出现 → `pr_ci_status=pending` → `wait` 且无 no-run kind → helper 把 `no_run_observations` 归零, 继续轮询; `passing` 且 master 无 in-flight → `green` → 退出 loop, 调 branch-manager merge (子模块侧按 CLAUDE.md 约束 1: **本地 `git merge` + 双推, 禁 Forgejo 服务端 merge**; 推后逐 remote `ls-remote` 核验), 随后 `gate_state_helper.py clear --state-file /home/dev/Aria/.aria/workflow-state.json`。
   - 仍零 run → obs 重新 1 → 2 → 3, 第三次 (≈ 92 + 120 + 300 + 300 ≈ 810s) 再次命中 2.5, 再弹同款 prompt。
   - `elapsed > 1800` → 命中 exit 2 (与 2.5 同轮并存时 2 优先) → prompt; 那时 `continue` 改为 `reset --retry-count --observations` (两者归零, started_at=now)。
   - 新 out `verdict=fail` (如 `pr-branch-not-found`) → exit 3, stop。

### 用户答 `abort`

1. **不**调 `reset` / `clear` / `record`:
   - `clear` 会把 gate_state 置 null, 与「保留 gate_state 给 audit trail」相悖;
   - `record --verdict fail` 没有 kind 旗标, helper 会把 `no_run_observations` 归零 (源码: 非 no-run kind 一律置 0), 同样丢失 audit trail。
   - 因此 gate_state 原样保留: `status=waiting, retry_count=2, no_run_observations=3, started_at 不变, raw_message` 内含 message 原文与处方行。

2. 按步骤 4「verdict=fail → workflow-state.session.status=failed」更新 workflow-state (workflow-runner 自身 State Updates 机制, 非 gate_state 字段: 先写 `/home/dev/Aria/.aria/workflow-state.json.tmp` 再 rename, 重算 `integrity.state_hash` / `integrity.validated_at`):
   - `session.status = "failed"`, `session.last_active_at = now`
   - `execution.phase_results.C.status = "failed"`
   - `execution.phase_results.C.error = "C.2.4 pre-merge gate: no-run-for-branch, user abort after 3 consecutive zero-run observations (~92s); PR branch fix/147-issue-triage-regression"`
   - 保留 `phase_results.C.2.action.pr_number` (PR 已创建, 不重建)
   - state file **不删除** (执行失败保留供恢复 / audit, State Cleanup 表)

3. 不执行任何 git / Forgejo 写操作: 不 merge、不 push、不删 `fix/147-issue-triage-regression`、不关 PR、不 dispatch。

4. 输出 WORKFLOW EXECUTION REPORT: `Status: FAILED`; Phase C 段写 C.2.4 `verdict=fail (user abort)` + PR number + `raw_message` 原文 (含处方 (a) 行) + 本次 gate 统计 (3 次观测 / 92s / master 无 in-flight); 后续建议: 用户手工执行 (a) 或 (b) 让 run 出现后, 重新启动 workflow 走 Phase C (新 workflow 会原子覆盖旧 state; 旧 state 在覆盖前仍可查)。

5. 自作主张项写入 handoff 请复议 (Rule #10 精神): SKILL 说 abort 取「verdict=fail 语义」, 但 `gate_state.status` 是否应由 `waiting` 翻成 `fail` 未明说; 现有 CLI 没有「翻 status 且不清零 observations」的路径, 而 SKILL 禁止手写 gate_state JSON, 故我选择**保留 `waiting`** 以保全计数, 用 `session.status=failed` 承载终态。若 owner 认为 status 也须翻, 需给 helper 加 `record --verdict fail` 保留计数的语义, 属 Skill 变更 (Rule #6 照跑)。
