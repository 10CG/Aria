# M7 Sub-Spec #1 Tasks — Agent Lifecycle Management (下行 pull 半环 MVP)

> **Spec**: [aria-2.0-m7-agent-lifecycle](./proposal.md)
> **Level**: 3 (Full)
> **Status**: ✅ **Approved** (owner sign-off 2026-06-18; post_spec R1→R2 CONVERGED; Phase A.3 agent 分配 LOCKED 2026-06-19 (见 §Phase A.3)。Phase B 受 D3 时机门 — M6 release-closeout ship 后)
> **Created**: 2026-06-18
> **Brainstorm Source**: [.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md](../../../.aria/notes/2026-06-16-agent-lifecycle-management-for-aria-fleet.md) (§1/§2/§3/§7; owner 逐段确认 2026-06-16) + D1-D6 上游 (2026-05-27)
> **Estimated total**: ~24h impl (单一 SoT; 与 proposal §Effort baseline 一致: TG-A ~6h + TG-B ~10h + TG-C ~4h + T-docs ~2h + ~2h buffer)
> **Agent allocation (Phase A.3 LOCKED 2026-06-19)**: 见下 §Phase A.3 — Agent Allocation。无需新建 agent (现有 aria-plugin roster 覆盖)。

---

## Task Group Overview

| Group | Topic | Scope ref | Est |
|-------|-------|-----------|-----|
| TG-A | 集合库骨架 (git repo layout + index + seed agents + L2 config 注入) | §What TG-A + AD-M7-1 | ~6h |
| TG-B | 推荐 + 加载 orchestrator (复用 4 Skill + 物化双层 + lockfile + 重启提示) | §What TG-B + AD-M7-2 | ~10h |
| TG-C | 更新-基础版 detector (semver 比较 + 三档提示, 不自动覆盖) | §What TG-C + AD-M7-3 | ~4h |
| T-docs | 文档 (SKILL.md / config schema / CLAUDE.md 信息地图 / standards 引用) | §Constraints + 信息地图 | ~2h |

**依赖**: TG-A → TG-B (推荐/物化读库) → TG-C (更新读 lockfile + index)。T-docs 末尾。

---

## Phase A.3 — Agent Allocation (LOCKED 2026-06-19)

> 现有 aria-plugin agent roster 完全覆盖本 Spec 任务类型, **无 coverage gap, 无需新建 agent**。**meta-note**: 本 Spec 实施的正是"agent 生命周期管理"能力本身, 但其 Phase B 实施仍用现成 plugin agent (非本 Spec 产出的集合库 agent — 那是 ship 后才有的产物)。Phase B 由 subagent-driver 按下表 dispatch。

| Task Group | Primary Agent | 协同 | 分配理由 (capability match) |
|------------|---------------|------|------------------------------|
| TG-A 集合库骨架 (git repo layout + index + seed + L2 config) | `aria:backend-architect` | — | 目录契约 + index schema + L2 注入边界 = 系统/数据建模 |
| TG-B 推荐+加载 orchestrator (核心新件) | `aria:backend-architect` | `aria:qa-engineer` (AC + dogfood) | 编排 4 Skill + 物化双层 + lockfile 原子写 = 后端核心; 物化/lockfile 测试 = QA |
| TG-C 更新-基础版 detector | `aria:backend-architect` | `aria:qa-engineer` (三档处置单测) | semver 比较 + 三档处置逻辑 + 只读断言 |
| T-docs (SKILL.md / config schema / 信息地图) | `aria:knowledge-manager` | — | SKILL.md progressive-disclosure + 文档结构 = 知识管理 |
| 跨切架构评审 (AD-M7-1/2/3 + 三层映射 + session-start caveat) | `aria:tech-lead` | — | 集合库/lockfile/物化去 metadata 三决策评审 (Phase B kickoff) |
| Phase B post-implementation review | `aria:code-reviewer` | — | 规范合规 + 代码质量两阶段审查 |

**分工原则** (memory `feedback_agent_team_dynamic_workflow_division`): 强依赖/零回归核心 (物化 orchestrator + lockfile + detector) 主 loop 亲自边验 (memory `feedback_verify_edit_landed_grep_count`); 文档 (T-docs) + 单测交 workflow agent 并行 (disjoint 文件集)。

---

## TG-A — 集合库骨架 (~6h)

