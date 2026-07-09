---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T21:09:10.040Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 审计报告 — agent-router-auto-project-agent-injection (knowledge-manager)

## R1 closure 核验

对我维度(文档同步/知识架构)内 R1 findings 逐条核对 Rev1 源文件(非仅信 Resolved 表字面):

**全关 6 条**(直接对源文件核验通过):
- 我自己 R1 报的「§438 未链 ROUTING_RULES / §93 未呼应 §CAP」→ §6 已补(SKILL.md §93/§438 均在连带清单内)
- 「§323/§35/§305 三段汇总性段落未纳入新机制」→ §6 已补齐全部 3 段
- 「§383 错误处理表未纳入新退化路径」→ §6 已补「3e 退化行」
- SKILL.md 版本三处漂移(L17/L449/ROUTING_RULES L3)→ §6 精确到位(经直接读取源文件验证 L17="1.0.0"、L449="1.1.0"、ROUTING_RULES L3="1.0.0"、L270 仅日期无版本, 与 Rev1 描述完全吻合), 未重蹈 Rev0「frontmatter/footer」旧误称
- 「M7 依赖关系表述反转」(262e329e)→ Why 段已重写为「M7 不依赖本 change」, 经 grep 核实 M7 proposal.md:129 原文确实如此
- recommend/manual「未受影响」未注明 → Impact 段已补「manual 模式: step 2 前置返回, 不受 3e 影响」

**纸面关闭/精度倒退 2 处**(本轮重点发现):
1. 我在 R1 原始报告精确点名 US-011.md 的三个真实锚点「AC-4/D4/Scope」(均逐一核实为文档中真实存在的段落), Rev1 改写后退化为「D4/交付清单」——「交付清单」在 US-011.md 真实结构中**不存在**(真实结构是「设计决策」表 + 「Acceptance Criteria」编号列表 + 「Scope」段), AC-4 与 Scope 两个原本被 R1 正确点名的锚点在 Rev1 文字中丢失(详见 finding M4)。
2. qa-engineer R1 MAJ-6 是复合发现(排序歧义 + 相对 D9 奠基决策的静默漂移), Rev1 Resolved 表(id 450102ae)只承接了排序歧义半句, 「静默漂移」半句未被承接, 且 §1 新文本反而写「(D9 语义保留)」, 与 qa-engineer 已核实的「D9 原意含显式确认, 现状已弱化为仅警告」相悖(详见 finding N7)。

**净新发现**(R1 五人 + 我自己 R1 均未覆盖): §393 缓存子段/cache_ttl_seconds 与 What §4 新机制脱节、§205 step 5 伪代码遗漏 recommend/manual 分支显式声明、§47 auto 模式概览段完全未纳入连带清单、AC-9 与 §5/§6 边界两处清单归属精度问题、Resolved 表 id 引用格式两处硬伤、§250 未提 agent_source、ROUTING_RULES 维护指南「四类」仍遗漏「技术栈」、Why 段上游关系讨论遗漏 DEC-20260621-001 配套决策记录同款过时断言。

**总体判断**: Rev1 在我维度内对 R1 的 8 major + 2 minor 吸收扎实、大方向对——§6 从「3 段」扩到「7 段 + 发版清单 + errata」是真实、可验证的扩容, 非灌水; 全部 7 段连带清单的 line-level 锚点逐一核对与 SKILL.md 真实标题/行号精确匹配。但改写过程本身引入了若干新的精度缺口, 且对 R1 原文有 2 处不完整/不准确的承接, 尚不构成「文档同步」维度可直接放行 A.2 的状态。

## 审计结论(新 finding, 按严重度排序)

### Major(4)

1. **§393 缓存子段 + cache_ttl_seconds config key 未纳入 §6 同步清单**: What §4 重写缓存失效机制(per-file stat 比对), 但 SKILL.md:412-413「缓存失效条件: 目录 mtime 变化或文件数量变化」与 :431 `cache_ttl_seconds` key 的新机制下语义均未在 §6 中安排同步, 新旧机制并存会产生矛盾文本。

