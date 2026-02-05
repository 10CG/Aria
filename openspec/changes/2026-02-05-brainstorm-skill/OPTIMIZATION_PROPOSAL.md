# Brainstorm Skill 结构优化提案

> **日期**: 2026-02-05
> **状态**: Draft
> **目标**: 将 1723 行 SKILL.md 优化至 ~450 行

---

## 问题陈述

### 当前状态

```
brainstorm/SKILL.md: 1723 行 (过大型)
├── Phase 1 实现: +908 行 (最大增量来源)
├── ASCII 状态机图: 63 行
├── 嵌入式 YAML 配置: ~400 行
├── 引导模板系统: 355 行
├── 使用示例: 136 行
└── 错误处理场景: 233 行
```

### 对比参考

| Skill | 行数 | 评级 |
|-------|------|------|
| Superpowers brainstorming | 77 | ⭐ 极简 |
| spec-drafter | 433 | ✅ 优秀 |
| state-scanner | 566 | ✅ 良好 |
| workflow-runner | 619 | ⚠️ 偏高 |
| **brainstorm (当前)** | **1723** | ❌ **严重过大** |

### 违反的原则

根据 Anthropic skill-creator 最佳实践：

1. **Concise is Key**: 上下文窗口是公共资源
2. **Progressive Disclosure**: 3级加载系统 (Metadata → Body → Resources)
3. **SKILL.md < 500 行**: 当前行数超标 3.4 倍
4. **避免嵌入配置**: YAML 配置应独立
5. **避免重复内容**: 约束管理出现两次

---

## 优化策略

### 策略 1: Progressive Disclosure (渐进式披露)

```
Level 1: Metadata (始终加载, ~100 词)
  ├── name: brainstorm
  ├── description: 一句话说明
  └── argument-hint: [mode] [topic]

Level 2: SKILL.md (触发时加载, <500 行)
  ├── 快速开始 (是/否决策)
  ├── 核心功能 (表格)
  ├── 三种模式概述
  ├── 执行流程概览
  └── 引导策略矩阵

Level 3: References (按需加载)
  ├── references/STATE_MACHINE.md (状态机详解)
  ├── references/DEPTH_CONTROL.md (深度控制算法)
  ├── references/DECISION_WORKFLOW.md (决策记录流程)
  ├── templates/*.md (引导模板)
  ├── config/*.yaml (配置文件)
  └── examples/*.md (使用示例)
```

### 策略 2: 提取配置文件

```yaml
# config/state-machine.yaml (104 行)
states:
  INIT:
    entry: [...]
    exit_condition: ...
  CLARIFY:
    entry: [...]
    exit_condition: ...
  ...

# config/constraints.yaml (128 行)
constraint_library:
  business:
    budget: {...}
  technical:
    deployment: {...}
  team:
    skills: {...}
```

### 策略 3: 模板化引导系统

```
templates/
├── problem.md       (85 行) - problem 模式引导
├── requirements.md  (95 行) - requirements 模式引导
├── technical.md     (133 行) - technical 模式引导
└── common.md        (31 行) - 通用追问技巧
```

### 策略 4: 示例独立化

```
examples/
├── problem-dialogue.md    (完整对话示例)
├── requirements-dialogue.md
├── technical-dialogue.md
└── error-scenarios.md     (错误处理场景)
```

---

## 目标结构

### 新文件布局

```
aria/skills/brainstorm/
├── SKILL.md                  (~450 行) ← 主文件
├── SKILL_DESIGN.md           (设计文档, 保持不变)
├── references/               (技术详解)
│   ├── STATE_MACHINE.md      (状态机详细定义)
│   ├── DEPTH_CONTROL.md      (深度计算逻辑)
│   └── DECISION_WORKFLOW.md  (决策记录流程)
├── templates/                (引导模板)
│   ├── problem.md
│   ├── requirements.md
│   ├── technical.md
│   └── common.md
├── config/                   (配置文件)
│   ├── state-machine.yaml
│   └── constraints.yaml
└── examples/                 (使用示例)
    ├── problem-dialogue.md
    ├── requirements-dialogue.md
    ├── technical-dialogue.md
    └── error-scenarios.md
```

### 新 SKILL.md 结构 (~450 行)

```markdown
# 头脑风暴引擎 (Brainstorm v1.1)

## 快速开始
### 我应该使用这个 Skill 吗？
(使用场景 + 不使用场景)

## 核心功能
(功能表格, 6-7 行)

## 工作模式
(三种模式精简表格, ~30 行)

## 执行流程概览
### 阶段 1: 初始化
(模式检测 + 上下文加载, ~20 行)

### 阶段 2: 对话引导
#### 状态机概览
  - 状态序列: INIT → CLARIFY → EXPLORE → CONVERGE → SUMMARY → COMPLETE
  - 详细定义: 见 [STATE_MACHINE.md](references/STATE_MACHINE.md)

#### 引导策略矩阵
  (表格, 8 行)

  - 深度控制: 见 [DEPTH_CONTROL.md](references/DEPTH_CONTROL.md)
  - 决策记录: 见 [DECISION_WORKFLOW.md](references/DECISION_WORKFLOW.md)
  - 约束管理: 见 [config/constraints.yaml](config/constraints.yaml)

### 阶段 3: 输出生成
(输出映射, 简化版, ~20 行)

## 引导模板
- problem 模式: 见 [templates/problem.md](templates/problem.md)
- requirements 模式: 见 [templates/requirements.md](templates/requirements.md)
- technical 模式: 见 [templates/technical.md](templates/technical.md)
- 通用技巧: 见 [templates/common.md](templates/common.md)

## 与其他 Skills 的集成
(精简表格, ~30 行)

## 配置
- 项目级配置示例 (~20 行)
- 详细配置: 见 [config/](config/)

## 使用示例
- 完整对话: 见 [examples/](examples/)
- 快速参考: (保留 1-2 个简短示例, ~20 行)

## 输出文件规范
(简化版, ~30 行)

## 检查清单
(使用前/中/后, ~20 行)

## 相关文档
(引用列表)
```

