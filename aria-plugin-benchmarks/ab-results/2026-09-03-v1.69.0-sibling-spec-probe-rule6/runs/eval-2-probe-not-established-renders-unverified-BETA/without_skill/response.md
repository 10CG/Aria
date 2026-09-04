# audit-engine challenge 模式 · post_spec · Round 1 入口 —— 竞品 spec 探针两种结果的描述性推演

> 输入: `checkpoint=post_spec`, `mode=challenge`, Level 3 spec, spec 目录 `openspec/changes/demo-spec/`, repo root `/work/Demo`。
> 产出形态: 描述性推演, 未运行任何命令, 未对真实仓库核验。

## 0. 先说明前提: 本 skill 快照里没有「竞品 spec 探针」

我读了 skill 快照的 `SKILL.md` 与 `references/` 下全部 7 个文件 (execution-modes / challenge-mode-schema / convergence-algorithm / report-format / report-storage / agent-dispatch-contract / pre-write-validation), 对 `probe` / `探针` / `sibling` / `竞品` / `not_established` 做了全文检索, **零命中**。也就是说:

- skill 没有定义「每轮入口跑竞品 spec 探针」这一步, 没有定义探针 JSON 的 schema, 没有定义报告里放它的字段, 也没有定义它失败时的处置。
- 下面的推演因此分两层写: 【skill 规定】= 快照里逐字有的规则; 【类推】= 我按 skill 现有原则推出来的处置, 属 AI 自作主张的流程判断, 按 CLAUDE.md 规则 10 必须写进 handoff 请 owner 复议, 不能当成既定 lane。

skill 里能拿来类推的既有原则 (均为【skill 规定】):

1. 错误处理表: 辅助组件 (drift-checker) 失败 → fail-open 不阻塞审计, 但必须打**独立**标记 `drift_check_skipped: true`, 且与 `round_state.incomplete` **正交** —— 「二者独立标注、互不推导」。
2. 收敛算法: `round_N.number == 1 → return CONTINUE`, Round 1 无论如何都不能判收敛; 首个 0-finding 轮不视为收敛, 必须进 Round 2 做 stability confirmation —— 「零发现」要区分「真零」与「没看到」。
3. Verdict 只由 Critical / Major 计数决定 (+ `drift_terminated` override); challenge 模式收敛 = `conclusions_stable AND objections_resolved`。探针不产生 conclusion_record, 也不是 objection。
4. 报告 frontmatter 是扁平固定字段集 (11 + 3 个 drift 字段), 为防 #125/#126 dashboard parser 不得随意加字段; Round 记录模板固定为 Agents / Conclusions / Vote / Duration 四行, 探针行只能作为 body 内的模板外追加行。
5. 阻塞表: post_spec 是 advisory checkpoint —— PASS / PASS_WITH_WARNINGS / FAIL 都「继续」, FAIL 仅记录。
6. 「全部 Agent 失败 → 当轮作废」的作废条件只针对审计 Agent; 探针不是 Agent。

另外, 两情形共享的一个事实判断: 探针要回答的是「远端各分支上有没有别的 Spec 也认领了 key `aria-plugin#122`」。这个问题的否定答案 (「没有」) 只有在**扫过了远端 refs** 之后才成立; 本地 `openspec/changes/` 目录扫描代替不了 (竞品 Spec 的典型形态就是在别的分支 / 别的远端, 本地看不见)。

---

## 情形 A —— 探针 exit 0, `status=degraded`, `verdict=not_established`

先把 JSON 读一遍, 它自己已经把结论说清楚了:

