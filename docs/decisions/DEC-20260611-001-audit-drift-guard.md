# DEC-20260611-001: audit-engine 多轮审计 Drift Guard — 原始目的锚定 (#17)

> **状态**: Approved (owner 已选 D1-D4 + R1-R3 审计累计修订全部并入; R3 两条 blocking 按裁判既定 escalation 口径以"裁判闭合标准全文钉死为本 DEC 契约 C-1/C-2 + tasks.md 强制首批任务"收口)
> **关联 Issue**: Forgejo 10CG/aria-plugin#17 (triage verdict = confirmed)
> **brainstorm 模式**: technical (issue 原案 + 4 哲学对齐决策 + 3 轮 challenge 收敛审计)
> **ship target**: aria-plugin v1.44.0 (当前 SOT = plugin.json v1.43.0, A.1 spec-drafter 须 re-verify, per memory `feedback_dec_ship_target_staleness_verify`)
> **决策日期**: 2026-06-11

---

## 1. 背景

### 1.1 触发与 triage verdict

#17 报告: audit-engine challenge 模式 (讨论组 → 挑战组 → 合并 → 挑战组再审) 的收敛判定基于四元组 `(type, severity, category, scope)` 集合比较, 存在结构性盲点 — **只检测"结论集合是否稳定", 不检测"我们是否还在讨论最初那个问题"**。triage verdict = **confirmed**: 当前收敛零 anchor/drift 机制, "集合稳定 ≠ 命中原始目的"。

### 1.2 Drift 发生路径 (issue 实证推演, post_spec 为例)

```
Round 1: anchor = proposal.md "问题 A" → 讨论组围绕 A 产出 {d1, d2} → 挑战组指出副作用 B
Round 2: 合并后主要在处理 B → 挑战组围绕 B 的新实现提 {c1, c2}
Round 3: 讨论组针对 c1/c2 修订 → 挑战组 {c1, c2} 稳定
→ 收敛判定: PASS (四元组集合两轮相同)
→ 但"问题 A 是否被正确解决"从未被重新验证
```

对抗式讨论从原始 anchor 慢慢漂走, 轮数越多越严重, 且被"全员合并"步骤放大。

### 1.3 影响范围

高风险 (多轮数 + 开放式讨论): `post_spec` / `post_brainstorm` (最易漂移) / `post_planning` (易被"新发现约束"带跑) / `pre_merge` (易从"Spec 是否实现"漂到"代码风格/工程实践")。影响最小: `post_closure` (已限 `max_rounds=1`, 本机制不适用)。

### 1.4 与 #79 的边界

**#17 = 审计讨论轮内 drift** (anchor 固化在单次审计周期内); **#79 = mid-implementation spec drift** (实施期偏离 Spec)。两者机制独立, audit-engine SKILL.md 加一行 NOTE 划清边界; tasks.md 明确 #79 文档归属文件, 可行则加对称反向 cross-ref, 若 #79 尚无文档落点则标注 "#79 文档待定, #17 单向 NOTE 暂可接受"。

---

## 2. 约束条件

