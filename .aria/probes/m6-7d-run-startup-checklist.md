# M6 #2 e2e-resilience — 7 天运营跑启动 Checklist (Runbook)

> **目的**: owner kick off 168h E2E 跑时照此执行。判据全部来自 `openspec/changes/aria-2.0-m6-e2e-resilience/proposal.md` §A.1-A.7 + `evals/m6-prompt-quality/` rubric。
> **Created**: 2026-06-27 (AI 整理, owner 执行)
> **现状核实 (2026-06-27)**: 代码侧 100% ship; Phase B 前置 (Spec #1 AC-7) ✅ PASS (`m6-gate-check.md`, 2026-06-01); **168h 时钟未启动** (无 day-N probe, corpus/score 全空模板, provenance/log 未填)。

---

## 时间线本质 (先读)

- **168h = 硬地板 7 天**, 不可压缩 (持续 uptime 要求)。
- **alloc 一旦 alloc 级重启 → CreateTime 变 → 时钟清零重跑** (task 级重启不影响, 用 alloc.CreateTime)。
- **Day-3 健康闸不过 → 暂停 + 从 Day-1 重启** (时钟清零)。
- **corpus 评分是 owner 人工** (10 样本 ×7 维, AI 不可代/不可伪造)。
- 绝对最短 ≈ 7 天 + pre-flight (~1 天) + 评分/closeout (~1-2 天), 前提全程不重启、Day-3 过、owner 评分及时。
- 跑完 #2 后还有 **#4 release-closeout** (0/41, 独立 Phase B cycle, 消费 #2 证据)。

---

## Phase 0 — 启动前准备 (时钟未走)

- [x] **A-infra-1** Spec #1 AC-7 (3-day cost history) gate PASS — 已于 2026-06-01 light-1 cron 确认 (`m6-gate-check.md`)。**无需重做**。
- [ ] **migration 007 应用到 live DB** — 文件已 ship (`hermes-extensions/aria-layer1/aria_layer1/migrations/007_schema_v4.3_add_is_synthetic.sql`), 但须在 aria-layer1 节点对 live DB 实际 apply + 验证:
  ```bash
  # 节点上: 确认 is_synthetic 列存在 (schema v5.0)
  sqlite3 <live aria_layer1.db> "PRAGMA table_info(dispatches);" | grep is_synthetic
  ```
- [ ] **T-validate-schema-1** 逐列核对 live `dispatches` schema (drift guard, 写任何 SQL 前):
  ```bash
  sqlite3 <live aria_layer1.db> "PRAGMA table_info(dispatches);"
  ```
- [ ] **核对 issue_type 的 json_extract key** (stratification SQL 依赖) — 实际 payload key 是 `$.issue_labels` 还是 `$.issue_type_hint`:
  ```bash
  sqlite3 <live aria_layer1.db> "SELECT payload_json FROM dispatch_audit_log LIMIT 3;"
  ```
- [ ] **abi_compat 校验** (migration 007 后) — `validate-m6-handoff.py --check-abi-compat` 5 promises 仍过。
- [ ] **选 pre-flight fixture provenance** (§A.5, 填 `m6-preflight-provenance.md`): A=replay M5 O3 (首选, 回归连续性) / B=fresh synthetic `[DEMO-M6-P*]` / C=cross-project Kairos/SilkNode。记 `Selected option:` + rationale。
- [ ] **跑 3 次 pre-flight dispatch** (真 LLM, 每次 ≤$2, 合计 ≤$6) → 填 `m6-preflight-log.md` (dispatch_id + fixture_source + outcome[到 S9_CLOSE 或 8h 内 S_FAIL] + cost_usd 真值)。
- [ ] **验 pre-flight 闸**: `check-m6-e2e-acceptance.py --tg-a --check-preflight` (前 3 条 cost_usd 全 ≤$2 → PASS, = AC-6)。

---

## Phase 1 — Day 1: 启动 168h 时钟

- [ ] **确认 aria-layer1 alloc up + 健康** (这是时钟载体)。
- [ ] **落 alloc anchor** (canonical clock start):
  ```bash
  nomad alloc status <ALLOC_ID> -json \
    | jq '{alloc_id: .ID, create_time_ns: .CreateTime}' \
    > .aria/probes/m6-7d-day-1-alloc-anchor.json
  ```
- [ ] **写 Day-1 probe** `.aria/probes/m6-7d-day-1.md`, 含 `## Alloc anchor` 段 (Alloc ID + CreateTime ns + ISO-8601)。
- [ ] ⚠️ **自此 alloc 不可 alloc 级替换/重建** (否则 AC-1 FAIL + 时钟清零)。

---

## Phase 2 — Day 2-7: 每日 probe + 喂 dispatch

- [ ] 每天写 `.aria/probes/m6-7d-day-{N}.md`: alloc status (uptime hours) + dispatch summary (S9 完成数 / S_FAIL / stuck>4h / synthetic 比) + stratification 表 (bug/feature/stale)。
- [ ] **跑期凑够 dispatch 闸** (AC-2): ≥10 个走完 S0→S9_CLOSE; **≤70% synthetic** (即 ≥3 个真实); **bug/feature/stale 各 ≥1**。
- [ ] (可选, 加分) **cross-project** Kairos/SilkNode 真 issue 走完 1 个 S0→S9 (is_synthetic=0) → AC-2 升 `PASS+` (P-9 条件: 目标 repo 可达 + 现有 PAT scope 够 + 无需新 scope)。

---

## Phase 3 — Day 3 (hour 72): 中途健康闸

- [ ] 评 3 条件 (填 day-3 probe `## Health gate` 段):
  1. ≥1 个完整 S0→S9 cycle。
  2. S_FAIL rate ≤50% (`S_FAIL / total ≤ 0.50`)。
  3. 无 dispatch 卡非终态 >4h。
- [ ] 任一不过 → **暂停 + 调查 + 从 Day-1 重启** (时钟清零)。Day-3 verdict 必须 = PASS 才算数 (AC-1 要 7 天 probe 齐 + Day-3 PASS)。

---

## Phase 4 — Day 7+: corpus 采集 + owner 评分

- [ ] 从 `dispatches` 表挑 **10 个完成 dispatch** (类型/状态多样 + synthetic/real 混)。
- [ ] 逐个填 `evals/m6-prompt-quality/corpus/sample-{NN}.md`: 逐字 command text + metadata (dispatch_id / issue type / state / is_synthetic / 时间戳)。
- [ ] **owner 评分** `score-{NN}-owner.md`: 7 维 (Naturalness/Specificity/Tone/Completeness/Conciseness/Technical accuracy/Autonomy footprint) 各 0-10 → 该样本 median。
- [ ] **AC-5 闸**: median(10 个样本 median) **≥ 7.0** (中位数, 非均值)。

---

## Phase 5 — Acceptance 总闸 + 归档

- [ ] `python3 acceptance/check-m6-e2e-acceptance.py --tg-a` → AC-1 (uptime≥168h + 7 probe) / AC-2 (stratification) / AC-6 (pre-flight) 全 PASS。
- [ ] `--tg-c` → AC-5 (corpus median ≥7) PASS。
- [ ] AC-7 abi_compat (脚本 delegate `validate-m6-handoff.py --check-abi-compat`) PASS。
- [ ] 全 PASS → #2 e2e-resilience 验收达成 → **归档 Spec #2** (走 openspec-archive; archive-completeness gate 需 tasks done)。
- [ ] **然后**: 起 #4 release-closeout Phase B (独立 cycle, 消费 #2 证据)。

---

## 已 ship 的代码件 (无需重做)

| 件 | 路径 |
|----|------|
| migration 007 (is_synthetic) | `hermes-extensions/aria-layer1/.../migrations/007_schema_v4.3_add_is_synthetic.sql` |
| acceptance 脚本 | `acceptance/check-m6-e2e-acceptance.py` |
| abi_compat 校验 (Spec #1 拥有, 勿改) | `docs/validate-m6-handoff.py` |
| probe/corpus/score/rubric 模板 | `.aria/probes/m6-preflight-*.md` + `evals/m6-prompt-quality/` |

> 路径相对 `aria-orchestrator/` (probe 文件除外 — 在主仓 `/home/dev/Aria/.aria/probes/`)。
