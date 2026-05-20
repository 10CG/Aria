# multi-terminal-coordination P3 Closeout + Release-Ready Note

> **Date**: 2026-05-20
> **Spec**: `openspec/changes/multi-terminal-coordination/`
> **Branch**: `feature/multi-terminal-coordination`(Aria 主仓 + standards + aria-plugin 三 repo)
> **P3 status**: ✅ 8/8 atomic implementation done;**release + Phase D.2 archive owner-gated**
> **aria-plugin version**: 1.21.4 → **1.22.0**(MINOR bump,本 spec ship)

---

## P3 ship snapshot

| Round | Task | Title | Status | aria-plugin SHA |
|-------|------|-------|--------|-----------------|
| R1 | TASK-023 | concurrent_tracks (Design A 触发) | ✅ done | 21b567d |
| R1 | TASK-026 | Rule #6 structural benchmark.yaml 设计 | ✅ done | (Aria 主仓) |
| R1 | TASK-029 | 5-layer matrix doc 同步 (CLAUDE.md + SKILL.md + matrix doc) | ✅ done | 21b567d |
| R2+3 | TASK-024 | worktree 自动创建 + 子模块独立 checkout | ✅ done | 2bc5712 |
| R2+3 | TASK-025 | worktree 生命周期 (cleanup + 误用保护) | ✅ done | 2bc5712 |
| R4 | TASK-027 | 执行 benchmark + 写 result.json | ✅ done | (Aria 主仓 aria-plugin-benchmarks/) |
| R5 | TASK-028 | dogfood instrumentation + organic-evidence pending report | ✅ done | (Aria 主仓 `.aria/`) |
| R6 | TASK-030 | 版本 bump v1.22.0 + release-ready prep | ✅ implementation done;**merge/archive owner-gated** | 5be61f7 |

**Aria 主仓 feature 分支 HEAD pre-final**: `ce1032a`(post P3 R2+3 pointer bump)

**Cumulative state (P1 + P2 + P3 implementation)**:
- **22 + 8 = 30 atomic tasks shipped**(全 detailed-tasks.yaml 覆盖)
- 108 tests PASS in 1.336s(P1 18 + P2 90)
- full state-scanner suite: 568 tests PASS
- ~3000 lines code + ~2000 lines tests
- 3-way SHA parity verified throughout(Aria 主仓 + aria-plugin + standards × forgejo + github)

---

## Rule #6 Benchmark Result (TASK-027 mechanical run)

`aria-plugin-benchmarks/ab-results/2026-05-20T042320Z-multi-terminal-coordination/benchmark-result.json`

| Metric | Sample | Pass | Rate | Baseline | Δ | Threshold | Passed |
|---|---:|---:|---:|---:|---:|---:|:---:|
| board_correctness | 18 | 18 | 100% | 0% | +100% | ≥95% | ✅ |
| race_reproducibility | 12 | 12 | 100% | 0% | +100% | =100% | ✅ |
| reconcile_determinism | 55 | 55 | 100% | 0% | +100% | =100% | ✅ |
| failure_matrix_coverage | 23 | 23 | 100% | 0% | +100% | ≥90% | ✅ |

**AUTO_GATE**: ✅ true(所有 4 delta > 0 AND 所有 threshold 满足)
**HUMAN_REVIEW**: 🟡 pending(user 后续 `/skill-creator` 或 equivalent 确认)
**verdict**: pending_human_review(等待充分条件)

---

## Dogfood Report (TASK-028 organic + pending)

`.aria/dogfood-reports/multi-terminal-coordination-2026-05-20.md`

**Organic evidence (本 session 真实 race 3 件)**:
1. ⚠️ **wrong-baton**:master 视角 `latest.md` 指 2026-05-16,但 feature 分支 2026-05-17 evening handoff 不可见 → 手动 `git show origin/feature/...` 才找到
2. ⚠️ **push reject non-fast-forward**:首次 master push 被拒,因另一终端 ship Spec Y T2-T8 + closeout × 多 + archive → rebase 解决
3. ⚠️ **submodule detached at stale m4 commit**:`aria-orchestrator` 在 834c313(非 master 也非 spec-y)→ 用 `.git/worktrees/` 隔离

**Counterfactual**: 若 Layer L 已 ship,本 session 会:
1. state-scanner Phase 1 跨分支扫到 spec-y track active → 看板红条提示
2. `resilient_push` 在 non-ff 时自动 fetch-replay-repush(N=3)
3. concurrent_tracks 检测到 ≥2 track → 自动 `create_worktree` 隔离子模块

