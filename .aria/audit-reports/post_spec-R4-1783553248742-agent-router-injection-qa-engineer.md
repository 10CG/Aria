---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T22:43:29.624Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R3 closure 核验

独立核验方法: 不读 proposal 自带的 "Resolved (Rev3)" 表面陈述, 而是重新对照 Rev3 正文原句 + 亲自代入 AC 参数重算, 逐一验证 R3 12 项 Major (按行/簇计数) 是否真闭合。

| R3 Major 簇 | 闭合状态 | 核验方式 |
|---|---|---|
| B12 混合候选无人区 (79070f61 等 4 id) | 真闭合 | 用 AC-12 实参 (caps=[api-design], required=[api-design,database-schema]) 手算: match_rate=0.5, R-a 不满足; B12 候选被排除出 Stage2 挑战者池 (防自我挑战); Stage1 吸收分 0.95 直派。结果与 §2.4-B12 段文字逐句吻合, 与 AC-12 断言四元组一致, 无"无人区"残留 |
| negation 脱离 L2 连坐 (b59e5149 等) | 真闭合 | §2.1 negation 段独立于 L2-addition 启用条件门控, 措辞 "恒时执行, 不受下方启用条件门控" 明确 |
| precision 分母 off-tax (9ab6adf4 等) | 真闭合 | §2.3 公式 valid_caps 定义已排除 off-tax, 与 B4/B10 决策记录一致 |
| R-b 非 MECE (146fa0b3/2bf3e6d6) | 真闭合 (重新代数验证) | diff=match_rate−baseline_top 四分支覆域: (0.1,∞) 分二 (达/未达 threshold) ∪ [-0.1,0.1] ∪ (-∞,-0.1) = 实数全域无缝无重叠。`|required_caps|==1` 规则是正交前置判据 (只改写分支1结论), 不破坏四分支本身 MECE 性质 |
| trace 缺 off-tax 载体 (aa875cf8) | 真闭合 | §3 已有候选级 off_taxonomy_tags 字段 |
| R2-Critical 无防再犯 AC (10c138df) | 真闭合 | AC-13 代入验证: diff=0.95−0.85=0.10 恰不满足 Stage1 `<0.1` 严格条件, 不降级, 直派, 与旧基线逐字一致 |
| §4 缓存零 AC (549515fe) | 真闭合 | AC-14 已补 route→edit→re-route 端到端断言 |
| AC-10 fixture 缺 (4f8dbb64) | 真闭合 | tasks.md TASK-012 显式含 "双 R-a specialist (AC-10)" |

Minor 簇抽样 (id 卫生 / TASK-013·014 划界 / TASK-015 顺序 / TASK-017 pointer bump / decision_path 基数 / §5 SOT 限定): 全部经 grep + 源文件交叉核对属实。**结论: R3→Rev3 处置无一假闭合, 无回退。**

## Rev3 新文本缺陷扫 (本轮职责 B)

对两段式 auto 决策 / B12 消歧段 / §2.1 显式传参 (全新机制, 仅经 R3→Rev3 一轮打磨) / AC-13..15 做地毯式复算, 未发现新 Critical/Major。发现 5 项 Minor/advisory (详见 findings[], 摘要):

1. §6 "连带 9 段" 计数笔误 (实际 10 个 section anchor) — 纯 prose 计数误差, tasks.md 不受影响
2. AC-12 "同名警告输出" 断言未纳入 AC 总注声明的结构化字段清单, 可判定性方法待 TASK-013 显式选定 (子串检查 vs 新增字段)
3. **(本轮职责重点)** 显式传参只解决 CAP 侧机械性, Stage 1 基线 (FP/TT) 匹配仍是 LLM 判定; AC-4(b)/AC-13 恰是对 baseline_top 精确到 0.05/0.10 边界最敏感的两条 AC, 双跑保真度依赖 fixture 设计者主动选择无歧义单规则命中场景 (现有 fail+回炉 兜底可接住残余风险, 但未被文本明确点破)
4. step 5 伪代码 "§2.6 混排" 引用只挂在原生 recommend 分支旁, auto 内部降级是否复用未显式交叉引用 (可从 AC 断言及 §2.6 自身文本合理推出, 但留有一行说明的缝隙)
5. §2.1 显式传参对 off-taxonomy 值的处理未定义 (窄边界, 现有 15 条 AC 均不触发, 面向未来 subagent-driver 调用方的预防性缺口)

