# Tasks — Aria Issue Triage SOP

> Parent: [proposal.md](./proposal.md) | **Status**: Phase A.2 draft, ready for post_spec audit

## Phase B Tasks (按依赖顺序)

### T1 — `triage.py` collector (~3h)

**目标**: stdlib-only Python script, 接收 issue 引用 → 输出 `triage-report.json` (步骤 1-5 机械执行)

- [ ] T1.1 创建 `aria/skills/issue-triage/scripts/triage.py` 入口
  - 接收参数: `--issue <owner>/<repo>#N` 或 `--issue-url <url>` 或 `--issue N` (默认本仓库)
  - `--output` 路径默认 `.aria/triage-report.json`
- [ ] T1.2 步骤 1 (Read issue) collector — `collectors/_issue.py`,调 `forgejo` CLI fetch issue + comments + labels
- [ ] T1.3 步骤 2 (Version check) collector — `collectors/_version.py`,读 `aria/.claude-plugin/plugin.json` + grep issue body 报告版本
- [ ] T1.4 步骤 3 (Code path) collector — `collectors/_code.py`,正则抽 `path:line` 引用 + 验证存在
- [ ] T1.5 步骤 4 (Git log) collector — `collectors/_history.py`,`git log -n 20 --oneline -- <file>` 对每个 cited file
- [ ] T1.6 步骤 5 (In-flight) collector — `collectors/_inflight.py`,API 检索 open PR + branch keyword match
- [ ] T1.7 Triage report JSON schema 定义 — `references/triage-report-schema.md` (类比 state-snapshot-schema.md)
- [ ] T1.8 Exit code 契约 — 0/10/20/30 同 scan.py 模式
- [ ] T1.9 Unit test: fixture issue body + git fixture repo

### T2 — `SKILL.md` 定义 (~1h)

- [ ] T2.1 `aria/skills/issue-triage/SKILL.md` 写入,结构类比 `state-scanner/SKILL.md`:
  - 快速开始 / 核心功能 / 配置 / 执行流程 (Step 0 跑 triage.py, 阶段 1-2-3-4 同 state-scanner)
  - 步骤 6 (复现) 由 AI 跑,因 AI-assisted 不机械化
  - 输出 `triage_comment.md` 草稿模板
- [ ] T2.2 跨平台命令规范段落 (沿用 state-scanner 模板)
- [ ] T2.3 错误处理表 (issue 不存在 / API 失败 / git fixture 不全 / 复现超时)

### T3 — `standards/conventions/issue-triage.md` (~1h)

- [ ] T3.1 标准文档定义 6 步 SOP + verdict 枚举 + 输出格式
- [ ] T3.2 引用本次 #101 作为 case study
- [ ] T3.3 标准库 README 更新 (links list)

### T4 — Unit test (~2h)

- [ ] T4.1 Mock Forgejo API responses (fixture JSON in `tests/fixtures/`)
- [ ] T4.2 Git fixture repo (`tests/fixtures/triage-repo.tar.gz`,含 cited file + 2 commit history)
- [ ] T4.3 4 用例: confirmed / not-reproducible / fixed-in-X / needs-info
- [ ] T4.4 Edge: API timeout / issue body 无 file 引用 / cited file 不存在

### T5 — Dogfooding 验证 (~1h)

- [ ] T5.1 `/issue-triage 101` 实跑,输出 `triage-report.json`
- [ ] T5.2 与本次手工 triage (issuecomment-5972) 字段 diff
- [ ] T5.3 Acceptance: 6 步 verdict 全部一致 + 复现命中率 (2/4 主因 + 2/4 次生) 准确
- [ ] T5.4 在 #101 加 dogfooding comment 贴 AI 输出,人工 vs AI diff 留存

### T6 — CLAUDE.md Rule #9 决策 (post_spec audit 前 open)

- [ ] T6.1 audit 阶段决定: Advisory (warning) vs Strict (报错) vs 完全靠 SOP 自觉
- [ ] T6.2 如加 Rule #9,文档化触发场景 + exception 模板 (类比 Rule #7 / #8 结构)

### T7 — Phase C ship

- [ ] T7.1 Phase B 完成后,branch-manager 起 PR
- [ ] T7.2 phase-c-integrator pre-merge gate (Rule #8) 通过
- [ ] T7.3 PR merge + 关联 close #101 (issue triage SOP 与 #101 修复 cycle 独立, 仅 reference)
- [ ] T7.4 Phase D — 进度更新 + Spec archive

---

## 依赖图

```
T1 ─┬─ T2 (SKILL.md 依赖 collector 输出 schema)
    └─ T4 (unit test 验证 collector)
T2 ── T3 (convention doc 引用 Skill)
T1+T2+T3 ── T5 (dogfooding 跑完整流程)
T5 ── T6 (基于 dogfooding 体验决定 Rule #9 强制度)
T6 ── T7 (ship)
```

---

## Effort baseline

| Phase | Tasks | Effort |
|---|---|---|
| Phase B core | T1 + T2 + T3 | ~5h |
| Phase B test | T4 | ~2h |
| Phase B dogfood | T5 | ~1h |
| Phase B decision | T6 | ~0.5h (post_spec audit 解决) |
| Phase C ship | T7 | ~1h |
| **Total** | | **~9.5h** |

Level 2 minimal scope 上限 1-3 day,实际 ~1.2 day,size 合理。

---

## Out of Scope (本 cycle 不做)

- 自动化 issue triage (Forgejo webhook → aria-runner-bot) — M2+
- Issue 自动 labeling (基于 triage verdict) — M2+
- 跨平台 issue 抓取 (GitHub / GitLab 适配) — 仅 Forgejo
- Triage report 的 audit log immutable 存储 — 引用 US-025 M5 通用 audit-log 即可
- 真实修复 #101 的 `_normalize_status` bug — **独立 cycle** `aria-issue-101-status-normalize`,本 SOP 仅定义流程,不做 bug 修复
