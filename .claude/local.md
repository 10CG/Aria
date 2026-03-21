# Aria - AI 工作流配置

> **用途**: Claude Code 的工作指令
> **更新**: 2026-01-18
> **说明**: 本文件定义 AI 在 Aria 项目中的行为模式

---

## 工作流入口规则

```
所有任务必须从 A.0 状态扫描开始:

用户: "我要开发一个新功能"
   ↓
/state-scanner → 分析当前状态 → 推荐下一步
   ↓
用户确认 → 执行对应 Phase
```

**关键原则**: 不要跳过状态扫描，AI 需要先理解"在哪"才能建议"去哪"。

---

## 自动触发映射

| 用户意图关键词 | 调用技能 | 时机 |
|----------------|----------|------|
| `state` / `状态` / `进度` / `扫描` | state-scanner | 任务开始 |
| `spec` / `规范` / `proposal` | spec-drafter | 需要规范 |
| `plan` / `规划` / `任务` / `分解` | task-planner | 规划任务 |
| `branch` / `分支` / `worktree` | branch-manager | 创建分支 |
| `test` / `测试` / `tdd` | tdd-enforcer | 测试驱动 |
| `commit` / `提交` | commit-msg-generator | 提交代码 |
| `arch` / `架构` / `设计文档` | arch-search / arch-update | 架构工作 |
| `progress` / `进度更新` | progress-updater | 更新状态 |

```
禁用: 请求前加 NO_AUTO_TRIGGER
```

---

## 十步循环技能映射

```
A. 规划阶段
├── A.0 → state-scanner
├── A.1 → spec-drafter
├── A.2 → task-planner
└── A.3 → task-planner (内嵌)

B. 开发阶段
├── B.1 → branch-manager
└── B.2 → phase-b-developer (含两阶段评审)

C. 集成阶段
├── C.1 → commit-msg-generator
└── C.2 → branch-manager

D. 收尾阶段
├── D.1 → progress-updater
└── D.2 → phase-d-closer
```

---

## 不可协商规则

AI 在工作中**必须遵守**的规则:

1. **需求变更必须有 OpenSpec** - Level 2 或 Level 3
2. **不能跳过 Phase A** - 必须先状态扫描
3. **架构文档必须同步** - 代码变更时更新文档
4. **提交遵循规范** - Conventional Commits 格式

---

## 子模块引用

详细规范和技能定义:

| 需要了解 | 查看位置 |
|----------|----------|
| 项目本质 | `CLAUDE.md` (根目录) |
| 十步循环 | `standards/core/ten-step-cycle/` |
| OpenSpec | `standards/openspec/project.md` |
| 技能定义 | `.claude/skills/*/SKILL.md` |
| 提交规范 | `standards/conventions/git-commit.md` |

---

## 术语表

| 术语 | 含义 |
|------|------|
| AI-DDD | AI 辅助的领域驱动设计 |
| OpenSpec | 标准化需求规范格式 |
| 十步循环 | Aria 的结构化工作流 |
| Phase | 工作流的阶段 (A/B/C/D) |
| Skill | 工作流的执行单元 |
| Level 1/2/3 | OpenSpec 的规范级别 |

---

## 开发模式

### TDD 模式 (测试驱动)

```
RED → GREEN → REFACTOR

触发: "测试" / "test" / "tdd"
技能: tdd-enforcer
```

### Worktree 模式 (并行开发)

```
git worktree add .git/worktrees/TASK-XXX

触发: "worktree" / "并行开发"
技能: branch-manager (worktree 支持)
```

---

**维护**: 10CG Lab
**仓库**: https://github.com/10CG/Aria
