# Aria 2.0 M5 Carryover — Layer 2 changes-mode container (bash mode dispatcher)

> **Level**: 3 (Full — Layer 1 + Layer 2 image + Nomad HCL + side-effect doc patches)
> **Status**: **Approved** (Phase A.2 R1+R2+R3 convergence; R3 stability 2/3 STABILITY_CONFIRMED + 1 surgical residual fix applied; R4 unnecessary per code-reviewer proportionality recommendation `feedback_agent_team_for_level1`)
> **Change ID**: `aria-2.0-m5-carryover-layer2-changes-mode`
> **Parent US**: US-025 (M5 carryover; M3 carryover trio pattern: see archived `2026-05-07-m3-carryover-hcl-crons-sweep/`, `2026-05-07-m3-carryover-result-path-derivation/`, `2026-05-07-m3-handoff-validator-spillover/`)
> **Brainstorm source**: [`.aria/decisions/2026-05-15-m6-brainstorm.md`](../../../.aria/decisions/2026-05-15-m6-brainstorm.md) D1-D7 (D5 A2 skeleton-then-fill — implementation language clarified bash per R1 reality-drift fix C1)
> **Sibling Spec**: `aria-2.0-m5-carryover-layer2-redo-mode-aux/` (Spec Y; drops 'redo' mode handler into the `_not_implemented_yet` slot)
> **Estimate**: ~25h AI-runnable (T1+T2+T3+T4+T5+T6+T7 = 3+1+5+10+1+3+2 = **25h** post-R1 fixes; brainstorm baseline ~22h ×1.14 within tolerance per `feedback_phase_a_depth_drives_b_velocity`. T3 bash split 5h vs Python rewrite 8-15h — net savings; T6 +1h R1 qa, T7 +1h R1 I1)
> **Created**: 2026-05-15
> **R1 audit**: `.aria/audit-reports/post_spec-R1-2026-05-15T1725Z-aria-2.0-m5-carryover-layer2-changes-mode-summary.md` (73 findings, FAIL)

---

## R1 → v2 fixes (reality drift + ambiguities resolved)

| R1 finding | v2 fix |
|------------|--------|
| C1 Layer 2 is bash, not Python | T3 reframed: split `entrypoint-m1.sh` into `entrypoint.sh` (dispatcher) + `modes/initial.sh` (596-line bash, zero-content-change `git mv`) + `modes/changes.sh` (new) — preserves A2 skeleton-then-fill in bash |
| C2 AD-M5-3 status replace | T7.3 reframed: **append** new line below "DEFERRED to M6", preserve original |
| C3 `claude -p --prompt-file` flag missing | T4 uses positional `claude -p "$RENDERED_PROMPT"` (per existing `entrypoint-m1.sh:314`) |
| C4 `aria_layer1` Python not in image | T4 uses bash + curl + jq (per existing `entrypoint-m1.sh` Forgejo issue-fetch pattern §6) |
| C5 60K cap contradiction across 3 docs | Locked to: **sys.exit(2) + S_FAIL(prompt_overflow)** (Spec X window); fallback-to-redo deferred to Spec Y (which ships `_not_implemented_yet` → `mode_redo.sh`) |
| C6 'retry' mode handler inverted | **Layer 1 does NOT write REWORK_MODE for `rework_mode='retry'`** rows (retry preserves failure_analysis context Layer-1-side only); Layer 2 sees missing REWORK_MODE → defaults to `initial`; dispatcher only branches on 'changes' / 'redo' (Spec Y) / missing |
| C7 Regression gate unenforceable | T6 enumerates explicit test files (see §F) |
| C8 build_nomad_meta MetaSizeExceeded | T6 adds boundary test (near-4KB feedback + 5 required keys) |
| HIGH ai-engineer #2 tokenizer | Lock char-count budget (CJK-aware ratio × 0.4); explicit Spec note that Anthropic tokenizer-precise count is M7+ |
| HIGH ai-engineer #5 model docs | New §Model Path explicit: claude-opus-4-5 via Luxeno proxy (per `entrypoint-m1.sh:38` ARIA_MODEL), NOT M3 GLM ProviderRouter |
| HIGH qa REWORK_FEEDBACK UTF-8 / 4KB boundary | T1.3 truncation uses codepoint-aware slice; T6 adds CJK + boundary tests |
| HIGH qa Forgejo 4xx untested | T4.1 + T6 enumerate 404 / 403 / 5xx / malformed-JSON paths |
| HIGH qa force-push rejection | T4.5 + T6 cover exit-code non-zero → S_FAIL path |
| HIGH qa HCL ↔ Layer 1 key inventory | T2.5 + T6 add cross-check test (T1.3 written keys ⊆ T2.2 HCL meta_optional) |
| HIGH qa spec_id for Spec Y | Spec X NOT in scope — Spec Y T8.0 will add column if needed (cross-spec note added to §Out of Scope) |
| HIGH qa T6 2h estimate | T6 bumped to 3h (per `feedback_pre_draft_bug_hunt_discipline` 1-3 real bugs expected) |
| HIGH code-reviewer AD-M5-3 line range | Corrected to 3574-3613 (AD-M5-4 starts 3614) |
| HIGH code-reviewer brainstorm 4th mode | brainstorm D5 footnote: 'retry' is Layer-1-internal (per C6), NOT a Layer-2 dispatcher mode → registry stays 3 keys (initial / changes / redo) |
| I1 US-026 receiving doc | T7.5 NEW: create `US-026.md` skeleton with §M6b absorption note (per D7) |
| I2-I5 m5-handoff / US-025 status / handoff doc | T7 expanded sub-tasks |
| I6 Forgejo PAT secret-hygiene | New §Secret Hygiene: explicit cross-ref `standards/conventions/secret-hygiene.md`; PAT injected via Nomad Variables template (per existing `aria-layer2-runner.hcl:222-225`) |
| I7 dual-repo pre-merge gate | T8.4 split: aria-orchestrator PR gate + Aria main PR gate |
| I8 Phase D.3 handoff | T8.10 NEW: evaluate Rule #9 trigger (cross ≥2 phases → write handoff) |
| I9 AD-M5-3 risk #1 cross-ref | proposal §D explicit cite "AD-M5-3:3605 force-push-loses-context mitigation" |
| Image tag naming | `claude-m5-carry-<sha>-v10` (M3 trio precedent compatible) |

