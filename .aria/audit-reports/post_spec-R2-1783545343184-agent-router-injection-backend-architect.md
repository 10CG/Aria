---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-07-08T20:32:28.627Z
context: openspec/changes/agent-router-auto-project-agent-injection/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 审计报告 — backend-architect

角色侧重: §2.4 决策规则完备性推演 / §2.1 L1-L2 分工 / §4 per-file 缓存 / match_rate 公式规模效应。

## R1 closure 核验

| R1 finding | 我维度内的核验结论 |
|---|---|
| Critical#1 required_caps 无确定性来源 (6dc8588a/866a9c98/73eba2dc) | **纸面关闭**。两级闭集机制真实存在, 但『L1 机械层为主干』的核心论据与源文件(TT 表 24% 对齐率 + subagent-driver 不传 task_type)矛盾, 生产路径事实上几乎全靠 L2。见 finding 2。 |
| Critical#2 B5 与 AC-1 数学冲突 (d378eb8a/af713ec5) | 对 AC-1 场景**真实关闭**(R-a 前置豁免可验证)。但修复动作本身(step 5 无条件整体重写)带出新回归, 见 finding 1。 |
| Major 跨池同分裁决缺失+一致性表述不实 (0c20a9e0) | **半关闭**。R-c 补了同分规则, 但『不再声称一致』只是撤回措辞, 没有真正协调 <0.1 与 <=0.1 的数值差异。见 finding 1。 |
| Major 同名保护复合顺序未定义 (450102ae) | **部分关闭**。评分时序已定义, 但置信度继承(替换后原插件规则分是否失效)未定义。见 finding 8。 |
| Major 缓存对原地编辑不敏感 (e7a6b2b5/94801d3c) | **部分关闭**。per-file 粒度收窄了问题, 未消除(同秒同 size 仍漏检), 且与 cache_ttl_seconds 复合语义未定义。见 finding 5/6。 |
| Major 量纲失配+单标签饱和抢占 (92358876/24b743aa/f8c242e4) | **真实关闭**。R-a/R-b/B4 tiebreak 推演自洽, 未见新缺口(含 R-a 多候选并列、R-a 与 plugin_only 互斥关系均验证清楚, 无 dead zone)。 |

## 审计结论 (新 finding, 按严重度排序)

### Finding 1 (Critical) — R-b 差值护栏边界静默收紧, 零 CAP 候选场景违反零回归承诺

`proposal.md:58-62` 的 step 5 被"重新成文"整体替换, 不是"仅当候选池含 CAP 候选时才接管"的条件分支。R-b (`proposal.md:108-109`) 用"差值 <= 0.1(含边界)", 而 `ROUTING_RULES.md:198` 既有规则是"差值 < 0.1"(严格)。ROUTING_RULES.md 整套置信度体系建立在 0.05 网格上——FP-002(`api/**/*` → backend-architect 0.95, 行 30) 与 FP-015(`docs/**/*` → knowledge-manager 0.85, 行 43) 恰好相差 0.10。

**具体回归场景**: `plugin_only:true` 或空 `.aria/agents/`(AC-3 声称的零回归三支之一)下, 任务同时触及 `backend/api/auth.js` 与 `docs/README.md`。Rev1 之前(旧规则 `<0.1`): 0.10 不算"相近", 0.95 auto 直派。Rev1 之后(step 5 被 R-a/R-b/R-c 无条件接管, `<=0.1`): 同一任务、同一"零项目 Agent"配置, 结果变成降级 recommend。这发生在一个**没有任何 CAP 候选参与**、被 AC-3 明确声称"逐字段等同基线"的路径上, 直接违反 Rule #4。`SKILL.md:389` 错误处理表还有第三种独立措辞("多个 Agent 置信度都 > threshold"), Rev1 What §6 未提及协调。这也是 R1 finding 0c20a9e0(跨池同分裁决缺失)未被真正关闭的证据——Rev1 只是撤回了"一致"的措辞声明, 没有协调数值本身。

