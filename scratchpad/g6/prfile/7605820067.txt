# 竞品 spec 探针 not_established 两情形推演 (audit-engine · challenge · post_spec · Round 1)

设定: checkpoint = `post_spec`, mode = `challenge` (Level 3 → `adaptive_rules.level_3 = "challenge"`, 与题面一致), 本轨 spec 目录 `demo-spec`, repo root `/work/Demo`。以下全部为描述性推演, 未执行任何命令。

## 0. 入口调用与消费契约 (两情形共用)

Round 1 入口的第一步即竞品 spec 探针 (challenge 模式块围栏首行; 与 Step 0 Anchor 固化显式消歧 —— Step 0 在 Round 1 启动前一次性执行, 探针每轮入口跑, 不沿用 Step 编号):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" \
  --own-spec-dir "demo-spec" --repo-path "/work/Demo"
```

消费规则 (SOT: `references/execution-modes.md` `## 竞品 spec 探针 (per-round 入口)`, 自我声明为 stdout 契约 + exit code + 消费措辞的权威可执行版):

1. **(α)** 读 stdout JSON 的**一等字段 `verdict`**, 把结果渲染进当轮 `### Round N` 记录的 `- Sibling probe:` 行 (report-format.md 模板) 并进聚合报告。
2. **(β)** `verdict == not_established` / exit≠0 / stdout 非 JSON / `schema_version` 未知 ⇒ 渲染「**未能核实**」, **不得**渲染为「无竞品」—— 零证据不当正证据。
3. **消费方 fail-closed 义务**: exit≠0 **或** stdout 无法解析为 JSON **或** `schema_version` 未知 ⇒ 一律按 `not_established` 处置。
4. **不阻断**: 探针是 advisory 副机制 —— 不改 verdict 计算、不改收敛判定、不改轮次路由; `sibling_found` 命中尚且只是告警不是判决, `not_established` 更不构成任何 gate。
5. `not_established` 档措辞 (三档, 不得合并): 「**未能核实** —— 本轮竞品扫描未取到完整证据 (原因: <reason>)」。

## 情形 A — exit 0, stdout 为合法 JSON, verdict = not_established

先过门槛: exit==0、stdout 可解析为 JSON、`schema_version == "1"`、`probe == "sibling_spec_probe"` ⇒ 走 **(α)** 正常读 `verdict` 路径 (不触发 fail-closed); `verdict == "not_established"` ⇒ 落 **(β)** 第三档。

这份 stdout 与脚本源码的 fetch 失败路径逐字段吻合 (`run_probe`: `any_fetch_failed` → `status="degraded"` + `reason="fetch_failed"`; `_scan_remote` fetch 两连败 → remote_entry 保留已解析的 `default_branch` 与 `resolved_by`, 带 `error_kind="network"`, `scanned=0`, `refs_scanned=0`): origin 的默认分支解析成功 (`master`, 经 `ls_remote_symref`), 但 fetch 两次尝试均网络失败, 一条 ref 都没扫。own 侧输入健在: `own_layer="canonical"`, `own_keys=[["k","aria-plugin",122]]` 非空 —— 失败纯在远端覆盖面, 不在本轨可比较性。从 `remotes[]` 只有一条记录可知 enforced 集合就是 `{origin}` 一个。

### (1) `### Round 1` 记录里关于探针的那一行

```markdown
### Round 1
- Agents: <agent_list>
- Sibling probe: **未能核实** —— 本轮竞品扫描未取到完整证据 (原因: fetch_failed)
- Conclusions: <count>
- Vote: <PASS/REVISE>
- Duration: <seconds>s
```

`<reason>` 字面取 JSON 一等字段 `reason` 的值 `fetch_failed` (契约保证 `status != "ok"` 或 `verdict == "not_established"` 时该字段必非空)。report-format.md 模板行的紧凑形态 `- Sibling probe: 未能核实 (原因: fetch_failed)` 与之同档 —— execution-modes.md 的三档措辞是权威版, 不合并、不升档, 更不得改写成「无竞品」。

### (2) 对本轮是否继续、verdict 与收敛判定的影响

- **本轮继续, 零阻断**。探针 advisory: 不改 verdict 计算、不改收敛判定、不改轮次路由。Round 1 照常走 challenge 流程 Step 1 讨论组 spawn → Step 2 挑战组质疑 → Step 3 全员合并 → Step 4 挑战组再审 → Step 5 Drift Check。
- **verdict 照常计算**: PASS (0 Critical + 0 Major) / PASS_WITH_WARNINGS (0C + ≥1M) / FAIL (≥1C), 只数审计 Agent 的 findings, 与探针结果零关联 (post_spec 检查点上 audit FAIL 本身也仅记录不阻塞, 更不会被探针翻转)。
- **收敛判定照常**: challenge 收敛 = 提案结论四元组集合无变化 (vs Round N-1) AND objections 全部 `resolved`; 探针结果既不进 comparison_key 也不进 objections, 对判定两不沾; 未收敛则按正常路由进 Round 2。
- 报告面影响仅此一行 (当轮记录 + 聚合报告措辞)。`elapsed_ms=61203` (~61s, 双远端常态 ~25s/轮, 此处被 fetch 失败重试放大) 是记录在案的入口成本, 无 gate 效应。
- 每轮入口重跑 (不复用缓存): Round 2 入口会重新取证, 网络恢复即可自然翻转为 `no_sibling_found` / `sibling_found`。

