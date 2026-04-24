---
checkpoint: pre_merge
round: 1
timestamp: "2026-04-24T00:00Z"
spec: state-scanner-mechanical-enforcement
pr_main: https://forgejo.10cg.pub/10CG/Aria/pulls/33
pr_submodule: https://forgejo.10cg.pub/10CG/aria-plugin/pulls/20
verdict_distribution:
  HOLD_DRAFT: 2
  MERGE_WITH_REVISIONS: 2
anchor_alignment_distribution:
  partial: 3
  full: 1
recommendation_distribution:
  continue_draft: 3
  merge_now: 1
collective_verdict: HOLD_DRAFT
collective_recommendation: continue_draft
converged: false
---

# Round 1 pre_merge Aggregated Findings

## 共识 Critical (≥2 agents)

| ID | Agents | Issue |
|---|---|---|
| R1-C1 | TL / BA / QA | Phase 1.13 (原始 Why 痛点) 不在 PR, 合并后漏跑仍可复现 |
| R1-C2 | TL / QA | 0/9 acceptance criteria 满足 |
| R1-C3 | TL / QA | SKILL.md Step 0 未落地 → scan.py 是死代码 |
| R1-C4 | TL / QA | T6 测试覆盖 0% + T10 benchmark 未跑 |
| R1-C5 | TL / BA / QA / CR | schema.md 死链 (docstring 引用未存在文件) |
| R1-C6 | TL | 3 sister-bug 修改语义但违 proposal §非目标 "不改变数据采集语义"; 需 Revisions 章节显式 document |

## 共识 Important (≥2 agents 或 单 agent 高严重)

| ID | Agents | Issue |
|---|---|---|
| R1-I1 | BA | snapshot_schema_version additive-change 规则未 document (T3 加 key 时是否 bump) |
| R1-I2 | BA | exit code 消费协议 (0/10/20/30) 未写入 SKILL.md |
| R1-I3 | QA-07 | CLI --output 与 stdout 双写 |
| R1-I4 | QA-08 | uncommitted_count 对 MM 文件双计 |
| R1-I5 | QA-10 | _normalize_status 缺 Active/Deprecated/Archived |
| R1-I6 | QA-11 | collect_audit frontmatter `converged: true` 解析为字符串非 bool |
| R1-I7 | QA-12 | _extract_status Pattern 4 不支持 `## Status:` heading 前缀 (与 SKILL.md Pattern 1 不对齐) |

## 共识 Minor (收敛阶段可延后)

| ID | Agents | Issue |
|---|---|---|
| R1-M1 | BA / CR | tasks.md T3 需显式列出 TL-1/TL-2/CR-I1-I4 遗留条目 |
| R1-M2 | QA | _UPM_CANDIDATES 固定 3 路径, Kairos 覆盖不足 |
| R1-M3 | QA | .mjs/.cjs 不在 _CODE_EXTS |

## Drift Guard 判定

- **Phase 1.13 缺席**: 3/4 agent 判 "partial alignment", 1/4 (CR) 判 "full" (只看代码质量). 多数 "partial" 与 anchor 偏离但属**planned-deferral** (Spec 多 session 交付, 非 uncontrolled drift).
- **Sister-bug 打包**: 4/4 agent 判 "collateral-improvement" (合理的 in-file 修正, 按 feedback_sister_bug_bundling 模式). 但 TL 指出需在 Revisions 章节 document 为 intentional divergence.

## R1 决议

**不合并** (3/4 continue_draft). **进入 R2 前应用的 revision**:

Tier 1 (session-actionable):
- R1-C5/C6: 补 Revisions 章节记录 sister-bug 是 intentional divergence, 创建 schema.md 最小 stub 解决死链
- R1-I3: scan.py --output 互斥 stdout
- R1-I4: uncommitted_count 去重
- R1-I5: _normalize_status 加 Active/Deprecated/Archived
- R1-I6: collect_audit frontmatter bool 解析
- R1-I7: _extract_status heading 前缀支持
- R1-M1: tasks.md T0.2-T0.4 checkbox 同步 + T3 显式列 deferred IDs

Tier 2 (session infeasible, handoff):
- R1-C1/C3: SKILL.md Step 0 + Phase 1.13 需 T3 + T5 (~14h)
- R1-C2/C4: T6 测试 (~8h) + T10 benchmark (~2h)
- R1-I1/I2: T4.1 schema.md full spec + consumer contract (~3h)

R2 将审计 R1 Tier 1 revisions + Drift Guard 再次检查。
