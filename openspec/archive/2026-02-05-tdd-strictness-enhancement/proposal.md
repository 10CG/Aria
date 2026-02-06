# TDD 执行严格度增强

> **Level**: Full (Level 3 Spec)
> **Status**: Completed
> **Created**: 2026-02-05
> **Updated**: 2026-02-06 (设计重构：文档驱动)
> **Reference**: [Superpowers TDD](https://github.com/obra/superpowers)

---

## Why

### 核心问题：TDD 检查不够严格

当前 Aria 的 `tdd-enforcer` 与 Superpowers 的 TDD 强制执行存在根本性差异：

| 检查点 | Aria 当前实现 | Superpowers 实现 |
|--------|--------------|-----------------|
| **测试文件存在性** | ✅ 检查 | ✅ 检查 |
| **测试状态 (RED)** | ❌ 不检查 | ✅ **必须处于失败状态** |
| **代码变更范围** | ❌ 不检查 | ✅ GREEN 阶段最小实现检查 |
| **执行级别** | 警告 (可绕过) | 强制 (不可绕过) |

### 设计理念重构

经过分析，我们发现**之前的实现方向有误**：

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    错误的设计思路                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ❌ 把 Skill 当作 Python 包来开发                                      │
│     → 创建大量 Python 模块                                             │
│     → 实现复杂的类继承结构                                             │
│     → 编写单元测试                                                     │
│                                                                         │
│  问题:                                                                   │
│    - Claude Code 不会导入执行这些 Python 代码                          │
│    - Skill 系统读取的是 SKILL.md 文档                                   │
│    - 违背了 Agent Skills 的设计原则                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    正确的设计思路                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ 参考 Superpowers：文档驱动，AI 理解执行                              │
│     → SKILL.md 描述工作流                                               │
│     → AI 读取并理解流程                                                 │
│     → AI 按流程执行检查                                                 │
│                                                                         │
│  优势:                                                                   │
│    - 符合 Agent Skills 设计原则                                          │
│    - 修改简单，更新文档即可                                             │
│    - Token 效率高（文档比代码简洁）                                     │
│    - 易于维护和扩展                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Superpowers 的启示

Superpowers 的 `test-driven-development` skill 非常简洁：

```
test-driven-development/
└── SKILL.md
    ├── 工作流程描述 (RED-GREEN-REFACTOR)
    ├── 检查点说明
    └── 使用示例
```

**没有复杂的代码实现**，只有**清晰的文档描述**。AI 读取文档后理解并执行。

---

## What

重构 `tdd-enforcer` 为文档驱动的 Skill，实现三级严格度模式。

### 核心变更

| 组件 | 旧设计 (代码驱动) | 新设计 (文档驱动) |
|------|-----------------|-------------------|
| **tdd-enforcer** | 17+ Python 模块 | 1 个 SKILL.md |
| **测试运行器** | Python 类实现 | 命令示例描述 |
| **验证器** | Python 类实现 | 检查规则描述 |
| **Hook** | Python 代码实现 | Hook 配置描述 |
| **状态追踪** | Python 类实现 | 状态文件格式描述 |

### 三级严格度架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       TDD 严格度三级架构                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Level 1: Advisory (警告模式)                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 检查: 测试文件是否存在                                           │    │
│  │ 违规: 警告但允许继续                                             │    │
│  │ 用途: 新项目团队适应期                                           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              ↓                                          │
│  Level 2: Strict (严格模式)                                             │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 检查: 测试文件存在 + 测试必须失败 (RED)                           │    │
│  │ 违规: 阻止操作，要求修正                                         │    │
│  │ 用途: 生产环境项目                                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              ↓                                          │
│  Level 3: Superpowers (完全模式)                                       │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 检查: RED 状态 + GREEN 最小实现 + REFACTOR 保持通过               │    │
│  │ 违规: 不可绕过，强制 TDD 完整循环                                │    │
│  │ 用途: 高质量要求项目                                             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. 新的目录结构 (简化版)

```
tdd-enforcer/
├── SKILL.md                    # 主要文档 (<500 行)
├── EXAMPLES.md                 # 使用示例
└── references/                 # 按需加载的详细参考
    ├── strictness-levels.md    # 严格度级别详解
    ├── red-state-detection.md # RED 状态检测说明
    ├── green-phase-check.md   # GREEN 阶段检查说明
    └── migration-guide.md      # v1.x → v2.0 迁移指南
```

### 删除的文件

```
❌ 删除所有 Python 实现文件:
  - cache.py
  - config.py
  - diff_analyzer.py
  - state_persistence.py
  - state_tracker.py
  - test_runners/
  - validators/
  - hooks/pre_tool_use_hook.py
  - tests/
```

**理由**：这些是"实现代码"，不会被 Claude Code 执行。AI 只需要理解"做什么"，不需要"怎么做"的代码。

---

## 2. SKILL.md 核心内容设计

### 2.1 工作流程描述 (文档驱动)

```markdown
# TDD Enforcer

name: tdd-enforcer
description: 强制执行测试驱动开发 (TDD) 工作流

## 三级严格度

### Advisory (警告模式)

当用户编辑源代码时：

1. 检查是否存在对应的测试文件
2. 如果不存在，显示警告：
   ```
   ⚠️ 未找到测试文件
   建议先编写失败的测试 (RED 阶段)

   期望测试: tests/test_{name}.py
   当前文件: src/{name}.py
   ```
3. 允许继续操作

### Strict (严格模式)

当用户编辑源代码时：

1. 检查是否存在对应的测试文件
2. 如果不存在，阻止操作：
   ```
   🚫 TDD 严格模式拦截
   必须先创建测试文件

   [创建测试] [取消]
   ```

3. 如果测试文件存在，检查测试是否处于失败状态
4. 运行测试命令检测状态：
   ```bash
   # Python
   pytest tests/test_{name}.py --collect-only --quiet

   # JavaScript
   npx jest tests/{name}.test.js --passWithNoTests --verbose

   # Dart
   flutter test test/{name}_test.dart --dry-run
   ```
5. 如果测试全部通过，阻止操作：
   ```
   🚫 测试已通过 (GREEN)
   请添加新的失败测试 (RED) 后再编写实现代码
   ```

### Superpowers (完全模式)

包含 Strict 的所有检查，额外增加：

1. **金装甲测试检测**
   - 扫描测试文件内容，检测反模式
   - `assert True` / `assert False`
   - `@skip` / `test.skip()`
   - 空测试（没有断言）

2. **GREEN 阶段限制**
   - 监控代码增量
   - 测试通过后，新增代码超过 50 行 → 警告
   - 测试通过后，新增函数超过 3 个 → 警告

3. **状态持久化**
   - 记录 TDD 阶段状态
   - 支持跨会话恢复
```

### 2.2 跨语言检测命令 (文档描述)

```markdown
## 测试状态检测命令

AI 根据文件类型选择合适的命令检测测试状态：

### Python

```bash
# 检测框架
if [ -f pytest.ini ] || grep -q "pytest" pyproject.toml; then
    framework="pytest"
    command="pytest tests/ --collect-only --quiet"
else
    framework="unittest"
    command="python -m unittest discover -s tests"
fi

# 运行检测
result=$(eval $command)

# 判断 RED 状态
# pytest: exit_code != 0 表示有测试
# unittest: 输出包含 "FAILED" 或 "ERROR"
```

### JavaScript

```bash
# 检测框架
if [ -f jest.config.js ] || grep -q '"test": "jest"' package.json; then
    framework="jest"
    command="npx jest --passWithNoTests --verbose"
elif [ -f mocha.opts ]; then
    framework="mocha"
    command="npx mocha --require ./test/setup.js"
fi

# 运行检测
result=$(eval $command)

# 判断 RED 状态
# 输出包含 "failing" 或 "FAIL" 或 exit_code != 0
```

### Dart

```bash
# 检测框架
if grep -q "flutter:" pubspec.yaml; then
    framework="flutter"
    command="flutter test --dry-run"
else
    framework="dart"
    command="dart test --dry-run"
fi

# 运行检测
result=$(eval $command)

# 判断 RED 状态
# 输出包含 "FAIL" 或 exit_code != 0
```
```

### 2.3 配置文件格式 (JSON Schema)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TDD Enforcer Configuration",
  "type": "object",
  "properties": {
    "enabled": {
      "type": "boolean",
      "default": true,
      "description": "是否启用 TDD 强制执行"
    },
    "strictness": {
      "type": "string",
      "enum": ["advisory", "strict", "superpowers"],
      "default": "advisory",
      "description": "严格度级别"
    },
    "skip_patterns": {
      "type": "array",
      "items": {"type": "string"},
      "default": ["**/*.md", "**/*.json", "**/config/**"],
      "description": "跳过检查的文件模式"
    },
    "test_patterns": {
      "type": "object",
      "description": "各语言的测试文件模式",
      "properties": {
        "python": {
          "type": "array",
          "items": {"type": "string"},
          "default": ["test_*.py", "*_test.py"]
        },
        "javascript": {
          "type": "array",
          "items": {"type": "string"},
          "default": ["*.test.js", "*.spec.js"]
        },
        "dart": {
          "type": "array",
          "items": {"type": "string"},
          "default": ["*_test.dart"]
        }
      }
    },
    "green_phase_limits": {
      "type": "object",
      "description": "GREEN 阶段限制 (仅 superpowers)",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": false
        },
        "max_lines_after_pass": {
          "type": "integer",
          "default": 50
        },
        "max_new_functions": {
          "type": "integer",
          "default": 3
        }
      }
    },
    "golden_testing_detection": {
      "type": "object",
      "description": "金装甲测试检测 (仅 superpowers)",
      "properties": {
        "enabled": {
          "type": "boolean",
          "default": false
        },
        "patterns": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "pattern": {"type": "string"},
              "description": {"type": "string"},
              "severity": {"type": "string", "enum": ["warning", "error"]}
            }
          },
          "default": [
            {"pattern": "assert True", "description": "永远通过的断言", "severity": "error"},
            {"pattern": "assert False", "description": "永远通过的断言", "severity": "error"},
            {"pattern": "@skip", "description": "跳过的测试", "severity": "warning"}
          ]
        }
      }
    }
  }
}
```

---

## 3. Hook 集成 (文档描述)

```markdown
## Hook 集成

