---
type: ownership_transfer
subject: credential-rotation-forgejo-nexus-cfaccess
transferred_to: 10CG/Aether
tracking_issue: https://forgejo.10cg.pub/10CG/Aether/issues/283
status: transferred
decided_by: owner (uni.concept.wzfq@gmail.com)
decided_at: 2026-08-08
---

# Owner Decision — 凭据轮换归属转交 Aether + 一处错挂期限的更正

> **Date**: 2026-08-08
> **Decider**: solo-lab (uni.concept.wzfq@gmail.com)
> **Type**: Ownership transfer (跨仓归属裁定) + carry-forward 记录更正
> **Trigger**: owner 在 `/state-scanner` 会话入口提出「凭据轮换是否应和其他项目一样转交 Aether 经 issue 反馈, 不应记录为 Aria 开发任务」

---

## 决策

`FORGEJO_TOKEN` / `NEXUS_API_TOKEN` / `CF_ACCESS_CLIENT_SECRET` 三个凭据的轮换**归属 Aether**, 经 [Aether #283](https://forgejo.10cg.pub/10CG/Aether/issues/283) 跟踪。

**Aria 侧这条 carry-forward 就此关闭** —— 不再出现在 Aria 的 handoff §2 / §6 / `/state-scanner` 推荐区。后续状态查询指向 Aether #283。

## 归属核实 (2026-08-08)

| 凭据 | 归属证据 | Aria 侧消费方 |
|------|----------|---------------|
| `FORGEJO_TOKEN` | org 级 `10CG/FORGEJO_TOKEN` Actions secret (Aether #189 TL;DR 逐字) | **无** — Aria 用 `FORGEJO_BOT_PAT`, 独立凭据线 |
| `NEXUS_API_TOKEN` | nexus / devpi 内网镜像 = Aether 基建 (Aether #257 / #242) | **无** — 全仓 grep `*.py/*.sh/*.hcl/*.json/*.yaml` 零命中 |
| `CF_ACCESS_CLIENT_SECRET` | CF Access = Aether 集群 ingress 平面 | **无** |

判据不是「谁泄漏的」而是「**谁有轮换执行面**」。三者的轮换工具链在 Aether: `aether-rotate-pat` (Tier 1, Aether #45) + `.aether/pat-inventory.yaml` + `docs/guides/forgejo-token-map.md`。Aria 侧连一个消费点都没有, 无从验证轮换是否生效。

**对照 (为什么不是一刀切转交)**: Aria 真正自有的凭据 —— `LUXENO_API_KEY` / `ARIA_FEISHU_*` / Nomad var `FORGEJO_BOT_PAT` —— 有 Aria 侧 decision 记录且已各自处置, 那些**不**转交。归属判定按凭据逐个做, 不按「凭据类」做。

## 更正: `2026-08-02` hard cap 是错挂的

Aria 侧连续约 10 份 handoff 把这三个凭据标为「🔴🔴 hard cap `2026-08-02` 逾期不可补救」。核实后该期限对这组凭据**不成立**:

| 事实 | 证据 |
|------|------|
| `2026-08-02` 属于**另一组 4 key** (`GLM_API_KEY` + 3×`FEISHU_*`) 的 90 天护栏 | `.aria/decisions/2026-05-02-secret-rotation-deferred.md:51` |
| 那组已 **Resolved 2026-05-22**, 且 cap 已显式撤销 | 同文件 `:7` status + §Resolution「2026-08-02 hard cap: 已可撤销对应 calendar reminder (4 key 均已处置)」 |
| 本组三个凭据的真实来源是 **2026-07-19** 一次 `assertIn` 对 dict 查键 → unittest 把整个 env 渲染进 failure diff | `docs/handoff/2026-07-19-mainspec-phase4-todo-closeout-v1.62.0.md:44` |
| 本组**从未有任何 decision 记录指派期限** | `grep -rln FORGEJO_TOKEN .aria/decisions/` 唯一命中是 2026-08-06 决策单, 而那只是转抄的 carry 表 |
| cap 被接到本组上的时点 | `docs/handoff/2026-07-22-...md:33`「bot 07-22 handoff 记『第六次未回, hard cap 2026-08-02 (剩 ~11 天)』」 |

⇒ 真实状态: **一次 Lab 内部 transcript 暴露, 2026-07-19 发生, 未轮换**。风险真实, 但没有 Aria 侧能计的 deadline。「逾期 6 天」是从一份已关闭的豁免上借来的数字。

## 方法论教训 (memory candidate)

**两条独立的错误在同一条 carry 上叠加, 且都靠「重复」获得了可信度**:

1. **归属错**: 泄漏发生在 Aria 的 session 里 ⇒ 被当成 Aria 的待办。但「暴露地点」与「轮换执行面」是两回事; 判据应是后者。
2. **期限错挂**: 一个真实存在过、但已正式撤销的日期, 被接到一组毫无关系的凭据上, 然后跨 ~10 份 handoff 逐次继承, 每次继承都追加一个更急迫的措辞 (「第四次未回」→「第七次」→「剩 11 天」→「剩 6 天」→「今天」→「逾期 4 天」→「逾期 6 天」)。**递增的紧迫感全部来自转抄次数, 没有一次回到源记录核验。**

这与 memory `feedback_scoped_git_add_splits_claim_from_landing` 同型 (声称与落地脱钩), 但形状不同: 那条讲「做了一半却声称全做」, 本条讲「**转抄链上没人回源**, 于是一个已撤销的期限获得了 10 次背书」。handoff 的 append-only 性质放大了它 —— 每份新 handoff 都以上一份为输入, 而不是以 canonical 记录为输入。

**处方**: handoff §2 中带日期/计数的 carry 项 (「hard cap X」「第 N 次」), 转抄时必须同时带上**源记录路径**, 且每 ~3 次转抄回源核验一次。无源路径的期限视为无期限。

## 落地工件

1. 本文件
2. [Aether #283](https://forgejo.10cg.pub/10CG/Aether/issues/283) — 含归属证据表 + 轮换请求 + 期限更正说明 (请 Aether 侧若要设期限则另立成文记录, 不继承已关闭的 cap)
3. 后续 handoff §2/§6 移除该项, 改为一行指针

## 跨引用

- `.aria/decisions/2026-05-02-secret-rotation-deferred.md` — 被误借期限的源记录 (Resolved 2026-05-22)
- `.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md` — Aria 自有凭据的处置轨迹 (对照组)
- `docs/handoff/2026-07-19-mainspec-phase4-todo-closeout-v1.62.0.md:44` — 本组泄漏的首次记录
- Aether #189 / #195 / #257 / #242 — 三个凭据归属 Aether 的外部证据
- Rule #7 `standards/conventions/secret-hygiene.md` — 暴露侧代码已修 (脱敏 ≠ 闭环)
