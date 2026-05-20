# Owner Decision — Secret Rotation Active + Plugin-Level secret-guard Upgrade Path

> **Date**: 2026-05-20
> **Decider**: solo-lab (uni.concept.wzfq@gmail.com)
> **Type**: Risk response (active leak) + framework upgrade decision
> **Trigger**: M5 T-deploy Phase B.5 `nomad var get -out=json` 命令在本 session 输出完整 8-key JSON 到 transcript
> **Status**: Layer 1 (rotation) in progress; Layer 2 (Aria-local hook) done; Layer 3 (plugin upgrade) decided, deferred to next cycle
> **Supersedes**: [`2026-05-02-secret-rotation-deferred.md`](2026-05-02-secret-rotation-deferred.md) — status changes from `Active deferral` to `Trigger #1 + #3 fired, rotation in progress`

---

## §1 决策（三层）

### Layer 1 — 5 leaked keys 立即轮换（owner-action）

5 个被本 session 暴露的 Nomad var 字段全部轮换。对应 [`2026-05-02-secret-rotation-deferred.md`](2026-05-02-secret-rotation-deferred.md) 中**触发条件 #1**（Aria 2.0 production launch — M5 T-deploy 即触发）+ **触发条件 #3**（任一 key 被任何手段重新暴露 — 本 session `nomad var get -out=json` 即触发）**同时 fire**。

### Layer 2 — Aria 项目本地装 secret-guard hook（已完成，本 session）

Cherry-pick SilkNode PR #429 的 4 个 hook 文件到 `/home/dev/Aria/.claude/scripts/`，注册 `.claude/settings.json` 的 PreToolUse + PostToolUse matcher。本 session 实测：
- 251/251 self-tests PASS（secret-guard 207 + secret-scan 44）
- Live block 验证：`nomad var get -out=json` 命令被 EXIT 2 拦截
- guard:ack bypass + jq keys 过滤路径均 EXIT 0
- 当前 session 内 hook 已激活（已在 `cat scan.sh && grep .env` 上触发 false-positive 一次，规则 conservative 符合预期）

### Layer 3 — 升级 secret-guard 为 aria-plugin 默认 hook（决议，下一 cycle 实施）

本次事故是 Lab 内**同一 root cause 的第三次复现**：
- 2026-05-02 Aria 自身 (`nomad job inspect`) — 4 keys leak
- 2026-05-06 truffle-hound (Python `subprocess.run` 默认 inherit stdio) — 4 keys leak
- 2026-05-20 Aria 自身 (`nomad var get -out=json`) — 5 keys leak（本 session）

