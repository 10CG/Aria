# state-scanner carry-forward inventory — structural benchmark

> **Skill**: `state-scanner` (v1.23.0 enhancement,Spec `state-scanner-inline-carry-forward-surfacing`)
> **Mode**: structural deterministic (per [`feedback_rule6_framing_differs_by_skill_type`](../../../.claude/projects/-home-dev-Aria/memory/feedback_rule6_framing_differs_by_skill_type.md))
> **Created**: 2026-05-20 (Phase B.7 of Spec cycle)
> **Authority**: Rule #6 substitute(/skill-creator AB 不适用 — 见下方 Framing 决策)

---

## Framing 决策

Rule #6 standard pattern = `/skill-creator benchmark` with/without LLM AB delta(适用 capability-style Skills,LLM 主观判断输出质量)。

本 Spec 是 **deterministic structural collector enhancement**:additive snapshot field `openspec.carry_forward_inventory`,exact-match metric。`with_skill` vs `without_skill` 在数学上 binary:
- **with_skill** (post v1.23.0 collector):snapshot 含 `openspec.carry_forward_inventory.{total, active_change_count, by_change}`,total = exact match of injected annotation count
- **without_skill** (pre v1.23.0 collector):snapshot 不含 `openspec.carry_forward_inventory` field,total field absent or null

任何 fixture input → with_skill 100% PASS / without_skill 0% PASS。LLM AB 在此 framing 下无信号(deterministic 已 100% confidence)。

per `feedback_rule6_framing_differs_by_skill_type` memory entry:
> "Rule #6 benchmark AB 框架按 Skill 类型:capability / structural / deterministic 三种 metric,不一刀切 LLM with/without"

本 Skill = **structural deterministic** → unit tests + live dogfood 已构成 binary deterministic evidence。

---

## Evidence (本 Spec Phase B 实证)

### 16 unit tests (TestCarryForwardInventory)

`aria/skills/state-scanner/tests/test_openspec.py::TestCarryForwardInventory`,covers:

- **9 core cases**:no-annotations / single / mixed tokens / hyphen-space variants / multi-change aggregation / archive-excluded / multi-line normalize / substring shadow guard / first-3 truncation
- **7 R1-audit gap fills**:empty tasks.md / missing tasks.md / proposal.md negative scope / CRLF normalization / nested brackets / archive substring not matched / code-block + HTML comment INCLUDE

**Result**: 16/16 PASS on first run。Full regression (584 tests) PASS。

### Live dogfood (B.6, 2026-05-20)

Real-spec scan on `/home/dev/Aria/openspec/changes/state-scanner-inline-carry-forward-surfacing/`:
- **Baseline** (本 Spec 自身 tasks.md 含 4 真实 inline annotations from R2 audit fix examples): `total = 4` ✓
- **+5 dogfood injection**: appended 5 `[carry-forward: dogfood-test-N]` annotations → `total = 9` ✓ (exact 4+5 match)
- **Cleanup** via `git checkout`: `total = 4` ✓ (baseline restored)
- **Atomicity verify** (per B.6.7): `git diff tasks.md` line count = 0 ✓

Active change count tracked correctly throughout(`active_change_count = 2`,即 M5 deploy spec + 本 Spec)。

### "Without skill" 对照(可选实地验证)

如需 explicit AB demonstration:
```bash
cd /home/dev/Aria/aria
# pre-Rev1 collector (without carry_forward_inventory):
git stash push -m "with-skill-snapshot"
git checkout master -- skills/state-scanner/scripts/collectors/openspec.py
python3 skills/state-scanner/scripts/scan.py --output /tmp/without-skill.json
# Verify: 'carry_forward_inventory' not in snapshot['openspec']
git stash pop
# post-Rev1 collector (with carry_forward_inventory):
python3 skills/state-scanner/scripts/scan.py --output /tmp/with-skill.json
# Verify: snapshot['openspec']['carry_forward_inventory']['total'] >= 0
diff <(jq '.openspec | keys' /tmp/without-skill.json) <(jq '.openspec | keys' /tmp/with-skill.json)
# Expected diff: with_skill 多一行 "carry_forward_inventory"
```

实地 mechanical 对照:**with-skill 多 1 个顶层字段;without-skill 完全无此字段**。Delta = 100% / 0% = AUTO_GATE=true 等价信号。

---

## AUTO_GATE 评估

| 维度 | 结果 |
|------|------|
| Deterministic exactness | ✅ 16/16 unit tests + dogfood 5+5 mathematical match |
| No regression | ✅ 584 tests pass full suite |
| Schema additive | ✅ snapshot_schema_version still 1.0(per state-snapshot-schema.md 演进契约) |
| Backward compat | ✅ 旧 consumers 不读 `carry_forward_inventory` 不报错 |
| Empty-state safety | ✅ `active_change_count` 字段总是 present;`total=0` 时 by_change={} |
| Cross-platform | ✅ CRLF + LF + 单 \r 全 normalized(test_crlf_line_endings_normalized) |
| Word-boundary guard | ✅ #101 lesson applied via token-end `\b`(test_substring_shadow_guard_token_extension) |

**AUTO_GATE**: ✅ **true** — Rule #6 verdict satisfied via structural deterministic evidence。

---

## Storage convention

per Aria methodology(详见 `AB_TEST_OPERATIONS.md`):

- Structural benchmark fixtures + READMEs: `aria-plugin-benchmarks/structural/<skill>-<feature>/`(本目录)
- Result archive: `aria-plugin-benchmarks/ab-results/`(不适用本 case — deterministic 无 multi-round LLM 结果可 archive)

---

**Last updated**: 2026-05-20 (Phase B.7)
**Status**: AUTO_GATE=true(structural deterministic substitute for /skill-creator LLM AB)
