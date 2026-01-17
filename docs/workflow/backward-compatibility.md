# 向后兼容性说明

> **版本**: 1.0.0
> **来源**: TASK-029
> **提案**: aria-workflow-enhancement

---

## 概述

`aria-workflow-enhancement` 遵循**完全向后兼容**原则，确保现有工作流程、配置和代码不受影响。

### 兼容性目标

- ✅ 现有工作流程完全可用
- ✅ 现有配置自动迁移
- ✅ 新功能默认禁用，可选启用
- ✅ 无破坏性变更

---

## 兼容性矩阵

### 按模块

| 模块 | 兼容性 | 说明 |
|------|--------|------|
| **mobile** | ✅ 完全兼容 | Flutter/Dart 代码无变更 |
| **backend** | ✅ 完全兼容 | Python/FastAPI 代码无变更 |
| **shared** | ✅ 完全兼容 | API 契约无变更 |
| **standards** | ✅ 完全兼容 | 规范文件向后兼容 |
| **docs** | ✅ 完全兼容 | 文档格式无破坏性变更 |

### 按功能

| 功能 | 默认状态 | 兼容性影响 |
|------|----------|------------|
| **TDD Enforcer** | ❌ 禁用 | 无影响，需显式启用 |
| **Git Worktrees** | ❌ 禁用 | 无影响，需显式使用 |
| **自动触发** | ✅ 启用 | 仅影响 Skill 调用方式 |
| **两阶段评审** | ❌ 禁用 | 无影响，需显式启用 |
| **Hooks** | ⚠️ 部分启用 | session-start 轻量运行 |

---

## 详细兼容性说明

### 1. Skills 目录结构

#### 保持不变

```
claude/skills/
├── tdd-enforcer/           # 新增，不影响现有
├── branch-manager/          # 已有，更新版本
├── phase-b-developer/       # 已有，更新版本
├── ...                      # 其他 skills 不变
```

**兼容性**:
- ✅ 现有 Skills 完全可用
- ✅ 新 Skills 不自动激活
- ✅ 符合 Agent Skills 官方规范

#### 版本更新

| Skill | 旧版本 | 新版本 | 破坏性变更 |
|-------|--------|--------|------------|
| `branch-manager` | 1.1.0 | 1.2.0 | ❌ 无 (仅添加 worktree 支持) |
| `phase-b-developer` | 1.0.0 | 1.1.0 | ❌ 无 (仅添加评审机制) |

### 2. 配置文件

#### 新增配置（不影响现有）

```
.claude/
├── CLAUDE.md              # 新增，可选读取
└── trigger-rules.json     # 新增，可选读取
```

**兼容性**:
- ✅ 现有项目无需此文件
- ✅ 缺失时使用默认行为
- ✅ 格式错误时不影响其他功能

### 3. Hooks 系统

#### Hook 执行策略

```yaml
执行策略:
  session-start:
    enabled: true
    blocking: false    # 失败不阻塞
    timeout: 30        # 超时后跳过

  pre-commit:
    enabled: false     # 默认禁用
    blocking: true     # 启用后可阻塞

  task-complete:
    enabled: false     # 默认禁用
    blocking: false
```

**兼容性**:
- ✅ 仅 session-start 默认启用
- ✅ 失败时不阻塞会话
- ✅ 可完全禁用

### 4. Git Worktrees

#### 与传统分支共存

```bash
# 传统方式 (仍然支持)
git checkout -b feature/new-branch
git work
git commit
git push

# Worktree 方式 (新增)
git worktree add .git/worktrees/feature feature/new-branch
cd .git/worktrees/feature
git work
git commit
git push
```

**兼容性**:
- ✅ 两种方式可以混用
- ✅ Worktrees 是可选的
- ✅ 不影响现有分支

---

## 配置迁移

### 自动迁移

无需手动迁移，新功能默认禁用。

### 手动启用

按需启用各个功能，参见 [迁移指南](./migration-guide.md)。

---

## 行为变更

### 无变更的场景

以下场景行为**完全不变**：

| 场景 | 行为 |
|------|------|
| 直接调用 Skill | `/branch-manager` 正常工作 |
| 提交代码 | 现有提交流程不变 |
| 分支管理 | 常规 Git 操作不变 |
| 代码审查 | 现有审查流程不变 |

### 有变更的场景

以下场景有**新增行为**，但不影响现有流程：

| 场景 | 新行为 | 可禁用 |
|------|--------|--------|
| 自然语言请求 | 可能自动触发 Skill | `NO_AUTO_TRIGGER` |
| 会话开始 | 运行 session-start hook | 禁用 hooks |
| Phase B 执行 | 可选的两阶段评审 | 禁用 review |

---

## 降级方案

### 如果新功能有问题

#### 方案 1: 禁用特定功能

```yaml
# 禁用自动触发
export CLAUDE_AUTO_TRIGGER=false

# 禁用 TDD Enforcer
# (不使用相关关键词)

# 禁用两阶段评审
# (在 phase-b-developer 中设置 enabled: false)

# 禁用 Hooks
mv aria/hooks aria/hooks.bak
```

#### 方案 2: 回退 Skills 子模块

```bash
cd standards
git checkout <previous-commit>
cd ..
git add standards
git commit -m "rollchore: rollback skills"
```

#### 方案 3: 使用旧版工作流程

```bash
# 绕过所有新功能
NO_AUTO_TRIGGER
export CLAUDE_HOOKS_ENABLED=false

# 按原有方式工作
/branch-manager  # 仍然可用
```

---

## 测试兼容性

### 验证步骤

1. **基础功能测试**
   ```bash
   # 确认现有 Skills 仍然可用
   /branch-manager
   /task-planner
   /state-scanner
   ```

2. **工作流程测试**
   ```bash
   # 确认十步循环仍然工作
   /state-scanner
   /workflow-runner
   ```

3. **配置测试**
   ```bash
   # 确认没有配置冲突
   cat .claude/CLAUDE.md
   git status
   ```

---

## 兼容性承诺

### 版本兼容

| Aria 版本 | aria-workflow-enhancement | 兼容性 |
|-----------|---------------------------|--------|
| v1.0.0 | N/A | 基线 |
| v1.1.0 | v1.0 | ✅ 完全兼容 |
| v1.2.0+ | v1.0+ | ✅ 向后兼容 |

### API 兼容

- ✅ 现有 Skill API 不变
- ✅ 现有配置格式不变
- ✅ 现有文件结构不变

### 数据兼容

- ✅ 现有 Git 历史不变
- ✅ 现有文档格式不变
- ✅ 现有测试用例不变

---

## 升级路径

### 从 v1.0 到 v1.1 (Workflow Enhancement)

```yaml
升级步骤:
  1. 更新 skills 子模块
  2. (可选) 启用自动触发
  3. (可选) 启用其他功能

回滚步骤:
  1. 禁用新功能
  2. 或回退子模块
```

### 未来升级

所有未来升级将保持：
- ✅ 向后兼容
- ✅ 渐进式启用
- ✅ 可随时回滚

---

## 已知限制

### 需要注意的事项

1. **自动触发误判**
   - 置信度约 80%
   - 可使用 `NO_AUTO_TRIGGER` 绕过

2. **Hooks 性能**
   - session-start 增加约 2 秒
   - 可禁用以提升性能

3. **Worktrees 空间**
   - 多个 worktrees 会增加磁盘使用
   - 完成后记得清理

---

**版本**: 1.0.0
**创建**: 2026-01-18
**提案**: aria-workflow-enhancement v1.1
**相关**: [迁移指南](./migration-guide.md)
