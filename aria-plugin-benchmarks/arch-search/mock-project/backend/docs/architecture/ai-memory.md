# AI 记忆系统架构

> **文档层级**: L1 架构文档
> **模块**: AI 系统
> **最后更新**: 2026-03-13

## 概述

AI 记忆系统是智能应用的核心组件，负责持久化和管理用户交互历史、上下文信息以及模型训练数据。

## 系统架构

### 数据层

#### 记忆存储 (Memory Store)
- **类型**: 分层存储（短期记忆 + 长期记忆）
- **技术栈**:
  - 短期: In-Memory Cache (Redis)
  - 长期: SQLite 数据库
- **路径**: `src/data/memory/`

```dart
// 代码文件指针
├── src/data/memory/memory_store.dart      // 主存储实现
├── src/data/memory/short_term_cache.dart  // 短期缓存
└── src/data/memory/long_term_db.dart     // 长期存储
```

#### 向量索引 (Vector Index)
- **功能**: 语义搜索与记忆检索
- **技术**: ChromaDB + Sentence-BERT
- **用途**: 模糊匹配和上下文检索

### 业务层

#### 记忆管理器 (Memory Manager)
- **职责**:
  - 记忆的增删改查
  - 记忆生命周期管理
  - 上下文聚合
- **路径**: `src/services/memory/`

```dart
// 代码文件指针
├── src/services/memory/memory_manager.dart    // 核心管理器
├── src/services/memory/context_aggregator.dart // 上下文聚合
└── src/services/memory/lifecycle_manager.dart  // 生命周期管理
```

#### 策略引擎 (Policy Engine)
- **功能**: 记忆压缩、重要性计算
- **算法**:
  - 重要度评分: 基于访问频率、时效性、相关性
  - 压缩策略: LRU + 重要性阈值
- **路径**: `src/policies/memory/`

### 接口层

#### 记忆 API
- **REST 接口**: `/api/v1/memories`
- **WebSocket**: 实时记忆同步
- **SDK**: `src/clients/memory_client.dart`

## 关键特性

### 1. 分层存储
- **短期记忆 (0-24h)**: 高速访问，自动清理
- **长期记忆 (永久)**: 结构化存储，索引检索
- **工作记忆**: 当前会话上下文

### 2. 智能检索
- **语义搜索**: 基于向量相似度
- **时间衰减**: 随时间降低权重
- **相关性过滤**: 上下文相关性评分

### 3. 压缩策略
- **重要度阈值**: 自动清理低价值记忆
- **摘要生成**: 长对话自动生成摘要
- **去重机制**: 避免重复存储

## 性能指标

| 操作 | 延迟 | QPS |
|------|------|-----|
| 读取记忆 | <50ms | 1000+ |
| 写入记忆 | <100ms | 500+ |
| 语义搜索 | <200ms | 100+ |

## 安全考虑

- **数据加密**: 敏感记忆 AES-256 加密
- **访问控制**: RBAC 权限控制
- **隐私保护**: GDPR 合规设计

## 相关文档

- **AI 混合系统**: `mobile/docs/ai-hybrid-system/`
- **数据同步**: `mobile/docs/architecture/sync.md`
- **安全架构**: `mobile/docs/architecture/security.md`