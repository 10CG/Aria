# Smoke Evidence — aria-secret-guard-plugin-default

> **Spec**: `openspec/changes/aria-secret-guard-plugin-default`
> **Ship target**: aria-plugin v1.24.0
> **Verdict**: **REVIEW → PASS_TRIAGED** (2 findings triaged by owner 2026-05-23, both Accept-with-doc, see §3.1)
> **Mode**: Aria self = P1; SilkNode = P2.5 deferred 7-day post-ship

---

## §1 Aria self dogfood (TASK-007)

**Captured**: 2026-05-23T07:12:29Z
**Environment**: Aria worktree `feature/aria-secret-guard-plugin-default` at SHA eac9630;
                 hook invoked directly via `bash aria/hooks/secret-guard.sh` (proxy for
                 production `bash ${CLAUDE_PLUGIN_ROOT}/hooks/secret-guard.sh`).

### Schema (per tasks.md §5.3)

```yaml
mode: dogfood_in_session
project: aria-self
captured_at: 2026-05-23T07:12:29Z
hook_sha256: f182ca437dccf5b57cf34bab0886dc5daeb9b9e26a108b4d7a0c723643f75c72  # secret-guard.sh
plugin_version: 1.24.0
events:
  pretooluse_10_daily: 10
  pretooluse_block_validation: 3
  posttooluse_scans: 3
counters:
  unexpected_false_positive: 0
  unexpected_false_negative: 0   # B3 reclassified as known_limit (see §2)
  known_limit_finding: 1         # cat <key-file> via Bash not in regex coverage
timing_pretooluse_10_daily_ms:
  n: 10
  min: 101
  max: 337
  p50: 305
  p95: 337
  all: [330, 316, 337, 295, 322, 300, 101, 102, 102, 305]
timing_block_validation_ms: [144, 104, 324]
timing_posttooluse_ms: [222, 174, 176]
performance_budget_ms: 100        # per proposal §Impact
performance_budget_met: false     # p95=337 > 100 — finding F1, see §2
```

### Event-by-event

#### PreToolUse (10 daily commands — representative Aria daily-use mix)

| # | Event | Tool | Elapsed | Want exit | Got exit | Verdict | Classification |
|---|-------|------|---------|-----------|----------|---------|----------------|
| 1 | `ls /home/dev/Aria` | Bash | 330 ms | 0 | 0 | OK | expected_allow |
| 2 | `git status` | Bash | 316 ms | 0 | 0 | OK | expected_allow |
| 3 | `cat README.md` | Bash | 337 ms | 0 | 0 | OK | expected_allow |
| 4 | `grep -rn TODO src/` | Bash | 295 ms | 0 | 0 | OK | expected_allow |
| 5 | `python3 -c print(2+2)` | Bash | 322 ms | 0 | 0 | OK | expected_allow |
| 6 | `forgejo GET /repos/10CG/Aria/pulls` | Bash | 300 ms | 0 | 0 | OK | expected_allow |
| 7 | Read `/home/dev/Aria/CLAUDE.md` | Read | 101 ms | 0 | 0 | OK | expected_allow |
| 8 | Read `proposal.md` | Read | 102 ms | 0 | 0 | OK | expected_allow |
| 9 | Edit `aria/skills/x/y.py` | Edit | 102 ms | 0 | 0 | OK | expected_allow |
| 10 | `make test` | Bash | 305 ms | 0 | 0 | OK | expected_allow |

Observation: **Bash tool calls (1-6, 10) clock 295-337 ms**; **Read/Edit calls (7-9) clock 101-102 ms** — distinct latency profiles per code path inside the hook.

#### PreToolUse (block-validation, validates hook actively rejects risky patterns)

| # | Event | Tool | Elapsed | Want exit | Got exit | Verdict | Classification |
|---|-------|------|---------|-----------|----------|---------|----------------|
| B1 | nomad-var-get (risky secret store read) | Bash | 144 ms | 2 | 2 | OK | expected_block |
| B2 | Read `/home/dev/proj/.env` | Read | 104 ms | 2 | 2 | OK | expected_block |
| B3 | Bash `cat ~/.ssh/id_rsa` | Bash | 324 ms | 2 | 0 | KNOWN-LIMIT | reclassified, see F2 |

