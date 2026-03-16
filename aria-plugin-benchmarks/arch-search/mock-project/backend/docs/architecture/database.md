# Database Architecture

> Backend 数据库架构设计

## 概述

本文档描述后端数据库的设计原则和实现细节。

## 数据库选型

- **主数据库**: PostgreSQL 15
- **缓存层**: Redis 7
- **搜索引擎**: Elasticsearch (可选)

## Schema 设计原则

1. **规范化**: 第三范式 (3NF)
2. **索引策略**: 基于查询模式优化
3. **软删除**: 使用 `deleted_at` 字段
4. **审计字段**: `created_at`, `updated_at`, `created_by`, `updated_by`

## 核心表结构

### 用户表 (users)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
```

### 任务表 (tasks)

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(500) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 相关代码

| 功能 | 文件路径 |
|------|----------|
| 数据库配置 | `backend/src/config/database.py` |
| 用户模型 | `backend/src/models/user.py` |
| 任务模型 | `backend/src/models/task.py` |
| 迁移脚本 | `backend/migrations/` |
| Repository | `backend/src/repositories/` |

## 性能优化

- 连接池: PgBouncer
- 读写分离: 主从复制
- 分区: 按时间分区大表
