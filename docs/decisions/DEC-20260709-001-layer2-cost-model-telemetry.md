# DEC-20260709-001 — Layer 2 cost/model 遥测回报 + 容器模型接线统一

> **状态**: v2 (4-agent 设计审议已折入; 待 owner 最终点头 → spec-drafter L3)
> **创建**: 2026-07-09 | **v2 修订**: 2026-07-09 (折入 tech-lead/backend/qa/km 审议 2 OBJECTION + 2 CONCERNS)
> **触发**: M6 168h 自主跑「cost 维度可评分 (AC-5/AC-6)」依赖遥测 Spec (preflight 2026-07-02 §6 item4 + DEC-20260702-001 §依赖边)
> **决策人**: 10CG Lab owner (2026-07-09 交互: Q1/Q2/Q3 + scope A + 兜底配置驱动+可见 + opus 档)
> **前置 grounding**: Explore「Layer2→Layer1 遥测链现状」+ glm-5.2-cutover-runbook + cost-acceptance 归档 + **4-agent code-grounded 设计审议 (§9)**
> **关联**: SilkNode #830 (glm-5.2 路由; phantom 契约由本 Spec 兑现) / Aria #147 / DEC-20260702-001 (sibling 输入投递)
> **Spec Level**: 3 (Full — 跨容器 3 执行体 [initial/changes/redo] + commit-lint + Layer1 + schema + cost.json + config)
> **AD 分配**: 本 Spec 占 **AD-M6-13 / AD-M6-14 / AD-M6-15** (显式避开 AD-M6-10..12 双重认领区, 见 §10 heads-up)

---

## 1. Context — grounded 缺口 (2 断点 + 模型接线糊涂账 + cutover-inert 红旗)

### 1.1 遥测链两断点 (Explore code-grounded)

自主容器 dispatch 的 per-dispatch cost/model 在到达 dispatches 表前丢失:
- **断点 1 (传输)**: 容器 result.json 写跨节点不可读 host volume (`aria-layer2-runner.hcl:213-215`); Layer 1 只经 `get_alloc_logs()` 读 stderr (`alloc_status_provider.py:258-267`); 容器只发 outcome marker (`initial.sh:307`), 不含 cost/model。
- **断点 2 (model 源)**: `result.json.claude_usage` 6 字段无 model (`initial.sh:954-961`); parser 只取 result 帧无 model (`parse-stream-json.sh:55-67`); **但 assistant 帧带 `message.model` (服务端回填的实际服务模型) 被丢弃** — 这是唯一客观 served-model 观测点 (审议 O1 挖出)。

现状落 dispatches = 仅 Layer1 S2/S3/S6 编排调用 (`extension.py:873,3140`, Luxeno $0 / glm-4.5-air / subscription_flat)。容器真实工作全链丢失。

### 1.2 容器模型接线糊涂账 (审议补全: **5 处**, 非 4)

| 位置 | model 行为 | 性质 |
|------|-----------|------|
| `Dockerfile:73` `ENV ARIA_MODEL=smart-sonnet` → `initial.sh:683 --model` | 别名 smart-sonnet | 烤死默认 |
| `initial.sh:38` `:-claude-opus-4-5-20250929` | 兜底字面量 | 死码 (env 已 set) |
| `initial.sh:675` `ARIA_SETTINGS_JSON` model 字段 | 同 ARIA_MODEL | 第二写点 (须与 --model 同步) |
| `commit-lint-retry.sh:113` `--model "${ARIA_MODEL:-opus}"` | 别名或 opus | commit-lint 子调用 |
| **`redo.sh:275` / `changes.sh:252` `claude -p` 裸调** | **无 --model** | **走 claude 内建默认 (审议补: grep 字面量 0 命中但仍失控)** |

D6「grep 无硬编码字面量」**必要非充分** (审议 C1): redo/changes 无 flag 亦失控。完整判据 = **枚举所有 claude 调用点全部显式经 `$MODEL`**。

### 1.3 🔴 cutover-inert 红旗 (审议 O2/A2 从代码强化到近实锤)

