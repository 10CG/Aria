# 集成测试覆盖

> **版本**: 1.0.0
> **来源**: TASK-030
> **提案**: aria-workflow-enhancement

---

## 概述

本文档定义 `aria-workflow-enhancement` 的集成测试策略和测试用例。

---

## 测试策略

### 测试层级

```
┌─────────────────────────────────────────────────────────┐
│                     E2E 测试                            │
│  (完整工作流验证，需要实际运行环境)                     │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                   集成测试                              │
│  (组件间交互验证，部分需要实际环境)                     │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                   单元测试                              │
│  (独立功能验证，无需实际环境)                            │
└─────────────────────────────────────────────────────────┘
```

### 测试覆盖范围

| 功能 | 单元测试 | 集成测试 | E2E 测试 |
|------|----------|----------|----------|
| TDD Enforcer | ✅ | ⚠️ 需环境 | ❌ |
| Git Worktrees | ✅ | ✅ | ❌ |
| 自动触发 | ✅ | ⚠️ 需环境 | ❌ |
| 两阶段评审 | ✅ | ✅ | ❌ |
| Hooks 系统 | ✅ | ⚠️ 需环境 | ❌ |

---

## 单元测试

### 1. 自动触发匹配测试

**文件**: `tests/auto-trigger/test_matching.py`

```python
class TestAutoTriggerMatching:
    def test_tdd_keywords_match(self):
        results = matcher.match("write a test")
        assert results[0][0] == "testing"
        assert results[0][1] >= 0.9

    def test_confidence_threshold(self):
        results = matcher.match("hello world")
        assert len(results) == 0 or results[0][1] < 0.6
```

### 2. Worktree 脚本测试

```bash
# test_worktree_scripts.sh
#!/bin/bash

echo "Testing worktree-create.sh..."

# 测试创建
./worktree-create.sh test-branch
[ -d ".git/worktrees/test-branch" ] && echo "✓ Create passed"

# 测试清理
./worktree-cleanup.sh test-branch
[ ! -d ".git/worktrees/test-branch" ] && echo "✓ Cleanup passed"

echo "All worktree script tests passed!"
```

### 3. Hooks 配置验证

```python
import json

def test_hooks_config_schema():
    """验证 hooks.json 配置格式"""
    with open("aria/hooks/hooks.json") as f:
        config = json.load(f)

    assert config["version"] == "1.0.0"
    assert "session-start" in config["hooks"]
    assert config["hooks"]["session-start"]["enabled"] in [True, False]
```

---

## 集成测试

### 1. Worktree 完整流程测试

```bash
#!/bin/bash
# test-worktree-workflow.sh

echo "=== Worktree 完整流程测试 ==="

# 1. 创建 worktree
echo "1. 创建 worktree..."
./worktree-create.sh feature/test-workflow
[ $? -eq 0 ] || exit 1

# 2. 切换到 worktree
echo "2. 切换 worktree..."
./worktree-switch.sh test-workflow
CURRENT=$(./worktree-status.sh | grep "current" | awk '{print $2}')
[ "$CURRENT" = "test-workflow" ] || exit 1

# 3. 在 worktree 中工作
echo "3. 在 worktree 中工作..."
cd .git/worktrees/test-workflow
echo "test content" > test-file.txt
cd ../..

# 4. 检查状态
echo "4. 检查状态..."
./worktree-status.sh | grep "dirty"

# 5. 清理
echo "5. 清理 worktree..."
./worktree-cleanup.sh test-workflow
[ ! -d ".git/worktrees/test-workflow" ] || exit 1

echo "✓ Worktree 流程测试通过!"
```

### 2. 两阶段评审集成测试

```python
import subprocess

def test_two_phase_review():
    """测试两阶段评审流程"""

    # Phase 1: 规范合规性
    result = subprocess.run(
        ["python", "validators/spec-compliance.py"],
        capture_output=True
    )
    assert result.returncode == 0 or "warning" in result.stdout.decode()

    # Phase 2: 代码质量
    result = subprocess.run(
        ["python", "validators/code-quality.py"],
        capture_output=True
    )
    assert result.returncode == 0 or "warning" in result.stdout.decode()
```

### 3. 自动触发端到端测试

