# Tasks: aria-2.0-m6-cost-model-telemetry

> **Spec Level**: 3 | **决策 SOT**: DEC-20260709-001 v2 (owner 决策 2026-07-09 + 4-agent 设计审议折入) | **Parent US**: US-026
> 双层架构: 本 tasks.md = 粗粒度功能层; 细粒度 (agent/文件/verification↔AC 映射) 由 A.2/A.3 `detailed-tasks.yaml` 承载。
> Success Criteria (AC-1/1b/2..9/11/10, 共 12) 见 `proposal.md`。编号不可变 (创建后不改; approve 前修订只追加)。
> **AD 分配**: AD-M6-13 (模型接线单源) / AD-M6-14 (遥测 marker 协议) / AD-M6-15 (dispatch_telemetry 表 + cost.json 评分)。

## 相位约束 (审议 km6 + DEC §7)

- **Track-1 (Layer 1 侧遥测管道)**: Phase 4-5 (建表/migration + marker 解析 + cost.json) **可先独立推进** (additive 低风险, 不需活体 Luxeno, 不碰 initial.sh/Dockerfile)。
- **Track-2 (容器侧)**: Phase 1-3 (模型接线 + parser + marker emit + 镜像重建) **gate 在 `aria-2.0-m6-dispatch-input-delivery` 合并 aria-orchestrator 主干后** (文件级重叠 initial.sh + 共享镜像门)。
- **Track-3 (硬前置活体)**: Phase 7 (AC-10 真跑验证) **gate 在 Luxeno 延迟门 (Blocker 4) 解除后**。

---

## Phase 1 — 容器模型接线统一 (AD-M6-13, Track-2 gated) [§What A]

- [ ] 1.1 容器单源解析 helper: `MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ARIA_MODEL_FALLBACK:-}}"` + 主+兜底皆缺 fail loud (exit infra-code); 置于 entrypoint/lib 一处供各 mode 引用
- [ ] 1.2 删净 smart-sonnet + 硬编码兜底 (5 处): `Dockerfile:73 ENV` / `initial.sh:38 :-claude-opus-4-5` / `initial.sh:675 ARIA_SETTINGS_JSON.model` / `commit-lint-retry.sh:71 :-opus`; **并删死文件 `docker/aria-runner/entrypoint-m0-scaffold.sh.bak`** (内含未 guard 裸 `claude -p`, 从根消 AC-1 grep 噪音源, 审议 R2 qa D-4)
- [ ] 1.3 全部 claude 调用点经 `$MODEL`: `initial.sh:675/683` + `commit-lint-retry.sh:113` + **`redo.sh:275` + `changes.sh:252` 裸调补 `--model "$MODEL"`**
- [ ] 1.4 兜底 `ARIA_MODEL_FALLBACK` 配置项接线 (Nomad Var; 非硬编码, 非跨档借 SONNET); 启用经 §Phase 2 served 遥测可见
- [ ] 1.5 完整性测试: 枚举真实 claude 调用点 (排注释/echo/`.bak`; 多行数组按块) 逐一断言带 `--model "$MODEL"`; `grep -rn smart-sonnet docker/` (排 `tests/fixtures/`+`*.bak`+`*.md`) == 0 [→ AC-1]
- [ ] 1.6 fail-loud 独立测试: 主+兜底 env 皆 unset → exit infra-code + 错误信息含两 var 名 [→ AC-1b]
- [ ] 1.7 兜底激活测试: 主 unset/兜底 set → 跑兜底模型 + telemetry.intended_model==兜底值 (降级可见) [→ AC-11]

## Phase 2 — served model 观测 (AD-M6-13 延伸, Track-2 gated) [§What B]

- [ ] 2.1 `parse-stream-json.sh` 增提 assistant 帧 `message.model` (served) **+ result 帧 `.result` 文本** (现 jq 输出 shape 不含 .result; commit_message 提取 [3.3] 依赖它 — 扩 parser shape 或 3.3 单独 jq 二选一, 审议 R2 qa D-5); 与既有 usage 并出
- [ ] 2.2 单元测试: 合成 stream-json fixture (assistant 帧 model=X) → 提取 X [→ AC-2]

## Phase 3 — TELEMETRY marker 全执行体全终态 (AD-M6-14, Track-2 gated) [§What C]

