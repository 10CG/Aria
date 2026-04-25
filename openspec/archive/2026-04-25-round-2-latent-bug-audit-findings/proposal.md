# round-2-latent-bug-audit-findings — 主动 audit 第 2 轮发现汇总

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 作为 backlog catalog 用)
> **Status**: Complete (2026-04-25, catalog finalized + archived per self-instruction "merge 后立即归档")
> **Created**: 2026-04-25
> **Completed**: 2026-04-25
> **Type**: 调查报告 + backlog grouping (非单一实现 Spec)
> **Source**: 2026-04-25 v1.17.3 发布后 user 选 [C] = "再来一轮主动 audit, 这次扫 aria-orchestrator / 其他 Skill". 4 个并行 Explore agent dispatch.
> **Estimate**: 各子项 0.5-3h (后续每条择优立独立 Spec)
> **Related Memory**: `feedback_smoke_benchmark_truthiness.md`, `feedback_pre_draft_bug_hunt_discipline.md`, `feedback_smoke_vs_full_ab_benchmark.md`

---

## 为什么独立 Spec 而非直接修

Round-1 (state-scanner trilogy v1.17.1/2/3) 之后 main repo + aria 干净, 主线已闭环.
Round-2 audit 跨 4 个独立 subsystem (orchestrator / phase-c / audit-engine / validator), 不能简单一个 patch 修完. 把所有发现先汇总 + 标 verifiability + 排优先级, 然后**用户选**哪些立独立 Spec 实施, 哪些放进 backlog 长期跟进, 哪些标 false-positive 关闭.

如果直接修, 风险:
- 不同 subsystem 的修复相互无关, 应该独立验证 (混在一起回归追查难)
- audit 报告是 LLM 输出, 部分 finding 是基于读 SKILL.md 推测, 需要读实际实现验证再下结论
- 一次 session 修 4 子系统 ≠ 严谨工程

---

## 4 个 audit 来源

| Audit # | 范围 | Findings (HIGH/MED/LOW) |
|---|---|---|
| 1 | aria-orchestrator (triage/dispatch/heartbeat/notify shell scripts) | 4 / 4 / 3 |
| 2 | phase-c-integrator + git-remote-helper push flow | 3 / 3 / 3 |
| 3 | agent-team-audit + audit-engine convergence logic | 3 / 4 / 5 |
| 4 | requirements-validator + git-remote-helper cross-doc | 3 / 3 / 3 |

---

## 优先级 P0/P1/P2 分类 (按 verifiability + impact 排序)

### P0 — 已 verified + 易修 + 复用近期教训

#### P0.1 requirements-validator Status i18n gap

**File**: `aria/skills/requirements-validator/SKILL.md` 第 104, 138 行
**Finding**: SKILL.md 仅文档化 `Status: Draft|Review|Active|...` 半角冒号形式, 未提及全角 `：` 或 6-pattern 兼容. 该 Skill 是 LLM-driven (allowed-tools: Read/Glob/Grep, 无 scripts), validator 行为依赖 prompt.
**Risk**: 中文项目 (Kairos / 任何中文 adopter) 的 PRD/User Story 用全角冒号或 heading-prefix 形式被误报 validation 失败.
**Verifiability**: HIGH ✓ (grep 已确认仅半角)
**Fix**: SKILL.md prompt 文档同步 state-scanner v1.17.2/v1.17.3 的 6 pattern union form, 引用 `state-snapshot-schema.md`. ~10 行 doc 改动, 0 代码.
**估时**: 0.5h. 候选独立 Spec `requirements-validator-status-i18n-alignment`.

#### P0.2 audit-engine 报告文件名时间戳碰撞 (并行 4 agent 同分钟落盘)

**File**: `aria/skills/audit-engine/SKILL.md:429` (`{checkpoint}-{timestamp}.md`)
**Finding**: 时间戳粒度仅到秒级 (实际报告样本是分钟级 `T2030Z` `T2200Z`). 4 个 agent 并行 dispatch 在同一秒/分钟内完成 → 文件名碰撞 → 后写覆盖前写, 部分 agent 输出永久丢失.
**Risk**: 4-agent strict 模式审计输出不完整, 影响收敛判定.
**Verifiability**: HIGH ✓ (grep 确认无微秒/计数器后缀)
**Fix**: 文件名加微秒或 agent role suffix (e.g. `pre_merge-R1-2026-04-24T203015Z-spec-x-qa-engineer.md`).
**估时**: 1h. 候选独立 Spec `audit-engine-report-filename-uniqueness`.

