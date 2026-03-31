# 新增 aria-report 技能 — Issue 报告与反馈

## Level: 2 (Minimal)

## 概述

为 Aria 插件新增 `aria-report` 技能，让用户能从终端直接向维护团队报告 Bug、提交功能建议或提问。自动收集环境信息，自动路由到 Forgejo（内部用户）或 GitHub（外部用户）。

## 动机

- Aria 插件已公开发布到 GitHub，外部用户缺少结构化的反馈入口
- 问题排查常需 plugin 版本、Skills 数量、配置状态等环境信息，手动收集低效
- Aether 项目已验证 `aether-report` 模式可行，Aria 应复用该架构
- 与 `state-scanner`、`agent-team-audit` 等现有技能集成后，可形成"发现问题 → 报告问题"闭环

## 变更内容

### 1. 新增 `aria/skills/aria-report/SKILL.md`

参考 Aether `aether-report` 技能，适配 Aria：

- **Issue 类型**: Bug / Feature / Question
- **环境收集**: Plugin 版本、Skills 数量、OS、`.aria/config.json` 状态
- **隐私审查**: 提交前必须用户确认内容
- **提交路由**: Forgejo (内部) → GitHub API → GitHub Pre-filled URL (降级)
- **目标仓库**: Forgejo `10CG/Aria` / GitHub `10CG/aria-plugin`

### 2. 与现有技能集成

- `state-scanner` 发现异常时可建议 `/aria:report`
- `agent-team-audit` 检测到 Aria 自身问题时可引导反馈

### 3. 不变更

- 不修改现有技能逻辑
- 不新增外部依赖
- 不需要新的 Agent

## 影响范围

| 文件 | 操作 |
|------|------|
| `aria/skills/aria-report/SKILL.md` | 新建 |
| `aria/.claude-plugin/plugin.json` | 更新 Skills 数量描述 |
| `aria/.claude-plugin/marketplace.json` | 更新版本 |
| `aria/VERSION` | 更新 |
| `aria/CHANGELOG.md` | 添加版本条目 |
| `aria/README.md` | 更新 Skills 数量和版本号 |

## 验收标准

- [ ] `aria-report` 技能可通过 `/aria:report [bug|feature|question]` 调用
- [ ] 自动收集 Aria 环境信息（Plugin 版本、Skills 数量、OS、配置状态）
- [ ] 提交前展示完整内容并获用户确认
- [ ] 支持 Forgejo / GitHub API / GitHub URL 三种提交路由
- [ ] 版本文件一致性：plugin.json 为真理来源，其他文件同步
