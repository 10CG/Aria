# Decision: M1 T1.b Spike Templates v0.2-reviewed — Agent Team Audit Convergence

> **Status**: Decision recorded (converged)
> **Date**: 2026-04-19
> **Scope**: `aria-orchestrator/spikes/m1-registry-auth/{spike-report.md, access-audit-report.md}` 模板 pre-draft 质量审计
> **Pattern**: multi-agent parallel review + 1 round verification (R1 → R2 = 0 Critical)
> **Parent**: [US-021 Phase B.2 T1.b](../../openspec/changes/aria-2.0-m1-mvp/tasks.md)

---

## 背景

2026-04-18 session handoff (`2026-04-18-m1-phase-b-predraft-session.md`) 交付了 T1.b spike 需要的 owner-fill 模板两份, 作为 AI pre-draft 产物. 2026-04-19 new session 入口通过 `aria:state-scanner` 恢复, owner 请求"并行起草模板"→ AI 产出 v0.1-draft (~270 行) → 请求"集体评审"→ 触发 5-agent team audit → 收敛至 v0.2-reviewed.

本决定记录审计轨迹, 供 T6.3 M1 Report 与 AD-M1-1/8 回填引用.

---

## Agent Team 构成

### Round 1 (初审, parallel)

| Agent | 聚焦维度 | 提交 findings |
|-------|---------|-------------|
| `aria:tech-lead` | AD 回填充分性 / M1-M2 scope 守护 / handoff schema 契约 | 3 Critical, 3 Important, 3 Minor |
| `aria:backend-architect` | Forgejo API 技术准确性 / 可回放性 / failure mode | 2 Critical, 4 Important, 2 Minor |
| `aria:legal-advisor` | 签字格式 mechanical gate / disclaimer / residual risk chain | 4 Critical, 3 Important, 2 Minor |
| `aria:qa-engineer` | 验收标准机械化 / 边界条件 / verdict 三态 | 3 Critical, 4 Important, 2 Minor |
| `aria:knowledge-manager` | 命名一致 / 交叉引用 / 归档可寻性 / 占位符统一 | 3 Critical, 4 Important, 3 Minor |
| **小计** | — | **15 Critical, 18 Important, 12 Minor** |

### Round 2 (验证, 3 agents, 聚焦 R1 Critical 修复效果)

| Agent | 验证聚类 | Verdict |
|-------|---------|---------|
| backend-architect | 聚类 A (Forgejo API 准确性) | CONVERGED (0 新 finding) |
| legal-advisor | 聚类 B (签字 / Verdict gate 统一) | CONVERGED (1 PARTIAL 建议已吸收) |
| qa-engineer | 聚类 D (证据粒度 / cache hit / 503 分离) | CONVERGED (1 Minor 措辞已吸收) |

---

## 6 聚类修复摘要

### A — Forgejo API 准确性 (BA 主责)

| 问题 | 修复 |
|------|------|
| `has_packages` 字段不在 Forgejo API schema | `access-audit §2.4` 改用 `/repos/.../settings` + `/packages/10CG?type=container` |
| `forgejo GET /admin/config` 不是真实 endpoint | `access-audit §3.1` 改为三路备选 (ssh app.ini / admin panel / UNCLEAR 降级) |
| `/admin/actions?type=package_push` 同样伪造 | 删除 |
| 匿名 pull 预期 401/403 不一致 | 统一 "401 (WWW-Authenticate Bearer) 或 403 均 PASS" |
| Forgejo tag 删除路径模糊 | `spike-report §9` 补完整 API: `/packages/10CG?type=container` + `.id` |

### B — 签字 / Verdict Gate 统一 (LA 主责)

