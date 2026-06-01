---
track-id: m6-e2e-resilience-tga
owner-container: simonfishgit/dev-claude
phase: B
status: in_progress
updated-at: 2026-06-01T14:48:00Z
---

# Aria — Session Handoff (2026-06-01 ~14:48 UTC) — M6 e2e-resilience (Spec #2) Phase B: TG-A 代码件全交付 + 验证

> **Status**: 🟢 owner 选定的 **"TG-A 代码件"slice 全部交付并验证** (985 tests green, 2 commits on aria-orchestrator feature 分支)。M6 e2e-resilience Phase B 启动。
> **Type**: `/state-scanner` → 选 M6 e2e-resilience Phase B → 选 TG-A 代码件优先 → infra/validate/uptime/dispatch/acceptance 全做
> **Rule #9 trigger**: 跨多 arc (5 task group) + ship 实质代码 slice + 跨 phase
> **本终端**: dav-claude (simonfishgit/dev-claude) — aria-orchestrator 在 feature 分支 (2 commits, **未 push**);主仓 master + 3 个 .aria/probes/ 待提 + 本 handoff

---

## §0 入口 (新 session 优先读)

1. **本 doc**
2. **⏰ 头号 — 决定 TG-A 后续走向 (3 选 1)**:
   - **(a) TG-B 崩溃恢复套件** (~13h, mock-only 零成本零 owner 依赖) — 最大自包含纯代码 slice, 推荐下一步。
   - **(b) Phase C 集成 TG-A 代码** (merge feature 分支 → 解锁 owner 启动 168h 运营跑) — 提前 merge 子集。
   - **(c) owner 启动 168h 运营跑** (需先做 issue_type_hint 依赖, 见 §3) — 长 pole, owner 驱动。
3. **aria-orchestrator feature 分支** `feature/aria-2.0-m6-e2e-resilience-tg-a` (HEAD `f0acfc5`, 2 commits, **未 push**) — TG-A 全部代码在此。
4. **owner-gated 残留** (不变): #136 Feishu 轮换 / v1.29.0 block-flip (06-07) / Blocker #-1 light-1 节点凭据。

→ **next session 入口**: `/aria:state-scanner` → 读本 doc §6。

---

## §1 已完成 (TG-A 代码件, 5 task group)

| # | task group | 产物 | commit |
|---|-----------|------|--------|
| 1 | **TG-A-infra** | migration `007_schema_v4.3_add_is_synthetic.sql` (is_synthetic, **schema v5.0**) + canonical schema.sql + schema_migrate.py 注册 + `test_schema_column_guard.py` (T-validate-schema-1) + `test_t_schema_v5_0_migration.py` | `b903ee2` |
| 2 | **TG-A-validate** | `test_m6_abi_compat_after_migration_007.py` 配对三测 (触发器存活 + 无 trigger-drop + validate exit 0) | `b903ee2` |
| 3 | **T-docs** | AD-M6-4 (decided+impl) + AD-M6-5/6 (reserved) in architecture-decisions.md | `b903ee2` |
| 4 | **TG-A-uptime + dispatch + acceptance** | `acceptance/check-m6-e2e-acceptance.py` (AC-1 alloc 168h gate + 7-probe + Day-3 / AC-2 分层 SQL / AC-6 preflight / AC-7 abi_compat delegate) + `tests/acceptance/test_m6_e2e_acceptance.py` (22 测) | `f0acfc5` |
| 5 | **模板 + gate 记录** (主仓 .aria/probes/) | `m6-gate-check.md` (A-infra-1 PASS 记录) + `m6-preflight-provenance.md` + `m6-preflight-log.md` | 待提交 |

**测试**: aria-layer1 **864** + aria-orchestrator tests/ **121** (含新 22 acceptance) = **全绿, 零回归**。
**回归 sweep**: 6 个现存 schema/acceptance 测试文件 4.2→5.0 latest pin + applied 列表加 "007" (milestone bump 预期 blast radius)。
**real-env smoke**: AC-7 PASS / AC-1 优雅报 missing anchor (rc=2, 7d 未跑) / AC-6 PASS (模板占位)。