#### PostToolUse (3 representative scans)

| # | Event | Tool | Elapsed | Behavior | Classification |
|---|-------|------|---------|----------|----------------|
| P1 | Clean Bash output ("hello world") | Bash | 222 ms | pass-through | expected_passthrough |
| P2 | Known-secret-shaped payload | Bash | 174 ms | REDACT applied to stdout | expected_redact |
| P3 | Read clean code line | Read | 176 ms | pass-through | expected_passthrough |

### Findings

#### F1 — Performance budget overshoot (p95 = 337 ms vs budget < 100 ms)

- **Severity**: Major (ship-gate concern, not regression)
- **Scope**: PreToolUse Bash matcher path; Read/Edit path is within budget (~100 ms)
- **Root cause** (decomposed via baseline measurement):
  - `bash -c true` startup: ~5 ms
  - `jq -n .` startup: ~55 ms
  - secret-guard.sh full warm invocation: ~300 ms (regex + jq pipeline work)
  - secret-guard.sh full COLD invocation: 600-1400 ms (filesystem/library load)
- **Why budget set at 100 ms**: Spec wrote "p95 hook overhead < 100 ms per tool event (single sub-shell launch + jq parse expected < 50 ms, 2× headroom)". This estimate **omitted the ~100-pattern regex sweep + multi-stage jq pipeline cost** that dominates the warm path.
- **Owner triage options**:
  - (a) **Accept** with budget revision: bump proposal Performance Budget to `p95 < 400 ms` (Bash path) / `p95 < 150 ms` (Read/Edit path); ship v1.24.0; track optimization as v1.25.x scope.
  - (b) **Accept + 48 h SLA v1.24.1**: ship v1.24.0; track v1.24.1 perf hotfix (compile regex to AWK / pre-flatten jq pipeline / move to single-pass POSIX shell) within 48 h.
  - (c) **Block**: pause ship until perf met (rewrite hook in compiled language or radically simplify regex).

#### F2 — Bash matcher false-negative for local `cat <key-file>` (NEW known-limitation)

- **Severity**: Minor (functional gap, NOT regression — never claimed coverage)
- **Scope**: Bash `cat ~/.ssh/id_rsa` / `head id_rsa` / `tail .pem` etc. NOT blocked when invoked as Bash command. **Read/Edit/Write/MultiEdit matcher DOES catch the same file_path** (line 153 of secret-guard.sh).
- **Root cause**: Bash command-pattern regex covers ~100 risky patterns (nomad/curl/cat .env/SSH wrappers/etc.) but does NOT include local `cat|head|tail|less|more <key-file>` for ssh keys / .pem / .key files. Only the **remote-ssh wrapper** (line 398) covers `ssh ... cat id_rsa`.
- **Workarounds available**:
  - User should invoke Read tool (caught by Read matcher) instead of Bash `cat` for inspecting key files
  - secret-scan.sh PostToolUse provides second-line defense (REDACT key-shaped output)
  - `# guard:ack: <reason>` bypass for legitimate one-off ack'd reads
- **Owner triage options**:
  - (a) **Accept** as new known-limitation: add to v1.24.0 CHANGELOG known-limitations list; track v1.25.x as roadmap item; defer regex addition until empirical incidence accumulates.
  - (b) **v1.24.1 patch within 48 h SLA**: add `(cat|head|tail|less|more)[[:space:]]+[^|]*\.(key|pem|p12|gpg|age)` + `(cat|head|tail|less|more)[[:space:]]+[^|]*id_(rsa|ed25519|ecdsa)` to Bash regex risky_patterns; add regression tests; ship v1.24.1.
  - (c) **Block v1.24.0**: pause until gap closed.

### Memory: per-event substring captures, complete event log

```
all_pretooluse_10_daily_ms = [330, 316, 337, 295, 322, 300, 101, 102, 102, 305]
all_block_validation_ms    = [144, 104, 324]
all_posttooluse_ms         = [222, 174, 176]
```