- [ ] A-scaffold-1 (~1h) 定义集合库目录契约 (AD-M7-1): 建 `<collection-repo>/` 骨架 (MVP 可先在 `aria-orchestrator/extensions/aria-fleet/registry/` 或独立 repo, 经 L2 config 指向)。布局: `registry-index.yaml` + `agents/<name>/{agent.md, VERSION}` + `README.md` (上行 ⑤⑥ M7+ 占位说明)。**deps**: 无。
- [ ] A-index-2 (~1.5h) 实现/手写 `registry-index.yaml` (schema_version "1"; agents[]{name,version,capabilities,scope,path})。`capabilities[]` 标签**全部**来自 `aria/references/capabilities-taxonomy.yaml` 既有词表 (grep 验证每个标签存在)。**deps**: A-scaffold-1。
- [ ] A-seed-3 (~1.5h) 填 L1 通用种子 agent (5 个真实存在的语言/框架无关 agent): 从 `aria/agents/{backend-architect,code-reviewer,qa-engineer,api-documenter,tech-lead}.md` 复制 STCO+capabilities frontmatter 进 `agents/<name>/agent.md` + 各写 `VERSION`=1.0.0。**deps**: A-index-2。
- [ ] A-config-4 (~1h) L2 注入契约: 定义 `.aria/config.json` `agent_lifecycle.registry.{repo, branch, local_cache_path}` schema (D5 模式); L1 读取代码只认抽象 `local_cache_path`, **零** repo 地址 hardcode。**deps**: A-scaffold-1。
- [ ] A-test-5 (~1h) **Rule #6 substitute** (deterministic, structural fixture + unit test):
  - **AC-A1**: index YAML-parse + 每个 `agents[].path` 文件存在 + 每个 capability ∈ taxonomy。
  - **AC-A2**: `grep -rE 'forgejo\.10cg|10cg\.pub|simonfishgit|aria-workspace'` over L1 code/index 返回空 (L1 零 10CG hardcode)。
  - **deps**: A-index-2, A-seed-3, A-config-4。

---

## TG-B — 推荐 + 加载 orchestrator (~10h)