---

## 实施计划

### Phase 1: 提取配置 (1 小时)

- [ ] 创建 `config/` 目录
- [ ] 提取状态转换规则 → `config/state-machine.yaml`
- [ ] 提取约束库定义 → `config/constraints.yaml`
- [ ] 更新 SKILL.md 中的引用

### Phase 2: 提取模板 (1 小时)

- [ ] 创建 `templates/` 目录
- [ ] 提取 problem 模板 → `templates/problem.md`
- [ ] 提取 requirements 模板 → `templates/requirements.md`
- [ ] 提取 technical 模板 → `templates/technical.md`
- [ ] 提取通用追问 → `templates/common.md`

### Phase 3: 提取参考文档 (1 小时)

- [ ] 创建 `references/` 目录
- [ ] 提取深度控制逻辑 → `references/DEPTH_CONTROL.md`
- [ ] 提取决策记录工作流 → `references/DECISION_WORKFLOW.md`
- [ ] 提取状态机详细定义 → `references/STATE_MACHINE.md`

### Phase 4: 提取示例 (1 小时)

- [ ] 创建 `examples/` 目录
- [ ] 提取对话示例 → `examples/`
- [ ] 提取错误处理场景 → `examples/error-scenarios.md`

### Phase 5: 精简主文件 (1 小时)

- [ ] 删除 ASCII 状态机图，替换为简化描述
- [ ] 删除重复的约束管理章节
- [ ] 精简工作模式为表格
- [ ] 添加所有引用链接
- [ ] 验证行数 < 500 行

### Phase 6: 验证 (30 分钟)

- [ ] 确认所有链接正确
- [ ] 确认功能完整性
- [ ] 测试 skill 触发
- [ ] 验证参考文件可访问

---

## 预期效果

### 行数对比

| 文件 | 优化前 | 优化后 | 减少 |
|------|--------|--------|------|
| SKILL.md | 1723 | ~450 | -1273 (-74%) |
| references/STATE_MACHINE.md | - | ~150 | +150 |
| references/DEPTH_CONTROL.md | - | ~100 | +100 |
| references/DECISION_WORKFLOW.md | - | ~120 | +120 |
| templates/problem.md | - | ~85 | +85 |
| templates/requirements.md | - | ~95 | +95 |
| templates/technical.md | - | ~133 | +133 |
| templates/common.md | - | ~31 | +31 |
| config/state-machine.yaml | - | ~104 | +104 |
| config/constraints.yaml | - | ~128 | +128 |
| examples/* | - | ~369 | +369 |
| **总计** | **1723** | **1765** | +42 |

**关键指标**:
- 主 SKILL.md: 1723 → 450 (-74%)
- 触发时加载: 1723 → 450 (-74%)
- 按需加载: 0 → 1315 (新增独立文件)

### 上下文效率

```
优化前: 每次 skill 触发加载 1723 行
优化后: 每次 skill 触发加载 450 行
节省: 74% 上下文窗口

参考文件仅在需要时加载:
- 状态转换 → config/state-machine.yaml
- 约束验证 → config/constraints.yaml
- 引导模板 → templates/*.md (按模式加载)
```

---

## 参考模式

### Superpowers brainstorming (77 行)

```markdown
# Brainstorming Ideas Into Designs

## Overview
(2-3 行概述)

## The Process
**Understanding the idea:**
(4 个要点, ~8 行)

**Exploring approaches:**
(3 个要点, ~6 行)

**Presenting the design:**
(5 个要点, ~10 行)

## After the Design
(2 个部分, ~8 行)

## Key Principles
(6 个原则, ~6 行)

总计: 77 行
```

### 优化后 brainstorm 目标结构

```markdown
# 头脑风暴引擎 (Brainstorm v1.1)

## 快速开始
(是/否决策, ~15 行)

## 核心功能
(表格, ~10 行)

## 工作模式
(3 种模式, ~30 行)

## 执行流程
(3 个阶段概览 + 引用, ~60 行)

## 引导模板
(4 个引用, ~10 行)

## 集成
(精简表格, ~30 行)

## 配置
(简述 + 引用, ~30 行)

## 示例
(简述 + 引用, ~30 行)

## 规范
(简化, ~50 行)

## 检查清单
(~20 行)

## 相关文档
(~10 行)

总计: ~450 行
```

---

## 风险与缓解

| 风险 | 缓解措施 |
|------|---------|
| 引用文件路径错误 | Phase 6 验证所有链接 |
| 功能缺失 | 对比原文件逐项检查 |
| 独立文件不可访问 | 使用相对路径, 确保正确 |
| 用户习惯变化 | 保持核心接口不变 |

---

## 批准

- [ ] Phase 1-6 计划确认
- [ ] 开始实施
- [ ] 完成验证

---

**创建日期**: 2026-02-05
**状态**: Draft