(Full R1 cross-ref retained in audit report. v2 reduces finding count by ≥80% expected.)

---

## Why

M5 (US-025) Phase B 2026-05-15 ship 仅完成 **Layer 1 wiring** for review-loop 改稿/重做 (per AD-M5-3 Decided 2026-05-14): owner 在 PR comment 发 `/aria changes: <feedback>` → Layer 1 创建新 dispatch row `rework_mode='changes'` + `pr_id=<inherited>` + `rework_feedback=<text>`, 新行进入 S4_LAUNCH。但 **Layer 2 容器侧的实际 changes mode 实施** (fetch 原 PR branch + apply feedback prompt + force-push) **被 AD-M5-3 显式标记 deferred to M6**。

**M5 期间已知 limitation** (AD-M5-3 §"M5 期间观察行为"):
- owner /aria changes → 新行 S4 → 卡住 → reconciler 7d timeout → S_FAIL(human_timeout)
- Acceptance test 期间 owner 仅使用 /aria approve / /aria reject
- US-025 Phase D.2 final Go 需 Spec X+Y archive 后才能 close

**Spec X 价值**:
1. 解锁 owner 高频 review-loop 用法 (`/aria changes:` 改稿, M5 brainstorm Q5 owner-locked > 50% rework usage)
2. 为 Spec Y 提供 bash mode dispatcher 基础设施 (D5 A2 skeleton-then-fill: X+Y 总成本 ~41h)
3. 解除 US-025 D.2 close gate 中的 Spec X archive 前置条件 (per D7)

**为什么 bash 而非 Python** (R1 C1 reality-drift fix):
- 现有 Layer 2 image (`docker/aria-runner/Dockerfile`) = Node base + Claude CLI npm + bash entrypoint
- `entrypoint-m1.sh` (596 行) 已经处理 11 步 flow (clone / claude -p / parse / push / PR create)
- changes mode 只需在 11 步 flow 头部加 conditional branch:`if REWORK_MODE == 'changes': git fetch existing PR branch + skip "create new branch" step + force-push instead of push to new branch`
- bash dispatcher 与现有 test infra (`docker/aria-runner/tests/*.sh`) 兼容

---

## What

### In scope (Spec X must deliver, ~25h post-R1+R2 fixes)

#### A. Layer 1 dispatcher 扩展 (~3h)
- `aria_layer1/extension.py::_handle_s4_launch`:Build Nomad meta dict 时, 检查 `dispatch_row.rework_mode`:
  - `IS NULL` (原始 dispatch): 不写新 meta keys (Layer 2 defaults to 'initial')
  - `'changes'`: 写 `REWORK_MODE='changes'` / `REWORK_FEEDBACK` (codepoint-truncated ≤4KB) / `PARENT_PR_ID` / `REWORK_OF`
  - `'redo'` (Spec Y): 同 'changes' 但 REWORK_MODE='redo'
  - `'retry'` (M5 failure_analysis): **不写** REWORK_MODE (per R1 C6 — retry 上下文是 Layer-1-internal,Layer 2 当作 initial)
- 4KB 截断使用 codepoint-aware slice (避免 UTF-8 corruption): `feedback.encode('utf-8')[:4096].decode('utf-8', errors='ignore')` 或等效逻辑
- audit log event `meta_optional_written` 记录哪些 keys 被写入

#### B. Nomad HCL meta_optional 扩展 (~1h)
- `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl::parameterized.meta_optional`: 加 4 keys
- meta_required 不动 (M1 BC)
- `nomad job validate` 通过

