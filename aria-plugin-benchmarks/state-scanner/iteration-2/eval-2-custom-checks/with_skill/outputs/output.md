╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/us-006-custom-health-checks
  模块: Aria (方法论研究项目)
  Phase/Cycle: US-006 in_progress
  变更: 1 文件 (untracked: .aria/state-checks.yaml)
  未提交: 无暂存变更

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: 配置文件 (config)
  复杂度: Level 1
  架构影响: 无
  测试覆盖: N/A (配置文件)
  Skill 变更: 无 SKILL.md 变更检测

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: 已配置
  PRD: prd-aria-v1.md (Active)
  User Stories: 6 个 (done: 3, in_progress: 2, pending: 1)
    - US-001: done
    - US-002: done
    - US-003: pending
    - US-004: done
    - US-005: in_progress
    - US-006: in_progress
  OpenSpec 覆盖: 6/6 (100%)

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: 存在
  路径: docs/architecture/system-architecture.md
  状态: Active | 版本: 1.7.0 | 最后更新: 2026-04-03
  Parent PRD: prd-aria-v1.md
  需求链路: 完整

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 2 个 | 已归档: 36 个 | 待归档: 1 个
  活跃变更详情:
    - aria-dashboard: In Progress (Phase 1 Complete, Phase 2-3 Pending)
    - custom-health-checks: In Progress
  待归档警告:
    - aria-dashboard: Status 包含 "Complete" (Phase 1)，建议归档已完成部分

📖 README 同步检查
───────────────────────────────────────────────────────────────
  根目录 README.md:
    版本号: Plugin-v1.8.0 (不一致 — plugin.json 为 v1.10.0)
    建议: 更新 README.md 插件版本号为 v1.10.0
  aria/README.md:
    版本号: 1.10.0 (一致)

📦 插件依赖检测
───────────────────────────────────────────────────────────────
  standards 子模块: 已注册且已初始化
  aria 子模块: 已注册且已初始化
  子模块状态: 均与当前指针一致 (无 '+' 前缀)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: 有审计报告存在
  最近审计: post_spec — convergence 模式
    时间: 2026-04-01T23:00:00Z
    上下文: openspec/changes/auto-audit-system/proposal.md
    轮次: 3
    收敛: 未收敛 (1 PASS / 3 REVISE, trend converging)
    严重阻塞 Issues: 4 项 (收敛判定算法缺失、汇总引擎未定义、Severity 体系缺失、challenge 模式 schema 缺失)
  未收敛警告: 存在未收敛审计报告，建议处理后再继续相关工作

🔧 自定义检查
───────────────────────────────────────────────────────────────
  配置文件: .aria/state-checks.yaml (已检测, version: "1")
  检查项总数: 2 | 通过: 2 | 失败: 0

  ✅ submodule-freshness: OK [severity: warning]
     描述: Check if git submodules are up to date with remote
     修复建议: git submodule update --remote

  ✅ changelog-version-match: OK [severity: error]
     描述: Check if CHANGELOG latest entry matches plugin version
     修复建议: Update CHANGELOG.md to match plugin.json version

  总结: 全部自定义检查通过

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  当前状态分析:
  - 分支 feature/us-006-custom-health-checks 对应 US-006 (in_progress)
  - 工作区仅有 1 个 untracked 配置文件
  - 无暂存/未暂存的代码变更
  - 根 README 版本号与 plugin.json 不一致 (v1.8.0 vs v1.10.0)
  - 存在 1 个未收敛审计报告 (auto-audit-system)
  - 自定义检查全部通过

  ➤ [1] commit_only (推荐)
      理由: 仅有配置文件变更，可直接提交 .aria/state-checks.yaml
  ○ [2] quick-fix
      理由: 修复根 README 版本号不一致 (v1.8.0 -> v1.10.0)
  ○ [3] feature-dev (继续 US-006)
      理由: US-006 custom-health-checks 仍在 in_progress，可继续开发
  ○ [4] 自定义组合

🤔 选择 [1-4] 或输入自定义:
