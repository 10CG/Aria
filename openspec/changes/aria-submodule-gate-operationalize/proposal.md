# aria-submodule-gate-operationalize — 修复 gate 生态零运营证据 (R-fix-1 + R-fix-2)

> **Status**: 🔵 **TG-1 SHIPPED (2026-06-07, aria-plugin v1.40.0); TG-2 PENDING (infra)**。Phase A.2 CONVERGED 2026-06-07 (post_spec R1 qa REVISE → Rev1 → R2 全票 PASS 3/3)。**TG-1 (R-fix-1)** = gate `submodule-gate-executions.jsonl` per-invocation 计数 (含 PASS) + PostToolUse `submodule-gate-telemetry.sh` hook (OQ1=(a′), gitlink-commit 触发, warn-only) + 7 测; code-review PASS (Minor #1 锚定修复 + #2 timeout wrapper 已收)。**TG-2 (R-fix-2)** tripwire runner forgejo 凭据 = infra-gated, 待办。Spec 保留 changes/ 直到 TG-2 done。
> **Level**: 2 (Minimal — proposal + tasks)
> **Target**: aria-plugin **v1.40.0** (submodule_gate 调用面) + Aria 主仓 (tripwire workflow) v1.7.1
> **Trigger**: block-flip D+14 defer 决策 (`.aria/decisions/2026-06-07-v1.40.0-block-flip.md` §FINAL) — Trigger C (0 gate executions) + tripwire 验活 5/5 失败 → 两层防御均无 live 运营证据, 翻转前置不满足。
> **Parent**: `openspec/archive/2026-05-24-aria-submodule-pointer-regression-gate/` (gate 机制) + `openspec/changes/aria-submodule-gate-block-flip/` (deferred, 本 Spec 是其 unblock 前置)

## Why

submodule pointer regression gate (parent Spec, v1.28.0 ship) 设计了两层防御:
- **Pre-merge gate** (`submodule_gate.sh` via phase-c-integrator §C.2.4.5) — warn/block 模式。
- **Post-merge tripwire** (`.forgejo/workflows/submodule-gate-tripwire.yml`) — 周期 ancestry 审计兜底。

block-flip D+14 (2026-06-07) 验活暴露:**两层在 14 天观察窗内均无任何 live 运营证据**:

### R-fix-1 — pre-merge gate telemetry invocation gap (0 executions)
- `aria/metrics/` 仅 `.gitkeep`,`total_gate_executions = 0`。
- 观察窗内三仓 merged **10 个 PR**,但 gate telemetry **0 写入**。
- 根因: gate 只在**完整 phase-c-integrator merge 流程**执行时才跑 + 写 telemetry;而实际 ship (含 v1.38/v1.39 主仓 gitlink bump) 走 **git 直驱** (`git commit`/`git push` + Forgejo API merge),**绕过** `submodule_gate.sh` 调用点。
- **约束 (agent team 警告)**: **不**得把所有 git-直驱 ship 强行改道经 phase-c-integrator skill (过度工程)。fix 须是轻量、对 git-直驱 ship 也生效的调用面。

### R-fix-2 — tripwire run failure (5/5 dispatch 全失败)
- tripwire workflow dispatch run #7–#11 **全部 `failure`** (自 v1.28.0 ship 起从未成功运行)。
- **强假设 (grounded in `.gitmodules`)**: 3 个 submodule URL 全为 `ssh://forgejo@forgejo.10cg.pub/...` (CF-Access 保护 + SSH 协议)。tripwire `actions/checkout@v4 submodules:true` + 后续 `git -C <sub> fetch origin` + `merge-base --is-ancestor` 需克隆/fetch 这 3 个 forgejo submodule,而 Forgejo Actions runner **缺 forgejo SSH 凭据** → checkout/fetch 失败。5/5 一致失败符合结构性 (非瞬时) 问题。
- **待 Phase B 确认**: 实际失败 step (日志 API 经 CLI 不可达, Phase B 经 SSH/runner 或替代手段确认)。

## What Changes

两 task group (R-fix-1 调用面 + R-fix-2 tripwire),同属 submodule-gate 生态,无交叉依赖可并行。

### TG-1 (R-fix-1) — gate 在 git-直驱 ship 也能执行 + 记 telemetry

**目标**: 让 submodule pointer 变更的 ship (无论走 phase-c-integrator skill 还是 git 直驱) 都触发 gate 检测 + 写 telemetry,使观察数据真实累积。

**候选方案 (OQ1, post_spec + owner 定)**:
- (a) **git pre-push hook**: 复用 aria-plugin hook 机制 (已有 secret-guard/handoff-location-guard 先例),新增 pre-push hook 在 push 含 submodule pointer 变更时跑 `submodule_gate.sh` (warn 模式) + 写 telemetry。覆盖 git-直驱。**倾向**。
- (b) **standalone CLI 一行**: 提供 `submodule_gate.sh` 易调用入口,ship 流程 (含 phase-d/c 收尾) 显式调一次。需 ship 流程纪律。
- (c) 仅 convention 文档化 ship 必跑 gate。最弱,不推荐。
- **约束**: 不改道 git-直驱经 phase-c-integrator skill;telemetry 写入路径与 parent 一致 (`aria/metrics/*.jsonl`)。

### TG-2 (R-fix-2) — tripwire runner 可克隆/fetch forgejo submodule

**目标**: tripwire workflow dispatch 能成功完成 (clean run 或正确 detect)。

**Phase B step 0 (必办)**: 先经可达手段 (runner SSH / forgejo web / act_runner host) **确认实际失败 step + 错误**,验证或推翻 SSH-auth 假设。

**候选修复 (OQ2, 待失败确认后定)**:
- (a) runner 注入 forgejo 凭据 + git `url.insteadOf` 把 `ssh://forgejo@...` 重写为带 token 的 https (复用 workflow 已引用的 `FORGEJO_TRIPWIRE_TOKEN` secret)。
- (b) tripwire 重写为**不需 submodule checkout**: gitlink SHA 用 `git ls-tree` (superproject tree, 无需 submodule);ancestry 检查改用对 submodule remote 的 authenticated https fetch 或 API,而非 `git -C <sub>`。
- (c) tripwire 不在 Forgejo Actions 跑,改 host cron + durable volume (per [[feedback_periodic_job_acceptance_data_on_durable_volume]] 模式)。
- **若 CF-Access 致 runner 根本无法 reach forgejo** → (c) 或 (b) 优先。

## Impact

- **Affected**: aria-plugin `aria/skills/phase-c-integrator/scripts/submodule_gate.sh` + hook 机制 (TG-1) + `aria/hooks/` (若选 a) | Aria 主仓 `.forgejo/workflows/submodule-gate-tripwire.yml` (TG-2) + 可能 runner 配置/secret。
- **向后兼容**: ✅ gate 默认仍 warn 模式 (本 Spec **不** flip,flip 仍是 deferred block-flip Spec 的事);新增调用面 additive。
- **Rule #6**: deterministic/structural — TG-1 telemetry 写入单测 (fixture submodule-change push → 断言 jsonl 行) + TG-2 tripwire dry-run dispatch 成功 (dogfood) = substitute,per [[feedback_deterministic_structural_skill_rule6_substitute]]。
- **Versioning**: aria-plugin v1.39.0 → v1.40.0 (MINOR);主仓 v1.7.1。
- **Unblocks**: 修好后 gate 真实累积 ≥3 executions + tripwire 验活 → 重启 deferred block-flip (新 hard date,max D+42=2026-07-05)。

## Out of scope
- **不 flip** warn→block (那是 deferred block-flip Spec)。
- 不把所有 git-直驱 ship 改道经 phase-c-integrator (agent team 明确警告的过度工程)。
- gate 检测逻辑本身的灵敏度调整 (parent §AD-FOLLOWUP 范围)。

## AC 路径无关原则 (Rev1, per R1 qa 2 major)

OQ1/OQ2 裁定**前**, AC-1/AC-2 写成**路径无关抽象形式**, OQ 裁定后在 tasks 具体化 (防 [[feedback_spec_rework_leaves_downstream_ac_drift]] 式 downstream drift):
- **AC-1 抽象**: "submodule pointer 变更的 ship 后, telemetry 出现 ≥1 行" + 验证机制随 OQ1 具体化:
  - 选 (a) hook → 端到端 fixture (真实 `git push` 触发 hook → 断言 jsonl), 验证**触发面**而非仅 gate 写入;
  - 选 (b) CLI → 直接调用 fixture 验 gate 写入, "git-直驱自动覆盖"靠 convention (AC-1 降为验证 gate 写入 + convention 文档审阅, 不声称 hook 级自动触发)。
- **AC-2 抽象**: "tripwire 能成功执行一次 (clean 或正确 detect, 非 failure)" — 触发方式 (dispatch for OQ2 a/b / cron for OQ2 c) 由裁定后具体化; 选 (c) host-cron 时 AC-2 = "cron job 首次成功执行"。

## Open questions (Phase A.2 audit / owner)
1. **OQ1**: TG-1 调用面 = pre-push hook (a) / standalone CLI (b) / convention (c)? 倾向 (a)。**裁定 (a) 时须澄清** (R1 tech-lead): hook 触发点 (superproject gitlink bump push) 捕获的 master/feature 指针对, 是否等价于现行 gate (PR-merge-time, `submodule_gate.sh` 比 local HEAD vs origin/master) 的期望输入 — 否则 telemetry 记到与设计不符的对比基准。
2. **OQ2**: TG-2 修复路径 — 待 Phase B step 0 确认实际失败后, 在 token-rewrite (a) / 免-checkout 重写 (b) / host-cron 迁移 (c) 中定。CF-Access 是否让 runner 根本无法 reach forgejo 是关键变量。**(a) 须核 token scope** (R1 code-reviewer): `FORGEJO_TRIPWIRE_TOKEN` 现为 issues:write (file-issue 用途), 做 submodule https-fetch 需 repo-read, scope 可能不足 — Phase B step 0 顺带核。
3. **OQ3**: 本 Spec ship 后是否立即重启 block-flip, 还是再观察一个真实窗口攒 ≥3 executions? 倾向后者 (defer 的本意)。
