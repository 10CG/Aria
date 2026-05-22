# 决策: DEC-20260522-001 — aria-secret-guard-plugin-default Spec brainstorm

> **日期**: 2026-05-22 | **模式**: technical
> **前置**: [`2026-05-20-secret-rotation-during-m5-deploy.md`](2026-05-20-secret-rotation-during-m5-deploy.md) §5 (Layer 3 决议)
> **后续**: A.1 spec-drafter → `openspec/changes/aria-secret-guard-plugin-default/proposal.md`

---

## §1 背景

2026-05-20 M5 T-deploy Phase B Aria 自身第二次 Rule #7 leak (`nomad var get -out=json` 暴露 5 keys), Layer 3 决议提出"把 SilkNode v1.2 secret-guard 升级为 aria-plugin 默认 hook"。决议保留 3 个 open question 进入下一 cycle brainstorm:

- Q1: plugin-level + project-level hook 同事件合并语义
- Q2: 全局 blast radius 与 ship gate mitigation 范围
- Q3: Source-of-truth 治理位置

本 brainstorm 收敛三问 + 锁定 Spec scope/timeline。

---

## §2 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 流程 | Rule #6 (Skill 改动需 benchmark) | aria-doctor SKILL.md 改动触发 structural substitute (memory `feedback_deterministic_structural_skill_rule6_substitute`) |
| 流程 | Rule #7 (secret 命令必须 redirect) | Spec 实施过程中本身必遵守, hook 文本含 grep 模式时 sanitize |
| 流程 | Rule #8 (pre-merge gate) | C.2.4 必跑 aether ci status verify |
| 流程 | Rule #9 (handoff docs in docs/handoff/) | D.3 写 cycle handoff |
| 兼容 | 现有项目本地 copy (Aria self + SilkNode 历史 SOT) | plugin 装上后必须不冲突 (Q1 实证回答) |
| 资源 | Aether owner 不在场 | smoke ship gate 路径选 P2 |

---

## §3 考虑的方案

### Scope (Spec 范围)

| 方案 | 范围 | 工作量 | 评分 | 状态 |
|------|------|--------|------|------|
| Min | 仅 plugin hook 注册 + version bump | ~1-2h | 不取 — 老项目无检测路径 | ❌ |
| **Mid** | Min + aria-doctor check 项 + standards prose update | ~5.5-8.5h | **推荐** — 装 + 检测二齿 | ✅ |
| Full | Mid + aria-doctor self-test + 跨项目 rollout playbook + governance | ~1-2 day | 长期目标, 非 v1.23.0 阻断 | ❌ |

### Q1 — Plugin vs Project hook 合并语义 (本 session 实证)

| Hypothesis | 实证结果 |
|-----------|---------|
| (a) 全部依次执行 + 任一 exit 2 即 block | ✅ **正确** (5 trials 一致, 见 §4) |
| (b) plugin 被 project override | ❌ 错 |
| (c) 按 declare order | ⚠️ 部分 (确有顺序: project-first → plugin-second ~17-34ms, 但所有 hook 都跑) |

Aria 本地 copy 处置 (Q1 mitigation):

| 选项 | 评分 | 状态 |
|------|------|------|
| (a) 直接删除依赖 plugin | 激进, 失去 v1.2 实战 fallback | ❌ |
| **(b)** 保留过渡期 snapshot, aria-doctor 检测 + owner 决定 | ⭐ 推荐 | ✅ |
| (c) thin wrapper 调 plugin | 多此一举 | ❌ |

### Q2 — Blast radius mitigation (ship gate 范围)

5 mitigation 中:

- #1 conservative 默认 — baseline (v1.2 已有)
- #2 `# guard:ack` escape — baseline (v1.2 已有)
- #3 regex 修需 minor bump + changelog — 流程约束 (硬)
- **#5 跨项目 smoke** — **ship gate** ✅
- #4 aria-doctor self-test 子命令 — defer v1.24.x

### Q2 ship gate path

| 方案 | 工作 | 状态 |
|------|------|------|
| P1 严格: Aria + SilkNode + Aether 全过 | +1-3 天 wait Aether owner | ❌ |
| **P2**: Aria + SilkNode ship gate; Aether 7-天 post-ship dogfood | 不阻塞本 cycle | ✅ |

### Q3 — Source-of-truth

| 方案 | SOT 位置 | 状态 |
|------|---------|------|
| **A** | aria-plugin SOT | ✅ 推荐 + 已锁 |
| B | SilkNode SOT (subtree pull) | ❌ 维护负担高 |
| C | standards/hooks/ 新增 executable | ❌ scope 漂移 |

