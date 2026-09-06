# 支持的模块标识符 (module)

branch-manager 在 B.1 分支创建时，`module` 是**必填**参数，取值封闭为下面 6 个：

| 模块 | 标识符 | 说明 |
|------|--------|------|
| Backend | `backend` | Python/FastAPI 服务 |
| Mobile | `mobile` | Flutter 应用 |
| Shared | `shared` | API 契约、schemas |
| Cross-module | `cross` | 多模块变更 |
| Documentation | `docs` | 仅文档变更 |
| Standards | `standards` | AI-DDD 规范 |

## 它出现在分支名的哪一段

分支命名规范是 `{branch_type}/{module}/{task_id}-{desc}`，`module` 是**第二段**：

```
feature/backend/TASK-001-user-auth
bugfix/mobile/ISSUE-42-login-crash
        ^^^^^^ 这一段就是 module
```

## 三个容易混淆的点

1. **`module` 不是 `branch_type`**。第一段 `branch_type` 的取值是另一组：`feature` / `bugfix` / `hotfix` / `release` / `experiment`（默认 `feature`）。两组不要互相代入。

2. **只有 `feature` 和 `bugfix` 的命名格式带 module 段**。其余三类的格式里根本没有这一段：
   - `hotfix/{version}-{desc}`（如 `hotfix/v1.2.1-security-patch`）
   - `release/{version}`（如 `release/v1.3.0`）
   - `experiment/{name}`（如 `experiment/openspec-pilot`）

3. **跨模块变更用 `cross`，不要自造拼接值**。同时动 backend 和 mobile 时写 `cross`，而不是 `backend-mobile` 之类不在表内的写法。

## 补充

- `in_submodule: true`（在 `backend/`、`mobile/` 等子模块内建分支）时，module 仍然从上表取值，命名规范不变；差别只在于要 `cd` 进子模块建分支，并在完成后回主仓库更新子模块指针。
- 分支名不规范是 branch-manager 明确列出的 Red Flag（难以识别和管理），所以取值请严格落在上表内。

> 本次是纯查询，我没有执行任何 git 操作，也没有创建分支或 claim。需要我按其中某个 module 实际走 B.1 建分支时，告诉我 `task_id` 和 `description` 即可。