### P1 — 已 verified + 中等修复成本

#### P1.1 aria-orchestrator shell 脚本 silent stderr 一系列

**Files**: `triage.sh`, `scripts/dispatch-issue.sh`, `heartbeat.sh`, `notify-feishu.sh`, `scan.sh`
**Finding**: 多处 `2>/dev/null || echo ""` / `python3 -c | tail -1` 等模式吞掉 stderr, 导致网络/auth/JSON parse 错误无法区分.
**Risk**: 生产部署时 cron 失败原因诊断难, 错误聚合到 "fail" 一类.
**Verifiability**: HIGH ✓ (audit 给出具体 file:line)
**Fix**: 系统性 stderr capture + 分类 enum reporting. 跨 5+ 文件.
**估时**: 3h+. 候选独立 Spec `orchestrator-shell-error-handling-hardening`.

#### P1.2 phase-c-integrator 提交-子模块原子性 / 部分推送状态

**File**: `aria/skills/phase-c-integrator/SKILL.md:184-190` + `git-remote-helper/scripts/push_all_remotes.sh:104-127`
**Finding 1**: `pre_remote_head` 从本地 tracking ref 读取, 远程被 force-push 后本地 ref 陈旧, success check 假阳性
**Finding 2**: 子模块 push 到 remote X 成功但主仓库 push 到 remote X 失败 → 主仓库 submodule pointer 在该 remote 指向不存在的 commit
**Risk**: 数据/状态完整性 (跨 remote 不一致) — 但日常 happy path 不触发, 仅 force-push 场景或网络 partial failure
**Verifiability**: MEDIUM (需读实际脚本验证 audit 推断)
**Fix**: 设计层面 (rollback 策略 / pre-fetch 强制 / atomic transaction 模拟)
**估时**: 2h 调查 + 2h 实现 = 4h. 候选独立 Spec `phase-c-push-atomicity-hardening`.

#### P1.3 audit-engine finding ID 哈希稳定性未明确

**File**: `aria/skills/audit-engine/SKILL.md:226` (`"id": "auto-generated-hash"`)
**Finding**: 文档说 "auto-generated-hash" 但未规范哈希函数输入 (是否包含 timestamp, agent name 等). 不同 agent 报相同 finding 但 ID 不同 → 跨轮 `R_N == R_{N-1}` 比较失败 → 永远无法收敛
**Risk**: 收敛不能机械判定, 依赖 AI prose 共识 (违反 mechanical-mode 设计哲学)
**Verifiability**: MEDIUM (需读实际 audit 报告样本验证 ID 是否真的 hash 还是 random)
**Fix**: 显式规范 hash 函数 = `sha256(category + scope + severity + spec_id)[:8]`. ~15 行 SKILL.md 改动 + 1 backfill audit 报告样本.
**估时**: 1.5h. 候选独立 Spec `audit-engine-finding-id-determinism`.

### P2 — 需调查 verify 再下结论

#### P2.1 verify_post_push.py 早退 vs all_match 矛盾

**File**: `aria/skills/git-remote-helper/scripts/verify_post_push.py:147`
**Finding (claim)**: 单个 remote 第一次匹配后早退, 不等其他 remote, race window 期下游假定已 parity
**Verifiability**: LOW — 需读完整 control flow 验证: line 198 `all_match = all(...)` 表明 final aggregation 是正确的, 早退可能仅在 per-remote loop 内
**Action**: 暂搁置 P2, 用户认为有疑问时再立 spike

#### P2.2 verify_post_push.py 短 SHA 静默失败

**File**: 同上, line 147 `if sha == expected_sha`
**Finding (claim)**: ls-remote 返回 full SHA, caller 可能传 short SHA, 静默 mismatch
**Verifiability**: LOW — 需 grep 调用方实际传什么 SHA. 通常 Aria 流程用 `git rev-parse HEAD` 返回 full, 此 finding 可能是 false positive
**Action**: P2, 加 1 个 defensive normalize step (`expected_sha[:len(sha)]` 比较) 是 5 行 patch, 但需 verify 是否真问题

#### P2.3 audit-engine 0-finding 第 1 轮 mechanical 强制

