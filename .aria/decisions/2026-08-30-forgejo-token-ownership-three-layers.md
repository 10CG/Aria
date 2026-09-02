---
type: ownership_ruling
subject: forgejo-token-ownership-aria-aether-10cg-local
status: decided
decided_by: owner
decided_at: 2026-08-30
inventory: .aria/pat-inventory.yaml
liveness_check: forgejo-app-token-liveness (.aria/state-checks.yaml)
related:
  - .aria/decisions/2026-08-08-credential-rotation-ownership-transfer-to-aether.md
  - https://forgejo.10cg.pub/10CG/Aria/issues/151#issuecomment-20214
  - Aether/docs/guides/forgejo-token-map.md
  - Aether/.aether/pat-inventory.yaml
---

# Owner Decision — Forgejo token 三层归属: 实例 / 账号与集群级 / 应用级

> **Date**: 2026-08-30 | **Decider**: owner | **执行容器**: bfe8285d
> **Trigger**: M6 TASK-028 实测发现 Layer 2 容器的 `FORGEJO_BOT_PAT` 已死 (Forgejo 不认, uid 0),
> owner 问「token 这个事情归 Aria 管, 还是归 Aether 或 10cg local 管? 现在感觉有些乱」。

## 裁定

沿用 2026-08-08 决策的判据 —— **「谁有轮换执行面谁管」, 逐凭据判, 不按类判** —— 三方各管一层:

| 层 | 归属 | 依据 |
|---|---|---|
| Forgejo **实例** (LXC 300 @ pve-node2; 数据库、备份、升级、cloudflared 链路) | **10cg.local** | 其 CLAUDE.md: 「aether 管集群, 本仓库管本地」; 规则 3「不在本仓库存放 secrets / tokens」—— 管机房不管凭据 |
| **账号模型** + 机器账号 `10cg-ci-bot` + 规则 (人机分离 / 最小 scope / 按 store 登记 / 吊销前枚举全 store) + 轮换原语 (`aether-rotate-pat`, `aether env set`) + **集群级 token** (T2 `docker_auth_*` 镜像拉取 · T3 org CI · T4 aria-build 推镜像) | **Aether** | `forgejo-token-map.md` 权威; Aether 明言看不到 Aria 的 store (Aria #151) |
| **应用级 token** —— Aria 运行时代码自己消费的: `nomad/jobs/aria-orchestrator.FORGEJO_BOT_PAT` (Layer 1) / `nomad/jobs/aria-layer2-runner.FORGEJO_BOT_PAT` (Layer 2) | **Aria** | 只有 Aria 知道各消费点的 scope 需求 (Layer 2 要 `write:repository`, Layer 1 不要); 消费代码在 Aria; 挂了只在 Aria 的 dispatch 链路显形; 08-08 决策已点名「Nomad var `FORGEJO_BOT_PAT` 不转交」 |

**分工**: Aether 只提供原语 (在 `10cg-ci-bot` 名下签 token 的 PAT API 通道、CAS 安全的单键写 `aether env set`), 不替 Aria 做决定; Aria 定 scope、答归属、登台账、跑活性检查; owner 批准 + 持有 bootstrap 凭据的那一步。

## 「乱」的三个来源与对应处置

1. Aria 的 token 挂在共享机器账号下且命名像 org 的 → 答 #151 (comment 20214); 命名约定 `aria-<consumer>-<yyyymmdd>`。**不新开账号** (两账号模型是 Aether H1 的核心修复)。
2. Aria 没有台账也没有活性检查 → `.aria/pat-inventory.yaml` (元数据, 与 Aether 同指纹算法) + state-check `forgejo-app-token-liveness` (每次 `/state-scanner` 探活性 + 指纹漂移, 只输出元数据)。
3. 同一 Nomad 变量里两家的键混住 → 键级归属写进台账 `key_ownership` 段 (混住可以, 写下来就不乱)。

## 落地工件 (2026-08-30)

- `.aria/pat-inventory.yaml` — 3 条 (Layer 1 active / Layer 2 dead_pending_reissue / runner-template deprecated_dead) + 指针 + 键级归属
- `.aria/probes/forgejo-app-token-liveness.py` + `.aria/state-checks.yaml` 新 check —— 首跑: Layer 1 OK (200, 指纹一致) / **Layer 2 FAIL DEAD** (预期的红, 重签后转绿)
- Aria #151 归属回复 (comment 20214): `aria-runner-bot` = Aria 在用, 保持; `…v2-full-scope` = Aria 无消费点, 同意 Aether 枚举 store 后吊销
- 本文件

## 待办 (凭据动作, owner)

1. `10cg-ci-bot` 名下签 `aria-layer2-git-2026-Q3` (**命名勘正 2026-09-02**: 初版写 `-<yyyymmdd>` 是 AI 自拟, 与现行实态不符; 现行 = `<用途>-<YYYY>-Q<n>` cohort 形式, 先例 `todo-web-ci-2026-Q3` [08-08 最新真实签发] / `org-ci-shared-2026-Q3` / `aria-build-bot-2026-Q3`, 轮换时随台账 Q 后缀改名; 登记必带 account + forgejo_token_name, per Aether #292) (scope `write:repository` + `write:issue`; 不要 `write:package`) → `aether env set --job aria-layer2-runner FORGEJO_BOT_PAT <new>` → 跑 scratchpad `m6-pat-scope-probe.hcl` 验 push --dry-run → 更新台账 → check 转绿 → #151 补一条 (账号名+token 名+指纹), 供 Aether 定期对账 bot 账号 token 时有档可查 (他们 §5 的「册外盲点」教训)。
2. `nomad/jobs/aria-runner-template` 变量: 删 (job 已 deprecate, DEC-20260523-001)。

> **补记 (2026-09-02, owner 两项裁定)**: (a) 名字定为 `aria-layer2-git-2026-Q3` (Q-cohort 勘正已入上文);
> (b) **轮换周期 = 永久** —— Forgejo token 默认不过期, 不设强制轮换; 台账两条应用级 token 均改
> `rotation.policy: permanent`。补偿控制 = state-check `forgejo-app-token-liveness` 每次扫描做活性 +
> 指纹漂移检查; 若发生泄露, 按即时吊销重签处理 (先枚举全 store), 不依赖周期兜底。

3. 纯卫生 (随下次碰这两处一起): `initial.sh:602` 用户名字面量 / `aria-orchestrator.FORGEJO_BOT_USER` 改 `10cg-ci-bot` (实测不影响鉴权)。
