# OD-9 — silknode → Luxeno endpoint reframe (T8 实施期)

> **Date**: 2026-05-02
> **Owner**: solo-lab (uni.concept.wzfq@gmail.com)
> **Spec**: aria-2.0-m2-layer1-state-machine
> **Tasks affected**: T8.1 / T8.2 / T8.3 / T8.4 / T9.2 / T10
> **Triggers**: Phase B implementation discovery (T8.3 smoke session 2026-05-02)

## Decisions

### Decision 1: Routing — silknode-gateway → Luxeno coding-plan baseURL

**From**: `https://silknode.10cg.pub/v1` (Cloudflare Access protected)
**To**: `https://api.luxeno.ai/v1` (Luxeno coding-plan subscription)

**Why**:
- silknode.10cg.pub 在 Cloudflare Access 后, 现有 CF Access service token 未授权该 application
- silknode-gateway 内网直连 (`192.168.69.82:8787`, Portkey AI Gateway) 内置的 `zhipu_api_key` (Nomad Variables) 已过期, 实测 401 "令牌已过期"
- 直配 `api.bigmodel.cn` (智谱官方) 会按 pay-per-token 计费, owner 已在 Luxeno coding-plan 订阅, 不接受 cost regression

**Implementation**:
- env vars: `LUXENO_BASE_URL` + `LUXENO_API_KEY` (key 格式 `sk-silk-*`)
- 文件名 `silknode_client.py` 保留 (Protocol naming + 历史兼容)
- `extension.py` 保留 `SILKNODE_BASE_URL` 作 second-tier env fallback (向后兼容)

### Decision 2: Primary model — glm-4.7-air (不存在) → glm-4.5-air

**Why**:
- `glm-4.7-air` 不存在于智谱催化 (4.7 系列只有 flash / flashx / 旗舰)
- 原 spec 是 brainstorm 阶段笔误, 通过 post_spec audit 时未发现
- `glm-4.5-air` 是 M1 已实战 provider, coding plan 内, 是 thinking model — 调用必须 `max_tokens ≥ 2000` 让 reasoning_tokens 完成 + content 输出

### Decision 3: Fallback model — glm-4.7-flashx → glm-4.7 旗舰

**Why**:
- 4.7-flash RPM 限制风险 (owner 实战经验)
- 4.7 旗舰在 coding plan 内, S6_REVIEW 高质量兜底
- 与 AD-M0-8 主/fallback 非对称设计意图一致 (主便宜稳定 / fallback 高质量)

### Decision 4: HTTP client — User-Agent 必填 (CF 1010 防御)

**Why**:
- T8.3 实测发现 `Python-urllib/X.Y` 默认 UA 触发 Cloudflare 1010 (访问被禁)
- 必须设置 `User-Agent: aria-orchestrator/1.0 (+luxeno-client)` 才能通过 WAF
- curl 默认 UA 也通过, 所以早期 curl probing 没触发

### Decision 5: Implementation — stdlib urllib, 不引入 openai SDK

**Why**:
- Hermes plugin 应保持轻量, 不 vendor 大依赖
- urllib 足够 + JSON 解析 + 3-attempt expo backoff (1/2/4s) on 408/429/5xx + 网络错误
- T9 不需 tiktoken: Luxeno 透传 `usage.prompt_tokens` / `usage.completion_tokens` (实测确认)

## Audit Trail

### Verification Evidence (2026-05-02)
- T8.3 live smoke: `glm-4.5-air` HTTP 200 / latency ~5s / output `'PASS'` / `fallback_chain: ["glm-4.5-air:ok"]`
- T8.3 fallback path: bogus model → 400 → fallback `glm-4.5-air` → `'OK'` / chain `["glm-bogus:fail:http_400", "glm-4.5-air:ok"]`
- T10.4 accuracy: 5/6 synthetic = 83.3% ≥ 80% target

### Reframe Documentation (per feedback_spec_reframe_in_session memory)
3 处文档化:
1. **commit messages**: `feat(layer1): T8.1/T8.2/T8.3` + `feat(m2): T8 done + OD-9 reframe`
2. **proposal.md §6.1 消费规则**: 重写为 Luxeno 路由 + UA 要求 + 模型选择 rationale
3. **tasks.md T8 reframe banner**: 三连决策 reframe note + T8.x 标记 done

### Memory Updates
- 新建: `feedback_secrets_never_in_conversation.md` (本 session 教训: secret 永不出现在对话中)
- 引用: `project_glm_routing_luxeno.md` (Luxeno = silknode = 10CG 自有 Portkey 代理)
- 引用: `reference_10cg_cluster_internal_routing.md` (CF Access 绕过模式)

## Status

- [x] OD-9 owner sign-off: 2026-05-02 (3 round dialog: routing / model selection / config security)
- [x] Implementation merged to feature/aria-2.0-m2-layer1-state-machine (e57ffe0 orchestrator, e4d606d main repo)
- [x] Pushed to origin (Forgejo) + github (双远程, SHA 4 处校验)
- [x] T8 + T10 complete; T8.4 lint rule complete
- [ ] M2 closeout (T15 + T16) — deferred to next session

## Supersedes

无 — OD-9 是新增决策, 不撤销 OD-1~OD-8。但 OD-3 ("S5/S6 review 走 silknode→GLM") 的 "silknode" 字面词在 OD-9 后等价于 "Luxeno coding-plan baseURL", 不改 OD-3 文本。
