# audit-engine challenge 模式 Round 1 入口 — 竞品 spec 探针两情形描述性推演

> 产出形态: descriptive (描述性推演)。全程只读 SKILL.md / references / scripts 源码, 未实际执行任何命令、未做任何 git 读写、未调 forgejo 接口。
> 依据: `aria/skills/audit-engine/SKILL.md` §「per-round 入口探针」+ `references/execution-modes.md` §「竞品 spec 探针 (per-round 入口)」(stdout 契约 + exit code + 三档消费措辞的**权威可执行版**) + `references/report-format.md` 轮次记录模板 + `scripts/sibling_spec_probe.py` 源码 (只读)。

## 0. 推演前提: 探针在本题流程中的位置与调用

- 场景参数: `checkpoint=post_spec`, `mode=challenge` (Level 3, 与 `adaptive_rules.level_3="challenge"` 下游一致), spec 目录 `openspec/changes/demo-spec/`, repo root `/work/Demo`, 进入 Round 1。
- `post_spec` **不是** `pre_merge`, 故 pre-merge completeness gate 不参与 (那条机械检查是 pre_merge 专属, SKILL.md 有「与上方探针无关的另一条机械检查」的显式消歧 —— 它的 fail-closed 是「拒绝执行审计」, 与探针的 fail-closed「按 not_established 渲染」后果完全不同, 不得混淆)。
- Step 0 (Anchor 固化) 在 Round 1 启动前**一次性**执行; 竞品 spec 探针是**每轮入口** (Round 1, 2, …, N) 重跑, 两者显式消歧、互不沿用编号。Round 1 入口的第一件事就是跑探针:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/audit-engine/scripts/sibling_spec_probe.py" \
  --own-spec-dir "demo-spec" --repo-path "/work/Demo"
```

- 读法 (SKILL.md (α)/(β)): **(α)** stdout 合法 JSON 且 `schema_version="1"` 时, 读一等字段 `verdict` 按三档渲染; **(β)** `verdict == not_established` / `exit≠0` / stdout 非 JSON / `schema_version` 未知 ⇒ 渲染「**未能核实** (原因: <reason>)」, **不得**渲染为「无竞品」—— 零证据不当正证据。
- 渲染落点: 当轮 `### Round N` 记录的 `- Sibling probe:` 行 (report-format.md 模板), 并进聚合报告; frontmatter 无探针字段。

---

## 1. 情形 A: exit 0, stdout 为合法 JSON, `status="degraded"`, `reason="fetch_failed"`, `verdict="not_established"`

先核对这份 stdout 与源码的自洽性 (只读推演, 不执行): 十二字段齐全、`schema_version="1"`; `remotes[0]` 形态逐字段吻合 `_scan_remote` 的 fetch-failed 返回 (默认分支已解析 `master`/`resolved_by="ls_remote_symref"`, 失败在 fetch 腿: `error_kind="network"`, `scanned=0`, `refs_scanned=0`); `run_probe` 聚合后 `any_fetch_failed=True → reason="fetch_failed"`, `status="degraded"`, `hits=[]` 且 `status!="ok"` → `verdict="not_established"`。`elapsed_ms=61203` 与 fetch 腿最多 2 次 × 30s 预算的慢网络失败自洽。另注意 `own_keys=[["k","aria-plugin",122]]` 非空、`own_layer="canonical"` —— 本轨输入面完好, 判定未成立纯因远端覆盖缺口 (不是 `own_token_absent` 路径)。

### (1) `### Round 1` 记录中探针那一行的措辞

走 (α) 正门: exit=0、stdout 是合法 JSON、`schema_version` 已知 ⇒ **不触发**消费方 fail-closed 侧通道; 直读一等字段 `verdict="not_established"` 落 (β) 渲染分支。`reason` 直接取 stdout 的结构化 `reason` 字段。按权威三档措辞表 (execution-modes.md):

```markdown
### Round 1
- Agents: …
- Sibling probe: 未能核实 —— 本轮竞品扫描未取到完整证据 (原因: fetch_failed)
- Conclusions: …
```

(report-format.md 模板占位短式即 `- Sibling probe: 未能核实 (原因: fetch_failed)`。) 两个措辞来源在此档一致; `status="degraded"` 本身**不是**第四档措辞 —— 「(覆盖不完整: <reason>)」追注仅属 `sibling_found` 档, 本档的缺口已由 `(原因: fetch_failed)` 表达。禁止项: 不得渲染为「无竞品」/「未发现同 issue 竞品」。

### (2) 对本轮是否继续、verdict 与收敛判定的影响

- **本轮照常继续**: 探针是 advisory 副机制, 「不阻断」条款 = 不改 verdict 计算、不改收敛判定、不改轮次路由。连 `sibling_found` 都只是告警不是判决, `not_established` 更不阻断。Round 1 随后照常进入 Step 1 讨论组 spawn → Step 2 挑战组 → Step 3 全员 → Step 4 再审 → Step 5 drift check。
- **审计 verdict 不受影响**: PASS / PASS_WITH_WARNINGS / FAIL 由 Critical/Major/Minor 计数决定 (SOT 在 report-storage.md), 探针结果零输入。
- **收敛判定不受影响**: challenge 模式收敛 = 提案结论四元组集合无变化 (vs Round N-1) AND objections 全部 `resolved`; Round 1 本无前轮可比较, 且探针结构性不参与该判据。探针也不因此消耗或追加轮次。
- 唯一落点 = 报告 body 的 `- Sibling probe:` 行 + 聚合报告呈现; 对人的信号 = 远端 fetch 网络失败 (`error_kind=network`, 61.2s), 属环境/网络面而非本轨 spec 输入面。
- **后续轮**: Round 2 入口会**重新**跑探针 (每轮重跑、不复用缓存 —— 设计动机: 审计跨天时首轮结论会陈旧), 网络恢复即有机会直接得出 `sibling_found` 或 `no_sibling_found` (本轨 `own_keys` 完好, 只欠覆盖)。

