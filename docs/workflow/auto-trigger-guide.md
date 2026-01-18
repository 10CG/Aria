# 自动触发系统用户指南

> **版本**: 1.0.0
> **来源**: TASK-016
> **配置文件**: `.claude/CLAUDE.md`, `.claude/trigger-rules.json`

---

## 目录

1. [概述](#概述)
2. [工作原理](#工作原理)
3. [配置规则](#配置规则)
4. [使用示例](#使用示例)
5. [故障排除](#故障排除)
6. [自定义规则](#自定义规则)

---

## 概述

自动触发系统根据用户输入的**意图关键词**自动激活对应的 Skill，无需显式调用。

### 优势

- ✅ 降低认知负担 - 记住意图而非 Skill 名称
- ✅ 提高开发效率 - 自动选择正确的工具
- ✅ 减少错误 - 避免使用错误的 Skill

### 基本流程

```
用户输入 → 关键词提取 → 意图匹配 → Skill 激活 → 执行任务
```

---

## 工作原理

### 1. 关键词检测

系统扫描用户输入，查找预定义的关键词：

```yaml
用户输入: "创建一个测试用于登录功能"

关键词检测:
  - "创建" → context boost
  - "测试" → "testing" skill (weight: 0.9)

匹配结果:
  - testing: 0.9 (基础)
  - + 0.1 (上下文: "创建")
  - = 1.0 (置信度)
```

### 2. 置信度计算

```python
confidence = base_weight + context_boost + match_bonus

其中:
  base_weight: 关键词的基础权重 (0-1)
  context_boost: 上下文加成 (最多 +0.2)
  match_bonus: 多关键词匹配加成 (+0.1 per extra keyword)
```

### 3. 触发决策

```yaml
置信度 >= 0.8: 自动激活 Skill
0.6 <= 置信度 < 0.8: 请求用户确认
置信度 < 0.6: 不触发
```

---

## 配置规则

### 规则文件位置

```
.claude/
├── CLAUDE.md              # 主配置文件
└── trigger-rules.json     # 详细规则配置
```

### 规则格式

```json
{
  "rules": {
    "skill_name": {
      "keywords": [
        {"word": "keyword", "weight": 0.9}
      ],
      "context_boost": {
        "before": ["create", "write"],
        "after": ["first", "before"]
      }
    }
  }
}
```

### 预配置的 Skill 触发

| 意图 | 关键词 | 触发 Skill | 置信度 |
|------|--------|-----------|--------|
| 编写测试 | test, 测试, tdd | tdd-enforcer | 0.9-1.0 |
| 创建分支 | branch, 分支 | branch-manager | 0.9 |
| 提交代码 | commit, 提交 | commit-msg-generator | 0.8 |
| 规划任务 | plan, 规划 | task-planner | 0.85 |
| 查看状态 | state, 状态 | state-scanner | 0.9 |
| 代码评审 | review, 评审 | phase-b-developer | 0.85 |

---

## 使用示例

### 示例 1: 自动触发 TDD Enforcer

```
你: 写一个测试用于用户登录

系统: [自动激活 tdd-enforcer skill]

    📝 TDD Enforcer 已激活
    当前阶段: RED

    请先编写测试用例，然后再实现功能。

    你想为哪个功能编写测试？
```

### 示例 2: 自动触发 Branch Manager

```
你: 创建一个新分支用于登录功能

系统: [自动激活 branch-manager skill]

    🌿 Branch Manager 已激活

    请提供以下信息:
    - 模块: mobile, backend, 或其他?
    - 任务ID: TASK-XXX
    - 描述: login-feature
```

### 示例 3: 低置信度请求确认

```
你: 帮我处理代码

系统: [检测到多个可能的 skills]

    检测到多个匹配:
    1. phase-b-developer (置信度: 0.75)
    2. code-quality (置信度: 0.70)

    请选择要使用的 Skill，或提供更多细节。
```

---

## 故障排除

### 问题 1: Skill 没有自动触发

**可能原因**:
- 关键词不在规则列表中
- 置信度低于阈值
- 自动触发被禁用

**解决方案**:
```bash
# 检查自动触发状态
echo $CLAUDE_AUTO_TRIGGER  # 应该为 "true" 或未设置

# 查看匹配日志（开发模式）
export CLAUDE_DEBUG_MATCH=true
```

### 问题 2: 触发了错误的 Skill

**可能原因**:
- 关键词冲突
- 上下文未正确识别

**解决方案**:
```
使用 NO_AUTO_TRIGGER 禁用自动触发
然后显式调用 Skill:
  /branch-manager
  /tdd-enforcer
```

### 问题 3: 需要临时禁用

**解决方案**:
```bash
# 临时禁用
export CLAUDE_AUTO_TRIGGER=false

# 或在请求前加
NO_AUTO_TRIGGER
创建一个文件...
```

---

## 自定义规则

### 添加新规则

编辑 `.claude/trigger-rules.json`:

```json
{
  "rules": {
    "my-custom-skill": {
      "keywords": [
        {"word": "deploy", "weight": 0.9},
        {"word": "部署", "weight": 0.9}
      ],
      "context_boost": {
        "before": ["help", "please"],
        "after": ["to", "to"]
      }
    }
  }
}
```

### 调整置信度阈值

编辑 `.claude/trigger-rules.json`:

```json
{
  "matching": {
    "thresholds": {
      "auto_trigger": 0.8,   // 自动触发阈值
      "confirm_trigger": 0.6, // 确认阈值
      "no_trigger": 0.0
    }
  }
}
```

### 添加上下文加成

```json
{
  "context_boost": {
    "before": ["create", "write", "add"],  // 前置词
    "after": ["for", "with", "to"]         // 后置词
  }
}
```

---

## 最佳实践

### 1. 关键词选择

- ✅ 使用独特的词: "worktree" 比 "tree" 更好
- ✅ 中英文双语: 同时支持中英文
- ✅ 避免通用词: "do" 太通用，"do test" 更好

### 2. 权重设置

| 场景 | 建议权重 |
|------|----------|
| 完全匹配 | 1.0 |
| 强关键词 | 0.9 |
| 常用关键词 | 0.8 |
| 弱关键词 | 0.6 |

### 3. 上下文加成

- 为常用组合添加加成
- "create test" 比 "test" 更明确
- 最大加成: +0.2

---

## 配置文件完整示例

### CLAUDE.md

```markdown
# 自动触发规则

| 关键词 | 触发 Skill | 置信度 |
|--------|-----------|--------|
| test | tdd-enforcer | 0.9 |
| branch | branch-manager | 0.9 |

详细配置见: trigger-rules.json
```

### trigger-rules.json

```json
{
  "version": "1.0.0",
  "confidence_threshold": 0.8,
  "rules": {
    "testing": {
      "skill": "tdd-enforcer",
      "keywords": [
        {"word": "test", "weight": 0.9},
        {"word": "tdd", "weight": 1.0}
      ]
    }
  }
}
```

---

## 开发者参考

### 匹配算法

```python
def match_intent(user_input: str) -> Optional[str]:
    results = []

    for skill, rule in RULES.items():
        for keyword in rule["keywords"]:
            if keyword["word"] in user_input.lower():
                confidence = calculate_confidence(user_input, keyword)
                results.append((skill, confidence))

    if not results:
        return None

    results.sort(key=lambda x: x[1], reverse=True)
    top_skill, top_confidence = results[0]

    if top_confidence >= AUTO_TRIGGER_THRESHOLD:
        return top_skill
    elif top_confidence >= CONFIRM_THRESHOLD:
        return request_confirmation(results)
    else:
        return None
```

### 调试模式

```bash
# 启用调试输出
export CLAUDE_AUTO_TRIGGER_DEBUG=true

# 查看匹配详情
# 输出会显示每个关键词的匹配分数和最终置信度
```

---

**版本**: 1.0.0
**创建**: 2026-01-18
**相关**: [CLAUDE.md](../.claude/CLAUDE.md) | [trigger-rules.json](../.claude/trigger-rules.json)
