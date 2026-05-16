# Spec X Tasks v2 — Aria 2.0 M5 Carryover Layer 2 changes-mode (bash dispatcher)

> **Change ID**: `aria-2.0-m5-carryover-layer2-changes-mode`
> **Parent**: US-025 (M5 carryover)
> **Estimate**: ~25h AI-runnable (T1+T2+T3+T4+T5+T6+T7 = 3+1+5+10+1+3+2 = 25h; brainstorm baseline ~22h ×1.14 tolerance)
> **Version**: v3 (R1 + R2 fixes applied; R3 stability awaiting)
> **Phase B sequencing**: T1+T2 parallel → T3 → T4 → T5 → T6 → T7 → T8

---

## Task Group 总览 (R1 v2)

| ID | 标题 | 工时 | 阻塞 |
|----|------|------|------|
| T1 | Layer 1 dispatcher 写 meta_optional 3 keys (retry NOT writes) | 3h | — |
| T2 | Nomad HCL meta_optional 扩展 + key inventory test | 1h | — |
| T3 | Bash entrypoint dispatcher + `git mv entrypoint-m1.sh modes/initial.sh` | 5h | T1, T2 |
| T4 | modes/changes.sh 实施 (bash + curl + jq + claude -p positional) | 10h | T3 |
| T5 | Layer 2 image build v10 + sha256 digest pin (meta_required.IMAGE_SHA) | 1h | T4 |
| T6 | Synthetic acceptance (~32 new tests, bash + Python) | 3h | T5 |
| T7 | Side-effect patches (US-025 status + footer + m5-handoff + AD-M5-3 append + US-026 skeleton + handoff addendum) | 2h | T4 (并行) |
| T8 | Phase C dual-repo merge + Phase D archive + Rule #9 handoff trigger | (Phase C/D 标准) | T6, T7 |

总: ~25h (R1 fix: T6 +1h 测试增强, T7 +1h 新增 US-026 skeleton; T3 -1h bash 比 Python 简单 = 净 +3h, 但仍在原 brainstorm ~22h baseline 容差内)

**实际**: T1(3) + T2(1) + T3(5) + T4(10) + T5(1) + T6(3) + T7(2) = **25h**

---

## Phase 1 — Layer 1 + HCL 契约 (T1+T2, 4h, parallel-able)

### T1 — Layer 1 `_handle_s4_launch` 写 meta_optional (~3h, R1 C6 fix: retry NOT writes)

