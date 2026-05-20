---
track-id: aria-2-0-m5-replay-reconciler-drift-review-loop-audit
owner-container: simonfish/dev-claude2
phase: B
status: active
updated-at: 2026-05-20T14:01:23Z
---

# Aria — Session Handoff (2026-05-20 ~14:00 UTC) — M5 T-deploy Phase B SHIPPED (Layer 1 only)

> **Status**: Active — Phase B complete (Layer 1 deploy + schema v4.2 + 2 new Nomad jobs + Smoke A/B/C PASS); Phase C (Layer 2 image + real dispatch smoke + Tier-1 live LLM) carry-forward to next dedicated ~2h session, gated to ≥24h Phase B observation
> **Predecessor handoff**: [`2026-05-20-m5-phase-a-snapshot-done.md`](2026-05-20-m5-phase-a-snapshot-done.md) — same track, Phase A snapshot + A.7 dry-run + 5 OD locked + 4 prod reframes
> **Cross-container note**: Phase A 由 `simonfish/dev-claude` 起,Phase B 由 `simonfish/dev-claude2` 完成(self-multi-container 场景 per §2.3.5 — 🟡 soft hint, 同 owner 跨容器,无需 yield)
> **Next session 入口**: 优先读本 doc → §6 → Phase C(Layer 2 image build + real dispatch smoke)gated to ≥24h Phase B 稳定后

---

## §0 入口 (新 session 优先读)

新 session 读取顺序硬约束:

1. **本 doc** (你正在读) — Phase B 全部 deliverables + Phase C carry-forward + 3 浮出 advisories(M1 handoff missing / auto-migration meta-lesson / Lark connect timeout)
2. **Predecessor `2026-05-20-m5-phase-a-snapshot-done.md`** — Phase A 5 OD + 3 dry-run advisories(本 session 已全 inline 处理)
3. **`docs/handoff/2026-05-20-m5-deploy-playbook-v2-accurate.md`** §Phase C — Layer 2 image build playbook(本 session 未触及,carry-forward)
4. **Predecessor's `.aria/notes/m5-deploy-phase-a*` 4 文件** — Phase A baseline 仍 forensically 相关(尤其 phase-a-snapshot 内 dispatch ID 列表 + backup branch path)

读完后:**Phase C 推进条件 = Phase B ≥24h 稳定观察**(reconcile + cron 自然 tick × N 次 0 error)。可转 Path B (Tier 2 state-scanner family) 或其它 backlog 填空窗口。

**架构 awareness** (本 session 后):
- `/root/Aria` (light-1 prod) `master` @ `244151e` (与 dev container parity)
- 3 子模块 @ `aria=62c3249 / aria-orchestrator=962cb56 / standards=16041f4` (与 dev container parity)
- aria-layer1 prod 包版本: **v0.4.0** (pip editable from `/root/Aria/aria-orchestrator/hermes-extensions/aria-layer1`)
- dispatches.db schema: **v4.2** (16 rows, integrity ok, all 16 issue_ids preserved)
- Nomad jobs running: aria-orchestrator (Hermes), aria-layer1-reconcile (periodic 30min), aria-layer1-cron (periodic 60min), aria-layer1-comment-poll (periodic 60s)

---

## §1 已完成 (按时间顺序)

