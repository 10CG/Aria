---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-05-29T02:09:43.000Z
context: openspec/changes/aria-context-monitor/proposal.md
agents: [qa-engineer]
---

# QA Engineer Audit — aria-context-monitor post_spec R1

**Spec**: `openspec/changes/aria-context-monitor/proposal.md`
**Decision basis**: `.aria/decisions/2026-05-29-context-monitor-architecture.md` (DEC-20260529-001)
**Spike evidence**: `.aria/notes/2026-05-29-context-monitor-spike.md`
**Source issue**: Forgejo Aria #104

---

## 审计结论

### [critical] C1 — staleness threshold 未定义，Success Criteria 不可证伪

**Category**: Falsifiability | **Scope**: Success Criteria + Task 1.6

Spec "Success Criteria" 中无任何 staleness 阈值数值。`staleness_seconds` 字段出现在输出 schema (§What 输出结构)，Task 1.6 提及"staleness 判定"，但 Spec 全文无明确规定"超过 N 秒视为 stale"。

问题：
1. 不存在可测的 acceptance criterion — 测试者无法写断言 `assert staleness_seconds < THRESHOLD`，因为阈值未定义。
2. "cache 陈旧" 在 Task 1.7 中列为 fallback 路径单测目标，但缺少驱动该测试的契约值，测试设计本身就无法确定。
3. 在 3 档 fallback 逻辑中，"何时 cache 被判定为 stale 从而降级到 transcript fallback"是一个关键分支条件，其缺失直接导致 fallback 路径行为不确定。

**引用**: feedback_falsifiable_evidence_for_binary_acceptance — "Acceptance bool 必 mandate 可验 metric,否则 AI 代填 true 无法 audit"

**修复方向**: 在 Success Criteria 中添加"relay cache 新鲜度: `staleness_seconds` 超过 X 秒(建议 300s 或 1 个 statusLine 渲染周期)时 skill 返回 `confidence=estimate` 并降级"，并在 Task 1.6 中固化该数值为可测常量。

---

### [critical] C2 — relay 注入幂等性：验证断言缺失，"幂等"无可测定义

**Category**: Testability / Edge Case | **Scope**: Task 1.3 + Success Criteria

Success Criteria 中写"setup_relay.sh 幂等 (重复运行不重复注入)"，但：

1. **无定义"注入"的检测边界** — 若用户 statusLine 脚本已含功能等效的 relay 行但文本不完全匹配，setup_relay.sh 会判定为"未注入"并重复写入，还是正确识别？Spec 未说明检测粒度（精确字符串匹配 vs 功能检测）。
2. **无 idempotency 测试场景** — Task 1.7 列出"无 statusLine / cache 陈旧 / transcript-only window 推断"，但没有"重复运行 setup_relay.sh 2+ 次"的测试场景，这是 relay 机制最高频的现实失败模式。
3. **用户现有 statusLine 内有相似逻辑的情况未覆盖** — Spec 提到"保留用户现有 statusLine display 逻辑不动"（§Key Deliverables），但未定义当用户已有自己写的 context bar 逻辑时，relay 行与之是否冲突或重复写 JSON。这是一个确定性的边缘场景，影响 Impact 表所列"低风险"评估的准确性。

**修复方向**: Task 1.7 加入 `setup_relay.sh` 幂等性测试场景 (run-twice / pre-existing-relay-line / user-has-custom-context-bar); Success Criteria 明确幂等检测算法（字符串锚点匹配 vs marker 注释）。

---

### [major] M1 — window_source 标注语义不完整：transcript fallback 下 4 个 source 值未全覆盖

**Category**: Specification Completeness | **Scope**: §What 输出结构 + Task 1.6

输出 schema 中 `window_source` 枚举为 `"runtime | config | empirical_peak | default"`，对应 3 档 fallback 中第 3 档的 4 层 window 推断：
- relay-cached size → `runtime`
- config `window_tokens` → `config`
- observed-peak 反推 → `empirical_peak`
- 200K 默认 → `default`

问题：
1. **`source=relay_cache` 时 `window_source` 应始终为 `runtime`**，但这个约束未在 Spec 中明确，实施者可能对 relay cache 命中时仍写入错误 window_source 值（比如 config）。
2. **`source=transcript_fallback` 时 window_source 4 级降级顺序有语义歧义** — "relay-cached size 复用" 在没有新的 statusLine 渲染时使用已过期 cache 的 `context_window_size` 字段（而 `used_percentage` 已过期），Task 1.6 描述"relay-cached size 复用逻辑"但未说明何时该 size 可信（cached size 是 session 内不变量，而 % 会变），此混用逻辑在 Spec 中是隐含的，实施中容易错误地同时复用 `used_percentage`。
3. **mislabeling 风险** — 实施者可能在 transcript fallback 路径下把 empirical_peak 推断的结果标注为 `config` 或把 config 值标注为 `runtime`，没有 Spec 级约束阻止这种 mislabeling。

