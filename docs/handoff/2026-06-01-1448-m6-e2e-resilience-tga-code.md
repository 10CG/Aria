---
track-id: m6-e2e-resilience-tga
owner-container: simonfishgit/dev-claude
phase: B
status: in_progress
updated-at: 2026-06-01T17:10:00Z
---

# Aria — Session Handoff (2026-06-01 ~14:48 UTC) — M6 e2e-resilience (Spec #2) Phase B: TG-A 代码件全交付 + TG-B recon→#138 缺陷+LLM 子集

> **Status**: 🟢 **TG-A 代码件全交付** (985 tests) + **TG-B 全部完成** (recon→#138 缺陷→Phase A rework owner 批准→覆盖矩阵 doc + 已交付 gap + B-sm-1 转换表 drift-guard; 879 tests green)。feature 分支 5 commits (`97f979b`) + 主仓 spec amend。**M6 Spec #2 代码侧 TG-A+TG-B 全交付; 剩 = 168h 运营跑 (owner) + TG-C (依赖跑)**。
> **Type**: `/state-scanner` → M6 e2e-resilience Phase B → TG-A 代码件优先 (infra/validate/uptime/dispatch/acceptance) → 再 TG-B (recon→#138 缺陷+LLM crash 子集)
> **Rule #9 trigger**: 跨多 arc (TG-A 5 task group + TG-B recon/issue/subset) + ship 实质代码 + 跨 phase
> **本终端**: dev-claude (simonfishgit/dev-claude) — aria-orchestrator feature 分支 3 commits (`85b8f46`, origin 到 `f0acfc5`, **末 commit 待 push**);主仓 master 已提 handoff+probes 并双远程 push

---

## §0 入口 (新 session 优先读)

1. **本 doc**
2. **TG-A + TG-B 代码侧全部完成** (TG-B Phase A rework + B-sm-1 done)。M6 Spec #2 剩余 = **168h 运营跑 (owner)** + **TG-C 拟人样本 (依赖跑)**。
3. **⏰ 头号候选**: (a) **Phase C 集成** (merge feature 分支 → 主仓 gitlink bump + .aria/probes 提 → 解锁 owner 168h 运营跑) 或 (b) **TG-C 模板** (~2h, 内容待跑后填) 或 (c) 对 TG-B rework 跑 focused post_spec audit (可选, 风险低)。
4. **issue_type_hint 运营依赖** (§3.1): 真 168h 跑前必须建立, 否则 AC-2 永远 FAIL。
5. **aria-orchestrator feature 分支** `feature/aria-2.0-m6-e2e-resilience-tg-a` (HEAD `97f979b`, 5 commits) — TG-A 全部 + TG-B (LLM 子集 + 矩阵 doc + B-sm-1)。
6. **owner-gated 残留** (不变): #136 Feishu 轮换 / v1.29.0 block-flip (06-07) / Blocker #-1 节点凭据。

→ **next session 入口**: `/aria:state-scanner` → 读本 doc §6。

---

## §1 已完成 (TG-A 代码件, 5 task group)

| # | task group | 产物 | commit |
|---|-----------|------|--------|
| 1 | **TG-A-infra** | migration `007_schema_v4.3_add_is_synthetic.sql` (is_synthetic, **schema v5.0**) + canonical schema.sql + schema_migrate.py 注册 + `test_schema_column_guard.py` (T-validate-schema-1) + `test_t_schema_v5_0_migration.py` | `b903ee2` |
| 2 | **TG-A-validate** | `test_m6_abi_compat_after_migration_007.py` 配对三测 (触发器存活 + 无 trigger-drop + validate exit 0) | `b903ee2` |
| 3 | **T-docs** | AD-M6-4 (decided+impl) + AD-M6-5/6 (reserved) in architecture-decisions.md | `b903ee2` |
| 4 | **TG-A-uptime + dispatch + acceptance** | `acceptance/check-m6-e2e-acceptance.py` (AC-1 alloc 168h gate + 7-probe + Day-3 / AC-2 分层 SQL / AC-6 preflight / AC-7 abi_compat delegate) + `tests/acceptance/test_m6_e2e_acceptance.py` (22 测) | `f0acfc5` |
| 5 | **模板 + gate 记录** (主仓 .aria/probes/) | `m6-gate-check.md` (A-infra-1 PASS 记录) + `m6-preflight-provenance.md` + `m6-preflight-log.md` | `34494ae` (主仓) |
| 6 | **TG-B recon → 缺陷 + LLM 子集** | **Forgejo #138** (TG-B-infra mock 面虚构 + 重复 M3 覆盖) + `test_crash_llm_provider_error_s_fail.py` (5 测, handler `except→S_FAIL(PROVIDER_5XX)` 真实分支) | `85b8f46` |
| 7 | **TG-B Phase A rework** (owner 批准 reframe) | 分析 doc `tgb-rework-analysis.md` (`ca0a163`) + #138 评论 10930 + **覆盖矩阵 doc** `crash-recovery-coverage-matrix.md` (`5f56584`) + spec amend proposal§B/AC-3/tasks TG-B (`2b5918d`, 净 -317 行) | 见右 |
| 8 | **TG-B B-sm-1** (确定性转换表 drift-guard) | `test_transition_table_determinism.py` (10 测: 3-表一致性 + assert_legal_transition 行为 + 终态无出边) + tasks B-sm-1/B-matrix-2 标 done | `97f979b` |

**测试**: aria-layer1 **869** (含新 5 LLM crash) + aria-orchestrator tests/ **121** (含新 22 acceptance) = **全绿, 零回归**。
**回归 sweep**: 6 个现存 schema/acceptance 测试文件 4.2→5.0 latest pin + applied 列表加 "007" (milestone bump 预期 blast radius)。
**real-env smoke**: AC-7 PASS / AC-1 优雅报 missing anchor (rc=2, 7d 未跑) / AC-6 PASS (模板占位)。

### TG-B recon 关键发现 + rework (→ #138, owner 批准 reframe)
两个错误: **(A) mock 符号虚构** (`hermes_client`/`layer2_client`/`recovery.py`/`ProcessKilledError`/`AllocTerminatedError` 全不存在; aria-layer1 是 Hermes plugin 不调 Hermes) + **(B) recovery 模型错** (spec 全写 →S_FAIL, 真实是**三模型**: 进程 kill→**auto-resume from DB** / WAL→**durability** / LLM+死 alloc→**S_FAIL**)。全 6 模式已被既有 M2/M3 测试覆盖 (`test_t12`/`test_t7_crash_recovery`/`test_t2_alloc_status_provider`(ExitCode 137=SIGKILL)/`test_t22_t23`/`test_t9`) + 本 session 1 新测。
**rework (owner 批准)**: TG-B = 覆盖矩阵 doc (映射 6 模式→既有测试+正确模型) + 已交付 gap + B-sm-1 确定性转换表 only (非 100% line cov 4500 行)。重估 ~13h→~2-3h。**B-matrix-2 验证: 75 权威 crash-recovery 测试 PASS**。**B-sm-1 完成** (`97f979b`): survey 确认逐状态转换已覆盖, 真实 gap = 转换表 3 表示一致性 (extension.TRANSITION_TABLE/transitions.LEGAL_TRANSITIONS_FULL/interfaces.LEGAL_TRANSITIONS 仅有弱 len==9 检查) + assert_legal_transition 行为未测 → `test_transition_table_determinism.py` (10 测 drift-guard)。**TG-B 全部完成** (879 tests green)。

---

## §2 未完成 / Carry-forward 清单

| 优先级 | 项 | 类型 | 说明 |
|--------|-----|------|------|
| **P1 🚫** | **TG-B-infra + statemachine 重做** | **blocked on #138** | spec mock 面虚构 + 重复 M3 覆盖 → 需 Phase A rework (映射 6-mode 到 test_t12/test_t22_t23 + 更正 mock 目标 + 重估 100% cov scale)。**不要盲目实施**。LLM 子集已做 (§1.6)。 |
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
1. **[P1]** **Phase C 集成** (merge feature 分支 → 解锁 owner 168h 运营跑)。aria-orch 仅 origin (无 github); pre-merge gate 无 CI backend → skip_with_warning; merge 后主仓 gitlink bump + .aria/probes/ 一起提。
2. **[P1.5]** 真 168h 跑启动前先解 **issue_type_hint 运营依赖** (§3.1) —— 否则 AC-2 永远 FAIL。
3. **[P2]** TG-C 模板可先写 (内容待跑后填) / 对 TG-B rework 跑 focused post_spec audit (可选)。
4. **[owner]** 168h 运营跑 / #136 轮换 / v1.29.0 block-flip 06-07 / Blocker #-1 节点凭据。

---

## §7 提交清单 (commit hash + parity)

| 仓 | HEAD | 远程 | 本 session 提交 |
|----|------|------|------------------|
| **aria-orchestrator** | `97f979b` (feature 分支 `feature/aria-2.0-m6-e2e-resilience-tg-a`, 5 commits) | origin 到 `5f56584` (`97f979b` 待 push) | `b903ee2` (TG-A-infra+validate) + `f0acfc5` (TG-A acceptance) + `85b8f46` (TG-B LLM 子集) + `5f56584` (覆盖矩阵) + `97f979b` (B-sm-1 转换表 drift-guard) |
| **主仓 Aria** | master `05a2104` | origin/github 到 `05a2104` (tasks.md B-sm-1 done 待提) | `34494ae`/`860895c`/`ca0a163`/`2b5918d`/`05a2104` + 本次 tasks.md B-sm-1/matrix-2 标 done; gitlink 仍 `1b69564` 未 bump |
| **standards** | `95cbdc9` | ✓ | 未改 |
| Forgejo | — | — | **10CG/Aria #138** (open) + 评论 10930 (rework 分析) |

> ⚠️ 待 push: aria-orch `97f979b` (origin) + 主仓 tasks.md B-sm-1 commit (origin+github)。

---

## §8 Memory entries this session

0 new committed (候选见 §4, 与既有 memory 同源, 可下 session 评估是否新增)。

---

## Cross-references

- Spec: `openspec/changes/aria-2.0-m6-e2e-resilience/` (proposal + tasks, Approved 2026-05-24 R3 STABLE)
- 代码 (aria-orchestrator feature 分支): `acceptance/check-m6-e2e-acceptance.py` + `hermes-extensions/aria-layer1/aria_layer1/migrations/007_*.sql` + `.../schema.sql` + `.../schema_migrate.py` + 5 新测试文件 (含 `test_crash_llm_provider_error_s_fail.py`) + `docs/architecture-decisions.md` AD-M6-4/5/6
- **Forgejo #138**: TG-B spec 缺陷 (Infra-1/2/3 mock 虚构 + 重复 M3 覆盖, 需 Phase A rework) https://forgejo.10cg.pub/10CG/Aria/issues/138
- gate: `.aria/notes/2026-06-01-m6-phase-b-gate-result.md` (Spec #1 AC-7 PASS, 解锁本 Phase B)
- 前序 handoff: `2026-06-01-0441-state-scanner-diagnosis-71-72-spec.md` (M6 AC-7 闸 PASS, 解锁本 Phase B)
