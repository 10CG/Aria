# Aria 2.0 M7 Sub-Spec #1 — Agent Lifecycle Management (下行 pull 半环 MVP)

> **Level**: 3 (Full — net-new collection-repo skeleton + net-new materialization orchestrator Skill + lockfile schema + update-detector, spanning ①推荐→②加载→④更新-基础版 across L1/L2/L3; reuses 4 existing Skills as black-box dependencies but introduces a new orchestration layer + new artifact contract `.aria/agents-lock.yaml`)
> **Status**: ✅ **Approved** (owner sign-off 2026-06-18; Phase A.2 post_spec R1→R2 **CONVERGED** [R2 unanimous PASS 3/3]; **Phase A.3 agent 分配 LOCKED 2026-06-19** (无新 agent, 现有 roster 覆盖; 见 tasks.md §Phase A.3)。**Phase B 受 D3 时机门 — M6 release-closeout ship 后方可开**)
> **Change ID**: `aria-2.0-m7-agent-lifecycle`
> **Parent US**: [US-028](../../../docs/requirements/user-stories/US-028.md) (Aria 2.0 M7 — aria-fleet 落地; 立 2026-06-18, 规范先行前置已补; **注**: US-027 = Cost-routing 语义已占用, aria-fleet 用独立 US-028, memo 曾误并 #128↔US-027 已更正)
> **Parent PRD**: [prd-aria-v2.md](../../../docs/requirements/prd-aria-v2.md) §里程碑概览 M7 (post-v2.0.0) + §User Stories US-028 (M7 milestone stub 立 2026-06-18)
> **Sibling Spec (M7 并行子能力)**: `aria-2.0-m7-fleet-aggregation` (跨项目只读聚合 MVP, 来自 2026-06-18 memo; 与本 Spec 共享 aria-fleet L1/L2/L3 框架但 disjoint 交付物 — 本 Spec 管 agent 生命周期, sibling 管 state-snapshot 聚合)
> **Brainstorm Source**: [.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md](../../../.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md) (§1 四决策收敛 + §2 六阶段飞轮 + §3 四块硬骨头 + §7 三层映射/M7 第一刀; owner 逐段确认通过 2026-06-16, 无正式 DEC) — 上游约束 [.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md](../../../.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md) (D1-D6 Approved, 本 Spec 不重议)
> **Tracker**: Forgejo Aria #128 (M7 aria-fleet); Claude Code session-start 加载机制依据 #145 (动态 agent 当前 session 不可 spawn, 需重启)
> **Effort baseline**: ~24h impl baseline (TG-A 集合库骨架 ~6h + TG-B 推荐/加载 orchestrator + lockfile ~10h + TG-C 更新-基础版 detector ~4h + T-docs ~2h + ~2h buffer). 单一 SoT, frontmatter + §Effort baseline + tasks.md 三处一致引用.
> **AD allocation reservation**: **AD-M7-1**, **AD-M7-2**, **AD-M7-3** 预留给本 Spec。AD-M7-1 = 集合库目录契约 (git collection repo layout + manifest index schema)。AD-M7-2 = `.aria/agents-lock.yaml` lockfile schema + 物化层去 Aria-metadata 契约。AD-M7-3 = 更新-基础版 lockfile-vs-registry 版本比对裁决 (三方不冲改写仅"提示"不"自动合并")。Sibling Spec `fleet-aggregation` 持 AD-M7-4..AD-M7-6。
> **abi_compat hard constraints**: (a) 不修改既有 4 Skill 的 input/output 契约 — 全部当 black-box 消费 (`project-analyzer`→`.aria/project-profile.yaml`; `agent-gap-analyzer`→`.aria/coverage-report.yaml`; `agent-creator`→`.aria/agents/<name>.md`; `agent-router`→runtime 扫描 `.aria/agents/`); (b) `.aria/agents-lock.yaml` 为 net-new artifact, 不与任何既有 schema 冲突; (c) 物化产物 `.claude/agents/aria-<name>.md` 为纯 Claude Code STCO frontmatter, 不引入 custom field (向后兼容 CC 原生加载)。
> **Audit trajectory**: **R1→R2 CONVERGED (2026-06-18)**。R1 (agent-team 3 lens) = PASS_WITH_WARNINGS (0 Critical / 8 Important / 多 Minor); Important 全部主 loop 落地: frontmatter 悬空引用 (旧目标 US-027/§M7) → **改锚定真实 US-028 + PRD M7 milestone** / 2 处虚构 `[[memory]]` token 删除 / agent-router 软注入 over-claim 修正为 pattern (真实 v1.1.0 仅 routing-context, 无现成 spawn 机制) / `## What Changes`+`## Impact` 补全。**R2 (agent-team 3 lens) = unanimous PASS** (3/3, r1_landed=true; 仅 2 Minor: #128 标题已主 loop 用 forgejo 核实 = "M7: aria-fleet implementation tracker" 确非 Cost-routing / audit-traj 措辞已澄清锚点为 US-028)。规范先行前置已补 (PRD M7 stub + US-028 立 2026-06-18)。**待**: owner Approve → Phase A.3; Phase B 受 D3 时机门 (M6 ship 后)。

---

## Why

aria-fleet 的 L1/L2 愿景 (D1-D6 Approved 2026-05-27) 包含一个**跨项目 agent 复用 + 回流**子能力: 让"重复需求的 agent 不重复设计", 并在 Aria 生态中持续汇总、自我迭代。2026-06-16 brainstorm 把它收敛成**六阶段双向飞轮** (①推荐 ②加载 ③使用 ④更新 ⑤吸收 ⑥汇总)。

但飞轮的**上行半环** (⑤吸收 / ⑥汇总) 在依赖关系上被锁死: 吸收/AB 裁决/去重汇总都需要"已部署的 agent + 累积的真实使用数据"才能成立 — 没有项目先 pull、先用, 就没有任何观测数据可供回流决策。memo §7 明确: **上行必须先有下行**, 顺序由依赖锁定, 不可随意切。

因此 M7 第一刀 = **下行 pull 半环 ONLY** (①推荐 → ②加载 → ④更新-基础版)。这一刀解决三个具体问题:

1. **无集合库, agent 设计重复**: 当前每个 Aria 项目要么手写 `.aria/agents/`, 要么靠 `agent-creator` 现场生成, 跨项目相同需求 (如"backend API 审查") 各造一遍。没有一个 git 集合库承载精选 agent + 能力标签 + 版本, "复用"无从谈起。

2. **推荐→加载之间有断层**: 既有 4 Skill 已经能 (a) `project-analyzer` 扫出项目特征 → `.aria/project-profile.yaml`; (b) `agent-gap-analyzer` 比对能力标签 → `.aria/coverage-report.yaml` (含 `gaps[].suggested_agent`); (c) `agent-creator` 物化进 `.aria/agents/`。但**没有任何一环把库里的精选 agent 拉下来物化进 Claude Code 原生加载目录 `.claude/agents/`** —— agent-creator 显式声明"不自动物化到 `.claude/agents/`, 只输出到 `.aria/agents/` (project source layer)"。这个物化断层是 MVP 要补的核心新件。

3. **库升级后项目无感知**: 库里的 agent 改进版本后, 用旧版的项目无任何提示。MVP 提供**更新-基础版**: lockfile 记录的版本 < 库版本 → 提示重物化 (三方不冲改写的真正合并是 fast-follow, 基础版仅"提示")。

**Gate role / 时机**: 本 Spec 是 M7 的第一刀, **严格在 M6 ship 之后**起 (D3 时机锁); 与 sibling `fleet-aggregation` 可并行 Phase A/B (disjoint 交付物)。

**为什么是 git 集合库, 不是 marketplace** (memo §1 决策 #2, §3 硬骨头 #4): Claude Code marketplace 的选择性最细只到**整个插件** (`enabledPlugins` 整包开关), 给不了 **agent 粒度**的按项目配给 (#145 + claude-code-guide 核实)。要 agent 粒度智能配给, 唯一办法是**文件物化进 `.claude/agents/`**。故核心机制 = "集合库 = git 仓库, Aria 直接读 + 物化", marketplace 既非核心机制也不做试水 (memo §1 #2/#3)。

---

## What Changes

### In scope (~24h impl) — 下行 pull 半环: ①推荐 → ②加载 → ④更新-基础版

本 Spec 交付物分三个 Task Group:
- **TG-A**: 集合库骨架 (git collection repo layout + 精选 agent + 能力标签 + 版本 + index)
- **TG-B**: 推荐 + 加载 orchestrator (接 `project-analyzer` + `agent-gap-analyzer` 读库 → 物化进 `.claude/agents/aria-<name>.md` + 写 `.aria/agents-lock.yaml` + "重启生效"提示)
- **TG-C**: 更新-基础版 (lockfile 版本 < 库版本 → 提示重物化)

---

#### TG-A. 集合库骨架 (collection repo skeleton) (~6h)

**机制锁定** (memo §3 #4 + AD-M7-1): 集合库 = **git 仓库**, 非 marketplace、非自建 registry service。Aria 直接 `git clone`/`pull` + 读文件。**对内通用定位** (memo §1 #1): 代码写成 any-org 通用 (零 10CG hardcode), 但当前只 10CG 一个 workspace 实例用。

**三层映射** (memo §7 + D2):
- **L1 通用层**: 语言/框架无关的精选 agent (任何 org 可用) + 集合库目录契约 + index schema。零 10CG hardcode。
- **L2 workspace (10CG 私有)**: 10CG 私有 agent (如 shell-safety / ssh-egress / homelab-topology) 放 `10CG/aria-workspace` 私有 repo (D4), **不**进 L1 通用库。

**A.1 — 集合库目录契约** (AD-M7-1):

```
<collection-repo>/                      # git 仓库 (L1 通用; L2 workspace 私有库结构镜像)
├── registry-index.yaml                 # 机读索引: 全部 agent + 能力标签 + 版本 (推荐环节读这一份)
├── agents/
│   ├── backend-architect/
│   │   ├── agent.md                    # STCO+capabilities frontmatter (= agent-creator 输出格式)
│   │   └── VERSION                     # 单 agent 语义版本 (e.g. 1.0.0)
│   ├── code-reviewer/
│   │   ├── agent.md
│   │   └── VERSION
│   └── ...
└── README.md                           # 库使用说明 + 贡献约定 (上行 ⑤⑥ 是 M7+ 占位)
```

**A.2 — `registry-index.yaml` schema** (推荐环节的读入源, 镜像 `agent-gap-analyzer` 已消费的 `capabilities-taxonomy.yaml` 标签词表):

```yaml
schema_version: "1"
registry_name: "<repo-name>"            # 不 hardcode org
agents:
  - name: backend-architect
    version: "1.0.0"
    capabilities: [api-design, database-schema, microservice-architecture, performance-optimization, service-boundary]
    scope: "RESTful API design, microservice boundaries, database schemas"
    path: "agents/backend-architect/agent.md"
  - name: code-reviewer
    version: "1.0.0"
    capabilities: [code-review, spec-compliance, security-audit, pre-merge-verification]
    path: "agents/code-reviewer/agent.md"
```

**约束**: `capabilities[]` 的标签**必须**来自 `aria/references/capabilities-taxonomy.yaml` 既有词表 (real tags: `api-design` / `code-review` / `security-audit` / `system-architecture` / `test-strategy` / `documentation-audit` / ... — 见 §Constraints 词表锚定)。这保证推荐环节 (TG-B) 能用 `agent-gap-analyzer` 的**确定性标签匹配** (match_rate = matched_tags / required_tags) 直接比对, 零新匹配逻辑。

**A.3 — L1 精选 agent 种子集** (MVP 用既有 `aria/agents/*.md` 中**语言/框架无关**的子集作初始库内容): `backend-architect` / `code-reviewer` / `qa-engineer` / `api-documenter` / `tech-lead` (5 个已验证 STCO frontmatter agent, 真实存在于 `aria/agents/`)。这些是 seed, 不是穷举; 库后续靠上行回流增长 (M7+)。

**A.4 — 库定位 / 拉取契约** (L2 注入): 集合库 repo 地址 / 分支 **不** hardcode 进 L1 代码, 经 `.aria/config.json` 的 `agent_lifecycle.registry.{repo, branch, local_cache_path}` 字段注入 (D5 L2 workspace config 模式)。L1 代码只认抽象的"本地 cache 路径", 由 L2 config 决定指向哪个 repo。

**AC-A1** — 集合库骨架可被机读消费:
```bash
# registry-index.yaml YAML-parse 成功 + 每个 agents[].path 文件存在 + 每个 capabilities[] 标签 ∈ capabilities-taxonomy.yaml
python3 -c "import yaml,sys; idx=yaml.safe_load(open('<cache>/registry-index.yaml')); assert idx['schema_version']=='1'; assert all((__import__('pathlib').Path('<cache>')/a['path']).is_file() for a in idx['agents'])"
```
**AC-A2** — L1 零 10CG hardcode: `grep -rE 'forgejo\.10cg|10cg\.pub|simonfishgit|aria-workspace' <L1-code>` 返回空 (org-specific 值全部经 L2 config)。

---

#### TG-B. 推荐 + 加载 orchestrator (~10h) — ①推荐 + ②加载

**新件定位**: 一个**新 Skill** `agent-lifecycle` (或 Phase B step), 编排既有 4 Skill 的输出, 补"读库 → 物化 → 写 lockfile"断层。**不重实现** 4 Skill 的逻辑 (memo §2 复用约定; CAVEAT #1)。

**B.1 — ①推荐 (Recommend)**: 串联既有 Skill 链 (memo §2 表)

| 步 | 复用 Skill | 真实 input | 真实 output |
|----|-----------|-----------|-----------|
| 1 | `project-analyzer` | project root 目录 (扫 package.json/go.mod/pyproject.toml/...) | `.aria/project-profile.yaml` (schema_version "1": tech_stack / patterns / work_modes / detected_from) — **确定性文件扫描, 无 LLM 推断** |
| 2 | `agent-gap-analyzer` | `.aria/project-profile.yaml` + agent capabilities 标签 + `capabilities-taxonomy.yaml` | `.aria/coverage-report.yaml` (schema_version "1": covered[] / gaps[] / summary) — **确定性标签匹配, covered if match_rate ≥0.5** |
| 3 | (新) 推荐合成 | `.aria/coverage-report.yaml` + `registry-index.yaml` | 推荐清单: 对 `gaps[].required_capabilities` 在 `registry-index.yaml` 找标签覆盖最高的库 agent → "建议从库装这几个" |

**关键 grounding**: 推荐**不**发明新匹配算法 —— `agent-gap-analyzer` 已经把项目需求降维成 `gaps[].required_capabilities` (能力标签数组), TG-B 第 3 步只是把这些标签拿去 `registry-index.yaml` 里查"哪个库 agent 的 `capabilities[]` 覆盖率最高", 复用同一套确定性标签匹配语义。**routing prior-art 弱** (memo §8 #1: RouteLLM/MoA 未存活), 故推荐环节明确是**启发式 (标签覆盖率排序)**, MVP 可接受 (memo §6-C); 不声称是已验证的智能路由。

**B.2 — ②加载 (Load) / 物化 orchestrator** (AD-M7-2 + CAVEAT #1):

owner 确认推荐清单后, 物化层执行 (这是 agent-creator **不做**的那一段, 须新写):

1. **拉源**: 从库 (本地 cache) 复制选中 agent 的 `agent.md` (STCO+capabilities frontmatter)。
2. **写 source 层**: 落 `.aria/agents/<name>.md` (= `agent-creator` 输出位置, 保留 capabilities 标签供 `agent-router` runtime 扫描 + `agent-gap-analyzer` 后续 gap 分析)。**复用 agent-creator 物化逻辑** (memo §2 表"+ agent-creator 物化逻辑") 写这一层。
3. **物化 native 层**: 复制并**剥离 Aria-specific metadata** → `.claude/agents/aria-<name>.md` (纯 STCO frontmatter, NO `capabilities` / NO `aria_managed` / NO custom field)。
   - **剥离理由** (CAVEAT #4): Claude Code 官方文档对 custom frontmatter field 行为标注"uncertain whether safely ignored" → MVP 最安全做法 = native 层零 custom field。capabilities 标签只活在 `.aria/agents/` source 层。
   - **`aria-` 前缀** (CAVEAT #9): 命名空间隔离 + 便于批量清理 (`rm .claude/agents/aria-*.md`)。`aria-<name>` 仍是 bare-name namespace (project agent 用 bare name, plugin agent 用 `plugin:name`), 不与 CC scoping 冲突。
4. **写 lockfile**: 落/更新 `.aria/agents-lock.yaml` (账本)。
5. **"重启生效"提示** (CAVEAT #3, HARD REQUIREMENT): 物化进 `.claude/agents/` 的 agent **当前 session 不被原生加载** —— Claude Code subagent 在 session-start 加载, 直接写盘 → 当前 session 不识别, 需**重启 session** 才能原生 `subagent_type` spawn (#145 实证)。orchestrator 收尾**必须**打印此提示。同 session 即用的兜底 = **软注入 pattern** (memory `feedback_dynamic_agent_session_start_vs_soft_injection` / #145: general-purpose + 定义注入)。⚠️ **grounding 修正**: 这是一个**实践 pattern**, **非** agent-router 现成暴露的能力 —— `agent-router` 真实版本 = v1.1.0, 只做"将项目级 Agent 注入路由上下文"(routing-context, 仅供选择), **不**含"把 agent 定义包进 general-purpose body spawn"的机制。故同 session 即用须 owner 显式走 `/agents` reload 或重启; 软注入 pattern 由调用方按需实现。本 Spec **不**依赖任何未实现的 routing 能力, 也**不**改 agent-router。

**B.3 — `.aria/agents-lock.yaml` schema** (AD-M7-2, memo §3 #1 账本):

```yaml
schema_version: "1"
project: "<project-name>"
generated_at: "2026-06-18T..."          # UTC ISO
agents:
  - name: backend-architect
    source: "registry"                   # registry | local (local = 项目本地新建, 非库 pull)
    registry_version: "1.0.0"            # 物化时库版本; source==local 时省略
    local_modifications: false           # true = 物化后 .aria/agents/ 被本地改写 (供 ④ 更新判断)
    materialized_at: "2026-06-18T..."
manifest_hash: "<checksum>"             # 全 lockfile 内容 checksum, 供漂移检测
```

**`local_modifications` 字段必要性** (CAVEAT #6): ④ 更新逻辑需要区分"未改 (可直接重物化)" vs "已本地改写 (不可盲覆盖)"。MVP 基础版只**读**这个 flag 做提示分流; 真正的三方合并是 fast-follow。

**原子写** (CAVEAT #8): lockfile 写用 `.aria/agents-lock.yaml.tmp` → `os.replace()` 原子 rename, 防多终端并发写 race (与既有 concurrent-session-write-safety convention 一致; advisory-over-hardlock)。

**AC-B1** — 推荐链贯通: 给定一个有 `.aria/project-profile.yaml` + `.aria/coverage-report.yaml` 的项目 fixture + 一个 `registry-index.yaml`, orchestrator 输出推荐清单, 清单中每个 agent 的 capabilities 与某个 `gaps[].required_capabilities` 标签覆盖率 ≥ 0.5 (复用 gap-analyzer 阈值)。
**AC-B2** — 物化产物双层正确:
```bash
# source 层保留 capabilities; native 层剥离
grep -q 'capabilities:' .aria/agents/backend-architect.md          # source 层有
! grep -q 'capabilities:' .claude/agents/aria-backend-architect.md  # native 层无 (剥离)
! grep -qE 'aria_managed|gap_source|audit_points' .claude/agents/aria-backend-architect.md  # 无任何 Aria metadata
```
**AC-B3** — lockfile 写入 + 原子: 物化后 `.aria/agents-lock.yaml` YAML-parse 成功, `schema_version=="1"`, 每个 `agents[].name` 对应 `.claude/agents/aria-<name>.md` 存在; 写过程用 `.tmp`+rename (无半写文件残留)。
**AC-B4** — "重启生效"提示存在: orchestrator stdout 含明确的"agents materialized to .claude/agents/; restart Claude Code session for native subagent spawn (or use /agents reload / soft-injection pattern for same-session)"字样 (CAVEAT #3; 不声称 agent-router 现成支持软注入)。

---

#### TG-C. 更新-基础版 (update detector) (~4h) — ④更新 (基础版)

**MVP 范围** (memo §7 + AD-M7-3): **仅版本检测 + 提示重物化**。三方不冲改写 (库旧版 base / 库新版 / 项目当前) 的真正合并是 **fast-follow** (CAVEAT #10; memo §3 #2 标"阶段④最难")。

**C.1 — 检测逻辑**: 对 `.aria/agents-lock.yaml` 每个 `source==registry` 的 agent:
1. 读 lockfile `registry_version`。
2. 读库 `registry-index.yaml` 当前 `version`。
3. `lockfile_version < registry_version` (semver 比较) → 该 agent stale。

**C.2 — 三档处置** (基础版仅提示, 不自动改写):

| 状态 | 判据 | 动作 |
|------|------|------|
| up-to-date | lockfile_version == registry_version | 无动作 |
| stale, 未本地改写 | version < registry **且** `local_modifications==false` | 提示"可重物化更新" (owner 确认后走 TG-B 物化, 覆盖 native + source) |
| stale, 已本地改写 | version < registry **且** `local_modifications==true` | 提示"库已升级但本项目已本地改写; **不自动覆盖**, 请人工合并 (三方合并 = fast-follow)" |

**关键约束** (memo §3 #2): 任何情况下 MVP **绝不自动冲掉** `local_modifications==true` 的 agent —— 只 surface "已分叉, 请人工合并"。这是飞轮 ④ 的核心安全不变式, fast-follow 的三方合并在此基础上增量。

**AC-C1** — stale 检测正确: lockfile version `1.0.0` + registry index version `1.1.0` → detector 报该 agent stale。
**AC-C2** — 本地改写保护: `local_modifications==true` 的 stale agent → 输出"不自动覆盖 / 请人工合并", **不**触发任何文件写 (detector 是只读检测, 不动 native/source 层)。
**AC-C3** — up-to-date 静默: version 相等 → 无 stale 提示。

---

### Out of scope (显式 DEFER 到 M7+ — memo §7 推迟项, 不在本 Spec spec 范围内)

| ID | Description | Drop reason |
|----|-------------|-------------|
| OOS-1 | **⑤吸收 (Absorb / push-back)**: 项目新建/改进 agent 推回库当候选 | 依赖"已部署 agent + 累积真实使用数据" (memo §7 上行依赖锁); M7+ |
| OOS-2 | **⑥汇总/优化 (Curate)**: 候选审核 + 去重 (能力标签 80% 重叠合并) + 版本提升 | 同上; curation 闸 ownership 未定 (memo §8 #6: Aria 辅助 / audit-engine / 人工?) |
| OOS-3 | **AB-judge harness** (pairwise LLM-judge / PoLL / position-swap / 五维 forced-choice) | memo §4/§5/§6 deep-research 部分; 仅服务 ⑤⑥ 裁决; M7+。**§6 四处修正是 forward-context, 不适用本 MVP** (CAVEAT) |
| OOS-4 | **影子/配对评测** (同任务两 agent 并发跑 + 配对打分) | memo §5; prior-art 最弱 (§6-C); 须真实数据后自研; M7+ |
| OOS-5 | **生态池化 usage-telemetry** (被 N 项目采用 / M 次调用 / 成功率 → 采用度/声誉) | memo §4 活体库; 跨会话遥测须先验证真产出 (R-fix-1 教训); schema 未定 (CAVEAT #10); M7+ |
| OOS-6 | **curation 质量闸**执行 (谁审 / 自动化细节) | memo §8 #6 ownership 开放; M7+ |
| OOS-7 | **零游离 agent 不变式强制** (每个项目 agent 必须 from 库或已吸收) | memo §4 收敛不变式; 依赖上行铺好; M7+ |
| OOS-8 | **三方 override-safe 合并** (库旧版/库新版/项目当前 真正三方 merge) | 本 MVP ④ 仅"提示已分叉"; 真合并 = fast-follow (memo §3 #2 标最难; CAVEAT #10) |
| OOS-9 | **marketplace 集成** (registry ↔ marketplace 耦合) | memo §1 #2/#3: marketplace 不参与核心闭环, 未来若需做粗粒度分发 backbone, 非 M7 |
| OOS-10 | **粒度版本 / 覆盖率 / push-back 机制细节** | memo §1 #4: 等下行铺好 + 真实数据后设计 (用数据说话哲学) |
| OOS-11 | **agent-router / agent-creator / project-analyzer / gap-analyzer 既有逻辑修改** | 本 Spec 全部当 black-box 消费; 不改其 input/output 契约 (abi_compat (a)) |

**Critical forward-context caveat**: memo §6 的 deep-research 四处修正 (one-shot gate→pairwise judge / PoLL 三件套去偏 / 影子-池化标 Aria 原创 / 配对必须并发) **只适用于 ⑤⑥+ 的 AB/观测部分**, 本 MVP 下行半环**不含**任何 AB / judge / telemetry, 故这四处修正是**前瞻语境 (forward context), 非 MVP scope** —— Spec 在此显式标注, 防止后续误把 AB harness 卷入下行半环。

---

## Impact

**纯 additive** (Aria 原则 #4; 不改既有 Skill / schema / 4 复用 Skill 契约)。受影响清单:

| 类别 | Affected | 性质 |
|------|----------|------|
| 新 git repo | 集合库 (collection repo, L1 通用 + L2 10CG 私有镜像) | net-new (repo 地址经 L2 config 注入) |
| 新 Skill | `aria/skills/agent-lifecycle/` (推荐+加载+更新 orchestrator) | net-new |
| 新 artifact | `.aria/agents-lock.yaml` (lockfile 账本) | net-new schema (AD-M7-2) |
| 新 config section | `.aria/config.json` `agent_lifecycle.*` (registry repo/branch/cache_path + 阈值) | additive (A-5 验证不冲突) |
| 新物化目标 | `.claude/agents/aria-<name>.md` (native 层, 纯 STCO 剥 metadata) | net-new (CC 共享 namespace, `aria-` 前缀隔离) |
| 复用 (不改) | `project-analyzer` / `agent-gap-analyzer` / `agent-creator` / `agent-router` (black-box) | 零改动 (abi_compat (a)) |
| 复用 (不改) | `aria/references/capabilities-taxonomy.yaml` (标签词表锚) | 只读消费 |
| 文档 | `aria/skills/agent-lifecycle/SKILL.md` + 集合库 README | net-new |
| **不涉及** | standards submodule / 既有 schema / 既有 hooks | 无改动 |

**迁移路径**: 无 (net-new 能力, 无既有用户受影响)。**回滚**: 删新 Skill + 新 config section + `rm .claude/agents/aria-*.md` + `rm .aria/agents-lock.yaml` 即完全回退。

---

## Constraints

### 对内通用定位 (L1 零 10CG hardcode) — D1-D6 Approved hard constraint
L1 代码 (集合库读取 / 推荐合成 / 物化 orchestrator / 更新 detector) **禁止** hardcode: `forgejo.10cg.pub` / `Aether` / `simonfishgit` / `10CG/aria-workspace` repo 地址 / Feishu webhook。所有 org-specific 值经 L2 `.aria/config.json` `agent_lifecycle.*` 注入 (D5 模式)。AC-A2 用 `grep -rE` 机械验证。

### 集合库 = git 仓库, NOT marketplace (memo §3 #4)
核心机制锁定为"git collection repo + 文件物化"。marketplace 在本 Spec 完全不参与 (OOS-9)。理由: marketplace 选择性最细只到整插件, 给不了 agent 粒度配给 (#145 核实)。

### session-start reload caveat (HARD REQUIREMENT, CAVEAT #3, #145)
物化进 `.claude/agents/` 的 agent 当前 session **不被原生加载**, 需重启 session。orchestrator **必须**输出此提示 (AC-B4)。`/agents` 交互 UI 是唯一同 session 即时生效途径; 软注入 pattern (memory `feedback_dynamic_agent_session_start_vs_soft_injection` / #145, **非** agent-router 现成能力) 是同 session 兜底, 本 Spec 不改 agent-router。

### 既有 4 Skill 当 black-box, 输出契约锚定 (abi_compat (a))
本 Spec 引用的所有 Skill 输出**必须**是它们真实产出的契约, 不得发明 (per `[[feedback_recon_real_code_before_implementing_spec_test_suite]]`):
- `project-analyzer` → `.aria/project-profile.yaml` (schema_version "1"; tech_stack/patterns/work_modes/detected_from; 确定性文件扫描, 无 LLM)
- `agent-gap-analyzer` → `.aria/coverage-report.yaml` (schema_version "1"; covered[]/gaps[]/summary; match_rate = matched_tags/required_tags, covered ≥0.5)
- `agent-creator` → `.aria/agents/<name>.md` (STCO+capabilities frontmatter; **不自动物化到 `.claude/agents/`**)
- `agent-router` → runtime 扫描 `.aria/agents/` (真实版本 **v1.1.0**; cache 到 `.aria/cache/project-agents.json`; 仅 routing-context 注入, **无**现成"定义注入 spawn"机制)

### capabilities-taxonomy.yaml 词表锚定
`registry-index.yaml` 与库 agent 的 `capabilities[]` 标签**必须**来自 `/home/dev/Aria/aria/references/capabilities-taxonomy.yaml` 既有词表 (real tags: Architecture/Design 组 `system-architecture`/`api-design`/`database-schema`/`microservice-architecture`/`performance-optimization`/`service-boundary`/`architecture-decision`; Code Quality 组 `code-review`/`spec-compliance`/`security-audit`/`pre-merge-verification`; QA 组 `test-strategy`/`defect-analysis`/`release-readiness`; Docs 组 `documentation-audit`/`doc-codebase-alignment`/`ai-ddd-methodology`; 等)。这保证推荐环节复用 gap-analyzer 确定性匹配, 不引入新词表。

### capabilities 不可 agent 粒度选择性禁用 (documented limitation, CAVEAT #5)
项目内所有加载的 agent 都看到全部 capabilities, 不能选择性禁用; marketplace 同样无 agent 级激活 (整插件 only)。本 Spec 把 `.claude/agents/` 物化作为达成"项目级 agent 子集"的**唯一**途径, 并记录此 limitation。

### 向后兼容 (Aria 原则 #4)
纯 additive: 新集合库 repo / 新 Skill `agent-lifecycle` / 新 artifact `.aria/agents-lock.yaml` / 新 config section `agent_lifecycle.*`。不改既有 Skill, 不改既有 schema。

### Rule #6 benchmark substitute (deterministic Skill)
TG-B/TG-C 的物化 orchestrator + update detector 是 **deterministic** (文件扫描 / 标签匹配 / semver 比较 / 文件复制), 非 capability Skill。按 `[[feedback_deterministic_structural_skill_rule6_substitute]]`, Rule #6 substitute = structural fixture + unit tests + dogfood (见 tasks.md TG-B/TG-C 测试任务), 非 `/skill-creator` AB。

---

## Assumptions

Phase B kick 前 owner 须逐条 recheck assumptions (Spec assumption 是 snapshot, Phase B 前须复验当前真实性):

| # | Assumption | 验证命令 |
|---|------------|---------|
| A-1 | 4 既有 Skill 当前输出契约未漂移 (project-profile/coverage-report/agents/*.md/router 扫描) | `ls aria/skills/{project-analyzer,agent-gap-analyzer,agent-creator,agent-router}/SKILL.md` 全在 + grep 各自 output 路径声明 |
| A-2 | `capabilities-taxonomy.yaml` 词表可读 + 含本 Spec 引用的种子标签 | `python3 -c "import yaml; t=yaml.safe_load(open('aria/references/capabilities-taxonomy.yaml')); assert 'api-design' in str(t)"` |
| A-3 | `.aria/agents/` 不预存在 (agent-creator 首写时创建; 物化层亦须 mkdir-if-absent) | `ls -d .aria/agents/ 2>&1` 预期 not-exist (CAVEAT #2) |
| A-4 | 种子 agent (`backend-architect`/`code-reviewer`/`qa-engineer`/`api-documenter`/`tech-lead`) STCO frontmatter 可解析 | `for a in ...; do grep -q '^capabilities:' aria/agents/$a.md; done` |
| A-5 | `.aria/config.json` 可扩展 `agent_lifecycle.*` section (不与既有 key 冲突) | `python3 -c "import json; c=json.load(open('.aria/config.json')); assert 'agent_lifecycle' not in c"` |

---

## How

### 数据流 (下行 pull 半环)

```
            集合库 (git collection repo, L1 通用 / L2 10CG 私有)
            registry-index.yaml + agents/<name>/agent.md + VERSION
                          │  (L2 config: agent_lifecycle.registry.repo)
                          ▼  git clone/pull → 本地 cache
   ┌──────────────────────────────────────────────────────────────┐
   │  ①推荐 (TG-B.1)                                                │
   │    project-analyzer  → .aria/project-profile.yaml             │  (复用)
   │    agent-gap-analyzer → .aria/coverage-report.yaml (gaps[])    │  (复用)
   │    (新) 推荐合成: gaps[].required_capabilities × index 标签覆盖率│
   └───────────────────────────┬──────────────────────────────────┘
                               │ owner 确认推荐清单
                               ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  ②加载 / 物化 orchestrator (TG-B.2, AD-M7-2)                   │
   │   1. 拉源 agent.md (STCO+capabilities)                         │
   │   2. → .aria/agents/<name>.md   (source 层, 留 capabilities)   │  (复用 agent-creator 物化)
   │   3. → .claude/agents/aria-<name>.md (native 层, 剥 metadata)  │  (新)
   │   4. → .aria/agents-lock.yaml   (账本, 原子写)                 │  (新, AD-M7-2)
   │   5. 打印 "重启生效" 提示 (#145 caveat)                        │
   └───────────────────────────┬──────────────────────────────────┘
                               │ (库升级后)
                               ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  ④更新-基础版 detector (TG-C, AD-M7-3)                         │
   │   lockfile.registry_version < index.version → stale           │
   │   ├ 未本地改写 → 提示可重物化                                  │
   │   └ 已本地改写 → 提示"已分叉, 人工合并" (绝不自动覆盖)         │
   └──────────────────────────────────────────────────────────────┘
```

### Key design decisions (AD-M7-1..AD-M7-3)

| ID | Topic | Decision |
|----|-------|----------|
| AD-M7-1 | 集合库目录契约 | git collection repo (NOT marketplace/service); `registry-index.yaml` (机读索引, schema_version "1") + `agents/<name>/{agent.md, VERSION}`; capabilities 标签锚定既有 `capabilities-taxonomy.yaml`; repo 地址经 L2 config 注入, L1 零 hardcode |
| AD-M7-2 | lockfile schema + 物化去 metadata 契约 | `.aria/agents-lock.yaml` (schema_version "1"; agents[]{name,source,registry_version,local_modifications,materialized_at}; manifest_hash); 原子写 (.tmp+rename); native 层 `.claude/agents/aria-<name>.md` 纯 STCO 剥 capabilities/aria_managed (CC custom-field 行为不确定 → 安全起见零 custom field); source 层 `.aria/agents/` 留全标签供 router/gap-analyzer |
| AD-M7-3 | 更新-基础版裁决 | semver 比较 lockfile vs registry; 三档 (up-to-date / stale-clean→提示重物化 / stale-dirty→提示人工合并 **绝不自动覆盖**); 三方真合并 = fast-follow (OOS-8); detector 只读不写文件 |

---

## Acceptance criteria

全部 binary-falsifiable (每条 AC 给出可机械判真伪的证据命令/断言, 不留主观判断)。汇总:
- **AC-A1/A2**: 集合库骨架机读可消费 + L1 零 10CG hardcode (见 TG-A)
- **AC-B1/B2/B3/B4**: 推荐链贯通 + 物化双层正确 (native 剥 metadata) + lockfile 原子写 + 重启提示存在 (见 TG-B)
- **AC-C1/C2/C3**: stale 检测 + 本地改写保护 (不自动覆盖) + up-to-date 静默 (见 TG-C)
- **AC-D1** — dogfood: 在一个真实测试项目 (或 Aria 自身 sandbox) 跑完整 ①→②→④ 链, 物化出 ≥1 个 `aria-<name>.md` + lockfile 落地 + 重启提示打印 + 模拟库升版后 detector 正确报 stale。

---

## Risks

| Risk | Mitigation |
|------|-----------|
| 既有 Skill 输出契约已漂移, 推荐链断 | A-1 Phase B kick 验证 + 全部当 black-box (per `[[feedback_recon_real_code_before_implementing_spec_test_suite]]`) |
| native 层 custom field 致 CC 加载异常 | AD-M7-2 零 custom field; Phase B dogfood 实测 CC 加载行为 (CAVEAT #4) |
| 多终端并发物化致 lockfile race | 原子 .tmp+rename (CAVEAT #8; concurrent-session-write-safety convention) |
| "重启生效" 提示被忽略 → owner 困惑 agent 没出现 | AC-B4 强制提示 + 文档明确 + 软注入兜底说明 (#145) |
| 推荐启发式不准 (routing prior-art 弱) | 明确标 MVP 启发式, owner 确认 gate; 自我验证留 M7 (memo §8 #1) |

## Memory entries (Phase D 候选)
- `feedback_agent_lifecycle_pull_half_loop_reuses_4skills` — 下行 pull 半环靠编排既有 4 Skill (不重实现), 新件只补"读库→物化→lockfile"断层
- `feedback_native_agent_layer_strips_aria_metadata` — `.claude/agents/aria-*.md` 物化必剥 capabilities/aria_managed (CC custom-field 行为不确定); 标签留 `.aria/agents/` source 层