`--model smart-sonnet` 非 canonical alias (opus/sonnet/haiku 无一命中) → `ANTHROPIC_DEFAULT_*_MODEL` 的 alias remap 对 initial.sh **结构性 inert**; redo/changes 无 flag 至多吃 DEFAULT_SONNET=glm-5-turbo (**非** opus cutover 目标 glm-5.2)。**结论: 当前无任何容器路径 honor `ANTHROPIC_DEFAULT_OPUS_MODEL`, glm-5.2 opus-档 cutover 对全部 mode inert**。残余不确定 = claude CLI 对非标 alias 确切行为 (§6 待核实-1, 硬前置)。

---

## 2. 锁定决策 (owner 2026-07-09 + 审议折入)

| # | 决策点 | 决定 |
|---|--------|------|
| D1 | cost 维度捕获什么 | model (**served 观测 + intended 请求双记, 审议 O1**) + 完整 token 分项 (input/output/cache_creation_input/cache_read_input) + cost_usd_reported 仅 informational (Luxeno 下非权威, 不汇 metered) |
| D2 | 容器 model 权威 | 配置真名 (glm-5.2) 权威; smart-sonnet 彻底清; **acceptance 断言 served==期望 且 served==intended (否则=cutover inert 报警)** |
| D3 | 遥测落 schema | 独立 `dispatch_telemetry` 表; **PK = dispatch_id 单列** (审议 O2/S3: 每返工轮已是独立 dispatch_id, run_ordinal 建模了不存在的 cardinality → 删除); 一 dispatch 内多 claude 调用 (main + commit-lint) **token 求和记一行**; 返工链靠既有 `rework_of` / issue_id rollup |
| D4 | scope | **遥测 Spec 一起管模型接线统一, 且覆盖全部 3 执行体 (initial/changes/redo) + commit-lint** (owner scope A: 返工路径不留盲区) |
| D5 | 单一真源 | `ANTHROPIC_DEFAULT_OPUS_MODEL` (opus 档, owner 确认 Layer2=opus tier) |
| D6 | 兜底 | 全配置驱动 (非硬编码); **兜底启用经 served-model 遥测可见** (审议 C2: 防静默跨档降级); **主+兜底配置皆缺才 fail loud** |
| D7 | marker 发射条件 | **claude 曾产 usage (CLAUDE_USAGE_JSON 非 null) 即无条件 emit, 与 FINAL_OUTCOME 解耦** (审议 C1/C3: 8 种 token-bearing 失败终态不能漏, 尤其 CLAUDE_TIMEOUT 有 flush 末帧设计) |
| D8 | #830 兑现 | 记 **served model** 断言 (非仅 intended); intended-only 是套套逻辑检不出 inert (审议 O1 否证初版 D8) |

---

## 3. 统一模型逻辑设计 (D2/D4/D5/D6)

### 3.1 config-driven 单源, 覆盖全部 claude 调用点 (零硬编码 + 无裸调)

```
MODEL = ${ANTHROPIC_DEFAULT_OPUS_MODEL:?}      # 主 (opus 档单源); 未配 → 读配置兜底 ↓
        或 ${ARIA_MODEL_FALLBACK}              # 兜底 (配置项非硬编码); 亦缺 → fail loud
claude --model "$MODEL"                        # 传真名 (glm-5.2 端点直通 #830; 非别名)
```

**所有 claude 调用点统一经 `$MODEL`** (审议 C1 完整性判据): `initial.sh:675`(settings.model) + `:683`(--model) + `commit-lint-retry.sh:113` + **`redo.sh:275`** + **`changes.sh:252`** (后两者当前裸调, 须加 `--model "$MODEL"`)。删 Dockerfile ENV smart-sonnet + initial.sh:38 兜底 + commit-lint :71 兜底。测试: `grep 'claude -p'` 次数 == 带 `--model "$MODEL"` 次数。

**兜底非「降级链」** (审议 C2 纠正术语): DEFAULT_{OPUS,SONNET,HAIKU} 是 3 独立 alias 映射非 degrade ladder (真 degrade 在 provider_router.py Layer1 Python, 容器用不了); 用专设 `ARIA_MODEL_FALLBACK` 配置项, 不跨档静默借 SONNET。

