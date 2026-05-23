# aria-secret-guard-plugin-default

> **Level**: Full (Level 3 Spec)
> **Status**: Draft (Rev1, post R1 audit)
> **Created**: 2026-05-22
> **决策来源**: [DEC-20260522-001](../../../.aria/decisions/2026-05-22-aria-secret-guard-plugin-default-brainstorm.md), Parent: [2026-05-20-secret-rotation-during-m5-deploy §5](../../../.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md)
> **Ship target**: aria-plugin v1.24.0

---

## Why

2026-05-20 M5 T-deploy Phase B, Aria 自身**第二次** Rule #7 leak: `nomad var get -out=json` 把 8-key Items map (含 5 个 secret 值) 全打印到 chat transcript → 触发紧急 5-key rotation + secret-guard hook 紧急 cherry-pick 到 Aria 本地。

Layer 3 决议 (parent DEC §5): 把已在 SilkNode 实战验证的 secret-guard hook (v1.2, 2 轮 audit + 251 self-tests) 提升为 aria-plugin **默认安装**, 让所有 aria-plugin consumer (Aria/SilkNode/Aether/truffle-hound 等) 自动获得 LLM-readable secret leak 防护, 不再需要逐项目 manual install。

**核心论据 (parent DEC §6.1)**: ROI 已 inverted — 同 root cause 3 次复现 (Aria self ×2 + truffle-hound ×1), 继续 deferral 的"省 30min owner time"不再合理; framework default-on 的 onboarding 价值 + 跨项目复用价值远超实施成本。

## What

aria-plugin v1.24.0 ship:

1. **Plugin-level PreToolUse + PostToolUse hook** — cherry-pick SilkNode PR #429 v1.2 secret-guard.sh + secret-scan.sh 到 `aria/hooks/`, 注册到 `aria/hooks/hooks.json` 的 PreToolUse + PostToolUse (matcher 详见 §Tool Matcher & Contract)
2. **aria-doctor dual-install advisory** — 新增 `check_secret_guard_install()` function 检测项目本地 `.claude/scripts/secret-guard.sh` 状态, 输出 5 primary states (详见 §State Schema for aria-doctor)
3. **Convention update** — `standards/conventions/secret-hygiene.md` 新增 Layer 2 enforcement 段 + Path↔Layer terminology mapping (§3 task), 引用 plugin SOT 路径, 说明老项目本地 copy 与 plugin coexist 模式

### Key Deliverables

- `aria/hooks/secret-guard.sh` + `secret-scan.sh` (cherry-pick from SilkNode v1.2 commit `8eef709`)
- `aria/hooks/tests/secret-guard.test.sh` + `secret-scan.test.sh` (port 251 pure-bash self-tests, 0 bats 依赖) + 1 path-resolution test (verify `${CLAUDE_PLUGIN_ROOT}` substitution)
- `aria/hooks/hooks.json` (新增 PreToolUse + PostToolUse 4 个 hook entry)
- `aria/skills/aria-doctor/SKILL.md` (新增 `check_secret_guard_install()` function + 5-state output schema)
- 5+1 SOT bump v1.23.0 → v1.24.0:
  - `aria/.claude-plugin/plugin.json` (version 真理来源)
  - `aria/.claude-plugin/marketplace.json` (version + plugins[].version)
  - `aria/VERSION` (人类可读快照)
  - `aria/CHANGELOG.md` (新增 [1.24.0] 段, 显式列已知 limitation 全集)
  - `aria/README.md` (version + Skills count + hooks count)
