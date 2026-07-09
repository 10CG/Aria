---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-07-08T19:51:33.942Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论 (逐条 finding 带证据)

先说清楚这份 spec 做对了什么，再说问题在哪：CAP match_rate 公式本身 (交集/required_caps) 与 agent-gap-analyzer 的既有语义确实同构、平局 tie-break (精度→字典序) 明确可执行、`required_caps` 为空时退化基线的边界写得干净、B2/B5 对既有『差值<0.1降级』规则的复用意图也是对的。问题集中在：**这份 spec 把新引入的『从任务文本推断能力标签』这一步默认当成了跟『在已知标签表里查表』同等确定性的操作，而它其实不是** —— 这一条根因串起了下面大半个 finding 列表，也是我作为 QA 这一轮最想讲清楚的一件事。

### Critical

**CRIT-1｜required_caps 推导机制未定义, 威胁提案自选验证策略的根基**

`ROUTING_RULES.md §CAP` (提案新增) 的公式 `required_caps = normalize(task_type→caps ∪ 关键词→caps ∪ file-path→caps)` 标注为"确定性"，但这三个箭头函数在提案全文、`ROUTING_RULES.md` 现有表、`capabilities-taxonomy.yaml` 里都找不到定义：
- 现有 FP-*/TT-*/关键词表只映射"任务特征→Agent名"，不是"→能力标签"。
- `capabilities-taxonomy.yaml` 只是 46 个 tag 的同义词归一字典，没有"关键词/task_type→标签"的索引——它能把已经识别出的候选标签词归一化，不能从自然语言里"识别"出候选标签词。
- `agent-gap-analyzer/SKILL.md:33-43` 的 `tech_stack_mapping` 是提案 B3 援引"复用 gap-analyzer 语义"的对象，但它的键是 project-profile.yaml 的技术栈字段 (如 "orm: Prisma")，是项目清单信号，不是运行时任务描述文本——键空间完全不同，不能直接复用。
- 全文 grep `parse|malform|skip|非法|失败` 在 `proposal.md` 中零命中，确认没有为这一步定义任何降级/推导算法。

再往上追一层：B3 决策记录写"与 D7/D10 一致: 确定性 > LLM 评分, 可审计"，但 D7 原文 (`openspec/archive/2026-04-11-agent-project-adapter/proposal.md:193`) 是"capabilities 标签匹配 (**非 LLM 解析 description**)"——D7 管的是 Agent 侧已声明标签的匹配，不覆盖"从任务文本推断标签"这一步。把这一步也贴上"确定性"标签，是对 D7 适用范围的不准确援引。

**为什么是 critical 而不是 major**：这不只是"少一张表"的完善度问题。提案自己选择的 Rule #6 替代验证策略是"structural fixture"（`proposal.md` 末段：'AC 由 structural fixture 验证 (Rule #6: deterministic/structural Skill 用 substitute)'）——而 structural fixture 的前提就是"确定性可复现"。AC-1/AC-2 (本提案最核心的两条正召/不误召验收) 都要求 fixture 里的任务能确定性地映射到 required_caps。这一步没有定义，Phase B 写 fixture 时只能临时发明一套映射，测的是发明出来的东西，不是 spec 本身——这直接动摇了"用 structural fixture 代替 AB benchmark"这个选择的正当性。

**建议**：在 §CAP 补一张显式"task 信号 → capability 标签"表 (结构类比 FP-*/TT-*)，或明确给出至少几组 worked example 复用 gap-analyzer 模式；否则要么这条路走不通，要么应如实承认 Rule #6 替代论证的局限。

### Major

**MAJ-1｜AC-4/AC-5 依赖的"差值<0.1降级"规则本身可能是另一个孤儿**

`SKILL.md §232` (L232-237) 字面执行流程只检查单一 `top_confidence >= threshold`，不检查"是否有第二名与第一名差值<0.1"。这条规则实际只活在 `ROUTING_RULES.md` L198-201 和 `SKILL.md` L389 (错误处理表)，两处都不在 §232 的字面步骤序列里——这正是本提案给 §393 定性"孤儿"的同一判据。B5 把 AC-4 的可证性建立在这条同样游离于主链之外的规则上，却没有像对 step 3d 那样显式接线，也没安排验证它目前是否真的生效。建议把这条比较逻辑显式写进 §232 的 step 5 文本，并在 Phase B 验证清单里加一条：先确认基线下这条规则确实生效。

**MAJ-2｜AC-3"逐字节相同"对含自由文本 reason 字段的路由输出不可验证**

`SKILL.md §输出格式` 所有示例的 `reason` 字段都是自然语言复述，不是查表拼接产物 (ROUTING_RULES.md 各表只有"说明"列，无固定 reason 模板)。agent-router 是 `context:fork + agent:general-purpose` 的纯 prose Skill，两次独立 fork 执行间 `reason` 措辞几乎必然有差异，即使 agent/confidence 完全稳定。AC-3/B6 两处"逐字节相同"按字面覆盖整个输出载荷，这个门槛大概率会在 Phase B 验证时虚假失败或被松弛执行成"看起来差不多就算过"。建议限定在结构化字段等价 (status/agent/confidence/model)，显式放开 reason 措辞差异。

**MAJ-3｜CAP 公式分数与 FP/TT 常数分数的可比性未经论证**

B4 只堵住了"agent 标签集过窄导致虚高"，没堵"required_caps 本身推断得窄"这条路径——两者对 `match_rate` 的数学效果相同(分母小→易达1.0)。#153 实证里 `database-specialist 3/3=1.00` 对 `backend-architect 0.33` 的悬殊差距，侧面印证 match_rate 容易触顶。FP/TT 是人工调校常数 (base+booster)，CAP 是公式比值，两套量纲未经校准就直接"取全局最高"(B2)，可能让窄任务下的项目级候选系统性压过精调过的插件级候选，且发生在无人复核的 auto 模式。建议给低 `|required_caps|` 场景加分数折扣或强制降级推荐。

**MAJ-4｜recommend(默认)模式 Top-3 构成变化零 AC 覆盖**

`SKILL.md` L62 明确 recommend 是默认模式。step4 的统一候选池同时喂给 auto 阈值判断和 recommend Top-3 选择，但 AC-1~AC-6 全部聚焦 auto 模式。若项目积累多个弱相关 CAP 候选，Top-3 可能被项目级候选挤占，插件级"常客"被移出榜单——这是可感知的默认模式行为变化，B6 的零回归承诺只锚定在".aria/agents/ 空"场景，非空场景完全未加约束。建议补一条 AC 验证多候选场景下 Top-3 是否仍合理。

**MAJ-5｜frontmatter 解析失败/字段缺失边界未定义**

对照角色附加必读 `agent-team-audit-project-agent-augmentation/proposal.md` AC-4 (`capabilities` 缺失/非list/parse失败→skip不阻断基线；空list→合法)——这是姊妹 precedent 在自己的 R1 收敛中才补上的边界，本提案的 step 3d 完全没提这条路径 (全文 grep 相关词零命中)。建议直接复用姊妹 precedent 的收敛结论。

**MAJ-6｜§393 同名保护与新的全局最高裁决复合关系未定义, 且相对奠基决策已有静默漂移**

§393 现状是"同名时项目级无条件覆盖(仅警告)"，但奠基决策 D9 (`openspec/archive/2026-04-11-agent-project-adapter/proposal.md:191`) 原意是"警告 + **显式确认**"——§393 现有文本已经把"显式确认"门槛静默弱化成"仅警告"。本提案 What Changes §3 只说"保留同名保护"，既没指出这处 D9→§393 的既存漂移，也没说明"按名覆盖"和新的"按置信度全局裁决"(B2) 谁优先——这恰是本提案自己存在的理由（文档描述的机制未必真接线）在其自身编辑范围内的又一次复现。建议借这次重写机会一并成文澄清。

**MAJ-7｜"强制"步骤未接线既有配置门控, 且该配置从未进入机读 schema**

