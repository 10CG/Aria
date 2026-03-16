# Domain Routing Map

> Layer 1 快速路由映射表

## 认证与安全 (auth_security)

**Primary**: `mobile/docs/architecture/security.md`
**Secondary**:
- `shared/contracts/api/auth.yaml`
- `backend/src/middleware/README.md`

**Keywords**: auth, 认证, 登录, login, security, 安全, token, JWT, password, 密码

---

## 数据存储 (data_storage)

**Primary**: `backend/docs/architecture/database.md`
**Secondary**:
- `shared/contracts/db/schema.sql`
- `backend/src/models/README.md`

**Keywords**: database, 数据库, DB, storage, 存储, schema, 表, table, model, 模型

---

## 网络通信 (network)

**Primary**: `mobile/docs/architecture/network.md`
**Secondary**:
- `shared/contracts/openapi/`
- `backend/src/api/README.md`

**Keywords**: API, endpoint, 端点, network, 网络, HTTP, REST, request, response, 请求

---

## 数据同步 (sync)

**Primary**: `mobile/docs/architecture/sync.md`
**Secondary**:
- `mobile/src/services/sync/README.md`
- `backend/docs/sync-protocol.md`

**Keywords**: sync, 同步, offline, 离线, conflict, 冲突, merge, 合并

---

## 状态管理 (state_management)

**Primary**: `mobile/docs/architecture/state.md`
**Secondary**:
- `mobile/src/providers/README.md`
- `shared/state/README.md`

**Keywords**: state, 状态, provider, riverpod, bloc, redux, store, 管理

---

## UI组件 (ui_components)

**Primary**: `mobile/docs/architecture/ui-components.md`
**Secondary**:
- `mobile/src/widgets/README.md`
- `shared/ui/README.md`

**Keywords**: UI, widget, 组件, component, screen, 页面, view, 视图, button, text

---

## 导航路由 (navigation)

**Primary**: `mobile/docs/architecture/navigation.md`
**Secondary**:
- `mobile/src/routes/README.md`
- `mobile/app_router.dart`

**Keywords**: navigation, 导航, router, 路由, route, 页面跳转, deep link

---

## 测试 (testing)

**Primary**: `docs/architecture/testing.md`
**Secondary**:
- `mobile/tests/README.md`
- `backend/tests/README.md`

**Keywords**: test, 测试, unit, 单元, integration, 集成, mock, stub

---

## Git版本管理 (git_version)

**Primary**: `docs/architecture/git-workflow.md`
**Secondary**:
- `.github/README.md`
- `docs/branch-strategy.md`

**Keywords**: git, 版本, branch, 分支, commit, 提交, merge, PR, release

---

## 约定规范 (conventions)

**Primary**: `docs/CONVENTIONS.md`
**Secondary**:
- `docs/CODING_STYLE.md`
- `.editorconfig`

**Keywords**: convention, 约定, style, 风格, standard, 标准, lint, format

---

## 进度管理 (progress_management)

**Primary**: `docs/architecture/progress-management.md`
**Secondary**:
- `docs/UPM.md`

**Keywords**: progress, 进度, task, 任务, UPM, milestone, 里程碑, sprint

---

## API契约 (api_contracts)

**Primary**: `shared/contracts/openapi/`
**Secondary**:
- `docs/api-design.md`

**Keywords**: contract, 契约, openapi, swagger, yaml, spec, specification

---

## AI系统 (ai_system)

**Primary**: `mobile/docs/architecture/ai-memory.md`
**Secondary**:
- `mobile/src/services/ai/README.md`
- `backend/docs/ai-service.md`

**Keywords**: AI, 智能, memory, 记忆, ML, model, learning, GPT, LLM

---

## 缓存策略 (cache)

**Primary**: `mobile/docs/architecture/cache.md`
**Secondary**:
- `mobile/src/services/cache/README.md`

**Keywords**: cache, 缓存, memo, store, persist, 持久化

---

## 模块入口

| 模块 | 入口文档 |
|------|----------|
| mobile | `mobile/docs/ARCHITECTURE.md` |
| backend | `backend/docs/ARCHITECTURE.md` |
| shared | `shared/README.md` |
