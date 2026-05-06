# Owner Decision — Secret Rotation Deferred to Production Launch

> **Date**: 2026-05-02
> **Decider**: solo-lab (uni.concept.wzfq@gmail.com)
> **Type**: Risk acceptance (security debt)
> **Trigger**: T1.7 cluster deploy 前置评估 (M2 deploy session)
> **Status**: Active deferral until production launch

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
