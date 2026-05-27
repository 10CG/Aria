# Design Memo: aria-fleet + 三层架构 + 10CG.local 边界 (2026-05-27)

> **Type**: Design exploration memo (非 OpenSpec 决策 — 沉淀战略对话, 供 M7+ 实施时参考)
> **Context**: 本 session 从 "Aria 看板的视觉/排版改进" 起步, 经 Owner 关键洞察 "现有飞书 bot 接的是 Hermes, aria-hub 是不是该是 Hermes tool pack?" 重新框架了整个 cross-project capability 设计, 并扩展到 Aria 通用性 vs 10CG.local 边界问题。
> **Status**: 战略方向已确认, 实施时机 M7+ (M6 v2.0.0 release 后)
> **Predecessors**:
>   - aria-dashboard v1.1.0 first Aria self-dogfood (2026-05-27, commit `1730884`) — 发现 cross-project gap
>   - 3 Forgejo issues filed: [#125 AB parser](https://forgejo.10cg.pub/10CG/Aria/issues/125) / [#126 audit frontmatter](https://forgejo.10cg.pub/10CG/Aria/issues/126) / [#127 UPM-less rendering](https://forgejo.10cg.pub/10CG/Aria/issues/127)
>   - US-024 M4 ship (2026-05-09) — Hermes + Feishu approval pipeline 已建立, MIT entry-point plugin API 验证
>   - AD3 (M0 T4 Spike, 2026-04-16) — Hermes Option C tool pack 4.5h POC 13/13 pass
> **Owner sign-off**: pending (本 memo 由 AI 起草, 待 owner review)

---

## §1 Naming Decision: `aria-fleet`

### 候选评估

| 名字 | 语义 | 评分 | 决定 |
|------|------|------|------|
| **aria-fleet** ⭐ | "fleet of projects" — Apple/AWS 用 "Fleet View" 同样语义; conductor 比喻自然 | 9/10 | **选定** |
| aria-atlas | "map of all projects" — 全景图 | 8/10 | 备选 |
| aria-vantage | "vantage point" — 观察制高点 | 7/10 | 备选 |
| aria-overview | 太朴素 | 6/10 | drop |
| aria-cockpit | 控制台 — control 含义偏强 | 6/10 | drop |
| aria-dashboard-hub | 暴露实现而非本质 (dashboard 只是渲染之一) | 5/10 | **drop** |
| aria-hub | 太泛 | 4/10 | drop |

### 选定理由

1. **单 word + 跨语言** (中英文都 work)
2. **conductor 比喻**: aria-orchestrator = conductor, fleet = 被 conduct 的项目群, 与 Aria 2.0 vision "AI 主管指挥 AI 工程师群组" 完美 mapping
3. **扩展性**: `fleet status` / `fleet members` / `fleet command` / `fleet health` 都自然成立
4. **不锁定 dashboard**: HTML / Feishu card / CLI / Voice 等多 channel 渲染都是 fleet 的 output mode
5. **业界先例**: Apple MDM "Fleet view", Cloud providers "Fleet management", 用户认知成本低

### 命名规则约定 (本 memo 范围内)

- repo / module: `aria-fleet` (kebab-case)
- Python tool pack name (Hermes entry-point): `aria_fleet` (snake_case per PEP 8)
- Skill 名 (若 wrap 成 Skill): `/aria:fleet-*` (e.g., `/aria:fleet-status`, `/aria:fleet-render`)
- Doc 引用: "aria-fleet" (kebab)

---

## §2 三层架构 (核心设计)

### 全景图

```
┌────────────────────────────────────────────────────────────────┐
│  Layer 1: 通用框架层                                            │
│  (any-org installable, MIT/Apache, 公开)                       │
│  ──────────────────────────────────────────────────────────  │
│  aria-standards/      方法论定义 (无团队特化)                   │
│  aria-plugin/         38 Skills + 11 Agents + Hooks            │
│  aria-orchestrator/   Hermes wrapper + 状态机 + tool pack 框架   │
│  aria-fleet/          跨项目聚合 capability (tool pack 形式)     │
│  aria-templates/      workspace template (orgs fork & init)    │
│                                                                │
│  约束:                                                          │
│   ❌ 不 hardcode forgejo / Aether / 10CG / simonfishgit         │
│   ❌ 不 ship 10CG 的 secrets / API key / 飞书 webhook            │
│   ✅ 提供 abstraction: GitProvider / IMChannel / LLMProvider /   │
│      DeployPlatform / SecretStore                              │
│   ✅ 通过 workspace config 注入具体值                            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                              ▲
                              │ uses (引用 + 升级跟 upstream)
                              │
┌────────────────────────────────────────────────────────────────┐
│  Layer 2: workspace 配置层                                       │
│  (per-org, 私有 repo, 各团队自有)                                │
│  ──────────────────────────────────────────────────────────  │
│  10CG/aria-workspace/                                          │
│  ├── config/                                                   │
│  │   ├── projects.yaml         (10CG 监管的项目清单)            │
│  │   ├── integrations.yaml     (Forgejo URL / Feishu webhook)   │
│  │   ├── llm-providers.yaml    (GLM 5.1 primary, Claude fallback)│
│  │   ├── deploy-platforms.yaml (Aether 配置)                    │
│  │   └── secrets.gpg           (encrypted: keys, tokens)        │
│  ├── playbooks/                                                │
│  │   ├── rotate-pat.md                                         │
│  │   ├── audit-drift-recovery.md                               │
│  │   ├── cf-access-troubleshoot.md                             │
│  │   └── secret-rotation.md                                    │
│  ├── memory-shared/            (跨项目共享 patterns)            │
│  │   ├── team-conventions.md                                   │
│  │   ├── feedback-extracts.md  (from individual .claude/memory/)│
│  │   └── brainstorm-archive/                                   │
│  ├── branding/                                                 │
│  │   ├── logo.svg                                              │
│  │   ├── colors.css                                            │
│  │   └── footer.html                                           │
│  └── artifacts/                (累积资产)                       │
│      ├── audit-archive-2026/   (cross-project audit history)   │
│      ├── dashboard-snapshots/  (定期 archive)                   │
│      └── risk-register.md      (跨项目持续 risk)                │
│                                                                │
│  特征:                                                          │
│   ✅ 完全持有 10CG 实证 / 累积 / 文化                            │
│   ✅ 私有 repo (敏感配置不公开)                                  │
│   ✅ 升级通用层不影响本 repo (cattle vs pets 哲学)               │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                              ▲
                              │ provides workspace bundle
                              │
┌────────────────────────────────────────────────────────────────┐
│  Layer 3: instance 运行层                                       │
│  (running process)                                             │
│  ──────────────────────────────────────────────────────────  │
│  $ aria-orch --workspace 10CG/aria-workspace                  │
│                                                                │
│  Hermes process loads:                                         │
│    • Layer 1 通用 (aria/aria-orchestrator/aria-fleet)          │
│    • Layer 2 workspace (10CG/aria-workspace) — config + assets │
│                                                                │
│  Provides to owner via routing:                                │
│    Feishu chat / Web dashboard / CLI / REST API                │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 关键 abstractions (Layer 1 必须提供)

要让 Layer 1 真正通用, 必须设计这些 abstraction (Layer 2 注入具体实现):

| Abstraction | 接口 | 10CG 实现 | hypothetical 其他 |
|------------|------|----------|------------------|
| **GitProvider** | `clone(url) / push() / pull_request() / issue()` | Forgejo (10cg.pub) | GitHub Enterprise / GitLab / Gitea |
| **IMChannel** | `notify(card) / receive(msg) / subscribe()` | Feishu (10CG group webhook) | Slack / Discord / Teams / Matrix |
| **LLMProvider** | `complete(prompt, route)` | GLM 5.1 (primary) + Claude (fallback per US-027) | OpenAI / Gemini / 自有 LLM |
| **DeployPlatform** | `deploy(image, env) / rollback() / status()` | Aether (Nomad-based) | k8s / ECS / Fly.io |
| **SecretStore** | `get(key) / set(key, value) / rotate()` | Nomad Var (10CG) | Vault / AWS Secrets / sealed-secrets |
| **AuthProvider** | `challenge(req) / verify(token)` | CF Access | Okta / Auth0 / Keycloak |

> Note: 不是 over-engineering — Aria 2.0 vision 本身就要求 cross-org applicable (per PRD §核心定位 "Aria 2.0 是 AI-AI 分工协作的自主软件工程方法论, 由 Layer 1 AI 主管 指挥 Layer 2 AI 工程师 完成端到端开发的**参考实现**")。"参考实现" = template, 必须能被其他 org 复用。

---

## §3 10CG.local 的独特价值

### 问题: aria-orchestrator 跑起来后, 10CG.local 跟通用层怎么区分价值?

### 答: 通用层 = framework, 10CG.local = workspace + 累积资产 + 团队 knowledge graph

### 具体 unique value 清单

| 类别 | 内容 | 为什么 only-10CG |
|------|------|------------------|
| **跨项目 audit 库** | 105 audit reports (truffle-hound + Aria + silknode + aria-plugin + aria-orchestrator) | 10CG 实际 ship 产物 |
| **跨项目 spec 库** | 200+ archived specs | 10CG 实际工作历史 |
| **30+ feedback memory** | `feedback_brainstorm_*` / `feedback_paper_fix_antipattern` 等 | 10CG 实证 patterns (dogfood-driven, 非理论) |
| **Brainstorm decisions** | DEC-20260524-001 (M6) / DEC-20260524-002 (#124) / 等 ~12 个 | 10CG 团队决策 history |
| **跨项目 risk register** | "M6 是否又卡 cost-acceptance" 类 trend insight | 10CG-specific business context |
| **团队文化** | 中文工作语言 / 单 owner / 周末 ship / 跨午夜 UTC session | owner=simonfishgit 的工作习惯 |
| **工具链 binding** | Aether + Forgejo + 飞书 + GLM 5.1 + CF Access 这个 combo | 10CG 自有 infra |
| **跨项目 pattern recognition** | "Spec 拆 sub-PR 三段式 (prereq → parallel → cleanup)" 这种规律 | 跨 N 个项目实践才能 surface |

### 价值层次

```
通用层提供 = capability (能做什么)
  └─ "我能跨项目聚合状态 + AI 自然语言查询 + 多 channel surface"

10CG.local 提供 = context (用什么数据回答)
  └─ "你问 'M6 现在卡哪了', 我用 10CG 实际 M6 数据 + DEC + audit history + memory 回答"

合并 = AI-driven contextualized intelligence
  └─ 不只是 "我能查 Spec 状态", 而是 "我知道 10CG 上次类似问题怎么解的"
```

### 具体例子

```
[场景 A: 通用层 only — hypothetical 其他工作室刚装上 Aria]
owner: M6 现在卡哪了?
Hermes: "我看到 5 个 active Specs (1 标记 'M6')。Spec 'aria-2.0-m6-cost-acceptance'
        Status = Approved, 没有 in-flight 进度。建议你看 proposal.md 了解 next step。"

[场景 B: 通用层 + 10CG.local workspace]
owner: M6 现在卡哪了?
Hermes: 调 aria-fleet.get_project_state("aria")
      + 查 10CG/aria-workspace/memory-shared/feedback-extracts.md
      + 查 10CG/aria-workspace/artifacts/risk-register.md
       "M6 4 sub-Specs 都 Approved 了, Phase B kickoff 等 Spec #1 ship。
        Spec #1 cost-acceptance 是 Spec #2 e2e-resilience 的 3-day data
        precondition (per DEC-20260524-001 Q8 sequencing)。
        建议: 先启 Spec #1 Phase B.1 启 cost gate cron 累积数据,
        同时 Spec #3 docs (TG-DOCS-A v2.0.0-blocker) 可并行不阻塞。
        Risk: 8-2 secret rotation hard cap buffer ~36 days at 5w (RED threshold,
        per Spec #4 release-closeout RED/ABORT gates)。"
```

后者就是 10CG.local 的 unique value — **从通用规则 → contextualized intelligence**。

---

## §4 边界切割规则 (具体)

### 应放通用层

- 框架代码 / 状态机定义 / Hermes tool pack 接口
- Skill 定义 / 模板 / 测试
- Default LLM provider abstraction (GLM/Claude/OpenAI 互换)
- Git provider abstraction
- IM abstraction
- Deploy platform abstraction
- Methodology / 不可协商规则 (Rule #5-#9)
- 5 数据源 parser (UPM/Stories/Specs/Audits/Bench)
- Audit-engine framework
- Brainstorm SKILL 框架
- Pattern memory **schema**
- 文档示例 / placeholder example (e.g., "假设你的 git URL 是 ..." 的 forgejo.10cg.pub mention OK)

### 应放 10CG.local

- 项目清单 (`projects.yaml`)
- API keys / tokens / webhook URLs
- 当前选哪个 LLM + cost routing 配置
- `forgejo.10cg.pub` URL + CF Access binding 实际值
- 实际飞书 group webhook 实际值
- 团队 culture / 工作时间 / language preference 具体值
- 实际 N 个项目的数据 / commit history / etc.
- 实际 audit 历史 (105 reports)
- 实际 brainstorm decisions (DEC-*)
- Pattern memory **content** (30+ feedback)

### 灰色地带 (需 case-by-case 判定)

- `aria-plugin-benchmarks/` 子模块: 通用框架 (eval suite) + 10CG 实证数据 (ab-results/*) 混合
  - 拆: framework 进通用, ab-results 进 10CG.local
- Memory entries: schema 通用 / content 10CG.local
  - 通用层提供 schema + tooling (write / search / prune)
  - Workspace 持有具体 memory file 内容
- Brainstorm DEC: framework 通用 / DEC content 10CG.local
  - 通用层提供 brainstorm SKILL 框架
  - Workspace 持有 DEC-* 实际决策记录

---

## §5 Risk + 现状 audit (parallel task)

### 风险

**关键 risk**: aria-orchestrator M4/M5 现有代码很可能**已经 leaked** 10CG-specific 假设 (hardcoded forgejo.10cg.pub / Aether / 飞书 webhook)。如果不及早分层, 后期拆开是技术债。

### 已发起 audit (本 memo 同时进行)

委托 Explore agent 跑 boundary audit, 产出 `/home/dev/Aria/.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md`:
- grep `forgejo.10cg.pub` / `Aether` / `10cg` / `simonfishgit` 在 aria/ standards/ aria-plugin-benchmarks/ 的位置
- 区分 (D) Doc-mention 无害 vs (C) Code-hardcoded 技术债 vs (P) Path-hardcoded
- 输出 Top 3-5 修复优先级

---

## §6 实施时机 & 路径

### 短期 (M6 之前, ~2-4 weeks)

- ❌ **不动 aria-orchestrator** — 它在 M5/M6 主线, 加 fleet tool pack 会撞 in-flight 工作
- ✅ **用 aria-dashboard skill 替代** — 单项目 use case 沿用本 session dogfood 模式
- ✅ **本 memo 沉淀** — 后续起 fleet 时不重复讨论
- ✅ **Boundary audit** — 找到 hardcoded 位置, 修起来不阻塞 M6

### 中期 (M6 ship 后, v2.0.0 release)

- ✅ **建 10CG/aria-workspace 私有 repo** — workspace template 第一个实例
- ✅ **start `aria-fleet` 通用层** — 作为 aria-orchestrator/extensions/aria-fleet/ Python entry-point plugin
- ✅ **Layer 1 abstraction 完善** — GitProvider / IMChannel / LLMProvider 接口
- ✅ **重构 hardcoded 位置** (based on audit report) — 通用层去除 10CG 假设

### 长期 (post v2.0.0)

- ✅ **aria-fleet 容量扩展** — search / event subscription / cross-project pattern surfacing
- ✅ **第二个 workspace 实例** (验证通用性) — 真实其他工作室 or hypothetical mock workspace
- ✅ **aria-templates** repo — workspace template, 任何 org 可 clone & init

### 不做 (明确 out-of-scope)

- ❌ aria-fleet 重新搭飞书 webhook (复用 US-024 ship 的 feishu-io tool pack)
- ❌ aria-fleet 重新搭 cron / event loop (复用 Hermes 已有的)
- ❌ aria-fleet 独立 hub-api 服务 (Hermes process inline tool pack 调用即可)
- ❌ 等 v2.0.0 之前重构 hardcoded 位置 (audit 先,修复随 M6 之后)

---

## §7 跟 PRD / 现有 milestone 的对应

| PRD/Milestone | 对应本 memo 内容 |
|---------------|-----------------|
| Layer 1 (Hermes AI 主管) | 通用层 = aria-orchestrator core |
| Layer 2 (容器 AI 工程师) | 通用层 = aria-plugin (容器 build-time 预装) |
| US-007 aria-orchestrator | 通用层 framework |
| US-024 M4 Feishu approval | 通用层 = feishu-io tool pack (already shipped) |
| US-025 M5 Replay/Reconciler | 通用层 framework + Workspace 持累积 replay data |
| US-026 M6 4 sub-Specs | M6 ship 后 = aria-fleet 实施起点 |
| US-027 Cost routing | 通用层 = LLMProvider abstraction (各 provider 切换) |
| AD3 (Hermes Option C entry-point plugin) | 本 memo 的 architectural foundation |
| AD11 (CLAUDE.md 不动) | workspace 层应该有 workspace-CLAUDE.md (类似), 不污染通用 |
| AD12 (aria-orchestrator 不剥离) | 通用层一致性 |

---

## §8 决策点 (待 owner sign-off)

| 决策 | 推荐 | 备选 | 状态 |
|------|------|------|------|
| **D1 命名** | `aria-fleet` | `aria-atlas` / `aria-vantage` | pending owner |
| **D2 架构** | 三层 (通用 / workspace / instance) | 当前 monolithic | pending owner |
| **D3 实施时机** | M6 ship 后 (M7+) | 现在 (M6 之前) | pending owner |
| **D4 workspace repo** | 10CG/aria-workspace 私有 repo | 直接放 10CG/Aria 主仓 | pending owner |
| **D5 fleet 形态** | aria-orchestrator/extensions/aria-fleet/ tool pack | 独立 repo 10CG/aria-fleet | pending owner |
| **D6 短期** | aria-dashboard skill 沿用 + boundary audit + 本 memo 沉淀 | 立即建 aria-fleet | pending owner |

---

## §9 Memory 候选 (本 session 反思)

候选 cross-cycle valuable insights (待 owner 判断是否固化):

| Candidate | Cross-cycle valuable? |
|-----------|---------------------|
| **"hub 不应该是 standalone service, 在 agent OS vision 下应该是 tool pack"** | ✅ YES — universal pattern: 任何 cross-cutting capability 在有 agent OS 时该是 plugin 不是 service. Memory key candidate: `feedback_cross_cutting_capability_as_agent_tool_pack` |
| **"通用 / workspace / instance 三层架构"** | ✅ YES — universal SaaS-style architecture pattern for AI-driven systems. Memory key candidate: `feedback_three_layer_universal_workspace_instance` |
| **"飞书 / web / CLI 等 channel 是 AI agent 的 render output, 不该单独建 bot"** | ✅ YES — 设计原则. Memory key candidate: `feedback_channels_as_agent_render_outputs` |
| **"10CG.local 的 unique value = 累积 + contextualized intelligence, 不是 features"** | ⚠ 可能 too org-specific, 但其他工作室也适用 (any-org's workspace value = accumulated context). Memory key candidate: `feedback_workspace_value_is_accumulated_context` |

owner 判 ≥1 个固化, 其余降级为本 memo 注脚。

---

## §10 Cross-references

### Forgejo issues (待本 memo 决议影响优先级)
- [#125 aria-dashboard AB parser](https://forgejo.10cg.pub/10CG/Aria/issues/125) — 仍有价值 (无论 standalone 或 tool pack)
- [#126 audit-engine YAML frontmatter](https://forgejo.10cg.pub/10CG/Aria/issues/126) — 仍有价值 (cross-cutting supply-side constraint)
- [#127 aria-dashboard UPM-less rendering](https://forgejo.10cg.pub/10CG/Aria/issues/127) — **降级**: aria-fleet tool pack 可 dynamically 决定哪些 section 渲染, 不再是 hard problem。可 close 或 mark "deferred to aria-fleet design"

### 引用文档
- PRD: `docs/requirements/prd-aria-v2.md` §核心定位 / §Hermes 集成方式 / §AD3
- US-007: `docs/requirements/user-stories/US-007.md` (aria-orchestrator)
- US-024: `docs/requirements/user-stories/US-024.md` (Human gate + Feishu, M4 ship)
- US-027: Cost routing (LLM provider abstraction)
- AD3: M0 T4 Spike, entry-point plugin API POC 13/13
- aria-dashboard SKILL: `aria/skills/aria-dashboard/SKILL.md` v1.1.0

### Predecessor session artifacts
- Spec proposal: `openspec/changes/aria-submodule-gate-block-flip/proposal.md` (本 session shipped Phase A)
- Handoff: `docs/handoff/2026-05-25-v1.29.0-flip-phase-a-approved.md`
- Dashboard dogfood: `.aria/dashboard/index.html` (commit `1730884`)

### 平行 audit (本 memo 同时进行)
- `/home/dev/Aria/.aria/notes/2026-05-27-boundary-audit-10cg-hardcode.md` (待 Explore agent 完成)

---

**Created**: 2026-05-27 (session continued from 2026-05-25 ~14:35Z and 2026-05-27 ~02:00Z)
**Author**: AI (Claude Opus 4.7 1M context) via owner-driven dialog
**Status**: Strategic direction confirmed; implementation deferred to M7+
**Next**: owner review → D1-D6 sign-off → 在 M6 ship 前后启动 M7 OpenSpec brainstorm 阶段