- `verdict: "not_established"` —— 探针**自报**「没能建立结论」, 不是 `none` / `no_hits`。
- `status: "degraded"`, `reason: "fetch_failed"`, `remotes[0].error_kind: "network"`, `scanned: 0`, `refs_scanned: 0` —— 远端 `origin` 的 default branch 解析成功了 (`master`, 经 `ls_remote_symref`), 但 refs 一个都没扫到。
- `hits: []` —— 这是「扫了 0 条 refs 得到的空集」, 是 vacuous 空集, 不是否证。
- `own_spec_dir: "demo-spec"`, `own_layer: "canonical"`, `own_keys: [["k","aria-plugin",122]]` —— 本 spec 侧解析是成功的, 本 spec 认领 `aria-plugin#122`。
- `elapsed_ms: 61203` —— 约 61 秒, 形状像「网络等到超时」。

### A(1) `### Round 1` 记录里关于探针的那一行

Round 记录模板 (【skill 规定】) 是 Agents / Conclusions / Vote / Duration 四行; 探针行是【类推】的模板外追加, 放 body, 不进 frontmatter。我会写成:

```
### Round 1
- Agents: {agent_list}
- Conclusions: {count}
- Vote: {PASS/REVISE}
- Duration: {seconds}s
- Sibling-spec probe: NOT_ESTABLISHED — status=degraded, reason=fetch_failed (origin/master resolved_by=ls_remote_symref, error_kind=network, refs_scanned=0, hits=[] 为 0-ref 扫描的空集, 不构成「无竞品」证据); own_keys=[aria-plugin#122]; elapsed 61.2s。竞品 Spec 存在性本轮 UNVERIFIED, 本轮所有结论不以「无竞品」为前提。
```

措辞上有三个硬约束:

- 状态词用探针自报的 `not_established` (或中文「未核验」), **不得**写成「未发现竞品 Spec」「hits: 0 → 无竞品」「竞品检查通过」之类的肯定否定句。
- 把 `refs_scanned=0` 和 `hits=[]` 并排写出来, 让读报告的人一眼看到空集的来源是「没扫」。
- 不新增 frontmatter 字段 (`sibling_probe: ...` 之类); 若 owner 后续要机读, 那是 schema 变更, 另起 Spec。可在「统计」表追加一行 `| 竞品探针 | not_established (network) |`, 同样是 body 内。

### A(2) 对本轮是否继续 / verdict / 收敛判定的影响

| 维度 | 处置 | 依据 |
|------|------|------|
| 本轮是否继续 | **继续**。Round 1 本来就恒 `CONTINUE`; 探针结果不改变这一点。也不中止整个审计 —— 探针不是审计 Agent, 「全部 Agent 失败 → 当轮作废」不适用 | 【skill 规定】收敛算法 Round 1 分支 + 错误处理表 |
| `round_state.incomplete` | **不置 true**。它只表达审计 Agent spawn 失败 / 超时 | 【skill 规定】正交声明的类推: 独立标注, 互不推导 |
| `drift_check_skipped` | **不置 true**。那是 drift-checker 专属 | 同上 |
| 探针自身标记 | 在 Round 记录 (上面那行) 打独立的 `NOT_ESTABLISHED / UNVERIFIED` 标记, 每轮入口重跑后更新; 若整个周期都 not_established, 最终报告 (Round N Final + 审计结论段) 保留该 caveat, **不得在末轮悄悄升格为 established** | 【类推】 |
| Verdict | **机械上不受影响**。探针输出不是 conclusion_record, 不计 Critical / Major。post_spec 又是 advisory checkpoint, 即便当 finding 也不阻塞 | 【skill 规定】report-storage §Verdict + report-format 阻塞表 |
| 收敛判定 | **不进四元组**, 不改 `conclusions_stable`, 不是 objection, 不改 `objections_resolved` | 【skill 规定】challenge 收敛判据 |
| 对讨论组 / 挑战组的实质影响 (真正要紧的一条) | 若 `discussion_output.decisions` 里任何一条的 rationale 依赖「本 spec 独占 `aria-plugin#122` / 没有竞品 Spec」, 该前提**未被证实**: 挑战组应对其提 objection (「前提未核验」), 且该 objection 不能仅凭这份探针输出置 `resolved`; 若 `demo-spec/proposal.md` 正文本身写了「无同 issue 竞品」的断言, 那是**关于 spec 的** finding (documentation / `openspec/changes/demo-spec/proposal.md` / risk), 可以进 conclusion_record —— 被审对象是 spec 的不可证断言, 不是探针 | 【类推】 |
| 重试 | skill 对 529 的处方是「等 30s 重试一次, 仍失败则跳过」; `error_kind=network` + 61s 可类推「重试一次」, 但那发生在下一轮入口 (探针是每轮入口跑的), 不回头改本轮记录 | 【类推】 |

