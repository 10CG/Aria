---
track-id: aria-2-0-m5-replay-reconciler-drift-review-loop-audit
owner-container: simonfish/dev-claude
phase: A.7
status: paused
updated-at: 2026-05-20T10:15:00Z
---

# Aria — Session Handoff (2026-05-20 ~10:15 UTC) — M5 T-deploy Phase A done + A.7 dry-run derisk, Phase B gated

> **Status**: Paused — Phase A 5 OD + Phase A.7 dry-run + 2 memory entries + 0 prod mutation; Phase B (~2-3h prod-write) gated to next dedicated session
> **Predecessor handoff**: [`2026-05-20-session-final-o1-paused-with-v2-playbook.md`](2026-05-20-session-final-o1-paused-with-v2-playbook.md) — same track, the v2 playbook this session executed Phase A against
> **Next session 入口**: 优先读本 doc → §6 → Phase B 直接走 v2 playbook §Phase B 步骤 1-8 (5 OD 已锁 + 3 dry-run advisories applied per §3 R5)
> **Revision history**: Initially written 07:32 (Phase A.5 sign-off); amended 10:15 to include Phase A.7 dry-run + 2 memory writes + 2 multi-terminal races + Q3 audit confirmation.

---

## §0 入口 (新 session 优先读)

新 session 读取顺序硬约束 (如果你要推 Phase B):

