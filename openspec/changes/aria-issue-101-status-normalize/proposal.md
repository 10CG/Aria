# Aria Issue #101 — fix `_normalize_status` substring + `Implemented` token gap

> **Level**: 2 (Minimal — 单文件 bug fix + 4 unit test + 1 doc note)
> **Status**: Draft (Phase A.1+A.2)
> **Change ID**: `aria-issue-101-status-normalize`
> **Trigger**: Forgejo Aria [#101](https://forgejo.10cg.pub/10CG/Aria/issues/101) — state-scanner v3.0 `_normalize_status` 子串匹配 "done" → `pending_archive` 假阳性
> **Triage evidence**: [issuecomment-5972](https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-5972) (manual) + [issuecomment-6019](https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-6019) (AI dogfood)
> **Triage verdict**: `partial-repro` (2/4 命中主 bug + 2/4 命中次生 bug)
> **Created**: 2026-05-13

---

## Why

`state-scanner` v3.0 的 `aria/skills/state-scanner/scripts/collectors/_status.py::_normalize_status` 有两个独立但同根的 bug:

### Bug 1 (主因, 2/4 spec 命中): `done` token 优先级太高

```python
# 当前实现 (L52-75 优先级链):
for token in ("done", "complete"):  # ← L58-60
    if token in low:
        return "done"
# ...
if "approved" in low:                # ← L64, 永远到不了
    return "approved"
```

任何 Status 行含子串 `done` 即短路返回 `"done"`,与 raw_status 语义无关。

**真实命中**:
- `"Approved (Rev2 CONVERGED) — Phase A done, ready for Phase B"` → `"done"` ❌ 应是 `"approved"`
- `"⏸ DRAFT pending lawyer review — Phase B PR-A done 2026-05-09"` → `"done"` ❌ 应是 `"pending"`

下游影响: `pending_archive` 包含这些 WIP spec → state-scanner 推荐 `openspec-archive` 工作流 → user 跟推荐执行会**silent 移走活跃 spec**。

### Bug 2 (次生, 2/4 spec 命中): `Implemented` 不在 token 字典

```python
# _normalize_status 字典缺 "implemented" → 返回 "unknown"
```

**真实命中**:
- `"Implemented (Phase B PR-A merged 2026-05-10) — post-deploy 验证后归档"` → `"unknown"` ❌
- `"Implemented (Phase B PR-A merged 2026-05-10) — UAT PASS; post-monitoring 后归档"` → `"unknown"` ❌

下游影响: state-scanner 把这些 spec 标为 unknown 状态,导致依赖 status 的 surfacing 规则(如 mid-implementation carry-forward)漏报。

---

## What

### In scope

1. **修 Bug 1**: 重排 token 优先级 — `archived` / `deprecated` 不动 (terminal states),然后**先**检查显式状态 `draft / pending / approved / reviewed / active / in_progress / implemented`,**最后**才 `done / complete` 兜底
2. **修 Bug 2**: 加 `implemented` token,映射到 `implemented` lifecycle state (新增 state, 介于 `approved` 与 `done` 之间)
3. **加 unit test**: 用 issue #101 列出的 4 个真实 Status 字符串 + 至少 3 个 edge case 作 regression test
4. **state-scanner SKILL.md 加文档**: "Status 行最佳实践" 小节,指导用户用 single-token 或 `<token> — <narrative>` 格式

### Out of scope

- `_normalize_status` 整体 rewrite (优先级 chain 模式保留)
- 改 `openspec.py` 的 `pending_archive` 触发逻辑 (仅 `status == "done"` 触发是正确的;改 token 归一即可)
- 新增 lifecycle states 超出 `implemented` (如 `verifying`, `monitoring` 等推后续 cycle 评估)
- 改 state-scanner snapshot schema (新 state `implemented` 仅出现在 collector 输出, scan-snapshot consumers 兼容)

### Fix sketch

```python
def _normalize_status(raw: str | None) -> str:
    if raw is None:
        return "unknown"
    low = raw.lower()
    # Terminal states first (irreversible)
    if "archived" in low:
        return "archived"
    if "deprecated" in low:
        return "deprecated"
    # Explicit lifecycle states (priority: most specific to least)
    for token in ("draft", "pending", "placeholder"):
        if token in low:
            return "pending"
    for token in ("in progress", "in_progress", "in-progress", "进行中"):
        if token in low:
            return "in_progress"
    if "implemented" in low:           # ← NEW (Bug 2 fix)
        return "implemented"
    if "approved" in low:               # ← moved BEFORE done (Bug 1 fix)
        return "approved"
    if "reviewed" in low:
        return "reviewed"
    if "active" in low:
        return "active"
    if "ready" in low:
        return "ready"
    # Done/complete LAST as fallback (avoids substring shadowing)
    for token in ("done", "complete"):
        if token in low:
            return "done"
    return "unknown"
```

---

## Impact

| Type | Description |
|---|---|
| **Positive** | `pending_archive` 不再 silent 移走 WIP spec; `implemented` spec 正确归类不再标 unknown |
| **Positive** | state-scanner 推荐 `openspec-archive` 工作流时 spec 列表准确,减少误操作 |
| **Risk** | 新 lifecycle state `implemented` 添加到 enum,下游 consumer (state-scanner snapshot consumers) 需识别;缓解: snapshot schema 是 additive (不破坏 backward compat),识别为 unknown 也不影响推荐 |
| **Risk** | token 优先级重排可能影响其他 status 字符串归类;缓解: 4 issue #101 字符串 + 3 edge case unit test + state-scanner 既有 benchmark suite (Rule #6) |

---

## Tasks

详见 [tasks.md](./tasks.md)。简版:

- [ ] T1 — `_status.py` 修复 (Bug 1 + Bug 2)
- [ ] T2 — `tests/test_status.py` (4 #101 字符串 + 3 edge case)
- [ ] T3 — `state-scanner/SKILL.md` "Status 行最佳实践" 段
- [ ] T4 — Rule #6: skill-creator AB benchmark on state-scanner (verify pending_archive 行为改善)
- [ ] T5 — Phase C ship (pre-merge gate Rule #8)
- [ ] T6 — Phase D archive

---

## Success Criteria

- [ ] `_normalize_status` 对 issue #101 列出的 4 个 Status 字符串返回**与人工判断一致**的结果:
  - `"Approved (Rev2 CONVERGED) — Phase A done, ready for Phase B"` → `approved`
  - `"Implemented (...) — post-deploy 验证后归档"` → `implemented`
  - `"Implemented (...) — UAT PASS; post-monitoring 后归档"` → `implemented`
  - `"⏸ DRAFT pending lawyer review — Phase B PR-A done 2026-05-09"` → `pending`
- [ ] 现有 state-scanner 测试 (`aria/skills/state-scanner/tests/`) 全部通过 (无 regression)
- [ ] 新 unit test (T2) 全部通过
- [ ] `pending_archive` snapshot field 在 Aria 自身 4 个 active spec 上返回**空数组** (live 验证)
- [ ] Rule #6 benchmark: with-fix vs without-fix delta > 0 on pending_archive accuracy

---

## References

- Trigger issue: [Forgejo Aria #101](https://forgejo.10cg.pub/10CG/Aria/issues/101)
- Triage: manual [#5972](https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-5972) + AI dogfood [#6019](https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-6019)
- Triage SOP cycle: `openspec/archive/2026-05-13-aria-issue-triage-sop/` (just shipped)
- Related Skill: `aria/skills/state-scanner/` (target of this fix)
- Rule #6 (CLAUDE.md): skill-creator benchmark required for Skill logic modification
- Rule #8 (CLAUDE.md): pre-merge gate required (aether 1.8.5 fallback `skip_with_warning` applies)
