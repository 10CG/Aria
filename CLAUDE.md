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
  - [ ] 主项目 root README.md Plugin Version badge (L8 shields badge + Project Status 段) 同步插件版本
        # 根因记录: root README badge 是 plugin 版本的派生显示, 但不在 aria/ 子模块 SOT 内,
        # 每次 plugin bump 易漏 → 连续两次 ship (v1.44→45, v1.45→46) 都滞后一版。
        # 自动兜底: custom check m6-version-badge-match (.aria/state-checks.yaml) 每次 scan 检出 DRIFT。
  - [ ] 主项目 root i18n README (README.{zh,ja,ko}.md) — 仅当本次发版有 README.md **正文实质变更** 时同步:
        # 以 README.md (英文 SOT) 为源重译滞后语种 + 更新各文件顶部 <!-- translated-from: vX.Y.Z --> 标记。
        # 策略 (Issue #140, aria-i18n-readme-full-resync B 档): full-translation 维护; 纯 badge/patch 无需重译
        # (每 patch 重译正是滞后根因)。advisory-over-hardlock。
        # 自动兜底: custom check i18n-readme-translation-currency 比对 translated-from 标记 vs plugin 版本,
        # 检出正文滞后 (非仅 badge — #140 核心: badge current 但正文旧更误导)。

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
当前阶段: v2.0 M6 执行中 (M1-M5 shipped; M6 Spec #1+#3 archived, **Spec #2 e2e-resilience 代码侧完成 2026-06-02**; **168h 运营跑 now make-ready (2026-06-30) — #147 Layer1 runtime 降级全部修复**[B1 Luxeno 早已修/B2 Feishu WS 重启复连/B3 stale 重启重载/B4-code issue_type_hint PR #28[audit 2 轮收敛]/B5 scan.sh PR #27/节点 fetch 凭据=只读 deploy key/#28 部署 light-1/M1 handoff 放置[prod tick 验证 "not found" 消失]/镜像确认/labels 建好], **只剩 owner 168h 运营仪式 (pre-flight→Day-1 anchor→B4-label 造 aria-auto issue→每日 probe→corpus+评分→AC-5)**; Spec #4 sequential 待)
成熟度:   0.9 (M1-M5 端到端验证 + 多终端协调 + 跨 30+ Spec 实证 + AB benchmark 累积)
插件版本: v1.50.1 (aria-plugin, 35 user-facing + 7 internal Skills + 11 Agents + secret-guard
                  default + aria-doctor v1.2.0 + §C.2.4.5 submodule pointer regression gate
                  **block default (v1.49.0+ warn→block flip)** + Forgejo hosts parameterization + CI backend abstraction;
                  v1.50.0 = session-closer-synthesis [DEC-20260625-001, supersedes 搁浅的 session-closeout-internalization
                  复用 ~70-80% 实现]: 新 user-facing **leaf skill** `session-closer` — 会话维度收尾仪式, 与十步循环 Phase D
                  **正交平级**。AI 对话内省优先 (step1 未完成线程 + step2 待固化经验, 结构标记 `[候选 memory]`/`[未写下经验]`
                  AC-5b) + 机械 autofill 交叉核验补漏 (snapshot 有但 AI 没提 → flag) + 按**共享既有** handoff-mechanics.md
                  写 docs/handoff/ (引用不复制, 无第二份 ref) + **leaf 终结** (检出未归档 cycle 仅 advisory 提议, 不调
                  phase-a/b/c/d)。**trigger 消歧根治**: phase-d-closer description 中度 rebind (删「写 session handoff」+裸
                  「收尾」, rebind cycle-explicit + 负向消歧; D.1/D.2/D.3 action 零 diff) + session-closer 强绑会话词 +
                  standards §1.3 周期vs会话收尾消歧矩阵 (第三方 load-bearing: description + standards, 第三方不加载 CLAUDE.md;
                  1.1.0→1.2.0)。3 脚本 (handoff_autofill adapter 重建 + consistency_check + closeout_trigger) + 49 单测 +
                  真 snapshot 集成测试 (堵手造 fixture 假绿)。phase-b/c context-monitor step 接 closeout_trigger (喂
                  token_telemetry 输出非 relay cache)。**Phase A**: brainstorm 5 决策 → DEC → proposal/tasks → **post_spec
                  R1 REVISE×3** (2 Critical: 既有 handoff-mechanics.md 复用非新建 [起草未 recon] / collector 字段漂移
                  [active_changes→changes, cycle_number→current_cycle, in_progress 不存在标 fixture-only]; 4 Major: §2.2.1
                  重写非照搬 / AC-8 机械化 / 消歧矩阵 / 路径重映射) → **Rev1 → R2 PASS×3 unanimous** (二次核实字段漂移事实
                  非 paper-fix)。**Phase B**: cherry-pick 重组 (路径 session-closeout→session-closer, grep 0 残留) + 字段修正
                  + leaf 重写。**code-review** Phase 1 PASS + Phase 2 I-1 (钩子喂 relay cache 无 source → trigger 生产恒不
                  fire silent → 改喂 token_telemetry) / I-2 (carry_forward 真形态 {count,samples} 产垃圾 → samples 展开) 假绿
                  全修 + 真形态/负向契约测试。**Rule #6**: deterministic 核心 49 单测 = structural substitute; 触发命中率
                  description 工程; capability AB **+13.3pp** (判别项 = step2 结构标记可机械验证, baseline 因场景显式接近 =
                  process skill in-repo 保守下界) owner sign-off (delta≤0 非硬门)。aria PR/merge `9a2d185` + standards
                  `350a7cf` + 主仓 gitlink; Spec 归档 `openspec/archive/2026-06-26-session-closer-synthesis`。Skills 41→42。
                  v1.49.0 = submodule-gate-block-flip #124 [PR #90 `f3b7ac5` 双远程]: C.2.4.5 submodule
                  pointer regression gate 默认 mode warn→block (parent aria-submodule-pointer-regression-gate
                  Two-phase rollout 执行单元)。Trigger B: 5 gate executions (all warn-PASS) + 4 clean
                  host-cron tripwire + FP 0% + owner risk-accept (透明披露 5 条聚 2 ship 事件 + index.lock
                  重试虚增, 严格独立=2)。§A 3 处 default flip (submodule_gate.sh:33 + SKILL.md:450 + config/
                  wording) + T-flip-12 测试 (unset MODE→block, 15 PASS); §F standards wording (`ddaf3d1`);
                  §B workflow cron 作废 (host-cron 已迁移)。backward-compat (warn/off/env override 保留)。
                  决策记录 .aria/decisions/2026-06-21-v1.49.0-block-flip.md; Spec 归档。block-flip 闭环
                  (D+14 DEFER → telemetry 修 → Trigger B flip)。主仓 v1.7.1。
                  v1.48.0 = agent-team-audit-project-agent-augmentation #145 [PR #89 `a922e5c` 双远程]:
                  agent-team-audit 选择 step 3 拆 3a 固定基线 / 3b 项目级 capabilities 增补 —
                  `.aria/agents/` 中 capabilities 命中检查点"增补白名单"(pre_merge/post_implementation:
                  security-audit, performance-optimization; post_spec 空, 锚定 capabilities-taxonomy.yaml)
                  的项目专属 audit agent 加入审计批次 (复用 agent-router `.aria/agents/` 发现范式; 冷路径
                  直读 frontmatter); **判据 = 专有标签阈值非 baseline 减法** (code-reviewer 已带 security-audit
                  → 减法会盖住项目 security-auditor 恰打不中 reporter 用例 → 显式白名单解耦); augment-only
                  (基线永远跑+项目 agent 纯加法); 增补 agent 受 max_parallel_agents 节流但不丢弃; 降级纯基线
                  零回归 (空/无命中/缺字段skip/空list合法)。matrix 新增白名单列+step 3b 算法; SKILL.md 触发点表/
                  输出分母 (=基线+增补); audit-points 各 agents 字段注记 (mid_post_spec 标注不在增补范围)。**与 M7
                  agent-lifecycle 正交** (M7=物化到 .claude/agents/ 原生加载侧; 本=audit 消费侧; OOS: agent-creator→
                  .claude/agents/ 让给 M7 / override / 扩 taxonomy / 改 agent-router / experiment 转正)。experimental
                  skill (默认关), 能力随 experiment 转正才默认可用。Rule #6 = structural fixture (5 文件) + AC-5 dogfood
                  (Aria 无 .aria/agents/ → 纯基线零回归)。post_spec R1 REVISE 7 findings → R2 CONVERGED (unanimous
                  PASS); code-review Phase 1 PASS + Phase 2 I-1/I-2/M-1/M-2 全收。agent-team-audit skill 1.0.0→1.1.0。
                  源自本日 #145 re-triage (`next-cycle`); 等待期填空与 M6/M7 主线解耦。Skills 不变 (34+7=41);
                  v1.47.0 = issue-sweep release train [4 cycle / 6 issue, PR #88 `281388d` 双远程]:
                  (A) secret-guard 扩 exfil 覆盖 #69 [Aether dogfood 5 FN + 6 探针实测 v1.46.5 仍漏 →
                  RED-first regex 254/254 + 2-lens 对抗 review 修真 FP/bypass]; (B) audit 数据可用性 #54 +
                  框架约定 #95 检查项 [verdict-load-bearing] + phase-b 可选 build gate [tri-state];
                  (C) mid_post_spec 条件触发检查点 #79 [Phase B spec 漂移 single-round; 补齐 4 处
                  engine-internal 契约含 pre-merge gate 排除]; (D) tdd-enforcer security_commit_separation
                  #32 [安全代码 RED/GREEN commit 分离, = level_3_strict 改名, commit-msg hook];
                  每 cycle 独立 agent-team 对抗 review, Rule #6 = deterministic structural +
                  dogfood-by-construction, 4 OpenSpec 归档 2026-06-19, Skills 不变 41;
                  (CIBackend ABC + AetherBackend full + GitHubActions stub) via ci_backends/;
                  v1.30.1 closed #125+#126 (dashboard parser+audit frontmatter), v1.30.2 closed
                  #57+#56+#67 (multi-terminal sandbox+RECOMMENDATION_RULES+phase-d latest.md),
                  v1.30.3 closed #131 (Windows GBK guard), v1.32.0 = 4 SKILL.md progressive-
                  disclosure restructure (avg -58% lines, all <500, 36-run AB verified),
                  v1.33.0 = aria-context-monitor #104 (context-monitor + token-telemetry skills
                  + statusLine relay, runtime-truth context occupancy), v1.34.0 = ai-native-
                  estimator #18 (Token-axis cycle workload estimation v1 + phase-d D.4 capture),
                  v1.34.1 closed #132 (secret-guard CRLF fail-closed Windows hotfix — jq|tr -d '\r'),
                  v1.35.0 = emergency-hotfix-and-audit-file-scope #58 (emergency_hotfix 规则 priority
                  1.85 + phase-b Prod-Validated commit trailer gate + audit-engine file-scope 二次过滤
                  降级 convergence; standards git-commit.md §6.4 trailer), v1.36.0 = shell-jq-crlf-
                  hardening #132 follow-up (系统性加固全 plugin shell jq 消费点对 Windows CRLF +
                  crlf-shim 测试框架 + jq-crlf-guard + standards shell-jq-crlf-hygiene convention),
                  v1.37.0 = concurrent-session-upm-safety #133 (并发写安全 convention 主解药 +
                  tracks_multibranch.collision 持久化 lib/collision.py + 切口2 rule 1.54
                  concurrent_churn_detected + 切口1 phase-d-closer fetch_gate; advisory-over-hardlock;
                  standards concurrent-session-write-safety convention; 27 tests);
                  v1.38.0 = state-scanner-output-cap-hardening #71+#72 (TG-B handoff_multibranch
                  MAX_BRANCHES_SCANNED 三层可配置 resolver [env>config>default 20, int 域 fail-soft,
                  上界 500 warn-only per OQ3] + TG-A SKILL.md 输出格式补 10 区块字段骨架防 v1.32.0
                  字段层漂移 + sync-check 测试; 45 新测 deterministic/structural Rule #6 substitute);
                  v1.29.0 slot 跳过 (block-flip 实际 ship 为 v1.49.0 2026-06-21, 见下 v1.49.0 clause);
                  v1.42.0 = archive-completeness-gate #134 [禁止归档仅-Phase-A-收敛 spec: lib/spec_complete.py
                  单一可执行 complete SOT (archive-ready={done} only) + openspec-archive Step1 gate
                  (--archive-design-only 逃生舱 + frontmatter archive_type 标记) + phase-d-closer D.2 三路堵
                  Level 2 旁路 + state-scanner design_deferred[] surface (fresh-approved 合法在飞,
                  complement-invariant 4 桶) + standards 废弃 Phase-A-converged 即归档惯例; DEC-20260609-001]];
                  v1.43.0 = handoff-frontmatter-enforcement #137 [frontmatter content enforcement 两层:
                  E1 phase-d-closer D.3 写后自校验 + E2 scanner handoff_frontmatter_missing soft warning
                  (resolved latest 双路径) + standards §2.3.7; 注入机制 v1.22.x+ 已存在, 修的是 enforcement]];
                  v1.44.0 = audit-drift-guard #17 [audit-engine 多轮审计 Drift Guard 原始目的锚定:
                  Step 0 anchor 固化 + Step 5 独立 drift-checker + 三档处置 (可配 0.2/0.5) +
                  REFOCUS_ROUND 耗配额 + DRIFT_TERMINATED 终局态 → FAIL drift override;
                  challenge 默认开; 契约 C-1 config drift_guard / C-2 report schema drift_metrics;
                  dogfood 机制首跑产出非空 drift_metrics; DEC-20260611-001]);
                  v1.45.0 = cross-worktree-handoff-discovery #139 [Phase 1.15b handoff_worktrees
                  collector: git worktree list --porcelain 枚举 + 复用 handoff.py 抽出 _resolve_latest
                  helper (单份 H5 pointer→mtime, collect_handoff 逐字段零回归) + epoch 域 frontmatter
                  updated-at 仲裁全局最新 (tie current-wins / other path 字典序) → 落他树阶段 2 advisory
                  EnterWorktree; 纯机械发现零 frontmatter schema 变更 (加字段破 #137 E1 head-8 窗口);
                  resolve_max_worktrees_scanned resolver 镜像 #71; 52 测试 739→791 零回归 + 三重 dogfood
                  (真树 no-op + sandbox + 端到端 scan.py 多 worktree); DEC-20260611-002];
                  v1.46.0 = state-scanner-coordination-fetch-resilience #141 软错误① + aria-plugin #75
                  [coordination_fetch 拆两条 fetch 修原子 fetch rc=128: collectors/coordination_fetch.py 把
                  +refs/heads/* 与 refs/aria/coordination 合成单条原子 git fetch, 远端无 coord ref 项目 (多数
                  非多终端协调) 整条 rc=128 失败 + 分支头不刷新 + 每扫描 spurious coordination_fetch_failed (exit 10);
                  拆 Fetch1 分支头载重先跑 + Fetch2 协调 ref 仅 Fetch1 后 (benign 三重 AND 闸 rc==128 +
                  couldn't-find-remote-ref + refs/aria/coordination 先于 _classify_error → 缺失不报错 success 保持;
                  Fetch1 失败短路); additive coordination_ref_present 三态 cache 持久化不进 normalize DROP_KEYS;
                  12 新测 803 全绿 (1 已知 timing flake 无关) + dogfood no-coord sandbox 真 git 修复确证; schema SOT
                  新建 coordination_fetch section; post_spec R1 4/5 REVISE 8M → R2 5/5 PASS; code-review code-reviewer
                  PASS + silent-failure-hunter → absent-vs-hidden ref 歧义 documented-limitation + 3 follow-up
                  (F3 ls-remote / F4 LC_ALL=C / F5 track_board); DEC triage partial-repro #issuecomment-12658];
                  v1.46.1 = state-scanner-git-stderr-locale-hardening #143 (F4) + #142 (F3 wont-fix)
                  [_run 注入 LC_ALL=C 强制 git 英文诊断输出, 修多 collector (coordination_fetch benign 闸 +
                  _classify_error / multi_remote / issue_scan) 在非英文 git locale 下英文 stderr 匹配失灵
                  (benign false-negative + 误分类); 与 #61 encoding=utf-8 正交 (LC_ALL 管诊断文本 / encoding 管
                  字节解码, commit/ref/path 字节直通 md5 一致实测); LANG=C 冗余省。#142 wont-fix: ls-remote
                  --exit-code 对 absent 与 hidden 同 rc=2 git 协议不可解 (标题目标不可达), decline ls-remote
                  (LC_ALL=C 后仅边际 race-catch), auth-masked silent 保持 documented-limitation。env 断言测试
                  (mock subprocess.run host-locale-agnostic 闭合 C-locale CI 循环论证) + CJK 直通真测 (实际
                  git log --oneline); 805 全绿 + 138 git-解析 collector 测试 under LC_ALL=C 零回归; post_spec
                  R1 2/4 REVISE 3 major → R2 4/4 PASS; code-review PASS];
                  v1.46.2 = track-board-coordination-stale-bar #144 (F5, 源自 #141 silent-failure-hunter #5)
                  [render_track_board 原只读 coordination_fetch.degraded/cached; Fetch1 ok + Fetch2 非 benign
                  失败 (success=True/degraded=False + coordination_ref_fetch_failed soft_error 进 errors[]/exit 10)
                  时多终端看板全绿无提示 (half-silent)。加非阻塞黄条 "⚠ 协调 ref 未取到 ... 队友协调数据可能陈旧",
                  gate 在 errors[] 的 coordination_ref_fetch_failed (唯一无误报判别器 — 仅 Fetch2 非 benign emit;
                  code-review 验证 coordination_ref_present is None 单独会误报 Fetch-1-fail-no-cache); degraded 时
                  红条优先。Level 1 (render-only 单函数 graceful, 无 OpenSpec); TestCaseF 6 测试 810 全绿; code-review
                  PASS (errors[] 耦合经验证优于备选 + M-1 fail-soft 加固)];
                  v1.46.3 = coordination-ref-lib-run-parity (F1, 源自 #141 silent-failure-hunter M2)
                  [lib/coordination_ref.py 有自己的 _run (独立于 collectors/_common._run), #61 (UTF-8
                  crash-safe) + #143 (LC_ALL=C) 加固只改了 collector 那个。本地 _run 加 encoding=utf-8/
                  errors=replace (#61: C-locale + 非 ASCII claim 内容严格解码崩溃) + env {**environ,
                  **(extra_env or {}), LC_ALL:C} (LC_ALL 末位非覆盖, GIT_INDEX_FILE 仍生效); 只加 #61/#143,
                  timeout/None-guard 留 F2。fetch_coordination_ref 加 benign-absent 三重 AND 闸 (rc==128 +
                  couldn't-find-remote-ref + REF_NAME 镜像 collector 用 lib 自己常量不 import 防 layering) →
                  absent ref=success=True → health_check 不误标 partial_fetch。可达性低 (opt-in phase1_gate
                  默认关) 但真实潜在崩溃/locale 隐患。TG-C 7 lib-直测 (非 mock wholesale: env 断言 host-locale-
                  agnostic + extra_env 共存 + benign/converse/wrong-ref/auth + crash-safe 真 subprocess); 97
                  coordination 测试全过 + 818 全绿。post_spec R1 2/3 REVISE 3 major (测试落点太松) → R2 3/3 PASS;
                  code-review PASS];
                  v1.46.4 = coordination-ref lib _run timeout ceiling (F2-minimal, #141 follow-up)
                  [lib/coordination_ref.py::_run 无 timeout → phase1_gate coordination git op 网络卡住无限挂起。
                  加 timeout=30 (tiny ref + 亚秒级本地 op 极宽松不误失败) + TimeoutExpired→124 (fetch 分类 network)
                  + #131 None-guard。故意跳过 rc 对齐 (FileNotFoundError 保 -1; lib callers 判 rc<0 改 127 会破坏)。
                  dedup 两 _run + 分支头耦合解耦 defer (低价值/风险 opt-in-gated)。Level 1; TestRunTimeout 3 测试
                  + 88 coordination 测试全过 + 821 全绿; code-review PASS (全 11 lib _run callers 优雅处理 rc=124)];
                  v1.46.5 = submodule-gate-telemetry-timeout (R-fix-1 follow-up, block-flip 重启诊断 owner Path A)
                  [telemetry hook WARN 跑 gate 记录执行, 但 log_execution 在 per-submodule fetch 后; aria/aria-
                  orchestrator origin=forgejo (CF-Access) fetch hang 超 hook timeout 15 → gate 杀于记录前 → 0
                  executions (block-flip D+14 Trigger C 根因持续, 2026-06-14 复现 exit 124)。修: WARN/telemetry 跳过
                  per-sub fetch (O(N)→O(1) 本地 refs WARN advisory) + bounded_fetch (timeout 包裹防无限 hang) +
                  hook wrap 15→25 + hooks.json 20→30; block/merge-flow fetch 不变 (authoritative)。WARN 完成 9s +
                  记录真实 PASS execution; gate 14 PASS (新 scenario_11 WARN origin 不可达仍完成+记录) / hook 7 PASS
                  / state-scanner 821 OK; future ships gitlink bump 真累积 executions → block-flip Trigger B ≥3
                  minimum-observation guard (tripwire 已绿 2 clean host-cron)。aria PR #87 merge `28c1a4d` 双远程])
主项目版本: v1.7.2
运行时版本: v2.0.0 (aria-orchestrator master `f3848b2`, M6 execution phase;
          Spec #2 e2e-resilience TG-A+TG-B+TG-C 模板代码侧 100% ship via PR #23+#24;
          AC-6 false-green 修复 PR #26 [#146, audit 3 轮收敛]; #147 runtime remediation:
          scan.sh PR #27 + issue_type_hint PR #28 [audit 2 轮收敛] merged a7afaaa, 已部署 light-1;
          **Layer 2 主力 LLM 2026-07-01 glm-5.1→glm-5.2** [SilkNode #830 确认上线可路由 (Anthropic 端点直通,
          z.ai+bigmodel 双活, 同价); 改 light-1 nomad var `ANTHROPIC_DEFAULT_OPUS_MODEL` 单字段 (CAS check-index,
          8 keys/3 secret 全保); Layer 1 保持 glm-4.5-air; 待 pre-flight `result.json` 端到端验证; runbook
          `aria-orchestrator/docs/glm-5.2-cutover-runbook.md`])
PRD v2.0: Approved (2026-04-11) — M0-M5 done; M6 active (4 sub-Specs Approved 2026-05-24~25):
          #1 cost-acceptance + #3 docs archived 2026-05-28; **#2 e2e-resilience 代码侧完成
          2026-06-02** (TG-A runtime obs gate + TG-B crash-recovery 覆盖矩阵 [Phase A rework #138:
          spec mock 虚构→映射既有 M2/M3 测试] + TG-C 拟人样本模板; Spec 未归档, 待 168h 运营跑
          → 填 corpus + 评分 → AC-5);
          **✅ 168h 跑 now make-ready #147 (2026-06-30 全部修复, prod tick 验证)**: 2026-06-29 live 诊断
          发现 Layer1 runtime 降级 (deploy-doctor 初判经真核实纠正 4 处: tick job 存在/register() 仓库有=
          stale deploy 非缺代码/系统在跑非"从未"/修复走 Luxeno 非充值)。修复闭环: B1 LLM Luxeno (实地核实早已
          配置, z.ai 是 stale 进程旧日志); B2 Feishu WS (gateway 重启复连稳定, 进程态非凭据非网络); B3 stale
          (重启重载当前 0.4.0); B4-code issue_type_hint (PR #28, audit 2 轮收敛 PASS); B5 scan.sh exit 127
          (PR #27); 节点 fetch 凭据 (只读 deploy key + ssh remote, forgejo SSH user=forgejo); #28 部署 light-1
          (editable, cron tick 自动生效); M1 handoff 放置 (prod 05:00 tick 验证 "not found" 消失, 读真 sha);
          镜像 claude-m5-91b8975-v11 在 registry; feature/stale labels 建好。AC-6 false-green 修 (#146 PR #26)。
          **剩余 = owner 168h 运营仪式** (pre-flight→Day-1 anchor→B4-label seed-aria-auto-issues.sh→每日 probe→
          corpus+评分→AC-5), AI 侧阻塞全清; runbook .aria/probes/m6-7d-run-startup-checklist.md;
          #4 release-closeout sequential (消费 #2 证据);
          M6 ship 后 (M7+) aria-fleet 三层架构 (通用/workspace/instance);
          **M7 设计 brainstorm 已起步 (2026-06-18, 纯 planning 非 OpenSpec)**: 两子能力设计备忘录就绪 —
          agent 生命周期管理 `.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md`
          + fleet MVP 跨项目聚合 `.aria/notes/2026-06-18-aria-fleet-mvp-cross-project-aggregation.md`;
          三层架构基线 `.aria/notes/2026-05-27-aria-fleet-three-layer-architecture.md` (D1-D6 Approved)。
          **M7 OpenSpec 两 sub-Spec ✅ Approved (2026-06-18, owner sign-off; post_spec R1→R2 CONVERGED)**:
          `openspec/changes/aria-2.0-m7-fleet-aggregation/` + `aria-2.0-m7-agent-lifecycle/` (各 proposal.md + tasks.md);
          规范先行前置已补 (PRD §里程碑 M7 stub + **US-028** [US-027 已被 Cost-routing 占用]);
          **ready for Phase A.3 agent 分配; Phase B 受 D3 时机门 (M6 release-closeout ship 后)**
```

### User Story 编号分区

```
US-001~009: v1.x 已有 (done/in_progress/pending)
US-010~019: v1.x 新增 (Agent Team 质量 + 项目适配)
US-020~027: v2.0 (待起草)
```

---

**更新**: 2026-07-01 (Layer 2 主力 LLM glm-5.1→glm-5.2 切换 — 无插件版本变更, aria-orchestrator 运行时侧, 主仓 gitlink `f5fdb9e`): owner 追问 "Layer 2 用哪个 LLM" 起。**(1) 认知纠正**: 核实 Layer 2 虽装 Claude Code CLI, **底层实跑 GLM (非 Claude)** —— `ANTHROPIC_BASE_URL=luxeno.ai` (10CG 自有 Portkey 代理, Anthropic 兼容 schema) + `ANTHROPIC_DEFAULT_*_MODEL` 把 CC 内部 opus/sonnet/haiku 三档重映射到 glm-5.1/glm-5-turbo/glm-4.5-air; 主力 opus 档=glm-5.1。根因 AD-M1-12 (owner 无 Anthropic 账号/预算 → 回滚 Luxeno→GLM)。**两层都跑 GLM, Claude Code 只是 agent 外壳**。修正前几轮 "Layer 2=Claude" 口误; memory `project_layer2_actual_llm_is_glm_via_luxeno` 新建。**(2) glm-5.2 反馈**: owner 要升 glm-5.2 (国内外皆可) → SilkNode **#830** feature request (p2-high) → SilkNode 回帖**确认 glm-5.2 上线可路由** (model 名 `glm-5.2`, Anthropic 端点直通, z.ai 国际+bigmodel 国内**双活冗余**, 同价 $1.0/$3.2)。**(3) Layer 2 切换执行**: light-1 `nomad var` 改 `ANTHROPIC_DEFAULT_OPUS_MODEL` glm-5.1→glm-5.2 (get-json→python 改单字段→put **CAS `-check-index`**; 无 jq 用 python; 8 keys/3 secret 严格断言全保; Rule #7 secret 不回显; CAS 冲突=安全网重放)。验 opus=glm-5.2 ✅; **Layer 1 保持 glm-4.5-air** (owner 决定, triage 低频省成本)。**(4) 文档**: `glm-5.2-cutover-runbook.md` 入库 (实测版 python/CAS/8-keys) + M6 `m6-7d-run-startup-checklist.md` Phase 0 补 pre-flight dispatch 确切命令 (provenance A replay M5 O3 不可用[capture 缺]→用 B fresh synthetic; 手动直派 aria-layer2-runner 5 meta 跳过 Layer 1 不打 aria-auto vs Phase 2 seed 区别; 验 glm-5.2 via result.json)。**剩余**: #830 留 open 待 pre-flight `result.json` model=glm-5.2 端到端验证后 close; glm-5.2 真跑质量待 168h 跑验 (架构 R1 tool-use/R2 命令质量)。aria-orchestrator `a7afaaa→f3848b2` (runbook×2); 主仓 gitlink+checklist 双远程 parity。**并发 session note**: 本 session 期间另有 session ship aria v1.50.2 secret-guard (2026-07-01 泄露事件, disjoint 不冲突)。
> 前次 2026-06-30 (M6 #147 runtime remediation 闭环 — 168h 跑 now make-ready, aria-orchestrator 侧无插件版本变更): 承 2026-06-29 诊断, 把 #147 Layer1 runtime 降级**逐项修复 + prod 验证**, M6 从"误以为只差启动"→真正 make-ready。**修复**: B1 LLM Luxeno (实地核实 .env/auth.json 早已配 Luxeno, z.ai 429 是 stale 进程旧日志, 最新 stderr 0 条 z.ai = 已解决, 非待办); B2 Feishu WS 长连 (分诊: 凭据有效[tenant_access_token code=0]+egress 通[短连 10/10], 是连上后 keepalive 掉线=进程态 → gateway 重启后稳定连 msg-frontier.feishu.cn 3+min 0 掉线); B3 stale (重启重载磁盘 0.4.0 register()); **B4-code issue_type_hint (PR #28)**: seed 从 bug/feature/stale 标签写 issue_type_hint 进 audit payload 顶层 (transition_state 加 audit_extra, 区别于 extra_fields=DB列) 供 AC-2 stratification, 经 **audit-engine pre_merge 2 轮收敛** (R1 qa REVISE 抓 2 important: gate-chain 两半未合验[seed dict.get vs acceptance json_extract] + 三类型仅测 bug → 落地 json_extract 合验+三类型+reserved 守卫 → R2 全票 PASS); B5 scan.sh exit 127 (PR #27); **节点 fetch 凭据卡点** (root@light-1 无 key+空 .git-credentials → 生成只读 deploy key 注册两 repo[id5/6]+remote 切 ssh://forgejo@192.168.69.200, **forgejo SSH user=forgejo 非 git**); #28 部署 light-1 (git pull+submodule a7afaaa, pip editable cron tick 自动生效); M1 handoff 放置 (docs/m1-handoff.yaml→运行时路径, **05:00 prod tick 验证 "M1 handoff not found" 消失** 读真 sha 91b8975; 校验器对运行时副本 FAIL 是 memo_path 相对路径假象非内容错); 镜像 claude-m5-91b8975-v11 ∈ registry 确认; feature/stale labels 建。**B4-label 故意保留给 owner kickoff** (造 aria-auto issue=启动自主派发, 应落 Day-1 anchor 后, 现造会出 168h 窗口浪费预算)。aria-orchestrator master dd52d34→a7afaaa (PR #27+#28); 主仓 gitlink + 3 审计报告/runbook/脚本 committed; #147 open (剩 owner 运营仪式)。2 memory (verify_agent_diagnosis_against_live_state / forgejo_ssh_node_deploy_key)。M6 现 100% AI-side make-ready, 启动只剩不可代劳的 owner 168h 运营 + 评分。
> 前次 2026-06-29 (M6 AC-6 修复 cycle + M6 runtime live 诊断纠正 + M7 agent 集合库调研 — 无插件版本变更, aria-orchestrator 侧): owner 多轮驱动的 M6 推进 session。**(1) M6 AC-6 false-green 修复 (#146→PR #26 merge `dd52d34`)**: state-scanner 等待期发现 `check-m6-e2e-acceptance.py` AC-6 pre-flight 闸只校验 cost ≤$2, 空模板 `cost_usd:0.00`+`dispatch_id:<id>` 占位即 PASS (假绿)。RED-first 修 (占位检测: 3 非占位 dispatch_id + provenance option∈{A,B,C}) → **audit-engine pre_merge 3 轮收敛审计** (code-reviewer/qa/tech-lead): R1 全 PASS(minor) → **R2 qa REVISE 抓出 R1 修复自身引入的二次 false-PASS** (`[:3]` 窗口被行首 prose 挤出隐藏占位) → R3 全票 PASS CONVERGED; 28→42 测试; owner 授权自合 PR #26。审计报告 `.aria/audit-reports/pre_merge-R3-*-m6-ac6-146-convergence.md`; spec §A.8 errata 标 RESOLVED; #146 closed。memory `feedback_multiround_audit_catches_fix_introduced_regression`。**(2) M6 168h 跑就绪性 live 诊断 → 认知纠正 (#147)**: 为启动 168h 跑查 light-1 集群, `aether-status`+`deploy-doctor` 发现 Layer1 runtime **降级非就绪**: 主 tick `aria-layer1-cron` 在跑但 `processed:0` 空转 (0 dispatch)+M1 handoff 缺失 / gateway heartbeat LLM 打 z.ai 死账户 (429, **应改走 Luxeno** per owner) / Feishu 凭据失效 37 天 (人类门 AD10 失联) / gateway 插件+cron 多处 stale deploy。**deploy-doctor 初判经真核实纠正 4 处** (tick job 存在/register() 仓库有=stale deploy 非缺代码/系统在跑非"从未"/修复走 Luxeno 非充值)。开 **#147** 跟踪 (B1 Luxeno/B2 Feishu/B3 redeploy/B4 tick空转/B5 scan.sh); **B5 scan.sh 相对路径 exit 127 修复 PR #27** (AI 唯一可独立修, 其余 owner/基建); redeploy 步骤入 #147。memory `feedback_verify_agent_diagnosis_against_live_state`。**纠正**: 之前"M6 只差 owner 启动 168h 跑"错误, B1-B4 修好前 168h 跑无意义。**(3) M7 agent 集合库 deep-research**: 评估高星 agent 合集作 backing library — VoltAgent/awesome-claude-code-subagents 首选 (MIT/154+/原生格式), wshobson/agents 确认为 Aria agent 血缘源 (已 web 比对); cherry-pick 非整库 vendor。notes `.aria/notes/2026-06-27-agent-collection-backing-library-research.md` + #128 评论 + memory。**(4) M6 启动 runbook** `.aria/probes/m6-7d-run-startup-checklist.md`。主仓 commits 双远程 parity; PR #26 已合 (aria-orchestrator), PR #27 待 owner 合。主线 M6 现实状态 = runtime 降级待 owner 修 (B1-B4), 非待启动)
> 前次 2026-06-26 #2 (插件 v1.50.1 patch — session-closer 触发消歧矩阵**内联自包含** + Parent US-013 锁定: 承 v1.50.0 ship 后 owner 两问。(1) **补 Parent US**: 建 US-013 会话维度收尾仪式 (done v1.50.0) + 回填归档 spec Parent US 待分配→US-013, carry M1 闭环 (主仓 `18c2dc6`)。(2) **第三方可用性确认 + 内联**: 核实第三方升级 aria-plugin v1.50.0 + 重启 Claude Code 即可用 (skill auto-discovery 无需登记 / 触发靠 description 随插件走 / 脚本+模板+handoff-mechanics SOT 全在插件内); 但 standards §1.3 消歧节**不随插件分发** (standards 独立子模块, 16 skill 通用引用模式 — 非 session-closer 回归)。owner 要求内联 → session-closer SKILL.md「我应该用这个 Skill 吗？」加**触发消歧速查表** (对话收尾/写交接/收尾阶段 → 期望命中 skill), 第三方不 vendor aria-standards 也有自包含路由消歧; standards §1.3 保留完整方法论 SOT, SKILL.md 速查非完整复制避 drift (Level 1 doc 自包含, 无逻辑/测试变更; Skill 1.0.0→1.0.1)。aria patch `daa3945` 双远程 + 主仓 gitlink + 6 面 SoT v1.50.1 + 主仓 v1.7.2→1.7.3 + root badge/i18n marker sync。Skills 不变 (42)。**meta-dogfood 收尾** (handoff `2026-06-26-#2`): session-closer 自身写本 session handoff ("执行对话收尾" 命中 session-closer 非 phase-d-closer — 消歧实战验证); 2 memory (reused-code 假绿 / plugin 路由内容自包含)。**旧分支清理**: 已被取代的 3 个 session-closeout-internalization feature 分支 (主仓 spec/ tip 53b3bc0 / aria 776e140 / standards f7b7f42) 6 远程分支删除 (origin+github 各仓); SHA 在 handoff/archive 留档 (归档 trail 无损), stale ref pruned 0 残留。主线 M6/M7 未触碰)
> 前次 2026-06-26 (插件 v1.50.0 ship — **session-closer-synthesis** [DEC-20260625-001]: owner 起于第三方用 Aria 输入"执行对话收尾"误命中 phase-d-closer (周期收尾)。调研发现该 5 步会话收尾**之前已立项实现** (Spec `session-closeout-internalization`, Phase B 9/10 + benchmark +28.5% owner 签字) 但**从未 ship**, 搁浅 3 未合并 feature 分支 ~3 周。**重评估**: owner 偏好"独立 leaf skill"(正交平级仪式) 而非旧"薄入口委托 phase-d closeout_only"(三理由: 概念完整 / trigger 消歧干净 [旧因 phase-d 仍是引擎摘不掉「收尾/handoff」description → Gap 1 撞车未根治] / step1/2 字面=对话内省被旧 Spec 降级 best-effort)。**综合方案** = 独立 leaf + 复用既有 handoff-mechanics.md 共享 SOT + AI 内省优先机械兜底 + description 收紧消歧。**brainstorm 5 决策 → DEC → Phase A**: proposal/tasks → **post_spec R1 REVISE×3** (审计抓出主 loop 可行性"绿灯"漏的 2 Critical: 既有 ref 复用非新建 [起草未 recon, 违 `[[feedback_recon_real_code_before_implementing_spec_test_suite]]`] + collector 字段漂移 [旧脚本基于 v1.39, 真 collector active_changes→changes / cycle_number→current_cycle / in_progress 不存在; 旧测试手造 fixture 假绿]) → Rev1 → **R2 PASS×3 unanimous**。**Phase B**: cherry-pick 重组 (路径 session-closeout→session-closer grep 0 残留) + handoff_autofill adapter 重建 + 字段修正 + leaf SKILL.md + phase-d description rebind (D.1/D.2/D.3 零 diff) + standards §1.3 消歧矩阵 + phase-b/c 钩子。49 单测 + 真 snapshot 集成 (堵假绿)。**code-review** Phase 1 PASS + Phase 2 I-1 (钩子喂 relay cache 无 source → trigger 生产恒不 fire silent → 改喂 token_telemetry) + I-2 (carry_forward 真形态 {count,samples} 产垃圾 → samples 展开) 假绿全修 + 真形态/负向契约测试。**Rule #6**: 49 单测 = deterministic structural substitute + capability AB **+13.3pp** (判别项 = step2 结构标记 `[候选 memory]` 可机械验证; baseline 因场景显式接近 = process skill in-repo 保守下界 `[[feedback_process_vs_content_skills]]`) **owner sign-off A** (delta≤0 非硬门 per AC-10b)。aria master `9a2d185` + standards `350a7cf` 双远程; 主仓 gitlink + VERSION 1.7.1→1.7.2 + CHANGELOG + root README badge v1.50.0 + i18n marker sync + 6 aria SOT; Spec 归档 `openspec/archive/2026-06-26-session-closer-synthesis`。Skills 41→42 (新 user-facing session-closer)。旧 3 feature 分支**已清理** (见下 #2 收尾后)。M6/M7 主线仍 owner/外部门控 (本 cycle 是 owner 直接需求, 与主线解耦))
> 前次 2026-06-21 #3 (插件 v1.49.0 ship — submodule-gate warn→block flip [#124 parent Two-phase rollout 执行单元]: 本日 v1.48.0 ship 把 block-flip telemetry executions 推到 5/3 (≥3 阈值) → /state-scanner 检出 `block-flip-executions-progress` READY → owner 评估。**真实证据核实** (不只信 check): 5 gate executions (`submodule-gate-executions.jsonl`, 全 mode=warn/PASS) + 4 clean host-cron tripwire (`misses.jsonl`) + FP 0%。**诚实披露 integrity nuance**: 5 条聚 2 个 ship 事件 (v1.47.0+v1.48.0), 后 3 条是 v1.48.0 release commit 的 index.lock 重试虚增 → 严格独立观察=2; gate 全程 warn-PASS 从未走真实 block 路径 (无 regression 发生)。owner 三选 (等第 3 独立 ship / risk-accept / 留独立动作) → **risk-accept flip** (字面阈值满足 + tripwire 真绿独立 + FP 0% + backward-compat 逃生舱)。**执行** (Spec 已 Approved 2026-05-25, 仅 Phase B/C/D): §A 3 处 default flip (`submodule_gate.sh:33` MODE `:-warn}`→`:-block}` runtime SOT + `SKILL.md:450` inline-bash + config 表/Two-phase/verdict 三态/mode 参数表 全集 warn→block 现在时, 保留 v1.28.0 历史行) + **新测试 T-flip-12** (unset MODE→block, regression exit 1; 锁定 flip, 15 PASS/0 FAIL was 14) + §F standards wording。**§B workflow cron 作废** (host-cron `0 4 * * 0` 已迁移 v1.41.0 R-fix-2)。backward-compat: `mode=warn` legacy / `mode=off` bypass / env override 全保留。决策记录 `.aria/decisions/2026-06-21-v1.49.0-block-flip.md` (§6 open-PR 审查: 无 in-flight 撞 block; standards 并发 sister PR #11 STD-GUIDE-003 正交吸收)。aria PR #90 merge `f3b7ac5` 双远程; standards `ddaf3d1` 双远程 (我的 wording rebase 在 sister cdf6bfd 上, origin ff + github force-with-lease); 主仓 gitlink aria→f3b7ac5 + standards→ddaf3d1 + VERSION 1.7.0→1.7.1 + CHANGELOG [1.7.1] + README badge v1.49.0 + 5 aria SOT v1.49.0; Spec 归档 `openspec/archive/2026-06-21-aria-submodule-gate-block-flip`。Skills 不变 (34+7=41)。**block-flip 闭环** (D+14 DEFER → 06-14 telemetry 根因修 → 本日 Trigger B flip)。M6/M7 主线仍 owner/外部门控。**本 session 早段**: #145 re-triage → v1.48.0 agent-team-audit 增补 ship → i18n marker 同步 → 本 v1.49.0 block-flip。**flip 后 closeout** (`e9a7313`): 退役过时 `block-flip-executions-progress` custom check (监控目的已达成, 今后由 T-flip-12 测试 + tripwire host-cron 守护) + i18n marker 再同步 v1.49.0; 复扫 custom checks 6 pass / 0 fail)
> 前次 2026-06-21 #2 (插件 v1.48.0 ship — agent-team-audit-project-agent-augmentation #145: 承接本日 #145 re-triage (verdict `next-cycle`) → owner 选起 cycle → 完整十步循环单 session 闭环。**问题**: `agent-team-audit` 选择 step 3 写死静态 matrix (3 触发点→固定 4 内置 agent), 从不消费 `.aria/agents/` 项目专属 audit agent; `agent-gap-analyzer→agent-creator→.aria/agents/` 生成链 (含 capabilities tags) 建成但 audit 消费方永不选入 → reporter 项目 security-auditor 抓的 Critical 用不上。**brainstorm** (technical, 2 决策 + 1 代码核实触发修正 → DEC-20260621-001): 选择模型 = **Augment 增补** (基线永远跑+项目 agent 纯加法) + 匹配判据 = **专有标签阈值** (显式策展白名单); **段 2 关键修正**: 放弃 baseline 减法 (code-reviewer 已带 `security-audit` → 减法会盖住项目 security-auditor 恰打不中 reporter 用例) → 改显式白名单解耦。**post_brainstorm 配置 off** (预算集中 post_spec)。**Phase A** Level 2 proposal → **post_spec R1 REVISE** (tech-lead PASS_WITH_WARNINGS + km REVISE; 7 实质 findings: I-1 max_parallel_agents×增补交互 / K-1 文档同步漏 audit-points agents 字段 / K-2 AC-5 dogfood 在 Aria 无 .aria/agents/ 只验 AC-3 → 新增 AC-6 绑 fixture / M-1 experiment 门控披露 / M-2 frontmatter 边界可证化 / M-3 OOS 措辞 / M-4 输出分母) → Rev1 全落地 → **R2 CONVERGED** (unanimous PASS 2/2, r1_landed=true)。**Phase B** (aria 子模块): step 3 拆 3a 固定基线 / 3b 项目级 capabilities 增补 (复用 agent-router `.aria/agents/` 发现范式; 冷路径直读 frontmatter; 降级纯基线零回归); matrix 新增白名单列 (pre_merge/post_implementation: `security-audit`,`performance-optimization`; post_spec 空) + step 3b 算法 + 并发调度; SKILL.md 触发点表/输出分母 (=基线+增补); audit-points 各 agents 字段注记 (mid_post_spec 标注不在增补范围)。**Rule #6** = structural fixture (5 文件: security-auditor 命中 / doc-helper 通用不命中 / malformed 缺失skip / empty-caps 空list合法 / 1 算法 trace) + **AC-5 dogfood** (Aria 无 `.aria/agents/` + experiment 默认关 → 纯基线零回归确认)。**code-review** Phase 1 PASS (规范合规, 非 baseline 减法决策三重锚定, 无 paper-fix) + Phase 2 I-1 (补 empty-caps fixture) / I-2 (执行+记录 dogfood) / M-1 (taxonomy 路径消歧) / M-2 (领域标签非 load-bearing) 全收。**与 M7 agent-lifecycle 正交** (M7=物化到 .claude/agents/ 原生加载侧; 本=audit 消费侧; OOS: agent-creator→.claude/agents/ 让给 M7 / override / 扩 taxonomy / 改 agent-router / experiment 转正)。`agent-team-audit` = experimental (默认关), 能力随 experiment 转正才可用。agent-team-audit skill 1.0.0→1.1.0。aria PR #89 merge `a922e5c` 双远程 parity; 主仓 gitlink → a922e5c + 5 SOT v1.48.0 + root README badge/L242 + i18n badge (aria/README.zh 预存在滞后 1.41.0 不动, #140 B 档无正文变更); Spec 归档 `openspec/archive/2026-06-21-agent-team-audit-project-agent-augmentation`; close #145。Skills 不变 (34+7=41)。M6/M7 主线仍 owner/外部门控 (本 cycle 与主线解耦, 等待期填空))
> 前次 2026-06-21 (#145 re-triage — **无 ship / 无版本变更 / issue 保持 open**: owner /state-scanner → 判定主线 M6/M7 全 owner/外部门控 (M6 168h 运营跑 + AC-5 不可伪造; M7 Phase B 受 D3=M6 ship 门; block-flip 1/3 executions 需 future ship 累积) → 等待期, 仅 #145 为自上次 sweep 后新增候选 → owner "triage #145"。**#145 已于 2026-06-13 (v1.46.4) triage 过** (verdict `partial-repro`/`major`/`next-cycle` 已 POST), 本次 re-triage 确认**结论在 v1.47.0 仍成立**: triage.py exit 0 + 复核 5 步; 核实 v1.47.0 cycle B/C **改了** agent-team-audit (加 data-availability + mid_post_spec 检查点) 但 **selection-matrix 对 `.aria/agents/` / capabilities 路由仍零支持** (grep 零命中), 8 天无修复 commit / 无 in-flight → 核心断裂 (agent-team-audit 永不发现/唤醒项目专属 audit agent) **CONFIRMED 持续**。**关键新核实**: M7 agent-lifecycle Spec **引用 #145 仅用于 "重启生效" caveat (CAVEAT #3) + git 集合库 vs marketplace 决策依据**, **不覆盖** #145 核心诉求 (M7 = 项目 agent 物化进 `.claude/agents/` 原生加载; #145 = audit selection-matrix 按 capabilities 动态选项目 agent — **两者正交, M7 ship 不自动解决 #145**)。owner 选"更新 triage 评论" → POST 补充评论 `#issuecomment-13407` (不重复原 verdict, 仅加 v1.47.0 断裂持续 + M7 正交性澄清)。`agent-team-audit` = experimental (默认关闭) 影响优先级但不改断裂真实性; `next-cycle` 需 brainstorm 收敛 capabilities 路由设计 (可复用 agent-router 的 `.aria/agents/` 发现范式), 待 owner M7 立项时一并排期或下个等待期填空批起独立 cycle。Skills/版本/插件全不变 (v1.47.0)。主线未触碰)
> 前次 2026-06-19 (插件 v1.47.0 ship — **issue-sweep release train, 4 cycle / 6 issue 一次性执行**: owner /goal "遵循 aria 规范, 创建 agent team, 动态工作流, 自我判断优化, 一次性执行完纯 AI 可独立完成 + 现在值得做的 issue"。先 triage 13 open issue → 判定 5 个纯 AI 可独立完成 (#69/#54/#95/#79/#32; 排除 owner/外部门控 #136 轮换 / #120 基建 / #5 战略 + 非独立 #138/#128)。**自我判断优化 = release-train**: 4 cycle 全 aria-plugin Skill 变更 → 共享 release 分支增量实现 + per-cycle 独立 agent-team 对抗 review, 一次 Phase D 打包 v1.47.0 (省 4× ship 开销)。**Cycle A #69** secret-guard 扩 exfil: Aether v1.28.0 dogfood 5 FN, **实测 triage 确认 v1.46.5 仍全漏 + 6 额外探针** → RED-first 16 BLOCK 探针 + 4 FP guard → regex (base64 reader/非标准 ssh key/.docker/config.json/Vault HTTP header/kubectl sh-c 包裹/scp·rsync·cp·tar|ssh·wget exfil), 254/254; 2-lens (code-reviewer + 对抗 hunter) 修真 FP (scp /private/ macOS / X-Vault-Token 文档提及 / hvs.{6→24} / tar .sshconfig) + bypass (dd bs= / cp EOL-dest)。**Cycle B #54+#95** audit-points 加 数据可用性 (verdict-load-bearing 缺失→REVISE/FAIL) + 框架约定 检查项 + phase-b 可选 B.2.5 build gate (tri-state not_configured≠pass) + spec-drafter Framework Constraints; knowledge-manager+tech-lead review 修 verdict 后果/skip tri-state/3 处列表去重。**Cycle C #79** mid_post_spec 条件触发检查点 (Phase B spec 漂移 single-round/scope-limited/append-only amendment+neutralize); tech-lead 根因洞察补齐 4 处 engine-internal 契约 (pre-merge 完整性 gate **排除** 事件条件触发 checkpoint [ship-blocking] / max_rounds clamp / anchor 分类 / blocking 表)。**Cycle D #32** tdd-enforcer security_commit_separation (安全代码 RED/GREEN commit 强制分离, = level_3_strict 改名避 strictness 歧义, commit-msg hook + word-boundary 检测); code-reviewer+tech-lead 修参考 hook 真 bug (pre-commit 读错 commit→commit-msg / test_*.py 前缀 + top-level tests/ 锚 / 安全 grep word-boundary 防 authority/oauth/healthcheck 误命中, 自身 dogfood 14 case 验证 / advisory 行 self-negating 删)。aria PR #88 merge `281388d` 双远程 parity; 主仓 gitlink → 281388d + 5 SOT v1.47.0 + i18n badge/marker 同步 (#140 B 档无重译); 4 OpenSpec 归档 `openspec/archive/2026-06-19-*`; close #69/#54/#95/#79/#32。Rule #6 全 cycle = deterministic structural + dogfood-by-construction (多-agent 审计无自动 AB harness)。Skills 不变 (41)。M6/M7 主线仍 owner/外部门控 (本批是等待期填空, 不动 M6 ship / M7 Phase B D3 门))
> 前次 2026-06-18 (M7 aria-fleet 双 brainstorm — **纯 planning, 无 ship / 不动插件版本**: owner "M7 aria-fleet brainstorm" → 定焦 "先 1 再 2" → 两轮战略设计 brainstorm, 产出两份设计备忘录 (planning sediment, 非 OpenSpec, 正式 audit 留 M7 立项时)。**轮 1 = agent 生命周期管理** (fleet 子能力, `.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md`): 定位先对内 / 设计预留通用 (避方法论红线); **机制反转** —— marketplace 选择性最细只到插件粒度 (claude-code-guide 核实), 给不了 agent 粒度 → 撤销 marketplace 试水, 改 **git 集合库 + 文件物化进 .claude/agents/**; 六阶段双向飞轮 (推荐→加载→使用→更新 / 吸收→汇总); AB 驱动吸收矩阵 (reverse-push / forward-pull) + usage-telemetry 活体库 + 零游离不变式; **deep-research 业界对标** (22 源 / 25 对抗核实 / 24 确认 1 驳回) → 4 修正: ① 不拿固定测试集当 one-shot 择优 gate (基准可 harness-game 刷满分 + UTBoost 排名翻转 24-41% + SWE-bench Verified 2026-02 弃用) ② 裁决用 pairwise LLM-judge + PoLL + 去偏三件套 (position-swap 双跑 / 五维 forced-choice) ③ 影子-配对**并发**避时间混淆 ④ 影子 + 池化遥测 = Aria 原创须自证 (interleaving 100× 主张 3 票驳回); M7 第一刀 = 下行 pull 半环 (复用现成 project-analyzer / agent-gap-analyzer / agent-creator / agent-router)。**轮 2 = fleet 整体 MVP** (核心指挥塔, `.aria/notes/2026-06-18-aria-fleet-mvp-cross-project-aggregation.md`): 第一刀 = 跨项目状态**只读聚合 tool pack** (复用各项目 state-snapshot.json); 取数模型 ① 默认读现有快照 + 陈旧度 + ② 超阈/按请求跑 scan.py 刷新 (scan.py 幂等安全不破只读) + ③ 推送中央库推迟; recon 确认 boundary-audit (2026-05-27) 两 P0 已 ship (v1.30.0 Forgejo hosts 参数化 + v1.31.0 CI 后端抽象) → 候选 ③ hardcode 修复作废。**收尾**: 2 memory (`feedback_static_benchmark_unfit_as_oneshot_selection_gate` + `reference_llm_judge_debiasing_trio`) + #128 tracker 评论 `#issuecomment-13165` + 主仓 commit `8d50cb8` 双远程 parity。实施待 M6 ship 后据两份备忘录起 M7 OpenSpec)
> 前次 2026-06-14 (插件 v1.46.5 ship — submodule-gate telemetry timeout 修复 (R-fix-1 follow-up; block-flip 重启诊断): owner "block-flip 重启" → 系统 recon 发现重启前置 ≥3 gate executions **无法靠等待满足** —— tripwire 已绿 (2 clean host-cron runs), 但 executions=0/6 次 gitlink commit。**根因实测** (exit 124 复现): R-fix-1 (v1.40.0) telemetry hook WARN 跑 gate 记录执行, 但 `log_execution` 在 per-submodule `git fetch origin` **之后**; aria/aria-orchestrator origin=forgejo (CF-Access) fetch hang 超 hook `timeout 15` → gate 杀于记录前 → 0 executions (block-flip D+14 Trigger C 根因**持续**, R-fix-1 未真修)。诊断改变"重启"性质 (代码 bug 非观察窗口) → 给 owner A/B/C 三路径 → owner 选 **A: 先修 telemetry 再攒真数据**。修: WARN/telemetry 模式**跳过** per-sub fetch (O(N)→O(1) 本地 refs, WARN 仅 advisory; 因 3 个 forgejo submodule 各 fetch 即使 bounded 也撞 budget) + `bounded_fetch` (timeout 包裹防无限 hang, Windows fall back) + hook wrap 15→25 + hooks.json 20→30; block/merge-flow fetch 不变 (authoritative)。**dogfood**: WARN 完成 9s + 记录真实 PASS execution; block 32s 不变 + 记录。gate 14 PASS (新 scenario_11: WARN origin 不可达仍完成+记录) / hook 7 PASS / state-scanner 821 OK (1 issue-cache timing flake 复跑转绿)。aria PR #87 merge `28c1a4d` 双远程 parity; 主仓 gitlink → 28c1a4d。i18n badge+marker 机械同步 v1.46.4→v1.46.5 (非重译, README 可译内容未变; #140 B 档 check 提醒)。block-flip Spec 状态更新 (telemetry 已修, 待 ≥3 真 executions 累积 → Trigger B flip; D+42=2026-07-05)。**本 session 双 cycle**: 早 #140 i18n README 全量重译 (root docs, 无 plugin bump, 已 closeout) + 本 v1.46.5 telemetry ship)
> 前次 2026-06-13 #4 (插件 v1.46.4 ship — coordination-ref lib _run timeout ceiling (F2-minimal): owner "修 F2" → **澄清歧义** (F2 两读法: 我上条 summary 的 _run full-parity vs 原 #141 的分支头耦合解耦) + 验证价值 (最低价值剩余项; F1 已补关键 #61/#143, 剩 timeout 唯一真实有用, dedup/耦合解耦是风险 refactor) → owner 选 **Minimal: 加 timeout** → Level 1 → lib _run 加 timeout=30 (tiny ref 极宽松不误失败) + TimeoutExpired→124 (fetch 分类 network) + None-guard; **故意跳过 rc 对齐** (FileNotFoundError 保 -1; lib callers 判 rc<0 改 127 会破坏, F1 review 已 flag) → code-review PASS (全 11 lib _run callers 优雅处理 rc=124 + rc-跳过正确)。dedup 两 _run + 分支头耦合解耦 defer (低价值/风险 opt-in-gated)。TestRunTimeout 3 测试 + 88 coordination 测试全过 + 821 全绿 (一次 transient 726+5err = run_tests collection flake 非本变更, 3 次复跑稳定)。aria PR #86 merge `ffdbec5` + release `1961f6c` 双远程; 主仓 gitlink → 1961f6c; F2-minimal 收口 (无 issue)。**#141 review 派生 follow-up 全处置**: F1 fixed v1.46.3 / F2 timeout-slice fixed v1.46.4 [dedup+耦合解耦 backlog] / F3=#142 wont-fix / F4=#143 fixed / F5=#144 fixed)
> 前次 2026-06-13 #3 (插件 v1.46.3 ship — coordination-ref-lib-run-parity (F1): owner "修 F1" → 验证诊断 (lib/coordination_ref.py 有**自己的 _run** 独立于 collectors/_common._run, #61/#143 加固只改了 collector 那个 → 本地 _run ① 非英文 locale auth/network 匹配失灵 ② C-locale+非ASCII claim 内容 UnicodeDecodeError 崩溃; fetch_coordination_ref 无 benign-absent) → owner 选 "修 a+b 一致性" → Level 2 Spec → post_spec R1 2/3 REVISE 3 major (全为测试落点太松允许 mock 绕过真 code path) → Rev1 强制 TG-C lib-直测 → R2 3/3 PASS → 实施 (本地 _run 加 #61 encoding/errors + #143 LC_ALL=C 末位非覆盖; fetch_coordination_ref 加 benign 三重 AND 镜像 collector 复制非 import 防 layering; 只加 #61/#143 timeout/None-guard 留 F2) → code-review PASS。可达性低 (opt-in phase1_gate 默认关) 但真实潜在崩溃/locale 隐患, 消除两分叉 _run 缺口。7 lib-直测 (非 mock wholesale) + 97 coordination 测试全过 under LC_ALL=C + 818 全绿 (1 已知 flake 无关)。aria PR #85 merge `0ccf42e` + release `82e0e75` 双远程; 主仓 gitlink → 82e0e75; F1 收口 (无 issue)。**本 session #141 review 派生 F1-F5 全收口** (F1 fixed v1.46.3 / F2 仍 open 低优 / F3=#142 wont-fix / F4=#143 fixed / F5=#144 fixed))
> 前次 2026-06-13 #2 (插件 v1.46.2 ship — track-board-coordination-stale-bar #144 (F5): owner "修 F5 #144" → 验证诊断 (track_board 确不读 errors[]/coordination_ref_present, half-silent 属实) → **Level 1** (render-only 单函数低 blast-radius, 无 OpenSpec; 区别于 #143 改共用 _run=Level 2) → 实施 render_track_board 加非阻塞黄条 "⚠ 协调 ref 未取到 ..." gate 在 errors[] 的 coordination_ref_fetch_failed → code-review PASS [验证 errors[] 耦合**优于**备选: coordination_ref_present is None 单独会误报 Fetch-1-fail-no-cache; M-1 fail-soft 断言加固]。Fetch1 ok + Fetch2 非 benign 失败时看板原全绿无提示 (soft_error 进 errors[]/exit 10 但 render 缺感知) → 黄条消除 half-silent; degraded 时红条优先。TestCaseF 6 测试 + 810 全绿 (1 已知 timing flake 无关, render-side 不碰 normalize)。aria PR #84 merge `3e3cdc6` + release `bfcd47a` 双远程; 主仓 gitlink → bfcd47a; #144 closed [fixed]。Level 1 无 Spec 归档。**本 session F3/F4/F5 follow-up 全收口** (#142 wont-fix / #143 fixed / #144 fixed))
> 前次 2026-06-13 (插件 v1.46.1 ship — state-scanner-git-stderr-locale-hardening #143 (F4) + #142 (F3 wont-fix): owner /state-scanner 后选"修 #142" → 验证 ls-remote 实测 absent 与 hidden 同 rc=2 [git 协议不可解, #142 标题目标做不到] → owner 大白话理解后选 ③ 合并 #142+#143 一 cycle → Level 2 Spec → post_spec R1 2/4 REVISE 3 major [#142 收口 conflate (LC_ALL=C 不解决 auth-masked) / "803 绿"C-locale CI 循环论证 / CJK 命令 --format=%s→--oneline] → Rev1 → R2 4/4 PASS unanimous → 实施 [_run 注入 env LC_ALL=C 主 loop 亲自; env 断言 host-locale-agnostic + CJK 真测] → code-review PASS [M-1 CJK 全 subject 断言加固]。LC_ALL=C 强制 git 英文诊断 → 全 git-collector 英文 stderr 匹配任意 locale 可靠; 与 #61 encoding 正交; LANG=C 冗余省。#142 wont-fix (git 协议不可解 + ls-remote decline + auth-masked documented-limitation)。805 全绿 + 138 git-collector 测试 under LC_ALL=C 零回归。aria PR #83 merge `2976dc3` + release `528d4af` 双远程; 主仓 gitlink → 528d4af; Spec 归档 `2026-06-13-state-scanner-git-stderr-locale-hardening`; #143 closed [fixed], #142 closed [wont-fix])
> 前次 2026-06-12 (插件 v1.46.0 ship — state-scanner-coordination-fetch-resilience #141 软错误① + aria-plugin #75: triage partial-repro [软错误① coordination_fetch 原子 fetch rc=128 confirmed live; 软错误② handoff_multibranch cap 已 v1.38.0 #71/#72 修, out-of-scope] → POST comment-12658 → Level 2 Spec → post_spec R1 4/5 REVISE 8 major [版本 PATCH→MINOR 先例 parity / normalize DROP_KEYS 裁定 / lib::fetch_coordination_ref distinct 路径 out-of-scope / Fetch ordering 短路 / state-snapshot-schema 新建 section] → Rev1 全落地 → R2 5/5 PASS unanimous → **agent-team 实施** [核心 coordination_fetch.py 拆两条 fetch + test_coordination_fetch.py 12 测试 主 loop 亲自零回归; TG-C 文档主 loop] → code-review 2-lens [code-reviewer PASS + silent-failure-hunter: #1 git absent-vs-hidden ref 歧义 Critical→降级 documented-limitation (Aria Forgejo 部署不可达, repo 级 ACL 同管 refs/aria/*) + #2 LC_ALL=C locale + #5 track_board 黄条 → 3 follow-up F3/F4/F5]。拆两条 fetch: Fetch1 分支头载重先跑 + Fetch2 协调 ref benign 三重 AND 闸 → 缺失不报错 success 保持 True; additive coordination_ref_present 三态 cache 持久化不进 DROP_KEYS; 803 全绿 (1 已知 flake 无关) + dogfood no-coord sandbox 真 git 修复确证 + Aria 零回归。aria PR #82 merge `2d9bbb3` + release `e45ed3c` 双远程 parity; 主仓 gitlink → e45ed3c; Spec 归档 `2026-06-12-state-scanner-coordination-fetch-resilience`; aria-plugin #75 closed [PR Closes], Aria #141 closing)
> 前次 2026-06-11 #2 (插件 v1.45.0 ship — cross-worktree-handoff-discovery #139: triage confirmed 4/4 → brainstorm 3 决策 (纯机械发现 / 两级语义+epoch 仲裁 / advisory 引导) → DEC-20260611-002 → Level 2 post_spec R1 FAIL 5M+7m → R2 PWW N-1..N-9 → R3 PASS → **agent-team 动态工作流实施** (TG-0 helper+resolver 亲自零回归 / TG-A collector / TG-B 文档 agent-team 5 文件 / TG-C 47 测试) → code-review 3-lens PWW [important ⑫ abandoned/legacy status verbatim + minor 全收: cap path 排序 / stat-fail kind / None 回退 / key-leak 守卫]。新 collector handoff_worktrees.py: git worktree list 枚举 + 复用 handoff.py 抽 _resolve_latest helper (单份 H5, collect_handoff 逐字段零回归) + epoch 域 updated-at 仲裁全局最新 → 落他树阶段 2 advisory EnterWorktree; 纯机械发现零 frontmatter schema 变更。三重 dogfood (真树 no-op + sandbox + 端到端 scan.py 多 worktree, triage case-4 修复); 52 测试 739→791 零回归; 8 文档同位; **不含 standards 变更**。aria PR #81 merge `a398b65` 双远程; Spec 归档 `2026-06-11-cross-worktree-handoff-discovery`; #139 closed)
> 前次 2026-06-11 (插件 v1.44.0 ship — audit-drift-guard #17: triage confirmed → brainstorm 4 决策 → post_brainstorm 19-agent/3 轮 23 修订 + 2 blocking 转契约 → DEC-20260611-001 → post_spec R3 PASS [抓 DEC 两勘误] → agent-team 实施 [TG-0 契约首 commit b67ccb5] → code-review PWW 全收 [I-1 防漂移文档自身漂移 / I-2 REFOCUS 撞 max_rounds 守卫] → **dogfood: Drift Guard 机制首跑产出非空 drift_metrics** [报告即新 schema 首份真实产物, 抓 2I+4m 全收]。aria PR #80 merge `5871e17` 双远程; Spec 归档 `2026-06-11-audit-drift-guard`; #17 closed。注意: challenge 审计现默认带 drift guard)
> 前次 2026-06-10 #2 (插件 v1.43.0 ship — handoff-frontmatter-enforcement #137: triage partial-repro [注入机制已存在, 缺 enforcement] → Level 2 post_spec R1/R2→R3 PASS → E1 D.3 写后自校验 + E2 scanner soft warning (resolved latest 双路径, mtime=SilkNode 事故主场景) + standards §2.3.7。739 tests + 真树 dogfood; meta-dogfood²: Level 2 归档走 v1.42.0 gap(a) Status-only 路径 + handoff 跑 E1 ==5。aria PR #79 merge `7214ae8` + standards `1be388b`; #137 closed)
> 前次同日 (插件 v1.42.0 ship — archive-completeness-gate #134: triage partial-repro → brainstorm 4 决策 → post_brainstorm 19-agent/3 轮 + post_spec 25-agent/4 轮 + verification 2 轮 [r1 抓 fresh-approved 第 4 桶黑洞] → DEC-20260609-001 两契约 [A 单一可执行 complete SOT spec_complete.py / B 单一标记载体 frontmatter archive_type] → agent-team 实施 [TG-A lib+collector / TG-B SKILL gates / TG-C standards 5 处] → code-review PASS [I-1 CRLF + I-2 渲染骨架 收]。731 tests [34 新] + 真树 dogfood [block-flip 落 design_deferred / fresh-approved 不卷入 / 100 archive 零误报]。meta-dogfood: 新 gate 上线第一刀阻断自己 spec 归档, 两条理由全对。aria PR #78 merge `18c6ba3` + standards `7ecf522` 双远程 parity; Spec 归档 `2026-06-10-aria-archive-completeness-gate`; #134 closed)
> 前次 2026-06-08 (插件 v1.41.0 ship — aria-submodule-gate-operationalize TG-2 / R-fix-2: tripwire 5/5 Actions runner 失败 [runner 无 forgejo 凭据克隆 ssh:// submodule + CF Access; 日志 API 不可达 tentative-confirm] → OQ2=(c) host-cron 迁移。新 standalone scripts/submodule-tripwire-audit.sh [HEAD~1 vs HEAD per-submodule ancestry + cat-file-e 防误报; misses.jsonl heartbeat+miss; set -u 空数组守卫; host-cron 跑绕开 runner→forgejo 墙] + 坏 workflow 标 DEPRECATED。dogfood 真仓库跑通首条成功 tripwire telemetry。10 新测 + 13 gate replay 零回归; code-review PASS [I-2/M-2/M-3/M-4 收 + I-1 确认]。**TG-1+TG-2 全完成 → Spec 归档 `openspec/archive/2026-06-08-aria-submodule-gate-operationalize`; block-flip 机制层 unblock** [gate 记 executions + tripwire 可跑], 待攒 ≥3 真实 executions + tripwire 绿即可重启 (owner)。aria-plugin PR #77 merge `b9b5d12` 双远程 parity)
> 前次 2026-06-07 (插件 v1.40.0 ship — aria-submodule-gate-operationalize TG-1 / R-fix-1: block-flip D+14 defer 的 unblock 前置。block-flip 经多 agent 动态工作流 + owner 门控 [先 dispatch tripwire 验活] 判定 = DEFER [Trigger C 0 gate executions + tripwire 5/5 验活失败, 两层防御无 live 证据]。R-fix-1 修 telemetry invocation gap: submodule_gate.sh 加 submodule-gate-executions.jsonl per-invocation 计数 [含 PASS, total_gate_executions 从推算变直接计数] + 新 PostToolUse Bash hook submodule-gate-telemetry.sh [OQ1=(a′), git commit 触 gitlink (awk 锚定 :160000 mode) 跑 gate warn+timeout15 记 execution, 零自锁 + 三层 no-op 守卫]; 不改道经 phase-c-integrator [过度工程警告]; 7 新测 + 全 hook 套件零回归; post_spec 2-round CONVERGED + code-review PASS [Minor #1 锚定/#2 timeout 已收]。TG-2 [R-fix-2 tripwire runner forgejo 凭据] infra-gated 待办, Spec 留 changes/。aria-plugin PR #76 merge `494b2f8` 双远程 parity)
> 前前次 2026-06-05 (插件 v1.39.0 ship — state-scanner-git-operation-awareness #135: interrupt collector 检测不到 git rebase/merge-in-progress 误报 interrupt:none 修复; git.py _detect_git_operation collector 字段 + 阶段 2 priority 0.5 规则 [与 interrupt 正交]; 21 新测 712 全绿; aria-plugin PR #74 merge `49722ef` 双远程 parity)
**维护**: 10CG Lab
**主仓库**: https://github.com/10CG/Aria
**插件仓库**: https://github.com/10CG/aria-plugin
**规范仓库**: https://github.com/10CG/aria-standards
