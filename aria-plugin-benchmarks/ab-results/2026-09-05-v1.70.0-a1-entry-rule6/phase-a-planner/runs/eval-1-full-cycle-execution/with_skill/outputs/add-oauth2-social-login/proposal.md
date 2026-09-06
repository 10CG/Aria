# Add OAuth2 Social Login (GitHub + Google)

> **Level**: Full (Level 3)
> **Status**: Draft — post_spec audit R1+R2+R3 已吸收；**未达 PASS，A.2 门禁状态见文末「审计结论」**
> **Created**: 2026-09-05
> **Linked Issue**: `none`
> **审计轨迹**: 同目录 `audit-trail.md` (append-only, 与本收敛型规格分居两文)

## Why

当前登录只有本地账号密码一条路径，新用户注册转化受阻，且密码重置/凭据保管的运维成本全部落在本项目。GitHub 与 Google 覆盖目标用户的绝大多数已有身份，接入这两家 OAuth2 提供方可以让新用户零密码注册、老用户把社交身份绑定到既有账号，同时把凭据保管责任外移给提供方。

选择 GitHub + Google 而不是"先做一个"，是因为两家的差异（GitHub 的 email 可能不公开且可多个、Google 的 `email_verified` 与 OIDC `sub`/`nonce`）恰好能把 provider 抽象层的接缝一次性压出来。

## What

在现有认证系统上新增 OAuth2 Authorization Code + PKCE 登录路径，支持 GitHub 与 Google 两个提供方，并支持社交身份与既有本地账号的绑定 (account linking)。

### In scope

#### A. Provider 抽象层

```
authorize_url(state, code_challenge, nonce | None)     -> str
exchange_code(code, code_verifier, redirect_uri)       -> TokenResponse{access_token, id_token?, expires_in}
fetch_identity(token_response, expected_nonce | None)  -> NormalizedIdentity
```

- `nonce` 仅 OIDC provider (Google) 生成与校验；**禁止**用 `state` 顶替
- **双向 fail-closed**：OIDC adapter 收到 `expected_nonce is None` 必须抛错（不得跳过校验）；非 OIDC adapter (GitHub) 收到**非** `None` 的 `expected_nonce` 也必须抛错（挡 provider mix-up 的另一个方向）
- `redirect_uri` 是显式入参，取值来自服务端配置常量 (§F)，不接受任何请求参数注入
- `NormalizedIdentity` 字段：`provider`, `provider_user_id`, `email`, `email_verified`, `display_name`, `avatar_url`
- provider 注册表由配置驱动（新增第三家 = 一个 adapter + 一段配置，不改路由层）

#### B. 两个 adapter

**GitHub**（`fetch_identity` 用 `access_token` 调 REST，`expected_nonce` 必为 `None`）：`provider_user_id` = `GET /user` 的数字 `id`（**不是** `login`）。邮箱**只从 `GET /user/emails` 取**，`GET /user` 的 profile `email` 字段**禁止**作为来源。四种输入形态穷尽：

| `GET /user/emails` 输入形态 | `email` | `email_verified` |
|---|---|---|
| 存在 `primary && verified` 的邮箱 | 该邮箱 | `true` |
| 有 primary 但 unverified（无论是否另有 verified 邮箱） | `null` | `false` |
| 无 primary 标记，但存在 ≥1 个 verified 邮箱 | `null` | `false` |
| 无任何 verified 邮箱 / 邮箱不可见 / 接口 403 | `null` | `false` |

> 推论（承重）：GitHub **永不产出** `email != null && email_verified == false`。故 §D 分支 4 对 GitHub 不可达，SC-4 必须点名 **Google**。

**Google**（OIDC）：discovery 取 JWKS，本地校验 `id_token`（签名 / `iss` / `aud` / `exp` / `nonce == expected_nonce` 逐字相等），不调 userinfo。`provider_user_id` = `id_token.sub`；`email` / `email_verified` 取自同名 claim。

#### C. 路由与会话

**`GET /auth/{provider}/start?next=<path>`**
1. 生成 `state`、PKCE `code_verifier` 与 `code_challenge = S256(code_verifier)`、(仅 OIDC) `nonce`，连同 `provider` / `next` / `session_binding` **同批**写入 `oauth_transactions` (§E.2)，得 `txn_key`
2. `session_binding` = 当前登录前匿名会话 ID 的 HMAC（服务端密钥）；无匿名会话时先创建
3. `txn_key` 写进关联 cookie；**该 cookie 与承载匿名会话 ID 的 cookie 属性一律为** `__Host-` 前缀 + `HttpOnly` + `Secure` + `SameSite=Lax`（**禁止** `Strict` —— Strict 会让从提供方顶层跳回时 cookie 不发送，整条流程静默失败）
4. 302 到 `authorize_url(...)`