### PreToolUse Hook

tdd-enforcer 通过 PreToolUse Hook 在 Write/Edit 操作前进行检查。

### Hook 配置 (hooks.json)

```json
{
  "name": "tdd-enforcer",
  "events": ["PreToolUse"],
  "description": "TDD 工作流强制执行",
  "handler": "tdd-enforcer"
}
```

### Hook 执行流程

1. **触发条件**：用户使用 Write 或 Edit 工具
2. **加载配置**：读取 `.claude/tdd-config.json`
3. **检查跳过**：匹配 `skip_patterns`
4. **检查文件类型**：跳过测试文件本身
5. **查找测试文件**：根据源文件路径查找对应测试
6. **应用严格度检查**：根据配置的级别执行检查
7. **返回结果**：Allow / Warn / Block
```

---

## 4. 与 Superpowers 对比

| 维度 | Superpowers | TDD Enforcer (新设计) |
|------|-------------|----------------------|
| **实现方式** | TypeScript 代码 | 文档描述 |
| **复杂度** | 中等 | 简洁 |
| **可维护性** | 需要改代码 | 需要改文档 |
| **Token 效率** | 中等 | 高 |
| **严格度级别** | 单一 | 三级 (可配置) |
| **语言支持** | TypeScript/JS | 多语言 |
| **缓存机制** | 无 | 有 (文档描述) |
| **企业集成** | 无 | 十步循环集成 |

**新设计优势**：
- ✅ 符合 Agent Skills 设计原则
- ✅ 修改简单，无需编程
- ✅ Token 效率更高
- ✅ 易于维护和扩展

---

## 5. 实施计划

### Phase 1: 文档重构 (本周)

```
任务:
  [ ] 重写 SKILL.md (文档驱动设计)
  [ ] 更新 EXAMPLES.md
  [ ] 编写 references/ 详细文档
  [ ] 删除所有 Python 实现代码
  [ ] 更新 tdd-config-schema.json
