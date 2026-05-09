# Aria — Session Handoff (2026-05-09 EOD) — Track A T-deploy COMPLETE

> **Status**: US-024 M4 Track A T-deploy + E2E smoke COMPLETE — production active
> **Cycle period**: 2026-05-09 morning (M4 closeout) → 2026-05-09 afternoon (Track A deploy)
> **Next session 入口**: 优先读本 doc → `/aria:state-scanner` 看完整状态

---

## TL;DR

Aria 2.0 M4 (US-024) **production deploy 已激活** 在 Aether light-1。
3 production bug 沿途发现并修复。E2E smoke 验证 S7_HUMAN_GATE → S8_MERGE 全链路。

**已完成**:
1. **8 nomadVar keys 配置完毕** (4 已有 + 4 新增 M4: ARIA_FEISHU_OPS_ALERT_WEBHOOK / ARIA_FEISHU_SIGNING_SECRET / ARIA_AUTHORIZED_APPROVERS=`simonfish` / ARIA_BOT_USERNAME=`aria-runner-bot`)
2. **2 个 Nomad 部署**: aria-layer1-comment-poll (1-min cron + `--continuous --interval 30 --max-iterations 2`) + aria-layer1-reconcile (30min cron, M3 carryover gap closed)
3. **light-1 venv refresh**: M2 v0.2.0 → M4 master via git pull + `pip install -e`
4. **dispatches.db schema migration**: v1.1 → v3.0 (002 + 003) with 3-safeguard backup pattern, 14 rows preserved, integrity ok
5. **3 production fix shipped**: HCL cron fallback / Feishu HMAC swap / venv + schema
6. **E2E smoke S7→S8 verified**: PR #97 dummy + SQL inject row 16 + Feishu card delivered + `/aria approve` detected within 30s + cron tick transitions to S8_MERGE
7. **Closeout**: m4-handoff.yaml Tier-2 partial fill + OD-M4-2 sign-off + Forgejo housekeeping + 6 memory entries

**Pending (deferred, 不阻塞)**:
- 🟡 **Phase D.2 final go_decision**: awaiting Tier-2 N≥3 real owner workload accumulation (smoke = 1)
- 🟡 **Task #42 secret rotation**: 4 keys 多次暴露 (2026-05-02 + 2026-05-09 conversations),hard cap 2026-08-02
- 🟡 **M5 inputs**: aria-layer1-cron 1h cadence vs PRD §618 SLO < 10min;aria-layer2-runner job 缺失

---

## Repository state (final 2026-05-09 EOD)

| 仓库 | Local HEAD | Forgejo origin/master | GitHub master | Parity |
|------|-----------|------------------------|---------------|--------|
| Aria 主仓 | a25dbd2 | a25dbd2 | a25dbd2 | ✅ 1 SHA |
| aria-orchestrator submodule | 834c313 | 834c313 | 834c313 | ✅ 1 SHA |
| aria submodule (aria-plugin) | 5767fe3 (v1.18.0) | 5767fe3 | 5767fe3 | ✅ 1 SHA |
| standards submodule | 2cd34d3 | 2cd34d3 | 2cd34d3 | ✅ 1 SHA |

**Working tree**: clean

---

## Active production state on Aether light-1

```
aria-orchestrator     service       running (5d)        (host of venv)
aria-layer1-cron      batch/periodic 1h cadence (152 dead children)
aria-layer1-reconcile batch/periodic 30min cadence (6 ticks since 14:54)
aria-layer1-comment-poll batch/periodic 1min cron + --continuous (132 ticks since 14:54)
aria-build            service       running (5d)
aria-runner-template  batch/parameterized running (注意: 不是 aria-layer2-runner)
```

dispatches.db 状态:
- 34 columns (M4 v3.0 schema)
- 10 indexes (含 M4 uq_approval_comment UNIQUE INDEX)
- 16 dispatches (14 historical + smoke row 15 stuck S2_DECIDE + smoke row 16 → S9_CLOSE)
- backup at `/opt/aether-volumes/aria-layer1/data/backups/dispatches.db.pre-m4.20260509T151221Z`

