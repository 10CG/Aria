# Commit Message Generator Benchmark Tests

> **版本**: 1.0.0
> **目标 Skill**: aria/skills/commit-msg-generator (v2.0.1)

## 📋 概述

本目录包含 `commit-msg-generator` skill 的基准测试用例，用于验证 skill 生成的 commit 消息是否符合 Conventional Commits 规范和项目的增强标记格式。

## 📁 目录结构

```
commit-msg-generator/
├── README.md                 # 本文档
├── evals/
│   ├── evals.json           # 测试用例定义
│   └── validate_commit.py   # 验证脚本
├── iteration-1/             # 第一次迭代结果
│   ├── eval-1/
│   │   ├── with_skill/
│   │   │   ├── outputs/
│   │   │   └── timing.json
│   │   ├── without_skill/
│   │   │   ├── outputs/
│   │   │   └── timing.json
│   │   └── eval_metadata.json
│   └── benchmark.json
└── results/                  # 历史结果归档
```

## 🎯 测试用例分类

### 独立模式 (Independent Mode)
日常开发提交，无增强标记：

| ID | 名称 | 描述 |
|----|------|------|
| 1 | simple-feat-add-files | 新功能添加 |
| 2 | bugfix-typo-fix | Bug 修复 |
| 3 | docs-update-only | 文档更新 |
| 4 | refactor-code-restructure | 代码重构 |
| 10 | test-addition | 测试添加 |
| 12 | chore-config | 配置更新 |

### 编排模式 (Orchestrated Mode)
被 strategic-commit-orchestrator 调用，带增强标记：

| ID | 名称 | 描述 |
|----|------|------|
| 5 | orchestrated-mode-full-params | 完整参数增强标记 |
| 6 | orchestrated-mobile-developer | 移动端开发者场景 |

### 特殊场景 (Special Cases)

| ID | 名称 | 描述 |
|----|------|------|
| 7 | breaking-change-api | Breaking Change 声明 |
| 8 | closes-issue | Closes Issue 关联 |
| 9 | refs-document | Refs 文档引用 |

### 格式验证 (Format Validation)

| ID | 名称 | 描述 |
|----|------|------|
| 13 | enhanced-marker-format-validation | 增强标记格式验证 |
| 15 | conventional-commits-compliance | Conventional Commits 合规 |

### Scope 检测 (Scope Detection)

| ID | 名称 | 描述 |
|----|------|------|
| 14 | scope-extraction-path-based | 从文件路径提取 scope |

## 🔬 断言类型

### Critical 级别 (必须通过)
- `type_is_*` - Commit 类型正确性
- `scope_is_*` - Scope 正确性
- `*_format` - 格式规范
- `closes_footer` - Closes 关键字

### High 级别
- `subject_length` - Subject 长度限制
- `imperative_mood` - 祈使语气
- `scope_from_path` - Scope 路径提取

### Medium 级别
- `has_body` - Body 存在性
- `subject_concise` - Subject 简洁性

## 🚀 运行测试

### 方法 1: 使用验证脚本

```bash
# 验证单个 commit 消息
python evals/validate_commit.py <commit_message_file> <eval_id>

# 批量验证
python evals/validate_commit.py --all <commit_messages_dir>
```

### 方法 2: 使用 skill-creator 流程

1. **创建工作区**
   ```bash
   mkdir -p iteration-1/eval-{1..15}/{with_skill,without_skill}/outputs
   ```

2. **运行测试** (使用 subagent)
   ```
   让 Claude 使用 commit-msg-generator skill 执行每个 eval 的 prompt
   ```

3. **验证结果**
   ```bash
   python evals/validate_commit.py --all iteration-1/
   ```

## 📊 评估指标

| 指标 | 目标 | 说明 |
|------|------|------|
| Pass Rate (Critical) | ≥95% | Critical 断言通过率 |
| Pass Rate (All) | ≥90% | 所有断言通过率 |
| Format Compliance | 100% | Conventional Commits 格式合规 |
| Enhanced Markers | 100% | 增强标记格式正确性 |

## 🔧 断言语法

测试用例使用简化的断言语法：

```yaml
# 消息匹配
commit_message.matches(/^feat\(/)

# 消息包含
commit_message.includes('text')

# 长度检查
first_line_length <= 50

# 索引比较
commit_message.indexOf('X') < commit_message.indexOf('Y')

# 分割长度
commit_message.split('\n\n').length >= 2

# 布尔组合
!commit_message.match(/^feat/) || subject.match(/^fix/)
```

## 📝 示例输出

### 通过的测试

```
[✅ PASS] Eval 1: simple-feat-add-files
    [✓] A1: type_is_feat (critical)
    [✓] A2: scope_is_auth (high)
    [✓] A3: subject_length (high)
    [✓] A4: imperative_mood (medium)
    [✓] A5: no_enhanced_markers (high)
```

### 失败的测试

```
[❌ FAIL] Eval 8: closes-issue
    [✓] A2: type_is_fix (critical)
    [✗] A1: closes_footer (critical)
        Expected: Closes #123 in footer
        Actual: No Closes footer found
```

## 🔄 迭代工作流

1. **Iteration 1**: 基线测试，收集当前 skill 表现
2. **分析**: 识别失败的测试和常见问题
3. **优化**: 更新 skill 文档或逻辑
4. **Iteration 2**: 重新测试，验证改进
5. **重复**直到满足目标指标

## 📚 相关文档

- [commit-msg-generator SKILL.md](../../../aria/skills/commit-msg-generator/SKILL.md)
- [ENHANCED_MARKERS_SPEC.md](../../../aria/skills/commit-msg-generator/ENHANCED_MARKERS_SPEC.md)
- [COMMIT_FOOTER_GUIDE.md](../../../aria/skills/commit-msg-generator/COMMIT_FOOTER_GUIDE.md)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**创建**: 2026-03-13
**维护者**: Aria Benchmark Team
