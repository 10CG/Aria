# aria-2.0-m2-layer1-state-machine — Aria 2.0 M2 Layer 1 状态机 + Hermes Extension

> **Level**: Full (Level 3 Spec)
> **Status**: **Approved** (Phase A.1 起草 + post_spec audit PASS_WITH_WARNINGS + OD-8 锁定预算 156h, 2026-04-28)
> **Created**: 2026-04-28
> **Approved**: 2026-04-28 (owner sign-off, Status: Draft → Approved)
> **Parent Story**: [US-022](../../../docs/requirements/user-stories/US-022.md)
> **Target Version**: v2.0.0-m2
> **Source**:
>   - [Brainstorm conclusion 2026-04-27](../../../.aria/decisions/2026-04-27-us022-state-machine-brainstorm.md) — OD-1~OD-7 owner 锁定
>   - [PRD v2.1 §M2 (lines 159-174)](../../../docs/requirements/prd-aria-v2.md)
>   - [M0 Spike Report](../../../openspec/archive/2026-04-16-aria-2.0-m0-spike-hermes/spike-report.md) — Option C POC 13/13 tests
>   - [M1 handoff schema v1.0](../../../aria-orchestrator/docs/m1-handoff.yaml)
>   - [silknode-integration-contract](../aria-2.0-silknode-integration-contract/proposal.md) — 契约 1 verbatim 消费
> **Forgejo Issue**: _Pending creation T0_
> **Related**:
>   - **前置 (硬门控)**: [US-021 / aria-2.0-m1-mvp](../../archive/2026-04-23-aria-2.0-m1-mvp/) — `e2e_demo_passed=true` (2026-04-23 已满足)
>   - **后继**: US-023 (M3 双 provider + Crash recovery + Reconciler)
> **Owner Decisions**: OD-1 (PRD 命名) / OD-2 (验收 B 弱形式) / OD-3 (silknode→GLM) / OD-4 (patch 推 A.1) / OD-5 (6 项 M2 必做) / OD-6 (单文件输出) / OD-7 (146h 裁 M2-15, **superseded by OD-8**) / **OD-8 = a (156h 新基线, 2026-04-28)** / **OD-9 (silknode→Luxeno reframe, 2026-05-02)** / **OD-10 (T1 实施偏离 AD3 finding + 修复路径锁定 [A], 2026-05-02; AD-M2-7 回填)**

> ⚠️ **OD-10 finding 2026-05-02**: T1 实施 (Phase B.2 startup) 的 aria-layer1 plugin 包结构偏离 AD3 Option C "pip entry-point" 路径 — 用了自创 `plugin.json` 格式而非 hermes 标准 `plugin.yaml` + `pyproject.toml` entry-point + `register(ctx)`。`_register_with_hermes_scheduler` 是 NotImplementedError dead code, T1.7 DEPLOYMENT.md 基于 docker / heavy-1 错误前提 (实际 hermes 以 raw_exec 跑在 light-1)。修复路径已锁定 Option A (严格修, 详见 [.aria/decisions/2026-05-02-od-10-...](../../../.aria/decisions/2026-05-02-od-10-t1-ad3-deviation-finding.md) + AD-M2-7 在 architecture-decisions.md)。214 unit tests pass 不能覆盖此偏移, 因为单元测试 mock 掉了 hermes 加载路径。T1.1 / T1.3 / T1.7 已 reopened; T1.2 / T1.4 / T1.5 / T1.6 (状态机内部逻辑) 保持 done。

> **silknode contract 消费声明 (per silknode-integration-contract §Acceptance 第 1 项)**: 本 Spec verbatim 引用 silknode-integration-contract §契约 1 全文 (silknode-integration-contract proposal.md line 31-40, 见本 Spec §What 六 6.1), 满足该 Spec §Acceptance line 99 第一项 checkmark。S2_DECIDE / S3_BUILD_CMD / S6_REVIEW 三个 LLM 调用状态依此契约保证 no-storage 透传。

## Why

US-021 M1 (2026-04-23 done) 已证明 Layer 2 容器路径可工作: registry push + Nomad parameterized dispatch + Forgejo PR 闭环 + DEMO E2E (`e2e_demo_passed=true`, 5/5 + 8/9 SUCCESS, p50 baseline 已建立)。但 M1 是**手动 dispatch** — owner 跑脚本触发, 不是 "Aria 自动看到 Issue 自己处理"。

M2 的核心价值: 把 "owner 触发" 升级为 "Aria 自动 tick + 状态机驱动 dispatch", 是 Aria 2.0 从 demo 到 "可运营基础设施" 的关键跃迁。

具体变化:

| 维度 | M1 (手动) | M2 (状态机) |
|------|-----------|-------------|
| 触发方式 | `dispatch-issue.sh DEMO-001` | cron 60min tick + 状态机自动派发 |
| Layer 1 | 不存在 (脚本) | Hermes Extension plugin (Option C, 0 hermes core 修改) |
| 状态持久化 | 无 (一次性脚本) | SQLite WAL `dispatches.db` (跨 tick 可恢复) |
| 失败处理 | bash 退出 | S_FAIL 终态 + reason enum (forensic 字段为 M3 reconciler 铺路) |
| 人类介入 | 全程 owner 手动 | 仅 S7_HUMAN_GATE Feishu webhook 通知 (M2 桩, M4 完整 ack) |
| LLM 调用 | M1 改走 Anthropic 直连 | **回到 silknode 代理路径** (Q1+Q1.5 决议: silknode OAI baseURL → GLM-air, fallback flashx) |

**为什么 M2 改走 silknode 而非延续 M1 Anthropic**: 这是 brainstorm Q1 + Q1.5 owner 决议 (2026-04-26~27): silknode 同时暴露 OAI + Anthropic 兼容 baseURL, 模型切换 = 改 model 参数, 不改 SDK/auth/客户端代码。M2 用 OAI → GLM-air 启动状态机 dogfooding, M3 (US-023) 启用 Anthropic baseURL 形成真双 provider。silknode-integration-contract 契约 1 (no-storage 硬约定) 在 M2 即被代码级消费, 不再仅文档声明。

**M2 出 scope 时的 deliverable**: Aria 能在 cron tick 期间自动派发 ≥10 个 synthetic issue (M1 fixture 复用), 全程不要 owner 手动触发 dispatch; LLM 流量 100% 走 silknode (Aria 客户端直连 silknode OAI baseURL, 不走 Anthropic / 不走智谱直连); 失败有可追溯的 reason 字段供后续 M3 reconciler 消费。

## What

### 一、状态机 (10 状态 + S_FAIL)

**命名权威 (per OD-1)**: 采用 PRD §M2 命名 (S0_IDLE…S9_CLOSE + S_FAIL); AD5 line 399 + 451-453 由本 Spec 配套 patch 对齐 (见 §Patches)。

**约定偏离声明 (per Phase A.1 followup R3-OBJ-3)**: PRD §M2 状态命名采用 SCREAMING_SNAKE_with_underscore (如 `S0_IDLE`), 偏离 Aria/OpenSpec snake_case 约定。OD-1 锁定保留, AD5 patch 时一并记录 rationale (frozen architecture decision precedence over convention purity)。

| State | 名称 | 类型 | 含义 | 角色映射 (per AD-M0-9) |
|-------|------|------|------|------------------------|
| S0_IDLE | 等待 | 起点/可重入 | cron 60min tick 等待 | 系统 |
| S1_SCAN | 扫描 | 普通 | heartbeat + triage (确定性规则, 不调 LLM) | 系统 |
| S2_DECIDE | 决策 | 普通 (LLM) | 是否派发 + 目标 issue 选择 | LLM (silknode→GLM-air) |
| S3_BUILD_CMD | 构建命令 | 普通 (LLM) | 生成拟人 dispatch 命令 | LLM (silknode→GLM-air) |
| S4_LAUNCH | 派发 | 普通 | Nomad parameterized dispatch + 记 alloc_id | 系统 |
| S5_AWAIT | 等待执行 | 普通 (跨 tick) | poll Nomad alloc, 可持续多个 cron tick | 系统 |
| S6_REVIEW | 评审 | 普通 (LLM) | 评审 Layer 2 结果 (代码质量 + 越界 + acceptance) | LLM (silknode→GLM-air) |
| S7_HUMAN_GATE | 人类门控 | 普通 (M2 桩) | Feishu webhook 发送 + cron tick 轮询 PR merge 状态 (block-until-PR-merge, 无 auto-pass); M4 加 webhook ack 监听 | **owner 单角色 (continues AD-M0-9)** |
| S8_MERGE | 合并 | 普通 | 确定性 git merge + Forgejo API | 系统 |
| S9_CLOSE | 归档 | 终态 | OpenSpec archive + CHANGELOG + 清理 | 系统 |
| S_FAIL | 失败 | 终态 (universal sink) | 任意 S2-S6/S8 异常进入; M2 不重试 (M3-1 retry policy) | 系统 + 人工 forensic |

**S7_HUMAN_GATE 阻塞行为 (per Phase A.1 followup R3-OBJ-5)**: 默认 block-until-PR-merge, 无 auto-pass timeout (M2)。M4 (US-024) 加 ack 监听后才有真正放行/超时语义。

**M0 Spike POC → M2 状态映射 (per Phase A.1 followup R3-OBJ-cm-1)**:

POC (5 状态, 286 LoC) 与 M2 生产 10 状态映射:

