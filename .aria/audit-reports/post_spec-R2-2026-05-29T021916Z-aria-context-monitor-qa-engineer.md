---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: true
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-05-29T02:19:16.000Z
context: openspec/changes/aria-context-monitor/proposal.md
agents: [qa-engineer]
---

# QA Engineer Audit — aria-context-monitor post_spec R2 (稳定性/验证轮)

**Spec**: `openspec/changes/aria-context-monitor/proposal.md` (Rev1, post R1 修订)
**R1 报告**: `.aria/audit-reports/post_spec-R1-2026-05-29T020837Z-aria-context-monitor-qa-engineer.md`
**Decision basis**: `.aria/decisions/2026-05-29-context-monitor-architecture.md` (DEC-20260529-001)
**审计方法**: 逐条验证 R1 findings 闭合状态 + 扫描 Rev1 新增内容引入的新 defect

---

## 审计结论

### R1 Finding 闭合状态表

| R1 ID | 级别 | 描述 | Rev1 fix 方案 | R2 状态 | 证据 |
|-------|------|------|--------------|---------|------|
| C1 | critical | staleness 阈值未定义 | §Staleness 契约表 + Success Criteria 行 + Task 1.6 | **CLOSED** | 见 C1 闭合验证 |
| C2 | critical | relay 幂等无操作性定义 | §Relay 注入语义 marker-注释锚点 + Task 1.7 三场景 | **CLOSED** | 见 C2 闭合验证 |
| M1 | major | window_source 枚举不完整 | §window_source 解析链 + relay_cache 恒=runtime 约束 + `cached_size_reuse` 值 | **CLOSED** | 见 M1 闭合验证 |
| M2 | major | Rule #6 Task 1.9 描述不足 | Task 1.9 改为 deterministic structural substitute + fixture 路径 + 豁免路径明确 | **CLOSED** | 见 M2 闭合验证 |
| M3 | major | jq 硬依赖 doctor 检测范围 + 跨平台 | jq 硬依赖 aria-doctor 检测 + 缺失 graceful degradation | **CLOSED** | 见 M3 闭合验证 |
| m1 | minor | schema_version 防御措施不可测 | 输出 schema 加 `schema_version` 字段 + Task 1.7 加 corrupt-cache 场景 | **CLOSED** | schema_version 出现在输出 JSON |
| m2 | minor | #104 复现 criterion 不可执行 | 调整为 relay 路径 0 偏差可执行 criterion | **CLOSED** | Success Criteria 中"与状态栏显示 0 偏差"已有定义 |
| m3 | minor | 阈值建议无依据 | Task 1.8 + 成功准则中 e.g. used%>85 作建议性参考 | **CLOSED** | 已标注为建议值，非决定性规范 |

---

### C1 闭合验证 — CLOSED (实质性修复)

**R1 问题**: staleness threshold 未定义，导致 Task 1.6/1.7 fallback 测试无法执行，Success Criteria 不可证伪。

**Rev1 修复内容**:

1. **§Staleness 契约**（§What 中新增独立小节）明确给出三元定义：
   - 默认值 `300s`（具体数值，可测）
   - Config key `context_monitor.staleness_threshold_seconds`（可覆盖，命名明确）
   - 超过阈值行为: `confidence=estimate` + fallback 降级（行为语义定义完整）

2. **Success Criteria** 新增两条可证伪 criterion：
   - "cache staleness > 300s: skill 降级 `confidence=estimate`, 不再信任 relay used_percentage" — 明确数值，可写断言
   - "statusLine 已配 + fresh (staleness≤300s): skill 返回 `source=relay_cache` + `confidence=high`" — 正向路径也已定义

3. **Task 1.6** 明确"固化 staleness 阈值常量 (300s, config `context_monitor.staleness_threshold_seconds` 可覆盖)"——常量固化任务存在。

4. **Task 1.7** 包含"cache 陈旧 (>300s)" 场景，与 C1 中"阈值缺失导致测试无法设计"问题直接对应。

**闭合判定**: 实质性修复。值 `300s`、config key、超阈值行为、两条可证伪 Success Criteria、Task 常量固化——五项均到位，不是文字润色。

---

### C2 闭合验证 — CLOSED (实质性修复)

**R1 问题**: relay 幂等性无可测的操作性定义；Task 1.7 缺少 run-twice / pre-existing-relay / user-custom-bar 三场景；检测边界未定义（字符串匹配 vs 功能检测）。

**Rev1 修复内容**:

