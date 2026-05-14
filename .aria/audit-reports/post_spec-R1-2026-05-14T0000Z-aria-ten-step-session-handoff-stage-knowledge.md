---
checkpoint: post_spec
round: R1
timestamp: 2026-05-14T00:00Z
spec: aria-ten-step-session-handoff-stage
role: knowledge-manager
verdict: SCOPE_OK_WITH_MAJORS
converged: false
---

# Post-Spec R1 审计报告 — aria-ten-step-session-handoff-stage
## 角色: knowledge-manager

> **审计时间**: 2026-05-14T00:00Z
> **规范路径**: `openspec/changes/aria-ten-step-session-handoff-stage/`
> **轮次**: R1 (收敛轮 1/N)
> **审计焦点**: 文档结构、交叉引用、模板设计、方法论对齐

---

## 执行摘要

本规范整体思路清晰，5 层纵深防御架构完整，dogfood 证据充分（4 次实证）。发现 2 项 Major、3 项 Minor、2 项 Observation。Major 均可在 Phase B 前修正，不阻塞实施。核心问题：(1) 8 段模板有 1 个隐形章节缺失（memory entries），导致模板不完整；(2) Rule #9 延迟激活的论据缺乏对比基线（#7/#8 均在首次 ship 时直接激活，无观察期前例）。

---

## Critical 级别发现

无。

---

## Major 级别发现

### M1 — 8 段模板缺少 "memory entries" 章节，与实战 handoff 不一致

**文件**: `proposal.md` 第 28-29 行、`tasks.md` T2.1  
**证据**: 审阅 `docs/handoff/2026-05-13-us025-m5-phase-a-b1-done.md`，该文档含独立的 **"Memory entries (this session — 4 new)"** 章节（第 145-154 行），列出本 session 新增的 memory 条目及其主题。`docs/handoff/2026-05-09-session-handoff.md` 无此章节（该 doc 是 SilkNode 参考模板），但 Aria 自身 8 个 handoff 中最新的一个明确含此字段。

**问题**: 提案定义的 8 段骨架（§0-§7）不含 "本 session 新增 memory entries" 的标准位置。tasks.md T2.1 描述 `aria/templates/session-handoff.md` 的 8 段时同样无此段。若按此模板写 handoff，AI 在下 session 读 handoff 时将找不到本 session 沉淀的 memory 索引，形成知识断链。

**风险**: template 规范化反而降低了现有 Aria 实战 handoff 的信息密度。新模板若不含此字段，下游项目 handoff 质量低于 Aria 自身现有水准。

**建议**: 在 §4 教训 之后、§5 4 维度同步 之前，加入 **§4.5 memory entries（可选段，仅 AI session 时适用）**，或将其显式定义为 §5 或独立 §4b，以 optional 标记。tasks.md T2.1 模板 variables 列表中相应补充 `{memory_entries_count}` 和条目表。

---

### M2 — Rule #9 延迟激活论据存在逻辑不一致（无历史前例支撑）

**文件**: `proposal.md` 第 90 行、`tasks.md` T5.3  
**证据**: CLAUDE.md 规则 #7（secret-hygiene）与规则 #8（pre-merge gate）的历史显示——两者均在首个 ship cycle **同时**写入 CLAUDE.md 规则列表，未设 30 天观察期。`secret-hygiene.md` 标注 "Version 1.0.0, 2026-05-07"，同日 CLAUDE.md Rule #7 激活。Rule #8 同理（phase-c-integrator C.2.4 与 CLAUDE.md 规则同步）。

**问题**: 提案写道 "待 ship + 3 dogfood reuse + 0 漂移 30 天后激活，避免 rule churn"。但该项目没有任何先例说明规则在 ship 后需要观察期才升级为不可协商规则。Rule #7 和 #8 都是在首次 ship 时直接激活，而非延迟。提案声称延迟是"避免 rule churn"，但 session-handoff 规则有 4 次 dogfood 实证（比 #7/#8 的 2 次更充分），实际上反而满足比 #7/#8 更高的激活门槛。