```

### Phase 2: 示例更新

```
任务:
  [ ] 更新 Python 示例
  [ ] 更新 JavaScript 示例
  [ ] 更新 Dart 示例
  [ ] 添加配置文件示例
```

### Phase 3: 验证和发布

```
任务:
  [ ] 文档审查
  [ ] 示例测试
  [ ] v2.0.0 发布
```

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | - 符合 Skill 设计原则<br>- 文档比代码更易维护<br>- Token 效率更高<br>- 修改简单无需编程 |
| **Risk** | 无 | 文档描述方式已在 Superpowers 验证 |
| **Breaking** | 无 | 功能保持不变，只是实现方式改变 |

---

## Key Deliverables

```
aria/skills/tdd-enforcer/
├── SKILL.md                    # 重写: 文档驱动设计
├── EXAMPLES.md                 # 更新: 使用示例
└── references/                 # 新增: 详细参考文档
    ├── strictness-levels.md
    ├── red-state-detection.md
    ├── green-phase-check.md
    └── migration-guide.md

examples/
├── python/                     # 更新配置
├── javascript/                 # 更新配置
└── dart/                       # 更新配置
```

---

## Success Criteria

- [ ] SKILL.md < 500 行
- [ ] 文档清晰描述三级严格度
- [ ] 跨语言检测命令示例完整
- [ ] 配置 JSON Schema 准确
- [ ] 示例项目可运行
- [ ] 删除所有 Python 实现代码
- [ ] 符合 Agent Skills 设计原则

---

## References

- [Superpowers test-driven-development](https://github.com/obra/superpowers)
- [Agent Skills 规范](https://agentskills.io/specification)
- [Aria vs Superpowers 分析](../../../docs/analysis/superpowers-vs-aria.md)

---

**Maintained By**: 10CG Lab
**Spec Level**: Full (Level 3)
**Estimate**: 8-16h (2天)
**Priority**: High
**Version**: 2.0 (设计重构)
