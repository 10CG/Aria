# 版本信息规范化 (Version Standardization)

> **Change ID**: 2026-02-06-version-standardization
> **Status**: Completed
> **Priority**: P0
> **Complexity**: S
> **Estimated**: 2-4h
> **Completed**: 2026-02-06

---

## Overview

规范 Aria 项目的版本管理，确保主项目、子模块、插件配置文件的版本信息一致且同步。

---

## Motivation

### Current Problems

1. **版本信息分散且不一致**
   - `aria/.claude-plugin/plugin.json`: v1.3.0
   - `aria/.claude-plugin/marketplace.json`: v1.1.1 (过时)
   - `aria/.claude-plugin/hooks.json`: v1.1.0 (过时)
   - `aria/VERSION`: 不存在

2. **缺少明确的版本更新规范**
   - 不知道哪些文件需要在版本更新时同步修改
   - 没有版本号含义的统一约定

3. **CHANGELOG 与实际版本不同步**
   - 有时忘记更新 CHANGELOG
   - 版本发布日期不一致

---

## Proposed Solution

### 1. 版本信息文件架构

```
aria/
├── .claude-plugin/
│   ├── plugin.json       # 主版本文件 (真理来源)
│   ├── marketplace.json   # 市场发布配置
│   └── hooks.json        # Hooks 配置
├── VERSION               # 人类可读版本快照
├── CHANGELOG.md          # 版本变更记录
└── README.md             # 包含版本号
```

### 2. 版本号语义约定

遵循 [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR: 破坏性变更 / 架构重构
MINOR: 新功能 / 向后兼容
PATCH: Bug 修复 / 小改进
```

**Aria 项目特殊约定**:

| 变更类型 | 版本变更 | 示例 |
|----------|----------|------|
| 新增 Skill | MINOR+ | 1.2.0 → 1.3.0 |
| Skill 架构重构 | MINOR+ | 1.2.0 → 1.3.0 |
| 文档更新 | PATCH | 1.3.0 → 1.3.1 |
| Bug 修复 | PATCH | 1.3.0 → 1.3.1 |
| 破坏性变更 | MAJOR+ | 1.x → 2.0 |

### 3. 版本更新检查清单

每次发布新版本时，必须更新以下文件：

```yaml
版本发布检查清单:
  真理来源:
    - [ ] aria/.claude-plugin/plugin.json (version 字段)

  派生文件 (必须同步):
    - [ ] aria/.claude-plugin/marketplace.json (version, plugins[].version)
    - [ ] aria/.claude-plugin/hooks.json (version 字段)
    - [ ] aria/VERSION (创建或更新)
    - [ ] aria/CHANGELOG.md (添加新版本条目)
    - [ ] aria/README.md (更新版本号和描述)

  主项目:
    - [ ] 更新子模块指针 (git add aria)
    - [ ] 主项目/VERSION 更新插件版本记录
```

### 4. VERSION 文件格式

```markdown
# Aria Plugin 版本信息

> **版本**: 1.3.0
> **发布日期**: 2026-02-06
> **仓库**: https://forgejo.10cg.pub/10CG/aria-plugin

## 版本号

```
1.3.0
```

## 说明

- **Major (1)**: 稳定核心架构
- **Minor (3)**: 25 个 Skills，TDD Enforcer v2.0 重构
- **Patch (0)**: 当前版本

## 包含内容

- 25 个 Skills
- 10 个 Agents
- Hooks 系统
- Progressive Disclosure 文档架构

## 依赖

- Claude Code 1.0+
- aria-standards v2.1.0+
```

---

## Implementation Tasks

### Phase 1: 修正当前版本 (1h)

- [ ] TASK-001: 更新 `marketplace.json` 版本到 1.3.0
- [ ] TASK-002: 更新 `hooks.json` 版本到 1.3.0
- [ ] TASK-003: 创建 `aria/VERSION` 文件

### Phase 2: 更新文档 (1h)

- [ ] TASK-004: 更新 `aria/README.md` 确保版本一致
- [ ] TASK-005: 在 `CLAUDE.md` 中添加版本更新规范

### Phase 3: 归档 (30m)

- [ ] TASK-006: 更新 CHANGELOG.md 记录本次规范化
- [ ] TASK-007: 提交并打标签

---

## Success Criteria

1. 所有版本信息文件同步到 v1.3.0
2. CLAUDE.md 中有明确的版本更新规范
3. 后续版本更新有明确的检查清单

---

## References

- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- aria/.claude-plugin/plugin.json (真理来源)
