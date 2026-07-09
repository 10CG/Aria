# agent-router-auto-project-agent-injection — auto 路由消费项目级 Agent (发现 B)

> **Level**: 3 (Full — 两段式决策规则 + 输出契约扩展 + 缓存 schema 变更 + 配置增补)
> **Status**: done (Rev4; shipped v1.55.0 2026-07-09, aria-plugin#98 + Aria#155)
> **Created**: 2026-07-08
> **Parent Issue**: [#153](https://forgejo.10cg.pub/10CG/Aria/issues/153) 发现 B
> **Target**: agent-router SKILL v1.1.0 → v1.2.0; aria-plugin v1.53.0 → v1.54.0 (Skill 逻辑变更 = MINOR)
> **Grounding**: `openspec/archive/2026-04-11-agent-project-adapter/proposal.md` (D4 盲点) + `aria/skills/agent-router/SKILL.md` §205/§232/§393 + `aria/skills/agent-router/ROUTING_RULES.md`

## Why

`agent-project-adapter` (v1.13.0) 建成了「生产者 → 中央登记处 `.aria/agents/` → 多消费者」的项目级 Agent 集中管理架构。agent-router 是其中最核心的消费者 (任务路由), 但 **auto 路径从不真正消费 `.aria/agents/`** —— 中央登记处建好了, 主消费者的自动通道是断的。

对着真代码 (agent-router 是纯 prose 驱动 Skill, `context: fork` + general-purpose, 无 Python) 核实, 三处缺陷:

1. **孤儿段** — SKILL.md §393「项目级 Agent 发现 (v1.1.0)」整段贴在文末, 从没接进 §205「执行流程」。§221 step 3「规则匹配」只列 文件路径 / 任务类型 / 技术栈 / 关键词 四个平级子项, 无 capability 注入步骤。
2. **短路 return** — §232 step 5 `if top_confidence >= threshold: return`。FP/TT 命中插件级 Agent (≥0.9) 直接 return, `.aria/agents/` 扫描永远轮不到。
3. **无评分规则** — ROUTING_RULES.md 只有 FP/TT/关键词/技术栈四张表, **没有 capability-match 评分规则**。§393 说"按 capabilities 路由", 但没有成文的确定性算法。(连带: SKILL.md 自身版本标记已漂移 — L17 header `1.0.0` vs L449 footer `1.1.0`。)

**实证** (#153, cesura 项目): `.aria/agents/database-specialist.md` (capabilities=[orm-migration, query-optimization, database-schema]) 存在。给 router 一个 DB 迁移任务:
- 第一次 auto 跑: 只走 FP(backend/**)+TT(database-schema) → `backend-architect` (0.95) 短路收工。`database-specialist` **从没进候选池**。
- 第二次显式要求"扫 `.aria/agents/` 并注入候选": router 正确列 12 候选, `database-specialist` 3/3=1.00 决定性胜出 (次优 backend-architect 0.33)。

即项目级 Agent 在自动路径上**形同虚设**, 只有显式要求扫描才生效。

**对上游 Spec 的关系**:
- `agent-team-audit-project-agent-augmentation` (2026-06-21) proposal L16「triage 已确认 agent-router **会**扫 `.aria/agents/`」—— 该假设对 auto 路径为假, 本 change 修好后才兑现其表述。其决策文件 `.aria/decisions/DEC-20260621-001-agent-team-audit-project-agent-augmentation.md` 内有**两处**同源失实前提: **L13**「agent-router v1.1.0 **已实现**所需机制——扫描 `.aria/agents/*.md` → 合并候选 → 按 capabilities + FP/TT/关键词路由」与 **L90**「triage 已确认那条路正常 (项目 agent 在任务路由已被感知)」(L21 借力表述顺带), §6 按实文逐处加勘误注记。
- `aria-2.0-m7-agent-lifecycle` L129 **显式声明**「本 Spec 不依赖任何未实现的 routing 能力, 也不改 agent-router」(pin 真实版本 v1.1.0) —— M7 **不依赖**本 change; 本 change 使 M7 描述的 routing-context 注入在 auto 路径成真, 但非其前置。本 change 将 agent-router bump 到 v1.2.0, M7 Phase B 启动时其 v1.1.0 black-box pin 需 re-baseline (**输入契约 additive 扩展** — 新增可选 `required_caps` 参数; **输出 additive 扩展** — agent_source/decision_path 等新字段; 均对 M7 无害)。

**根因 (设计盲点, 非退化)**: agent-project-adapter D4 把选择框成二选一「Plugin 静态注册 vs Skill 运行时注入」, 正确选了后者, 但 §393 只把它写成"文末补充说明", 没落进主执行流程与评分规则。运行时注入的**机制**从未在 auto 路径成文实现。US-011 (标记 done) 的 **AC-4 / D4 / Scope** 三处因此含已被 #153 证伪的「运行时注入已兑现」表述, 本 change 一并回溯订正 (见 What §6)。

**修复效果的预期管理** (R4 1e54a002): 核心可见性修复 (项目级 Agent 进候选池 / 进 recommend Top-3) **不依赖**推断精度; R-a **自动直派**额外依赖推断产出 |required_caps| ≥ 2 (生产自然语言路径推断可能只出 1 个 tag → 单标签禁令优雅降级 recommend — agent 仍现身, 由人一键选中)。#153 的"形同虚设"被修复为"至少可见、精确对位时自动直达"。

## What Changes

### 1. SKILL.md §205「执行流程」— 项目级 capability 匹配接入主链 (行为契约变更)

step 3「规则匹配」**忠实保留源文件 4 个平级子项**, 新增第 5 子项; step 5 决策**仅重写 auto 分支的跨池部分**, recommend / manual 分支显式保留:

```
  3. 规则匹配:
     ├── 3a 文件路径匹配 (FP)          ← 既有
     ├── 3b 任务类型匹配 (TT)          ← 既有
     ├── 3c 技术栈匹配                 ← 既有
     ├── 3d 关键词匹配                 ← 既有
     └── 3e 项目级 capability 匹配 (v1.2.0 新增, 主链默认步, 受配置门控):
         ├── 门控 (最先判定, 命中即整步不执行 — 含同名检测/吸收在内的一切 3e 逻辑):
         │   agent_router.plugin_only == true 或 scan_project_agents == false
         │   → 跳过 3e, 退化纯基线 (输出 shape 完全等同旧版)
         ├── 扫描 .aria/agents/*.md (缓存见 §4)
         ├── frontmatter 健壮性: capabilities 缺失/非 list/YAML parse 失败 → skip 该
         │   agent 不阻断; 空 list → 合法 (零命中)
         ├── 同名保护复合 (B12): 候选池构建期先按名去重 — 项目级与插件级同名 →
         │   项目级替换插件级候选 + 输出警告; 幸存项目级候选**吸收**插件级按名命中的
         │   全部 FP/TT/技术栈/关键词 confidence (名匹配语义随名走, 保持 v1.1.0 §416
         │   「覆盖插件级路由」= 接管其路由的语义); agent_source 恒 = project;
         │   其自身 CAP 分数照常另算; **裁决消歧见 §2.4-B12**
         ├── 读 capabilities, 经 taxonomy 归一 (语义见 §2.2)
         └── 按 §CAP 评分产出项目级候选 (match_rate > 0 才产出候选; 候选携带
             match_rate + |matched| + |required_caps| + precision + off_taxonomy_tags)

  4. 置信度聚合:
     └── 基线候选 (FP/TT/技术栈/关键词) + 项目级 CAP 候选进入同一候选池
         (各候选携带 agent_source 标记; B12 吸收候选凭吸收分归**基线侧**参与;
          其 CAP 分录**仅用于 recommend 排序与 trace, 不参与 Stage 2 auto 挑战者
          遴选** — 见 §2.4-B12, R4 4d6a7c73 收紧)

  5. 模式决策 (伪代码骨架 — 仅 auto 分支重写, 其余分支保留):
     ├── if mode == manual: 既有逻辑不变 (user_agent 显式指定时于 step 2 前置返回;
     │   未指定时等待指定 — 两形态均不经 3e 评分, R4 f8b35406 注释修正)
     ├── if mode == auto: 两段式 (§2.4):
     │   Stage 1 基线裁决: 基线侧候选 (含 B12 吸收分) 按既有规则得出 baseline
     │           决策 + baseline_top — 本段规则与今日行为一致 (含**基线侧候选间**
     │           差值 < 0.1 严格降级, 沿用 ROUTING_RULES §优先级处理「多个 Agent
     │           置信度相近 (差值 < 0.1)」既有规则, R4 5f46109b 措辞修正:
     │           吸收候选亦受此降级检查, 不因 agent_source=project 逃逸)
     │   Stage 2 项目级 CAP 挑战 (仅当存在纯 CAP 项目级候选): R-a → R-b → R-c;
     │           无 CAP 候选 → 直接采纳 Stage 1 决策
     │   (auto 内部任何降级产出的 recommend 输出, 同样按 §2.6 混排, R4 64fd85e6)
     └── if mode == recommend: Top-3 生成 (混排规则见 §2.6), 既有分支保留
```

**关键**: 项目级候选在 step 5 裁决**之前**已入池 → 堵死 §232「FP/TT 局部最高先 return」短路。

### 2. ROUTING_RULES.md 新增 §CAP capability-match 评分与决策规则

#### 2.1 required_caps 确定 — 显式传参优先 + 两级闭集推断

```
第 0 优先 — 显式传参 (v1.2.0 新增可选输入参数, additive):
    router 输入参数表增 required_caps (可选, list of tag)。显式传入 → 跳过 L1/L2
    推断, 经 taxonomy 归一后采用; **无法归一的传入值 (off-taxonomy/拼写错) → 剔除 +
    WARN, 不进入 required_caps 分母** (R4 c2e66062/ce1967f7)。
    fixture 与高级调用方由此获得推断-裁决解耦。

无显式传参时 — 两级闭集推断:
L1 (机械, 可复算): 对 taxonomy (tag 名 + synonyms) 的词边界全名命中:
    - 显式传入的 task_type 参数值 == tag 名或 synonym (单值参数, 最多贡献 1 个命中)
    - task 文本 / files 路径中逐字出现 tag 名或 synonym
L2-negation (恒时执行, 不受下方启用条件门控):
    执行 agent 可依据相反证据 token 将 L1 命中标记 negated 并移除 (须引用原文证据)
L2-addition (受启用条件门控): 语义补充 tag, 约束:
    (a) taxonomy 闭集; (b) 每 tag 引用证据 token; (c) 标记 inferred=semantic;
    (d) 上界 3 个; (e) 启用条件: 仅当 |L1_hits − negated| < 2 (净值计数)

编排: required_caps = (L1_hits − negated) ∪ L2_additions
去重按 canonical tag; required_caps 为空 → CAP 候选空集 → 纯基线
```

**确定性定位 (诚实版)**: agent-router 是 prose Skill, FP/TT 匹配同样由 LLM 执行 (受确定性规则表约束 — 既有性质, 本 change 不改变)。§CAP 的确定性 = 「显式传参全机械 + L1 机械可复算 + L2 闭集/证据/上界受约束 + 推断轨迹落输出字段可审计」。生产自然语言路径 (无传参) 以 L2 为常态。

#### 2.2 归一语义

- tag 在 taxonomy (名或 synonym) → 归一到 canonical tag
- **off-taxonomy 自造标签 = 惰性**: 不可能命中 required_caps (零分), **也不计入 precision 分母** — 惰性标签无匹配力, 不构成劫持向量, 计入分母只会错杀携带遗留/自定义标签的真 specialist。候选条目输出 `off_taxonomy_tags` 提示 (§3)。

#### 2.3 评分公式

```
valid_caps = normalize(agent.capabilities) ∩ taxonomy 词表      # off-tax 惰性排除
matched    = valid_caps ∩ required_caps
match_rate = |matched| / |required_caps|                        # 覆盖率, [0,1]
precision  = |matched| / |valid_caps|                           # 精度; valid_caps = ∅ →
                                                                #   不产出候选 (含除零防护)
match_rate == 0 → 不产出候选 (不入池, 不进 recommend)
```

> 防劫持语义: generalist 靠**有效标签**堆宽度 → precision 被稀释 → R-a 拒之门外;
> off-tax 标签不增加任何匹配力, 故不参与该攻防。

#### 2.4 auto 决策规则 (两段式)

**Rationale**: 唯一硬理由是数学事实 — CAP match_rate 上限 1.0, 对 confidence >0.9 的插件对手差值恒 <0.1, 纯数值比较 + 差值护栏会把 #153 黄金场景**恒降级 recommend**。故为 exact-full-match 设 R-a 序数快路; R-b 的跨刻度数值比较是**有界务实近似**, 不声称两刻度同量纲。

```
Stage 1 — 基线裁决 (规则与今日一致):
    基线侧候选 = FP/TT/技术栈/关键词候选 + B12 吸收分候选 (若有)
    按既有规则: 同 Agent 多规则取最高 → 全局排序 → **基线侧候选间**差值 < 0.1 (严格,
    沿用 ROUTING_RULES §优先级处理「多个 Agent 置信度相近」既有规则; 吸收候选一并
    适用) → 降级 recommend; threshold 检查照旧
    产出: baseline 决策 + baseline_top

Stage 2 — 项目级 CAP 挑战 (仅当池中存在纯 CAP 项目级候选; 无则采纳 Stage 1):
    挑战者 = **纯 CAP 候选** (B12 吸收候选的 CAP 分录不参与遴选, 防自我挑战 —
             R4 7c9cfa4e 显式) 中 match_rate 最高者 (再平按 §2.5)

    R-a 决定性直派 (序数快路):
        挑战者满足: match_rate == 1.0 AND |required_caps| >= 2 AND precision >= 0.5
        → auto 直派挑战者 (多候选同满足 → §2.5 tiebreak, AC-10)
    R-b 跨池数值裁决 (R-a 不满足; **按序判定, 先匹配先裁决** — R4 bd89d02f/8e74045b
        MECE 化, d = 挑战者 match_rate − baseline_top confidence):
        (0) |required_caps| == 1 的挑战者永不 auto 直派, 仅进 recommend
        (1) |d| <= 0.1 → 降级 recommend                    # 近分先判, 含 R-c 同分
        (2) d > 0.1 且 match_rate >= threshold → 直派挑战者
        (3) d > 0.1 且 match_rate <  threshold → 降级 recommend (领先但不够格)
        (4) 其余 (d < -0.1, baseline_top 显著领先) → 采纳 Stage 1 决策
    decision_path 赋值通则 (R4 63c17b55): R-b 评估中结论 = 采纳 Stage 1 (分支 4)
        → decision_path = baseline; 由 R-b 逻辑裁定 (分支 0/1/2/3) → decision_path = R-b

B12 吸收候选裁决消歧:
    - 吸收的 baseline confidence 是该候选在 auto 裁决中的 governing confidence,
      于 Stage 1 按基线侧参与 (可以成为 baseline_top, 也受基线侧 <0.1 近分降级检查);
      其自身 CAP match_rate 仅用于 trace 与 recommend 排序, 不作为 auto 挑战分数
    - 凭吸收分胜出 → decision_path = "baseline" + agent_source = "project"
      (组合语义 = 「同名接管」)
    - junk-caps 同名候选 (match_rate == 0): 无 CAP 候选产出, 仅以吸收分走 Stage 1
      — 一切候选恒有唯一归属 (吸收分→Stage 1; 纯 CAP 分→Stage 2)
```

**R-a 覆盖面诚实刻画**: |required_caps| 大时全命中率下降, R-a 只服务「需求标签集中且 specialist 精确对位」场景 (#153 型), 其余走 R-b/recommend; L2 上界 3 防膨胀。

#### 2.5 CAP 候选互相平局

match_rate 相等的项目级候选之间: precision 高者优先, 再平 → agent name 字典序。(跨池不适用。) 理论注记: 项目级互相 0<差值≤0.1 近分无专门护栏 — 需 |required_caps| ≥ 10 才可达, 现实几乎不可达, 接受。

#### 2.6 recommend Top-3 混排

```
排序: (1) R-a 合格候选置顶 (若有);
      (2) 其余按 confidence 数值降序混排 (项目级 CAP 候选用 match_rate, 基线候选
          [含 B12 吸收候选] 用基线 confidence; 跨刻度务实近似, recommend 由人裁决);
      (3) 同分 → 项目级列前, 再平字典序
候选条目携带 agent_source (+项目级候选带 off_taxonomy_tags); decision_path 为
decision 级单值字段, 不逐候选携带
max_candidates 仍为 3 (居 legacy config, 见 §5 限定语)
本节适用于一切 recommend 输出 — 原生 recommend 模式与 auto 内部降级产出者同
```

### 3. 输出契约 (范围收窄版)

**仅 `auto_match` 与 `recommend` 两种输出**、且**仅当 3e 实际执行时** additive 增加:

```yaml
agent_source: "plugin" | "project"        # auto_match: 胜出者; recommend: 每候选条目
decision_path: "R-a" | "R-b" | "baseline" # decision 级单值; 赋值通则见 §2.4;
                                           # baseline+agent_source=project = 同名接管
required_caps_trace:
  explicit: <bool>                         # 显式传参时 true, l1/l2 为空
  l1: [<tag>, ...]
  l2: [{tag: <tag>, evidence: "<原文 token>"}, ...]
  negated: [<tag>, ...]
off_taxonomy_tags: [<tag>, ...]            # 项目级候选条目级 (auto_match 胜出者为项目级时同带)
warnings: [...]                            # 既有输出惯例 (同名警告等), AC 断言载体之一
```

- **manual / fallback 不加** (manual 不经 3e; fallback 恒 general-purpose)
- **3e 被门控跳过 / `.aria/agents/` 空时: 输出 shape 完全等同旧版, 不含任何新字段**
- subagent-driver `references/handoff-contract.md:14,33` 预留字段 `agent_source` 的供给侧接线; subagent-driver 契约不改

### 4. 缓存失效修复

```
缓存 schema (.aria/cache/project-agents.json):
    last_full_scan: <int epoch seconds UTC>    # TTL 判定基准 (格式定案, R4 f8b8ca9e)
    files: [{path, mtime[ns 精度, 可用时], size}, ...]
主判: 每次 3e stat 集合比对, 任何差异 (增/删/改) → 重建 + 更新 last_full_scan
已知残余窗口 (诚实标注): 同秒 (纳秒不可用) + 字节数不变的原地编辑可能漏检 —
    兜底 1: cache_ttl_seconds; 兜底 2: rm .aria/cache/project-agents.json 逃生门
cache_ttl_seconds 语义重定义 (更严方向): >0 = 即使 stat 一致, now − last_full_scan
    超 TTL 也强制重建; 0 (默认) = 仅 stat 比对。旧注释随 §393 更新
写入健壮性: .aria/cache/ 不存在 → mkdir -p; 写入失败 → WARN + 直读 frontmatter
    不阻断; tmp + rename 原子写。旧 schema 缓存 (无 last_full_scan) → 视为失效重建
```

### 5. 配置: 门控归口 + template 补齐

- 3e 门控消费 `.aria/config.json` `agent_router.*`; **限定语: `.aria/config.json` 是本 change 新增/收编的 3 个门控 key 的 SOT; 既有 threshold / max_candidates / default_mode 等仍居 legacy `.claude/agent-router-config.json` (§277), 迁移 OOS**
- 3 key 全枚举: `scan_project_agents` (默认 true) / `plugin_only` (默认 false) / `cache_ttl_seconds` (默认 0, §4 新语义)
- `.aria/config.template.json` 补 `agent_router` 块 (3 key + 注释)
- SKILL.md §277 标注 legacy + 指向本节

### 6. 版本 + 文档同步 (Rev4 全量清单)

**agent-router 自身**:
- SKILL.md **L17 header 行整体更新** (版本号 1.0.0→1.2.0 及邻接日期/说明文字) + **L449 footer** 1.1.0→1.2.0 (YAML frontmatter 无 version 字段); §132 输入参数表增 `required_caps` 可选参数行
- §393 改写: 保留 D4 rationale + 删「已生效」暗示 + 缓存子段 §4 新语义 + 「FP/TT/关键词 + capabilities」措辞修正为「FP/TT/技术栈/关键词 (基线) + capabilities (项目级)」+ §277 legacy 标注
- **连带 10 段** (计数统一, R4 bc0b0447/c41deac8/2da43e11): §35 核心功能表 / §47 自动模式概览 (两段式简述) / §93 路由规则 (+§CAP 呼应) / §132 输入参数 (+required_caps) / §145 输出格式 (+§3 字段) / §250 subagent-driver 集成 (提及 agent_source) / §305 能力矩阵 (项目级动态注记) / §323 使用示例 (+项目级 R-a 胜出示例) / §383 错误处理 (+3e 退化行) / §438 相关文档 (+ROUTING_RULES.md)
- ROUTING_RULES.md: L3 文首版本 1.0.0→1.1.0 + §CAP (2.1-2.6) + 维护指南规则类型枚举 → **五类 (FP/TT/关键词/技术栈/CAP)**
- `aria/references/capabilities-taxonomy.yaml` 头注释补 agent-router 消费者

**发版清单** (对齐主仓 CLAUDE.md 版本发布检查清单原文):
- SOT: plugin.json; 派生: marketplace.json (两处 version) / VERSION / CHANGELOG.md / README.md
- 主仓: submodule pointer bump + 主仓 VERSION + root README badge (m6-version-badge-match)
- i18n README: 纯 badge/版本变更 → 免重译 (#140 B 档)

**上游文档回溯**:
- US-011.md **AC-4 / D4 / Scope 三锚点** errata: 「agent-router 运行时注入」v1.13.0-v1.53.0 auto 路径未真正生效 (#153 发现 B), v1.54.0 兑现
- DEC-20260621-001 **两处**勘误 (按实文): **L13**「已实现所需机制——扫描…路由」与 **L90**「那条路正常 (项目 agent 在任务路由已被感知)」— 对 auto 路径失实, 注记指向 #153 + 本 change (L21 借力表述顺带一并)

## Decision Records

| ID | 决策 (Rev4) | 理由 |
|----|------|------|
| B1 | 3e 主链默认步, 门控最先判定; 跳过支输出 shape 等同旧版 | 接主链 + 关闭退路 + 零回归含 shape |
| B2 | 两段式: Stage 1 基线裁决 (基线侧候选间 <0.1 一并适用吸收候选) → Stage 2 纯 CAP 挑战 (R-a 序数 / R-b 有序四分支 / R-c 并入) | 零回归 by construction; MECE 有序判定 (R4 bd89d02f); 吸收候选不逃逸近分检查 (R4 5f46109b) |
| B3 | required_caps: 显式传参 (归一失败值剔除+WARN) > L1 词边界 > L2 (negation 恒时 / addition 净值 <2 启用+上界 3) | 推断-裁决解耦; 分母防污染 (R4 c2e66062) |
| B4 | precision 门 + tiebreak; 分母 = valid_caps (off-tax 不计); valid_caps=∅ 不产出候选 | 惰性标签非劫持向量; 除零防护 (R4 backend-architect) |
| B5 | 差值护栏: Stage 2 跨池 ≤0.1 (含, 先判); Stage 1 基线侧沿用 <0.1 严格 | 边界显式且不篡改基线; AC-13 防再犯 |
| B6 | 零回归三支: 行为与输出 shape 逐字段等同旧版 | Rule #4 |
| B7 | 发现 A → M7 agent-lifecycle B.2 | 范围不重叠 |
| B8 | 输出 additive (agent_source / decision_path 单值+赋值通则 / trace / off_taxonomy_tags / warnings 断言载体); 仅 auto_match+recommend 且 3e 执行时 | 下游区分 + 机械断言载体 (R4 3893dad4 warnings 入清单) |
| B9 | 缓存: last_full_scan (int epoch) + per-file + TTL 更严 + 原子写 + 失败降级 + 旧 schema 重建 | 可执行且格式定案 |
| B10 | off-taxonomy 惰性 + 候选级提示 | 确定性 + 不错杀 |
| B11 | §CAP 仅对项目级候选评分 | 插件级已有成熟刻度; 留观 |
| B12 | 同名替换: 吸收 confidence 走 Stage 1 基线侧 (可为 baseline_top, 受近分检查); CAP 分仅 trace/recommend (不参与挑战者遴选); 胜出 = baseline+project (同名接管) | 唯一归属无“无人区”; 防自我挑战 (R4 7c9cfa4e 显式) |

## Impact

| Type | Description |
|------|-------------|
| **Positive** | agent-creator 生成物在 auto 路径真正被消费; gap→create→route 闭环兑现 (可见性不依赖推断精度; R-a 直派依赖 \|req\|≥2, 否则优雅降级 recommend — 见 Why 预期管理) |
| **Positive** | 兑现 audit-augmentation L16 表述; 使 M7 描述的注入在 auto 成真 (非其前置) |
| **向后兼容 (Rule #4)** | 三支零回归 (行为+shape); Stage 1 基线规则一致 (吸收候选按既有规则参与); 新字段仅 3e 执行时输出 |
| **无新 artifact** | 复用既有文件; 缓存 json 内部 schema 升级 (旧文件直接重建) |
| **波及面刻画** | recommend: 项目级按 §2.6 混排进 Top-3; manual: 不经 3e; fallback: 不变 |
| **Risk** | R-a 覆盖面窄: 仅 specialist 精确对位场景, 其余走 R-b/recommend — 设计取舍 |
| **Risk** | 宽标签劫持面: precision 门仅锁 R-a 快路; R-b 分支 2 对 match_rate 1.0 宽标签候选仍开 (AC-16 锁定该风险接受实证), 由护栏/threshold/单标签禁令约束; owner 保持标签精准 (off_taxonomy_tags/trace 辅助) |
| **Risk** | B12 同名静默接管: 同名+低质 caps 项目级 agent 在 auto 凭吸收分被直派; 缓释 = 同名警告 + baseline+project 组合可察 + plugin_only 逃生门; owner 对 .aria/agents/ 命名负责 |
| **Risk** | L1 假阳性经 negation 恒时执行收窄; 残余: negation 依赖语义判断非机械 |
| **Risk** | L2 语义补充有界不确定; 缓存 stat 粒度残余窗口 (TTL+清缓存兜底); M7 v1.1.0 pin 需 re-baseline |

## Out of scope

- ❌ 发现 A (原生列表 / `.claude/agents/` 物化) → M7 agent-lifecycle B.2 (#128)
- ❌ `.aria/agents/` 存储位置 (D1 不变)
- ❌ subagent-driver 契约 (agent_source 为其预留字段, 仅供值)
- ❌ taxonomy 词表内容 (只消费 + 头注释)
- ❌ 插件级 capabilities 参与评分 (B11 留观)
- ❌ §277 legacy config 迁移 (仅标注; threshold/max_candidates 等居 legacy)
- ❌ 同 session 即用 (软注入 pattern)

## 验收标准 (AC)

> 验证手段: structural fixture。裁决类 AC (AC-1..AC-8, AC-10..AC-14, AC-16) 一律显式传参 `required_caps` pin; 推断层由 AC-15 专项覆盖 (在**非空 `.aria/agents/` fixture** 下跑, R4 bffd81d4)。断言为结构化字段级 (agent / status / agent_source / decision_path / off_taxonomy_tags / **warnings**), reason 不比字节。每 AC 双跑; 双跑不一致处置 = 判 fail 并回炉 SKILL 文本消歧, 无容忍阈值。Stage 1 基线匹配为 LLM 执行但受确定性规则表约束 (既有性质, 双跑一致要求覆盖全输出)。

- **AC-1** (正召+决定性直派, #153 复现): database-specialist (3 caps); required_caps=[orm-migration, database-schema] → decision_path=R-a, auto 直派, agent_source=project。
- **AC-2** (不误召): (a) required_caps=[interface-design] → 零命中不产出候选; (b) 单标签禁令: required_caps=[query-optimization], 项目级 1/1=1.0, 基线 top 0.85 (d=0.15 — 无禁令则 R-b 分支 2 直派; 有禁令 → recommend) → 断言 recommend + decision_path=R-b。
- **AC-3** (零回归三支): (a) 空/不存在; (b) plugin_only:true **且 fixture 含同名 backend-architect 文件**; (c) scan_project_agents:false → 行为与输出 shape 均等同纯基线 (与旧 SKILL 文本基线对照)。
- **AC-4** (跨池护栏): (a) required_caps 3 个, 项目级 2/3≈0.67 vs baseline_top 0.90 (d≈−0.23, R-b 分支 4) → 采纳 Stage 1, decision_path=baseline; (b) 宽标签 (valid caps 8, matched 2, precision 0.25) match_rate 1.0 → R-a 拒, R-b: baseline_top 0.95, d=0.05 → 分支 1 → recommend。
- **AC-5** (堵短路): FP/TT 命中 0.95 插件 agent 时, 项目级候选仍进池且 R-a 满足时胜出。
- **AC-6** (recommend 混排): 项目级候选按 §2.6 进 Top-3, 排序可解释, 候选带 agent_source。
- **AC-7** (frontmatter 边界): capabilities 缺失/非 list/parse 失败 → skip 不阻断; 空 list 合法。
- **AC-8** (输出契约): 3e 执行时 auto_match/recommend 含 agent_source + decision_path + required_caps_trace (显式传参 explicit:true); manual/fallback 不含。
- **AC-9** (文档同步机械核对, **两段式拆分** — R4 918a4d69): **AC-9a 插件侧** (SKILL/ROUTING_RULES/taxonomy/插件 5 文件, TASK-017 于 TG-E 内核对) + **AC-9b 主仓侧** (config.template/US-011/DEC/主仓 VERSION/badge/pointer bump, TASK-018 于 Phase C 末核对)。
- **AC-10** (R-a 平局): 双 R-a specialist fixture → precision 高者胜。
- **AC-11** (off-taxonomy 惰性): off-tax 标签不计分不稀释 precision, 候选条目 off_taxonomy_tags 列出。
- **AC-12** (同名接管): fixture 项目级 backend-architect caps=[api-design]; 任务 backend/api/** (FP-001 0.90 + FP-002 0.95 双命中同 agent 取 max = 0.95 被吸收 — ROUTING_RULES 自身示例 L177-185 佐证该 glob 语义, R4 d7b1e41b 核验存证), required_caps=[api-design, database-schema] (match_rate 0.5, 无 R-a) → auto 直派 (凭吸收分走 Stage 1), decision_path=baseline, agent_source=project, **warnings 含同名警告** — 四元组断言。
- **AC-13** (R2-Critical 防再犯): 纯插件双候选 confidence 差恰 =0.1 (0.95/0.85), 无项目级 → 沿用既有 <0.1 严格 (=0.1 不降级) → auto 直派 top, 无新字段, 与旧基线对照一致。
- **AC-14** (缓存端到端): 路由一次 → 原地编辑 agent capabilities (**编辑须改变文件字节数**, 避开 §4 残余窗口致假 fail, R4 08086335) → 再路由 → 新 capabilities 生效。
- **AC-15** (推断层专项, 非空 fixture 下): 不传 required_caps; 任务文本逐字含 2 tag 全名 → trace.l1 含二者 (explicit:false); 否定语境 fixture → negated 移除生效。L2-addition 语义不断言。
- **AC-16** (R-b 分支 2/3 覆盖, R4 bb6041c8): (a) 宽标签 match_rate 1.0 / precision 0.25 / baseline_top 0.85 (d=0.15, ≥threshold) → R-b 分支 2 直派 (锁定 Impact 已登记风险的接受实证); (b) 挑战者 match_rate 0.75 vs baseline_top 0.60 (d=0.15, <threshold 0.9) → 分支 3 → recommend。

## Resolved (Rev1 — post_spec R1, 39 deduped findings)

| R1 finding (id) | severity | 处置 (最终版) |
|----|----|------|
| required_caps 无确定性来源 (6dc8588a/866a9c98/73eba2dc) | **Critical** | §2.1 显式传参 + 两级闭集编排 + AC-15 |
| B5 与 AC-1 数学冲突 (d378eb8a/af713ec5) | **Critical** | §2.4 R-a 序数快路 + rationale 重写 |
| 量纲失配 + 单标签饱和 (92358876/24b743aa/f8c242e4) | Major | R-a/R-b + 单标签禁令 + AC-2(b) |
| 跨池同分 + "与既有一致"不实 (0c20a9e0) | Major | R-b 有序分支 1 + Stage 1 声明 |
| 3e"强制" vs 配置开关 (01c95136/5155b495/5b54f55f/1d35911a-a) | Major | §1 门控 + §5 三 key + AC-3 |
| 同名保护复合 (450102ae) | Major | B12 + §2.4-B12 + AC-12 |
| 输出无来源层 (d444327d/9aa59e37) | Major | §3 + AC-8 |
| 缓存原地编辑 (e7a6b2b5/94801d3c) | Major | §4 + AC-14 |
| off-taxonomy (0db5a671) | Major | §2.2 惰性 + AC-11 |
| 差值规则孤儿 (7c110f13) | Major | step 5 两段式成文接线 |
| recommend 无 AC (83779e5f/02d35656/9926aa3b) | Major | AC-6 + §2.6 |
| AC-3 逐字节不可判定 (f01c7b19/ba76a232) | Major | 结构化字段级总注 |
| frontmatter 边界 (f4da105a) | Major | §1 + AC-7 |
| 文档同步范围 (4c38e2e1/e8a82d88/25408aa1/2bda53a7/b2de157a/ab490f33/1d35911a-b) | Major/Minor | §6 全量 + AC-9 |
| US-011 (54e7101d) | Major | §6 三锚点 errata |
| §408 framing (f2a4ac9a/8b92dbe8) | Minor | §6 保留 D4 rationale |
| M7 表述 (262e329e) | Minor | Why 重写 |
| 3a-3c 漂移 (053b5cba) | Minor | §1 忠实 4+1 |
| SKILL L17 版本 (bade152e) | Minor | §6 (含邻接文字) |

> R1 表注: 1d35911a 以 -a/-b 后缀区分两个独立 finding; 正文与表 id 统一 8 位。

## Resolved (Rev2 — post_spec R2, 49 deduped findings)

| R2 finding (id/簇) | severity | 处置 (最终版) |
|----|----|------|
| 差值边界静默改+波及纯插件 (1a1d3115/1ba6f643) | **Critical** | 两段式 + Stage 1 沿用 <0.1 + AC-13 |
| R-a 宽标签劫持 (eabedb99) | Major | precision 门 + AC-16 风险实证 |
| rationale 矛盾 (ab462321) | Major | §2.4 rationale 重写 |
| 同名得分归属 (596796f6/58fdd64d/ad0fde48/a9988e4d) | Major | B12 + §2.4-B12 + AC-12 |
| L2 无输出载体 (b4aeb123/d4ea6516) | Major | §3 decision_path/trace + AC-8 |
| L1/L2 编排 (cf4aa23e/5e35cfee/ad935a3a) | Major | §2.1 (negation 恒时 + 净值 + 显式传参) |
| task_type 失实 (f3677340/87ff93a7) | Major/Minor | §2.1 单值注记 |
| R-a 覆盖面 (762b7952) | Major | 诚实刻画 + L2 上界 + Why 预期管理 |
| 缓存簇 (97cb686e/c40b3889/ca38f800/e7d5f1d3/345c4246) | Major/Minor | §4 完整化 |
| 插件级 capabilities (c0e74580) | Major | B11 + OOS |
| step5 吞分支 (2b6e2b60) | Major | step 5 三分支骨架 |
| 清单缺项 (be54898b/21ed1c4c/1e5bcf08/4f933d9e) | Major/Minor | §6 (DEC 两处定位) |
| D9 归因 (bac15556/01c79c30/9b3c4ed7) | Major/Minor | §416 实现语义表述 |
| agent_source 全形态 (e16ad9fc/ce10e1d9) | Major/Minor | §3 收窄 |
| AC-2(b) 区分力 (91c8e97b/4a3f5098) | Major | 0.85 参数 + 显式传参 |
| recommend 排序 (308d52af) | Major | §2.6 |
| US-011 锚点 (6eba1f5c) | Major | §6 三锚点 |
| 其余 minor 簇 (5e88d186/822165ba/9681f9b2/8cb5b4cd/b549d1ee/74dce1fc/814e68de/a1fd3131/f3d5f9b9/36e88095/b304c182/25220fa6) | Minor | shape/Level 3/五类/措辞/AC 归属/id 卫生/AC-10..11/零分/Rule #6 |

> R2 表注: 簇合并展示; 逐 id 全集 (49) 见 `.aria/audit-reports/post_spec-R2-*` 五份报告 (R4 a1298281)。

## Resolved (Rev3 — post_spec R3, 37 deduped findings)

| R3 finding (id/簇) | severity | 处置 |
|----|----|------|
| B12 混合候选无人区 (79070f61/ff4315de/95d37650/4b94a576) | Major×3+m | §2.4-B12 消歧 (R4 确认真关闭, tech-lead 双读法实测收敛) |
| negation 连坐 (b59e5149/bebaa452/84638119/975f2c51/a5d2ae2a) | Major×2+m | §2.1 恒时 + 净值门控 |
| precision 分母 (9ab6adf4/80cc7a0f) | Major+m | §2.3 valid_caps 定案 |
| R-b 非 MECE (146fa0b3/2bf3e6d6) | Major×2 | 四分支 (R4 有序化终格) |
| trace 载体 (aa875cf8) | Major | §3 off_taxonomy_tags + AC-11 |
| 防再犯 AC (10c138df) | Major | AC-13 |
| 缓存零 AC (549515fe) | Major | AC-14 |
| AC-10 fixture (4f8dbb64) | Major | 双 specialist fixture |
| 其余 minor 簇 (d4230221/19b57114/8660ec54/8520f4ee/93d0156b/f9be7c6c/06ea177f/057b9fbe/b6fc6b5f/af073236/3b31fafb/a8676b50/5ee5fbbc/c9c7ef84/d4325bfd/a6cd04f6/0c63c7ae/e9439697/0c23dfae/1830cb7c) | Minor | Impact 登记/last_full_scan/挑战者规则/理论注记/DEC 两处/L17 整行/SOT 限定/id 卫生/decision 级单值/task_type 注/显式传参/双跑处置/组合 AC/tasks 划界与顺序 |

## Resolved (Rev4 — post_spec R4, 27 deduped findings 全处置)

| R4 finding (id/簇) | severity | 处置 |
|----|----|------|
| Stage 1「插件间」窄化 + 引语失实 + 吸收候选逃逸近分检查 (5f46109b/b6bbd096) | **Major**+m | §1/§2.4 Stage 1 改「基线侧候选间」+ 按源文原字「多个 Agent」引用 + 吸收候选显式一并适用 |
| 挑战者遴选未排除吸收 CAP 分录 (7c9cfa4e/4d6a7c73) | **Major**+m | §2.4 Stage 2 挑战者行显式排除 + step 4 措辞收紧 |
| AC-9/TASK-017 时序结构矛盾 (918a4d69) | **Major** | AC-9 拆 9a 插件侧 (TASK-017) / 9b 主仓侧 (TASK-018) |
| R-b C/D 区间重叠 (bd89d02f/8e74045b) | Minor | R-b 有序四分支 (先匹配先裁决, 近分先判) |
| decision_path 赋值通则 (63c17b55) | Minor | §2.4 通则成文 |
| R-b 分支 2/3 无 AC (bb6041c8) | Minor | AC-16 (a)(b) |
| 显式传参 off-tax 值 (c2e66062/ce1967f7) | Minor | §2.1 剔除+WARN |
| manual 注释失实 (f8b35406) | Minor | step 5 注释修正 |
| last_full_scan 格式 (f8b8ca9e) | Minor | int epoch seconds 定案 |
| valid_caps=∅ 除零 (backend-architect) | Minor | §2.3 不产出候选 |
| 连带段计数 9 vs 10 (bc0b0447/c41deac8/2da43e11) | Minor | 统一「连带 10 段」(tasks.md 同步) |
| Level 徽标术语 (2bb3ff6a) | Minor | 「两段式」统一 |
| DEC 第二处定位 (96391f18) | Minor | Why/§6 L13+L90 定位 |
| AC-12 数值 (836c9a7f vs d7b1e41b 交叉证伪) | Minor | 0.95 保留 + glob 语义佐证注 |
| AC-12 警告断言载体 (3893dad4) | Minor | §3 warnings 入断言字段清单 |
| AC-14 假 fail (08086335) | Minor | 编辑须改字节数注 |
| AC-15 需非空 fixture (bffd81d4) | Minor | AC 总注注明 |
| R2 表计数 (a1298281) | Minor | R2 表注 (逐 id 全集见 audit-reports) |
| 生产推断预期管理 (1e54a002) | Minor | Why 预期管理段 |
| Stage 1 LLM 性质 (9d275830) | Minor | §2.1 确定性定位补句 + AC 总注 |
| auto 内降级 recommend 混排归属 (64fd85e6) | Minor | step 5 + §2.6 适用范围句 |

## Estimation

| Task | 工作量 |
|------|--------|
| ROUTING_RULES.md §CAP (2.1-2.6) + L3 + 维护指南 | 2-3h |
| SKILL.md §205/step5/§393 + 连带 10 段 + 版本 | 3-4h |
| config.template + taxonomy 头注 + US-011/DEC 注记 | 0.5-1h |
| structural fixture AC-1..AC-16 (双跑) + 机械 AC-9a/9b | 4-6h |
| 发版 (插件 5 文件 + 主仓 3 项) | 0.5-1h |
| **合计** | **10-15h** |

## 后续 (本 proposal 外)

- post_spec convergence: R1 39 (3C+25M, FAIL) → R2 49 (1C+28M) → R3 37 (0C+12M, PWW) → R4 27 (0C+3M, PWW; tech-lead/qa-engineer PASS 票) → 本 Rev4 (R4 三 Major + 全部可落 minor 已吸收)。max_rounds=4 耗尽, 未达全票 PASS — 按 audit-engine 降级策略交 owner 三路径裁决。
- **Rule #6 substitute 适格性**: agent-router 属结构化决策 Skill — AC 断言对象是决策规则的结构化输出字段; 推断层不确定性经显式传参在裁决类 AC 中完全隔离。substitute 判据 = 可复跑 (双跑一致, 不一致即 fail 回炉) + 可机械判定 (字段级断言)。AB benchmark 对"规则是否被遵守"无增量信息, 不跑。
