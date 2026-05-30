# Aria - AI-DDD Methodology

> **项目本质**: AI-DDD 方法论的定义与端到端参考实现 (v1.x 方法论 + v2.0 自主运行时)
> **核心假设**: AI 不仅是协作者 (v1.x), 更是 SDLC 的自主执行者 (v2.0)
> **版本**: 2.0.0

---

## 文档边界

| 文档 | 受众 | 目的 |
|------|------|------|
| **README.md** | 人类用户 | 项目介绍、快速开始、使用指南 |
| **CLAUDE.md** | AI 助手 | 项目定位、上下文地图、不可协商规则 |

**README.md** = "用户如何使用 Aria"
**CLAUDE.md** = "AI 如何理解 Aria 项目"

## 工作语言

**Aria 工作语言 = 中文**。AI 助手与 owner 对话默认中文叙述,不要大量中英混杂。

**保留英文**(技术 token,翻译反而损害清晰度): 代码 / 命令 / 文件路径 / git SHA / branch / PR# / 版本号 / commit message / spec 术语 (Phase A.1 / Rule #7 / OpenSpec / Layer L / Q-NEW etc.) / 工具/Skill/Agent 名 / memory 引用。

**用中文**: 叙述 / 解释 / 进度更新 / 建议 / 风险说明 / 询问 (含 AskUserQuestion options) / handoff prose 段落 / audit verdict 判定。

详细 do/don't + 实证: memory `user_chinese_conversation_default`。

---

## 项目定位

Aria 是一个**方法论研究项目**，而非框架实现。它探索如何让 AI Agent 深度参与软件工程全流程，从需求到交付的完整协作模式。

### 核心假设

```
传统模式: 人类主导 → AI 辅助
Aria 模式: AI 理解 → 人类确认 → 协作交付
```

### 身份演进 (v1.x → v2.0)

```
v1.x 定位: 方法论研究项目 (人类交互式)
v2.0 定位: 方法论定义 + 端到端参考实现 (AI 自主式)
```

v1.x 的十步循环已被验证为可执行, v2.0 把同一套方法论放到**无人值守**场景下验证。两者共享方法论本体, 区分在于**执行主体**:
- v1.x: 人类 + Claude Code (interactive)
- v2.0: Hermes (Layer 1) + aria-runner 容器 (Layer 2)

详细运行时架构见 [aria-orchestrator/docs/architecture-decisions.md](aria-orchestrator/docs/architecture-decisions.md) (AD1-AD12)。

### 研究目标

1. **可重现的 AI 协作流程** - 不同项目、不同 AI 都能获得一致结果
2. **最小化的上下文传递成本** - AI 能快速理解项目状态
3. **结构化的决策记录** - 每个"为什么"都有据可查

---

## 核心概念

### AI-DDD (AI-Assisted Domain-Driven Design)

领域驱动设计的 AI 增强版，强调 AI 对业务领域的理解和建模能力。

### 十步循环 (Ten-Step Cycle)

```
A. 规划 (Spec & Planning)
├── A.0 状态扫描    → 理解当前在哪
├── A.1 规范创建    → 定义要去哪
├── A.2 任务规划    → 规划怎么去
└── A.3 Agent 分配  → 谁去执行

B. 开发 (Development)
├── B.1 分支创建    → 隔离工作空间
├── B.2 执行验证    → 开发+评审 (Skill 变更时含 /skill-creator benchmark)

C. 集成 (Integration)
├── C.1 提交        → 记录变更
└── C.2 合并        → 集成到主干

D. 收尾 (Closure)
├── D.1 进度更新    → 同步状态
└── D.2 归档        → 完成闭环
```

### 两层 AI 分工 (v2.0 新增)

v2.0 在"十步循环"之上建立了两层执行结构:

- **Layer 1 (主管)**: Hermes + Luxeno-routed GLM models, 做 PM 角色 (triage / 派发 / 审批)
- **Layer 2 (工程师)**: aria-runner 容器 + Claude Code + aria-plugin, 做工程师角色 (执行十步循环)

