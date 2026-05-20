> **Status**: **Approved (R2 CONVERGED at PASS_WITH_WARNINGS — 3 agents unanimous)** — Rev1.1 (R1 + R2 audit revisions applied)
> **Level**: 2 (Minimal — proposal.md + tasks.md)
> **Source**: Forgejo Issue [#90](https://forgejo.10cg.pub/10CG/Aria/issues/90) + related [#89](https://forgejo.10cg.pub/10CG/Aria/issues/89)
> **Cycle target**: ~3-4h(collector enhancement + recommendation rule + tests + Rule #6 benchmark + version bump)
> **Created**: 2026-05-20 (post M5 T-deploy Phase B ship,24h Phase C observation 窗口的 fill-in cycle)
> **Owner**: simonfish/dev-claude2
> **Audit history**:
> - **R1** (2026-05-20) — 3 agents (tech-lead / backend-architect / qa-engineer) all REVISE, 0 critical / ~5 majors / ~12 minors → Rev1 addresses
> - **R2** (2026-05-20) — 3 agents all PASS_WITH_WARNINGS, **all R1 majors ADDRESSED** + 0 new critical/major + ~6 new minors (含 1 cross-agent converged: tasks.md/proposal.md regex string drift,已 sync) → Rev1.1 + Approved
> - Convergence: unanimous PASS-tier + verdict improved (REVISE→PASS_WITH_WARNINGS) + 无振荡 per [`feedback_post_spec_audit_pragmatic_convergence`](../../../../.claude/projects/-home-dev-Aria/memory/feedback_post_spec_audit_pragmatic_convergence.md)
> **M5 attention split hedge**: 本 Spec C.2 merge gated on M5 Phase C 完成 OR M5 24h 观察期 0 P0 issue。若 M5 Phase C 暴露 P0 必须立即 halt 本 Spec implementation(B.* halt-safe,Spec 无 irreversible state)直到 M5 收口

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

在 snapshot 顶层 `openspec` object 内增加 `carry_forward_inventory` 子字段。**字段总是 present**(消除 "no field" vs "field=empty" 歧义),`total=0` 表示 0 annotations 或 0 active changes 任一情况:

```json
{
  "openspec": {
    "configured": true,
    "active_changes": [...],
    "pending_archive": [...],
    "carry_forward_inventory": {
      "total": 7,
      "active_change_count": 2,      // 区分 "0 active changes" vs "active 但无 annotations"
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

**Empty-state semantics**:
- 0 active changes → `{total:0, active_change_count:0, by_change:{}}`
- N active changes 但都 0 annotations → `{total:0, active_change_count:N, by_change:{}}`(consumers 可区分两种 zero)
- 部分 active changes 有 annotations → only those changes 出现在 `by_change` map(无 annotations 的 active change 不占 key,降 noise)

**Helper signature 决定**:本 Spec 实施时 helper 返回 `list[str]` raw matches。**故意不**返回 `list[tuple[int, str]]`(line number)— line number 增加 collector 复杂度但当前 advisory 输出无需。如 future Spec 需 link 到 specific task line,可 minor bump signature(向后兼容 wrapper 函数)。

### Change 2 — Regex detection

`scripts/collectors/openspec.py` 增加 helper `_extract_carry_forward_annotations(tasks_md_content: str) -> list[str]`:

- **Pattern**: `r'\[(?:carry-forward|TODO|defer(?:red)?|known[ -]gap|PASS-with-note)\b[\s\S]*?\]'`
  - **Positional anchoring**: `\[` literal 起始 + token group **紧贴** opening `[` — `[my-carry-forward-note]` 不匹配(token group 必须紧贴 `[`,非 token alt 前缀失效)
  - **Token-end `\b`**: `carry-forward\b` 保证不被 `carry-forwarded` / `carry-forward-extended` 等 substring 误命中(per `feedback_word_boundary_root_causes_substring_shadows` Issue #101 lesson)
  - **Multi-line capture**: `[\s\S]*?` 非贪婪跨行(Python `re` 默认 `.` 不含 `\n`,这里用 `[\s\S]` 显式跨行;非贪婪 `*?` 防 `]` 跨多 annotation 误粘连)
  - **Token alternatives**: `carry-forward` / `TODO` / `defer` / `deferred` / `known gap` / `known-gap` / `PASS-with-note`(hyphen/space variants per #101 lesson — `[ -]` 允许 hyphen 或 space)
  - **Word-boundary 说明**: `\b` 仅加在 token group **末尾**(`[` 是 non-word char,起始位置 `\b` implicit;`\b` 加在 token 后保 token 完整匹配)
- **Scope**: 仅 `openspec/changes/*/tasks.md`(active changes only — 不扫 `openspec/archive/`,不扫 `proposal.md`);glob 使用 `pathlib.Path('openspec/changes').glob('*/tasks.md')` — 避免任何含 `changes/` substring 的 archive path 误匹配
- **Per-change aggregation**: count + first-3 samples,每 sample truncate 策略 = `match[:80] + "..."` if `len(match) > 80` else `match`(trailing ellipsis,简单 sufficient)
- **Multi-line normalization**: raw match 内部 `\r\n` → ` ` + `\n` → ` ` + `\r` → ` `(handles Windows CRLF + Unix LF + 单 `\r`,multi-platform compatibility)
- **Code-block / HTML comment scope decision**:**INCLUDE** annotations inside fenced code blocks(```` ``` ````) 和 HTML 注释(`<!-- ... -->`)。Rationale: tasks.md 是 plain markdown,真实使用中 annotations 极少嵌 code block;HTML comments 历史 used to hide WIP notes 也算 carry-forward 价值。Edge-case 实证频繁误命中可加 exclude rule(future Spec)
- **Empty / missing tasks.md**:active change directory 内 `tasks.md` 不存在 → silently skip(不算 error,不计入 total);存在但空文件 → regex 0 match → count=0,该 change 不出现在 `by_change` map(`by_change.get(change_id, {count:0, samples:[]})` 缺省)
- **Nested brackets `[[carry-forward: x]]`**:非贪婪 `[\s\S]*?` 在第一个 `]` 停止,产 sample = `[carry-forward: x]`(外层 `]` 保留为下一独立 match 候选,实际不命中 — 等价于 1 annotation)。此为可接受语义(用户更可能误手抖 `[[` 而非 nest 意图)

### Change 3 — Recommendation rule `carry_forward_pile`(2-tier)

`RECOMMENDATION_RULES.md` 增加 2-tier 新规则(per R1 backend-architect + qa-engineer 双 agent 共识 — 单 threshold ≥5 silent floor 1-4 风险):

```yaml
- name: carry_forward_info
  priority: 80  # INFO tier, lower priority than WARNING
  condition: 0 < openspec.carry_forward_inventory.total < 5
  action: info_note   # 显示在 status 输出末尾,不影响 primary recommendation
  format: "ℹ {{total}} inline carry-forward annotation(s) across {{by_change.keys() | join(', ')}}"
  block: false

- name: carry_forward_pile
  priority: 50  # advisory WARNING, doesn't downgrade primary
  condition: openspec.carry_forward_inventory.total >= 5
  action: advisory_warning
  format: |
    ⚠ Active OpenSpec changes have {{total}} accumulated inline carry-forward annotations.
    Top by count: {{by_change | sort_desc | first(3) | format_brief}}
    Suggest: consolidate to project_v<XX>_carry_forward.md before next major checkpoint,
    or address in current implementation phase.
  block: false
```

Threshold tier rationale:
- `>=5` 灵感 #90 TH v0.3.2 真实案例(7 项 trigger)+ Aria 5/35 Skill 分布"小数效应"经验(5 是 multi-source 累积下限)
- `1 <= total < 5` 也 surface(避免 silent floor)— 只是降级到 INFO,不打断 primary workflow recommendation
- `total == 0` 不输出任何信号(zero-noise principle)

**Output UI contract**:advisory output 出现在 state-scanner 标准输出的"🎯 推荐工作流"section **之前**,与"📋 OpenSpec 状态"section 并列(独立 section header 形如 `📌 Carry-forward inventory` + 单行 summary)。INFO 用单行 inline,WARNING 用 indented 多行块,保 visual distinction。具体格式见 [output-formats.md](./../../../aria/skills/state-scanner/references/output-formats.md) 扩展(Phase B.5.1 实施)。

### Change 4 — Tests

`aria/skills/state-scanner/tests/test_openspec.py` 增加 `TestCarryForwardInventory` 测试类(**16 cases** post-R1 audit gap fills):

**Core cases (R0 baseline)**:
1. `test_no_annotations_returns_zero_total` — `tasks.md` 无 carry-forward → `total=0`,`active_change_count=N` 反映实际 N active changes
2. `test_single_carry_forward` — 1 annotation → count=1, sample truncate trailing `...` 若 >80 chars
3. `test_mixed_token_types` — 同 file 含 carry-forward + TODO + PASS-with-note + defer + known gap → 全 capture
4. `test_hyphen_vs_space_variants` — `[known gap]` vs `[known-gap]` vs `[deferred]` vs `[defer]` 全 match
5. `test_multi_change_aggregation` — 2 active changes 各 3 项 → `total=6`, `by_change` 含 2 keys
6. `test_archive_excluded` — `openspec/archive/<change>/tasks.md` 含 annotation NOT counted
7. `test_multi_line_annotation_normalized` — `[carry-forward:\n  detail]` → single-line sample(`\n` → ` `)
8. `test_substring_shadow_guard_token_extension` — `[carry-forwarded-detail]` 不命中(`\b` after `carry-forward` blocks substring extension)
9. `test_first_3_samples_truncation` — 5 annotations 中只保留前 3 + 各 truncate 80 chars

**Gap fills (R1 audit findings)**:
10. `test_empty_tasks_md` — `tasks.md` 0 字节 → count=0 for that change
11. `test_missing_tasks_md` — active change dir 无 `tasks.md` → silently skipped(not in `by_change`)
12. `test_proposal_md_not_scanned` — annotation in `proposal.md` NOT counted(scope-glob only `tasks.md`)
13. `test_crlf_line_endings_normalized` — `[carry-forward:\r\n  windows-detail]` → `\r\n` → ` ` 正常合并
14. `test_nested_brackets_handled` — `[[carry-forward: x]]` 命中 1 次(非贪婪 `*?` 在第一个 `]` 停止)
15. `test_archive_substring_in_path_not_matched` — 路径含 `archive/old-changes/sub/tasks.md` 不被 glob `openspec/changes/*/tasks.md` 匹配
16. `test_code_block_and_html_comment_included` — annotation 在 ```` ``` ```` 代码块内 / `<!-- ... -->` 注释内 都被 count(scope decision per §Change 2 INCLUDE policy)

**Note**: 0 active changes 场景 by structure trivial(`active_changes=[]` 时 `by_change={}` empty,无需 dedicated test)。Performance bound test(1MB+ tasks.md)defer 到 future Spec — 当前 real-world tasks.md 远不到此量级(Aria 最大 spec ~30KB tasks.md)。

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
- ❌ **Large tasks.md performance bound test** (R1 qa-engineer F6 + R2 qa-engineer 重申):当前 Aria 最大 tasks.md ~30KB,1MB+ 场景 real-world 未出现。如 future 大型 OpenSpec(>500KB tasks.md)出现,可加 perf bound test + 单 file IO 上限 + early-truncate fallback。本 Spec 不前置实现
- ❌ **TODO token 严格 qualifier**(R2 qa-engineer):当前 `TODO` token alternative 接受 `[TODO: anything]`;若 future 实证 task cross-reference 类 `[TODO: TASK-012]` 误命中率高,可加 stricter qualifier(e.g., 要求 `TODO\b[: ]`)。本 Spec 保 permissive,优先 false-positive over false-negative(carry-forward surfacing 的本意是宁可多 surface 不要漏)

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

1. `python3 -m pytest aria/skills/state-scanner/tests/test_openspec.py::TestCarryForwardInventory` 全 PASS(**16 cases** post-R1 gap fills)
2. 手动 dogfood(B.7 task):在 Aria 主仓 active OpenSpec(本 Spec 自身的 tasks.md)内塞 5 项 `[carry-forward: dogfood-test-N]` → run `/state-scanner` → snapshot 含 `total=5`,recommendation output 含 carry_forward_pile advisory warning(per §Change 3 UI contract)。**Atomicity guard**:dogfood 前 `git add -A && git stash` snapshot working tree,B.7.5 cleanup 后 `git stash pop` 验证 working tree 与 dogfood 前一致(防 cleanup 失败留垃圾)
3. Rule #6 benchmark: deterministic structural verification(fixture project 含 2 active changes / 7 annotations → snapshot `total == 7` exact match)PASS,via `/skill-creator benchmark --mode=structural-deterministic`(per `feedback_rule6_framing_differs_by_skill_type` collector Skill 路径)
4. Phase D handoff doc 覆盖 Spec full cycle ship,4-repo 3-way SHA parity post-merge
5. Forgejo #90 + #89 close — **manual post-merge step**(owner 在 PR merge 后手工 close):#90 reference 本 PR + "addressed via primary spec";#89 reference 本 PR + "addressed via 选项 B variant (active-only scan + advisory rule + inventory field;exclude 选项 C `_carry_forward.md` running file + 选项 D `.aria/state-checks.yaml` self-config)"。close mechanism 不自动化(无 hook 配置,简单 manual 即可)

### #89 close-by-reference selection table

| #89 选项 | 本 Spec 覆盖? | 说明 |
|---------|---------------|------|
| 选项 A — new Phase 1.X "Active openspec carry-forward scan" | ✅ 部分(作为 Phase 1.6 sub-section,非独立 Phase) | 实际实现 fold 到 existing 1.6 collector(scope creep 最低) |
| 选项 B — 通用化 detect 任意 TODO/FIXME/carry-forward | ✅ 完全 | 本 Spec §Change 2 token alternatives 含 TODO + carry-forward + defer + known-gap + PASS-with-note |
| 选项 C — `_carry_forward.md` running file convention | ❌ Non-Goal | future Spec / 用户可自配 `.aria/state-checks.yaml` 实现 |
| 选项 D — `.aria/state-checks.yaml` user-config grep check | ❌ Non-Goal | 同上,本 Spec 仅 in-Skill detection |

## Cross-references

- Forgejo Issue [#90](https://forgejo.10cg.pub/10CG/Aria/issues/90) — primary trigger
- Forgejo Issue [#89](https://forgejo.10cg.pub/10CG/Aria/issues/89) — superset(本 Spec covers 选项 B variant of #89)
- Related:Issue #54(audit data availability)/ #79(mid-implementation spec-drift trigger)— 同 family "silent gaps in state-scanner" theme
- Predecessor handoff:[`2026-05-20-m5-phase-b-shipped.md`](../../../docs/handoff/2026-05-20-m5-phase-b-shipped.md) — 本 Spec 是 §6 Path B 推荐填充 cycle
- Aria methodology:CLAUDE.md "认知框架 §1 规范先行" + "Rule #5 项目变更必须在项目的 openspec/changes/" + "Rule #6 Skill 基准测试必须使用 /skill-creator"
- Memory entry referenced:[`feedback_word_boundary_root_causes_substring_shadows`](../../../../.claude/projects/-home-dev-Aria/memory/feedback_word_boundary_root_causes_substring_shadows.md)
