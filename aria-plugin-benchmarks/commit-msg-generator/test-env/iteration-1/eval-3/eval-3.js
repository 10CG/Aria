/**
 * State-Scanner Eval-3: OpenSpec 状态检查测试
 *
 * 测试 state-scanner 技能检查项目 OpenSpec 状态的能力
 */

// 导入 Skill 运行器
const { runSkill } = require('../../../shared/skill-runner.js');

async function runStateScannerEval3() {
  console.log('\n=== State-Scanner Eval-3: OpenSpec 状态检查测试 ===\n');

  // 定义测试配置
  const config = {
    skillPath: 'F:/work2025/cursor/Aria/aria/skills/state-scanner',
    action: 'default',
    args: [
      '检查 OpenSpec 状态',
      '--verbose',
      '--output-dir', './iteration-1/eval-3/with_skill/outputs'
    ],
    description: '检查 OpenSpec 状态',
    expectedOutput: '应该报告 OpenSpec 状态部分，显示活跃的变更（如果有的话）',
    outputFiles: [
      './iteration-1/eval-3/with_skill/outputs/scan_result.txt'
    ]
  };

  try {
    // 运行技能
    const result = await runSkill(config);

    // 验证输出
    console.log('\n=== 验证结果 ===');

    if (result.success) {
      console.log('✅ 技能执行成功');

      // 检查输出文件是否创建
      for (const outputFile of config.outputFiles) {
        const fs = require('fs');
        if (fs.existsSync(outputFile)) {
          console.log(`✅ 输出文件已创建: ${outputFile}`);

          // 读取并显示内容
          const content = fs.readFileSync(outputFile, 'utf8');
          console.log('\n=== 输出内容 ===');
          console.log(content);

          // 验证是否包含预期的内容
          if (content.includes('OpenSpec') || content.includes('状态')) {
            console.log('✅ 输出包含 OpenSpec 状态信息');
          } else {
            console.log('⚠️  输出可能缺少 OpenSpec 状态信息');
          }
        } else {
          console.log(`❌ 输出文件未找到: ${outputFile}`);
        }
      }
    } else {
      console.log('❌ 技能执行失败:', result.error);
    }

    return result;

  } catch (error) {
    console.error('执行测试时出错:', error);
    return { success: false, error: error.message };
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  runStateScannerEval3().then(result => {
    process.exit(result.success ? 0 : 1);
  }).catch(error => {
    console.error('执行失败:', error);
    process.exit(1);
  });
}

module.exports = { runStateScannerEval3 };