# User Preference Extraction

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-03-27
> **Location**: `openspec/changes/user-preference-extraction/proposal.md`

## Why

Kairos 的 AI Sales Agent 当前与客户对话时，不会自动捕获和结构化用户的产品偏好信息。销售人员需要手动从聊天记录中提取客户的价格范围、品类偏好、购买意向等关键信息，再手工录入 CRM。这导致：

1. **信息丢失** — 对话中隐含的偏好信号（如"这个价位有点高"）没有被捕获，用户画像不完整
2. **响应滞后** — Agent 无法基于历史偏好进行个性化推荐，每次对话都像从零开始
3. **人工成本** — 手动归纳偏好耗时，且容易遗漏关键信号

自动化偏好提取能让 Agent Pipeline 在对话过程中实时构建用户画像，提升推荐精准度和转化率。

## What

在 Agent Pipeline 中新增 **Preference Extraction Stage**，利用 LLM 从对话上下文中提取结构化的用户偏好数据，并通过 CRM Core 模块持久化到用户画像中。

### Key Deliverables

- **PreferenceExtractor** — Pipeline 中的新 Stage，负责从对话消息中提取偏好信号
- **Preference Schema** — 定义偏好数据的结构化格式（价格范围、品类、意向等级、品牌偏好等）
- **UserProfile 扩展** — CRM Core 中的用户画像模型扩展，支持偏好数据的增量更新与合并
- **Preference Merge Strategy** — 多轮对话中偏好数据的冲突解决和置信度衰减机制
- **Pipeline Integration** — 将 PreferenceExtractor 集成到现有 Agent Pipeline 的合适位置

### Scope Boundary

```
IN SCOPE:
  - 从文本对话中提取偏好（中文为主）
  - 偏好数据持久化到 CRM 用户画像
  - 多轮对话的偏好合并
  - 基本置信度评分

OUT OF SCOPE:
  - 多模态偏好提取（图片、语音）
  - 实时推荐引擎（后续 Spec）
  - 偏好数据的分析报表
  - 跨用户的群体偏好聚合
```

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Agent 能基于用户画像进行个性化推荐，预计提升推荐相关性 30%+ |
| **Positive** | 减少销售人员手动录入偏好的工作量，每次对话节省 2-5 分钟 |
| **Risk** | LLM 偏好提取可能误判用户意图，需要置信度阈值过滤低质量数据 |
| **Risk** | Pipeline 增加一个 Stage 会增加单次对话的延迟和 Token 消耗，需要异步处理或批量提取 |
| **Breaking** | 无破坏性变更 — UserProfile schema 向后兼容扩展 |

## Architecture

### High-Level Design

```
┌──────────────────────────────────────────────────────────────┐
│                     Agent Pipeline                           │
│                                                              │
│  ┌───────────┐   ┌──────────────┐   ┌───────────────────┐   │
│  │  Message   │──▶│  Existing    │──▶│  Response          │   │
│  │  Ingress   │   │  Stages      │   │  Generation        │   │
│  └───────────┘   └──────────────┘   └───────┬───────────┘   │
│                                              │               │
│                                              ▼               │
│                                    ┌─────────────────────┐   │
│                                    │  PreferenceExtractor │   │
│                                    │  (async, post-reply) │   │
│                                    └─────────┬───────────┘   │
│                                              │               │
└──────────────────────────────────────────────┼───────────────┘
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────────┐
│                       CRM Core                               │
│                                                              │
│  ┌─────────────────┐   ┌──────────────────────────────────┐ │
│  │  PreferenceStore │──▶│  UserProfile (preferences field) │ │
│  │  (merge + save)  │   │  - priceRange                   │ │
│  └─────────────────┘   │  - categoryPrefs                 │ │
│                         │  - purchaseIntent                │ │
│                         │  - brandPrefs                    │ │
│                         │  - extractionHistory             │ │
│                         └──────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| `PreferenceExtractor` | Pipeline Stage: 调用 LLM 从对话提取偏好 | `src/pipeline/stages/preference-extractor.ts` |
| `PreferenceSchema` | 偏好数据类型定义和验证 | `src/pipeline/types/preference.ts` |
| `PreferencePrompt` | LLM 提取用的 prompt template | `src/pipeline/prompts/preference-extraction.ts` |
| `PreferenceStore` | 偏好数据的持久化和合并逻辑 | `src/core/crm/preference-store.ts` |
| `UserProfile` (扩展) | 用户画像模型，增加 preferences 字段 | `src/core/crm/models/user-profile.ts` |
| `PreferenceMerger` | 多轮对话偏好的合并和冲突解决 | `src/core/crm/preference-merger.ts` |

### Data Flow

```
1. Agent 完成一轮对话回复
2. Pipeline 异步触发 PreferenceExtractor
3. PreferenceExtractor 将最近 N 条消息 + 历史偏好 发送给 LLM
4. LLM 返回结构化偏好 JSON
5. PreferenceMerger 将新偏好与历史偏好合并 (置信度加权)
6. PreferenceStore 将合并结果持久化到 UserProfile
```

### Preference Schema (Draft)

```typescript
interface UserPreference {
  // 价格敏感度
  priceRange?: {
    min?: number;
    max?: number;
    sensitivity: 'low' | 'medium' | 'high';
    currency: string;
  };

