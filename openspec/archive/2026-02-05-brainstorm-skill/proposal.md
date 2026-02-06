# Brainstorm Skill - AI-DDD 协作思考引擎

> **Level**: Full (Level 3 Spec)
> **Status**: Completed
> **Created**: 2026-02-05
> **Reference**: [Superpowers brainstorming](https://github.com/obra/superpowers)
> **Design Docs**: [brainstorming-in-ai-ddd.md](../../docs/analysis/brainstorming-in-ai-ddd.md)

---

## Why

### 核心问题：缺少"协作思考"环节

当前 Aria 方法论的执行流程是：

```
人类思考 → 写文档 → AI 读取理解 → 执行
```

这种模式存在根本性问题：

1. **文档是思考结果的固化**，而非思考过程的记录
2. **AI 无法参与"为什么"的讨论**，只能在"做什么"上执行
3. **决策理由丢失**，后期无法追溯"为什么选A而非B"
4. **需求澄清不足**，过早进入实现导致返工

### 核心洞察：AI-DDD 需要的不是文档工具，而是思考工具

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    传统模式 vs AI-DDD 模式                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  传统模式:                              AI-DDD 模式:                      │
│  ┌─────────┐      ┌─────────┐          ┌─────────────────────────┐      │
│  │ 人类    │ ────▶ │ 文档    │          │ 人类 + AI 协作思考       │      │
│  │ 思考    │      │ (结果)  │          │      ↓                  │      │
│  └─────────┘      └─────────┘          │ 共同理解                  │      │
│       □                                   │      ↓                  │      │
│  AI 无法参与                              │ 文档 (思考过程的记录)    │      │
│                                           │      ↓                  │      │
│                                           │ 执行                    │      │
│                                           └─────────────────────────┘      │
│                                                                         │
│  关键差异: 头脑风暴不是"附加功能"，而是 AI-DDD 的核心载体                │
└─────────────────────────────────────────────────────────────────────────┘
```

### Superpowers 的启示

Superpowers 项目有一个 `brainstorm` skill，但它的定位是**技术讨论工具**：

```
用户提出想法 → brainstorm 对话 → 直接写代码
```

Aria 需要更全面的定位：

```
问题空间探索 → 需求分解 → 技术方案设计 → 文档生成
     ↓            ↓            ↓
  problem    requirements   technical
    模式         模式          模式
```

### 当前 Aria 的缺失

| 阶段 | 当前状态 | 缺失 |
|------|----------|------|
| A.0 状态扫描 | ✅ 实现 | 无法触发头脑风暴 |
| A.0.5 需求澄清 | ❌ 缺失 | **没有问题空间探索环节** |
| A.1 规范创建 | ✅ spec-drafter | 无交互式讨论，直接生成文档 |
| A.2 任务规划 | ✅ task-planner | 基于不充分的输入 |
| 决策记录 | ❌ 缺失 | **没有"为什么"的记录** |

---

## What

创建 `brainstorm` skill，作为 AI-DDD 协作思考的核心载体，实现三层头脑风暴体系。

### 核心变更

| 技能 | 类型 | 说明 |
|------|------|------|
| **brainstorm** | 新增 | AI-DDD 协作思考引擎，三种模式 |
| **state-scanner** | 增强 | 集成头脑风暴推荐 |
| **spec-drafter** | 增强 | 内置头脑风暴流程 |
| **决策记录** | 新增 | 结构化决策日志系统 |

### 三层模式架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Brainstorm Skill 三层架构                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Level 1: problem 模式                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 触发: 用户提出模糊想法                                           │    │
│  │ 目标: 澄清真需求 vs 伪需求                                       │    │
│  │ 输出: problem-definition.md + 决策:是否需要 PRD                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              ↓                                          │
│  Level 2: requirements 模式                                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 触发: PRD 创建/细化                                              │    │
│  │ 目标: 分解 User Stories + 优先级排序                             │    │
│  │ 输出: user-stories/US-*.md + 优先级矩阵                          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              ↓                                          │
│  Level 3: technical 模式                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 触发: OpenSpec 创建前                                            │    │
│  │ 目标: 技术选型 + 方案对比                                        │    │
│  │ 输出: decision-log.md + proposal.md (草案)                       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 与十步循环集成

```
修改后的十步循环:

A. 规划阶段
├── A.0 状态扫描
│   └── [智能推荐] → 发现模糊需求
│       ↓
├── A.0.5 问题空间头脑风暴 ← 新增
│   └── 澄清: 是真需求还是伪需求?
│       ↓
├── A.1 规范创建
│   ├── PRD 创建 (可选)
│   │   └── [内置 requirements 模式头脑风暴]
│   └── OpenSpec 创建
│       └── [内置 technical 模式头脑风暴]
├── A.2 任务规划 (基于头脑风暴结果，更准确)
└── A.3 Agent 分配

B. 开发阶段
C. 集成阶段
D. 收尾阶段
```

---

## 1. Brainstorm Skill 规范

### 1.1 对话状态机

```yaml
状态流转:
  INIT → CLARIFY → EXPLORE → CONVERGE → SUMMARY → COMPLETE

  INIT:
    入口: 对话开始
    动作: 加载上下文，选择引导模板
    出口: 用户首次响应

  CLARIFY:
    目标: 统一术语，明确概念
    动作: 识别模糊术语，请求定义
    出口: 关键术语已定义

  EXPLORE:
    目标: 探索选项，分析约束
    动作: 列举方案，收集约束，过滤不可行
    出口: 可行方案已明确

  CONVERGE:
    目标: 方案对比，做出选择
    动作: 多维度对比，风险评估
    出口: 明确选择或达成共识

  SUMMARY:
    目标: 总结决策，记录理由
    动作: 生成决策记录
    出口: 用户确认

  COMPLETE:
    动作: 写入日志，同步文档
```

### 1.2 深度控制指标

```yaml
对话指标:
  fuzziness: 模糊度 0-1 (输入的清晰程度)
  coverage: 覆盖面 0-1 (讨论的完整性)
  consensus: 共识度 0-1 (意见一致程度)

深度判断:
  shallow:  coverage < 0.5 → 继续探索
  adequate: coverage >= 0.5 && consensus >= 0.7 → 可以收敛
  deep:     coverage >= 0.7 && consensus >= 0.8 → 应该收敛

最大轮次:
  problem: 10 轮
  requirements: 15 轮
  technical: 8 轮
```

### 1.3 决策记录格式

```markdown
## 决策: DEC-001 - AI 客服技术方案

> **日期**: 2026-02-05
> **模式**: technical
> **状态**: Active
> **可撤销**: 是 (v2.0 前)

### 背景
{{决策的背景和上下文}}

### 约束条件
| 类型 | 约束 | 影响 |
|------|------|------|
| business | 预算 < $500/月 | 排除昂贵托管服务 |
| technical | 私有化部署 | 需要自建 RAG |

### 考虑的方案
| 方案 | 评分 | 可行性 | 理由 |
|------|------|--------|------|
| A: OpenAI API | ❌ | 不可行 | 数据出境 |
| B: 自建 RAG | ✅ | 可行 | 满足约束 |
| C: 混合方案 | ⭐ | 备选 | 复杂度高 |

### 最终选择
**方案 B**: 自建 RAG (FAISS + 本地模型)

### 理由
1. 满足合规要求 (数据不出境)
2. 成本可控
3. 满足初期性能需求

### 假设条件
- 初期 QPS < 100
- 文档总量 < 10万条

### 风险与缓解
| 风险 | 缓解措施 |
|------|----------|
| 增量更新复杂 | 预留迁移接口 |
| 模型效果不佳 | 定期评估托管选项 |
```

### 1.4 约束管理系统

```yaml
约束分类:
  business:
    - budget: 预算限制
    - timeline: 时间限制
    - compliance: 合规要求

  technical:
    - architecture: 架构约束
    - tech_stack: 技术栈限制
    - performance: 性能要求

  team:
    - skills: 团队技能
    - capacity: 可用工时

约束验证流程:
  1. 收集约束 (配置 + 对话)
  2. 方案过滤 (硬约束排除)
  3. 风险评估 (软约束评分)
  4. 记录决策
```

### 1.5 输入输出

```yaml
输入:
  mode: problem | requirements | technical
  topic: string (讨论主题)
  context:
    constraints: Constraint[]
    related_docs: string[]
    previous_decisions: string[]

输出:
  decision_log: string (markdown)
  artifacts:
    problem: problem-definition.md
    requirements: user-stories/*.md
    technical: decision-log.md + proposal.md
```

---

## 2. state-scanner 增强

### 2.1 新增推荐规则

```yaml
新增规则:
  fuzziness_requirement:
    条件: fuzziness >= 0.6 + 无对应文档
    推荐: brainstorm.problem
    理由: "需求模糊，建议先澄清问题空间"

  missing_prd:
    条件: !prd_exists + 复杂度 >= Level2
    推荐: brainstorm.problem
    理由: "复杂功能变更，建议先创建 PRD"

  prd_refinement:
    条件: prd_exists + 无 User Stories
    推荐: brainstorm.requirements
    理由: "PRD 需要细化为 User Stories"

  tech_design_needed:
    条件: 有 ready Story + 无 OpenSpec
    推荐: brainstorm.technical
    理由: "有就绪 Story，建议先讨论技术方案"
```

### 2.2 状态报告新增

```yaml
状态报告新增段落:

💡 头脑风暴建议
───────────────────────────────────────────────────────────────
  检测到模糊需求 (fuzziness: 0.7)
  建议先进行问题空间探索，澄清真需求 vs 伪需求

  [1] 开始头脑风暴 (problem 模式)
  [2] 直接创建 PRD
  [3] 跳过，稍后处理
```

---

## 3. spec-drafter 增强

### 3.1 内置头脑风暴流程

```yaml
spec-drafter (增强):

创建 PRD 时:
  1. 检测是否有 decision-log
  2. 如果没有 → 触发 requirements 模式
  3. 基于讨论结果 → 生成 PRD

创建 OpenSpec 时:
  1. 检测是否有 technical decision-log
  2. 如果没有 → 触发 technical 模式
  3. 基于讨论结果 → 预填充 proposal.md
```

### 3.2 预填充逻辑

```yaml
proposal.md 预填充:

  Background: ← 来自 problem 模式的决策
  Constraints: ← 收集的约束条件
  Technical Approach: ← 来自 technical 模式的决策
  Decisions: ← 引用决策 ID

示例:
  ```markdown
  ## 背景
  > 基于决策: [DEC-001](../../docs/decisions/problem-001.md)

  用户需要 24/7 可用的客服支持...

  ## 技术方案
  > 基于决策: [DEC-002](../../docs/decisions/technical-002.md)

  采用自建 RAG 方案...
  ```
```

---

## 4. 决策记录系统

### 4.1 文件结构

```
docs/decisions/
├── .template.md           # 决策记录模板
├── problem-001.md         # 问题空间探索决策
├── requirements-001.md    # 需求分解决策
└── technical-001.md       # 技术方案决策
```

### 4.2 命名规范

```yaml
格式: {mode}-{sequence}.md

示例:
  problem-001.md    → 问题空间探索，第 1 个
  requirements-003.md → 需求分解，第 3 个
  technical-002.md  → 技术方案，第 2 个
```

### 4.3 决策引用

```yaml
OpenSpec 中引用:
  ## 背景
  基于 [DEC-001](../../docs/decisions/problem-001.md) 的讨论...

User Story 中引用:
  ### 技术方案
  参考 [DEC-002](../../docs/decisions/technical-002.md)

决策追溯:
  - 每个决策包含前置决策链接
  - 形成决策链，支持完整追溯
```

---

## 5. 与 Superpowers 的差异化

| 维度 | Superpowers | Aria Brainstorm |
|------|-------------|-----------------|
| **定位** | 技术讨论工具 | AI-DDD 协作思考载体 |
| **时机** | 代码实现前 | 需求形成全周期 |
| **模式** | 单一模式 | 三层分层模式 |
| **输出** | 会话记忆 | 持久化决策日志 |
| **约束管理** | 无 | 完整的约束系统 |
| **集成** | 独立使用 | 深度融入方法论 |
| **领域建模** | 无 | 核心能力 |
| **决策记录** | 无 | 结构化记录 |

---

## 6. 配置选项

### 6.1 项目级配置

```yaml
# .claude/aria.local.md

brainstorm:
  enabled: true
  trigger_mode: auto  # auto | always | manual

  auto_trigger:
    fuzziness_threshold: 0.6
    complexity_threshold: Level2

  conversation:
    max_rounds:
      problem: 10
      requirements: 15
      technical: 8
    convergence_threshold: 0.7

  output:
    save_decisions: true
    save_conversation: false
    decision_dir: docs/decisions/
    auto_sync_openspec: true

  default_constraints:
    business:
      budget: "$1000/月"
      timeline: "8周"
    technical:
      deployment: "on-premise"
```

### 6.2 会话级配置

```bash
# 指定模式
/brainstorm problem "添加新功能"

# 指定约束
/brainstorm --constraints budget:$500,deployment:private

# 指定最大轮次
/brainstorm --max-rounds 15
```

---

## 7. 实施计划

### Phase 1: 核心框架 (2周)

```
Week 1:
  Day 1-2: 对话状态机
    - [ ] 状态定义和转换逻辑
    - [ ] 单元测试

  Day 3-4: 问题生成器
    - [ ] 模板系统
    - [ ] 问题选择逻辑
    - [ ] 单元测试

  Day 5: 深度控制器
    - [ ] 深度计算逻辑
    - [ ] 收敛检测
    - [ ] 单元测试

Week 2:
  Day 1-2: 决策记录
    - [ ] 决策识别逻辑
    - [ ] Markdown 生成
    - [ ] 单元测试

  Day 3-4: 约束管理
    - [ ] 约束库定义
    - [ ] 约束验证
    - [ ] 单元测试

  Day 5: 集成测试
  - [ ] 端到端测试
  - [ ] 文档更新
```

### Phase 2: 集成 (1周)

```
Week 3:
  Day 1-2: state-scanner 集成
    - [ ] 推荐触发逻辑
    - [ ] 模式选择
    - [ ] 测试

  Day 3-4: spec-drafter 集成
    - [ ] 预填充逻辑
    - [ ] 决策引用
    - [ ] 测试

  Day 5: 文档和示例
  - [ ] 使用文档
  - [ ] 示例对话
```

### Phase 3: 验证 (1周)

```
Week 4:
  Day 1-3: 用户测试
    - [ ] 找试点用户
    - [ ] 收集反馈
    - [ ] 修复问题

  Day 4-5: 优化和发布
    - [ ] 性能优化
    - [ ] 文档完善
    - [ ] v1.0.0 发布
```

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | - AI-DDD 获得真正的"协作思考"能力<br>- 决策可追溯，减少重复讨论<br>- 需求澄清更充分，减少返工<br>- 与 Superpowers 形成差异化 |
| **Risk** | 增加流程复杂度 | 缓解: 保持可选性，简单场景可跳过 |
| **Breaking** | 无 | 向后兼容 |

---

## Key Deliverables

```
aria/skills/brainstorm/
├── SKILL.md                  # Skill 规格说明
├── SKILL_DESIGN.md           # 技术设计文档
├── templates/
│   └── decision-template.md  # 决策记录模板
└── config-example.md         # 配置示例

docs/decisions/               # 新增目录
├── .template.md
└── (decision logs)

docs/analysis/
└── brainstorming-in-ai-ddd.md  # 设计分析

现有技能更新:
├── state-scanner/SKILL.md    # 集成推荐
├── spec-drafter/SKILL.md     # 内置头脑风暴
└── workflow-runner/SKILL.md  # 集成新流程
```

---

## Success Criteria

- [ ] brainstorm skill 三种模式均可独立使用
- [ ] 对话状态机正确流转
- [ ] 深度控制能有效收敛
- [ ] 决策日志格式正确
- [ ] state-scanner 正确推荐头脑风暴
- [ ] spec-drafter 能预填充决策结果
- [ ] 约束管理系统正常工作
- [ ] 完整的单元测试覆盖
- [ ] 至少 3 个端到端测试场景
- [ ] 用户文档完整
- [ ] 示例对话充分

---

## References

- [Design: Brainstorming in AI-DDD](../../docs/analysis/brainstorming-in-ai-ddd.md)
- [Design Summary](../../docs/analysis/brainstorm-design-summary.md)
- [Superpowers brainstorming](https://github.com/obra/superpowers)
- [Aria System Architecture](../../docs/architecture/system-architecture.md)
- [OpenSpec v2.1.0](../../standards/openspec/project.md)
- [十步循环规范](../../standards/core/ten-step-cycle/README.md)

---

## Related Decisions

| 决策 | 描述 | 链接 |
|------|------|------|
| DEC-001 | 头脑风暴是核心而非附加功能 | [docs/analysis/brainstorming-in-ai-ddd.md](../../docs/analysis/brainstorming-in-ai-ddd.md) |
| DEC-002 | 采用三层模式架构 | [SKILL_DESIGN.md](../../aria/skills/brainstorm/SKILL_DESIGN.md) |
| DEC-003 | 决策记录优先于文档生成 | [SKILL_DESIGN.md](../../aria/skills/brainstorm/SKILL_DESIGN.md) |

---

**Maintained By**: 10CG Lab
**Spec Level**: Full (Level 3)
**Estimate**: 80-120h (4周)
**Priority**: High
**Version**: 1.0
