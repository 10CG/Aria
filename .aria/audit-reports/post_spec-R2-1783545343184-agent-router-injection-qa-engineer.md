---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T20:49:22.649Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R1 closure 核验

**两条 R1 Critical 已真实闭合 (非纸面)**:

1. `required_caps 无确定性来源` (6dc8588a/866a9c98/73eba2dc) — Rev1 §2.1 给出 L1(机械词边界)/L2(受约束语义补充) 两级闭集, B3 诚实定位为「半确定性」而非过度声称的「确定性」, 与 agent-gap-analyzer 语义边界划清 (required 来自单任务串而非 project-profile)。机制真实存在, 非仅措辞软化。
2. `B5 与 AC-1 黄金场景数学冲突` (d378eb8a/af713ec5) — Rev1 §2.4 R-a 序数决定性直派规则前置于数值比较, 逐条推演验证: R-a 的判据 (match_rate==1.0 且 |required_caps|>=2) 与 FP/TT 数值完全无关, 在 R-b 数值路径评估之前就已经裁决, #153 黄金场景 (3/3=1.00 vs backend-architect 0.33) 与单标签饱和场景 (AC-2b) 都能在新规则下正确推演出预期结果, 数学冲突已解开。

**QA 维度内 4 项『纸面关闭』** (计入下方 findings, 不重复展开, 仅索引):

- Finding 1 (recommend Top-3 排序机制): 回收我 R1-MAJ4 + tech-lead R1-m3, Rev1 只加了 AC-6 文字, 没配套机制, 且与 §2.4 自己的量纲论证冲突。
- Finding 2 (manual agent_source 矛盾): 回收 tech-lead R1-m3 的『manual 不波及未刻画』, Rev1 的『不受 3e 影响』澄清与同版本新增的『agent_source additive 覆盖 manual』直接打架——是**修复引入的新矛盾**, 而非未处理的旧问题。
- Finding 3 (L1/L2 共存污染 fixture pin): 回收我 R1-CRIT1『required_caps 推导机制未定义』的残留部分——Rev1 解决了『有来源』但没解决『L1 命中后 L2 是否仍会追加』, 威胁 AC-1 旗舰场景可复现性。
- Finding 4 (D9 语义保留声称不准确): 回收我 R1-MAJ6『相对奠基决策已有静默漂移』的一半——Rev1 处置了评分先后顺序 (450102ae), 但没处理『D9=警告+显式确认』vs『现状=仅警告』这层漂移, 新增的『(D9 语义保留)』括注反而是不准确的重申。

其余 R1 Major (差值规则孤儿/AC-3 逐字节不可判定/frontmatter 边界) 经核对 proposal.md 与 SKILL.md 现有文本, 确认落地扎实, 不再重复报告。

## 审计结论 (新 finding 带证据)

本轮共提交 8 项 Major finding (0 Critical), 详见结构化 findings 字段, 覆盖:
1. recommend 模式 Top-3 排序机制缺失 (纸面关闭)
2. manual 模式 agent_source 自相矛盾 (纸面关闭 + 修复引入)
3. required_caps L1/L2 共存威胁 AC-1 旗舰场景可复现性 (纸面关闭)
4. 『(D9 语义保留)』表述与 D9 原文不符 (纸面关闭)
5. 同名替换后置信度归属未定义, 可能制造静默 regression (新发现, 与 §4 缓存问题同构但未被同等审视)
6. §4 缓存机制三处未覆盖边界: 写失败/目录不存在/既有 cache_ttl_seconds 交互 (新发现)
7. AC 方法论承诺的『决策路径 R-a/R-b』字段在输出契约中未定义 (新发现)
8. AC-2(b) 数值选择无法甄别『单标签禁止直派』规则是否生效, 且暴露 R-b 排除时序未定义 (新发现)