1. **§Relay 注入语义** 新增 marker-注释锚点定义：
   - 具体 marker 字面值: `# >>> aria-context-monitor relay >>>` / `# <<< aria-context-monitor relay <<<`
   - 检测算法语义明确: "检测此 marker 判定'已注入'（非脆弱字符串匹配）"——区分了字符串匹配与 marker 语义检测，回应了 R1 提出的"检测粒度未说明"。

2. **Task 1.7** 明确列入三个场景（Rev1 changelog 中以加粗体标出新增）：
   - `setup_relay run-twice 幂等`
   - `pre-existing relay marker`
   - `user 已有 custom context bar`

3. **Success Criteria** 新增三条对应 criterion：
   - "setup_relay.sh 幂等: run-twice 不重复注入 (marker 检测); pre-existing relay marker 识别正确; user 已有 custom context bar 不冲突"

4. **R1-relay-stdin fix** 也同步补充了注入位置约束（`input=$(cat)` 之后）和 `$input` 变量复用约束，消除了位置敏感性的歧义。

**闭合判定**: 实质性修复。marker 锚点字面值已定、检测语义已区分（标记检测 vs 字符串匹配）、三个 R1 要求的测试场景全部进入 Task 1.7 和 Success Criteria。

---

### M1 闭合验证 — CLOSED

**R1 问题**: window_source 枚举值不完整（缺少 `cached_size_reuse`）；relay_cache 命中时 window_source 应恒 = `runtime` 但约束未声明；source × window_source 联合约束无 Spec 级定义。

**Rev1 修复内容**:

1. **§window_source 解析链** 独立列出（Rev1 新增节）：
   - relay_cache 命中 → `window_source 恒 = "runtime"（约束: 不得标其他值）`——约束明确，带括号强调。
   - transcript fallback 的 4 档枚举完整：`cached_size_reuse` / `config` / `empirical_peak` / `default`，与 DEC 4-tier 对齐。

2. **输出 schema** 中 `window_source` 枚举更新为 5 值：`"runtime | cached_size_reuse | config | empirical_peak | default"`，包含原来缺少的 `cached_size_reuse`。

3. **Task 1.6** 明确"固化…window_source enum 5 值"。

4. **`cached_size_reuse` 语义**在解析链中说明："复用上次 relay cache 见过的 `context_window_size`（session 内不变）"——澄清了 R1 所指"size 可信但 % 不可信"的混用风险。

**闭合判定**: 实质性修复。5 值枚举完整、relay_cache→runtime 约束显式、`cached_size_reuse` 语义已定义。

---

### M2 闭合验证 — CLOSED

**R1 问题**: Task 1.9 使用"structural substitute"备选路径但未定义条件、最低证明要求；Rule #6 豁免理由未提供；Level 2 patch 豁免条件检查不适用于新增完整 user-facing skill。

**Rev1 修复内容**:

Task 1.9 改写为：
```
Rule #6: deterministic structural substitute (token_telemetry parse 单测 fixture at
`aria-plugin-benchmarks/context-monitor/` — relay/transcript/corrupt/stale 各 1 fixture
+ window 4 档断言; 非 LLM AB, 参 `feedback_deterministic_structural_skill_rule6_substitute`)
```

分析：
1. **豁免路径已非"或"选**——Rev1 中 Task 1.9 删除了"或"选项，确定为 deterministic structural substitute，不再给实施者自行判断空间。
2. **fixture 路径已具名**: `aria-plugin-benchmarks/context-monitor/`，可审计。
3. **测试矩阵 4 fixture**: relay / transcript / corrupt / stale 各 1 fixture + window 4 档断言——覆盖范围明确。
4. **豁免理由成立性**: `token_telemetry.py` 是纯函数解析（读文件/读 JSONL → 计算），无 LLM 调用，确属 deterministic skill，Rule #6 feedback 中"deterministic structural substitute"先例适用。
5. **Memory 引用**: `feedback_deterministic_structural_skill_rule6_substitute` 已引用，有 owner-记录追溯。

**轻微保留（非 OPEN，降为观察）**: Rev1 没有 owner sign-off 明文，但 feedback memory 引用 + fixture 路径具名 + 测试矩阵明确，可接受为 Rule #6 要求的 structural substitute 最低证明要求。不升为 major，因为 Task 1.9 现在是确定性路径而非歧义路径。

**闭合判定**: 实质性修复。从"或选/未定义"变为"确定路径 + fixture 位置 + 4-fixture 矩阵 + memory 引用"。

---

### M3 闭合验证 — CLOSED

**R1 问题**: jq 缺失时 setup_relay.sh 行为未定义；doctor 输出格式与现有 aria-doctor 契约的继承关系未说明；3 态检测 Success Criteria 无伪造抗性测试要求。

**Rev1 修复内容** (Rev1 changelog M-rule6+jq 条目):