---

## §2 未完成 / Carry-forward 清单

| 优先级 | 项 | 类型 | 说明 |
|--------|-----|------|------|
| **P1** | **TG-B 崩溃恢复套件** | 纯代码 (~13h) | 6-mode + 4 WAL + 状态机 100% det cov + AdvancingClock DI + `m6-wal-fault.sh`。mock-only 零成本零 owner 依赖, 下一步首选。tasks.md §TG-B-* |
| **P1.5** | **issue_type_hint 运营依赖** | 阻断 AC-2 真跑 | 见 §3。生产 dispatcher 不写该 payload key → AC-2 分层永远查到 0。168h 跑前必须建立/核实真 key。 |
| **P2** | TG-C 拟人样本 | 依赖 7d 跑产物 | rubric + 10 sample/score 模板可先写 (~2h), 内容待跑后填 |
| **owner** | 168h E2E 运营跑 | wall-clock + $6 | Day-1 alloc anchor 记录 + 3 pre-flight 真 dispatch + 每日 probe + Day-3 gate + owner 评分 |
| **owner** | #136 Feishu 轮换 / Blocker #-1 节点凭据 / v1.29.0 06-07 | 不变 | — |

---

## §3 关键风险 / 已知陷阱 (本 session 实证)

1. **⚠️ issue_type_hint 运营依赖 (最重要)**: AC-2 分层 SQL 读 `json_extract(dispatch_audit_log.payload_json, '$.issue_type_hint')`, 但**核实生产代码 `append_audit_log` 当前不写该 key** (payload 是通用 dict)。后果: 真 168h 跑时 AC-2 bug/feature/stale 分层永远查到 0 → AC-2 FAIL。**168h 跑启动前必须**: 要么增强 dispatcher 在 S0_IDLE 写 `issue_type_hint`, 要么把常量 `_ISSUE_TYPE_HINT_KEY` 映射到真实已写的 payload key。已 flag 进 `check-m6-e2e-acceptance.py` docstring + AC-2 注释。
2. **3 个 spec-vs-reality drift (均按真代码修正)**:
   - schema 版本值 **5.0** (spec 文件名 "v4.3" 是 erratum; 约定=每 milestone 主版本 M5=4.0→M6=5.0, 已在 migration header + AD-M6-4 + schema.sql 注释记档)。
   - DB 文件名 **dispatches.db** (tasks A-dispatch-1 误写 `aria_layer1.db`; Spec #1 C-R1-2 SoT 明确 dispatches.db)。
   - `validate-m6-handoff.py --check-abi-compat` **静默 exit 0 不 echo promise token** (tasks A-validate-1 Test-3 的 stdout-token 断言是错的; AC-7 + 我的 validate 三测均只依赖 returncode, 已规避)。
3. **migration 注释踩子串陷阱**: migration header 原含 "DROP TRIGGER" 字面量 → naive 子串 abi_compat 检查会 false-positive 自己 ([[feedback_word_boundary_root_causes_substring_shadows]])。改注释措辞 + 测试用 `_strip_sql_line_comments` 语义检查双修。
4. **milestone schema bump 的 blast radius**: 把 _LATEST 4.2→5.0 后, 凡 seed 在旧 latest 再 `apply_migrations` 的测试会真 cascade 应用 007 触发 post-migration transform/backfill (需更全列 seed)。生产 DB 有全列无害; 仅最小 seed 测试需补列 (006 idempotent 测试已重构为 double-apply + 补 3 列)。

---

## §4 实战教训 (memory 候选)

1. **复用/断言下游 payload key 前必核实生产代码确实写它** —— spec 的 `$.issue_type_hint` 是占位符, 生产 dispatcher 实际不写 → 否则验收 gate 永远查 0 (created_at-class 教训再现, 本 session AC-2)。*(候选, 与 [[feedback_rebenchmark_test_diagnosis_not_metric]] 同源, 可不新增)*
2. **milestone schema 主版本 bump 的测试 blast radius 是机械但必然的** —— 凡 pin "latest version" 的测试都要随 bump 更新; cascade 测试的最小 seed 需补 post-migration steps 触及的列。
3. (既有强化) spec 文本 vs 真实代码 drift 在实施期高频出现 (本 session 3 处), 一律以真代码为准并记 erratum, 不盲从 spec 字面。

---

## §5 多维度同步状态 (Aria 4 维度)

| 维度 | 状态 | 说明 |
|------|------|------|
| **UPM** | **N/A** | Aria self `upm.configured=false` ([[project_aria_no_runtime_upm]]) |
| **US** | ⏸️ 无需改 | US-026 (M6) 仍 in_progress; Spec #2 Phase B 进行中, 未完成不改 US |
| **Spec** | ⏸️ 进行中 | `aria-2.0-m6-e2e-resilience` Approved, TG-A 代码 done, TG-B/C + 运营跑未做; **未归档** |
| **PRD** | 无需改 | 不动里程碑 |

---

## §6 Next session 入口 + 优先级建议

**入口**: `/aria:state-scanner` → 读本 doc。

**优先级**:
1. **[P1]** 决定 TG-A 后续 (§0.2 三选一)。推荐 **TG-B 崩溃恢复套件** (最大自包含纯代码, 零 owner 依赖, ~13h)。
2. **[P1.5]** 真 168h 跑启动前先解 **issue_type_hint 运营依赖** (§3.1) —— 否则 AC-2 永远 FAIL。
3. **[P2]** TG-C 模板可先写 (内容待跑后填)。
4. **[owner]** #136 轮换 / v1.29.0 block-flip 06-07 / Blocker #-1 节点凭据。

**若选 Phase C 集成 TG-A 代码**: aria-orchestrator 仅 `origin` 远程 (无 github); pre-merge gate (Rule #8) 无 CI backend → skip_with_warning; merge 后主仓 gitlink bump + .aria/probes/ 一起提。

---

## §7 提交清单 (commit hash + parity)

| 仓 | HEAD | 远程 | 本 session 提交 |
|----|------|------|------------------|
| **aria-orchestrator** | `f0acfc5` (feature 分支 `feature/aria-2.0-m6-e2e-resilience-tg-a`) | **未 push** ⚠️ | `b903ee2` (TG-A-infra+validate) + `f0acfc5` (TG-A acceptance) |
| **主仓 Aria** | master (gitlink 仍 `1b69564`, 未 bump) | — | 待提: 3 .aria/probes/ + 本 handoff |
| **standards** | `95cbdc9` | ✓ | 未改 |

> ⚠️ **aria-orchestrator feature 分支未 push** —— 工作仅在本地 (2 commits 已落, 但未推 origin)。若担心丢失或跨终端可见, 建议 `git -C aria-orchestrator push origin feature/aria-2.0-m6-e2e-resilience-tg-a`。

---

## §8 Memory entries this session

0 new committed (候选见 §4, 与既有 memory 同源, 可下 session 评估是否新增)。

---

## Cross-references

- Spec: `openspec/changes/aria-2.0-m6-e2e-resilience/` (proposal + tasks, Approved 2026-05-24 R3 STABLE)
- 代码 (aria-orchestrator feature 分支): `acceptance/check-m6-e2e-acceptance.py` + `hermes-extensions/aria-layer1/aria_layer1/migrations/007_*.sql` + `.../schema.sql` + `.../schema_migrate.py` + 4 新测试文件 + `docs/architecture-decisions.md` AD-M6-4/5/6
- gate: `.aria/notes/2026-06-01-m6-phase-b-gate-result.md` (Spec #1 AC-7 PASS, 解锁本 Phase B)
- 前序 handoff: `2026-06-01-0441-state-scanner-diagnosis-71-72-spec.md` (M6 AC-7 闸 PASS, 解锁本 Phase B)
