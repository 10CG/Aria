# Aria 2.0 M6 — Layer 2 cost/model 遥测回报 + 容器模型接线统一

> **Level**: 3 (Full — 跨容器 3 执行体 [initial/changes/redo] + commit-lint + Layer 1 解析 + schema migration + cost.json 聚合 + Nomad Var 配置面)
> **Status**: **post_spec CONVERGED (待 owner 批准)** — Phase A.1 起草 2026-07-09, 据 DEC-20260709-001 v2 [4-agent 设计审议折入]; **post_spec 5-agent R1 (2C/多 I/m 全 spec-doc 层) → R1-fix → R2 (tech-lead CONVERGED / backend·qa 机械 REVISE) → R2-fix → R3 backend 0 新 CONVERGED** (报告 `.aria/audit-reports/post_spec-FINAL-1783602519132-*`)。owner 批准后 → Phase A.2/A.3 (detailed-tasks.yaml)
> **Change ID**: `aria-2.0-m6-cost-model-telemetry`
> **Parent US**: [US-026](../../../docs/requirements/user-stories/US-026.md)
> **决策 SOT**: [docs/decisions/DEC-20260709-001-layer2-cost-model-telemetry.md](../../../docs/decisions/DEC-20260709-001-layer2-cost-model-telemetry.md) (v2, owner 决策 2026-07-09 + tech-lead/backend/qa/km 4-agent code-grounded 审议 2 OBJECTION + 2 CONCERNS 折入)
> **AD 分配**: **AD-M6-13 / AD-M6-14 / AD-M6-15** (显式避开 AD-M6-10..12 双重认领区, 见 DEC §10)
> **⚠️ 串行前置**: `aria-2.0-m6-dispatch-input-delivery` — 容器侧改动 (initial.sh/Dockerfile) 与其文件级重叠 + 共享镜像重建门, 本 Spec 容器侧 Phase B 不得在 input-delivery 合并主干前开 (Layer 1 侧遥测管道可先独立推进)
> **上游**: SilkNode #830 (glm-5.2 路由解锁; phantom 契约「result.json model=glm-5.2」由本 Spec 兑现) / cost-acceptance 归档 (dual-row cost.json 契约, 本 Spec 扩展不破)

---

## Why

M6 168h 自主跑要在「**cost 维度可评分 (AC-5/AC-6)**」下发布, 需要每次自主容器 dispatch 的真实 cost/model 落进遥测。**现状: 全链丢失** (DEC §1, Explore code-grounded):

| 断点 | 现状 | 证据 |
|------|------|------|
| 传输层 | 容器 result.json 写跨节点不可读 host volume; Layer 1 只读 stderr; 容器 outcome marker 不含 cost/model | `alloc_status_provider.py:258-267` / `initial.sh:307` |
| model 源 | result.json.claude_usage 无 model; parser 弃 assistant 帧的 served model | `initial.sh:954-961` / `parse-stream-json.sh:55-67` |

结果: cost.json metered SUM 对自主跑恒 0; dispatches 里只有 Layer 1 编排调用的 cost/model (Luxeno $0 / glm-4.5-air), **容器真实工作 = 盲区**。

**且模型接线本身是笔糊涂账** (DEC §1.2, **5 处**打架): 容器 `--model smart-sonnet` (非 canonical alias) 使 2026-07-01 的 glm-5.2 opus-档 cutover **对全部 mode 结构性 inert** (`ANTHROPIC_DEFAULT_OPUS_MODEL` 从不被 honor); redo/changes 裸调无 `--model` 走 claude 默认。**没有遥测, 这类「配了没生效」永久隐身** — 这正是本 Spec 的价值: 让运行现实 (真跑什么模型/烧多少 token) 在归档与评分时可见。

**诚实前提 (审议 O1 + post_spec R1 精化)**: 「记请求模型 $MODEL」相对期望值 (`intended==glm-5.2?`) **已能抓住 motivating 场景** (smart-sonnet 非标 alias → intended≠glm-5.2)。**served model (assistant 帧观测) 的增量价值 = 检出服务端 (Luxeno) 静默替换**, 且**以 Luxeno 返 ground-truth (非 verbatim-echo 请求名) 为前提** —— 若 Luxeno 回显请求名, served≡intended 零增量信息 (R-1 echo 失效模式)。故本 Spec 的 served 检测器**结构有效性硬前置于 §待核实-1 活体判定**; #830 由 served 断言兑现 (echo 情形下降级为客户端配置检测器 + 独立 oracle, AC-10)。

