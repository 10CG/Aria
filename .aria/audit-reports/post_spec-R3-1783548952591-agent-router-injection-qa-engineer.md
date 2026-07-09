---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T21:49:32.103Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R2 closure 核验

对源文件逐条核验 (不信 Resolved 表字面):

- **R2 唯一 Critical (1a1d3115/1ba6f643)**: proposal.md:139-141 明文"纯插件级候选之间...差值<0.1严格...一字不改", 已用 Bash 比对真实 `aria/skills/agent-router/ROUTING_RULES.md:198` 确认既有 `<0.1` 严格边界字面未被触碰 —— **规则文字层面确认真关闭**。但深挖 AC 层发现该修复缺乏验收锁定: 12 条 AC 无一显式构造"纯插件 diff 恰=0.1"边界 fixture (见下 Major finding 2), textually-closed 不等于 regression-proof, 这是本轮新抓的残留风险。
- 其余 R2 Major/Minor findings (R-a precision 门 eabedb99 / rationale 重写 ab462321 / L1-L2 编排 cf4aa23e 系 / task_type 事实修正 f3677340 / R-a 覆盖面 762b7952 / 缓存完整化 97cb686e 系 / B11 裁决 c0e74580 / step5 三分支 2b6e2b60 / 文档清单 be54898b 系 / D9 语义归因 bac15556 系 / agent_source 收窄 e16ad9fc 系 / AC-2b 参数 91c8e97b 系 / recommend 排序 308d52af / US-011 锚点 6eba1f5c / B6 口径 5e88d186 / Level 3 升级 822165ba) 经逐条对文本 + 对真实 SKILL.md/ROUTING_RULES.md/taxonomy.yaml/US-011.md/DEC 文件核验 (含实地 grep/Read 验证行号锚点), **均已正确落地**, 未见纸面关闭而实质未关的情形。
- 已用 Bash 核对环境锚点: 主仓 SHA `2067ddf`、aria 子模块 SHA `93b7406` 与任务声明的 source_sha 一致; `.aria/config.template.json` 确认无 `agent_router` 块 (TASK-009 依据成立); `.aria/agents/` 目录确认不存在 (AC 总注"本项目无.aria/agents/"属实); US-011.md 的 AC 项 4/D4/Scope 三处锚点、DEC-20260621-001 的"router 已实现"表述均确认存在且与 proposal 描述一致。

**结论**: R2 的显式 findings 全部真实关闭; 但本轮 (R3) 在"关闭点周边"发现 6 处 Major 级新缺口 —— 均是 Rev2 新引入或大改的机制 (R-b 决策树 / B12 吸收 / 缓存 / off-taxonomy trace) 缺乏与之匹配的验收覆盖, 而非规则文字本身的错误。

## 审计结论

本轮聚焦点为 (A) R2 closure 核验、(B) Rev2 8 项新机制的边界推演、(C) AC-1..AC-12 与 tasks.md TG-D 的可实施性核对。三重职责均已执行, 结果:

**新发现 6 处 Major (均为 R3 新抓, 非 R1/R2 已处置项的复发)**:

1. **R-b 三分支非 MECE**: "项目级候选领先>0.1但自身match_rate未达threshold"这一输入组合未被 R-b 任何分支覆盖, 行为未定义 (proposal.md:135-138)。
2. **护栏 Critical 修复缺验收锁定**: 无 AC 显式钉住"纯插件候选 diff 恰=0.1"边界, R2 唯一 Critical 的"防再犯"没有测试层保障; 附带 AC-4 两半均未像同类 AC 那样显式给出 decision_path 期望值。
3. **B12 吸收分与 §2.4 决策公式接口未定义**: R-b 明文"以match_rate为confidence"未对同名吸收场景给出替代口径, 吸收值若只影响展示不影响决策, B12 rationale 声称的"防回归"目标在决策层面未必成立; AC-12 也未钉住项目候选自身 CAP 为部分匹配 (非 R-a-qualifying) 的 fixture, 存在被"简单化实现"回避核心问题的风险。
4. **tasks.md TASK-012 fixture 清单缺 AC-10 所需第二个 R-a 合格候选**: 现有 6 类 fixture (proj-a/proj-empty/宽标签/同名/broken frontmatter/off-taxonomy) 中宽标签被 R-a 自身拒绝、同名会引入 B12 干扰, 均不能干净充当 AC-10 tiebreak 的第二候选, TASK-013 现状无法实施 AC-10。
5. **off-taxonomy trace 提示无 schema 归属**: AC-11 测的是 agent 侧 off-taxonomy 标签, 但 §3 required_caps_trace 的 l1/l2/negated 三键全部服务任务侧推断轨迹, 两个数据域不匹配, 现有 schema 无字段可承载该断言。
6. **§4 缓存机制 (汇总 5 个 R2 finding 的最大改动区之一) 零 AC 覆盖**: AC-1..AC-12 无一处涉及缓存行为, 原始"对原地编辑不敏感"bug 修复后若实现阶段复发, 现有验收标准无法探测。