**建议**: 要么把 R-a/R-b/R-c 限定为"仅当候选池含 >=1 个 CAP 候选时才接管", 零 CAP 场景完全落回原逻辑; 要么显式收紧全局边界并放弃"零回归"字面声称, 同时把这个 exact-0.10 场景补进 AC-3 fixture。

### Finding 2 (Major) — L1"主命中面"表述与源文件事实矛盾

`proposal.md:73` 称 task_type 精确匹配是"L1 主命中面", `proposal.md:188` Risk 行称"L1 机械层为主干"。逐项核对 `ROUTING_RULES.md:59-85` 的 25 个既有 TT task_type 值与 `capabilities-taxonomy.yaml`: 仅 6 个(24%, TT-002/006/007/010/023/024)词边界对齐 taxonomy tag/synonym; 其余 19 个(database/microservice/testing/performance/llm/rag 等)均不匹配(如 `capabilities-taxonomy.yaml:20-21` database-schema 的 synonyms 不含"database")。更关键的是, `SKILL.md:257-262` 记录的 subagent-driver 调用契约(唯一/主要调用方)根本不传 task_type(默认"自动推断", `SKILL.md:137`)。即 L1 的"主命中面"在真实主调用路径上基本不触发, 生产路径事实上接近 100% 落 L2, "半确定性定位"名不副实。这是 R1 Critical#1 在我维度内的纸面关闭证据。

**建议**: 软化"主命中面/主干"表述; 补 task_type→taxonomy 映射表或扩充 synonyms; 或在 Risk 行如实承认 L1 覆盖率。

### Finding 3 (Major) — L2 evidence token 无输出承载, "可审计"不可验证

`proposal.md:74-76` 要求 L2 每个 tag 引用 evidence token 并标记 `inferred=semantic`, 但 `proposal.md` §3(121-130 行)输出契约 additive 只加了 `agent_source` 一个字段, 完全没有承载 evidence token 或 inferred 标记的位置; `proposal.md:202` AC 总注又明确排除对 reason 自由文本的断言。三者组合意味着 L2 的证据链只存在于执行时的内部推理, 从未落到可复查的结构化输出里——鉴于 finding 2 已证明生产路径几乎全靠 L2, 这个审计缺口影响的是绝大多数真实路由决策。

**建议**: 输出契约新增 `required_caps_trace: [{tag, source: L1|L2, evidence}]` 或等价结构化字段, 使 AC 可断言而非依赖不测的 reason 文本。

### Finding 4 (Major) — match_rate 门槛随 required_caps 规模的可达性未被验证

