---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-08T19:59:55.701Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 审计报告 — agent-router-auto-project-agent-injection (code-reviewer)

## 审计结论

### 逐行 grounding 核验 — 全部通过 (proposal 对源文件的核心事实声称精确)

对照真源文件逐条核验, proposal 的三处缺陷诊断**全部成立**:

- (a) SKILL.md L205 确为「## 执行流程」; L221-225 step 3 只列 文件路径/任务类型/技术栈/关键词 四类, 无 capability 步 — proposal Why 第 1 条 ✅
- (b) L232-237 step 5 auto 分支 `top_confidence >= threshold → 返回自动匹配`, 且 step 4 聚合 (L227-230) 的输入只来自 step 3 四类 → 短路结构属实 — Why 第 2 条 ✅
- (c) L393-434 §393「项目级 Agent 发现 (v1.1.0)」确为文末孤儿段, 自带一套与 §205 编号体系脱节的 5 步图 (L399-406), 从未接进主流程 ✅; L408「Plugin 不会自动加载 .aria/agents/」声明存在 ✅; L410-414 缓存 + mtime 失效语义与 proposal 3d「复用」描述一致 ✅
- (d) ROUTING_RULES.md 确只有 FP (L27-53) / TT (L59-85) / 关键词 (L89-143) / 技术栈 (L148-168) 四表, 全部映射到 **agent**, 无 capability 评分规则 — Why 第 3 条 ✅; B5 引用的差值 <0.1 降级是 L198-201 既有规则 ✅
- (e) capabilities-taxonomy.yaml 同义词映射存在: orm-migration↔database-migration/schema-migration (L136-137), query-optimization (L138-139), database-schema↔db-design (L21-22) — #153 的 database-specialist 三标签全在词表 ✅
- (f) agent-gap-analyzer match_rate = 命中标签数/需求标签数 (SKILL.md L55) =「标签重合率, 非 AI 评分」(L92) — B3「复用 gap-analyzer 语义」声称成立 ✅
- (g) subagent-driver 契约含 `agent_source: "plugin"|"project"` — 位于 `aria/skills/subagent-driver/references/handoff-contract.md` L14/L33 (契约参考文件, SKILL.md 本体无此词) — OOS 声称实质成立 ✅
- (h) 上游引用双准: augmentation proposal **L16** 原文「triage 已确认 agent-router 任务路由路径**会**扫 .aria/agents/」✅; M7 agent-lifecycle **L129**「只做『将项目级 Agent 注入路由上下文』」✅; 发现 A 认领处 M7 L28 (物化断层) + B.2 step 3 (L125 物化 native 层) ✅; agent-project-adapter D4 (L190) framing 转述准确, B3 引 D7/D10 (L193/L196) 语义一致 ✅
- (i) #153 数字 (0.95 短路 / 12 候选 / 3/3=1.00 / 次优 0.33) 全部置于「**实证** (#153, cesura 项目)」标注段内, 未当无源事实使用 ✅ (12 = 插件 11 agent 能力矩阵 L307-319 + 1 项目级, 自洽)
- (j) 合规: Rule #5 位置正确 (openspec/changes/) ✅; Level 2 判级合理 (单 Skill 行为契约, additive) ✅; Rule #6 structural substitute 路线有 shipped 先例 (augmentation 同为 prose skill 行为改造, 5 structural fixture + dogfood, R2 CONVERGED) ✅; Rule #4 零回归以 B6/AC-3 承载 ✅; plugin.json 现值 1.53.0 与 Target 起点一致 ✅

**结构逻辑自洽**: 3d 候选在 step 4 聚合前入池 → step 5 的 top 自然为全局最高, 「堵死 §232 短路」的机制推理成立。

### Major-1 (architecture, proposal.md#What-2-CAP) — required_caps 三映射无成文规则, §CAP「确定性」主张输入侧留白

§CAP 公式 (L58) 依赖 task_type→caps / 关键词→caps / file-path→caps 三个映射, 但: taxonomy 只有 tag↔synonym 归一; ROUTING_RULES 四表映射到 agent 非 capability 标签 (grep orm-migration/query-optimization 零命中); gap-analyzer 的既有映射是 tech_stack→caps (输入为 project-profile 非 task, SKILL.md L36-43)。gap-analyzer 的确定性恰恰建立在「场景映射规则成文」+「场景列表来自规则映射, 非每次 LLM 推断」(L36, L93) 之上 — 先例标准表明: 映射不成文, 确定性不成立。当前草案下 forked agent 每次自由联想 task→标签, B3/D7/D10 的「确定性可审计」主张断在输入侧, AC-1/2/4/5 fixture 复跑结果可漂移。Impact L99「可迭代补表」暗示有表, 但 What §2 只有公式没有表也没有建表要求。
**修法**: §CAP 内增补 task→caps 种子映射表小节 (仍无新 artifact), 至少覆盖 AC-1 场景标签, 并声明「推断仅查表, 不做自由联想; 不命中→空集退化基线」。

### Major-2 (architecture, proposal.md#AC-1-AC-4-AC-5) — 差值降级带与「胜出」承诺在主打场景数学冲突, 修复后行为未言明