1. **jq 硬依赖 aria-doctor 检测**——确认 jq 是 doctor 必检项，而非 setup_relay.sh 自行处理。
2. **缺失 graceful degradation**——jq 缺失时 skill 降级路径已确认（transcript fallback + unavailable）。
3. **Task 1.5** 列入"jq 可用性"检测与 relay 3 态检测，作为 aria-doctor 集成任务。
4. **Success Criteria**: "aria-doctor 正确报告 3 态 + jq 缺失提示"——测试目标明确。

**部分保留（minor，已存在于 R1 m1 类别的延伸，此处降级记录）**: aria-doctor 输出格式继承关系（扩展现有 JSON schema vs 新脚本）Rev1 未显式说明，但 Task 1.5 定性为"aria-doctor 集成"，隐含继承现有契约。这是实施层面的细节而非 Spec 层漏洞，不妨碍 Phase B 进入。

**闭合判定**: 实质性修复——jq 降级路径已定义、doctor 检测职责已分配、Success Criteria 已含 3 态验收标准。

---

### R1 minor findings 闭合状态

**m1 (schema 版本漂移防御不可测)**: CLOSED。输出 schema 中已加入顶层 `schema_version: "1.0"` 字段（§What 输出结构中可见），Task 1.7 加入 corrupt-cache 场景，Task 1.2 明确 JSONDecodeError/OSError→unavailable 防御。