---

## §4 Q1 实证证据 (本 session 跑出)

**实验设置** (本 session ~2026-05-22 早段, /home/dev/Aria):

1. plugin hook (`${CLAUDE_PLUGIN_ROOT}/hooks/handoff-location-guard.sh`) + project hook (`.claude/scripts/secret-guard.sh`) 各注入一行 marker:
   `echo "$(date +%s%N) <SOURCE> pid=$$" >> /tmp/hook-merge-test.log`
2. 触发: `Write /tmp/test-merge-canary*.txt` (普通路径, 两 hook matcher 均匹配 Write)
3. Block 测试: 注入 `if [[ -f /tmp/<marker> ]]; then exit 2; fi` 在两个 hook, 通过 marker 文件控制

**5 trials 一致结果** (摘):

```
Trial 1 (no-block Write):
  1779381960336757847 PROJECT pid=3329322
  1779381960370589044 PLUGIN  pid=3329335   ← 34ms gap, sequential
  → file created (both pass-through)

Trial 2 (plugin exit 2):
  1779382016900647419 PROJECT pid=3332723
  1779382016925796385 PLUGIN  pid=3332731   ← 25ms gap, PROJECT 先跑完
  → file NOT created (plugin blocked)
  → stderr: [plugin-test] BLOCK

Trial 3 (project exit 2):
  1779382059995659475 PROJECT pid=3335312
  1779382060012220132 PLUGIN  pid=3335315   ← 17ms gap, PLUGIN 仍执行
  → file NOT created (project blocked)
  → stderr: [project-test] BLOCK
  → 决定性: PROJECT exit 2 后 PLUGIN 仍 fire ✅
```

**核心证据**: Trial 3 pid=3335312 PROJECT (exit 2) 后 17ms pid=3335315 PLUGIN 仍记录 marker → **non-short-circuit 模型确认**。

**收尾**: 两 hook 脚本完全还原 (`git status` clean), 测试 artifacts 清理。

---

## §5 最终选择

```yaml
spec_name: aria-secret-guard-plugin-default
spec_level: 3
scope: Mid
sot: A (aria-plugin)
ship_target: aria-plugin v1.23.0
close_issues:
  - Forgejo Aria #84
  - Forgejo Aria #107
ship_gate:
  baseline:
    - conservative_default       # v1.2 已有
    - guard_ack_escape           # v1.2 已有
    - regex_change_minor_bump    # 流程约束
  added:
    - cross_project_smoke (Aria + SilkNode)   # P2: Aether deferred
post_ship:
  - Aether 7-day dogfood
  - aria-doctor dual-install advisory (Mid scope 输出, owner 决定删本地 copy 时机)
  - v1.24.x: aria-doctor self-test 子命令 (#4)
known_limitations:
  - cat <script> && grep .env <script>  # false-positive, changelog only, 不修 v1.23.0
```

---

## §6 理由

1. **Q1 实证证据已锁** — all-fire + sequential + non-short-circuit, 任何"override/short-circuit"担忧消除。设计可放心让 plugin + project copy 共存
2. **SOT = aria-plugin (A)** — 安装 plugin → 自动获保护; standards 留给 prose convention 定位清晰
3. **Mid scope** — 装 + 检测二齿是最小可治理化范围 (引 §5.2 决议 §6.2 理由)
4. **P2 ship gate** — Aria + SilkNode 双源足以覆盖 blast radius; Aether 装 hook 是"从无到有", 即使发现 false-positive 也是新增 finding 而非 regression
5. **Known false-positive 不修** — `cat <script> && grep .env <script>` 模式 conservative regex 选择"宁可 over-block", 修将放宽 regex 引入新风险; changelog 显式 list 给 owner 已知 limitation 后, ack 路径足够

---

## §7 风险与缓解

| # | 风险 | 缓解 |
|---|------|------|
| R1 | Aether smoke 推后期发现 false-positive | 7-day deadline + v1.23.1 minor 放宽 regex (流程已有) |
| R2 | plugin v1.23.0 一旦 ship 全 consumer 自动激活 | conservative + ack + minor bump 三层 + post-ship monitor |
| R3 | guard:ack 滥用 | 已有 `~/.claude/logs/guard-bypass.log` audit; v1.24.x self-test 加滥用警报 |
| R4 | Aria 本地 copy 何时切到 (a) 删除 | aria-doctor advisory 报告; owner 后续 cycle 决 (本 Spec 不强制时间表) |
| R5 | Plugin SOT 后 SilkNode v1.2 漂移 | SilkNode owner 自决迁移; 短期 v1.2 与 plugin SOT 内容一致 (本次 cherry-pick 同源) |
| R6 | Rule #6 benchmark gate 满足 | aria-doctor 是 deterministic check skill, 走 structural substitute (unit tests + dogfood + atomicity guard) |

