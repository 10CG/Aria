# Navigation Architecture

> Mobile App 导航路由架构

## 概述

本文档描述应用的导航和路由系统设计。

## 技术选型

**go_router** - 声明式路由

## 路由配置

```dart
// lib/routes/app_router.dart
final goRouter = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/tasks/:id',
      builder: (context, state) => TaskDetailScreen(
        taskId: state.pathParameters['id']!,
      ),
    ),
  ],
  errorBuilder: (context, state) => const ErrorScreen(),
);
```

## 深层链接

支持 URL Scheme 和 Universal Links：

- URL Scheme: `myapp://tasks/123`
- Universal Link: `https://app.example.com/tasks/123`

## 路由守卫

```dart
// 认证守卫
GoRoute(
  path: '/profile',
  redirect: (context, state) {
    if (!isAuthenticated) return '/login';
    return null; // 允许访问
  },
)
```

## 相关代码

| 功能 | 文件路径 |
|------|----------|
| 路由配置 | `mobile/src/routes/app_router.dart` |
| 路由守卫 | `mobile/src/routes/guards/` |
| 深层链接处理 | `mobile/src/services/deep_link_service.dart` |

## 导航最佳实践

1. 使用命名路由而非直接 Navigator 调用
2. 需要认证的路由添加守卫
3. 传递复杂对象使用 extra 参数