**`GET /auth/{provider}/callback`** —— 校验顺序钉死，任一步失败即返回对应码：

| 步 | 动作 | 失败码 |
|---|---|---|
| 0 | query 含 `error`（如 `access_denied`）⇒ 按步 4 消费事务 + 302 回登录页，**不打 `ERROR` 告警**（用户取消是常规交互） | `oauth_user_denied` |
| 1 | 查找键 = cookie 里的 `txn_key`，查找条件 `WHERE txn_key=? AND provider=:path_provider`（挡跨 provider 复用）；无 cookie / 查无此行 | `oauth_state_invalid` |
| 2 | 行内 `state` 与 query `state` **逐字相等**（挡"自己的 cookie + 别人的 state"） | `oauth_state_invalid` |
| 3 | 行内 `session_binding` 与当前匿名会话重算值相等 | `oauth_state_invalid` |
| 4 | 一次性消费：`UPDATE oauth_transactions SET consumed_at=now() WHERE txn_key=? AND provider=? AND consumed_at IS NULL AND expires_at>now()`；**影响行数为 0 即判定已用过/已过期**（不做先读后写） | `oauth_state_invalid` |
| 5 | **PKCE 本地预检**：行内 `code_verifier` 非空 **且** `S256(code_verifier) == code_challenge`；不满足则**不发起** token 交换 | `oauth_pkce_invalid` |
| 6 | `exchange_code` → 提供方返回 `invalid_grant` | `oauth_pkce_invalid` |
| 7 | `fetch_identity(token_response, expected_nonce)` | `oauth_nonce_invalid` |
| 8 | §D 账号解析 → **先轮换会话标识**，再沿用既有 session/JWT 签发路径 | 见 §D 表 |

**回跳目标**：`next` 只接受站内相对路径且必须命中回跳白名单；不命中则忽略回落首页。发给提供方的 `redirect_uri` 是服务端常量，**任何请求参数都不能影响它**。

**error_code 枚举（封闭 + fail-closed）**：
`oauth_state_invalid` / `oauth_nonce_invalid` / `oauth_pkce_invalid` / `oauth_provider_unavailable` / `oauth_user_denied` / `oauth_email_required` / `oauth_email_unverified` / `oauth_link_ambiguous` / `oauth_pending_invalid` / `oauth_link_denied`

> 新增失败分支**必须先扩这个枚举**；任何未列举的失败一律映射为 500 + `ERROR` 告警，**不得**回落到某个已有码（SC-21 钉这条）。

#### D. 账号解析与绑定

自上而下判定，**命中即返回、不再判断后续分支**（if-elif 链，不得写成多个独立 if）。判据三维：`email` 是否 null × provider 侧 `email_verified` × §D.1 归一化匹配数：

| # | 条件 | 动作 | error_code |
|---|---|---|---|
| 1 | `(provider, provider_user_id)` 命中 `user_identities` | 登录该 user | — |
| 2 | `email == null` | 写 pending(lane=**EMAIL**) | `oauth_email_required` |
| 3 | §D.1 匹配数 **≥2**（**与 `email_verified` 无关**，本行必须早于第 4 行） | 拒绝绑定 + 写 pending(lane=**MANUAL**，**不向浏览器下发 `pending_key`**) + 打 `ERROR` 告警 | `oauth_link_ambiguous` |
| 4 | provider `email_verified == false`（此时匹配数只可能 0 或 1） | 写 pending(lane=**VERIFY**) | `oauth_email_unverified` |
| 5 | `email_verified == true` 且匹配数 1 且**该既有 user 的本地 `users.email_verified == true`** | 自动绑定并登录 | — |
| 6 | `email_verified == true` 且匹配数 1 但本地 `users.email_verified == false` | 写 pending(lane=**VERIFY**)，走密码确认 | `oauth_email_unverified` |
| 7 | `email_verified == true` 且匹配数 0 | 按 §D.2 新建 | — |

> 第 5/6 行的分野是 R3 补的承重条件：只信 provider 侧 verified 而不问本地邮箱是否验证过，等于把每个存量未验证邮箱账号变成一键接管入口。

