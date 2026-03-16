# State Management Architecture

> Mobile App 状态管理架构

## 概述

本文档描述应用的状态管理策略和实现。

## 技术选型

**Riverpod 2.0** - 响应式状态管理

### 为什么选择 Riverpod

1. 编译时安全
2. 不依赖 BuildContext
3. 易于测试
4. 支持依赖注入

## 状态分层

```
┌─────────────────────────────────┐
│         UI Layer                │
│  (Widgets, Screens)             │
├─────────────────────────────────┤
│         ViewModel Layer         │
│  (StateNotifierProviders)       │
├─────────────────────────────────┤
│         Repository Layer        │
│  (Data Providers)               │
├─────────────────────────────────┤
│         Data Source Layer       │
│  (API, Local Storage)           │
└─────────────────────────────────┘
```

## Provider 组织

### 全局状态

```dart
// lib/providers/global_providers.dart
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.read(authRepositoryProvider));
});

final userProvider = Provider<User?>((ref) {
  return ref.watch(authProvider).user;
});
```

### 局部状态

```dart
// 每个功能模块有自己的 provider 文件
// lib/features/task/providers/task_providers.dart
final taskListProvider = StateNotifierProvider<TaskListNotifier, TaskListState>(...);
```

## 相关代码

| 功能 | 文件路径 |
|------|----------|
| 全局 Providers | `mobile/src/providers/global_providers.dart` |
| 认证状态 | `mobile/src/providers/auth/auth_notifier.dart` |
| 任务状态 | `mobile/src/features/task/providers/` |
| 设置状态 | `mobile/src/providers/settings/` |

## 最佳实践

1. **单一职责**: 每个 Provider 只管理一类状态
2. **不可变数据**: 使用 freezed 生成不可变类
3. **异步处理**: 使用 AsyncValue 处理加载状态