| 问题 | 修复 |
|------|------|
| 三份文件 (memo §11 / spike §11 / audit §6) 签字格式三样 | 统一三行: `Signed-by / Verdict / Scope` |
| `PASS_WITH_WARNINGS` 触发规则缺失 | `access-audit §1` 前加机械降级规则 |
| `spike.Outcome ↔ audit.Verdict` 联动未锁 | 双文件各加 `Consistency check (mechanical)` 块 |
| spike-report 缺 Footer Disclaimer | 新增 `§13 Footer Disclaimer` (对齐 AD-M0-6 + memo §12) |
| audit §6 Rationale 未澄清 "audit PASS ≠ Anthropic 合规" | 新增 `§6.3 Scope 分离声明` |
| §4 Residual 脱钩 Luxeno cleanup | §4 新增 "Luxeno legacy cleanup status" 行 + spike §10.6 独立签字声明 (R2 LA L1) |

### C — AD 回填完整性 (TL + KM 主责)

| 问题 | 修复 |
|------|------|
| `image_refs.registry_auth_method` 不在 proposal handoff schema | 改 `legal_assumptions.registry_auth_method` + schema amendment 注释 (守 AD-M1-7 additive 窗口) |
| spike §10 缺 AD-M1-1 3 项必填 (Secret store / Rotation 自动化 / Luxeno transition audit) | §10 扩展为 6 子节 (10.1-10.6) |
| Rotation policy 缺 `Injection method` 字段 (未锁 AD-M1-11) | §10.3 新增字段 + AD-M1-11 交叉引用 |
| AD-M1-x 引用无 path+anchor | 首次出现改 `(见 [architecture-decisions.md §AD-M1-x](../../docs/architecture-decisions.md#ad-m1-x))` |

### D — 证据可复核性 (QA 主责)

| 问题 | 修复 |
|------|------|
| Pull 验证 cache hit 假阳性 | 加 `docker image rm` + `docker image prune -f` 强制清 + 记 `Pull complete` 行数 |
| 503 vs 401 未分离 | 非 4xx auth rejection → `RETRY` 不计 PASS (三处一致: audit §2.1 / §2.3 / spike §7) |
| 命令块无时间戳 | 所有 bash 块前加 `date '+%Y-%m-%d %H:%M:%S'` |
| sha256 digest 捕获不可靠 | `spike §5` 双源捕获 (push output + registry API canonical) + 一致性比对 |
| Push 耗时无上限 | push > 60s 触发 warning + 分析网络路径 |
| Option C 回退原因自由文本 | §8 要求格式 `[procedure §Step 5 诊断表条目 N: error] → 无法修复原因` |

### E — 文档结构 (KM 主责)

| 问题 | 修复 |
|------|------|
| Front-matter 缺 `Status` | 两份均加 `Status: template (owner-to-fill)` |
| anchor slug 不稳 | 缩短为 `#7-forgejo` |
| 版本历史表缺 | §版本历史 加 v0.1-draft → v0.2-reviewed |
| 占位符三种格式混用 | 统一 `[OWNER-TO-FILL: hint]` + `[PASS/FAIL/N/A]` |
| PAT 路径两份重复 | audit §2.2 改 "见 spike-report §3" (single source of truth) |
| Audit §5 Gate 措辞歧义 "4 PASS_WITH_WARNINGS" | 改 "§0 Verdict ∈ {PASS, PASS_WITH_WARNINGS}" (R2 QA N1) |
| §2.4 legal memo 版本未标注 | 加 "v0.2+" 版本注脚 (R2 LA L2) |

### F — Scope 守护 (TL 主责)

| 问题 | 修复 |
|------|------|
| audit §4 混入 M2 关切 (HA / 季度 re-audit) | 迁至 §5 Open Issues, §4 仅留 M1 可控项 (PAT 泄露 / Bot 权限 / Luxeno carryover) |

### Minor 批

- PAT 文件名 hardcode `20260418` → `$(date +%Y%m%d)` 占位
- Forgejo 1.21+ `[log] + [actions]` 版本差异注
- §0 Summary `≤120 字` 硬约束
- `Build platform` 字段 (multi-arch 记录)
- spike §11 Outcome 四态 → 三态 (移除 Option B, 与 procedure Deliverables 一致)