**§D.1 email 匹配规则（钉到字符级，两侧同源）**
- 归一化 = 去首尾空白 + 整串 **ASCII** 小写化。**禁止** plus 别名剥离、**禁止** dot 归一化、禁止任何 provider 特有折叠
- **落地方式不用函数索引**：`users` 增冗余列 `email_normalized`（写入侧由应用层用上面同一个函数产生）+ 普通 `UNIQUE(email_normalized)`；查询形态 `WHERE email_normalized = :normalized`
  （不用 `UNIQUE INDEX ON lower(trim(email))`：函数索引在 MySQL <8.0.13 / SQL Server 上不可直接建，且 SQL `lower()` 是 locale/Unicode 相关的，与"ASCII 小写化"在非 ASCII 本地部分上会给出两套等价关系）
- 迁移在建唯一约束**之前**跑存量去重检查，发现归一化后重复 ⇒ **失败退出**并列出冲突行（不自动合并账号）
- 约束建成后匹配数 ≥2 在正常数据下不可达；分支 3 是**防御性分支**，其测试用 mock repository 返回 2 行构造 (SC-17)

**§D.2 新建事务语义**
- 单事务内：**先插 `users`，再插 `user_identities`**（`user_identities.user_id` 是 `NOT NULL` FK，反序当场违反 FK；防孤儿靠事务原子性，不是插入顺序）
- **两类唯一冲突各有恢复动作**（缺一就是未处理异常 → 500）：
  - `UNIQUE(provider, provider_user_id)` 冲突 ⇒ 整事务回滚 ⇒ 重查改走分支 1
  - `UNIQUE(users.email_normalized)` 冲突 ⇒ 整事务回滚 ⇒ 重查改走分支 5/6
- 事务隔离级别假设**不高于 READ COMMITTED**；若部署在更高级别，条件更新与本节冲突捕获须额外 catch 可串行化冲突并映射为 `oauth_state_invalid`，不得逃逸成 500
- **§G 建号路径**：`pending_key` 的消费 UPDATE 与 `users`/`user_identities` 的 INSERT 必须落在**同一事务**（否则 key 已烧而账号未建 = 死路）；且 lane EMAIL 补填邮箱后必须**重入 §D 判定表**，不得直接建号

#### E. 数据模型

**E.1 `user_identities`**：`(id, user_id NOT NULL FK→users, provider, provider_user_id, email, email_verified, created_at, updated_at)`；`UNIQUE(provider, provider_user_id)`；索引 `(user_id)`。
**`users` 侧**：需要 `email_normalized`（见 §D.1）与 `email_verified` 两列 —— 若既有 schema 已有等价列则复用并在迁移注明列名映射；回填口径：存量已完成邮箱验证的账号置 `true`，其余置 `false`（**不得**默认 `true`）。

**E.2 `oauth_transactions`**：`(txn_key PK, provider, state, code_verifier, code_challenge, nonce, next_path, session_binding, created_at, expires_at, consumed_at)`。`txn_key` ≥128bit 随机不可枚举；一次性由 §C 步 4 条件更新保证；TTL 10 分钟；`expires_at` 建索引。

**E.3 `pending_identities`**：`(pending_key PK, provider, provider_user_id, email, email_verified, display_name, avatar_url, lane, session_binding, created_at, expires_at, consumed_at)`。
- `pending_key` ≥128bit 随机，载体与 `txn_key` 同款（`__Host-` cookie + `HttpOnly`+`Secure`+`SameSite=Lax`），**禁止**出现在 URL / query / hidden field
- 一次性消费 SQL 与 §C 步 4 同形态：`UPDATE pending_identities SET consumed_at=now() WHERE pending_key=? AND consumed_at IS NULL AND expires_at>now()`，影响行数为 0 即拒绝
- 两个端点必须重算比对 `session_binding`（同 §C 步 3），并按 **lane 白名单**受理：`/auth/link/confirm` 只收 `lane=VERIFY`，`/auth/link/email` 只收 `lane=EMAIL`；lane 不匹配 ⇒ `oauth_pending_invalid`，**且不得按 email 重新查候选人**
- 身份字段只存服务端；客户端只持有 `pending_key`

**E.4 迁移**：三张表 + `users` 两列 + 唯一约束，全部可逆 (up/down)。

#### F. 安全与配置