SilkNode 已在 2026-05-16 给 Aria 提了 [Issue #107](https://forgejo.10cg.pub/10CG/Aria/issues/107) 提议把方案上移到 aria 框架默认，因 v1.22.x 优先排程 (multi-terminal-coordination) 未实施 → 本次直接 dogfood 验证了 framework gap 的 ROI。

**升级决议**：起 Spec `aria-secret-guard-plugin-default`，目标 aria-plugin v1.23.0 ship；同时 close [Issue #84](https://forgejo.10cg.pub/10CG/Aria/issues/84) + [Issue #107](https://forgejo.10cg.pub/10CG/Aria/issues/107)（这两个本质讨论同一件事不同角度）。

---

## §2 暴露 audit trail（本 session, 2026-05-20 ~13:25 UTC）

来源命令：
```
ssh light-1 'NOMAD_ADDR=http://192.168.69.70:4646 nomad var get -out=json nomad/jobs/aria-orchestrator | head -50'
```

输出完整 Items map 到 stdout → bash → 工具结果 → chat transcript（Lab 内部 transcript, 未离开 Lab 边界）。

| # | Nomad var Key | 用途 | 与 2026-05-02 leak 关系 |
|---|---------------|------|------------------------|
| 1 | `LUXENO_API_KEY` | silknode/Luxeno OpenAI-compat API key (`sk-silk-*`) | 替代 2026-05-02 leak 中 `GLM_API_KEY` 直连 |
| 2 | `FORGEJO_BOT_PAT` | `aria-runner-bot` Personal Access Token | 新增（2026-05-02 leak 不含） |
| 3 | `ARIA_FEISHU_SIGNING_SECRET` | Feishu 自定义机器人签名密钥（M4 webhook approval 路径，**不同**于 M0/M1 OAuth 路径的 `FEISHU_APP_SECRET`） | 部分重合（不同机器人） |
| 4 | `ARIA_FEISHU_WEBHOOK_URL` | Feishu webhook URL（token 嵌入 URL，UUID `fa4fe804-87df-4b27-8653-6f168e0aa8c5`） | 新增 |
| 5 | `ARIA_FEISHU_OPS_ALERT_WEBHOOK` | 同 #4（与 #4 同 token，复用同一机器人，详见 §3.2） | 新增 |

**实际 distinct secret 数**: 4（#4 与 #5 同值）。

**轮换后 Nomad var Items 数变化**: 8 → 7（决议 §3.2 选 Option B 简化为 1 key，删除 #5）。

### §2.5 Secondary leak — Lark WebSocket session credentials (2026-05-20 ~14:45 UTC)

第二次 transcript leak (本 session 内, 间接 / 派生级):

来源命令: `grep -B3 -A20 "Insufficient balance" /root/.hermes/logs/gateway.log` (B.5 deep-dive 调查 67h 429 时, 用于给 silknode 准备错误体)

输出包含 Hermes 重连 Feishu WebSocket 的日志行 (Lark/Feishu 平台 SDK 标准日志格式):

```
INFO Lark: connected to wss://msg-frontier.feishu.cn/ws/v2?
  fpid=493
  &aid=<feishu_app_id>      ← 5-7 位整数, identifies App
  &device_id=<long_int>     ← 19 位, Hermes session-scoped device ID
  &access_key=<32_hex>      ← ⚠ 32 hex chars, WS auth credential
  &service_id=<7_digit_int> ← ID, less sensitive
  &ticket=<uuid>            ← ⚠ UUID format, per-connection auth ticket
  [conn_id=<long_int>]
```

(本 decision 不复述实际值, 防止"为记录而再暴露"。具体值在 session transcript 内 + Hermes gateway.log 内, Lab 边界。)

| 字段 | 性质 | TTL | rotation 路径 |
|------|------|-----|--------------|
| `aid` | Feishu App ID | 长期, app 生命周期 | 删 + 重建 Feishu app (即 2026-05-02 deferral set 中 `FEISHU_APP_ID/SECRET`) |
| `access_key` | WS 长连接 access key, 由 APP_SECRET 派生 | session-scoped, 每次 Hermes 重启 / WS 重连即换发 | 间接 — rotate FEISHU_APP_SECRET 后旧 access_key 立即作废 |
| `ticket` | WS 连接 ticket, 单次连接握手 | 短期 (单次握手), 重连即换 | 间接 — 同上 |
| `device_id`, `service_id`, `conn_id` | session-internal identifiers | session-scoped | 自动随重启换新 |

**风险评估**:

- `access_key` + `ticket` 在 session 期间有效, 理论上可用来劫持 Feishu WS 长连接发送指令到 Hermes (但仅限当前 conn_id 期间, Hermes 一旦内部重连即作废)
- Hermes gateway.log 显示频繁重连 (本 session 已 capture 2 次 13:24/14:55 CST + 之前历史多次), 每次重连产新 access_key + ticket → 本次 leak 的 access_key 大概率**在 owner 看到 transcript 之前已自动作废**
- 但严格 zero-trust + Rule #7 #3 (任一 key 任何手段重新暴露) 角度: 这是一次真实 exposure, 应当记录

**决议**:

**不单独 rotate access_key + ticket** (它们是派生/短期, 单独 rotate 无意义)。改为:

**触发 2026-05-02 deferred 4-key set 中 `FEISHU_APP_SECRET` 的轮换紧迫性升级**:
- 原计划: defer 到 Phase C 完成后 OR 2026-08-02 hard cap (whichever first)
- **本决议提前**: rotate `FEISHU_APP_SECRET` 应在 **M5 Phase B 结束前** 完成 (B.9 sign-off 前一并 sweep)
- 其余 3 keys (GLM_API_KEY / FEISHU_VERIFICATION_TOKEN / FEISHU_ENCRYPT_KEY) 保持原计划 (Phase C 或 hard cap)

**理由**:
- `FEISHU_APP_SECRET` 是 Lark WS access_key + ticket 的派生源, 间接 leak 触发了上游轮换义务
- Phase B 已经在搞 Feishu 相关 secrets (webhook + signing), 同 cycle 多带 1 个 secret 边际成本低
- 与本次 5-key rotation 不能合并: APP_SECRET 是 `/root/.hermes/.env` 落盘 dotenv 路径, 不在 Nomad var. 轮换需独立步骤 (Feishu 后台重建 app + 改写 .env 文件 + Hermes 重启)
- 实际操作放在 B.9 sign-off 阶段 (Hermes 已经因为 ChangeMode=restart 重启过一次, 多 1 次重启边际成本可忽略)

**Action item for B.9**:
1. Feishu 后台: 删除现有 app → 重建 → 拿到新 `FEISHU_APP_ID/SECRET/VERIFICATION_TOKEN/ENCRYPT_KEY` (注意: APP_ID 也会变, callback URL 需重新配置)
2. light-1: 改写 `/root/.hermes/.env` 4 个 FEISHU_* keys (Rule #7: 用 `cat > /root/.hermes/.env <<EOF` heredoc + 显式 redirect, **不**用 `nano/vim` 等可能保留 swap 文件)
3. Hermes restart: `nomad job restart aria-orchestrator` (或等下一次 ChangeMode=restart 触发)
4. 验证: aria-heartbeat 下一次 cron tick 仍能成功投递 Feishu
5. 更新 2026-05-02 deferral decision: `FEISHU_APP_SECRET` 改 status `Resolved 2026-05-20`, 其余 3 keys 保持 deferred

**注意**: 若 B.9 时间不允许做 Feishu app 重建 (Feishu 后台操作 + callback 重新配 ~ 30-45min), 可顺延到 Phase C 头部, 但**不允许**再次 defer 到 2026-08-02。

### §2.6 Methodology lesson — log file grep 也是 secret-bearing-source

第 2 个 leak 的 lesson:

- Secret-guard hook v1.2 当前 risky_patterns 列表覆盖 `.env` 文件读 / nomad var get / cloud secret managers / 等显式 secret store 操作
- **不覆盖** application log file 读 (Hermes log / Nomad alloc log / 等), 因为 log 在原则上不应 contain secrets — 但 third-party SDK (Feishu Lark SDK) 在 INFO log 中打了 WS URL 含 query string credentials, 这是 SDK 的 logging 错误 / aggressive verbosity, 不是 Hermes 自身的失误
- AI 跑 `grep` log file 时 hook 不阻断 — false negative

**Plugin v1.23.0 upgrade scope 可考虑增项** (Layer 3 §5.3 Q1/Q2/Q3 之外):
- Q4: 是否扩展 risky_patterns 到 application log files? 或反向, 走 PostToolUse `secret-scan.sh` content scan 兜底? (后者 SilkNode v1.2 已实现, Aria 本次也已装但 active 性未观察 → 下一 cycle dogfood)

**短期 mitigation** (next session 立即起):
- AI 跑 `grep <log>` 或 `tail/head <log>` 前应 mental check: "此 log 是否可能含 SDK 写入的 third-party credential?"
- 优先用 `awk '$NF !~ /access_key|ticket|password|token/' log` 或类似 negative filter
- 或限定 grep 关键字使输出尽量 narrow (本次 grep "Insufficient balance" 范围合理, 但 -A20 给了太大 context window)



---

## §3 决策详细 — Layer 1 (rotation)

### §3.1 轮换执行 SOP（owner-runnable）

参考 [`2026-05-02-secret-rotation-deferred.md`](2026-05-02-secret-rotation-deferred.md) §轮换执行 SOP，**针对本次 5 keys 做以下调整**：

| 步骤 | 操作 | 注意事项 |
|------|------|---------|
| R1.A | Luxeno (silknode) 后台 → revoke 现 key (`sk-silk-bB8H555*` 前缀) → 生成新 key | 命名 `aria-orchestrator-prod-20260520-rotated` |
| R1.B | Forgejo (`aria-runner-bot`) → revoke PAT → 生成新 PAT | 权限范围: read+write:repository / read+write:issue / read:user |
| R1.C | Feishu 群机器人 → 安全设置 → **重置签名**（不删机器人） | webhook URL 不变（详见 §3.2） |
| R2 | 4 个新值写入 light-1 临时文件，0600 权限 | `/tmp/luxeno.new` / `/tmp/forgejo.new` / `/tmp/feishu_webhook.new`（旧 URL 不变）/ `/tmp/feishu_signing.new` |
| R3 | `nomad var put -force` 全量替换（7 keys，删 OPS_ALERT），**必须 `>/dev/null 2>&1`** | 触发 ChangeMode=restart → aria-orchestrator + aria-layer1-comment-poll 自动重启 |
| R4 | AI 用 Python `subprocess.run(capture_output=True)` 验证 keys-only（长度 + 存在性，不读 value） | Rule #7 compliant 路径 |
| R5 | `shred -u /tmp/{luxeno,forgejo,feishu_webhook,feishu_signing}.new` | 防本地落盘残留 |

### §3.2 OPS_ALERT vs WEBHOOK 架构决策

发现 `ARIA_FEISHU_WEBHOOK_URL` (general) 与 `ARIA_FEISHU_OPS_ALERT_WEBHOOK` (ops alert preferred) 设计本意是**两个 Feishu 群两个受众**（per archived Spec `2026-05-06-aria-2.0-m3-cycle-close-glm-routing-recovery` T6.4 + `reconcile_runner.py:50-67`）：

- `ARIA_FEISHU_WEBHOOK_URL` → S7_HUMAN_GATE approval 群（dev/approver 看）
- `ARIA_FEISHU_OPS_ALERT_WEBHOOK` → reconcile_runner 系统告警群（ops 看）

但实际部署时两 key 指向**同一 webhook URL**（同一 UUID token），即 M4 deploy (2026-05-09) 为 forward-compat 预留 OPS_ALERT key 但复用同 URL，因 M5 reconciler 当时未部署、无独立 ops 群必要。

**本次决议**: **Option B — 简化为 1 key**：
- R3 时只设 `ARIA_FEISHU_WEBHOOK_URL`，不设 `ARIA_FEISHU_OPS_ALERT_WEBHOOK`
- `reconcile_runner._build_feishu_client()` 走 fallback path：unset OPS_ALERT → fall through to general URL + warn log（设计内优雅降级，非 bug）
- `aria-layer1-reconcile.nomad.hcl` 已有 `{{- if .ARIA_FEISHU_OPS_ALERT_WEBHOOK }}` conditional，渲染时跳过

**为什么不选 Option C（真正分群）**: 需要新增 `ARIA_FEISHU_OPS_ALERT_SIGNING_SECRET` env key + 改 reconcile_runner 支持 per-URL signing（当前对两 URL 复用同一 `ARIA_FEISHU_SIGNING_SECRET`）。这是 Spec 工作，不在本 rotation 范围。**Future enhancement**: 若运营中发现 ops 告警与 approval 提示在同一群造成信号噪音，再起一个 ops-channel-consolidation Spec 把 OPS_ALERT 接到 `aria-heartbeat` 机器人所在的 ops 群。

**Rationale**:
- Lab 1 人 + AI，告警量短期不会大
- aria-heartbeat 机器人已经在独立 ops 群发送（per Phase A.6: `/root/.hermes/cron/jobs.json` 中 `48ed7e826bc3` 每 60min 发 Feishu），ops 通道事实存在
- 少管一个 secret 半年后减少一次 rotation 操作

### §3.3 关于其他暴露源（部分提前 + 部分仍 deferred）

`/root/.hermes/.env` 文件中**仍有 2026-05-02 leak 名单中未轮换的 4 keys**:
- `GLM_API_KEY` (智谱直连)
- `FEISHU_APP_SECRET` (M0/M1 OAuth Feishu app, **不同于** #3 ARIA_FEISHU_SIGNING_SECRET) — **2026-05-20 amendment: 提前到 M5 Phase B.9**, 见 §2.5
- `FEISHU_VERIFICATION_TOKEN`
- `FEISHU_ENCRYPT_KEY`

**Rotation 时间表 (本次 amendment 后)**:

| Key | 原计划 (2026-05-02) | **本次 (2026-05-20) amendment** |
|-----|---------------------|--------------------------------|
| FEISHU_APP_SECRET | Phase C / 2026-08-02 (whichever first) | **M5 Phase B.9 sign-off 前** (因 §2.5 Lark WS access_key 派生 leak 触发) |
| GLM_API_KEY | Phase C / 2026-08-02 | 不变 |
| FEISHU_VERIFICATION_TOKEN | Phase C / 2026-08-02 | 不变 |
| FEISHU_ENCRYPT_KEY | Phase C / 2026-08-02 | 不变 |

**理由**:
- FEISHU_APP_SECRET 是 §2.5 Lark WS `access_key` + `ticket` 的派生源, 间接 leak 触发上游轮换义务
- 其余 3 keys 在本 session **未被重新暴露**, 2026-05-02 hard cap 仍适用 (距今 75 天)
- Hermes 自身 (`/root/.hermes/.env` 中的 ANTHROPIC_API_KEY + LUXENO_API_KEY 等) 是 **M0/M1 era 旧配置**, 预计在 M5 reconciler + cron Pure Nomad 化完成后逐步迁移到 Nomad var 渲染路径 (此时 `/root/.hermes/.env` 整体废止 = 4 keys 都进 Nomad var 或 Vault)

**Action items**:
- 把 2026-05-02 deferral 的 `2026-08-02` hard cap 写入 calendar reminder (剩余 3 keys 用)
- **B.9 sign-off 前**: rotate FEISHU_APP_SECRET (Feishu app 重建; SOP 见 §2.5)
- Phase C 完成后 (≥ 24h Phase B 稳定): 评估是否一并 rotate 剩余 3 keys + `/root/.hermes/.env` 迁移路径 (消除明文 .env 落盘)

### §3.4 New key live-validation (pre-R3 dogfood verify)

Owner R1.A 完成后 (Luxeno backend revoke 旧 `sk-silk-bB8H555*` + 生成新 key 写入 `/tmp/luxeno.new`)，本 session 跑了 minimal endpoint test：

```python
POST https://api.luxeno.ai/v1/chat/completions
Authorization: Bearer <new key from /tmp/luxeno.new>
{"model": "glm-4.5-air", "messages": [...], "max_tokens": 5}
```

Result: **HTTP 200**，model 返回 `glm-4.5-air`，usage `prompt=6 + completion=5 + cached=4 / total=11`. New key 验证有效, silknode 账户当前 quota 可用。

**Implications**:
- 67h 429 历史 (2026-05-17 11:00 UTC ~ 2026-05-20 06:49 UTC) **已经自动恢复** (recovery 时间窗 14:49→15:50 UTC，原因可能是 silknode 订阅 cycle 自动重置 / 端配置变更 — 不可考据)
- Luxeno 充值 **不需要**, silknode 投诉/调查 **不需要**
- R3 可以直接推 — R3 后 ChangeMode=restart 让 Hermes 拿新 key, 立即可工作

**Lesson** (新 memory candidate `feedback_test_new_credential_before_rotation_commit`):
- Phase B.5 类轮换流程中, 在 R3 (全量替换 nomad var) 之前**必须**做一个最小 endpoint test 验证新 credential 实际可用
- 不要假设 "key 在后台生成 ≠ key 实际能用" (后台可能延迟 propagate / 权限范围错配 / 账户级 quota 已用尽)
- Test 走 Rule #7 compliant 路径: Python subprocess 读 /tmp/<cred>.new, 调最小 API, **不 echo key value, 只 print HTTP status + metadata + usage**
- 本次 dogfood 实证: AI 错误地假设余额仍为 0 → 推荐 owner 充值 → owner 反问 "不是先确认新 key 状态吗" → live test 立即驳回原假设 — owner 直觉是对的, AI 应主动建议这一步

---

## §4 决策详细 — Layer 2 (Aria 本地 hook，已完成)

### §4.1 安装内容

| 路径 | 来源 | 大小 |
|------|------|------|
| `/home/dev/Aria/.claude/scripts/secret-guard.sh` | SilkNode commit `8eef709` v1.2 | 29762 bytes |
| `/home/dev/Aria/.claude/scripts/secret-guard.test.sh` | 同上 | 28735 bytes |
| `/home/dev/Aria/.claude/scripts/secret-scan.sh` | 同上 | 18424 bytes |
| `/home/dev/Aria/.claude/scripts/secret-scan.test.sh` | 同上 | 11447 bytes |
| `/home/dev/Aria/.claude/settings.json` | 新建（matchers: Bash + Read/Edit/Write/MultiEdit PreToolUse + Bash/Read/Edit/Write/MultiEdit PostToolUse） | 555 bytes |

### §4.2 验证结果

| 测试项 | 结果 |
|--------|------|
| `secret-guard.test.sh` 自检 | 207/207 PASS |
| `secret-scan.test.sh` 自检 | 44/44 PASS |
| Live block test (`nomad var get -out=json | head -50`) | EXIT 2（block） |
| Live allow test (`nomad var get -out=json | jq keys`) | EXIT 0（allow） |
| Live ack test (`... # guard:ack: <reason ≥ 8 chars>`) | EXIT 0（allow + logged to `~/.claude/logs/guard-bypass.log`） |
| Current-session activation | ✅ Confirmed via false-positive at ~14:30 UTC（`cat scan.sh && grep .env` 被 `(head|tail|less|more)[[:space:]]+[^|]*\.env` 误匹配 block） |

### §4.3 已知 false-positive trade-off

Hook 对 `head/tail/less/more` 后跟 `[^|]*\.env` 的 pattern 在**整条命令字符串维度**匹配。本 session 实际遇 1 次：命令含 `cat scan.sh | head -30 && ... grep ... /root/.hermes/.env` 整体被 block。

- **Mitigation**：拆分命令（一条不含 head/tail/less/more 配合 .env 提及）或用 `# guard:ack: <reason>` bypass。
- **Lesson**：Hook 倾向 conservative（over-block 优于 under-block）。属设计内。后续 plugin v1.23.0 上游可视情况调整 regex（窄化为"head/tail 紧接 .env 文件路径"而非"整命令字符串维度"），但需要重跑 251 test fixtures 验证不松动 true-positive。

---

## §5 决策详细 — Layer 3 (Plugin 升级路径)

### §5.1 Spec 名称 + 范围

**Spec 名**: `aria-secret-guard-plugin-default`
**Level**: 3 (跨 aria-plugin + standards repo + 多项目 rollout，含 governance)
**ship target**: aria-plugin v1.23.0
**Close**: Forgejo Issue #84 + Issue #107（合并为本 Spec 的实施依据）

### §5.2 三个 scope 选项

| 选项 | 范围 | 工作量 | 倾向 |
|------|------|--------|------|
| **Min** | 仅 plugin-level hook 注册 (`aria/hooks/secret-guard.sh` + `hooks/hooks.json` PreToolUse + PostToolUse matcher 用 `${CLAUDE_PLUGIN_ROOT}`) + CHANGELOG + version bump | ~1-2h | 最小可上 |
| **Mid** | Min + `aria-doctor` 新增 secret-guard install 检测项 + `standards/conventions/secret-hygiene.md` update（指向 plugin-level default） | ~3-4h | ⭐ **推荐** |
| **Full** | Mid + `aria-init` skill 自动 .gitignore re-include + 跨项目 rollout playbook (Aria/SilkNode/Aether/truffle-hound) + 治理章程（governance, source-of-truth, version sync） | ~1-2 day | 长期目标 |

**本次决议倾向 Mid**: 既装上 plugin default 又有 aria-doctor 老项目补装路径，治理细节（governance / 跨项目 rollout）留给后续 minor 升级。

### §5.3 三个非平凡 open question（带入下一 cycle brainstorm）

#### Q1 — Plugin hook 与 project hook 的合并语义

Claude Code 同时加载 user-level / project-level / plugin-level 三种 hook 源时：

- 全部依次执行（任一 exit 2 即 block）— 大概率（按 Claude Code hooks docs 默认）
- 还是 plugin 被 project override
- 还是按 declare order

需在 Spec A.1 brainstorm 阶段实证（写一个最小 plugin + 项目都装 hook，用同一 trigger 跑，看实际行为）。

**实施前提**: 若是"依次执行"，则 Aria 项目本地 copy（本 session 装的）+ plugin v1.23.0 上游 copy **会跑两次**。性能 OK，但 v1.2 与 v1.23 不同步时会双重判定造成困惑。

**Mitigation 候选**: plugin ship 后 Aria 项目本地 copy 选 (a) 删除依赖 plugin，(b) 保留作 v1.2 snapshot 直到验证 plugin 路径，(c) 改成 thin wrapper 调用 plugin（最稳）。

#### Q2 — 全局 blast radius

Plugin-level hook 一旦装 → 该 plugin 加载就 active → 几乎等同 user-global（aria-plugin 是常驻插件）。任何 false positive 影响**所有 aria-plugin 项目**。

**今日已实测 1 个 false positive**（§4.3）。

**Mitigation**:
- 严格 conservative 默认（宁可 over-block）
- `# guard:ack: <reason>` escape hatch 已有
- 上游修 regex 需 minor bump + changelog 显式说明"放宽 X pattern"
- aria-doctor 加 "test your project's typical commands against the hook" 子命令
- plugin v1.23.0 ship 前在 Aria + SilkNode + Aether 跨项目跑 daily-use command 集合 smoke verify

#### Q3 — Source-of-truth 治理

三选一：

| 选项 | SOT 位置 | 维护负担 |
|------|---------|---------|
| **A** | aria-plugin SOT | plugin 维护 + version sync；SilkNode/truffle-hound 等是消费者 |
| **B** | SilkNode SOT (因实战 2 轮 audit + 251 tests) | aria-plugin 引用 SilkNode（git subtree 或人工 sync 流程） |
| **C** | `standards/hooks/secret-guard.sh` (新增 SOT 路径) | standards repo 从纯 prose 变成含 executable，scope 漂移风险 |

**本次决议倾向 A**: aria-plugin SOT。理由：
- standards repo 留给 prose convention（`secret-hygiene.md` 已在），加 executable 会 dilute 定位
- 不强制 SilkNode 立即迁移（v1.2 local copy 保留作过渡期）
- aria-plugin SOT 让"安装 plugin → 自动获得保护"成立

### §5.4 实施 timeline

**本 session（2026-05-20）**: 仅决议（本文件），不实施。

**下一 cycle (estimated 2026-05-21 ~ 2026-05-23)**:
- A.1: brainstorm + 实证 Q1 (plugin vs project hook 合并语义)
- A.2-A.3: OpenSpec `aria-secret-guard-plugin-default` Level 3
- B: 实施 Mid scope (~3-4h)
  - cherry-pick SilkNode v1.2 → `aria/hooks/`
  - `hooks/hooks.json` 加 PreToolUse + PostToolUse matcher
  - `aria-doctor` 检测项（如果项目存在 `.claude/scripts/secret-guard.sh` 本地 copy → 提示是否可移除依赖 plugin）
  - port 251 self-tests 到 plugin test suite
  - `standards/conventions/secret-hygiene.md` update
- C: PR merge + multi-remote push
- D: archive + Issue #84 + #107 close 评论 + memory entry
- Ship: aria-plugin v1.23.0

**Aria 项目自身的 follow-up**（plugin v1.23.0 ship 后）：
- 决 Q1 取舍后处理 `.claude/scripts/` 本地 copy（保留 / 删除 / 改 wrapper）
- 此 decision 文件 §4 加 amendment 标记 plugin 路径已生效

---

## §6 决策理由（meta）

### §6.1 为什么本次"用力轮换 + 升级 plugin" 优于"继续 deferral"

| 因素 | 2026-05-02 选 deferral | 2026-05-20 选 active rotation + plugin upgrade |
|------|----------------------|------------------------------------------------|
| 阶段 | M2 dev | M5 T-deploy（**正是 2026-05-02 deferral 触发 #1 production launch**） |
| 已 ack hard cap | 90 天 (2026-08-02) | 距今 75 天，越来越近 |
| 同 root cause 复现 | 0 次（事故首例） | **3 次**（Aria self ×2 + truffle-hound ×1） |
| Framework gap 论据 | 仅理论 | Issue #107 + 今日实测 dogfood |
| Rotation 成本 | 30min owner time + 1 次 hermes restart | 30-45min owner time + Luxeno 余额充值（独立任务） |
| Plugin 升级成本 | 未估 | Mid scope ~3-4h，下一 cycle |

**ROI 已经 inverted**：继续 deferral 的"省 30min owner time"在第三次复现的语境下不再合理；framework default-on 的 onboarding 价值 + 跨项目复用价值远超实施成本。

### §6.2 为什么选 Mid scope 而非 Full

- Min 不够：装上但没有"如何检测既有项目是否已装"的路径，老项目仍需 manual install
- Full 太多：rollout playbook + governance chart 是好东西但不是 ship blocker
- Mid 卡在"装 + 检测"二齿，是最小可治理化的范围

### §6.3 为什么不在本 session 实施

- Phase B 主线（M5 deploy）还有 B.5-B.9 未完成（Luxeno 余额阻塞中）
- Plugin 升级是跨 repo 工作（aria-plugin + standards + 测试 + CHANGELOG + multi-remote push），与 M5 deploy 是不同 cycle 节奏
- 实证 Q1 需要一个 throw-away test plugin，session 内做粗糙、下一 cycle brainstorm 段做扎实

---

## §7 触发条件（本决议的回顾点）

| 条件 | 监控点 |
|------|--------|
| Layer 1 rotation 完成 (R1-R5 全部 done + R4 验证 keys-only ok) | 本 session 内 (owner 充值 + 准备临时文件后) |
| Layer 2 hook commit 到 Aria 主 repo | 本 session 末 |
| Layer 3 Spec 启动 | 下一 cycle 入口 `aria:state-scanner` |
| Plugin v1.23.0 ship | 下一 cycle 末 (~2026-05-23) |
| Issue #84 + #107 close 评论 | Plugin v1.23.0 ship 后 |
| `/root/.hermes/.env` 中 4 个 2026-05-02 leak 名单 keys 轮换 | M5 Phase C ship 后 OR 2026-08-02 hard cap 前（whichever first） |

---

## §8 跨引用

- **Predecessor decision**: [`2026-05-02-secret-rotation-deferred.md`](2026-05-02-secret-rotation-deferred.md) — 4 keys deferral (status 改 `Trigger #1+#3 fired 2026-05-20`)
- **Rule #7**: `standards/conventions/secret-hygiene.md` — Source-of-truth for secret-hygiene 行为规范
- **CLAUDE.md Rule #7**: 项目根 CLAUDE.md 已含 (本决议未改 CLAUDE.md 文字, 因 Rule #7 已 cover 此场景；plugin v1.23.0 ship 后可考虑在 Rule #7 加 "default-on enforcement via aria-plugin")
- **SilkNode upstream**: PR #429 commit `8eef709` (secret-guard v1.2)
- **Forgejo Issues**:
  - [#84](https://forgejo.10cg.pub/10CG/Aria/issues/84) — Path 3 hook follow-up (open)
  - [#107](https://forgejo.10cg.pub/10CG/Aria/issues/107) — silknode 提议 aria framework default (open)
  - [#78](https://forgejo.10cg.pub/10CG/Aria/issues/78) — 2026-05-06 truffle-hound 起源 (closed via Path 1 docs)
- **Phase B handoff**: 待 B.9 写 (`docs/handoff/2026-05-20-m5-phase-b-deploy-done.md`)
- **Memory entries to amend** (下次 session memory sweep):
  - `project_secret_rotation_deferred_2026-05-02.md` → status `Trigger #1+#3 fired 2026-05-20`
  - `feedback_nomad_inspect_secret_leak.md` → extend 覆盖 `nomad var get -out=json` (read-side 同样适用)
  - NEW: `feedback_secret_guard_plugin_upstream_dogfood.md` — Lab 跨项目 R&D 复用模式（SilkNode 先做 + Aria 跟做 + plugin 上游 = single source-of-truth）
  - NEW: `project_glm_routing_luxeno_v2.md` 或 amend existing → 修正 "glm-4.7-flashx" → "glm-4.7"（fallback 实际不带 -flash 后缀）

---

**Created**: 2026-05-20 by AI Phase B.5 rotation session
**Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7 (1M context) with explicit owner sign-off
**Status**: Layer 2 done; Layer 1 in-progress; Layer 3 decided (next-cycle Spec)