---

## What Changes

落地 DEC-20260709-001 v2 三部件 (模型接线统一 + 遥测回报 + cost.json 评分), owner scope A: **覆盖全部 3 执行体 (initial/changes/redo) + commit-lint, 返工路径不留盲区**。

### A. 容器模型接线统一 (config-driven 单源, 零硬编码 + 无裸调) — AD-M6-13

`aria-orchestrator/docker/aria-runner/` 全部 claude 调用点统一经解析后的 `$MODEL`:

```bash
# 单源解析 (容器 entrypoint/lib 一处, 各 mode 引用):
MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ARIA_MODEL_FALLBACK:-}}"
[ -z "$MODEL" ] && { echo "[FATAL] no model configured (ANTHROPIC_DEFAULT_OPUS_MODEL + ARIA_MODEL_FALLBACK both unset)"; exit <infra-code>; }
claude -p --model "$MODEL" ...   # 传真名 (glm-5.2 端点直通 #830), 非别名
```

- **删净 smart-sonnet + 全部硬编码兜底** (5 处): `Dockerfile:73 ENV ARIA_MODEL=smart-sonnet` / `initial.sh:38 :-claude-opus-4-5-20250929` / `initial.sh:675 ARIA_SETTINGS_JSON.model` / `commit-lint-retry.sh:71 :-opus` + `:113` / **`redo.sh:275` + `changes.sh:252` 裸调补 `--model "$MODEL"`**。
- **兜底 = 专设配置项** `ARIA_MODEL_FALLBACK` (非硬编码, 非跨档静默借 SONNET; DEC §3.1 术语纠正: DEFAULT_{OPUS,SONNET,HAIKU} 是独立 alias 映射非 degrade ladder)。兜底启用经 §C served-model 遥测**可见** (防静默跑弱模型)。主+兜底皆缺才 fail loud。
- **单源 = opus 档** `ANTHROPIC_DEFAULT_OPUS_MODEL` (owner 确认 Layer2=opus tier; owner 已用此切模型, 不重学换法)。
- **完整性判据** (审议 C1, 强于「grep 无字面量」): 测试断言 `grep 'claude -p'` 出现次数 == 带 `--model "$MODEL"` 次数 (redo/changes 裸调=失控, 字面量 grep 抓不住)。

### B. served model 观测 (parser 增提 assistant 帧) — AD-M6-13 延伸

`parse-stream-json.sh` 增提 **assistant 帧 `message.model`** (服务端回填的实际服务模型, 现被弃)。这是唯一客观 served-model 观测点; 与请求 `$MODEL` (intended) 一并入遥测。**残余**: served 可能仍是 Luxeno 服务端别名 → §待核实-1 硬前置活体验证。

### C. 容器 stderr TELEMETRY marker (全执行体 + 全终态) — AD-M6-14

3 执行体 claude 调用后**无条件** emit (只要 CLAUDE_USAGE_JSON 非 null, **与 FINAL_OUTCOME 解耦** — 审议 C1/qa2: 8 种 token-bearing 失败终态不能漏):

```
[<mode>.sh] TELEMETRY dispatch_id=<id> served_model=<obs> intended_model=<$MODEL> \
  input_tokens=<i> output_tokens=<o> cache_creation_input_tokens=<cc> \
  cache_read_input_tokens=<cr> cost_usd_reported=<$|NA> source=<s>
```

