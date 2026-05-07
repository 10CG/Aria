# m3-carryover-result-path-derivation

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-05-07, archived per Level 2 micro-Spec "merge 后立即归档" convention)
> **Created**: 2026-05-07
> **Completed**: 2026-05-07 (aria-orchestrator PR #8 merged at 499d4c4; Aria main PR #81 merged at 6ae57f6; Forgejo Issue #75 close pending owner; 393 tests PASS)
> **Type**: Schema-code drift 收敛 (1 prod 文件 + 6-8 test 文件 + 1 新 drift-guard test)
> **Source**: M3 closeout backlog Forgejo Issue [#75](https://forgejo.10cg.pub/10CG/Aria/issues/75); m3-handoff.yaml §10 t16_backlog_issues #75; T12.1 5-step crash-recovery integration test 触发
> **Owner decision**: **Option B** (drop persistence, do not migrate schema) per session 2026-05-07
> **Related memory**: `feedback_validator_repo_drift_guard_test.md` (drift guard pattern), `feedback_scaffold_helpers_drift_without_callers.md` (helper drift pattern)

---

## Why

**生产症状** (M3 T12.1 集成测试发现):

`_handle_s5_await` (extension.py:1929-1953) 在 `alloc_state == "terminated"` + `exit_code == 0` 路径返回:

```python
return (
    DispatchState.S6_REVIEW.value,
    {"result_path": result_path},   # ← 隐性 schema 写入
)
```

`extra_fields` dict 由 `transition_state` (db.py:476-525) 机械转为 `UPDATE dispatches SET result_path = ? ...`。但 production `schema.sql` (v2.0) **没有 `result_path` 列**:

```sql
-- aria_layer1/schema.sql
CREATE TABLE IF NOT EXISTS dispatches (
  issue_id, dispatch_id, attempt_count, state, ...,
  alloc_id, notification_status, pr_id,
  fail_reason, fail_detail, ..., cycle_*, attempt_history_json
  -- NO result_path COLUMN
);
```

→ SQLite 抛 `OperationalError: no such column: result_path`
→ `extension.py` tick error handler 捕获并将 dispatch 标 `S_FAIL(OTHER)`
→ **production 永不通过 alloc=terminated 路径正常推进到 S6_REVIEW**

**为何 latent 至 M3 T12**:

测试文件 6 处 hand-rolled DDL **都包含** `result_path TEXT,` 列, 让所有 M2 单元测试 PASS。Drift 在 prod ↔ test schema 间, 不在 prod ↔ migration 间 (现有 drift guard `test_drift_guard_committed_schema_matches_migrated_v1` 只守 prod ↔ migration v1, **不**守 prod ↔ test-helper)。

T12.1 集成测试 (`test_t12_reconciler_crash_recovery_integration.py:122-127`) reframe 后用 `alloc state="running"` + heartbeat-advance 信号绕开此 gap, footnote 内显式 record latent bug 等待本 Spec 收敛。

T7 (`test_t7_crash_recovery.py:181-186`) 同样 footnote 标记。

---

## Decision: Option B — Drop Persistence (No Schema Migration)

### 决策事实

`_handle_s6_review` (extension.py:2012-2158) **从未读取 `result_path`**。它只读 `pr_diff` / `commit_message` / `acceptance_criteria` (从 `ctx.dispatch_row` 注入, 非 DB 列), 然后调 `call_review` LLM。

| 状态 | 是否读 result_path |
|------|-------------------|
| S6_REVIEW | ❌ 从未读 (LLM 调用只用 pr_diff/commit_message/acceptance_criteria) |
| S7_HUMAN_GATE | ❌ 从未读 (Feishu webhook + PR detect, 用 issue_id/pr_id) |
| S8_MERGE | ❌ 从未读 (用 pr_id) |
| S9_CLOSE | ❌ 从未读 |
| S_FAIL | ❌ 从未读 |

**结论**: `result_path` 是 **dead persistence** — 写入路径(S5_AWAIT terminated branch)与读取路径(无)断链。Option B 直接 drop, 不改 schema, 不引入 derivation。

### 替代方案 (rejected)

| Option | 描述 | 弃因 |
|--------|------|------|
| A: Additive migration v3.0 (`ALTER TABLE ... ADD result_path TEXT`) | 加列 + 写 + 后续状态如需可读 | 列写无人读 → dead column; schema bump 维护成本; drift guard 复杂度增加 |
| C: 计算式 derivation 入 S6_REVIEW (Issue 原推荐) | drop 写, S6 入口按 alloc_id 重算 (`f"/data/aria-layer1/results/{alloc_id}/result.json"`) | S6 不需此值, 重算函数无 caller, 触犯 `feedback_scaffold_helpers_drift_without_callers` |
| **B: Drop persistence, no derivation** | drop `{"result_path": ...}` extra_fields; 不引入新代码 | **选** — 符合 YAGNI, 消除 schema↔code drift 根因 |

### 反向兼容性 (forward planning)

**M5 LLM observer 假设需 result_path**: 届时可重新 additive migration (Option A 路径), 旧 row backfill = NULL (无历史)。本 Spec 不挡未来路径。

**KI-12 fix (test_29 / test_29b 来源) obsolete**: KI-12 假设 NomadClient 在 alloc status dict 中 populate `result_path` 字段, _handle_s5_await 读出并 persist。Option B 下 NomadClient 即使返回 `result_path` 也忽略。alloc_status_provider 接口契约不变 (允许 dict 含 `result_path`, 消费者选择忽略)。

---

## What

### 1. Source code 改动 (`aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/extension.py`)

**File**: `extension.py:1804-1953` (`_handle_s5_await`)

**Diff (terminated + exit_code==0 path)**:

```diff
         elif alloc_state == "terminated":
             if exit_code == 0:
                 # Successful completion → advance to S6_REVIEW.
-                # KI-12 fix: result_path is read from NomadClient alloc response
-                # when available. The alloc status dict may include a "result_path"
-                # key populated by the production NomadClient from the alloc's
-                # bind-mount output directory.
-                # Stub convention (when NomadClient does not provide result_path):
-                #   /data/aria-layer1/results/{alloc_id}/result.json
-                # T7 KI-12 fix: true path provided by NomadClient response, stub
-                # falls back to convention path. Code comment is the audit trail.
-                result_path = status.get(
-                    "result_path",
-                    f"/data/aria-layer1/results/{alloc_id}/result.json",
-                )
                 logger.info(
-                    "_handle_s5_await: alloc terminated exit_code=0 "
-                    "alloc_id=%s issue_id=%s → S6_REVIEW result_path=%s",
+                    "_handle_s5_await: alloc terminated exit_code=0 "
+                    "alloc_id=%s issue_id=%s → S6_REVIEW",
                     alloc_id,
                     issue_id,
-                    result_path,
                 )
                 return (
                     DispatchState.S6_REVIEW.value,
-                    {"result_path": result_path},
+                    {},  # result_path not persisted (no consumer; AD §M3-carryover-result-path)
                 )
```

**Docstring update (line 1815-1817)**:

```diff
              - "running"  → update heartbeat, stay in S5_AWAIT (return None).
              - "terminated" + exit_code==0 → transition to S6_REVIEW.
-               result_path is set to a deterministic path based on alloc_id.
+               (result_path is NOT persisted — no downstream consumer;
+                see openspec/archive/<date>-m3-carryover-result-path-derivation)
              - "terminated" + exit_code!=0 → S_FAIL(CONTAINER_CRASH).
```

**Doc-only touch (`alloc_status_provider.py:19`)**:

```diff
-    Production extends the dict additively (e.g. result_path), per AD-M2-9
+    Production may extend the dict additively (consumers may ignore unknown
+    keys; e.g. legacy `result_path` no longer persisted, see m3-carryover-result-path-derivation)
```

### 2. Test schema 对齐 (6 文件: drop `result_path TEXT,`)

| 文件 | 行 | 改动 |
|------|----|------|
| `tests/test_state_machine_skeleton.py` | 844 (`_setup_full_schema`) | drop `result_path TEXT,` |
| `tests/test_t1_extension_integration.py` | 58 | drop `result_path TEXT,` |
| `tests/test_t7_http_dispatch.py` | 69 | drop `result_path TEXT,` |
| `tests/test_t12_s7_webhook.py` | 70 | drop `result_path TEXT,` |
| `tests/test_t7_prompt_nomad.py` | 77 | drop `result_path TEXT,` |
| `tests/test_t13_s8_merge.py` | 63 | drop `result_path TEXT,` |

> **注**: 6 处 hand-rolled DDL 各自维护; 本 Spec 不引入 schema 共享 helper (out of scope)。

### 3. Test assertion 更新 (3 文件)

**`tests/test_state_machine_skeleton.py` T6.2 test (line ~1730-1754)**:

```diff
     """T6.2: alloc terminated exit_code=0 → S6_REVIEW + result_path set."""
-    result_path = extra_fields.get("result_path", "")
-    self.assertIn(
-        alloc_id,
-        result_path,
-        "result_path must include the alloc_id for traceability",
-    )
-    self.assertTrue(result_path, "result_path must be non-empty")
+    self.assertEqual(
+        extra_fields, {},
+        "M3 carryover #75: result_path no longer persisted (no consumer; "
+        "schema lacks column; transition_state would raise OperationalError)",
+    )
```

(Test 名 + docstring 同步更新为 "T6.2 v2: alloc terminated exit_code=0 → S6_REVIEW (no result_path persistence)")

**`tests/test_t7_crash_recovery.py:181-215` 同 pattern**:

```diff
-    self.assertTrue(extras.get("result_path"),
-                    "result_path must be non-empty for downstream S6_REVIEW")
-    self.assertIn("alloc-resume-1", extras["result_path"],
-                  "result_path should contain alloc_id for forensic traceability")
+    self.assertEqual(extras, {},
+                     "M3 carryover #75: result_path no longer persisted")
```

(test docstring 同步去掉 "this path persists `result_path`" footnote, 反向 expect 空 extras)

**`tests/test_t7_prompt_nomad.py` test_29 + test_29b (KI-12 fixture obsolete)**:

```diff
-def test_29_ki12_result_path_from_nomad_response(self) -> None:
-    """_handle_s5_await must read result_path from alloc status dict when present.
-    ...
-    """
-    real_result_path = "/nomad/alloc/.../local/result.json"
-    ...
-    self.assertEqual(extra_fields.get("result_path"), real_result_path, ...)
-
-def test_29b_ki12_convention_path_fallback_when_no_result_path(self) -> None:
-    ...

+# KI-12 (test_29 / test_29b) obsoleted by m3-carryover-result-path-derivation
+# (Forgejo #75): _handle_s5_await no longer reads or persists result_path;
+# alloc status dict may still include the field but consumer ignores it.
+# Tests deleted (Option B = drop persistence; no fixture to assert against).
```

### 4. New drift-guard test (extend `tests/test_t3_schema_migration.py`)

```python
def test_drift_guard_test_helper_matches_committed_schema(self) -> None:
    """Per feedback_validator_repo_drift_guard_test (extended for test-helper).

    Compare prod schema.sql columns vs test-helper _setup_full_schema columns.
    The 6 hand-rolled DDLs in tests/ must not declare any column absent from
    schema.sql (which would mask drift bugs like Forgejo #75 result_path).

    On future schema additive change: prod adds first, helpers follow.
    """
    # Read prod committed schema columns
    conn_prod = sqlite3.connect(":memory:")
    schema_sql = (Path(__file__).parent.parent / "aria_layer1" / "schema.sql").read_text()
    conn_prod.executescript(schema_sql)
    cols_prod = _read_columns(conn_prod, "dispatches")

    # Run test-helper _setup_full_schema (the canonical DDL form among 6 hand-rolls)
    from tests.test_state_machine_skeleton import _setup_full_schema
    conn_helper = sqlite3.connect(":memory:")
    _setup_full_schema(conn_helper)
    cols_helper = _read_columns(conn_helper, "dispatches")

    extra_in_helper = cols_helper - cols_prod
    self.assertEqual(
        set(), extra_in_helper,
        f"test-helper has columns absent from prod schema.sql: {extra_in_helper}\n"
        f"This masks the production schema-write OperationalError (Forgejo #75 pattern).\n"
        f"Either add to schema.sql (additive migration) or drop from helper."
    )
```

### 5. Doc updates

- `aria-orchestrator/docs/m3-handoff.yaml` §10 #75 entry: `triage_t16` → `fix-now: closed 2026-05-07 by m3-carryover-result-path-derivation Spec ...`
- `aria-orchestrator/docs/architecture-decisions.md` §AD-M3-6 §风险 (crash recovery) — append note: latent S5_AWAIT terminated bug closed by separate Spec (cross-ref)
- 主 Aria repo `openspec/changes/m3-carryover-result-path-derivation/proposal.md` (this file)

---

## 非目标

- **不引入 schema migration** (Option A 弃)
- **不实现 result_path on-demand derivation 函数** (Option C 弃 — 无 caller, 触犯 `feedback_scaffold_helpers_drift_without_callers`)
- **不重构 6 处 hand-rolled DDL 共享 helper** (out of scope; drift guard 守残)
- **不改 alloc_status_provider Protocol** (接口允许 dict 含 result_path, 消费者忽略, 向后兼容)
- **不改 NomadClient 真实路径计算逻辑** (production NomadClient 仍可在 status dict 内 set result_path, 仅 _handle_s5_await 不再消费)
- **不改 KI-12 与无关的其他 NomadAllocHTTPProvider 行为** (test_29* 仅测 result_path 来源, 与 alloc state routing 无关)

---

## 验收

- [ ] `extension.py:_handle_s5_await` terminated+exit_code==0 路径: 不再 set `result_path`, 返回 `(S6_REVIEW.value, {})`
- [ ] `extension.py:1816` docstring 与 `alloc_status_provider.py:19` 注释更新, 指向本 Spec archive
- [ ] 6 个 test 文件 schema DDL 删除 `result_path TEXT,`
- [ ] 3 个 test assertion 更新 (test_state_machine_skeleton T6.2 / test_t7_crash_recovery / test_t7_prompt_nomad test_29 + test_29b)
- [ ] 新增 `test_drift_guard_test_helper_matches_committed_schema` in `test_t3_schema_migration.py`, 通过 prod schema ↔ helper schema 列集对比
- [ ] 整包 `python -m unittest discover -s tests` 全 PASS, 0 regression on baseline (M3 close 时 394 tests PASS)
- [ ] 新 drift guard 测试运行: PASS (helper 与 prod 已对齐)
- [ ] 反向验证: 临时 `_setup_full_schema` 加回 `result_path TEXT,` → drift guard FAIL with informative msg
- [ ] `m3-handoff.yaml` §10 #75 `triage_t16` 字段从 `<pending>` 改为 `fix-now: ...` cross-ref
- [ ] AD-M3-6 §风险 append latent bug closure note
- [ ] PR + 多远程 push (origin + github × 2 repos), Forgejo Issue #75 close + comment ref archive

---

## 价值

- **Schema↔code drift 根因消除**: dead persistence 删除, 不留 `result_path` 列 schema 债务 (vs Option A 加无人读列)
- **新 drift guard 守未来**: prod ↔ test-helper 列集分歧机械检测, 防"6 处 hand-rolled DDL 偷加列"再发生 (Forgejo #75 pattern 守残)
- **KI-12 obsolete 显式归零**: test_29* 删除而非保留 confusing fixture, 与 `feedback_scaffold_helpers_drift_without_callers` 一致 (无 caller 即砍)
- **YAGNI 兑现**: 6 行净删 + 1 测试新增 vs Option A 的 `ALTER TABLE` + migration + backfill rule + 新 schema_meta version bump (~80 行)
- **M5 路径不挡**: 未来 LLM observer 真需 result_path 时可走 Option A additive migration, 本 Spec 不引入路径互斥
- **样本积累**: M3 carryover 三连 2/3, 与 #76 hygiene + #77 validator 并列形成"micro-Spec PR 流水线"模板

---

## 风险与回滚

| # | 风险 | 影响 | 缓解 |
|---|------|------|------|
| 1 | 6 处 hand-rolled DDL 删除一致性失误 → 某 test 文件残留 result_path 列 → drift guard FAIL | 低 | drift guard 是本 Spec 强制项, fail 时 stack trace 直指残留文件; CI 红才能 merge |
| 2 | `_handle_s6_review` 隐性依赖 result_path (我未发现的间接读) | 低 | grep -rn 全 prod 代码已确认仅 _handle_s5_await write site + alloc_status_provider 注释; 394 tests baseline 全 PASS = behavioral 验证 |
| 3 | 未来 M5 LLM observer 需 result_path → 重新 additive migration 成本 | 低 | 届时走 Option A; 本 Spec 不破坏路径; backfill rule 时机自然 (M5 launch) |
| 4 | KI-12 历史价值 (test_29/29b 删除 = 失去测试覆盖) | 低 | KI-12 fix 本就 dead path (S6 不读), 删除测试就是删除"测试不存在的 contract"; 历史 audit trail 在 git blame 与本 Spec |
| 5 | drift guard 误报 (helper 合理多列 / 少列) | 低 | drift guard 仅检 `extra_in_helper` (helper 多, prod 少) 单方向; helper 少于 prod 是合理 (test 不需用全部列) |

**回滚路径**:

- **Level 1 (revert this Spec)**: 反向 git revert, 6 测试文件加回 `result_path TEXT,` + 代码加回 `{"result_path": ...}` + 删除新 drift guard test。Issue #75 重新 reopen。
- **Level 2 (Option A pivot)**: 不 revert 本 Spec, 立另一 Spec `add-result-path-column` 走 additive migration (附加, 非互斥)
- **Level 3 (no-op)**: 本 Spec 不可回滚到"现状" — 现状是 latent bug, Spec 实施后 latent 显形 = drift guard 启用; "回滚" 等价于 "反向 revert + 故意保留 latent bug" 不合理

> **决策**: Level 1 是干净 revert; Level 2 是路径 pivot; Level 3 不存在。