`SKILL.md §393` 文档化的 `agent_router.scan_project_agents`/`plugin_only` 配置，经核实从未出现在 `.aria/config.template.json`（对照 `experiments.agent_team_audit` 已正确落地的正例，证明这是本仓库的既有惯例）。step 3d 标注"强制"且 bullet 列表完全没提检查任何 config gate。上线后项目 owner 事实上没有生效的关闭开关。建议要么把检查写进 step 3d 并补 schema，要么在 Out of scope 显式声明当前无配置化关闭手段。

**MAJ-8｜路由输出契约未新增字段披露候选来源层**

`SKILL.md §输出格式` 的 auto_match/recommend 载荷都没有 plugin/project 标识字段（`manual` 模式的 `source` 字段语义是"如何被选中"而非"来自哪层"）。已核实 `subagent-driver/references/handoff-contract.md` 的 `agent_source` 字段属于 Agent 执行完的 handoff 上下文块，非路由决策输出契约，二者用途不同。本提案首次让项目级 agent 能在 auto 模式真正胜出，却没同步给输出契约加来源层标识，下游消费方无从区分。

**MAJ-9｜缓存失效规则遗漏原地内容编辑, 死代码变活代码后成为可达 bug**

`SKILL.md §393` 缓存失效判据是"目录 mtime 变化 或 文件数量变化"。已用 bash 实测验证：对目录内已存在文件做原地内容编辑，目录 mtime 完全不变，只有文件自身 mtime 变化——这是 Unix 语义，不是猜测。这意味着 owner 编辑已有 agent 文件的 capabilities 字段（不增删文件）时，若缓存未被手工清空，路由会静默使用陈旧数据。此规则此前是孤儿死代码，本提案把它接入主链后成为真实可达路径，且无 AC 覆盖。

### Minor

**MIN-1｜版本变更位置描述与源文件实际结构不符**

`SKILL.md` frontmatter (L1-13) 无 version 字段，实际版本标记在 L17 正文 header ('版本: 1.0.0'，已与 footer L449 '1.1.0' 存在既存不一致) 和 L449 footer。`ROUTING_RULES.md` 版本标记在 L3 文首而非文末/footer。提案"frontmatter/footer"的描述不准确，且 AC-6 未显式核对这两处 Skill 自身版本行是否落地。

## Verdict

**verdict: FAIL** (1 critical + 9 major)
**vote: REVISE**

核心诉求：required_caps 推导机制必须先补齐（CRIT-1），否则 AC-1/AC-2 的 structural fixture 验证手段站不住脚，Rule #6 替代论证也站不住脚。9 条 major 里，MAJ-1/MAJ-2 直接触及本轮 QA 职责核心（AC 可验证性），MAJ-5/MAJ-6/MAJ-7/MAJ-9 是边界覆盖缺口，MAJ-3/MAJ-4/MAJ-8 是设计/接口完整性缺口。这些问题不推翻"auto 路径应该消费项目级 Agent"这个核心方案——CAP 公式、tie-break、B2 池化思路本身是合理的——但当前文本距离"可直接进 A.2"还有实质性 rework 要做。

## 核验锚点

- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md` (全文)
- `aria/skills/agent-router/SKILL.md:1-13,17,145-201,205-246,383-389,393-434,449`
- `aria/skills/agent-router/ROUTING_RULES.md:1-6,172-186,190-212,268-270`
- `aria/references/capabilities-taxonomy.yaml` (全文)
- `aria/skills/agent-gap-analyzer/SKILL.md:23-57`
- `aria/skills/subagent-driver/references/handoff-contract.md:1-58`
- `openspec/archive/2026-04-11-agent-project-adapter/proposal.md:183-198` (D1-D11)
- `openspec/archive/2026-06-21-agent-team-audit-project-agent-augmentation/proposal.md:86-94`
- `.aria/config.template.json` (全文)
- bash 实测：目录 mtime 对子文件原地内容编辑不敏感 (验证 MAJ-9)
