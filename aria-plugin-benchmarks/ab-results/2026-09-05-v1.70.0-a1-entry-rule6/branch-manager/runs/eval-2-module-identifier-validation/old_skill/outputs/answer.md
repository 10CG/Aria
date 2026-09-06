branch-manager 支持的**模块标识符** (`module` 参数) 共 6 个:

| 模块 | 标识符 | 说明 |
|------|--------|------|
| Backend | `backend` | Python/FastAPI 服务 |
| Mobile | `mobile` | Flutter 应用 |
| Shared | `shared` | API 契约、schemas |
| Cross-module | `cross` | 多模块变更 |
| Documentation | `docs` | 仅文档变更 |
| Standards | `standards` | AI-DDD 规范 |

## 它用在哪里

`module` 是 B.1 分支创建的**必需参数**, 直接进分支名的第二段:

```
{branch_type}/{module}/{task_id}-{description}
```

例如:

1. `feature/backend/TASK-001-user-auth`
2. `bugfix/mobile/ISSUE-42-login-crash`
3. `feature/shared/TASK-010-api-contract`
4. `feature/cross/TASK-020-auth-e2e`
5. `feature/docs/TASK-030-readme`
6. `feature/standards/TASK-040-commit-convention`

## 选择要点

- **单模块改动**: 按代码归属挑 `backend` / `mobile` / `shared`。
- **同时动到 2 个以上模块**: 用 `cross`, 不要挑其中一个模块名。
- **只改文档**: 用 `docs`; 但如果改的是 AI-DDD 方法论规范 (standards 子模块), 用 `standards`。
- 分支名不规范是 branch-manager 明确列出的 Red Flag —— 难以识别和管理, 请固定用上表的标识符, 不要自造 (如 `api`、`web`、`fe`)。

## 两个相关的格式例外

`hotfix` / `release` / `experiment` 三种分支类型**不带 module 段**, 命名格式不同:

| 类型 | 格式 | 示例 |
|------|------|------|
| hotfix | `hotfix/{version}-{desc}` | `hotfix/v1.2.1-security-patch` |
| release | `release/{version}` | `release/v1.3.0` |
| experiment | `experiment/{name}` | `experiment/openspec-pilot` |

只有 `feature` 和 `bugfix` 走 `{type}/{module}/{task-id}-{desc}` 这个带 module 的格式。

需要我直接按某个模块帮你创建分支吗? 告诉我 `module` + `task_id` + `description` 就可以。