- **dispatch_id 来源钉死** (审议 R1 I-1, 消 DEC OR): 容器读 `NOMAD_META_DISPATCH_ID` 直发真 dispatch_id (changes.sh:47/redo.sh:73 已有此写法; **initial.sh 补 `DISPATCH_ID="${NOMAD_META_DISPATCH_ID:-unknown}"`** — 唯一缺此线的执行体)。Layer1 直插满足 FK, 免 issue_id→映射歧义 (删 DEC/tasks 的映射措辞)。
- **redo.sh/changes.sh 当前裸文本 `claude -p > file 2>&1`** → 补 `--output-format stream-json` + `parse-stream-json.sh` 调用 + **stdout/stderr 分离** (仿 initial.sh:691-692, 防 `2>&1` 污染流文件); **commit_message 从 result 帧 `.result` 提取** (非裸行首 grep, 切 stream-json 后必失配 → 静默 fallback 质量回归, R-2/AC-4)。
- **commit-lint 子调用** (commit-lint-retry.sh, 现裸文本): 若纳入求和须同补 stream-json 捕获 usage (Phase 3.6); 否则 §What D 求和降级为 main-only accepted-gap (R-6 二选一)。
- **null 编码**: cost_usd_reported 可 null (parse :56 无 `// 0`) → 字面量 `NA` (非空串, 防空格分割吞字段); Layer1 NA→NULL。
- **字段名对齐 result.json** (`cache_creation_input_tokens`/`cache_read_input_tokens` 全名)。
- **fail-toward-warn + 防伪**: 锚定 regex 取容器 emit 那条; marker 缺失/解析失败**不阻塞 dispatch 终态** (遥测加分项非 block 源)。

### D. Layer 1 S5 解析 → 独立 dispatch_telemetry 表 — AD-M6-15

`extension.py` S5 终态 (现只读 outcome marker :2704-2727) **additive** 解析 TELEMETRY marker → 写新表:

```sql
CREATE TABLE IF NOT EXISTS dispatch_telemetry (
  dispatch_id                 TEXT PRIMARY KEY,      -- 单列 (每返工轮已独立 dispatch_id, 非 run_ordinal 复合键)
  served_model                TEXT,                  -- 观测服务模型 (assistant 帧)
  intended_model              TEXT,                  -- 请求模型 ($MODEL)
  input_tokens                INTEGER,               -- 一 dispatch 内多 claude 调用求和 (含 commit-lint 见 R-6 二选一)
  output_tokens               INTEGER,
  cache_creation_input_tokens INTEGER,
  cache_read_input_tokens     INTEGER,
  cost_usd_reported           REAL,                  -- informational (NULL 合法, Luxeno 下非权威)
  source                      TEXT,
  recorded_at                 TEXT,                  -- RFC-3339 UTC +00:00
  FOREIGN KEY (dispatch_id) REFERENCES dispatches(dispatch_id)
);
```

- **migration 5 步硬约束** (审议 C3, memory `feedback_schema_migration_to_version_bump`): schema.sql 内联新表 + schema_version bump / `migrations/00N_*.sql` 末 `UPDATE schema_meta` / `_MIGRATIONS` 加元组 / `_LATEST_SCHEMA_VERSION` bump (防 current==_LATEST 静默 no-op) / `_apply_backfill_rules` 新 migration_id early-return 分支 (防污染 audit)。**A.2/A.3 detailed-tasks 必须把 5 步拆独立可勾选 verification, 不得合并** (006/007/008 已踩 3 次)。
- **新建 `DispatchTelemetry` dataclass** (非往 Dispatch 加 field — 全新表, PK/列集与 dispatches 不同) + 专属 `from_row()` (仿 Dispatch.from_row optional-column graceful degrade) (审议 R1 I-2)。
- **served/intended 单值取 main 调用** (Phase 1 统一后同 dispatch 内所有 claude 同 `$MODEL`, 应一致): main 与 commit-lint served 若不一致 (Luxeno 后端多实例路由极低概率) 属**已知限制** (记 main 值, 不单开 flag 列/AC — 审议 R2 qa D-2; 见 OOS-6), 非静默假可评分 (token 仍求和, 仅 model 标量取 main)。
- 不动 dispatches 既有 cost 列 (编排 cost 走 update_token_usage, 与容器遥测正交)。

### E. cost.json 聚合改造 (168h cost 维度可评分) — AD-M6-15 延伸