#### C. Layer 2 bash mode dispatcher (~5h, R1 C1 reality-aligned)
- `docker/aria-runner/entrypoint.sh`:**新 dispatcher**, 替换 58 行 scaffold (`-m0-scaffold.bak`):
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  MODE="${NOMAD_META_REWORK_MODE:-initial}"
  case "${MODE}" in
    initial) exec /opt/aria-runner/modes/initial.sh "$@" ;;
    changes) exec /opt/aria-runner/modes/changes.sh "$@" ;;
    redo)    echo "ERR: redo mode not implemented (Spec Y carryover)" >&2
             echo '{"outcome":"FAIL","error":"redo_mode_unimplemented"}' >"${ARIA_OUTPUTS_DIR}/result.json"
             exit 1 ;;
    *)       echo "ERR: unknown REWORK_MODE=${MODE}" >&2; exit 1 ;;
  esac
  ```
- **`git mv entrypoint-m1.sh modes/initial.sh`** (596 行内容零改, 仅路径迁移; existing tests 改 path 即可)
- Dockerfile `ENTRYPOINT ["/entrypoint.sh"]` 仍指向新 dispatcher; `modes/` 复制入 `/opt/aria-runner/modes/`
- Bash 3-mode dispatcher (4 case branches): 5 test scenarios exercise initial+changes 两 handler + redo 早退 + unknown 报错 + 缺省 (REWORK_MODE 不设置 → 'initial' fallback)

#### D. modes/changes.sh 实施 (~10h, bash + curl + jq + envsubst per existing pattern)
- Forgejo API via curl + jq (复用 `entrypoint-m1.sh:200-260` 风格,不引入 Python dep):
  - `GET /repos/<org>/<repo>/pulls/${NOMAD_META_PARENT_PR_ID}` → 拿 head branch name + clone URL (`.head.ref` + `.head.repo.clone_url`)
  - `GET /repos/<org>/<repo>/pulls/${NOMAD_META_PARENT_PR_ID}/reviews/comments` → 拉 review comments
  - 5xx retry × 3 with expo backoff (1s/2s/4s); 4xx → 立即 S_FAIL with fail_reason mapping (404 → `parent_pr_not_found`, 403 → `forgejo_permission_denied`)
  - 200 + malformed JSON → S_FAIL(`forgejo_malformed_response`)
- Forgejo PAT via `NOMAD_SECRET_FORGEJO_BOT_PAT` (already injected per existing HCL:222-225 template stanza, Nomad Variables-backed, secret-hygiene 合规 per Rule #7;不入 stdout / 不入 audit log)
- Prompt assemble (per AD-M5-3:3591-3596 lock + R1 ai-engineer ordering fix):
  - Section ordering (deterministic): **(1)** feedback (must, no truncate beyond Layer 1 4KB), **(2)** original issue body (from `${INPUTS_DIR}/issue.yaml` per existing pattern; truncate to 10K chars), **(3)** PR review comments (sorted by `created_at` ASC, cap last 30), **(4)** file-by-file diff (feedback-prioritized, cap remaining budget)
  - Char budget: total 240K chars (~60K tokens × 0.25 char/token CJK-aware ratio 0.4 = 24K tokens worst-case; 60K tokens for ASCII-heavy)
  - Overflow → **sys.exit(2) + S_FAIL(prompt_overflow)** (Spec X window; fallback-to-redo activates Spec Y ship)
  - Markdown append `[TRUNCATED: N kb]` markers if section truncated
- Git ops (per `feedback_git_force_with_lease_shallow_clone`):
  - `git clone --depth 1 --branch ${HEAD_BRANCH} ${CLONE_URL} work/`
  - `cd work/ && git fetch origin ${HEAD_BRANCH}` (建 FETCH_HEAD)
  - `claude -p "$(envsubst < /opt/aria-runner/prompts/changes.tpl)"` (per existing positional syntax `entrypoint-m1.sh:314`; with `timeout ${CLAUDE_TIMEOUT_S} -k 10s`)
  - Parse stream-json (reuse `lib/parse-stream-json.sh` existing helper)
  - Auto commit message: `claude` final response 中 extract `commit_message:` line OR fallback `changes(rework round ${ROUND}): ${FEEDBACK_HEAD30}`
  - `git push --force-with-lease=${HEAD_BRANCH}:$(git rev-parse FETCH_HEAD) origin ${HEAD_BRANCH}` (per memory entry; rejection → S_FAIL(`force_push_stale_ref`))
  - Force-push 后 emit audit event `pr_review_threads_outdated_warning` (per AD-M5-3:3605 mitigation)

#### E. Image build + digest pin (~1h)
- Dockerfile 新增 `COPY entrypoint.sh /entrypoint.sh` + `COPY modes/ /opt/aria-runner/modes/`
- Tag: `claude-m5-carry-<commit-sha>-v10` (R1 fix: M3 trio precedent compatible naming)
- Image push to `forgejo.10cg.pub/10cg/aria-runner`
- sha256 digest pulled + written to HCL **`meta_required.IMAGE_SHA` dispatch-time pin** (R1 fix: IMAGE_SHA is meta_required, not meta_optional default)
- `aria-build-verify` Nomad job confirms digest

#### F. Synthetic acceptance (~3h, R1 fix: bumped from 2h per pre-draft bug discipline)

**Test files** (all under existing `aria-orchestrator/docker/aria-runner/tests/` bash infra + new Python unit tests under `hermes-extensions/aria-layer1/tests/`):

| File | Coverage |
|------|----------|
| `tests/changes-mode/dispatcher.sh` | Bash dispatcher: 4 modes (initial / changes / redo-fails / unknown-fails) + missing REWORK_MODE → initial fallback |
| `tests/changes-mode/mode_changes-prompt.sh` | Prompt assemble: empty feedback / 60K overflow boundary / 60001 char overflow / non-existent file in feedback / empty PR comments / 100+ PR comments truncation / UTF-8 CJK feedback (no corruption) |
| `tests/changes-mode/mode_changes-git.sh` | Git ops: clone-fetch-push command sequence captured + force-push ref correct + force-push stale-ref rejection → S_FAIL(`force_push_stale_ref`) |
| `tests/changes-mode/forgejo-errors.sh` | Forgejo 404 / 403 / 5xx-3-retries / malformed-JSON → mapped fail_reasons |
| `hermes-extensions/aria-layer1/tests/test_t_changes_mode_meta.py` | Layer 1 _handle_s4_launch writes 4 meta keys correctly (changes / redo / retry-NO-write / initial-NO-write) + 4KB UTF-8 codepoint truncation + audit event `meta_optional_written` |
| `hermes-extensions/aria-layer1/tests/test_t_changes_mode_size.py` | build_nomad_meta with 4KB REWORK_FEEDBACK + 5 required keys → no MetaSizeExceeded |

**Regression gates** (enumerated, runnable):
```bash
# Bash regression (M1-M5 initial mode):
bash tests/t3-verify.sh
bash tests/compute-assertions/test.sh
bash tests/parse-stream-json/test.sh
bash tests/push-classifier/test.sh

