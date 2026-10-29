# hermes-upgrade-poc — Aria #262 (hermes 0.7.0 → 0.19.0 升级评估)

> 判据先行 (评估报告在 #262 评论)。本 cell 执行 P2a/P3/P4/P5;
> P1 已在 dev 容器实测通过 (config migrate v0→v33, zai/glm + luxeno fallback
> 逐键存活)。P2b (真实 feishu app WS 实连) owner 门控 —— 复用现役 app 会踢掉
> 生产连接 (Feishu 每 app 单 WS), 需一次性测试 app 或获准的短暂 kick 窗口。

## 判据

| # | 判据 | 方法 | 结果 |
|---|------|------|------|
| P1 | config migrate 后 zai 主模型 + luxeno fallback 键存活 | dev 容器 `config migrate` + `config get` | ✅ 2026-10-24 (config.yaml 即迁移产物) |
| P2a | feishu adapter 装载 + webhook 传输 + url_verification challenge 应答 | dummy 凭据, 127.0.0.1:8765, 全程无伤 | ✅ 3 个 alloc 连庄 (`{"challenge":"poc-challenge-262"}`) |
| P2b | feishu WS 实连 (真实 app) | 测试 app cli_aa56255…, owner DM "555" | ✅ **2026-10-25 闭合**: WS 实连 + 消息入站(text='555') + 120 字符回复出站, 双向往返全通。模型 400 (glm-4.7-flashx 不走 luxeno chat-completions) 属 P4 配置项, 非通道问题 |
| P3 | cron 真跑 | `--no-agent --script` 确定性 tick (零 token) | ✅ 分钟级自然 tick 连续 completed (post-hoc 实证; entrypoint 的 3s 即查是已知假阴性, 见下) |
| P4 | claude -p dispatch | luxeno messages 通道 + `ANTHROPIC_MODEL=glm-4.5-air` | ✅ `P4-PASS: claude -p 经 luxeno 路由应答` (注: claude 不识 glm id → 按 200k 窗跑, 真迁移时按官方指引设窗) |
| P5 | 不打扰现役 | 独立 job + 容器内 hermes-home, 只读复用 var | ✅ 全程现役 0.7 gateway 同 alloc 零重启 |

## 实测踩坑记录 (真迁移的输入)

1. **aiohttp 打包缺口**: feishu adapter 的 webhook 模式 import aiohttp, 但它属
   `messaging` extra — 须 `[feishu,messaging]` 双 extra
2. **claude 认证三件套**: `ANTHROPIC_BASE_URL=api.luxeno.ai` +
   `ANTHROPIC_API_KEY=<luxeno key>` + `ANTHROPIC_MODEL=glm-4.5-air` (luxeno 的
   Anthropic Messages 通道按模型开放: glm-4.5-air/glm-4.6 通, claude-*/flashx
   不通 — 400; /v1/models 是网页路由没有清单, 逐模型探测定论)
3. **claude 安装**: claude.ai/install.sh 跨境失败 → 内网 Verdaccio (.206:4873)
   `npm i -g @anthropic-ai/claude-code` 稳定
4. **P3 检测假阴性**: entrypoint tick 后 3s 即查 `cron runs` 拿空表 (store 写入
   滞后), 等 1-2 分钟自然 tick 即见 completed 记录
5. **P2b 排查路 (10-24/25 两天, 最终根因 = `im:message.p2p_msg` 权限缺失)**:
   - `activate_status=2` **不是 blocker** (差分实证: 生产 bot 也是 2, 照样收事件)
   - **`im:message.p2p_msg` (获取用户发给机器人的单聊消息) 才是 DM 事件触发的
     前提** — 飞书官方文档明确 "开启任一 p2p 权限即可订阅", 没有它事件订阅
     配得再对也不推单聊。此前只开了泛 `im:message` 不够 (或够但当时版本未含)
   - 排查方法论教训: **先做差分对照** (生产 app 同 API 跑一遍, 看什么是正常态),
     **再做裸 SDK 二分** (lark-oapi 直连绕开 hermes, 隔离客户端 vs 平台侧),
     **最后全量日志** (不要过滤, 过滤探针是假阴性之源)
   - `GATEWAY_ALLOW_ALL_USERS=true` 是另一个隐性前置 (不设则 DM 走 pairing
     fail-close, bot 沉默且日志只在 DEBUG 级别) — 生产 .env 里有, 测试初始没配
   - hermes 0.19 的 config.yaml 里 model 的 provider=custom + model=glm-4.7-flashx
     走 luxeno **chat-completions** 端点 → 400 (该模型只在 Anthropic Messages
     通道可用); 真迁移须改 provider 形态或换模型名

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