---

## R2 Polish 吸收 (第 2 轮 CONVERGED 后的 non-blocking 小修)

| 来源 | 建议 | 落位 |
|------|------|------|
| LA R2 L1 | Luxeno cleanup 与 registry audit 独立签字声明 | `spike-report §10.6` 新增"独立签字声明"段 |
| LA R2 L2 | access-audit §2.4 legal memo 版本引用 | 注脚标 "legal memo §7 [v0.2+]" |
| QA R2 N1 | Gate 措辞 "4 PASS_WITH_WARNINGS" 歧义 | 改为 "§0 Verdict ∈ {PASS, PASS_WITH_WARNINGS}" |

---

## 收敛指标

```
R1 findings:  15 Critical / 18 Important / 12 Minor = 45 total
R2 findings:  0 Critical / 0 Important / 2 Minor (advisory, 已吸收)
Convergence:  R1 → R2 = 0 Critical, CONVERGED per feedback_audit_convergence_pattern

注: 本次 review scope 小 (2 份模板), 采用 1-round verification 而非标准 5-round pre_merge pattern.
    大 scope (如 pre_merge 合入 master) 仍需走 5-round + 稳定性确认轮标准流程.
```

---

## 产出文件

### aria-orchestrator submodule

- `spikes/m1-registry-auth/spike-report.md` — v0.2-reviewed (14 节, ~270 行, untracked → commit pending)
- `spikes/m1-registry-auth/access-audit-report.md` — v0.2-reviewed (8 节, ~220 行, untracked → commit pending)

### Aria 主仓库

- `.aria/decisions/2026-04-19-m1-t1b-template-review.md` — 本文件

---

## 对下游任务的 Unblock

| 任务 | 依赖 | 状态 |
|------|------|------|
| T1.b.1 Forgejo bot + PAT 创建 | — | **UNBLOCKED** (owner 可按 spike-procedure §Step 1-2 执行) |
| T1.b.2 docker push smoke | T1.b.1 | **UNBLOCKED** (spike-report §5 template ready) |
| T1.b.3 access audit | T1.b.2 | **UNBLOCKED** (access-audit template ready + Verdict 降级规则机械化) |
| T1.c.2-4 真 build + 三节点 pull | T1.b 全链路 PASS | Blocked on owner |
| T6.3 AD-M1-1/8 回填 | T1.b §11 + §6.4 双签字 | Blocked on T1.b 执行 |

---

## 下一步

1. Owner 按 `aria-orchestrator/spikes/m1-registry-auth/spike-procedure.md` §Step 1-7 执行 spike
2. 填充 `spike-report.md` 与 `access-audit-report.md` 所有 `[OWNER-TO-FILL]` 占位
3. 签字 `§11` + `§6.4` (机械 gate)
4. 若 spike.Outcome = Option A + audit.Verdict ∈ {PASS, PASS_WITH_WARNINGS} → T1.c.2-4 docker build/push 真实镜像
5. 完成后触发 new AI session 继续 T4/T5 (per 2026-04-18 handoff §AI-Next-Session)

---

## Memory 候选

- 是否新建 `feedback_small_scope_audit_1_round.md`? (v0.2-reviewed 证明小 scope pre-draft 用 1-round verification 足够, 不需要 5-round 标准流程)
- 是否更新 `feedback_audit_convergence_pattern.md` 加入 "scope-sized audit rounds" 维度?
- 决议: 本次暂不建, 需 2-3 次同类样本再归纳

---

**AI advisory attribution**: 本评审产出由 Claude session 编排 8 个 agent 完成 (R1 × 5 + R2 × 3). 所有结论为 advisory, 最终采纳由 owner (simonfish) 决策. per AD-M0-9.
