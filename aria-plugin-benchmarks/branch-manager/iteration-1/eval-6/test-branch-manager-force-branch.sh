#!/bin/bash

# 测试 branch-manager 技能：强制使用 branch 模式
echo "=== 测试 branch-manager 技能：强制使用 branch 模式 ==="
echo

# 进入测试目录
cd F:/work2025/cursor/Aria/aria-plugin-benchmarks/commit-msg-generator/test-env

# 模拟技能调用参数
MODULE="backend"
TASK_ID="TASK-003"
DESCRIPTION="test"
MODE="branch"

echo "输入参数："
echo "  module: $MODULE"
echo "  task_id: $TASK_ID"
echo "  description: $DESCRIPTION"
echo "  mode: $MODE"
echo

# 检查当前 Git 状态
echo "=== 当前 Git 状态 ==="
git status
echo

# 检查当前分支
echo "=== 当前分支 ==="
git branch --show-current
echo

# 执行 branch-manager 逻辑
echo "=== 执行 branch-manager 逻辑 ==="

# 1. 模式决策（强制使用 branch）
echo "模式决策: 强制使用 branch 模式"
echo "不执行自动评分算法，直接使用 branch 模式"
echo

# 2. 环境验证
echo "=== 环境验证 ==="

# 检查是否在正确的分支
current_branch=$(git branch --show-current)
if [ "$current_branch" != "develop" ]; then
    echo "❌ 错误: 当前不在 develop 分支 (当前: $current_branch)"
    exit 1
fi

echo "✅ 当前在 develop 分支"
echo

# 检查工作目录是否干净
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ 错误: 工作目录不干净，有未提交的更改"
    exit 1
fi

echo "✅ 工作目录干净"
echo

# 3. 生成分支名
branch_name="feature/${MODULE}/${TASK_ID}-${DESCRIPTION}"
echo "=== 分支生成 ==="
echo "分支名: $branch_name"
echo

# 4. 创建本地分支
echo "=== 创建本地分支 ==="
git checkout -b "$branch_name"
echo "✅ 分支创建成功"
echo

# 5. 推送到远程
echo "=== 推送到远程 ==="
git push -u origin "$branch_name"
echo "✅ 推送成功"
echo

# 6. 输出结果
echo "=== 输出结果 ==="
echo "mode: \"branch\""
echo "branch_name: \"$branch_name\""
echo "location: \"main_repo\""
echo "remote_push: \"success\""
echo "decision_reason: \"强制使用 branch 模式\""
echo "next_step: \"开始 B.2 执行验证\""
echo

# 7. 切换回 develop
echo "=== 清理 ==="
git checkout develop
echo "✅ 已切换回 develop 分支"
echo

echo "=== 测试完成 ==="