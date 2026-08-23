# workflow-runner §wait_recoverable — 第 3 次重查后的下一步 (old_skill 快照)

> 依据: 快照 `workflow-runner/SKILL.md` §`wait_recoverable` (exit conditions 1-4 + 实施步骤 1-4) · 快照 `phase-c-integrator/SKILL.md` §C.2.4 (verdict 计算 / 路由 / 配置默认) · `references/workflow-state-schema.md` §1.1 `gate_state`。
> 输入: `inputs/gate-output.json` (verdict=wait, `gate_error.kind=no-run-for-branch`, `prompt_after_observations=3`) · `inputs/record-stdout.json` (retry_count=2, no_run_observations=3, should_prompt=true, elapsed_seconds=92, next_check_at=2026-08-22T21:40:00Z)。

---

## (1) 命中的 exit condition 判定与理由

**判定: 进入 exit condition 2 的 user prompt 分支 (continue / abort), 现在就问, 不再睡 120s 做第 4 次重查。** 但必须如实说明: 这是 SKILL.md 四条 exit condition **字面上无一命中**之后的上报动作, 不是字面匹配。逐条核对如下:

| # | 条件 (SKILL.md 原文, first-match-wins) | 本轮取值 | 命中? |
|---|---|---|---|
| 1 | user Ctrl-C → suspended | `.aria/.workflow-interrupt` 不存在, 无中断 | 否 |
| 2 | `retry_count > max` OR `elapsed > wait_timeout_seconds` → user prompt | retry_count=2; elapsed=92s, `wait_timeout_seconds` 默认 1800; **`max` 在本版 SKILL.md / §C.2.4 配置表里根本没有定义** (只有 `wait_check_intervals=[30,60,120,300,300]`, 且明写「数组耗尽后重复 intervals[-1]」, 所以数组长度也不是 max) | 字面: 否 |
| 3 | verdict=fail → stop | verdict=wait | 否 |
| 4 | verdict=green → merge | verdict=wait | 否 |

字面执行的结果是: `sleep wait_check_intervals[min(2,4)] = 120s` → 21:40:00Z 第 4 次调 C.2.4 → 大概率同样结果 → 再睡 300s … 直到 elapsed > 1800s (约 22:06Z) 才触发条件 2 的 prompt。

我不走这条字面路径, 理由三点:

1. **gate 自己已经声明「等待不能自愈」**: `raw_message` 说明这是 aria-plugin#152 形态 (新分支首推 × `paths` 过滤, Forgejo 不建 run), `in_flight_runs=[]`, `pr_ci_status=not_found`。SKILL.md 把 `wait_recoverable` 定义为「等待外部 CI 完成是协作正常态」—— 前提是**有一个 CI 在跑**。这里没有任何 run 存在, 继续轮询 28 分钟只是把「恒 wait」翻译成零信息的空转 (恒红与假绿同样零信息)。
2. **gate 输出自带了上限并已达到**: `gate_error.prompt_after_observations=3`, helper record 回报 `no_run_observations=3` 且 `should_prompt=true`。这正是条件 2 「重试到上限 → 问人」的意图; 本版 SKILL.md 的 `max` 恰好是个没定义的空位, gate 给出的 3 次观察阈值是唯一可用的上限信号。我把它当作条件 2 的「重试上限」分支来处理, 但**明确标注这是覆盖外解读**, 写进 handoff 请 owner 复议 (Rule #10: AI 自作主张的流程判断必须留痕复议)。
3. **prompt 是上报, 不是自搭桥**: 可选动作里只有三种 —— (a) 继续空转; (b) 我自己执行 `forgejo POST .../dispatches` 把 run 造出来; (c) 问用户。(b) 是网络写操作, 本版 workflow-runner `allowed-tools: Task, Read, Write, Glob, Grep` 连 Bash 都没有, 且 gate 处方里的 dispatch 不是 SKILL.md 授权给 runner 的动作; 覆盖外分支应上报而非自搭桥。(c) 既不合并也不 dispatch, gate 仍然挡着 (Rule #8 未被豁免), 只是把决定权交给人。

**本版 skill 的盲区 (如实记录, 供对照)**:
- `gate_error.kind=no-run-for-branch` 与 verdict=wait 同在: §C.2.4 文档说 `gate_error` 「仅 main 分支存在性核验判 fail 时在场」, 枚举只有 `main-branch-not-found|main-branch-verify-failed`; `pr_ci_status=not_found` 文档说「gate 输出目前不产生」。gate 输出已经超出本版 schema。
- `should_prompt` / `no_run_observations` / `prompt_after_observations`: 本版 SKILL.md、schema §1.1 `gate_state`、`scripts/gate_state_helper.py` 都没有这些字段; 快照里的 `gate_state_helper.py` 是纯库 (无 argparse / `__main__`), 没有 `record` 子命令。题干说的「CLI record stdout」在本版不存在, 我把它当作 gate/helper 的扩展输出消费, 不依赖它做字段级断言。
- `max` 未定义 (上表)。

---

## (2) 对用户输出的内容 (原文)

```
╔══════════════════════════════════════════════════════════════╗
║  C.2.4 pre-merge gate 等待已到上限 — 需要你决定 (continue / abort)  ║
╚══════════════════════════════════════════════════════════════╝

对象:   aria-plugin 子模块分支 fix/147-issue-triage-regression → master (主仓 /home/dev/Aria)
gate:   verdict=wait (第 3 次重查, 前两次结果相同)
状态:   retry_count=2 | elapsed=92s / 1800s | no_run_observations=3/3 (should_prompt=true)
        in_flight_runs=[] | pr_ci_status=not_found | primitive=aether-ci-cli (f29abee)
路径覆盖: covered — 变更命中 .forgejo/workflows/issue-triage-tests.yml (1/1 changed file)

gate 原话 (raw_message):
  no-run-for-branch: 变更 path-matched .forgejo/workflows/issue-triage-tests.yml 但远端零 run —
  符合 aria-plugin#152 (新分支首推 × paths 过滤, Forgejo 不建 run), 或 run 尚未被 runner 领走,
  或 workflow branches 过滤不含本分支
  处方 (a): forgejo POST /repos/<owner>/<repo>/actions/workflows/issue-triage-tests.yml/dispatches \
            -d '{"ref":"fix/147-issue-triage-regression"}'

我的判断:
  这不是「CI 在跑、等它结束」的常态 wait —— 远端根本没有 run, 继续轮询不会自愈,
  只会空转到 1800s 超时。SKILL.md 四条 exit condition 字面上都没命中 (condition 2 的
  retry 上限 `max` 在本版未定义, elapsed 92s < 1800s), 我按 gate 自带的
  prompt_after_observations=3 已达来提前上报; 这一判断会写进 handoff 请你复议。
  我不会自己执行 dispatch (网络写操作, 不在 runner 授权内), 也不会绕过 gate 合并。

请选择:
  [continue]  你先手动触发 run (按上面处方 (a), owner/repo 填 10CG/aria-plugin),
              或确认 run 已被 runner 领走; 我 reset retry_count=0 后继续 polling
              (30s 后第 4 次 C.2.4 重查)。
  [abort]     停止本 workflow: 不合并、不动分支/PR、保留 workflow-state 供日后 resume,
              输出执行报告 (含 PR 信息 + gate 原话 + 处方)。
```

(以 AskUserQuestion 形式呈现, options = `continue` / `abort`, 叙述中文, 命令原文保留。)

---

## (3) 用户回答后的具体动作

约束共同项: 两条分支都**不**做 git 写操作、不调 forgejo、不 dispatch; runner 本身只有 Task / Read / Write / Glob / Grep。

### 用户答 `continue`

按 SKILL.md 实施步骤 4 「timeout → user prompt; continue → reset retry_count + 继续」:

1. **更新 `gate_state`** (Read `/home/dev/Aria/.aria/workflow-state.json` → 改字段 → 按 schema §4 原子写回: 先写 `.aria/workflow-state.json.tmp` 再 rename; 重算 `integrity.state_hash`):
   ```json
   "gate_state": {
     "name": "pre_merge",
     "status": "waiting",
     "started_at": "<保留原值, ≈2026-08-22T21:36:28Z>",
     "retry_count": 0,
     "next_check_at": "<now + 30s, 即 wait_check_intervals[0]>",
     "in_flight_runs": [],
     "primitive_used": "aether-ci-cli",
     "raw_message": "<gate-output.json 的 raw_message 原文>"
   }
   ```
   `started_at` 保留不重锚 (elapsed 仅 92s, 离 1800s 远; SKILL.md 只说 reset retry_count, 未说 started_at —— 若将来是 timeout 触发的 continue, started_at 不重锚会让条件 2 立刻再触发, 此歧义记 handoff)。
2. **polling sleep 30s**, 按 CR-5 拆 5s 块, 每块后检查 `/home/dev/Aria/.aria/.workflow-interrupt`; flag 出现 → 立即 break, `session.status=suspended`, 保留 gate_state。
3. **重新调 phase-c-integrator C.2.4** (经 Task 派给 phase-c-integrator; 它在子模块根执行, `main_branch` 显式传 `master`, 不吃 CLI 默认 `main`):
   ```bash
   cd /home/dev/Aria/aria && python3 "${ARIA_PLUGIN_ROOT:-/home/dev/Aria/aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" \
     --pr-branch fix/147-issue-triage-regression \
     --main-branch master \
     --remote origin \
     --config-file /home/dev/Aria/.aria/config.json
   ```
4. **按 exit conditions first-match 处理新 verdict**:
   - `green` → 清 `gate_state=null`, 调 branch-manager merge action 进 C.2.5。子模块分支 ⇒ 遵守 CLAUDE.md 硬约束 1: **本地 `git merge` + `git push origin && git push github`, 禁 Forgejo 服务端 merge**; 推后对每个 remote `git ls-remote <remote> master` 逐个核对 SHA (约束 2)。
   - `fail` → `session.status=failed`, 保留 gate_state 作 audit trail, 报告中带 PR 信息 + raw_message。
   - `wait` 且仍是 `no-run-for-branch` → 不再静默续转: retry_count 按常规 +1 写回, 但 gate 再次给出 `should_prompt=true` 时**立刻再次弹出同款 prompt** (第 (2) 节文案, 更新计数), 不等 1800s。
   - `wait` 且 `in_flight_runs != []` 或 `pr_ci_status=pending` (说明 run 已经建出来了) → 回到常规 wait_recoverable 指数退避 (60s → 120s → 300s …), 直到 green / fail / 1800s 超时 prompt。

### 用户答 `abort`

按 SKILL.md 「abort → stop」+ Phase 级 `on_phase_error: action: stop, report: true`:

1. **不**合并、**不**删分支、**不**关 PR、**不** dispatch —— 远端一切原样。
2. **写回 workflow-state** (同样原子写): `session.status = "failed"`, `gate_state` 保留 (status 仍 `waiting`, retry_count=2, raw_message 原文) 作 audit trail / 日后 resume 凭据。
   说明: State Cleanup 表写「用户放弃 → 删除 workflow-state.json」, 而 verdict=fail / Ctrl-C 分支都写「保留」; 这里 PR 已建、gate 未过, 我取保留 (可 resume, 与 Resume 语义段 `gate_state.status==waiting AND pr_number != null` 的入口条件对得上)。两处规则打架, 记 handoff 请复议。
3. **输出 WORKFLOW EXECUTION REPORT**: Status=STOPPED (用户 abort); Phase C 段含 PR_NUMBER / PR_URL / 分支 `fix/147-issue-triage-regression`、C.2.4 三次 verdict=wait 的时间线 (started_at / 3 次 next_check_at / elapsed 92s)、gate raw_message 原文、处方 (a) 命令原文, 以及「后续手动路径: 先 dispatch 出 run → 再 resume workflow 或直接重跑 C.2.4 gate」。
4. `.aria/.workflow-interrupt` 本来不存在, 不动; 不清理 gate_state。
5. handoff 记三条待复议: (i) `max` 未定义 & should_prompt 提前上报的解读; (ii) abort 时 state 文件保留 vs 删除的规则冲突; (iii) gate 输出 (`gate_error.kind=no-run-for-branch` 与 verdict=wait 同在、`pr_ci_status=not_found`) 超出本版 §C.2.4 schema。