`acceptance/m6-cost-snapshot.py` 增读 dispatch_telemetry (纯 additive 顶层 key, 不破 cost-acceptance AC-2 子集断言):
- **served-model 正确性**: 断言容器 dispatch **served_model** == 期望 (glm-5.2) 显式 PASS/FAIL 状态位 — 兑现 #830 (非 intended-only; 有效性前提=Luxeno 返 ground-truth 非 echo, R-1)。
- **token 趋势**: SUM(4 token 维); **窗口锚点选定** (审议 R1 backend C2, DEC 委派): telemetry JOIN dispatches, 以 `dispatches.COALESCE(cycle_start_ts, state_entered_at)` (起点) 为锚 — **与既有 metered_usd 同口径** (保同一 cost.json 内多窗口可比; telemetry.recorded_at 是终点, 口径不一致会使窗口边界可比性失真)。返工链经 `rework_of`/issue_id rollup; NULL/0 显式 COALESCE。
- **覆盖率状态位** (审议 R1 I-3 防假可评分): 顶层 `telemetry_coverage_status: ok|degraded` (阈值 ≥90%, 非仅原始比例 — 评估者扫顶层数字不会漏「70% dispatch 无 telemetry」信号) + 缺行 dispatch 显式列出。
- **cost_usd_reported**: informational 段, **不汇 metered_usd**; 强 caveat「claude-code 按 **Anthropic 定价表**估算, Luxeno/GLM 路由下既非 GLM 挂牌价亦非 flat 实付, 仅 token 相对代理, 永不作 USD」(审议 R7)。
- **cache 维 caveat** (审议 ai Minor1): cache_creation/read_input_tokens 是 Anthropic prompt-caching 专有, GLM 经 Luxeno 大概率恒 0 (待核实-8) → **不得呈现 cache_read 为「缓存节省」**。

### 连带文档同步 (Rule #3)

- `layer-boundary-contract.md` §6 容器遥测 marker 协议 + Appendix cost.json schema v2 行。
- `glm-5.2-cutover-runbook.md` §5 死指令 (查 claude_usage.model, 字段从不存在) → 改指 dispatch_telemetry.served_model; §7 checklist **最后一项** (追加 AD 批注, 该 §7 仅 7 条无「项 8」, 审议 km) 挂新 AD。
- CLAUDE.md M6 依赖链 (input-delivery ↔ 遥测 两 disjoint 前置) + architecture-decisions.md AD-M6-13/14/15。

### Out of scope (显式)

| ID | Description | Drop 理由 |
|----|-------------|----------|
| OOS-1 | Layer 1 编排调用 (S2/S3/S6) 的遥测重构 | 已有 update_token_usage 路径; 本 Spec 只补容器工作遥测, 二者正交 |
| OOS-2 | per-dispatch USD 真实归因汇入 metered | Luxeno flat 订阅结构不可归因 (对齐 cost-acceptance Luxeno=null); cost_usd_reported 仅 informational |
| OOS-3 | cost.json dual-row schema 重构 | 本 Spec additive 加顶层 telemetry key, 不改既有 metered/subscription 契约 (AC-2 不破) |
| OOS-4 | AD-M6-10 双重认领理顺 | 历史遗留 (release-closeout vs input-delivery), 上报 owner 独立处理 (DEC §10); 本 Spec 只避开 |
| OOS-5 | Luxeno 服务端 served-model 别名解析改造 | 服务端 (SilkNode) 范畴; 本 Spec 记观测到的 served (别名或真名), 别名情形由 §待核实-1 活体验证界定 |
| OOS-6 | main vs commit-lint served-model 不一致检测 (flag 列/AC) | Phase 1 统一后同 $MODEL 应一致; 不一致极低概率 (Luxeno 多实例路由), 记 main 值为已知限制, 不值单开机制 (审议 R2 qa D-2) |

---

## Constraints