- [ ] B-skel-1 (~1h) 建新 Skill `aria/skills/agent-lifecycle/SKILL.md` 骨架 (或 Phase B step): description + 使用场景 + 前置 (config + cache 存在)。声明**复用** 4 Skill, 不重实现 (CAVEAT #1)。**deps**: TG-A 全。
- [ ] B-recommend-2 (~2h) ①推荐合成 (TG-B.1 第 3 步, 新逻辑):
  - 读 `.aria/coverage-report.yaml` `gaps[].required_capabilities` (既有 gap-analyzer 输出, **不重算 gap**)。
  - 对每个 gap 在 `registry-index.yaml` 查标签覆盖率最高的库 agent (复用 match_rate = matched/required 语义, ≥0.5 入选)。
  - 输出推荐清单 (owner 确认 gate)。**明确标启发式** (routing prior-art 弱, memo §8 #1)。
  - **deps**: B-skel-1。
- [ ] B-materialize-3 (~3h) ②加载物化 orchestrator (AD-M7-2, 核心新件):
  - 拉选中 agent `agent.md` (从 cache)。
  - 写 source 层 `.aria/agents/<name>.md` (mkdir-if-absent, CAVEAT #2; 保留 capabilities; 复用 agent-creator 物化逻辑)。
  - 写 native 层 `.claude/agents/aria-<name>.md`: **剥离** capabilities/aria_managed/gap_source/audit_points, 纯 STCO frontmatter (CAVEAT #4)。`aria-` 前缀 (CAVEAT #9)。
  - **deps**: B-recommend-2。
- [ ] B-lockfile-4 (~2h) `.aria/agents-lock.yaml` 写入 (AD-M7-2, memo §3 #1):
  - schema_version "1" + agents[]{name,source,registry_version,local_modifications,materialized_at} + manifest_hash。
  - **原子写**: `.aria/agents-lock.yaml.tmp` → `os.replace()` (CAVEAT #8; concurrent-session-write-safety)。
  - 增量 (再次物化 merge 进既有 lockfile, 不覆盖无关条目)。
  - **deps**: B-materialize-3。
- [ ] B-reload-prompt-5 (~0.5h) "重启生效"提示 (CAVEAT #3 HARD REQUIREMENT, #145):
  - orchestrator 收尾 stdout: "agents materialized to .claude/agents/; restart Claude Code session for native subagent spawn (or use /agents reload / soft-injection pattern for same-session)" (不声称 agent-router 现成支持软注入, 见 proposal grounding 修正)。
  - **deps**: B-materialize-3。
- [ ] B-test-6 (~1.5h) **Rule #6 substitute** (deterministic, structural fixture + unit + dogfood):
  - **AC-B1**: 推荐链贯通 (fixture: project-profile + coverage-report + index → 推荐清单标签覆盖 ≥0.5)。
  - **AC-B2**: 物化双层 (source 留 capabilities; native 剥 capabilities + 无 aria_managed/gap_source/audit_points)。
  - **AC-B3**: lockfile YAML-parse + schema_version "1" + 每 name↔native 文件存在 + 原子写无 .tmp 残留。
  - **AC-B4**: 重启提示 stdout 字样存在。
  - **deps**: B-lockfile-4, B-reload-prompt-5。

---

## TG-C — 更新-基础版 detector (~4h)

- [ ] C-detect-1 (~1.5h) ④更新检测 (AD-M7-3, 基础版仅检测):
  - 对 lockfile 每个 `source==registry` agent: semver 比较 `registry_version` vs index `version`。
  - `<` → stale; `==` → up-to-date。detector **只读**, 不写任何文件 (CAVEAT: detector 不动 native/source)。
  - **deps**: TG-B 全 (读 lockfile + index)。
- [ ] C-triage-2 (~1.5h) 三档处置 (基础版仅提示):
  - up-to-date → 无动作。
  - stale + `local_modifications==false` → 提示"可重物化更新" (owner 确认走 TG-B 物化)。
  - stale + `local_modifications==true` → 提示"已分叉, 库已升级但本地改写; **不自动覆盖**, 请人工合并 (三方合并 = fast-follow, OOS-8)"。
  - **核心安全不变式**: MVP 绝不自动冲掉 `local_modifications==true` (memo §3 #2)。
  - **deps**: C-detect-1。
- [ ] C-test-3 (~1h) **Rule #6 substitute** (deterministic):
  - **AC-C1**: version `1.0.0` < index `1.1.0` → 报 stale。
  - **AC-C2**: `local_modifications==true` stale → 输出人工合并提示 + **断言无文件写** (detector 只读)。
  - **AC-C3**: version 相等 → 无 stale 提示。
  - **deps**: C-triage-2。

---

## T-docs — 文档 (~2h)

- [ ] D-skill-1 (~0.5h) `aria/skills/agent-lifecycle/SKILL.md` 正文 (progressive-disclosure, <500 行): ①推荐 ②加载 ④更新 流程 + 复用 4 Skill 表 + 重启 caveat + 软注入兜底说明。**deps**: TG-B/TG-C 全。
- [ ] D-config-2 (~0.5h) config schema 文档: `.aria/config.json` `agent_lifecycle.*` 字段说明 (L2 注入, 零 hardcode)。**deps**: A-config-4。
- [ ] D-claudemd-3 (~0.5h) CLAUDE.md 信息地图加 "agent 生命周期管理 (下行 pull 半环) → aria/skills/agent-lifecycle/" 一行 (additive)。**deps**: D-skill-1。
- [ ] D-dogfood-4 (~0.5h) **AC-D1 dogfood**: Aria sandbox 或测试项目跑完整 ①→②→④ 链 (物化 ≥1 agent + lockfile 落地 + 重启提示 + 模拟库升版 detector 报 stale); 证据存 Phase B 报告。**deps**: 全部前置。

---

## Precision Items

| P-N | Source (memo §) | §What 落点 | Task(s) |
|-----|-----------------|-----------|---------|
| P-1 | §1 #2/#3 (git repo NOT marketplace) | TG-A 机制锁定 + OOS-9 | A-scaffold-1 |
| P-2 | §1 #1 (对内通用 零 hardcode) | Constraints L1 + AC-A2 | A-config-4, A-test-5 |
| P-3 | §2 表 (复用 4 Skill) | TG-B.1 推荐链 | B-recommend-2 |
| P-4 | §3 #1 (lockfile 账本) | TG-B.3 + AD-M7-2 | B-lockfile-4 |
| P-5 | §3 #2 (更新不冲本地改写) | TG-C.2 三档 + OOS-8 | C-triage-2 |
| P-6 | §7 + #145 (重启生效 caveat) | TG-B.2 step5 + AC-B4 | B-reload-prompt-5 |
| P-7 | §7 (M7 第一刀 = 下行半环, 上行 DEFER) | Out of scope OOS-1..OOS-10 | (全 Spec 边界) |
| P-8 | §6 (deep-research 修正 = forward-context) | OOS-3/4/5 + Critical caveat | (全 Spec 边界) |

---

## Ordering Dependencies

```
TG-A (集合库骨架)
  A-scaffold-1 ──┬── A-index-2 ── A-seed-3 ──┐
                 └── A-config-4 ─────────────┴── A-test-5 (AC-A1/A2)
                          │
                          ▼
TG-B (推荐 + 加载)
  B-skel-1 ── B-recommend-2 ── B-materialize-3 ──┬── B-lockfile-4 ──┐
                                                  └── B-reload-prompt-5 ┴── B-test-6 (AC-B1..B4)
                          │
                          ▼
TG-C (更新-基础版)
  C-detect-1 ── C-triage-2 ── C-test-3 (AC-C1/C2/C3)
                          │
                          ▼
T-docs
  D-skill-1 ── D-config-2 ── D-claudemd-3 ── D-dogfood-4 (AC-D1)
```

**Parallel boundaries**: A-index-2/A-seed-3 链 与 A-config-4 可并行 (汇于 A-test-5)。B-lockfile-4 与 B-reload-prompt-5 可并行 (都依赖 B-materialize-3, 汇于 B-test-6)。TG-C 必须在 TG-B 全完 (读 lockfile)。

**Blocking conditions**: Phase B kick 前过 §Assumptions A-1..A-5 verify probe (4 Skill 契约未漂移 + taxonomy 词表可读 + config 可扩展)。

---

## Status

- Phase A.1: Draft 起草完成 (2026-06-18); 待 post_spec audit (R1...) + owner Approve。
- Phase B precondition gate: M6 ship 完成 (D3 时机锁: M7 AFTER M6); §Assumptions A-1..A-5 verify probe 全绿。