逐条推演结论 (角色侧重问题回答):
- **AC-1/AC-5**: R-a 触发条件可满足, fixture 可构造 (task_type 传 tag 值 + 任务文本嵌入第二个 tag 字符串), 但见 finding 3, 存在 L2 追加推断导致 required_caps 漂移的残留风险。
- **AC-2(b)**: 见 finding 8, 当前数值选择缺乏区分力, 建议改用差值 > 0.1 的 FP 分数重新设计。
- **AC-4**: match_rate 0.67 与差值 <=0.1 可同时构造 (taxonomy tag 数量 + FP/TT 常数表组合空间充足), 未发现阻断性问题。
- **AC-3**: 结构化字段级一致 (agent/status/confidence-来源规则) 可判定, additive 字段 (agent_source) 被显式排除在比较范围外, 设计合理。
- **AC-6**: 见 finding 1, 缺排序机制。
- **AC-7**: 可构造, 且已有姊妹 Spec (agent-team-audit-project-agent-augmentation) 的 `project-malformed.md`/`project-security-auditor.md` fixture 先例可直接复用范式, 未发现问题。
- **新机制未测边界**: agent_source 在 manual/fallback (finding 2)、缓存重建失败/.aria/cache/ 目录不存在 (finding 6)、同名保护警告在 auto 直派时的输出承载面未定义 (finding 5 中一并讨论——警告若落在 free-text reason 里则被 AC 方法论自身排除断言, 事实上不可测)。

## Verdict

**verdict: PASS_WITH_WARNINGS** (0 critical + 8 major)
**vote: REVISE**

不投 PASS 的原因: 8 项 Major 里有 4 项是『纸面关闭』——即 R1 已经指出问题, Rev1 做了文字层面的回应, 但机制/证据没有跟上, 其中 1 项 (finding 2) 更是 Rev1 自己两处新增文本互相矛盾。这些不是"鸡蛋里挑骨头"式的措辞问题: finding 1/3 直接触及本提案选择的验证策略 (structural fixture 替代 AB benchmark, Rule #6) 的可靠性根基; finding 2/4 是可以在 30 分钟内用一两句话修正的具体文本矛盾; finding 5/6/7/8 是新机制 (同名替换/缓存/输出契约/AC 数值设计) 在从『孤儿』变『主链』过程中被激活的边界, 目前均无 AC 兜底。不推翻方案本身——R-a/R-b/R-c 分层决策、两级闭集 required_caps、per-file 缓存比对的**方向**都是对的, 且两条 R1 Critical 是真闭合而非纸面闭合, 本轮不需要回到『方案层面重新设计』, 但在进入 A.2 任务规划前, 建议至少处理 finding 1/2/4 (文本层面矛盾, 修复成本低) 与 finding 3 (fixture 可靠性, 影响 Phase B 验证阶段是否会遇到"测试自己先假失败"), 其余 4 项可视 owner 风险偏好决定是否本轮一并处理或作为已知限制显式承认。

## 核验锚点

- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md` (全文, 重点 §1/§2.1/§2.4/§3/§4/AC 段/Resolved 表)
- `aria/skills/agent-router/SKILL.md:1-13,17,145-246,383-434,449`
- `aria/skills/agent-router/ROUTING_RULES.md:172-212`
- `aria/references/capabilities-taxonomy.yaml` (全文)
- `aria/skills/subagent-driver/references/handoff-contract.md:14,33` (agent_source 预留字段, 已核实引用准确)
- `.aria/config.template.json` / `.aria/config.json` (均无 agent_router 块, 核实 §5 claim 准确)
- `openspec/archive/2026-04-11-agent-project-adapter/proposal.md:195` (D9 原文核对)
- `openspec/archive/2026-06-21-agent-team-audit-project-agent-augmentation/proposal.md` (AC 范式对照, fixtures 先例)
- `aria/skills/agent-team-audit/references/fixtures/project-security-auditor.md` / `project-malformed.md` (fixture 构造范式实证)
- `.aria/audit-reports/post_spec-R1-1783541662234-agent-router-injection-qa-engineer.md` (本人 R1 报告, 全文)
- `.aria/audit-reports/post_spec-R1-1783541662234-agent-router-injection-tech-lead.md:40-56` (m-2/m-3 交叉核对)
- `openspec/changes/aria-2.0-m7-agent-lifecycle/proposal.md:120-135` (M7 L129 不依赖声明, 核实引用准确)
- `docs/requirements/user-stories/US-011.md:43-61` (D4 errata 依据, 核实引用准确)
