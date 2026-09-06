# Audit Trail — add-oauth2-social-login

> **append-only**。与 `proposal.md`（收敛型交付面）分居两文：append-only 叙事和会被反复重写的规格同居一文会造成耦合。
> 本文件**不参与**规格判定；proposal.md 才是唯一 SOT。

## post_spec R1 (2026-09-05, convergence, team = tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager)

计数（口径见文末「计数口径」节）：**条目口径 28 (8C/16M/4m) · 簇口径 25 (7C/14M/4m)**。

| 簇 | 严重度 | 席位 | 处置 |
|---|---|---|---|
| C1 nonce 无生成/存储通道 | CRITICAL ×2 | backend-architect / code-reviewer | §A 接口加 `nonce`、§C 同批存储、§E.2 建表、SC-15 |
| C2 email 匹配语义未定 | CRITICAL ×2 | backend-architect / code-reviewer | §D.1 钉字符级 + ≥2 命中拒绝、SC-12 / SC-17 |
| C3 分支 3 无代码宿主 | CRITICAL ×2 | tech-lead / code-reviewer | 新增 §G + §E.3、SC-13 / SC-16 |
| C4 SC-4 指标测不出目标缺陷 | CRITICAL | qa-engineer | SC-4 换量（identity 行 + 会话 + error_code） |
| C5 SC-5/SC-7 矛盾 + 无事务语义 | CRITICAL | code-reviewer | §D.2；SC-7 改"两次独立授权" |
| C6 tasks.md 缺失 | CRITICAL | knowledge-manager | **判定非本检查点缺陷**：tasks.md 是 A.2 产物，post_spec 在 A.2 之前 |
| M1 state/PKCE 存储介质未定 | MAJOR | tech-lead | §E.2 |
| M2 绑定不可逆无出口 | MAJOR | tech-lead | §H `unlink-identity` + Impact 新增 Risk 行 |
| M3 SC-8/SC-11 依赖无人认领的 CI 改动 | MAJOR | tech-lead | §H CI 节 |
| M4 无"GitHub 无邮箱新用户"SC | MAJOR | tech-lead | SC-16 |
| M5 SC-6 的输入不存在 | MAJOR ×2 | qa-engineer / code-reviewer | §C `redirect_uri` 为常量 + `next` 白名单；SC-6 改写 |
| M6 PKCE 零覆盖 | MAJOR | qa-engineer | SC-14 |
| M7 state 跨会话重放未覆盖 | MAJOR | qa-engineer | SC-5b |
| M8 SC-8 抽样不穷尽 | MAJOR | qa-engineer | 改静态扫描 |
| M9 接口混淆 access_token/id_token、缺 redirect_uri | MAJOR | backend-architect | §A `TokenResponse` |
| M10 关联 cookie SameSite 未定 | MAJOR | backend-architect | §C `SameSite=Lax` |
| M11 GitHub 邮箱选取欠定 | MAJOR | code-reviewer | §B 判定表 + SC-4 点名 Google |
| M15 缺模板要求的 `## Tasks` 节 | MAJOR | knowledge-manager | 补节指向 tasks.md |
| M16 默认值隐性生效无留痕 | MAJOR | knowledge-manager | 「决策留痕」表 + 不适用"无回应即批准" |
| M12 SC-10 "可读"主观 / M13 §D 未写短路 / M14 Q3 非阻塞 / M17 内联工时 | MINOR ×4 | qa / backend-architect / tech-lead / knowledge-manager | 全部吸收 |

## post_spec R2 (2026-09-05, 同一 team, 对象 = R1 修订版)

计数：**条目口径 27 (7C/17M/3m) · 簇口径 20 (5C/12M/3m)**；标注 `NEW_IN_R1_FIX` 的占 **26/27 = 96%** —— 绝大多数是 R1 修复轮自己造出来的。

