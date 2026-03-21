# Aria Workflow Enhancement 迁移指南

> **版本**: 1.0.0
> **来源**: TASK-028
> **提案**: aria-workflow-enhancement

---

## 目录

1. [概述](#概述)
2. [迁移前准备](#迁移前准备)
3. [功能迁移步骤](#功能迁移步骤)
4. [验证清单](#验证清单)
5. [回滚方案](#回滚方案)
6. [常见问题](#常见问题)

---

## 概述

本文档指导现有 Aria 用户平滑迁移到新的工作流程增强功能。

### 新功能概览

| 功能 | 说明 | 是否必须 |
|------|------|----------|
| **TDD Enforcer** | 强制测试驱动开发 | ❌ 可选 |
| **Git Worktrees** | 隔离开发环境 | ❌ 可选 |
| **自动触发** | 意图识别自动激活 Skill | ❌ 可选 |
| **两阶段评审** | 规范→质量递进检查 | ❌ 可选 |
| **Hooks 系统** | 关键节点自动验证 | ❌ 可选 |

### 迁移原则

- ✅ **渐进式** - 可以逐步启用各个功能
- ✅ **向后兼容** - 现有工作流程不受影响
- ✅ **可选启用** - 每个功能都有独立开关
- ✅ **安全回滚** - 可以随时禁用任何功能

---

## 迁移前准备

### 1. 环境检查

```bash
# 检查 Git 版本 (需要 >= 2.30)
git --version

# 检查 Bash 可用性
bash --version

# 检查 Python (可选，用于 hooks 验证)
python3 --version
```

### 2. 备份当前配置

```bash
# 备份现有配置
cp .claude/CLAUDE.md .claude/CLAUDE.md.backup  # 如果存在

# 记录当前 Git 配置
git config --local --list > git-config-backup.txt
```

### 3. 了解新功能

阅读相关文档：

1. [TDD Enforcer](../../.claude/skills/tdd-enforcer/SKILL.md)
2. [自动触发指南](../docs/workflow/auto-trigger-guide.md)
3. [Hooks 系统](../aria/hooks/README.md)

---

## 功能迁移步骤

### 步骤 1: 更新 Skills 子模块

```bash
# 进入 standards 子模块
cd standards

# 拉取最新更新
git fetch origin
git checkout master
git pull origin master

# 返回主仓库
cd ..

# 更新子模块指针
git add standards
git commit -m "chore: update skills submodule"
```

### 步骤 2: 启用自动触发（推荐）

自动触发是最简单的启用方式，无需改变现有工作流程。

```bash
# 检查配置文件是否存在
cat .claude/CLAUDE.md

# 如果不存在，从模板创建
# 配置已在主仓库中自动创建
```

**验证自动触发**：

```
你: 创建一个测试
系统: [自动激活 tdd-enforcer]
```

### 步骤 3: 启用 TDD Enforcer（可选）

TDD Enforcer 会在编写代码前提醒先写测试。

```yaml
启用方式:
  自动: 当检测到 "test" 关键词时自动激活
  手动: 使用 /tdd-enforcer 命令

工作流程:
  1. RED: 编写失败测试
  2. GREEN: 编写最小实现
  3. REFACTOR: 重构优化
```

### 步骤 4: 启用 Git Worktrees（可选）

Worktrees 允许并行开发多个功能。

```bash
# 创建 worktree
git worktree add .git/worktrees/TASK-001 feature/branch-name

# 切换到 worktree
cd .git/worktrees/TASK-001

# 完成后删除
git worktree remove .git/worktrees/TASK-001
```

### 步骤 5: 启用两阶段评审（可选）

在 `phase-b-developer` 中启用规范和质量检查。

```yaml
配置位置: claude/skills/phase-b-developer/SKILL.md

启用方式:
  review_config:
    enabled: true
    phase1:
      enabled: true  # 规范合规性检查
      blocking: true
    phase2:
      enabled: true  # 代码质量检查
      blocking: false
```

### 步骤 6: 启用 Hooks（可选）

Hooks 在关键节点自动执行验证。

```bash
# 检查 hooks 配置
cat aria/hooks/hooks.json

# 启用 session-start hook
# (自动在会话开始时执行)

# 手动运行 hooks
./aria/hooks/run-hook.cmd session-start  # Windows
bash aria/hooks/session-start.sh         # Linux/Mac
```

---

## 验证清单

### 基础验证

- [ ] Skills 子模块已更新到最新版本
- [ ] `.claude/CLAUDE.md` 配置文件存在
- [ ] `.claude/trigger-rules.json` 配置文件存在

### 功能验证

#### 自动触发

- [ ] 输入 "创建测试" 能自动激活 `tdd-enforcer`
- [ ] 输入 "创建分支" 能自动激活 `branch-manager`
- [ ] 输入 "查看状态" 能自动激活 `state-scanner`

#### TDD Enforcer

- [ ] RED 阶段提示先编写测试
- [ ] GREEN 阶段接受最小实现
- [ ] REFACTOR 阶段提示在测试保护下重构

#### Git Worktrees

- [ ] 能成功创建 worktree
- [ ] 能成功切换 worktree
- [ ] 能成功删除 worktree
- [ ] `git worktree list` 显示正确

#### Hooks

- [ ] `session-start.sh` 在 Linux/Mac 上可执行
- [ ] `run-hook.cmd` 在 Windows 上可执行
- [ ] hooks.json 格式正确

---

## 回滚方案

### 禁用自动触发

```bash
# 方法 1: 环境变量
export CLAUDE_AUTO_TRIGGER=false

# 方法 2: 在请求前加前缀
NO_AUTO_TRIGGER
创建一个文件...

# 方法 3: 重命名配置文件
mv .claude/CLAUDE.md .claude/CLAUDE.md.disabled
```

### 禁用 TDD Enforcer

```yaml
# 方法 1: 在请求中绕过
"实现这个功能 --bypass tdd"

# 方法 2: 重命名 skill 目录
mv claude/skills/tdd-enforcer claude/skills/tdd-enforcer.disabled
```

### 禁用 Worktrees

```bash
# 清理所有 worktrees
git worktree list | grep -v '\)' | awk '{print $1}' | xargs -I {} git worktree remove {}

# 或手动删除
rm -rf .git/worktrees/*
git worktree prune
```

### 禁用 Hooks

```yaml
# 方法 1: 在 hooks.json 中禁用
{
  "enabled": false,
  ...
}

# 方法 2: 重命名 hooks 目录
mv aria/hooks aria/hooks.bak
```

### 完全回滚

```bash
# 回退 skills 子模块
cd standards
git checkout previous-commit
cd ..
git add standards
git commit -m "rollchore: rollback skills submodule"

# 恢复配置备份
cp .claude/CLAUDE.md.backup .claude/CLAUDE.md
```

---

## 常见问题

### Q1: 迁移后原有工作流程还能用吗？

**A**: 是的。所有新功能都是可选的，原有的工作流程完全不受影响。

### Q2: 可以只启用部分功能吗？

**A**: 可以。每个功能都有独立的开关，可以按需启用。

### Q3: 自动触发准确吗？

**A**: 准确率约 80%。如果触发错误的 Skill，可以：
- 使用 `NO_AUTO_TRIGGER` 前缀禁用
- 手动指定 Skill: `/branch-manager`

### Q4: Worktrees 会增加很多空间吗？

**A**: Worktrees 共享 Git 对象数据库，空间增量很小。完成后可以删除。

### Q5: Hooks 会拖慢开发速度吗？

**A**: Hooks 设计为轻量级：
- `session-start`: ~2秒
- `pre-commit`: 可选，按需启用
- 失败时不阻塞，仅记录警告

### Q6: TDD Enforcer 会强制我写测试吗？

**A**: 不会"强制"，但会强烈建议。你可以：
- 使用 `--bypass` 跳过
- 解释为什么不写测试
- 标记为技术债务

### Q7: 两阶段评审会阻塞开发吗？

**A**: 仅 Phase 1 (规范合规性) 会阻塞关键问题。
Phase 2 (代码质量) 仅记录警告，不阻塞。

### Q8: 如何验证迁移成功？

**A**: 运行验证清单中的所有检查项，或使用：
```bash
# 快速验证
cat .claude/CLAUDE.md
git worktree list
ls aria/hooks/
```

---

## 迁移支持

### 获取帮助

- 查看各功能的 SKILL.md 文档
- 阅读 [常见问题](#常见问题)
- 提交 issue 到项目仓库

### 反馈渠道

- GitHub Issues: `https://github.com/10CG/Aria/issues`
- 文档讨论: `standards/openspec/changes/aria-workflow-enhancement/`

---

**版本**: 1.0.0
**创建**: 2026-01-18
**提案**: aria-workflow-enhancement v1.1
**相关**: [向后兼容性说明](./backward-compatibility.md)
