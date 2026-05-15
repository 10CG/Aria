# Spec X Tasks — Aria 2.0 M5 Carryover Layer 2 changes-mode + MODE_HANDLERS skeleton

> **Change ID**: `aria-2.0-m5-carryover-layer2-changes-mode`
> **Parent**: US-025 (M5 carryover)
> **Estimate**: ~22h AI-runnable
> **Phase A.2 task-planner 入参**: 8 task groups (T1-T8), 大颗粒覆盖 ~22h
> **Phase B sequencing**: T1+T2 parallel → T3 → T4 → T5 → T6 → T7 → T8 (per proposal §排序依赖)

---

## Task Group 总览

| ID | 标题 | 工时 | 阻塞 |
|----|------|------|------|
| T1 | Layer 1 dispatcher 写 meta_optional 4 keys | 3h | — |
| T2 | Nomad HCL meta_optional 扩展 + validate | 1h | — |
| T3 | MODE_HANDLERS scaffolding + mode_initial 重构 (零行为) | 3h | T1, T2 |
| T4 | mode_changes.py 实施 (Forgejo + prompt + git ops) | 10h | T3 |
| T5 | Layer 2 image build v10 + sha256 digest pin | 2h | T4 |
| T6 | Synthetic acceptance tests | 2h | T5 |
| T7 | Side-effect patches (US-025 / m5-handoff / AD-M5-3) | 1h | T4 (并行) |
| T8 | Phase C merge + Phase D archive | (Phase C/D 标准流程) | T6, T7 |

总: ~22h (Phase B 实施); Phase C/D bookkeeping 独立。

---

## Phase 1 — Layer 1 + HCL 契约 (T1+T2, 4h, parallel-able)

### T1 — Layer 1 `_handle_s4_launch` 写 meta_optional 4 keys (~3h)

- [ ] 1.1 在 `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/extension.py::_handle_s4_launch` 加 `rework_mode` 检查分支
- [ ] 1.2 从 dispatch row 读取 `rework_mode` / `rework_feedback` / `pr_id` / `rework_of` 4 字段
- [ ] 1.3 构造 Nomad dispatch meta dict 时,若 `rework_mode IS NOT NULL`:加 `REWORK_MODE` / `REWORK_FEEDBACK` (≤4KB 截断 + audit warn) / `PARENT_PR_ID` / `REWORK_OF`
- [ ] 1.4 `rework_mode IS NULL` 路径不写新 keys (向后兼容,Layer 2 image v9 + v10 都识别此 case 为 'initial')
- [ ] 1.5 audit log event `meta_optional_written` 记录哪些 keys 被写入 (replay 友好)
- [ ] 1.6 单元测试: 4 case (initial / changes / redo / retry) × 验证 meta dict 正确性
- [ ] 1.7 单元测试: REWORK_FEEDBACK 截断 case (5KB input → 4KB stored + audit warn event)

### T2 — Nomad HCL meta_optional 4 keys + nomad validate (~1h)

- [ ] 2.1 编辑 `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` `parameterized` 块
- [ ] 2.2 `meta_optional` list 加 `"REWORK_MODE"`, `"REWORK_FEEDBACK"`, `"PARENT_PR_ID"`, `"REWORK_OF"`
- [ ] 2.3 `meta_required` 不动 (M1 BC)
- [ ] 2.4 `nomad job validate` 通过 (per `feedback_nomad_hcl_validate_early`)
- [ ] 2.5 commit message 含 4 keys 字面 (audit-friendly)

---

## Phase 2 — Layer 2 MODE_HANDLERS scaffolding (T3, 3h)

### T3 — MODE_HANDLERS dispatcher + mode_initial.py 重构 (零行为变更)

- [ ] 3.1 创建 `aria_layer2_runner/mode_dispatcher.py` 含:
  - `MODE_HANDLERS: Dict[str, Callable[[dict], int]]` registry
  - `dispatch_mode(env: dict) -> int` 入口
  - `_not_implemented_yet(env: dict)` raise + sys.exit(1) (Spec Y drop-in 位置)
