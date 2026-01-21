# Aria 双重隔离策略

> **版本**: 1.0.0
> **创建日期**: 2026-01-21
> **相关提案**: enforcement-mechanism-redesign v2.0

---

## 概述

Aria v2.0 实现了**双重隔离策略**，结合 Git Worktree 文件系统隔离和 Fresh Subagent 上下文隔离，提供渐进式的隔离能力。

---

## 隔离层次架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Aria 双重隔离策略                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L1 - 对话隔离 (Dialogue Isolation)                         │
│  ├── Fresh Subagent (新对话上下文)                          │
│  ├── 无文件系统隔离                                          │
│  └── 适用: 简单任务、低风险变更                              │
│                                                             │
│  L2 - 文件系统隔离 (Filesystem Isolation)                   │
│  ├── Fresh Subagent + Git Worktree                         │
│  ├── 独立工作目录                                            │
│  └── 适用: 中等复杂度、跨目录变更                            │
│                                                             │
│  L3 - 完全隔离 (Full Isolation)                             │
│  ├── Fresh Subagent + Git Worktree + 进程隔离               │
│  ├── 独立依赖环境                                            │
│  └── 适用: 高风险、并行开发、大规模重构                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 隔离级别详解

### L1 - 对话隔离

```yaml
名称: Dialogue Isolation
隔离范围: 仅 AI 对话上下文
文件系统: 共享主工作目录
适用场景:
  - 单文件修改
  - 简单 Bug 修复
  - 配置调整

实现方式:
  subagent_driver:
    isolation_level: "L1"
    fresh_context: true
    worktree: false

优势:
  - 启动快速 (无 git 操作)
  - 资源消耗低
  - 适合快速迭代

风险:
  - 变更直接影响主分支
  - 无法回滚到干净状态
  - 不适合并行开发
```

### L2 - 文件系统隔离

```yaml
名称: Filesystem Isolation
隔离范围: AI 对话 + 文件系统
文件系统: 独立 Git Worktree
适用场景:
  - 跨多文件变更
  - 中等复杂度功能
  - 需要测试验证

实现方式:
  branch_manager:
    mode: "worktree"
    worktree_path: ".git/worktrees/{task-name}"

  subagent_driver:
    isolation_level: "L2"
    fresh_context: true
    worktree: true

优势:
  - 主分支保持干净
  - 支持快速回滚
  - 变更可预览

风险:
  - 共享 node_modules 等依赖
  - 可能有缓存污染
```

### L3 - 完全隔离

```yaml
名称: Full Isolation
隔离范围: AI 对话 + 文件系统 + 进程/依赖
文件系统: 独立 Worktree + 独立依赖
适用场景:
  - 高风险变更
  - 并行多任务开发
  - 大规模重构
  - 依赖版本冲突场景

实现方式:
  branch_manager:
    mode: "worktree"
    worktree_path: "{external_path}/{task-name}"
    install_dependencies: true

  subagent_driver:
    isolation_level: "L3"
    fresh_context: true
    worktree: true
    isolated_env: true

优势:
  - 完全隔离，无干扰
  - 支持并行多任务
  - 可测试不同依赖版本

风险:
  - 启动慢 (需要安装依赖)
  - 磁盘空间消耗大
  - 同步复杂
```

---

## 自动级别选择

### 决策算法

```python
def select_isolation_level(context: dict) -> str:
    """
    根据任务上下文自动选择隔离级别

    Returns: "L1" | "L2" | "L3"
    """
    score = 0

    # 因子评分
    if context.get("parallel_needed"):
        return "L3"  # 并行需求直接 L3

    if context.get("file_count", 0) > 10:
        score += 3
    elif context.get("file_count", 0) > 3:
        score += 1

    if context.get("cross_directory"):
        score += 2

    if context.get("risk_level") == "high":
        score += 3
    elif context.get("risk_level") == "medium":
        score += 1

    if context.get("task_count", 0) > 8:
        score += 3
    elif context.get("task_count", 0) > 3:
        score += 1

    # 级别映射
    if score >= 6:
        return "L3"
    elif score >= 3:
        return "L2"
    else:
        return "L1"
```

### 决策矩阵

