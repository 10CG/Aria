# hermes-019-migration tasks

## Phase 0 — 镜像与验证 (CI)

- [x] TASK-001: 生成 0.19.0 wheelhouse (`pip download hermes-agent[feishu]==0.19.0`,
       仅 feishu extra; 若 WS 模式需 aiohttp 则加 messaging)
- [x] TASK-002: 重写 aria-orchestrator/Dockerfile (删 vendor, 加 wheelhouse, 保 claude)
- [x] TASK-003: 生成迁移后 config (0.7 yaml → `config migrate` → v33, 模型改 glm-4.5-air)
- [x] TASK-004: CI build + verify (hermes --version + config check + 镜像体积)
- [x] TASK-005: C1 判据记录

## Phase 1 — 测试 app 全功能冒烟

- [x] TASK-006: 部署 0.19 job (独立名, 测试 app 凭据, nomad var)
- [x] TASK-007: C2 判据 (config show 主模型/fallback)
- [x] TASK-008: C3 判据 (WS 实连 + DM 往返, 同 PoC P2b)
- [x] TASK-009: 从 0.7 hermes-home/cron/ 导出 cron 条目清单
- [x] TASK-010: 逐条转 0.19 cron create + C4 判据 (每条 exit 0)
- [x] TASK-011: skills 迁移 + C5 判据 (识别 + 触发)
- [x] TASK-012: C6 判据 (claude -p dispatch)
- [x] TASK-013: Phase 1 判据汇总 → owner 过审

## Phase 2 — Cutover (生产 app)

- [x] TASK-014: 生产 app 凭据写入 var (feishu 键追加到 nomad/jobs/aria-orchestrator)
- [x] TASK-015: 低峰窗口: 停 0.7 → 起 0.19 (生产 app) → C7 判据 (WS/DM/cron)
- [x] TASK-016: 0.7 job 保留 (stopped 不 purge, 24h 回滚保险)

## Phase 3 — 观察 + 收尾

- [x] TASK-017: 24h 观察 (C8: gateway 零重启 + cron 按时 + 零事故) — **[终判绿 2026-10-28]** gateway 实测 Total Restarts=0 26h+ / 零事故 (1 次 WS 瞬断 11s 自愈); cron 面经 owner 裁定 (#266): 0.7 hermes cron 职责由 aria-layer1-* 4 nomad 轨覆盖
- [x] TASK-018: 关 0.7 job (purge) + 归档旧镜像 + 更新文档 (CLAUDE.md hermes 版本) — **[执行 2026-10-28]** 0.7 无残留 job 对象 (cutover 时 in-place 同名替换, 无可 purge, 实测核); 旧镜像 digest 20f9cb5a 退役记录于本归档; CLAUDE.md Layer 1 行 → hermes 0.19 (glm-4.6)

## 依赖

- #262 PoC 六绿 (已完成)
- 飞书测试 app (已有, 凭据已清 — Phase 1 需 owner 重放 secret)
- luxeno API key (nomad var 已有)
- 内网 Verdaccio (.206:4873, 已有)
