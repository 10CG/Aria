---
track-id: aria-2-0-m5-replay-reconciler-drift-review-loop-audit
owner-container: simonfish/dev-claude
phase: B-stabilized
status: ship_ready
updated-at: 2026-05-21T12:00:00Z
---

# Aria — Session Handoff (2026-05-21 ~12:00 UTC) — M5 Phase B 稳定化 + Hermes→Luxeno 重定向 + Spec tasks.md 同步

> **Status**: SHIP READY — Phase B 全闭环 + 24h 稳定观察 + aria-heartbeat 修复 (Hermes 重定向 Luxeno, 双路径统一) + M5 Spec tasks.md T-deploy 6.17-6.26 同步。Phase C gated (24h gate 22:02 UTC May 21 + owner O1/O2)。
> **Predecessor handoff**: [`2026-05-20-m5-phase-b-deploy-done.md`](2026-05-20-m5-phase-b-deploy-done.md) — Phase B (B.1-B.9) 主体 + Layer 1/2/3
> **Next session 入口**: 优先读本 doc → §6 → Phase C 或 secret-guard Spec
> **本 session 性质**: Phase B 完成后的稳定化续推 (~2h, 续 predecessor 同 track)

---

## §0 入口 (新 session 优先读)

读取顺序:
1. **本 doc** — 2026-05-21 稳定化 + Hermes→Luxeno 重定向
2. **`2026-05-20-m5-phase-b-deploy-done.md`** — Phase B 主体 (predecessor)
3. **`.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md`** — secret rotation 三层 + §3.5-3.7 (Hermes 重定向)
4. Optional: `2026-05-20-m5-deploy-playbook-v2-accurate.md` §Phase C

读完后 → **Path A**: Phase C (≥ 22:02 UTC May 21 后) | **Path B**: Spec `aria-secret-guard-plugin-default` | **Path C**: backlog

---

## §1 已完成 (本 session, 2026-05-21)

