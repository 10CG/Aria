# Tasks: Add OAuth2 Social Login (GitHub + Google)

> **Spec**: `proposal.md`
> **Level**: Full (Level 3)
> **Status**: Draft (post_spec = PASS_WITH_WARNINGS, R4 表决轮受会话级配额限制未跑 — 见 proposal §审计结论)
> **Created**: 2026-09-05
> **Estimated**: 72-104h

---

## 1. 数据层与抽象层 (无外部依赖, 可最先开工)

- [ ] 1.1 迁移 A：`user_identities` 表 + `UNIQUE(provider, provider_user_id)` + 索引 `(user_id)`
- [ ] 1.2 迁移 B：`users` 增 `email_normalized` / `email_verified` 两列（含既有列名映射与回填口径）+ `UNIQUE(email_normalized)` + **建约束前的存量去重检查**
- [ ] 1.3 迁移 C：`oauth_transactions` / `pending_identities` 两表 + `expires_at` 索引
- [ ] 1.4 Provider 抽象层：`authorize_url` / `exchange_code` / `fetch_identity` 三接口 + `TokenResponse` / `NormalizedIdentity` + 配置驱动注册表 + **双向 nonce fail-closed**

## 2. 两个 Provider Adapter

- [ ] 2.1 GitHub adapter：`GET /user` 数字 id + `GET /user/emails` 四形态判定表（禁用 profile email 回落）
- [ ] 2.2 Google adapter：OIDC discovery + JWKS + `id_token` 五项校验（签名/iss/aud/exp/nonce）

## 3. 路由、事务与会话

- [ ] 3.1 `/auth/{provider}/start`：事务行写入（state/verifier/challenge/nonce/next/session_binding）+ 三个 cookie 的统一属性 + `next` 白名单
- [ ] 3.2 `/auth/{provider}/callback` 八步校验链：`error` 短路 → provider 绑定查找 → state 逐字 → session_binding → 条件更新一次性消费 → **PKCE 本地预检** → token 交换 → 身份获取
- [ ] 3.3 `error_code` 封闭枚举 + fail-closed 兜底（未列举失败 → 500 + 告警，不回落已有码）
- [ ] 3.4 会话签发接线：复用既有 session/JWT 路径 + **签发前轮换会话标识**
- [ ] 3.5 启动期配置校验：`redirect_uri` 不在白名单则进程非零退出

## 4. 账号解析与绑定

- [ ] 4.1 §D 七行判定表（if-elif 短路）+ §D.1 字符级归一化匹配
- [ ] 4.2 §D.2 建号事务语义：插入顺序 + **两类唯一冲突各自的恢复动作** + 隔离级别假设

## 5. 待确认流程 §G（**门禁：D-1 / D-2 待 owner 批准**）

- [ ] 5.1 `pending_identities` 服务端流程：随机 key + cookie 载体 + `session_binding` 比对 + **lane 白名单** + 一次性条件更新（MANUAL lane 不下发 key）
- [ ] 5.2 两个端点 `/auth/link/email` / `/auth/link/confirm`：补填后**重入 §D 判定表**、密码确认绑定、消费与建号同事务

## 6. 运维与 CI

- [ ] 6.1 `unlink-identity` 管理命令 + 审计日志 + "最后一条 identity" 拒绝分支
- [ ] 6.2 过期行清理：定时任务 + lazy delete-on-read
- [ ] 6.3 CI 三项：secret 扫描 / 覆盖率产出物与阈值 gate / 日志调用点静态扫描

## 7. 验收与文档

- [ ] 7.1 SC 覆盖矩阵：30 条 Success Criteria 与测试用例一一对账，缺口清零
- [ ] 7.2 架构与接入文档同步（新表、新端点、新 error_code、运维手册）

---

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 1. 数据层与抽象层 | 4 | 14-20h |
| 2. Provider Adapter | 2 | 10-14h |
| 3. 路由/事务/会话 | 5 | 20-28h |
| 4. 账号解析 | 2 | 10-14h |
| 5. 待确认流程 §G | 2 | 8-12h |
| 6. 运维与 CI | 3 | 6-10h |
| 7. 验收与文档 | 2 | 4-6h |
| **Total** | **20** | **72-104h** |

---

## Dependencies

```
1.1 ─┬─> 1.2 ─┬─> 4.1 ──> 4.2 ──> 5.2
1.3 ─┘        │
1.4 ──> 2.1 ──┤
1.4 ──> 2.2 ──┤
1.3 ──> 3.1 ──> 3.2 ──> 3.4
        3.3 ──> 3.2
        3.5 (独立)
5.1 ──> 5.2
6.1 / 6.2 / 6.3 (独立, 6.3 是 7.1 的证据来源)
所有实现 ──> 7.1 ──> 7.2
```

**关键门禁**
- **5.1 / 5.2 在 D-1、D-2 获 owner 批准前不得进入 `in_progress`**（proposal「Open Questions / 决策留痕」）
- 4.1 依赖 1.2 的 `users.email_verified` 列，否则分支 5/6 无法表达
- 3.2 的 PKCE 本地预检依赖 1.3 的 `code_challenge` 列
