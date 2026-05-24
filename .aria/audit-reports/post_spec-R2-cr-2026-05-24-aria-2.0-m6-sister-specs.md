# Post_Spec R2 Audit (challenge, combined) — code-reviewer — Spec #2 + #3

> **Auditor**: code-reviewer
> **Round**: R2 challenge combined
> **Spec status**: Draft post-R1-fix (commit 8a5fdc4)
> **R1 baseline**: 11 unified themes (10 Critical + 5 X-Critical cluster + 13 Important)
> **Vote**: **SCOPE_OK_R2**
> **Per-Spec verdict**: Spec #2 = **PASS**, Spec #3 = **PASS**

## Summary

Both Specs converged cleanly at commit `8a5fdc4`. **23/23 R1 findings CLOSED** (10 Critical Spec #2/#3 themes + 5 X-Critical themes + 13 Important themes), 0 PARTIAL, 0 PAPER, 0 REGRESSION. R1-fix introduced one new well-formed AD slot (AD-M6-4b for pre-flight routing strategy) cleanly grafted onto AD-M6-4..AD-M6-6 allocation without renumbering. Inline `<!-- R1-<ID> fix: ... -->` traces consistently applied at every edit site per `[[feedback_audit_driven_fix_conventions]]`. PRD §568 + §656 catch-up patches (commit `e884e62`) verified live and cross-referenced from both Specs. DEC-20260524-002 referenced in Spec #3 T-B0.10 v1.29.0 gate per X-T2 owner Q5 pre-decision. **0 NEW_CRITICAL** findings; only 2 minor observations (non-blocking). Recommend Phase A.3 agent allocation.

## R1 closure matrix (combined)

| R1 ID | Status | Evidence | Note |
|-------|--------|----------|------|
| **T2-1 SQL columns** | CLOSED | Spec #2 proposal:106-149 (SQL rewrite using `state='S9_CLOSE'`, `state_entered_at`, `json_extract(dispatch_audit_log.payload_json)`); proposal:748-805 AC-2 evidence block; tasks:198-300 TG-A-dispatch tasks; Dependencies table 1036-1039 column list corrected | Schema verified live `schema.sql:35-239` — `state` (line 66), `state_entered_at` (line 67), `provider_cost_model` (line 137) present; `title`/`final_state`/`issue_type`/`created_at`/`project_name` confirmed ABSENT |
| **T2-2 state_machine.py path** | CLOSED | Spec #2 proposal:393-414 (4-module distribution lock); 409-415 (4-module cov target); 836-858 AC-4 evidence with 4-module `--cov` flag; 685 AD-M6-6 4-module note; tasks:609-693 B-sm-* tasks all use 4-module list | Remaining `state_machine.py` references all in NEGATIVE context ("does NOT exist", "will NOT be created", "no state_machine.py") — Q1 lock applied consistently |
| **T2-3 AC-6 Luxeno=0** | CLOSED | Spec #2 proposal:895-944 AC-6 rewrite with non-null guard (line 921) + bounded zeros (line 930-933) + AD-M6-4b new slot (902-908); proposal:683-685 AD allocation extended | New AD-M6-4b cleanly inserted; old Luxeno=0 trap eliminated; `assert all(c <= 2.0)` retained as hard cap but with structural guards |
| **T2-4 is_synthetic Mech B** | CLOSED | Spec #2 proposal:152-172 (Mech A LOCKED, Mech B removal note); 608-617 (migration 006); 683 AD-M6-4 LOCKED; tasks:50-99 TG-A-infra; T-validate-schema-1 (tasks:56-78) | Migration renamed 005→006 (avoids collision with Spec X migration 005); targets schema v5.0 with explicit `schema_meta` bump per `[[feedback_schema_migration_to_version_bump]]` |
| **T2-5 AC-1 CreateTime** | CLOSED | Spec #2 proposal:73-102 (alloc.CreateTime persisted as anchor); 706-744 AC-1 evidence with alloc_id identity check + CreateTime computation; tasks:112-192 A-uptime-1..5 with alloc_id mismatch FAIL fixture | StartedAt removed; `m6-7d-day-1-alloc-anchor.json` introduced as canonical Day-1 anchor |
| **T2-6 AC-2 check order** | CLOSED | Spec #2 proposal:763-785 (STEP 1 total>=10 FIRST, STEP 2 cap guarded `if total_s9 > 0 else 0.0`); tasks:205-258 A-dispatch-1..4 with explicit total=0 FAIL fixture (not ZeroDivisionError) | Check order now correctly enforces "assert count BEFORE division" pattern |
| **T3-1 CLAUDE.md 9 diffs** | CLOSED | Spec #3 proposal:48-101 (9-diff enumeration anchored to live CLAUDE.md line ranges); proposal:52-61 (live section map: 1-5/9-18/21-37/40-76/120-188/208-228/343-426/429-453); Diff 6 reframed to "Rules #1-#9 ALL FROZEN" with AC-1 git-diff check; Diff 9 incremental noted | Verified live `CLAUDE.md` against Spec map: §不可協商規則 line 343 ✓, §项目状态 line 429 ✓, plugin version v1.22.0 line 434 ✓ (Diff 9 target confirmed stale per design). Minor: line numbers ~off-by-1-2 (e.g. spec says "line ~66" for Diff 3 anchor; live shows §核心概念 at line 40 with §十步循环 inside that block). Anchors are by section header not literal line so this is acceptable |
| **T3-2 Probe 1 regex** | CLOSED | Spec #3 proposal:166-188 (anchored regex `'badge[^\d]*v?\K[0-9]+\.[0-9]+\.[0-9]+'`); PASS/FAIL fixtures (lines 186-188) | `head -1` removed; explicit task dependency on T-A2.1 noted (Probe 1 expected to FAIL before T-A2.1 README badge update — correct semantics) |
| **T3-3 Plugin version SoT** | CLOSED | Spec #3 proposal:91-99 (dynamic plugin.json read instruction); proposal:478-485 AC-3 with `PLUGIN_VER=$(python3 ... plugin.json ...)` dynamic resolution; tasks:72 T-A2.1 explicit "do not hardcode" | plugin.json verified live = v1.27.0; AC-3 evidence reads SoT dynamically not hardcoded |
| **T3-4 PRD line citations** | CLOSED | Spec #2 proposal:7 (cites §638-646); 50, 54 (§656 rubric); 1064-1066 PRD references with post-patch line numbers; Spec #3 proposal:672-674 (§567-568, §639, §656 all post-patch) | PRD live verification: §568 = `aria-orchestrator/docs/` ✓ (T3-5 closure), §656 = "median ≥ 7/10" ✓ (X-T3 closure); citations resolved post `a786444` + `e884e62` |
| **T3-5 PRD §568 reference** | CLOSED | Spec #3 proposal:335-336 (post-patch `e884e62` PRD §568 cite); cross-ref note "PRD §568 post-patch text and Spec #3 §B.4 are now in alignment"; B.4 file at `aria-orchestrator/docs/layer-boundary-contract.md` confirmed | PRD live verification: §567-568 reads `aria-orchestrator/docs/ (Aria-specific 内部契约,非 Lab-shareable; per km M-km-R2-005 brainstorm 决策 + Spec #3 R1-audit-Q3 lock 2026-05-24)` ✓ |
| **X-T1 BOTH-locations path** | CLOSED | grep across both Specs for `aria-orch/` (excluding `aria-orchestrator`): **0 hits outside fix-trail comments**; all functional references use full `aria-orchestrator/evals/m6-prompt-quality/` | Spec #3 tasks:271,295,315,316 all use full `aria-orchestrator/evals/m6-prompt-quality/`; AC-6 grep at proposal:532 verified |
| **X-T2 T-B0.10 v1.29.0 gate** | CLOSED | Spec #3 tasks:191-211 (T-B0.10 precondition block with `git -C standards fetch origin master` + `merge-base --is-ancestor`); proposal:668 cross-ref to DEC-20260524-002 file; DEC file existence confirmed | DEC-20260524-002 (`.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md`) exists; effort baseline updated to ~33h impl (+0.1h T-B0.10) frontmatter line 10 |
| **X-T3 mean→median** | CLOSED | Spec #2 proposal:519, 523, 860, 874-876, 968 (all median); Spec #3 proposal:303, 311, 326, 674 (all median); PRD §656 live = "median ≥ 7/10" ✓ | Zero residual "mean"/"平均" references outside fix-trail comments (verified via grep); PRD post-patch e884e62 lands the median lock |
| **X-T4 AD-M5-11 → AD-M6-9** | CLOSED | Spec #3 proposal:12 frontmatter (AD-M6-9 reserved, AD-M5-11 vacated); proposal:439 AD-M6-9 in §How table; proposal:574-588 AC-10 verifies AD-M6-9; tasks:8 frontmatter; tasks:394-428 T-B6 fully renamed | Bilateral guard: Spec #3 BOTH "claim AD-M6-9" AND "DO NOT overwrite AD-M5-11" (which stays as M5-spillover reservation). Clean separation |
| **X-T5 rubric 7 dimensions** | CLOSED | Spec #2 proposal:507-517 (D1-D7 table); Spec #3 proposal:313-330 (D1-D7 table identical); Spec #3 tasks:296-305 T-B3.2.3 lists D1-D7; AC-6 structural check at proposal:534-535 (`grep -c "^### Pattern" >= 10`) replaces fragile `wc -l >= 200` | Cross-Spec rubric identity verified D1-D7 word-for-word; structural check replaces line-count proxy |
| **I2-1 Day-3 gate 3-conditions** | CLOSED | Spec #2 proposal:726-741 (4 grep checks for 3 conditions + verdict); tasks:188-192 A-uptime-5 unit test |
| **I2-2 WAL-D outcome** | CLOSED | Spec #2 proposal:375-389 (WAL-D = NO S_FAIL, auto-recreate, separate log event); tasks:488-502 B-infra-3 WAL-D fixture comment |
| **I2-3 LLM-4 provider split** | CLOSED | Spec #2 tasks:408-409 (2 LLM-4 test files: luxeno_429 + zhipu_429); proposal:340-346 mock-shape table per-provider |
| **I2-4 LLM-5/6 httpx_mock split** | CLOSED | Spec #2 tasks:410-413 (4 test files: llm5_luxeno/zhipu + llm6_luxeno/zhipu); proposal:341-346 |
| **I2-5 llm_client.complete()** | CLOSED | Spec #2 proposal:323-328 + tasks:537-539, 613-615 (mock targets updated to `silknode_client.call_llm`/`zhipu_client.call_llm`/`provider_router.call_llm`) |
| **I2-6 Exception class names** | CLOSED | Spec #2 proposal:329-336 + tasks:540-542 (`_LLMHTTPError`/`ZhipuHTTPError`/`LLMRouteExhausted` replace fictitious `RateLimitError`/`ProviderUnavailableError`) |
| **I2-7 --cov-fail-under in pyproject.toml** | CLOSED | Spec #2 proposal:666-668 (note); tasks:686-692 B-sm-4 declares `[tool.pytest.ini_options] addopts = "--cov-fail-under=100"` |
| **I2-8 AC-7 non-mutation contract** | CLOSED | Spec #2 proposal:285-294 (explicit non-mutation contract: Spec #2 only invokes + tests `validate-m6-handoff.py`; mods require Spec #1 patch) |
| **I3-1 Rule body freeze** | CLOSED | Spec #3 proposal:81-82 (extended freeze to Rules #1-#9); 461 AC-1 git-diff check `grep "Rule #[1-6]"`; tasks:39 T-A1.6 AD11 verification block |
| **I3-2 AC-4 grep -c → per-name** | CLOSED | Spec #3 proposal:489-507 AC-4 (per-probe `grep -qF "name: \"${probe}\""` loop + Python YAML check as authoritative gate); tasks:146-157 same pattern |
| **I3-3 date -d → python3** | CLOSED | Spec #3 proposal:217-231 Probe 3 (python3 datetime.fromisoformat + timedelta); tasks:141 T-A6.3 cross-platform note |
| **I3-4 Hermes + GLM → Luxeno-routed** | CLOSED | Spec #3 proposal:70 (Diff 3 Layer 1 = "Hermes + Luxeno-routed GLM models"); tasks:36 T-A1.3 explicit phrasing |
| **I3-5 AC-3 hardcode** | CLOSED | (Same as T3-3 above) — Spec #3 proposal:478-485 + tasks:72 |

**Total: 23 CLOSED / 0 PARTIAL / 0 PAPER / 0 REGRESSION**

## New findings (R2-introduced; should be 0 for SCOPE_OK_R2)

### Critical

*(none — vote precondition satisfied)*

### Important

*(none — all R1-fix-pass edits are coherent and inline-traced)*

### Minor / Observations

- **M-R2-1 (Spec #3 minor)**: Live CLAUDE.md section line-number drift vs. Spec #3 §A.1 enumeration. Spec #3 proposal:52-61 declares "Lines 1-5: Header block / Lines 21-37: 项目定位 / Lines 40-76: 核心概念 / Lines 343-426: 不可协商规则 / Lines 429-453: 项目状态". Live grep confirms §不可協商規則 at line 343 ✓, §项目状态 at 429 ✓, but §核心概念 at line 40 (Spec says 40-76 inclusive — first §subsection §十步循环 inside that block at ~line 50, not 66 as comment in T-A1.3 says "live CLAUDE.md ~line 66"). The "~line 66" is approximate and Diff 3 is anchored to §十步循环 header not the literal line — Phase B implementer should re-grep at edit time. Non-blocking (anchors are by header not line literal).

- **M-R2-2 (Spec #2 minor / observation, not new — surfaces R1-baseline edge)**: Effort baseline arithmetic per R1 cr-I4 said midpoints summed to 27.5h vs frontmatter 29h. R1-fix bumped frontmatter to ~29h impl + 1h R1-fix delta (T-validate-schema-1 + AD-M6-4b) → ~30h. Spec #2 frontmatter line 11 still reads "~29h impl" while §Effort baseline body line 1015 reads "~29-30h ≈ 30h" and tasks frontmatter line 7 reads "~30h impl". Three-way reconciliation: 29 vs 29-30 vs 30. Pedantically inconsistent but within rounding tolerance for a Spec at Draft → Approved transition. Recommend Phase A.3 implementer or owner adopts single value "~30h" at Approved time. Non-blocking.

## Vote rationale

**SCOPE_OK_R2 satisfies all 3 preconditions**:

1. **≥70% R1 reduction**: 23/23 R1 themes CLOSED = **100% reduction** (far exceeds 70%).

2. **0 NEW_CRITICAL**: Two minor observations (M-R2-1 line-number drift, M-R2-2 effort baseline three-way pedantic gap) are both Phase B / Approved-time housekeeping items, not Critical defects. No new bugs surfaced.

3. **All R1 Critical CLOSED (not PARTIAL/PAPER/REGRESSION)**: Each of the 16 Critical themes (10 Spec #2/#3 + 5 X-Critical + 1 from R1 cr-private C4 reframed into T3-3) has substantive content fix mapped to specific line ranges with inline `<!-- R1-<ID> fix: ... -->` audit-trail comments. Ground-truth probes confirmed:
   - Live schema.sql columns match T2-1 rewrites (no `final_state`/`title`/`issue_type`/`created_at`/`project_name`; `state` + `state_entered_at` + `provider_cost_model` present).
   - Live CLAUDE.md has 9 Rules at expected sections (T3-1 enumeration matches structural anchors).
   - Live plugin.json reads v1.27.0 dynamically (T3-3 SoT verified).
   - Live PRD §568 = `aria-orchestrator/docs/` post `e884e62` (T3-5 verified).
   - Live PRD §656 = "median ≥ 7/10" post `e884e62` (X-T3 verified).
   - DEC-20260524-002 file exists and is cross-referenced from Spec #3 T-B0.10 (X-T2 verified).
   - grep across both Specs for residual `aria-orch/` shorthand: 0 functional hits (X-T1 verified).
   - grep for residual AD-M5-11 claims in Spec #3: only in "vacated" / "do not overwrite" guard contexts (X-T4 verified).
   - grep for residual `state_machine.py` references in Spec #2: only in negative ("does NOT exist") contexts (T2-2 verified).

**Combined-mode value reconfirmed**: R1 aggregate flagged that single-Spec dispatch would have missed all 5 X-Critical findings. R2 combined verification efficiently confirms cross-Spec consistency at the rubric-7-dimension level (X-T5), median-metric level (X-T3), path-notation level (X-T1), and AD-allocation level (X-T4) in a single pass — same methodology pays dividend again.

**Recommendation**: Advance both Specs to **Phase A.3 (agent allocation)**. Per Spec #1 precedent (R2 SCOPE_OK_R2 4/4 in M5), R3 stability round is OPTIONAL when R2 reduction is ≥90% and 0 NEW_CRITICAL. Owner may collapse R3+R4 per `[[feedback_audit_collapse_r3_r4_when_r2_clean]]` decision pattern, OR run a 1-agent stability spot-check (≤5 min) for the line-number drift in Spec #3 §A.1 if extra rigor desired. Either path → A.3.

---

**Audit completed**: 2026-05-24
**Reviewer**: code-reviewer (R2 challenge, combined sister-Spec mode)
**Time budget consumed**: ~17min (within 15-20 min allowance)
**Next**: Aggregate with ai-engineer + tech-lead-critic R2 reports → R2 aggregate verdict → Phase A.3 if 3/3 SCOPE_OK_R2