两层通过**拟人命令**(自然语言 YAML) 通信, 不用结构化 RPC。详见 AD1 + AD6。

**重要**: Layer 1 **不加载** aria-plugin, 只加载 ~1K token 元知识 (AD7); Layer 2 **完整加载** aria-plugin, 执行完整十步循环。

### OpenSpec 需求规范

标准化的需求描述格式，让 AI 和人类对"做什么"达成共识。

- **Level 1**: Skip - 简单修复，无需规范
- **Level 2**: Minimal - `proposal.md`
- **Level 3**: Full - `proposal.md` + `tasks.md`

---

## 认知框架

理解 Aria 项目的四个原则:

### 1. 规范先行 (Spec First)

```
❌ 先写代码，后补文档
✅ 先写规范，后写代码

原因: AI 需要理解"为什么"才能给出好的建议
```

### 2. 小步迭代 (Incremental)

```
❌ 大爆炸式重构
✅ 每个任务 4-8 小时可完成

原因: 小步快跑，风险可控，AI 容易验证
```

### 3. 文档同步 (Docs in Sync)

```
❌ 代码和文档分离维护
✅ 架构文档与代码同步演进

原因: AI 通过文档理解结构，文档过时 = AI 误解
```

### 4. 向后兼容 (Backward Compatible)

```
❌ 破坏性变更
✅ 所有变更保持兼容

原因: 方法论需要稳定性，频繁弃用会破坏信任
```

---

## 信息地图

### 子模块职责