| POC 状态 | M2 状态 | 增量说明 |
|----------|---------|----------|
| PENDING | S0_IDLE | 直接对应 (cron 等待) |
| — (无对应) | S1_SCAN | **新增**: heartbeat + triage 确定性规则 |
| — (无对应) | S2_DECIDE | **新增**: LLM 决策派发哪个 issue |
| — (无对应) | S3_BUILD_CMD | **新增**: LLM 生成拟人命令 |
| RUNNING | S4_LAUNCH + S5_AWAIT | **拆分**: dispatch 动作 vs 跨 tick poll |
| SUCCESS (合并到这里) | S6_REVIEW | **新增**: LLM 评审 + acceptance |
| — (无对应) | S7_HUMAN_GATE | **新增**: 人类门控 (M2 桩) |
| — (无对应) | S8_MERGE | **新增**: 确定性 merge |
| SUCCESS | S9_CLOSE | 对应 (终态归档) |
| FAILED | S_FAIL | 对应 (terminal sink) |
| TIMEOUT | S_FAIL with reason=timeout | 折叠 (M3-4 拆分细分) |

**LoC 增量重算**: POC 286 LoC → M2 5 个新增 + 1 个拆分, 增量预算 ~150-275 LoC (从原 AD5 估 100-200 上调 ~25%)。

### 二、状态字段最小集 (per OD-5 全 6 项 + cr R1 OBJ-4)

`dispatches.db` SQLite WAL mode 表 schema (M2 v1.0):

```sql
CREATE TABLE IF NOT EXISTS dispatches (
  -- 主键 + idempotency (OD-5a)
  issue_id              TEXT NOT NULL,
  dispatch_id           TEXT NOT NULL,    -- hash(issue_id || attempt_count), Nomad meta idempotency_token
  attempt_count         INTEGER NOT NULL DEFAULT 1,

  -- 状态 + 时间戳
  state                 TEXT NOT NULL,    -- enum: S0_IDLE | ... | S9_CLOSE | S_FAIL
  state_entered_at      TEXT NOT NULL,    -- ISO8601 UTC
  last_heartbeat_at     TEXT,             -- 用于 S3/S5/S6 timeout 判定

  -- 输入契约 (R7 / AD-M1-2)
  prompt_path           TEXT,             -- bind mount 路径, size ≤ 128 KiB (R7 hard cap)
  image_sha             TEXT NOT NULL,    -- 来自 m1-handoff.yaml.image_refs.image_sha_final (AD-M1-2 immutable pin, 拒绝 image_tag_mutable)
  alloc_id              TEXT,             -- Nomad alloc_id (S4 后填)

  -- 失败 forensic (OD-5c, M2 不重试但留字段为 M3 reconciler)
  fail_reason           TEXT,             -- enum (见下)
  fail_detail           TEXT,             -- 自由文本 + 可选结构化 JSON
  failed_from_state     TEXT,             -- 进入 S_FAIL 前的状态

  -- LLM cost 跟踪 (OD-5d, US-027 cost routing 依赖)
  token_usage_input     INTEGER DEFAULT 0,
  token_usage_output    INTEGER DEFAULT 0,
  token_cost_usd        REAL DEFAULT 0.0,
  model_used            TEXT,             -- 实际命中的 model (glm-4.5-air | glm-4.7) — OD-9 reframe 2026-05-02

  -- S7 人类门控通知 (F3 fix: 原 SQL 缺失此字段; schema.sql 已含, 本文档补齐)
  -- notification_status: Feishu webhook HTTP 响应码或错误字符串
  -- 值域: NULL (未发送) | "200" | "5xx" | "network_error"
  -- 非 2xx 仅 log warning, 不触发 S_FAIL (per qa R1 OBJ-6 / T12.3)
  notification_status   TEXT,

  -- Fallback 跟踪 (OD-5e, AD-M0-8 主/fallback 非对称)
  fallback_triggered    INTEGER DEFAULT 0,  -- bool
  fallback_chain_json   TEXT,             -- JSON: [{model, trigger_reason, latency_ms, endpoint_from, endpoint_to}, ...]

  -- M3 retry forensic (M2 = 0, M3 incrementable)
  retry_count           INTEGER DEFAULT 0,

  PRIMARY KEY (issue_id, dispatch_id)
);

-- OD-5a idempotency: 同一 issue 只能有一个非终态 dispatch
-- 注意: SQLite 不支持 inline `UNIQUE (col) WHERE ...` constraint, 必须用独立 CREATE UNIQUE INDEX (qa KI-1 Phase B startup 实测发现)
CREATE UNIQUE INDEX uq_issue_active_partial
  ON dispatches (issue_id)
  WHERE state NOT IN ('S_FAIL', 'S9_CLOSE');

CREATE INDEX idx_state ON dispatches(state);
CREATE INDEX idx_state_entered ON dispatches(state_entered_at);
```