**引用**: feedback_window_source mislabeling 是审计要求明确列出的测试维度。

**修复方向**: Task 1.6 或 §What 中明确 window_source 与 source 的联合约束表（二维 source x window_source 合法值矩阵），同时在 Task 1.7 测试场景中加入 window_source 标注验证。

---

### [major] M2 — Rule #6 任务 (Task 1.9) 描述不足以指导实施者决策

**Category**: Process Compliance / Rule #6 | **Scope**: Task 1.9

Task 1.9: "Rule #6: skill benchmark 或 structural substitute (deterministic data-relay skill)"

问题：
1. **"structural substitute" 未定义** — Rule #6 (CLAUDE.md) 明确"Skill 基准测试必须使用 `/skill-creator`"，但 Task 1.9 引入"structural substitute"作为备选路径而未说明何种条件触发该路径、substitute 的最低证明要求是什么。
2. **"deterministic data-relay skill"的论证是推断而非核定** — 这是 Spec 起草者的分类，但未经过 Rule #6 要求的 benchmark 对比验证。一个"确定性中继"是否真的可以豁免 AB benchmark 本身需要 Spec 中有明确的 skip 理由和 owner sign-off，而不是一个括号备注。
3. **feedback_level2_patch_no_benchmark 适用条件检查** — 该反馈记录的豁免适用于"Level 2 patch 不动 Skill 逻辑"，但本 Spec 新增一个完整 user-facing skill，Task 1.9 至少需要说明"为何本 case 满足豁免条件"。

**修复方向**: Task 1.9 明确以下其一：(a) 使用 `/skill-creator` 全流程 benchmark；(b) 明确 structural substitute 的最低要求（例如：静态 input/output 对覆盖 3 档 fallback + owner sign-off + 豁免理由记录）。不可以"或"字留给实施者自行判断。

---

### [major] M3 — jq 硬依赖的 doctor 检测范围与跨平台测试策略缺口

**Category**: Cross-platform / Edge Case | **Scope**: §Key Deliverables + Success Criteria

Spec 在 §Key Deliverables 中明确"jq (硬依赖, doctor 检测)"，但：

1. **jq 缺失的 graceful degradation 路径未定义** — `jq` 不存在时 `setup_relay.sh` 的行为是 hard exit？是 fallback 到无 relay？是提示 install？Spec 未说明，这直接影响 transcript fallback 路径的触发条件。
2. **doctor 检测的输出格式未对齐现有 aria-doctor 契约** — 现有 aria-doctor 输出结构基于 `{"state": "<primary>", "sub_flags": [...], "advisory": "..."}` 的 JSON schema（SKILL.md §Functions）。Task 1.5 中"3 态 relay install-state"检测的输出格式未说明是扩展现有 JSON schema、新增独立检测函数、还是输出纯文本。实施者可能产生与现有 aria-doctor 契约不一致的输出。
3. **Success Criteria 中"aria-doctor 正确报告 3 态"无伪造抗性测试** — 3 态 (`installed / statusline-no-relay / no-statusline`) 必须通过实际文件系统状态驱动，而非 mock，但 Task 1.5/1.7 未要求集成级别的 doctor 测试。

**修复方向**: §Key Deliverables 中补充 jq 缺失时的降级行为声明；Task 1.5 明确 aria-doctor 集成模式（扩展现有脚本 vs 新脚本）及输出 schema 继承关系。

---

### [minor] m1 — statusLine stdin schema 版本漂移的防御措施不可测

**Category**: Resilience / Schema Stability | **Scope**: Task 1.1 + DEC-20260529-001 §风险与缓解

决策文档提到"collector 防御式读取 + schema_version 标注"作为应对 statusLine stdin schema 未来变动的缓解措施，但：

1. **`schema_version` 在输出结构中不存在** — 输出 JSON schema (§What) 无 `schema_version` 字段，collector 内部标注的版本不会向消费者暴露，无法从 skill 输出反向验证 collector 使用的 schema 版本。
2. **"防御式读取"无具体测试场景** — Task 1.1 只要求"capture 一次 + 记录字段契约"，没有要求测试"某字段缺失时的降级行为"，而 Spike 已实测 `fast_mode`、`rate_limits` 等字段有出现但格式未完全固化。

