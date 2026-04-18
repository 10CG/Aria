# Decision: M1 Phase B Pre-draft Session Handoff (2026-04-17 → 2026-04-18)

> **Status**: Session closeout 归档
> **Pattern**: AI-predraft all AI-executable artifacts + flag owner-only items for new session
> **Trigger**: owner request 执行当前对话收尾, 未完成打包进新对话

---

## 背景

本决定记录 2 天 AI session (2026-04-17 → 2026-04-18) 的收尾结构, 明确:
1. 哪些产出已 AI-completed 且 committed
2. 哪些是真正 owner-only action items (infra / signature)
3. 哪些 AI 工作延后到新 session (依赖 owner 前置)
4. 新 session 如何通过 `/state-scanner` 入口无缝恢复

---

## Session Scope

### 起点
2026-04-17 session 开始: M0 US-020 ~90%, 剩 T6.4 Phase 2 + Spec 归档 + pd_signoff

### 终点
2026-04-18 session 结束:
- **M0 US-020**: done 2026-04-17 (full lifecycle + Aria#20 merged to master)
- **M1 US-021**: Phase A ✅ + Phase B.1 ✅ + Phase B.2 T0 ✅ + T1-T4 pre-draft ✅
- **下一步**: owner 执行 T1 infrastructure action items → AI 继续 T5/T6

---

## AI-Completed Artifacts (Session 产出)

### Aria 主仓库 (`feature/aria-2.0-m1-mvp` @ 82fdd1c)

```
docs/requirements/user-stories/US-021.md          — M1 MVP Story (draft)
docs/requirements/user-stories/US-022.md          — M2 Layer 1 placeholder
docs/requirements/prd-aria-v2.md                   — US-020~027 重排 + milestone 更新
openspec/changes/aria-2.0-m1-mvp/proposal.md       — Level 3 Spec (9+2 AD-M1 decisions)
openspec/changes/aria-2.0-m1-mvp/tasks.md          — T0-T6 分解 + STCO Agent 分配
openspec/changes/aria-2.0-m1-mvp/artifacts/
  ├── issue-schema-v0.1.md                         — T3.1.1
  └── validate-issue-schema.py                     — T3.1.2 (stdlib, DEMO-001/002 PASS)
.aria/issues/DEMO-001.yaml                         — synthetic trivial (pipeline)
.aria/issues/DEMO-002.yaml                         — synthetic non-trivial (quality)
.aria/decisions/2026-04-17-aria-2.0-m1-scope-reorg.md
.aria/decisions/2026-04-18-m1-phase-b-predraft-session.md  — 本文件
aria-plugin-benchmarks/ab-suite/m1-mvp/fixtures/   — M1 fixture repo stub
```

### aria-orchestrator 子模块 (master @ 7fa981c)

```
docs/m1-legal-carryover.md                         — v0.2-advisory (AI-researched Anthropic ToS)
docs/bot-token-lifecycle-design.md                 — v0.2 (Forgejo API + rotation script)
docs/architecture-decisions.md                     — AD-M1-1~11 占位 + AD-M1-10 decided (envsubst)
docker/aria-runner/Dockerfile                      — M1 scaffold (ENV ARIA_MODEL / GIT_AUTHOR_*)
docker/aria-runner/entrypoint-m1.sh                — 538 行 11-step T4.1.1 pre-draft
docker/aria-runner/prompts/issue-dispatch.md       — T3.4.1 (5-var envsubst whitelist)
docker/aria-runner/lib/parse-stream-json.sh        — T4.2 (jq result frame + fallback)
docker/aria-runner/lib/compute-assertions.sh       — T4.3 (literal substring + header filter)
nomad/jobs/aria-runner-template.hcl                — T2.2.1 (parameterized dispatch)
nomad/client-config/host-volume.hcl                — T2.1.1 (outputs RW + inputs RO)
nomad/README.md                                    — deployment + 排错手册
nomad/registry-push-guide.md                       — T1.c.5 (.env.local mode)
spikes/m1-registry-auth/spike-procedure.md         — T1.b.1 7-step checklist for owner
scripts/dispatch-issue.sh                          — T3.3.1 (manual dispatch + poll)
```

### Audit Trail

```
post_spec audit:      6 轮 × 7 agents (45 → 31 → 21 → 1 → 0 → 0 strict convergence)
post_planning audit:  4 轮 × 7 agents (26 → 11 → 2 → 0 strict convergence)
Total agent calls:    70 (7 agents × 10 rounds)
```

---

## Owner Action Items (真正 owner-only, 按依赖顺序)

### Priority 1 (解锁 T3/T4 启动)

1. **T1.a.1** 基于 [memo v0.2 §11 sign-off](../../aria-orchestrator/docs/m1-legal-carryover.md) 审阅 AI advisory + 签字
2. **T1.a.2** 发送 Luxeno cleanup request ([template §9](../../aria-orchestrator/docs/m1-legal-carryover.md)), 等 Luxeno 回应
3. **T1.a.3** 基于 §11 template 签最终 signature line (solo-lab owner 职责)
4. **T1.b.1** 按 [spike-procedure.md](../../aria-orchestrator/spikes/m1-registry-auth/spike-procedure.md) 执行 7 步 (bot account + PAT + docker push smoke)
5. **T1.b.3** 产出 access-audit-report.md + 签字
6. **T1.c.2-4** 按 [registry-push-guide.md](../../aria-orchestrator/nomad/registry-push-guide.md) docker build/push 双 tag + 三节点 pull 验证

### Priority 2 (解锁 T3.2+ 执行)

7. **T2.1** 按 [nomad/README.md](../../aria-orchestrator/nomad/README.md) §Step 1 配置三节点 host_volume + smoke dispatch 验证
8. **T2.3** Resource profiling (stress-ng)

### Priority 3 (解锁 T5 执行)

9. **T3.2.3** DEMO IP classification audit owner signoff
10. **T4.5** 真实 Anthropic API smoke (DEMO-001 一次)
11. **T4.6** (T5.1.0 time) entrypoint-m1.sh → entrypoint.sh swap + image rebuild

### Priority 4 (T5 全流程)

12. **T5.1** DEMO-001 5 轮
13. **T5.2** DEMO-002 5 轮
14. **T5.2.3** 5 个 PR diff owner review + signoff
15. **T5.3/5.4** 统计 + Week 2 checkpoint 评估

### Priority 5 (T6 收尾)

16. **T6.1** M1 Report 起草 (based on T5 实测)
17. **T6.2** handoff-m1.yaml + validator PASS (final)
18. **T6.3** AD-M1-1~11 回填 (基于 T1-T5 实测结论)
19. **T6.4** Owner final Go/No-Go/revision signoff

---

## AI-Next-Session 工作 (等 owner 前置完成后)

### T4/T5 支持工作 (可与 owner 并行)

- [ ] `entrypoint-m1.sh` 5 种 stream-json fixture 单元测试 (per AI-R1-3)
  - Fixture 1: 正常 result 帧
  - Fixture 2: 无 result 帧 (timeout SIGKILL)
  - Fixture 3: is_error=true
  - Fixture 4: 格式损坏 / 截断 JSON
  - Fixture 5: 多 result 帧取最后
- [ ] `validate-m1-handoff.py` 起草 (T6.2.2, 仿 M0 pattern)
  - schema v1.0 字段必填
  - outcome enum + SUM(distribution) == runs 约束
  - legal_assumptions orphan 检测 (anthropic_api_terms_verified=true 需 memo + 签字)
  - go_decision 4-enum 验证
  - image_refs.immutable_sha 非空 (非 scaffold 占位)

### T6 Report 模板前置 (owner 提供 T5 data 后填充)

- [ ] `m1-report.md` 结构模板 (§0 Summary / §1 Image / §2 Nomad / §3 DEMO / §4 Legal / §5 Open issues / §6 Signoff)

### AD 回填支持 (T6.3)

- [ ] AD-M1-1 Registry auth 最终决议 (based on T1.b.1 实测)
- [ ] AD-M1-2 Image tag 策略 (based on T1.c 产出)
- [ ] AD-M1-3 Issue schema (M1 执行后可能需要 v0.1 修正)
- [ ] AD-M1-4 Outcome enum (T4/T5 实际使用分布)
- [ ] AD-M1-5 DEMO 选型 (实际执行效果)
- [ ] AD-M1-6 LLM 栈 (T4.5 真实调用验证)
- [ ] AD-M1-7 M1/M2 契约 (handoff schema final 态)
- [ ] AD-M1-8 Registry access control (audit report)
- [ ] AD-M1-9 ip_classification governance (M2+ 治理流程)
- [ ] AD-M1-10 Prompt engine (决议已 decided 2026-04-18, 保留 execution review)
- [ ] AD-M1-11 API key inject (T2.2.1 Spike 结果)

---

## 新 Session 入口 (state-scanner pattern)

### 恢复流程 (新 session)

```
用户: 遵循 aria 规范, 查看当前项目状态, 给我建议
  ↓
Skill: aria:state-scanner 自动执行
  ↓
收集:
  - git: feature/aria-2.0-m1-mvp @ 82fdd1c (clean, 0/0 vs origin)
  - OpenSpec: 3 active drafts (aria-2.0-m1-mvp + silknode + state-scanner-mechanical-enforcement)
  - Issue: #21 open (US-021 tracking)
  - Memory index: project_m1_session_handoff.md (本 session 产物)
  ↓
推荐:
  若 owner 尚未开始 T1 → [1] 打开 spike-procedure.md 开始 T1.b
  若 T1 部分完成 → [2] 继续未完成 action item
  若 T1 全完成 → [3] 解锁 T2 + 让 AI 起草 T4 单元测试并行
```

### Entry memory (next session 应读)

- `MEMORY.md` → `project_m1_session_handoff.md` (本 session 总结)
- `project_us021_us022_reorg.md` (范围重排)
- `feedback_audit_convergence_pattern.md` (10 轮 audit pattern 传承)
- `feedback_submodule_branch_before_archive.md` (M0 实战教训)
- `feedback_ai_advisory_catches_spec_bugs.md` (legal-advisor 贡献 pattern)

### 关键 links

```
US-021 Story:           docs/requirements/user-stories/US-021.md
M1 Spec:                openspec/changes/aria-2.0-m1-mvp/proposal.md
M1 Tasks + STCO:        openspec/changes/aria-2.0-m1-mvp/tasks.md
M1 Legal Memo v0.2:     aria-orchestrator/docs/m1-legal-carryover.md
M1 Spike procedure:     aria-orchestrator/spikes/m1-registry-auth/spike-procedure.md
M1 Entrypoint draft:    aria-orchestrator/docker/aria-runner/entrypoint-m1.sh
M1 Nomad HCL:           aria-orchestrator/nomad/jobs/aria-runner-template.hcl
M1 scope reorg:         .aria/decisions/2026-04-17-aria-2.0-m1-scope-reorg.md
M1 predraft handoff:    .aria/decisions/2026-04-18-m1-phase-b-predraft-session.md (本文件)
Forgejo Issue:          https://forgejo.10cg.pub/10CG/Aria/issues/21
```

---

## Session 指标

- **持续时间**: 2 天 (2026-04-17 → 2026-04-18)
- **Commits**: 主仓库 7 个 + aria-orchestrator 8 个
- **文件产出**: ~20 文件, ~3000 行
- **Agent 协作 audit**: 70 calls (7 agents × 10 rounds over 2 checkpoints)
- **AI 工时估算**: ~20h 研究 + 起草 + 审计编排
- **Owner 预期工时**: ~70h (T1 infra + T2 部署 + T5 DEMO + T6 Report, per tasks.md 分配)

---

**Signed-by (session handoff audit trail)**: ai:aria-agent @ 2026-04-18
**Reference**: per AD-M0-9, AI session 产出均为 advisory, owner 负责最终采纳 / 修正 / 签字。
