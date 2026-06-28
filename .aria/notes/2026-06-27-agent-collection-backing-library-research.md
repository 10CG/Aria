# 调研:GitHub agent 合集作为 Aria backing library 的可行性

> **Created**: 2026-06-27
> **Author**: AI (Claude Opus 4.8 1M context) via owner-driven deep-research (100 agent / 6.5M token / 5 角度搜索 + 3 票对抗式交叉验证)
> **目的**: 回答 M7 agent-lifecycle Spec 悬而未决的输入 —— "集合库 (collection repo) 从哪来";评估能否用现成高星仓库当 backing library, 省去从零造 agent。
> **上游**: [.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md](./2026-06-16-agent-lifecycle-management-for-aria-fleet.md) (§1 决策 #2: git 集合库 vs marketplace)
> **Tracker**: Forgejo Aria #128 (评论已贴)

---

## TL;DR

1. **有现成、高星、MIT、格式原生兼容的库可复用** —— 不必从零造集合库。
2. **首选 `VoltAgent/awesome-claude-code-subagents`** (格式零转换 + 带 tools 字段 + 分类目录可索引 + 维护活跃)。
3. **Aria 现有 agent 名极可能来自 `wshobson/agents`** (命名一一对应, provenance 仅 "likely" 未逐 prompt 确证)。
4. **但不建议整库 vendor, 建议选择性 cherry-pick** —— 质量未验证 (撞 Rule #6) + 缺 capabilities 标签 (接不进 agent-router/audit) 是两个硬成本。

---

## 候选库对比 (star/数量为近似, 变动快, 用前实时核)

| 仓库 | ★ | agent 数 | 格式 | 目录结构 | 许可证 | 维护 | 适配度 |
|------|----|---------|------|---------|--------|------|--------|
| **VoltAgent/awesome-claude-code-subagents** | ~22.5k | 154+ | ✅ 原生 CC subagent (name/desc/**tools**/model + body) | 10 个编号分类目录, 扁平逐文件可索引 | MIT | 活跃 (commit 2026-06-24) | **最高** |
| **wshobson/agents** | ~37.3k | 194 | ✅ 合法 .md+frontmatter | ⚠️ 重构成 multi-harness marketplace: agent 嵌在 `plugins/*/agents/*.md`, name 被 plugin 前缀污染 (如 `backend-development-backend-architect`) | MIT | 很活跃 (508 commits) | 中 (需树遍历+剥前缀) |
| **0xfurai/claude-code-subagents** | — | 100+ | ⚠️ frontmatter 仅 name/desc/model, **无 tools、无 tags** | 扁平 `agents/*.md` | MIT | — | 中 (缺机读元数据) |
| lst97/claude-code-sub-agents | — | ~33 (存疑) | ✅ 原生 | 扁平 | MIT | — | 低 (规模太小) |
| ~~VoltAgent/awesome-agent-skills~~ | — | 1000+ | ❌ 是 Skills (SKILL.md) **不是 subagent** | — | MIT | — | **不匹配, 勿混淆** |

**官方格式锚定** (code.claude.com/docs/en/sub-agents): subagent = Markdown + YAML frontmatter, 仅 `name`+`description` 必填, `tools`/`model`/`skills`/`color` 可选, 未知 YAML key 被忽略而非报错; 文件存 `.claude/agents/` (项目级) 或 `~/.claude/agents/` (用户级); 官方明确推荐 **check 进版本控制供团队共享** —— 与 M7 "物化进 .claude/agents/ 原生加载" 计划完全吻合。

## 推荐排序

1. **VoltAgent/awesome-claude-code-subagents** —— M7 backing library 首选 (格式零转换、带 tools、分类目录适合机器索引、维护活跃)。
2. **wshobson/agents** —— 作为**质量/血缘对照源**最有价值 (规模最大、最可能是 Aria agent 血缘来源、口碑好); 但已变 marketplace, 扁平索引被破坏, 机器消费需剥前缀+树遍历。可用它核对 Aria 现有 agent 落后 upstream 多少 (= 生命周期更新提示机制的基线)。
3. 0xfurai —— 备选, 缺 tools/tags, enrich 成本更高。

## 复用风险 (= 为什么不整库 vendor)

1. **质量未验证 (最关键)**: 所有候选库白纸黑字 "provided as-is, 无安全/正确性审计"。prompt 质量参差无第三方背书 → **直接撞 Rule #6** (agent 价值必须 benchmark 验证)。vendor 进来的 agent **仍要过 AB/对抗审计** 才能进 roster。省的是写 prompt 的功, 省不了验证的功。
2. **元数据缺口**: 所有候选库用标准 CC frontmatter, **全无** Aria `.aria/agents/` STCO 的 `capabilities` 标签 —— 那是 `agent-router` / `agent-gap-analyzer` / `agent-team-audit` selection-matrix (#145 那条断裂) 消费的机读字段。整库 vendor 后**必须自行 enrich capabilities**, 否则接不进 Aria 现有路由/审计链。
3. **许可证义务**: MIT 允许 vendor/再分发, 但须保留各库版权声明 + LICENSE 文本 (非零成本)。
4. **血缘只 "likely"**: wshobson 是命名推断, 未逐 agent 比对 prompt 正文确证。
5. **计数易漂**: wshobson 几个月 29k→37k★; 数字用前实时核。

## 对 M7 的直接影响

- **不必从零造集合库**: 用 VoltAgent 做 seed → M7 TG-A "集合库骨架" 大幅省力。
- **M7 真正工作量不在"收集"而在"治理"**: enrich capabilities 标签 + 过 Rule #6 benchmark 筛选 + 建版本更新提示 —— 这三件恰好接 Aria 已有能力 (`agent-gap-analyzer` / `/skill-creator` AB / lockfile)。
- **印证 "先下行 pull 半环"**: 先把外部库拉下来用, 才有数据驱动后续吸收/回流 (memo §7)。
- **不改变当前阻塞**: M7 Phase B 仍受 M6 ship 的 D3 时机门, 本调研是**解锁后准备**。

## Open Questions (留 M7 立项)

1. ~~wshobson 是否确为 Aria agent 精确来源?~~ **✅ RESOLVED (2026-06-27, web 比对)**: Aria `backend-architect` body 开头与 wshobson 逐字近同 ("You are a backend system architect specializing in scalable...") + 同款 "Use PROACTIVELY when creating new backend services or APIs" description → **确定派生自 wshobson 早期版本**, 再叠 Aria 定制 (STCO description + `capabilities:` 标签 + color + 显式 model tier)。**Aria 副本已滞后 upstream**: 现 wshobson 已演进为 `## Purpose / ## Core Philosophy / ## Capabilities` 结构 + marketplace 命名空间前缀 (`backend-development-backend-architect`, model:inherit)。→ 这是 M7 TG-C 版本更新检测的天然基线; 重 vendor 须在 upstream 上重叠 Aria 定制层。
2. VoltAgent vs 0xfurai 领域覆盖重叠/互补程度? 多源聚合 vs 单选?
3. 各库 prompt 在 Aria Rule #6 benchmark (AB/pairwise LLM-judge) 下真实表现? with/without delta 是否正向 → 决定 cherry-pick 取舍标准。
4. VoltAgent (有 tools/model 无 capabilities) → Aria STCO 格式的自动 enrichment 成本? 能否用 project-analyzer/agent-gap-analyzer 链反向推导 capabilities 标签?

## 来源 (primary)

- https://github.com/wshobson/agents (+ /blob/main/docs/agents.md, /tree/main/plugins)
- https://github.com/VoltAgent/awesome-claude-code-subagents
- https://github.com/0xfurai/claude-code-subagents
- https://github.com/lst97/claude-code-sub-agents
- https://github.com/VoltAgent/awesome-agent-skills (区分陷阱: 是 Skills 非 subagent)
- https://code.claude.com/docs/en/sub-agents (官方格式权威)
