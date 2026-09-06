# Tasks: OAuth2 Social Login (GitHub + Google)

> **Spec**: changes/oauth2-social-login/proposal.md
> **Level**: Full (Level 3)
> **Status**: Draft
> **Created**: 2026-09-05
> **Estimated**: 111-176h

---

## 1. 基础设施与数据模型

- [ ] 1.1 新增 `identities` 表与可逆迁移 (up/down, 含 DEC-1 级联)
- [ ] 1.2 provider 凭据与回调 URL 的配置装载层
- [ ] 1.3 共享短时存储 (state/nonce/code_verifier/binding_id/flow 同记录, TTL + 原子一次性消费)
- [ ] 1.4 **零号任务**: 解析并填实 proposal「现状锚点」**A-1~A-6** (users 表 / 会话签发模块 / 既有登录回归集 / 密码列可空性与 has_password 判定 / **users.email 唯一性与匹配规范化规则** / **账户状态字段及其在既有登录路径的校验位置**)

## 2. Provider 抽象与适配器

- [ ] 2.1 定义 `OAuthProvider` 接口 + `ProviderTokens` + `NormalizedIdentity` 契约
- [ ] 2.2 Google 适配器 (OIDC discovery + JWKS 验签 + nonce; id_token 缺失 fail-closed)
- [ ] 2.3 GitHub 适配器 (可信主邮箱筛选 + 「无可信邮箱」路径 + 非 primary 回退禁令)
- [ ] 2.4 Provider 注册表: 未知 provider 404、provider 故障降级

## 3. 端点与会话集成

- [ ] 3.1 `GET /auth/oauth/{provider}/start` (**flow 取值域与会话相容性校验** + PKCE challenge + **按 state 命名空间化的** pre-auth binding cookie)
- [ ] 3.2 `GET /auth/oauth/{provider}/callback` (binding/state 校验 → 换 token → fetch_identity)
- [ ] 3.3 决策矩阵实现 (login 11 分支 + link 5 分支 + D0/L0 fail-closed)
- [ ] 3.4 会话签发衔接既有 session/JWT 签发器
- [ ] 3.5 `POST /auth/identities/{id}/unlink` (越权防护 + 最后登录方式保护)
- [ ] 3.6 `redirect_uri` 固定化 (忽略请求参数覆盖) 与 `next` 同源白名单
- [ ] 3.7 三端点限流接入 (IP + binding 维度, 超限 429)

## 4. 前端接入

- [ ] 4.1 登录页社交登录入口与 provider 按钮
- [ ] 4.2 账户设置页身份管理 (查看 / 关联 link 流 / 解绑, 含不可解绑态)
- [ ] 4.3 callback 失败与拒绝授权的错误呈现与降级回邮箱登录

## 5. 安全与测试

- [ ] 5.1 state / binding 负控套件 (含「正控先立」的会话签发正控)
- [ ] 5.2 账户接管防线 (D4a-pw / D4a-nopw / D4b / D5 不自动关联)
- [ ] 5.3 login 流端到端集成测试 (provider mock server, 四路径)
- [ ] 5.4 敏感值日志泄漏扫描 (含「扫描目标非空」正向锚)
- [ ] 5.5 既有邮箱密码登录回归验证
- [ ] 5.6 PKCE 与 nonce 负控 (含 mock 侧确实校验 verifier 的正控)
- [ ] 5.7 `next` 白名单与 `redirect_uri` 覆盖负控 (含未逐字列举的绕过形态)
- [ ] 5.8 数据库层唯一约束负控 (直接对 DB 断言, 不经应用层)
- [ ] 5.9 前端验收 (可解绑态正向锚 + 不可解绑态 + 登录入口 e2e)
- [ ] 5.10 迁移可逆性与 DEC-1 级联验收
- [ ] 5.11 短时存储 TTL 与并发原子消费验收 (同步屏障强制竞态窗口)
- [ ] 5.12 unlink 验收 (成功正控 + 越权 error code + last_login_method 保护)
- [ ] 5.13 link 流会话不变量 (L1-L4) 与 DEC-2 应用层竞态映射为 409
- [ ] 5.14 provider 无关性检查器 (AST/等价写法级) + D4a/D4b 文案方向性断言
- [ ] 5.15 端点鲁棒性验收 (provider 超时/5xx 降级、限流 429、未知 provider 404)
- [ ] 5.16 决策 resolver 单元负控 (D0/L0 非法组合、D6 歧义匹配、账户状态旁路含 L-inactive)
- [ ] 5.17 binding cookie 契约验收 (多标签并发、缺失态可自解释、SameSite 前提实测)
- [ ] 5.18 `flow` 取值域与会话相容性验收 (invalid_flow / already_authenticated / login_required)

## 6. 文档与发布

- [ ] 6.1 API 文档与 OpenAPI 片段更新
- [ ] 6.2 架构文档 (围栏代码块给规范化 route 列表) 与 provider 凭据运维说明
- [ ] 6.3 文档同步机械核验脚本 (抽取数断言 + 端点名逐字比对)

---

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 1. 基础设施与数据模型 | 4 | 12-20h |
| 2. Provider 抽象与适配器 | 4 | 15-24h |
| 3. 端点与会话集成 | 7 | 25-39h |
| 4. 前端接入 | 3 | 7-12h |
| 5. 安全与测试 | 18 | 46-70h |
| 6. 文档与发布 | 3 | 6-11h |
| **Total** | **39** | **111-176h** |