- [ ] 3.1 marker emit helper: 格式 `[<mode>.sh] TELEMETRY dispatch_id= served_model= intended_model= input_tokens= output_tokens= cache_creation_input_tokens= cache_read_input_tokens= cost_usd_reported=<$|NA> source=`; **CLAUDE_USAGE_JSON 非 null 即 emit, 与 FINAL_OUTCOME 解耦** (D7)
- [ ] 3.2 initial.sh 接线 emit (claude 调用后, 不 gate 在 SUCCESS) + **补 `DISPATCH_ID="${NOMAD_META_DISPATCH_ID:-unknown}"`** (initial.sh 唯一缺此线; 对齐 changes.sh:47/redo.sh:73) [→ AC-2 dispatch_id]
- [ ] 3.3 **redo.sh/changes.sh 加 `--output-format stream-json` + `parse-stream-json.sh` + emit + stdout/stderr 分离** (仿 initial.sh:691-692); **commit_message 改从 result 帧 `.result` 提取** + 回归断言提取值==原始 (非 fallback 模板, 防静默质量回归) [→ AC-4]
- [ ] 3.4 null 编码 `NA` (cost_usd_reported 可 null, 防空格分割吞字段) + 字段名对齐 result.json 全名
- [ ] 3.5 集成测试: SUCCESS + ASSERTION_MISMATCH (必测, 结构保证 usage) + CLAUDE_TIMEOUT (必测, 依赖 flush; 若恒 null 记录该事实) 均按 usage 有无产 marker [→ AC-3]
- [ ] 3.6 commit-lint token: **二选一钉死** (R-6) — (a) commit-lint-retry.sh 加 stream-json + usage 捕获求和入该 dispatch, **且同步把 `:127` `new_msg` 提取从裸行首 grep 改 result 帧 `.result`** (否则重演 R-2 同类回归: 重写结果静默丢弃走 chore: fallback 无红, backend R2 Finding B); **或** (b) 降级 accepted-gap (改 §What D「求和」措辞 + 入 OOS; 不碰 stream-json 故不触此回归) [→ 待核实-5 定]

## Phase 4 — Layer 1 解析 + dispatch_telemetry 表 (AD-M6-15, **Track-1 独立**) [§What D]

- [x] 4.1 schema.sql 内联 `CREATE TABLE IF NOT EXISTS dispatch_telemetry` (PK=dispatch_id 单列, served+intended+4 token 维+cost_usd_reported+source+recorded_at, FK dispatch_id) + schema_version 字面量 bump
- [x] 4.2 migration `migrations/00N_*.sql` (末 `UPDATE schema_meta`) + `_MIGRATIONS` 加元组 + `_LATEST_SCHEMA_VERSION` bump + `_apply_backfill_rules` 新 migration_id early-return 分支 [migration 5 步, memory schema_migration_to_version_bump]。**A.2/A.3 detailed-tasks 必须把此 4 子步拆独立可勾选 verification, 不得合并一条** (006/007/008 已踩 3 次)
- [x] 4.3 **新建 `DispatchTelemetry` dataclass** (独立于 Dispatch — 全新表非加 field) + 专属 `from_row()` (仿 Dispatch.from_row optional-column graceful degrade) (memory schema_column_dataclass_field_pair)
- [x] 4.4 `extension.py` S5 终态 additive 解析 TELEMETRY marker (锚定 regex 防伪) → 写 dispatch_telemetry; **dispatch_id 取自 marker 自带字段** (容器直发 NOMAD_META_DISPATCH_ID, 见 3.2/§What C; 无 issue_id→映射); token 求和按 **3.6 决议**落地 (a: main+commit-lint 求和一行 / b: 仅 main + 求和范围收窄入 OOS)
- [x] 4.5 **fail-toward-warn**: marker 缺失/畸形不阻塞 dispatch 终态判定 [→ AC-8]
- [x] 4.6 集成测试: migration round-trip (新旧库) + schema_version==新值 + dataclass from_row + marker 解析落库 [→ AC-5]

## Phase 5 — cost.json 聚合评分 (AD-M6-15 延伸, **Track-1 独立**) [§What E]

