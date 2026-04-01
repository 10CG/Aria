# Commit Message Generator Output

## Generated Commit Message

```
feat(provider-health): add provider health monitoring dashboard

- 新增 /api/providers/health 端点，返回所有 Provider 的延迟、错误率、可用状态
- 新增 ProviderHealthDashboard 组件，展示实时状态表格和 30 分钟延迟趋势图
- 在 gateway.ts 中增加 getProviderStats() 方法用于收集统计数据
```

## Analysis

| Field | Value | Rationale |
|-------|-------|-----------|
| **Type** | `feat` | 新功能：Provider 健康监控是全新的能力 |
| **Scope** | `provider-health` | 变更横跨 API、Console、Core 三层，以功能域命名更准确 |
| **Subject** | `add provider health monitoring dashboard` | 祈使句，概括整体功能，49 字符 |
| **Body** | 3 bullet points | 分别描述 API 端点、前端组件、核心方法三个组成部分 |
| **Footer** | (none) | 无关联 Issue 信息，无破坏性变更 |
| **Mode** | 独立模式 | 无 orchestrator 参数，不添加增强标记 |
