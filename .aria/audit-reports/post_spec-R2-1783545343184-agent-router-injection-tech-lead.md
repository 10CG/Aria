---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T20:29:09.457Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R1 closure 核验 (tech-lead 维度, 对源文件核验非信 Resolved 表字面)

| R1 finding | Rev1 声称处置 | 核验结论 |
|---|---|---|
| **C2 数学冲突** (d378eb8a/af713ec5, 黄金场景恒降级) | §2.4 R-a 决定性直派前置豁免差值护栏 | **真关闭 (机制层)**。逐 AC 推演: AC-1 (match_rate 1.0, \|req\|>=2 → R-a 触发, 不入差值护栏); AC-5 (0.95 插件在场, R-a 满足项目级仍可胜出 → 堵短路); AC-4 (R-a 不满足→R-b 护栏)。R-a 绕过 B5 差值护栏, 黄金场景不再恒降级。C2 具体冲突已消解。 |
| **required_caps 无确定性来源** (Critical, 3-agent 收敛) | §2.1 两级闭集 + B3 半确定性定位 + fixture pin | **真关闭 (诚实重构)**。「半确定性」+ L1 机械可复算 + L2 闭集受约束 + fixture pin 输入 = 撤回 Rev0 over-claim, 非画饼。 |
| **同名保护与全局最高复合未定义** (450102ae) | §1 3e 复合顺序: 池构建期按名去重项目级优先, 后评分 | **纸面关闭**。只定义了「顺序」, 未定义幸存同名候选是否继承插件级 FP/TT 分数 / agent_source 取值 → R-b 数值裁决与 §3 输出仍未定义 (Finding 3)。 |
| **量纲失配 + 单标签饱和抢占** (92358876/24b743aa/f8c242e4) | §2.4 R-a 序数 + R-b 单标签禁直派 + 边界≤0.1 | **部分关闭 + 新洞**。\|req\|==1 单标签饱和已由 R-b 禁直派关闭 (AC-2b); 但 R-a 的 \|req\|>=2 宽标签劫持面是 fix 新开的同类洞 (Finding 1)。 |
| **跨池同分 + 「与既有一致」不实** (0c20a9e0) | §2.4 R-c + 与优先级处理分工 cross-ref; B4 范围限定 | **真关闭**。R-c 精确同分降级 + B4 限定项目级互相 + 显式 cross-ref, 措辞不再声称「一致」。 |
| doc-sync / M7 / US-011 / agent_source 引用 (非本 lens 主战场) | §6 全量扩定 / Why 重写 / errata | 抽查核实: M7 L129 表述**准确** (M7 不依赖/不改 agent-router, pin v1.1.0); handoff-contract.md:14,33 `agent_source` 预留字段**属实**; audit-augmentation 归档 L16「triage 已确认会扫」被本 change 正确指认为「对 auto 路径为假」= 准确诚实。 |

**小结**: R1 两大 Critical 机制层真闭合, closure 质量有 4 处 rework (纸面关闭 450102ae + fix 新开 92358876 变体 + rationale 自相矛盾)。

## 审计结论 (新 finding, 均带 file:§ 证据)

### Major

**F1 (risk) — R-a 宽标签项目级 agent 劫持面 [FRESH, 角色核心问题]**
§2.4 R-a (L99-103) 只查 `match_rate==1.0 AND |required_caps|>=2`, 不对候选自身能力宽度设精度门。`match_rate=|matched|/|required_caps|`, ==1.0 仅要求 `agent.caps ⊇ required_caps` — 标签越宽越易成 required 超集, match_rate 越易 1.0 (单调有利)。唯一防护 §2.5 精度 tiebreak (L117-119) 只在「多个满足 R-a」时激活, **单个宽 agent 无精度门**。角色问题「项目级 agent 标签齐全即可劫持一切匹配任务」= **成立**。不同于 R1 已关的 \|req\|==1 单标签饱和, 是 R-a 引入的 \|req\|>=2 新洞; Impact/Risk 表未登记。

**F2 (issue) — §2.4 rationale 自相矛盾: 断言量纲不可比却仍跨刻度比较 [FRESH]**
§2.4 (L96)「量纲不可直接互比」证成 R-a, 但 R-b 兜底 (L104-110) 以 match_rate 为 confidence 与 FP/TT 做差值护栏比较 = 正是被判无效的跨刻度数值比较; recommend (默认 mode) 按 AC-6 (L209) Top-3 同表排序亦然。真正硬理由是 §2.4 第二句 (match_rate 上限 1.0 对 >0.9 FP 差值恒<0.1→黄金场景恒降级), 有效; 「量纲不可直接互比」是 overreach 且被 R-b/recommend 自我否证。这是 C2 closure 核心 rationale 的内部不一致。