**fail_reason enum (OD-5c, 10 值)**:
- `quota_exhausted`: silknode 返回 429, GLM token 配额耗尽
- `provider_5xx`: silknode/GLM 持续 5xx (单次请求 OpenAI SDK 内重试 3 次仍失败)
- `timeout`: S3/S5/S6 LLM call > 120s 或 alloc heartbeat > 30min (M3-4 拆分细分)
- `schema_invalid`: Layer 2 输出 JSON schema 校验失败
- `container_crash`: alloc exit code != 0 + 无结果文件
- `dispatch_lost`: Nomad alloc lost / OOM kill 等基础设施级失败
- `review_rejected`: S6 LLM 评审给出 negative verdict
- `infrastructure`: 其他基础设施错误 (网络 / 文件系统 / Forgejo API)
- `partial_write`: M2 监控路径 — 状态 transition 中途写入中断 (M2-15 mitigation brainstorm 引用; M3-2 完整 crash recovery 实施)
- `other`: 兜底未分类

**fallback_chain_json 字段 schema (per Phase A.1 followup R3-OBJ-4; OD-9 reframe 2026-05-02 model names)**:

注: T8 实施时简化为 `["{model}:ok"|"{model}:fail:{reason}", ...]` 字符串数组 (compact form, audit log 友好). 完整对象形式保留为可选扩展, 当前实现取 compact form。

```json
[
  {
    "model": "glm-4.5-air",
    "trigger_reason": "primary_fail_429",
    "latency_ms": 1234,
    "endpoint_from": "luxeno-oai/v1/chat/completions",
    "endpoint_to": "luxeno-oai/v1/chat/completions",
    "model_switched_to": "glm-4.7"
  }
]
```

### 三、Timeout 路径 (per OD-5b)

| Source state | Trigger | Target | Reason |
|--------------|---------|--------|--------|
| S2_DECIDE | LLM call > 120s (含 OpenAI SDK 内 3 次重试) | S_FAIL | `timeout` |
| S3_BUILD_CMD | LLM call > 120s | S_FAIL | `timeout` |
| S4_LAUNCH | Nomad dispatch ack > 30s | S_FAIL | `dispatch_lost` |
| S5_AWAIT | alloc last_heartbeat_at > 30min (env: HERMES_ALLOC_TIMEOUT_MIN, 默认 30, 可在 Hermes 部署时覆盖) | S_FAIL | `timeout` |
| S6_REVIEW | LLM call > 120s | S_FAIL | `timeout` |
| S7_HUMAN_GATE | (M2: 无超时, block-until-merge); M4: webhook ack > 7d | (M4 only) S_FAIL | `human_timeout` |
| S8_MERGE | Forgejo API > 30s | S_FAIL | `infrastructure` |

**实施期 escalation matrix (per Phase A.1 followup R3-OBJ-cm-4)**:
- S_FAIL retry 次数上限: 0 (M2 不重试, 进入 S_FAIL = 终态)
- silknode 不可用降级: 单次请求级 (OAI SDK 3 次 expo backoff) + 状态机级 (3 次连续 5xx → owner Feishu 紧急通知, 但仍不重试)
- S6 review 持续 LOW (review_rejected ≥ 5 / 24h): 触发 owner 介入审查 prompt 模板或 Layer 2 输出格式

### 四、Idempotency 策略 (per OD-5a + qa R1 OBJ-2)

**S0_IDLE → S1_SCAN guard**: 启动每次 tick 前先查 `SELECT issue_id FROM dispatches WHERE state NOT IN ('S_FAIL', 'S9_CLOSE')`, 跳过已有 active dispatch 的 issue。

**S1_SCAN UNIQUE 约束**: SQLite `UNIQUE (issue_id) WHERE state NOT IN ('S_FAIL', 'S9_CLOSE')` 物理保证同一 issue 不能有两条 active 记录, INSERT 冲突时跳过本次 (cron tick 重入安全)。

**S4_LAUNCH Nomad meta idempotency_token**: `dispatch_id = SHA256(issue_id || attempt_count)`, 通过 `nomad job dispatch -meta IDEMPOTENCY_KEY={dispatch_id}` 传递, Nomad 侧重复 dispatch 自动去重。

**S8_MERGE Forgejo PR idempotency**: PR 评论使用幂等 marker `[aria-dispatch:{dispatch_id}]`, Forgejo 侧已有评论则跳过。

### 五、并发保护 (per OD-5f + qa R1 OBJ-5 cron tick 重叠 TOCTOU)

**机制**:
1. **进程级 advisory lock**: cron tick 启动前 `flock -n .aria/cache/hermes-tick.lock`, 已锁则跳过本次 tick (避免双 tick 重叠)
2. **SQLite 事务级**: 每次状态 transition `BEGIN EXCLUSIVE` + `COMMIT`, 防止读 → 计算 → 写中的 race
3. **冲突日志**: tick 跳过事件落 audit trail (`.aria/audit-reports/cron-tick-skip-{ts}.log`), owner 可观测

### 六、外部依赖契约

