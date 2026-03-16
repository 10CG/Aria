#!/usr/bin/env node

/**
 * State-Scanner Eval-3: OpenSpec 状态检查测试
 *
 * 直接使用 Claude Code 运行 state-scanner 技能
 */

const { execSync } = require('child_process');

// 运行 state-scanner 技能
console.log('=== State-Scanner Eval-3: OpenSpec 状态检查测试 ===\n');

try {
  // 运行 state-scanner 技能
  const command = 'cd /f/work2025/cursor/Aria && aria run skill:state-scanner -- "检查 OpenSpec 状态" --verbose';
  console.log(`执行命令: ${command}\n`);

  const output = execSync(command, {
    encoding: 'utf8',
    stdio: 'inherit',
    cwd: '/f/work2025/cursor/Aria'
  });

  console.log('\n=== 测试执行完成 ===');

} catch (error) {
  console.error('执行失败:', error.message);
  process.exit(1);
}