---
track-id: us026-m6-phase-a-spec-batch
owner-container: simonfish/dev-claude
phase: phase-a-closed
status: closed
updated-at: 2026-05-24T16:30:00Z
---

# Aria — Session Handoff (2026-05-24 ~16:30 UTC) — Track G: M6 Phase A Spec Batch (3/4 Approved)

> **Status**: 🎉 **M6 Phase A.1 + A.2 CONVERGED for 3 of 4 sub-Specs** (Spec #1 cost-acceptance + Spec #2 e2e-resilience + Spec #3 docs all Approved). 4 owner Q-locks applied (Q1-Q4 + AI-pre-decided Q5). 16 audit reports committed. Spec #4 release-closeout deferred to next session (depends on #1+#2+#3 done, all 3 done now).
> **Predecessor (same day, Track F)**: [M6 brainstorm CONVERGED](./2026-05-24-m6-brainstorm-converged-track-f.md) (~00:45 UTC, DEC-20260524-001 4 sub-Specs ~82h locked)
> **Sister Track (dev-claude2 parallel)**: [Track E follow-ups #16+#17](./2026-05-24-track-e-followups-17-16-done.md) (~11:50 UTC) + [Aria #124 regression-gate Spec Approved](./2026-05-24-aria-124-spec-approved.md) (~15:20 UTC)
> **Session 性质**: 高强度连续 ~6.2h (10:21→16:30 UTC), 3 cycles 完整 Phase A (Spec #1 + #2 sister + #3 sister)。

---

## §0 入口 (新 session 优先读)

按 Aria Rule #9 + state-scanner Phase 1.15 collector 自动 surface:

1. **本 doc** — Track G M6 Phase A Spec batch 闭环 + 下次 session 入口
2. **Phase A.2 audit reports (16 总)**:
   - Spec #1 (8): R1-{4 raw + aggregate} + R2-{3 raw} + R3-stability
   - Spec #2+#3 sister (8): R1-{4 raw + aggregate} + R2-{3 raw} + R3-stability
3. **US-026 Status**: Phase A.1 × 3/4 sub-Specs Approved (Spec #4 释 backlog 待 next session)
4. **Sister dev-claude2 同日 ship**:
   - Track E follow-ups #16/#17 (`2945f61` Phase A.1 + `7e684b0` Phase A.2 Rev1 + `1a06bbd` Approved)
   - Aria #124 regression-gate Spec full Phase A→Approved 同步实证 X-T2 cross-ref source
5. **Aria #124 regression-gate Spec (dev-claude2 CONVERGED)**: 提供 Spec #3 T-B0.10 v1.29.0 block-mode gate 的 SoT canonical pattern (lines 86-87)

→ **next session**:
- **Path A (推荐)**: Spec #4 `aria-2.0-m6-release-closeout` Phase A.1 + A.2 (~10h Level 2, tech-lead agent), 然后 4 sub-Specs 全 Phase A 关门
- **Path B**: 跳过 Spec #4 drafting,直接 Spec #1 Phase B.1 启动 (Spec #1 c29a800 唯一可启动 because Spec #2 gated on Spec #1 AC-7; Spec #3 独立但 Spec #4 未存在)
- **Path C**: Spec #1 Phase B.1 + Spec #4 Phase A 并行 (2 agent + multi-cycle)

---

## §1 已完成 (本 session, ~6.2h, 3 Phase A cycles + 2 PRD patches + 2 hygiene + 多终端协调)

### Cycle 1: Spec #1 `aria-2.0-m6-cost-acceptance` Phase A.1 + A.2 ~45min (10:30→11:15 UTC)

| Stage | Output |
|-------|--------|
| Pre-work | Hygiene [4]+[5]: standards typo `6fcce24` + pyyaml install + issues cache clear |
| PRD patches | M6 reframe 3w→5w + cost gate dual-track (`a786444`, dual-push 3-way parity after 2 rebases) |
| Phase A.1 draft | backend-architect agent: proposal.md 444 / tasks.md 209 (32 tasks) |
| Phase A.2 R1 (4-agent parallel) | NEEDS_FIX 4/4: 11 unified Critical (de-dup from 12 raw) + 8 Important |
| Owner Q1-Q4 | AC-9 exit code lift / pricing freshness check / USD only / AD-M6-1/2/3 lock |
| R1-fix → R2 (3-agent challenge) | SCOPE_OK_R2 conditional 3/3, 90.6% reduction; 1 NEW Critical (REPO_ROOT off-by-1, self-spot) + 2 Important |
| R2-fix → R3 stability (1-agent) | R3_STABLE — 0 new C + 0 new I; 3/3 R2 fixes CLOSED byte-for-byte |
| **CONVERGED** | proposal.md 707 / tasks.md 360 (38 tasks) / 10 AC / ~12h impl baseline / commit `c29a800` |

### Cycle 2 + 3 (parallel): Spec #2 + #3 Phase A.1 + A.2 ~3h (12:00→15:30 UTC)

**Phase A.1 (parallel dispatch)**:
- Spec #2 (backend-architect): proposal 843 / tasks 791 / 7 AC / ~29h / AD-M6-4/5/6
- Spec #3 (knowledge-manager): proposal 595 / tasks 462 / 10 AC / ~33h / AD-M6-7/8

**Phase A.2 R1 (4-agent combined sister-Spec mode)**: NEEDS_FIX 4/4
- ~25 raw Critical → 10 de-dup themes (6 Spec #2 + 5 Spec #3 + 5 X-Critical)
- Combined-mode 实证: 5 X-Critical 只在 cross-Spec verification 才 caught (BOTH-locations path drift / DEC-002 non-consumption / mean-median PRD-Spec contradiction / AD-M5-11 multi-source collision / rubric dimension mismatch)

**Owner Q1-Q4 (4 R1 escalations)**:
- Q1: Path B multi-file cov target (no state_machine.py file extraction)
- Q2: AD-M6-9 (drop AD-M5-11 claim, live `architecture-decisions.md:3460-3478` reserved for M5-spillover)
- Q3: Patch PRD §568 to follow Spec (km M-km-R2-005 authoritative)
- Q4: Patch PRD §656 mean → median (bimodal-score robust)
- Q5 AI-pre-decided: Spec #3 T-B0.10 +v1.29.0 block-mode gate (DEC-20260524-002 consumption)

**R1-fix (commit `8a5fdc4`)**: backend-architect + knowledge-manager parallel pass
- Spec #2: +233 / +166 lines (SQL columns rewrite, state_machine path B, AC-6 Luxeno=0 reframe, is_synthetic Mech A lock, AC-1 CreateTime, AC-2 check order, mean→median, I2-1..I2-8)
- Spec #3: +90 / +43 lines (CLAUDE.md 9-diff re-anchor, Probe 1 regex, plugin SoT dynamic, PRD line citations, BOTH-locations full path, T-B0.10 v1.29.0 gate, AD-M5-11→AD-M6-9 swap, rubric 7-dim sync)
- PRD §568 + §656 caught-up (`e884e62` message claimed them but stash-pop missed them; `8a5fdc4` actually shipped)

**R2 challenge (3-agent combined)**: SPLIT — cr SCOPE_OK_R2 23/23 + ai SCOPE_OK_R2 6/6 + tl-critic NEEDS_FIX (2 NEW C self-spot via cross-Spec verify)
- Per `[[feedback_cross_agent_verdict_independent_verify]]`: 1/N NEEDS_FIX MUST owner-verify, no majority-collapse
- Independent verify confirmed all 3 tl-critic findings TRUE via ls/grep + dev-claude2 parallel Spec:
  - NC-tl-R2-1: migration slot 006 collision with M5's shipped `006_schema_v4.2_add_spec_id.sql`
  - NC-tl-R2-2: Spec #3 T-B0.10 v1.29.0 gate args INVERTED vs dev-claude2's authoritative Spec lines 86-87
  - C-tl-#3-1 paper-fix completion: 4 sites `Rule #1-#6` → `#1-#9` (Chinese + English variants)

**R2-fix (commit `c0e9d79`)**: All 3 fixes byte-exact mechanical
- migration 006_schema_v5 → 007_schema_v4.3 (23 sites swept)
- gate single-call → 3-zone branching (PASS/REGRESSION/DIVERGENT, mirror dev-claude2 SoT)
- paper-fix #1-#6 → #1-#9 propagation (Chinese 规则 + English Rule + AC regex)

**R3 stability (tl-critic 1-agent scope-limited)**: **R3_STABLE** — 0 new C + 0 new I; 3/3 R2 fixes CLOSED byte-for-byte

**Approved (commit `413dd75`)**: Status flip + audit trajectory frontmatter; Spec #2 ready Phase A.3 (gated on Spec #1 AC-7 3-day data); Spec #3 ready Phase A.3 (TG-DOCS-A v2.0.0-blocker, TG-DOCS-B v2.0.1-deferrable per Q-final-1 Menu C)

### Multi-terminal coordination 实战 (dev-claude2 并行 ship 3 commits)

| Commit | Time UTC | Content | 我方 coordination |
|--------|----------|---------|-------------------|
| `c8a5f03` | 早 | aria-orch submodule bump #16+#17 | Rebase 1 (sub-pointer regression guard 接住) |
| `a4abf66` | 早 | Track E follow-ups handoff | Rebase 2 |
| `13035d8` | 中 | DEC-20260524-002 Aria #124 brainstorm | Cross-ref source for X-T2 |
| `2945f61` | 中 | Aria #124 Spec Phase A.1 drafted | Cross-ref for X-T2 fix |
| `7e684b0` | 中 | Aria #124 Spec Phase A.2 Rev1 | Cross-ref for SoT lines 86-87 |
| `1a06bbd` | 晚 | Aria #124 Spec CONVERGED Approved | **SoT validated** for Spec #3 T-B0.10 R2-fix |

Net: 6 dev-claude2 commits interleaved with 7 我方 commits = 13 commits in ~6h cross-track integration zero conflict (Layer L Phase B multi-terminal stress test 持续 pass)。

### Closeout audit (本 doc, ~16:30 UTC)

- ~3 new memory entries 固化 (combined-mode value + migration slot draft-time-verify + gate logic SoT cross-validate)
- MEMORY.md index update
- 本 Track G handoff doc
- latest.md pointer update
- Closing commit + dual push (即将)

### Total session cumulative output

| 维度 | 数量 |
|-----|------|
| Aria 主仓 commits (我方) | 7 (e54ace7 / a786444 / 6e58b75→c29a800 [4 commits Spec #1] / 5d85617 / 8a5fdc4 / c0e9d79 / 413dd75) — 当前 HEAD |
| Aria 主仓 commits (dev-claude2 interleave) | 6 (Track E + Aria #124 全 Phase A→Approved) |
| Forgejo PR | 0 (本 session 全 direct master commits, Specs 是 docs 不走 PR) |
| Forgejo Issues | 0 created |
| Memory entries written | 3 new (本 closeout) |
| Owner Q answered | 8 (Spec #1 Q1-Q4 + Spec #2/#3 Q1-Q4) |
| Sub-agent dispatches | ~30 (Spec #1: 4+1+3+1+1 backend-arch=10; Spec #2/#3: 2+4+2+3+1=12 + 8 PRD/aggregate writing) |
| Files net add | ~6 Spec files + 16 audit reports + 1 handoff = 23 |
| audit reports total | **16** (Spec #1: 8 / sister #2+#3: 8) |
| Phase A.2 rounds executed | 6 (3× R1 + 3× R2 + 2× R3 stability) |

---

## §2 未完成 / Carry-forward

### **AI-runnable next session**

| Item | 时机 | 工作量估 |
|------|-----|------|
| **Spec #4 `aria-2.0-m6-release-closeout` Phase A.1** (proposal.md + tasks.md, ~10h Level 2, tech-lead agent) | next session first | ~30min draft + ~30min audit cycle = ~1h |
| **Spec #4 Phase A.2 audit** (3-4 agent R1 + R2; R3 likely not needed for Level 2 trivial scope unless surprise) | post Spec #4 draft | ~30min |
| **Spec #1 Phase A.3 + Phase B.1** (branch creation, agent allocation done in DEC §6) | parallel with Spec #4 Phase A | depend on owner availability |
| **Spec #2 Phase A.3 + Phase B.1** (gated on Spec #1 AC-7 PASS — needs 3-day cost data accumulation) | after Spec #1 cron live ≥3 days | wall-clock 72h+ |
| **Spec #3 Phase A.3 + Phase B.1** (TG-DOCS-A v2.0.0-blocker independent of #1/#2) | any time post-Approved | ~11h impl |

### **Owner-action**

| Item | 时机 | 工作量 |
|------|-----|------|
| **Phase B.1 start order decision** | Spec #4 Approved 后 | 决策: Spec #1 first / Spec #3 TG-DOCS-A first / parallel triple |
| **Spec #1 cron daily kick** for 3-day history accumulation (Spec #2 precondition) | Phase B.1 后 | owner manual, ≥3 daily runs |
| **Pricing rotation ritual** (Q3 carry-forward) — Zhipu CNY→USD review + `_PRICING_OWNER_VERIFIED=True` | Phase B 中或前 | owner manual, ~30min |

### **跨 session 长期 carry-forward (non-session)**

| Item | Deadline | 当前状态 |
|------|---------|---------|
| Secret rotation deferred pool 4-key set | 2026-08-02 hard cap | partial rotation in progress; M6 5w timeline 压缩 buffer 到 ~36 days at start (RED threshold per Spec #4 design) |
| Plugin v1.29.0 block-mode gate ship (dev-claude2 Aria #124 Spec, 现 Approved Phase A) | Phase B by dev-claude2 | Spec #3 T-B0.10 已预 consume |
| CLAUDE.md plugin version field stale (live shows v1.22.0; plugin.json v1.27.0) | Spec #3 T-A1.9 Phase B 时修 | known |

### **Discovered patterns to consider memory-promoting later (not yet固化)**

1. **Audit cycle wall-clock 估算**: Spec #1 ~45min (single-Spec), Spec #2+#3 sister-Spec ~3h. **Sister-spec 因 R2 split + R3 needed 比 single 慢 4×**, 而非线性 2×。原因: combined-mode finding 翻倍 + 1 NEW C 在 R2 必触 R3。
2. **PRD patch via Spec audit Q-escalation**: 1 session ship 4 PRD patches (Q-final-1/Q-final-2 from brainstorm + Q3 §568 + Q4 §656 from R1 audit). PRD 在 Spec drafting 期间 "动态" 修正不是反模式, 而是正常 catch-up (spec drafter 比 PRD writer 更接近 implementation reality)。
3. **dev-claude2 multi-terminal 协调成熟度**: Layer L Phase B 设计目标全实现, 6 commits 跨终端零冲突。SoT cross-validation (我方 Spec #3 R2-fix 参考 dev-claude2 已 CONVERGED Spec) 是新涌现的工作模式。

---

## §3 关键风险 / 已知陷阱 (本 session 新增)

### Audit methodology

- **R1 — Combined-mode sister-Spec audit 是质量飞跃 vs 单 Spec dispatch**: 本 session 5 X-Critical (BOTH-locations path / DEC-002 non-consumption / mean-median / AD-M5-11 / rubric dim mismatch) + 1 R2 X-Critical (v1.29.0 gate inversion) **全部** 只在 cross-Spec verification 才 caught。Lab convention candidate: ≥2 sister-Specs MUST use combined-mode audit dispatch。
- **R2 — 1/N NEEDS_FIX vote 必须 owner 独立 verify, 不能 majority-collapse**: tl-critic 3-for-3 right。`[[feedback_cross_agent_verdict_independent_verify]]` 实证升级。
- **R3 — R2 self-introduced Critical 必 trigger R3 stability**: Spec #1 + Spec #2/#3 都遇到, 都 R3 stability PASS。1-agent scope-limited ~5-8min cheap vs 漏 caught 的 Phase B 损失。
- **R4 — Schema migration slot draft-time live-verify discipline**: Spec drafter assume `migrations/006_schema_v5_*` 可用 ← reality 是 M5 已占 006 = v4.2。Same class as Spec #1 R1-C3 state_machine.py + Spec #2 R1 title column。Pattern: spec drafter 必须 `ls migrations/` + `head -1 schema_migrate.py 看 _LATEST_VERSION` 后再写 slot/version。
- **R5 — Gate logic 跨 Spec consume 必须 byte-exact validate against canonical SoT**: Spec #3 T-B0.10 写 `merge-base --is-ancestor FEATURE MASTER` claiming "forward (safe to bump)", 实际 dev-claude2 SoT 标 same args = REGRESSION。combined-mode R2 catch only via cross-Spec ref。

### Multi-terminal coordination

- **R6 — Submodule pointer regression-guard 必须 every commit pre-stage check**: 本 session 2 次 dev-claude2 rebase 期间各 1 次 stale aria-orchestrator pointer 几乎 leak (`0ce52b9` vs `1c23407`)。`git ls-tree HEAD aria-orchestrator` + `git submodule update --init aria-orchestrator` 是 mandatory neutralize sequence。
- **R7 — Stash + stash-pop 期间漏 staged file**: PRD patches 在 `git stash` 后 `git stash pop` 重新 unstaged, 而 commit message claim 它们 included → audit trail lie (e884e62)。Mitigation: stash 后 verify staging area 是否完整。
- **R8 — `git commit` 异常退出留 index.lock**: 本 session 1 次撞 `.git/index.lock: File exists`。Recovery: `rm -f .git/index.lock`。

### Spec drafting

- **R9 — Combined-mode sister-Spec wall-clock 4×非线性**: 估 ~1.5× (2 Specs × ~0.75 normalize) 实际 ~4× (3h vs Spec #1 45min)。原因: R2 split 触发 R3, finding count 翻倍 + cross-Spec cleanup overhead。Plan budget accordingly。
- **R10 — `[[feedback_paper_fix_antipattern]]` cross-spec 同形**: paper-fix 不仅 audit fix 出现, R1 partial-fix (e.g., 4 sites 写新, 4 sites stale) 也是 paper-fix antipattern。Substance-level audit catch (tl-critic R2 paper-fix C-tl-#3-1)。

---

## §4 实战教训 (本 session)

### Audit methodology (跨 cycle 验证)

- **Combined-mode sister-Spec audit 是 Lab-wide 质量飞跃** — M6 实证: 5 X-Critical R1 + 1 X-Critical R2 全部仅 cross-Spec verification caught; single-Spec dispatch 100% 漏。Lab convention candidate (memory promoted)
- **R3 forcing function 节省 ~2 round wall-clock 双实证** — Spec #1 R3 forcing function (M6 brainstorm Track F) + Spec #1/#2/#3 audit R3 stability (本 session) 都验证: scope-limited 1-agent vs full re-audit 比例 6:1
- **1/N NEEDS_FIX rule** — 通过 R2 tl-critic 3-for-3 right (我方独立 verify confirmed) 验证 `[[feedback_cross_agent_verdict_independent_verify]]` 不仅 R3 同 agent 跨轮, 也 R2 跨 agent 适用。Memory update candidate
- **Live-grep verify draft-time assumptions** — 3 次重复同型错误 (Spec #1 state_machine.py + Spec #2 Mech-B title + Spec #2 migration 006) 提示 Lab-wide discipline 缺失。新 memory candidate: spec drafter 必跑 mechanical check before write assumption

### PRD patch trajectory

- **PRD 在 spec drafting 期间动态 patch 是正常 catch-up 非反模式** — 本 session 4 patches (Q-final-1/2 from brainstorm + Q3 §568 + Q4 §656 from R1 audit)。Spec drafter contact reality 比 PRD writer 紧密。
- **PRD patch line number drift 必须 grep verify 跨 patches** — 多次 patch 后线号偏移, R1 audit C-cr-3 + T3-4 都因此。Spec body 必须使用 §section name + post-patch line, 不能 fix line numbers。

### Multi-terminal coordination 成熟度

- **Layer L Phase B 设计目标 100% 达标** — 6 dev-claude2 commits + 7 我方 commits 跨终端 ~6h 全 fast-forward 零冲突。submodule pointer regression-guard pattern 抓住 2 次 stale 已存盘 `[[project_submodule_drift_direction]]`
- **Cross-Spec SoT validation 是新涌现协调模式** — Spec #3 T-B0.10 R2-fix 直接参考 dev-claude2 Approved Spec lines 86-87 校对 args order。两终端独立 Spec 互为 cross-validation source = 协调 + 质量 双赢
- **Stash + pop staging hazard** — 1 次 PRD patches 在 stash 漏 staged 导致 commit message 虚假声称。Discipline: stash 后 `git status` verify pre-commit

### Spec drafting (sister-Spec 模式)

- **Sister-Spec 并行 drafting wall-clock 估算修正** — 本 session 实测 ~3h (Phase A.1 ~10min draft + Phase A.2 ~2.5h audit-fix-audit-fix-audit) 远超线性 2× Spec #1 (45min)。R2 split + R3 stability 复合成本。Future plan should budget 4× single-Spec for sister-Spec mode。
- **Spec #1 lessons 传染 Spec #2/#3 drafter** — REPO_ROOT canonical pattern, schema column SoT, exit code 0/1/2, fix-trail comment pattern 全部 Spec #2/#3 agents 主动应用 (因 R1 audit explicit prompt 提示)。但仍 R1 found ~25 raw Critical — drafter context limit。
- **Phase A precision items P-N 2-pass 自动化 candidate** — 每次 Spec 都人工 thread P-N 到 §What body + tasks.md, 但容易漏 → 1 Important 报警 (Diff 3 Layer 1 "Hermes+GLM" → "Hermes + Luxeno-routed GLM" 单点修)。Drafter Skill 可能加 propagation lint。

---

## §5 多维度同步状态

| 维度 | 状态 |
|------|------|
| **UPM** | N/A — Aria 主仓不使用 UPM |
| **User Story** | US-026 Phase A.1+A.2 (3/4 sub-Specs Approved); Spec #4 release-closeout 待 next session |
| **OpenSpec** | 3 active changes (M6 Spec #1/#2/#3 all Approved Draft folder) + dev-claude2's aria-submodule-pointer-regression-gate Approved; 0 待 archive (Phase D not yet for M6); M0-M5 全 archived (M5 last 2026-05-23) |
| **PRD** | `prd-aria-v2.md` 4 patches landed: §M6 timeline (a786444) + §628-639 cost gate (a786444) + §568 layer-boundary (e884e62/8a5fdc4 真) + §656 mean→median (e884e62/8a5fdc4 真) |
| **DEC** | DEC-20260524-001 (M6 brainstorm, +AD-M6-* allocation memo 8a5fdc4) + DEC-20260524-002 (Aria #124, dev-claude2 13035d8) |
| **Standards** | 1 small commit (`6fcce24` anchor typo) bumped to 主仓 e54ace7 |
| **aria-orchestrator** | dev-claude2 ship Track E follow-ups #16+#17 (`0ce52b9` bumped) |
| **aria-plugin** | v1.27.0 stable (no change本 session); v1.29.0 block-mode gate dev-claude2 Spec Approved Phase A, Phase B 待 |
| **Memory** | 3 entries written this closeout (combined-mode + slot-draft-verify + gate-SoT-validate); MEMORY.md index update (~25KB now estimated) |
| **Handoff (Rule #9)** | Predecessor Track F + sister Track E + 本 Track G ✓; latest.md pointer update |
| **Production** | aria-layer2-runner stable (Track E 2026-05-23 deploy), aria-orchestrator alloc stable, cron-daily 待启 (Spec #1 Phase B precondition) |
| **Forgejo Issues** | 3 still open (Track E carry: aria-orch #16/#17 dev-claude2 已 close; Aria main #124 dev-claude2 Spec implementing); 0 created本 session |
| **Multi-remote parity** | 主 Aria HEAD `413dd75` 3-way verified ✓ |
| **Multi-track coordination** | 同日 5+ tracks 跨 2 dev-claude container ship + integrate 全 zero conflict (Layer L Phase B 大规模 stress test 通过) |

---

## §6 Next session 入口 + 优先级

```bash
/aria:state-scanner   # 看板会 surface 本 Track G handoff + 推荐 Spec #4 Phase A.1
```

**推荐优先级**:

1. **Spec #4 `aria-2.0-m6-release-closeout` Phase A.1** — ~10h Level 2 tech-lead agent, draft + 单 Spec audit cycle (估 ~1-1.5h wall-clock total)
2. **Spec #1 Phase B.1 starter** — 启动 branch creation + cron-daily 让 3-day data 累积 (Spec #2 precondition)
3. **Spec #3 TG-DOCS-A v2.0.0-blocker Phase B.1** — CLAUDE.md v2.0 + README badge + Release notes, independent of #1/#2
4. **Owner: pricing rotation ritual** (Q3 carry-forward) — Zhipu CNY→USD review, ~30min

**不应该做的**:
- ❌ 不要跳过 Spec #4 直接 Phase D (release-closeout 是 Phase D gate provider; 跳过 = 无 RED/ABORT pre-release gate)
- ❌ 不要在 Spec #1 AC-7 (3-day data) 未 PASS 时启 Spec #2 Phase B (会撞 stale data error)
- ❌ 不要 cherry-pick TG-DOCS-B 优先 vs TG-DOCS-A (按 Spec #3 sequencing, A is v2.0.0 blocker, B is v2.0.1-deferrable)

---

## §7 提交清单 (Phase 收尾 closing commit, 待 push)

主仓 (1 closing commit):
- `?? docs/handoff/2026-05-24-m6-phase-a-spec-batch-approved.md` (本 doc)
- `M docs/handoff/latest.md` (pointer update Track G)
- `M /home/dev/.claude/projects/-home-dev-Aria/memory/MEMORY.md` (index +3 entries — local file, NOT in git)
- `?? feedback_combined_mode_sister_spec_audit_value.md` (local memory)
- `?? feedback_schema_migration_slot_draft_time_verify.md` (local memory)
- `?? feedback_gate_logic_cross_spec_sot_validate.md` (local memory)

注: memory 文件在 `~/.claude/projects/.../memory/` 是 local-state, **不进 git commit**。只 commit handoff doc + latest.md pointer。

**双推**: origin + github, 3-way SHA parity verify post-push。

---

## §8 Memory entries this session

### Track G (本 closeout, ~16:30 UTC 写)

- 🆕 [`feedback_combined_mode_sister_spec_audit_value`](../../.claude/projects/-home-dev-Aria/memory/feedback_combined_mode_sister_spec_audit_value.md) — Combined-mode sister-Spec audit catches X-Critical that single-Spec misses; M6 实证 5 X-Critical R1 + 1 X-Critical R2; Lab convention for ≥2 sister-Specs
- 🆕 [`feedback_schema_migration_slot_draft_time_verify`](../../.claude/projects/-home-dev-Aria/memory/feedback_schema_migration_slot_draft_time_verify.md) — Spec drafter MUST live-grep `ls migrations/` + check `_LATEST_VERSION` BEFORE writing slot N; same class as state_machine.py / title column / 006-collision 三连发
- 🆕 [`feedback_gate_logic_cross_spec_sot_validate`](../../.claude/projects/-home-dev-Aria/memory/feedback_gate_logic_cross_spec_sot_validate.md) — Spec consuming another's gate primitive MUST byte-exact verify args/semantic against canonical SoT; M6 Spec #3 T-B0.10 vs dev-claude2 #124 Spec line 86-87 实证

MEMORY.md 索引 +3 行 update (Track G new entries), estimated total ~25KB / 24.4KB limit (需 review pruning 时机近)。

**Q-audit (收尾, 答 owner 4 问题)**:

- **Q1 未完成 task?** AI-runnable: Spec #4 Phase A.1 (`~1h next session first`) + Spec #1 Phase B.1 (gated on owner availability)。Owner-action: pricing rotation ritual + Phase B start order decision。全 §2 documented。
- **Q2 未固化经验?** 3 new memory entries (combined-mode value / slot-draft-verify / gate-SoT-validate)。§3/§4 prose 总结。`[[feedback_cross_agent_verdict_independent_verify]]` candidate update (R2 cross-agent variant 验证) 留 next session 写时合并。无遗漏。
- **Q3 UPM/US/Spec/PRD 同步?** UPM N/A; US-026 Phase A.1+A.2 done 3/4; Spec #1/#2/#3 Approved + Spec #4 待 next session; PRD 4 patches landed。**唯一缺口** = Spec #4 + Phase B.1 (next session)。
- **Q4 收尾交接?** 本 doc + 3 new memories + MEMORY.md index + latest.md pointer + closing commit。完整。

---

## Cross-references

- **Predecessor Track F handoff**: [`2026-05-24-m6-brainstorm-converged-track-f.md`](./2026-05-24-m6-brainstorm-converged-track-f.md)
- **Sister Track E follow-ups (dev-claude2 ship)**: [`2026-05-24-track-e-followups-17-16-done.md`](./2026-05-24-track-e-followups-17-16-done.md)
- **DEC M6 brainstorm**: [`.aria/decisions/2026-05-24-us026-m6b-brainstorm.md`](../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (+AD memo)
- **DEC Aria #124 regression-gate**: [`.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md`](../../.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md)
- **Spec #1 (Approved)**: [`openspec/changes/aria-2.0-m6-cost-acceptance/`](../../openspec/changes/aria-2.0-m6-cost-acceptance/) (c29a800)
- **Spec #2 (Approved)**: [`openspec/changes/aria-2.0-m6-e2e-resilience/`](../../openspec/changes/aria-2.0-m6-e2e-resilience/) (413dd75)
- **Spec #3 (Approved)**: [`openspec/changes/aria-2.0-m6-docs/`](../../openspec/changes/aria-2.0-m6-docs/) (413dd75)
- **dev-claude2 Aria #124 Spec (Approved cross-ref)**: [`openspec/changes/aria-submodule-pointer-regression-gate/`](../../openspec/changes/aria-submodule-pointer-regression-gate/) (1a06bbd)
- **16 audit reports**: [`.aria/audit-reports/post_spec-R*-*-2026-05-24-aria-2.0-m6-*`](../../.aria/audit-reports/)
- **PRD post-patch**: [`docs/requirements/prd-aria-v2.md`](../requirements/prd-aria-v2.md) 4 patches §M6 timeline / §628-639 / §568 / §656
- **US-026 spec**: [`docs/requirements/user-stories/US-026.md`](../requirements/user-stories/US-026.md)

---

**Created**: 2026-05-24 ~16:30 UTC
**Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7 (1M context)
**Status**: Track G CLOSED — M6 Phase A.1+A.2 done 3/4 sub-Specs Approved; Spec #4 release-closeout deferred to next session
**Next entry**: `/aria:state-scanner` 看板 surface 本 doc + 推荐 Spec #4 Phase A.1 (tech-lead agent, ~1-1.5h cycle)
