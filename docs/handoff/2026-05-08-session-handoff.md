# Aria — Session Handoff (2026-05-08)

> **Status**: Active — Ready for next session
> **Cycle period**: 2026-05-07 (T5 quick-win) → 2026-05-08 (G2+G3+G4 Spec approved)
> **Next session 入口建议**: 优先读本 doc,然后按 [Recommended workflow](#recommended-workflow) 选轨道

---

## TL;DR

本 cycle 完成两件事 + 留下三轨道未启动工作:

**完成**:
1. **T5 quick-win shipped** — state-scanner SKILL.md 加 inter-cycle resume AI 行为兜底指引(17 行 → R2 收敛后一并 ship);aria submodule `b22d27d`,主项目 `a9a6a6a`
2. **G2+G3+G4 OpenSpec approved + merged** — `state-scanner-inter-cycle-surfacing` Level 2 Spec,post_spec audit R1+R2 收敛 PASS_WITH_WARNINGS(4/4 vote PASS);主项目 master `0d3796e`

**未启动(下次 session 选项)**:
- Phase B 实施 G2+G3+G4(18 任务,1-2 cycle)
- #60 phase-c-integrator pre-merge gate(aether#89 已解锁)
- #58 F2+F3 audit scope/level
- #58 F1 brainstorm + Spec(碰 CLAUDE.md 不可协商规则 #2,需慎重)

**等待外部输入**:
- G1 PRD Status 解析诊断 — 等 SilkNode 回贴 `state-snapshot.json` 摘录 + PRD 头部 raw bytes,deadline **2026-05-22**

---

## Repository state

| 仓库 | HEAD | origin (Forgejo) | github | Status |
|---|---|---|---|---|
| Aria (主) | `0d3796e` | ✅ | ✅ | parity |
| aria (submodule) | `b22d27d` | ✅ | ✅ | T5 ship 后 parity |
| standards (submodule) | `2cd34d3` | ✅ | ✅ | unchanged |
| aria-orchestrator | `3e559a7` | ✅ | (Forgejo only) | unchanged |

工作树:干净。所有 feature 分支已清理。

---

## 已完成事项 (按 cycle 顺序)

### 2026-05-07

1. **同步本地与远程**(初始 cycle entry) — main 拉了 25+ 提交(US-024 Phase A docs / m3 carryover trio archive / aria-secret-hygiene-rule archive 等)
2. **三个 SilkNode issue triage**:
   - `#60` phase-c-integrator pre-merge gate(aether#89 unblocked)→ accept
   - `#85` state-scanner surfacing gap → partial accept(G2/G3/G4 ✅,G1 等数据)
   - `#58` 3 hotfix improvements → partial accept(F2/F3 ✅,F1 待 brainstorm)
3. **T5 quick-win** — SKILL.md 阶段 2 加 17 行 inter-cycle resume AI 行为兜底
   - aria PR #36 → merged → SHA `eaaf422` → merge commit `b22d27d`
   - 主项目 PR #87 → merged → SHA `a9a6a6a`(submodule pointer + benchmark archive)
   - Smoke benchmark R1 12/12 → R2 13/13(响应 `aria:code-reviewer` Important #2 移除 branch check)
   - benchmark archive: `aria-plugin-benchmarks/ab-results/2026-05-07-state-scanner-t5-ai-fallback/`

### 2026-05-08

4. **state-scanner-inter-cycle-surfacing OpenSpec**(Level 2)
   - proposal.md drafted(243 行 → 修订后 351 行)
   - post_spec audit R1: FAIL(5 Critical / 12 Major / 11 Minor,4 agent vote 1 PASS / 3 REVISE)
   - Path A 修订:5 Critical + 6 高 Major fix
   - post_spec audit R2: **PASS_WITH_WARNINGS**(0 Critical / 0 Major post-fix / 10 minor/low,**4/4 vote PASS**)
   - R2 single-point fix: G3 备选 regex 移除 "入口" 独立 alternation(4 agent 一致 raise)
   - Spec PR #88 → merged
   - Audit reports committed:`.aria/audit-reports/post_spec-R{1,2}-2026-05-08-*.md`

---

## 未完成事项 (by priority)

### P1 — Ready to start

#### Phase B 实施 G2+G3+G4(state-scanner-inter-cycle-surfacing)

**Spec**: `openspec/changes/state-scanner-inter-cycle-surfacing/proposal.md`(已 merge 到 master)

**执行顺序**(per Spec L227 声明):
1. **TX.0** `collectors/git.py` 加 derived 字段 `status_clean`(prerequisite)
2. **TX.1** `state-snapshot-schema.md` 四节扩充 + `normalize_snapshot.py` 加 raw_row DROP_KEYS
3. **G2 ∥ G3 ∥ G4** 并行(三组无文件冲突)
4. **TX.2-TX.7** 串行(SKILL.md 降级 / AB benchmark / version bump / dogfooding 等)

**预计**: 18 任务 + 3 项目 dogfooding + 完整 `/skill-creator` AB benchmark = 1-2 cycle 周期

**关键引用**:
- 主参考: proposal.md
- audit follow-up: `.aria/audit-reports/post_spec-R2-2026-05-08-state-scanner-inter-cycle-surfacing.md`(10 minor/low follow-up checklist)
- 版本规划: aria-plugin v1.17.7 → **v1.18.0**(MINOR)

#### #60 phase-c-integrator pre-merge gate OpenSpec(已承诺)

**Issue**: [10CG/Aria#60](https://forgejo.10cg.pub/10CG/Aria/issues/60) — triage 已 accept(2026-05-07 issuecomment-5378)

**上游已就绪**: aether#89 已 closed(2026-05-06),`aether ci status --in-flight` flag + `aether-pre-merge-check` skill 可用

**预计 Spec scope**(Level 3):
- `phase-c-integrator/SKILL.md` 加 C.2 步骤 `pre-merge-precondition`(调 `aether-pre-merge-check`)
- `workflow-runner` BLOCK 路径改为 wait+retry(协作正常态,非 fatal)
- `CLAUDE.md` 不可协商规则集加一条(与"push 后必跑 aether-ci 监控"同等级)

#### #58 F2+F3 audit scope/level OpenSpec(已承诺)

**Issue**: [10CG/Aria#58](https://forgejo.10cg.pub/10CG/Aria/issues/58) — triage 已 accept(2026-05-07 issuecomment-5380)

**Scope**:
- F2: audit-engine adaptive_rules 加 file-scope 二次过滤;`audit.scope_skip_paths` 配置项
- F3: 推荐配置矩阵显式文档化(Level 1→off / 2→convergence / 3→challenge);新配置项 `adaptive_force_challenge_levels: [3]`

**预计 Spec level**: Level 2

### P2 — Needs prerequisite or care

#### G1 PRD Status 解析诊断(等 SilkNode 数据)

**Status**: `_status.py` 已含 6 个 pattern(包括 `**Status**: Approved` 和 i18n 全角冒号),SilkNode 5/5 全 null 是异常

**等数据**(per spec out-of-scope L329):
- SilkNode `.aria/state-snapshot.json` 中 `requirements.prd[]` 5 条目的 `path` + `raw_status`
- 任意 1 个 PRD 文件头部前 30 行 raw bytes(不要 copy-paste 后再粘 — 保留原始格式)
- PRD 文件实际路径

**Deadline**: 2026-05-22 — 若无数据,Tech Lead 决策关闭 G1 / 转 backlog / 降优;G1 独立 Spec(如需)在 `openspec/changes/` 另起,**不**修改 `state-scanner-inter-cycle-surfacing` spec

#### #58 F1 emergency hotfix lane(brainstorm + 谨慎 Spec)

**Issue**: [10CG/Aria#58](https://forgejo.10cg.pub/10CG/Aria/issues/58)F1 — triage 已标 "需 brainstorm"(2026-05-07 issuecomment-5380)

**冲突点**: 直接违反 CLAUDE.md 不可协商规则 #2 "十步循环不能跳过 Phase A"

**反提案** (待 brainstorm 确认):不 "跳过" Phase A,而是 fast path — A.1-A.3 由 commit body 充当 inline Spec,Phase A audit 自动降级为 `convergence + max_rounds=1`

**预计 Spec level**: Level 3(碰红线,需慎重 + 多轮 audit)

### P3 — Implementation phase tracking

R2 audit 10 minor/low follow-up(已记录在 R2 audit report,转 Phase B implementation 阶段处理):

- TL-6 baseline 372 计数缺 commit SHA 锚点 → PR review 时附 grep 命令
- TL-7 AB benchmark arm B "v1.17.7+T5" 在 fixture 上 LLM 噪声风险 → TX.3 加 ≥5 trials 取均值约束(可选)
- BA-10 T2.2 全角空格 (Python `\s` 含 U+3000) edge case → 实现时改 `[ \t]+` 替换 `\s+`
- BA-11 T3.2 绝对路径 `relative_to` 处理 → try `relative_to(project_root)`,失败保留 + soft_warn
- QA-N2 T4.5 config-loader 路径 → 沿用 `.aria/config.json` schema 扩展惯例
- QA-N3 AB arm B 与 git.status_clean 缺失互动 → TX.3 加 note(arm B 不依赖 status_clean)
- KM-08 TX.1 物理排版 vs 执行顺序声明 → G2/G3/G4 节头加 "前置: TX.0 + TX.1 必须已完成" NOTE

---

## 风险点

1. **G1 deadline 2026-05-22 临近** — 如 SilkNode 不回贴数据,需主动 follow-up 或 Tech Lead 决策关闭。提醒触发点:**5/15 起每周一 review issue #85 状态**
2. **Phase B 实施跨度大** — 18 任务在单 session 跑会很长,建议拆 sub-PRs:(a) TX.0+TX.1 schema 一个 PR;(b) G2/G3/G4 各一个 PR;(c) TX.2-TX.7 cleanup 一个 PR。或 sub-batches
3. **#60 spec 起草前确认 aether 上游 primitive 可用** — `aether ci status --in-flight` flag + `aether-pre-merge-check` skill 已 closed,实施时验证它们已 ship 到生产
4. **F1 hotfix lane 碰不可协商规则 #2** — 任何 spec 改动必须保留 "Phase A 不能跳过",只能优化 fast path

---

## Recommended workflow (按你的目标选)

| 你想做 | 推荐路径 |
|---|---|
| 让 v1.18.0 早 ship,unblock SilkNode 主诉求 | **Phase B 实施 G2+G3+G4**(P1) — 调 `aria:phase-b-developer`,先做 TX.0+TX.1,再并行 G2/G3/G4 |
| 跨项目 CI 安全 net 优先(避免 PR-321/PR-322 类事故再发) | **#60 pre-merge gate Spec**(P1) — `aria:spec-drafter` Level 3 起草 |
| audit ceremony 优化(降低 Level 1 over-audit) | **#58 F2+F3 Spec**(P2) — Level 2 起草 |
| G1 推动 | 给 SilkNode 团队 ping,索取 snapshot 摘录 + PRD 头部 raw bytes |
| 想先了解全貌再决定 | 调 `/state-scanner` 扫一遍,看推荐入口 |

---

## Next session 入口建议(若你直接复用 inter-cycle-resume scenario)

> 🚪 Next session 入口: 见 [docs/handoff/2026-05-08-session-handoff.md](docs/handoff/2026-05-08-session-handoff.md)

(此格式与 issue #85 G3 spec 中定义的 `> .*Next session 入口.*\(.+\.md\)` regex 兼容,Phase B 实施 G3 后会被 collector 自动识别)

---

## 引用清单

### 本 cycle artifacts

- aria PR #36(merged): https://forgejo.10cg.pub/10CG/aria-plugin/pulls/36
- 主项目 PR #87(merged): https://forgejo.10cg.pub/10CG/Aria/pulls/87
- Spec PR #88(merged): https://forgejo.10cg.pub/10CG/Aria/pulls/88
- T5 smoke benchmark R2: `aria-plugin-benchmarks/ab-results/2026-05-07-state-scanner-t5-ai-fallback/`
- post_spec R1 audit: `.aria/audit-reports/post_spec-R1-2026-05-08-state-scanner-inter-cycle-surfacing.md`
- post_spec R2 audit: `.aria/audit-reports/post_spec-R2-2026-05-08-state-scanner-inter-cycle-surfacing.md`
- approved Spec: `openspec/changes/state-scanner-inter-cycle-surfacing/proposal.md`

### Issue tracking

- [10CG/Aria#85](https://forgejo.10cg.pub/10CG/Aria/issues/85) — open(G1 等数据 + G2/G3/G4 spec 已 ship 待实施)
- [10CG/Aria#60](https://forgejo.10cg.pub/10CG/Aria/issues/60) — open(待起 spec)
- [10CG/Aria#58](https://forgejo.10cg.pub/10CG/Aria/issues/58) — open(F2/F3 待 spec,F1 待 brainstorm)

### 方法论参考

- v1.17.3 立例(state-scanner-collector-regex-hardening): `aria-plugin-benchmarks/ab-results/2026-04-25-state-scanner-regex-hardening-v1.17.3/`
- m3 carryover 系列(类似 Level 2 spec 流程参考): `openspec/archive/2026-05-07-m3-*/`
- Aria CLAUDE.md 不可协商规则(尤其 #2 / #3 / #6)