**影响**: 30 天窗口期内若有 AI 漂移写 `.aria/handoff/`，Rule #9 未激活意味着 CLAUDE.md 无法引用权威规则，L1 hook 虽阻断但缺少 CLAUDE.md 级别的规范依据，造成 "enforcement 强于 policy" 的倒置。

**建议**: 两个方向二选一：
- **方向 A（推荐）**: 与 #7/#8 对齐，在 T5.3 中改为 **在 ship 时同步激活 Rule #9**，写入 CLAUDE.md 规则列表（同时在 CLAUDE.md 中引用 `standards/conventions/session-handoff.md`）。
- **方向 B（保留延迟，但须理由文档化）**: 在 proposal.md Out of scope 段和 T5.3 中补充一段解释 "为何此规则需要观察期而 #7/#8 不需要" 的论据（例如：session-handoff 有可选性，#7/#8 无）。若选方向 B，须同时在 CLAUDE.md 预留 Rule #9 桩的具体措辞草稿，并在 tasks.md 加一个验收标准 "CLAUDE.md 含 Rule #9 预留桩"。

---

## Minor 级别发现

### m1 — `§5 4 维度同步` 过于 Aria-内部化，下游项目适配性差

**文件**: `proposal.md` 第 28-29 行，`tasks.md` T2.1  
**问题**: "4 维度同步" 指 UPM / PRD / US / OpenSpec 四个 Aria 特有概念。SilkNode 等下游项目若无 UPM（Aria 自身也无 UPM，per memory `project_aria_no_runtime_upm`），此段要么为空要么需要改写。模板若不设条件，会对无 UPM 的项目产生误导。

**建议**: 在 T2.1 模板定义时将 §5 标注为 **"optional — 仅 UPM 项目适用"**，并提供无 UPM 场景的替代文字（例如 "无 UPM 项目可改为：本 session 影响的关键文档同步状态"）。同时在 `standards/conventions/session-handoff.md` §2 Template 结构中，对 §5 的可选性做明确标注。

---

### m2 — `standards/conventions/session-handoff.md` 结构缺少 "Source incidents" 节

**文件**: `tasks.md` T5.1  
**证据**: `standards/conventions/secret-hygiene.md` 含 **§8 历史 incidents** 表（文件第 269-274 行），列出 2 次真实事故日期/项目/命令/泄露规模/修复。这是 secret-hygiene.md 作为参考结构的核心特征之一。

**问题**: tasks.md T5.1 规划的 session-handoff.md 结构为 §1-§6，无 "Source incidents" 或 "历史案例" 章节。但提案 proposal.md 本身已有 4 次 dogfood 实证（第 8 行列出），这些实证是说服后续维护者"为何要有此规范"的关键证据，应固化到 convention 文档中。

**建议**: 在 T5.1 规划的 §6 References 之前加入 **§5.5 Source incidents**（或将其作为 §5 Migration 的 subsection），记录 4 次 dogfood 事件（SilkNode 2026-05-09 + Aria self 2026-05-13 ×3），与 secret-hygiene.md §8 结构对齐。

---

### m3 — CLAUDE.md `信息地图` 目录导航在 ship 后将缺少 handoff doc 条目（任务缺失）

**文件**: `tasks.md` 整体  
**证据**: `CLAUDE.md` 第 130-147 行的 `信息地图 → 目录导航` 代码块，目前无 `docs/handoff/` 或 `standards/conventions/session-handoff.md` 的条目。ship 后这两个路径成为重要的知识资产入口，但 CLAUDE.md 信息地图不会自动更新。

**问题**: tasks.md 中的 T5.3 只说 "不修改 CLAUDE.md Rule list"，但完全未提及更新 `信息地图` 表的需求。根据 AI-DDD 原则 #3（文档同步），若新增文档路径不在 CLAUDE.md 信息地图中，AI 在下次 session 做状态扫描时将无法通过 CLAUDE.md 发现这两个入口，影响可发现性。

**建议**: 在 tasks.md 中新增一个子任务（可归入 T5 或 T8），要求在 ship 时更新 CLAUDE.md `信息地图 → 目录导航`，加入：
```
├── Session Handoff → docs/handoff/latest.md (最新 session 交接文档)
└── Handoff 规范   → standards/conventions/session-handoff.md
```

