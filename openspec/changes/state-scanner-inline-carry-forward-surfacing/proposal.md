> **Status**: Draft
> **Level**: 2 (Minimal — proposal.md + tasks.md)
> **Source**: Forgejo Issue [#90](https://forgejo.10cg.pub/10CG/Aria/issues/90) + related [#89](https://forgejo.10cg.pub/10CG/Aria/issues/89)
> **Cycle target**: ~3-4h(collector enhancement + recommendation rule + tests + Rule #6 benchmark + version bump)
> **Created**: 2026-05-20 (post M5 T-deploy Phase B ship,24h Phase C observation 窗口的 fill-in cycle)
> **Owner**: simonfish/dev-claude2

# state-scanner inline carry-forward surfacing

## Why

Multi-session OpenSpec change(尤其 long-running, ≥8 sessions / ≥14 天)在 implementation 期间会累积 inline `[carry-forward: ...]` / `[code-ready: ...]` / `[PASS-with-note: ...]` 注释到 `openspec/changes/<change>/tasks.md`,记录 deferred minor issues / scope hygiene observations / known races。当前 state-scanner Phase 1.6 OpenSpec collector **不识别这些 inline 注释**,导致:

1. **多 session 接手 blind spot**:下次 session(同 AI 实例换 context 或不同 owner 接手)运行 `/state-scanner`,看不到累积的 carry-forward pile;只看到 task count(`30 done / 5 skipped / 22 open`)
2. **session 闭合误判**:active 没问题 = 干净结束 ≠ 真实状态。可能 ship 时才汇总到 `project_v<X>_carry_forward.md`,re-discovery 成本最高
3. **mid-flight invisible**:`project_v<X>_carry_forward.md` memory 文件**仅在 D.2 archive 时**创建,implementation 期间无 consolidated tracker

**Real incident** (#90 cited):TH v0.3.2 chat MVP,8 sessions / 14 天,7 项 inline carry-forward(含 race condition / users_cache bug / channel heuristic / observability gap / dispatch persistence gap / CF tunnel / trailer 缺失)→ 全部内联 `openspec/changes/v0-3-2-chat-mvp/tasks.md`,state-scanner 报告里**完全不可见**。直到用户主动问"是否会被遗忘?"才暴露。

**Why now**: M5 T-deploy Phase B 已 ship,24h Phase C observation 窗口需要 fill-in 工作。Tier 2 state-scanner family 是 handoff §6 Path B 推荐填充,#90 是该 family 最具体可执行 sub-issue(#89 是 superset,本 Spec 自然覆盖 #89 选项 B 的 80% 价值)。

## What Changes

新增 **Phase 1.6.1 sub-section**(append-only 不破 v3.0.0 schema 1.0)到 state-scanner snapshot,具体 5 项变动:

### Change 1 — `openspec.carry_forward_inventory` 新字段(additive)

在 snapshot 顶层 `openspec` object 内增加 `carry_forward_inventory` 子字段(可选,empty 时 `total=0`):

```json
{
  "openspec": {
    "configured": true,
    "active_changes": [...],
    "pending_archive": [...],
    "carry_forward_inventory": {
      "total": 7,
      "by_change": {
        "v0-3-2-chat-mvp": {
          "count": 7,
          "samples": [
            "TASK-027a: write_raw_file race outside git_lock during burst events",
            "TASK-027b: users_cache 400 → alias=feishu:<hash> instead of real name",
            "TASK-027c: capture_trace channel_type heuristic uses chat_id prefix..."
          ]
        }
      }
    }
  }
}
```

### Change 2 — Regex detection

`scripts/collectors/openspec.py` 增加 helper `_extract_carry_forward_annotations(tasks_md_content: str) -> list[str]`:

- **Pattern**: `r'\[(?:carry-forward|TODO|defer(?:red)?|known[ -]gap|PASS-with-note)[^\]]*\]'`(word-boundary,跨多 token 容忍 hyphen/underscore/space variants per `feedback_word_boundary_root_causes_substring_shadows`)
- **Scope**: 仅 `openspec/changes/*/tasks.md`(active changes only — 不扫 archive/)
- **Per-change aggregation**: count + first-3 samples truncated 至 80 chars each
- **Multi-line tolerance**:annotation 跨行(`[carry-forward:\n  long detail]`)按 raw match 抓取,replace `\n` → ` `

### Change 3 — Recommendation rule `carry_forward_pile`

`RECOMMENDATION_RULES.md` 增加新规则:

```yaml
- name: carry_forward_pile
  priority: 50  # advisory, doesn't downgrade primary
  condition: openspec.carry_forward_inventory.total >= 5
  action: advisory_warning
  message: |
    Active OpenSpec changes have {{total}} accumulated inline carry-forward annotations.
    Top: {{by_change | sort_desc | first(3)}}
    Suggest: consolidate to project_v<XX>_carry_forward.md before next major checkpoint,
    or address in current implementation phase.
  block: false
```

Threshold `>=5` 灵感来自 #90 TH v0.3.2 真实案例(7 项 trigger)+ Aria 5/35 Skill 分布"小数效应"经验(5 是有意义的 multi-source 累积下限)。

### Change 4 — Tests

`aria/skills/state-scanner/tests/test_openspec.py` 增加 `TestCarryForwardInventory` 测试类(8+ cases):

1. `test_no_annotations_returns_empty` — `tasks.md` 无 carry-forward → `total=0`
2. `test_single_carry_forward` — 1 annotation → count=1, sample 截断 80 chars
3. `test_mixed_token_types` — 同 file 含 carry-forward + TODO + PASS-with-note → 全 capture
4. `test_hyphen_vs_space_variants` — `[known gap]` vs `[known-gap]` vs `[deferred]` vs `[defer]` 全 match
5. `test_multi_change_aggregation` — 2 active changes 各 3 项 → `total=6`, `by_change` 含 2 keys
6. `test_archive_excluded` — `openspec/archive/<change>/tasks.md` 含 annotation NOT counted
7. `test_multi_line_annotation_normalized` — `[carry-forward:\n  detail]` → single-line sample
8. `test_substring_shadow_guard` — `[other-token-with-carry-forward-in-narrative]` 词边界正确 reject(per word boundary lesson)
9. `test_first_3_samples_truncation` — 5 annotations 中只保留前 3 + 各 truncate 80 chars

### Change 5 — Documentation + 版本

- `aria/skills/state-scanner/SKILL.md` Phase 1.6 表格添加 `carry_forward_inventory` 字段说明,跨链到 §子阶段
- `aria/skills/state-scanner/references/state-snapshot-schema.md` 增加 `openspec.carry_forward_inventory` schema 定义(additive,schema_version 仍 `"1.0"` — 符合 v3.0.0 additive 兼容契约)
- `aria/CHANGELOG.md` + `aria/.claude-plugin/plugin.json` MINOR bump(预计 v1.22.1 → **v1.23.0**)
- `aria/.claude-plugin/marketplace.json` 同步 version
- `aria/VERSION` + `aria/README.md` 同步
- **Rule #6 benchmark**: `/skill-creator` benchmark on state-scanner(structural Skill,**deterministic verification**:fixture tasks.md 含 N 个 inline annotations → assert snapshot 含 `carry_forward_inventory.total == N`;不走 LLM AB)
- 主项目:bump aria gitlink + 写 Phase D handoff

## Non-Goals

明确**不在本 Spec 范围**(future work):

- ❌ Auto-consolidate at D.2 archive(只 surface,不自动改 memory 文件 — owner 决定何时 consolidate)
- ❌ Per-annotation severity classification(carry-forward vs known-gap vs TODO 一视同仁)
- ❌ `_carry_forward.md` running file convention(#89 选项 C 推迟,可由用户自配 `.aria/state-checks.yaml` 实现 → #89 选项 D 价值)
- ❌ archive 历史 carry-forward 历史扫描(#89 implicit 提到,本 Spec 仅 active changes)
- ❌ Forgejo issue cross-link automation(carry-forward 提到的 race condition / bug 不自动开 issue)

## Impact

### Files modified (estimate)

| File | Type | Lines |
|------|------|-------|
| `aria/skills/state-scanner/scripts/collectors/openspec.py` | code | +30/-0 |
| `aria/skills/state-scanner/tests/test_openspec.py` | test | +120/-0 |
| `aria/skills/state-scanner/SKILL.md` | doc | +5/-0 |
| `aria/skills/state-scanner/references/state-snapshot-schema.md` | doc | +25/-0 |
| `aria/skills/state-scanner/RECOMMENDATION_RULES.md` | doc | +15/-0 |
| `aria/CHANGELOG.md` | doc | +10/-0 |
| `aria/.claude-plugin/plugin.json` | config | +1/-1 |
| `aria/.claude-plugin/marketplace.json` | config | +2/-2 |
| `aria/VERSION` | config | +1/-1 |
| `aria/README.md` | doc | +1/-1 |

### Backward compatibility

- ✅ Schema additive(`carry_forward_inventory` 新增字段,空场景 `total=0` 不影响 existing consumers)
- ✅ snapshot_schema_version 仍 `"1.0"`(per v3.0.0 additive-only 演进契约)
- ✅ 旧版 AI / collector 不读 `carry_forward_inventory` 字段不报错(Phase 2 推荐规则 advisory only,不 block primary)
- ✅ 项目无 active OpenSpec change → `carry_forward_inventory.total=0`,无副作用

### Risk

- **Low** — single Skill collector enhancement + recommendation rule;不动 state-scanner 其它 collectors / workflow-runner / phase Skills
- Edge case: `tasks.md` 在 archive 子目录但 path 含 `changes/` substring → glob 必须用 `openspec/changes/*/tasks.md`(active only),NOT `**/tasks.md`(test #6 守 archive 排除)
- Edge case: word-boundary substring shadow(per `feedback_word_boundary_root_causes_substring_shadows`)— test #8 守

## Success Criteria

1. `python3 -m pytest aria/skills/state-scanner/tests/test_openspec.py::TestCarryForwardInventory` 全 PASS(9 cases)
2. 手动 dogfood:在 Aria 主仓 active OpenSpec(本 Spec 自身的 tasks.md)内塞 5 项 `[carry-forward: dogfood-test]` → run `/state-scanner` → snapshot 含 `total=5`,recommendation output 含 advisory warning
3. Rule #6 benchmark: deterministic verification(N annotations in fixture → snapshot count == N)PASS
4. Phase D handoff doc 覆盖 Spec full cycle ship,4-repo 3-way SHA parity post-merge
5. Forgejo #90 closed(reference 本 PR + close);#89 closed-by-reference(addressed via 选项 B variant)

## Cross-references

- Forgejo Issue [#90](https://forgejo.10cg.pub/10CG/Aria/issues/90) — primary trigger
- Forgejo Issue [#89](https://forgejo.10cg.pub/10CG/Aria/issues/89) — superset(本 Spec covers 选项 B variant of #89)
- Related:Issue #54(audit data availability)/ #79(mid-implementation spec-drift trigger)— 同 family "silent gaps in state-scanner" theme
- Predecessor handoff:[`2026-05-20-m5-phase-b-shipped.md`](../../../docs/handoff/2026-05-20-m5-phase-b-shipped.md) — 本 Spec 是 §6 Path B 推荐填充 cycle
- Aria methodology:CLAUDE.md "认知框架 §1 规范先行" + "Rule #5 项目变更必须在项目的 openspec/changes/" + "Rule #6 Skill 基准测试必须使用 /skill-creator"
- Memory entry referenced:[`feedback_word_boundary_root_causes_substring_shadows`](../../../../.claude/projects/-home-dev-Aria/memory/feedback_word_boundary_root_causes_substring_shadows.md)