2. **§205 step 5 伪代码遗漏 recommend/manual 分支显式保留声明**: What §1 对 step 5 的替换文本只展示 auto 分支(R-a/R-b/R-c), 原有三顶层分支(auto/recommend/manual)中另外两个未被保留或提及, 若逐字应用于 §205 会使 recommend/manual 从主执行流程正文消失, 与 AC-6 冲突。

3. **§47「路由模式→自动模式」概览段完全未纳入连带清单**: 该段仍写「触发: confidence >= threshold」旧描述, proposal.md 全文 grep「§47」「路由模式」零命中, 与 §205 新分层决策(R-a/R-b/R-c)直接矛盾, 且是读者最先接触的 auto 模式说明。

4. **US-011 errata 锚点相比 R1 原始表述退化**: 我 R1 精确定位的「AC-4/D4/Scope」三锚点, Rev1 改写为不存在于真实文件的「D4/交付清单」, AC-4 与 Scope 两处真实过时断言面临被遗漏订正的风险。

### Minor(8)

5. AC-9「What §6 全清单落地」误将实际声明于 §5 的 `config.template.json agent_router 块` 算入 §6。
6. §6「插件 SOT 5 文件」组成(含 plugin.json、不含 hooks.json)与我 R1 已核实无误的 CLAUDE.md 口径(派生文件 5 条含 hooks.json、不含 plugin.json)不同。
7. Resolved 表 id 引用不一致: L151「f2a4a9a」(7字符) vs L233「f2a4ac9a」(8字符), 同指一条 finding 却字符串不同。
8. Resolved 表 id「1d35911a」跨两行重复列出, 使 distinct id 计数(38)与标题「39 deduped findings」字面冲突, 无脚注说明。
9. §250「与 subagent-driver 集成」段未提及新增 agent_source 字段, 与 What §3 引入该字段的动机未呼应。
10. ROUTING_RULES 维护指南「四类含 CAP」仍遗漏既有「技术栈」类别(应为五类) —— 此项延伸自我自己 R1 minor finding 的原始欠精确表述。
11. §1「同名保护复合顺序」文本「(D9 语义保留)」措辞与 qa-engineer 已核实的 D9→§393 静默漂移事实相悖, 应改为「§393 既有行为保留」。
12. Why 段「上游关系」讨论未覆盖 `.aria/decisions/DEC-20260621-001-*.md:13` 里同款过时断言(该断言钉死在 v1.1.0, 本 change 上线也不会使其变真), 处置口径与已处理的另外两处交叉引用不对齐。

## Verdict

**verdict: PASS_WITH_WARNINGS**(0 critical / 4 major / 8 minor) → **vote: REVISE**

方案在我维度内的核心结构(§6 文档同步范围扩容、AC-9 机械检查清单、7 段连带锚点)是扎实、可验证的真实进展, 非纸面堆砌; 但 (a) 2 处新引入的伪代码/连带段落缺口(§205 step5、§47)、(b) 2 处对我 R1 原文的不完整/不准确承接(US-011 锚点退化、D9 语义误归因)、(c) 若干 checklist 归属与 id 引用的精度问题, 合计 4 Major + 8 Minor, 尚需一轮 rework 才能使「文档与代码 100% 同步」(Rule #3)的目标真正落地, 不建议直接放行 A.2。均为局部修订, 不动摇 Rev1 方案本体(§CAP 评分算法、分层决策规则等由其他 lens 审定的核心设计不在本报告范围内, 且经我旁证交叉核对未见新的架构级矛盾)。

## 核验锚点

见 `code_anchors` 字段, 涵盖: proposal.md 全文(逐段核对 What §1/§4/§5/§6、Decision Records、AC-1~AC-9、Resolved 表 20 行 id)、agent-router SKILL.md 全文 449 行(重点 §47/§145/§205/§232/§250/§393/§408/§416-421/§423-434)、ROUTING_RULES.md 全文 270 行(重点 L3/§253-259 维护指南)、capabilities-taxonomy.yaml、US-011.md 全文、CLAUDE.md 版本发布检查清单段、.aria/config.template.json 全文(确认现状无 agent_router 块)、.aria/decisions/DEC-20260621-001、以及全部 5 份 R1 原始审计报告(tech-lead/code-reviewer/qa-engineer/backend-architect/knowledge-manager 自身)交叉核验 closure 与 id 溯源。
