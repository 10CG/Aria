# 决策: DEC-20260530-002 — emergency hotfix lane + audit file-scope filter

> **日期**: 2026-05-30 | **模式**: brainstorm (lightweight — issue prescriptive)
> **Source**: Forgejo Aria [#58](https://forgejo.10cg.pub/10CG/Aria/issues/58) (3-in-1, filed v1.16.0)
> **Spec**: `openspec/changes/emergency-hotfix-and-audit-file-scope/proposal.md`

## 背景

#58 来自 SilkNode 2026-04-28 prod cron 5-day silent failure hotfix (PR #268)。3 个规范 gap。**关键 triage 发现 (v1.16.0 → v1.34.0, 18 minor drift)**: sub-item #3 (推荐 adaptive_rules L1 off/L2 convergence/L3 challenge) **已是 v1.34.0 默认** (DEFAULTS.json), 且 audit checkpoints 默认全 off —— over-audit 痛点现默认已规避。故 #58 缩水到 2 个真 gap。

## triage 逐项判定

| sub-item | 状态 | 处置 |
|----------|------|------|
| #3 challenge over-audit / adaptive_rules 推荐 | ✅ 已是 v1.34.0 默认 (adaptive_rules + checkpoints off) | **关闭** (`adaptive_force_challenge_levels` 大体冗余) |
| #2 file-scope 二次过滤 | 🔶 真 gap (scope_skip_paths ABSENT); 价值限 audit-on 项目 | **做** (DEC-4) |
| #1 emergency hotfix lane | 🔶 真 gap (无 hotfix lane, quick_fix 不覆盖 prod-emergency 语义); 价值最高 | **做** (DEC-2/3) |

## 最终决策

| # | 决策 | 选择 | 理由 |
|---|------|------|------|
| DEC-1 | scope | **#1 + #2** (#3 关闭, 已默认) | triage: #3 已是默认, version drift 18 minor |
| DEC-2 | hotfix lane 强度 | **advisory** (state-scanner `emergency_hotfix` 推荐规则 + phase-a-planner 文档化 lighter lane) | 符合 Aria "规则推荐不强制" 模式; 不硬跳 A.1-A.3 |
| DEC-3 | prod-validated 验证 | **commit trailer** `Prod-Validated: <evidence>` + root-cause block; **phase-b 机检存在性 gate** (Rev1) | 满足 issue 证据强制要求; 机械可 grep; Rev1: phase-b-developer 跳单测时 grep trailer 存在性 (无→block), 内容真实性靠 owner review (诚实 soft-gate) |
| DEC-4 | file-scope ops/docs-only audit 动作 | **降级到 convergence** (非 skip) | issue 自身事故是 deploy script (challenge 找到真退化) → deploy 改动不能全 skip; 降级保留安全网又省 ceremony (~5min vs 15-30min) |
| DEC-5 (默认) | scope_skip_paths | 默认 `[deploy/, docs/, .forgejo/workflows/, .github/workflows/]` + `*.md`; config 可覆盖 | issue 给的清单; 可配 |
| DEC-6 (默认) | file-scope 求值方式 | **prose-driven** (audit-engine SKILL.md: adaptive/checkpoint 解析**后** `min(resolved_mode, convergence)`; **audit-engine 自取** `git diff --name-only $(git merge-base HEAD <base>)`, base 可配, 不依赖 snapshot/changes 字段); 0 文件 pass-through; 机械 scan.py 字段 = optional follow-up | Rev1: `changes` collector 无文件路径 + audit-engine 不读 snapshot → 必须自取 git diff; Rev2: 用 merge-base diff (非 `HEAD`) 防 pre_merge 漏已提交变更; 解析后 cap; 0 文件防 vacuous-true |

## hotfix lane 行为 (DEC-2/3 细化)

emergency_hotfix 触发 (Rev1): **`hotfix/*` 分支为主触发** (`git.current_branch`); commit `hotfix(...)` prefix 仅 corroborating (best-effort)。state-scanner 出 `emergency_hotfix` 推荐 (confidence 85% / auto_execute No), lighter lane:
- 跳 Phase A.1-A.3 (commit body + Prod-Validated trailer 取代独立 spec)
- B.3 单测可被 **manual prod validation 替代** —— **仅当** commit 含 `Prod-Validated: <evidence>` trailer + 根因块 (无 trailer → 不允许替代, 回标准 lane)
- 仍走 Phase C/D (commit/PR/merge/UPM)
- pre_merge audit (若 enabled) 降级到 convergence (不 challenge)

## 考虑过但否决

| 方案 | 否决理由 |
|------|----------|
| #1 硬机械 skip gate | 与 Aria advisory 模式不一致; 紧急场景仍应 AI 判断 |
| #1 prod-validated advisory 口头 | 丢 audit trail, 与 issue 证据强制要求矛盾 |
| #2 ops/docs 完全 skip | issue 实证 deploy script 改动会退化, skip 风险高 |
| #3 全做 (adaptive_force_challenge_levels + 文档) | 大体重复 v1.34.0 默认, 性价比低 |

## v1 deliverables

1. state-scanner: 新 `emergency_hotfix` 推荐规则 (references/rules/) + RECOMMENDATION_RULES 索引
2. phase-a-planner: 文档化 emergency hotfix lighter lane (skip A.1-A.3 条件 + Prod-Validated trailer + 根因块要求)
3. audit-engine: file-scope 二次过滤 (SKILL.md: scope_skip_paths 全覆盖 → cap convergence)
4. config-loader: `audit.scope_skip_paths` namespace (默认清单) + `git-commit` convention 加 `Prod-Validated:` trailer
5. standards/conventions: emergency-hotfix lane 约定 (git-commit.md 或新 doc) + Prod-Validated trailer schema
6. Rule #6: deterministic structural substitute (rule fixture / 文档一致性), 非 LLM AB

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| hotfix lane 成 "跳测试" 漏洞 | Prod-Validated trailer + 根因块强制 (无 → 不允许替代单测); audit trail 留痕 |
| file-scope 误判 (混合 ops+业务) | "全部" 变更文件 ∈ skip_paths 才降级; 任一业务文件 → 标准 audit |
| advisory 规则被忽略 | 推荐规则 surface 给 AI; phase-a-planner 文档化; 不强制但留 prose SOT |

## 后续 (defer)

- 机械 scan.py `changes.scope_skip_match` 字段 (DEC-6 optional)
- `adaptive_force_challenge_levels` (sub-item #3 残留, 大体冗余)
- PR body 验证块 (DEC-3 选 commit trailer 而非 PR body)