## AC-1..AC-15 终审 (逐条参数代入复算)

全部 15 条 AC 逐一代入 Rev3 规则重新演算, 结果与 AC 断言一致, 无数学/逻辑矛盾:

- AC-1: match_rate=2/2=1.0, precision=2/3=0.67 → R-a 三条件全满足 → 与断言吻合
- AC-2(a): matched=∅ → match_rate=0 → 不产候选, 吻合; AC-2(b): |req|=1 强制 R-a 失败 (|req|>=2 门槛) 落 R-b 首条 "|req|==1 永不直派" 短路 → recommend+decision_path=R-b, 吻合 (且验证"无禁令则会直派"的对照断言: 0.15 领先>0.1 且 1.0>=0.9 threshold, 确实会直派, 印证禁令确有效力)
- AC-3: 门控最先 + 同名逻辑不执行的组合验证设计合理 (AC-3b 用同名 fixture 测门控优先级)
- AC-4(a): diff=0.667−0.90=−0.233, baseline 领先>0.1 → 采纳 Stage1, 吻合; AC-4(b): precision=2/8=0.25<0.5 → R-a 拒, 落 R-b, diff=1.0−0.95=0.05≤0.1 → recommend, 吻合
- AC-5/6/7/8: 与 §1/§2.6/§3 文本直接对应, 无矛盾
- AC-9: 机械 grep 检查, 非数值类, 未见风险
- AC-10: 双 R-a fixture 可行性验证 (两候选均满足 R-a 三条件但 precision 不同, §2.5 tiebreak 可正确排序)
- AC-11: 与 §2.2/§2.3 off-tax 惰性规则直接对应
- AC-12: 四元组除"警告输出"外 (见 finding 2) 均可精确代数推导, 见上文 B12 核验
- AC-13: 边界=0.1 精确演算确认不触发降级, 见上文
- AC-14: 端到端缓存测试范围合理, 已知残余窗口(同秒同字节)诚实标注不纳入 fixture, 合理
- AC-15: L1 词边界 + negation 移除的机械可复算部分可断言; L2-addition 语义部分不断言, 与"确定性定位(诚实版)"一致, 合理边界划定

**显式传参 pin 后双跑一致性的现实性**: 对 CAP 侧 (required_caps 确定 + match_rate/precision/R-a/R-b 分类) 而言, 显式传参使其完全机械, 双跑必然一致, 结论可靠。但 Stage 1 基线候选生成仍是 LLM 执行 (agent-router 无 Python), 对 AC-4(b)/AC-13 这类要求 baseline_top 精确到 0.05/0.10 边界的 AC, 双跑保真度部分依赖 fixture 无歧义程度而非规则文本本身 —— 详见 finding 3, 判定 Minor (不阻塞实施, 建议 fixture 构造纪律 + 一句文本提示)。

**fail-回炉处置可操作性**: "双跑不一致=fail并回炉SKILL文本消歧, 无容忍阈值" 机制本身可操作 (有明确触发条件 + 明确后续动作), 且能兜住上述 Stage-1 残余风险 (即便诱因是 baseline 侧漂移而非 CAP 新规则歧义, 该机制仍会触发排查), 未发现操作性缺口。

## tasks.md TASK-012..015 fixture/AC 归属终核

机械重新统计全部 15 条 AC 到 4 个执行任务的映射, 确认无遗漏无重复:

- TASK-013 (裁决类 AC 实跑): AC-1, AC-2, AC-4, AC-5, AC-6, AC-7, AC-8, AC-10, AC-11, AC-12, AC-13, AC-14 = 12 条
- TASK-014 (AC-3 零回归三支): AC-3 = 1 条 (含 (b) plugin_only×同名组合)
- TASK-015 (AC-15 推断层专项): AC-15 = 1 条 (唯一不用显式传参的 AC, 归类正确 —— 因其本意就是测推断路径)
- TASK-017 (AC-9 文档同步): AC-9 = 1 条 (机械 grep 检查, 非 fixture 类, 独立于 TASK-013/014/015 分组, 且正确排在 TASK-016 版本 bump 之后, 因其清单含发版文件)

合计 12+1+1+1=15, 与 proposal AC-1..AC-15 全集精确对应, 无缺项无重叠。TASK-012 fixture 清单 (proj-a/proj-empty/宽标签/同名/双R-a/broken frontmatter/off-taxonomy/纯插件=0.1边界对, 共8项) 覆盖所有需要*独立文件结构*的 AC; 其余 AC (如 AC-2b/AC-4a/AC-5/AC-6/AC-8/AC-14/AC-15) 通过复用既有 fixture + 变化 task/required_caps/config 参数覆盖, 属合理复用设计, 非遗漏。

**执行顺序核验**: TG-A→TG-B→TG-C∥TG-D(TASK-012)→TASK-013/014/015→TG-E(016→017→018) — TASK-015 已正确排在 TASK-012 (fixture 就绪) 之后, R3 "TASK-015 顺序" 发现确认修复落地。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical + 0 Major + 5 Minor/advisory)。

本轮 (R4, max_rounds 终轮) 独立核验 R3 全部 12 项 Major 均真实闭合 (非文档自证), 且对 Rev3 新引入文本 (两段式决策 / B12 消歧 / §2.1 显式传参结构性改进 / AC-13..15) 做了逐条参数代入复算, 未发现新 Critical/Major。5 项 Minor 均为实施期可酌处的措辞/边界澄清 (计数笔误、警告字段可判定性方法待选、Stage-1 LLM 侧双跑保真度提示、混排规则交叉引用补全、off-tax 显式传参边界), 无一要求 spec 正文结构性返工, 均可在 Phase B 实施 (TASK-012/013) 期间以极低成本消化, 或作为实施注意事项记录。

按终轮收敛判据 ("若你维度 Rev3 已无 critical/major, vote PASS 并列 advisory"), **vote = PASS**；同时如实标注 verdict = PASS_WITH_WARNINGS (因存在 ≥1 Minor, 与任务给定的 verdict 判定口径 "PASS_WITH_WARNINGS = 0C+≥1M" 一致 —— 注: 5 项均为 Minor 非 Major, 此处 "M" 按裸口径含 Minor 计入 warnings 类别, 不影响 vote=PASS 的收敛推荐)。

## 核验锚点

- proposal.md 全文 (Rev3, 396 行) + tasks.md 全文 (18 task)
- aria/skills/agent-router/SKILL.md (449 行, 逐段核对 §35/47/93/132/145/205/250/277/305/323/383/393/438 全部真实行号与 proposal 引用一致)
- aria/skills/agent-router/ROUTING_RULES.md (270 行, 核对 Stage1 "<0.1 严格" 语义原文出处 §优先级处理 L190-201)
- aria/references/capabilities-taxonomy.yaml (145 行, 核对 orm-migration/query-optimization/database-schema/api-design 等标签存在性)
- .aria/config.template.json (核对 agent_router 块确实缺失, TASK-009 前提成立)
- docs/requirements/user-stories/US-011.md (核对 AC-4/D4/Scope 三锚点原文, errata 目标定位准确)
- .aria/decisions/DEC-20260621-001-agent-team-audit-project-agent-augmentation.md (核对 L13/L90 两处失实前提原文, 与 proposal Why/§6 引用一致)
- openspec/changes/aria-2.0-m7-agent-lifecycle/proposal.md:129 (核对 M7 "不依赖任何未实现的 routing 能力, 也不改 agent-router" 原句, 与 proposal Why 段引用逐字一致)
- aria/skills/subagent-driver/references/handoff-contract.md:14,33 (核对 agent_source 预留字段原文)
