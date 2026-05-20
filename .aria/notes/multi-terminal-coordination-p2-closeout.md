# multi-terminal-coordination P2 Layer L Closeout + P3 Entry Checklist

> **Date**: 2026-05-20
> **Spec**: `openspec/changes/multi-terminal-coordination/`
> **Branch**: `feature/multi-terminal-coordination`(Aria 主仓 + standards + aria-plugin)
> **P2 status**: ✅ 13/13 atomic tasks shipped + Round 8 audit (READY_TO_MERGE / SHIP_NOW) + 108 tests PASS
> **Audit reports**: P1 closeout note + Round 6 (P1) + Round 8 (P2)

---

## P2 ship snapshot

| Round | Task | Title | aria-plugin SHA |
|-------|------|-------|-----------------|
| R1 | TASK-010 | claim YAML schema v1 + coordination-ref-schema doc | (in 313b6c4) |
| R1 | TASK-011 | identity (owner/container/session) + 持久化 | (in 313b6c4) |
| R1 | TASK-014 | 确定性 track-id 派生函数 | (in 313b6c4) |
| R2 | TASK-012 | orphan ref bootstrap | `99ce0d2` |
| R3 | TASK-013 | claim CRUD + push/fetch (file-per-writer) | `e0de899` |
| R4 | TASK-018 | lifecycle + constants + GC + **Finding #3 closed** | `355c143` |
| R5 | TASK-015 | reconcile 4-rule deterministic protocol | (in dcf41d5) |
| R5 | TASK-019 | failure_handlers 7-case resilient wrapper | (in dcf41d5) |
| R6 | TASK-016 | phase1_gate 9-step 急切认领闸门 | (in f9306a0) |
| R6 | TASK-017 | track_board collision render upgrade (reconcile-based) | (in f9306a0) |
| R7 | TASK-020 | reconcile golden table tests (55) | (in cf79975) |
| R7 | TASK-021 | race window tests (12, threading.Barrier zero-sleep) | (in cf79975) |
| R7 | TASK-022 | failure injection tests (23, 7-case mock.patch) | (in cf79975) |

**Aria 主仓 feature 分支 HEAD**: `6d48016`

**Cumulative state**(P1 + P2 combined):
- 22/22 atomic tasks shipped
- 108 tests PASS in 1.381s (18 P1 + 90 P2)
- full state-scanner suite: 568 tests PASS in 5.4s
- ~3000 lines code + ~2000 lines tests
- 3-way SHA parity verified throughout (Aria 主仓 + aria-plugin + standards × forgejo + github)

---

## Round 8 Final Audit Verdict

### tech-lead — PASS_WITH_WARNINGS / **READY_TO_MERGE**
- 6 minor findings, all `blocks_merge: no`
- "P2 Layer L 13 atomic ship 构成完整、内聚的协调机制 ... DEC-20260519-001 5 决策全部实现且 final 一致"
- "108 tests / ~5500 行实现代码 ≈ 0.55 ratio 健康"
- "关键架构成就:6-rule reconcile 含 sole_active+stale_takeover_eligible 优雅边角 + clock-skew CONFLICT 不静默 + schema v2 forward-compat unknown sentinel"

### code-reviewer — PASS_WITH_WARNINGS / **SHIP_NOW**
- 9 minor findings (3 deliverable deferred + 6 style/lint), all `blocks_merge: no`
- **Zero critical or major issues**
- "Rule #7 audit clean — every subprocess invocation routes through _run with capture_output=True"
- "Rule #9 frontmatter ↔ claim YAML schema alignment verified. No circular imports; one-way dependency DAG"
- "Race window test uses threading.Barrier — zero sleep, non-flaky"
- "Architecture and testing discipline materially exceed P1's quality bar"

---

## 15 Findings dispositioned

### 共识 actionable(已在本 closeout commit 处理)

- **D-1 tasks.md 22 checkbox 未勾选** → ✅ 本 commit 已批量 tick 1.1-1.9 + 2.1-2.10

### Deferred to P3(merge_order 一致)

- **TASK-018 gc.archive_done_claims `dry_run=False` 写路径**: 当前 log WARNING + 返回元数据 metadata 但未实际 git mv;P3 GC 调度器集成自然落地。**Code-reviewer 已确认**:"P3 GC scheduler integration is the natural home for write wiring"
- **TASK-018 heartbeat 周期 push (10min) 调度器**: API 已 ship + 单测;实际周期调用由 caller (e.g. phase-b-developer mid-cycle)。**Code-reviewer 已确认**:"acceptable for sub-PR; aligns with merge_order"
- **TASK-022 "降级行为符合规范率 ≥ 90%"**: 7 case 全部 deterministic PASS(23/23 = 100%);"≥ 90% rate" 是 P3 TASK-026 Rule #6 benchmark.yaml 的 量化基线;非单元测试阈值
- **Rule #6 structural benchmark** 整体延后 → TASK-026/027 (P3) 实施
- **phase1_gate 与 state-scanner 主流程集成** → P3 TASK-024 worktree 触发流程入口

