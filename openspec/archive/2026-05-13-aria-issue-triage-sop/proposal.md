# Aria Issue Triage SOP — 6-step standard process

> **Level**: 2 (Minimal — 单 Skill 新增 + convention doc + 标准化已有手工流程)
> **Status**: **Complete** (Phase A+B+C+D shipped 2026-05-13; merged via PR Aria#102 + aria-plugin#43 + aria-standards#3; ready for archive)
> **Change ID**: `aria-issue-triage-sop` (`-sop` 后缀仅区分本次变更范围;Skill 目录名为 `issue-triage`)
> **Trigger context**: 2026-05-13 处理 Forgejo [#101](https://forgejo.10cg.pub/10CG/Aria/issues/101) 时识别 — issue triage 流程缺位,容易跳到方案推荐而忽略版本/代码/in-flight 核对
> **Triage canonical example**: [issuecomment-5972](https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-5972)
> **Created**: 2026-05-13

---

## Why

收到 issue (bug report / feature request / discussion) 时,**直接进推荐解决方案是反模式** — 容易错过:

1. 报告版本可能已过期,issue 在新版本已修
2. 引用的 file:line 可能不存在 / 已重构,描述与实际代码漂移
3. 已有 in-flight branch / PR / 本地 worktree 修复,新起 cycle = 重复劳动
4. 复现可能与描述不一致 (本次 #101: 自报 4/4,实测 2/4 命中主因 + 2/4 命中次生 bug → 新 verdict `partial-repro` 之诞生)

需要把"先核对再推荐"沉淀为**可执行的标准流程**,避免每次都靠当下记得。

参考实践: GitHub issue triage labels (`needs-info` / `confirmed` / `not-reproducible` / `duplicate`) + Linux kernel triage SOP (reproduce-before-recommend)。

---

## What

### Truth-source declaration (R1 KM-M1 fix)

为防 SKILL.md 与 convention doc 内容漂移,本 cycle 显式约定:

- **`standards/conventions/issue-triage.md`** = 6 步流程定义 + verdict 字典 + exception 模板的**唯一真理来源 (SOT)**,与 `secret-hygiene.md` / `git-commit.md` 同模式
- `aria/skills/issue-triage/SKILL.md` = 引用 SOT (`See: standards/conventions/issue-triage.md §Steps`),仅描述 Skill 调用契约 + 输入/输出 schema + Aria 内集成点,**不复制**步骤定义
- `CLAUDE.md` 后续如加 Rule #9 (本 cycle **不加**, 见 Open Questions 决策) 仅含要点摘要 + 指向 SOT 链接

### Key Deliverables

| Deliverable | 路径 | 角色 |
|---|---|---|
| Skill 调用入口 | `aria/skills/issue-triage/SKILL.md` | Aria Plugin 内 `/issue-triage` 触发 |
| 机械 collector | `aria/skills/issue-triage/scripts/triage.py` (stdlib-only) | 步骤 1-5 机械执行,产 JSON |
| Schema reference | `aria/skills/issue-triage/references/triage-report-schema.md` | JSON 输出契约 source-of-truth |
| Convention SOT | `standards/conventions/issue-triage.md` | 6 步 + verdict + exception SOT |
| Decision memo | `docs/decisions/2026-05-13-rule-9-deferral.md` (T6 输出) | Rule #9 强制度决策延后说明,**不入 CLAUDE.md** |

**显式排除** (R1 KM-m5): SOP 是操作流程,归 `standards/conventions/`;不入 `standards/methodology/` (后者存放哲学性文档如 `aria-brand-guide.md`)。

### Skill 输入 / 输出

```yaml
inputs:
  issue:           # Forgejo URL / "<owner>/<repo>#N" / 裸编号 (本仓库默认)
  cited_files:     # optional, 自动从 issue body 抽取 (T1.4 列 3 种 citation format)

outputs:
  triage-report.json:    # 机械产出 (步骤 1-5 + sanity check)
  triage-comment.md:     # AI 合成 comment 草稿, 准备 POST 到 issue
  next_actions:          # checklist: [ ] proposal / [ ] branch / [ ] close-as-X
```

### 6-step 流程定义

| Step | 子任务 | 机械化? | Snapshot 字段 |
|---|---|---|---|
| 1 | Read issue body + comments + labels | forgejo API | `issue.title`, `issue.body`, `issue.labels[]`, `issue.comments[]` |
| 2 | Version check (reported vs current) — **fail-soft chain** | grep + diff | `version.reported`, `version.current` (`unknown` 允许), `version.gap` |
| 3 | Code path verification — 引用文件存在 + line 范围与描述一致 | path + line read | `code.cited_paths[]`, `code.matches_description: bool` |
| 4 | Git log on cited files (recent N=20 commit, 关键词匹配) | `git log` | `git_history.likely_fix_candidates: [{sha, message, match_reason}]` (空 array 即 false) |
| 5 | In-flight check — **三段独立** | API + git | `inflight.remote_prs[]`, `inflight.local_branches[]`, `inflight.worktrees[]` |
| 6 | Reproduction — **三模式 exit** | AI-assisted | `repro.cases[]`, `repro.exit_mode: auto/pause/skip`, `repro.hit_rate: N/M` |

#### Step 2 跨仓库 fail-soft (R1 KM-C1 fix)

按顺序尝试,首个命中即用,全失败则 `version.current: "unknown"` (`gap: null`):

```
1. {project_root}/aria/.claude-plugin/plugin.json       (Aria meta-repo)
2. {project_root}/.claude-plugin/plugin.json            (Aria plugin 独立仓库)
3. {project_root}/VERSION                                (SilkNode + 通用)
4. {project_root}/package.json                          (JS 项目)
5. {project_root}/pyproject.toml                        (Python 项目)
```

#### Step 5 In-flight 三段 (R1 TL-M2 fix)

- `remote_prs[]`: forgejo API `/repos/<owner>/<repo>/pulls?state=open` + keyword 匹配 (issue#, normalize, status 等)
- `local_branches[]`: `git branch -a --list "*<keyword>*"` 全本地分支扫描
- `worktrees[]`: `git worktree list --porcelain` 解析每个 worktree 的 branch + path

#### Step 6 三模式 exit (R1 TL-M3 fix)

| exit_mode | 触发场景 | verdict 路径 |
|---|---|---|
| `auto` | AI 独立完成 repro,所有 `cases[]` 填 match=true/false | 进 Step 7 verdict 计算 |
| `pause` | 需要用户提供 env/data/交互 | Skill 暂停,提示用户补 repro,resume 时继续 |
| `skip` | 无法复现 (缺资源 / 环境 / 凭证) | verdict 强制 = `needs-info` |

每个 case **必须**填结构化 schema (即使 verdict=not-reproducible 也需 ≥1 case 记录缺失原因):

```json
{
  "case_id": "string",
  "input": "...",
  "expected_behavior": "...",
  "actual_behavior": "...",
  "match": true | false | null,
  "notes": "..."
}
```

### Verdict 字典 (R1 QA-C1 fix — 加 partial-repro)

| Verdict | 定义 |
|---|---|
| `confirmed` | 复现成功 + bug 真实 + 与 issue 描述一致 |
| `partial-repro` | **新增** — repro 显示真实 defect, 但症状/hit-rate 与 issue 描述实质偏离 (#101 即此情况);携带 `deviation_note` 字段 |
| `not-reproducible` | 跑不出报告的症状 |
| `fixed-in-X` | 在 commit/版本 X 已修 (Step 4 命中) |
| `duplicate-of-#N` | 另一 issue 已覆盖 |
| `needs-info` | 报告信息不足 / Step 6 skip 模式 |
| `wont-fix` | 确认是 by-design / out-of-scope |

### 正交字段 (R1 TL-M4 fix — verdict 与优先级解耦)

triage-report.json 在 verdict 外**额外**输出:

```json
{
  "severity": "critical | major | minor | trivial",
  "recommended_action": "hotfix | next-cycle | backlog | close",
  "deviation_note": "..." // 仅 partial-repro verdict 必填
}
```

severity 由 AI 在 Step 6 后填,基于影响面 (commit blast radius / hit_rate / data corruption 风险等);不机械化。

### Sanity check (R1 QA-m5 fix)

`triage.py` 在生成 JSON 前 pre-flight: 若 `steps_with_data < 2` (步骤 1-5 至少 2 个有数据) → exit code 30 + message "Insufficient data — check credentials and issue ref"。阻止 AI 在 null 输入上编造 Step 6。

---

## Impact

| Type | Description |
|---|---|
| **Positive** | 每个 issue 留 audit trail (comment) + verdict;减少"基于不准确报告写错误方案"风险;新人 + cross-project 也能 triage |
| **Positive** | Triage 流程机械化 70% (步骤 1-5) → AI 仅做步骤 6 + verdict 综合,大幅减少遗漏;`partial-repro` verdict 强制结构化报告偏差 |
| **Risk** | 增加每个 issue 处理前置时间 (~5min);缓解: 简单 issue (typo/docs-only) 允许跳步,且大部分流程并行 |
| **Risk** | Triage Skill 自身可能 bug;缓解: JSON schema_version + jsonschema 强制 + sanity check (steps_with_data<2 → exit 30) + Rule #6 skill-creator benchmark gating |
| **Risk** | Forgejo API 调用涉及 token,违反 Rule #7 secret-hygiene 风险;缓解: 所有 forgejo CLI 调用 `subprocess.run(..., capture_output=True)` 显式声明 (见 tasks T1.2/T1.6) |

---

## Tasks

详见 [tasks.md](./tasks.md)。简版:

- [ ] T1 — `triage.py` collector (6 sub-collectors + JSON schema + exit codes + sanity check)
- [ ] T2 — `SKILL.md` 定义 Skill 调用契约,引用 SOT
- [ ] T3 — `standards/conventions/issue-triage.md` SOT 文档 (6 步 + verdict 字典 + case study)
- [ ] T4 — Unit test (mock Forgejo API + programmatic git fixture + CI 集成)
- [ ] T5 — Dogfooding 用 #101 验证, hard-gate + soft-% rubric acceptance
- [ ] T6 — Rule #9 决策 memo (本 cycle **不**入 CLAUDE.md)
- [ ] T7 — Phase C ship (pre-merge gate Rule #8)
- [ ] T8 — **Rule #6 skill-creator AB benchmark** (新 Skill 不可协商)

---

## Success Criteria (R1 QA-C2 fix — hard-gate + soft-% rubric)

**Hard gates** (任一失败即 fail,不计入 soft %):

- [ ] `triage-report.json` schema 验证通过 (jsonschema, 含 schema_version 字段)
- [ ] Step 1-5 必填字段全部存在 (空字符串或 0 也算"存在",null 不算)
- [ ] `version.*` / `code.cited_paths[]` / `git_history.likely_fix_candidates[]` 与人工 triage 完全一致 (确定性字段不允许偏差)

**Soft fields** (累计 ≥85% 视为通过):

- [ ] `inflight.*` 三段 union 命中率 ≥ 人工 triage 命中的 80%
- [ ] `repro.cases[]` verdict + cited 主因 file 与人工 triage 一致, hit_rate 数值差异 ≤ 1 case
- [ ] AI 合成的 `triage-comment.md` 与本次 issuecomment-5972 关键结论 (verdict + Critical findings list) 一致

**其他**:

- [ ] `/issue-triage 101` 不需要 user interaction (除 Step 6 三模式)
- [ ] 新 issue 上线后, dogfood 1 个月 (≥3 issue 跑通) 后再评估 Rule #9 升级

---

## Open Questions (decisions, R1 unanimous)

| Q | Decision | Rationale |
|---|----------|-----------|
| Q1 Skill vs Command | **CLOSED — Skill (SKILL.md + scripts/), 通过 `/issue-triage` 触发** | Aria 36 既有 Skill 同模式,与 state-scanner 同构;非真二选一 |
| Q2 Rule #9 强制度 | **CLOSED — 本 cycle 不加 Rule;仅出 decision memo** | Rule #7/8 均 incident 驱动入册 (#78 secret leak / #60 PR-321 cancel);本 SOP 缺该证据链,延后到 ≥3 dogfood + 1 missed-triage incident 后再评估 |
| Q3 跨仓库 issue 支持 | **CLOSED — Day-1 支持任何 Forgejo repo** | forgejo CLI 已通用;仅 Step 2 需 fail-soft (见上) |
| Q4 触发时机 | **CLOSED — M1 仅手动** | webhook 需 aria-runner-bot 基础设施 + 误触发回滚机制,与 SOP 正交,推后续 cycle |

(R1 audit 后所有 open question 已 close, 不留 A.2 audit 负担)

---

## References

- **Trigger issue**: [Forgejo Aria #101](https://forgejo.10cg.pub/10CG/Aria/issues/101) — state-scanner `_normalize_status` 子串匹配 done 假阳性
- **Canonical case study**: [issuecomment-5972](https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-5972) — 手工 triage 完整推理过程
- **Convention precedent**: `standards/conventions/git-commit.md`, `standards/conventions/secret-hygiene.md` (Rule #7 SOT 模式)
- **Skill precedent**: `aria/skills/state-scanner/SKILL.md` + `scripts/scan.py` (机械化 collector pattern)
- **Boundary**: 与 `aria-report` (用户→Aria inbound) 反向;`issue-triage` 是 Aria→issue triage outbound (T2.1 SKILL.md 必含 "与 aria-report 的关系" 段)
- **Compliance**: Rule #6 (skill-creator benchmark, T8 必跑) + Rule #7 (secret-hygiene, forgejo subprocess capture_output=True)
- **Boilerplate Spec (Level 3 precedent)**: `openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/` (2026-05-12 SCOPE_OK_R2,Phase Decomposition + AD slot 模式参考)

---

## Audit footprint

- **R1 report**: `.aria/audit-reports/post_spec-R1-2026-05-13T0030Z-aria-issue-triage-sop.md`
- **R1 verdict**: PASS_WITH_WARNINGS (3/3 unanimous, 4 Critical + 12 Major + 13 Minor)
- **R2 report**: `.aria/audit-reports/post_spec-R2-2026-05-13T0130Z-aria-issue-triage-sop.md`
- **R2 verdict**: SCOPE_OK_R2 (tech-lead PASS + KM PASS_WITH_WARNINGS + QA PASS_WITH_WARNINGS, **29/29 R1 CLOSED**, 0 new Critical, 3 R2-NEW Major inline 已修)
- **Convergence**: pragmatic (per feedback memory `feedback_post_spec_audit_pragmatic_convergence.md`) — unanimous PASS spectrum + verdict 改善 + 无振荡 + 0 new Critical
