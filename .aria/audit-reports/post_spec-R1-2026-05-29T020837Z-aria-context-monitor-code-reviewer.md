---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-05-29T02:08:37.000Z
context: openspec/changes/aria-context-monitor/proposal.md
agents: [code-reviewer]
---

# post_spec R1 — code-reviewer — aria-context-monitor

审计视角: code-reviewer。审计 spec 的技术声明准确性、输出 JSON schema 内部一致性、deliverable 完整性/路径正确性、statusLine relay 注入方案的技术可行性 (对照真实 statusline 脚本 + transcript JSONL 实证)。**无代码 — 审 spec implementation-readiness**。

## 实证交叉验证 (verified against runtime artifacts)

以下 spike/proposal 声明我已对照真实文件验证 **属实**:

1. ✅ transcript path slug 推导: `pwd | sed 's#/#-#g'` → `-home-dev-Aria`, 真实路径 `~/.claude/projects/-home-dev-Aria/*.jsonl` 存在 (spike #5 验证项属实)。
2. ✅ transcript `usage` block 存在且含 `input_tokens / cache_creation_input_tokens / cache_read_input_tokens / output_tokens` (spike #3 属实)。
3. ✅ **`message.model` 丢 `[1m]` 后缀且 4-7/4-8 跳变** — 实测同一 transcript 内同时出现 `claude-opus-4-7` 和 `claude-opus-4-8` (无 `[1m]`)。这是 DEC 约束表第 2 行 "model→window 查表不可靠" 的**核心论据**, 实证完全成立。这是本 Spec 架构选择 (放弃 model→window 查表, 改 statusLine relay) 的最强支撑。
4. ✅ statusLine 脚本确实 `jq` 读 `.context_window.used_percentage` (line 40)、`.context_window.total_input_tokens` (57)、`.cost.total_cost_usd` (34)、`.rate_limits.*` (84/92)、`.model.display_name` (15)。证明 stdin 含 `context_window` + `cost` + `rate_limits` + `model` 顶层键 — relay 中继的字段基础**真实存在**。

---

## 审计结论

### [major] (S1) statusLine stdin schema 的一半字段未被生产脚本佐证 — 仅 spike 一次性 capture 单点证据 / category: 技术声明可验证性 / scope: proposal §核心机制 + DEC 约束表 + Tasks 1.1

proposal (L54-67) + DEC (L22) + spike (L53-70) 把整个 relay 架构建立在 statusLine stdin 含这些字段:
`context_window.context_window_size`、`remaining_percentage`、`exceeds_200k_tokens`、`transcript_path`、`model.id` (带 `[1m]`)。

但我 grep 真实 `~/.claude/statusline-command.sh` 发现: 生产脚本**只**消费 `used_percentage` / `total_input_tokens` / `total_output_tokens` / `cost.total_cost_usd` / `rate_limits` / `model.display_name` / `workspace.*`。它**从不引用** `context_window_size`、`remaining_percentage`、`exceeds_200k_tokens`、`transcript_path`、`model.id`。

后果: 这 5 个字段 (尤其是 spec "零推断主路径" 的命脉 `context_window_size` 和 `model.id` 带 `[1m]`) 的存在性**仅靠 spike 一次临时 capture** (spike L51 "已还原")，**无独立可复现证据**保留。生产脚本无法佐证, transcript 也没有 (transcript 恰恰丢 `[1m]`)。若 capture 当时 jq 路径笔误或 runtime 版本差异, 整个 "零推断主路径" 假设可能站不住。

**为何重要**: 这是 code-reviewer 视角下 spec 最大的 verifiability gap — 架构基石声明的证据是 ephemeral 的、已删除的、不可复现的。Tasks 1.1 ("实测固化 statusLine stdin schema + 记录字段契约") 确实意图补救, 但它作为**实施期任务**意味着: **如果 1.1 capture 发现 `context_window_size` 实际不存在, 主路径架构当场崩塌而 spec 已 Approved**。

**修复**: 把 schema 固化前置为 Phase A 验收门 (或 Tasks 1.1 标 BLOCKING + 失败回退条款)。最低限度: 在 proposal/spike 中明确标注 "L54-67 字段中, `context_window_size` / `model.id[1m]` / `transcript_path` / `remaining_percentage` / `exceeds_200k_tokens` 来自单次 capture, 生产 statusline 脚本未独立佐证, Tasks 1.1 必须先重新 capture 验证再实施 1.2-1.4; 若 `context_window_size` 缺失则 fallback window 推断链 (config/peak/200K) 升级为主路径"。

### [major] (S2) `used_percentage` 语义在 relay 路径 vs transcript fallback 路径**不一致**, 但输出 schema 用同一字段名无区分 / category: schema 内部一致性 / scope: proposal §输出结构 + Success Criteria 第1条 ("0 偏差")

两条数据路径算出的 `used_percentage` 语义不同:
- **relay 路径**: runtime `used_percentage` ≈ `total_input_tokens / context_window_size`。实测 spike 示例 673955/1M = 67.4% ≈ 67 ✅ 自洽 (即 used% 跟踪 *total_input*, 不含本-turn cache 细分)。
- **transcript fallback 路径**: spike L28-31 定义 proxy = `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`, 实测 628248 ≈ 62.8%。

这两个公式**计算的不是同一个量**。relay 用 runtime 预算口径 (total_input cumulative), transcript proxy 用 last-turn 的 input+cache 合计。在同一 session 它们会给出**不同百分比**, 但 proposal 输出 schema (L94-105) 把两者都塞进同一个 `used_percentage` 字段, 仅靠 `source` / `confidence` 区分来源, **不区分语义**。

**为何重要**: Success Criteria 第1条要求 relay 路径 "与状态栏显示一致, 0 偏差" — 可达成 (同一公式)。但第2条 transcript fallback 用**不同公式**, 消费方 (phase-b/c-developer 决策阈值, Tasks 1.8) 若用同一阈值 (如 "remaining<25% 暂停") 判两路径, 会因口径差产生新的系统性偏差 — 这恰恰是本 Spec 要消灭的 "22% 偏差" 问题的复刻。

**修复**: 在输出 schema 增加字段语义注释 (e.g. `usage_basis: "total_input_cumulative" | "last_turn_input_plus_cache"`), 或在 SKILL.md 明确两路径 used% 口径差 + 给 fallback 路径一个 transcript→total_input 的近似换算, 使两路径数值可比。Tasks 1.8 决策阈值文档必须区分 source 给阈值。

### [major] (S3) `window_source` 枚举值与 fallback 链描述用词不匹配 (enum mismatch) / category: schema 内部一致性 / scope: proposal §输出结构 L98 vs §数据来源 L79 + DEC L63

- 输出 schema (L98): `window_source: "runtime | config | empirical_peak | default"`
- 数据来源表 (L79) + DEC (L63) fallback 链: `relay-cached size > config window_tokens > observed-peak 下界 > 200K 默认`

映射不显式:
- `runtime` ↔ "relay-cached size" — **但 fallback 链第一档实际是两个来源混合**: (a) cache fresh 时 runtime size, (b) transcript fallback 但复用**之前 relay-cached 的 size** (DEC L79 "relay-cached size 复用 (见过即持久)")。这两种情况都映射到 `runtime` 吗? 若是, 则 `window_source=runtime` 但 `source=transcript_fallback` 的组合会出现 — schema 未声明这是合法组合, code-reviewer 无法判断这是 bug 还是 feature。
- `empirical_peak` ↔ "observed-peak 下界" — 用词不同但可对应。
- `default` ↔ "200K 默认" — 对应。
- "relay-cached size 复用" 这第 4 种来源 (transcript 路径但用历史 cache 的 size) **在枚举里没有专属值**, 被迫复用 `runtime` 或 `config`, 造成 provenance 失真。

**为何重要**: window_source 的全部价值是 provenance 可审计 (区分 runtime-truth vs 推断)。枚举漏掉 "复用历史 cache size" 这一档 = 审计时无法分辨 "本次 runtime 直读" vs "复用上次 relay 残留", 而后者可能跨 session 失效 (window 切换 model 时变)。

**修复**: 显式映射表写进 SKILL.md, 并补一个枚举值 (e.g. `cached_runtime` 表示 transcript 路径复用历史 relay size), 或在 schema 注释 `(source, window_source)` 的合法笛卡尔组合。

### [minor] (S4) cache schema 缺 `schema_version` 字段 (DEC 风险表自己提了但 proposal 输出/cache schema 没落实) / category: cache schema 完整性 / scope: DEC L77 vs proposal §输出结构 + DEC L46-48 cache 内容

DEC 风险缓解 (L77): "statusLine stdin schema 未来变动 → collector 防御式读取 + **schema_version 标注**"。但:
- DEC cache 内容描述 (L46-48) 列出 cache 字段时**无** `schema_version`。
- proposal §输出结构 (L94-105) 也无 `schema_version` (这是 skill 返回, 与 cache schema 不同, 但 cache schema 本身在 proposal 中根本未独立定义 — 见 S5)。

**修复**: cache 文件 schema 显式加 `schema_version` (DEC 自己的缓解措施); Tasks 1.2 落实。

### [minor] (S5) cache 文件 (`.aria/cache/context-window.json`) 的 schema 在 proposal 中无独立定义, 只在 DEC L46-48 散列 / category: deliverable 完整性 / scope: proposal §Key Deliverables L85 + Tasks 1.3

proposal 把 cache 文件列为 deliverable (L85) 并多处引用, 但**从未给出 cache 文件本身的字段 schema**。它只给了 "skill 返回" schema (L94-105) 和 statusLine stdin schema (L54-67)。cache schema 只在 DEC L46-48 以散文列出 (`{used_percentage, remaining_percentage, context_window_size, total_input/output_tokens, model_id, exceeds_200k_tokens, cost_usd, captured_at}`)。

问题: relay 行 (Tasks 1.3) 是写 cache 的唯一生产者, 其字段集必须精确定义。DEC 的散列与 proposal skill-output schema 字段集**不完全一致** (cache 有 `cost_usd`, skill-output 没有; skill-output 有 `window_source`/`staleness_seconds`/`confidence`/`source` 这些是 skill 派生的不该在 cache)。这种隐式区分对实施者不清晰。

**修复**: proposal 增补独立 "Cache 文件 schema" 小节 (含 `captured_at` 格式 ISO8601, `schema_version`), 明确 cache 字段 = relay 从 stdin 直接转存的子集, skill-output 字段 = cache + skill 派生 (source/window_source/staleness/confidence)。

### [minor] (S6) relay 注入方案需对照真实 statusline 脚本结构验证 "1 行幂等" 可行性 — 脚本末尾是 `printf` 退出, 注入点需谨慎 / category: relay 注入技术可行性 / scope: proposal L85-86 + Tasks 1.3

对照真实 `statusline-command.sh`: 它 `input=$(cat)` 在 line 2 一次性消费 stdin, 末尾 line 186 `printf '%b' "$parts"` 输出。Relay 行若要复用 `$input`, **必须注入在 line 2 之后** (stdin 已被 `cat` 吃掉, 之后无法再读)。proposal "1 行 relay" (L85) 技术上可行 (e.g. `echo "$input" | jq '{...}' > .aria/cache/context-window.json` 注入在 `input=$(cat)` 之后), 但:
- spec 未说明注入**锚点** (必须在 `input=$(cat)` 之后、任意输出之前)。盲目 append 到文件末尾 (最直觉的幂等做法) 会**失败** — 因为彼时若 relay 行自己再 `cat` 则 stdin 已空。
- proposal L86 "依赖 jq (硬依赖)" 与真实脚本一致 (脚本已重度用 jq) ✅, 这点正确。
- 幂等检测 (Success Criteria L149) 需 grep sentinel 注释标记; spec 未指定标记字符串。

**为何重要**: 这是 code-reviewer 对 "注入技术是否 sound" 的直接问题。结论: **可行但 spec 欠精确**, 注入锚点假设 ("append 末尾") 若实施者想当然会引入 silent bug (relay 行读空 stdin → 写空 cache)。

**修复**: Tasks 1.3 明确: (a) 注入锚点 = `input=$(cat)` 行之后立即插入; (b) sentinel 标记 (e.g. `# aria-context-monitor relay (idempotent)`) 供幂等 grep; (c) relay 行复用已有 `$input` 变量, 不重新 `cat`。

### [minor] (S7) 引用的 "secret-guard dual-install 模式" 实际目录名是 `aria-doctor` 下的 check + secret-guard hook, deliverable 路径需核对 / category: deliverable 路径正确性 / scope: proposal L86 "类 secret-guard dual-install 模式"

proposal L86 + DEC L62 类比 "secret-guard dual-install" 作为 setup_relay.sh 的模式范本。实测: 该模式的 detection 脚本在 `aria/skills/aria-doctor/scripts/check_secret_guard_install.sh` (输出单行 compact JSON `{"state":...,"sub_flags":...}`, 3+ 状态机)。proposal Tasks 1.5 要 aria-doctor "3 态 relay install-state" — 与 secret-guard 的 state-machine 输出契约一致 ✅。这是**正面**: 类比有真实先例可循。

唯一 minor: proposal §Key Deliverables (L83-88) 把 "aria-doctor 集成" 列为 deliverable 但**未给具体脚本路径** (应是 `aria/skills/aria-doctor/scripts/check_context_relay_install.sh` 镜像 secret-guard 命名)。建议补全路径 + 配套 test 路径 (secret-guard 有 `tests/check_secret_guard_install.test.sh`, 本 Spec 应对称提供)。

---

## Verdict

**PASS_WITH_WARNINGS** (0 critical + 6 major/minor; 其中 3 major S1/S2/S3 + 3 minor S4/S5/S6 + 1 正面注记 S7)

> 注: 按 verdict 规则 (FAIL = ≥1 critical), 本审无 critical (实证核心声明均验证属实, 架构方向 sound)。但 3 个 major 涉及 schema 一致性与证据可复现性, ship 前应 close。

| 严重度 | 数量 | 条目 |
|--------|------|------|
| critical | 0 | — |
| major | 3 | S1 (schema 证据不可复现), S2 (used_percentage 双路径语义不一致), S3 (window_source enum mismatch) |
| minor | 3 | S4 (cache 缺 schema_version), S5 (cache schema 未独立定义), S6 (relay 注入锚点欠精确) |
| 正面 | 1 | S7 (secret-guard 类比有真实先例; jq 硬依赖与真实脚本一致) |

**Implementation-readiness 评估**: 架构方向技术 sound (model→window 不可靠 + statusLine 含富 stdin 的核心实证均验证属实, transcript fallback 路径切实可行)。但 spec 在 **schema 精确度** 上欠成熟: cache schema 未独立定义 (S5)、used% 双路径语义混用 (S2)、window_source 枚举漏档 (S3)、关键字段证据 ephemeral (S1)。这些是实施期高概率触发 silent bug 的来源, 建议 R1 内修订后再进 Phase B。

## 轮次记录

- **R1 (code-reviewer)**: 6 findings (3 major + 3 minor) + 1 正面。Verdict PASS_WITH_WARNINGS。核心实证 (transcript model 丢[1m]/4-7+4-8 跳变、usage block、slug 推导、statusline 脚本读 context_window) 已对照 runtime artifact 验证属实。主要风险集中在 schema 一致性 + 单点 capture 证据不可复现。建议 converged=null (待 orchestrator 综合多 agent + R2)。
