---
checkpoint: post_spec
mode: convergence
round: 1
change_id: aria-issue-triage-sop
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
unanimous_vote: PASS_WITH_WARNINGS
timestamp: 2026-05-13T00:30Z
context: openspec/changes/aria-issue-triage-sop/
agents: [aria:tech-lead, aria:knowledge-manager, aria:qa-engineer]
r1_findings_total: 30
r1_critical: 4
r1_major: 13
r1_minor: 13
adaptive_level: 2
---

# aria-issue-triage-sop post_spec R1 — 2026-05-13T00:30Z

> **R1 verdict**: PASS_WITH_WARNINGS (3/3 unanimous, no FAIL/NEEDS_FIX vote)
> **Trigger**: Phase A.2 post_spec audit for Level 2 minimal Spec, convergence mode
> **Next**: Apply C+M findings → R2 verify convergence (target: SCOPE_OK_R2)

---

## Vote distribution

| Agent | R1 Vote | Findings (C/M/m) | Focus area |
|-------|---------|------------------|-------------|
| aria:tech-lead | PASS_WITH_WARNINGS | 1C / 4M / 3m = 8 | SOP architecture, Rule #9 strategy |
| aria:knowledge-manager | PASS_WITH_WARNINGS | 1C / 4M / 5m = 10 | doc placement, truth-source, cross-refs |
| aria:qa-engineer | PASS_WITH_WARNINGS | 2C / 4M / 5m = 11 | test strategy, dogfooding, repro accuracy |
| **Total** | **PASS_WITH_WARNINGS** | **4C / 12M / 13m = 29** | |

(Aggregate count 29 ≠ 30 due to 1 finding overlap KM-m4 ≈ TL-C1; deduplicated below.)

---

## Critical findings (4 — must fix before A.3)

| ID | Theme | scope | Suggested fix | Status |
|----|-------|-------|---------------|--------|
| TL-C1 | Skill vs Command 是伪选择,Q1 应直接关闭 | proposal §Open Q1 | 关闭 Q1: "Skill (SKILL.md + scripts/), 通过 /issue-triage 触发,与 state-scanner 同构" | _open_ |
| KM-C1 | Step 2 版本路径硬编码 Aria 自身,无法跨仓库 | tasks T1.3 / proposal §Step 2 | fail-soft chain: plugin.json → VERSION → package.json → unknown | _open_ |
| QA-C1 | verdict 枚举缺 partial-repro — #101 自身落不到 6 枚举任一 | proposal §6-step + verdict | 加第 7 枚举 partial-repro + deviation_note 字段 | _open_ |
| QA-C2 | "80% field match" 无 denominator 也无 weighting,acceptance 不可验证 | proposal §Success Criteria + tasks T5.2 | 改为 hard-gate (version/code/git) + soft-fields % rubric, 单 SOT | _open_ |

---

## Major findings (12)

| ID | Theme | scope | Suggested fix |
|----|-------|-------|---------------|
| TL-M1 | Rule #9 应解耦出本 cycle (precedent: Rule #7/8 incident 驱动) | proposal §Open Q2 + tasks T6 | T6 改为 "decision memo 进 docs/decisions/, 延后到 ≥3 dogfood + 1 missed-triage incident 后再评估" |
| TL-M2 | Step 5 in-flight check 漏 worktree + 本地未推送分支 | proposal §Step 5 + tasks T1.6 | T1.6 拆 (a) remote PR/branch (b) local branches (c) worktrees,3 段 JSON |
| TL-M3 | Step 6 "AI 无法纯机械" 与 Success Criteria "不需 user interaction" 矛盾 | proposal §Step 6 + Success Criteria #3 | 改 SC: 步骤 1-5 不需 interaction, 步骤 6 三模式 (auto / pause / skip→needs-info) |
| TL-M4 | verdict 缺 severity + recommended_action 正交字段 | triage-report JSON schema | 加 severity (C/M/m/trivial) + recommended_action (hotfix/next-cycle/backlog/close) |
| KM-M1 | SKILL.md vs convention doc 真理来源未声明 → drift 风险 | proposal §What + References | 显式: convention doc = SOT, SKILL.md 引用而非复制,镜像 Rule #7 模式 |
| KM-M2 | 缺 Rule #6 skill-creator benchmark (新 Skill 不可协商) | tasks.md 全体 | 新增 T8: /skill-creator benchmark issue-triage → ab-results/, T7.2 pre-merge gate 列必需 |
| KM-M3 | forgejo CLI 调用未提 secret-hygiene Rule #7 合规 | tasks T1.2/T1.6 | subprocess capture_output=True 显式声明; proposal References 加 secret-hygiene.md |
| KM-M4 | Rule #9 (如加) 主体应指向 convention doc (镜像 Rule #7) | tasks T6.2 | Rule #9 body in standards/conventions/issue-triage.md, CLAUDE.md 仅摘要 (本 cycle 已决: Rule #9 不加, 见 TL-M1) |
| QA-M1 | triage-report JSON 缺 schema_version + version stamp 必需字段 | tasks T1.7 | 必需字段: schema_version (semver), triage_tool_version, issue_ref, generated_at, steps[1..5], repro, verdict; jsonschema 强制 |
| QA-M2 | Step 6 缺结构化 repro 模板 → 同型 #101 hallucination 风险 | proposal §Step 6 + tasks T2.1 | per-case schema: {case_id, input, expected, actual, match: bool, notes}; "not-reproducible" 也需 ≥1 case 记录 |
| QA-M3 | T4 缺 CI 集成 + binary tar.gz fixture 易漂移 | tasks T4 | T4.5: 接入 CI workflow YAML; conftest.py programmatic git fixture 替代 tar.gz |
| QA-M4 | API rate-limit / auth failure 致部分 collector null,与 "无数据" 难分 | tasks T2.3 + T1.8 | 每 collector 加 collection_status: ok/error/skipped; exit code 20 = partial, 30 = total fail |

