# branch-manager eval-7: 强制 Worktree 模式测试

## 测试概览
- **测试日期**: 2026-03-13
- **测试内容**: branch-manager 技能在强制 Worktree 模式下的行为
- **输入参数**: module=backend, task_id=TASK-004, description=simple, mode=worktree
- **预期结果**: 使用 Worktree 模式，提及 .git/worktrees 路径

## 测试执行过程

### 1. 环境准备
- 检测到当前只有 master 分支
- 自动创建 develop 分支
- 处理工作目录中的未提交变更

### 2. 分支创建流程
- 生成分支名: `feature/backend/TASK-004-simple`
- 创建该分支（如果不存在）
- 切换回 develop 分支

### 3. Worktree 创建
- Worktree 路径: `.git/worktrees/TASK-004-simple`
- 执行: `git worktree add .git/worktrees/TASK-004-simple feature/backend/TASK-004-simple`
- 成功创建隔离工作目录

## 测试结果

✅ **成功**

branch-manager 技能在强制 Worktree 模式下正确执行：
- 识别并使用 Worktree 模式
- 在 `.git/worktrees/` 目录下创建隔离工作目录
- 正确生成分支名和 worktree 路径
- 提供清晰的下一步指示和清理命令

## Worktree 验证
```bash
$ git worktree list
F:/work2025/cursor/Aria/aria-plugin-benchmarks/commit-msg-generator/test-env                                 fe27246 [develop]
F:/work2025/cursor/Aria/aria-plugin-benchmarks/commit-msg-generator/test-env/.git/worktrees/TASK-004-simple  fe27246 [feature/backend/TASK-004-simple]
```

## 结论
branch-manager 技能的强制 Worktree 模式实现正确，能够：
1. 在指定路径创建 worktree
2. 隔离开发环境
3. 提供完整的生命周期管理（创建→使用→清理）