**Instrumentation lib**: `.aria/scripts/dogfood/measure_multi_terminal.py` (654 lines, stdlib-only) — pending: master merge 后 user 跑收集真实 metric a/b/c 数值

---

## Round 8 / R6 outstanding findings (deferred to P3 cleanup OR known design)

All 15 R8 findings + 3 P1 + 4 P2-design-behavior items dispositioned:

**Closed in P3**:
- Finding #3 P1 (constants duplication) — ✅ closed by TASK-018 lib/constants.py + track_board.py migration
- D-1 P2 (tasks.md checkboxes) — ✅ closed by P2 closeout commit (22 P1+P2 ticked)
- Cleanup follow-up: 部分 trivial 已在 R6 hygiene 应用;余下 follow-up 进 P3 hygiene patch

**Deferred to P3 hygiene (post-merge)**:
- Dead `timedelta` import in reconcile.py
- `lib/__init__.py` docstring stale("后续 P2 task 将加入" — 已 P2 ship)
- `lib/__init__.py` 双上下文 import (try relative + except sys.path) 模板重复 → 提取 helper
- `_TERMINAL_STATUSES` 双定义 cross-ref 注释
- `verdict_reason` 改 typed enum
- `parse_claim`/`serialize_claim` lazy import 可 promote 到模块顶
- `_resolve_ref` cross-module private name access 公共化或文档化
- `normalize_snapshot` flaky 测试 fixture isolation
- STATUS 列对齐(track_board.py)
- f-string F541 风格

**Known design choices (non-bug)**:
- reconcile missing/unparseable `heartbeat_at` → NOT-stale(保守)
- `stale_ttl` + `clock_skew` boundary 严格 `>`(exclusive)
- `yielded` 非 terminal(reconcile 视同 active candidate)
- `abandoned` vs `done` 语义合并 in current impl

**Deferred to TASK-030 owner action (本 spec 范围内余下 2 项)**:
- gc.archive_done_claims `dry_run=False` git write 实际路径(目前 log WARNING)
- heartbeat 周期 push (10min) 调度器(API 已 ship,调用 owner / phase-b-developer 触发)

---

## Release-Ready State

### aria-plugin (`5be61f7`)

```
.claude-plugin/plugin.json     version: "1.22.0"  ✅
.claude-plugin/marketplace.json version: "1.22.0" (top + plugins[]) ✅
VERSION                         header 1.21.4 → 1.22.0  ✅
CHANGELOG.md                    [1.22.0] entry prepended  ✅
README.md                       (无显式 version 行,内部 description 含 v1.22.x 引用)
```

### standards (`03ddfd0`)

```
conventions/session-handoff.md  v1.0.0 → v1.1.0 (additive,§2.3 frontmatter schema)
```

### Aria 主仓 (待 final commit)

```
CLAUDE.md                       Rule #9 Extension 段(引用 v1.22.0 spec)
aria-plugin-benchmarks/         + ab-suite/multi-terminal-coordination/benchmark.yaml
                                + ab-results/2026-05-20T042320Z-multi-terminal-coordination/
.aria/dogfood-reports/          + multi-terminal-coordination-2026-05-20.md
.aria/scripts/dogfood/          + measure_multi_terminal.py
.aria/notes/                    + multi-terminal-coordination-{p1,p2,p3}-closeout.md
openspec/changes/multi-terminal-coordination/  proposal + tasks (22/30 ticked,P3 8/8 待 tick) + detailed-tasks.yaml
aria submodule pointer          → 5be61f7 (待 bump)
```

---

## Owner-Gated Action Sequence(用户后续 ship)

per CLAUDE.md Rule #5 + Rule #8 pre-merge gate + tasks.md Notes §5 merge order:

### Step A — standards repo PR (先 merge)

```bash
cd /home/dev/Aria/.git/worktrees/multi-terminal-coordination/standards
# PR via forgejo CLI
forgejo POST /repos/10CG/aria-standards/pulls -d '{
  "title": "feat(handoff): Rule #9 §2.3 frontmatter schema (v1.1.0 additive)",
  "body": "Per OpenSpec multi-terminal-coordination + DEC-20260519-001. Adds 5-field machine-readable frontmatter to session-handoff.md (track-id / owner-container / phase / status / updated-at). v1.0.0 → v1.1.0 additive bump. See full proposal at https://forgejo.10cg.pub/10CG/Aria/pulls/<TBD>",
  "head": "feature/multi-terminal-coordination",
  "base": "master"
}'
# Rule #8 pre-merge gate (aether ci status if applicable)
# Owner merge via forgejo UI or:
forgejo POST /repos/10CG/aria-standards/pulls/<N>/merge -d '{"Do": "merge"}'
```

