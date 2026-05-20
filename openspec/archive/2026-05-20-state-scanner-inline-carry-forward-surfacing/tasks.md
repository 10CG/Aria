# state-scanner inline carry-forward surfacing — tasks

> **Spec proposal**: [proposal.md](proposal.md)
> **Level**: 2 (Minimal)
> **Estimated cycle**: ~3-4h(本 Spec 半 session draft + 下 session B+C+D 推完 OR 同 session 全推)
> **Status**: **Approved (R2 CONVERGED)** — A.2 complete (R1 REVISE → Rev1 → R2 PASS_WITH_WARNINGS unanimous → Rev1.1 sync) — Ready for Phase B in next dedicated session

---

## Phase A: Planning

- [x] A.0 — state-scanner ran(`.aria/state-snapshot.json` ✓ exit 0)
- [x] A.1 — Spec proposal drafted(本 file + `proposal.md` 创建)
- [x] A.2.0 — **Pre-B Q1 dispatcher discovery**(resolve Q1 — RECOMMENDATION_RULES.md is doc-only OR has code dispatcher?):
  - grep `aria/skills/state-scanner/scripts/` 查找 RECOMMENDATION_RULES.md 实施位置
  - 决定:Q1 答案 = pure-doc(AI 解读)→ B.3 是纯 doc 任务;OR code-dispatcher 存在 → B.3 同步更新代码
  - 结论锁入 tasks.md(R2 audit 前)
- [x] A.2 — Pre-spec audit ✅ CONVERGED
  - [x] R1 — 3 agents(tech-lead / backend-architect / qa-engineer)→ all REVISE,0 critical / 5 majors / ~12 minors → Rev1 addresses
  - [x] R2 — re-run 3 agents on Rev1 → **unanimous PASS_WITH_WARNINGS**(all R1 majors ADDRESSED + 0 new critical/major + ~6 new minors,含 1 cross-agent converged regex sync drift)→ Rev1.1 sync
- [ ] A.3 — N/A(单 Skill change,无 Agent 分配需要)

## Phase B: Development

### B.1 — 分支 + scaffolding

- [x] B.1.1 — feature branch created `feature/state-scanner-inline-carry-forward-surfacing` ✓
- [ ] B.1.2 — verify aria submodule clean,confirm 在 `aria` subdir 内独立 feature branch(命名 `feature/inline-carry-forward-surfacing`,parent 同名)

### B.2 — Collector enhancement(`aria/skills/state-scanner/scripts/collectors/openspec.py`)

- [ ] B.2.1 — 新增 helper `_extract_carry_forward_annotations(tasks_md_content: str) -> list[str]`:
  - regex `r'\[(?:carry-forward|TODO|defer(?:red)?|known[ -]gap|PASS-with-note)\b[\s\S]*?\]'`(per proposal.md §Change 2 Rev1 — `[\s\S]*?` 跨行非贪婪 + token-end `\b` 防 substring shadow)
  - multi-line normalization:`\r\n` → ` ` + `\n` → ` ` + `\r` → ` `(handles CRLF + LF + 单 CR)
  - 返回 raw matches list(no dedup,顺序保留 tasks.md 内出现顺序)
  - **TODO false-positive note** (R2 qa-engineer minor): `[TODO: TASK-012 title]` 类 task cross-reference 会被命中 — 这是 acceptable false-positive(TODO 本身就是 carry-forward 语义);若实证误命中率高,future Spec 可 stricter qualify(e.g., 要求 `[TODO:`); 当前不 over-engineer
- [ ] B.2.2 — main collector function 内集成:
  - 对每个 `openspec/changes/<change>/tasks.md`(active only — `pathlib.Path('openspec/changes').glob('*/tasks.md')`,**严格不含 archive**)
  - 调用 helper → 累积 per-change `{count: int, samples: list[str]}`,samples 取前 3 + 各 truncate `match[:80] + "..."` if `len > 80` else `match`(trailing ellipsis)
  - 顶层 `total` = sum of all per-change counts
  - 顶层 `active_change_count` = count of active changes (区分 0 active vs N active 但 0 annotations)
- [ ] B.2.3 — 添加到 snapshot output:`snapshot['openspec']['carry_forward_inventory'] = {total, active_change_count, by_change}`(字段总是 present,empty 时 `total=0`)

### B.3 — Recommendation rule(doc-only per A.2.0 discovery)

> **A.2.0 conclusion**: `RECOMMENDATION_RULES.md` 是 pure documentation(AI-interpreted)。`scripts/` 内无 recommendation dispatcher code。B.3 是纯 doc 任务。

