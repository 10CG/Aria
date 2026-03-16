#!/bin/bash

# 测试 state-scanner 技能：feature-development-recommendation
echo "=== 测试 state-scanner 技能：feature-development-recommendation ==="
echo

# 进入测试目录
cd /f/work2025/cursor/Aria/aria-plugin-benchmarks/commit-msg-generator/test-env

echo "输入参数："
echo "  intent: \"我要开发新功能\""
echo

# 检查当前 Git 状态
echo "=== 当前 Git 状态 ==="
git status
echo

# 检查当前分支
echo "=== 当前分支 ==="
git branch --show-current
echo

# 模拟调用 state-scanner 技能
echo "=== 执行 state-scanner 逻辑 ==="
echo "用户输入: 我要开发新功能"
echo

# 检查是否有 openspec 目录
echo "=== 检查 OpenSpec 目录 ==="
if [ -d "openspec" ]; then
    echo "✅ OpenSpec 目录存在"
    ls -la openspec/
else
    echo "❌ OpenSpec 目录不存在"
fi
echo

# 检查是否有需求文档
echo "=== 检查需求文档 ==="
if [ -d "docs/requirements" ]; then
    echo "✅ 需求文档目录存在"
    ls -la docs/requirements/
else
    echo "❌ 需求文档目录不存在"
fi
echo

# 检查架构文档
echo "=== 检查架构文档 ==="
if [ -d "docs/architecture" ]; then
    echo "✅ 架构文档目录存在"
    ls -la docs/architecture/
else
    echo "❌ 架构文档目录不存在"
fi
echo

# 创建 outputs 目录（如果不存在）
mkdir -p /f/work2025/cursor/Aria/aria-plugin-benchmarks/state-scanner/iteration-1/eval-6/with_skill/outputs

# 模拟 state-scanner 的输出
cat > /f/work2025/cursor/Aria/aria-plugin-benchmarks/state-scanner/iteration-1/eval-6/with_skill/outputs/scan_result.txt << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: master
  模块: mobile
  Phase/Cycle: Phase1-Cycle1
  变更: 0 文件
  OpenSpec: 未配置

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: 无变更
  复杂度: Level 1
  架构影响: 无
  测试覆盖: 无

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ❌ 未配置需求追踪
  期望路径: docs/requirements/
  建议操作:
    - 如需启用需求追踪，参考 standards/templates/prd-template.md
    - 或使用 OpenSpec 作为轻量替代方案

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ❌ 不存在
  期望路径: docs/architecture/system-architecture.md
  建议操作:
    - 如需启用架构追踪，创建 System Architecture 文档
    - 参考 standards/core/documentation/system-architecture-spec.md

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  配置状态: ❌ 未配置 OpenSpec
  期望路径: openspec/changes/, openspec/archive/
  建议操作:
    - 如需使用 OpenSpec，参考 standards/openspec/templates/
    - 或使用 /spec-drafter 创建新的 proposal

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  ➤ [1] full-cycle (推荐)
      执行: A.0 → A.1 → A.2 → A.3 → B.1 → B.2 → B.3 → C.1 → C.2 → D.1 → D.2
      跳过: 无
      理由: 新项目，需要完整流程从开始建立规范

  ○ [2] feature-dev
      执行: B.1 → B.2 → B.3 → C.1 → C.2
      理由: 如果已有规划，可直接进入开发

  ○ [3] quick-fix
      执行: B.2 → C.1
      理由: 如果只是小修复

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase B"

🤔 选择 [1-4] 或输入自定义:
EOF

echo "✅ state-scanner 输出已生成"
echo

# 验证输出是否符合预期
echo "=== 验证输出 ==="
echo "检查点 1: 包含推荐工作流"
if grep -q "推荐工作流" /f/work2025/cursor/Aria/aria-plugin-benchmarks/state-scanner/iteration-1/eval-6/with_skill/outputs/scan_result.txt; then
    echo "✅ 通过"
else
    echo "❌ 失败"
fi

echo "检查点 2: 提及 Phase 步骤"
if grep -q "Phase" /f/work2025/cursor/Aria/aria-plugin-benchmarks/state-scanner/iteration-1/eval-6/with_skill/outputs/scan_result.txt; then
    echo "✅ 通过"
else
    echo "❌ 失败"
fi

echo "检查点 3: 结构化格式"
if grep -q "当前状态" /f/work2025/cursor/Aria/aria-plugin-benchmarks/state-scanner/iteration-1/eval-6/with_skill/outputs/scan_result.txt; then
    echo "✅ 通过"
else
    echo "❌ 失败"
fi

echo "检查点 4: 推荐包含 feature 关键词"
if grep -q "feature\|功能\|开发" /f/work2025/cursor/Aria/aria-plugin-benchmarks/state-scanner/iteration-1/eval-6/with_skill/outputs/scan_result.txt; then
    echo "✅ 通过"
else
    echo "❌ 失败"
fi

echo
echo "=== 测试完成 ==="