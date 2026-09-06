# M6 Dispatch Input Delivery — Tasks (C' dual-channel)

> **Spec**: [proposal.md](./proposal.md)
> **Level**: 3 (Full)
> **Status**: ✅ Approved (owner sign-off 2026-07-03; Phase A.2 post_spec CONVERGED). Task granularity is functional; A.2 task-planner adds detailed-tasks.yaml with paths/estimates, A.3 assigns agents.
> **Decision Source**: [DEC-20260702-001](../../../docs/decisions/DEC-20260702-001-layer2-input-delivery-architecture.md)
> **Ordering rationale (DEC §落地)**: container code + assertion fix (RED-first) → Layer 1 code (same scope, else ineffective) → key migration → image build/freeze → contract-doc sync → E2E dogfood. Layer 1 (TG-2) and container (TG-1) must ship together; assertion fix (TG-1.C) is RED-first before container fetch is exercised.

---

## Task Group Overview

| Group | Topic | Scope ref |
|-------|-------|-----------|
| TG-1 | Container side: regex + dual-mode input + fetch + sanitization + three-outcome model | §What A + §What C |
| TG-2 | Layer 1 side: additive seed columns + id format + META + ISSUE_URL rebuild + head_branch + outcome-class/INPUT_FETCH_FAILED consumption + acceptance stratify | §What B + §What C.3 |
| TG-3 | Key format value migration + acceptance-query survey | §What D |
| TG-4 | Image rebuild + freeze | §What E |
| TG-5 | Contract + doc sync (AD-M6-10 / AD4-cell correction / AD-M1-4 amend / §5 / CLAUDE.md) | §What F |
| TG-6 | E2E dogfood + pre-run egress live-test | §Acceptance AC-1/AC-3/AC-6 |

> TG-1 and TG-2 are **co-dependent** (regex fires before input load — a container-only ship stays 100% S_FAIL). They land in one integrated change; TG-3/TG-5 can proceed in parallel; **TG-4 (image build) gates on TG-1 only** (only container-side code is baked in; TG-2/TG-3 deploy to Hermes/light-1 separately); TG-6 E2E dogfood gates on TG-1+TG-2+TG-3+TG-4 all deployed.

---

## TG-1 — Container side (initial.sh + compute-assertions.sh)

