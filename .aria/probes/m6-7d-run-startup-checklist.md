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
- [ ] **migration 007 应用到 live DB** — 文件已 ship (`hermes-extensions/aria-layer1/aria_layer1/migrations/007_schema_v4.3_add_is_synthetic.sql`)。
  > ⚠️ **必须经 `schema_migrate.py` runner 应用, 不可 raw `sqlite3 < 007.sql`** (2026-06-27 AI 预演确认): `schema.sql` 已是 v5.0 含 `is_synthetic`; SQLite 无 `ADD COLUMN IF NOT EXISTS`, 幂等性靠 runner 的版本守卫 (`_LATEST_SCHEMA_VERSION='5.0'` → 已达则 no-op)。raw apply 到已 v5.0 库会抛 `duplicate column name: is_synthetic`。runner 幂等 no-op 已验 PASS; AC-7 abi_compat 5 promises 已验 PASS (代码级)。
  ```bash
  # 节点上: 经 runner 应用 (DB 若停在 v4.2 则升 5.0; 若已 5.0 则 no-op), 再确认列
  sqlite3 <live aria_layer1.db> "SELECT value FROM schema_meta WHERE key='schema_version';"  # 期望 5.0
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
  > ⚠️ **AC-6 false-green 警告** (2026-06-27 AI 干跑发现): 当前空模板的 `cost_usd: 0.00` 占位**也能让 AC-6 PASS** (gate 只看 cost ≤$2, 不看 dispatch_id 是否填)。**AC-6 PASS ≠ pre-flight 真跑过** —— 必须人眼确认 `m6-preflight-log.md` 的 3 个 `dispatch_id` 已填真值 + `m6-preflight-provenance.md` 的 `Selected option` 已选。

### Phase 0 dispatch — ⚠️ 手动 dispatch 路径待修复 (2026-07-02 canary 实证)

> - **provenance A (replay M5 O3) 不可用**: capture 文件 `docs/demo-m5-o3-*.yaml` 不存在 → 用 **B (fresh synthetic)**。
> - **pre-flight ≠ Phase 2 seed**: pre-flight 手动直派 `aria-layer2-runner` (**跳过 Layer 1**, fixture **不打 `aria-auto`** 防 tick 抢派), 只验 Layer 2 管道 + glm-5.2 + AC-6 cost; Layer 1 GLM triage 首验在 **Phase 2** (seed+tick)。
> - **勿在 Phase 0 跑 `seed-aria-auto-issues.sh`** —— 那会让 tick 自动派 = 提前启动时钟。

#### 🔴 2026-07-02 canary 发现: 下方原"裸 nomad job dispatch"配方是坏的

真跑一次 canary (DEMO issue #148, DISPATCH_ID b663f5b2) 证明**旧配方必挂**, 且**成本 $0**(容器在入口 Step 1 就 FATAL, 从未到 LLM)。两处确证缺陷:

1. **ISSUE_ID 正则** (`docker/aria-runner/modes/initial.sh:106` = `^[A-Z][A-Z0-9-]+$`): 传 Forgejo 数字号 (如 `148`) 直接 `FATAL: ISSUE_ID 148 不符合正则`。ISSUE_ID 必须是 `DEMO-M6-P1` 这种大写字母开头的逻辑 ID, 非 issue number。
2. **容器 Step 2 从预置 `issue.yaml` 加载任务** (`initial.sh:142-147`), **不从 `ISSUE_URL` 拉**。裸 `nomad job dispatch` 没 stage 输入 → 即使 ID 合规也会挂 `issue.yaml not found`。`ISSUE_URL` meta 对入口任务加载**无用**。

**正确路径 (原则上)** = `scripts/dispatch-issue.sh <ISSUE_ID>` (它 stage `.aria/issues/<ID>.yaml` + referenced files → `/opt/aria-inputs/<ID>/` → 再 dispatch)。

#### ⚠️ 但 manual dispatch 工具链已与自主路径分叉 — 用前必须先验证/修复

`dispatch-issue.sh` 是 **M1 MVP 遗留**, 尚未确证能对当前 M5 镜像端到端跑通:

- **validator 失效**: `dispatch-issue.sh:82` 引用 `openspec/changes/aria-2.0-m1-mvp/artifacts/validate-issue-schema.py`, 该 spec 已归档 → 路径不存在 (脚本 fallback "skip schema check")。真 `issue.yaml` schema 无 SOT 校验。
- **repo `.aria/issues/` 为空**: 需现写 `DEMO-M6-P1.yaml` (字段: `title` / `files:` list / `metadata.target_repo` / `metadata.base_branch`, 从 `initial.sh:142-245` 反推; 精确 schema 待恢复 validator 确认)。
- **卷在 heavy 节点**: `/opt/aria-inputs` **不在 light-1** (canary 实测), staging 须落到容器实际调度的节点 (dispatch 非确定性 → 需节点约束或共享卷确认)。
- **契约可能分叉**: 自主路径 (`aria_layer1/prompt_render.py`) 把 **`prompt.txt`** 预渲染到 `/opt/aria-inputs/{dispatch_id}/` 供容器消费; manual 路径走 `issue.yaml`。部署的 M5 镜像 (`claude-m5-91b8975-v11`) 入口到底认哪个契约, 未确证。

**→ OWNER 决策 (pre-flight 启动前必须定)**:
- **(A) 修复 manual 路径**: 恢复/重写 issue-schema validator + 写 `.aria/issues/DEMO-M6-P*.yaml` + 理清节点/卷 staging + 确认 M5 镜像入口契约。工作量中等, 但保住"隔离 Layer 2 + 不启动时钟"的 pre-flight 本意。
- **(B) pivot 到自主路径验证**: seed **1 个** `aria-auto` issue 让 tick 派 (已知可跑的 prompt.txt 路径, Hermes tick 认证已核实健康)。代价: engages Layer 1 + 接近启动时钟, 违背 pre-flight "隔离"初衷; 需重新界定它算不算启动 168h。

#### ✅ canary 已证明 (基建健康, 阻塞面收窄)

- 镜像 digest (`5b80ca6...`) 有效, registry **cold-pull 认证正常** (#147 修复生效, 越过 14 次历史 `S4_LAUNCH infrastructure` 失败)。
- 调度到 heavy-2 + 容器正常启动到入口。
- **唯一阻塞 = 输入 staging 契约 (上述 A/B), 非集群基建。**

<details><summary>原坏配方 (存档, 勿直接用 — 见上方缺陷)</summary>

```bash
# ❌ 会 FATAL: ISSUE_ID 数字号不合正则 + 无 issue.yaml staging
ssh light-1; export PATH=$PATH:/usr/local/bin
N=<issue number>
DISPATCH_ID=$(python3 -c 'import uuid;print(uuid.uuid4())'); IDEM=$(python3 -c 'import uuid;print(uuid.uuid4())')
IMAGE_SHA=5b80ca6cd04ab31b3d8165eb82f4ac9edd824b45e8181adf9325e80cf35148f5   # bare hex, HCL 已带 @sha256:
nomad job dispatch -meta ISSUE_ID="$N" -meta ISSUE_URL="https://forgejo.10cg.pub/10CG/Aria/issues/$N" \
  -meta DISPATCH_ID="$DISPATCH_ID" -meta IMAGE_SHA="$IMAGE_SHA" -meta IDEMPOTENCY_KEY="$IDEM" aria-layer2-runner
```
</details>

**跑通后 (A 或 B)**: poll → 读 `result.json` 验 `claude_usage.model=glm-5.2` + cost → 填 `m6-preflight-log.md` (真 dispatch_id + fixture_source + outcome + cost_usd) → 3 次凑齐 → 关 `[DEMO-M6-P*]` issue → 填 `m6-preflight-provenance.md` (option B) → 验 AC-6 → 进 Phase 1。

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
  > **B4 dispatch 语料**: tick 只派 `aria-auto` 标签 issue。用 `./seed-aria-auto-issues.sh --apply` (本目录) 批量造分层 `[DEMO-M6-P*]` 合成 issue (默认 12, 轮流 bug/feature/stale + aria-auto)。**前置**: #147 B4-code (PR #28 issue_type_hint) 已合并 + 部署到 light-1, 否则 dispatch 不带 `issue_type_hint`, AC-2 分层仍失败。跑后清理这些 DEMO issue。
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
