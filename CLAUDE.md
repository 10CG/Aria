# Aria - AI-DDD Methodology

> **项目本质**: AI-DDD 方法论的定义与端到端参考实现 (v1.x 方法论 + v2.0 自主运行时)
> **核心假设**: AI 不仅是协作者 (v1.x), 更是 SDLC 的自主执行者 (v2.0)
> **版本**: 2.0.0

---

## 文档边界

- **README.md** = 人类用户 ("如何使用 Aria") | **CLAUDE.md** = AI 助手 ("如何理解 Aria 项目")
- **CLAUDE.md 卫生** (Option A, `standards/conventions/claude-md-hygiene.md`, 对齐 Claude Code 官方 memory 指南 ≤200 行目标): 只放稳定的「每 session 都该知道的事实」。**不放**: 版本 changelog (→ `aria/CHANGELOG.md` SOT) / session 进展流水 (→ `docs/handoff/`, Rule #9) / **Skill 设计内部术语** (→ 各 SKILL.md 按需加载; 抄进本文件会污染 AB baseline, 实证 aria-plugin #116)。「项目状态」段 = live 覆写, 预算 15-20 行。enforcement: state-check `claude-md-changelog-free`。

## 工作语言

**中文叙述为主**。保留英文技术 token: 代码 / 命令 / 路径 / SHA / branch / PR# / 版本号 / spec 术语 / Skill·Agent 名 / memory 引用。叙述 / 解释 / 建议 / 询问 (含 AskUserQuestion options) / handoff prose 用中文。详: memory `user_chinese_conversation_default`。

## 项目定位

**方法论研究项目** (非框架实现): 探索 AI Agent 深度参与软件工程全流程。

- 协作模式: AI 理解 → 人类确认 → 协作交付 (对比传统: 人类主导 → AI 辅助)
- v1.x = 人类 + Claude Code (interactive); v2.0 = 同一套方法论放到**无人值守** (Hermes Layer 1 + aria-runner Layer 2)
- 研究目标: 可重现的 AI 协作流程 / 最小化上下文传递成本 / 结构化决策记录
- 运行时架构详见 [aria-orchestrator/docs/architecture-decisions.md](aria-orchestrator/docs/architecture-decisions.md) (AD1-AD12)

## 核心概念

**十步循环**: A 规划 (A.0 状态扫描 → A.1 规范创建 → A.2 任务规划 → A.3 Agent 分配) → B 开发 (B.1 分支创建 → B.2 执行验证; Skill 变更时含 benchmark) → C 集成 (C.1 提交 → C.2 合并) → D 收尾 (D.1 进度更新 → D.2 归档)。SOT: `standards/core/ten-step-cycle/`。

**两层 AI 分工 (v2.0)**: Layer 1 主管 (Hermes + Luxeno-routed GLM, PM 角色: triage/派发/审批; 只加载 ~1K token 元知识, **不加载** aria-plugin, AD7) / Layer 2 工程师 (aria-runner 容器 + Claude Code + aria-plugin 完整加载, 执行完整十步循环)。两层用拟人命令 (自然语言 YAML) 通信, 非结构化 RPC (AD1 + AD6)。

**OpenSpec 需求规范**: Level 1 = Skip (简单修复) / Level 2 = `proposal.md` / Level 3 = `proposal.md` + `tasks.md`。

**协作原则**: 规范先行 (先 spec 后代码) / 小步迭代 (任务 4-8h 粒度) / 文档同步 (文档过时 = AI 误解) / 向后兼容 (破坏性变更须 MAJOR)。

## 信息地图

| 子模块/目录 | 职责 |
|-------------|------|
| `standards/` | 方法论定义 (十步循环 / OpenSpec / conventions) |
| `aria/` | 工具集 Plugin (Skills + Agents + Hooks) |
| `aria-plugin-benchmarks/` | Skill AB 基准测试 (固定套件 / 结果存档 / 运维手册) |
| `docs/handoff/` | Session handoff records (Rule #9 canonical) |
| `aria-orchestrator/` | v2.0 运行时 Layer 1/2 (仅 10CG Lab 内部) |

常用定位:

- 需求规范 → `standards/openspec/project.md` | 提交规范 → `standards/conventions/git-commit.md`
- Secret 卫生 → `standards/conventions/secret-hygiene.md` (Rule #7)
- 闸门权限归属 → `standards/conventions/configured-gate-authority.md` (Rule #10)
- Session handoff → `standards/conventions/session-handoff.md` (Rule #9; §1.3 周期 vs 会话收尾消歧)
- Rule #6 豁免判据 → `standards/conventions/skill-benchmark-exemption.md`
- 版本/tag 规则 → `standards/conventions/version-management.md` (§4.3 分发型 vs meta-repo)
- 其余 conventions (submodule-pointer / jq-CRLF / 并发写入安全等) → `standards/conventions/`
- 需求文档 → `docs/requirements/` | 架构文档 → `docs/architecture/system-architecture.md`
- 项目配置 → `.aria/config.json` (从 config.template.json 复制)
- AB 运维手册 → `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` | AB 结果 → `aria-plugin-benchmarks/ab-results/`

**Plugin 调用** (Aria 仓内直调; 其他项目经 Plugin 安装用 `/aria:` 前缀): Skills 如 `/state-scanner` `/spec-drafter` `/workflow-runner`; Agents 如 `/tech-lead` `/backend-architect` `/knowledge-manager`。

**子模块操作**: 更新 `git submodule update --remote [aria|standards]`; 首次 clone 后 `git submodule update --init --recursive`; 查状态 `git submodule status`。

**Forgejo API** (CF Access 后, 用 CLI wrapper `/home/dev/.npm-global/bin/forgejo`):

```bash
forgejo <METHOD> <ENDPOINT> [curl options]
forgejo GET /repos/10CG/Aria/pulls                                # 列出 PR
forgejo POST /repos/10CG/Aria/pulls -d '{"title":"...","head":"branch","base":"master"}'
```

## 技术约束

- Aria 定义「如何思考 / 如何协作 / 如何决策」+ 文档格式 / 流程 / 命名规范; **不提供**代码生成模板, 不强制语言, 不绑定 AI 模型, 不提供 CI/CD 配置。
- 例外: `aria-orchestrator/` 是方法论的**参考实现** (仅 10CG Lab 内部, 不对外发布, 不构成 Aria 对「实现」的背书)。

## 版本管理

- SemVer。Aria 约定: 新增 Skill / Skill 架构重构 = MINOR+; 文档更新 / bug 修复 = PATCH。
- **版本 SOT = `aria/.claude-plugin/plugin.json`**; 派生文件 (marketplace.json / VERSION / CHANGELOG.md / README.md) 必须与其一致。
- 发布同步面: aria 子模块 5 文件 + 主仓 gitlink + 主仓 VERSION + root README badge + i18n README (**仅正文实质变更**才重译, #140 B 档)。机械兜底: custom checks `m6-version-badge-match` / `i18n-readme-translation-currency`。
- Skill 变更发版前须过 Rule #6 benchmark。多远程推送由 phase-c-integrator §C.2.5 自动化 (post-push SHA 验证); 手工路径守下方两条硬约束。

### 多远程推送 — 两条硬约束 (owner 裁决 2026-07-20, 根治 Aria #165)

多远程一致靠**本地双推** (`git push origin && git push github`) 保证; #165 三次复发的根因都是有路径绕过了它。

**约束 1 — 子模块合并一律本地做, 禁止 Forgejo 服务端合并**: 子模块 (aria / standards / aria-orchestrator) 的分支合并必须本地 `git merge` + 双推, **禁**用 Forgejo Web UI / API 的 `Do: merge`。原因: 服务端合并的 merge commit 只在 Forgejo 生成, 本地 master 从未 fast-forward ⇒ 本地双推与 C.2.5 结构上都不触发, 主仓随后 bump gitlink 即产生 orphaned gitlink, GitHub `clone --recursive` 断裂 (2026-07-14 事故)。例外: 主仓 (Aria) 自身 PR 可走 Forgejo merge — 它没有「被 bump gitlink」的下游。

**约束 2 — 推后逐个 `ls-remote` 核验, 不信 push 回执**: 双推后对每个 remote 独立 `git ls-remote <remote> master` 取 SHA 与本地比对, **全部一致才算推成功**; push 退出码 / 回执两个方向都会骗人 (假阴性诱发误 force; 半推造成镜像分叉)。ls-remote 自身失败 → 重试几次再下结论。分叉后处置见 memory `feedback_partial_push_creates_mirror_divergence`。

## 不可协商规则

违背以下规则就不符合 Aria 方法论。每条详情见其 SOT, 此处只放判据本体:

1. **所有需求变更必须有 OpenSpec** — Level 2 或 Level 3。
2. **十步循环不能跳过 Phase A** — 先理解现状再行动。
3. **文档与代码必须同步更新** — 架构文档与代码一致。
4. **每个提交遵循 Conventional Commits**。
5. **项目变更放本项目 `openspec/changes/`** — 不放 `standards/openspec/changes/` (standards 是共享子模块, 变更属项目自身)。
6. **Skill 基准测试必须用 `/skill-creator`** (自研 runner 已废弃)。触发: 新增 Skill / 改逻辑 / 改 description / 发版审计。**豁免判据 = 内容是否影响 AI 行为 + 那个行为 AB 套件测不测得到** (不按文件目录判; 同文件两性质并存时逐 hunk 判):

| 内容性质 | AB 测得到吗 | 处置 |
|----------|------------|------|
| 描述性 (schema / 字段 / 命令 / 勘正) | 不适用 | substitute: SC 级 baseline-failing 结构化测试替代 |
| 处方性 · 运行时指令面 | 能 | 照跑 AB, 零裁量 |
| 处方性 · 套件覆盖外 (典型: authoring 向导) | 不能 | 点名行为 + 建可证伪定向 fixture + 套件缺口开 issue (缺一照跑) |
| 拿不准 | — | 照跑 (宁跑勿豁) |

   `description` 或指令流程变动一律照跑; 豁免须在 spec/tasks 留 `rule6_note`。跑 benchmark 本身不需要 OpenSpec。SOT: `standards/conventions/skill-benchmark-exemption.md` + 手册 `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md`。

7. **Secret 写入/读取命令必须 redirect output** — stdout/stderr 不得流入 chat-visible 通道 (Bash 强制 `>/dev/null 2>&1`; Python subprocess 强制 `capture_output=True` 且不 print)。验证用 metadata (status code / key 名 / 长度), 不读 secret value 字面。Exception 须 `# secret-leak-ok-explicit` + 理由 + owner sign-off。SOT: `standards/conventions/secret-hygiene.md`。
8. **PR merge 前必跑 pre-merge gate** — phase-c-integrator C.2.4 验证 (a) 本 PR CI passing; (b) main 无 in-flight CI run; 经 CI backend 抽象层调用 (Aether 默认)。无可用 backend 按 `no_ci_fallback` 显式降级; stub backend 抛 NotImplementedError 时 gate 必须 abort, 不得静默降级。SOT: `aria/skills/phase-c-integrator/SKILL.md §C.2.4`。
9. **Session handoff 必须写 `docs/handoff/`** — 禁 `.aria/handoff/` (零 exception; 5 层 enforcement)。两个正交入口: 周期收尾 (phase-d-closer, cycle 单元) vs 会话收尾 (session-closer, session 单元)。机读 frontmatter 5 字段; 多终端场景经 claim/reconcile advisory 协调 (phase1_gate)。SOT: `standards/conventions/session-handoff.md`。
10. **已启用的审计检查点不得由 AI 自行豁免** — enabled 闸门是 owner 的配置决定, 不是 AI 临场判断; 不得以「变更小 / Level 低 / 1:1 派生 / 性价比 / session 已长」等价值评估跳过、降级或改序。**豁免白名单 (仅四类, 封闭)**: config 显式 off / adaptive_rules 映射 / 已成文 lane 降级 / 结构性前提不成立 (审的对象整个未产生; 「存在但简单」不算)。AI 任何自作主张的流程判断必须写进 handoff 请复议。「跟踪 AI 判断准确率 → 放权」已否决, **不要再提议** (论证见规范 §4)。SOT: `standards/conventions/configured-gate-authority.md`。

## Aria 2.0 运行时

```
方法论层  standards/          ← 思考/协作/决策规范 (v1.x 不变)
工具层    aria-plugin (+ CC)  ← 交互式使用 + Layer 2 容器内嵌
运行时层  aria-orchestrator/  ← Layer 1 主管 + Layer 2 工程师 (仅 10CG Lab 内部)
```

v2.0 严格遵守全部 10 条不可协商规则 (由 Layer 2 内 aria-plugin 执行; 自主运行时无人复议, Rule #10 更硬)。人类参与点仅 1 个 (AD10): S7_AWAITING_MERGE 由产品负责人 Feishu 签字 merge。入口: [architecture-decisions.md](aria-orchestrator/docs/architecture-decisions.md) / [layer-boundary-contract.md](aria-orchestrator/docs/layer-boundary-contract.md) / [PRD v2.0](docs/requirements/prd-aria-v2.md) / [系统架构](docs/architecture/system-architecture.md)。

## 项目状态

```
当前阶段: v2.0 M6 执行中 (M1-M5 shipped)。168h 自主跑三门未清:
  - Blocker 3 输入投递: spec aria-2.0-m6-dispatch-input-delivery — B.2 实现完成
    (aria-orchestrator feature/m6-dispatch-input-delivery), 卡 C.2 合并于 4 owner/infra 门
  - Blocker 4: Luxeno 后端延迟 45-54s (owner/基建门)
  - 遥测 spec aria-2.0-m6-cost-model-telemetry — Track-1 实施完成
    (feature/m6-cost-model-telemetry, 合并 gate input-delivery); 168h AC-6 可评分须其独立 ship
  M6 release-closeout + M7 两 sub-Spec: Approved 待 Phase B (受门顺序, 详见各 proposal.md)
  aria-plugin 方法论轨: v1.52.0–v1.64.0 已 ship — 逐版本史见 aria/CHANGELOG.md (SOT);
    残余 deferred 挂 Aria #168; 并发 in-flight track 见 docs/handoff/latest.md
版本: 插件 aria-plugin v1.64.0 | 主项目 v1.7.3 | 运行时 aria-orchestrator v2.0.0 (86bb684)
  Layer 2 主力 LLM = glm-5.2 via Luxeno, Layer 1 = glm-4.5-air
```

进展查询: `/state-scanner` (live) | session 史 → `docs/handoff/` (Rule #9 canonical) | 版本史 → `aria/CHANGELOG.md` (SOT) | 活跃 spec 详情 → `openspec/changes/*/proposal.md`

**User Story 编号分区**: US-001~009 v1.x 已有 | US-010~019 v1.x 新增 | US-020~027 v2.0 待起草

---

**维护**: 10CG Lab | **主仓**: https://github.com/10CG/Aria | **插件**: https://github.com/10CG/aria-plugin | **规范**: https://github.com/10CG/aria-standards