---

## §8 实施 timeline (单 cycle, ~5.5-8.5h)

| Phase | 步骤 | 工作量 |
|-------|------|--------|
| **A.1** | spec-drafter → proposal.md | ~1h |
| **A.2** | task-planner → tasks.md (Level 3) | ~30min |
| **A.3** | agent-router 分配 (mostly self) | 5min |
| **B.1** | branch create + worktree | 10min |
| **B.2** | implementation (cherry-pick + tests + aria-doctor) + dogfood | ~3-4h |
| **B.3** | Aria + SilkNode cross-project smoke | ~1-2h |
| **C.1** | commit batch (aria-plugin + standards) | 30min |
| **C.2** | 2 PR merge (Rule #8 pre-merge gate) + submodule re-bump | 1h |
| **D.1** | progress update (Aria 自身无 UPM, no-op) | 5min |
| **D.2** | archive spec → archive/ | 5min |
| **D.3** | handoff doc + 5+1 multi-remote push + Issue #84/#107 close + memory | 30-45min |
| **Post-ship** | Aether 7-day dogfood (gated by Aether owner) | (out-of-cycle) |

---

## §9 跨引用

- **Parent 决议**: [`2026-05-20-secret-rotation-during-m5-deploy.md`](2026-05-20-secret-rotation-during-m5-deploy.md) §5
- **Upstream source**: SilkNode PR #429 commit `8eef709` (secret-guard.sh v1.2 + secret-scan.sh + 251 self-tests)
- **本地 copy**: `.claude/scripts/secret-guard.sh` (~30KB) + `.claude/scripts/secret-scan.sh` (~18KB) + tests (251 cases, 251/251 PASS verified this session)
- **Forgejo Issues**: Aria [#84](https://forgejo.10cg.pub/10CG/Aria/issues/84) (Path 3 hook follow-up) + [#107](https://forgejo.10cg.pub/10CG/Aria/issues/107) (silknode framework default 提议)
- **Rule #6 substitute pattern**: memory `feedback_deterministic_structural_skill_rule6_substitute`
- **Convention 引用**: `standards/conventions/secret-hygiene.md` (本 Spec D 阶段 update)
- **Memory 新增**: `feedback_claude_code_hook_merge_all_fire.md` (Q1 实证沉淀, 见 §4)

---

**Created**: 2026-05-22
**Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7 (1M context)
**Brainstorm 时长**: ~1h (4 segments + Q1 实证 ~10min instrumented test)
**Status**: brainstorm CONVERGED, ready for A.1 spec-drafter

---

## §10 Post-spec audit outcome (2026-05-22)

A.1 spec-drafter executed and `openspec/changes/aria-secret-guard-plugin-default/` (proposal.md + tasks.md) created. Subsequent post_spec convergence audit (5 agents, 2 rounds, max_rounds=4) **converged at R2 with PASS_WITH_WARNINGS**:

- **R1**: 1 Critical (orchestrator-upgraded version conflict, §5.1 yaml predated v1.23.0 ship; actual target = **v1.24.0**) + 12 Major + 17 Minor across 5 agents
- **Rev1**: all R1 findings addressed; new sections: §Tool Matcher & Contract, §State Schema (5 primary + 2 sub-flags), §Ship Gate Fallback (P2/P2.5/P3 + 14-day Aether escalation), §Rollback Plan (4-row); broken memory ref removed; Rule #9 §2.3 frontmatter explicit
- **R2**: 5/5 agents PASS_WITH_WARNINGS, 5/5 ADDRESSED their R1 findings; 12 new Minor (cosmetic / impl-stage); 2 schema-bug Minor (handoff frontmatter enum non-compliance) **fixed inline post-R2**
- **Verdict**: converged (no oscillation, verdict improved), no R3 needed

**⚠ Note for downstream reference**: §5.1 `ship_target: aria-plugin v1.23.0` in this DEC is **historical/superseded**. Effective ship target = **aria-plugin v1.24.0** (since v1.23.0 was occupied by state-scanner-inline-carry-forward-surfacing Spec 2026-05-20). DEC is a record of decisions made at the brainstorm time; proposal.md is the authoritative SOT for ship target.

**Audit report**: `.aria/audit-reports/post_spec-R2-2026-05-22T141716-511Z-aria-secret-guard-plugin-default-orchestrator.md`