```python
def test_auto_trigger_e2e():
    """测试自动触发完整流程"""

    # 模拟用户输入
    user_inputs = [
        "创建一个测试",
        "规划这个功能",
        "查看当前状态",
        "创建新分支"
    ]

    expected_skills = [
        "tdd-enforcer",
        "task-planner",
        "state-scanner",
        "branch-manager"
    ]

    for user_input, expected_skill in zip(user_inputs, expected_skills):
        results = matcher.match(user_input)
        assert results[0][0] == expected_skill
```

---

## E2E 测试（需要实际环境）

### 测试场景

以下测试需要在实际的 Claude Code 环境中运行：

#### 场景 1: 完整开发流程

```yaml
场景: 使用新工作流完成一个功能
步骤:
  1. 用户: "创建用户登录功能"
  2. 系统: [自动激活 spec-drafter 或 state-scanner]
  3. 用户: "编写测试"
  4. 系统: [激活 tdd-enforcer]
  5. 用户: "创建分支"
  6. 系统: [激活 branch-manager with worktree]
  7. ...完成开发
  8. 系统: [phase-b-developer 两阶段评审]

预期结果:
  - 正确的 Skill 按顺序激活
  - Worktree 正确创建和清理
  - 评审报告正确生成
```

#### 场景 2: Worktree 并行开发

```yaml
场景: 同时在多个 worktree 中工作
步骤:
  1. 创建 worktree-1
  2. 创建 worktree-2
  3. 在 worktree-1 中开发
  4. 切换到 worktree-2 继续开发
  5. 完成后清理所有 worktrees

预期结果:
  - Worktrees 互不干扰
  - 切换正确
  - 清理无残留
```

---

## 测试执行

### 运行单元测试

```bash
# Python 测试
pytest tests/ -v

# Shell 脚本测试
bash tests/workflow/test-worktree-scripts.sh

# 配置验证
python tests/validate_config.py
```

### 运行集成测试

```bash
# Worktree 流程测试
bash tests/integration/test-worktree-workflow.sh

# 两阶段评审测试
python tests/integration/test-two-phase-review.py
```

### 运行覆盖率检查

```bash
# Python 覆盖率
pytest --cov=. --cov-report=html

# 检查覆盖率是否 >= 85%
coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//' | \
  awk '{if ($1 < 85) exit 1; else exit 0}'
```

---

## 测试数据

### 测试分支命名

| 模式 | 示例 |
|------|------|
| feature | `feature/mobile/TASK-001-login` |
| bugfix | `bugfix/backend/ISSUE-42-crash` |
| hotfix | `hotfix/v1.2.1-security` |

### 测试 Worktree 路径

| 路径 | 说明 |
|------|------|
| `.git/worktrees/TASK-001` | 单任务 worktree |
| `.git/worktrees/feature-name` | 功能 worktree |

---

## 持续集成配置

### GitHub Actions (示例)

```yaml
name: Aria Workflow Enhancement Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Python tests
        run: |
          pip install pytest
          pytest tests/ -v

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run worktree tests
        run: bash tests/integration/test-worktree-workflow.sh

  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check coverage
        run: |
          pip install pytest pytest-cov
          pytest --cov=. --cov-report=xml
          # 检查覆盖率 >= 85%
```

---

## 测试报告

### 报告格式

```yaml
测试报告:
  timestamp: "2026-01-18T10:30:00Z"
  total_tests: 25
  passed: 24
  failed: 1
  skipped: 0
  coverage: 87.5%

  失败测试:
    - name: "test_worktree_create"
      error: "目录已存在"
      suggestion: "清理后重试"

  覆盖率:
    unit: 90%
    integration: 75%
    overall: 87.5%
```

---

## 测试检查清单

### 功能测试

- [ ] TDD Enforcer 工作流程正确
- [ ] Worktree 创建/切换/清理正确
- [ ] 自动触发匹配准确率 >= 80%
- [ ] 两阶段评审正确区分警告和阻塞
- [ ] Hooks 配置加载正确

### 兼容性测试

- [ ] 现有 Skills 仍然可用
- [ ] 现有工作流程不受影响
- [ ] 配置缺失时使用默认值
- [ ] 多种 Git 版本兼容

### 性能测试

- [ ] 自动触发响应时间 < 100ms
- [ ] Hooks 执行时间 < 30 秒
- [ ] Worktree 操作无明显延迟

---

**版本**: 1.0.0
**创建**: 2026-01-18
**相关**: [用户验收测试](./acceptance-report.md)