| 簇 | 严重度 | 席位 | 来源 | 处置 |
|---|---|---|---|---|
| R2-C1 §D if-elif 链把"≥2 命中"漏进新建分支，与 §D.1 / SC-17 相反 | CRITICAL ×2 | tech-lead / code-reviewer | NEW_IN_R1_FIX | §D 改 6 行判定表，≥2 命中单列分支 4 |
| R2-C2 §D.2"先插 identities"与 `user_id` NOT NULL FK 冲突，且其理由本身站不住 | CRITICAL ×3 | tech-lead / backend-architect / code-reviewer | NEW_IN_R1_FIX | 改"先插 users 再插 identities"，防孤儿靠事务原子性 |
| R2-C3 nonce 只补了生成侧、`fetch_identity` 拿不到期望值 ⇒ SC-15 结构上不可实现（C1 形状在自己的修复里复发） | CRITICAL | tech-lead | NEW_IN_R1_FIX | `fetch_identity(token_response, expected_nonce)` + SC-15b fail-closed |
| R2-C4 §G"已定稿"字样与决策留痕表"待批准"两套真值 | CRITICAL | knowledge-manager | NEW_IN_R1_FIX | 全文改"拟定值"，状态只由留痕表给 |
| R2-C5 SC-13"伪造 email_verified 载荷"无真实输入通道 ⇒ 恒绿 | CRITICAL | qa-engineer | NEW_IN_R1_FIX | 拆 SC-13a（篡改 key）/ SC-13b（密码错误） |
| R2-M1 §G lane 定义与 §D 分支 3 / SC-4 三方矛盾，且"未验证 email + 零匹配"是死路 | MAJOR ×2 | tech-lead / code-reviewer | NEW_IN_R1_FIX | §G 改三 lane 正交矩阵，VERIFY lane 覆盖零匹配 |
| R2-M2 error_code 枚举漏 §G 失败分支 ⇒ 自己新写的章节 fail-open | MAJOR | tech-lead | NEW_IN_R1_FIX | 枚举补两码 + fail-closed 声明 |
| R2-M3 `session_binding` 无产生者/比对规则；SC-5b 测的是缺参不是绑定 | MAJOR ×2 | tech-lead / backend-architect | NEW_IN_R1_FIX | §C 定义 HMAC + 查找键钉为 `txn_key`；SC-5b 两变体 + SC-20 |
| R2-M4 §B 判定表对"无 primary 但有 verified"不穷尽 + 未禁 `/user.email` 回落 | MAJOR | code-reviewer | NEW_IN_R1_FIX | §B 表补第 3 行 + 显式禁用 |
| R2-M5 唯一约束与 §D.1 归一化不同源 ⇒ SC-17 不可构造 / 误判 ≥2 | MAJOR ×3 | backend-architect / code-reviewer / qa-engineer | NEW_IN_R1_FIX | 唯一索引建在 `lower(trim(email))` + 迁移去重前置 (SC-9b)；SC-17 改 mock 构造 |
| R2-M6 SC-14 输入不存在（code_verifier 不随 callback 往返） | MAJOR ×2 | code-reviewer / qa-engineer | NEW_IN_R1_FIX | 拆 SC-14a 白盒本地拒绝 / SC-14b provider 侧 `invalid_grant` |
| R2-M7 两张短 TTL 表无清理机制、`expires_at` 无索引 | MAJOR | backend-architect | NEW_IN_R1_FIX | §H 定时清理 + lazy delete；§E.2/E.3 建索引 |
| R2-M8 §G 建号路径未重申 §D.2 事务语义 ⇒ 并发竞态复现 | MAJOR | backend-architect | NEW_IN_R1_FIX | §D.2 末句 + SC-19 |
| R2-M9 §H `unlink-identity` 是 Risk 唯一缓解却无 SC | MAJOR | qa-engineer | NEW_IN_R1_FIX | SC-18（含"最后一条 identity"边界） |
| R2-M10 决策留痕预写 `TASK-008` 硬 ID，A.2 编号不同即静默失效 | MAJOR | knowledge-manager | NEW_IN_R1_FIX | 改功能锚点，ID 待 A.2 回填 |
| R2-Minor 分支 3 两码未一一对应 / Q3 删除理由挂错引用 / C6 行全角括号 | MINOR ×3 | backend-architect / knowledge-manager | 混合 | 全部吸收（§D 判定表逐行给码；Out of scope 补显式条目；本文件重排） |

**R2 的元观察**：缺陷绝大多数由 R1 的修复轮引入而非母版遗留（96%）。

---

## post_spec R3 (2026-09-05, 同一 team, 对象 = R2 修订版, 镜头 = 实现者试派生)

计数：**条目口径 21 (9C/10M/2m) · 簇口径 17 (7C/8M/2m)**；`NEW_IN_R2_FIX` 占 **16/21 = 76%**。
⚠️ **可比性告示**：R3 每席 findings 上限从 6 降到 5，故 R3 的绝对计数偏低，与 R1/R2 不严格可比。

