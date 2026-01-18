# Aria 项目配置

> **Claude Code 项目级配置**
> **版本**: 1.0.0
> **更新**: 2026-01-18

---

## 自动触发规则 (Auto-Trigger Rules)

当用户请求中包含以下关键词时，自动激活对应的 Skill：

### 测试相关

| 关键词 | 触发 Skill | 置信度 |
|--------|-----------|--------|
| `test`, `测试`, `单元测试` | `tdd-enforcer` | 0.9 |
| `tdd`, `test-driven` | `tdd-enforcer` | 1.0 |
| `coverage`, `覆盖率` | `tdd-enforcer` | 0.8 |
| `spec`, `规范`, `proposal` | `spec-drafter` | 0.85 |

### Git 相关

| 关键词 | 触发 Skill | 置信度 |
|--------|-----------|--------|
| `branch`, `分支`, `创建分支` | `branch-manager` | 0.9 |
| `commit`, `提交` | `commit-msg-generator` | 0.8 |
| `pr`, `pull request`, `合并` | `branch-manager` (C.2) | 0.85 |
| `worktree` | `branch-manager` (worktree) | 1.0 |

### 规划相关

| 关键词 | 触发 Skill | 置信度 |
|--------|-----------|--------|
| `plan`, `规划`, `任务` | `task-planner` | 0.85 |
| `state`, `状态`, `进度` | `state-scanner` | 0.9 |
| `workflow`, `工作流`, `执行` | `workflow-runner` | 0.8 |

### 开发相关

| 关键词 | 触发 Skill | 置信度 |
|--------|-----------|--------|
| `develop`, `开发`, `实现` | `phase-b-developer` | 0.75 |
| `review`, `评审`, `审查` | `phase-b-developer` (review) | 0.85 |
| `integrate`, `集成` | `phase-c-integrator` | 0.8 |
| `close`, `收尾`, `完成` | `phase-d-closer` | 0.8 |

### 架构相关

| 关键词 | 触发 Skill | 置信度 |
|--------|-----------|--------|
| `arch`, `架构`, `设计` | `arch-update` | 0.8 |
| `arch search`, `查找`, `定位` | `arch-search` | 0.85 |
| `arch scaffold`, `骨架` | `arch-scaffolder` | 0.9 |

### 文档相关

| 关键词 | 触发 Skill | 置信度 |
|--------|-----------|--------|
| `progress update`, `进度更新` | `progress-updater` | 0.9 |
| `validate`, `验证`, `检查` | `requirements-validator` | 0.8 |

---

## 匹配策略

```yaml
算法: 模糊匹配 + 置信度阈值

触发条件:
  - 关键词匹配 >= 0.8 置信度 → 自动激活
  - 关键词匹配 0.6-0.8 置信度 → 提示确认
  - 关键词匹配 < 0.6 置信度 → 不触发

多关键词匹配:
  - 取最高置信度
  - 累积匹配 (同一 Skill 多个关键词) +0.1 加成
```

---

## 项目结构

```
Aria/
├── .claude/
│   ├── CLAUDE.md          # 本配置文件
│   ├── agents/            # Agents (子模块)
│   ├── skills/            # Skills (子模块)
│   └── trigger-rules.json # 自动触发规则
├── aria/
│   └── hooks/             # Hooks 系统
├── backend/               # Python FastAPI 后端
├── mobile/                # Flutter 应用
├── shared/                # API 契约、schemas
├── standards/             # AI-DDD 规范 (子模块)
└── docs/                  # 项目文档
```

---

## 模块上下文

### Backend (Python/FastAPI)
- 主要目录: `backend/src/`
- 测试目录: `backend/tests/`
- 数据库迁移: `backend/migrations/`
- OpenAPI: `backend/openapi.json`

### Mobile (Flutter)
- 主要目录: `mobile/lib/`
- 测试目录: `mobile/test/`
- 资源: `mobile/assets/`

### Standards (子模块)
- OpenSpec: `standards/openspec/`
- 工作流: `standards/workflow/`
- 核心: `standards/core/`

---

## 默认行为

### 开发任务默认流程

当用户请求开发功能时，按以下流程引导：

1. **A.0 状态扫描** → `state-scanner`
2. **A.1 规范创建** → `spec-drafter` (如需要)
3. **A.2 任务规划** → `task-planner`
4. **B.1 分支创建** → `branch-manager`
5. **B.2 开发执行** → `phase-b-developer`
6. **C.1 提交** → `commit-msg-generator`
7. **C.2 集成** → `phase-c-integrator`
8. **D.1 进度更新** → `progress-updater`

### Bugfix 默认流程

当用户报告 bug 时，按以下流程引导：

1. **问题确认** → 理解问题
2. **分支创建** → `branch-manager` (bugfix)
3. **测试编写** → `tdd-enforcer` (RED)
4. **修复实现** → `tdd-enforcer` (GREEN)
5. **提交推送** → `commit-msg-generator`
6. **PR 创建** → `branch-manager` (C.2)

---

## 禁用自动触发

如果需要禁用自动触发功能，在请求前添加：

```
NO_AUTO_TRIGGER
```

或设置环境变量：
```bash
export CLAUDE_AUTO_TRIGGER=false
```

---

## 相关文档

- [十步循环概览](standards/core/ten-step-cycle/README.md)
- [Skill 目录](.claude/skills/)
- [Workflow Enhancement](standards/openspec/changes/aria-workflow-enhancement/proposal.md)

---

**版本**: 1.0.0
**最后更新**: 2026-01-18
**维护**: Aria Team
