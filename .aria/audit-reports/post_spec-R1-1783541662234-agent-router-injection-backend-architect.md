---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-07-08T19:30:37.844Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

角色定位：backend-architect，本轮侧重 §CAP capability-match 评分算法的可实施性、量纲/评分体系一致性、taxonomy 归一语义、缓存失效语义、以及"复用 agent-gap-analyzer 语义"的真实性核验。已逐字通读全部必读文件 + 角色附加必读文件，并额外核对 agent-creator/SKILL.md 与 agent-project-adapter 归档 proposal 的 D4/D7/D10 决策记录以核实"根因"叙事与"确定性"血统的真实来源。

**先确认成立的部分**（避免只报问题不报grounding）：Why 段三点缺陷描述（孤儿段/短路/无评分规则）逐一对照 SKILL.md §221/§232/§393 与 ROUTING_RULES.md 现有四表，均**准确**；D4 (运行时注入而非静态注册)、D7 (标签匹配非 LLM 解析)、D10 (taxonomy 规范标签+同义词) 三条决策记录引用与归档 proposal.md:190-196 原文**完全一致**；match_rate 公式 (`|matched|/|required|`) 与 agent-gap-analyzer/SKILL.md:51-57 的公式**形式一致**，B3"复用标签重合率语义"在公式层面成立。

**但发现 1 个 critical + 4 个 major + 2 个 minor 问题，核心矛盾是：CAP 算法把"标签重合率"公式从 agent-gap-analyzer 搬了过来，却没有搬运公式背后真正撑起"确定性"承诺的东西——一张封闭的、任务特征到标签的映射表。**

### 发现 1 (critical) — required_caps 计算无确定性来源，"复用 gap-analyzer 语义"在关键处不成立

`required_caps = normalize(task_type→caps ∪ 关键词→caps ∪ file-path→caps)` (proposal.md:58) 假设存在三个映射函数，但：
- ROUTING_RULES.md 现有四张表 (FP/TT/关键词/技术栈) 全部映射到 **Agent 名**，不是 capability 标签 (例：TT-003 `database`→`backend-architect`，不产出任何标签)。
- capabilities-taxonomy.yaml 只是「canonical tag → synonyms」封闭表，不含任务特征→标签的条目。
- 真正撑起 gap-analyzer "确定性"承诺的是 tech_stack_mapping (agent-gap-analyzer/SKILL.md:36-43)——一张针对**项目 tech_stack 封闭枚举值**（"Prisma"/"Express"等）的显式表；agent-gap-analyzer/SKILL.md:93 明确强调"场景列表来自规则映射，非每次 LLM 推断"。CAP 算法面对的是**单个任务的开放文本** (task_type/关键词/files)，没有等价封闭表，而 agent-router 是纯 prose Skill (SKILL.md:1-13，无 Python)，若靠 forked LLM 临场推断标签，恰恰退化成 gap-analyzer 明确要避免的"每次 LLM 推断"，与 D7 (openspec/archive/2026-04-11-agent-project-adapter/proposal.md:193) 矛盾。
- 后果：AC-1 (proposal.md:113) 依赖 required_caps 正确推出 orm-migration/database-schema，但没有可审计推导路径，是不可 falsify 的验收标准。

判定为 critical：spec 在此处**不可实施** (核心输入无定义) 且**自相矛盾** (声称"确定性"却缺确定性来源)。

### 发现 2 (major) — normalize() 对词表外自造标签行为未定义

agent-creator/SKILL.md:49-51 的 frontmatter 模板允许任意 `<tag>`，且 SKILL.md:82-84 承认存在人工/LLM 生成路径，不保证标签落在 capabilities-taxonomy.yaml 封闭词表内。CAP 算法的 `normalize(a.capabilities)` (proposal.md:60) 没有定义遇到未登录标签时的行为——静默丢弃会让项目级 Agent 的真实能力再次"形同虚设"，正是本 change 试图修复的问题的缩小版重演。

### 发现 3 (major) — match_rate 与 FP/TT confidence 量纲不可比，单标签/少标签场景可虚高到 1.0

match_rate 是比率 [0,1]，FP/TT confidence 是人工标定值 (0.70-0.95 基础值 + booster，上限 1.0，ROUTING_RULES.md:174-186)。当 required_caps 只有 1-2 个标签且全命中时，match_rate=1.0，而 B4 (proposal.md:85) 的精度 tiebreak **只在项目级候选互相打平时生效**，从不参与和 FP/TT 候选的主排序比较；B5 差值<0.1 降级 (proposal.md:86) 只在 FP/TT 竞争信号本身较强(与CAP接近)时才拦截——若 FP/TT 信号弱或缺失 (差值>0.1)，CAP 的 1.0 会直接 auto 胜出，且这恰是最需要审慎的场景。B4 决策记录自称"防1个泛标签agent靠1/1=1.0秒杀全场"，但其机制并不能兑现这个承诺（只挡得住"项目级候选互相比"，挡不住"项目级 vs 插件级比"）。