### Cleanup follow-up(进 P3 hygiene commit 一次性清)

- 双上下文 import 模板(try/relative + except/sys.path)在 3 处重复 → P3 提取 `_dual_context_import.py` 或 packaging fix
- `lib/reconcile.py` 不用的 `timedelta` import — 删除
- `lib/coordination_ref.py` 函数内的 `import os as _os_run` → 提到模块顶
- `lib/__init__.py` 模块 docstring 说"后续 P2 task 将加入" 而下方 import 已含 → 同步更新 docstring
- `failure_handlers._resolve_ref` cross-module private name access → 暴露公共 helper 或文档化 intentional package-internal API
- `verdict_reason` 自由格式字符串 → typed enum 或文档化 composition 规则
- `_TERMINAL_STATUSES` 在 reconcile.py 和 claim_lifecycle.py 各有不同 membership → 加 cross-ref 注释或改名 disambiguate
- normalize_snapshot flaky 测试(P1 域)→ P3 加 per-test fixture isolation 清 30s TTL cache
- `parse_claim` / `serialize_claim` lazy import 在 coordination_ref.py 内 → 验证后可提到模块顶(无 actual circular)

### 设计行为差异(已 documented,非 bug)

- **reconcile: missing/unparseable heartbeat → NOT stale**(保守):reconcile.py docstring 明示;若希望立即可接管,改为 stale 即可(P3 决策点,non-blocking)
- **stale_ttl + clock_skew boundary 是严格 `>`**(exclusive):exactly 阈值 → NOT trigger;tests B.2/CS.2 已 document + assert
- **`yielded` 非 terminal**(reconcile 视同 active candidate);若希望视同 terminal,改 `_TERMINAL_STATUSES` 即可
- **abandoned vs done 语义合并**:reconcile 视 abandoned 同 terminal;claim_schema STATUS_WRITABLE 不含 abandoned。功能等价 done — 是否在 v2 schema 中显式表达?P3 决策点

---

## P3 Entry Checklist

启动 P3 第一个 task 前确认:

- [x] P2 Layer L 13/13 ship + Round 8 audit reviewed (READY_TO_MERGE)
- [x] 108 tests PASS (P1 18 + P2 90)
- [x] tasks.md 22 done checkbox 勾选(本 commit)
- [ ] **(可选 pre-flight)** Cleanup follow-up patch:dead imports + docstring stale 句 + lazy imports promote(~30 min 一次性 hygiene)
- [ ] **(P3 必做)** phase1_gate 集成到 state-scanner 主流程(TASK-024 worktree 触发流程入口)
- [ ] **(P3 必做)** Rule #6 structural benchmark 4 维度阈值 → TASK-026/027
- [ ] **(P3 必做)** dogfood ≥1 多终端 cycle + e2e 集成 test → TASK-028(同时填补 R8 tech-lead surfaced "e2e two-clone real push/fetch" 测试 gap)
- [ ] **(P3 必做)** gc.archive_done_claims 写路径实施(若 P3 scheduler 集成)
- [ ] **(C.2 fanout)** 跨 3-repo merge 顺序:standards → aria-plugin → 主仓 gitlink re-bump

---

## P3 task DAG(8 atomic,~14h 估时)

```
P3 = Design A 条件触发 + Rule #6 benchmark + Dogfood (~14h)

TASK-023 (S, 1h) — 同容器并发 active claim 计数检测 [deps TASK-013 ✓]
TASK-024 (M, 2h) — worktree 自动创建 + 子模块独立 checkout + B.1 钩入 [deps TASK-023]
TASK-025 (S, 1h) — worktree 生命周期(release 清理 + 误用保护)[deps TASK-024 + TASK-018]
TASK-026 (M, 2h) — Rule #6 structural benchmark 设计(4 量化指标)[deps TASK-022 ✓]
TASK-027 (S, 1h) — 执行 /skill-creator benchmark 存入 ab-results [deps TASK-026]
TASK-028 (L, 3h) — Aria 主仓 dogfood ≥1 cycle + observable instrumentation [deps TASK-027]
TASK-029 (M, 2h) — 文档同步 5-layer enforcement matrix 全覆盖 [deps TASK-001/002/009 ✓]
TASK-030 (M, 2h) — 跨 3-repo C.2 + Rule #8 gate + Phase D 归档 [deps TASK-028 + TASK-029]
```

---

## Cross-references

- Spec: `openspec/changes/multi-terminal-coordination/{proposal,tasks,detailed-tasks}.{md,yaml}`
- Decision: `docs/decisions/DEC-20260519-001-multi-terminal-coordination.md`
- P1 closeout: `.aria/notes/multi-terminal-coordination-p1-closeout.md`
- post_spec R1+R2 audits: `.aria/audit-reports/post_spec-{R1,R2}-2026-05-19*-summary.md`
- Round 6 audit (P1, informal): aria 7fe50de hygiene commit
- Round 8 audit (P2, post_implementation): 本 closeout note 总结部分
- Memory: `feedback_concurrency_advisory_over_hardlock`(local-only,non-git-tracked)
