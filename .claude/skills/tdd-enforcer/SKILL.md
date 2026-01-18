---
name: tdd-enforcer
description: |
  强制执行测试驱动开发 (TDD) 工作流程。

  确保 RED-GREEN-REFACTOR 循环的正确执行：
  - RED: 先编写失败测试
  - GREEN: 编写最小实现使测试通过
  - REFACTOR: 重构优化代码质量

  使用场景：需要强制测试先于代码的开发任务。
---

# TDD 强制执行器 (TDD Enforcer)

> **版本**: 1.0.0 | **十步循环**: B.2 (验证执行)

## 快速开始

### 我应该使用这个 skill 吗？

**使用场景**:
- 需要严格遵循 TDD 流程的开发任务
- 测试覆盖率有明确要求的项目
- 需要防止"补测试"反模式

**不使用场景**:
- 仅文档修改
- 紧急 hotfix（可使用 `--bypass` 跳过）

---

## 核心功能

| 功能 | 描述 |
|------|------|
| RED 强制 | 编写业务代码前必须存在失败测试 |
| GREEN 验证 | 最小实现，仅满足测试要求 |
| REFACTOR 引导 | 测试保护下的安全重构 |
| 删除保护 | 删除测试前检查代码依赖 |

---

## TDD 工作流程

```yaml
RED (编写测试):
  前置条件:
    - 无对应业务代码存在
  输出:
    - 失败的测试用例
    - 明确的失败原因

GREEN (最小实现):
  前置条件:
    - 测试用例已存在且失败
  规则:
    - 仅编写使测试通过的最小代码
    - 不考虑未来需求
    - 不进行优化
  输出:
    - 通过的测试用例

REFACTOR (重构优化):
  前置条件:
    - 所有测试通过
  规则:
    - 在测试保护下修改代码
    - 保持功能不变
    - 改善代码结构和可读性
  输出:
    - 仍通过所有测试
    - 更好的代码质量
```

---

## 强制规则

### 规则 1: 测试先于代码

**触发条件**: 用户尝试 Write/Edit 业务代码文件

**验证逻辑**:
```python
def verify_test_first(file_path):
    # 检查是否存在对应的测试文件
    test_file = find_test_file(file_path)

    if not test_file.exists():
        BLOCK("请先编写测试用例")
        return False

    # 检查测试是否失败
    if test_file.status == "passing":
        WARN("测试已通过，请进入 REFACTOR 阶段")
        return True

    return True  # 测试失败，可以进行 GREEN 阶段
```

**测试文件映射**:
| 业务代码 | 测试文件 |
|----------|----------|
| `lib/foo.dart` | `test/lib/foo_test.dart` |
| `src/service.py` | `tests/test_service.py` |
| `components/Button.tsx` | `components/Button.test.tsx` |

### 规则 2: 删除保护

**触发条件**: 用户尝试删除测试代码

**验证逻辑**:
```python
def verify_test_deletion(test_file_path):
    # 查找依赖此测试的代码
    dependencies = find_code_dependents(test_file_path)

    if dependencies:
        BLOCK(f"无法删除: {len(dependencies)} 个文件依赖此测试")
        SHOW_DEPENDENCIES(dependencies)
        return False

    CONFIRM("确认删除测试？")
    return True
```

---

## 使用方式

### 激活 TDD 模式

```
你正在 TDD 模式下工作。
当前阶段: RED

在编写业务代码前，请先编写测试用例。
```

### 阶段转换

```yaml
进入 GREEN 阶段:
  条件: 测试用例编写完成且失败
  指导: "编写最小实现使测试通过"

进入 REFACTOR 阶段:
  条件: 所有测试通过
  指导: "在测试保护下重构代码"

完成 TDD 循环:
  条件: 重构完成，测试仍然通过
  指导: "TDD 循环完成，可以继续下一个功能"
```

---

## 跳过机制

### 紧急绕过

```yaml
--bypass flag:
  使用场景: 紧急 hotfix、调试代码
  要求: 明确说明跳过原因
  记录: 标记为"技术债务"，需后续补齐
```

---

## 检查清单

### RED 阶段
- [ ] 测试用例已编写
- [ ] 测试运行失败（预期失败）
- [ ] 失败原因明确

### GREEN 阶段
- [ ] 仅编写最小实现
- [ ] 测试通过
- [ ] 无额外功能

### REFACTOR 阶段
- [ ] 代码结构改善
- [ ] 测试仍然通过
- [ ] 功能行为不变

---

## 示例

### 示例 1: 新功能开发

```yaml
用户请求: "添加用户登录功能"

TDD Enforcer 响应:
  1. 检查是否存在登录测试文件
  2. 不存在 → 引导进入 RED 阶段
  3. 用户编写测试 → 测试失败 ✓
  4. 进入 GREEN 阶段 → 用户编写实现
  5. 测试通过 → 进入 REFACTOR 阶段
  6. 重构完成 → TDD 循环结束
```

### 示例 2: 修复 Bug

```yaml
用户请求: "修复登录页面的崩溃问题"

TDD Enforcer 响应:
  1. 引导编写复现 bug 的测试
  2. 测试失败（复现 bug）✓
  3. 引导编写修复代码
  4. 测试通过 → bug 修复
  5. 检查是否有其他测试被破坏
```

---

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `test_first` | `strict` | strict | warn | off |
| `delete_protect` | `true` | 是否启用删除保护 |
| `test_patterns` | 自动检测 | 测试文件匹配模式 |

---

## 错误处理

| 场景 | 行为 |
|------|------|
| 无法找到测试文件 | 提示测试文件位置 |
| 测试一直失败 | 建议检查测试逻辑 |
| 删除被依赖的测试 | 阻止并显示依赖链 |

---

## 相关文档

### 参考
- [Superpowers test-driven-development](https://github.com/obra/superpowers)
- [TDD 最佳实践](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

### Aria 相关
- [phase-b-developer](../phase-b-developer/SKILL.md) - 开发执行阶段
- [commit-msg-generator](../commit-msg-generator/SKILL.md) - 提交消息生成

---

**版本**: 1.0.0
**创建**: 2026-01-18
**提案**: aria-workflow-enhancement
**状态**: Draft