| 簇 | 严重度 | 席位 | 来源 | 处置 |
|---|---|---|---|---|
| §D.2 只捕获 identity 唯一冲突，翻转插入顺序后先撞的是 users 邮箱唯一约束 ⇒ 无恢复路径、SC-7 无实现能满足 | CRITICAL | tech-lead | NEW | §D.2 两类冲突各给恢复动作；lane EMAIL 补填后重入 §D 判定表；SC-30 |
| SC-14a 无代码宿主：§E.2 不存 `code_challenge`、§C 五步里没有 PKCE 本地校验 | CRITICAL | tech-lead / qa-engineer | NEW | §E.2 增列 `code_challenge`；§C 增步 5 本地预检；SC-14a 点名宿主 |
| §G lane 与 §D 判定顺序错位 ⇒ "≥2 命中"被分支 3 截走进 VERIFY（R2-C1 形状原样复发） | CRITICAL | tech-lead / qa-engineer / code-reviewer | NEW | §D 判定表重排为 7 行，"≥2 命中"提为第 3 行且与 `email_verified` 无关；MANUAL lane 不下发 `pending_key` |
| 匿名会话 cookie 属性未定 + 无会话轮换 ⇒ Strict 时全量 callback 失败 / session fixation | CRITICAL | backend-architect / code-reviewer | NEW | §C 步 3 + §F 统一 `__Host-`+`HttpOnly`+`Secure`+`SameSite=Lax`；§C 步 8 轮换；SC-27 / SC-29 |
| 分支 5 只校验 provider 侧 verified，不问本地 `users.email_verified`（该列还不存在）⇒ 存量未验证账号是一键接管入口 | CRITICAL | code-reviewer | PRE | §D 表拆第 5/6 行 + §E.1 补列与回填口径；SC-28 |
| fail-closed 兜底声明零验收 | CRITICAL | qa-engineer | NEW | SC-21 |
| `oauth_transactions.provider` 有产生者无消费者 ⇒ provider mix-up | MAJOR | tech-lead / code-reviewer | NEW | §C 步 1/4 查找条件带 `provider`；§A 双向 fail-closed；SC-26 |
| `pending_key` 载体/绑定未定，可落进 URL | MAJOR | tech-lead | PRE | §E.3 同款 cookie + `session_binding` 列；SC-23 |
| `lower(trim(email))` 函数索引方言依赖 + 与 ASCII 归一化不同源 | MAJOR | backend-architect | NEW | 改 `email_normalized` 冗余列 + 普通唯一索引 |
| 条件更新隐含 READ COMMITTED 假设 | MAJOR | backend-architect | PRE | §D.2 写明隔离级别假设与更高级别的捕获义务 |
| `pending_key` 消费与建号是否同事务未定 | MAJOR | backend-architect | NEW | §D.2 末条 |
| lane VERIFY / MANUAL 的 pending 行在 SC-4 / SC-17 无断言（生产端覆盖不对称） | MAJOR | qa-engineer | NEW | SC-4(d) / SC-17 补 lane 断言 |
| §H 清理任务零验收 | MAJOR | qa-engineer | NEW | SC-24 |
| 用户在提供方取消 (`access_denied`) 无枚举码 ⇒ 撞 fail-closed 变 500 告警风暴 | MAJOR | code-reviewer | NEW | 枚举补 `oauth_user_denied`；§C 步 0；SC-25 |
| §E.3 一次性消费未给显式 SQL | MINOR | backend-architect | PRE | §E.3 补同形态 SQL |
| 本文件计数口径不自洽（而该计数正是"是否收敛"判定的直接依据） | MINOR | knowledge-manager | PRE | 本节起全部计数由脚本按两种口径机械重算，见下 |

---

## 计数口径 (2026-09-05 由 knowledge-manager R3 的 MINOR 触发, 机械重算)

- **条目口径** = 各席位输出的 findings 逐条求和（同一问题被 N 个席位提出记 N 条）
- **簇口径** = 跨席位按问题去重，簇严重度取各席位给出的**最高**值
- 两种口径都由脚本从各席位原始输出逐条录入后计算，不手写

| 轮次 | 条目口径 (C/M/m) | 簇口径 (C/M/m) | 上一轮修复引入占比 | 每席上限 |
|---|---|---|---|---|
| R1 | 28 (8/16/4) | 25 (7/14/4) | — | 6 |
| R2 | 27 (7/17/3) | 20 (5/12/3) | 26/27 = 96% | 6 |
| R3 | 21 (9/10/2) | 17 (7/8/2) | 16/21 = 76% | **5**（口径变化，绝对值与 R1/R2 不严格可比） |

**两条判据给出相反结论，如实并列**：
1. 「MAJOR 是否还在降」⇒ 簇口径 MAJOR **14 → 12 → 8**，仍在降 ⇒ **继续加轮有产出**
2. 「本轮发现里由上一轮修复引入的占比 > 1/2 即到边际拐点」⇒ 96% / 76%，两轮都 > 1/2 ⇒ **已过拐点，应换执笔席而非继续刷轮次**

CRITICAL 簇数 7 → 5 → 7 基本持平，且每轮落点都在**新章节**上（R2 落在 R1 新写的 §D.2/§G，R3 落在 R2 新写的 §C 五步/§E.2/§E.3）。这个形状本身就是结论：**规格面每轮都在长大，新表面带来新缺陷**。