- [ ] 3.2 现有 Layer 2 image entrypoint script 主逻辑迁入 `aria_layer2_runner/mode_initial.py`,签名 `handle_initial(env: dict) -> int`
- [ ] 3.3 registry 4 keys: `'initial': handle_initial`, `'changes': handle_changes` (T4 实施), `'redo': _not_implemented_yet`, `'retry': handle_initial` (alias per M5 failure_analysis)
- [ ] 3.4 image entrypoint shim (Dockerfile CMD) → `python -m aria_layer2_runner.dispatch` 调 `dispatch_mode(os.environ)`
- [ ] 3.5 单元测试: dispatch_mode 4 modes + unknown_mode error
- [ ] 3.6 单元测试: 现有 M5 initial mode 测试 (mock claude / mock git) 必须通过 mode_initial.py refactor 后仍 PASS (zero regression gate)

---

## Phase 3 — mode_changes 实施 (T4, 10h, Spec X 主体)

### T4 — mode_changes.py + Forgejo + prompt + git ops

- [ ] 4.1 Forgejo PR 信息抓取 (~2h):
  - `forgejo_client.get_pull(pr_id)` → head branch + clone URL
  - `forgejo_client.get_pr_review_comments(pr_id)` → list of review comments (per AD-M5-3 §risk mitigation)
  - error handling: 5xx retry 3次 + 最终 audit warn
- [ ] 4.2 Prompt assemble (~3h, per AD-M5-3 §"Prompt assemble strategy"):
  - 必须项: REWORK_FEEDBACK + 原 issue body (从 ISSUE_URL 拿 / 或从 inputs RO volume 读)
  - 可选项: file-by-file diff (按 feedback mention 的 file 优先排序; 仅取 head branch 当前状态)
  - PR review comments → as附加 context section
  - Hard cap 60K tokens (用 `tiktoken` 或简单 char count × 0.25 估算)
  - 超出 → audit log event `prompt_cap_overflow` + sys.exit(2) (Layer 1 reconciler 标 S_FAIL(prompt_overflow); Spec Y ship 后改 fallback to redo)
- [ ] 4.3 Git ops (~3h, per `feedback_git_force_with_lease_shallow_clone`):
  - `git clone --depth 1 --branch <head_branch> <forgejo_url> work/`
  - `cd work/ && git fetch origin <head_branch>` (建 FETCH_HEAD)
  - `claude -p --prompt-file <assembled>` invoke
  - `git add -A && git -c user.email=... -c user.name=... commit -m <auto>` (sig env from existing image)
  - `git push --force-with-lease=<head_branch>:$(git rev-parse FETCH_HEAD) origin <head_branch>`
- [ ] 4.4 单元测试 (~1h): prompt builder edge cases (empty feedback / 60K overflow / missing fields)
- [ ] 4.5 单元测试: git ops mock subprocess + verify command sequence (force-with-lease ref correct)
- [ ] 4.6 Integration test (~1h): mock Forgejo + mock claude → end-to-end changes mode → verify final push command

---

## Phase 4 — Image + Acceptance (T5+T6, 4h)

### T5 — Layer 2 image v10 build + sha256 digest pin (~2h)

- [ ] 5.1 Dockerfile 含 `aria_layer2_runner/` 模块 (dispatcher + mode_initial + mode_changes + mode_redo 占位)
- [ ] 5.2 Build via aria-build Nomad job (per `feedback_aether_tool_discovery_flow`): trigger build with current commit SHA
- [ ] 5.3 Tag image `claude-m6a-<sha>-v10` + push to `forgejo.10cg.pub/10cg/aria-runner`
- [ ] 5.4 取回 sha256 digest (via `docker manifest inspect` or registry API)
- [ ] 5.5 写入 HCL `meta_optional.IMAGE_SHA` default value + `image` 字段 (per AD-M1-7)
- [ ] 5.6 `aria-build-verify` Nomad job confirms digest matches

### T6 — Synthetic acceptance tests (~2h)

