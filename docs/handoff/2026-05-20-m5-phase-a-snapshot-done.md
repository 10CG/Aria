---
track-id: aria-2-0-m5-replay-reconciler-drift-review-loop-audit
owner-container: simonfish/dev-claude
phase: A
status: paused
updated-at: 2026-05-20T07:32:01Z
---

# Aria — Session Handoff (2026-05-20 ~07:30 UTC) — M5 T-deploy Phase A done, Phase B gated

> **Status**: Paused — Phase A 5 OD resolved + 4 prod findings + zero prod mutation; Phase B (~2-3h prod-write) gated to next dedicated session
> **Predecessor handoff**: [`2026-05-20-session-final-o1-paused-with-v2-playbook.md`](2026-05-20-session-final-o1-paused-with-v2-playbook.md) — same track, the v2 playbook this session executed Phase A against
> **Next session 入口**: 优先读本 doc → §6 → Phase B 直接走 v2 playbook §Phase B 步骤 1-8 (5 OD 已锁,4 prod findings 已 reframe)

---

## §0 入口 (新 session 优先读)

新 session 读取顺序硬约束 (如果你要推 Phase B):

1. **本 doc** (你正在读) — 锁 5 OD + 4 reframe + DB snapshot path + backup branch name
2. **`.aria/notes/m5-deploy-od-decisions-2026-05-20.md`** — 5 OD 决策正式记录 (AskUserQuestion-backed)
3. **`.aria/notes/m5-deploy-phase-a-snapshot-2026-05-20.md`** — DB 快照 + 16 dispatch IDs + backup branch + sign-off checklist
4. **`.aria/notes/prod-job-spec-live-2026-05-20.md`** — Live Nomad spec (Rule #7 scrubbed)
5. Optional: `2026-05-20-prod-state-investigation.md` (Phase A reframes 2 of its §2 finding 顺序 — 见 §3 R1)
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

### R4 — Concurrent terminal awareness 仍 active (本 session 实测 0 race)

**预期对照**: `simonfish/dev-claude2` 终端在 ~04:50 UTC ship 完 v1.22.0 + multi-terminal-coordination archive 后,本 session ~05:48 UTC 启动时已经 quiesce。本 session 全程未与另一终端发生 push reject。

**Mitigation 持续**: 提交前 `git fetch` + Rule #8 gate + push 前 multi-remote parity verify (per `feedback_sequenced_multirepo_gitlink_bump`)。

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
# Path A: 推 Phase B (full M5 deploy Layer 1) — Phase A 5 OD + 4 reframe 已就绪
# 1. 读取顺序:
cat docs/handoff/2026-05-20-m5-phase-a-snapshot-done.md       # 本 doc
cat .aria/notes/m5-deploy-od-decisions-2026-05-20.md           # 5 OD
cat .aria/notes/m5-deploy-phase-a-snapshot-2026-05-20.md       # DB + backup + checklist
cat .aria/notes/prod-job-spec-live-2026-05-20.md               # Live Nomad spec
# 2. 走 v2 playbook §Phase B Step 1-8 (5 OD 已锁, 不再 prompt)
# 3. ~2-3h dedicated session, prod-write
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

**Pre-commit Rule #8 gate**: ✅ `aether ci status --branch master --in-flight --json` returned `runs: []` GREEN (07:30 UTC)

**This session's Aria main commit** (即将):
- `docs(handoff): M5 Phase A snapshot done — 5 OD locked + 4 prod reframes + DB/backup ready for Phase B`

**Pre-commit state** (about to commit):
```
?? .aria/notes/m5-deploy-od-decisions-2026-05-20.md
?? .aria/notes/m5-deploy-phase-a-snapshot-2026-05-20.md
?? .aria/notes/prod-job-spec-live-2026-05-20.md
+  docs/handoff/2026-05-20-m5-phase-a-snapshot-done.md   (本 doc)
+  docs/handoff/latest.md   (updated to add Track B Phase A entry)
```

**Pre-push state target** (3-way SHA parity, multi-remote):
- Aria main: master push to `origin` + `github`
- aria submodule: unchanged this session (still at `ce58d35` v1.22.0)
- aria-orchestrator submodule: unchanged this session (still at `962cb56`)
- standards submodule: unchanged this session (still at `16041f4`)

**No regression**:
- 0 prod modifications (snapshot + backup + read-only inspect only)
- 0 code/test/skill changes
- aria-plugin tests: untouched (no submodule bump)

---

## §8 Memory entries this session (0 new committed; 3 candidates surfaced)

本 session committed 0 new MEMORY.md entries(沿用 predecessor pattern — 先 in handoff, owner review 后再决定文字)。

**3 candidates** for owner decision (内容见 §4):
1. `feedback_prod_state_must_ground_playbook` (re-激活, predecessor §4 同候选;本 session 第 2 次激活 — owner 是否本 session 写入,或继续 defer 到 Phase B 后再总成 1 条?)
2. `feedback_layered_od_resolution_with_live_probe` (新, medium-high) — OD 不是 one-shot, prod-state-dependent OD 需 live probe 后细化 sub-prompt
3. `feedback_git_stash_skips_submodule_pointer` (低, 通用 Git 知识) — backup branch 是更稳的 submodule pointer M 保留方式

**Cumulative MEMORY.md count**: ~138 entries (unchanged this session).

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

**Created**: 2026-05-20 ~07:32 UTC (post-A.5-sign-off, pre-本-commit)
**Session duration**: ~2h (focused, no fatigue overlap with predecessor's 16h)
**Status**: Paused — Phase A done, Phase B ready in next dedicated session
**Next session entry**: Path A (Phase B 推 deploy) 或 Path B (do other backlog) — owner 决定