R-a 要求 match_rate==1.0(项目级 agent.capabilities 必须是 required_caps 全超集)。L2 对推断 tag 数量没有任何上界/精简约束(`proposal.md:74-76`); AC-1 只验证 required_caps>=2 的小规模(#153 原始 3 标签)黄金场景, AC 全集(`proposal.md:200-212`)没有任何 4-5 标签规模场景验证 R-a 实际触发率。一个措辞较宽泛、经 L2 推断出 5 个 required_caps 的真实任务, 某 specialist 即便精准覆盖 3-4 个(0.6-0.8)也无法触发 R-a, 落入 R-b 后大概率因差值 <=0.1 被系统性降级——"auto 路径真正消费项目级 Agent"的真实覆盖面可能远窄于 proposal 暗示, 且这一点未被 AC 验证。

**建议**: 为 L2 补"每任务最多推断 N 个 tag"或"仅取证据最强 top-K"的成文上界; AC 补一个中等规模、部分命中的 fixture 场景。

### Finding 5 (Major) — per-file 缓存对同秒同 size 原地编辑仍漏检

`proposal.md:132-136` 的 per-file (path,mtime,size) 比对相比目录级 mtime 是真实收窄, 但 POSIX mtime 多为秒级粒度, 若同一秒内对某 agent 文件做等字节数的原地编辑(如调整 capabilities 顺序或替换等长 tag), 三元组不变, 判定"无差异"——与"任何差异(增/删/改)→重建缓存"的声称不符。3e 本就要读文件内容解析 frontmatter, 顺带算内容 hash 边际成本趋近零。

**建议**: 用内容 hash 替代或补充 mtime+size。

### Finding 6 (Major) — per-file 缓存与既有 cache_ttl_seconds 复合语义未定义

`proposal.md` §4 全文未提及 `cache_ttl_seconds`(`SKILL.md:429-431` 既有配置, 语义为"0=仅 mtime 失效, >0=时间失效"的二选一)。若沿用旧的"二选一"语义, owner 把 `cache_ttl_seconds` 设为正值(合理的运维选择)会导致 TTL 窗口内完全跳过 per-file stat 比对, 重新引入 B9 声称已修复的陈旧读取问题。

**建议**: §4 显式声明新旧机制为 AND 关系, 或废弃 TTL 模式的"绕过比对"语义。

### Finding 7 (Major) — L1/L2 组合算法未成文, L1 无否定语境鉴别力

`proposal.md:71-80` 分别定义 L1、L2 各自判定标准, 但从未给出"required_caps = f(L1_hits, L2_hits)"的显式合成规则(总是并集?去重规则?)。L1"词边界全名命中"是纯字面匹配, 不识别否定语境(如任务原文写"这不是 api-design 问题"仍会字面命中 api-design), 无仲裁说明。

**建议**: 补显式编排公式(union, L1 标记优先于 L2); 明确"L1 不做否定识别"是已知设计限制。

### Finding 8 (Major) — 同名替换后原插件级置信度是否失效未定义

`proposal.md:50-51` 只定义了"先去重后评分"的时序, 未定义替换后该候选的 FP/TT/关键词/技术栈分数来源。这些规则(`ROUTING_RULES.md`)纯粹按 Agent 名字匹配路径/关键词, 不检查定义内容——若项目级同名 Agent 语义上与原插件级 Agent 完全不同(如复用"backend-architect"这个名字做别的用途), 可能借壳插件级路径启发式获得与其真实能力不符的高置信度。

**建议**: 明确替换后原插件级 FP/TT/关键词/技术栈分数应清零或标记待重估。

## Verdict

**FAIL** (1 Critical + 7 Major)。vote = REVISE。

Critical 项(finding 1)是 fix-introduced regression: R1 Critical#2 的修复动作(step 5 整体重写)在解决 AC-1 黄金场景数学冲突的同时, 静默改变了"零 CAP 候选"(纯插件路由, 恰恰是 AC-3 承诺"逐字段等同基线"的场景)下的差值护栏边界, 有具体、非罕见的复现路径(0.05 置信度网格下 exact-0.10 差值组合很常见)。其余 7 条 Major 集中在两类: (a) R1 Critical#1 的"半确定性"关闭质量被 L1 覆盖率证据(24% 词表对齐 + 主调用方不传参)证伪为纸面关闭; (b) §4 缓存修复窄化但未消除原问题, 且与既有配置复合语义空白。均需 rework, 不建议直接进 A.2。

## 核验锚点

- `openspec/changes/agent-router-auto-project-agent-injection/proposal.md:58-62`(step 5 重写)、`71-80`(§2.1 L1/L2)、`94-113`(§2.4 R-a/R-b/R-c)、`132-139`(§4 缓存)、`188`(Risk 行)
- `aria/skills/agent-router/SKILL.md:137`(task_type 默认)、`257-262`(subagent-driver 调用契约)、`383-389`(错误处理表)、`416-421`(同名保护既有文字)、`429-431`(cache_ttl_seconds 既有配置)
- `aria/skills/agent-router/ROUTING_RULES.md:30`(FP-002)、`43`(FP-015)、`59-85`(TT 表)、`190-201`(优先级处理既有 <0.1 规则)
- `aria/references/capabilities-taxonomy.yaml:18-25,30-33,42-43,54-55,86-87`(tag/synonym 对照)
- `aria/skills/agent-gap-analyzer/SKILL.md:53-57`(match_rate>=0.5 covered 门槛, 对照 R-a 的 1.0 门槛)
