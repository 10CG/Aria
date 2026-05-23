# post_spec R1 audit report — aria-layer2-docker-auth-cold-pull-fix

> **Date**: 2026-05-23 ~07:00-09:00 UTC
> **Spec**: `openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md` (Draft v1)
> **DEC**: `.aria/decisions/2026-05-23-layer2-docker-auth-cold-pull-fix.md`
> **Mode**: 4-agent parallel (tech-lead / backend-architect / qa-engineer / knowledge-manager)
> **Orchestrator**: Claude Opus 4.7 (1M context), solo-lab session

---

## §1 Verdict matrix

| Agent | Verdict | Critical | Important | Minor |
|-------|---------|----------|-----------|-------|
| tech-lead | PASS_WITH_WARNINGS | 0 | 4 | 3 |
| backend-architect | **NEEDS_FIX** | **1** | 4 | 3 |
| qa-engineer | **NEEDS_FIX** | **1** | 4 | 3 |
| knowledge-manager | **NEEDS_FIX** | **2** | 4 | 3 |
| **聚合** | **3/4 NEEDS_FIX** | **4** | 16 | 12 |

---

## §2 Critical findings (4) — 全部 R2 Rev1 addressed

### M-ba-C-1 + M-qa-I-4: 验收 C `nomad system gc` 不清 docker image cache

- **R1 location**: proposal.md §Acceptance C
- **Issue**: `nomad system gc` 只清 dead allocations + reaps stopped jobs, **不**触发 docker daemon image GC。image GC 由 docker daemon 按 `client.gc.image_delay` 跑。owner 跑 `nomad system gc` 看到 success 后 dispatch 命中 cache,声称 fix verified → false-pass acceptance。
- **Suggested fix (applied in Rev1)**: 改用 `docker rmi -f <image>` per node 直接清,或 `force_pull = true` 临时 patch HCL config 测试。Rev1 §Acceptance C 已重写 3 步流程 (C1/C2/C3) per-node:
  1. SSH 强清 image (`docker rmi -f`)
  2. dispatch with per-node constraint (临时 meta override)
  3. alloc log 必须含 "Pulling from forgejo.10cg.pub" (非 "Status: Image is up to date")
- **Status**: ✅ ADDRESSED in Rev1

### M-qa-C-1: 验收 A grep 漏 sister HCL

- **R1 location**: proposal.md §Acceptance A
- **Issue**: 单文件 grep `aria-layer2-runner.hcl == 0` 漏 `aria-runner-template.hcl`。两 HCL 都需删 auth block,但 A 只 gate 一个 → sister 静默回归。
- **Suggested fix (applied in Rev1)**: A 改为 3 grep (两 HCL + nomad/jobs/ regression sweep)
- **Status**: ✅ ADDRESSED in Rev1

### M-km-C-1: Convention §1 不能与 Aether spike GO 结论矛盾

- **R1 location**: convention doc planned §1 (DEC §4 D4)
- **Issue**: Aether 2026-04-23 spike GO (Nomad < v1.11.2, 同集群 11.5MB image cold-pull alloc d360435e) vs Aria 2026-05-23 M5 O3 live FAIL (Nomad v1.11.2 + Forgejo 11.0.6) — 30 天前 GO / 现在 FAIL。Convention §1 直接照搬 proposal 的"HCL config-time"解释会与 Aether 已验证 GO 结论矛盾。其他 Lab 项目读 convention 不知道哪个结论正确。
- **Suggested fix (applied in Rev1)**: proposal §Why 加 "Aether vs Aria 时序矛盾" 表 + DEC §4 D4 convention 大纲扩 6→8 段,加 §0 Rationale + Observed contradiction。Aria 当前实测立场 = 更新的 ground truth SOT。
- **Status**: ✅ ADDRESSED in Rev1

### M-km-C-2: `aria-orchestrator/nomad/README.md` 行 170 主动误导

- **R1 location**: `aria-orchestrator/nomad/README.md` 行 170 故障排查表
- **Issue**: 原 wording `检查 HCL config.auth.password template 指向 Nomad Variable 正确` 是 active 误导。新 session owner 或 Lab 其他成员查表会按已证实无效的方案排查。proposal §Key Deliverables 漏列 nomad/README.md update。
- **Suggested fix (applied in Rev1)**: §What deliverable 3b 显式列 nomad/README.md 行 170 update + Key Deliverables 加进清单
- **Status**: ✅ ADDRESSED in Rev1

---

## §3 Important findings (16) — 8 cross-cutting 多 agent 共识 R2 addressed

### Cross-cutting cluster — Rev1 addressed

| ID | 主题 | Rev1 fix |
|----|------|---------|
| M-ba-I-3 + M-qa-I-1 | length-equal 不能证 cred 一致 (M5 R5 实证 + `[[feedback_test_mock_pattern_hides_prod_bug]]`) | 验收 B 改 fingerprint + round-trip mandatory (HTTP 200) |
| M-tl-I-2 + M-qa-I-2 | "独立 PAT rotation cycle" 是 dead reference | R1 escalation 决策树 3 步: 查 active rotation → piggyback if FORGEJO_BOT_PAT in scope → otherwise open Forgejo issue + block |
| M-ba-I-1 + M-km-C-1 | 精确机制 NOMAD_META_* vs template env timing | proposal §Why 加 1 段精确解释 + DEC §4 D4 §2 Mechanism |
| M-tl-I-1 | merge-order vs secret-guard track | proposal §Risks R5 (独立 standards/ branch, 不同文件,无写冲突) |
| M-tl-I-3 + M-km-I-2 | standards/ Lab-shareable scope | convention 用 Lab 占位符 + envsubst 模式声明 out-of-scope |
| M-ba-I-4 | config.json schema | DEC §4 D4 §4 锁死 schema (no email + base64 -w0) |
| M-km-I-1 | §5 PAT rotation 与 secret-hygiene §2.4 重叠 | DEC §4 D4 §5 改单向 reference secret-hygiene |
| M-km-I-3 | AD-M1-8 Revised note | §What deliverable 3c + Key Deliverables 加进 |
| M-km-I-4 | memory plan 缺失 | §What deliverable 3d + Key Deliverables 加 3 memory entries (1 update + 2 new) |

