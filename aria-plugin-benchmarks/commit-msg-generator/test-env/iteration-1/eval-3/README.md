# State-Scanner Eval-3: OpenSpec 状态检查测试

## 测试目标
验证 state-scanner 技能是否能正确报告 OpenSpec 的状态，包括：
- 检查项目中的 OpenSpec 文档状态
- 识别活跃的变更
- 报告当前分支的规范遵循情况

## 测试配置
- **技能**: state-scanner
- **路径**: `/F/work2025/cursor/Aria/aria/skills/state-scanner/SKILL.md`
- **描述**: "检查 OpenSpec 状态"
- **输出路径**: `./iteration-1/eval-3/with_skill/outputs/scan_result.txt`
- **预期**: 报告 OpenSpec 状态部分，显示活跃的变更（如果有的话）

## 环境设置
1. 已创建 `openspec/` 目录结构
2. 包含一些 OpenSpec 文档
3. 包含 `proposal.md` 和 `tasks.md` 文件
4. 测试分支处于 feature/eval-3-open-spec 状态

## 执行步骤
1. 调用 state-scanner 技能
2. 扫描项目的 OpenSpec 文档
3. 生成状态报告
4. 验证报告中包含 OpenSpec 状态部分