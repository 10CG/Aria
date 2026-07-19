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

**CLAUDE.md 卫生** (Option A, 见 `standards/conventions/claude-md-hygiene.md`): 只放稳定内容; **不放** 版本 changelog (→ `aria/CHANGELOG.md` SOT) / session 进展流水 (→ `docs/handoff/`, Rule #9, 用 `/state-scanner` 查); 「项目状态」段 = live 覆写非 append log。enforcement: state-check `claude-md-changelog-free`。

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
├── Session handoff → standards/conventions/session-handoff.md (Rule #9, v1.21.0+; §1.3 周期vs会话收尾消歧 v1.50.0+)
├── 会话收尾 (对话维度)  → aria/skills/session-closer/ (leaf skill, 正交于十步循环 Phase D; "对话收尾")
├── Submodule pointer 卫生 → standards/conventions/submodule-pointer-hygiene.md (aria-plugin v1.49.0+ §C.2.4.5 mechanical gate companion, **block default** since v1.49.0; v1.28.0-v1.48.x warn-only)
├── Shell jq CRLF 卫生 → standards/conventions/shell-jq-crlf-hygiene.md (aria-plugin v1.36.0+ #132 follow-up; CR 处理决策表 + jq-crlf-guard + crlf-shim 测试框架)
├── 并发 Session 写入安全 → standards/conventions/concurrent-session-write-safety.md (aria-plugin v1.37.0+ #133; 并发安全写法主解药 + AI 记录硬证据自律 + 切口1/2 advisory; advisory-over-hardlock)
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
  - [ ] 主项目 root README.md Plugin Version badge (L8 shields + Project Status 段) 同步插件版本
        # badge 不在 aria/ 子模块 SOT 内, 每次 bump 易漏; 兜底 custom check m6-version-badge-match。
  - [ ] 主项目 root i18n README (README.{zh,ja,ko}.md) — **仅当 README.md 正文实质变更** 时重译 (#140 B 档: 纯 badge/patch 免重译)
        # 更新各文件顶部 <!-- translated-from: vX.Y.Z --> 标记; 兜底 custom check i18n-readme-translation-currency。

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

**规则 #9 要点:** session handoff 文档 (`docs/handoff/{YYYY-MM-DD}-{slug}.md`) 必须写在 `docs/handoff/` (canonical), 禁止写 `.aria/handoff/*.md`。`.aria/` 是机器状态 namespace, `docs/` 是人类/AI 可读 prose namespace; handoff 是 prose 范畴。5 层 defense-in-depth: L1 PreToolUse hook 阻断写入 + L2 scan.py collector 检测 misplaced + L3 state-scanner 推荐迁移 + L4 本规范 (Convention SOT) + L5 phase-d-closer D.3 **及 session-closer step4** template 硬编码输出路径。

**两种收尾 (session-closer-synthesis, 插件 v1.50.0+)**: handoff 由两个正交入口写出 —— **周期收尾** (`phase-d-closer`, cycle 单元, 十步循环 Phase D) vs **会话收尾** (`session-closer`, session 单元, leaf skill, owner 任意时刻调"对话收尾")。二者共享本规范 + 同一 handoff-write SOT (`handoff-mechanics.md`) 引用不复制, 工作单元不同不混淆。消歧矩阵见 `standards/conventions/session-handoff.md §1.3` (第三方 load-bearing)。

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

**更新** (`interactive-session-dedup-coordination`, 完成 TASK-024 集成 + advisory 改造后): 上文所述 Layer L (`phase1_gate`) 的 `run_gate()` 原为死代码 —— 母 spec 的 TASK-024 集成从未落地 (P3 deferred, run_gate 零生产调用点; 缺口记录于 aria-plugin `skills/state-scanner/references/layer-l-integration.md`)。经 DEC-20260704-002 接活为 **advisory 认领**: AI 编排层 (state-scanner 阶段 2 / Phase B-entry) 首次接线 `run_gate()`,详见该 Spec proposal.md。

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
当前阶段: v2.0 M6 执行中 (M1-M5 shipped; 成熟度 ~0.9 — 端到端验证 + 多终端协调 + 跨 30+ Spec + AB 累积)
  M6 sub-Specs: #1 cost + #3 docs 已归档; #2 e2e-resilience 代码侧完成 (未归档, 待 168h 跑); #4 release-closeout sequential 待
  ⚠️ 168h 自主跑 ≠ make-ready: pre-flight (2026-07-02) 证自主 E2E 从未闭环 (数字-id dispatch 100% S_FAIL)。三门未清:
    - Blocker 3 输入投递 (`aria-2.0-m6-dispatch-input-delivery`, A.3 30-task post_planning CONVERGED): **Phase B.2 实现完成 + pre-merge code-reviewed** (aria-orchestrator `feature/m6-dispatch-input-delivery`, 26/30 task 绿 / 1 Critical 修 / WIP 未 merge)。**卡 Phase C.2 合并**于 4 owner/infra 门: build(021) / deploy(镜像先) / egress(028) / E2E dogfood(029=AC-1, 受 **Blocker 4**)
    - Blocker 4 Luxeno 后端延迟 45-54s (owner/基建门, 非 mihomo)
    - 遥测 Spec (AC-6 评分依赖, 独立) — **Approved + Track-1 实施完成** (`aria-2.0-m6-cost-model-telemetry`, owner 批准 2026-07-09; DEC-20260709-001 v2 4-agent 设计审议 + post_spec 5-agent R1→R3 CONVERGED)。范围: Layer2 cost/model 遥测回报 + 容器模型接线统一 [smart-sonnet 清 + 单源 ANTHROPIC_DEFAULT_OPUS_MODEL + served-model 观测 (记 served 非 intended, echo 失效模式待 AC-10 活体)]。**Track-1 (Layer1 遥测管道 Phase 4-5) 动态工作流实施完成**: aria-orchestrator `feature/m6-cost-model-telemetry` @ `92acce5` (叠 input-delivery, migration 009 [5.1→5.2]; dispatch_telemetry 表 + marker 解析 fail-toward-warn + cost.json 评分; 979+196 tests 绿; code-reviewer PASS + silent-failure-hunter echo-caveat 修/0 Critical) —— **合并 gate input-delivery** (选项 A stacked, schema/migration 文件级重叠不可并行占号)。⚠️ 红旗: glm-5.2 cutover 对容器疑 inert (--model smart-sonnet 非 canonical alias 使 ANTHROPIC_DEFAULT_OPUS_MODEL 结构性 inert) 待 AC-10 活体验。Track-2 容器侧 gate input-delivery; Track-3 AC-10 gate Luxeno Blocker 4。**依赖链** (input-delivery ↔ 遥测 disjoint): 168h 跑 AC-6 cost 维度可评分须遥测 Spec 独立 ship — input-delivery ship 不代表对 AC-6 可评分
  M7 aria-fleet: 2 sub-Spec (fleet-aggregation + agent-lifecycle) Approved 2026-06-18; Phase B 受 D3 门 (M6 release-closeout ship 后)
  aria-plugin 方法论轨 (与 M6/M7 正交): `interactive-session-dedup-coordination` (DEC-20260704-002 防交互 session [双子星] 重复, 接活 Layer L 死代码 → advisory 认领 + 结构化 carry-id + 完成 TASK-024): **✅ SHIPPED v1.52.0 (2026-07-05)** — Phase B 全 19 impl 任务完成 (run_gate 死代码→advisory 接活 + CLI + carry-id schema + 机械 owner-container + telemetry 分区防伪 + 14d 新鲜度探针 + 可证伪 harness + dogfood); 双轮 code-grounded 对抗审计 R1(2C+8I)→R2 CONVERGED(0C); 关 aria-plugin #94 / 部分回应 #95; Phase D 归档 `openspec/archive/2026-07-05-interactive-session-dedup-coordination`
  aria-plugin 方法论轨 (与 M6/M7 正交): `archive-gate-runtime-reality` (DEC-20260704-003 归档 gate 硬化 #95「勾选完成≠运行现实」, 延伸 #134): **✅ SHIPPED v1.53.0 (2026-07-05)** — C 分级证据闸 (block 高置信死代码=符号有 Py 定义但生产零语义引用 / warn 模糊声称+unverified_claims frontmatter / fail-toward-warn 默认) + D auto-issue (单一 owner 幂等 headless) + tri-state gate_result(complete 正交); post_spec R1→R5 (R1 否证初版 Gate B checkbox 交叉核对→owner B→C) + post_planning R1→R4 双 CONVERGED + pre-merge review (silent-failure 1C/2I 修); 60 unit+9 integration, 116 归档 sweep 仅死代码 block (SC 零影响); dogfood: 自身 gate 跑自身 spec verdict=warn/0-block; 关 aria-plugin #95; Phase D 归档 `openspec/archive/2026-07-05-aria-archive-gate-runtime-reality`。**与 DEC-002 disjoint 并发 ship** (双子星 v1.52.0 / 本 v1.53.0, rebase 化解版本撞车; DEC-002 接活 phase1_gate 恰使 #95 golden 反例不再 block — gate 追踪运行现实实证)
  aria-plugin 方法论轨 (与 M6/M7 正交): `runtime-probe-archive-gate-integration` (DEC-20260705-001 归档 gate 硬化 #95 follow-up A「勾选完成≠运行现实」的运行时维度): **✅ SHIPPED v1.54.0 (2026-07-09)** — 把 DEC-002 单一用途动态探针 (coordination_probe) 泛化成归档门声明式可选动态子检查: spec 在 proposal.md frontmatter 声明 `runtime_probe` (partition/symbol/max_age_days/enabled_when), 归档门见声明才跑并把「最近真被调用过吗」按 fail-toward-warn 折进裁决 (probe-warn 双写 warnings[]+unverified_claims[] 复用 #95 双下游 D auto-issue), 无声明 spec 零影响 (SC-1: 124 spec 全语料 diff=0); coordination_probe 薄壳化 (四态逐字节 + read-failure 假绿修复 exit 0→1); merge-append 同名键裁决 (结果字段追加进作者声明 mapping 不删改)。post_spec R4 + post_planning R3 + pre-merge 4 视角 R1(1C/7I/13M)→R2→R3 零新 finding CONVERGED; python 968/E2E 67/CLI 10; dogfood phase1_gate 真调 + 真分区 probe=pass; 关 aria-plugin #95 (follow-up A 收尾); Phase D 归档 `openspec/archive/2026-07-09-runtime-probe-archive-gate-integration`
  aria-plugin 方法论轨 (与 M6/M7 正交): `coordination-claim-lifecycle-and-overlap` (2026-07-11 双子星撞车实证的协调机制 3 缺陷: a 认领非强制 / b track-id 纯字符串 / c claim 从不释放): **✅ SHIPPED v1.56.0 (2026-07-11)** — Part C claim 释放闭环 (release_gate CLI 按 track+container 定位 + apply_tree_edits CAS 批量原语 + GC 真写入 + sweep SWEEP_TTL=24h + phase-d-closer D.2b 接线 + 一次性清理真 ref) + Part A1 认领强制 (coordination.enabled 默认 false→true opt-out ⚠️行为变更 + phase-b B.0/branch-manager REQUIRE claim + doc lock-in) + Part B1 语义重叠 (claim schema linked_issue additive + phase1_gate --linked-issue + linked_issue_overlap advisory); pre-merge 对抗 review R1 1C (sweep 30min TTL 误杀并行活 session) + 5I 全修; 测试 968→1006 (含 pytest 裸函数假绿修复); aria PR#106 `504da89`; Phase D 归档 `openspec/archive/2026-07-11-coordination-claim-lifecycle-and-overlap`。**follow-up**: orchestrator 强制 bot claim (defect a Layer 2 维度) 待开 aria-orchestrator issue; heartbeat 生产接线待 follow-up
  aria-plugin 方法论轨 (与 M6/M7 正交): `agent-router-auto-project-agent-injection` (#153 发现 B「agent-creator 生成物 auto 路由从不消费」): **✅ SHIPPED v1.55.0 (2026-07-09)** — 项目级 capability 匹配接入 auto 主链: §CAP 评分成文 (显式传参/L1 词边界/L2 受约束 + off-tax 惰性 + precision 门拦 generalist) + 两段式决策 (Stage1 基线一致 + Stage2 R-a 序数直派/R-b 有序分支含单标签禁令与空基线分支) + 同名吸收得分归属 + 输出契约 additive (agent_source/decision_path/trace) + 缓存 per-file 语义; US-011 三锚点 errata + DEC-20260621-001 勘误; post_spec R1→R4 (152 findings, owner 接受) + post_planning R1→R4 CONVERGED (unanimous 5/5) + 16 AC × 双跑 48 runner structural fixture 全绿 (回炉 1 轮修真歧义 — 双跑分叉实锤空基线分支缺失); 版本两度让位并行 ship (v1.54.0 runtime-probe 抢注, 5 SOT 撞车 rebase 机械解 ×2 + C.2.4.5 指针 gate 拦到 standards 真回归); 关 #153 (发现 A 归 M7 #128); Phase D 归档 `openspec/archive/2026-07-09-agent-router-auto-project-agent-injection`
  aria-plugin 方法论轨 (与 M6/M7 正交): `state-scanner-issue-cache-freshness-assertion` (false-parity 三 spec 之 C, 先行; aria-plugin #110 issue-cache-freshness check 结构性恒红): **✅ SHIPPED v1.57.0 (2026-07-16)** — snapshot 顶层加 `generated_at` (additive schema 1.0) + check 从跨 scan 文件 mtime 恒红重定义为可复用探针 (lag-1 读上一份 snapshot issue-fetch 健康) + custom_checks skip 态 (`##SKIP##` stdout marker + exit 0, 非 exit 2 避与 grep/diff/argparse 撞码) + skipped 计数三分支; **B.2 Phase B review-driven A1 精修**: 原 Δ-only 机制对真实数据近乎无用 (collector 1×TTL 门控 STALE 不可达 + fetch 失败绿真空) → 主信号改 issue-fetch 健康 (fetched_at 缺失=持续破坏→STALE 暴露; 保 AC-2 正交 瞬时 fetch_error+新鲜→OK), Δ 降次要守卫; 双动态工作流 (蓝图 backend-architect+qa-engineer → 核心主 loop 亲验 → 对抗 review 3-agent → post_impl 确认 review, fix_introduced_regression: no) + 1031 real-green + 真实 dogfood 全生命周期正确; aria `a9e8652` / 主仓 gitlink `36050cc`; 关 aria-plugin #110; Phase D 归档待。**同 session sign-off**: false-parity 三 spec (主 stale-refs v10 / C issue-cache v6 / B stderr-leak v5) 全 Approved (Spec B R6→R7→R8 抓 2 连 fix-introduced Critical → option B 重框 best-effort); 落地序 C→B→主, C 先行 ship, B/主 待实现
  aria-plugin 方法论轨 (与 M6/M7 正交): `state-scanner-snapshot-stderr-secret-leak` (false-parity 三 spec 之 B; Rule#7: git 命令 stderr 直传 snapshot 泄露凭据 URL): **✅ SHIPPED v1.58.0 (2026-07-16)** — 类型化错误通道: `_common.py` GitErrorClass (frozen, 无 stderr 字段, 结构级不可承载 secret) + classify_git_error(rc,stderr,cmd) 消费 stderr 取 bounded label 即丢弃 (label∈{network,auth_403,non_ff,git_missing,other}); 5 直传 callsite (git×2/sync×3) + 4 助手内部自分类 (handoff_multibranch×3 benign-skip 保全/handoff_worktrees×1) + coordination_fetch._classify_error 委托 (措辞逐字节保 test_p1_layer_h, 无第三份); 次级泄露收口 (_run timeout/FileNotFound 分支 argv 含凭据 URL 经通道丢弃); §3b signal 扩充 (network+4 / publickey; R6-m1 守卫裸本地权限错不误标) + AC-2 best-effort lint (AST 追 _run 第三返回值, option B: 结构保证=类型不可承载, routing=lint+review); **B.2 review-driven fold**: silent-failure 抓 lint denylist 洞 (form B return-plain 助手可达) → 加 Return denylist + docstring 诚实化; code-reviewer PASS + silent-failure PASS-with-fixes (fix_introduced_regression: no); 双动态工作流 + 1047 real-green; aria `cae92e8` / 主仓 gitlink `de9abae`; 关 aria-plugin #92 (secret-scan 反馈闭环相关) 部分; Phase D 归档待。**三 spec 落地序 C→B→主: C(v1.57.0)+B(v1.58.0) 已 ship; 主 stale-refs v10 待实现 (B 已先于其 F3′)**
  aria-plugin 方法论轨 (与 M6/M7 正交): `state-scanner-stale-refs-false-parity` (false-parity 三 spec 之主; sync_status/overall_parity 陈旧 remote-tracking ref 下撒谎报 parity=equal): **Phase 0 (prereq) SHIPPED v1.59.0 (2026-07-17)** — 零行为变更基础独立先行 ship 于 Level-3 core: F5′ resolve_enforced_remotes 纯函数 (INERT, enforced_remotes:[] → 自动发现全部远程陷阱守卫, 零调用点直到 Phase 1 F4′) + sync_freshness.* config 键 (DEFAULTS) + D16 predicate-domain-table.md 表骨架 + 8 测试 (全量 1072 绿); F5′ INERT 确认 → Rule #6 benchmark N/A; aria `a537e7d` / 主仓 gitlink `e54a891`。**Phase 1-3 核心 SHIPPED v1.60.0 (2026-07-19)** — 四段式核心全实施: Phase 1 (F1′ 双轴双角色谓词 evidence_grade∈{fresh,stale_unverified,expired} + F2′ 退役 mtime + F3′ remote_refresh collector [Phase 0.5 per-host 并行 fetch --prune + deadline 三态 + coordination_fetch 派生 shim] + F4′ overall_parity 四子句裁决 [陈旧 equal 非正证据 + _blocking_unknown 严格补集 fail-CLOSED] + F6′ + 9.7 offline 冻结) + Phase 2A (F10″ gitlink_integrity[] 九分支域, R5-C-A 事故解药, orphaned⇒blocking, ok/orphaned 均过豁免资格门) + Phase 2B (F9′ sync.py 消费 evidence_grade, US-008 护栏逐字节未动) + Phase 3 (golden 重采 + 12.10 六通道 + schema doc)。⚠️行为变更 13.6: overall_parity 事故形态 true→false; Fetch1 --prune。四动态工作流 (蓝图→实施→3-agent 对抗 review) + 主 loop 亲验 (抓修 gitlink ok 路径 BLOCKER false-green: 陈旧 refs 上的 ok 未过新鲜度门); 全套件 1219 绿 + 真实 dogfood 验证 (gitlink 5 ok/1 no_matching 诚实, evidence_grade join 通, overall_parity 诚实判 behind→False)。aria `e162f7b` / 主仓 gitlink `d319d6f`。**spec 保持 active (不归档, 十步循环 Phase D 未走 D.2)**: 79/119 task done, k_eff observed_rotation DEFERRED (fail-CLOSED, k_eff=k_min 冷启动), **29 TODO** (F5′ enforced/read_only 接进 _overall_parity 6.1/6.2 / 非交互 git 3.4 / tracks 同分支不可达 2.12 AC-5 / 命名空间 split-brain 1.6 / gitlink drift 文案 13.3·9.2)。**follow-up**: Aria #165 (镜像漏推, 方案 B 复用 F10″ 谓词)。详见 docs/handoff/
  aria-plugin 方法论轨 (与 M6/M7 正交): `state-scanner-openspec-collector-false-green` (Aria #166 三缺陷: OpenSpec 维度沉默假绿, 消费方 Aether 中招 8 周): **✅ SHIPPED v1.61.0 (2026-07-19)** — 缺陷1 `collectors/openspec.py` changes/ 缺失 early-return 静默全零且连带不扫正交 archive/ (归档完最后一个 spec → git 丢弃空目录 → 与「没用 OpenSpec」输出等价) → 移 early-return (loop 改 guarded iterable 防 FileNotFoundError) + archive/ 始终扫 + 高置信 `layout_drift` soft_error (archive 非空或裸/错位 proposal 才发, 冷启动与无 openspec/ 静默) + configured 保 False 由 soft_error 消歧 (新组合 configured=False ∧ archive.total>0); 缺陷2 `lib/spec_complete.py::gate_result` 对 detailed-tasks.yaml-only spec 早退致归档安全网失明 (verdict=pass/d_payload=None, headless 一个 tracker 不建) → 追 unverified_claims 条目(含 symbols) + verdict=warn + 构造非 None d_payload, 点亮 warn_overlay frontmatter + D auto-issue 两条 #95 既有通道 (零改 openspec-archive, 遵循 `_fold_runtime_probe` 主线双写先例); 缺陷3 `_status.py` done 家族加 `completed` (#101 词边界过度收紧致 Completed→unknown + design_deferred 噪音; `\bcompleted\b` 不匹配 uncompleted, #101 保持闭合)。post_spec convergence **R1→R4 CONVERGED** (R1 3-agent 收敛 Critical: 缺陷2 位置钉错——继承 issue 自身 mis-citation, 真实生产者是 gate_result 非 collector 展示字段; R2 3-agent 收敛 Major: 「仅 warn 即经 Step7 surface」被源码证伪, D-tracker 门控 d_payload!=null 不看 verdict; R3 rationale-only Major 先例定性弄反; R4 零新 finding); pre-merge code-reviewer PASS(0C/0I) + silent-failure-hunter 抓 **1 MEDIUM fix-introduced regression** (stray 检测器 `except OSError: pass` 系本 change 立意要杀的同款静默吞咽) → 改发 `openspec_scan_failed` + archive iterdir 对称 fail-soft + 2 OSError 测试。TDD 三缺陷各 baseline-failing RED 先行 + 3 对称负控; 13 新测试; 全量 **1232 绿**; dogfood scan.py exit=10 + archive.total 正确。**版本让位** v1.60.0 给并发 ship 的主 spec, rebase 无冲突 (改动区域不相交)。aria `55ab21d` (PR #112) / 主仓 gitlink `d7b2a4f`。**follow-up**: gate_result 完整解析 detailed-tasks.yaml (精确 per-spec verdict 取代 blanket unverified + 顺带修 carry_forward_inventory 展示假绿)。Phase D 归档 `openspec/archive/2026-07-19-state-scanner-openspec-collector-false-green` (verdict=warn 经 #95 warn_overlay 记入 frontmatter: 归档门 artifact 分类器路径正则硬编码只认 ab-results|ab-suite, 非-AB dogfood 声称结构性恒 warn — 真实执行记录已落盘 dogfood-evidence.md)
  → 详细进展见 docs/handoff/ (latest, Rule #9 canonical) + 各 Spec proposal.md + Aria #147

版本: 插件 aria-plugin v1.61.0 (35 user-facing + 7 internal Skills, 11 Agents) | 主项目 v1.7.3 | 运行时 aria-orchestrator v2.0.0 (`f3848b2`)
  → 完整版本变更史见 aria/CHANGELOG.md (SOT); 运行时 Layer 2 主力 LLM = glm-5.2 via Luxeno, Layer 1 = glm-4.5-air
```

### User Story 编号分区

```
US-001~009: v1.x 已有 (done/in_progress/pending)
US-010~019: v1.x 新增 (Agent Team 质量 + 项目适配)
US-020~027: v2.0 (待起草)
```

---

> **进展查询**: 当前状态见上「项目状态」段 (live 覆写) | session 进展史 → `docs/handoff/` (Rule #9 canonical, 用 `/state-scanner` 查) | 版本变更史 → `aria/CHANGELOG.md` (SOT)
> **CLAUDE.md 不保留 changelog / session 流水** (规矩: `standards/conventions/claude-md-hygiene.md`, Option A 彻底移交 — 时效内容归各自 canonical 家, CLAUDE.md 只放稳定「如何理解项目」)

**维护**: 10CG Lab
**主仓库**: https://github.com/10CG/Aria
**插件仓库**: https://github.com/10CG/aria-plugin
**规范仓库**: https://github.com/10CG/aria-standards
