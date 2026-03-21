# Aria Plugin v1.4.0 - Release Notes

> **Release Date**: 2026-02-07
> **Version**: 1.4.0
> **Milestone**: Superpowers 两阶段代码审查集成

---

## 概述 / Overview

Aria Plugin v1.4.0 引入了 **Superpowers 风格的两阶段代码审查机制**，这是 Aria 向企业级代码质量管控迈出的重要一步。本次更新借鉴了 [obra/superpowers](https://github.com/obra/superpowers) (501+ GitHub Stars) 的核心设计理念，实现了规范合规性检查与代码质量检查的分离。

### 核心亮点 / Key Highlights

- ✅ **新增** `aria:code-reviewer` Agent - 执行两阶段代码审查
- ✅ **新增** `requesting-code-review` Skill - 用户可调用入口
- ✅ **增强** `subagent-driver` v1.3.0 - 集成两阶段审查流程
- ✅ **中英双语** - 审查结果支持中文/英文输出
- ✅ **7 个示例** - 完整的使用场景文档

---

## 新功能 / What's New

### 1. 两阶段代码审查机制 / Two-Phase Code Review

#### Phase 1: 规范合规性检查 / Specification Compliance

**目标**: 验证实现是否与计划一致

```yaml
检查项:
  - 文件路径与计划一致
  - 所有计划功能已实现
  - 无范围变更 (scope creep)
  - OpenSpec 字段已更新

阻塞性: FAIL 终止审查
```

#### Phase 2: 代码质量检查 / Code Quality

**目标**: 验证代码的技术质量

```yaml
检查项:
  - 代码质量: 关注点分离、错误处理、类型安全
  - 架构设计: 设计决策、可扩展性、性能、安全
  - 测试覆盖: 真实测试、边界情况、集成测试
  - Aria 最佳实践: CLAUDE.md 合规性、文档完整性

阻塞性: 仅 Critical 阻塞
```

### 2. aria:code-reviewer Agent

专业代码审查 Agent，执行两阶段检查并输出结构化报告。

```bash
# 调用方式
/code-reviewer

# 或通过 Task tool
Task(subagent_type: "aria:code-reviewer", prompt: "...")
```

**输出格式**:
```
Phase 1: PASS/FAIL
├── PASS → 继续 Phase 2
└── FAIL → 审查终止

Phase 2: PASS/PASS_WITH_WARNINGS/FAIL
├── Critical (必须修复)
├── Important (应该修复)
└── Minor (建议修复)
```

### 3. requesting-code-review Skill

用户可调用入口，自动填充模板并启动审查。

```bash
# 调用方式
/requesting-code-review
```

**核心功能**:
- 自动检测 Git 状态
- 收集任务信息
- 自动填充模板
- 调用 aria:code-reviewer Agent

### 4. subagent-driver 集成

subagent-driver v1.3.0 新增两阶段审查支持。

```yaml
新增参数:
  enable_two_phase: true (默认值)

工作流:
  - Fresh Subagent 任务完成
  - 自动触发两阶段代码审查
  - 审查通过后继续下一任务
```

---

## 变更内容 / Changes

### 新增组件 / Added Components

| 组件 | 类型 | 描述 |
|------|------|------|
| `aria:code-reviewer` | Agent | 两阶段代码审查执行器 |
| `requesting-code-review` | Skill | 代码审查请求入口 |
| `code-reviewer.md` | 模板 | Agent 模板文件 |
| `examples/` | 文档 | 7 个使用场景示例 |

### 更新组件 / Updated Components

| 组件 | 版本变更 | 描述 |
|------|----------|------|
| `subagent-driver` | 1.2.0 → 1.3.0 | 新增 `enable_two_phase` 参数 |
| `aria/` | 1.3.2 → 1.4.0 | Skills: 25 → 26, Agents: 10 → 11 |

### 文档更新 / Documentation Updates

- `CHANGELOG.md` - 添加 v1.4.0 版本条目
- `README.md` - 更新 Skills/Agents 数量和说明
- `docs/architecture/system-architecture.md` - 新增 8.6 节"两阶段代码审查"
- `VERSION` - 版本号更新
- `plugin.json`, `marketplace.json`, `hooks.json` - 版本同步

---

## 升级指南 / Upgrade Guide

### 从 v1.3.x 升级到 v1.4.0

#### 1. 更新插件

```bash
# 使用 marketplace 更新
/plugin update aria@10CG-aria-plugin

# 或手动拉取
cd aria
git pull origin master
git submodule update --remote
```

#### 2. 验证安装

```bash
# 检查版本
/aria

# 应该显示 Version: 1.4.0

# 检查新组件
/code-reviewer
/requesting-code-review
```

#### 3. 配置 (可选)

```yaml
# 在 .claude/CLAUDE.local.md 中配置
subagent_driver:
  enable_two_phase: true  # 默认已启用
```

#### 4. 破坏性变更

**无破坏性变更** - v1.4.0 完全向后兼容 v1.3.x

---

## 使用示例 / Usage Examples

### 示例 1: 任务完成后审查

```bash
# 1. 完成任务
# (代码实现完成)

# 2. 请求审查
/requesting-code-review

# 3. 审查通过
# Phase 1: ✅ PASS
# Phase 2: ✅ PASS
# → 可以继续下一任务
```

### 示例 2: Phase 1 失败

```bash
/requesting-code-review

# Phase 1: ❌ FAIL
# 阻塞问题:
#   - 计划功能缺失: 密码强度验证
#   - 范围变更: 日期格式化工具
#
# 审查终止 - 请修复后重新提交
```

### 示例 3: Phase 2 有警告

```bash
/requesting-code-review

# Phase 1: ✅ PASS
# Phase 2: ⚠️  PASS_WITH_WARNINGS
# Issues:
#   Important (2):
#     - 缺少缓存命中率监控
#     - 潜在的性能瓶颈 (N+1 查询)
#
# Assessment: 建议修复 Important 问题后继续
```

---

## 已知问题和限制 / Known Issues & Limitations

### 当前限制

1. **大变更集性能**
   - 超过 1000 行代码变更可能导致审查时间过长
   - 建议: 使用分批审查模式

2. **Git 依赖**
   - 依赖 git diff 命令获取变更
   - 非 Git 仓库无法使用

3. **计划文件要求**
   - Phase 1 需要详细的任务计划 (detailed-tasks.yaml)
   - 无计划文件时自动降级到仅 Phase 2

### 计划改进

- [ ] 添加并发审查支持 (多个 Agent 并行审查)
- [ ] 增加自定义审查规则
- [ ] 支持审查结果缓存

---

## 致谢 / Acknowledgments

### 参考项目 / Reference Projects

本功能的设计和实现深受以下项目启发:

- **[obra/superpowers](https://github.com/obra/superpowers)** (501+ Stars)
  - 两阶段代码审查核心概念
  - requesting-code-review Skill 设计
  - code-reviewer Agent 模板

- **[anthropics/claude-code](https://github.com/anthropics/claude-code)**
  - Agent 框架设计
  - Hooks 系统集成

### 特别感谢

- **obra/superpowers 社区** - 提供优秀的设计参考和最佳实践
- **Aria 项目组** - 方法论规范和持续改进

---

## 问题反馈 / Feedback

### 报告问题

- **GitHub Issues**: https://github.com/10CG/aria-plugin/issues
- **GitHub Issues**: https://github.com/10CG/aria-plugin/issues

### 功能建议

欢迎提交功能建议和改进意见！

---

## 完整变更日志 / Full Changelog

详见 [CHANGELOG.md](../CHANGELOG.md)

---

**Release Author**: 10CG Lab
**Release Date**: 2026-02-07
**License**: MIT