**m2 (#104 复现 criterion 不可执行)**: CLOSED。Success Criteria 中"与状态栏显示 0 偏差"对 relay_cache 路径有定义，Task 1.7 中含 fixture 验证，已足够在实施中可测。

**m3 (阈值建议无依据)**: CLOSED。Task 1.8 中"e.g. used%>85 建议暂停"加了 `e.g.` 标注，Success Criteria 相关条目未将其写为硬性规范，保留实施时校准空间。

---

## R2 新 Findings — Rev1 引入的新内容审查

### Rev1 新增内容范围

Rev1 新增了: §Staleness 契约 / §Relay 注入语义 / §window_source 解析链 / 输出 schema 拆分 `used_percentage`/`used_percentage_proxy` / atomic write 要求 / 新 internal skill `aria-token-telemetry` 分离 / Task 1.6-1.9 扩充 / Success Criteria 扩充。

---

### [minor] NEW-m1 — `used_percentage_proxy` 在 transcript fallback 路径下的语义契约不完整

**Category**: Specification Completeness | **Scope**: §What 输出结构

输出 schema 说明 `used_percentage_proxy` 为"transcript_fallback: (input+cache_read+cache_creation)/window"，但:

1. **`cache_creation` 是否同等权重计入**未说明依据——在 Claude API billing 语义中，cache_creation token 通常比 input token 更贵，但在 context window 占用上是同等权重的输入。Spec 省略了是否按 billing 权重还是 raw count 计算的说明，两种语义会给出不同的 `used_percentage_proxy` 值，实施时有歧义空间。

2. **`null` 一致性约束**——输出 schema 注释显示 relay 路径 `used_percentage_proxy` = null，transcript 路径 `used_percentage` = null。但当 `source=unavailable` 时两个字段的值未说明（均 null？仅 `used_percentage_proxy` null？），实施者无明确指导。

**严重级判定**: minor，不阻 Phase B。`source=unavailable` 时两字段均 null 是自然语义，且实施者可从 task 文本推断。但增加"source=unavailable 时 used_percentage 和 used_percentage_proxy 均为 null"的单行 note 可消除歧义。

---

### [minor] NEW-m2 — atomic write 与 relay 位置约束之间的并发模型未完整定义

**Category**: Resilience / Concurrency | **Scope**: §Relay 注入语义

Rev1 引入"原子写 tmp→rename"机制，理由是"避免 truncate→write 间并发读 corrupt"。但:

1. **tmp 文件路径未定义**——若多个 session 同时运行（multi-terminal coordination，Aria v1.22.x+），两个 session 的 statusLine command 均写 `.aria/cache/context-window-tmp-XXXX`，临时文件可能相互覆盖。Spec 中 tmp 文件命名策略（随机后缀 / PID 后缀 / session_id 后缀）未说明。

2. **最终 cache 文件路径是否 session-scoped**——`.aria/cache/context-window.json` 是单一全局 cache，但在 multi-terminal 下两个 session 写的可能是不同 model 的不同 window 尺寸。Spec 未说明是否需要 session-scoped cache（e.g. `context-window-{session_id}.json`）。

**严重级判定**: minor。目前 Aria 十步循环通常单 terminal 执行，且 DEC-20260529-001 未提及 multi-terminal 路径。但该场景在 Aria v1.22.x+ 已有先例，Phase B 实施者应意识到此风险。建议 Task 1.3 加 note 说明 tmp 命名策略或显式 OOS（Out of Scope）声明 multi-terminal 并发写不在本 Spec 范围。

---

### [minor] NEW-m3 — `aria-token-telemetry` 作为 internal skill 的加载边界未明确

**Category**: Architecture / Plugin Loading | **Scope**: §What Key Deliverables

Rev1 将 `aria-token-telemetry` 定义为 `user-invocable: false` 的 internal skill，复用 git-remote-helper US-012 Layer 3 先例。但:

1. **internal skill 被 user-facing skill 调用的机制**——Spec 说 `aria-context-monitor` "调 telemetry"，但 Plugin 系统中 internal skill 的加载方式是"由 aria-context-monitor 作为 dependency 声明"还是"直接调用 Python 脚本"未说明。两种方式对 aria-doctor 的覆盖能力有不同影响（前者依赖 plugin 依赖声明；后者是直接路径导入）。

2. **`user-invocable: false` 的 enforcement**——Spec 未说明这是 `.claude-plugin` metadata 字段（`plugin.json` 中配置）还是约定。若实施者遗漏该标注，skill 将对用户可见，但不会有功能影响。

**严重级判定**: minor。git-remote-helper Layer 3 先例已有实施，Phase B 实施者可参照。但对于 Phase B 开发者而言，"调 telemetry"的技术语义值得在 SKILL.md 实施阶段明确，避免接口边界歧义。

---

### 未发现新 [critical] 或新 [major]

对以下 Rev1 新增内容逐项扫描，未发现 critical/major 级新 defect：

- **§Staleness 契约** — 值、config key、行为三元完整，无歧义引入。
- **used_percentage / used_percentage_proxy 拆分** — 口径分离设计正确，`source` 字段作路由键，消费方协议明确。主要歧义限于 NEW-m1 的 `unavailable` 状态，属 minor。
- **`aria-token-telemetry` internal skill 分离** — 架构上正确（单一职责，#18 复用基础），加载边界属 minor（NEW-m3）。
- **Task 1.1 BLOCKING pre-Phase-B gate** — 失败回退条款有效；若 `context_window_size` 缺失，回退条款是合理的安全网。
- **window_source 5 值枚举 + relay_cache→runtime 约束** — 约束语义完整，实施层无新歧义。

---

## Verdict

| 维度 | 计数 | 项目 |
|------|------|------|
| R1 critical 已闭合 | 2/2 | C1 CLOSED / C2 CLOSED |
| R1 major 已闭合 | 3/3 | M1 / M2 / M3 均 CLOSED |
| R1 minor 已闭合 | 3/3 | m1 / m2 / m3 均 CLOSED |
| 新 critical (Rev1 引入) | 0 | — |
| 新 major (Rev1 引入) | 0 | — |
| 新 minor (Rev1 引入) | 3 | NEW-m1 / NEW-m2 / NEW-m3 |

**PASS_WITH_WARNINGS**

- 全部 R1 critical 已实质性闭合（C1 三元定义 + C2 marker 锚点 + Task 1.7 三场景）
- 全部 R1 major 已实质性闭合
- Rev1 新增内容引入 3 个 minor（均不阻 Phase B 进入）
- 无新 critical / major

**Phase B 进入资格**: 合格，附 3 个 minor warning 供实施者知悉。

**建议**: Phase B 开发者在 Task 1.2-1.3 实施时关注 NEW-m1（`used_percentage_proxy` 计算口径 + `unavailable` null 一致性）和 NEW-m2（tmp 文件命名策略）。NEW-m3（internal skill 加载边界）可参照 git-remote-helper SKILL.md 先例解决。

---

## 轮次记录

### R1 (2026-05-29T02:09:43Z)

**审计员**: qa-engineer
**结论**: FAIL — 2C + 3M + 3m
**关键发现**: C1 staleness threshold 缺失（Spec 层漏洞）; C2 relay 幂等无操作性定义（测试策略无法执行）

### R2 (本轮, 2026-05-29T02:19:16Z)

**审计员**: qa-engineer
**方法**: 逐条 R1 finding 闭合验证（5 项闭合标准：值/config key/行为/Success Criteria/Task）+ Rev1 新增内容全文扫描
**结论**: PASS_WITH_WARNINGS — 0C + 0M + 3 new minor; 全部 R1 findings CLOSED
**收敛状态**: 收敛 (converged=true) — R1 critical/major 均已实质性修复，无新 critical/major 引入，3 new minor 不影响 Phase B 进入资格