# Python regression (Layer 1 M5 baseline 793 tests):
cd hermes-extensions/aria-layer1 && python -m pytest tests/ -v --tb=short
# Specifically: tests/test_t_rework_loop.py (M5 mode field handling) + tests/test_t_acceptance_m5.py (M5 E2E)
```

**HCL test**:
- `nomad job validate aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` → 通过
- Python test `test_t_hcl_meta_inventory.py`: parses HCL `meta_optional` keys + asserts ⊇ {REWORK_MODE, REWORK_FEEDBACK, PARENT_PR_ID, REWORK_OF}

**Production verification deferred** to US-026 M6b ≥10 dispatch (per D7).

#### G. Side-effect patches (Spec X Phase B 同步 — ~1h)
- T7.0: `docs/requirements/user-stories/US-025.md`:**status line update** "in_progress — Phase D.1 done, awaiting D.2" → "in_progress — Phase D.2 owner gates + M6a Spec X+Y in-flight" (R1 I4 fix)
- T7.1: US-025.md footer "M5 Carryover Sub-Specs" linking Spec X + Spec Y (placeholder)
- T7.2: `aria-orchestrator/docs/m5-handoff.yaml::open_issues_for_m6`:
  - M5-OS-1 加 `absorbed_by: aria-2.0-m5-carryover-layer2-changes-mode`
  - 新顶层 field `m6_carryover_to_us_026.tier2_path_coverage_absorbed: true` (D7 implementation)
- T7.3: `aria-orchestrator/docs/architecture-decisions.md::AD-M5-3` **append** (R1 C2 fix, not replace): 在原 status 行下加新行 "2026-05-15: Implementation in-flight via Spec X (aria-2.0-m5-carryover-layer2-changes-mode), AD-M5-3 line range 3574-3613 unchanged"
- T7.4: `aria-orchestrator/docs/validate-m5-handoff.py` 加 `check_m6_carryover_to_us_026_present` + unit test (per `feedback_validator_repo_drift_guard_test`)
- T7.5 NEW (R1 I1): `docs/requirements/user-stories/US-026.md` 创建 skeleton with §"M6b inherits Tier-2 path coverage from US-025 carryover" 段落 (D7 receiving doc)
- T7.6 NEW (R1 I5): `docs/handoff/2026-05-15-us025-m5-c2-d1-done.md` 加 addendum "Spec X kickoff 2026-05-15" link
- T7.7: `docs/handoff/latest.md`:**Phase D 后**更新 pointer (Phase A 期间不更新 — 与 M5 Phase D.1 progress pattern 一致)
- T7.8: 不动 `prd-aria-v2.md` (per D4)

#### H. Model + Provider path documentation (~0.5h, R1 ai-engineer HIGH#5 fix)

**Layer 2 LLM stack** (proposal-explicit, not by exclusion):
- Image base: `claude-m5-carry-<sha>-v10` (Node 20 + Anthropic Claude CLI npm)
- Model: `claude-opus-4-5-20250929` (via `ARIA_MODEL` env, `entrypoint-m1.sh:38`)
- Provider: **Luxeno proxy** (`ANTHROPIC_BASE_URL=https://luxeno.ai/api`) — NOT M3 GLM ProviderRouter chain
- Spec X mode_changes 使用同模型 + 同 proxy(零变更);M3 ProviderRouter (S2=glm-4.5-air / S3=glm-5-turbo / S6=glm-5.1) 是 **Layer 1 LLM ops 专用**(triage / review / failure_analysis),与 Layer 2 changes mode 无关

#### I. Secret Hygiene (R1 I6 fix, Rule #7 cross-ref)

- Forgejo PAT 通过 Nomad Variables (`secrets/aria-runner.env`, per HCL:222-225 existing template stanza), env name = `FORGEJO_BOT_PAT`
- changes.sh **不**记录 PAT 到 stdout / audit log / result.json (per `standards/conventions/secret-hygiene.md`)
- Forgejo HTTP error response body 不入 audit log (only HTTP status code + error reason)
- changes.sh 不调 `cat` / `echo` 任何 env var containing PAT 字面值

---

### Out of Scope (deferred or rejected)