- [x] 5.1 `m6-cost-snapshot.py` 增读 dispatch_telemetry: served-model 正确性断言 (served==期望, served!=期望→FAIL) [→ AC-6]
- [x] 5.2 token 趋势 SUM(4 维); **窗口锚点 = telemetry JOIN dispatches 用 `COALESCE(cycle_start_ts,state_entered_at)` (与 metered_usd 同口径, 保多窗口可比)** + 返工链 `rework_of`/issue_id rollup + NULL/0 COALESCE [→ AC-7]
- [x] 5.3 覆盖率**状态位** `telemetry_coverage_status: ok|degraded` (阈值 ≥90%, 非仅比例) + 缺行 dispatch 显式列出 (防假可评分) [→ AC-7]
- [x] 5.6 cost_usd_reported 强 caveat (Anthropic 定价套非 Anthropic 模型, 仅 token 相对代理永不作 USD) + cache 维 caveat (GLM 大概率恒 0, 不作节省信号) [→ 待核实-8]
- [x] 5.4 cost_usd_reported 仅 informational 段, 不汇 metered_usd; cost.json 顶层 additive telemetry key
- [x] 5.5 回归: `check-m6-cost-acceptance.py` AC-2/AC-2b 仍 PASS (additive key 不破子集断言) [→ AC-9]

## Phase 6 — 连带文档同步 (Rule #3) [§连带文档同步]

- [ ] 6.1 `layer-boundary-contract.md` §6 容器遥测 marker 协议 (仿 §5 格式) + Appendix cost.json schema v2 行 + 头注更新
- [ ] 6.2 `glm-5.2-cutover-runbook.md` §5 死指令 (查 claude_usage.model 字段从不存在) → 改指 dispatch_telemetry.served_model; §7 checklist **最后一项** (§7 仅 7 条无「项 8」) 挂新 AD
- [ ] 6.3 `architecture-decisions.md` 新增 AD-M6-13/14/15 (含 alternatives considered)
- [ ] 6.4 CLAUDE.md M6 依赖链更新 (input-delivery ↔ 遥测 两 disjoint 前置; high-contention 段 fetch 后改)

## Phase 7 — 硬前置活体验证 (Track-3, gate Luxeno Blocker 4) [§AC-10]

- [ ] 7.1 (§待核实-1 解除后) 真实 dispatch → dispatch_telemetry.served_model 反映 Luxeno 实际服务模型; served==intended==glm-5.2 (或 served≠intended 正确报警)
- [ ] 7.2 Nomad Var `ANTHROPIC_DEFAULT_OPUS_MODEL` 实际当前值核实 (5.1 vs 5.2 漂移; Rule #7 只读模型名字段) [§待核实-4]
- [ ] 7.3 兑现 SilkNode #830 phantom 契约 (served 断言真跑 = glm-5.2) → close #830

## Phase 8 — 版本 + 归档 (Phase C/D)

- [ ] 8.1 aria-orchestrator 版本 + 子模块指针 bump + 镜像重建 push redeploy (与 input-delivery 同 rebuild 周期捎带, 审议 km6)
- [ ] 8.2 **部分归档规则** (审议 R1 I-4/I-5, 防 dispatch-input-delivery 式 limbo): Track-1 (Layer1 遥测管道 Phase 4-5) 完成 + review 后**可独立先归档**; Track-2 (容器侧, gate input-delivery) + Track-3 (AC-10 活体, gate Luxeno) 阻塞超期则拆**独立 tracked follow-up** (仿 cost-acceptance 2 deferred follow-up 先例)。**「model 维度对 AC-6 可评分」条件于 AC-10 解除** — Track-1 先归档不等于 168h cost 维度已可评分 (诚实标注, 防假可评分声称)
- [ ] 8.3 openspec-archive 归档 (gate 过自身)

## 早期文档 (Phase A 定稿即做, 不等 Phase 6)

- [x] A.0 CLAUDE.md M6 状态段「遥测 Spec ... 待起」→「Drafting (`aria-2.0-m6-cost-model-telemetry`, post_spec CONVERGED)」轻量替换 (审议 km4: high-contention 段, 过期误导多终端; 完整依赖链叙事仍 Phase 6.4 做; fetch 后改防并发覆盖)

---

## 待核实项 (Phase B 前 ground; §1 硬前置) — 见 proposal §待核实项 1-8
## 依赖 — 见 proposal §Dependencies (input-delivery 串行前置容器侧 / #830 上游 / cost-acceptance 契约不破 / 168h 下游)
