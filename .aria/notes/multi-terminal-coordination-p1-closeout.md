# multi-terminal-coordination P1 Layer H Closeout + P2 Entry Checklist

> **Date**: 2026-05-20
> **Spec**: `openspec/changes/multi-terminal-coordination/`
> **Branch**: `feature/multi-terminal-coordination` (Aria 主仓 + standards + aria-plugin)
> **P1 status**: ✅ 9/9 atomic tasks shipped + Round 6 audit reviewed + 18 tests PASS
> **Audit reports**: `.aria/audit-reports/post_spec-{R1,R2}-*-multi-terminal-coordination-summary.md` + Round 6 informal review (tech-lead + code-reviewer parallel)

---

## P1 ship snapshot

| Task | Title | aria-plugin SHA | Status |
|------|-------|-----------------|--------|
| TASK-001 | standards §2.3 frontmatter schema | (standards `03ddfd0`) | ship |
| TASK-002 | template frontmatter head | `6cb110f` | ship |
| TASK-003 | coordination_fetch + 30s TTL cache | `f086bb8` | ship |
| TASK-007 | offline degradation (extend 003) | `776498b` | ship |
| TASK-009 | Rule #9 5-layer matrix + L1/L2 helpers | `52bc897` | ship |
| TASK-004 | handoff_multibranch + scan.py 集成 | `914de60` | ship |
| TASK-005 | track_board renderer | `8899443` | ship |
| TASK-006 | latest_md_writer (single/multi/zero) | `7907fd9` | ship |
| TASK-008 | P1 test suite (18 PASS) | `9ec00db` | ship |
| Hygiene | Round 6 trivial fixes (3 minor) | `7fe50de` | ship |

Aria 主仓 feature 分支 HEAD: `3481f8f`(含全部子模块 pointer bump,3-way SHA parity 已验证)

---

## 4 major findings — 决策与归宿

### Finding #2 — `latest_md_writer` call-site integration (RESOLVED — 决策记录)

**决策**: 采纳 tech-lead 建议 (b) — **显式文档化 writer 是 D.3-scoped,P1 防接错棒来自 board 渲染本身,不在 P1 加 production call-site**。

理由(Aria 原则):
- **规范先行**: P1 标榜"纯读零行为变更",加 scan.py 自动写 latest.md 违反此承诺
- **向后兼容**: P1 不重写 latest.md,意味着老 session 看到的 latest.md 仍是 git 历史中由 phase-d-closer 上次写的内容(向后兼容老 reader)
- **职责单一**: writer 由 `phase-d-closer` D.3 step 调用 — 它本来就负责"session 结束写新 handoff + 更新 latest.md",writer 是 D.3 的工具
- **多 track 防接错棒** 由 `render_track_board(snapshot)` 提供(读全分支 frontmatter 重建看板),**不依赖 latest.md**

**Action items**:
- ✅ 本 closeout commit 在 SKILL.md TASK-006 TODO 块上注明此决策
- ⏸ phase-d-closer SKILL 更新调用 writer — 归入 `TASK-029`(P3 文档同步)或新增独立 atomic task,**P2 不依赖**
- 用户层影响: 老 session `cat docs/handoff/latest.md` 仍正常;多 track 真实 surface 经 `/aria:state-scanner` 看板

### Finding #1 — PyYAML hard-dependency 未文档化 (DEFERRED → TASK-029)

**决策**: 延后至 `TASK-029` 文档同步阶段。理由:
- 不影响 P2 设计决策
- 当前 graceful fallback (legacy 标 + soft_error) 已确保运行时不崩溃
- aria-plugin 的 `pyproject.toml` / `setup.py` 已应含 pyyaml(待 TASK-029 验证),只需在 SKILL.md / README 明示

**P2 action**: 不阻塞 P2 任何 task。Carry-forward to TASK-029。

### Finding #3 — Constants 双源风险 (DEFERRED → TASK-018 entry criterion)

