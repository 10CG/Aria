# m3-handoff-validator-spillover

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Draft
> **Created**: 2026-05-07
> **Type**: New tool (validate-m3-handoff.py + tests) + sentinel logic for AD slot fail-fast guard
> **Source**: M3 closeout backlog Forgejo Issue [#77](https://forgejo.10cg.pub/10CG/Aria/issues/77); m3-handoff.yaml §10 t16_backlog_issues #77 (`<required for T16.2 implementation; not optional>`); AD-M3-* §治理影响 fail-fast 守卫 line (architecture-decisions.md:2357)
> **Owner decision**: 一并实施 T16.2 validator 主体 (per session 2026-05-07: "A, B, 一并做"; not just sentinel logic)
> **Related memory**: `feedback_ad_slot_backfill_checkpoint.md` (AD slot fail-fast pattern), `feedback_validator_repo_drift_guard_test.md` (validator pattern)

---

## Why

**Two coupled gaps**:

### Gap 1 — T16.2 validator does not exist

m3-handoff.yaml is the M3 closeout 机读移交 artifact (sister to m1-handoff.yaml + m2-handoff.yaml, both of which have validators). When T16.4 owner closeout signs off, the handoff yaml must pass mechanical validation per AD-M1-7 additive-only governance + 多 schema field constraints.

m1 + m2 已有 validators (`docs/validate-m1-handoff.py` + `docs/validate-m2-handoff.py`) — m3 缺 validator 是 T16 hard blocker。

### Gap 2 — AD slot fail-fast 守卫 sentinel exception not implemented

`architecture-decisions.md:2357` 显式 fail-fast 守卫规则:

> T16 closeout 必须 verify AD-M3-1..7 status 全部 Decided; AD-M3-8/9/10 `_spillover_` 字面值是预期占位; 实际未用归档时清空 status 改 `_unused_`

Three sentinel patterns:
| Pattern | 含义 | Validator action |
|---------|------|------------------|
| `_待回填_` | Decision pending, NOT decided | **fail** (T16 closeout 阻断) |
| `_spillover_` | 前向预留 slot, 永不期望填写 (per AD-M3-1 §治理影响) | **skip + log info** |
| `_unused_` | 归档时确认未用, 主动清空 | **skip + log info** |
| 其它 (Decided 等) | Decision recorded | **pass** |

**Risk if not implemented**: T16.4 owner runs validator → AD-M3-8/9/10 `_spillover_` 被误判为 `_待回填_` 变体 → fail → 阻塞 closeout → owner 必须手工 grep 排除。`feedback_ad_slot_backfill_checkpoint` 教训直接来源此 pattern。

**Per Issue #77 acceptance**: validator 必须显式区分 `_待回填_` (error) vs `_spillover_` (info) for ops clarity.

---

## What

### 1. New file: `aria-orchestrator/docs/validate-m3-handoff.py` (~400 行)

镜像 `validate-m2-handoff.py` 结构, 适配 m3-handoff.yaml schema:

**架构 (复用 m2 模式)**:
- stdlib only (no external deps); Python 3.8+
- Reuse `parse_yaml_subset()` line-regex parser from m2 validator (same indentation conventions)
- Same `is_pending()` / `unquote()` / `coerce_scalar()` helpers
- Same exit code contract: 0 / 1 / 2

**M3-specific check functions**:

```python
def check_required_fields(data, errors): ...
  # Required top-level: schema_version, go_decision, rationale, acceptance,
  # cost_attribution, multi_model_routing_benchmark, performance_vs_m1,
  # secret_rotation, effort, owner_signoff, tech_lead_cosign,
  # carryover_to_m4, t16_backlog_issues

def check_schema_version(data, errors): ...  # "1.0" lock

def check_go_decision(data, errors): ...
  # enum: Go | Go-with-revision | No-Go | No-Go-with-revision (or pending)

def check_acceptance_when_final(data, errors): ...
  # When go_decision is final: a/b/c/d/e all required + types

def check_cost_attribution(data, errors): ...
  # zhipu_pricing_review_due must be YYYY-MM-DD format
  # zhipu_pricing_owner_verified must be bool
  # luxeno_subscription_baseline_usd_monthly + zhipu_metered_usd_total
  #   must be set (not pending) when go_decision is final

def check_performance_vs_m1(data, errors): ...
  # m1_baseline_p50_seconds == 31.5 (M1 carry-forward lock)
  # threshold_seconds == 47.25 (1.5× baseline)

def check_secret_rotation(data, errors): ...
  # When go_decision is final: completed=true required;
  # date YYYY-MM-DD; rotated_keys must be non-empty list

def check_signoffs_when_final(data, errors): ...
  # owner_signoff + tech_lead_cosign signed_by + date
  # (mirrors m2 pattern)

def check_multi_model_benchmark(data, errors): ...
  # multi_model_benchmark_gate must be bool
  # benchmark_actual_cost_usd ≤ 5 hard ceiling per R1-I9
  # benchmark_run=true requires non-null s2/s3/s6 accuracy

def check_t16_backlog_issues(data, errors): ...
  # All issues must have triage_t16 != "<pending ...>" when go_decision is final

# ────────────────────────────────────────────────────────────
# NEW: AD-M3 slot fail-fast guard (Issue #77 sentinel logic)
# ────────────────────────────────────────────────────────────

PLACEHOLDER_SENTINEL = "_待回填_"
SPILLOVER_SENTINEL = "_spillover_"
UNUSED_SENTINEL = "_unused_"

def check_ad_m3_slots(data, errors, info_lines): ...
  # Read aria-orchestrator/docs/architecture-decisions.md (sister file)
  # Scan ### AD-M3-N — ... headers + their > **状态**: ... lines
  # For each AD-M3-N (N=1..10):
  #   if status contains PLACEHOLDER_SENTINEL → errors.append("AD-M3-N still placeholder")
  #   elif status starts with SPILLOVER_SENTINEL → info_lines.append("AD-M3-N: spillover reserved (skip)")
  #   elif status starts with UNUSED_SENTINEL → info_lines.append("AD-M3-N: unused, archived (skip)")
  #   else → pass
```

### 2. New file: `aria-orchestrator/docs/test_validate_m3_handoff.py` (~300 行)

镜像 m2 test pattern + 新增 sentinel-specific 测试:

```python
class TestSentinelExceptionLogic(unittest.TestCase):
    """Issue #77 acceptance: validator must distinguish:
       _待回填_ → error / _spillover_ → info / _unused_ → info / Decided → pass"""

    def test_spillover_slot_skipped_with_info(self): ...
        # AD-M3-8 marked _spillover_ → info log, no error

    def test_placeholder_slot_fails_fast(self): ...
        # Hypothetical AD-M3-X marked _待回填_ → error

    def test_unused_slot_skipped_with_info(self): ...
        # AD-M3-Y marked _unused_ → info log, no error

    def test_decided_slot_passes_silently(self): ...
        # AD-M3-1 (Decided 2026-05-05) → no info, no error

    def test_actual_ad_doc_today_passes(self): ...
        # Real architecture-decisions.md state today: AD-M3-1..7 Decided,
        # AD-M3-8/9/10 _spillover_ → 0 errors, 3 info lines

# Plus standard checks mirrored from m2:
class TestDraftPassesValidation(unittest.TestCase): ...
class TestSchemaVersionEnforcement(unittest.TestCase): ...
class TestGoDecisionEnum(unittest.TestCase): ...
class TestAcceptanceWhenFinal(unittest.TestCase): ...
class TestCostAttribution(unittest.TestCase): ...
class TestPerformanceVsM1(unittest.TestCase): ...
class TestSecretRotation(unittest.TestCase): ...
class TestMultiModelBenchmark(unittest.TestCase): ...
class TestSignoffsWhenFinal(unittest.TestCase): ...
class TestT16BacklogIssues(unittest.TestCase): ...
class TestActualHandoffPasses(unittest.TestCase): ...
    # Repo m3-handoff.yaml current state should pass all checks that
    # don't require final go_decision (draft mode tolerated)
```

### 3. Doc updates

**`aria-orchestrator/docs/m3-handoff.yaml` §10 #77** entry:

```diff
   - number: 77
     title: "[T16-backlog] T16.2 validator must recognize _spillover_ sentinel for AD-M3-8/9/10"
     ...
-    triage_t16: "<required for T16.2 implementation; not optional>"
+    triage_t16: "fix-now: closed 2026-05-07 by m3-handoff-validator-spillover Spec; validate-m3-handoff.py + tests live; sentinel logic distinguishes _待回填_ (error) vs _spillover_/_unused_ (info+skip); actual AD doc today (AD-M3-1..7 Decided + AD-M3-8/9/10 _spillover_) PASSes 0 errors + 3 info lines"
```

**Optional: `architecture-decisions.md:2357` fail-fast 守卫 line** add validator path reference:

```diff
-> **fail-fast 守卫** (per `feedback_ad_slot_backfill_checkpoint`): T16 closeout 必须 verify AD-M3-1..7 status 全部 Decided; AD-M3-8/9/10 `_spillover_` 字面值是预期占位; 实际未用归档时清空 status 改 `_unused_`
+> **fail-fast 守卫** (per `feedback_ad_slot_backfill_checkpoint`): T16 closeout 必须 verify AD-M3-1..7 status 全部 Decided; AD-M3-8/9/10 `_spillover_` 字面值是预期占位; 实际未用归档时清空 status 改 `_unused_`. 机械实施: `aria-orchestrator/docs/validate-m3-handoff.py::check_ad_m3_slots` (Issue #77 closed by `m3-handoff-validator-spillover` Spec 2026-05-07).
```

---

## 非目标

- **不实现 T16.2 之外的 T16.x tasks** (T16.1 expand schema / T16.3 effort accounting / T16.4 owner closeout 是独立 owner-driven tasks; 本 Spec 仅 T16.2 validator + sentinel)
- **不改 m1/m2 validator** (only m3, additive)
- **不引入 PyYAML 依赖** (复用 m2 stdlib YAML subset parser, 与 m1/m2 一致)
- **不做 m3-handoff.yaml schema expansion** (T16.1 owner task; 本 Spec 仅 validate 当前 schema 形态)
- **不做 AD-M3-* 内容修改** (sentinel pattern 已在文档中, 仅 validator 识别)
- **不集成入 CI** (本地运行即可; CI 集成是后续可选 task, 见 m1/m2 同样路径)

---

## 验收

- [ ] `aria-orchestrator/docs/validate-m3-handoff.py` 创建, 镜像 m2 validator 结构 (~400 行)
- [ ] `aria-orchestrator/docs/test_validate_m3_handoff.py` 创建, 含 sentinel-specific 测试类 + 标准 check 测试 (~300 行)
- [ ] `python3 docs/test_validate_m3_handoff.py` 全 PASS
- [ ] `python3 docs/validate-m3-handoff.py docs/m3-handoff.yaml -v` 当前 (draft go_decision) 状态 → exit 0, 3 info lines (AD-M3-8/9/10)
- [ ] sentinel logic 4 case 测试覆盖: spillover 跳过 / placeholder 失败 / unused 跳过 / Decided 通过
- [ ] `m3-handoff.yaml` §10 #77 `triage_t16` 字段从 `<required ...>` 改为 `fix-now: ...` cross-ref
- [ ] (optional) `architecture-decisions.md:2357` fail-fast 守卫 line append validator 路径引用
- [ ] PR + 多远程推送 (origin + github × 2 repos), Forgejo Issue #77 close + comment ref archive

---

## 价值

- **T16.2 解锁**: m3-handoff.yaml 机读 validation 落地, T16 closeout 不再 hard-blocked on validator 缺失
- **AD slot 三态语义化**: `_待回填_` / `_spillover_` / `_unused_` 区别有机械保证, 不依赖 owner 手工 grep
- **owner 体验**: 跑一行 `python3 validate-m3-handoff.py` 拿明确 verdict + info trail; 与 m1/m2 体验一致
- **`feedback_ad_slot_backfill_checkpoint` 闭环**: pattern 不再只是 doc note, 有可执行验证器
- **样本积累**: M3 carryover 三连 3/3 完成, 三连完整 archive 后 m3-handoff §10 全 fix-now
- **m4 forward**: validator pattern 已机械化, m4-handoff 时只需复制改字段即可 (m1→m2→m3 系列三代验证器累积成熟)

---

## 风险与回滚

| # | 风险 | 影响 | 缓解 |
|---|------|------|------|
| 1 | YAML subset parser 不识别 m3 特定语法 (如 §11/§12 audit_trail 嵌套深度) | 中 | 借鉴 m2 parser 已经在 m2-handoff.yaml 通过; m3-handoff.yaml 当前结构 ≤ 3 层嵌套, 不超 m2 复杂度上限; 测试 `test_actual_ad_doc_today_passes` 兜底 |
| 2 | architecture-decisions.md 解析 (regex `### AD-M3-N` + `状态: ...`) 误识别 | 中 | 测试覆盖现实 AD doc 今日状态 (10 slots, 7 Decided, 3 spillover) → 必须 0 errors + 3 info lines; markdown 结构稳定 |
| 3 | AD-M3-* 未来加 N=11 spillover slot 时 validator 是否兼容 | 低 | check_ad_m3_slots 实施按 regex `### AD-M3-(\d+)` 动态扫描, 不 hardcode N; 任意 N 自动支持 |
| 4 | sentinel 字面值未来变化 (`_待回填_` 改字符) | 低 | 集中在 PLACEHOLDER_SENTINEL/SPILLOVER_SENTINEL/UNUSED_SENTINEL 三个常量; 改 1 处即可 |
| 5 | m3-handoff.yaml 字段顺序变化致 parse 失败 | 低 | parse_yaml_subset 是基于 indent + key 的 map, 不依赖字段顺序 |
| 6 | T16.1 future schema expansion 致 required_fields list 不全 | 低 | 本 Spec 仅 lock 当前字段 set; T16.1 后另起 minor patch 扩 required_fields |

**回滚路径**:

- **Level 1 (revert this Spec)**: 反向 git revert, 删 validate-m3-handoff.py + test_validate_m3_handoff.py + 反向 m3-handoff.yaml §10 #77 triage 编辑。Issue #77 重 reopen。
- **Level 2 (validator 错误致 owner T16 closeout 阻塞)**: validator 内部 bug → owner 临时跳过 (不跑 validator), 手工 closeout; 同时立 patch Spec 修 validator
- **Level 3 (no-op)**: 不存在 — 本 Spec 不修改既有行为, 全部新增

---

## 实施顺序 (Phase B 内部)

1. **B.2.1** Read m2 validator 全文 + parser → copy 框架 to validate-m3-handoff.py
2. **B.2.2** 改写 check_* 函数, 适配 m3-handoff.yaml schema (cost_attribution / performance_vs_m1 / secret_rotation 等)
3. **B.2.3** **新增** check_ad_m3_slots (PLACEHOLDER/SPILLOVER/UNUSED 三态识别) — 这是 Spec 核心交付物
4. **B.2.4** 写 test_validate_m3_handoff.py (镜像 m2 测试 + 新增 TestSentinelExceptionLogic 类)
5. **B.2.5** Run tests → confirm PASS
6. **B.2.6** Run validator on actual m3-handoff.yaml 当前 → confirm exit 0 + 3 info lines
7. **B.2.7** 更新 m3-handoff.yaml §10 #77 + (optional) AD-M3 §2357 references
8. **B.2.8** Self-review (per Level 2 proportionality, 无 multi-agent audit)

预估总: ~5-6h (validator 主体 ~3h + tests ~2h + doc 0.5h + self-review 0.5h)。