1. **本 doc** (你正在读) — 锁 5 OD + 4 reframe + DB snapshot path + backup branch name
2. **`.aria/notes/m5-deploy-od-decisions-2026-05-20.md`** — 5 OD 决策正式记录 (AskUserQuestion-backed)
3. **`.aria/notes/m5-deploy-phase-a-snapshot-2026-05-20.md`** — DB 快照 + 16 dispatch IDs + backup branch + sign-off checklist
4. **`.aria/notes/prod-job-spec-live-2026-05-20.md`** — Live Nomad spec (Rule #7 scrubbed)
5. **`.aria/notes/m5-deploy-phase-a7-dry-run-2026-05-20.md`** — **(A.7 amendment 10:15)** Phase B HCL validate + migrations + Nomad var + 3 advisories (HCL ambiguity / 005 row count assert / M1_VALIDATOR_PATH file)
6. Optional: `2026-05-20-prod-state-investigation.md` (Phase A reframes 2 of its §2 finding 顺序 — 见 §3 R1)
6. Optional: `2026-05-20-m5-deploy-playbook-v2-accurate.md` (§Phase B 1-8 仍可用, 但 §OD-3/§OD-4 假设需替换为本 doc 的 reframe)

读完后:**Phase B 可直接进**, 5 OD 已锁, Phase A 所有前置完成。预计 ~2-3h dedicated session。

如果**今天不打算 Phase B** → `/aria:state-scanner`, 会 surface 本 doc + handoff multi-track 看板, 可转 Path B (Tier 2 state-scanner family) 或其它 backlog。

**重要架构 awareness** (从 predecessor 继承):
- aria-plugin **v1.22.0 已 ship** (multi-terminal-coordination Spec, by `simonfish/dev-claude2`)
- CLAUDE.md 现含 Rule #9 Extension (Layer H handoff frontmatter)
- 本 doc 是 **`simonfish/dev-claude` 终端第二份**使用 Layer H frontmatter 的 handoff (predecessor 是第一份)
- aria-plugin master = `ce58d35` (v1.22.0), aria-orchestrator master = `962cb56` (v11 HCL fix), standards master = `16041f4` (Layer H schema)

---

## §1 已完成 (按时间顺序)

| 时间 (UTC) | 事件 | Commit / 文件 | 备注 |
|-----------|------|---------------|------|
| 2026-05-20 ~05:48 | Session start: `/aria:state-scanner` v3.0.0 mechanical scan, snapshot clean | — | scan.py exit 0, schema 1.0 |
| ~05:50 | 读取 prerequisites: predecessor session-final + prod-state-investigation + v2-accurate playbook | — | 3 docs, ~3000 lines |
| ~05:52 | AskUserQuestion 4-batch: OD-1 + OD-2 + OD-5 + Phase A go-ahead | 全 (a)/(b)/(a)/yes 与推荐一致 | OD-3 + OD-4 deferred to post-A.4 |
| ~05:54 | SSH light-1 connectivity verified | — | hostname light-1, NOMAD_ADDR 已知 |
| ~05:55 | **A.2 DB snapshot** | `/tmp/aria-layer1-snapshot-20260520T055525/dispatches.db.pre-m5` | integrity=ok, 16 rows, schema=3.0 |
| ~05:55 | A.2-supplement: 16 dispatch IDs + state distribution + migration_notes captured | `.aria/notes/m5-deploy-phase-a-snapshot-2026-05-20.md` | 1 S9_CLOSE + 15 S_FAIL |
| ~05:56 | **A.3 Git backup branch** | `backup/pre-m5-upgrade-20260520T055622` @ `e416920` | git stash skipped (submodule M not stashable by default) |
| ~05:57 | **A.4 Nomad inspect** (Rule #7 scrubbed Python wrapper) | `.aria/notes/prod-job-spec-live-2026-05-20.md` | raw_exec driver, 16 env keys (0 secret-likely), Templates DestPath only |
| ~05:58 | A.4-followup: probe `/root/.hermes/` + `/opt/aria-orchestrator/app/` + nomad data dir | inline output captured in notes | discovered `/opt/aria-orchestrator/app/` ACTIVE (not obsolete) |
| ~06:00 | AskUserQuestion 2-batch: OD-3 (i) + OD-4 (a) | (i)/(a) 与推荐一致 | OD-3 升级为 "Phase A.6 verification" |
| ~06:02 | **A.6 Source review** — aria-layer1 v0.4.0 `__init__.py` + extension.py + plugin.yaml | dev-container 路径 read-only | confirmed on_session_start no-op stub (AD-M2-7 lock 2026-05-02) |
| ~06:05 | A.6 supplement: prod `/root/.hermes/cron/jobs.json` read | 1 active cron = `aria-heartbeat` 48ed7e826bc3 (995 runs) | **NOT aria-layer1** — orthogonal M0/M1 tooling |
| ~06:10 | A.5 sign-off checklist 全勾 (10/11, 仅 owner go/no-go pending) | notes 三份齐 | zero prod mutation accumulated |
| ~07:30 | AskUserQuestion 1: Phase B gate → (a) wrap clean | — | 本 doc + commit + push |
| ~07:33 | **Aria main commit `34106d1`** docs(handoff): Phase A snapshot done | 5 文件 (3 notes + handoff + latest.md) | Phase A.5 sign-off |
| ~07:35 | **Multi-terminal race #1**: push reject (origin advanced to `a2d06e7` v1.22.1 hotfix by `simonfish/dev-claude2`) → clean rebase | — | 第 N+1 次 race meta-dogfood |
| ~07:38 | Push retry success → 3-way SHA parity `34106d1` | origin + github | per `feedback_concurrent_edit_clean_rebase_pattern` |
| ~08:00 | **Phase A.7 dry-run validation** (opportunistic derisking, zero prod write) | `.aria/notes/m5-deploy-phase-a7-dry-run-2026-05-20.md` | nomad job validate (2 HCL) + migrations 004/005/006 inspect + Nomad var existence (Rule #7) + 3 advisories surfaced |
| ~09:30 | Memory entries: `feedback_prod_state_must_ground_playbook` amend + `feedback_layered_od_resolution_with_live_probe` new + MEMORY.md index | harness `~/.claude/.../memory/` (non-repo) | 2 committed; `feedback_git_stash_skips_submodule_pointer` skipped (low value, general Git knowledge) |
| ~09:35 | Issue cache cleared (`.aria/cache/issues.json`) | — | next-session ergonomics — Phase 1.13 will live-fetch |
| ~10:00 | **Aria main commit `54c2488`** docs(handoff): Phase A.7 dry-run validation | 1 file (advisory note) | |
| ~10:02 | **Multi-terminal race #2**: push reject (origin advanced to `34a1ce7` D.3 update by `simonfish/dev-claude2`) → clean rebase | — | 2nd race this session |
| ~10:05 | Push retry success → 3-way SHA parity `54c2488` | origin + github | clean |
| ~10:10 | Q1-Q4 closeout audit: 4-repo parity verify + US-025/US-026 status check + OpenSpec inventory (M5 Spec still active, T-deploy unchecked = correct) + UPM N/A + PRD unchanged | inline shell + reads | this amendment trail |
| ~10:15 | **Handoff doc amendment**: frontmatter phase A→A.7, updated-at bumped, §1 timeline extended, §3 R5 added (3 advisories), §6 + §7 refreshed | 本 file | Phase B closure for handoff |

**Cycles shipped this session**: **0 OpenSpec Spec full cycle**。Phase A 是 deploy-prep,非 Spec cycle 范畴。

**累计 Phase A deliverables**: 5 OD 决策 + 3 notes (~500 行) + 1 backup branch + 1 DB snapshot + 4 prod reframes + 16 dispatch ID census + 0 secret leak + 0 prod mutation。

---

## §2 未完成 / Carry-forward 清单

### Owner-gated 执行 (US-025 close gate — Track B 主线)

| # | 项目 | 状态 | 备注 |
|---|------|------|------|
| **O1** | **T-deploy Phase B execution** (v2 playbook Phase B 步骤 1-8) | **READY** — 5 OD 锁, 4 reframe, backup + snapshot 就绪 | ~2-3h dedicated session, prod-write (DB migration + Hermes restart + 2 new Nomad jobs) |
| O1c | Layer 2 image v11 build + real smoke (v2 playbook Phase C) | gated to ≥ 24h after Phase B stable | ~2h separate session |
| O2 | Tier-1 live LLM 验证 | gated to Phase B Step 8 或 Phase C | owner-executable, ~¥0.10 |

### Phase B 进入前必读 prerequisites (本 doc + 3 notes 已 cover)

| 资源 | 用途 |
|------|------|
| `.aria/notes/m5-deploy-od-decisions-2026-05-20.md` | 5 OD 锁定决策(Reset/Pure Nomad/N/A/Leave alone/Big leap) |
| `.aria/notes/m5-deploy-phase-a-snapshot-2026-05-20.md` | DB snapshot path + 16 dispatch IDs + backup branch + rollback procedure |
| `.aria/notes/prod-job-spec-live-2026-05-20.md` | raw_exec driver + 16 env keys + Hermes state at /root/.hermes/ |
| `docs/handoff/2026-05-20-m5-deploy-playbook-v2-accurate.md` | §Phase B 步骤 1-8 仍可用, **但 §OD-3 / §OD-4 假设需用本 doc §3 R1 替换** |

### 非阻塞 backlog (Forgejo, 继承自 predecessor)

| Tier | 状态 |
|------|------|
| **Tier 1** (v1.21.4 patch) | ✅ DONE (predecessor session) |
| **Tier 2** (state-scanner family: #58/#89/#90/#79) | 可推 |
| **Tier 3** (secret-hygiene #84/#107) | 可推 |
| **Tier 4** (audit rubric #54/#95) | Level 2-3 |
| **Tier 5** (proposals #59/#104/#111) | 待 owner OD |
| **Tier 6** (远期 #5/#32) | 远期 |

详见 `.aria/notes/issue-triage-2026-05-19.md` (本 session 未修改)。

---

## §3 关键风险 / 已知陷阱

### R1 — Investigation §2.4 + §2.2 reframe (本 session 实地推翻)

**事件**: `2026-05-20-prod-state-investigation.md` §2.2 (hermes-data 缺失) + §2.4 (app/ 是 obsolete artifact) 是该 doc Created 时基于 dev-source HCL 推断的;Phase A.4 + A.6 live probe 推翻了两项。

**新事实**:
- `/opt/aria-orchestrator/hermes-data/` 不存在不是 bug — prod 用 `raw_exec`(非 docker),不挂载该路径。Hermes state 在 `/root/.hermes/`(active, last write 06:06 UTC)
- `/opt/aria-orchestrator/app/` 不是 obsolete — `aria-heartbeat` cron(`48ed7e826bc3`)每 60min 调用 `./scan.sh /opt/aria-orchestrator/app --json`,995 次成功 run。**DO NOT delete during Phase B/C**

**根因**: Investigation 由"读源码 HCL + 推断"完成,没逐项验证。Phase A 通过"读 Nomad live job spec + ls 主机 fs + cat cron jobs.json"才发现。

**实战教训** (memorialize 候选, 见 §4): `feedback_prod_state_must_ground_playbook` (predecessor §4 §1 候选, 本 session 第 2 次激活,这次自己又踩了一遍 — investigation 也是"AI 推断不实地"的复发,只是范围更小)。

### R2 — OD-3 重定义 (原 OD-3 自然消解,新 OD-3 = Hermes-cron 验证)

**原 OD-3** (v2 playbook 顶部 §OD-3): hermes-data mount missing
**新 OD-3** (本 session AskUserQuestion-backed): aria-layer1 plugin entry-point 是否 register hermes-internal cron, OD-2 (b) Pure Nomad 前置

**Resolution**: M5 source v0.4.0 `__init__.py:60-70` 已是 explicit no-op stub(AD-M2-7 / 2026-05-02 M2 deploy pivot)。Prod 现 v0.2.0 also 不注册 aria-layer1 cron(jobs.json 仅 aria-heartbeat)。**Pure Nomad upgrade 自然干净,零 double-cron risk**。

**下次类似 deploy prep 用 pattern**: deploy playbook 起草后, 必须把 "ssh prod + cat live config + ls fs" 加入 Phase A,**不能跳过**。Investigation doc 本身就是这个 pattern 的产物, 但 §2 ambiguities 还是逃过, 验证 pattern 需细化到逐项 OD。

### R3 — git stash 不 stash submodule pointer-only changes (Phase A.3 silent caveat)

**事件**: `git -C /root/Aria stash push` 报 "No local changes to save" 即使 `git status` 显示 `M aria-orchestrator`。

**根因**: Default `git stash` 不 capture submodule pointer 变更,需 `git stash push --include-untracked --keep-index` 等组合, 或显式 `git update-index --add aria-orchestrator` 后再 stash。

**Mitigation 已用**: Backup branch `backup/pre-m5-upgrade-20260520T055622` 锁住 parent index `aria-orchestrator @ e0cc6de`。working tree 的 `5467991` SHA preserved in:
1. Phase A snapshot doc (注 + commit `54679910de6b3c06d8ee5fc9d611493c122c51f4`)
2. Investigation §2.3 (历史)
3. aria-orchestrator submodule `.git/` 本地 clone(reflog)

**Lesson 候选** (low priority): `feedback_git_stash_skips_submodule_pointer` — pointer-only submodule M 不能用 default stash 保存,显式 `git diff aria-orchestrator > /tmp/...` patch 才稳。

### R4 — Concurrent terminal awareness 仍 active (本 session 实测 2 race — 10:15 amendment)

**Pre-A.5 (07:30 之前)**: `simonfish/dev-claude2` 终端在 ~04:50 UTC ship 完 v1.22.0 + multi-terminal-coordination archive 后已 quiesce。

**Post-A.5 (07:35 + 10:02)**: 在 Phase A 收尾 push + Phase A.7 push 时连续 2 次撞上 `simonfish/dev-claude2` 的并发 push (`a2d06e7` v1.22.1 hotfix + `34a1ce7` D.3 update),均 clean rebase 解决,零 file conflict。这是 multi-terminal-coordination Spec 要解决的场景的第 7、8 次连续 dogfood (前 6 次记录在 Track A handoff)。

**Mitigation 持续**: 提交前 `git fetch` + Rule #8 gate + push 前 multi-remote parity verify (per `feedback_sequenced_multirepo_gitlink_bump` + `feedback_concurrent_edit_clean_rebase_pattern`)。Future v1.22.x Layer L claim/reconcile 实施后, 这种 race 会更早被 awareness。

### R5 — Phase A.7 dry-run 3 advisories (Phase B 必读 — 10:15 amendment)

Phase A.7 dry-run validation (零 prod 写) surface 了 3 个 Phase B 需要 inline 处理的 advisory (详见 `.aria/notes/m5-deploy-phase-a7-dry-run-2026-05-20.md`):

1. **HCL ambiguity trap** (CRITICAL): `aria-orchestrator.nomad.hcl` 是 docker 变体 (task name `hermes`), `aria-orchestrator-light.nomad.hcl` 才是 prod raw_exec 变体 (task `hermes-gateway`)。Phase B Step 5 `nomad job restart aria-orchestrator` 不 re-apply HCL → 安全;但若以后任何 `nomad job run` 必用 `-light` 后缀,否则会 flip prod driver。
2. **005 migration row count assert** (MEDIUM): Migration 005 `_schema_v4_drop_inline_uq.sql` 用 SQLite 标准 DROP CONSTRAINT workaround (CREATE TABLE new + copy + RENAME),对 16 prod rows 全表 rebuild。Phase B Step 4 必须在 005 应用后 assert `SELECT COUNT(*) FROM dispatches = 16`,否则视为 copy 步骤数据丢失,立即 rollback 至 A.2 snapshot。
3. **M1_VALIDATOR_PATH file** (LOW, non-blocker): 新 cron HCL 引用 `/opt/aether-volumes/aria-layer1/data/validate-issue-schema.py` (env block default)。Nomad var 若未设此 key 且 host 文件 missing,job start 不 block 但首 tick 触发 validator 调用会 fail。Phase B Step 7 smoke 加 validator 文件 existence 检查 OR Nomad var `M1_VALIDATOR_PATH=` 显式置空 skip。

3 个 advisory 都 surface 在 Phase A.7 dry-run note 内 + 本 §3 R5。新 session 启 Phase B 前先读这两处。

---

## §4 实战教训 (memory 沉淀候选 — 由 owner review 决定文字)

**未写入 MEMORY.md 的本 session 候选**:

1. **`feedback_prod_state_must_ground_playbook` (re-激活, NOT 新)**: predecessor §4 已 surface 此候选,本 session 第 2 次激活 — investigation doc 自己也踩了一遍(§2.2 + §2.4 错判)。Owner 是否本 session 写入 MEMORY.md,或继续 defer 直到 Phase B 结束再回头看?
2. **`feedback_layered_od_resolution_with_live_probe` (新)**: Owner OD 不是 one-shot, 当 OD 假设依赖 prod state 时,**先 Phase A live probe 再 prompt OD-N 的细化版**。本 session OD-3 重定义 + OD-4 reclassification 实证 — original AskUserQuestion 4-batch 之后,A.4 live data 强制 OD-3 (i) sub-question,A.6 supplement 又强制 OD-4 reclassify。
3. **`feedback_git_stash_skips_submodule_pointer` (低, 通用 Git 知识)**: 已在 §3 R3 记录, owner 决定是否单独 MEMORY 入口。

**reused/reinforced**:
- `feedback_secrets_never_in_conversation` — 本 session 全 Rule #7 hygiene (Python wrapper 限定 env keys / template DestPath / no value reads)
- `feedback_aether_tool_discovery_flow` — Rule #8 `aether ci status --branch master --in-flight --json` GREEN (1 次, pre-commit)
- `feedback_concurrent_edit_clean_rebase_pattern` — 本 session 0 race (`simonfish/dev-claude2` 已 quiesce)
- `feedback_audit_driven_fix_conventions` — 本 commit message 拟 prose-rich

---

## §5 多维度同步状态

| 维度 | 本 session 涉及? | 状态 |
|------|------------------|------|
| UPM | no | N/A (Aria 主仓不使用 UPM) |
| User Stories | no | US-025 unchanged (in_progress, O1+O2 pending — same as predecessor) |
| OpenSpec | no | 无活跃 Spec |
| PRD | no | unchanged |
| Standards / conventions | no | unchanged |
| Skill docs | no | unchanged (aria-plugin v1.22.0 in submodule, 不动 source) |
| Architecture docs | no | unchanged |
| Auto-memory | 0 new (3 candidates surfaced §4) | Cumulative ~138 entries |
| Decision memos | 0 new (5 OD 写在 `.aria/notes/m5-deploy-od-decisions-2026-05-20.md`,非 `.aria/decisions/` 因为 deploy-specific, 不通用) | — |
| Audit reports | 0 new | — |
| Production DB | **read-only snapshot only** | dispatches.db 16 rows preserved, snapshot at /tmp/...20260520T055525/ |
| Production source tree | **read-only** | /root/Aria still on feature/aria-2.0-m2-layer1-state-machine, no checkout/pull |
| Cross-project coordination | yes (light-1 SSH 7 round-trips) | All read-only, Rule #7 hygiene maintained |
| Multi-remote parity | ✅ N/A this session (no push yet — about to commit then push) | will verify post-push |
| Forgejo issue backlog | no | 13 open (unchanged from predecessor) |

---

## §6 Next session 入口 + 优先级建议

```bash
# Path A: 推 Phase B (full M5 deploy Layer 1) — Phase A 5 OD + 4 reframe + 3 advisory 已就绪
# 1. 读取顺序 (本 doc + 4 notes, 10:15 amendment 完整):
cat docs/handoff/2026-05-20-m5-phase-a-snapshot-done.md       # 本 doc (此 amendment)
cat .aria/notes/m5-deploy-od-decisions-2026-05-20.md           # 5 OD
cat .aria/notes/m5-deploy-phase-a-snapshot-2026-05-20.md       # DB + backup + checklist
cat .aria/notes/prod-job-spec-live-2026-05-20.md               # Live Nomad spec
cat .aria/notes/m5-deploy-phase-a7-dry-run-2026-05-20.md       # 3 Phase B advisories (HCL trap / 005 assert / validator path)
# 2. 走 v2 playbook §Phase B Step 1-8 + inline §3 R5 三 advisories
# 3. ~2-3h dedicated session, prod-write (Phase B 是真正首次 prod 写 — 5 OD 锁定且 3 advisories 处理后风险已最小)
# 4. 完成后 Phase D archive + handoff (Phase B done)

# Path B: 不推 Phase B, 做别的 backlog
/aria:state-scanner   # 会自动 surface 本 doc, 转 Tier 2/3/4
```

**优先级建议** (本 session 视角):

1. ⭐ **Path A (Phase B execution)** — US-025 close gate 真正主线;Phase A 已锁所有前置,执行风险已最小化
2. **Tier 2 state-scanner family** (#58/#89/#90/#79) — 可独立 session,与 Phase B 不冲突
3. **Tier 3 secret-hygiene** (#84/#107) — 同上
4. **Tier 4/5/6** 等

**不应该做的**:
- ❌ 不要跳过本 doc + 3 notes 直接进 Phase B(5 OD 必读)
- ❌ 不要 unilaterally 在 Phase A 5 OD 上 second-guess(已 AskUserQuestion-backed locked)
- ❌ 不要 delete `/opt/aria-orchestrator/app/`(reframe: active by aria-heartbeat)
- ❌ 不要试图 cleanup `/root/.hermes/cron/output/<旧 7 个 hash>/`(虽然死掉但是诊断价值,留给 GC session)

---

## §7 提交清单 (commit hash + multi-remote parity)

**Pre-commit Rule #8 gates this session**: 3 invocations, all `runs: []` GREEN (pre-`34106d1` + pre-`54c2488` + pre-本-amendment)

**Aria main commits this session** (in order):
- `34106d1` docs(handoff): M5 T-deploy Phase A snapshot done — 5 OD locked + 4 prod reframes + zero prod mutation
- `54c2488` docs(handoff): Phase A.7 dry-run validation — 0 blockers + 3 advisories for Phase B
- (本 amendment commit, 即将) docs(handoff): M5 Phase A handoff 10:15 amendment — A.7 + memory + races + Q3 audit

**3-way SHA parity (post-本-commit target)**:
- Aria main: master push to `origin` + `github`
- aria submodule: `62c324978333d1ffacde0a20436043e96f257f4c` (v1.22.1 hotfix, by `simonfish/dev-claude2`)
- aria-orchestrator submodule: `962cb56c1bbec46ff20783bfa909beb312d5eb85` (HCL registry-lock)
- standards submodule: `16041f4df2f9ff2f4a6a6cb8a1cd8c40b92048c1` (Layer H schema)

**Q1 closeout audit** (10:10 UTC): ALL 4 repos 3-way SHA parity verified ✅ (`git ls-remote` + `git rev-parse HEAD` per repo)

**No regression**:
- 0 prod modifications (snapshot + backup + read-only inspect + read-only HCL validate only)
- 0 code/test/skill changes (only handoff doc + advisory notes)
- aria-plugin tests: untouched (no source change)
- aria submodule auto-bumped to v1.22.1 via rebase (orthogonal track A's commit, not our work)

---

## §8 Memory entries this session (2 committed harness, 1 skipped — 10:15 amendment)

本 session 10:00 决策 — auto-advance 阶段 commit 了 2/3 candidates 到 harness 持久化 memory store (`~/.claude/projects/-home-dev-Aria/memory/`,非 repo):

1. **`feedback_prod_state_must_ground_playbook.md`** ✅ — **amended** existing entry with second activation note (Phase A 中 investigation doc §2.2 + §2.4 自己也被 live probe 推翻 — meta-instance 强化 lesson "investigation doc 不 immutable")
2. **`feedback_layered_od_resolution_with_live_probe.md`** ✅ — **new** entry + MEMORY.md index line。Universal lesson: Owner OD 不 one-shot, prod-state-dependent OD 需 Phase A live probe 后细化 sub-prompt;两轮 OD 比单轮稳。Source incident = 本 session OD-3 重定义 + OD-4 reclassify
3. **`feedback_git_stash_skips_submodule_pointer`** ❌ **skipped** — 通用 Git 知识, 不属"项目特有教训", per CLAUDE.md memory rules "Don't save what repo already records"

**Cumulative MEMORY.md count**: ~139 entries (+1 new this session)。

**Q2 audit** (10:10 UTC): 无未沉淀的经验。HCL ambiguity / multi-terminal race / Rule #7 hygiene pattern 都已被现有 memory 覆盖 (`feedback_nomad_hcl_validate_early` / `feedback_concurrent_edit_clean_rebase_pattern` / `feedback_nomad_inspect_secret_leak`)。

---

## Cross-references

- **Predecessor (Track B same line)**: [`2026-05-20-session-final-o1-paused-with-v2-playbook.md`](2026-05-20-session-final-o1-paused-with-v2-playbook.md) — same track-id, predecessor "paused with v2 playbook ready", 本 session 是该 v2 playbook 的 Phase A 实地执行
- **Parallel track (orthogonal, done)**: [`2026-05-20-multi-terminal-coordination-v1220-shipped.md`](2026-05-20-multi-terminal-coordination-v1220-shipped.md) — `simonfish/dev-claude2`,本 session 启动时已 quiesce
- **🎯 MUST READ before Phase B**: 本 doc § + 3 `.aria/notes/...2026-05-20.md`(见 §0 入口)
- **🎯 MUST USE for Phase B**: [`2026-05-20-m5-deploy-playbook-v2-accurate.md`](2026-05-20-m5-deploy-playbook-v2-accurate.md) §Phase B Step 1-8,但 §OD-3 / §OD-4 假设需用本 doc §3 R1 替换
- **DEPLOYMENT.md** (live source at `aria-orchestrator/hermes-extensions/aria-layer1/DEPLOYMENT.md`) — AD-M2-7 canonical pattern,本 session A.6 source review 引用
- **Layer H frontmatter schema (standards SoT)**: `standards/conventions/session-handoff.md §2.3` (v1.1.0)
- **Rule #9 trigger eval (本 session)**: **MODERATE** — session ~2h cumulative (NOT > 4h L1), 0 cycles shipped (NOT ≥ 2 L2), 1 phase touched (Phase A only, NOT ≥ 2 L3 distinct), 但 substantial 5 OD + 4 reframe + 16 dispatch ID + DB snapshot + backup + Rule #7 hygiene + Phase B gate 决定 — L4 user prompt yes (track-B continuation needs explicit handoff). Handoff doc 写出。

---

**Created**: 2026-05-20 ~07:32 UTC (post-A.5-sign-off, pre-`34106d1`-commit)
**Amended**: 2026-05-20 ~10:15 UTC (post-A.7-dry-run + post-Q1-Q4-audit, pre-amendment-commit)
**Session duration**: ~4.5h cumulative (07:32 amendment trigger + 2h pre-amendment work)
**Status**: Paused — Phase A.7 done (Phase A + dry-run derisking), Phase B ready in next dedicated session
**Next session entry**: Path A (Phase B 推 deploy) 或 Path B (do other backlog) — owner 决定。**优先级 ⭐ Path A** — US-025 close gate 主线, Phase A + A.7 derisking 已让 Phase B 风险降到可接受。

---

## Q1-Q4 closeout audit summary (10:15 UTC)

| Q | 问 | 答 |
|---|---|---|
| Q1 | 本地 vs 远程仓库同步? | ✅ ALL 4 repos 3-way SHA parity (Aria main `54c2488` + aria `62c3249` + standards `16041f4` + aria-orchestrator `962cb56`)。工作树 clean。 |
| Q2 | 未完成 task / 讨论? | 无 in-scope incomplete。Phase B 是 deferred-by-design (owner Path A 选择 wrap clean),非本 session 任务。Q2 唯一 gap = handoff doc 本身 stale → 本 amendment 已 fix。 |
| Q3 | UPM / US / Spec / PRD 维度? | UPM N/A (Aria 主仓 不用)。US-025 + US-026 status 已含 2026-05-20 update note 指向 v2 playbook + investigation (predecessor session 完成的)。M5 main Spec Approved + T-deploy tasks 6.17-6.30 全 unchecked (owner-runnable) — Phase A 是 pre-6.17 derisking,**不对应任何 sub-task**, tasks.md 不需更新 ✅。PRD unchanged。 |
| Q4 | 收尾交接? | ✅ 本 amendment commit 后,新 session 走 `/aria:state-scanner` Phase 1.15 collector 会自动 surface `docs/handoff/latest.md` → 本 doc (Track B latest entry)。读完本 doc + 4 notes 即可推 Phase B 或转其他 backlog。 |