### (3) 能否据此断言「没有同 issue 的竞品 Spec」

**不能。** 三层依据:

1. 一等字段 `verdict` 就是 `not_established` —— 契约 (β) 明文禁止渲染为「无竞品」: 零证据不当正证据。
2. `no_sibling_found` 的取值前提是 `hits` 为空 **且覆盖完整** (全部 enforced remote 解析出默认分支、fetch 成功、全部 `refs/heads/*` 已枚举、无任何 cap) **且 `own_keys` 非空**。本例 own_keys 非空, 但 fetch 失败、覆盖不完整 —— 结构上到不了这一档。
3. 消费方不得从 `hits == []` 推断结论 —— 「扫完没有」与「没扫到」在 `hits` 上取值相同; 本例 `remotes[].scanned == 0`、`refs_scanned == 0` 实际是后者: 一条 ref 都没扫。

据此能说的最强命题: 「origin (唯一 enforced remote) 默认分支解析成功, 但 fetch 网络失败, 竞品语料覆盖为零; 同 issue 竞品 Spec 的存在性未知」。若写成「无竞品」, 即把 advisory 通道的覆盖缺口伪装成正结论 —— 正是 (β) 要防的形态。

## 情形 B — exit 1, stdout 为空, stderr 是 Python traceback

脚本侧定位: `main()` 只在 `run_probe` 抛内部异常时走 `traceback.print_exc(file=sys.stderr); return 1`, 此前 stdout 从未写入, 故为空。exit 1 + traceback 形态与该分支严格相符 (参数错 / 仓库不可读是 exit 2 且 stderr 非 traceback; sister module 不可导入是 exit 3, stderr 是日志行不是 traceback)。即: 探针进程自身崩溃, 十二字段 JSON 一个都没产出。

### (1) `### Round 1` 记录里关于探针的那一行

触发 fail-closed 义务 (exit≠0 ⇒ 一律按 `not_established` 处置; 本例同时满足 stdout 无法解析为 JSON):

```markdown
### Round 1
- Agents: <agent_list>
- Sibling probe: **未能核实** —— 本轮竞品扫描未取到完整证据 (原因: 探针自身失败 exit=1, stdout 无 JSON)
- Conclusions: <count>
- Vote: <PASS/REVISE>
- Duration: <seconds>s
```

与情形 A 的差别只在 `<reason>` 的来源: A 有结构化来源 (JSON `reason` 字段); B 没有 JSON, 消费方按可观测失败形态概括填写 (exit≠0 + stdout 空非 JSON ⇒ 探针自身失败 —— 参数错 / 内部异常 / 仓库不可读; 此处 traceback 指向内部异常)。契约只钉死档位与 `<reason>` 槽位, 不要求把 stderr traceback 原文搬进报告行。禁止渲染为「无竞品」同样适用。

### (2) 对本轮是否继续、verdict 与收敛判定的影响

与情形 A 完全同构: **不阻断**。fail-closed 把 B 折叠到与 A 相同的消费终点 (按 `not_established` 渲染「未能核实」), 而 `not_established` 本身就是 advisory:

- Round 1 照常进入 challenge Step 1-5, 本轮继续;
- verdict 照常由 Critical/Major 计数得出 —— 探针崩溃不产生 finding、不进 severity 统计、不改 verdict;
- 收敛判定与轮次路由照常 (四元组集合比较 + objections `resolved`; 未收敛正常路由 Round 2);
- 下轮入口重跑探针: 崩溃若为一过性 (环境 / 瞬时异常) 可自行恢复, 逐轮各自取证。

### (3) 能否据此断言「没有同 issue 的竞品 Spec」

**不能, 且证据面比 A 更弱。** A 至少还有一份自洽的结构化输出, 能定位缺口在哪 (origin fetch 网络失败, scanned=0); B 连 `verdict` 都读不到, 十二字段一个都没有 —— 不存在任何证据面。fail-closed 义务的存在意义正在于此: 探针自身失败时, 禁止把「没有输出」当「没有竞品」。据此能说的最强命题: 「探针进程自身异常退出 (exit=1, stdout 空), 未产出任何判定; 同 issue 竞品 Spec 存在性未知」。

## A / B 对照

| | 情形 A | 情形 B |
|---|---|---|
| 契约路径 | (α) 正常读 verdict → (β) not_established 档 | fail-closed (exit≠0) → 强制按 not_established 处置 |
| 语义 | 探针跑完了一次有定义的判定, 判定面落在「未能建立」(覆盖缺口 = origin fetch 网络失败) | 探针没跑成 (自身内部异常), 无判定面 |
| `<reason>` 来源 | JSON `reason` 字段 = `fetch_failed` | 可观测形态: exit=1 + stdout 空非 JSON |
| Round 1 行 | 未能核实 (原因: fetch_failed) | 未能核实 (原因: 探针自身失败 exit=1, stdout 无 JSON) |
| 是否继续 / verdict / 收敛 | 三者均不受影响 (advisory, 不阻断) | 同左 |
| 断言「无竞品」 | 禁止 (verdict 明示未建立; scanned=0, 零覆盖) | 禁止 (连 verdict 都不存在, 零证据面) |