### 3.2 真实性: 记 served (观测) 非仅 intended (审议 O1 核心修正)

parser 增提 **assistant 帧 `message.model`** (served, 服务端回填) → telemetry 记 `served_model` + `intended_model` 两列。**记录=intended 是套套逻辑 (检不出 inert); served≠intended 才是 cutover-inert 检测器**。#830 由 served 断言兑现。残余: served 可能仍是别名 (Luxeno 服务端解析) → §6 待核实-1 活体验证 (硬前置)。

---

## 4. 遥测架构 (D1/D3/D7)

### 4.1 断点 1 修 — 容器 stderr TELEMETRY marker (全执行体 + 全终态)

3 执行体 (initial/changes/redo) claude 调用后**无条件** emit (D7, 只要有 usage; 与 SUCCESS 解耦):
```
[<mode>.sh] TELEMETRY dispatch_id=<id> served_model=<obs> intended_model=<$MODEL> \
  input_tokens=<i> output_tokens=<o> cache_creation_input_tokens=<cc> \
  cache_read_input_tokens=<cr> cost_usd_reported=<$|NA> source=<s>
```
- **redo.sh/changes.sh 当前裸文本 `claude -p > file`** (无 stream-json), 须加 `--output-format stream-json` + `parse-stream-json.sh` 调用 (审议 O2/qa1: 否则返工轮零 usage 数据源)。
- **null 编码** (审议 C4): cost_usd_reported 可为 null (parse :56 无 `// 0`) → marker 用字面量 `NA` (非空串, 防空格分割吞下字段); Layer1 解析 NA→NULL。
- **字段名对齐 result.json** (审议 C4): `cache_creation_input_tokens`/`cache_read_input_tokens` (非简写)。
- **防伪 + fail-toward-warn** (审议 A1): 锚定 regex 取容器 emit 那条; marker 缺失/解析失败**不阻塞 dispatch 终态** (遥测加分项非 block 源)。
- dispatch_id 来源 (审议 C3): 容器 marker 现用 issue_id; 由 Layer1 S5 当前 dispatch 上下文映射 (Layer1 本就知 dispatch_id) 或容器 import NOMAD_META_DISPATCH_ID。

### 4.2 断点 2 修 — Layer 1 S5 additive 解析 → 独立表 (PK=dispatch_id)

```sql
CREATE TABLE IF NOT EXISTS dispatch_telemetry (     -- 审议 C3: IF NOT EXISTS (对齐既有 4 表)
  dispatch_id                 TEXT PRIMARY KEY,      -- 审议 O2: 单列, 非 (dispatch_id,run_ordinal)
  served_model                TEXT,                  -- 审议 O1: 观测服务模型 (assistant 帧)
  intended_model              TEXT,                  -- 请求模型 ($MODEL)
  input_tokens                INTEGER,               -- 一 dispatch 内多 claude 调用求和 (main+commit-lint)
  output_tokens               INTEGER,
  cache_creation_input_tokens INTEGER,
  cache_read_input_tokens     INTEGER,
  cost_usd_reported           REAL,                  -- informational (NULL 合法)
  source                      TEXT,
  recorded_at                 TEXT,                  -- RFC-3339 UTC (S5 终态写入)
  FOREIGN KEY (dispatch_id) REFERENCES dispatches(dispatch_id)  -- dispatch_id 有 uq_dispatches_dispatch_id
);
```
**migration 机制 5 步硬约束** (审议 C3, memory `feedback_schema_migration_to_version_bump`): ① schema.sql 内联新表 + schema_version 字面量 bump ② `migrations/00N_*.sql` 新文件末 `UPDATE schema_meta SET value='<新版>'` ③ `schema_migrate.py:_MIGRATIONS` 加元组 ④ `_LATEST_SCHEMA_VERSION` bump (否则 current==_LATEST 静默 no-op) ⑤ `_apply_backfill_rules` 加新 migration_id **early-return 分支** (防污染 audit 轨迹, 006/007/008 已无声踩 3 次)。**dataclass field + from_row 配套** (memory `feedback_schema_column_dataclass_field_pair`)。

