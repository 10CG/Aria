# OAuth2 Social Login (GitHub + Google)

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-09-05
> **Linked Issue**: `none`
> **Change ID**: `oauth2-social-login`
> **Revision**: R5-fixed (post_spec 审计 5 轮 findings 已吸收)

> Status 字段刻意保持**单值枚举**，不承载任何条件语句 —— 把 blocker 叙述塞进 Status 已在本项目两次造成机读分类 bug (aria-plugin #101 substring-shadow / #50 status-extraction-range)。门槛写在下面的「现状锚点」节。

## 现状锚点 (A.0 未解析项)

本 Spec 反复引用「既有邮箱账户体系」「既有 session/JWT 签发器」「既有邮箱密码登录」。这些引用必须落到具体路径才可实现、可核验。A.0 状态扫描**未能解析**以下六项 (本仓无对应应用代码，须在目标代码库内解析):

| # | 锚点 | 用途 | 状态 |
|---|------|------|------|
| A-1 | `users` 表定义位置 (迁移文件 / ORM 模型) | `identities.user_id` 外键与 DEC-1 级联的落点 (tasks 1.1) | ⛔ 未填 |
| A-2 | session / JWT 签发模块路径 | tasks 3.4 的复用点；决定「不新建并行身份体系」是否真成立 | ⛔ 未填 |
| A-3 | 既有邮箱密码登录路由与其回归用例集路径 | SC-6 / SC-8 的被测对象 (tasks 5.5) | ⛔ 未填 |
| A-4 | `users` 密码列的**可空性** + `has_password` 的判定方式 (列名或派生逻辑) | unlink 不变量与矩阵 D3 (建无密码用户) 的承重前提 | ⛔ 未填 |
| A-5 | `users.email` 是否有唯一约束 + email 匹配所用的**规范化规则** (大小写、Gmail 点号/加号别名是否折叠) | 决策矩阵第 4 列的「匹配」动作本身是否可判定；无此项则 D6 (匹配到 ≥2 个 user) 的可达性无法评估 | ⛔ 未填 |
| A-6 | 账户状态字段 (停用 / 锁定 / 软删除) 及其在既有邮箱密码登录路径上的校验位置 | 矩阵第 6 列；缺它则社交登录成为绕过账户状态校验的旁路 | ⛔ 未填 |

**门槛 (三条，互不重叠，避免自锁)**:

1. `tasks 1.4` 是解析这六项的**零号任务**，它**可以且必须在 Draft 态执行** —— 不受下面两条门槛约束 (否则「Approved 需锚点 → 锚点需跑 1.4 → 1.4 需 Approved」构成循环死锁)。
2. 六项全部变成具体路径/结论前，本 Spec **不得进入 Approved** (Approved 语义 = 可进入实现)。
3. 除 `1.4` 外，Phase B 其余任务不得开工 (由第 2 条自然蕴含，此处显式重述以防 Status 被人工提前推进)。
4. **Impact 表中标注「需 owner 签字接受」的残留风险 (`provider_user_id` 稳定性假设) 未拿到签字前，同样不得进入 Approved** —— 与锚点走同一道门。否则「一条已知无防线的接管路径」可以在无人拍板的情况下随 Spec 一起被批准，正是本 Spec 前面已犯过一次的「空洞不挡 Approved」。

- **A-4 的分支后果**: 若解析结果为「密码列 NOT NULL」，矩阵 D3 无法建无密码用户，须追加一条 `users` 迁移任务与对应 SC —— 该分支在锚点解析前不可判定，不得靠猜。
- **A-5 / A-6 的分支后果**: 若 `users.email` 无唯一约束，D6 是真实可达分支而非理论情形，SC-24 必须用真实双匹配数据构造；若账户状态字段不存在，需与 owner 确认既有登录路径是否本就无此校验 (不得由本 Spec 单方面发明一套)。

## Why

当前登录只支持「邮箱 + 密码」，新用户注册转化受口令创建与验证邮件两步流失影响，且平台自持口令带来长期的凭据保管与泄露责任。GitHub / Google 覆盖目标用户群体的绝大多数已有身份，接入这两家的 OAuth2 社交登录可同时降低注册摩擦与自持凭据的风险面。

## What

新增 OAuth2 **Authorization Code + PKCE** 通道，支持 GitHub 与 Google 两个 provider，覆盖两条**流程 (flow)**:

- `flow = login`: 未登录用户经第三方身份登录 / 注册
- `flow = link`: **已登录**用户在账户设置页把第三方身份关联到**当前会话用户**

两条流共用端点与存储，但走**不同的决策规则** (见决策矩阵) —— 这是承重区分: 用同一套 email 匹配规则跑 link 流会导致会话被静默切换到他人账户。

### Key Deliverables

- Provider 无关的 OAuth2 抽象层 (`OAuthProvider` 接口 + `ProviderTokens` / `NormalizedIdentity` 契约) + GitHub / Google 两个适配器
- `identities` 表与既有 `users` 表的关联迁移 (约束见「数据模型」)
- 三个端点: `GET /auth/oauth/{provider}/start`、`GET /auth/oauth/{provider}/callback`、`POST /auth/identities/{id}/unlink`
- `state` + `nonce` + `code_verifier` + `binding_id` + `flow` **同记录**存于共享短时存储，原子一次性消费
- pre-auth 绑定 cookie (未登录用户在 start 时也有非空 `binding_id`)
- 前端「使用 GitHub / Google 登录」入口 + 账户设置页的身份管理 (查看 / 关联 / 解绑)
- 三端点限流接入
- **文档同步产出** (Rule #3): API/OpenAPI 三端点、架构文档认证时序与 `identities` schema、运维文档 provider 凭据配置与轮换 —— 与代码同批交付 (SC-16)

### 非目标 (Out of Scope)

- **本 Spec 只实现 GitHub 与 Google 两个 provider**；其余 (Apple / 微信 / 企业 SSO / SAML / 任何其他提供方) 由后续 Spec。判据是**名单**不是协议族 —— 用「OIDC 之外」当判据会把无 OIDC 的 GitHub 自己排除掉
- 不实现「社交注册后补设密码」的口令回填 (后续 Spec)。与 unlink 锁死风险的耦合处置见「unlink 不变量」
- 不改动既有邮箱密码登录的会话签发机制 (复用同一签发器)
- 不做 provider 侧业务 API 调用 (只取身份)
- 不做站内邮箱二次验证流程

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 注册路径从 3 步缩短为 1 次跳转授权；平台不再为社交登录用户保管口令 |
| **Positive** | Provider 抽象层使新增 provider 成本收敛到「一个适配器 + 一组配置」—— 以「Provider 抽象契约」写死的接口为前提，非空口承诺 |
| **Risk** | **账户接管 · 邮箱路径**: 缓解 = 只在 `email_verified == true` 时自动关联，其余 fail-closed (SC-3) |
| **Risk** | **账户接管 · 多绑路径**: 缓解 = `UNIQUE(provider, provider_user_id)` 数据库硬约束 (SC-11) |
| **Risk** | **会话劫持 · link 流**: 已登录用户关联他人已持有的身份时若复用 login 规则会静默切换会话主体。缓解 = flow 维度分流 + `409 identity_taken` (SC-17) |
| **Risk** | **CSRF / 授权码注入 / 重放**: 缓解 = binding 绑定 + 原子一次性消费 + PKCE S256 (拒 `plain`) + nonce 校验 (SC-2 / SC-9 / SC-12) |
| **Risk** | **开放重定向**: 缓解 = `redirect_uri` 服务端常量不可被参数覆盖 (SC-18) + `next` 同源白名单 (SC-13) |
| **Risk** | **账户锁死**: 缓解 = unlink 不变量 (SC-10)；其判定依赖锚点 A-4 |
| **Risk** | **provider 不可用**: 缓解 = 失败降级回邮箱密码登录并给可读错误码 (SC-8) |
| **Risk** | **滥用**: callback 外部可达。缓解 = 三端点限流 (SC-19) |
| **Risk** | **`provider_user_id` 稳定性假设失效 (已知残留风险, 需 owner 签字接受)**: 本 Spec 无条件信任「provider 侧 ID 稳定不可变」。provider 账号被删后 ID 被回收、或账号所有权转让 (企业 Workspace 离职邮箱回收再分配是常见场景) 时，D1 会把新主人登进旧账户。现有唯一相关信号 = D1 的 email 漂移事件，它 (a) 是**事后检测** —— 告警投递时登录已放行；(b) **只在 email 也变化时触发** —— 而 Workspace 转让恰恰连 email 一起转移，此时该事件根本不会触发，接管**无声且不可检测**。本 Spec **不提供**对该最坏子情形的防线，明确列为残留风险；若 owner 不接受，须追加一条「与账户最近活跃时间/状态做二次校验」的任务与 SC (本期未规划) |
| **Risk** | **身份漂移事件无消费方 (已知残留风险)**: D1 检出 provider 侧 email 变化时写一条 error 级结构化事件，但本 Spec 未规划风控/告警队列、锚点表也无其位置、38 项任务里无人建它或接它 ⇒ 该事件**写下来没人看**。刻意**不**在验收里写「断言消费方收到」—— 无代码宿主的机制只能靠 stub 满足，那是假绿。若 owner 要求它成为真缓解，须追加一条锚点 (既有队列及投递 API 位置) + 一条接入任务 + 配套 SC，本期未规划 |
| **Risk** | 新增 `identities` 表与迁移，回滚需成对 down migration (SC-7) |

## 数据模型

```sql
identities(
  id            PK,
  user_id       FK -> users(id) ON DELETE CASCADE,   -- DEC-1
  provider      TEXT NOT NULL,        -- 'github' | 'google'
  provider_user_id TEXT NOT NULL,     -- provider 侧稳定不可变 ID (非 email/username)
  email_at_link TEXT,                 -- 关联时快照, 仅供审计, 不作为后续匹配依据
  created_at, updated_at
)
UNIQUE (provider, provider_user_id)   -- 承重: 一个第三方身份只映射一个本站用户
UNIQUE (provider, user_id)            -- DEC-2: 同一用户同一 provider 只允许一个账号
INDEX  (user_id)
```

- **DEC-1 (FK 级联)**: `ON DELETE CASCADE`。删 user 连带删其 identity，不留孤儿、不阻塞删除；反向不成立。
- **DEC-2**: 本期不支持一个用户绑同一 provider 的多个账号。放开须先移除该约束并补迁移。
- **DEC-3 (D3 新建用户的密码列)**: 取值取决于锚点 A-4。若可空 → 写 NULL 并令 `has_password = false`；若 NOT NULL → **本 Spec 未规划的 users 迁移**，须先追加任务与 SC，不得用空串/随机值绕过 (空串会让 `has_password` 判定失真，直接破坏 unlink 不变量)。
- **unlink 不变量**: 当且仅当 `has_password == true` 或「解绑后仍剩 ≥1 个 identity」时允许解绑；否则 `409 last_login_method`。`has_password` 的判定来源即锚点 A-4，**不得由实现者自行发明**。前端亦不得渲染可点的解绑动作 (SC-14)。
- **越权**: `{id}` 必须属当前会话用户，否则 `404` (不用 403，避免探测他人 identity id 存在性)。

## Provider 抽象契约

两个适配器验证路径结构不同 (Google = OIDC discovery + id_token 验签；GitHub = 两次 REST + 邮箱筛选)，接口把差异吸收在实现内，只向上暴露统一形状:

```
interface OAuthProvider:
    name: str                                   # 'github' | 'google'
    authorize_url(state, nonce, code_challenge, redirect_uri) -> str
    exchange_code(code, code_verifier, redirect_uri) -> ProviderTokens
    fetch_identity(tokens, expected_nonce) -> NormalizedIdentity

ProviderTokens:
    access_token: str            # 必填非空
    id_token: str | None         # GitHub 恒 None; Google 恒非 None
    token_type: str
    expires_at: int | None

NormalizedIdentity:
    provider: str
    provider_user_id: str        # 必填非空, provider 侧稳定 ID
    email: str | None            # 无可信邮箱时为 None (不得填占位值)
    email_verified: bool         # 不变量: email is None ⇒ email_verified == False (SC-20b)
```

- `fetch_identity` 是唯一允许做 provider 专属校验的地方 (Google 在此校验 `iss`/`aud`/`exp`/`nonce`；GitHub 在此做邮箱筛选)。调用方只消费 `NormalizedIdentity`，**不得**出现 `if provider == 'github'` 形态分支 (SC-15)。
- **Google 且 `id_token is None`**: 抛机读 error code `id_token_missing`，**禁止**降级为「不验签放行」——这正是 fail-closed 最容易被绕开的口子。
- 任一校验失败一律 fail-closed 拒绝登录，不得回退到更弱路径。

## 技术方案要点

```
Browser ──1 GET /auth/oauth/github/start?flow=login&next=/dashboard──▶ App
        ◀─2 Set-Cookie: oauth_binding=<binding_id>; 302 to provider──
        ──3 用户在 provider 授权──▶ Provider
        ◀─4 302 /auth/oauth/github/callback?code&state──
        ──5 callback (带 binding cookie)──▶ App ──6 换 token──▶ Provider
                        7 fetch_identity → 8 决策矩阵(flow) → 9 签发会话 → 10 跳回 next
```

### 短时存储契约

- 介质: **共享**存储 (Redis 或 DB)。**禁止**进程内存 / 加密 cookie —— start 与 callback 可能落在不同实例。
- 一条记录 = `state`(key) + `nonce` + `code_verifier` + `binding_id` + `flow` + `link_user_id`(仅 link 流，是 link 流承重变量 `U` 的**唯一**来源) + `next_url` + `created_at`；TTL 10 min。
- **`binding_id` 恒非空**: 未登录用户在 start 时由服务端签发 pre-auth cookie，随 state 一次性消费同时失效；已登录用户用其会话 id 派生。**不允许该字段为 null** —— 否则跨会话绑定在最主要的首登路径上直接失效 (SC-2 断言其非空)。
- **cookie 必须按 flow 命名空间化**: cookie 名为 `oauth_binding_{state}` (不是固定名 `oauth_binding`)。浏览器 cookie 按 name+domain+path 存储、与标签页无关，固定名会让「tab1 走 GitHub、tab2 走 Google」的后者覆盖前者，tab1 回来时误杀为无效 state。属性: `HttpOnly` + `SameSite=Lax` + `Secure` + `Path=/auth/oauth`。
  > `SameSite=Lax` 在 provider 的 302 顶层 GET 导航上会被携带 —— 这是本设计成立的前提，**必须由 `5.17` 用真实浏览器 e2e 实测确认**，不得当作理所当然 (SC-26c)。实现侧 (`3.1`) 只负责按此属性种 cookie，实测义务在验收侧，两者不要弄混。
- **callback 侧比对**，并区分两种失败成因 (不可合并为一个码，否则禁用 cookie 的用户拿到的永远是「无效 state」这种不可自解释的提示):
  - cookie **缺失** → `403 binding_cookie_missing`，前端给出「请启用 cookie 后重试」的可操作提示
  - cookie **存在但不符** → `403 binding_mismatch`
- 消费必须**原子** (`GETDEL` / `DELETE ... RETURNING`)；read-then-delete 竞态视为缺陷 (SC-9)。

### redirect_uri 与 return-URL

- `redirect_uri` 是**服务端常量**，与 provider 后台注册值逐字一致；请求参数中的同名值一律忽略，不参与拼装 (SC-18)。
- 登录后跳转 `next` 只接受**同源相对路径**。判定按**白名单**而非黑名单: 规范化后必须匹配 `^/[A-Za-z0-9._~!$&'()*+,;=:@%/?-]*$` 且不以 `//` 或 `/\` 开头、不含反斜杠与控制字符；任何不匹配一律静默改用默认首页，绝不 302 到外域。
  > 验收侧注意 (author-to-match-checker 反模式): SC-13 的负控**不得只测本 Spec 出现过的形态**。本文档**刻意不给绕过样例** —— 给了就等于把合格样例集清空 (凡被列举的都不再满足「未列举」)。由实现者自选 ≥2 个**不在本 Spec 任何位置出现**的形态并在 PR 描述中列出，评审据此判定。

### Provider 差异

- **Google**: OIDC discovery；`id_token` 用 JWKS 验签并校验 `iss` / `aud` / `exp` / `nonce`。
- **GitHub**: 无 OIDC；额外调 `GET /user` 与 `GET /user/emails`。**可信邮箱**只取 `primary == true && verified == true` 的那一条；不存在时 (全未验证 / primary 未验证 / private / 未授 `user:email`) `email = None, email_verified = False`，**不**退取「非 primary 但 verified」的邮箱 (否则在 provider 侧新增一个可控邮箱即可指向他人账户)。
- **未知 `{provider}` 路径参数**: 三端点一律 `404`，不得 500、不得回落到默认 provider (SC-21)。
- **限流**: 三端点按 IP + binding 维度限流，超限 `429 rate_limited` (响应体给出被触发的维度，与其余拒绝分支统一为 `{status, error_code}` 二元组) (SC-19)。若既有网关已提供则接入既有机制并在实现说明中引用，不重复造。

### 关联决策矩阵

输入 = (`flow`, **发起时是否已有会话**, `identity_hit`, `email` 是否存在, `email_verified`, **匹配到的既有 user 基数**, 该 user 本 provider 是否已有 identity, **目标 user 账户状态**)。

### flow 的取值域与相容性 (start 端点强制，先于矩阵)

`flow` 是**第一分流维**且来自请求参数，因此它自身必须先被校验 —— 否则「flow 分流 + binding 绑定」这条承重防线只在 link 一侧成立:

| 情形 | 处置 |
|---|---|
| `flow` 缺失 或 取值 ∉ {`login`,`link`} | `400 invalid_flow`，**fail-closed**。**禁止默认 login** —— 默认 login 那支连 D0 都抓不到 (输入确实落在 login 表内)，两个实现者会给出语义相反的实现 |
| `flow=login` 且发起时**已有会话** | `409 already_authenticated`，要求先登出再发起。**这是承重条款**: 该路径上 `binding_id` 由受害者自己的会话派生、比对必然通过，攻击者递一个 `?flow=login` 链接即可把受害者会话静默换成攻击者的第三方身份 (受害者随后把数据写进攻击者账户) —— 与 link 侧被 L2 挡住的是同一形状，只是发生在 login 侧 |
| `flow=link` 且发起时**无会话** | `401 login_required`。**不得**放行到矩阵后落 L0 —— 用 `unresolved_identity_state` 这个通用码表达「你没登录」是不可自解释的错误 |

以上三条由 start 端点执行 (SC-27)，矩阵只处理已通过该校验的输入。

两条设计规则，违反任一即算矩阵欠定:

1. **第 5 列是基数 (0 / 1 / ≥2)，不是布尔「有/无」**。布尔化会把「同一 email 匹配到 ≥2 个既有 user」静默吞进「有」，落进 D2/D4a 后实现者只能取第一条 = 任意选中受害者的账户接管；D0 的 fail-closed 抓不到它 (它确实落在表内)。基数 ≥2 是否真实可达取决于锚点 A-5。
2. **账户状态是独立列**。签发器 (锚点 A-2) 通常只签发不校验状态，社交登录若不自查会成为绕过邮箱密码路径账户状态校验的旁路。

**flow = login** (无当前会话用户；出口 = 登录谁):

| # | identity_hit | email | verified | 匹配 user 基数 | 该 user 本 provider 已有 identity | 目标 user 状态 | 处理 |
|---|---|---|---|---|---|---|---|
| **D1** | ✓ | * | * | 不适用 | 不适用 | active | 登录该 identity 的 user。**不**用 provider email 覆盖站内 email；不同则更新 `email_at_link` 并写一条 **error 级结构化事件**。⚠️ **本期无消费方** —— 本 Spec 未规划风控/告警队列, 锚点表也没有它的位置, 因此该事件目前只是「写下来没人看」。**不把它当缓解措施**, 见 Impact 表同名残留风险行 |
| **D1-inactive** | ✓ | * | * | 不适用 | 不适用 | 非 active (停用/锁定/软删除) | 拒绝。错误码**登记为 `account_inactive` (占位)**，最终取值必须与既有邮箱密码路径逐字对齐 —— 取决于锚点 A-6，A-6 未解析前该码是待定的，此处显式登记以免它隐形于错误码枚举之外 |
| **D2** | ✗ | 有 | ✓ | 1 | ✗ | active | 建 identity 关联该 user 并登录 |
| **D2'** | ✗ | 有 | ✓ | 1 | ✓ (DEC-2 冲突) | * | 拒绝 `409 provider_already_linked` |
| **D2-inactive** | ✗ | 有 | ✓ | 1 | ✗ | 非 active | 拒绝，同 D1-inactive (同一占位码 `account_inactive`) |
| **D3** | ✗ | 有 | ✓ | 0 | 不适用 | 不适用 | 新建 user (密码列按 DEC-3) + identity 并登录 |
| **D4a-pw** | ✗ | 有 | ✗ | 1，且该 user `has_password == true` | * | * | 拒绝 `403 email_not_verified`，提示「先用邮箱密码登录，再到账户设置关联」 |
| **D4a-nopw** | ✗ | 有 | ✗ | 1，但该 user `has_password == false` (D3 建的纯 OAuth 用户) | * | * | 拒绝 `403 email_not_verified`，提示「请先用你已绑定的第三方账号登录，再到账户设置关联」。**不得**沿用「先用邮箱密码登录」—— 该用户没有密码，与 D4b 的不可执行指引是同一缺陷换了受害群体 |
| **D4b** | ✗ | 有 | ✗ | 0 | 不适用 | 不适用 | 拒绝 `403 email_not_verified`，提示「先在 {provider} 验证该邮箱后重试，或用邮箱注册」(**不**说「先登录」——无账户可登 = 不可执行指引) |
| **D5** | ✗ | 无 | (必 ✗) | 不适用 | 不适用 | 不适用 | 拒绝 `403 email_unavailable` |
| **D6** | ✗ | 有 | * | **≥2** | 不适用 | 不适用 | **fail-closed**: 拒绝 `403 ambiguous_email_match` + error 级告警。**绝不**从多个候选里选一个 (SC-24) |

**flow = link** (出口 = 绑或不绑，**永不切换会话主体**):

> 承重变量 `U` 的**唯一**来源 = 短时存储记录中 start 时快照的 `link_user_id`。callback 侧必须额外断言 `link_user_id == 当前会话 user_id`，不等一律 `403 session_subject_changed` 且不建 identity —— 「start 后登出、以他人身份登录再 callback」是 binding cookie 判别不了的 (cookie 值没变)。**不得**改用 callback 时的会话主体。

| # | identity_hit | 处理 |
|---|---|---|
| **L1** | ✓ 且 owner == U | 幂等成功 (已绑过)，不改会话 |
| **L2** | ✓ 且 owner ≠ U | 拒绝 `409 identity_taken`，**不改会话主体** |
| **L3** | ✗ 且 U 在本 provider 下已有 identity (DEC-2) | 拒绝 `409 provider_already_linked` |
| **L4** | ✗ 且 U 在本 provider 下无 identity | 建 identity 绑到 `U`。**完全跳过** D2/D3/D4/D6 的 email 匹配逻辑 (email 只写入 `email_at_link` 快照)。因 `UNIQUE(provider, provider_user_id)` 已由 L2 前置排除冲突，此处插入不会与 D2 语义打架 |
| **L-inactive** | `U` 自身为非 active (任何 identity_hit 取值) | 拒绝，同 `account_inactive`。**本行不可省略**: 若既有签发器只在登录时查一次账户状态而非每请求中间件持续校验 (A-6 目前只承诺给出「既有登录路径上的校验位置」，未承诺是否为 continuous middleware)，被停用但仍持旧会话的用户可在停用期间继续经 L4 关联新身份。A-6 若明确「middleware 层每请求校验」成立，本行退化为冗余守卫但仍保留 |

- **D0 / L0 (fail-closed 缺省)**: 任何未落入上两表的输入组合 → 拒绝 `403 unresolved_identity_state` + error 级结构化告警。
  > 覆盖率口径 (与 SC-5 的「无豁免」协调): D0/L0 在全枚举下端到端不可达，其覆盖由**直接调用 resolver 并传入构造的非法组合**的单元用例提供 (SC-20a，执笔任务 tasks 5.16)，不计入端到端路径清单。

## Tasks

- **Layer 1** `tasks.md` (同目录，与 proposal 同批产出，编号不可变)。**项数与估时以 tasks.md 的 Summary 表为准，本文件不持硬编码副本** (副本与本体必然漂移)。
- **Layer 2** `detailed-tasks.yaml` —— 由 task-planner 在 **A.2** 生成，现已存在。**本文件一律用 Layer 1 编号 (`1.1`/`3.4`) 引用任务，不用 `TASK-{NNN}`** —— 两套编号空间混用会让引用在其中一层悬空。

## Success Criteria

> **born-red 义务**: 每条 SC 必须在实现前基线上为红。纯负向断言须配一条证明「被检查对象存在/非空」的正向锚，并给出一个能让它变红的坏实现样本；否则功能未实现时天然为真 = 恒绿 = 零信息。基线天然为绿的 tripwire 须显式标注角色 (SC-6)。

- [ ] SC-1: `login` 流 GitHub × Google × (D3 新建 / D2 关联既有) 四条路径各 ≥1 条端到端用例通过 (provider mock server)
- [ ] SC-2: **正控先立** —— 合法 state 的 callback 返回 302 且**确实签发会话** (断言 Set-Cookie / session 行存在)，并断言存储记录的 `binding_id` **非空**。在正控通过前提下，**五**种请求返回 **400 或 403** (排除 404) 且均不签发会话，error code **按成因分列**，不得笼统归入 `invalid_state` (那会与 SC-26(b) 直接互斥、同一条件下两条验收不可同时满足): `state` 篡改 → `invalid_state`；`state` 复用已消费 → `invalid_state`；`state` 缺失 → `invalid_state`；binding cookie **缺失** → `binding_cookie_missing`；binding cookie **不符** → `binding_mismatch`
- [ ] SC-3: `email_verified == false` 时 (a) 响应 `403 email_not_verified` — 正向；(b) `identities` 与 `users` 行数均未增 — 负向。两者同成立才通过。另含 D5 (`email is None`) 一条断言 `403 email_unavailable`
- [ ] SC-4: (a) 测试期 OAuth 相关日志行数 ≥ 1 — 证明扫描目标非空；(b) 同批日志正则扫描 `client_secret` / `code_verifier` / `access_token` 字面量，命中即失败。坏实现样本 = 故意打印一次 token，必须让本条变红
- [ ] SC-5: login 流 D1 / D1-inactive / D2 / D2' / D2-inactive / D3 / D4a-pw / D4a-nopw / D4b / D5 / D6 (**11** 条) 与 link 流 L1 / L2 / L3 / L4 / **L-inactive** (**5** 条) 共 **16 条**分支各 ≥1 条带断言用例；D1 用例额外断言 `email_at_link` 已更新，且身份漂移事件**确实被投递到风控/告警队列** (断言消费方收到，不是断言日志被写 —— 无人消费的记录 = 静默)。D1 用例断言该 error 级结构化事件**已被写出且字段完整** (事件类型 / 旧 email / 新 email / identity id) —— **不**断言「消费方收到」: 本期没有消费方，那样的断言只能靠测试自造 stub 来满足，而自造 stub 恒绿正是本文档反复点名的假绿。新增代码**分支**覆盖率 ≥ 85% (D0/L0 的单元用例计入)，OAuth 模块无覆盖率豁免
- [ ] SC-5b: **方向性断言** (覆盖率维度对文案错位天然免疫) —— 直接断言 D4a-pw / D4a-nopw / D4b 三条响应文案两两不同，且: D4b 文案**不含**「登录」类指引词；D4a-nopw 文案**不含**「密码」；D4a-pw 文案含「密码」。坏实现样本 = 把 D4a 与 D4b 文案对调，必须让本条变红
- [ ] SC-6: 邮箱密码登录既有回归用例 100% 通过。**角色**: 非回归 tripwire，基线天然为绿，不作为「新功能已实现」的证据
- [ ] SC-7: `identities` up/down migration 在空库与有数据库两种起点各执行一次并可逆 (down 后 schema diff 为空)；另一条断言删除持有 identity 的 user 后其 identity 按 DEC-1 级联删除
- [ ] SC-8: provider 在 token 交换步骤超时 / 5xx / 网络错误时返回可读错误码，且邮箱密码登录在同一进程内仍可成功登录
- [ ] SC-9: (a) 已过 TTL 但从未被消费的合法 `state` 被拒绝 (mock clock)；(b) 同一 `state` **并发**两次 callback 恰好一次成功，另一次被拒且不产生第二个 session 或第二行 identity。**并发必须用同步屏障/注入延迟强制两个请求同时进入消费逻辑**，不得靠线程调度碰运气 (否则坏实现会偶然通过 = 不稳定的假绿)。坏实现样本 = read-then-delete 非原子实现，必须让 (b) 变红
- [ ] SC-10: (a) **正控先立** —— 有权用户 (已设密码或另有 identity) unlink 自己的 identity 成功，返回 2xx 且该行**确实被删除**；(b) 在正控通过前提下，越权 (他人 identity id) 返回 404 **且响应体 error code 为 `identity_not_found`** —— 单看 404 无法与「路由不存在」区分 (这正是 SC-2 已修的 404 冒充形状，此处是同类推广)；(c) `has_password == false` 且仅剩唯一 identity 时返回 `409 last_login_method` 且该行未被删除
- [ ] SC-11: 两条约束**各自**一条负控 (直接对 DB 断言，不经应用层)，且**各自**配坏实现样本: (a) 同一 `(provider, provider_user_id)` 二次插入到不同 user_id 被拒 —— 坏实现 = 迁移里去掉该 UNIQUE；(b) 同一 `(provider, user_id)` 二次插入被拒 (DEC-2) —— 坏实现 = 迁移里去掉该 UNIQUE。只写 (a) 视为本条未完成
- [ ] SC-12: **正控先立** —— 一条正确 `code_verifier` + 正确 `nonce` 的换 token 必须成功并签发会话，且 mock provider **确实校验** `code_verifier` (用错值调 mock 必须由 mock 侧拒绝，证明这不是被端点绕过的空校验)。在此前提下 **5 条**负控，逐条编号交付:
      (12-1) `code_verifier` 缺失 → 失败;
      (12-2) `code_verifier` 错值 → 失败;
      (12-3) `code_challenge_method` 降级为 `plain` → 失败;
      (12-4) Google `id_token` 的 `nonce` 与存储值不符 → 拒绝签发;
      (12-5) Google `id_token is None` → 抛 `id_token_missing` 而非放行
- [ ] SC-13: **正控先立** —— 合法 `next=/dashboard` 登录后确实跳到 `/dashboard` (证明 next 机制存在且生效)。在此前提下负控 ≥ 4 条，全部断言跳转目标为默认首页。其中 ≥2 条 payload 的**选取权不得落在 3.6 的实现者手上**:
      **唯一路径**: 由不参与 `3.6` 的一方 (qa-engineer 席) 在 Phase B 开工前，把选定的 ≥2 条 payload 封存写入 `tests/security/redirect_payloads/`，对实现者不可见；PR 评审只核对该路径下测试文件已存在且非空。
      > 「引自 OWASP WSTG-CLNT-04」这条备选路径**已被删除**: WSTG-CLNT-04 是一个叙述性测试用例编号，不是逐条编号的 payload 清单，不存在可引用的条目号 —— 保留它等于让实现者给任意自选 payload 贴一个查不了的外部标签，把刚堵上的「自报」漏洞以「引用权威」的名义重新打开。若将来要恢复外部语料分支，必须指向**真正逐条可寻址**的公开语料 (具体条目 ID 可被第三方独立取回核对)。
      > 两次修订的教训: 「文档逐字列举样例」会把「未列举」的合格集清空 (条件不可满足)；「由实现者自报所选样例」则是 author-to-match-checker 的镜像 —— 检查内容由被检者事后挑选，第三方无法复核。两条都不行，判据必须落在**独立于实现者的外部基线**上。
- [ ] SC-14: 前端 —— (a) **正向锚**: 账户设置页对有多个 identity 的用户确实渲染出身份列表与可点解绑动作；在此前提下，对「唯一 identity 且 `has_password == false`」的用户不渲染可点解绑动作；(b) e2e 覆盖两个 provider 的登录入口点击后跳到本站 start 端点 (而非前端直接拼 provider URL)
- [ ] SC-15: (a) **正向锚**: 决策矩阵/端点模块文件存在且对 `NormalizedIdentity` 的消费点 ≥ 1 (证明扫描目标非空)；(b) 该范围内**语义等价的 provider 分支**零命中，判据**只能是 AST 级** —— 「穷举等价形态清单」这一支已被删除: 清单与被检代码由同一人按同一张表写，同义写法 (枚举恒等比较、字典/注册表分派、前缀匹配、双分派) 天然全绿，是 author-to-match-checker 的又一形态；(c) 坏实现样本 ≥ 2 个，且两个都必须是**本条 (b) 未点名的分派写法**。不计入名额的写法: ①「字面 `provider == 'github'` 比较」—— 它是被检基线形态本身；②「装饰器注册的策略对象」—— 装饰器只是把条目写进注册表的另一种语法，仍属 (b) 已点名的「字典/注册表分派」。合格例: 基于类型的多态方法重写、反射式属性查找、三元表达式链
- [ ] SC-16: 文档同步 (Rule #3) —— (a) OpenAPI 含全部三端点且通过 schema 校验；(b) 架构文档必须用**围栏代码块**给出规范化 route 列表 (机械可抽取，不从中文散文里猜)，比对前先各自断言「抽取到的 route 数 == 3」——两侧皆空时空集比空集会假绿；在此前提下两侧逐字一致，不一致即红；(c) 运维文档写明凭据存放与轮换步骤且不含任何真实 secret
- [ ] SC-17: link 流会话不变量 —— (a) L1/L2/L3/L4 四条用例**各自**断言操作前后会话主体 user_id 未变；L2 额外断言返回 `409 identity_taken` 且未新增 identity 行；(b) **主体更替负控**: start 后登出、以另一用户身份登录、再 callback，必须返回 `403 session_subject_changed` 且不建 identity (binding cookie 判别不了这种更替，只有 `link_user_id == 当前会话 user_id` 的断言能抓)。坏实现样本 = ①link 流复用 login 矩阵 (让 L2 变红) ②callback 侧改用当前会话主体而非 `link_user_id` (让 (b) 变红)
- [ ] SC-18: start 请求中携带 `redirect_uri=https://evil.example` 时，302 目标中的 `redirect_uri` 仍为服务端注册常量 (参数被忽略)
- [ ] SC-19: 三端点各 1 条用例，超过限流阈值后返回 `429` **且**响应体 `error_code == "rate_limited"`、**且**含可机读的触发维度字段 (IP or binding)。只断言裸状态码不算通过 —— 「响应体给出被触发的维度」是技术方案段的明文承诺，无断言即无覆盖
- [ ] SC-20a: 直接调用 resolver 传入构造的非法组合 → `403 unresolved_identity_state` 且产生 error 级告警记录。坏实现样本 = 缺省分支写成「按 D3 建号」或静默 `pass`，必须让本条变红。**执笔任务唯一为 tasks 5.16** (5.13 不得重复实现同一用例，只可复用)
- [ ] SC-20b: `NormalizedIdentity` 不变量 `email is None ⇒ email_verified == False` 在**适配器层**被断言，两个适配器各 1 条 (执笔任务 tasks 2.2 / 2.3 的验收项，不在 link 流范围内)
- [ ] SC-21: 未知 `{provider}` (如 `/auth/oauth/facebook/start`) 在三端点上均返回 `404` 且响应体 error code 为 `unknown_provider`，非 500、非回落默认 provider
- [ ] SC-22: DEC-2 应用层竞态 —— 并发触发两个 D2 (同一 user、同一 provider、不同 provider_user_id) 时，一个成功、另一个返回 `409 provider_already_linked`，**不得**是未捕获唯一约束冲突导致的 500。同 SC-9(b) 用同步屏障强制竞态窗口
- [ ] SC-23: GitHub 邮箱回退禁令 —— mock 一个「primary 未验证、另有非 primary 且 verified」的账户，断言 `NormalizedIdentity.email is None` 且 `email_verified == False` (即**未**回退取用那条非 primary 邮箱)。坏实现样本 = 适配器改为取任一 verified 邮箱，必须让本条变红
- [ ] SC-24: D6 歧义匹配 fail-closed —— 构造同一 email 匹配到 2 个既有 user 的数据 (可达性取决于锚点 A-5)，断言返回 `403 ambiguous_email_match`、产生 error 级告警、且**未**登录任何一个候选用户。坏实现样本 = 取匹配结果的第一条登录，必须让本条变红
- [ ] SC-25: 账户状态旁路 —— 目标 user 为非 active (停用/锁定/软删除) 时，D1-inactive / D2-inactive / **L-inactive** 三条路径均拒绝，且返回的错误语义与既有邮箱密码登录路径**同一套** (对照锚点 A-6 给出的既有校验位置逐字比对)。坏实现样本 = 社交登录不查状态直接签发，必须让本条变红
- [ ] SC-26: binding cookie 契约 —— (a) **多标签并发**: 同一浏览器并发发起 GitHub 与 Google 两个流，两个 callback **都**成功 (固定名 cookie 的坏实现会让先发起的那个变红)；(b) **缺失态可自解释**: 禁用 cookie 的客户端得到 `403 binding_cookie_missing` 而非 `binding_mismatch`/`invalid_state`，前端渲染「请启用 cookie」提示；(c) **SameSite 前提实测**: 用真实浏览器 e2e 确认 provider 的 302 顶层导航确实携带该 cookie —— 这是整条链成立的前提，不得靠推断
- [ ] SC-27: `flow` 取值域与相容性 (start 端点，先于矩阵) —— (a) **正控**: `flow=login` 无会话、`flow=link` 有会话两条正常路径均 302 到 provider；(b) `flow` 缺失 / `flow=bogus` → `400 invalid_flow` (2 条)；(c) `flow=login` 且已有会话 → `409 already_authenticated`，且**会话主体未变**；(d) `flow=link` 且无会话 → `401 login_required`，且**不产生短时存储记录**。坏实现样本 = start 不校验 flow 与会话相容性 (缺失时默认 login)，必须让 (b)(c)(d) 变红

## References

- RFC 6749 (OAuth 2.0) / RFC 7636 (PKCE) / OpenID Connect Core 1.0
- OAuth 2.0 Security Best Current Practice (draft-ietf-oauth-security-topics)
- GitHub: Authorizing OAuth apps / Google: OpenID Connect

## 审计留痕

post_spec 审计 (audit-engine, convergence mode, 5 席) 跑满配置上限 **5 轮**，逐轮吸收共 5 簇 Critical 与数十条 Major，**未达成收敛** (相邻两轮结论集合始终不同)；触及 `max_rounds=5` 而终止，非「已通过」。第 5 轮仍存的阻塞项与需 owner 裁决项随本 Spec 一并上呈，Spec 因此停在 `Draft`。

> 逐轮完整记录**刻意不放在本变更目录内** —— Level 3 产物只有 proposal.md + tasks.md + detailed-tasks.yaml，审计叙事是 append-only 的另一类东西，与收敛型交付面同居会互相污染。真实运行时它应落 `.aria/audit-reports/`；本次交付受沙箱限制暂存于 `outputs/_audit-trail-NOT-a-change-artifact/`，该文件不是本 change 的产物。