### Step B — aria-plugin PR (在 standards 子模块指针更新后)

```bash
cd /home/dev/Aria/.git/worktrees/multi-terminal-coordination/aria
forgejo POST /repos/10CG/aria-plugin/pulls -d '{
  "title": "release(v1.22.0): multi-terminal coordination (Layer H + Layer L + Design A)",
  "body": "Per OpenSpec multi-terminal-coordination + DEC-20260519-001. 13 lib modules + 2 scripts + 108 tests PASS + Rule #6 structural benchmark AUTO_GATE=true. R8 audit: tech-lead READY_TO_MERGE + code-reviewer SHIP_NOW. CHANGELOG.md [1.22.0] entry complete.",
  "head": "feature/multi-terminal-coordination",
  "base": "master"
}'
# Rule #8 pre-merge gate (aether ci status --branch master --in-flight --json)
forgejo POST /repos/10CG/aria-plugin/pulls/<N>/merge -d '{"Do": "merge"}'
```

### Step C — Aria 主仓 PR (子模块指针 bump + dogfood + 主仓 docs)

```bash
cd /home/dev/Aria/.git/worktrees/multi-terminal-coordination
# 确保 standards + aria 子模块指针都指向各自 master post-merge SHA
git -C standards checkout master && git -C standards pull
git -C aria checkout master && git -C aria pull
git add standards aria
git commit -m "chore(submodule): bump standards + aria post-merge for v1.22.0 ship"
git push origin feature/multi-terminal-coordination
git push github feature/multi-terminal-coordination

# Aria 主仓 PR
forgejo POST /repos/10CG/Aria/pulls -d '{
  "title": "feat(multi-terminal): submodule bump + dogfood + CLAUDE.md Rule #9 Extension (v1.22.0)",
  "body": "Per OpenSpec multi-terminal-coordination + DEC-20260519-001. Bumps standards (Rule #9 §2.3) + aria (v1.22.0) submodule pointers. Includes dogfood report + benchmark result + P1/P2/P3 closeout notes.",
  "head": "feature/multi-terminal-coordination",
  "base": "master"
}'
# Rule #8 pre-merge gate
forgejo POST /repos/10CG/Aria/pulls/<N>/merge -d '{"Do": "merge"}'
```

### Step D — Phase D.2 archive (post-3-PR merge)

```bash
# 在 master,各 repo merge 完成后
git checkout master
git pull origin master
# 移 spec 到 archive (Rule #5 项目内变更)
git mv openspec/changes/multi-terminal-coordination openspec/archive/2026-05-20-multi-terminal-coordination
git commit -m "chore(openspec): D.2 archive multi-terminal-coordination"
git push origin master
git push github master
```

### Step E — 多远程推送 verify (per CLAUDE.md v1.15.0+ 自动化)

phase-c-integrator C.2.5 在 C.2 流程中已自动 push;**手动 fallback** 见 CLAUDE.md "灾备" 段。

### Step F — Real dogfood metric collection (post-merge)

```bash
python3 .aria/scripts/dogfood/measure_multi_terminal.py \
  --cycle-id post-v1.22.0-merge-2026-05-XX \
  --output .aria/dogfood-reports/multi-terminal-coordination-post-merge-2026-05-XX.md
```

填入 metric a/b/c 实测数值 → 验证 verdict 由 PENDING → PASS。

---

## Cross-references

- Spec: `openspec/changes/multi-terminal-coordination/{proposal,tasks,detailed-tasks}.{md,yaml}` (22 + 8 = 30/30 atomic, tasks.md 22/27 ticked,P3 8 待 tick in this commit)
- Decision: `docs/decisions/DEC-20260519-001-multi-terminal-coordination.md`
- Closeout: `.aria/notes/multi-terminal-coordination-{p1,p2,p3}-closeout.md`
- Audits: `.aria/audit-reports/post_spec-{R1,R2}-2026-05-19*-summary.md` + Round 6/8 informal (in closeout notes)
- Benchmark: `aria-plugin-benchmarks/ab-suite/multi-terminal-coordination/benchmark.yaml` + `ab-results/2026-05-20T042320Z-multi-terminal-coordination/`
- Dogfood: `.aria/dogfood-reports/multi-terminal-coordination-2026-05-20.md` + `.aria/scripts/dogfood/measure_multi_terminal.py`
- CHANGELOG: `aria/CHANGELOG.md` [1.22.0] entry
- Memory: `feedback_concurrency_advisory_over_hardlock` (local-only, non-git-tracked)