### 4.3 cost.json 聚合改造 (D1)

`m6-cost-snapshot.py` 增读 dispatch_telemetry 产 168h cost 维度信号 (审议 backend: 纯 additive 顶层 key, 不破 cost-acceptance AC-2 子集断言):
- **model 正确性**: 断言容器 dispatch **served_model** == 期望 (glm-5.2) — 兑现 #830 (非 intended-only)。
- **token 趋势**: SUM(4 token 维) by 窗口; 返工链经 `rework_of`/issue_id rollup (审议 O2: 否则返工轮系统低估); NULL vs 0 语义显式 (审议 C4/qa5: COALESCE, 别把缺轮当零成本)。
- cost_usd_reported: 仅 informational 段, **不汇 metered_usd** (D1)。
- **覆盖率断言** (审议 qa2: 防假可评分): 断言窗口内 dispatch 有 telemetry 行的比例; 缺行 dispatch 显式列出 (非静默当零)。
- 窗口锚点 (审议 backend): dispatches 用 `COALESCE(cycle_start_ts,state_entered_at)` (起点), telemetry.recorded_at 是终点 — spec-drafter 明确选锚或记差异可接受。
- 不影响 `check_cost_measurement_method_enum` AC-8 (zhipu_client 路径, 与容器直连正交 — 显式记「不影响」审议 km4)。

---

## 5. 决策点清单 (spec-drafter 无歧义引用)

1. 全部 claude 调用点 (5 处) 统一经 config-driven `$MODEL`; redo/changes 从裸调加 `--model`+stream-json; 零硬编码 + 无裸调 (§3.1)。
2. 兜底 = 专设配置项, 启用经 served-model 可见, 主+兜底皆缺才 fail loud (D6)。
3. 传真名非别名; smart-sonnet 全清 (5 处) (D2)。
4. parser 增提 assistant 帧 served model; telemetry 记 served+intended (§3.2, O1)。
5. 3 执行体无条件 emit TELEMETRY marker (D7, 全终态); redo/changes 补 stream-json; NA null 编码; 字段名对齐 (§4.1)。
6. 独立表 PK=dispatch_id (非 run_ordinal); 多 claude 调用求和; migration 5 步 + dataclass 配套 (§4.2)。
7. cost.json 增读 telemetry: served-model 正确性 + token 趋势 (rework rollup) + 覆盖率断言; cost_usd_reported 不汇 metered (§4.3)。
8. 遥测 fail-toward-warn: marker 缺失/解析失败不阻塞 dispatch 终态 (§4.1)。
9. 兑现 #830: served 断言 (非 intended) (D8)。

## 6. 待核实项 (spec 前置; 1 为**硬前置**)

