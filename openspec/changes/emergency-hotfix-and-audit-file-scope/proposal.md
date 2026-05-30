# emergency-hotfix-and-audit-file-scope — hotfix lane + audit file-scope 过滤

> **Level**: 2 (Minimal — proposal.md only; state-scanner 规则 + phase-a-planner doc + audit-engine 逻辑 + config + convention, 不跨多 service)
> **Status**: ✅ **Approved** — Phase A.2 CONVERGED 2026-05-30 via R1 (3/3 REVISE, 3 Critical: file-scope 数据源 + Prod-Validated gate 无 enforcer + DEC-6 时机) → Rev1 → R2 (2 PWW + 1 REVISE: NEW-C NC1 git diff HEAD pre_merge 漏已提交变更) → Rev2 (merge-base diff) → R3 (PASS + PWW, 0 new Critical, tech-lead CONVERGED)。Level 2 baseline。triage-driven scope (#3 已 v1.34.0 默认 → 关闭)。连续 2 轮拦截 git 数据源/ref load-bearing 缺陷。
> **Change ID**: `emergency-hotfix-and-audit-file-scope`
> **Source**: Forgejo Aria [#58](https://forgejo.10cg.pub/10CG/Aria/issues/58) (3-in-1, filed v1.16.0; triage 缩水到 2 gap)
> **决策来源**: [DEC-20260530-002](../../../.aria/decisions/2026-05-30-emergency-hotfix-and-audit-file-scope.md)
> **Target version**: aria-plugin v1.35.0
> **Risk class**: Additive (新推荐规则 + config + doc + audit 二次过滤 + phase-b 轻量 trailer gate; 无 API break; 默认行为不变 — file-scope 仅 audit-on 项目生效, hotfix lane advisory)

> **Rev1 changelog (post_spec R1 audit 闭合, 2026-05-30, R1 = 3/3 REVISE)**:
>   - **C (backend+qa) file-scope 数据源错配**: `changes` collector **不暴露文件路径** (仅 file_types 计数); audit-engine **不读 snapshot** (Phase Skill 调用, 只传 context)。修: audit-engine file-scope 自行跑 `git diff --name-only HEAD` (+ untracked via `git ls-files --others --exclude-standard`) 取变更文件列表, **不依赖 snapshot/changes 字段**。DEC-6 + Task 1.3 + Impact 更正。
>   - **C (tech-lead) Prod-Validated gate 无 enforcer (advisory paper-fix)**: 修 = **方案 B 轻量机械 leg** — phase-b-developer 在 hotfix 分支 + 跳单测时 grep commit 是否含 `Prod-Validated:` trailer, 缺则 **block** (回标准 lane); trailer **存在性**机检, **内容真实性**仍靠 owner PR review + audit trail。诚实声明: 防"忘记留证", 不防"故意造假"。
>   - **C (qa+tech-lead) DEC-6 求值时机矛盾**: 统一为 **adaptive/checkpoint 解析后** `min(resolved_mode, convergence)` (先有 resolved_mode 才能 cap)。DEC-6 措辞更正。
>   - **M (tech-lead) quick_fix 优先级方向**: "高于/低于" 歧义 (数字越小越优先)。修: emergency_hotfix 优先级数值 **1.85** (< quick_fix 2, 与 audit_unconverged 1.9 同档但更急)。
>   - **M (tech-lead) hotfix lane 跨 4 phase deliverable 错位**: 修 = 拆分 — skip A.1-A.3 → phase-a-planner; B.3 单测替代 + trailer gate → **phase-b-developer** (持 --skip-tests); pre_merge→convergence → **phase-c-integrator/audit-engine**; phase-a-planner 留 lane 概览 + cross-ref。
>   - **M (backend) scope_skip_paths 匹配语义**: 目录项用 `path.startswith(prefix)` (尾斜杠规范化); 后缀项 (`*.md`) 用 `path.endswith('.md')`。Task 1.4 明确。
>   - **M (backend) 0 文件 vacuous true**: `len(changed_files)==0` → file-scope **不生效** (pass-through, 不降级)。加 SC + Task。
>   - **M (qa) hotfix 触发时机**: commit `hotfix(...)` 是 future commit (开发期未提交)。修: **`hotfix/*` 分支 (`git.current_branch`) 为主触发**; commit prefix 仅 corroborating (检 `git.recent_commits[0].subject`, best-effort)。
>   - **M (qa) 双降级 + audit-on**: pre_merge→convergence **仅 `audit.enabled=true` 且 checkpoint != off** 时生效 (与 file-scope "仅 audit-on" 对齐); 双降级幂等 (都 → convergence)。加注 + SC。
>   - **M (qa) Rule #6 SC 分层**: 拆"文档存在性 SC" (fixture 可验 — 字符串/字段存在) vs "行为遵从性 SC" (dogfood-only, 标注不可 fixture 验)。SC + Task 1.6 区分。
>   - **m**: Submodule-Rollback trailer 先例在 CLAUDE.md (非 git-commit.md) — 引用更正; RECOMMENDATION_RULES 双写 (主索引 + basic-rules.md); trailer 单行值 (evidence 换行用分号); emergency_hotfix 规则补 confidence% + auto_execute 字段。

> **Rev2 changelog (post_spec R2 audit 闭合, 2026-05-30, R2 = 2 PWW + 1 REVISE / 1 NEW Critical)**:
>   - **NEW-C (backend) git diff ref 语义错**: Rev1 的 `git diff --name-only HEAD` 在 **pre_merge 时点** 漏掉**已提交**变更 (hotfix 文件已 commit 到 HEAD → diff HEAD 仅返未提交, 通常空 → 0-files pass-through → 过滤在主用例失效)。修: file-scope 取变更用 **`git diff --name-only $(git merge-base HEAD <base>)`** (捕获 base→工作树的 committed+staged+unstaged 全部变更, 跨 checkpoint 正确); 不再单独依赖 untracked (merge-base diff 已覆盖 hotfix committed 文件; untracked 临时文件 pre_merge 不应计入)。
>   - **NW (backend) base branch 硬编码**: `<base>` 不硬编码 `origin/master`; 从 `.aria/config.json` `phase_c_integrator.*` base 或 `git symbolic-ref refs/remotes/origin/HEAD` 取, fallback `origin/main`→`origin/master`。
>   - **m (qa) confidence/auto_execute 具体值**: emergency_hotfix 规则 `confidence: 85%` + `auto_execute: No` (紧急但需人判断, 不自动执行)。
>   - **m (qa+tl) DEC prose 触发措辞**: DEC hotfix lane 行为段 "分支 **或** prefix" → 对齐 proposal "分支主触发 / prefix corroborating"。
>   - **m (backend) 尾斜杠规范化方向**: config 目录项规范化为**确保有尾斜杠** (`"deploy"` → `"deploy/"`), 防 `startswith("deploy")` 误匹配 `deployment/`。

---

## Why

### Source (#58, SilkNode hotfix PR #268)

2026-04-28 SilkNode prod cron 5-day silent failure 紧急 hotfix (5 deploy script `curl→wget`)。走 aria 十步循环遇 2 个真 gap (triage 后, 第 3 项已是 v1.34.0 默认):

1. **无 emergency hotfix lane**: prod 紧急修复必须 lighter weight, 但 aria 无明确"emergency 跳哪些步"→ 要么全跑耗时, 要么全跳丢文档化。
2. **adaptive audit 不按 file scope 过滤**: `audit.mode=adaptive` 只按 Level (复杂度) 决定严格度, 但 **file scope 也是关键信号** —— `deploy/*.sh` 33 LOC ops-only 跑 challenge audit 收益极低 (agent team 难比 prod 实证强), 与 `web/src/lib/wallet.ts` 33 LOC 业务逻辑享受同样 audit 配置, 但风险面差数量级。

### triage: version drift 缩水 scope

issue filed v1.16.0, 现 v1.34.0 (18 minor)。sub-item #3 (推荐 adaptive_rules L1 off/L2 convergence/L3 challenge) **已是 v1.34.0 默认** + checkpoints 默认全 off → over-audit 默认已规避, **关闭** #3。本 Spec 做剩余 2 gap。

---

## What

### Part 1 — emergency hotfix lane (advisory, DEC-2/3)

state-scanner 新增 `emergency_hotfix` 推荐规则; phase-a-planner 文档化 lighter lane。

**触发** (Rev1): **主触发 = `hotfix/*` 分支** (`git.current_branch`, 可靠机检); commit `hotfix(...)` prefix 仅 corroborating signal (检 `git.recent_commits[0].subject`, best-effort, 因 future commit 开发期未提交)。

**lighter lane 行为** (advisory 推荐, 非硬 skip; 跨 phase deliverable 拆分见下):
- **[phase-a-planner]** 跳 Phase A.1-A.3 (无独立 spec; commit body + trailer 取代)
- **[phase-b-developer]** B.3 单测可被 **manual prod validation 替代** —— phase-b-developer 在 hotfix 分支 + 跳单测时 **机械 grep** commit 是否含 `Prod-Validated:` trailer: **有 → 允许替代; 无 → block, 回标准 lane** (Rev1 方案 B 轻量 gate)
- **[phase-c/d]** 仍走 Phase C/D (commit / PR / merge / UPM)
- **[phase-c-integrator/audit-engine]** pre_merge audit **仅 `audit.enabled=true` 且 pre_merge checkpoint != off 时** 降级到 **convergence** (不 challenge)

**prod-validated 证据 (DEC-3, 强制)**: commit message 必含:
```
hotfix(scope): <summary>

根因: <root cause>
Prod-Validated: <evidence — e.g. cron 恢复 2026-04-28, 9 jobs uploaded, run #3162>
```
`Prod-Validated:` 是机械可 grep 的单行 trailer (evidence 内换行用分号; 复用 Aria trailer 约定: `Co-Authored-By:` [git-commit.md] / `Submodule-Rollback:` [CLAUDE.md Rule #8])。

> **gate 硬度 (Rev1, 诚实声明)**: phase-b-developer 机检 trailer **存在性** (无 trailer 跳单测 → block, 回标准 lane) —— 防"忘记留验证证据"。trailer **内容真实性** (`Prod-Validated: x` vs 真实 evidence) 仍靠 owner PR review + audit trail 事后追溯, **不**事前机械防伪。hotfix 低频 + 留痕 + owner gate 下此权衡可接受。

### Part 2 — audit file-scope 二次过滤 (DEC-4/5/6)

audit-engine 在解析 adaptive/checkpoint mode **之后** 加 file-scope 二次判定 (Rev1: 解析后 cap, 先有 resolved_mode 才能 min):

```
base = .aria/config base  OR  git symbolic-ref refs/remotes/origin/HEAD  (fallback origin/main→origin/master)
changed_files = git diff --name-only $(git merge-base HEAD <base>)
                # Rev2: merge-base diff 捕获 base→工作树的 committed+staged+unstaged 全部变更,
                # 跨 checkpoint 正确 (pre_merge 时 hotfix 已 commit, diff HEAD 会漏 → 必须 merge-base)
                # audit-engine 自取 (不依赖 snapshot — audit-engine 由 Phase Skill 调用, 不读 snapshot)

若 len(changed_files) == 0:
    file-scope 不生效 (pass-through, 不降级)        # Rev1: 防 vacuous-true 空集误触
elif (changed_files 全部 ⊆ scope_skip_paths):
    audit mode = min(resolved_mode, convergence)   # challenge → convergence; convergence/off 不变
else (任一业务文件 ∉ skip_paths):
    audit mode 不变 (标准)

匹配语义 (Rev1): 目录项 (deploy/) 用 path.startswith(prefix, 尾斜杠规范化);
              后缀项 (*.md) 用 path.endswith('.md')
```

- **降级而非 skip** (DEC-4): issue 自身事故是 deploy script (challenge 找到 wget HTTP 4xx 退出 0 真退化) → deploy 改动不能全 skip; convergence 保留安全网 (~5min vs challenge 15-30min)。
- **scope_skip_paths 默认** (DEC-5): `["deploy/", "docs/", ".forgejo/workflows/", ".github/workflows/"]` + `*.md` 后缀; `.aria/config.json` `audit.scope_skip_paths` 可覆盖。
- **数据源** (Rev2, DEC-6 更正): audit-engine 自取 `git diff --name-only $(git merge-base HEAD <base>)` (merge-base diff, 跨 checkpoint 正确捕获 branch 全部变更; base branch 可配/symbolic-ref 取) —— **不依赖** `changes` collector (只 file_types 计数, 无路径) 或 snapshot (audit-engine 不读)。机械 scan.py `changes.scope_skip_match` 字段 = optional follow-up (defer)。
- **仅 audit-on 项目生效**: audit 默认全 off, 故本过滤只对显式 enable audit 的项目 (如 SilkNode) 减负; hotfix lane 的 pre_merge→convergence 与此过滤双降级时幂等 (都 → convergence)。

### Key Deliverables (Rev1: 跨 phase 拆分)

- `aria/skills/state-scanner/references/rules/basic-rules.md` (新 `emergency_hotfix` 规则, 优先级数值 **1.85** < quick_fix 2; 含 confidence% + auto_execute 字段) + `RECOMMENDATION_RULES.md` 主索引 (双写)
- `aria/skills/phase-a-planner/SKILL.md` — emergency hotfix lane **概览** (触发 + skip A.1-A.3) + cross-ref 各 phase 落点
- `aria/skills/phase-b-developer/SKILL.md` — B.3 单测替代 + **Prod-Validated trailer 机检 gate** (无 trailer → block, 回标准 lane)
- `aria/skills/audit-engine/SKILL.md` — file-scope 二次过滤 (自取 `git diff --name-only`; 0 文件 pass-through; adaptive 解析后 cap convergence) + pre_merge→convergence (hotfix lane, 仅 audit-on)
- `aria/skills/phase-c-integrator/SKILL.md` — hotfix lane pre_merge→convergence 调用点 (advisory)
- `aria/skills/config-loader/{DEFAULTS.json, config-example.md}` — `audit.scope_skip_paths` (默认清单 + 匹配语义注)
- `standards/conventions/git-commit.md` — `Prod-Validated:` 单行 trailer schema + emergency hotfix commit 格式
- Rule #6: deterministic structural substitute (规则/config/convention 字段一致性 fixture; 行为遵从性标 dogfood-only)

---

## Impact

| 组件 | 变更 | 风险 |
|------|------|------|
| state-scanner | 新 emergency_hotfix 推荐规则 (优先级 1.85) | 低 (additive 规则) |
| phase-a-planner | hotfix lane 概览 + cross-ref (advisory) | 低 (doc) |
| phase-b-developer | B.3 单测替代 + Prod-Validated trailer 机检 gate | 低 (仅 hotfix 分支 + 跳单测时) |
| audit-engine | file-scope 二次过滤 (自取 git diff) + pre_merge→convergence | 低 (仅 audit-on 项目; 降级非 skip) |
| phase-c-integrator | hotfix pre_merge→convergence 调用点 | 低 (advisory) |
| config-loader | `audit.scope_skip_paths` namespace | 低 |
| standards/git-commit | `Prod-Validated:` trailer schema | 低 (additive convention) |

**Backward compat**: file-scope 仅 audit-on 项目生效 (默认 audit off → 无影响); hotfix lane advisory (不强制, 不改标准 lane); scope_skip_paths 缺省用内置清单; 无 API break。

---

## Tasks

- [ ] 1.1 state-scanner `emergency_hotfix` 规则: 主触发 `hotfix/*` 分支 (`git.current_branch`); commit prefix corroborating (best-effort); 优先级数值 **1.85** (< quick_fix 2); `confidence: 85%` + `auto_execute: No` (紧急但需人判断); 推荐 lighter lane。**双写**: 规则细节进 `references/rules/basic-rules.md` (quick_fix 同档) + 索引行进 `RECOMMENDATION_RULES.md` 主表
- [ ] 1.2 phase-a-planner SKILL.md: hotfix lane **概览** (触发 + skip A.1-A.3) + cross-ref phase-b-developer (B.3 gate) / audit-engine (pre_merge→convergence)
- [ ] 1.3 phase-b-developer SKILL.md: hotfix 分支 + 跳单测时 **机械 grep** commit `Prod-Validated:` trailer; 有 → 允许 manual prod validation 替代单测; 无 → block 回标准 lane
- [ ] 1.4 audit-engine SKILL.md file-scope 二次过滤: **自取** `git diff --name-only $(git merge-base HEAD <base>)` (merge-base diff 跨 checkpoint 正确; base 从 config/`symbolic-ref` 取, 不硬编码; **base 全 fallback 失败 (R3 NW-R3-1) → file-scope skip + warn, 不 crash audit-engine**; 不依赖 snapshot/changes 字段); `len==0` pass-through; adaptive/checkpoint 解析**后** 判定全部 ⊆ scope_skip_paths → `min(resolved, convergence)`; 匹配语义 (目录项规范化确保尾斜杠后 startswith / 后缀 endswith); + pre_merge→convergence (hotfix lane, 仅 audit.enabled + checkpoint!=off)
- [ ] 1.5 phase-c-integrator SKILL.md: hotfix lane pre_merge→convergence 调用点 (advisory)
- [ ] 1.6 config-loader: `audit.scope_skip_paths` 默认 `["deploy/","docs/",".forgejo/workflows/",".github/workflows/"]` + `*.md`; 匹配语义注 (目录 startswith / 后缀 endswith); DEFAULTS.json + config-example.md
- [ ] 1.7 standards/conventions/git-commit.md: `Prod-Validated:` **单行** trailer schema (evidence 换行用分号) + emergency hotfix commit 格式 (hotfix(scope) + 根因 + Prod-Validated); 引 CLAUDE.md Submodule-Rollback 作 trailer 先例
- [ ] 1.8 Rule #6 deterministic structural substitute: **文档存在性 fixture** (emergency_hotfix 规则字段完整含 priority 1.85/confidence/auto_execute / scope_skip_paths 默认值 + 匹配语义 / git-commit Prod-Validated trailer 文档 / phase-b trailer gate 文本存在); **行为遵从性 (advisory lane 执行 / file-scope 实际过滤) 标 dogfood-only 不可 fixture 验**

---

## Success Criteria

**文档存在性 (Rule #6 fixture 可验)**:
- [ ] state-scanner `emergency_hotfix` 规则存在: 触发 = `hotfix/*` 分支 (主); 优先级数值 1.85 (< quick_fix 2); confidence% + auto_execute 字段齐全; 双写 (basic-rules.md + RECOMMENDATION_RULES 主表)
- [ ] phase-b-developer SKILL.md 含 Prod-Validated trailer gate 文本 (hotfix + 跳单测 → grep trailer → 无则 block)
- [ ] config `audit.scope_skip_paths` 缺省用内置清单 + 匹配语义注 (目录 startswith / 后缀 endswith); 可覆盖
- [ ] git-commit.md 含 `Prod-Validated:` 单行 trailer schema + emergency hotfix commit 格式
- [ ] audit-engine SKILL.md file-scope 文档: 自取 git diff (不依赖 snapshot) + 0 文件 pass-through + adaptive 解析后 min(resolved, convergence)

**行为遵从性 (dogfood-only, 不可 fixture 验)**:
- [ ] (dogfood) hotfix 分支 + 全 ops 变更 + audit-on → 实际降级 convergence; 任一业务文件 → 不降级
- [ ] (dogfood) hotfix 分支跳单测无 Prod-Validated trailer → phase-b block 回标准 lane
- [ ] (dogfood) 默认行为不变: audit off 项目不受 file-scope 影响; 非 hotfix 分支不触发 lane; 0 文件不误降级

---

## Out of Scope (defer / 关闭)

- **#3 challenge over-audit / adaptive_rules 推荐** — 已是 v1.34.0 默认 (adaptive_rules L1 off/L2 convergence/L3 challenge + checkpoints off), **关闭**
- **`adaptive_force_challenge_levels: [3]`** — sub-item #3 残留, adaptive_rules 已给 level-gated, 大体冗余, defer
- **机械 scan.py `changes.scope_skip_match` 字段** — DEC-6 prose-driven v1; 机械字段 defer follow-up
- **PR body 验证块** — DEC-3 选 commit trailer (进 git 历史) 而非 PR body
- **硬机械 hotfix skip gate** — advisory 模式 (DEC-2), 不硬跳
- **file-scope 区分 deploy (downgrade) vs docs (skip)** — v1 统一 downgrade; 细分 defer