**修复方向**: Task 1.7 加入"statusLine JSON 缺少 `context_window.used_percentage` 或 `context_window.context_window_size` 时的降级行为"测试场景。

---

### [minor] m2 — "#104 场景复现"Success Criteria 缺乏操作性

**Category**: Falsifiability | **Scope**: Success Criteria

"复现 #104 场景: AI 调 skill 得准确 % (消除 22% 凭感觉偏差)" — 这个 criterion 无法作为 acceptance test 执行，原因：

1. "AI 调 skill 得准确 %"无法在 CI 中机器验证，因为"AI 的感觉偏差"不是可测量输出。
2. 实际可测的替代：`skill_used_percentage - statusline_display_percentage == 0`（对 relay_cache 路径）。Spec 也写了"与状态栏显示一致, 0 偏差"，但这仅在 relay_cache 命中路径下成立，且 statusline_display_percentage 本身无法机器读取用于对比。

**修复方向**: 将该 criterion 改写为可执行的测试断言，例如：relay_cache 路径下 skill 输出的 `used_percentage` 与 relay 写入时 statusLine stdin JSON 的 `context_window.used_percentage` 差值为 0（由 token_telemetry.py 单测验证）。

---

### [minor] m3 — 消费集成文档（Task 1.8）的决策阈值建议无依据

**Category**: Specification Completeness | **Scope**: Task 1.8

Task 1.8: "消费集成文档: phase-b/c-developer 调用点 + 决策阈值建议"

Spec §Out of Scope 明确"'暂停 vs 继续'决策仍由 AI/phase skill 判断，不自动中断"，但 Task 1.8 中的"决策阈值建议"若不经实证就写入 phase-b/c-developer 文档，会形成与 Spec #104 实证数据（22% 偏差、55% 实际余量触发不必要暂停）存在潜在矛盾的建议值。例如，若建议"剩余 < 30% 时考虑暂停"，而实证场景中 45% 剩余量即被 AI 误判，说明阈值选择需要实测依据。

**修复方向**: Task 1.8 明确"决策阈值建议"为初始建议值（附来源依据），或显式标注为"待运营数据后校准"，避免文档被当作确定性规范。

---

## Verdict

| 严重级 | 数量 | 项目 |
|--------|------|------|
| [critical] | 2 | C1 (staleness threshold 未定义) / C2 (relay 幂等性无可测定义) |
| [major] | 3 | M1 (window_source 语义) / M2 (Rule #6 不足) / M3 (jq 依赖 + doctor 契约) |
| [minor] | 3 | m1 (schema 版本漂移) / m2 (#104 复现 criterion) / m3 (阈值无依据) |

**FAIL** — 2 critical findings。

**Critical 判定依据**:
- C1: staleness threshold 缺失导致 Task 1.6 + Task 1.7 fallback 测试无法执行（feedback_falsifiable_evidence_for_binary_acceptance 直接适用）
- C2: relay 幂等性 Success Criterion 无操作性定义 + 最高频失败模式未纳入 Task 1.7 测试范围

两个 Critical 均属于"测试策略无法执行"类型，不是实施层面问题，须在 Spec 层修复后再进入 Phase B。

---

## 轮次记录

### R1 (本轮) — 2026-05-29T02:09:43Z

**审计范围**: 全文 (proposal.md + DEC-20260529-001 + spike note)
**方法**: QA lens — falsifiability / fallback testability / edge case coverage / Rule #6 adequacy / mislabeling risk
**结论**: FAIL — 2C + 3M + 3m

**关键观察**:
1. Spec 架构选择 (statusLine relay 为主路径 + transcript fallback) 技术上合理，spike 验证充分
2. 3 档 fallback 设计有依据，但 fallback 触发条件 (staleness threshold) 是整个体系的运行时契约核心，缺失属于 Spec 级漏洞而非实施细节
3. Rule #6 的"structural substitute"路径在现有 Aria 规范中无先例，须澄清或 close with owner sign-off
4. Task 1.7 测试矩阵不完整：覆盖了 3 档 fallback 的存在性，但缺少 relay 幂等性、window_source 正确性、statusLine JSON 字段缺失 3 个测试维度

**下一步**: 修复 C1/C2 后可重新审计；M1-M3 建议在同一修订中一并解决以避免 R3。