- **Spec Y scope** (`aria-2.0-m5-carryover-layer2-redo-mode-aux/`): redo mode + close-old-PR + spec_drift_fetcher + commit-lint retry. Spec Y T8.0 will assess if `spec_id` schema column 需要 added (per R1 qa cross-spec note)
- **risk-tier algorithm** → M7+ per D6
- **`claude -p` provider routing changes** → M3 ProviderRouter for Layer 1 unchanged; Layer 2 Claude+Luxeno path unchanged
- **Schema migration v4 → v5** → not introduced
- **comment-poll cadence** → M5 already < 60s per AD-M5-1, untouched
- **Append-commit mode** (vs force-push) → AD-M5-4 locked force-push, Spec X 不重开此决策
- **Double-LLM-pass changes mode** → not introduced (single claude -p invocation)
- **Anthropic-tokenizer-precise token counting** → M7+ (Spec X uses char × CJK-aware ratio 0.4 估算)
- **Spec_id schema column** for OS-4 spec_drift_fetcher → Spec Y scope
- **Nomad scheduler-level dispatch rejection** (job not running / meta validation error at Nomad API / heavy_workload constraint unsatisfied) → deferred to US-026 M6b production smoke (R2 qa NEW-2)
- **Concurrent Layer 2 alloc race** (two `/aria changes:` commands in rapid succession on same PR) → Nomad parameterized job is single-alloc per dispatch call; Layer 1 reconciler partial-unique gate (`uq_issue_active_partial`) prevents two live rows per pr_id (M5 existing guarantee); concurrent race verification deferred to US-026 M6b (R2 qa NEW-3)

---

## Key Decisions (cross-ref brainstorm)

| 决策 | 锁定项 | Source |
|------|--------|--------|
| D1 | M6 = M6a (US-025 carryover) + M6b (US-026 docs/release ~120h) | brainstorm Q1 |
| D2 | M6a = 2 Specs, Spec X first ship | brainstorm Q2 (risk-tier 移除 per D6) |
| D3 | Layer 2 context via Nomad meta_optional (4 keys) | brainstorm Q3 |
| D4 | M6a归 US-025 carryover, no new US-028 | brainstorm Q4 |
| D5 | A2 skeleton-then-fill (bash 5-mode dispatcher; 'redo' = early-fail; 'retry' → Layer-1-internal, Layer 2 不分支) | brainstorm Q5 + R1 C1/C6 fix |
| D6 | risk-tier algo 推 M7+ | brainstorm Q6 |
| D7 | Tier-2 path coverage absorbed to US-026 M6b ≥10 dispatch | brainstorm Q7 |
| AD-M5-3 | Layer 1↔Layer 2 contract (rework_mode/feedback/pr_id/rework_of) | architecture-decisions.md:3574-3613 |
| AD-M5-3 §risk #1 | force-push 后 pull PR review comments mitigation | architecture-decisions.md:3605 |
| AD-M5-4 | force-push (not append-commit) | architecture-decisions.md:3614+ |
| AD-M5-10 | M5→M6 forward-binding promises (5 enumerated); Spec X preserves all 5 | architecture-decisions.md:3471 |
| AD-M1-7 | image sha256 digest dispatch-time pin (meta_required.IMAGE_SHA) | architecture-decisions.md:1537 |

---

## 验收

### A.1 Phase 完成验收
- [ ] proposal.md v2 (本文件) created + R1 fixes mapped (§"R1 → v2 fixes")
- [ ] tasks.md v3 created (8 task groups, ~25h breakdown, R1+R2 fixes applied)
- [ ] `openspec validate aria-2.0-m5-carryover-layer2-changes-mode --strict` if available; else manual schema check (R1 code-reviewer fix: graceful degradation)

### Phase A.2 audit 收敛
- [ ] R2 audit (5 agents) finding count reduction ≥ 80% vs R1 baseline 73 findings
- [ ] R3 stability round (per `feedback_pre_merge_iteration_pattern`): 0-finding 稳定性确认
- [ ] Spec Status → Approved