- **串行前置 (input-delivery)**: 容器侧 initial.sh/Dockerfile 改动 + 镜像重建与 `aria-2.0-m6-dispatch-input-delivery` 文件级重叠 + 共享 build/deploy 门。本 Spec 容器侧 Phase B **gate 在 input-delivery 合并主干后**; Layer 1 侧遥测管道 (建表/marker 解析/cost.json 读) 可先独立推进 (additive 低风险, 不需活体 Luxeno)。
- **镜像重建确定** (非「改 config 免重建」): Dockerfile ENV 删改**必须** rebuild aria-runner 镜像 + push + redeploy。
- **cost-acceptance 契约不破**: cost.json dual-row (归档 Spec AC-2/AC-2b) + validate-m6-handoff (归档 Spec AC-8 `check_cost_measurement_method_enum` 走 zhipu_client 路径, 与容器直连正交, **不影响**)。〔注: 「归档 Spec AC-8」指 cost-acceptance 的 AC-8, 非本 Spec AC-8 fail-toward-warn〕
- **平台**: Linux/Nomad; SQLite; stdlib-only Python (Layer 1) + bash (容器)。
- **Rule #7**: 核 Nomad Var 模型名字段只读该字段不打印同 Var 内 API keys。

---

## Acceptance criteria (binary-falsifiable, `[[feedback_falsifiable_evidence_for_binary_acceptance]]`)

- [ ] **AC-1 模型接线单源无裸调**: (a) 全容器脚本每个**真实** `claude -p` 调用点 (排除注释行 `^\s*#` / echo·log·report 字符串 / `.bak` 死文件 [Phase 1.2 一并删]; 多行数组式调用按「调用块」匹配非单行) 都带 `--model "$MODEL"` — 测试枚举调用点清单 (initial.sh/redo.sh/changes.sh/commit-lint-retry.sh) 逐一断言; (b) `grep -rn smart-sonnet docker/` 排除 `tests/fixtures/`+`*.bak`+`*.md` == 0; (c) [见 AC-1b 独立测试] 主+兜底皆缺 → fail loud
- [ ] **AC-1b fail-loud 独立断言** (拆自 AC-1c, 审议 R1 I-2): `ANTHROPIC_DEFAULT_OPUS_MODEL` + `ARIA_MODEL_FALLBACK` 皆 unset fixture → 容器 exit infra-code + 错误信息含两 var 名 (非静默默认)
- [ ] **AC-2 served-model 观测落库 (两侧)**: (a) 合成 stream-json fixture (assistant 帧 message.model=X) → parser 提取 X (取帧规则明确: last assistant 帧或断言一致); (b) Layer1 解析 marker 落库断言 `served_model==X 且 intended_model==$MODEL` **两相邻字段未错位** (marker `served_model=<obs> intended_model=<$MODEL>` 相邻, 解析错位风险点)
- [ ] **AC-3 TELEMETRY marker 全终态覆盖**: fixture **必测** SUCCESS + **ASSERTION_MISMATCH** (结构保证 usage 非 null) + **CLAUDE_TIMEOUT** (usage 依赖 SIGTERM grace 期 flush, 见待核实-7) → 有 usage 者产 marker + 落库 (证 D7 与 FINAL_OUTCOME 解耦); CLAUDE_TIMEOUT 若实测恒 usage=null 则记录该事实 (非视为 emit 覆盖); null cost_usd_reported → marker `NA` → 库 NULL
- [ ] **AC-4 3 执行体全覆盖 + commit_message 回归**: initial/changes/redo 各合成 fixture → 均产 TELEMETRY marker + 落库; **且 redo/changes 切 stream-json 后, 含 `commit_message:` 的 fixture 提取值 == 原始值 (非 fallback 模板)** — 防静默质量回归 (审议 C-2, 从 result 帧 `.result` 提取, 非裸行首 grep)
- [ ] **AC-5 独立表 schema + migration**: migration 5 步齐 (schema.sql 内联 + version bump / _MIGRATIONS 元组 / _LATEST bump / schema_meta UPDATE / backfill early-return); **新库走 schema.sql + 老库走 migration 两路径**均产 dispatch_telemetry + schema_version==新值; **新建 `DispatchTelemetry` dataclass** (非 Dispatch 加 field) + from_row round-trip
- [ ] **AC-6 cost.json served-model 正确性断言**: 合成 telemetry 行 served_model==glm-5.2 → cost.json model 正确性 **显式 PASS/FAIL 状态位** (非仅展示); served_model!=期望 → FAIL (检出服务端替换; 前提=Luxeno 返 ground-truth 非 echo, 见 R-1/待核实-1)
- [ ] **AC-7 token 趋势 + 返工 rollup + 覆盖率状态位**: 多 dispatch + 返工链 (rework_of) fixture → SUM by issue_id rollup 正确 (返工轮计入; NULL/0 COALESCE); **窗口锚点与 metered_usd 对齐** (见 §What E); 覆盖率**顶层状态位** `telemetry_coverage_status: ok|degraded` (阈值 ≥90%, 非仅原始比例, 呼应 AC-6 状态位模式) + 缺行 dispatch 显式列出
- [ ] **AC-8 fail-toward-warn**: marker 缺失/畸形 fixture → dispatch 终态判定不受阻 (遥测非 block 源); cost.json 该 dispatch 记「无 telemetry」非「零成本」
- [ ] **AC-9 cost-acceptance 不破**: 加 telemetry 顶层 key 后 `check-m6-cost-acceptance.py` (归档 Spec) AC-2/AC-2b 仍 PASS (子集断言); 不影响其 AC-8 `check_cost_measurement_method_enum` (走 zhipu_client 路径, 与容器直连正交 — 显式核)
- [ ] **AC-11 兜底激活可见** (审议 R1 I-4, D6 安全属性): 合成「主 unset / 兜底 set」fixture → 容器跑兜底模型 + telemetry.intended_model==兜底值 (证兜底非静默; 降级从遥测可见)
- [ ] **AC-10 [硬前置活体] served==真跑**: (§待核实-1 解除后) 真实 dispatch → dispatch_telemetry.served_model 反映 Luxeno 实际服务模型。**独立 oracle** (非自指): 交叉核 SilkNode #830 路由日志 / provider 侧 response 元数据, 或 canary (故意设 intended=已知异值验 served 是否跟随)。served==intended==glm-5.2 (或正确检出偏离)。**终版判据待 §待核实-1 解除后钉死** (含 echo-contingency: 若实测 Luxeno verbatim-echo 请求名, served 检测器降级为仅客户端配置检测, 撤服务端断言)。**卡 Luxeno Blocker 4, 本 Spec「model 正确性对 AC-6 可评分」的硬前置**