| 时间 (UTC) | 事件 | 结果 |
|-----------|------|------|
| ~08:20 | `/aria:state-scanner` 重扫 + Phase B 24h 稳定性观察 | 发现 aria-heartbeat 持续 429 (00:54-06:59) → 401 (07:59) |
| ~08:24 | (误诊#1) resync `/root/.hermes/.env` ANTHROPIC_API_KEY+LUXENO_API_KEY → restart | 仍有效 hygiene (stale 副本真实), 但**未修好 aria-heartbeat** |
| ~09:00 | aria-heartbeat 09:00 tick 仍 401 → 回 config 层重诊 | 发现 Hermes `provider: zai` 用 `GLM_API_KEY` 直连 Z.AI, 不读 resync 的 key |
| ~09:40 | faithful-reporting 更正: decision §3.5 误诊更正 + §3.6 双路径 architecture | commit `fcb7b5c` |
| ~11:26 | owner 选 option (c) → Hermes 重定向 Luxeno (`GLM_BASE_URL`+`GLM_API_KEY`) → restart | Total Restarts 4→5 |
| ~11:28 | `hermes cron run` 手动触发 aria-heartbeat 验证 | tick `11-27-47.md` Response `[SILENT]` — **成功** |
| ~11:30 | decision §3.7 + handoff R6 + memory 更新 | commit `6528051` |
| ~12:00 | Phase D 收尾: M5 Spec tasks.md T-deploy 6.17-6.26 同步 + 新 memory + 本 handoff | (本 commit) |

**Cycles shipped**: 0 OpenSpec full cycle (稳定化 + 修复, 非 Spec cycle)。

**累计交付**: aria-heartbeat 修复 (双 LLM 路径统一 Luxeno) + 1 误诊 faithful 更正 + M5 Spec tasks.md 6.17-6.26 checked + 1 新 memory + 3 memory 更正 + decision §3.5-3.7。

---

## §2 未完成 / Carry-forward (全部 genuinely gated, 非遗漏)

### Phase C (US-025 close gate)

| # | 项目 | gate |
|---|------|------|
| O1 | FEISHU_APP_SECRET 轮换 (per decision §2.5) | owner Feishu 后台重建 app, ~30-45min |
| O2 | Layer 2 image v11 build + push + m1-handoff.yaml `image_sha_final` | aria-build infra + owner |
| O3 | Tier-1 live LLM gates (B.1.live + C.2.live, ¥0.10) | owner 触发 |
| O4 | Tier-2 N≥3 real dispatches 累积 | owner 日常 workload |
| 6.21.1 | verify aria-runner-template stub alloc | Phase C (Layer 2) |
| 6.27-6.30 | Tier-2 累积型验收 + Phase D.2 final go | Phase C 后 |

> **Phase C 24h 稳定 gate**: Layer 1 deploy 22:02 UTC May 20 → gate 到期 **22:02 UTC May 21**。

### Spec / 后续

| # | 项目 | 状态 |
|---|------|------|
| S1 | Spec `aria-secret-guard-plugin-default` (plugin v1.23.0; close Forgejo #84+#107) | 下一 cycle, 需 owner brainstorm Q1/Q2/Q3 |
| S2 | M5-OS-PB-1: comment_poll_runner ctx.forgejo lazy-wire bug (Smoke B placeholder skipped) | M6 follow-up (m5-handoff.yaml open_issues) |
| S3 | M5-OS-PB-2: `version=0.1.0` log string stale (vs pip 0.4.0) | M6 cosmetic |
| S4 | 6.19 nomadVar: `ARIA_REWORK_MAX_ROUND`/`ARIA_SPEC_DRIFT_THRESHOLD`/`ARIA_FAIL_RETRY_CONFIDENCE_MIN` 未显式设 (用 code 默认 3/70/0.7) | owner Phase C 若要显式锁定需补设 |
| S5 | DEMO-M5-001/002/003 smoke dispatch rows 留 prod DB | M6 cleanup (`WHERE issue_id LIKE 'DEMO-M5-%'`) |
| S6 | `/root/.hermes/.env` 的 3 个 `.env.bak-*` 备份 (含旧死 key) | 保留 ~24h 作 rollback, 之后 shred |
| S7 | 长期: `/root/.hermes/.env` 迁 Nomad-var-rendered (消除 static 多副本) | 后续 backlog |
| S8 | 2026-05-02 deferred: GLM_API_KEY (现已弃用) + FEISHU_VERIFICATION_TOKEN + FEISHU_ENCRYPT_KEY 轮换 | Phase C / 2026-08-02 hard cap |

---

## §3 关键风险 / 已知陷阱

### R1 — Hermes 重定向后同一 Luxeno key 现 4 处副本

`nomad var LUXENO_API_KEY` + `/root/.hermes/.env` 的 `GLM_API_KEY` / `ANTHROPIC_API_KEY` / `LUXENO_API_KEY` 全 = 同一 Luxeno key (sha `987201dd4773`)。下次 Luxeno rotation 必 4 处全换 (per `feedback_rotation_enumerate_all_credential_stores`)。长期 fix = S7。

### R2 — Z.AI 直连账户 (旧 GLM_API_KEY) 已弃用但未清理

Hermes 重定向 Luxeno 后, 旧 Z.AI 直连账户不再被使用。该账户 + 旧 GLM_API_KEY (sha `2d15bf433f57`) 现是 orphan。owner 可在 Z.AI console 注销/确认, 非紧急。

### R3 — 误诊教训 (本 session faithful-reporting)

aria-heartbeat 401 初诊误判为 "Phase B rotation 回归", resync 错的 key。根因实为 Hermes `provider: zai` 直连 Z.AI + GLM_API_KEY (config 层未先查)。教训已固化 memory `feedback_diagnose_from_provider_config_not_symptom`。decision §3.5 保留误诊→更正全过程作 audit trail。

### R4 — Phase C 不被 aria-heartbeat block

aria-heartbeat 是 M0/M1-era 监控, 与 M5 Layer 1 (走 Luxeno, 健康) 正交。已修复。Phase C gate 只剩 24h wall-clock + owner O1/O2。

---

## §4 实战教训 (memory 固化)

**本 session 新增 memory** (1):
- `feedback_diagnose_from_provider_config_not_symptom` — 服务认证/路由故障先查 (provider, credential, endpoint) 三元组; 修复后症状不消失=原假设证伪立即回 config 层重诊

**本 session 更正 memory** (3):
- `project_glm_routing_luxeno` — 更正 2026-05-20 错误 amendment; 厘清双路径 + 记录 2026-05-21 Hermes→Luxeno 重定向
- `feedback_rotation_enumerate_all_credential_stores` — 加更正段 (初稿误归因)
- `MEMORY.md` index — 3 行更新

**predecessor session memory** (固化完整, 见 `2026-05-20-m5-phase-b-deploy-done.md` §4): `feedback_secret_guard_plugin_upstream_dogfood` / `feedback_test_new_credential_before_rotation_commit` / `feedback_rotation_enumerate_all_credential_stores` / `feedback_nomad_inspect_secret_leak` (ext) / `project_secret_rotation_deferred_2026-05-02` (amend)。

无未固化的值得总结的经验。

---

## §5 多维度同步状态 (Q3 核对)

| 维度 | 状态 |
|------|------|
| **UPM** | N/A — Aria 主仓不使用 UPM |
| **User Story** | US-025 `in_progress` — 正确 (Phase C+D 未完); Phase B 完成是 Spec-internal 粒度, US 状态不变, 无需改 |
| **OpenSpec (Spec)** | M5 Spec `aria-2.0-m5-...` `approved` — proposal.md 不变 (Phase C/D 未完不归档); **tasks.md T-deploy 6.17-6.26 本 session 已同步勾选** (Q3 修复的 gap), 6.21.1/6.27-6.30 留 Phase C |
| **PRD** | prd-aria-v2.md §M5 不变 — 正确 (PRD = 需求, 非执行状态) |
| **Architecture docs** | 不变 |
| **Auto-memory** | +1 new, 3 corrected (见 §4) |
| **Decision memos** | `.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md` §3.5-3.7 |
| **Production** | aria-orchestrator alloc d43c2a7e healthy (Restarts 5); Layer 1 jobs (reconcile/cron/comment-poll) running; 双 LLM 路径统一 Luxeno; schema v4.2 |
| **Multi-remote parity** | Aria main + aria-orchestrator: origin + github 同步 (本 commit 后 verify) |

---

## §6 Next session 入口 + 优先级

```bash
# Path A (推荐, ≥ 22:02 UTC May 21 后): Phase C — US-025 close gate
/aria:state-scanner   # 自动 surface 本 handoff
# 1. O1 FEISHU_APP_SECRET 轮换 (Feishu 后台重建 app)
# 2. O2 Layer 2 image v11 build + push + m1-handoff.yaml
# 3. O3 Tier-1 live LLM gates
# 4. Phase D.2: tasks.md 6.21.1/6.27-6.30 + proposal.md archive

# Path B: Spec aria-secret-guard-plugin-default (plugin v1.23.0)
# Path C: backlog (Tier 2/3/4 Forgejo issues)
```

**优先级**: ⭐ Path A (Phase C) — M5 close gate 主线。

**不应该做的**:
- ❌ 24h gate (22:02 UTC May 21) 前不要推 Phase C prod-write
- ❌ 不要 unilaterally 改 Hermes provider 配置 (option c 已锁)
- ❌ 不要 shred `.env.bak-*` 备份直到 Hermes 重定向稳定 ≥24h
- ❌ 不要 DELETE DEMO-M5-* dispatch rows (audit trail, M6 cleanup)

---

## §7 提交清单

**本 session commits** (Aria main, origin + github 双推):
- `fcb7b5c` docs(decision,handoff): 误诊更正 §3.5 + §3.6 双路径
- `6528051` docs(decision,handoff): §3.7 Hermes→Luxeno 重定向
- (本 commit) docs(closeout): M5 Spec tasks.md T-deploy 同步 + stabilization handoff + memory

**预期 3-way SHA parity** (post-commit): Aria main origin == github; submodules 不变 (aria `964f5ad` / aria-orchestrator `91b8975` / standards `16041f4`)。

**无 regression**: 0 prod 破坏; Layer 1 + Hermes 双健康; M5 Layer 1 走 Luxeno。

---

## §8 Memory entries this session

见 §4。Cumulative MEMORY.md ~144 entries。

**Q-audit (收尾)**:
- Q1 未完成 task/讨论? 12 explicit task 全 done; carry-forward (§2 O1-O4 + S1-S8) 全 documented + gated; 无遗漏。
- Q2 未固化经验? 无 — 1 新 memory + 3 更正已写。
- Q3 UPM/US/Spec/PRD? 见 §5 — UPM N/A, US-025 正确不变, Spec tasks.md 已同步 (gap fixed), PRD 不变。
- Q4 收尾交接? 本 doc + latest.md pointer 更新 → 新 session `/aria:state-scanner` Phase 1.15 自动 surface。

---

## Cross-references

- **Predecessor (same track)**: [`2026-05-20-m5-phase-b-deploy-done.md`](2026-05-20-m5-phase-b-deploy-done.md)
- **Decision**: [`.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md`](../../.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md) §3.5-3.7
- **M5 Spec**: `openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/` (tasks.md T-deploy 6.17-6.26 done)
- **Phase C playbook**: [`2026-05-20-m5-deploy-playbook-v2-accurate.md`](2026-05-20-m5-deploy-playbook-v2-accurate.md)
- **m5-handoff.yaml**: `aria-orchestrator/docs/m5-handoff.yaml` (t_deploy_status Phase B done)

---

**Created**: 2026-05-21 ~12:00 UTC
**Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7 (1M context)
**Status**: SHIP READY — Phase B stabilized, aria-heartbeat fixed, dual LLM path unified on Luxeno. Phase C gated (24h + owner O1/O2).
**Next entry**: Path A Phase C (≥ 22:02 UTC May 21).
