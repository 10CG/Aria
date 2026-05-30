---
track-id: session-2026-05-30-issue-sweep-133-spec-banked
owner-container: simonfishgit/dev-claude
phase: D-closed
status: done
updated-at: 2026-05-30T11:57:00Z
---

# Aria — Session Handoff (2026-05-30, arc 2) — Issue sweep + #133 Spec banked (A.2 未收敛)

> **Status**: ✅ 本 session 第 2 弧:全 issue 梳理 → #133 triage → Level 2 proposal → post_spec R1→Rev1→R2 **未收敛 banked**
> **Type**: 接续同 session 第 1 弧(M6 cost-snapshot hotfix+deploy,见前置 handoff)
> **Rule #9 trigger**: 跨多 phase (M6 hotfix A→D + #133 triage→A.2) + 超长 session

---

## §0 入口 (新 session 优先读)

1. **本 doc** — arc 2 (#133 Spec banked)
2. **arc 1 (同 session 前置)**: `docs/handoff/2026-05-30-m6-cost-snapshot-hotfix-deployed.md` — M6 created_at hotfix 诊断→修→发→部署→验证 + 2026-06-01 闸门双提醒
3. **#133 proposal**: `openspec/changes/concurrent-track-proactive-coordination/proposal.md`(§R2-CARRY = Rev2 清单)
4. **#133 audit**: `.aria/audit-reports/post_spec-R1R2-2026-05-30-concurrent-track-proactive-coordination-consolidated.md`

→ **next session 入口**: 见 §6。

---

## §1 本 session 完成了什么 (两弧)

### Arc 1 — M6 cost-snapshot created_at hotfix (详见前置 handoff)
- state-scanner → M6 e2e Phase B 闸门 FAIL → **4 层 blocker 链诊断**(cron 未部署 → 节点代码旧 → 节点 git 凭据过期 → 真根因 created_at 代码 bug)
- emergency_hotfix cycle:`COALESCE(cycle_start_ts, state_entered_at)` + anti-recurrence regression gate → aria-orch `72fa62b` / 主仓发版 → **部署 light-1 验证 cost.json 生成**
- 2026-06-01 Phase B 闸门检查:本机 cron(真执行)+ 云端 routine(兜底)双保险

### Arc 2 — Issue 梳理 + #133 Spec
- **全生态 issue 梳理**:Forgejo 11 open(Aria 9 / aria-plugin 1 / aria-orch 1;aria-standards 0);GitHub 镜像限流但 issue 都在 Forgejo
- **#133 triage**:并发多 session UPM merge thrash + 矛盾记录 = VALID,无重复实现
- **Level 2 proposal**(scope c + a-lite):phase-d 前置并发检测 + state-scanner opt-out 主动提示
- **post_spec R1→Rev1→R2 未收敛**:见 §2

---

## §2 关键技术发现 / 决策

1. **created_at-class 教训本 session 三次实证**(贯穿主线):
   - M6 (arc 1): cost SQL 查不存在的 `created_at` 列 → prod 非功能
   - #133 R1: proposal 假设 `tracks_multibranch.collision_type` 字段存在 → 不存在(只在设计文档)
   - #133 R2: Rev1 假设 `_classify_collision` 输入 `tracks[]` → 实际 `list[ClaimRecord]`;假设 phase1_gate 共享 collision 字段 → 实际读独立 claim refs
   - **统一教训**: 复用/断言任何数据,必先对**真代码** verify 可达性 + ref 语义,**不止存在性**(`feedback_spec_reuse_data_source_must_match_actual_access`)
2. **audit 在代码前拦截价值兑现**:#133 两轮 multi-agent post_spec 把 created_at-class 缺陷在**写码前**全拦下 —— 这是 #133 cycle 的最大产出,胜过仓促实现一个错的 Spec
3. **#133 真 scope 比想的大**:collision 持久化需迁移 `_track_to_claim_record → reconcile_all` 整链(非"抽函数");phase1_gate 与 snapshot 是独立数据源 → 建议拆 collision-field-persistence 独立 Spec
4. **多终端并发实时佐证 #133**:本 session push 撞另一终端 **2 次**(rebase 化解,零 regression),正是 #133 描述的场景

---

## §3 运行时状态

- 主仓 master `117c632`(origin+github 一致);aria-orch `72fa62b`;light-1 节点 @ 72fa62b
- M6 cost-sentinel cron running(daily 02:00 UTC),snapshot rolling **1/3**
- 2026-06-01 闸门检查:本机 crontab `0 3 1 6 *` + 云端 routine `trig_01Pf3zZjW2ucWy22s2cTpZC4`
- #133 proposal banked(REVISE,A.2 未收敛)

---

## §4 carry-forward (未完成, 按优先级)

| 优先级 | 项 | 入口 |
|--------|-----|------|
| **P1** | 2026-06-01 M6 Phase B 闸门检查(自动) | `.aria/notes/2026-06-01-m6-phase-b-gate-result.md`(本机 cron 写)/ 云端 routine |
| **P1 (owner)** | v1.29.0 block-flip D+14 ship | 2026-06-07, owner F1 tripwire |
| **P2** | #133 Rev2 + scope 重构(拆 collision-persistence 子 Spec) | proposal §R2-CARRY(6 项)+ audit 报告 |
| P2 | M6 Blocker #-1(节点 git 凭据过期)+ Blocker #2(snapshot-locality 永久解) | arc-1 handoff §4 |
| P2 | M6 e2e-resilience + release-closeout Phase B(闸门过后) | 2 Spec Approved |
| P3 | 余下 issue:audit 集群 #54/#95/#79/#17(与本 session 教训强相关)/ #128 M7 / #59 / #120 / #32 / #5 | Forgejo |

---

## §5 维度审计 (Q3)

- **UPM/US**: M6 hotfix + #133 均 issue-driven 非 US-tied;US-026 (M6) 仍 in_progress
- **Spec**: #133 `concurrent-track-proactive-coordination` proposal banked(REVISE);M6 Spec#1 加 POST-ARCHIVE CORRECTION 横幅;active 不变
- **CLAUDE.md**: 无需改(无插件版本变;hotfix 是 aria-orch runtime)
- **Memory**: 新增 `feedback_shipped_archived_spec_can_be_nonfunctional_on_prod`(arc 1);**候选(arc 2)**: audit 两轮拦 created_at-class 在代码前 = "spec-reuse verify 在 Phase A.2 的 ROI"(可并入既有 spec_reuse memory 作二/三实证补强)
- **子模块**: aria-orch 72fa62b(已 bump + 推);aria/standards 本弧未改

---

## §6 next session priorities

1. **2026-06-01 看 M6 闸门结果**(`.aria/notes/2026-06-01-m6-phase-b-gate-result.md`)→ PASS 则 M6 e2e Phase B 解锁
2. **#133 Rev2 + scope 重构**(fresh session):先决策拆 collision-field-persistence 独立 Spec,再 Rev2 修 6 项(§R2-CARRY)→ R3 收敛 → A.3/B
3. v1.29.0 block-flip D+14(2026-06-07, owner-gated)
4. M6 收尾 gap(节点凭据 #-1 / snapshot-locality #2)
5. audit 质量集群 #54/#95(与本 session created_at 教训强相关,杠杆高)

---

## §7 注意事项

- **created_at-class 是本 session 反复栽的坑**:下次起草任何 Spec,引用 snapshot 字段 / 复用函数前,**先 grep/read 真实 collector + 函数签名**,别信设计文档(`layer-l-integration.md` 的 phantom 字段就是反例)
- **#133 collision 持久化别低估**:不是抽函数,是迁移 reconcile 链 + 跨 render-time→collect-time 数据源;phase1_gate 不读 snapshot collision
- **多终端 push 高频撞**:本 session 撞 3 次(M6 + #133 ×2),都靠 fetch+rebase 零冲突化解;push 前先 `git fetch` 是肌肉记忆
- 本机 cron + 云端 routine 都设了 2026-06-01;dev 机届时需开机本机 cron 才跑(云端兜底不依赖)
