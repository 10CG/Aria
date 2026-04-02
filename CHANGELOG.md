# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- 多 AI 平台兼容性 (US-003)

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

[Unreleased]: https://github.com/10CG/Aria/compare/v1.0.4...HEAD
[1.0.4]: https://github.com/10CG/Aria/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/10CG/Aria/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/10CG/Aria/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/10CG/Aria/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/10CG/Aria/releases/tag/v1.0.0
