# 设计输入: Agent Registry (for aria-fleet M7)

> **类型**: 战略 epic 设计输入 (待 M7 brainstorm 消费)
> **日期**: 2026-06-13
> **来源**: Forgejo Aria #145 triage → brainstorm 升级 (owner 主动提出"升级设计")
> **关联**: aria-fleet M7 (#128 tracker) + `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` (L1/L2/L3 三层)
> **状态**: 未立项。本 notes 仅封存愿景 + 调研事实 + 关键洞察,**不是** Approved 设计。

---

## 0. 一句话

把 `.aria/agents/` 升级为一个**中心化精选 Agent Registry**(curated agent 库),第三方项目从它 pull agent 到本地 `.claude/agents/`(原生可用),支持 **version / pull / push-back**,像 agent 层的包管理器。本质是 aria-fleet **L1(通用)/ L2(workspace)** 的"跨项目 agent 复用/分发"子能力。

## 1. 愿景 (owner 原话转述)

- `.aria/agents/` = 一个**子仓库**,专门汇总大量好的 agent(registry / curated 库)。
- `.claude/agents/` = 第三方项目的**物理原生目录**,里面的项目级 agent **来自 aria 的 agent 仓库**(pull 下来的)。
- registry 提供:**拉取 (pull) / 推送 (push) / 版本 (version)** 管理。

## 2. 关键调研事实 (claude-code-guide ×2, 均附官方 URL)

### 2.1 Claude Code 项目 agent 加载机制 (sub-agents.md)

| 维度 | 事实 |
|------|------|
| 加载目录 | 项目级 `.claude/agents/`(支持递归子目录,子目录**不影响** name,裸 name 调用);用户级 `~/.claude/agents/`;**无官方方式从非 `.claude/agents/` 目录加载**(`--add-dir` 只给文件访问不扫描 agent) |
| 优先级 (高→低) | managed settings > `--agents` CLI > **项目 `.claude/agents/` > 用户 `~/.claude/agents/` > plugin `agents/`** |
| 调用名 | 项目/用户级 = **裸 name**;plugin = scoped `plugin:agent` |
| frontmatter 容错 | 必需 name+description;**自定义额外字段 (capabilities/audit_points/aria_managed) 是否被安全忽略 = 官方"不确定"**(YAML 标准应忽略,但 CC 可能有 validation 层) |
| 🔴 **session-start 时效** | **"Subagents are loaded at session start. 直接写文件到磁盘 → 当前会话不识别,要重启"**。只有 `/agents` 交互界面创建的即时生效。 |

### 2.2 plugin marketplace 分发 agent 能力 (plugin-marketplaces.md / discover-plugins.md)

**已能做**: agent 分发(plugin-scoped `plugin:agent`)/ 版本(plugin.json version + auto-update)/ **私有 marketplace(git repo + marketplace.json,Forgejo/Gitea 支持)** / 团队订阅(`.claude/settings.json` `extraKnownMarketplaces` 项目级声明依赖)/ agent-only plugin(无最小内容要求)。

**3 个真实 gap(marketplace 做不到 → registry 差异化点)**:
1. **agent 粒度版本** — marketplace 是 plugin **整包原子版本**,无法"升级包内 agent A 保持 agent B"。
2. **scoped agent 不能被项目覆盖** — plugin agent 恒 `plugin:name`,项目无法以同名 shadow/patch;而项目 `.claude/agents/` 裸名**可覆盖** plugin(优先级 #3 > #5)。
3. **无 push-back 贡献流** — marketplace 单向 pull,无"改进 → push 回中央"协作。

**plugin agent 安全限制**: 不支持 `hooks` / `mcpServers` / `permissionMode` / custom `tools`(官方安全约束)。

## 3. 关键设计洞察 (本次 brainstorm 收敛)

### 3.1 软注入 vs 原生 subagent_type — 服务不同时序 (重要)

| 场景 | 软注入 (general-purpose + 注入 agent 定义内容) | 原生 `.claude/agents/` subagent_type |
|------|---|---|
| **当场生成、同 session 即用** | ✅ **唯一可行**(绕过 session-start 限制) | ❌ 要重启 session |
| **预先配置、跨 session 用** | ✅ 可以 | ✅ **更干净,零 workaround** |

- 这解释了**为什么现状 agent-router 用软注入** —— 那是当前 session 用上动态生成 agent 的唯一办法。
- 推论:对**预先配置的项目 agent**(如 audit security auditor),原生 `.claude/agents/` 路径完全够用且更干净;软注入只是"即时生成即时用"的兜底。

### 3.2 双层 `.aria/` source + `.claude/` 部署 — 有真实技术分工(非仅组织整洁)

- **`.aria/agents/` = aria 源 + 管理台账层**:权威定义 + aria 专属元数据(capabilities / audit_points / gap 溯源 / aria_managed)。aria 自己的工具读这里(agent-router 软注入即时用 / state-scanner 盘点 / gap-analyzer 复查)。私有 namespace,不污染 `.claude/`,好清理。**额外理由**:把 aria 元数据留在源层,物化到 `.claude/` 时剥离成纯净原生格式 → 规避 §2.1 "自定义 frontmatter 字段是否被忽略=不确定"的风险。
- **`.claude/agents/aria-<name>.md` = 物化原生部署层**:纯净 CC 格式,`aria-` 前缀隔离,项目级优先级 > plugin。下次 session 起原生 spawn。
- **代价**:同步一致性(改源要重物化)+ 漂移检测(state-scanner)+ session 时效兜底(同 session 即用仍需软注入)。

### 3.3 方法论边界澄清(本次纠偏)

- 曾误判"生成到 `.claude/agents/` 撞 Aria 不绑定 AI 工具的方法论基石" → **owner 质疑后收回**。
- 正解:"不绑定 AI 工具"管的是 `standards/` **方法论层**;aria-plugin(skills/agents/hooks)本就是 100% Claude Code 专属**实现层**;agent 定义文件放 `.aria/` 还是 `.claude/` 都是 CC 格式,放 `.aria/` 不带来任何跨工具可移植性(那是幻觉)。当初选 `.aria/agents/` **无任何"工具无关"理由记录**(SKILL.md 写的是"项目级、不提交 plugin")。
- 真实 trade-off = **共享空间卫生**(`.claude/` 是用户/多 plugin 共享,污染/冲突)+ **迁移成本**(agent-router/subagent-driver 改路径),都可缓解(`aria-` 前缀 + 可清理标记)。

## 4. 与 aria-fleet 三层的映射 (待 M7 确认)

- **L1 通用 (any-org)**: 通用精选 agent(语言/框架无关的 reviewer / architect 等)。
- **L2 workspace (per-org)**: org 私有 agent(如 10cg.local 的 shell-safety-auditor / ssh-egress-security-auditor / homelab-topology-auditor — reporter 实证抓 2 Critical)。
- **L3 instance**: 项目本地 `.claude/agents/`(pull 下来 + 项目自定义覆盖)。
- registry 的 pull/push/version 正是 L1/L2 → L3 的分发/回流机制。

## 5. 待 M7 brainstorm 回答的关键决策

1. **对内 (10CG Lab) vs 对外发布定位** — 对内 = 合 v2.0 reference-impl 例外;对外 = 触及"不提供模板/不绑定工具"边界。这是 M7 战略级问题。
2. **3 个 gap 是否值得自建 registry** — 还是**先用 marketplace 试水**(把 curated agents 打包成 `aria-agents` plugin 经私有 Forgejo marketplace 分发,跑起来验证真实需求,再决定 3 gap 值不值得自建)。**marketplace 已覆盖主诉求(团队 pull + 更新 + 私有 + 版本)**。
3. **registry 与 marketplace 的关系** — 共存?registry 作为 marketplace 之上的 agent 粒度层?
4. **agent 粒度版本 + 项目覆盖 + push-back 的具体机制**(若决定自建)。

## 6. 与 #145 的关系(已剥离)

- #145 本体 = experimental `agent-team-audit` 编排读不到项目 agent(triage verdict **partial-repro/major**,comment 已 POST `#issuecomment-12888`)。
- #145 **小修方案**(与本 registry epic 解耦):selection-matrix 复用 agent-router 的 `.aria/agents/` 发现 + 对预存 `.claude/agents/` agent 原生 spawn。
- 本 registry 是 owner 从 #145 升级出的**独立战略愿景**,scope 远超 #145,归 M7。
