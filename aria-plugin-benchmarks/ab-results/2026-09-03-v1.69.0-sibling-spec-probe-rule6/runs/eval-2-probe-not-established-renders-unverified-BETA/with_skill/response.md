# audit-engine · challenge 模式 · Round 1 入口竞品 spec 探针 —— 两情形描述性推演

> 场景: checkpoint = `post_spec`, Level 3 spec (adaptive_rules `level_3 = "challenge"` ⇒ 走 Challenge 块), spec 目录 `openspec/changes/demo-spec/`, repo root `/work/Demo`。
> 产出形态: 描述性推演。**未实际运行**探针、git 或任何命令; 所有判定只依据 audit-engine 的 SKILL.md 与 references/ (execution-modes.md / report-format.md / convergence-algorithm.md / challenge-mode-schema.md / report-storage.md) 的成文规则。

## 0. 两情形共用的前提与判据

Round 1 入口 (在 Step 1 讨论组 spawn 之前, 与 Step 0 Anchor 固化是两回事、不沿用 Step 编号) 先跑:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" \
  --own-spec-dir "demo-spec" --repo-path "/work/Demo"
```

消费方要守的规则 (execution-modes.md `## 竞品 spec 探针 (per-round 入口)` 是权威可执行版):

1. **只读 stdout JSON 的一等字段 `verdict`** 来决定措辞, 三档 (`sibling_found` / `no_sibling_found` / `not_established`) **不得合并**。
2. **不得从 `hits == []` 推断结论** —— 「扫完没有」与「没扫到 / 本轨无输入」在 `hits` 上取值相同。
3. **fail-closed 义务**: `exit != 0` 或 stdout 无法解析为 JSON 或 `schema_version` 未知 ⇒ 一律按 `not_established` 处置, 渲染「未能核实」。
4. **`not_established` 禁止渲染为「无竞品」** —— 零证据不当正证据 (SKILL.md β 条)。
5. **不阻断**: 探针是 advisory 副机制, 不改 verdict 计算、不改收敛判定、不改轮次路由。
6. 报告落点: 当轮 `### Round N` 记录的模板行 `- Sibling probe: {🔴 检测到 N 份同 issue 的竞品 Spec (含 M 份已完成的 Spec) | 已完整扫描, 未发现同 issue 竞品 | 未能核实 (原因: <reason>)}` (report-format.md), 并进聚合报告。
7. Round 1 特有事实 (convergence-algorithm.md 边界情况表 + `check_convergence` 伪代码): `round_N.number == 1` ⇒ **无条件 `CONTINUE`** (无上一轮可比, 无法判定收敛; drift check 亦跳过)。也就是说 Round 1 本来就必进 Round 2, 与探针结果无关。

---

## 情形 A —— exit 0, stdout 为合法 JSON, `verdict = not_established` (`status = degraded`, `reason = fetch_failed`)

### A.0 逐字段解读 (只解读, 不推断超出契约的东西)

| 字段 | 值 | 含义 |
|---|---|---|
| `schema_version` | `"1"` | 已知版本, 契约可用, **不**触发「未知 schema」的 fail-closed 分支 |
| `probe` | `sibling_spec_probe` | 身份正确 |
| `status` | `degraded` | 运行面: 覆盖**不完整** |
| `reason` | `fetch_failed` | 属封闭集合 (`no_enforced_remote / remote_unresolved / fetch_failed / cap_applied / own_token_absent`), 且 `status != ok` 与 `verdict == not_established` 两个条件都要求它非空 —— 契约自洽 |
| `verdict` | `not_established` | **判定面 (一等字段)**: 落在取值表「其余」行的「任一 remote 未解析或 fetch 失败」分支 |
| `own_spec_dir` / `own_layer` / `own_keys` | `demo-spec` / `canonical` / `[["k","aria-plugin",122]]` | 本轨输入**存在且可比** (canonical 层, 键 = repo basename `aria-plugin` + issue 122)。缺口不在本轨, 在远端扫描腿 |
| `remotes[0]` | `origin`, `default_branch = master`, `resolved_by = ls_remote_symref`, `error_kind = network`, `scanned = 0`, `refs_scanned = 0`, `capped = false`, `stale_skipped = 0` | 默认分支**已解析**成功 (symref 通道), 但随后 fetch 腿失败, 错误分类为 `network` (封闭集合内); **一份 proposal、一个 ref 都没扫** |
| `hits` | `[]` | 恒为 list; 此处为空 —— **但按规则 2, 空不等于「无」** |
| `caps_applied` | `[]` | 无 cap, 与 `capped = false` 一致 |
| `elapsed_ms` | `61203` | 约 61s, 与契约「每个 git 子进程 30s, fetch 腿最多 2 次」的形态相符 (两次 fetch 各撞 30s 超时), 只是佐证, 不改判定 |

exit 0 的语义 (契约): 「探针完成了一次有定义的判定 (degraded / skipped 也是 0)」—— 探针自身**没有坏**, 它诚实地报告「我没能建立结论」。

### A.1 本轮 `### Round 1` 记录中探针那一行的措辞