- [x] 1.1 Align Step 1 ISSUE_ID regex to accept `ARIA-<repo>-<number>` (still reject bare numeric; `DEMO-`/`TEST-` preserved)
- [x] 1.2 Step 2 dual-mode resolution: `DEMO-`/`TEST-` + file-exists → validated file read (non-empty + YAML-parseable, no silent fallback); `ARIA-` → always-fetch (ignore existing file)  <!-- ✅ 补强落地 2026-09-05 (aria-orchestrator feature 分支 9ec1fcc): initial-sh-integration scenario 6 — issue.yaml 缺失/空/非 YAML 三分支各自 die (exit 1 + 专属 FATAL + 未 clone); 反事实删 :460 die → 红。原 2026-08-27 recon 缺口 (缺 file-mode 失败路径测试) 已闭合。 -->
- [x] 1.3 Fetch title/body from `ISSUE_URL` with `FORGEJO_BOT_PAT`; read `target_repo`/`base_branch`/`files_hint` from Nomad META  <!-- ✅ 补强落地 2026-09-05 (9ec1fcc): scenario 1 加 3 断言 — 抓回 body / title / NOMAD_META_FILES_HINT 真进交给 `claude -p` 的 prompt (stub claude 落盘 argv); 反事实 body 换常量 → 红, files_hint 置空 → 红。原 recon 缺口 (body 半边零验证 + files_hint 无测试 + 证据引用不存在的 log) 已闭合。 -->
- [x] 1.4 Fetch validation + retry classification: HTTP 2xx + legitimate JSON (reject CF-Access pseudo-success) + non-empty; retriable (timeout/5xx/429) → bounded backoff; non-retriable (404/401/pseudo-success/empty) → immediate fail (no `|| true`)
- [x] 1.5 Title/body sanitization pipeline: control-char strip (was YAML-safe escape, amended 2026-09-05) + CRLF→LF + length cap + injection isolation; route through existing envsubst whitelist (body not re-expanded)  <!-- ✅ owner 裁定 2026-09-05 选 A (改条文对齐实现): verification「YAML-safe escape」→「控制字符剥离」, 理由 = 数据流经 envsubst 进 markdown 模板, 不经 YAML 解析, 转义无消费方; proposal §A.4/AC-7 + yaml + AD-M6-10 风险 5 同步; initial-sh-unit 加 3 条锁定 (特殊字符原样 / 控制字符剥离 / 反斜杠不加倍), 将来加转义层即红。DEC-20260702-001 为日期化决策记录不改。 -->
- [x] 1.6 `base_branch` from META with Forgejo `default_branch` fallback (never hardcode `master`)
- [x] 1.7 **RED-first** at the real `initial.sh` call-site: reproduce current empty-`expected_changes` false-green; fix compute-assertions to emit `unknown`/`skip` (not `true`) on empty lists (file-mode defense-in-depth)  <!-- ✅ 补强落地 2026-09-05 (9ec1fcc): scenario 7 — file 模式 expected_changes 两空列表走真 initial.sh → hits=unknown / ASSERTION_MISMATCH / exit 1 / 无 SUCCESS marker; 反事实撤销 compute-assertions 空表守卫 → 5 断言红 (原 false-green 复现)。RED-at-real-call-site 要求已满足。 -->
- [x] 1.8 Fetch mode **skips** the `compute-assertions.sh` call entirely; wire the skip at `initial.sh:513-515`. (Mechanism, corrected by mid_post_spec dogfood 2026-07-04: the call at `:514` has `| tail -5 || true` under `set -euo pipefail` — compute-assertions.sh's `exit 1` at `:37` is **swallowed**, container does NOT die there; real dead-end is `FILE_TOUCHED_HIT`/`DIFF_CONTAINS_HIT` defaulting `false` at `:517-518` → 5-AND fail → `ASSERTION_MISMATCH` `:534` → `exit 1` `:595` → `S_FAIL`. Skip avoids this dead-end.)  <!-- ✅ 补强落地 2026-09-05 (9ec1fcc): scenario 1 原「assertion-results.json NEVER created」断言实证为重言式 (撤销 skip 仍绿), 换为 SKIPPED 日志行存在 + `issue yaml not found` 不泄漏两条; 反事实调用点守卫改 `__NEVER__` → 2 红。 -->
- [x] 1.9 Define `AUTONOMOUS_COMPLETED` outcome (fetch mode) = `claude_exit==0 AND commit AND PR` (no file/diff hits); map to `exit 0`  <!-- ✅ 补强落地 2026-09-05 (9ec1fcc): scenario 8 (ARIA_TEST_CLAUDE_NO_OP 无 commit → CLAUDE_NO_OP / exit 1 / 无 AUTONOMOUS_COMPLETED marker) + scenario 9 (PR 创建失败 → PR_CREATE_FAILURE / exit 1 / 无 marker) + unit compute_fetch_mode_outcome 4 例。注: recon 建议断 ASSERTION_MISMATCH 与实现不符 — 无 commit 在 Step 8 先判 CLAUDE_NO_OP (PENDING 才走三条件函数), 按实况断言。 -->
- [x] 1.10 Emit the outcome-**class** stderr marker on the channel Layer 1 reads (cf. `redo.sh` precedent, consumed via `get_alloc_logs`): on success distinguish `AUTONOMOUS_COMPLETED` vs file-mode `SUCCESS`; on fetch failure emit `INPUT_FETCH_FAILED` + `exit 1`. (Do **not** rely on `result.json` — Layer 1 never reads it and it is on cross-node-unreadable storage.)

## TG-2 — Layer 1 side (extension.py + schema migration)

- [x] 2.1 Add additive nullable columns (`migrations/00N_schema_vN_additive.sql` pattern, M3/M4/M5 precedent): `raw_issue_number` / `target_repo` / `base_branch` / `files_hint` (+ optional `outcome_class`); seed (`_phase1_scan_and_seed`) writes them
- [x] 2.2 Dispatch `ISSUE_ID = ARIA-<repo>-<number>` (letter-prefixed, issue number not internal id, repo component anti-collision)
- [x] 2.3 Extend Nomad META builder with `target_repo` / `base_branch` / `files_hint` read from the persisted columns (2.1) via `dispatch_row` — not global env  <!-- ✅ 补强落地 2026-09-05 (9ec1fcc): HCL meta_optional 补 TARGET_REPO/BASE_BRANCH/FILES_HINT (`nomad job validate` 过); test_t_hcl_meta_inventory 加 M6 三键断言 + 结构性 fence (extension.py 全部 extra_meta 键 ⊆ HCL 声明); 反事实 HCL 去 FILES_HINT → 2 红。原 recon 缺口 (Layer 1 写、HCL 未声明 ⇒ Nomad 拒 dispatch) 已闭合。 -->
- [x] 2.4 **Rebuild `ISSUE_URL`** = `{target_repo}/issues/{raw_issue_number}` from the persisted columns (do NOT parse the composite `issue_id`, do NOT use hardcoded `FORGEJO_ORG`/`FORGEJO_REPO`); fixes the current internal-id + hardcoded-repo construction (`extension.py:1176/2147-2152`)
- [x] 2.5 Unify `head_branch = aria/{issue_id}` with container `BRANCH` under new scheme (preserve S6_REVIEW PR binding)
- [x] 2.6 Add `FailReason.INPUT_FETCH_FAILED` (`interfaces.py`); in `_handle_s5_await` (`extension.py:2593-2640`) consume the container outcome-class marker via `get_alloc_logs()`: `exit_code!=0` → route `INPUT_FETCH_FAILED` distinct from `CONTAINER_CRASH`; `exit_code==0` → record `outcome_class` (`AUTONOMOUS_COMPLETED` vs `SUCCESS`) into DB (**single carrier** — additive column preferred over audit payload). **Fail-closed**: marker absent/malformed on `exit 0` → `outcome_class=UNKNOWN` (not `SUCCESS`); fixture covers absent + malformed
- [x] 2.7 Make Spec #2's acceptance query (`check-m6-e2e-acceptance.py`) outcome-class-aware: `AUTONOMOUS_COMPLETED` excluded from verified-SUCCESS counts / stratified (cross-Spec coordination)

## TG-3 — Key format migration + query survey

- [x] 3.1 Reformat `issue_id` **value** to `ARIA-<repo>-<number>` (value-level; the **key** is not restructured — composite embedded in TEXT, partial-unique-active invariant preserved). Distinct from the additive input columns of TG-2.1 (those are separate additive migrations, not a key change).
- [x] 3.2 Decide + document clean-DB vs historical-migration for existing `issue_id` rows. **DECISION (Phase B.2, 2026-07-04): forward-only reformat, NO backfill / NO historical migration.** Rationale: `issue_id` is opaque TEXT everywhere (per §3.3 survey); old-format autonomous rows are already terminal (per #147 pre-flight — all S_FAIL), so the partial-unique-active invariant is unaffected; new dispatches emit `ARIA-<repo>-<number>`, historical rows retain old format + degrade gracefully (NULL additive columns tolerated). Recorded in migration `008_schema_v5.1_additive.sql` header.
- [x] 3.3 Survey every acceptance/dispatch query keying on `issue_id`; confirm new-format tolerance; verify #147 issue_type_hint stratification (json_extract path) unaffected  <!-- ✅ 补强落地 2026-09-05 (9ec1fcc): 普查漏掉的 extension.py 已修 — _handle_s1_scan 按内部 id 键候选而 seed 已是复合键 (幂等守卫失效 / is_self 恒假 / S2_DECIDE 载荷把复合键覆写成裸数字); 抽 `_compose_dispatch_issue_id` 单一 helper 两处共用; 新增 6 例 (id≠number 夹具), 修前 3 FAIL + 3 ERROR, 修后 6 过。 -->

## TG-4 — Image rebuild + freeze

- [ ] 4.1 Rebuild `aria-runner` via `aether-build-container` after **TG-1** lands (only container-side code is baked into the image; TG-2/TG-3 are Hermes/light-1 side, deployed separately); push to internal registry  <!-- ⚠️ 部分完成 TASK-021: 需要 owner 实际触发 /aether:aether-build-container (或手工 docker build) 对 post-merge master SHA 构建镜像并 push 到 forgejo.10cg.pub/10cg/aria-ru -->
- [ ] 4.2 Capture immutable `image_sha256`; freeze single `IMAGE_SHA` for the 168h run; record rollback (old sha)

## TG-5 — Contract + doc sync (Rule #3)

- [x] 5.1 Write **AD-M6-10** (six-section: decision/background/alternatives/rationale/risks/rollback); include single-node scope of the bind-mount input assumption  <!-- ✅ owner 裁定 2026-09-05 选 A (只改论据不改决定): AD-M6-10 背景第 1 点 + Alternatives D 格「heavy 卷本地 ext4 非 NFS」勘正为实况 (三 heavy guest 共享 virtiofs over NFS, R8 + storage-validation-report md5 一致; host-volume.hcl 不含文件系统类型); D 仍被否的三条理由 (写方 light-1 不在树上 / stale-read 面 / 逆节点无关哲学+单点) 前两条独立于 heavy 侧共享; proposal §Alternatives D 行同步。六段结构 + 单节点作用域声明本就成立。 -->
- [x] 5.2 **Correct the AD4 risk-table cell** (`architecture-decisions.md:384`): fix the "AD-M0-5 约定" mislabel + scope bind-mount premise to single-node + xref AD-M6-10. **Do NOT touch the AD-M0-5 body** (`:1035`, m0-handoff schema — unrelated)
- [x] 5.3 **Amend AD-M1-4**: scope 5-AND SUCCESS to file mode; document `AUTONOMOUS_COMPLETED` + `INPUT_FETCH_FAILED`. **Caveat (R2 km):** the AD-M1-4 body (`architecture-decisions.md:1360`) has pre-existing doc/code drift (records a 9-enum/6-AND `entrypoint-m1.sh` version vs the current 5-AND `initial.sh:524`) — verify the AD's current literal content before editing to avoid conflating the two generations.
- [x] 5.4 Add `layer-boundary-contract.md §5 "Task Content Delivery Mechanism"` (dual-channel field schema + file-mode lifecycle)
- [x] 5.5 Update CLAUDE.md M6 status section: record input-delivery ↔ telemetry dependency chain (fetch-before-edit; high-contention region)

## TG-6 — E2E dogfood + pre-run verification

- [x] 6.1 Live-test heavy-node Forgejo egress/auth (fetch reachability) before any run  <!-- ✅ 完成 2026-09-02 (TASK-028): heavy-node 实测双腿 PASS — 内网 issue/repo GET 200 合法 JSON (非 CF-Access 伪成功) + git ls-remote rc=0 + push --dry-run rc=0 (write:repository 实证)。新 token aria-layer2-git-2026-Q3 (owner 2026-09-02 签, 台账 .aria/pat-inventory.yaml); 08-29 首测曾 FAIL (旧 PAT 死)。证据: .aria/notes/2026-08-29-m6-blocker4-recheck-and-task028-egress-probe.md §2.7 -->
- [ ] 6.2 E2E dogfood: real numeric-id autonomous dispatch → S9_CLOSE with merged PR (AC-1)
- [x] 6.3 Verify fetch-failure classes distinguishable to Layer 1 as infra-fail vs agent-fail (AC-6)

---

## Notes

- **Not in this Spec** (explicit dependency edge): container → Layer 1 cost/model telemetry (separate Spec; the 168h run is not scorable for AC-6 until that ships).
- **Sequencing**: this Spec is a precondition to Spec #2's *operational* 168h run, not to Spec #2's code (already shipped 2026-06-02).
- **Phase A.3** will assign agents (no new agent expected — existing roster: backend-architect / qa-engineer / knowledge-manager cover container/assertion/contract-doc work).
