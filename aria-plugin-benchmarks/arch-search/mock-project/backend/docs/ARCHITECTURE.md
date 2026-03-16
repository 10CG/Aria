# Backend Module Architecture

> Backend 整体架构文档

## 概述

本文档是 Backend 模块的主入口，提供整体架构视图。

## 技术栈

- **框架**: FastAPI (Python 3.11+)
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7
- **任务队列**: Celery

## 架构分层

```
┌─────────────────────────────────────────────┐
│                  API Layer                  │
│         (Routes, Controllers)               │
├─────────────────────────────────────────────┤
│                Service Layer                │
│         (Business Logic)                    │
├─────────────────────────────────────────────┤
│              Repository Layer               │
│         (Data Access)                       │
├─────────────────────────────────────────────┤
│               Data Layer                    │
│         (Models, Schemas)                   │
└─────────────────────────────────────────────┘
```

## 子模块文档

| 领域 | 文档 |
|------|------|
| 数据库 | [architecture/database.md](./architecture/database.md) |

## 目录结构

```
backend/
├── src/
│   ├── api/           # API路由
│   ├── services/      # 业务逻辑
│   ├── repositories/  # 数据访问
│   ├── models/        # 数据模型
│   └── middleware/    # 中间件
├── tests/
└── docs/
```