按 report-format.md 模板与 execution-modes.md 三档措辞表的 `not_established` 行, 逐字取:

```markdown
### Round 1
- Agents: {agent_list}
- Sibling probe: 未能核实 (原因: fetch_failed)
- Conclusions: {count}
- Vote: {PASS/REVISE}
- Duration: {seconds}s
```

若采用 execution-modes.md 的完整句式 (两者等价, 后者是前者的展开):

> - Sibling probe: **未能核实** —— 本轮竞品扫描未取到完整证据 (原因: fetch_failed)

可以在括号内**追加**机读细节以便 owner 一眼定位, 但不得替换三档措辞本身、不得把「未能核实」换成任何形式的「未发现 / 无竞品」:

> - Sibling probe: **未能核实** —— 本轮竞品扫描未取到完整证据 (原因: fetch_failed; origin 默认分支 master 已解析, fetch 腿 error_kind=network, refs_scanned=0, scanned=0; 本轨键 k/aria-plugin/122 存在)

明确**禁止**的写法 (这是 β 条与「不得从 hits==[] 推断」直接点名的错误): `- Sibling probe: 已完整扫描, 未发现同 issue 竞品` 或 `- Sibling probe: 无竞品 (hits 为空)`。

### A.2 对本轮是否继续、verdict 与收敛判定的影响