> 派生数字核对 (每次追加任务后必做)：条目计数 4+4+7+3+18+3 = 39 ✅；估时 min 12+15+25+7+46+6 = 111 ✅，max 20+24+39+12+70+11 = 176 ✅。

---

## SC ↔ 任务映射 (每条 SC 必须有执笔任务)

| SC | 承载任务 | SC | 承载任务 |
|----|---------|----|---------|
| SC-1 | 5.3 | SC-13 | 5.7 |
| SC-2 | 5.1 | SC-14 | 5.9 |
| SC-3 | 5.2 | SC-15 | 5.14 |
| SC-4 | 5.4 | SC-16 | 6.3 |
| SC-5 | 5.3 (D1/D2/D2'/D3) + 5.2 (D4a-pw/D4a-nopw/D4b/D5) + 5.16 (D1-inactive/D2-inactive/D6) + 5.13 (L1-L4) | SC-17 | 5.13 |
| SC-5b | 5.14 | | |
| SC-6 | 5.5 | SC-18 | 5.7 |
| SC-7 | 5.10 | SC-19 | 5.15 |
| SC-8 | 5.15 | SC-20a | 5.16 |
| SC-9 | 5.11 | SC-21 | 5.15 |
| SC-10 | 5.12 | SC-22 | 5.13 |
| SC-11 | 5.8 | SC-23 | 5.2 |
| SC-12 | 5.6 | SC-20b | 2.2 + 2.3 (适配器验收项) |
| SC-24 | 5.16 | SC-25 | 5.16 |
| SC-26 | 5.17 | SC-27 | 5.18 |

---

## Dependencies

```
1.4 (零号) ──▶ 1.1 / 1.2 / 1.3 ──▶ Phase 2 ──▶ Phase 3 ──┬──▶ Phase 4 ──┐
                                                          │              ├──▶ Phase 6
                                                          └──▶ 5.3 5.4 5.5 5.9 5.10 ──┘
```

- `1.4` 是全局零号前置: **A-1~A-6** 未填实则 1.1 / 3.3 / 3.4 / 3.5 / 5.5 / 5.16 均无可核验对象。按 proposal「现状锚点」**门槛 1**，它**可以且必须在 Draft 态执行，不受门槛 2 (不得 Approved) 与门槛 3 (Phase B 不得开工) 约束** —— 否则闸门阻断了解除自己的唯一路径。
- **Phase 5 的负控任务不受本图时序约束**: 5.1 / 5.2 / 5.6 / 5.7 / 5.8 / 5.11 / 5.12 / 5.13 / 5.14 / 5.15 / 5.16 / 5.17 / 5.18 (共 **13** 项) 必须**先于**其对应实现任务落地并确认为红 (born-red)，图中把 Phase 5 画在 Phase 3 之后只表示归类，按图串行执行会使 born-red 义务结构上不可满足。成对关系 (13 对): 5.1↔3.2、5.2↔3.3、5.6↔2.2/3.2、5.7↔3.6、5.8↔1.1、5.11↔1.3、5.12↔3.5、5.13↔3.3、5.14↔3.3、5.15↔2.4/3.7、5.16↔3.3、5.17↔3.1、5.18↔3.1。
- **5.4 / 5.5 不是 born-red，是 tripwire** —— 它们出现在上面图的分支里 (实现之后执行)，**不**出现在下面的 born-red 名单里。⚠️ 这两处必须成对维护: 5.4 已经被「加新项时挤出名单」两次，加任何新的 Phase 5 任务时都要回头确认 5.4 仍在图分支列中。角色说明: 5.5 的既有回归集基线天然为绿 (SC-6 已声明)；5.4 的正向锚是「测试期 OAuth 相关日志行数 ≥ 1」，实现不存在时它必红，但红的原因是「扫描目标为空」—— 恰是它自己被设计来排除的那个假信号，所以对它要求 born-red 结构上不可满足。两者都在其被测实现落地**之后**立即执行。

---

## Notes

1. **Numbering Immutability**: 编号一经建立不得变更；新增用新号 (本 Spec 迄今追加过 1.4 / 3.6 / 3.7 / 5.6-5.18 / 6.3，均为追加，未重排既有编号)，取消用 ~~删除线~~ 标记，不删除。
2. **Task Granularity**: 按 `standards/core/ten-step-cycle/phase-a-spec-planning.md` 的 complexity 标度 —— S (1-2h) / M (2-4h) / L (4-8h) / XL (8h+)，逐项估时见 `detailed-tasks.yaml`。detailed-tasks.yaml 已由 A.2 生成，本表分项与其逐项区间之和逐格核对一致；后续任何一侧改动都必须双向重算。**不是每项都 4-8h** (4-8h 是 L 级的区间，非全体任务的粒度断言)；Total 是逐项区间之和，不是「项数 × 4-8h」。
3. **追加任务时的同步义务**: 每次追加必须同时重算 Summary 分项与 Total，并检查 proposal 是否有硬编码副本 (proposal 已改为「以本表为准」不再持有副本，副本与本体必然漂移)。
4. **born-red 义务**: 每条负控任务的验收都必须先在基线跑一次并确认为红，并附一个能让它变红的坏实现样本；基线即绿的用例视为零信息，须换判据重写。