**File**: `audit-engine/references/convergence-algorithm.md:48-49`
**Finding (claim)**: 第 1 轮 0 findings + 第 2 轮 0 findings 直接判收敛, 缺 stability confirmation 轮
**Verifiability**: MEDIUM — 需读 convergence-algorithm.md 确认是否有显式 force-second-round gate
**Fix if real**: 加 mechanical guard: 任何 0-finding 轮必须紧跟一个 stability confirmation 轮才算 converge

#### P2.4 push_all_remotes.sh 部分推送 rollback

**File**: `git-remote-helper/scripts/push_all_remotes.sh:77-148`
**Finding (claim)**: 第 1 个 remote 成功, 第 2 个失败, 没 rollback, 无法从本地 ref 恢复 partial-success 状态
**Verifiability**: MEDIUM — 实现可能依赖调用方处理 partial; SKILL.md `fail_on_partial_push` flag 可能已 cover
**Action**: P2 调查后再决定立 Spec

### P3 — Negative result / 已硬化, 仅记录

- ✓ `aria-orchestrator/spikes/.../sqlite_store.py` `state_machine.py` 设计良好, 异常正确传播
- ✓ `test-dispatch-idempotency.sh` mock-based test 实质性断言, 非 smoke false-pass
- ✓ `validate-m1-handoff.py` 显式 None 检查, 无歧义
- ✓ `git-remote-helper/scripts/check_parity.sh:45-53,143-162` shallow/detached HEAD guards 正确
- ✓ `verify_post_push.py:130-156` exponential backoff 边界明确 (4 attempts × 15s = 74s)
- ✓ `push_all_remotes.sh:114-127` SHA-based success 拒绝 "Everything up-to-date" 文本启发式
- ✓ audit-engine 振荡检测 (R_N vs R_{N-2}) 设计合理
- ✓ change_id anchor validation (Issue #27) 已机械化
- ✓ checkpoint completeness gate (Issue #26) 已机械化
- ✓ challenge mode serial flow (无 race condition by data dependency)

---

## 推荐执行顺序

### 立即 (本 Spec PR merge 后, 单独立 Spec 实施)

- [ ] **Spec 1**: `requirements-validator-status-i18n-alignment` (P0.1, ~0.5h, doc-only)
- [ ] **Spec 2**: `audit-engine-report-filename-uniqueness` (P0.2, ~1h, 单文件改动)

可在下次 session 一起做, 类似 v1.17.3 节奏快速 patch (v1.17.4?).

### 下批 (估时 4h+, 单独 session)

- [ ] **Spec 3**: `audit-engine-finding-id-determinism` (P1.3, ~1.5h)
- [ ] **Spec 4**: `orchestrator-shell-error-handling-hardening` (P1.1, ~3h+)

### 调查后再立 Spec

- [ ] **Spike**: P2.1 - P2.4 各自 spike (~30min/项), 决定是 false-positive 还是真 bug
- [ ] **Spec 5 候选**: `phase-c-push-atomicity-hardening` (P1.2, ~4h, depends on spike)

### Defer indefinitely

- 所有 Negative result 项 (P3) — 仅作 hardening 信心证据保留

---

## 非目标

- 本 Spec 不实施任何修复 — 仅汇总 + 排优先级 + 提供 catalog
- 本 Spec merge 后立即归档 (它是工作记录, 不是变更集)
- 不重复 Round-1 trilogy 的 Spec 内容 (i18n / regex hardening 已发版 v1.17.2/3)

## 验收

- [ ] 本 proposal.md merge 到 master
- [ ] PR 描述链接到 4 个 audit agent 对话 (作为来源审计追溯)
- [ ] merge 后立即归档 (非长期 active changes/)
- [ ] 用户基于本 catalog 选 P0/P1/P2 子项立独立 Spec 推进

## 价值

- **跨 session 可见性**: 4 audit 输出 ~3000 字 finding 信息原本会随 session 结束丢失. 本 Spec 把它结构化保留.
- **下次主动 audit 的 baseline**: 未来每次 v1.17.x patch 后再做 round-3 audit, 可对比本 baseline 增量.
- **教训复用机制化**: P0.1 (requirements-validator i18n gap) 是 state-scanner v1.17.2 教训直接外溢, 验证"教训作为 lint 标准"的跨 Skill 适用性.