- `state` 一次性、TTL ≤ 10 分钟、经 `txn_key` cookie + `session_binding` 双重绑定
- PKCE S256 强制；`code_verifier` 只活在服务端事务行，从不随浏览器往返；`code_challenge` 入库供 §C 步 5 本地预检
- `nonce` 一次性、仅 OIDC、与 `state` 分离存储与比对
- 所有本流程 cookie（匿名会话 / `txn_key` / `pending_key`）统一 `__Host-` + `HttpOnly` + `Secure` + `SameSite=Lax`
- **会话固定防护**：签发登录会话前必须轮换会话标识
- 发给提供方的 `redirect_uri` 是服务端常量，**进程启动时**与白名单精确匹配，不匹配则**启动即失败**；禁止通配
- client secret 只从环境变量/密钥管理读取，禁止入库、禁止进日志；日志中 token / code / secret / id_token / code_verifier 一律脱敏
- 提供方 access token 用完即弃（本期不做 refresh token 存储）

#### G. 待确认流程（三条 lane）

lane 由 §D 判定表第 2/3/4/6 行产生，**端点侧按 lane 白名单受理**（见 §E.3）：

| lane | 产生自 §D | 用户要做什么 | 端点 | 完成后 |
|---|---|---|---|---|
| **EMAIL** | 第 2 行 | 补填邮箱 + 走既有邮箱验证流程 | `POST /auth/link/email` | **重入 §D 判定表**（拟定值 D-2：强制补填，不允许无邮箱账号） |
| **VERIFY** | 第 4 / 6 行 | 输入本地账号密码确认绑定；无匹配账号时走邮箱验证后按 §D.2 建号 | `POST /auth/link/confirm` | 绑定或建号（拟定值 D-1：密码确认页，不走确认邮件） |
| **MANUAL** | 第 3 行 (≥2 匹配) | 无自助出口，提示联系支持 | 无（**不下发 `pending_key`**，仅服务端留档供 §H） | 运维处置 |

失败码：`oauth_pending_invalid`（key 无效/过期/已消费/lane 不匹配/`session_binding` 不符）、`oauth_link_denied`（密码确认失败）。

#### H. 运维与 CI 变更

- **最小解绑**：`unlink-identity --user-id --provider`，删一行 `user_identities` + 写审计日志；若该 user 无本地密码且这是最后一条 identity ⇒ **拒绝**并非零退出
- **过期行清理**：定时任务清 `oauth_transactions` / `pending_identities` 中 `expires_at < now()` 的行，另配 lazy delete-on-read
- **CI**：secret 扫描步骤；覆盖率产出物（路径 + 阈值 gate）供 SC-11；日志调用点静态扫描供 SC-8

### Out of scope

- 第三家及以上提供方 (Apple / Microsoft / 企业 SSO / SAML)
- 面向终端用户的多身份管理 UI 与自助解绑（运维侧最小解绑已在 §H）
- 管理员侧"查看用户已绑定身份"的只读视图
- 用社交身份做 API 授权；provider refresh token 的存储与轮换

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 新用户注册路径缩短为一次跳转；密码相关支持工单预期下降 |
| **Positive** | provider 抽象层落地后，接第三家 = 一个 adapter + 一段配置 |
| **Risk (High)** | **账号劫持**：缓解 = §D 判定表（含本地 `email_verified` 合取条件）+ §D.1 字符级规则 + §E.3 服务端存储与 lane 白名单，由 SC-4 / SC-12 / SC-13a / SC-13b / SC-22 / SC-28 钉死 |
| **Risk (Medium)** | **回调伪造 / CSRF / 重放 / provider mix-up / session fixation**：缓解 = §C 八步 + `session_binding` + PKCE 本地预检 + `nonce` + 会话轮换，对应 SC-5 / SC-5b / SC-14a / SC-14b / SC-15 / SC-20 / SC-26 / SC-27 / SC-29 |
| **Risk (Medium)** | **密钥泄漏**：缓解 = secret 只走环境变量 + 日志调用点静态扫描 (SC-8) |
| **Risk (Medium)** | **绑定不可逆**：缓解 = §H `unlink-identity` + 审计日志 (SC-18) |
| **Risk (Low)** | **提供方不可用**：返回 `oauth_provider_unavailable`，本地密码登录不受影响 (SC-10) |

## Tasks

任务拆分见同目录 `tasks.md` (Layer 1) 与 `detailed-tasks.yaml` (Layer 2, 由 task-planner 于 A.2/A.3 生成)。本节不重复列举以免双写漂移；工时估算只出现在 Layer 2。

## Success Criteria