  // 品类偏好 (按置信度排序)
  categoryPrefs: Array<{
    category: string;
    confidence: number;      // 0.0 - 1.0
    lastMentioned: string;   // ISO date
  }>;

  // 购买意向
  purchaseIntent: {
    level: 'browsing' | 'comparing' | 'ready_to_buy' | 'urgent';
    confidence: number;
    signals: string[];       // 支持判断的原始信号
  };

  // 品牌偏好
  brandPrefs: Array<{
    brand: string;
    sentiment: 'positive' | 'neutral' | 'negative';
    confidence: number;
  }>;

  // 其他偏好 (可扩展)
  custom: Record<string, {
    value: string;
    confidence: number;
    source: 'explicit' | 'inferred';
  }>;

  // 元数据
  meta: {
    lastUpdated: string;
    extractionCount: number;
    totalMessagesAnalyzed: number;
  };
}
```

## Tasks

- [ ] 1.1 定义 Preference Schema 类型和验证规则
- [ ] 1.2 编写偏好提取 prompt template（含中文对话示例）
- [ ] 1.3 实现 PreferenceExtractor Pipeline Stage
- [ ] 1.4 实现 PreferenceExtractor 单元测试
- [ ] 2.1 扩展 UserProfile 模型，添加 preferences 字段
- [ ] 2.2 实现 PreferenceMerger（合并策略 + 置信度衰减）
- [ ] 2.3 实现 PreferenceStore（持久化 + 查询接口）
- [ ] 2.4 实现 CRM 模块的单元测试
- [ ] 3.1 将 PreferenceExtractor 集成到 Agent Pipeline（异步 post-reply 触发）
- [ ] 3.2 编写集成测试（完整对话流 → 偏好提取 → 画像更新）
- [ ] 3.3 性能测试（确认异步提取不阻塞回复延迟）

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 1. Pipeline Stage 开发 | 4 | 6-8h |
| 2. CRM Core 扩展 | 4 | 6-8h |
| 3. 集成与测试 | 3 | 4-6h |
| **Total** | **11** | **16-22h** |

## Dependencies

```
Phase 1 (Pipeline Stage) ──┐
                           ├──> Phase 3 (Integration & Testing)
Phase 2 (CRM Core)  ──────┘
```

Phase 1 和 Phase 2 可以并行开发，Phase 3 依赖两者完成。

### Internal Dependencies

- `src/pipeline/` — 现有 Pipeline Stage 接口和生命周期
- `src/core/crm/` — 现有 UserProfile 模型和 CRM 数据层
- LLM Provider Gateway — 用于偏好提取的 LLM 调用

### External Dependencies

- 无新增外部依赖 — 复用 Kairos 现有的 LLM Provider 和数据存储

## Success Criteria

- [ ] PreferenceExtractor 能从中文销售对话中提取 4 类偏好（价格、品类、意向、品牌），准确率 >= 80%
- [ ] 偏好提取异步执行，不增加 Agent 回复延迟（P99 延迟无显著变化）
- [ ] 多轮对话的偏好能正确合并，新信号覆盖旧信号时置信度更新正确
- [ ] UserProfile schema 变更向后兼容，现有无偏好数据的用户画像不受影响
- [ ] 所有新增代码覆盖率 >= 85%，含单元测试和集成测试

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM 提取质量不稳定，偏好识别准确率低 | MEDIUM | HIGH | 设置置信度阈值（< 0.5 丢弃），提供 few-shot 中文示例，支持人工修正入口 |
| 异步提取增加 Token 消耗成本 | HIGH | MEDIUM | 仅在对话轮次 >= 3 时触发提取，批量处理最近消息而非逐条处理 |
| 多轮对话偏好冲突（用户改变主意） | MEDIUM | MEDIUM | 时间衰减机制：旧偏好置信度随时间降低，最新信号权重更高 |
| UserProfile 数据膨胀 | LOW | LOW | 限制每个维度最多保留 Top-N 条目，定期清理低置信度数据 |

## References

- Kairos Agent Pipeline 架构: `src/pipeline/README.md`
- CRM 模块文档: `src/core/crm/README.md`
- 现有 Pipeline Stage 实现参考: `src/pipeline/stages/`

---

**File Path**: `openspec/changes/user-preference-extraction/proposal.md`
**Next Step**: Review & Approve, then generate `tasks.md` via task-planner