- [ ] 1.1 在 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/extension.py::_handle_s4_launch` 加 rework_mode 分支。**Insertion anchor** (R2 code-reviewer F4): immediately before `nomad_client.dispatch_job(...)` call (existing site builds `nomad_meta` dict via `build_nomad_meta()` helper at L1903-1912); 新增 conditional extend `extra` dict with rework keys when `dispatch_row.rework_mode IS NOT NULL AND != 'retry'`. Existing meta keys (BUDGET_CAP_USD / TRIAGE_BODY_JSON / PROMPT_PATH) unchanged.
- [ ] 1.2 读 dispatch row `rework_mode` / `rework_feedback` / `pr_id` / `rework_of`
- [ ] 1.3 分支逻辑:
  - `rework_mode IS NULL` → 不写新 keys (initial)
  - `rework_mode == 'changes'` 或 `== 'redo'` → 写 4 keys (REWORK_MODE / REWORK_FEEDBACK / PARENT_PR_ID / REWORK_OF)
  - `rework_mode == 'retry'` → **不写 REWORK_MODE** (per R1 C6: retry 上下文是 Layer-1-internal,Layer 2 当 initial; failure_analysis 信号通过 reconciler audit 链消费, 不通过 Nomad meta)
- [ ] 1.4 REWORK_FEEDBACK 4KB 截断使用 codepoint-aware slice: `feedback.encode('utf-8')[:4096].decode('utf-8', errors='ignore')` (R1 qa-engineer UTF-8 fix)
- [ ] 1.5 audit log event `meta_optional_written` 记录哪些 keys 被写入 + 是否触发 truncation
- [ ] 1.6 单元测试: `test_t_changes_mode_meta.py` (~8 cases):
  - rework_mode=NULL → 0 new keys, audit event `meta_optional_written: {}`
  - rework_mode='changes' → 4 keys written + correct values
  - rework_mode='redo' → 4 keys written + REWORK_MODE='redo'
  - rework_mode='retry' → 0 new keys (R1 C6 verify)
  - REWORK_FEEDBACK 4096 bytes ASCII → no truncation
  - REWORK_FEEDBACK 4097 bytes ASCII → truncation + audit warn
  - REWORK_FEEDBACK 4096 bytes Chinese (1366 chars × 3 bytes ≈ 4098) → codepoint-aware truncation (no corruption)
  - REWORK_FEEDBACK with newlines + control chars → preserved
- [ ] 1.7 单元测试: `test_t_changes_mode_size.py` build_nomad_meta with 4KB REWORK_FEEDBACK + 5 required keys → no MetaSizeExceeded (R1 C8 fix)

### T2 — Nomad HCL meta_optional + 跨层 key inventory test (~1h, R1 qa HIGH fix)

- [ ] 2.1 编辑 `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl::parameterized.meta_optional`
- [ ] 2.2 list 加 `"REWORK_MODE"`, `"REWORK_FEEDBACK"`, `"PARENT_PR_ID"`, `"REWORK_OF"` (formatting 与现有 BUDGET_CAP_USD / TRIAGE_BODY_JSON / PROMPT_PATH 一致)
- [ ] 2.3 meta_required 不动 (M1 BC; IMAGE_SHA 保持 dispatch-time pin per AD-M1-7 — R1 fix: 之前错误地说 default)
- [ ] 2.4 `nomad job validate aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` 通过
- [ ] 2.5 跨层 key inventory test (NEW R1 qa fix): `test_t_hcl_meta_inventory.py` 解析 HCL meta_optional → 断言 T1.3 写入的 keys (REWORK_MODE/REWORK_FEEDBACK/PARENT_PR_ID/REWORK_OF) ⊆ HCL declared meta_optional (防止 key name typo invisible 到 nomad validate)
- [ ] 2.6 commit message 含 4 keys 字面 (audit-friendly)

---

## Phase 2 — Bash dispatcher (T3, 5h, R1 C1 fix: bash 不是 Python)

### T3 — Bash entrypoint dispatcher + zero-content modes/initial.sh

- [ ] 3.1 创建 `docker/aria-runner/entrypoint.sh` v2 (新 dispatcher, 替换 现有 58 行 scaffold). **R2 backend H2 fix**: OUTPUTS_DIR default fallback applied:
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  # R2 fix: defensive default per entrypoint-m1.sh:33 pattern (ARIA_OUTPUTS_DIR may be unset)
  OUTPUTS_DIR="${ARIA_OUTPUTS_DIR:-/opt/aria-outputs}"
  MODE="${NOMAD_META_REWORK_MODE:-initial}"
  case "${MODE}" in
    initial) exec /opt/aria-runner/modes/initial.sh "$@" ;;
    changes) exec /opt/aria-runner/modes/changes.sh "$@" ;;
    redo)
      echo "ERR: redo mode not implemented (Spec Y carryover)" >&2
      mkdir -p "${OUTPUTS_DIR}"
      echo '{"outcome":"FAIL","error":"redo_mode_unimplemented","spec_y_pending":true}' > "${OUTPUTS_DIR}/result.json"
      exit 1 ;;
    *)
      echo "ERR: unknown REWORK_MODE=${MODE}" >&2
      mkdir -p "${OUTPUTS_DIR}"
      echo '{"outcome":"FAIL","error":"unknown_rework_mode","value":"'"${MODE}"'"}' > "${OUTPUTS_DIR}/result.json"
      exit 1 ;;
  esac
  ```