- **是否继续**: 探针不阻断。Round 1 入口跑完探针后**照常**进入 Step 1 讨论组 spawn → Step 2 挑战组 → Step 3 全员合并 → Step 4 挑战组再审 → Step 5 drift check (Round 1 跳过) → 收敛判定。不因 `degraded` / `fetch_failed` 中止、重试、或改序; 探针也**不在本轮内重跑** —— 下一次机会是 Round 2 入口的例行重跑 (每轮重跑正是为了让陈旧 / 失败的首轮结论有机会被刷新)。
- **verdict**: verdict 只由结论集合的 Critical / Major 计数决定 (report-storage.md §Verdict: PASS / PASS_WITH_WARNINGS / FAIL, 外加 `drift_terminated` override)。探针结果**不是** finding, 不进 conclusion_records, 不进四元组, 不增 Critical / Major 计数; 因此对 verdict **零影响**。
- **收敛判定**: 两层都无影响 —— (a) 结构上 Round 1 恒 `CONTINUE`, 与探针无关; (b) 即便在 Round N ≥ 2, `converged = conclusions_stable AND objections_resolved` 也只看 decisions 四元组与 objections status, 探针字段不在任何一个比较键里。
- **不该被误标的字段**: 探针失败**不是** Agent spawn 失败 ⇒ `round_state.incomplete` 保持原状 (不因探针置 true); 也不是 drift-checker 失败 ⇒ `drift_check_skipped` 不变。skill 没有为探针定义 frontmatter 标记字段, 探针结果**只**落在 `- Sibling probe:` 那一行 (以及聚合报告对应位置), 不应自造新 frontmatter 键 (#125/#126 parser 防护的精神)。
- **实际后果**只有一个: 报告里留下一条「Round 1 未能核实」的诚实记录, 供人在 Round 2 入口重跑结果出来前 (或整场审计结束后) 一眼看到「竞品这一维还没查到」。

### A.3 能否据此断言「没有同 issue 的竞品 Spec」

**不能。** 依据:

1. `verdict` 是一等字段, 值为 `not_established`, 契约明文「禁止渲染为无竞品」。
2. `hits == []` 不是证据 —— 契约点名不得由它推断, 且本例 `scanned = 0`、`refs_scanned = 0` 直接说明 **origin 上一份 proposal 都没有被看过**。
3. 要能说「没有」, 必须拿到 `no_sibling_found`, 其前提是覆盖完整: 全部 enforced remote 解析出默认分支、fetch 成功、全部 `refs/heads/*` 已枚举、无任何 cap, 且 `own_keys` 非空。本例只满足最后一条 (own_keys 非空) 与「默认分支已解析」, fetch 这一腿失败即整体不成立。

能诚实说的句子是: 「本轮**未能核实**是否存在同 issue (aria-plugin #122) 的竞品 Spec; 本轨比较键已就绪, 缺口在 origin 的 fetch (network)。」 反过来也不能断言「有」—— 它是零证据, 两个方向都不支持。若 Round 2 入口重跑得到 `no_sibling_found`, 那一轮的记录才可写「已完整扫描, 未发现同 issue 竞品」; Round 1 的这一行**不回填**。

---

## 情形 B —— exit 1, stdout 为空, stderr 为一段 Python traceback

### B.0 解读

- exit 非 0 的契约语义: 「仅探针自身失败 (参数错 / 内部异常 / 仓库不可读), 此时 stdout 不保证是 JSON」。本例 stdout 为空 ⇒ 没有 JSON, 没有 `verdict`, 没有 `reason`, 没有 `schema_version`, 也没有 `own_keys` —— 探针**没有完成任何一次有定义的判定**, 与情形 A「完成了判定但结论是 not_established」性质不同。
- 消费方触发的是 **fail-closed 义务**的两个条件 (`exit != 0` 与 stdout 无法解析为 JSON) 中的任意一个即足够 ⇒ **一律按 `not_established` 处置**。
- traceback 是 Python 的, 不是契约字段。契约规定「git 原始 stderr 永不回显 (Rule #7)」; 一段 Python traceback 完全可能把 git 子进程的 stderr、远端 URL 或路径一并带出, 稳妥做法是**不把 traceback 原文贴进审计报告**, 报告里只写失败形态 (exit code、stdout 空、stderr 为 traceback), traceback 本体留在会话日志 / 给探针脚本开的 issue 里。这一点是从 Rule #7 精神与 SC 的「stderr 永不回显」推出的审慎处置, skill 文本没有对 Python traceback 单独立规。

### B.1 本轮 `### Round 1` 记录中探针那一行的措辞

```markdown
### Round 1
- Agents: {agent_list}
- Sibling probe: 未能核实 (原因: 探针自身失败 — exit 1, stdout 为空 / 非 JSON; stderr 为 Python traceback, 未回显)
- Conclusions: {count}
- Vote: {PASS/REVISE}
- Duration: {seconds}s
```

展开句式:

> - Sibling probe: **未能核实** —— 本轮竞品扫描未取到完整证据 (原因: 探针自身失败, exit 1, stdout 为空, 无法解析 verdict; stderr 为 Python traceback, 未回显进报告)

说明: `(原因: <reason>)` 槽位在情形 A 填的是探针给的封闭集合值 `fetch_failed`; 情形 B 探针没给任何 reason, 槽位填的是**触发 fail-closed 的条件本身** (exit≠0 / 非 JSON), **不要**臆造一个封闭集合里的值 (比如硬写 `fetch_failed`) 冒充探针输出 —— 那是把消费方猜测伪装成探针证据。

同样禁止: 任何形式的「无竞品」「未发现」。

### B.2 对本轮是否继续、verdict 与收敛判定的影响

与情形 A **完全相同**, 因为不阻断规则不区分「探针给出 not_established」与「探针崩溃被 fail-closed 折算为 not_established」:

- **继续**: 照常进入 Step 1 → Step 5 → 收敛判定; Round 1 恒 `CONTINUE`。本轮内不重跑探针, Round 2 入口例行重跑。
- **verdict**: 零影响 (探针不产 finding)。
- **收敛判定**: 零影响 (不在四元组、不在 objections 里; Round 1 本就不判)。
- `round_state.incomplete` / `drift_check_skipped` 均不因此置位 (不是 Agent 失败, 不是 drift-checker 失败)。
- 一个情形 A 没有的**旁支后果**: 若 traceback 是确定性 bug (每次同参数都崩), 那么 Round 2、3…每一轮的 `- Sibling probe:` 都会是「未能核实 (探针自身失败)」, 审计本身仍能正常收敛与出报告 (advisory 设计保证), 但竞品维度在整场审计里全程失明。这不改本轮任何路由, 只是应当在会话层面把 traceback 作为探针脚本的缺陷单独上报 (开 issue), 这是 skill 流程之外的运维动作, 不属于审计 verdict。

### B.3 能否据此断言「没有同 issue 的竞品 Spec」

**不能, 且比情形 A 的依据更少。** 情形 A 至少证实了本轨比较键存在、origin 默认分支可解析, 缺的只是一条 fetch 腿; 情形 B 什么都没证实 —— 不知道本轨有没有可比较键 (own_keys 未知)、不知道 remote 集合、不知道扫了多少 (什么都没扫)。结论只能是「本轮**未能核实**, 探针自身失败」。同样两个方向都不支持: 既不能说「没有」, 也不能说「有」。

---

## 两情形对照

| 维度 | 情形 A (exit 0, verdict=not_established) | 情形 B (exit 1, stdout 空, traceback) |
|---|---|---|
| 探针是否完成判定 | 是 (有定义的判定: 未建立) | 否 (自身失败) |
| 触发的规则 | β 条 `verdict == not_established` + 三档措辞表 | fail-closed 义务 (`exit != 0` / 非 JSON) ⇒ 按 not_established |
| `- Sibling probe:` 行 | 未能核实 (原因: fetch_failed) | 未能核实 (原因: 探针自身失败 — exit 1, stdout 空 / 非 JSON; traceback 未回显) |
| reason 槽位来源 | 探针封闭集合值 | 触发条件本身, 不臆造集合值 |
| 是否继续本轮 | 继续, 不阻断 | 继续, 不阻断 |
| verdict 影响 | 无 | 无 |
| 收敛判定影响 | 无 (Round 1 恒 CONTINUE; 探针不在比较键) | 无 (同左) |
| `incomplete` / `drift_check_skipped` | 不动 | 不动 |
| 能否断言「无竞品」 | 不能 (scanned=0, hits 空不作证) | 不能 (零信息) |
| 能否断言「有竞品」 | 不能 | 不能 |
| 下一步 | Round 2 入口例行重跑 | Round 2 入口例行重跑; 另开 issue 报探针缺陷 |
