# Mobile Module Architecture

> Mobile App 整体架构文档

## 概述

本文档是 Mobile 模块的主入口，提供整体架构视图和子模块导航。

## 技术栈

- **框架**: Flutter 3.x
- **语言**: Dart 3.x
- **状态管理**: Riverpod
- **网络**: Dio + Retrofit
- **本地存储**: Drift (SQLite) + flutter_secure_storage

## 架构分层

```
┌─────────────────────────────────────────────┐
│                  Presentation               │
│     (Screens, Widgets, ViewModels)          │
├─────────────────────────────────────────────┤
│                   Domain                    │
│     (Entities, UseCases, Repositories)      │
├─────────────────────────────────────────────┤
│                    Data                     │
│   (Repository Impl, Data Sources, Models)   │
├─────────────────────────────────────────────┤
│                 Infrastructure              │
│    (Network, Storage, External Services)    │
└─────────────────────────────────────────────┘
```

## 子模块架构文档

| 领域 | 文档 | 描述 |
|------|------|------|
| 认证安全 | [architecture/security.md](./architecture/security.md) | JWT认证、安全措施 |
| 状态管理 | [architecture/state.md](./architecture/state.md) | Riverpod状态管理 |
| 数据同步 | [architecture/sync.md](./architecture/sync.md) | 离线同步、冲突解决 |
| 网络通信 | [architecture/network.md](./architecture/network.md) | API调用、网络层 |
| 导航路由 | [architecture/navigation.md](./architecture/navigation.md) | 路由配置、深层链接 |
| AI记忆 | [architecture/ai-memory.md](./architecture/ai-memory.md) | AI功能、记忆系统 |

## 目录结构

```
mobile/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── src/
│   │   ├── features/        # 功能模块
│   │   ├── providers/       # 状态管理
│   │   ├── services/        # 服务层
│   │   ├── screens/         # 页面
│   │   ├── widgets/         # 组件
│   │   └── routes/          # 路由
│   └── core/                # 核心工具
├── docs/
│   ├── ARCHITECTURE.md      # 本文档
│   └── architecture/        # 子模块架构
└── tests/
```

## 快速导航

- **新增功能**: 参考 [architecture/](./architecture/) 下对应领域的文档
- **API调用**: 查看 [architecture/network.md](./architecture/network.md)
- **状态管理**: 查看 [architecture/state.md](./architecture/state.md)
- **认证流程**: 查看 [architecture/security.md](./architecture/security.md)
