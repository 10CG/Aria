# requirements-validator-status-i18n-alignment

> **Level**: Minimal (Level 2 Spec — 仅 proposal.md, 无 tasks.md)
> **Status**: Complete (2026-04-26, archived per Level 2 micro-Spec "merge 后立即归档" convention)
> **Created**: 2026-04-25
> **Completed**: 2026-04-26 (aria-plugin PR #33 merged, commit 843e435; bundled with audit-engine-report-filename-uniqueness as v1.17.4 sister-bug release)
> **Type**: doc-only Skill prompt 文档同步
> **Source**: Round-2 latent-bug audit catalog P0.1 (`openspec/archive/2026-04-25-round-2-latent-bug-audit-findings/proposal.md` 第 41-48 行)
> **Related Spec**: `state-scanner-i18n-status-regex` (v1.17.2 已落地的 6-pattern union form 起源)
> **Related Memory**: `feedback_lessons_as_lint_audit_engine.md` (教训作为 lint 标准的跨 Skill 适用性)

---

## Why

`state-scanner-i18n-status-regex` (v1.17.2) 把 User Story 状态提取的 6 种文化习惯模式正式机械化为 `collectors/_status.py::_STATUS_PATTERNS`, 但 `requirements-validator` Skill 是独立的 LLM-driven Skill (allowed-tools: Read/Glob/Grep, 无 scripts), 它的 SKILL.md prompt 仍然只描述半角冒号 `Status: Draft|Review|Active|...` 的单一形式 (第 104, 138 行).

**风险**: 中文项目 (Kairos / 任何中文 adopter) 写 PRD/User Story 时常用全角冒号 `：` (中文 IME 默认) 或 heading-prefix `## Status: ...`. requirements-validator 在缺少 i18n 文档化的情况下, LLM 可能:
- 把 `**状态**：active` 误判为 "缺少 Status 字段"
- 把 `## Status: Active` 误判为 "格式不规范" (因不是 bold)
- 跨语言混用项目报多个 false-positive

**为何独立 Spec**: requirements-validator 是用户文档校验 Skill, 与 state-scanner 的状态收集 collector 是不同子系统; 一个负责 ingest (state-scanner), 一个负责 validate (requirements-validator). 它们对"何为合法 Status 行"的判定必须**机械等价**, 否则 ingest 看见的、validator 报错的不是同一份语义.

**为何不直接修而立 Spec**: SKILL.md prompt 改动会影响所有用 requirements-validator 的项目, 需要文档化决策路径与 reference 来源, 不是单行 patch.

---

## What

### 改动范围 (单文件 doc-only)

**File**: `aria/skills/requirements-validator/SKILL.md`

**改动 1**: 第 100-108 行 System Architecture `version_header.required_fields`
- 当前: `"Status" (Draft|Review|Active|Deprecated|Archived)`
- 改为: 引用 6-pattern union form, 明确接受半角 `:` + 全角 `：` + heading-prefix + blockquote + table cell + inline blockquote 6 种形式

**改动 2**: 第 132-148 行 User Story `header_fields.Status`
- 当前: `Status (draft/ready/in_progress/done/blocked)`
- 改为: 同上 6-pattern union form, 状态值列表保留

**改动 3**: 第 405-415 行 输出示例中的 `field: "Status"` issue 报告
- 增补: 当 LLM 找不到 Status 字段时, 必须先尝试 6 个模式后再报 "无效"

**改动 4** (新增 reference 段落):
在 SKILL.md 适当位置 (建议 "## 检查规范" 章节末尾) 新增子节:
```markdown
### Status 字段提取规范 (i18n alignment)

为与 state-scanner v1.17.2+ 的 collector 行为保持机械等价, Status 字段
提取按以下 6 个模式顺序匹配 (来源: `state-scanner/references/state-snapshot-schema.md`
第 142-153 行 _STATUS_PATTERNS):

| # | 模式 | 示例 |
|---|------|------|
| 1 | `**Status**[：:] X` | `**Status**: Active` |
| 2 | `**状态**[：:] X` | `**状态**：pending` |
| 3 | `> **Status**[：:] X` | `> **Status**: done` |
| 4 | `(#{1,6}\s+)?Status[：:] X` | `## Status: Reviewed` |
| 5 | `\| Status \| X \|` | `\| Status \| active \|` |
| 6 | `> ... **(Status\|状态)**[：:] X` | `> **优先级**：P0 \| **状态**：pending` |

**i18n 关键点**: 模式 1-4 的字符类 `[：:]` 同时接受 ASCII U+003A 和全角 U+FF1A
(中文 IME 默认). 模式 6 处理 inline blockquote 多 meta 行 (Kairos 项目实际样本).

**Negative case 不应误报**: prose 中提到 "状态" 而非 `**状态**` bold + blockquote
形式时, 不应被识别为 Status 字段缺失.
```

### 不改的内容

- Status 合法值列表 (Draft|Review|Active|... 等) 保持不变, 只扩展 *如何提取* 这一行的规则
- 不改 scripts/ (本 Skill 无 scripts)
- 不改其他 Skill (audit-engine 走 P0.2 独立 Spec)
- 不改 state-scanner (它已在 v1.17.2 完成对应改动)

---

## 非目标

- 不实施 collector 端补充 (state-scanner v1.17.2 已交付)
- 不写 unit test (本 Skill 是 LLM-driven, 无 Python 实现可测; benchmark 走 v1.17.4 smoke)
- 不引入新模式 (6 个固定, 与 state-snapshot-schema.md 契约对齐)
- 不改 PRD / Architecture / User Story 模板 (仅改 validator 看法, 不改用户写法)

## 验收

- [ ] `aria/skills/requirements-validator/SKILL.md` 4 处改动落地
- [ ] 引用 `state-snapshot-schema.md` 作为 SoT, 防止双源漂移
- [ ] smoke benchmark: 准备 1 个 mixed-i18n PRD 样本 + 1 个 User Story 样本, LLM 在不报 Status-missing 误判前提下完成 validation
- [ ] 与 P0.2 (audit-engine-report-filename-uniqueness) sister-bug bundling 合并, 走 v1.17.4 patch
- [ ] merge 后立即归档 (符合 Level 2 micro-Spec 节奏)

## 价值

- **跨 Skill 教训复用机械化**: state-scanner v1.17.2 教训外溢到 validator, 验证 `feedback_lessons_as_lint_audit_engine.md` 的可重复性
- **i18n 一等公民**: 中文项目 onboarding 不再因冒号字符差异遭遇 validator false-positive
- **SoT 单点管理**: 6-pattern 定义集中在 `state-snapshot-schema.md`, validator 引用而非复制, 防止漂移
