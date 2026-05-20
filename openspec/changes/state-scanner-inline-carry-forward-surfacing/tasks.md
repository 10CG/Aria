# state-scanner inline carry-forward surfacing — tasks

> **Spec proposal**: [proposal.md](proposal.md)
> **Level**: 2 (Minimal)
> **Estimated cycle**: ~3-4h(本 Spec 半 session draft + 下 session B+C+D 推完 OR 同 session 全推)
> **Status**: Draft(post-A.1 — R1 pre_spec audit pending)

---

## Phase A: Planning

- [x] A.0 — state-scanner ran(`.aria/state-snapshot.json` ✓ exit 0)
- [x] A.1 — Spec proposal drafted(本 file + `proposal.md` 创建)
- [ ] A.2 — Pre-spec audit R1(可选 Level 2,但 fill cycle 时间允许 = 推荐跑)
  - [ ] audit-engine post_spec(adaptive,Level 2 → convergence mode)
  - [ ] 等 R1 audit verdict(PASS / CONVERGE 后进 Phase B)
- [ ] A.3 — N/A(单 Skill change,无 Agent 分配需要)

## Phase B: Development

### B.1 — 分支 + scaffolding

- [x] B.1.1 — feature branch created `feature/state-scanner-inline-carry-forward-surfacing` ✓
- [ ] B.1.2 — verify aria submodule clean,confirm 在 `aria` subdir 内独立 feature branch(命名 `feature/inline-carry-forward-surfacing`,parent 同名)

### B.2 — Collector enhancement(`aria/skills/state-scanner/scripts/collectors/openspec.py`)

- [ ] B.2.1 — 新增 helper `_extract_carry_forward_annotations(tasks_md_content: str) -> list[str]`:
  - regex `r'\[(?:carry-forward|TODO|defer(?:red)?|known[ -]gap|PASS-with-note)[^\]]*\]'` word-boundary
  - multi-line annotation 内部 `\n` → ` ` normalize
  - 返回 raw matches list(no dedup,顺序保留 tasks.md 内出现顺序)
- [ ] B.2.2 — main collector function 内集成:
  - 对每个 `openspec/changes/<change>/tasks.md`(active only — `glob('openspec/changes/*/tasks.md')`,不含 archive)
  - 调用 helper → 累积 per-change `{count: int, samples: list[str]}`,samples 取前 3 + 各 truncate 80 chars
  - 顶层 `total` = sum of all per-change counts
- [ ] B.2.3 — 添加到 snapshot output:`snapshot['openspec']['carry_forward_inventory'] = {...}`

### B.3 — Recommendation rule

- [ ] B.3.1 — `aria/skills/state-scanner/RECOMMENDATION_RULES.md` 加 `carry_forward_pile` rule(advisory,priority 50,threshold ≥5,non-blocking)
- [ ] B.3.2 — 验证 rule engine 实现位置(若 RECOMMENDATION_RULES.md 是纯 doc + AI 解读型,则 doc 更新即足;若有代码层 dispatcher,同步更新)

### B.4 — Tests(`aria/skills/state-scanner/tests/test_openspec.py`)

- [ ] B.4.1 — Add `TestCarryForwardInventory` test class with 9 cases per proposal §Change 4:
  - test_no_annotations_returns_empty
  - test_single_carry_forward
  - test_mixed_token_types
  - test_hyphen_vs_space_variants
  - test_multi_change_aggregation
  - test_archive_excluded(关键 guard)
  - test_multi_line_annotation_normalized
  - test_substring_shadow_guard(word-boundary regression)
  - test_first_3_samples_truncation
- [ ] B.4.2 — `pytest aria/skills/state-scanner/tests/test_openspec.py -v` 全 PASS
- [ ] B.4.3 — Full regression run:`pytest aria/skills/state-scanner/tests/` 全 PASS(确保不破 #101 现有 13 cases + 其它)

### B.5 — Documentation

- [ ] B.5.1 — `aria/skills/state-scanner/SKILL.md` Phase 1.6 表格 + 子阶段表添加 `openspec.carry_forward_inventory` 字段说明
- [ ] B.5.2 — `aria/skills/state-scanner/references/state-snapshot-schema.md` 增加 `openspec.carry_forward_inventory` schema 定义(additive)
- [ ] B.5.3 — `aria/skills/state-scanner/RECOMMENDATION_RULES.md` 验证 rule 文档完整

### B.6 — Rule #6 benchmark(structural deterministic verification)

- [ ] B.6.1 — Create benchmark fixture:`aria-plugin-benchmarks/structural/state-scanner-carry-forward/`
  - fixture project with 2 active OpenSpec changes,each 含 3-5 inline annotations(共 7 total)
  - expected snapshot output: `total=7, by_change[change-A].count=3, by_change[change-B].count=4`
- [ ] B.6.2 — `/skill-creator benchmark` run on state-scanner(deterministic verification flag)
- [ ] B.6.3 — Verify `with_skill` vs `without_skill` delta(structural metric:`exact match on carry_forward_inventory.total + by_change keys`)
- [ ] B.6.4 — 结果存入 `aria-plugin-benchmarks/ab-results/state-scanner-carry-forward-<TS>/`

### B.7 — Dogfood

- [ ] B.7.1 — 在本 Spec 自己的 `tasks.md` 末尾塞 5 行 `[carry-forward: dogfood-test-N]` annotations
- [ ] B.7.2 — `python3 aria/skills/state-scanner/scripts/scan.py --output .aria/state-snapshot.json`
- [ ] B.7.3 — Verify snapshot output: `openspec.carry_forward_inventory.total >= 5` + 含 `state-scanner-inline-carry-forward-surfacing` change key
- [ ] B.7.4 — Verify recommendation output contains `carry_forward_pile` advisory warning
- [ ] B.7.5 — DELETE dogfood annotations(本 Spec ship 前自洁)

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

## Open questions(post-A.1 + pre-R1 audit)

- Q1:RECOMMENDATION_RULES.md 是否有 code-level dispatcher?如有,B.3.2 需同步代码;否则纯 doc 更新即可。Audit R1 决定。
- Q2:Rule #6 benchmark "structural deterministic" pattern 是否与 `feedback_rule6_framing_differs_by_skill_type` 对齐?(本 Spec 是 collector-level deterministic — 期待 with_skill 100% / without_skill 0% exact match)
- Q3:Threshold `>=5` 是否合理?#90 案例 7 项 trigger,5 是 conservative。Audit R1 / dogfood B.7 验证后回调。
