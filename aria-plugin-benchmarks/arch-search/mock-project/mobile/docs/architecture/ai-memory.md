# AI Memory System Architecture

> Mobile App AI 记忆系统架构

## 概述

本文档描述应用中 AI 智能功能的记忆系统设计。

## 系统目标

1. **上下文记忆**: 记住用户偏好和历史交互
2. **智能建议**: 基于使用模式提供建议
3. **隐私优先**: 敏感数据不上传云端

## 架构设计

```
┌─────────────────────────────────────────────┐
│                AI Service                   │
│         (LLM API Integration)               │
├─────────────────────────────────────────────┤
│             Memory Manager                  │
│    (Context Assembly, Retrieval)            │
├───────────────────┬─────────────────────────┤
│   Short-term     │      Long-term          │
│     Memory       │        Memory           │
│  (Session-based) │   (Persistent Store)    │
└───────────────────┴─────────────────────────┘
```

## 记忆类型

### 短期记忆 (Session Memory)

- 当前会话上下文
- 最近 N 条对话历史
- 会话结束后清除

### 长期记忆 (Persistent Memory)

- 用户偏好设置
- 重要决策记录
- 使用习惯分析

## 数据存储

```dart
class MemoryEntry {
  final String id;
  final MemoryType type;
  final String content;
  final Map<String, dynamic> metadata;
  final DateTime createdAt;
  final double relevanceScore;
}
```

## 相关代码

| 功能 | 文件路径 |
|------|----------|
| AI 服务 | `mobile/src/services/ai/ai_service.dart` |
| 记忆管理 | `mobile/src/services/ai/memory_manager.dart` |
| 向量存储 | `mobile/src/services/ai/vector_store.dart` |
| 上下文组装 | `mobile/src/services/ai/context_assembler.dart` |

## 隐私考虑

- 敏感数据本地加密存储
- 用户可清除所有记忆
- 可选的云端同步