- [ ] B.3.1 — `aria/skills/state-scanner/RECOMMENDATION_RULES.md` 加 2-tier 规则:
  - `carry_forward_info`(INFO tier,priority 80,1≤total<5,non-blocking)
  - `carry_forward_pile`(WARNING tier,priority 50,total≥5,non-blocking)
  - 完整 format 见 proposal.md §Change 3

### B.4 — Tests(`aria/skills/state-scanner/tests/test_openspec.py`)

- [ ] B.4.1 — Add `TestCarryForwardInventory` test class with **16 cases** per proposal §Change 4(post-R1 gap fills):
  Core (R0):
  - test_no_annotations_returns_zero_total
  - test_single_carry_forward
  - test_mixed_token_types
  - test_hyphen_vs_space_variants
  - test_multi_change_aggregation
  - test_archive_excluded(关键 guard)
  - test_multi_line_annotation_normalized
  - test_substring_shadow_guard_token_extension(`\b` after token blocks `carry-forwarded`)
  - test_first_3_samples_truncation
  Gap fills (R1 audit):
  - test_empty_tasks_md(0 bytes file)
  - test_missing_tasks_md(active change dir 无 tasks.md → silently skipped)
  - test_proposal_md_not_scanned(negative scope guard)
  - test_crlf_line_endings_normalized(\r\n → space)
  - test_nested_brackets_handled([[carry-forward: x]] = 1 match,非贪婪 *? 在第一个 ] 停止)
  - test_archive_substring_in_path_not_matched(glob 严格 `changes/*/tasks.md`,排除 `archive/old-changes/...`)
  - test_code_block_and_html_comment_included(INCLUDE policy per §Change 2)