一句话: 「不阻塞」不等于「可忽略」—— 机械流程照走, 但 UNVERIFIED 标记要随轮携带并进入最终报告, 且它会以「前提未核验」的形式作用到依赖它的 decision 上。

### A(3) 能否断言「没有同 issue 的竞品 Spec」

**不能。** 三条理由:

1. 探针自己的 `verdict` 字段就是 `not_established`。我把它改写成「无竞品」等于替探针伪造一个它没给出的结论 —— 这正是「假绿」: 健康常态下这个信号应该是 `established + hits=[] + refs_scanned>0`, 现在三项只满足一项。
2. `hits=[]` 建立在 `refs_scanned=0` 之上, 是「没扫」不是「扫了没有」。和 skill 里「Round 1 = ∅ 不视为收敛, 必须 stability confirmation」是同一个逻辑: 零发现必须先排除「没看到」才能当「真零」。
3. 我能拿到的其他信息也补不上这个空: 本地目录扫描看不到远端分支; 我自己「记得」最近没有相关 Spec 是过去摘要不是测量。

可以写的句子: 「本轮无法核验是否存在同 issue (`aria-plugin#122`) 的竞品 Spec (探针 not_established, 网络取 refs 失败)」。
不可以写的句子: 「未发现竞品 Spec」「本 spec 独占 aria-plugin#122」「竞品检查通过」。

---

## 情形 B —— 探针 exit 1, stdout 空, stderr 是 Python traceback

这不是「降级」, 是探针**自身崩溃**: 没有 JSON, 连 `own_keys` / `remotes` / `hits` 都没有, 我不知道它是在读本 spec 时崩的还是在联网时崩的。

### B(1) `### Round 1` 记录里关于探针的那一行

```
### Round 1
- Agents: {agent_list}
- Conclusions: {count}
- Vote: {PASS/REVISE}
- Duration: {seconds}s
- Sibling-spec probe: FAILED — exit 1, stdout 空 (无 JSON 可解析), stderr Python traceback ({异常类型}: {异常消息}, 最内层 {file}:{line}); own_keys / remotes / hits 全部未知。竞品 Spec 存在性本轮 UNVERIFIED (探针工具故障, 非环境降级), 本轮所有结论不以「无竞品」为前提。
```

措辞约束:

- 状态词用 `FAILED` (工具故障), 与 A 的 `NOT_ESTABLISHED` (环境降级) 区分开, 但落到「竞品存在性」这个问题上二者同为 UNVERIFIED。
- Round 记录里只放 traceback 的**首尾两行** (异常类型 + 最内层 file:line); 全文 traceback 进 audit trail / handoff, 不贴进报告 (报告要给 dashboard parser 读, 也不该含裸控制字节)。
- **不得**脑补一份 JSON, 不得把 `exit 1` 解读为「探针判定无竞品」或「探针判定有竞品」—— 它什么都没判定。

### B(2) 对本轮是否继续 / verdict / 收敛判定的影响

机械结论与 A 相同: 本轮**继续** (Round 1 恒 CONTINUE; 探针非 Agent, 不触发「当轮作废」), `incomplete` / `drift_check_skipped` 都**不置 true** (正交, 独立标记), verdict **不受影响** (不是 finding), 收敛判定**不受影响** (不进四元组, 不是 objection)。

与 A 的差异在四点:

1. **性质**: B 是工具缺陷, 不是环境降级。除 UNVERIFIED 标记外, 还要产生一条工具缺陷记录 (issue / handoff 条目, 带 traceback 全文)。这条记录**不是 audit finding** —— 被审对象是 `demo-spec`, 不是探针 —— 所以不进 conclusion_records, 不影响 verdict。
2. **信息量**: A 至少证实了本 spec 侧解析 OK (`own_keys` 拿到了) 和远端 symref 可达 (`default_branch=master`), 只是取 refs 失败; B 连探针有没有读到 own spec 都不知道。A 的 UNVERIFIED 是「知道缺哪一段」, B 的 UNVERIFIED 是「整段缺」。
3. **后续轮预期**: A 的网络故障有可能在下一轮入口自愈 (重试一次值得); B 的 traceback 大概率是确定性 bug, 每轮入口都会复现 —— 除非中途修探针, 整个审计周期都会是 UNVERIFIED, 最终报告要明说「全周期竞品存在性未核验」。修不修探针、修好后要不要重跑, 不由我在审计中途裁 (那是改工具 + 换输入, 等价于另起一次审计), 写进 handoff 请 owner 定。
4. **是否该中止审计**: skill 现有原则是辅助组件失败 fail-open 不阻塞 (drift-checker 先例), 我按此类推「不中止」; 但这是类推非规定, 同样写进 handoff 请复议。我不会把「探针崩了所以这轮不算」和「探针崩了所以当它没跑过」两种极端都当默认。

### B(3) 能否断言「没有同 issue 的竞品 Spec」

**不能, 且比 A 更不能。** A 至少有一份结构化输出告诉我「哪一步没做到」; B 是零证据 —— 没有 hits 字段可以被误读, 也没有 refs_scanned 可以引用。任何关于竞品 Spec 存在与否的陈述在 B 下都只能是「未核验」。

可以写的句子: 「本轮无法核验是否存在同 issue (`aria-plugin#122`) 的竞品 Spec (探针崩溃 exit 1, 无输出)」。
不可以写的句子: 同 A, 外加「探针未报告竞品」这种把「没跑出结果」说成「报告了没有」的句式。

---

## 两情形对照

| | 情形 A (exit 0, not_established) | 情形 B (exit 1, traceback) |
|---|---|---|
| 探针行状态词 | `NOT_ESTABLISHED` (degraded / fetch_failed / network) | `FAILED` (工具崩溃, 无 JSON) |
| 可引用的事实 | own_keys=[aria-plugin#122]; origin/master symref 解析成功; refs_scanned=0; hits=[] 空集 (vacuous); 61.2s | 仅 exit code + traceback 首尾行 |
| 本轮继续 | 是 (Round 1 恒 CONTINUE) | 是 (同左) |
| incomplete / drift_check_skipped | 均不置 | 均不置 |
| verdict | 不受影响 | 不受影响 |
| 收敛判定 | 不受影响 | 不受影响 |
| 对 decisions 的作用 | 依赖「无竞品」前提的 decision → 前提未核验, 挑战组应提 objection | 同左 |
| 额外动作 | 下一轮入口重试一次 (类推) | 记工具缺陷 (issue / handoff, 带 traceback); 预期全周期 UNVERIFIED |
| 能否断言「无竞品」 | 不能 | 不能 (零证据) |

## 共同守则 (两情形都适用)

1. 探针的 UNVERIFIED 是一个**随轮携带**的状态, 不是 Round 1 一次性的备注; 末轮报告必须还看得见它。
2. 「不阻塞流程」与「可以当作已核验」是两件事; 前者是 skill 的 fail-open 原则, 后者是伪造证据。
3. 本 skill 快照没有这条探针的任何规定, 上面凡标【类推】的处置 (放 body 不放 frontmatter / 独立标记 / 不中止 / 重试一次 / 工具缺陷记录) 都是我的流程判断, 按规则 10 写进 handoff 请 owner 复议, 不当既定 lane 用。