1. **[硬前置] claude CLI model 优先级 + served 观测活体验证**: `--model <真名>` 实际路由 + assistant 帧 model 是真名 glm-5.2 还是别名 → 决定 §3.2 served 断言是否有效。卡 Luxeno 延迟门 (Blocker 4)。**本 Spec「model 正确性断言」有效性的硬前置, 非并列待核实** (审议 qa3)。
2. Luxeno 真名直通确认 (#830 说可, 核 silknode/provider 侧无需别名); 容器 Luxeno 账户 vs Layer1 是否同 (memory `project_glm_routing_luxeno` 两独立账户)。
3. redo/changes 加 stream-json 对返工产出的兼容性 (现纯文本 grep commit_message, 改 stream-json 后 grep 逻辑须适配)。
4. Nomad Var `ANTHROPIC_DEFAULT_OPUS_MODEL` **实际当前值** (5.1 vs 5.2 漂移; :259 注释仍写 glm-5.1 — Rule #7: 该 Var 同存 API keys, 只读模型名字段不打印 secret)。
5. commit-lint 子调用 token 捕获完备性 (每轮≤3 次 claude, 求和入该 dispatch 行)。
6. 镜像重建确定 (审议 km6: Dockerfile ENV 改**必须** rebuild, 非「改 config 不用重建」; 与 input-delivery 同吃紧 build/deploy 门 — 排序见 §7)。

## 7. 依赖边 (审议 km6 修正: input-delivery 非正交, 是文件级重叠 + 串行前置)

- **上游硬前置**: SilkNode #830 (glm-5.2 路由) / cost-acceptance 契约 (dual-row 不破) / DEC-20260702-001。
- **⚠️ input-delivery = 串行前置 (非正交)**: 二者都改 `initial.sh` (input-delivery 分支已 +478/-64) + 都需 Dockerfile 改 + 镜像重建。**本 Spec 容器侧改动 (initial.sh/Dockerfile) 不得在 input-delivery 合并进 aria-orchestrator 主干前开 Phase B**; 建议同一次镜像 rebuild 周期捎带 (省紧张的 build/deploy 门)。**Layer1 侧遥测管道 (建表+marker 解析+cost.json 读) 可先独立推进** (additive 低风险, 不需活体 Luxeno)。
- **下游**: M6 168h 跑 cost 维度评分 (AC-5/AC-6) — 本 Spec 与 input-delivery **两个** disjoint 前置皆 ship 才 168h 可闭环+可评分。

## 8. 连带文档同步 (审议 km3/5/6)

- `layer-boundary-contract.md` 新增 §6 容器遥测 marker 协议 (格式仿 §5) + Appendix cost.json schema v2 行 + 更新头注。
- `glm-5.2-cutover-runbook.md` §5 验证方法: 「查 result.json.claude_usage.model」是死指令 (字段从不存在) → 改指向 dispatch_telemetry.served_model; §7 checklist 项 8 收口挂新 AD。
- CLAUDE.md M6 项目状态段: 遥测依赖链更新 (input-delivery ↔ 遥测 两 disjoint 前置)。
- architecture-decisions.md: 新增 AD-M6-13/14/15。

## 9. 4-agent code-grounded 设计审议记录 (2026-07-09)

| agent | verdict | 关键 finding → 折入 |
|-------|---------|---------------------|
| tech-lead | OBJECTION | O1 记 config 非 served (套套逻辑检不出 inert) → §3.2/D8 served 双记; O2 run_ordinal 建模不存在 cardinality → D3 PK=dispatch_id; C1-C3 marker 覆盖/兜底术语/emit gate → D7/D6/§4.1 |
| backend-architect | CONCERNS | redo/changes 无 usage 源 → §4.1 补 stream-json; migration 5 步静默陷阱 → §4.2; null 编码/字段名/source 常量 → §4.1; cost.json additive 不破 AC-2 ✓ |
| qa-engineer | OBJECTION | redo/changes 漏改 (对标 sibling①) + 假可评分 (marker 只覆盖 2/10 终态, 对标 sibling②) → D4 scope A/D7; phantom 契约换马甲 (served) → §3.2; run_ordinal 建模错 → D3 |
| knowledge-manager | CONCERNS | AD 零分配 + AD-M6-10 双重认领 → §此 AD-M6-13+/§10; layer-boundary §6 缺口 + cutover-runbook 死指令 + input-delivery 文件级重叠 → §7/§8 |

**2 OBJECTION 核心 (O1 served-model + O2/scope 返工路径) 均触 locked D1/D3/D8, 已经 owner 2026-07-09 定夺折入** (scope A + served 双记 + PK 简化)。全部 findings 已消化, 无遗留 objection。

## 10. Heads-up (非本 Spec 范畴, 上报 owner)

**AD-M6-10 双重认领**: release-closeout proposal.md:15 保留 AD-M6-10..12; 但 dispatch-input-delivery 的 architecture-decisions.md:4041 也用 AD-M6-10 (未合并主干, 一合即撞)。本 Spec 避开 (从 AD-M6-13)。建议 owner 择机理顺 (input-delivery 快合并, 现在改号成本最低; 参照 AD-M6-8 "Retired" repurpose 先例格式)。