---

## Minor findings (13 — defer 可)

| ID | Theme | Quick action |
|----|-------|--------------|
| TL-m1 | Effort 9.5h 偏紧 | 标 "9.5h optimistic / 12h pessimistic" |
| TL-m2 | 与 aria-report Skill 边界 | SKILL.md 加 "与 aria-report 的关系" 段 |
| TL-m3 | T5.3 硬编码 #101 实测 2/4 数字 | 改为 "verdict + cited 主因 file 一致, hit_rate 差异 ≤1 case" |
| KM-m1 | change-id `-sop` 后缀 vs Skill `issue-triage` 不对称 | proposal header 加映射注 |
| KM-m2 | case study 引用缺 issuecomment-5972 URL | T3.2/T5.2 加链接 |
| KM-m3 | T3.3 "standards README 更新" 目标不明 | 改为 "CLAUDE.md 导航表更新 (如需)" 或删除 |
| KM-m4 | Q1 已是非问题 | 与 TL-C1 dedup, 关闭即可 |
| KM-m5 | 不入 standards/methodology/ 应显式说明 | proposal §What 加一行排除注 |
| QA-m1 | binary tar.gz fixture 易漂移 | (并入 QA-M3) |
| QA-m2 | likely_fix_present 缺 confidence | 改为 likely_fix_candidates: [{sha, message, match_reason}] |
| QA-m3 | T5.3 vs SC 双重 acceptance | SC 删除 80% 改为 T5.3 表述 (并入 QA-C2) |
| QA-m4 | cited_files 正则未定义 | T1.4 列 3 citation format + test case |
| QA-m5 | 0/5 steps null 仍出 verdict 风险 | triage.py pre-flight: steps_with_data<2 → exit 30 |

---

## Open question recommendations (3 agents unanimous on all 4)

| Q | Recommendation | Rationale (3 agents 一致) |
|---|----------------|---------------------------|
| Q1 Skill vs Command | **Skill (SKILL.md + scripts/), 通过 /issue-triage 触发** | Aria 36 既有 Skill 同模式,非真二选一 |
| Q2 Rule #9 强制度 | **本 cycle 不加 Rule, 仅产 decision memo 延后** | Rule #7/8 都是 incident 驱动入册,本 SOP 缺该证据链 |
| Q3 跨仓库支持 | **Day-1 支持任何 Forgejo repo** | forgejo CLI 已通用; 仅 Step 2 需 fail-soft (KM-C1) |
| Q4 触发时机 | **M1 仅手动** | webhook 需 aria-runner-bot 基础设施, 与 SOP 正交, 推后续 |

---

## Convergence analysis (R1 → R2 prep)

- **Unanimous PASS_WITH_WARNINGS**: ✅ (no FAIL/NEEDS_FIX in any agent vote)
- **4-tuple stability**: N/A (this is R1, no R0 to compare)
- **Pragmatic convergence (per feedback memory)**: requires R2 to verify Criticals closed + verdict 改善 + 无新 Critical
- **Decision**: 应用 4 Critical + 12 Major 修正 → 跑 R2,目标 SCOPE_OK_R2

---

## R1 → R2 fix plan (per Aria precedent)

1. `proposal.md` 改动:
   - 关闭 Q1 + Q2 (TL-C1, KM-m4, TL-M1)
   - Step 2 fail-soft (KM-C1)
   - 加 7 枚举 + severity/recommended_action 字段 (QA-C1, TL-M4)
   - Step 5 worktree+local 拆 3 段 (TL-M2)
   - Step 6 三模式 (TL-M3)
   - Success Criteria 替换 80% → hard-gate + soft-% (QA-C2)
   - References 加 secret-hygiene.md (KM-M3)
   - 真理来源声明 (KM-M1)
   - 显式排除 methodology/ (KM-m5)

2. `tasks.md` 改动:
   - T1.3 fail-soft (KM-C1)
   - T1.4 列 3 citation format (QA-m4)
   - T1.6 三段 inflight (TL-M2)
   - T1.7 enumerate required fields + jsonschema (QA-M1)
   - T2.1 加 repro template + 与 aria-report 边界 (QA-M2, TL-m2)
   - T4.5 CI 集成 + programmatic git fixture (QA-M3, QA-m1)
   - T5.2 scoring rubric (QA-C2)
   - T5.3 改为 verdict 一致 + ≤1 case 差异 (TL-m3)
   - T6 → decision memo (TL-M1)
   - T8 skill-creator benchmark (KM-M2)
   - collection_status per collector (QA-M4)
   - pre-flight steps_with_data<2 → exit 30 (QA-m5)

3. R2 spawn 同 3 agent, 输入 R1 findings + 修订版 proposal/tasks

---

## Audit trail

- R1 timestamp: 2026-05-13T00:30Z
- Trigger issue: [Forgejo Aria #101](https://forgejo.10cg.pub/10CG/Aria/issues/101) (state-scanner _normalize_status bug)
- Triage comment: [issuecomment-5972](https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-5972)
- Pre-write validation: ✅ change_id `aria-issue-triage-sop` proposal.md exists in openspec/changes/
- Checkpoint completeness: N/A (post_spec checkpoint, not pre_merge)
