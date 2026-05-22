# Owner Decision — Secret Rotation Deferred to Production Launch

> **Date**: 2026-05-02
> **Decider**: solo-lab (uni.concept.wzfq@gmail.com)
> **Type**: Risk acceptance (security debt)
> **Trigger**: T1.7 cluster deploy 前置评估 (M2 deploy session)
> **Status**: **Resolved 2026-05-22** — 原 4-key set 处置完毕:3 个 FEISHU_* key 轮换 (O1, 保留 app 仅重置密钥) + GLM_API_KEY 经 Hermes→Luxeno 重定向架构性退役。见 §Resolution。
>
> **2026-05-20 amendment**:
> - **触发条件 #1** (Aria 2.0 production launch — M5 T-deploy) fired
> - **触发条件 #3** (任一 key 被任何手段重新暴露) fired — 5 个 Nomad var keys 经 `nomad var get -out=json` 在 chat transcript 暴露 (本决议未列入这 5 个 key, 它们是 M4/M5 era 新增 secret, 不与本决议原 4-key set 重叠)
> - **本决议原 4-key set (GLM_API_KEY + FEISHU_APP_SECRET + FEISHU_VERIFICATION_TOKEN + FEISHU_ENCRYPT_KEY) 仍未轮换**, 延后到 M5 Phase C 完成后 OR 2026-08-02 hard cap (whichever first); 详见 [`2026-05-20-secret-rotation-during-m5-deploy.md`](2026-05-20-secret-rotation-during-m5-deploy.md) §3.3
> - 本决议 status 在原 4-key set 实际轮换后改为 `Resolved YYYY-MM-DD`

---

## 决策

继续使用当前 4 个被对话日志暴露过的 keys，**不轮换**, 直到 Aria 2.0 正式上线 (production launch). 上线前**必须**轮换全部 4 个 + 任何后续被同样路径暴露的 key.

## 暴露的 4 个 Key (audit trail)

来源: 2026-05-02 T15.1 deployment session 中, `nomad job inspect aria-orchestrator` 命令的输出包含 dotenv 渲染后的 runtime resolved Env, 进入对话 transcript (transcript 已保留在 session 历史内, 未流出 lab 边界).

| # | Key 名称 | 用途 | 存储位置 |
|---|---------|------|---------|
| 1 | `GLM_API_KEY` | 智谱 GLM API 直连 (现已通过 Luxeno 代理走, 此 key 实际仅作为历史 fallback) | `/root/.hermes/.env` (light-1) |
| 2 | `FEISHU_APP_SECRET` | Feishu app authentication secret | `/root/.hermes/.env` |
| 3 | `FEISHU_VERIFICATION_TOKEN` | Feishu webhook verification token | `/root/.hermes/.env` |
| 4 | `FEISHU_ENCRYPT_KEY` | Feishu webhook payload encryption key | `/root/.hermes/.env` |

**暴露路径**: `nomad job inspect` 命令的 `Env` 字段在 Nomad template 渲染后会包含明文 key, 命令输出经 transcript 进入 session log. 不是网络泄露, 不是 stdout 泄露给 third-party, 但理论上若 transcript 被外发可能扩散.

## 决策理由

| 因素 | 说明 |
|------|------|
| 当前阶段 | M2 dev (Lab 内部 dogfooding, 无 external access) |
| Lab 边界 | 10CG Lab 自有基础设施 (Aether cluster + Forgejo + Luxeno = silknode 自有品牌); 4 个 key 都是 lab 自管, 无外部暴露面 |
| 轮换成本 | Feishu 端需要重新申请 + 重新配置回调; Luxeno key 需走 silknode 流程; 总成本 ~30min owner time |
| 风险评估 | Lab 内 dev 阶段, 风险等级 LOW; 上线生产前必修 |
| 触发时机 | 当 Aria 2.0 转为对外 / production-grade 服务 (M3+ 完成 + 正式上线决议) 时强制执行 |

## 触发条件 (强制)

下列**任一**条件满足时, 必须立即执行 4 个 key 轮换且不再延期:

1. **Aria 2.0 production launch** (M5 或后续, 任何对 Lab 外提供服务的 milestone)
2. **Transcript 离开 Lab 边界** (例如 owner 把 session log 分享给 lab 外人员 / 上传到 public repo)
3. **任一 key 被任何手段重新暴露** (新 nomad inspect / 日志 / 截图)
4. **超过 90 天未轮换** (2026-08-02 到期, 用作硬时限护栏防止 dev 期无限拖延)