---

## Risks

| ID | Risk | Sev | Mitigation |
|----|------|-----|-----------|
| R-1 | **served-model verbatim-echo 失效模式** (审议 R1 I-1): Luxeno 静默降级跑弱模型却在 response `message.model` 回显请求名 → served==intended==期望, AC-6/AC-10 假 PASS (false negative) | High | 关键前提 = Luxeno 返 **ground-truth** 非 echo; §待核实-1 硬前置活体判定; 若 echo → AC-10 echo-contingency 降级为客户端配置检测器 + 改用独立 oracle (#830 日志/canary)。**served 相对 intended 的增量价值仅在服务端替换检测且 Luxeno 返真值时成立** |
| R-2 | redo/changes 切 stream-json 静默毁 commit_message 提取 (裸行首 grep 失配 → 静默 fallback 通用模板, 质量回归无红) | **Med→High** (审议 C-2) | AC-4 显式回归断言 (提取值==原始, 从 result 帧 `.result`); stdout/stderr 分离 (仿 initial.sh:691-692, 防 `2>&1` 污染流) |
| R-3 | migration 静默 no-op / backfill 污染 audit | Med | AC-5 5 步 + early-return (memory `feedback_schema_migration_to_version_bump` + 006/007/008 踩 3 次); **A.2/A.3 必须把 5 步拆独立可勾选项** (审议 R1 I-3) |
| R-4 | 假可评分 (marker 覆盖不全但 cost.json 显示可评分) | High | D7 全终态 emit + AC-3 必测 + AC-7 覆盖率**状态位** (≥90% 阈值, 非仅比例) |
| R-5 | 容器侧 Phase B 与 input-delivery 镜像重建撞门 | Med | 串行前置 gate + 同一 rebuild 周期捎带 |
| R-6 | commit-lint 子调用 token 无捕获源 (裸文本 claude, 无 stream-json) → 「求和」当前无实现路径 | Med (审议 C1) | Phase 3.6 加 commit-lint stream-json 捕获, **或**降级为 accepted-gap (改 §What D「求和」措辞 + OOS) — spec-drafter A.2 二选一钉死 |
| R-7 | cost_usd_reported 在 Luxeno 下 = claude-code 按 **Anthropic 定价表**套 glm-5.2 (不在其表) → 非 null 值本身是 smell (GLM 当 Anthropic 计价) | Low | 仅 token 相对代理, **永不作 USD**; §What E 强 caveat (informational 不够) |

---

## 待核实项 (Phase B 前 ground; 1 为硬前置)

1. **[硬前置] claude CLI model 优先级 + served 观测活体 + echo 判定**: `--model 真名` 实际路由 + assistant 帧 message.model 是 glm-5.2 真名 / Luxeno 别名 / **verbatim-echo 请求名** (决定 served 检测器是否结构有效, R-1)。卡 Luxeno Blocker 4。
2. Luxeno 真名直通 (#830) + 容器 Luxeno 账户 vs Layer1 是否同 (`[[project_glm_routing_luxeno]]` 两独立账户)。
3. redo/changes stream-json 对现产出兼容性 (commit_message 从 result 帧 `.result` 提取)。
4. Nomad Var `ANTHROPIC_DEFAULT_OPUS_MODEL` 实际当前值 (5.1 vs 5.2 漂移, :259 注释仍写 5.1; Rule #7 只读模型名)。
5. commit-lint 子调用 token 捕获完备性 (决定 R-6 二选一)。
6. 镜像重建与 input-delivery 排序 (同 rebuild 周期?)。
7. **CLAUDE_TIMEOUT 是否真 flush usage** (审议 C-1): `timeout -k 10s` SIGTERM grace 期内 claude 是否 flush result 帧 — DEC D7「CLAUDE_TIMEOUT 有 flush 末帧设计」前提**代码库从未验证** (parse-stream-json 既有 fixture 里 timeout 恒 usage=null)。经验假设, 独立于待核实-1。
8. **GLM/Luxeno 是否回填 Anthropic prompt-caching 字段** (审议 ai Minor1): cache_creation/read_input_tokens 是 Anthropic 专有, GLM 大概率恒 0 → cost.json 不得把 cache_read 当「节省」呈现。

---

## Dependencies

| Dependency | Direction | Notes |
|------------|-----------|-------|
| `aria-2.0-m6-dispatch-input-delivery` | **串行前置 (容器侧)** | 文件级重叠 initial.sh + 共享镜像门; 容器侧 Phase B gate 其合并后 |
| SilkNode #830 | 上游 (已解锁) | glm-5.2 路由; served 断言兑现其 phantom 契约 |
| cost-acceptance 归档 (dual-row cost.json) | 上游契约 | 本 Spec additive 扩展不破 AC-2/8 |
| M6 168h 跑 cost 评分 (AC-5/AC-6) | 下游 | 本 Spec + input-delivery 两 disjoint 前置皆 ship 才可评分 |

---

## Cross-references

- **决策 SOT**: [DEC-20260709-001](../../../docs/decisions/DEC-20260709-001-layer2-cost-model-telemetry.md) v2 (含 §9 4-agent 审议记录 + §10 AD-M6-10 heads-up)
- **Sibling**: [aria-2.0-m6-dispatch-input-delivery](../aria-2.0-m6-dispatch-input-delivery/proposal.md) (串行前置) / [aria-2.0-m6-cost-acceptance 归档](../../archive/2026-05-28-aria-2.0-m6-cost-acceptance/proposal.md) (契约上游)
- **Runbook**: `aria-orchestrator/docs/glm-5.2-cutover-runbook.md` (§5 死指令待改) / SilkNode #830
- **Memory**: `[[feedback_falsifiable_evidence_for_binary_acceptance]]` / `[[feedback_schema_migration_to_version_bump]]` / `[[feedback_schema_column_dataclass_field_pair]]` / `[[feedback_completion_signals_vs_runtime_invocation]]` (served 非 intended) / `[[project_glm_routing_luxeno]]` / `[[feedback_combined_mode_sister_spec_audit_value]]` (本 Spec DEC 4-agent + post_spec 5-agent 审议实证)
