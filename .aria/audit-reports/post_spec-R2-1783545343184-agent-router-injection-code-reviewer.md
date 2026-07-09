---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T20:57:19.928Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 审计报告 — agent-router-auto-project-agent-injection Rev1 (code-reviewer)

## R1 closure 核验

我维度 R1 findings (2 Major + 5 Minor) 对 Rev1 逐条核验, **7/7 全部实质落文, 无纸面关闭**:

| R1 finding | Rev1 处置 | 核验结论 |
|---|---|---|
| Major-1 required_caps 无成文映射 | §2.1 两级闭集 + B3 半确定性定位 + AC fixture pin 输入 | 实质关闭 (路线不同于 R1 建议的种子映射表, 但闭集+证据+pin 等效成立); **衍生新缺口 → R2-CR-1** |
| Major-2 差值带 vs 胜出数学冲突 | §2.4 R-a 决定性直派前置豁免 (采纳 R1 修法(b) 增强版) | **真关闭** — #153 场景数学复算: match_rate 1.0 + \|required\|≥2 → R-a 直派, 不进 R-b 差值带; AC-1/AC-5 期望统一; **但 §2.4 新文本衍生 R2-CR-2/3** |
| M-1 版本位置失准 | §6 L17 header 1.0.0→1.2.0 + L449 footer 1.1.0→1.2.0 + frontmatter 无 version 更正 + ROUTING_RULES L3 | **真关闭** — 对源核验四处全准 (SKILL.md L17=`1.0.0` / L449=`1.1.0` / L1-13 无 version 字段 / ROUTING_RULES L3=`1.0.0`) |
| M-2 发版清单缺主仓段 | §6 发版清单: marketplace **两处** version (不同缩进) / gitlink / 主仓 VERSION / badge L8+Project Status / i18n #140 B 档 | **真关闭** — R1 点名项全覆盖 |
| M-3 §408 framing 删除歧义 | §6 保留 D4 rationale (回撤 Rev0 表述), 仅删「已生效」暗示 | **真关闭** — 采纳 R1 修法 (id 拼写 f2a4a9a/f2a4ac9a 不一致 → R2-CR-8) |
| M-4 B1 强制步 vs 既有配置 | B1 重写为「默认步受门控」+ §1 3e 门控 bullet + §5 归口 + AC-3 三支 | **真关闭** |
| M-5 逐字节断言过强 | AC 总注: 结构化字段级, reason 不比字节 | 关闭; **但「决策路径 R-a/R-b」断言维度无输出字段载体 → 并入 R2-CR-2** |

跨维度观察: **450102ae (同名保护与全局最高复合, R1 Major) 关闭不完全** — Rev1 给了复合顺序 (池构建期先去重后评分), 但「替换」的得分归属仍未定义, 沿用 R1 scope 以 R2-CR-5 报出。

角色侧重的引用逐行核验 (Rev1 新增引用 vs 源) **全部通过**:
- (a) handoff-contract.md L14 `agent_source: "plugin" # "plugin" (内置) | "project" (项目级 .aria/agents/)` + L33 `预留 Layer 2 项目级 Agent` — OOS 转述与原文一致, 行号准确
- (b) US-011.md L5 Status done / L40 D1 / L43 D4「agent-router 需动态感知项目级 Agent」/ L51 AC-4「运行时注入…首次缓存」/ L61 Scope「修改: agent-router」— errata 对象准确, 「auto 路径未真正生效」措辞与 #153 双跑实证精确对齐
- (c) config.template.json 确无 `agent_router` 块 (全文 L1-72 核验) — §5「owner 无发现路径」属实
- (d) SKILL.md 版本三处与 Rev1 表述一致 (见上表 M-1)
- (e) ROUTING_RULES L3 版本位置准确; 维护指南 L255 枚举原文 `(FP/TT/关键词)` 转述准确 (但见 R2-CR-12)
- (f) SKILL.md L136 `task_type` 确为既有可选参数 (默认「自动推断」→ 见 R2-CR-11)
- (g) taxonomy L2 头注释 `# Used by agent-gap-analyzer for deterministic tag matching` 原文核实
- Resolved 表 39 条 vs 正文处置一致性**全表核对** (超出 10 条抽查要求): §2.1/§2.2/§2.3/§2.4/§2.5/§3/§4/§5/§6/B1-B10/AC-1..AC-9 声称的段落全部真实存在且含对应内容; 仅 2 处元数据失真 (R2-CR-8)
- Why 段 M7 L129 转述与原文一致 (「本 Spec 不依赖任何未实现的 routing 能力, 也不改 agent-router」+ v1.1.0 pin); audit-augmentation archive L16 原文「triage 已确认 agent-router 任务路由路径**会**扫 .aria/agents/」转述一致; adapter D4 (L190) framing 准确

## 审计结论 (新 finding, 全部带证据)

### Major (5)

