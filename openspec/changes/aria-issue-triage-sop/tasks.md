# Tasks — Aria Issue Triage SOP

> Parent: [proposal.md](./proposal.md) | **Status**: Phase A.2 (R1 fixes applied 2026-05-13, ready for R2 audit)
> **Truth-source**: convention doc (`standards/conventions/issue-triage.md`); SKILL.md 引用而非复制

## Phase B Tasks (按依赖顺序)

### T1 — `triage.py` collector (~3.5h)

**目标**: stdlib-only Python script, 接收 issue 引用 → 输出 `triage-report.json` (步骤 1-5 机械执行 + sanity check)

- [ ] **T1.1** 入口 `aria/skills/issue-triage/scripts/triage.py`
  - 参数: `--issue <owner>/<repo>#N` / `--issue-url <url>` / `--issue N` (本仓库默认)
  - `--output` 默认 `.aria/triage-report.json`
  - **Pre-flight sanity check**: 在 Step 6 前若 `steps_with_data < 2` → exit 30 + "Insufficient data — check credentials and issue ref"

- [ ] **T1.2** Step 1 (Read issue) — `collectors/_issue.py`
  - 调 `forgejo` CLI fetch issue + comments + labels
  - **Rule #7 合规**: `subprocess.run(..., capture_output=True)` 显式声明,不打印 stdout/stderr
  - `collection_status: ok | error | skipped` 字段必填

- [ ] **T1.3** Step 2 (Version check) — `collectors/_version.py`
  - **Fail-soft chain** (R1 KM-C1):
    1. `aria/.claude-plugin/plugin.json`
    2. `.claude-plugin/plugin.json`
    3. `VERSION`
    4. `package.json`
    5. `pyproject.toml`
    6. 全失败 → `version.current: "unknown"`, `version.gap: null`
  - grep issue body 抽报告版本 (regex: `version: X.Y.Z` / `Plugin: X.Y.Z`)

- [ ] **T1.4** Step 3 (Code path) — `collectors/_code.py`
  - **支持 3 种 citation format** (R1 QA-m4):
    1. backtick inline: `` `path/to/file.py:42` ``
    2. prose: `path/to/file.py line 42` / `path/to/file.py L42`
    3. markdown link: `[file.py](url)` (URL 含 `path:` 锚点的也算)
  - 验证 path 存在 + line 范围内代码片段抓取 (用于后续 AI verify)
  - 每种 format 至少 1 unit test case (T4)

- [ ] **T1.5** Step 4 (Git log) — `collectors/_history.py`
  - `git log -n 20 --oneline -- <file>` per cited file
  - **改 schema** (R1 QA-m2): `likely_fix_candidates: [{sha, message, match_reason}]`,空 array 即 false (boolean derive at read time)
  - 关键词 match: `fix` / `resolve` / `close #<issue>` / `normalize` 等

