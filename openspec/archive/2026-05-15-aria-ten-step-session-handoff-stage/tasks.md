# Tasks — H0 aria-ten-step-session-handoff-stage

> Parent: [proposal.md](./proposal.md) | **Status**: **Complete** 2026-05-15 — all T1-T8 shipped via 3-PR sequenced merge + v1.21.0 release

## Phase B Tasks (按依赖顺序)

### T1 — `collectors/handoff.py` + snapshot.handoff field (Layer 2) (~4h)

- [ ] **T1.1** New file `aria/skills/state-scanner/scripts/collectors/handoff.py`:
  - Stdlib-only (Python 3, no deps per scan.py contract)
  - Scan `docs/handoff/*.md` by mtime DESC,取 latest
  - Compute `age_hours = (time.time() - mtime) / 3600` (UTC epoch float;F8 minor — 不用 `datetime.now()` 防 timezone/DST)
  - Detect `.aria/handoff/*.md` 存在 → 列入 `misplaced_files` (return list of relative paths)
  - Return dict: `{exists: bool, latest_path: str|null, latest_filename: str|null, last_modified_iso: str|null, age_hours: float|null, misplaced_files: list, canonical_dir: "docs/handoff/"}`
  - Empty `docs/handoff/` edge: `exists=false, latest_path=null`, but still emit `misplaced_files` correctly
  - **No version bump** — additive top-level field per Aria precedent (v1.18.0 G2/G3/G4)
- [ ] **T1.2** Edit `aria/skills/state-scanner/scripts/scan.py`:
  - Import + invoke `collectors.handoff`
  - Add to snapshot top-level `handoff` key
  - **不修改 `snapshot_schema_version`** — 保持 `"1.0"` (F1 fix per R1 backend-C1 + qa-C1: additive 不 bump)
- [ ] **T1.3** Edit `aria/skills/state-scanner/scripts/collectors/__init__.py`:
  - Register new `handoff` module in `__all__` (per existing collector convention)
- [ ] **T1.4** Edit `aria/skills/state-scanner/references/state-snapshot-schema.md`:
  - Document `handoff` field schema (7 keys above)
  - **不**新增 Versioning entry (schema 仍 1.0,additive 字段在 1.0 内 listed)
  - 在现有 §Fields 表加 `handoff` row
- [ ] **T1.5** Edit `aria/skills/state-scanner/SKILL.md`:
  - 阶段 1.x 子阶段表加 `handoff` (Phase 1.15)
  - **不**修改阶段 2 入口断言 (schema 仍 "1.0",SKILL.md line 155 hardcoded check 继续通过)
  - "完整性兜底" 段加 handoff sanity check (`upm.configured == false` 时 fallback 用 `handoff.latest_path` 作为 inter-cycle 信号源)

### T2 — `phase-d-closer` D.3 + template (Layer 5) (~4h)

- [ ] **T2.1** New file `aria/templates/session-handoff.md`:
  - **9 段骨架** (F4 fix per R1 knowledge-M1 — 加 §8 memory entries):
    - §0 入口 (强调下次 session 用 state-scanner 进入)
    - §1 已完成 (按时间顺序, 含 commit hash)
    - §2 未完成/carry-forward (按 P1/P2/P3 优先级)
    - §3 关键风险点 / 已知陷阱
    - §4 实战教训 (memory 沉淀来源)
    - §5 4 维度同步 (PRD/User Story/OpenSpec/UPM 或对应外部系统)
    - §6 Next session 入口 + 优先级建议
    - §7 提交清单 (commit hash + multi-remote parity)
    - **§8 Memory entries this session** (auto-memory 新增列表 — Aria 实证 必含)
  - Variables: `{cycle_name}`, `{date}`, `{session_duration}`, `{shipped_cycles}` 等
  - 参考 Aria `docs/handoff/2026-05-13-us025-m5-phase-a-b1-done.md` 实战版 (§Memory entries 在 line 145)
