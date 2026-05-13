# Aria Issue Triage SOP — 6-step standard process

> **Level**: 2 (Minimal — 单 Skill 新增 + convention doc + 标准化已有手工流程)
> **Status**: Draft (Phase A.1)
> **Change ID**: `aria-issue-triage-sop`
> **Trigger context**: 2026-05-13 处理 Forgejo [#101](https://forgejo.10cg.pub/10CG/Aria/issues/101) 时识别 — issue triage 流程缺位,容易跳到方案推荐而忽略版本/代码/in-flight 核对,质量风险高
> **Created**: 2026-05-13

---

## Why

收到 issue (bug report / feature request / discussion) 时,**直接进推荐解决方案是反模式** — 容易错过:

1. 报告版本可能已过期,issue 在新版本已修
2. 引用的 file:line 可能不存在 / 已重构,描述与实际代码漂移
3. 已有 in-flight branch / PR 修复,新起 cycle = 重复劳动
4. 复现可能与描述不一致 (如本次 #101: 自报 4/4,实测 2/4 命中主因 + 2/4 命中次生 bug)

需要把"先核对再推荐"沉淀为**可执行的标准流程**,避免每次都靠当下记得。

参考实践: GitHub issue triage labels (`needs-info` / `confirmed` / `not-reproducible` / `duplicate`) + Linux kernel triage SOP (reproduce-before-recommend)。

---

## What

### Key Deliverables

- **`aria/skills/issue-triage/SKILL.md`** — 可调用 Skill,接收 issue URL 或编号,机械执行 6 步核对
- **`standards/conventions/issue-triage.md`** — 流程规范文档(类似 `git-commit.md` / `secret-hygiene.md`),定义 6 步 + 输出 verdict 字典
- **`aria/skills/issue-triage/scripts/triage.py`** — stdlib-only Python collector,产出 JSON triage report (类比 state-scanner 的 scan.py 机械化模式)
- **CLAUDE.md** Rule #9 (可选,如果用户认同要硬约束) — "Issue 响应前必须跑 triage SOP"

### Skill 输入 / 输出

```yaml
inputs:
  issue:        # Forgejo URL 或 owner/repo#N 或裸编号(本仓库默认)
  cited_files:  # optional, 自动从 issue body 抽取 file:line 引用

outputs:
  triage_report.json:        # 机械产出, 6 步逐项结果 + verdict
  triage_comment.md:          # AI 合成, 准备 POST 到 issue 的 comment 草稿
  next_actions:               # checklist: [ ] proposal / [ ] branch / [ ] close-as-X
```

### 6-step 流程定义

| Step | 子任务 | 机械化? | 输出字段 |
|---|---|---|---|
| 1 | Read issue body + comments + labels | API fetch | `issue.title`, `issue.body`, `issue.labels`, `issue.comments[]` |
| 2 | Version check (reported vs current) | grep plugin.json / VERSION + diff | `version.reported`, `version.current`, `version.gap` |
| 3 | Code path verification — 引用文件存在 + line 范围内代码与 issue 描述一致 | path exists + read line range | `code.cited_paths[]`, `code.matches_description: bool` |
| 4 | Git log on cited files (过去 N=20 commit) | `git log` 抽 commit message | `git_history.recent_commits[]`, `git_history.likely_fix_present: bool` |
| 5 | In-flight branch / PR check | API 检索 + keyword match | `inflight.branches[]`, `inflight.prs[]`, `inflight.has_match: bool` |
| 6 | Reproduction — 跑 issue 提供的 repro / 自构造 minimal repro | AI-assisted (无法纯机械) | `repro.cases[]: {input, expected, actual, verdict}`, `repro.hit_rate: N/M` |

**最终 verdict** (枚举):
- `confirmed` — 复现成功 + bug 真实
- `not-reproducible` — 跑不出报告的症状
- `fixed-in-X` — 在 commit/版本 X 已修
- `duplicate-of-#N` — 另一 issue 已覆盖
- `needs-info` — 报告信息不足,等用户补充
- `wont-fix` — 确认是 by-design / out-of-scope

---

## Impact

| Type | Description |
|---|---|
| **Positive** | 每个 issue 留 audit trail (comment) + verdict;减少"基于不准确报告写错误方案"风险;新人也能 triage |
| **Positive** | Triage 流程机械化 70% (步骤 1-5) → AI 只需做步骤 6 + 综合判断,大幅减少遗漏 |
| **Risk** | 增加每个 issue 的处理前置时间 (~5min);缓解: 步骤 1-5 自动化 + 简单 issue (typo / docs-only) 允许跳步 |
| **Risk** | Triage Skill 自身可能 bug (如 state-scanner #101 的元 bug);缓解: triage report 是 JSON + AI 二次校验,而非直接行动 |

---

## Tasks

(详见 [tasks.md](./tasks.md))

精简版:

- [ ] T1 — `triage.py` collector (步骤 1-5 机械执行,输出 JSON)
- [ ] T2 — `SKILL.md` 定义 Skill 调用契约 + 6 步流程文档化
- [ ] T3 — `standards/conventions/issue-triage.md` SOP 文档
- [ ] T4 — Unit test (mock Forgejo API + git fixture)
- [ ] T5 — 用 #101 dogfooding 验证 (跑 Skill, 输出 vs 手工 triage 对比)
- [ ] T6 — CLAUDE.md Rule #9 决策(加 / 不加)
- [ ] T7 — Phase C pre-merge gate + ship

---

## Success Criteria

- [ ] `/issue-triage 101` 在 SilkNode/Aria 上能跑通,输出 `triage_report.json` 含 6 步全部字段
- [ ] AI 合成的 `triage_comment.md` 与本次手工 triage comment 至少 80% 一致 (人工 diff 评估)
- [ ] 跑 `/issue-triage` 不需要 user interaction (除步骤 6 复现可能需要确认)
- [ ] 新 issue 上线后,maintainer 第一动作能从"看一眼就推荐" → "/issue-triage 先核对",通过 1 个月 dogfooding 验证

---

## Open Questions (Phase A.2 audit 解决)

1. **Skill vs Command?** Issue triage 是否应该是 slash command (`/issue-triage`) 还是 Skill 调用? Aria 现有 Skill 多以 `/<skill>` 触发,统一即可
2. **CLAUDE.md Rule #9 强制度?** Strict (违反报错) / Advisory (warning) / 完全靠 SOP 自觉?建议 Advisory 起步
3. **跨仓库 issue 支持?** 默认仅 Aria 自身,还是 day-1 支持 `10CG/silknode` / `10CG/aria-plugin` 等?建议 day-1 支持任何 Forgejo repo (forgejo CLI 已通用)
4. **Triage 触发时机?** 仅 maintainer 显式调用,还是新 issue 自动触发 (Forgejo webhook → aria-runner-bot)?M1 仅手动,自动化推后续

---

## References

- 触发 issue: [Forgejo #101](https://forgejo.10cg.pub/10CG/Aria/issues/101) `state-scanner v3.0 _normalize_status 子串匹配 done 假阳性`
- 类似规范: `standards/conventions/git-commit.md` / `secret-hygiene.md`
- Mechanical pattern: `aria/skills/state-scanner/scripts/scan.py` (collector + JSON output)