| 时间 (UTC) | 事件 | 备注 |
|-----------|------|------|
| 13:01 | Pre-flight: SSH light-1 connectivity + git state + dispatches.db baseline (16 rows / schema 3.0) + backup branch + Phase A `/tmp/` snapshot 全 ✅ | Phase A 所有锁定前置仍成立 |
| 13:10 | **B.1 Reset uncommitted M aria-orchestrator** (OD-1 a): `git submodule update --init aria-orchestrator` → pointer 恢复到 `e0cc6de` 匹配 gitlink(M3 bump `5467991` discarded) | submodule 内残留 `egg-info/` untracked,B.3 会 overwrite |
| 13:10 | **B.2 Single-leap to master** (OD-5 a): `git checkout master + pull --ff-only + submodule update --init --recursive --remote` → HEAD `e416920` → **`244151e`**(258 → 246 → 0 commits behind),3 子模块 SHA 全部匹配 dev container | 与 multi-terminal-coordination v1.22.0 ship 后的 dev 状态精确同步 |
| 13:10 | **B.3 Refresh editable install**: `pip install -e .` aria-layer1 → **v0.4.0** ✅ | venv 内 schema_migrate + 5 migration files (002-006) present |
| ~13:17 | **B.4 自动触发的 schema migration v3.0 → v4.2** ⚠ | comment-poll Nomad periodic (60s cadence) 在 B.3 完成 ~7min 后 tick 一次,以新 editable v0.4.0 启动 → 在 startup 路径自动 invoke `apply_migrations()` → 004 + 005 + 006 全应用,时间戳 `2026-05-20T13:17:33Z` |
| 13:18 | B.4 safeguards 1+2 + dry-run on /tmp/ copy → 三层验证(integrity ok / row count 16 / schema 4.2 / spec_id + risk_tier + 4 rework_* + audit_log table) | playbook B.4 顺序被 auto-migration 旁路,但 outcome 正确 |
| 13:19 | B.4 forensic: 16 issue_ids match Phase A baseline exactly + state distribution (15 S_FAIL + 1 S9_CLOSE) + migration_notes 004/005/006 timestamps + Phase A pre-migration `/tmp/` snapshot 仍 pristine (schema 3.0, 34 cols) | data integrity 完全 verified |
| 13:20 | B.4 durable backup move: `cp -a /tmp/aria-layer1-snapshot-20260520T055525/dispatches.db.pre-m5 → /opt/aether-volumes/aria-layer1/data/backups/dispatches.db.pre-m5-v3.0.20260520T055525` | rollback 资产 reboot-safe;durable backups dir 共 4 文件(pre-m4 + pre-m5-v3.0 + 2x pre-v4.2) |
| 13:22 | **B.5 Nomad var key inventory** (Rule #7 — go-template keys only,playbook `-out=keys` flag stale 已修): 8 existing keys ok;5 M5 feature flags missing 但 Python defaults 兜底 (3/70/0.7/0/0 = playbook 推荐值);M1_VALIDATOR_PATH missing | R5.3 active |
| 13:23 | B.5 R5.3 mitigation: `cp /root/Aria/openspec/archive/2026-04-23-aria-2.0-m1-mvp/artifacts/validate-issue-schema.py → /opt/aether-volumes/aria-layer1/data/validate-issue-schema.py` + chmod 0755 | M1 validator install,cron 首 tick 不会 fail |
| 13:24 | **B.6 Hermes restart** (raw_exec in-place, R5.1 safe): `nomad job restart -on-error=fail -yes aria-orchestrator` → `Job restarted successfully!` + Deployment Healthy=1 + Modified 29s ago(同 alloc id `d43c2a7e` — raw_exec restart-in-place 正常) | Hermes Gateway banner 表明 fresh start;pre-existing zai 429 余额耗尽 + Lark connect timeout 浮出,non-blocking |
| 13:25 | **B.7 Deploy aria-layer1-reconcile + aria-layer1-cron** (OD-2 b): 2x `nomad job validate` ✅ + 2x `nomad job run` ✅ | 意外发现:两 job 都早于今日(reconcile 自 2026-05-09 已部署,~521 dead children;cron 也有 418 dead children),实为 **M4→M5 HCL upgrade**,non playbook 假设的 fresh deploy |
| 13:27 | **B.8 Smoke A + B**: `nomad job periodic force` 立即触发两 job → 都 Complete 状态 | reconcile output `{stuck_rows_found: 0, ..., s7_decided_advance_ok: 0}` + log `AriaLayer1Extension initialized (db=...)` + `reconciler pass complete` 全 ✅;cron output `{processed: 0, skipped: 0, failed: 0, seeded: 0}` + log `Phase 1: lazy-wired ForgejoCliClient (org=10CG repo=Aria)` ✅;cron 浮出 **新 advisory**:`m1-handoff.yaml not found at /opt/.../data/, using sentinel image_sha` |
| 13:55 | **B.8 Smoke C** (synthetic SQL-inject + v4.2 cols + cleanup): INSERT 1 row with full M5 col set (risk_tier='always' / spec_id='M5-T-DEPLOY-SMOKE' / rework_round=0 / image_sha='sha256:smoke-phase-b-synthetic' / fail_reason='smoke_test_synthetic') → 16→17 → force reconcile (stuck_rows_found=0 ✅ terminal guard works) → DELETE → 17→16 → 16 issue_ids match Phase A baseline exactly | full v4.2 schema acceptance + terminal-state guard + reconciler tolerance 全 ✅;0 net prod row change |
| 14:00 | **B.9 Phase D writeback**: 本 doc + Aria main commit + push + multi-remote SHA parity verify | (即将) |

**Cycles shipped this session**: **Phase B of M5 deploy** (US-025 close gate Layer 1 portion);未 ship 完整 OpenSpec Spec cycle(Phase A/B/C/D 横跨多 session,US-025 close 等 Phase C)。

**累计 Phase B deliverables**: 3 prod state changes (git pull + pip editable v0.4.0 + schema v4.2 migration via auto-trigger) + 2 Nomad job HCL upgrades (M4→M5) + 1 M1 validator file install + 1 durable backup move + 0 net DB row delta + 3 smoke verifications + 0 errors。

---

## §2 未完成 / Carry-forward 清单

### Owner-gated 执行 (US-025 close gate — Track B 主线 Phase C)

| # | 项目 | 状态 | 备注 |
|---|------|------|------|
| **O1c** | **Phase C: Layer 2 image v11 build + real Layer 2 smoke** (v2 playbook §Phase C) | **READY** — Phase B 稳定 ≥24h 后即可启动 | ~2h dedicated session;aria-build container 镜像构建 + 推送 + sha pin + real Layer 2 dispatch smoke(force-push / close-old-PR / commit-lint retry)替换 SQL-inject |
| O2 | Tier-1 live LLM gates(B.1.live failure_analysis + C.2.live spec_drift) | gated to Phase C 末或独立 session | ~5min, ~¥0.10 cost;set `ARIA_FAILURE_ANALYSIS_ENABLED=1` + `ARIA_SPEC_DRIFT_ENABLED=1` 后 reconciler 自动调用 |
| O3 | Tier-2 accumulation(≥3 real workload dispatches with ≥1 each changes/redo/reject) | passive,无 scripted action | owner 正常工作积累 |

### Phase C 进入前必读 prerequisites (本 doc + 本 session 已 cover)

| 资源 | 用途 |
|------|------|
| 本 doc §1 表 | Phase B 全 deliverables + outcome verification |
| 本 doc §3 R6 | M1 handoff yaml gap(Phase C 强相关——Layer 2 dispatch 需要 m1-handoff.yaml::image_sha_final 指向新 v11 image) |
| `docs/handoff/2026-05-20-m5-deploy-playbook-v2-accurate.md` §Phase C | Layer 2 image build playbook framework(本 session 未触及) |

### 非阻塞 backlog (Forgejo,继承自 predecessor)

| Tier | 状态 |
|------|------|
| **Tier 1** (v1.21.4 patch) | ✅ DONE (predecessor) |
| **Tier 2** (state-scanner family: #58/#89/#90/#79) | 可推 — Phase B 24h 观察窗口的 natural fill |
| **Tier 3** (secret-hygiene #84/#107) | 可推 |
| **Tier 4** (audit rubric #54/#95) | Level 2-3 |
| **Tier 5** (proposals #59/#104/#111) | 待 owner OD |
| **Tier 6** (远期 #5/#32) | 远期 |

---

## §3 关键风险 / 已知陷阱

### R6 — m1-handoff.yaml missing at prod (cron 浮出, Phase C 阻塞)

**事件**: B.8 cron Smoke 浮出 `WARNING: M1 handoff not found at /opt/aether-volumes/aria-layer1/data/m1-handoff.yaml; using sentinel image_sha`

**Source 位置**: `/root/Aria/aria-orchestrator/docs/m1-handoff.yaml`(已 checkout 到 prod git tree,但未 cp 到 data dir)。

**当前影响**: 本 session 0 dispatches seeded by cron(processed=0),sentinel image_sha 未被实际使用。

**Phase C 阻塞**: Layer 2 image build 完成后必须更新 `aria-orchestrator/docs/m1-handoff.yaml::image_sha_final` → 新 v11 image SHA → cp 到 `/opt/aether-volumes/aria-layer1/data/m1-handoff.yaml`。若不修复,任何 Phase B 之后新出现的 Forgejo issue 被 cron 尝试 seed 时会用 sentinel SHA → Layer 2 dispatch fail → 该 dispatch row 进 S_FAIL(infrastructure)。

**Mitigation 候选**:
- (a) Phase C 处理时一并 install(自然修复;recommended)
- (b) Phase B 后立刻 install 当前 source 版(M4-era image SHA,Phase B → Phase C 间窗口 Layer 2 仍可 dispatch 老镜像)
- (c) 全局 disable cron 直到 Phase C(简单,但 Phase B 期间手工 dispatch 路径也不可用)

**Recommendation**: (a) — Phase B ≥24h 观察期内 Forgejo 不期待新 issue,sentinel 不会 fire;Phase C 自然修复。

### R7 — auto-migration via pip editable + periodic Nomad jobs (meta-lesson)

**事件**: B.3 pip install 后 ~7min,comment-poll Nomad periodic (60s cadence) tick 一次,以新 editable v0.4.0 启动 → 在 `_get_db_connection` / module init 路径 invoke `apply_migrations()` → 004 + 005 + 006 全应用,**bypass playbook §B.4 显式 3-safeguard gate**。

**实战教训**:
> Pip editable install (`pip install -e .`) on a host with **running periodic Nomad jobs** that import the package → next tick automatically picks up new code → migrations run **immediately, not deferred to Hermes restart or explicit invocation**.

**playbook 修正建议**(for 未来 deploy):
- Pattern 1: 先 `nomad job stop` periodic jobs → pip install → explicit migration gate → `nomad job start` periodic jobs
- Pattern 2: 接受 auto-migration,删除 playbook B.4 显式步骤,把 safeguards 改为 post-hoc verification
- Pattern 3: 在 apply_migrations 函数加 `ARIA_MIGRATION_LOCK` env gate,部署中开锁,正常运行关锁

本 session 选择: outcome 正确 + 旁路无害,memory entry 记录 lesson,playbook 文字下次修订时改。

### R8 — Pre-existing zai 429 余额耗尽 + Lark connect timeout (non-blocking, surfaced)

**zai 429**: `aria-heartbeat` cron 每 60min 调用 `glm-4.5-air` model,余额耗尽,所有 call 失败。Phase B Layer 1 reconcile/cron **不依赖** zai LLM(只在 ARIA_FAILURE_ANALYSIS_ENABLED + ARIA_SPEC_DRIFT_ENABLED gated path),所以不阻塞。Phase D Tier-1 live LLM gates(O2)需要余额充足或先 recharge。

**Lark timeout**: Feishu webhook/messaging 连接 handshake 超时。Layer 1 reconcile/cron 不依赖 Lark(notification 是 ops-alert 通道)。

**两者都 pre-existing**,非本 session 引入;non-blocking for Phase B sign-off。

### R1-R5 (predecessor — for reference)

predecessor handoff §3 R1-R5 全部已在本 session inline 处理 / 验证:
- R1 (investigation reframe): Phase A 已闭合,本 session B.7 多发现 reconcile + cron HCL 早已部署(M4-era), 进一步 reinforce "investigation 不 immutable" 教训
- R2 (OD-3 redefine): Phase A 闭合,Pure Nomad 自然干净 — 本 session B.7 确认(comment-poll 早是 Nomad,reconcile + cron HCL 也已 Nomad-deployed)
- R3 (git stash submodule pointer): Phase A 已 mitigated by backup branch,本 session 无新触发
- R4 (multi-terminal awareness): 本 session 0 race(Track A 已 quiesce, dev-claude2 内单独工作)
- R5.1 (HCL ambiguity docker vs raw_exec): B.6 用 `nomad job restart` 不 re-apply HCL,自然安全;本 session 未触发任何 `nomad job run aria-orchestrator.*hcl`
- R5.2 (005 migration row count assert): auto-migration 已应用,migration_notes 005 entry 自报 "16 dispatch rows copied verbatim, data integrity preserved",B.4 forensic 验证 16 issue_ids match baseline exactly
- R5.3 (M1_VALIDATOR_PATH missing): B.5 cp 安装 validator,问题闭合

---

## §4 实战教训 (memory 沉淀候选 — 由 owner review 决定文字)

**未写入 MEMORY.md 的本 session 候选**:

1. **`feedback_pip_editable_periodic_auto_migration` (新, 高价值)**: Pip editable install on host with running periodic jobs that import the package → next tick automatically activates new code → migrations + side-effects run **without explicit gate**. Source: 本 session B.3 → B.4 auto-trigger by comment-poll 60s cadence。Universal lesson: 涉及 host-side schema/data migration 的 deploy 必须在 pip install 前先 stop periodic jobs OR 移除 playbook "显式 migration step"(因为它会被旁路)OR 设 migration lock env gate。
2. **`feedback_investigation_doc_layered_reframe` (re-激活, 第 3 次)**: predecessor §3 R1 已记录;本 session B.7 再次实证 — "Layer 1 cron + reconcile NOT deployed" 假设也是 stale(实际两 job 早 deployed M4-era HCL,本 session 实为 upgrade)。Owner 是否本 session 写入 MEMORY.md?第 3 次激活足以 promote 为 lesson。
3. **`feedback_nomad_restart_in_place_for_raw_exec` (低, 通用知识)**: `nomad job restart` 对 raw_exec 是 in-place 操作(task kill+restart 同 alloc id),不轮换 alloc 像 docker / containerized job 那样;别误判 "alloc id 不变 = restart 没生效"。Owner 决定是否单独 entry。
4. **`feedback_nomad_var_get_out_keys_flag` (低, deploy 工具具体)**: `-out=keys` flag 在 nomad var get 中**不存在**(valid: go-template, hcl, json, none, table);playbook 文字 stale。Rule #7 hygiene 替代方式 = `nomad var get -out=go-template -template='{{range $k,$v := .Items}}{{$k}}{{"\n"}}{{end}}'`。Owner 决定。

**reused/reinforced**:
- `feedback_secrets_never_in_conversation` — Rule #7 全程 hygiene maintained(Nomad var keys only via go-template;migration SQL no value 读取)
- `feedback_aether_tool_discovery_flow` — Phase B 不涉及 Rule #8 PR merge gate(deploy 非 merge)
- `feedback_concurrent_edit_clean_rebase_pattern` — 本 session 0 race(Track A 已 quiesce)
- `feedback_layered_od_resolution_with_live_probe` (本 session **第 4 次**激活,predecessor 第 3 次刚沉淀):本 session R6 m1-handoff missing 是 Phase A live probe + Phase B smoke 双层暴露的 prod-state-dependent 事实

---

## §5 多维度同步状态

| 维度 | 本 session 涉及? | 状态 |
|------|------------------|------|
| UPM | no | N/A (Aria 主仓不使用 UPM) |
| User Stories | indirect | US-025 unchanged status(in_progress),Phase B 完成是 US-025 close gate 子里程碑,O1c/O2/O3 仍 pending |
| OpenSpec | no | 无活跃 Spec 改动(M5 main Spec `aria-2.0-m5-replay-reconciler-drift-review-loop-audit` Approved,T-deploy tasks 6.17-6.30 owner-runnable,本 session 推进 Phase B 但 tasks.md 仍按"全 unchecked"管理因为 6.17-6.30 是 sub-step granularity 而非"Phase B done" milestone) |
| PRD | no | unchanged |
| Standards / conventions | no | unchanged(Layer H frontmatter schema 已 §2.3, 本 doc 第 3 份 v1.22.0 frontmatter handoff) |
| Skill docs | no | unchanged |
| Architecture docs | no | unchanged |
| Auto-memory | 0 new(4 candidates surfaced §4) | Cumulative ~139 entries (predecessor +1 = ~140) |
| Decision memos | 0 new | — |
| Audit reports | 0 new | — |
| Production DB | **modified** (schema v3.0 → v4.2, 16 rows preserved) | 1 net change:schema migrated + 7 new cols + 1 new table + 2 triggers + 1 partial UQ index + 4 new migration_notes entries;0 net dispatches row delta;all 16 issue_ids preserved exact |
| Production source tree | **modified** (`/root/Aria` from `e416920` feature → `244151e` master) | branch switch + 3 submodule SHA bumps + pip editable v0.2.0 → v0.4.0 |
| Production Nomad jobs | **modified** (3 jobs HCL re-registered, 1 restarted) | aria-orchestrator restarted in-place;aria-layer1-reconcile HCL upgraded M4→M5;aria-layer1-cron HCL upgraded M4→M5 |
| Production data dir | **modified** (1 file added) | `/opt/aether-volumes/aria-layer1/data/validate-issue-schema.py` installed(M1 validator)+ 4 durable backups in `/opt/.../data/backups/` |
| Cross-project coordination | yes (light-1 SSH 多次,Rule #7 hygiene 全程) | All Rule #7-compliant;0 secret leak |
| Multi-remote parity | will verify post-push | Aria main:about to push;3 子模块 unchanged this session |
| Forgejo issue backlog | no | 13 open (unchanged from predecessor) |

---

## §6 Next session 入口 + 优先级建议

```bash
# Path A: 推 Phase C (Layer 2 image build + real dispatch smoke) — gated to Phase B ≥24h 稳定观察
# 1. 读取顺序:
cat docs/handoff/2026-05-20-m5-phase-b-shipped.md       # 本 doc
cat docs/handoff/2026-05-20-m5-deploy-playbook-v2-accurate.md  # §Phase C framework
# 2. 验证 Phase B 24h 观察期 reconcile + cron 自然 tick 全 healthy(no S_FAIL ramp-up / no error in alloc logs)
# 3. 走 v2 playbook §Phase C:aria-build container image build + push + sha pin + m1-handoff.yaml update + cp to prod data dir + real Layer 2 dispatch smoke A/B/C
# 4. 完成后 → Phase D archive + handoff(Phase C done)

# Path B: 不推 Phase C(填 Phase B 24h 观察窗口),做其他 backlog
/aria:state-scanner   # 多 track 看板 + recommendation
# 推 Tier 2 state-scanner family (#58/#89/#90/#79) 或 Tier 3 secret-hygiene
```

**优先级建议** (本 session 视角):

1. ⭐ **Phase B 24h 稳定观察** — 让 reconcile (30min cadence) + cron (60min cadence) 自然 tick × ~48 / ~24 次,确认 0 error
2. **Tier 2 state-scanner family** — 与 Phase C 不冲突,natural 填空窗口
3. **Phase C(Layer 2 image build)** — 24h 后启动,US-025 close gate 最后里程碑
4. **R6 m1-handoff.yaml install** — Phase C 自然修复(无需单独 session)
5. **Tier 3-6** — 同 predecessor 顺序

**不应该做的**:
- ❌ 不要在 Phase B 观察 24h 内启 Phase C(若 Phase B 有 latent issue,Phase C 会复杂化 rollback)
- ❌ 不要触发 Tier-1 live LLM gates(O2)在 zai 余额未 recharge 前(会全 fail)
- ❌ 不要 cp m1-handoff.yaml 当前 source 版到 prod(当前是 M4-era SHA;Phase C 会用新 v11 SHA 覆盖)— 这是 R6 mitigation (b) 不推荐的原因

---

## §7 提交清单 (commit hash + multi-remote parity)

**Pre-commit Rule #8 gates this session**: N/A — Phase B deploy 不涉及 PR merge(Rule #8 适用 PR merge 前)。Aria 主仓 commit 不触发 aether ci status check(本 commit 是 docs-only handoff)。

**Aria main commits this session** (in order):
- (本 doc commit,即将) docs(handoff): M5 T-deploy Phase B shipped — Layer 1 deploy + schema v4.2 + 2 Nomad jobs upgraded + Smoke A/B/C PASS

**Submodule changes**: 0(本 session 不改 submodule,只读)。

**3-way SHA parity target (post-本-commit)**:
- Aria main: master push to `origin` + `github`
- aria submodule: `62c324978333d1ffacde0a20436043e96f257f4c`(v1.22.1,unchanged this session)
- aria-orchestrator submodule: `962cb56c1bbec46ff20783bfa909beb312d5eb85`(M5 HCL fix,unchanged this session)
- standards submodule: `16041f4df2f9ff2f4a6a6cb8a1cd8c40b92048c1`(Layer H schema,unchanged this session)

**No regression**:
- Aria main repo: docs-only commit,代码 / 测试 / skills 全 untouched
- aria-plugin (submodule): untouched
- aria-orchestrator (submodule): untouched(prod 端 git tree 已 bumped 到 962cb56,与 dev 一致)
- standards (submodule): untouched

---

## §8 Memory entries this session (post-cycle owner review)

本 session 14:00 决策 — 4 candidates surfaced(§4),所有 commit 推迟到 owner review:

1. **`feedback_pip_editable_periodic_auto_migration`** (新,高价值)— B.3→B.4 auto-trigger lesson
2. **`feedback_investigation_doc_layered_reframe`** (3rd activation)— predecessor 已 surface,本 session B.7 第 3 次实证(reconcile + cron HCL 早 deployed)
3. **`feedback_nomad_restart_in_place_for_raw_exec`** (低,通用)
4. **`feedback_nomad_var_get_out_keys_flag`** (低,deploy 工具具体)

**Cumulative MEMORY.md count target**: ~141 entries(predecessor +1 = ~140, + #1 high-value = ~141);#2-4 owner 决定。

---

## Cross-references

- **Predecessor (Track B same line)**: [`2026-05-20-m5-phase-a-snapshot-done.md`](2026-05-20-m5-phase-a-snapshot-done.md) — same track-id, predecessor "Phase A done + A.7 dry-run + 5 OD locked",本 session 是该 playbook 的 Phase B 实地执行 + 3 dry-run advisories inline 处理
- **Parallel track (orthogonal, done)**: [`2026-05-20-multi-terminal-coordination-v1220-shipped.md`](2026-05-20-multi-terminal-coordination-v1220-shipped.md) — `simonfish/dev-claude2` 本 container 之前的 ship,quiesce 状态贯穿本 session
- **🎯 MUST READ before Phase C**: 本 doc §1 + §3 R6 + `2026-05-20-m5-deploy-playbook-v2-accurate.md` §Phase C framework
- **DEPLOYMENT.md** (live source at `aria-orchestrator/hermes-extensions/aria-layer1/DEPLOYMENT.md`) — AD-M2-7 canonical pattern
- **Layer H frontmatter schema (standards SoT)**: `standards/conventions/session-handoff.md §2.3` (v1.1.0)
- **Rule #9 trigger eval (本 session)**: **HIGH** — session ~2h cumulative + 1 substantial cycle phase shipped (M5 Phase B Layer 1 deploy = prod-write) + 1 phase touched + 4 memory candidates surfaced + 1 high-value lesson — L1-L4 信号都满足。Handoff 必写。

---

**Created**: 2026-05-20 ~14:00 UTC (post-B.8-smoke, pre-commit)
**Session duration**: ~1.5h (Phase B 真正执行) — well within owner's ~2-3h commitment;1-1.5h buffer 给 commit + push + multi-remote verify + 任何 unexpected
**Status**: Active — Phase B done, Phase C carry-forward gated to ≥24h Phase B observation
**Next session entry**: Path A (Phase C Layer 2 build,~24h 后)或 Path B (Tier 2 backlog 填空) — owner 决定
