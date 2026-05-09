# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Track A — US-024 M4 T-deploy + smoke (2026-05-09 EOD)

production deploy + E2E smoke for Aria 2.0 M4 (US-024). Submodule bumps
(aria-orchestrator) capture 3 deploy-time production fixes; no Aria main
version bump (M4 logic ships via submodule).

#### Deploy artifacts
- aria-layer1-comment-poll deployed on Aether light-1 (5-field cron + `--continuous --interval 30 --max-iterations 2`, 30s effective cadence)
- aria-layer1-reconcile deployed (M3 carryover gap closed in Track A B2 scope)
- light-1 venv refresh: M2 v0.2.0 → M4 master + dispatches.db schema v1.1 → v3.0 (14 dispatches preserved, integrity ok)

#### Production fixes (aria-orchestrator submodule)
- `ec264f0` HCL cron 6-field → 5-field + `--continuous` fallback (Aether Nomad v1.7.7 6-field validate-passes-but-degrades-to-30min discovery; AD-M4-9 §风险 #2 path activated)
- `5467991` `_compute_feishu_signature` HMAC key/msg swap fix (Feishu code:19021 silent reject bug; +1 swap_regression test; existing test was reproducing the bug with same wrong formula)
- `834c313` m4-handoff.yaml Tier-2 partial writeback + t_deploy_status section + go_decision/rationale

#### Closeout
- m4-handoff.yaml validator OK ✅
- OD-M4-2 underbaseline retrospective signed off (28h actual / 60h baseline = 0.47, T-deploy added ~6h)
- Forgejo housekeeping: Issue #86 closed, PR #10 + #94 description amended (R3+R4 collapsed → R1-R5 owner-invoked CONVERGED), smoke PR #97 + branch deleted
- 6 incident memory entries (3 from Track A discovery: feishu_hmac_swap / nomad_cron_silent_degrade / handoff_doc_venv_ready_smell + 3 closeout patterns: smoke_dispatch_sql_inject / secret_env_inject_via_go_template / schema_migration_3_safeguard)

#### Pending (deferred, not blocking)
- Phase D.2 final go_decision: awaiting Tier-2 N≥3 real owner workload accumulation
- Task #42 secret rotation: 4 keys re-exposed in conversation 2026-05-02 + 2026-05-09, hard cap 2026-08-02
- M5 inputs filed: aria-layer1-cron 1h cadence vs SLO + aria-layer2-runner job missing (M2/M3 era infra gap)

### Planned
- 多 AI 平台兼容性 (US-003)
- US-007 Phase 3c: 半自动开发闭环 (v2.0.0)

---

## [1.6.0] - 2026-05-09

### Added — state-scanner-inter-cycle-surfacing (Spec 18 任务全实装)

aria-plugin v1.17.7 → v1.18.0 ship。Spec `state-scanner-inter-cycle-surfacing`
全部 18 任务通过 3 个 sub-PR 串行交付,每个 sub-PR 经 4-5 轮 multi-agent
pre_merge audit 收敛(详见各 sub-PR audit reports)。

#### Sub-PR (a) — TX.0 + TX.1 prerequisite (aria-plugin#37, merged 8ecee44)
- TX.0 `git.status_clean` derived field
- TX.1 `state-snapshot-schema.md` 4 nested-field sections + backward-compat contract
- TX.1.a `normalize_snapshot.py` DROP_KEYS for `raw_row` + `raw_match`
- TX.1.b 4 normalize tests
- 4 rounds R1-R4, R3==R4 converged, 4/4 PASS

#### Sub-PR (b) — G2 + G3 + G4 collectors (aria-plugin#38, merged 9242d8d)
- G2: `_parse_followups_table` (heading regex + column normalization +
  pipe-escape + BA-10 fullwidth space rejection)
- G3: `_detect_handoff_doc` (primary regex Chinese/English/Emoji + R2-converged
  fallback BA-02 form + 3-state path resolution)
- G4: `_derive_priority_items` (3-level stable sort + configurable limit +
  non-dict JSON guards)
- 2 new RECOMMENDATION_RULES: `pending_followups_p1` (1.85) +
  `resume_in_progress_us` (1.88)
- 32 new tests (24 initial + 8 R2 corrections)
- 5 rounds R1-R5, R4==R5 converged after 8 R2 corrections (2 Majors closed:
  schema doc-sync + handoff_doc absence contract)

#### Sub-PR (c) — TX.2 + TX.3 + TX.4 + TX.6 + TX.7 cleanup (aria-plugin#39, merged 5767fe3)
- TX.2 SKILL.md T5 兜底降级 (17 → ~9 lines sanity check)
- TX.3 three-arm AB benchmark (PASS — efficiency wins -70% tools / -24%
  duration vs A; findability tied at ceiling per memory precedent;
  Spec L218 negative fixtures × 2 added per R1 audit Major)
- TX.4 aria-plugin v1.17.7 → v1.18.0 + marketplace.json drift fix
- TX.6 4 backward-compat verify tests (defensive `.get()` patterns)
- TX.7 Aria + Kairos + Aether dogfooding (3 projects exit=0 errors=[])
- 4 rounds R1-R4, R3==R4 converged after R1 corrections (2 Majors closed:
  variance disclaimer + negative fixtures)

### Changed
- **aria submodule pointer**: 8ecee44 → 9242d8d → 5767fe3 (3 PR merges)
- **VERSION**: 1.5.0 → 1.6.0 + aria plugin reference 1.16.0 → 1.18.0
- **aria-plugin-benchmarks/ab-results/2026-05-09-state-scanner-inter-cycle-surfacing/**:
  full benchmark artifacts (12 trial outputs + benchmark.{json,md} +
  variance disclaimer)

### Aria methodology dogfooding outcomes
- 3 sub-PR 串行交付模式验证 (handoff doc 推荐的拆分方式)
- multi-agent convergence audit 模式累计 13 轮 audit-engine 调用
- 4-agent team (code-reviewer + backend-architect + qa-engineer +
  knowledge-manager) 共识机制有效 (R2 escalation + R3-R5 stability)
- 智能 PR scope 拆分 (sub-PR (a) 4 任务 / sub-PR (b) 9 任务 / sub-PR (c) 5 任务)
  避免单 PR review 压力

### Refs
- Spec: `openspec/changes/state-scanner-inter-cycle-surfacing/proposal.md`
  (Approved 2026-05-08 post_spec R2 PASS_WITH_WARNINGS, 4/4 vote)
- Issue: 10CG/Aria#85 (SilkNode inter-cycle surfacing forcing function)
- Audit reports: `.aria/audit-reports/pre_merge-R1-R{4,5,4}-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-{a,b,c}.md`
- Benchmark: `aria-plugin-benchmarks/ab-results/2026-05-09-state-scanner-inter-cycle-surfacing/benchmark.md`

---

## [1.4.2] - 2026-04-09

### Security
- **scan.sh 复杂度分析器安全加固** — 扩展安全关键词, 强制高危 issue tier=3
  - 原列表只有 `security` 一个安全词, 漏判 SQL injection/XSS/CVE/RCE 等
  - 新增 10+ 安全关键词: `vulnerabilit/cve/exploit/injection/xss/csrf/rce/sqli/auth bypass/privilege escalation/credential/secret leak/password leak/token leak/data leak`
  - 安全匹配现在是硬性规则, 任何命中强制 tier=3
  - 防止 Aria 2.0 自主 dispatch 模式下高危 issue 绕过人类审批

### Changed
- **scan.sh / heartbeat.sh 重命名 level → complexity_tier** — 消除与 OpenSpec Level 的语义冲突
  - JSON 字段: `complexity_level` → `complexity_tier`, `by_level` → `by_complexity_tier`, `level_N` → `tier_N`
  - 人类输出: `[Level N]` → `[Tier N]`
  - 新增注释明确 "Complexity Tier" 与 "OpenSpec Level" 是不同概念
  - 影响文件: `scan.sh`, `heartbeat.sh`, `schema/scan-result.json`, `skills/heartbeat-scan/SKILL.md`

### Docs
- **Aria 2.0 PRD** 初稿 (`docs/requirements/prd-aria-v2.md`)
  - 基于 5 轮 Agent Team 收敛讨论
  - 两层 AI 分工架构 (Hermes Layer 1 + 容器 Layer 2)
  - 12 项关键架构决策记录
  - 路线图 M0-M6 (~750h / 9 月 50% 投入)

---

## [1.4.1] - 2026-04-09

### Added
- **心跳执行日志** — 每次心跳追加到 `.aria/heartbeat-log/{date}.log`
  - 记录: 时间戳, 扫描模式, issue 数量, 分级统计, 通知结果
  - silent 模式 (0 issues) 也记录，确保完整审计轨迹
  - notify 失败时附带 `err=` 错误详情
- **扫描级熔断机制** — 连续 3 次心跳失败自动暂停
  - 创建 `.aria/heartbeat-breaker` + 飞书告警
  - 手动恢复: 删除 breaker + fail-count 文件
  - 计数文件健壮性: 非数字内容自动重置

### Fixed
- heartbeat.sh python3 消息构建增加异常防护 (set -e 下不再静默中断)

---

## [1.4.0] - 2026-04-08

### Added
- **aria-orchestrator 子模块** — 外部编排器 Phase 3b 完成 (US-007)
  - Hermes Agent 心跳扫描 (60m 间隔, GLM-4.5-Air, 零成本)
  - 飞书 (Feishu) 通知集成 — WebSocket gateway E2E 验证
  - Aether Nomad 部署 (raw_exec driver, light-1 节点)
  - heartbeat-scan Skill + scan.sh 确定性扫描器
- **US-006 自定义健康检查** — state-scanner v2.8.0 完成

### Changed
- **US-007 Phase 3b-M1~M3 全部完成** — 从 scan-only 到飞书心跳通知
- **OpenSpec aria-orchestrator** — Status: Draft → In Progress
- **Hermes 运行时验证**: cron 调度 + 消息网关 + FTS5 memory

### Fixed
- GLM-4.7-Flash 429 限流 → 切换 GLM-4.5-Air (中文输出优化)
- Feishu 集成 6 项必要配置 (D17-D22 gotchas 文档化)
- heartbeat SILENT 模式 + 60m 间隔调整

---

## [1.3.0] - 2026-04-03

### Added
- **aria-dashboard Skill** (aria-plugin v1.10.0) — 项目进度看板生成器
  - 5 数据解析器: UPM, Stories, OpenSpec, Audit Reports, AB Benchmark
  - 单文件自包含 HTML 模板 (深色主题, 响应式, 零 CDN)
  - 跨项目兼容: UPM 双格式, Story 中英文字段, 任意 ID 前缀
  - Issue 存储适配器设计 (Phase 2 提前准备)
- **架构文档** v1.7.0 — Dashboard 可视化子系统, Skills 32→33

### Changed
- **US-005 Phase 1 完成** — 看板 Skill 已交付, Phase 2-3 待实施
- **aria 子模块** — 更新至 v1.10.0 (30 user-facing + 3 internal Skills)

---

## [1.2.0] - 2026-04-02

### Added
- **自动审计系统** (US-004, aria-plugin v1.9.0)
  - audit-engine Skill: convergence/challenge 双模式多轮收敛审计
  - 7 个审计检查点覆盖十步循环全流程
  - config-loader 旧配置兼容映射
  - state-scanner v2.7.0 审计状态扫描 + adaptive 路由
  - AB benchmark: delta +0.5 (WITH_BETTER)
  - 3 轮循环审计验证 OpenSpec (4 agents x 3 rounds, 25+ issues 修正)
- **架构文档** v1.6.0 — 审计子系统章节, Skills 30→32

### Changed
- **US-004 自动审计系统** — 标记 done
- **aria 子模块** — 更新至 v1.9.0 (29 user-facing + 3 internal Skills)

---

## [1.1.0] - 2026-04-01

### Added
- **aria-report Skill** (aria-plugin v1.8.0) — Issue 报告与反馈 (Bug/Feature/Question)
  - AB benchmark: delta +0.375 (WITH_BETTER)
  - 自动环境收集、隐私审查、三级提交路由
- **跨项目 Benchmark 框架** — `CROSS_PROJECT_BENCHMARKING.md` + `external/` 目录
- **GitHub Issue Templates** — Adoption Report + Adaptation Issue (aria-plugin)
- **Quick Start 指南** — 10 分钟零到工作流 (EN + ZH, aria-plugin)
- **Standards 独立使用指南** — 不依赖 aria-plugin 的使用文档 (EN + ZH)

### Changed
- **US-001 增强工作流自动化** — 标记 done (4/4 验收标准达成, auto-proceed ~80% 步骤减少)
- **US-002 跨项目方法论验证** — 标记 done (Kairos 试点完成, Adoption Report 已提交)

### Research Findings
- **Process vs Content Skills 可移植性模型**: Process Skills (state-scanner +0.25, aria-report +0.375) 跨项目价值高于 Content Skills (commit-msg 0.0, spec-drafter 0.0)
- Kairos 试点零适配需求 — Aria 工具链开箱即用

---

## [1.0.5] - 2026-04-01

### Changed
- **aria 子模块** — 更新至 v1.8.0
  - 新增 aria-report Skill (Issue 报告与反馈)
  - AB benchmark: delta +0.375 (WITH_BETTER)
  - Skills 数量: 28 面向用户 + 2 内部 = 30
- **架构文档** — system-architecture.md v1.5.1→v1.5.2, Skills 29→30
- **版本文件** — VERSION 内部版本号不一致修复 (1.0.2→1.0.5)
- **OpenSpec 归档** — aria-report-skill, readme-i18n-upgrade

---

## [1.0.4] - 2026-03-21

### Added
- **MIT LICENSE 文件** — 修复 README 中的死链
- **多语言 README** — 英文 (默认)、中文、日文占位、韩文占位
  - 主项目: README.md (EN) + README.zh.md + README.ja.md + README.ko.md
  - aria-plugin: README.md (EN) + README.zh.md
  - aria-standards: README.md (EN) + README.zh.md
- **GitHub 仓库公开** — 三个仓库均设为 public，配置 About/Topics

### Changed
- **aria 子模块** — 更新至 v1.7.2 最新提交
  - Skills 数量修正: 27 面向用户 + 2 内部 (arch-common, config-loader)
  - Hooks 描述修正: 仅 SessionStart (中断恢复检测)
  - plugin.json/marketplace.json 描述同步更新
  - VERSION 发布日期和 Patch 说明修正
- **standards 子模块** — README 国际化 + 目录结构修正
  - 修正 openspec/ 目录结构 (移除不存在的 changes/archive/)
  - 补全 conventions/ (6 文件)、templates/ (3 文件)
  - 添加 core/documentation/ 目录
- **CLAUDE.md 同步更新**
  - 插件版本 v1.7.0 → v1.7.2
  - hooks.json 路径 .claude-plugin/ → hooks/
  - 移除版本检查清单中过时的 hooks.json version 条目
  - 仓库 URL Forgejo → GitHub
  - 目录导航 aria-proposal.md → aria-brand-guide.md

### Fixed
- **全项目 Forgejo URL 清理** — 所有文档中的 forgejo.10cg.pub 替换为 github.com/10CG
  - 影响: CHANGELOG.md, .claude/local.md, system-architecture.md, migration-guide.md,
    aria-vs-superpowers-comparison.md, openspec/project.md, version-management.md,
    release-notes/, openspec/archive/ 等
- **OpenSpec 路径修正** — README 中 `standards/openspec/changes/` → `openspec/changes/` (符合 CLAUDE.md 规则 #5)
- **安装命令大小写** — `10cg-aria-plugin` → `10CG-aria-plugin`
- **Skills 数量统一** — 全项目统一为 29 Skills (27 面向用户 + 2 内部)
- **GitHub 仓库 About 配置** — Description, Homepage, Topics 设置完成

---

## [1.0.3] - 2026-02-07

### Changed
- **aria 子模块** — 更新至 v1.4.0
  - **两阶段代码审查** — Superpowers 风格的代码审查机制
    - 新增 `aria:code-reviewer` Agent — Phase 1 (规范合规性) + Phase 2 (代码质量)
    - 新增 `requesting-code-review` Skill — 用户可调用入口
    - **subagent-driver** 集成两阶段审查 — 新增 `enable_two_phase` 参数 (默认: true)
    - 审查结果分类: Critical (必须修复) / Important (应该修复) / Minor (建议修复)
  - **Skills 总数**: 25 → 26
  - **Agents 总数**: 10 → 11

---

## [1.0.2] - 2026-02-06

### Changed
- **aria 子模块** — 更新至 v1.3.2
  - brainstorm v2.0.0: 基于 Superpowers 最佳实践重构对话流程
  - 新增"不可协商规则"强制对话控制
  - 修复 AI 跳过对话直接生成 User Stories 的问题

---

## [1.0.1] - 2026-02-06

### Changed
- **aria 子模块** — 更新至 v1.3.1
  - state-scanner: 新增跨平台兼容性指南
  - 新增 references/cross-platform-commands.md
  - Progressive Disclosure 优化 (SKILL.md 精简至 1,362 词)

---

## [1.0.0] - 2026-01-23

### Added
- **版本管理系统**: VERSION 文件 + Git Tag 规范
- **版本管理规范**: `standards/conventions/version-management.md`
- **十步循环工作流**: 完整的 AI 协作流程定义
  - A.0 状态扫描 (state-scanner)
  - A.1 规范创建 (spec-drafter)
  - A.2 任务规划 (task-planner)
  - A.3 Agent 分配
  - B.1 分支管理 (branch-manager)
  - B.2 执行验证 (subagent-driver)
  - B.3 架构同步 (arch-update)
  - C.1 提交 (strategic-commit-orchestrator)
  - C.2 合并 (PR 创建)
  - D.1 进度更新 (progress-updater)
  - D.2 归档
- **OpenSpec v2.1.0**: 标准化需求规范格式
  - Level 1 (Skip): 简单修复
  - Level 2 (Minimal): proposal.md
  - Level 3 (Full): proposal.md + tasks.md
- **Skills 框架**: 20+ 工作流单元
- **Agents**: 专业领域代理 (tech-lead, backend-architect, etc.)
- **强制执行机制** (v1.2.0): branch-manager v2.0, subagent-driver, branch-finisher
- **Hooks 系统**: SessionStart 生命周期事件自动化
- **文档系统**: CLAUDE.md, System Architecture, 方法论文档
- **aria-plugin**: Plugin Marketplace 分发方式

### Changed
- 优化 OpenSpec 目录结构 (项目 vs 规范定义)
- 更新插件安装方式为 marketplace 模式

### Fixed
- 修正 marketplace 命令格式
- 修正 Agents 安装来源文档

### Documentation
- 添加强制执行机制分析文档
- 添加 Superpowers vs Aria 对比分析
- 完善十步循环各阶段文档

---

## Version History

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.4 | 2026-03-21 | README 国际化、GitHub 公开、全项目文档修正 |
| 1.0.3 | 2026-02-07 | aria 子模块更新至 v1.4.0 (两阶段代码审查) |
| 1.0.2 | 2026-02-06 | aria 子模块更新至 v1.3.2 (brainstorm v2.0.0) |
| 1.0.1 | 2026-02-06 | aria 子模块更新至 v1.3.1 |
| 1.0.0 | 2026-01-23 | 首个正式发布 |

---

[Unreleased]: https://github.com/10CG/Aria/compare/v1.4.2...HEAD
[1.4.2]: https://github.com/10CG/Aria/compare/v1.4.1...v1.4.2
[1.4.1]: https://github.com/10CG/Aria/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/10CG/Aria/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/10CG/Aria/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/10CG/Aria/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/10CG/Aria/compare/v1.0.5...v1.1.0
[1.0.5]: https://github.com/10CG/Aria/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/10CG/Aria/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/10CG/Aria/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/10CG/Aria/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/10CG/Aria/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/10CG/Aria/releases/tag/v1.0.0
