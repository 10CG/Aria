---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T21:33:39.771Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R2 closure 核验

**R2 Critical 1a1d3115 + 1ba6f643（差值边界静默改 + 波及纯插件路由）**：在我负责的「池含项目级但项目级非 top-2 时，纯插件 top-2 差值裁决用哪条规则」维度上，**真实关闭**。用两组数值推演验证 §2.4 R-b 三分支结构：

- 例1（基线 A=0.95, B=0.80, 项目 C=0.83）：C 与基线 top（A）差值 0.12 > 0.1 → 不落入新 `<=0.1` 降级分支 → 落到第三分支「基线 top 领先 → 基线内部按既有规则裁决」→ 单独用 A、B 走既有 `<0.1` 严格规则（0.15 差值不触发降级）→ A 胜出，**与池中不存在项目候选时的结果完全一致**。
- 例2（基线 A=0.95, B=0.87, 项目 C=0.30）：C 与基线 top 差值 0.65 > 0.1 → 同样回退基线内部，A、B 按既有规则（0.08 差值 < 0.1 触发降级）→ 降级 recommend，**同样与纯基线结果一致**。

两例都确认「纯插件级候选之间沿用既有 <0.1 严格边界」在文本层面已经可以正确落地，不受候选池是否混入项目级候选影响；此前担心的「仍有歧义」在这版文本的三分支结构（项目领先>0.1 直派 / 差值<=0.1 降级 / 基线 top 领先转既有规则）下已被消除。

**R2 eabedb99（R-a 宽标签劫持 / precision 门）、cf4aa23e+5e35cfee+ad935a3a（L1/L2 编排未成文）、596796f6 一族（同名得分归属）**：三项在「R2 字面要求」层面都已落地——precision 门已加入 R-a、L1/L2 编排算法已成文、B12 已定案得分归属规则。但本轮把这三项新机制放到一起做边界推演后，**各自暴露出一个 Impact/Risk 表未登记覆盖的新缺口**（见下方 findings A/B/C）。定性为「R2 要求已落地，但落地内容自身产生了 R3 该抓的新洞」，不是「R2 未关闭」——这与 R1→R2 时「双 Critical 真关闭，但抓到 Rev1 fix-introduced 洞」的模式是同一性质，符合收敛审计的预期节奏。

## 审计结论

在我的三条角色侧重上分别得出：

1. **R-b 零回归恢复**：closed（见上）。
2. **L2 |L1_hits|<2 启用边界**：编排算法本身自洽（`required_caps = L1_hits ∪ L2_additions − negated`, 门控 `|L1_hits|<2`），Risk 表也已登记「漏召」这一半（§252）。但**negation 被和 additions 捆在同一开关下**是一个新问题：negation 的存在理由是纠正 L1 字面机械匹配的假阳性（如否定语境），却恰好在 L1 富命中（>=2，字面误命中概率客观上更高）场景下最不可用，Risk 表未登记这个对称风险（Major，见 finding B）。
3. **precision 门数学**：`precision = |matched| / |normalize(agent.capabilities)|` 的分母是否含 off-taxonomy 标签未定义。若按字面「identity 保留」实现，分母会计入 off-taxonomy 标签，使一个持有无关自造/遗留标签的真 specialist 的 precision 被稀释，可能跌破 R-a 的 0.5 门槛——与 B10「零分」（不参与评分）立意冲突（Major，见 finding A）。agent-gap-analyzer 没有 precision 概念可比对，说明这是本 proposal 原创公式，之前没有先例校验。
4. **缓存 TTL 重定义与旧缓存迁移**：Impact 表已明确「旧缓存内容 schema 升级…旧缓存直接重建」，是充分的迁移路径声明；且 v1.1.0 时代 auto 路径从未真正消费该缓存（Why 段自述），历史脏缓存的实际风险面很小。**未发现新问题，视为已妥善处置**，未列为 finding。

新增一项跨机制组合发现（B12 × §2.4，均为 Rev2 内容，非某一方单独的锅）：同名吸收后的候选是「一体两分」（absorbed 基线 confidence + 自身 CAP match_rate），但 §2.4 R-a/R-b 仍以两个不同候选人的框架书写，两种可能读法（absorbed 分数独立参与比较 / 只做展示不参与决策）都存在问题，其中一种直接违背 B12 自己的 rationale（Major，见 finding C）。

另有 2 项 minor（advisory，可随实施酌处，不阻塞收敛）：R-b 场景下多个未满足 R-a 的项目级候选如何选代表比较、decision_path 在 recommend 语境下对非胜出候选的取值口径。

## Verdict

**PASS_WITH_WARNINGS**（0 Critical + 3 Major + 2 minor）。vote = **REVISE**——三项 Major 都是 Rev2 新增/修订机制自身的组合缺口（precision 公式 × off-taxonomy identity 保留；negation × L2 门控；B12 得分吸收 × §2.4 两方比较框架），不是对已被 R1/R2 关闭问题的重开，符合本轮「B. Rev2 新机制审计」的任务边界。三项都有具体数值/文本推演支撑，非猜测性质；均建议在 Rev3 补一到两句明确口径/子规则即可收口，预计不需要结构性重做。

## 核验锚点

- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md:105-116`（§2.2 归一语义 + §2.3 评分公式，precision 分母口径未定义处）
- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md:119-146`（§2.4 auto 决策规则分层，R2 1a1d3115 闭合验证处 + B12 消费处）
- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md:80-101`（§2.1 L1/L2 编排算法，negation 门控耦合处）
- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md:44-59`（§1 step3 3e，B12 同名保护复合原文）
- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md:152-161`（§2.6 recommend 混排，decision_path 归属处）
- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md:241-254`（Impact/Risk 表，风险披露完整性核对基准）
- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md:266-281`（AC-1..AC-12，AC-11/AC-12/AC-6 断言范围核对）
- `openspec/changes/agent-router-auto-project-agent-injection/tasks.md:26-31`（TG-D 验证任务与 AC 对齐核对，未发现缺口）
- `aria/skills/agent-router/ROUTING_RULES.md:190-201`（既有「差值<0.1 严格」优先级处理原文，R-b 零回归对照基准）
- `aria/skills/subagent-driver/references/handoff-contract.md:14,33`（agent_source 预留字段核实，与 proposal Why/§3 描述一致，无发现）
- `aria/skills/agent-gap-analyzer/SKILL.md:55-57`（match_rate 语义核对一致；该 Skill 无 precision 概念，佐证 finding A 是本 proposal 原创未经先例验证的公式）