#### 6.1 silknode 集成契约 (verbatim, per OD-3 + silknode-integration-contract §契约 1 line 31-40)

> **silknode 代理 (Luxeno 品牌) 在 Aria 2.0 架构中必须保持 "API 调用透传, 不落地存储" 的行为**:
>
> - **禁止**: 在 silknode 侧对 issue body / code diff / Aria prompt / GLM response 进行任何形式的持久化 (磁盘日志 / 内存缓存 > 单次请求生命周期 / 数据库存储 / 审计日志保留)
> - **允许**: 单次请求生命周期内的内存缓冲区 (用于协议转换 / 格式适配 / 错误重试)
> - **允许**: 指标级 meta 日志 (请求次数 / 延迟 / 错误码), 前提是不含 request/response payload 内容
> - **可追溯**: 若 silknode 新增任何落地行为, **必须**触发 r1-legal-memo v1.1 失效条件, 重新评估 IS-3/IS-4 并更新 Memo 至 v2.0+

**消费规则 (M2 实施期, OD-9 reframe 2026-05-02)**:
- M2 LLM 调用 (S2/S3/S6) 100% 经 **Luxeno OAI baseURL** `https://api.luxeno.ai/v1/chat/completions` (env: `LUXENO_BASE_URL`, key: `LUXENO_API_KEY`). **不**走 silknode-gateway (Portkey, 内置 key 已过期 + caller 仍需自带 key), **不**直连 `api.bigmodel.cn` (会触发 pay-per-token 计费). Luxeno 是 silknode 项目的运营品牌 (10CG 自有, R1 Legal Memo IS-3 cover), 走 coding-plan 订阅。
- 主 model: **`glm-4.5-air`** (M1 已实战, thinking model, 需 max_tokens ≥ 2000); fallback model: **`glm-4.7`** (旗舰, S6_REVIEW 高质量兜底). 排除 `glm-4.7-flash` (RPM 限制风险) 与 `glm-4.7-air` (不存在). 与 AD-M0-8 主/fallback 非对称设计意图一致 (主便宜稳定 / fallback 高质量).
- Aria 客户端 SHOULD NOT 在 prompt 内 inline secrets/PII (T2 静态 lint rule 检查)
- HTTP client 必带 `User-Agent: aria-orchestrator/...` header (Cloudflare 1010 防御 — 默认 Python-urllib UA 被 block)
- S6_REVIEW 同一 dispatch_id 内 review prompt hash 命中可复用 cache (Aria 侧), 跨 dispatch 不复用

#### 6.2 Nomad meta 边界 (R7 / T2.4 hard cap)

- `nomad job dispatch -meta` 单 key 上限 = **131048 bytes (128 KiB hard cap, T2.4 实测)**
- prompt 走 bind mount 文件 (`prompt_path`), meta 仅传 `ISSUE_ID + DISPATCH_ID + PROMPT_PATH`
- Hermes 客户端断言 (per T2.4 §6.2): dispatch 前 `assert len(meta_value) < 100 KB`, 失败立即 S_FAIL with `reason=infrastructure`
- 错误分诊: 监听 Nomad 错误字符串 `"meta key value exceeds maximum"` (per T2.4 §6.3, 否则 silent failure)

#### 6.3 Image refs (AD-M1-2 / TL-R3-4)

- `dispatches.image_sha` 字段必填且 = m1-handoff.yaml `image_refs.image_sha_final` 值 (M1 实际为短 SHA 如 `5154c13`, 非完整 sha256:[a-f0-9]{64} 格式)
- M2 dispatch 时强制使用 `m1-handoff.yaml.image_refs.image_sha_final`, **禁** 引用 `image_refs.image_tag_mutable` (claude-latest)
- S4_LAUNCH guard: 启动前 `assert image_sha == m1_handoff.image_refs.image_sha_final else S_FAIL(reason=infrastructure)`; image_sha 长度/格式校验 in T11.2 实施期 owner 决定 (full sha256 vs 短 SHA, M1 现状是短 SHA `5154c13`)

#### 6.4 M1 handoff 输入契约 (additive-only, per AD-M1-7)

> **Field name verified 2026-04-28** against `aria-orchestrator/docs/m1-handoff.yaml` v1.0 actual schema. 旧 brainstorm 引用 (`immutable_sha`/`mutable_tag`/`nomad_job_id`/`host_volumes`/`demo_002_p50_duration_s`) 已校正。

M2 消费 m1-handoff.yaml v1.0 字段 (read-only, 不修改 schema):

- **镜像选型** (per AD-M1-2 / TL-R3-4 immutable pin):
  - `image_refs.registry` = `forgejo.10cg.pub/10CG/aria-runner`
  - `image_refs.image_sha_final` ← **immutable SHA, M2 dispatch 时 pin 此字段**
  - `image_refs.image_tag_immutable_pattern` (`aria-runner:claude-<sha>`) ← M2 解析 `<sha>` 占位符为 `image_sha_final`
  - `image_refs.image_tag_mutable` (`aria-runner:claude-latest`) ← **禁** M2 dispatch 引用 (per AD-M1-2)

