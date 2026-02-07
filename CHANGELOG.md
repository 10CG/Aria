# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- 工作流自动化增强
- 扩展到更多 AI 平台

---

## [1.0.3] - 2026-02-07

### Changed
- **aria 子模块** - 更新至 v1.4.0
  - **两阶段代码审查** - Superpowers 风格的代码审查机制
    - 新增 `aria:code-reviewer` Agent - Phase 1 (规范合规性) + Phase 2 (代码质量)
    - 新增 `requesting-code-review` Skill - 用户可调用入口
    - **subagent-driver** 集成两阶段审查 - 新增 `enable_two_phase` 参数 (默认: true)
    - 审查结果分类: Critical (必须修复) / Important (应该修复) / Minor (建议修复)
  - **Skills 总数**: 25 → 26
  - **Agents 总数**: 10 → 11

---

## [1.0.2] - 2026-02-06

### Changed
- **aria 子模块** - 更新至 v1.3.2
  - brainstorm v2.0.0: 基于 Superpowers 最佳实践重构对话流程
  - 新增"不可协商规则"强制对话控制
  - 修复 AI 跳过对话直接生成 User Stories 的问题

---

## [1.0.1] - 2026-02-06

### Changed
- **aria 子模块** - 更新至 v1.3.1
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
  - state-scanner: 状态感知与智能推荐
  - spec-drafter: OpenSpec 草稿生成
  - task-planner: 任务分解与规划
  - phase-a/b/c/d-planner: 各阶段编排
  - arch-search: 架构文档搜索
  - arch-update: 架构文档同步
  - tdd-enforcer: TDD 强制执行
  - forgejo-sync: Forgejo Issue 同步
  - requirements-validator: 需求文档验证
  - workflow-runner: 工作流执行器
- **Agents**: 专业领域代理
  - tech-lead: 技术架构决策
  - backend-architect: 后端架构设计
  - api-documenter: API 文档生成
  - ai-engineer: AI 应用开发
  - mobile-developer: 移动应用开发
  - knowledge-manager: 知识库管理
  - context-manager: 上下文管理
- **强制执行机制** (v1.2.0):
  - branch-manager v2.0: 自动模式决策 (Branch vs Worktree)
  - subagent-driver v1.0: 逐任务执行 + 上下文隔离
  - branch-finisher v1.0: 测试前置验证 + 完成流程
  - 双重隔离策略 (L1/L2/L3)
  - 5因子评分算法
- **Hooks 系统**: 生命周期事件自动化
  - PreToolUse: TDD 流程验证
  - PostToolUse: 文档同步
  - SessionStart/Stop: 环境初始化/清理
- **文档系统**:
  - CLAUDE.md: AI 认知框架
  - System Architecture: v1.2.0
  - 方法论文档: 十步循环、OpenSpec、UPM
- **aria-plugin**: Plugin Marketplace 分发方式

### Changed
- 优化 OpenSpec 目录结构 (项目 vs 规范定义)
- 更新插件安装方式为 marketplace 模式
- 重构 agents 和 skills 为独立子模块

### Fixed
- 修正 marketplace 命令格式
- 修正 Agents 安装来源文档

### Documentation
- 添加强制执行机制分析文档
- 添加 Superpowers vs Aria 对比分析
- 完善十步循环各阶段文档
- 添加 Skills/Agents 使用指南

---

## Version History

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.3 | 2026-02-07 | aria 子模块更新至 v1.4.0 (两阶段代码审查) |
| 1.0.2 | 2026-02-06 | aria 子模块更新至 v1.3.2 (brainstorm v2.0.0) |
| 1.0.1 | 2026-02-06 | aria 子模块更新至 v1.3.1 |
| 1.0.0 | 2026-01-23 | 首个正式发布 |

---

[Unreleased]: https://forgejo.10cg.pub/10CG/Aria/compare/v1.0.3...HEAD
[1.0.3]: https://forgejo.10cg.pub/10CG/Aria/releases/tag/v1.0.3
[1.0.2]: https://forgejo.10cg.pub/10CG/Aria/releases/tag/v1.0.2
[1.0.1]: https://forgejo.10cg.pub/10CG/Aria/releases/tag/v1.0.1
[1.0.0]: https://forgejo.10cg.pub/10CG/Aria/releases/tag/v1.0.0