- [ ] **SC-1** GitHub 全新用户走完 start→callback：`users` +1、`user_identities` +1 且 `provider='github'`、`provider_user_id` = `/user` 数字 `id`（fixture 里 `id != login`），会话 cookie 过既有中间件
- [ ] **SC-2** Google 同上，`provider_user_id == id_token.sub`（fixture 里 `sub != email`）
- [ ] **SC-3** 既有已验证账号 `a@example.com` + Google `email_verified=true` ⇒ 不新建 user，`user_identities` +1 指向既有 `user_id`
- [ ] **SC-4** **负向**（必须用 Google）：`email_verified=false` ⇒ (a) 无对应 `user_identities` 行；(b) 未签发会话；(c) `oauth_email_unverified`；(d) 产生 1 行 `pending_identities` 且 `lane=VERIFY`。**不用** "`users` 计数不变" 做指标
- [ ] **SC-5** **负向**：`state` 缺失 / 过期 / 已消费 / 与事务行不等 ⇒ 四次全 4xx + `oauth_state_invalid` + 不签发会话
- [ ] **SC-5b** **负向**：(a) 完全不带关联 cookie；(b) 带浏览器 B 自己合法未消费的 cookie 但 query `state` 换成 A 的 ⇒ 两次都 4xx
- [ ] **SC-6** 启动时 `redirect_uri` 不在白名单 ⇒ 进程非零退出；`next` 传站外/白名单外 ⇒ 忽略回落首页且不影响发给提供方的 `redirect_uri`
- [ ] **SC-7** 两次独立授权并发 callback 指向同一 `(provider, provider_user_id)` ⇒ `user_identities` 恰好 1 行、`users` 恰好 1 行、两次响应都非 5xx
- [ ] **SC-8** 静态扫描全部日志调用点：实参须落在白名单内，出现 `client_secret`/`code`/`access_token`/`id_token`/`code_verifier` 即失败；运行期 grep 只作补充
- [ ] **SC-9** 迁移 up→down→up 可重复，schema 与首次 up 后逐字一致
- [ ] **SC-9b** 存量 `users` 含归一化后重复邮箱 ⇒ 迁移失败退出并列冲突行
- [ ] **SC-10** 提供方 token 端点 5xx / 超时 ⇒ `oauth_provider_unavailable`；同一测试进程内本地密码登录仍 200
- [ ] **SC-11** adapter + §D 解析层分支覆盖率 ≥ 85%，报告由 CI 产出物给出
- [ ] **SC-12** **负向**：`a+x@example.com` 不得命中 `a@example.com`；`a.b@gmail.com` 不得命中 `ab@gmail.com`
- [ ] **SC-13a** **负向**：篡改 `pending_key` ⇒ `oauth_pending_invalid`、无 identity 行产生
- [ ] **SC-13b** **负向**：`pending_key` 正确但本地密码错误 ⇒ `oauth_link_denied`、无 identity 行产生
- [ ] **SC-14a** **负向（白盒）**：构造 `code_verifier` 为 NULL / 与 `code_challenge` 不匹配的事务行 ⇒ `oauth_pkce_invalid` + provider mock 收到**零**次 token 请求（宿主 = §C 步 5）
- [ ] **SC-14b** 提供方返回 `invalid_grant` ⇒ 映射 `oauth_pkce_invalid`（此路径 token 交换必已发起，与 SC-14a 的零请求互斥）
- [ ] **SC-15** **负向**：`id_token.nonce` 缺失 / 不等 ⇒ `oauth_nonce_invalid`；且同一流程内 `nonce != state`
- [ ] **SC-15b** **负向**：OIDC adapter 收 `expected_nonce=None` ⇒ 抛错；GitHub adapter 收非 `None` ⇒ 抛错（双向 fail-closed）
- [ ] **SC-16** GitHub `email=null` 全新用户 ⇒ 不建 `users`/`user_identities`，返回 `oauth_email_required` + 1 行 `pending_identities`(lane=EMAIL)
- [ ] **SC-17** §D 分支 3 防御性分支：mock repository 返回 2 行 ⇒ `oauth_link_ambiguous` + 1 条 `ERROR` 告警 + **不新增 `users` 行** + 产生 1 行 `pending_identities`(lane=MANUAL) 且**未向响应下发 `pending_key`**
- [ ] **SC-18** `unlink-identity` 执行后目标行消失 + 1 条审计日志；对"无本地密码 + 最后一条 identity"的 user 执行 ⇒ 拒绝并非零退出
- [ ] **SC-19** lane EMAIL 两个 `pending_key` 并发补填同一 `(provider, provider_user_id)` ⇒ `users` 恰好 1 行、`user_identities` 恰好 1 行
- [ ] **SC-20** **负向**：合法未消费 `txn_key` + 匹配 `state`，但匿名会话变更致 `session_binding` 重算不等 ⇒ 4xx（使"`session_binding` 当死列"的实现必红）
- [ ] **SC-21** **负向（fail-closed 兜底）**：注入一个刻意不在枚举内的内部异常 ⇒ 响应 500 且 body 的 error_code **不等于**枚举十码中任何一个 + 产生 `ERROR` 告警
- [ ] **SC-22** **负向**：拿 lane=MANUAL 的 `pending_key`（白盒构造）打 `/auth/link/confirm`，即使密码正确 ⇒ `oauth_pending_invalid`、无 identity 行；同理 lane=EMAIL 的 key 打 confirm 端点亦拒
- [ ] **SC-23** **负向**：异浏览器持合法未消费 `pending_key`（`session_binding` 不符）⇒ 4xx、无 identity 行
- [ ] **SC-24** 定时清理跑后过期行清零、未过期行不受影响；且对尚未被定时任务清理的过期行，一次读路径触发后该行消失
- [ ] **SC-25** 用户在提供方点取消 (`error=access_denied`) ⇒ `oauth_user_denied` + 302 回登录页 + 事务行被消费 + **零** `ERROR` 告警
- [ ] **SC-26** **负向**：拿 provider A 的 `txn_key`/`state` 打 `/auth/{B}/callback` ⇒ `oauth_state_invalid`，且**零**次 token 请求
- [ ] **SC-27** **正向**：经真实跨站顶层 302 回跳后，三个 cookie 均随请求发送、`session_binding` 重算相等、流程 2xx（使把任一 cookie 设成 `SameSite=Strict` 的实现必红）
- [ ] **SC-28** **负向**：既有 user 本地 `email_verified=false`，Google 返回同邮箱 `email_verified=true` ⇒ **不自动绑定**，返回 `oauth_email_unverified` 并写 lane=VERIFY
- [ ] **SC-29** 登录会话签发前会话标识发生轮换（断言签发前后标识不同）
- [ ] **SC-30** 并发致 `UNIQUE(users.email_normalized)` 冲突 ⇒ 回滚后重查改走分支 5/6，响应非 5xx