**R2-CR-1 (architecture, §2.1) — L1/L2 复合规则未定义, AC-1 fixture pin 可被 L2 加料击穿** [fix-introduced]
§2.1 定义了 L1/L2 各自命中方式与空集退化, 但没有一句定义两级复合关系 (L1 命中非空时 L2 是否仍运行/union)。AC 总注声称「fixture 按 §2.1 L1 pin 住 required_caps 输入…断言不依赖 L2 采样」— 若 L2 总运行且与 L1 union, fixture pin 住 L1 命中 2 tag 后 L2 仍可采样性追加第 3 个 agent 未持有的 tag → \|required_caps\|=3 → match_rate 2/3=0.67 → R-a 不触发 → AC-1「auto 直派」跨采样可翻车。pin 只约束了 L1 命中, 没有封住分母。
**修法**: 显式成文复合规则, 推荐 L1-first-else-L2 (L1 命中 ≥1 → required_caps=L1 结果, L2 不运行), 与 B3 确定性优先及 L1/L2 召回分工刻画自洽; 选 union 则须另定 fixture 禁 L2 机制。

**R2-CR-2 (testing, AC-2(b) + AC 总注) — 无区分力测试 + 决策路径断言无字段载体** [fix-introduced]
AC-2(b) 参数 1/1=1.0 vs 插件 0.90: 差值恰 0.10, 按 R-b「≤0.1 → 降级」, 即使单标签禁令完全没实现, 差值护栏也独立产生相同可观察结果 (status=recommend) — 该 AC 对「单标签禁直派」零证伪力, 假绿测试。连带: AC 总注声称按「决策路径 R-a/R-b」断言, 但 §3 输出契约只 additive 加 `agent_source`, auto_match/recommend schema (SKILL.md L147-181) 无决策路径字段 — AC-2(b) 路径归因与 AC-5「仍进候选池」均无机械读取载体。
**修法**: (a) AC-2(b) 插件对手降至 ≤0.85 (差值 >0.1) 使禁令成为唯一降级原因; 且/或 (b) §3 加 `decision_path` 字段 (R-a/R-b-margin/R-b-single-cap-block/R-c/baseline)。至少做 (a)。

**R2-CR-3 (architecture, §2.4 R-b) — 差值边界 ≤0.1 vs 既有 <0.1 翻转 + 适用范围自相矛盾, 波及 AC-3 零回归** [fix-introduced]
ROUTING_RULES L198 既有规则 = 「差值 **< 0.1** 降级」; R-b = 「差值 **<= 0.1** (含 0.1) 降级」— 差值恰 =0.1 (0.95 vs 0.85; 1.0 vs 0.90) 行为相反。§1 step 5 声明「决策规则重新成文」且流程图把 R-b 作为 auto 数值路径本体 (不限跨池), 而 §2.4 关系段又说「§优先级处理管…插件级互相差值降级; §CAP 管跨池」— CAP 候选在池但 top-2 均插件级、差值 0.1 时两处给出相反裁决。且 3e 关闭 (AC-3 三支) 时若 step 5 新文本生效, 0.95/0.85 场景基线直派 (0.1 不满足 <0.1) 而 R-b 降级 → 「结构化字段级一致」结构性可失败, 触 Rule #4。
**修法**: (a) R-b 差值护栏显式限定「比较对中含 CAP 候选」, 纯插件级 top-2 (含 3e 关闭时整个 step 5) 沿用既有 <0.1; 或 (b) 全局统一 ≤0.1 + 同步改 ROUTING_RULES + B6/AC-3 显式注明有意变更并论证。