---

## Recommended next workflow (3 轨)

### Track B — US-025 M5 brainstorm (推荐)

M5 范围 (per PRD §409): Replay + Reconciler 深度增强 + 防漂移 + Review loop
+ 审计日志 immutable, ~120h baseline。

**M5 brainstorm Q0 必读** (per AD-M4-10 + abi_compat_promises):
1. risk_tier_stub_to_risk_tier (M5 ADD column, 不 RENAME 不 DROP)
2. forgejo_approval_comment_id_unique_index (M5 preserve)
3. comment_poll_cadence_independent (30s + 30min cron stay separate)
4. human_decision_first_decision_wins (review-loop 用新 enum, NOT multi-write)

**新增 M5 输入** (Track A 发现):
- aria-layer1-cron 1h cadence vs PRD §618 SLO < 10min: 评估改 30/15min OR M5 让 comment-poll 直接做 transition
- aria-layer2-runner 缺失: M2/M3 infra gap, 决策 deploy 还是 disable S0-S6

入口:
```
/aria:brainstorm mode=requirements topic="Aria 2.0 M5 — Replay + Reconciler 深度增强 + 防漂移 + Review loop + 审计日志 immutable" parent_us=US-025 parent_prd=docs/requirements/prd-aria-v2.md predecessor=US-024
```

### Track C — Tier-2 N≥3 累积 (产品自然累积,不需主动)

M4 production 已激活,owner 日常用 Aria 派发任务时 Tier-2 自动累积。
当累积到 N≥3 dispatches (含 ≥1 approve + ≥1 reject 路径) 后,M4 Phase D.2 final go_decision
可以从 `<pending>` 改为 `Go`。无主动 task,被动等。

### Track D — Secret rotation (low priority but bounded)

per OD-M4-secret-rotation: 4 keys (FEISHU_WEBHOOK_URL / FORGEJO_BOT_PAT / FORGEJO_BOT_USER /
LUXENO_API_KEY) 暴露过两次,deferred to production launch with hard cap 2026-08-02.
85d 后必须 rotate。

每个 rotation:
1. 飞书/Forgejo/Luxeno 后台 reset → 取新 secret
2. `nomad var put -force` 覆盖 (单步 atomic, 各 alloc 下次启动自动 pickup)
3. 验证: `nomad var get -out=go-template -template='{{.Items.X | len}}'` 确认 length 合理

---

## Open issues + carryover (m4-handoff::open_issues_for_m5 + 本 session 新增)

| ID | Severity | Description | Track |
|----|----------|-------------|-------|
| BA-R3-1 | observation | mock fidelity gap acceptable for M4 single-writer | C |
| BA-R3-2 | observation | rowcount=0 silent skip (intended design) | C |
| **TL-R3-4** | important | abi_compat_promises governance — M5 brainstorm Q0 acknowledge | B (mandatory) |
| TL-R3-5 | minor | OD-M4-2 underbaseline retrospective | ✅ done this session |
| TL-R3-6 | minor | first-decision-wins ↔ M5 review-loop concept boundary | B |
| QA-R3-1 | minor | repo._conn encapsulation (3 sites in comment_poll.py) | C |
| QA-R3-2 | minor | test_t_pre_merge_r2_fixes.py 文件名误导 | C |
| QA-R3-3 | trivial | list_pending_s7 direct test gap | C |
| AI-R3-4 | low | Feishu 401 silent failure window 7d | C |
| BA-R4-1 | observation | --continuous mode warning skip | C |
| **NEW Track-A-1** | critical | Feishu HMAC swap bug | ✅ fixed `5467991` |
| **NEW Track-A-2** | high | Nomad v1.7.7 6-field cron silent degrade | ✅ fallback `ec264f0` |
| **NEW Track-A-3** | high | light-1 venv 不刷新,M2 v0.2.0 stuck | ✅ pip install -e refresh |
| **NEW Track-A-4** | medium | aria-layer2-runner missing (S0→S6 真实 dispatch fail) | M5 input |
| **NEW Track-A-5** | medium | aria-layer1-cron 1h cadence vs PRD §618 SLO | M5 input |