- **Nomad 配置** (per M1 deployment infrastructure):
  - `nomad_config.job_template_path` ← M2 Hermes Extension 复用此 HCL template
  - `nomad_config.host_volume_config_path` ← host volume 挂载配置
  - `nomad_config.volumes[]` ← 数组, 含 `aria-runner-inputs` + `aria-runner-outputs` 三节点卷

- **Performance 基线** (M2 验收 D non-regression 数据源):
  - `performance_baseline.dispatch_to_pr_p50_s` = 28 ← **M2 验收 D 基线**: m2 实测 p50 ≤ 28 × 1.5 = 42s
  - `performance_baseline.dispatch_to_pr_p95_s` = 95 ← 辅助参考
  - `performance_baseline.heavy_node_alloc_success_rate` = 1.0 ← 基础设施可用性

- **Token cost 基线** (M2 cost 对比, US-027 数据源):
  - `demo_token_usage.DEMO-001.{input_tokens_total, output_tokens_total}`
  - `demo_token_usage.DEMO-002.{input_tokens_total, output_tokens_total}`
  - M2 实测 token 数应在 ±2x 范围 (Anthropic vs GLM 对比, AD-M1-12 Luxeno pivot 影响)

- **Legal 前提** (per M1 carryover):
  - `legal_assumptions.luxeno_data_cleared` = true ← M2 silknode 路径合规依赖
  - `legal_assumptions.m1_memo_signed` = true ← M2 启动前提

M2 产出 m2-handoff.yaml v1.0 (additive-only, schema_version="1.0"), 新增段 `m2_dispatches/*` (state machine metrics + handoff 给 US-023 M3)。

### 七、Acceptance (验收标准)

**A. cron tick 自动 dispatch**
- 60min cron tick 期间, Hermes Extension 自动派发 ≥ 10 个 synthetic issue (复用 M1 fixture DEMO-001/002 + 8 个 variants)
- 全程不需要 owner 手动触发 `dispatch-issue.sh`
- 每个 issue 状态机走完 S0 → S9_CLOSE 或 S_FAIL

**B. SQLite 状态持久化 (per OD-2 弱形式)** ← v1.0 已降级
- SQLite WAL mode 启用, dispatches.db 在 Hermes 进程重启后状态可读 (state 字段不丢失)
- 不丢已 dispatched 记录 (kill -9 Hermes 进程后, 重启可看到所有 SQLite rows 完整)
- **不要求**: 完整 reconciler / replay / orphan alloc 清扫 / crash-mid-transition recovery (这些 M3-2 deferred)

**C. M2 handoff validator PASS**
- m2-handoff.yaml 通过 `aria-orchestrator/scripts/validate-m2-handoff.py` 验证
- 继承 m1-handoff.yaml additive-only 规则 (新增 `m2_dispatches/*` 段, 不改 m1 段)

**D. Performance non-regression**
- `m2_demo_002_p50_duration_s ≤ m1_demo_002_p50_duration_s × 1.5` (per QA-M2)
- 状态机 overhead 不应导致单 issue dispatch 时长突破 1.5x

**E. silknode contract 消费验证**
- M2 实施期所有 LLM 调用 (S2/S3/S6) 验证经 silknode baseURL (Aria 客户端日志可追溯)
- silknode-integration-contract §Acceptance 第一项 checkmark 满足 (本 Spec verbatim 引用契约 1)

**F. Owner sign-off**
- 产品负责人 (10CG Lab solo per AD-M0-9) 签字确认 Go/No-Go (per M0 sign-off 模板)

### 八、核心交付一致性声明 (F3-cr: tasks ↔ US-022 §核心交付 + OD-5 mapping)

本 Spec tasks.md 的 17 个任务组与 US-022 §核心交付 6 项 + OD-5 6 项 + OD-3 LLM review 的映射关系:

| tasks.md 任务组 | 对应 §核心交付 / OD 条目 |
|-----------------|--------------------------|
| T0–T1 (Spec + scaffold) | 前置: US-022 §验收 F (owner sign-off) 准入条件 |
| T2 (SQLite WAL schema) | US-022 §核心交付 2: 状态持久化 + OD-5b schema |
| T3 (Transition logic) | US-022 §核心交付 1: 状态机 10 状态 + OD-5a/f 并发 + OD-5b timeout |
| T4 (Timeout + forensic) | US-022 §核心交付 3: 失败处理 + OD-5b timeout + OD-5c forensic 字段 |
| T5 (Idempotency) | US-022 §核心交付 4: cron 重入安全 + OD-5a idempotency |
| T6 (Cron scheduler) | US-022 §核心交付 1: 自动 cron 60min tick 触发 |
| T7 (Nomad dispatch) | US-022 §核心交付 1: S4_LAUNCH Nomad parameterized dispatch |
| T8 (silknode LLM) | US-022 §核心交付 5: LLM 100% 走 silknode + OD-3 (silknode→GLM) |
| T9 (m1-handoff 消费) | US-022 §核心交付 6: m1-handoff additive-only 消费 (AD-M1-7) |
| T10 (S6 LLM review) | OD-3 LLM review (S6_REVIEW state) + US-022 §验收 E silknode contract |
| T11 (image SHA guard) | US-022 §核心交付 6 + AD-M1-2 immutable pin enforcement |
| T12 (S7 Feishu webhook) | US-022 §核心交付 1: S7_HUMAN_GATE notification stub |
| T13 (S8 Forgejo merge) | US-022 §核心交付 1: S8_MERGE deterministic merge |
| T14 (DI + unit tests) | US-022 §验收 A: cron dispatch ≥10 synthetic issues (test coverage) |
| T15 (E2E validation) | US-022 §验收 A/B/C/D: end-to-end acceptance criteria |
| T16 (m2-handoff + validator) | US-022 §验收 C: m2-handoff.yaml + validate-m2-handoff.py |
| T17 (M2 Report + archive) | US-022 §验收 F: owner sign-off + Phase D closure |

OD-5 6 项完整覆盖:
- OD-5a (idempotency) → T3 guard + T5
- OD-5b (timeout) → T3 S5_AWAIT + T4
- OD-5c (forensic fields) → T4 + schema.sql
- OD-5d (LLM cost tracking) → T8 + schema.sql
- OD-5e (fallback tracking) → T8 + schema.sql
- OD-5f (advisory lock) → T3.3 TickLock + T6

### 九、Patches (per OD-4, T6 阶段实施)

本 Spec 起草过程产出以下 3 个 patch (推到 T6 M2 Report 阶段, 与 m2-handoff.yaml 一同提交):

#### Patch 1: AD5 (`aria-orchestrator/docs/architecture-decisions.md`)

- Line 399: `9 正常状态 + S_FAIL` → `10 正常状态 + S_FAIL` ; 状态名重写为 PRD §M2 命名 (`S0_IDLE → S9_CLOSE`)
- Line 451-453: mapping table 重做 (POC 5 状态 → M2 10 状态, LoC 增量 100-200 → 150-275)

#### Patch 2: PRD `docs/requirements/prd-aria-v2.md`

- §M2 line 159: 标题 `9 states + S_FAIL` → `10 states + S_FAIL`

#### Patch 3: US-022 `docs/requirements/user-stories/US-022.md`

- Line 78 (验收 B): `通过 crash recovery 测试 (kill alloc + 重启可恢复)` → `SQLite WAL 持久化 + 进程重启后状态可读 + 不丢已 dispatched 记录 (完整 reconciler 推 M3)`
- Line 87 (§不在范围): `Crash recovery + Replay + Reconciler → US-023 (M3)` → `Crash recovery 完整 reconciler + Replay + 主动 orphan 清扫 → US-023 (M3); M2 仅做 WAL persist 弱形式`

## Impact

### 直接影响

- **M2 工时锁定 146h** (per OD-7 = b, 裁 M2-15 partial-write 6h)
- **silknode contract Spec 状态推进**: 本 Spec verbatim 消费契约 1 后, silknode-integration-contract 满足 §Acceptance 第一项 (US-022 起草时 verbatim 引用), 离归档前进一步
- **M1 → M2 input 契约首次实证**: m1-handoff.yaml v1.0 在 M2 实施期被消费, AD-M1-7 additive-only 规则受首次跨 milestone 检验
- **Hermes Extension 在 10CG Lab 内首次 production 部署**: M0 仅 POC, M2 是真 cron 跑

### 不变更

- **不变更**: 已归档的 M0/M1 任何 Spec / handoff / artifact (read-only consumer)
- **不变更**: silknode 仓库代码 (M2 仅消费契约, 不审计 silknode 实现, 见 silknode-integration-contract §Out of Scope)
- **不变更**: aria-plugin (M2 是 aria-orchestrator 单仓变更, aria submodule pointer 仅在最终 release 时 bump)

### 治理影响

- **silknode contract Acceptance 部分满足**: 本 Spec 是该 contract 4 项 acceptance 中第 1 项的实施载体
- **r1-legal-memo IS-3/IS-4 假设代码级锚定**: M2 LLM 流量第一次真实流过 silknode 路径, IS-3 (no-storage 透传) 不再仅声明而是 production 验证
- **PRD §M2 first-time patch**: 本 Spec 是 PRD v2 §M2 的首个实施级消费者, 暴露 PRD line 159 标题 bug → patch (Patch 2)

## Acceptance (本 Spec 自身的验收 ≠ M2 deliverable 验收)