**R2-CR-4 (architecture, §CAP 评分范围) — 插件级 capabilities 不参与评分的裁决缺失** [新鲜扫, R1 五人漏网]
grep 实证: **全部 11 个插件级 agent (aria/agents/*.md) 都有 capabilities 机读字段** (US-011 AC-8 前置交付, 如 backend-architect: `[api-design, database-schema, microservice-architecture, performance-optimization, service-boundary]`)。§CAP 却只「产出项目级候选」、R-a 资格限项目级 — 不对称全文未论证。更要害: §393 既有 prose L401-404「3. 合并: 项目级 Agent 加入候选列表 / 4. 执行路由匹配 (FP/TT/关键词 **+ capabilities**)」— step 4 字面作用于合并后列表 (含插件级), 与 §CAP 限项目级直接冲突 → 实施分歧点 (两种读法产出不同 confidence 值与 recommend 排序)。
**修法**: 加一条显式裁决 (推荐: 插件级 capabilities 不参与 §CAP 评分 — 其路由信号已由四表人工标定承载, CAP 通道专属无人工标定规则的项目级 agent), §393 改写时同步限定 L404 该句。

**R2-CR-5 (architecture, 同名保护与全局最高复合 — 沿用 R1 450102ae scope) — 「替换」得分归属未定义, 关闭不完全**
Rev1 给了顺序 (「候选池构建期先按名去重…之后才进评分」) 但「项目级**替换**插件级候选」未定义被替换者已获得的 FP/TT 得分归属。移除读法下: 同名项目级 agent 若 CAP 零命中, 失去插件级 FP/TT 高分条目后**整体出局** — 而 SKILL.md L419 既有语义是「覆盖了插件级**路由**」(定义指向替换, 非删除得分信号), L420「项目级优先」— 优先不等于消失。两种读法路由结果差异巨大, AC-3 三支不覆盖同名场景。另注: 「(D9 语义保留)」引用不精确 (见 R2-CR-6)。
**修法**: 3e 同名 bullet 补得分归属: 替换 = 候选身份/定义/agent_source 指向项目级, 已获 FP/TT/技术栈/关键词得分保留, CAP 得分另评后取 max (与 §416 语义一致); 或显式声明移除语义并论证。

### Minor (7)

- **R2-CR-6 (documentation, §1 3e)**: 「D9 语义保留」引用失准 — archive D9 原文 (adapter proposal L195) = 「警告 + **显式确认**」; Rev1 描述保留的实为 SKILL.md §416 实现语义 (警告+项目级优先+plugin_only, 无确认)。auto 直派同名替换后的项目级 agent 无确认环节与 D9 字面不符 (既有实现已如此, 预先存在)。→ 改引 §416 或注明差异。
- **R2-CR-7 (testing, 后续段)**: Rule #6 处置声称 deterministic/structural substitute, 但同文 B3 定位 agent-router 为半确定性 prose Skill (L2 为生产常态) — 表面张力未消解。substitute 有 shipped 先例 (augmentation v1.48.0 同为 prose skill 行为改造) 且本 change 验证对象是结构性契约接线, 适格可论证 → 补一句论证即可。
- **R2-CR-8 (documentation, Resolved 表)**: 1d35911a 在第 5 行与第 14 行重复计入 — 表内 id 恰 39 但 unique 38, 「39 deduped findings」计数存疑; f2a4ac9a (表) vs f2a4a9a (§6) 拼写不一致。→ 与 R1 去重清单对账。
- **R2-CR-9 (implementation, §4/§5)**: per-file stat 每次比对使既有 `cache_ttl_seconds` (SKILL.md L431 注释「0 = 仅 mtime 失效, >0 = 时间失效」) 语义悬空, 而 §5 template 补的 3 key 含它; v1.1.0 旧 schema 缓存文件的处置 (视为失效重建) 未写。→ §4 补两句。
- **R2-CR-10 (implementation, §2.3)**: match_rate=0 候选是否入池未成文 — AC-2(a)「零命中不进决策」与 Impact「无命中不变」隐含不产出, 但 §CAP 正文无「matched 为空 → 不产出候选」规则。→ 补一句。
- **R2-CR-11 (documentation, §2.1 L1)**: task_type 默认「自动推断」(SKILL.md L136) 且 subagent-driver 集成调用 (L253-260) 不传该参数 — 生产上 L1 主命中面输入值可能本身是 LLM 推断产物, 「机械可复算」定语仅显式传参时完全成立。→ L1 行补注边界; fixture 显式传参不受影响。
- **R2-CR-12 (documentation, §6)**: 维护指南枚举「→ 四类含 CAP」延续既有漏项 — 文件实有 FP/TT/关键词/技术栈四表而既有枚举漏技术栈; 本 change 触碰该行, 应为五类顺带补齐。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical + 5 Major + 7 Minor) → **vote: REVISE**

Rev1 是高质量修订: R1 两大 Critical 的解法 (两级闭集 / R-a 序数前置) 数学成立、方向正确, 我维度 7 条 R1 findings 无一纸面关闭, 引用精度显著优于 Rev0。剩余问题全部是新机制的边缘完备性 (L1/L2 复合、差值边界归属、同名替换得分、插件级 capabilities 裁决) 与 AC 可证伪性 (AC-2(b) 无区分力、决策路径无载体), 均为局部补文, 不推翻分层决策骨架 — 收敛在望, 建议 Rev2 后可直接进 A.2。

## 核验锚点

- openspec/changes/agent-router-auto-project-agent-injection/proposal.md:1-253 (Rev1 全文含 Resolved 表)
- aria/skills/agent-router/SKILL.md:1-13, 17, 132-141, 145-201, 205-246, 250-273, 277-289, 393-434 (含 399-406 机制图 / 416-421 同名保护 / 425-434 配置), 449
- aria/skills/agent-router/ROUTING_RULES.md:3, 146-168, 172-186, 190-201, 251-259
- aria/references/capabilities-taxonomy.yaml:1-4, 136-145
- aria/skills/subagent-driver/references/handoff-contract.md:14, 33
- docs/requirements/user-stories/US-011.md:5, 40, 43, 51, 61
- .aria/config.template.json:1-72 (确无 agent_router 块)
- openspec/archive/2026-04-11-agent-project-adapter/proposal.md:188-197 (D4 L190 / D9 L195)
- openspec/archive/2026-06-21-agent-team-audit-project-agent-augmentation/proposal.md:16
- openspec/changes/aria-2.0-m7-agent-lifecycle/proposal.md:129, 244
- aria/agents/*.md (11/11 含 capabilities 字段; backend-architect 样本核验)
- aria/.claude-plugin/plugin.json:4 (现值 1.53.0)
- .aria/audit-reports/post_spec-R1-1783541662234-agent-router-injection-code-reviewer.md (R1 基线)
- 本 Aria 项目 .aria/agents/ 确不存在 (AC 总注 fixture 前提属实)