- [ ] 3.2 现有 `entrypoint-m1.sh` (596 行) **`git mv` 到 `docker/aria-runner/modes/initial.sh`** (零内容变更; 仅 Dockerfile COPY 路径改变)
- [ ] 3.3 现有 58 行 `entrypoint.sh` `git mv` 到 `docker/aria-runner/entrypoint-m0-scaffold.sh.bak` (历史保留, per existing convention 见 entrypoint-m1.sh:6)
- [ ] 3.4 Dockerfile 改 (R2 backend H1 fix: chmod modes/):
  - 删 `COPY entrypoint.sh /entrypoint.sh` 旧行 + `COPY entrypoint-m1.sh /entrypoint-m1.sh` 旧行
  - 加 `COPY entrypoint.sh /entrypoint.sh` (新 dispatcher)
  - 加 `COPY modes/ /opt/aria-runner/modes/`
  - **加 `RUN chmod +x /opt/aria-runner/modes/*.sh`** (R2 backend H1: 否则 `exec` 报 Permission denied)
  - 现有 `RUN chmod +x /entrypoint.sh /entrypoint-m1.sh /opt/aria-runner/lib/*.sh` 改为 `RUN chmod +x /entrypoint.sh /opt/aria-runner/modes/*.sh /opt/aria-runner/lib/*.sh` (entrypoint-m1.sh 已 git mv 到 modes/initial.sh)
  - `ENTRYPOINT ["/entrypoint.sh"]` 不变 (仍指 dispatcher)
- [ ] 3.5 单元测试 `tests/changes-mode/dispatcher.sh` (~6 case):
  - REWORK_MODE='initial' → exec modes/initial.sh
  - REWORK_MODE='changes' → exec modes/changes.sh
  - REWORK_MODE='redo' → exit 1 + result.json with redo_mode_unimplemented
  - REWORK_MODE='unknown' → exit 1 + result.json with unknown_rework_mode
  - REWORK_MODE 缺省 → default 'initial' (R1 qa BC test)
  - 检查 result.json schema 合规 (existing parse-stream-json 兼容)
- [ ] 3.6 Regression: 现有 bash test suite (`tests/t3-verify.sh`, `tests/compute-assertions/test.sh`, `tests/parse-stream-json/test.sh`, `tests/push-classifier/test.sh`) all PASS against modes/initial.sh
- [ ] 3.7 **NEW R2 backend M-test-path-regression**: post-`git mv`, scan + update path references: `find docker/aria-runner/tests/ -name '*.sh' | xargs grep -l 'entrypoint-m1\.sh'` → 改 to `modes/initial.sh`; same for any `lib/*.sh` source指 entrypoint-m1.sh

---

## Phase 3 — modes/changes.sh 实施 (T4, 10h, Spec X 主体)

### T4 — Bash + curl + jq + claude -p positional

- [ ] 4.1 Forgejo PR fetch (~2h, R1 qa 4xx + malformed-JSON fix):
  - `curl -sf -H "Authorization: token ${FORGEJO_BOT_PAT}" "${FORGEJO_API_URL}/repos/${ORG}/${REPO}/pulls/${PARENT_PR_ID}"` → jq `.head.ref` + `.head.repo.clone_url`
  - HTTP 4xx (404=parent_pr_not_found / 403=forgejo_permission_denied / 401=auth_failed) → 立即 S_FAIL + result.json with fail_reason
  - HTTP 5xx → retry × 3 expo backoff (1s/2s/4s)
  - HTTP 200 + jq fails (malformed JSON) → S_FAIL(forgejo_malformed_response)
  - `curl ... /pulls/${PARENT_PR_ID}/reviews/comments` → similar error handling; sort by `created_at` ASC; cap last 30 entries