**Minor (3 处, advisory, 不阻塞收敛)**:
7. negation 机制 (§2.1-e, R2 新增) 零 AC 覆盖, 虽与 L2 共享既有豁免 rationale 但未被明确点名。
8. B12 同名吸收 + plugin_only 门控的组合无显式 fixture (架构上应安全, 但缺乏显式回归测试)。
9. "双跑一致"要求叠加多子场景后实际调用量较大 (20+次 LLM 执行), 且未定义不一致时的处置 SOP。

**AC-1..AC-12 逐条核对结论**: AC-1/AC-2/AC-3/AC-5/AC-7/AC-8/AC-9 与 Rev2 规则对齐、fixture 可构造、断言可判定, 未见新问题。AC-2(b) 的 0.85 参数在 R-b 语义下推演正确 (|required_caps|==1 的单标签禁令在数值比较之前拦截, 与 R2 91c8e97b/4a3f5098 的修正意图一致)。AC-4 首半"0.67 vs 0.90 差值0.23>0.1→基线胜出"经推演数学自洽 (baseline top 0.90 恰好触及默认 threshold 0.9, 落入 R-b 第三分支"基线top领先→基线内部按既有规则裁决", 非该分支缺失导致的问题), 但如上 Major finding 2 所述, 该 AC 断言精度弱于同类 AC。AC-10/AC-11/AC-12 各自存在结构性缺口 (Major finding 3/4/5)。tasks.md TG-D 任务编号与 AC 编号范围 (TASK-013 "AC-1..AC-8+AC-10..12" 正确跳过归 TASK-015 单独处理的 AC-9) 核对无误。

**为何不因 R3 已是收敛轮而压低severity**: 上述 6 处 Major 均满足 (a) 有具体、可复现的输入/组合可构造失败场景, (b) 不是 R1/R2 已处置条目的重复 (tasks.md 本身是 Rev2 新增产物, AC-10 fixture gap 结构上不可能在此前轮次被发现; 其余 5 处均是"规则文字本身已修好"但"验收覆盖未跟上"的新角度), (c) 均有低成本、非推翻式的具体修复建议。故如实按 Major 报告, 不做人为降级凑 PASS, 也未把可随实施酌处的措辞类问题拔高为 Major (3 条 Minor 均标注为 advisory)。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical + 6 Major + 3 Minor) — **vote: REVISE**。核心决策规则 (R-a/R-b/R-c/B1-B11) 文字层面自洽且 R2 Critical 确认真关闭, 不构成 FAIL; 但 6 处 Major 集中在"新机制/新产物 (B12吸收/缓存/tasks.md fixture/off-taxonomy schema) 的验收覆盖未跟上规则改动幅度", 建议 Rev3 补齐后再入 A.2, 而非直接放行仅靠 Phase B 实施阶段自由裁量弥补 —— 尤其 finding 2 (护栏 Critical 缺验收锁定) 和 finding 6 (缓存零覆盖) 涉及本 change 改动面最大、风险面最集中的两块, 不建议降级为 advisory。

## 核验锚点

- `proposal.md:135-141` — §2.4 R-b 三分支决策 + 纯插件裁决声明 (findings 1/2)
- `proposal.md:51-56` — §1 3e 同名保护复合 / B12 吸收机制 (finding 3)
- `proposal.md:92-93` — §2.1-e negation 子规则 (finding 7)
- `proposal.md:168-175` — §3 required_caps_trace schema (finding 5)
- `proposal.md:181-197` — §4 缓存失效修复完整段 (finding 6)
- `proposal.md:270-281` — AC-1..AC-12 全文 (逐条核对基础)
- `proposal.md:355` — 后续段 L2 不确定性隔离 rationale (finding 7 对照)
- `tasks.md:28-29` — TASK-012 fixture 清单 / TASK-013 AC 范围 (finding 4)
- `aria/skills/agent-router/ROUTING_RULES.md:190-201` — 既有 <0.1 严格边界实代码基线 (R2 closure 核验用)
- `aria/references/capabilities-taxonomy.yaml:1-4` — 消费者头注释现状 (grounding 核验用)
- 环境锚点已验证: 主仓 SHA `2067ddf` / aria 子模块 SHA `93b7406` 与任务声明一致; `.aria/agents/` 不存在、`.aria/config.template.json` 无 `agent_router` 块均属实
