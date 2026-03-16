# Data Synchronization Architecture

> Mobile App 离线数据同步架构

## 概述

本文档描述应用的离线数据同步机制和冲突解决策略。

## 核心特性

1. **离线优先**: 所有操作优先本地存储
2. **自动同步**: 网络恢复后自动同步
3. **冲突解决**: 基于时间戳的自动合并

## 同步流程

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Local   │────▶│  Sync    │────▶│  Remote  │
│  Store   │     │  Engine  │     │   API    │
└──────────┘     └──────────┘     └──────────┘
     ▲                │                 │
     └────────────────┴─────────────────┘
                   Sync Queue
```

## 冲突解决策略

### Last-Write-Wins (LWW)

```dart
// 基于服务器时间戳
if (serverVersion.updatedAt > localVersion.updatedAt) {
  return serverVersion;
}
return localVersion;
```

### 三向合并 (3-Way Merge)

对于复杂对象，使用三向合并：

1. 获取 base (共同祖先)
2. 计算 local diff 和 remote diff
3. 合并 diffs，自动解决非冲突部分
4. 冲突部分标记为需要人工处理

## 相关代码

| 功能 | 文件路径 |
|------|----------|
| 同步引擎 | `mobile/src/services/sync/sync_engine.dart` |
| 冲突解决 | `mobile/src/services/sync/conflict_resolver.dart` |
| 离线队列 | `mobile/src/services/sync/offline_queue.dart` |
| 网络检测 | `mobile/src/services/network_detector.dart` |

## 同步状态

```dart
enum SyncStatus {
  synced,      // 已同步
  pending,     // 待同步
  conflict,    // 存在冲突
  error,       // 同步失败
}
```

## 性能考虑

- 增量同步: 只同步变更数据
- 批量操作: 合并多个小请求
- 后台同步: 使用 WorkManager