### 发现 4 (major) — 平局链不完整 + "与既有§优先级处理一致"表述不准确

proposal.md:64『裁决 (与既有 §优先级处理一致)』引入的"精度→字典序"平局链，在 ROUTING_RULES.md:190-201 现有「优先级处理」中**完全找不到对应**——现有规则是"同 Agent 多规则去重"(置信度→规则优先级→规则ID) 和"跨 Agent 差值<0.1 降级"两条，都不含"精度"或"字典序"概念。这是净新增裁决逻辑，非复用。更关键的是：精度 `|matched|/|a.capabilities|` 只对拥有 capabilities 字段的项目级 agent 有定义，插件级 (FP/TT) 候选没有等价概念——若两者精确同分 (在发现 3 揭示的分布下相当可能)，裁决路径缺失。

### 发现 5 (major) — 缓存 mtime 失效语义在新主链下暴露既存漏洞

SKILL.md:412-413 的缓存失效条件（目录 mtime 变化 或 文件数量变化）在 POSIX 语义下**不覆盖"编辑已存在文件内容、不增删文件"**的场景（目录 mtime 只在增删/改名条目时变化）。此前因 auto 路径从不真正扫描，这个盲点"无关痛痒"；本提案把扫描升为每次路由强制步骤后，它变成"项目 owner 编辑 Agent capabilities 想修正路由却静默不生效"的真实故障模式。proposal Risk 段 (98-99) 未披露此风险，AC 的 structural fixture（一次性创建）也不会覆盖这条路径。

### 发现 6 (minor) — §205 step 3 转述编号与源文件结构不完全对应

SKILL.md:221-225 原文 4 个平级子项 (FP/TT/技术栈/关键词) 被 proposal.md:37-41 压缩改写成 3a-3c (技术栈+关键词合并)，纯转述精度问题，不影响功能。

### 发现 7 (minor) — SKILL.md 第三处版本声明未纳入同步范围

SKILL.md:17 正文版本横幅 (现 1.0.0) 与 footer:449 (1.1.0) 已经不一致（既存漂移）；proposal.md:74 版本同步范围写"frontmatter/footer"，但 SKILL.md frontmatter (1-13) 实际无 version 字段，真正的两个版本字符串是行 17 横幅和行 449 footer，行 17 未被点名，AC-6 可能遗漏。

## Verdict

**FAIL**（≥1 critical）。发现 1 (required_caps 计算无确定性来源) 是致命缺陷：它是整个 §CAP 算法的输入源头，没有它，AC-1 (核心正召场景) 无法被客观验证，B3 的"确定性"决策依据不成立。发现 2-5 (major) 进一步表明即便发现 1 被修复，评分体系在标签词表边界、跨池量纲比较、平局裁决完备性、缓存失效边界上仍有需要 rework 的缺口。发现 6-7 (minor) 为转述精度问题，Phase B 顺手可修，不阻断本轮判定。

建议：REVISE。核心待补：(a) 为 required_caps 提供一张显式封闭映射表（仿 gap-analyzer tech_stack_mapping 模式），或明确降级"确定性"措辞并补充审计机制；(b) 定义 normalize() 对词表外标签的行为；(c) 给 CAP 分数体系加最小标签数门槛或把精度纳入主排序，堵住少标签虚高分绕过 B4/B5 的路径；(d) 补全跨池精确同分裁决 + 修正"与既有一致"表述；(e) 缓存失效条件补充文件级 mtime。

## 核验锚点

- openspec/changes/agent-router-auto-project-agent-injection/proposal.md:1-124 (全文逐段核对 Why/What/Decision Records/Impact/OOS/AC)
- aria/skills/agent-router/SKILL.md:1-13, 17, 205-246, 221-225, 227-230, 232-243, 393-434, 410-414, 449
- aria/skills/agent-router/ROUTING_RULES.md:25-53, 57-85, 89-143, 146-168, 172-186, 190-201, 205-211
- aria/references/capabilities-taxonomy.yaml:1-146 (全文)
- aria/skills/agent-gap-analyzer/SKILL.md:1-93 (全文，重点 36-43 tech_stack_mapping / 51-57 match_rate / 89-93 非LLM推断声明)
- aria/skills/agent-creator/SKILL.md:1-85 (全文，重点 25-28 / 40-54 frontmatter 模板)
- openspec/archive/2026-04-11-agent-project-adapter/proposal.md:190-196 (D4/D7/D10 决策记录核验)
