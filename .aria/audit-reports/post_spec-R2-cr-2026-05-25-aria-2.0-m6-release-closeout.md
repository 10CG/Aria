# Phase A.2 R2 audit — code-reviewer — aria-2.0-m6-release-closeout

> **R1-fix commit**: `cdd2e5e`
> **Audit date**: 2026-05-25
> **Agent**: aria:code-reviewer (Opus 4.7 sub-agent, R2 challenge round)
> **Audit perspective**: byte-exact compliance verification + self-trap detection + cross-Spec consistency

## Verdict
**NEEDS_FIX_R2**

0 NEW Critical, 2 NEW Important (self-trap propagation + AD lock vs reality gap), 3 NEW Minor. R1 5C closed 5/5 (100%). R1 7I closed 6/7 (86%). R1 10N closed 9/10 (90%). Reduction: (22-5)/22 = **77%** (passes 70% threshold).

## R1 finding closure

### Critical (5/5 CLOSED)
| ID | Status | Evidence |
|----|--------|----------|
| C-cr-1 | CLOSED | aria/VERSION regex byte-exact verified `re.search` against `> **版本**: 1.27.0` → matches |
| C-cr-2 | CLOSED | aria/README.md regex verified against `> **Version**: 1.27.0 \| ...` → matches |
| C-cr-3 | CLOSED | T-A1.4 reconciles main /VERSION row v1.23.1 → SoT before Phase B G-7 |
| C-cr-4 | CLOSED (with I-NEW-r2-1 residual) | Per-flag canonical primary throughout body + Assumptions + tasks; 2 residual --all literals in §Dependencies + Risk-mit |
| C-cr-5 | CLOSED | All 3 submodules enumerated; in-tree special case removed |

### Important (6/7 CLOSED + 1 PARTIAL)
| ID | Status |
|----|--------|
| I-cr-1 | CLOSED — memory candidates correctly relocated |
| I-cr-2 | CLOSED — §J 36-line substantive delegation explanation |
| I-cr-3 | CLOSED — RED-is-expected-v2.0.0 + loose heading regex |
| I-cr-4 | CLOSED (with N-NEW-r2-2 residual) — "6 surfaces" in body but 4 residual "5-files" literals |
| I-cr-5 | CLOSED — §H Step 7 symmetric recommendation |
| I-cr-6 | PARTIAL — orchestrator dry-run clear, archive runner dry-run polarity needs AC-1 mention |
| I-cr-7 | CLOSED (passing) |

### Minor (9/10 CLOSED + 1 PARTIAL)
| ID | Status |
|----|--------|
| N-cr-1..9 | CLOSED |
| N-cr-10 | PARTIAL — `<R1-FIX-COMMIT-PENDING>` placeholder not replaced post-commit |

## NEW findings (R2 independent scan)

### NEW Important (2)

| ID | Location | Issue |
|----|----------|-------|
| **I-NEW-r2-1** | proposal.md:629/630 + tasks.md:399/400 | Self-trap antipattern per `[[feedback_doc_self_trap_pattern]]`: §Dependencies + Risk-mit checklist still say `--all` while body says per-flag canonical. Implementer reading these first builds wrong primary path. |
| **I-NEW-r2-2** | proposal.md:417 AD-M6-10 vs §H step 5 + T-A2.1 sys.exit(20) + T-A4.5 | AD-M6-10 lock says "exit 0/1/2" + AC-1 says "No other exit codes" — but R1-fix introduced exit 3 + exit 20. AD-M6-10 not amended; AC-1 factually false. |

### NEW Minor (3)

| ID | Issue |
|----|-------|
| N-NEW-r2-1 | AC-9 heading "Owner override env var" (stale; mechanism is CLI flag) |
| N-NEW-r2-2 | 4 residual "5-files" literals (proposal:31/392/591 + tasks:342) contradict "6 surfaces" body |
| N-NEW-r2-3 | `<R1-FIX-COMMIT-PENDING>` placeholder in Audit trajectory line 17 |

## Cross-Spec byte-exact verification

| Check | Result |
|-------|--------|
| Spec #1 sibling: 4 individual flags only, no --all | ✅ grep verified |
| Spec #2 sibling: 3 --tg-* flags only, no --all | ✅ grep verified |
| Spec #3 §A.5 line 160 cross-ref | ✅ verbatim match |
| .gitmodules 3 submodules | ✅ confirmed |
| Memory entries cited as existing | ✅ all 17 entries verified post I-cr-1 cleanup |
| phase-d-closer + openspec-archive Skills exist | ✅ both present |

## Self-Q-escalation check
No paper-fix pattern detected EXCEPT the 2 NEW residuals (§Dependencies + Risk-mit `--all` literals are paper-fix surface vs the otherwise per-flag canonical body).

## Reduction metric
- R1 total: 22 findings (5C + 7I + 10N)
- Net residual after R2: 0 Critical, 2 Important (NEW), 5 Minor (3 NEW + 2 partial)
- Reduction: 77%

## Collapse recommendation

**Do NOT collapse R3 by default** — 1 NEW Important (I-NEW-r2-1) is a self-trap contradiction violating `[[feedback_gate_logic_cross_spec_sot_validate]]` byte-exactness; 1 NEW Important (I-NEW-r2-2) is a lock-vs-reality gap that propagates downstream (Phase B implementer would code wrong exit codes).

Per `[[feedback_3round_early_convergence]]`: pre_merge 3-round permissible if R2 fix <100 lines + 0 logic change. Both new Important are paper-fixable (~5 line edits + 1 paragraph). After R2-fix, R3 stability check (1-agent scope-limited) verifies fixes didn't introduce new criticals.

Recommend: apply R2-fix → R3 stability → Approved.