| 场景 | 文件数 | 跨目录 | 风险 | 并行 | 级别 |
|------|--------|--------|------|------|------|
| 单文件修复 | 1 | ❌ | 低 | ❌ | L1 |
| 多文件功能 | 5 | ✅ | 中 | ❌ | L2 |
| 大规模重构 | 20+ | ✅ | 高 | ❌ | L3 |
| 并行开发 | 任意 | 任意 | 任意 | ✅ | L3 |

---

## 隔离组件协作

```
┌─────────────────────────────────────────────────────────────┐
│                    组件协作流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. branch-manager 评估复杂度                                │
│     │                                                       │
│     ├─ 评分 < 3 → Mode A (Branch)                           │
│     │   └─ subagent-driver 使用 L1 隔离                     │
│     │                                                       │
│     └─ 评分 >= 3 → Mode B (Worktree)                        │
│         │                                                   │
│         ├─ 评分 < 6 → subagent-driver 使用 L2 隔离          │
│         │                                                   │
│         └─ 评分 >= 6 → subagent-driver 使用 L3 隔离         │
│                                                             │
│  2. subagent-driver 执行任务                                 │
│     ├─ 启动 Fresh Subagent                                  │
│     ├─ 设置工作目录 (L2/L3)                                 │
│     └─ 执行任务 + 审查                                       │
│                                                             │
│  3. branch-finisher 完成流程                                 │
│     ├─ 测试验证                                              │
│     ├─ 4选项完成                                             │
│     └─ Worktree 清理 (L2/L3)                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 对比传统方案

### Superpowers (始终 Worktree)

```yaml
优势:
  - 一致性强
  - 实现简单

劣势:
  - 简单任务过度隔离
  - 启动开销大
  - 资源浪费
```

### Aria v2.0 (智能选择)

```yaml
优势:
  - 效率优化 (简单任务无需隔离)
  - 资源节省
  - 灵活适配不同场景

劣势:
  - 决策逻辑复杂
  - 需要正确评估复杂度
```

---

## 最佳实践

### 何时使用 L1

```yaml
推荐场景:
  - 单文件 Bug 修复
  - 配置文件调整
  - 文档更新
  - 简单重命名

不推荐场景:
  - 跨文件重构
  - API 变更
  - 测试不充分的代码
```

### 何时使用 L2

```yaml
推荐场景:
  - 新功能开发 (3-10 文件)
  - 模块内重构
  - 需要测试验证的变更

不推荐场景:
  - 依赖版本冲突
  - 并行多任务开发
```

### 何时使用 L3

```yaml
推荐场景:
  - 大规模重构 (10+ 文件)
  - 并行多任务开发
  - 高风险变更
  - 依赖版本测试

不推荐场景:
  - 简单修复 (过度工程)
  - 磁盘空间受限
```

---

## 配置参数

```yaml
# .claude/isolation-config.yaml

isolation:
  # 自动选择阈值
  auto_select:
    l2_threshold: 3   # 评分 >= 3 使用 L2
    l3_threshold: 6   # 评分 >= 6 使用 L3

  # 因子权重
  factors:
    file_count:
      low: 0    # 1-3 文件
      medium: 1 # 4-10 文件
      high: 3   # 10+ 文件

    cross_directory:
      no: 0
      yes: 2

    risk_level:
      low: 0
      medium: 1
      high: 3

    task_count:
      low: 0    # 1-3 任务
      medium: 1 # 4-8 任务
      high: 3   # 8+ 任务

    parallel_needed:
      no: 0
      yes: 999  # 强制 L3

  # 默认配置
  defaults:
    level: "L1"
    worktree_base: ".git/worktrees"
    cleanup_on_complete: true
```

---

## 相关文档

- [branch-manager SKILL.md](../../.claude/skills/branch-manager/SKILL.md) - 模式决策
- [subagent-driver SKILL.md](../../.claude/skills/subagent-driver/SKILL.md) - 隔离执行
- [branch-finisher SKILL.md](../../.claude/skills/branch-finisher/SKILL.md) - 清理决策
- [superpowers-vs-aria.md](./superpowers-vs-aria.md) - 对比分析

---

**创建日期**: 2026-01-21
**维护者**: 10CG Lab