---

## §2 SilkNode cross-project smoke (TASK-008)

**Mode**: **P2.5 (deferred post-ship)** per `tasks.md §5.2.fallback`.

**Rationale**:
- SilkNode owner not present in current session (single-user session, no SilkNode owner-provided daily-use command set).
- Day 0 of Spec cycle — P2.5 explicitly permits deferring SilkNode smoke to 7-day post-ship dogfood window.
- Aria-self smoke (TASK-007) provides ship-gate signal independently;
  SilkNode hook IS bytewise identical to Aria's (SilkNode is the upstream
  source per TASK-001 cherry-pick), so cross-project behavior validates by
  source identity rather than independent run on Day 0.

**Schema**:

```yaml
mode: deferred_post_ship
project: silknode
deadline_iso: 2026-05-30T07:00:00Z  # Day 0 + 7
escalation_iso: 2026-06-06T07:00:00Z  # Day 0 + 14 (P3 escalation per §5.2.fallback)
escalation_action: aria_owner_stand_in_with_documented_inventory
inventory_documented_inline: false  # to be added if P3 triggers (per R2 QA NF1)
```

Post-ship update protocol: when SilkNode owner runs ≥10 daily commands with v1.24.0
plugin loaded, append a `## §2 Update — SilkNode smoke (P2 captured Day-N)` section
to this file with parallel structure to §1.

---

## §3 Ship gate verdict (TASK-009)

### Verdict: **REVIEW**

Per tasks.md §5.4 rubric:
- **0 unexpected_false_positive** ✓
- **0 unexpected_false_negative** ✓ (B3 reclassified as known_limit F2)
- **2 findings requiring triage** (F1 perf overshoot, F2 new known-limit)
- **TASK-008 deferred via P2.5** (per spec fallback, acceptable Day 0 path)

### Triage required

Owner decision needed on **F1** (perf budget) and **F2** (new known-limit). 3 options each:

| Finding | (a) Accept w/ doc | (b) v1.24.1 48h SLA | (c) Block v1.24.0 |
|---------|--------------------|----------------------|-------------------|
| F1 perf | Bump budget to p95 < 400 ms (Bash) / 150 ms (Read), v1.25.x optimize | Ship v1.24.0, perf hotfix v1.24.1 in 48 h | Pause ship until perf met |
| F2 cat key-file | Add to known-limitations list, v1.25.x regex extension | Ship v1.24.0, regex patch v1.24.1 in 48 h | Pause ship until regex extended |

### §3.1 Triage decisions (owner-recorded)

| Finding | Decision | Recorded |
|---------|----------|----------|
| F1 perf budget overshoot | **(a) Accept + budget 修订** — bump CHANGELOG / proposal Performance Budget to `p95 < 400 ms (Bash path)` / `p95 < 150 ms (Read/Edit path)`. v1.25.x roadmap: hook perf optimization (compile regex / pre-flatten jq pipeline). | 2026-05-23 owner sign-off via AskUserQuestion |
| F2 Bash cat-key-file false-negative | **(a) Accept as new known-limit** — add to v1.24.0 CHANGELOG known-limitations list as item (c). Workarounds: use Read tool / secret-scan PostToolUse second-line defense / `# guard:ack:` bypass. v1.25.x roadmap: Bash regex `risky_patterns` extension for local `(cat\|head\|tail\|less\|more) <key-file>`. | 2026-05-23 owner sign-off via AskUserQuestion |

### After triage

TASK-010 (post_implementation audit) proceeds. CHANGELOG.md + proposal.md updated
to reflect revised perf budget + new known-limit per owner triage decisions.

---

## §4 Updates ledger

| Date | Event | Author |
|------|-------|--------|
| 2026-05-23T07:12:29Z | Initial Aria self dogfood capture (TASK-007); SilkNode P2.5 fallback recorded (TASK-008); REVIEW verdict (TASK-009) with 2 findings + owner triage required | Claude Opus 4.7 (1M ctx) |
