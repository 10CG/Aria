# Spec Drafter Output

## Level Judgment

```
╔══════════════════════════════════════════════════════════╗
║           SPEC LEVEL DECISION                            ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Keyword Analysis:                                       ║
║    - "新功能" (new feature)        → Level 2+            ║
║    - "自动提取" (auto-extraction)  → Level 2+            ║
║    - "用户画像" (user profile)     → integration         ║
║    - src/pipeline/ + src/core/     → cross-module        ║
║                                                          ║
║  Scope Analysis:                                         ║
║    - Modules affected: 2 (pipeline, core)                ║
║    - Cross-module: YES → auto-escalate to Level 3        ║
║    - New data flow: pipeline → core (CRM)                ║
║    - Estimated files: > 10                               ║
║                                                          ║
║  Result: LEVEL 3 (Full)                                  ║
║    proposal.md + tasks.md                                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

## Module Detection

```
Module: cross (pipeline + core)
  - src/pipeline/ : Agent Pipeline (preference extraction logic)
  - src/core/     : CRM module (user profile storage)
```

---

## Generated Files

### File 1: proposal.md

**Location**: `openspec/changes/user-preference-extraction/proposal.md`

```markdown
# User Preference Extraction

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-03-27

## Why

Kairos 的 AI Sales Agent 在与客户对话时产生大量有价值的用户意向信号，但目前这些信息随对话结束而丢失。销售团队无法基于历史偏好数据进行精准跟进，导致转化率和客户体验不理想。通过自动从聊天记录中提取用户产品偏好（价格范围、品类偏好、购买意向等），并持久化到 CRM 用户画像中，可以实现数据驱动的个性化销售策略。

## What

在 Agent Pipeline 中新增偏好提取阶段（Preference Extraction Stage），利用 LLM 结构化输出能力，从对话上下文中实时识别并提取用户的产品偏好信息。提取结果通过标准化的偏好模型写入 CRM 的用户画像模块，支持增量更新和冲突合并。

### Key Deliverables

- **Preference Extraction Stage** (`src/pipeline/`) - Pipeline 中的新处理阶段，负责调用 LLM 提取结构化偏好数据
- **Preference Data Model** (`src/core/`) - 定义用户偏好的类型系统（价格范围、品类偏好、购买意向、品牌倾向等）
- **User Profile Integration** (`src/core/`) - 将提取的偏好数据合并到 CRM 用户画像，支持增量更新
- **Preference Extraction Prompt Template** - 专用的 LLM 提示词模板，确保提取结果的结构化和一致性
- **Unit & Integration Tests** - 覆盖提取逻辑、数据合并、异常处理等场景

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 销售团队可基于用户画像进行精准推荐，提升转化率和客户满意度 |
| **Positive** | 用户偏好数据积累后可用于数据分析和销售策略优化 |
| **Risk** | LLM 提取准确率可能不稳定，需要 fallback 和人工校验机制 |
| **Risk** | 跨模块数据流增加系统耦合度，需要清晰的接口边界 |
| **Risk** | 实时提取可能影响对话响应延迟，需考虑异步处理策略 |

## Constraints

| Type | Constraint |
|------|------------|
| **Performance** | 偏好提取不应增加对话响应延迟 > 200ms（考虑异步方案） |
| **Data** | 偏好数据必须支持增量更新，新数据不覆盖已有有效偏好 |
| **Accuracy** | 提取结果需包含置信度评分，低置信度数据标记为 "unconfirmed" |
| **Privacy** | 偏好数据须遵循现有 CRM 数据隐私策略，不存储原始对话内容 |
| **Compatibility** | 不破坏现有 Pipeline 阶段的执行顺序和接口 |

## Technical Approach

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Pipeline                            │
│                                                              │
│  ... → [Conversation Stage] → [Preference Extraction] → ... │
│                                       │                      │
│                                       │ PreferenceResult     │
│                                       ▼                      │
│                              ┌─────────────────┐            │
│                              │ Preference       │            │
│                              │ Merger Service   │            │
│                              └────────┬────────┘            │
│                                       │                      │
└───────────────────────────────────────│──────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────┐
│                    CRM Core Module                            │
│                                                               │
│  ┌──────────────┐    ┌──────────────────┐                    │
│  │ User Profile  │◄───│ Preference Store │                    │
│  │ (existing)    │    │ (new)            │                    │
│  └──────────────┘    └──────────────────┘                    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Extraction timing | Post-conversation (async) | Avoid blocking conversation flow |
| LLM call strategy | Batch per conversation turn | Balance cost vs. freshness |
| Preference merge | Confidence-weighted merge | Higher confidence overwrites lower |
| Data model | Typed preference categories | Enable structured querying and analytics |