- [ ] **T2.2** Edit `aria/skills/phase-d-closer/SKILL.md`:
  - 加 §D.3 session-handoff step
  - **触发条件信号 fallback 层级** (F2 fix per R1 backend-M1):
    1. Primary: `.aria/workflow-state.json::session.started_at` if active workflow → 计算 elapsed → check > 4h
    2. Secondary (cycles count): `git log` since last `docs/handoff/*.md` mtime,count cycle archive entries created in window → check ≥ 2
    3. Tertiary (phase count): count distinct phase markers in commits since last handoff (look for `Phase {A,B,C,D}` substring in commit subjects) → check ≥ 2
    4. Fallback: prompt user "本 session 是否符合 D.3 触发条件 (跨度 > 4h / ship ≥ 2 cycles / 跨 ≥ 2 phases)?" — default `yes` if Phase D 执行到 D.2 archive 成功 (一般 D.2 ship 已意味本 session 完整闭环 1 cycle,prompt 用户确认)
  - 输出路径硬编码: `docs/handoff/{YYYY-MM-DD}-{slug}.md` (slug = 用户提供 OR cycle change_id 后缀)
  - 同日重名 fallback: `{YYYY-MM-DD}-{HHMM}-{slug}.md`
  - 自动更新 `docs/handoff/latest.md` pointer 到新 doc
  - 关闭条件: 用户拒绝写 (D.3 是 optional, 触发条件 met 时 prompt 而非强制)
- [ ] **T2.3** Edit `aria/skills/phase-d-closer/SKILL.md` D.2 → D.3 flow (D.2 archive 完后进 D.3)

### T3 — PreToolUse hook (Layer 1) (~2h)

- [ ] **T3.1** New file `aria/hooks/handoff-location-guard.json`:
  - Event: `PreToolUse`
  - Match `tool_name` ∈ {`Write`, `Edit`, `NotebookEdit`} (F3 fix per R1 backend-M2 — 修 typo "Write OR Edit OR Write")
  - Path matcher: **regex on resolved absolute path** `^(?:.+[/\\])?\.aria[/\\]handoff[/\\][^/\\]+\.md$` (G2 fix per R2 backend-M2 — `[/\\]` char class 兼容 Windows backslash)
  - Hook 自身 resolve `realpath` (Python `pathlib.Path.resolve()`) 防 symlink 绕过 + 跨平台 path normalize
  - **Action mechanism** (G3 fix per R2 qa-M2): 优先 `exit 0 + JSON deny payload` (preferred per Claude Code PreToolUse hook spec — structured response), fallback `exit code 2 + stderr` (legacy mechanism, 部分版本不识别 JSON)
  - JSON deny payload 格式:
    ```json
    {"decision": "block", "reason": "<error message below>"}
    ```
- [ ] **T3.2** Error message (multi-line):
  ```
  ❌ Handoff docs must be written to docs/handoff/ (canonical location).

  .aria/handoff/ is forbidden — see standards/conventions/session-handoff.md.

  Reason: docs/ holds human-readable prose; .aria/ is for machine state only.

  Action: rewrite path to docs/handoff/<filename>.
  ```
- [ ] **T3.3** Register hook in `aria/hooks/hooks.json` per existing pattern (check 现有 hooks 注册方式 in `aria/hooks/`)
- [ ] **T3.4** Smoke test 改用 **shell subprocess + synthetic event JSON** (F7 fix per R1 qa-M1 — PreToolUse hook 无 unittest 路径):
  - 写 `aria/skills/state-scanner/tests/test_handoff_hook.sh`
  - 构造 synthetic event JSON payload (含 `tool_name: "Write"` + `tool_input.file_path: ".aria/handoff/foo.md"`)
  - 调用 hook script → assert exit code 2 + stderr 含 "must use docs/handoff/"
  - 反例: payload with path `docs/handoff/foo.md` → exit 0 (不拦)
  - **不**在 `tests/test_handoff.py` 内实施 (Python unittest 无法 trigger Claude Code 运行时 hook event)

### T4 — `RECOMMENDATION_RULES.md` handoff_drift rule (Layer 3) (~1h)