## 轮换执行 SOP (上线前清单)

1. **Feishu 后台**: 删除当前 app credentials → 重建 app → 拿到新的 `APP_SECRET` / `VERIFICATION_TOKEN` / `ENCRYPT_KEY`
2. **智谱后台 / Luxeno**: 旋转 `GLM_API_KEY` (或确认通过 Luxeno 代理后此 key 是否仍需要; 若否则直接删除)
3. **Nomad Variables**: `nomad var put aria-orchestrator/secrets KEY=NEW_VALUE` (4 处, batch)
4. **本地 .env**: 清除 `/root/.hermes/.env` 旧值, 改为引用 Nomad Variables 渲染 (避免再次明文落盘)
5. **重启 hermes**: `nomad job stop -purge aria-orchestrator && nomad job run aria-orchestrator.hcl`
6. **验证**: `nomad job inspect aria-orchestrator | grep -i 'GLM_API_KEY\|FEISHU' | wc -l` 确认输出已是 redacted 或不在 Env 字段中
7. **本文件 status**: 改为 `Resolved YYYY-MM-DD` + 在结尾追加 rotation 实际日期 + 操作摘要

## 监控点

- M2 → M3 transition session 入口 (state-scanner 自动检查 `.aria/decisions/` 目录) 应主动提醒此 deferral
- M3 brainstorm / Spec drafting 必须把 secret rotation 列入 production-launch checklist
- 90 天硬时限到期时 (2026-08-02), 即使 production launch 未发生也应触发 reminder

## 跨引用

- 当前 `aria-orchestrator` job runtime env (light-1): `nomad job inspect aria-orchestrator`
- M2 handoff `legal_assumptions` + `open_issues_for_m3` 段
- AD-M1-11 Nomad Variables 注入路径 (本决议明确选择继续走 Variables, 不切 Vault — Vault Aether#32 仍 open)
- Aether#32 (Vault + Workload Identity) — 长期 fix, 不是 M2 范围

---

## Resolution (2026-05-22)

原 4-key deferral set 处置完毕,本决议 **CLOSED**:

| Key | 处置 | 日期 |
|-----|------|------|
| `FEISHU_APP_SECRET` | **轮换** — Feishu 后台重置 App Secret (保留 app, APP_ID 不变);写入 `/root/.hermes/.env`;Hermes 重启验证 Feishu WS 干净重连 ✅ | 2026-05-22 |
| `FEISHU_VERIFICATION_TOKEN` | **轮换** — Feishu 事件订阅重新生成;写入 `.env` | 2026-05-22 |
| `FEISHU_ENCRYPT_KEY` | **轮换** — 同上 (注:Hermes 现为 websocket 连接模式,该 key 属 webhook 模式工件,已轮换但运行时不行使) | 2026-05-22 |
| `GLM_API_KEY` | **superseded** — Hermes 2026-05-21 重定向 Luxeno,不再直连 Z.AI 智谱;`.env` 的 `GLM_API_KEY` var 现持 Luxeno key。原 Z.AI 账户 + 旧 key 成 orphan,owner 可在 Z.AI console 注销 (非紧急) | 2026-05-21 (架构性退役) |

**执行偏离 SOP**: §轮换执行 SOP step 1 原写"删除 app 重建",实际选"保留 app 仅重置密钥" —— APP_ID 不变免重配 callback,安全目标等效 (App Secret 一重置即作废所有派生 access_key/ticket)。owner 决策 (solo-lab) 2026-05-22。

**2026-08-02 hard cap**: 已可撤销对应 calendar reminder (4 key 均已处置)。

**残留 hygiene** (非本决议范畴): `/root/.hermes/.env` 仍明文 dotenv 落盘 → 长期迁 Nomad-var-rendered (见 `docs/handoff/2026-05-21-m5-phase-b-stabilization-hermes-luxeno.md` §2 S7)。

**触发链**: `2026-05-20-secret-rotation-during-m5-deploy.md` §2.5 (Lark WS access_key 间接 leak → FEISHU_APP_SECRET 轮换紧迫性升级) → O1 执行 (`docs/handoff/2026-05-22-m5-phase-c-playbook.md` §O1)。
