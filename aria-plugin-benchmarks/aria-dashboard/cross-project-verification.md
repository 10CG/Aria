# aria-dashboard 跨项目数据解析可行性验证报告

> **任务**: T3 — 验证 aria-dashboard Skill 在两个项目上的数据解析可行性
> **验证日期**: 2026-03-27
> **验证者**: QA Engineer
> **技能版本**: aria-dashboard v1.0.0
> **数据 Schema**: aria/skills/aria-dashboard/references/data-schema.md

---

## 执行摘要

| 项目 | 看板生成可行性 | 可用数据源数 | 阻塞问题 |
|------|--------------|------------|---------|
| Aria (/home/dev/Aria) | **可行 (受限)** | 4 / 5 | UPM 格式不兼容 |
| Kairos (/home/dev/Kairos) | **可行 (受限)** | 3 / 5 | UPM 格式不兼容、Stories 格式偏差、Benchmark 缺失 |

两个项目均可生成看板，但 **UPM 区块在两个项目上都将显示"未配置"**，因为两个项目的 UPM 文档均未使用 Skill 要求的 HTML 注释格式 (`<!-- UPMv2-STATE ... -->`）。

---

## 项目 1: Aria (/home/dev/Aria)

### 数据源可用性检查

#### DS-1: UPM (项目进度总览)

| 检查项 | 结果 |
|--------|------|
| 文件是否存在 | MISSING — 无 `unified-progress-management.md`，Glob `**/unified-progress-management.md` 返回空 |
| UPM.md 替代文件 | 不适用 — Aria 项目根目录无 `UPM.md` |
| docs/ 目录内容 | `docs/` 包含 analysis/、architecture/、decisions/、requirements/、workflow/，无进度文件 |

**状态: MISSING**

**根因**: Aria 项目未创建 `unified-progress-management.md`。Skill 使用 Glob `**/unified-progress-management.md` 搜索，任何其他文件名都无法命中。

**容错行为**: 按 SKILL.md 规范，UPM 区块显示空状态 "No UPM document found. Run progress-updater to initialize."，不报错，不中断其余数据源解析。

---

#### DS-2: User Stories (三列看板)

| 检查项 | 结果 |
|--------|------|
| 路径存在 | YES — `docs/requirements/user-stories/` 存在 |
| 文件数量 | 5 个 US-*.md 文件 |
| ID 格式 | 符合 — `US-001.md` ... `US-005.md`，正则 `^(US-\d+)` 可提取 |
| Status 字段 | 符合 — 全部使用 `> **Status**: <value>` 引用块格式 |
| Priority 字段 | 符合 — 全部使用 `> **Priority**: <value>` 引用块格式 |
| 状态值映射 | done (3), in_progress (1), pending (1) — 全部在 Skill 的映射表内 |

**状态: AVAILABLE**

**三列预期分布**:
- 已完成 (Done): US-001, US-002, US-004
- 进行中 (In Progress): US-005
- TODO: US-003

---

#### DS-3: OpenSpec (活跃 + 归档)

| 检查项 | 结果 |
|--------|------|
| 活跃路径 | EXISTS — `openspec/changes/aria-dashboard/proposal.md` (1 个) |
| 归档路径 | EXISTS — `openspec/archive/*/proposal.md` (36 个) |
| 活跃 Spec 字段格式 | 符合 — Status/Level/Created/Parent Story 均为引用块格式 |
| 归档 Spec 字段覆盖率 | PARTIAL — 36 个中 23 个有完整 blockquote 字段，8 个完全缺失，5 个部分缺失 |
| 归档目录名格式 | 符合 — `YYYY-MM-DD-{name}` 格式，前 10 字符为有效日期 |
| 耗时计算可行性 | PARTIAL — 有 Created 字段的 28 个 Spec 可计算耗时，8 个无法计算 |

**状态: PARTIAL**

**缺失字段的归档 Spec 列表** (8 个):
- `2025-12-23-git-commit-convention` — 使用 `- **Status**:` 列表格式
- `2025-12-24-refactor-workflow-architecture` — 无标准字段
- `2026-02-06-version-standardization` — 无标准字段
- `2026-03-13-aria-plugin-benchmarks` — 使用 `- **Level**:` 列表格式
- `2026-03-19-aria-plugin-v1.7-enhancements` — 无标准字段
- `2026-03-19-strengthen-rule-6-enforcement` — 无标准字段
- `2026-03-21-readme-i18n-upgrade` — 使用 `## Level:` 标题格式
- `2026-03-27-aria-report-skill` — `## Level:` 标题格式，无 Created

**容错行为**: 字段缺失的 Spec 将显示 Duration = `--`，Status 显示 `Archived`（强制覆盖），其余正常展示，不中断。

---

#### DS-4: Audit Reports (审计历史)

| 检查项 | 结果 |
|--------|------|
| 路径存在 | YES — `.aria/audit-reports/` 存在 |
| 文件数量 | 1 个 — `post_spec-2026-04-01T23.md` |
| YAML frontmatter 格式 | 符合 — 包含 checkpoint/mode/rounds/converged/timestamp/context/agents |
| converged 字段 | `false (1 PASS / 3 REVISE, trend converging)` — 第一个单词为 `false`，解析为 REVISE |
| timestamp 字段 | `2026-04-01T23:00:00Z` — 合法 ISO 8601 格式 |

**状态: AVAILABLE**

**预期显示**: 1 条审计记录，verdict = REVISE，mode = convergence，rounds = 3。

---

#### DS-5: AB Benchmark (基准测试摘要)

| 检查项 | 结果 |
|--------|------|
| latest 路径 | YES — `aria-plugin-benchmarks/ab-results/latest/summary.yaml` 存在 |
| 日期目录路径 | YES — `aria-plugin-benchmarks/ab-results/2026-03-13/summary.yaml` 存在 |
| overall 区块 | 符合 — total_skills/with_better/mixed/equal/without_better/avg_delta/with_skill_win_rate 均存在 |
| results 区块 | 符合 — 28 个 skills，每个有 delta_pass_rate 和 verdict |
| 数据完整性 | 28 skills tested, avg_delta 字段在 summary 中可提取 |

**状态: AVAILABLE**

**注意**: `latest/summary.yaml` 存在且有效，Skill 应优先使用此路径（data-schema.md 中列为优先级 1）。

---

### Aria 项目看板生成可行性评估

**可行性: 可行 (4/5 数据源正常)**

| 区块 | 状态 | 质量 |
|------|------|------|
| UPM / Phase / KPI | 空状态（显示"未配置"） | N/A |
| User Stories 三列 | 正常 | 高 — 全部 5 个 Story 字段完整 |
| OpenSpec 列表 | 部分正常 | 中 — 36 个 Spec 中 8 个无法显示 Duration |
| Audit 历史 | 正常 | 中 — 仅 1 条记录（少于 5 条上限无问题） |
| AB Benchmark 摘要 | 正常 | 高 — 28 skills，数据完整 |

---

## 项目 2: Kairos (/home/dev/Kairos)

### 数据源可用性检查

#### DS-1: UPM (项目进度总览)

| 检查项 | 结果 |
|--------|------|
| 文件是否存在 | EXISTS — `/home/dev/Kairos/UPM.md` 存在 |
| 文件名格式 | NOT MATCHED — 文件名为 `UPM.md`，Skill 的 Glob 模式为 `**/unified-progress-management.md` |
| UPMv2-STATE 标记 | EXISTS 但格式不兼容 |
| 格式分析 | 使用 `## UPMv2-STATE` + ` ```yaml ``` ` 代码块，**不是** `<!-- UPMv2-STATE ... -->` HTML 注释 |
| Skill 提取正则 | `<!--\s*UPMv2-STATE\s*\n([\s\S]+?)\n-->` — 无法匹配当前格式 |
| YAML 内容字段 | 有 `phase`、`status`、`requirements`，**无** `kpi`、`currentCycle`、`risks` 字段 |

**状态: MISSING (双重不兼容)**

**根因 1**: 文件名不匹配。Skill 使用 Glob `**/unified-progress-management.md`，Kairos 的文件名为 `UPM.md`。

**根因 2**: 即使文件被找到，YAML 嵌套在 Markdown 代码块 (` ```yaml ```) 而非 HTML 注释 (`<!-- ... -->`) 中，Skill 提取正则无法匹配。

**根因 3**: Kairos UPM.md 的 YAML schema 与 Skill 期望的 schema 不兼容 — 缺少 `kpi`、`currentCycle`、`risks` 等字段。

**容错行为**: UPM 区块显示空状态，不中断其余解析。

---

#### DS-2: User Stories (三列看板)

| 检查项 | 结果 |
|--------|------|
| 路径存在 | YES — `docs/requirements/user-stories/` 存在 |
| 全部文件数量 | 26 个 .md 文件 |
| US-prefixed 文件数量 | 15 个 (US-001 — US-015 等) |
| 非 US 前缀文件 | 11 个 (MEM-001, MM-001, OPS-001, VOX-001 等) |
| ID 格式兼容性 | PARTIAL — US-prefixed 文件符合 `^(US-\d+)` 正则；非 US 前缀文件 ID 提取失败 |
| Status 字段 | NOT FOUND — Kairos 使用 `> **优先级**：P0` 中文字段，**无** `> **Status**: <value>` 英文字段 |
| Priority 字段 | NOT FOUND — 使用中文字段名 `**优先级**`，Skill 正则 `\*\*Priority\*\*:\s*(\w+)` 无法匹配 |

**状态: PARTIAL (严重格式偏差)**

**影响分析**:
- 全部 26 个 Story 的 Status 字段解析失败，所有 Story 将归入 TODO 列（默认值 `pending`）
- 全部 26 个 Story 的 Priority 字段解析失败，显示默认优先级 P3
- 11 个非 US 前缀文件 ID 提取失败，标题可能无法正确显示
- 看板三列看板将出现：26 个 TODO、0 个进行中、0 个已完成 — **严重失真**

---

#### DS-3: OpenSpec (活跃 + 归档)

| 检查项 | 结果 |
|--------|------|
| 活跃路径 | EXISTS — `openspec/changes/multi-provider-failover/proposal.md` (1 个) |
| 归档路径 | EXISTS — `openspec/archive/*/proposal.md` (31 个) |
| 活跃 Spec 字段格式 | 符合 — `multi-provider-failover` 有 Status/Level/Created 引用块字段 |
| 归档 Spec 字段覆盖率 | PARTIAL — 31 个中仅 6 个有完整 blockquote 字段 (19%)，18 个完全缺失，7 个部分缺失 |
| 早期归档格式 (2026-03-01) | 无 Status/Level/Created 字段 — 10 个 Phase 1 Spec 均为此格式 |
| 近期归档格式 (2026-03-22+) | 基本符合 — 最近 10 个归档 Spec 大多有完整字段 |
| 归档目录名格式 | 符合 — 均为 `YYYY-MM-DD-{name}` 格式 |

**状态: PARTIAL**

**耗时计算可行性**: 31 个归档 Spec 中，25 个无法计算耗时（缺少 Created 字段），6 个可计算，平均耗时数值可信度低。

---

#### DS-4: Audit Reports (审计历史)

| 检查项 | 结果 |
|--------|------|
| 路径存在 | MISSING — `.aria/audit-reports/` 目录不存在 |
| 替代位置 | `.aria/` 目录存在（含 `config.json`），但无 `audit-reports/` 子目录 |

**状态: MISSING**

**容错行为**: 审计历史区块显示空状态 "No audit reports found in .aria/audit-reports/"，不报错。

---

#### DS-5: AB Benchmark (基准测试摘要)

| 检查项 | 结果 |
|--------|------|
| aria-plugin-benchmarks/ 存在 | MISSING — Kairos 无此目录 |

**状态: MISSING (预期缺失)**

**容错行为**: Benchmark 区块显示空状态 "No AB benchmark results found in aria-plugin-benchmarks/"，不报错。

---

### Kairos 项目看板生成可行性评估

**可行性: 可行 (技术上可生成，但 3/5 数据源缺失或严重失真)**

| 区块 | 状态 | 质量 |
|------|------|------|
| UPM / Phase / KPI | 空状态（显示"未配置"） | N/A |
| User Stories 三列 | 严重失真 | 极低 — 所有 Story 状态/优先级无法解析 |
| OpenSpec 列表 | 部分正常 | 低 — 25/31 归档 Spec 无法显示 Duration |
| Audit 历史 | 空状态（无记录） | N/A |
| AB Benchmark 摘要 | 空状态（无目录） | N/A |

---

## 容错机制验证

### 缺失路径容错测试

按 SKILL.md 规范：**"任何数据源不存在或解析失败时，对应区块显示'未配置'，不报错，不中断。"**

| 场景 | 预期行为 | 验证结论 |
|------|---------|---------|
| UPM 文件不存在 (Aria) | 显示空状态，不报错 | PASS — 设计正确 |
| UPM 文件存在但格式不兼容 (Kairos) | 正则不匹配 → 返回 found:false → 显示空状态 | PASS — 设计正确 |
| Audit 目录不存在 (Kairos) | 显示空状态 | PASS — 设计正确 |
| Benchmark 目录不存在 (Kairos) | 显示空状态 | PASS — 设计正确 |
| Proposal 字段缺失 (两个项目的旧格式 Spec) | 跳过该字段，Duration 显示 `--` | PASS — 设计正确 |
| 非 US 前缀 Story 文件 ID 提取失败 (Kairos) | ID 为 null/空，标题可渲染，归入 TODO | PARTIAL — 行为可运行但输出有噪音 |
| Story Status 字段中文名 (Kairos) | 解析失败 → 默认 pending → 归入 TODO | 技术上不报错，但看板数据严重失真 |

**容错结论**: Skill 的容错设计覆盖了路径缺失场景，不会因任何单一数据源失败而崩溃。然而，格式不兼容（如 Kairos Stories）会导致静默的数据失真，用户得到的是形式上完整但内容严重偏离实际状态的看板。

---

## 缺陷与风险汇总

### 高优先级缺陷 (会导致数据失真)

| ID | 项目 | 数据源 | 问题描述 | 影响 |
|----|------|--------|---------|------|
| BUG-1 | 两个项目 | UPM | Skill Glob 模式 `**/unified-progress-management.md` 与实际文件名不兼容 | UPM 区块始终为空 |
| BUG-2 | Kairos | UPM | 即使文件名匹配，UPMv2-STATE 在代码块内而非 HTML 注释内，正则无法提取 | UPM 区块始终为空 |
| BUG-3 | Kairos | Stories | Story 文件使用中文字段名（`**优先级**`、无 Status 字段），Skill 正则无法解析 | 全部 26 个 Story 强制归入 TODO，三列看板严重失真 |
| BUG-4 | Kairos | Stories | 11 个非 US 前缀文件（MEM-、MM-、OPS-、VOX-）ID 提取失败 | 这些 Story 在看板中无有效 ID |

### 中优先级问题 (影响数据完整性)

| ID | 项目 | 数据源 | 问题描述 | 影响 |
|----|------|--------|---------|------|
| WARN-1 | Aria | OpenSpec | 8/36 归档 Spec 使用旧格式（列表/标题），无法提取 Duration | 这 8 个 Spec 耗时显示 `--` |
| WARN-2 | Kairos | OpenSpec | 25/31 归档 Spec 无 Created 字段，主要为 2026-03-22 前的早期 Spec | 平均耗时统计不具代表性 |
| WARN-3 | Aria | Audit | 仅 1 条审计报告，历史趋势无法体现 | 审计区块数据有限 |

### 低优先级观察

| ID | 项目 | 数据源 | 观察 |
|----|------|--------|------|
| INFO-1 | Kairos | Benchmark | 无 aria-plugin-benchmarks 目录，符合预期（Kairos 非 Aria Plugin 项目） |
| INFO-2 | Aria | Benchmark | `latest/` 目录存在且与 `2026-03-13/summary.yaml` 内容一致，解析路径明确 |

---

## 改进建议

### 必须修复 (阻塞跨项目可用性)

**REC-1: 扩展 UPM 文件名 Glob 模式**

当前 Glob `**/unified-progress-management.md` 无法匹配 `UPM.md`。建议扩展为多模式搜索：

```yaml
UPM 文件查找优先级:
  1. **/unified-progress-management.md  (标准名)
  2. **/UPM.md                          (简短名，Kairos 等项目使用)
  取第一个包含 "UPMv2-STATE" 字符串的文件
```

**REC-2: 扩展 UPMv2-STATE 提取格式**

当前仅支持 HTML 注释格式。建议增加 Markdown 代码块格式支持：

```
格式 1 (当前支持): <!-- UPMv2-STATE\n...\n-->
格式 2 (需新增):   ## UPMv2-STATE\n\n```yaml\n...\n```
```

**REC-3: 扩展 Story Status/Priority 字段解析**

当前解析仅支持 `> **Status**:` 和 `> **Priority**:` 英文字段名。建议增加中文字段名别名映射：

```yaml
Status 字段别名: Status | 状态
Priority 字段别名: Priority | 优先级
```

### 建议修复 (提升数据质量)

**REC-4: 对旧格式 OpenSpec 的字段格式升级**

Aria 项目有 8 个旧格式归档 Spec 使用列表/标题格式，Kairos 有 25 个。可以在 data-schema.md 中添加回退解析规则，或在 proposal.md 迁移时统一格式。

**REC-5: Kairos 补充 UPM kpi/cycle/risks 字段**

如果希望 Kairos 的看板展示 KPI 和周期进度，需在 `UPM.md` 中补充这些字段（它们在 Kairos 当前 schema 中缺失）。

---

## 结论

| 维度 | Aria | Kairos |
|------|------|--------|
| 技术上可生成看板 | YES | YES |
| 数据源覆盖率 | 4/5 (80%) | 2/5 (40%) |
| 看板数据可信度 | 中（UPM 缺失） | 低（UPM + Stories 均失真） |
| 容错不崩溃 | YES | YES |
| 数据静默失真风险 | 低 | 高 |

**Aria 项目** 可以生成一个有意义的看板，User Stories、OpenSpec、Audit 和 Benchmark 数据均可正常展示，主要缺陷是 UPM 区块为空（缺少 `unified-progress-management.md`）。

**Kairos 项目** 在当前状态下可以生成看板，但看板质量严重受限：User Stories 的三列分布完全失真（所有 Story 落入 TODO），OpenSpec 耗时统计不可信，UPM/Audit/Benchmark 均为空状态。建议优先修复 REC-1/REC-2/REC-3 后再在 Kairos 上测试看板功能。

---

**文件路径参考**:
- Skill 定义: `/home/dev/Aria/aria/skills/aria-dashboard/SKILL.md`
- Data Schema: `/home/dev/Aria/aria/skills/aria-dashboard/references/data-schema.md`
- Aria UPM: 不存在 (`**/unified-progress-management.md` 无结果)
- Aria Stories: `/home/dev/Aria/docs/requirements/user-stories/` (5 个 US-*.md)
- Aria Active Spec: `/home/dev/Aria/openspec/changes/aria-dashboard/proposal.md`
- Aria Archive: `/home/dev/Aria/openspec/archive/` (36 个 proposal.md)
- Aria Audit: `/home/dev/Aria/.aria/audit-reports/post_spec-2026-04-01T23.md`
- Aria Benchmark: `/home/dev/Aria/aria-plugin-benchmarks/ab-results/latest/summary.yaml`
- Kairos UPM: `/home/dev/Kairos/UPM.md` (存在但格式双重不兼容)
- Kairos Stories: `/home/dev/Kairos/docs/requirements/user-stories/` (26 个，15 个 US-前缀)
- Kairos Active Spec: `/home/dev/Kairos/openspec/changes/multi-provider-failover/proposal.md`
- Kairos Archive: `/home/dev/Kairos/openspec/archive/` (31 个，25 个缺少字段)
- Kairos Audit: 不存在 (`.aria/audit-reports/` 目录缺失)
- Kairos Benchmark: 不存在 (`aria-plugin-benchmarks/` 目录缺失)