---

## Observation 级别发现

### O1 — `handoff_drift` 规则优先级 1.9+ 的边界情形分析

**文件**: `proposal.md` 第 81 行，`tasks.md` T4.1  
**分析**: 提案指定 `handoff_drift` 优先级在 `audit_unconverged`（1.9）之下、`commit_only`（1.0）之上。对照 `RECOMMENDATION_RULES.md` 规则表，1.0-1.9 区间已有 14 条规则（commit_only → audit_unconverged），区间密集。

对三个假设场景验证：
- **场景 A**: `audit_unconverged=true` AND `handoff drift detected` → 按提案 priority，audit_unconverged（1.9）先触发，handoff_drift 作为次级提示。语义正确：审计未收敛是更紧迫的流程问题，先处理。
- **场景 B**: 干净状态 + handoff drift → 无其他规则触发，handoff_drift 以最高优先级显示。语义正确：只剩一个问题时，直接显示。
- **场景 C**: `resume_in_progress_us`（1.88）AND `handoff drift` → resume_in_progress_us（1.88）先触发。语义略有争议：in_progress US 是"做什么"，而 handoff drift 是"位置错了"。两者不互斥，handoff drift 作为附加警告（non_blocking: true）可能更合适。

**建议**: tasks.md T4.1 中补充说明 `handoff_drift` 是 `non_blocking: true`（同 audit_unconverged），不阻断主推荐，仅作附加提示。若当前设计为 blocking，场景 C 中会错误阻断正常工作流推荐。

---

### O2 — skill 数量声明存在内部不一致，需 ship 前对齐

**文件**: `tasks.md` T8.6  
**证据**: 
- T8.6 写 "30 → 30 user-facing"（无变化）。
- `aria/README.md`（当前 v1.20.0）声明 "31 user-facing Skills + 6 internal + 11 Agents"（README 顶部描述行），但紧接着又写 "### Skills (30 user-facing + 6 internal = 36 total)"（细节列表行）。
- 实际 `aria/skills/` 目录中有 32 个 user-facing skills（38 总计 - 6 internal = 32）。
- `CLAUDE.md` 第 409 行：`v1.19.0 (aria-plugin, 30 user-facing + 6 internal Skills + 11 Agents)` — 已落后于 v1.20.0 现实。

**问题**: 当前 README 和 CLAUDE.md 自身已存在 skill 数量不一致（30 vs 31 vs 32）。T8.6 直接写 "30 → 30" 会固化现有错误。此外，新增的 `collectors/handoff.py` 是收集器模块，不是独立 skill；phase-d-closer D.3 是现有 skill 的步骤扩展，也不是新 skill。因此 v1.21.0 确实不新增 user-facing skill，但数字本身需要先经 audit 确认。

**建议**: T8.6 中的 "30 → 30" 改为 "维持 N → N（实际数量以 `ls aria/skills/ | wc -l` 减去 6 internal 为准）"，并作为 ship 前检查点验证 README + CLAUDE.md 中 skill 数字的一致性。这是 README 同步问题的副作用，建议与 readme_outdated 规则联动修复。

---

## Verdict

**SCOPE_OK_WITH_MAJORS**

规范范围合理，5 层 enforcement 架构完备，dogfood 证据充分。2 项 Major 可在 Phase B 前修正：M1 要求模板补充 memory entries 章节，M2 要求厘清 Rule #9 激活时机逻辑（或补充延迟理由文档）。3 项 Minor 均为文档质量改进，不阻塞实施但应在 Phase B 完成前纳入对应任务。

---

## 收敛投票

- **R1 结论**: NOT_CONVERGED（存在 2 Major 需 spec 作者确认处置方向后进入 R2）
- **投票**: 需要 R2（Major M1 spec 改动 + Major M2 方向选择 → 修改 proposal.md 和 tasks.md 后重审）
- **R2 预期收敛条件**: M1 模板段落补充完整 + M2 选定方向并在文档中体现 + m3 任务新增 → R2 应达到 SCOPE_OK

---

*审计人: knowledge-manager | 基于 CLAUDE.md AI-DDD 方法论*