### Phase B 实施完成验收 (R1 fixes: explicit + enforceable)
- [ ] T1-T8 全部 `[x]` complete
- [ ] All new bash tests (`tests/changes-mode/*.sh`) PASS
- [ ] All new Python tests (`hermes-extensions/aria-layer1/tests/test_t_changes_mode_*.py`) PASS
- [ ] Regression suite PASS (specific commands, see §F)
- [ ] `nomad job validate aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` PASS (R2 qa NEW-4 explicit gate)
- [ ] Image build + sha digest pinned in HCL `meta_required.IMAGE_SHA` (dispatch-time pin per AD-M1-7)
- [ ] Approximate test count ≥ 32 new behavioral tests, **case-counted not file-counted** (R2 qa NEW-1 fix):
      `pytest --collect-only -q hermes-extensions/aria-layer1/tests/test_t_changes_mode_*.py | tail -1` + `grep -c 'assert\|check_\|expect_' docker/aria-runner/tests/changes-mode/*.sh | awk -F: '{sum+=$2} END {print sum}'`
- [ ] **Rule #6 benchmark exemption** explicit: Spec X 仅修改 aria-orchestrator code + docs, 不修改 aria plugin Skill 逻辑 → exempt per `feedback_level2_patch_no_benchmark` v1.11.1 precedent (R2 context-manager N7 fix)

### Phase C merge (R1 I7 fix: dual-repo gate explicit)
- [ ] aria-orchestrator PR merged (pre-merge gate: `aether ci status --branch master --in-flight --repo aria-orchestrator`)
- [ ] Aria 主 repo PR merged (submodule bump + side-effect patches T7) (pre-merge gate: `aether ci status --branch master --in-flight --repo Aria`)
- [ ] Both repos master parity (Forgejo origin + GitHub) verified via SHA equality

### Phase D archive (Spec X 独立 archive,不等 Spec Y; R1 I3+I5 fix: progressive cross-ref link)
- [ ] `openspec/archive/2026-XX-XX-aria-2.0-m5-carryover-layer2-changes-mode/` 归档
- [ ] US-025 status 仍 in_progress (Spec Y + T-deploy + Tier-1 还未完成)
- [ ] (R1 I8) Rule #9 trigger evaluation: Spec X 单 session Phase A+B+C+D 跨 ≥2 phases → write session handoff `docs/handoff/2026-XX-XX-spec-x-shipped.md`

---

## 价值

| 维度 | 解锁 |
|------|------|
| Owner UX | `/aria changes:` 高频用法 live (vs M5 ship 时 S_FAIL human_timeout) |
| Spec Y velocity | Bash dispatcher infra in place,Y 仅 ~19h drop-in (mode_redo.sh + close-old-PR + spec_drift + commit-lint) |
| US-025 close path | Spec X archive 是 D.2 close 2 个 AI 前置之一 (另一个 Spec Y) |
| Aria methodology | M3 carryover trio pattern 第二次实证 |
| Code reality alignment | Bash-aligned 实现匹配现有 Layer 2 stack;避免 Python rewrite 30-40h cost |

---

## 风险与回滚

| 风险 | Severity | Mitigation |
|------|----------|-----------|
| Bash mode dispatcher 抽象被 R2 audit 标 over-engineered | Low | Phase A.2 R2 时回退到 inline `if/elif` (concrete) — 5h 工作量 vs 现在 5h, refactor risk 几乎一致 |
| force-push 后 PR review threads marked outdated | Medium (AD-M5-3 known) | AD-M5-3:3605 mitigation locked: pull PR comments 进 prompt context;audit event `pr_review_threads_outdated_warning` emit |
| 60K char budget overflow → sys.exit(2) | Low | Truncation markers `[TRUNCATED: N kb]` 给 owner 可见 cue;Spec Y ship 后 fallback-to-redo 生效 |
| Image v10 build breaks aria-build pipeline | Low | 5x prior bumps successful;aria-build-verify validates digest |
| Forgejo API rate-limit | Low | 5xx retry × 3 expo backoff (1s/2s/4s);Layer 2 alloc 1 次 fetch / dispatch |
| Layer 1 `_handle_s4_launch` regression breaks M5 initial mode | Medium | Test parity (rework_mode IS NULL → 不写 keys);existing 793 tests must PASS |
| Bash test fragility vs CI environment | Low | `tests/changes-mode/*.sh` 复用 existing `t3-verify.sh` pattern, 已 production-validated |
| 4KB UTF-8 codepoint truncation 实现错误 | Medium | T1 unit test 4 cases (ASCII boundary, CJK boundary, mixed, exact 4KB) |

