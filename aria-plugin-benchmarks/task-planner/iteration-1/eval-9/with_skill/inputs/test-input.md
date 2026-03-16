# Test: Task-planner include_tests=true

## 测试描述
验证 task-planner 技能是否能正确处理 include_tests=true 参数，自动在任务列表中包含测试任务。

## 输入参数
- spec_path: /f/work2025/cursor/Aria/aria-plugin-benchmarks/task-planner/iteration-1/eval-9/
- include_tests: true

## 预期输出
任务列表应该包含：
1. 原功能任务（来自 proposal.md）
2. 自动生成的测试任务
3. 测试任务应该有明确的验证标准