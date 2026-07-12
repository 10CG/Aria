# DEC-20260712-002 — 撤销 task-level docker auth 禁令 (推翻 DEC-20260523-001)

> **状态**: **Decided** (2026-07-12) — owner 采纳判别式实测证据, 禁令撤销, SOT 反转。
> **创建**: 2026-07-12
> **触发**: Aether [#234](https://forgejo.10cg.pub/10CG/Aether/issues/234) prong b 跨仓迁移撞上本禁令 —— `aria-layer2-runner` 是集群里最后一个仍靠节点凭据拉私有镜像的 job。
> **决策人**: 10CG Lab owner
> **前置 grounding**: 判别式实测 (同集群、同 Nomad v1.11.2 未升级、复刻本 job 自身形态)
> **关联**: [Aria #161](https://forgejo.10cg.pub/10CG/Aria/issues/161) · aria-standards #14 · aria-orchestrator #32 · Aria #162
> **Supersedes**: DEC-20260523-001 (记录保留作历史, **结论作废**)

> ⚠️ **编号说明**: 本决策最初被引用为 `DEC-20260712-001`, 与并发 session 的 state-scanner parity 决策**撞车**, 且**未创建决策文件** (dangling ref) —— 由并发 session 于 Aria 主仓 `dfb3118` 发现。现改用 **-002** 并补齐本文件。根因: DEC 编号无 claim 机制。

---

## §1 被推翻的是什么

`DEC-20260523-001` / `standards/conventions/nomad-docker-registry-auth.md` v1.0.0 **禁止** task-level `config.auth` + `template{env=true}` 组合, 并把**节点级 `plugin "docker" { auth { config = ... } }` 定为 SOT**, 在 HCL 里明文写下 **"DO NOT re-add task-level auth block"**。

其依据是一个**时序断言**:

> docker driver image pull 发生在 template render **之前** → `${VAR}` 在 pull 时仍是 unresolved literal 或空 → registry 收到空 password → 401

## §2 推翻依据 (判别式实测, 2026-07-12)

节点凭据当时**完全健康**, 所以"能拉到镜像"**不构成证据** (可能是 job auth 生效, 也可能是 driver 回退用了节点凭据, 观感完全一样)。必须给 job 级凭据注入**错误值**, 要求**硬失败**:

| 实验 (Nomad **v1.11.2**, 与 v1.0.0 失败时**同版本、未升级**; `force_pull = true` 强制冷拉) | 正确凭据 | **故意写错**的凭据 |
|---|---|---|
| 普通 batch + 静态 tag | ✅ `Downloading image` → Exit 0 | ❌ `401 Unauthorized` |
| **parameterized (dispatch) + `image = repo@sha256:${NOMAD_META_IMAGE_SHA}`** ← **本 job 自身形态** | ✅ `Downloading image` → Exit 0 | ❌ `401 Unauthorized` |

**两行合起来闭合**:

- 错误凭据 → 401 ⇒ docker driver **确实在消费 auth block**, 且其失败时**不回退**节点 `config.json`。
- 正确凭据 → 成功 ⇒ 既无回退路径, 成功**只可能**来自 auth block 里**已正确 resolve 的模板值** ⇒ **template env 在 image pull 时已经就位**。

⇒ v1.0.0 §2 的生命周期图**是错的**: template 是 **prestart hook**, 早于 `driver.StartTask`。

## §3 2026-05-23 那次 401 的真因

**未知, 且不编。** 但有一个不需要新假设的解释: 彼时用的 `FORGEJO_BOT_PAT` 属于 `ca32267` 那代 token —— 后 (2026-07-01) 被查明**泄露 + 过度授权**并已 revoke; 且 `AD-M1-8` 同期记录 "partial 4-scope **FAIL** → full 7-scope **PASS**"。**scope 不足/无效的 token 同样 401**, 而当年归因为"插值时序"时**没有做判别式实验** (未验证渲染出的值是否为空)。

v1.0.0 自己写过 "本 convention 不假装能解释根因" —— 这份诚实是对的, 但"取严格立场"的代价是把 job 锁死在了单点凭据上。

## §4 为什么必须反转 (不只是"解禁")

节点级 `/root/.docker/config.json` 是**无 IaC、无模板、纯手工维护的单点凭据文件**。

**2026-07-08 它在 heavy-3 上被清空** (Aether #234 字节级取证: 16B = `docker logout` 对空 auths 的序列化), 依赖它的 job 集体 401、alloc 卡 pending 反复退避。同族漂移已复发多次 (Aether #200 / #225 / #232 / #234)。

另: v1.0.0 自称适用**全 Lab**, 且其 §7/§8 教人"**删除** task-level auth block" —— 而集群内 Aether / SilkNode / Kairos / Kino / shenquant / nexus / todo-web 等 **21 个 task 一直在用该模式且工作正常**。真按 v1.0.0 全 Lab 执行 = 把能用的 auth 删掉、集体退回单点。

## §5 决定

1. **禁令撤销**。SOT **反转**为: task-level `config.auth` + `template{env=true}` 从 Nomad Variable 注入 (Aether #46 pattern)。
2. **节点级 `auth.config` 降级为 fallback** —— 仅**宿主 build** (docker CLI 直跑, 不经 Nomad task config) 与未迁移 job 仍需; 其 schema / base64 `-w0` / 多节点 atomic sync + fingerprint verify 轮换流程**保留**。
3. `aria-layer2-runner` **迁 job 级 auth**, 用 `docker_auth_*` (**read:package**) 而非其 var 里既有的 `FORGEJO_BOT_PAT` (7-scope 写权限 → 给 docker daemon 拉镜像属**过度授权**, least privilege)。
4. `aria-runner-template` (**DEPRECATED**, 0 dispatch) **不迁移**, 仅标注其 auth 结论已作废, 避免继续传播错误归因。
5. **DEC-20260523-001 的记录保留作历史, 结论作废** (加 `REVERSED by` note, 不改写历史)。

## §6 附带实测发现

**Forgejo registry 用 token (password) 认证, 完全忽略 username**: 用当前名 `10cg-ci-bot` / 已改名的旧名 `aria-runner-bot` / 甚至 `WRONG-USER-XYZ` 请求 `/v2/token`, 都能签出 token 并成功 GET manifest (HTTP 200); **只有 token 错误才 401**。

→ 排查 registry 401 **不要在 username 上浪费时间, 直接查 token** (scope / 是否 revoke / 是否 stale)。

## §7 落地

| 仓 | PR | 内容 |
|---|---|---|
| aria-standards | [#14](https://forgejo.10cg.pub/10CG/aria-standards/pulls/14) | `nomad-docker-registry-auth.md` **v2.0.0** |
| aria-orchestrator | [#32](https://forgejo.10cg.pub/10CG/aria-orchestrator/pulls/32) | `aria-layer2-runner` 迁移 + `AD-M1-8` REVERSED note |
| Aria (主仓) | [#162](https://forgejo.10cg.pub/10CG/Aria/pulls/162) | submodule 指针 |
| Aether | [#239](https://forgejo.10cg.pub/10CG/Aether/pulls/239) | `pat-inventory` 登记消费者 |

**集群终态**: **48/48** 拉私有镜像的 docker task 全部走 job 级 auth —— 节点 `/root/.docker/config.json` 不再是**任何** Nomad job 的可用性依赖。
