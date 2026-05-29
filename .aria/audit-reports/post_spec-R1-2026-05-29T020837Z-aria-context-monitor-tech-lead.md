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
agents: [tech-lead]
---

# Post-Spec Audit (R1) — aria-context-monitor — tech-lead lens

## 审计结论

### Decisions (架构判断 — 与 DEC-20260529-001 一致性)

- **[ok] 双 Spec 解耦 + 共享 collector 边界设计正确** [category: architecture / scope: cross-issue #104↔#18]
  proposal L12/L48/L158 与 DEC-20260529-001 L30/L70 一致: #104 (窄 feature) 与 #18 (6-skill 重构) 拆为 2 独立 Spec, 仅共享数据层 `lib/token_telemetry.py`。决策记录明确否决"合并单 Spec" (DEC L29) 和"collector 算 %" (DEC L31, Q2=a 单一职责)。proposal L151 success criterion "raw counts 解析独立于 window%" 正确落实了"collector 不碰 window 推断"的职责切分。这是干净的边界 — collector 只做 parse, window% 由消费方计算。**架构主干站得住**。

- **[ok] statusLine relay 为主路径 + transcript fallback 的分层正确** [category: architecture / scope: data-source]
  spike (note L47-86) 实地 capture 证实 statusLine stdin 含 `context_window_size` + `used_percentage` + `model.id`(带 [1m])。我已独立验证: 当前 `/home/dev/.claude/statusline-command.sh` L43 已在生产消费 `.context_window.used_percentage`，schema 是真实的、runtime 直供的。"从'如何推断 window'退化为纯中继"(proposal L69) 是正确的问题重构。

### Issues

- **[major] 共享 collector 落点 `state-scanner/scripts/lib/` 违反现有目录约定且制造跨-skill 耦合** [category: architecture / scope: aria/skills/state-scanner/scripts/lib/token_telemetry.py]
  proposal L84/L117/L133 把共享 collector 放在 `aria/skills/state-scanner/scripts/lib/token_telemetry.py`。两个问题:
  1. **`lib/` 目录不存在且非现有约定** — 实测 `state-scanner/scripts/` 下用的是 `collectors/`(含 `_common.py` 共享代码)、`renderers/`、`writers/`，全仓 `grep "scripts/lib/"` 零命中。新建 `lib/` 是凭空引入的第四种组织模式。
  2. **跨-skill ownership 倒置** — 这个 collector 的两个消费方是 `aria-context-monitor` (本 Spec, #104) 和 `ai-native-estimator` (#18)，**都不是 state-scanner**。把共享 lib 塞进 state-scanner 的 scripts 子树，意味着两个无关 skill 在 import 路径上硬依赖 state-scanner 的内部目录结构。这是 #57 式数据层重复想避免的反面 — 但解法选错了宿主。建议落点应是 skill-neutral 的共享位置 (如本 Spec 自己的 `aria-context-monitor/scripts/lib/`，由 #18 跨-skill import；或一个独立的 telemetry skill)，而不是寄生在 state-scanner 下。proposal L48 文字说"提取共享 collector"，但 L84 落点与"共享"语义矛盾 (放进了一个具体消费者都不是的 skill)。**这是会固化为技术债的边界错误，应在 Phase A.2 修正落点再进 task-planner。**

- **[major] statusLine relay 注入的 stdin 重入语义未在 Spec 中约束 — 有静默破坏用户状态栏的实质风险** [category: cross-system / scope: setup_relay.sh + 用户 statusLine command]
  proposal L11/L85/L118 称 relay 注入为"1 行 / 幂等 / 低风险 / 不修改 statusLine 显示行为"。但实测用户脚本首行是 `input=$(cat)` —— **stdin 是一次性流，`cat` 已耗尽**。relay 行若也想读 stdin (`echo "$input" | jq ... > cache` 或独立 `cat`)，必须复用已捕获的 `$input` 变量，且**必须注入在 `input=$(cat)` 之后**而非任意"1 行"。proposal/DEC 把它描述为位置无关的"加 1 行"，低估了注入语义:
  - 若注入到 `input=$(cat)` 之前 → relay 吃掉 stdin → 用户原状态栏 `input` 为空 → 状态栏静默失效。
  - 若用户脚本不用 `input=$(cat)` 模式 (例如逐字段 `jq` 直读 stdin 多次) → 注入点判定更复杂。
  这与 risk class "不修改 statusLine 显示行为" (L11/L126) 的声明冲突 —— 注入错位会直接破坏显示。Spec 必须把 setup_relay.sh 的**注入点检测算法** (定位 stdin 捕获语句、复用其变量、AST/正则识别多种 statusLine 写法) 提升为显式 task + 单测，而非藏在 L134 "幂等注入"一句里。Task 1.3 当前粒度不足以覆盖此 cross-system 失败面。

- **[minor] window_source 优先级链在 proposal 内部表述不自洽** [category: spec-consistency / scope: proposal L79 vs L98 vs DEC L63]
  proposal L79 fallback 链: `relay-cached size > config window_tokens > observed-peak 下界 > 200K`。L98 输出字段 `window_source: "runtime | config | empirical_peak | default"`。两处枚举可对齐，但 L79 第一档写"relay-cached size"而 L98 写"runtime" —— 在 transcript fallback 路径里 window 来自**上一次 relay 写的 cache**，严格说不是本次 runtime 直供，命名应统一 (建议 `cached_runtime` 区别于主路径 `runtime`)。否则消费方无法从 `window_source` 区分"本次 relay fresh"与"复用历史 cache size"，而后者的 staleness 语义不同。

- **[minor] config schema 新增字段 (`context_monitor.window_tokens`) 未在 config-loader / DEFAULTS.json 落 task** [category: completeness / scope: config-loader]
  proposal L79 fallback 档 3 引用 config `window_tokens`，但实测 config-loader 与 `.aria/config.json` 均无此 key，Tasks (L132-140) 无"在 config-loader DEFAULTS.json 注册新 key"的条目。Aria 约定新配置项须经 config-loader 注册 (否则消费方读取无默认、无校验)。应补 task。

### Risks

- **[major] statusLine stdin schema 是未文档化的 Claude Code 内部契约 — 跨 runtime 版本脆弱** [category: strategic / scope: runtime-dependency]
  整个主路径建立在 statusLine stdin JSON 的 `.context_window.{context_window_size,used_percentage}` 字段上。这是 Claude Code harness 的**内部、未承诺稳定**的 schema —— 非公开 API，可随 CC 版本静默改名/改结构。DEC L77 缓解措施"collector 防御式读取 + schema_version 标注 + transcript fallback 兜底"方向对，但 proposal **没有把它落成硬约束**: Task 1.1 ("实测固化 schema") 只 capture 一次记录契约，**缺少运行时 schema-drift 检测 + 自动降级到 transcript 的逻辑**。一旦 CC 改字段名，relay 行会静默写出缺字段的 cache，skill 读到 `null` 却仍标 `confidence=high`（因为 source=relay_cache），给 AI 错误的高置信坏数据 —— 这比 fallback 到 estimate 更危险。**建议 (R1 fix)**: Task 增加"relay cache 字段完整性校验 → 字段缺失时 source 降级 unavailable/transcript，confidence 不得为 high"。这是 strategic risk 因为它决定了 feature 在 CC 升级后的存活率，且静默坏数据违反 #104 的核心价值 (消除凭感觉)。

- **[major] staleness 阈值缺失 — relay cache 陈旧时的 confidence 判定无 Spec 定义** [category: timing / scope: proposal L103-104, L137]
  proposal 输出含 `staleness_seconds` (L103) 且 Task 1.6 提"staleness 判定"，但**没有定义陈旧阈值与超阈后的行为**。spike note L21 实测 transcript "1 turn stale"；relay cache 的新鲜度取决于 statusLine 渲染频率 (用户不交互时不渲染 → cache 可任意陈旧)。关键时序问题: AI 在一个长 Bash 执行后调 skill 决策"暂停 vs 继续"，此时 statusLine 可能几分钟未渲染，cache 反映的是**几个 turn 前**的占用，而决策最需要的恰是"刚消耗了大量 token 之后"的实时值。proposal 没说明: 超过 N 秒/N turns 的 cache 是否仍报 `source=relay_cache confidence=high`？这直接关系到 #104 实证场景 (L148, 消除 22% 偏差) 是否真被解决 —— 若 cache 陈旧仍标 high，会复现"高置信但失准"的原始病。**建议**: Spec 须定义 staleness 阈值 + 超阈后 confidence 降级 (或交叉校验 transcript last-turn 修正)。

- **[minor] "0 偏差"success criterion 可证伪性不足** [category: acceptance / scope: proposal L146]
  L146 "used_percentage 与状态栏显示一致, 0 偏差"是同义反复 —— relay cache 与状态栏读的是同一 stdin JSON，必然一致。真正要验的是"skill 报的 % 与 AI 决策时刻的真实 context 占用一致"。建议 acceptance 改为可证伪的时序断言 (如: 在已知消耗 X token 的操作后调 skill，报告值与 transcript last-turn 重算值偏差 < 阈值)，呼应 memory `feedback_falsifiable_evidence_for_binary_acceptance`。

### Level 分类与 Rule #6 判断

- **[ok] Level 2 (Minimal, proposal-only) 分类正确** [category: scope-boundary]
  变更 = 1 新 skill + 1 collector lib + 1 relay 行 + doctor 集成 + 文档，单 cycle ~3-4h，无 API break、无跨多 service、additive。符合 Level 2 (vs Level 3 须 tasks.md)。proposal L3 自带 Tasks 区块 (L130-140) 已足够，无需独立 tasks.md。**分类站得住。**

- **[ok] Rule #6 (benchmark) 处理得当** [category: process]
  Task 1.9 提出"skill benchmark 或 structural substitute (deterministic data-relay skill)"。对一个确定性 data-relay skill (输入 stdin JSON → 输出结构化 occupancy，无 LLM 判断面)，structural/smoke substitute 是合理的 (呼应 memory `feedback_smoke_vs_full_ab_benchmark` / `feedback_python_script_importlib_smoke`)。但建议 R1 明确: 若 skill 的 description 触发面/AI 消费决策面 (L88/L139 phase-b/c 调用点) 引入 LLM 判断，则 description-triggering 部分仍需 AB。当前 1.9 措辞已留口子，可接受。

## Verdict

**PASS_WITH_WARNINGS**

- critical: 0
- major: 4
  - [issue] 共享 collector 落点违反目录约定 + 跨-skill 耦合倒置
  - [issue] statusLine relay stdin 重入语义未约束 (有破坏用户状态栏风险)
  - [risk] statusLine stdin schema runtime-dependency 脆弱 + 静默坏数据未防御
  - [risk] staleness 阈值缺失 (陈旧 cache 仍报 high confidence 复现原始病)
- minor: 4
  - window_source 命名不自洽 (L79 vs L98)
  - config schema 新 key 未落 config-loader task
  - "0 偏差" acceptance 同义反复 / 可证伪性不足
  - (Rule #6 description-trigger AB 口子, 建议性)

架构主干 (双 Spec 解耦 + 共享 collector + relay 主路径/transcript fallback) 经 spike 实证、与 DEC-20260529-001 一致，可继续。但 4 个 major 中有 2 个 (collector 落点、relay 注入语义) 是会固化为技术债/用户可见破坏的边界设计问题，2 个 (schema 脆弱、staleness) 是决定 feature 真实价值与存活率的时序/strategic risk —— 均应在进入 task-planner 前于本 Spec 修正，不宜降级为实施期发现。

## 轮次记录

- **R1 (tech-lead, 2026-05-29T02:08:37Z)**: 首轮。读 proposal + DEC-20260529-001 + spike note 三件套，并独立验证生产 `statusline-command.sh` 实证 stdin schema 真实性、`state-scanner/scripts/` 实际目录约定、config-loader 无 `context_monitor` key。发现 0 critical / 4 major / 4 minor。verdict = PASS_WITH_WARNINGS。converged=null (待其他 agent R1 结论 + 是否进 R2)。