### (3) 能否断言「没有同 issue 的竞品 Spec」

**不能。** 三层理由:

1. `not_established` 的字面语义就是「判定未成立」, 不是「不存在」—— 它与 `no_sibling_found` 是两个不同判定值。
2. 证据面为零: origin 的 fetch 腿失败, `scanned=0` / `refs_scanned=0` —— enforced 远端语料一个 proposal blob 都没进比较面,「没扫到」与「扫完没有」在本情形不可区分。
3. 契约明文 (execution-modes.md verdict 取值表): 消费方**不得**从 `hits == []` 推断结论 —— `hits` 为空在「扫完没有」与「没扫到 / 本轨无输入」上取值相同; SKILL.md (β): 零证据不当正证据。

可断言的上限仅是: 「本轮竞品扫描未能核实 (原因: fetch_failed)」, 把不确定性如实留在报告里。

---

## 2. 情形 B: exit 1, stdout 为空, stderr 是 Python traceback

源码映射 (只读推演): exit 三分中, 参数/仓库错 = 2、姊妹模块 import 失败 = 3、`run_probe` 内部异常 = 1 —— 后者正是 `main()` 的 `except Exception: traceback.print_exc(file=sys.stderr); return 1`, stdout 只在 `run_probe` 成功后才写, 故 stdout 为空与此完全吻合。即: 探针自身崩溃, 连判定面都没有产出。

### (1) `### Round 1` 记录中探针那一行的措辞

走 (β) 的 fail-closed 侧通道: `exit != 0` (且 stdout 为空、无法解析为 JSON —— 双重触发) ⇒ **一律按 `not_established` 处置**, 渲染同一档措辞。与情形 A 的差别在 `reason` 的来源: `reason` 的封闭枚举 (`no_enforced_remote | remote_unresolved | fetch_failed | cap_applied | own_token_absent`) 只存在于 stdout JSON 中; exit≠0 时 stdout 不保证 JSON (本情形为空), 消费方**没有结构化 reason 可读**, 只能把 fail-closed 触发形态的稳定事实 (exit code + stdout 形态) 填进原因栏, 不把 stderr traceback 原文贴进报告:

```markdown
### Round 1
- Agents: …
- Sibling probe: 未能核实 —— 本轮竞品扫描未取到完整证据 (原因: 探针自身失败 — exit 1, stdout 无 JSON)
- Conclusions: …
```

同样**禁止**渲染为「无竞品」。

### (2) 对本轮是否继续、verdict 与收敛判定的影响

与情形 A 完全同构:

- **本轮照常继续**: 同一条「不阻断」条款, 不改 verdict 计算、不改收敛判定、不改轮次路由; Round 1 的 Step 1–5 照常执行。
- **审计 verdict / 收敛判定零影响**: 判据集里没有探针的输入项; 探针行只落轮次记录与聚合报告。
- **后续轮**: Round 2 入口重跑探针, 本轮崩溃不污染后续轮 (每轮全新运行)。若崩溃是环境性/偶发的, 后续轮可自愈; 若持续复现, 信号是探针自身缺陷 (值得人工看 stderr traceback 定位), 但这超出 audit-engine 的机械消费义务 —— 消费面只欠下「未能核实」一行, 不做诊断分支。

### (3) 能否断言「没有同 issue 的竞品 Spec」

**不能, 且本情形证据面比 A 更空。** 情形 A 至少还携带探针的结构化运行面信息 (本轨 `own_keys` 完好、origin 默认分支 `master`、失败形态 `network`); 情形 B 连探针自身的判定都没产出 (stdout 无 JSON), 消费方对竞品状态的全部知识 = 「探针内部异常退出」。fail-closed 义务原文 (execution-modes.md / sibling_spec_probe.py docstring): exit≠0 或 stdout 非 JSON 或 `schema_version` 未知 ⇒ 一律按 `not_established` 处置 —— **never as "no sibling"**。可断言上限: 「本轮竞品扫描未能核实 (探针自身失败)」。

---

## 3. 两情形殊途同归与差异

| 维度 | 情形 A | 情形 B |
|---|---|---|
| 消费路径 | (α) 正门: exit 0 + 合法 JSON + schema 已知, 读一等字段 `verdict` | (β) fail-closed 侧门: exit≠0 + stdout 非 JSON, 兜底按 `not_established` 处置 |
| 渲染终点 | 「未能核实 —— … (原因: fetch_failed)」 | 「未能核实 —— … (原因: 探针自身失败 — exit 1, stdout 无 JSON)」 |
| reason 来源 | stdout 结构化字段 | 无结构化来源, 以 fail-closed 触发事实描述 |
| 本轮继续 / verdict / 收敛 | 三者均不受影响 (advisory 不阻断) | 同左 |
| 断言「无竞品」 | 禁止 (零证据不当正证据; hits==[] 不可推断) | 禁止 (never as "no sibling") |
| 对人的后续信号 | 网络层 fetch 失败, 可恢复面 | 探针内部异常, 需看 stderr traceback (人工诊断面) |

两情形在消费面**殊途同归**: 都必须渲染「未能核实」、都不得渲染「无竞品」、都不阻断本轮、都不改 verdict 与收敛判定。渲染「本轮已完整扫描, 未发现同 issue 竞品」的唯一合法前提是 stdout 给出一等字段 `verdict == "no_sibling_found"` (覆盖完整 + `own_keys` 非空 + `hits` 空) —— 两个假想情形均不满足。