### Preference Data Model (Draft)

```typescript
interface UserPreference {
  userId: string;
  preferences: {
    priceRange?: { min: number; max: number; currency: string; confidence: number };
    categoryPreferences?: Array<{ category: string; interest: 'high' | 'medium' | 'low'; confidence: number }>;
    purchaseIntent?: { level: 'ready' | 'considering' | 'browsing'; confidence: number; timeframe?: string };
    brandPreferences?: Array<{ brand: string; sentiment: 'positive' | 'neutral' | 'negative'; confidence: number }>;
    featurePreferences?: Array<{ feature: string; importance: 'must-have' | 'nice-to-have' | 'indifferent'; confidence: number }>;
  };
  metadata: {
    extractedFrom: string;   // conversation ID
    extractedAt: string;     // ISO timestamp
    modelVersion: string;    // LLM model used
    overallConfidence: number;
  };
}
```

## Tasks

> Detailed task breakdown in [tasks.md](./tasks.md)

- [ ] 1.1 Define preference data model and TypeScript types
- [ ] 1.2 Design preference extraction prompt template
- [ ] 2.1 Implement Preference Extraction Pipeline Stage
- [ ] 2.2 Implement Preference Merger Service
- [ ] 2.3 Integrate preference store into CRM User Profile
- [ ] 3.1 Write unit tests for extraction and merge logic
- [ ] 3.2 Write integration tests for end-to-end pipeline flow
- [ ] 3.3 Performance benchmarking and async optimization

## Success Criteria

- [ ] Agent 对话后，用户偏好自动出现在 CRM 用户画像中
- [ ] 多轮对话的偏好数据正确增量合并，不丢失已有有效偏好
- [ ] 提取结果包含置信度评分，低置信度数据不覆盖高置信度数据
- [ ] 偏好提取不增加对话响应延迟（异步处理）
- [ ] 单元测试和集成测试覆盖率 >= 85%
- [ ] 支持至少 5 种偏好类型：价格范围、品类偏好、购买意向、品牌倾向、功能偏好
```

---

### File 2: tasks.md

**Location**: `openspec/changes/user-preference-extraction/tasks.md`

```markdown
# Tasks: User Preference Extraction

> **Spec**: changes/user-preference-extraction/proposal.md
> **Level**: Full (Level 3)
> **Status**: Draft
> **Created**: 2026-03-27
> **Estimated**: 24-32h

---

## 1. Data Model & Design

- [ ] 1.1 Define preference data model and TypeScript types
- [ ] 1.2 Design preference extraction prompt template

## 2. Core Implementation

- [ ] 2.1 Implement Preference Extraction Pipeline Stage
- [ ] 2.2 Implement Preference Merger Service
- [ ] 2.3 Integrate preference store into CRM User Profile

## 3. Testing & Optimization

- [ ] 3.1 Write unit tests for extraction and merge logic
- [ ] 3.2 Write integration tests for end-to-end pipeline flow
- [ ] 3.3 Performance benchmarking and async optimization

---

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 1. Data Model & Design | 2 | 4-6h |
| 2. Core Implementation | 3 | 14-18h |
| 3. Testing & Optimization | 3 | 6-8h |
| **Total** | **8** | **24-32h** |

---

## Dependencies

```
Phase 1 ──────> Phase 2 ──────> Phase 3
  1.1 (types) ──> 2.1 (extraction stage)
  1.2 (prompt) ──> 2.1 (extraction stage)
                   2.1 ──> 2.2 (merger service)
                   2.2 ──> 2.3 (CRM integration)
                          Phase 2 ──> 3.1 (unit tests)
                          Phase 2 ──> 3.2 (integration tests)
                                      3.2 ──> 3.3 (perf benchmark)
```

---

## Notes

1. **Numbering Immutability**: Once numbering (1.1, 1.2, etc.) is established, it MUST NOT be changed
   - Adding new tasks: Use new numbers (1.3, 2.4, etc.)
   - Removing tasks: Mark as ~~cancelled~~ instead of deleting

2. **Task Granularity**: Each item represents a coarse-grained functional deliverable
   - Detailed file paths and agent assignments belong in detailed-tasks.yaml (Layer 2)
   - Time estimates per task belong in detailed-tasks.yaml (Layer 2)
```

---

## Validation Reminder

> After creating the spec files, run:
> ```
> openspec validate user-preference-extraction --strict
> ```
> to verify format compliance.

## Next Steps

1. Review and approve the proposal (Level 3 Spec)
2. Proceed to **A.2 (Task Planning)** - use `task-planner` to generate `detailed-tasks.yaml` from `tasks.md`
3. Proceed to **A.3 (Agent Assignment)** - use `agent-router` to assign agents to tasks