- [ ] **T4.1** Edit `aria/skills/state-scanner/RECOMMENDATION_RULES.md`:
  - 加 rule `handoff_drift`
  - Condition: `snapshot.handoff.misplaced_files != []`
  - Priority: 在 `audit_unconverged` 之下 (audit 优先), 在 `commit_only` 之上
  - Recommendation: workflow = "migrate-handoff-drift" (custom steps: `git mv .aria/handoff/*.md docs/handoff/` + 更新 latest.md + commit)
  - Confidence: 95 (deterministic detect, action 无歧义)
- [ ] **T4.2** Edit `aria/skills/state-scanner/references/output-formats.md`:
  - 加 "handoff drift detected" 输出变体

### T5 — Convention SOT (Layer 4) (~2.5h)

- [ ] **T5.1** New file `standards/conventions/session-handoff.md`:
  - §1 Rule statement: canonical = `docs/handoff/`,forbidden = `.aria/handoff/`
  - §2 Template structure (**9 段引用** F4) + 触发条件
  - §3 Enforcement matrix (proposal §Layered defense matrix 表搬过来 + 详细每层职责)
  - §4 Exception: 零 — 无 exception (与 secret-hygiene.md 不同,handoff 路径无 ambiguity)
  - §5 **Source incidents** (F5 align): 4 dogfood 实证 (SilkNode 2026-05-09 + Aria self 2026-05-13 ×3)
  - §6 Migration notes (for downstream projects upgrading from ad-hoc handoff dirs)
  - §7 References (proposal, #92, real-world handoff examples)
- [ ] **T5.2** Edit `standards/conventions/README.md` (if exists) 加 link 到 session-handoff.md
- [ ] **T5.3** **CLAUDE.md Rule #9 同步激活** (F5 fix per R1 knowledge-M2 — align Rule #7/#8 ship-time precedent):
  - 在 §不可协商规则 list 加 Rule #9 (位置: secret-hygiene Rule #7 + pre-merge gate Rule #8 之后)
  - 文案参考 Rule #7 结构: 要点 + 触发场景 + Source incidents (4 dogfood) + 详细规范 ref
- [ ] **T5.4** CLAUDE.md 信息地图 同步更新 (F6 fix per R1 knowledge-m3 — 文档同步原则 #3):
  - 在 §目录导航 表加: `├── session handoff   → docs/handoff/`
  - 在 §信息地图 子模块职责表加 `standards/conventions/session-handoff.md` 引用

### T6 — Migrate `.aria/handoff/*.md` → `docs/handoff/` (~1.5h)

- [ ] **T6.0** Pre-check (F9 idempotency per R1 qa-M3):
  - `ls .aria/handoff/*.md 2>/dev/null` 为空 → skip 整个 T6 (已迁移,无操作)
  - 检查 `docs/handoff/` 中有无同名 file → 冲突时 `--abort` 不覆盖
  - Snapshot pre-state: `ls .aria/handoff/*.md > /tmp/h0-migration-pre.list`
- [ ] **T6.1** `git mv .aria/handoff/*.md docs/handoff/` (6 files)
- [ ] **T6.2** Verify mtime 保留 (git history follows mv, blame preserved)
- [ ] **T6.3** Update `docs/handoff/latest.md`:
  - 把 Latest pointer 改成迁移后的 `2026-05-13-issue-101-cycle-closeout.md` (这是真正最新,May 13 20:31)
  - 历史 handoff 表加入迁移的 6 条
- [ ] **T6.4** `rmdir .aria/handoff/` (now empty, history preserved by git)
- [ ] **T6.5** Verify: `ls docs/handoff/*.md | wc -l` (含 `latest.md`) == 15 (8 原有 含 latest.md + 6 迁移 + 1 dogfood Phase D 自身 handoff,实际比对需在 Phase D dogfood 完成后再校验; pre-dogfood = 14)
- [ ] **T6.6** Rollback plan (F9 per R1 qa-M3, G4 fix per R2 qa-minor):
  - If `git mv` partial fails (某 file 冲突): `git restore --source=HEAD -SW .aria/handoff/ docs/handoff/` (G4 — `-S` staged + `-W` working tree 两者都回退,缺 flag 只回工作树会留 index half-state)
  - 验证: `git status` 应 clean + `ls .aria/handoff/*.md` 应 == pre-migration list (compare with `/tmp/h0-migration-pre.list` from T6.0)
  - Log to `.aria/audit-reports/2026-05-XX-h0-migration-rollback.md`
  - Re-attempt 时先解决冲突 (rename or skip 冲突 file)

### T7 — Tests + Phase D dogfood (~2h)

- [ ] **T7.1** New file `aria/skills/state-scanner/tests/test_handoff.py`:
  - Test mtime sort DESC (3 fixture files,不同 mtime → latest 正确)
  - Test age_hours computation (mock `time.time()`,确认 epoch float 输出)
  - Test misplaced detection (fixture `.aria/handoff/foo.md` → `misplaced_files == ['.aria/handoff/foo.md']`)
  - Test schema additive (snapshot 含 `handoff` field + `snapshot_schema_version` 仍 `"1.0"`)
  - Test edge: empty `docs/handoff/` → `handoff.exists == false`, `latest_path == null`,但 `misplaced_files` 字段仍 present
  - Test edge: non-UTF-8 filename in `docs/handoff/` → 跳过 file,emit warning to `errors[]` (F8 minor per R1 qa)
  - Test edge: `docs/handoff/` 不存在 → 同 empty dir 处理,不 throw
- [ ] **T7.2** Run state-scanner 整体 test suite, 确认无 regression (pre-fix all green, post-fix all green)
- [ ] **T7.3** Hook smoke test (F7 ref T3.4): 调用 `tests/test_handoff_hook.sh` → assert exit code 2 on `.aria/handoff/` path + exit 0 on `docs/handoff/` path
- [ ] **T7.4** **Dogfood Phase D** (F8 bootstrap clarification per R1 qa-minor):
  - 本 cycle T1-T8 全 land + PR merged → v1.21.0 release tagged
  - 第三方 `claude plugin update aria` 拉到 v1.21.0 → `phase-d-closer` D.3 step 可用
  - 本 session 在 v1.21.0 land 后执行 D.3 (注意:本 cycle 期间手动模拟 D.3 step,因为 plugin 尚未 ship to local cache; D.3 流程 deployment 是 v1.21.0 ship 的副作用,not pre-req for dogfood)
  - 写 `docs/handoff/2026-05-XX-h0-cycle-done.md`,验证 9 段模板 fill + latest.md 自动更新 + dogfood 第 5 次实证

### T8 — Pre-merge audit + benchmark + Phase C + Phase D + release (~3h, F10 fix per R1 qa-M4 estimate correction)

- [ ] **T8.1** Pre-merge audit-engine `pre_merge` checkpoint (convergence mode, 3 agents — backend-architect, knowledge-manager, qa-engineer)
- [ ] **T8.2** Rule #6 `/skill-creator benchmark state-scanner` (F8 重定义 metrics per R1 qa-M2):
  - **Structural metric 1**: mtime sort 准确性 — fixture set 含 5 个 dated handoff files with known mtimes → assert latest detected == newest mtime (deterministic 100%)
  - **Structural metric 2**: misplaced detection precision/recall — synthetic project (3 fixture: legitimate `docs/handoff/` only / both dirs populated / `.aria/handoff/` only) → assert collector accurately classifies → precision=recall=1.0
  - **不**用 "field present with/without collector" 作为 metric (tautological per R1 audit)
  - Store results in `aria-plugin-benchmarks/ab-results/2026-05-XX-h0-handoff-stage/`
- [ ] **T8.3** Phase C.1 — commit per repo, Conventional Commits:
  - `standards`: `feat(conventions): add session-handoff.md (Layer 4 SOT)`
  - `aria` (plugin): `feat(state-scanner): add handoff collector + snapshot.handoff field (additive, schema 1.0)` / `feat(phase-d-closer): add D.3 session-handoff step + template` / `feat(hooks): add handoff-location-guard PreToolUse hook` / `docs(skills): update RECOMMENDATION_RULES + SKILL.md + output-formats`
  - main `Aria`: `chore(handoff): migrate .aria/handoff/ → docs/handoff/ (14 files canonical)` + submodule pointer bump
- [ ] **T8.4** Phase C.2 — Create 3 PRs:
  - aria-standards PR (smallest, no deps)
  - aria-plugin PR (depends on standards link)
  - Aria main PR (depends on aria submodule pointer bump after aria-plugin merge)
  - Rule #8 pre-merge gate verify each PR (aether fallback `skip_with_warning` per current config)
- [ ] **T8.5** Phase D.2 — `openspec archive aria-ten-step-session-handoff-stage --yes`,fix CLI bug if needed
- [ ] **T8.6** **v1.21.0 release** — 5+1 SOT files atomic bump:
  - `plugin.json` (1.20.0 → 1.21.0)
  - `marketplace.json` (1.20.0 → 1.21.0)
  - `VERSION` (1.20.0 → 1.21.0)
  - `CHANGELOG.md` add `[1.21.0]` entry
  - `README.md` version + skill count (30 → 30 user-facing,因 phase-d-closer 是已有 skill 不新增,但加新 collector + hook + convention)
  - `README.zh.md` 同步
  - Git tag `v1.21.0` annotated
  - Multi-remote push (origin + github) per Phase C.2.5 enforced
- [ ] **T8.7** Phase D.3 — **dogfood** 写 closeout handoff to `docs/handoff/2026-05-XX-h0-cycle-done.md` (本 cycle 自身 5th dogfood evidence)

---

## Phase A.3 Agent Assignment

| Task | Primary agent | Rationale |
|------|---------------|-----------|
| T1 collector | `aria:backend-architect` | Python stdlib collector logic, deterministic |
| T2 phase-d-closer + template | `aria:knowledge-manager` | SKILL.md doc + 8-section template structure |
| T3 hook | `aria:backend-architect` | Hook JSON + PreToolUse semantics |
| T4 RECOMMENDATION_RULES | `aria:knowledge-manager` | Doc edit, deterministic rule |
| T5 convention SOT | `aria:knowledge-manager` | Normative doc creation |
| T6 migration | `claude` (default) | git mv + verify, 工具操作 |
| T7 tests + dogfood | `aria:qa-engineer` | Test design + regression check |
| T8 audit + benchmark + ship + release | `claude` (orchestration) + `aria:code-reviewer` (pre-merge audit member) | 多 repo 协调 |

---

## Estimated effort

| Task | Estimate | Cumulative |
|------|----------|-----------|
| T1 collector | 4h | 4h |
| T2 phase-d-closer + template | 4h | 8h |
| T3 hook | 2h | 10h |
| T4 RECOMMENDATION_RULES | 1h | 11h |
| T5 convention SOT (+ CLAUDE.md Rule #9 + 信息地图) | 2.5h | 13.5h |
| T6 migration (+ idempotency + rollback) | 1.5h | 15h |
| T7 tests + dogfood Phase D | 2h | 17h |
| T8 audit + benchmark + ship + release | 3h | **20h** |

**Total**: ~20h (F10 corrected from 17h per R1 qa-M4 — Level 2 upper bound slight overrun, still manageable;若 R2 出新 Critical 拆 sub-cycle)

**PERT** (R1 audit 已 inform):
- Optimistic: ~17h (R2 SCOPE_OK 一次过)
- Likely: ~20h (含 R2 fix-verify round inline-fix)
- Pessimistic: ~24h (R3 振荡 + scope creep,触发 OD trigger 时拆 sub-cycle)

---

## Mid-impl checkpoint

实测 T1+T2+T3 累计 (10h baseline) 超过 13h (+30%) 即 trigger reforecast 协议:
- 检查 scope creep (是否新增 in-scope item)
- 检查 hook PreToolUse 是否遇到 framework 边界 (例如其他 hook 冲突)
- 必要时拆 T4-T8 到 separate cycle (推 v1.22.0)