**F3 (issue) — 同名去重的分数归属 + agent_source 未定义 [R1 450102ae 纸面关闭]**
§1 3e (L50-51) 只定义顺序 (池构建期项目级替换插件级→后评分)。FP/TT 规则按 agent 名匹配。项目级 `backend-architect` 遮盖插件同名时, 幸存候选是否继承 FP 0.95 → R-b 直派 vs 仅 recommend, 两解读相反, 无 AC 锁定; §3 要求的 agent_source 对被替换候选亦未明说。R1 Resolved 只答顺序未答分数归属。

**F4 (issue) — §4 per-file 缓存与既有 `cache_ttl_seconds` 未协调; §5「3 key」未枚举 [FRESH]**
SKILL.md L429-431 现有 3 key, 第 3 = `cache_ttl_seconds:0 // 0=仅 mtime 失效`。§4 (L136-139) 无条件 per-file 比对取代目录 mtime, 未提 TTL 存废; §5 (L143-144)「3 key」只点名 2 个。该注释在 per-file 模型下事实错误却不在 AC-9 doc-sync 清单内。实施者无从判定第 3 key 命运 → 可能保留旧 mtime 语义, 重开本 change 要修的 staleness 类 (§4 存在的唯一目的), 亦违 Rule #4 对既有 key 语义的澄清义务。

### Minor

- **F5 (issue)** — §3 (L123) 把 agent_source 加到 manual 输出, 但 manual 在 step 2 (SKILL L216-219) 于 3e 扫描前前置 return (Impact L186), user 手工点名项目级 agent 时源层无从判定; AC-8 只覆盖 auto_match/recommend。
- **F6 (issue, testing)** — B4 精度 tiebreak (§2.5) 与 B10 off-taxonomy 零分 (§2.2) 均无对应 AC (AC-7 只验 frontmatter 边界不含 taxonomy 外标签; AC-1 只验单候选 R-a)。精度 tiebreak 恰是 F1 唯一防护却无测试锁定。
- **F7 (issue)** — B6 (L172)「逐字段等同基线」与 §3 (agent_source additive 加到基线输出) 矛盾; AC-3 (L206「agent/status/confidence 字段级一致」) 才是准确口径。
- **F8 (issue, doc)** — Why (L28) / Risk (L189)「I/O 契约不变」与 §3 additive 增 agent_source 输出字段不符; 虽对 M7 无害 (不消费 routing 输出), 措辞应改「input 不变 + output additive」。
- **F9 (decision)** — Level 2 定级处 2/3 边界: §CAP 全新评分算法 + R-a/R-b/R-c 三层决策 + 新输出契约 + 缓存 schema 变更 + Estimation 已列 5 工作流, 且工作流下一步计划 A.2/A.3/post_planning (隐含 tasks.md), 与 Level 2「无 tasks.md」张力; 需显式论证或升 Level 3。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical + 4 Major + 5 Minor)。**vote: REVISE** (存在 Major, 必 REVISE)。

Rev1 对 R1 两大 Critical 的机制层是真修复 (R-a 消解 C2 数学冲突, §2.1 诚实重构 required_caps), 方向正确不推翻。但 closure 质量与 fix-introduced 新缺陷需再一轮: F1 (R-a 宽标签劫持, 角色核心风险面无防护)、F2 (§2.4 rationale 自相矛盾)、F3 (450102ae 纸面关闭)、F4 (缓存 config 未协调) 四条 Major 须 rework 后方可进 A.2。

## 核验锚点

- proposal.md §2.4 R-a/R-b/R-c (L96-113) — F1/F2/F3 决策规则源
- proposal.md §1 3e 同名保护 (L50-51) / §2.5 tiebreak (L117-119) — F1/F3
- proposal.md §3 (L121-130) / §4 (L132-139) / §5 (L141-145) — F3/F4/F5
- proposal.md AC-3/AC-6/AC-7/AC-8 (L206-211) / B6 (L172) / Why L28 / Risk L189 — F2/F6/F7/F8
- SKILL.md L429-431 (3 config key 含 cache_ttl_seconds) / L216-219 (manual step 2) / L62,139,239 (recommend 默认) / L286 (max_candidates:3) / L17,393,449 (三处版本)
- subagent-driver/references/handoff-contract.md:14,33 (agent_source 预留字段, 核实属实)
- aria-2.0-m7-agent-lifecycle/proposal.md:129 (M7 Why 表述, 核实准确)