- `standards/conventions/secret-hygiene.md` (Layer 2 enforcement update + Path↔Layer mapping)
- Forgejo 关闭: Aria Issue [#84](https://forgejo.10cg.pub/10CG/Aria/issues/84) + [#107](https://forgejo.10cg.pub/10CG/Aria/issues/107); SilkNode PR #429 reference comment (上游 archived 标记)

## Tool Matcher & Contract (R1 audit M1 + M2 closure)

### PreToolUse — secret-guard.sh

| Matcher | Behavior | Exit semantics |
|---------|----------|----------------|
| `Bash` | command-pattern scan (risky_patterns) | exit 2 = block; exit 0 = allow |
| `Read \| Edit \| Write \| MultiEdit` | file_path-pattern scan (.env / id_rsa / .pem / secrets/ etc.) + content scan on Write/Edit pre-image when applicable | exit 2 = block; exit 0 = allow |
| `NotebookEdit` | **不注册** (v1.24.0 决定 — defer 到有实际场景再加; .ipynb cell 多用于实验代码, 内联 secret 概率低 + ack 路径已足够) | N/A |

v1.2 上游脚本 case statement 已覆盖 `Bash` + `Read|Edit`。**Write / MultiEdit 实际行为**: case 落入 default (exit 0 pass-through) — 即 PreToolUse 在 Write/MultiEdit 上目前不主动 block, 仅占注册位 (与 PostToolUse 配对触发)。后续 minor 可加 Write 内容扫描。

### PostToolUse — secret-scan.sh

| Matcher | Behavior | Exit semantics |
|---------|----------|----------------|
| `Bash \| Read \| Edit \| Write \| MultiEdit` | output/content scan + REDACT secret values in tool_response (mutating) | **exit 0 always** (warn-only, never block retroactively) |

**Contract**: PostToolUse 是 **read-modify-write** of tool_response — fail-open semantics by design (执行已完成, exit 2 不能 retroactively block)。stderr REDACTED summary 给操作者 audit signal; tool result 已被改写 (secret 值 replaced)。

### Q1 evidence boundary (R1 audit M8 + T8 closure)

DEC §4 实证覆盖: PreToolUse on Write event。Bash PreToolUse 与 PostToolUse 行为 **由 Claude Code 同一 hook orchestrator 处理**, all-fire + non-short-circuit 模型按 hook spec 适用于所有 PreToolUse 事件 (not just Write)。Bash 高频场景 overhead 单次 sub-shell launch + jq parse ~17-34ms 与 Write 同量级 (跨项目 dogfood §5.1 will measure p95)。Performance budget: p95 hook overhead < 100ms per event (单次 sub-shell + script 执行预期 < 50ms;100ms gives 2x headroom)。

## State Schema for aria-doctor (R1 audit M3 + T1 closure)

`check_secret_guard_install()` 输出: `{ state: <primary>, sub: <optional flags> }`

| state | 含义 | sub flags (optional) |
|-------|------|---------------------|
| `not_installed` | 既无 `${CLAUDE_PROJECT_DIR}/.claude/scripts/secret-guard.sh` 也无 plugin hook 注册 (=不可能 since plugin default-on, 仅作 hypothetical complete) | `plugin_load_failed` |
| `single_plugin` | 仅 plugin hook 活跃, 无项目本地 copy | (none) |
| `single_local` | 仅项目本地 copy + `.claude/settings.json` 注册, plugin hook 未加载 | (异常状态, advisory: "plugin 未加载?") |
| `dual_install` | plugin + 项目本地 copy 并存 (本 Spec 后 Aria/SilkNode 的预期状态) | `stale_local_version` (本地 < plugin SOT 版本), `divergent_content` (sha 不一致) |
| `corrupted_settings` | `.claude/settings.json` 解析失败 / hook 注册条目 malformed | (mutually exclusive with above) |

**Sub-status detection**: stale-version 通过 `${PROJECT_DIR}/.claude/scripts/secret-guard.sh` 顶部 banner version 解析 (v1.2 已有), 与 plugin SOT 比较; divergent_content 通过 SHA256 对比。

**Schema backwards-compat guarantee**: 后续 minor 仅可 **append** sub flags, 不可重命名 primary state (Rule #6 atomicity guard per memory `feedback_deterministic_structural_skill_rule6_substitute`)。

## Hook Merge Semantics (Q1 实证, 本 Spec 设计前提)

本 brainstorm session 跑 instrumented test (两 hook 各注入 marker + 文件 toggle 控制 exit 2), **5 trials 一致结果**:

| 维度 | 实证结果 | 设计含义 |
|------|---------|---------|
| 同事件多源 hook 触发 | **All-fire** (project + plugin 都跑) | Plugin SOT + 项目本地 copy 共存可行, 双重防线生效 |
| 触发顺序 | project-level → plugin-level, **~17-34ms gap (sequential)** | overhead 可忽略 (sub-shell launch cost), 不并行 |
| Exit 2 是否短路后续 hook | **不短路** (前面 hook exit 2 后, 后续仍执行) | 设计 block 策略不能依赖前置 hook short-circuit; 任一 exit 2 即整体 block |
| Block reporting | 仅 stderr 显示触发 block 的那个 hook 路径 | 用 `$CLAUDE_PROJECT_DIR/...` vs `${CLAUDE_PLUGIN_ROOT}/...` 区分 source |

详见 [DEC §4](../../../.aria/decisions/2026-05-22-aria-secret-guard-plugin-default-brainstorm.md)。结论沉淀为 memory `feedback_claude_code_hook_merge_all_fire`。

**实证边界 (R1 audit QA F6)**: 实验 plugin hook 用 `handoff-location-guard.sh` 作 proxy (而非未来的 plugin secret-guard.sh)。结论对 **Claude Code hook orchestrator merge 语义** 适用; secret-guard.sh 自身行为由 251 self-tests + §5 dogfood 覆盖。

## Impact

| Type | Description |
|------|-------------|
| **Positive — 默认保护** | 所有装 aria-plugin 的 consumer 项目 (Aria/SilkNode/Aether/truffle-hound 等) ship 后自动获 LLM secret leak 防护;不再 per-project install。新项目 onboard 一次性受益。 |
| **Positive — Lab 标准化** | secret-hygiene Rule #7 从纯 prose convention 升级为 mechanical enforcement (Layer 2), 与 Rule #9 handoff defense-in-depth 模式一致 |
| **Risk — Blast Radius** | Plugin-level hook 一旦 ship → 全 consumer 自动激活。1 false-positive 影响所有项目。**Mitigation**: (1) conservative 默认 (v1.2 baseline); (2) `# guard:ack <reason>` one-shot escape; (3) regex 修改强制 minor bump + changelog 显式说明 "放宽 X pattern"; (4) **ship gate**: Aria self + SilkNode 跨项目 smoke (Q2 P2); (5) Aether 7-天 post-ship dogfood + escalation deadline (见 §Ship Gate Fallback); (6) post-ship Aria daily 操作累积 monitor |
| **Risk — Dual Install** | 既装项目 (Aria/SilkNode 本地 copy) 与 plugin 双跑。Q1 实证: all-fire + sequential + non-short-circuit, 无冲突, ~17-34ms/event overhead。**风险**: 两版不同步时双重 block message 可能困惑 owner。**Mitigation**: aria-doctor 5-state advisory (含 `stale_local_version` / `divergent_content` sub flags) + owner 后续 cycle 决定 cleanup 时机 |
| **Risk — Known False-Positive / False-Negative** | v1.24.0 ships with documented known-limitations (CHANGELOG.md [1.24.0]): (a) `cat <script> && grep .env <script>` false-positive (parent DEC §4.3); (b) log-file grep absent from risky_patterns false-negative (parent DEC §2.6); **(c) Bash `cat\|head\|tail <key-file>` false-negative — NEW from TASK-007 dogfood 2026-05-23** (Bash matcher regex covers SSH-wrapper key-file reads but not local cat key-file; Read/Edit matcher does catch the same paths). Workarounds available: Read tool / secret-scan PostToolUse REDACT / `# guard:ack:`. v1.25.x roadmap: regex extension for (c). Owner triage: smoke-evidence.md §3.1 F2 = Accept-as-new-known-limit. |
| **Risk — Aether 未在场** | Q2 ship gate path P2: Aether owner 不可用时 ship 不阻塞, deferred 7-天 post-ship dogfood。**风险**: post-ship 才发现 false-positive。**Mitigation + 硬 deadline**: 14 天 post-ship 若 Aether dogfood 仍未跑 → 由 Aria owner 主动 stand-in (跑 Aether daily-use 通用集合 §5.1 + 加 Aether 项目特有 `nomad ssh` / `aether ci status` 等 3-5 命令);v1.24.1 minor 流程已就绪 (规则 #3) |
| **Risk — PR Rollback** | aria-plugin PR 通过 Rule #8 gate 后 merge, 但 push 阶段 / 跨远程同步 fail → standards PR 已 merge 形成 forward reference。**Mitigation**: 见 §Rollback Plan |
| **Performance Budget** | p95 hook overhead < 100ms per tool event (单次 sub-shell launch + jq parse 预期 < 50ms, 2x headroom); §5.1 dogfood capture timing |

## Ship Gate Fallback Paths (R1 audit M6 + M7 closure)

### SilkNode owner 不可用 (M6)

- **P2 默认** (Spec lock): Aria + SilkNode smoke 双跑 = ship gate
- **P2.5 降级** (SilkNode owner 7 天内无法提供 daily-use 命令集): Aria smoke pass + SilkNode 改为 7-天 post-ship dogfood (与 Aether 对称)
- **P3 紧急** (Spec 起 14 天 SilkNode + Aether 双双未跑): Aria owner stand-in (跑两项目通用集合 + 各加 3-5 项目特有命令); 记录到 smoke-evidence.md `mode: owner_stand_in`

### Aether 7-天 post-ship 未跑 (M7)

- **Day 0-7**: 等 Aether owner, 0 escalation
- **Day 8-14**: Aria owner 提醒 + advisory comment 在 Forgejo Issue #107
- **Day 14+**: Aria owner 主动 stand-in (跑通用 ~10 命令 + Aether 特有 3-5);若仍有阻碍 → 升级到 Aria session OD 决"接受未验证 ship 或回滚 v1.24.0"

## Rollback Plan (R1 audit M4 closure)

| 失败点 | Rollback 动作 | 数据完整性 |
|--------|--------------|-----------|
| aria-plugin PR Rule #8 gate fail | standards PR 已 merge → 回滚 standards PR (revert commit) 到 pre-spec state | 可逆 (prose-only change) |
| aria-plugin PR 已 merge, 单远程 push fail | 重试 push (per memory `feedback_release_phase_d_5_files_synchronization`); 若 SHA 始终不一致 → revert aria-plugin merge commit + revert standards | 可逆 (在 SHA 不一致前) |
| Plugin v1.24.0 ship 后 critical false-positive (跨多 consumer 大面积 block daily) | v1.24.1 minor 紧急放宽 regex (24-48h 内); 若不可控 → v1.24.2 改 hooks.json 改 opt-in (PR 已就绪 template) | 不可逆 (consumer 已升级);仅 forward-fix |
| 灾难性 (整套设计有缺陷) | revert plugin SOT, 各项目回到本地 copy 模式 (= 当前 Aria 状态) — Aria/SilkNode 本地 copy Q1-b 保留作 fallback | 灾难情况下保有过渡态 |

## Tasks

详见 [tasks.md](./tasks.md)。8 phases, ~5.5-8.5h 单 cycle (不含 §8 post-ship Aether dogfood)。

## Success Criteria

- [ ] **Unit tests**: 251 ported tests 全 PASS (207 guard + 44 scan, 与本 session local verify 一致) + 1 新增 `${CLAUDE_PLUGIN_ROOT}` path-resolution test PASS
- [ ] **aria-doctor**: `check_secret_guard_install()` 5-state schema 输出正确 (本 §State Schema), unit tests 5 cases (1 per primary state) + sub-flag detection 2 cases (stale_local_version + divergent_content) PASS
- [ ] **Performance**: p95 hook overhead < 100ms per tool event (§5.1 dogfood timing capture)
- [ ] **Aria self dogfood**: ~10 daily-use commands smoke, 0 unexpected false-positive (known limitation 全集除外, §smoke-evidence.md rubric)
- [ ] **SilkNode dogfood**: ~10 daily-use commands smoke (P2 default), 或 P2.5/P3 fallback per §Ship Gate Fallback;0 unexpected false-positive
- [ ] **smoke-evidence.md**: 完整 (schema 见 tasks.md §5.3); 标注 mode: `owner_provided` | `owner_stand_in` | `deferred_post_ship`
- [ ] **post_implementation audit**: PASS (convergence mode, 5-agent team locked: tech-lead + backend-architect + qa-engineer + code-reviewer + knowledge-manager — same as post_spec)
- [ ] **pre_merge audit + Rule #8 gate**: PASS + `aether ci status --branch main --in-flight --json` clean (or fallback per `.aria/config.json` `phase_c_integrator.pre_merge_gate.no_aether_fallback`)
- [ ] **3-way SHA parity**: aria-plugin + standards + Aria main 跨 origin/github 全绿 post-merge
- [ ] **Issue close**: Forgejo Aria #84 + #107 close-by-PR with commit hash comment + Q1 evidence summary + aria-doctor 检测命令示例; SilkNode PR #429 reference comment
- [ ] **CHANGELOG**: [1.24.0] 段含 known limitation **全集** 显式 list (`cat && grep .env` false-positive + log-file grep false-negative)
- [ ] **Handoff + memory**: D.3 handoff doc (Rule #9 §2.3 frontmatter: track-id=`aria-secret-guard-plugin-default`, owner-container=<container-id>, phase=D.3, status=done, updated-at=ISO timestamp) + 确认 `feedback_claude_code_hook_merge_all_fire` 已 indexed
- [ ] **Rollback SLA**: v1.24.1 minor response window ≤ 48h post-detection of critical false-positive (per §Rollback Plan)

## Out of Scope (defer to future cycles)

- **aria-doctor self-test 子命令** (实际跑 hook 对项目典型命令 sanity check) — defer aria-plugin **v1.25.x** (Q2 mitigation #4)
- **PreToolUse Write 内容扫描** — 当前 v1.2 case statement Write 落入 default (pass-through), 后续 minor 可加 Write pre-image 扫描 (Q4 candidate)
- **跨项目 rollout playbook + governance chart** (Aria/SilkNode/Aether/truffle-hound 统一迁移流程) — Full scope, defer 长期目标
- **SilkNode v1.2 本地 copy 主动迁移** — 由 SilkNode owner 自决 (aria-doctor advisory 输出建议, 不强制)
- **Aria self `.claude/scripts/secret-guard.sh` 删除** — 由 aria-doctor advisory 报告 + owner 后续 cycle 决 (Q1-b 决议: 保留过渡期)
- **Aether daily-use command smoke (Day 0-13)** — ship gate path P2: 推后 7-天 post-ship dogfood, gated by Aether owner availability;Day 14+ Aria owner stand-in (见 §Ship Gate Fallback)
- **v1.24.0 内修 known false-positive (`cat && grep .env`)** — changelog only, ack 路径足够
- **PostToolUse retroactive block** — 设计上 exit-0-always, scan + REDACT only;真正 retroactive block 需要 LLM context revoke (out of Claude Code hook spec)

## References

- **DEC**: [2026-05-22 brainstorm](../../../.aria/decisions/2026-05-22-aria-secret-guard-plugin-default-brainstorm.md) (Q1/Q2/Q3 收敛 + Q1 实证 5 trials)
- **Parent DEC**: [2026-05-20 §5 Layer 3 决议](../../../.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md)
- **Upstream source**: SilkNode PR #429 commit `8eef709` (v1.2, 2 轮 audit + 251 self-tests)
- **Local cherry-pick**: `.claude/scripts/secret-guard.sh` + `secret-scan.sh` + tests (本 session local verify 251/251 PASS)
- **Forgejo Issues**: Aria [#84](https://forgejo.10cg.pub/10CG/Aria/issues/84) Path 3 hook follow-up + Aria [#107](https://forgejo.10cg.pub/10CG/Aria/issues/107) silknode framework default 提议
- **Convention**: `standards/conventions/secret-hygiene.md` (Rule #7, 本 Spec D 阶段 update + Path↔Layer mapping)
- **Memory**: `feedback_claude_code_hook_merge_all_fire` (Q1 实证, indexed), `feedback_deterministic_structural_skill_rule6_substitute` (aria-doctor SKILL 改动 Rule #6 substitute pattern, indexed), `feedback_release_phase_d_5_files_synchronization` + `feedback_sequenced_multirepo_gitlink_bump` (ship 流程)