| 子模块/目录 | 职责 | 关键内容 |
|-------------|------|----------|
| `standards/` | 方法论定义 | 十步循环、OpenSpec、约定 (含 secret-hygiene / **session-handoff**) |
| `aria/` | 工具集 (Plugin) | Skills + Agents + Hooks 配置 |
| `aria-plugin-benchmarks/` | Skill 基准测试 | AB 测试套件、结果存档、运维手册 |
| `docs/handoff/` | Session handoff records | 跨 session 优先级 / carry-forward / 实战教训传递 (Rule #9) |
| `aria-orchestrator/` | v2.0 运行时 (Layer 1/2) | Hermes fork / Docker 镜像 / Nomad job / ADR |

### 目录导航

```
需要理解 X? 找这里:

├── 项目定位       → standards/methodology/aria-brand-guide.md
├── 工作流程       → standards/core/ten-step-cycle/
├── 需求规范       → standards/openspec/project.md
├── 提交规范       → standards/conventions/git-commit.md
├── Secret 卫生   → standards/conventions/secret-hygiene.md (Rule #7)
├── Session handoff → standards/conventions/session-handoff.md (Rule #9, v1.21.0+)
├── Submodule pointer 卫生 → standards/conventions/submodule-pointer-hygiene.md (aria-plugin v1.28.0+ §C.2.4.5 mechanical gate companion)
├── 进度管理       → standards/core/progress-management/
├── 研究文档       → docs/
├── 需求文档       → docs/requirements/ (PRD + User Stories)
├── 架构文档       → docs/architecture/system-architecture.md
├── Session handoff → docs/handoff/{date}-{slug}.md (canonical, Rule #9)
├── 项目配置       → .aria/config.json (从 config.template.json 复制)
├── 配置加载       → aria/skills/config-loader/ (内部基础设施)
├── Skill 基准测试 → aria-plugin-benchmarks/AB_TEST_OPERATIONS.md
├── AB 测试数据    → aria-plugin-benchmarks/ab-results/latest/summary.yaml
├── AB 固定测试集  → aria-plugin-benchmarks/ab-suite/
├── Aria 2.0 架构决策  → aria-orchestrator/docs/architecture-decisions.md
└── Layer 边界契约     → aria-orchestrator/docs/layer-boundary-contract.md
```

### Plugin 调用方式 (Aria 项目内部)

在 Aria 项目内部，Skills 和 Agents 可以直接调用：

```
Skills:
  /state-scanner
  /spec-drafter
  /workflow-runner

Agents:
  /tech-lead
  /backend-architect
  /knowledge-manager
```

其他项目通过 Plugin 安装后使用 `/aria:` 前缀。

### Git 子模块操作

```bash
# 更新所有子模块到远程最新
git submodule update --remote

# 更新单个子模块
git submodule update --remote aria
git submodule update --remote standards

# 初始化 (首次 clone 后)
git submodule update --init --recursive

# 查看子模块状态
git submodule status
```

### Forgejo API (PR Operations)

Forgejo 位于 Cloudflare Access 后，使用 `forgejo` CLI wrapper：

```bash
# 路径: /home/dev/.npm-global/bin/forgejo
# 用法: forgejo <METHOD> <ENDPOINT> [curl options]

forgejo GET /repos/10CG/Aria/pulls                    # 列出 PR
forgejo GET /repos/10CG/Aria/pulls/1                   # 查看 PR
forgejo POST /repos/10CG/Aria/pulls -d '{              # 创建 PR
  "title": "feat: description",
  "head": "feature-branch", "base": "master"
}'
forgejo POST /repos/10CG/Aria/pulls/1/merge -d '{"Do": "merge"}'  # 合并
```

---

## 技术约束

### Aria 不做什么

- ❌ 不提供代码生成模板
- ❌ 不强制特定编程语言
- ❌ 不绑定特定 AI 模型
- ❌ 不提供 CI/CD 配置

### Aria 的边界

```
┌─────────────────────────────────────────────────────────┐
│                   Aria 的边界                           │
├─────────────────────────────────────────────────────────┤
│  ✅ 定义: 如何思考、如何协作、如何决策                 │
│  ✅ 规范: 文档格式、工作流程、命名约定                 │
│  ❌ 实现: 具体代码、工具配置、部署脚本                 │
│  ✅ 实现 (v2.0): 端到端参考实现 (aria-orchestrator,    │
│                  仅限 10CG Lab 内部)                    │
└─────────────────────────────────────────────────────────┘
```

**v2.0 的例外**: Aria 2.0 的运行时层 (`aria-orchestrator/`) 是**方法论的参考实现**, 不是通用框架。它仅供 10CG Lab 内部使用, 不对外发布, 不构成 Aria 对"实现"的背书。其他项目仍应把 Aria 方法论视为"如何思考", 而非"用什么工具"。

---

## 版本管理规范

### 版本号语义

遵循 [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR: 破坏性变更 / 架构重构
MINOR: 新功能 / 向后兼容
PATCH: Bug 修复 / 小改进
```

### Aria 特殊约定

| 变更类型 | 版本变更 | 示例 |
|----------|----------|------|
| 新增 Skill | MINOR+ | 1.2.0 → 1.3.0 |
| Skill 架构重构 | MINOR+ | 1.2.0 → 1.3.0 |
| 文档更新 | PATCH | 1.3.0 → 1.3.1 |
| Bug 修复 | PATCH | 1.3.0 → 1.3.1 |
| 破坏性变更 | MAJOR+ | 1.x → 2.0 |

### 版本信息文件架构

```
aria/
├── .claude-plugin/
│   ├── plugin.json       # 主版本文件 (真理来源 Source of Truth)
│   └── marketplace.json   # 市场发布配置
├── hooks/
│   └── hooks.json        # Hooks 配置 (SessionStart 中断恢复检测)
├── VERSION               # 人类可读版本快照
├── CHANGELOG.md          # 版本变更记录
└── README.md             # 包含版本号
```

### 版本发布检查清单

每次发布新版本时，必须更新以下文件：

```yaml
真理来源 (Source of Truth):
  - [ ] aria/.claude-plugin/plugin.json (version 字段)

派生文件 (必须同步):
  - [ ] aria/.claude-plugin/marketplace.json (version, plugins[].version)
  - [ ] aria/hooks/hooks.json (确保 hooks 配置正确)
  - [ ] aria/VERSION (创建或更新)
  - [ ] aria/CHANGELOG.md (添加新版本条目)
  - [ ] aria/README.md (更新版本号和 Skills 数量)

Skill 基准测试 (新增或修改 Skill 时):
  - [ ] /skill-creator benchmark 已执行 (with/without AB 对比)
  - [ ] with_skill 通过率高于 without_skill (delta 为正值)
  - [ ] 人类已审阅结果并确认 Skill 有正向价值
  - [ ] 结果已存入 aria-plugin-benchmarks/ab-results/ (常态化积累)

主项目:
  - [ ] 更新子模块指针 (git add aria)
  - [ ] 主项目/VERSION 更新插件版本记录

多远程推送 (v1.15.0+ 自动化):
  - [x] Phase C.2.5 自动推送所有 enforced remote + post-push SHA 验证 (见 aria/skills/phase-c-integrator/SKILL.md)
  - [ ] 若 C.2.5 报错 → 按错误提示手动修复后继续
  - [ ] 灾备 (C.2.5 完全不可用时, 保留作为人工 fallback):
    - aria 子模块: git -C aria push origin master && git -C aria push github master
    - standards 子模块 (如有变更): git -C standards push origin master && git -C standards push github master
    - 主项目: git push origin master && git push github master
```

> **为什么需要多远程推送**: Claude Code 插件市场从 GitHub 拉取,Forgejo 是主开发仓库。
> 仅推送 Forgejo 会导致市场版本滞后。2026-04-10 事故: aria v1.11.1 发版后未推送 GitHub,
> 市场停留在 v1.11.0。

### 版本信息一致性

所有版本信息文件必须保持一致：

| 文件 | 字段 | 示例 |
|------|------|------|
| plugin.json | `version` | `"1.3.0"` |
| marketplace.json | `version`, `plugins[].version` | `"1.3.0"` |
| VERSION | `版本` | `1.3.0` |
| CHANGELOG.md | `## [X.Y.Z]` | `## [1.3.0]` |
| README.md | `**Version**: X.Y.Z` | `**Version**: 1.3.0` |

**重要**: `plugin.json` 是版本号的**真理来源 (Source of Truth)**，其他文件必须与其保持一致。

---

## 与其他方法论的关系

```
                    DDD (领域驱动设计)
                           │
                           │ 延伸
                           ▼
                    AI-DDD (本项目的核心)
                           │
                           │ 具体化
                           ▼
                  十步循环 (工作流)
                           │
                           │ 形式化
                           ▼
                 OpenSpec (需求规范)
```

---

## 不可协商规则

这些规则是 Aria 的基石，违背它们就不符合 Aria 方法论:

1. **所有需求变更必须有 OpenSpec** - Level 2 或 Level 3
2. **十步循环不能跳过 Phase A** - 必须先理解现状再行动
3. **文档与代码必须同步更新** - 架构文档与代码一致
4. **每个提交必须遵循规范** - Conventional Commits 格式
5. **项目变更必须在项目的 openspec/changes/ 目录** - 不得放在 `standards/openspec/changes/`

```
┌─────────────────────────────────────────────────────────────────┐
│  规则 #5: 变更位置边界 (OpenSpec 兼容)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  aria-standards/openspec/changes/  → 已废弃，不应使用           │
│                                                                 │
│  项目/openspec/changes/            ← 正确位置                   │
│  ├── Aria/openspec/changes/        → Aria 自身的变更            │
│  └── your-project/openspec/changes/ → 用户项目的变更            │
│                                                                 │
│  原因: aria-standards 是共享子模块，变更应属于项目自身           │
└─────────────────────────────────────────────────────────────────┘
```

6. **Skill 基准测试必须使用 `/skill-creator`** - 不得使用自研 runner

**规则 #6 要点:** 只有 with/without AB 对比能回答"Skill 是否提升了质量"。自研 runner (`aria-plugin-benchmarks/runner/`) 已废弃。

**触发时机:** 新增 Skill / 修改 Skill 逻辑 / 修改 description / 发版前质量审计

**操作:** `/skill-creator` → benchmark 流程 → 结果存入 `aria-plugin-benchmarks/ab-results/`

**详细运维手册:** `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`

**不需要 OpenSpec:** 运行 benchmark 是验证活动。发现需要改进时才需要 OpenSpec。

7. **Secret 写入/读取命令必须 redirect output** - 详见 `standards/conventions/secret-hygiene.md`

**规则 #7 要点:** Secret 命令的 stdout/stderr 不得流入 chat-visible 通道。Bash 强制 `>/dev/null 2>&1`; Python `subprocess` 强制 `capture_output=True` (且不 print) 或 `stdout=DEVNULL`。验证用 metadata (status code / 字段长度 / `nomad var get -out=keys` 仅取 key 名), 不读 secret value 字面。Exception 必须 `# secret-leak-ok-explicit` 注释 + 理由 + 隔离环境证据 + owner sign-off。

**触发场景:** `nomad var put/get` / `kubectl create secret` / `vault kv put` / `gh secret set` / `forgejo POST /tokens` / cloud secret manager / DB password commands / `cat <key-file>` / `echo $SECRET` / `nomad job inspect` (含 runtime env)。完整清单见规范 §2。

**Source incidents:** 2026-05-02 Aria 自身 (4 keys via `nomad inspect`) + 2026-05-06 truffle-hound (4 keys via Python subprocess inherit stdio); Forgejo Issue [#78](https://forgejo.10cg.pub/10CG/Aria/issues/78).

**详细规范 + 正向 pattern + exception 模板:** `standards/conventions/secret-hygiene.md`

8. **PR merge 前必跑 pre-merge gate** - 详见 `aria/skills/phase-c-integrator/SKILL.md §C.2.4` (v1.3.0+, v1.31.0+ 通过 CI backend 抽象层支持多 CI 后端)

**规则 #8 要点:** Phase C.2 PR merge 前必须通过 phase-c-integrator C.2.4 pre-merge precondition gate 验证 (a) 本 PR CI 已 passing; (b) main 分支无 in-flight CI run。Gate 通过 **CI backend 抽象层** (`aria/skills/phase-c-integrator/scripts/ci_backends/`) 调用配置的 CI primitive — v1.31.0+ 支持多 backend (Aether 默认 / GitHub Actions stub),通过 `.aria/config.json` 的 `phase_c_integrator.pre_merge_gate.ci_backends` 或自动 probe 选择。`wait` 状态由 workflow-runner `wait_recoverable` 错误类型处理 (指数退避 + Ctrl-C escape hatch),**不**视为 workflow failure。

**触发场景:** Phase C.2 action 流程中 (auto_merge 或 user-triggered merge) 必须经过 C.2.4 gate。`auto_merge=true` workflow 自动调用; `auto_merge=false` user 触发 merge 前由 phase-c-integrator 强制 invoke。

**Source incidents:** 2026-05-02 SilkNode PR-321 cancel PR-322 main CI Run #3161 (459s 部署观测丢失);Forgejo Issue [#60](https://forgejo.10cg.pub/10CG/Aria/issues/60)。

**Exception:** 项目无可用 CI backend (所有 backend probe=False) 时按配置 `phase_c_integrator.pre_merge_gate.no_ci_fallback` 降级:`skip_with_warning` (默认,记录到 workflow report) / `abort` (严格模式)。Exception 必须在项目 `.aria/config.json` 显式声明字段。**Backward-compat (v1.31.0+):** 旧 key `no_aether_fallback` 仍可读取并发 deprecation warning,将于 v2.0 移除。

**NIE-propagation 安全约束 (v1.31.0+, Hard Constraint #7):** 当某 backend probe=True 但 query 方法 raise `NotImplementedError` (stub backend, 如 GitHub Actions v1.31.0 stub),gate **必须 abort** (raise to caller),**不允许** catch-and-route 到 `no_ci_fallback`。这防止"装了 `gh` CLI 但实际用 Aether"的项目因 GHA stub 抢先注册而 Rule #8 静默降级。如需禁用 backend probing,显式设 `ci_backends: []` (explicit disable)。

**Primitive responsibility split:**
- **CI backend 实现** 提供 query primitives (each backend in `ci_backends/`):
  - Aether (默认 backend, 10CG Lab 内部): `aether ci status --branch X --in-flight --json` query (aether-cli #116 SHA `f29abee` 2026-05-06)
  - GitHub Actions (stub v1.31.0+, real 实现 deferred): `gh run list --json` 待实施
- **aria 消费 + verdict 计算**: phase-c-integrator C.2.4 + workflow-runner `wait_recoverable` + 本规则 #8 强制约束

**详细实施规范:** `aria/skills/phase-c-integrator/SKILL.md §C.2.4` + §C.2.4.X CI Backends (与 Rule #7 引用 `standards/conventions/secret-hygiene.md` 同结构)

9. **Session handoff docs 必须写在 `docs/handoff/`** - 详见 `standards/conventions/session-handoff.md` (aria-plugin v1.21.0+)

**规则 #9 要点:** session handoff 文档 (`docs/handoff/{YYYY-MM-DD}-{slug}.md`) 必须写在 `docs/handoff/` (canonical), 禁止写 `.aria/handoff/*.md`。`.aria/` 是机器状态 namespace, `docs/` 是人类/AI 可读 prose namespace; handoff 是 prose 范畴。5 层 defense-in-depth: L1 PreToolUse hook 阻断写入 + L2 scan.py collector 检测 misplaced + L3 state-scanner 推荐迁移 + L4 本规范 (Convention SOT) + L5 phase-d-closer D.3 template 硬编码输出路径。

**触发场景:** session 跨度 > 4h **或** 本 session 完整 ship ≥ 2 cycles/US **或** 本 session 跨 ≥ 2 phases。phase-d-closer D.2 archive 完成后, D.3 step 评估上述条件 (4-level fallback 信号), 满足则 prompt user 写 handoff (template `aria/templates/session-handoff.md`, 9-section skeleton 含 §0 入口 / §1-§7 标准段 / §8 memory entries)。

**Source incidents:** 4 起 dogfood (SilkNode 2026-05-09 1 起 + Aria self 2026-05-13 3 起,含 H0 spec 起草本 session 自身);Forgejo Issue [#92](https://forgejo.10cg.pub/10CG/Aria/issues/92) (triage [#6170](https://forgejo.10cg.pub/10CG/Aria/issues/92#issuecomment-6170)).

**Exception:** **零 exception** (与 Rule #7 不同, handoff 路径选择无 ambiguity 边缘场景)。任何 `.aria/handoff/*.md` 写入企图都应 redirect 到 `docs/handoff/`。

**Extension** (multi-terminal-coordination, aria-plugin v1.22.x+):
Rule #9 在 v1.22.x 引入机读 frontmatter schema (Layer H, §2.3, 5 字段:
`track-id` / `owner-container` / `phase` / `status` / `updated-at`)。state-scanner
Phase 1.16/1.17 从此跨分支 fetch + 重建多 track 看板,根除单写者 `latest.md` pointer
branch-local siloing 问题。Layer L (TASK-010~022, P2 shipped) 补充 claim/reconcile
协调机制:急切认领闸门 (phase1_gate) + orphan ref claim YAML + 确定性 reconcile 6-rule。
详见 `openspec/changes/multi-terminal-coordination/`
(Approved 2026-05-19 per DEC-20260519-001) + `standards/conventions/session-handoff.md §2.3`。

**详细规范 + 9-section template + 5 层 enforcement matrix + migration notes:** `standards/conventions/session-handoff.md`

---

## Aria 2.0 运行时 (参考实现层, v2.0.0 in progress)

Aria 2.0 引入"参考实现层", 把 v1.x 的十步循环方法论**端到端自动化**。这一层**不改变方法论本体**, 只改变执行主体。

### 分层叙述

```
方法论层  standards/          ← 思考/协作/决策规范 (v1.x 不变)
工具层    aria-plugin (+ CC)  ← 交互式使用 (不变) + Layer 2 容器内嵌
运行时层  aria-orchestrator/  ← v2.0 新增, 仅 10CG Lab 内部
          ├── Layer 1: Hermes + Luxeno-routed GLM models (AI 主管)
          └── Layer 2: aria-runner 容器 (AI 工程师)
```

### 与 9 条不可协商规则的关系

v2.0 运行时**严格遵守** 9 条规则, 规则由 Layer 2 容器内的 aria-plugin 负责执行:
- Rule #1 OpenSpec: Layer 1 在 S1_TRIAGED 前确认 issue 是否有对应 Spec
- Rule #2 十步循环不跳过 Phase A: Layer 2 执行完整十步循环
- Rule #3 文档同步: Layer 2 在 S5_REVIEWING 前强制 arch-update
- Rule #4-6: Layer 2 按 v1.x 语义执行
- Rule #7-9: Layer 2 内 Claude Code 实例遵守相同 secret / pre-merge / handoff 规则

### 人类参与点

v2.0 保留 **1 个** 人类参与点 (AD10 human gate): S7_AWAITING_MERGE, 产品负责人通过 Feishu 签字 merge PR。其他阶段完全自主。

### 详细入口

- 架构决策: [aria-orchestrator/docs/architecture-decisions.md](aria-orchestrator/docs/architecture-decisions.md)
- Layer 边界契约: [aria-orchestrator/docs/layer-boundary-contract.md](aria-orchestrator/docs/layer-boundary-contract.md)
- PRD v2.0: [docs/requirements/prd-aria-v2.md](docs/requirements/prd-aria-v2.md)
- 系统架构: [docs/architecture/system-architecture.md](docs/architecture/system-architecture.md)
- M0 Spec (历史): [openspec/archive/2026-04-17-aria-2.0-m0-prerequisite/proposal.md](openspec/archive/2026-04-17-aria-2.0-m0-prerequisite/proposal.md)

---

## 项目状态

```
当前阶段: v2.0 M6 执行中 (M1-M5 shipped)
成熟度:   0.9 (M1-M5 端到端验证 + 多终端协调 + 跨 30+ Spec 实证 + AB benchmark 累积)
插件版本: v1.34.1 (aria-plugin, 34 user-facing + 7 internal Skills + 11 Agents + secret-guard
                  default + aria-doctor v1.2.0 + §C.2.4.5 submodule pointer regression gate
                  warn-only mode + Forgejo hosts parameterization + CI backend abstraction
                  (CIBackend ABC + AetherBackend full + GitHubActions stub) via ci_backends/;
                  v1.30.1 closed #125+#126 (dashboard parser+audit frontmatter), v1.30.2 closed
                  #57+#56+#67 (multi-terminal sandbox+RECOMMENDATION_RULES+phase-d latest.md),
                  v1.30.3 closed #131 (Windows GBK guard), v1.32.0 = 4 SKILL.md progressive-
                  disclosure restructure (avg -58% lines, all <500, 36-run AB verified),
                  v1.33.0 = aria-context-monitor #104 (context-monitor + token-telemetry skills
                  + statusLine relay, runtime-truth context occupancy), v1.34.0 = ai-native-
                  estimator #18 (Token-axis cycle workload estimation v1 + phase-d D.4 capture),
                  v1.34.1 closed #132 (secret-guard CRLF fail-closed Windows hotfix — jq|tr -d '\r');
                  v1.29.0 reserved for block-flip ship 2026-06-07 D+14)
主项目版本: v1.7.0
运行时版本: v2.0.0 (aria-orchestrator, M6 execution phase)
PRD v2.0: Approved (2026-04-11) — M0-M5 done; M6 active (4 sub-Specs Approved 2026-05-24~25);
          M6 ship 后 (M7+) aria-fleet 三层架构 (通用/workspace/instance) 待 brainstorm
          → 详见 `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` (D1-D6 Approved)
```

### User Story 编号分区

```
US-001~009: v1.x 已有 (done/in_progress/pending)
US-010~019: v1.x 新增 (Agent Team 质量 + 项目适配)
US-020~027: v2.0 (待起草)
```

---

**更新**: 2026-05-29 (插件 v1.33.0 ship — aria-context-monitor #104; 项目状态段同步)
**维护**: 10CG Lab
**主仓库**: https://github.com/10CG/Aria
**插件仓库**: https://github.com/10CG/aria-plugin
**规范仓库**: https://github.com/10CG/aria-standards
