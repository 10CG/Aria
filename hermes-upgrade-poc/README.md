# hermes-upgrade-poc — Aria #262 (hermes 0.7.0 → 0.19.0 升级评估)

> 判据先行 (评估报告在 #262 评论)。本 cell 执行 P2a/P3/P4/P5;
> P1 已在 dev 容器实测通过 (config migrate v0→v33, zai/glm + luxeno fallback
> 逐键存活)。P2b (真实 feishu app WS 实连) owner 门控 —— 复用现役 app 会踢掉
> 生产连接 (Feishu 每 app 单 WS), 需一次性测试 app 或获准的短暂 kick 窗口。

## 判据

| # | 判据 | 方法 | 结果 |
|---|------|------|------|
| P1 | config migrate 后 zai 主模型 + luxeno fallback 键存活 | dev 容器 `config migrate` + `config get` | ✅ 2026-10-24 (config.yaml 即迁移产物) |
| P2a | feishu adapter 装载 + webhook 传输 + url_verification challenge 应答 | dummy 凭据, 127.0.0.1:8765, 全程无伤 | 待 cell |
| P2b | feishu WS 实连 (真实 app) | **owner 门控** (见上) | 待 owner |
| P3 | cron 真跑 | `--no-agent --script` 确定性 tick (零 token) | 待 cell |
| P4 | claude -p dispatch | luxeno 路由 (现役同款), `P4-OK` 应答 | 待 cell |
| P5 | 不打扰现役 | 独立 job + 容器内 hermes-home, 只读复用 var | 结构即证 |

## 打包事实 (对 #262 报告的补充)

- wheelhouse 57MB/83 wheels (`pip download hermes-agent[feishu,messaging]==0.19.0`,
  python3.11) — **小于 0.7 的 129MB vendor 快照**
- ⚠️ 上游打包缺口: aiohttp 属 `messaging` extra, 但 feishu adapter 的 webhook
  模式 import aiohttp — 单装 `[feishu]` 不够, 须 `[feishu,messaging]` 双 extra
- venv 离线闭环 (`--no-index --find-links`) 已验证

## 文件

- `Dockerfile` — python:3.11-slim + wheelhouse 离线装 + claude CLI
- `config.yaml` — P1 迁移产物 (model 默认改 luxeno, 其余逐字保留)
- `entrypoint.sh` — P2a/P3/P4 顺序判据, verdict 行落 `/root/poc-verdicts.txt`
- `poc-tick.sh` — P3 载荷
- `deploy/hermes-upgrade-poc.nomad.hcl` — heavy docker, 独立性见头注
- `wheels/` — 构建时覆盖 (不入库, .gitignore)