- [ ] B.4.2 — `pytest aria/skills/state-scanner/tests/test_openspec.py -v` 全 PASS(16 new + 13 existing #101 = 29 cases)
- [ ] B.4.3 — Full regression run:`pytest aria/skills/state-scanner/tests/` 全 PASS(确保不破 现有 ~40 tests)

### B.5 — Documentation

- [ ] B.5.1 — `aria/skills/state-scanner/SKILL.md` Phase 1.6 表格 + 子阶段表添加 `openspec.carry_forward_inventory` 字段说明
- [ ] B.5.2 — `aria/skills/state-scanner/references/state-snapshot-schema.md` 增加 `openspec.carry_forward_inventory` schema 定义(additive)
- [ ] B.5.3 — `aria/skills/state-scanner/RECOMMENDATION_RULES.md` 验证 rule 文档完整

### B.6 — Dogfood(顺序前置 per R1 tech-lead — dogfood discoveries feed benchmark fixture design)

> **R1 audit reordering**: B.6 dogfood 先于 B.7 benchmark。Rationale: dogfood 在真实 Spec 上发现 edge cases → 反馈给 B.7 fixture 设计,benchmark 更可信。

- [ ] B.6.1 — **Atomicity guard**:`git add -A && git stash push -m "pre-dogfood-snapshot-state-scanner-carry-forward"` snapshot working tree pre-state
- [ ] B.6.2 — 在本 Spec 自己的 `tasks.md` 末尾塞 5 行 `[carry-forward: dogfood-test-N]` annotations(N=1..5)
- [ ] B.6.3 — `python3 aria/skills/state-scanner/scripts/scan.py --output .aria/state-snapshot.json`
- [ ] B.6.4 — Verify snapshot output:
  - `openspec.carry_forward_inventory.total >= 5`
  - `openspec.carry_forward_inventory.active_change_count` 正确反映 N active changes
  - `by_change` 含 `state-scanner-inline-carry-forward-surfacing` change key + count=5
- [ ] B.6.5 — Verify recommendation output contains `carry_forward_pile` advisory warning(WARNING tier per 2-tier rule)
- [ ] B.6.6 — DELETE dogfood annotations from tasks.md
- [ ] B.6.7 — **Atomicity verify**:`git diff --no-color tasks.md` 必须 empty(0 diff) OR `git stash pop` restore + assert clean。**若 verify fail**(working tree 有意外 diff)→ abort B.6 + 调查
- [ ] B.6.8 — 任何 dogfood 发现的 edge cases 记入 B.7 fixture 设计

### B.7 — Rule #6 benchmark(structural deterministic verification)

> per `feedback_rule6_framing_differs_by_skill_type` — state-scanner = collector Skill = **deterministic metric**,非 LLM AB

- [ ] B.7.1 — Create benchmark fixture:`aria-plugin-benchmarks/structural/state-scanner-carry-forward/`
  - fixture project with 2 active OpenSpec changes,each 含 3-4 inline annotations(共 7 total)
  - fixture 含 B.6 dogfood 暴露的 edge cases(若有)— e.g., CRLF / multi-line / nested brackets actual usage shape
  - expected snapshot output: `total=7, by_change[change-A].count=3, by_change[change-B].count=4, active_change_count=2`
- [ ] B.7.2 — `/skill-creator benchmark --mode=structural-deterministic` run on state-scanner(**exact-match metric** on `carry_forward_inventory.total` + `by_change` keys + counts;not LLM AB)
- [ ] B.7.3 — Verify `with_skill` 100% / `without_skill` 0% on exact match metric(deterministic Skill = binary)
- [ ] B.7.4 — 结果存入 `aria-plugin-benchmarks/ab-results/state-scanner-carry-forward-<TS>/`

### B.8 — Version bump(5+1 SOT atomic)

- [ ] B.8.1 — `aria/.claude-plugin/plugin.json` version `v1.22.1` → `v1.23.0`(MINOR for new Skill feature)
- [ ] B.8.2 — `aria/.claude-plugin/marketplace.json` version + plugins[].version sync
- [ ] B.8.3 — `aria/VERSION` sync
- [ ] B.8.4 — `aria/CHANGELOG.md` 新条目 v1.23.0:summary + collector enhancement + benchmark
- [ ] B.8.5 — `aria/README.md` version 引用 sync
- [ ] B.8.6 — 主项目 `VERSION`(若 plugin version 引用)sync

## Phase C: Integration

- [ ] C.1.1 — aria submodule commit on feature branch + push
- [ ] C.1.2 — Aria 主仓 commit(spec proposal + tasks + gitlink bump)+ push
- [ ] C.2.1 — aria-plugin PR create(feature → master)
- [ ] C.2.2 — pre_merge audit(adaptive Level 2 → convergence)— Rule #8 gate
- [ ] C.2.3 — `aether ci status --branch master --in-flight --json` GREEN check(无 in-flight CI race)
- [ ] C.2.4 — aria-plugin PR merge + multi-remote push(forgejo + github)
- [ ] C.2.5 — Post-merge:Aria 主仓 gitlink re-bump 到 aria post-merge HEAD(per `feedback_sequenced_multirepo_gitlink_bump`)
- [ ] C.2.6 — Aria 主仓 PR create + same Rule #8 gate + merge + multi-remote push

## Phase D: Closure

- [ ] D.1 — Forgejo issue close:#90 closed-by-PR / #89 closed-by-reference(链 PR + addressed-via summary)
- [ ] D.2 — `openspec/changes/state-scanner-inline-carry-forward-surfacing/` → `openspec/archive/2026-05-XX-state-scanner-inline-carry-forward-surfacing/`
- [ ] D.3 — Handoff doc:`docs/handoff/2026-05-XX-state-scanner-carry-forward-shipped.md`(Layer H frontmatter,track-id 与本 Spec id 一致)
- [ ] D.4 — Update `docs/handoff/latest.md` Track 信息
- [ ] D.5 — 4-repo 3-way SHA parity verify(Aria main + aria + standards unchanged + aria-orchestrator unchanged)
- [ ] D.6 — Memory entry candidates review(本 Spec 实施期间发现的 lessons,owner 决定 promote)

---

## Exit criteria for this Spec

- [ ] All B.* + C.* + D.* tasks ✓
- [ ] proposal.md §Success Criteria 5 项全 met
- [ ] aria-plugin v1.23.0 released to both Forgejo + GitHub(market 拉得到)
- [ ] Phase D handoff doc covers full cycle

---

## Dependencies / Blockers

- ✅ None — purely Skill collector enhancement,无 cross-project dependency
- ✅ Phase B (M5 deploy) 不冲突 — Phase B 在 light-1 prod,本 Spec 在 dev container Aria 主仓 + aria submodule

## Open questions — R1 audit 已解决

- ~~Q1:RECOMMENDATION_RULES.md 是否有 code-level dispatcher?~~ ✅ **A.2.0 答**:pure documentation (AI-interpreted),`scripts/` 无 dispatcher code → B.3 doc-only
- ~~Q2:Rule #6 benchmark "structural deterministic" pattern 是否与 `feedback_rule6_framing_differs_by_skill_type` 对齐?~~ ✅ **R1 qa-engineer 确认**:collector Skill = deterministic exact-match metric,B.7 已 explicit `--mode=structural-deterministic` flag
- ~~Q3:Threshold `>=5` 是否合理?~~ ✅ **R1 backend-architect + qa-engineer 共识**:改 2-tier(INFO 1≤total<5 / WARNING ≥5)— 避免 silent floor

**All 3 Open Questions 已解决,无 R2 pre-condition blocker。**
