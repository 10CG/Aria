# Aria Skills

> Aria AI-DDD 方法论配套的 Claude Code Skills

## 安装方式

### 方式一: Plugin Marketplace (推荐)

```bash
# 添加 marketplace
/plugin marketplace add 10CG/aria-skills

# 安装完整 Skills
/plugin install all-skills@10cg-aria-skills

# 或选择性安装
/plugin install aria-core@10cg-aria-skills           # 十步循环核心
/plugin install git-tools@10cg-aria-skills           # Git 工作流
/plugin install arch-tools@10cg-aria-skills          # 架构文档
/plugin install requirements-tools@10cg-aria-skills  # 需求管理
```

### 方式二: 手动克隆到 Personal Skills

```bash
# Linux/macOS
git clone ssh://forgejo@forgejo.10cg.pub/10CG/aria-skills ~/.claude/skills

# Windows
git clone ssh://forgejo@forgejo.10cg.pub/10CG/aria-skills %USERPROFILE%\.claude\skills
```

## Plugin 分组

| Plugin | 包含 Skills | 描述 |
|--------|------------|------|
| `aria-core` | state-scanner, workflow-runner, phase-*, spec-drafter, task-planner, progress-updater | 十步循环核心 |
| `git-tools` | commit-msg-generator, strategic-commit-orchestrator, branch-manager | Git 工作流 |
| `arch-tools` | arch-common, arch-search, arch-update, arch-scaffolder, api-doc-generator | 架构文档 |
| `requirements-tools` | requirements-validator, requirements-sync, forgejo-sync | 需求管理 |
| `all-skills` | 以上全部 (20 个 Skills) | 完整安装 |

## Skills 列表

### Git 工具

| Skill | 描述 |
|-------|------|
| commit-msg-generator | 单模块简单变更的提交消息生成 |
| strategic-commit-orchestrator | 跨模块/批量/里程碑提交 |
| branch-manager | 分支创建与 PR 管理 |

### 架构文档

| Skill | 描述 |
|-------|------|
| arch-common | 架构工具共享组件 |
| arch-search | 搜索架构文档 |
| arch-update | 更新架构文档 |
| arch-scaffolder | 从 PRD 生成架构骨架 |
| api-doc-generator | API 文档生成 |

### Aria 十步循环

| Skill | 描述 |
|-------|------|
| phase-a-planner | Phase A 规划 |
| phase-b-developer | Phase B 开发 |
| phase-c-integrator | Phase C 集成 |
| phase-d-closer | Phase D 收尾 |

### 进度管理

| Skill | 描述 |
|-------|------|
| progress-updater | 更新 UPM 状态 |
| spec-drafter | 创建 OpenSpec |
| task-planner | 任务规划 |
| state-scanner | 项目状态扫描 |
| workflow-runner | 工作流编排执行 |

### 需求管理

| Skill | 描述 |
|-------|------|
| requirements-validator | PRD/Story/Architecture 验证 |
| requirements-sync | Story ↔ UPM 状态同步 |
| forgejo-sync | Story ↔ Issue 同步 |

## 使用方式

安装后，所有项目自动继承这些 Skills。

项目特定的 Skills 放在项目的 `.claude/skills/` 目录，会覆盖同名的 Personal Skills。

## 相关项目

- [ai-dev-standards](https://forgejo.10cg.pub/10CG/ai-dev-standards) - Aria AI-DDD 方法论规范
- [todo-app](https://forgejo.10cg.pub/10CG/todo-app) - 示例项目
- [nexus](https://forgejo.10cg.pub/10CG/nexus) - AI 认知服务平台

## License

Proprietary - 10CG