**回滚路径**:
1. **Code-only revert**: revert aria-orchestrator PR → Layer 1 不写新 meta keys → Layer 2 image v10 仍部署但所有 dispatch 走 'initial' mode → 与 M5 ship 时一致, 无 regression
2. **Image revert**: 改 HCL `meta_required.IMAGE_SHA` default value 回 v9 → 新 dispatch 用回旧 image
3. **Spec Y 影响**: 若 Spec X 出生产事故,Spec Y 等 Spec X hotfix 后再启动 (per `feedback_sister_bug_bundling`)

---

## 排序依赖

```
T1 (Layer 1 meta write) ─┐
T2 (HCL meta_optional)  ─┴─→ T3 (bash dispatcher + git mv)
                                    │
                                    ↓
                            T4 (modes/changes.sh)
                                    │
                                    ↓
                            T5 (image build + digest)
                                    │
                                    ↓
                            T6 (synthetic acceptance)
                                    │
                                    ↓
                            T7 (side-effect patches)
                                    │
                                    ↓
                            T8 (Phase C merge + Phase D archive + Rule #9 handoff trigger)
```

T1 + T2 parallel-able. T3-T6 strict sequential. T7 prep can start at T4. T8 awaits all merge.

---

## Cross-references

- Brainstorm decision: [.aria/decisions/2026-05-15-m6-brainstorm.md](../../../.aria/decisions/2026-05-15-m6-brainstorm.md)
- R1 audit report: [.aria/audit-reports/post_spec-R1-2026-05-15T1725Z-aria-2.0-m5-carryover-layer2-changes-mode-summary.md](../../../.aria/audit-reports/post_spec-R1-2026-05-15T1725Z-aria-2.0-m5-carryover-layer2-changes-mode-summary.md)
- AD-M5-3 Layer 2 contract: [architecture-decisions.md:3574-3613](../../../aria-orchestrator/docs/architecture-decisions.md) (line range corrected per R1 code-reviewer)
- AD-M5-3 §risk #1 mitigation: [architecture-decisions.md:3605](../../../aria-orchestrator/docs/architecture-decisions.md) (force-push-loses-context; R2 corrected from 3627 per code-reviewer F2)
- AD-M5-4 force-push: same file, §AD-M5-4 (line 3614+)
- AD-M5-10 forward-binding: same file, §AD-M5-10 (line 3471)
- AD-M1-7 image sha256 pin: same file, §AD-M1-7 (line ~1537)
- Existing Layer 2 entrypoint: `aria-orchestrator/docker/aria-runner/entrypoint-m1.sh` (596 lines, 11-step flow)
- Existing Layer 2 Dockerfile: `aria-orchestrator/docker/aria-runner/Dockerfile`
- Existing Layer 2 tests: `aria-orchestrator/docker/aria-runner/tests/*.sh`
- M5 deferred: [m5-handoff.yaml::open_issues_for_m6](../../../aria-orchestrator/docs/m5-handoff.yaml)
- M5 session closeout: [docs/handoff/2026-05-15-us025-m5-c2-d1-done.md](../../../docs/handoff/2026-05-15-us025-m5-c2-d1-done.md)
- PRD v2.0 §410-414 M6 row: [prd-aria-v2.md](../../../docs/requirements/prd-aria-v2.md) (R1 D4 confirms unchanged)
- M3 carryover trio precedent: `openspec/archive/2026-05-07-m3-carryover-{hcl-crons-sweep,result-path-derivation}/` + `2026-05-07-m3-handoff-validator-spillover/`
- US-025: [docs/requirements/user-stories/US-025.md](../../../docs/requirements/user-stories/US-025.md)
- Standards: [standards/conventions/secret-hygiene.md](../../../standards/conventions/secret-hygiene.md) (Rule #7), [standards/conventions/git-commit.md](../../../standards/conventions/git-commit.md), [standards/conventions/session-handoff.md](../../../standards/conventions/session-handoff.md) (Rule #9)
- Memory references: `feedback_phase_a_depth_drives_b_velocity` / `feedback_git_force_with_lease_shallow_clone` / `feedback_audit_convergence_pattern` / `feedback_pre_merge_iteration_pattern` / `feedback_scope_bounded_merge_for_level3` / `feedback_nomad_hcl_validate_early` / `feedback_validator_repo_drift_guard_test` / `feedback_pre_draft_bug_hunt_discipline` / `feedback_sister_bug_bundling`