---

## 6 memory entries (this session)

| File | Theme |
|------|-------|
| [feedback_feishu_hmac_key_msg_swap.md](../../.claude/projects/-home-dev-Aria/memory/feedback_feishu_hmac_key_msg_swap.md) | Feishu HMAC key/msg 不可颠倒;test 需 independent oracle |
| [feedback_nomad_cron_field_count_silent_degrade.md](../../.claude/projects/-home-dev-Aria/memory/feedback_nomad_cron_field_count_silent_degrade.md) | Nomad v1.7.7 接受 6-field 但 schedule 退化;deploy 后必须 verify |
| [feedback_handoff_doc_assumes_venv_ready_smell.md](../../.claude/projects/-home-dev-Aria/memory/feedback_handoff_doc_assumes_venv_ready_smell.md) | T-deploy handoff 必须显式 venv refresh + schema migration step |
| [feedback_smoke_dispatch_sql_inject_pattern.md](../../.claude/projects/-home-dev-Aria/memory/feedback_smoke_dispatch_sql_inject_pattern.md) | 测 M_n 链路绕过 M_{n-1} infra gap 的 SQL inject 手法 |
| [feedback_secret_env_inject_via_go_template.md](../../.claude/projects/-home-dev-Aria/memory/feedback_secret_env_inject_via_go_template.md) | secret-hygiene 合规的 env 注入 (vs 全量 dump) |
| [feedback_schema_migration_3_safeguard_pattern.md](../../.claude/projects/-home-dev-Aria/memory/feedback_schema_migration_3_safeguard_pattern.md) | Production schema migration 3 重 safeguard |

---

## Effort actuals (Track A T-deploy + smoke)

| Phase | 时长 | 备注 |
|-------|------|------|
| §0 prereq | ~10min | Aether status / Forgejo / submodule HEAD / host volume |
| §1 nomad var | ~15min | 4 owner-action secrets + 4 verify |
| §2 HCL validate + redeploy | ~10min | 含 6-field cron fallback edit |
| §3 first deploy attempt → fail | ~20min | comment_poll_runner ImportError |
| **deploy gap repair** | ~75min | venv refresh (45min) + schema migration (30min) |
| §3 second deploy + verify alloc | ~10min | clean ticks confirmed |
| **Feishu HMAC bug** | ~75min | 诊断 → fix → test → push → verify |
| §4 E2E smoke | ~30min | PR #97 + SQL inject + card + approve + transition |
| §5-§8 closeout | ~45min | m4-handoff Tier-2 + memories + housekeeping |
| **Total Track A** | **~5-6h** | actual T-deploy 复杂度 |

加入 OD-M4-2 retrospective ratio: B.2 ~22h + T-deploy ~6h = 28h vs 60h baseline = **0.47**.

---

## Next session 入口

```bash
/aria:state-scanner
```

state-scanner v3.0 会:
1. scan.py 机械扫描 → snapshot.json
2. 检测 M4 spec archived ✅ + state-scanner-inter-cycle-surfacing v1.18.0 ✅
3. 检测无活跃 OpenSpec change → 推荐 brainstorm
4. **会读取 `docs/handoff/latest.md`** (per Aria internal convention) → 跳转本 doc

读完本 doc 后,推荐:
1. ⭐ **Track B M5 brainstorm** (~12h Phase A.1, AI-runnable)
2. **Track C 自然累积** (Tier-2 + secret rotation 时间窗,被动)
3. **Track D quick wins** (post-merge polish)

---

**Created**: 2026-05-09 EOD
**Cycle**: US-024 M4 Track A T-deploy + smoke COMPLETE
**Status**: Active — production live on Aether light-1, awaiting M5 brainstorm trigger