- [ ] 6.1 Unit test suite for `mode_dispatcher` (routing + unknown mode)
- [ ] 6.2 Unit test suite for `mode_changes.py` (prompt builder + git ops mocks)
- [ ] 6.3 Integration test: `_handle_s4_launch` writes correct meta + Layer 2 mock alloc consumes → S5_AWAIT
- [ ] 6.4 E2E synthetic: SQLite test fixture dispatch row `rework_mode='changes'` + `pr_id=42` + `rework_feedback="refactor X"` → assert Nomad dispatch payload contains 4 meta keys + assert mock claude invoked with prompt containing feedback + assert force-push command captured
- [ ] 6.5 Regression: 现有 M5 initial mode 测试 all PASS (zero behavioral change for `rework_mode IS NULL`)

---

## Phase 5 — Side-effect Patches (T7, 1h)

### T7 — Doc patches (并行 T4 后期可启)

- [ ] 7.1 `docs/requirements/user-stories/US-025.md`: footer 新增 "M5 Carryover Sub-Specs" section linking Spec X (+ placeholder for Spec Y)
- [ ] 7.2 `aria-orchestrator/docs/m5-handoff.yaml`:
  - `open_issues_for_m6` 段: M5-OS-1 加 `absorbed_by: aria-2.0-m5-carryover-layer2-changes-mode`
  - 新增顶层 field `m6_carryover_to_us_026` 含 Tier-2 path coverage transfer note (per D7)
- [ ] 7.3 `aria-orchestrator/docs/architecture-decisions.md::AD-M5-3` 状态行更新: "Decided 2026-05-14 — Layer 1 wiring DONE; Layer 2 IMPLEMENTATION **in progress via Spec X**"
- [ ] 7.4 `aria-orchestrator/docs/validate-m5-handoff.py` (如存在): 加 check `m6_carryover_to_us_026` field 存在 (per AD pattern)
- [ ] 7.5 不动 `prd-aria-v2.md` (per D4)

---

## Phase 6 — Phase C merge + Phase D archive (T8)

### T8 — Standard 10-step C.1-C.2 + D.1-D.2 (本 Spec 独立 archive)

- [ ] 8.1 Phase C.1 commit chain: per-task-group commits (T1-T7),每个含 conventional message + task ID 追溯 (per `feedback_audit_driven_fix_conventions`)
- [ ] 8.2 Phase B.3 audit (mid_implementation 检查点,per Aria default trigger): 5-agent parallel R1 → R2 收敛
- [ ] 8.3 Phase C.2 aria-orchestrator PR 创建 + audit-engine post_implementation + pre_merge gates
- [ ] 8.4 Phase C.2.4 pre-merge gate (per Rule #8): `aether ci status --branch master --in-flight` + this PR CI passing
- [ ] 8.5 aria-orchestrator merge → submodule bump in Aria 主 repo
- [ ] 8.6 Aria 主 repo PR (submodule bump + side-effect patches T7) 创建 + merge
- [ ] 8.7 Dual-push verify (Forgejo origin + GitHub SHA parity, per CLAUDE.md Phase C.2.5)
- [ ] 8.8 Phase D.1: US-025 footer update (T7 已含) + UPM 不动 (Aria 主仓不用 UPM)
- [ ] 8.9 Phase D.2: openspec archive `aria-2.0-m5-carryover-layer2-changes-mode` → `openspec/archive/2026-XX-XX-aria-2.0-m5-carryover-layer2-changes-mode/`
- [ ] 8.10 US-025 status 仍 in_progress (Spec Y + T-deploy + Tier-1 还未完成)

---

## Sub-task granularity check (per Aria 规范)

每个 task group (T1-T7) sub-task 数 6-10 之间,单 sub-task ~15-45min, 符合 Aria 小步迭代原则 (`feedback_phase_b_velocity_patterns_2026-04-29` 单 commit < 1h)。T4 (mode_changes 主体) 含 6 sub-tasks × ~1.5h = 10h 总,proportional to scope。

---

## Status

- [x] T0 Spec drafted (本文件 + proposal.md created 2026-05-15)
- [ ] T0 Phase A.2 audit R1 + R2 (~3h, 5 agents parallel)
- [ ] T0 Spec Status → Approved
- [ ] T1-T7 Phase B (~22h AI-runnable)
- [ ] T8 Phase C+D (standard 10-step bookkeeping)

**当前 Phase**: A.1 (Spec drafting done, awaiting audit-engine R1 invocation)