### Other Important — Rev1 partially addressed

| ID | 主题 | Rev1 处理 |
|----|------|---------|
| M-tl-I-4 | C "force image GC" 实际不可行 (同 M-ba-C-1) | 同 M-ba-C-1 Critical fix |
| M-ba-I-2 | 验收 A 单文件 grep (同 M-qa-C-1) | 同 M-qa-C-1 Critical fix |
| M-qa-I-3 | plugin config reload 语义 unresolved | §Risks R4 改 definitive 答案 (不需 restart;driver per-alloc 读) |
| M-ba-I-3 already counted | length-equal | counted above |

---

## §4 Minor findings (12) — ~6 absorbed in Rev1 sweep, ~6 deferred

### Rev1 absorbed (≤10 line touches)

- **M-tl-M-1** fingerprint 命令模板 → §What §2 B1 加 specific `python3 -c hashlib.sha256(...)[:12]` 命令
- **M-tl-M-2** commit message template by T1.0 分支 → DEC §4 D3 加 3 个 commit message template
- **M-tl-M-3** M6 dependency soft-block → proposal §Why 末加 "M6 soft-dependency" 段
- **M-ba-M-1** standards/README 双索引 → 验收 D 加 conventions-summary.md grep
- **M-ba-M-2** Nomad reload definitive (同 M-qa-I-3) → §Risks R4 改 definitive 答案
- **M-km-M-2** convention §7 + §8 → DEC §4 D4 扩 6→8 段
- **M-km-M-3** Aether Spec 槽 → DEC §6 reframe (补全 fix-hardcoded-docker-auth-node-login, 不开新 issue)

### Deferred — non-blocking

- **M-km-M-1** secret-hygiene + session-handoff 索引缺失 → 顺带 hygiene, owner 决, 不阻 Rev1
- **M-qa-M-1** D "索引出现" 模糊 → 已通过 M-ba-M-1 + M-km-C-2 升级为 binary grep, 不需独立处理
- **M-qa-M-2** dispatch-issue.sh / t5-run-demo.sh 已知 broken → T1.0 报告标 follow-up Forgejo issue, 不在本 Spec scope
- **M-qa-M-3** non-forgejo registry impact → §Out of Scope 加 1 行 verified (aria-build/layer1 no auth block)
- **M-ba-M-3** Rollback ordering → §Acceptance 顶部加 ordering invariant + 各 risk mitigation

---

## §5 Strategic observations (tech-lead, 非 finding)

1. **Probe-first discipline 第二次实证** — 本 Spec drafting 用 probe-first 把 scope 从 ~2-4h 压到 ~1.5-2.5h, 是 [[feedback_prod_state_must_ground_playbook]] 跨 session 第二次应用。phase-a-planner skill 应固化"drafting 前必跑 probe"为 mandatory step。Phase D.3 应新增 memory `feedback_probe_first_scope_reframe`。
2. **借机 sister HCL drift forensic** — T1.0 probe 可顺手 audit `aria-runner-template` ↔ `aria-layer2-runner` 完整 divergence 作 M3 era 历史 reference,防未来 forensic 浪费时间。
3. **Aria secret 体系两端闭环** — 本 Spec + `aria-secret-guard-plugin-default` 都是 2026-05-20 secret rotation event 下游, 一端 conversational hygiene (LLM-readable, Rule #7 enforcement),一端 deployment hygiene (node-level SOT, Rule #7 deploy-side enforcement)。两 Spec done 后写联合 retrospective 在 `2026-05-20-secret-rotation-during-m5-deploy.md` 续记 — 这会成为后续 Vault/Workload Identity 接入的 baseline。

---

## §6 R2 readiness checklist

Rev1 sweep 完成产物:
- ✅ proposal.md → Draft v2 (本 audit 所有 Critical + 8 cross-cutting Important + ~6 absorbed Minor)
- ✅ DEC §4 D3 commit message template + §4 D4 convention 大纲 6→8 段 + §6 Aether Spec 槽 reframe + §7 Audit history (本 R1 记录)
- ✅ 本报告归档 `.aria/audit-reports/post_spec-R1-2026-05-23T0900Z-aria-layer2-docker-auth-cold-pull-fix-orchestrator.md`
- ⏳ R2 4-agent verify (Task #3) — 目标 4/4 PASS_WITH_WARNINGS + 0 NEW critical + ≥70% Important 减少 (per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`)

---

## §7 Cross-references

- **Spec proposal**: `openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md`
- **Decision memo**: `.aria/decisions/2026-05-23-layer2-docker-auth-cold-pull-fix.md`
- **Parent handoff**: `docs/handoff/2026-05-23-m5-phase-c-o3-done-d2-close.md` §2 F2/F3 + §3 R2
- **Sister Spec** (orthogonal): `openspec/changes/aria-secret-guard-plugin-default/` (Phase A done, Phase B pending)
- **R1 raw transcripts**: preserved in session conversation history (2026-05-23 ~07:00-09:00 UTC), 4 agent outputs full content

**Created**: 2026-05-23 ~09:00 UTC
**Author**: solo-lab (uni.concept.wzfq@gmail.com), aggregated by Claude Opus 4.7