## Open Questions / 决策留痕

原 Q1/Q2 已写进 §G 正文以消除"无代码宿主的分支"，但**写进正文不等于已获批准**：

| 项 | 现行正文取值（**拟定值**） | 性质 | 状态 |
|---|---|---|---|
| **D-1** | lane VERIFY 走密码确认页，不走确认邮件 | 产品级 | `awaiting_owner_ratification` |
| **D-2** | lane EMAIL 强制补填邮箱，不允许无邮箱账号 | 产品级 | `awaiting_owner_ratification` |

**不适用"无回应即批准"**。Phase B 可先做不依赖它们的部分（§A / §B / §C / §D / §E）；门禁锚点 = **"§G 待确认流程"对应的那两个任务**；A.2 生成后回填为 **TASK-014 / TASK-015**（`tasks.md` 5.1 / 5.2），二者在 D-1/D-2 获批前不得进入 `in_progress`（已写进 `detailed-tasks.yaml` 的 `gates` 与两任务的 `blocked_by_gate`）。

原 Q3（管理员只读视图）非阻塞项，已删除并在 Out of scope 补为显式条目。

## 审计结论 (post_spec, 截至 R3)

三轮 convergence 审计，计数由脚本按两种口径机械重算（口径定义与逐簇表见 `audit-trail.md`）：

| 轮次 | 簇口径 C/M/m | 上一轮修复引入占比 |
|---|---|---|
| R1 | 7 / 14 / 4 | — |
| R2 | 5 / 12 / 3 | 96% |
| R3 | 7 / 8 / 2 | 76% (每席上限由 6 降为 5, 绝对值不严格可比) |

MAJOR 簇 **14 → 12 → 8 仍在降**，但每轮发现里 **>3/4 是上一轮修复自己引入的**，且 CRITICAL 每轮都落在上一轮**新写的章节**上。两条判据结论相反，故 R4 作为**表决轮**执行（见文末交付说明）。

## References

- OAuth 2.0 Authorization Code + PKCE (RFC 7636)
- OpenID Connect Core 1.0 §3.1.3.7
- GitHub REST `GET /user` / `GET /user/emails` 的 `primary` / `verified` 语义