**决策**: P2 `TASK-018` 实施时**显式 migrate**。track_board.py / latest_md_writer.py 已在文档注释中提示常量来源应在 P2 后切换。

**TASK-018 实施时必做**:
1. `aria/skills/state-scanner/lib/constants.py` 含 `HEARTBEAT_INTERVAL=600` / `STALE_TTL=1800` / `CLOCK_SKEW_WARN_THRESHOLD=30`
2. `track_board.py` 顶部 `from ..lib.constants import HEARTBEAT_INTERVAL, STALE_TTL` 替换本地常量
3. `latest_md_writer.py` 若有依赖常量同步

**P2 不阻塞**:TASK-018 早期 task,自然在 reconcile/gate 之前完成。

### Finding #4 — `git show` 缺 `--` defensive separator (DEFERRED — minor)

**决策**: 保留现状,加 1 行注释说明。理由:
- `git for-each-ref` 已过滤合法 branch ref,不可被注入
- 风险 < 1 line code change benefit
- code-reviewer 自己评 "实际可保留"

**Action**: 本 closeout commit 在 `handoff_multibranch.py` `_git_show` 函数加 inline 注释。

---

## P2 entry checklist (Layer L Orphan ref + 急切认领 + reconcile)

在启动 P2 第一个 task 前确认:

- [x] P1 Layer H 9/9 ship + audit reviewed + tests PASS(本 doc 即闭环记录)
- [x] Finding #2 决策记录(本节)
- [x] Finding #3 TASK-018 entry criterion 文档化(本节)
- [x] Finding #1/#4 deferred 路径明确(本节)
- [ ] **(Round 1 启动前)**Spawn 3 个并行 agent: TASK-010(schema)+ TASK-011(identity)+ TASK-014(track-id derivation)— 全部 independent
- [ ] **(P2 收尾)**triggered Rule #6 structural benchmark — 归入 `TASK-026/027`(P3)
- [ ] **(P2 收尾)**复查 Finding #3 实施(TASK-018 是否真的迁移常量)

## P2 task DAG(13 atomic,~26h 估时)

```
独立起点(并行 Round 1):
  TASK-010 (M, 2h) — claim schema design
  TASK-011 (M, 2h) — identity gen + persistence
  TASK-014 (S, 1h) — track-id derivation

  ↓ (Round 2)
TASK-012 (S, 1h) — orphan ref bootstrap [deps 010]

  ↓ (Round 3)
TASK-013 (M, 3h) — claim CRUD + push/fetch [deps 010, 011, 012]

  ↓ (Round 4)
TASK-018 (M, 2h) — lifecycle + constants + GC [deps 013]
                   ⚠ Finding #3 implementation point

  ↓ (Round 5 — parallel)
TASK-015 (M, 2h) — reconcile protocol [deps 013, 018]
TASK-017 (M, 2h) — collision row + clock skew [deps 005, 015]

  ↓ (Round 6 — parallel)
TASK-016 (L, 3h) — eager claim gate [deps 013, 014, 015]
TASK-019 (L, 3h) — failure handling matrix [deps 013, 018]

  ↓ (Round 7 — parallel tests)
TASK-020 (M, 2h, QA) — reconcile golden table tests [deps 015]
TASK-021 (M, 2h, QA) — race window test (ClockProvider) [deps 015, 016]
TASK-022 (S, 1h, QA) — failure injection tests [deps 019]
```

---

## Cross-references

- Spec: `openspec/changes/multi-terminal-coordination/{proposal,tasks,detailed-tasks}.{md,yaml}`
- Decision: `docs/decisions/DEC-20260519-001-multi-terminal-coordination.md`
- post_spec audits: `.aria/audit-reports/post_spec-{R1,R2}-2026-05-19*-summary.md`
- Round 6 audit: 非正式 (audit-engine post_implementation=off),tech-lead + code-reviewer 并行 review(详见本 closeout note 总结部分)
- Round 6 hygiene patch commit: aria `7fe50de`
