---
name: hermes-019-migration
level: 2
status: done — 全周期 C1-C8 绿; C8 经 owner 2026-10-28 裁定 (#266: aria-layer1-* 覆盖 cron 面; gateway 26h+ 零重启实测); cutover 2026-10-27T16:26:36Z (#262); 归档为本侧重做 (原轨 209bd272 全绿宣称曾与实测不符, 未并)
module: aria-orchestrator (子模块: Dockerfile + config + deploy HCL) + Aria (CI workflow)
created: 2026-10-26
issue: https://forgejo.10cg.pub/10CG/Aria/issues/262
evidence_base:
  - Aria #262 PoC 六判据全绿 (P1/P2a/P2b/P3/P4/P5, 2026-10-24/25)
  - poc/hermes-019-upgrade 分支 (判据表 + 五条踩坑记录, 0.19.0 实测)
  - Aether #543 R3-R5 (平台目录 + 渠道身份与接管)
  - 0.7 现役: aria-orchestrator docker (heavy, 129MB vendor, digest 20f9cb5a)
unverified_claims:
  - claim: "TASK-006: 部署 0.19 job (独立名, 测试 app 凭据, nomad var)"
    reason: "dogfood/benchmark/deploy claim 无可链接产物路径或路径不存在"
    symbols: []
unverified_ack: false
---

# hermes 0.7.0 → 0.19.0 真迁移

> **Linked Issue**: `10CG/Aria#262, 10CG/Aria#266`

## Why

- **供应链复活**: 0.7.0 已被 PyPI 索引淘汰, 129MB 死 venv vendor; 0.19.0 活源
  (wheelhouse 57MB, 含完整依赖), 内置 config migrate (v0→v33)
- **原生 feishu 适配器**: 0.19 的 plugins/platforms/feishu (WS 长连/去重/串行/
  reaction/卡片) 比 0.7 自建 Lark 接入层完整 (openclaw 血统)
- **PoC 全绿**: Aria #262 六判据通过, 判定 GO 无保留

## What Changes

### 1. Dockerfile 重写 (aria-orchestrator 子模块)

- 删: `COPY aria-orchestrator/vendor/` (129MB 死树)
- 加: `pip install --no-index --find-links=/tmp/wheels hermes-agent[feishu]==0.19.0`
  (wheelhouse 57MB; `[messaging]` extra 仅当 feishu WS 模式需要 aiohttp 时加)
- 保留: claude CLI (内网 Verdaccio 安装, P4 已验)
- 保留: scan.sh + skills/ + config
- **瘦身目标**: <1.5GB (0.7 时代 ~500MB; PoC 全家桶 2.74GB 因含 messaging 全栈)
  - 去 messaging extra 省 ~500MB (telegram/discord/slack 栈)
  - wheelhouse 层多阶段构建优化
- **必须包含**: `GATEWAY_ALLOW_ALL_USERS=true` 环境变量 (PoC 教训 #5)

### 2. 配置迁移 (hermes-config.yaml)

- `hermes config migrate` v0→v33 (P1 已验: zai 主模型 + luxeno fallback 逐字存活)
- **模型路由修正** (PoC 教训: glm-4.7-flashx 不走 luxeno chat-completions → 400):
  - 方案 A: 改 `model.default: glm-4.5-air` (P4 实测 luxeno Anthropic Messages 通)
  - 方案 B: 保留 0.7 的 zai/glm-4.5-air provider (需 zai key 注入)
  - **裁定**: 方案 A (最小变更, luxeno 已有 key)
- **新增 feishu 通道配置** (template 注入, 不落 HCL 明文):
  - `FEISHU_APP_ID` / `FEISHU_APP_SECRET` (生产 app cli_a95f50…)
  - `FEISHU_CONNECTION_MODE=websocket`
  - `FEISHU_DOMAIN=feishu`
  - `GATEWAY_ALLOW_ALL_USERS=true`
  - `FEISHU_ALLOWED_USERS` (owner open_id, cutover 后从首条 DM 日志捕获)

### 3. Cron 迁移

- 0.7: cron 条目在 hermes-home 运行时状态 (不在 config.yaml 里)
- 0.19: `hermes cron create --name X --script Y 'schedule' 'prompt'`
- **迁移面**: 逐条从 0.7 hermes-home/cron/ 目录导出 → 转为 0.19 `cron create`
- scan.sh (277 行) 保持原样 (bash 脚本, 0.19 的 `--script` 模式直接调)

### 4. Skills 迁移

- 2 个 skill: `dispatch-development` (claude -p 调度) + `heartbeat-scan` (scan.sh)
- 各只有 SKILL.md, 无代码; 验证 0.19 的 skills 系统能识别 0.7 格式

### 5. 部署策略 (渐进, 不双活)

WS 单连接约束 → 0.7 和 0.19 **不能同时连同一飞书 app**:

```
Phase 0: 构建新镜像 (CI) + 本地 verify
Phase 1: 用测试 app (cli_aa56255…) 部署 0.19 → 全功能冒烟
         (gateway 起 / cron 真跑 / skill 触发 / claude dispatch / Lark 往返)
Phase 2: cutover — 停 0.7 → 换生产 app 凭据 → 起 0.19 → 验收
Phase 3: 观察 24h → 关 0.7 job → 归档
```

### 6. 不变面 (明确排除)

- **4 个 layer1 periodic job**: plain-python (aria_layer1 包), 零 hermes 依赖, 不动
- **scan.sh 本体**: bash 脚本独立于 hermes 版本, 不改
- **nomad var 结构**: `nomad/jobs/aria-orchestrator` 路径不变, 加 feishu 键
- **飞书 app 身份**: 生产 app cli_a95f50… (cutover 时沿用)

## 判据 (C1-C8, 演练前写定)

| # | 判据 | 方法 |
|---|------|------|
| C1 | 新镜像从 Dockerfile 构建, `hermes --version` = 0.19.0, 镜像 <1.5GB | CI verify |
| C2 | config migrate 后主模型 + fallback 解析正确 (`config show` 实证) | Phase 1 |
| C3 | feishu WS 实连 + DM 消息收发往返 (同 PoC P2b 标准) | Phase 1 (测试 app) |
| C4 | 全部 cron 条目从 0.7 格式迁移到 0.19 store, 每条真跑一轮 exit 0 | Phase 1 |
| C5 | 两个 skill (dispatch-development, heartbeat-scan) 可被 0.19 识别和触发 | Phase 1 |
| C6 | claude -p dispatch 经 luxeno 路由应答 (同 PoC P4 标准) | Phase 1 |
| C7 | cutover: 停 0.7 → 起 0.19 (生产 app) → WS 连通 + DM 往返 + cron 首轮 OK | Phase 2 |
| C8 | 24h 无回归: gateway 零重启 + cron 按时跑 + 零生产事故 | Phase 3 |

## 已知风险与缓解

| 风险 | 缓解 |
|------|------|
| 0.19 cron store ≠ 0.7 cron 目录格式 | Phase 1 逐条迁移验证; 遗漏条目从 0.7 hermes-home/cron/ 对照 |
| 模型路由 (chat-completions vs Anthropic Messages) | 方案 A 用 glm-4.5-air; 如 luxeno 不支持则 fallback zai |
| 飞书 WS 单连接 → cutover 有秒级窗口 | 秒级可接受 (Aether #543 R5 接管能力); Phase 2 在低峰执行 |
| 0.19 的 80+ 子命令表面积 (攻击面/资源) | 资源限制 512MB + 重启策略 mode=delay; 表面积风险接受 (PoC 已跑) |
| skills 格式不兼容 | Phase 1 C5 判据; 如不兼容仅改 SKILL.md frontmatter |

## Alternatives Considered

| 方案 | 否决理由 |
|------|----------|
| 升级到 0.22.x (GitHub 源装) | 增量 = Connectors/桌面端/pm (非我们依赖面); 0.19.0 已验全绿 |
| 保持 0.7 不动 | 供应链已死 (PyPI 无此版本), 每次重建都是考古 |
| 自维护 0.7 fork | owner 定调"最后手段"; 0.19 已验证不需要 |