| # | 约束 | 来源 |
|---|------|------|
| C1 | **advisory-over-hardlock**: 不发明新硬中止路径; refocus 只约束审计 agent 不约束 owner; drift 终止以既有 FAIL verdict 正常结束走 owner 决策流程 | DEC-20260519-001 既定哲学 + memory `feedback_concurrency_advisory_over_hardlock` |
| C2 | **additive backward-compat**: 报告 schema 全部 additive; 旧报告缺 drift 字段视为 `drift_ratio=0`, `converged_on_anchor=null`, 不告警 | Rule #4 + report-format.md 既有 backward-compat 模式 |
| C3 | **audit-engine 无 Python**: 触及面 = 纯 prose + schema (SKILL.md + references/*.md), 无代码 | audit-engine 既有架构 |
| C4 | Rule #6: 纯 prose/schema 变更 → substitute = doc-existence + schema 骨架 fixture + 本 Spec post_spec audit dogfood (非 capability AB) | 不可协商规则 #6 + memory `feedback_deterministic_structural_skill_rule6_substitute` |
| C5 | 配置经 config-loader 统一管线, 默认值落 DEFAULTS.json, 验证规则进 SKILL.md 字段验证规则表 | config-loader 既有契约 |
| C6 | **供给侧契约 (#126 同构)**: frontmatter 字段供给侧强制声明, 不把字段设置责任全丢给事后聚合层 | memory `feedback_audit_prompt_must_require_frontmatter` |
| C7 | **dashboard parser 兼容 (#125/#126)**: frontmatter `verdict` 字段恒为裸枚举 (FAIL), drift override rationale 仅出现在 body `## Verdict` 节 | aria-dashboard parser 既有约束 |
| C8 | **token 护栏有效性**: refocus 轮必须消耗 max_rounds 配额 (防活锁), max_rounds 仍是总轮数硬上界 | 审计 R1 修订 |
| C9 | fail-open 一致性: drift-checker 失败/超时不得阻塞审计本体 (drift guard 是附加防护, 不是新单点故障) | C1 推论 + 审计修订 |

---

## 3. 考虑的方案 (D1-D4 候选 + 评分 + 选定)

### D1 — drift_ratio > 50% 的处置

| 候选 | 描述 | 评分 | 选定 |
|------|------|------|------|
| A (issue 原案) | Abort & Refocus, round 计数不前进; 连续 2 次偏移则**中止审计并上报** | 低 — 发明新硬中止路径, 违反 advisory-over-hardlock; round 冻结使 max_rounds token 护栏失效 (活锁风险) | |
| **B** | **强制 refocus 轮 (prompt 回锚 anchor) + 连续 2 次 → 审计以既有 FAIL verdict (drift 标注) 正常结束, 走 owner 决策流程** | **高 — 不发明新中止路径, refocus 只约束审计 agent 不约束 owner** | **✅** |

**D1 选定 = B (审计强修订)**, 三组关键修订:
- **配额与编号**: refocus 轮**消耗 max_rounds 配额** (防活锁, token 护栏有效); round 展示用独立标签 (`R{N}-refocus` / `per_round[].is_refocus` 字段) 而非冻结重号; 引入 `consecutive_refocus_count` (normal round 后归零) 定义"连续 2 次"; refocus 轮输出**替换 round_N 作下轮 stability 比较基线**, 不进入 oscillation N/N-2 序列。
- **终局语义**: drift 终止走 **verdict override** 规则 (`drift_terminated: true → verdict=FAIL`, additive frontmatter 字段), 不走 synthesized critical finding (避免污染 category 枚举)。
- **状态机**: `check_convergence()` 新增独立终局状态 **DRIFT_TERMINATED** (详见 §4.4)。

### D2 — drift 判定主体

| 候选 | 描述 | 评分 | 选定 |
|------|------|------|------|
| **A** | **每轮收敛判定前, 独立轻量 drift-checker (与讨论组/挑战组/judge 三方分离) 拿 anchor + 本轮结论清单逐条分类 on-topic/adjacent/off-topic → drift_ratio = off-topic/all** | **高 — 第四方独立视角, 无自评偏置** | **✅** |
| B | judge/收敛判定者自评 drift | 低 — 自评偏置, judge 自身可能已被带跑; 与三方分离原则冲突 | |

**D2 选定 = A (审计强修订)**:
- **定位**: drift-checker 是 **audit-engine 内部轻量调用** (非 agent-team-audit 编排的审计 agent), 输出结构化 `drift_metrics` 而非 audit report, **不适用 8-field 契约** (agent-dispatch-contract.md 加一句 scope 排除)。
- **分母 per-mode 显式定义**: convergence = 当轮 `conclusion_records`; challenge = `revised_discussion_output.decisions ∪ updated_challenge_output.objections` (否则对抗式发散场景 drift guard 半盲)。
- **除零 guard per-mode 精确化**: convergence 模式 `conclusion_records=∅`; challenge 模式 `decisions=∅ AND objections=∅` (即 `|decisions ∪ objections|=0`) → `drift_ratio=0` (vacuously zero, 跳过 LLM 调用), 与 0-finding 双轮稳定性既有路径及 backward-compat 语义对齐。防实现者以 `decisions=∅` 单边触发致 objections 被误排除。
- **命名空间**: `off_topic_ids` 条目保留原 id 前缀 (`d-`/`obj-`) 标注来源; challenge objection 因无结构化 scope, 分类仅基于 point 文本 + `anchor.in_scope/out_of_scope_hints` 关键词比对, 置信度低于 decision 路径, 报告需可区分两类来源。
- **fail-open**: spawn 失败/超时 → `drift_ratio=null` 按 <warn 档处理 + `drift_check_skipped: true`, `consecutive_refocus_count` 不增加 (advisory-over-hardlock 一致); 与 `round_state.incomplete` **正交** (二者错误处理表明确区分), 整轮超时耗尽场景的归因规则补入正交声明。
- **时间契约**: drift-checker 独立短超时 (**30-60s**), 不计入审计 agent 的 300s/轮预算; 并发控制表显式区分**单次 agent spawn 超时 (300s)** 与**整轮 wall-clock** (challenge 模式整轮 = 4×串行 spawn + drift-checker 独立配额)。

### D3 — 默认 scope

| 候选 | 描述 | 评分 | 选定 |
|------|------|------|------|
| **A** | **challenge 模式默认开; convergence 可选默认关; post_closure (max_rounds=1) 不适用** | **高 — 高风险场景默认防护, 低风险不加税** | **✅** |
| B | 全检查点全模式默认开 | 中 — convergence 单向收敛漂移风险低, 默认开过严 + token 税 | |
| C | 全部默认关 (opt-in) | 低 — 高风险 challenge 场景 guard 形同虚设 | |

**D3 选定 = A**。

### D4 — 阈值

| 候选 | 描述 | 评分 | 选定 |
|------|------|------|------|
| A | 硬编码 issue 阈值表 (20% / 50%) | 中 — 不同项目讨论风格差异大, 阈值不可调 | |
| **B** | **可配 — `.aria/config.json` `audit.drift_guard.{warn_threshold: 0.2, refocus_threshold: 0.5, convergence_mode: false}`, 经 config-loader, 默认值即 issue 阈值表** | **高 — 默认即最佳实践, 可按项目调** | **✅** |

**D4 选定 = B**, 配置契约详见 §4.6 (契约 C-1)。

---

## 4. 最终机制

### 4.1 Step 0 — Anchor 固化 (Round 1 前一次性, 审计周期内不可变)

SKILL.md 入口流程新增 **Step 0**, 固化结构:

```json
{
  "anchor": {
    "checkpoint": "post_spec",
    "primary_goal": "<从 context 提取的原始目的>",
    "in_scope": [],
    "out_of_scope_hints": [],
    "source_sha": "<freeze 时 git SHA>"
  }
}
```

写入报告头, 审计周期内不可变 (不支持 mid-audit re-anchor)。

**per-checkpoint anchor 来源 fallback 链** (序: 正向 source → 降级 → fail-soft):
1. **proposal 类** (post_spec / post_planning): proposal.md 的 Why/Goal 段。
2. **diff/UPM 类** (mid_implementation / post_implementation / pre_merge): 经 `change_id` 解析 proposal.md (复用 pre-write-validation 既有锚点链) → 降级 PR 标题/描述 (此时 `source_sha` = 当前 HEAD SHA + `anchor_source=degraded`)。
3. **brainstorm_decisions** (post_brainstorm 正向覆盖, 第四 source 类型): 从传入 context (brainstorm 决策记录) 提取 `primary_goal`=核心议题 / `in_scope`=已确认决策方向 / `out_of_scope_hints`=DEFERRED 条目; 含 Forgejo issue 链接时可升级抓 issue 标题。链序: brainstorm_decisions → issue_title → fail-soft, 使 fail-soft **不再是 D3 默认开启 checkpoint 的预期常态**。
4. **全缺 → fail-soft**: 跳过 drift 计算 + 报告标注 `drift_anchor_missing` / `anchor_source=degraded`, **不阻塞审计**。

**post_brainstorm 调用契约** (SKILL.md Step 0 节单独说明): (a) brainstorm skill 调用时 context 传入决策记录文件路径 (如 `.aria/brainstorm-{id}.md`); (b) 提取器识别"已确认决策"段提取 `in_scope`、"DEFERRED 条目"段提取 `out_of_scope_hints`; (c) context 为 Forgejo issue URL 时降级 issue_title。brainstorm SKILL.md (或调用接口文档) 注明应传入的 context 类型, 保证调用契约与 anchor 提取链对齐。

**partial anchor 分类规则** (写入 challenge-mode-schema.md D2 节, 防实现者自行发明): anchor 结构完整但 `in_scope=[] AND out_of_scope_hints=[]` 时, drift-checker 降为 primary_goal 语义相似度单维分类 (语义相关 → on-topic, 否则 adjacent), 报告标注 `anchor_scope_empty: true` + `drift_classification_confidence: low`; **不触发 fail-soft skip**。

### 4.2 每轮 Drift Check (Step 5)

`check_convergence()` 伪代码在 **Round-1 guard 之后**嵌入 `drift_action = check_drift(round_N, anchor)` 节点; challenge-mode-schema.md 数据流图与步骤列表加 **Step 5: Drift Check** + 三档处置决策树。

- **Round 1 跳过** drift 检查 (`drift_ratio` 不计算, `consecutive_refocus_count` 不变), 理由: 无前序稳定基线; 边界情况表加"Round 1 drift check → 跳过"行。
- 分类三档: on-topic / adjacent / off-topic; `drift_ratio = off-topic / all` (公式与阈值不改, adjacent 不计入分子 — 尊重 owner D2 决策 + advisory 哲学)。
- **adjacent 盲区可观测性 (additive)**: `drift_metrics.per_round` 从仅 `off_topic_ids` 扩为三类计数 `{on_topic, adjacent, off_topic}`; 最终轮 `on_topic==0` 时报告标注 `anchor_engagement: none` (纯 annotation, 不改收敛/verdict 行为)。

### 4.3 三档处置

| drift_ratio | 处置 |
|---|---|
| `< warn_threshold` (默认 0.2) | 正常进入收敛判定 |
| `[warn, refocus)` 档 | **Warning** — 报告标注; **双模式语义不同** (见下) |
| `>= refocus_threshold` (默认 0.5) | **强制 refocus 轮** (REFOCUS_ROUND); 连续 2 次 → DRIFT_TERMINATED |

**warn 档双模式语义** (分别写入 convergence-algorithm.md / challenge-mode-schema.md):
- **convergence 模式**: 解读 A — 该轮**不允许全票 PASS 收敛**。实现点定为**汇总层覆盖**: `check_convergence` 内 `drift_action=WARN` 时强制 `unanimous=false`, 与 agent 投票解耦, **不注入 agent prompt** (避免 agent 知晓 drift 的副作用)。每轮独立重新评估 (drift_ratio 回落则收敛正常恢复, 持续触发由 max_rounds 降级兜底)。
- **challenge 模式**: 收敛判据为 `objections_resolved`, 与 unanimous_pass 无关 → warn 档**降格为仅标注不阻塞** (报告追加 `drift_warning` 字段, 不覆盖 `objections_resolved`); refocus 档仍按 REFOCUS_ROUND 执行。

**refocus 轮机制**:
- prompt 回锚 anchor, **消耗 max_rounds 配额**; 底层逻辑 round 为整数 N + `is_refocus: true` 字段 (展示标签 `R{N}-refocus`, `rounds 整数 + is_refocus` 组合唯一标识一轮, 标签不止于展示层)。
- `consecutive_refocus_count`: refocus 触发 +1, normal round 后归零; >= 2 → DRIFT_TERMINATED。drift_check_skipped 轮不增加。
- refocus 轮输出**替换 round_N 作下轮 stability 比较基线**; oscillation 检测的 N-2 寻址显式定义为 **normal-round 逻辑序列** (`is_refocus==true` 条目从振荡比较序列剔除), 与 stability 基线替换保持同一索引语义。convergence-algorithm.md 附 normal→refocus→normal 最小 trajectory 示例, 逐轮标注 stability 比较对象与 oscillation 比较对象, 并标注第二次连续 refocus 轮的 oscillation 比较序列 (确认 is_refocus 当轮不作为 oscillation 的 keys_N), 防误判 OSCILLATION 而非 DRIFT_TERMINATED。

### 4.4 终局状态机

`check_convergence` 新增独立终局状态 **DRIFT_TERMINATED**, 与 CONVERGED / OSCILLATION / MAX_ROUNDS_EXHAUSTED 并列:

- **四终局完整优先级链** (伪代码显式写出 return 顺序): `CONVERGED → DRIFT_TERMINATED → OSCILLATION → MAX_ROUNDS_EXHAUSTED`。
- `converged=false + drift_terminated=true` 组合**不触发 max_rounds 三路径降级**, 直接以 FAIL 结束; report-storage.md converged × verdict 组合含义表加 `drift_terminated` 行, 并将"false | * | 触发降级策略"行**排除 drift_terminated 情形**。
- **边界轮**: 第二次连续 refocus 恰逢 `round == max_rounds` 时, DRIFT_TERMINATED **优先于** MAX_ROUNDS_EXHAUSTED。
- **max_rounds<3 死代码标注** (纯文档说明不改逻辑): convergence-algorithm.md 边界情况表补行 — `max_rounds < 3` 时 DRIFT_TERMINATED 不可达 (`consecutive_refocus>=2` 需至少 3 轮), drift guard 降级为 max_rounds 兜底。config-loader max_rounds 验证注释补 "drift guard 完整功能需 max_rounds >= 3"。
- **verdict override**: `drift_terminated: true → verdict=FAIL`; frontmatter verdict 恒为裸枚举 `FAIL` (C7), drift override rationale 仅出现在 body `## Verdict` 节, 模板加 rationale 锚点 (如 `FAIL (drift override) — 连续 2 次 refocus 未回锚, Critical=0`)。阻塞行为表注明 drift-FAIL 继承 per-checkpoint 既有处置, 并为 blocking checkpoint 写明 **owner remediation 路径** (重跑 / 收窄 context / 显式 override), 区别于普通 FAIL 的修 finding 路径。

### 4.5 报告 schema — 契约 C-2 (R3 blocking #2 闭合标准全文钉死, tasks.md 强制首批任务)

全部 **additive**:

- **report-format.md**: frontmatter template 补 `drift_terminated` / `drift_check_skipped` / `is_refocus` (默认 `false`, 与 backward-compat 缺字段视为 `drift_ratio=0` 语义一致); `drift_metrics` 章节骨架 = anchor 快照 + per_round 表 (三类计数 `{on_topic, adjacent, off_topic}` + `off_topic_ids` 带 namespace 前缀) + `anchor_engagement` 标注 + `consecutive_refocus_count` + `converged_on_anchor`; "特殊标记字段"节末尾补 drift_metrics backward-compat 小节 (缺字段 → `drift_ratio=0`, `converged_on_anchor=null`, 不告警)。
- **converged_on_anchor 计算规则显式写明**: `= converged AND 最终轮 drift_ratio < warn_threshold`; `drift_terminated` 时恒 `false`。
- **report-storage.md 同步**: frontmatter 补同名字段 + "drift_metrics 见 report-format.md (SOT)" cross-ref; converged×verdict 组合含义表加 drift_terminated 行 (`converged: false, drift_terminated: true, verdict: FAIL`) 并排除该行触发降级策略; `is_refocus` / `consecutive_refocus_count` 字段定义落 report-storage.md。
- **verdict 计算规则 SOT 归属显式指定**: report-storage.md §Verdict 为 SOT, report-format.md 改 cross-ref (一处声明一处 cross-ref, 双文件不重复声明)。
- **drift 字段注入语义统一 (复用既有 oscillation pattern)**: `drift_terminated` / `drift_check_skipped` 不做 all-or-nothing 条件注入 — template **无条件**加 `drift_terminated: false` / `drift_check_skipped: false` 默认字段, 单 agent 默认 false, 由 audit-engine **聚合时覆盖**; 仅 dispatch 时已知字段 (`is_refocus`、上一轮 `drift_check_skipped`) 注入实值。同时消解"强制全填 vs 条件注入"语义冲突与"agent 不可能预知 drift_terminated"时序矛盾。
- **供给侧契约 (#126 同构)**: agent-dispatch-contract.md 在固定 8-field 模板后加 "### Drift Guard 字段" 小节说明聚合覆盖语义 + refocus 轮 frontmatter 显式定义 (`rounds` 填底层逻辑 round 整数 N + `is_refocus: true`, audit-engine refocus 轮 dispatch 时注入) + 一句 drift-checker scope 排除 (内部调用, 输出 drift_metrics 非 audit report, 不适用 8-field 契约)。
- **存储位置节 drive-by 修复** (升格为 tasks.md 独立 doc-existence 检查项, 标注 "drive-by, pre-existing" 防 post_spec audit 误归为 drift guard 机制): report-format.md 删除旧 schema `{checkpoint}-{timestamp}.md` 示例, 替换为指向 report-storage.md §存储位置 (v1.17.4+ 5-field schema) 的 cross-ref, 存在 cross-ref 链接即为验证完成。

### 4.6 配置 — 契约 C-1 (R3 blocking #1 闭合标准全文钉死, tasks.md 强制首批任务)

`.aria/config.json` → `audit.drift_guard.*`, 经 config-loader:

| 字段 | 类型/域 | 默认 | 验证规则 (config-loader SKILL.md 字段验证规则表三条) |
|------|---------|------|------|
| `warn_threshold` | number, [0,1] | 0.2 | 域外 → warn + default |
| `refocus_threshold` | number, [0,1] | 0.5 | 约束 `>= warn_threshold`, 违反时 **warn + 单向 clamp** (R3 闭合标准, 取代 R1 暂案 warn+swap) |
| `convergence_mode` | boolean | false | 描述注明: challenge 默认开 + convergence 可选 (本字段) + post_closure 由模式选择阶段屏蔽 |

- **DEFAULTS.json** audit 块新增 `drift_guard {warn_threshold: 0.2, refocus_threshold: 0.5, convergence_mode: false}` 同步。
- SKILL.md 配置依赖区块说明 `convergence_mode` 语义。
- `max_rounds` 验证注释补 "drift guard 完整功能需 max_rounds >= 3"。

### 4.7 Token 成本

convergence-algorithm.md 收敛统计表加 drift-checker per-round token 增量估算 (**~+1-2K/轮**), 修复 max_rounds token 护栏论证基数 (refocus 消耗配额 + 增量入表 → 总成本仍有硬上界)。

---

## 5. 理由

1. **D1=B advisory 哲学对齐**: 不发明新硬中止路径 — drift 终止复用既有 FAIL verdict 通道正常结束, owner 保留全部决策权 (重跑/收窄/override); refocus 消耗 max_rounds 配额使 token 护栏始终有效 (issue 原案"round 计数不前进"有活锁风险)。
2. **D2=A 第四方分离消除自评偏置**: judge 自身可能已被讨论带跑, 独立 drift-checker 只看 anchor + 结论清单, 判定面最小; 定位为内部轻量调用而非审计 agent, 避免污染 agent-team-audit 编排契约与 8-field 报告契约。
3. **D3=A 风险分层**: challenge 对抗式多轮是 drift 高发区默认开; convergence 单向收敛漂移风险低, 可选开避免 token 税; post_closure 1 轮无 drift 可言。
4. **D4=B 默认即最佳实践**: issue 阈值表作为默认值, 项目可按讨论风格调整, 经 config-loader 统一验证管线 (含 clamp 守卫) 防配置自相矛盾。
5. **分母 per-mode 定义堵住半盲**: challenge 模式若只看 decisions, 挑战组 objections 发散 (drift 最常见路径) 完全不可见; `decisions ∪ objections` 使 guard 覆盖对抗双侧。
6. **注入语义复用 oscillation pattern**: 无条件默认 false + 聚合覆盖, 同时满足 #126 供给侧契约 (template 强制声明字段) 与时序现实 (agent 不可能预知 drift_terminated), 不引入第二套注入语义。
7. **R3 两条 blocking 以裁判自身闭合标准收口**: 裁判明示"至少落地为设计 delta/tasks.md 可验证条目方可关闭"+"建议降格为 tasks.md 强制首批任务后带条件收敛" — 本 DEC §4.5/§4.6 即设计 delta 全文, 并钉死为 tasks.md 强制首批任务 (实施期 post_spec audit 将 grep 核验真实文件落地)。

---

## 6. 风险与缓解

| # | 风险 | 缓解 |
|---|------|------|
| R1 | refocus 冻结重号致活锁 / token 无上界 | refocus 消耗 max_rounds 配额 (C8); 标签层用 is_refocus 区分, 不冻结底层计数 |
| R2 | drift-checker 成为新单点故障阻塞审计 | fail-open: spawn 失败/超时 → drift_ratio=null 按 <warn 档 + drift_check_skipped=true; 独立 30-60s 超时不占 300s/轮预算; 与 round_state.incomplete 正交 |
| R3 | DRIFT_TERMINATED 被误判为 OSCILLATION (refocus 轮卷入 N/N-2 比较) | oscillation N-2 寻址 = normal-round 逻辑序列 (is_refocus 剔除); 四终局优先级链显式排序; trajectory 示例逐轮标注两类比较对象 |
| R4 | anchor 提取失败使 guard 在高风险 checkpoint 形同虚设 | 四级 fallback 链 (proposal Why/Goal → change_id 锚点链 → brainstorm_decisions/issue_title → PR 标题); fail-soft 仅最终兜底且报告显式标注 drift_anchor_missing, 不再是 post_brainstorm 预期常态 |
| R5 | partial anchor (in_scope/hints 双空) 静默错误分类 | 降为 primary_goal 单维分类 + anchor_scope_empty + confidence: low 显式标注, 不 fail-soft skip |
| R6 | drift override rationale 写入 frontmatter verdict 破坏 dashboard parser (#125/#126 重演) | C7: frontmatter verdict 恒裸枚举, rationale 仅 body ## Verdict 节 |
| R7 | 旧报告 / 未升级 agent 缺 drift 字段致消费侧崩 | C2 additive backward-compat: 缺字段 → drift_ratio=0, converged_on_anchor=null, 不告警; template 无条件默认 false |
| R8 | verdict 规则双文件 (report-format / report-storage) 漂移 | SOT 归属显式指定: report-storage.md §Verdict 为 SOT, report-format.md cross-ref |
| R9 | challenge 模式 drift 半盲 (只看 decisions) | 分母 = decisions ∪ objections; 除零条件 per-mode 精确定义 (AND 联合判空) |
| R10 | agent 知晓 drift 状态产生迎合性副作用 | warn 档实现点 = 汇总层覆盖 unanimous, 不注入 agent prompt |
| R11 | adjacent 大量堆积但 ratio 不触发, guard 盲区 | 三类计数全披露 + 最终轮 on_topic==0 → anchor_engagement: none 标注 (advisory, 不改行为) |
| R12 | config-loader / report schema 落地再次"零落地" (R1-R3 三轮实证风险) | 契约 C-1/C-2 闭合标准全文入 DEC + tasks.md 强制首批任务; post_spec audit / 实施 code-review 以 grep 核验真实文件命中为验收 (memory `feedback_verify_edit_landed_grep_count`) |

---

## 7. 实现触及面 (纯 prose + schema, audit-engine 无 Python)

| 文件 | 改动 |
|------|------|
| `aria/skills/audit-engine/SKILL.md` | 入口流程加 **Step 0 anchor 固化** (fallback 链 + post_brainstorm 调用契约); 错误处理表加 drift-checker 行 (fail-open + 正交声明); #17 vs #79 边界 NOTE 一行 |
| `references/challenge-mode-schema.md` | 数据流图 + 步骤列表加 **Step 5: Drift Check** + 三档处置决策树; 分母 (decisions ∪ objections) 显式定义; partial anchor 分类规则 (D2 节); 除零 per-mode 条件; warn 档 challenge 语义; 时间契约 (Step 5 节) |
| `references/convergence-algorithm.md` | check_convergence 伪代码嵌 drift_action 节点 (Round-1 guard 后) + REFOCUS_ROUND 分支 + 四终局优先级链 return 顺序; consecutive_refocus_count 章节 (normal 归零, >=2 终止); 振荡豁免节 (N-2 normal-round 序列) + trajectory 示例; warn 档 convergence 实现点 (汇总层覆盖); 边界情况表 (Round 1 跳过行 + max_rounds<3 死代码行); 收敛统计表 (token +1-2K/轮 + spawn vs wall-clock 区分) |
| `references/report-format.md` | **契约 C-2**: frontmatter 补 drift_terminated/drift_check_skipped/is_refocus 默认 false; drift_metrics 章节骨架 (anchor 快照 + per_round 三类计数 + anchor_engagement + consecutive_refocus_count + converged_on_anchor 计算规则); backward-compat 小节; rounds+is_refocus 唯一标识说明; verdict 改 cross-ref report-storage.md SOT; 存储位置节改 cross-ref (drive-by, pre-existing) |
| `references/report-storage.md` | **契约 C-2 同步**: frontmatter 字段同步 + drift_metrics cross-ref; §Verdict (SOT) 加 drift_terminated override 规则 + rationale 锚点 + owner remediation 路径; converged×verdict 表加 drift_terminated 行并排除降级; is_refocus / consecutive_refocus_count 字段定义 |
| `references/agent-dispatch-contract.md` | 8-field 模板后加 "### Drift Guard 字段" 小节 (无条件默认 false + 聚合覆盖 + dispatch 已知字段注入实值); refocus 轮 frontmatter 定义 (rounds 整数 N + is_refocus: true); drift-checker scope 排除一句 |
| `references/execution-modes.md` | 核查 challenge 步骤列表: 有独立 4-step 列表则同步加 Step 5 或 cross-ref challenge-mode-schema.md; 仅委托则标注 "仅 cross-ref, 无须独立修改" 封闭歧义 |
| `aria/skills/config-loader/SKILL.md` | **契约 C-1**: 字段验证规则表补三条 (warn_threshold / refocus_threshold 含 >= 约束 + 单向 clamp / convergence_mode); 配置依赖区块 convergence_mode 语义; max_rounds 注释补 ">= 3" |
| `aria/skills/config-loader/DEFAULTS.json` | **契约 C-1**: audit 块新增 `drift_guard {warn_threshold: 0.2, refocus_threshold: 0.5, convergence_mode: false}` |
| `CLAUDE.md` | **免改** (审计两轮 endorse 复确认; ship 时按 Phase D 标准流程更新项目状态/footer) |
| 版本 SOT (5+1) | plugin.json (真理来源) + marketplace.json (×2 缩进, memory `feedback_marketplace_json_dual_version_indent`) + VERSION + CHANGELOG.md + README.md + 主项目 gitlink/VERSION |

**tasks.md 要求**: ① 上表全部文档锚点并入 **doc-existence 可验证清单** (含 execution-modes.md 条目 + verdict SOT 归属 + 存储位置节 drive-by 单列 task); ② **契约 C-1/C-2 为强制首批任务** (R3 blocking 收口, 实施首个 commit 落地, post_spec audit grep 核验); ③ #79 文档归属明确 (无落点则标注 "#79 文档待定, #17 单向 NOTE 暂可接受")。

---

## 8. Rule #6 验证策略

触及面 = 纯 prose + schema (无代码) → Rule #6 substitute = **doc-existence + structural fixture + dogfood** (非 capability AB):

1. **doc-existence 清单** (tasks.md 可验证条目, 逐条 grep 核验): §7 表全部锚点, 重点 = 契约 C-1 (DEFAULTS.json + config-loader SKILL.md 对 `drift` 命中) 与契约 C-2 (report-format.md drift_metrics 骨架 + frontmatter 字段) — R1-R3 三轮零落地的两处, 实施验收以 grep 命中为准。
2. **schema 骨架 fixture**: drift_metrics 章节结构 (per_round 三类计数 / anchor 快照 / converged_on_anchor) 与 frontmatter 默认字段作为 structural fixture。
3. **结构性可验证标准**: `drift_metrics.per_round 条目数 == 实际轮次数` (含 drift_ratio=0 正常轮与 is_refocus 轮)。
4. **dogfood**: 本 Spec 自身的 post_spec audit (challenge 模式, drift guard 默认开) 须产出**非空 drift_metrics** — 机制上线第一刀验自己。

---

## 9. Out-of-Scope

- **#79 mid-implementation spec drift**: 实施期偏离 Spec 的检测属 #79, 本 DEC 仅做边界 NOTE + 可行时对称 cross-ref。
- **D2 公式与阈值语义变更**: adjacent 不计入 drift_ratio 分子的公式不改 (仅加三类计数可观测性 annotation); 阈值默认值即 issue 原案。
- **post_closure**: max_rounds=1, drift guard 不适用, 不做任何改动。
- **mid-audit re-anchor**: anchor 审计周期内不可变, 不支持中途换锚 (换锚 = 另起一次审计)。
- **旧报告 backfill**: backward-compat 仅消费侧容错 (缺字段视为 drift_ratio=0), 不回填历史报告。
- **drift-checker 升格为编排 agent / 8-field 契约纳入**: 永久定位为 audit-engine 内部轻量调用。