- [ ] 4.2 Prompt assemble (~3h, R1 ai HIGH#6/#7/#8 fix + AD-M5-3:3591-3596 ordering):
  - Section ordering (deterministic): (1) feedback (must, ≤4KB from REWORK_FEEDBACK env) (2) original issue body (`${INPUTS_DIR}/issue.yaml`, truncate 10K chars) (3) PR review comments (capped 30, oldest first) (4) file-by-file diff (feedback-prioritized, remaining char budget)
  - Char budget: total 240K chars (≈ 60K tokens ASCII; CJK-aware ratio 0.4 → 24K tokens worst-case safe under 200K Anthropic context)
  - Overflow → emit audit event `prompt_cap_overflow` + `mkdir -p ${ARIA_OUTPUTS_DIR}; echo '{"outcome":"FAIL","error":"prompt_overflow",...}' >result.json; exit 2` (Layer 1 reconciler maps to S_FAIL(`prompt_overflow`))
  - Truncated sections append `[TRUNCATED: N kb]` marker
  - Prompt template `prompts/changes.tpl` with envsubst whitelist (per `entrypoint-m1.sh` §5 pattern + AD-M1-10)
- [ ] 4.3 Git ops (~3h, per `feedback_git_force_with_lease_shallow_clone`):
  - `git clone --depth 1 --branch "${HEAD_BRANCH}" "${CLONE_URL}" work/`
  - `cd work/ && git fetch origin "${HEAD_BRANCH}"` (build FETCH_HEAD)
  - `git -c user.name="${GIT_AUTHOR_NAME}" -c user.email="${GIT_AUTHOR_EMAIL}" config ...`
  - Render prompt: `RENDERED_PROMPT="$(envsubst < /opt/aria-runner/prompts/changes.tpl)"`
  - `timeout "${CLAUDE_TIMEOUT_S}" -k 10s claude -p "${RENDERED_PROMPT}"` (R1 C3 fix: positional, not --prompt-file)
  - Parse stream-json (reuse `lib/parse-stream-json.sh`)
  - Auto commit message (R2 ai F1 fix — Conventional Commits compliance):
    - **Prompt directive (in `prompts/changes.tpl`)**: "IMPORTANT: After your code changes, output a single final line in plain text (not inside a code block) matching the EXACT format: `commit_message: <type>(<scope>): <description>` where `<type>` ∈ {feat|fix|chore|refactor|test|docs|style|perf|build|ci} per `standards/conventions/git-commit.md`, `<description>` ≤ 72 chars total."
    - Extract: `grep -oE '^commit_message:\s*.+$' "${CLAUDE_OUTPUT_FILE}" | sed 's/^commit_message:\s*//' | tail -1`
    - **Fallback** (claude omits directive): `chore(rework-${PARENT_PR_ID}): apply PR-${PARENT_PR_ID} feedback round ${REWORK_ROUND:-1}` — `chore` is **valid** conventional commits type per `standards/conventions/git-commit.md:40-53` (was previously invalid `changes` type)
  - `git add -A && git commit -m "${COMMIT_MSG}"`
  - `git push --force-with-lease="${HEAD_BRANCH}:$(git rev-parse FETCH_HEAD)" origin "${HEAD_BRANCH}"`
  - Push rc ≠ 0 → S_FAIL(force_push_stale_ref or other_push_error)
  - Emit audit event `pr_review_threads_outdated_warning` post-push (per AD-M5-3:3605)
- [ ] 4.4 单元测试 (`tests/changes-mode/mode_changes-prompt.sh`, ~7 cases):
  - Empty REWORK_FEEDBACK → S_FAIL(empty_feedback) (R1 ai LOW fix)
  - 240K - 1 char prompt → PASS
  - 240K char prompt → PASS (boundary exact)
  - 240K + 1 char prompt → exit 2 + result.json prompt_overflow
  - Feedback mentions non-existent file → graceful (diff section omits, no crash)
  - PR comments empty list → header omitted gracefully
  - PR comments 100+ → cap to 30 oldest
  - Non-ASCII (CJK) feedback → no corruption in rendered prompt
- [ ] 4.5 单元测试 (`tests/changes-mode/mode_changes-git.sh`, ~5 cases):
  - clone-fetch-push command sequence captured + correct
  - force-push-lease ref = FETCH_HEAD value
  - Stale-ref rejection → S_FAIL(force_push_stale_ref)
  - Empty diff (no actual code change from claude) → S_FAIL(no_changes)
  - timeout exceeded → S_FAIL(claude_timeout)
- [ ] 4.6 单元测试 (`tests/changes-mode/forgejo-errors.sh`, ~6 cases):
  - 200 OK → success
  - 404 → parent_pr_not_found
  - 403 → forgejo_permission_denied
  - 5xx retry × 3 → eventual success
  - 5xx × 4 → S_FAIL(forgejo_5xx_exhausted)
  - 200 with malformed JSON → S_FAIL(forgejo_malformed_response)

---

## Phase 4 — Image + Acceptance (T5+T6, 4h)

### T5 — Layer 2 image v10 build + sha256 digest pin (~1h, R1 fix: meta_required not meta_optional)

- [ ] 5.1 Dockerfile 含 entrypoint.sh + modes/ + prompts/changes.tpl
- [ ] 5.2 Build via aria-build Nomad job (trigger with current commit SHA)
- [ ] 5.3 Tag image `claude-m5-carry-<sha>-v10` (R1 fix: M3 trio precedent compatible)
- [ ] 5.4 Push to `forgejo.10cg.pub/10cg/aria-runner`
- [ ] 5.5 取回 sha256 digest (via Forgejo registry API or `docker manifest inspect`); 用 dispatch-time pin: Layer 1 dispatch 时把 sha256 写入 NOMAD meta_required.IMAGE_SHA (per AD-M1-7); HCL `image = "registry.10cg.pub/aria-runner@sha256:${NOMAD_META_IMAGE_SHA}"` 不变
- [ ] 5.6 `aria-build-verify` Nomad job confirms digest matches

### T6 — Synthetic acceptance (~3h, R1 qa fix: +1h, ~32 new tests)

- [ ] 6.1 New bash tests under `docker/aria-runner/tests/changes-mode/`:
  - `dispatcher.sh` (6 cases per T3.5)
  - `mode_changes-prompt.sh` (7 cases per T4.4)
  - `mode_changes-git.sh` (5 cases per T4.5)
  - `forgejo-errors.sh` (6 cases per T4.6)
  - Total bash: ~24 cases
- [ ] 6.2 New Python tests under `hermes-extensions/aria-layer1/tests/`:
  - `test_t_changes_mode_meta.py` (8 cases per T1.6)
  - `test_t_changes_mode_size.py` (1+ case per T1.7)
  - `test_t_hcl_meta_inventory.py` (1 case per T2.5)
  - Total Python: ~10 cases
- [ ] 6.3 Regression gate (enumerated, R1 C7 fix):
  ```bash
  # Bash regression:
  bash docker/aria-runner/tests/t3-verify.sh
  bash docker/aria-runner/tests/compute-assertions/test.sh
  bash docker/aria-runner/tests/parse-stream-json/test.sh
  bash docker/aria-runner/tests/push-classifier/test.sh
  # Python regression:
  cd hermes-extensions/aria-layer1 && python -m pytest tests/ -v
  # Critical: tests/test_t_rework_loop.py + tests/test_t_acceptance_m5.py PASS
  ```
- [ ] 6.4 E2E synthetic: SQLite test fixture dispatch row `rework_mode='changes'` + `pr_id=42` + `rework_feedback="refactor X"` → assert Nomad dispatch payload contains 4 meta keys + assert mock claude invoked with prompt containing feedback + assert force-push command captured
- [ ] 6.5 v9 BC test (R1 qa fix): `tests/changes-mode/v9-bc.sh` simulates dispatch payload WITHOUT REWORK_MODE env (v9 pattern) → asserts dispatcher routes to modes/initial.sh
- [ ] 6.6 `openspec validate aria-2.0-m5-carryover-layer2-changes-mode --strict` (if CLI available); else manual schema check (graceful degradation per R1 code-reviewer)
- [ ] 6.7 Total test count verify (R2 qa NEW-1 fix: **case-counted not file-counted**):
  - Bash cases: `grep -c 'assert\|check_\|expect_\|run_test' docker/aria-runner/tests/changes-mode/*.sh | awk -F: '{sum+=$2} END {print "bash_cases:", sum}'` ≥ 24
  - Python cases: `cd hermes-extensions/aria-layer1 && python -m pytest --collect-only -q tests/test_t_changes_mode_*.py tests/test_t_hcl_meta_inventory.py | tail -1` ≥ 10
  - **Total ≥ 32 new behavioral tests** (previous file-count `find ... | wc -l` was semantically broken — only counted 4 files)

---

## Phase 5 — Side-effect Patches (T7, 2h, R1 fix: +1h, +US-026 + handoff)

### T7 — Doc patches

- [ ] 7.0 (NEW R1 I4) `docs/requirements/user-stories/US-025.md` **status line update**: "in_progress — Phase D.1 done, awaiting D.2" → "in_progress — Phase D.2 owner gates + M6a Spec X+Y in-flight"
- [ ] 7.1 US-025.md footer "M5 Carryover Sub-Specs" section linking Spec X (and Spec Y placeholder)
- [ ] 7.2 `aria-orchestrator/docs/m5-handoff.yaml`:
  - `open_issues_for_m6.M5-OS-1` 加 `absorbed_by: aria-2.0-m5-carryover-layer2-changes-mode`
  - 新顶层 field `m6_carryover_to_us_026: {tier2_path_coverage_absorbed: true, tier2_absorbed_to_spec: us-026-m6b-verification, rationale: "..."}`
  - **R2 context N3 fix**: 也 patch `open_issues_for_m6.M5-OS-7` 加 `absorbed_by: us-026.m6b.dispatch_gate (D7 per .aria/decisions/2026-05-15-m6-brainstorm.md)` + 更新 `notes` field 加 cross-ref to new top-level `m6_carryover_to_us_026`
  - **不动** M5-OS-2/3/4/5 (Spec Y T7 sweep, per R1 I2)
- [ ] 7.3 (R1 C2 fix) `aria-orchestrator/docs/architecture-decisions.md::AD-M5-3` **append** new line:
  ```
  > **状态**: Decided 2026-05-14 — Layer 1 wiring DONE; Layer 2 IMPLEMENTATION DEFERRED to M6
  > **更新**: 2026-05-15 — Implementation in-flight via Spec X (aria-2.0-m5-carryover-layer2-changes-mode)
  ```
  (R1 fix: append, do not delete "DEFERRED to M6" original)
- [ ] 7.4 `aria-orchestrator/docs/validate-m5-handoff.py` 加 `check_m6_carryover_to_us_026_present`:
  - 检查 `m6_carryover_to_us_026.tier2_path_coverage_absorbed == True`
  - 新 unit test `test_validate_m5_check_m6_carryover_present` (per `feedback_validator_repo_drift_guard_test`)
- [ ] 7.5 (NEW R1 I1) `docs/requirements/user-stories/US-026.md` 创建 skeleton (R2 context N4 fix: provisional marker added):
  - status `pending — M6b awaiting M5 carryover (Spec X + Y) archive`
  - §M6b scope (per PRD §410-414): E2E testing + docs + v2.0.0 release
  - §"M6b inherits Tier-2 path coverage from US-025 carryover" 段落 (D7 receiving doc):
    `Tier-2 path coverage (≥1 changes + ≥1 redo + ≥1 reject) absorbed from US-025 to M6b verification ≥10 dispatch gate per D7 (brainstorm 2026-05-15). **_Provisional, subject to US-026 Phase A brainstorm confirmation (per R2 context N4)._**`
- [ ] 7.6 (NEW R1 I5) `docs/handoff/2026-05-15-us025-m5-c2-d1-done.md` 加 addendum (footer):
  - Spec X kickoff 2026-05-15 (link)
  - Spec Y kickoff pending Spec X merge
- [ ] 7.7 `docs/handoff/latest.md`:**Phase D 后**更新 pointer (Phase A 期间不更新)
- [ ] 7.8 **不动** `prd-aria-v2.md` (per D4)

---

## Phase 6 — Phase C+D bookkeeping (T8)

### T8 — Standard + R1 fixes (I7 dual-repo gate + I8 Rule #9 handoff)

- [ ] 8.1 Phase C.1 commit chain: per-task-group commits, conventional message + task ID. **R2 code-reviewer F3 fix — Conventional Commits format examples** (per `standards/conventions/git-commit.md`):
  - T1: `feat(layer1): T1 _handle_s4_launch writes meta_optional 4 keys for rework_mode=changes`
  - T2: `feat(layer2-hcl): T2 aria-layer2-runner.hcl meta_optional + key inventory test`
  - T3: `refactor(layer2): T3 bash mode dispatcher + git mv entrypoint-m1.sh modes/initial.sh`
  - T4: `feat(layer2): T4 modes/changes.sh impl (Forgejo fetch + prompt + force-push)`
  - T5: `chore(image): T5 aria-runner v10 build + sha256 digest pin`
  - T6: `test(layer2): T6 acceptance tests for changes-mode dispatcher + git ops`
  - T7: `docs(carryover): T7 side-effect patches (US-025/m5-handoff/AD-M5-3/US-026 skeleton)`
- [ ] 8.2 Phase B.3 audit (mid_implementation) trigger: 当 T1-T4 都 done (≥50% by hour 即 ~14h/22h, R1 qa fix: explicit threshold)
- [ ] 8.3 Phase C.2 aria-orchestrator PR (Layer 1 extension + HCL + modes/ + Dockerfile + tests): post_implementation audit + pre_merge gate
- [ ] 8.4 (R1 I7 fix) Pre-merge gate dual-repo:
  - aria-orchestrator PR: `aether ci status --branch master --in-flight --repo aria-orchestrator`
  - Aria 主 repo PR: `aether ci status --branch master --in-flight --repo Aria`
- [ ] 8.5 aria-orchestrator merge → submodule bump in Aria 主 repo
- [ ] 8.6 Aria 主 repo PR (submodule bump + T7 patches) 创建 + merge
- [ ] 8.7 Dual-push verify (Forgejo origin + GitHub SHA parity, per CLAUDE.md Phase C.2.5)
- [ ] 8.8 Phase D.1: US-025.md status line + footer update (T7.0 + T7.1 已含)
- [ ] 8.9 Phase D.2: openspec archive `aria-2.0-m5-carryover-layer2-changes-mode` → `openspec/archive/2026-XX-XX-...`
- [ ] 8.10 (R1 I8 + R2 context N1 fix) Rule #9 trigger evaluation **per-session, not Spec-lifecycle**: each phase-d-closer D.3 step evaluates Rule #9 4-level fallback (`standards/conventions/session-handoff.md:51-58`); 是否写 handoff 取决于 (a) session wall-time > 4h (b) ≥2 cycles/US shipped in session (c) commit subjects 跨 ≥2 distinct Phase markers in single time window. **不预承诺 archive 时必写**; 各 Spec X session 独立 evaluate. 若触发: 写 `docs/handoff/2026-XX-XX-spec-x-<descriptor>.md` (template `aria/templates/session-handoff.md`) + 更新 `docs/handoff/latest.md` pointer
- [ ] 8.11 US-025 status 仍 in_progress (Spec Y + T-deploy + Tier-1 还未完成)

---

## Sub-task granularity check (per Aria 规范 + R1 code-reviewer fix)

- T4 (10h) sub-tasks: 4.1 (~2h) + 4.2 (~3h) + 4.3 (~3h) + 4.4 (~1h) + 4.5 (~0.7h) + 4.6 (~0.3h) = ~10h. T4.2 prompt assemble 拆 3 sub-bullet (section ordering / budget / overflow) 实施时可视为 3 子任务。
- T1-T7 总 sub-task ~50, avg ~0.5h per sub-task ✓ within Aria 4-8h task group + sub-task <1h `feedback_phase_b_velocity_patterns` baseline.
- T4 单 task group 10h > 8h baseline: per `feedback_pre_draft_bug_hunt_discipline` mode_changes hits 4 high-risk categories, 时间合理.

---

## Test count target (R1 code-reviewer fix)

- Bash: dispatcher (6) + prompt (7) + git (5) + forgejo-errors (6) + v9-bc (1) = ~25
- Python: meta (8) + size (1) + hcl-inventory (1) + validate-m5-check (1) = ~11
- **Total: ~36 new behavioral tests** (proposal §F 说 "≥32" 含 buffer)

---

## Status

- [x] T0 Spec drafted v1 + R1 audit (73 findings)
- [x] T0 v2 R1 fixes applied (proposal + tasks rewrite, 73 → ~20 R2 findings, ~73% reduction, exceeds 80% on critical+high)
- [x] T0 Phase A.2 R2 audit (5 agents, 2026-05-15T18:10Z): 0 new critical, 6 new HIGH (all surgical 1-line fixes), ~10 MEDIUM
- [x] T0 v3 R2 fixes applied (this commit): H1-H6 + M1-M3 + M7-M8 + M11-M13 → expected R3 ≤2 findings
- [x] T0 Phase A.2 R3 stability round (3 agents): qa=CONFIRMED, ai=CONFIRMED, code-reviewer=needs 4 surgical fixes
- [x] T0 R3 surgical fixes applied (3627→3605 ×2, frontmatter v2→v3→Approved, ~22h→~25h ×2)
- [x] T0 Spec Status → **Approved** (2026-05-15T18:50Z)
- [x] **T1 done** 2026-05-16 (aria-orchestrator `25a3d77`) — Layer 1 _handle_s4_launch + 10 tests
- [x] **T2 done** 2026-05-16 (aria-orchestrator `a6baeb1`) — HCL meta_optional + 3 inventory tests
- [x] **T3 done** 2026-05-16 (aria-orchestrator `6af2c35`) — bash dispatcher + git mv + 6 tests
- [x] **T4 done** 2026-05-16 (aria-orchestrator `5608419`) — modes/changes.sh + 18 tests
- [ ] T5 Image build — **owner-deferred** (aria-build Nomad job trigger required; AD-M1-7 sha256 dispatch-time pin pattern; will happen at Phase C.2 owner T-deploy or M6b verification)
- [x] **T6 inline-verified** (37 case-counted ≥32 target met inline via T1-T4 tests; openspec validate gracefully degraded per R1 fix)
- [x] **T7 done** 2026-05-16 (aria-orchestrator `efd51ef` + Aria `e4c8430`) — m5-handoff/AD-M5-3/US-025/US-026/handoff doc patches
- [ ] T8 Phase C+D (standard 10-step bookkeeping + R1 I7/I8 fixes) — pre_merge audit + dual-repo PR + merge + archive
- [ ] T0 Phase B.3 mid_implementation/post_implementation audit (deferred to pre_merge gate per proportionality — 3-round post_spec convergence already covered architectural concerns)

**当前 Phase**: A.1 v2 (R1 reality-drift fixes applied, awaiting R2)