CAP match_rate 上限 1.0 (L61), 插件分同 cap 1.0 (ROUTING_RULES L185)。对 **>0.9** 的 FP/TT 对手, 差值恒 <0.1 → 按 AC-4/B5 (沿用 L198-201) **恒降级推荐, auto 直派不可达**。AC-5 (L117) 自己锁死「FP/TT 命中 0.95 插件 agent」→ 差值 ≤0.05, 该场景「按全局最高裁决」的 auto 分支结构性不可达; AC-1 (L113)「auto 模式…胜出。复现 #153 场景」而 #153 正是 0.95 对手 → 实际可观察行为 = `recommend` + 项目级 rank 1, 不是 auto 派。Why L22 引第二次跑「次优 0.33」是 capability-only 量纲; 混池后 backend-architect 取 max(FP/TT 0.95, CAP 0.33)=0.95, 「1.00 vs 0.33 决定性胜出」图景不会出现。降级本身可能正是 B5 想要的保守行为, 但 spec 从未言明「主打场景的修复后终态 = 降级推荐」, AC-1 的「胜出」与 Why 的「决定性胜出」叙事制造 auto-派期待 — fixture 落笔时 validator 无法确定该断言 `auto_match` 还是 `recommend`, 两条 AC 对同一 fixture 给出可冲突的期望。
**修法** (推荐 a 最小变更): (a) 定义「胜出 = rank 1 (降级推荐属预期)」并在 Why 补一句消除期待; 或 (b) full-match 1.0 项目级豁免差值带; 或 (c) 差值带限同量纲比较。任选后 fixture 断言粒度随之钉死。

### Minor 4 条

- **M-1 (documentation, #What-3)**: 版本位置/现值描述失准 — SKILL.md frontmatter (L1-13) **无 version 字段**, 版本在 L17 正文 header 且现值为 **1.0.0** (v1.1.0 发版漏改的既有漂移); 按「v1.1.0 → v1.2.0」字面替换会漏 L17, 把 header 1.0.0 / footer 1.2.0 的更大漂移固化进本次发版。ROUTING_RULES 版本在 header L3, 非 proposal 所说 footer (L270 只有日期)。→ What §3 改精确指令并点名 L17 一并修正。
- **M-2 (documentation, #AC-6)**: 「版本 5 文件同步」只覆盖子模块 5 文件; CLAUDE.md 发布清单的主仓段 (gitlink / 主项目 VERSION / root README badge L8 + Project Status / i18n B 档) 与 marketplace.json **双 version 字段** (实测 L3 + L16) 未点名 — 均为历史实证漂移源 (badge 不在子模块 SOT)。→ AC-6 补一句指向完整清单。
- **M-3 (documentation, #What-3 §408 处置)**: 「删除『Plugin 不加载』的误导性 framing」有歧义 — 该句是技术正确且 load-bearing 的边界澄清 (D4 L190 + M7 L129 双重印证), 恰是发现 A/B 的文档分界锚, 字面删除会重蹈 #153 发现 A 混淆。→ 改「改写 framing, 保留技术事实 + 指针 M7 B.2」。
- **M-4 (implementation, #Decision-B1)**: B1「强制步」与 §393 既有配置 `scan_project_agents`(默认 true)/`plugin_only`(可关) (SKILL.md L425-433) 关系未言明, What §3 只说保留缓存/同名保护。→ 补「默认强制, plugin_only=true 为显式 opt-out」, AC-3 fixture 顺带覆盖。
- **M-5 (testing, #AC-3, risk)**: 「逐字节相同」对含自由文本 `reason` 字段的 LLM 输出是过强断言粒度 (措辞继承自 augmentation AC-3 L90 先例, 但先例比较对象是离散批次集合)。→ 注明比较粒度 = 决策字段 (status/agent/confidence/排序), prose 不参与。

## Verdict

**PASS_WITH_WARNINGS** (0 critical + 2 major + 5 minor) → **vote: REVISE**

方案骨架 (3d 入池 + 全局最高裁决 + 复用既有缓存/taxonomy/差值规则) code-grounded 且逻辑成立, 诊断与上游引用精度是本批 spec 中的高水准; 但 §CAP 输入侧映射留白 (Major-1) 与「胜出 vs 降级带」的主打场景行为未言明 (Major-2) 必须在 Rev 中收敛, 否则 A.2 落 fixture 时验收期望会分裂。两处均为局部 rework, 不推翻方案。

## 核验锚点

- openspec/changes/agent-router-auto-project-agent-injection/proposal.md:1-123 (全文)
- aria/skills/agent-router/SKILL.md:1-13, 17, 205, 221-225, 227-230, 232-237, 393-434, 408, 410-414, 425-433, 449
- aria/skills/agent-router/ROUTING_RULES.md:3, 27-53, 59-85, 89-143, 148-168, 185, 190-201, 270
- aria/references/capabilities-taxonomy.yaml:21-22, 136-145
- aria/skills/agent-gap-analyzer/SKILL.md:36-43, 51-57, 89-93
- aria/skills/subagent-driver/references/handoff-contract.md:14, 33
- aria/.claude-plugin/plugin.json:4; aria/.claude-plugin/marketplace.json:3, 16
- openspec/archive/2026-04-11-agent-project-adapter/proposal.md:190-196
- openspec/archive/2026-06-21-agent-team-audit-project-agent-augmentation/proposal.md:16, 90, 92
- openspec/changes/aria-2.0-m7-agent-lifecycle/proposal.md:28, 119-129
- CLAUDE.md#版本发布检查清单 (主项目段 + 5 文件一致性表)