- [ ] **T1.6** Step 5 (In-flight) — `collectors/_inflight.py`
  - **三段独立** (R1 TL-M2):
    - `remote_prs[]`: `forgejo GET /repos/<owner>/<repo>/pulls?state=open` + keyword match (issue#, file 名, normalize 等)
    - `local_branches[]`: `git branch -a --list "*<keyword>*"` 全扫
    - `worktrees[]`: `git worktree list --porcelain` 解析 branch + path
  - **Rule #7 合规**: 同 T1.2

- [ ] **T1.7** Triage report JSON schema — `references/triage-report-schema.md`
  - **Required fields** (R1 QA-M1):
    ```yaml
    schema_version: string (semver, current "1.0")
    triage_tool_version: string (from plugin.json)
    issue_ref: string ("<owner>/<repo>#N")
    generated_at: string (ISO-8601)
    steps:
      step1_issue: {collection_status, title, body, labels, comments[]}
      step2_version: {collection_status, reported, current, gap}
      step3_code: {collection_status, cited_paths[], matches_description}
      step4_history: {collection_status, likely_fix_candidates[]}
      step5_inflight: {collection_status, remote_prs[], local_branches[], worktrees[]}
    repro:
      exit_mode: "auto" | "pause" | "skip"
      cases: [{case_id, input, expected_behavior, actual_behavior, match, notes}]
      hit_rate: "N/M"
    verdict: enum (7 values: confirmed / partial-repro / not-reproducible / fixed-in-X / duplicate-of-#N / needs-info / wont-fix)
    severity: "critical" | "major" | "minor" | "trivial"
    recommended_action: "hotfix" | "next-cycle" | "backlog" | "close"
    deviation_note: string  # 仅 partial-repro verdict 必填
    ```
  - **Conditional required (R2 QA-R2-1)**: jsonschema 必须含 `if/then`: `{if: {properties: {verdict: {const: "partial-repro"}}}, then: {required: ["deviation_note"]}}` — 否则 CI gate 无法机械捕捉 `partial-repro` 漏填 `deviation_note`
  - **`triage_tool_version` 采集 (R2 QA-R2-m3)**: 由 T1.3 collector 顺带读 `aria/.claude-plugin/plugin.json::version` 字段写入 (不新增 collector)
  - **`hit_rate` 双格式 (R2 QA-R2-m1)**: schema 输出 `repro.hit_count: int` + `repro.total_count: int` (机械比较) 与 `repro.hit_rate: "N/M"` (人类展示) 并存
  - jsonschema 文件 `references/triage-report.schema.json`,unit test 强制 validate (含 partial-repro 漏填 deviation_note negative test)

- [ ] **T1.8** Exit code 契约 (**R2 QA-R2-2 fix**: 评估顺序 + 阈值边界明确)
  - `0` — 全部成功 (`steps_with_data == 5`)
  - `10` — 部分 collector 错误 (`steps_with_data >= 2 AND <= 4`, 仍生成 report)
  - `30` — 硬失败 (`steps_with_data < 2`, 不生成 report, **不允许** AI 进 Step 6)
  - **评估顺序**: 先 30 (hard fail), 再 10 (partial), 否则 0;**取消 exit 20 (与 30 重叠不可达,R1 草案漏)**

- [ ] **T1.9** Unit test fixture: mock Forgejo API response JSON + git fixture (见 T4)

### T2 — `SKILL.md` (~1.2h)

- [ ] **T2.1** `aria/skills/issue-triage/SKILL.md`
  - 结构类比 `state-scanner/SKILL.md` (Step 0 跑 triage.py, 阶段 1-2-3-4)
  - **引用 SOT** (R1 KM-M1): "6 步定义见 `standards/conventions/issue-triage.md` §Steps,本文档**不**复制"
  - 必含 "与 aria-report 的关系" 段 (R1 TL-m2): aria-report = inbound user→Aria;issue-triage = outbound Aria→verdict;两者方向相反,不冲突
  - Step 6 **三模式 exit** (auto/pause/skip) 显式标注 + verdict 路径表
  - 输出 `triage-comment.md` 草稿模板 (markdown 节: Version / Code / Git / In-flight / Repro / Verdict)

- [ ] **T2.2** 跨平台命令规范段落 (沿用 state-scanner 模板)

- [ ] **T2.3** 错误处理表 (issue 不存在 / API 失败 / git fixture 不全 / 复现超时 / API rate limit / auth expiry)

### T3 — `standards/conventions/issue-triage.md` SOT (~1.2h)

- [ ] **T3.1** 标准文档定义 6 步 SOP + 7 verdict + severity/recommended_action 字段 + exception 模板
  - 与 `secret-hygiene.md` 同结构: 触发场景 / 正向 pattern / exception 模板
- [ ] **T3.2** §Case Study 节 — 直接链接 [issuecomment-5972](https://forgejo.10cg.pub/10CG/Aria/issues/101#issuecomment-5972) 作 canonical example;说明 `partial-repro` verdict 起源 (#101 自报 4/4 实测 2/4 主+2/4 次)
- [ ] **T3.3** CLAUDE.md 导航表更新 (`standards/conventions/` 行) — 如需

### T4 — Unit test + CI 集成 (~2.5h)

- [ ] **T4.1** Mock Forgejo API responses — `tests/fixtures/forgejo/issue-101.json` 等
- [ ] **T4.2** **Programmatic git fixture** (R1 QA-m1) — `tests/conftest.py` 用 `git init` + 控制 commits 生成,**不**用 binary tar.gz
- [ ] **T4.3** 7 verdict 用例 (含 partial-repro) + 正交字段 (severity / recommended_action) 测试
- [ ] **T4.4** Edge cases:
  - API timeout / rate limit (429) → `collection_status: error`
  - Issue body 无 file 引用 → step3 仍出空 array, 非 null
  - Cited file 不存在 → `matches_description: false`
  - Cited file 在错 commit (line shift) → match 但 line 范围 hash 不一致 → flag warning
  - 3 种 citation format 各 1 case
  - Forgejo CLI 第 3 步失败 → step3 error, step4-5 skipped, exit 10
  - 0/5 steps 有效 → exit 30, 不生成 report
- [ ] **T4.5** **CI 集成** (R1 QA-M3) — 加 `pytest aria/skills/issue-triage/` 到 CI workflow YAML;确认 workflow 文件路径 (扫 `.forgejo/workflows/` 或 `.github/workflows/`)

### T5 — Dogfooding 验证 (~1.2h)

- [ ] **T5.1** `/issue-triage 101` 实跑,输出 `.aria/triage-report.json` + `.aria/triage-comment.md`
- [ ] **T5.2** Acceptance rubric (R1 QA-C2):
  - **Hard gates** (任一失败即 fail):
    - jsonschema validate 通过 (含 schema_version)
    - Step 1-5 必填字段全部存在
    - `version.* / code.cited_paths[] / git_history.likely_fix_candidates[]` 与人工 triage 100% 一致
  - **Soft fields** (累计 ≥85%):
    - `inflight.*` 三段 union 命中 ≥ 人工 80%
    - `repro.cases[]` verdict + 主因 file 一致, hit_rate 差异 ≤ 1 case
    - `triage-comment.md` Critical findings 与 issuecomment-5972 一致
- [ ] **T5.3** 在 #101 加 dogfooding comment 贴 AI 输出, 人工 vs AI diff 留存;若 verdict 不一致 → bug,回 Phase B 修
- [ ] **T5.4** Acceptance 通过后,proposal Status 更新至 `Approved (post_dogfood)` (Phase D 时再 Implemented)

### T6 — Rule #9 决策 memo (~0.5h)

- [ ] **T6.1** 写 `docs/decisions/2026-05-13-rule-9-deferral.md`
  - 记录: 本 cycle 不入 CLAUDE.md Rule #9 的理由 (incident 证据链缺失)
  - 升级条件: ≥3 dogfood issue + 1 missed-triage incident → 重新评估
  - 类似 Rule #7/8 历史路径 (incident 驱动入册)
- [ ] **T6.2** (条件触发) 若 dogfood 期出现 missed-triage incident → 新 cycle `aria-issue-triage-rule9-add`

### T7 — Phase C ship (~1h)

- [ ] **T7.1** branch-manager 起分支 `feature/aria-issue-triage-sop`,Phase B 完成后开 PR
- [ ] **T7.2** phase-c-integrator pre-merge gate (Rule #8) 通过 + **T8 benchmark 结果存在 ab-results/** (Rule #6 不可协商)
- [ ] **T7.3** PR merge + 关联 reference #101 (本 SOP 与 #101 真实修复 cycle `aria-issue-101-status-normalize` 独立, 仅 reference)
- [ ] **T7.4** Phase D — 进度更新 + Spec archive (`openspec/archive/2026-MM-DD-aria-issue-triage-sop/`)

### T8 — **Rule #6 skill-creator AB benchmark (新 Skill 不可协商)** (~1h)

- [ ] **T8.1** `/skill-creator benchmark issue-triage` 执行 with/without AB 对比
- [ ] **T8.2** with_skill 通过率 > without_skill (delta 必须为正值)
- [ ] **T8.3** 结果存入 `aria-plugin-benchmarks/ab-results/<timestamp>-issue-triage/`
- [ ] **T8.4** **T7.2 pre-merge gate 必需条件**: ab-results 存在 + delta > 0 + 人工 review confirmed

---

## 依赖图

```
T1 ─┬─ T2 (SKILL.md 依赖 collector 输出 schema)
    ├─ T3 (convention SOT 文档与 schema 一致)
    └─ T4 (unit test 验证 collector + CI 集成)
T2 ── T3 (SKILL.md 引用 SOT)
T1+T2+T3 ── T5 (dogfooding 跑完整流程)
T5 ── T6 (基于 dogfooding 体验决定 Rule #9 升级条件)
T5 ── T8 (**T5 acceptance 通过后**方可运行 benchmark; T5 失败回 Phase B 修复需重跑 T8 — R2 KM-R2-M1)
T6+T8 ── T7 (ship)
```

---

## Effort baseline (R1 TL-m1 fix — 加 buffer)

| Phase | Tasks | Optimistic | Pessimistic |
|---|---|---|---|
| Phase B core | T1 + T2 + T3 | 5.9h | 7.5h |
| Phase B test | T4 | 2.5h | 3.5h |
| Phase B dogfood | T5 | 1.2h | 2h |
| Phase B decision | T6 | 0.5h | 0.5h |
| Phase B benchmark | T8 | 1h | 1.5h |
| Phase C ship | T7 | 1h | 1.5h |
| **Total** | | **~12h** | **~16h** |

~12-16h baseline (1.5-2 day),Level 2 minimal 上限 1-3 day,scope 合理。

---

## Out of Scope (本 cycle 不做)

- 自动化 issue triage (Forgejo webhook → aria-runner-bot) — M2+ (Q4 决策)
- Issue 自动 labeling (基于 triage verdict) — M2+
- 跨平台 issue 抓取 (GitHub / GitLab) — 仅 Forgejo (forgejo CLI 已通用,GitHub 适配推后续)
- Triage report 的 audit log immutable 存储 — 引用 US-025 M5 通用 audit-log 即可 (M5 ship 后)
- **真实修复 #101 的 `_normalize_status` bug** — 独立 cycle `aria-issue-101-status-normalize`,本 SOP 仅定义流程,不做 bug 修复
- **CLAUDE.md Rule #9 入册** — 本 cycle 不加, 见 T6 决策 memo (Q2 决策)
