# DEC-20260524-002 — Forgejo Aria #124 Submodule Pointer Regression Gate

> **日期**: 2026-05-24
> **模式**: technical (brainstorm)
> **状态**: CONVERGED (R1 4-agent discuss → R2 reversals → R3 4/4 ACCEPT_R3 unified anchor)
> **Forgejo issue**: [Aria #124](https://forgejo.10cg.pub/10CG/Aria/issues/124)
> **Source incident**: 2026-05-23 PR #123 silent submodule pointer regression (commit 6fea5d7) caught by post-merge audit, fast-forward fixed by a8e0096

---

## §1 背景

**2026-05-23 incident**: 主 Aria PR #123 (Track E `aria-layer2-docker-auth-cold-pull-fix`) rebase against master 时,执行 `git checkout origin/master -- aria` 解决 submodule pointer conflict。本地 `origin/master` ref **未 refresh** (no `git fetch` before checkout)。Staged aria pointer 是 **stale SHA** (3b688a9),merge 后**静默回滚** dev-claude2 4 commits:aria-plugin v1.24.1 + atomicity-guard + v1.25.0 + v1.26.0。

被 post-merge audit catch + fast-forward fix `a8e0096`(~10min)。但若 audit 晚跑或被跳过:
- dev-claude2 几天工作隐式 revert
- Plugin marketplace (从 GitHub mirror 拉) 看到旧版本
- 下游 consumer fresh clone 一直 broken

**根因分析**: stale local `origin/master` ref + rebase conflict resolution shortcut 信任 stale ref。**Layer L 6-rule reconcile**(multi-terminal-coordination v1.22.0+ ship)覆盖 orphan ref claim conflicts,**不**覆盖 submodule pointer write conflicts during PR rebase。

---

## §2 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 范围 | aria-plugin Skill scope | 改 `aria/skills/phase-c-integrator/SKILL.md` §C.2.5,Level 3 OpenSpec |
| 兼容性 | 向后兼容(Aria Rule #4) | Two-phase rollout: warn-only → block,给 ecosystem 缓冲 |
| 哲学 | advisory over hardlock(`feedback_concurrency_advisory_over_hardlock`) | Override 必须 explicit per-PR,不 sticky;rebase conflict resolution 不强改 |
| 工具 | Git primitive only | `merge-base --is-ancestor`,no custom logic |
| Methodology | N=1 cost-benefit(Aria Rule "不为假想未来加 infra") | 单 gate scope,但建 tripwire 准备 N=2 |
| 实现物理 | git hook injection point 在 `git checkout -- <path>` 期间 interactive rebase 中**不存在** | (C) 作 code 是 IMPLEMENTATION BLOCKER (backend-architect R1) |

---

## §3 考虑的方案

| # | 方案 | R1 verdict | R2 verdict | R3 verdict |
|---|------|------|------|------|
| **(A)** | branch-finisher post-merge backward-move detector(告警) | tech-lead ACCEPT(weak) / backend-architect REJECT / qa REVISE / code-reviewer REVISE-DEFER | tech-lead CONCEDE (A 部分) / code-reviewer CONCEDE (full A+B) | DEFERRED via tripwire |
| **(B)** | Phase C.2.5 pre-merge `merge-base --is-ancestor` 阻断 gate | **4/4 ACCEPT** | **4/4 ACCEPT (hardened (B+))** | **ANCHOR** |
| **(C-code)** | Layer L Rule 7 改 rebase conflict 解决偏好 `<submodule>-master HEAD` | **4/4 REJECT** (backend-architect: 无 git hook injection point — implementation BLOCKER) | — | — |
| **(C-doc)** | (C) 作 convention doc(zero code) | 3/4 ACCEPT 作 doc | — | ACCEPTED 作 SOT in standards/conventions/ |

### R2 双反转事件(关键 evidence)

| Agent | R1 → R2 | 关键 concession |
|---|---|---|
| tech-lead | (A)+(B) → **(B) only** | code-reviewer arg 3 决定性:fail-loud fetch hardening 关闭 ~80% (B) stale-ref gap → (A) 不再 justify |
| code-reviewer | DEFER → **(A)+(B)** | tech-lead mechanical analysis 正确:(A) 读 tree-embedded SHAs immutable, (B) 读 remote-tracking refs mutable — disjoint failure modes |
| ai-engineer(neutral) | — | 第三路径:(B+) hardened + measured tripwire = 同时满足两边 |

R2 两个 R1 主要 forking agents 各自 CONCEDE 到对方立场 — 实质性更新,非 paper-fix surface agreement(per `feedback_brainstorm_forcing_function_unified_anchor` warning)。

### R3 forcing function unified anchor 验证

orchestrator(本 brainstorm)合成 ai-engineer 第三路径作 unified anchor,4 R3 agents validate(NOT re-propose,per M6 R3 pattern):

- **4/4 ACCEPT_R3** unanimous
- 3 Q-NEW MINOR(全部 Phase A.1 spec-drafter 处理):
  - backend-architect Q1: drop fragile fetch grep,exit-code-only abort
  - qa Q1: name tripwire monitoring observer(periodic job or human cadence)
  - code-reviewer Q1: tripwire counter mechanical(file/label)or convention-only

---

## §4 最终选择

**方案**: (B+) hardened pre-merge gate + measured tripwire + (C) as convention doc

### Phase A.1 Spec scope (Level 3 OpenSpec)

1. **(B+) pre-merge gate** in `aria/skills/phase-c-integrator/SKILL.md` §C.2.5(after Rule #8 `aether ci status` check,before merge execution)
   - 主 check: `git -C <submodule> merge-base --is-ancestor MASTER_PTR FEATURE_PTR`(exit 0 = forward,exit 1 = regression-or-divergence)
   - 双向 ancestry check: 若 exit 1,再跑反向 `is-ancestor FEATURE_PTR MASTER_PTR`(若 exit 0 = (c) regression,若 exit 1 = (d) divergence)
   - **Hardening 1 — exit-code-only fail-loud fetch**(per backend-architect Q-NEW-1): `git fetch origin master` 非零 exit 即 abort,**不要** grep success patterns(`grep "up to date|new ref"` fragile — git success signatures 复杂)
   - **Hardening 2 — refspec assertion**: capture `git rev-parse origin/master` before/after fetch;若 expected-to-advance and didn't → abort with operator confirm
   - **Hardening 3 — visible SHA diff print**: 每次 gate run 打印 `submodule=<name> master=<sha> feature=<sha> verdict=<PASS|REGRESSION|DIVERGENT>` 到 audit log
   - **nil-SHA handling**: `git ls-tree HEAD <submodule>` 空输出 = first-time submodule → exit 0 + INFO log(qa CRITICAL TEST GAP from R1)
   - **Race handling**(per backend-architect R3 missing scenario): 并发 force-push 到 origin/master during gate execution → refspec assertion 不 false-positive(只要 fetch 成功 + ancestry 关系正确即放行)

2. **Override mechanism** — per-PR explicit ONLY:
   - Commit trailer: `Submodule-Rollback: <sub> <old-sha>→<new-sha> reason=<...>` (mirrors Rule #7 `secret-leak-ok-explicit` pattern)
   - OR PR label `submodule-rollback-approved`
   - Gate parses + ALLOW with audit log entry
   - **不**支持 sticky config flag

3. **Tripwire pre-commitment**(Spec proposal.md §Risks codified):
   - Auto-promote (A) post-merge detector **without re-brainstorm** if 任一:
     - 任何 submodule pointer regression 逃过 (B+) within 12 months OR 100 merges(whichever first)
     - 任何 (B+) fetch-failure incident manifests in audit logs
     - 任何 non-PR-flow regression observed(direct master push bypassing PR)
   - **Counter mechanism**(per code-reviewer Q-NEW-1): tracked in `aria/metrics/submodule-gate-misses.json` OR Forgejo issue label `gate-tripwire-count`(Phase A.1 二选一)
   - **Monitoring observer**(per qa Q-NEW-1): named periodic job(weekly cron 比对 master HEAD~1 vs HEAD submodule gitlink ancestry)OR named human review cadence(Phase A.1 二选一,推荐 periodic job 因为 dead-tripwire risk)

4. **(C) convention doc** in `standards/conventions/submodule-pointer-hygiene.md`(NEW file):
   - "Always `git fetch origin` before any rebase that may have submodule pointer conflicts"
   - "Never resolve submodule conflict via `git checkout origin/master -- <sub>` without explicit `git fetch` first"
   - "If conflict resolution requires stale ref,abort + manual investigation"
   - **不**加入 CLAUDE.md numbered Rule(per code-reviewer:已 Rule #1-#9 重,convention SOT 在 standards/ 足够)

5. **Two-phase rollout**(mirrors Rule #8):
   - **v1.28.0 — warn-only mode**:gate logs `WOULD-BLOCK submodule=<name> master=<sha> feature=<sha> reason=<regression|divergence>`,**不**拒绝 merge
   - Telemetry collected during warn-only:每次 gate fire,记 (SHA-before, SHA-after, PR#, timestamp, classification)
   - **FP threshold for flip**(per qa Q-NEW + code-reviewer Q-NEW concerns):<2% sustained over 20+ merges(Spec 明确 number,避免 indefinite warn-only drift)
   - **v1.29.0 — block mode**:flip after threshold met OR time-boxed hard date(Spec 二选一,推荐 hard date 例如 v1.28.0 ship +14 天 default-on unless explicit FP evidence files defer OpenSpec)

### Phase B replay test scope(7 + 1 race scenarios)

| # | 场景 | Expected | 测试方式 |
|---|------|---------|---------|
| 1 | Happy path forward bump | gate PASS(exit 0) | ephemeral fixture repo + real git ops |
| 2 | Pure regression(ancestor) | gate BLOCK(exit 1 + `REGRESSION: <old>..<new>`) | fixture: feature ptr = master ptr 的 ancestor |
| 3 | Divergent history(unrelated branch) | gate BLOCK with `DIVERGENT: no common ancestor` | fixture: 完全独立 submodule branch |
| 4 | Stale-ref incident replay | fetch refreshes → ancestor check accurate | fixture: 本地 origin/master ref 故意 stale → fetch → 验证 fetch fail-loud OR ancestry correct |
| 5 | Legitimate revert + trailer override | ALLOW + audit log entry | fixture: feature ptr = ancestor + commit msg `Submodule-Rollback: ...` |
| 6 | No-change(same pointer) | PASS trivially | fixture: master ptr == feature ptr |
| 7 | First-time submodule(nil prior gitlink) | PASS + INFO log | fixture: master 无该 path,feature 新加 submodule |
| 8 | Submodule removed from feature | gate 不 crash | fixture: master 有,feature 删 |
| **9 (added per backend-architect R3)** | Concurrent force-push to origin/master during gate execution | gate 不 false-positive abort | fixture: 模拟 fetch 中 origin/master 改变 |

### Phase B Rule #6 substitute(deterministic structural Skill,non-LLM AB)

per `feedback_deterministic_structural_skill_rule6_substitute`:
- Structural fixture README in `aria-plugin-benchmarks/submodule-gate/`
- 9-scenario unit tests
- Dogfood: 在 fresh feature branch artificially set submodule ptr to ancestor → attempt PR merge → gate blocks
- Atomicity guard test

---

## §5 理由

### 为何 (B+) hardened 是 anchor

1. **Direct address root cause**:incident 根因是 stale `origin/master` ref + rebase conflict shortcut。(B+) mandatory fail-loud fetch 直接 close 此根因(若 fetch 失败,gate abort 不 silent fallback)。
2. **R2 双方收敛**:tech-lead 接受 fail-loud fetch 关闭 80% stale-ref gap;code-reviewer 接受 disjoint failure modes 是 real。ai-engineer 第三路径合二为一 — (B+) hardening 吸收大部分 (A) 价值,tripwire 吸收余下。
3. **Aria methodology compatibility**:
   - Rule #5 spec 位置 ✓(aria-plugin openspec/changes/)
   - Rule #8 hook 位置 ✓(C.2.5 同处)
   - Rule #6 deterministic substitute ✓
   - Two-phase rollout 与 Rule #8 一致
4. **Minimal scope discipline**:~70 LOC + ~5h,单 Skill 改动,无 multi-Skill split,无 numbered Rule overhead
5. **Measured tripwire 替代模糊 defer**:把 code-reviewer R1 模糊 "N=2 再说" 变成可观测 trigger(12mo OR 100 merges OR fetch-fail OR bypass)

### 为何 不上 (A) 本 cycle

1. R2 tech-lead concede:fail-loud fetch hardening 关闭 stale-ref attack surface ~80%(主要场景)
2. (A) 是 retrospective(post-merge),detection-only,不 prevent 落 master
3. N=1 incident + 已被 manual audit 在 ~10min 内 catch — 增量价值 = MTTD 从"次日 audit"压缩到"merge 后立即",但 incident cost <1 day,边际 ROI 低
4. Tripwire 把 (A) 升级路径 mechanize — 若 (B+) gap manifests,auto-promote 无须 re-brainstorm

### 为何 (C) 仅作 convention doc

1. backend-architect R1 **IMPLEMENTATION BLOCKER**:`git checkout -- <path>` 在 interactive rebase 中**无** git hook injection point(`pre-rebase` 已 fire,`post-checkout` 不 trigger path-level checkout,`prepare-commit-msg` 不能 inspect staged paths)。代码实施需 wrap `git` 本身 — out of scope。
2. tech-lead R1 哲学反对:Layer L 既定 "advisory > hardlock"(per `feedback_concurrency_advisory_over_hardlock` DEC-20260519-001)。强 override conflict resolution 违此原则,且会 mask 操作员"为什么 master HEAD 比 feature 旧"的真正认知信号。
3. qa R1 高 blast radius:cross-team scenarios 中 (C) 沉默覆盖人类意图。
4. As doc-only:zero code cost,convention SOT 在 standards/,cross-ref from CLAUDE.md(NOT numbered Rule per code-reviewer R3)— 教学价值保留,无 enforcement risk。

---

## §6 风险与缓解

| # | 风险 | 缓解 |
|---|------|------|
| R1 | Tripwire dead-zone(没人查 → 12mo 过去 silently) | qa Q-NEW resolve:Phase A.1 必须 spec named periodic job(weekly cron 比对 master HEAD~1 vs HEAD submodule gitlink ancestry) |
| R2 | Warn-only mode permanent(zero FP → 无 trigger flip) | code-reviewer R3 mitigation:hard date flip threshold(例 v1.28.0 ship +14d default-on unless explicit FP defer OpenSpec) |
| R3 | Fail-loud fetch 误报(`git fetch` 网络 transient blip 阻塞 merge) | backend-architect Q-NEW resolve:`wait_recoverable` 错误类型(per workflow-runner pattern)— transient fetch failure 自动 retry 指数退避,non-transient(auth / URL drift)才 block |
| R4 | Override trailer 被 abuse(operator 误判 legitimate revert) | Audit log per override + 月度 review override 使用率(qa R1 metric);若 >15% gate fires 用 override → 重审 gate sensitivity |
| R5 | First-time submodule false-block(qa R1 CRITICAL TEST GAP) | Scenario 7 explicit test + nil-SHA handling spec'd(empty ls-tree output → exit 0 INFO) |
| R6 | Concurrent force-push race(backend-architect R3 missing scenario) | Scenario 9 added;refspec assertion 不 false-positive(只要 fetch 成功 + ancestry 正确即放行) |
| R7 | URL drift attack(submodule remote URL 偷换到 attacker server,fetch succeeds against wrong remote)| **Out of scope** for this Spec — separate threat model (supply chain security);若 manifests → tripwire condition #3 (non-PR-flow) catch + 升级到独立 Spec |

---

## §7 Open Q-NEW(Phase A.1 spec-drafter 处理)

| Q | 来源 | 内容 | 处理 |
|---|------|------|------|
| Q-NEW-1 | backend-architect R3 | Explicitly drop fragile fetch success grep in favor of exit-code-only abort | Spec §C.2.5 step 3 明文写 "rely on `git fetch` exit code,do NOT grep success patterns" |
| Q-NEW-2 | qa R3 | Name tripwire monitoring observer(periodic job vs human review cadence) | Spec §Risks 推荐 weekly periodic job(`aria/skills/tripwire-monitor/SKILL.md` NEW file OR 集成到 state-scanner Phase 1.x as opt-in collector) |
| Q-NEW-3 | code-reviewer R3 | Tripwire counter mechanical(file/label)or convention-only | Spec 推荐 mechanical:`aria/metrics/submodule-gate-misses.json` 由 (B+) gate audit log emitter 写入 OR Forgejo issue label `gate-tripwire-count` 由 weekly cron 计数 |

3 Q-NEW 都是 Spec drafting concerns,brainstorm 阶段不阻塞,Phase A.1 必须明确解决。

---

## §8 Cross-references

### 本 brainstorm 全产出

- 4 R1 agent reports(tech-lead / backend-architect / qa / code-reviewer)
- 3 R2 agent reports(tech-lead reversal / code-reviewer reversal / ai-engineer neutral third path)
- 4 R3 validation reports(4/4 ACCEPT_R3 + 3 Q-NEW MINOR)
- 本 DEC

### 上游

- Forgejo Aria [#124](https://forgejo.10cg.pub/10CG/Aria/issues/124)
- Track E Spec(archived): `aria/openspec/archive/2026-05-23-aria-layer2-docker-auth-cold-pull-fix/`
- 2026-05-23 incident commits: `6fea5d7` (PR #123 merge regression) + `a8e0096` (fast-forward fix)
- Memory: `feedback_submodule_pointer_post_merge_bump` (existing)
- Track F handoff: `docs/handoff/2026-05-24-m6-brainstorm-converged-track-f.md` §3 R1 (incident document)

### 复用 brainstorm pattern memory

- `feedback_brainstorm_forcing_function_unified_anchor` — R3 orchestrator forcing function(M6 实证,本 brainstorm 复制)
- `feedback_brainstorm_owner_escalation_discipline` — Q-escalation count discipline(本 brainstorm Q-NEW = 3,健康 threshold ≤2 中等偏高,但都是 spec-drafting concern non-fork-reopening)
- `feedback_post_spec_audit_pragmatic_convergence` — unanimous PASS + 无振荡 = 收敛(本 R3 4/4 ACCEPT 直接达成)
- `feedback_paper_fix_antipattern` — R2 双反转都是 substance-level(非 surface verdict match),无 paper-fix 风险

### 下游

- **Phase A.1 spec-drafter**(本 cycle 下一步): write `aria/openspec/changes/aria-submodule-pointer-gate/proposal.md` + `tasks.md`,resolve 3 Q-NEW MINOR,run post_spec audit
- **Phase B**:implement (B+) in `aria/skills/phase-c-integrator/SKILL.md` §C.2.5 + 9-scenario replay tests + Rule #6 structural substitute
- **Phase C**:aria-plugin PR + v1.28.0 release(5+1 SOT bump)+ main Aria submodule pointer re-bump + 3-way SHA parity
- **Phase D**:Spec archive + handoff doc per Rule #9 + memory entries(possibly new entry for "R2 mutual concession unified anchor pattern")

### Convention doc deliverable

- `standards/conventions/submodule-pointer-hygiene.md`(NEW file in Phase B)— (C) doc-only version

---

## §9 Brainstorm meta-observations(supports future methodology refinement)

### 新现象 #1: R2 双反转 → 第三路径合成

本 brainstorm 出现 M6 brainstorm 未见的现象:**R2 双方都 concede 到对方 R1 立场**(tech-lead → "B only"; code-reviewer → "A+B")。这是 brainstorm 成熟度信号(non-stubborn agents capable of mechanical position update),而非 paper-fix(双方都不再坚持 R1 立场)。

ai-engineer(R2 neutral 3rd party,fresh perspective)的第三路径 **strict superset** 双方 R2 concessions:既 honor tech-lead R2 的"(B) hardening 足够",也 honor code-reviewer R2 的"disjoint failure modes 是 real" → 用 tripwire 把 (A) 留作 N=2 fallback,而非 N=1 ship。

这个 pattern 是否值得固化为新 memory? 候选 entry:
`feedback_r2_mutual_concession_third_path_synthesis`:
- 当 R1 fork 双方 R2 都 concede 到对方时,neutral 3rd party 的第三路径(同时 honor 双方 concessions)往往是 forcing function unified anchor 候选
- Detection signal: R2 reports 含 "I concede" + opposite-direction conclusions
- 价值: 缩短到 R3 收敛(本 brainstorm 3 rounds vs M6 R4+R5 可能性)

(Phase D 决定是否 ship 此 memory)

### 新现象 #2: Q-NEW count

R1 → 0 Q-NEW(纯 discussion);R2 → 0 Q-NEW(纯 challenge);R3 → 3 Q-NEW(all MINOR spec-drafting)。Total Q-escalation = 3 across 3 rounds = average 1 per round = **healthy threshold per `feedback_brainstorm_owner_escalation_discipline`**(≤2 per round)。3 Q-NEW 都被 R3 自己 inline resolve 或 defer 到 Phase A.1,无须 owner 决策。这是 brainstorm 自闭环成功标志。

---

**Created**: 2026-05-24T~11:55Z
**Author**: orchestrator(Claude Opus 4.7 1M context)+ 7 agent participants(tech-lead R1+R2+R3, backend-architect R1+R3, qa R1+R3, code-reviewer R1+R2+R3, ai-engineer R2)
**Status**: ✅ CONVERGED — 4/4 ACCEPT_R3 unanimous + 3 Q-NEW MINOR(spec-drafting resolvable)
**Next**: Phase A.1 spec-drafter — write proposal.md + tasks.md in `aria/openspec/changes/aria-submodule-pointer-gate/`(aria-plugin 子模块)