本 Spec 起草后的形式验收:

- [ ] **Phase A.1 完成**: proposal.md + tasks.md + 3 patches 全部产出
- [ ] **Brainstorm conclusion 全部 19 sections 消化**: OD-1~OD-7 / state_fields / timeout / idempotency / silknode / Q1+Q1.5 / R3 phase_a1_followup 7 项 全部映射到 Spec 章节
- [ ] **Phase A.1 followup 7 项落地**: R3-OBJ-3 (SCREAMING_SNAKE 备注) / R3-OBJ-4 (fallback log schema) / R3-OBJ-5 (S7 阻塞行为) / R3-OBJ-cm-1 (POC mapping) / R3-OBJ-cm-2 (S7=owner) / R3-OBJ-cm-3 (R7 prompt 128 KiB) / R3-OBJ-cm-4 (escalation matrix) — 全部在本文件可 grep 验证
- [ ] **post_spec 审计** (可选, owner 决策): audit-engine 跑 convergence/challenge mode 验证 Spec 与 brainstorm conclusion / silknode-contract / m1-handoff.yaml 一致性
- [ ] **owner 签字 Status: Draft → Approved**: 准入 Phase B (开发阶段)

## Out of Scope (本 Spec 不做什么)

继承 US-022 §不在范围 + brainstorm M3 deferrals:

- ❌ **M3-1 自动 retry policy** (transient/permanent 分类) — 12h, US-023 实施
- ❌ **M3-2 完整 crash recovery + reconciler + replay** (含 M2-15 partial-write 原子性) — 30h, US-023 实施
- ❌ **M3-3 silknode quota 预检接口集成** — 6h, 等 silknode 团队提供 endpoint
- ❌ **M3-4 S_TIMEOUT 拆分细分** (S_TIMEOUT_RUN / S_TIMEOUT_REVIEW) — 4h, M3 数据驱动
- ❌ **M3-5 Anthropic endpoint 启用 + 双 provider fallback** — 10h, M2 仅 OAI
- ❌ **M3-6 S_FAIL reset-issue CLI 工具** — 4h, M3 配套
- ❌ **M3-7 AD3 Option C 0 hermes core 修改 final 验证** — 3h spike, M3 ratify
- ❌ **M3-8 observability hooks (Prometheus / OTel)** — 12h, M3 配套 dashboard
- ❌ **Real / trivial-real IP DEMO** (per AD-M1-9): M2 仍 synthetic only, 与 M1 一致

## References

- [Brainstorm conclusion 2026-04-27](../../../.aria/decisions/2026-04-27-us022-state-machine-brainstorm.md) — 本 Spec 全部决议来源
- [silknode-integration-contract](../aria-2.0-silknode-integration-contract/proposal.md) — 契约 1 消费目标
- [US-022](../../../docs/requirements/user-stories/US-022.md) — Parent Story
- [PRD v2.1 §M2](../../../docs/requirements/prd-aria-v2.md) — 状态机命名权威
- [AD3 Option C Extension-only](../../../aria-orchestrator/docs/architecture-decisions.md) — Hermes 集成模式
- [AD5 状态机 9→10](../../../aria-orchestrator/docs/architecture-decisions.md) — 状态机框架
- [AD-M0-8 主/fallback 非对称](../../../aria-orchestrator/docs/architecture-decisions.md) — silknode air/flashx
- [AD-M0-9 solo lab 角色合并](../../../aria-orchestrator/docs/architecture-decisions.md) — owner 单角色
- [AD-M1-2 image_sha pin](../../../aria-orchestrator/docs/architecture-decisions.md) — immutable 强制
- [AD-M1-7 handoff additive-only](../../../aria-orchestrator/docs/architecture-decisions.md) — m2-handoff schema 治理
- [M0 Spike Report](../../../openspec/archive/2026-04-16-aria-2.0-m0-spike-hermes/spike-report.md) — 13/13 tests POC
- [m1-mvp Spec (archive)](../../archive/2026-04-23-aria-2.0-m1-mvp/) — Layer 2 deliverable, M2 input 契约源
- [m1-handoff.yaml v1.0](../../../aria-orchestrator/docs/m1-handoff.yaml) — 实体存在的 schema 文件
- [r1-legal-memo](../../../aria-orchestrator/docs/r1-legal-memo.md) — silknode no-storage 上游依据
- [T2.4 R7 meta-boundary](../../../openspec/archive/2026-04-17-aria-2.0-m0-prerequisite/artifacts/t2/t2.4-meta-boundary.md) — 128 KiB hard cap

## 版本历史

| Version | Date | Changes |
|---------|------|---------|
| 0.1 (Draft) | 2026-04-28 | 初版 (Phase A.1.1), 基于 brainstorm conclusion 2026-04-27 全部 19 sections + OD-1~OD-7 + 7 phase_a1_followup |
